"""Monte Carlo for the C gate in C_TRAIN_RECIPE.md v3 (sections 6 and 10). CPU only, no data read.

Every number is an ASSUMPTION stated in the recipe (section 10.1), except the dev standard errors, which were MEASURED on
C-like 4B pairs by nearnull_calib.py (v11b/v11c vs v11, 7.6-8.3% of dev rows answered differently: full set 0.43-0.46,
yes/no 0.62-0.67, choice 0.51-0.56, dev-unseen 0.49-0.53 pp). The output is a rough guide, not a measurement.
v2 of this script is kept as gate_sim_c_v2.py.
Run: python3 gate_sim_c.py
"""
import numpy as np

N = 400_000
SE_YN, SE_CH, SE_UN = 0.65, 0.53, 0.51        # measured; the full-set noise is their row-weighted mean (SE about 0.43)
W_YN = 3867 / 7056                             # yes/no share of the 7,056-row full set
N_A, SEL_FRAC = 5000, 0.4                      # sealed part A items; select share (sha256 mod 5 in {0, 1})


def se_sealed(n, d=0.10, cf=1.2):
    """paired SE (pp) of CAND - REF on n items at disagreement rate d and cluster factor cf"""
    return 100 * cf * np.sqrt(d / n)


def guards(rng, d, n, harm=True, prereg=False, full_thr=-1.5):
    """No-harm guards D1-D6 (recipe 6.4; also the no-harm half of the round-2 rule). d = true dev full-set effect.
    harm=True adds realistic true side effects (sub-type, unseen-set, Brier, flips, attack); harm=False = noise only.
    prereg=True applies PREREG_FINAL 3.3 unchanged: (a) LB > -1.0, (a2) each dev half >= -0.75, v2's D2 LB > -1.25."""
    z = (lambda s: rng.normal(0, s, n)) if harm else (lambda s: 0.0)
    yn = d + z(0.4) + rng.normal(0, SE_YN, n)
    ch = d + z(0.4) + rng.normal(0, SE_CH, n)
    full = W_YN * yn + (1 - W_YN) * ch
    se_full = np.sqrt((W_YN * SE_YN) ** 2 + ((1 - W_YN) * SE_CH) ** 2)
    ok = (yn >= -1.0) & (ch >= -1.0)                                      # D3 = PREREG (b), (c)
    un = 0.4 * d + z(0.5) + rng.normal(0, SE_UN, n)
    if prereg:
        e = rng.normal(0, se_full, n)
        ok &= (full - 1.96 * se_full > -1.0) & (full + e >= -0.75) & (full - e >= -0.75)
        ok &= un - 1.96 * SE_UN > -1.25
    else:
        ok &= full - 1.96 * se_full > full_thr                           # D1 non-inferiority
        ok &= ~((un < -1.0) & (un + 1.96 * SE_UN < 0))                   # D2 clear-harm veto
    ok &= z(0.002) + rng.normal(0, 0.0015, n) <= 0.005                   # D4 calibrated Brier
    ok &= (-0.3 + z(1.2)) * (1 if harm else 0) + rng.normal(0, 1.0, n) <= 2.0   # D5a equivalence flips
    ok &= z(0.5) + rng.normal(0, 0.3, n) <= 2.0                         # D5b permutation flips (option order)
    if harm:
        ok &= rng.random(n) >= 0.02                                      # D6 jagged/OPI: true harm in 2% of runs
    return ok


def p1_pass(conf, se, rule):
    if rule == "lb95":
        return (conf >= 1.0) & (conf - 1.96 * se > 0)
    if rule == "lb90":
        return (conf >= 1.0) & (conf - 1.645 * se > 0)
    return (conf >= 0.5) & (conf - 1.96 * se > -1.0)                     # v2 rule


def sealed_vetoes(rng, tf, n_a, n_dom=9, dom_sd=1.5, harm=True):
    n = len(tf)
    sd_dom = se_sealed(n_a / n_dom)
    dom = tf[:, None] + (rng.normal(0, dom_sd, (n, n_dom)) if harm else 0.0)
    p2 = ~((dom + rng.normal(0, sd_dom, (n, n_dom)) + 1.96 * sd_dom) < -2.0).any(1)
    pb = rng.normal(2.5, 2.0, n) if harm else np.full(n, 2.5)
    p3 = ~((pb + rng.normal(0, 1.7, n) + 1.96 * 1.7) < 0)
    return p2 & p3


