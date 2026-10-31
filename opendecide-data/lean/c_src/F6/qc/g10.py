"""G10 balance (independent F6 checker): C_DATA_SPEC v4 8 G10 + 2.1 quotas + F6 G0 section 6 (full v4 list plus the
F6 additions), from rows, meta, edge, the QC side file, the relations file and the shared negcount (recomputed on the
rendered question). Bins (G9 crowd) are absent in round-1 candidates (meta.difficulty_bin is null on every row), so
every 'x bin' axis is pooled and the bin axis is reported as pending.
- POOL checks: row or display properties selection cannot fix (gold letter uniform per bucket, longest option, abstain
  display and gold rates, abstain wrong rates, attack vs label, polarity coverage). Pass on the pool, with binomial
  noise tolerance (p > 0.01 against the nearest band edge).
- TARGET checks: shares that stratified block selection sets (yes rate per wording x k_all, per frame, per kind, per
  world x form, settled Q-DET split, Q-EST No split, can/cannot, yes=bad, quotas, twin share). A cell passes when in
  band, or noise-consistent, or when a block selection of round-1 size is LP-feasible (g10_feas.py, reported apart).
Prints counts only. Usage: g10.py [candidates_r1]"""
import json, sys
from collections import Counter, defaultdict
import numpy as np
from scipy.stats import chisquare, chi2_contingency, binomtest
import qc_lib as q
sys.path.insert(0, str(q.LEAN / "c_src/common"))
import negcount

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
N_SEL = 3600
rows, side = q.load(NAME)
rels = q.load_rel(NAME)
yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
S = lambda r: side.get(r["id"], {})
ABST = {"nei": ["Cannot be determined from the record", "The record does not settle this", "Not enough information to decide",
                "Undetermined on this record", "The record leaves this open"],
        "none": ["None of the listed outcomes", "None of these", "No listed outcome fits", "No outcome on this list applies"],
        "nothing": ["No additional detail is required", "No further fact is needed"]}
KIND = {t: k for k, ts in ABST.items() for t in ts}
okind = lambda o: KIND.get(o.strip(), "concrete")
CHK = []


def add(name, ok, kind, **info):
    CHK.append({"check": name, "kind": kind, "pass": bool(ok), **info})


def band_ok(x, n, lo, hi):
    if n == 0:
        return True, None
    r = x / n
    if lo <= r <= hi:
        return True, 1.0
    t = lo if r < lo else hi
    p = binomtest(x, n, t).pvalue
    return p > 0.01, round(float(p), 4)


def chi_p(table):
    t = np.array(table, dtype=float)
    t = t[t.sum(1) > 0][:, t.sum(0) > 0]
    if t.shape[0] < 2 or t.shape[1] < 2:
        return 1.0
    return float(chi2_contingency(t)[1])


def rate_cells(name, groups, lo, hi, kind, min_n=1):
    """groups: key -> list of 0/1. Adds one summary check; returns the failing cells."""
    bad = []
    for key, ys in sorted(groups.items(), key=lambda kv: str(kv[0])):
        if len(ys) < min_n:
            continue
        ok, p = band_ok(sum(ys), len(ys), lo, hi)
        if not ok:
            bad.append({"cell": str(key), "n": len(ys), "rate": round(sum(ys) / len(ys), 4), "p": p})
    add(name, not bad, kind, n_cells=sum(1 for v in groups.values() if len(v) >= min_n), n_fail=len(bad), fails=bad[:30])
    return bad


# ---------------------------------------------------------------- POOL checks (choice display)
rng = np.random.default_rng(10)
by_b = defaultdict(list); per_k = defaultdict(list)
for r in ch:
    k = len(r["options"]); g = r["options"].index(r["gold"])
    by_b[q.bucket(k)].append((g + rng.random()) / k); per_k[k].append(g)
for b, us in sorted(by_b.items()):
    p = float(chisquare(np.histogram(us, bins=10, range=(0, 1))[0]).pvalue)
    add(f"gold_letter_uniform[{b}]", p > 0.01, "pool", n=len(us), chi2_p=round(p, 4))
