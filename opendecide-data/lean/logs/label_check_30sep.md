# Teacher-label checks (30 Sep 2026)

## Shards 10-19 (account arya-mahadik-ai, Modal H100)
- **Completeness:** 211,020 rows (10 x 21,102). Settings are q35_4b_pxE, Qwen/Qwen3.5-4B @ 851bf6e8, schema_branch_mark,
  cygnet, perm_seed 20260930, merged, no TTA.
- **Adapter:** every file of models/q35_4b_pxE on the account's volume has the same sha256 as the Mac backup
  (backups/gcp_models/q35_4b_pxE). adapter_model.safetensors is 1bbd8a79143f7ab5.
- **Numbers vs the L4 audit labels** on the 9,755 overlapping rows (same option order on all of them):
  - argmax agreement 99.63%, which meets the >= 99% bar;
  - mean |dp| 0.00186, which meets the <= 0.005 bar;
  - max |dp| 0.0518, which is over the 0.05 bar by 0.0018.
- **The one row over the bar** is r_gd_semtabfacts_sci_2750: 0.470 on the L4 vs 0.418 on the H100, a near-50/50 row.
  Only 3 rows are above 0.04 and 13 above 0.03.
- **Verdict:** the model files are identical, so the differences come from the GPUs (L4 vs H100, bf16 kernels). The
  labels are accepted. The bar comes from FINETUNE_PLAN 3.2, where it is defined for the dev parity check.

## Shards 0-9 (account aryamhd)
- **Adapter:** identical to the Mac backup (all 6 files have the same sha256).
- **Labels:** pending, the job is still running.

## The kd_full fix in build_2b_kd.py (commits f22b468 and the next one)
- gd_gen2_probability has 478 rows: 238 yes/no rows with exact probabilities, 94 yes/no rows without, and 146 choice
  rows without. All 240 rows without an exact probability are eligible for 4B-E labels.
- **The bug covered the 94 yes/no rows only.** train_decoder uses a yes/no kd_full teacher alone as the target, so
  4B-E's guess would have replaced the gold answer. This matches the audit's count: 332 - 238 = 94.
- The first fix (f22b468) also removed 4B-E from the 146 choice rows. That went too far, because choice rows are
  mixed with gold at kd 0.5 as usual. The second commit restores them.
- Final state: the 94 yes/no rows train on gold only, the 146 choice rows use normal KD, the 238 exact rows are
  unchanged, and expect_kd_full stays at 238.

## Shards 0-9 (account aryamhd): done
- **Completeness:** 211,024 rows. Both halves together make 422,044 rows, which equals the shard manifest.
- **Shards and settings:** a local rebuild of the 20 shards (shard_golden.py) matches every label meta's shard_sha256
  and row count, with 0 mismatches. All 20 metas have one identical settings block.
- **Numbers vs the L4 audit labels** on 5,835 overlapping rows: agreement 99.43%, mean |dp| 0.00114, max |dp| 0.0612
  (2 rows above 0.05). As with shards 10-19, this is GPU numerics on an identical adapter, so the labels are accepted.

## The 2B file (build_2b_kd.py, 4B-E teacher)
- data/v14_parts/train_2b_golden_kd.jsonl: 501,732 rows, sha256 e7b61114b6027b08..., built with check_rows.
- kd_targets: 449,957 = 381,236 fresh + 43,363 human/exact + 25,358 twin copies. kd_full_no_fresh_teacher is 94, and
  kd_full rows are 238.
- runs/q35_2b_main.json: expect_kd_targets = 449957. Rebuild the file and update this number if the new 4B passes the
  gate and relabels, or if hard rows are added.

## Why the two halves differ by 4 rows (211,024 vs 211,020)
- 422,044 rows / 20 shards = 21,102.2, so shard_golden.py gives the first 4 shards one extra row. Shards 000-003 have
  21,103 rows each and shards 004-019 have 21,102 (data/v14_label_shards/shards.json).
- aryamhd (shards 0-9): 4 x 21,103 + 6 x 21,102 = 211,024. arya-mahadik-ai (shards 10-19): 10 x 21,102 = 211,020.
  The sum is 422,044, which equals the manifest.
- No earlier log gives "211,020 + 211,020". The first check counted only shards 10-19 (211,020); the other half was
  still running.

## Teacher roles (agreed with the owner and Codex)
- The 4B-E labels in train_2b_golden_kd.jsonl are the BACKUP teacher.
- If the new 500K 4B passes the ship gate, it relabels the same 422,044 rows (same shards, same settings except the
  adapter). build_2b_kd.py is then rerun and expect_kd_targets updated, and the 2B learns from the new 4B.
- If the new 4B fails the gate, the 2B trains on this file as it is.

## 2B smoke (30 Sep, 22:20 UTC, arya-mahadik-ai, September credit): PASS
- 32 of 32 steps at micro_tokens 16384 with PRISM-X I. Peak reserved memory 25.4 GB (32% of the H100), no OOM.
- trainable (LoRA) 33,638,400, which is now expect_trainable in runs/q35_2b_main.json. trainable_px (PRISM-X) is
  50,547,309.
- The 2B epochs is 0.9712363276890207, the same stream as the 4B: 501,732 rows, 351,122 units, 30,457 steps. It was
  checked with the replay on the 2B file (extra/replay_2b.json).
- Files: extra/smoke2b_h100_mt16384.json and extra/heavy_batches_2b.json.
- The smoke's step times include Triton autotune, so its "3.05 s/step" is not the real speed. The steady steps are
  about 1.6-2.4 s. A 150-step speed test was started to measure it (extra/speed_2b_run.log).

