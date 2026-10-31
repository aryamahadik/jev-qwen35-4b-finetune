"""G10 balance (independent F13 checker, check:F13, c-lanes-v3). C_DATA_SPEC v4 2.1 / 8 G10 + F13 G0 10 ("G10 balance
targets"). Counts only, never row text. Usage: chk_g10.py <name>
Part A (pool-level; gated on candidates_r1; qc_sample reported):
 v4 / 2.1: yes/no share 45-55%; per-card yes rate 20-80 (cards with >= 10 yes/no rows); syntactic negation (shared
 negcount k_syn on the question) >= 10% and double negation (k_syn >= 2) with an affirmative twin in its unit (same
 call_id or relation partner with lower k_syn) >= 2% of yes/no rows; gold letter uniform per option bucket (stored
 order; chi-square, p > 0.01); "longest option is gold" within +/- 2 pp of mean 1/k (ties split); abstain options wrong
 on >= 2/3 of the rows that show them (G0 XF01; v4 >= 50%) and gold at 1/k +/- 2 pp per k bucket and abstain option
 (a cell outside fails only if binomial p <= 0.01); attack present uncorrelated with the label (yes/no Fisher; choice
 gold-is-abstain Fisher and gold relative position chi-square; p > 0.01); option buckets 35/35/15/15 +/- 3 pp;
 label-flip twin sets 20-25% of rows (report; G0 9 counts it after selection); attack rows about 5% (3-7%).
 F13 G0 10: length bins 50/30/20 +/- 3 pp per sampler; state_tokens >= 2,000 and n_tokens <= 7,850; decisive count
 non-AG 1/2/3 = 50/35/15 +/- 3, AG 2/3 = 60/40 +/- 5, label independent of count and case location (chi-square
 p > 0.01); decisive decile 10 +/- 2 pp per decile (family) and uniform per sampler x length bin (p > 0.01);
 near-miss >= 1 per row, kinds V/R/I 33 +/- 5, decile uniform (p > 0.01), |corr(near-miss decile, decisive decile)| <
 0.05; aggregate 20 +/- 2 of rows, 15-25 per sampler, AG-1/2/3 33 +/- 5 of AG rows; skills Q-P 30 / Q-R 30 / Q-T 25 /
 Q-D 15 +/- 3; open-world cards 50 +/- 5; traces 1-3 per row with >= 1 T-B or T-D; yes rate 50 +/- 3 per length bin x
 skill (binomial p <= 0.01 to fail); attack decile uniform and the attack-named option gold on 1/k (binomial p > 0.01;
 named option read from the lines the attack twin adds to its base); numeric gold rank and gold mention-count rank
 uniform (chi-square p > 0.01); masked 10-15% / swapped about 5% of choice rows, few-shot 5-10% and inverted 10-15% of
 cards (detected from the text); "yes = bad" polarity 50 +/- 5 (needs the G0 12 sidecar `polarity`).
 Items whose G0 12 sidecar field is missing and which the text cannot settle are listed in `not_verifiable` and fail.
Part B (after-selection cells): yes rate per wording x k_all cell (difficulty bin pooled: G9 not run). Feasibility:
 an exactly balanced selection inside every cell (min(yes, no) of each label kept) must keep >= 45% of the planned
 round-1 F13 rows (2,050) as yes/no rows, and the balanced yes/no rows must be >= 45% of the kept rows."""
import json, re, sys, math
from collections import Counter, defaultdict
import numpy as np
from scipy.stats import chisquare, binomtest, fisher_exact, chi2_contingency
import chk_lib as q
sys.path.insert(0, str(q.LEAN / "c_src/common"))
import negcount  # noqa: E402

NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows, side = q.load(NAME)
S = lambda r: side.get(r["id"]) or {}
yn = [r for r in rows if q.is_yn(r)]; ch = [r for r in rows if not q.is_yn(r)]
n = len(rows); P = {}; R = {}; NV = {}


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def within(x, lo, hi):
    return x is not None and lo <= x <= hi


def chi_unif(counts):
    c = [x for x in counts]
    if sum(c) < 5 * len(c) or len(c) < 2:
        return None
    return float(chisquare(c).pvalue)


