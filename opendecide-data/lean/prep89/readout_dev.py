"""Readout analysis on DEV only (goal step 8, A5 readouts) for 4B-E (q35_4b_pxE_fresh) and the 4B main run
(q35_4b_main500k). CPU only, reads stored dev predictions, writes prep89/readout_dev.json and prints a text report.
No OHS file is opened. Nothing is fitted on OHS-1/2/3. gate_dev.py and bench/v154/v154lib.py are imported read-only
so the accuracy, flip and ECE definitions are exactly the gate's and JevBench v1.5's.

  (1) per-type temperature (noul, choice): NLL fit on pooled dev-select, evaluated on dev-confirm
  (2) read-twice (2-view): mean of the standard and the _perm view in probability space; accuracy, permutation flips,
      equivalence (double-negation) flips, complement violations
  (3) band-edge yes/no readout on dev calibration
Run: ../.venv/bin/python prep89/readout_dev.py
"""
import hashlib
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

LEAN = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(LEAN))
import gate_dev as G  # noqa: E402  (read-only: half, score, argmax_label, SPLITS)
sys.path.insert(0, str(LEAN.parent.parent / "bench" / "v154"))
import v154lib as V  # noqa: E402  (read-only: ece_bins 10 equal-width bins, NOUL_NO / NOUL_YES)

SPLITS = G.SPLITS.split(",")
MODELS = {"4B-E": "q35_4b_pxE_fresh", "4B-main": "q35_4b_main500k"}
GRID_A5 = [round(0.50 + 0.05 * i, 2) for i in range(31)]  # A5 item 4: 0.50 .. 2.00
GRID_GATE = G.GRID  # calibrate.py / gate_dev: 0.25 .. 10.0
BOOTS, SEED = 10000, 0
HALVES = ("select", "confirm")


# ---------------------------------------------------------------- loading
def load_preds(path):
    return {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(path)}


def meta(sp, name):
    p = LEAN / f"preds_{sp}" / f"{name}.meta.json"
    return json.loads(p.read_text()) if p.exists() else None


def view_perm(r, seed=1):
    """decoder_io.view_perms, re-implemented (decoder_io imports torch): the displayed order of the seeded random view."""
    rng = random.Random(int.from_bytes(hashlib.sha256(f"{seed}:{r['id']}".encode()).digest()[:8], "big"))
    p = list(range(len(r["options"]))) if r["qtype"] == "choice" else [0, 1]
    rng.shuffle(p)
    return p


def keys_of(r):
    return ["yes", "no"] if r["qtype"] == "noul" else r["options"]


def norm(r, p):
    ks = keys_of(r)
    v = {k: max(float(p.get(k, 0.0)), 0.0) for k in ks}
    s = sum(v.values())
    return {k: x / s for k, x in v.items()} if s > 0 else v


def avg(r, p, q):
    return {k: (float(p.get(k, 0.0)) + float(q.get(k, 0.0))) / 2 for k in keys_of(r)}


rows = []
for sp in SPLITS:
    for l in open(LEAN / f"data/{sp}.jsonl"):
        r = json.loads(l)
        p = view_perm(r)
        rows.append({"split": sp, "id": r["id"], "group_id": r["group_id"], "half": G.half(r["group_id"]),
                     "source": r["source"], "qtype": r["qtype"], "gold": r["gold"], "options": r.get("options"),
                     "role": r.get("role"), "nopt": len(r["options"]) if r["qtype"] == "choice" else 2,
                     "perm": p, "perm_identity": p == sorted(p), "perm_reversed": p == sorted(p)[::-1]})
KEY = {(x["split"], x["id"]): x for x in rows}
checks = []

R = {}  # R[model][readout][(split, id)] = probs over the row's keys
for m, name in MODELS.items():
    std, prm = {}, {}
    for sp in SPLITS:
        a, b = load_preds(LEAN / f"preds_{sp}/{name}.jsonl"), load_preds(LEAN / f"preds_{sp}/{name}_perm.jsonl")
        ma, mb = meta(sp, name), meta(sp, name + "_perm")
        assert ma["perm_seed"] is None and mb["perm_seed"] == 1 and not any(mb[k] for k in ("tta", "tta_choice", "tta_noul"))
        for r in (x for x in rows if x["split"] == sp):
            std[(sp, r["id"])], prm[(sp, r["id"])] = a[r["id"]], b[r["id"]]
    R[m] = {"1v": std, "1v_perm": prm,
            "2v_perm": {k: avg(KEY[k], std[k], prm[k]) for k in std}}
    # A5 (a) as testable: choice rows 2-view, yes/no rows single read
    R[m]["A5a_perm"] = {k: (R[m]["2v_perm"][k] if KEY[k]["qtype"] == "choice" else std[k]) for k in std}
    # check: the _perm read equals the standard read exactly on rows whose seeded view is the identity
    same = [max(abs(float(std[k].get(o, 0)) - float(prm[k].get(o, 0))) for o in keys_of(KEY[k])) == 0 for k in std]
    ident = [KEY[k]["perm_identity"] for k in std]
    checks.append(f"{m}: _perm read == standard read on exactly the identity-view rows: {same == ident} "
                  f"({sum(ident)} identity-view rows of {len(ident)})")

