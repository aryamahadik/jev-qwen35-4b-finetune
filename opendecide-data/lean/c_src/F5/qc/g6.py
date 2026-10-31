"""G6 partial-input and metadata baselines (independent F5 checker). C_DATA_SPEC 8 G6 + F5 G0 sec 9.
5-fold CV grouped by meta.card_id (F5 G0 9: a card's rows never span folds; random-fold accuracy reported, not gated)
on out/qc_sample.jsonl. Every F5 row is yes/no, chance = 0.5. Models: logistic regression on word 1-2 gram TF-IDF
(sparse one-hot for metadata) and HistGradientBoosting on dense features (64-d SVD of the n-grams for text views).
Views: (a) question only (sentences of `instructions` with '?'); (b) options only (always Yes/No: chance by
construction); (c) card without question (card + the non-question wording of `instructions`); (d) metadata only
(spec list + F5 G0 9 additions from the sidecar; label-derived fields gold, v_P, pair_change never used).
Pass: every gated accuracy <= 0.52. Usage: g6.py [qc_sample]"""
import json, sys, time
import numpy as np
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold, KFold
from sklearn.preprocessing import MaxAbsScaler
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
T0 = time.time()


def log(m):
    print(f"[{time.time() - T0:7.1f}s] {m}", flush=True)


def meta_feats(r, s, attacked):
    m = r["meta"]; st = r["state"]; nu = L.nums(st)
    mag = [np.log10(abs(x)) if x else 0.0 for x in nu]
    cat = {"sampler": m["sampler"], "wording": m["wording_id"], "style": m["format_style"], "defs": m["defs_style"],
           "pack": m["domain_pack"], "row_type": s["row_type"], "template": s["template"], "core": s["core"],
           "frame": str(s["frame"]), "frame_id": str(s["frame_id"]), "location": s["location"],
           "world": s["world_cell"], "card_form": s["card_form"], "tag_P": str(s["tag_P"]),
           "polarity_P": str(s["polarity_P"]), "yes_is_bad": str(s["yes_is_bad"]), "no_pol": str(s["no_polarity"]),
           "inverted": str(s["inverted"]), "fewshot": str(s["fewshot"]), "decoy": str(s["decoy"]),
           "two_lcore": str(s["two_lcore"]), "vcore": str(s["vcore"]), "attack_push": str(s["attack_push"]),
           "base_attacked": str(attacked), "pair_member": str(s["pair_member"]), "deep": str(m.get("deep"))}
    for f in s["families"]:
        cat["fam=" + f] = "1"
    for k in s["sem_keys"]:
        cat["sem=" + k] = "1"
    num = {"k_neg": s["k_neg"], "k_syn": s["k_syn"], "k_all": s["k_all"], "j_q": s["j_q"], "j_t": s["j_t"],
           "t_txt": s["t_txt"], "depth": float(s["base_depth"]), "len_state": len(st), "len_ins": len(r["instructions"]),
           "len_card": len(r.get("card") or ""), "n_lines": st.count("\n"), "n_nums": len(nu),
           "mag_max": max(mag) if mag else -1.0, "mag_mean": float(np.mean(mag)) if mag else -1.0,
           "n_sem": len(s["sem_keys"]), "n_fam": len(s["families"])}
    return cat, {k: float(v) for k, v in num.items()}


def lr():
    return LogisticRegression(C=1.0, max_iter=3000, solver="liblinear")


def gbt():
    return HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def cv(Xs, Xd, y, groups):
    res = {}
    for fold_nm, splits in (("grouped", list(GroupKFold(n_splits=5).split(Xs, y, groups))),
                            ("random", list(KFold(n_splits=5, shuffle=True, random_state=0).split(Xs)))):
        for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
            pred = np.zeros(len(y))
            for tr, te in splits:
                if len(set(y[tr])) < 2:
                    pred[te] = y[tr][0]; continue
                pred[te] = mk().fit(X[tr], y[tr]).predict(X[te])
            res[f"{nm}_{fold_nm}"] = round(float((pred == y).mean()), 4)
    return res


def main():
    rows = L.load(NAME); side = L.load_side(NAME)
    att = {side[r["id"]]["base_id"] for r in rows if side[r["id"]]["row_type"] == "Vp"}
    y = np.array([int(r["gold"]) for r in rows]); groups = [r["meta"]["card_id"] for r in rows]
    out = {"set": NAME, "n": len(rows), "yes_rate": round(float(y.mean()), 4), "chance": 0.5, "bar": 0.52,
           "folds": "GroupKFold(5) by card_id (gated); KFold(5, shuffle, seed 0) reported only"}
    views = {"a_question": [L.split_q(r["instructions"])[0] for r in rows],
             "c_card_noq": [((r.get("card") or "") + "\n\n" + L.split_q(r["instructions"])[1]).strip() for r in rows]}
    for nm, tx in views.items():
        Xs = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True,
                             token_pattern=r"[A-Za-z0-9'-]+").fit_transform(tx)
        Xd = TruncatedSVD(n_components=min(64, Xs.shape[1] - 1), random_state=0).fit_transform(Xs)
        out[nm] = cv(Xs, Xd, y, groups); log(f"{nm} {out[nm]}")
    D = [dict(**c, **n) for c, n in (meta_feats(r, side[r["id"]], side[r["id"]]["base_id"] in att) for r in rows)]
    dv = DictVectorizer(); Xs = MaxAbsScaler().fit_transform(dv.fit_transform(D)).tocsr()
    Xd = DictVectorizer(sparse=False).fit_transform(D)
    out["d_meta"] = cv(Xs, Xd, y, groups); out["d_meta_n_features"] = len(dv.feature_names_); log(f"d_meta {out['d_meta']}")
    out["b_options"] = {"all": 0.5, "note": "options are always Yes / No on every F5 row: chance by construction"}
    gated = {f"{v}.{k}": a for v in ("a_question", "c_card_noq", "d_meta") for k, a in out[v].items() if k.endswith("grouped")}
    out["gated"] = gated; out["max_gated"] = max(gated.values())
    out["pass"] = all(a <= 0.52 for a in gated.values())
    json.dump(out, open(L.QC / f"g6_{NAME}.json", "w"), indent=1); log(f"pass={out['pass']} max={out['max_gated']}")


if __name__ == "__main__":
    main()