## 2-view teacher labels for choice rows (30 Sep, 22:18-22:50 UTC, aryamhd, September credit, about $10)
- **Job:** extra/modal_label_rev.py re-read all 137,543 choice rows of the 20 shards with 4B-E and the REVERSED
  seeded view: 4 H100 containers, about 24.5 rows/s, 20 of 20 shards done. The views were checked against the stored
  first-read views.
- **Merge:** extra/merge_rev.py, with output in extra/labels_q35_4b_pxE_2view/. Choice rows are averaged over the
  two views and yes/no rows are unchanged.
  - **Flip rate** (argmax differs between the two views): **17.98%**. Mean |dp| is 0.0393.
  - **Accuracy on choice rows:** view 68.05%, reversed 68.08%, **2-view average 69.51% (+1.46 pp)**.
  - The FINETUNE_PLAN 3.2 pre-registered rule (2 views if flips >= 3%, and the 2B trains on the H100) is met.
- **New 2B file:** data/v14_parts/train_2b_golden_kd_2view.jsonl, sha256 1d44fd63d43d80d2..., teacher_src
  q35_4b_E2v.
  - kd_targets 450,170, up from 449,957: the twin copies rise to 22,372 and the twins deleted because the partner
    answered wrong fall to 6,365.
  - The kd_full guard held: 94 rows got no fresh teacher.
- **runs/q35_2b_main.json:** train_file is now the 2view file and expect_kd_targets 450170.
  - The 1-view file train_2b_golden_kd.jsonl is kept.
  - If the new 4B passes the gate and relabels, both of its views must be read (choice rows twice).
  - TODO in the 2B worktree before any 2B GPU run: add the 2view file to V14_KEEP (modal_od.py), and rebuild the
    yn2b arm files from the final teacher file.

## 2B speed and memory (30 Sep, 22:30-22:50 UTC)
- **grad_ckpt on, 16384:** 150 steps at 1.99 s/step (median 1.72, 2.04 including checkpoints), about 17.3 h and
  about $82 (x1.21) for the full pass. File: logs/pilot/speed_h100_mt16384_expect_trainable-none.json.
- **grad_ckpt off, 16384:** OOM at 73 GB, both in the speed test at step 20 and in the heavy smoke at step 17. grad_ckpt
  stays on.
- **The 2B cost estimate rises from $56-70 to about $82-85** (+4% for yn2b rows).

## Checks on the 2-view merge and the yes/no letter swap (30 Sep, 23:00 UTC)
- **Codex's check: are both views mapped to the same option identities?** Yes.
  - On all 137,543 choice rows: 0 key mismatches (the options equal the keys in the view, reversed and 2-view files),
    0 views that are not the exact reverse, and 0 rows where 2view != (view + rev)/2 by option name.
  - Counterfactual: if the rev read were wrongly keyed by display position, its accuracy would be 18.1% (5% sample),
    against 68.1% keyed by option text.
- **Yes/no letter swap** (extra/modal_label_rev_yn.py, shards 10-13, 79,666 yes/no rows, aryamhd, about $2):
  - The first run failed on an options-null check and saved nothing. It was fixed, tested locally end to end, and
    rerun.
  - Flips 3.63%, mean |dp| 0.0236.
  - Accuracy: view 81.16%, swap 81.14%, average 81.25% (+0.09 pp, noise).
  - Share of targets in 0.2-0.8: 41.5% for the view, 41.8% for the average.
  - **Decision (recommended, following Codex):** do NOT add a second view for yes/no.
    - The flip rate is just over the 3% line, but the accuracy gain is about 0 and a full run would cost about $9 of
      October credit.
    - This is recorded as a deliberate choice against the letter of FINETUNE_PLAN 3.2's flip criterion. Reason:
      +0.09 pp is negligible.
    - Choice rows keep the 2-view average (+1.46 pp).
  - The 41.5% share of soft yes/no targets is the arm C lever (gold-only on exact program rows). It is tested in the
    2B A/B.
  - Output: extra/revyn_result.txt.

## yn2b wave 1a done (1 Oct, about 00:50 UTC); details in yn2b/WAVE1A_STATUS.md
- GREEN families:
  - F2 tool_guard: 5,202 train / 524 dev, decide2 100%, blind 130/130;
  - F5 lead_score: 2,160 / 200, decide2 100%, blind 120/120;
  - F3 state_track: 3,780 / 349, decide2 100%, blind 100/100. Its fixed build was written by the orchestrator at
    00:52 UTC with the shas checked (train bfaa171f, dev 5f894a42), the gate green, and the test passing.
- Tools and mv_core GREEN; 535 tests passed.
- Label audit for arm C: the teacher gate moves the share of yes/no targets inside 0.2-0.8 from 36.7% to 14.1%. The
  teacher is wrong on 22.6% of generator yes/no rows (numeric_dates 41.9%).
- **Found: a bug in the FROZEN golden_train.** In gen_numeric_dates, the choice twins reuse the base row's question.
  - It affects 121 raw rows: 73 in the 2B file and 4 in arm S. There are also 12 ambiguous tables rows.
  - The ids are in yn2b/label_audit_known_bad_ids.json.
  - The 4B main run trains on them: 121 of 501,732 rows (0.02%), negligible, and the run is not touched.
  - The 2B will exclude them where the SPEC applies.
- Wave 1b (F1, F6, F4, devx, decontamination, assembly, arm files from the 2-view teacher file) was started at about
  00:55 UTC (workflow wf_4048ca8f-a0d).
