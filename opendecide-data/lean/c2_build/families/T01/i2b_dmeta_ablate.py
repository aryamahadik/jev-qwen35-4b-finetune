"""Diagnostic: leave-one-group-out / only-group CV of the choice d_meta LR (pilot._pair_rows d_meta, rebuilt from
pilot_i2/i2b/choice_rows.json), and k-stratified association of the row-level meta features with the gold position.
Read-only analysis; G6 itself is untouched.  ../../.venv/bin/python -B families/T01/i2b_dmeta_ablate.py [file.json]"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import numpy as np  # noqa: E402
import pilot  # noqa: E402
from scipy import sparse  # noqa: E402
from scipy.stats import chi2 as CHI  # noqa: E402
from sklearn.feature_extraction import DictVectorizer  # noqa: E402
from sklearn.feature_extraction.text import HashingVectorizer  # noqa: E402
from sklearn.preprocessing import MaxAbsScaler  # noqa: E402

OUT = C2 / "families/T01/pilot_i2/i2b"
FN = sys.argv[1] if len(sys.argv) > 1 else "choice_rows.json"
rows = json.load(open(OUT / FN))
CATS = list(rows[0]["cat"])
NUMS = list(rows[0]["num"])
OPT = ["k", "tlen", "clen", "len_rank", "is_longest", "is_shortest", "abstain", "neg", "verbatim", "has_digit"]


def build(drop=(), only=None):
    """drop/only: group names among tok, optdn, num, cat:<name>."""
    def on(g):
        return (g not in drop) if only is None else (g in only)
    T, D, Y, Rw = [], [], [], []
    for ri, r in enumerate(rows):
        k = r["k"]
        order = sorted(range(k), key=lambda j: -r["clen"][j])
        rank = {j: n for n, j in enumerate(order)}
        for j, o in enumerate(r["opts"]):
            ou = pilot.toks(o)
            kinds = set(r["all_kinds"][j])
            dn = {"k": float(k), "tlen": float(len(ou)), "clen": float(r["clen"][j]), "len_rank": rank[j] / max(1, k - 1),
                  "is_longest": float("kind:longest" in kinds), "is_shortest": float("kind:shortest" in kinds),
                  "abstain": float("kind:abstain" in kinds), "neg": float("kind:neg" in kinds),
                  "verbatim": float("kind:verbatim_in_text" in kinds), "has_digit": float(any(c.isdigit() for c in o))}
            tk = []
            if on("tok"):
                tk += ["o:" + t for t in ou] + ["o2:" + a + "_" + c for a, c in zip(ou, ou[1:])]
            d = dict(dn) if on("optdn") else {}
            if on("num"):
                d.update(r["num"])
            for kk, vv in r["cat"].items():
                if on("cat:" + kk):
                    tk.append(f"m:{kk}={vv}|neg{int(dn['neg'])}|abs{int(dn['abstain'])}|lr{int(dn['len_rank'] * 4)}")
            T.append(tk)
            D.append(d or {"_": 0.0})
            Y.append(int(j == r["gold"]))
            Rw.append(ri)
    return T, D, np.array(Y), np.array(Rw)


def cv(drop=(), only=None):
    T, D, Y, Rw = build(drop, only)
    Xs = HashingVectorizer(n_features=2 ** 18, analyzer=lambda x: x, alternate_sign=False, norm="l2").transform(T)
    Xd = DictVectorizer(sparse=False).fit_transform(D)
    groups = np.array([rows[ri]["card"] for ri in Rw])
    folds = pilot._folds(list(groups))
    sc = np.zeros(len(Y))
    for tr, te in folds:
        sca = MaxAbsScaler().fit(Xd[tr])
        Xtr = sparse.hstack([Xs[tr], sparse.csr_matrix(sca.transform(Xd[tr]))]).tocsr()
        Xte = sparse.hstack([Xs[te], sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()
        sc[te] = pilot._lr().fit(Xtr, Y[tr]).predict_proba(Xte)[:, 1]
    best = defaultdict(list)
    for s, ri, yy in zip(sc, Rw, Y):
        best[ri].append((s, yy))
    acc = np.zeros(len(rows))
    for ri, lst in best.items():
        m = max(s for s, _ in lst)
        top = [yy for s, yy in lst if s >= m - 1e-12]
        acc[ri] = sum(top) / len(top)
    return round(float(acc.mean()), 4)


def strat_chi(featfn):
    """k-stratified chi2 of gold position vs a feature value (summed over k strata)."""
    x = dof = 0
    for k in sorted({r["k"] for r in rows}):
        tab = defaultdict(Counter)
        for r in rows:
            if r["k"] == k:
                tab[featfn(r)][r["pos"]] += 1
        tot = Counter()
        for c in tab.values():
            tot.update(c)
        n = sum(tot.values())
        for c in tab.values():
            nv = sum(c.values())
            for p in tot:
                e = nv * tot[p] / n
                if e > 0:
                    x += (c.get(p, 0) - e) ** 2 / e
        dof += (len(tab) - 1) * (len(tot) - 1)
    return x, dof


res = {"chance": round(sum(1 / r["k"] for r in rows) / len(rows), 4), "full": cv()}
res["drop_group"] = {g: cv(drop=(g,)) for g in ["tok", "optdn", "num"] + ["cat:" + c for c in CATS]}
res["only_optdn_plus"] = {"optdn": cv(only=("optdn",)), "optdn+tok": cv(only=("optdn", "tok")),
                          "optdn+num": cv(only=("optdn", "num"))}
res["only_optdn_plus"].update({"optdn+cat:" + c: cv(only=("optdn", "cat:" + c)) for c in CATS})
st = []
for c in CATS:
    x, dof = strat_chi(lambda r, c=c: r["cat"][c])
    st.append({"feature": c, "chi2": round(x, 1), "dof": dof, "p": float(CHI.sf(x, dof)), "excess_per_row": round((x - dof) / len(rows), 4)})
for f in NUMS:
    vals = sorted(r["num"][f] for r in rows)
    t1, t2 = vals[len(rows) // 3], vals[2 * len(rows) // 3]
    x, dof = strat_chi(lambda r, f=f: 0 if r["num"][f] <= t1 else 1 if r["num"][f] <= t2 else 2)
    if dof:
        st.append({"feature": "num:" + f, "chi2": round(x, 1), "dof": dof, "p": float(CHI.sf(x, dof)), "excess_per_row": round((x - dof) / len(rows), 4)})
res["k_stratified_pos_assoc"] = sorted(st, key=lambda d: -d["excess_per_row"])
# k distribution is itself a gold-position predictor only through chance level; also gold-pos by (qform,k)
cells = {}
for q in sorted({str(r["qform"]) for r in rows}):
    for k in sorted({r["k"] for r in rows}):
        sub = [r for r in rows if str(r["qform"]) == q and r["k"] == k]
        if len(sub) >= 30:
            cnt = Counter(r["pos"] for r in sub)
            x = sum((cnt.get(p, 0) - len(sub) / k) ** 2 / (len(sub) / k) for p in range(k))
            cells[f"{q}|k{k}"] = {"n": len(sub), "pos": [cnt.get(p, 0) for p in range(k)], "chi2": round(x, 1), "p": round(float(CHI.sf(x, k - 1)), 4)}
res["pos_by_qform_k"] = cells
(OUT / ("DMETA_ABLATION_" + FN)).write_text(json.dumps(res, indent=1))
print(json.dumps({k: res[k] for k in ("chance", "full", "drop_group", "only_optdn_plus")}))
print(json.dumps(res["k_stratified_pos_assoc"][:8]))
print(json.dumps(res["pos_by_qform_k"]))
