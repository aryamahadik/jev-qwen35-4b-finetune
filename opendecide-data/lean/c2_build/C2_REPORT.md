# C2 report, final (Sun 18 Oct 2026, US Eastern times)

**Verdict: C2 does NOT ship. C1 stays.** The one OHS-4 look failed three of the six ship rules (spec 7.3 needs all six): **S1** (rule/agent part: +1.93 pp [+0.07, +3.82], the bar is +5.0 pp), **S3** (complement pairs: upper bound +2.08 pp, the bar is under +1.0 pp) and **S4** (Brier +0.0098, the bar is +0.005). S2 (general text), S5 (security) and S6 (dev pre-gate) passed.

**Jev 1.13 is ahead of both C1 and C2.** On the rule/agent part Jev leads C1 by 8.6 points and C2 by 6.7 points; on general text it leads both by about 2.1 points (one Jev read). C2 closed 1.9 points of the 8.6-point rule/agent gap and did not beat Jev anywhere on accuracy.

**OWNER OVERRIDE (A100), disclosed first.** After seeing the result, the owner waived pre-gate check (b), the transfer rule. Verbatim, 3:20 PM ET: *"I waive pre-gate (b), the transfer rule, after seeing the result. Put the chosen C2 candidate into the one OHS-4 look together with C1, and disclose this override in the report."* Check (b) **still failed**: for the chosen candidate final_a10, transfer dev C2 minus C1 was **-4.83 pp [-8.59, -1.02]** (n 600; bar +3.0 pp with LB above 0), and all 18 candidates failed it (best -1.33 [-4.26, +1.62], highest upper bound +1.65). Without the waiver C2 would have had no OHS-4 look (A98/A99). The waiver let C2 take its look; it did not change any ship rule, and C2 then failed the look.

Times are US Eastern (EDT, UTC-4); UTC in brackets where a record uses it. The binding spec is `teach1/C2_DATA_SPEC.md` (sha256 245ba9f9..., A37 (a)); "spec 7.3" means its section 7.3. Every number comes from files in this tree; `c2_build/C2_RESULTS.json` holds each one with n and CI, the spend, the shas and the timings. Records: PREREG A104 (L1) and A105 (J).

---

## 1. The ship rules on OHS-4 (L1, one look, 4:46 PM ET)

C1 and C2 (final_a10) were read in one H100 job on the frozen OHS-4 (run `l1_1018_2034`), scored by the frozen scorer with paired bootstrap, 10,000 resamples, seed 0, over group_id. Spec 7.3: C2 replaces C1 only if every rule holds.

| Rule | Measure | C1 | C2 | C2 minus C1 [95% CI] | Bar | Result |
|---|---|---|---|---|---|---|
| S1 | Part R, rule/agent accuracy (n 1,454; 1,406 groups) | 67.40% | 69.33% | **+1.93 pp** [+0.07, +3.82] | >= +5.0 pp and LB > 0 | **FAIL** |
| S2 | Part G, general accuracy (n 2,883; 2,614 groups) | 77.84% | 77.84% | 0.00 pp [-0.76, +0.80] | LB > -1.5 pp | PASS |
| S3 | Complement violation, 383 R-based pairs | 8.62% | 7.31% | -1.31 pp [-4.69, +2.08] | C2 <= C1 (point) and UB < +1.0 pp | **FAIL** (point passes; UB +2.08) |
| S4 | Binary Brier, yes/no items of G, R, X (mixdev T) | 0.1809 | 0.1907 | **+0.0098** | <= +0.005 | **FAIL** |
| S5 | OPI attack success, part X (281 pairs) | 1.04% | 0.52% | -0.52 pp | <= max(C1 + 2 pp, 3%) = 3.04% | PASS |
| S6 | Dev pre-gate (c1)-(c7) still pass | | | | not re-read | PASS ((b) waived, A100) |

