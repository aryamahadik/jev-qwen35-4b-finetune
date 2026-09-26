# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **1915** in **295** groups. Brackets = 95% bootstrap CI over groups.

| Metric | jev_guard | jev | jev_guard_bc | g12_v06_A3_cal_bc |
|---|---|---|---|---|
| Choice accuracy, in-domain (%) | 88.0 [83.2–92.2] | 89.5 [85.2–93.5] | 88.0 [83.2–92.2] | 93.0 [89.3–96.1] |
| Choice accuracy, zero-shot (%) | 91.6 [85.7–96.4] | 90.5 [84.8–95.6] | 89.5 [83.3–95.2] | 91.6 [85.9–96.8] |
| Yes/no accuracy, base question, ID (%) | 88.5 [84.2–92.5] | 89.0 [84.8–93.0] | 88.5 [84.2–92.5] | 90.0 [85.6–93.7] |
| Yes/no accuracy, base question, ZS (%) | 85.3 [78.2–91.8] | 86.3 [79.6–92.6] | 85.3 [78.2–91.8] | 92.6 [87.2–97.7] |
| Yes/no accuracy, negated question, ID (%) | 86.5 [81.8–90.8] | 87.5 [83.0–91.7] | 86.5 [81.8–90.8] | 92.0 [88.1–95.3] |
| Yes/no accuracy, negated question, ZS (%) | 85.3 [78.3–91.8] | 83.2 [76.0–90.1] | 85.3 [78.3–91.8] | 90.5 [84.0–96.2] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.085 [0.077–0.094] | 0.073 [0.065–0.080] | 0.085 [0.077–0.094] | 0.058 [0.046–0.072] |
| Contradiction rate ↓ (%) | 4.4 | 6.4 | 4.4 | 4.7 |
| Pairs summing to 1±0.05 ↑ (%) | 39.3 | 46.8 | 39.3 | 76.9 |
| Paraphrase drift |ΔP| ↓ | 0.020 [0.017–0.024] | 0.020 [0.017–0.025] | 0.020 [0.017–0.024] | 0.023 [0.018–0.030] |
| Paraphrase flip rate ↓ (%) | 2.0 | 2.0 | 2.0 | 1.7 |
| Double-negation drift ↓ | 0.206 [0.192–0.219] | 0.168 [0.153–0.182] | 0.206 [0.192–0.219] | 0.067 [0.053–0.082] |
| Brier (yes/no, core) ↓ | 0.106 [0.089–0.123] | 0.099 [0.082–0.117] | 0.106 [0.089–0.123] | 0.075 [0.054–0.097] |
| ECE (yes/no, core) ↓ | 0.047 | 0.028 | 0.047 | 0.019 |
| Coverage @1% error, cross-fitted ↑ (%) | 2.1 | 0.0 | 2.1 | 18.3 |
| Injection attack success, held-out C+D ↓ (%) | 10.0 [3.2–17.7] | 18.3 [9.8–28.1] | 10.0 [3.2–17.7] | 4.2 [0.0–9.6] |
| Choice acc under injection C (%) | 86.7 | 81.7 | 86.7 | 90.0 |
| Choice acc under injection D (%) | 83.3 | 75.0 | 83.3 | 88.3 |
| Choice acc, same items clean (%) | 90.0 | 90.0 | 90.0 | 93.3 |
| Echo control choice acc (%) | 98.3 | 98.3 | 98.3 | 95.0 |
| Distractor choice acc (%) | 72.5 | 72.5 | 72.5 | 90.0 |
| Distractor, same items clean (%) | 80.0 | 82.5 | 80.0 | 90.0 |
| Neg. acc ID, wording 0 'someone who says … mistaken' (near train wordings) (%) | 81.0 | 81.0 | 81.0 | 88.0 |
| Neg. acc ID, wording 1 'reader who concluded … misreading' (truly unseen) (%) | 92.0 | 94.0 | 92.0 | 96.0 |
| Coverage @2% error, cross-fitted ↑ (%) | 11.0 | 33.0 | 11.0 | 48.7 |
| Coverage @3% error, cross-fitted ↑ (%) | 39.6 | 36.8 | 39.6 | 61.7 |
| Coverage @5% error, cross-fitted ↑ (%) | 61.2 | 66.2 | 61.2 | 79.8 |

**Paired differences vs jev_guard** (model − jev_guard, 95% bootstrap CI over the same groups; * = CI excludes 0)

| Metric | jev | jev_guard_bc | g12_v06_A3_cal_bc |
|---|---|---|---|
| choice_acc_ID | +1.5 [+0.0, +3.3] | +0.0 [+0.0, +0.0] | +5.0 [+2.0, +8.4]* |
| noul_base_acc_ID | +0.5 [-1.0, +2.1] | +0.0 [+0.0, +0.0] | +1.5 [-2.2, +5.0] |
| noul_neg_acc_ID | +1.0 [-1.0, +3.1] | +0.0 [+0.0, +0.0] | +5.5 [+2.0, +9.4]* |
| choice_acc_ZS | -1.1 [-3.5, +0.0] | -2.1 [-7.3, +3.1] | +0.0 [-4.0, +4.2] |
| noul_base_acc_ZS | +1.1 [+0.0, +3.4] | +0.0 [+0.0, +0.0] | +7.4 [+1.9, +13.9]* |
| noul_neg_acc_ZS | -2.1 [-5.1, +0.0] | +0.0 [+0.0, +0.0] | +5.3 [-3.1, +13.7] |
| brier_noul_core | -0.007 [-0.009, -0.004]* | +0.000 [+0.000, +0.000] | -0.031 [-0.043, -0.018]* |
| complement_violation | -0.013 [-0.018, -0.007]* | +0.000 [+0.000, +0.000] | -0.027 [-0.040, -0.013]* |
| double_negation_drift | -0.037 [-0.046, -0.030]* | +0.000 [+0.000, +0.000] | -0.139 [-0.159, -0.115]* |
| inj_ASR_pooled | +8.3 [+2.8, +15.6]* | +0.0 [+0.0, +0.0] | -5.8 [-13.9, +1.1] |
| dist_choice_acc | +0.0 [+0.0, +0.0] | +0.0 [+0.0, +0.0] | +17.5 [+6.7, +30.6]* |

**Latency**

- jev_guard: {"api_per_call_median_ms": 194.3671249318868, "api_per_call_p95_ms": 305.24051225511346}
- jev: {"api_per_call_median_ms": 187.25333304610103, "api_per_call_p95_ms": 266.3771624909714}
- jev_guard_bc: {"api_per_call_median_ms": 194.3671249318868, "api_per_call_p95_ms": 305.24051225511346}
- g12_v06_A3_cal_bc: {}
