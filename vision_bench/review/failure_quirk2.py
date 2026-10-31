import json, sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/vision_bench/harness")
import score_vision as sv
cases = sv.load_cases()
OUT = "/Users/aryamahadik/Documents/jev/vision_bench/review/tmp/preds_allfail.jsonl"
seen=set()
with open(OUT, "w") as f:
    for cid, c in cases.items():
        if c['suite'] not in seen:   # one ok row only so the latency summary has something to take percentiles of
            qid, q = next(iter(c["questions"].items())); k = 2 if q["type"] == "noul" else len(q["criteria"])
            f.write(json.dumps({"id": cid, "suite": c["suite"], "probs": [1.0 / k] * k, "compute_ms": 1, "fwd_ms": 1, "prep_ms": 1}) + "\n"); seen.add(c["suite"])
        else:
            f.write(json.dumps({"id": cid, "suite": c["suite"], "error": "x"}) + "\n")
r = sv.score_model("allfail", cases, OUT)
print({s: (r[s]["acc"], r[s]["failed"]) for s in sv.SUITES}, "Vision Index", r["vision_index"], "failed", r["all"]["failed"])
