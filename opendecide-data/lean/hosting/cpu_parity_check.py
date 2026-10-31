"""cpu_parity_check: a REAL-model CPU parity reference for C1, and a parity checker for any API v1 decider (SPEED-1,
hosting/SPEED1_DESIGN.md). NEW file; decoder_io, gate_dev and modal_direct_host (as core) are imported read-only.

C1 = Qwen/Qwen3.5-4B @ 851bf6e8 + LoRA q35_4b_main500k (adapter sha256 507d1c29..., checked before any load), loaded as
the server boots it (core.boot_gpu): decoder_io.load(BASE, "cpu", adapter=<Mac backup>, revision=REVISION,
return_info=True), then merge_and_unload, BF16. Readout = A5 = decoder_io.predict(tta_choice=True): choice reads the
given order and the exact reversal and averages them in probability space ("2view"), noul is one read, T = 1, and the
per-letter logits are fp32 logsumexps over Readout.cand(row) from the last real token.

  1. sample: a fixed, seeded, stratified 36-row sample of the 9 gate dev splits (SAMPLE_PLAN). It holds 12 noul rows
     (the longest one, 6 with a card, 5 without), 12 choice rows with 2-9 options (the longest one plus 11 spread) and
     12 choice rows with >= 10 options (the 3 longest, 2 more with > 26 options, and 7 with 10-26). Picks do not depend
     on file order: inside a split, rows are ranked by sha256(f"{SAMPLE_SEED}:{id}"), and splits take turns, rarest
     first. "Longest" means identity-read prompt tokens, as the server counts them.
  2. ref: C1 reads the sample on this laptop's CPU, one row at a time. Output goes to speed/cpu_ref/ref36.jsonl (per
     row: probs, which is the 2view read or the noul read, plus probs_identity, probs_reversed, tokens and ms) and to
     speed/cpu_ref/summary.json. The summary compares against the stored L4 reads
     preds_<split>/q35_4b_main500k_pre_served.jsonl (2view) and q35_4b_main500k_pre.jsonl (identity view).
     The 2view composition is checked bit for bit against decoder_io.predict(tta_choice=True) on two short rows, and
     check() with the in-process reference decider is checked against ref36.jsonl on the 4 shortest rows.
  3. check(decide_fn, rows, ref="stored" | path | [several]) -> summary. Each row goes to decide_fn as ONE API v1
     request (one question); decide_fn takes a v1 request dict and returns the v1 response dict. check() validates the
     v1 answer shape and compares with the stored reads and/or reference files on argmax agreement, |dp| stats,
     accuracy difference, first-view token counts and call ms.

Commands (from lean/; CPU only):
  ../.venv/bin/python hosting/cpu_parity_check.py sample                       the 36 rows (no model; ~15 s)
  ../.venv/bin/python hosting/cpu_parity_check.py ref [--threads N] [--resume]  C1 on CPU -> speed/cpu_ref/
  ../.venv/bin/python hosting/cpu_parity_check.py check --url URL --token TOKEN [--ref stored] [--ref PATH] [--out DIR]
  ../.venv/bin/python hosting/cpu_parity_check.py check --decider MODULE:FACTORY [--rows sample|PATH] [--limit N]
      (FACTORY() must return decide_fn; e.g. a fastcore host decider built on load_c1_cpu()'s model)
  ../.venv/bin/python -m pytest hosting/tests/test_cpu_parity_check.py
Cost guards: nothing here starts Modal, a GPU or a paid API (core is imported for its pure helpers only). The only
network use is the first `ref` run's public download of the pinned base snapshot into the default HF cache (~9 GB).
After that, `ref` runs with HF_HUB_OFFLINE=1. Only dev rows are read: a split named ohs* is refused before any file
is opened. CPU time: the 36 rows took 3.2 h on a 16 GB Apple M4 on 12 Oct (61K padded tokens, about 190 ms per padded
token; wall 3.3 h with the load and self-checks). On this CPU, BF16 GEMMs run at about 25 GFLOPS against about 210 for
fp32, and the 8.4 GB model swaps. summary.json records RAM, swap and peak RSS.

How this CPU read differs from the GPU reads (nothing pinned is edited; summary.json records what was actually used):
  - gated delta rule: the Mac has no fla/Triton, so transformers 5.17 runs its reference PyTorch kernels
    (torch_chunk_gated_delta_rule, fp32 inside, chunk 64). The GPU image (PINNED35) runs fla-core 0.5.2's Triton
    chunk kernel instead.
  - short conv: F.conv1d on both, because causal-conv1d is not in PINNED35, so nothing differs here.
  - attention: SDPA's CPU kernel in BF16, versus the CUDA flash / memory-efficient SDPA kernels.
  - matmuls: CPU BF16 GEMMs (fp32 accumulation; bit-identical across 4-10 threads here) versus cuBLAS, with
    different blocking and accumulation order.
  - LoRA merge: peft keeps the adapter in fp32 on a BF16 base (recorded: lora_dtype_before_merge), so on both devices
    the delta B@A*scale is computed in fp32 and added into the BF16 weight. Only fp32 GEMM rounding can differ.
  - batching: one row per call here (batch 1, padded to a multiple of 256 with a mask, as predict pads). The stored
    reads used predict's token-budget batches of up to 16 rows (right padding plus a mask). Everything is causal, so
    padding never reaches the last real token; only the numerics change.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
for _p in (str(HERE), str(LEAN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import modal_direct_host as core  # noqa: E402  (pure helpers: BASE, REVISION, sha256_file, lean_import, ...)
import gate_dev  # noqa: E402  (SPLITS, score, argmax_label)

MODEL = "q35_4b_main500k"
ADAPTER_SHA256 = "507d1c29690579f928a265713cd14b9c54a34baa8b74abd1e641560d987db078"
ADAPTER_DIR = LEAN.parent.parent / "backups" / "modal_models" / MODEL
DATA = LEAN / "data"
OUT = LEAN / "speed" / "cpu_ref"
REF36 = OUT / "ref36.jsonl"
STORED = {"stored_served": f"{MODEL}_pre_served", "stored_identity": f"{MODEL}_pre"}  # 2view / identity, L4 reads
SAMPLE_SEED = "speed1-cpu-ref:0"
AFFORD_TOKENS = 4096  # CPU budget per view; every dev row is shorter (longest >= 10-option row: 2,538 tokens)
# The SPEED1_DESIGN.md parity bars (gated in SPEED-2 on the 8,143-row P set against a same-session H100 read). On a
# 36-row sample, one flip is already 2.8 pt of agreement, so the bars are reported here as information only.
PARITY_BARS = {"argmax_agree_min": 0.995, "acc_diff_max_pt": 0.3, "acc_diff_max_pt_fp8": 1.0}
V1_TIMING = ("tokenize_ms", "queue_ms", "model_ms", "total_ms")
V1_TOP = ("answers", "usage", "timing", "server_ms", "engine", "path", "batch_rows")
MAX_V1_OPTIONS = 255
PROB_TOL = 1e-4  # a v1 answer's probabilities must sum to 1 within this (float32 softmax rounding)


def _log(*a):
    print(*a, flush=True)  # long CPU runs log to files: unbuffered progress


def _nopt(r) -> int:
    return len(r.get("options") or [])


STRATA = {  # stratum -> row predicate
    "noul_longest": lambda r: r["qtype"] == "noul",
    "noul_card": lambda r: r["qtype"] == "noul" and bool(r.get("card")),
    "noul_nocard": lambda r: r["qtype"] == "noul" and not r.get("card"),
    "choice_2_9_longest": lambda r: r["qtype"] == "choice" and 2 <= _nopt(r) <= 9,
    "choice_2_9": lambda r: r["qtype"] == "choice" and 2 <= _nopt(r) <= 9,
    "choice_ge10_longest": lambda r: r["qtype"] == "choice" and _nopt(r) >= 10,
    "choice_gt26": lambda r: r["qtype"] == "choice" and _nopt(r) > 26,
    "choice_10_26": lambda r: r["qtype"] == "choice" and 10 <= _nopt(r) <= 26,
}
# (stratum, rows, how) in pick order. "longest" = most identity-read tokens (<= AFFORD_TOKENS), ties by key; "spread" =
# round robin over splits, rarest split first, lowest key first inside a split. A row is picked at most once.
SAMPLE_PLAN = (
    ("noul_longest", 1, "longest"), ("noul_card", 6, "spread"), ("noul_nocard", 5, "spread"),
    ("choice_2_9_longest", 1, "longest"), ("choice_2_9", 11, "spread"),
    ("choice_ge10_longest", 3, "longest"), ("choice_gt26", 2, "spread"), ("choice_10_26", 7, "spread"),
)


def group_of(r) -> str:
    if r["qtype"] == "noul":
        return "noul"
    return "choice_ge10" if _nopt(r) >= 10 else "choice_2_9"


# ------------------------------------------------------------------ dev rows and the fixed sample (no model)

def gate_splits() -> list:
    return gate_dev.SPLITS.split(",")


def _refuse_protected(split: str):
    if "ohs" in split.lower():
        raise SystemExit(f"cpu_parity_check: DEV splits only ({split!r} refused before any file is opened)")


def load_dev(splits=None, data_dir=DATA) -> list:
    """Every row of the given dev splits (default: the 9 gate splits), each tagged with "_split" = its file name
    (a row's own "split" field is the source family, e.g. "dev" for dev_nc)."""
    splits = list(splits or gate_splits())
    for sp in splits:
        _refuse_protected(sp)
    out = []
    for sp in splits:
        with open(Path(data_dir) / f"{sp}.jsonl") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    r["_split"] = sp
                    out.append(r)
    return out


def row_key(seed, rid) -> str:
    return hashlib.sha256(f"{seed}:{rid}".encode()).hexdigest()


def sample_rows(rows, length_fn, seed=SAMPLE_SEED, plan=SAMPLE_PLAN, afford=AFFORD_TOKENS) -> list:
    """The stratified sample (see SAMPLE_PLAN), in plan order. length_fn(row) -> identity-read prompt tokens (the real
    counter for the fixed sample; any monotone proxy in tests). Each returned row is a copy carrying "_stratum",
    "_group" and "_tokens". Deterministic and independent of the order of `rows`. Raises if a stratum runs short."""
    taken, out, lens = set(), [], {}

    def length(r):
        if r["id"] not in lens:
            lens[r["id"]] = int(length_fn(r))
        return lens[r["id"]]

    for stratum, n, how in plan:
        cands = [r for r in rows if r["id"] not in taken and STRATA[stratum](r)]
        if how == "longest":
            ok = [r for r in cands if length(r) <= afford]
            picked = sorted(ok, key=lambda r: (-length(r), row_key(seed, r["id"])))[:n]
        elif how == "spread":
            by = defaultdict(list)
            for r in cands:
                by[r["_split"]].append(r)
            for v in by.values():
                v.sort(key=lambda r: row_key(seed, r["id"]))
            order = sorted(by, key=lambda s: (len(by[s]), s))
            picked = []
            while len(picked) < n and any(by[s] for s in order):
                for s in order:
                    if by[s] and len(picked) < n:
                        picked.append(by[s].pop(0))
        else:
            raise ValueError(f"unknown pick rule {how!r}")
        if len(picked) < n:
            raise ValueError(f"stratum {stratum}: only {len(picked)} eligible rows, the plan needs {n}")
        for r in picked:
            taken.add(r["id"])
            out.append({**r, "_stratum": stratum, "_group": group_of(r), "_tokens": length(r)})
    return out


def sample_sha(rows) -> str:
    return hashlib.sha256(json.dumps([r["id"] for r in rows]).encode()).hexdigest()


def prompt_counter(adapter_dir=ADAPTER_DIR, tok=None):
    """(dio, tok, ro, count). decoder_io is set to C1's layout and style (from the adapter's train_meta.json), the
    tokenizer is the one load() uses (the adapter folder's copy), the Readout's vocabulary scan sets the two-letter
    labels after Z, and count(row) returns the identity-read prompt tokens. This sets decoder_io.LAYOUT and STYLE in
    THIS process, to the same values decoder_io.load sets for C1."""
    dio = core.lean_import()
    info = dio.resolve_prompt([str(adapter_dir)], core.BASE, None, None, core.REVISION)
    dio.LAYOUT, dio.STYLE = info["layout"], info["style"]
    tok = tok or dio.load_tokenizer(core.BASE, adapter=str(adapter_dir), revision=info["revision"])
    ro = dio.Readout(tok)

    def count(row):
        return len(tok(ro.prompt(row), add_special_tokens=False)["input_ids"])
    return dio, tok, ro, count


def fixed_sample(count=None, data_dir=DATA) -> list:
    """The 36-row SPEED-1 CPU reference sample (real token counts)."""
    if count is None:
        count = prompt_counter()[3]
    return sample_rows(load_dev(data_dir=data_dir), count)


def rows_by_ids(ids, data_dir=DATA) -> list:
    """Dev rows (tagged with _split) in the order of `ids`; raises on an id that no gate dev split has."""
    by = {r["id"]: r for r in load_dev(data_dir=data_dir)}
    miss = [i for i in ids if i not in by]
    if miss:
        raise SystemExit(f"{len(miss)} ids not in the gate dev splits (first: {miss[0]})")
    return [by[i] for i in ids]


def ref36_rows(path=REF36, data_dir=DATA) -> list:
    """The sample rows recorded in a ref36.jsonl, rebuilt from the dev files (with _stratum/_group/_tokens), so a later
    check() runs exactly the rows the reference read without recounting tokens."""
    recs = read_jsonl(path)
    rows = rows_by_ids([x["id"] for x in recs], data_dir)
    return [{**r, "_stratum": x.get("stratum"), "_group": group_of(r), "_tokens": x.get("tokens_identity")}
            for r, x in zip(rows, recs)]


def read_jsonl(path) -> list:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


# ------------------------------------------------------------------ comparison math (no model)

def prob_keys(row) -> list:
    return ["yes", "no"] if row["qtype"] == "noul" else list(row["options"])


def top_label(row, probs) -> str:
    """gate_dev.argmax_label as a label: noul -> "yes" iff P(yes) > 0.5; choice -> the first option (in the row's
    option order) with the highest probability."""
    lab = gate_dev.argmax_label(row, probs)
    if row["qtype"] == "noul":
        return "yes" if lab else "no"
    return lab


def row_diff(row, p, q) -> dict:
    """One row: argmax agreement and |dp| = the largest |p - q| over the options (choice) or |P(yes) - Q(yes)| (noul:
    P(no) is 1 - P(yes) by construction, so it carries no extra information, only float rounding)."""
    keys = ["yes"] if row["qtype"] == "noul" else prob_keys(row)
    dp = max(abs(float(p.get(k, 0.0)) - float(q.get(k, 0.0))) for k in keys)
    a, b = top_label(row, p), top_label(row, q)
    return {"agree": a == b, "dp": dp, "top": a, "top_ref": b}


def pct(xs, q):
    """Nearest-rank percentile s[int(q*n)] (clamped), as client_bench / bench_api."""
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))] if s else None


