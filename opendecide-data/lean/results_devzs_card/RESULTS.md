# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **800** in **200** groups. Brackets = 95% bootstrap CI over groups.

| Metric | q4b_v05_A3 | q4b_v05_A3_bc | qwen3-4b_zs | qwen3-30b-a3b_zs | qwen3-30b-a3b_zs_bc |
|---|---|---|---|---|---|
| Choice accuracy (%) | 62.5 [56.0–69.5] | 63.5 [57.0–70.5] | 62.5 [56.5–69.0] | 63.5 [57.0–70.5] | 64.5 [58.0–71.5] |
| Yes/no accuracy, base question (%) | 75.0 [69.5–81.0] | 75.0 [69.5–81.0] | 72.5 [66.5–78.5] | 77.0 [71.5–83.0] | 77.0 [71.5–83.0] |
| Yes/no accuracy, negated question (%) | 76.5 [71.0–82.5] | 76.5 [71.0–82.5] | 63.0 [56.5–70.0] | 49.0 [42.5–56.0] | 49.0 [42.5–56.0] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.087 [0.068–0.108] | 0.087 [0.068–0.108] | 0.519 [0.457–0.584] | 0.387 [0.323–0.448] | 0.387 [0.323–0.448] |
| Contradiction rate ↓ (%) | 6.5 | 6.5 | 52.5 | 39.0 | 39.0 |
| Pairs summing to 1±0.05 ↑ (%) | 68.5 | 68.5 | 36.0 | 52.5 | 52.5 |
| Paraphrase drift |ΔP| ↓ | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Paraphrase flip rate ↓ (%) | nan | nan | nan | nan | nan |
| Double-negation drift ↓ | 0.062 [0.049–0.078] | 0.062 [0.049–0.078] | 0.288 [0.228–0.347] | 0.049 [0.028–0.074] | 0.049 [0.028–0.074] |
| Brier (yes/no, core) ↓ | 0.178 [0.135–0.216] | 0.178 [0.135–0.216] | 0.369 [0.336–0.401] | 0.307 [0.259–0.354] | 0.307 [0.259–0.354] |
| ECE (yes/no, core) ↓ | 0.118 | 0.118 | 0.367 | 0.303 | 0.303 |
| Coverage @1% error, cross-fitted ↑ (%) | 18.8 | 18.8 | 14.3 | 0.0 | 0.0 |
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
