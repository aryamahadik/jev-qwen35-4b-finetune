# Completeness critic on FINETUNE_PLAN.md (30 Sep 2026)

**Completeness critique of FINETUNE_PLAN.md: 12 gaps and a budget check (research only; no project files edited, no GPU or cloud jobs run)**

Before the gaps, these CPU checks came back clean. The scripts are in `/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad/crit/`.
- **kd targets:** after `kd_skip_src` the count is exactly 43,363, and 238 of them are `gd_gen2_probability` rows.
- **Teacher labels:** choice-row teacher keys equal the options on every row, every sum is 1 ± 0.01, and no yes/no teacher value is invalid.
- **Out-of-sample labels:** the 453,980 `gd_*` rows share 0 exact states and 0 normalised states with any file in 4B-E's lineage (train_v07, v08s2, v09s3, v10s4, v11, v11b, v11c, v13t, train_prism_arms). The 4B-E labels on those rows really are out of sample.
- **Train vs gate-dev overlap:** 12-gram overlap between golden_train and the 9 gate splits is template-level only. It touches pg_dev (107 rows at ≥50% coverage), hard_dev (44) and taskbank_dev (3), and it comes from pg_*/hard_* replay that 4B-E also trained on. It is not a ship-rule bias.

## Gaps, most important first

**1. The ship rule leans toward REF and does not measure what OHS-3 tests.**
- **Evidence (`srcfam.py`, `persplit.py`):**
  - tb_mixtral is 1,087 of the 8,143 pooled dev rows. It has 0 golden rows (excluded under the no-bigger-models rule) but 21,575 rows in 4B-E's lineage; 4B-E scores 84.5 on taskbank vs 75.9 for the frozen base.
  - clinc/banking, pg_* and hard_* (about 2,700 dev rows) have 4-9x more training rows in 4B-E's lineage than in golden.
  - Only 3,847 dev rows come from sources neither model trained on: dev_nc btzsc 1,008, ag_news, emotion, rotten_tomatoes, irony, spam, climate, cb and bbc.
  - The v11r reference for the 2B has the same lean.
- **Consequence:** a model that generalises better can fail "+0.2 pooled", and 4B-E or v11r (with the legacy lineage) ships instead.
- **Fix (before step 0, in `PREREG_FINAL.md` and `gate_dev.py --mode ship`):**
  - Primary test: the same paired group bootstrap on the 3,847 rows with sources unseen by both models (≥ +0.2, lower bound > −0.75).
  - Constraint: the full pooled set with lower bound > −1.0.
  - Report taskbank_dev separately, with a note that the new model is barred from its training family.
  - Add to report-only: JevBench half A (after the C6 `jevbench_od` fix) and p50/p95 latency. `cand_logits` skips CUDA graphs whenever PRISM-X is active, so the 2B's 9 ms p50 no longer holds.
  - Optional, needs the owner: hold out one small source from each of moral norms, tables and claims (about 1% of rows) as a yes/no transfer dev.
- Effect: none on the model; better decisions. Risk: none. Cost: CPU only.

**2. The PRISM-X gate for the 2B ignores security.**
- The gate is accuracy-only (+1.3 pp, lower bound > 0). E_L4 jagged ASR was 19.2%, vs I 5.9% and I_1600 1.1% (ledger X7, X17). The 2B ship rule caps ASR at min(8.8%, v11r + 3) = 6.9%. A layout-E-only 2B would probably fail that cap, wasting the whole 2B pass.
- E_L4_1600 predictions are not local yet, so the gate can still be amended honestly.
- **Fix:** use arm I if dev-confirm vs E_L4_1600 has lower bound > −0.75 AND jagged ASR is lower with the bootstrap lower bound of the reduction > 0. Commit this before scoring.
- Risk: low. Cost: 0.

**3. REF is not re-scored in the same pipeline.**
- 81.49 / 79.84 come from in-process, unmerged predictions on the L4 (`od_gcp.cmd_train`). The candidates will be merged bf16 reads, possibly on another host. Parity between hosts was 99.5% (ledger G1), and merging moves probabilities by up to 0.018 (X3). Both are the same size as the +0.2 bar.
- **Fix:** score REF and every candidate in one job, on one GPU type, with the same merge path, revision and layout. Pre-register "REF = fresh score", not the stored numbers.
- Cost: about 1 L4-hour.

