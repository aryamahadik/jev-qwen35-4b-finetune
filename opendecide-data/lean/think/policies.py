"""A17 think policies, built on think_engine.ThinkPath: the prompt and the answer parsing are IDENTICAL to the L4 path
(bench/think_check/think_run.py / think_rows.py): system decoder_io.SYSTEM, user decoder_io.user_msg(row) (layout
schema_branch_mark, style cygnet, decoder_io.Readout(tok) built first), chat template with enable_thinking=True; the
think is closed ("</think>\\n\\n" on a natural end, "\\n</think>\\n\\n" when cut), 8 greedy tokens, the first
r"\\b([A-Z])\\b" is the letter; yes/no rows map the "Yes..." letter to yes and any other letter to no.

  short_cot     maths-like rows: thinking capped at 300 tokens, 4 tries in one parallel engine call (T 0.6 / top_p
                0.95 / top_k 20, A17-B0b sampling), each answered as above, then a majority vote over the parsed keys.
                The think block opens with SHORT_STEER, a fixed generic "be brief" line (no per-set wording);
                steer="" gives the bare think prompt. Vote ties go to C1's answer when it is tied, else to the key
                that appeared first.
  capped_think  every other routed row: thinking capped at 1,024 tokens with the DEER early exit (think_engine.DEER:
                probe the trial answer at "Wait" / every 128 tokens, stop when its top letter prob >= 0.95).
  full_think    reference for the B1 rule ("full-thinking accuracy"): 8,192 tokens, no early exit, one try.

A policy never leaves a routed row unanswered at system level: no parsed answer -> C1's answer, flagged "fallback"
(A17-B0b). Backends: think_engine.SGLBackend (H100), hf_backend.HFBackend (L4), think_engine.FakeBackend (CPU tests).

  python think/policies.py --rows R.jsonl --decisions D.jsonl --out O.jsonl [--backend hf|fake] [--batch 0|1]
      D.jsonl = router.py route output ({"id", "route", "policy", "c1_key"}); only routed rows are run.
      --policy short_cot|capped_think|full_think forces one policy on every row of R (e.g. the B1 reference).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import think_engine as te  # noqa: E402
from common import read_jsonl, write_jsonl  # noqa: E402

SHORT_STEER = "Let me solve this step by step, briefly.\n"  # fixed a priori; generic, no per-set wording
SHORT = {"budget": 300, "tries": 4}
CAPPED = {"budget": 1024, "deer": dict(te.DEER)}
FULL = {"budget": 8192}
POLICIES = ("short_cot", "capped_think", "full_think")


def vote(keys: list, c1_key=None):
    """Majority vote over parsed keys (None = unparsed, ignored). Ties: C1's key if tied, else first seen."""
    got = [k for k in keys if k is not None]
    if not got:
        return None, {}
    cnt = Counter(got)
    top = max(cnt.values())
    tied = [k for k in dict.fromkeys(got) if cnt[k] == top]
    win = c1_key if c1_key in tied else tied[0]
    return win, dict(cnt)


def _groups(preps, batch):
    if batch == 1:
        return [[p] for p in preps]
    step = batch or len(preps) or 1
    return [preps[i:i + step] for i in range(0, len(preps), step)]


def short_cot(tp, items, tries=SHORT["tries"], budget=SHORT["budget"], steer=SHORT_STEER, c1_keys=None, batch=0):
    """items: [{"id", "row"}]. One engine call per group runs every try of every item in parallel."""
    c1_keys = c1_keys or {}
    recs = []
    for g in _groups(tp.prepare(items), batch):
        t0 = time.perf_counter()
        sp = [{**p, "prompt": p["prompt"] + steer} for p in g for _ in range(tries)]
        th = tp._think_plain(sp, budget)
        t1 = time.perf_counter()
        an = tp._answer(sp, th)
        t2 = time.perf_counter()
        for j, p in enumerate(g):
            a, t = an[j * tries:(j + 1) * tries], th[j * tries:(j + 1) * tries]
            win, votes = vote([x["pred_key"] for x in a], c1_keys.get(p["id"]))
            recs.append({"id": p["id"], "policy": "short_cot", "pred_key": win,
                         "letter": next((x["letter"] for x in a if win is not None and x["pred_key"] == win), None),
                         "votes": votes, "tries": tries, "parsed_tries": sum(x["pred_key"] is not None for x in a),
                         "think_tokens": max(x["tokens"] for x in t), "think_tokens_sum": sum(x["tokens"] for x in t),
                         "capped": sum(x["capped"] for x in a), "exit": Counter(x["exit"] for x in t).most_common(1)[0][0],
                         "think_s": round((t1 - t0) / len(g), 4), "answer_s": round((t2 - t1) / len(g), 4),
                         "wall_s": round((t2 - t0) / len(g), 4), "group_wall_s": round(t2 - t0, 4), "group_size": len(g)})
    return recs


