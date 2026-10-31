# Readout settings on dev (goal step 8, A5), 1 Oct 2026

**Scope.** Dev only, CPU only. Two models are covered so the settings are ready whichever one ships:
- **4B-E**, `q35_4b_pxE_fresh`. This ships by default, because the 4B gate said DO NOT SHIP for the main run.
  - **Update (2 Oct):** the shipped 4B is now TBD by gate job 3 (`prereg_drafts/A8prime.md`): 4B-E, or the top-up
    C4 = `q35_4b_main500k_fix2` if it passes. The same T rule is applied to whichever ships with
    `prep89/t_rule_check.py`, which reproduces this file's 1.00 / 1.00 for both models below.
- **4B-main**, `q35_4b_main500k`.

Inputs are the stored fresh reads (standard read and `_perm` read) on the 9 gate splits: 8,143 rows, 4,329 yes/no and
3,814 choice. The dev halves come from `gate_dev.half`.

**What was not done:**
- no OHS file was opened;
- nothing was fitted on OHS-1/2/3;
- no Modal, gcloud, ssh or paid call was made;
- no tracked file was edited (`git status` shows the same 7 modified files as at the start).

One early listing loop over `data/*_relations.jsonl` named the `ohs*_relations.jsonl` files. It failed on a wrong
interpreter path before reading anything.

**Files** (all new, in `lean/prep89/`):
- `readout_dev.py`, the analysis. It imports `gate_dev.py` and `bench/v154/v154lib.py` read-only, so the accuracy,
  flip and ECE definitions are exactly the gate's and JevBench v1.5's.
- `readout_dev.txt`, the full printout.
- `readout_dev.json`, every number.

**Checks that passed:**
- Gate (f): 2.43% vs 3.78%. Gate (e): 8.86% vs 5.68%. Both reproduce `look_ship1.txt`.
- The gate's dev-select T values reproduce (4B-main / 4B-E, without tb_mixtral): yes/no 0.95 / 0.95, and choice
  1.05 / 1.00.
- The drift numbers reproduce: 7.37% single, 3.72% 2-view.
- `q35_4b_pxE_parity` is bit-identical to `q35_4b_pxE_fresh`.

## Short answers

1. **Temperatures:** ship **T = 1.00 for yes/no and 1.00 for choice**, for both models and both readouts.
   - The dev-select fits are 0.90 / 1.00 (4B-E) and 0.95 / 1.05 (4B-main).
   - None of them improves dev-confirm enough to meet A5 item 4's bar.
2. **Read twice (2-view)** halves choice option-order flips and leaves accuracy unchanged.
   - It slightly hurts yes/no accuracy.
   - **It does not reduce the (e) equivalence (double-negation) flips:** 4B-main goes from 8.86% to 9.14%.
   - Gate (e) fails under every readout. No readout setting can rescue the main run: T cannot change an argmax, band
     edge keeps the argmax, and 2-view does not help.
3. **Band edge** worsens dev yes/no calibration: Brier +0.004 to +0.006, and the ECE gets worse.
   - Under JevBench v1.5's scoring rule, applied to dev-confirm, it lifts committed yes/no accuracy a lot: 62.5 → 85.8
     (4B-E).
   - Use it on JevBench only, disclosed, and never on OHS-3.
4. **A5 recommendation** (details at the end):
   - choice rows: 2-view (given order + exact reversal);
   - yes/no rows: single read;
   - T = 1.00 / 1.00;
   - the single read is also reported as a secondary configuration;
   - JevBench: 1 read + band edge.
   - PREREG_OHS3 rule 4 must be amended, because "plain readout" is no longer the primary.
5. **Side finding for the top-up.** The main run's (e) failure comes from one source.
   - `devp_card/hate` has 32 of 60 equivalence pairs flipped, vs 2 of 60 for 4B-E.
   - Without hate it is 4.83% vs 5.89%.

## Caveat: what "2-view" means here

- **The `_perm` read (perm-seed 1) is one seeded random view per row. It is not the reversed order.**
  - On choice rows, 3,098 of 3,814 rows got a non-identity order. The other 716 are identical to the standard read, so
    on them the 2-view equals the 1-view.
  - On yes/no rows, the Yes/No letters were swapped on 2,138 of 4,329 rows. On the other 2,191 rows the 2-view equals
    the 1-view.
  - Checked: the `_perm` read equals the standard read on exactly the identity-view rows.
