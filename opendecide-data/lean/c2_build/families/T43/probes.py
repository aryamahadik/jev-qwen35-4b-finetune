"""families/T43/probes.py: the T43 probes (A42-D 3.2), measured on an in-memory build (pilot.build_pilot infos), never on files.

  options_only(infos)     pilot G6 view (b) per head (ll, lf, pv): a model sees only the option texts of a choice row. Bar: accuracy
                          within chance +/- 3 pp, chance = max(mean 1/k, majority share of the gold option text).
  formatting_only(infos)  per head, a model sees only formatting: option length / character classes / length rank, the layout, the
                          line counts, lengths and indentation of the code, tests, run and patch sections; no word is read.
  diff_size(infos)        pv rows: a predictor from added / removed lines, hunk count, token edit distance and AST node delta (patched
                          against shown file) predicts the verdict label A / B / C (D rows: dev only). Bar: CV accuracy <= majority + 3 pp.
  g6_by_head(infos)       pilot.g6 on every head with >= 1,000 rows (the A45 d per-head rule).
"""
from __future__ import annotations

import ast
import difflib
import re
from collections import Counter, defaultdict

import numpy as np

BAR_PP = 3.0
HEADS = ("ll", "lf", "pv")


def head_of(info) -> str:
    return info.spec.structure["head"]


def _folds(groups, n=5):
    from sklearn.model_selection import GroupKFold
    return list(GroupKFold(n_splits=min(n, len(set(groups)))).split(np.zeros(len(groups)), groups=np.array(groups)))


def _lr():
    from sklearn.linear_model import LogisticRegression
    return LogisticRegression(C=1.0, max_iter=3000)


def _gbt():
    from sklearn.ensemble import HistGradientBoostingClassifier
    return HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def _chance(part) -> float:
    base = float(np.mean([1 / len(i.row["options"]) for i in part]))
    maj = max(Counter(i.row["gold"] for i in part).values()) / len(part)
    return max(base, maj)


def _verdict(acc, chance):
    d = 100 * (acc - chance)
    return {"acc": round(acc, 4), "chance": round(chance, 4), "delta_pp": round(d, 2), "pass": abs(d) <= BAR_PP}


def options_only(infos) -> dict:
    import pilot
    res = {}
    for h in HEADS:
        part = [i for i in infos if head_of(i) == h]
        if len(part) < 100:
            continue
        g = pilot.g6_choice(part)
        ch = _chance(part)
        v = {m: _verdict(g["b_options"][m], ch) for m in ("lr", "gbt")}
        res[h] = {"n": len(part), **v, "pass": all(x["pass"] for x in v.values())}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res


def g6_by_head(infos) -> dict:
    import pilot
    out = {}
    for h in HEADS:
        part = [i for i in infos if head_of(i) == h]
        if len(part) >= 1000:
            g = pilot.g6(part)
            out[h] = {"n": len(part), "verdict": g["verdict"], "fails": g["fails"], "choice": g["choice"]}
    return out


def _shape(t: str) -> dict:
    return {"len": len(t), "digits": sum(c.isdigit() for c in t), "alpha": sum(c.isalpha() for c in t),
            "upper": sum(c.isupper() for c in t), "space": t.count(" "), "colon": t.count(":"), "under": t.count("_")}


def _layout(row, st) -> dict:
    s = row["state"]
    lines = s.split("\n")
    ind = [len(re.match(r"[ \t>|0-9]*", ln).group()) for ln in lines]
    code = st["code"].split("\n")
    return {"lay_len": len(s), "lay_lines": len(lines), "lay_maxline": max(map(len, lines)), "lay_ind_max": max(ind),
            "lay_ind_mean": float(np.mean(ind)), "code_lines": len(code), "code_len": len(st["code"]), "q_len": len(row["instructions"]),
            "layout=" + str(row["meta"]["c2"]["register"]): 1.0}


