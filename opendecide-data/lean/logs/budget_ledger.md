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
| M4 | D schema_branch (question repeated after the text) | 72.66 (vs A +0.27 [-1.09, +1.65]) | 42.7% | 2.9% | 74.8 |
| M5 | E schema_branch + trust markers | 72.58 (vs A +0.20) | 5.8% | 2.3% | 75.6 |
| – | RESULT: PRISM v2 layout = schema -> marked text -> trusted question branch -> answer (arm E) PASSES gate L: accuracy equal to text_first within noise, jagged ASR 5.8% vs 4.7% (within +3 pp), OPI better (2.3% vs 5.8%). The branch alone (D) or the markers alone (C) do not fix the jagged attack; both are needed. Next: F = E + protected memory (write-block on policy heads after the trusted prefix). | | | | |
| M6 | F = E + protected memory (write-block after the trusted prefix, 4/16 DeltaNet v-heads, 18 layers), trained 800 steps; ablation = same weights, block off | 66.69 (vs E -5.89 [-7.31, -4.50]) | 30.4% (off: 99.7%) | 1.1% (off: 1.7%) | 73.3 |
| – | RESULT gate S FAILED: taking over 25% of heads costs about 5.5 pp accuracy (untrained P0 cost was 6.8) and the jagged ASR is worse. Reliance is proven: switching the block off in the trained F model sends jagged ASR 30.4% -> 99.7%, so the model routes its defence through the protected state. Gains: OPI 1.1% (best), definition-overwrite ASR 0.8% (E 2.8%, off 4.0%; new attack set eval_redef is weak, n~250). Next design: SHADOW memory (add protected copies of policy heads instead of taking over existing heads) or fewer heads plus longer training. Keep E as the PRISM layout. | | | | |

## PRISM-X code check (28 Sep 2026, Modal atmosphor, H100): code only, no experiment
| # | What | Result |
|---|---|---|
| X1 | CPU tests: tests/test_prism_x.py (10) + tests/test_train_loss.py (47) | all pass |
| X2 | 6-step smoke, arm J (all parts on), 200-row slice incl. 50 anchor rows, then 48-row predictions with PRISM-X on and off | zero-init self-check max logit diff 0.0 (exactly E at init); every hook fired; KL anchor 0.0 at step 0; losses finite; all new parts moving (gate max 0.009, head weight 0.008); 48/48 valid predictions; on vs off differs (1 answer flip) |
| X3 | Reload from the volume (maybe_load + merge_and_unload, run with layout text_first to check the automatic layout switch) | PRISM-X re-installed (51.4M params); 0 of 48 answers differ from in-training predictions (max prob diff 0.018, bf16 merge noise) |

