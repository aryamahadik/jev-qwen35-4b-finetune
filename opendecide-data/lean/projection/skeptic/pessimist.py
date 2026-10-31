"""PESSIMIST re-run of projection/model/project.py (read-only; 30 Sep 2026).
Re-implements the same chain with every assumption as a parameter. First reproduces the base projection (check), then
applies pessimist corrections one at a time and all together. Sign: GAP = ours - Jev (pp); BRIER = ours - Jev.
Run: python3 projection/skeptic/pessimist.py > projection/skeptic/pessimist_out.txt"""
import numpy as np

N = 400_000
W_YN, W_CH = 716 / 1852, 1136 / 1852
# ---- pools: (value, rows) from projection/recompute/ohs1_out.txt and ohs2_out.txt (v11c, ours - Jev) ----
YN_CLASS = {"ohs2 ibm_argq": (-0.83, 120), "ohs1 cuad": (-0.62, 80), "ohs1 hatecheck": (-3.10, 145),
            "ohs1 overruling": (+5.00, 40), "ohs1 tinad": (+3.06, 180)}
YN_RULE = {"ohs2 moral_stories": (-12.50, 120), "ohs2 tabfact": (-8.33, 120), "ohs1 legalbench_hearsay": (-29.27, 82)}
CH_TOPIC = {"ohs1 qbio": (-5.83, 60), "ohs1 physics": (-1.67, 60), "ohs1 econqfin": (-1.67, 60), "ohs1 condmat": (+7.50, 60),
            "ohs2 math": (-3.33, 60), "ohs2 astro": (-3.33, 60), "ohs2 stat_eess": (+1.67, 60), "ohs2 cs": (+6.67, 60),
            "ohs2 big_patent": (-1.67, 120), "ohs2 medical_abstracts": (+3.33, 120), "ohs1 ledgar": (+1.67, 60),
            "ohs1 unfair_tos": (+1.88, 80), "ohs1 go_emotions": (-4.33, 150), "ohs1 sgd": (-1.50, 200), "ohs2 ddi2013": (+12.50, 120)}
CH_REASON = {"ohs1 vitaminc": (-7.75, 200), "ohs1 scone": (-8.06, 180), "ohs1 abercrombie": (-8.33, 60), "ohs1 pubmedqa": (-1.67, 150),
             "ohs2 scifact": (-7.08, 120), "ohs2 pubmed_rct": (-4.17, 120), "ohs2 evidence_inference": (0.00, 120)}
H_MI, H_YN, H_CH, H_BR = 1.6, 2.8, 1.85, 0.013
BASE = dict(p_rule=0.30, p_reason=0.10, jit=(3.0, 2.5), shift_sd=1.0, row_weight=False, drop=(), ch_shift=0.0,
            inc_yn=(1.52, 2.26), inc_ch=(0.41, 0.63), rho_med=0.9, rho_sd=0.6, rho_shared=False,
            gw=(0.15, 0.15, 0.25, 0.30, 0.15), c_pass=(0.9, 0.8), g2=(4.0, 3.8), hard=(0.0, 0.5),
            casc=(0.0, 0.8), br_a=0.007, comp_ratio=(1.25, 1.9), dd4=(-1.0, 4.0), dd2=(0.0, 4.0),
            hij=(0.97, 0.97, 0.97), inj=(0.70, 0.45, 0.50), host=0.85, spd_ok=(0.95, 0.85, 0.80), spd_bad=(0.05, 0.05, 0.03),
            cost_jb=(0.97, 0.97, 0.75), jb=(0.93, 0.80, 0.88))