**4. Base revision and tokenizer are not pinned in the labelling and eval paths.**
- `od_gcp.cmd_predict`, `multi_eval_remote`, `teacher_label_remote` and `soup_eval_remote` all call `decoder_io.load(base)` without `revision`. Only training is pinned.
- 4B-E's meta also records the wrong base. The 2B config fills its revision from whatever `main` is at smoke time, not from the arm-I runs.
- **Fix (extend C6):**
  - read `cfg.base` and `base_revision` from `train_meta`, and raise on a mismatch;
  - pass `revision=` everywhere;
  - pin the 2B to the snapshot hash in the L4's HF cache used by arm I and E_L4;
  - set `HF_HUB_OFFLINE=1` on the L4 during labelling;
  - write the sha of the chat template into every preds meta.
- Source: https://huggingface.co/docs/huggingface_hub/guides/download

**5. The packing speed model contradicts the plan's own profiling, and the smoke never tests "no packing".**
- The cost model assumes time is proportional to padded characters. The 30 Sep B200 note says steps are dominated by kernel launches and use only 10-20% of H100 matmul power. At 10240, each batch becomes 2-3 separate forward/backward passes, so packing could be slower on the H100.
- **Fix:**
  - Smoke candidates on the H100: micro_tokens {0 (no packing), 10240, 16384, 24576}, same 100 real batches, measured s/step.
  - Land C1 and upgrade it to must: it is what lets the H100 use its fastest value while the L4 tail uses 10240 without changing the objective.
  - Without C1, the 10240 fallback stands.
- Effect: possibly the difference between 3.34 and 4.6 s/step, i.e. between a full pass and decision 4. Not sure.

**6. The smoke harness cannot run the smoke the plan specifies.**
- `od_gcp.cmd_smoke` trains on `src[:n]` with an empty relations file. So the heaviest real micro-batches, inv-merged units, anchor groups and PRISM-X on long rows are never exercised.
- Host RAM with the full 1.2 GB file (about 500K dicts plus units and replay) is not measured on the L4 VM. I am not sure of the VM's RAM.
- **Fix:** a new `smoke_heavy` entrypoint in both od_gcp and modal_od (these files are not hashed):
  - build a mini train/relations file from the exact units of the top-k batches in the CPU tokenizer replay;
  - run 20 ordinary steps, then one step each;
  - log `max_memory_reserved` and peak RSS (`resource.getrusage`).

**7. The KL anchor is about 7x weaker than in any tested from-base run, over a 17x longer run.**
- Anchor share by mix (`anchor.py`): v07 15.4%, v11 6.5%, prism_arms 6.2%, golden 0.6% (2,965 rows).
- Share of steps with any anchor row: v11 about 1 − 0.935^16.5 ≈ 67%; golden about 9%.
- LoRA forgetting "tends to worsen with training duration": https://arxiv.org/html/2405.09673
- Our own data point: v12t and v13t already lost 1.8-2.6 pp on devzs and dev_nc.
- **Fix (owner picks):**
  - (a) In a derived file, set `meta.anchor=true` on a seeded 6% of clean, non-twin rows from broad classification families. This restores the tested regime, costs about +2% compute (one extra no-grad base forward on those rows), and needs a new `epochs` replay.
  - (b) At minimum: score s002500 / s010000 / s020000 on dev_nc and devzs on a Modal L4 ($0.80/h), and consult the owner if the drop is more than 2 pp vs s002500.
- Effect: not sure.

**8. The label audit comes too late for the 4B.**
- §3.4 runs only before the 2B. A generator bug like D6's (gen_msn_consent, 5,000 rows) would be baked into the one-shot 4B.
- **Fix:** after C6, C7 and C10 land, have 4B-E label a stratified 30K sample (about 150 rows per source, about 2.5 L4-hours). Run the §3.4 group-outlier screen on the generator sources and fix confirmed bugs before step 0. Those labels are reused for the 2B. Per-family 4B-E accuracy from this sample also shows where kd might hurt the 2B.
- Evidence for model-based flagging: https://arxiv.org/abs/1911.00068
- Cost: about $3 plus Claude audit time.

**9. The L4 critical path is not scheduled.**
- One L4 has to handle, in some order:
  - E_L4_1600 plus the TTA test (about 7 h);
  - teacher smoke;
  - labels (about 33 h);
  - the L4 memory and relay-resume pilots;
  - the s002500 check;
  - evals;
  - possibly the 4B tail and the 2B (5+ days).
