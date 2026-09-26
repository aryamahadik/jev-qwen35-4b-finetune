"""Offline post-processing of JevBench runs (exact, no GPU): temperature scaling and S1/S2 blending, then re-score
with JevBench's own score_task. Usage:
  apply_T.py SRC DST --T 0.8,0.95                       (per-type temperature on stored probabilities)
  apply_T.py SRC_S2 DST --blend_s1 SRC_S1 --w 0.75       (escalated items: w*S2 + (1-w)*S1)
"""
import argparse, json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "jevbench"))
from jevbench.tasks import load_jsonl
from jevbench.scoring import score_task
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--T", default="1,1"); ap.add_argument("--blend_s1", default=None); ap.add_argument("--w", type=float, default=1.0)
a = ap.parse_args()
H = os.path.dirname(os.path.abspath(__file__))
tasks = {t.id: t for f in ("easy", "original", "hard") for t in load_jsonl(f"{H}/jevbench/datasets/public/{f}.jsonl")}
tn, tc = map(float, a.T.split(","))
S1 = {json.loads(l)["task_id"]: json.loads(l) for l in open(f"{H}/runs/{a.blend_s1}/results.jsonl")} if a.blend_s1 else {}
os.makedirs(f"{H}/runs/{a.dst}", exist_ok=True)
with open(f"{H}/runs/{a.dst}/results.jsonl", "w") as f:
    for l in open(f"{H}/runs/{a.src}/results.jsonl"):
        r = json.loads(l); t = tasks[r["task_id"]]
        p = dict(r["probs"])
        if a.blend_s1 and (r.get("runtime") or {}).get("system2"):
            p1 = S1[r["task_id"]]["probs"]; p = {k: a.w * p[k] + (1 - a.w) * p1.get(k, 0.0) for k in p}
        T = tn if t.question["type"] == "noul" else tc
        z = {k: math.exp(math.log(max(v, 1e-12)) / T) for k, v in p.items()}; s = sum(z.values())
        r["probs"] = {k: v / s for k, v in z.items()}
        sc = score_task(r["probs"], t); r["correct"] = sc["correct"]; r["predicted"] = sc.get("predicted")
        f.write(json.dumps(r) + "\n")
print("wrote", a.dst)
