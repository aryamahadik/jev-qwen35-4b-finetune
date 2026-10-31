"""End-to-end check of score_vision.py on synthetic results: failures reported per suite and strictly, a suite with NO successful row
does not crash the scorer, diagnostics are scored, latency is labelled not comparable. Writes only under tests/tmp_scorer."""
import json, os, random, subprocess, sys, shutil
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); VB = os.path.dirname(HERE)
OUT = f"{HERE}/tmp_scorer"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
sys.path.insert(0, f"{VB}/harness")
os.environ["VB_RESULTS"] = OUT
import score_vision as sv
cases = sv.load_cases()
rng = random.Random(3); nrng = np.random.default_rng(3)

def gold(c):
    qid, q = next(iter(c["questions"].items()))
    return q, (list(q["criteria"]).index(c["gold"][qid]["label"]) if q["type"] == "choice" else int(c["gold"][qid]["label"]))

def synth(boost, dead_suite=None, fail_frac=0.0):
    rows = []
    for cid, c in cases.items():
        q, y = gold(c); k = 2 if q["type"] == "noul" else len(q["criteria"])
        if c["suite"] == dead_suite or rng.random() < fail_frac:
            rows.append({"id": cid, "suite": c["suite"], "error": "synthetic"}); continue
        lg = nrng.normal(0, 1.2, k); lg[y] += boost
        p = np.exp(lg - lg.max()); p /= p.sum()
        ms = rng.uniform(80, 300)
        rows.append({"id": cid, "suite": c["suite"], "probs": [float(x) for x in p], "compute_ms": ms, "fwd_ms": ms * .8, "prep_ms": ms * .2,
                     "retried": rng.random() < 0.01 or None})
    return rows
def dump(path, rows):
    open(path, "w").write("\n".join(json.dumps(r) for r in rows) + "\n")
dump(f"{OUT}/preds_c1.jsonl", synth(2.5, fail_frac=0.01))
dump(f"{OUT}/preds_base.jsonl", synth(1.5, dead_suite="img_pets"))      # a whole suite failed: must not crash
for m in ("c1", "base"):
    d = []
    for cid, c in cases.items():
        q, y = gold(c)
        if c["suite"] == "img_count" or q["type"] == "noul":
            k = 2 if q["type"] == "noul" else len(q["criteria"]); lg = nrng.normal(0, 1.2, k); lg[y] += 1.0
            p = np.exp(lg - lg.max()); p /= p.sum()
            d.append({"id": cid, "suite": c["suite"], "variant": "x", "probs": [float(x) for x in p]} if rng.random() > 0.01 else {"id": cid, "error": "x"})
    dump(f"{OUT}/diag_{m}.jsonl", d)
    json.dump({"c1": {"p50": 400.0, "p95": 900.0}, "c8": {"p50": 2500.0, "p95": 4000.0}}, open(f"{OUT}/e2e_{m}.json", "w"))
r = subprocess.run([sys.executable, "-I", f"{VB}/harness/score_vision.py"], capture_output=True, text=True, env={**os.environ, "VB_RESULTS": OUT})
print(r.stdout[-6500:]); print(r.stderr[-1500:])
assert r.returncode == 0, r.returncode
s = json.load(open(f"{OUT}/scores.json"))
assert s["base"]["img_pets"]["failed"] == 200 and s["base"]["latency_compute_by_suite"]["img_pets"]["p50"] is None
assert s["c1"]["all"]["failed"] > 0 and s["c1"]["vision_index_strict"] <= s["c1"]["vision_index"]
assert "NOT COMPARABLE" in r.stdout and "FAILED" in r.stdout and "DIAGNOSTICS" in r.stdout
print("SCORER TEST PASSED")
