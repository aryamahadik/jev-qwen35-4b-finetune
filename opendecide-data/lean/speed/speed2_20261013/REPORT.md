# SPEED-2 report: session `speed2_20261013`

Generated 2026-10-13T06:07:13Z by hosting/speed_bench.py. Dev rows only (gate dev splits). Workloads manifest sha256 `dc3fec5fa29eb99e`; calls P 8143, S 660, N 660, R 3305 (68 tasks).
Parity bars: argmax agreement >= 99.5%, |accuracy diff| <= 0.3 pt (1.0 pt for FP8 arms); gated against the baseline arm **A0** of this session; the stored L4 reads are context only.

## Arms

| arm | engine | GPU | region | boot s | flags |
|---|---|---|---|---|---|
| A0 | hf | NVIDIA H100 80GB HBM3 | us-east | 1119.7 | `{"legacy": true, "choice_views": 2}` |
| A1 | hf | NVIDIA H100 80GB HBM3 | us-east | 1119.7 | `{"legacy": false, "twoview_split": true, "graph_plan": "speed1", "tokenize_outside_lock": true, "cross_batch": false, "choice_views": 2}` |
| A2 | hf | NVIDIA H100 80GB HBM3 | us-east | 1119.7 | `{"legacy": false, "twoview_split": true, "graph_plan": "speed1", "tokenize_outside_lock": true, "cross_batch": true, "batch_wait_ms": 0, "choice_views": 2}` |
| S1 | sglang | NVIDIA H100 80GB HBM3, 81559 MiB | eu-north | 175.7 | `{}` |
| S2 | sglang | NVIDIA H100 80GB HBM3, 81559 MiB | eu-south | 152.3 | `{}` |

