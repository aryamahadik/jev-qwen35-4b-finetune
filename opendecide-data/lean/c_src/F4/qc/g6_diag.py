"""G6 diagnostic (choice d_meta): per metadata feature, label-class association on CH-3 / CH-2 rows (chi-square),
numeric features binned in quartiles. Prints counts and p-values only."""
import json, sys
import numpy as np
from collections import Counter, defaultdict
from scipy.stats import chi2_contingency
import qc_lib as L
sys.path.insert(0, str(L.QC))
from g6 import meta_feats
NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
rows = L.load(NAME)
side = {json.loads(l)["id"]: json.loads(l) for l in open(L.OUT / f"{NAME}.sidecar.jsonl")}
for form in ("CH-3", "CH-2", "CH-claim"):
    rs = [r for r in rows if side[r["id"]]["form"] == form]
    lab = [side[r["id"]]["label_c"] if form != "CH-claim" else str(L.is_abstain(r["gold"])) for r in rs]
    feats = [meta_feats(r, side[r["id"]]) for r in rs]
    res = []
    keys = list(feats[0][0].keys()) + list(feats[0][1].keys())
    for k in keys:
        vals = [f[0].get(k, f[1].get(k)) for f in feats]
        if isinstance(vals[0], float):
            qs = np.quantile(vals, [0.25, 0.5, 0.75]); vals = [int(np.searchsorted(qs, v, side="right")) for v in vals]
        tab = defaultdict(Counter)
        for v, y in zip(vals, lab):
            tab[v][y] += 1
        ys = sorted(set(lab)); vs = [v for v in tab if sum(tab[v].values()) >= 5]
        if len(vs) < 2:
            continue
        M = np.array([[tab[v][y] for y in ys] for v in vs])
        M = M[:, M.sum(0) > 0]
        try:
            p = chi2_contingency(M)[1]
        except ValueError:
            continue
        res.append((p, k, len(vs)))
    res.sort()
    print(form, len(rs), Counter(lab))
    for p, k, nv in res[:8]:
        print(f"   {k:12s} levels={nv:3d} p={p:.2e}")
