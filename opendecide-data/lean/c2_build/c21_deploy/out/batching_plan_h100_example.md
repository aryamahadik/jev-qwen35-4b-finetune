# Batching plan (modelled) curve `h100_s1_modal_reference`

Curve tag: {'tag': 'author-run', 'n_per_point': 660, 'source': 'speed/opt_c1_round2_20261017/h100/results/session_20261017_161152/volume/session_20261017_161152/r2_a/measure.json (arm A, SGLang 0.5.20 S1 bf16, H100)', 'mix': 'N traffic-like dev mix, 660 calls'}. u* = 0.59 (break-even vs Jev; cost_calc.py computes it from rate and T_sat). T_sat = 325,826 decisions/h; one instance needs 192,237 decisions/h (53.4 per second) to stay at u*.

WARNING: the curve has only 2 measured points (fewer than 5): the operating point is a coarse step function; rerun with the full ladder

SLO server p95 <= 60.0 ms: utilisation ceiling = 0.3479 of T_sat (ladder c = 1). This is BELOW u*: interactive traffic alone cannot reach break-even within the SLO; use the levers.

## solo_dev
mean 417 dph, peak 0.3 dec/s; instances needed for the peak: 1

| N | mean util | time at util >= u* | time overloaded | peak p95 ms | meets SLO at peak | background fill dph to reach u* |
|---|---|---|---|---|---|---|
| 1 | 0.0013 | 0.0 | 0.0 | 38.09 | True | 191,821 |
| 2 | 0.0006 | 0.0 | 0.0 | 38.09 | True | 384,058 |
| 3 | 0.0004 | 0.0 | 0.0 | 38.09 | True | 576,295 |
| 4 | 0.0003 | 0.0 | 0.0 | 38.09 | True | 768,533 |

## small_team
mean 5,832 dph, peak 4.0 dec/s; instances needed for the peak: 1

| N | mean util | time at util >= u* | time overloaded | peak p95 ms | meets SLO at peak | background fill dph to reach u* |
|---|---|---|---|---|---|---|
| 1 | 0.0179 | 0.0 | 0.0 | 38.09 | True | 186,405 |
| 2 | 0.0089 | 0.0 | 0.0 | 38.09 | True | 378,643 |
| 3 | 0.006 | 0.0 | 0.0 | 38.09 | True | 570,880 |
| 4 | 0.0045 | 0.0 | 0.0 | 38.09 | True | 763,117 |

## company
mean 146,880 dph, peak 100.0 dec/s; instances needed for the peak: 4

| N | mean util | time at util >= u* | time overloaded | peak p95 ms | meets SLO at peak | background fill dph to reach u* |
|---|---|---|---|---|---|---|
| 1 | 0.4408 | 0.3462 | 0.1438 |  |  | 45,357 |
| 2 | 0.2254 | 0.0 | 0.0 | 911.16 | False | 237,595 |
| 3 | 0.1503 | 0.0 | 0.0 | 911.16 | False | 429,832 |
| 4 | 0.1127 | 0.0 | 0.0 | 38.09 | True | 622,069 |
| 5 | 0.0902 | 0.0 | 0.0 | 38.09 | True | 814,307 |
| 6 | 0.0751 | 0.0 | 0.0 | 38.09 | True | 1,006,544 |
| 7 | 0.0644 | 0.0 | 0.0 | 38.09 | True | 1,198,781 |
| 8 | 0.0563 | 0.0 | 0.0 | 38.09 | True | 1,391,019 |
| 9 | 0.0501 | 0.0 | 0.0 | 38.09 | True | 1,583,256 |
| 10 | 0.0451 | 0.0 | 0.0 | 38.09 | True | 1,775,493 |
| 11 | 0.041 | 0.0 | 0.0 | 38.09 | True | 1,967,731 |
| 12 | 0.0376 | 0.0 | 0.0 | 38.09 | True | 2,159,968 |

## ci_burst
mean 9,000 dph, peak 30.0 dec/s; instances needed for the peak: 1

| N | mean util | time at util >= u* | time overloaded | peak p95 ms | meets SLO at peak | background fill dph to reach u* |
|---|---|---|---|---|---|---|
| 1 | 0.0276 | 0.0 | 0.0 | 38.09 | True | 183,237 |
| 2 | 0.0138 | 0.0 | 0.0 | 38.09 | True | 375,475 |
| 3 | 0.0092 | 0.0 | 0.0 | 38.09 | True | 567,712 |
| 4 | 0.0069 | 0.0 | 0.0 | 38.09 | True | 759,949 |
| 5 | 0.0055 | 0.0 | 0.0 | 38.09 | True | 952,187 |
| 6 | 0.0046 | 0.0 | 0.0 | 38.09 | True | 1,144,424 |

## steady_high
mean 216,000 dph, peak 60.0 dec/s; instances needed for the peak: 2

| N | mean util | time at util >= u* | time overloaded | peak p95 ms | meets SLO at peak | background fill dph to reach u* |
|---|---|---|---|---|---|---|
| 1 | 0.6629 | 1.0 | 0.0 | 911.16 | False | 0 |
| 2 | 0.3315 | 0.0 | 0.0 | 38.09 | True | 168,475 |
| 3 | 0.221 | 0.0 | 0.0 | 38.09 | True | 360,712 |
| 4 | 0.1657 | 0.0 | 0.0 | 38.09 | True | 552,949 |
| 5 | 0.1326 | 0.0 | 0.0 | 38.09 | True | 745,187 |
| 6 | 0.1105 | 0.0 | 0.0 | 38.09 | True | 937,424 |
| 7 | 0.0947 | 0.0 | 0.0 | 38.09 | True | 1,129,661 |
| 8 | 0.0829 | 0.0 | 0.0 | 38.09 | True | 1,321,899 |
| 9 | 0.0737 | 0.0 | 0.0 | 38.09 | True | 1,514,136 |
| 10 | 0.0663 | 0.0 | 0.0 | 38.09 | True | 1,706,373 |
| 11 | 0.0603 | 0.0 | 0.0 | 38.09 | True | 1,898,611 |
| 12 | 0.0552 | 0.0 | 0.0 | 38.09 | True | 2,090,848 |
