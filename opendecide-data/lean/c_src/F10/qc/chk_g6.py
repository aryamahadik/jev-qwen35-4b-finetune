"""G6 partial-input and metadata baselines (independent F10 checker, check:F10, c-lanes-v3). 5-fold GroupKFold by
meta.card_id on out/qc_sample.jsonl (5,189 rows from the same generators). Models: logistic regression on TF-IDF word
1-2 grams; sklearn HistGradientBoosting on dense features (SVD of the n-grams, or the metadata).
Yes/no: predict gold from (a) question paragraph, (c) card + instructions without the question, (d) visible metadata
(chk_lib.meta_feats: FIX RULE "G6 metadata = only what the model sees"); chance = majority rate; (b) n/a.
Choice: pointwise (row, option) scorer, argmax per row (ties split), chance = mean 1/k; per-option features:
(a) option n-grams + question mention, (b) option n-grams + option-set structure (length rank, longest / shortest,
abstain, card-list position first / last, in-record mention, definition shown), (c) option n-grams + mentions in
card-without-question, (d) row visible metadata x option kind.
Rule: accuracy <= chance + 2 pp for every view and model. Counts only. Usage: chk_g6.py [name]"""
import json, re, sys, time
import numpy as np
from scipy import sparse
from scipy.stats import rankdata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import MaxAbsScaler
import chk_lib as q
from chk_g7 import opt_kinds

NAME = ([a for a in sys.argv[1:] if not a.startswith("--")] or ["qc_sample"])[0]
REUSE_YN = "--reuse-yn" in sys.argv  # yes/no views do not use option order; reuse a previous run on the same pool
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def lr():
    return LogisticRegression(C=1.0, max_iter=3000, solver="liblinear")


def gbt():
    return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def cv_yn(Xs, Xd, y, g):
    res = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        pred = np.zeros(len(y))
        for tr, te in GroupKFold(5).split(X, y, g):
            pred[te] = mk().fit(X[tr], y[tr]).predict(X[te])
        res[nm] = round(float((pred == y).mean()), 4)
    return res


def cv_ch(Xs, Xd, yp, prow, g):
    res = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        sc = np.zeros(len(yp))
        for tr, te in GroupKFold(5).split(X, yp, g):
            sc[te] = mk().fit(X[tr], yp[tr]).predict_proba(X[te])[:, 1]
        by = {}
        for i, (ri, s) in enumerate(zip(prow, sc)):
            by.setdefault(ri, []).append((round(float(s), 9), yp[i]))
        acc = []
        for lst in by.values():
            top = max(s for s, _ in lst); tied = [t for s, t in lst if s == top]; acc.append(sum(tied) / len(tied))
        res[nm] = round(float(np.mean(acc)), 4)
    return res


