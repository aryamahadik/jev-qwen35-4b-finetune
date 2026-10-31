# C2 report (Sun 18 Oct 2026, US Eastern times)

**OWNER OVERRIDE (A100).** After seeing the result, the owner waived pre-gate check (b), the transfer rule. Verbatim, 3:20 PM ET: *"I waive pre-gate (b), the transfer rule, after seeing the result. Put the chosen C2 candidate into the one OHS-4 look together with C1, and disclose this override in the report."* Check (b) **still failed**: for the chosen candidate final_a10, transfer dev C2 minus C1 is **-4.83 pp [-8.59, -1.02]** (n 600; the bar is +3.0 pp with LB above 0). All 18 candidates failed it: the best was -1.33 pp [-4.26, +1.62] (final_a05) and the highest upper bound was +1.65 (last3_a05). Without the waiver there was no eligible candidate and C2 would have had no OHS-4 look (A98/A99). With it, every other check, parity and the spec 7.3 ship rules bind unchanged.

**Status: DRAFT, updated about 4:15 PM ET. Open: L1 (C1 + final_a10 on OHS-4, S1-S6) and J (Jev once). Sections 8 and 9 are placeholders. The ship decision is undecided until they are logged.** Pre-gate result: **PASS except (b), failed and waived by the owner.**

Times are US Eastern (EDT, UTC-4); UTC in brackets where a record uses it. The binding spec is `teach1/C2_DATA_SPEC.md` (sha256 245ba9f9..., A37 (a)); "spec 7.2" means its section 7.2. All numbers come from files in this tree; `c2_build/C2_RESULTS.json` holds every number with n and CI, the spend, the shas and the timings.

---

## 1. At a glance

| Item | Result |
|---|---|
| Training | Done 6:24 AM ET. 3,673 steps, 186 min, 59,340 rows (23,736 new + 35,604 replay), **$13.14**, free credit only |
| Forgetting monitor (old slice, C2 minus C1) | -1.80 pp at 25%, -1.15 pp at 50%, -0.50 pp at 75%. Stop rule (below -1.5 at both 25% and 50%) did not fire |
| Grid | 18 candidates (3 bases x alpha 0.5-1.0), recorded 6:26 AM ET before any read; C1 + 18 read in one H100 job, $7.49 |
| Pre-gate (a) trained-family gain, chosen candidate | **+12.31 pp** [+10.47, +14.15] (n 2,795). Bar +8.0 pp: PASS |
| Pre-gate (b) transfer, chosen candidate | **-4.83 pp** [-8.59, -1.02] (n 600). Bar +3.0 pp, LB > 0: **FAIL, waived by the owner (A100)** |
| General dev accuracy, chosen candidate vs C1 | **Pooled, 8,143 rows over 9 splits: -0.48 pp** [-1.14, +0.16]. **D1 check (n 7,056, without tb_mixtral): -0.60 pp** [-1.31, +0.15]. Both pass |
| Every other pre-gate check | PASS (D1-D6, D9 latency 30.9 vs 31.6 ms, complement) |
| Candidate chosen (A42-D 9.5 under the waiver) | **final_a10**, the C2 final step, adapter 93aba519...; 13 candidates were eligible; S 89.4671, tied with last3_a09, tie goes to the final step |
| H100 parity (S1 vs HF adapter) | **PASS**: n 2,000, argmax 99.9% (bar 99.5%), within 0.02 on 99.0% (bar 99%, exactly at it) |
| Official pre-gate reads | The chosen candidate's H100 grid reads copied byte for byte to the `q35_4b_c2` names (48 files, A97 2) |
| L1 (OHS-4: C1 + final_a10 in one job) and J (Jev once) | **Pending** |
| Spend | Training $13.14 + grid $7.49 + parity $0.52 = **$21.15** (ledger basis; Modal billing basis $13.25 + $8.56 = $21.81). H100 post-training ledger **$8.01 of the $15 cap**. Cap on all C2 Modal lines $40 |

