"""Official selection dry-run on the DI-KR pool (report only; writes work/select_dry.json, work/crowd_summary.json). Usage: python -B kr_selectdry.py [candidates.jsonl]"""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kr_lib import *
sys.path.insert(0, str(LEAN))
import c2_select as S, shard_golden as sg
src = sys.argv[1] if len(sys.argv) > 1 else str(WORK / "candidates.jsonl")
rows = [json.loads(l) for l in open(src, encoding="utf-8")]
probs = sg.load_labels(LEAN / "data/c2_crowd_shards/DI-KR/labels_q35_4b_main500k")
pg = S.c1_pg(rows, probs)
low = sorted(r["id"] for r in rows if pg[r["id"]] < 0.05)
bins = Counter()
agree = 0
for r in rows:
    p = probs[r["id"]]
    top = max(p, key=p.get)
    agree += (top == r["gold"])
cells = Counter()
for r in rows:
    p = probs[r["id"]]; top = max(p, key=p.get)
    cells[(r["meta"]["di_kr"]["gold_rank"], "ok" if top == r["gold"] else "wrong")] += 1
summ = {"rows": len(rows), "c1_agrees_with_gold": round(agree / len(rows), 4), "p_g_lt_0.05": len(low), "low_pg_ids_n": len(low),
        "mean_pg": round(sum(pg[r["id"]] for r in rows) / len(rows), 4), "cells_rank_vs_c1": {f"{k[0]}/{k[1]}": v for k, v in sorted(cells.items())}}
rec = S.select_family("DI-KR", rows, [], pg, 2400)
sel = set(rec["selected_ids"]); sr = [r for r in rows if r["id"] in sel]
out = {"rows": len(rows), "selected": len(sel), "bins": dict(Counter(rec["difficulty_bin"][i] for i in sel)),
       "wordings": len(Counter(r["meta"]["wording_id"] for r in sr)), "pos": dict(Counter(r["options"].index(r["gold"]) for r in sr)),
       "rank": dict(Counter(r["meta"]["di_kr"]["gold_rank"] for r in sr)), "a49c_failing": rec["report"]["a49c"]["failing"],
       "mean_pg_selected": round(sum(pg[i] for i in sel) / len(sel), 4)}
json.dump({**summ, "low_pg_ids": low}, open(WORK / "crowd_summary.json", "w"), indent=1)
json.dump(out, open(WORK / "select_dry.json", "w"), indent=1); print(json.dumps(summ)); print(json.dumps(out))
