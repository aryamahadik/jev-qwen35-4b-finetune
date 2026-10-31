"""OHS-3 / JevBench projection model (read-only; 30 Sep 2026). Every input is a named constant with its source.
Nothing here reads OHS-3 items. Sign convention everywhere: GAP = ours - Jev (pp; positive = we are better),
BRIER_DIFF = ours - Jev (positive = we are worse). Run: python3 projection/model/project.py
"""
import numpy as np

rng = np.random.default_rng(0)
N = 400_000

# ---------------- 1. Baseline: a v11c-class 4B on a new exam, built from per-task gaps we measured ----------------
# Per-task gaps of q35_4b_v11c (_cal) vs Jev (mean of 2 runs), ours - Jev, from projection/recompute/ohs1_out.txt and
# ohs2_out.txt (sign flipped from their "gap" column).
YN_CLASS = {"ohs2 ibm_argq": -0.83, "ohs1 cuad": -0.62, "ohs1 hatecheck": -3.10, "ohs1 overruling": +5.00, "ohs1 tinad": +3.06}
YN_RULE = {"ohs2 moral_stories": -12.50, "ohs2 tabfact": -8.33, "ohs1 legalbench_hearsay": -29.27}
CH_TOPIC = {"ohs1 qbio": -5.83, "ohs1 physics": -1.67, "ohs1 econqfin": -1.67, "ohs1 condmat": +7.50, "ohs2 math": -3.33,
            "ohs2 astro": -3.33, "ohs2 stat_eess": +1.67, "ohs2 cs": +6.67, "ohs2 big_patent": -1.67,
            "ohs2 medical_abstracts": +3.33, "ohs1 ledgar": +1.67, "ohs1 unfair_tos": +1.88, "ohs1 go_emotions": -4.33,
            "ohs1 sgd": -1.50, "ohs2 ddi2013": +12.50}
CH_REASON = {"ohs1 vitaminc": -7.75, "ohs1 scone": -8.06, "ohs1 abercrombie": -8.33, "ohs1 pubmedqa": -1.67,
             "ohs2 scifact": -7.08, "ohs2 pubmed_rct": -4.17, "ohs2 evidence_inference": 0.00}
# OHS-3 composition (PREREG_OHS3.md:10-31; data/ohs3_summary.json): 5 yes/no tasks (716 rows), 8 choice tasks (1,136).
W_YN, W_CH = 716 / 1852, 1136 / 1852
N_YN_TASKS, N_CH_TASKS = 5, 8
# EST (judgement from task descriptions in PREREG_OHS3 only): chance that an OHS-3 yes/no task behaves like a
# rule-application task (hearsay/moral/tabfact) rather than a classification-like one. openfda_recall_class
# (21 CFR severity rule) is the clearest rule task; nvd_attack_vector is in between; ct/zenodo/CNC are label checks.
P_RULE = 0.30
P_REASON_CH = 0.10          # all 8 OHS-3 choice tasks are label-set / topical classification
JIT_YN, JIT_CH = 3.0, 2.5   # EST: a new task is not a copy of a pooled task
EXAM_SHIFT = 1.0            # EST: exam-level common shift (card wording, Jev familiarity with U-track corpora)


def draw_pool(pool_a, pool_b, p_b, n_tasks, jit):
    a, b = np.array(list(pool_a.values())), np.array(list(pool_b.values()))
    use_b = rng.random((N, n_tasks)) < p_b
    va = a[rng.integers(0, len(a), (N, n_tasks))]
    vb = b[rng.integers(0, len(b), (N, n_tasks))]
    return (np.where(use_b, vb, va) + rng.normal(0, jit, (N, n_tasks))).mean(1)


shift = rng.normal(0, EXAM_SHIFT, N)
B_yn = draw_pool(YN_CLASS, YN_RULE, P_RULE, N_YN_TASKS, JIT_YN) + shift
B_ch = draw_pool(CH_TOPIC, CH_REASON, P_REASON_CH, N_CH_TASKS, JIT_CH) + shift

