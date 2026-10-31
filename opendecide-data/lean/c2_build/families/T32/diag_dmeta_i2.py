"""families/T32/diag_dmeta_i2.py: which pilot.meta_features drive the G6 d_meta view (fix iteration 2, item 1).

  dump    in-memory build of N rows (G15 off, nothing written to pilot/), saves the d_meta inputs to a pickle
  rank    univariate association (yes/no: accuracy of one feature (+qform) under the G6 CV; mutual information with the
          gold; choice: per option score) and GBT permutation importance on the pickle
  python -B families/T32/diag_dmeta_i2.py dump --n 6000 --out <pkl> ; python -B ... rank --pkl <pkl>   (from lean/c2_build)
"""
from __future__ import annotations

import argparse
import json
import pickle
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))


def dump(n: int, out: str) -> None:
    import pilot
    import pilot_loaders as PL
    with PL.open_family("T32") as kit:
        b = pilot.build_pilot(kit, n, run_g15=False)
        yn = [i for i in b.infos if i.row["qtype"] == "noul"]
        ch = [i for i in b.infos if i.row["qtype"] == "choice"]
        d = {"n": len(b.infos),
             "yn": {"feats": [dict(zip(("cat", "num"), pilot.meta_features(i))) for i in yn],
                    "y": [int(i.row["gold"]) for i in yn], "groups": [i.row["meta"]["card_id"] for i in yn],
                    "status": [kit.plugin._fold(i.spec)[0] for i in yn]},
             "ch": {"feats": [dict(zip(("cat", "num"), pilot.meta_features(i))) for i in ch],
                    "gold": [i.row["gold"] for i in ch], "groups": [i.row["meta"]["card_id"] for i in ch],
                    "qform": [i.row["meta"].get("qform") for i in ch]}}
        for view in ("d_meta",):
            T, D, Y, Rw = pilot._pair_rows(ch, view)
            d["ch"]["pairs"] = {"T": T, "D": D, "Y": Y, "Rw": Rw}
    Path(out).write_bytes(pickle.dumps(d))
    print("saved", out, d["n"], len(yn), len(ch))


def rank(pkl: str) -> None:
    import numpy as np
    import pilot
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.feature_selection import mutual_info_classif
    from scipy import sparse
    d = pickle.loads(Path(pkl).read_bytes())
    yn = d["yn"]
    y = np.array(yn["y"])
    folds = pilot._folds(yn["groups"])
    feats = yn["feats"]
    names = [("cat", k) for k in feats[0]["cat"]] + [("num", k) for k in feats[0]["num"]]
    res = []
    for kind, k in names:
        dv = [{k: f[kind][k]} for f in feats]
        Xd = DictVectorizer(sparse=False).fit_transform(dv)
        acc = pilot._cv_binary(sparse.csr_matrix(Xd), Xd, y, folds)
        # rate spread: for cat features, max |P(yes | level) - 0.5| over levels with >= 30 rows
        spread = None
        if kind == "cat":
            lv = {}
            for f, yy in zip(feats, y):
                lv.setdefault(f[kind][k], []).append(yy)
            sp = [(abs(np.mean(v) - 0.5), key, len(v)) for key, v in lv.items() if len(v) >= 30]
            spread = max(sp) if sp else None
        else:
            xs = np.array([f[kind][k] for f in feats])
            spread = float(np.corrcoef(xs, y)[0, 1]) if xs.std() > 0 else 0.0
        res.append({"feature": k, "acc_1feat": max(acc.values()), "lr": acc["lr"], "gbt": acc["gbt"], "assoc": spread})
    res.sort(key=lambda r: -r["acc_1feat"])
    print("YES/NO single-feature CV accuracy (chance .5, n=%d)" % len(y))
    for r in res:
        print(" ", r["feature"], r["lr"], r["gbt"], r["assoc"])
    # permutation importance of the full gbt on a held-out fold split
    from sklearn.inspection import permutation_importance
    Xd_all = DictVectorizer(sparse=False)
    X = Xd_all.fit_transform([{**f["cat"], **f["num"]} for f in feats])
    tr, te = folds[0]
    m = pilot._gbt().fit(X[tr], y[tr])
    pi = permutation_importance(m, X[te], y[te], n_repeats=5, random_state=0)
    order = np.argsort(-pi.importances_mean)[:15]
    print("YES/NO permutation importance, fold 0 (acc %.4f)" % m.score(X[te], y[te]))
    for j in order:
        print("  ", Xd_all.get_feature_names_out()[j], round(float(pi.importances_mean[j]), 4))
    # per level yes rate of the strongest numeric features
    for k in ("depth", "len_state", "n_lines", "n_numbers", "len_q", "len_card", "len_ins", "mag_max"):
        xs = np.array([f["num"][k] for f in feats])
        qs = np.quantile(xs, [0.2, 0.4, 0.6, 0.8])
        bins = np.digitize(xs, qs)
        print("  yes rate by quintile of", k, [round(float(y[bins == b].mean()), 3) for b in range(5)])
    # choice: gold status share against the metadata
    ch = d["ch"]
    pr = ch["pairs"]
    Y = np.array(pr["Y"])
    Dm = DictVectorizer(sparse=False).fit_transform(pr["D"])
    Dn = DictVectorizer(sparse=False)
    Dn.fit(pr["D"])
    mg = pilot._gbt().fit(Dm, Y)
    pim = permutation_importance(mg, Dm, Y, n_repeats=3, random_state=0)
    order = np.argsort(-pim.importances_mean)[:15]
    print("CHOICE pairwise gbt permutation importance (in-sample, ranking only)")
    for j in order:
        print("  ", Dn.get_feature_names_out()[j], round(float(pim.importances_mean[j]), 4))
    # per-row choice: accuracy of the d_meta features with one numeric feature at a time (row-level majority class)
    print("CHOICE gold position / k / qform mix:", {q: ch["qform"].count(q) for q in set(ch["qform"])})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("dump", "rank"))
    ap.add_argument("--n", type=int, default=6000)
    ap.add_argument("--out", default="")
    ap.add_argument("--pkl", default="")
    a = ap.parse_args()
    dump(a.n, a.out) if a.cmd == "dump" else rank(a.pkl)
