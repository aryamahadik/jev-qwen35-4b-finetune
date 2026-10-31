"""Official selection dry-run on the screened SB5 pool (report only, writes work/select_dry.json)."""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sb5_lib import *
sys.path.insert(0, str(LEAN))
import c2_select as S, shard_golden as sg
rows = [json.loads(l) for l in open(WORK / "candidates_screened.jsonl", encoding="utf-8")]
probs = sg.load_labels(LEAN / "data/c2_crowd_shards/SB5/labels_q35_4b_main500k")
pg = S.c1_pg(rows, probs)
rec = S.select_family("SB5", rows, [], pg, 750)
sel = set(rec["selected_ids"]); sr = [r for r in rows if r["id"] in sel]
out = {"rows": len(rows), "selected": len(sel), "yes_share": round(sum(r["gold"] for r in sr) / len(sr), 4),
       "labels": dict(Counter(r["meta"]["sb5"]["orig_label"] for r in sr)),
       "bins": dict(Counter(rec["difficulty_bin"][i] for i in sel)),
       "wordings": len(Counter(r["meta"]["wording_id"] for r in sr)),
       "a49c_failing": rec["report"]["a49c"]["failing"], "g5": {k: (len(v) if hasattr(v, "__len__") else v) for k, v in rec["g5"].items()} if isinstance(rec["g5"], dict) else str(rec["g5"])[:200],
       "mean_pg_selected": round(sum(pg[i] for i in sel) / len(sel), 4)}
json.dump(out, open(WORK / "select_dry.json", "w"), indent=1); print(json.dumps(out))
