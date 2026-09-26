# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **600** in **150** groups. Brackets = 95% bootstrap CI over groups.

| Metric | gemma4-12b_zs | g12_v06_A3 | q4b_v05_A3 |
|---|---|---|---|
| Choice accuracy (%) | 85.3 [79.3–90.7] | 91.3 [86.7–95.3] | 95.3 [92.0–98.7] |
| Yes/no accuracy, base question (%) | 85.3 [79.3–90.7] | 92.0 [87.3–96.0] | 96.0 [92.7–98.7] |
| Yes/no accuracy, negated question (%) | 48.0 [39.3–55.3] | 89.3 [84.0–94.0] | 95.3 [92.0–98.7] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.542 [0.465–0.617] | 0.113 [0.095–0.133] | 0.023 [0.011–0.037] |
| Contradiction rate ↓ (%) | 54.7 | 9.3 | 2.0 |
| Pairs summing to 1±0.05 ↑ (%) | 38.7 | 34.0 | 93.3 |
| Paraphrase drift |ΔP| ↓ | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Paraphrase flip rate ↓ (%) | nan | nan | nan |
| Double-negation drift ↓ | 0.752 [0.688–0.814] | 0.226 [0.196–0.259] | 0.018 [0.008–0.032] |
| Brier (yes/no, core) ↓ | 0.462 [0.435–0.488] | 0.103 [0.083–0.126] | 0.038 [0.016–0.066] |
| ECE (yes/no, core) ↓ | 0.458 | 0.048 | 0.049 |
| Coverage @1% error, cross-fitted ↑ (%) | 4.8 | 22.5 | 66.7 |
| Injection attack success, held-out C+D ↓ (%) | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Choice acc under injection C (%) | nan | nan | nan |
| Choice acc under injection D (%) | nan | nan | nan |
| Choice acc, same items clean (%) | nan | nan | nan |
| Echo control choice acc (%) | nan | nan | nan |
| Distractor choice acc (%) | nan | nan | nan |
| Distractor, same items clean (%) | nan | nan | nan |

**Latency**

- gemma4-12b_zs: {}
- g12_v06_A3: {}
- q4b_v05_A3: {}
