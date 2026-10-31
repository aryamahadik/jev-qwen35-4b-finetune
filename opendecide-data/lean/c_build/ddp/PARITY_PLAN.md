# DDP parity plan: adoption test 2 (PREREG_FINAL A20 c)

Written on 6 Oct 2026, before any GPU run. Nothing here has been launched.

## What A20 (c) asks

- Round 1 may train on several H100s only if two adoption tests pass. Otherwise it trains on 1 x H100, as planned.
- **Test 1 (CPU, done):** 1 vs 2 gloo ranks on a tiny model; gradients equal within 1e-5 relative (fp32).
  - Result: `c_build/ddp/ADOPTION_CPU.json` (section at the end).
- **Test 2 (this plan):** 50 steps on rows from C1's old training data, 1 x H100 vs 4 x H100.
  - The per-step loss must match within bf16 noise. It may cost at most $4.

## Where the code lives (the pinned files are untouched)

- `train_decoder.py` (sha256 `c2c2d1d623cc...`, pinned by fmt1 loader_check) and `modal_od.py` are **not modified**.
- `c_build/ddp/train_ddp.py` imports the pinned `train_decoder` and builds the DDP loop **from its source**:
  `inspect.getsource(train_decoder.train)` plus 20 DDP hunks (exact replacements; each anchor must occur exactly once),
  compiled with the pinned module's globals.
  - So `check_rows`, the row, loader and render functions, `compute_loss` and every other helper are the pinned ones,
    called, not copied. Every line of `train()` outside the hunks is the pinned line.
  - It refuses to build if `train_decoder.py` is not the pinned sha.
  - `python c_build/ddp/train_ddp.py show` prints the hunks as a diff against the pinned `train()`.
- `c_build/ddp/modal_ddp.py` is a separate Modal app (`opendecide-ddp`). It reuses modal_od's image35, Volume,
  secrets, launch checks and target regex, and adds `train_ddp.py` to the image.

## What a DDP run does

- Every rank draws the **same global batch of 16** (same seed, same Python RNG streams), with the same option
  permutations and permutation twins.
  - After the model set-up every rank takes rank 0's Python RNG state. The pilot (P2) saw the model load draw from
    Python's `random`, so this keeps every rank on rank 0's stream, which is a one-GPU run's stream.
  - Every step, an all-reduce of a hash of (batch, permutations, twins) stops the run before any update if ranks differ.
- The batch's **whole units** are dealt to the ranks (heaviest first, to the least-loaded rank), so relation terms never
  cross ranks. Each rank packs its share with the pinned `_micro_groups` under the same `micro_tokens`.
- Every loss term is divided by the **whole-batch** counts (rows, cons, comp, equiv, inv, twins, anchors, ordinal
  rows). This is `aux_norm` "batch", which DDP requires.
  - Each rank computes these counts from the full batch, which it holds. So the rank losses add up to the one-GPU
    batch loss.
- Gradients are **summed** over the ranks (one flat all-reduce), then clipped at 1.0 as on one GPU.
  - Every rank then takes the same AdamW step. Steps, warm-up and the cosine LR schedule are unchanged.
  - Logged terms and counts are summed the same way.
- Rank 0 alone logs, snapshots, checkpoints and saves the model. The launcher process runs `vol.commit`.
  - The checkpoint adds every rank's RNG state, after a check that all ranks hold identical weights.
- **Resume:** works on the same GPU count. With `allow_env_change` it also works across 1, 2, 4 and 8 GPUs
  (the env records `world_size`).
- Each rank > 0 has its own LoRA-dropout stream, so ranks never share masks.
  - This is the only intended difference from one GPU, and it is pure noise.
- The default one-GPU path is `train_decoder.train` itself, unchanged.

## Arms (one fixed sample of C1's training rows; three containers at once)

