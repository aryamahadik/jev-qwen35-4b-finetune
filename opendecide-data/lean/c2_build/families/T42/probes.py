"""families/T42/probes.py: the T42 probes (FINAL_PLAN section 3 and BUILD brief): measured on an in-memory build
(pilot.build_pilot infos), never on files.

  options_only(infos)      pilot G6 view (b): a model sees only the option texts of a choice row (tokens, lengths, ranks,
                           kinds), 5-fold GroupKFold by card, LR and GBT; reported per head. Bar: accuracy within chance +/- 3 pp.
  formatting_only(infos)   a model sees only FORMATTING: option length / character classes / length rank (output head) and
                           the layout, line counts, length and indentation of the code blocks (both heads); no word is
                           read. Bar: within chance +/- 3 pp (output head: 1/k per row; equivalence: 1/3).
  diff_size(infos)         equivalence pairs: do token / line / character diff sizes of f against g predict SAME against
                           DIFFERS? Reported: per-metric AUC (Mann-Whitney), CV accuracy and AUC of LR / GBT on all the
                           size features, and the majority baseline. Bar: CV accuracy <= majority + 3 pp and AUC within
                           0.5 +/- 0.05.
  cues(infos)              report only: the median-number and medoid (most similar to the others) options of the output head.
"""
from __future__ import annotations

import difflib
import math
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


def _split(infos):
    out = [i for i in infos if i.row["meta"]["qform"] in ("ch_output", "ch_return")]
    eq = [i for i in infos if i.row["meta"]["qform"] == "ch_equiv"]
    return out, eq


def _verdict(acc, chance):
    d = 100 * (acc - chance)
    return {"acc": round(acc, 4), "chance": round(chance, 4), "delta_pp": round(d, 2), "pass": abs(d) <= BAR_PP}


# ------------------------------------------------------------------------------------------------ options only
def options_only(infos) -> dict:
    import pilot
    res = {}
    out, eq = _split(infos)
    for name, part in (("output", out), ("equivalence", eq)):
        if len(part) < 20:
            continue
        g = pilot.g6_choice(part)
        chance = g["chance"]
        v = {m: _verdict(g["b_options"][m], chance) for m in ("lr", "gbt")}
        res[name] = {"n": len(part), **v, "pass": all(x["pass"] for x in v.values())}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res


# ------------------------------------------------------------------------------------------------ formatting only
def _shape(t: str) -> dict:
    return {"len": len(t), "digits": sum(c.isdigit() for c in t), "alpha": sum(c.isalpha() for c in t),
            "upper": sum(c.isupper() for c in t), "space": t.count(" "), "comma": t.count(","),
            "brk": sum(t.count(c) for c in "[](){}"), "quote": t.count("'") + t.count('"'), "dot": t.count("."),
            "minus": t.count("-"), "colon": t.count(":"), "raises": float(t.startswith("raises "))}


def _layout_feats(row) -> dict:
    st = row["state"]
    lines = st.split("\n")
    ind = [len(re.match(r"[ \t>0-9]*", ln).group()) for ln in lines]
    return {"lay_len": len(st), "lay_lines": len(lines), "lay_maxline": max(map(len, lines)),
            "lay_ind_max": max(ind), "lay_ind_mean": float(np.mean(ind)), "lay_q": len(row["instructions"])}