## 2. How the result moved (history, kept for the record)

1. **6:30 AM ET, first stop.** The H100 grid launch was denied by the permission classifier and not retried or worked around. Training was done and the 18 candidates were built and recorded. (The report of that stop is kept as `C2_REPORT_STOPPED_0630ET_20261018.md`.)
2. **Grid reads.** C1 and final_a10 were first read on the free L4 (A90). On the owner's A91 "do it" all 19 models were read on one H100 job (12:15-1:34 PM ET).
3. **A98 (about 3:05 PM ET): NO CANDIDATE.** `grid_elig` + `select_candidate` (run once, no waiver): every candidate failed (b); by A42-D 9.5 and spec 7.2 the pre-gate failed and C2 would have had no OHS-4 look. That output is kept as `CHOSEN_A98_NOCANDIDATE.json` (sha256 54ba8937...). 13 of 18 failed (b) only; the other five (last3_a05, last3_a10, earlylate_a08/09/10) also failed D9, D3, D1 or D2. An earlier draft of this report (kept as `C2_REPORT_DRAFT_A98_NOCANDIDATE.md`) stated that outcome.
4. **A99.** A 3-verifier workflow and an Opus judge reproduced the numbers from the raw predictions, matched the rule to the code and checked the transfer set (T19 + T21, no leak): NO CANDIDATE STANDS. Correction: 13 of 18, not 12.
5. **A100 (3:20 PM ET): the owner waived (b).** See the first lines.
6. **A101 (3:58 PM ET): selection under the waiver.** `select_candidate` (run once) picked final_a10. Parity, the official read copy and the pre-gate followed (sections 5.2-5.4).

## 3. What was trained

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

## 4. Forgetting monitor (old slice, 2,000 replay rows, C1 = 92.15%; monitors only, never candidates)

| Snapshot | Step | C2 minus C1 | P(yes) drift | KL(C1 to snap) | Flags |
|---|---|---|---|---|---|
| 25% | 918 | -1.80 pp | -0.0013 | 0.044 | none |
| 50% | 1,836 | -1.15 pp | +0.0002 | 0.030 | none |
| 75% | 2,754 | -0.50 pp | +0.0042 | 0.028 | none |

The A37 (k) stop rule fires only if the old slice is below -1.5 pp at both the 25% and the 50% snapshot. It did not fire.

## 5. The grid, the choice, parity, the official reads and the pre-gate

### 5.1 Grid and reads
`merge_avg.py` built 18 candidates in merged-weight space: final step, last-3 average, early+late average (early = s001212), each at alpha 0.5-1.0. Recorded at 6:26 AM ET, before any read: grid_sha256 `ef77658b420952c47a75c4fe1e8a949e0940cd37385fee8453beab1a44f85725`. One H100 session (`grid_1018_1215`, 5,877 s, $7.49) read C1 and all 18 on the same SGLang S1 path (bf16 merged, fp32 LM head), 26,191 rows each, plus a batch-1 latency run per model. 19 of 19 completed.

### 5.2 Choice (A101)
Under the waiver 13 candidates were eligible (those failing only (b)). A42-D 9.5 chose **final_a10**: "final step is the highest-S eligible candidate" (S 89.4671 = mean of G-proxy 98.684 and mixdev 80.25; last3_a09 has the same S, and the tie order puts the final step first; its S gain over the final step is 0.00 pt [-0.24, +0.23]). CANDIDATE_C2.json sha256 `86ce1de4...`, CHOSEN.json sha256 `4826448f...`; `grid_plan candidate-check`: OK_BEFORE_READS.