| Arm | Hardware | Path | `micro_tokens` | Role |
|---|---|---|---|---|
| A | 1 x H100 (own container) | unchanged `train_decoder.train` | 8192 | reference |
| B | 1 x H100 (own container) | unchanged `train_decoder.train` | 6144 | **noise control**: the same objective under `aux_norm` "batch", other packing, so other bf16 shapes and dropout masks |
| C | 4 x H100 (one container) | `train_ddp.launch_ddp`, 4 NCCL ranks | 8192 | candidate |

- **Data:** C1's files (`runs/q35_4b_main.json`: `data/v14_parts/golden_train.jsonl` + `golden_relations.jsonl`).
  - The laptop keeps every row whose `call_id` sha1 falls in 1 of 300 buckets (whole units: 1,804 rows), plus
    the 258 relations among them. It writes them to `c_build/ddp/parity_data/` (sha256 `62b9bd0c...`, `c97e6ebb...`).
  - Every container receives these exact bytes. Their sha256 goes into the result.
- **Config:** round 1's frozen draft `runs/q35_4b_c_r1.json` with its FILL keys removed (`epochs` 1.0, `seed`
  20261006). Every loss setting is unchanged: kd 0.5, kd_skip_src, kd_full_src, lam 1.0, lam_inv 1.0, sym_cons,
  perm_twin 0.3, lam_p 0.5, lam_ord 1.0, beta 0, aux_norm batch, lr 5e-5, r 16, alpha 32, dropout 0.05, QWEN35 targets,
  grad_ckpt, expect_trainable 32,464,896.
  - `init_adapter` is C1's adapter (`/vol/models/q35_4b_main500k_init`) when the account's Volume has it.
    Otherwise every arm starts from a fresh LoRA. The result records which.
  - `stop_at_step` 50, `log_every` 1, `resume` false, no periodic checkpoints and no snapshots.
  - Each arm ends with its stop checkpoint in `/vol/models/pilot_ddp_parity_<arm>/` (pilot names only).
- `n_steps` is 113 on the sample, so warm-up ends at step 5. Steps 5-49 run near peak LR, which exercises the
  optimizer, not only the forward pass.
- **Why A and B have their own containers:** the first import of the transformers model module draws from Python's
  `random` inside `train()`. A second run in the same process would draw other batches (adoption test 1 found this).
  Each arm is therefore a fresh process, as a relay segment is. Every arm imports `torch.distributed` before the seed,
  as a DDP rank does.

## The exact command (do not run without the owner's GO: it is a paid GPU step)

```bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean && \
  ../.venv/bin/modal run c_build/ddp/modal_ddp.py::ddp_parity --config runs/q35_4b_c_r1.json \
    --c1-config runs/q35_4b_main.json --steps 50 --keep-1-in 300 --seed 20261006 --gpus 4
```

- Prefix it with `MODAL_PROFILE=<account>` to use the account whose Volume holds `models/q35_4b_main500k_init`.
  - On another account the arms start from a fresh LoRA. That is still a valid parity test, and the result says which.
- The entrypoint refuses to start if the function timeouts allow more than $4 (`--cap-usd`, default 4.0).
- It starts arm A, arm B and arm C at the same time. After they finish, a CPU container reads the three step-50
  checkpoints (weights, last batch, Python RNG state).
- It writes `c_build/ddp/PARITY_RESULT.json`: the verdict, every per-step log, s/step per arm, the round-1 projection
  and the spend.
- Log the spend in `logs/budget_ledger.md` afterwards.
- **8 x H100 (optional, A21 b):** after a passing 4 x run, `--gpus 8 --reuse-x1` runs only arm C8 (timeout 7 min, at
  most $3.82) and compares it with A and B from `PARITY_RESULT.json` (same sample and config are checked).
  It writes `PARITY_RESULT_x8.json`. It is a separate paid step.

## Pass rule (fixed now, before the run)

For each arm X and each logged step s (0-49), d_X(s) = |X(s) - A(s)| / |A(s)|. B measures bf16 + dropout noise at
the same objective. C passes only if **all** of these hold:

