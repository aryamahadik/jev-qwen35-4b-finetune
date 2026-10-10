"""Shared code for the OHS-3 harness (prep89/). NEW file; it edits nothing.

Rules this module enforces for every prep89 script:
  * Blind: nothing here prints item text (state, instructions, options, cards). Scripts print counts, ids of files,
    timings and aggregate numbers only.
  * Exactness: the Jev request is built by run_jev.py's OWN `card_defs` / `question` functions and its GUARD string,
    taken from run_jev.py's source by AST (so it cannot drift from the OHS-1/OHS-2 collector), and T-scaling is
    calibrate.py's own `scaled`, taken the same way (importing calibrate.py would run its CLI loop on our argv).
  * The A5 readout (`a5_read`) is decoder_io.predict's batching and 2-view code with the identity view kept as a
    by-product; tests/test in prep89 checks it equals decoder_io.predict exactly (fake logits, CPU).
  * Real OHS-3 is recognised by the frozen sha256 values of PREREG_OHS3.md; fake backends refuse it.
  * Token counts (a5_read(usage=...), A5Decider "usage"): read from the tokenizer encodes cand_logits already makes
    (a transparent wrapper, probabilities bit-identical); counts only, never text. Output tokens are 0 (the readout
    generates nothing).
  * The 2B (PRISM-X I) is always read eagerly (decoder_io skips GRAPHS for it, GraphRunner refuses it);
    check_prism_x makes sure its control plane is active with the config's parts. The cascade is one rule
    (cascade_answer), used offline (ohs3_cascade.py) and served (CascadeDecider), parameters from the config only.
"""
from __future__ import annotations

import ast
import hashlib
import json
import math
import os
import random
import re
import subprocess
import time
from pathlib import Path

PREP = Path(__file__).resolve().parent
LEAN = PREP.parent
REPO = LEAN.parent.parent
PY = LEAN.parent / ".venv" / "bin" / "python"
SPLIT = "ohs3"
FROZEN_OHS3 = {  # PREREG_OHS3.md, "Frozen files"
    "ohs3.jsonl": "68cb27da139010a9d9b00bfedc32e3ba8f1b963bf68c6cca85fd5e491868fd66",
    "ohs3_relations.jsonl": "c2e1dcee9ba40faea316140d423d5acf85644a6aa9af953ac5b0d95b3f5a04dc",
    "ohs3_calls.jsonl": "ed6fb8af24c3ca51a044953d487959315c879c418c0a64bb12c61875f72c80b0",
    "ohs3_summary.json": "81f5ceab7950b12eacf663109efdbad45acdc3b5c9fa5c89eae88d04efad2036",
}
PINNED_JEV = "typesafe/jev-1.13-20260917"
JEV_REQUEST_MODEL_OPENROUTER = "jev-1.13"  # run_jev.py's DEFAULT_MODEL on the OpenRouter route (OHS-1/OHS-2)
JEV_USD_PER_M_INPUT = 0.042  # list price (speed_cost_definition.md); output is free
OHS2_JEV_CALLS_PER_RUN = 1320  # preds_ohs2/jev_guard_raw.jsonl: 1,320 calls, 0 errors, all typesafe/jev-1.13-20260917
OHS3_CALLS = 2456
PLACEHOLDER = re.compile(r"^<OWNER")
D1_VALUES = ("served_h100", "L4_batch")  # decisions.od_scored_run (ohs3_runbook.md D1)
D2_VALUES = ("extra_pass", "run1_via_harness")  # decisions.jev_timing (ohs3_runbook.md D2)
OPTION_MAX = 255  # decoder_io.MAX_OPTIONS (two-letter single-token labels after Z)
QUESTION_MAX = 16


# ------------------------------------------------------------------ files, hashes, blind helpers

def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_jsonl(p):
    with open(p) as f:
        return [json.loads(l) for l in f if l.strip()]


def write_jsonl_atomic(p, recs):
    p = Path(p)
    tmp = p.with_name(p.name + ".tmp")
    with open(tmp, "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    os.replace(tmp, p)


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def frozen_status(root) -> dict:
    """{file: True/False/None(missing)} against PREREG_OHS3's frozen sha256 values."""
    out = {}
    for fn, want in FROZEN_OHS3.items():
        p = Path(root) / "data" / fn
        out[fn] = None if not p.exists() else sha256_file(p) == want
    return out


def is_real_ohs3(root) -> bool:
    p = Path(root) / "data" / "ohs3.jsonl"
    return p.exists() and sha256_file(p) == FROZEN_OHS3["ohs3.jsonl"]


def require_frozen(root):
    st = frozen_status(root)
    bad = {k: v for k, v in st.items() if v is not True}
    if bad:
        raise SystemExit(f"STOP: OHS-3 files differ from the frozen sha256 of PREREG_OHS3.md: {bad}")
    return st


def require_synthetic(root):
    """Fake backends (fake Jev, oracle model) read gold labels: only ever on the synthetic stand-in."""
    p = Path(root) / "data" / "ohs3.jsonl"
    if is_real_ohs3(root):
        raise SystemExit("REFUSED: this is the real OHS-3 file; fake/oracle backends run on the synthetic stand-in only")
    with open(p) as f:
        first = json.loads(f.readline())
    if not (first.get("meta") or {}).get("synthetic"):
        raise SystemExit(f"REFUSED: {p} is not marked meta.synthetic=true")


def blind_print(*a, **k):
    """print() for prep89 scripts: everything printed must be counts/aggregates. A guard against accidents: strings
    longer than 400 characters are refused (no single status line of ours is that long)."""
    s = " ".join(str(x) for x in a)
    if len(s) > 400:
        raise RuntimeError("blind_print: refusing a >400-character line (possible item text)")
    print(s, **{"flush": True, **k})


# ------------------------------------------------------------------ exact pieces of frozen scripts (AST, no import)

def _ast_functions(path, names, extra_globals=None):
    src = Path(path).read_text()
    tree = ast.parse(src)
    keep = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    found = {n.name for n in keep}
    if found != set(names):
        raise SystemExit(f"{path}: functions {sorted(set(names) - found)} not found")
    mod = ast.Module(body=keep, type_ignores=[])
    ns = dict(extra_globals or {})
    exec(compile(mod, str(path), "exec"), ns)  # noqa: S102 - our own frozen source file
    return ns, sha256_bytes(src.encode())


def run_jev_guard_text(path=None) -> str:
    """The GUARD string of run_jev.py (the body of `GUARD = (<text> if TAG.endswith("guard") else "")`)."""
    tree = ast.parse(Path(path or LEAN / "run_jev.py").read_text())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "GUARD" for t in n.targets):
            if isinstance(n.value, ast.IfExp) and isinstance(n.value.body, ast.Constant):
                return n.value.body.value
    raise SystemExit("run_jev.py: GUARD assignment not found in the expected form")


