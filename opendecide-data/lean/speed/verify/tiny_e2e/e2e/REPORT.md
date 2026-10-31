# SPEED-2 report: session `e2e`

Generated 2026-10-13T01:17:13Z by hosting/speed_bench.py. Dev rows only (gate dev splits). Workloads manifest sha256 `e57ed361f59f4d82`; calls P 40, S 24, N 12, R 20 (68 tasks).
Parity bars: argmax agreement >= 99.5%, |accuracy diff| <= 0.3 pt (1.0 pt for FP8 arms); gated against the baseline arm **A0** of this session; the stored L4 reads are context only.

## Arms

| arm | engine | GPU | region | boot s | flags |
|---|---|---|---|---|---|
| A0 | hf | cpu (e2e) | None | 0.0 | `{"legacy": true, "choice_views": 2}` |
| A1 | hf | cpu (e2e) | None | 0.0 | `{"legacy": false, "twoview_split": true, "graph_plan": "speed1", "tokenize_outside_lock": true, "cross_batch": false, "choice_views": 2}` |
| A2 | hf | cpu (e2e) | None | 0.0 | `{"legacy": false, "twoview_split": true, "graph_plan": "speed1", "tokenize_outside_lock": true, "cross_batch": true, "batch_wait_ms": 0, "choice_views": 2}` |
| A3 | hf | cpu (e2e) | None | 0.0 | `{"legacy": false, "twoview_split": true, "graph_plan": "speed1", "tokenize_outside_lock": true, "cross_batch": true, "batch_wait_ms": 0, "choice_views": 2}` |
| S1 | sglang | fake SGLang (tiny model) | None | 0.0 | `{}` |

## Latency, S at concurrency 1 (ms, client = laptop round trip)

| arm | client p50 | p95 | p99 | server p50 | server p95 | network p50 | failed |
|---|---|---|---|---|---|---|---|
| A0 | 53.5 | 75.6 | 108.9 | 52.3 | 74.6 | 1.2 | 0 |
| A1 | 60.1 | 86.1 | 121.5 | 59.0 | 84.3 | 1.1 | 0 |
| A2 | 48.7 | 65.8 | 95.0 | 47.7 | 64.8 | 1.1 | 0 |
| A3 | 65.8 | 86.9 | 99.0 | 64.4 | 85.8 | 1.1 | 0 |
| S1 | 62.2 | 83.5 | 84.3 | 61.1 | 82.4 | 1.1 | 0 |

## Throughput, S closed loop (decisions/hour; failed calls in brackets)

| arm | c=1 | c=2 | c=4 | c=8 | c=16 | sustained | at c |
|---|---|---|---|---|---|---|---|
| A0 | 74,128 | 98,118 | 97,540 | 104,318 | 56,665 | 104,318 | 8 |
| A1 | 69,103 | 72,288 | 94,244 | 100,013 | 92,309 | 100,013 | 8 |
| A2 | 83,418 | 90,279 | 98,370 | 123,018 | 46,572 | 123,018 | 8 |
| A3 | 63,000 | 69,580 | 72,868 | 90,530 | 45,736 | 90,530 | 8 |
| S1 | 68,432 | 78,426 | 83,740 | 94,351 | 63,196 | 94,351 | 8 |

## Cost, $ per 1,000 decisions (rate $3.95/h x region multiplier {"any": 1.0, "us-east": 1.75}, multipliers to be confirmed; / utilisation)

| arm | any @ 100% | any @ 40% | us-east @ 100% | us-east @ 40% |
|---|---|---|---|---|
| A0 | 0.0379 | 0.0947 | 0.0663 | 0.1657 |
| A1 | 0.0395 | 0.0987 | 0.0691 | 0.1728 |
| A2 | 0.0321 | 0.0803 | 0.0562 | 0.1405 |
| A3 | 0.0436 | 0.1091 | 0.0764 | 0.1909 |
| S1 | 0.0419 | 0.1047 | 0.0733 | 0.1832 |

## Other workloads

| arm | P pass c=16 decisions/h | P pass s | N c=1 p50 / p99 ms | R c=1 p50 ms | R c=8 decisions/h | R c=8 cached-token share | batch rows mean (S c=16) |
|---|---|---|---|---|---|---|---|
| A0 | 71,174 | 2.0 | 39.2 / 49.2 | 23.0 | 132,411 | - | 1.22 |
| A1 | 67,879 | 2.1 | 41.0 / 49.0 | 21.7 | 128,536 | - | 1.00 |
| A2 | 77,476 | 1.9 | 38.2 / 47.0 | 20.9 | 167,104 | - | 1.78 |
| A3 | 63,775 | 2.3 | 52.3 / 76.3 | 31.7 | 109,135 | - | 4.44 |
| S1 | 59,936 | 2.4 | 44.8 / 76.2 | 24.8 | 117,485 | 0.0% | 1.11 |

## Parity, gated vs A0 (same session)

