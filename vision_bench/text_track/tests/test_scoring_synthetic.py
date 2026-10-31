import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
"""score_text.py (which runs the bench's own score.py) and skeptic_rescore.py on COMPLETE synthetic per-item logs for all 4,850 decisions:
random logits with a signal toward the gold option, two failed decisions, one retried decision, diagnostics for every score and yes/no
item, latency rows, a Modal cost file. Expected: the skeptic finds every number identical (exit 0). Then three deliberate corruptions
(a changed accuracy in scores.json, a changed logit, a missing decision) must each be caught. Writes only under tests/tmp_synth."""
import json, os, shutil, subprocess, sys
from common import *
import numpy as np, torch
import tt_core as tt
PY = sys.executable
OUT = f"{TT}/tests/tmp_synth"; shutil.rmtree(OUT, ignore_errors=True); R = f"{OUT}/results"; os.makedirs(R)
ds = tt.load_decisions()
rng = np.random.default_rng(0)

def make(arm, boost, variant="main", only=None):
    recs = []
    for i, d in enumerate(ds):
        if only and not tt.variant_applies(d, variant): continue
        row, keys = tt.to_row(d["q"], d["state"], score_prefix=(variant != "score_noprefix"))
        views = tt.views_for(row, variant)
        k = 2 if row["qtype"] == "noul" else len(row["options"])
        lgs = []
        for perm in views:
            lg = rng.normal(size=k) * 1.5
            if row["qtype"] == "noul":
                p = perm if perm is not None else [0, 1]
                lg[p.index(0 if d["gold"] == 1 else 1)] += boost
            else:
                p = perm if perm is not None else list(range(k))
                lg[p.index(d["gold"])] += boost
            lgs.append(torch.tensor(lg, dtype=torch.float32))
        prep = {"d": d, "variant": variant, "views": views, "seqs": [[1] * (50 + i % 40) for _ in views], "texts": [f"prompt {d['id']} {d['qid']} {v}" for v in range(len(views))], "row": row}
        probs = tt.Reader.decide(prep, lgs)
        rec = tt.result_record(prep, lgs, probs)
        if arm == "c1" and variant == "main" and i in (7, 1234):
            rec = tt.error_record(prep, "RuntimeError: synthetic failure")
        if arm == "c1" and variant == "main" and i == 55:
            rec["retried"] = True
        recs.append(rec)
    return recs

for arm, boost in (("c1", 2.2), ("base", 0.6)):
    with open(f"{R}/preds_{arm}.jsonl", "w") as f:
        for r in make(arm, boost): f.write(json.dumps(r) + "\n")
    with open(f"{R}/diag_{arm}.jsonl", "w") as f:
        for v in ("score_noprefix", "yn_swapped"):
            for r in make(arm, boost, v, only=True): f.write(json.dumps(r) + "\n")
    with open(f"{R}/lat_{arm}.jsonl", "w") as f:
        for j in range(60):
            f.write(json.dumps({"id": f"x{j}", "suite": "sst2", "nq": 1, "n_seq": 1, "n_tokens": 200, "prep_ms": 3 + j % 5, "fwd_ms": 20 + j, "total_ms": 25 + j * 1.5, "max_prob_diff_vs_batched": 0.001, "argmax_same_as_batched": True}) + "\n")
json.dump({"function_wall_s": 1000.0, "est_cost_usd_at_4.3_per_h": 1000 / 3600 * 4.30}, open(f"{R}/modal_done.json", "w"))
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
r = subprocess.run([PY, "-B", "-I", f"{TT}/harness/score_text.py", "--results", R], capture_output=True, text=True, env=env)
print(r.stdout[-5200:]); assert r.returncode == 0, r.stderr[-3000:]
sc = json.load(open(f"{R}/scores.json"))
assert sc["arms"]["c1"]["complete"] and sc["arms"]["c1"]["failed_total"] == 2 and sc["arms"]["c1"]["suites"]["sst2"]["n"] == 200
r = subprocess.run([PY, "-B", "-I", f"{TT}/harness/skeptic_rescore.py", "--results", R], capture_output=True, text=True, env=env)
print(r.stdout[-3500:]); assert r.returncode == 0, ("skeptic found mismatches", r.stdout[-2500:], r.stderr[-1500:])
print("SKEPTIC MATCHES ON CLEAN DATA")
# 1) a number changed in scores.json
s2 = json.load(open(f"{R}/scores.json")); s2["arms"]["c1"]["suites"]["ag_news"]["acc"] += 0.01
bak = open(f"{R}/scores.json").read(); json.dump(s2, open(f"{R}/scores.json", "w"))
r = subprocess.run([PY, "-B", "-I", f"{TT}/harness/skeptic_rescore.py", "--results", R], capture_output=True, text=True, env=env)
assert r.returncode == 1 and "ag_news: acc vs score_text" in r.stdout, r.stdout[-800:]
open(f"{R}/scores.json", "w").write(bak); print("caught: changed accuracy in scores.json")
# 2) a logit changed so an argmax flips (logged probs no longer follow from the logits)
lines = open(f"{R}/preds_base.jsonl").read().split("\n"); rec = json.loads(lines[3]); rec["view_logits"][0][0] += 25.0; lines[3] = json.dumps(rec)
open(f"{R}/preds_base.jsonl", "w").write("\n".join(lines))
r = subprocess.run([PY, "-B", "-I", f"{TT}/harness/skeptic_rescore.py", "--results", R], capture_output=True, text=True, env=env)
assert r.returncode == 1 and "recomputed probabilities equal logged" in r.stdout, r.stdout[-800:]
print("caught: tampered logit")
# 3) a decision dropped from the log
lines = open(f"{R}/preds_c1.jsonl").read().strip().split("\n"); open(f"{R}/preds_c1.jsonl", "w").write("\n".join(lines[:-1]) + "\n")
r = subprocess.run([PY, "-B", "-I", f"{TT}/harness/skeptic_rescore.py", "--results", R], capture_output=True, text=True, env=env)
assert r.returncode == 1, r.stdout[-800:]
print("caught: dropped decision")
print("SCORING SYNTHETIC TEST PASSED")
