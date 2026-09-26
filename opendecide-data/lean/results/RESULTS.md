# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **1915** in **295** groups. Brackets = 95% bootstrap CI over groups.

| Metric | jev_guard | jev | g12_v06_A3_cal | g12_v06_A3_cal_bc |
|---|---|---|---|---|
| Choice accuracy, in-domain (%) | 88.0 [83.2–92.2] | 89.5 [85.0–93.3] | 93.0 [89.3–96.1] | 93.0 [89.3–96.1] |
| Choice accuracy, zero-shot (%) | 92.6 [87.0–97.4] | 92.6 [87.0–97.4] | 90.5 [84.4–95.7] | 89.5 [83.1–95.1] |
| Yes/no accuracy, base question, ID (%) | 88.0 [83.7–92.2] | 89.0 [84.8–93.0] | 90.0 [85.6–93.7] | 90.0 [85.6–93.7] |
| Yes/no accuracy, base question, ZS (%) | 87.4 [80.8–93.5] | 88.4 [82.0–94.1] | 91.6 [85.7–96.6] | 91.6 [85.7–96.6] |
| Yes/no accuracy, negated question, ID (%) | 87.0 [82.4–91.3] | 87.5 [82.7–91.4] | 92.0 [88.1–95.3] | 92.0 [88.1–95.3] |
| Yes/no accuracy, negated question, ZS (%) | 85.3 [77.9–91.8] | 84.2 [77.1–91.1] | 91.6 [85.1–96.7] | 91.6 [85.1–96.7] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.075 [0.067–0.082] | 0.073 [0.065–0.081] | 0.082 [0.068–0.097] | 0.082 [0.068–0.097] |
| Contradiction rate ↓ (%) | 3.4 | 5.8 | 6.1 | 6.1 |
| Pairs summing to 1±0.05 ↑ (%) | 41.0 | 44.1 | 67.1 | 67.1 |
| Paraphrase drift |ΔP| ↓ | 0.025 [0.021–0.029] | 0.027 [0.022–0.031] | 0.054 [0.044–0.066] | 0.054 [0.044–0.066] |
| Paraphrase flip rate ↓ (%) | 3.1 | 2.4 | 2.7 | 2.7 |
| Double-negation drift ↓ | 0.206 [0.193–0.220] | 0.168 [0.152–0.182] | 0.082 [0.067–0.098] | 0.082 [0.067–0.098] |
| Brier (yes/no, core) ↓ | 0.105 [0.089–0.122] | 0.098 [0.082–0.116] | 0.081 [0.062–0.103] | 0.081 [0.062–0.103] |
| ECE (yes/no, core) ↓ | 0.056 | 0.036 | 0.014 | 0.014 |
| Coverage @1% error, cross-fitted ↑ (%) | 2.0 | 0.0 | 2.7 | 2.7 |
| Injection attack success, held-out C+D ↓ (%) | 10.8 [3.8–18.4] | 19.2 [10.5–29.0] | 4.2 [0.0–9.6] | 4.2 [0.0–9.6] |
| Choice acc under injection C (%) | 81.7 | 81.7 | 90.0 | 90.0 |
| Choice acc under injection D (%) | 86.7 | 73.3 | 88.3 | 88.3 |
| Choice acc, same items clean (%) | 90.0 | 90.0 | 93.3 | 93.3 |
| Echo control choice acc (%) | 98.3 | 98.3 | 95.0 | 95.0 |
| Distractor choice acc (%) | 72.5 | 72.5 | 90.0 | 90.0 |
| Distractor, same items clean (%) | 80.0 | 85.0 | 90.0 | 90.0 |
| Neg. acc ID, wording 0 'someone who says … mistaken' (near train wordings) (%) | 82.0 | 81.0 | 88.0 | 88.0 |
| Neg. acc ID, wording 1 'reader who concluded … misreading' (truly unseen) (%) | 92.0 | 94.0 | 96.0 | 96.0 |
| Coverage @2% error, cross-fitted ↑ (%) | 16.1 | 21.8 | 19.9 | 19.9 |
| Coverage @3% error, cross-fitted ↑ (%) | 37.4 | 39.8 | 51.7 | 51.7 |
| Coverage @5% error, cross-fitted ↑ (%) | 63.4 | 66.6 | 73.4 | 73.4 |

**Paired differences vs jev_guard** (model − jev_guard, 95% bootstrap CI over the same groups; * = CI excludes 0)

| Metric | jev | g12_v06_A3_cal | g12_v06_A3_cal_bc |
|---|---|---|---|
| choice_acc_ID | +1.5 [+0.0, +3.3] | +5.0 [+2.0, +8.4]* | +5.0 [+2.0, +8.4]* |
| noul_base_acc_ID | +1.0 [+0.0, +2.6] | +2.0 [-1.5, +5.4] | +2.0 [-1.5, +5.4] |
| noul_neg_acc_ID | +0.5 [-1.6, +2.9] | +5.0 [+1.1, +9.0]* | +5.0 [+1.1, +9.0]* |
| choice_acc_ZS | +0.0 [+0.0, +0.0] | -2.1 [-6.7, +1.9] | -3.2 [-7.1, +0.0] |
| noul_base_acc_ZS | +1.1 [-2.3, +4.9] | +4.2 [+0.0, +9.8] | +4.2 [+0.0, +9.8] |
| noul_neg_acc_ZS | -1.1 [-3.8, +0.0] | +6.3 [-2.2, +14.3] | +6.3 [-2.2, +14.3] |
| brier_noul_core | -0.007 [-0.009, -0.004]* | -0.024 [-0.035, -0.011]* | -0.024 [-0.035, -0.011]* |
| complement_violation | -0.002 [-0.007, +0.004] | +0.007 [-0.006, +0.022] | +0.007 [-0.006, +0.022] |
| double_negation_drift | -0.039 [-0.047, -0.030]* | -0.125 [-0.146, -0.102]* | -0.125 [-0.146, -0.102]* |
| inj_ASR_pooled | +8.3 [+2.9, +14.5]* | -6.7 [-14.7, +0.0] | -6.7 [-14.7, +0.0] |
| dist_choice_acc | +0.0 [-6.9, +6.2] | +17.5 [+6.7, +30.6]* | +17.5 [+6.7, +30.6]* |

**Latency**

- jev_guard: {"api_per_call_median_ms": 193.92791693098843, "api_per_call_p95_ms": 394.8230544803656}
- jev: {"api_per_call_median_ms": 203.43395799864084, "api_per_call_p95_ms": 311.98124998481916}
- g12_v06_A3_cal: {}
- g12_v06_A3_cal_bc: {}
