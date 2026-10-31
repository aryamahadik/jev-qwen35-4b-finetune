"""Dev tool (A44 d, fix iteration 3): rank the drivers of T35's choice d_meta view on an in-memory build.

  cd lean/c2_build
  ../../.venv/bin/python -B families/T35/dev_tools/i3_choice_drivers.py build 6000 <features.pkl>   # build + features
  ../../.venv/bin/python -B families/T35/dev_tools/i3_choice_drivers.py rank <features.pkl> [out.json]

build: runs run_pilot_i3's loader and pilot.build_pilot in memory (nothing under pilot_i3 is written), keeps the d_meta pointwise
features of the choice rows (pilot._pair_rows) plus the planned gold position. rank: 5-fold GroupKFold (by card) GBT on those
features; the drivers are (1) permutation importance (accuracy lost when one feature is shuffled inside the test fold), (2) the
standardised gold-vs-wrong gap of each option feature, (3) the row-level gap between gold-is-"no line" rows and line rows.
"""
import json
import pickle
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[2]))


def build(n, out):
    import pilot as PI
    import pilot_loaders as PL
    import run_pilot_i3 as R
    R.install_loader()
    with PL.open_family("T35") as kit:
        b = PI.build_pilot(kit, n, run_g15=False)
    ch = [i for i in b.infos if i.row["qtype"] == "choice"]
    T, D, Y, Rw = PI._pair_rows(ch, "d_meta")
    cards = [i.row["meta"]["card_id"] for i in ch]
    gold_pos = [i.row["options"].index(i.row["gold"]) for i in ch]
    ks = [len(i.row["options"]) for i in ch]
    abst = [int("kind:abstain" in PI.option_kinds(i)[i.row["options"].index(i.row["gold"])]) for i in ch]
    pickle.dump({"D": D, "Y": Y, "Rw": Rw, "cards": cards, "gold_pos": gold_pos, "k": ks, "abstain": abst,
                 "n_rows": len(b.infos)}, open(out, "wb"))
    print(f"built {len(b.infos)} rows, {len(ch)} choice rows")


def rank(path, out=None):
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.model_selection import GroupKFold
    d = pickle.load(open(path, "rb"))
    dv = DictVectorizer(sparse=False)
    X = dv.fit_transform(d["D"])
    names = list(dv.get_feature_names_out())
    Y, Rw = np.array(d["Y"]), np.array(d["Rw"])
    groups = np.array([d["cards"][r] for r in Rw])
    nrow = len(d["cards"])
    chance = float(np.mean([1 / k for k in d["k"]]))
    rng = np.random.RandomState(0)

    def row_acc(rows_idx, prob):
        hit, tot = 0, 0
        for r in np.unique(Rw[rows_idx]):
            m = Rw[rows_idx] == r
            j = np.argmax(prob[m])
            hit += int(Y[rows_idx][m][j] == 1)
            tot += 1
        return hit, tot

    base_hit = base_tot = 0
    loss = {n: 0 for n in names}
    for tr, te in GroupKFold(5).split(X, Y, groups):
        m = GradientBoostingClassifier(random_state=0).fit(X[tr], Y[tr])
        p = m.predict_proba(X[te])[:, 1]
        h, t = row_acc(te, p)
        base_hit, base_tot = base_hit + h, base_tot + t
        for j, nm in enumerate(names):
            Xp = X[te].copy()
            Xp[:, j] = rng.permutation(Xp[:, j])
            h2, _ = row_acc(te, m.predict_proba(Xp)[:, 1])
            loss[nm] += h - h2
    acc = base_hit / base_tot
    perm = sorted(((v / base_tot, k) for k, v in loss.items()), reverse=True)
    gold = Y == 1
    opt_gap = {}
    for j, nm in enumerate(names):
        a, b = X[gold & (X[:, names.index("abstain")] == 0), j], X[(~gold) & (X[:, names.index("abstain")] == 0), j]
        sd = X[:, j].std() or 1.0
        opt_gap[nm] = round(float((a.mean() - b.mean()) / sd), 3) if len(a) and len(b) else 0.0
    ab = np.array(d["abstain"]) == 1
    first = {}
    for r, rr in enumerate(Rw):
        first.setdefault(rr, r)
    idx = np.array([first[r] for r in range(nrow)])
    row_gap = {}
    for j, nm in enumerate(names):
        col = X[idx, j]
        sd = col.std() or 1.0
        row_gap[nm] = round(float((col[ab].mean() - col[~ab].mean()) / sd), 3)
    gp = np.array(d["gold_pos"])
    ks = np.array(d["k"])
    res = {"n_rows_total": d["n_rows"], "n_choice": nrow, "chance": round(chance, 4), "gbt_acc": round(acc, 4),
           "permutation_importance_top": [(round(v, 4), k) for v, k in perm[:12]],
           "option_gap_gold_vs_wrong_top": sorted(opt_gap.items(), key=lambda kv: -abs(kv[1]))[:10],
           "row_gap_abstain_gold_vs_line_gold_top": sorted(row_gap.items(), key=lambda kv: -abs(kv[1]))[:12],
           "gold_pos_by_k": {int(k): np.bincount(gp[ks == k], minlength=int(k)).tolist() for k in np.unique(ks)}}
    print(json.dumps(res, indent=1))
    if out:
        Path(out).write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build(int(sys.argv[2]), sys.argv[3])
    else:
        rank(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