def run_jev_question_fn(tag: str, path=None):
    """(question(row) -> typesafe Question, run_jev.py sha256): run_jev.py's own functions with its GUARD rule
    (the guard is on iff the tag ends with "guard", exactly as run_jev.py decides it)."""
    from typesafe_sdk import Choice, Noul
    path = path or LEAN / "run_jev.py"
    guard = run_jev_guard_text(path) if tag.endswith("guard") else ""
    ns, sha = _ast_functions(path, ["card_defs", "question"], {"GUARD": guard, "Noul": Noul, "Choice": Choice})
    return ns["question"], sha


def run_jev_qmap(call):
    """run_jev.py's seeded question order: {"q0": row id, ...}."""
    rid = list(call["row_ids"])
    random.Random(call["call_id"]).shuffle(rid)
    return {f"q{i}": r for i, r in enumerate(rid)}


def jev_raw_to_preds(raw_path, rows, tag):
    """run_jev.py's raw -> preds conversion (its top-level tail), reproduced line by line: the LAST successful record
    per call (dict insertion order of the first success), choice probabilities renormalised over the options, with
    the raw sum kept as "_raw_sum". The dry run checks this is byte-identical to run_jev.py's own output."""
    out, ok = [], {}
    for l in open(raw_path):
        rec = json.loads(l)
        if rec["answers"]:
            ok[rec["call_id"]] = rec
    for rec in ok.values():
        for q, rid in rec["row_map"].items():
            ans = rec["answers"].get(q)
            r = rows[rid]
            if ans is None:
                continue
            if r["qtype"] == "noul":
                p = float(ans["noul"])
                probs = {"yes": p, "no": 1 - p}
            else:
                pr = {k: float(v) for k, v in ans["probabilities"].items()}
                s = sum(pr.values()) or 1.0
                probs = {o: pr.get(o, 0.0) / s for o in r["options"]}
                probs["_raw_sum"] = s
            out.append({"id": rid, "model": tag, "probs": probs, "latency_ms": rec["latency_ms"], "jev_model": rec["model"]})
    return out


_SCALED = None


def scaled(probs, T):
    """calibrate.py's `scaled` (softmax(log p / T) over the non-underscore keys), taken from its source by AST."""
    global _SCALED
    if _SCALED is None:
        ns, _ = _ast_functions(LEAN / "calibrate.py", ["scaled"], {"math": math})
        _SCALED = ns["scaled"]
    return _SCALED(probs, T)


def apply_T(probs, row, T: dict):
    """Per question type temperature (A5 item 4): T = {"noul": t, "choice": t}, applied with calibrate.scaled for
    every T (also T = 1, which only renormalises), exactly as calibrate.py wrote the OHS-1/OHS-2 *_cal files."""
    return scaled(probs, float(T["noul" if row["qtype"] == "noul" else "choice"]))


# ------------------------------------------------------------------ the A5 readout (decoder_io.predict, + 1-view)

READOUTS = ("2view", "single", "2view_ge10")


def two_view(row, readout):
    if row["qtype"] != "choice":
        return False  # A5 item 2: yes/no rows are a single read everywhere
    return readout == "2view" or (readout == "2view_ge10" and len(row["options"]) >= 10)


def predict_batches(rows, batch_size=16, token_budget=12000):
    """decoder_io.predict's order and token-budget batching, verbatim."""
    order = sorted(range(len(rows)), key=lambda i: len(rows[i]["state"]) + 20 * len(rows[i]["options"] or []))
    est = lambda i: (len(rows[i]["state"]) + len(rows[i].get("card") or "") + 400) / 3.2  # noqa: E731
    batches, cur = [], []
    for i in order:
        if cur and (len(cur) >= batch_size or (len(cur) + 1) * est(i) > token_budget):
            batches.append(cur)
            cur = []
        cur.append(i)
    if cur:
        batches.append(cur)
    return batches


class _TokTap:
    """A transparent tokenizer wrapper: every call and attribute goes to the real tokenizer and the SAME result object is
    returned, so the read is bit-identical. Each call is logged as (per-row unpadded token counts, padded tokens):
    decoder_io's eager encode (padded tensors + attention mask) or GraphRunner's encode (lists of ids)."""

    def __init__(self, tok):
        self._tok, self.log = tok, []

    def __call__(self, *a, **k):
        out = self._tok(*a, **k)
        ids = out["input_ids"]
        if hasattr(ids, "shape"):
            self.log.append(([int(x) for x in out["attention_mask"].sum(1).tolist()], int(ids.numel())))
        else:
            self.log.append(([len(x) for x in ids], None))
        return out

    def __getattr__(self, k):
        return getattr(self._tok, k)

    def __len__(self):
        return len(self._tok)


class _RoTap:
    """decoder_io.Readout with only .tok replaced by a _TokTap (prompt / cand / groups are the real Readout's)."""

    def __init__(self, ro, tok):
        self._ro, self.tok = ro, tok

    def __getattr__(self, k):
        return getattr(self._ro, k)


def _cand_counted(dio, model, ro, rows, dev, perms, usage, idx, first):
    """decoder_io.cand_logits with the token counts of the forward pass(es) it ran added to usage (per row of idx).
    Eager path (no graphs, PRISM-X, refused or uncaptured shapes): every eager encode is a forward pass (a PRISM-X
    counterfactual null pass included); graph path (no eager encode happened): the last graph encode is the replayed one
    (earlier graph encodes were shape attempts that ran nothing). Counting reads lengths that cand_logits computed anyway.
    A backend without a tokenizer (the synthetic oracle) is read as is and counted as "uncounted"."""
    if getattr(ro, "tok", None) is None:
        lg = dio.cand_logits(model, ro, rows, dev, perms=perms)
        for i in idx:
            usage["rows"][i]["reads"] += 1
        usage["paths"]["uncounted"] = usage["paths"].get("uncounted", 0) + 1
        usage["forward_calls"] += 1
        return lg
    eager = _TokTap(ro.tok)
    G = getattr(dio, "GRAPHS", None)
    gtap = keep = None
    if G is not None and getattr(G, "model", None) is model and hasattr(G, "tok"):
        gtap, keep = _TokTap(G.tok), G.tok
        G.tok = gtap  # under the caller's GPU lock: graphs are single-threaded
    try:
        lg = dio.cand_logits(model, _RoTap(ro, eager), rows, dev, perms=perms)
    finally:
        if gtap is not None:
            G.tok = keep
    if eager.log:
        lens = [sum(e[0][j] for e in eager.log) for j in range(len(rows))]
        padded, path = sum(e[1] for e in eager.log), "eager"
    elif gtap is not None and gtap.log:
        lens = gtap.log[-1][0]
        shape = getattr(G, "last_shape", None)
        padded, path = (int(shape[0]) * int(shape[1]) if shape else None), "graph"
    else:
        raise RuntimeError("token count: cand_logits ran no encode that the tap saw")
    for j, i in enumerate(idx):
        u = usage["rows"][i]
        u["total"] += lens[j]
        u["reads"] += 1
        if first:
            u["first_view"] += lens[j]
    usage["padded_tokens"] += padded or 0
    usage["forward_calls"] += 1
    usage["paths"][path] = usage["paths"].get(path, 0) + 1
    return lg