# ---- yes/no share, per-card yes rate
R["yes_no_share_pct"] = pct(len(yn), n); P["yes_no_share_45_55"] = within(R["yes_no_share_pct"], 45, 55)
cy = defaultdict(lambda: [0, 0])
for r in yn:
    c = cy[r["meta"]["card_id"]]; c[0] += 1; c[1] += int(r["gold"])
rates = {c: v[1] / v[0] for c, v in cy.items() if v[0] >= 10}
R["per_card_yes_rate"] = {"cards_ge10": len(rates), "min": round(min(rates.values()), 3) if rates else None,
                          "max": round(max(rates.values()), 3) if rates else None,
                          "outside_20_80": sum(not (0.2 <= v <= 0.8) for v in rates.values())}
P["per_card_yes_20_80"] = R["per_card_yes_rate"]["outside_20_80"] == 0
R["yes_rate_pct"] = pct(sum(int(r["gold"]) for r in yn), len(yn))

# ---- negation (question only)
qo = {r["id"]: q.qtext(r, S(r)) for r in yn}
ks = {i: negcount.k_syn(t) for i, t in qo.items()}; ka = {i: negcount.k_all(t) for i, t in qo.items()}
rel = q.relations(NAME); part = defaultdict(set)
for x in rel:
    part[x["a"]].add(x["b"]); part[x["b"]].add(x["a"])
bycall = defaultdict(list)
for r in rows:
    bycall[r["call_id"]].append(r["id"])
grp = defaultdict(list)
for r in rows:
    grp[r["group_id"]].append(r["id"])
neg1 = sum(v >= 1 for v in ks.values())
dn = 0
for r in yn:
    if ks[r["id"]] >= 2:
        mates = part[r["id"]] | set(bycall[r["call_id"]]) | set(grp[r["group_id"]])
        if any(m != r["id"] and m in ks and ks[m] < ks[r["id"]] for m in mates):
            dn += 1
R["negation"] = {"k_syn_ge1_pct": pct(neg1, len(yn)), "k_syn_ge2_with_affirmative_twin_pct": pct(dn, len(yn)),
                 "k_syn_ge2_pct": pct(sum(v >= 2 for v in ks.values()), len(yn))}
P["negation_ge10"] = (R["negation"]["k_syn_ge1_pct"] or 0) >= 10
P["double_negation_twin_ge2"] = (R["negation"]["k_syn_ge2_with_affirmative_twin_pct"] or 0) >= 2

# ---- option buckets, gold letter, longest option
bk = Counter(q.bucket(len(r["options"])) for r in ch)
R["option_buckets_pct"] = {b: pct(bk.get(b, 0), len(ch)) for b in ("2-4", "5-9", "10-19", "20-60")}
tgt = {"2-4": 35, "5-9": 35, "10-19": 15, "20-60": 15}
P["option_buckets_35_35_15_15"] = all(within(R["option_buckets_pct"][b], t - 3, t + 3) for b, t in tgt.items())
gl = {}
for b in tgt:
    rs = [r for r in ch if q.bucket(len(r["options"])) == b]
    if not rs:
        continue
    if b == "2-4":
        sub = {}
        for k in (3, 4):
            rk = [r for r in rs if len(r["options"]) == k]
            if rk:
                c = Counter(q.gold_index(r) for r in rk); sub[k] = chi_unif([c.get(i, 0) for i in range(k)])
        ps = [v for v in sub.values() if v is not None]
        gl[b] = {"n": len(rs), "p_by_k": sub, "pass": all(p > 0.01 for p in ps)}
    else:
        # relative position (decile of gold index / k) for mixed k
        c = Counter(min(9, int(10 * q.gold_index(r) / len(r["options"]))) for r in rs)
        exp = np.zeros(10)
        for r in rs:
            k = len(r["options"])
            for i in range(k):
                exp[min(9, int(10 * i / k))] += 1 / k
        obs = np.array([c.get(i, 0) for i in range(10)], float); m = exp > 0
        p = float(chisquare(obs[m], exp[m] * obs.sum() / exp[m].sum()).pvalue) if len(rs) >= 30 else None
        gl[b] = {"n": len(rs), "p_rel_pos": p, "pass": p is None or p > 0.01}
R["gold_letter_uniform"] = gl; P["gold_letter_uniform"] = all(v["pass"] for v in gl.values())
lg, ek = 0.0, 0.0
for r in ch:
    L = [len(o) for o in r["options"]]; mx = max(L); t = [i for i, x in enumerate(L) if x == mx]
    lg += (q.gold_index(r) in t) / len(t); ek += 1 / len(r["options"])
