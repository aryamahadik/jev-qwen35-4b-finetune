# TRIALS_H100 (round 2, one H100 window)

Generated 2026-10-17T17:01:33Z from `/Users/aryamahadik/Documents/jev/opendecide-data/lean/speed/opt_c1_round2_20261017/h100/results/session_20261017_161152/volume/session_20261017_161152`. Rate used for $/1K: **USD 4.3952/h** (H100 3.95 + 4 cores x 0.0473 + 32 GiB x 0.008, region 'any' x1.0). Bar: Wilson95 lower bound >= 0.995 on the full 8,143 parity set vs the same-session S1 BF16 pass (c32).

Session: GPU NVIDIA H100 80GB HBM3, 81559 MiB, 610.57.04, region us-central, wall 2060.4 s, in-container spend estimate USD 2.618.

Decisions taken during the window:
- r2_b: full-graph prefill not usable as asked (booted=False, resolved=None, aborted=None, step errors={}, agree=None, error='RuntimeError: SGLang exited (-9) during boot; last lines:\n  File "/sgl-workspace/sglang/python/sglang/srt/managers/tp_worker.py", line 443, in init_cuda_graphs\n    self.model_runner.init_cuda_graphs(\n  File "/sgl-workspace/sglang/python/sgl'); next: r2_b_nofull

## Findings in one page