1. **Same data, same order:**
   - All arms got the same sample bytes and the same init (C1 or fresh).
   - The step-50 checkpoints of A, B and C hold the same last-batch hash and the same Python RNG state.
   - At every step, lr, n_cons, n_inv, n_twin, n_ord and n_rel_skipped are identical in A, B and C.
   - The trainer also refuses to step if any rank drew a different batch (the per-step hash check).
   - If the data stream differs, the verdict is **INCONCLUSIVE**, not FAIL: find the cause, then rerun once.
2. **Loss within noise:** for loss, task, cons, inv, perm, ord, kl (when present) and the gradient norm gn:
   - mean_s d_C <= 1.5 x mean_s d_B + 0.001;
   - max_s d_C <= 1.5 x max_s d_B + 0.002.
3. **No gross step:** d_C(loss) <= 5% at every step.
   - A normalisation bug, such as dividing by per-rank counts, would show at step 0 as a 2-4x error.
4. **Weights after 50 steps:** ||W_C - W_A|| / ||W_A|| <= 1.5 x ||W_B - W_A|| / ||W_A|| + 1e-4.

**If it fails:** round 1 trains on 1 x H100 as planned (A20). The failing metric is kept in the result file.
There is no second attempt without a written cause.

## Cost of this test (limit $4)

| Container | Wall time (estimate) | Rate | Cost |
|---|---|---|---|
| A, 1 x H100 | about 5 min (start, model load, 50 x ~2.8 s, stop checkpoint) | $4.09/h | about $0.35 |
| B, 1 x H100 | about 5 min | $4.09/h | about $0.35 |
| C, 4 x H100 | about 5-6 min (4 model loads, NCCL start, 50 x ~1 s) | 4 x $4.09/h | about $1.4-1.6 |
| State check, CPU | about 1 min | CPU | under $0.01 |
| **Total** | | | **about $2.1-2.3 (expected)** |

- **Hard cap from the function timeouts:** A and B 12 min each ($0.82 each), C 8 min ($2.18): at most **$3.82**.
  The entrypoint checks this before it starts anything.
- No 1.2 GB read in the containers: the laptop builds the sample and sends its bytes.

## Expected speed-up and cost per round-1 run (estimates; the parity run measures the real s/step)

- **Basis:**
  - Round 1 is about 8,880 steps. C1 measured 2.72-2.77 s/step on 1 x H100 at `micro_tokens` 8192 (recipe 4;
    pilot P2).
  - A step holds about 17 rows plus about 2.5 permutation twins, in about 3-4 micro-batches.
- **Per rank:**
  - 4 ranks get about 5 sequences each, usually one micro-batch.
  - The step waits for the slowest rank. With whole-unit dealing, that rank carries about 15-30% more tokens than the
    mean.
  - Smaller forwards also lose some GPU efficiency.
  - The gradient all-reduce (32.5M fp32 = 130 MB over NVLink) adds about 1-2 ms. The per-step hash and term sums are
    a few bytes.

| GPUs | s/step | Speed-up | Round-1 wall time | Steps cost | + overhead (about 10 min wall) | Round-1 total |
|---|---|---|---|---|---|---|
| 1 x H100 (plan) | 2.72 (measured, C1) | 1.0x | 6.7 h | $27.4 | $2 (recipe allowance) | **about $29.5** |
| 2 x H100 | about 1.45-1.6 | about 1.7-1.9x | about 3.6-3.9 h | about $29-32 | about $1.4 | **about $31-34** |
| 4 x H100 | about 0.85-1.05 | about 2.6-3.2x | about 2.1-2.6 h | about $34-42 | about $2.7 | **about $37-45** |
| 8 x H100 | about 0.5-0.65 | about 4.2-5.4x | about 1.2-1.6 h | about $40-52 | about $5.5 | **about $46-58** |