def power_curve(n_conf, rule="lb95", dev=0.3, prereg=False, full_thr=-1.5, n_a=N_A, seed=1):
    """P(ship) of the confirm stage for a FIXED finalist with true sealed gain g, true dev effect dev, and NO true
    harm anywhere else (noise only): the power of the ship gate."""
    rng = np.random.default_rng(seed)
    se = se_sealed(n_conf)
    out = {}
    for g in (-1.0, 0.0, 1.0, 1.5, 2.0, 2.5, 3.0):
        tf = np.full(N, g)
        conf = tf + rng.normal(0, se, N)
        ok = p1_pass(conf, se, rule) & sealed_vetoes(rng, tf, n_a, harm=False) & \
            guards(rng, np.full(N, dev), N, harm=False, prereg=prereg, full_thr=full_thr)
        out[g] = ok.mean()
    return se, out


def guard_oc(seed=3):
    """Operating characteristic of the dev accuracy guards (D1-D3) alone, noise only: P(pass) by true uniform dev
    effect."""
    rng = np.random.default_rng(seed)
    res = {}
    for name, pr, thr in (("v3 (D1 LB > -1.5, a2 report-only, D2 clear-harm)", False, -1.5),
                          ("v3 with D1 LB > -1.25", False, -1.25), ("PREREG 3.3 unchanged + v2 D2", True, -1.0)):
        res[name] = {d: guards(rng, np.full(N, d), N, harm=False, prereg=pr, full_thr=thr).mean()
                     for d in (-1.5, -1.0, -0.5, 0.0, 0.3, 0.5)}
    return res


def r1_curve(n_sel, dev=0.3, seed=2):
    rng = np.random.default_rng(seed)
    se = se_sealed(n_sel)
    return se, {g: ((g + (s := rng.normal(0, se, N)) >= 2.0) & (g + s - 1.96 * se > 0)
                    & guards(rng, np.full(N, dev), N, harm=False)).mean() for g in (0.0, 1.0, 1.5, 2.0, 2.5, 3.0)}


def run(seed=0, n_a=N_A, sel_frac=SEL_FRAC, d_far=0.10, mu_g2=1.0, sd_g2=1.56, dev_mu=0.3, dev_sd=0.6, g0_ohs=-1.0,
        rho=0.6, rho_gd=0.0, rule="lb95", prereg=False, full_thr=-1.5):
    rng = np.random.default_rng(seed)
    se_s, se_c = se_sealed(n_a * sel_frac, d_far), se_sealed(n_a * (1 - sel_frac), d_far)
    g2 = rng.normal(mu_g2, sd_g2, N)                       # round-2 candidate (final step): true sealed part-A gain
    g1 = 0.7 * g2 + rng.normal(0, 0.5, N)                  # round-1 candidate (half the new data)
    zg = (g1 - g1.mean()) / g1.std()
    d1 = dev_mu + dev_sd * (rho_gd * zg + np.sqrt(1 - rho_gd ** 2) * rng.standard_normal(N))
    d2 = 0.7 * d1 + rng.normal(dev_mu * 0.3, dev_sd * 0.7, N)
    shared = rng.normal(0, se_s * np.sqrt(rho), N)         # both candidates are read on the same select items
    s1 = g1 + shared + rng.normal(0, se_s * np.sqrt(1 - rho), N)
    s2 = g2 + shared + rng.normal(0, se_s * np.sqrt(1 - rho), N)
    go2 = (s1 >= 2.0) & (s1 - 1.96 * se_s > 0) & guards(rng, d1, N, prereg=prereg, full_thr=full_thr)
    pick2 = go2 & (s2 + 0.3 >= s1)                         # finalist: better select read; within 0.3 -> round 2
    tf = np.where(pick2, g2, g1)
    df = np.where(pick2, d2, d1)
    conf = tf + rng.normal(0, se_c, N)                     # the one confirm look
    ship = p1_pass(conf, se_c, rule) & sealed_vetoes(rng, tf, n_a) & guards(rng, df, N, prereg=prereg, full_thr=full_thr)
    h = 0.6 * tf + rng.normal(0, 0.8, N)                   # finalist's true OHS-like gain
    # C1's true OHS-3 gap = practice gap + set-to-set spread (SD 1.0, incl. the practice read's own SE) ; OHS-3 read SE 1.0
    ohs_obs = g0_ohs + np.where(ship, h, 0.0) + rng.normal(0, 1.0, N) + rng.normal(0, 1.0, N)
    e = rng.normal(1.0, 2.0, N)
    ejs_obs = np.where(ship, -4.4 + e + rng.normal(0, 1.75, N), -4.4)
    return {
        "SE sel/conf": (round(se_s, 2), round(se_c, 2)),
        "P(round 2 runs)": go2.mean(),
        "P(C ships)": ship.mean(),
        "P(ship | true >= +2)": ship[tf >= 2].mean(),
        "P(ship | true > +1)": ship[tf > 1].mean(),
        "P(ship | true <= 0)": ship[tf <= 0].mean(),
        "P(ship | true <= -1)": ship[tf <= -1].mean(),
        "E[true | ship]": tf[ship].mean(),
        "E[shipped gain]": np.where(ship, tf, 0.0).mean(),
        "OHS P(>= Jev-1)": (ohs_obs >= -1).mean(),
        "OHS P(>= Jev)": (ohs_obs >= 0).mean(),
        "OHS P(>= Jev+1)": (ohs_obs >= 1).mean(),
        "OHS median gap": float(np.median(ohs_obs)),
        "ejs5 P(>= Jev)": (ejs_obs >= 0).mean(),
        "ejs5 P(>= Jev-2)": (ejs_obs >= -2).mean(),
    }


