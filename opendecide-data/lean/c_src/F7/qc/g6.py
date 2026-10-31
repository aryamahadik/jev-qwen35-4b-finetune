"""G6 partial-input and metadata baselines (independent F7 checker). C_DATA_SPEC 8 G6 + F7 G0 4.6 (R08, L13) and 6.5.
5-fold CV grouped by meta.card_id (GroupKFold; random KFold reported only) on out/qc_sample.jsonl (separate QC sample
from the same samplers). Label = gold level index 0..K-1. Chance = mean over rows of 1/K (= the majority-class rate
when gold is uniform per card); bar = chance + 0.02. Models: logistic regression on word 1-2 gram TF-IDF (one-hot
for metadata) and HistGradientBoosting on dense features (64-d SVD of the n-grams for text views).
Views (F7 G0 4.6):
 (a) question only = `state` + the row-level wording and question of `instructions` (no card content, no options);
 (b) options only = the option texts, no definitions: pointwise option model (option n-grams + position j/(K-1),
     end-level flags, K, length rank), top-scored option per row is the prediction;
 (c) card only = `card` option-definition lines + the card content moved into `instructions` (paragraphs present on
     >= 50% of the card's rows: C-lines, rubric, worked cases); no state, wording or question;
 (d) metadata only: features the model can see in the prompt (task rule): K, mode, defs style, container, format
     style, wording, label form, defs variant, few-shot template, pack (name pool), depth / deep (card-level), lengths,
     option lengths, line / number counts, number magnitudes, attack present, absence-word count and negcount k_all
     over `state`, number of option names / numbers found in `state`;
 (e) option x case cues (G0 6.5: gold level name / synonym or the gold level's number as a digit in the case text):
     pointwise option model on [name word in state, number digit in state, position, K]. Gated like (a)-(d).
Hidden or label-derived meta (sampler, row_kind, twin_kind, edge, case_features) is reported in (d_hidden_info) only.
Usage: g6.py [qc_sample]"""
import json, re, sys, time
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold, KFold
from sklearn.preprocessing import MaxAbsScaler
from scipy.sparse import hstack, csr_matrix
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
T0 = time.time()
sys.path.insert(0, str(L.LEAN / "c_src/common"))
import negcount  # noqa: E402


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def kall(t):
    try:
        r = negcount.count(t)
        return float(r.get("k_all", 0) if isinstance(r, dict) else getattr(r, "k_all", 0))
    except Exception:  # noqa: BLE001
        return -1.0


def lr():
    return LogisticRegression(C=1.0, max_iter=3000)


def gbt(cls=True):
    return HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def splits(n, groups):
    return (("grouped", list(GroupKFold(n_splits=5).split(np.zeros(n), np.zeros(n), groups))),
            ("random", list(KFold(n_splits=5, shuffle=True, random_state=0).split(np.zeros(n)))))


def cv_rows(Xs, Xd, y, groups):
    res = {}
    for fold_nm, sp in splits(len(y), groups):
        for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
            pred = np.zeros(len(y))
            for tr, te in sp:
                if len(set(y[tr])) < 2:
                    pred[te] = y[tr][0]; continue
                pred[te] = mk().fit(X[tr], y[tr]).predict(X[te])
            res[f"{nm}_{fold_nm}"] = round(float((pred == y).mean()), 4)
    return res


def cv_options(Xs, Xd, lab, prow, groups_rows, n_rows):
    """pointwise option model; a row is right when its top-scored option is gold (random tie-break)."""
    res = {}; rng = np.random.default_rng(0)
    for fold_nm, sp in splits(n_rows, groups_rows):
        for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
            right = np.zeros(n_rows)
            for tr, te in sp:
                trm = np.isin(prow, tr); tem = np.isin(prow, te)
                m = mk().fit(X[trm], lab[trm])
                s = m.predict_proba(X[tem])[:, 1] + rng.random(int(tem.sum())) * 1e-9
                pr, lb = prow[tem], lab[tem]
                order = np.lexsort((-s, pr)); ps = pr[order]
                top = order[np.flatnonzero(np.r_[True, ps[1:] != ps[:-1]])]
                right[pr[top]] = lb[top]
            res[f"{nm}_{fold_nm}"] = round(float(right.mean()), 4)
    return res


def text_view(tx, y, groups):
    Xs = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, token_pattern=r"[A-Za-z0-9'-]+").fit_transform(tx)
    Xd = TruncatedSVD(n_components=min(64, Xs.shape[1] - 1), random_state=0).fit_transform(Xs)
    return cv_rows(Xs, Xd, y, groups)


def name_in(name, st_low):
    ws = [w for w in L.toks(name) if len(w) >= 3]
    return float(any(re.search(r"\b" + re.escape(w) + r"\b", st_low) for w in ws)) if ws else 0.0


