"""G6 partial-input and metadata baselines (independent F4 checker). C_DATA_SPEC 8 G6 + F4 G0 8:
5-fold CV grouped by meta.card_id (F4 G0 8 asks for card-grouped folds) on out/qc_sample.jsonl (5,400 rows).
Models: logistic regression on word 1-2 gram TF-IDF (or hashed n-grams), and sklearn HistGradientBoosting on dense
features (SVD of the n-grams for text views). Yes/no rows: predict gold from (a) question only, (c) card only (the
card on yes/no rows), (d) metadata only; (b) options only is the constant Yes/No pair (chance by construction).
Choice rows: pointwise scorer over (row, option) pairs, argmax per row, chance = mean 1/k over rows. Pair features:
option n-grams + option x view crossed unigrams (k <= 4 rows) + option-view overlap; (b) option n-grams, option-set
features and the option definition line; (c) the card clauses (in `instructions` on choice rows, F4 7.6) without the
question; (d) row metadata x option-set features (option token lengths). Pass: every accuracy <= chance + 2 pp.
Display position is never a feature (gold-letter uniformity is G10). Usage: g6.py [qc_sample]"""
import json, sys, time, re
import numpy as np
from collections import Counter
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import MaxAbsScaler
import qc_lib as L

NAME = sys.argv[1] if len(sys.argv) > 1 else "qc_sample"
EXT = "--ext" in sys.argv
T0 = time.time()
WRX = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def log(msg):
    print(f"[{time.time() - T0:7.1f}s] {msg}", flush=True)


def toks(s):
    return WRX.findall(s.lower())


HEDGE = ("most", "many", "usually", "often", "some", "not every", "may be", "might be", "may well be")


def text_counts(r):
    t = (r["state"] or "").lower()
    return {"n_unless": t.count("unless") + t.count("except"), "n_hedge": sum(t.count(h) for h in HEDGE),
            "n_closure": t.count("names every") + t.count("is complete") + t.count("are complete"),
            "n_numbers": float(len(L.nums(r["state"]))), "n_source": t.count("source"),
            "n_notrec": t.count("not recorded") + t.count("null"), "n_onlyif": t.count("only if"),
            "n_either": t.count("either"), "n_atleast": t.count("at least")}


def meta_feats(r, sc):
    """F4 G0 8 metadata list: depth, rule count, length, option lengths, number magnitudes, name pool, template id,
    sampler id, statement count, entity count, exception-word count, hedge count, closure count, carrier kind, inert
    kind, pack, label form, counted length. Never a label or pivot tag."""
    m = r["meta"]; ed = m.get("edge", [])
    tag = lambda p: next((e for e in ed if e.split(":")[0] == p), p + ":none")
    cat = {"sampler": m["sampler"], "template": m["wording_id"] + "|" + tag("frame"), "pack": m["domain_pack"],
           "carrier": str(sc.get("carrier")), "inert": str(sc.get("inert")), "label_form": str(sc.get("label_form"))}
    if EXT:  # report-only extension: other visible generator properties (style, defs, world, unless, negcount, ...)
        cat.update({"style": m["format_style"], "defs": m["defs_style"], "world": tag("world"),
                    "unless": tag("unless"), "boundary": tag("boundary"), "negcount": tag("negcount"),
                    "yes_bad": tag("yes_bad"), "wording": m["wording_id"], "frame": tag("frame")})
    nums = L.nums(r["state"])
    mag = [np.log10(abs(x)) if x else 0.0 for x in nums]
    num = {"depth": float(m.get("depth") or 0), "n_rules": float(sc.get("n_rules") or 0),
           "n_ents": float(sc.get("n_ents") or 0), "n_stmts": float(sc.get("n_stmts") or 0),
           "len_tokens": float(sc.get("len_tokens") or 0), "len_state": float(len(r["state"])),
           "len_ins": float(len(r["instructions"])), "len_card": float(len(r.get("card") or "")),
           "k": float(len(r["options"] or [])) or 2.0, "mag_max": max(mag) if mag else -1.0,
           "mag_mean": float(np.mean(mag)) if mag else -1.0,
           "n_dec": float(sum(1 for x in nums if x != int(x)))}
    num.update({k: float(v) for k, v in text_counts(r).items()})
    return cat, num


def lr():
    return LogisticRegression(C=1.0, max_iter=3000, solver="liblinear")


def gbt():
    return HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, max_leaf_nodes=31, random_state=0)


def dense_text(X, n=64):
    n = min(n, X.shape[1] - 1)
    return TruncatedSVD(n_components=n, random_state=0).fit_transform(X)