## PRISM-X arms on the Google L4 (28 Sep 2026; 2B from base, 800 steps, matched to arm E; micro_tokens 16384)
| # | Arm | dev-confirm vs E | yes/no Brier vs E | jagged ASR (E 5.8%) | OPI ASR (E 2.3%) | redef ASR (E 2.8%) | PRISM-X off |
|---|---|---|---|---|---|---|---|
| X4 | H = authority signal + shadow memory (2 heads/layer), 166 min training | +0.25 [-0.89, +1.34] (72.83 vs 72.58) | -0.010 (better) | 17.2% | 3.0% | 8.8% | jagged 45.4%, OPI 2.9%, redef 10.6% |
| – | RESULT gate H: accuracy PASS (>= -0.5), calibration better, security FAIL (jagged 17.2% > 8.8%; OPI 3.0% > 1.3%). The model relies on the new parts again (switching them off: jagged 17.2% -> 45.4%), but defends worse than E. Per split: hard_dev +3.9, devzs +1.9, dev +1.0, taskbank -0.6. Confound: E trained on an H100 without micro-batches, H on the L4 with micro-batches, and the run-to-run spread of jagged ASR is unknown. Added a control, q35_2b_armE_L4 (E itself on the L4, same setup), queued after I. | | | | | | |
| X5 | Offline architecture tests (no GPU, existing predictions; `cascade_sim.py`) | Thresholds and weights chosen on dev-select, reported on dev-confirm (4,041 rows) | | | | | |
| – | Batch calibration: E +0.37 on confirm (+0.56 on select); H with batchcal vs E: +0.89 on confirm (+1.58 on select). Calibration-style add-ons are worth about +0.4-0.6 on the 2B. | | | | | | |
| – | **Cascade: 2B first, its least-sure questions go to our 4B** (v13t, chosen on dev-select). 2B v11r alone 76.24 -> route 40%: 80.15 (= 4B alone 80.13) -> route 50%: 80.35. Arm H alone 72.83 -> route 50%: 79.46. Blending 2B and 4B on the routed questions: 80.38-80.45 (+0.3 over the 4B), Brier slightly worse (0.116 vs 0.113). Ensembling 4B v11c and v13t: 80.08-80.33, no gain (the errors are correlated). **Conclusion:** at inference, architecture reaches the 4B's accuracy at about 2B cost, but not above it; going above needs better training (the planned fine-tuning round). | | | | | | |
| – | JevBench half A (public practice set; threshold taken from dev-select): cascade 2B v11r -> 4B v11c = **105/118** (34-44% routed) vs Jev 103/103 (two runs), 2B alone 101, 4B alone 107. Not significant (n = 118). | | | | | | |
| X6 | I = H + option-query head (trusted option definitions query the text), 164 min training | **+1.26 [+0.15, +2.41]** (73.84 vs 72.58); vs H +1.01 [+0.00, +2.05] | **-0.016** (vs H -0.006) | 5.9% | **0.8%** | 6.0% | jagged 20.4%, OPI 2.9%, redef 7.2% |
| – | RESULT gate I (at least +1.3 with the lower bound above 0): **missed by 0.04 pp**. The gain is significant (lower bound +0.15) but just under the fixed bar, so it is recorded as FAIL. The first clearly positive PRISM-X result: <br>- **accuracy** +1.26 vs E; <br>- **calibration** Brier -0.016 vs E; <br>- **injection** 0.8%, below Jev's 1.3%; <br>- **hijack** back to E's level (5.9%; H was 17.2%); <br>- **definition following** devp_card +2.7, largest where the option queries aim; also dev +2.5, negation words +3.4, devzs +1.6, dev_nc +1.3; dev_claims -3.4. <br>Reliance: with PRISM-X off, jagged is 20.4%. | | | | | | |
| X7 | **Control E_L4** = arm E re-trained on the L4 with micro-batches (the same setup as H-L), 800 steps | vs E (H100): -0.87 [-1.95, +0.20] confirm, +0.10 select | -0.003 | **19.2%** | 1.9% | 6.5% | – |
| – | **RESULT: the security loss in H was the hardware and training setup, not PRISM-X.** E itself, re-run on the L4, is hijacked 19.2% of the time (5.8% on the H100): the jagged ASR swings a lot between runs and setups. Against the matched control (same GPU, same setup): <br>- **H:** +1.11 [+0.02, +2.22] confirm (+0.95 select), Brier -0.007, jagged 17.2 vs 19.2. <br>- **I:** **+2.13 [+0.99, +3.28] confirm (+1.95 [+0.93, +3.00] select)**, Brier **-0.014**, **jagged 5.9% vs 19.2%**, OPI 0.8 vs 1.9%, redef 6.0 vs 6.5%. <br>**I passes the +1.3 bar with a lower bound above 0 against the matched control.** The gates were written against E (H100); the control was added after H's result and before I was scored, for the reason stated in the plan. Both comparisons are reported. | | | | | | |
| X8 | J = I + latent decision loop (1-4 steps, random depth in training), 164 min | vs E_L4 +1.44 [+0.37, +2.49] confirm (+1.00 select); **vs I -0.69 [-1.81, +0.38] confirm (-0.95 select)** | vs I +0.008 (worse) | 30.4% | 1.9% | 9.5% | jagged 64.9% |
| – | RESULT gate J (better than I on hard_dev and breadth_dev, no dev-confirm loss): **FAIL**. hard_dev 67.3 vs I 63.5 (+3.8: the loop helps on hard items), but breadth 75.0 vs 76.4, dev-confirm -0.69 vs I, calibration worse, security worse. At 800 steps the loop costs more than it gives; I stays best. **Note on security:** jagged ASR swings a lot between runs (E 5.8, E_L4 19.2, H 17.2, I 5.9, J 30.4), so security claims need several seeds. | | | | | | |
| X9 | O1 = I + policy compiler (per-layer FiLM from the trusted-schema summary, unbounded, lr 3e-4); interrupted at step 204 by the VM stop and resumed exactly | vs E_L4 +0.25 [-0.95, +1.45] confirm; **vs I -1.88 [-3.02, -0.76] confirm (-2.02 select)** | vs I +0.012 (worse) | 35.5% | 1.2% | 4.9% | jagged 69.4% |
| – | RESULT gate O1: **FAIL**. The compiler map grew to norm 13; the unbounded FiLM on every text token at every layer disrupts reading (it loses I's gains; security worse). Retry as O1b (fixed before its run): the same compiler with the scale and shift capped at +-0.1 (bound x tanh) and lr 1e-4. | | | | | | |
| X10 | KI = I + per-question confidence temperature | vs I -0.27 [-1.35, +0.81] confirm (-1.10 select); vs E_L4 +1.86 [+0.69, +3.02] | vs I +0.004 (worse) | **4.4%** | **0.4%** | 6.0% | – |
| – | RESULT gate KI (Brier at least 0.003 better than I): **FAIL**. The learned temperature rose to about 2.1 (it softened every answer), and yes/no Brier on dev-confirm was 0.1632 vs I 0.1592 (E_L4 0.1729); top-1 ECE 0.043 vs I 0.046. Best security so far, but within the run-to-run spread. I stays best. Google spend since 27 Sep: $20.09 (kill-switch log, 29 Sep 00:38 UTC). | | | | | | |
| X11 | Offline, free (`offline_calib.py`, dev-select fit -> dev-confirm) | Ensembles of PRISM-X runs: I+KI+J 74.04 acc (+0.2 vs I), Brier worse (0.1611). **Post-hoc temperature on I:** yes/no T = 0.65, choice T = 0.95 -> Brier 0.1592 -> **0.1530**, top-1 ECE 0.046 -> **0.009**; per-source T -> Brier 0.1493, ECE 0.014. | | | | | |
| – | FINDING: the model is **under-confident on yes/no** (the best T is below 1). Label smoothing (eps 0.05) and the soft teacher targets train it to hedge. KI's learned temperature went the wrong way (T 2.1). Fix: post-hoc per-type temperature (free) and less target softening on yes/no rows (a training change). | | | | | | |
| X12 | **Where Jev beats us (maths, free)** | OHS-2 yes/no rows (analysis of an already-used exam; OHS-3 stays the only clean final test): **Jev 96.1% acc, Brier 0.037, REL 0.0071; our 4B 88.6%, Brier 0.083, REL 0.0041**. Jev's Brier lead is all resolution, i.e. yes/no accuracy (our REL is *better*). Choice rows: **ours 76.7 vs Jev 76.6 (tie)**. Yes/no by source: moral stories 85.0 vs 97.5, tabfact 84.2 vs 93.3, argument stance 96.7 vs 97.5. On dev-confirm, PRISM-X I's gain is almost all yes/no: 77.2 vs control 73.4 (+3.8); choice 70.0 vs 69.7. Blend50 4B teacher: best T yes/no 0.9, choice 1.0 (near calibrated). | | | | | |
| – | CONCLUSION: the whole accuracy and Brier gap to Jev is yes/no reasoning (moral norms, tables, evidence). Priorities: (1) PRISM-X I on the 4B; (2) sharper targets (label smoothing 0); (3) yes/no reasoning data in the 500K set; (4) the 1,600-step persistence test. | | | | | | |
| X13 | L = I + counterfactual evidence (a no-text prior pass; learned subtraction alpha reached 0.32) | **vs I -2.03 [-3.13, -0.95] confirm (-1.39 select)**; vs E_L4 +0.10 | vs I +0.013 (worse) | 30.9% | 1.3% | 8.5% | – |
| – | RESULT gate L: **FAIL**. Every addition on top of I has now lost to I (J, O1, KI, L). **I is the design to freeze** (layout E + authority signal + shadow memory + option-query head), with post-hoc per-type temperature at inference. Caveat: I was the best of several arms, so its true gain may be smaller than the +2.1 measured; the 1,600-step run of I doubles as a replication. | | | | | | |

## Golden dataset v14 (29 Sep 2026; CPU only, built by Claude agents; no model labels)
| # | Step | Result |
|---|---|---|
| D1 | Round 1: 10 public-source families + 5 exact-label generators, each built then strictly reviewed (30 agents, about 3 h). The spec is in `golden_src/GOLDEN_SPEC.md`: permissive licences, human labels, train splits, OHS/eval/label-NLI exclusions. | 397,713 accepted raw rows, 72 datasets (47 fixed by reviewers, 5 rejected: sharc, social_i_qa, mhs_hate, eurlex_domain, megaacceptability) |
| D2 | Assembled (`build_v14_golden.py`): 12-gram decontamination vs all exams and evals, exact dedup, near-miss yes/no bundles, attack twins (inv), definition-swap twins, fact-flip twins, clean v13 replay | 426,403 train + 15,453 dev, 173 sources, 105,923 soft-label rows; 161 rows dropped for held-out overlap, 1,025 duplicates; yes/no share 81%, too high |
| D3 | Round 2 launched: choice-heavy (MCQ exams, relations and entities, ordinal scales, large label sets, routing, plus 3 generators), about 126K rows | pending; the final selection targets 500K at a 62% yes/no share |
| D3 | Round 2 (choice-heavy): 5 families + 3 generators, 16 agents | 116,223 accepted rows, 30 datasets (aqua_rat and elife_assessment rejected) |
| D4 | **Final assembly** (`build_v14_golden.py --target 500000`): yes/no share band 62% target, priority families (moral norms, tables and fact checks, science claims, generators) kept in full, replay source judge_ifcheck dropped after the audit | **500,000 train + 22,503 dev rows, 200 sources, yes/no share 64.6%, 88,228 annotator soft-label rows, 77K+ relations. 0 exact and 0 13-gram overlaps with OHS-3.** |
| D5 | **Label audit:** 442 stratified random rows (2-3 per source), 4 independent auditors | 91.0% correct, 6.3% ambiguous (partly from the audit's 2,500-character cut), 2.7% wrong. New golden sources about 1.5% wrong; legacy replay about 6%. judge_ifcheck removed. |
| – | NEXT: 4B soft teacher labels for the new rows (GPU), then the main 4B + PRISM-X training (1 full pass). Card: `data/v14_parts/GOLDEN_CARD.md`. | |
| X14 | **4B-E control**: q35_4b_v13t + layout E + 800 steps on train_prism_arms (kd 0.5, lr 4e-5, L4) | **vs v13t +1.36 [+0.25, +2.45] confirm (81.49 vs 80.13)**; select +0.27 | confirm -0.005 | – | 1.0% | – | – |
| – | yes/no 85.8 vs 84.1, choice 76.6 vs 75.6. The new best 4B on dev-confirm; the PRISM layout works on the 4B. 4B-I (+ PRISM-X I) is running. | | | | | | |
| D6 | **Targeted audit of the priority families:** 450 rows (150 each), full texts, 5 auditors | moral norms 94.0% correct / 1.3% wrong / 4.7% ambiguous; science claims 92.0 / 0.7 / 7.3; tables and fact checks 96.7 / 2.0 / 1.3; **overall 94.2% correct, 1.3% wrong** |
| – | Systematic bug found and fixed in `gen_msn_consent`: with "share it with a friend" permission, the friend passing it on further, or hosting three friends, was wrongly counted as covered. Rule fixed, 5,000 rows regenerated (self-check passes), dataset re-assembled: 500,000 train / 22,507 dev. | |
| X15 | **4B-I**: q35_4b_v13t + layout E + PRISM-X I, 800 steps (the same recipe as 4B-E) | vs 4B-E: **+0.59 [-0.10, +1.25] select, -0.59 [-1.21, +0.02] confirm, so about 0** | about 0 | 0.0% (E 0.6%) | 1.5% (E 1.0%) | **10.2% (E 16.5%)** | jagged 0.0%, OPI 1.5% |
| – | RESULT gate 4B-I: **FAIL**, no accuracy gain on the 4B (yes/no 85.4 vs 85.8, choice 75.7 vs 76.6). It helps definition-overwrite resistance only. The strong 4B already follows definitions; the option-query head adds little. **DECISION:** final 4B = layout E without PRISM-X (4B-E: 81.49 confirm, the best 4B); final 2B = PRISM-X I (+2.1 on the 2B); serving = cascade (2B+PX first, 4B for unsure questions). Main training: 4B, layout E, on the 500K golden set. | | | | | | |
| D7 | **Gap-fill vs the JevBench task families.** An audit of the 500K found gaps in very long policies (8-16K chars), probability/likelihood (calibration), JSON-record states and enum field extraction with traps, and tool selection with traps. 4 exact-label generators, each reviewed by hand (probability 236 checked / 0 label errors; long policy 49 / 0 label errors, 7 wording fixes; JSON and fields 36 / 0; tools 70 / 0). | +1,900 raw rows -> **+1,732 train rows added on top: 501,732 train / 22,587 dev, 204 sources**. Verified: every one of the previous 500K rows is present and unchanged. The probability rows carry the exact probability as the soft target. |
| X16 | I_LS0 = I with label_smooth 0 and teacher T yes/no 0.9 (same seed as I) | **vs I -1.29 [-2.42, -0.18] confirm (-0.95 select)** | vs I +0.012 (worse) | 5.8% | 0.8% | – | – |
| – | RESULT gate I_LS0: **FAIL**. The fitted yes/no T is still 0.65, so label smoothing was not the cause of the under-confidence. Keep label smoothing 0.05 in the main run and use post-hoc per-type temperature. This is also a second, lower run of I's architecture (72.56 vs 73.84), a hint that I's +2.1 includes some luck; the 1,600-step pair (I_1600 vs E_L4_1600) is the decisive replication. | | | | | | |
| X17 | I_1600 = PRISM-X I, 1,600 steps (2x I; resumed once after the VM auto-stop at step 586) | **interim** vs E_L4 (800 steps) +3.46 [+2.08, +4.83] confirm; vs I (800) +1.34 [+0.07, +2.55]. The matched test vs E_L4_1600 is pending | vs E_L4 -0.0225; vs I -0.0088 | **1.1%** (E 5.8%) | 4.4% (E 2.3%, CI crosses 0) | 3.3% (E 2.8%) | off: jagged 2.6%, OPI 3.8% |
| – | Longer training helps I (+1.3 over 800 steps) and keeps hijack resistance (1.1%). Per split: hard_dev 69.2 vs E 62.0, pg_dev 54.6 vs 51.5, dev_nc 69.7 vs 68.9. The decision waits for E_L4_1600 (same steps, same GPU). | | | | | | |
| X18 | **Matched pair: I_1600 vs E_L4_1600** (both 1,600 steps, same L4 setup; the decisive replication) | **dev-confirm −0.27 [−1.34, +0.79]** (75.18 vs 75.45); dev-select +0.85 [−0.15, +1.87] | confirm +0.0030 (worse) | **1.1% vs 10.0%: −8.9 pp [−5.7, −12.0]** | 4.4% vs 2.1% (+1.3 [−0.7, +3.6], n.s.) | 3.3% vs 2.8% | – |
| – | RESULT (pre-registered at 06:30 UTC, before scoring): (a) accuracy gate +1.3 **FAIL**; (b) non-inferiority needs a lower bound > −0.75 and got −1.34, so **FAIL** (the security part passes clearly: jagged −8.9 pp, lower bound +5.7; OPI increase not significant). **By the rule, the final 2B = layout E without PRISM-X.** PRISM-X I's accuracy gain did NOT replicate: with 1,600 steps the plain model caught up (75.45 vs 75.18). What remains is a large, significant hijack-resistance gain (10.0% → 1.1%). Trade-offs for the owner: PRISM-X also disables CUDA graphs in cand_logits, so the 2B is slower. Layout E alone is still far more secure than Jev (~100% on jagged). | | | | | | |
| X19 | **4B-E "read twice" (TTA)**: the same model on the 9 gate splits, two views averaged (choice: reversed options; yes/no: letters swapped), vs the stored single read | confirm −0.07 [−0.53, +0.39]; select +0.00 [−0.42, +0.43]. yes/no −0.32 confirm / −0.09 select; choice +0.21 / +0.10 | +0.0004 (not better) | – | – | – | – |
| – | RESULT (pre-registered gate: ≥ +0.3 accuracy or ≥ +0.5 on yes/no, Brier not worse): **FAIL, no TTA at serving.** The 4B's yes/no errors are not letter-position bias, so the yes/no gap to Jev is knowledge/reasoning and has to be closed by training. Caveat: the single read comes from the in-training prediction path; the plan's same-job comparison would be cleaner, but the difference is well inside noise either way. | | | | | | |
| – | **OWNER DECISION (30 Sep, 12:30 UTC): the final 2B = PRISM-X I (frozen)**, for security (1.1% vs 10.0% jagged hijack, accuracy tied). This overrides the accuracy-only rule in X18. | | | | | | |
| D8 | **Pre-4B label audit** (critic gap 8): 4B-E labelled a 15,590-row stratified sample on the L4 (75 min, Google credit); flag screen; 12 outlier groups audited by agents (374 rows + builder code + raw data) | **0 systematic pipeline bugs**; about 4% single-row annotator errors (kept, per the rules); high flag rates explained by subjective or noisy tasks and model leniency. The golden set stays frozen. |
| P1 | **Pilot step 1: heavy-batch memory smoke** (H100!, jaypatil-duke; frozen 4B config; 20 real steps plus the heaviest real micro-batches) | micro_tokens 10240: **PASS** (35% memory, 4.26 s/step); 16384: PASS (52%, 5.12 s/step); 24576: PASS (67%, 5.71 s/step); **0 (no packing): OOM** on the heaviest batch (118K tokens). Trainable params 32,464,896 as expected; all startup checks passed. Billed **$2.36**. |
| – | Speed note: smaller micro-batches are FASTER (less padding). At 4.26 s/step a full pass costs about $172 (x1.21), over the $135 cap, so the speed step must test smaller micro_tokens (e.g. 6144/8192) and causal-conv1d before deciding (plan 2.4, decision 4). | |
| P2 | **Pilot step 2: speed** (H100!, jaypatil-duke, 100 real packed steps of the frozen config) | grad_ckpt ON: **8192 = 2.77 s/step (full pass about $113 at x1.21)**, 10240 = 2.91 s/step (about $121); memory about 22-23%. grad_ckpt OFF: OOM at both 8192 and 10240 (99% memory), so ruled out. The smoke's 4.26 s/step was inflated by heavy-only batches. **A full 4B pass fits under the $135 cap.** Data-stream note: the GPU last_batch at step 100 (a47518dc…) differs from the CPU replay (a2792225…) but is identical across the two GPU runs. Likely model load consumes Python `random`; the relay test checks determinism. |
| P3 | **Pilot step 3: relay proof** (frozen config at micro_tokens 10240; A1 = 300 straight on jaypatil-duke; A2 = 300 straight on arya-mahadik-ai; B = 150 on aryamhd -> checkpoint moved -> 150 on jaypatil-duke) | **PASS.** B resumed at exactly 150 with "manifest, config, data, env, code, tensors, optimizer order, data order: all match". Weight distance d(A1,B) 0.00991 vs d(A1,A2) 0.01046 (B is closer to A1 than a second straight run is); loss g(A1,B) 0.0121 vs g(A1,A2) 0.0132; all exact checks pass; A1 and A2 used the identical data stream (same last-batch hash at step 300) on different accounts; the loss fell from 0.977 to 0.720. The first download of A1's trainable.safetensors was corrupted in transit; the manifest check caught it, and a re-download matched. |
| – | **PILOT RESULT: all pass.** Memory: 8192 / 10240 / 16384 / 24576 fit (8192 at 36% on the heaviest batches); no packing OOMs; grad_ckpt off OOMs. Speed: **8192 = 2.77 s/step, full 4B pass about $113**. The relay is proven on the real GPU. **Final config micro_tokens = 8192.** Pilot billed about $8 so far (about $10-11 expected once the last hour posts). | |

## 4B ship gate, job 1 (1 Oct 2026, 17:58-21:12 UTC, Google L4 od-l4 us-central1-a; about 3.3 L4-hours, Google credit)
| Look | Result |
|---|---|
| refparity1 | **PASS**: q35_4b_pxE_fresh vs stored q35_4b_pxE_parity: agree 100.00%, mean/max \|dp\| 0.0000, accuracy 80.72 vs 80.72 |
| c3trigger | no trigger (C1 passes (b), (c), (d), (g) on dev-select) |
| replacement | C2 (snapshot cat average) vs C1: dev-select +0.20 pp, confirm +0.05 → does not replace; chosen C1 = q35_4b_main500k |
| **ship1** | **DO NOT SHIP (FINAL)**. Primary (unseen sources, n=3,847): 83.99 vs 81.52, **+2.47 pp [+1.31, +3.70] PASS**. (a) +1.19 [+0.17, +2.23] PASS; (a2) select +1.83 / confirm +0.54 PASS; (b) yes/no +1.40 PASS; (c) choice +0.94 PASS; (d) Brier 0.1099 vs 0.1184 PASS; **(e) equivalence flip rate 8.86% vs 5.68% (limit REF + 2 pp) FAIL**; (f) permutation flips 2.43% vs 3.78% PASS; (g) jagged 0.0% vs 0.6% PASS, OPI 1.3% vs 1.8% PASS |
| Outcome | FALLBACK: 4B-E (q35_4b_pxE) stays the shipped 4B (PREREG 5.7). Teacher rule (b) fails, so the teacher stays 4B-E and the memorisation read was skipped |
- **Where the (e) failure comes from** (analysis after the look; it cannot change the verdict):
  - all of it is devp_card's 372 double-negation equivalence pairs, e.g. "Can we conclude X?" vs "Should the statement
    that not-X be rejected?": new model 12.1% flips vs 4.8%;
  - devzs and dev equivalence flips are equal or better.

| B1a | 5 Oct 2026, Modal aryamhd, H100: bf16_nospec (383 s + 81 s engine start) OK; bf16_dflash container died ("Server has lost track of input", Modal internal) | ~$0.6 [E]; re-run of bf16_dflash launched (cap $5) |
| B1a retries | 5 Oct, aryamhd H100. bf16_dflash failed 3x at init: SGLang 0.5.20 DFlash KV-pool accounting bug on Qwen3.5, "draft weights are now counted" (mem 0.55 and 0.85). nospec re-run (412 s) OK. Fast path failed: C1 final files were missing on aryamhd /vol; uploaded from the Mac backup (sha 507d1c29); re-run launched | ~$1.5 [E] cumulative for B1a so far |
| B1a fast path | 5 Oct, aryamhd H100, bf16_nospec + C1 fast path (794 s). Two OOM attempts before it (SGLang at 55% plus 160 CUDA graphs at 46 GB); fixed with mem 0.25 and graphs at (1, 8) up to 1,536 tokens | ~$1.0 [E]; B1a total ≈ $3 |
| B1a ACTUAL (billing, 5 Oct 23:00 UTC) | `modal billing report` on aryamhd, hourly: opendecide-think 02:00-05:00 EDT on 5 Oct = $0.19 + $3.55 + $1.84 = **$5.57** (7 app runs). The ~$3 estimate above was low. Nothing has run on any of the 7 profiles since then | **$5.57 [A]** |
| Card charge | aryamhd October: metered $32.12 (1 Oct `opendecide` run $26.31 + B1a $5.57 + volumes $0.24, free), $30.00 monthly credit used up → **$1.88 billed to the card**. From now on every aryamhd run is paid in full | $1.88 real |
| rrun running total | mahadikarya44 CPU (app od-rrun, A20 a), updated 7 Oct 01:01 UTC: 29 runs in c_build/rrun_ledger.jsonl est $11.12 + 0 open reservations $0.00; modal billing report $9.51 this month; hard CPU/mem limits = request; auto-stop $15. Running total, rewritten in place on every run (the milestone rows are not additive) | ~$11.12 [E] |                                                  
| A20 rrun (to 6 Oct 01:40 UTC) | Modal CPU runner on jaypatil-duke: adoption tests + first lane jobs. Billing: $1.68 of the monthly credit used, $0 billed. Self-stop at $15 | $1.68 credit |
| A20 c parity | 6 Oct 01:31-01:35 UTC, jaypatil-duke (credit): DDP parity, 1×H100 (A, B) vs 4×H100 (C), 50 steps. Verdict **FAIL** under the pre-set rule. Loss: max 6.7% > 5% gross bar, but the 1-GPU noise arm B itself shows 10.3%. Tiny aux terms: cons max rel 9.3 vs B 3.3; perm 1.37 vs 0.79. Mean loss deviation C 0.0198 vs B 0.0200. Weights C 0.0178 vs B 0.0168 (pass). s/step: A 2.75, B 3.05, C 1.08 (2.56x, efficiency 0.64). Projected round 1: 1×H100 6.8 h $27.8; 4×H100 2.7 h **$43.5** (> $35 hard stop) | $1.14 credit |
| rrun milestone $5 | 6 Oct 02:51 UTC: jaypatil-duke od-rrun spend passed $5 (~$5.03 at 68 runs); auto-stop at $15 | marker only: amount is in the rrun running total row |
| rrun milestone $10 | 6 Oct 03:51 UTC: jaypatil-duke od-rrun spend passed $10 (~$11.05 at 84 runs); auto-stop at $15 | marker only: amount is in the rrun running total row |
| Owner decision 6 Oct ~04:50 UTC | Free credit first, then aryamhd card. Crowd on atmosphor credit; pre-reads, pre-smoke and final tests on jaypatil-duke credit; round 1 (~$30) on aryamhd card. Round 1 auto-starts when ready | — |
| Billing snapshot 6 Oct 05:15 UTC | `modal billing summary --for "this month"`: atmosphor metered $17.01, credit used $14.78 → **$15.22 credit left**; jaypatil-duke metered $20.01, credit used $19.82 → **$10.18 left** (rrun still running 2 jobs, ~$8.3 after it self-stops at $15) — already **below the owner's $12 final-test reserve**; aryamhd metered $32.12, card billed $1.88 (every new aryamhd run is card) | — |
| Endgame prep, volume copies (6 Oct 05:15-05:22 UTC) | free Volume get/put only, no compute: `q35_4b_main500k_init` jaypatil-duke → **aryamhd**; `q35_4b_pxE` aryamhd → **atmosphor**; `q35_4b_base0` (make-base0, A18.2 form, local CPU) → **atmosphor + aryamhd**. Read-back sha256 all match (init/C1 507d1c29…, pxE 1bbd8a79…, base0 d92d259f…): `c_build/endgame/COPY_RECORD.json` | $0 |
| C1 pre-reads (A21 d) + pipeline pre-smoke (A20 d): NOT RUN (6 Oct 05:25 UTC) | jaypatil-duke is below the $12 reserve (any spend breaks the owner guard); the aryamhd-card launch (cap $2.90) was refused by the permission system (card spend needs the owner). Tools + inputs ready: `c_build/endgame/RUNBOOK.md` P1/P2 (P2-L4 on Google credit recommended) | $0 |
| Crowd budget check (6 Oct 05:35 UTC) | ~80K candidate rows over 13 families + COMMIT ≈ 240K reads ≈ $25-31 at the assumed 10.4 reads/s/H100 vs atmosphor $15.22: about half will not fit; `crowd_cap.py` REFUSES even F1-F8 (needs 76.5 min/container, credit pays 72). Owner: spill to aryamhd card or wait; measure the real rate on the first launch | — |
| Billing re-check + discrepancy (6 Oct 05:42-05:48 UTC) | free billing/app-list calls only. jaypatil-duke: 05:42 metered $16.83, credit left **$13.36**; 05:48 metered $17.41, credit left **$12.78** (falling: rrun `od-rrun` still running, 1 task). This does NOT match the 05:15 line above (metered $20.01, $10.18 left); the newer reads are used. atmosphor 05:42: metered $17.01, credit left $15.22 (unchanged). aryamhd 05:42: metered $32.12, billed (card) $1.88, credit 0. P1 pre-smoke NOT run: `spend_guard.py check jaypatil-duke --cap-usd 1 --reserve 12` REFUSED (unexplained running app rrun; $12.78 − $12 = $0.78 < $1 cap). Owner guard at risk: rrun stops itself at $15 of rrun spend, not at the $12 reserve (RUNBOOK B7) | $0 |
| rrun switch 6 Oct ~05:30 UTC | jaypatil-duke od-rrun ≈ $18 of credit (billing ~$19.7 total incl. parity $1.14), $0 billed; ~$12.8 credit left, reserved for the final tests. rrun now rotates mahadikarya2/3/44 credit, $12 cap each, default 8 cores | — |
| crowd F3,F6: BEFORE launch (cap 39 min x 3 H100) | 06 Oct 12:12 UTC, atmosphor | metered $17.01, billed $0.00, credit left $15.22 | credit |
| crowd F9: BEFORE launch (cap 18 min x 3 H100) | 06 Oct 12:42 UTC, atmosphor | metered $17.02, billed $0.00, credit left $15.21 | credit |
| crowd F3,F6: BEFORE launch (cap 31 min x 3 H100) | 06 Oct 13:45 UTC, atmosphor | metered $17.48, billed $0.00, credit left $15.19 | credit |
| crowd F9: BEFORE launch (cap 17 min x 3 H100) | 06 Oct 14:11 UTC, atmosphor | metered $20.95, billed $0.00, credit left $11.72 | credit |
| crowd F5: BEFORE launch (cap 17 min x 3 H100) | 06 Oct 16:57 UTC, atmosphor | metered $22.38, billed $0.00, credit left $10.29 | credit |
| crowd F5: AFTER | 06 Oct 17:03 UTC, atmosphor | metered $23.04, billed $0.00, credit left $9.63 | credit |
| P1 pre-smoke (A20 d): BEFORE (cap 14 min, <= $0.95) | 06 Oct 17:31 UTC, jaypatil-duke | metered $17.17, billed $0.00, credit left $13.07 | credit |
| P1 pre-smoke (A20 d): AFTER (client exit 0) | 06 Oct 17:36 UTC, jaypatil-duke | metered $17.17, billed $0.00, credit left $13.07 | credit |
| crowd F4: BEFORE launch (cap 11 min x 3 H100) | 06 Oct 19:36 UTC, atmosphor | metered $23.68, billed $0.00, credit left $8.99 | credit |
| crowd F4: AFTER | 06 Oct 19:42 UTC, atmosphor | metered $25.19, billed $0.00, credit left $7.48 | credit |
| crowd F11: BEFORE launch (cap 11 min x 3 H100) | 07 Oct 00:35 UTC, atmosphor | metered $25.21, billed $0.00, credit left $7.46 | credit |
| crowd F11: AFTER | 07 Oct 00:47 UTC, atmosphor | metered $27.86, billed $0.00, credit left $4.81 | credit |
| crowd F11: BEFORE launch (cap 7 min x 3 H100) | 07 Oct 00:48 UTC, atmosphor | metered $27.86, billed $0.00, credit left $4.81 | credit |
| crowd F11: AFTER | 07 Oct 00:56 UTC, atmosphor | metered $30.12, billed $0.00, credit left $2.55 | credit |
| crowd F11: BEFORE launch (cap 27 min x 3 H100) | 07 Oct 01:27 UTC, mahadikarya44 | metered $12.94, billed $0.00, credit left $17.42 | credit |
| crowd F11: AFTER | 07 Oct 01:39 UTC, mahadikarya44 | metered $13.59, billed $0.00, credit left $16.77 | credit |
| crowd F7: BEFORE launch (cap 23 min x 3 H100) | 07 Oct 04:56 UTC, mahadikarya44 | metered $12.91, billed $0.00, credit left $17.45 | credit |
| crowd F7: AFTER | 07 Oct 05:01 UTC, mahadikarya44 | metered $13.93, billed $0.00, credit left $16.43 | credit |
| crowd F5: BEFORE launch (cap 26 min x 3 H100) | 07 Oct 05:50 UTC, mahadikarya44 | metered $14.32, billed $0.00, credit left $16.04 | credit |
| crowd F5 (A32 regen): AFTER | 07 Oct 05:50 UTC, mahadikarya44 | metered $14.32, billed $0.00, credit left $16.04 | credit |
| crowd F6: BEFORE launch (cap 26 min x 3 H100) | 07 Oct 06:39 UTC, mahadikarya44 | metered $15.28, billed $0.00, credit left $15.08 | credit |
| crowd F6 (A32 regen): AFTER | 07 Oct 06:39 UTC, mahadikarya44 | metered $15.28, billed $0.00, credit left $15.08 | credit |
| crowd F5 (A32 regen): AFTER (refetch) | 07 Oct 06:40 UTC, mahadikarya44 | metered $15.28, billed $0.00, credit left $15.08 | credit |
| crowd F6 (A32 regen): AFTER (refetch) | 07 Oct 06:45 UTC, mahadikarya44 | metered $16.83, billed $0.00, credit left $13.53 | credit |
| crowd F5: BEFORE launch (cap 26 min x 3 H100) | 08 Oct 05:32 UTC, mahadikarya44 | metered $15.52, billed $0.00, credit left $14.90 | credit |
| crowd F5 (wording rebuild): AFTER | 08 Oct 05:38 UTC, mahadikarya44 | metered $17.02, billed $0.00, credit left $13.40 | credit |
| crowd F9: BEFORE launch (cap 28 min x 3 H100) | 08 Oct 05:44 UTC, mahadikarya44 | metered $16.86, billed $0.00, credit left $13.56 | credit |
| crowd F9 (wording rebuild): AFTER | 08 Oct 05:53 UTC, mahadikarya44 | metered $19.26, billed $0.00, credit left $11.16 | credit |
| crowd F3 (wording rebuild): AFTER | 08 Oct 06:36 UTC, mahadikarya44 | metered $21.46, billed $0.00, credit left $8.96 | credit |
| crowd F4: BEFORE launch (cap 27 min x 3 H100) | 08 Oct 07:25 UTC, mahadikarya44 | metered $18.39, billed $0.00, credit left $12.03 | credit |
| crowd F4 (wording rebuild): AFTER | 08 Oct 07:31 UTC, mahadikarya44 | metered $19.93, billed $0.00, credit left $10.49 | credit |
| crowd F4 (wording rebuild): AFTER | 08 Oct 07:31 UTC, mahadikarya44 | metered $19.93, billed $0.00, credit left $10.49 | credit |
| crowd F3: BEFORE launch (cap 34 min x 3 H100) | 08 Oct 08:53 UTC, mahadikarya44 | metered $19.63, billed $0.00, credit left $10.79 | credit |
| crowd F3 (wording rebuild): AFTER | 08 Oct 09:03 UTC, mahadikarya44 | metered $21.07, billed $0.00, credit left $9.35 | credit |
| round 1 (C r1): D2 seg1 0-100: BEFORE (cap 30 min) | 09 Oct 19:53 UTC, aryamhd | metered $32.34, billed $1.88, credit left $0.00 | card |
| round 1 (C r1): D2 seg1: AFTER | 09 Oct 20:02 UTC, aryamhd | metered $32.99, billed $2.53, credit left $0.00 | card |
| round 1 (C r1): D4 seg2 100-300: AFTER | 09 Oct 20:15 UTC, aryamhd | metered $34.20, billed $3.74, credit left $0.00 | card |
| round 1 (C r1): D5 seg3 to the end: BEFORE (cap 540 min) | 09 Oct 20:16 UTC, aryamhd | metered $34.20, billed $3.74, credit left $0.00 | card |
| round 1 (C r1): D5 seg3: AFTER | 09 Oct 21:44 UTC, aryamhd | metered $40.71, billed $10.25, credit left $0.00 | card |
| OHS-3 C1 scored/timed pass: BEFORE (owner GO; Modal cap $9) | 10 Oct 15:41 UTC, jaypatil-duke | metered $18.61, billed $0.00, credit left $11.79 | credit |
| OHS-3 C1 scored/timed pass: AFTER | 10 Oct 18:00 UTC, jaypatil-duke | metered $21.43, billed $0.00, credit left $8.97 | credit |
| C2 training: seg1 0-100: BEFORE (cap 30 min) | 18 Oct 06:45 UTC, mahadikarya2 | metered $18.18, billed $0.00, credit left $19.10 | free credit |
| C2 training: STOPPED: seg1 client exit 1 (see c2_build/train/logs/c2_seg1.log) | 18 Oct 07:03 UTC, mahadikarya2 | metered $18.18, billed $0.00, credit left $19.10 | free credit |
| C2 training: seg1 0-100: BEFORE (cap 30 min) | 18 Oct 07:03 UTC, mahadikarya2 | metered $18.18, billed $0.00, credit left $19.10 | free credit |
| C2 training: seg1: AFTER | 18 Oct 07:13 UTC, mahadikarya2 | metered $19.04, billed $0.00, credit left $18.26 | free credit |
| C2 training: STOPPED: first100 ABORT (A37 k: non-finite loss, or the chain guards); owner review | 18 Oct 07:13 UTC, mahadikarya2 | metered $19.04, billed $0.00, credit left $18.26 | free credit |
| C2 training: seg2 100-300: AFTER | 18 Oct 07:33 UTC, mahadikarya2 | metered $19.72, billed $0.00, credit left $17.58 | free credit |
| C2 training: seg3_mahadikarya2 to the end/cap: BEFORE (cap 221 min, limited by credit) | 18 Oct 07:34 UTC, mahadikarya2 | metered $19.79, billed $0.00, credit left $17.51 | free credit |
| C2 training: seg3_mahadikarya2: AFTER (client exit 0) | 18 Oct 10:24 UTC, mahadikarya2 | metered $31.33, billed $0.00, credit left $5.97 | free credit |
| C2 training: C2 FINAL | 18 Oct 10:24 UTC, mahadikarya2 | metered $31.33, billed $0.00, credit left $5.97 | free credit |
