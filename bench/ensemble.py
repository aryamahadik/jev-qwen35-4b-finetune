"""Offline two-view ensemble of JevBench runs (exact, no GPU): p = w*p_A + (1-w)*p_B, then JevBench's own scoring.
Latency of the ensemble = sum of both views (two forward passes; same weights with the adapter on/off)."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, f"{H}/jevbench")
from jevbench.tasks import load_jsonl
from jevbench.scoring import score_task
a, b, w, dst = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
T = {t.id: t for f in ("easy", "original", "hard") for t in load_jsonl(f"{H}/jevbench/datasets/public/{f}.jsonl")}
A = {json.loads(l)["task_id"]: json.loads(l) for l in open(f"{H}/runs/{a}/results.jsonl")}
B = {json.loads(l)["task_id"]: json.loads(l) for l in open(f"{H}/runs/{b}/results.jsonl")}
os.makedirs(f"{H}/runs/{dst}", exist_ok=True)
with open(f"{H}/runs/{dst}/results.jsonl", "w") as f:
    for i, ra in A.items():
        rb = B[i]; r = dict(ra)
        p = {k: w * ra["probs"].get(k, 0) + (1 - w) * rb["probs"].get(k, 0) for k in set(ra["probs"]) | set(rb["probs"])}
        r["probs"] = p; sc = score_task(p, T[i]); r["correct"] = sc["correct"]; r["predicted"] = sc.get("predicted")
        r["latency_s"] = ra["latency_s"] + rb["latency_s"]
        r["usage"] = {"input_tokens": (ra.get("usage") or {}).get("input_tokens", 0) + (rb.get("usage") or {}).get("input_tokens", 0), "output_tokens": 0}
        f.write(json.dumps(r) + "\n")
