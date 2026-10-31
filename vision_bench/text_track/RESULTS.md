# Text track: C1 vs base Qwen3.5-4B vs Jev 1.14 / 1.13 (published)

**C1 System One Index 77.6** (SE 0.7) | base Qwen3.5-4B 73.0 | Jev 1.14 79.3 | Jev 1.13 79.0.

**C1 vs Jev 1.14: gap -1.65 points, SE 1.00, z -1.65 -> no difference demonstrated (gap under 3 Index points or z under 2).** (Rule: a win or loss is called only if the gap is at least 3 points AND |z| >= 2.)

C1 vs Jev 1.13: gap -1.37, SE 1.00, z -1.37 -> no difference demonstrated (gap under 3 Index points or z under 2).

Calibration (top-label ECE over all 4850 decisions): C1 3.3% | base 8.1% | Jev 1.14 6.0% | Jev 1.13 6.1%.

Failed decisions: C1 0, base 0 (of 4850); Jev 0.

## Accuracy per suite (%)

n = decisions (typed-decisions: 400 cases x 5 questions). Jev columns are the bench's published runs. Standard error of one suite is 1.7 to 3.5 points (about 1.0 for typed-decisions if its 2,000 decisions were independent; 2.2 if only its 400 cases count).

| Suite | n | C1 | Base Qwen3.5-4B | Jev 1.14 (pub.) | Jev 1.13 (pub.) | C1 - Jev 1.14 (z) |
|---|---:|---:|---:|---:|---:|---:|
| AG News (4) | 200 | 89.0 | 87.5 | 89.0 | 88.5 | +0.0 (+0.0) |
| SST-2 (yes/no) | 200 | 92.0 | 85.5 | 95.0 | 94.5 | -3.0 (-1.2) |
| SST-5 (score 5) | 200 | 51.0 | 52.0 | 60.0 | 62.0 | -9.0 (-1.8) |
| DAIR Emotion (6) | 200 | 56.0 | 55.5 | 57.5 | 56.0 | -1.5 (-0.3) |
| Banking77 (77) | 200 | 79.5 | 70.0 | 78.5 | 79.0 | +1.0 (+0.2) |
| BoolQ (yes/no) | 200 | 87.5 | 86.0 | 90.0 | 89.5 | -2.5 (-0.8) |
| XNLI English (3) | 150 | 86.7 | 84.0 | 86.0 | 86.0 | +0.7 (+0.2) |
| Typed decisions (5 q/case) | 2000 | 68.9 | 66.2 | 74.2 | 72.7 | -5.3 (-1.6) |
| XNLI French (3) | 150 | 76.7 | 73.3 | 76.7 | 76.7 | +0.0 (+0.0) |
| XNLI Arabic (3) | 150 | 68.0 | 62.0 | 71.3 | 69.3 | -3.3 (-0.6) |
| MASSIVE-ar scenario (18) | 200 | 66.0 | 61.0 | 65.0 | 63.0 | +1.0 (+0.2) |
| MASSIVE-ar intent (20) | 200 | 83.5 | 71.0 | 85.0 | 84.0 | -1.5 (-0.4) |
| OSACT4 offensive (yes/no) | 200 | 89.0 | 73.5 | 87.0 | 90.0 | +2.0 (+0.6) |
| Arabic tweet sentiment (3) | 200 | 72.5 | 74.0 | 76.0 | 76.0 | -3.5 (-0.8) |
| MIRACL-ar rerank (1 of 8) | 200 | 85.5 | 84.5 | 87.5 | 86.5 | -2.0 (-0.6) |
| MIRACL-ar pairwise (yes/no) | 200 | 90.5 | 82.5 | 90.0 | 90.5 | +0.5 (+0.2) |
| **System One Index (16 suites)** | 4850 | **77.6** | 73.0 | 79.3 | 79.0 | -1.6 (-1.6) |
| English index (8 suites) | | 76.3 | 73.3 | 78.8 | 78.5 | -2.5 (-1.8) |
| Arabic index (7 suites) | | 79.3 | 72.6 | 80.3 | 79.9 | -1.0 (-0.6) |
| Index SE (points) | | 0.71 | 0.77 | 0.70 | 0.70 | gap SE 1.00 |
| Index, failed = wrong (strict) | | 77.6 | 73.0 | | | |

## Calibration (ECE %, 10 bins, top label)