def formatting_only(infos) -> dict:
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import MaxAbsScaler
    res = {}
    for h in HEADS:
        part = [i for i in infos if head_of(i) == h]
        if len(part) < 100:
            continue
        D, Y, R_, G_ = [], [], [], []
        for ri, i in enumerate(part):
            r, st = i.row, i.spec.structure
            opts = r["options"]
            lens = [len(o) for o in opts]
            order = sorted(range(len(opts)), key=lambda j: (lens[j], opts[j]))
            rank = {j: n for n, j in enumerate(order)}
            lay = _layout(r, st)
            for j, o in enumerate(opts):
                D.append({**_shape(o), "k": len(opts), "rank": rank[j], "rank_frac": rank[j] / (len(opts) - 1),
                          "longest": float(lens[j] == max(lens)), "shortest": float(lens[j] == min(lens)),
                          "len_vs_mean": lens[j] - sum(lens) / len(lens), **lay})
                Y.append(int(o == r["gold"]))
                R_.append(ri)
                G_.append(r["meta"]["card_id"])
        X = DictVectorizer(sparse=False).fit_transform(D)
        Y, R_ = np.array(Y), np.array(R_)
        folds = _folds(G_)
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
            acc = np.zeros(len(part))
            for ri, lst in best.items():
                m = max(s for s, _ in lst)
                top = [yy for s, yy in lst if s >= m - 1e-12]
                acc[ri] = sum(top) / len(top)
            sub[nm] = _verdict(float(acc.mean()), _chance(part))
        res[h] = {"n": len(part), **sub, "pass": all(v["pass"] for v in sub.values())}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res


def size_features(st: dict) -> dict:
    a, b = st["code"], st["patched"] if st["patched"] is not None else st["code"]
    ta, tb = re.findall(r"\w+|[^\w\s]", a), re.findall(r"\w+|[^\w\s]", b)
    ops = [o for o in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes() if o[0] != "equal"]
    tok = sum(max(i2 - i1, j2 - j1) for _, i1, i2, j1, j2 in ops)
    dl = [x for x in (st["patch"] or "").split("\n") if x[:1] in "+-" and not x.startswith(("+++", "---"))]
    hunks = sum(1 for x in (st["patch"] or "").split("\n") if x.startswith("@@"))
    na, nb = sum(1 for _ in ast.walk(ast.parse(a))), sum(1 for _ in ast.walk(ast.parse(b)))
    return {"added": sum(x[0] == "+" for x in dl), "removed": sum(x[0] == "-" for x in dl), "hunks": hunks,
            "tok_edit": tok, "tok_hunks": len(ops), "ast_delta": nb - na, "ast_abs": abs(nb - na),
            "patch_lines": len((st["patch"] or "").split("\n")), "code_lines": len(a.split("\n"))}


def _auc(pos, neg) -> float:
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if not len(pos) or not len(neg):
        return float("nan")
    allv = np.concatenate([pos, neg])
    ranks = allv.argsort().argsort() + 1.0
    for v in np.unique(allv):
        m = allv == v
        ranks[m] = ranks[m].mean()
    return float((ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def diff_size(infos) -> dict:
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import MaxAbsScaler
    pv = [i for i in infos if head_of(i) == "pv" and i.row["gold"] != "does not apply"]
    if len(pv) < 100:
        return {"skipped": "fewer than 100 pv rows", "pass": True}
    labs = {"fixes the bug": 0, "does not fix the bug": 1, "passes the target test but is still wrong": 2}
    y = np.array([labs[i.row["gold"]] for i in pv])
    F = [size_features(i.spec.structure) for i in pv]
    per = {}
    for k in F[0]:
        v = np.array([x[k] for x in F], float)
        per[k] = {f"auc_{c}": round(_auc(v[y == c], v[y != c]), 3) for c in (0, 1, 2)}
    X = DictVectorizer(sparse=False).fit_transform(F)
    folds = _folds([i.row["meta"]["card_id"] for i in pv])
    maj = float(np.bincount(y).max() / len(y))
    models = {}
    for nm, mk in (("lr", _lr), ("gbt", _gbt)):
        pred = np.zeros(len(y), dtype=int)
        prob = np.zeros((len(y), 3))
        for tr, te in folds:
            Xtr, Xte = X[tr], X[te]
            if nm == "lr":
                sca = MaxAbsScaler().fit(Xtr)
                Xtr, Xte = sca.transform(Xtr), sca.transform(Xte)
            m = mk().fit(Xtr, y[tr])
            prob[te] = m.predict_proba(Xte)
            pred[te] = m.predict(Xte)
        acc = float((pred == y).mean())
        aucs = [_auc(prob[y == c, c], prob[y != c, c]) for c in range(3)]
        models[nm] = {"cv_acc": round(acc, 4), "majority": round(maj, 4), "cv_auc_per_label": [round(a, 3) for a in aucs],
                      "pass": acc <= maj + BAR_PP / 100}
    return {"n": len(pv), "label_shares": [round(float((y == c).mean()), 4) for c in range(3)], "per_metric": per,
            "models": models, "pass": all(m["pass"] for m in models.values())}