# ---------------- 2. v11c -> 4B-E held-out increment ----------------
# Dev gains v11c -> 4B-E (projection/recompute/dev_out.txt): yes/no select +1.52, pooled +2.26; choice select +0.41,
# pooled +0.63. Transfer ratio rho (held-out gain / dev gain): observed 1.35 (OHS-2, v10->v11c), 1.5 / 2.2 / 0.26
# (OHS-1 steps; OHS-1 guided v11 data, ledger A7), ~0.03 (frozen->v10). EST: lognormal, median 0.9, sd(log) 0.6
# -> 80% interval about [0.42, 1.95].
def rho():
    return np.exp(rng.normal(np.log(0.9), 0.6, N))


rE = rho()
inc_yn = rE * rng.uniform(1.52, 2.26, N)
inc_ch = rE * rng.uniform(0.41, 0.63, N)

# ---------------- 3. New 4B (q35_4b_main500k) over 4B-E, gated by the ship rule ----------------
# EST scenario weights for the TRUE dev gain g over 4B-E (see projection.md section 2 for the reasoning).
G_VALS = np.array([-0.5, 0.0, 0.5, 1.5, 2.5])
G_PROB = np.array([0.15, 0.15, 0.25, 0.30, 0.15])
g = G_VALS[rng.choice(len(G_VALS), N, p=G_PROB)] + rng.normal(0, 0.3, N)
# Ship rule (PREREG_FINAL 3.2/3.5): primary diff >= +0.2 and LB > -0.75. For two 4Bs the primary half-width is about
# +-1.1 (sd about 0.6), so LB > -0.75 needs an observed diff >= about +0.35. Constraints (b)-(g) pass w.p. 0.9 (0.8
# when the model is truly worse) - EST.
d_obs = g + rng.normal(0, 0.6, N)
ship = (d_obs >= 0.35) & (rng.random(N) < np.where(g >= 0, 0.9, 0.8))
rN = rho()
YN_SHARE_MULT, CH_SHARE_MULT = 1.2, 0.75   # EST: golden set is 64.6% yes/no; 4B-E's own dev gain was yes/no-heavy
new_yn = np.where(ship, rN * YN_SHARE_MULT * g, 0.0)
new_ch = np.where(ship, rN * CH_SHARE_MULT * g, 0.0)

yn4 = B_yn + inc_yn + new_yn
ch4 = B_ch + inc_ch + new_ch
mi4 = W_YN * yn4 + W_CH * ch4
yn4E = B_yn + inc_yn; ch4E = B_ch + inc_ch; mi4E = W_YN * yn4E + W_CH * ch4E

# ---------------- 4. Final 2B (PRISM-X I, teacher 4B-E) ----------------
# 2B - teacher gap on dev: matched distillation v11c->v11r yes/no -2.80, choice -3.72 (pooled, dev_out.txt);
# unmatched I_1600 vs 4B-E yes/no -5.77, choice -5.16. The final 2B gets 19x I_1600's steps (2B step-doubling
# evidence: +1.3 / +3.0 per doubling at 800->1600, about +0.8 at 1.5K->3.7K). Held-out amplification for v11r:
# JevBench-A -5.1 vs dev -3.2 (x1.6), eval_card wide -3.3 (x1.0). EST: held-out gap to 4B-E ~ N(4.0, 1.5) yes/no,
# N(3.8, 1.3) choice, correlated (common factor).
z = rng.normal(0, 1, N)
G2_yn = 4.0 + 1.5 * (0.8 * z + 0.6 * rng.normal(0, 1, N))
G2_ch = 3.8 + 1.3 * (0.8 * z + 0.6 * rng.normal(0, 1, N))
kappa = rng.uniform(0.3, 0.8, N)            # EST: share of the new 4B's data gain the 2B also gets from the same gold rows
HARD_ROWS = rng.uniform(0.0, 0.5, N)        # EST: new program-labelled hard yes/no rows; verifier says ~0 on OHS-3
yn2 = yn4E + kappa * new_yn - G2_yn + HARD_ROWS
ch2 = ch4E + kappa * new_ch - G2_ch
mi2 = W_YN * yn2 + W_CH * ch2