def formatting_only(infos) -> dict:
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import MaxAbsScaler
    res = {}
    out, eq = _split(infos)
    if len(out) >= 20:
        D, Y, R_, G_ = [], [], [], []
        for ri, i in enumerate(out):
            r = i.row
            opts = r["options"]
            lens = [len(o) for o in opts]
            order = sorted(range(len(opts)), key=lambda j: (lens[j], opts[j]))
            rank = {j: n for n, j in enumerate(order)}
            lay = _layout_feats(r)
            for j, o in enumerate(opts):
                d = {**_shape(o), "k": len(opts), "rank": rank[j], "rank_frac": rank[j] / (len(opts) - 1),
                     "longest": float(lens[j] == max(lens)), "shortest": float(lens[j] == min(lens)),
                     "len_vs_mean": lens[j] - sum(lens) / len(lens), **lay,
                     "layout=" + str(r["meta"]["c2"]["register"]): 1.0}
                D.append(d)
                Y.append(int(o == r["gold"]))
                R_.append(ri)
                G_.append(r["meta"]["card_id"])
        X = DictVectorizer(sparse=False).fit_transform(D)
        Y, R_ = np.array(Y), np.array(R_)
        folds = _folds(G_)
        chance = float(np.mean([1 / len(i.row["options"]) for i in out]))
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
            acc = np.zeros(len(out))
            best = defaultdict(list)
            for s, ri, yy in zip(sc, R_, Y):
                best[ri].append((s, yy))
            for ri, lst in best.items():
                m = max(s for s, _ in lst)
                top = [yy for s, yy in lst if s >= m - 1e-12]
                acc[ri] = sum(top) / len(top)
            sub[nm] = _verdict(float(acc.mean()), chance)
        res["output"] = {"n": len(out), **sub, "pass": all(v["pass"] for v in sub.values())}
    if len(eq) >= 30:
        D, y, G_ = [], [], []
        labs = ["SAME", "DIFFERS_TYPICAL", "DIFFERS_EDGE"]
        for i in eq:
            r = i.row
            f, g = i.spec.structure["f"], i.spec.structure["g"]
            lay = _layout_feats(r)
            D.append({**lay, "len_f": len(f), "len_g": len(g), "len_diff": len(f) - len(g), "lines_f": f.count("\n") + 1,
                      "lines_g": g.count("\n") + 1, "line_diff": f.count("\n") - g.count("\n"),
                      "ind_f": max(len(x) - len(x.lstrip()) for x in f.split("\n")),
                      "ind_g": max(len(x) - len(x.lstrip()) for x in g.split("\n")),
                      "gold_pos": r["options"].index(r["gold"]), "layout=" + str(r["meta"]["c2"]["register"]): 1.0})
            y.append(labs.index(r["gold"]))
            G_.append(r["meta"]["card_id"])
        X = DictVectorizer(sparse=False).fit_transform(D)
        y = np.array(y)
        folds = _folds(G_)
        sub = {}
        for nm, mk in (("lr", _lr), ("gbt", _gbt)):
            pred = np.zeros(len(y), dtype=int)
            for tr, te in folds:
                Xtr, Xte = X[tr], X[te]
                if nm == "lr":
                    sca = MaxAbsScaler().fit(Xtr)
                    Xtr, Xte = sca.transform(Xtr), sca.transform(Xte)
                pred[te] = mk().fit(Xtr, y[tr]).predict(Xte)
            sub[nm] = _verdict(float((pred == y).mean()), 1 / 3)
        res["equivalence"] = {"n": len(eq), **sub, "pass": all(v["pass"] for v in sub.values()),
                              "note": "label classes: SAME / DIFFERS_TYPICAL / DIFFERS_EDGE from formatting features of the "
                                      "two code blocks and the layout only; the option position is included"}
    res["pass"] = all(v["pass"] for v in res.values() if isinstance(v, dict))
    return res


# ------------------------------------------------------------------------------------------------ diff size
def size_features(f: str, g: str) -> dict:
    g2 = re.sub(r"\bdef g\(", "def f(", g, count=1)
    tf, tg = re.findall(r"\w+|[^\w\s]", f), re.findall(r"\w+|[^\w\s]", g2)
    sm = difflib.SequenceMatcher(None, tf, tg, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    tok = sum(max(i2 - i1, j2 - j1) for _, i1, i2, j1, j2 in ops)
    lf, lg = f.split("\n"), g2.split("\n")
    lops = [o for o in difflib.SequenceMatcher(None, lf, lg, autojunk=False).get_opcodes() if o[0] != "equal"]
    lines = sum(max(i2 - i1, j2 - j1) for _, i1, i2, j1, j2 in lops)
    cs = difflib.SequenceMatcher(None, f, g2, autojunk=False)
    chars = sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in cs.get_opcodes() if t != "equal")
    return {"tok_diff": tok, "tok_hunks": len(ops), "line_diff": lines, "line_hunks": len(lops), "char_diff": chars,
            "tok_ratio": tok / max(1, len(tf) + len(tg)), "len_gap": abs(len(f) - len(g)),
            "tok_gap": abs(len(tf) - len(tg)), "total_tok": len(tf) + len(tg)}