def dp_stats(dps) -> dict:
    if not dps:
        return {"n": 0}
    return {"n": len(dps), "mean": statistics.fmean(dps), "p50": pct(dps, 0.5), "p95": pct(dps, 0.95),
            "max": max(dps), "n_gt_1e-3": sum(d > 1e-3 for d in dps), "n_gt_1e-2": sum(d > 1e-2 for d in dps),
            "n_gt_5e-2": sum(d > 5e-2 for d in dps)}


def ms_stats(ms) -> dict:
    if not ms:
        return {"n": 0}
    return {"n": len(ms), "mean": round(statistics.fmean(ms), 1), "p50": round(pct(ms, 0.5), 1),
            "p95": round(pct(ms, 0.95), 1), "max": round(max(ms), 1), "sum_s": round(sum(ms) / 1000, 1)}


def compare(rows, got, ref) -> dict:
    """got / ref: {id: probs}. Argmax agreement, |dp| stats (row max over keys), report-only accuracy of both (gate_dev
    score: ties and missing are wrong) and its difference in points, the same per group (noul / choice_2_9 /
    choice_ge10), and the SPEED-1 bars. Rows missing on either side are counted and left out of every number."""
    pairs, miss_got, miss_ref = [], [], []
    for r in rows:
        if r["id"] not in got:
            miss_got.append(r["id"])
        elif r["id"] not in ref:
            miss_ref.append(r["id"])
        else:
            pairs.append((r, row_diff(r, got[r["id"]], ref[r["id"]])))
    out = {"rows": len(pairs), "missing_got": len(miss_got), "missing_ref": len(miss_ref)}
    if not pairs:
        return {**out, "argmax_agree": None, "bars_pass": None}

    def block(ps):
        n = len(ps)
        acc = [(gate_dev.score(r, got[r["id"]])[0], gate_dev.score(r, ref[r["id"]])[0]) for r, _ in ps
               if r.get("gold") is not None]
        b = {"rows": n, "argmax_agree": round(sum(d["agree"] for _, d in ps) / n, 4),
             "n_disagree": sum(not d["agree"] for _, d in ps), "dp": dp_stats([d["dp"] for _, d in ps])}
        if acc:
            a_got, a_ref = statistics.fmean(x for x, _ in acc), statistics.fmean(y for _, y in acc)
            b.update(acc=round(a_got, 4), acc_ref=round(a_ref, 4), acc_diff_pt=round(100 * (a_got - a_ref), 2),
                     acc_rows=len(acc))
        return b

    out.update(block(pairs))
    out["disagree"] = [{"id": r["id"], "group": group_of(r), "top": d["top"], "top_ref": d["top_ref"],
                        "dp": round(d["dp"], 5)} for r, d in pairs if not d["agree"]]
    by = defaultdict(list)
    for r, d in pairs:
        by[group_of(r)].append((r, d))
    out["by_group"] = {g: block(v) for g, v in sorted(by.items())}
    out["bars"] = PARITY_BARS
    out["bars_pass"] = bool(out["argmax_agree"] >= PARITY_BARS["argmax_agree_min"]
                            and abs(out.get("acc_diff_pt", 0.0)) <= PARITY_BARS["acc_diff_max_pt"])
    return out