# ---------------- 5. Cascade (2B first, least-sure rows to the final 4B) ----------------
# projection/model/cascade_ext_out.txt: with a 2B gap of -3.9 (v11r->v13t) the cascade = 4B from 40% routing
# (+0.02 [-0.76,+0.88]); with -5.3 to -6.3 it is -1.0 at 40%, -0.5 at 60%, -0.25 at 70%. The plan's rule picks the
# smallest budget with select LB > -0.5 (FINETUNE_PLAN 5.3). EST held-out loss vs the 4B: U(0, 0.8), yes/no 1.2x.
dl = rng.uniform(0.0, 0.8, N)
ynC, chC = yn4 - 1.2 * dl, ch4 - 0.85 * dl
miC = W_YN * ynC + W_CH * chC

# ---------------- 6. Brier (yes/no; PREREG_OHS3 primary endpoint 3) ----------------
# Fit on the 5 measured (yes/no acc gap, Brier diff) pairs: OHS-1 v11c (-4.08,+.0308), v11b (-6.55,+.0343),
# v10 (-6.17,+.0471); OHS-2 v11c (-7.22,+.0452), v10 (-8.89,+.0525).
X = np.array([-4.08, -6.55, -6.17, -7.22, -8.89]); Y = np.array([.0308, .0343, .0471, .0452, .0525])
b_fit, a_fit = np.polyfit(X, Y, 1)
resid_sd = np.sqrt(np.sum((Y - (a_fit + b_fit * X)) ** 2) / 3)


# The fitted intercept (Brier gap at EQUAL yes/no accuracy) is an extrapolation from x in [-8.9, -4.1]: se about
# 0.011. Cross-set evidence says equal accuracy gives about equal Brier (Jev OHS-1 83.97% -> 0.1142; 4B-E dev
# 84.45% -> 0.1143; 4B-E beats Jev on JevBench Noul 0.070 vs 0.105 and jagged clean 0.032 vs 0.096). EST: intercept
# N(0.007, 0.007) (midway), slope N(-0.0053, 0.001) (fit -0.0043; dev 4B family v10 -> 4B-E about -0.0065).
A_BR, B_BR = 0.007, -0.0053


def brier(yn, cal_lo, cal_hi):
    a = rng.normal(A_BR, 0.007, N); b = rng.normal(B_BR, 0.001, N)
    return a + b * yn + rng.normal(0, resid_sd, N) - rng.uniform(cal_lo, cal_hi, N)


# dev-fitted T gain: 4B-E 0.0003-0.0006 (dev_out.txt; FINETUNE_PLAN 5.1); 2B I_1600 0.0022 on confirm.
br4, br2, brC = brier(yn4, 0.0, 0.001), brier(yn2, 0.001, 0.003), brier(ynC, 0.0, 0.002)

# ---------------- 7. Consistency: complement violation on the 300 _neg pairs ----------------
# Dev complement violation (projection/evidence.md s5): 4B-E 4.81%, v11r 8.11%, I_1600 10.78%. Dev -> OHS-1 ratio
# 1.25-1.9 (v10, v11b, v11c). Jev on OHS-1 about 10.8% (runs 11.05 / 10.53). OHS-3 frames (T1-T6, clause negation) are
# new for both systems: common novelty factor plus system-specific factors (EST). Violations also rise when yes/no
# accuracy falls (EST 4% relative per pp). Sampling noise of a paired difference on 300 pairs: sd about 2.2 pp.
common = np.exp(rng.normal(0, 0.3, N))


def comp_viol(dev_rate, yn):
    return dev_rate * rng.uniform(1.25, 1.9, N) * common * np.exp(rng.normal(0, 0.35, N)) * np.exp(-0.04 * (yn - np.median(yn)))


