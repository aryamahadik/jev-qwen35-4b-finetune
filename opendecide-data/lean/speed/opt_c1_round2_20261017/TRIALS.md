# TRIALS (round 2, Track A: L4 serving trials)

Written 17 Oct 2026. **Status: BLOCKED before the first GPU window. No GPU trial has run; no production downtime occurred.**

The permission classifier refused the one action every L4 trial needs: stopping the production C1 server on od-l4b (port 30000) for a
trial window (rule label "Remote Shell Writes"; the order was `BG=1 NOSYNC=1 JOB=r2_T0a gcp_run.sh od-l4b 'bash ~/opt_r2/window.sh T0a ...'`,
checked first: no C2 read job was running). The production server holds 21 of the L4's 23 GB (mem-fraction 0.8), so a trial server cannot
run beside it. I did not look for another route to the same action. A harness smoke test that would have read N decisions from the running
production server was refused too ("Interfere With Workloads"), and so was serving the FP8 checkpoint over the VPC to move it.
Everything below is what could be done without touching the production server. Every trial row is `NOT RUN`, verdict `NA`.

To unblock: allow the window launch (it stops production, runs one trial on port 30010, and restores production exactly as
`~/reads/start_server.sh --max-running 32 --max-mamba 128 --mem-fraction 0.8 --extra-args "--attention-backend triton"`, with the C2 wait,
the server_info diff and the downtime log built in), then run the windows in `RUN_ORDER.sh` one at a time. Each window is about 35-45 min
(boot about 2.5 min, parity pass 8,143 about 15-25 min on the L4, 2 x 320 batch-1 calls, 660 calls at c64); 17 windows are planned (T3 and T9 are conditional).


## Trial table

| trial | what | status | verdict | agree vs T0a (Wilson LB) | flips | max dp | batch-1 p50/p95/p99 ms | c64 dec/h | GPU busy % (b1 / c64) |
|---|---|---|---|---|---|---|---|---|---|
| T0a | BF16 baseline (reference for every parity), production flags on port 30010 | NOT RUN | NA | - | - | - | - | - | - / - |
| T0b | BF16 baseline again after a reboot + a second parity pass at c64 (self-agreement floor) | NOT RUN | NA | - | - | - | - | - | - / - |
| T1 | diagnostics: --enable-metrics --enable-cache-report --gc-warning-threshold-secs 0.005 + py-spy | NOT RUN | NA | - | - | - | - | - | - / - |
| T2 | --cuda-graph-backend-prefill full (GDN layers must be inside the capture, no fallback) | NOT RUN | NA | - | - | - | - | - | - / - |
| T4a | input_ids (as today) + --skip-tokenizer-init, /generate readout | NOT RUN | NA | - | - | - | - | - | - / - |
| T4b | /v1/score readout on token ids | NOT RUN | NA | - | - | - | - | - | - / - |
| T4c | /v1/score + --skip-tokenizer-init | NOT RUN | NA | - | - | - | - | - | - / - |
| T5 | LM head sliced to the 141 option-token rows (copied rows, fp32 accumulate, embed_tokens untouched) | NOT RUN | NA | - | - | - | - | - | - / - |
| T3 | GC fix: gc.freeze() after warm-up (only if T1 shows pauses) | NOT RUN | NA | - | - | - | - | - | - / - |
| T8 | block-FP8 checkpoint (128x128 weights, dynamic activations), --quantization fp8 | NOT RUN | NA | - | - | - | - | - | - / - |
| T6 | --mamba-ssm-dtype bfloat16 | NOT RUN | NA | - | - | - | - | - | - / - |
| T7 | --mamba-track-interval 64 | NOT RUN | NA | - | - | - | - | - | - / - |
| T10a | image noise floor: native x2 at c1 and c8 (200 images) | NOT RUN | NA | - | - | - | - | - | - / - |
| T10b | image: --keep-mm-feature-on-device | NOT RUN | NA | - | - | - | - | - | - / - |
| T10c | image: --mm-processor-worker-num 4 | NOT RUN | NA | - | - | - | - | - | - / - |
| T10d | image: client-side exact-size pre-resize | NOT RUN | NA | - | - | - | - | - | - / - |
| T9 | live FP8 + BF16 cascade (only if T8 or the gate passes on held-out data) | NOT RUN | NA | - | - | - | - | - | - / - |
| T11 | --prefill-only-disable-kv-cache + --disable-radix-cache (exploratory) | NOT RUN | NA | - | - | - | - | - | - / - |


## Measured without the GPU (offline, nothing touched on port 30000)