@lru_cache(maxsize=32)
def _stored_split(split, name) -> dict:
    _refuse_protected(split)
    p = LEAN / f"preds_{split}" / f"{name}.jsonl"
    if not p.exists():
        raise SystemExit(f"missing stored read {p}")
    return {o["id"]: o["probs"] for o in read_jsonl(p)}


def stored_reads(which, rows) -> dict:
    """{id: probs} of a stored L4 read ("stored_served" = 2view, "stored_identity" = identity view) for these rows,
    from preds_<_split>/ (rows without _split: looked up across the 9 gate splits; ids are unique across them)."""
    name = STORED[which]
    splits = {r.get("_split") for r in rows}
    if None in splits:
        splits = set(gate_splits())
    out = {}
    for sp in sorted(splits):
        out.update(_stored_split(sp, name))
    return out


def load_ref(ref, rows) -> dict:
    """{name: {id: probs}}. "stored" = both stored reads (2view first, the identity view as context); "stored_served" /
    "stored_identity" = one of them; anything else = a jsonl path whose lines have "id" and "probs" (e.g.
    ref36.jsonl)."""
    if ref == "stored":
        return {k: stored_reads(k, rows) for k in STORED}
    if ref in STORED:
        return {ref: stored_reads(ref, rows)}
    p = Path(ref)
    if "ohs" in str(p).lower():
        raise SystemExit(f"refused: {p} (protected path)")
    return {str(p): {o["id"]: o["probs"] for o in read_jsonl(p)}}


