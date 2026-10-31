"""Reviewer round 2 (CPU, Mac): independent re-score of the saved per-item logs, written from the bench's README/score.py rules without
importing score_vision.py. No real C1/base logs exist yet (GPU not run), so the only saved per-item logs are the synthetic ones the
harness' own tests wrote (tests/tmp_scorer/preds_{c1,base}.jsonl). This re-scores those and compares with tests/tmp_scorer/scores.json,
then probes three scorer behaviours on small synthetic edits (written to the scratchpad, never into tests/).
Run: vision_bench/.venv/bin/python -I -B harness/rv2_rescore.py"""
import json, math, os, subprocess, sys, shutil
import numpy as np
from sklearn.metrics import roc_auc_score

VB = "/Users/aryamahadik/Documents/jev/vision_bench"
SCR = "/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/adbc4a3b-e366-431b-b0e2-96c55904b928/scratchpad/rescore"
SUITES = ["img_sst2", "img_ar_sentiment", "img_pets", "img_vqa_yesno", "img_count"]

cases = {}
for s in SUITES:
    for l in open(f"{VB}/data/{s}/cases.jsonl", encoding="utf-8"):
        c = json.loads(l); cases[c["id"]] = c


def gold_and_k(c):
    qid, q = next(iter(c["questions"].items()))
    g = c["gold"][qid]["label"]
    if q["type"] == "noul": return int(g), 2
    if q["type"] == "score": return int(g), len(q["criteria"])
    return list(q["criteria"]).index(g), len(q["criteria"])


def ece10(conf, ok):
    conf = np.asarray(conf, float); ok = np.asarray(ok, float); e = 0.0
    for b in range(10):
        lo, hi = b / 10, (b + 1) / 10
        m = (conf > lo) & (conf <= hi)          # (lo, hi]
        if m.any(): e += m.sum() / len(conf) * abs(conf[m].mean() - ok[m].mean())
    return e


def rescore(path, failed_counts_correct=True):
    preds = {}
    for l in open(path):
        r = json.loads(l); preds[r["id"]] = r
    per = {s: {"c": [], "conf": [], "fail": 0, "pty": [], "nll": []} for s in SUITES}
    for cid, c in cases.items():
        y, k = gold_and_k(c)
        r = preds.get(cid)
        if r is None or "error" in r:
            p = np.full(k, 1 / k); per[c["suite"]]["fail"] += 1; failed = True
        else:
            p = np.array(r["probs"], float); p = p / p.sum(); failed = False
        yh = int(np.argmax(p))
        per[c["suite"]]["c"].append(int(yh == y) if not (failed and not failed_counts_correct) else 0)
        per[c["suite"]]["conf"].append(p.max()); per[c["suite"]]["nll"].append(-math.log(max(p[y], 1e-6)))
    out = {}
    allc, allconf = [], []
    for s in SUITES:
        d = per[s]; out[s] = {"acc": float(np.mean(d["c"])), "ece": ece10(d["conf"], d["c"]), "failed": d["fail"], "nll": float(np.mean(d["nll"]))}
        allc += d["c"]; allconf += d["conf"]
    out["index"] = 100 * float(np.mean([out[s]["acc"] for s in SUITES]))
    out["all_ece"] = ece10(allconf, allc)
    return out


