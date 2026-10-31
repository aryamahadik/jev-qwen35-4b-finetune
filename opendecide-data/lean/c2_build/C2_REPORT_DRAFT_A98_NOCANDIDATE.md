# C2 report (Sun 18 Oct 2026, US Eastern times)

**Status: DRAFT, updated about 4:10 PM ET. Open: L1 and J (sections 7 and 8 are placeholders), and the owner's choice between keeping the rule (the one OHS-4 look goes to C1 alone) and an owner override.** The independent re-check ordered by PREREG Record A98 is done: three verifiers reproduced the numbers from the raw predictions, the rule matches the code, and the transfer set is the pre-registered one. No candidate stands. Everything else below is measured and final.

**Verdict so far: C2 does NOT pass its pre-gate and will not ship.** Every one of the 18 pre-registered candidates fails pre-gate check (b), transfer to unseen families. By A42-D 9.5 and spec 7.2, with no eligible candidate the pre-gate fails: C2 gets no OHS-4 look. C2 did learn the trained families (+12.3 pp on their mixdev), but it did not improve general dev accuracy (-0.48 pp, CI includes 0) and it got worse on one unseen family (T19, -11.3 pp).

Times are US Eastern (EDT, UTC-4); UTC in brackets where a record uses it. The binding spec is `teach1/C2_DATA_SPEC.md` (sha256 245ba9f9..., A37 (a)); "spec 7.2" below means its section 7.2. All numbers are from files in this tree; `c2_build/C2_RESULTS.json` holds every number with n and CI, the spend, the shas and the timings.

---

## 1. At a glance

| Item | Result |
|---|---|
| Training | Done 6:24 AM ET. 3,673 steps, 186 min, 59,340 rows (23,736 new + 35,604 replay), **$13.14**, free credit only |
| Forgetting monitor (old slice, C2 minus C1) | -1.80 pp at 25%, -1.15 pp at 50%, -0.50 pp at 75%. Stop rule (below -1.5 at both 25% and 50%) did not fire |
| Grid | 18 candidates (3 bases x alpha 0.5-1.0), recorded 6:26 AM ET before any read; read on one H100 job, C1 + 18 in the same job, $7.49 |
| Trained-family gain, final step | **+12.31 pp** [+10.47, +14.15] on mixdev (n 2,795). Bar (a) is +8.0 pp: PASS |
| General dev accuracy, final step vs C1 | **Pooled, 8,143 rows over 9 splits: -0.48 pp** [-1.14, +0.16]. **D1 check (n 7,056, without tb_mixtral): -0.60 pp** [-1.31, +0.15]. Both pass (D1 needs LB above -1.5). Alpha 0.5, pooled: +0.05 pp [-0.39, +0.48] |
| Transfer to unseen families (T19 + T21, 600 rows), final step | **-4.83 pp** [-8.59, -1.02] (n 600). Bar (b) is +3.0 pp with LB above 0: **FAIL**. Best candidate (alpha 0.5): -1.33 pp [-4.26, +1.62], still a FAIL |
| Candidate chosen | **None** (NO CANDIDATE). `CANDIDATE_C2.json` not written |
| H100 parity, official pre-gate, OHS-4 look for C2, S1-S6 | Not run (they follow the choice) |
| L1 (OHS-4, C1 alone) and J (Jev once) | **Pending** |
| Spend | Training $13.14 + grid $7.49 = $20.63 (ledger basis; Modal billing basis $13.25 + $7.95 = $21.20). Cap $40. Parity $0, L1 and J not yet |

## 2. What was trained

Training ran on mahadikarya2 free credit only (no relay needed; the card was never used).

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

## 3. Forgetting monitor (old slice, 2,000 replay rows, C1 = 92.15%; monitors only, never candidates)

| Snapshot | Step | C2 minus C1 | P(yes) drift | KL(C1 to snap) | Flags |
|---|---|---|---|---|---|
| 25% | 918 | -1.80 pp | -0.0013 | 0.044 | none |
| 50% | 1,836 | -1.15 pp | +0.0002 | 0.030 | none |
| 75% | 2,754 | -0.50 pp | +0.0042 | 0.028 | none |

The A37 (k) stop rule fires only if the old slice is below -1.5 pp at both the 25% and the 50% snapshot. It did not fire.

## 4. The grid, the H100 reads and the choice

