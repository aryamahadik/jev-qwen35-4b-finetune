"""W9 scratch (never a gate): ablate context tokens of the T15 c_card LR on a saved 12,000-row diagnostic build."""
import sys, json, pickle, re, time
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]; sys.path.insert(0, str(C2))
import numpy as np
from collections import defaultdict
from scipy import sparse
import pilot
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import MaxAbsScaler
rows = pickle.load(open(sys.argv[1], "rb")); OUT = Path(sys.argv[2])
base = [SimpleNamespace(row=r, question=q, context=c) for r, q, c in rows if r["qtype"] == "choice"]
def run(sub):
    T, D, Y, Rw = pilot._pair_rows(sub, "c_card_without_question")
    Y, Rw = np.array(Y), np.array(Rw)
    Xs = HashingVectorizer(n_features=2**18, analyzer=lambda x: x, alternate_sign=False, norm="l2").transform(T)
    Xd = DictVectorizer(sparse=False).fit_transform(D)
    gr = [i.row["meta"]["card_id"] for i in sub]; groups = np.array([gr[ri] for ri in Rw])
    folds = pilot._folds(list(groups)); sc = np.zeros(len(Y))
    for tr, te in folds:
        sca = MaxAbsScaler().fit(Xd[tr])
        Xtr = sparse.hstack([Xs[tr], sparse.csr_matrix(sca.transform(Xd[tr]))]).tocsr()
        Xte = sparse.hstack([Xs[te], sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()
        sc[te] = pilot._lr().fit(Xtr, Y[tr]).predict_proba(Xte)[:, 1]
    best = defaultdict(list)
    for s, ri, yy in zip(sc, Rw, Y): best[ri].append((s, yy))
    acc = np.zeros(len(sub))
    for ri, l in best.items():
        m = max(s for s, _ in l); top = [yy for s, yy in l if s >= m - 1e-12]; acc[ri] = sum(top) / len(top)
    ch = np.mean([1.0 / len(i.row["options"]) for i in sub])
    return round(float((acc.mean() - ch) * 100), 2)
V = {"full": lambda c: c,
     "no_cents": lambda c: re.sub(r"\.\d\d\b", "", c),
     "no_digits": lambda c: re.sub(r"\d+", "", c),
     "no_facts_block_numbers": lambda c: c,   # placeholder replaced below
     "cents_only_00_01_99": lambda c: re.sub(r"\.(00|01|99)\b", "", c)}
res = {}
for qf in ("ch_outcome", "ch_claimant"):
    sub0 = [i for i in base if i.row["meta"]["qform"] == qf]
    for nm, fn in V.items():
        if nm == "no_facts_block_numbers": continue
        sub = [SimpleNamespace(row=i.row, question=i.question, context=fn(i.context)) for i in sub0]
        res[f"{qf}/{nm}"] = run(sub); print(qf, nm, res[f"{qf}/{nm}"], flush=True)
json.dump(res, open(OUT / "ablate.json", "w"), indent=1)