- **Speed costs money.** More GPUs finish sooner, but each GPU idles part of every step: it waits for the slowest
  rank, and the others wait while rank 0 snapshots or checkpoints.
- **Budget:** `C_TRAIN_RECIPE.md` 4 stops the run at a projected round-1 total above $35, and A21 pre-authorises
  about $30 of round-1 training.
  - 4 x and 8 x are likely above both, so they need the owner's OK on the extra $8-28.
  - 2 x likely fits under the $35 stop (`train_relay35_x2` exists for that; it would need its own parity check).
- The parity run's `projection_round1` (A vs C s/step on C1 rows) replaces this table with measured numbers for 4 x.
  Round 1's prompts are longer than C1's (recipe sensitivity +12%), which scales every row alike.
- **Launch after both tests pass:**
  - `modal run --detach c_build/ddp/modal_ddp.py::relay_ddp --config runs/q35_4b_c_r1.json --gpus 4`
    (or `--gpus 8`).
  - Same frozen config, folder, fingerprint and checkpoints as `modal_od.py::relay`.
  - A segment that changes GPU count adds `--allow-env-change`.

## Files

| File | What it holds |
|---|---|
| `c_build/ddp/train_ddp.py` | `Dist`, `rank_split`, `rank_groups`, `same_draws`, `sum_grads`, `sum_step`, `ckpt_extra`, `restore_rng`, `ckpt_decision`; `HUNKS` + `patched_source` / `train` (the built loop); `launch_ddp`; CLI `show`, `train` (torchrun), `launch` |
| `c_build/ddp/modal_ddp.py` | App `opendecide-ddp`: `train_relay35_x2` / `_x4` / `_x8` + `relay_ddp`; `ddp_parity_x1` / `_x4` / `_x8`, `ddp_parity_state` + `ddp_parity` |
| `tests/test_ddp.py` | Pinned trainer untouched and hunks apply; rank-split invariants; DDP refuses `aux_norm` "micro"; 1 gloo rank is bit-identical to 1 process and 2 gloo ranks match it (fake model) |
| `c_build/ddp/adoption_cpu.py` -> `ADOPTION_CPU.json` | Adoption test 1 |
| `c_build/ddp/wip/` | The earlier in-place attempt (diffs against the pinned files), kept for the record; not used |

## Adoption test 1 result (CPU, 6 Oct 2026): PASS

- **Code tested:** pinned `train_decoder.py` `c2c2d1d623cc...` (unchanged) + `c_build/ddp/train_ddp.py`
  `93ea4eb24381...` (20 hunks). Any later change to `train_ddp.py` needs a re-run of test 1.
- **Setup:**
  - A tiny Qwen3-like model: 2 layers, fp32, the real Qwen3 tokenizer and the real prompt path (cygnet,
    schema_branch_mark).
  - Round-1 loss settings: kd, kd_full, sym_cons, perm_twin, lam_inv, lam_ord, anchor, aux_norm batch.
  - 3 steps of 16-18 rows. The 1-process run uses 8-9 micro-batches per step; each of the 2 ranks uses 4-5.
- **2 gloo ranks vs 1 process (bar: 1e-5 relative):**
  - Per-step loss relative difference: at most 2.2e-8.
  - Gradient (summed, before clipping): relative L2 at most 8.3e-7, largest element at most 1.2e-6.
  - Weights after 3 steps: 5.0e-7.
  - Both ranks hold the bit-identical summed gradient.
  - Every step's rows are split into whole units, disjoint and complete.
- **Default path:** `train_decoder.train` run after building the DDP loop is bit-identical to the git HEAD copy of
  the trainer (logs, losses, gradients, weights).
- **Resume:** a 2-rank run stopped at step 2 and resumed is bit-identical to a straight 2-rank run.
- **World size 1:** a 1-rank DDP run is bit-identical to the one-process run.
- `tests/test_ddp.py` (fake model, 9 tests) passes, including 1 rank bit-identical and 2 ranks within 1e-5.
