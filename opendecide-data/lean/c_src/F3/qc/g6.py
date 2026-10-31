"""G6 partial-input and metadata baselines (independent F3 checker). 5-fold CV grouped by card (GroupKFold on
meta.card_id, so twins and a card's drawn yes rate never cross folds) on out/qc_sample.jsonl. Models: logistic
regression on TF-IDF word 1-2 grams (+ char 3-5 grams for options) and sklearn HistGradientBoosting on dense features.
Yes/no rows: predict gold from (a) question, (c) card without question, (d) metadata; chance = majority-label rate.
Choice rows: pointwise scorer over (row, option) pairs, argmax per row; chance = mean 1/k. Pair features per view:
(a) option n-grams + question-option similarity, (b) option n-grams + option-set features (length rank, look-alike
siblings, abstain), (c) option n-grams + card-option overlap, (d) row metadata x option features. Pass: every
accuracy <= chance + 2 pp. Usage: g6.py [qc_sample]"""
import json, sys, time
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
T0 = time.time()


def log(msg):
    print(f"[{time.time() - T0:7.1f}s] {msg}", flush=True)


def lev(a, b):
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def grams(s, n=3):
    s = s.lower(); return {s[i:i + n] for i in range(max(1, len(s) - n + 1))}


def jac(a, b):
    return len(a & b) / max(1, len(a | b))


def sim_feats(o, text, ids):
    """Similarity between an option and a view text: exact mention count, char-3gram Jaccard to the closest ID,
    min edit distance to an ID in the text, shared 2-char prefix with an ID."""
    f = {"mention": float(text.count(o)), "mention_any": float(o in text)}
    if ids:
        ds = [lev(o, i) for i in ids]
        f["min_lev"] = float(min(ds)); f["n_lev_le2"] = float(sum(d <= 2 for d in ds))
        f["max_jac"] = max(jac(grams(o), grams(i)) for i in ids)
        f["prefix2"] = float(any(o[:2] == i[:2] for i in ids))
    else:
        f.update(min_lev=-1.0, n_lev_le2=0.0, max_jac=0.0, prefix2=0.0)
    return f


def optset_feats(r):
    opts = r["options"]; k = len(opts); lens = [len(o) for o in opts]
    order = np.argsort(np.argsort(-np.array(lens), kind="stable"))
    out = []
    for i, o in enumerate(opts):
        ds = [lev(o, p) for j, p in enumerate(opts) if j != i] if k <= 60 else []
        g = grams(o)
        out.append({"k": float(k), "len": float(len(o)), "len_rank": float(order[i]) / max(1, k - 1),
                    "is_longest": float(lens[i] == max(lens)), "is_shortest": float(lens[i] == min(lens)),
                    "len_z": (lens[i] - np.mean(lens)) / (np.std(lens) + 1e-6), "abstain": float(L.is_abstain(o)),
                    "has_digit": float(any(c.isdigit() for c in o)), "n_words": float(len(o.split())),
                    "sib_lev_le1": float(sum(d <= 1 for d in ds)), "sib_lev_le2": float(sum(d <= 2 for d in ds)),
                    "sib_min_lev": float(min(ds)) if ds else -1.0,
                    "sib_mean_jac": float(np.mean([jac(g, grams(p)) for j, p in enumerate(opts) if j != i])) if k > 1 else 0.0})
    return out


def lr():
    return LogisticRegression(C=1.0, max_iter=3000, solver="liblinear")


def gbt():
    return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def cv_yn(Xs, Xd, y, groups):
    gkf = GroupKFold(n_splits=5); res = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        if X is None:
            continue
        pred = np.zeros(len(y))
        for tr, te in gkf.split(X, y, groups):
            m = mk().fit(X[tr], y[tr]); pred[te] = m.predict(X[te])
        res[nm] = float((pred == y).mean())
    return res


def cv_choice(Xs, Xd, yp, prow, groups_p, nrows):
    gkf = GroupKFold(n_splits=5); res = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        if X is None:
            continue
        sc = np.zeros(len(yp))
        for tr, te in gkf.split(X, yp, groups_p):
            m = mk().fit(X[tr], yp[tr]); sc[te] = m.predict_proba(X[te])[:, 1]
        # expected accuracy under uniform random tie-breaking (canonical option order never decides a tie)
        by = {}
        for i, (ri, s) in enumerate(zip(prow, sc)):
            by.setdefault(ri, []).append((round(float(s), 9), yp[i]))
        accs = []
        for lst in by.values():
            top = max(s for s, _ in lst); tied = [g for s, g in lst if s == top]
            accs.append(sum(tied) / len(tied))
        res[nm] = float(np.mean(accs))
    return res