def new_usage(n):
    return {"rows": [{"first_view": 0, "total": 0, "reads": 0} for _ in range(n)], "padded_tokens": 0,
            "forward_calls": 0, "paths": {}}


def a5_read(dio, model, ro, rows, dev, readout, batch_size=16, token_budget=12000, usage=None):
    """-> (p_identity, p_readout): per row, the identity-view probabilities and the A5 readout (2-view = identity and
    reversed option order averaged in probability space, as decoder_io.predict(tta_choice=True)). No temperature here.
    With readout "2view" this equals decoder_io.predict(..., tta_choice=True); with "single" decoder_io.predict(...).
    usage: a dict from new_usage(len(rows)) to also count, per row, the input tokens of the identity read
    ("first_view"), of every read ("total": + the reversed read on 2-view rows) and the reads; the probabilities are
    bit-identical with or without it (tested)."""
    import torch
    if readout not in READOUTS:
        raise ValueError(f"readout {readout!r} not in {READOUTS}")

    def cand(batch, idx, perms=None, first=True):
        if usage is None:
            return dio.cand_logits(model, ro, batch, dev, perms=perms) if perms else dio.cand_logits(model, ro, batch, dev)
        return _cand_counted(dio, model, ro, batch, dev, perms, usage, idx, first)

    p1, pr = [None] * len(rows), [None] * len(rows)
    with torch.no_grad():
        for idx in predict_batches(rows, batch_size, token_budget):
            batch = [rows[i] for i in idx]
            lg = cand(batch, idx)
            for j, i in enumerate(idx):
                p1[i] = dio.to_probs(rows[i], lg[j])
                pr[i] = p1[i]
            ch = [(j, i) for j, i in enumerate(idx) if two_view(rows[i], readout)]
            if ch:
                rev = [list(range(len(rows[i]["options"])))[::-1] for _, i in ch]
                lg2 = cand([rows[i] for _, i in ch], [i for _, i in ch], perms=rev, first=False)
                for (j, i), p, l2 in zip(ch, rev, lg2):
                    p2 = dio.to_probs(rows[i], l2, p)
                    pr[i] = {o: (p1[i][o] + p2[o]) / 2 for o in rows[i]["options"]}
    return p1, pr


def usage_totals(usage, idx=None):
    """Request-level token counts from a5_read's usage (idx: the rows of one request, default all). Our readout reads
    the next-token distribution at the answer slot and generates nothing: output_tokens = 0 (JevBench's convention for
    this model, bench/v154/lean_snapshot/jevbench_od.py)."""
    rs = usage["rows"] if idx is None else [usage["rows"][i] for i in idx]
    return {"input_tokens": sum(r["total"] for r in rs), "output_tokens": 0,
            "input_tokens_first_view": sum(r["first_view"] for r in rs), "forward_passes": sum(r["reads"] for r in rs)}


# ------------------------------------------------------------------ served requests (our endpoint)

def od_request(call, rows, return_views=True):
    """Our endpoint's request for one call: the row fields decoder_io reads (state, instructions, qtype, options,
    card), in run_jev.py's seeded question order, so the served prompt is the batch prompt."""
    qmap = run_jev_qmap(call)
    qs = {}
    for k, rid in qmap.items():
        r = rows[rid]
        q = {"type": r["qtype"], "instructions": r["instructions"]}
        if r["qtype"] == "choice":
            q["options"] = list(r["options"])
        if r.get("card"):
            q["card"] = r["card"]
        qs[k] = q
    return {"state": call["state"], "questions": qs, "return_views": bool(return_views)}, qmap


def parse_rows(req):
    """Request -> [(name, decoder_io row)]. Accepts cards on both types and up to 255 options (decoder_io's limit;
    hosting/modal_direct_host.parse_request stops at 26 and has no yes/no cards, so it cannot serve OHS-3)."""
    if not isinstance(req, dict) or not isinstance(req.get("state"), str):
        raise ValueError('"state" must be a string')
    qs = req.get("questions")
    if not isinstance(qs, dict) or not qs:
        raise ValueError('"questions" must be a non-empty object')
    if len(qs) > QUESTION_MAX:
        raise ValueError(f"at most {QUESTION_MAX} questions per request")
    out = []
    for k, q in qs.items():
        if not isinstance(q, dict) or q.get("type") not in ("noul", "choice"):
            raise ValueError(f'{k}: "type" must be "noul" or "choice"')
        ins = q.get("instructions")
        if not isinstance(ins, str) or not ins.strip():
            raise ValueError(f'{k}: "instructions" must be a non-empty string')
        row = {"state": req["state"], "instructions": ins, "qtype": q["type"], "options": None}
        if q["type"] == "choice":
            opts = q.get("options")
            if not isinstance(opts, list) or not all(isinstance(o, str) and o.strip() for o in opts):
                raise ValueError(f'{k}: a choice needs "options" (a list of non-empty strings)')
            if not 2 <= len(opts) <= OPTION_MAX:
                raise ValueError(f"{k}: 2 to {OPTION_MAX} options")
            if len(set(opts)) != len(opts):
                raise ValueError(f"{k}: duplicate options")
            row["options"] = list(opts)
        card = q.get("card")
        if card is not None:
            if not isinstance(card, str):
                raise ValueError(f'{k}: "card" must be a string')
            if card:
                row["card"] = card
        out.append((k, row))
    return out


