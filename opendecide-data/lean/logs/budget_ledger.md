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
| – | RESULT q35_2b_v11r (A13) dev gate FAILED again: dev_nc 68.2 plain / 70.0 BC (gate 71.3). Gains: pg_dev +5.7, hard_dev +2.4, dev_negwords +2.4, dev +2.9, taskbank +1.2. Losses: devp_card -1.5, devzs -0.9. Billed after A13: $21.86. No OHS-2 run for the 2B. | | | |
| A14 | E0: JevBench half A, q35_2b_v11r with CUDA graphs | H100 | ~0.3 | |
| A15 | E0: attack + wide-option suites (eval_opi, eval_jagged, eval_card): q35_2b_v11r and q35_4b_v11c | H100 | ~0.4 | 4B never measured on these before |
| A16 | P0: separation forward-only checks on q35_2b_v11r (T0a mechanism, T0b kernel path, clean dev-select accuracy with untrained block p=0.25, head rules first/random/low-write, beta-only/g-only) | H100 | ~0.4 | |
| – | RESULT E0, JevBench half A (official public-only scoring): q35_2b_v11r 101/118, score v14 76.85 (Jev 72.51, 4B v11c 74.80, old 2B pilot 74.86); hard tier 76% = Jev; calibration 81.3 vs 76.4; p50 9 ms vs 239 ms. Paired accuracy vs Jev -1.7 pp [-9.3, +5.9]. Half A is a dev set. | | | |
| – | RESULT E0, attacks: jagged audit attack success Jev 100% / 4B v11c 1.1% / 2B v11r 3.9% (attacked accuracy 26.5 / 95.9 / 91.2). OPI with Jev guard prompt: ASR 1.3 / 1.0 / 2.4% (all ties). eval_card wide options: Jev 86.3 / 4B 89.8 / 2B 86.5. | | | |
| – | RESULT P0 (bf16, q35_2b_v11r, dev-select dev_nc/hard_dev/pg_dev, n=1,138): T0b PASS (wrapper fires and blocks on 18/18 DeltaNet layers per forward, fla installed). Clean accuracy: off 62.04; untrained block p=0.25 first 55.27 / random 55.18 / low-write 54.92; first beta-only 52.64 / g-only 52.64. Best drop -6.8 pp <= 10, gate GO. T0a: policy state with evidence E vs E' max rel diff 8.5e-5 (data heads 0.05-0.24); vs T-alone state median 7e-7, max 1.8e-2, which misses the literal 1e-5 threshold; hypothesis: bf16 chunk-alignment rounding, fp32 re-check A17. Trusted-position hidden states identical (0.0). erank of the policy state is about 8 of 128 (median). | | | |
| A17 | P0 T0a re-check in fp32 (mechanism only) | H100 | ~0.15 | |
| – | RESULT A17 (fp32 load; fla triton kernels use TF32 dots, about 5e-4 precision): policy state T+E vs T median 6.3e-4 / max 2.3e-3 (bf16 max was 1.8e-2), E vs E' median 6.3e-4 / max 2.8e-3; trusted hidden states, which must be equal by causality, also differ by up to 5e-4, so this is the kernel's noise floor. Data heads 0.05-0.24. Deviation shrinks with precision and stays >= 20x below the evidence effect in every triple: no leak; the literal 1e-5 threshold cannot be reached with these kernels. P0 verdict: GO (precision-limited T0a). Top-up TODO: an fp64 pure-torch reference check (fla off) to show exactness < 1e-10. | | | |
| A18 | TRAIN q35_4b_v12t = teacher round T: from q35_4b_v11c, 400 steps (0.727 epoch) on train_4b_v12t (8,800 rows: hard12 x2, proc12, planted12, clean replay 4,200 with the legacy 235B rows removed and Claude cards swapped in), lr 4e-5, gold labels, v0.11 loss | H100 | ~2.0 | gate T: dev-confirm micro >= v11c + 1.3 pp (LB > 0), Brier not worse by > 0.005, ASR not worse by > 2 pp |
| – | RESULT A18 gate T FAILED: q35_4b_v12t vs v11c on dev-confirm -0.69 pp [-1.54, +0.15] (needed +1.3, LB > 0), yes/no Brier +0.002; dev-select -0.44. In-family v12 devs improved: hard12 81.4 -> 88.7, proc12 70.4 -> 77.4, planted12 80.3 -> 98.5 (2B v11r: 64.9 / 60.4 / 80.3). Lesson: narrow hard items teach in-family and do not transfer to broad dev; slight forgetting on classification (dev_nc -2.2, devzs -1.8). Keep v11c as teacher. Top-up: breadth (Claude-labelled broad decisions) plus more replay. | | | |
| A19 | multi_eval v11c + 2B v11r on the new v12 dev splits (baselines) | H100 | ~0.15 | |