def run(seed=0, **kw):
    p = dict(BASE); p.update(kw)
    rng = np.random.default_rng(seed)

    def pool(d):
        d = {k: v for k, v in d.items() if k not in p["drop"]}
        v = np.array([x[0] for x in d.values()]); w = np.array([x[1] for x in d.values()], float)
        return v, (w / w.sum() if p["row_weight"] else np.full(len(v), 1 / len(v)))

    def draw(a, b, pb, k, j):
        (va, wa), (vb, wb) = pool(a), pool(b)
        use = rng.random((N, k)) < pb
        xa = va[rng.choice(len(va), (N, k), p=wa)]; xb = vb[rng.choice(len(vb), (N, k), p=wb)]
        return (np.where(use, xb, xa) + rng.normal(0, j, (N, k))).mean(1)
    sh = rng.normal(0, p["shift_sd"], N)
    Byn = draw(YN_CLASS, YN_RULE, p["p_rule"], 5, p["jit"][0]) + sh
    Bch = draw(CH_TOPIC, CH_REASON, p["p_reason"], 8, p["jit"][1]) + sh + p["ch_shift"]
    rho = lambda: np.exp(rng.normal(np.log(p["rho_med"]), p["rho_sd"], N))
    rE = rho()
    ynE = Byn + rE * rng.uniform(*p["inc_yn"], N); chE = Bch + rE * rng.uniform(*p["inc_ch"], N)
    G = np.array([-0.5, 0.0, 0.5, 1.5, 2.5]); gw = np.array(p["gw"]) / sum(p["gw"])
    g = G[rng.choice(5, N, p=gw)] + rng.normal(0, 0.3, N)
    ship = (g + rng.normal(0, 0.6, N) >= 0.35) & (rng.random(N) < np.where(g >= 0, *p["c_pass"]))
    rN = rE if p["rho_shared"] else rho()
    ny = np.where(ship, rN * 1.2 * g, 0.0); nc = np.where(ship, rN * 0.75 * g, 0.0)
    yn4, ch4 = ynE + ny, chE + nc; mi4 = W_YN * yn4 + W_CH * ch4
    z = rng.normal(0, 1, N); kap = rng.uniform(0.3, 0.8, N)
    yn2 = ynE + kap * ny - (p["g2"][0] + 1.5 * (0.8 * z + 0.6 * rng.normal(0, 1, N))) + rng.uniform(*p["hard"], N)
    ch2 = chE + kap * nc - (p["g2"][1] + 1.3 * (0.8 * z + 0.6 * rng.normal(0, 1, N)))
    mi2 = W_YN * yn2 + W_CH * ch2
    dl = rng.uniform(*p["casc"], N); ynC, chC = yn4 - 1.2 * dl, ch4 - 0.85 * dl; miC = W_YN * ynC + W_CH * chC
    # Brier (same fit as project.py; intercept mean is the parameter under attack)
    X = np.array([-4.08, -6.55, -6.17, -7.22, -8.89]); Y = np.array([.0308, .0343, .0471, .0452, .0525])
    b_fit, a_fit = np.polyfit(X, Y, 1); rs = np.sqrt(np.sum((Y - (a_fit + b_fit * X)) ** 2) / 3)
    br = lambda yn, lo, hi: rng.normal(p["br_a"], 0.007, N) + rng.normal(-0.0053, 0.001, N) * yn + rng.normal(0, rs, N) - rng.uniform(lo, hi, N)
    br4, br2, brC = br(yn4, 0, 0.001), br(yn2, 0.001, 0.003), br(ynC, 0, 0.002)
    common = np.exp(rng.normal(0, 0.3, N))
    cv = lambda rate, yn: rate * rng.uniform(*p["comp_ratio"], N) * common * np.exp(rng.normal(0, 0.35, N)) * np.exp(-0.04 * (yn - np.median(yn)))
    vj = 10.8 * common * np.exp(rng.normal(0, 0.35, N))
    dv4 = cv(np.where(ship, 4.81 * (1 - 0.08 * np.clip(g, 0, None)), 4.81), yn4) - vj + rng.normal(0, 2.2, N)
    dv2 = cv(rng.uniform(7.0, 10.8, N), yn2) - vj + rng.normal(0, 2.2, N); dvC = 0.5 * dv4 + 0.5 * dv2
    dd4, dd2 = rng.normal(*p["dd4"], N), rng.normal(*p["dd2"], N); ddC = 0.5 * (dd4 + dd2)
    host = rng.random(N) < p["host"]
    out = {}
    for i, (s, mi, yn, ch, b, dv, dd) in enumerate((("4B", mi4, yn4, ch4, br4, dv4, dd4), ("2B", mi2, yn2, ch2, br2, dv2, dd2),
                                                    ("CASC", miC, ynC, chC, brC, dvC, ddC))):
        hij = rng.random(N) < p["hij"][i]; inj = rng.random(N) < p["inj"][i]
        spd = rng.random(N) < np.where(host, p["spd_ok"][i], p["spd_bad"][i])
        cjb = rng.random(N) < p["cost_jb"][i]; jb = rng.random(N) < p["jb"][i]
        match = mi - H_MI > -2.0
        cons = (dv <= 0) & (dd <= 0)
        out[s] = dict(med=np.median(mi), q10=np.percentile(mi, 10), q90=np.percentile(mi, 90), p0=np.mean(mi >= 0),
                      pm=np.mean(match), pns=np.mean(mi > -H_MI), yn_med=np.median(yn), pyn=np.mean(yn >= 0),
                      ch_med=np.median(ch), pch=np.mean(ch >= 0), br_med=np.median(b), pbr=np.mean(b + H_BR < 0.010),
                      pcomp=np.mean(dv <= 0), pcons=np.mean(cons), pspd=np.mean(spd),
                      owner=np.mean(match & hij & inj & spd & cjb & jb),
                      allw=np.mean(match & (yn >= 0) & (ch >= 0) & cons & hij & inj & spd & cjb & jb))
    out["ship"] = np.mean(ship)
    return out