R["longest_is_gold"] = {"rate": round(lg / len(ch), 4), "mean_1_over_k": round(ek / len(ch), 4)}
P["longest_option_within_2pp"] = abs(lg - ek) / len(ch) <= 0.02

# ---- abstain options
ab = {}
okab = True
for o, nm in ((q.NEI, "NEI"), (q.NONE, "None")):
    rs = [r for r in ch if o in r["options"]]
    if not rs:
        continue
    g = sum(r["gold"] == o for r in rs)
    cells = {}
    for b in tgt:
        rb = [r for r in rs if q.bucket(len(r["options"])) == b]
        if len(rb) < 20:
            continue
        gb = sum(r["gold"] == o for r in rb); e = sum(1 / len(r["options"]) for r in rb) / len(rb)
        p = float(binomtest(gb, len(rb), e).pvalue)
        cells[b] = {"n": len(rb), "gold_pct": pct(gb, len(rb)), "exp_pct": round(100 * e, 2), "p": round(p, 5),
                    "pass": abs(gb / len(rb) - e) <= 0.02 or p > 0.01}
    ab[nm] = {"rows_shown": len(rs), "gold": g, "wrong_pct": pct(len(rs) - g, len(rs)), "cells": cells}
    okab &= (len(rs) - g) / len(rs) >= 2 / 3 and all(c["pass"] for c in cells.values())
ow = [r for r in ch if S(r).get("world") == "open"]; cw = [r for r in ch if S(r).get("world") == "closed"]
ab["NEI_on_every_open_choice_row"] = sum(q.NEI in r["options"] for r in ow) == len(ow)
ab["None_on_every_closed_choice_row_k_ge3"] = sum(q.NONE in r["options"] for r in cw if len(r["options"]) >= 3) == sum(
    len(r["options"]) >= 3 for r in cw)
R["abstain"] = ab
P["abstain"] = okab and ab["NEI_on_every_open_choice_row"] and ab["None_on_every_closed_choice_row_k_ge3"]

# ---- attack
byid = {r["id"]: r for r in rows}
att = [r for r in rows if r["meta"].get("twin_kind") == "attack"]
R["attack_rows_pct"] = pct(len(att), n); P["attack_rows_about_5pct"] = within(R["attack_rows_pct"], 3, 7)
A = {}
a_yn = [int(r["meta"].get("twin_kind") == "attack") for r in yn]
t = [[sum(1 for a, r in zip(a_yn, yn) if a and r["gold"] == 1), sum(1 for a, r in zip(a_yn, yn) if a and r["gold"] == 0)],
     [sum(1 for a, r in zip(a_yn, yn) if not a and r["gold"] == 1), sum(1 for a, r in zip(a_yn, yn) if not a and r["gold"] == 0)]]
A["yes_no_fisher_p"] = float(fisher_exact(t)[1])
a_ch = [int(r["meta"].get("twin_kind") == "attack") for r in ch]
ga = [int(r["gold"] in (q.NEI, q.NONE)) for r in ch]
t2 = [[sum(1 for a, g in zip(a_ch, ga) if a and g), sum(1 for a, g in zip(a_ch, ga) if a and not g)],
      [sum(1 for a, g in zip(a_ch, ga) if not a and g), sum(1 for a, g in zip(a_ch, ga) if not a and not g)]]
A["choice_gold_abstain_fisher_p"] = float(fisher_exact(t2)[1])
tab = np.zeros((2, 3))
for a, r in zip(a_ch, ch):
    tab[a, min(2, int(3 * q.gold_index(r) / len(r["options"])))] += 1
A["choice_gold_relpos_chi2_p"] = float(chi2_contingency(tab)[1]) if tab.min() > 0 else None
named_g, named_e, named_n, dec = 0, 0.0, 0, Counter(); unk = 0
for r in att:
    base = [byid[b] for b in part[r["id"]] if b in byid]
    if not base:
        unk += 1; continue
    bl = set(base[0]["state"].splitlines())
    lines = r["state"].splitlines(); add = [(i, l) for i, l in enumerate(lines) if l not in bl and l.strip()]
    if not add:
        unk += 1; continue
    pos = r["state"].find(add[0][1]); dec[min(9, int(10 * pos / max(1, len(r["state"]))))] += 1
    txt = " ".join(l for _, l in add).lower()
    opts = ["yes", "no"] if q.is_yn(r) else r["options"]
    hit = [o for o in opts if re.search(r"(?<![\w-])" + re.escape(o.lower()) + r"(?![\w-])", txt)]
    if len(hit) == 1:
        named_n += 1; named_e += 1 / len(opts)
        g = ("yes" if r["gold"] == 1 else "no") if q.is_yn(r) else r["gold"]
        named_g += int(hit[0] == g)
