# V_latent: can latent recurrence close our hard-reasoning gap?

Verifier A (hard-reasoning claims) for the "OpenDecide-4B ARC" proposal. Planning only. I made no Modal, gcloud or paid calls.
Date: 4 Oct 2026. I read every paper below from its arXiv PDF or HTML. Numbers are copied from the papers' tables. Where a paper does not give a number, I say "not stated".

## 0. Bottom line in plain words

1. **The two papers the proposal cites are real, but neither one tests what we need.** "Latent Recurrent Thoughts" (LRT) and "ReLIT" both freeze a model and add a small looping block. That part matches the proposal. But each is trained **separately for each task**, and neither reports GPQA, MMLU, GSM8K or CRUXEval. ReLIT also has no ablation, and it compares a model fine-tuned on in-domain data against other models' zero-shot leaderboard scores.
2. **The research pattern is consistent.** Latent recurrence helps short, step-by-step problems (arithmetic, logic chains, graph search). It does **not** add knowledge. It also stops working when the real reasoning needs hundreds to thousands of tokens. GPQA is exactly that case: Qwen3.5-4B gets 76.2 only with a 32,768-token thinking budget.
3. **My honest estimate for one-pass latent recurrence on C1:**
   - GPQA: +0 to +5 points, which closes 0-13% of the 38.8-point gap.
   - GSM8K: +5 to +15 points (22-65% of the 23.2-point gap), and only with step-level supervision.
   - CRUXEval: +2 to +8 points (10-35% of the 21.5-point gap). No paper measures this, so confidence is low.
   - Decision Index: about **+0.2 to +0.9** in total. We trail by 4.68.
4. **Text thinking closes the GPQA gap. Latent recurrence does not.** On the same 4B, thinking gives 76.2 vs Jev's 78.6, about 94% of the gap. But that takes tens of seconds per question, far outside Jev's 70-500 ms. No published latent method has matched thinking on GPQA at any size.
5. **If we test it, a small Modal pilot can do it** (section 6). The proposal's "tiny block over cached states" is the weakest-evidence form. The two forms with evidence are:
   - LRT-style: latents are fed back into the backbone as soft tokens.
   - ETD/LOTUS-style: the backbone's own middle layers are looped.

## 1. The two cited papers: what they actually show

### 1a. Latent Recurrent Thoughts (LRT)
Chen and Fu, arXiv 2609.01117, 1 Sep 2026. https://arxiv.org/abs/2609.01117

- **Setup:** a frozen Qwen3-8B decoder, a 4.2M-parameter "proposer" and a 7M-parameter TRM-style refiner, 11.2M trainable parameters in total. K=32 latents in training and 4 at inference.
  - The refiner makes 45 passes (S=3, H=3, T=4). Only the last cycle gets gradients.
  - The refined latents are **injected as soft input tokens into the frozen LLM**, which then runs a full forward pass and decodes the answer.
- **Results (Table 1):** LRT vs Direct vs zero-shot CoT (non-thinking mode), mean of 3 seeds.

  | Task | LRT | Direct | Zero-shot CoT |
  |---|---:|---:|---:|
  | Countdown-4 | 56.7 | 27.8 | 30.0 |
  | Sudoku | 49.2 | 17.3 | 23.9 |
  | HumanEval | 37.8 | 13.4 | 15.9 |
  | MBPP | 51.5 | 28.7 | 35.4 |
  | StrategyQA | 75.1 | 67.4 | 69.9 |
  | **Average** | **54.1** | **30.9** | **35.0** |

- **Against Qwen3 thinking mode** (Table 2, 32,768-token budget, LRT on the left):

  | Task | LRT | Thinking | Winner |
  |---|---:|---:|---|
  | Countdown | 56.7 | 85.3 | thinking |
  | Sudoku | 49.2 | 0.5 | LRT (thinking fails within its budget) |
  | HumanEval | 37.8 | 92.1 | thinking |
  | MBPP | 51.5 | 49.3 | LRT |
  | StrategyQA | 75.1 | 76.4 | thinking |

  Thinking costs 8.9x to 453.9x more FLOPs per example.
