"""DI-KR apply A46 drops (drop only, no relabel) -> candidates_screened.jsonl / owndev_screened.jsonl, gates, counts. Usage: python -I -B kr_apply.py
Reads screen/REPLAY_DENY_A46.json (screen.py finalize) plus an optional work/extra_drop_ids.json (rows dropped by the p_g < 0.05 re-read cascade)."""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kr_lib import *
deny = json.load(open(KR / "screen/REPLAY_DENY_A46.json"))
drop = set(deny["drop_ids"])
ex = WORK / "extra_drop_ids.json"
if ex.exists(): drop |= set(json.load(open(ex)))
def split(src, dst):
    rows = [json.loads(l) for l in open(src, encoding="utf-8")]
    keep = [r for r in rows if r["id"] not in drop]; gone = [r for r in rows if r["id"] in drop]
    with open(dst, "w", encoding="utf-8") as f:
        for r in keep: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows, keep, gone
c0, c1, cg = split(WORK / "candidates.jsonl", WORK / "candidates_screened.jsonl")
d0, d1, dg = split(WORK / "owndev.jsonl", WORK / "owndev_screened.jsonl")
rep = {"deny_ids": len(drop), "candidates": [len(c0), len(c1), len(cg)], "owndev": [len(d0), len(d1), len(dg)], "ids_unmatched": len(drop - {r["id"] for r in c0 + d0}),
       "dropped_by_gold_rank": dict(Counter(r["meta"]["di_kr"]["gold_rank"] for r in cg + dg)),
       "kept_by_gold_rank": dict(Counter(r["meta"]["di_kr"]["gold_rank"] for r in c1)), "kept_by_position": dict(Counter(r["options"].index(r["gold"]) for r in c1)),
       "deny_counts": deny.get("counts")}
json.dump(rep, open(WORK / "apply_report.json", "w"), indent=1); print(json.dumps(rep))
