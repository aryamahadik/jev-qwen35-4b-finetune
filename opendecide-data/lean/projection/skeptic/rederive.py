"""Pessimist re-derivations (read-only; numbers copied from the cited files)."""
import numpy as np
hm = lambda *x: len(x) / sum(1 / v for v in x)
print("== pools (projection/recompute/ohs1_out.txt, ohs2_out.txt; v11c ours-Jev, rows)")
YC = {"argq": (-0.83, 120), "cuad": (-0.62, 80), "hatecheck": (-3.10, 145), "overruling": (5.00, 40), "tinad": (3.06, 180)}
YR = {"moral": (-12.50, 120), "tabfact": (-8.33, 120), "hearsay": (-29.27, 82)}
CT = {"qbio": (-5.83, 60), "physics": (-1.67, 60), "econqfin": (-1.67, 60), "condmat": (7.50, 60), "math": (-3.33, 60), "astro": (-3.33, 60),
      "stat_eess": (1.67, 60), "cs": (6.67, 60), "big_patent": (-1.67, 120), "medabs": (3.33, 120), "ledgar": (1.67, 60),
      "unfair_tos": (1.88, 80), "go_emotions": (-4.33, 150), "sgd": (-1.50, 200), "ddi2013": (12.50, 120)}
def m(d, drop=(), w=False):
    v = [(a, n) for k, (a, n) in d.items() if k not in drop]
    return np.average([a for a, n in v], weights=[n if w else 1 for a, n in v])
print(f"yes/no class pool: unweighted {m(YC):+.2f} | row-weighted {m(YC, w=True):+.2f} | row-weighted w/o TINAD {m(YC, ('tinad',), True):+.2f} | unweighted w/o TINAD {m(YC, ('tinad',)):+.2f}")
print(f"yes/no rule pool: unweighted {m(YR):+.2f} | row-weighted {m(YR, w=True):+.2f}; base rate of rule-like yes/no tasks in past exams = 3/8 = {3/8:.3f}")
v = sorted(a for a, n in CT.values())
print(f"choice topical pool: mean {m(CT):+.2f} | row-weighted {m(CT, w=True):+.2f} | median {np.median(v):+.2f} | 2-trimmed {np.mean(v[2:-2]):+.2f} | w/o ddi2013 {m(CT, ('ddi2013',)):+.2f} / row-wtd {m(CT, ('ddi2013',), True):+.2f} | negative in {sum(a < 0 for a in v)}/{len(v)}")
for p_rule in (0.30, 0.375, 0.40, 0.50):
    yn = (1 - p_rule) * m(YC, ('tinad',), True) + p_rule * m(YR, w=True)
    print(f"  v11c-class yes/no baseline (row-wtd, no TINAD) at P_rule {p_rule:.3f}: {yn:+.2f}  (projection at 0.30 unweighted: {0.7*m(YC)+0.3*m(YR):+.2f})")
print("== selection signature (dev_out.txt): confirm - select per 4B")
cs = {"v10": (78.20, 77.65), "v11": (78.35, 77.47), "v11b": (79.19, 78.28), "v11c": (79.49, 78.84), "v12t": (78.79, 78.40),
      "v13t": (80.13, 79.57), "blend50": (80.05, 79.40), "pxI": (80.90, 80.42), "pxE": (81.49, 79.84)}
sib = [c - s for k, (c, s) in cs.items() if k != "pxE"]
print("  siblings:", {k: round(c - s, 2) for k, (c, s) in cs.items()}, f"sibling mean {np.mean(sib):+.2f}; pxE excess {1.65 - np.mean(sib):+.2f}")
print("== transfer ratios (evidence.md s12): clean ones = OHS-2 v10->v11c 1.35, OHS-1 frozen->v10 ~0.03; geometric mean of the clean two",
      f"{np.exp(np.mean(np.log([1.35, 0.03]))):.2f}; of all five {np.exp(np.mean(np.log([1.5, 1.35, 2.2, 0.26, 0.03]))):.2f}; median of all five 1.35")
print(f"  lognormal(0.9, 0.6): P(rho<0.3) = {np.mean(np.exp(np.random.default_rng(0).normal(np.log(0.9), 0.6, 10**6)) < 0.3):.3f}")
print("== 2B held-out amplification: kd pilot dev(4 splits) -7.85 -> OHS-1 -9.75 = x%.2f; v11r dev -3.23 -> JevBench-A -5.1 = x%.2f" % (9.75 / 7.85, 5.1 / 3.23))
print("== Brier: fitted line diff = +0.0136 - 0.0043*gap -> 'matches' (point < -0.003) needs yes/no gap > %.2f pp; projection's line needs > %.2f" % ((0.0136 + 0.003) / 0.0043, (0.007 + 0.003) / 0.0053))
print("== JevBench v1.5.4 public (RESULTS_30sep.md): Score A = harmonic(I, C, S, $)")
print(f"  4B committed 78.7/83.4/88.6/58.3 -> {hm(78.7, 83.4, 88.6, 58.3):.2f}; same with I = Jev-committed 73.6 -> {hm(73.6, 83.4, 88.6, 58.3):.2f}; Jev committed 70.66, as returned 68.80")
print(f"  4B raw (T=1) 62.5/84.3/88.6/58.3 -> {hm(62.5, 84.3, 88.6, 58.3):.2f}; decisive-readout effect on I = {78.7 - 62.5:+.1f} (policy); fair I diff (both committed) +5.1 [-4.4, +15.0]")
print(f"  Score A lead over committed Jev from non-I axes alone: {hm(73.6, 83.4, 88.6, 58.3) - 70.66:+.2f} of {75.27 - 70.66:+.2f}")
for I in (50, 55, 57, 58, 60, 65, 70):
    print(f"  board-like (C 88.3, S 93.6, $ 63.1 = JevK5 axes): I {I} -> A {hm(I, 88.3, 93.6, 63.1):.2f} vs Jev 72.13 | with C 83.4 -> {hm(I, 83.4, 93.6, 63.1):.2f}")
print("== speed axis: points = 100 - 20 log10(s/0.1); self-hosted s = 2t + 0.15")
pt = lambda s: 100 - 20 * np.log10(s / 0.1)
for t in (0.024, 0.035, 0.050, 0.059, 0.070, 0.110, 0.128):
    print(f"  t = {t*1000:.0f} ms -> {pt(2 * t + 0.15):.1f} (Jev 91.4)")
print(f"  2B-I H100 eager EST: 128 ms (L4 eager) / 2.17 (earlier 4B eager L4 59.8 / H100 27.5) = {128 / (59.8 / 27.5):.0f} ms")
print("== real serving cost at 100% utilisation ($/1K decisions) = rate/3600 * t * 1000")
for lab, rate, t in (("H100 GPU-only 24 ms", 3.95, 0.024), ("H100 server 44.8 ms (v10 tunnel, measured)", 3.95, 0.0448),
                     ("H100 server ~56 ms (layout E EST)", 3.95, 0.056), ("L4 110 ms", 0.80, 0.110), ("2B H100 eager 59 ms", 3.95, 0.059)):
    c = rate / 3600 * t * 1000
    print(f"  {lab:45s} ${c:.3f} (at 50% use ${2*c:.3f}; at 30% ${c/0.3:.3f}); Jev $0.032 per 1K calls billed, $0.0384 list")
