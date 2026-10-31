"""families/T46/probes.py: the A42-D 3.2 probes of T46, measured on an in-memory build (pilot.build_pilot infos).

  options_only(infos)     pilot G6 view (b) on the choice rows: a model sees only the option texts (tokens, lengths, ranks,
                          kinds), 5-fold GroupKFold by card, LR and GBT.
  formatting_only(infos)  a model sees only FORMATTING: the state's layout, line lengths, field counts, character classes and
                          the length of the instructions; for choice rows also each option's shape (length, rank, position);
                          for yes/no rows the length of the proposed label. No word is read. LR and GBT, GroupKFold by card.
Bar (A42-D 3.2): accuracy within chance +-3 pp, two-sided; chance = max(mean 1/k, the majority-class share) for choice rows
and max(.5, the majority share) for yes/no rows.
"""
from __future__ import annotations

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


def _verdict(acc, chance_1k, chance_maj):
    chance = max(chance_1k, chance_maj)
    d = 100 * (acc - chance)
    return {"acc": round(acc, 4), "chance": round(chance, 4), "delta_pp": round(d, 2), "pass": abs(d) <= BAR_PP}


def majority_share(part) -> float:
    c = Counter(i.row["gold"] for i in part)
    return max(c.values()) / len(part)


def options_only(infos) -> dict:
    import pilot
    part = [i for i in infos if i.row["qtype"] == "choice"]
    if len(part) < 20:
        return {"pass": True, "note": "fewer than 20 choice rows"}
    g = pilot.g6_choice(part)
    maj = majority_share(part)
    v = {m: _verdict(g["b_options"][m], g["chance"], maj) for m in ("lr", "gbt")}
    return {"n": len(part), **v, "pass": all(x["pass"] for x in v.values())}


def _shape(t: str) -> dict:
    return {"len": len(t), "digits": sum(c.isdigit() for c in t), "alpha": sum(c.isalpha() for c in t),
            "upper": sum(c.isupper() for c in t), "us": t.count("_"), "sp": t.count(" ")}


def state_formatting(row) -> dict:
    st = row["state"]
    lines = st.split("\n")
    d = {"n_lines": float(len(lines)), "st_len": float(len(st)), "st_digits": float(sum(c.isdigit() for c in st)),
         "st_upper": float(sum(c.isupper() for c in st)), "st_dot": float(st.count(".")),
         "st_colon": float(st.count(":")), "st_us": float(st.count("_")), "ins_len": float(len(row["instructions"])),
         "card_len": float(len(row.get("card") or "")), "max_line": float(max(len(x) for x in lines)),
         "layout=" + str(row["meta"]["c2"]["skin_id"]): 1.0}
    return d


def formatting_only(infos) -> dict:
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import MaxAbsScaler
    res = {}
    ch = [i for i in infos if i.row["qtype"] == "choice"]
    yn = [i for i in infos if i.row["qtype"] == "noul"]
    if len(ch) >= 20:
        D, Y, R_, G_ = [], [], [], []
        for ri, i in enumerate(ch):
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
        chance = float(np.mean([1 / len(i.row["options"]) for i in ch]))
        maj = majority_share(ch)
        sub = {}
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
            acc = np.zeros(len(ch))
            for ri, lst in best.items():
                m = max(s for s, _ in lst)
                top = [yy for s, yy in lst if s >= m - 1e-12]
                acc[ri] = sum(top) / len(top)
            sub[nm] = _verdict(float(acc.mean()), chance, maj)
        res["choice"] = {"n": len(ch), **sub, "pass": all(v["pass"] for v in sub.values())}
    if len(yn) >= 20:
        D = [{**state_formatting(i.row), "ask_len": float(len(i.row["instructions"].split("\n")[0])),
              "qform=" + i.row["meta"]["qform"]: 1.0} for i in yn]
        X = DictVectorizer(sparse=False).fit_transform(D)
        y = np.array([int(i.row["gold"]) for i in yn])
        folds = _folds([i.row["meta"]["card_id"] for i in yn])
        maj = max(y.mean(), 1 - y.mean())
        sub = {}
        for nm, mk in (("lr", _lr), ("gbt", _gbt)):
            pr = np.zeros(len(y))
            for tr, te in folds:
                if len(set(y[tr])) < 2:
                    continue
                Xtr, Xte = X[tr], X[te]
                if nm == "lr":
                    sca = MaxAbsScaler().fit(Xtr)
                    Xtr, Xte = sca.transform(Xtr), sca.transform(Xte)
                pr[te] = mk().fit(Xtr, y[tr]).predict(Xte)
            sub[nm] = _verdict(float((pr == y).mean()), 0.5, float(maj))
        res["yes_no"] = {"n": len(yn), **sub, "pass": all(v["pass"] for v in sub.values())}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res