- Arms ran in different regions: compare latency on server_ms (client and network ms include each region's network path).

## Latency, S at concurrency 1 (ms, client = laptop round trip)

| arm | client p50 | p95 | p99 | server p50 | server p95 | network p50 | failed |
|---|---|---|---|---|---|---|---|
| A0 | 99.4 | 217.4 | 227.5 | 48.8 | 165.8 | 49.2 | 0 |
| A1 | 101.1 | 216.3 | 224.0 | 53.1 | 165.0 | 47.8 | 0 |
| A2 | 97.0 | 216.3 | 226.3 | 48.7 | 165.0 | 47.9 | 0 |
| S1 | 177.5 | 229.9 | 242.5 | 45.3 | 97.8 | 131.6 | 0 |
| S2 | 158.6 | 203.1 | 214.2 | 35.3 | 78.4 | 122.7 | 0 |
| Jev (OpenRouter) | 209.7 | 319.3 | 381.8 | - | - | - | 0 |

## Throughput, S closed loop (decisions/hour; failed calls in brackets)

| arm | c=1 | c=2 | c=4 | c=8 | c=16 | sustained | at c |
|---|---|---|---|---|---|---|---|
| A0 | 31,740 | 50,641 | 59,016 | 59,173 | 59,244 | 59,244 | 16 |
| A1 | 32,280 | 51,345 | 60,349 | 60,824 | 60,808 | 60,824 | 8 |
| A2 | 32,820 | 51,886 | 61,709 | 63,338 | 63,888 | 63,888 | 16 |
| S1 | 19,320 | 31,200 | 57,826 | 85,177 | 124,305 | 124,305 | 16 |
| S2 | 21,660 | 37,804 | 64,883 | 100,452 | 151,058 [1] | 100,452 | 8 |

## Cost, $ per 1,000 decisions (rate $3.95/h x region multiplier {"any": 1.0, "us-east": 1.75}, multipliers to be confirmed; / utilisation)

| arm | any @ 100% | any @ 40% | us-east @ 100% | us-east @ 40% |
|---|---|---|---|---|
| A0 | 0.0667 | 0.1667 | 0.1167 | 0.2917 |
| A1 | 0.0649 | 0.1624 | 0.1136 | 0.2841 |
| A2 | 0.0618 | 0.1546 | 0.1082 | 0.2705 |
| S1 | 0.0318 | 0.0794 | 0.0556 | 0.1390 |
| S2 | 0.0393 | 0.0983 | 0.0688 | 0.1720 |

## Other workloads

| arm | P pass c=16 decisions/h | P pass s | N c=1 p50 / p99 ms | R c=1 p50 ms | R c=8 decisions/h | R c=8 cached-token share | batch rows mean (S c=16) |
|---|---|---|---|---|---|---|---|
| A0 | 125,866 | 232.9 | 68.5 / 209.5 | 69.2 | 123,720 | - | 1.59 |
| A1 | 119,409 | 245.5 | 75.5 / 212.4 | 75.2 | 115,020 | - | 1.00 |
| A2 | 147,936 | 198.2 | 74.3 / 214.0 | 68.4 | 141,360 | - | 2.78 |
| S1 | 167,661 | 174.8 | 178.1 / 235.9 | 173.5 | 129,120 | 57.5% | 1.59 |
| S2 | 210,217 | 139.4 | 159.1 / 206.7 | 154.7 | 143,280 | 57.3% | 1.59 |

## Parity, gated vs A0 (same session)

| arm | set | rows | argmax agree | acc arm | acc base | diff pt | bar pt | mean / p99 / max abs dp | result |
|---|---|---|---|---|---|---|---|---|---|
| A0 | **gate** | | | | | | | | **BASELINE** |
| A1 | P | 8143 | 100.00% | 81.44 | 81.44 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| A1 | R (rows both answered) | 2079 | 100.00% | 81.87 | 81.87 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| A1 | **gate** | | | | | | | | **PASS** |
| A2 | P | 8143 | 100.00% | 81.44 | 81.44 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| A2 | R (rows both answered) | 2238 | 100.00% | 81.64 | 81.64 | 0.00 | 0.3 | 0.0000 / 0.0000 / 0.0000 | PASS |
| A2 | **gate** | | | | | | | | **PASS** |
| S1 | P | 8143 | 99.77% | 81.48 | 81.44 | 0.04 | 0.3 | 0.0017 / 0.0120 / 0.0452 | PASS |
| S1 | R (rows both answered) | 2238 | 99.91% | 81.64 | 81.64 | 0.00 | 0.3 | 0.0015 / 0.0095 / 0.0177 | PASS |
| S1 | **gate** | | | | | | | | **PASS** |
| S2 | P | 8143 | 98.64% | 81.49 | 81.44 | 0.05 | 1.0 | 0.0108 / 0.0807 / 0.3919 | FAIL |
| S2 | R (rows both answered) | 2238 | 98.97% | 81.41 | 81.64 | -0.22 | 1.0 | 0.0102 / 0.0672 / 0.1513 | FAIL |
| S2 | **gate** | | | | | | | | **FAIL** |

### By type and options bucket (P vs baseline: argmax agree / diff pt / max abs dp)

- A1: noul n=4329 100.00% / 0.00 / 0.0000; 2-4 n=2527 100.00% / 0.00 / 0.0000; 5-9 n=900 100.00% / 0.00 / 0.0000; 10-25 n=153 100.00% / 0.00 / 0.0000; 26+ n=234 100.00% / 0.00 / 0.0000
- A2: noul n=4329 100.00% / 0.00 / 0.0000; 2-4 n=2527 100.00% / 0.00 / 0.0000; 5-9 n=900 100.00% / 0.00 / 0.0000; 10-25 n=153 100.00% / 0.00 / 0.0000; 26+ n=234 100.00% / 0.00 / 0.0000
- S1: noul n=4329 99.84% / -0.02 / 0.0433; 2-4 n=2527 99.68% / 0.08 / 0.0389; 5-9 n=900 99.67% / 0.11 / 0.0452; 10-25 n=153 99.35% / 0.65 / 0.0164; 26+ n=234 100.00% / 0.00 / 0.0102
- S2: noul n=4329 98.89% / -0.05 / 0.3006; 2-4 n=2527 98.34% / 0.16 / 0.3919; 5-9 n=900 98.78% / 0.44 / 0.3394; 10-25 n=153 98.69% / 0.00 / 0.0656; 26+ n=234 96.58% / -0.85 / 0.0827

## Parity vs the stored L4 reads (context, not gated; 2view served read)

| arm | rows | argmax agree | acc arm | acc L4 | diff pt | mean / p99 / max abs dp | bars |
|---|---|---|---|---|---|---|---|
| A0 | 8143 | 99.84% | 81.44 | 81.46 | -0.01 | 0.0016 / 0.0120 / 0.0918 | PASS |
| A1 | 8143 | 99.84% | 81.44 | 81.46 | -0.01 | 0.0016 / 0.0120 / 0.0918 | PASS |
| A2 | 8143 | 99.84% | 81.44 | 81.46 | -0.01 | 0.0016 / 0.0120 / 0.0918 | PASS |
| S1 | 8143 | 99.73% | 81.48 | 81.46 | 0.03 | 0.0017 / 0.0135 / 0.1013 | PASS |
| S2 | 8143 | 98.70% | 81.49 | 81.46 | 0.04 | 0.0108 / 0.0816 / 0.3604 | FAIL |

## Reversed-view check

Stored L4 reads: reversed view = 2 x served - identity on 3814 choice rows; invalid rows 0, max violation 2e-07 -> PASS.

- A0 (per-view answers, 3814 rows): identity view vs L4 identity agree 99.74%, max dp 0.0517; reversed view vs L4 reversed agree 99.74%, max dp 0.1117; reconstruction valid PASS.
- A1 (per-view answers, 3814 rows): identity view vs L4 identity agree 99.74%, max dp 0.0517; reversed view vs L4 reversed agree 99.74%, max dp 0.1117; reconstruction valid PASS.
- A2 (per-view answers, 3814 rows): identity view vs L4 identity agree 99.74%, max dp 0.0517; reversed view vs L4 reversed agree 99.74%, max dp 0.1117; reconstruction valid PASS.
- S1: not available (the arm returned only the 2view average (no per-view answers, no identity pass)).
- S2: not available (the arm returned only the 2view average (no per-view answers, no identity pass)).

## Token check (server identity-view tokens == local C1 count, P)

- A0: 8143/8143 equal, server missing 0, max abs diff 0
- A1: 8143/8143 equal, server missing 0, max abs diff 0
- A2: 8143/8143 equal, server missing 0, max abs diff 0
- S1: 8143/8143 equal, server missing 0, max abs diff 0
- S2: 8143/8143 equal, server missing 0, max abs diff 0

## Jev (report-only, dev S rows, concurrency 1; never used for training)

Route openrouter (httpx, no SDK), model jev-1.13; 660 calls, 0 errors, yes/no cards dropped 0.
Accuracy on S: Jev 71.36 vs stored C1 L4 68.18 (argmax agreement with C1 77.88%).
Same rows, A0 answers: accuracy 68.18.

## Notes

- Latency is from this client's network position; server_ms excludes the network.
- Sustained = best S level with 0 failed calls; no call repeats inside a level; caches flushed between levels.
- A missing answer counts as a disagreement and as wrong; percentiles are nearest rank. A gate with P rows unanswered by the arm or the baseline reads INCOMPLETE (FAIL if the rows both answered fail a bar).
- Region multipliers are CLI inputs to be confirmed against Modal's billing page.
