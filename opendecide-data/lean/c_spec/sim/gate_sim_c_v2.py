"""Monte Carlo for the C gate in C_TRAIN_RECIPE.md (sections 6 and 10). CPU only, no data read.

Every number here is an ASSUMPTION written in the recipe. The output is a rough guide, not a measurement.
Run: python3 gate_sim_c.py
"""
import numpy as np

N = 400_000


def run(seed=0, se_half=0.9, mu_g2=1.0, sd_g2=1.56, dev_mu=0.3, dev_sd=0.6, g0_ohs=-2.2, rho=0.6, rho_gd=0.0):
    rng = np.random.default_rng(seed)
    # true sealed part-A gains (pp, candidate minus REF)
    g2 = rng.normal(mu_g2, sd_g2, N)                       # round-2 K1
    g1 = 0.7 * g2 + rng.normal(0, 0.5, N)                  # round-1 K1 (half the new data)
    c1 = np.stack([g1, 0.9 * g1 + rng.normal(0, 0.4, N)], 1)   # round 1: K1, K4 (75% snapshot)
    c2 = np.stack([g2, 0.9 * g2 + rng.normal(0, 0.4, N)], 1)   # round 2: K1', K4'

    def obs(t, se):  # one half-read of several candidates: shared + own noise
        return t + rng.normal(0, se * np.sqrt(rho), (N, 1)) + rng.normal(0, se * np.sqrt(1 - rho), t.shape)

    def dev_ok(d):  # PREREG_FINAL 3.3 (a), (a2), (b), (c), (d), (e), (f), (g) + D2 non-inferiority (LB > -1.25)
        a = d + rng.normal(0, 0.42, N) - 1.96 * 0.42 > -1.0
        a2 = (d + rng.normal(0, 0.6, N) >= -0.75) & (d + rng.normal(0, 0.6, N) >= -0.75)
        b = d + rng.normal(0, 0.4, N) + rng.normal(0, 0.55, N) >= -1.0
        c = d + rng.normal(0, 0.4, N) + rng.normal(0, 0.65, N) >= -1.0
        d2 = 0.7 * d + rng.normal(0, 0.6, N)
        D2 = d2 + rng.normal(0, 0.58, N) - 1.96 * 0.58 > -1.25
        brier = rng.normal(0, 0.003, N) + rng.normal(0, 0.0015, N) <= 0.005
        ef = (rng.normal(-0.3, 1.0, N) + rng.normal(0, 1.0, N) <= 2.0) & (rng.normal(0, 0.5, N) + rng.normal(0, 0.3, N) <= 2.0)
        g = rng.random(N) < 0.97
        return a & a2 & b & c & D2 & brier & ef & g

    # true dev effect; rho_gd > 0 links it to the true sealed gain (a model that transfers better rarely hurts dev)
    zg = (g1 - g1.mean()) / g1.std()
    d_r1 = dev_mu + dev_sd * (rho_gd * zg + np.sqrt(1 - rho_gd ** 2) * rng.standard_normal(N))
    d_r2 = 0.7 * d_r1 + rng.normal(dev_mu * 0.3, dev_sd * 0.7, N)

    s1 = obs(c1, se_half)                                   # round-1 select-half reads
    k1_sel = s1[:, 0]
    r1 = (k1_sel >= 2.0) & (k1_sel - 1.96 * se_half > 0)    # owner rule, one pre-registered candidate (K1)
    go2 = r1 & dev_ok(d_r1)                                 # + no harm to dev / security / calibration / option order

    s2 = obs(c2, se_half)
    t_all = np.where(go2[:, None], np.concatenate([c1, c2], 1), np.concatenate([c1, c1], 1))
    s_all = np.where(go2[:, None], np.concatenate([s1, s2], 1), np.concatenate([s1, s1], 1))
    fi = s_all.argmax(1)
    tf = t_all[np.arange(N), fi]
    d_f = np.where(go2 & (fi >= 2), d_r2, d_r1)

    conf = tf + rng.normal(0, se_half, N)                   # one confirm look
    P1 = (conf >= 0.5) & (conf - 1.96 * se_half > -1.0)
    dom = tf[:, None] + rng.normal(0, 1.5, (N, 8))          # 8 real-text domains, heterogeneity sd 1.5
    P2 = ~((dom + rng.normal(0, 1.9, (N, 8)) + 1.96 * 1.9) < -2.0).any(1)   # veto: a domain's UB < -2
    pb = rng.normal(2.5, 2.0, N)                            # part B true gain (commits + long docs)
    P3 = ~((pb + rng.normal(0, 1.7, N) + 1.96 * 1.7) < 0)   # veto: part B UB < 0
    ship = P1 & P2 & P3 & dev_ok(d_f)

    # vs Jev after C (shipped model, else REF)
    h = 0.6 * tf + rng.normal(0, 0.8, N)                    # true OHS-like gain of the finalist
    ohs_obs = g0_ohs + np.where(ship, h, 0.0) + rng.normal(0, 1.0, N)
    e = rng.normal(1.0, 2.0, N)                             # ejs-5 (in-domain now) true gain of the finalist
    ejs_obs = np.where(ship, -4.4 + e + rng.normal(0, 1.75, N), -4.4)
    shipped_gain = np.where(ship, tf, 0.0)
    return {
        "P(round 2 runs)": go2.mean(),
        "P(ship)": ship.mean(),
        "P(ship | true gain > +1)": ship[tf > 1].mean(),
        "P(ship | true gain <= 0)": ship[tf <= 0].mean(),
        "P(ship | true gain <= -1)": ship[tf <= -1].mean() if (tf <= -1).any() else float("nan"),
        "E[true gain | ship]": tf[ship].mean(),
        "E[shipped gain] (0 if not shipped)": shipped_gain.mean(),
        "P(true finalist gain > 0)": (tf > 0).mean(),
        "OHS-like: P(obs >= Jev - 1)": (ohs_obs >= -1).mean(),
        "OHS-like: P(obs >= Jev)": (ohs_obs >= 0).mean(),
        "OHS-like: P(obs >= Jev + 1)": (ohs_obs >= 1).mean(),
        "OHS-like: median obs gap": float(np.median(ohs_obs)),
        "ejs-5: P(obs >= Jev)": (ejs_obs >= 0).mean(),
        "ejs-5: P(obs within 2 of Jev)": (ejs_obs >= -2).mean(),
    }


if __name__ == "__main__":
    for label, kw in [("base", {}),
                      ("se_half 0.8 (4,000 items)", {"se_half": 0.8}),
                      ("se_half 1.1 (smaller suite)", {"se_half": 1.1}),
                      ("pessimistic gain (mu 0.3)", {"mu_g2": 0.3}),
                      ("optimistic gain (mu 1.8)", {"mu_g2": 1.8}),
                      ("dev neutral (mu 0.0)", {"dev_mu": 0.0}),
                      ("OHS start -1.0", {"g0_ohs": -1.0}),
                      ("dev effect linked to sealed gain (rho 0.4)", {"rho_gd": 0.4})]:
        r = run(**kw)
        print(label)
        for k, v in r.items():
            print(f"   {k:38s} {v:6.3f}")
