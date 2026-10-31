"""T01 scratch: what does the options-only LR use? Build ~5,000 rows, per-qform CV of b_options LR + top coefficients."""
import sys, collections
sys.path.insert(0, '.')
import numpy as np
import pilot, pilot_loaders as PL
from scipy import sparse
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import MaxAbsScaler
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
with PL.open_family("T01") as kit:
    b = pilot.build_pilot(kit, n, run_g15=False, log=lambda m: None)
    infos = b.infos
    ch = [i for i in infos if i.row["qtype"] == "choice"]
    print("choice rows", len(ch), collections.Counter(i.row["meta"]["qform"] for i in ch), flush=True)
    for view in ("b_options",):
        T, D, Y, Rw = pilot._pair_rows(ch, view)
        Y, Rw = np.array(Y), np.array(Rw)
        # keep token vocabulary visible: use CountVectorizer-like mapping via DictVectorizer on token multiset
        dv = DictVectorizer()
        Xt = dv.fit_transform([{t: 1 for t in tk} for tk in T])
        names_t = dv.feature_names_
        dd = DictVectorizer(sparse=False)
        Xd = dd.fit_transform(D)
        names_d = dd.feature_names_
        sca = MaxAbsScaler().fit(Xd)
        X = sparse.hstack([Xt, sparse.csr_matrix(sca.transform(Xd))]).tocsr()
        names = names_t + names_d
        groups = np.array([ch[ri].row["meta"]["card_id"] for ri in Rw])
        folds = pilot._folds(list(groups))
        sc = np.zeros(len(Y))
        for tr, te in folds:
            sc[te] = pilot._lr().fit(X[tr], Y[tr]).predict_proba(X[te])[:, 1]
        # accuracy per qform
        per = collections.defaultdict(list)
        best = collections.defaultdict(list)
        for s, ri, yy in zip(sc, Rw, Y):
            best[ri].append((s, yy))
        for ri, lst in best.items():
            m = max(s for s, _ in lst)
            top = [yy for s, yy in lst if s >= m - 1e-12]
            per[ch[ri].row["meta"]["qform"]].append((sum(top) / len(top), 1 / len(lst)))
        tot = [a for v in per.values() for a, _ in v]
        tch = [c for v in per.values() for _, c in v]
        print("overall acc %.4f chance %.4f" % (np.mean(tot), np.mean(tch)))
        for q, v in sorted(per.items()):
            print("  %-15s n=%4d acc %.3f chance %.3f  diff %+.3f" % (q, len(v), np.mean([a for a, _ in v]), np.mean([c for _, c in v]),
                                                                  np.mean([a - c for a, c in v])))
        m = pilot._lr().fit(X, Y)
        coef = m.coef_[0]
        freq = np.asarray((X != 0).sum(axis=0)).ravel()
        order = np.argsort(-np.abs(coef) * np.sqrt(freq))[:25]
        print("top coefficients (|coef| x sqrt(freq)):")
        for j in order:
            print("   %-40s coef %+.3f freq %d" % (names[j][:40], coef[j], freq[j]))