- **Grid.** `merge_avg.py` built 18 candidates in merged-weight space: final step, last-3 average, early+late average (early = s001212), each at alpha 0.5, 0.6, 0.7, 0.8, 0.9, 1.0. Recorded at 6:26 AM ET (before any read): grid_sha256 `ef77658b420952c47a75c4fe1e8a949e0940cd37385fee8453beab1a44f85725`.
- **Reads.** After the owner moved the reads to an H100 (A88/A91), one session (`grid_1018_1215`, 12:15 PM to 1:34 PM ET, 5,877 s, $7.49 on the ledger) read C1 and all 18 candidates on the same SGLang S1 path (bf16 merged, fp32 LM head), 26,191 rows each, with a batch-1 latency run per model. 19 of 19 models completed; every file was held to its sha256.
- **Choice.** `grid_elig.py` applied gate_c2's own rules to each candidate; `select_candidate.py` (run once) answered **NO CANDIDATE: no eligible candidate; the pre-gate fails (spec 7.2)**. CHOSEN.json sha256 `54ba8937fa96cdeb48b17b131b0c2bd75257d1b6dfbb8f818579a40a53b3da7f`.
- **Not run because there is no chosen candidate:** H100 parity (S1 vs HF adapter), the official pre-gate, the copy of the grid reads as official reads (A97 2; tool built and tested, unused).

## 5. Dev results for all 18 candidates (every candidate vs C1, same job)

(a) needs +8.0 pp with LB > 0 on the mixdev rows of trained families; (b) needs +3.0 pp with LB > 0 on the transfer dev. Dev CIs are 10,000 paired group-bootstrap resamples, seed 0.

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

S is the mean of G-proxy and mixdev accuracy (no new-family dev split entered C2). The G-proxy carries the label "A42-D 12.2 unmet" (A61 f). The other pre-gate checks, for the final step: D1 -0.60 [-1.31, +0.15] PASS; D2 -0.78 [-1.68, +0.11] PASS; D3 yes/no -0.36, choice -0.88 PASS; D4 Brier +0.0017 PASS; D5 equiv 5.68% vs 9.00% and perm 2.91% vs 2.52% PASS; D6 jagged 0.0% vs 0.0% and OPI 0.4% vs 1.3% PASS; D9 p50 30.9 vs 31.6 ms PASS; complement 0.0446 vs 0.0462 PASS.

Two different dev figures appear in this report and both are right: **pooled, 8,143 rows over the 9 dev splits: -0.48 [-1.14, +0.16]** (the plain pooled accuracy gap) and **the D1 check, n 7,056 (the pooled set without tb_mixtral, which the gate excludes): -0.60 [-1.31, +0.15]**. Both pass D1 (LB above -1.5).

**Final step (alpha 1.0) vs C1, per dev split (pp):** dev_nc -1.59, taskbank_dev +0.42, hard_dev +0.96, dev_negwords +0.75, dev_claims -0.93, pg_dev -1.72, devzs -1.62, devp_card -0.17, dev +0.83. Pooled -0.48 [-1.14, +0.16] (n 8,143). Unseen-source primary set -0.78 [-1.68, +0.11] (n 3,847).
**Alpha 0.5 vs C1:** dev_nc -0.10, taskbank_dev 0.00, hard_dev +0.96, dev_negwords +1.62, dev_claims -0.40, pg_dev -0.57, devzs -0.88, devp_card +0.23, dev +0.33. Pooled +0.05 [-0.39, +0.48].

**Trained families, mixdev gain (final step):** T28 +28.0, T30 +27.3, T31 +24.7, T06 +24.0, T25 +22.7, T29 +14.7, T23 +12.7, F4 +12.0, T01 +11.3, F6 +9.9, T26 +8.0, T15 +6.7, F11 +6.5, F5 -1.0. Families that left the mix, report-only: T33 +2.1, T24 -1.3, T07 -4.0, T12 -4.7.

## 6. Why the pre-gate fails

Check (b) uses the transfer dev: families that C2 did not train, scored as C2 minus C1.
- **What the transfer dev is.** T19 (300 rows) + T21 (300 rows) = **600 rows**, file `data/c2_transfer_dev.jsonl`, sha256 `2b9702a7eb68d56901e4a37e46a56399672a600fde5706ad0572489fac9af93e`, built 16 Oct at 7:50 AM ET (11:50 UTC), before any read. The spec's section 7.1 lists four families (T36, T19, T21, T20; 1,200 rows). T20 and T36 were left out under A45 (c) after failing G6 (A50). **No PREREG record names this 600-row set**; the GO #1 draft says only "600 transfer rows" and that pre-gate (b) has little power. The independent re-check (A98) confirmed it is the pre-registered set and has no leak.
- **Power.** (b) has low power at n = 600. The failure does not depend on power: every one of the 18 point estimates is negative (the best is -1.33), and the highest upper bound of any CI is +1.65 (last3_a05), below the +3.0 bar.
- Final step: T19 51.7% vs C1 63.0% = **-11.3 pp**; T21 77.0% vs 75.3% = +1.7 pp; together -4.83 pp [-8.59, -1.02].
- Alpha 0.5 (halfway back to C1): T19 -7.0 pp, T21 +4.3 pp; together -1.33 pp [-4.26, +1.62].
- Dropping T21 does not help: T19 alone is -7.0 to -16.3 pp on every candidate, so (b) would be worse, not better.
- Moving toward C1 trades the trained-family gain for transfer almost linearly (mixdev +9.55 and transfer -1.33 at alpha 0.5; +12.31 and -4.83 at alpha 1.0), and the whole grid stays below the +3.0 bar. No blend can pass; (b) fails on all 18. **For 13 of 18 it is the only failed check.** The other five also fail other checks: last3_a05 (D9, 1.09x), last3_a10 (D3 and D9, 1.08x), earlylate_a08 (D3), earlylate_a09 and earlylate_a10 (D1, D2 and D3).

