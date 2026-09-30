# Overnight autonomous plan, 28 Sep 2026 (the user is asleep and asked me to handle everything)

Fixed **before** any result is seen, so the choices are not driven by the results.

## Hard limits
- **Money.** At most **$35 of Google credit tonight**, the H, I, J chain included (about $11). No Modal spend. No
  new cloud accounts or GPU types. The kill switch and the VM's 15-hour stop stay on.
- **Held-out data.** Never touch OHS-1, OHS-2, OHS-3 or JevBench half B. Choose only on dev-select; report
  dev-confirm.
- **Models and data.** No bigger models, no Jev outputs used as training data, no new dataset writing.
- **Public actions.** No submission, no Hugging Face upload, no git push.
- **Claude usage.** Mostly waiting: watchers wake me only when an arm finishes or fails.

## Loop
1. **Chain.** Run H, then I, then J (`gcp/run_prismx.sh`). The VM shuts itself down at the end or at the first
   failure.
2. **If an arm crashes:**
   - Read the log, fix the bug, re-copy the code and restart the chain. Finished arms are skipped and a
     half-finished arm resumes from its checkpoint.
   - Allow at most 2 fix attempts per arm, then stop and write it up.
3. **After each arm:**
   - Copy its predictions back and score them against E: `gate_dev.py` for dev-select and dev-confirm, then jagged,
     OPI, redef, breadth, and the switch-off comparison (`_nopx`).
   - Write the results into `budget_ledger.md`.
4. **Pre-set gates, all against arm E:**
   - **H:** dev-confirm at least -0.5 pp, OPI at most 1.3%, jagged at most 8.8%.
   - **I:** dev-confirm at least +1.3 pp, with the lower bound of the interval above 0.
   - **J:** better than I on hard_dev and breadth_dev (dev-select), with no dev-confirm loss.
5. **Follow-up, only if all of these hold:** the chain has finished, tonight's Google spend is under $25, and some
   arm passes its gate or at least equals E.
   - Pick the arm with the best dev-select micro accuracy whose jagged ASR is at most 8.8%.
   - Train it again at **1,600 steps** (epochs 0.4294), same everything else, as `q35_2b_arm<X>_1600`.
   - Reason: all the 800-step arms are under-trained (about -3 pp against the 2B v11r), so this shows how far
     PRISM-X goes with more training. It takes about 7 h and about $6.
   - Score it the same way.
6. **Morning summary** for the user: a short table, pass or fail for each gate, spend, and the next step.

## Update 03:55 UTC (the user set a /goal: keep improving PRISM-X with the architecture only; close the gap to Jev)
- **Budget.** The Google cap for this goal is **$60** (it was $35); about $280 is available. All other limits stay.
- **Queue.** The chain was swapped for a queue (`gcp/queue_runner.sh`, `logs/px_queue.txt`) so experiments can be
  added without the VM shutting down.