A["named_option"] = {"rows_resolved": named_n, "gold_hits": named_g, "expected": round(named_e, 1),
                     "p": float(binomtest(named_g, named_n, named_e / named_n).pvalue) if named_n else None, "unresolved": unk}
A["attack_decile_counts"] = [dec.get(i, 0) for i in range(10)]
A["attack_decile_p"] = chi_unif(A["attack_decile_counts"])
R["attack"] = A
P["attack_uncorrelated_with_label"] = (A["yes_no_fisher_p"] > 0.01 and A["choice_gold_abstain_fisher_p"] > 0.01
                                       and (A["choice_gold_relpos_chi2_p"] or 1) > 0.01
                                       and (A["named_option"]["p"] is None or A["named_option"]["p"] > 0.01))
P["attack_decile_uniform"] = A["attack_decile_p"] is None or A["attack_decile_p"] > 0.01

# ---- twins
tk = Counter(r["meta"].get("twin_kind") for r in rows)
flip_kinds = {"neg", "dneg", "inner_neg", "delete_nei", "nm_activate", "boundary_flip"}
sets = defaultdict(set)
for r in rows:
    sets[r["group_id"]].add(r["meta"].get("twin_kind"))
in_flip = sum(1 for r in rows if sets[r["group_id"]] & flip_kinds)
R["twins"] = {"twin_kind_rows": dict(tk), "rows_in_label_flip_sets_pct": pct(in_flip, n),
              "move_pair_rows_pct": pct(2 * tk.get("move", 0), n)}
P["move_pairs_le_5pct"] = R["twins"]["move_pair_rows_pct"] <= 5
R["twins"]["note"] = "20-25% label-flip set share is judged after selection (G0 9); reported here"

# ---- F13 G0 10 structure targets
smp = sorted({r["meta"]["sampler"] for r in rows})
lb = {}
okl = True
for s_ in smp:
    rs = [r for r in rows if r["meta"]["sampler"] == s_]; c = Counter(q.lbin(r["meta"].get("state_tokens")) for r in rs)
    lb[s_] = {b: pct(c.get(b, 0), len(rs)) for b in ("2-4K", "4-6K", "6-7.9K")}
    okl &= all(within(lb[s_][b], t_ - 3, t_ + 3) for b, t_ in (("2-4K", 50), ("4-6K", 30), ("6-7.9K", 20)))
R["length_bins_pct"] = lb; P["length_bins_per_sampler"] = okl
R["length_limits"] = {"state_tokens_lt_2000": sum((r["meta"].get("state_tokens") or 0) < 2000 for r in rows),
                      "n_tokens_gt_7850": sum((r["meta"].get("n_tokens") or 0) > 7850 for r in rows)}
P["length_limits"] = not any(R["length_limits"].values())
ag = [r for r in rows if r["meta"].get("subtype") == "aggregate"]; nag = [r for r in rows if r["meta"].get("subtype") != "aggregate"]
dc = Counter(int(S(r).get("decisive_n") or 0) for r in nag); dca = Counter(int(S(r).get("decisive_n") or 0) for r in ag)
R["decisive_count_pct"] = {"non_ag": {k: pct(dc.get(k, 0), len(nag)) for k in (1, 2, 3)},
                           "ag": {k: pct(dca.get(k, 0), len(ag)) for k in (2, 3)}, "other": {
                               "non_ag": sum(v for k, v in dc.items() if k not in (1, 2, 3)), "ag": sum(v for k, v in dca.items() if k not in (2, 3))}}
P["decisive_count"] = (all(within(R["decisive_count_pct"]["non_ag"][k], t_ - 3, t_ + 3) for k, t_ in ((1, 50), (2, 35), (3, 15)))
                       and all(within(R["decisive_count_pct"]["ag"][k], t_ - 5, t_ + 5) for k, t_ in ((2, 60), (3, 40))))