## Google Cloud (project system-one-509903, $300 trial credit on billing account 01DE8E-AEC6DB-5712C5)
| # | What | GPU | Est. $ | Note |
|---|---|---|---|---|
| G1 | L4 VM od-l4 (us-central1-a) setup, parity vs Modal (4B v11c dev 99.5% same answers), OOM fix and save-and-resume test (killed and resumed within GPU noise) | L4 | ~1 | |
| G2 | TRAIN q35_4b_v13t = v11c + 1,200 steps (0.497 epoch) on train_v13t (38,660 rows: breadth 15,640 + Claude items 3,719 + clean replay 19,301; 4,330 soft labels), lr 4e-5, kd 0.5, micro_tokens 10240, then 13 dev splits | L4 | ~6.5 | about 19 s/step |
| – | RESULT: dev-confirm +0.64 pp [-0.15, +1.46] vs v11c: gate FAILED (needs +1.3, LB > 0). Yes/no Brier improved (-0.0051 confirm, -0.0068 select); dev-select +0.73. In-family: breadth_dev 76.8 -> 80.5, proc12 69.8 -> 77.4, hard12 81.4 -> 84.5, planted12 80.3 -> 96.4. Losses: dev_nc -2.6 (confirm), hard_dev -1.8, dev -1.0. Keep v11c as teacher; q35_4b_v13t saved as candidate (backups/modal_models/q35_4b_v13t). Next idea: blend v11c + v13t. | | | |
| G3 | L4 chain: blend q35_4b_blend50 (0.5 v11c + 0.5 v13t) on 13 dev splits; 2B v11r baselines on the new devs; blend teacher labels for teacher_pool (59,617 clean rows) | L4 | ~4.5 | RESULT blend: dev-confirm +0.57 [+0.00, +1.13], gate FAIL; Brier -0.0034; dev_nc drop cut to -1.1; breadth_dev 78.6. Teacher labels: preds_teacher_pool/q35_4b_blend50_teacher.jsonl |

## Modal extra accounts (mahadikarya2 / mahadikarya3 / mahadikarya44): PRISM layout test, 2B from base, 800 steps, blend-teacher kd 0.5, H100
| # | Arm | dev-confirm micro | jagged ASR | OPI ASR | breadth_dev |
|---|---|---|---|---|---|
| M1 | A text_first (current) | 72.38 | 4.7% | 5.8% | 74.9 |
| M2 | B schema_first (untrusted text last) | 70.48 (-1.91 [-3.37, -0.42]) | 64.8% | 2.6% | 76.7 |
| M3 | C schema_first + trust markers | 68.72 | 34.2% | 2.8% | 75.6 |
| – | RESULT: gate L FAILED. Untrusted text placed last before the answer is much easier to hijack (recency). Markers halve that but do not fix it. Fix, as in the master plan: schema -> text -> question repeated (trusted branch) -> answer. Clean 2B at 800 steps is -2.9/-3.9 pp vs v11r (under-trained). | | | | |
