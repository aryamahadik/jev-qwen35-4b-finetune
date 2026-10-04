# R_tokens: making think mode fast by thinking fewer tokens

Date: 4 Oct 2026. Scope: fewer thinking tokens, or no visible thinking, for a 4B model.
Rules followed: only the same 4B as teacher, no Jev outputs, no paid calls, no sealed or test data opened.
Faster kernels and speculative decoding are covered by the other reports. This one is only about the number of tokens.

## 0. TL;DR (plain words)

1. **The real problem is token count, not the model.** In the DEER paper's tables, Qwen3-4B in thinking mode writes **2,175 tokens on GSM8K and 9,294 on GPQA-D**. At the measured batch-1 speed of a 4B (**133 tok/s in BF16, 201 tok/s in FP8**, SGLang on an H20), that is **11-16 s for GSM8K** and **46-70 s for GPQA**. To finish in under 1 s we need about **150-200 tokens or fewer**. A "few seconds" allows about **500-1,000 tokens**.
2. **Under 1 s on math is only realistic with short explicit CoT (about 40-150 tokens), not with a "thinking" trace.** On Qwen3-4B, short CoT SFT reaches **82.2% at 85 tokens** on GSM8k-AugNL, and the best latent method reaches **75.3% at 38 tokens**. With no CoT the score is **38.4%**.
3. **The cheapest big win is routing.** Answer easy items with no thinking and think only on hard ones. In the papers, **13-23% of GSM8K items** still go to thinking (Thinkless, AdaptThink), and average tokens drop 50-70% with equal or better accuracy. A training-free router (DART) cuts wall time from **67.6 s to 29.5 s** on Qwen3-8B. Caution: **at 4B, DART loses 5 points on MATH-500.**
4. **Early exit is free and works on GPQA.** DEER on **Qwen3-4B cuts GPQA-D from 9,294 to 3,275 tokens (-65%), and accuracy goes from 46.5 to 47.5**. On GSM8K it goes from 2,175 to 1,250 tokens (-43%) with accuracy 94.1 → 94.5. It needs no training, has MIT code and runs on vLLM.
5. **Concise self-distillation from the same model fits our rules and our budget.** Sample the 4B several times, keep the shortest correct answer, and fine-tune on it. Reported results:
   - **-26% tokens at 99.5% relative accuracy** with self-only data (Munkhbat).
   - **-57 to -64% tokens with +6 to +9 points** on MATH-500 for 8B on-policy variants (OPSDC, BIRD).
6. **Latent or implicit CoT (Coconut, CODI, KaVa, SIM-CoT) is not ready for us.** It only works on GSM8K-style arithmetic and stays **7-10 points below short explicit CoT** at 3-8B. There is no evidence for GPQA. Distilling CoT straight into a direct answer **failed** on GSM8K (7.1% vs 52.8%).
7. **Parallel beats sequential for latency at batch 1.** A 4B at batch 1 is limited by memory bandwidth, so 4-8 parallel samples cost little extra wall time. Reported results:
   - BAEE (parallel probes from early prefixes) on **Qwen3-8B-Think: +5 points with 63-76% lower latency.**
   - NoThinking + parallel: **up to 9x lower latency** than sequential thinking.
   - ParaThinker on 1.5B: 8 paths give **+12.3% accuracy for 7.1% extra latency.**
   - Self-parallel threading (ThreadWeaver): only 1.14-1.22x.

**Suggested stack (in order):**
1. Router first: the fast path or no-think answers easy items.
2. For items that do think: a hard thinking budget plus DEER-style early exit, with 4 parallel short samples and a vote.
3. Then one cheap concise self-distillation LoRA pilot (about $10-15).

RL length training (L1, ThinkPrune, AdaptThink) is stronger but costs about $300-1,000 or more. That is above the pilot budget.

## 1. Latency arithmetic (why tokens matter)