def lab(r):
    return ("y" if r["gold"] == 1 else "n") if q.is_yn(r) else ("abst" if r["gold"] in (q.NEI, q.NONE) else "val")


def indep(key, rs, labf):
    tab = defaultdict(Counter)
    for r in rs:
        tab[key(r)][labf(r)] += 1
    ks_ = sorted(tab); ls = sorted({l for v in tab.values() for l in v})
    M = np.array([[tab[k][l] for l in ls] for k in ks_], float)
    M = M[M.sum(1) >= 20]
    if M.shape[0] < 2:
        return None
    M = M[:, M.sum(0) > 0]
    return float(chi2_contingency(M)[1]) if M.shape[1] >= 2 else None


# per form: yes/no label vs key; choice: gold-is-abstain vs key. Rows with decisive count 0 (no decisive section, e.g.
# deletion twins) are left out of the count test (their abstain gold is by construction), reported separately.
yl = lambda r: int(r["gold"]); cl = lambda r: int(r["gold"] in (q.NEI, q.NONE))
dk = lambda r: str(S(r).get("decisive_n")) + ("A" if r["meta"].get("subtype") else "")
nz = lambda rs: [r for r in rs if int(S(r).get("decisive_n") or 0) > 0]
R["label_vs_decisive_count_p"] = {"yes_no": indep(dk, nz(yn), yl), "choice": indep(dk, nz(ch), cl),
                                  "rows_with_count_0": sum(int(S(r).get("decisive_n") or 0) == 0 for r in rows)}
R["label_vs_case_location_p"] = {"yes_no": indep(lambda r: str(S(r).get("case_loc")), yn, yl),
                                 "choice": indep(lambda r: str(S(r).get("case_loc")), ch, cl)}
pl = [v for d in (R["label_vs_decisive_count_p"], R["label_vs_case_location_p"]) for k, v in d.items() if k in ("yes_no", "choice")]
P["label_independent_of_count_and_case_loc"] = all(p is None or p > 0.01 for p in pl)
dd = Counter(); dsl = defaultdict(Counter)
for r in rows:
    for d in S(r).get("decisive_deciles") or []:
        dd[d] += 1; dsl[(r["meta"]["sampler"], q.lbin(r["meta"].get("state_tokens")))][d] += 1
tot = sum(dd.values())
R["decisive_decile_pct"] = [pct(dd.get(i, 0), tot) for i in range(10)]
cellp = {f"{a}|{b}": chi_unif([c.get(i, 0) for i in range(10)]) for (a, b), c in dsl.items()}
R["decisive_decile_cell_p_min"] = min((p for p in cellp.values() if p is not None), default=None)
R["decisive_decile_cells_failing"] = sorted(k for k, p in cellp.items() if p is not None and p <= 0.01)
P["decisive_decile"] = all(within(x, 8, 12) for x in R["decisive_decile_pct"]) and not R["decisive_decile_cells_failing"]
nmk = Counter(); nmd = Counter(); no_nm = 0; pairs = []
for r in rows:
    nm = S(r).get("nm") or []
    if not nm:
        no_nm += 1
    dds = S(r).get("decisive_deciles") or []
    for x in nm:
        nmk[x.get("kind")] += 1; nmd[x.get("decile")] += 1
        for d in dds:
            pairs.append((x.get("decile"), d))
tn = sum(nmk.values())
R["near_miss"] = {"rows_without": no_nm, "kinds_pct": {k: pct(v, tn) for k, v in nmk.items()},
                  "decile_counts": [nmd.get(i, 0) for i in range(10)], "decile_p": chi_unif([nmd.get(i, 0) for i in range(10)]),
                  "corr_with_decisive": round(float(np.corrcoef(np.array(pairs, float).T)[0, 1]), 4) if len(pairs) > 2 else None}
P["near_miss"] = (no_nm == 0 and all(within(R["near_miss"]["kinds_pct"].get(k), 28, 38) for k in ("V", "R", "I"))
                  and (R["near_miss"]["decile_p"] or 1) > 0.01 and abs(R["near_miss"]["corr_with_decisive"] or 0) < 0.05)