### 5.3 Parity and official reads
- **Parity (4:05 PM ET, H100, parity_1018): PASS.** n 2,000 rows of the G-block; argmax agreement 99.9% (2 disagreements; bar 99.5%); |change in label probability| <= 0.02 on 99.0% of rows (bar 99%: exactly at the bar); adapter sha held to CANDIDATE_C2.json. Record `c2_build/train/PARITY_final_a10.json` (sha256 95f0a220...). Cost $0.52.
- **Official reads (4:06 PM ET).** Per A97 (2) the 48 files of final_a10's grid read were copied byte for byte to the `q35_4b_c2` names, after CANDIDATE_C2.json. No prediction value and no meta field was changed. Record `OFFICIAL_READ_COPY_A97.json` (sha256 6c5dabb1...).

### 5.4 Pre-gate (official, logged 4:07 PM ET)
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

## 6. Dev results for all 18 candidates (every candidate vs C1, same job)

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

## 7. Why (b) fails, and what the T19 loss looks like

- **The transfer dev.** T19 (300 rows) + T21 (300 rows) = **600 rows**, `data/c2_transfer_dev.jsonl`, sha256 `2b9702a7eb68d56901e4a37e46a56399672a600fde5706ad0572489fac9af93e`, built 16 Oct at 7:50 AM ET (11:50 UTC), before any read. The spec's section 7.1 lists four families (T36, T19, T21, T20; 1,200 rows); T20 and T36 were left out under A45 (c) after failing G6 (A50). **No PREREG record names this 600-row set**; the GO #1 draft says only "600 transfer rows" and that (b) has little power. (b) has low power at n 600, but the failure does not depend on power: all 18 point estimates are negative and the highest upper bound is +1.65, below +3.0.
- **By family, final step:** T19 51.7% vs C1 63.0% = **-11.3 pp** [-17.2, -5.6] (n 300); T21 77.0% vs 75.3% = +1.7 pp [-2.7, +6.0]. T19 loses 7.0 to 16.3 pp on every candidate; T21 gains 1.7 to 6.7. Dropping T21 would make (b) worse.
- **T19 diagnosis (orchestrator dev analysis; I re-derived the same totals, 63.0 / 51.7, from the dev files).** T19 is the compliance-checking family. On its 98 verdict questions (gold: Compliant 39, Non-compliant 33, "Cannot be determined from the records" 26) C2 answers "Cannot be determined" on **76** (truth 26; C1 54). Recall on the gold "Compliant" items falls from 30.8% (C1) to **7.7%** (C2); on "Non-compliant" 63.6% to 48.5%. The pick-the-failing-item questions (n 57) lose **-15.8 pp** and the yes/no questions (n 145; 64.8% to 55.2%) **-9.7 pp**. The pattern reads as over-abstention on an unseen family; it is a dev observation, not a causal test.
- The trade between trained-family gain and transfer is nearly linear in alpha (mixdev +9.55 and transfer -1.33 at alpha 0.5; +12.31 and -4.83 at alpha 1.0). Blending toward C1 cannot reach the +3.0 bar.

## 8. OHS-4 look L1 and S1-S6: PLACEHOLDER

L1 reads **C1 and final_a10 in one job** on the frozen OHS-4 (spec 8.5, A100). It has not run. The runner is under skeptic review. The Opus pre-look ruling (`c2_build/zed_orch/RULING_L1_PRELOOK.md`, written 3:50 PM ET before any OHS-4 read) fixes, from written text only: one temperature per question type fitted on the C2 mixdev groups (group key `meta.family`), binary Brier for S4, the OPI definition for S5, complement pairs of G and R for S3, the single Jev read, the `jev-1.13` model pin (if it is not served there is no J and no substitute), SPEED-3 allowed to be "not run" with a disclosure, and the A100 mode (C1 + the A42-D 9.5 output, from the tool, parity still binding).
Results to fill in: S1 (R: C2 - C1 >= +5.0 pp and LB > 0), S2 (G non-inferiority, LB > -1.5), S3 (complement), S4 (Brier), S5 (security), S6 (dev pre-gate still passes, not re-read), each with n and CI; report-only parts U, per kind and domain, consistency, ECE.