def _auc(pos, neg) -> float:
    """Mann-Whitney AUC of 'larger value -> positive class' (ties count half)."""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if not len(pos) or not len(neg):
        return float("nan")
    allv = np.concatenate([pos, neg])
    ranks = allv.argsort().argsort() + 1.0
    for v in np.unique(allv):                      # average ranks over ties
        m = allv == v
        ranks[m] = ranks[m].mean()
    return float((ranks[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def diff_size(infos) -> dict:
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import MaxAbsScaler
    _, eq = _split(infos)
    if len(eq) < 30:
        return {"skipped": "fewer than 30 equivalence rows", "pass": True}
    F = [size_features(i.spec.structure["f"], i.spec.structure["g"]) for i in eq]
    lab = np.array([i.row["gold"] for i in eq])
    same = lab == "SAME"
    per = {}
    for k in F[0]:
        v = np.array([x[k] for x in F], float)
        a = _auc(v[same], v[~same])
        per[k] = {"auc_same_vs_differs": round(a, 3), "mean_same": round(float(v[same].mean()), 2),
                  "mean_differs": round(float(v[~same].mean()), 2)}
    X = DictVectorizer(sparse=False).fit_transform(F)
    y = same.astype(int)
    folds = _folds([i.row["meta"]["card_id"] for i in eq])
    maj = float(max(y.mean(), 1 - y.mean()))
    models = {}
    for nm, mk in (("lr", _lr), ("gbt", _gbt)):
        p = np.zeros(len(y))
        for tr, te in folds:
            Xtr, Xte = X[tr], X[te]
            if nm == "lr":
                sca = MaxAbsScaler().fit(Xtr)
                Xtr, Xte = sca.transform(Xtr), sca.transform(Xte)
            if len(set(y[tr])) < 2:
                p[te] = y[tr][0]
                continue
            p[te] = mk().fit(Xtr, y[tr]).predict_proba(Xte)[:, 1]
        acc = float(((p >= 0.5) == y).mean())
        auc = _auc(p[y == 1], p[y == 0])
        models[nm] = {"cv_acc": round(acc, 4), "cv_auc": round(auc, 3), "majority": round(maj, 4),
                      "pass": acc <= maj + BAR_PP / 100 and abs(auc - 0.5) <= 0.05}
    # label thirds within each token-diff bin (the sampler balances them by construction)
    bins = defaultdict(Counter)
    for i in eq:
        bins[i.spec.structure["diff_bin"]][i.row["gold"]] += 1
    res = {"n": len(eq), "same_share": round(float(y.mean()), 4), "per_metric": per, "models": models,
           "label_by_diff_bin": {str(b): dict(c) for b, c in sorted(bins.items())},
           "pass": all(m["pass"] for m in models.values())}
    return res


# ------------------------------------------------------------------------------------------------ report-only cues
def cues(infos) -> dict:
    out, _ = _split(infos)
    med_hit = med_n = md_hit = md_n = 0
    chance_med = chance_md = 0.0
    for i in out:
        r = i.row
        opts = r["options"]
        nums = [(float(o), o) for o in opts if re.fullmatch(r"-?\d+(?:\.\d+)?", o)]
        if len(nums) >= 3 and r["gold"] in [o for _, o in nums]:
            order = sorted(nums)
            mid = order[(len(order) - 1) // 2][1]
            med_hit += mid == r["gold"]
            med_n += 1
            chance_med += 1 / len(nums)
        sims = [sum(difflib.SequenceMatcher(None, o, p).ratio() for p in opts if p is not o) for o in opts]
        top = [j for j, s in enumerate(sims) if s >= max(sims) - 1e-12]
        md_hit += (opts.index(r["gold"]) in top) / len(top)
        md_n += 1
        chance_md += 1 / len(opts)
    return {"median_number": {"rows": med_n, "hit": round(med_hit / max(1, med_n), 4),
                              "chance": round(chance_med / max(1, med_n), 4)},
            "medoid_option": {"rows": md_n, "hit": round(md_hit / max(1, md_n), 4),
                              "chance": round(chance_md / max(1, md_n), 4)}}