| arm | set | rows | argmax agree | acc arm | acc base | diff pt | bar pt | mean / p99 / max abs dp | result |
|---|---|---|---|---|---|---|---|---|---|
| A0 | **gate** | | | | | | | | **BASELINE** |
| A1 | P | 40 | 100.00% | 32.50 | 32.50 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| A1 | R (rows both answered) | 20 | 100.00% | 35.00 | 35.00 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| A1 | **gate** | | | | | | | | **PASS** |
| A2 | P | 40 | 100.00% | 32.50 | 32.50 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| A2 | R (rows both answered) | 20 | 100.00% | 35.00 | 35.00 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| A2 | **gate** | | | | | | | | **PASS** |
| A3 | P | 40 | 85.00% | 37.50 | 32.50 | 5.00 | 1.0 | 0.0194 / 0.0410 / 0.0410 | FAIL |
| A3 | R (rows both answered) | 20 | 85.00% | 30.00 | 35.00 | -5.00 | 1.0 | 0.0236 / 0.0489 / 0.0489 | FAIL |
| A3 | **gate** | | | | | | | | **FAIL** |
| S1 | P | 40 | 100.00% | 32.50 | 32.50 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| S1 | R (rows both answered) | 20 | 100.00% | 35.00 | 35.00 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| S1 | **gate** | | | | | | | | **PASS** |

### By type and options bucket (P vs baseline: argmax agree / diff pt / max abs dp)

- A1: noul n=14 100.00% / 0.00 / 0.0000; 2-4 n=10 100.00% / 0.00 / 0.0000; 5-9 n=8 100.00% / 0.00 / 0.0000; 10-25 n=5 100.00% / 0.00 / 0.0000; 26+ n=3 100.00% / 0.00 / 0.0000
- A2: noul n=14 100.00% / 0.00 / 0.0000; 2-4 n=10 100.00% / 0.00 / 0.0000; 5-9 n=8 100.00% / 0.00 / 0.0000; 10-25 n=5 100.00% / 0.00 / 0.0000; 26+ n=3 100.00% / 0.00 / 0.0000
- A3: noul n=14 100.00% / 0.00 / 0.0410; 2-4 n=10 80.00% / 20.00 / 0.0245; 5-9 n=8 87.50% / 0.00 / 0.0291; 10-25 n=5 60.00% / 0.00 / 0.0170; 26+ n=3 66.67% / 0.00 / 0.0245
- S1: noul n=14 100.00% / 0.00 / 0.0000; 2-4 n=10 100.00% / 0.00 / 0.0000; 5-9 n=8 100.00% / 0.00 / 0.0000; 10-25 n=5 100.00% / 0.00 / 0.0000; 26+ n=3 100.00% / 0.00 / 0.0000

## Parity vs the stored L4 reads (context, not gated; 2view served read)

| arm | rows | argmax agree | acc arm | acc L4 | diff pt | mean / p99 / max abs dp | bars |
|---|---|---|---|---|---|---|---|
| A0 | 40 | 37.50% | 32.50 | 85.00 | -52.50 | 0.4946 / 0.9013 / 0.9013 | FAIL |
| A1 | 40 | 37.50% | 32.50 | 85.00 | -52.50 | 0.4946 / 0.9013 / 0.9013 | FAIL |
| A2 | 40 | 37.50% | 32.50 | 85.00 | -52.50 | 0.4946 / 0.9013 / 0.9013 | FAIL |
| A3 | 40 | 37.50% | 37.50 | 85.00 | -47.50 | 0.4911 / 0.9032 / 0.9032 | FAIL |
| S1 | 40 | 37.50% | 32.50 | 85.00 | -52.50 | 0.4946 / 0.9013 / 0.9013 | FAIL |

## Reversed-view check

Stored L4 reads: reversed view = 2 x served - identity on 26 choice rows; invalid rows 0, max violation 1.6e-07 -> PASS.

- A0 (per-view answers, 26 rows): identity view vs L4 identity agree 23.08%, max dp 0.8932; reversed view vs L4 reversed agree 15.38%, max dp 0.9348; reconstruction valid PASS.
- A1 (per-view answers, 26 rows): identity view vs L4 identity agree 23.08%, max dp 0.8932; reversed view vs L4 reversed agree 15.38%, max dp 0.9348; reconstruction valid PASS.
- A2 (per-view answers, 26 rows): identity view vs L4 identity agree 23.08%, max dp 0.8932; reversed view vs L4 reversed agree 15.38%, max dp 0.9348; reconstruction valid PASS.
- A3 (per-view answers, 26 rows): identity view vs L4 identity agree 26.92%, max dp 0.8965; reversed view vs L4 reversed agree 11.54%, max dp 0.9347; reconstruction valid PASS.
- S1: not available (the arm returned only the 2view average (no per-view answers, no identity pass)).

## Token check (server identity-view tokens == local C1 count, P)

- A0: 40/40 equal, server missing 0, max abs diff 0
- A1: 40/40 equal, server missing 0, max abs diff 0
- A2: 40/40 equal, server missing 0, max abs diff 0
- A3: 40/40 equal, server missing 0, max abs diff 0
- S1: 40/40 equal, server missing 0, max abs diff 0

## Notes

- Latency is from this client's network position; server_ms excludes the network.
- Sustained = best S level with 0 failed calls; no call repeats inside a level; caches flushed between levels.
- A missing answer counts as a disagreement and as wrong; percentiles are nearest rank.
- Region multipliers are CLI inputs to be confirmed against Modal's billing page.
