"""SB5 apply A46 drops (drop only, no relabel), gates, package, official selection dry-run. Counts only on stdout.
Usage: python -B sb5_apply.py   (reads screen/REPLAY_DENY_A46.json, work/candidates.jsonl, work/owndev.jsonl)"""
import json, subprocess, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sb5_lib import *
deny = json.load(open(SB5 / "screen/REPLAY_DENY_A46.json"))
drop = set(deny["drop_ids"])
fp = json.load(open(SB5 / "screen/adjudicate/FIRST_PASS.json")) if (SB5 / "screen/adjudicate/FIRST_PASS.json").exists() else {}
def split(src, dst):
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    keep = [r for r in rows if r["id"] not in drop]; gone = [r for r in rows if r["id"] in drop]
    with open(dst, "w", encoding="utf-8") as f:
        for r in keep: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows, keep, gone
c0, c1, cg = split(WORK / "candidates.jsonl", WORK / "candidates_screened.jsonl")
d0, d1, dg = split(WORK / "owndev.jsonl", WORK / "owndev_screened.jsonl")
rep = {"deny_ids": len(drop), "candidates": [len(c0), len(c1), len(cg)], "owndev": [len(d0), len(d1), len(dg)],
       "ids_unmatched": len(drop - {r["id"] for r in c0 + d0}),
       "dropped_by_label": dict(Counter(r["meta"]["sb5"]["orig_label"] for r in cg + dg)),
       "dropped_by_answer": dict(Counter(r["gold"] for r in cg + dg)),
       "kept_cells": dict(Counter(f'{r["meta"]["sb5"]["orig_label"]}/{r["gold"]}' for r in c1)),
       "deny_counts": deny["counts"]}
json.dump(rep, open(WORK / "apply_report.json", "w"), indent=1)
print(json.dumps(rep))
