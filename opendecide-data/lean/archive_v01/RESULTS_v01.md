# OpenDecide lean benchmark v0.1 — first results

Rows scored (all models, same rows): **1915** in **295** groups. Brackets = 95% bootstrap CI over groups.

| Metric | edge_zeroshot | base_zeroshot | edge_A0 | edge_A3 |
|---|---|---|---|---|
| Choice accuracy, in-domain (%) | 43.5 [37.0–50.5] | 58.5 [51.6–65.0] | 90.0 [85.9–94.1] | 81.0 [75.7–86.6] |
| Choice accuracy, zero-shot (%) | 30.5 [22.0–41.1] | 36.8 [27.0–46.2] | 40.0 [30.1–50.6] | 36.8 [27.9–47.3] |
| Yes/no accuracy, base question, ID (%) | 52.0 [45.0–59.2] | 57.5 [50.8–63.6] | 80.5 [75.1–85.4] | 70.0 [64.1–76.0] |
| Yes/no accuracy, base question, ZS (%) | 49.5 [39.8–59.6] | 48.4 [38.6–58.3] | 42.1 [32.3–52.1] | 45.3 [35.4–54.9] |
| Yes/no accuracy, negated question, ID (%) | 48.0 [40.9–54.9] | 46.5 [40.0–53.1] | 36.5 [30.1–42.6] | 44.0 [36.9–50.7] |
| Yes/no accuracy, negated question, ZS (%) | 45.3 [35.7–55.4] | 46.3 [36.5–56.0] | 52.6 [42.3–62.6] | 49.5 [40.0–59.6] |
| Complement violation |P(A)+P(not A)−1| ↓ | 0.491 [0.459–0.521] | 0.321 [0.305–0.335] | 0.655 [0.619–0.690] | 0.324 [0.303–0.347] |
| Contradiction rate ↓ (%) | 67.8 | 93.6 | 78.0 | 50.8 |
| Pairs summing to 1±0.05 ↑ (%) | 6.4 | 2.4 | 6.4 | 7.1 |
| Paraphrase drift |ΔP| ↓ | 0.459 [0.428–0.490] | 0.090 [0.081–0.098] | 0.157 [0.131–0.188] | 0.266 [0.240–0.293] |
| Paraphrase flip rate ↓ (%) | 43.1 | 7.1 | 16.3 | 35.6 |
| Double-negation drift ↓ | 0.246 [0.226–0.270] | 0.110 [0.101–0.119] | 0.112 [0.091–0.134] | 0.526 [0.499–0.554] |
| Brier (yes/no, core) ↓ | 0.366 [0.345–0.385] | 0.284 [0.268–0.300] | 0.302 [0.282–0.323] | 0.322 [0.313–0.331] |
| ECE (yes/no, core) ↓ | 0.299 | 0.169 | 0.258 | 0.254 |
| Coverage @1% error, cross-fitted ↑ (%) | 0.0 | 0.0 | 0.0 | 0.1 |
| Injection attack success, held-out C+D ↓ (%) | 80.0 [70.4–88.6] | 75.0 [64.4–84.4] | 65.0 [54.0–75.0] | 28.3 [18.8–38.0] |
| Choice acc under injection C (%) | 13.3 | 18.3 | 28.3 | 71.7 |
| Choice acc under injection D (%) | 18.3 | 25.0 | 40.0 | 55.0 |
| Choice acc, same items clean (%) | 41.7 | 65.0 | 86.7 | 85.0 |
| Echo control choice acc (%) | 96.7 | 93.3 | 100.0 | 95.0 |
| Distractor choice acc (%) | 40.0 | 50.0 | 72.5 | 85.0 |
| Distractor, same items clean (%) | 52.5 | 60.0 | 92.5 | 87.5 |

**Latency**

- edge_zeroshot: {"latency_mps": {"device": "mps", "median_ms": 7.829457987099886, "p95_ms": 101.31575004197657, "n": 200}, "latency_cpu": {"device": "cpu", "median_ms": 7.0451670326292515, "p95_ms": 9.197917068377137, "n": 100}}
- base_zeroshot: {"latency_mps": {"device": "mps", "median_ms": 68.95712506957352, "p95_ms": 221.69745794963092, "n": 200}, "latency_cpu": {"device": "cpu", "median_ms": 122.03829200007021, "p95_ms": 302.34749999362975, "n": 100}}
- edge_A0: {}
- edge_A3: {}
