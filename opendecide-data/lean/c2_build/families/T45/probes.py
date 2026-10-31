"""families/T45/probes.py: the A42-D 3.2 probes of T45, measured on an in-memory build (pilot.build_pilot infos).

  options_only(infos)     pilot G6 view (b) per head: a model sees only the option texts of a choice row (tokens, lengths,
                          ranks, kinds), 5-fold GroupKFold by card, LR and GBT.
  formatting_only(infos)  a model sees only FORMATTING of the state (register, line lengths, item counts, character
                          classes, command length) plus formatting of each option (length, rank, position, shape); no word
                          is read. Per head, LR and GBT, GroupKFold by card.
Bar (A42-D 3.2): accuracy within chance +/- 3 pp, two-sided, chance = the majority-class share of the probe's evaluation
split (never below the mean 1/k). Here the anchor label is shown in every row and the gold is uniform inside the shown
set, so the majority share equals the mean 1/k by construction; both are reported.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

import numpy as np

BAR_PP = 3.0


def _folds(groups, n=5):
    from sklearn.model_selection import GroupKFold
    g = np.array(groups)
    return list(GroupKFold(n_splits=min(n, len(set(groups)))).split(np.zeros(len(g)), groups=g))


def _lr():
    from sklearn.linear_model import LogisticRegression
    return LogisticRegression(C=1.0, max_iter=3000)


def _gbt():
    from sklearn.ensemble import HistGradientBoostingClassifier
    return HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def split_heads(infos):
    return {h: [i for i in infos if i.row["meta"]["qform"] == h] for h in ("ch_outcome", "ch_move")}


def majority_share(part) -> float:
    c = Counter(i.row["gold"] for i in part)
    return max(c.values()) / len(part)


def _verdict(acc, chance_1k, chance_maj):
    chance = max(chance_1k, chance_maj)
    d = 100 * (acc - chance)
    return {"acc": round(acc, 4), "chance": round(chance, 4), "chance_mean_1_over_k": round(chance_1k, 4),
            "chance_majority_share": round(chance_maj, 4), "delta_pp": round(d, 2), "pass": abs(d) <= BAR_PP}


def options_only(infos) -> dict:
    import pilot
    res = {}
    for h, part in split_heads(infos).items():
        if len(part) < 20:
            continue
        g = pilot.g6_choice(part)
        maj = majority_share(part)
        v = {m: _verdict(g["b_options"][m], g["chance"], maj) for m in ("lr", "gbt")}
        res[h] = {"n": len(part), **v, "pass": all(x["pass"] for x in v.values())}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res


def _shape(t: str) -> dict:
    return {"len": len(t), "digits": sum(c.isdigit() for c in t), "alpha": sum(c.isalpha() for c in t),
            "upper": sum(c.isupper() for c in t), "us": t.count("_")}


def state_formatting(row) -> dict:
    lines = row["state"].split("\n")
    d = {f"len_l{i}": float(len(x)) for i, x in enumerate(lines)}
    d.update({f"items_l{i}": float(x.count("=")) for i, x in enumerate(lines)})
    st = row["state"]
    d.update({"st_len": float(len(st)), "st_digits": float(sum(c.isdigit() for c in st)),
              "st_upper": float(sum(c.isupper() for c in st)), "st_dash": float(st.count("-")), "st_slash": float(st.count("/")),
              "st_dot": float(st.count(".")), "ins_len": float(len(row["instructions"])),
              "layout=" + str(row["meta"]["c2"]["register"]): 1.0})
    return d


def formatting_only(infos) -> dict:
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import MaxAbsScaler
    res = {}
    for h, part in split_heads(infos).items():
        if len(part) < 20:
            continue
        D, Y, R_, G_ = [], [], [], []
        for ri, i in enumerate(part):
            r = i.row
            opts = r["options"]
            lens = [len(o) for o in opts]
            order = sorted(range(len(opts)), key=lambda j: (lens[j], opts[j]))
            rank = {j: n for n, j in enumerate(order)}
            base = state_formatting(r)
            for j, o in enumerate(opts):
                D.append({**_shape(o), **base, "k": len(opts), "pos": j, "rank": rank[j],
                          "longest": float(lens[j] == max(lens)), "len_vs_mean": lens[j] - sum(lens) / len(lens)})
                Y.append(int(o == r["gold"]))
                R_.append(ri)
                G_.append(r["meta"]["card_id"])
        X = DictVectorizer(sparse=False).fit_transform(D)
        Y, R_ = np.array(Y), np.array(R_)
        folds = _folds(G_)
        sub = {}
        chance = float(np.mean([1 / len(i.row["options"]) for i in part]))
        maj = majority_share(part)
        for nm, mk in (("lr", _lr), ("gbt", _gbt)):
            sc = np.zeros(len(Y))
            for tr, te in folds:
                if len(set(Y[tr])) < 2:
                    continue
                Xtr, Xte = X[tr], X[te]
                if nm == "lr":
                    sca = MaxAbsScaler().fit(Xtr)
                    Xtr, Xte = sca.transform(Xtr), sca.transform(Xte)
                sc[te] = mk().fit(Xtr, Y[tr]).predict_proba(Xte)[:, 1]
            best = defaultdict(list)
            for s, ri, yy in zip(sc, R_, Y):
                best[ri].append((s, yy))
            acc = np.zeros(len(part))
            for ri, lst in best.items():
                m = max(s for s, _ in lst)
                top = [yy for s, yy in lst if s >= m - 1e-12]
                acc[ri] = sum(top) / len(top)
            sub[nm] = _verdict(float(acc.mean()), chance, maj)
        res[h] = {"n": len(part), **sub, "pass": all(v["pass"] for v in sub.values())}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res
