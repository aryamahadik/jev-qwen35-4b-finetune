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