- **Arm K, fixed before any H/I/J result (calibration, Jev's biggest lead: Brier 0.038 vs 0.083):**
  - **What:** J plus a per-row confidence temperature (tau = exp(0.75 tanh(w.f)), w = 0 at init, so tau = 1 and
    the model is exactly E) plus a loop ensemble at inference (average the probabilities of loop steps 1..T).
  - **Gate:** yes/no Brier on dev-confirm better than J and better than E; dev-confirm accuracy not below J by more
    than 0.3 pp.
- **1,600-step follow-up (unchanged rule).** Take the best arm by dev-select, whose jagged ASR is at most 8.8%, and
  train it again at 1,600 steps.
- **Order of the night.** H, I, J, then K, then the follow-up. The VM auto-stops at about 18:15 UTC (15-hour
  limit); if a run is cut, restart the VM and it resumes from its checkpoint.

## Update 07:20 UTC, after H (a deviation from the plan, recorded before any I, J or K result)
- H passed on accuracy (+0.25) and improved calibration (Brier -0.010), but failed on security (jagged 17.2% vs E 5.8%).
- **Added a control, `q35_2b_armE_L4`:** arm E re-trained on the L4 with the same micro-batch setup as the PRISM-X
  arms. It measures the hardware and run-to-run spread of every metric. Without it, the H-K security differences
  cannot be interpreted.
- **New queue order:** I (running), E_L4, J, K. I, J and K keep their pre-registered gates.
- **Next hypothesis to separate H's two parts,** if E_L4 confirms the security loss is real:
  - H-shadow-only and H-authority-only, to find which part hurts hijack defence;
  - as a candidate fix, an attacked-twin invariance term routed through the protected path.

## Update 08:00 UTC: arm L (counterfactual evidence), fixed before its run
- **What:** L = H + counterfactual. A no-gradient second pass reads the same question with the text removed. The
  final logits are the logits minus tanh(alpha[qtype]) x log_softmax(no-text logits), with alpha = 0 at init, so the
  model starts exactly as H.
- **Gate:** dev-confirm at least H + 0.3 pp, and yes/no Brier not worse than H.
- **Offline cascade finding, recorded in the ledger:** at inference, architecture reaches 4B accuracy at about 2B cost,
  but not above it.

## Update 11:00 UTC, after I (recorded before L runs)
- I gave +1.26 [+0.15, +2.41] vs E (just under the +1.3 bar), Brier -0.016, OPI 0.8%, jagged 5.9%. It is the best arm
  so far.
- **Change to L: it is now I + counterfactual** (it was H + counterfactual). The gate is now at least I + 0.3 pp on
  dev-confirm, with yes/no Brier not worse than I. This is a design iteration on the best base; the final claim still
  comes only from OHS-3.
- **Follow-up (unchanged rule):** after K and L, train the best arm by dev-select with jagged at most 8.8% at 1,600
  steps.

## Update 13:55 UTC: control result
- E_L4 (arm E on the L4 with micro-batches) is the matched control for H-L: accuracy -0.87 vs E on the H100, jagged
  19.2% (vs 5.8%).
- **From now on, arms are compared with E_L4, the same setup;** the comparison with E is also reported.
- **I vs E_L4:** +2.13 [+0.99, +3.28] on confirm, Brier -0.014, jagged 5.9 vs 19.2%. **I passes.**

## Update 14:05 UTC: PRISM-X on our 4B (fixed before either run)
- **Why:** the 2B alone cannot reach Jev, but our 4B already ties Jev on OHS-2. The most direct test of whether
  PRISM-X can close the gap is adding arm I's parts to the 4B.
- **Pair, identical except for PRISM-X:** both start from `q35_4b_v13t` (the best 4B on dev-select), switch to layout
  E, and train 800 steps on `train_prism_arms` with kd 0.5, lr 4e-5, micro_tokens 10240, on the L4.
  - `q35_4b_pxE`: the control, no PRISM-X.
  - `q35_4b_pxI`: preset I.
- **Gate for 4B-I vs 4B-E:** dev-confirm at least +1.0 pp with the lower bound above 0; yes/no Brier not worse;
  jagged ASR not worse by more than 3 pp. v13t (text-first layout) is also reported as a reference.
- **Queue order:** J (running), 4B-E, 4B-I, K, L, then the 2B follow-up. Budget check: about $30 of the $60 is left;
  this pair costs about $9.5.

## Update 15:05 UTC: PRISM-Omega arms (fixed before their runs)
- **O1 = I + policy compiler.** At each decoder layer, the mean hidden state over trusted SCHEMA tokens (causally
  independent of the text) is compiled, through a shared encoder and a per-layer zero-init map, into a FiLM scale
  and shift. These apply only to tokens after the trusted prefix: h + h*g + b*RMS(h).
- **O4 = I + action tower.** A CLM-style two-tower score <A q_i, B c> between each trusted option query and the
  decision state; A = 0 at init.
- **Gate for each, vs I (same L4 setup):** dev-confirm at least +0.5 pp with the lower bound above 0, the same
  direction on dev-select, yes/no Brier not worse, jagged ASR not worse than I by more than 3 pp.
- **Queue:** J (running), O1, K, L, O4, then the 4B pair last (about 27 L4 hours; total spend stays under the $60
  cap).

## Update 17:35 UTC: J failed its gate (fixed before the next runs)
- **K is replaced by KI = I + confidence temperature** (no loop and no loop ensemble, since the loop underperformed).
  - **Gate:** yes/no Brier at least 0.003 better than I on dev-confirm; accuracy not below I by more than 0.3 pp.
- **The loop is parked.** It may return for a longer run, because it helped on hard_dev (+3.8).
- **Queue:** O1 (running), KI, L, O4, then the 4B pair.

## Update 21:50 UTC: O1 failed (-1.88 vs I)
- **O1b** (fixed before its run): I + the policy compiler capped at +-0.1, lr 1e-4. It has the same gate as O1.
- **The 4B pair moves to the A100 phase** (lean plan), to stay under the $60 cap.
- **Queue:** KI (running), L, O4, O1b. Then a combination of I and every part that passed, and a 1,600-step
  confirmation of the final design.

## Update 01:20 UTC, 29 Sep: KI failed; follow-up fixed now
- The follow-up rule (best dev-select arm with jagged at most 8.8%) picks **I** (dev-select 73.89).
- **Queued after O4 and O1b:**
  - `q35_2b_armI_1600` (I at 1,600 steps, epochs 0.4294);
  - `q35_2b_armE_L4_1600`, the matched control (E on the L4 at 1,600 steps).
- **Gate:** I_1600 vs E_L4_1600 on dev-confirm at least +1.3 pp with the lower bound above 0. This tests whether
  PRISM-X I's advantage survives longer training.
- **Spend:** $20.09 since 27 Sep. The remaining queue is about 24 L4 hours, about $21, so the total stays well under
  the $60 cap.

## Update 03:50 UTC, 29 Sep: the user asked not to waste GPU time
- The decisive pair (I_1600 vs E_L4_1600) now runs right after L.
- O4 and O1b move behind it, since their predicted chance of passing is only about 15%. They may be replaced by
  research-driven arms.

## Update 05:00 UTC, 29 Sep: research round and yes/no finding (fixed before these runs)
- The deep research round (6 angles, synthesis, critique) plus free maths show the gap to Jev is **yes/no accuracy**,
  not calibration error.
- **New queue order:** L (finishing), then the **4B pair** (4B-E control and 4B-I, from v13t, 800 steps, the gate as
  written earlier), then **I_LS0** (I with label smoothing 0 and teacher T yes/no 0.9, T fitted on dev-select;
  paired with I on the same seed; gate: yes/no Brier at least 0.005 better than I, accuracy not below I by more than
  0.5), then the 1,600-step pair.
- **Dropped:** O4 and O1b (predicted neutral).
- **Disclosure:** the OHS-2 yes/no breakdown informed these priorities. OHS-3 remains untouched.

## Update 18:50 UTC, 29 Sep: 4B-I result and the frozen design
- 4B-I is about equal to 4B-E (select +0.59, confirm -0.59). Gate FAIL.
- **Frozen design:**
  - **4B:** layout E, plain (no PRISM-X).
  - **2B:** PRISM-X I (layout E + authority signal + shadow memory + option queries).
  - **Serving:** cascade, with post-hoc per-type temperature.
- The remaining L4 queue (2B I_LS0 and the 1,600-step pair) only refines the 2B recipe.
- **Next big step:** the main 4B training on golden_train (500K, 1 full pass) on a rented H100/B200 or the Modal refill.

## Update 20:00 UTC, 29 Sep: 4B->2B distillation recipe (deep research: 6 angles + synthesis + critique)
- **Expected:** the 2B gets within about 1-3 pts of the 4B (fair gap now 5.25: v11r 76.24 vs 4B-E 81.49). The
  remaining gap is knowledge; the 2B can match the 4B on calibration and security. The 2B alone beating Jev on
  accuracy is unlikely (<25%), so the cascade is the headline system.
- **Recipe, in priority order:**
  1. Teacher labels from the 4B, out of sample (from 4B-E before the main run, or check memorisation). Use 2 views
     (original + 1 permutation); add the negation view where it is an exact complement. First measure the 4B's flip
     rate; skip averaging if it is low.
  2. Consistent teaching: 1 pass over the 500K with a random view per row, each with its own teacher label. Start
     from merged v11r with the PRISM-X I heads re-warmed. Add a 2nd pass only if the learning curve and time allow.
  3. Target y = w*p_teacher + (1-w)*g, with g = vote share or gold. w = 0.7 where the teacher is right and 0.4-0.5
     where it is wrong; tune on dev-select. Label smoothing 0.
  4. Attack twins: KL(teacher clean || student attacked), only where the teacher's clean answer is correct and not a
     boundary case.
  5. Post-hoc per-type temperature on the 2B.
  6. Measure: H100 smoke run for speed, 2 seeds, paired CIs; a 20K-row pilot A vs B; score the cascade too.
- **Do not use:** DKD/DIST (they degenerate at K = 2), hidden-state matching (below logit KD in 2026 evidence),
  on-policy methods (generation only), hard-only sampling.
- **Compute:** about 40-50 H100-h for 3 passes; plan 1 pass (about 15-20 h) first.

## Update 01:10 UTC, 30 Sep: architecture-only yes/no attempt on the 4B (fixed before the run)
- **Why:** the gap to Jev is yes/no. Test-time augmentation on the best 4B (4B-E): read every question twice, with
  the options reversed and, for yes/no, the Yes/No letters swapped, then average. Inference only; latency about 2×
  (still far under Jev's 239 ms).
- **Where:** the L4, automatically after the 1,600-step queue (`gcp/after_queue.sh`), on the 9 gate dev splits.
  Then the VM shuts down.
- **Adopt in serving if**, vs the stored single-read 4B-E predictions on dev-confirm: accuracy at least +0.3 pp or
  yes/no at least +0.5 pp, with yes/no Brier not worse. Checked on dev-select in the same direction.

## Update 30 Sep, the user's instruction: PAUSE POINT
- Finish I_1600 vs E_L4_1600 and the 4B TTA test, freeze the design and prepare the 500K run config.
- **Then PAUSE: do not start the 500K fine-tune or spend on a big GPU.**
- The user arranges the GPU and says when; resume exactly there (4B main run, then 2B distillation, then OHS-3).

## Update 30 Sep, the resources for 1 Oct (user)
**Resources:** only the L4 plus $118 of Modal credit (4 accounts).

**Plan:**
- **Modal H100 relay:** the 4B main run (from base, layout E, 1 pass, label smoothing 0.05). Checkpoint handover at
  about $28 per account.
- **L4:** 4B-E teacher labels (out of sample), then the 2B (from base, PRISM-X I if I_1600 passes, else layout E).

**Smoke tests first, on both machines:**
- **4B on Modal:** OOM check on the longest rows (max 22.5K characters), loss falling, speed, stop/resume, and the
  cross-account resume.
- **Teacher on the L4:** matches the stored 4B-E predictions; flip rate; speed.

**Rules:**
- Total 4B steps are fixed from the measured speed so the schedule completes in budget; trim rows up front, never stop
  mid-schedule.

**Open items:**
- Jev's OHS-3 answers are not collected yet (they need the rotated OpenRouter key).
- Google credit headroom is about $200 before the kill switch, against an L4 need of about $170, so consider a spot L4.

## Update 30 Sep: 500K cost model from measured step times (H100, no packing)
**Measured time per padded character per step:**
- 4B: 0.052 ms per 1K padded chars (v11 3.23 s/step, v11c 4.13 s/step; v12t 0.047).
- 2B: 0.024 ms per 1K padded chars (v11, v11r, arms A-F).

**Golden set:**
- Rows are about 45% longer than the v11 mix.
- A 16-row batch pads to 88,957 chars. One pass = 501,732 / 16 = 31,358 steps.
- Without packing: 4B about 4.6 s/step, about 40 h; 2B about 2.2 s/step, about 19-20 h.
- Micro-batch packing (micro_tokens 8-16K, the same maths, already used by 4B-E on the L4) cuts padded tokens to
  0.55-0.67x. Expected: 4B about 26-32 h, 2B about 13-16 h. The H100 packing gain must be measured in the smoke run.
- The L4 is about 7x slower: 4B 19 s/step (a tail fallback only); 2B about 13 s/step, about 4.8 days.
- causal_conv1d is not installed (the PyTorch reference path); a possible extra speed-up, to test.

**Plan with $150 of Modal credit:** the 4B on the H100 (any shortfall finishes on the L4 by resume); labels, then the
2B, on the L4.

**Plan with $210:** the 4B, then the 2B on the H100; the labels on the L4 in parallel; any shortfall of the 2B finishes
on the L4.

## Update 30 Sep: B200 vs H100 (research workflow, 3 agents, web sources)
**Verdict:** B200 is about 1.45-1.6x faster than the H100 for our workload (range 1.2-1.9x). Break-even at $6.25 vs
$3.95 is 1.58x, so the cost per run is about equal or worse.

**Why:** our steps use only about 10-20% of the H100's matmul power. They are dominated by kernel launches,
memory-bound work and the fla GDN kernels, and those parts get little faster on a B200.

**Risks:**
- Open fla Blackwell GDN correctness issues (#790, #948) could make a run train wrong without any error.
- Modal may silently upgrade an H100 request to an H200 at the H100 price.

**Decision:** stay on the H100.

**Extra speed-ups to test in the smoke run:**
- Install causal-conv1d. HF #48718: Qwen3.5 step 0.58 -> 0.49 s; we run the PyTorch reference path now.
- Micro-batch packing.

## Update 30 Sep: relay research done (see logs/relay_protocol.md)
The resume maths is correct: step, adapter, AdamW, LR, RNG and exact data replay are all restored.

**Critical gaps to fix before any relay:**
1. A fingerprint mismatch silently starts from step 0, then deletes the copied checkpoint.
2. `set_peft_model_state_dict` is called with strict=False and its result is ignored, so a bad load leaves LoRA at
   init without any error.
3. Packages are unpinned in image35 (peft 0.21.1 came out today; account 1 has 0.21.0), and the base model has no
   revision pin.

**Also needed:**
- Hash the data and code into the fingerprint, and check the optimizer's parameter names.
- Commit the Volume after each checkpoint.
- Add `stop_after_min` and a SIGINT flag; checkpoint every 5 min.
- Use `gpu="H100!"` (plain H100 can be upgraded to an H200).
- Keep one frozen config JSON, keep a manifest of sha256 checksums, and add a CPU resume test.

**Proof test before the run (pre-registered):** A1 and A2 each run 300 steps straight; B runs 150 steps, relays to
another account, then runs 150 more. Pass criteria:
- the lr, counts and batch hashes are identical;
- d(A1, B) ≤ 1.5 × d(A1, A2) for the weights, and the same for the loss curve.

**Open question:** the O1 resume on the L4 showed step losses that differed after resuming, so the relay counts as
unproven until the test passes.

## Update 30 Sep, 03:00 UTC: relay fixes implemented (code only, no GPU)
**train_decoder:**
- A mismatch now raises (config, data sha256, env, code) instead of starting fresh.
- Trained tensors are saved and loaded by name, with a sha256 check. The optimizer order is checked. The replay is
  verified (py/twin RNG and the last batch).
- manifest.json holds per-file sha256.
- New knobs: stop_at_step / stop_after_min (a planned stop) and expect_resume. SIGINT/SIGTERM save at the step
  boundary, then raise.
- Other fixes: the _ckpt.old clean-up, on_ckpt (vol.commit), the final save order (meta, commit, then delete the
  checkpoint), and no_overwrite.

**decoder_io.load:** a revision= argument.

**modal_od:**
- PINNED35: all 88 packages pinned exactly, as in the 25 Sep image.
- Data upload filtered with _data_ignore.
- train_relay35: gpu "H100!", timeout 10 h, commit after every checkpoint.
- A `relay` entrypoint that reads the frozen config `runs/q35_4b_main.json` (DRAFT; open items in runs/README.md).

**Tests:** tests/test_resume.py. A 3-segment relay is bit-identical to a straight run on CPU. A preemption signal
resumes exactly. Every mismatch raises. Mutation checks (drop the RNG restore, drop the optimizer load, replay one
batch fewer) are all caught. 71/71 tests pass. An adversarial review is running.
- Review (13 agents, adversarially verified): 6 real issues, none affecting accuracy. All fixed:
  - one flag read per step (signal race);
  - an absolute deadline stop_at_unix set by relay(), so a preemption restart keeps its end time;
  - the final save sits inside the signal guard, and the checkpoint delete is atomic (_ckpt.done);
  - the smoke run never resumes;
  - the data-upload filter applies to both images.
  73/73 tests pass.
- 4B config: `kd` 0.5 with `kd_skip_src` ["blend50"] (new trainer filter, tested).
  - This uses only the 43,363 human vote-share rows. The 45,103 old model-teacher rows (teacher_src blend50) are
    dropped, per the "no old-teacher kd" rule.
  - Correction: GOLDEN_CARD's "88,228 annotator soft-label rows" counts both kinds.
- Still open: micro_tokens and lr. Both are measured in the smoke run.

## Update 30 Sep, ~06:00 UTC: FROZEN ROADMAP (user + Codex + Claude agree)
1. The matched 1600-step pair (PRISM-I vs plain 2B) decides the 2B architecture. Use PRISM-I only if it keeps a real
   matched advantage (the pre-registered gate is +1.3 pp with a lower bound above 0). Then the 4B TTA test.
2. **Dataset frozen at 501,732 rows; no new sources.** Weak yes/no families (moral norms, tables/fact-checks, science
   claims) get a modest 1.5-2x weight, never 4-5x (earlier narrow-data rounds hurt generalisation).
3. **Pilot on Modal, about $20:** switching (A1/A2/B), throughput and packing, plus a short LR comparison if the
   research supports it.
4. **Final 4B:** layout E, 501K, 1 pass, settings from FINETUNE_PLAN.md (research).
5. **Gate on dev-confirm vs 4B-E (81.49):** overall up, yes/no clearly up, choice not materially down.
6. **Teacher:** if the new 4B passes, it produces teacher probabilities on the TRAINING rows only (standard
   distillation); if it fails, 4B-E is the teacher. Labels run on the L4 (free).
7. **2B targets:**
   - rows with human vote shares: the human distribution;
   - other rows: gold mixed with the 4B's soft distribution.
   Final 2B = PRISM-I (if step 1 passes), else layout E.
8. Cascade threshold and per-type temperature: dev only, on the L4.
9. Fingerprint and freeze everything, then OHS-3 once vs Jev.

**Budget (Modal $300):**
| Item | Budget |
|---|---|
| Pilots | $15-25 |
| 4B | $120-135 |
| 2B | $50-65 |
| Gate / evals | about $5 |
| **Reserve** | **$40-60, untouchable** |

Teacher labels, the cascade and OHS-3 run on the L4 so the reserve holds.

## Update 30 Sep, 06:30 UTC: PRISM-X gate for the final 2B, amended BEFORE E_L4_1600 is scored
**Status when fixed:** E_L4_1600 was at step 500 of 1600, and no predictions from it existed locally.

**Why amend:** the research critic (logs/finetune_research_critic.md, gap 2) found that the accuracy-only gate ignores
PRISM's main role in the 2B, which is security. A layout-E-only 2B (E_L4 jagged ASR 19.2%) would likely fail the 2B
ship rule's ASR cap (6.9%).

**Decision rule:** use arm I in the final 2B if (a) OR (b); otherwise layout E only.
- (a) The original gate passes: I_1600 vs E_L4_1600 on dev-confirm ≥ +1.3 pp with a lower bound > 0 (reported
  regardless).
- (b) Both of these hold:
  - Accuracy is non-inferior: the dev-confirm difference has a lower bound > −0.75 pp.
  - Jagged hijack ASR is lower, with the paired bootstrap lower bound of the reduction > 0.

  In addition, the OPI ASR increase must not be significant: the bootstrap lower bound of the increase must be ≤ 0.

## Update 30 Sep, 07:15 UTC: research applied (code only, CPU)
**Research** (37 agents): FINETUNE_PLAN.md, critic in logs/finetune_research_critic.md, items in
logs/finetune_research_items.json.

**Implemented:**
- **train_decoder** (C1-C5):
  - aux_norm "batch" (packing-invariant loss);
  - KNOWN_KEYS unknown-key refusal; expect_trainable / kd / kd_full checks; the float32-masters check; a style check;
    a layout guard after the model load; check_rows validates teacher distributions;
  - grad-norm NaN guard before opt.step, plus gn / gn_med / clip_frac logging, ALERTs and _ckpt_good;
  - snapshots (with train_meta.json);
  - kd_full_src.
- **decoder_io / od_gcp / jevbench_od** (C6-C10, agent A): layout/style/revision resolved from train_meta, predict
  perms, tta_choice, od_gcp relay (L4 tail), sharded resumable label command, shard_golden / build_2b_kd / flag_labels.
- **modal_od** (agent B): smoke_heavy, speed, relay --name-suffix / --log-every; replay_steps.py, rank_microbatches.py,
  pilot/RUNBOOK.md, pilot/compare_relay.py.

**Checks:**
- Tests: 179 pass.
- Real data: check_rows passes on all 501,732 rows with 43,363 kd targets.
- replay: 30,457 steps = one pass.
- Pre-pass: 0 of 30,457 batches have a relation split across micro-batches at 10240 / 12288 / 16384 / 24576 (terms:
  36,958 comp, 1,922 equiv, 35,214 inv).
- Heaviest micro-batch: 23,296 tokens at 10240.

**runs/q35_4b_main.json** is set to plan 2.1: r16 / a32, epochs 0.97124, aux_norm batch, kd_full, snapshots, expect_*.
Owner decisions are listed in runs/README.md. An adversarial code review is running before the pilot.

## Update 30 Sep, 08:00 UTC: code review before the freeze (26 agents)
17 issues were confirmed (4 major, 13 minor), none in the loss maths. All are fixed, each with a test. The suite now
passes: 197 passed, 1 skipped.

**Trainer and loader:**
- `_ckpt_good` freezes after any alert and is never copied on the preemption path.
- On resume, snapshots newer than the resume step are moved aside.
- `_ckpt/adapter` holds the tokenizer and a snap.json with the cfg, so it loads on its own.
- The manifest is checked only on the path that resumes.
- decoder_io takes the tokenizer from the adapter only if the adapter has one.
- `label_smooth` is removed from the 4B config, which restores the tested recipe (MNLI yes/no 0.08).

**Tools:**
- soup_eval and multi_eval get layout, style and revision from each adapter.
- Label shards: settings are checked across all shards, the base commit is pinned, and content hashes decide what is
  done.
- Snapshot names are flattened in predict and blend.
- `_data_ignore` keeps the 2B training file and skips the label shards.
- Pilot containers are single-use.
- compare_relay checks that A1 and A2 ran straight through.
- RUNBOOK fixes.
- image35 is pinned to Python 3.12.10, the version builder 2025.06 gives on all accounts.

## Update 30 Sep, 10:35 UTC: PRISM-X decision for the 2B (pre-registered rule applied)
I_1600 vs E_L4_1600:
- **Accuracy:** dev-confirm −0.27 pp [−1.34, +0.79]; dev-select +0.85 [−0.15, +1.87].
- **Jagged ASR:** 1.1% vs 10.0%, a reduction of 8.9 pp [5.7, 12.0].
- **OPI:** +1.3 [−0.7, +3.6].

(a) fails, and (b) fails on the accuracy margin (lower bound −1.34 < −0.75). **Decision by the rule: the final 2B uses
layout E without PRISM-X.** Report this to the owner, with the security trade-off, as an override option. It is the
owner's call, because the rule was ours and the security gain is large.

## Update 30 Sep, 11:30 UTC: DESIGN LOCKED
- **4B:** layout E, no PRISM-X, no TTA.
- **2B:** layout E (PRISM-X I not adopted by the pre-registered rule; the owner may override for security, at a
  speed cost).
- **Serving:**
  - the final 4B alone is the accuracy system (plan S10);
  - the 2B is the fast tier (cascade only if the cost rule passes);
  - per-type temperature on dev-select if it passes the plan 5.1 check;
  - no TTA (X19).

Next: the Modal pilot, waiting for the user's direct confirmation (the auto-mode classifier blocked continuing the paid
steps). The memory smoke on jaypatil-duke finished with exit 0; its results have not been read yet (same block).

## Update 30 Sep, 12:25 UTC: teacher-pipeline parity (L4, new decoder_io)
4B-E single read through the new `predict` path vs the stored in-training predictions, 8,143 dev rows:
- argmax agreement 99.57% (limit ≥ 99%);
- mean |dp| 0.0012 (limit ≤ 0.005);
- accuracy 80.72 vs 80.66 (limit: within 0.3 pp).

max |dp| is 0.099; only 3 rows are above 0.05, all bf16 path noise (pg_dev ×2, devp_card).

**PASS in substance.** The labelling pipeline reads 4B-E correctly: layout resolved from train_meta, pinned
revision. The 15,590-row audit labelling is running.

## Update 30 Sep, 12:30 UTC: OWNER DECISION, PRISM-X I FROZEN for the final 2B
The owner chose full PRISM-X I for the 2B:
- security: hijacks 1.1% vs 10.0%;
- accuracy tied;
- a plain 2B would fail the 2B ship-rule attack cap.

This overrides the accuracy-only pre-registered rule (X18), and the override is recorded.

**Architecture fully frozen:**
- 4B = layout E;
- 2B = PRISM-X I;
- no TTA.

2B config draft: runs/q35_2b_main.json (arm I's regime).

## RECOVERY NOTE, 30 Sep 12:35 UTC (the owner closes the laptop; local jobs may pause)
**State:**
1. **L4 audit** (4B-E labels on 15,590 rows in data/v14_audit_shards) is running on the VM. `stop_after_audit.sh`
   shuts the VM down by itself after "AUDIT END". Results stay on the VM disk.
   - To fetch: start the VM, then scp `~/lean/data/v14_audit_shards/labels_q35_4b_pxE` and `~/lean/logs/audit_*.log`,
     then stop the VM. The parity predictions were already fetched.
   - Then run `flag_labels.py` (plan 3.4 screen) on the labels.
   - The local watcher (buabt5q1j) may miss the fetch; do it by hand.
2. **Ship-rule fixes** (workflow wf_c1736313-7ec). If interrupted, resume with Workflow scriptPath
   `.../workflows/scripts/ship-rule-fixes-wf_c1736313-7ec.js` and resumeFromRunId wf_c1736313-7ec. Then run the tests.
3. **Modal pilot:** step 1 (memory smoke, jaypatil-duke) ran, exit 0. Its log is logs/pilot/smoke_heavy_run.log and
   logs/pilot/*.json, NOT READ: the auto-mode classifier requires the owner's direct "go pilot" first. Steps 2-5
   (speed, relay proof) wait for "go pilot". After the pilot: report and PAUSE (no 4B main run).
4. **Architecture FINAL:** 4B = layout E; 2B = PRISM-X I (owner, 12:30 UTC).

## Update 30 Sep, 12:50 UTC: ship rule built, reviewed, fixed and re-verified
The ship rule is `gate_dev.py --mode ship / c3trigger / refparity`, with PREREG_FINAL.md (DRAFT, for owner review).

**Review and fixes:** the review found 10 defects, all fixed and verified. The verifier then found two residual holes,
which I closed:
- a wrong --size is now checked against the base in the preds meta;
- the refparity look records the sha256 of the fresh REF files, and ship refuses if they change.

**Other fixes:**
- An attack rate with 0 eligible items is UNMEASURED, not PASS.
- calibrate.py marks `_cal` metas with path=calibrate.

**Tests:** 226 passed.

**Owner defaults, flagged in PREREG section 10:**
- constraints use the full set minus tb_mixtral;
- the half condition applies to the full set;
- the unit is group_id.

## Update 30 Sep, 15:50 UTC: label audit (critic gap 8) done on the L4
4B-E labelled the 15,590-row stratified sample (104 sources, at most 150 per source) in 75 min. The VM stopped itself;
the labels were fetched by hand because the laptop was asleep.

**flag_labels screen:** 12,732 rows screened (2,858 designed-hard rows skipped), 775 flagged.

**Top outlier groups:**
- **gd_uds_ordinal** (10-19 options): 72.5% flagged, suspicious;
- **helpsteer2_attr / helpsteer3_pref / mtbench_human / clickbait / sarcasm / politeness:** subjective human votes,
  disagreement expected;
- **meganegraising, gd_gen_msn_consent** (15.6%; the generator that had the 29 Sep bug), **smcalflow_action,
  ncbi_disease:** elevated.

A workflow (wf_c7eb161b-6f8) is auditing 12 groups × 30 rows, plus their builder code, for SYSTEMATIC pipeline bugs,
with a verifier on any claimed bug. The rules: fix only pipeline bugs, and never relabel human data.

## Update 30 Sep, 16:05 UTC: label audit verdict, NO pipeline bugs
12 flagged groups audited (374 rows, 30-45 per group, plus builder code and raw source data): **0 systematic pipeline
bugs.** 15 rows (4%) looked wrong (single annotator errors, never relabelled) and 70 were ambiguous (subjective/noisy
tasks).

**Why the flag rates are high:**
- gd_uds_ordinal: soft, noisy crowd durations; the model's prior mismatch; one-hot-teacher vote gaps.
- helpsteer2: the model is too lenient on "is this correct?", and the humans were right. This is exactly what training
  should teach.
- gd_gen_msn_consent: 0 wrong of 45 rows; 13 edge cases out of 5,161 (0.25%).

**Optional scope item (not a bug; not applied):** the 71 uds 'was_used' rows, where raters read "used" as "involved
in".

**Decision:** the golden data stays as frozen. golden_train.jsonl is unchanged.

## Update 30 Sep, 16:20 UTC: L4 stockout (us-central1-a)
- Starting od-l4 fails with STOCKOUT. The disk and results are safe; everything needed is already fetched.
- The optional 2B PRISM-vs-plain latency check is deferred.

**Risk for the plan:** labels, evals and the 2B/4B tail need the L4.
- Retry later (grab_l4.sh / other zones via a disk snapshot, as on 28 Sep).
- Or use a Modal L4 at $0.80/h. The 422K labels would cost about $29 Modal, from the reserve, and need the owner's OK.

## Update 30 Sep, 16:45 UTC: pilot step 1 read (the owner asked about "that run")
The memory smoke ($2.36) passed at 10240 / 16384 / 24576 and hit OOM with no packing. It ran at 4.26 s/step at 10240,
which would make a full pass about $172 (over $135).

**Speed levers for step 2:**
- causal-conv1d: SKIPPED. Source only on PyPI; it needs an nvcc build for torch 2.14 / cu130. Risky.
- **grad_ckpt off.** The memory smoke used only 35% of the H100 at 10240. Recompute costs about 25-30% of step time,
  and turning it off changes no maths. Needs the heavy-batch memory re-check.
- Smaller micro_tokens (8192).

modal_od now takes `--override '{"grad_ckpt": false}'` for pilots.

**Planned step 2 (on "go pilot", about $5):**
- smoke_heavy --micro-tokens 8192,10240 --override '{"grad_ckpt": false}';
- speed --micro-tokens 8192,10240 with and without the override.

**Then step 3:** the relay proof (about $6). Pilot total about $13, under the $15 cap.

## Update 30 Sep, 17:00 UTC: PILOT DONE, ALL PASS. PAUSED for owner review (pause rule)
- **Speed:** 2.77 s/step at 8192 (about $113 for the full 4B).
- **Memory:** OK at 8192 (36%).
- **Relay:** PASS. B ≈ A1 as closely as A1 ≈ A2; every exact check matched after a cross-account resume.
- **Config:** micro_tokens set to 8192.

**Ready but NOT started (the owner decides):**
- 4B main run: `modal run --detach modal_od.py::relay --config runs/q35_4b_main.json --stop-after-min <m>` on
  account 1.
- Teacher labels on Modal: `modal_od.py::label --shards 0-9 / 10-19` on arya-mahadik-ai / aryamhd. The 4B-E adapter
  must be uploaded to each account's Volume first.
- Before the 4B: commit and freeze the code (plan 2.3 freeze procedure), and `chmod 444` the golden files.

## 30 Sep, 17:45 UTC (1:45 pm EDT): OWNER GO. MAIN 4B RUN STARTED + TEACHER LABELS
- **4B:** `q35_4b_main500k` segment 1 on jaypatil-duke (stop_after_min 290, so it stops about 6:35 pm EDT at about $21).
  - Startup checks OK: rows 501,732; kd 43,363; kd_full 238; trainable 32,464,896.
  - Step-0 loss 0.9367, identical to the pilot.
- **Labels:** 4B-E, perm_seed 20260930, merged, pinned revision.
  - Shards 0-9 on aryamhd; shards 10-19 on arya-mahadik-ai.
  - Both built the identical shard set (422,044 rows, 20 shards) in the container.
- golden_train / golden_relations set to chmod 444.
- **Code freeze:** the 4 hashed files must NOT change until the run ends.
- **Next relay:** when segment 1 stops, download _ckpt from jaypatil-duke and verify it (re-download on a manifest
  mismatch), upload to arya-mahadik-ai, then relaunch with --expect-resume.