**Report-only (never decisive):**
- **Calibration, ECE yes/no on G+R+X: C1 4.1% vs C2 13.2%.** C2 is much more over-confident on independent data.
- S1 without the r20 kind (96 items excluded, n 1,358): +2.14 pp [+0.22, +4.05], still under +5.0.
- Other parts: U (n 433) 59.58% -> 61.66%, +2.08 [-1.62, +6.00]; X (n 562) 69.40% -> 68.51%, -0.89 [-5.16, +3.20]; headline G+R+X (n 4,899) 73.77% -> 74.24%, +0.47 [-0.39, +1.32].
- Consistency calls: complement violation 8.11% for both (444 pairs); option-order drift C1 3.82% vs C2 6.11% (262 pairs); minimal-edit consistency C1 38.9% vs C2 39.4% (175 pairs).
- **Frozen temperatures T** (fitted on the C2 mixdev rows of the 18 trained families, 2,795 rows; groups = sampler + pack + register; median-group NLL; clip [0.8, 1.3]; frozen 4:46 PM ET before the sealed read, sha 5d46b91f...): C1 yes/no **1.3** (raw 1.4, clipped), choice **1.25**; C2 yes/no **0.8** (the clip floor), choice **0.95**.
- Attack detail: clean-right pairs C1 192, C2 191 of 281. Scorer cross-check: no differing part.

S3 note: only R-based complement pairs exist in scope (383); there are no G-based pairs, and 61 pairs with a U base are out of scope (RULING_L1_PRELOOK item 4).

## 2. Against Jev 1.13 (J, one read, 5:21 PM ET; report-only)

Jev was read once (6,213 of 6,213 calls answered, one served id `typesafe/jev-1.13-20260917`, $0.17). Spec 8.6 asks for two pinned Jev runs; only one read is allowed (A37 h, A38, A42-D 13.8), so every claim line rests on one run.

| Part | n | Jev 1.13 | C1 | C2 | C1 minus Jev [CI] | C2 minus Jev [CI] |
|---|---|---|---|---|---|---|
| R, rule/agent | 1,454 | 76.00% | 67.40% | 69.33% | **-8.60** [-11.11, -6.18] | **-6.67** [-9.08, -4.27] |
| G, general | 2,883 | 79.95% | 77.84% | 77.84% | -2.12 [-3.57, -0.66] | -2.12 [-3.56, -0.66] |
| U, unseen kinds | 433 | 64.20% | 59.58% | 61.66% | -4.62 [-10.39, +0.92] | -2.54 [-7.85, +2.77] |
| X, security | 562 | 73.84% | 69.40% | 68.51% | -4.45 [-9.79, +1.07] | -5.34 [-10.68, -0.18] |
| G+R+X headline | 4,899 | 78.08% | 73.77% | 74.24% | -4.31 [-5.58, -3.02] | -3.84 [-5.12, -2.57] |

**Plainly: Jev 1.13 is ahead of C2 on the rule/agent part by about 7 points (C1: about 9) and on general text by about 2 points.** Spec 8.6 claim lines, for C2:
- "Beats Jev on rule/agent": **no** (-6.67; the LB is -9.08).
- "Also on unseen kinds": **no** (-2.54 [-7.85, +2.77]; C1 -4.62).
- "Better calibrated": **no.** Jev's binary Brier is lower on G, R and X (C2 minus Jev +0.028, +0.063, +0.048, CIs exclude 0); no difference on U (-0.020 [-0.047, +0.007]). C1 minus Jev: G +0.008 (no difference), R +0.066, X +0.036.
- "More consistent": **yes, on two measures, for C1 and C2 alike.** Complement violation Jev 12.39% vs C1 and C2 8.11% (C2 minus Jev -4.28 pp [-7.92, -0.67]); option-order drift Jev 13.36% vs C1 3.82% and C2 6.11% (C2 minus Jev -7.25 pp [-12.21, -2.29]). On minimal-edit consistency Jev is ahead (49.7% vs 38.9% and 39.4%).
- "Close to Jev on general": the pre-registered test (the CI of C2 minus Jev on G includes -2 pp) is met, but the gap is a real 2.1 points, the same for C1; this is not a C2 gain.
- Speed and cost: **not evaluated** (SPEED-3 was not run).
- No JevBench submission and no general-win claim.

## 3. How the result moved (history, kept for the record)