bad = 0
sc = json.load(open(f"{VB}/tests/tmp_scorer/scores.json"))
for m in ("c1", "base"):
    mine = rescore(f"{VB}/tests/tmp_scorer/preds_{m}.jsonl"); strict = rescore(f"{VB}/tests/tmp_scorer/preds_{m}.jsonl", failed_counts_correct=False)
    h = sc[m]
    for s in SUITES:
        for a, b, nm in ((mine[s]["acc"], h[s]["acc"], "acc"), (mine[s]["ece"], h[s]["ece"], "ece"), (mine[s]["nll"], h[s]["nll"], "nll"),
                         (strict[s]["acc"], h[s]["acc_strict"], "acc_strict")):
            if abs(a - b) > 6e-5: bad += 1; print("MISMATCH", m, s, nm, a, b)
    for a, b, nm in ((mine["index"], h["vision_index"], "index"), (strict["index"], h["vision_index_strict"], "index_strict"),
                     (mine["all_ece"], h["all"]["ece"], "all_ece")):
        if abs(a - b) > 6e-3: bad += 1; print("MISMATCH", m, nm, a, b)
    print(f"{m}: independent Index {mine['index']:.2f} (harness {h['vision_index']}) strict {strict['index']:.2f} (harness {h['vision_index_strict']}) | all-ECE {100*mine['all_ece']:.2f}% (harness {100*h['all']['ece']:.2f}%) | failed {sum(mine[s]['failed'] for s in SUITES)}")
print("re-score mismatches vs harness scores.json:", bad)

# ---- probe 1: a NaN probability vector is not counted as a failure
shutil.rmtree(SCR, ignore_errors=True); os.makedirs(SCR)
src = [json.loads(l) for l in open(f"{VB}/tests/tmp_scorer/preds_c1.jsonl")]
def write(rows, name):
    open(f"{SCR}/{name}", "w").write("\n".join(json.dumps(r) for r in rows) + "\n")
def run_scorer(res_dir):
    env = {**os.environ, "VB_RESULTS": res_dir}
    r = subprocess.run([f"{VB}/.venv/bin/python", "-I", "-B", f"{VB}/harness/score_vision.py"], capture_output=True, text=True, env=env)
    return r, (json.load(open(f"{res_dir}/scores.json")) if r.returncode == 0 else None)

rows = [dict(r) for r in src]
nan_ids = []
for r in rows:
    if "error" in r: continue
    c = cases[r["id"]]; y, k = gold_and_k(c)
    if y == 0 and len(nan_ids) < 20:
        r["probs"] = [float("nan")] * k; nan_ids.append(r["id"])
d1 = f"{SCR}/nan"; os.makedirs(d1)
write(rows, "nan/preds_c1.jsonl")
r1, s1 = run_scorer(d1)
base_run = rescore(f"{VB}/tests/tmp_scorer/preds_c1.jsonl")
print(f"\n[probe NaN] scorer rc={r1.returncode}; {len(nan_ids)} items given all-NaN probabilities (gold option 0 each)")
if s1:
    print("   failed reported:", s1["c1"]["all"]["failed"], "| Index with NaN rows:", s1["c1"]["vision_index"], "vs clean fixture", round(base_run["index"], 2),
          "| acc NaN rows counted correct:", "yes" if s1["c1"]["vision_index"] > base_run["index"] - 1e-9 else "no")
else:
    print("   scorer stderr:", r1.stderr[-400:])

# ---- probe 2: verdict vs Jev uses the bench-rule Index even when failures exist
rows2 = []
for r in src:
    r = dict(r)
    rows2.append(r)
# make C1 equal to Jev 1.14 (acc about 85.1) is not possible here; instead fail every item of one suite and compare rule vs strict verdict inputs
d2 = f"{SCR}/fail"; os.makedirs(d2)
fr = []
for r in src:
    c = cases[r["id"]]
    fr.append({"id": r["id"], "suite": c["suite"], "error": "synthetic"} if c["suite"] in ("img_sst2", "img_vqa_yesno") else r)
write(fr, "fail/preds_c1.jsonl")
r2, s2 = run_scorer(d2)
if s2:
    o = s2["c1"]
    print("\n[probe failures] two yes/no suites fully failed (400 items): bench-rule Index", o["vision_index"], "| strict Index", o["vision_index_strict"],
          "| vs Jev 1.14 index_diff used for the verdict:", o["vs_jev114"]["index_diff"], "=", round(o["vision_index"] - 85.1, 2), "(bench-rule) vs", round(o["vision_index_strict"] - 85.1, 2), "(strict)")
    print("   verdict text:", o["vs_jev114"]["verdict"])
else:
    print("   scorer stderr:", r2.stderr[-400:])