## 7. OHS-4 look L1 and S1-S6: PLACEHOLDER

By spec 7.2 C2 gets no OHS-4 look. L1 reads **C1 alone** (SPEED-3 numbers and the C1 side of the Jev comparison). S1 to S6 do not apply to C2. L1 has not run. The A98 re-check is finished; the owner is choosing between keeping the rule (L1 = C1 alone, then J = C1 vs Jev) and an owner override, because the one OHS-4 look cannot be undone.
Results to fill in: C1 on OHS-4 by part (R, G, U, X, consistency), accuracy with CIs, p50/p95/p99 at concurrency 1, 16 and 64, $/1K at 40% use.

## 8. Jev comparison J: PLACEHOLDER

Jev is read once, after the L1 verdict is logged. The claim lines of spec 8.6 ("beats Jev on rule/agent", "also on unseen kinds", "more consistent / better calibrated", "close to Jev on general", speed, cost) will be stated for **C1** vs Jev only, since C2 has no OHS-4 read. Results to fill in.

## 9. Honest verdict

C2 is **not a ship**, on the pre-registered rules. It is a strong specialist and a weak generaliser: +12.3 pp on the families it trained on, flat to slightly negative on general dev data (-0.48 pp at the final step, about 0 at alpha 0.5), and negative on one unseen family (T19 loses 7.0 to 16.3 pp on every candidate). It costs nothing in latency, calibration (Brier +0.0017) or security. The odds stated at GO #1 (A81) were about 15-20% of passing every check; this result is on the failing side, and it fails on a check (transfer) whose bar was set before any data. No bar was changed or relaxed.
Caveats to keep: the transfer dev is two families and 600 rows (low power; the failure does not depend on power, see section 6), T19 carries the loss, and the G-proxy is flagged "12.2 unmet". The independent re-check (A98) reproduced the numbers from the raw predictions and found no defect in the rule, the code or the transfer set.

## 10. What carries into C2.1

