"""G6 partial-input and metadata baselines (independent F2 checker). 5-fold CV grouped by card (GroupKFold on
meta.card_id: per-card yes rates are drawn 20-80% by design, spec 2.1, and twins never cross folds) on
out/qc_sample.jsonl (separate QC sample, >= 5,000 rows). Models: logistic regression on TF-IDF word 1-2 grams and
sklearn HistGradientBoosting on dense features. Yes/no rows: predict gold from (a) question, (c) card without
question, (d) metadata; chance 0.5 (F2 G0 6, SC2; the majority rate is reported). Choice rows: pointwise scorer over
(row, option) pairs, argmax per row (ties split evenly); chance = mean 1/k (k shown options, abstain included), also
per option bucket. Pair features: (a) option n-grams + option-question overlap, (b) option n-grams + option-set
features (length rank, numeric rank, abstain, look-alikes), (c) option n-grams + option-card overlap, (d) row metadata
x option-set features. Pass: every accuracy <= chance + 2 pp. Usage: g6.py [qc_sample]"""
import json, sys, time, re
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import MaxAbsScaler
import qc_lib as L
from collections import Counter
from scipy.stats import binomtest

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
T0 = time.time()


def log(msg):
    print(f"[{time.time() - T0:7.1f}s] {msg}", flush=True)


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


def onum(o):
    n = L.nums(o)
    return n[0] if n else None


def sim_feats(o, text):
    toks = set(re.findall(r"\w+", o.lower())); tt = set(re.findall(r"\w+", text.lower()))
    return {"mention": float(text.count(o)), "mention_any": float(o in text),
            "tok_overlap": len(toks & tt) / max(1, len(toks)), "num_in": float(any(x in L.nums(text) for x in L.nums(o)))}


def optset_feats(r):
    opts = r["options"]; k = len(opts); lens = [len(o) for o in opts]
    lr_ = np.argsort(np.argsort(-np.array(lens), kind="stable"))
    vals = [onum(o) for o in opts]; nv = sorted(v for v in vals if v is not None)
    out = []
    for i, o in enumerate(opts):
        v = vals[i]
        rk = (nv.index(v) / max(1, len(nv) - 1)) if v is not None and len(nv) > 1 else -1.0
        out.append({"k": float(k), "len": float(len(o)), "len_rank": float(lr_[i]) / max(1, k - 1),
                    "is_longest": float(lens[i] == max(lens)), "is_shortest": float(lens[i] == min(lens)),
                    "abstain": float(L.is_abstain(o)), "has_digit": float(any(c.isdigit() for c in o)),
                    "n_words": float(len(o.split())), "num_rank": rk, "is_num_min": float(v is not None and v == nv[0]),
                    "is_num_max": float(v is not None and v == nv[-1]),
                    "dec": float(v is not None and v != int(v)),
                    "n_same_val": float(sum(1 for w in vals if w is not None and w == v)) if v is not None else 0.0})
    return out


def lr():
    return LogisticRegression(C=1.0, max_iter=3000, solver="liblinear")


def gbt():
    return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def cv_yn(Xs, Xd, y, groups):
    gkf = GroupKFold(n_splits=5); res = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        pred = np.zeros(len(y))
        for tr, te in gkf.split(X, y, groups):
            m = mk().fit(X[tr], y[tr]); pred[te] = m.predict(X[te])
        res[nm] = float((pred == y).mean())
    return res


def cv_choice(Xs, Xd, yp, prow, groups_p, rows):
    gkf = GroupKFold(n_splits=5); res = {}; per_b = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        sc = np.zeros(len(yp))
        for tr, te in gkf.split(X, yp, groups_p):
            m = mk().fit(X[tr], yp[tr]); sc[te] = m.predict_proba(X[te])[:, 1]
        by = {}
        for i, (ri, s) in enumerate(zip(prow, sc)):
            by.setdefault(ri, []).append((round(float(s), 9), yp[i]))
        accs = {}
        for ri, lst in by.items():
            top = max(s for s, _ in lst); tied = [g for s, g in lst if s == top]
            accs[ri] = sum(tied) / len(tied)
        res[nm] = float(np.mean(list(accs.values())))
        for ri, a in accs.items():
            per_b.setdefault((nm, bucket(len(rows[ri]["options"]))), []).append(a)
    return res, {f"{nm}:{b}": round(float(np.mean(v)), 4) for (nm, b), v in sorted(per_b.items())}


