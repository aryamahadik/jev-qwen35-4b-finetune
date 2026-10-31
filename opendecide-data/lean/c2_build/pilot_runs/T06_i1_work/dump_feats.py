"""Build N rows in memory (T06 current generator, pilot seeds) and dump the yes/no rows' model-visible metadata, the
hidden facts and the gold to JSON for offline analysis; also print pilot.meta_drivers. Scratch (not part of the family)."""
import sys, json, importlib
from pathlib import Path
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
import numpy as np
import pilot
from families.T06 import plugin as T
rp = importlib.import_module('families.T06.run_pilot')
N = int(sys.argv[1]); out = sys.argv[2]
with rp._t06() as kit:
    b = pilot.build_pilot(kit, N, run_g15=False)
rows = []
for i in b.infos:
    c, n = pilot.meta_features(i)
    f = T.facts(i.spec)
    rows.append({"qtype": i.row["qtype"], "qform": i.row["meta"]["qform"], "gold": i.row["gold"] if i.row["qtype"] == "noul" else None,
                 "card": i.row["meta"]["card_id"], "cat": c, "num": n, "policy": f.policy, "goods": f.goods, "reason": f.reason,
                 "handover": f.handover, "seal": f.seal, "counts": bool(i.spec.structure["counts"]),
                 "p": f.p, "n_rej": f.n_rej, "n_wd": f.n_wd, "sampler": i.spec.sampler,
                 "refund": bool(T._grants(f)), "grants": sorted(T._grants(f)), "role": getattr(i, "role", None)})
Path(out).write_text(json.dumps(rows))
yn = [i for i in b.infos if i.row["qtype"] == "noul"]
y = np.array([int(i.row["gold"]) for i in yn])
folds = pilot._folds([i.row["meta"]["card_id"] for i in yn])
print("n", len(yn), "yes", y.mean())
for d in pilot.meta_drivers(yn, y, folds, top=12):
    print(d)
