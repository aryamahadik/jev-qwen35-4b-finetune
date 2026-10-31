"""Optimist re-run of the accuracy chain in projection/model/project.py (sections 1-5), same pools, same seed logic,
with ONE input changed at a time and then the defensible changes together. Read-only; no OHS-3 access.
Each change and its evidence:
  C1 per-task P(rule-like) = the projection's own task reading (projection.md s2): ct / zenodo / CNC label checks 0.10,
     openfda (21 CFR rule) 0.50, nvd (in between) 0.30 -> 1.1 expected rule tasks instead of 1.5.
  C2 4B-E's gain over v11c taken from the ship rule's unseen-source set (sources neither model trained on):
     yes/no U(+1.72 select, +2.68 both halves), choice U(+0.50, +0.85) (projection/optimist/o4_out.txt, o3_out.txt),
     instead of all-dev U(+1.52, +2.26) / U(+0.41, +0.63).
  C3 transfer ratio rho median 1.2 (sd(log) 0.6): the 4 fine-tune -> fine-tune steps seen on a held-out exam gave
     1.35 (OHS-2, clean), 1.5, 2.2, 0.26 (OHS-1, which guided v11 data), median 1.4; only frozen -> v10 (first
     fine-tune) was ~0.03 (evidence.md s12). Relative to the unseen-source set the observed ratios were 3.4 / 3.9 / 2.45.
  C4 new-4B scenario weights with P(g <= 0) = 0.20 instead of 0.30 (6.7x steps, 2.7x rows, 97% carded yes/no like
     OHS-3, OHS-3-shaped government-record sources in golden; still no measurement) - ARGUABLE.
  C5 SPECULATIVE: rule-task gaps x U(0.5, 1.0) on track-F yes/no tasks (every rule-pool loss was a classic U-track
     corpus where Jev beat published fine-tuned SOTA; on track F we tied Jev on both exams, choice only).
"""
import numpy as np
YN_CLASS = [-0.83, -0.62, -3.10, +5.00, +3.06]
YN_RULE = [-12.50, -8.33, -29.27]
CH_TOPIC = [-5.83, -1.67, -1.67, +7.50, -3.33, -3.33, +1.67, +6.67, -1.67, +3.33, +1.67, +1.88, -4.33, -1.50, +12.50]
CH_REASON = [-7.75, -8.06, -8.33, -1.67, -7.08, -4.17, 0.00]
W_YN, W_CH = 716 / 1852, 1136 / 1852
N = 400_000
# OHS-3 yes/no tasks in PREREG order: ct_study_type (F), openfda (F 91/U 53), nvd (F), zenodo (F), causal_news (U)
TRACK_F = np.array([1.0, 91 / 144, 1.0, 1.0, 0.0])