v_jev = 10.8 * common * np.exp(rng.normal(0, 0.35, N))
dv4 = comp_viol(np.where(ship, 4.81 * (1 - 0.08 * np.clip(g, 0, None)), 4.81), yn4) - v_jev + rng.normal(0, 2.2, N)
dv2 = comp_viol(rng.uniform(7.0, 10.8, N), yn2) - v_jev + rng.normal(0, 2.2, N)
dvC = (0.5 * (dv4 + v_jev) + 0.5 * (dv2 + v_jev)) - v_jev   # EST: routed half from each
# Option-order drift on 304 _perm pairs: NEVER measured for anyone. EST prior only.
dd4, dd2 = rng.normal(-1.0, 4.0, N), rng.normal(0.0, 4.0, N); ddC = 0.5 * (dd4 + dd2)

# ---------------- 8. Decision rules (PREREG_OHS3.md:122-127) ----------------
H_MI, H_YN, H_CH, H_BR = 1.6, 2.8, 1.85, 0.013   # 95% half-widths scaled from OHS-1/OHS-2 by sqrt(n) (EST)


def summ(name, v, h=None, lo_bar=None):
    q = np.percentile(v, [10, 50, 90])
    s = f"{name:26s} median {q[1]:+6.2f}  80% [{q[0]:+6.2f}, {q[2]:+6.2f}]  P(>=0) {np.mean(v >= 0):.2f}"
    if h is not None:
        s += f"  P(not sig. worse) {np.mean(v > -h):.2f}"
    if lo_bar is not None:
        s += f"  P(PREREG matches) {np.mean(v - h > lo_bar):.2f}"
    print(s)


print(f"Brier fit: diff = {a_fit:+.4f} + {b_fit:+.5f} * yes/no gap (pp); resid sd {resid_sd:.4f}; used: intercept N({A_BR}, 0.007), slope N({B_BR}, 0.001)")
print(f"new 4B ships in {np.mean(ship):.2f} of draws; mean shipped dev gain {np.mean(np.where(ship, g, 0)):+.2f}")
print("\n--- v11c-class baseline and 4B-E (for reference) ---")
summ("v11c-class micro", W_YN * B_yn + W_CH * B_ch, H_MI, -2.0); summ("v11c-class yes/no", B_yn, H_YN); summ("v11c-class choice", B_ch, H_CH)
summ("4B-E micro", mi4E, H_MI, -2.0); summ("4B-E yes/no", yn4E, H_YN); summ("4B-E choice", ch4E, H_CH)
res = {}
for sysname, mi, yn, ch, br, dv, dd in (("FINAL 4B", mi4, yn4, ch4, br4, dv4, dd4), ("FINAL 2B", mi2, yn2, ch2, br2, dv2, dd2),
                                        ("CASCADE", miC, ynC, chC, brC, dvC, ddC)):
    print(f"\n--- {sysname} (ours - Jev) ---")
    summ("micro accuracy", mi, H_MI, -2.0); summ("yes/no accuracy", yn, H_YN); summ("choice accuracy", ch, H_CH)
    q = np.percentile(br, [10, 50, 90])
    print(f"{'Brier diff (ours-Jev)':26s} median {q[1]:+.4f}  80% [{q[0]:+.4f}, {q[2]:+.4f}]  P(<=0) {np.mean(br <= 0):.2f}"
          f"  P(PREREG matches: diff+{H_BR} < 0.010) {np.mean(br + H_BR < 0.010):.2f}  P(not sig. worse) {np.mean(br - H_BR <= 0):.2f}")
    q = np.percentile(dv, [10, 50, 90])
    print(f"{'complement viol. diff':26s} median {q[1]:+.2f} pp  80% [{q[0]:+.2f}, {q[2]:+.2f}]  P(ours <= Jev) {np.mean(dv <= 0):.2f}")
    print(f"{'option-order drift diff':26s} prior only: P(ours <= Jev) {np.mean(dd <= 0):.2f}")
    res[sysname] = dict(mi=mi, yn=yn, ch=ch, br=br, dv=dv, dd=dd)