def cv_yn(Xs, Xd, y, groups):
    gkf = GroupKFold(n_splits=5); res = {}
    for nm, X, mk in (("lr", Xs, lr), ("gbt", Xd, gbt)):
        pred = np.zeros(len(y))
        for tr, te in gkf.split(X, y, groups):
            if len(set(y[tr])) < 2:
                pred[te] = y[tr][0]; continue
            m = mk().fit(X[tr], y[tr]); pred[te] = m.predict(X[te])
        res[nm] = float((pred == y).mean())
    return res


def run_yn(rows, side):
    y = np.array([int(r["gold"]) for r in rows]); groups = [r["meta"]["card_id"] for r in rows]
    out = {"n": len(rows), "yes_rate": float(y.mean()), "chance": 0.5, "majority": float(max(y.mean(), 1 - y.mean()))}
    V = {r["id"]: L.views(r) for r in rows}
    texts = {"a_question": [V[r["id"]]["q"] for r in rows], "c_card": [r.get("card") or "" for r in rows]}
    for nm, tx in texts.items():
        Xs = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, token_pattern=r"[A-Za-z0-9'-]+").fit_transform(tx)
        Xd = dense_text(Xs) if Xs.shape[1] > 2 else Xs.toarray()
        out[nm] = cv_yn(Xs, Xd, y, groups); log(f"yn {nm} {out[nm]}")
    cats, numsd = zip(*[meta_feats(r, side[r["id"]]) for r in rows])
    Xc = DictVectorizer().fit_transform([{**c, **n} for c, n in zip(cats, numsd)])
    Xs = MaxAbsScaler().fit_transform(Xc).tocsr()
    dv = DictVectorizer(sparse=False).fit([{**c, **n} for c, n in zip(cats, numsd)])
    Xd = dv.transform([{**c, **n} for c, n in zip(cats, numsd)])
    out["d_meta"] = cv_yn(Xs, Xd, y, groups); log(f"yn d_meta {out['d_meta']}")
    out["b_options"] = {"lr": out["chance"], "gbt": out["chance"], "note": "options are always Yes/No"}
    return out


def bucket(k):
    return "2-4" if k <= 4 else "5-9" if k <= 9 else "10-19" if k <= 19 else "20-60"


NEG = re.compile(r"\bnot\b|n't\b|\bno\b|\bnever\b")


def optset(r, defs):
    opts = r["options"]; k = len(opts); lens = [len(toks(o)) for o in opts]
    clen = [len(o) for o in opts]
    rk = np.argsort(np.argsort(-np.array(clen), kind="stable"))
    out = []
    for i, o in enumerate(opts):
        out.append({"k": float(k), "tlen": float(lens[i]), "clen": float(clen[i]), "len_rank": float(rk[i]) / max(1, k - 1),
                    "is_longest": float(clen[i] == max(clen)), "is_shortest": float(clen[i] == min(clen)),
                    "abstain": float(L.is_abstain(o)), "neg": float(bool(NEG.search(o.lower()))),
                    "has_def": float(o in defs), "def_len": float(len(defs.get(o, ""))),
                    "has_digit": float(any(c.isdigit() for c in o))})
    return out


def overlap(o, vt):
    ot = set(toks(o))
    return {"ov": len(ot & vt) / max(1, len(ot)), "ov_n": float(len(ot & vt))}


def pair_data(rows, side, view):
    """Returns token lists (for hashing), dense dicts, pair labels, row index per pair."""
    d = L.dio(); T, D, Y, R = [], [], [], []
    for ri, r in enumerate(rows):
        defs = d.card_defs(r.get("card")); V = L.views(r); k = len(r["options"])
        vtext = {"a_question": V["q"], "c_card": V["cardnoq"].replace(r.get("card") or "", ""), "b_options": "",
                 "d_meta": ""}[view]
        vt = set(toks(vtext)); os_ = optset(r, defs)
        if view == "d_meta":
            cat, num = meta_feats(r, side[r["id"]])
        for i, o in enumerate(r["options"]):
            ou = toks(o); tk = ["o:" + t for t in ou] + ["o2:" + a + "_" + b for a, b in zip(ou, ou[1:])]
            dn = dict(os_[i])
            if view == "b_options":
                du = toks(defs.get(o, "")); tk += ["d:" + t for t in du] + ["d2:" + a + "_" + b for a, b in zip(du, du[1:])]
            elif view in ("a_question", "c_card"):
                dn.update(overlap(o, vt))
                if k <= 4:
                    tk += ["x:" + a + "|" + b for a in set(ou[:6]) for b in vt]
                tk += ["ov:%d" % min(5, int(dn["ov_n"]))]
            else:
                dn.update(num); dn.update({"c_" + kk: vv for kk, vv in cat.items()})
                tk += ["m:%s=%s|neg%d|abs%d|lr%d" % (kk, vv, dn["neg"], dn["abstain"], int(dn["len_rank"] * 4))
                       for kk, vv in cat.items()]
            T.append(tk); D.append(dn); Y.append(int(o == r["gold"])); R.append(ri)
    return T, D, np.array(Y), np.array(R)


