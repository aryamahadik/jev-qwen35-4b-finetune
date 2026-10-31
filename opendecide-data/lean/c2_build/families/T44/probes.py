"""families/T44/probes.py: the A42-D 3.2 probes for T44, measured on an in-memory build (pilot.build_pilot infos).

  options_only(infos)     pilot G6 view (b) per head: a model sees only the option texts (tokens, lengths, ranks, kinds),
                          5-fold GroupKFold by card, LR and GBT. Bar: accuracy within chance +/- 3 pp (chance = the
                          majority share of the eval split, never below 1/k; per row 1/k for choice rows).
  formatting_only(infos)  a model sees only FORMATTING, no word: layout (register), line counts, lengths, indentation,
                          plan / call-list length, comma and bracket counts; next head: also the option shapes
                          (length, character classes, length rank). Verdict head: predicts the gold label (majority
                          share of the eval split is the chance); next head: the gold option among 4.
  (the diff-size probe of the coding families does not apply to T44)
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

import numpy as np

BAR_PP = 3.0
HEADS = ("ch_verdict", "ch_next")


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


def _split(infos):
    return {h: [i for i in infos if i.row["meta"]["qform"] == h] for h in HEADS}


def _verdict(acc, chance):
    d = 100 * (acc - chance)
    return {"acc": round(acc, 4), "chance": round(chance, 4), "delta_pp": round(d, 2), "pass": abs(d) <= BAR_PP}


def options_only(infos) -> dict:
    import pilot
    res = {}
    for name, part in _split(infos).items():
        if len(part) < 20:
            continue
        g = pilot.g6_choice(part)
        if name == "ch_verdict":
            maj = max(Counter(i.spec.structure.get("label_key", i.row["gold"].split("_")[0]) for i in part).values()) / len(part)
            chance = max(g["chance"], maj)
        else:
            chance = g["chance"]
        v = {m: _verdict(g["b_options"][m], chance) for m in ("lr", "gbt")}
        res[name] = {"n": len(part), **v, "pass": all(x["pass"] for x in v.values())}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res


def _shape(t: str) -> dict:
    return {"len": len(t), "digits": sum(c.isdigit() for c in t), "alpha": sum(c.isalpha() for c in t),
            "upper": sum(c.isupper() for c in t), "space": t.count(" "), "comma": t.count(","), "us": t.count("_"),
            "dot": t.count("."), "dash": t.count("-")}


def _layout(row) -> dict:
    st = row["state"]
    lines = st.split("\n")
    tools = lines[1:next(i for i, l in enumerate(lines) if l.startswith("Objects:"))]
    plan_i = next(i for i, l in enumerate(lines) if l.startswith(("Plan:", "Calls so far:")))
    plan = lines[plan_i + 1:]
    ind = [len(l) - len(l.lstrip()) for l in lines]
    return {"len": len(st), "lines": len(lines), "maxline": max(map(len, lines)), "ind_max": max(ind),
            "n_tools": len(tools), "len_tools": sum(map(len, tools)), "n_plan": len(plan), "len_plan": sum(map(len, plan)),
            "commas_plan": sum(l.count(",") for l in plan), "commas_all": st.count(","), "parens": st.count("("),
            "len_ins": len(row["instructions"]), "len_start": len(lines[plan_i - 2]), "len_goal": len(lines[plan_i - 1]),
            "len_objs": len(lines[plan_i - 3]), "nots": st.count("not "),
            "reg=" + str(row["meta"]["c2"]["register"]): 1.0}


def formatting_only(infos) -> dict:
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import MaxAbsScaler
    res = {}
    parts = _split(infos)
    nx = parts["ch_next"]
    if len(nx) >= 20:
        D, Y, R_, G_ = [], [], [], []
        for ri, i in enumerate(nx):
            r = i.row
            opts = r["options"]
            lens = [len(o) for o in opts]
            order = sorted(range(len(opts)), key=lambda j: (lens[j], opts[j]))
            rank = {j: n for n, j in enumerate(order)}
            lay = _layout(r)
            for j, o in enumerate(opts):
                D.append({**_shape(o), "k": len(opts), "rank": rank[j], "longest": float(lens[j] == max(lens)),
                          "shortest": float(lens[j] == min(lens)), "len_vs_mean": lens[j] - sum(lens) / len(lens), **lay})
                Y.append(int(o == r["gold"]))
                R_.append(ri)
                G_.append(r["meta"]["card_id"])
        X = DictVectorizer(sparse=False).fit_transform(D)
        Y, R_ = np.array(Y), np.array(R_)
        folds = _folds(G_)
        chance = float(np.mean([1 / len(i.row["options"]) for i in nx]))
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
            acc = np.zeros(len(nx))
            for ri, lst in best.items():
                m = max(s for s, _ in lst)
                top = [yy for s, yy in lst if s >= m - 1e-12]
                acc[ri] = sum(top) / len(top)
            sub[nm] = _verdict(float(acc.mean()), chance)
        res["ch_next"] = {"n": len(nx), **sub, "pass": all(v["pass"] for v in sub.values())}
    vd = parts["ch_verdict"]
    if len(vd) >= 40:
        labs = ["INVALID", "STEP", "GOAL_NOT_REACHED", "VALID"]
        D, y, G_ = [], [], []
        for i in vd:
            r = i.row
            D.append({**_layout(r), "gold_pos": r["options"].index(r["gold"]),
                      "kshow": int(re.search(r"STEP_(\d+)", " ".join(r["options"])).group(1))})
            y.append(labs.index("STEP" if r["gold"].startswith("STEP_") else r["gold"]))
            G_.append(r["meta"]["card_id"])
        X = DictVectorizer(sparse=False).fit_transform(D)
        y = np.array(y)
        folds = _folds(G_)
        maj = float(np.bincount(y).max() / len(y))
        sub = {}
        for nm, mk in (("lr", _lr), ("gbt", _gbt)):
            pred = np.zeros(len(y), dtype=int)
            for tr, te in folds:
                Xtr, Xte = X[tr], X[te]
                if nm == "lr":
                    sca = MaxAbsScaler().fit(Xtr)
                    Xtr, Xte = sca.transform(Xtr), sca.transform(Xte)
                pred[te] = mk().fit(Xtr, y[tr]).predict(Xte)
            sub[nm] = _verdict(float((pred == y).mean()), max(maj, 0.25))
        res["ch_verdict"] = {"n": len(vd), **sub, "pass": all(v["pass"] for v in sub.values()),
                             "note": "gold label (4 classes) from layout / count / length features and the gold position"}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res