# 4B-E only: the identity+reversed 2-view read (od_gcp --tta: choice reversed, yes/no letters swapped) and the drift
# reads (rotated view, rotated + its reversal), all od_gcp-style merged reads on the L4
tta, rot, rott = {}, {}, {}
for sp in SPLITS:
    t = load_preds(LEAN / f"preds_{sp}/q35_4b_pxE_tta.jsonl")
    mt = meta(sp, "q35_4b_pxE_tta")
    assert mt["tta"] is True and mt["gpu"] == "NVIDIA L4"
    for r in (x for x in rows if x["split"] == sp):
        tta[(sp, r["id"])] = t[r["id"]]
    for view, d in (("rot", rot), ("rot_tta", rott)):
        f = LEAN / f"drift/out/q35_4b_pxE__{sp}__{view}.jsonl"
        if f.exists():
            for k, v in load_preds(f).items():
                d[(sp, k)] = v
parity_equal = all(load_preds(LEAN / f"preds_{sp}/q35_4b_pxE_parity.jsonl") == load_preds(LEAN / f"preds_{sp}/q35_4b_pxE_fresh.jsonl")
                   for sp in SPLITS)
checks.append(f"4B-E: q35_4b_pxE_parity (the identity view inside the _tta and drift comparisons) == q35_4b_pxE_fresh "
              f"bit for bit: {parity_equal}")
R["4B-E"]["2v_rev"] = tta
R["4B-E"]["A5a_rev"] = {k: (tta[k] if KEY[k]["qtype"] == "choice" else R["4B-E"]["1v"][k]) for k in tta}
# consistency of the 2v_rev read with the stored views: on rows whose seeded view IS the reversal / letter swap,
# 2*tta - identity should equal the _perm read
dd = [max(abs(2 * float(tta[k][o]) - float(R["4B-E"]["1v"][k][o]) - float(R["4B-E"]["1v_perm"][k][o])) for o in keys_of(KEY[k]))
      for k in tta if KEY[k]["perm_reversed"] and not KEY[k]["perm_identity"]]
checks.append(f"4B-E: on the {len(dd)} rows whose seeded view is the reversal/letter swap, |2*tta - identity - perm| "
              f"mean {np.mean(dd):.5f}, max {np.max(dd):.4f} (same model, same pipeline up to batch noise)")
checks.append(f"4B-E drift reads: rot {len(rot)} choice rows, rot_tta {len(rott)} choice rows")


# ---------------------------------------------------------------- helpers
def acc(r, p):
    return G.score({"qtype": r["qtype"], "gold": r["gold"], "options": r["options"]}, p)[0]


def unit_boot(items, boots=BOOTS, seed=SEED):
    """items: (unit, a, b, w). Paired bootstrap over units of sum(a - b) / sum(w); returns point and 95% interval."""
    U = defaultdict(lambda: [0.0, 0.0, 0.0])
    for u, a, b, w in items:
        g = U[u]; g[0] += a; g[1] += b; g[2] += w
    A = np.array(list(U.values()))
    if not len(A):
        return {"diff": math.nan, "lo": math.nan, "hi": math.nan, "n": 0, "units": 0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(A), (boots, len(A)))
    S = A[idx].sum(1)
    bs = (S[:, 0] - S[:, 1]) / S[:, 2] * 100
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"diff": float((A[:, 0].sum() - A[:, 1].sum()) / A[:, 2].sum() * 100), "lo": float(lo), "hi": float(hi),
            "n": int(A[:, 2].sum()), "units": len(A)}


def sel(half=None, qtype=None, split=None, excl=()):
    return [x for x in rows if (half is None or x["half"] == half) and (qtype is None or x["qtype"] == qtype)
            and (split is None or x["split"] == split) and x["source"] not in excl]


def accuracy(rs, P):
    return 100 * sum(acc(x, P[(x["split"], x["id"])]) for x in rs) / len(rs) if rs else math.nan


