# Frozen run configs (relay runs across Modal accounts)

Each file sets every key. `modal_od.py::relay` (Modal) or `od_gcp.py relay` (L4 tail) reads it, and only the stop point
and `--expect-resume` come from the command line. The trainer refuses unknown keys, and refuses to resume if the
config, data, code or software differ.

## q35_4b_main.json: FINETUNE_PLAN.md section 2.1, applied 30 Sep
The research round's verified changes are applied:
- `r16`/`alpha32` (the tested from-base setting);
- `epochs` 0.97124, exactly one real pass of 30,457 steps (checked by replay_steps.py);
- `aux_norm` "batch" (the loss does not depend on packing);
- `kd` 0.5 on the 43,363 human soft-label rows, with `kd_skip_src` blend50;
- `label_smooth` REMOVED (code review, 30 Sep): the per-source default is exactly what 4B-E, v11 and arm I trained
  with (0.05; MNLI yes/no 0.08);
- `kd_full_src` for the 238 exact-probability rows;
- snapshots every 2,500 steps and at 85/90/95%;
- startup `expect_*` checks.

**Still set by the pilot:** `micro_tokens` (candidates 0 / 10240 / 16384 / 24576; the fastest allowed value) and
whether to install causal-conv1d.

**Owner decisions (current values in the file):**
1. **Weak yes/no family weight:** 1.0x now. The roadmap said 1.5-2x; the research recommends 1.0x (earlier in-family
   gains did not transfer).
2. **`lr`:** 7e-5 now. The critic notes that 5e-5 is the direction the evidence points for a run 17x longer.
3. **KL anchor share:** 0.6% of rows. Tested runs had 6%. Options: add anchors on a seeded 6% of rows (+2% compute),
   or monitor snapshots on dev_nc/devzs.
4. **Cost cap:** if a full pass costs more than $135, give the 4B up to $175 and move the 2B to the L4, or trim
   uniformly.

## q35_2b_main.json: DRAFT. PRISM-X I FROZEN by the owner (30 Sep, 12:30 UTC)
- **Owner decision:** the final 2B uses full PRISM-X I: layout E + authority signal + shadow memory + option-query
  head.
  - Evidence (ledger X18): accuracy ties the plain 2B (−0.27 [−1.34, +0.79]); jagged hijack 1.1% vs 10.0%
    (−8.9 pp [−5.7, −12.0]).
  - A plain 2B would fail the 2B ship rule's attack cap (6.9%).
  - This overrides the pre-registered accuracy-only rule. The owner's reason is security; the cost is a slower 2B
    (no CUDA graphs with PRISM-X).
- **Arm I's tested regime:** from base, r32/a64, lr 1e-4, loss weights 1/1/0.5, kd 0.5, no `label_smooth` key (the
  per-source default), `aux_norm` "micro" at micro_tokens 16384.
- **base_revision:** 15852e8c…, the L4 cache snapshot that arm I and E_L4 used.
- **Still FILL:** `epochs` (replay on the built 2B file), `expect_trainable` (2B smoke), `expect_kd_targets` (the
  build_2b_kd print). The trainer refuses to run until these are filled.

## q35_4b_fix2.json: the 4B top-up C4 = q35_4b_main500k_fix2 (draft amendment A8-prime, 2 Oct)
One pass over `v14_parts/fix2_train.jsonl` (42,570 rows: F7 nested negation, v2 r6, and a 70% stratified replay of
C1's own golden_train rows; no part (ii); `extra/build_fix2.py`, `data/v14_parts/fix2_counts.json`),
continued from C1's adapter (`q35_4b_main500k`, adapter_model.safetensors sha256 507d1c29…), uploaded to the Volume
folder `models/q35_4b_main500k_init` (`extra/fix2_spawn.py::fix2_upload_init`).

**Same as the main run** (checked by `extra/fix2_spawn.py`, key by key): base and revision, recipe A3, batch 16,
r16 / alpha 32 / dropout 0.05, QWEN35 targets, lam 1, beta 1, kd 0.5, `kd_skip_src` ["blend50"], `kd_full_src`,
lam_inv 1.0, sym_cons, perm_twin 0.3, lam_p 0.5, aux_norm "batch", grad_ckpt, style cygnet, layout E
(`schema_branch_mark`), micro_tokens 8192, `expect_trainable`, ckpt_every_min 10. The code is the main run's frozen
code (train_decoder, decoder_io, prism_x, writeblock sha256 = C1's train_meta "code").

**Different, and why:**
- `init_adapter`: C1, byte-identical to the gated read (A8-prime B). The optimizer is fresh (C1's AdamW moments are
  not carried over).
- `lr` 2e-5 peak (the main run peaked at 7e-5): a short top-up of a trained adapter, the owner's setting.
- **Warm-up: the trainer's fixed 5% linear warm-up, 125 steps, then cosine to 0.** It is not a free key (the
  trainer computes `int(0.05 * n_steps)`), and it is the right shape here: a fresh AdamW has no second-moment estimate
  yet, so its first updates are as large as lr allows; ramping lr from 0 over the first 125 steps keeps those
  first steps from pushing C1's adapter around before the moments settle. The consistency losses ramp to full weight
  by 20% of the run (step 503), as in every run of this trainer.
- `epochs` 0.9452666196852243: exactly one pass, 2,515 steps (`replay_steps.py --config runs/q35_4b_fix2.json`:
  `config_is_one_pass` true).
- `seed` 20261002: a new data order for new data.
- `snap_every` 0, `snap_fracs` []: no snapshots, so no dev-selected weights; C4 is the last step's adapter.
- `expect_kd_targets` 1,369 / `expect_kd_full` 16: the builder's counts for this file (the trainer refuses to
  start on any other count).
- `log_every` 25 (shorter run).

## q35_4b_c_r1.json: DRAFT. C round 1 (C_TRAIN_RECIPE.md v4, config sketch in section 3)
Every value is the recipe's, except the ones the build fills. They are written `FILL_...`, and
`modal_od._launch_checks` refuses the config until they are filled:
- `epochs`: 16 / the measured rows per step from the `batches()` dry run (pre-flight 7).
- `expect_ord_rows`: the mixer's ordinal row count. The trainer requires it to equal the ordinal rows in the file
  exactly, and the planned draw to cover them within 1%.
- `expect_kd_targets` / `expect_kd_full`: the mixer's counts.
- `seed`: a new seed.

`init_adapter` is C1's adapter on the account's Volume (`models/q35_4b_main500k_init`, as for fix1 and fix2).
`train_file` / `rel_file` sit in `data/c_parts/`. They are in `modal_od.C_KEEP`, so the default image uploads them
(`tests/test_pilot_tools.py::test_data_ignore_uploads_run_files_and_skips_label_shards` checks this).

## Configs the default image cannot launch
- `q35_4b_fix1.json`, `q35_4b_fix2.json`: finished top-ups. Each was launched by its own spawn script
  (`extra/fix1_spawn.py`, `extra/fix2_spawn.py`), which uploads only that run's two files (`modal_od.SPAWN_LAUNCHED`).
- `q35_2b_main.json`: the 2B is paused. Its train file `v14_parts/train_2b_golden_kd_2view.jsonl` (1.4 GB) is not in
  `V14_KEEP`, so 4B launches do not upload it. `relay` refuses this config until the file is added to `V14_KEEP`
  when the 2B resumes.