- **A (S1 BF16 reference, this session):** batch-1 N p50/p95/p99 29.86/38.09/82.12 ms (640 calls); N c64 325,826 dec/h, P c64 364,985.00 dec/h; GPU busy 43.8% at batch 1 and 82.5% at c64; USD/1K at 100/50/20% utilisation {'100%': 0.01349, '50%': 0.02698, '20%': 0.06745}. BF16 self-agreement floor (A c32 vs A c64): 2 flips of 8,143.
- **B (exact bundle):** `--cuda-graph-backend-prefill full` does NOT work for this GDN hybrid on SGLang 0.5.20: the server dies while capturing the prefill graph (`IndexError: list index out of range` in hybrid_linear_attn_backend._replay_metadata), so it is dropped from the bundle. The rest of the bundle (skip-tokenizer-init + input_ids, /v1/score, metrics, gc warnings) is **exact** (1 flip, Wilson LB 0.999305) but gives no gain: batch-1 p50 29.54 vs 29.86 ms, p99 81.08 vs 82.12 ms, N c64 326,024 dec/h (same).
- **LM-head slice:** the opt-in patch was installed in 3 SGLang processes but never took the slice path (patch report has no `rows_copied` / counters), so the 141-row head was NOT exercised on the GPU; the arithmetic is CPU-tested and the cost it could remove is about 0.4 ms (1.27 GB head read at 3.35 TB/s). Not measured, not adopted.
- **GC:** SGLang already freezes the GC after its warm-up (`/freeze_gc` called once, seen in the metrics); the only long GC in the log is one 0.36 s generation-2 pass at warm-up, none in the measured loops. gc.freeze() after warm-up changed nothing: p50 29.78, p99 81.05 ms. The p99 tail (~82.12 ms) is not GC.
- **C (block-FP8):** FAIL alone: 8011/8,143 agree (0.98379, Wilson LB 0.98081, 132 flips, max |dp| 0.546921). Throughput is +27.8% (N c64 416,410 dec/h) and p99 65.47 ms, but p50 is unchanged (29.81 ms). With the margin gate the bar is met only at a large deferral share; see the ladder below (tau 0.20: 10.6% deferred, 10 flips, both halves above the bar, +11.2% cascade throughput, batch-1 p99 ~108 ms). The split-half test as specified is not stable (tau fitted on half 0 fails on half 1 with LB 0.9948), so the gate is NOT confirmed.
- **D (images):** native-vs-native noise floor on the 200-image pack is 1 flip in 200 at c1 (dp up to 0.0045) and 0 at c8 (dp up to 0.0128). `--keep-mm-feature-on-device` (pass): steady-state c1 p50 19.45 ms lower, c8 throughput +66.2%, agreement with A's native within the floor (1 flip). D1 and D2 give bit-identical probabilities to each other on the 200 images (both fresh boots), so the flags do not change the numerics; the 1-flip / dp <= 0.016 difference to arm A's server is a server-state effect of the size of the noise floor (A's pass ran after 5 min of text load). `--mm-processor-worker-num 4` (pass): no gain (c1 p50 1.2 ms, c8 throughput -15.1%). Client-side exact-size pre-resize is NOT bit-identical (4-5 flips in 200, dp up to 0.18) and costs ~23 ms of client time: rejected.
- **E (cache knobs):** `--mamba-ssm-dtype bfloat16` pass (3 flips), p50 28.77 ms (-1.09), throughput +1.7%: below the adopt threshold. `--mamba-track-interval 64` pass (1 flip), no gain. Cached share unchanged (R: 0.5271).
- **Adoptable set (bar met AND a real gain):** ['r2_d1']. Exact/pass but with no gain (safe, optional): the bundle without `full` and the cache knobs. Money: ledger USD 2.5705 of the USD 5.00 cap; billing report for the app USD 2.5248.

## One row per arm

| arm | config | verdict | agree (Wilson LB) | flips | max dp | b1 p50/p95/p99 ms | d p50/p99 vs A | N c64 dec/h | P c64 dec/h | GPU busy b1 / c64 % | USD/1K @100/50/20% (N c64) | adopt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | `r2_a` | **reference** | 1.00000 (0.99953) | 0 | 0.0000 | 29.86/38.09/82.12 | -/- | 325,826 | 364,985.00 | 43.80 / 82.50 | 0.0135 / 0.0270 / 0.0674 | no |
| B | `r2_b` | **NA** | - (-) | - | - | -/-/- | -/- | - | - | - / - | - / - / - | no |
| B (variant) | `r2_b_dcpc` | **NA** | - (-) | - | - | -/-/- | -/- | - | - | - / - | - / - / - | no |
| B' | `r2_b_nofull` | **exact** | 0.99988 (0.99930) | 1 | 0.0306 | 29.54/38.20/81.08 | -0.32/-1.04 | 326,024 | 361,681.00 | 46.50 / 84.90 | 0.0135 / 0.0270 / 0.0674 | no |
| B+gc | `r2_b_gc` | **exact (by construction; parity pass not re-run)** | - (-) | - | - | 29.78/38.17/81.05 | -0.08/-1.07 | 327,698 | 363,283.00 | 44.90 / 86.40 | 0.0134 / 0.0268 / 0.0671 | no |
| C | `r2_c` | **fail** | 0.98379 (0.98081) | 132 | 0.5469 | 29.81/33.39/65.47 | -0.05/-16.65 | 416,410 | 460,453.00 | 40.90 / 85.60 | 0.0106 / 0.0211 / 0.0528 | no |
| D1 | `r2_d1` | **pass** | - (-) | - | - | -/-/- | -/- | - | - | - / - | - / - / - | yes |
| D2 | `r2_d2` | **pass** | - (-) | - | - | -/-/- | -/- | - | - | - / - | - / - / - | no |
| E1 | `r2_e1` | **pass** | 0.99963 (0.99892) | 3 | 0.0316 | 28.77/37.75/82.06 | -1.09/-0.06 | 331,396 | 366,586.00 | 44.90 / 86.00 | 0.0133 / 0.0265 / 0.0663 | no |
| E2 | `r2_e2` | **pass** | 0.99988 (0.99930) | 1 | 0.0320 | 30.26/38.59/83.08 | 0.40/0.96 | 328,592 | 361,976.00 | 48.90 / 89.20 | 0.0134 / 0.0267 / 0.0669 | no |

NA rows: the arm did not run (see the notes per arm below). `exact` = numerics-preserving by construction, bar met, 0 flips.

### A. S1 BF16 reference  (`r2_a`: reference)

- prefill graph backend resolved by SGLang: `breakable`
- parity vs A (same session, c32): 8143/8143 = 1.0 (Wilson95 [0.999528, 1.0]), flips 0, max |dp| 0.0, mean dp 0.0, flip ref-margin median None max None, flips with ref margin <= 0.005/0.01/0.02/0.05/0.1: {'0.005': 0, '0.01': 0, '0.02': 0, '0.05': 0, '0.1': 0}
- per bucket: 10-25: 153/153 LB 0.975506 (underpowered); 2-4: 2527/2527 LB 0.998482; 26+: 234/234 LB 0.983848 (underpowered); 5-9: 900/900 LB 0.99575; noul: 4329/4329 LB 0.999113
- per view type: choice: 3814/3814 LB 0.998994; noul: 4329/4329 LB 0.999113
- BF16 self-agreement floor (A c32 vs A c64 on the same server): 8141/8143 = 0.999754 (Wilson95 [0.999105, 0.999933]), max |dp| 0.030554
- A vs SPEED-2's stored S1 answers (13 Oct): {'n': 8143, 'argmax_agree': 0.999877, 'n_flips': 1, 'agree_wilson95': [0.999305, 0.999978], 'dp_max': 0.039805}
- batch-1 N, 2 x 320 calls: rep1 {'n': 320, 'p50': 29.85, 'p95': 38.07, 'p99': 82.12, 'mean': 31.79, 'max': 87.81, 'noul_p50': 29.28, 'choice_p50': 30.98}; rep2 {'n': 320, 'p50': 29.89, 'p95': 38.09, 'p99': 82.06, 'mean': 31.74, 'max': 83.17, 'noul_p50': 29.23, 'choice_p50': 30.92}; pooled {'n': 640, 'p50': 29.86, 'p95': 38.09, 'p99': 82.12, 'mean': 31.76, 'max': 87.81}; rep p50 spread 0.04 ms
- throughput: {"N_c64_dph": 325826, "N_c64_dph_runs": [325974.0, 325677.0], "N_c64_gpu_busy_pct": 82.5, "N_c64_cached_share": 0.1691, "P_sat_c64_dph": 364985.0, "P_sat_c64_gpu_busy_pct": 87.1, "parity_pass_c32_dph": 343661.0, "parity_pass_cached_share": 0.2077, "parity_pass_gpu_busy_pct": 85.7, "P_full_c64_dph": 357043.0, "P_full_c64_gpu_busy_pct": 87.6, "batch1_gpu_busy_pct": 43.8}
- USD/1K (N c64): {'100%': 0.01349, '50%': 0.02698, '20%': 0.06745}; (P c64): {'100%': 0.01204, '50%': 0.02408, '20%': 0.06021}
- R prefix-repeat set cached share: {'cached_token_share': 0.5271, 'rows': 800}
- log scan: gc: 0; graph: 0; fallback: 0; error: 0; fp8: 0
- images (200 items, ms per decision = both views for choice items):
    - native:1#1: acc 85.5, p50 107.734 p95 161.248 p99 199.417, items/s 9.673, token mismatches 0, errors 0
    - native:1#2: acc 85.5, p50 94.573 p95 161.919 p99 196.194, items/s 11.185, token mismatches 0, errors 0
    - native:8#1: acc 85.5, p50 265.991 p95 410.699 p99 487.75, items/s 31.859, token mismatches 0, errors 0
    - native:8#2: acc 85.5, p50 249.023 p95 424.401 p99 476.288, items/s 32.099, token mismatches 0, errors 0
    - exact:1#1: acc 85.5, p50 122.378 p95 189.992 p99 221.235, items/s 6.676, token mismatches 0, errors 0
    - exact:8#1: acc 86.0, p50 238.103 p95 461.956 p99 515.21, items/s 26.522, token mismatches 0, errors 0
    - noise_floor_native_c1_run1_vs_run2: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.004465, 'dp_mean': 0.000702, 'identical_probs': False}
    - noise_floor_native_c8_run1_vs_run2: {'n': 200, 'flips': 0, 'agree': 1.0, 'dp_max': 0.012776, 'dp_mean': 0.0003833, 'identical_probs': False}
    - native_c1_vs_c8: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.010961, 'dp_mean': 0.0007695, 'identical_probs': False}
    - exact_vs_native_c1: {'n': 200, 'flips': 4, 'agree': 0.98, 'dp_max': 0.175393, 'dp_mean': 0.0192846, 'identical_probs': False}
    - exact_vs_native_c8: {'n': 200, 'flips': 5, 'agree': 0.975, 'dp_max': 0.181394, 'dp_mean': 0.0193053, 'identical_probs': False}