def run(p_rule=(0.3,) * 5, yn_gain=(1.52, 2.26), ch_gain=(0.41, 0.63), rho_med=0.9, gw=(0.15, 0.15, 0.25, 0.30, 0.15),
        f_shrink=None, seed=0, g2=(4.0, 3.8)):
    rng = np.random.default_rng(seed)
    a, b = np.array(YN_CLASS), np.array(YN_RULE)
    use = rng.random((N, 5)) < np.array(p_rule)
    rule = b[rng.integers(0, 3, (N, 5))]
    if f_shrink:
        rule = rule * np.where(rng.random((N, 5)) < TRACK_F, rng.uniform(*f_shrink, (N, 5)), 1.0)
    yn_t = np.where(use, rule, a[rng.integers(0, 5, (N, 5))]) + rng.normal(0, 3.0, (N, 5))
    ct, cr = np.array(CH_TOPIC), np.array(CH_REASON)
    usec = rng.random((N, 8)) < 0.10
    ch_t = np.where(usec, cr[rng.integers(0, 7, (N, 8))], ct[rng.integers(0, 15, (N, 8))]) + rng.normal(0, 2.5, (N, 8))
    sh = rng.normal(0, 1.0, N)
    Byn, Bch = yn_t.mean(1) + sh, ch_t.mean(1) + sh
    rho = lambda: np.exp(rng.normal(np.log(rho_med), 0.6, N))
    rE = rho(); ynE = Byn + rE * rng.uniform(*yn_gain, N); chE = Bch + rE * rng.uniform(*ch_gain, N)
    G = np.array([-0.5, 0, 0.5, 1.5, 2.5]); g = G[rng.choice(5, N, p=np.array(gw) / sum(gw))] + rng.normal(0, 0.3, N)
    ship = (g + rng.normal(0, 0.6, N) >= 0.35) & (rng.random(N) < np.where(g >= 0, 0.9, 0.8))
    rN = rho(); ny, nc = np.where(ship, rN * 1.2 * g, 0), np.where(ship, rN * 0.75 * g, 0)
    yn4, ch4 = ynE + ny, chE + nc; mi4 = W_YN * yn4 + W_CH * ch4
    z = rng.normal(0, 1, N); k = rng.uniform(0.3, 0.8, N)
    yn2 = ynE + k * ny - (g2[0] + 1.5 * (0.8 * z + 0.6 * rng.normal(0, 1, N))) + rng.uniform(0, 0.5, N)
    ch2 = chE + k * nc - (g2[1] + 1.3 * (0.8 * z + 0.6 * rng.normal(0, 1, N)))
    mi2 = W_YN * yn2 + W_CH * ch2
    dl = rng.uniform(0, 0.8, N); miC = W_YN * (yn4 - 1.2 * dl) + W_CH * (ch4 - 0.85 * dl)
    miE = W_YN * ynE + W_CH * chE
    return dict(mi4=mi4, yn4=yn4, ch4=ch4, mi2=mi2, miC=miC, miE=miE, ynE=ynE)


def line(name, r):
    m = r["mi4"]; q = np.percentile(m, [10, 50, 90])
    print(f"{name:44s} 4B-E med {np.median(r['miE']):+5.2f} | final 4B med {q[1]:+5.2f} [{q[0]:+5.1f},{q[2]:+5.1f}] P>=0 {np.mean(m>=0):.2f}"
          f" match {np.mean(m-1.6>-2):.2f} yn>=0 {np.mean(r['yn4']>=0):.2f} ch>=0 {np.mean(r['ch4']>=0):.2f}"
          f" | 2B P>=0 {np.mean(r['mi2']>=0):.2f} | casc P>=0 {np.mean(r['miC']>=0):.2f} match {np.mean(r['miC']-1.6>-2):.2f}")


C1 = dict(p_rule=(0.10, 0.50, 0.30, 0.10, 0.10))
C1b = dict(p_rule=(0.10, 0.50, 0.30, 0.10, 0.25))   # CNC made more rule-like (causal judgement, classic corpus)
C2 = dict(yn_gain=(1.72, 2.68), ch_gain=(0.50, 0.85))
C3 = dict(rho_med=1.2)
C4 = dict(gw=(0.10, 0.10, 0.25, 0.35, 0.20))
C5 = dict(f_shrink=(0.5, 1.0))
if __name__ == "__main__":
  print("variant (one change at a time, then combined)   [median gap ours - Jev in pp; P over 400K draws, seed 0]")
  line("base = projection/model/project.py inputs", run())
  for nm, kw in (("C1 per-task P(rule-like)", C1), ("C2 4B-E gain from unseen-source set", C2), ("C3 rho median 1.2", C3),
                 ("C4 new-4B P(g<=0) 0.20 (arguable)", C4), ("C5 track-F rule shrink (speculative)", C5)):
      line(nm, run(**kw))
  line("C1b (CNC 0.25) instead of C1", run(**C1b))
  line("C1+C2+C3 (defensible)", run(**C1, **C2, **C3))
  line("C1b+C2+C3 (defensible, CNC 0.25)", run(**C1b, **C2, **C3))
  line("C1+C2+C3+C4", run(**C1, **C2, **C3, **C4))
  line("defensible + 2B gap to teacher 3.3/3.3", run(**C1, **C2, **C3, g2=(3.3, 3.3)))
  line("C1..C5 (optimist ceiling)", run(**C1, **C2, **C3, **C4, **C5))