def show(name, o):
    a = o["4B"]; b = o["2B"]; c = o["CASC"]
    print(f"{name:58s} {a['med']:+6.2f} [{a['q10']:+5.1f},{a['q90']:+5.1f}] {a['p0']:.2f} {a['pm']:.2f} {a['pns']:.2f} | yn {a['yn_med']:+5.2f} {a['pyn']:.2f}"
          f" ch {a['ch_med']:+5.2f} {a['pch']:.2f} | Br {a['pbr']:.2f} comp {a['pcomp']:.2f} cons {a['pcons']:.2f} | owner {a['owner']:.2f} all {a['allw']:.3f}"
          f" || 2B {b['med']:+5.2f} {b['p0']:.2f} own {b['owner']:.2f} | casc {c['med']:+5.2f} {c['p0']:.2f} own {c['owner']:.2f} | ship {o['ship']:.2f}")


print("cols: 4B micro median [80%] P(>=0) P(matches) P(not sig worse) | yes/no med P | choice med P | Brier P(matches) complement P consistency-both P |"
      " owner-success all-conditions || 2B micro med P owner | cascade med P owner | P(new 4B ships)")
show("BASE (should reproduce project_out.txt)", run())
one = [
    ("S1 yes/no class pool row-weighted, TINAD dropped", dict(row_weight=True, drop=("ohs1 tinad",))),
    ("S2 P(rule-like yes/no) 0.40 (past base rate 3/8)", dict(p_rule=0.40)),
    ("S3 choice pool without ddi2013 (1-task outlier)", dict(drop=("ohs2 ddi2013",))),
    ("S4 wide-option shift -0.65 on choice (25% rows x -2.6)", dict(ch_shift=-0.65)),
    ("S5 4B-E dev gain = dev-select only (winner's curse)", dict(inc_yn=(1.40, 1.64), inc_ch=(0.35, 0.47))),
    ("S6 transfer ratio median 0.65, sd(log) 0.7", dict(rho_med=0.65, rho_sd=0.7)),
    ("S7 same rho for both steps (not independent)", dict(rho_shared=True)),
    ("S8 g weights (0.20,0.25,0.25,0.22,0.08)", dict(gw=(0.20, 0.25, 0.25, 0.22, 0.08))),
    ("S9 constraints pass 0.75/0.65 (REF-lineage seen sources)", dict(c_pass=(0.75, 0.65))),
    ("S10 2B held-out gap N(5.0)/N(4.6) (kd x1.24, JB x1.6)", dict(g2=(5.0, 4.6))),
    ("S11 Brier intercept = fitted +0.0136", dict(br_a=0.0136)),
    ("S12 complement dev->OHS ratio U(1.7,2.4) (novel frames)", dict(comp_ratio=(1.7, 2.4))),
    ("S13 option-order drift prior 0.5/0.4", dict(dd4=(0.0, 4.0), dd2=(1.0, 4.0))),
    ("S14 injection 0.60 / 0.25 / 0.40", dict(inj=(0.60, 0.25, 0.40))),
    ("S15 hosting 0.75; speed|host 0.90/0.75/0.70", dict(host=0.75, spd_ok=(0.90, 0.75, 0.70))),
    ("S16 JevBench = sealed/board proxy 0.40/0.20/0.30", dict(jb=(0.40, 0.20, 0.30))),
]
for n, kw in one:
    show(n, run(**kw))
