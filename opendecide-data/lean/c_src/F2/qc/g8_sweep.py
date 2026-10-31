"""G8 sensitivity (report only): grouped-by-card AFLite-lite at several L2 strengths C, real labels vs the
permuted-label control (seed 4242), to separate model-stability floor from real cues. Usage: g8_sweep.py <name>"""
import json, sys, random
import numpy as np
import qc_lib as L
import g8
NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME)
D = np.load(L.QC / f"tmp/g8_emb_{NAME}.npz"); Z = D["rowemb"].astype(np.float32); OI = D["opt_idx"]; OV = D["opt_vec"]
rng = random.Random(4242); perm = [dict(r) for r in rows]; byc = {}
for i, r in enumerate(perm):
    if L.is_yn(r):
        byc.setdefault(r["meta"]["card_id"], []).append(i)
    else:
        r["gold"] = r["options"][rng.randrange(len(r["options"]))]
for idx in byc.values():
    gl = [perm[i]["gold"] for i in idx]; rng.shuffle(gl)
    for i, v in zip(idx, gl):
        perm[i]["gold"] = v
from sklearn import linear_model
orig = linear_model.LogisticRegression
out = {}
for C in (0.01, 0.05, 0.2):
    linear_model.LogisticRegression = lambda C=1.0, **kw: orig(C=C_sweep, **kw)
    C_sweep = C
    real = g8.aflite(rows, Z, OI, OV, True); ctrl = g8.aflite(perm, Z, OI, OV, True)
    out[str(C)] = {"real": {k: real[k] for k in ("predictable_share", "yes_no_share", "choice_share", "by_sampler_qtype")},
                   "control": {k: ctrl[k] for k in ("predictable_share", "yes_no_share", "choice_share")}}
    g8.log(f"C={C} real {real['predictable_share']:.4f} control {ctrl['predictable_share']:.4f}")
    (L.QC / f"g8_sweep_{NAME}.json").write_text(json.dumps(out, indent=1))
g8.log("done")