for k in sorted(per_k):
    if k <= 6 and len(per_k[k]) >= 30:
        c = np.bincount(per_k[k], minlength=k); p = float(chisquare(c).pvalue)
        add(f"gold_letter_uniform[k={k}]", p > 0.01, "pool", n=int(c.sum()), counts=c.tolist(), chi2_p=round(p, 4))
# longest option gold within 1/k +/- 2 pp (expected = mean m/k over rows; m = options tied at max length)
hit = 0; exp = 0.0
for r in ch:
    L = [len(o) for o in r["options"]]; mx = max(L); m = sum(1 for x in L if x == mx)
    hit += int(len(r["gold"]) == mx); exp += m / len(L)
n = len(ch); ok, p = band_ok(hit, n, exp / n - 0.02, exp / n + 0.02)
add("longest_option_gold", ok, "pool", n=n, rate=round(hit / n, 4), expected=round(exp / n, 4), p=p)
for f in ("c_out", "c_rec", "c_gap", "c_case"):
    rr = [r for r in ch if S(r).get("form") == f]
    h = sum(int(len(r["gold"]) == max(len(o) for o in r["options"])) for r in rr)
    e = sum(sum(1 for o in r["options"] if len(o) == max(len(x) for x in r["options"])) / len(r["options"]) for r in rr)
    ok, p = band_ok(h, len(rr), e / len(rr) - 0.02, e / len(rr) + 0.02)
    add(f"longest_option_gold[{f}]", ok, "pool", n=len(rr), rate=round(h / len(rr), 4), expected=round(e / len(rr), 4), p=p)
# abstain display (C-OUT + C-REC): k = 2 none shown; k = 3-4 at most one; P(NEI|k>=3)=min(1,.1k), P(None|k>=3)=min(1,.05k)
oc = [r for r in ch if S(r).get("form") in ("c_out", "c_rec")]
k2_shown = k34_both = 0
disp = {"nei": defaultdict(lambda: [0, 0]), "none": defaultdict(lambda: [0, 0])}
goldk = {"nei": defaultdict(lambda: [0, 0]), "none": defaultdict(lambda: [0, 0])}
for r in oc:
    k = len(r["options"]); ks = [okind(o) for o in r["options"]]; gk = okind(r["gold"])
    if k == 2 and any(x != "concrete" for x in ks): k2_shown += 1
    if 3 <= k <= 4 and "nei" in ks and "none" in ks: k34_both += 1
    for a in ("nei", "none"):
        if k >= 3:
            disp[a][k][0] += int(a in ks); disp[a][k][1] += 1
        if a in ks:
            goldk[a][k][0] += int(gk == a); goldk[a][k][1] += 1
add("abstain_none_at_k2", k2_shown == 0, "pool", n_violations=k2_shown)
add("abstain_disjoint_k3_4", k34_both == 0, "pool", n_violations=k34_both)
for a, f in (("nei", 0.10), ("none", 0.05)):
    bad = []
    for k, (x, n) in sorted(disp[a].items()):
        t = min(1.0, f * k); ok, p = band_ok(x, n, t - 0.02, t + 0.02) if t < 1 else (x == n, None)
        if not ok: bad.append({"k": k, "n": n, "shown": round(x / n, 3), "target": t, "p": p})
    add(f"abstain_display_rate[{a}]", not bad, "raw", n_k=len(disp[a]), fails=bad)
    bad = []; X = N = 0; E = 0.0
    for k, (x, n) in sorted(goldk[a].items()):
        X += x; N += n; E += n / k
        ok, p = band_ok(x, n, 1 / k - 0.02, 1 / k + 0.02)
        if not ok: bad.append({"k": k, "n": n, "gold_rate": round(x / n, 3), "target": round(1 / k, 3), "p": p})
    ok, p = band_ok(X, N, E / N - 0.02, E / N + 0.02) if N else (True, None)
    add(f"abstain_gold_1_over_k[{a}]", not bad and ok, "target", n_shown=N, gold=X, expected=round(E, 1), p_pooled=p, fails_per_k=bad)