# ---- temperature
def logmat(rs, P):
    items = []
    for x in rs:
        p = P[(x["split"], x["id"])]
        ks = keys_of(x)
        gi = (0 if x["gold"] == 1 else 1) if x["qtype"] == "noul" else ks.index(x["gold"])
        items.append(([math.log(max(float(p.get(k, 0.0)), 1e-12)) for k in ks], gi))
    L = np.full((len(items), max(len(l) for l, _ in items)), -np.inf)
    for i, (l, _) in enumerate(items):
        L[i, :len(l)] = l
    return L, np.array([g for _, g in items])


def scaled(L, T):
    Z = L / T
    E = np.exp(Z - Z.max(1, keepdims=True))
    return E / E.sum(1, keepdims=True)


def nll(L, gi, T):
    P = scaled(L, T)
    return float(-np.log(np.maximum(P[np.arange(len(gi)), gi], 1e-12)).mean())


def fit(L, gi, grid):
    best, bt = math.inf, 1.0
    for T in grid:  # gate_dev.fit_T's rule: lowest NLL, first one on ties
        v = nll(L, gi, T)
        if v < best:
            best, bt = v, T
    return bt


def calib_metrics(rs, P, T):
    """Metrics of rows rs (one qtype) under readout P with temperature T."""
    if not rs:
        return None
    L, gi = logmat(rs, P)
    Q = scaled(L, T)
    n = len(rs)
    top = Q.argmax(1)
    # ties count wrong (gate rule): a row is right only if the gold is the unique max
    mx = Q.max(1, keepdims=True)
    uniq = (Q == mx).sum(1) == 1
    ok = (top == gi) & uniq
    out = {"n": n, "T": T, "nll": float(-np.log(np.maximum(Q[np.arange(n), gi], 1e-12)).mean()),
           "acc": float(100 * ok.mean())}
    if rs[0]["qtype"] == "noul":
        y = np.array([float(x["gold"]) for x in rs])
        py = Q[:, 0]
        out["brier"] = float(((py - y) ** 2).mean())
        out["ece10_pyes"] = V.ece_bins(list(zip(py.tolist(), y.tolist())))  # JevBench v1.5 noul ECE
        out["ece10_top"] = V.ece_bins(list(zip(Q.max(1).tolist(), ok.tolist())))
    else:
        oh = np.zeros_like(Q); oh[np.arange(n), gi] = 1
        Qf = np.where(np.isfinite(L), Q, 0.0)
        out["brier_mc"] = float(((Qf - oh) ** 2).sum(1).mean())
        out["ece10_top"] = V.ece_bins(list(zip(Q.max(1).tolist(), ok.tolist())))  # JevBench v1.5 choice ECE
    return out


# ---- relation pairs
def pairs(types):
    out = []
    for sp in SPLITS:
        p = LEAN / f"data/{sp}_relations.jsonl"
        if not p.exists():
            continue
        for l in open(p):
            rel = json.loads(l)
            a, b = KEY.get((sp, rel["a"])), KEY.get((sp, rel["b"]))
            if rel["type"] in types and a is not None and b is not None and a["qtype"] == b["qtype"]:
                out.append((a, b))
    return out


def lab(x, P):
    return G.argmax_label(x, P[(x["split"], x["id"])])


def decision(x, P):
    """OHS-3 decision: yes if P(yes) > 0.5, no if < 0.5, None on a tie."""
    p = float(P[(x["split"], x["id"])].get("yes", 0.0))
    return "yes" if p > 0.5 else "no" if p < 0.5 else None


def flip_rate(prs, P, Q=None):
    Q = Q or P
    return 100 * sum(lab(a, P) != lab(b, Q) for a, b in prs) / len(prs) if prs else math.nan


def compl_viol(prs, P):
    v = 0
    for a, b in prs:
        da, db = decision(a, P), decision(b, P)
        v += da is None or db is None or da == db
    return 100 * v / len(prs) if prs else math.nan


def swap_class(a, b):
    s = (not a["perm_identity"]) + (not b["perm_identity"])
    return {0: "neither", 1: "one", 2: "both"}[s]


res = {"checks": checks, "models": MODELS}
print("==== checks"); [print("  " + c) for c in checks]

# ================================================================= (2) read-twice: accuracy
print("\n==== (2a) ACCURACY: 1-view vs 2-view (gate scoring, ties wrong; paired bootstrap over group_id, 10,000, seed 0)")
nv = sum(not x["perm_identity"] for x in rows if x["qtype"] == "noul")
nc = sum(not x["perm_identity"] for x in rows if x["qtype"] == "choice")
print(f"  seeded perm-seed-1 view: choice rows non-identity {nc}/{sum(x['qtype']=='choice' for x in rows)}, "
      f"yes/no rows letter-swapped {nv}/{sum(x['qtype']=='noul' for x in rows)}; on the rest the 2-view = the 1-view")
