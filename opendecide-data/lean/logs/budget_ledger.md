# Budget ledger: "beat Jev" loop on Modal account mahadikarya44

**Caps:**
- Modal: $30 credit, hard stop at **$28** (billing lags by up to about an hour).
- OpenRouter key: $5 limit with $4.33 left at start, stop at $4.80 used.

**Rates** (`modal billing rates`, 26 Sep 2026): H100 $3.95/h · A100-80 $2.50/h · L40S $1.95/h · L4 $0.80/h · CPU $0.047/core-h · memory $0.008/GiB-h. Every estimate adds 10% for CPU and memory.

**Starting balances:**
- mahadikarya44: $0.00 spent.
- mahadikarya3 (old): $24.21 spent, $5.79 left, unused unless noted.
- OpenRouter: $0.673 used.

| # | Run | GPU | Est. $ | Billed $ (check) | Notes |
|---|---|---|---|---|---|
| 1 | frozen Qwen3.5-4B baseline, 8 splits (cygnet) | L40S | ~0.50 | | P1 |
| 2 | training speed smoke, Qwen3.5-4B, 0.01 epoch | H100 | ~0.35 | | P1 |
| 3 | training speed smoke 2 (bucketed lengths), 0.04 epoch | H100 | ~0.60 | | P1 |
| – | OpenRouter: LAH pilot 10 items | API | 0.005 | | P2 |
| – | OpenRouter: LAH 2,400 items (cap) | API | ~1.3 | 1.39 (real) | 1,669 kept (self-verified) |
| 4 | JevBench half A, frozen Qwen3.5-4B + robust decoding (sym+LBD), cygnet | H100 | ~0.40 | | 80/118 (LBD hurts untrained; sym-only 95) |
| 5 | padding probe x2 (padding/batching change probs < 0.001) | L4 | ~0.10 | | |
| 6 | TRAIN q35_4b_v07: Qwen3.5-4B LoRA r16, A3 + KL anchor (beta 1), cygnet, 0.5 epoch of train_v07 (52.5k rows, ~1,640 steps), lr 7e-5 | H100 | ~5.6 | | + plain preds on dev, devzs, devp_card, pg_dev |
| 7 | robust-decoding correctness check (Qwen3.5-0.8B) x2 | L4 | ~0.08 | | batched = per-row within bf16 noise; two-stage same decisions |
| – | OpenRouter: meta-claim texts (gen_meta.py, 160 calls) | API | ~0.03 | | |
| – | OpenRouter: second verifier gpt-oss-120b on 1,667 LAH items | API | 0.37 est | | 1,518 kept (both verifiers agree) |

**OpenRouter used after LAH + verify: $2.178** (stop at $4.80).
| 8 | TRAIN q35_4b_v08 = stage 2 from v07: 0.8 epoch of train_v08s2 (3,036 double-verified LAH + 6,004 replay), lr 4e-5 | H100 | ~2.3 | | + plain preds on dev splits |
| 9 | EVAL q35_4b_v07 plain + full system (all variants), 9 splits (dev, devzs, devp_card, pg_dev, eval_card, jagged, opi, long, multi) | H100 | ~2.2 | | |
| 10 | JevBench half A, q35_4b_v07 plain, cygnet, warm-up | H100 | ~0.4 | | |
| 11 | latency probe: CUDA graphs vs eager (v07, JevBench A prompts) | H100 | ~0.4 | | |
| 12 | JevBench half A, q35_4b_v08 plain + CUDA graphs | H100 | ~0.4 | | selection v07 vs v08 |
| 13 | TRAIN q35_4b_v09 = stage 3 from v08: 0.6 epoch of train_v09s3 (5,578 judge rows + 5,005 replay), lr 4e-5 | H100 | ~1.9 | | |
| 14 | JevBench half A, q35_4b_v09 plain + CUDA graphs | H100 | ~0.4 | | |
| 15 | TRAIN q35_4b_v10 = stage 4 from v09: 0.8 epoch of train_v10s4 (2,335 debate + 4,300 replay), lr 4e-5 | H100 | ~1.6 | | |
| 16 | debate_dev predictions (selection v09 vs v10), 2 small runs | L40S | ~0.3 | | |
| 17 | JevBench half A, q35_4b_v10 plain + CUDA graphs | H100 | ~0.4 | | |
| 18 | FINAL EVAL q35_4b_v10 plain + full system (two-stage, meta floor 0.3), 10 splits | H100 | ~2.0 | | |
| 19 | JevBench half A, q35_4b_v10 robust (sym + LBD two-stage tau .35 meta .9) + CUDA graphs | H100 | ~0.5 | | |
| 20 | graph debugging (0.8B, 4 small runs) + 2 failed robust launches (OOM / assert) | L4/H100 | ~0.6 | | |
| 21 | JevBench half B (confirmation, once), q35_4b_v10 plain + CUDA graphs (B=1) | H100 | ~0.4 | | |
| 22 | end-to-end latency via direct tunnel, q35_4b_v10 plain + CUDA graphs, 515 eval calls | H100 | ~0.4 | | |