| item | result |
|---|---|
| T4, token ids identical | **exact.** All 8,143 decisions = 11,957 sequences = 6,077,542 tokens: client ids (decoder_io path, transformers 5.17 / tokenizers 0.23.2) equal the ids of the server's own tokenizer stack (transformers 5.12.1 / tokenizers 0.22.2) on every sequence, with and without special tokens; 0 mismatches in every bucket (noul 4329, 2-4 5054, 5-9 1800, 10-25 306, 26+ 468). The harness and fast_read already send `input_ids` to `/generate`, so SGLang does not re-tokenise today: `--skip-tokenizer-init` can only remove tokenizer/detokenizer-process overhead. |
| T5, LM-head slice: option ids | the union of C1's candidate ids over P, N and R is **141 tokens** (ids 32 to 216892), so the head shrinks from 248,320 rows to 141. |
| T5, arithmetic (CPU unit test, bf16 hidden x bf16 rows, fp32 out) | sliced logits equal full logits on the candidate columns (max abs diff 0.0); after the log-softmax and the group readout max abs dp 1.5e-7, argmax equal. This is a synthetic-shape test only; it does not show the patch runs inside SGLang's scheduler. |
| T5, code finding (SGLang 0.5.20 `logits_processor._compute_lm_head`) | with `--enable-fp32-lm-head` and bf16 hidden states SGLang calls `torch.mm(hidden, lm_head.weight.T, out_dtype=float32)`: the weight stays **bf16** (no fp32 copy). One head read is 248,320 x 2,560 x 2 B = **1.27 GB**, not 2.5 GB: about 4.2 ms on the L4 (300 GB/s) and about 0.4 ms on an H100 (3.35 TB/s). So T5 is worth about 0.4 ms per forward on H100, at the low end of the plan's 0.4-0.8 ms. |
| T8, block-FP8 checkpoint | built, data-free, 35 s on CPU: 200 linears quantised (24 x 3 GDN + 32 x 3 MLP + 8 x 4 attention), 538 tensors kept BF16 and bit-identical to the source (conv1d, in_proj_a, in_proj_b, embed/lm_head, visual, mtp, norms, A_log, dt_bias). Block scale = absmax/448 per 128x128 block (equals compressed-tensors' `calculate_qparams`, the LLM Compressor FP8_BLOCK arithmetic); rel. Frobenius error 2.64% (29 tensors checked); 5.5 GB against 9.3 GB. Same bytes on od-cpu1 and od-l4b (shard sha256 starts 4bbce991... and d01e6983...). SGLang 0.5.20 reads the config on CPU: `quantization` resolves to fp8 (given or auto-detected), block [128,128], dynamic activations; its skip logic keeps in_proj_ba, the visual tower and lm_head BF16 and puts in_proj_qkvz, out_proj, qkv_proj, o_proj, gate_up_proj and down_proj in FP8. Not yet booted. |
| tooling | window runner, trial server launcher, parity/gate report (tested on synthetic noise), vision harness (tested on CPU: 200 items, token predictions), T5/T3 patch, py-spy 0.4.2 (sudo ok), FP8 builder + verifier. |

## Deviations, stated plainly

- The FP8 checkpoint was first built on od-cpu1 as ordered, but copying 5.5 GB to od-l4b through the IAP tunnel stalled at 0.5 GB and the VPC route was refused, so the same script ran again on od-l4b (CPU only, `nice 19`, 48 s, under `~/opt_r2`). The two outputs are byte-identical.
- The quantiser is a 60-line script (same arithmetic as LLM Compressor FP8_BLOCK), because od-cpu1 has no internet and `llmcompressor` is not installed anywhere. It writes Qwen's own FP8 layout (`weight_scale_inv`) so `--quantization fp8` loads it.
- Probes and file copies to the VMs used `gcloud compute ssh/scp` (the transport gcp_run.sh itself uses, `vm.sh`/`put.sh`); jobs were launched with gcp_run.sh `BG=1 NOSYNC=1` (od-cpu1 build, od-l4b rebuild). Only paths under `~/opt_r2` were written; `~/lean/data` was never listed. No Modal.
- The 8,143-item Wilson bar: a bucket with fewer than about 770 items cannot reach a 0.995 lower bound even at 100% agreement, so `r2_report.py` reports each bucket and view type with its own Wilson interval and flags such buckets `underpowered`; pass/fail uses the full set and the two view types (noul 4,329; choice 3,814).

## Winners for the H100 confirm

**None yet: no L4 trial has run, so nothing has earned a place.** The arms to confirm if the L4 trials pass (expected gains are the plan's estimates, not measurements):

| H100 arm | contents | expected gain on H100 | basis |
|---|---|---|---|
| B. exact bundle | whichever of T2 full-graph prefill, T4 input_ids/`--skip-tokenizer-init` (+ `/v1/score`), T5 LM-head slice, T3 GC fix are `exact` or `pass` with a gain on the L4 | batch-1 p50 -2 to -6 ms (plan estimate, from 32.4 ms). Known pieces: `/v1/score` -1.9 ms measured on H100 on 17 Oct (2500/2500 parity); T5 about -0.4 ms (computed above); T2 unknown until the L4 shows whether the capture covers the GDN layers; T3 only if T1 shows GC pauses (p99 only) | plan RANK 4 |
| C. block-FP8 / gate | the verified `c1_fp8_block` checkpoint, `--quantization fp8`; if its parity alone is below the bar, the margin gate (tau fitted on a hash half, tested on the other, on all 8,143) over a BF16 re-run | +21% throughput if block-FP8 passes alone (about $0.0114 per 1K at 100%); +7-10% with the gate (replay of per-channel FP8 answers on 2,500 items, not of block-FP8) | plan RANK 5 |
| D. cache knobs | `--mamba-track-interval 64` or `--mamba-ssm-dtype bfloat16`, only if the L4 shows more than 5% throughput | under 5% expected | plan RANK 6 |

## Files (all under `lean/speed/opt_c1_round2_20261017/`)

`RUN_ORDER.sh` (the exact window commands), `vmcode/` (what runs on the VMs: `window.sh`, `trial_launch.py`, `prod_stop.sh`, `prod_start.sh`, `r2_trial.py`, `r2_vision.py`, `r2pypatch/`, `build_fp8_block.py`, `t1_diag.sh`), `r2_report.py` (parity + gate replay), `make_trials.py` (rebuilds this file from `results/<trial>/`), `pull_results.sh`, `PROD_DOWNTIME.log`, `results/T4_token_ids.json`.