res["view_counts"] = {"choice_nonidentity": nc, "noul_swapped": nv,
                      "choice_n": sum(x['qtype'] == 'choice' for x in rows), "noul_n": sum(x['qtype'] == 'noul' for x in rows)}
res["acc"] = {}
for m in MODELS:
    variants = ["1v", "1v_perm", "2v_perm", "A5a_perm"] + (["2v_rev", "A5a_rev"] if m == "4B-E" else [])
    res["acc"][m] = {}
    for v in variants:
        P = R[m][v]
        d = {}
        for h in (None,) + HALVES:
            for qt in (None, "noul", "choice"):
                rs = sel(h, qt)
                d[f"{h or 'pooled'}/{qt or 'all'}"] = accuracy(rs, P)
        res["acc"][m][v] = d
    print(f"  {m}")
    print(f"    {'readout':10s} " + " ".join(f"{c:>15s}" for c in ("pooled all", "select all", "confirm all", "pooled yes/no", "pooled choice")))
    for v in variants:
        d = res["acc"][m][v]
        print(f"    {v:10s} " + " ".join(f"{d[c]:15.2f}" for c in ("pooled/all", "select/all", "confirm/all", "pooled/noul", "pooled/choice")))
    res["acc"][m]["diff"] = {}
    for v in variants[1:]:
        for h in (None,) + HALVES:
            for qt in (None, "noul", "choice"):
                rs = sel(h, qt)
                b = unit_boot([(x["group_id"], acc(x, R[m][v][(x["split"], x["id"])]), acc(x, R[m]["1v"][(x["split"], x["id"])]), 1)
                               for x in rs])
                res["acc"][m]["diff"][f"{v}|{h or 'pooled'}/{qt or 'all'}"] = b
        b = res["acc"][m]["diff"]
        print(f"    {v} - 1v:  pooled {b[f'{v}|pooled/all']['diff']:+.2f} [{b[f'{v}|pooled/all']['lo']:+.2f}, {b[f'{v}|pooled/all']['hi']:+.2f}]"
              f"  select {b[f'{v}|select/all']['diff']:+.2f}  confirm {b[f'{v}|confirm/all']['diff']:+.2f}"
              f"  | yes/no {b[f'{v}|pooled/noul']['diff']:+.2f} [{b[f'{v}|pooled/noul']['lo']:+.2f}, {b[f'{v}|pooled/noul']['hi']:+.2f}]"
              f" (sel {b[f'{v}|select/noul']['diff']:+.2f} / conf {b[f'{v}|confirm/noul']['diff']:+.2f})"
              f"  | choice {b[f'{v}|pooled/choice']['diff']:+.2f} [{b[f'{v}|pooled/choice']['lo']:+.2f}, {b[f'{v}|pooled/choice']['hi']:+.2f}]"
              f" (sel {b[f'{v}|select/choice']['diff']:+.2f} / conf {b[f'{v}|confirm/choice']['diff']:+.2f})")
# yes/no accuracy on the letter-swapped rows only (where 2v_perm is a full 2-view)
res["acc_swapped_noul"] = {}
for m in MODELS:
    rs = [x for x in rows if x["qtype"] == "noul" and not x["perm_identity"]]
    b = unit_boot([(x["group_id"], acc(x, R[m]["2v_perm"][(x["split"], x["id"])]), acc(x, R[m]["1v"][(x["split"], x["id"])]), 1) for x in rs])
    res["acc_swapped_noul"][m] = {"n": len(rs), "1v": accuracy(rs, R[m]["1v"]), "2v": accuracy(rs, R[m]["2v_perm"]), "diff": b}
    print(f"  {m} yes/no rows with a letter-swapped view only (n={len(rs)}): 1v {accuracy(rs, R[m]['1v']):.2f} -> 2v "
          f"{accuracy(rs, R[m]['2v_perm']):.2f}: {b['diff']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]")