# abstain wrong >= 2/3 per option (F6), >= 50% (v4); both gold <= 2/5 of rows showing both; nothing >= 50% wrong
for a, need in (("nei", 2 / 3), ("none", 2 / 3), ("nothing", 0.5)):
    sh = [r for r in ch if any(okind(o) == a for o in r["options"])]
    w = sum(1 for r in sh if okind(r["gold"]) != a)
    ok, p = band_ok(w, len(sh), need, 1.0)
    add(f"abstain_wrong[{a}]", ok, "pool", n_shown=len(sh), wrong_rate=round(w / max(1, len(sh)), 4), need=round(need, 3), p=p)
both = [r for r in ch if {"nei", "none"} <= {okind(o) for o in r["options"]}]
g = sum(1 for r in both if okind(r["gold"]) in ("nei", "none"))
ok, p = band_ok(g, len(both), 0.0, 0.4)
add("abstain_both_gold_le_2_5", ok, "pool", n_both=len(both), gold_rate=round(g / max(1, len(both)), 4), p=p)
# attack present vs label
ya = [int(r["gold"]) for r in yn if S(r).get("attack")]; yc = [int(r["gold"]) for r in yn if not S(r).get("attack")]
gap = abs(np.mean(ya) - np.mean(yc)) if ya else 0.0
pz = chi_p([[sum(ya), len(ya) - sum(ya)], [sum(yc), len(yc) - sum(yc)]]) if ya else 1.0
add("attack_vs_label_yes_no", gap <= 0.02 or pz > 0.01, "pool", n_attack=len(ya), yes_attack=round(float(np.mean(ya)), 4) if ya else None,
    yes_clean=round(float(np.mean(yc)), 4), gap_pp=round(100 * gap, 2), chi2_p=round(pz, 4))
cls = sorted({S(r).get("gold_class") for r in ch})
tab = [[sum(1 for r in ch if bool(S(r).get("attack")) == a and S(r).get("gold_class") == c) for c in cls] for a in (True, False)]
p = chi_p(tab); add("attack_vs_gold_class_choice", p > 0.01, "pool", classes=cls, table=tab, chi2_p=round(p, 4))
# polarity coverage: yes/no rows whose S has no polarity <= 5%
npol = sum(1 for r in yn if S(r).get("valence") not in ("good", "bad"))
ok, p = band_ok(npol, len(yn), 0.0, 0.05)
add("no_polarity_le_5pct", ok, "pool", n_yes_no=len(yn), n_no_polarity=npol, rate=round(npol / len(yn), 4), p=p,
    note="row-level property; selection cannot add polarity to a row")
# ---------------------------------------------------------------- TARGET checks (selection sets these)
kq = {r["id"]: negcount.count(q.split_q(r["instructions"])[0]) for r in yn}
mism = sum(1 for r in yn if S(r).get("k_all") is not None and kq[r["id"]].k_all != S(r).get("k_all"))
add("negcount_side_agrees", True, "info", n_k_all_mismatch=mism)
y = lambda r: int(r["gold"])
G = lambda f: {k: v for k, v in _grp(f).items()}
def _grp(f):
    d = defaultdict(list)
    for r in yn: d[f(r)].append(y(r))
    return d
TFAIL = {}
TFAIL["yes_wording_x_kall"] = rate_cells("yes_rate[wording x bin(pooled) x k_all]", _grp(lambda r: (r["meta"]["wording_id"], kq[r["id"]].k_all)), .48, .52, "target")
TFAIL["yes_kind"] = rate_cells("yes_rate[yes/no kind]", _grp(lambda r: S(r).get("form")), .48, .52, "target")
TFAIL["yes_frame"] = rate_cells("yes_rate[frame_id]", _grp(lambda r: S(r).get("frame_id")), .48, .52, "target")
TFAIL["yes_world_form"] = rate_cells("yes_rate[world x form]", _grp(lambda r: (S(r).get("card_variant"), S(r).get("form"))), .48, .52, "target")
TFAIL["yes_wording"] = rate_cells("yes_rate[wording]", _grp(lambda r: r["meta"]["wording_id"]), .48, .52, "target")
ok, p = band_ok(sum(map(y, yn)), len(yn), .48, .52)
add("yes_rate_family", ok, "target", n=len(yn), rate=round(np.mean([y(r) for r in yn]), 4), p=p)
# settled Q-DET split per frame (T={true} vs {false}); Q-EST No split (refuted vs open); can/cannot on C-CASE
sd = defaultdict(list)
for r in yn:
    t = S(r).get("t_set")
    if S(r).get("form") == "qdet" and t and len(t) == 1: sd[S(r).get("frame_id")].append(int(t[0] is True))