R["aggregate"] = {"pct": pct(len(ag), n), "per_sampler_pct": {s_: pct(sum(1 for r in ag if r["meta"]["sampler"] == s_),
                                                                     sum(1 for r in rows if r["meta"]["sampler"] == s_)) for s_ in smp},
                  "ag_kinds_pct": {k: pct(v, len(ag)) for k, v in Counter(str(S(r).get("kind"))[:3] for r in ag).items()},
                  "ag_subkinds_pct": {k: pct(v, len(ag)) for k, v in Counter(S(r).get("kind") for r in ag).items()},
                  "ag_yes_no_rows": sum(q.is_yn(r) for r in ag)}
P["aggregate"] = (within(R["aggregate"]["pct"], 18, 22) and all(within(v, 15, 25) for v in R["aggregate"]["per_sampler_pct"].values())
                  and all(within(R["aggregate"]["ag_kinds_pct"].get(k), 28, 38) for k in ("ag1", "ag2", "ag3"))
                  and R["aggregate"]["ag_yes_no_rows"] == 0)
sk = Counter(S(r).get("skill") for r in rows)
R["skills_pct"] = {k: pct(v, n) for k, v in sk.items()}
P["skills"] = all(within(R["skills_pct"].get(k), t_ - 3, t_ + 3) for k, t_ in (("QP", 30), ("QR", 30), ("QT", 25), ("QD", 15)))
cw_ = {}
for r in rows:
    cw_[r["meta"]["card_id"]] = S(r).get("world")
R["open_world_cards_pct"] = pct(sum(v == "open" for v in cw_.values()), len(cw_))
P["open_world_cards_50"] = within(R["open_world_cards_pct"], 45, 55)
tr_bad = sum(1 for r in rows if not (1 <= q.n_traces(S(r)) <= 3 and set(S(r).get("traces") or []) & {"TB", "TD"}))
R["traces_rows_failing"] = tr_bad; P["traces"] = tr_bad == 0
yc = {}
okc = True
for r in yn:
    yc.setdefault((q.lbin(r["meta"].get("state_tokens")), S(r).get("skill")), []).append(int(r["gold"]))
for kk, v in yc.items():
    p = float(binomtest(sum(v), len(v), 0.5).pvalue); fail = abs(np.mean(v) - 0.5) > 0.03 and p <= 0.01
    yc[kk] = {"n": len(v), "yes_pct": pct(sum(v), len(v)), "p": round(p, 5), "fail": bool(fail)}; okc &= not fail
R["yes_rate_lbin_x_skill"] = {f"{a}|{b}": v for (a, b), v in yc.items()}; P["yes_rate_lbin_x_skill"] = okc
# numeric gold rank and mention rank
nr = Counter(); nre = defaultdict(float); mr = Counter(); mre = defaultdict(float)
for r in ch:
    if r["gold"] in (q.NEI, q.NONE):
        continue
    da = [o for o in r["options"] if o not in (q.NEI, q.NONE)]
    nums = {o: q.as_num(o) for o in da}
    if len(da) >= 2 and all(v is not None for v in nums.values()):
        srt = sorted(da, key=lambda o: nums[o]); m = len(da)
        nr[min(2, int(3 * srt.index(r["gold"]) / m))] += 1
        for i in range(m):
            nre[min(2, int(3 * i / m))] += 1 / m
    mc = {o: q.mention_pos(r["state"], o)[0] for o in da}
    if len(da) >= 2:
        srt = sorted(da, key=lambda o: -mc[o]); m = len(da); top = [o for o in da if mc[o] == mc[srt[0]]]
        mr["max" if r["gold"] in top else "not_max"] += 1; mre["max"] += len(top) / m; mre["not_max"] += 1 - len(top) / m


def chi_exp(obs, exp):
    ks_ = sorted(exp); o = np.array([obs.get(k, 0) for k in ks_], float); e = np.array([exp[k] for k in ks_])
    return float(chisquare(o, e * o.sum() / e.sum()).pvalue) if o.sum() >= 30 else None


R["numeric_gold_rank"] = {"obs": dict(nr), "exp": {k: round(v, 1) for k, v in nre.items()}, "p": chi_exp(nr, nre)}
R["gold_mention_max"] = {"obs": dict(mr), "exp": {k: round(v, 1) for k, v in mre.items()}, "p": chi_exp(mr, mre)}
P["numeric_gold_rank_uniform"] = (R["numeric_gold_rank"]["p"] or 1) > 0.01
P["gold_mention_rank_uniform"] = (R["gold_mention_max"]["p"] or 1) > 0.01

