"""prompt_audit.py: the rendered-prompt identity and thinking-OFF audit of plan section 6 (v3), CPU, over dump files.

  prompt_audit.py --dumps out/dump_trainer.jsonl out/dump_gate.jsonl out/dump_server.jsonl [--expect-n 11957] --out out/prompt_audit.json

Each dump is written by dump_prompt_shas.py (or by the training side with the same schema, one line per prompt:
{"source","key","prompt_sha256","ids_sha256","n_tokens","think_state","tail"}). PASS needs ALL of:
  1. every dump has the same key set (a missing or extra key is a problem; --expect-n also fixes the size);
  2. for every key the prompt_sha256 (and ids_sha256 when present) is identical in every dump ("identical rendered-prompt
     sha in trainer, gate and server");
  3. think_state == "off" in every line of every dump (Qwen3.5 thinks by default; enable_thinking False renders an empty
     think block). "open" and "other" are problems; the tail strings (template tokens only) are listed.
Any re-render (a template, card, option-order or system-prompt change) needs a new audit: the output records the sha256 of
each dump file so a stale audit is visible. Counts only; keys appear as 8-character hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402


def hid(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()[:8]


def audit(dumps: dict, expect_n: int | None = None) -> dict:
    """dumps: {label: {key: record}} -> report."""
    labels = list(dumps)
    problems = []
    keysets = {lb: set(d) for lb, d in dumps.items()}
    union = set().union(*keysets.values()) if keysets else set()
    for lb in labels:
        miss = union - keysets[lb]
        if miss:
            problems.append({"kind": "missing_keys", "dump": lb, "n": len(miss), "examples": sorted(hid(k) for k in miss)[:5]})
        if expect_n is not None and len(keysets[lb]) != expect_n:
            problems.append({"kind": "unexpected_size", "dump": lb, "n": len(keysets[lb]), "expected": expect_n})
    mism_prompt = mism_ids = 0
    ex = []
    for k in sorted(union):
        recs = [dumps[lb][k] for lb in labels if k in dumps[lb]]
        if len({r["prompt_sha256"] for r in recs}) > 1:
            mism_prompt += 1
            ex.append(hid(k))
        ids = {r.get("ids_sha256") for r in recs if r.get("ids_sha256")}
        if len(ids) > 1:
            mism_ids += 1
    if mism_prompt:
        problems.append({"kind": "prompt_sha_mismatch", "n": mism_prompt, "examples": ex[:5]})
    if mism_ids:
        problems.append({"kind": "ids_sha_mismatch", "n": mism_ids})
    think = {lb: dict(Counter(r.get("think_state") for r in d.values())) for lb, d in dumps.items()}
    tails = {lb: dict(Counter(r.get("tail") for r in d.values() if r.get("think_state") != "off").most_common(5))
             for lb, d in dumps.items()}
    for lb, c in think.items():
        bad = sum(v for k, v in c.items() if k != "off")
        if bad:
            problems.append({"kind": "thinking_not_off", "dump": lb, "n": bad, "tails": tails[lb]})
    return {"n": len(union), "dumps": labels, "think_state": think, "problems_n": sum(p["n"] for p in problems),
            "problems": problems, "verdict": "PASS" if union and not problems else "FAIL"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dumps", nargs="+", required=True)
    ap.add_argument("--expect-n", type=int)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if len(a.dumps) < 2:
        raise SystemExit("need at least two dumps (e.g. trainer and server) to compare")
    dumps, shas = {}, {}
    for p in a.dumps:
        recs = C.read_jsonl(p)
        lb = (recs[0].get("source") if recs else None) or Path(p).stem
        if lb in dumps:
            lb = f"{lb}:{Path(p).stem}"
        dumps[lb] = {r["key"]: r for r in recs}
        shas[lb] = {"file": p, "sha256": C.sha256_file(p), "lines": len(recs)}
    rep = audit(dumps, a.expect_n)
    rep["files"] = shas
    rep["tag"] = C.tag("author-run", n=rep["n"], source="dump_prompt_shas.py dumps") if rep["n"] else C.tag("not-measured")
    rep["utc"] = C.utc()
    C.write_json(a.out, rep)
    print(f"prompts={rep['n']} dumps={rep['dumps']} think={rep['think_state']} problems={rep['problems_n']} -> {rep['verdict']}")
    return 0 if rep["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
