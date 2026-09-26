# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **1915** in **295** groups. Brackets = 95% bootstrap CI over groups.

| Metric | jev | q35_4b_v10_tunnel_plain |
|---|---|---|
| Choice accuracy, in-domain (%) | 89.5 [85.0–93.3] | 93.5 [90.1–96.4] |
| Choice accuracy, zero-shot (%) | 92.6 [87.0–97.4] | 90.5 [84.0–95.6] |
| Yes/no accuracy, base question, ID (%) | 89.0 [84.8–93.0] | 92.0 [88.5–95.5] |
| Yes/no accuracy, base question, ZS (%) | 88.4 [82.0–94.1] | 90.5 [84.7–95.8] |
| Yes/no accuracy, negated question, ID (%) | 87.5 [82.7–91.4] | 91.5 [87.6–95.0] |
| Yes/no accuracy, negated question, ZS (%) | 84.2 [77.1–91.1] | 90.5 [84.5–95.7] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.073 [0.065–0.081] | 0.064 [0.054–0.075] |
| Contradiction rate ↓ (%) | 5.8 | 5.1 |
| Pairs summing to 1±0.05 ↑ (%) | 44.1 | 70.5 |
| Paraphrase drift |ΔP| ↓ | 0.027 [0.022–0.031] | 0.027 [0.021–0.034] |
| Paraphrase flip rate ↓ (%) | 2.4 | 2.0 |
| Double-negation drift ↓ | 0.168 [0.152–0.182] | 0.047 [0.037–0.058] |
| Brier (yes/no, core) ↓ | 0.098 [0.082–0.116] | 0.071 [0.053–0.090] |
| ECE (yes/no, core) ↓ | 0.036 | 0.039 |
| Coverage @1% error, cross-fitted ↑ (%) | 0.0 | 3.1 |
| Injection attack success, held-out C+D ↓ (%) | 19.2 [10.5–29.0] | 0.8 [0.0–2.7] |
| Choice acc under injection C (%) | 81.7 | 90.0 |
| Choice acc under injection D (%) | 73.3 | 88.3 |
| Choice acc, same items clean (%) | 90.0 | 93.3 |
| Echo control choice acc (%) | 98.3 | 98.3 |
| Distractor choice acc (%) | 72.5 | 87.5 |
| Distractor, same items clean (%) | 85.0 | 87.5 |
| Neg. acc ID, wording 0 'someone who says … mistaken' (near train wordings) (%) | 81.0 | 88.0 |
| Neg. acc ID, wording 1 'reader who concluded … misreading' (truly unseen) (%) | 94.0 | 95.0 |
| Coverage @2% error, cross-fitted ↑ (%) | 21.8 | 14.4 |
| Coverage @3% error, cross-fitted ↑ (%) | 39.8 | 57.1 |
| Coverage @5% error, cross-fitted ↑ (%) | 66.6 | 80.9 |

**Paired differences vs jev** (model − jev, 95% bootstrap CI over the same groups; * = CI excludes 0)

| Metric | q35_4b_v10_tunnel_plain |
|---|---|
| choice_acc_ID | +4.0 [+1.5, +6.9]* |
| noul_base_acc_ID | +3.0 [-1.0, +6.9] |
| noul_neg_acc_ID | +4.0 [+0.0, +8.2] |
| choice_acc_ZS | -2.1 [-8.0, +3.4] |
| noul_base_acc_ZS | +2.1 [-3.5, +8.0] |
| noul_neg_acc_ZS | +6.3 [+0.0, +13.0] |
| brier_noul_core | -0.027 [-0.041, -0.013]* |
| complement_violation | -0.009 [-0.021, +0.004] |
| double_negation_drift | -0.120 [-0.137, -0.101]* |
| inj_ASR_pooled | -18.3 [-27.9, -10.2]* |
| dist_choice_acc | +15.0 [+2.6, +29.4]* |

**Latency**

- jev: {"api_per_call_median_ms": 203.43395799864084, "api_per_call_p95_ms": 311.98124998481916}
- q35_4b_v10_tunnel_plain: {"api_per_call_median_ms": 114.57312502898276, "api_per_call_p95_ms": 122.71466256352133}