def main():
    rows = L.load(NAME); n = len(rows)
    y = np.array([L.level(r) for r in rows]); Ks = np.array([L.K(r) for r in rows])
    groups = np.array([r["meta"]["card_id"] for r in rows])
    chance = round(float(np.mean(1.0 / Ks)), 4); bar = round(chance + 0.02, 4)
    maj = round(max(Counter(y.tolist()).values()) / n, 4)
    cp = L.card_paras(rows)
    out = {"set": NAME, "n": n, "cards": len(set(groups)), "chance_mean_1_over_K": chance, "majority_rate": maj,
           "bar": bar, "folds": "GroupKFold(5) by card_id (gated); KFold(5, shuffle, seed 0) reported only"}
    split = [L.split_ins(r, cp) for r in rows]
    out["a_question"] = text_view([r["state"] + "\n\n" + s[1] for r, s in zip(rows, split)], y, groups); log(f"a {out['a_question']}")
    out["c_card"] = text_view([((r.get("card") or "") + "\n\n" + s[0]).strip() for r, s in zip(rows, split)], y, groups); log(f"c {out['c_card']}")
    # (b) options only and (e) option x case cues: pointwise
    otext, odense, ecue, lab, prow = [], [], [], [], []
    for i, r in enumerate(rows):
        k = len(r["options"]); st = r["state"].lower(); lens = [len(o) for o in r["options"]]
        rk = {j: sorted(range(k), key=lambda t: (-lens[t], t)).index(j) for j in range(k)}
        for j, o in enumerate(r["options"]):
            otext.append(o)
            pos = {"pos": j / (k - 1), "first": float(j == 0), "last": float(j == k - 1), "K": float(k),
                   "len": float(len(o)), "len_rank": float(rk[j]), "longest": float(rk[j] == 0)}
            odense.append(pos)
            num = L.opt_num(o)
            ecue.append(dict(pos, name_in_state=name_in(L.opt_name(o), st),
                             num_in_state=float(bool(num) and re.search(r"(?<![\d.])" + num + r"(?![\d.])", st) is not None)))
            lab.append(int(o == r["gold"])); prow.append(i)
    lab = np.array(lab); prow = np.array(prow)
    Xt = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, token_pattern=r"[A-Za-z0-9'-]+").fit_transform(otext)
    dvb = DictVectorizer(sparse=False); Db = dvb.fit_transform(odense)
    Xb = hstack([Xt, csr_matrix(MaxAbsScaler().fit_transform(Db))]).tocsr()
    out["b_options"] = cv_options(Xb, Db, lab, prow, groups, n); log(f"b {out['b_options']}")
    dve = DictVectorizer(sparse=False); De = dve.fit_transform(ecue)
    out["e_option_x_case"] = cv_options(csr_matrix(MaxAbsScaler().fit_transform(De)), De, lab, prow, groups, n)
    out["e_rates"] = {"rows_with_any_name_in_state": int(sum(1 for i in range(n) if any(De[prow == i][:, dve.vocabulary_["name_in_state"]]))),
                      "rows_gold_name_in_state": int(De[(lab == 1)][:, dve.vocabulary_["name_in_state"]].sum()),
                      "rows_with_any_num_in_state": int(sum(1 for i in range(n) if any(De[prow == i][:, dve.vocabulary_["num_in_state"]]))),
                      "rows_gold_num_in_state": int(De[(lab == 1)][:, dve.vocabulary_["num_in_state"]].sum())}
    log(f"e {out['e_option_x_case']} {out['e_rates']}")
    # (d) visible metadata
    D, H = [], []
    for r in rows:
        m = r["meta"]; st = r["state"]; nu = L.nums(st); mag = [np.log10(abs(x)) if x else 0.0 for x in nu]
        ol = [len(o) for o in r["options"]]; stl = st.lower()
        cat = {"K": str(len(r["options"])), "mode": m.get("mode"), "defs": m.get("defs_style"), "container": m.get("container"),
               "style": m.get("format_style"), "wording": m.get("wording_id"), "label_form": m.get("label_form"),
               "defs_variant": str(m.get("defs_variant")), "fewshot": str(m.get("fewshot_template")),
               "pack": m.get("domain_pack"), "deep": str(m.get("deep")),
               "attack": str(bool((m.get("case_features") or {}).get("injected")))}
        num = {"depth": float(m.get("depth") or 0), "len_state": len(st), "len_ins": len(r["instructions"]),
               "len_card": len(r.get("card") or ""), "n_lines": st.count("\n"), "n_nums": len(nu),
               "mag_max": max(mag) if mag else -1.0, "mag_min": min(mag) if mag else -1.0,
               "mag_mean": float(np.mean(mag)) if mag else -1.0, "num_last": float(nu[-1]) if nu else -1.0,
               "opt_len_max": max(ol), "opt_len_mean": float(np.mean(ol)), "opt_len_sd": float(np.std(ol)),
               "n_absence_words": len(L.NEG_RX.findall(st)), "kall_state": kall(st),
               "n_words_state": len(L.toks(st)),
               "n_names_in_state": sum(name_in(L.opt_name(o), stl) for o in r["options"])}
        D.append(dict(**cat, **{k: float(v) for k, v in num.items()}))
        cf = m.get("case_features") or {}
        H.append(dict(D[-1], sampler=m["sampler"], row_kind=m.get("row_kind"), twin_kind=str(m.get("twin_kind")),
                      **{f"cf_{k}": (str(v) if not isinstance(v, (int, float)) or isinstance(v, bool) else float(v))
                         for k, v in cf.items()}))
    for key, rec in (("d_meta", D), ("d_hidden_info", H)):
        dv = DictVectorizer(); Xs = MaxAbsScaler().fit_transform(dv.fit_transform(rec)).tocsr()
        Xd = DictVectorizer(sparse=False).fit_transform(rec)
        out[key] = cv_rows(Xs, Xd, y, groups); out[key + "_n_features"] = len(dv.feature_names_); log(f"{key} {out[key]}")
    gated = {f"{v}.{k}": a for v in ("a_question", "b_options", "c_card", "d_meta", "e_option_x_case")
             for k, a in out[v].items() if k.endswith("grouped")}
    out["gated"] = gated; out["max_gated"] = max(gated.values())
    out["pass"] = all(a <= bar for a in gated.values())
    out["hidden_info_grouped_max"] = max(a for k, a in out["d_hidden_info"].items() if k.endswith("grouped"))
    json.dump(out, open(L.QC / f"g6_{NAME}.json", "w"), indent=1)
    log(f"pass={out['pass']} max={out['max_gated']} bar={bar}")


if __name__ == "__main__":
    main()