- client-side exact-size pre-resize (arm A server): {"c1": {"identical_probs_to_native": false, "agree": 0.98, "flips": 4, "dp_max": 0.175393, "server_ms_p50_native": 107.734, "server_ms_p50_exact": 122.378, "client_prep_ms_p50_exact": 22.814, "client_prep_ms_p50_native": 1.922, "net_p50_gain_ms_incl_client_resize": -35.54, "verdict": "fail"}, "c8": {"identical_probs_to_native": false, "agree": 0.975, "flips": 5, "dp_max": 0.181394, "server_ms_p50_native": 265.991, "server_ms_p50_exact": 238.103, "client_prep_ms_p50_exact": 28.144, "client_prep_ms_p50_native": 2.856, "net_p50_gain_ms_incl_client_resize": 2.6, "verdict": "fail"}}
- gain vs A: {}; adopt: {'adopt': False, 'why': 'the reference'}

### B. exact bundle (full prefill graph + skip-tokenizer-init + /v1/score + LM-head slice + metrics + gc warn)  (`r2_b`: NA)

- block error: `RuntimeError: SGLang exited (-9) during boot; last lines:
  File "/sgl-workspace/sglang/python/sglang/srt/managers/tp_worker.py", line 443, in init_cuda_graphs
    self.model_runner.init_cuda_graphs(
  File "/sgl-workspace/sglang/python/sglang/srt/model_executor/model_runner.py", line 1100, in init_cuda_graphs
    capture = capture_cuda_graphs(
              ^^^^^^^^^^^^^^^^^^^^
  File "/sgl-works`
- log scan: gc: 0; graph: 20; fallback: 0; error: 1; fp8: 0
    - error: `[2026-10-17 16:20:47] Scheduler hit an exception: Traceback (most recent call last):`
