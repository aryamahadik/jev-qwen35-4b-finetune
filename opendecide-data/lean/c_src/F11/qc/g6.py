"""G6 partial-input and metadata baselines (independent F11 checker, check:F11, c-lanes-v3; adapted from the F8
checker's g6.py, models and rule unchanged). C_DATA_SPEC 8 G6 + F11 G0 6. 5-fold GroupKFold by meta.card_id on
out/<name>.jsonl (gated on the separate >= 5,000-row qc_sample). LR on TF-IDF word 1-2 grams; HistGradientBoosting on
dense features (64-d SVD of the n-grams, or the metadata). Yes/no: (a) question paragraph, (c) card + instructions
without the question paragraph, (d) metadata (chk_lib.meta_feats: model-visible fields only); (b) n/a (Yes/No fixed).
Choice: pointwise (row, option) scorer, argmax per row (ties split), chance = mean 1/k (also per option bucket);
(a) option n-grams + question mention, (b) option n-grams + option-set structure, (c) option n-grams + mention /
listing order in card-without-question, (d) row metadata x option kind. Rule: accuracy <= chance + 2 pp for every view
and model (per bucket: > chance + 2 pp AND binomial p < 0.01 fails). Counts only. Usage: g6.py [qc_sample]"""
import json, re, sys, time
from collections import Counter
import numpy as np
from scipy import sparse
from scipy.stats import binomtest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import MaxAbsScaler
import chk_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
T0 = time.time()


def log(msg):
    print(f"[{time.time() - T0:7.1f}s] {msg}", flush=True)


def onum(o):
    n = L.nums(o)
    return n[0] if n else None


def sim_feats(o, text):
    toks = set(re.findall(r"\w+", o.lower())); tt = set(re.findall(r"\w+", text.lower()))
    pos = text.find(o)
    return {"mention": float(text.count(o)), "mention_any": float(o in text),
            "tok_overlap": len(toks & tt) / max(1, len(toks)), "num_in": float(any(x in L.nums(text) for x in L.nums(o))),
            "first_pos": (pos / max(1, len(text))) if pos >= 0 else -1.0}


def list_rank(r, text):
    """listing order of each option's first mention in `text` (tier / bin / outcome order), as a rank in [0, 1]."""
    opts = r["options"]; pos = [text.find(o) for o in opts]
    ok = [p for p in pos if p >= 0]; uk = sorted(set(ok))
    out = []
    for p in pos:
        if p < 0 or len(uk) < 2:
            out.append({"lr_first": 0.0, "lr_last": 0.0, "lr_rank": -1.0})
        else:
            i = uk.index(p)
            out.append({"lr_first": float(i == 0), "lr_last": float(i == len(uk) - 1), "lr_rank": i / (len(uk) - 1)})
    return out


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
                    "n_words": float(len(o.split())), "num_rank": rk,
                    "is_num_min": float(v is not None and v == nv[0]), "is_num_max": float(v is not None and v == nv[-1]),
                    "n_commas": float(o.count(","))})
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
            pred[te] = mk().fit(X[tr], y[tr]).predict(X[te])
        res[nm] = round(float((pred == y).mean()), 4)
    return res


def cv_choice(Xs, Xd, yp, prow, groups_p, rows):
    gkf = GroupKFold(n_splits=5); res = {}; per_b = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        sc = np.zeros(len(yp))
        for tr, te in gkf.split(X, yp, groups_p):
            sc[te] = mk().fit(X[tr], yp[tr]).predict_proba(X[te])[:, 1]
        by = {}
        for i, (ri, s) in enumerate(zip(prow, sc)):
            by.setdefault(ri, []).append((round(float(s), 9), yp[i]))
        accs = {}
        for ri, lst in by.items():
            top = max(s for s, _ in lst); tied = [g for s, g in lst if s == top]
            accs[ri] = sum(tied) / len(tied)
        res[nm] = round(float(np.mean(list(accs.values()))), 4)
        for ri, a in accs.items():
            per_b.setdefault((nm, L.bucket(len(rows[ri]["options"]))), []).append(a)
            if rows[ri]["meta"].get("subtype") == "inverted":
                per_b.setdefault((nm, "inverted"), []).append(a)
    return res, {f"{nm}:{b}": round(float(np.mean(v)), 4) for (nm, b), v in sorted(per_b.items())}


