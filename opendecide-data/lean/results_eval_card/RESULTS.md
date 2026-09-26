# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **1915** in **295** groups. Brackets = 95% bootstrap CI over groups.

| Metric | jev_guard | q35_4b_v10_plain_cal | q35_4b_v10_plain_cal_bc | q35_4b_v10_lbd_cal_bc |
|---|---|---|---|---|
| Choice accuracy, in-domain (%) | 88.0 [83.2–92.2] | 93.5 [90.1–96.4] | 93.5 [90.1–96.4] | 93.0 [89.4–96.2] |
| Choice accuracy, zero-shot (%) | 91.6 [85.7–96.4] | 90.5 [84.3–95.8] | 91.6 [85.8–96.8] | 92.6 [87.4–97.2] |
| Yes/no accuracy, base question, ID (%) | 88.5 [84.2–92.5] | 92.0 [88.5–95.5] | 92.0 [88.5–95.5] | 92.0 [88.5–95.5] |
| Yes/no accuracy, base question, ZS (%) | 85.3 [78.2–91.8] | 86.3 [79.1–92.6] | 86.3 [79.1–92.6] | 89.5 [83.3–95.2] |
| Yes/no accuracy, negated question, ID (%) | 86.5 [81.8–90.8] | 91.5 [87.6–95.0] | 91.5 [87.6–95.0] | 91.5 [87.6–95.0] |
| Yes/no accuracy, negated question, ZS (%) | 85.3 [78.3–91.8] | 90.5 [84.8–95.8] | 90.5 [84.8–95.8] | 89.5 [82.7–95.3] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.085 [0.077–0.094] | 0.055 [0.046–0.066] | 0.055 [0.046–0.066] | 0.046 [0.037–0.056] |
| Contradiction rate ↓ (%) | 4.4 | 4.4 | 4.4 | 3.1 |
| Pairs summing to 1±0.05 ↑ (%) | 39.3 | 75.9 | 75.9 | 78.6 |
| Paraphrase drift |ΔP| ↓ | 0.020 [0.017–0.024] | 0.024 [0.019–0.030] | 0.024 [0.019–0.030] | 0.022 [0.018–0.027] |
| Paraphrase flip rate ↓ (%) | 2.0 | 2.4 | 2.4 | 0.7 |
| Double-negation drift ↓ | 0.206 [0.192–0.219] | 0.048 [0.038–0.059] | 0.048 [0.038–0.059] | 0.044 [0.034–0.055] |
| Brier (yes/no, core) ↓ | 0.106 [0.089–0.123] | 0.073 [0.055–0.093] | 0.073 [0.055–0.093] | 0.072 [0.053–0.092] |
| ECE (yes/no, core) ↓ | 0.047 | 0.042 | 0.042 | 0.032 |
| Coverage @1% error, cross-fitted ↑ (%) | 2.1 | 3.2 | 3.2 | 2.8 |
| Injection attack success, held-out C+D ↓ (%) | 10.0 [3.2–17.7] | 0.8 [0.0–2.7] | 0.8 [0.0–2.7] | 3.3 [0.0–7.8] |
| Choice acc under injection C (%) | 86.7 | 90.0 | 90.0 | 85.0 |
| Choice acc under injection D (%) | 83.3 | 88.3 | 88.3 | 88.3 |
| Choice acc, same items clean (%) | 90.0 | 93.3 | 93.3 | 91.7 |
| Echo control choice acc (%) | 98.3 | 98.3 | 98.3 | 96.7 |
| Distractor choice acc (%) | 72.5 | 87.5 | 87.5 | 85.0 |
| Distractor, same items clean (%) | 80.0 | 87.5 | 87.5 | 87.5 |
| Neg. acc ID, wording 0 'someone who says … mistaken' (near train wordings) (%) | 81.0 | 88.0 | 88.0 | 88.0 |
| Neg. acc ID, wording 1 'reader who concluded … misreading' (truly unseen) (%) | 92.0 | 95.0 | 95.0 | 95.0 |
| Coverage @2% error, cross-fitted ↑ (%) | 11.0 | 26.9 | 26.9 | 30.2 |
| Coverage @3% error, cross-fitted ↑ (%) | 39.6 | 53.9 | 53.9 | 55.9 |
| Coverage @5% error, cross-fitted ↑ (%) | 61.2 | 83.6 | 83.6 | 82.9 |

**Paired differences vs jev_guard** (model − jev_guard, 95% bootstrap CI over the same groups; * = CI excludes 0)

| Metric | q35_4b_v10_plain_cal | q35_4b_v10_plain_cal_bc | q35_4b_v10_lbd_cal_bc |
|---|---|---|---|
| choice_acc_ID | +5.5 [+2.5, +8.8]* | +5.5 [+2.5, +8.8]* | +5.0 [+2.0, +8.3]* |
| noul_base_acc_ID | +3.5 [-0.5, +7.4] | +3.5 [-0.5, +7.4] | +3.5 [-0.5, +7.4] |
| noul_neg_acc_ID | +5.0 [+1.0, +9.2]* | +5.0 [+1.0, +9.2]* | +5.0 [+1.0, +9.2]* |
| choice_acc_ZS | -1.1 [-6.7, +4.0] | +0.0 [-6.2, +5.9] | +1.1 [-4.2, +6.7] |
| noul_base_acc_ZS | +1.1 [-7.4, +9.8] | +1.1 [-7.4, +9.8] | +4.2 [-3.2, +11.9] |
| noul_neg_acc_ZS | +5.3 [-1.3, +12.3] | +5.3 [-1.3, +12.3] | +4.2 [-3.8, +12.0] |
| brier_noul_core | -0.033 [-0.048, -0.018]* | -0.033 [-0.048, -0.018]* | -0.034 [-0.049, -0.019]* |
| complement_violation | -0.030 [-0.040, -0.018]* | -0.030 [-0.040, -0.018]* | -0.039 [-0.050, -0.027]* |
| double_negation_drift | -0.158 [-0.175, -0.139]* | -0.158 [-0.175, -0.139]* | -0.161 [-0.178, -0.144]* |
| inj_ASR_pooled | -9.2 [-16.7, -2.8]* | -9.2 [-16.7, -2.8]* | -6.7 [-13.2, -1.6]* |
| dist_choice_acc | +15.0 [+2.5, +29.7]* | +15.0 [+2.5, +29.7]* | +12.5 [-2.6, +27.3] |

**Latency**

- jev_guard: {"api_per_call_median_ms": 194.3671249318868, "api_per_call_p95_ms": 305.24051225511346}
- q35_4b_v10_plain_cal: {}
- q35_4b_v10_plain_cal_bc: {}
- q35_4b_v10_lbd_cal_bc: {}