- LM-head patch report: {"n": 3, "events": [{"pid": 3166, "t": 1792254009.37, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 3197, "t": 1792254037.43, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 3198, "t": 1792254037.52, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 3166, "t": 1792254009.37, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 3197, "t": 1792254037.43, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 1
- gain vs A: {}; adopt: {'adopt': False, 'why': 'verdict NA'}

### B (variant). bundle + --disable-chunked-prefix-cache so that full-graph prefill can boot  (`r2_b_dcpc`: NA)

not run (not queued, or the plan did not reach it)

### B'. bundle without full-graph prefill  (`r2_b_nofull`: exact)

- prefill graph backend resolved by SGLang: `breakable`
- parity vs A (same session, c32): 8142/8143 = 0.999877 (Wilson95 [0.999305, 0.999978]), flips 1, max |dp| 0.030554, mean dp 0.0001651, flip ref-margin median 0.001 max 0.001, flips with ref margin <= 0.005/0.01/0.02/0.05/0.1: {'0.005': 1, '0.01': 1, '0.02': 1, '0.05': 1, '0.1': 1}
- per bucket: 10-25: 153/153 LB 0.975506 (underpowered); 2-4: 2527/2527 LB 0.998482; 26+: 234/234 LB 0.983848 (underpowered); 5-9: 899/900 LB 0.993733; noul: 4329/4329 LB 0.999113
- per view type: choice: 3813/3814 LB 0.998516; noul: 4329/4329 LB 0.999113
- batch-1 N, 2 x 320 calls: rep1 {'n': 320, 'p50': 29.54, 'p95': 38.27, 'p99': 81.41, 'mean': 31.62, 'max': 84.15, 'noul_p50': 28.99, 'choice_p50': 30.65}; rep2 {'n': 320, 'p50': 29.54, 'p95': 38.04, 'p99': 80.94, 'mean': 31.59, 'max': 95.41, 'noul_p50': 28.87, 'choice_p50': 30.64}; pooled {'n': 640, 'p50': 29.54, 'p95': 38.2, 'p99': 81.08, 'mean': 31.6, 'max': 95.41}; rep p50 spread 0.0 ms; delta vs A {'p50': -0.32, 'p95': 0.11, 'p99': -1.04}
- throughput: {"N_c64_dph": 326024, "N_c64_dph_runs": [325684.0, 326363.0], "N_c64_gpu_busy_pct": 84.9, "N_c64_cached_share": 0.0, "P_sat_c64_dph": 361681.0, "P_sat_c64_gpu_busy_pct": 85.0, "parity_pass_c32_dph": 345174.0, "parity_pass_cached_share": 0.0, "parity_pass_gpu_busy_pct": 85.8, "batch1_gpu_busy_pct": 46.5, "N_c64_dph_vs_A_pct": 0.1, "P_sat_c64_dph_vs_A_pct": -0.9, "parity_pass_c32_dph_vs_A_pct": 0.4}
- USD/1K (N c64): {'100%': 0.01348, '50%': 0.02696, '20%': 0.06741}; (P c64): {'100%': 0.01215, '50%': 0.0243, '20%': 0.06076}
- log scan: gc: 1; graph: 0; fallback: 1; error: 0; fp8: 0
    - gc: `[2026-10-17 16:22:04] LONG GARBAGE COLLECTION DETECTED | Generation 2 | Duration: 0.3630s | # Objects: gen0=0, gen1=0, gen2=1094650 | This may cause latency jitter. Consider calling the freeze_gc API after sending a few `
    - fallback: `[2026-10-17 16:22:04] Using fallback token IDs for yes/no (9693/2152)`
- LM-head patch report: {"n": 3, "events": [{"pid": 3280, "t": 1792254075.58, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 3312, "t": 1792254102.55, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 3313, "t": 1792254102.58, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 3280, "t": 1792254075.58, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 3312, "t": 1792254102.55, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 1
- gain vs A: {'p50_down_ms': 0.32, 'p99_down_ms': 1.04, 'p95_down_ms': -0.11, 'throughput_up_pct_N': 0.1, 'throughput_up_pct_P': -0.9, 'throughput_up_pct_min': -0.9}; adopt: {'adopt': False, 'why': 'bar met but no gain >= 2 ms p50/p99 or >= 5% throughput', 'gain': {'p50_down_ms': 0.32, 'p99_down_ms': 1.04, 'p95_down_ms': -0.11, 'throughput_up_pct_N': 0.1, 'throughput_up_pct_P': -0.9, 'throughput_up_pct_min': -0.9}}

### B+gc. bundle + gc.freeze() after warm-up  (`r2_b_gc`: exact (by construction; parity pass not re-run))

- prefill graph backend resolved by SGLang: `breakable`
- batch-1 N, 2 x 320 calls: rep1 {'n': 320, 'p50': 29.89, 'p95': 38.25, 'p99': 81.31, 'mean': 32.01, 'max': 105.27, 'noul_p50': 29.14, 'choice_p50': 30.93}; rep2 {'n': 320, 'p50': 29.71, 'p95': 37.97, 'p99': 80.67, 'mean': 31.61, 'max': 81.19, 'noul_p50': 29.01, 'choice_p50': 30.8}; pooled {'n': 640, 'p50': 29.78, 'p95': 38.17, 'p99': 81.05, 'mean': 31.81, 'max': 105.27}; rep p50 spread 0.18 ms; delta vs A {'p50': -0.08, 'p95': 0.08, 'p99': -1.07}
- throughput: {"N_c64_dph": 327698, "N_c64_dph_runs": [327738.0, 327657.0], "N_c64_gpu_busy_pct": 86.4, "N_c64_cached_share": 0.0, "P_sat_c64_dph": 363283.0, "P_sat_c64_gpu_busy_pct": 85.1, "batch1_gpu_busy_pct": 44.9, "N_c64_dph_vs_A_pct": 0.6, "P_sat_c64_dph_vs_A_pct": -0.5}
- USD/1K (N c64): {'100%': 0.01341, '50%': 0.02682, '20%': 0.06706}; (P c64): {'100%': 0.0121, '50%': 0.0242, '20%': 0.06049}
- log scan: gc: 1; graph: 0; fallback: 1; error: 0; fp8: 0
    - gc: `[2026-10-17 16:26:03] LONG GARBAGE COLLECTION DETECTED | Generation 2 | Duration: 0.3490s | # Objects: gen0=0, gen1=0, gen2=1094674 | This may cause latency jitter. Consider calling the freeze_gc API after sending a few `
    - fallback: `[2026-10-17 16:26:02] Using fallback token IDs for yes/no (9693/2152)`
- LM-head patch report: {"n": 7, "events": [{"pid": 4759, "t": 1792254314.86, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 4792, "t": 1792254341.5, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 4793, "t": 1792254341.53, "event": "patched", "target": "sglang.srt.layers.logits_processor", "n_ids": 141}, {"pid": 4792, "t": 1792254367.42, "event": "gc_frozen", "frozen": 1109958, "threshold": [700, 10, 10]}, {"pid": 4793, "t": 1792254367.57, "event": "gc_frozen", "frozen": 909730, "threshold": [700, 10, 10]}, {"pid": 4791, "t": 1792
- gain vs A: {'p50_down_ms': 0.08, 'p99_down_ms': 1.07, 'p95_down_ms': -0.08, 'throughput_up_pct_N': 0.6, 'throughput_up_pct_P': -0.5, 'throughput_up_pct_min': -0.5}; adopt: {'adopt': False, 'why': 'bar met but no gain >= 2 ms p50/p99 or >= 5% throughput', 'gain': {'p50_down_ms': 0.08, 'p99_down_ms': 1.07, 'p95_down_ms': -0.08, 'throughput_up_pct_N': 0.6, 'throughput_up_pct_P': -0.5, 'throughput_up_pct_min': -0.5}}

### C. block-FP8 checkpoint, --quantization fp8  (`r2_c`: fail)

- prefill graph backend resolved by SGLang: `breakable`
- parity vs A (same session, c32): 8011/8143 = 0.98379 (Wilson95 [0.98081, 0.986313]), flips 132, max |dp| 0.546921, mean dp 0.0105263, flip ref-margin median 0.0393 max 0.7564, flips with ref margin <= 0.005/0.01/0.02/0.05/0.1: {'0.005': 13, '0.01': 21, '0.02': 40, '0.05': 77, '0.1': 109}
- per bucket: 10-25: 149/153 LB 0.934712 (underpowered); 2-4: 2480/2527 LB 0.975356; 26+: 224/234 LB 0.923134 (underpowered); 5-9: 887/900 LB 0.975444; noul: 4271/4329 LB 0.98272
- per view type: choice: 3740/3814 LB 0.975712; noul: 4271/4329 LB 0.98272
- batch-1 N, 2 x 320 calls: rep1 {'n': 320, 'p50': 29.88, 'p95': 33.36, 'p99': 65.47, 'mean': 31.21, 'max': 108.69, 'noul_p50': 29.4, 'choice_p50': 30.82}; rep2 {'n': 320, 'p50': 29.71, 'p95': 33.55, 'p99': 65.38, 'mean': 30.98, 'max': 79.92, 'noul_p50': 29.22, 'choice_p50': 30.75}; pooled {'n': 640, 'p50': 29.81, 'p95': 33.39, 'p99': 65.47, 'mean': 31.09, 'max': 108.69}; rep p50 spread 0.17 ms; delta vs A {'p50': -0.05, 'p95': -4.7, 'p99': -16.65}
- throughput: {"N_c64_dph": 416410, "N_c64_dph_runs": [416063.0, 416758.0], "N_c64_gpu_busy_pct": 85.6, "N_c64_cached_share": 0.1728, "P_sat_c64_dph": 460453.0, "P_sat_c64_gpu_busy_pct": 84.2, "parity_pass_c32_dph": 429676.0, "parity_pass_cached_share": 0.2085, "parity_pass_gpu_busy_pct": 82.3, "batch1_gpu_busy_pct": 40.9, "N_c64_dph_vs_A_pct": 27.8, "P_sat_c64_dph_vs_A_pct": 26.2, "parity_pass_c32_dph_vs_A_pct": 25.0}
- USD/1K (N c64): {'100%': 0.01055, '50%': 0.02111, '20%': 0.05277}; (P c64): {'100%': 0.00955, '50%': 0.01909, '20%': 0.04773}
- log scan: gc: 0; graph: 0; fallback: 0; error: 0; fp8: 264
    - fp8: `Capturing num tokens (num_tokens=8192 avail_mem=16.50 GB):   0%|          | 0/58 [00:00<?, ?it/s][2026-10-17 16:28:30] Entering DeepGEMM JIT Pre-Compile session. It may take a long time (typically 10-20 mins) if you have`
    - fp8: `DeepGEMM warmup:   0%|          | 0/16384 [00:00<?, ?it/s][A`
    - fp8: `DeepGEMM warmup:   0%|          | 1/16384 [00:04<19:43:02,  4.33s/it][A`
- gain vs A: {'p50_down_ms': 0.05, 'p99_down_ms': 16.65, 'p95_down_ms': 4.7, 'throughput_up_pct_N': 27.8, 'throughput_up_pct_P': 26.2, 'throughput_up_pct_min': 26.2}; adopt: {'adopt': False, 'why': 'verdict fail'}

### D1. --keep-mm-feature-on-device (images)  (`r2_d1`: pass)

- prefill graph backend resolved by SGLang: `breakable`
- log scan: gc: 0; graph: 0; fallback: 0; error: 0; fp8: 0
- images (200 items, ms per decision = both views for choice items):
    - native:1#1: acc 86.0, p50 78.183 p95 110.815 p99 123.746, items/s 12.818, token mismatches 0, errors 0
    - native:1#2: acc 85.5, p50 75.123 p95 79.534 p99 82.2, items/s 17.237, token mismatches 0, errors 0
    - native:8#1: acc 86.0, p50 180.281 p95 239.351 p99 276.64, items/s 51.973, token mismatches 0, errors 0
    - native:8#2: acc 85.5, p50 174.426 p95 229.985 p99 243.164, items/s 53.338, token mismatches 0, errors 0
    - noise_floor_native_c1_run1_vs_run2: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.010536, 'dp_mean': 0.0008127, 'identical_probs': False}
    - noise_floor_native_c8_run1_vs_run2: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.010441, 'dp_mean': 0.0004494, 'identical_probs': False}
    - native_c1_vs_c8: {'n': 200, 'flips': 0, 'agree': 1.0, 'dp_max': 0.004507, 'dp_mean': 0.0007825, 'identical_probs': False}
    - native:1#1_vs_A_native:1#1: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.015975, 'dp_mean': 0.0015809, 'identical_probs': False}
    - native:1#2_vs_A_native:1#2: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.016331, 'dp_mean': 0.0015724, 'identical_probs': False}
    - native:8#1_vs_A_native:8#1: {'n': 200, 'flips': 2, 'agree': 0.99, 'dp_max': 0.015616, 'dp_mean': 0.0015716, 'identical_probs': False}
    - native:8#2_vs_A_native:8#2: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.016152, 'dp_mean': 0.0015395, 'identical_probs': False}
    - vs_r2_d2_native_c1_pass1: {'n': 200, 'flips': 0, 'agree': 1.0, 'dp_max': 0.0, 'dp_mean': 0.0, 'identical_probs': True}
- image latency gain vs arm A: {'c1#1_p50_down_ms': 29.55, 'c1#1_p95_down_ms': 50.43, 'c8#1_items_per_s_up_pct': 63.1, 'c8#1_p50_down_ms': 85.71, 'c1#2_p50_down_ms': 19.45, 'c1#2_p95_down_ms': 82.39, 'c8#2_items_per_s_up_pct': 66.2, 'c8#2_p50_down_ms': 74.6, 'note': "A's pass #1 ran after 5 min of text load, the D servers' pass #1 right after boot, so the steady-state passes (#2) are the fair comparison; p50/p95 are ms per image decision (both views for choice items)"}
- gain vs A: {}; adopt: {'adopt': True, 'why': 'bar met and a real gain', 'gain': {'c1#1_p50_down_ms': 29.55, 'c1#1_p95_down_ms': 50.43, 'c8#1_items_per_s_up_pct': 63.1, 'c8#1_p50_down_ms': 85.71, 'c1#2_p50_down_ms': 19.45, 'c1#2_p95_down_ms': 82.39, 'c8#2_items_per_s_up_pct': 66.2, 'c8#2_p50_down_ms': 74.6, 'note': "A's pass #1 ran after 5 min of text load, the D servers' pass #1 right after boot, so the steady-state passes (#2) are the fair comparison; p50/p95 are ms per image decision (both views for choice items)"}}

### D2. --mm-processor-worker-num 4 (images)  (`r2_d2`: pass)

- prefill graph backend resolved by SGLang: `breakable`
- log scan: gc: 0; graph: 0; fallback: 0; error: 0; fp8: 0
- images (200 items, ms per decision = both views for choice items):
    - native:1#1: acc 86.0, p50 100.955 p95 169.34 p99 200.085, items/s 9.563, token mismatches 0, errors 0
    - native:1#2: acc 85.5, p50 93.372 p95 134.817 p99 161.779, items/s 11.799, token mismatches 0, errors 0
    - native:8#1: acc 85.5, p50 300.986 p95 600.456 p99 7630.503, items/s 13.723, token mismatches 0, errors 0
    - native:8#2: acc 85.5, p50 278.402 p95 537.611 p99 573.492, items/s 27.249, token mismatches 0, errors 0
    - noise_floor_native_c1_run1_vs_run2: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.010536, 'dp_mean': 0.0008127, 'identical_probs': False}
    - noise_floor_native_c8_run1_vs_run2: {'n': 200, 'flips': 0, 'agree': 1.0, 'dp_max': 0.002765, 'dp_mean': 0.0003885, 'identical_probs': False}
    - native_c1_vs_c8: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.010536, 'dp_mean': 0.0008396, 'identical_probs': False}
    - native:1#1_vs_A_native:1#1: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.015975, 'dp_mean': 0.0015809, 'identical_probs': False}
    - native:1#2_vs_A_native:1#2: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.016331, 'dp_mean': 0.0015724, 'identical_probs': False}
    - native:8#1_vs_A_native:8#1: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.015616, 'dp_mean': 0.0015067, 'identical_probs': False}
    - native:8#2_vs_A_native:8#2: {'n': 200, 'flips': 1, 'agree': 0.995, 'dp_max': 0.016867, 'dp_mean': 0.0015542, 'identical_probs': False}
    - vs_r2_d1_native_c1_pass1: {'n': 200, 'flips': 0, 'agree': 1.0, 'dp_max': 0.0, 'dp_mean': 0.0, 'identical_probs': True}
- image latency gain vs arm A: {'c1#1_p50_down_ms': 6.78, 'c1#1_p95_down_ms': -8.09, 'c8#1_items_per_s_up_pct': -56.9, 'c8#1_p50_down_ms': -35.0, 'c1#2_p50_down_ms': 1.2, 'c1#2_p95_down_ms': 27.1, 'c8#2_items_per_s_up_pct': -15.1, 'c8#2_p50_down_ms': -29.38, 'note': "A's pass #1 ran after 5 min of text load, the D servers' pass #1 right after boot, so the steady-state passes (#2) are the fair comparison; p50/p95 are ms per image decision (both views for choice items)"}
- gain vs A: {}; adopt: {'adopt': False, 'why': 'bar met but no gain >= 2 ms p50/p99 or >= 5% throughput', 'gain': {'c1#1_p50_down_ms': 6.78, 'c1#1_p95_down_ms': -8.09, 'c8#1_items_per_s_up_pct': -56.9, 'c8#1_p50_down_ms': -35.0, 'c1#2_p50_down_ms': 1.2, 'c1#2_p95_down_ms': 27.1, 'c8#2_items_per_s_up_pct': -15.1, 'c8#2_p50_down_ms': -29.38, 'note': "A's pass #1 ran after 5 min of text load, the D servers' pass #1 right after boot, so the steady-state passes (#2) are the fair comparison; p50/p95 are ms per image decision (both views for choice items)"}}

### E1. --mamba-ssm-dtype bfloat16  (`r2_e1`: pass)

- prefill graph backend resolved by SGLang: `breakable`
- parity vs A (same session, c32): 8140/8143 = 0.999632 (Wilson95 [0.998917, 0.999875]), flips 3, max |dp| 0.031553, mean dp 0.0002795, flip ref-margin median 0.008 max 0.0146, flips with ref margin <= 0.005/0.01/0.02/0.05/0.1: {'0.005': 1, '0.01': 2, '0.02': 3, '0.05': 3, '0.1': 3}
- per bucket: 10-25: 153/153 LB 0.975506 (underpowered); 2-4: 2527/2527 LB 0.998482; 26+: 234/234 LB 0.983848 (underpowered); 5-9: 899/900 LB 0.993733; noul: 4327/4329 LB 0.998317
- per view type: choice: 3813/3814 LB 0.998516; noul: 4327/4329 LB 0.998317
- batch-1 N, 2 x 320 calls: rep1 {'n': 320, 'p50': 28.8, 'p95': 37.85, 'p99': 82.25, 'mean': 30.92, 'max': 119.08, 'noul_p50': 28.15, 'choice_p50': 29.74}; rep2 {'n': 320, 'p50': 28.74, 'p95': 37.49, 'p99': 82.06, 'mean': 30.84, 'max': 117.17, 'noul_p50': 28.06, 'choice_p50': 29.83}; pooled {'n': 640, 'p50': 28.77, 'p95': 37.75, 'p99': 82.06, 'mean': 30.88, 'max': 119.08}; rep p50 spread 0.06 ms; delta vs A {'p50': -1.09, 'p95': -0.34, 'p99': -0.06}
- throughput: {"N_c64_dph": 331396, "N_c64_dph_runs": [330186.0, 332607.0], "N_c64_gpu_busy_pct": 86.0, "N_c64_cached_share": 0.1693, "P_sat_c64_dph": 366586.0, "P_sat_c64_gpu_busy_pct": 86.8, "parity_pass_c32_dph": 352134.0, "parity_pass_cached_share": 0.2077, "parity_pass_gpu_busy_pct": 87.1, "batch1_gpu_busy_pct": 44.9, "N_c64_dph_vs_A_pct": 1.7, "P_sat_c64_dph_vs_A_pct": 0.4, "parity_pass_c32_dph_vs_A_pct": 2.5}
- USD/1K (N c64): {'100%': 0.01326, '50%': 0.02653, '20%': 0.06631}; (P c64): {'100%': 0.01199, '50%': 0.02398, '20%': 0.05995}
- R prefix-repeat set cached share: {'cached_token_share': 0.5271, 'rows': 800}
- log scan: gc: 0; graph: 0; fallback: 0; error: 0; fp8: 0
- gain vs A: {'p50_down_ms': 1.09, 'p99_down_ms': 0.06, 'p95_down_ms': 0.34, 'throughput_up_pct_N': 1.7, 'throughput_up_pct_P': 0.4, 'throughput_up_pct_min': 0.4}; adopt: {'adopt': False, 'why': 'bar met but no gain >= 2 ms p50/p99 or >= 5% throughput', 'gain': {'p50_down_ms': 1.09, 'p99_down_ms': 0.06, 'p95_down_ms': 0.34, 'throughput_up_pct_N': 1.7, 'throughput_up_pct_P': 0.4, 'throughput_up_pct_min': 0.4}}

### E2. --mamba-track-interval 64  (`r2_e2`: pass)

- prefill graph backend resolved by SGLang: `breakable`
- parity vs A (same session, c32): 8142/8143 = 0.999877 (Wilson95 [0.999305, 0.999978]), flips 1, max |dp| 0.031953, mean dp 0.0002244, flip ref-margin median 0.0021 max 0.0021, flips with ref margin <= 0.005/0.01/0.02/0.05/0.1: {'0.005': 1, '0.01': 1, '0.02': 1, '0.05': 1, '0.1': 1}
- per bucket: 10-25: 153/153 LB 0.975506 (underpowered); 2-4: 2526/2527 LB 0.997762; 26+: 234/234 LB 0.983848 (underpowered); 5-9: 900/900 LB 0.99575; noul: 4329/4329 LB 0.999113
- per view type: choice: 3813/3814 LB 0.998516; noul: 4329/4329 LB 0.999113
- batch-1 N, 2 x 320 calls: rep1 {'n': 320, 'p50': 30.18, 'p95': 38.24, 'p99': 83.08, 'mean': 32.1, 'max': 102.5, 'noul_p50': 29.39, 'choice_p50': 31.09}; rep2 {'n': 320, 'p50': 30.33, 'p95': 38.72, 'p99': 81.78, 'mean': 32.12, 'max': 83.69, 'noul_p50': 29.44, 'choice_p50': 31.27}; pooled {'n': 640, 'p50': 30.26, 'p95': 38.59, 'p99': 83.08, 'mean': 32.11, 'max': 102.5}; rep p50 spread 0.15 ms; delta vs A {'p50': 0.4, 'p95': 0.5, 'p99': 0.96}
- throughput: {"N_c64_dph": 328592, "N_c64_dph_runs": [326726.0, 330457.0], "N_c64_gpu_busy_pct": 89.2, "N_c64_cached_share": 0.1698, "P_sat_c64_dph": 361976.0, "P_sat_c64_gpu_busy_pct": 85.8, "parity_pass_c32_dph": 346073.0, "parity_pass_cached_share": 0.2079, "parity_pass_gpu_busy_pct": 87.2, "batch1_gpu_busy_pct": 48.9, "N_c64_dph_vs_A_pct": 0.8, "P_sat_c64_dph_vs_A_pct": -0.8, "parity_pass_c32_dph_vs_A_pct": 0.7}
- USD/1K (N c64): {'100%': 0.01338, '50%': 0.02675, '20%': 0.06688}; (P c64): {'100%': 0.01214, '50%': 0.02428, '20%': 0.06071}
- R prefix-repeat set cached share: {'cached_token_share': 0.5271, 'rows': 800}
- log scan: gc: 0; graph: 0; fallback: 0; error: 0; fp8: 0
- gain vs A: {'p50_down_ms': -0.4, 'p99_down_ms': -0.96, 'p95_down_ms': -0.5, 'throughput_up_pct_N': 0.8, 'throughput_up_pct_P': -0.8, 'throughput_up_pct_min': -0.8}; adopt: {'adopt': False, 'why': 'bar met but no gain >= 2 ms p50/p99 or >= 5% throughput', 'gain': {'p50_down_ms': -0.4, 'p99_down_ms': -0.96, 'p95_down_ms': -0.5, 'throughput_up_pct_N': 0.8, 'throughput_up_pct_P': -0.8, 'throughput_up_pct_min': -0.8}}

## Margin gate on arm C (offline, on the H100 answers)

- BF16 re-run vs reference (A c64 vs A c32): {'n': 8143, 'agree': 8141, 'flips': 2, 'agree_rate': 0.999754, 'wilson95': [0.999105, 0.999933], 'underpowered': False, 'pass_wilson': True, 'max_dp': 0.030554, 'flip_ref_margin_median': 0.0032, 'flip_ref_margin_max': 0.0032}
- fit_target_0.998: no gate (FP8 alone) {'n': 8143, 'tau': 0.0, 'deferred': 0, 'deferral_share': 0.0, 'flips': 132, 'agree_rate': 0.98379, 'wilson_lb': 0.98081}; split-half: {"fit0": {"tau": 0.14, "fit": {"n": 4098, "tau": 0.14, "deferred": 347, "deferral_share": 0.0847, "flips": 2, "agree_rate": 0.999512, "wilson_lb": 0.998222}, "test": {"n": 4045, "tau": 0.14, "deferred": 290, "deferral_share": 0.0717, "flips": 12, "agree_rate": 0.997033, "wilson_lb": 0.994821}}, "fit1": {"tau": 0.37, "fit": {"n": 4045, "tau": 0.37, "deferred": 688, "deferral_share": 0.1701, "flips": 2, "agree_rate": 0.999506, "wilson_lb": 0.998199}, "test": {"n": 4098, "tau": 0.37, "deferred": 771, "deferral_share": 0.1881, "flips": 0, "agree_rate": 1.0, "wilson_lb": 0.999063}}}
  full set at the larger fitted tau: {'n': 8143, 'tau': 0.37, 'deferred': 1459, 'deferral_share': 0.1792, 'flips': 2, 'agree_rate': 0.999754, 'wilson_lb': 0.999105}
- fit_target_0.996: no gate (FP8 alone) {'n': 8143, 'tau': 0.0, 'deferred': 0, 'deferral_share': 0.0, 'flips': 132, 'agree_rate': 0.98379, 'wilson_lb': 0.98081}; split-half: {"fit0": {"tau": 0.08, "fit": {"n": 4098, "tau": 0.08, "deferred": 215, "deferral_share": 0.0525, "flips": 8, "agree_rate": 0.998048, "wilson_lb": 0.996152}, "test": {"n": 4045, "tau": 0.08, "deferred": 172, "deferral_share": 0.0425, "flips": 18, "agree_rate": 0.99555, "wilson_lb": 0.992976}}, "fit1": {"tau": 0.245, "fit": {"n": 4045, "tau": 0.245, "deferred": 475, "deferral_share": 0.1174, "flips": 8, "agree_rate": 0.998022, "wilson_lb": 0.996102}, "test": {"n": 4098, "tau": 0.245, "deferred": 542, "deferral_share": 0.1323, "flips": 1, "agree_rate": 0.999756, "wilson_lb": 0.998619}}}
  full set at the larger fitted tau: {'n': 8143, 'tau': 0.245, 'deferred': 1017, 'deferral_share': 0.1249, 'flips': 9, 'agree_rate': 0.998895, 'wilson_lb': 0.997901}
- cascade estimate: {"fit_target": 0.998, "tau": 0.37, "deferral_share": 0.1792, "flips_full_set": 2, "agree_full_set": 0.999754, "wilson_lb_full_set": 0.999105, "half_results": {"fit0": {"tau": 0.14, "test": {"n": 4045, "tau": 0.14, "deferred": 290, "deferral_share": 0.0717, "flips": 12, "agree_rate": 0.997033, "wilson_lb": 0.994821}}, "fit1": {"tau": 0.37, "test": {"n": 4098, "tau": 0.37, "deferred": 771, "deferral_share": 0.1881, "flips": 0, "agree_rate": 1.0, "wilson_lb": 0.999063}}}, "no_gate_fp8": {"n": 8143, "tau": 0.0, "deferred": 0, "deferral_share": 0.0, "flips": 132, "agree_rate": 0.98379, "wilson_lb": 0.98081}, "throughput_P_sat_c64_dph": {"fp8": 460453.0, "bf16": 364985.0, "cascade_effective": 375551, "gain_vs_bf16_pct": 2.9, "usd_per_1k": {"100%": 0.0117, "50%": 0.02341, "20%": 0.05852}, "model": "GPU-seconds add: 1/T = 1/T_fp8 + deferral_share/T_bf16 (both models resident, one stream)"}, "batch1_latency_ms": {"n": 320, "p50": 30.28, "p95": 66.98, "p99": 107.91, "mean": 37.91, "max": 159.12, "deferred_in_N": 61, "model": "per N id: FP8 call, plus the BF16 call when the FP8 margin < tau (sequential, no router cost)"}}


Cascade ladder (FP8 answer when its margin >= tau, else the BF16 re-run; in-sample on all 8,143 items):

| tau | deferred | flips (half0/half1) | agree | Wilson LB (full / half0 / half1) | bar met: full, both halves | cascade dec/h (P c64) | vs BF16 | USD/1K @100% | batch-1 p50/p95/p99 ms (N) |
|---|---|---|---|---|---|---|---|---|---|
| 0.05 | 0.0316 | 42 (20/22) | 0.994842 | 0.993036 / 0.992473 / 0.991778 | False, False | 442822 | 21.3% | 0.00993 | [29.86, 58.02, 65.61] |
| 0.08 | 0.0475 | 26 (8/18) | 0.996807 | 0.995326 / 0.996152 / 0.992976 | True, False | 434407 | 19.0% | 0.01012 | [29.93, 58.98, 73.63] |
| 0.1 | 0.0588 | 21 (5/16) | 0.997421 | 0.996061 / 0.997147 / 0.993584 | True, False | 428643 | 17.4% | 0.01025 | [29.98, 59.35, 73.63] |
| 0.12 | 0.0689 | 20 (5/15) | 0.997544 | 0.996209 / 0.997147 / 0.99389 | True, False | 423633 | 16.1% | 0.01038 | [29.98, 61.32, 85.24] |
| 0.14 | 0.0782 | 14 (2/12) | 0.998281 | 0.997116 / 0.998222 / 0.994821 | True, False | 419093 | 14.8% | 0.01049 | [30.02, 62.5, 101.06] |
| 0.15 | 0.0825 | 14 (2/12) | 0.998281 | 0.997116 / 0.998222 / 0.994821 | True, False | 417035 | 14.3% | 0.01054 | [30.02, 62.5, 101.06] |
| 0.2 | 0.1063 | 10 (1/9) | 0.998772 | 0.997741 / 0.998619 / 0.995776 | True, True | 405984 | 11.2% | 0.01083 | [30.08, 65.41, 107.91] |
| 0.245 | 0.1249 | 9 (1/8) | 0.998895 | 0.997901 / 0.998619 / 0.996102 | True, True | 397779 | 9.0% | 0.01105 | [30.12, 66.62, 107.91] |
| 0.3 | 0.1488 | 4 (1/3) | 0.999509 | 0.998738 / 0.998619 / 0.997822 | True, True | 387661 | 6.2% | 0.01134 | [30.17, 66.62, 107.91] |
| 0.37 | 0.1792 | 2 (0/2) | 0.999754 | 0.999105 / 0.999063 / 0.998199 | True, True | 375562 | 2.9% | 0.0117 | [30.28, 66.98, 107.91] |
| 0.5 | 0.2443 | 2 (0/2) | 0.999754 | 0.999105 / 0.999063 / 0.998199 | True, True | 351988 | -3.6% | 0.01249 | [30.43, 68.96, 148.07] |

## Billing (jaypatil-duke, `modal billing summary` / `report`)

```
{
 "before": {
  "taken_utc": "2026-10-17T16:11:41Z",
  "metered_cost_usd": "25.57541881",
  "credits_applied_usd": "-24.88000000",
  "billed_cost_usd": "0E-8",
  "ephemeral_apps_usd": "24.89655121",
  "volumes_usd": "0.68094119"
 },
 "after": {
  "taken_utc": "2026-10-17T17:01:05Z",
  "metered_cost_usd": "28.23541921",
  "credits_applied_usd": "-27.54000000",
  "billed_cost_usd": "0E-8",
  "ephemeral_apps_usd": "27.55808934",
  "volumes_usd": "0.68094119"
 },
 "delta_metered_usd": 2.66,
 "delta_credits_applied_usd": -2.66,
 "report_app_cost_by_resource_usd": {
  "Network Egress": 0.0,
  "CPU": 0.1087,
  "Memory": 0.1471,
  "H100": 2.2691
 },
 "report_app_cost_total_usd": 2.5248
}
```

## How this window was run, and what to know before relying on it

- One Modal app, one H100 container (`H100!`, region 'any' x1.0; it landed in us-central on an H100 80GB HBM3, driver 610.57.04), profile jaypatil-duke only, fresh ledger `h100/ledger.json` (cap 5.00, stop-launch 4.50, cancel 4.80; nothing was cancelled or skipped by the budget gate). Image layers came from the 17 Oct cache (container up 6 s after spawn).
- Blocks run in the priority order A, B, C, D, E; conditional blocks were decided by code from what the block showed: `r2_b` failed to boot, so `r2_b_nofull` followed; the GC log line (one benign 0.36 s generation-2 pass at warm-up) triggered `r2_b_gc`; `r2_b_dcpc` (`--disable-chunked-prefix-cache`) was NOT run because the failure was not the chunked-prefix assertion.
- Parity was measured at concurrency 32 (not 16) to save GPU time, with a canary on the first 300 decisions for every non-reference arm (stops a catastrophic arm early; it never fired). Arm A also ran a second full pass at c64: that is the BF16 self-agreement floor (2 flips) and the 'BF16 re-run' of the margin-gate replay.
- Throughput: 'N c64' = the 660-call natural-mix set twice (short runs, shown as the mean of two); 'P c64' = the first 2,500 parity rows (longer, steadier). Both are closed loops with caches flushed before. Cost per 1K = rate / (decisions per hour x utilisation) x 1000 with rate USD 4.3952/h (list rates for the container); the hourly billing report priced the whole window at about USD 2.52 for 2,060 s of container time (about USD 4.41/h all-in, within 1% of that rate).
- Block-FP8 checkpoint: built on od-cpu1/od-l4b (byte-identical), brought to the laptop in 200 MB parts through the IAP tunnel (each part sha256-checked, shard shas rebuilt and matched 4bbce991... / d01e6983...), uploaded to the Volume (`models/q35_4b_main500k_merged__fp8_block`) with a per-file manifest, and the manifest + both shard shas were re-verified INSIDE the container before arm C (no problems). One edit: `config.json` `modules_to_not_convert` got 24 extra entries `model.visual.blocks.N.attn.qkv_proj` (SGLang names the vision qkv `qkv_proj`; the checkpoint's list says `attn.qkv`, which SGLang would not match for Qwen3.5). Shards are untouched; original config sha256 3a741cef..., edited a1e79ec9.... It booted with DeepGEMM (a one-off 16,384-kernel JIT pre-compile made that boot 220 s instead of ~80 s).
- The LM-head slice patch (`r2pypatch/sitecustomize.py.as_run_17oct`) is what ran. The copy in `r2pypatch/sitecustomize.py` is a later version with per-reason counters and without the `extend_return_logprob` condition; it was only CPU-tested and has NOT been run on a GPU.
- Nothing was changed on od-l4b/production, C2 data/tools, HANDOFF.md or PREREG_FINAL.md; no OpenRouter/Jev call; no path containing ohs/sealed/quarantine/longbench was opened. The FP8 checkpoint stays on the Volume (about 5.5 GB; Volumes bill about USD 0.09 per GiB-month).
- Code: `modal_app_r2.py`, `oc1/` (copy of the 17 Oct harness plus `oc1/r2.py`), `tests/test_r2.py` (12 CPU tests, all pass), `analyze_h100.py` (this file's generator), `r2_report.py`, `billing/`, `results/session_20261017_161152/`.

## Adoptable set

['r2_d1']
