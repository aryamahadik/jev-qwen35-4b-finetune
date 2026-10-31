# TEACH-0 report (PREREG A36): Claude teachers vs Jev vs C1, 2,000 dev rows

Sample T sha a4c2b788da5f3e90: S 660 + U 1,340 gate dev rows. Answered rows: Jev 2000, C1 2000, haiku 1980. Missing or invalid answers count as wrong.

## Accuracy (%)

| subset | n | Jev | C1 | haiku |
|---|---|---|---|---|
| T | 2000 | 78.0 | 77.8 | 83.3 |
| S | 660 | 71.4 | 68.2 | 74.2 |
| U | 1340 | 81.2 | 82.6 | 87.8 |
| public (decision) | 1722 | 79.0 | 78.6 | 80.8 |
| authored (hard_dev, pg_dev) | 278 | 71.6 | 73.0 | 98.9 |
| yes/no | 977 | 84.2 | 84.5 | 87.5 |
| choice | 1023 | 71.9 | 71.5 | 79.4 |
| split dev_nc | 468 | 65.0 | 62.4 | 68.4 |
| split taskbank_dev | 276 | 81.5 | 81.9 | 81.2 |
| split hard_dev | 72 | 79.2 | 73.6 | 98.6 |
| split dev_negwords | 192 | 84.9 | 87.0 | 85.4 |
| split dev_claims | 152 | 85.5 | 90.1 | 93.4 |
| split pg_dev | 206 | 68.9 | 72.8 | 99.0 |
| split devzs | 151 | 73.5 | 77.5 | 75.5 |
| split devp_card | 348 | 89.1 | 85.3 | 86.5 |
| split dev | 135 | 86.7 | 87.4 | 94.1 |

## Yes/no Brier (lower is better; teachers from stated confidence)

| model | Brier | rows with a probability / yes-no rows |
|---|---|---|
| Jev | 0.113 | 977 / 977 |
| C1 | 0.112 | 977 / 977 |
| haiku | 0.098 | 966 / 977 |

## Decision (public-source subset, paired bootstrap 95% CI, 10,000 draws)

| model | diff vs Jev (pt) | 95% CI | diff vs C1 (pt) | 95% CI | A36 verdict |
|---|---|---|---|---|---|
| haiku | +1.9 | [+0.2, +3.5] | +2.2 | [+0.5, +3.9] | **MARGINAL (b)** |
| C1 (context) | -0.3 | [-2.0, +1.3] | - | - | - |