ACC = dict(row_weight=True, drop=("ohs1 tinad",), p_rule=0.40, ch_shift=-0.65, inc_yn=(1.40, 1.64), inc_ch=(0.35, 0.47),
           rho_med=0.65, rho_sd=0.7, gw=(0.20, 0.25, 0.25, 0.22, 0.08), c_pass=(0.75, 0.65), g2=(5.0, 4.6))  # S1,S2,S4-S6,S8-S10
ALL = dict(ACC, br_a=0.0136, comp_ratio=(1.7, 2.4), dd4=(0.0, 4.0), dd2=(1.0, 4.0), inj=(0.60, 0.25, 0.40), host=0.75,
           spd_ok=(0.90, 0.75, 0.70))                                                                        # + S11-S15
print()
show("PESSIMIST accuracy chain (S1,S2,S4,S5,S6,S8,S9,S10)", run(**ACC))
show("  same, but S3 (drop ddi2013) instead of S4", run(**dict(ACC, ch_shift=0.0, drop=("ohs1 tinad", "ohs2 ddi2013"))))
show("PESSIMIST all but board (S1-S2,S4-S15)", run(**ALL))
show("PESSIMIST all incl. board JevBench (+S16)", run(**dict(ALL, jb=(0.40, 0.20, 0.30))))
MID = dict(row_weight=True, drop=("ohs1 tinad",), p_rule=0.375, inc_yn=(1.40, 1.64), inc_ch=(0.35, 0.47), rho_med=0.75, rho_sd=0.65,
           gw=(0.18, 0.20, 0.25, 0.27, 0.10), c_pass=(0.8, 0.7), g2=(4.6, 4.3), br_a=0.010, comp_ratio=(1.5, 2.2),
           dd4=(-0.5, 4.0), inj=(0.65, 0.30, 0.45), host=0.8, spd_ok=(0.92, 0.8, 0.75))
show("MODERATE-PESSIMIST (halfway settings)", run(**MID))
for s in (1, 2):
    show(f"  seed {s} check of PESSIMIST S1-S15", run(seed=s, **ALL))
print()
show("GROUP task-mix only (S1+S2)", run(row_weight=True, drop=("ohs1 tinad",), p_rule=0.40))
show("GROUP task-mix + choice (S1+S2+S4)", run(row_weight=True, drop=("ohs1 tinad",), p_rule=0.40, ch_shift=-0.65))
show("GROUP our-gain side only (S5+S6+S8+S9)", run(inc_yn=(1.40, 1.64), inc_ch=(0.35, 0.47), rho_med=0.65, rho_sd=0.7,
                                                   gw=(0.20, 0.25, 0.25, 0.22, 0.08), c_pass=(0.75, 0.65)))
show("CASCADE cost coupled: budget r~0.65 -> JB cost loses (cost_jb casc 0.40)", run(**dict(MID, cost_jb=(0.97, 0.97, 0.40))))
