# C2 report (Sun 18 Oct 2026)

**Status: STOPPED EARLY, at the grid launch, before any evaluation read.** C2 training finished cleanly. The 18 grid
candidates are built and recorded. No candidate has been read on any dev set. No candidate has been chosen. No pre-gate,
no OHS-4 look, and no Jev read has happened. `c2_build/C2_RESULTS.json` does not exist, because nothing was scored.
**There is no ship / no-ship verdict yet.**

Times are UTC, with US Eastern (EDT, UTC-4) in brackets.

---

## 1. Where and why it stopped

- **Step:** RUNBOOK step 6 (`grid_h100`). This is the one paid H100 command that reads C1 plus the 18 candidates on dev:
  `MODAL_PROFILE=mahadikarya3 modal run c2_build/train/grid_h100/modal_app_grid.py::grid --run-id grid_<id>`.
- **Why:** the Claude Code auto-mode permission classifier denied the command, giving the reason "Real-World
  Transactions". The orchestrator did not retry it and did not work around it, as the hard rules require. This happened
  at about 10:30 UTC (6:30 AM ET).
- **Everything before it passed.** `driver.py check` reported no blockers (`ready: true`). `driver.py plan` estimated
  19 reads plus the parity fit at about $10.08 (low $7.93, high $15.01). The grid ledger stood at $0 of the $15 cap.
  The payer would have been mahadikarya3, which has $13.86 of free credit.
- **Money spent after training: $0.** No paid step ran after training.

## 2. What was trained

Training ran on mahadikarya2 only. No relay to mahadikarya3 was needed. Nothing was charged to aryamhd.

| Item | Value |
|---|---|
| Start | C1 adapter `q35_4b_main500k`, sha 507d1c29…; base Qwen3.5-4B @ 851bf6e8 |
| Recipe | round-1 recipe unchanged: LoRA r16 / alpha 32, lr 5e-5 cosine, batch 16, one pass (epochs 0.9901), KD 0.5 on replay, lam_ord 1.0 (14 ordinal rows), seed 20261013 |
| Rows | **59,340**: 23,736 new rows + 35,604 replay rows. Relations 8,690 (complement 4,382, equiv 1,442, inv 2,866) |
| Mix ids sha | 77ca615f9444b69b… (mix_report_c2.json `selection_digest`); data shas cc1d1ff5… / 9bee74bf… |

### 2.1 New rows per block (18 blocks entered)

| Group | Block: rows |
|---|---|
| Agent core (4 of 6) | T28 2,247 · T29 2,000 · T30 1,400 · T26 1,398 |
| Other program families (6) | T31 999 · T01 1,600 · T23 794 · T06 600 · T15 900 · T25 600 |
| F-blocks | F5 1,362 · F6 930 · F11 552 · F4 500 |
| Other blocks | GB 3,376 · GW 3,696 · I10 100 · SB5 682 |
| Replay | 35,604 |

That makes 10 program families (the minimum is 10) and an agent core of 4 of 6 (the minimum is 4 under A80). Several
blocks entered short of target after the binding drops: F5, F6, F11, GB, GW and SB5. No refill went beyond the
pre-registered rules. I10 has 100 of 5,000 target rows.

### 2.2 Families and blocks left out

| Left out | Reason (ruling) |
|---|---|
| T33, T12, T24 | The faithful A69 repair and (f)(ii) refuse their selections, so (f)(iii) leaves them out (A78 finding, A80 owner ruling). Their mixdev rows are report-only: "family not trained in C2". |
| T27, RTW | QC record not passed |
| T07 | 1 confirmed wrong gold, which means a generator bug (A72) |
| T32 | The binding G13 drops removed every equiv twin, so equiv_share is 0 (A71 a) |
| T35, T37b, T46 | Moved to C3 (A65, A52 a, A67) |
| T40-T45 | No candidates on disk by the new-family deadline (A42-D 13.1) |
| MD | 3 sources were 8.5 HITs (md_worldbank, md_usgs, md_cma). After removing them, MD fell under the A42-D 8.2 floor, so it was removed whole (A61 f, A73) |
| DI-KR, DI-LANG, DI-TS, DI-RC, DI-TOOLS | No DI block enters C2 (A61) |
| Item 10 (Opus distillation) | Not built for C2 (A42-D (f)) |

### 2.3 Required disclosures (A78, A80)