# ================================================================= (2) permutation flips
print("\n==== (2b) PERMUTATION FLIPS (share of rows whose answer changes between two displayed orders)")
res["perm_flips"] = {}
for m in MODELS:
    d = {}
    for qt in (None, "noul", "choice"):
        rs = sel(qtype=qt)
        d[f"1v std vs perm/{qt or 'all'}"] = 100 * sum(lab(x, R[m]["1v"]) != lab(x, R[m]["1v_perm"]) for x in rs) / len(rs)
    rs = [x for x in sel(qtype="choice") if not x["perm_identity"]]
    d["1v std vs perm/choice, non-identity views"] = 100 * sum(lab(x, R[m]["1v"]) != lab(x, R[m]["1v_perm"]) for x in rs) / len(rs)
    rs10 = [x for x in sel(qtype="choice") if x["nopt"] >= 10]
    d["1v std vs perm/choice 10+ options"] = 100 * sum(lab(x, R[m]["1v"]) != lab(x, R[m]["1v_perm"]) for x in rs10) / len(rs10)
    res["perm_flips"][m] = d
    print(f"  {m}: gate (f) all rows {d['1v std vs perm/all']:.2f}%  (yes/no {d['1v std vs perm/noul']:.2f}%, choice "
          f"{d['1v std vs perm/choice']:.2f}%, choice with a non-identity view {d['1v std vs perm/choice, non-identity views']:.2f}%, "
          f"choice 10+ options {d['1v std vs perm/choice 10+ options']:.2f}%)")
# 4B-E: two independent 2-view reads exist on choice rows: (identity + perm1) and (rotation + its reversal)
E = R["4B-E"]
ch = [x for x in sel(qtype="choice") if (x["split"], x["id"]) in rot]
ch10 = [x for x in ch if x["nopt"] >= 10]
P_rot, P_rott = rot, rott
fl = {}
for name, A, B in (("1v identity vs 1v rotated", E["1v"], P_rot),
                   ("1v perm1 vs 1v rotated", E["1v_perm"], P_rot),
                   ("2v(identity+perm1) vs 2v(rotated+reversed rotated)", E["2v_perm"], P_rott),
                   ("2v(identity+reversed) vs 2v(rotated+reversed rotated)", E["2v_rev"], P_rott),
                   ("2v(identity+perm1) vs 2v(identity+reversed) [share the identity view]", E["2v_perm"], E["2v_rev"])):
    fl[name] = {"all": 100 * sum(lab(x, A) != lab(x, B) for x in ch) / len(ch),
                "10+": 100 * sum(lab(x, A) != lab(x, B) for x in ch10) / len(ch10), "n": len(ch), "n10": len(ch10)}
res["perm_flips"]["4B-E choice, 2-view vs 2-view"] = fl
print(f"  4B-E choice rows (n={len(ch)}; 10+ options n={len(ch10)}), flips between two reads:")
for k, v in fl.items():
    print(f"    {k:75s} {v['all']:5.2f}%   10+ options {v['10+']:5.2f}%")
print("  yes/no: a 2-view read uses both Yes/No letter orders, so it has no permutation left to flip: 0 by construction.")
print("  4B-main: only two views exist (identity, perm1), so its 2-view choice flip rate cannot be measured here.")