## 9. Jev comparison J: PLACEHOLDER

Jev is read once, after the L1 verdict is logged. The spec 8.6 claim lines ("beats Jev on rule/agent" with LB > 0 in both pinned runs, "also on unseen kinds", "more consistent / better calibrated", "close to Jev on general", speed, cost) will be stated for C2 and C1 against Jev as the L1 results allow. Results to fill in.

## 10. Honest verdict (so far)

The pre-gate passes only because the owner waived (b); on its own terms (b) is a clear fail, and the T19 loss is real on dev. C2 is a strong specialist: +12.3 pp on the families it trained, no latency or calibration cost, no security regression, and general dev accuracy flat to slightly negative (-0.48 pp pooled, CI includes 0). Whether it **ships** is decided only by L1 (S1: +5.0 pp on part R with LB above 0, S2: general non-inferiority, S3-S6) and nothing before that. The odds stated at GO #1 (A81) were about 15-20% of passing every check. No bar was changed; (b) was waived by the owner, openly, after the result.

## 11. What carries into C2.1

- **The gain is real but narrow;** the transfer loss is concentrated in one family (T19), by over-abstention. C2.1 should read a per-family transfer table at every checkpoint, include held-out families in its transfer dev from the start, and watch the share of "cannot be determined" answers.
- **Interpolation cannot fix it;** the alpha curve is nearly linear. The levers are the data mix and the recipe (more T19-like verdict items with a resolvable gold, less abstention pressure, lower LR or fewer steps on the families that move T19), not blending.
- **S cannot see transfer.** S (G-proxy + mixdev) rises with alpha while transfer falls; C2.1's selection score should include the transfer dev.
- **R14 init rule, with numbers.** The written rule: C2 ships (init C2); C2 fails only the Jev-beat gate S1 but passes its G floor and non-regression gates (init = C2's unshipped weights); C2 fails its G floor or a non-regression gate (init C1). It is computed the hour L1 is logged. Pre-L1 facts: every non-regression dev check passes at the final step (D1 -0.60, D2 -0.78, D3 -0.36/-0.88, D4 +0.0017, D5, D6, D9, complement); transfer -4.83 (waived); G floor (S2) not yet measured.
- **Process:** read the stored reference on the same path as the candidates; record the transfer set's composition in PREREG before training; wire an owner acceptance into the tools before the reads, not after (A96, A100).

## 12. Deviations, rulings and disclosures, in order

1. **A78 / A80:** the selection code that built the C2 records was not the adopted A69 text. The owner set the agent core to 4 of 6 for C2 only ("ok go with b"). T33, T12, T24 left out.
2. **A84:** one re-run of the A61 (f) 8.5 check, same tool and input, so the tool wrote its own result files.
3. **A85:** the first launch crash-looped on a path bug (zero steps, about $0.0002); the generator was fixed and the owner approved the relaunch.
4. **A86 / A87:** the first100 guard aborted by mistake (JSON null counted as non-finite); fixed (NaN/inf still abort), reviewed by a skeptic, owner approved continuing.
5. **A88 / A91:** the first attempt to launch the H100 grid (about 6:30 AM ET) was denied by the permission classifier and was not retried or worked around. The reads then started on the free L4 (A90). On the owner's A91 "do it" all 19 models were read on an H100 (cap $15, payer mahadikarya3, never the card).
6. **A93:** the 98 L4 read files for C1 and final_a10 were moved, not deleted, to `c2_build/_superseded_L4_reads_20261018/` (sha manifest) so all 19 models are H100 reads. No score had been computed.
7. **A94 / A95:** the pre-registered refparity look (fresh H100 C1 vs stored C1, n 8,143) failed one bar, max |dp| 0.1013 vs 0.05 (1 row; argmax agreement 99.75%, mean |dp| 0.00198, accuracy +0.04 pp all passed). Logged at 1:49 PM ET as pass false; it stays so. The owner accepted it as serving-path noise (A95).
8. **A96:** the tools refused after A95, so `gate_dev.py` and `gate_c2.py` were edited after the reads to accept that one named look only (full A95 sentence, look sha, n and max_dp pinned in code; read files re-hashed). 123 tests pass; three skeptics reviewed it, the conformance skeptic found one defect (the quote was checked as a substring), fixed and re-checked.
9. **A97:** the owner approved GO #2 (L1 and J), reuse of the chosen candidate's H100 reads as the official reads (done: 48 files byte for byte), and skipping symmetrisation (**not evaluated**).
10. **A98 / A99:** the first selection (no waiver) found no candidate; verified by three verifiers and an Opus judge.
11. **A100 (OWNER OVERRIDE):** (b) waived after the result; see the first lines. The hook (`waiver_a100.py`, `WAIVER_B_A100.json`; `select_candidate.py` and `gate_c2.py` changed; 38 + 7 new tests) passed a 3-lens skeptic (all SOUND). Minor items found, not changed: (i) the waiver's PREREG search window is not bounded to the A100 block; (ii) the OWNER_GO line check is an unanchored substring match; (iii) the waiver is not bound to the C2 run id; (iv) CANDIDATE_C2.json carries no waiver flag; (v) the L1 helper `l1common.load_waiver_b` is looser than `waiver_active`.
12. **A101:** selection under the waiver; parity, official read copy and pre-gate followed.
13. **L1 pre-look ruling:** `RULING_L1_PRELOOK.md` (Opus, 3:50 PM ET, before any OHS-4 read) fixes the L1/J details listed in section 8; runner changes it required are under skeptic review.
14. **Pre-existing weakness, found during A96:** `gate_dev.refparity_status` never stops on a failed look for a reference whose stored name is not its built-in one, so the PREREG section 4 ship-mode refusal was already weaker than written for C2. For C2, `gate_c2.check_refparity` was the only enforcement point and it did enforce.
15. **Transfer-set history (found by the A99 re-check; neither point rescues (b)):** T21 was admitted on a single-build G6 rather than the A50 average; T20 ran a third iteration although A48 (a) allows 2. No PREREG record names the 600-row set.
16. **Other:** the T19 diagnosis is an orchestrator dev analysis, not a pre-registered test. Parity passed with the within-0.02 share exactly at its bar. PREREG_FINAL.md is not committed in git. Scout agents had accidental grep hits on sealed-side file names; no sealed content was read or used. The G-proxy is labelled "A42-D 12.2 unmet". The grid ledger ($7.49; session report $7.54; Modal billing $7.95 before parity) and `c2_check status` (which shows "training $21.81" and also "other $8.01", counting the grid and parity twice) differ; the real C2 Modal total is about $21.15 to $21.81 of the $40 cap.

No bar, gate, seed, candidate rule or look rule was changed except the owner's explicit waiver of (b). No sealed or OHS path was opened by me.

## 13. Where things are

`c2_build/C2_RESULTS.json` (all numbers); `c2_build/train/grid_reads/*.json` (per-candidate eligibility records); `c2_build/train/CHOSEN.json` (A101) and `CHOSEN_A98_NOCANDIDATE.json`; `c2_build/CANDIDATE_C2.json`; `c2_build/train/WAIVER_B_A100.json`; `c2_build/train/PARITY_final_a10.json`; `c2_build/train/OFFICIAL_READ_COPY_A97.json`; `c2_build/logs/gate_c2_pregate_q35_4b_c2.json`; `c2_build/logs/grid/ship_*.json` and `latency_*.json`; `c2_build/train/REFPARITY_ACCEPT_A95.json`; tool shas in `c2_build/zed_orch/a64/A64_TOOLS.md`. Earlier versions: `C2_REPORT_STOPPED_0630ET_20261018.md` (stop state, with the training numbers in full) and `C2_REPORT_DRAFT_A98_NOCANDIDATE.md`.