# ------------------------------------------------------------------ API v1 (request builder, answer validation)

def v1_request(row, qname="q0") -> dict:
    """One dev row as one API v1 request with one question; the card goes in as is (noul or choice)."""
    q = {"type": row["qtype"], "instructions": row["instructions"]}
    if row["qtype"] == "choice":
        q["options"] = list(row["options"])
    if row.get("card"):
        q["card"] = row["card"]
    return {"id": row["id"], "state": row["state"], "questions": {qname: q}}


def rows_from_v1(req) -> list:
    """[(name, decoder_io row)] from an API v1 request (the reference decider's parser; the hosts have their own).
    The row holds exactly {"state", "instructions", "qtype", "options", "card"}, the fields decoder_io's prompt reads,
    so its prompt is byte-identical to the dev row's. Raises ValueError on a request that breaks v1."""
    if not isinstance(req, dict) or not isinstance(req.get("state"), str):
        raise ValueError('"state" must be a string')
    qs = req.get("questions")
    if not isinstance(qs, dict) or not qs:
        raise ValueError('"questions" must be a non-empty object')
    if len(qs) > core.MAX_QUESTIONS:
        raise ValueError(f"at most {core.MAX_QUESTIONS} questions per request")
    out = []
    for k, q in qs.items():
        if not isinstance(q, dict) or q.get("type") not in ("noul", "choice"):
            raise ValueError(f'{k}: "type" must be "noul" or "choice"')
        if not isinstance(q.get("instructions"), str) or not q["instructions"].strip():
            raise ValueError(f'{k}: "instructions" must be a non-empty string')
        card = q.get("card")
        if card is not None and not isinstance(card, str):
            raise ValueError(f'{k}: "card" must be a string')
        row = {"state": req["state"], "instructions": q["instructions"], "qtype": q["type"], "options": None,
               "card": card or None}
        if q["type"] == "choice":
            o = q.get("options")
            if not isinstance(o, list) or not all(isinstance(x, str) and x.strip() for x in o):
                raise ValueError(f'{k}: a choice needs "options" (a list of non-empty strings)')
            if not 2 <= len(o) <= MAX_V1_OPTIONS:
                raise ValueError(f"{k}: 2 to {MAX_V1_OPTIONS} options")
            if len(set(o)) != len(o):
                raise ValueError(f"{k}: duplicate options")
            row["options"] = list(o)
        out.append((k, row))
    return out


def v1_answer(row, probs, usage) -> dict:
    """The v1 answer object for one question from its readout probabilities (keyed yes/no or by option)."""
    if row["qtype"] == "noul":
        p = float(probs["yes"])
        return {"type": "noul", "noul": p, "probabilities": {"yes": p, "no": 1 - p}, "usage": usage}
    pr = {o: float(probs[o]) for o in row["options"]}
    best = max(pr, key=pr.get)
    return {"type": "choice", "choice": best, "confidence": pr[best], "probabilities": pr, "usage": usage}


def v1_probs(row, ans) -> tuple:
    """(probs keyed like the stored reads, or None when unusable; [problems]) for one v1 answer object."""
    probs = None
    if not isinstance(ans, dict):
        return None, ["answer missing or not an object"]
    bad = [] if ans.get("type") == row["qtype"] else [f"type {ans.get('type')!r} != {row['qtype']!r}"]
    pr = ans.get("probabilities")
    if row["qtype"] == "noul":
        p = ans.get("noul")
        if not isinstance(p, (int, float)) or not 0.0 <= p <= 1.0:
            return None, bad + [f"noul {p!r} is not a probability"]
        probs = {"yes": float(p), "no": 1.0 - float(p)}
        if not isinstance(pr, dict) or set(pr) != {"yes", "no"}:
            bad.append("noul probabilities must be {yes, no}")
        elif abs(float(pr["yes"]) - p) > 1e-6 or abs(float(pr["yes"]) + float(pr["no"]) - 1.0) > PROB_TOL:
            bad.append("noul probabilities disagree with noul / do not sum to 1")
    else:
        if not isinstance(pr, dict) or any(o not in pr for o in row["options"]):
            return None, bad + ["probabilities missing an option"]
        probs = {o: float(pr[o]) for o in row["options"]}
        if set(pr) != set(row["options"]):
            bad.append("probabilities have keys that are not options")
        if abs(sum(probs.values()) - 1.0) > PROB_TOL:
            bad.append(f"probabilities sum to {sum(probs.values()):.6f}")
        best = max(probs.values())
        if ans.get("choice") not in probs or probs[ans["choice"]] != best:
            bad.append("choice is not the argmax")
        if not isinstance(ans.get("confidence"), (int, float)) or abs(ans["confidence"] - best) > 1e-6:
            bad.append("confidence != the top probability")
    u = ans.get("usage")
    want_views = 2 if row["qtype"] == "choice" else 1
    if not isinstance(u, dict) or any(k not in u for k in ("input_tokens", "input_tokens_first_view", "views")):
        bad.append("answer usage missing input_tokens / input_tokens_first_view / views")
    elif u["views"] != want_views:
        bad.append(f"views {u['views']} != {want_views} (A5: 2view for choice, one read for noul)")
    return probs, bad