# ================================================================= (2) equivalence / complement / inv pairs
print("\n==== (2c) EQUIVALENCE flips (gate (e): affirmative vs double-negated yes/no pairs), COMPLEMENT violations, INV flips")
EQ, CO, INV = pairs(("equiv",)), pairs(("complement",)), pairs(("inv",))
print(f"  pairs: equiv {len(EQ)} (all yes/no), complement {len(CO)} (all yes/no), inv {len(INV)}")
res["pairs"] = {"n_equiv": len(EQ), "n_complement": len(CO), "n_inv": len(INV)}
for m in MODELS:
    variants = ["1v", "1v_perm", "2v_perm"] + (["2v_rev"] if m == "4B-E" else [])
    d = {}
    for v in variants:
        P = R[m][v]
        d[v] = {"equiv_flip": flip_rate(EQ, P), "complement_violation": compl_viol(CO, P), "inv_flip": flip_rate(INV, P),
                "equiv_by_swap": {c: (flip_rate([p for p in EQ if swap_class(*p) == c], P), sum(swap_class(*p) == c for p in EQ))
                                  for c in ("neither", "one", "both")},
                "complement_by_swap": {c: (compl_viol([p for p in CO if swap_class(*p) == c], P), sum(swap_class(*p) == c for p in CO))
                                       for c in ("neither", "one", "both")},
                "equiv_mean_abs_dp": float(np.mean([abs(float(P[(a['split'], a['id'])]['yes']) - float(P[(b['split'], b['id'])]['yes'])) for a, b in EQ])),
                "complement_mean_abs_sum": float(np.mean([abs(float(P[(a['split'], a['id'])]['yes']) + float(P[(b['split'], b['id'])]['yes']) - 1) for a, b in CO]))}
    # paired bootstrap of 2-view minus 1-view flip rate (unit = group_id of the pair)
    def fb(prs, v, f):
        return unit_boot([(a["group_id"], f([(a, b)], R[m][v]), f([(a, b)], R[m]["1v"]), 100) for a, b in prs])
    d["boot"] = {}
    both_eq = [p for p in EQ if swap_class(*p) == "both"]
    both_co = [p for p in CO if swap_class(*p) == "both"]
    d["boot"]["equiv 2v_perm-1v all"] = fb(EQ, "2v_perm", flip_rate)
    d["boot"]["equiv 2v_perm-1v both-swapped"] = fb(both_eq, "2v_perm", flip_rate)
    d["boot"]["complement 2v_perm-1v all"] = fb(CO, "2v_perm", compl_viol)
    d["boot"]["complement 2v_perm-1v both-swapped"] = fb(both_co, "2v_perm", compl_viol)
    if m == "4B-E":
        d["boot"]["equiv 2v_rev-1v all"] = fb(EQ, "2v_rev", flip_rate)
        d["boot"]["complement 2v_rev-1v all"] = fb(CO, "2v_rev", compl_viol)
        d["boot"]["equiv 2v_rev-1v both-swapped"] = fb(both_eq, "2v_rev", flip_rate)
    res["pairs"][m] = d
    print(f"  {m}")
    for v in variants:
        e = d[v]
        bs = e["equiv_by_swap"]
        print(f"    {v:8s} equiv flips {e['equiv_flip']:5.2f}%  [pairs with 0/1/2 letter-swapped rows in perm1: "
              f"{bs['neither'][0]:.2f}% (n={bs['neither'][1]}) / {bs['one'][0]:.2f}% (n={bs['one'][1]}) / {bs['both'][0]:.2f}% (n={bs['both'][1]})]"
              f"  mean|dP| {e['equiv_mean_abs_dp']:.4f} | complement viol {e['complement_violation']:5.2f}%"
              f" (both-swapped {e['complement_by_swap']['both'][0]:.2f}%, n={e['complement_by_swap']['both'][1]}) | inv flips {e['inv_flip']:.2f}%")
    for k, b in d["boot"].items():
        print(f"    {k:40s} {b['diff']:+.2f} pp [{b['lo']:+.2f}, {b['hi']:+.2f}] (pairs {b['n'] // 100}, units {b['units']})")

# the gate's (e) comparison re-run under each readout (4B-main vs 4B-E, REF + 2 pp)
print("  gate (e) re-read under each readout (cand 4B-main vs REF 4B-E; bar REF + 2.00 pp):")
res["gate_e_by_readout"] = {}
for vm, ve, label in (("1v", "1v", "1-view (the gate's look)"), ("2v_perm", "2v_perm", "2-view identity+perm1 for both"),
                      ("2v_perm", "2v_rev", "2-view: 4B-main identity+perm1, 4B-E identity+swap (full)")):
    c, r = flip_rate(EQ, R["4B-main"][vm]), flip_rate(EQ, R["4B-E"][ve])
    res["gate_e_by_readout"][label] = {"cand": c, "ref": r, "pass": c <= r + 2.0}
    print(f"    {label:62s} {c:5.2f}% vs {r:5.2f}%  {'PASS' if c <= r + 2 else 'FAIL'}")
bothq = [p for p in EQ if swap_class(*p) == "both"]
c1, r1 = flip_rate(bothq, R["4B-main"]["1v"]), flip_rate(bothq, R["4B-E"]["1v"])
c2, r2 = flip_rate(bothq, R["4B-main"]["2v_perm"]), flip_rate(bothq, R["4B-E"]["2v_perm"])
res["gate_e_by_readout"]["both-swapped subset"] = {"n": len(bothq), "1v": [c1, r1], "2v": [c2, r2]}
print(f"    both-swapped subset (n={len(bothq)}, both rows of the pair have a full 2-view): 1-view {c1:.2f}% vs {r1:.2f}%;"
      f" 2-view {c2:.2f}% vs {r2:.2f}%")