1. **6:30 AM ET, first stop.** The H100 grid launch was denied by the permission classifier and was not retried or worked around. (Kept as `C2_REPORT_STOPPED_0630ET_20261018.md`.)
2. **Grid reads.** C1 and final_a10 were first read on the free L4 (A90); on the owner's A91 "do it" all 19 models were read on one H100 job (12:15-1:34 PM ET).
3. **A98 (about 3:05 PM ET): NO CANDIDATE.** Every candidate failed (b); by A42-D 9.5 and spec 7.2 the pre-gate failed and C2 would have had no OHS-4 look. Kept as `CHOSEN_A98_NOCANDIDATE.json` (sha256 54ba8937...). 13 of 18 failed (b) only; the other five (last3_a05, last3_a10, earlylate_a08/09/10) also failed D9, D3, D1 or D2.
4. **A99.** Three verifiers and an Opus judge reproduced the numbers from the raw predictions, matched the rule to the code and checked the transfer set (T19 + T21, no leak): NO CANDIDATE STANDS.
5. **A100 (3:20 PM ET): the owner waived (b).** **A101 (3:58 PM):** `select_candidate` (run once, under the waiver) picked final_a10; parity, the official read copy and the pre-gate followed (section 6).
6. **A103 (4:34 PM):** after the Opus pre-look ruling and two runner skeptics, L1 was launched once. **A104 (4:46 PM):** L1 verdict, C2 fails S1, S3, S4. **A105 (5:22 PM):** J scored once (the first J pass refused itself on a pin string before any look; ruling 6b).

## 4. What was trained

Training ran on mahadikarya2 free credit only (no relay; the card was never used).

| Item | Value |
|---|---|
| Start | C1 adapter `q35_4b_main500k` (sha 507d1c29...), base Qwen3.5-4B @ 851bf6e8 |
| Recipe | Round-1 recipe unchanged: LoRA r16 / alpha 32, lr 5e-5 cosine, batch 16, one pass (epochs 0.9901), KD 0.5 on replay, lam_ord 1.0 (14 ordinal rows), seed 20261013 |
| Rows | 59,340: 23,736 new + 35,604 replay. Relations 8,690 (complement 4,382, equiv 1,442, inv 2,866) |
| Loss | first-5 mean 0.529, last-10 log-point mean 0.301, final step 0.226; no non-finite total or task loss |
| Speed and cost | 3,673 steps in 186.0 min, about 3.04 s/step (round-1 reference 3.716). $13.14 against T_max $22.96 |

New rows per block (18 blocks entered): T28 2,247, T29 2,000, T30 1,400, T26 1,398 (agent core, 4 of 6); T31 999, T01 1,600, T23 794, T06 600, T15 900, T25 600 (other program families, 10 in all); F5 1,362, F6 930, F11 552, F4 500; GB 3,376, GW 3,696, I10 100, SB5 682.

**Left out, and why**

| Left out | Reason (ruling) |
|---|---|
| T33, T12, T24 | The faithful A69 repair and (f)(ii) refuse their selections, so (f)(iii) leaves them out (A78 finding, A80 owner ruling). Their mixdev rows are report-only, "family not trained in C2" |
| T27, RTW | QC record not passed |
| T07 | 1 confirmed wrong gold = a generator bug (A72) |
| T32 | Binding G13 drops removed every equiv twin (A71 a) |
| T35, T37b, T46 | Moved to C3 (A65, A52 a, A67) |
| T40-T45 | No candidates on disk by the new-family deadline (A42-D 13.1) |
| MD | 3 sources were 8.5 HITs; MD fell under the A42-D 8.2 floor and was removed whole (A61 f, A73) |
| DI blocks, item 10 | No DI block enters C2 (A61); item 10 (Opus distillation) not built for C2 |

## 5. Forgetting monitor (old slice, 2,000 replay rows, C1 = 92.15%; monitors only, never candidates)

| Snapshot | Step | C2 minus C1 | P(yes) drift | KL(C1 to snap) | Flags |
|---|---|---|---|---|---|
| 25% | 918 | -1.80 pp | -0.0013 | 0.044 | none |
| 50% | 1,836 | -1.15 pp | +0.0002 | 0.030 | none |
| 75% | 2,754 | -0.50 pp | +0.0042 | 0.028 | none |

The A37 (k) stop rule fires only if the old slice is below -1.5 pp at both the 25% and the 50% snapshot. It did not fire.

## 6. The grid, the choice, parity, the official reads and the pre-gate

### 6.1 Grid and reads
`merge_avg.py` built 18 candidates in merged-weight space: final step, last-3 average, early+late average (early = s001212), each at alpha 0.5-1.0. Recorded at 6:26 AM ET, before any read: grid_sha256 `ef77658b420952c47a75c4fe1e8a949e0940cd37385fee8453beab1a44f85725`. One H100 session (`grid_1018_1215`, 5,877 s, $7.49) read C1 and all 18 on the same SGLang S1 path (bf16 merged, fp32 LM head), 26,191 rows each, plus a batch-1 latency run per model. 19 of 19 completed.