# ---- card overlays read from the text (sidecar few_shot / names / polarity / inverted are absent: G0 12)
MASK = re.compile(r"^(?:[A-Z]{1,3}-?\d{1,3}|(?:code|label|class|type|category|outcome|option|group)\s+[A-Z0-9]{1,3})$", re.I)
masked = sum(1 for r in ch if any(MASK.match(o) for o in r["options"] if o not in (q.NEI, q.NONE)))
INV = re.compile(r"(?i)\bwhich (?:of (?:these|the following) )?(?:\w+ ){0,4}(?:meets|satisf|qualif|would (?:get|receive)|gets|receives|has the outcome)")
inv_cards = {r["meta"]["card_id"] for r in ch if INV.search(S(r).get("question") or "")}
FEW = re.compile(r"(?i)\b(?:worked example|example excerpt|few-shot|example document|excerpt \d|sample excerpt)")
few_cards = {r["meta"]["card_id"] for r in rows if FEW.search((r.get("card") or "") + "\n" + r["instructions"])}
nC = len({r["meta"]["card_id"] for r in rows})
R["overlays_from_text"] = {"masked_choice_rows_pct": pct(masked, len(ch)), "inverted_cards_pct": pct(len(inv_cards), nC),
                           "few_shot_cards_pct": pct(len(few_cards), nC),
                           "note": "detected from the visible text by regex (sidecar fields few_shot / names / inverted missing)"}
P["masked_10_15"] = within(R["overlays_from_text"]["masked_choice_rows_pct"], 10, 15)
P["inverted_cards_10_15"] = within(R["overlays_from_text"]["inverted_cards_pct"], 10, 15)
P["few_shot_cards_5_10"] = within(R["overlays_from_text"]["few_shot_cards_pct"], 5, 10)
NV["swapped_names_about_5pct"] = "sidecar `names` missing; a swapped name (familiar word, other definition) is not detectable from text"
NV["yes_eq_bad_polarity_50"] = "sidecar `polarity` missing (G0 10 / 12 per-row polarity); not computable from text"
NV["establish_no_contradicted_vs_undetermined_50"] = "needs frame + contradicted / undetermined flag (sidecar date / frame fields missing)"
NV["settle_yes_true_vs_false_50"] = "needs the settle frame's inner-claim truth value (not in the sidecar)"
NV["role_symmetry"] = "needs date_role / governing_date / question_date (sidecar fields missing)"
NV["difficulty_shares"] = "G9 not run (difficulty_bin null); judged after selection"
R["not_verifiable"] = NV
for k in NV:
    if k != "difficulty_shares":
        P["verifiable:" + k] = False

# repair r3 (builder): r3 sidecars carry the G0 12 fields `names` (plain / masked / swapped per row), `few_shot` (shown
# on the row) and `frame_claim` (establish / settle effective claim: true / false / open); judge those parts from the
# sidecar (the text regex above stays as a reported cross-check). Marker: every row has `skill_q` (r3 build).
if rows and all("skill_q" in S(r) for r in rows):
    nmc = Counter(S(r).get("names") for r in ch)
    few_sc = {r["meta"]["card_id"] for r in rows if S(r).get("few_shot")}
    est = Counter(S(r).get("frame_claim") for r in rows if S(r).get("form") == "establish")
    stl = Counter(S(r).get("frame_claim") for r in rows if S(r).get("form") == "settle")
    R["overlays_sidecar"] = {"masked_choice_rows_pct": pct(nmc["masked"], len(ch)),
                             "swapped_choice_rows_pct": pct(nmc["swapped"], len(ch)),
                             "few_shot_cards_pct": pct(len(few_sc), nC),
                             "establish_no_contradicted_pct": pct(est["false"], est["false"] + est["open"]),
                             "settle_yes_true_pct": pct(stl["true"], stl["true"] + stl["false"]),
                             "n_establish_no": est["false"] + est["open"], "n_settle_yes": stl["true"] + stl["false"]}
    O = R["overlays_sidecar"]
    P["masked_10_15"] = within(O["masked_choice_rows_pct"], 10, 15)
    P["few_shot_cards_5_10"] = within(O["few_shot_cards_pct"], 5, 10)
    P["verifiable:swapped_names_about_5pct"] = within(O["swapped_choice_rows_pct"], 3, 7)
    P["verifiable:establish_no_contradicted_vs_undetermined_50"] = within(O["establish_no_contradicted_pct"], 45, 55)
    P["verifiable:settle_yes_true_vs_false_50"] = within(O["settle_yes_true_pct"], 45, 55)
    for k in ("swapped_names_about_5pct", "establish_no_contradicted_vs_undetermined_50", "settle_yes_true_vs_false_50"):
        NV.pop(k, None)

