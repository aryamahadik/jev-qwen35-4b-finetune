# JevBench v1.5.4, our run of the 231 public items (30 Sep 2026)

Unofficial: our own run on the public items, scored with the official v1.5 formulas. Not a leaderboard position.
It has no sealed half and no judge tier. The public items have been our development set, so our numbers are optimistic.

- Models: 4B-E (`q35_4b_pxE`) and 2B PRISM-X I pilot (`q35_2b_armI_1600`).
- Run on the Google L4 with no CUDA graphs and the slow causal_conv1d fallback.
- Checks passed: code, model and item hashes are identical to the Mac, and 231/231 prompts are identical.
- Jev comes from our own OpenRouter runs `jev_p1` and `jev_p2`.

| Run | Intelligence | Calib | Speed | Cost | Score A | Noul abstain |
|---|---|---|---|---|---|---|
| 4B-E, T=1 (as trained) | 62.5 | 84.3 | 88.6 | 58.3 | 71.03 | 33.8% |
| 4B-E, yes/no committed (T->0) | 78.7 | 83.4 | 88.6 | 58.3 | 75.27 | 0% |
| 2B-I pilot, T=1 | 39.9 | 81.8 | 87.8 | 58.3 | 38.62 | 56.8% |
| 2B-I pilot, yes/no committed | 70.3 | 78.1 | 87.8 | 58.3 | 71.96 | 0% |
| Jev p1 | 63.2 | 81.2 | 91.4 | 52.5 | 68.80 | 27.0% |
| Jev p2 | 62.3 | 79.7 | 90.6 | 52.5 | 68.14 | 28.4% |

Intelligence difference vs Jev p1 (paired bootstrap):

| Run | All 231 items | Half B (113 items) |
|---|---|---|
| 4B T=1 | -0.7 [-9.8, +9.3], tie | +3.9, tie |
| 4B committed | +15.5 [+5.2, +26.9], better | +19.9 [+4.2, +37.9], better |
| 2B committed | +7.1, tie | +15.8 [+3.8, +29.0], better |

## Why the scores move

v1.5 counts a Noul answer with 0.2 < P(yes) < 0.8 as an abstention, and scores it the same as a wrong answer
(METHOD-v1.5.md, section 3.1). Our models give soft yes/no probabilities, because they were trained on human vote
shares plus KD.

Committing (P(yes) -> 0 or 1 by argmax) can therefore never lower Intelligence; only Calibration can move. For the
4B, calibration stays above Jev's (83.4 vs 81.2), and at T=0.5 its Noul ECE even improves (0.095 -> 0.058).

## Caveats

- The commit rule is chosen from the method text, not fitted on these items. Any temperature must be fitted on dev
  (calibrate.py), never on JevBench.
- The sealed half, which is 50% of Intelligence, is unknown. The held-out lesson from v0.10 applies.

Files: bench/runs/v154_q35_4b_pxE, bench/runs/v154_q35_2b_armI_1600, bench/runs/v154_whatif/, bench/runs/scores_v154_all.json.

## 3 Oct 2026: C1 (q35_4b_main500k, the shipped 4B under A10) on the same 231 public items

Run on the Google L4: eager mode, no CUDA graphs. Scored with `bench/runs/scores_v154_c1.json`. The readout variants
are in `bench/runs/v154_whatif/`. The pre-registered JevBench readout is band edge (prep89/READOUT_DEV.md A5).

| Run | Intelligence | Calib | Speed | Cost | Score A | vs Jev p1 (Intelligence) |
|---|---|---|---|---|---|---|
| C1, as trained (T=1) | 61.5 | 83.6 | 88.4 | 58.3 | 70.56 | −1.7 [−9.7, +6.6], tie |
| C1, committed yes/no | 75.1 | 78.4 | 88.4 | 58.3 | 73.36 | +11.9 [+3.0, +21.3], better |
| **C1, band edge (pre-registered)** | **75.1** | **83.1** | 88.4 | 58.3 | **74.34** | **+11.9 [+3.0, +21.3], better** |
| 4B-E, band edge | 78.7 | 86.1 | 88.6 | 58.3 | 75.81 | +15.5 [+5.2, +26.9], better |
| Jev p1 | 63.2 | 81.2 | 91.4 | 52.5 | 68.80 | — |

C1 vs 4B-E on these items:
- Choice: C1 81.8 vs 80.6.
- Yes/no (committed): C1 65.2 vs 75.9; the hard tier is 47.4 vs 57.9.
- Score: C1 78.4 vs 79.5.

These public items were the development set for 4B-E's lineage, so 4B-E's row is optimistic.