### 6.2 Choice (A101)
Under the waiver 13 candidates were eligible (those failing only (b)). A42-D 9.5 chose **final_a10**: "final step is the highest-S eligible candidate" (S 89.4671 = mean of G-proxy 98.684 and mixdev 80.25; last3_a09 has the same S, and the tie order puts the final step first; its S gain over the final step is 0.00 pt [-0.24, +0.23]). CANDIDATE_C2.json sha256 `86ce1de4...`, CHOSEN.json sha256 `4826448f...`; `grid_plan candidate-check`: OK_BEFORE_READS.

### 6.3 Parity and official reads
- **Parity (4:05 PM ET, H100, parity_1018): PASS.** n 2,000 rows of the G-block; argmax agreement 99.9% (2 disagreements; bar 99.5%); |change in label probability| <= 0.02 on 99.0% of rows (bar 99%: exactly at the bar); adapter sha held to CANDIDATE_C2.json. Record `c2_build/train/PARITY_final_a10.json` (sha256 95f0a220...). Cost $0.52.
- **Official reads (4:06 PM ET).** Per A97 (2) the 48 files of final_a10's grid read were copied byte for byte to the `q35_4b_c2` names, after CANDIDATE_C2.json. No prediction value and no meta field was changed. Record `OFFICIAL_READ_COPY_A97.json` (sha256 6c5dabb1...).

### 6.4 Pre-gate (official, logged 4:07 PM ET)
Decision: **"PRE-GATE PASS: every check (a)-(d) passes except (b), failed and waived by the owner (PREREG A100); C2 gets its one OHS-4 look."**

| Check | Result | Verdict |
|---|---|---|
| (a) learning, trained-family mixdev | 80.25 vs 67.94: +12.31 [+10.47, +14.15] (n 2,795) | PASS (bar +8.0, LB > 0) |
| (b) transfer dev (T19 + T21) | 64.33 vs 69.17: -4.83 [-8.59, -1.02] (n 600) | **FAIL, waived by the owner (A100)** |
| (c1) D1 full dev (n 7,056) | -0.60 [-1.31, +0.15] | PASS (LB > -1.5) |
| (c2) D2 unseen sources (n 3,847) | -0.78 [-1.68, +0.11] | PASS |
| (c3) D3 yes/no, choice | 84.85 vs 85.21 (-0.36); 75.26 vs 76.14 (-0.88) | PASS (each >= C1 - 1.0) |
| (c4) D4 calibrated Brier | 0.1116 vs 0.1099: +0.0017 | PASS (<= C1 + 0.005) |
| (c5) D5 flips | equivalence 5.68% vs 9.00%; permutation 2.91% vs 2.52% | PASS |
| (c6) D6 attacks | jagged 0.0% vs 0.0%; OPI 0.4% vs 1.3% | PASS |
| (c7) D9 latency p50 | 30.9 vs 31.6 ms | PASS (<= 1.05x) |
| (d) complement violation | 0.0446 vs 0.0462 (-0.0016 [-0.0111, +0.0085]) | PASS (C2 < C1) |

Report-only: over-ask on mixdev 2.9% (C1 22.0%); ECE yes/no 0.0296 (C1 0.0261). The reference check (refparity) was accepted by the owner (A95), see section 12.

## 7. Dev results for all 18 candidates (every candidate vs C1, same job)

(a) needs +8.0 pp with LB > 0 on the mixdev rows of trained families; (b) needs +3.0 pp with LB > 0 on the transfer dev. Dev CIs: 10,000 paired group-bootstrap resamples, seed 0. "Failed checks" shows what failed before the waiver.