- **Fix:** write a Gantt with the critical path, move mid-run checks to a Modal L4, and consider a spot L4 for evals. The trainer already checkpoints on SIGTERM.

**10. LR and horizon: the rationale is wrong, and the choice is untested at this length.**
- 7e-5 was used only for 1.6-1.8K steps (v07, v11); this run is 30,457 steps.
- The plan cites https://arxiv.org/abs/2409.19913 against LR changes, but that paper says "longer training necessitates smaller LR" (pretraining evidence).
- Thinking Machines says the LoRA optimum is "higher for shorter training runs", about 15x FullFT for short runs converging to about 10x for longer ones: https://thinkingmachines.ai/blog/lora/
- **Fix:** correct the citation. The owner chooses between 7e-5 as-is and 5e-5 (about 0.7x, the direction both sources point; 4e-5 was used on every 4B continuation run). Effect: not sure, and the regression risk is symmetric.

**11. Citation and consistency fixes.**
- https://arxiv.org/abs/2602.09492 does not claim a large-batch LoRA penalty. The Thinking Machines blog does: cite that instead.
- https://arxiv.org/abs/2608.27729 is about seed collapse in small-model KD (per-seed std 2.8-48.7 pp). That supports "pilots can't resolve w", and it is also a warning that a single-seed 2B KD run can be unstable.
- https://arxiv.org/abs/2502.06761 says averaging complements annealing with "mild" gains. It does not say averaging "converges to the annealed model".
- Rows to label = 501,732 − 79,688 = **422,044** (verified), not 424,693.
- §3.4 uses T = 0.65, which is the 2B arm-I fit. 4B-E's fitted yes/no T is 0.9.
- `kd_full_src` has to match on `r["source"]`: those rows have `teacher_src = None`, while `kd_skip_src` matches on `teacher_src`. C2's "== 238" assert catches this.
- The risk list leaves out the Modal terms §1.3(c) account-policy risk flagged in `logs/relay_protocol.md`.

**12. The 2B's PRISM-X cost is unmeasured on the H100.** The 13-16 h H100 estimate comes from arms A-F, which had no PRISM-X. Add PRISM-X on and off to the 2B smoke to get the overhead.

## Budget math

**Confirmed:**
- ceil(31,358.25 × 0.97123633) = 30,457 steps.
- Warm-up int(0.05 × 30,457) = 1,522 steps; the consistency ramp reaches full weight at step 6,091.
- Snapshots at steps 25,888 / 27,411 / 28,934.
- 3.34 and 4.33 s/step thresholds (cost = s × 40.43 with ×1.21); the 36.6 h trim.
- The $118 case: 22.6 h, ≤ 2.67 s/step, 24,654 steps at 3.3 s/step.
- Modal plan total: 25 + 135 + 65 + 5 = $230.

**Disputed:**
- **"For scale" rows.** They use ×1.10, while the thresholds use ×1.21. Corrected full-pass costs:

  | s/step | Plan says | Corrected (×1.21) |
  |---|---|---|
  | 3.0 | $110 | $121 |
  | 3.5 | $129 | $142 |
  | 4.0 | $147 | $162 |
  | 4.6 | $169 | $186 |

  So 3.5 s/step does not fit $135, and 4.6 needs the trim.
- **No-packing extrapolation.** The 30 Sep note gives 4.6 s/step without packing, so packing must be at least 1.38x faster to fit $135. Given gap 5, decision 4 is likely.
- **2B on the H100.** With ×1.21 it costs $62-76, not $56-70, before any PRISM-X overhead. The $65 cap buys about 13.6 h.
- **2B on the L4.** The plan's 13 s/step is too low. Arm I measured 12.3 s/step (328 min for 1,600 steps) on rows 1.23-1.34x shorter, which gives 15.1-16.5 s/step. That is 128-140 h (5.3-5.8 days) and $115-140, not 110 h and $110-115.
- **L4 total if the 2B runs there.** About 170-190 h (about $155-190) against about $200 of headroom, so there is no room for the 4B tail or a second view.
- **Labels.** Label time about 30-33 h is fine.
- **$118 case.** The $10 pilot line is below the $12-15 of itemised pilots.
- **Cheap budget lever.** Modal lists up to $10k academic credits and startup grants (https://modal.com/pricing). Applying before launch could remove both the relay and the account-policy risk.