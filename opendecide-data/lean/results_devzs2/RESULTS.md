# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **760** in **190** groups. Brackets = 95% bootstrap CI over groups.

| Metric | q4b_v05_A3 | q4b_v05_A3_bc | qwen3-4b_zs | qwen3-30b-a3b_zs | qwen3-30b-a3b_zs_bc |
|---|---|---|---|---|---|
| Choice accuracy (%) | 76.8 [71.1–83.2] | 81.1 [75.3–86.3] | 77.4 [71.6–83.2] | 82.6 [76.8–88.4] | 85.3 [80.0–90.5] |
| Yes/no accuracy, base question (%) | 81.1 [74.7–86.3] | 81.1 [74.7–86.3] | 78.4 [72.6–84.2] | 78.4 [72.6–84.2] | 78.4 [72.6–84.2] |
| Yes/no accuracy, negated question (%) | 74.2 [67.9–80.5] | 74.2 [67.9–80.5] | 54.2 [46.8–61.6] | 59.5 [52.1–66.8] | 59.5 [52.1–66.8] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.097 [0.082–0.114] | 0.097 [0.082–0.114] | 0.493 [0.424–0.563] | 0.388 [0.328–0.448] | 0.388 [0.328–0.448] |
| Contradiction rate ↓ (%) | 10.0 | 10.0 | 49.5 | 41.1 | 41.1 |
| Pairs summing to 1±0.05 ↑ (%) | 46.3 | 46.3 | 41.6 | 48.9 | 48.9 |
| Paraphrase drift |ΔP| ↓ | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Paraphrase flip rate ↓ (%) | nan | nan | nan | nan | nan |
| Double-negation drift ↓ | 0.073 [0.063–0.085] | 0.073 [0.063–0.085] | 0.437 [0.368–0.501] | 0.298 [0.239–0.353] | 0.298 [0.239–0.353] |
| Brier (yes/no, core) ↓ | 0.159 [0.125–0.195] | 0.159 [0.125–0.195] | 0.369 [0.340–0.398] | 0.303 [0.269–0.338] | 0.303 [0.269–0.338] |
| ECE (yes/no, core) ↓ | 0.053 | 0.053 | 0.362 | 0.290 | 0.290 |
| Coverage @1% error, cross-fitted ↑ (%) | 5.2 | 5.2 | 4.2 | 0.0 | 0.0 |
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