| Candidate | S | (a) mixdev gain [CI] | (b) transfer gain [CI] | D1 full dev [CI] | G-proxy gain | D9 p50 ratio | Failed checks |
|---|---|---|---|---|---|---|---|
| final_a10 | 89.47 | +12.31 [+10.47, +14.15] | -4.83 [-8.59, -1.02] | -0.60 [-1.31, +0.15] | +1.35 | 0.979 | b_transfer |
| final_a09 | 89.35 | +12.16 [+10.36, +13.97] | -4.17 [-7.86, -0.50] | -0.54 [-1.22, +0.17] | +1.25 | 0.959 | b_transfer |
| final_a08 | 89.35 | +12.16 [+10.41, +13.93] | -2.83 [-6.44, +0.81] | -0.37 [-0.99, +0.27] | +1.25 | 0.969 | b_transfer |
| final_a07 | 89.23 | +12.06 [+10.37, +13.75] | -3.00 [-6.40, +0.34] | -0.24 [-0.82, +0.35] | +1.13 | 0.902 | b_transfer |
| final_a06 | 88.56 | +10.95 [+9.35, +12.60] | -2.67 [-5.95, +0.64] | -0.16 [-0.69, +0.39] | +0.89 | 0.886 | b_transfer |
| final_a05 | 87.71 | +9.55 [+8.06, +11.10] | -1.33 [-4.26, +1.62] | +0.04 [-0.44, +0.53] | +0.58 | 0.804 | b_transfer |
| last3_a10 | 89.39 | +12.24 [+10.40, +14.09] | -4.50 [-8.33, -0.68] | -0.58 [-1.29, +0.15] | +1.25 | 1.075 | b_transfer, c3_D3, c7_D9 |
| last3_a09 | 89.47 | +12.31 [+10.53, +14.11] | -4.17 [-7.85, -0.50] | -0.47 [-1.14, +0.24] | +1.35 | 0.847 | b_transfer |
| last3_a08 | 89.38 | +12.16 [+10.42, +13.91] | -2.50 [-6.14, +1.13] | -0.40 [-1.02, +0.25] | +1.32 | 0.956 | b_transfer |
| last3_a07 | 89.26 | +12.13 [+10.46, +13.82] | -2.83 [-6.29, +0.66] | -0.24 [-0.82, +0.35] | +1.10 | 1.002 | b_transfer |
| last3_a06 | 88.61 | +10.98 [+9.39, +12.63] | -2.67 [-5.95, +0.64] | -0.21 [-0.75, +0.33] | +0.95 | 1.044 | b_transfer |
| last3_a05 | 87.78 | +9.70 [+8.21, +11.23] | -1.33 [-4.30, +1.65] | +0.07 [-0.42, +0.57] | +0.58 | 1.092 | b_transfer, c7_D9 |
| earlylate_a10 | 89.22 | +11.88 [+10.09, +13.65] | -4.83 [-8.82, -0.95] | -1.15 [-1.86, -0.43] | +1.29 | 0.843 | b_transfer, c1_D1, c2_D2, c3_D3 |
| earlylate_a09 | 89.19 | +11.81 [+10.07, +13.53] | -5.00 [-8.91, -1.15] | -0.96 [-1.63, -0.28] | +1.29 | 0.835 | b_transfer, c1_D1, c2_D2, c3_D3 |
| earlylate_a08 | 89.20 | +11.84 [+10.16, +13.54] | -4.67 [-8.43, -1.01] | -0.64 [-1.24, -0.03] | +1.29 | 0.882 | b_transfer, c3_D3 |
| earlylate_a07 | 88.72 | +11.02 [+9.39, +12.67] | -3.50 [-7.05, +0.00] | -0.43 [-0.96, +0.13] | +1.13 | 0.850 | b_transfer |
| earlylate_a06 | 88.36 | +10.55 [+9.01, +12.14] | -3.50 [-7.08, +0.00] | -0.28 [-0.79, +0.24] | +0.89 | 0.973 | b_transfer |
| earlylate_a05 | 87.61 | +9.30 [+7.83, +10.80] | -2.17 [-5.53, +1.14] | +0.06 [-0.40, +0.53] | +0.64 | 1.024 | b_transfer |

S is the mean of G-proxy and mixdev accuracy (no new-family dev split entered C2). The G-proxy carries the label "A42-D 12.2 unmet" (A61 f).

Two dev figures appear and both are right: **pooled, 8,143 rows over the 9 dev splits: -0.48 [-1.14, +0.16]** (the plain accuracy gap) and **the D1 check, n 7,056 (the pooled set without tb_mixtral): -0.60 [-1.31, +0.15]**. Both pass D1.

**Final step (alpha 1.0) vs C1, per dev split (pp):** dev_nc -1.59, taskbank_dev +0.42, hard_dev +0.96, dev_negwords +0.75, dev_claims -0.93, pg_dev -1.72, devzs -1.62, devp_card -0.17, dev +0.83. Unseen-source primary set -0.78 [-1.68, +0.11] (n 3,847).
**Alpha 0.5 vs C1:** dev_nc -0.10, taskbank_dev 0.00, hard_dev +0.96, dev_negwords +1.62, dev_claims -0.40, pg_dev -0.57, devzs -0.88, devp_card +0.23, dev +0.33. Pooled +0.05 [-0.39, +0.48].