- **4B-E also has the exact A5 (a) read:** `q35_4b_pxE_tta`.
  - This is the legacy `--tta` read: identity + reversed on choice rows, identity + swapped letters on yes/no rows.
  - It matches the `_perm` read on the 2,791 rows where the seeded view *is* the reversal or swap: mean |2·tta −
    identity − perm| = 0.0011, max 0.075.
  - So the **4B-E numbers for "2v_rev" are the real A5 (a) readout**. For 4B-main only the random view exists, so
    its 2-view numbers are a **proxy**: "2v_perm".
- In all averages, the views are averaged in probability space, as `decoder_io.predict` does.

## (2) Read twice: accuracy

Accuracy uses the gate's scoring (ties count as wrong). Each difference vs the 1-view comes with a paired bootstrap
over group_id units (10,000 resamples, seed 0).

| Model | Readout | All rows | Yes/no | Choice | Diff vs 1-view: yes/no | Diff vs 1-view: choice (sel / conf) |
|---|---|---|---|---|---|---|
| 4B-E | 1-view | 80.72 | 84.52 | 76.40 | – | – |
| 4B-E | 2-view, exact (identity + reversed / swapped) | 80.62 | 84.25 | 76.51 | −0.28 [−0.60, +0.05] | +0.10 [−0.48, +0.69] (−0.05 / +0.27) |
| 4B-E | **A5 (a): choice 2-view, yes/no 1-view** | **80.77** | 84.52 | 76.51 | 0 | +0.10 (as above) |
| 4B-main | 1-view | 81.42 | 85.19 | 77.14 | – | – |
| 4B-main | 2-view, proxy (identity + perm1) | 81.43 | 85.01 | 77.37 | **−0.18 [−0.33, −0.05]** | +0.24 [−0.24, +0.70] (+0.47 / 0.00) |
| 4B-main | A5 (a), proxy | 81.53 | 85.19 | 77.37 | 0 | +0.24 (as above) |

- Yes/no rows that really were read twice (the 2,138 with swapped letters):
  - 4B-main: −0.37 [−0.68, −0.09];
  - 4B-E: −0.23 [−0.71, +0.24].
- So reading yes/no twice costs a little accuracy for both models. This matches X19.
- Reading choice rows twice neither helps nor hurts accuracy on dev.

## (2) Read twice: permutation flips

A flip is a row whose answer changes between two displayed orders.

**1-view (gate (f), the standard read vs `_perm`):**

| Model | All rows | Yes/no | Choice | Choice, 10+ options |
|---|---|---|---|---|
| 4B-E | 3.78% | 1.18% | 6.74% | 17.3% |
| 4B-main | 2.43% | 0.53% | 4.59% | 10.9% |

**2-view, 4B-E choice rows (n = 3,814; 10+ options n = 387).** Two *independent* 2-view reads exist here: (identity +
perm1) and (rotated + reversed rotated, from `drift/out`).

| Pair of reads | Flips | Flips at 10+ options |
|---|---|---|
| 1-view identity vs 1-view rotated | 7.37% | 16.8% |
| 2-view (identity + perm1) vs 2-view (rotated + reversed rotated) | 4.48% | 12.4% |
| **2-view (identity + reversed) vs 2-view (rotated + reversed rotated)** | **3.72%** | **9.8%** |

- **Yes/no:** a 2-view read already uses both letter orders, so there is nothing left to flip. It is 0 by
  construction.
- **4B-main:** its 2-view choice flip rate **cannot be measured**, because that needs at least 3 views and only 2
  exist.
  - Its 1-view choice flip rate is 0.68 times 4B-E's (4.59 / 6.74).
  - An *extrapolation* (not a measurement) puts its 2-view at about 2.3-3.0%.
- **OHS-3 mix (4B-E, from `drift/RESULT_30sep.md`):** 7.79% single read → 1.90% with the 2-view.
  - Jev's floor is its run-to-run disagreement of 1.14-1.98%.
  - On the 149 reversed twins, the 2-view's drift is 0 by construction.

## (2) Read twice: equivalence (e), complement and inv pairs