# ---- anatomy of the (e) gap (1-view): which row of a flipped pair is wrong, by split; accuracy by role
print("  (e) anatomy, 1-view: flipped pairs by split and which row is wrong; yes/no accuracy by role")
res["equiv_anatomy"] = {}
for m in MODELS:
    P = R[m]["1v"]
    d = {"by_split": {}, "wrong_side": {"aff wrong": 0, "dneg wrong": 0}, "role_acc": {}}
    for sp in ("devzs", "devp_card", "dev"):
        prs = [p for p in EQ if p[0]["split"] == sp]
        d["by_split"][sp] = {"n": len(prs), "flip": flip_rate(prs, P)}
    for a, b in EQ:
        if lab(a, P) != lab(b, P):
            d["wrong_side"]["aff wrong" if not acc(a, P[(a["split"], a["id"])]) else "dneg wrong"] += 1
    for role in ("aff", "neg", "dneg"):
        rs = [x for x in rows if x["qtype"] == "noul" and x["role"] == role and x["split"] in ("devzs", "devp_card", "dev")]
        d["role_acc"][role] = {"n": len(rs), "acc": accuracy(rs, P)}
    bysrc = defaultdict(lambda: [0, 0])
    for a, b in EQ:
        bysrc[(a["split"], a["source"])][0] += 1
        bysrc[(a["split"], a["source"])][1] += lab(a, P) != lab(b, P)
    d["by_split_source"] = {f"{k[0]}/{k[1]}": {"n": v[0], "flips": v[1]} for k, v in sorted(bysrc.items())}
    res["equiv_anatomy"][m] = d
    print(f"    {m}: flips by split " + ", ".join(f"{k} {v['flip']:.2f}% (n={v['n']})" for k, v in d["by_split"].items())
          + f" | flipped pairs: affirmative row wrong {d['wrong_side']['aff wrong']}, double-negated row wrong {d['wrong_side']['dneg wrong']}"
          + " | yes/no acc by role (devzs+devp_card+dev): " + ", ".join(f"{k} {v['acc']:.2f} (n={v['n']})" for k, v in d["role_acc"].items()))
    print("      flips by split/source: " + ", ".join(f"{k} {v['flips']}/{v['n']}" for k, v in d["by_split_source"].items()))

# ================================================================= (1) temperature
print("\n==== (1) TEMPERATURE per question type: NLL fit on pooled dev-select (9 splits), evaluated on dev-confirm")
print("  grid A5 item 4: 0.50..2.00 step 0.05 (the gate grid 0.25..10.0 is checked too). ECE: JevBench v1.5 ece_bins,"
      " 10 equal-width bins; yes/no on P(yes), choice on top-label confidence.")
res["temperature"] = {}
for m in MODELS:
    variants = ["1v", "A5a_perm"] + (["A5a_rev", "2v_rev"] if m == "4B-E" else [])
    res["temperature"][m] = {}
    for v in variants:
        P = R[m][v]
        d = {}
        for qt in ("noul", "choice"):
            if qt == "noul" and v.startswith("A5a"):
                continue  # A5a yes/no = 1v yes/no
            fs, cf = sel("select", qt), sel("confirm", qt)
            L, gi = logmat(fs, P)
            T = fit(L, gi, GRID_A5)
            Tg = fit(L, gi, GRID_GATE)
            fs_x = sel("select", qt, excl=G.CONSTRAINT_EXCLUDE)
            Tx = fit(*logmat(fs_x, P), GRID_A5)
            Lc, gc = logmat(cf, P)
            Tconf = fit(Lc, gc, GRID_A5)  # for stability only, never used
            raw, cal = calib_metrics(cf, P, 1.0), calib_metrics(cf, P, T)
            e = {"T_select": T, "T_select_gategrid": Tg, "T_select_excl_tb_mixtral": Tx, "T_confirm_info": Tconf,
                 "confirm_raw": raw, "confirm_T": cal,
                 "select_raw": calib_metrics(fs, P, 1.0), "select_T": calib_metrics(fs, P, T)}
            if qt == "noul":
                ps = {}
                for sp in SPLITS:
                    rs = sel("confirm", "noul", split=sp)
                    if rs:
                        ps[sp] = {"n": len(rs), "raw": calib_metrics(rs, P, 1.0)["brier"], "T": calib_metrics(rs, P, T)["brier"]}
                e["confirm_split_brier"] = ps
                imp = raw["brier"] - cal["brier"]
                worst = max(v2["T"] - v2["raw"] for v2 in ps.values())
                e["A5_rule"] = {"pooled_improvement": imp, "worst_split_worsening": worst,
                                "ship_T": T if (T != 1.0 and imp >= 0.002 and worst <= 0.003) else 1.0}
            else:
                ps = {}
                for sp in SPLITS:
                    rs = sel("confirm", "choice", split=sp)
                    if rs:
                        ps[sp] = {"n": len(rs), "nll_raw": calib_metrics(rs, P, 1.0)["nll"], "nll_T": calib_metrics(rs, P, T)["nll"]}
                e["confirm_split_nll"] = ps
            d[qt] = e
        res["temperature"][m][v] = d
        print(f"  {m} / readout {v}")
        for qt, e in d.items():
            r0, r1 = e["confirm_raw"], e["confirm_T"]
            if qt == "noul":
                a5 = e["A5_rule"]
                print(f"    yes/no  T(select)={e['T_select']} (gate grid {e['T_select_gategrid']}, w/o tb_mixtral {e['T_select_excl_tb_mixtral']},"
                      f" confirm-fit {e['T_confirm_info']}) | confirm n={r0['n']}: Brier {r0['brier']:.4f} -> {r1['brier']:.4f},"
                      f" ECE {r0['ece10_pyes']:.4f} -> {r1['ece10_pyes']:.4f}, NLL {r0['nll']:.4f} -> {r1['nll']:.4f},"
                      f" acc {r0['acc']:.2f} -> {r1['acc']:.2f} | A5 rule: improvement {a5['pooled_improvement']:+.4f},"
                      f" worst split {a5['worst_split_worsening']:+.4f} -> ship T={a5['ship_T']}")
            else:
                print(f"    choice  T(select)={e['T_select']} (gate grid {e['T_select_gategrid']}, w/o tb_mixtral {e['T_select_excl_tb_mixtral']},"
                      f" confirm-fit {e['T_confirm_info']}) | confirm n={r0['n']}: NLL {r0['nll']:.4f} -> {r1['nll']:.4f},"
                      f" top ECE {r0['ece10_top']:.4f} -> {r1['ece10_top']:.4f}, Brier(mc) {r0['brier_mc']:.4f} -> {r1['brier_mc']:.4f},"
                      f" acc {r0['acc']:.2f} -> {r1['acc']:.2f}")