def main():
    rows, side = L.load(NAME)
    yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
    log(f"rows {len(rows)} yes/no {len(yn)} choice {len(ch)}")
    out = {"gate": "G6", "file": f"out/{NAME}.jsonl", "cv": "GroupKFold(5) by meta.card_id", "rule": "acc <= chance + 2 pp",
           "yes_no": {}, "choice": {}}
    # ---- yes/no
    y = np.array([int(r["gold"]) for r in yn]); g = [r["meta"]["card_id"] for r in yn]
    chance = float(max(y.mean(), 1 - y.mean()))
    V = [L.views(r) for r in yn]
    for key, field in (("a_question", "q"), ("c_card_without_question", "cardnoq")):
        tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
        Xs = tv.fit_transform([v[field] for v in V]).tocsr()
        Xd = TruncatedSVD(64, random_state=0).fit_transform(Xs)
        res = cv_yn(Xs, Xd, y, g); best = max(res.values())
        out["yes_no"][key] = {**res, "chance": chance, "best": best, "pass": best <= chance + 0.02}
        log(f"yn {key} {out['yes_no'][key]}")
    md = []
    for r in yn:
        c, n = L.meta_feats(r, side.get(r["id"])); md.append({**{f"{k}={v}": 1.0 for k, v in c.items()}, **n})
    dv = DictVectorizer(); Xm = dv.fit_transform(md).tocsr()
    from sklearn.preprocessing import MaxAbsScaler
    Xms = MaxAbsScaler().fit_transform(Xm)
    res = cv_yn(Xms, Xm.toarray(), y, g); best = max(res.values())
    out["yes_no"]["d_metadata"] = {**res, "chance": chance, "best": best, "pass": best <= chance + 0.02, "n_features": Xm.shape[1]}
    log(f"yn d_metadata {out['yes_no']['d_metadata']}")
    out["yes_no"]["b_options"] = "n/a (yes/no options are fixed)"
    choice_part(ch, side, out)
    allp = [v["pass"] for part in ("yes_no", "choice") for v in out[part].values() if isinstance(v, dict)]
    out["pass"] = all(allp); out["seconds"] = round(time.time() - T0, 1)
    (L.QC / "g6.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


def choice_part(ch, side, out):
    prow, yp, gp, otext, F = [], [], [], [], {"a": [], "b": [], "c": [], "d": []}
    meta_rows = []
    for ri, r in enumerate(ch):
        v = L.views(r); qids = set(L.ID_RX.findall(v["q"])) or set(); cids = set(L.ID_RX.findall(v["cardnoq"]))
        os_ = optset_feats(r); c, n = L.meta_feats(r, side.get(r["id"]))
        mrow = {**{f"{k}={x}": 1.0 for k, x in c.items()}, **n}
        for i, o in enumerate(r["options"]):
            prow.append(ri); yp.append(int(o == r["gold"])); gp.append(r["meta"]["card_id"]); otext.append(o)
            F["a"].append(sim_feats(o, v["q"], qids))
            F["b"].append(os_[i])
            F["c"].append(sim_feats(o, v["cardnoq"], cids))
            dd = dict(mrow); dd.update({"o_" + k: x for k, x in os_[i].items()})
            for k, x in c.items():  # crosses for the linear model: metadata value x option kind
                dd[f"x_{k}={x}_abst"] = os_[i]["abstain"]; dd[f"x_{k}={x}_longest"] = os_[i]["is_longest"]
            F["d"].append(dd)
    yp = np.array(yp); log(f"choice pairs {len(yp)} rows {len(ch)}")
    chance = float(np.mean([1 / len(r["options"]) for r in ch]))
    from sklearn.preprocessing import MaxAbsScaler
    tw = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, token_pattern=r"[^\s]+")
    tc = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, sublinear_tf=True, max_features=100000)
    Xo = sparse.hstack([tw.fit_transform(otext), tc.fit_transform(otext)]).tocsr()
    Xo_svd = TruncatedSVD(32, random_state=0).fit_transform(Xo)
    names = {"a": "a_question", "b": "b_options", "c": "c_card_without_question", "d": "d_metadata"}
    for key in ("a", "b", "c", "d"):
        dv = DictVectorizer(); Xf = dv.fit_transform(F[key]).tocsr(); Xf = MaxAbsScaler().fit_transform(Xf)
        Xs = sparse.hstack([Xo, Xf]).tocsr() if key != "d" else Xf
        if key == "d":
            keep = [j for j, nm in enumerate(dv.feature_names_) if not nm.startswith("x_")]
            Xd = Xf[:, keep].toarray()
        else:
            Xd = np.hstack([Xf.toarray(), Xo_svd])
        res = cv_choice(Xs, Xd, yp, prow, gp, len(ch)); best = max(res.values())
        out["choice"][names[key]] = {**res, "chance_mean_1_over_k": chance, "best": best, "pass": best <= chance + 0.02}
        log(f"choice {names[key]} {out['choice'][names[key]]}")


if __name__ == "__main__":
    main()