def v1_response_problems(resp) -> list:
    if not isinstance(resp, dict):
        return ["response is not an object"]
    bad = [f"response missing {k!r}" for k in V1_TOP if k not in resp]
    if isinstance(resp.get("timing"), dict):
        bad += [f"timing missing {k!r}" for k in V1_TIMING if k not in resp["timing"]]
    if isinstance(resp.get("usage"), dict):
        bad += [f"usage missing {k!r}" for k in ("input_tokens", "routed_rows") if k not in resp["usage"]]
    if "engine" in resp and resp["engine"] not in ("hf", "sglang"):
        bad.append(f"engine {resp['engine']!r} not hf/sglang")
    return bad


def check(decide_fn, rows, ref="stored", qname="q0", log=_log, keep_rows=True) -> dict:
    """Send every row as one v1 request (one question) to decide_fn (v1 request dict -> v1 response dict), validate
    the answers, and compare them with each reference: "stored" (the stored L4 2view read first, its identity read as
    context), "stored_served", "stored_identity", or a jsonl path with {"id", "probs"} lines (e.g. ref36.jsonl);
    several may be given as a list. First-view token counts are checked against row["_tokens"] (the local count) when
    both exist. Returns the summary; per-row records go in summary["per_row"] unless keep_rows=False."""
    refs = [ref] if isinstance(ref, (str, Path)) else list(ref)
    got, per, errors, probs_bad, ms = {}, [], [], Counter(), []
    tok_cmp, tok_bad = 0, []
    t_all = time.perf_counter()
    for i, r in enumerate(rows):
        req = v1_request(r, qname)
        t0 = time.perf_counter()
        try:
            resp = decide_fn(req)
        except Exception as e:  # noqa: BLE001 - a failing call is a result, not a crash
            errors.append({"id": r["id"], "error": f"{type(e).__name__}: {e}"[:300]})
            continue
        dt = (time.perf_counter() - t0) * 1000
        ms.append(dt)
        bad = v1_response_problems(resp)
        ans = (resp.get("answers") or {}).get(qname) if isinstance(resp, dict) else None
        probs, b2 = v1_probs(r, ans)
        bad += b2
        for b in bad:
            probs_bad[b] += 1
        if probs is not None:
            got[r["id"]] = probs
        ftv = ((ans or {}).get("usage") or {}).get("input_tokens_first_view") if isinstance(ans, dict) else None
        if ftv is not None and r.get("_tokens") is not None:
            tok_cmp += 1
            if int(ftv) != int(r["_tokens"]):
                tok_bad.append({"id": r["id"], "server": int(ftv), "local": int(r["_tokens"])})
        per.append({"id": r["id"], "split": r.get("_split"), "group": group_of(r), "ms": round(dt, 2),
                    "probs": probs, "top": top_label(r, probs) if probs else None, "problems": bad,
                    "tokens_first_view": ftv, "path": resp.get("path") if isinstance(resp, dict) else None,
                    "server_ms": resp.get("server_ms") if isinstance(resp, dict) else None})
        if log and (i + 1) % 10 == 0:
            log(f"check: {i + 1}/{len(rows)} rows")
    vs, by_id = {}, {r["id"]: r for r in rows}
    for rf in refs:
        for name, refmap in load_ref(rf, rows).items():
            vs[name] = compare(rows, got, refmap)
            for x in per:
                if x["probs"] is not None and x["id"] in refmap:
                    d = row_diff(by_id[x["id"]], x["probs"], refmap[x["id"]])
                    x.setdefault("vs", {})[name] = {"agree": d["agree"], "dp": d["dp"]}
    primary = next(iter(vs), None)
    out = {"rows": len(rows), "answered": len(got), "errors": len(errors), "error_examples": errors[:5],
           "schema_problems": dict(probs_bad), "call_ms": ms_stats(ms), "wall_s": round(time.perf_counter() - t_all, 1),
           "tokens_first_view": {"compared": tok_cmp, "mismatch": len(tok_bad), "examples": tok_bad[:5]},
           "primary_ref": primary, "vs": vs,  # clean_run: every row answered in v1 shape (parity is in "vs")
           "clean_run": bool(primary and not errors and not probs_bad and not tok_bad
                             and vs[primary]["missing_got"] == 0)}
    if keep_rows:
        out["per_row"] = per
    return out


def http_decider(url, token, timeout=900.0):
    """decide_fn for an HTTP host (POST /decide with the bearer token); decide.close() closes the connection."""
    import httpx
    c = httpx.Client(base_url=url.rstrip("/"), timeout=timeout, headers={"Authorization": f"Bearer {token}"})

    def decide(req):
        r = c.post("/decide", json=req)
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        return r.json()
    decide.close = c.close
    return decide


# ------------------------------------------------------------------ the real model on CPU

def hf_home() -> Path:
    return Path(os.environ.get("HF_HOME") or Path.home() / ".cache" / "huggingface")


def verify_adapter(adapter_dir=ADAPTER_DIR) -> str:
    got = core.sha256_file(Path(adapter_dir) / "adapter_model.safetensors")
    if got != ADAPTER_SHA256:
        raise SystemExit(f"{adapter_dir}: adapter sha256 {got} != pinned {ADAPTER_SHA256}")
    return got


def _sysctl(key):
    try:
        return subprocess.run(["sysctl", "-n", key], capture_output=True, text=True, timeout=5).stdout.strip() or None
    except Exception:  # noqa: BLE001 - not macOS
        return None


def runtime_info(model=None) -> dict:
    import resource
    from importlib.util import find_spec

    import peft
    import tokenizers
    import torch
    import transformers
    fla = find_spec("fla") is not None
    sysctl = _sysctl
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # bytes on macOS, KiB on Linux
    mem = {"ram_gb": round(int(sysctl("hw.memsize") or 0) / 2 ** 30, 1),
           "peak_rss_gb": round(rss / (2 ** 30 if sys.platform == "darwin" else 2 ** 20), 2),
           "swap_usage": sysctl("vm.swapusage"),
           "note": "CPU ms depend on memory pressure: an 8.4 GB BF16 model on a 16 GB laptop with other apps open "
                   "swaps, so these timings are an upper bound, not a compute measurement"}
    info = {"python": platform.python_version(), "platform": platform.platform(), "machine": platform.machine(),
            "cpu": sysctl("machdep.cpu.brand_string") or platform.processor(), "torch": torch.__version__,
            "transformers": transformers.__version__, "peft": peft.__version__, "tokenizers": tokenizers.__version__,
            "torch_threads": torch.get_num_threads(),
            "fla_installed": fla, "causal_conv1d_installed": find_spec("causal_conv1d") is not None,
            "gated_delta_rule": "fla (Triton)" if fla else "transformers reference torch_chunk_gated_delta_rule (fp32)",
            "hf_hub_offline": os.environ.get("HF_HUB_OFFLINE"), "memory": mem}
    if model is not None:
        dts = Counter(str(p.dtype) for p in model.parameters())
        cfg = getattr(model.config, "text_config", None) or model.config
        info.update(model_class=type(model).__name__, param_dtypes=dict(dts),
                    n_params=sum(p.numel() for p in model.parameters()),
                    attn_implementation=getattr(model.config, "_attn_implementation", None),
                    softcap=getattr(cfg, "final_logit_softcapping", None))
    return info