- **A78:** the A69 selection code that first built every C2 select record was not the adopted A69 text. It ran a
  greedy repair with no 25% loss limit; for example, T33 lost 86.7% of its rows. A faithful version, run scratch-only,
  refused T33, T12 and T24. Under the rules as adopted, this left the agent core at 4 of 6, which is a STOP.
- **A80 (owner words: "ok go with b"):** for C2 only, the agent-core minimum is **4 of 6 instead of 5 of 6**. A69 stays
  exactly as adopted: the faithful repair is wired in, and T33, T12 and T24 are left out. Nothing else changed: OHS-4
  binding, S1-S6, the pre-gates, the money caps, and GO #1 / GO #2.
- **G-proxy:** A42-D 12.2 is unmet (A61 f). Every G-proxy number in the selection score S would carry that label. No G-proxy
  number exists yet.

## 3. Training numbers

| Item | Value |
|---|---|
| Steps | 3,673 (one pass), 186.0 min of training |
| s/step | seg1 3.067 · seg2 (steps 100-300) 2.972 · overall about 3.04 (round-1 reference 3.716) |
| Loss | first-5 mean 0.529; mean of the last 10 log points 0.301; final step 0.226; no non-finite total or task loss |
| Cost | **$13.14** training, against T_max $22.96. Projection at step 300 was $14.90; the mix budget was $14.36 |
| C2 Modal total | $13.14 of $40 (A61 e) |
| Free credit left | mahadikarya2 $5.97 · mahadikarya3 $13.86 |
| Checkpoints | 7 snapshots (s000918, s001212, s001836, s002460, s002754, s003048, s003379) plus the final adapter |

**Snapshot monitor (old slice, 2,000 replay rows, C1 = 92.15%; monitors only, never candidates):**

| Snapshot | Step | Old slice C2 − C1 | P(yes) drift | KL(C1‖snap) | Flags |
|---|---|---|---|---|---|
| 25% | 918 | **−1.80 pp** | −0.0013 | 0.044 | none |
| 50% | 1,836 | **−1.15 pp** | +0.0002 | 0.030 | none |
| 75% | 2,754 | **−0.50 pp** | +0.0042 | 0.028 | none |

The A37 (k) stop rule fires only if the old slice is below −1.5 pp at both the 25% and the 50% snapshot. At 50% it was
−1.15 pp, so the rule did not fire. P(yes) drift stayed well inside ±0.02. The old-slice loss shrank as training went on.

**Timeline:** T_max fixed at 06:43 (2:43 AM ET). First launch at 06:45 (2:45 AM ET) crash-looped (A85). Relaunch at
07:03 (3:03 AM ET). seg1 ended at step 100 at 07:13. seg2 ran 07:21-07:33. The A37 (k) projection said GO at 07:33
(3:33 AM ET). seg3 ran 07:34-10:24. **C2 TRAINING FINAL at 10:24 (6:24 AM ET).**

## 4. The grid and the chosen candidate

- **Built:** `merge_avg.py grid` made the 18 candidates in merged-weight space: 3 bases (final, last-3 average,
  early+late average with early = s001212) × alpha {0.5, 0.6, 0.7, 0.8, 0.9, 1.0}. That is 6.5 GB in
  `models/q35_4b_c2_grid`, with worst verify error 7.5e-9 (the bar is < 1e-5).
- **Recorded before any look (A42-D 9.6), at 10:26 (6:26 AM ET):**
  - grid_sha256 `ef77658b420952c47a75c4fe1e8a949e0940cd37385fee8453beab1a44f85725`
  - grid.json file sha256 `dd01beb72742d25a893ac277cab9582e8d63c6c48e9fa87713b51b424eb74260`
  - GRID_RECORD.json sha256 `0714a1c328b2f095f240bd991087a967cfb14709e5ab9392b2209f5050ecc2a9` (18 candidates)
  - final_a10 (the final adapter) is 93aba519…
- **Prompt check:** `prompt_sha_check.py --adapter models/q35_4b_c2` PASSED on 32 probe views (prompt digest 64b50c55…,
  token-id digest 246f1472…).
- **The run folder is on the payer.** `models/q35_4b_c2` was copied for free to the mahadikarya3 Volume and checked.
- **Chosen candidate: NONE.** No dev reads exist, so the selection score S and the 11 eligibility checks were not
  computed. `select_candidate.py` did not run, and `CANDIDATE_C2.json` does not exist. S1 parity (≥ 99.5%) also did not
  run, because it comes after the choice.

## 5. Pre-gate (spec 7.2): NOT COMPUTED