TFAIL["qdet_settled_split"] = rate_cells("settled_qdet_true_share[frame]", sd, .48, .52, "target")
qn = [int(len(S(r)["t_set"]) == 1) for r in yn if S(r).get("form") == "qest" and y(r) == 0]
ok, p = band_ok(sum(qn), len(qn), .48, .52); add("qest_no_refuted_share", ok, "target", n=len(qn), rate=round(np.mean(qn), 4), p=p)
cc = [int(S(r).get("gold_class") == "can") for r in ch if S(r).get("form") == "c_case"]
ok, p = band_ok(sum(cc), len(cc), .48, .52); add("c_case_can_share", ok, "target", n=len(cc), rate=round(np.mean(cc), 4), p=p)
cg = [int(S(r).get("gold_class") == "nothing") for r in ch if S(r).get("form") == "c_gap"]
add("c_gap_nothing_share", True, "info", n=len(cg), rate=round(np.mean(cg), 4))
# yes = bad 50 +/- 5 over all yes/no rows (no polarity counts as not-bad), independent of the label
yb = [int(S(r).get("valence") == "bad") for r in yn]
ok, p = band_ok(sum(yb), len(yb), .45, .55)
yb1 = [int(S(r).get("valence") == "bad") for r in yn if y(r) == 1]; yb0 = [int(S(r).get("valence") == "bad") for r in yn if y(r) == 0]
ok1, p1 = band_ok(sum(yb1), len(yb1), .45, .55); ok0, p0 = band_ok(sum(yb0), len(yb0), .45, .55)
pol = [int(S(r).get("valence") == "bad") for r in yn if S(r).get("valence") in ("good", "bad")]
add("yes_bad_50pm5", ok and ok1 and ok0, "target", n=len(yb), rate=round(np.mean(yb), 4), p=p, rate_in_yes=round(np.mean(yb1), 4),
    rate_in_no=round(np.mean(yb0), 4), rate_among_polar_rows=round(np.mean(pol), 4), n_polar=len(pol))
# negation quotas (negcount on the rendered question)
ks1 = sum(1 for r in yn if kq[r["id"]].k_syn >= 1)
add("k_syn_ge1_ge10pct", ks1 / len(yn) >= 0.10, "target", n=ks1, rate=round(ks1 / len(yn), 4))
byid = {r["id"]: r for r in rows}; dn = 0
for u in rels:
    if u["type"] != "equiv": continue
    a, b = byid.get(u["a"]), byid.get(u["b"])
    if not a or not b or not q.is_yn(a) or not q.is_yn(b): continue
    for x, z in ((a, b), (b, a)):
        if kq[x["id"]].k_syn >= 2 and kq[z["id"]].k_syn == 0 and x["gold"] == z["gold"]: dn += 1
add("dneg_with_twin_ge2pct", dn / len(yn) >= 0.02, "target", n=dn, rate=round(dn / len(yn), 4))
# twins (XF03): rows in T1/T2 contrast sets (base + label-flip twin) 22 +/- 2 of all rows
tw = [r for r in rows if r["meta"].get("twin_kind") == "premise"]
inset = {r["id"] for r in tw} | {r["meta"]["twin_of"] for r in tw}
flip = sum(1 for r in tw if byid.get(r["meta"]["twin_of"]) and byid[r["meta"]["twin_of"]]["gold"] != r["gold"])
ok, p = band_ok(len(inset), len(rows), .20, .24)
add("twin_share_22pm2", ok, "target", n_rows_in_sets=len(inset), rate=round(len(inset) / len(rows), 4), p=p, n_t1_twins=len(tw),
    t1_label_flip=flip, n_t2=0)
