import json, os, sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/vision_bench/harness")
import score_vision as sv
cases = sv.load_cases()
OUT = "/Users/aryamahadik/Documents/jev/vision_bench/review/tmp/preds_allfail.jsonl"
with open(OUT, "w") as f:
    for cid, c in cases.items():
        f.write(json.dumps({"id": cid, "suite": c["suite"], "error": "x"}) + "\n")
# score_model needs latency of ok rows -> patch: with all failed there are none; compute accuracy part only
rows = []
import numpy as np
for cid, c in cases.items():
    qid, q = next(iter(c["questions"].items()))
    k = 2 if q["type"] == "noul" else len(q["criteria"])
    y = list(q["criteria"].keys()).index(c["gold"][qid]["label"]) if q["type"] == "choice" else int(c["gold"][qid]["label"])
    rows.append((c["suite"], y == 0))
for s in sv.SUITES:
    r = [x for t, x in rows if t == s]
    print(s, "ALL 200 decisions failed -> scorer accuracy", round(100 * sum(r) / len(r), 1), "%  (= share of items whose gold is option 0)")
