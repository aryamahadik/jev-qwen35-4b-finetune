import pickle, sys, numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
import pilot
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction import DictVectorizer
d = pickle.loads(open("pilot_i2/_dmeta_i1.pkl", "rb").read())
ch = d["ch"]
q = np.array(ch["qform"])
for form in ("ch_status", "ch_due"):
    idx = [i for i, x in enumerate(ch["qform"]) if x == form]
    feats = [ch["feats"][i] for i in idx]
    gold = [str(ch["gold"][i]) for i in idx]
    groups = [ch["groups"][i] for i in idx]
    if form == "ch_due":     # gold is a date; use its rank among the row's three options instead
        pr = ch["pairs"]
        rk = {}
        # rebuild per-row rank of the gold date from the pair rows (rows in order; Y marks gold, D has len_rank)
        pass
    print(form, len(idx), "gold dist", {g: gold.count(g) for g in sorted(set(gold))} if form == "ch_status" else "")
    if form == "ch_status":
        y = np.array(gold)
        X = DictVectorizer(sparse=False).fit_transform([f["num"] for f in feats])
        folds = pilot._folds(groups)
        pred = np.empty(len(y), dtype=object)
        for tr, te in folds:
            m = GradientBoostingClassifier(n_estimators=60, max_depth=3, random_state=0).fit(X[tr], y[tr])
            pred[te] = m.predict(X[te])
        print(" status-from-numerics CV acc", float((pred == y).mean()), "majority", max(gold.count(g) for g in set(gold)) / len(y))
        names = sorted(feats[0]["num"])
        for k in names:
            xs = np.array([f["num"][k] for f in feats])
            print("  ", k, {g: round(float(xs[y == g].mean()), 2) for g in sorted(set(gold))})
# ch_due: gold position among options and sorted rank from pair rows
pr = ch["pairs"]
Y = np.array(pr["Y"]); Rw = np.array(pr["Rw"])
pos, k_of = {}, {}
for j, (yy, ri) in enumerate(zip(Y, Rw)):
    k_of[ri] = k_of.get(ri, 0) + 1
    if yy:
        pos[ri] = k_of[ri] - 1
for form in ("ch_status", "ch_due"):
    idx = [i for i, x in enumerate(ch["qform"]) if x == form]
    p = [pos[i] for i in idx if i in pos]
    print(form, "gold position counts", np.bincount(p), "n", len(p))
lr = {}
for j, (dn, yy, ri) in enumerate(zip(pr["D"], Y, Rw)):
    if yy:
        lr[ri] = (dn["len_rank"], dn["clen"], dn["abstain"])
for form in ("ch_status", "ch_due"):
    idx = [i for i, x in enumerate(ch["qform"]) if x == form]
    v = [lr[i] for i in idx if i in lr]
    print(form, "gold len_rank counts", {r: sum(1 for a in v if a[0] == r) for r in sorted({a[0] for a in v})})
