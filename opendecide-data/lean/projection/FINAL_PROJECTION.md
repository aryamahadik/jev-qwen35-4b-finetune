# OpenDecide vs Jev: final projection (30 Sep 2026, about 20:30 UTC)

**Short answer.**
- Accuracy against Jev is close to a coin flip, tilted slightly against us: the central gap is −0.3 pp and P(we score higher) is 0.45.
- Any loss is on yes/no. Multiple choice is probably fine.
- We almost certainly beat Jev on hijack. Injection is a tie. Cost wins on the JevBench formula. Speed wins only if we host properly.
- Calibration (Brier) and option-order drift are probably lost.
- The 2B will not match Jev. The cascade is worse than the 4B alone. **The headline system should be the 4B.**

**How I reconciled the three reviews.**

For P(final 4B ≥ Jev), the projection said 0.54, the pessimist 0.33 and the optimist 0.73.

I kept these corrections:
- **From the pessimist:** the winner's-curse fix (A), the discount for ddi2013 and for 40-option tasks (E), lower ship odds (C), and the Brier intercept (F).
- **From the optimist:** the projection's own reading of each task (A3), the tie rule for injection (A6), and the measured drift and hedging findings (B1, B2).

I kept the transfer ratio at 0.9. Both sides' alternatives rest on one disputed data point.

Net effect: −0.6 pp against the projection. The reconciled numbers are my estimates (EST), built by hand from the three Monte Carlo outputs with a normal approximation (sd about 2.65 pp). They are not a new simulation.

**Source codes:**
- e§ = `evidence.md` section, which cites the raw files.
- p§ = `projection.md` section.
- pes = `skeptic/`.
- opt = `optimist/`.

**Signs:** gaps are ours − Jev, in pp. Ranges are 80% ranges.

## (A) Main table

| Metric | Jev | 4B today (measured, test) | Final 4B projected | Final 2B | Cascade | P(best system beats or ties Jev) |
|---|---|---|---|---|---|---|
| Overall accuracy | OHS-1 81.65, OHS-2 81.55 (e§1) | 4B-E dev-confirm 81.49 (Jev never run on dev). Best held-out 4B: v11c OHS-2 79.92, −1.63 [−3.30, +0.11] | **−0.3 [−3.6, +3.2]** | −4.5 [−8, −1] | −0.7 [−4.0, +2.8] | 4B: **0.45** higher; 0.50 PREREG tie; 0.68 not significantly worse |
| Yes/no | OHS-1 83.97, OHS-2 95.83 (e§2) | v11c OHS-2 88.61, −7.22 [−10.56, −3.75]; 4B-E dev-confirm 85.77 | −1.8 [−9, +4.5] | −6 [−13, 0] | −2.3 | **0.33** (0.17-0.62) |
| Multiple choice | OHS-1 80.72, OHS-2 76.20 (e§3) | v11c OHS-2 +0.47 [−1.51, +2.40]; OHS-1 −3.45 | +0.9 [−2.2, +4.2] | −3.5 [−7, 0] | +0.6 | **0.65** |
| Consistency: complement violations | about 10.8% (OHS-1, e§5) | v11c OHS-1 11.31% (tie); 4B-E dev 4.81% | about 7.5% (−3 [−10, +4]) | about 3 pp worse | about a tie | 0.70 |
| Consistency: option-order drift | never measured (noise floor 1.4-2.4%, opt o1) | 4B-E dev 8.2% overall; 18.1% at 20+ options (opt o2) | 12-15% (opt o6) | worse | same as the 4B | **0.30** (0.2-0.45); both endpoints 0.22 |
| Hijack (jagged ASR) | 99.4% (e§6) | 4B-E 0.6% | 0.6-3% (ship cap 3%) | about 1% | 0.3-1.1% | **0.97** (0.7-0.9 against an adaptive attack, never run) |
| Prompt injection (OPI ASR) | 1.3% (e§7) | 4B-E 1.0%, −0.4 [−1.1, +0.1] (tie) | about 1% | 2-5% (pilot 4.4%, significantly worse) | 0.8-2.8% | 0.70 as a point win; 0.10 as a significant win |
| Speed, compute (GPU p50) | unknown (hosted only) | 4B-E on L4, no CUDA graphs: 110 ms. JevBench speed axis 88.6 vs 91.4, a loss (e§9) | 15-35 ms on H100 with graphs (EST, never measured) | 50-60 ms (cannot use graphs; L4 128 ms) | 60-75 ms | 0.65 (the JevBench axis needs under 59 ms) |
| Speed, end to end (same laptop) | 187-248 ms via OpenRouter (e§9) | v10 through a direct tunnel 114.6 ms; through the Modal web endpoint 410 ms | 100-160 ms tunnel; about 400 ms Modal endpoint (loses) | 125-160 ms | 140-180 ms | **0.75** with direct hosting; about 0.1 without |
| Cost, JevBench formula | $0.0384 / 1K (e§10) | $0.0245 / 1K | $0.0245 | $0.0245 | $0.031-0.042 (loses if routing > 57%) | **0.95** |
| Cost, real serving | billed $0.032 / 1K calls | never measured | $0.011-0.053 (EST, depends on GPU and use) | $0.055+ | $0.039+ | 0.35 |
| JevBench public, raw readout (Score A) | 68.80 (e§11) | 4B-E 71.03 (Intelligence 62.5 vs 63.2) | about 71 | pilot 38.6 | – | 0.75 |
| JevBench public, decisive readout (Score A) | 68.80 as returned; 70.66 with Jev also committed | 4B-E 75.27. Intelligence +5.1 [−4.4, +15.0] vs committed Jev (tie) | 75-76 | about 72 (pilot 71.96) | 72.5-73.3 | **0.88** (real leaderboard about 0.35; no submission) |
| Calibration (yes/no Brier, ours − Jev) | 0.1142 / 0.0379 (e§4) | v11c OHS-2 +0.045 [+0.029, +0.062]. JevBench Noul 0.070 vs 0.105 (a win) | +0.015 [−0.02, +0.055] | +0.035 | +0.017 | **0.18** (PREREG "matches") |