# repair r4 (builder): sidecar `date_role` / `question_date` / `governing_date` on every row, `ver_latest` on S1 Q-R /
# AG-2 version rows (G0 2.6: in-force version = latest-dated version on 50% +/- 5). S2 / S3 / S6 version rows carry no
# flag yet (their decision / log builders), so role symmetry stays partly not verifiable.
if rows and all("date_role" in S(r) for r in rows):
    vl = Counter(S(r).get("ver_latest") for r in rows if S(r).get("ver_latest") is not None and not S(r).get("base_id"))
    dr = Counter(S(r).get("date_role") for r in rows)
    R["role_symmetry_sidecar"] = {"S1_qdate_version_rows": vl[True] + vl[False],
                                  "S1_latest_dated_gold_pct": pct(vl[True], vl[True] + vl[False]),
                                  "date_role_counts": dict(dr)}
    P["verifiable:role_symmetry_S1_qdate_latest_50"] = within(R["role_symmetry_sidecar"]["S1_latest_dated_gold_pct"],
                                                             45, 55)
    NV["role_symmetry"] = "S1 question-date rows judged from sidecar ver_latest; S2 / S3 / S6 version rows and " \
                          "governing-date rows not flagged yet"

# repair r6 (builder): sidecar `polarity` (G0 10 / 12, F13R2-17, XF04) on every yes/no row: "Yes = bad" = adverse share
# of ALL yes/no rows 50 +/- 5; neutral rows <= 5% of yes/no rows (count as not-bad). Label split reported.
if yn and all(S(r).get("polarity") in ("adverse", "favourable", "neutral") for r in yn):
    pc = Counter(S(r)["polarity"] for r in yn)
    pyes = [S(r)["polarity"] == "adverse" for r in yn if r["gold"] in ("yes", True, 1)]
    pno = [S(r)["polarity"] == "adverse" for r in yn if r["gold"] not in ("yes", True, 1)]
    R["polarity_sidecar"] = {"adverse_pct": pct(pc["adverse"], len(yn)), "neutral_pct": pct(pc["neutral"], len(yn)),
                             "counts": dict(pc), "adverse_pct_gold_yes": pct(sum(pyes), len(pyes)),
                             "adverse_pct_gold_no": pct(sum(pno), len(pno))}
    P["verifiable:yes_eq_bad_polarity_50"] = within(R["polarity_sidecar"]["adverse_pct"], 45, 55) and \
        R["polarity_sidecar"]["neutral_pct"] <= 5
    NV.pop("yes_eq_bad_polarity_50", None)

# ---- Part B: after-selection wording x k_all cells
cell = defaultdict(lambda: [0, 0])
for r in yn:
    c = cell[(r["meta"]["wording_id"], ka[r["id"]])]; c[0] += 1; c[1] += int(r["gold"])
kept_yn = sum(2 * min(y, m - y) for m, y in cell.values())
kept_ch = len(ch)
R["partB"] = {"cells": len(cell), "yes_no_rows": len(yn), "balanced_yes_no_rows_kept": kept_yn,
              "share_of_kept_pct": pct(kept_yn, kept_yn + kept_ch), "planned_r1_rows": 2050,
              "cells_off_50_by_gt2pp": sum(1 for m, y in cell.values() if abs(y / m - 0.5) > 0.02)}
P["partB_cell_balance_feasible"] = kept_yn >= 0.45 * 2050 and (kept_yn / (kept_yn + kept_ch)) >= 0.45

out = {"gate": "G10", "file": f"out/{NAME}.jsonl", "pool_sha256": q.sha(q.OUT / f"{NAME}.jsonl"), "rows": n,
       "yes_no_rows": len(yn), "choice_rows": len(ch), "results": R, "pass_parts": P, "pass": all(P.values())}
(q.QC / f"g10_{NAME}.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({"pass": out["pass"], "failed": [k for k, v in P.items() if not v]}))