def yes_no_part(yn, side, out):
    y = np.array([int(r["gold"]) for r in yn]); g = [r["meta"]["card_id"] for r in yn]
    chance = 0.5; maj = float(max(y.mean(), 1 - y.mean()))
    V = [L.views(r) for r in yn]
    for key, field in (("a_question", "q"), ("c_card_without_question", "cardnoq")):
        tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
        Xs = tv.fit_transform([v[field] for v in V]).tocsr()
        Xd = TruncatedSVD(64, random_state=0).fit_transform(Xs)
        res = cv_yn(Xs, Xd, y, g); best = max(res.values())
        out["yes_no"][key] = {**res, "chance": chance, "majority_rate": round(maj, 4), "best": best,
                              "pass": best <= chance + 0.02}
        log(f"yn {key} {out['yes_no'][key]}")
    md = []
    for r in yn:
        c, n = L.meta_feats(r); md.append({**{f"{k}={v}": 1.0 for k, v in c.items()}, **n})
    dv = DictVectorizer(); Xm = dv.fit_transform(md).tocsr(); Xms = MaxAbsScaler().fit_transform(Xm)
    res = cv_yn(Xms, Xm.toarray(), y, g); best = max(res.values())
    out["yes_no"]["d_metadata"] = {**res, "chance": chance, "majority_rate": round(maj, 4), "best": best,
                                   "pass": best <= chance + 0.02, "n_features": Xm.shape[1]}
    log(f"yn d_metadata {out['yes_no']['d_metadata']}")
    out["yes_no"]["b_options"] = "n/a (yes/no options are fixed)"


def inv_blocks(r):
    """recheck fix (G0 6 G6 (b)): on inverted rows, the report block each case reference points to (from the option's
    first whole-word mention in `state` to the next option's mention); '' on other rows."""
    if r["meta"].get("subtype") != "inverted":
        return [""] * len(r["options"])
    st = r["state"]; pos = sorted((L.wb_find(st, o), i) for i, o in enumerate(r["options"]) if L.wb_find(st, o) >= 0)
    out = [""] * len(r["options"])
    for j, (p, i) in enumerate(pos):
        out[i] = st[p + len(r["options"][i]):(pos[j + 1][0] if j + 1 < len(pos) else len(st))]
    return out