**Final check (26 Sep 2026, ~12:50 EDT):** `modal billing report` shows $19.70 billed; runs from the last hour were
still being billed, so the real total is about $22-23 of the $30 credit (under the $28 stop). No apps left running.
OpenRouter: $2.18 used on the key in total ($1.50 in this loop). Old account (mahadikarya3) untouched in this loop.

## $10 round (account mahadikarya44, billed $19.78 at start; stop when billed + running estimate reaches $29.5)

| # | Run | Hardware | Est. $ | Notes |
|---|---|---|---|---|
| 23 | Decision Index 0.2 suite rebuild + stratified sample (CPU) | 8 CPU | ~0.3 | independent 40-benchmark suite |
| 23b | (DI rebuild stopped: HLE is a gated dataset; ~0.1 CPU spent) | CPU | ~0.1 | needs HLE access or the user's OK |
| 24 | teacher labels: v0.10 soft answers on the 12k pilot mix | H100 | ~0.25 | for 0.8B / 2B students |
| 25 | TRAIN pilot q35_2b_kd: Qwen3.5-2B LoRA r32, A3 + KL anchor + distillation (kd 0.5), 1 epoch of 12k pilot mix | H100 | ~1.6 | + dev preds |
| 26 | TRAIN pilot q35_08b_kd: Qwen3.5-0.8B, same recipe | H100 | ~1.1 | + dev preds |
| 27 | v0.10 sweep: LoRA scale 0.7/0.85/1.0/1.15/1.3 + option-order averaging, dev splits + JevBench half A | H100 | ~1.0 | zero-training ideas |
| 28 | JevBench half A: q35_2b_kd and q35_08b_kd (plain + CUDA graphs) | H100 x2 | ~0.6 | can a 2B/0.8B beat Jev? |
| 29 | OHS-1 core (pre-registered, commit 273e76b): v0.10, frozen 4B, 2B student, 0.8B student, plain readout | H100 | ~1.0 | held-out test |
| – | OpenRouter: Jev x2 on OHS-1 (guard) | API | ~0.2 | run-to-run noise |

**$10 round closed (26 Sep 2026):** Modal billed $24.65 on mahadikarya44 at close (runs from the last hour may add
about $1; no apps left running). OpenRouter key usage $2.305 in total (Jev x2 on OHS-1 cost $0.12). GPU work stopped as
planned; the next steps are in FREEZE.md for the $30 account.

## Account atmosphor (workspace admin-22544, $30 credit; started 26 Sep 2026 at $0 billed; hard stop $28)