def fmt(v):
    return str(v) if isinstance(v, tuple) else f"{v:.3f}"


if __name__ == "__main__":
    print("== Dev accuracy guards alone (noise only): P(pass) by true uniform dev effect")
    for k, v in guard_oc().items():
        print(f"  {k:52s} " + "  ".join(f"{d:+.1f}:{p:.2f}" for d, p in v.items()))
    print("== Ship-stage power (fixed finalist; no true harm elsewhere): P(ship) by true sealed gain")
    for n_conf in (2000, 2500, 3000):
        for dev in (0.0, 0.3):
            for rule, pr, thr in (("lb95", False, -1.5), ("lb90", False, -1.5), ("lb95", True, -1.0)):
                se, pc = power_curve(n_conf, rule, dev, pr, thr)
                tag = f"n_conf {n_conf} (SE {se:.2f}) dev {dev:+.1f} {rule} {'PREREG dev rules' if pr else 'v3 guards'}"
                print(f"  {tag:58s} " + "  ".join(f"{g:+.1f}:{p:.2f}" for g, p in pc.items()))
    for n_sel in (2000, 2500):
        se, rc = r1_curve(n_sel)
        print(f"== Round-2 rule, n_sel {n_sel} (SE {se:.2f}), dev +0.3, no harm: P(round 2 runs) by round-1 true gain")
        print("  " + "  ".join(f"{g:+.1f}:{p:.2f}" for g, p in rc.items()))
    print("== Whole plan under the prior (section 10.1)")
    for label, kw in [("BASE: part A 5,000, 40/60 split, d 0.10", {}),
                      ("part A 5,000, 50/50 split", {"sel_frac": 0.5}),
                      ("part A 6,000, 50/50 split", {"n_a": 6000, "sel_frac": 0.5}),
                      ("part A 4,000, 50/50 (v2 maximum)", {"n_a": 4000, "sel_frac": 0.5}),
                      ("part A 3,200, 50/50 (v2 minimum)", {"n_a": 3200, "sel_frac": 0.5}),
                      ("disagreement d 0.14", {"d_far": 0.14}),
                      ("disagreement d 0.07", {"d_far": 0.07}),
                      ("pessimistic gain (median +0.3)", {"mu_g2": 0.3}),
                      ("optimistic gain (median +1.8)", {"mu_g2": 1.8}),
                      ("dev neutral (mean 0.0)", {"dev_mu": 0.0}),
                      ("dev linked to sealed gain (rho 0.4)", {"rho_gd": 0.4}),
                      ("PREREG 3.3 dev rules unchanged", {"prereg": True}),
                      ("P1 one-sided 95% (lb90)", {"rule": "lb90"}),
                      ("v2 P1 (>= +0.5, LB > -1)", {"rule": "v2"}),
                      ("OHS start -1.2 (OHS-1)", {"g0_ohs": -1.2}),
                      ("OHS start -0.6 (OHS-2)", {"g0_ohs": -0.6}),
                      ("OHS start -2.2 (older 4Bs)", {"g0_ohs": -2.2})]:
        r = run(**kw)
        print(label)
        print("   " + "; ".join(f"{k} {fmt(v)}" for k, v in r.items()))
