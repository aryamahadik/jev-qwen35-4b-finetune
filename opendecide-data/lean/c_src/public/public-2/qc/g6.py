"""G6 partial-input and metadata baselines on our framings (C_DATA_SPEC v4 8 G6; public rows: 'G6 (on our
framings)'). QC sample = every final public-2 row (rows + reserve + dev = 4,028; public datasets have no 5,000 rows of
our framings, like F8 / F12 / F13). 5-fold GroupKFold by source page / table / passage / record.
Models: logistic regression on TF-IDF word 1-2 grams (+ dense features), and small gradient-boosted trees
(HistGradientBoosting, depth 3) on the dense features + a 64-d SVD of the n-grams.
Yes/no (chance 0.5): (a) question only (instructions), (c) card + state without the question, (d) metadata only.
  (b) n/a: the options are always Yes / No.
Choice (pointwise (row, option) scorer, argmax per row, ties split; chance = mean 1/k):
  (a) option n-grams + question-option overlap, (b) option n-grams + option-set structure (length rank, longest,
  shortest, numeric max / min, abstain, k), (c) option n-grams + option mention in card / state (count, first-mention
  order), (d) metadata (dataset, framing, wording, card route, styles) x option kind.
Rule (gated): pooled over all public-2 rows, accuracy <= chance + 2 pp for every view and model. Per dataset
(n 140-1,000): a view fails when accuracy > chance + 2 pp AND one-sided binomial p < 0.01 (the point estimate is
reported too). Counts only."""
import json
import math
import re
import warnings
from collections import defaultdict

import numpy as np
from scipy import sparse
from scipy.stats import binomtest
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

from qclib import ABSTAIN, DATASETS, FILES, OUT, load_all, write_gate

warnings.filterwarnings("ignore")
NUM = re.compile(r"-?\d[\d,]*\.?\d*")


def group_key(r, th):
    s, rid = r["source"], r["meta"]["text_source"]["record_id"]
    if r["id"] in th:
        return s + ":" + re.sub(r"_\d+$", "", th[r["id"]]) if s == "c_pub_hybridqa" else s + ":" + th[r["id"]]
    if s == "c_pub_drop":
        return s + ":" + rid.split(":")[0]
    return s + ":" + rid


def tonum(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return None


def yn_meta(r):
    m = r["meta"]
    ns = [tonum(x) for x in NUM.findall(r["instructions"])]
    ns = [x for x in ns if x is not None]
    d = {f"{k}={m.get(k)}": 1 for k in ("framing", "wording_id", "card_id", "card_route", "defs_style",
                                         "format_style", "depth")}
    d["src=" + r["source"]] = 1
    d["len_ins"] = len(r["instructions"]) / 100
    d["len_state"] = math.log1p(len(r["state"]))
    d["n_nums_ins"] = len(ns)
    d["T_log"] = math.copysign(math.log10(1 + abs(ns[-1])), ns[-1]) if ns else 0
    d["T_int"] = float(bool(ns) and ns[-1] == int(ns[-1]))
    return d


def opt_units(r, view):
    """[(text, dense dict)] per option for one view."""
    opts = r["options"]
    k = len(opts)
    L = [len(o) for o in opts]
    rank = {i: sorted(L, reverse=True).index(L[i]) for i in range(k)}
    nums = [tonum(o) for o in opts]
    nn = [x for x in nums if x is not None]
    st, ins, card = r["state"].lower(), r["instructions"].lower(), (r.get("card") or "").lower()
    first = {i: (st.find(o.lower()) if o.lower() in st else 10 ** 9) for i, o in enumerate(opts)}
    order = sorted(range(k), key=lambda i: first[i])
    out = []
    for i, o in enumerate(opts):
        kind = {"abstain": float(o in ABSTAIN), "longest": float(L[i] == max(L)), "shortest": float(L[i] == min(L)),
                "num_max": float(nums[i] is not None and len(nn) > 1 and nums[i] == max(nn)),
                "num_min": float(nums[i] is not None and len(nn) > 1 and nums[i] == min(nn))}
        d = {}
        if view == "a":
            ow = set(re.findall(r"[a-z0-9]+", o.lower()))
            iw = set(re.findall(r"[a-z0-9]+", ins))
            d = {"overlap": len(ow & iw), "overlap_frac": len(ow & iw) / max(1, len(ow)), "in_ins": float(o.lower() in ins)}
        elif view == "b":
            d = dict(kind) | {"len_rank": rank[i] / max(1, k - 1), "len": math.log1p(L[i]), "k": k,
                              "is_num": float(nums[i] is not None)}
        elif view == "c":
            d = {"in_state": float(o.lower() in st), "count_state": math.log1p(st.count(o.lower())) if o else 0,
                 "first_order": order.index(i) / max(1, k - 1) if first[i] < 10 ** 9 else -1,
                 "in_card": float(o.lower() in card)}
        elif view == "d":
            m = r["meta"]
            for kk, v in kind.items():
                if v:
                    for f in ("framing", "wording_id", "card_route", "defs_style", "format_style"):
                        d[f"{f}={m.get(f)}|{kk}"] = 1
                    d["src=" + r["source"] + "|" + kk] = 1
            d["k"] = k
        out.append((o if view != "d" else "", d))
    return out


def cv_rows(rows, groups, X_txt, X_dense, y, n_rows=None, row_of=None):
    """Return out-of-fold scores for LR and HGB."""
    gkf = GroupKFold(n_splits=5)
    s_lr, s_gb = np.zeros(len(y)), np.zeros(len(y))
    for tr, te in gkf.split(np.zeros(len(y)), y, groups):
        mats_tr, mats_te, den_tr, den_te = [], [], [], []
        if X_txt is not None and any(t for t in X_txt):
            tv = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=50000, sublinear_tf=True)
            try:
                A = tv.fit_transform([X_txt[i] for i in tr])
                B = tv.transform([X_txt[i] for i in te])
                mats_tr.append(A)
                mats_te.append(B)
                if A.shape[1] > 70:
                    svd = TruncatedSVD(64, random_state=0)
                    den_tr.append(svd.fit_transform(A))
                    den_te.append(svd.transform(B))
            except ValueError:
                pass
        if X_dense is not None:
            dv = DictVectorizer()
            A = dv.fit_transform([X_dense[i] for i in tr])
            B = dv.transform([X_dense[i] for i in te])
            mats_tr.append(A)
            mats_te.append(B)
            den_tr.append(A.toarray())
            den_te.append(B.toarray())
        Xtr, Xte = sparse.hstack(mats_tr).tocsr(), sparse.hstack(mats_te).tocsr()
        ytr = y[tr]
        if len(set(ytr)) < 2:
            continue
        lr = LogisticRegression(max_iter=3000, C=1.0)
        lr.fit(Xtr, ytr)
        s_lr[te] = lr.predict_proba(Xte)[:, 1]
        gb = HistGradientBoostingClassifier(max_depth=3, max_iter=150, learning_rate=0.1, random_state=0)
        gb.fit(np.hstack(den_tr), ytr)
        s_gb[te] = gb.predict_proba(np.hstack(den_te))[:, 1]
    return s_lr, s_gb


