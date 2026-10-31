"""Harness scorer (score_vision.py) vs the bench's own score.py on the same synthetic predictions, written in each tool's own format
(harness: preds_*.jsonl with 'probs'; bench: Decisions-API answers built by the harness' own decision_record()).
score.py and data_lock.py were read in full before this was written (no import-time side effects); they are loaded from review/."""
import importlib.util, json, math, os, random, sys
import numpy as np
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/vision_bench/harness")
os.environ["VB_RESULTS"] = "/Users/aryamahadik/Documents/jev/vision_bench/review/tmp"
import vb_core as vb
import score_vision as sv
BENCH = "/Users/aryamahadik/Documents/jev/vision_bench/src/system-one-bench"
sys.path.insert(0, BENCH)
spec = importlib.util.spec_from_file_location("bench_score", f"{BENCH}/score.py")
bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)

cases = sv.load_cases()
bs.cases.update(cases)
rng = random.Random(7); nrng = np.random.default_rng(7)
OUT = "/Users/aryamahadik/Documents/jev/vision_bench/review/tmp"; os.makedirs(OUT, exist_ok=True)
fail_ids = set(rng.sample(sorted(cases), 12)) | {"img_count-0", "img_pets-0", "img_sst2-3"}   # incl. items whose gold is option 0 (check later)
h_rows, b_rows = [], []
for cid, c in cases.items():
    qid, q = next(iter(c["questions"].items()))
    gold = vb.gold_index(q, c["gold"][qid])
    k = 2 if q["type"] == "noul" else len(vb.bench_options(q))
    lg = nrng.normal(0, 1.5, k); lg[gold] += rng.choice([0.0, 1.0, 2.5, 4.0])
    p = np.exp(lg - lg.max()); p /= p.sum()
    if cid in fail_ids:
        h_rows.append({"id": cid, "suite": c["suite"], "error": "synthetic failure"})
        b_rows.append({"id": cid, "error": "synthetic failure"})
        continue
    probs = [float(x) for x in p]
    ms = rng.uniform(50, 400)
    h_rows.append({"id": cid, "suite": c["suite"], "probs": probs, "compute_ms": ms, "fwd_ms": ms * .8, "prep_ms": ms * .2})
    b_rows.append({"id": cid, "answers": {qid: vb.decision_record(q, None, probs)}, "ms": ms})
hp, bp = f"{OUT}/preds_synth.jsonl", f"{OUT}/bench_preds_synth.jsonl"
open(hp, "w").write("\n".join(json.dumps(r) for r in h_rows) + "\n")
open(bp, "w").write("\n".join(json.dumps(r) for r in b_rows) + "\n")

mine = sv.score_model("synth", cases, hp)
rows, lat, cost = bs.load(bp)
by = {}
for r in rows:
    by.setdefault(r["suite"], []).append(r)
bench = {s: bs.metrics(by[s]) for s in sv.SUITES}
bench["all"] = bs.metrics(rows)
keys = ["n", "failed", "acc", "macro_f1", "nll", "brier", "ece", "p_true_zero", "conf_auroc", "acc_at_50cov", "score_mae"]
worst = 0.0; bad = []
for s in sv.SUITES + ["all"]:
    for kk in keys:
        a, b = mine[s].get(kk), bench[s].get(kk)
        if a is None and b is None: continue
        if isinstance(a, float) and math.isnan(a) and math.isnan(b): continue
        d = abs(float(a) - float(b)); worst = max(worst, d)
        if d > 1e-9: bad.append((s, kk, a, b))
print("metric keys compared:", len(sv.SUITES) * 0 + (len(sv.SUITES) + 1) * len(keys), "| worst abs diff:", worst, "| mismatches:", bad)
vi_bench = round(100 * float(np.mean([bench[s]["acc"] for s in sv.SUITES])), 2)
print("Vision Index harness vs bench-formula:", mine["vision_index"], vi_bench)
print("failed counted:", mine["all"]["failed"], bench["all"]["failed"])
# failure quirk: a failed item with gold == option 0 is counted CORRECT by both scorers
for cid in ["img_count-0", "img_pets-0", "img_sst2-3"]:
    c = cases[cid]; qid, q = next(iter(c["questions"].items()))
    print(cid, "gold index", vb.gold_index(q, c["gold"][qid]), "(failed run -> uniform -> argmax 0)")
# same run with those 3 failed items replaced by deliberately WRONG answers: accuracy delta caused by the argmax-0 rule