- **With a frozen Qwen3-4B** (Appendix H, Table 16):
  - Five-task average 49.0, vs 54.1 with the 8B.
  - Countdown 51.2, Sudoku 43.1, HumanEval 33.0.
- **Training cost:** each stage runs 30 epochs at batch 64 on 1×96 GB GPU. Countdown and Sudoku use 100k generated examples each.
- **Caveats:**
  - Modules are trained per task. The authors write "each new task requires training new modules".
  - StrategyQA targets include the reference rationale, so the decoder still writes text there.
  - No MMLU, GPQA or GSM8K.
  - The refiner scales with size: 7M, 14M and 28M give 56.7, 66.3 and 69.1 on Countdown.
- **What it means for us:** a frozen backbone with a small trainable recurrent module works on narrow symbolic tasks. It gives no evidence on knowledge MCQ. It also differs from the ARC design in one important way: LRT feeds the latents **back into the backbone**, so the backbone's knowledge layers process them. LRT also uses 45 refiner passes, while ARC proposes 1-4.

### 1b. ReLIT
Panwar, Singh and Bansal (IIT Roorkee), arXiv 2608.08113, 8 Aug 2026. https://arxiv.org/abs/2608.08113

- **Setup:** a frozen TinyLlama-1.1B plus a trainable recursive block. The parameter count is not stated. Output is a single-token label.
  - Trained on each dataset's own train split: 5,000 examples each for ProofWriter and RuleTaker, 800 for HELP, 200 for NaN-NLI and 2,000 for TaxiNLI.
- **Results vs the best GLoRE baseline:**

  | Dataset | ReLIT | Best baseline |
  |---|---:|---|
  | ProofWriter | 98.6 | QwQ-32B 82.4 |
  | RuleTaker | 97.6 | QwQ-32B 82.4 |
  | HELP | 53.43 | QwQ-32B 78.1 |
  | TaxiNLI | 56.30 | o1-mini 81.4 |
  | NaN-NLI | 55.2 | ChatGPT 57.3 |

