"""T27 diagnostic (not a gate): the pilot's choice-G6 pointwise LR trained on one dump and tested on a fresh one."""
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import numpy as np
import scipy.sparse as sp
import pilot
from collections import defaultdict
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MaxAbsScaler
def load(p):
    rows = [json.loads(l) for l in open(p)]
    out = []
    for r in rows:
        if r["qtype"] != "choice":
            continue
        rules, _, q = r["instructions"].rpartition("\n\n")
        ctx = "\n".join(x for x in (r.get("card") or "", rules, r["state"]) if x.strip())
        out.append(pilot.RowInfo(r, None, None, 0, q, ctx, None))
    return out
A, B = load(sys.argv[1]), load(sys.argv[2])
for view in ("a_question", "b_options", "c_card_without_question", "d_meta"):
    TA, DA, YA, RA = pilot._pair_rows(A, view)
    TB, DB, YB, RB = pilot._pair_rows(B, view)
    YA, YB, RB = np.array(YA), np.array(YB), np.array(RB)
    hv = HashingVectorizer(n_features=2 ** 18, analyzer=lambda x: x, alternate_sign=False, norm="l2")
    dv = DictVectorizer(sparse=False).fit(DA + DB)
    XdA, XdB = dv.transform(DA), dv.transform(DB)
    scl = MaxAbsScaler().fit(XdA)
    XA = sp.hstack([hv.transform(TA), sp.csr_matrix(scl.transform(XdA))]).tocsr()
    XB = sp.hstack([hv.transform(TB), sp.csr_matrix(scl.transform(XdB))]).tocsr()
    s = LogisticRegression(C=1.0, max_iter=3000, solver="liblinear").fit(XA, YA).predict_proba(XB)[:, 1]
    best = defaultdict(list)
    for sc, ri, yy in zip(s, RB, YB):
        best[ri].append((sc, yy))
    accs = []
    for l in best.values():
        m = max(x for x, _ in l)
        top = [yy for x, yy in l if x >= m - 1e-12]
        accs.append(sum(top) / len(top))
    print(view, "lr train->test acc", round(float(np.mean(accs)), 4), "n_test", len(best), flush=True)
