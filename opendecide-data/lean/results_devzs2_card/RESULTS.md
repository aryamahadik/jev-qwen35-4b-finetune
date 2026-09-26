# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **760** in **190** groups. Brackets = 95% bootstrap CI over groups.

| Metric | q4b_v05_A3 | q4b_v05_A3_bc | qwen3-4b_zs | qwen3-30b-a3b_zs | qwen3-30b-a3b_zs_bc |
|---|---|---|---|---|---|
| Choice accuracy (%) | 81.6 [75.8–87.4] | 81.1 [75.3–86.8] | 78.9 [72.6–84.7] | 82.6 [77.4–87.9] | 82.6 [77.4–87.9] |
| Yes/no accuracy, base question (%) | 85.8 [80.5–90.5] | 85.8 [80.5–90.5] | 82.1 [76.3–87.4] | 86.8 [81.6–91.6] | 86.8 [81.6–91.6] |
| Yes/no accuracy, negated question (%) | 86.8 [82.1–91.6] | 86.8 [82.1–91.6] | 51.1 [43.7–58.4] | 60.0 [53.7–67.4] | 60.0 [53.7–67.4] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.061 [0.048–0.077] | 0.061 [0.048–0.077] | 0.502 [0.434–0.570] | 0.375 [0.314–0.442] | 0.375 [0.314–0.442] |
| Contradiction rate ↓ (%) | 8.4 | 8.4 | 51.1 | 37.4 | 37.4 |
| Pairs summing to 1±0.05 ↑ (%) | 75.8 | 75.8 | 44.7 | 48.9 | 48.9 |
| Paraphrase drift |ΔP| ↓ | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Paraphrase flip rate ↓ (%) | nan | nan | nan | nan | nan |
| Double-negation drift ↓ | 0.077 [0.060–0.095] | 0.077 [0.060–0.095] | 0.429 [0.366–0.494] | 0.378 [0.315–0.441] | 0.378 [0.315–0.441] |
| Brier (yes/no, core) ↓ | 0.108 [0.078–0.139] | 0.108 [0.078–0.139] | 0.369 [0.341–0.396] | 0.292 [0.260–0.324] | 0.292 [0.260–0.324] |
| ECE (yes/no, core) ↓ | 0.041 | 0.041 | 0.362 | 0.284 | 0.284 |
| Coverage @1% error, cross-fitted ↑ (%) | 2.1 | 2.1 | 9.2 | 0.0 | 0.0 |
| Injection attack success, held-out C+D ↓ (%) | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Choice acc under injection C (%) | nan | nan | nan | nan | nan |
| Choice acc under injection D (%) | nan | nan | nan | nan | nan |
| Choice acc, same items clean (%) | nan | nan | nan | nan | nan |
| Echo control choice acc (%) | nan | nan | nan | nan | nan |
| Distractor choice acc (%) | nan | nan | nan | nan | nan |
| Distractor, same items clean (%) | nan | nan | nan | nan | nan |

**Latency**

- q4b_v05_A3: {}
- q4b_v05_A3_bc: {}
- qwen3-4b_zs: {}
- qwen3-30b-a3b_zs: {}
- qwen3-30b-a3b_zs_bc: {}
