"""Verifier (stats lens): size of the A19 rule from the existing reports + exact simulation. Counts only."""
import json
from pathlib import Path
import numpy as np

G = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_build/g8v2")
OUT = G / "verify_stats/size_sim.json"
rng = np.random.default_rng(20261005)
res = {}

# 1) exchangeable-draw pass probability for "new <= q95_linear(K draws)" and "new <= min(q95 of two K-sets)"
for K in (20, 40, 100):
    a = rng.standard_normal((200000, K)); b = rng.standard_normal((200000, K)); x = rng.standard_normal(200000)
    qa = np.percentile(a, 95, axis=1); qb = np.percentile(b, 95, axis=1)
    res[f"sim_K{K}"] = {"p_pass_one_null": round(float((x <= qa).mean()), 4),
                        "p_pass_min_two_iid_nulls": round(float((x <= np.minimum(qa, qb)).mean()), 4),
                        "sd_q95_in_null_sd_units": round(float(qa.std()), 3)}
# expected number of false FAILs across 11 clean parts at the K=20 min-rule size
p = res["sim_K20"]["p_pass_min_two_iid_nulls"]
res["p_at_least_one_false_fail_11_parts"] = round(1 - p ** 11, 3)

# 2) per family/part: real vs nulls, null sd, bootstrap sd of q95, margins in units of that sd
fam = {}
for f in ["F1", "F2", "F3", "F4", "F5", "F6"]:
    d = json.loads((G / f"{f}.json").read_text())
    for part, v in d["parts"].items():
        w = np.array(v["null_within_card"]["shares"]); g = np.array(v["null_global"]["shares"])
        bw = np.percentile(w[rng.integers(0, 20, (20000, 20))], 95, axis=1)
        bg = np.percentile(g[rng.integers(0, 20, (20000, 20))], 95, axis=1)
        thr_boot = np.minimum(bw, bg); real = v["real"]["share"]; sp = v["partition_seed_spread"]["shares"]
        aw = np.array(v["null_within_card"]["accs"]); ag = np.array(v["null_global"]["accs"])
        fam[f"{f}/{part}"] = {
            "real": real, "thr": v["threshold"], "margin_pp": round(100 * (v["threshold"] - real), 2),
            "null_w_mean": round(float(w.mean()), 4), "null_w_sd": round(float(w.std(ddof=1)), 4),
            "null_g_mean": round(float(g.mean()), 4), "null_g_sd": round(float(g.std(ddof=1)), 4),
            "z_real_vs_within": round(float((real - w.mean()) / w.std(ddof=1)), 2),
            "z_real_vs_global": round(float((real - g.mean()) / g.std(ddof=1)), 2),
            "boot_sd_threshold_pp": round(100 * float(thr_boot.std()), 2),
            "boot_p_verdict_flips": round(float(((real <= thr_boot) != v["pass_share"]).mean()), 3),
            "real_partition_seed_shares": sp,
            "n_seed_shares_over_thr": int(sum(s > v["threshold"] for s in sp)),
            "chance": v["chance"], "null_acc_w_mean": round(float(aw.mean()), 4),
            "null_acc_g_mean": round(float(ag.mean()), 4),
            "null_acc_max": round(float(max(aw.max(), ag.max())), 4), "real_acc": v["real"]["acc"],
            "acc_bar": round(v["chance"] + 0.02, 4),
            "acc_slack_vs_null_mean_pp": round(100 * (v["chance"] + 0.02 - float(np.r_[aw, ag].mean())), 2)}
res["families"] = fam

# 3) F2: 20 extra within-card draws (power shuffled, seeds 3000+) are the same law as the within null
pw = json.loads((G / "power_F2.json").read_text())
for part in ("yes_no", "choice"):
    a = np.array(json.loads((G / "F2.json").read_text())["parts"][part]["null_within_card"]["shares"])
    b = np.array([r["share"] for r in pw["shuffled"][part]["runs"]])
    res[f"F2_{part}_two_within_sets"] = {"q95_set_A": round(float(np.percentile(a, 95)), 4),
                                         "q95_set_B": round(float(np.percentile(b, 95)), 4),
                                         "q95_pooled40": round(float(np.percentile(np.r_[a, b], 95)), 4),
                                         "B_over_qA": int((b > np.percentile(a, 95)).sum()),
                                         "A_over_qB": int((a > np.percentile(b, 95)).sum())}
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != "families"}))
for k, v in fam.items():
    print(k, {x: v[x] for x in ("real", "thr", "margin_pp", "z_real_vs_within", "z_real_vs_global",
                                "boot_sd_threshold_pp", "boot_p_verdict_flips", "n_seed_shares_over_thr",
                                "chance", "null_acc_w_mean", "null_acc_g_mean", "real_acc", "acc_slack_vs_null_mean_pp")})