def main():
    rows, side = q.load(NAME)
    yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
    log(f"rows {len(rows)} yn {len(yn)} choice {len(ch)}")
    out = {"gate": "G6", "file": f"out/{NAME}.jsonl", "cv": "GroupKFold(5) by meta.card_id", "rule": "acc <= chance + 2 pp",
           "metadata": "visible only (chk_lib.meta_feats)", "pool_sha256": q.sha(q.OUT / f"{NAME}.jsonl"), "option_order": "len_rank ties averaged (order-invariant; v1 stable-sort rank leaked stored option order)", "yes_no": {}, "choice": {}}
    y = np.array([int(r["gold"]) for r in yn]); g = [r["meta"]["card_id"] for r in yn]
    chance = round(float(max(y.mean(), 1 - y.mean())), 4)
    prev = q.QC / f"g6_{NAME}.json"; prev_j = json.loads(prev.read_text()) if (REUSE_YN and prev.exists()) else None
    if prev_j and prev_j.get("pool_sha256") == q.sha(q.OUT / f"{NAME}.jsonl"):
        out["yes_no"] = prev_j["yes_no"]; log("yes/no views reused from previous run (same pool sha)")
    else:
        V = [q.views(r) for r in yn]
        for key, f in (("a_question", "q"), ("c_card_without_question", "cardnoq")):
            tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
            Xs = tv.fit_transform([v[f] for v in V]).tocsr(); Xd = TruncatedSVD(64, random_state=0).fit_transform(Xs)
            res = cv_yn(Xs, Xd, y, g); best = max(res.values())
            out["yes_no"][key] = {**res, "chance": chance, "best": best, "pass": best <= chance + 0.02}
            log(f"yn {key} {out['yes_no'][key]}")
        md = []
        for r in yn:
            c, n = q.meta_feats(r, side.get(r["id"])); md.append({**{f"{k}={v}": 1.0 for k, v in c.items()}, **n})
        Xm = DictVectorizer().fit_transform(md).tocsr()
        res = cv_yn(MaxAbsScaler().fit_transform(Xm), Xm.toarray(), y, g); best = max(res.values())
        out["yes_no"]["d_metadata"] = {**res, "chance": chance, "best": best, "pass": best <= chance + 0.02}
        log(f"yn d {out['yes_no']['d_metadata']}")
    out["yes_no"]["b_options"] = "n/a (yes/no options fixed)"
    prow, yp, gp, otext = [], [], [], []
    F = {"a": [], "b": [], "c": [], "d": []}
    for ri, r in enumerate(ch):
        s = side.get(r["id"]) or {}; v = q.views(r); kinds = opt_kinds(r); opts = r["options"]; k = len(opts)
        L = [len(o) for o in opts]; rank = rankdata(-np.array(L), method="average") - 1  # ties averaged: stored option order is never shown (trainer re-shuffles)
        c, n = q.meta_feats(r, s); mrow = {**{f"{a}={b}": 1.0 for a, b in c.items()}, **n}
        ql, cl = v["q"].lower(), v["cardnoq"].lower()
        for i, o in enumerate(opts):
            ol = o.lower()
            prow.append(ri); yp.append(int(o == r["gold"])); gp.append(r["meta"]["card_id"]); otext.append(o)
            F["a"].append({"q_mention": float(ol in ql)})
            b = {"k": float(k), "len": float(L[i]), "len_rank": float(rank[i]) / max(1, k - 1),
                 "len_z": float((L[i] - np.mean(L)) / (np.std(L) + 1e-6))}
            b.update({kd: 1.0 for kd in kinds[i]}); F["b"].append(b)
            F["c"].append({"c_mention": float(cl.count(ol))})
            dd = dict(mrow); dd.update({"o_" + a: x for a, x in b.items()})
            for kd in kinds[i]:
                for a in ("sc_world", "sc_mode", "sampler", "sc_ctype"):
                    dd[f"x_{a}={c.get(a)}_{kd}"] = 1.0
            F["d"].append(dd)
    yp = np.array(yp); log(f"choice pairs {len(yp)}")
    chance_c = round(float(np.mean([1 / len(r["options"]) for r in ch])), 4)
    Xo = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit_transform(otext).tocsr()
    Xo_svd = TruncatedSVD(32, random_state=0).fit_transform(Xo)
    names = {"a": "a_question", "b": "b_options", "c": "c_card_without_question", "d": "d_metadata"}
    for key in ("a", "b", "c", "d"):
        dv = DictVectorizer(); Xf = MaxAbsScaler().fit_transform(dv.fit_transform(F[key]).tocsr())
        if key == "d":
            Xs = Xf; keep = [j for j, nm in enumerate(dv.feature_names_) if not nm.startswith("x_")]; Xd = Xf[:, keep].toarray()
        else:
            Xs = sparse.hstack([Xo, Xf]).tocsr(); Xd = np.hstack([Xf.toarray(), Xo_svd])
        res = cv_ch(Xs, Xd, yp, prow, gp); best = max(res.values())
        out["choice"][names[key]] = {**res, "chance_mean_1_over_k": chance_c, "best": best, "pass": best <= chance_c + 0.02}
        log(f"choice {names[key]} {out['choice'][names[key]]}")
    flat = [v["pass"] for part in ("yes_no", "choice") for v in out[part].values() if isinstance(v, dict)]
    out["pass"] = all(flat); out["seconds"] = round(time.time() - T0, 1)
    (q.QC / f"g6_{NAME}.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


if __name__ == "__main__":
    main()