| # | Run | Hardware | Est. $ | Notes |
|---|---|---|---|---|
| A1 | teacher probes: frozen Qwen3.5-27B, Qwen3.5-35B-A3B, Qwen3.5-9B on dev splits + JevBench half A | H100 x3 | ~2.5 | choose the distillation teacher on dev only |
| A2 | TRAIN q35_4b_v11: Qwen3.5-4B from base, v0.11 mix (57k rows: task bank with Claude definitions, Claude hard items x2, fixed intents/claims/negation, replay), 0.5 epoch, lam 1, lam_inv 1, sym_cons, perm_twin 0.3 | H100 | ~8.3 | + dev preds for the gate |
| A3 | baselines on the new dev sets: v0.10 and frozen 4B | H100 | ~0.5 | gate reference |
| – | v0.11 gate: dev_nc 71.9 vs v0.10 72.1 (needed 74.1) -> FAIL as-is. Gains: negation words +8.2, task bank +2.9, hard +1.5, 32/56-way +10/+8. Losses: binary judgments biased (over-flagging, too lenient on consistency). | | | |
| A4 | weight blend v0.10 x v0.11 (w = 0.3/0.5/0.7 on v0.10), dev splits only | H100 | ~0.8 | zero-training fix attempt |
| A5 | TRAIN q35_4b_v11b = fix-up from blend q35_4b_v11s30 (0.3 v10 + 0.7 v11): 948 Claude binary judgments x2 + all judge rows + v11 replay, 0.4 epoch, lr 4e-5 | H100 | ~1.9 | binary-bias fix |
| A6 | OHS-1 (once) for q35_4b_v11b, plain | H100 | ~0.5 | pre-registered test |
| A7 | JevBench half A for q35_4b_v11b, CUDA graphs | H100 | ~0.4 | dev benchmark |
| – | RESULT v0.11b on OHS-1 (all): 77.9 plain / 78.5 with batch calibration vs Jev 81.7 (-3.7 / -3.1, significant); v0.10 was 76.1. Sealed half: 77.4 / 78.4 vs 81.5. JevBench half A 100/118 (v0.10 104, Jev 103). Consistency now better than Jev on complement (0.080 vs 0.097) and double negation (0.101 vs 0.162). NOTE: OHS-1 task-level results have guided data choices since v0.10, so the final public claim needs a fresh OHS-2. | | | |
| A8 | TRAIN q35_4b_v11c = from v11b: 882 Claude standard-doctrine items x2 + procedural/judge replay + binj + v11 replay (   17022 rows), 0.352 epoch (~375 steps), lr 4e-5 | H100 | ~1.8 | |
| – | OpenRouter: Jev x2 on OHS-2 (guard) | API | ~0.1 | fresh held-out test |
| A9 | OHS-2 (pre-registered, amendment f2b103f): q35_4b_v11c + q35_4b_v10 reference; v11c also on OHS-1 | H100 | ~0.8 | fair final test |
| A10 | JevBench half A: q35_4b_v11c with CUDA graphs | H100 | ~0.4 | |
| – | RESULT OHS-2 (fresh, pre-registered): v11c 79.9 plain / 80.5 BC vs Jev 81.5 (-1.6 [-3.3,+0.1], p_holm 0.14: not significant); v10 78.3 (-3.3, significant). Jev better on yes/no Brier (0.038 vs 0.083). JevBench half A: v11c 107/118 (Jev 103). | | | |
| A11 | teacher labels: q35_4b_v11c on the 2B mix (train_v11 + binj + std x2) | H100 | ~1.5 | for the 2B student |
| A12 | TRAIN q35_2b_v11: Qwen3.5-2B from base, LoRA r32, distilled from q35_4b_v11c (kd 0.5) on the 2B mix (59.7k rows), 0.4 epoch (~1,493 steps), lr 1e-4, full v0.11 loss | H100 | ~3.6 | |
| – | RESULT q35_2b_v11 dev gate FAILED: dev_nc 68.5 plain / 69.5 BC (gate >= 71.3; 4B v11c 74.3). Biggest gaps: hard_policy, hard_evidence, pg reasoning, biasframes intent, manifesto. Better than the old 2B pilot on devzs/devp_card/dev (+4/+5/+10). Billed so far $17.90. Not run on OHS-2. | | | |
| A13 | TRAIN q35_2b_v11r = continue q35_2b_v11 on the 34,995 rows it had not seen (train_2b_rest, trainer shuffle replayed), 1 epoch (~2,188 steps), lr 5e-5, same loss + kd 0.5 | H100 | ~4.0 | 2B dev gate retry |
| – | PRISM-2B master plan written (../../PRISM_2B_MASTER_PLAN.md): the current account is for evaluation only (E0 > P0 > K0); new data goes into a 4B teacher round on the top-up first. v12 2B training round deferred. | | 0 | |
| – | Compliance audit: no 9B/27B/35B probe output in any training file. Legacy Qwen3-235B involvement in about 9k of the 59.7k 2B-mix rows (lah 1,518, meta 1,500, about 5,960 compile_cards cards): drop from future mixes and disclose the lineage. | | 0 | |