def load_c1_cpu(adapter_dir=ADAPTER_DIR, threads=None, log=_log):
    """C1 on CPU exactly as core.boot_gpu loads it (dio.load + merge_and_unload, BF16): (dio, model, tok, info).
    The adapter sha256 is checked first. When the pinned base snapshot is complete in the HF cache, the load runs with
    HF_HUB_OFFLINE=1 (set before transformers / huggingface_hub are imported here)."""
    import torch
    t0 = time.time()
    info = {"base": core.BASE, "revision": core.REVISION, "adapter": str(adapter_dir), "model": MODEL,
            "adapter_sha256": verify_adapter(adapter_dir)}
    if core.base_snapshot_complete(str(hf_home())):
        os.environ["HF_HUB_OFFLINE"] = "1"
        info["base_source"] = f"{hf_home()} snapshot (offline)"
        info["hub_imported_before_offline"] = "huggingface_hub" in sys.modules
    else:
        info["base_source"] = "Hugging Face Hub download (public weights, pinned revision)"
    if threads:
        torch.set_num_threads(int(threads))
    dio = core.lean_import()
    model, tok, load_info = dio.load(core.BASE, "cpu", adapter=str(adapter_dir), revision=core.REVISION,
                                     return_info=True)
    lora = Counter(str(p.dtype) for n, p in model.named_parameters() if "lora_" in n)
    model = model.merge_and_unload()
    model.eval()
    import gc
    gc.collect()
    commit = getattr(model.config, "_commit_hash", None)
    if commit is not None and commit != core.REVISION:
        raise SystemExit(f"loaded base commit {commit}, pinned {core.REVISION}")
    info.update(load={k: load_info.get(k) for k in ("layout", "style", "revision", "prism_x", "chat_template_sha")},
                base_commit=commit, lora_dtype_before_merge=dict(lora), merged=True,
                load_s=round(time.time() - t0, 1))
    if load_info.get("prism_x"):
        raise SystemExit("C1 has no PRISM-X; a prism_x.json here means the wrong adapter")
    meta = LEAN / "preds_dev" / f"{STORED['stored_served']}.meta.json"  # the stored read's own load record
    if meta.exists():
        want = (json.loads(meta.read_text()).get("load") or {})
        info["matches_stored_read_load"] = {k: load_info.get(k) == want.get(k)
                                            for k in ("layout", "style", "revision", "chat_template_sha")}
    log(f"C1 loaded on CPU in {info['load_s']} s: {json.dumps(info['load'])}")
    return dio, model, tok, info