att = sum(1 for r in rows if r["meta"].get("twin_kind") == "attack")
add("attack_share_about_5pct", 0.03 <= att / len(rows) <= 0.07, "target", n=att, rate=round(att / len(rows), 4))
# option buckets 35/35/15/15 of choice rows
bc = Counter(q.bucket(len(r["options"])) for r in ch)
bad = [b for b, t in (("2-4", .35), ("5-9", .35), ("10-19", .15), ("20-60", .15)) if not band_ok(bc[b], len(ch), t - .02, t + .02)[0]]
add("option_bucket_shares", not bad, "target", counts=dict(bc), fails=bad)
add("difficulty_bins_present", False, "pending", note="meta.difficulty_bin null on all rows; bin strata and crowd shares not checkable")
dep = Counter(r["meta"]["depth"] for r in rows); deep = sum(1 for r in rows if r["meta"]["deep"])
add("deep_le_10pct", deep / len(rows) <= 0.10, "target", depth_counts=dict(dep), deep=deep)
# selection-adjusted display (POOL): reweight gold classes per k to the display-rule targets, then the display rate
for a, f in (("nei", .10), ("none", .05)):
    bad = []
    byk = defaultdict(list)
    for r in oc: byk[len(r["options"])].append(r)
    for k, rr in sorted(byk.items()):
        if k < 3: continue
        t = {"nei": min(.1, 1 / k), "none": min(.05, 1 / k)}; t["concrete"] = 1 - t["nei"] - t["none"]
        pc = Counter(okind(r["gold"]) for r in rr); n = len(rr)
        w = {c: (t[c] / (pc[c] / n) if pc[c] else 0) for c in t}; W = sum(w[okind(r["gold"])] for r in rr)
        s = sum(w[okind(r["gold"])] for r in rr if any(okind(o) == a for o in r["options"])) / W
        tgt = min(1.0, f * k); xs = round(s * n)
        ok, p = band_ok(xs, n, tgt - .02, tgt + .02) if tgt < 1 else (s > 0.999, None)
        if not ok: bad.append({"k": k, "n": n, "adj_shown": round(s, 3), "target": round(tgt, 3), "p": p})
    add(f"abstain_display_rate_selection_adjusted[{a}]", not bad, "pool", fails=bad,
        note="gold class reweighted per k to display-rule targets; display given gold class is a row property")
# option buckets: the pool must hold enough rows per bucket and per form for the r1 table (C-OUT k up to 32)
need = {"2-4": 630, "5-9": 630, "10-19": 270, "20-60": 270}
fc = Counter((S(r).get("form"), q.bucket(len(r["options"]))) for r in ch)
short = {b: [bc[b], v] for b, v in need.items() if bc[b] < v}
cout_need = {"2-4": 306, "5-9": 522, "10-19": 162, "20-60": 90}
cshort = {b: [fc[("c_out", b)], v] for b, v in cout_need.items() if fc[("c_out", b)] < v}
add("option_buckets_feasible", not short and not cshort, "pool", pool_vs_r1_need=short, c_out_pool_vs_r1_need=cshort,
    c_out_k_max=max(len(r["options"]) for r in ch if S(r).get("form") == "c_out"))
res = {"gate": "G10", "file": f"out/{NAME}.jsonl", "n_rows": len(rows), "n_yes_no": len(yn), "n_choice": len(ch), "n_sel": N_SEL,
       "pool_fail": [c["check"] for c in CHK if c["kind"] == "pool" and not c["pass"]],
       "target_fail": [c["check"] for c in CHK if c["kind"] == "target" and not c["pass"]], "checks": CHK}
json.dump(res, open(q.QC / f"g10_{NAME}.json", "w"), indent=1)
print("pool_fail", res["pool_fail"]); print("target_fail", res["target_fail"])
