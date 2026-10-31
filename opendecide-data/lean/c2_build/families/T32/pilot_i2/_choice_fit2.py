import pickle, sys, numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
import pilot
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction import DictVectorizer
d = pickle.loads(open("families/T32/pilot_i2/_dmeta_i1.pkl", "rb").read())
ch = d["ch"]
idx = [i for i, x in enumerate(ch["qform"]) if x == "ch_status"]
feats = [ch["feats"][i] for i in idx]
y = np.array([str(ch["gold"][i]) for i in idx])
groups = [ch["groups"][i] for i in idx]
folds = pilot._folds(groups)
names = [k for k in sorted(feats[0]["num"]) if k not in ("k", "len_card", "mag_max")]
def cv(cols):
    X = np.array([[f["num"][k] for k in cols] for f in feats], float)
    pred = np.empty(len(y), dtype=object)
    for tr, te in folds:
        m = GradientBoostingClassifier(n_estimators=40, max_depth=3, random_state=0).fit(X[tr], y[tr])
        pred[te] = m.predict(X[te])
    return round(float((pred == y).mean()), 4)
print("all", cv(names))
for k in names:
    print(k, "alone", cv([k]), "without", cv([n for n in names if n != k]))