# ---------------- 9. Non-accuracy metrics (EST probabilities; reasoning in projection.md) ----------------
P = {  # (hijack, injection point <= Jev, speed | proper hosting, speed | no proper hosting, cost JevBench formula,
       #  cost real serving, JevBench Score A public)
    "FINAL 4B": dict(hij=0.97, inj=0.70, spd_ok=0.95, spd_bad=0.05, cost_jb=0.97, cost_real=0.50, jb=0.93),
    "FINAL 2B": dict(hij=0.97, inj=0.45, spd_ok=0.85, spd_bad=0.05, cost_jb=0.97, cost_real=0.30, jb=0.80),
    "CASCADE": dict(hij=0.97, inj=0.50, spd_ok=0.80, spd_bad=0.03, cost_jb=0.75, cost_real=0.20, jb=0.88),
}
P_HOSTING = 0.85   # EST: warm GPU + direct connection (tunnel or co-located), CUDA graphs for the 4B, measured before OHS-3
host = rng.random(N) < P_HOSTING
print("\n--- joint probabilities (accuracy part simulated; other parts EST Bernoulli, speed/cost share hosting) ---")
for s, p in P.items():
    r = res[s]
    hij = rng.random(N) < p["hij"]; inj = rng.random(N) < p["inj"]
    spd = rng.random(N) < np.where(host, p["spd_ok"], p["spd_bad"])
    cost_jb = rng.random(N) < p["cost_jb"]; cost_real = rng.random(N) < np.where(host, p["cost_real"], p["cost_real"] * 0.5)
    jbw = rng.random(N) < p["jb"]
    acc_strict, acc_match, acc_lenient = r["mi"] >= 0, r["mi"] - H_MI > -2.0, r["mi"] > -H_MI
    yn_closed, ch_nodrop = r["yn"] >= 0, r["ch"] >= 0
    cons = (r["dv"] <= 0) & (r["dd"] <= 0)
    owner = lambda acc, cost: np.mean(acc & hij & inj & spd & cost & jbw)
    allw = np.mean(acc_match & yn_closed & ch_nodrop & cons & hij & inj & spd & cost_jb & jbw)
    allw_cal = np.mean(acc_match & yn_closed & ch_nodrop & cons & hij & inj & spd & cost_jb & jbw & (r["br"] + H_BR < 0.010))
    print(f"{s:9s} owner-success: acc 'matches' {owner(acc_match, cost_jb):.2f} | acc not-sig-worse {owner(acc_lenient, cost_jb):.2f}"
          f" | acc point>=0 {owner(acc_strict, cost_jb):.2f} | 'matches' + real-serving cost {owner(acc_match, cost_real):.2f}")
    print(f"{'':9s} all win conditions: {allw:.3f} (with Brier 'matches' too: {allw_cal:.3f});"
          f" parts: acc-matches {acc_match.mean():.2f}, yes/no>=0 {yn_closed.mean():.2f}, choice>=0 {ch_nodrop.mean():.2f},"
          f" consistency both {cons.mean():.2f}, speed {spd.mean():.2f}")
# conditional: final 4B given the new 4B ships vs not
print(f"\nfinal 4B micro median | shipped {np.median(mi4[ship]):+.2f} (P>=0 {np.mean(mi4[ship] >= 0):.2f}) | not shipped "
      f"{np.median(mi4[~ship]):+.2f} (P>=0 {np.mean(mi4[~ship] >= 0):.2f})")
for gv in G_VALS:
    m = np.abs(g - gv) < 0.3
    print(f"  scenario g~{gv:+.1f}: P(ship) {np.mean(ship[m]):.2f}  micro median {np.median(mi4[m]):+.2f}  yes/no {np.median(yn4[m]):+.2f}"
          f"  choice {np.median(ch4[m]):+.2f}  P(micro>=0) {np.mean(mi4[m] >= 0):.2f}  P(matches) {np.mean(mi4[m] - H_MI > -2):.2f}")
