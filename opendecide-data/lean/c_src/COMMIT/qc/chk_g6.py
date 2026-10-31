"""G6 partial-input and metadata baselines (independent COMMIT checker, check:COMMIT, c-lanes-v3). 5-fold GroupKFold
on out/qc_sample.jsonl (the separate QC sample from the same generators; commits disjoint from training rows).
Grouping: by meta.card_id (orchestrator task text) and, as the G0 9 rule states, by repo group (sidecar repo_group);
both are run and both must pass. Message-only rows are their own group (v4 B1): every view runs separately on
diff-view and message-only rows, for yes/no and for choice. (d) also runs per commit type x qtype (G0 8 Sources, A58).
Models: logistic regression on TF-IDF word 1-2 grams; sklearn HistGradientBoosting on dense features (SVD of the
n-grams, or the metadata).
Yes/no: predict gold from (a) question paragraph, (c) visible card + instructions without the question, (d) metadata
(chk_lib.meta_feats); chance = majority rate; (b) n/a.
Choice: pointwise (row, option) scorer, argmax per row (ties split), chance = mean 1/k; per-option features:
(a) option-line n-grams + question mention, (b) option-line n-grams + option-set structure (length rank, longest /
shortest, definition shown), (c) option-line n-grams + mention count in visible card-without-question, (d) row
metadata x option kind. Option text = the option line decoder_io prints (option + card definition).
Rule: accuracy <= chance + 2 pp for every view, model and slice with >= 50 rows (smaller slices reported, n/a).
Counts only. Usage: chk_g6.py [name]"""
import json, sys, time
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

NAME = ([a for a in sys.argv[1:] if not a.startswith("--")] or ["qc_sample"])[0]
T0 = time.time()
N_MIN = 50


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def lr():
    return LogisticRegression(C=1.0, max_iter=3000, solver="liblinear")


def gbt():
    return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def folds(g):
    return min(5, len(set(g)))


def cv_yn(Xs, Xd, y, g):
    res = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        pred = np.zeros(len(y))
        for tr, te in GroupKFold(folds(g)).split(X, y, g):
            if len(set(y[tr])) < 2:
                pred[te] = y[tr][0]; continue
            pred[te] = mk().fit(X[tr], y[tr]).predict(X[te])
        res[nm] = round(float((pred == y).mean()), 4)
    return res


def cv_ch(Xs, Xd, yp, prow, g):
    res = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        sc = np.zeros(len(yp))
        for tr, te in GroupKFold(folds(g)).split(X, yp, g):
            sc[te] = mk().fit(X[tr], yp[tr]).predict_proba(X[te])[:, 1]
        by = {}
        for i, (ri, s) in enumerate(zip(prow, sc)):
            by.setdefault(ri, []).append((round(float(s), 9), yp[i]))
        acc = []
        for lst in by.values():
            top = max(s for s, _ in lst); tied = [t for s, t in lst if s == top]; acc.append(sum(tied) / len(tied))
        res[nm] = round(float(np.mean(acc)), 4)
    return res


def verdict(res, chance, n):
    best = max(res.values())
    return {**res, "chance": chance, "best": best, "n": n,
            "pass": (best <= chance + 0.02) if n >= N_MIN else None}


def tfidf(texts):
    tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200000, sublinear_tf=True)
    Xs = tv.fit_transform(texts).tocsr()
    nc = max(2, min(64, Xs.shape[1] - 1, Xs.shape[0] - 1))
    return Xs, TruncatedSVD(nc, random_state=0).fit_transform(Xs)


def meta_dicts(rs, side):
    md = []
    for r in rs:
        c, n = q.meta_feats(r, side.get(r["id"])); md.append({**{f"{k}={v}": 1.0 for k, v in c.items()}, **n})
    return md


def run_yn(rs, side, gkey, only_d=False):
    y = np.array([int(r["gold"]) for r in rs]); g = [gkey(r) for r in rs]
    chance = round(float(max(y.mean(), 1 - y.mean())), 4); out = {}
    if not only_d:
        V = [q.views(r) for r in rs]
        for key, f in (("a_question", "q"), ("c_card_without_question", "cardnoq")):
            Xs, Xd = tfidf([v[f] for v in V])
            out[key] = verdict(cv_yn(Xs, Xd, y, g), chance, len(rs))
    Xm = DictVectorizer().fit_transform(meta_dicts(rs, side)).tocsr()
    out["d_metadata"] = verdict(cv_yn(MaxAbsScaler().fit_transform(Xm), Xm.toarray(), y, g), chance, len(rs))
    return out


def opt_kinds(r):
    so = q.shown_opts(r); ls = [len(o) for o in so]; d = q.opt_defs(r); out = []
    for i, o in enumerate(r["options"]):
        k = set()
        if ls[i] == max(ls): k.add("kind:longest")
        if ls[i] == min(ls): k.add("kind:shortest")
        if o in d: k.add("kind:def_visible")
        out.append(k)
    return out


