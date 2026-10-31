"""T01 scratch: what does the yes/no context-only LR use? Per-kind CV accuracy and the top n-gram coefficients."""
import sys, collections
sys.path.insert(0, '.')
import numpy as np
import pilot, pilot_loaders as PL
from sklearn.feature_extraction.text import TfidfVectorizer
n = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
with PL.open_family("T01") as kit:
    b = pilot.build_pilot(kit, n, run_g15=False, log=lambda m: None)
    yn = [i for i in b.infos if i.row["qtype"] == "noul"]
    y = np.array([int(i.row["gold"]) for i in yn])
    print("yes/no rows", len(yn), "yes rate %.3f" % y.mean(), flush=True)
    folds = pilot._folds([i.row["meta"]["card_id"] for i in yn])
    for view, tx in (("context", [i.context for i in yn]), ("question", [i.question for i in yn])):
        vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, token_pattern=r"[A-Za-z0-9'-]+")
        X = vec.fit_transform(tx).tocsr()
        pred = np.zeros(len(y))
        for tr, te in folds:
            pred[te] = pilot._lr().fit(X[tr], y[tr]).predict(X[te])
        print(view, "LR acc %.4f" % (pred == y).mean())
        kinds = collections.defaultdict(list)
        for p, yy, i in zip(pred, y, yn):
            kinds[i.row["meta"]["qform"]].append(p == yy)
        for q, v in sorted(kinds.items()):
            print("   %-18s n=%4d acc %.3f" % (q, len(v), np.mean(v)))
        if view == "context":
            m = pilot._lr().fit(X, y)
            names = np.array(vec.get_feature_names_out())
            order = np.argsort(-np.abs(m.coef_[0]))[:25]
            for j in order:
                df = int((X[:, j] != 0).sum())
                print("   %-34s coef %+.3f docs %d  yes-rate-when-present %.3f" % (names[j], m.coef_[0][j], df, y[X[:, j].nonzero()[0]].mean()))