| Item | Source | Number |
|---|---|---|
| Qwen3-4B decode, batch 1, SGLang, H20 | [Qwen speed benchmark](https://qwen.readthedocs.io/en/latest/getting_started/speed_benchmark.html) | BF16 **133.1 tok/s**, FP8 **200.6 tok/s**, AWQ-INT4 199.7 tok/s (input length 1, 2,048 generated) |
| Same, HF transformers | same page | BF16 45.9 tok/s (this is the "no kernels" regime we are in today) |
| Qwen3-4B thinking tokens (vanilla) | [DEER Table 2/App.](https://arxiv.org/pdf/2504.15895) | GSM8K 2,175 · MATH-500 4,767 · AMC 7,443 · AIME24 11,916 · GPQA-D 9,294 |
| Qwen3.5-4B on GPQA-D with a Python tool | [kth8 dataset](https://huggingface.co/datasets/kth8/Qwen3.5-4B-GPQA-Diamond-benchmark) | about **4,589 completion tokens per question**, 69.2% (settings undocumented, so treat as a rough hint) |
| Qwen3.5-4B model card | [HF](https://huggingface.co/Qwen/Qwen3.5-4B) | GPQA-D 76.2; recommends a **32,768-token** output limit; thinking is turned off with `enable_thinking: False`; no /think soft switch; Apache-2.0 |

Rule of thumb (my estimate, using the H20 numbers above as a stand-in for H100): **1 s ≈ 130-200 tokens. 3 s ≈ 400-600 tokens.** Qwen3.5-4B speed on an H100 is **unknown**, because its Gated-DeltaNet hybrid has not been benchmarked here.

## 2. Length-controlled or concise reasoning

| Method | Model | Token change | Accuracy change | Training cost | Same-4B fit |
|---|---|---|---|---|---|
| **Budget forcing** (s1) [2501.19393](https://arxiv.org/abs/2501.19393) | Qwen2.5-32B, 1k SFT examples | hard cap; "Wait" extends | AIME24 50 → 57 when extended | SFT on 1k items | Fits (training-free at inference). **Weak when the budget is tight**: L1 beats it by **20-25 points absolute** at 512 and 1,024 tokens |
| Qwen built-in budget [Qwen3 report](https://arxiv.org/html/2505.09388v1) | Qwen3 | cap, then insert *"Considering the limited time by the user, I have to give the solution based on the thinking directly now.\n</think>.\n\n"* | smooth curve, e.g. 235B AIME'24 about 70 → 85 as the budget grows | none | Fits. Zero cost. Our baseline knob |
| **L1 / LCPO** [2503.04697](https://arxiv.org/html/2503.04697) | DeepScaleR-1.5B | user picks the budget; about 3% length error | L1-Max on MATH: **70.8 @512, 78.3 @1,024, 79.4 @2,048 tokens**; AIME 5.0 / 11.9 / 15.0 | RL, 700 + 120 steps (GPU hours not given) | Fits (own rollouts). Medium-to-high cost |
| **Elastic Reasoning** [2505.05315](https://arxiv.org/html/2505.05315) | 1.5B (E1-Math) | -30% overall; AIME -32.1% | MATH-500 83.6 at 1,619 tokens; AIME 41.0 → 35.0 | RL, **200 steps** (vs 700/820 for L1) | Fits. Cheapest RL option |
| **ThinkPrune** [2504.01296](https://arxiv.org/html/2504.01296) | R1-Distill-1.5B | avg **10,355 → 3,574 (-65%)** | AIME24 29.4 → 27.1 | RL with 4k → 3k → 2k caps, 2,470 prompts (GPU hours not given) | Fits |
| Length-penalty RL (Arora & Zanette) [2502.04463](https://arxiv.org/html/2502.04463) | R1-Distill-7B | GSM8K about -52% (α=0.05) to -83% (α=0.2) | about -0.7 to -1.7 points; MATH -27% tokens at about -2.5 points (values read approximately) | 100 RL steps, 3.2k prompts, **4-8 GH200 × about 20 h** (about $330-650 at our rate) | Fits. Above pilot budget |
| **TokenSkip** [2502.12067](https://arxiv.org/html/2502.12067) | Qwen2.5-7B-Inst | GSM8K **298 → 151 tokens** (γ=0.5) | 91.4 → 86.0 (γ=0.7: 217 tokens, 89.9) | LoRA r8, **about 2 h on 2×3090** | Fits. The pruner is LLMLingua-2, a small BERT-size scorer and not an LLM teacher. Built for short CoT; long thinking traces are untested |
| **Concise self-training** (Munkhbat) [2502.20122](https://arxiv.org/html/2502.20122) | 5 families, 1.5-7B | self-only FS-BoN: **length 73.8%** of baseline | **99.5% relative accuracy** (FS-Self: 83.0% length / 100.8% accuracy) | generating 16 paths took about 1.5 h; SFT **2 min 24 s on one H100** | **Fits best.** Use the self-only variants; the GPT-4o-exemplar variant is not allowed |
| **OPSDC** (on-policy self-distillation, concise prompt as teacher) [2603.05433](https://arxiv.org/html/2603.05433v4) | Qwen3-8B / 14B | MATH-500 **-58.8% / -56.5%** | MATH-500 **+8.9 / +16.1** points (their baselines are low, 77.7 / 70.0, likely because of a 30k cap or their protocol); AIME25 **-5.4** | about 100 steps, 13.6k problems, 8×H200 | Fits (the teacher is the same model with the instruction "Solve … concisely and correctly. Be direct…"). Hard math loses points |
| **BIRD** (bootstrapped self-distillation) [2607.15736](https://arxiv.org/abs/2607.15736) | Qwen3-8B | MATH-500 **3,099 → 1,115 tokens** | **86.2 → 92.0** | not stated | Fits |
| Short-chain SFT (s1-short) [2505.17813](https://arxiv.org/html/2505.17813) | 32B-class | -5.8% | +2.8% relative | SFT | Fits, but the gain is small |

**Accuracy vs token budget, small models:**
- Qwen3-4B no-think → think ([Qwen3 report](https://arxiv.org/html/2505.09388v1)): GPQA 41.7 → 55.9; MATH-500 84.8 → 97.0; AIME24 25.0 → 73.8.
- Qwen3-8B on GPQA ([Mid-Think](https://arxiv.org/pdf/2601.07036)): no-think 37.5, "NoThink+Okay" 47.3, think 60.9.
- **No published GPQA accuracy-vs-budget curve for a 4B model was found (unknown).**

## 3. Adaptive thinking (think only when needed)

| Method | Model | Result | Training | Same-4B fit |
|---|---|---|---|---|
| **AdaptThink** [2505.13417](https://arxiv.org/html/2505.13417) | R1-Distill 1.5B / 7B | GSM8K 1.5B: **978 → 480 tokens, 79.0 → 83.1, 86.9% answered without thinking**. 7B: 682 → 309 tokens, 87.9 → 91.0, 99.6% without thinking. MATH500 1.5B: 4,887 → 1,782, 80.6 → 82.0 | RL, 314 steps. **1.5B: 8×H800 × 32 h (about 256 GPU-h, about $1k)** | Fits (no outside teacher). Too expensive for a pilot |
| **Thinkless** [2505.13379](https://arxiv.org/html/2505.13379) | R1-Distill-1.5B | GSM8K **1,919 → 624 tokens, 83.5 → 84.2, think rate 13.3%**. MATH-500 5,675 → 2,555, 86.1 → 81.8 (-4.2). AIME: still thinks 100% | warm-up SFT + 600 RL steps on 4×H100 | Warm-up used **R1-671B**, which breaks our rule. Fix: Qwen3.5-4B already has think and no-think modes, so only the RL router part is needed |
| **AutoThink** [2505.10832](https://arxiv.org/html/2505.10832) | R1-Distill 1.5B / 7B, Qwen3-8B | 1.5B: **-52% tokens, accuracy 48.6 → 51.7**. 7B: -41% tokens with accuracy flat | 3-stage RL, about 500 steps | Fits |
| **DART** (2 no-think drafts; answer directly if they agree) [2606.23181](https://arxiv.org/html/2606.23181) | Qwen3 0.6-32B | Qwen3-8B MATH-500: **78% answered directly, -67% thinking tokens, +2.6 points, 67.6 s → 29.5 s**. **Qwen3-4B: MATH-500 -5.0 points (70.5 → 65.5) at -48% tokens; HumanEval +17.1** | **none** | Fits. Warning: small models produce drafts that agree on the same wrong answer |
| Path-Lock Expert [2604.27201](https://arxiv.org/abs/2604.27201) | Qwen3-4B | no-think AIME24 35.3 → 44.7; stops reasoning from leaking into no-think | architecture change + training | Not a fit for now |
| Mid-Think (prompt trigger `<think>\n\n</think>\n\n<reason>\nOkay`) [2601.07036](https://arxiv.org/pdf/2601.07036) | Qwen3-8B / 14B | Inference: accuracy lands between no-think and think, and on GPQA it beats fixed budgets at the same length. LiveCodeBench 8B: **49.7 at 2,212 tokens vs think 65.9 at 9,931** (no-think 40.8 at 760). Used inside RL training: Qwen3-8B GPQA 58.5 → 61.1 with 15% less training time | none at inference | Fits. **Untested on Qwen3.5**, which dropped the soft switch |

## 4. Early exit when confident

| Method | Model | Result | Training | Same-4B fit |
|---|---|---|---|---|
| **DEER** (insert a trial answer at "Wait"; exit if confidence ≥ 0.95) [2504.15895](https://arxiv.org/pdf/2504.15895), [code (MIT, vLLM)](https://github.com/iie-ycx/DEER) | **Qwen3-4B** | GSM8K **94.1 → 94.5, 2,175 → 1,250 tokens**. MATH-500 92.2 → 92.6, 4,767 → 3,214. **GPQA-D 46.5 → 47.5, 9,294 → 3,275 (-65%)**. AIME24 63.3, 11,916 → 9,327. Code (HumanEval) 91.5 → 92.7, 3,768 → 1,050. Latency -27.9 to -40.1% (-36 to -59% with the branch-parallel variant) | **none** | **Fits. Best first move.** For Qwen3, use the geometric-mean confidence (Qwen3 tends to be overconfident) |
| Hidden-state probe (Zhang et al.) [2504.05419](https://arxiv.org/html/2504.05419) | R1-Distill 1.5-70B | **-24% tokens at 88.2% accuracy**. At threshold 0.9: **-19% tokens with identical accuracy (88.6%)** | 2-layer MLP trained on ≤1,000 of our own labelled traces (cheap) | Fits. Pairs well with our existing probe stack |
| Dynasor-CoT / Certaindex [2412.20993](https://arxiv.org/abs/2412.20993) | various | up to 50% less compute, 3.3x throughput. On R1-7B (in the DEER table) only -16% tokens | none | Fits. Weaker than DEER |
| **BAEE** (8 parallel continuations from early prefixes; majority vote) [2604.06613](https://arxiv.org/html/2604.06613) | **Qwen3-8B Think**, 32B, gpt-oss-120B | **52-88% of CoT tokens come after the answer is already recoverable**. 8B-Think: **76 → 81%, -63 to -70% serial tokens, -63 to -76% latency when run in parallel** (but 3.6x total tokens) | none | Fits. Good for latency at batch 1 |
| NEAT (exit neurons) [2602.02010](https://arxiv.org/abs/2602.02010) | 6 models | -22 to -28% tokens, accuracy kept | none | Fits (more engineering work) |
| TRACES [2604.21057](https://arxiv.org/abs/2604.21057) | not stated | -20 to -50%; bigger trade-offs on hard items | unknown | Unknown |

## 5. Implicit or latent CoT (near-zero visible tokens)

Reference points on GSM8K:
- **Qwen3-4B thinking scores 94.1%** (DEER table).
- **The CoT baselines below are short GPT-4-written equation traces** (GSM8k-Aug), not thinking traces.

| Method | Model | No-CoT | Explicit short CoT | Latent | Tokens / passes | Notes |
|---|---|---|---|---|---|---|
| Stepwise Internalization [2405.14838](https://arxiv.org/html/2405.14838) | Mistral-7B | 38 | 68 | **51** | 0 CoT tokens | GPT-2 9×9 multiply 99%, 11x faster. Training is costly (one round per removed step) |
| Coconut [2412.06769](https://arxiv.org/html/2412.06769) | GPT-2 | 16.5 | 42.9 | 34.1 | 8.2 vs 25 tokens | Logic tasks: ProsQA **97.0 vs CoT 77.5** |
| CODI (same model as teacher and student) [2502.21074](https://arxiv.org/html/2502.21074) | LLaMA-3.2-1B | 40.7 | 56.9 | 51.9 (55.6 in a later report) | 6 latent tokens; **3.1x compression, 2.7x speedup** | Self-distillation design fits our rule |
| SIM-CoT (ICLR'26) [2509.20317](https://arxiv.org/pdf/2509.20317) | LLaMA-3.1-8B | 39.5 | **71.7** | **64.1** | 7.2 vs 27.4 tokens | 1B: 1.9x speedup |
| KaVa (ICLR'26) [2510.02312](https://arxiv.org/pdf/2510.02312) | LLaMA-3.2-3B | 41.7 | **73.2** | **65.7** | 6.4 vs 31.6 passes (-80%) | LoRA r128. Natural-language traces: 60.0 vs 68.4 |
| **Selective Latent Thinking** [2605.25745](https://arxiv.org/html/2605.25745v1) | **Qwen3-4B** | 38.4 | **82.2 @ 85 tokens** | **75.3 @ 38 tokens** (RL) | about 2.2x fewer tokens | Full fine-tune on 385k examples. SVAMP 81.1 @ 15 tokens vs 84.2 @ 37 |
| System-2 → System-1 distillation [2407.06023](https://arxiv.org/html/2407.06023) | Llama-2-70B | 7.6 | 52.8 | **7.1 (failed)** | 0 | CoT could not be distilled into a direct answer |

Takeaways:
- Latent methods keep about **85-96% of short-CoT accuracy**, but only on grade-school arithmetic.
- There are **no GPQA or knowledge results (unknown)**.
- They need big training sets, and the published traces were written by GPT-4, so we would have to regenerate them with our own 4B.
- The useful finding is the **short explicit CoT row: on Qwen3-4B, 82% at about 85 tokens.** That is the sub-second math path.

## 6. Parallel vs sequential thinking (for latency)

| Method | Model | Result | Teacher / training | Same-4B fit |
|---|---|---|---|---|
| **NoThinking + parallel** [2504.09858](https://arxiv.org/html/2504.09858) | R1-Distill-32B (7B/14B similar) | At 700 tokens on AMC: **NoThinking 51.3 vs Thinking 28.9**. Parallel best-of-N: **up to 9x lower latency**, 4x fewer tokens on tasks with a verifier | none | Fits |
| **ParaThinker** [2509.04475](https://arxiv.org/html/2509.04475) | 1.5B / 7B | 8 paths: **+12.3% (1.5B), +7.5% (7B)**, **7.1% extra latency**. AIME24 1.5B 26.1 → 48.1 | SFT on 6.2k items; extra paths from **gpt-oss-20b** | Breaks our rule as published. We would have to regenerate the paths with our own 4B |
| short-m@k [2505.17813](https://arxiv.org/html/2505.17813) | 32B-670B | shortest chain is up to 34.5% more accurate than the longest; **-33% wall time** vs majority vote | none | Fits. Stop when the first m of k samples finish |
| DeepConf [2508.15260](https://arxiv.org/abs/2508.15260) | Qwen3, gpt-oss | **-84.7% tokens** vs full parallel voting at the same accuracy | none | Fits |
| ThreadWeaver [2512.07843](https://arxiv.org/html/2512.07843v2) | Qwen3-8B | 72.2 → 71.9 avg; **1.22x token-latency, 1.14x wall-clock** (4 GPUs) | SFT data rewritten by **GPT-5** | Breaks our rule. Small gain anyway |

**Why parallel fits us:** at batch 1, a 4B model is limited by memory bandwidth, not compute. So 4-8 samples in one batch cost only a little more time per step than 1 sample. Width (several short samples plus a vote) recovers the accuracy that shortening loses, at almost no extra latency. This is an inference from the papers above (BAEE, ParaThinker's 7.1% overhead); **it is unmeasured on our stack.**

## 7. What fits OpenDecide (same-4B teacher, small budget)

| Step | What | Cost | Expected effect (from papers; unmeasured on Qwen3.5-4B) |
|---|---|---|---|
| **T0** (no training) | Measure Qwen3.5-4B think-token distributions on **public train-split** items (GSM8K/MATH train, science train sets). Never on Decision Index, OHS-3, ejs-5 or GPQA test items | about $1-3 (H100, vLLM) | Gives our real curve |
| **T1** (no training) | Hard budget using Qwen's early-stop string, swept over 256 / 512 / 1k / 2k | in T0 | Sets the floor. Weak at tight budgets (L1 vs s1 gap of 20-25 points) |
| **T2** (no training) | **DEER early exit** (MIT, vLLM) with geometric-mean confidence | in T0 | Qwen3-4B: GSM8K -43%, **GPQA -65% at +1 point** |
| **T3** (no training) | **Router**: fast-path LoRA or 2 parallel no-think drafts; think only on disagreement or low confidence (DART-style; could reuse our existing probe signal) | in T0 | Thinking on about 13-25% of easy math (Thinkless, AdaptThink). DART at 4B: -5 points on MATH-500, so check precision of accepted answers |
| **T4** (no training) | **Parallel width**: 4-8 short-budget samples, vote or short-m@k; BAEE-style parallel probes from early prefixes | in T0 | 8B-Think: +5 points at -63 to -76% latency (BAEE) |
| **P1** (pilot, about $10-15) | **Concise self-distillation LoRA for think mode**: sample 8-16 traces per item with "solve concisely" from our own 4B, keep the **shortest correct** one, SFT a LoRA on that | about 1-2 h generation + less than 1 h SFT on H100 (my estimate) | -26% tokens at 99.5% relative accuracy (self-only), up to -57 to -64% (OPSDC/BIRD on 8B, with on-policy updates) |
| P1b (pilot, about $10) | **Short explicit CoT LoRA** for math-like items (target 50-150 tokens), using the 4B's own shortest correct traces | small | Qwen3-4B 82% at 85 tokens (SLT baseline) → **sub-second** at 130-200 tok/s |
| P2 (later, about $300-1,000 or more) | RL length control (Elastic, 200 steps → L1/ThinkPrune → AdaptThink) | 80-256 GPU-h in the papers | -50 to -65% tokens at about -2 points (math). Above the pilot budget |
| Not now | Latent CoT (CODI, KaVa, SIM-CoT, SLT); ParaThinker/ThreadWeaver as published | high | Math-only, -7 to -10 points vs short CoT; published data used outside teachers |

**Rough end-to-end estimate (mine, not measured):**
- **Math-like items:** fast path or router, then a short-CoT LoRA of about 100 tokens. That gives **about 0.5-1 s at 130-200 tok/s**, at roughly 80-85% GSM8K-class accuracy versus 88% for full thinking.
- **Hard science items:** budget plus DEER brings GPQA to about 3k tokens. Concise SFT could take that to about 2k. Parallel width does not shorten the serial path. That leaves about 10-15 s at 130-200 tok/s.
- **Reaching "a few seconds" on GPQA also needs faster decode** (FP8, CUDA graphs, speculative decoding; see the other reports) or a lower accuracy target. **Whether 57 → 76 GPQA survives at about 1k tokens is unknown.**

## 8. Unknowns and cautions

- No method above has published results on **Qwen3.5-4B**, which uses Gated-DeltaNet and has no /think soft switch. Every number is a transfer from Qwen3 or R1-Distill.
- The H100 batch-1 tok/s for Qwen3.5-4B is unknown.
- Small models are weak at stopping. One on-policy distillation study found 4B students "reach but don't commit" ([2609.37326](https://arxiv.org/html/2609.37326)), and DART's agreement router loses accuracy at 4B or smaller. **Always check the precision of accepted answers.**
- GPQA has no train split, so use it for evaluation only. Science-side compression evidence comes only from training-free methods (DEER, Mid-Think, BAEE) and from RL that generalised out of domain (L1: GPQA scales linearly with budget; MMLU-style knowledge benefits less).
- Papers whose published data used bigger teachers: Thinkless (R1-671B warm-up), ParaThinker (gpt-oss-20b), ThreadWeaver (GPT-5), latent-CoT datasets (GPT-4 traces), and Munkhbat's best variant (GPT-4o exemplars). Use only their self-only or regenerated-with-our-4B versions.
- Licence check needed before use: LLMLingua-2 (TokenSkip), and the DEER/DART code (DEER is MIT; DART paper is CC BY 4.0 and its code licence is unverified).