- **Caveats:**
  - The baseline numbers are copied from the GLoRE leaderboard (zero-shot), so a fine-tuned classifier is being compared with zero-shot models.
  - There is no "frozen model without the block" baseline, no CoT baseline, no LoRA baseline and no ablation of recursion depth.
  - A fine-tuned RoBERTa already reached about 99% on RuleTaker-style rule reasoning in 2020 (Clark et al., https://arxiv.org/abs/2002.05867).
  - It loses badly on 3 of 5 datasets.
- **What it means for us:** it is not evidence that recurrence adds reasoning power, and it says nothing about GPQA, GSM8K or CRUXEval.

## 2. Method-by-method table

Column guide:
- "Gain vs same model without it" means vs no-CoT, direct, non-looped or iso-parameter.
- "vs text CoT / thinking" compares against the same model reasoning in text.
- "LoRA / frozen OK?" asks whether the method works with our LoRA'd frozen backbone.

| Method (paper) | Size | Gain vs same model without it | vs text CoT / thinking | Training cost | LoRA / frozen OK? | Knowledge vs math |
|---|---|---|---|---|---|---|
| **Coconut** ([2412.06769](https://arxiv.org/abs/2412.06769)) | GPT-2 124M; appendix: Llama-3.2-3B, Llama-3-8B | GSM8K 16.5 → 34.1 (GPT-2); ProsQA 76.7 → 97.0. **Llama-3.2-3B 26.0 → 31.7; Llama-3-8B 42.2 → 43.6** | **Below CoT on GSM8K: 34.1 vs 42.9.** Beats CoT on ProsQA (97.0 vs 77.5). Meta's card gives Llama-3-8B-Instruct 79.6 with 8-shot CoT | Multi-stage curriculum, full FT on GSM8K-Aug (385,620 ex.) | Full FT only. Not shown with LoRA | Math/logic only. [2512.21711](https://arxiv.org/abs/2512.21711) finds Coconut tokens are "uninterpretable placeholders" that exploit dataset artifacts on MMLU and HotpotQA |
| **CODI** ([2502.21074](https://arxiv.org/abs/2502.21074)) | GPT-2; LLaMA-3.2-1B | GSM8K 19.1 → 43.7 (GPT-2); SVAMP 44.1 → 61.1 (1B) | GPT-2: 43.7 vs CoT-SFT 44.1. 1B: "90% of CoT-SFT" (figure only); SVAMP 61.1 vs 66.7 | GPT-2: 36 h on 1 A100. 1B: 48 h on 1 A100 | **Yes, LoRA r=128, α=32** | Math (GSM8K-style short traces) |
| **Recurrent depth "Huginn"** ([2502.05171](https://arxiv.org/abs/2502.05171)) | 3.5B, 800B tokens from scratch | At 0.18T tokens vs a fixed-depth baseline trained the same way: MMLU 24.16 → 25.59, GSM8K-CoT 1.82 → 9.02. Final r=1 → r=32: MMLU 23.60 → 31.38, GSM8K-CoT 0.00 → 34.80/42.08 | Its GSM8K numbers already use text CoT. [2507.02199](https://arxiv.org/abs/2507.02199): extra recurrence "yields only marginal gains and falls well short" of explicit CoT | Pretraining on up to 4,096 AMD MI250X | No (pretrained from scratch) | **Knowledge weak**: MMLU 31.4. The authors say the model "has fewer facts memorized" (OBQA closed 38.2 vs open 49.2) |
| **Ouro / LoopLM** ([2510.25741](https://arxiv.org/abs/2510.25741)) | 1.4B and 2.6B, 4 loops, 7.7T tokens | 1.4B vs Qwen3-4B-Base: GSM8K 78.92 vs 72.86, MATH500 82.40 vs 59.60, BBH 71.02 vs 70.95, but **MMLU 67.35 vs 73.19**. No equal-data non-looped baseline at scale | **Ouro-Thinking (loops plus text thinking) GPQA 45.5 (1.4B) and 52.7 (2.6B) vs Qwen3-4B 54.5** (Ouro Table 9) | 7.7T-token pretraining. Its RL attempts "did not yield significant performance gains" | No (pretrained from scratch) | **Looping does not increase knowledge capacity: about 2 bits/parameter with or without loops.** Gains come from "knowledge manipulation" |
| **Looped transformers** (Saunshi et al., ICLR'25, [2502.17416](https://arxiv.org/abs/2502.17416)) | 1B-scale on Pile | 12⊗2 vs 12⊗1: math word problems 26.7 → 34.3 (24-layer model: 29.3); closed-book QA 8.2 → 9.3 (24-layer: 11.2) | Theory only: T loops can simulate T CoT steps | Pretraining | No | **Clean split:** looping recovers 282% of the depth gap on math but only 37% on closed-book (memorisation) QA |
| **Retrofitted recurrence** ([2511.07384](https://arxiv.org/abs/2511.07384)) | TinyLlama-1.1B, OLMo-2-1B, Llama-3.2-1B | TinyLlama (4,8,4), two-phase training vs static model on the same data: **GSM8K 51.2 vs 45.2**, MMLU 44.8 vs 44.4, ARC-C 37.7 vs 36.5 | GSM8K is scored with generation (1-shot), not one pass | 26B + 26B tokens of full training (layer surgery, then "healing") | No: weights are retrained. LoRA not shown | Math gains; MMLU flat |
| **ETD (Encode-Think-Decode)** ([2510.07358](https://arxiv.org/abs/2510.07358)) | OLMo-2 1B; loops 4 middle layers | k=5: GSM8K 44.05 → 56.56, ARC-C 50.85 → 61.43, MMLU 44.52 → 49.95, DROP 31.8 → 38.1. **NQ 20.98 → 20.53, TriviaQA 54.12 → 55.93.** MATH: 4.57 → 6.22 at k=3, then 4.33 at k=5 | Not compared | Full mid-training on 50B tokens | No (full weights) | **Factual recall flat; reasoning-heavy MC rises.** The best case for knowledge MC in this review is +5.4 MMLU at 1B |
| **Pause tokens** ([2310.02226](https://arxiv.org/abs/2310.02226)) | 1B, 130M | Pause in pretraining and fine-tuning: SQuAD +18 EM, CSQA +8, **GSM8K 7.5 → 8.5** | Not compared | Needs pause-pretraining | **Pause added only at fine-tuning gives "lukewarm", mixed results.** Filler "...." on a standard model gives no gain | Mixed |
| **Filler tokens** ([2404.15758](https://arxiv.org/abs/2404.15758)) | small synthetic | Solves 2 synthetic algorithmic tasks that no-CoT cannot | n/a | Needs "specific, dense supervision" | n/a | Synthetic only |
| **SoftCoT** ([2502.12134](https://arxiv.org/abs/2502.12134)) | Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct, frozen | GSM8K 83.70 → 85.81 (Qwen) and 79.61 → 81.03 (Llama) **vs zero-shot CoT** | The model **still writes text CoT** after the soft thoughts. It is an add-on, not a replacement | Small projection only | **Yes, frozen backbone** | Math, plus StrategyQA |
| **LOTUS** (looped, padded, step-supervised; [2606.31779](https://arxiv.org/abs/2606.31779)) | GPT-2, Llama-3.2-1B, **Llama-3.2-3B** | 3B: **GSM8K no-CoT 38.3 → 70.0** | **3B: 70.0 vs explicit CoT 71.5** (CODI only 60.8). Thought phase 133 ms vs 339 ms (H100, batch 1) | Full FT, 30 epochs on GSM8K-Aug | No (full FT) | GSM8K-style only. Needs gold step tokens. The authors say other latent methods "underperform explicit CoT beyond 1B parameters, and the gap widens with scale" |
| **Continuous CoT on long traces** ([2607.16972](https://arxiv.org/abs/2607.16972)) | Llama-3.2-1B, Qwen2.5-1.5B | n/a | **MATH, Qwen2.5-1.5B: CoT-SFT 52.80 vs CODI-10 14.52 and C-MTP 14.20.** Llama-1B: 23.80 vs 9.92 | Fine-tuning | LoRA-type FT | **About 65% drop once traces reach hundreds of tokens** |
| **HRPO** (hybrid latent RL; [2505.18454](https://arxiv.org/abs/2505.18454)) | Qwen2.5-1.5B and 3B | 3B average 0.700 vs GRPO 0.691. MMLU-ST 0.590 vs GRPO 0.601 | Both arms still generate text | RL | Full | About +1 point over text RL, and it loses on MMLU-ST |
| **Latent Thought Flow** ([2606.16222](https://arxiv.org/abs/2606.16222)) | Llama-3.2 1B/3B, Llama-3.1-8B; LoRA r=128 | "Beats CoT", but its **CoT baseline for Llama-3.1-8B on GSM8K-Aug is 19.17%** | The baseline is far too weak to trust (Meta's own 8B CoT is about 80) | 100 epochs | LoRA | Math only |
| **RLTT** (RL over Ouro loops; [2602.10520](https://arxiv.org/abs/2602.10520)) | Ouro 1.4B and 2.6B Thinking | GPQA 19.7 → 38.4 (2.6B, vs GRPO) | Under its 2,048-token budget **Qwen3-4B scores 11.1 on GPQA, below the 25% chance level**, so these GPQA numbers are a budget artifact | RL | No | GPQA claims not usable |
| **ReLAT** (test-time training on latents; [2606.06252](https://arxiv.org/abs/2606.06252)) | Qwen3-4B, 8B, 14B | Qwen3-8B AIME24 56.7 → 73.3 (vs a latent baseline) | GPQA-D 48.0 on Qwen3-14B, below Qwen3-14B thinking at 64.0 (Qwen3 report) | **1,167.55 s per sample vs 434.34 s** | Temporary LoRA | Unusable at 70-500 ms |

## 3. What the evidence says

1. **Looping does not add knowledge.**
   - Ouro measures about 2 bits/parameter with and without loops.
   - ETD: NQ 20.98 → 20.53 and TriviaQA 54.12 → 55.93.
   - Saunshi et al.: closed-book QA recovers only 37% of the depth gap.
   - Huginn: MMLU 31.4.
   - So looping cannot close the part of GPQA or MMLU that needs facts. Our MMLU is 82.5 vs 92.0.
2. **It helps "manipulation": composing facts and short multi-step computation.**
   - ETD (1B): GSM8K +12.5 points, ARC-C +10.6, MMLU +5.4.
   - Retrofit (TinyLlama): GSM8K +6.0.
   - LOTUS (3B): GSM8K +31.7 over no-CoT.
3. **The gains shrink as models get bigger and as traces get longer.**
   - Coconut: +5.7 at 3B, then +1.4 at 8B.
   - LOTUS reports that other latent methods' gap to CoT "widens with scale".
   - With realistic MATH traces of 300-600 tokens, continuous CoT keeps only about 27% of CoT-SFT accuracy (14.52 vs 52.80).
   - GPQA thinking traces are in the thousands of tokens: Qwen recommends 32,768 output tokens.
4. **No latent or looped method has matched a proper thinking baseline on GPQA.**
   - Ouro-Thinking uses loops plus text thinking and still scores 45.5 and 52.7, vs Qwen3-4B thinking at 54.5.
   - ReLAT: 48.0 vs 64.0.
   - RLTT's GPQA numbers are below chance for the base models.
5. **The strongest results need step-level supervision and weight changes.**
   - LOTUS uses full fine-tuning with gold CoT step tokens. Huginn, Ouro, ETD and retrofit pretrain or mid-train on 50B to 7.7T tokens.
   - Methods that work with a frozen or LoRA'd backbone are weaker on general tasks:
     - CODI and LTF use LoRA r=128.
     - LRT and ReLIT are trained per task.
     - SoftCoT still generates text CoT.
6. **Many "beats CoT" claims rest on weak CoT baselines.**
   - LTF's Llama-3.1-8B CoT scores 19.17 on GSM8K-Aug.
   - Several papers SFT the model on terse GPT-4 traces (GSM8K-Aug), which lowers its own CoT accuracy. LOTUS's explicit CoT at 3B is 71.5. Its natural-language CoT run is 68.41.

## 4. Our gap: what one-pass latent recurrence could plausibly close

The text-thinking reference is the same 4B family.
- **Qwen3.5-4B thinking:** GPQA-D 76.2 (https://huggingface.co/Qwen/Qwen3.5-4B, 32,768-token budget). The card gives no non-thinking scores.
- **Qwen3-4B** (Qwen3 report, [2505.09388](https://arxiv.org/abs/2505.09388), Tables 17 and 18):
  - GPQA-D: 41.7 non-thinking → 55.9 thinking (+14.2).
  - MMLU-Redux: 77.3 → 83.7.
  - MATH-500: 84.8 → 97.0.
- **Qwen3-4B-Base:** GSM8K 87.79 (4-shot CoT), CRUX-O 55.0 (1-shot).

| Benchmark (n in DI sample) | C1 | Jev | Gap | Text thinking (same 4B family) | **One-pass latent recurrence (my estimate)** | Why |
|---|---:|---:|---:|---|---|---|
| GPQA Diamond (196; SE ≈ 3.5) | 39.8 | 78.6 | 38.8 | 76.2 closes ~94%, but takes tens of seconds and up to 32K tokens | **+0 to +5 (0-13%)** | Knowledge-heavy with long chains. No GPQA win for any latent method. Ouro+thinking is still below Qwen3-4B thinking. Even +5 is only 1.4 SE, so we could not detect it with n=196 |
| GSM8K (460; SE ≈ 2.3) | 56.7 | 79.9 | 23.2 | Qwen3-4B-Base 87.79 with CoT text, so thinking clears Jev | **+5 to +15 (22-65%)** | Short traces are where latent methods work: LOTUS 3B gets 95% of the CoT gain and CODI 1B gets about 90%. That requires step supervision, many latent slots and loops through the backbone. The tiny side block in ARC is closer to Coconut-level gains (+1.4 to +5.7) |
| CRUXEval (229; SE ≈ 3.3) | 51.5 | 73.0 | 21.5 | Qwen3-4B-Base CRUX-O 55.0 (1-shot); thinking score unknown | **+2 to +8 (10-35%)**, low confidence | No latent paper reports CRUXEval. The closest is LRT on code, where it is far above direct but far below thinking (HumanEval 37.8 vs 92.1). Program tracing is a long-state task |

- **Decision Index effect.** Each benchmark point is worth 1/30 of an index point, because there are 6 knowledge benchmarks and 5 areas.
  - Sum of the low ends (0 + 5 + 2): about **+0.2** index.
  - Sum of the midpoints (2.5 + 10 + 5): about **+0.6**.
  - Sum of the high ends (5 + 15 + 8): about **+0.9**.
  - The gap to Jev is 4.68 (54.83 vs 59.51), so latent recurrence closes roughly 5-20% of it.
- **About Jev.** Jev scores 78.6 on GPQA within 70-500 ms. Among the numbers I read, no published model of 4B or below comes near that without thinking. That suggests Jev is a larger model (its size is unknown; our estimate is ≤30B active), not one with a smarter one-pass head. I infer this. It is not proven.

## 5. Implications for the ARC design (hard-reasoning part only)

1. **Do not count on latent recurrence for GPQA or MMLU.** Treat it as a GSM8K, CRUXEval, CLadder or Chess-type lever.
2. **A small side block over cached states is the weakest-evidence form.**
   - Every positive result either loops the backbone's own layers (Ouro, ETD, Huginn, retrofit, LOTUS) or feeds latents back through the backbone (LRT, Coconut, CODI, SoftCoT).
   - A block that only reads cached final states never re-uses the 4B's feed-forward layers, which is where the knowledge is stored.
   - Better variants to test:
     - (a) LRT-style: K=4-16 latents injected as soft tokens before the trusted question repeat.
     - (b) ETD-style: LoRA on a looped middle block, k=2-3, which ETD found best.
   - Qwen3.5-4B is a hybrid of Gated DeltaNet and attention, in the pattern 8 × (3 DeltaNet + 1 attention). No paper has looped or retrofitted that architecture, so this is unknown.
3. **Supervision.**
   - LOTUS, CODI and Coconut all need CoT traces. GSM8K-Aug was written by GPT-4, so our "no bigger teacher" rule excludes it.
   - A compliant source is **self-distillation from our own Qwen3.5-4B in thinking mode**, which is no bigger than our model. Claude-authored or program-generated traces (code execution) also work.
   - Keep traces short. Above a few hundred tokens the evidence says continuous CoT collapses.
4. **The halting gate and RL are risky.**
   - Ouro's dynamic exit broke RL tooling, and its RL "did not yield significant performance gains".
   - RLTT shows trajectory-level reward can help, but its GPQA numbers come from a broken token budget.
   - Fixed k=2-3 is the safer default.
5. **Latency fits.**
   - LRT reports net latency below zero-shot CoT.
   - LOTUS's thought phase is 133 ms on a 3B (H100, batch 1).
   - A 1-4 step small block adds milliseconds.
   - Latency is not the blocker. Accuracy on knowledge items is.

## 6. If the owner wants to test it on Modal (planning only, needs a GO)

The cheapest falsification test touches no DI, OHS-3 or ejs-5 items, and A16 stays frozen. It would need its own /goal step.

- **Training data:**
  - GSM8K train split (7,473 items, MIT licence, written by humans), converted to our decision format with program-made distractors.
  - Program-generated Python tracing items, with outputs computed by executing the code.
  - Short reasoning traces self-distilled from our own Qwen3.5-4B in thinking mode.
  - Dedupe against all 1,319 GSM8K test items and all 800 CRUXEval items.
- **Dev evaluation:**
  - A held-out slice of GSM8K train.
  - Held-out generated code items.
  - A SuperGPQA slice used for evaluation only (ODC-BY), as the GPQA proxy.
- **Arms** (each with a C1 control):
  - (a) C1 as-is.
  - (b) The ARC small block, 1-4 steps.
  - (c) LRT-style soft-token latents with K=8.
  - (d) An ETD-style looped middle block with LoRA, k=2.
- **Kill rule:** drop the idea if no arm beats C1 by ≥3 points on GSM8K-dev (paired bootstrap, p<0.05) and by ≥0 on the SuperGPQA proxy.
- **Cost (my estimate, not measured):**
  - Each arm: about 1-3 H100-hours for roughly 20k items × 3 epochs.
  - Trace generation: about 1-2 H100-hours.
  - Total: about 8-12 GPU-hours, roughly $30-50 at about $4/hour. Check Modal's current price before running.

## 7. Unknowns

- Qwen3.5-4B scores on GPQA, GSM8K and CRUXEval in **non-thinking** mode are not published.
- Qwen3.5-4B thinking scores on GSM8K and CRUXEval are not published.
- No paper tests latent recurrence on a LoRA'd hybrid DeltaNet model.
- No paper tests latent recurrence with a one-pass option-logit readout on knowledge MCQ.
- Not stated in the papers:
  - CODI's exact LLaMA-1B GSM8K number (figure only).
  - ReLIT's parameter count.
  - LRT's per-task data sizes for HumanEval and StrategyQA.
- Jev's size is unknown.

## Sources
- LRT: https://arxiv.org/abs/2609.01117
- ReLIT: https://arxiv.org/abs/2608.08113
- Coconut: https://arxiv.org/abs/2412.06769
- CODI: https://arxiv.org/abs/2502.21074
- Huginn: https://arxiv.org/abs/2502.05171
- Huginn latent-CoT analysis: https://arxiv.org/abs/2507.02199
- Ouro / LoopLM: https://arxiv.org/abs/2510.25741
- Looped transformers (Saunshi et al.): https://arxiv.org/abs/2502.17416
- Retrofitted recurrence: https://arxiv.org/abs/2511.07384
- ETD: https://arxiv.org/abs/2510.07358
- Pause tokens: https://arxiv.org/abs/2310.02226
- Filler tokens: https://arxiv.org/abs/2404.15758
- SoftCoT: https://arxiv.org/abs/2502.12134
- LOTUS: https://arxiv.org/abs/2606.31779
- Continuous CoT, two regimes: https://arxiv.org/abs/2607.16972
- HRPO: https://arxiv.org/abs/2505.18454
- Latent Thought Flow: https://arxiv.org/abs/2606.16222
- RLTT: https://arxiv.org/abs/2602.10520
- ReLAT: https://arxiv.org/abs/2606.06252
- Coconut causal analysis: https://arxiv.org/abs/2512.21711
- RuleTaker: https://arxiv.org/abs/2002.05867
- Qwen3 report: https://arxiv.org/abs/2505.09388
- Qwen3.5-4B card: https://huggingface.co/Qwen/Qwen3.5-4B
- Llama 3 model card: https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md
- Our DI numbers: bench/decision_index/report_sample10k.json
