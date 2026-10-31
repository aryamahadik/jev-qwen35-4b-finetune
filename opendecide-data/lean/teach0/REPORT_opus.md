# TEACH-0 report (PREREG A36): Claude teachers vs Jev vs C1, 2,000 dev rows

Sample T sha a4c2b788da5f3e90: 1000 rows scored (S 294 + U 706) = the rows of opus. Answered rows: Jev 1000, C1 1000, haiku 1000, opus 1000. Missing or invalid answers count as wrong.

## Accuracy (%)

| subset | n | Jev | C1 | haiku | opus |
|---|---|---|---|---|---|
| T | 1000 | 77.6 | 78.0 | 84.6 | 87.9 |
| S | 294 | 70.1 | 66.3 | 72.4 | 78.9 |
| U | 706 | 80.7 | 82.9 | 89.7 | 91.6 |
| public (decision) | 858 | 78.6 | 78.2 | 82.2 | 86.0 |
| authored (hard_dev, pg_dev) | 142 | 71.8 | 76.8 | 99.3 | 99.3 |
| yes/no | 496 | 82.7 | 83.3 | 88.5 | 91.5 |
| choice | 504 | 72.6 | 72.8 | 80.8 | 84.3 |
| split dev_nc | 233 | 66.1 | 61.8 | 68.7 | 74.2 |
| split taskbank_dev | 127 | 81.1 | 81.9 | 82.7 | 83.5 |
| split hard_dev | 32 | 84.4 | 84.4 | 100.0 | 100.0 |
| split dev_negwords | 98 | 80.6 | 87.8 | 87.8 | 92.9 |
| split dev_claims | 78 | 84.6 | 92.3 | 96.2 | 93.6 |
| split pg_dev | 110 | 68.2 | 74.5 | 99.1 | 99.1 |
| split devzs | 80 | 73.8 | 76.2 | 75.0 | 92.5 |
| split devp_card | 168 | 89.3 | 85.1 | 88.7 | 90.5 |
| split dev | 74 | 85.1 | 82.4 | 94.6 | 93.2 |

## Yes/no Brier (lower is better; teachers from stated confidence)

| model | Brier | rows with a probability / yes-no rows |
|---|---|---|
| Jev | 0.121 | 496 / 496 |
| C1 | 0.119 | 496 / 496 |
| haiku | 0.099 | 496 / 496 |
| opus | 0.073 | 496 / 496 |

## Decision (public-source subset, paired bootstrap 95% CI, 10,000 draws)

| model | diff vs Jev (pt) | 95% CI | diff vs C1 (pt) | 95% CI | A36 verdict |
|---|---|---|---|---|---|
| haiku | +3.6 | [+1.3, +5.9] | +4.0 | [+1.5, +6.5] | **MARGINAL (b)** |
| opus | +7.5 | [+4.9, +10.0] | +7.8 | [+5.1, +10.5] | **PROCEED (a)** |
| C1 (context) | -0.3 | [-2.7, +2.0] | - | - | - |
