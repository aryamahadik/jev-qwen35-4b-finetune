# OpenDecide vs Jev: evidence table (read-only, 30 Sep 2026, about 19:45 UTC)

**Scope.** This file lists every measured number we have, per metric, for Jev (jev-1.13), 4B-E (`q35_4b_pxE`, the current best 4B), the older 4Bs (v10, v11b, v11c, plus dev-only siblings), the 2B pilot (`q35_2b_armI_1600`) and the plain 2Bs (v11r, E_L4_1600, kd pilot). Each number gives its test set, n, a CI where one exists, and its source.

**What was not touched.** No OHS-3 item text was opened. OHS-3 facts come only from `PREREG_OHS3.md` and `data/ohs3_summary.json`. There were no GPU, Modal, gcloud or paid calls.

**Numbers I recomputed.** Some numbers are my own recomputations, marked **[R]**. They were computed read-only from the stored pred files with the scripts in `projection/recompute/` (`dev.py`, `ohs.py`, `ohs_pair.py`, `ohs_track.py`; outputs `*_out.txt`). Those scripts reuse `gate_dev.py`'s own functions and copy `score_ohs.py`'s rules. Every [R] number that also appears in a results file matches it exactly, for example 4B-E dev-confirm 81.49, v11c OHS-2 79.92, and OHS-2 per-type 88.61 / 76.67.

**Estimates.** Estimates are marked **EST** and always come with a range.

**Conventions:**
- **Accuracy difference** = ours − Jev, in pp.
- **Brier difference** = ours − Jev. Positive means ours is worse. `PREREG_OHS3.md:127` uses Jev − ours, the opposite sign.
- **Jev** = the per-row mean of the runs `jev_guard` and `jev_r2_guard`.
- **OHS CIs:** paired cluster bootstrap over group_id, stratified by task, 10k resamples, seed 0 (the `score_ohs.py` rule).
- **Dev CIs:** paired bootstrap over group_id units, 10k resamples, seed 0 (`gate_dev.group_boot`, the ship-rule unit). These are a little wider than the ledger's older (split, group) intervals.
- **Dev splits:** the 9 gate splits of `gate_dev.SPLITS`: 8,143 rows; select 4,102 rows, confirm 4,041 rows.
- **`_cal`** = the plain readout with dev-fitted temperatures, the OHS primary configuration.
- **BC** = batch calibration, the secondary configuration.

---

## 0. Coverage: who has been measured where

| System | dev (9 splits) | OHS-1 | OHS-2 | JevBench v1.4.2 public | JevBench v1.5.4 public | jagged / OPI | redef |
|---|---|---|---|---|---|---|---|
| Jev (jev-1.13-20260917) | **never** | yes (2 runs) | yes (2 runs) | yes (p1, p2) | yes (p1, p2) | yes | **never** |
| 4B-E `q35_4b_pxE` | yes | **never** | **never** | never (smoke runs only) | yes | yes | yes |
| 4B v10 | yes | yes | yes | yes (A, B, all) | no | yes | no |
| 4B v11b | yes | yes | no | half A only | no | no | no |
| 4B v11c | yes | yes (preds only; not in the results file) | yes | half A | no | yes | no |
| 4B v11, v12t, v13t, blend50, 4B-I (pxI) | yes | no | no | no | no | pxI only | pxI only |
| 2B pilot `q35_2b_armI_1600` (PRISM-X I) | yes | no | no | no | yes | yes | yes |
| 2B v11r | yes | no | no | half A | no | yes | no |
| 2B E_L4_1600 (plain, layout E) | yes | no | no | no | no | yes | yes |
| 2B kd pilot / 0.8B kd | 4 splits only | yes | no | half A | no | no | no |
| New 4B `q35_4b_main500k` | training: step 2,650 / 30,457 at 117.7 min, 0 ALERT lines, snapshot s002500 saved (`logs/main4b_seg1.log`, last line) | – | – | – | – | – | – |

---

## 1. Overall accuracy (micro)