def verdict(acc, chance, n, gated_strict):
    over = acc - chance
    p = float(binomtest(int(round(acc * n)), n, min(.999, chance), alternative="greater").pvalue) if n else 1.0
    fail = over > .02 if gated_strict else (over > .02 and p < .01)
    return {"acc": round(acc, 4), "chance": round(chance, 4), "over_pp": round(100 * over, 2), "n": n,
            "p_binom": round(p, 5), "fail": bool(fail)}


def main():
    data = load_all()
    th = {}
    for line in open(OUT / "table_hashes.jsonl"):
        t = json.loads(line)
        th[t["id"]] = t["table_id"]
    rows = [r for fn in FILES for r in data[fn]]
    res, fails = {}, []
    # ---------------- yes/no
    yn = [r for r in rows if r["qtype"] == "noul"]
    y = np.array([int(r["gold"]) for r in yn])
    g = np.array([group_key(r, th) for r in yn])
    views = {"a_question_only": ([r["instructions"] for r in yn], None),
             "c_card_state_no_question": [((r.get("card") or "") + "\n" + r["state"]) for r in yn],
             "d_metadata": (None, [yn_meta(r) for r in yn])}
    views["c_card_state_no_question"] = (views["c_card_state_no_question"], None)
    for vn, (txt, den) in views.items():
        s_lr, s_gb = cv_rows(yn, g, txt, den, y)
        print("yn view done", vn, flush=True)
        for mn, s in (("lr", s_lr), ("gbt", s_gb)):
            pred = (s >= .5).astype(int)
            ok = pred == y
            key = f"yes_no|{vn}|{mn}"
            res[key] = {"pooled": verdict(ok.mean(), .5, len(y), True)}
            if res[key]["pooled"]["fail"]:
                fails.append(key + "|pooled")
            for ds in DATASETS:
                idx = [i for i, r in enumerate(yn) if r["source"] == ds]
                if idx:
                    v = verdict(ok[idx].mean(), .5, len(idx), False)
                    res[key][ds] = v
                    if v["fail"]:
                        fails.append(f"{key}|{ds}")
    # ---------------- choice
    ch = [r for r in rows if r["qtype"] == "choice"]
    for vn in ("a", "b", "c", "d"):
        units, row_of, yy, gg = [], [], [], []
        for ri, r in enumerate(ch):
            gk = group_key(r, th)
            for (t, d), o in zip(opt_units(r, vn), r["options"]):
                units.append((t, d))
                row_of.append(ri)
                yy.append(int(o == r["gold"]))
                gg.append(gk)
        yy, gg, row_of = np.array(yy), np.array(gg), np.array(row_of)
        s_lr, s_gb = cv_rows(None, gg, [u[0] for u in units] if vn != "d" else None, [u[1] for u in units], yy)
        print("choice view done", vn, flush=True)
        vname = {"a": "a_question_options", "b": "b_options_only", "c": "c_options_card_state", "d": "d_metadata_x_kind"}[vn]
        for mn, s in (("lr", s_lr), ("gbt", s_gb)):
            accs = np.zeros(len(ch))
            by = defaultdict(list)
            for u, ri in enumerate(row_of):
                by[ri].append(u)
            for ri, us in by.items():
                sc = s[us]
                top = np.isclose(sc, sc.max())
                gold_u = [u for u in us if yy[u] == 1]
                accs[ri] = (1 / top.sum()) if gold_u and top[us.index(gold_u[0])] else 0.0
            chance = np.array([1 / len(r["options"]) for r in ch])
            key = f"choice|{vname}|{mn}"
            res[key] = {"pooled": verdict(accs.mean(), chance.mean(), len(ch), True)}
            if res[key]["pooled"]["fail"]:
                fails.append(key + "|pooled")
            for ds in DATASETS:
                idx = [i for i, r in enumerate(ch) if r["source"] == ds]
                if idx:
                    v = verdict(accs[idx].mean(), chance[idx].mean(), len(idx), False)
                    res[key][ds] = v
                    if v["fail"]:
                        fails.append(f"{key}|{ds}")
    write_gate("G6", not fails, res, fails=fails, qc_sample={"rows": len(rows), "yes_no": len(yn), "choice": len(ch)})
    print("G6", not fails, fails[:12])


if __name__ == "__main__":
    main()