def _from_run(res, policy):
    return [{"id": r["id"], "policy": policy, "pred_key": r["pred_key"], "letter": r["letter"], "tries": 1,
             "parsed_tries": int(r["pred_key"] is not None), "think_tokens": r["think_tokens"],
             "think_tokens_sum": r["think_tokens"], "capped": int(bool(r["capped"])), "exit": r["exit"],
             "probes": r["probes"], "chunks": r["chunks"], "deer_conf": r["conf"], "accept_len": r["accept_len"],
             "think_s": r["think_s"], "answer_s": r["answer_s"], "wall_s": round(r["think_s"] + r["answer_s"], 4),
             "group_wall_s": r["group_wall_s"], "group_size": r["group_size"]} for r in res["records"]]


def capped_think(tp, items, budget=CAPPED["budget"], deer=None, batch=0, **_):
    return _from_run(tp.run(items, budget, deer=deer if deer is not None else CAPPED["deer"], batch=batch),
                     "capped_think")


def full_think(tp, items, budget=FULL["budget"], batch=0, **_):
    return _from_run(tp.run(items, budget, deer=None, batch=batch), "full_think")


def run_policy(tp, items, policy, c1_keys=None, batch=0, **kw):
    """Run one policy and apply the A17-B0b fallback: no parsed answer -> C1's key ("fallback": true)."""
    c1_keys = c1_keys or {}
    if policy == "short_cot":
        recs = short_cot(tp, items, c1_keys=c1_keys, batch=batch, **kw)
    elif policy == "capped_think":
        recs = capped_think(tp, items, batch=batch, **kw)
    elif policy == "full_think":
        recs = full_think(tp, items, batch=batch, **kw)
    else:
        raise ValueError(f"unknown policy {policy!r}")
    for r in recs:
        r["fallback"] = r["pred_key"] is None
        r["final_key"] = c1_keys.get(r["id"]) if r["fallback"] else r["pred_key"]
    return recs


def run_routed(tp, rows, decisions, batch=0, force=None, **kw):
    """Routed rows only (decisions[id]["route"]), each with its router policy (or `force` for every row)."""
    by_pol, c1 = {}, {}
    for row in rows:
        d = decisions.get(row["id"]) or {}
        c1[row["id"]] = d.get("c1_key")
        if force or d.get("route"):
            by_pol.setdefault(force or d["policy"], []).append({"id": row["id"], "row": row})
    out = []
    for pol in POLICIES:
        if by_pol.get(pol):
            out += run_policy(tp, by_pol[pol], pol, c1_keys=c1, batch=batch, **kw)
    return out


BASE, REV = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"  # think_run.py


def make_path(backend: str, seed=0, device="cuda"):
    """(ThinkPath, backend). hf = base Qwen3.5-4B (LoRA OFF) in BF16 on the L4, as think_run.py; fake = CPU test
    double with the locally cached tokenizer."""
    import decoder_io as dio
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(BASE, revision=REV, local_files_only=(backend == "fake"))
    tok.padding_side = "left"
    if backend == "fake":
        be = te.FakeBackend(think_len=200)
    else:
        import torch
        from transformers import AutoModelForCausalLM
        from hf_backend import HFBackend
        model = AutoModelForCausalLM.from_pretrained(BASE, revision=REV, torch_dtype=torch.bfloat16,
                                                     device_map=device).eval()
        be = HFBackend(model, tok, seed=seed)
    return te.ThinkPath(be, tok, dio), be


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", required=True)
    ap.add_argument("--decisions", default=None, help="router.py route output; needed unless --policy is given")
    ap.add_argument("--policy", default=None, choices=POLICIES, help="force one policy on every row")
    ap.add_argument("--out", required=True)
    ap.add_argument("--backend", default="hf", choices=["hf", "fake"])
    ap.add_argument("--batch", type=int, default=0, help="1 = one request at a time (latency); 0 = chunk at once")
    ap.add_argument("--chunk", type=int, default=64, help="rows per resumable chunk")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args(argv)
    if not a.decisions and not a.policy:
        ap.error("give --decisions or --policy")
    rows = list(read_jsonl(a.rows))
    dec = {d["id"]: d for d in read_jsonl(a.decisions)} if a.decisions else {}
    out = Path(a.out)
    done = {r["id"] for r in read_jsonl(out)} if out.exists() else set()
    todo = [r for r in rows if r["id"] not in done and (a.policy or (dec.get(r["id"]) or {}).get("route"))]
    tp, _ = make_path(a.backend, a.seed)
    t0 = time.time()
    with open(out, "a", encoding="utf-8") as f:
        for i in range(0, len(todo), a.chunk):
            part = todo[i:i + a.chunk]
            for r in run_routed(tp, part, dec, batch=a.batch, force=a.policy):
                f.write(json.dumps({**r, "backend": a.backend}) + "\n")
            f.flush()
            print(json.dumps({"done": min(i + a.chunk, len(todo)), "of": len(todo), "sec": round(time.time() - t0)}),
                  flush=True)
    print("RUN DONE", round(time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
