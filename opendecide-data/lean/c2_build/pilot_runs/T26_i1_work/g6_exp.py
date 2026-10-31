import sys, pickle, collections
from pathlib import Path
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import pilot
from sklearn.feature_extraction import DictVectorizer
P = pickle.load(open(sys.argv[1] if len(sys.argv) > 1 else "g6_pairs.pkl", "rb"))
D, Y, Rw, groups, qf = P["D"], np.array(P["Y"]), np.array(P["Rw"]), P["groups"], P["qf"]
nrow = len(qf)
folds = pilot._folds(list(groups))
OPT = ["k", "tlen", "clen", "len_rank", "is_longest", "is_shortest", "abstain", "neg", "verbatim", "has_digit"]
META = sorted({k for d in D for k in d} - set(OPT))
def acc(keep, rows=None):
    Dd = [{k: v for k, v in d.items() if k in keep} for d in D]
    X = DictVectorizer(sparse=False).fit_transform(Dd)
    sc = np.zeros(len(Y))
    for tr, te in folds:
        sc[te] = pilot._gbt().fit(X[tr], Y[tr]).predict_proba(X[te])[:, 1]
    best = collections.defaultdict(list)
    for s, ri, yy in zip(sc, Rw, Y):
        best[ri].append((s, yy))
    a = np.zeros(nrow)
    for ri, l in best.items():
        m = max(s for s, _ in l); t = [yy for s, yy in l if s >= m - 1e-12]; a[ri] = sum(t) / len(t)
    return a
chance = np.zeros(nrow)
cnt = collections.Counter(Rw)
for ri in range(nrow): chance[ri] = 1 / cnt[ri]
print("chance", chance.mean().round(4))
a = acc(OPT + META); print("all", a.mean().round(4))
a0 = acc(OPT); print("opt only", a0.mean().round(4))
for qfm in set(qf):
    idx = [i for i in range(nrow) if qf[i] == qfm]
    print(qfm, len(idx), "all", a[idx].mean().round(4), "chance", chance[idx].mean().round(4), "opt", a0[idx].mean().round(4))
for m in META:
    print("opt+", m, acc(OPT + [m]).mean().round(4))