def argmax_acc(scores, R, Y, nrows):
    best = {}
    for s, ri, y in zip(scores, R, Y):
        best.setdefault(ri, []).append((s, y))
    acc = np.zeros(nrows)
    for ri, lst in best.items():
        m = max(s for s, _ in lst); top = [y for s, y in lst if s >= m - 1e-12]
        acc[ri] = sum(top) / len(top)
    return acc


def run_choice(rows, side):
    gidx = {}
    for ri, r in enumerate(rows):
        gidx[ri] = r["meta"]["card_id"]
    chance_rows = np.array([1.0 / len(r["options"]) for r in rows])
    out = {"n": len(rows), "chance": float(chance_rows.mean())}
    forms = [side[r["id"]]["form"] for r in rows]; bks = [bucket(len(r["options"])) for r in rows]
    for view in ("a_question", "b_options", "c_card", "d_meta"):
        T, D, Y, R = pair_data(rows, side, view)
        Xs = HashingVectorizer(n_features=2 ** 20, analyzer=lambda x: x, alternate_sign=False, norm="l2").transform(T)
        dv = DictVectorizer(sparse=False); Xd = dv.fit_transform(D)
        groups = np.array([gidx[ri] for ri in R])
        res = {}
        for nm in ("lr", "gbt"):
            sc = np.zeros(len(Y))
            for tr, te in GroupKFold(n_splits=5).split(Xd, Y, groups):
                if nm == "lr":
                    Xtr = sparse.hstack([Xs[tr], sparse.csr_matrix(MaxAbsScaler().fit(Xd[tr]).transform(Xd[tr]))]).tocsr()
                    sca = MaxAbsScaler().fit(Xd[tr])
                    Xte = sparse.hstack([Xs[te], sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()
                    m = lr().fit(Xtr, Y[tr]); sc[te] = m.predict_proba(Xte)[:, 1]
                else:
                    m = gbt().fit(Xd[tr], Y[tr]); sc[te] = m.predict_proba(Xd[te])[:, 1]
            acc = argmax_acc(sc, R, Y, len(rows))
            per_form = {}
            for f in sorted(set(forms)):
                ix = [i for i, x in enumerate(forms) if x == f]
                per_form[f] = {"n": len(ix), "acc": round(float(acc[ix].mean()), 4),
                               "chance": round(float(chance_rows[ix].mean()), 4)}
            per_b = {}
            for b in sorted(set(bks)):
                ix = [i for i, x in enumerate(bks) if x == b]
                per_b[b] = {"n": len(ix), "acc": round(float(acc[ix].mean()), 4),
                            "chance": round(float(chance_rows[ix].mean()), 4)}
            res[nm] = {"acc": float(acc.mean()), "per_form": per_form, "per_bucket": per_b}
        out[view] = res; log(f"choice {view} lr {res['lr']['acc']:.4f} gbt {res['gbt']['acc']:.4f} chance {out['chance']:.4f}")
    return out


def main():
    rows = L.load(NAME)
    side = {json.loads(l)["id"]: json.loads(l) for l in open(L.OUT / f"{NAME}.sidecar.jsonl")}
    log(f"loaded {len(rows)} rows")
    yn = [r for r in rows if r["qtype"] == "noul"]; ch = [r for r in rows if r["qtype"] != "noul"]
    res = {"gate": "G6", "file": f"out/{NAME}.jsonl", "rows": len(rows), "folds": "GroupKFold(5) by meta.card_id",
           "meta_features": "F4 G0 8 list (depth, rule/statement/entity counts, lengths, option token lengths, number "
                            "magnitudes, pack = name pool, template id = wording x frame paraphrase, sampler, exception/"
                            "hedge/closure counts, carrier, inert, label form, counted length)" + (" + extended visible "
                            "properties (report-only)" if EXT else "; row role / twin-set tags are not in the prompt "
                            "and are not features"),
           "yes_no": run_yn(yn, side), "choice": run_choice(ch, side)}
    fails = []
    for v in ("a_question", "c_card", "d_meta"):
        for m in ("lr", "gbt"):
            a = res["yes_no"][v][m]
            if a > 0.5 + 0.02:
                fails.append(f"yn {v} {m} {a:.4f}")
    ch0 = res["choice"]["chance"]
    for v in ("a_question", "b_options", "c_card", "d_meta"):
        for m in ("lr", "gbt"):
            a = res["choice"][v][m]["acc"]
            if a > ch0 + 0.02:
                fails.append(f"choice {v} {m} {a:.4f} vs chance {ch0:.4f}")
    res["fails"] = fails; res["pass"] = not fails
    json.dump(res, open(L.QC / f"g6_{NAME}{'_ext' if EXT else ''}.json", "w"), indent=1)
    log(f"DONE pass={res['pass']} fails={fails}")


if __name__ == "__main__":
    main()
