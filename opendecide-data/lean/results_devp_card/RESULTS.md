# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **1728** in **492** groups. Brackets = 95% bootstrap CI over groups.

| Metric | q35_08b_wb_off | q35_08b_wb_on |
|---|---|---|
| Choice accuracy (%) | 54.3 [49.0–59.4] | 46.2 [41.0–51.0] |
| Yes/no accuracy, base question (%) | 49.7 [44.5–54.3] | 49.7 [44.5–54.3] |
| Yes/no accuracy, negated question (%) | 50.3 [45.7–55.5] | 50.3 [45.7–55.5] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.956 [0.948–0.962] | 0.971 [0.969–0.973] |
| Contradiction rate ↓ (%) | 100.0 | 100.0 |
| Pairs summing to 1±0.05 ↑ (%) | 0.0 | 0.0 |
| Paraphrase drift |ΔP| ↓ | nan [nan–nan] | nan [nan–nan] |
| Paraphrase flip rate ↓ (%) | nan | nan |
| Double-negation drift ↓ | 0.022 [0.018–0.027] | 0.013 [0.012–0.014] |
| Brier (yes/no, core) ↓ | 0.481 [0.467–0.498] | 0.487 [0.472–0.505] |
| ECE (yes/no, core) ↓ | 0.480 | 0.486 |
| Coverage @1% error, cross-fitted ↑ (%) | 0.3 | 0.0 |
| Injection attack success, held-out C+D ↓ (%) | 72.5 [57.5–85.7] | 30.0 [16.7–44.7] |
| Choice acc under injection C (%) | 12.5 | 7.5 |
| Choice acc under injection D (%) | nan | nan |
| Choice acc, same items clean (%) | 45.0 | 10.0 |
| Echo control choice acc (%) | 82.5 | 30.0 |
| Distractor choice acc (%) | 45.0 | 27.5 |
| Distractor, same items clean (%) | 50.0 | 25.0 |

**Latency**

- q35_08b_wb_off: {}
- q35_08b_wb_on: {}
