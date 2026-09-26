# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **1728** in **492** groups. Brackets = 95% bootstrap CI over groups.

| Metric | qwen3-4b_zs | qwen3.5-4b_zs | qwen3.5-9b_zs | gemma4-12b_zs | qwen3-4b_zs_bc | qwen3.5-4b_zs_bc | qwen3.5-9b_zs_bc | gemma4-12b_zs_bc |
|---|---|---|---|---|---|---|---|---|
| Choice accuracy (%) | 82.8 [79.2–86.7] | 77.7 [73.7–81.8] | 84.7 [81.2–88.3] | 87.9 [84.5–90.8] | 83.6 [79.9–87.3] | 79.3 [75.3–83.5] | 83.1 [79.2–86.8] | 88.2 [84.8–91.3] |
| Yes/no accuracy, base question (%) | 80.1 [75.9–84.0] | 75.0 [70.5–79.3] | 76.3 [72.2–80.4] | 82.3 [78.4–85.9] | 80.1 [75.9–84.0] | 75.0 [70.5–79.3] | 76.3 [72.2–80.4] | 82.3 [78.4–85.9] |
| Yes/no accuracy, negated question (%) | 54.0 [49.2–59.5] | 57.0 [52.6–62.1] | 61.3 [56.7–66.2] | 65.6 [61.1–70.4] | 54.0 [49.2–59.5] | 57.0 [52.6–62.1] | 61.3 [56.7–66.2] | 65.6 [61.1–70.4] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.476 [0.426–0.521] | 0.340 [0.318–0.362] | 0.345 [0.325–0.365] | 0.309 [0.268–0.351] | 0.476 [0.426–0.521] | 0.340 [0.318–0.362] | 0.345 [0.325–0.365] | 0.309 [0.268–0.351] |
| Contradiction rate ↓ (%) | 48.7 | 47.0 | 51.6 | 32.3 | 48.7 | 47.0 | 51.6 | 32.3 |
| Pairs summing to 1±0.05 ↑ (%) | 41.7 | 6.2 | 6.7 | 55.4 | 41.7 | 6.2 | 6.7 | 55.4 |
| Paraphrase drift |ΔP| ↓ | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Paraphrase flip rate ↓ (%) | nan | nan | nan | nan | nan | nan | nan | nan |
| Double-negation drift ↓ | 0.467 [0.422–0.513] | 0.278 [0.259–0.298] | 0.201 [0.188–0.216] | 0.353 [0.313–0.396] | 0.467 [0.422–0.513] | 0.278 [0.259–0.298] | 0.201 [0.188–0.216] | 0.353 [0.313–0.396] |
| Brier (yes/no, core) ↓ | 0.366 [0.347–0.386] | 0.218 [0.203–0.233] | 0.210 [0.197–0.223] | 0.276 [0.250–0.300] | 0.366 [0.347–0.386] | 0.218 [0.203–0.233] | 0.210 [0.197–0.223] | 0.276 [0.250–0.300] |
| ECE (yes/no, core) ↓ | 0.357 | 0.099 | 0.066 | 0.262 | 0.357 | 0.099 | 0.066 | 0.262 |
| Coverage @1% error, cross-fitted ↑ (%) | 0.0 | 5.5 | 2.6 | 8.9 | 0.0 | 5.5 | 2.6 | 8.9 |
| Injection attack success, held-out C+D ↓ (%) | 47.5 [32.3–63.2] | 67.5 [53.7–82.1] | 50.0 [35.0–65.9] | 40.0 [25.6–55.9] | 47.5 [32.3–63.2] | 67.5 [53.7–82.1] | 50.0 [35.0–65.9] | 40.0 [25.6–55.9] |
| Choice acc under injection C (%) | 42.5 | 32.5 | 45.0 | 50.0 | 42.5 | 32.5 | 45.0 | 50.0 |
| Choice acc under injection D (%) | nan | nan | nan | nan | nan | nan | nan | nan |
| Choice acc, same items clean (%) | 87.5 | 87.5 | 87.5 | 82.5 | 87.5 | 87.5 | 87.5 | 82.5 |
| Echo control choice acc (%) | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| Distractor choice acc (%) | 70.0 | 45.0 | 70.0 | 65.0 | 70.0 | 45.0 | 70.0 | 65.0 |
| Distractor, same items clean (%) | 82.5 | 85.0 | 87.5 | 87.5 | 82.5 | 85.0 | 87.5 | 87.5 |

**Latency**

- qwen3-4b_zs: {}
- qwen3.5-4b_zs: {}
- qwen3.5-9b_zs: {}
- gemma4-12b_zs: {}
- qwen3-4b_zs_bc: {}
- qwen3.5-4b_zs_bc: {}
- qwen3.5-9b_zs_bc: {}
- gemma4-12b_zs_bc: {}
