"""Sensitivity of the accuracy projection (same chain as project.py sections 1-5, one assumption changed at a time).
Prints P(final 4B micro >= 0), P(PREREG 'matches'), P(final 4B yes/no >= 0), P(final 2B micro >= 0)."""
import numpy as np
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("pm", Path(__file__).with_name("project.py"))
src = Path(__file__).with_name("project.py").read_text().split("# ---------------- 6.")[0]
ns = {}
exec(compile(src.replace("N = 400_000", "N = 200_000"), "project_head", "exec"), ns)   # pools and constants only
YN_CLASS, YN_RULE, CH_TOPIC, CH_REASON = ns["YN_CLASS"], ns["YN_RULE"], ns["CH_TOPIC"], ns["CH_REASON"]
W_YN, W_CH = ns["W_YN"], ns["W_CH"]
N = 200_000


def run(p_rule=0.30, p_reason=0.10, jit=(3.0, 2.5), shift_sd=1.0, rho_med=0.9, rho_sd=0.6,
        gw=(0.15, 0.15, 0.25, 0.30, 0.15), g2=(4.0, 3.8), pools=None, seed=0):
    rng = np.random.default_rng(seed)
    yc, yr, ct, cr = pools or (YN_CLASS, YN_RULE, CH_TOPIC, CH_REASON)

    def draw(a, b, p, k, j):
        a, b = np.array(list(a.values())), np.array(list(b.values()))
        use = rng.random((N, k)) < p
        return (np.where(use, b[rng.integers(0, len(b), (N, k))], a[rng.integers(0, len(a), (N, k))]) + rng.normal(0, j, (N, k))).mean(1)
    sh = rng.normal(0, shift_sd, N)
    Byn, Bch = draw(yc, yr, p_rule, 5, jit[0]) + sh, draw(ct, cr, p_reason, 8, jit[1]) + sh
    rho = lambda: np.exp(rng.normal(np.log(rho_med), rho_sd, N))
    rE = rho(); yn = Byn + rE * rng.uniform(1.52, 2.26, N); ch = Bch + rE * rng.uniform(0.41, 0.63, N)
    ynE, chE = yn.copy(), ch.copy()
    G = np.array([-0.5, 0, 0.5, 1.5, 2.5]); g = G[rng.choice(5, N, p=np.array(gw) / sum(gw))] + rng.normal(0, 0.3, N)
    ship = (g + rng.normal(0, 0.6, N) >= 0.35) & (rng.random(N) < np.where(g >= 0, 0.9, 0.8))
    rN = rho(); ny, nc = np.where(ship, rN * 1.2 * g, 0), np.where(ship, rN * 0.75 * g, 0)
    yn, ch = yn + ny, ch + nc
    mi = W_YN * yn + W_CH * ch
    z = rng.normal(0, 1, N)
    k = rng.uniform(0.3, 0.8, N)
    yn2 = ynE + k * ny - (g2[0] + 1.5 * (0.8 * z + 0.6 * rng.normal(0, 1, N))) + rng.uniform(0, 0.5, N)
    ch2 = chE + k * nc - (g2[1] + 1.3 * (0.8 * z + 0.6 * rng.normal(0, 1, N)))
    mi2 = W_YN * yn2 + W_CH * ch2
    return np.median(mi), np.mean(mi >= 0), np.mean(mi - 1.6 > -2.0), np.mean(yn >= 0), np.mean(mi2 >= 0)


o2 = lambda d: {k: v for k, v in d.items() if k.startswith("ohs2")}
variants = [
    ("base (projection.md)", {}),
    ("P(rule-like yes/no task) 0.10", dict(p_rule=0.10)),
    ("P(rule-like yes/no task) 0.50", dict(p_rule=0.50)),
    ("no hearsay in rule pool", dict(pools=(YN_CLASS, {k: v for k, v in YN_RULE.items() if "hearsay" not in k}, CH_TOPIC, CH_REASON))),
    ("OHS-2 tasks only (freshest exam)", dict(pools=(o2(YN_CLASS), o2(YN_RULE), o2(CH_TOPIC), o2(CH_REASON)))),
    ("transfer ratio median 0.5", dict(rho_med=0.5)),
    ("transfer ratio median 1.4", dict(rho_med=1.4)),
    ("pessimistic new 4B (P(g<=0)=0.55)", dict(gw=(0.30, 0.25, 0.20, 0.20, 0.05))),
    ("optimistic new 4B (P(g>=1.5)=0.65)", dict(gw=(0.05, 0.10, 0.20, 0.40, 0.25))),
    ("wider task spread (jitter x2, shift 2)", dict(jit=(6.0, 5.0), shift_sd=2.0)),
    ("2B gap to teacher 3.0 / 2.8 (well distilled)", dict(g2=(3.0, 2.8))),
    ("2B gap to teacher 5.5 / 5.0 (like I_1600)", dict(g2=(5.5, 5.0))),
]
print(f"{'variant':46s} 4B micro med  P(4B>=0)  P(4B matches)  P(4B yes/no>=0)  P(2B>=0)")
for name, kw in variants:
    m, p0, pm, py, p2 = run(**kw)
    print(f"{name:46s} {m:+11.2f}  {p0:8.2f}  {pm:13.2f}  {py:15.2f}  {p2:8.2f}")
