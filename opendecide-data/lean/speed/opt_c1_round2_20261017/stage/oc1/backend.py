"""oc1.backend: two ways to read C1 from a running SGLang server, both on PRE-TOKENIZED ids (the model input is identical).

  GenerateBackend   arm S1's readout: ONE POST /generate per decision, input_ids of every (question, view), prefill only
                    (max_new_tokens 0), token_ids_logprob = each sequence's candidate ids; group logit = logsumexp of the
                    candidates' log-probabilities (hosting/sglang_host.build_generate_body / parse_generate_response).
  ScoreBackend      SGLang's POST /v1/score with label_token_ids + apply_softmax: per question one call, query = the
                    common token prefix of the views, items = their remaining suffixes (query + item reproduces each view's
                    ids EXACTLY: the model sees the same tokens), single-item mode (each item its own prompt).
                    apply_softmax = softmax over the label tokens only, so a letter's probability is the sum of its
                    candidates' scores; log of that is fed to the same combine() as the S1 logits (T = 1.0 for both types,
                    so softmax over letters of log(mass) = mass: identical to decoder_io.to_probs up to fp rounding).

Both return (answers, meta) through fastcore.readout.combine, i.e. the A5 readout (2view probability average for choice,
single read for yes/no). `meta` carries http_ms (wall of the HTTP calls), prompt/cached tokens (generate only) and the
server's own e2e_latency (generate only).
"""
from __future__ import annotations

import math
import time
import uuid

from . import items as I


class BackendError(RuntimeError):
    pass


def common_prefix_len(a: list, b: list) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i


class GenerateBackend:
    name = "generate"

    def __init__(self, client, timeout: float = 120.0, temps=None):
        self.SH = I.sglang_host_mod()
        self.R = I.readout_mod()
        self.client, self.timeout, self.temps = client, timeout, temps

    def read(self, prep, return_views: bool = False):
        SH = self.SH
        body = SH.build_generate_body(prep.items, uuid.uuid4().hex)
        t0 = time.perf_counter()
        resp = self.client.generate(body, self.timeout)
        http_ms = (time.perf_counter() - t0) * 1000.0
        logits, meta = SH.parse_generate_response(prep.items, resp, body["rid"])
        answers, usage = self.R.combine(prep.named, prep.items, logits, self.temps, return_views=return_views)
        e2e = [r["meta_info"].get("e2e_latency") for r in resp if isinstance(r, dict)]
        e2e = [x for x in e2e if isinstance(x, (int, float))]
        return answers, {"http_ms": http_ms, "prompt_tokens": meta["prompt_tokens"], "cached_tokens": meta["cached_tokens"],
                         "server_e2e_ms": max(e2e) * 1000.0 if e2e else None, "n_seq": len(prep.items),
                         "usage": usage}

    def read_many(self, preps: list):
        """ONE /generate call carrying every sequence of several decisions (the 'batch of B decisions' timing)."""
        SH = self.SH
        flat = [it for p in preps for it in p.items]
        body = SH.build_generate_body(flat, uuid.uuid4().hex)
        t0 = time.perf_counter()
        resp = self.client.generate(body, self.timeout)
        http_ms = (time.perf_counter() - t0) * 1000.0
        logits, meta = SH.parse_generate_response(flat, resp, body["rid"])
        out, k = [], 0
        for p in preps:
            n = len(p.items)
            ans, _ = self.R.combine(p.named, p.items, logits[k:k + n], self.temps)
            out.append(ans)
            k += n
        return out, {"http_ms": http_ms, "n_seq": len(flat), "prompt_tokens": meta["prompt_tokens"],
                     "cached_tokens": meta["cached_tokens"]}


def score_body(items: list, model: str = "default") -> dict:
    """The /v1/score body of ONE question's views (all share the candidate ids)."""
    flat = items[0].flat
    if any(it.flat != flat for it in items):
        raise BackendError("views of one question must share the candidate ids")
    ids = [list(map(int, it.ids)) for it in items]
    if len(ids) == 1:
        p = max(len(ids[0]) - 1, 1)
    else:
        p = min(common_prefix_len(ids[0], ids[1]), min(len(x) for x in ids) - 1)
        p = max(p, 1)
    query = ids[0][:p]
    return {"model": model, "query": query, "items": [x[p:] for x in ids], "label_token_ids": list(map(int, flat)),
            "apply_softmax": True, "item_first": False}


def scores_to_logits(items: list, scores: list):
    """/v1/score scores (per item: softmax over label_token_ids, in that order) -> per-item tensor of per-group
    log-masses (the logits combine() expects). Raises BackendError on a malformed/degenerate answer."""
    import torch
    if not isinstance(scores, list) or len(scores) != len(items):
        raise BackendError(f"/v1/score returned {len(scores) if isinstance(scores, list) else type(scores).__name__} score "
                           f"rows for {len(items)} items")
    out = []
    for it, row in zip(items, scores):
        if not isinstance(row, list) or len(row) != len(it.flat):
            raise BackendError(f"score row has {len(row) if isinstance(row, list) else '?'} entries for {len(it.flat)} labels")
        parts, k = [], 0
        for s in it.sizes:
            parts.append(sum(float(x) for x in row[k:k + s]))
            k += s
        if not all(math.isfinite(m) and m >= 0 for m in parts) or sum(parts) <= 0:
            raise BackendError("non-finite or all-zero label masses")
        out.append(torch.tensor([math.log(m) if m > 0 else float("-inf") for m in parts], dtype=torch.float32))
    return out


class ScoreBackend:
    name = "score"

    def __init__(self, client, timeout: float = 120.0, temps=None, model: str = "default"):
        self.R = I.readout_mod()
        self.client, self.timeout, self.temps, self.model = client, timeout, temps, model

    def post_score(self, body: dict) -> list:
        import httpx
        try:
            r = self.client.c.post("/v1/score", json=body, timeout=httpx.Timeout(self.timeout, connect=5.0))
        except httpx.HTTPError as e:
            raise BackendError(f"/v1/score transport error: {type(e).__name__}: {e}") from e
        if r.status_code != 200:
            raise BackendError(f"/v1/score HTTP {r.status_code}: {r.text[:300]}")
        d = r.json()
        return d["scores"], d.get("usage")

    def read(self, prep, return_views: bool = False):
        by_q = {}
        for it in prep.items:
            by_q.setdefault(it.q, []).append(it)
        logits_by_item, http_ms, ptok = {}, 0.0, 0
        for q, its in sorted(by_q.items()):
            body = score_body(its, self.model)
            t0 = time.perf_counter()
            scores, usage = self.post_score(body)
            http_ms += (time.perf_counter() - t0) * 1000.0
            if usage and isinstance(usage.get("prompt_tokens"), int):
                ptok += usage["prompt_tokens"]
            for it, lg in zip(its, scores_to_logits(its, scores)):
                logits_by_item[id(it)] = lg
        logits = [logits_by_item[id(it)] for it in prep.items]
        answers, usage = self.R.combine(prep.named, prep.items, logits, self.temps, return_views=return_views)
        return answers, {"http_ms": http_ms, "prompt_tokens": ptok or None, "cached_tokens": None, "server_e2e_ms": None,
                         "n_seq": len(prep.items), "usage": usage}


def answer_probs(ans: dict, qtype: str) -> dict:
    """API v1 answer -> the stored-read format of speed_bench (yes/no {"yes","no"}, choice {option: p})."""
    if qtype == "noul":
        p = float(ans["noul"])
        return {"yes": p, "no": 1.0 - p}
    return {k: float(v) for k, v in ans["probabilities"].items()}