class A5Decider:
    """The serving readout: a5_read on the request's rows, then T (A5 item 4). Thread-safe (one GPU lock).
    With "return_views": true, each answer also carries the pre-T readout ("raw"), the identity view ("1v") and the
    identity view under the single-read T ("1v_cal"), so one served run yields every pre-registered configuration."""

    def __init__(self, dio, model, ro, dev, readout, T, T_single, sync=None, lock=None):
        import threading
        self.dio, self.model, self.ro, self.dev = dio, model, ro, dev
        self.readout, self.T, self.T1 = readout, dict(T), dict(T_single)
        self.sync = sync or (lambda: None)
        self.lock = lock or threading.Lock()
        self.log = []
        if readout not in READOUTS:
            raise ValueError(readout)

    def read(self, rows):
        """(p_identity, p_readout, usage, path, shape) for decoder_io rows; the caller holds self.lock."""
        usage = new_usage(len(rows))
        p1, pr = a5_read(self.dio, self.model, self.ro, rows, self.dev, self.readout, batch_size=16, usage=usage)
        self.sync()
        G = getattr(self.dio, "GRAPHS", None)
        on_graph = G is not None and getattr(G, "model", None) is self.model
        path = (getattr(G, "last_path", None) or "eager") if on_graph else "eager"
        shape = list(G.last_shape) if on_graph and getattr(G, "last_shape", None) else None
        return p1, pr, usage, path, shape

    def answer(self, r, a, b, views, u=None):
        fin = apply_T(b, r, self.T)
        if r["qtype"] == "noul":
            ans = {"type": "noul", "noul": fin["yes"]}
        else:
            best = max(fin, key=fin.get)
            ans = {"type": "choice", "choice": best, "confidence": fin[best], "probabilities": fin}
        if views:
            ans["views"] = {"raw": b, "1v": a, "1v_cal": apply_T(a, r, self.T1)}
        if u is not None:
            ans["usage"] = {"input_tokens": u["total"], "input_tokens_first_view": u["first_view"], "reads": u["reads"]}
        return ans

    def decide(self, req) -> dict:
        t0 = time.perf_counter()
        named = parse_rows(req)
        rows = [r for _, r in named]
        with self.lock:
            t1 = time.perf_counter()
            p1, pr, usage, path, shape = self.read(rows)
            t2 = time.perf_counter()
        views = bool(req.get("return_views"))
        answers = {k: self.answer(r, a, b, views, u) for (k, r), a, b, u in zip(named, p1, pr, usage["rows"])}
        t3 = time.perf_counter()
        timing = {"parse_ms": round((t1 - t0) * 1000, 3), "model_ms": round((t2 - t1) * 1000, 3),
                  "readout_ms": round((t3 - t2) * 1000, 3),
                  "reads": sum(1 + two_view(r, self.readout) for r in rows)}
        self.log.append({"rows": len(rows), "model_ms": timing["model_ms"], "path": path})
        return {"answers": answers, "timing": timing, "path": path, "shape": shape, "readout": self.readout,
                "usage": {**usage_totals(usage), "padded_tokens": usage["padded_tokens"], "paths": usage["paths"]}}

    def stats(self) -> dict:
        ms = sorted(x["model_ms"] for x in self.log)
        return {"requests": len(self.log), "model_ms_p50": pct(ms, 0.5), "model_ms_p95": pct(ms, 0.95)}


# ------------------------------------------------------------------ PRISM-X (the 2B, PRISM-X I): eager, checked

PX_STRUCT = ("authority", "shadow_heads", "shadow_pick", "option_head", "loop_steps", "loop_exit_margin", "temp_head",
             "loop_ensemble", "counterfactual", "policy_compiler", "compiler_dim", "compiler_bound", "action_tower",
             "head_dim", "head_heads")  # prism_x.DEFAULTS minus the learning rates


def check_prism_x(m, dio, model) -> dict:
    """The loaded (merged) model's PRISM-X control plane must be what the config names (models.<k>.prism_x):
    absent for null; otherwise installed, ACTIVE on this model's body (prism_x.active_for: else cand_logits would
    silently run the backbone alone) and with the same parts as prism_x.resolve(<config value>). A PRISM-X model is
    always read eagerly: decoder_io.cand_logits skips GRAPHS for it and decoder_io.GraphRunner refuses it."""
    pxm = dio._prism_x()
    want = m.get("prism_x")
    active = pxm is not None and pxm.active_for(dio._parts(model)[0])
    if not want:
        if active:
            raise SystemExit(f"{m['name']}: a PRISM-X control plane is active but the config names none")
        return {"prism_x": None, "active": False}
    if not active:
        raise SystemExit(f"{m['name']}: the config names PRISM-X {want!r} but no control plane is active on the "
                         "loaded model (prism_x.json missing next to the adapter, or uninstalled by a later load)")
    exp, got = pxm.resolve(want), pxm.PX.cfg
    diff = {k: [exp.get(k), got.get(k)] for k in PX_STRUCT if exp.get(k) != got.get(k)}
    if diff:
        raise SystemExit(f"{m['name']}: PRISM-X parts differ from the config: {diff}")
    return {"prism_x": want if isinstance(want, str) else "cfg", "active": True,
            "params": int(sum(p.numel() for p in pxm.PX.parameters()))}


# ------------------------------------------------------------------ the 2B -> 4B cascade (one rule, offline and served)

ROUTE_ON = ("primary", "raw")


def cascade_norm(r, pr):
    """cascade_sim.py's / ohs3_cascade.py's norm: the row's answers in order, probabilities renormalised over them."""
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    p = [float(pr.get(k, 0.0)) for k in keys]
    s = sum(p) or 1.0
    return keys, [x / s for x in p]


def cascade_routed(r, p_route, tau) -> bool:
    """FINETUNE_PLAN 5.3: a row goes to the big model when the small model's top probability is below tau."""
    return max(cascade_norm(r, p_route)[1]) < float(tau)


def cascade_answer(r, p_small, p_big, routed, w_big) -> dict:
    """The cascade's probabilities for one row: the small model's PRIMARY probabilities, or on a routed row
    w_big * big PRIMARY + (1 - w_big) * small PRIMARY, both renormalised over the row's answers."""
    ks, ps = cascade_norm(r, p_small)
    if routed:
        _, pb = cascade_norm(r, p_big)
        ps = [float(w_big) * x + (1 - float(w_big)) * y for x, y in zip(pb, ps)]
    return dict(zip(ks, ps))