def main():
    rows = L.load(NAME)
    yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
    log(f"rows {len(rows)} yes/no {len(yn)} choice {len(ch)}")
    out = {"gate": "G6", "file": f"out/{NAME}.jsonl", "cv": "GroupKFold(5) by meta.card_id",
           "rule": "acc <= chance + 2 pp", "yes_no": {}, "choice": {}}
    y = np.array([int(r["gold"]) for r in yn]); g = [r["meta"]["card_id"] for r in yn]
    chance = 0.5; maj = float(max(y.mean(), 1 - y.mean()))
    V = [L.views(r) for r in yn]
    for key, field in (("a_question", "q"), ("c_card_without_question", "cardnoq")):
        tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
        Xs = tv.fit_transform([v[field] for v in V]).tocsr()
        Xd = TruncatedSVD(64, random_state=0).fit_transform(Xs)
        res = cv_yn(Xs, Xd, y, g); best = max(res.values())
        out["yes_no"][key] = {**res, "chance": chance, "majority_rate": maj, "best": best, "pass": best <= chance + 0.02}
        log(f"yn {key} {out['yes_no'][key]}")
    md = []
    for r in yn:
        c, n = L.meta_feats(r); md.append({**{f"{k}={v}": 1.0 for k, v in c.items()}, **n})
    dv = DictVectorizer(); Xm = dv.fit_transform(md).tocsr(); Xms = MaxAbsScaler().fit_transform(Xm)
    res = cv_yn(Xms, Xm.toarray(), y, g); best = max(res.values())
    out["yes_no"]["d_metadata"] = {**res, "chance": chance, "majority_rate": maj, "best": best,
                                   "pass": best <= chance + 0.02, "n_features": Xm.shape[1]}
    log(f"yn d_metadata {out['yes_no']['d_metadata']}")
    out["yes_no"]["b_options"] = "n/a (yes/no options are fixed)"
    choice_part(ch, out)
    allp = [v["pass"] for part in ("yes_no", "choice") for v in out[part].values() if isinstance(v, dict) and "pass" in v]
    out["pass"] = all(allp); out["seconds"] = round(time.time() - T0, 1)
    (L.QC / "g6.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


def choice_part(ch, out):
    prow, yp, gp, otext, F = [], [], [], [], {"a": [], "b": [], "c": [], "d": []}
    for ri, r in enumerate(ch):
        v = L.views(r); os_ = optset_feats(r); c, n = L.meta_feats(r)
        mrow = {**{f"{k}={x}": 1.0 for k, x in c.items()}, **n}
        for i, o in enumerate(r["options"]):
            prow.append(ri); yp.append(int(o == r["gold"])); gp.append(r["meta"]["card_id"]); otext.append(o)
            F["a"].append(sim_feats(o, v["q"]))
            F["b"].append(os_[i])
            F["c"].append(sim_feats(o, v["cardnoq"]))
            dd = dict(mrow); dd.update({"o_" + k: x for k, x in os_[i].items()})
            for k, x in c.items():
                for ok in ("abstain", "is_longest", "is_num_min", "is_num_max"):
                    dd[f"x_{k}={x}_{ok}"] = os_[i][ok]
            F["d"].append(dd)
    yp = np.array(yp); log(f"choice pairs {len(yp)} rows {len(ch)}")
    chance = float(np.mean([1 / len(r["options"]) for r in ch]))
    cb = {}
    for r in ch:
        cb.setdefault(bucket(len(r["options"])), []).append(1 / len(r["options"]))
    cb = {b: round(float(np.mean(v)), 4) for b, v in cb.items()}
    tw = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, token_pattern=r"[^\s]+")
    tc = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, sublinear_tf=True, max_features=100000)
    Xo = sparse.hstack([tw.fit_transform(otext), tc.fit_transform(otext)]).tocsr()
    Xo_svd = TruncatedSVD(32, random_state=0).fit_transform(Xo)
    names = {"a": "a_question", "b": "b_options", "c": "c_card_without_question", "d": "d_metadata"}
    for key in ("a", "b", "c", "d"):
        dv = DictVectorizer(); Xf = dv.fit_transform(F[key]).tocsr(); Xf = MaxAbsScaler().fit_transform(Xf)
        if key == "d":
            Xs = Xf; keep = [j for j, nm in enumerate(dv.feature_names_) if not nm.startswith("x_")]
            Xd = Xf[:, keep].toarray()
        else:
            Xs = sparse.hstack([Xo, Xf]).tocsr(); Xd = np.hstack([Xf.toarray(), Xo_svd])
        res, perb = cv_choice(Xs, Xd, yp, prow, gp, ch); best = max(res.values())
        bn = Counter(bucket(len(r["options"])) for r in ch); bfail = {}
        for kk, a in perb.items():
            bk = kk.split(":")[1]
            if a > cb[bk] + 0.02:
                pv = float(binomtest(int(round(a * bn[bk])), bn[bk], cb[bk], alternative="greater").pvalue)
                if pv < 0.01:
                    bfail[kk] = {"acc": a, "chance": cb[bk], "n": bn[bk], "p": pv}
        bpass = not bfail
        out["choice"][names[key]] = {**res, "chance_mean_1_over_k": chance, "best": best,
                                     "per_bucket": perb, "chance_per_bucket": cb, "per_bucket_rows": dict(bn),
                                     "per_bucket_fail_rule": "acc > bucket chance + 2 pp AND one-sided binomial p < 0.01",
                                     "per_bucket_fails": bfail, "per_bucket_pass": bpass,
                                     "pass": best <= chance + 0.02 and bpass}
        log(f"choice {names[key]} {out['choice'][names[key]]}")


if __name__ == "__main__":
    main()