## (B) Final 4B by gain over 4B-E

The new 4B needs a dev-confirm gain over 4B-E of **+0.5 / +1.5 / +2.5**, which means a dev-confirm score of 81.99 / 82.99 / 83.99. If it fails the ship rule, 4B-E is kept.

Run status: step 3,750 of 30,457 at 167.1 min, 0 ALERT lines. About 20 H100-hours remain (`logs/main4b_seg1.log`).

| New 4B's gain over 4B-E | OHS-3 overall vs Jev | P(≥ Jev) | P(PREREG tie or better) |
|---|---|---|---|
| Fails, 4B-E kept | −0.9 [−4.2, +2.4] | 0.36 | 0.42 |
| +0.5 | −0.7 [−4.0, +2.6] | 0.39 | 0.45 |
| +1.5 | +0.2 [−3.1, +3.5] | 0.53 | 0.59 |
| +2.5 | +1.0 [−2.3, +4.3] | 0.65 | 0.70 |

The measured gain understates the true gain for two reasons:
- 4B-E's dev-confirm score is inflated by about +1.0 pp, because 4B-E was picked on that half (pes A).
- The new model starts from base and loses the tb_mixtral lineage (p§4).

## (C) Success odds (final 4B)

| Question | Reconciled | Range | Earlier projection |
|---|---|---|---|
| Owner success: accuracy tie within noise (PREREG) AND a win on hijack, injection, speed, cost and JevBench | **0.21** | 0.15-0.37 | 0.30 |
| Same, if "tie" means not significantly worse | 0.29 | – | 0.38 |
| Same, if injection only needs a tie | 0.30 / 0.40 | – | – |
| Every metric at once (without / with calibration) | **0.03 / 0.01** | 0.01-0.08 | 0.08 / 0.06 |
| Statistically clear accuracy win (95% CI above 0) | **0.24** | 0.14-0.50 | about 0.3 |
| Owner success with the 2B / the cascade | 0.02 / 0.06 | – | 0.03 / 0.12 |

How the owner-success figure is built: 0.50 × 0.97 × 0.70 × 0.75 × 0.95 × 0.88 = 0.21. The factors are, in order: accuracy tie, hijack, injection, speed, cost and JevBench.

## (D) The 3 biggest levers left

| Lever | What it is worth (EST) |
|---|---|
| **1. Direct hosting and a written speed/cost rule before OHS-3.** Time the 4B on an H100 with CUDA graphs through a direct tunnel. | Speed rises from 0.75 to about 0.9. The JevBench speed axis turns from a loss into a win (about +1 Score A). Owner success rises by 0.03-0.05. Cheap. |
| **2. The yes/no gap.** The new 4B passing the ship rule; the definitions cards. | Each +1 pp on OHS-3 yes/no adds +0.39 pp overall and improves Brier by about 0.005. A shipped +1.5 model lifts P(≥ Jev) from 0.36 to 0.53. The biggest driver is outside our control: whether openfda and nvd behave like hearsay moves P between 0.35 and 0.75 (p§12). |
| **3. Option-order drift.** Measure `_perm` on dev now (about 1 L4-hour per model). If drift stays at 12-15%, test a read that averages the normal and reversed option order. | Drift P rises from 0.30 to 0.5-0.6, and every-metric odds from 0.03 to about 0.05. The averaged read removes drift on the 149 reversed twins by construction. It doubles compute, its effect on accuracy is unknown, and it must be pre-registered. |

Two things must be done but will not change the odds:
- fix `score_ohs.py` so it matches PREREG_OHS3;
- stop presenting the cascade as a headline system.

## (E) Codex's odds vs ours

| Codex | Ours | Verdict |
|---|---|---|
| Tie or beat 45-50% | 0.50 (PREREG tie); 0.68 if tie means not significantly worse | Agree |
| Higher 40-45% | 0.45 (0.33-0.73) | Agree |
| At least 1 pt ahead, 25-30% | 0.31 | Agree (top end) |
| Clear win 20-25% | 0.24 | Agree |
| Security > 90% | Hijack 0.97. Injection 0.70 as a point win, 0.10 as a significant win | Agree for hijack only; injection is a tie |
| Better product 75-85% | 0.43 for everything except accuracy (hijack, injection, speed, cost, JevBench). 0.79 only if hosting is fixed and injection counts as a tie | **Disagree:** too high today. Drift and Brier are also likely losses |

Rules followed: read-only; no OHS-3 item text opened; no GPU, Modal or paid calls.