def choice_part(ch, side, out):
    prow, yp, gp, otext, F = [], [], [], [], {"a": [], "b": [], "c": [], "d": []}
    btext = []
    for ri, r in enumerate(ch):
        v = L.views(r); os_ = optset_feats(r); c, n = L.meta_feats(r); lrk = list_rank(r, v["cardnoq"])
        blk = inv_blocks(r); bl = [len(b) for b in blk]
        mrow = {**{f"{k}={x}": 1.0 for k, x in c.items()}, **n}
        gi = L.gold_index(r)
        for i, o in enumerate(r["options"]):
            prow.append(ri); yp.append(int(i == gi)); gp.append(r["meta"]["card_id"]); otext.append(o)
            F["a"].append(sim_feats(o, v["q"]))
            btext.append(blk[i])
            F["b"].append({**os_[i], "blk_len": float(bl[i]), "blk_lines": float(blk[i].count("\n")),
                           "blk_nums": float(len(L.nums(blk[i]))),
                           "blk_len_rank": (sorted(bl, reverse=True).index(bl[i]) / max(1, len(bl) - 1)) if blk[i] else -1.0})
            F["c"].append({**sim_feats(o, v["cardnoq"]), **lrk[i]})
            dd = dict(mrow); dd.update({"o_" + k: x for k, x in os_[i].items()})
            for k, x in c.items():
                if k in ("format_style", "domain_pack", "wording_id"):
                    continue
                for ok in ("abstain", "is_longest", "is_num_min", "is_num_max"):
                    dd[f"x_{k}={x}_{ok}"] = os_[i][ok]
            F["d"].append(dd)
    yp = np.array(yp); log(f"choice pairs {len(yp)} rows {len(ch)}")
    chance = float(np.mean([1 / len(r["options"]) for r in ch]))
    cb = {}
    for r in ch:
        cb.setdefault(L.bucket(len(r["options"])), []).append(1 / len(r["options"]))
    cb = {b: round(float(np.mean(v)), 4) for b, v in cb.items()}
    tw = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, token_pattern=r"[^\s]+")
    tc = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, sublinear_tf=True, max_features=100000)
    Xo = sparse.hstack([tw.fit_transform(otext), tc.fit_transform(otext)]).tocsr()
    Xo_svd = TruncatedSVD(32, random_state=0).fit_transform(Xo)
    names = {"a": "a_question", "b": "b_options", "c": "c_card_without_question", "d": "d_metadata"}
    bn = Counter(L.bucket(len(r["options"])) for r in ch)
    inv = [r for r in ch if r["meta"].get("subtype") == "inverted"]
    if inv:
        bn["inverted"] = len(inv); cb["inverted"] = round(float(np.mean([1 / len(r["options"]) for r in inv])), 4)
    tb = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, max_features=100000)
    Xb = tb.fit_transform(btext).tocsr() if inv else None
    Xb_svd = TruncatedSVD(16, random_state=0).fit_transform(Xb) if inv else None
    for key in ("a", "b", "c", "d"):
        dv = DictVectorizer(); Xf = dv.fit_transform(F[key]).tocsr(); Xf = MaxAbsScaler().fit_transform(Xf)
        if key == "d":
            Xs = Xf; keep = [j for j, nm in enumerate(dv.feature_names_) if not nm.startswith("x_")]
            Xd = Xf[:, keep].toarray()
        elif key == "b" and inv:  # G0 6: on inverted rows (b) also reads the report blocks the options point to
            Xs = sparse.hstack([Xo, Xb, Xf]).tocsr(); Xd = np.hstack([Xf.toarray(), Xo_svd, Xb_svd])
        else:
            Xs = sparse.hstack([Xo, Xf]).tocsr(); Xd = np.hstack([Xf.toarray(), Xo_svd])
        res, perb = cv_choice(Xs, Xd, yp, prow, gp, ch); best = max(res.values())
        bfail = {}
        for kk, a in perb.items():
            bk = kk.split(":", 1)[1]
            if a > cb[bk] + 0.02:
                pv = float(binomtest(int(round(a * bn[bk])), bn[bk], cb[bk], alternative="greater").pvalue)
                if pv < 0.01:
                    bfail[kk] = {"acc": a, "chance": cb[bk], "n": bn[bk], "p": pv}
        out["choice"][names[key]] = {**res, "chance_mean_1_over_k": round(chance, 4), "best": best,
                                     "per_bucket": perb, "chance_per_bucket": cb, "per_bucket_rows": dict(bn),
                                     "per_bucket_fails": bfail, "pass": best <= chance + 0.02 and not bfail}
        log(f"choice {names[key]} {res} chance {chance:.4f} bfail {len(bfail)}")


def main():
    rows = L.load(NAME)
    yn = [r for r in rows if L.is_yn(r)]; ch = [r for r in rows if not L.is_yn(r)]
    log(f"rows {len(rows)} yes/no {len(yn)} choice {len(ch)}")
    out = {"gate": "G6", "file": f"out/{NAME}.jsonl", "cv": "GroupKFold(5) by meta.card_id",
           "rule": "acc <= chance + 2 pp", "n_rows": len(rows), "yes_no": {}, "choice": {}}
    yes_no_part(yn, None, out)
    choice_part(ch, None, out)
    allp = [v["pass"] for part in ("yes_no", "choice") for v in out[part].values() if isinstance(v, dict) and "pass" in v]
    out["pass"] = all(allp); out["seconds"] = round(time.time() - T0, 1)
    (L.QC / f"g6_{NAME}.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


if __name__ == "__main__":
    main()