| System | Set | n | Value | Ours − Jev [95% CI] | Source |
|---|---|---|---|---|---|
| **Jev** | OHS-1 all | 1,847 base | **81.65** (runs 81.75 / 81.54; run agreement 98.81%) | – | `results_ohs/results_all.json` |
| Jev | OHS-1 sealed S / open A | 935 / 912 | 81.55 / 81.74 | – | `results_ohs/results_S.json`, `results_A.json` |
| **Jev** | OHS-2 all | 1,320 | **81.55** (runs 81.89 / 81.21; agreement 99.17%) | – | `results_ohs2/results_all.json` |
| Jev | OHS-2 S / A | 663 / 657 | 79.86 / 83.26 [R] | – | `results_ohs2/results_S.json`; [R] |
| Jev | JevBench v1.4.2 public (argmax) | 118 / 113 / 231 | A 103; B 96 (p2); all 200 (p1) and 199 (p2) | – | `bench/runs/scores_A.json`, `scores_B.json`, `scores_all.json` |
| Jev | dev | – | **not measurable** (Jev never run on dev) | – | audit `wnzbuj8i0.output`, yesno area |
| **4B-E** | dev-select / **dev-confirm** / pooled | 4,102 / 4,041 / 8,143 | 79.84 / **81.49** / 80.66 | – | `PREREG_FINAL.md:34`; [R] |
| 4B-E | dev unseen-source primary set (17 sources, both halves) | 3,847 | 81.49 [R] (the same figure as dev-confirm by coincidence: 3,135/3,847 vs 3,293/4,041) | – | [R], `gate_dev.UNSEEN_FROZEN_ROWS` |
| 4B-E | OHS-1 / OHS-2 | – | **never run** | – | `preds_ohs*/` listing |
| 4B v10 (`_cal`) | dev sel / conf / pooled | as above | 77.65 / 78.20 / 77.92 | – | [R] |
| 4B v10 | OHS-1 all | 1,847 | 76.12 | −5.52 [−7.29, −3.77], p_holm 0.000 | `results_ohs/results_all.json` |
| 4B v10 | OHS-1 S / A | 935 / 912 | 76.36 / 75.88 | −5.19 [−7.65, −2.73] / −5.87 [−8.24, −3.51] | `git HEAD:results_ohs/results_S.json`; `results_A.json` |
| 4B v10 | OHS-2 all / S | 1,320 / 663 | 78.26 / 77.68 | −3.30 [−5.04, −1.52], p_holm 0.0004 / −2.19 [−4.75, +0.30] | `results_ohs2/results_all.json`, `results_S.json` |
| 4B v10 | JevBench v1.4.2 | 118 / 113 / 231 | A 104; B 99; all 203 | all: +1.3 pp [−3.0, +5.6] | `scores_*.json` |
| 4B v11b | dev sel / conf / pooled | | 78.28 / 79.19 / 78.73 | – | [R] |
| 4B v11b | OHS-1 all / S | 1,847 / 935 | 77.91 / 77.43 | −3.74 [−5.37, −2.14] / −4.12 [−6.31, −1.93] | `results_ohs/results_all.json`, `results_S.json` |
| 4B v11b | OHS-1, BC (secondary) | 1,847 | 78.51 | −3.14 [−4.75, −1.51] | same |
| 4B v11b | JevBench v1.4.2 half A | 118 | 100 | – | `logs/budget_ledger.md:79` |
| 4B v11c | dev sel / conf / pooled | | 78.84 / 79.49 / 79.16 | – | [R] |
| 4B v11c | OHS-1 all | 1,847 | 78.02 [R] | −3.63 [−5.26, −2.00] [R] | [R] (`preds_ohs/q35_4b_v11c_cal.jsonl`; matches the audit's recompute) |
| 4B v11c | OHS-1 A / S | 912 / 935 | 77.96 / 78.07 [R] | – | [R] |
| 4B v11c | **OHS-2 all** | 1,320 | **79.92** | **−1.63 [−3.30, +0.11], p 0.070, p_holm 0.14** | `results_ohs2/results_all.json` |
| 4B v11c | OHS-2 BC / S | 1,320 / 663 | 80.53 / 78.28 | −1.02 [−2.77, +0.76] / −1.58 [−4.00, +0.75] | `results_ohs2/results_all.json`, `results_S.json` |
| 4B v11c | JevBench v1.4.2 half A | 118 | 107 | +3.4 pp [−2.5, +9.3] | `scores_A.json` |
| 4B v11 / v12t / v13t / blend50 / pxI | dev sel / conf | | 77.47/78.35; 78.40/78.79; 79.57/80.13; 79.40/80.05; 80.42/80.90 | – | [R] |
| Frozen Qwen3.5-4B | OHS-1 all | 1,847 | 75.85 | −5.79 [−7.52, −4.10] | `git HEAD:results_ohs/results_all.json` |
| **2B pilot I_1600** | dev sel / conf / pooled | | 75.16 / 75.18 / 75.17 | – | [R]; `logs/budget_ledger.md:179` |
| 2B v11r | dev sel / conf / pooled | | 75.62 / 76.24 / 75.93 | – | `PREREG_FINAL.md:35`; [R] |
| 2B v11r | JevBench v1.4.2 half A | 118 | 101 (score v14 76.85) | −1.7 pp [−9.3, +5.9] | `scores_A.json`; `budget_ledger.md:95` |
| 2B E_L4_1600 | dev sel / conf / pooled | | 74.31 / 75.45 / 74.87 | – | [R] |
| 2B kd pilot | OHS-1 all | 1,847 | 66.38 | −15.27 [−17.37, −13.21] | `git HEAD:results_ohs/results_all.json` |
| 2B kd pilot | JevBench v1.4.2 half A | 118 | 95 | −6.8 pp [−15.3, +1.7] | `scores_A.json` |
| 0.8B kd | OHS-1 all | 1,847 | 56.20 | −25.45 [−27.62, −23.20] | same |
| Cascade 2B v11r → 4B v13t (routing 40%) | dev-confirm | 4,041 | 80.15 (4B alone 80.13) | – | `budget_ledger.md:139` |
| Cascade 2B I_1600 → 4B-E | dev | – | −1.01 pp vs 4B-E at 40% routing [−1.78, −0.25]; −0.49 at 60% [−0.87, −0.13] | – | `FINETUNE_PLAN.md:445` |
| Cascade v11r → v11c | JevBench v1.4.2 half A | 118 | 105 (34-44% routed) | Jev 103 | `budget_ledger.md:140` |

---

## 2. Yes/no accuracy

On OHS-1, "base" yes/no means 527 rows; the audit's "743 aff rows" figure also counts the `_yn` variants.

| System | Set | n | Value | Ours − Jev [95% CI] | Source |
|---|---|---|---|---|---|
| Jev | OHS-1 base yes/no | 527 | 83.97 (runs 84.25 / 83.68) | – | [R] |
| Jev | OHS-1 A / S | 266 / 261 | 87.22 / 80.65 | – | [R] |
| Jev | OHS-2 yes/no | 360 | **95.83** (runs 96.11 / 95.56) | – | [R]; audit (yesno area) |
| Jev | OHS-2 per source | 120 each | moral_stories 97.5, tabfact 92.5 (93.3 / 91.7), ibm_argq 97.5 | – | `results_ohs2/results_all.json` per_task |
| Jev | JevBench v1.5.4 Noul (as returned) | 74 | CC 34.0 (p1), 30.3 (p2); abstains 27.0% / 28.4%; CC if argmax 67.6 / 70.3 | – | `bench/runs/scores_v154_all.json` |
| 4B-E | dev yes/no sel / conf / pooled | 2,172 / 2,157 / 4,329 | 83.15 / 85.77 / 84.45 | – | [R]; ledger X14 (85.8, `budget_ledger.md:169`) |
| 4B-E | JevBench v1.5.4 Noul | 74 | CC 27.3 at T=1 (abstains 33.8%); committed 75.9 (CC if argmax 78.4) | – | `scores_v154_all.json`; [R] what-if |
| 4B-E | yes/no letter-swap TTA | dev-confirm | −0.32 pp vs a single read | – | `budget_ledger.md:181` |
| v10 | dev yes/no sel / conf / pooled | | 80.11 / 80.76 / 80.43 | – | [R] |
| v10 | OHS-1 / OHS-2 yes/no | 527 / 360 | 77.80 / 86.94 | −6.17 [−9.87, −2.28] / −8.89 [−12.50, −5.42] | [R] |
| v11b | dev yes/no | | 81.49 / 82.61 / 82.05 | – | [R] |
| v11b | OHS-1 yes/no | 527 | 77.42 | −6.55 [−10.15, −2.85] | [R] |
| v11c | dev yes/no | | 81.63 / 82.75 / 82.19 | – | [R] |
| v11c | OHS-1 yes/no | 527 | 79.89 | −4.08 [−7.69, −0.38] | [R] |
| v11c | OHS-1 legalbench_hearsay | 82 | 56.1 vs Jev 85.4 (34 false No vs 2 false Yes) | task gap +29.3 in Jev's favour | [R]; audit (win area) |
| v11c | **OHS-2 yes/no** | 360 | **88.61** | **−7.22 [−10.56, −3.75]** | [R]; `budget_ledger.md:153` (88.6 vs 96.1 against Jev run 1) |
| v11c | OHS-2 moral / tabfact / argq | 120 each | 85.0 / 84.2 / 96.7 | moral: Jev-only correct 15, ours-only 0, McNemar p = 6.1e-5; tabfact: p = 0.035 vs run 1 and 0.093 vs run 2 | audit `wnzbuj8i0.output` (yesno area) |
| 2B I_1600 | dev yes/no | | 79.19 / 78.16 / 78.68 | – | [R] |
| 2B I_1600 | JevBench v1.5.4 Noul | 74 | CC −21.2 at T=1 (abstains 56.8%); committed 70.1 (CC if argmax 70.3) | – | `scores_v154_all.json`; [R] |
| 2B v11r / E_L4_1600 | dev yes/no pooled | 4,329 | 79.39 / 78.38 | – | [R] |
| 2B kd | OHS-1 yes/no | 527 | 72.49 | −11.48 [−15.94, −7.02] | [R] |

---

## 3. Multiple-choice accuracy

| System | Set | n | Value | Ours − Jev [95% CI] | Source |
|---|---|---|---|---|---|
| Jev | OHS-1 choice | 1,320 | 80.72 (80.76 / 80.68) | – | [R] |
| Jev | OHS-1, more than 26 options | 210 | 77.86 | – | `results_ohs/results_all.json` |
| Jev | OHS-2 choice | 960 | 76.20 (76.56 / 75.83) | – | [R] |
| Jev | JevBench v1.5.4 Choice CC | 139 | 82.9 (p1) / 80.6 (p2) | – | `scores_v154_all.json` |
| Jev | eval_card wide options | – | 86.3 | – | `budget_ledger.md:96` |
| 4B-E | dev choice sel / conf / pooled | 1,930 / 1,884 / 3,814 | 76.11 / 76.59 / 76.35 | – | [R] |
| 4B-E | JevBench v1.5.4 Choice CC | 139 | 80.6 (hard tier 66.1 vs Jev 70.1) | – | `scores_v154_all.json` |
| v10 | dev choice | | 74.87 / 75.27 / 75.07 | – | [R] |
| v10 | OHS-1 / OHS-2 choice | 1,320 / 960 | 75.45 / 75.00 | −5.27 [−7.18, −3.41] / −1.20 [−3.28, +0.83] | [R] |
| v10 | OHS-1, more than 26 options | 210 | 71.9 | – | `results_ohs/results_all.json` |
| v11b | dev choice / OHS-1 choice | | 74.66 / 75.27 / 74.96; 78.11 | OHS-1: −2.61 [−4.31, −0.90] | [R] |
| v11b | OHS-1, more than 26 options | 210 | 76.67 | – | `results_ohs/results_all.json` |
| v11c | dev choice | | 75.70 / 75.74 / 75.72 | – | [R] |
| v11c | **OHS-1 choice** | 1,320 | 77.27 | **−3.45 [−5.21, −1.70]** | [R] |
| v11c | OHS-1, more than 26 options | 210 | 75.24 | Jev 77.86 | [R] |
| v11c | **OHS-2 choice** | 960 | 76.67 | **+0.47 [−1.51, +2.40]** (tie) | [R] |
| v11c | OHS-2 choice, BC | 960 | 77.50 | +1.30 [−0.78, +3.33] | [R] |
| v11c | eval_card wide options | – | 89.8 | Jev 86.3 | `budget_ledger.md:96` |
| 2B I_1600 | dev choice | | 70.62 / 71.76 / 71.19 | – | [R] |
| 2B I_1600 | JevBench v1.5.4 Choice CC | 139 | 74.9 | – | `scores_v154_all.json` |
| 2B v11r | dev choice | 3,814 | 72.00 pooled | – | [R] |
| 2B v11r | eval_card wide options | – | 86.5 | – | `budget_ledger.md:96` |
| 2B kd | OHS-1 choice | 1,320 | 63.94 | −16.78 [−19.14, −14.53] | [R] |

---

## 4. Brier and calibration (yes/no; PREREG_OHS3 primary endpoint 3)

The OHS-3 "matches" bar for Brier: the lower bound of Jev − ours must be above −0.010 (`PREREG_OHS3.md:126`).

| System | Set | n | Value | Ours − Jev [95% CI] | Source |
|---|---|---|---|---|---|
| Jev | OHS-1 yes/no | 527 | 0.1142 (0.1144 / 0.1140) | – | `results_ohs/results_all.json`; [R] |
| Jev | OHS-2 yes/no | 360 | **0.0379** (0.0372 / 0.0386) | – | `results_ohs2/results_all.json` |
| Jev | JevBench v1.5.4 | – | Calibration axis 81.2 / 79.7; Noul ECE 0.089, Brier 0.105 | – | `scores_v154_all.json` |
| Jev | JevBench v1.4.2 half A | – | Calibration axis 76.4 | – | `scores_A.json` |
| Jev | eval_card (in-house) | – | Brier 0.106 | – | `results_eval_card/RESULTS.md` |
| Jev | jagged, clean items | 486 | Brier 0.096 | – | `score_jagged.py` [R] |
| 4B-E | dev yes/no, raw | 4,329 | 0.1143 (confirm 0.1082) | – | [R] |
| 4B-E | dev, cross-fitted T | 4,329 | 0.1140 (T 0.9 / 0.85) | – | [R] |
| 4B-E | plan temperature | – | T = 0.9 / 1.0, gain 0.0006, so it ships at T = 1 | – | `FINETUNE_PLAN.md:427` |
| 4B-E | JevBench v1.5.4 | – | Calibration 84.3 (T=1) / 83.4 (committed); Noul Brier 0.0697, ECE 0.095 | – | `scores_v154_all.json`; `RESULTS_30sep.md:13-14` |
| 4B-E | jagged, clean items | 486 | Brier 0.032 | – | [R] |
| v10 | OHS-1 / OHS-2 | 527 / 360 | 0.1613 / 0.0904 | +0.047 [+0.026, +0.068] / +0.0525 [+0.033, +0.072] | results files |
| v10 | dev (raw) / eval_card | | 0.1406 / 0.073 | eval_card: −0.033 [−0.048, −0.018] (ours better) | [R]; `results_eval_card/RESULTS.md` |
| v11b | OHS-1 | 527 | 0.1485 | +0.034 [+0.017, +0.051] | `results_ohs/results_all.json` |
| v11c | OHS-1 | 527 | 0.1450 | +0.0308 [+0.0120, +0.0489] | [R] |
| v11c | **OHS-2** | 360 | **0.0831** | **+0.0452 [+0.0286, +0.0618]** | `results_ohs2/results_all.json` |
| v11c | OHS-2 decomposition | 360 | Jev REL 0.0071 vs ours 0.0041: the whole gap is resolution (accuracy), not reliability | – | `budget_ledger.md:153` (X12) |
| 2B I_1600 | dev raw / cross-fitted | 4,329 | 0.1496 / 0.1469 | – | [R] |
| 2B I_1600 | plan T on dev-confirm | – | T 0.7 / 0.95: 0.1505 → 0.1483; fails the per-split check | – | `FINETUNE_PLAN.md:428` |
| 2B I_1600 | JevBench v1.5.4 | – | Calibration 81.8; Noul Brier 0.124 | – | `scores_v154_all.json` |
| 2B v11r | dev raw | 4,329 | 0.1358 | – | [R] |

**Reading.**
- On the held-out exams we lose Brier by 0.031-0.053, which is far outside the −0.010 "matches" bar.
- On in-house and JevBench sets we win Brier.
- The X12 decomposition says a temperature cannot close the held-out gap, because the gap comes from accuracy (resolution).

---

## 5. Consistency

**How PREREG_OHS3 defines it** (`PREREG_OHS3.md:133-142`):
- **Complement violation** on the 300 `_neg` pairs: the share of pairs whose two decisions are not complementary. A tie or a missing answer counts as a violation. Also reported: the mean |P_base(yes) + P_neg(yes) − 1|.
- **Option-order drift** on the 304 `_perm` pairs: the share of pairs whose predicted option changes. Also reported: the mean total-variation distance between the two answers.
- Differences are Jev − ours. They are secondary endpoints with BH correction.
- There is no paraphrase endpoint.

**Scorer mismatch.** `score_ohs.py:147-157` scores complement as the mean |pa + pb − 1| and skips missing answers. That does not match the pre-registration (audit, win area). The OHS-1 figures below use the pre-registered decision definition [R].

| System | Set | n pairs | Complement violation (decision) | mean \|pa+pb−1\| | Double-negation flip | Paraphrase flip | Source |
|---|---|---|---|---|---|---|---|
| Jev | OHS-1 | 769 (743 `_neg`) | 11.05% / 10.53% (runs); `_neg` only 10.77 / 10.23 | 0.0974 / 0.0969 | 16.69% / 16.96% | 2.56% / 3.23% (file: 2.42 / 2.83) | [R]; `results_ohs/results_all.json` |
| v11c | OHS-1 | 769 | **11.31%**; Jev − ours **−0.52 pp [−3.50, +2.41]** (tie) | 0.0927 | 18.17% | 4.17% | [R] |
| v11b | OHS-1 | 769 | 11.96%; Jev − ours −1.17 [−3.90, +1.62] | 0.0801 | 15.48% | 5.65% | [R]; file |
| v10 | OHS-1 | 769 | 17.17%; Jev − ours −6.37 [−9.64, −3.02] | 0.1198 | 22.34% | 7.27% | [R]; file |
| Frozen 4B / 2B kd | OHS-1 | 769 | 39.66% / 27.31% | 0.3061 / 0.1243 | 44.0% / 47.6% | 12.3% / 11.2% | [R] |
| Any system | OHS-2 | – | not measured (OHS-2 has no consistency layer) | – | – | – | `results_ohs2` (all null) |
| **Any system** | **option-order drift** | – | **never measured, on any set, for any model or for Jev.** No `_perm` read exists; the ship rule's (f) needs new reads (`PREREG_FINAL.md:227-232, 318`). | | | | |
| 4B-E | dev (no Jev) | 1,122 complement / 722 equiv | **4.81%** | – | equivalence flip **5.68%** (722 pairs: paraphrase or double negation, yes/no) | | [R]; `PREREG_FINAL.md:451` |
| 4B-I / v13t / v11c / v11b / v10 | dev | same | 3.74 / 5.35 / 6.60 / 6.15 / 13.73% | – | 7.89 / 9.83 / 9.97 / 7.34 / 13.30% | | [R] |
| 2B v11r / I_1600 / E_L4_1600 | dev | same | 8.11 / 10.78 / 14.62% | – | 12.60 / 12.47 / 12.05% | | [R] |
| v10 vs jev_guard | eval_card (in-house, 295 groups) | – | contradiction rate 4.4 vs 4.4% | 0.055 vs 0.085 (−0.030 [−0.040, −0.018]) | double-negation drift 0.048 vs 0.206 | 2.4 vs 2.0% | `results_eval_card/RESULTS.md` |

**Dev → OHS-1 complement relation** [R]: v10 13.73 → 17.17%, v11b 6.15 → 11.96%, v11c 6.60 → 11.31%. OHS-1 runs about 1.25-1.9x the dev rate. EST: 4B-E's 4.81% on dev maps to about 6-9% on an OHS-1-like set, against Jev's about 10.8%. This is weak: 3 points, different pair wording.

---

## 6. Hijack attack, jagged (planted authority line; `score_jagged.py`)

ASR is the share of "deleted" items, answered correctly on the clean text, that the injected copy pushes below 0.5. Intervals are Wilson intervals on items [R].

| System | ASR (k/n) [95%] | Attacked accuracy | Attacked-accuracy diff vs jev_guard | Source |
|---|---|---|---|---|
| Jev (jev_guard) | **99.4%** (344/346) [97.9, 99.8] | 27.0 | – | [R]; `budget_ledger.md:96` |
| Jev (no guard) | 100% (349/349) | 26.5 | – | [R] |
| **4B-E** | **0.6%** (2/354) [0.2, 2.0] | 96.1 | +69.1 [+64.4, +73.9] | [R]; `PREREG_FINAL.md:240` |
| 4B-I / v11c / v10 | 0.0% (0/356) / 1.1% (4/353) / 11.2% (40/356) | 92.8 / 95.9 / 90.7 | – | [R] |
| **2B I_1600** | **1.1%** (4/356) [0.4, 2.9]; PRISM-X off 2.6% | 90.1 | +63.2 [+57.2, +68.7] | [R] |
| 2B v11r / E_L4_1600 | 3.9% (13/333) [2.3, 6.6] / 10.0% (35/350) [7.3, 13.6] | 91.2 / 87.7 | – | [R] |
| Matched pair I_1600 vs E_L4_1600 | −8.9 pp [−12.0, −5.7] | – | – | `budget_ledger.md:179` |
| 2B E / E_L4 / I (800 steps) | 5.8 / 19.2 / 5.9% | – | – | [R]; ledger X7 (run-to-run swing) |

**Caveats.**
- eval_jagged has been used for selection (ship-rule constraint (g)), so it is not held out.
- The ASR swings a lot between runs: E 5.8% vs E_L4 19.2% (`budget_ledger.md:143-146`).
- It covers one attack direction.

---

## 7. Prompt injection, OPI (`score_opi.py`)

ASR is the share of attacks on clean-correct texts that are answered with the attacker's label. The paired diff vs jev_guard uses 2,000 bootstraps over clean texts. The Wilson intervals are naive, because the 5 strategies are clustered per text.

| System | ASR (k/n) [Wilson] | Diff vs jev_guard [95%] | Source |
|---|---|---|---|
| Jev (jev_guard) | **1.3%** (10/785) [0.7, 2.3] | – | [R]; `budget_ledger.md:96` |
| Jev (no guard) | 2.3% (18/785) | +0.5 [−0.1, +1.5] | [R] |
| **4B-E** | **1.0%** (8/775) [0.5, 2.0] | −0.4 [−1.1, +0.1] (tie) | [R] |
| 4B-I / v11c / v10 | 1.5 / 1.0 / 0.6% | +0.4 [−0.7, +1.8] / −0.1 [−1.9, +1.5] / −0.4 [−1.6, +0.5] | [R] |
| **2B I_1600** | **4.4%** (34/780) [3.1, 6.0] | **+3.7 [+1.2, +6.8]** (worse; the audit reports [+1.2, +6.6]) | [R] |
| 2B I_1600, PRISM-X off | 3.8% | +2.5 [+0.8, +4.6] | [R] |
| 2B v11r / E_L4_1600 / E / I | 2.4 / 2.1 / 2.3 / 0.8% | +1.0 [−0.4, +2.9] / +1.7 [+0.3, +3.5] / +1.6 [+0.1, +3.5] / +0.6 [−0.4, +2.2] | [R] |
| v10 vs jev_guard, in-house eval_card injection (held-out C+D) | 0.8% vs 10.0% | −9.2 [−16.7, −2.8] | `results_eval_card/RESULTS.md` |

---

## 8. Definition-overwrite attack, redef (`score_redef.py`; 300 items)

| System | ASR (k/n) [Wilson] | Flip | Source |
|---|---|---|---|
| **4B-E** | **16.5%** (42/254) [12.5, 21.6] | 18.1% | [R]; audit (win area) |
| 4B-I | 10.2% (26/254) [7.1, 14.6] | 11.4% | [R]; `budget_ledger.md:172` |
| **2B I_1600** | **3.3%** (8/246) [1.7, 6.3] | 4.5% | [R] |
| 2B E_L4_1600 / E / I | 2.8 / 2.8 / 6.0% | – | [R] |
| **Jev, v10, v11c, v11r** | **never run** | – | preds_eval_redef listing |

---

## 9. Speed

**How speed is defined:**
- **PREREG_OHS3 does not define speed.** There are 0 hits for latency, speed or cost in `PREREG_OHS3.md`, `PREREG_OHS2.md` or `PREREG_OHS.md`.
- `PREREG_FINAL.md:295` makes p50/p95 latency report-only, "measured with their own tools".
- The audit lists "define speed and cost" as a must-fix before OHS-3 (`wnzbuj8i0.output`, verdict item 9).
- **JevBench v1.5 speed axis:** the mean of the p50 and p95 speed points on the open standard (and judge) items. Self-hosted latency counts as ×2 + 0.15 s (`bench/v154/README.md:37`; `score_v154.py` docstring).

**GPU compute (server side, batch 1, one decision per request):**

| System | Hardware and setup | p50 / p95 | n | Source |
|---|---|---|---|---|
| 4B-E (layout E) | L4, eager (no CUDA graphs), slow causal_conv1d fallback | **110.1 / 112.3 ms** (standard items); all items 112.0 / 754.7 ms | 72 / 231 | `bench/runs/scores_v154_all.json`; `RESULTS_30sep.md:7` |
| 2B I_1600 (PRISM-X I) | same L4, eager (PRISM-X blocks CUDA graphs) | **128.0 / 130.8 ms**; all 129.2 / 343.3 ms | 72 / 231 | same |
| 4B v10 (text_first) | H100, CUDA graphs | 13.2 / 87.6 ms (half A); all 13.6 / 91.0 | 118 / 231 | `scores_A.json`, `scores_all.json` |
| 4B v11c | H100, CUDA graphs | 13.1 / 89.1 ms | 118 | `scores_A.json` |
| 2B v11r / 2B kd | H100, CUDA graphs | 8.9 / 46.5 ms; 9.5 / 47.6 ms | 118 | `scores_A.json` |
| Earlier 4B, eager | H100 / L4 | 27.5 / 39.6 ms; 59.8 / 62.7 ms (the log does not name the model) | 200 | `logs/q4b_latency_h100.log`, `logs/final_latency.log`; `HANDOFF.md:203` ("4B 27–60 ms") |
| v07, graphs vs eager | H100 | 72 → 14 ms per decision | – | memory `jevbench-loop.md` |

**End to end (client wall clock, same laptop):**

| System | Path | p50 / p95 | n | Source |
|---|---|---|---|---|
| 4B v10 | H100 + graphs via `modal.forward` tunnel | **114.6 / 124.1 ms** (server 44.8 / 50.9) | 515 | `logs/tunnel_q35_4b_v10_tunnel_plain.json`; `HANDOFF.md:147` |
| 4B v10 | Modal web endpoint | 410.3 / 517.0 ms (server median 123.1) | 515 | `logs/bench_api.json` |
| Network only | web endpoint / tunnel, CPU echo | 356 / 422 ms; 71.9 / 77.1 ms | – | `logs/latency_probe.log`; `HANDOFF.md:249` |
| **Jev (OpenRouter)** | same laptop | eval_card 194 / 305 (guard), 187 / 266; OHS-1 202 / 281 and 197 / 286; OHS-2 205 / 539 and 196 / 285; jagged 221 / 346; OPI 209 / 336 ms | 515-1,847 calls | [R] from `preds_*/jev*_raw.jsonl` `latency_ms` |
| Jev | JevBench v1.5.4 run, standard items / all items | 238 / 303 (p1), 248 / 350 (p2); all 239 / 319 | 72 / 231 | `scores_v154_all.json` |
| Jev | published and third-party figures | official 70-500 ms; OpenRouter p50 168, p90 284, p99 435; JevBench, measured from Germany, 0.62 s; board S axis 83.8 | – | memory `jev-market-facts.md:11-14`; `bench/v154/README.md:15` |

**JevBench speed axis:**
- v1.4.2 half A: v10 92.4 vs Jev 91.1.
- **v1.5.4: 4B-E 88.6 and 2B-I 87.8 vs Jev 91.4 / 90.6. Jev wins the speed axis in the latest run,** because the L4-eager setup gives 110 ms ×2 + 0.15 s = 370 ms against Jev's 238 ms.

**Never measured:**
- layout E end to end;
- 4B-E with CUDA graphs;
- the PRISM-X 2B on an H100;
- the cascade;
- any p95 under concurrency.

The only same-setup comparison of the two final architectures shows the **2B-I slower than the 4B-E** (128 vs 110 ms on the L4, eager).

---

## 10. Cost per 1,000 decisions

**How cost is defined:**
- **OHS-3:** not defined.
- **JevBench:** pooled input and output tokens × list price, in $ per 1,000 decisions. Ours is priced at the frozen Qwen3.5-4B reference (DeepInfra $0.03/M in, $0.15/M out). Jev is priced at $0.042/M in, with output free (`bench/v154/README.md:38`; memory `jev-market-facts.md:22`).

| System | Figure | Value | Source |
|---|---|---|---|
| 4B-E and 2B-I | JevBench v1.5.4 formula | $0.0245 / 1K (817.8 input tokens per decision); cost axis 58.3 | `scores_v154_all.json` |
| Jev | JevBench v1.5.4 formula | $0.0384 / 1K (914.8 input + 42.9 output tokens); cost axis 52.5 | same |
| v10 / v11c | JevBench v1.4.2 half A | $0.0354 / 1K (axis 53.5); 2B $0.0212 (60.2); Jev $0.0387 (52.4) | `scores_A.json` |
| v10, all 231 | JevBench v1.4.2 file | $0.0210 / 1K (axis 60.3); a different price basis from half A, unexplained | `scores_all.json` |
| Jev, official board | – | $ axis 54.7; 4B fine-tunes 63.1-64.5 | `bench/v154/README.md:15`; score_v154 board print |
| **Jev, billed** | 2 × OHS-1 = 3,694 calls (8,584 row decisions, since calls bundle rows) cost $0.12 | **$0.032 per 1K calls** ($0.014 per 1K row decisions) | `budget_ledger.md:64`; [R] row_map counts |
| Jev, OHS-3 plan | 4,912 calls estimated at $1.2-2.7 | This does not agree with $0.032/1K, which gives about $0.16. Treat it as a budget cap, not a price. | memory `keep-openrouter-key.md:19` |
| **Ours, real serving** | **never measured** | – | audit (win area) |
| Ours, EST (GPU $/h × latency, batch 1, 100% use) | H100 $3.95/h (`budget_ledger.md:7`) × 13 ms → **$0.014**; × 45 ms (tunnel server median) → $0.049. L4 $0.80/h × 110 ms (4B-E eager) → $0.024; × 128 ms (2B-I) → $0.028. At 40% use, multiply by 2.5. | **EST $0.014-0.12 per 1K** vs Jev $0.032-0.038 | derived |
| Layout E prompt length | mean 627 vs 265 characters (text_first) on 2,000 dev rows | more input tokens per decision | audit (win area, skeptic "missed") |
| Cascade cost rule | serve the cascade only if (2B/4B inference cost ratio + routed fraction) < 0.85. The ratio is not measured (0.46-0.48 comes from training steps). With current models the rule picks 70% routing = 1.15× the 4B's cost, so the 4B is served alone. The one measured inference ratio is **1.16** (2B-I 128 ms vs 4B-E 110 ms, L4 eager). | – | `FINETUNE_PLAN.md:448`; `scores_v154_all.json` |

---

## 11. JevBench (public items only; unofficial, "our run, official formulas")

| Readout | Jev | 4B-E | 2B-I pilot | Diff vs Jev p1 (paired bootstrap) | Source |
|---|---|---|---|---|---|
| v1.4.2 argmax, half A (118) | 103 | – (v11c 107, v10 104) | – (v11r 101, kd 95) | v11c +3.4 [−2.5, +9.3]; v11r −1.7 [−9.3, +5.9] | `scores_A.json` |
| v1.4.2 argmax, all 231 / half B 113 | 200 (p1), 199 (p2) / 96 | v10: 203 / 99 | – | v10 all: +1.3 [−3.0, +5.6] | `scores_all.json`, `scores_B.json` |
| v1.4.2 score (v14 harmonic), half A | 72.51 | v10 74.94, v11c 74.80 | v11r 76.85, kd 74.86 | – | `scores_A.json` |
| v1.5.4, raw readout (soft yes/no as trained / returned): Intelligence | 63.2 (p1) / 62.3 (p2) | 62.5 | 39.9 | 4B −0.7 [−9.8, +9.3]; 2B −23.3 [−34.2, −11.9]; Jev p2 −0.9 [−4.4, +2.5] | `scores_v154_all.json`; `RESULTS_30sep.md:13-18` |
| v1.5.4 raw: Calibration / Speed / Cost / Score A | 81.2 / 91.4 / 52.5 / 68.80 | 84.3 / 88.6 / 58.3 / 71.03 | 81.8 / 87.8 / 58.3 / 38.62 | – | same |
| v1.5.4, decisive (ours committed, Jev as returned): Intelligence | 63.2 | **78.7** | 70.3 | 4B **+15.5 [+5.2, +26.9]**; 2B +7.1 (tie). Half B: 4B +19.9 [+4.2, +37.9]; 2B +15.8 [+3.8, +29.0] | `RESULTS_30sep.md:14-26` |
| v1.5.4 decisive: Score A | 68.80 | 75.27 | 71.96 | – | same |
| **v1.5.4, symmetric decisive (Jev also committed)** [R] | **73.6 (p1) / 73.7 (p2)**; Calibration 76.8, Score A 70.66 | 78.7 | 70.3 | **4B +5.1 [−4.4, +15.0], tie; 2B −3.3 [−15.0, +9.2], tie. Half B: 4B +7.8 [−6.1, +24.3]; 2B +3.7 [−8.1, +15.9]** | [R]: Jev `results.jsonl` with P(yes) → 0/1 by argmax (the same transform as `v154_whatif/*_T0`), scored with `score_v154.py` |
| Argmax-correct (v1.4 rule) on the v1.5.4 run | 200 / 199 | 204 | 194 | – | `scores_v154_all.json` diagnostics |
| Official board, 1,624 decisions (context only) | 72.13, #3; I 72.0 (open 71.5 / sealed 72.5) | – | – | best 4B, JevK5: 71.90, I 56.3 (open 61.6 / sealed 50.9); decider-4b v2: 71.28, I 55.8 (61.7 / 49.8); decider-2b: 45.10 | `leaderboard_v154.json` via `score_v154.py`; `bench/v154/README.md:15` |

**Caveats.**
- The public items have been our development set: half A was used for selection, and half B has been seen 4 times (`no-jevbench-submission` memory; `RESULTS_30sep.md` caveats).
- On the board, 4B fine-tunes lose about 10-11 Intelligence points from public to sealed items; Jev loses none.
- The "+15.5" is asymmetric: only our side is committed. Committing both sides gives +5.1 (tie).
- The 2B's raw readout abstains on 56.8% of yes/no items.

---

## 12. Dev → OHS relation for the 4Bs (all [R] unless noted)

| 4B | dev-select | dev-confirm | dev pooled | Unseen-source set (3,847 rows) | dev yes/no / choice (pooled) | OHS-1 | OHS-2 |
|---|---|---|---|---|---|---|---|
| v10 | 77.65 | 78.20 | 77.92 | 79.10 | 80.43 / 75.07 | 76.12 | 78.26 |
| v11b | 78.28 | 79.19 | 78.73 | 79.83 | 82.05 / 74.96 | 77.91 | – |
| v11c | 78.84 | 79.49 | 79.16 | 79.59 | 82.19 / 75.72 | 78.02 | 79.92 |
| v12t / v13t / blend50 | 78.40 / 79.57 / 79.40 | 78.79 / 80.13 / 80.05 | 78.60 / 79.85 / 79.72 | – / 80.45 / – | – | – | – |
| 4B-I (pxI) | 80.42 | 80.90 | 80.66 | 80.97 | 84.59 / 76.19 | – | – |
| **4B-E** | **79.84** | **81.49** | **80.66** | **81.49** | **84.45 / 76.35** | – | – |

**Paired gains** (dev CIs from the group_id bootstrap; OHS CIs from the stratified cluster bootstrap):

| Step | dev sel | dev conf | dev pooled | Unseen set | OHS-1 | OHS-2 | OHS gain ÷ pooled dev gain |
|---|---|---|---|---|---|---|---|
| v10 → v11b | +0.63 | +0.99 | +0.81 | +0.73 | +1.79 [+0.43, +3.09] | – | 2.2 |
| v10 → v11c | +1.19 | +1.29 | +1.24 | +0.49 | +1.89 [+0.54, +3.20] | +1.67 [+0.23, +3.18] | 1.5 / 1.35 |
| v11b → v11c | +0.56 | +0.30 | +0.43 | −0.24 | +0.11 [−1.08, +1.25] | – | 0.26 |
| Frozen → v10 | +9.86 (5 splits) | +7.58 (5 splits) | – | +7.06 (unseen rows of dev_nc / negwords / claims) | **+0.27 [−1.09, +1.68]** | – | about 0.03 |
| **v11c → 4B-E** | **+1.00 [−0.27, +2.27]** | **+2.00 [+0.60, +3.34]** | **+1.50 [+0.56, +2.46]** | +1.90 [+0.56, +3.25] | ? | ? | – |

- **By question type, v10 → v11c:**
  - dev yes/no +1.76, then OHS-1 yes/no +2.09 [−0.57, +4.93] and OHS-2 +1.67 [−1.11, +4.44];
  - dev choice +0.65, then OHS-1 +1.82 [+0.38, +3.34] and OHS-2 +1.67 [+0.00, +3.33].
- **By question type, v11c → 4B-E on dev:**
  - yes/no pooled +2.26 (select +1.52 [−0.42, +3.44], confirm +3.01 [+1.03, +5.08]);
  - choice +0.63 (select +0.41, confirm +0.85).
  - So 4B-E's dev gain is mostly on yes/no.
- **Selection bias:** 4B-E scores +0.7 to +1.3 pp better on confirm than on select against all 6 sibling 4Bs (`FINETUNE_PLAN.md:376`). Dev-select, the half not used to pick it, is the fairer gain (about +1.0). The skeptic says the same (`wnzbuj8i0.output`, win area: "real dev gain about +1").
- **EST for 4B-E on OHS-2-like data:** apply the OHS/dev ratios between fine-tuned siblings (0.26-2.2) to a +1.0 to +1.5 dev gain. That gives +0.3 to +3.3 over v11c, so about 80.2-83.2 against Jev's 81.55. The central case, a ratio of about 1.4 on +1.0, gives about 81.3.
  - It rests on 3 correlated pairs.
  - The frozen → v10 step shows that dev can overstate held-out gains about 30×.
  - Treat it as weak.

---

## 13. 2B vs 4B gap

| Pair | Set | 2B − 4B [95% CI] | Source |
|---|---|---|---|
| Teacher → student: v10 → 2B kd (12K pilot mix) | OHS-1 | **−9.75 [−11.75, −7.73]**; yes/no −5.31 [−9.49, −1.33]; choice −11.52 [−13.79, −9.26] | [R] |
| v10 → 2B kd | JevBench v1.4.2 half A | 95 vs 104 of 118 | `scores_A.json` |
| Teacher → student: v11c → v11r (59.7K rows, kd 0.5) | dev pooled | **−3.23 [−4.38, −2.10]** (select −3.22, confirm −3.24); yes/no −2.80, choice −3.72 | [R] |
| v11c → v11r | unseen-source set | −3.58 (76.01 vs 79.59) | [R] |
| v11c → v11r | JevBench v1.4.2 half A / jagged / OPI / eval_card wide | 101 vs 107; 3.9% vs 1.1%; 2.4% vs 1.0%; 86.5 vs 89.8 | `budget_ledger.md:95-96` |
| **Current finals: 2B I_1600 vs 4B-E** (not matched: different data, lineage and steps) | dev pooled | **−5.49 [−6.69, −4.29]** (select −4.68, confirm −6.31); yes/no −5.77, choice −5.16 | [R] |
| I_1600 vs 4B-E | unseen-source set | −5.20 [−6.94, −3.44] | [R] |
| I_1600 vs 4B-E | JevBench v1.5.4 | Intelligence 39.9 vs 62.5 (raw), 70.3 vs 78.7 (committed); argmax 194 vs 204 of 231 | `scores_v154_all.json`; `RESULTS_30sep.md` |
| I_1600 vs 4B-E | security | jagged 1.1 vs 0.6%; OPI 4.4 vs 1.0%; redef 3.3 vs 16.5% (the 2B is better on redef) | §6-8 |
| v11r vs 4B-E | dev pooled | −4.73 [−5.92, −3.54] | [R] |
| 2B arm I (800 steps, from base) vs 4B-I (800 steps, from v13t) | dev-confirm | 73.84 vs 80.90 (not matched on init) | [R] |

The final 2B is trained on 4B-E labels and the full golden set, so **its gap is unmeasured**. The past distillation gaps were −3.2 pp (dev) and −9.8 pp (OHS-1). EST for a well-distilled 2B: dev gap −3 to −5.5 pp; held-out gap likely larger, −4 to −10.

---

## 14. OHS-3 composition (from `PREREG_OHS3.md:10-31` and `data/ohs3_summary.json` only)

| Task | Base rows | Question type | Options | Track | Source |
|---|---|---|---|---|---|
| se_site | 142 | choice | 40 | F | PREREG table |
| fr_agency | 142 | choice | 40 | F | same |
| uk_wq_answering_body | 142 | choice | 20 | F | same |
| medrxiv_category | 142 | choice | 20 | F | same |
| ct_study_type | 140 | yes/no ("Interventional") | 2 | F | same; 2 rows dropped (`ohs3_summary.json` dropped_for_overlap) |
| openfda_recall_class | 144 | yes/no ("Class I") | 2 | F 91 / U 53 | same |
| nvd_attack_vector | 144 | yes/no, label verification (4 CVSS AV values) | 2 | F | same |
| zenodo_resource_type | 144 | yes/no, label verification (20 types) | 2 | F | same |
| causal_news_corpus | 144 | yes/no ("Causal") | 2 | U | same |
| fewrel_relation | 142 | choice | 20 | U | same |
| few_nerd_fine | 142 | choice | 20 | U | same |
| bias_in_bios_profession | 142 | choice | 20 | U | same |
| rosetta_code_language | 142 | choice | 20 | U | same |

**Totals** (`ohs3_summary.json`):
- 1,852 base rows: **1,136 choice (61.3%) and 716 yes/no (38.7%)**. Every yes/no task is exactly 50/50.
- 13 tasks and 1,806 groups.
- 284 base rows have more than 26 options (40 each).
- Halves: A 957 and S 895 base rows.
- 2,456 rows and 2,456 calls, one row per call.
- Twins:
  - 300 complement twins, 60 per yes/no task (136 clause-negated, 164 from templates T1-T6);
  - 304 permutation twins, 38 per choice task (149 reversed, 155 rotated).

**Track split** (derived from the PREREG task table):

| | Choice | Yes/no | Total |
|---|---|---|---|
| Track F | 568 | **519** | 1,087 |
| Track U | 568 | 197 | 765 |

**Comparison with the earlier exams:**

| | yes/no share | Yes/no rows on the fresh-text track F |
|---|---|---|
| OHS-1 | 28.5% (527 / 1,847) | **0** |
| OHS-2 | 27.3% (360 / 1,320) | **0** |
| OHS-3 | 38.7% | 519 |

**There is no evidence for our yes/no against Jev on fresh text.** Every earlier yes/no gap was measured on classic-corpus (U) or natural-negation (C) tasks.

**OHS-3's yes/no tasks** are definition-based label checks: interventional study, 21 CFR Class I, CVSS AV, DataCite type, CNC causal. There are no moral or table tasks (audit, yesno area, claim 6).

---

## 15. Decomposition of Jev's lead

**OHS-2, v11c primary configuration** [R]:

| | Value |
|---|---|
| Jev's lead | +1.63 pp |
| From yes/no rows | +1.97 (gap 7.22 × share 0.273) = 121% of the lead |
| From choice rows | −0.34 (gap −0.47 × share 0.727); choice slightly favours us |
| With BC (secondary configuration) | lead 1.02 = yes/no +1.97, choice −0.95 |
| v10 on OHS-2 | lead 3.30 = yes/no +2.42 (73%), choice +0.87 (27%) |

**Per-task contributions** to v11c's OHS-2 gap (pp of micro; positive = Jev better):
- **Yes/no tasks:**
  - moral_stories +1.14 (task gap 12.5);
  - tabfact +0.76 (gap 8.3);
  - ibm_argq +0.08.
- **Choice tasks:**
  - scifact +0.64;
  - pubmed_rct +0.38;
  - big_patent +0.15;
  - arxiv math / astro +0.15 each;
  - evidence_inference 0;
  - stat_eess −0.08;
  - medical_abstracts −0.30;
  - arxiv_cs −0.30;
  - **ddi2013 −1.14**.

**By track** [R]:

| Exam | Track and type | n | Ours − Jev [95% CI] |
|---|---|---|---|
| OHS-2 | F, all choice | 240 | **+0.42 [−3.96, +4.79]** |
| OHS-2 | U, yes/no | 360 | −7.22 [−10.56, −3.75] |
| OHS-2 | U, choice | 720 | +0.49 [−1.67, +2.71] |
| OHS-1 | F, all choice | 240 | **−0.42 [−4.58, +3.75]** |
| OHS-1 | U, all | 1,102 | −4.76 [−6.76, −2.77] (yes/no −11.14, choice −3.33) |
| OHS-1 | C, all | 505 | −2.67 [−6.14, +0.69] (yes/no +0.31, choice −8.06) |

On fresh text we tied Jev on both exams.

**OHS-1, v11c, for contrast** [R]:
- Lead 3.63 = yes/no +1.16 (32%) + choice +2.46 (68%). On OHS-1 **the choice gap dominates**.
- Top contributors: legalbench_hearsay +1.30, vitaminc +0.84, scone +0.79, go_emotions +0.35, abercrombie +0.27, hatecheck +0.24.
- We gain on this_is_not_a_dataset −0.30, condmat −0.24 and overruling −0.11.
- So the claim that "the gap to Jev is yes/no only" holds on OHS-2 only (skeptic, win area).

**EST: reweighting to the OHS-3 mix, for a v11c-class model** (illustration, not a forecast):
- OHS-2 per-type gaps × OHS-3 shares: 0.387 × (−7.22) + 0.613 × (+0.47) = **−2.5 pp**.
- OHS-1 per-type gaps: 0.387 × (−4.08) + 0.613 × (−3.45) = **−3.7 pp**.
- Track-based (F ≈ 0; U −2.1 to −4.8; F share 58.7%): **−0.9 to −2.0 pp**.
- Range for v11c: −0.9 to −3.7.
- Add 4B-E's EST held-out gain over v11c (+0.3 to +3.3, §12). This gives about **−3.4 to +2.4 pp for 4B-E vs Jev on OHS-3 micro**. The PREREG "matches" bar is a lower bound above −2.0.

---

## 16. Estimates made by others (for reference; not evidence)

- **Audit "honest odds"** (`wnzbuj8i0.output` verdict):
  - accuracy ≥ Jev 30-45%;
  - yes/no ≥ Jev 20-50%;
  - Brier 15-30%;
  - consistency 35-55%;
  - hijack > 90%;
  - OPI: the 4B ties, the 2B is worse;
  - speed (median) 70-85%;
  - cost likely;
  - JevBench public 65-80%;
  - all at once about 5-10%.
- **Status PDF p.5-6** (`reports/OpenDecide_Status_30Sep.pdf`):
  - security, speed and cost 90-95%;
  - multiple choice 75-80%;
  - JevBench and consistency 55-65%;
  - overall accuracy about 50%;
  - fully closing yes/no 10-15%;
  - every metric 15-25%.
  - Its "MC tie" line cites OHS-2 only; on OHS-1, choice was −3.45.
- **Yes/no research verifier** (`wfjjlksu2.output`, ver section 5): the planned fixes recover 1-3 of the 7.5-point OHS-2 yes/no gap, and about 0 on OHS-3.

## 17. Not measured (gaps in the evidence)

1. 4B-E, the new 4B, the final 2B and the cascade have **no held-out (OHS-1/2) numbers**.
2. Jev has **no dev numbers**. Jev was **never run on eval_redef**.
3. **Option-order drift** has never been measured for any system.
4. **Yes/no accuracy against Jev on fresh-text (track F) tasks** has never been measured.
5. **Speed and cost have no OHS-3 definition.** None of these was ever timed end to end:
   - layout E;
   - the PRISM-X 2B on an H100;
   - the cascade.
6. **Real serving cost** has never been measured.
7. **Cascade ASR and routed fraction under attack** have not been measured.
8. **Security evals are not held out:** jagged and OPI were used for selection.
9. **Yes/no accuracy is not an OHS-3 endpoint.** It is visible only through Brier and the per-task secondaries.
10. **`score_ohs.py` does not match PREREG_OHS3:**
    - complement is scored as a mean of |pa + pb − 1|;
    - missing answers are skipped;
    - there are no consistency CIs and no BH correction;
    - the Brier sign is flipped.

    See the audit, win area.