class CascadeDecider:
    """The 2B -> 4B cascade behind ONE endpoint (both models on one GPU, one lock), timed end to end with routing
    (speed_cost_definition.md). Per row: the small model's A5 read (its readout, its T); routed when the top of its
    routing probabilities (cascade.route_on: "primary" = after T, A5 item 5 "served probabilities"; "raw" = before T,
    FINETUNE_PLAN 5.3) is < tau; a routed row is also read by the big model (its readout, its T); the answer is
    cascade_answer(...), exactly ohs3_cascade.py's offline rule. tau / w_big / route_on come from the pre-registered
    config only (load_config refuses anything else). Both models must use the same decoder_io layout/style (module
    globals); the small one may be PRISM-X (eager), the big one may run on CUDA graphs."""

    def __init__(self, small: A5Decider, big: A5Decider, tau, w_big, route_on="primary", lock=None):
        import threading
        if route_on not in ROUTE_ON:
            raise ValueError(f"route_on {route_on!r} not in {ROUTE_ON}")
        rs, rb = getattr(small, "ro", None), getattr(big, "ro", None)
        if rs is not None and rb is not None and (rs.letters != rb.letters or rs.wide != rb.wide):
            # decoder_io.label() reads the module-global two-letter list the LAST Readout built: both models must have
            # the same answer-label tokens (Qwen3.5-2B and -4B share one tokenizer.json; checked here, not assumed)
            raise ValueError("cascade: the two models' answer-label tokens differ (different tokenizers)")
        self.small, self.big = small, big
        self.tau, self.w, self.route_on = float(tau), float(w_big), route_on
        self.lock = lock or threading.Lock()
        self.log = []

    def decide(self, req) -> dict:
        t0 = time.perf_counter()
        named = parse_rows(req)
        rows = [r for _, r in named]
        S, Bg = self.small, self.big
        with self.lock:
            t1 = time.perf_counter()
            s1, sr, su, spath, _ = S.read(rows)
            t2 = time.perf_counter()
            s_fin = [apply_T(b, r, S.T) for r, b in zip(rows, sr)]
            route_p = s_fin if self.route_on == "primary" else sr
            routed = [cascade_routed(r, p, self.tau) for r, p in zip(rows, route_p)]
            ri = [i for i, x in enumerate(routed) if x]
            b1 = br = bu = None
            bpath = None
            if ri:
                b1, br, bu, bpath, _ = Bg.read([rows[i] for i in ri])
            t3 = time.perf_counter()
        big_of = {i: j for j, i in enumerate(ri)}
        views = bool(req.get("return_views"))
        answers = {}
        for i, ((k, r), a, b, sf) in enumerate(zip(named, s1, sr, s_fin)):
            j = big_of.get(i)
            bf = apply_T(br[j], r, Bg.T) if j is not None else None
            fin = cascade_answer(r, sf, bf, j is not None, self.w)
            if r["qtype"] == "noul":
                ans = {"type": "noul", "noul": fin["yes"]}
            else:
                best = max(fin, key=fin.get)
                ans = {"type": "choice", "choice": best, "confidence": fin[best], "probabilities": fin}
            u_s = su["rows"][i]
            u_b = bu["rows"][j] if j is not None else {"total": 0, "first_view": 0, "reads": 0}
            ans["usage"] = {"input_tokens": u_s["total"] + u_b["total"], "input_tokens_first_view": u_s["first_view"],
                            "reads": u_s["reads"] + u_b["reads"], "small_input_tokens": u_s["total"],
                            "big_input_tokens": u_b["total"]}
            ans["routed"] = j is not None
            if views:
                ans["views"] = {"small_raw": b, "small_1v": a, "small_1v_cal": apply_T(a, r, S.T1),
                                "big_raw": br[j] if j is not None else None, "big_1v": b1[j] if j is not None else None,
                                "routed": j is not None, "route_top": max(cascade_norm(r, route_p[i])[1])}
            answers[k] = ans
        t4 = time.perf_counter()
        us = usage_totals(su)
        ub = usage_totals(bu) if bu is not None else {"input_tokens": 0, "forward_passes": 0}
        ut = {"input_tokens": us["input_tokens"] + ub["input_tokens"], "output_tokens": 0,
              "input_tokens_first_view": us["input_tokens_first_view"],
              "forward_passes": us["forward_passes"] + ub["forward_passes"]}
        timing = {"parse_ms": round((t1 - t0) * 1000, 3), "model_ms": round((t3 - t1) * 1000, 3),
                  "small_ms": round((t2 - t1) * 1000, 3), "big_ms": round((t3 - t2) * 1000, 3),
                  "readout_ms": round((t4 - t3) * 1000, 3),
                  "reads": sum(1 + two_view(r, S.readout) for r in rows)
                  + sum(1 + two_view(rows[i], Bg.readout) for i in ri)}
        path = f"small:{spath}" + (f"+big:{bpath}" if ri else "")
        self.log.append({"rows": len(rows), "routed": len(ri), "model_ms": timing["model_ms"], "path": path})
        return {"answers": answers, "timing": timing, "path": path, "shape": None,
                "readout": f"cascade(small {S.readout}, big {Bg.readout}, tau {self.tau}, w_big {self.w}, "
                           f"route_on {self.route_on})",
                "usage": {**ut, "small_input_tokens": us["input_tokens"], "big_input_tokens": ub["input_tokens"],
                          "routed_rows": len(ri), "rows": len(rows)}}

    def stats(self) -> dict:
        ms = sorted(x["model_ms"] for x in self.log)
        n = sum(x["rows"] for x in self.log)
        return {"requests": len(self.log), "model_ms_p50": pct(ms, 0.5), "model_ms_p95": pct(ms, 0.95),
                "routed_share": round(sum(x["routed"] for x in self.log) / n, 4) if n else None}


# ------------------------------------------------------------------ Modal region price multiplier (C1 / C2 rate)

REGION_MULT = {"any": 1.0, "broad": 1.15, "narrow": 1.75}  # hosting/modal_direct_host.REGION_MULT (test: equal)


def region_multiplier(region: str) -> float:
    """hosting/modal_direct_host._region_opt's price multiplier for a region string ("any" 1.0; "us"/"eu"/"ap" broad
    1.15; anything narrower 1.75). The served endpoint's all-in rate is od_usd_per_hour x this."""
    r = [x.strip() for x in str(region).split(",") if x.strip()]
    if not r or r == ["any"]:
        return REGION_MULT["any"]
    return REGION_MULT["narrow" if any(x not in ("us", "eu", "ap") for x in r) else "broad"]


# ------------------------------------------------------------------ config (pre-registered settings)