None of these checks was computed: (a) learning, (b) transfer, (c1) D1, (c2) D2, (c3) D3, (c4) D4, (c5) D5, (c6) D6,
(c7) D9 latency, and (d) complement.

## 6. OHS-4 look (L1) and S1-S6: NOT RUN

S1 (R ≥ +5.0 pp and LB > 0), S2 (G non-inferiority, LB > −1.5 pp), S3 (complement), S4 (Brier), S5 (security) and S6
(dev pre-gate) are all unmeasured. No CIs exist. The look log is untouched, so **the one OHS-4 look is still unused**.

## 7. Jev comparison (J, spec 8.6): NOT RUN

None of the claim lines can be stated: "beats Jev on rule/agent", "also on unseen kinds", "more consistent / better
calibrated", "close to Jev on general", speed, and cost. J comes only after the L1 verdict is logged. No OpenRouter
spend has happened.

## 8. Latency and cost notes

- C2 latency was not measured (D9 / SPEED-3 were not run). C2 uses the same base and the same r16 LoRA merged to bf16 on
  SGLang S1, so its serving path is the same as C1's. That is an expectation, not a measurement.
- C1 reference numbers, from earlier records and not new: S1 costs about $0.079 per 1K. On H100 the C1 fast path runs
  p50 14.1 ms and p95 19.2 ms per decision at batch 1.
- Training came in $1.76 under its step-300 projection.

## 9. Honest verdict

**No verdict.** C2 is not shipped and not rejected, because it has not been tested. The only quality signal so far is
the old-slice monitor. It shows C2 slightly below C1 on old skills: −1.80 pp early, recovering to −0.50 pp at 75%.
This is a guard against forgetting. It says nothing about the C2 bar, which is +5.0 pp on part R.

The odds stated at GO #1 were about 15-20% of passing every check (A81). Nothing since then changes that estimate.

## 10. What carries into C2.1: R14 init

The R14 default rule (C2_1_PLAN_v3 section 5) picks the init from C2's measured gates:
- If C2 ships, init = C2.
- If C2 fails only on S1, init = C2's unshipped weights.
- If C2 fails the G floor or any non-regression gate, init = C1.

**None of those gates exist yet, so the branch cannot be computed.** Recommendation: keep R14 at its default and
compute the branch the hour the pre-gate and S results exist. Do not choose an init now. The snapshot numbers above
(−1.80 / −1.15 / −0.50 pp on the old slice, KL 0.03-0.04) give no reason today to prefer C1 in advance. They also do
not show that C2 is better.

## 11. Deviations and stops, in order

1. **A78 / A80:** the selection code was not faithful to adopted A69. The owner set the agent core to 4 of 6 for C2 only.
2. **A84:** one re-run of the A61 (f) 8.5 check with the same tool and the same input. It ran only so that the tool
   itself wrote its result files.
3. **A85:** the first launch crash-looped at container start. The cause was a path bug in `modal_od_c2.py`. Zero
   steps ran, and billing was about $0.0002; the ledger briefly showed $1.23 because it counted the open segment's cap.
   The orchestrator's `modal app stop` was denied by the classifier ("Interfere With Workloads") and was not worked
   around. The generator was fixed and the relaunch was approved by the owner.
4. **A86 / A87:** the first100 guard ABORTED by mistake. It counted a JSON null, which marks an absent loss term, as
   non-finite. The guard was fixed so that NaN and inf still abort. A new `after100` chain command keeps every guard,
   including the A37 (k) projection. A Sonnet skeptic reviewed the fix, and the owner approved continuing.
5. **A88:** the post-training grid reads moved from the free L4 to an H100, with a $15 cap and mahadikarya3 as payer.
6. **S4 stop (this report):** the H100 grid launch was denied by the permission classifier ("Real-World Transactions").
   It was not retried and not worked around. This blocks the whole path: grid reads, choice, `CANDIDATE_C2.json`,
   parity, pre-gate, L1 and J.

No bar, gate, seed, candidate rule or look rule was changed. No sealed or OHS path was opened.

## 12. To resume

The owner can either run the RUNBOOK step 6 command himself or allow it for this session. Then the path continues
exactly as pre-registered: pull and post (step 7), `grid_elig` and `select_candidate`, `CANDIDATE_C2.json`, parity
(step 8), the official pre-gate, L1, and then J. The plan fits the cap: about $10.08 likely, against the $13.50
stop-launch level, with mahadikarya3 credit at $13.86. One H100 session is capped at 11,700 s, about 3.25 h. The free
L4 route is slower, and A88 replaced it for the grid; whether to use it is the owner's call.