- **The gain is real but narrow.** +9.5 to +12.3 pp on trained-family dev. It did not lift any general split (pooled -0.48 to +0.05).
- **Negative transfer is the problem to design against.** T19 loses 7.0 to 16.3 pp on every one of the 18 candidates, while T21 gains 1.7 to 6.7 pp. C2.1 should include held-out families in its transfer dev from the start and read a per-family transfer table at every checkpoint, not only a pooled number.
- **Interpolation cannot fix it.** The alpha curve is nearly linear and never reaches +3.0. The next lever is the data mix or the training recipe (more replay of the T19 kind, lower LR, fewer steps on the families that move T19), not blending.
- **S cannot see transfer.** The selection score S (G-proxy + mixdev) rises with alpha while transfer falls. A selection score for C2.1 should include the transfer dev.
- **R14 init rule, with numbers.** The written rule has three branches: C2 ships (init C2); C2 fails only the Jev-beat gate S1 but passes its G floor and non-regression gates (init = C2's unshipped weights); C2 fails its G floor or a non-regression gate (init C1). C2 fails none of those literally: it fails a transfer gate that the rule does not name, and its G floor (S2) is not measured (no C2 look). On dev, every non-regression check passes at the final step (D1 -0.60, D2 -0.78, D3 -0.36/-0.88, D4 +0.0017, D5, D6, D9, complement), but transfer is -4.83 [-8.59, -1.02]. Both options therefore have a case: C2's unshipped weights keep +12.3 pp on trained families; C1 avoids a measured loss on an unseen family. This needs the owner's R14 answer; the default text does not settle it.
- **Process.** Read the stored reference on the same path as the candidates (the refparity miss came from comparing an H100 read with an older L4 read). Record the transfer set's real composition in PREREG before training (the spec lists four families and 1,200 rows; the set used has two families and 600 rows, and no PREREG record names it). Apply an owner acceptance in the tool before the reads, not after (A96).

## 11. Deviations, rulings and disclosures, in order

1. **A78 / A80:** the selection code that built the C2 records was not the adopted A69 text. The owner set the agent core to 4 of 6 for C2 only ("ok go with b"). T33, T12, T24 left out.
2. **A84:** one re-run of the A61 (f) 8.5 check, same tool and input, so the tool wrote its own result files.
3. **A85:** the first launch crash-looped on a path bug (zero steps, about $0.0002); the generator was fixed and the owner approved the relaunch.
4. **A86 / A87:** the first100 guard aborted by mistake (JSON null counted as non-finite); fixed (NaN/inf still abort), reviewed by a skeptic, owner approved continuing.
5. **A88 / A91:** the first attempt to launch the H100 grid (about 6:30 AM ET) was denied by the permission classifier and was not retried or worked around (the earlier stop report). The grid reads then started on the free L4 (A90; C1 and final_a10 were read there, 8:28-11:12 AM ET). On the owner's A91 "do it" (about 12:10 PM ET) all 19 models were read on an H100 instead (cap $15, payer mahadikarya3, never the card).
6. **A93:** the 98 L4 read files for C1 and final_a10 were moved, not deleted, to `c2_build/_superseded_L4_reads_20261018/` (sha manifest) so all 19 models are H100 reads. No score had been computed.
7. **A94 / A95:** the pre-registered refparity look (fresh H100 C1 vs stored C1, n 8,143) failed one bar, max |dp| 0.1013 vs 0.05 (1 row; argmax agreement 99.75%, mean |dp| 0.00198, accuracy +0.04 pp all passed). The look was logged at 1:49 PM ET as pass false and stays so. The owner accepted it as serving-path noise (A95).
8. **A96:** the tools refused after A95, so `gate_dev.py` and `gate_c2.py` were edited after the reads, to accept that one named look only (full A95 sentence, look sha, n and max_dp pinned in code; fresh and stored read files re-hashed). 123 tests pass. Three independent skeptics (regression, bypass, conformance) reviewed it; the conformance skeptic found one defect (the owner's quote was checked as a substring), which was fixed and re-checked sound. The edit changes no bar.
9. **A97:** the owner approved reuse of the chosen candidate's H100 reads as the official pre-gate reads, GO #2 (L1 and J), and skipping symmetrisation. With no chosen candidate the reuse was not needed; symmetrisation was **not evaluated**.
10. **Pre-existing weakness, found during A96:** `gate_dev.refparity_status` never stops on a failed look for a reference whose stored name is not its built-in one, so the PREREG section 4 ship-mode refusal was already weaker than written for C2. For C2, `gate_c2.check_refparity` was the only enforcement point and it did enforce.
11. **Other disclosures:** PREREG_FINAL.md is not committed in git. Scout agents had accidental grep hits on sealed-side file names; no sealed content was read or used. The G-proxy is labelled "A42-D 12.2 unmet". The grid ledger ($7.49; the session report says $7.54; Modal billing delta $7.95) and `c2_check status` (which shows "training $21.2" because it counts the grid's billing twice) differ; the real C2 Modal total is about $20.6-21.2 of the $40 cap.
12. **Transfer-set history (found by the A98 re-check; neither point can rescue (b)):** T21 was admitted to the transfer dev on a single-build G6 rather than the A50 average (mean of four 6,000-row builds), and T20 ran a third iteration although A48 (a) allows 2. T20 and T36 then left the set (A45 c, A50). Dropping T21 makes (b) worse. No PREREG record names the 600-row set.
13. **A98 re-check:** three verifiers reproduced the transfer numbers from the raw predictions, checked the rule against the code and checked the set's composition (T19 + T21, built 16 Oct, no leak). Result: NO CANDIDATE stands.

No bar, gate, seed, candidate rule or look rule was changed. No sealed or OHS path was opened.

## 12. Where things are

`c2_build/C2_RESULTS.json` (all numbers); `c2_build/train/grid_reads/*.json` (per-candidate eligibility records); `c2_build/train/CHOSEN.json`; `c2_build/logs/grid/ship_*.json` and `latency_*.json`; `c2_build/train/REFPARITY_ACCEPT_A95.json`; tool shas in `c2_build/zed_orch/a64/A64_TOOLS.md`. The earlier stop-state report is kept as `c2_build/C2_REPORT_STOPPED_0630ET_20261018.md` (it records the training numbers, the family list and the A85-A87 history in full).
