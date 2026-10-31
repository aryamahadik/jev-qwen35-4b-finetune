"""W9 scratch diagnosis (never a gate): T15 choice c_card LR leak. In-memory build at a NON-binding diagnostic seed base."""
import sys, json, time, pickle
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2))
import numpy as np
from collections import defaultdict
from scipy import sparse
import gen_full_c2 as G
import pilot
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import MaxAbsScaler
N = int(sys.argv[1]); BASE = int(sys.argv[2]); OUT = Path(sys.argv[3]); OUT.mkdir(exist_ok=True, parents=True)
t0 = time.time()
fam = "T15"
src = G.quarantine_sources(fam); banned = set().union(*map(set, src.values()))
with G.loader_patch(fam):
    with G.PL.open_family(fam) as kit0:
        kit, xrep = G.apply_exclusions(kit0, banned)
        use_redraw = bool(xrep["dead_qforms"])
        rd = G.Redraw(kit.plugin, xrep["dead_qforms"]) if use_redraw else None
        try:
            b = G.pilot.build_pilot(kit, N, seed_base=BASE, run_g15=False)
        finally:
            if rd: rd.restore()
infos = b.infos
print("built", len(infos), round(time.time() - t0), flush=True)
pickle.dump([(i.row, i.question, i.context) for i in infos], open(OUT / "rows.pkl", "wb"))
ch = [i for i in infos if i.row["qtype"] == "choice"]

def run(sub, drop_prefix=(), only_dense=None, seeds=1):
    T, D, Y, Rw = pilot._pair_rows(sub, "c_card_without_question")
    T = [[t for t in tk if not t.startswith(drop_prefix)] for tk in T] if drop_prefix else T
    if only_dense is not None:
        D = [{k: v for k, v in d.items() if k in only_dense} for d in D]
    Y, Rw = np.array(Y), np.array(Rw)
    Xs = HashingVectorizer(n_features=2**18, analyzer=lambda x: x, alternate_sign=False, norm="l2").transform(T)
    Xd = DictVectorizer(sparse=False).fit_transform(D)
    groups_row = [i.row["meta"]["card_id"] for i in sub]
    groups = np.array([groups_row[ri] for ri in Rw])
    folds = pilot._folds(list(groups))
    sc = np.zeros(len(Y))
    for tr, te in folds:
        sca = MaxAbsScaler().fit(Xd[tr])
        Xtr = sparse.hstack([Xs[tr], sparse.csr_matrix(sca.transform(Xd[tr]))]).tocsr()
        Xte = sparse.hstack([Xs[te], sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()
        sc[te] = pilot._lr().fit(Xtr, Y[tr]).predict_proba(Xte)[:, 1]
    best = defaultdict(list)
    for s, ri, yy in zip(sc, Rw, Y): best[ri].append((s, yy))
    acc = np.zeros(len(sub))
    for ri, lst in best.items():
        m = max(s for s, _ in lst); top = [yy for s, yy in lst if s >= m - 1e-12]; acc[ri] = sum(top) / len(top)
    chance = np.mean([1.0 / len(i.row["options"]) for i in sub])
    return round(float(acc.mean()), 4), round(float(chance), 4), round(float(acc.mean() - chance) * 100, 2)

res = {}
for qf in ("ALL", "ch_outcome", "ch_claimant"):
    sub = ch if qf == "ALL" else [i for i in ch if i.row["meta"]["qform"] == qf]
    res[qf] = {"n": len(sub),
               "full": run(sub),
               "no_cross(x:)": run(sub, ("x:",)),
               "no_cross_no_ov": run(sub, ("x:", "ov:")),
               "no_option_tokens": run(sub, ("x:", "ov:", "o:", "o2:")),
               "dense_only_len": run(sub, ("x:", "ov:", "o:", "o2:"), {"k","tlen","clen","len_rank","is_longest","is_shortest","abstain","neg","verbatim","has_digit"})}
    print(qf, json.dumps(res[qf]), flush=True)
# per-class-of-gold coefficient inspection for the full model
for qf in ("ch_outcome", "ch_claimant"):
    sub = [i for i in ch if i.row["meta"]["qform"] == qf]
    T, D, Y, Rw = pilot._pair_rows(sub, "c_card_without_question")
    vocab = {}; rr, cc = [], []
    for ri, tk in enumerate(T):
        for t in set(tk):
            rr.append(ri); cc.append(vocab.setdefault(t, len(vocab)))
    X = sparse.csr_matrix((np.ones(len(rr)), (rr, cc)), shape=(len(T), len(vocab)))
    keep = np.where(np.asarray(X.sum(0)).ravel() >= 40)[0]
    inv = {j: t for t, j in vocab.items()}
    from sklearn.linear_model import LogisticRegression
    w = LogisticRegression(C=0.5, max_iter=500).fit(X[:, keep], np.array(Y)).coef_[0]
    o = np.argsort(-np.abs(w))[:30]
    res[qf]["top_coef"] = [(inv[keep[j]], round(float(w[j]), 2)) for j in o]
    print("COEF", qf, res[qf]["top_coef"], flush=True)
json.dump(res, open(OUT / "diag.json", "w"), indent=1)
print("done", round(time.time() - t0))