**What the pairs are:**
- **Equivalence pairs:** all 722 are yes/no. Each pairs an affirmative question with its double negation ("Should the
  statement that … is not … be rejected?"), in devzs, devp_card and dev.
- **Complement pairs:** 1,122 yes/no pairs, where the answer should flip.
- **inv pairs:** 500 in dev_claims.

| Model | Readout | Equiv flips (gate (e)) | Equiv flips, the 171 pairs fully read twice | Complement violations | inv flips |
|---|---|---|---|---|---|
| 4B-E | 1-view | 5.68% | 5.26% | 4.63% | 1.80% |
| 4B-E | 2-view, exact (letter swap on every row) | 5.82% (+0.14 [−0.83, +1.11]) | 4.68% (−0.58 [−2.92, +1.17]) | 4.90% (+0.27 [−0.54, +1.07]) | 2.60% |
| 4B-main | 1-view | **8.86%** | 7.02% | 3.30% | 1.80% |
| 4B-main | 2-view, proxy | **9.14%** (+0.28 [−0.28, +0.83]) | 8.19% (+1.17 [−1.17, +3.51]) | 3.30% (0.00) | 1.60% |

**Gate (e) re-read under each readout** (4B-main vs 4B-E; the bar is REF + 2 pp):

| Readout | 4B-main | 4B-E | Result |
|---|---|---|---|
| 1-view | 8.86% | 5.68% | FAIL |
| 2-view for both, perm1 | 9.14% | 5.96% | FAIL |
| 4B-main 2-view proxy vs 4B-E exact 2-view | 9.14% | 5.82% | FAIL |

**Answer: no. Averaging two views does not reduce the (e) flips.** The flips are not caused by the order of the
letters.

**Anatomy of the (e) gap** (1-view; `readout_dev.txt`, section 2c):
- 4B-main's flipped pairs are split evenly between the affirmative row being wrong (30) and the double-negated row
  being wrong (34). Its double-negation accuracy is *higher* than 4B-E's: 84.35 vs 82.96.
- The gap is one source:
  - `devp_card/hate`: **32 of 60** pairs flip for 4B-main, 2 of 60 for 4B-E.
  - Every other source: 32 of 662 (4.83%) for 4B-main, 39 of 662 (5.89%) for 4B-E.
- This points a fixed top-up at hate-card consistency. "hate" is a seen source, and §10 of PREREG_FINAL already lists
  it as an open point.
- **Caveat (review, 1 Oct).** This diagnosis was read off the gate's own (e) pairs. A top-up aimed at `devp_card/hate`
  and then judged by a new look at the same 722 pairs is tuned on its test. Pre-register the top-up's look before
  training it, and either judge (e) on pairs not used for this diagnosis or disclose that the fix was targeted.
  - **Addressed in `prereg_drafts/A8prime.md` (section C):** the top-up never contains dev wording, dev sources or the
    hate family; C4 must also pass (e) on the 662 non-hate pairs (no worse than C1 + 1 pp, so at most 5.83%) and a
    held-out F7 probe and blind devx pre-check before its one ship look; and a dev (e) pass is disclosed as weak
    evidence, with OHS-3 (sealed) as the real test.

## (1) Temperature per question type

**Method:**
- NLL fit on pooled dev-select (9 splits);
- A5 grid 0.50-2.00, step 0.05. The gate grid 0.25-10 gives the same values.
- Evaluated on dev-confirm. Accuracy is unchanged in every case, as it must be.
- ECE uses JevBench v1.5's `ece_bins` (10 bins): P(yes) on yes/no rows, top-label confidence on choice rows.

| Model / readout | Type | T fitted on select (without tb_mixtral; confirm fit, for information only) | Dev-confirm, T=1 → fitted T | A5 item 4 rule → shipped T |
|---|---|---|---|---|
| 4B-E / 1-view | yes/no | 0.90 (0.95; 0.85) | Brier 0.1084 → 0.1078; ECE 0.037 → 0.028; NLL 0.354 → 0.350 | gain 0.0006 < 0.002 → **1.00** |
| 4B-E / 1-view | choice | 1.00 (1.00; 0.95) | no change: NLL 0.623, top ECE 0.037 | **1.00** |
| 4B-E / A5 (a) exact | choice | 1.00 (0.95; 0.90) | no change: NLL 0.614, top ECE 0.041 | **1.00** |
| 4B-main / 1-view | yes/no | 0.95 (0.95; 0.95) | Brier 0.1080 → 0.1082 (worse); ECE 0.032 → 0.022 | gain −0.0002 → **1.00** |
| 4B-main / 1-view | choice | 1.05 (1.05; 1.00) | NLL 0.6093 → 0.6104 (worse); top ECE 0.035 → 0.031 | **1.00** (proposed choice rule below) |
| 4B-main / A5 (a) proxy | choice | 1.05 (1.00; 1.00) | NLL 0.6025 → 0.6041 (worse) | **1.00** |

- The worst single-split change in yes/no Brier under the fitted T is +0.0008 (4B-E) and +0.0017 (4B-main). Both are
  under the 0.003 limit, but the pooled gain fails the bar.
- The fitted T moves between 0.85 and 0.95 depending on the half and on whether tb_mixtral is in. The models are
  already close to calibrated, and T = 1 is the stable choice.
- **A5 item 4 needs a rule for choice rows.** The draft names only the yes/no Brier.
  - Proposed [OWNER]: choice T ≠ 1 only if pooled dev-confirm choice NLL improves by ≥ 0.002 nats per row and no
    split's choice NLL worsens by more than 0.005.
  - No model qualifies under this rule.

## (3) Band-edge yes/no readout (1 read, dev)

- **The rule:** P(yes) in (0.5, 0.8) → 0.8; P(yes) in (0.2, 0.5] → 0.2; applied after T.
- **v1.5 scoring:** P ≥ 0.8 is yes, P ≤ 0.2 is no, and anything between is an abstention counted wrong.
- **Calibration score:** 100·(1 − ECE/0.5).
- All rows below use T = 1, the recommended setting.

| Model, half | Readout | Brier | ECE (v1.5 noul calibration score) | v1.5 abstentions | v1.5 committed accuracy |
|---|---|---|---|---|---|
| 4B-E, confirm | as returned | 0.1084 | 0.037 (92.6) | 33.2% | 62.45 |
| 4B-E, confirm | full commit (0/1) | 0.1423 | 0.142 (71.5) | 0% | 85.77 |
| 4B-E, confirm | **band edge** | **0.1120** | 0.039 (**92.2**) | 0% | **85.77** |
| 4B-E, pooled | as returned → band edge | 0.1144 → 0.1205 | 0.030 → 0.047 (94.0 → 90.5) | 34.4% → 0% | 60.91 → 84.52 |
| 4B-main, confirm | as returned → band edge | 0.1080 → 0.1140 | 0.032 → 0.059 (93.5 → 88.2) | 23.7% → 0% | 69.63 → 85.49 |
| 4B-main, pooled | as returned → band edge | 0.1096 → 0.1157 | 0.028 → 0.058 (94.4 → 88.5) | 26.3% → 0% | 67.59 → 85.19 |

**What this means:**
- The band edge moves the 24-34% of yes/no rows in the band. Their argmax is right 67-70% of the time, and v1.5
  scores them 0 when they stay in the band.
- **On dev the band edge costs calibration:** Brier gets worse by 0.004-0.006, and the noul calibration score falls
  by 0.4 (4B-E confirm) to 5 points.
- So the dev data **does not reproduce** the JevBench public-item calibration gain (84.3 → 86.1, an all-type axis on
  231 items, including half B). Only the committed-accuracy gain reproduces.
- This is the dev ECE/Brier check that `board.md` §8 asks for. It supports keeping the band edge on JevBench only, as
  a disclosed scorer-aware readout, and **never on OHS-3**, whose Brier is a primary endpoint.

## (4) Recommended A5 settings for OHS-3 (fill into the A5 block; the owner decides)

| Setting | 4B-E (default ship) | 4B-main (only if the owner overrides) |
|---|---|---|
| Choice rows, primary | **2-view: given order + exact reversal**, averaged in probability space (`od_gcp predict --tta-choice`) | same |
| Yes/no rows | **single read** | single read |
| T yes/no / T choice | **1.00 / 1.00** (fits 0.90 / 1.00; failed the bar) | 1.00 / 1.00 (fits 0.95 / 1.05; both worsen confirm) |
| Secondary configurations | single read (the identity view); batch calibration on the primary probabilities | same |
| JevBench (no submission) | 1 read on every row + band edge, T = 1 | same |
| Dev evidence | choice accuracy +0.10 [−0.48, +0.69]; choice flips 7.37% → 3.72%; OHS-3 drift mix 7.79% → 1.90%; yes/no 2-view −0.28 | choice +0.24 [−0.24, +0.70] (proxy); yes/no 2-view −0.18 [−0.33, −0.05]; 2-view flip rate not measured |

**Why 2-view on choice rows:**
- It does not change any primary endpoint on dev: choice accuracy is flat, and yes/no stays a single read, so the
  yes/no Brier is unchanged.
- It brings the drift endpoint from about 4x Jev's floor to about Jev's floor.
  - Part of that is mechanical. The 149 reversed twins are read in their base row's two orders, so they drift 0 by
    construction. The informative number is the rotated twins: 7.37% → 3.72% on dev, still about 2-3x Jev's floor.
  - The final table therefore reports drift for reversed and rotated twins separately
    (`ohs3_final_table.drift_by_twin_kind`). The exact reversal is `decoder_io`'s existing `tta_choice` and the A5 (a)
    draft. Its overlap with how the OHS-3 twins were built must still be disclosed.

**What it costs:**
- About **1.59x forward passes** on the OHS-3 call mix: (1,016 yes/no + 2 × 1,440 choice) / 2,456.
- More than that in tokens, because choice prompts with 20-40 options are longer. That is unmeasured: it would need
  OHS-3 text lengths, which must not be read.
- p50 goes from 16.6 to 31.6 ms per choice decision on the H100.
- **If the owner ranks the cost claim above the drift endpoint, choose (b), a single read everywhere.** The C1 cost
  must then be measured with whichever readout is chosen.

**Disclosures to keep in A5:**
- The 2-view failed the FINETUNE_PLAN 5.2 accuracy bar, and it is adopted for consistency.
- Reversed twins drift 0 by construction.
- The 4B-main 2-view numbers are a proxy, made from a random view.
- The 2-view does not help the equivalence or complement pairs.

**PREREG_OHS3 rule 4 change needed if read-twice is primary.** Rule 4 today says "Primary configuration: plain
readout with the temperatures already fitted on dev". Draft text:

> **Amendment to PREREG_OHS3 rule 4 (<date>, before the first OHS-3 run).**
> - The primary configuration is the A5 serving readout:
>   - choice rows are read twice, in the given option order and its exact reversal (one forward pass each);
>   - the probabilities are averaged per option name, and T_choice is applied after the average;
>   - yes/no rows are read once;
>   - temperatures from dev-select: T_noul = 1.00, T_choice = 1.00.
> - The two passes of a choice row are one decision in one run, so "exactly once per model" still holds.
> - The identity-view probabilities from the same run are reported as a secondary configuration ("single read").
>   Batch calibration (secondary) is applied to the primary probabilities.
> - On the 149 reversed `_perm` twins, the twin's 2-view read uses the same two orders as its base row, so their drift
>   is 0 by construction. Drift is also reported separately for reversed and rotated twins.
> - The speed and cost endpoints are measured with this readout.

**Tooling gaps.** None of these were built here, and frozen code was not touched.
- **The identity view is not saved.** `decoder_io.predict` with `tta_choice` overwrites it with the average, so
  `od_gcp predict --tta-choice` writes only the averaged probabilities.
  - Reporting the single read "from the same run" therefore needs a new wrapper that writes both views.
  - The alternative is a separate identity read, disclosed as a second read.
  - Update (review, 1 Oct): the OHS-3 harness closes this gap. `prep89/ohs3_lib.a5_read` keeps both views, and
    `ohs3_od_run.py` and the served path write `<name>_1v(_cal)` from the same reads (`ohs3_runbook.md`).
- **The scorer is fine.** `score_ohs3.py` needs no change, because it scores whatever probabilities the predictions
  file holds.

**Not measured yet:**
- an identity + reversed read of 4B-main;
- 4B-main's 2-view flip rate;
- the 2-view cost in tokens on the OHS-3 mix, and the C1 cost under load;
- prefix caching;
- the 2B's readouts.

**Update (1 Oct, goal step 8 harness gaps; tooling only, nothing measured on a GPU):**
- *2-view token cost on the OHS-3 mix:* now **logged at run time, counts only**. Every served call and every batch
  row records the input tokens of the identity read and of all reads (output 0); the timing summary and the batch
  meta give the all-reads / identity-read multiplier on the OHS-3 calls. It becomes a number when the OHS-3 run
  happens (no OHS-3 text is read for it).
- *C1 under load:* `prep89/load_test_c1.py` (dev rows, length-matched to the run's logged token counts) is built
  and CPU-tested; it needs one H100 session (best: `--then-load-test` in the timing session, about $0.45-0.85).
- *The 2B:* eager serving (PRISM-X I) and the 2B → 4B cascade can now be served and timed (`modal_ohs3_host.py
  --model-key 2b / cascade`); the 2B's dev readouts (T fit, 2-view) still need its dev reads, which need the final
  2B (`prep89/t_rule_check.py` gives the T rule for it).
- *Still open, GPU needed:* an identity + reversed read of the shipped 4B (C4 or 4B-main) and its 2-view flip rate
  (3 views); prefix caching.

**Update (2 Oct UTC, step 8 caveats closed on CPU; still nothing measured on a GPU):**
- *Every pre-registered T and cascade value is now machine-checked against dev-only evidence.*
  `prep89/t_rule_check.py --model ... --choice-single ... --json` records the dev reads (sha256 per split, adapter,
  view flags) and the ship values; `prep89/cascade_rule_fit.py` applies FINETUNE_PLAN 5.3's budget rule to two T logs.
  `ohs3_lib.check_fit_logs` (preflight) and every real OHS-3 script (`ohs3_od_run.py`, `ohs3_timing.py`,
  `ohs3_cascade.py`) stop unless the config's T / tau / w_big / route_on equal those logs (97 unit checks).
- *4B-E's T, re-derived with the new tool:* ship T = 1.00 (yes/no), 1.00 (choice, 2-view), 1.00 (choice, single read);
  same fits as above (0.90 / 1.00 / 1.00 on dev-select). The log is `prep89/t_fit_q35_4b_pxE.json` (ready as 4B-E's
  `T_fit_log` if 4B-E ships; C4 needs its own after gate job 3).
- *The cascade rule on today's models (dev only; 2B I_1600, single read, its T 1.00 / 0.95 -> 4B-E 2-view, route on
  the raw 2B top):* budgets 30-60% fail the select bound (one-sided 95% LB -2.06, -0.92, -0.57, -0.54 pp); **70% is
  chosen** (tau 0.8470, LB -0.37 pp). Dev-confirm, reported once: cascade 81.34% vs 4B-E 81.59%
  (-0.25 pp, 95% [-0.52, 0.00]), routed 69.1%. 5.3's use rule needs cost ratio + 0.691 < 0.85, i.e. a 2B costing
  < 16% of the 4B per decision: not plausible, so on today's models **serve the 4B alone** (as FINETUNE_PLAN 5.3
  already says). Logs: `prep89/t_fit_q35_2b_armI_1600.json`, `prep89/cascade_fit_dev_armI1600_to_pxE.json`
  (dev evidence only; not a config value). The final 2B gets the same two commands once its dev reads exist; its cost ratio needs the 2B and
  4B dev load tests (one H100 session).
- *The 2B I_1600's dev reads predate the view flags in the preds metas*, so its T log shows TODO (view "unknown");
  the final 2B's od_gcp reads carry them.
- *PRISM-X weights are pre-registered too:* `models.2b.prism_x_sha256` (sha256 of `prism_x.safetensors`) is required
  for a PRISM-X model and checked by the L4 loader, the Modal eager host and the preflight.
- *2-view token cost on the OHS-3 mix, dev estimate (no OHS-3 text):* on the dry run's stand-in (OHS-3's type and
  option counts, dev text, the real 4B tokenizer) all reads / identity read = **x1.78** (identity read 844.8 input
  tokens per call, all reads 1,504.4). The real multiplier is logged on the OHS-3 calls at run time.
- *C1 load test cost from the config:* `load_test_c1.py --plan`: +7.2 min in the timing session ($0.51 any region,
  $0.90 us-east); a new session 16 min for the 4B ($1.16-2.03), 12 min for the 2B ($0.87-1.53), 18 min for the
  cascade ($1.30-2.28). Boot minutes are estimates until the first H100 session.