# ================================================================= (3) band edge
print("\n==== (3) BAND-EDGE yes/no readout (P(yes) in (0.5,0.8) -> 0.8, in (0.2,0.5] -> 0.2; after T), 1-view")
print("  v1.5 rule: P>=0.80 yes, P<=0.20 no, between = abstention counted wrong; noul calibration score = 100*(1 - ECE/0.5)")


def band_edge(y):
    return 0.8 if 0.5 < y < 0.8 else 0.2 if 0.2 < y <= 0.5 else y


def commit(y):
    return 1.0 if y > 0.5 else 0.0


res["band_edge"] = {}
for m in MODELS:
    T = res["temperature"][m]["1v"]["noul"]["A5_rule"]["ship_T"]
    Tfit = res["temperature"][m]["1v"]["noul"]["T_select"]
    res["band_edge"][m] = {"T_used": T}
    for Tuse, tag in ((1.0, "T=1"), (Tfit, f"T={Tfit} (select fit)")):
        for h in ("confirm", "select", None):
            rs = sel(h, "noul")
            L, gi = logmat(rs, R[m]["1v"])
            py = scaled(L, Tuse)[:, 0]
            y = np.array([float(x["gold"]) for x in rs])
            out = {}
            for name, f in (("as returned", lambda v: v), ("full commit", commit), ("band edge", band_edge)):
                q = np.array([f(v) for v in py])
                dec = np.where(q >= V.NOUL_YES, 1, np.where(q <= V.NOUL_NO, 0, -1))
                ece = V.ece_bins(list(zip(q.tolist(), y.tolist())))
                out[name] = {"brier": float(((q - y) ** 2).mean()), "ece10": ece, "v15_noul_calib": V.ece_score(ece),
                             "abstain": float(100 * (dec == -1).mean()), "v15_committed_acc": float(100 * (dec == y).mean()),
                             "argmax_acc": float(100 * (((q > 0.5) & (y == 1)) | ((q < 0.5) & (y == 0))).mean())}
            # band-edge Brier change split by whether the moved row was right or wrong
            moved = (py > 0.2) & (py < 0.8)
            out["moved_share"] = float(100 * moved.mean())
            out["moved_argmax_acc"] = float(100 * ((((py > 0.5) & (y == 1)) | ((py <= 0.5) & (y == 0)))[moved]).mean()) if moved.any() else math.nan
            res["band_edge"][m][f"{tag}|{h or 'pooled'}"] = out
    print(f"  {m}")
    for k, out in res["band_edge"][m].items():
        if k == "T_used":
            continue
        line = "; ".join(f"{n}: Brier {o['brier']:.4f}, ECE {o['ece10']:.4f} (cal {o['v15_noul_calib']:.1f}), abstain {o['abstain']:.1f}%,"
                         f" v1.5 acc {o['v15_committed_acc']:.2f}" for n, o in out.items() if isinstance(o, dict))
        print(f"    {k:28s} n/a moved {out['moved_share']:.1f}% (argmax acc there {out['moved_argmax_acc']:.1f}%) | {line}")

json.dump(res, open(OUT / "readout_dev.json", "w"), indent=1, default=float)
print(f"\nwrote {OUT / 'readout_dev.json'}")