def read_row(dio, model, ro, row, dev="cpu") -> dict:
    """decoder_io's reference readout of one row at batch 1. The identity view is cand_logits + to_probs (what predict
    without TTA does, = the _pre read). For choice, the exact reversal is read too, and the 2view probs are their mean
    in probability space, with the same arithmetic as predict(tta_choice=True). Also returns token counts and ms."""
    import torch
    perm_id = None
    views = [perm_id]
    if row["qtype"] == "choice":
        views.append(list(range(len(row["options"])))[::-1])
    ntok = [len(ro.tok(dio.prompt_texts(ro, [row], [p])[0], add_special_tokens=False)["input_ids"]) for p in views]
    out = {"tokens_identity": ntok[0], "tokens_views": ntok,
           "padded_len": [-(-n // dio.PAD_MULTIPLE) * dio.PAD_MULTIPLE for n in ntok], "views": len(views)}
    t0 = time.perf_counter()
    with torch.no_grad():
        lg = dio.cand_logits(model, ro, [row], dev)[0]
    t1 = time.perf_counter()
    p_id = dio.to_probs(row, lg)
    out["probs_identity"] = dict(p_id)
    out["ms_views"] = [round((t1 - t0) * 1000, 1)]
    if row["qtype"] == "choice":
        rev = views[1]
        with torch.no_grad():
            lg2 = dio.cand_logits(model, ro, [row], dev, perms=[rev])[0]
        out["ms_views"].append(round((time.perf_counter() - t1) * 1000, 1))
        p_rev = dio.to_probs(row, lg2, rev)
        out["probs_reversed"] = {o: p_rev[o] for o in row["options"]}
        out["probs"] = {o: (p_id[o] + p_rev[o]) / 2 for o in row["options"]}
    else:
        out["probs"] = dict(p_id)
    out["ms"] = round(sum(out["ms_views"]), 1)
    return out


def reference_decider(dio, model, ro, dev="cpu"):
    """An API v1 decide_fn on decoder_io's reference readout (eager, one view at a time, no batching): the yardstick a
    fast host must match. Its timing is indicative only (cand_logits tokenizes again inside model_ms)."""
    def decide(req):
        t0 = time.perf_counter()
        named = rows_from_v1(req)
        answers, n_in, model_ms = {}, 0, 0.0
        for k, row in named:
            rd = read_row(dio, model, ro, row, dev)
            usage = {"input_tokens": sum(rd["tokens_views"]), "input_tokens_first_view": rd["tokens_identity"],
                     "views": rd["views"]}
            n_in += usage["input_tokens"]
            model_ms += rd["ms"]
            answers[k] = v1_answer(row, rd["probs"], usage)
        total = (time.perf_counter() - t0) * 1000
        return {"answers": answers, "usage": {"input_tokens": n_in, "routed_rows": 0},
                "timing": {"tokenize_ms": None, "queue_ms": 0.0, "model_ms": round(model_ms, 2),
                           "total_ms": round(total, 2)},
                "server_ms": round(total, 2), "engine": "hf", "path": "eager", "batch_rows": len(named)}
    return decide


def predict_selfcheck(dio, model, tok, ro, recs_by_id, rows) -> dict:
    """read_row's 2view composition == decoder_io.predict(tta_choice=True) bit for bit, and its identity view ==
    predict() (no TTA), on the shortest noul and the shortest choice row of the sample."""
    out = {}
    for g in ("noul", "choice"):
        cands = [r for r in rows if r["qtype"] == g and r["id"] in recs_by_id]
        if not cands:
            continue
        r = min(cands, key=lambda x: recs_by_id[x["id"]]["tokens_identity"])
        p2 = dio.predict(model, tok, [r], dev="cpu", tta_choice=True)[0]
        d2 = max(abs(p2[k] - recs_by_id[r["id"]]["probs"][k]) for k in prob_keys(r))
        rec = {"id": r["id"], "max_abs_diff_2view_vs_predict": d2}
        if g == "choice":
            p1 = dio.predict(model, tok, [r], dev="cpu")[0]
            rec["max_abs_diff_identity_vs_predict"] = max(abs(p1[k] - recs_by_id[r["id"]]["probs_identity"][k])
                                                          for k in prob_keys(r))
        out[g] = rec
    out["pass"] = all(v.get("max_abs_diff_2view_vs_predict") == 0.0 and v.get("max_abs_diff_identity_vs_predict", 0.0)
                      == 0.0 for v in out.values() if isinstance(v, dict))
    return out


def file_sha(p) -> str:
    return core.sha256_file(p)


def summarize_ref(rows, recs) -> dict:
    """Comparison of the CPU reads (2view and identity) with the stored L4 reads, plus CPU time per row."""
    by = {x["id"]: x for x in recs}
    rows = [r for r in rows if r["id"] in by]
    served = {i: x["probs"] for i, x in by.items()}
    ident = {i: x["probs_identity"] for i, x in by.items()}
    res = {"cpu_2view_vs_stored_served": compare(rows, served, stored_reads("stored_served", rows)),
           "cpu_identity_vs_stored_identity": compare(rows, ident, stored_reads("stored_identity", rows)),
           "context_stored_identity_vs_stored_served": compare(rows, stored_reads("stored_identity", rows),
                                                               stored_reads("stored_served", rows))}
    ms = [by[r["id"]]["ms"] for r in rows]
    toks = [sum(by[r["id"]]["tokens_views"]) for r in rows]
    padded = [sum(by[r["id"]]["padded_len"]) for r in rows]
    per_g = defaultdict(list)
    for r in rows:
        per_g[group_of(r)].append(by[r["id"]]["ms"])
    res["cpu_time"] = {"ms_per_row": ms_stats(ms), "by_group": {g: ms_stats(v) for g, v in sorted(per_g.items())},
                       "tokens_read_total": sum(toks), "padded_tokens_total": sum(padded),
                       "ms_per_1k_tokens_read": round(sum(ms) / max(1, sum(toks)) * 1000, 1),
                       "ms_per_1k_padded_tokens": round(sum(ms) / max(1, sum(padded)) * 1000, 1),
                       "note": "per row: prompt render + tokenization + eager forward + readout, every view, batch 1"}
    return res


def run_reference(out_dir=OUT, threads=None, resume=False, limit=None, log=_log) -> dict:
    """Load C1 on CPU, read the fixed sample, write ref36.jsonl + summary.json, run the two self-checks."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    dio, model, tok, load = load_c1_cpu(threads=threads, log=log)
    _, _, ro, count = prompt_counter(tok=tok)
    t = time.time()
    rows = fixed_sample(count)
    sha = sample_sha(rows)
    log(f"sample: {len(rows)} rows, sha {sha[:16]}, built in {time.time() - t:.0f} s")
    if limit:
        rows = rows[:limit]
    part = out_dir / "ref36.partial.jsonl"
    done = {}
    if resume and part.exists():
        done = {x["id"]: x for x in read_jsonl(part) if x.get("sample_sha") == sha}
        log(f"resume: {len(done)} rows already read")
    with open(part, "a" if resume else "w") as f:
        for i, r in enumerate(rows):
            if r["id"] in done:
                continue
            rd = read_row(dio, model, ro, r)
            if rd["tokens_identity"] != r["_tokens"]:
                raise SystemExit(f"{r['id']}: token count {rd['tokens_identity']} != sample count {r['_tokens']}")
            rec = {"id": r["id"], "split": r["_split"], "stratum": r["_stratum"], "group": r["_group"],
                   "qtype": r["qtype"], "n_options": _nopt(r), "has_card": bool(r.get("card")), "gold": r.get("gold"),
                   **rd, "top": top_label(r, rd["probs"]), "sample_sha": sha}
            done[r["id"]] = rec
            f.write(json.dumps(rec) + "\n")
            f.flush()
            log(f"[{i + 1}/{len(rows)}] {r['_stratum']:20s} {r['id']} tok {rd['tokens_views']} {rd['ms']:.0f} ms")
    recs = [done[r["id"]] for r in rows]
    path = out_dir / "ref36.jsonl"
    path.write_text("".join(json.dumps(x) + "\n" for x in recs))
    part.unlink(missing_ok=True)
    summary = {"what": "SPEED-1 CPU parity reference: C1 read on CPU with decoder_io's A5 readout (2view choice, "
                       "noul single read, T=1), compared with the stored L4 reads",
               "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": load,
               "runtime": runtime_info(model),
               "sample": {"seed": SAMPLE_SEED, "plan": [list(x) for x in SAMPLE_PLAN], "afford_tokens": AFFORD_TOKENS,
                          "rows": len(rows), "sha256_ids": sha, "full": limit is None,
                          "by_stratum": dict(Counter(r["_stratum"] for r in rows)),
                          "by_group": dict(Counter(r["_group"] for r in rows)),
                          "by_split": dict(Counter(r["_split"] for r in rows)),
                          "gt26_options": sum(_nopt(r) > 26 for r in rows),
                          "noul_with_card": sum(r["qtype"] == "noul" and bool(r.get("card")) for r in rows)},
               "inputs_sha256": {**{f"data/{sp}.jsonl": file_sha(DATA / f"{sp}.jsonl")
                                    for sp in sorted({r['_split'] for r in rows})},
                                 **{f"preds_{sp}/{n}.jsonl": file_sha(LEAN / f"preds_{sp}" / f"{n}.jsonl")
                                    for sp in sorted({r['_split'] for r in rows}) for n in STORED.values()}},
               **summarize_ref(rows, recs)}
    log("self-check: read_row vs decoder_io.predict ...")
    summary["selfcheck_vs_predict"] = predict_selfcheck(dio, model, tok, ro, done, rows)
    short = sorted(rows, key=lambda r: r["_tokens"])[:4]
    dc = check(reference_decider(dio, model, ro), short, ref=[str(path)], log=None, keep_rows=False)
    summary["selfcheck_reference_decider"] = {"rows": [r["id"] for r in short], "ok": dc["clean_run"]
                                              and dc["vs"][str(path)]["dp"]["max"] == 0.0,
                                              "vs_ref36": dc["vs"][str(path)], "schema_problems": dc["schema_problems"],
                                              "tokens_first_view": dc["tokens_first_view"]}
    summary["wall_s"] = round(time.time() - t_start, 1)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1))
    log(short_report(summary))
    return summary


def short_report(s) -> str:
    a, b = s["cpu_2view_vs_stored_served"], s["cpu_identity_vs_stored_identity"]
    t = s["cpu_time"]
    L = [f"CPU ref ({s['sample']['rows']} rows, {s['runtime']['cpu']}, {s['runtime']['torch_threads']} threads):",
         f"  2view vs stored L4 2view:      argmax {a['argmax_agree']} ({a['n_disagree']} flips), |dp| mean "
         f"{a['dp']['mean']:.4f} p95 {a['dp']['p95']:.4f} max {a['dp']['max']:.4f}, acc diff {a.get('acc_diff_pt')} pt",
         f"  identity vs stored L4 identity: argmax {b['argmax_agree']} ({b['n_disagree']} flips), |dp| mean "
         f"{b['dp']['mean']:.4f} p95 {b['dp']['p95']:.4f} max {b['dp']['max']:.4f}",
         f"  CPU ms/row: mean {t['ms_per_row']['mean']} p50 {t['ms_per_row']['p50']} max {t['ms_per_row']['max']} "
         f"({t['ms_per_1k_tokens_read']} ms per 1K tokens read)"]
    if "selfcheck_vs_predict" in s:
        L.append(f"  self-checks: predict {'PASS' if s['selfcheck_vs_predict']['pass'] else 'FAIL'}, reference decider "
                 f"{'PASS' if s['selfcheck_reference_decider']['ok'] else 'FAIL'}")
    return "\n".join(L)


# ------------------------------------------------------------------ CLI

def _load_rows_arg(spec, limit):
    if spec == "sample":
        rows = ref36_rows() if REF36.exists() else fixed_sample()
    else:
        p = Path(spec)
        if "ohs" in str(p).lower():
            raise SystemExit(f"refused: {p} (protected path)")
        items = read_jsonl(p)
        rows = rows_by_ids([x["id"] for x in items])
    return rows[:limit] if limit else rows


def _decider_from(spec):
    mod, _, fn = spec.partition(":")
    if not fn:
        raise SystemExit("--decider MODULE:FACTORY (FACTORY() returns a decide_fn)")
    return getattr(importlib.import_module(mod), fn)()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample", help="print the fixed 36-row sample (no model)")
    s.add_argument("--json", action="store_true")
    r = sub.add_parser("ref", help="read the sample with C1 on CPU -> speed/cpu_ref/")
    r.add_argument("--threads", type=int, default=None)
    r.add_argument("--resume", action="store_true")
    r.add_argument("--limit", type=int, default=None,
                   help="first N sample rows only (smoke run; the summary says full=false)")
    r.add_argument("--out", default=str(OUT))
    c = sub.add_parser("check", help="run check() on an HTTP host or an in-process decider")
    c.add_argument("--url")
    c.add_argument("--token")
    c.add_argument("--decider", help="MODULE:FACTORY; FACTORY() returns decide_fn")
    c.add_argument("--rows", default="sample", help='"sample" (ref36.jsonl ids) or a jsonl with "id" lines')
    c.add_argument("--ref", action="append", help='"stored", "stored_served", "stored_identity" or a jsonl path')
    c.add_argument("--limit", type=int, default=None)
    c.add_argument("--out", default=None, help="directory for check_summary.json + check_rows.jsonl")
    a = ap.parse_args(argv)
    if a.cmd == "sample":
        rows = fixed_sample()
        if a.json:
            print(json.dumps([{k: r.get(k) for k in ("id", "_split", "_stratum", "qtype", "_tokens")}
                              | {"n_options": _nopt(r), "card": bool(r.get("card"))} for r in rows], indent=1))
        else:
            for r in rows:
                print(f"{r['_stratum']:20s} {r['_split']:13s} {r['id']} {r['qtype']:6s} opts {_nopt(r):3d} "
                      f"card {int(bool(r.get('card')))} tokens {r['_tokens']}")
        print(f"{len(rows)} rows, sha256(ids) {sample_sha(rows)}")
    elif a.cmd == "ref":
        run_reference(Path(a.out), threads=a.threads, resume=a.resume, limit=a.limit)
    else:
        if bool(a.url) == bool(a.decider):
            raise SystemExit("check: give --url/--token or --decider")
        fn = http_decider(a.url, a.token) if a.url else _decider_from(a.decider)
        refs = a.ref or (["stored", str(REF36)] if REF36.exists() else ["stored"])
        res = check(fn, _load_rows_arg(a.rows, a.limit), ref=refs)
        if hasattr(fn, "close"):
            fn.close()
        per = res.pop("per_row")
        if a.out:
            od = Path(a.out)
            od.mkdir(parents=True, exist_ok=True)
            (od / "check_summary.json").write_text(json.dumps(res, indent=1))
            (od / "check_rows.jsonl").write_text("".join(json.dumps(x) + "\n" for x in per))
        print(json.dumps({k: res[k] for k in ("rows", "answered", "errors", "schema_problems", "call_ms",
                                               "tokens_first_view", "clean_run")}, indent=1))
        for name, v in res["vs"].items():
            print(f"vs {name}: argmax {v['argmax_agree']} ({v.get('n_disagree')} flips), |dp| max "
                  f"{v.get('dp', {}).get('max')}, acc diff {v.get('acc_diff_pt')} pt")


if __name__ == "__main__":
    main()