| Suite | C1 | Base | Jev 1.14 | Jev 1.13 |
|---|---:|---:|---:|---:|
| AG News (4) | 3.3 | 9.5 | 6.9 | 8.6 |
| SST-2 (yes/no) | 3.5 | 8.5 | 7.7 | 6.4 |
| SST-5 (score 5) | 12.7 | 10.2 | 18.1 | 16.1 |
| DAIR Emotion (6) | 17.6 | 24.7 | 27.0 | 30.4 |
| Banking77 (77) | 6.0 | 5.2 | 10.4 | 10.1 |
| BoolQ (yes/no) | 4.9 | 4.2 | 2.7 | 3.9 |
| XNLI English (3) | 5.9 | 4.3 | 7.0 | 8.2 |
| Typed decisions (5 q/case) | 1.6 | 7.4 | 5.0 | 4.0 |
| XNLI French (3) | 4.9 | 10.1 | 10.7 | 12.2 |
| XNLI Arabic (3) | 10.9 | 20.4 | 11.3 | 14.0 |
| MASSIVE-ar scenario (18) | 10.2 | 18.6 | 16.3 | 21.0 |
| MASSIVE-ar intent (20) | 6.0 | 9.1 | 2.8 | 3.5 |
| OSACT4 offensive (yes/no) | 6.0 | 14.7 | 4.8 | 5.5 |
| Arabic tweet sentiment (3) | 6.1 | 12.9 | 9.5 | 9.7 |
| MIRACL-ar rerank (1 of 8) | 6.1 | 9.4 | 6.6 | 6.1 |
| MIRACL-ar pairwise (yes/no) | 4.2 | 11.8 | 2.1 | 2.7 |
| **All 4850 decisions** | **3.3** | 8.1 | 6.0 | 6.1 |

Sampling noise (bootstrap over the 3,250 cases, 2,000 resamples): C1 ECE 3.3% (95% interval 2.3 to 4.5), base 8.1% (7.1 to 9.5); C1 Index bootstrap SE 0.70 (interval 76.3 to 79.1), which agrees with the analytic SE 0.71 used above. Jev's per-item results are not published, so its numbers carry no interval here.

## Latency (NOT COMPARABLE)

NOT COMPARABLE. Jev: median / 95th percentile per API call over all 3,250 cases, 8 calls in flight, from a cloud server near OpenRouter, so it includes the network and JSON encoding. C1/base here: HF transformers bf16 on one Modal H100, no network, batch 1, one call = all questions of one case read as one batch (prompt rendering + tokenization + forward), 320 sampled cases (20 per suite), LoRA unmerged, no CUDA graphs, not SGLang. Different machine, protocol and sample: do not compare these numbers.

| | median per call | 95th percentile | calls |
|---|---:|---:|---:|
| Jev 1.14 (published, cloud + network, 8 in flight) | 136 ms | 175 ms | 3250 |
| Jev 1.13 (published) | 150 ms | 216 ms | 3250 |
| C1 (H100, HF bf16, batch 1, no network) | 81 ms | 218 ms | 320 |
| Base Qwen3.5-4B (same) | 57 ms | 133 ms | 320 |

C1 split: forward p50 79 ms, prompt rendering + tokenization p50 2 ms. The batch-1 answers agree with the batched pass (same argmax on 318/320 calls; largest probability difference 0.015).

## Cost

**Modal bill for this task: $0.95** (profile mahadikarya44; `modal billing report`): GPU run $0.94 (one H100, function time 728 s, plus container start and stop; the rate-card estimate from function time alone was $0.87) + CPU-only preflight $0.008. Cap was $2.00. No budget stop was needed (False); the app was stopped afterwards and no Modal app is running.

## Labelled diagnostics (not the headline)

- C1, score options (1000 items: SST-5 + typed-decisions score questions): with C1's `<i>: ` prefix (headline) 60.4% | bare criteria strings as Jev receives them 60.6%.
- C1, yes/no letters (1400 items): A = Yes (headline) 84.9% | A = No 84.6% | both orders averaged 84.9%.
- C1, Index variants (strict): {'headline_strict': 77.64, 'score_options_bare': 77.56, 'yes_no_both_orders_averaged': 77.61}
- Base, score options (1000 items: SST-5 + typed-decisions score questions): with C1's `<i>: ` prefix (headline) 56.5% | bare criteria strings as Jev receives them 55.2%.
- Base, yes/no letters (1400 items): A = Yes (headline) 78.8% | A = No 77.1% | both orders averaged 78.4%.
- Base, Index variants (strict): {'headline_strict': 73.04, 'score_options_bare': 72.71, 'yes_no_both_orders_averaged': 73.07}

## Skeptic re-score

`harness/skeptic_rescore.py` recomputed every number above from the raw per-view logits of the saved per-item logs (independent code, numpy only): **ALL CHECKS MATCH**. Details in `results/skeptic.txt`.

- c1: Index 77.64, English 76.32, Arabic 79.29, ECE 3.34%, SE 0.71, vs Jev 1.14 gap -1.65 (z -1.65) -> no difference demonstrated
- base: Index 73.04, English 73.34, Arabic 72.64, ECE 8.06%, SE 0.77, vs Jev 1.14 gap -6.25 (z -6.01) -> behind