def placeholders(obj, path=""):
    """Every "<OWNER ...>" string left in the config, with its JSON path."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not k.startswith("_"):
                out += placeholders(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += placeholders(v, f"{path}[{i}]")
    elif isinstance(obj, str) and PLACEHOLDER.match(obj):
        out.append(path)
    return out


def load_config(path, require_complete=True, model_keys=None):
    """The OHS-3 settings file. require_complete: no "<OWNER" placeholder may remain in the global sections or in the
    model sections that run (model_keys, default every model with run_on_ohs3 true)."""
    path = Path(path)
    raw = path.read_bytes()
    cfg = json.loads(raw)
    cfg["_sha256"] = sha256_bytes(raw)
    cfg["_path"] = str(path)
    if require_complete:
        run = list(model_keys or [k for k, m in cfg["models"].items() if m.get("run_on_ohs3") is True])
        casc = cfg.get("cascade") or {}
        if "cascade" in run and casc.get("run") is not True:
            raise SystemExit("cascade.run is not true: the cascade is not pre-registered to run")
        if casc.get("run") is True:  # a pre-registered cascade needs both of its models complete as well
            run = [k for k in run if k != "cascade"]
            for k in (casc.get("small"), casc.get("big")):
                if k not in cfg["models"]:
                    raise SystemExit(f"cascade: model key {k!r} not in models")
                if k not in run:
                    run.append(k)
        skip = {"models"} | ({"cascade"} if casc.get("run") is not True else set())
        bad = placeholders({k: v for k, v in cfg.items() if k not in skip})
        for k in run:
            bad += placeholders(cfg["models"][k], f"models.{k}")
        if bad:
            raise SystemExit(f"STOP: the config still has owner placeholders: {bad}")
        dec = cfg.get("decisions") or {}
        if dec.get("od_scored_run") not in D1_VALUES or dec.get("jev_timing") not in D2_VALUES:
            raise SystemExit(f"decisions: od_scored_run must be one of {D1_VALUES}, jev_timing one of {D2_VALUES}")
        for k in run:
            m = cfg["models"][k]
            if m["readout_choice"] not in READOUTS:
                raise SystemExit(f"models.{k}.readout_choice must be one of {READOUTS}")
            for tk in ("T_primary", "T_single"):
                for qt in ("noul", "choice"):
                    t = m[tk][qt]
                    if not isinstance(t, (int, float)) or not 0.5 <= float(t) <= 2.0:
                        raise SystemExit(f"models.{k}.{tk}.{qt} = {t!r}: A5 item 4 grid is 0.5-2.0")
            px, cg = m.get("prism_x"), m.get("cuda_graphs")
            if px is not None and not isinstance(px, (str, dict)):
                raise SystemExit(f"models.{k}.prism_x must be null, a PRISM-X preset name or a cfg dict")
            if cg is not None and not isinstance(cg, bool):
                raise SystemExit(f"models.{k}.cuda_graphs must be true or false")
            if px and cg:
                raise SystemExit(f"models.{k}: a PRISM-X model runs eagerly (decoder_io.GraphRunner refuses it): "
                                 "cuda_graphs must be false")
            if px and not re.fullmatch(r"[0-9a-f]{64}", str(m.get("prism_x_sha256", ""))):
                raise SystemExit(f"models.{k}.prism_x_sha256 must be the 64-hex sha256 of prism_x.safetensors (the "
                                 "PRISM-X weights are part of the served model)")
        if casc.get("run") is True:
            check_cascade(cfg)
        cost = cfg.get("cost") or {}
        dph = cost.get("od_decisions_per_hour_sustained")
        if dph is not None and dph != "load_test" and not (isinstance(dph, (int, float)) and dph > 0):
            raise SystemExit("cost.od_decisions_per_hour_sustained must be 'load_test' or a positive number")
        util = cost.get("utilisation_for_claim")
        if util is not None and not (isinstance(util, (int, float)) and 0 < util <= 1):
            raise SystemExit("cost.utilisation_for_claim must be in (0, 1]")
        head = (cfg.get("speed") or {}).get("headline_system", "4b")
        if head != "cascade" and head not in cfg["models"]:
            raise SystemExit(f"speed.headline_system {head!r} is neither a model key nor 'cascade'")
    return cfg


def check_cascade(cfg):
    """The pre-registered cascade rule (FINETUNE_PLAN 5.3, A5 item 5): numbers from the config only, set on dev-select."""
    c = cfg["cascade"]
    tau, w = c.get("tau"), c.get("w_big")
    if not isinstance(tau, (int, float)) or not 0 < float(tau) <= 1:
        raise SystemExit(f"cascade.tau = {tau!r}: must be a number in (0, 1] (dev-select)")
    if not isinstance(w, (int, float)) or not 0 <= float(w) <= 1:
        raise SystemExit(f"cascade.w_big = {w!r}: must be a number in [0, 1]")
    if c.get("route_on", "primary") not in ROUTE_ON:
        raise SystemExit(f"cascade.route_on must be one of {ROUTE_ON}")
    if c.get("small") == c.get("big"):
        raise SystemExit("cascade: small and big are the same model")
    ms, mb = cfg["models"][c["small"]], cfg["models"][c["big"]]
    if (ms["layout"], ms["style"]) != (mb["layout"], mb["style"]):
        raise SystemExit("cascade: the two models need the same decoder_io layout/style (module globals in one process)")
    if not isinstance(c.get("name"), str) or not c["name"]:
        raise SystemExit("cascade.name missing")


def system(cfg, key) -> dict:
    """The OpenDecide system a key names: a model ({"kind": "model", **models[key]}) or the cascade
    ({"kind": "cascade", "name", "small", "big", "tau", "w_big", "route_on", "readout_choice"})."""
    if key == "cascade":
        c = cfg["cascade"]
        ms, mb = cfg["models"][c["small"]], cfg["models"][c["big"]]
        return {"key": "cascade", "kind": "cascade", "name": c["name"], "small": c["small"], "big": c["big"],
                "small_name": ms["name"], "big_name": mb["name"], "tau": c["tau"], "w_big": c["w_big"],
                "route_on": c.get("route_on", "primary"),
                "readout_choice": f"cascade({ms['readout_choice']}->{mb['readout_choice']})"}
    return {"key": key, "kind": "model", **cfg["models"][key]}


# ------------------------------------------------------------------ dev-fit evidence: T (A5 item 4) and the cascade rule

FIT_EPS = 1e-9


def _fit_json(rel):
    """(parsed JSON | None if missing | "bad", resolved path) of a fit log named in the config (relative to lean/)."""
    if not rel or PLACEHOLDER.match(str(rel)):
        return None, None
    p = Path(rel) if Path(rel).is_absolute() else LEAN / rel
    if not p.exists():
        return None, p
    try:
        return json.loads(p.read_text()), p
    except Exception:  # noqa: BLE001
        return "bad", p


def _reads_changed(reads, root):
    """{read: {split: sha256}} -> the (read, split) whose dev preds file is missing here or changed since the fit."""
    bad = []
    for n, by in reads.items():
        for sp, sha in by.items():
            if sp.startswith("ohs"):
                bad.append((n, sp, "an OHS split"))
                continue
            f = Path(root) / f"preds_{sp}" / f"{n}.jsonl"
            if not f.exists():
                bad.append((n, sp, "missing"))
            elif sha256_file(f) != sha:
                bad.append((n, sp, "changed"))
    return bad


def check_T_log(m, k, rehash=True, root=None) -> tuple[str, str, str]:
    """models.<k>.T_fit_log must be prep89/t_rule_check.py's --json for THIS model and readout, from dev reads only,
    and the config's T_primary / T_single must equal its ship values. (status, what, detail): PASS, FAIL (a
    contradiction) or TODO (not machine-checkable: a log in another format, or an old read without view flags)."""
    what = f"models.{k}.T_fit_log: t_rule_check.py --json of {m.get('name')} (dev only) = the config's T"
    d, p = _fit_json(m.get("T_fit_log"))
    if d is None:
        return "FAIL", what, f"missing: {m.get('T_fit_log')}"
    if d == "bad" or not isinstance(d, dict) or not {"ship", "args", "provenance"} <= set(d):
        return "TODO", what, f"{p.name}: not a t_rule_check.py --json log (run it with --model --choice-single --json)"
    pv, sh = d["provenance"], d["ship"]
    fail, todo = [], []
    if pv.get("model") != m["name"]:
        fail.append(f"log model {pv.get('model')!r} != {m['name']!r}")
    if pv.get("dev_only") is not True or any(str(s).startswith("ohs") for s in pv.get("splits", [])):
        fail.append("not dev-only")
    ads = {n: r.get("adapter") for n, r in pv.get("reads", {}).items() if r.get("adapter") not in (None, m["name"])}
    if ads:
        fail.append(f"reads of another adapter {ads}")
    cr = pv.get("choice_readout")
    if cr in ("unknown", "mixed"):
        todo.append(f"choice read's view not recorded in its meta ({cr})")
    elif cr != m["readout_choice"]:
        fail.append(f"choice readout of the log {cr!r} != readout_choice {m['readout_choice']!r}")
    nv = pv.get("noul_read_view")
    if nv in ("unknown", "mixed"):
        todo.append(f"yes/no read's view not recorded ({nv})")
    elif nv != "single":
        fail.append(f"yes/no read is {nv!r}, the served yes/no read is single")
    eq = lambda a, b: isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) <= FIT_EPS  # noqa
    for tk, qt, key in (("T_primary", "noul", "T_noul"), ("T_primary", "choice", "T_choice"),
                        ("T_single", "noul", "T_noul")):
        if not eq(m[tk][qt], sh.get(key)):
            fail.append(f"{tk}.{qt} {m[tk][qt]} != log {key} {sh.get(key)}")
    if "T_choice_single" not in sh:
        todo.append("T_single.choice not in the log (t_rule_check.py --choice-single)")
    else:
        if pv.get("choice_single_view") not in ("single",):
            (todo if pv.get("choice_single_view") in ("unknown", "mixed") else fail).append(
                f"--choice-single read view {pv.get('choice_single_view')!r}")
        if not eq(m["T_single"]["choice"], sh["T_choice_single"]):
            fail.append(f"T_single.choice {m['T_single']['choice']} != log T_choice_single {sh['T_choice_single']}")
    if rehash:
        ch = _reads_changed({n: r["sha256"] for n, r in pv.get("reads", {}).items()}, root or LEAN)
        if ch:
            fail.append(f"dev reads missing or changed since the fit: {ch[:4]}")
    st = "FAIL" if fail else ("TODO" if todo else "PASS")
    return st, what, "; ".join(fail + todo) or f"{p.name} sha256 {sha256_file(p)[:16]}"


def check_cascade_log(cfg, rehash=True, root=None) -> tuple[str, str, str]:
    """cascade.tau_fit_log must be prep89/cascade_rule_fit.py's --json for the configured small/big models with the
    config's T logs (sha256), dev reads only, a chosen budget, and config_values == cascade.tau / w_big / route_on;
    its FINETUNE_PLAN 5.3 use rule must pass (not measured -> TODO; failed -> FAIL)."""
    c = cfg["cascade"]
    what = "cascade.tau_fit_log: cascade_rule_fit.py --json (dev only) = the config's tau / w_big / route_on"
    d, p = _fit_json(c.get("tau_fit_log"))
    if d is None:
        return "FAIL", what, f"missing: {c.get('tau_fit_log')}"
    if d == "bad" or not isinstance(d, dict) or not {"config_values", "small", "big", "use_rule"} <= set(d):
        return "TODO", what, f"{p.name}: not a cascade_rule_fit.py --json log"
    fail, todo = [], []
    if d.get("dev_only") is not True or any(str(s).startswith("ohs") for s in d.get("splits", [])):
        fail.append("not dev-only")
    for side in ("small", "big"):
        m = cfg["models"][c[side]]
        if d[side].get("model") != m["name"]:
            fail.append(f"{side} model {d[side].get('model')!r} != {m['name']!r}")
        _, tp = _fit_json(m.get("T_fit_log"))
        if tp is None or not tp.exists() or sha256_file(tp) != d[side].get("t_log_sha256"):
            fail.append(f"{side}: the fit used another T log than models.{c[side]}.T_fit_log")
    cv = d.get("config_values")
    if not cv:
        fail.append("the fit chose no cascade (no budget passed the dev-select bound)")
    else:
        if not (isinstance(c.get("tau"), (int, float)) and abs(float(c["tau"]) - float(cv["tau"])) <= 1e-12):
            fail.append(f"tau {c.get('tau')} != fit {cv['tau']}")
        if not (isinstance(c.get("w_big"), (int, float)) and abs(float(c["w_big"]) - float(cv["w_big"])) <= 1e-12):
            fail.append(f"w_big {c.get('w_big')} != fit {cv['w_big']}")
        if c.get("route_on", "primary") != cv["route_on"]:
            fail.append(f"route_on {c.get('route_on')} != fit {cv['route_on']}")
    u = d.get("use_rule") or {}
    if u.get("pass") is False:
        fail.append(f"FINETUNE_PLAN 5.3 use rule fails ({u.get('sum', u.get('note'))} vs < {u.get('max', 0.85)})")
    elif u.get("pass") is None:
        todo.append("5.3 use rule not measured (needs the 2B and 4B dev load tests: cascade_rule_fit.py --load-tests)")
    if rehash:
        ch = _reads_changed(d.get("reads") or {}, root or LEAN)
        if ch:
            fail.append(f"dev reads missing or changed since the fit: {ch[:4]}")
    st = "FAIL" if fail else ("TODO" if todo else "PASS")
    return st, what, "; ".join(fail + todo) or f"{p.name} sha256 {sha256_file(p)[:16]}"


def fit_keys(cfg, keys):
    """The model keys whose T logs a run of `keys` (model keys and/or "cascade") depends on, and whether the cascade."""
    mk, casc = [], False
    for k in keys:
        if k == "cascade":
            casc = True
            mk += [cfg["cascade"]["small"], cfg["cascade"]["big"]]
        else:
            mk.append(k)
    return list(dict.fromkeys(mk)), casc


def check_fit_logs(cfg, keys, rehash=True, root=None) -> list:
    """[(status, what, detail)] of the dev-fit evidence of every system in keys (ohs3_preflight.py lists them)."""
    mk, casc = fit_keys(cfg, keys)
    out = [check_T_log(cfg["models"][k], k, rehash, root) for k in mk]
    if casc:
        out.append(check_cascade_log(cfg, rehash, root))
    return out


def require_fit_logs(cfg, keys, rehash=False, root=None):
    """REAL OHS-3 runs, before any call or model load: every dev-fit check of the systems this run uses must PASS.
    rehash=False on the L4 VM (the dev reads are on the Mac; the Mac preflight re-hashes them)."""
    res = check_fit_logs(cfg, keys, rehash, root)
    bad = [r for r in res if r[0] != "PASS"]
    if bad:
        raise SystemExit("STOP: the dev-fit evidence of the pre-registered values does not check out: "
                         + " | ".join(f"{s} {w}: {d}" for s, w, d in bad))
    return res


def check_prism_x_file(m, adapter_dir) -> str | None:
    """A PRISM-X model's control-plane weights (prism_x.safetensors next to the adapter) are part of the served model:
    their sha256 must equal models.<k>.prism_x_sha256. Returns the sha256 (None for a model without PRISM-X)."""
    if not m.get("prism_x"):
        return None
    f = Path(adapter_dir) / "prism_x.safetensors"
    if not f.exists():
        raise SystemExit(f"{m['name']}: config names PRISM-X but {f} is missing")
    sha = sha256_file(f)
    if sha != m.get("prism_x_sha256"):
        raise SystemExit(f"{m['name']}: prism_x.safetensors sha256 {sha[:16]} != pre-registered "
                         f"{str(m.get('prism_x_sha256'))[:16]}")
    return sha


def git(*args, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd or LEAN, capture_output=True)


def committed_equal(path, commit) -> bool:
    """True if `path` at `commit` is byte-identical to the working file and `commit` is an ancestor of HEAD."""
    rel = os.path.relpath(Path(path).resolve(), REPO)
    show = git("show", f"{commit}:{rel}", cwd=REPO)
    anc = git("merge-base", "--is-ancestor", commit, "HEAD", cwd=REPO)
    return show.returncode == 0 and anc.returncode == 0 and show.stdout == Path(path).read_bytes()


# ------------------------------------------------------------------ rule-4 ledger (one OHS-3 run per model)

def ledger_path(root):
    return Path(root) / "logs" / "ohs3_runs.jsonl"


def ledger(root) -> list:
    p = ledger_path(root)
    return read_jsonl(p) if p.exists() else []


def ledger_append(root, rec):
    p = ledger_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f:
        f.write(json.dumps({**rec, "utc": utc()}) + "\n")


def completed_runs(root, name) -> list:
    return [r for r in ledger(root) if r.get("name") == name and r.get("status") == "complete"]


# ------------------------------------------------------------------ percentiles and the speed bootstrap

def pct(xs, q):
    """Nearest rank s[int(q*n)] (bench_api.py / client_bench.py convention)."""
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))] if s else None


def speed_bootstrap(od_ms, jev_ms, tasks, n_boot=10000, seed=0, chunk=500):
    """speed_cost_definition.md S1/S2: paired bootstrap over calls, stratified by task; difference = Jev - OD (positive
    = OpenDecide faster) of the p50 and the p95 (nearest rank). numpy.random.default_rng(seed); per resample, tasks in
    sorted order, rng.integers(0, n_t, n_t) per task (drawn in chunks of resamples: chunk x n_t per task)."""
    import numpy as np
    od, jv = np.asarray(od_ms, float), np.asarray(jev_ms, float)
    by = {}
    for i, t in enumerate(tasks):
        by.setdefault(t, []).append(i)
    order = sorted(by)
    rng = np.random.default_rng(seed)
    n = len(od)
    k50, k95 = min(n - 1, int(0.5 * n)), min(n - 1, int(0.95 * n))
    d50, d95 = [], []
    for s in range(0, n_boot, chunk):
        b = min(chunk, n_boot - s)
        idx = np.concatenate([np.asarray(by[t])[rng.integers(0, len(by[t]), (b, len(by[t])))] for t in order], axis=1)
        so, sj = np.sort(od[idx], axis=1), np.sort(jv[idx], axis=1)
        d50.append(sj[:, k50] - so[:, k50])
        d95.append(sj[:, k95] - so[:, k95])
    d50, d95 = np.concatenate(d50), np.concatenate(d95)

    def summ(d, point):
        lo, hi = np.percentile(d, [2.5, 97.5])
        p = float(min(1.0, 2 * min((d <= 0).mean(), (d >= 0).mean())))
        return {"diff_jev_minus_od_ms": point, "ci95": [float(lo), float(hi)], "p": p}

    return {"p50": summ(d50, pct(jev_ms, 0.5) - pct(od_ms, 0.5)), "p95": summ(d95, pct(jev_ms, 0.95) - pct(od_ms, 0.95)),
            "n_calls": n, "n_boot": n_boot, "seed": seed, "strata": len(order),
            "percentile": "nearest rank s[int(q*n)]", "ci": "95% percentile interval (numpy linear)"}
