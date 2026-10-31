import sys, pickle
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
import numpy as np
from scipy import sparse
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import MaxAbsScaler
import pilot, pilot_loaders as PL
with PL.open_family("T36") as kit:
    b = pilot.build_pilot(kit, 6000, seed_base=3_000_000, run_g15=False)
ch = [i for i in b.infos if i.row["qtype"] == "choice"]
pickle.dump([(i.row["options"], i.row["gold"], i.context, i.question, i.row["meta"]["card_id"]) for i in ch],
            open("transfer/T36/_w5/diag_rows6000.pkl", "wb"))
chance = float(np.mean([1.0 / len(i.row["options"]) for i in ch]))
def run(view, tokfilter, dense_keep):
    T, D, Y, Rw = pilot._pair_rows(ch, view)
    Y, Rw = np.array(Y), np.array(Rw)
    T = [[t for t in tk if tokfilter(t)] for tk in T]
    Xs = HashingVectorizer(n_features=2 ** 18, analyzer=lambda x: x, alternate_sign=False, norm="l2").transform(T)
    D = [{k: v for k, v in d.items() if dense_keep(k)} for d in D]
    Xd = DictVectorizer(sparse=False).fit_transform(D) if D[0] else np.zeros((len(D), 1))
    groups = [ch[ri].row["meta"]["card_id"] for ri in Rw]
    folds = pilot._folds(list(groups))
    sc = np.zeros(len(Y))
    for tr, te in folds:
        sca = MaxAbsScaler().fit(Xd[tr])
        Xtr = sparse.hstack([Xs[tr], sparse.csr_matrix(sca.transform(Xd[tr]))]).tocsr()
        Xte = sparse.hstack([Xs[te], sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()
        sc[te] = pilot._lr().fit(Xtr, Y[tr]).predict_proba(Xte)[:, 1]
    best = {}
    for s, ri, yy in zip(sc, Rw, Y):
        best.setdefault(ri, []).append((s, yy))
    acc = []
    for ri, lst in best.items():
        m = max(s for s, _ in lst); top = [yy for s, yy in lst if s >= m - 1e-12]; acc.append(sum(top) / len(top))
    return round(float(np.mean(acc)), 4)
print("n", len(ch), "chance", round(chance, 4), "bar", round(chance + 0.02, 4), flush=True)
allk = lambda k: True
for view in ("c_card_without_question", "b_options"):
    for name, tf, dk in (("full", lambda t: True, allk), ("no_cross_x", lambda t: not t.startswith("x:"), allk),
                         ("only_cross_x", lambda t: t.startswith("x:"), allk), ("no_bigram_o2", lambda t: not t.startswith("o2:"), allk),
                         ("only_o_unigram", lambda t: t.startswith("o:"), lambda k: False),
                         ("no_dense", lambda t: True, lambda k: False), ("no_ov", lambda t: not t.startswith("ov:"), lambda k: k not in ("ov", "ov_n"))):
        print(view, name, run(view, tf, dk), flush=True)