**Trained families, mixdev gain (final step):** T28 +28.0, T30 +27.3, T31 +24.7, T06 +24.0, T25 +22.7, T29 +14.7, T23 +12.7, F4 +12.0, T01 +11.3, F6 +9.9, T26 +8.0, T15 +6.7, F11 +6.5, F5 -1.0. Families that left the mix, report-only: T33 +2.1, T24 -1.3, T07 -4.0, T12 -4.7.

## 8. Why (b) failed, and what the T19 loss looks like

- **The transfer dev.** T19 (300 rows) + T21 (300 rows) = **600 rows**, `data/c2_transfer_dev.jsonl`, sha256 `2b9702a7eb68d56901e4a37e46a56399672a600fde5706ad0572489fac9af93e`, built 16 Oct at 7:50 AM ET (11:50 UTC), before any read. The spec's section 7.1 lists four families (T36, T19, T21, T20; 1,200 rows); T20 and T36 were left out under A45 (c) after failing G6 (A50). **No PREREG record names this 600-row set**; the GO #1 draft says only "600 transfer rows" and that (b) has little power. (b) has low power at n 600, but the failure does not depend on power: all 18 point estimates are negative and the highest upper bound is +1.65, below +3.0.
- **By family, final step:** T19 51.7% vs C1 63.0% = **-11.3 pp** [-17.2, -5.6] (n 300); T21 77.0% vs 75.3% = +1.7 pp [-2.7, +6.0]. T19 loses 7.0 to 16.3 pp on every candidate; T21 gains 1.7 to 6.7. Dropping T21 would make (b) worse.
- **T19 diagnosis (orchestrator dev analysis; I re-derived the same totals, 63.0 / 51.7, from the dev files).** T19 is the compliance-checking family. On its 98 verdict questions (gold: Compliant 39, Non-compliant 33, "Cannot be determined from the records" 26) C2 answers "Cannot be determined" on **76** (truth 26; C1 54). Recall on the gold "Compliant" items falls from 30.8% (C1) to **7.7%** (C2); on "Non-compliant" 63.6% to 48.5%. The pick-the-failing-item questions (n 57) lose **-15.8 pp** and the yes/no questions (n 145; 64.8% to 55.2%) **-9.7 pp**. The pattern reads as over-abstention on an unseen family; it is a dev observation, not a causal test.
- The trade between trained-family gain and transfer is nearly linear in alpha (mixdev +9.55 and transfer -1.33 at alpha 0.5; +12.31 and -4.83 at alpha 1.0). Blending toward C1 cannot reach the +3.0 bar.

## 9. What did not run

- **SPEED-3** (the load test for p50/p95/p99 and $/1K) was not built before the one-shot final, and A42-D 2.3 allows it only in full or not at all. No speed or cost claim against Jev. Earlier C1 numbers (C1 fast path p50 14.1 ms on H100; about $0.079 per 1K requests at the S1 arm) are from SPEED-2, not new, and not an OHS-4 measurement.
- **Symmetrisation** (A42-D 10) was **not evaluated** (A97 3).
- The pre-registered second Jev run of spec 8.6 does not exist (one Jev read only).

## 10. Spend

| Line | USD | Account |
|---|---|---|
| Training | 13.14 | mahadikarya2, free credit |
| Grid reads (19 models, one H100 session) | 7.49 | mahadikarya3 |
| H100 parity (final_a10) | 0.52 | mahadikarya3 |
| L1 (C1 + final_a10, one H100 job) | 0.85 | mahadikarya3 |
| **C2 Modal total, ledger basis** | **21.99** (the rounded lines above sum to 22.00) | cap $40 (A42-D 2.1) |
| J: one Jev 1.13 read via OpenRouter | 0.17 (the API usage-sum field reads 0.18) | OpenRouter, not Modal |
| **All C2 lines incl. OpenRouter** | **22.16** | |

The post-training H100 ledger is **$8.85 of the $15 cap** (A88; stop-launch 13.50). Modal's billing delta since the preflight is $22.57 so far ($13.25 on mahadikarya2, $9.32 on mahadikarya3); **billing lags, so the billing-basis total is pending** and may read a little above the ledger. `c2_check.py status` shows "training 22.57" plus "other 8.86": it counts the H100 lines twice (billing delta plus the hand-logged spend), so its "C2 total $31.43" is an over-count; the true total is about $22 against the $40 cap. `c2_check spend` logs only the relay accounts, so the OpenRouter $0.17 is recorded in A105 and `J_RESULT.json` only. The card was never used; nothing went to aryamhd.

