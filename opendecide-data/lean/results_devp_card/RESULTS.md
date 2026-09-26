# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **1728** in **492** groups. Brackets = 95% bootstrap CI over groups.

| Metric | gemma4-12b_zs | gemma4-12b_zs_cal_bc | g12_v06_A3 | g12_v06_A3_cal | g12_v06_A3_cal_bc |
|---|---|---|---|---|---|
| Choice accuracy (%) | 88.2 [84.7–91.4] | 88.2 [84.7–91.2] | 86.3 [82.7–89.6] | 86.3 [82.7–89.6] | 86.8 [83.3–90.0] |
| Yes/no accuracy, base question (%) | 84.1 [80.4–87.6] | 84.1 [80.4–87.6] | 86.6 [83.2–89.7] | 86.6 [83.2–89.7] | 86.6 [83.2–89.7] |
| Yes/no accuracy, negated question (%) | 76.3 [71.8–80.6] | 76.3 [71.8–80.6] | 85.5 [82.2–89.2] | 85.5 [82.2–89.2] | 85.5 [82.2–89.2] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.313 [0.269–0.354] | 0.181 [0.168–0.194] | 0.081 [0.071–0.092] | 0.084 [0.072–0.096] | 0.084 [0.072–0.096] |
| Contradiction rate ↓ (%) | 31.5 | 31.5 | 8.1 | 8.1 | 8.1 |
| Pairs summing to 1±0.05 ↑ (%) | 58.9 | 21.2 | 56.5 | 61.3 | 61.3 |
| Paraphrase drift |ΔP| ↓ | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Paraphrase flip rate ↓ (%) | nan | nan | nan | nan | nan |
| Double-negation drift ↓ | 0.318 [0.278–0.360] | 0.199 [0.184–0.215] | 0.084 [0.073–0.094] | 0.084 [0.072–0.096] | 0.084 [0.072–0.096] |
| Brier (yes/no, core) ↓ | 0.243 [0.219–0.268] | 0.176 [0.166–0.185] | 0.099 [0.084–0.116] | 0.099 [0.082–0.119] | 0.099 [0.082–0.119] |
| ECE (yes/no, core) ↓ | 0.238 | 0.059 | 0.034 | 0.034 | 0.034 |
| Coverage @1% error, cross-fitted ↑ (%) | 12.4 | 11.8 | 41.9 | 41.9 | 41.9 |
| Injection attack success, held-out C+D ↓ (%) | 40.0 [25.6–55.9] | 40.0 [25.6–55.9] | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] | 0.0 [0.0–0.0] |
| Choice acc under injection C (%) | 52.5 | 52.5 | 90.0 | 90.0 | 90.0 |
| Choice acc under injection D (%) | nan | nan | nan | nan | nan |
| Choice acc, same items clean (%) | 82.5 | 82.5 | 92.5 | 92.5 | 92.5 |
| Echo control choice acc (%) | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| Distractor choice acc (%) | 65.0 | 65.0 | 92.5 | 92.5 | 92.5 |
| Distractor, same items clean (%) | 87.5 | 87.5 | 90.0 | 90.0 | 90.0 |

**Latency**

- gemma4-12b_zs: {}
- gemma4-12b_zs_cal_bc: {}
- g12_v06_A3: {}
- g12_v06_A3_cal: {}
- g12_v06_A3_cal_bc: {}
