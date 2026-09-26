# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **800** in **200** groups. Brackets = 95% bootstrap CI over groups.

| Metric | q4b_v05_A3 | q4b_v05_A3_bc | qwen3-4b_zs | qwen3-30b-a3b_zs | qwen3-30b-a3b_zs_bc |
|---|---|---|---|---|---|
| Choice accuracy (%) | 62.5 [56.0–69.5] | 65.0 [58.5–72.0] | 64.5 [58.0–71.0] | 64.5 [58.0–71.5] | 67.0 [61.0–74.0] |
| Yes/no accuracy, base question (%) | 77.5 [72.0–83.0] | 77.5 [72.0–83.0] | 75.5 [70.0–81.5] | 73.5 [67.5–79.5] | 73.5 [67.5–79.5] |
| Yes/no accuracy, negated question (%) | 78.5 [73.0–83.5] | 78.5 [73.0–83.5] | 71.5 [65.5–77.5] | 70.5 [64.0–77.5] | 70.5 [64.0–77.5] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.072 [0.055–0.089] | 0.072 [0.055–0.089] | 0.435 [0.369–0.502] | 0.404 [0.343–0.463] | 0.404 [0.343–0.463] |
| Contradiction rate ↓ (%) | 9.0 | 9.0 | 44.0 | 41.0 | 41.0 |
| Pairs summing to 1±0.05 ↑ (%) | 70.0 | 70.0 | 52.0 | 51.0 | 51.0 |
| Paraphrase drift |ΔP| ↓ | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] | nan [nan–nan] |
| Paraphrase flip rate ↓ (%) | nan | nan | nan | nan | nan |
| Double-negation drift ↓ | 0.062 [0.049–0.077] | 0.062 [0.049–0.077] | 0.331 [0.267–0.399] | 0.112 [0.074–0.151] | 0.112 [0.074–0.151] |
| Brier (yes/no, core) ↓ | 0.159 [0.123–0.193] | 0.159 [0.123–0.193] | 0.338 [0.307–0.367] | 0.255 [0.216–0.293] | 0.255 [0.216–0.293] |
| ECE (yes/no, core) ↓ | 0.080 | 0.080 | 0.335 | 0.247 | 0.247 |
| Coverage @1% error, cross-fitted ↑ (%) | 22.9 | 22.9 | 0.0 | 8.2 | 8.2 |
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
