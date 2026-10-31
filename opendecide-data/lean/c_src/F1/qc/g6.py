"""G6 partial-input and metadata baselines (independent F1 checker). 5-fold GroupKFold by meta.card_id on
out/qc_sample.jsonl (5,102 rows; the drawn per-card yes rates of spec 2.1 cannot transfer across folds).
Models: logistic regression on TF-IDF word 1-2 grams; sklearn HistGradientBoosting on dense features (SVD of the
n-grams, or the metadata). Yes/no: predict gold from (a) question paragraph, (c) card + instructions without the
question, (d) metadata (row meta + non-label sidecar, incl. X_role / option-role counts); chance = majority rate.
Choice: pointwise (row, option) scorer, argmax per row (ties split), chance = mean 1/k; per-option features:
(a) option n-grams + question mention, (b) option n-grams + option-set structure (length rank, how many sibling
options share this option's outcome part / basis part, abstain), (c) option n-grams + mentions in card-without-
question, (d) row metadata x option role (default / escalate / fallback / M / cbd / none / case / other).
Rule: accuracy <= chance + 2 pp for every view and model. Counts only."""
import json, re, sys, time
from collections import Counter
import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import MaxAbsScaler
import qc_lib as q

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
T0 = time.time()
SEP = re.compile(r"\s+(?:via|under|/ basis|with basis|on basis)\s+", re.I)


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


def split_opt(o):
    p = SEP.split(o, maxsplit=1)
    return (p[0].strip().lower(), p[1].strip().lower()) if len(p) == 2 else (o.strip().lower(), "")


def optset(r, roles):
    opts = r["options"]; k = len(opts); L = [len(o) for o in opts]
    rank = np.argsort(np.argsort(-np.array(L), kind="stable"))
    parts = [split_opt(o) for o in opts]
    out = []
    for i, o in enumerate(opts):
        a, b = parts[i]
        out.append({"k": float(k), "len": float(L[i]), "len_rank": float(rank[i]) / max(1, k - 1),
                    "is_longest": float(L[i] == max(L)), "is_shortest": float(L[i] == min(L)),
                    "len_z": (L[i] - np.mean(L)) / (np.std(L) + 1e-6),
                    "share_outcome": float(sum(1 for j, p in enumerate(parts) if j != i and p[0] == a)),
                    "share_basis": float(sum(1 for j, p in enumerate(parts) if j != i and b and p[1] == b)),
                    "basis_is_code": float(b.startswith("code")), "has_basis": float(bool(b)),
                    "abstain_text": float(bool(re.match(r"(undetermined|cannot be determined|the file does not settle|none of these|no listed case)", o.lower())))})
    return out


def main():
    rows, side = q.load(NAME)
    yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
    log(f"rows {len(rows)} yn {len(yn)} choice {len(ch)}")
    out = {"gate": "G6", "file": f"out/{NAME}.jsonl", "cv": "GroupKFold(5) by meta.card_id",
           "rule": "acc <= chance + 2 pp", "yes_no": {}, "choice": {}}
    y = np.array([int(r["gold"]) for r in yn]); g = [r["meta"]["card_id"] for r in yn]
    chance = round(float(max(y.mean(), 1 - y.mean())), 4)
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
    dv = DictVectorizer(); Xm = dv.fit_transform(md).tocsr()
    res = cv_yn(MaxAbsScaler().fit_transform(Xm), Xm.toarray(), y, g); best = max(res.values())
    out["yes_no"]["d_metadata"] = {**res, "chance": chance, "best": best, "pass": best <= chance + 0.02}
    log(f"yn d {out['yes_no']['d_metadata']}")
    # diagnostic: X_role alone, and metadata without X_role
    xr = [{"xr=" + str((side.get(r["id"]) or {}).get("X_role")): 1.0} for r in yn]
    Xx = DictVectorizer().fit_transform(xr).tocsr()
    out["yes_no"]["diag_X_role_only"] = cv_yn(Xx, Xx.toarray(), y, g)
    md2 = [{k: v for k, v in d.items() if not k.startswith("sc_X_role")} for d in md]
    dv2 = DictVectorizer(); X2 = dv2.fit_transform(md2).tocsr()
    out["yes_no"]["diag_metadata_without_X_role"] = cv_yn(MaxAbsScaler().fit_transform(X2), X2.toarray(), y, g)
    log(f"yn diag {out['yes_no']['diag_X_role_only']} {out['yes_no']['diag_metadata_without_X_role']}")
    out["yes_no"]["b_options"] = "n/a (yes/no options fixed)"
    choice_part(ch, side, out)
    flat = [v["pass"] for part in ("yes_no", "choice") for k, v in out[part].items() if isinstance(v, dict) and "pass" in v]
    out["pass"] = all(flat); out["seconds"] = round(time.time() - T0, 1)
    (q.QC / f"g6_{NAME}.json").write_text(json.dumps(out, indent=1))
    log(f"done pass={out['pass']}")


