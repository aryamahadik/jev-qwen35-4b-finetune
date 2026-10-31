"""G6 partial-input and metadata baselines (independent F13 checker, check:F13, c-lanes-v3; adapted from the F12
checker's chk_g6.py). 5-fold GroupKFold by meta.card_id on out/qc_sample.jsonl (the separate QC sample, 5,750 rows from
the same generators). Models: logistic regression on TF-IDF word 1-2 grams; sklearn HistGradientBoosting on dense
features (SVD of the n-grams, or the metadata).
Views (F13 G0 10): question = instruction wording + question paragraph; card = card text (yes/no `card`; moved card text
in `instructions` on choice rows); options = option texts (+ definition lines); metadata = visible only
(chk_lib.meta_feats; FIX RULE "G6 metadata = only what the model sees"). Diagnostic d_plus adds the G0 10 structure
features (decisive deciles / count, near-miss kinds / deciles; chk_lib.g0_feats), reported, not gated in G6 (gated in G7).
Yes/no: predict gold from (a) question, (c) card without question, (d) visible metadata; chance = majority rate.
Choice: pointwise (row, option) scorer, argmax per row (ties split), chance = mean 1/k; per-option features:
(a) option n-grams + question mention, (b) option n-grams + option-set structure (length rank, longest / shortest,
abstain kinds, numeric rank, mention count class / max / first / last in the text, named in question / card),
(c) option n-grams + mentions in the card, (d) row visible metadata x option kind. b / d use option kinds read from the
text: STRICTER than literal "(b) options only" / "(d) metadata"; b_literal / d_literal reported as diagnostics.
Rule: accuracy <= chance + 2 pp for every gated view and model. Counts only. Usage: chk_g6.py [name]"""
import json, re, sys, time
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import MaxAbsScaler
import chk_lib as q

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
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
    out = {"gate": "G6", "file": f"out/{NAME}.jsonl", "pool_sha256": q.sha(q.OUT / f"{NAME}.jsonl"), "cv": "GroupKFold(5) by meta.card_id", "rule": "acc <= chance + 2 pp",
           "metadata": "visible only (chk_lib.meta_feats)", "views": "question = wording + question paragraph; card = card text wherever it sits; options incl. definition lines (F13 G0 10)", "yes_no": {}, "choice": {}}
    y = np.array([int(r["gold"]) for r in yn]); g = [r["meta"]["card_id"] for r in yn]
    chance = round(float(max(y.mean(), 1 - y.mean())), 4)
    V = [q.views(r, side.get(r["id"])) for r in yn]
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
    mdp = [{**d, **{f"g0_{k}={v}": 1.0 for k, v in q.g0_feats(side.get(r["id"])).items()}} for d, r in zip(md, yn)]
    Xp = DictVectorizer().fit_transform(mdp).tocsr()
    res = cv_yn(MaxAbsScaler().fit_transform(Xp), Xp.toarray(), y, g)
    out["diag_d_plus_g0_structure"] = {"yes_no": {**res, "chance": chance, "within_2pp": max(res.values()) <= chance + 0.02}}
    log(f"yn d_plus {out['diag_d_plus_g0_structure']}")
    prow, yp, gp, otext = [], [], [], []
    F = {"a": [], "b": [], "c": [], "d": [], "b2": [], "d2": []}
    POSK = ("kind:mention0", "kind:mention1", "kind:mention2p", "kind:mention_max", "kind:first_in_text",
            "kind:last_in_text", "kind:in_question", "kind:in_card")
    for ri, r in enumerate(ch):
        s = side.get(r["id"]) or {}; v = q.views(r, s); kinds = q.opt_kinds(r, s, v); opts = r["options"]; k = len(opts)
        L = [len(o) for o in opts]; rank = np.argsort(np.argsort(-np.array(L), kind="stable"))
        c, n = q.meta_feats(r, s); mrow = {**{f"{a}={b}": 1.0 for a, b in c.items()}, **n}
        ql, cl = v["q"].lower(), v["cardnoq"].lower()
        for i, o in enumerate(opts):
            ol = o.lower()
            prow.append(ri); yp.append(int(o == r["gold"])); gp.append(r["meta"]["card_id"]); otext.append(v["opts"][i])
            F["a"].append({"q_mention": float(ol in ql)})
            b = {"k": float(k), "len": float(L[i]), "len_rank": float(rank[i]) / max(1, k - 1),
                 "len_z": float((L[i] - np.mean(L)) / (np.std(L) + 1e-6))}
            b.update({kd: 1.0 for kd in kinds[i]}); F["b"].append(b)
            F["c"].append({"c_mention": float(cl.count(ol))})
            dd = dict(mrow); dd.update({"o_" + a: x for a, x in b.items()})
            for kd in kinds[i]:
                for a in ("sampler", "sc_form", "subtype", "sc_world", "sc_kind", "lbin", "attack"):
                    dd[f"x_{a}={c.get(a)}_{kd}"] = 1.0
            F["d"].append(dd)
            b2 = {a: x for a, x in b.items() if a not in POSK}; F["b2"].append(b2)
            d2 = {a: x for a, x in dd.items() if not any(pk in a for pk in POSK)}; F["d2"].append(d2)
    yp = np.array(yp); log(f"choice pairs {len(yp)}")
    chance_c = round(float(np.mean([1 / len(r["options"]) for r in ch])), 4)
    Xo = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit_transform(otext).tocsr()
    Xo_svd = TruncatedSVD(32, random_state=0).fit_transform(Xo)
    names = {"a": "a_question", "b": "b_options", "c": "c_card_without_question", "d": "d_metadata",
             "b2": "b_options_literal", "d2": "d_metadata_literal"}
    out["choice_diag_literal"] = {}
    for key in ("a", "b", "c", "d", "b2", "d2"):
        dv = DictVectorizer(); Xf = MaxAbsScaler().fit_transform(dv.fit_transform(F[key]).tocsr())
        if key in ("d", "d2"):
            Xs = Xf; keep = [j for j, nm in enumerate(dv.feature_names_) if not nm.startswith("x_")]; Xd = Xf[:, keep].toarray()
        else:
            Xs = sparse.hstack([Xo, Xf]).tocsr(); Xd = np.hstack([Xf.toarray(), Xo_svd])
        res = cv_ch(Xs, Xd, yp, prow, gp); best = max(res.values())
        tgt = out["choice_diag_literal"] if key in ("b2", "d2") else out["choice"]
        tgt[names[key]] = {**res, "chance_mean_1_over_k": chance_c, "best": best, "pass": best <= chance_c + 0.02}
        log(f"choice {names[key]} {tgt[names[key]]}")
    flat = [v["pass"] for part in ("yes_no", "choice") for v in out[part].values() if isinstance(v, dict)]
    out["pass"] = all(flat); out["seconds"] = round(time.time() - T0, 1)
    (q.QC / f"g6_{NAME}.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


if __name__ == "__main__":
    main()
