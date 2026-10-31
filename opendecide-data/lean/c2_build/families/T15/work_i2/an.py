"""Scratch analysis (never a gate): in-memory 6,000-row T15 build, G6 split by question form, c-view cue search."""
import sys, pickle, time, json, os
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
import pilot, pilot_loaders as PL
N = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
cache = os.environ.get("TMPDIR", "/tmp") + f"/t15_infos_{N}.pkl"
t0 = time.time()
with PL.open_family("T15") as kit:
    b = pilot.build_pilot(kit, N, run_g15=False)
infos = b.infos
print("built", len(infos), round(time.time() - t0), flush=True)
ch = [i for i in infos if i.row["qtype"] == "choice"]
deep = sum(bool(i.row["meta"].get("deep")) for i in infos) / len(infos)
print("deep share rows", round(deep, 4))
for qf in ("ch_outcome", "ch_claimant"):
    sub = [i for i in ch if i.row["meta"]["qform"] == qf]
    r = pilot.g6_choice(sub)
    print(qf, r["n"], r["chance"], {v: r[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")}, flush=True)
r = pilot.g6_choice(ch)
print("choice all", r["n"], r["chance"], {v: r[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")}, flush=True)
g = pilot.g6(infos)
print("G6", g["verdict"], g["fails"])

# ---- cue search: fit the c view (and d_meta gbt) on all choice rows, per question form
import numpy as np
from scipy import sparse
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance
for qf in ("ch_outcome", "ch_claimant"):
    sub = [i for i in ch if i.row["meta"]["qform"] == qf]
    T, D, Y, Rw = pilot._pair_rows(sub, "c_card_without_question")
    vocab = {}; rows_, cols_ = [], []
    for ri, tk in enumerate(T):
        for t in set(tk):
            rows_.append(ri); cols_.append(vocab.setdefault(t, len(vocab)))
    X = sparse.csr_matrix((np.ones(len(rows_)), (rows_, cols_)), shape=(len(T), len(vocab)))
    keep = np.where(np.asarray(X.sum(0)).ravel() >= 30)[0]
    inv = {j: t for t, j in vocab.items()}
    names = [inv[j] for j in keep]
    w = LogisticRegression(C=1.0, max_iter=300).fit(X[:, keep], np.array(Y)).coef_[0]
    o = np.argsort(-np.abs(w))[:14]
    print("CUE c", qf, [(names[j], round(float(w[j]), 2)) for j in o], flush=True)
    T, D, Y, Rw = pilot._pair_rows(sub, "d_meta")
    dv = DictVectorizer(sparse=False); Xd = dv.fit_transform(D)
    g_ = HistGradientBoostingClassifier(max_iter=60, max_depth=3, random_state=0).fit(Xd, np.array(Y))
    pi = permutation_importance(g_, Xd, np.array(Y), n_repeats=2, random_state=0, scoring="roc_auc")
    o = np.argsort(-pi.importances_mean)[:8]
    print("CUE d", qf, [(dv.feature_names_[j], round(float(pi.importances_mean[j]), 4)) for j in o], flush=True)