def choice_part(ch, side, out):
    prow, yp, gp, otext = [], [], [], []
    F = {"a": [], "b": [], "c": [], "d": []}
    for ri, r in enumerate(ch):
        s = side.get(r["id"]) or {}; v = q.views(r); roles = s.get("option_roles") or ["?"] * len(r["options"])
        os_ = optset(r, roles); c, n = q.meta_feats(r, s)
        mrow = {**{f"{k}={x}": 1.0 for k, x in c.items()}, **n}
        ql, cl = v["q"].lower(), v["cardnoq"].lower()
        for i, o in enumerate(r["options"]):
            ol = o.lower(); a, b = split_opt(o)
            prow.append(ri); yp.append(int(o == r["gold"])); gp.append(r["meta"]["card_id"]); otext.append(o)
            F["a"].append({"q_mention": float(ol in ql), "q_mention_outcome": float(a in ql)})
            F["b"].append(os_[i])
            F["c"].append({"c_mention": float(cl.count(ol)), "c_mention_outcome": float(cl.count(a)),
                           "c_mention_basis": float(cl.count(b)) if b else 0.0})
            dd = dict(mrow); dd.update({"o_" + k: x for k, x in os_[i].items()})
            dd["role=" + str(roles[i])] = 1.0
            for k in ("sc_world", "sc_policy", "sc_qtype", "sc_tie"):
                dd[f"x_{k}={c.get(k)}_role={roles[i]}"] = 1.0
            F["d"].append(dd)
    yp = np.array(yp); log(f"choice pairs {len(yp)}")
    chance = round(float(np.mean([1 / len(r["options"]) for r in ch])), 4)
    tw = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    Xo = tw.fit_transform(otext).tocsr(); Xo_svd = TruncatedSVD(32, random_state=0).fit_transform(Xo)
    names = {"a": "a_question", "b": "b_options", "c": "c_card_without_question", "d": "d_metadata"}
    for key in ("a", "b", "c", "d"):
        dv = DictVectorizer(); Xf = MaxAbsScaler().fit_transform(dv.fit_transform(F[key]).tocsr())
        if key == "d":
            Xs = Xf; keep = [j for j, nm in enumerate(dv.feature_names_) if not nm.startswith("x_")]
            Xd = Xf[:, keep].toarray()
        else:
            Xs = sparse.hstack([Xo, Xf]).tocsr(); Xd = np.hstack([Xf.toarray(), Xo_svd])
        res = cv_ch(Xs, Xd, yp, prow, gp); best = max(res.values())
        out["choice"][names[key]] = {**res, "chance_mean_1_over_k": chance, "best": best, "pass": best <= chance + 0.02}
        log(f"choice {names[key]} {out['choice'][names[key]]}")
    # diagnostic: option role alone
    rf = DictVectorizer().fit_transform([{"role=" + k.split("role=")[-1]: 1.0} if False else
                                         {kk: vv for kk, vv in d.items() if kk.startswith("role=")} for d in F["d"]]).tocsr()
    out["choice"]["diag_role_only"] = cv_ch(rf, rf.toarray(), yp, prow, gp)
    log(f"choice diag role {out['choice']['diag_role_only']}")


if __name__ == "__main__":
    main()
