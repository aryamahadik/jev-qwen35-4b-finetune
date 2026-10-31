"""Optimist joint probabilities for the final 4B (read-only). Accuracy draws from o7 (defensible C1+C2+C3), Brier from
the projection's own Brier model, then the non-accuracy parts with the corrections argued in optimist notes:
  injection counted with the same tie rule as accuracy (not significantly worse than Jev): 0.90 (projection: 0.70 point rule);
  speed 0.85 (P(win | no proper hosting) 0.30 instead of 0.05: L4-eager 110 ms + 72 ms tunnel ~ 185 ms vs Jev 187-248 ms);
  option-order drift P(ours <= Jev) 0.30 instead of 0.60 (PESSIMISTIC correction: measured 4B-E drift, o6_out.txt);
  Brier intercept at equal accuracy: projection N(0.007, 0.007) and the measured +0.011 (o1_out.txt) both shown.
"""
import numpy as np, importlib.util, pathlib
spec = importlib.util.spec_from_file_location("o7", pathlib.Path(__file__).with_name("o7_optimist_mc.py"))
o7 = importlib.util.module_from_spec(spec); spec.loader.exec_module(o7)
N = o7.N
rng = np.random.default_rng(1)
for label, kw in (("projection base", {}), ("defensible C1+C2+C3", {**o7.C1, **o7.C2, **o7.C3})):
    r = o7.run(**kw)
    yn, mi, ch = r["yn4"], r["mi4"], r["ch4"]
    for a_mean in (0.007, 0.011):
        br = rng.normal(a_mean, 0.007, N) + rng.normal(-0.0053, 0.001, N) * yn + rng.normal(0, 0.0059, N) - rng.uniform(0, 0.001, N)
        print(f"{label:22s} Brier intercept {a_mean}: diff median {np.median(br):+.4f}  P(PREREG matches) {np.mean(br + 0.013 < 0.010):.2f}")
    common = np.exp(rng.normal(0, 0.3, N))
    v_jev = 10.8 * common * np.exp(rng.normal(0, 0.35, N))
    v_our = 4.81 * rng.uniform(1.25, 1.9, N) * common * np.exp(rng.normal(0, 0.35, N)) * np.exp(-0.04 * (yn - np.median(yn)))
    comp = (v_our - v_jev + rng.normal(0, 2.2, N)) <= 0
    for p_drift, inj, spd in ((0.60, 0.70, 0.82), (0.60, 0.90, 0.85), (0.30, 0.90, 0.85)):
        drift = rng.random(N) < p_drift
        hij, injb, spdb, cost, jb = (rng.random(N) < p for p in (0.97, inj, spd, 0.97, 0.93))
        match = mi - 1.6 > -2.0
        owner = np.mean(match & hij & injb & spdb & cost & jb)
        allw = np.mean(match & (yn >= 0) & (ch >= 0) & comp & drift & hij & injb & spdb & cost & jb)
        print(f"   drift P {p_drift:.2f}, injection {inj:.2f}, speed {spd:.2f}: owner-success {owner:.2f}; all win conditions {allw:.3f};"
              f" complement P {comp.mean():.2f}")