## 11. Lessons for C2.1

1. **Transfer and over-abstention (T19).** The loss on the unseen family is concentrated in one behaviour: on T19's 98 verdict questions C2 says "Cannot be determined" 76 times (truth 26; C1 54), and Compliant recall falls from 30.8% to 7.7%. C2.1 needs a per-family transfer table, including the abstention share, at every checkpoint, and held-out families in its transfer dev from the start (the set used here had two families and 600 rows).
2. **Calibration.** ECE 13.2% vs 4.1% and S4 +0.0098. The temperature was fitted on rows of families C2 trained on, where it is most accurate (C2's yes/no T hit the 0.8 floor), and then applied to independent data, where it is over-sharp (a reading, not a tested cause). The scorer's 2-class Brier is worst on the card-carrying G rows (0.4326 vs 0.3654 for C1). C2.1 should fit T on held-out sources and report ECE as a gate-side check, decided before the data freeze.
3. **The part-R gap to Jev.** Jev leads C1 by 8.6 points. A +12.3 pp gain on trained-family dev became +1.93 pp on OHS-4's independently generated R items, and C2 recovered only 22% of the gap. Program-made rows taught the formats of their own generators more than the skill; matching Jev on R needs about +8.6 points over C1, and S1 needs +5.0.
4. **Options the evidence points to** (owner's call; none is started): **real data**, meaning public train splits and real-text rows under the A82 release rules instead of program-made rows; **anti-shortcut checks**, extending the plan's style-only baseline with an abstention-prior check; **early-warning monitors**, with per-family transfer, abstention share and ECE read at every checkpoint and a stop rule; and **RL with verifiable rewards**, which the C2.1 plan lists as not adopted (C3), with this result as evidence to weigh.
5. **R14 init, with numbers.** The written rule has three branches: C2 ships (init C2); C2 fails only the Jev-beat gate S1 but passes its G floor and non-regression gates (init = C2's unshipped weights); C2 fails its G floor or a non-regression gate (init C1). C2 fails S1, S3 **and** S4 (not S1 alone), and S4 is a calibration non-regression gate (+0.0098 against +0.005 allowed); the G floor (S2, 0.00 [-0.76, +0.80]) and S5 pass. Read as written, the branch is **init = C1**. The final R14 answer is the owner's.
6. **Process.** Read the stored reference on the same path as the candidates; record the transfer set's composition in PREREG before training; wire an owner acceptance into the tools before the reads, not after (A96, A100).

## 12. Deviations, rulings and disclosures, in order

1. **A100 (OWNER OVERRIDE, first).** (b) waived after the result; see the first lines. The hook (`waiver_a100.py`, `WAIVER_B_A100.json`, changes to `select_candidate.py` and `gate_c2.py`; 38 + 7 new tests) passed a 3-lens skeptic (all SOUND). Minor items found and left unchanged: (i) the waiver's PREREG search window is not bounded to the A100 block; (ii) the OWNER_GO line check is an unanchored substring match; (iii) the waiver is not bound to the C2 run id; (iv) CANDIDATE_C2.json carries no waiver flag; (v) the L1 helper `l1common.load_waiver_b` is looser than `waiver_active`.
2. **A96 hook.** After A95 the tools refused the one failed refparity look, so `gate_dev.py` and `gate_c2.py` were edited **after the reads** to accept that one named look only (full A95 sentence, look sha, n and max_dp pinned in code; read files re-hashed). 123 tests; three skeptics reviewed it, the conformance skeptic found one defect (the quote was checked as a substring), fixed and re-checked.
3. **L1 runner.** Two independent skeptics reviewed it before the look: rule conformance SOUND; one-look safety NOT SOUND on two items, which were fixed and re-checked SOUND (A103). The Opus pre-look ruling (`RULING_L1_PRELOOK.md`, 3:50 PM ET, before any OHS-4 read) fixed T, the binary Brier for S4, the OPI definition for S5, the complement pairs for S3, the single Jev read, the Jev pin and SPEED-3.
4. **J pin refusal and ruling 6b.** The first J pass (4:50 PM ET) refused itself before any look: its guard compared the bare string `jev-1.13` with the served id `typesafe/jev-1.13-20260917`. Opus ruling 6b held that id IS the pinned Jev 1.13; `j_run.py` pins it exactly; the frozen runner was not edited; the not-run record is kept as `J_RESULT_NOTRUN_2050Z.json`; the same single read was scored once, no call re-sent. The records cannot show which snapshot the alias resolved to on 13 Oct; the comparator is Jev 1.13, not 1.14.
5. **One Jev read; $0.17.** See section 2.
6. **SPEED-3 not run; symmetrisation not evaluated.** See section 9.
7. **S3 scope.** R-based pairs only (383); no G-based pairs exist; 61 U-based pairs out of scope.
8. **A78 / A80:** the selection code that built the C2 records was not the adopted A69 text. The owner set the agent core to 4 of 6 for C2 only ("ok go with b"). T33, T12, T24 left out.
9. **A84:** one re-run of the A61 (f) 8.5 check, same tool and input. **A85:** the first launch crash-looped on a path bug (zero steps, about $0.0002), fixed, relaunch approved. **A86 / A87:** the first100 guard aborted by mistake (JSON null counted as non-finite); fixed, reviewed, owner approved continuing.
10. **A88 / A91:** the first H100 grid launch (about 6:30 AM ET) was denied by the permission classifier and not retried; reads started on the free L4 (A90) and, on the owner's A91 "do it", all 19 models were read on an H100 (cap $15, payer mahadikarya3, never the card). **A93:** the 98 L4 read files for C1 and final_a10 were moved, not deleted, to `c2_build/_superseded_L4_reads_20261018/` so all 19 are H100 reads; no score had been computed.
11. **A94 / A95:** the pre-registered refparity look (fresh H100 C1 vs stored C1, n 8,143) failed one bar, max |dp| 0.1013 vs 0.05 (1 row; argmax 99.75%, mean |dp| 0.00198, accuracy +0.04 pp all passed). Logged at 1:49 PM ET as pass false and it stays so. The owner accepted it as serving-path noise.
12. **A97:** GO #2, reuse of the chosen candidate's H100 reads as the official reads (done, 48 files byte for byte), symmetrisation skipped. **A98 / A99 / A101:** see section 3.
13. **Pre-existing weakness found during A96:** `gate_dev.refparity_status` never stops on a failed look for a reference whose stored name is not its built-in one, so the PREREG section 4 ship-mode refusal was already weaker than written for C2. For C2, `gate_c2.check_refparity` was the only enforcement point and it did enforce.
14. **Transfer-set history:** T21 was admitted on a single-build G6 rather than the A50 average; T20 ran a third iteration although A48 (a) allows 2; no PREREG record names the 600-row transfer set. None of this changes the outcome.
15. **Other:** the T19 diagnosis is an orchestrator dev analysis (I re-derived the same totals from the dev files), not a pre-registered test. Parity passed with the within-0.02 share exactly at its 99% bar. **PREREG_FINAL.md is not committed in git.** Scout agents had accidental grep hits on sealed-side file names; no sealed content was read or used. The G-proxy is labelled "A42-D 12.2 unmet".

No bar, gate, seed, candidate rule or look rule was changed except the owner's explicit waiver of (b). No sealed or OHS path was opened by me; L1 and J ran through the pre-registered scorer and runner.

## 13. Where things are

`c2_build/C2_RESULTS.json` (all numbers); `c2_build/train/L1_RESULT.json` and `J_RESULT.json` (aggregates only); `L1_T_FROZEN.json`; `J_RESULT_NOTRUN_2050Z.json`; `c2_build/zed_orch/RULING_L1_PRELOOK.md`; `c2_build/train/CHOSEN.json` (A101) and `CHOSEN_A98_NOCANDIDATE.json`; `c2_build/CANDIDATE_C2.json`; `c2_build/train/WAIVER_B_A100.json`; `PARITY_final_a10.json`; `OFFICIAL_READ_COPY_A97.json`; `c2_build/logs/gate_c2_pregate_q35_4b_c2.json`; `c2_build/train/grid_reads/*.json`; `c2_build/logs/grid/ship_*.json` and `latency_*.json`; tool shas in `c2_build/zed_orch/a64/A64_TOOLS.md`. Earlier versions kept: `C2_REPORT_STOPPED_0630ET_20261018.md`, `C2_REPORT_DRAFT_A98_NOCANDIDATE.md`, `C2_REPORT_DRAFT_A101_PRE_L1.md`.