def run_ch(rs, side, gkey, only_d=False):
    prow, yp, gp, otext = [], [], [], []
    F = {"a": [], "b": [], "c": [], "d": []}
    for ri, r in enumerate(rs):
        s = side.get(r["id"]) or {}; v = q.views(r); kinds = opt_kinds(r); so = v["opts"]; k = len(so)
        L = [len(o) for o in so]; rank = rankdata(-np.array(L), method="average") - 1
        c, n = q.meta_feats(r, s); mrow = {**{f"{a}={b}": 1.0 for a, b in c.items()}, **n}
        ql, cl = v["q"].lower(), v["cardnoq"].lower()
        for i, o in enumerate(r["options"]):
            ol = o.lower()
            prow.append(ri); yp.append(int(i == q.gold_index(r))); gp.append(gkey(r)); otext.append(so[i])
            F["a"].append({"q_mention": float(ol in ql)})
            b = {"k": float(k), "len": float(L[i]), "len_rank": float(rank[i]) / max(1, k - 1),
                 "len_z": float((L[i] - np.mean(L)) / (np.std(L) + 1e-6))}
            b.update({kd: 1.0 for kd in kinds[i]}); F["b"].append(b)
            F["c"].append({"c_mention": float(cl.count(ol))})
            dd = dict(mrow); dd.update({"o_" + a: x for a, x in b.items()})
            for kd in kinds[i]:
                for a in ("sc_commit_type", "sc_card_form", "sampler", "input_view"):
                    dd[f"x_{a}={c.get(a)}_{kd}"] = 1.0
            F["d"].append(dd)
    yp = np.array(yp)
    chance = round(float(np.mean([1 / len(r["options"]) for r in rs])), 4)
    Xo = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit_transform(otext).tocsr()
    Xo_svd = TruncatedSVD(max(2, min(32, Xo.shape[1] - 1)), random_state=0).fit_transform(Xo)
    names = {"a": "a_question", "b": "b_options", "c": "c_card_without_question", "d": "d_metadata"}
    out = {}
    for key in (("d",) if only_d else ("a", "b", "c", "d")):
        dv = DictVectorizer(); Xf = MaxAbsScaler().fit_transform(dv.fit_transform(F[key]).tocsr())
        if key == "d":
            Xs = Xf; keep = [j for j, nm in enumerate(dv.feature_names_) if not nm.startswith("x_")]; Xd = Xf[:, keep].toarray()
        else:
            Xs = sparse.hstack([Xo, Xf]).tocsr(); Xd = np.hstack([Xf.toarray(), Xo_svd])
        out[names[key]] = verdict(cv_ch(Xs, Xd, yp, prow, gp), chance, len(rs))
    return out


def main():
    rows, side = q.load(NAME)
    out = {"gate": "G6", "file": f"out/{NAME}.jsonl", "pool_sha256": q.sha(q.OUT / f"{NAME}.jsonl"),
           "cv": "GroupKFold(5) by meta.card_id and by repo_group (both gated)", "rule": "acc <= chance + 2 pp (slices >= 50 rows)",
           "metadata": "visible + spec-listed design fields only (chk_lib.meta_feats)", "rows": len(rows),
           "floors": {}, "results": {}}
    ct = {}
    for r in rows:
        ct.setdefault(q.ctype(r, side), [0, 0]); ct[q.ctype(r, side)][0] += 1
        ct[q.ctype(r, side)][1] += int(q.view(r) == "message_only")
    mo = sum(v[1] for v in ct.values())
    out["floors"] = {"rows": len(rows), "rows_ge_5000": len(rows) >= 5000, "per_type": {k: v[0] for k, v in ct.items()},
                     "per_type_ge_1000": all(v[0] >= 1000 for v in ct.values()),
                     "message_only": mo, "message_only_ge_1000": mo >= 1000,
                     "message_only_per_type": {k: v[1] for k, v in ct.items() if k in ("route", "triage", "gate")},
                     "message_only_per_type_ge_334": all(ct.get(k, [0, 0])[1] >= 334 for k in ("route", "triage", "gate"))}
    gkeys = {"card": lambda r: r["meta"]["card_id"], "repo": lambda r: (side.get(r["id"]) or {}).get("repo_group")}
    for gname, gk in gkeys.items():
        R = out["results"].setdefault(gname, {})
        for vw in ("message_diff", "message_only"):
            yn = [r for r in rows if q.is_yn(r) and q.view(r) == vw]; ch = [r for r in rows if not q.is_yn(r) and q.view(r) == vw]
            if len(yn) >= 10:
                R[f"yes_no/{vw}"] = run_yn(yn, side, gk); log(f"{gname} yn {vw} n={len(yn)} {json.dumps(R[f'yes_no/{vw}'])[:300]}")
            if len(ch) >= 10:
                R[f"choice/{vw}"] = run_ch(ch, side, gk); log(f"{gname} ch {vw} n={len(ch)} {json.dumps(R[f'choice/{vw}'])[:300]}")
        for t in sorted(ct):
            for part in ("yes_no", "choice"):
                rs = [r for r in rows if q.ctype(r, side) == t and q.is_yn(r) == (part == "yes_no")]
                if len(rs) >= 10:
                    R[f"d_per_type/{t}/{part}"] = (run_yn if part == "yes_no" else run_ch)(rs, side, gk, only_d=True)
                    log(f"{gname} d {t} {part} n={len(rs)} {json.dumps(R[f'd_per_type/{t}/{part}'])[:200]}")
    fails = []
    for gname, R in out["results"].items():
        for sl, views in R.items():
            for vk, v in views.items():
                if v.get("pass") is False:
                    fails.append({"group": gname, "slice": sl, "view": vk, "best": v["best"], "chance": v["chance"], "n": v["n"]})
    out["fails"] = fails
    out["underpowered_slices_n_lt_50"] = sorted({f"{g}:{sl}" for g, R in out["results"].items() for sl, vv in R.items()
                                                 for v in vv.values() if v.get("pass") is None})
    out["pass_baselines"] = not fails
    out["pass_floors"] = out["floors"]["rows_ge_5000"] and out["floors"]["per_type_ge_1000"] and out["floors"]["message_only_ge_1000"]
    out["pass"] = out["pass_baselines"] and out["pass_floors"]
    out["seconds"] = round(time.time() - T0, 1)
    (q.QC / f"g6_{NAME}.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']} baselines={out['pass_baselines']} floors={out['pass_floors']} fails={len(fails)}")


if __name__ == "__main__":
    main()
