# R_training: training-side ways to close the knowledge gap (C1 4B vs Jev)

Researcher: training. Date: 3 Oct 2026. Web research only (no Modal, no paid calls). Local files read: only
`opendecide-data/lean/train_decoder.py` and `runs/q35_4b_main.json` (to get C1's LoRA config). Numbers marked
**(est.)** are my estimates; everything else is quoted from the cited source.

## TL;DR (plain words)

1. **Most of the "knowledge" gap is a thinking gap, not a missing-facts gap.** The same Qwen 4B family scores much
   higher when it is allowed to think: Qwen3-4B GPQA-Diamond is **41.7 without thinking and 55.9 with it**, and the
   Qwen3.5-4B model card lists **GPQA-Diamond 76.2** (mode not labelled; almost certainly thinking). Jev's score is 78.6.
   C1 one-pass scores 39.8, which is about the non-thinking level.
2. **Training can't squeeze multi-step thinking into one pass at about 4B.** Phi-3 3.8B on GSM8K scores **28%** with no CoT,
   **31%** with CoT "internalized" into one pass, and **74%** with written-out CoT. GSM8K, CRUXEval, GPQA, CLadder and
   ChessBench are "compute" items. More LoRA training will not fix them.
3. **The best lever is an optional "think route":** the same 4B model, with the adapter off and thinking on under a capped budget.
   A cheap router sends it only the items that need computation. One-pass stays the fast default. This is the only route
   that plausibly closes most of the GPQA, GSM8K and CRUXEval gaps. It costs latency (seconds, not ms) on the routed items.
4. **Measure forgetting before fixing it.** C1 already has a KL anchor to the frozen base. A free, inference-only test answers
   whether forgetting matters: base vs C1 vs C1 with a down-scaled LoRA, all on non-DI dev sets. If forgetting does matter,
   the cheapest repair is LoRA scaling (WiSE-FT for free), then more anchor/replay rows and on-policy targets.
5. **Adding facts through LoRA won't move MMLU.** C1 trains 32.5M parameters, which is ≤1% of the base model's ~8B-bit
   knowledge store (2 bits/param). Facts that are new to the model are learned slowly and raise hallucination.
6. **GRPO/RL: skip for now.** Qwen already did heavy RL. A public zero-RL 4B recipe ends below Qwen's own model. RL on a
   one-letter output has no reasoning to reinforce. The budget needed for meaningful RL (about $40+ per run (est.)) is
   above ours.
7. **The leftover MMLU gap (82.5 vs 92.0) is mostly capacity.** Jev is likely ≥7x bigger (est.). Training cannot close
   this at 4B. Thinking helps a little (+6 pts on MMLU-Redux for Qwen3-4B). Retrieval is the other lever (not in this
   report's scope).

---

## 1. Where the gap really comes from

### 1a. Same 4B, thinking vs no thinking (verified numbers)

| Model / mode | MMLU-Redux | GPQA-Diamond | MATH-500 | AIME'24 | Source |
|---|---|---|---|---|---|
| Qwen3-4B **non-thinking** | 77.3 | 41.7 | 84.8 | 25.0 | Qwen3 tech report, Table 18 |
| Qwen3-4B **thinking** | 83.7 | 55.9 | 97.0 | 73.8 | Qwen3 tech report, Table 17 |
| Qwen3.5-4B (card; mode not labelled) | 88.8 | 76.2 | – | – | HF model card (also MMLU-Pro 79.1, SuperGPQA 52.9) |
| Qwen3-4B-Base (few-shot) | MMLU 72.99 | GPQA 36.87 | GSM8K 87.79 (CoT) | CRUX-O 55.0 | Qwen3 tech report, Table 7 |
| **C1 one-pass** (DI) | MMLU 82.5 | 39.8 | GSM8K 56.7 | CRUXEval 51.5 | given |
| **Jev** (DI) | MMLU 92.0 | 78.6 | GSM8K 79.9 | CRUXEval 73.0 | given |

- **Qwen3.5-4B non-thinking scores: unknown.** One search snippet claimed GPQA 51.6 and MMLU-Redux 69.2, but I could not
  confirm them on the card. Treat them as unverified.
- The harnesses differ, so these rows are not directly comparable to the DI numbers. The pattern is still clear:
  C1 (39.8 GPQA) sits at the non-thinking level, and Jev (78.6) sits at the 4B thinking level.

### 1b. CoT matters for math, symbolic and code items, and barely at all for pure recall

- Sprague et al., *To CoT or not to CoT*:
  - Across 100+ papers and 20 datasets × 14 models, CoT helps mainly math and symbolic tasks: +12.3 on math and +14.2 on
    symbolic on average.
  - **On MMLU, direct answers ≈ CoT, except for questions containing "="; ~95% of MMLU's CoT gain comes from those.**
  - For us: MMLU recall items are fine in one pass. GPQA, GSM8K and CRUXEval are not.
- MMLU-Pro paper: CoT beats direct answering by up to ~19 pts (GPT-4o +19.1) on the reasoning-heavy MMLU-Pro.
- Physics of LMs 3.2 (knowledge manipulation): LMs retrieve stored facts well, but **fail at simple
  classification/comparison over those facts unless CoT is used in both training and inference**. Inverse search is
  ~0%. This is a property of the architecture, not of model size.

### 1c. One-pass ceiling: internalizing CoT barely works at 4B

- Deng et al., *Implicit CoT / Stepwise Internalization*, Table 3, GSM8K:

  | Model | No CoT | CoT internalized (one pass) | Written-out CoT |
  |---|---|---|---|
  | **Phi-3 3.8B** | 0.28 | **0.31** | 0.74 |
  | Mistral 7B | 0.38 | 0.51 | 0.68 |

- Yu, Xu, Weston, Kulikov, *Distilling System 2 into System 1*: several System-2 methods distill well, but **CoT on GSM8K
  did not distill**. The distilled model was much worse than the CoT model.
- **Conclusion:** the DI items where we lose most (GSM8K −23.2, CRUXEval −21.5, GPQA −38.8, CLadder −7.5,
  ChessBench −5.5) are mostly computation. A one-pass head will not reach Jev on them through any training recipe I found.

## 2. Does the decision fine-tune erase knowledge? Measure first, then repair

### 2a. Evidence

- **LoRA learns less, forgets less** (Biderman et al., TMLR 2024): LoRA keeps out-of-domain skills better than full
  fine-tuning, and regularizes better than weight decay or dropout. Full fine-tuning learns updates of 10–100× higher rank.
- **RL's Razor** (ICLR 2026): forgetting is predicted by the **KL between the fine-tuned and base model, measured on the
  new task's inputs**. On-policy methods (RL) find KL-minimal solutions. SFT can move arbitrarily far.
- **Retaining by Doing** (Chen, Razin, Narasimhan, Chen 2025): across Llama and Qwen at 1B–8B, RL forgets less than SFT
  with equal or better target accuracy. The practical recipe is **"Iterative-SFT": regenerate the training targets from the
  current model at the start of each epoch**. This "approximately on-policy" data substantially cuts forgetting.
- **Math-only SFT vs RL transfer** (arXiv 2507.00432), Qwen3-14B:
  - Non-reasoning transfer index: **SFT −104.1 vs RL +52.2**.
  - IFEval: 42.3 (SFT) vs 70.0 (RL).
  - KL on IFEval: 0.283 (SFT-no-think) vs 0.019 (RL).
  - Qwen3-8B: off-policy SFT has a non-reasoning transfer index of −40.5. On-policy SFT has +30.2.
- **SDFT** (ACL 2024): the model rewrites the targets in its own words. After OpenFunctions fine-tuning, HumanEval went
  13.4 → 9.8 with vanilla SFT and 13.4 → 15.2 with SDFT.
- **Self-Distillation Enables Continual Learning** (arXiv 2601.19897), Qwen2.5-7B:
  - Prior-task average: 64.5 (SDFT) vs 53.4 (SFT).
  - MMLU stays ~70–71 with SDFT vs 64–70 with SFT.
  - Cost: 2.5× FLOPs and ~4× wall-clock.
- **Spurious forgetting** (ICLR 2025): many apparent drops are lost *task alignment*, not lost knowledge. They come back
  with **50–100 samples and 1–3 epochs**. Freezing the bottom layers helps.
- **WiSE-FT, i.e. weight interpolation with the base** (Lin et al., *Speciality vs Generality*): this was the best
  balance of specialist skill and general skill among the methods tested. For a LoRA it costs nothing: scale the
  adapter by α in [0, 1] at inference.

### 2b. What C1 already does

From `runs/q35_4b_main.json` and `train_decoder.py`:
- LoRA r16, α32, on all 7 projections: **32,464,896 trainable params**.
- lr 7e-5, ~0.97 epoch over ~500K rows.
- **β=1.0 KL anchor to the frozen base** on rows marked `anchor`. This is already "replay of the base's own outputs" /
  learning-without-forgetting.

C1 is therefore partly protected. The anchor, though, ties C1 to the base model's *one-pass* answers. It cannot lift
GPQA or GSM8K above the base's one-pass level.

### 2c. Measurement protocol (free L4, inference only, ~1–3 h (est.))

1. **Dev sets with no DI overlap.** Decontaminate by exact or 13-gram match only. Never look at DI scores.
   - ARC-Challenge.
   - MMLU-Pro items whose `src` is **not** `ori_mmlu-*` (MMLU-Pro reuses MMLU questions).
   - A SuperGPQA subset.
   - A held-out slice of the GSM8K **train** split (MIT).
   - Program-generated Python "predict the output" items (CRUXEval-style, labels from actually running the code).
   - Licences for eval-only sets matter less, but keep them separate from training data.
2. **Arms, all in the same one-pass readout:**
   - base (adapter off)
   - C1 at α ∈ {0.5, 0.75, 1.0}
   - base in **thinking mode** with a capped budget (the ceiling)
3. **Also log the mean KL(base‖C1) over candidate tokens** on the decision dev set. This is RL's Razor's forgetting
   predictor; track it for every future round.
4. **Gate:**
   - If C1(α=1) ≥ base one-pass − 1 pt on knowledge dev, forgetting is not our problem. Stop working on forgetting.
   - If C1 is lower, pick α on the Pareto front of decision dev vs knowledge dev, then use the repairs in 2d.

### 2d. Repairs, cheapest first

1. **LoRA scale α** (free). Recovers up to the base-vs-C1 difference and costs some decision accuracy. Measure both.
2. **More anchor rows from general-knowledge MCQs.** The target is the base's own one-pass distribution. The trainer
   already supports this through `beta` and `meta.anchor`.
3. **On-policy refresh (Iterative-SFT):** recompute soft targets from the current model at each epoch start.
4. **LoRA on upper layers only, or freeze the bottom layers** (spurious-forgetting fix).

**Expected size:** bounded by (base one-pass − C1). C1's MMLU of 82.5 is already high for a one-pass 4B, so I expect this
to be **≤2 pts** (est.). It is not the main lever.

## 3. Think-then-distill with no bigger teacher (same 4B only)

### Options

- **A. Offline self-distillation**
  1. Run Qwen3.5-4B (adapter off, thinking on) k=4 times per question on licensed questions.
  2. Use the vote shares as soft labels for the one-pass head. The trainer's `kd` path already takes soft targets.
  3. Keep a row only if the majority answer matches the gold answer (STaR-style rejection sampling), or, where there is
     no gold, if agreement is ≥0.75.
- **B. On-policy self-distillation (OPSD)**, arXiv 2601.18734; *Rethinking OPSD* 2607.05184. The student is the
  non-thinking model. The teacher is the same model with thinking on or with privileged information.
  - With non-thinking training rollouts, performance is kept (0.591 → 0.590).
  - With thinking rollouts, it drops to 0.532.
  - Privileged-context distillation degraded thinking models by up to 17% relative on AIME/HMMT.
  - **Rule: use it only for the one-pass head, never on the think route.**

### Expected gain

- **Small.** On MMLU-type recall, CoT ≈ direct (Sprague). On multi-step items, internalization gives Phi-3 3.8B
  only 28 → 31 on GSM8K.
- The likely gain is better readout and calibration, plus some short-reasoning items: **+1–3 on the knowledge area**
  (est.).

### Cost (est.)

- 10K questions × 4 samples × ~1K thinking tokens ≈ 40M generated tokens.
- At an assumed 2–4K tok/s batched for a 4B model on an L4 with vLLM (unverified for the Qwen3.5 hybrid DeltaNet
  architecture), that is **~3–6 L4-hours**, which fits the free credit.

## 4. The big lever: an optional think route

- **Design**
  - Same base weights, adapter off (zero forgetting by construction).
  - Thinking on, with a budget cap (try 512 / 1024 / 2048 tokens).
  - Answer constrained to the option letter.
- **Router (no extra model)**
  - Use Sprague's finding: route when the question or options contain an equation or "=", numbers with operators, code,
    or units, **or** when one-pass max-probability is below τ.
  - Tune τ and the budget on the non-DI dev sets only.
- **Evidence that routing keeps most of the gain:** Thinkless (NeurIPS 2025) cuts long-chain use by **50–90%**. On Minerva
  Algebra it thinks on only **25.88%** of items and gets **0.9459 vs 0.9577** for always-think.
- **Expected effect (est.; different harnesses)**
  - **GPQA:** ~40 toward 56–76 (Qwen3-4B thinking 55.9; Qwen3.5-4B card 76.2).
  - **GSM8K:** toward ~85–90 (Qwen3-4B-Base 87.8 with CoT; Phi-3 3.8B explicit CoT 74).
  - **CRUXEval:** up, size unknown.
  - **MMLU:** +2–6 (Qwen3-4B MMLU-Redux 77.3 → 83.7).
- **Latency (est.):** 500–2,000 thinking tokens at ~100–200 tok/s single-stream is **~3–20 s per routed item**, which is
  10–100× slower than one-pass. That is acceptable only as an opt-in "deep mode" used where it pays (owner rule).
- **Training-side work**
  - None needed for v1, because base thinking is already strong.
  - **Optional:** shorten the traces with same-model rejection sampling. Sample k traces on GSM8K-train / MATH-train
    (MIT) and program-labelled code items, keep the shortest correct one, then SFT a small think-LoRA. The data is on-policy,
    so forgetting stays low.
  - Calibrate the router threshold.

## 5. RL with verifiable rewards (GRPO)

- **General-Reasoner-Qwen3-4B** (zero-RL from Qwen3-4B-Base): MMLU-Pro 62.8, GPQA 42.9, SuperGPQA 32.5. That is
  **below** the official Qwen3-4B thinking GPQA-D of 55.9, so Qwen's own post-training already beats a public RL recipe at
  4B. Extra GRPO on Qwen3.5-4B (card GPQA-D 76.2) is likely to give little.
- **Qwen3 report:** *"for Knowledge, STEM, Math, and Coding tasks, Thinking Mode Fusion and General RL do not bring
  significant improvements."* For Qwen3-8B, on-policy distillation took 1,800 GPU-h vs **17,920 GPU-h for RL**, with a
  better AIME'24 (74.4 vs 67.6).
- **Cost reference:** Open-RS used a 1.5B model, 7,000 samples and **$42** (4×A40, 24 h) to reach AIME24 46.7. A 4B
  thinking model costs more (est.).
- **GRPO on the one-pass head** means rewarding a single letter. That is on-policy classification with no reasoning to
  reinforce, so expect little.
- **Lesson from the RL papers above:** if we retrain the head, on-policy objectives forget less than more off-policy SFT.
- **Data under our rules** (no teacher: the rollouts come from our own 4B, and the answers come from programs or humans):
  - GSM8K train (MIT) and MATH train (MIT).
  - Generated Python programs with executed outputs.
  - Program-generated causal and logic questions.
- **Verdict:** skip now. Revisit only for think-route length compression (Thinkless-style) if the budget grows.

## 6. Licensed knowledge-rich data, and capacity limits

- **Capacity** (Physics of LMs 3.3)
  - LMs store **~2 bits per parameter**, including at int8. Reaching that needs **~1,000 exposures per fact**; with
    ~100 exposures capacity is lower.
  - Junk data lowers capacity. Prepending a domain name to the data restores it.
  - For us: base 4B ≈ **8B bits**. C1's LoRA (32.5M params) has a ceiling of ≈65M bits, under 1% of the base, and LoRA
    learns less than full fine-tuning.
  - Jev at ≤30B active (MoE total possibly larger; size unknown) ≈ **≥60B bits, ≥7.5× ours** (est.).
- **New facts through fine-tuning** (Gekhman et al., EMNLP 2024): unknown facts are learned much slower, and **as they are
  learned, hallucination rises linearly**. The best dev score comes from fitting mostly *known* examples.
- **Phi-4-mini** (3.8B, textbook-style synthetic data): MMLU 67.3. Microsoft's card says the model "does not have the
  capacity to store too much factual knowledge" and suggests search/RAG.
- **FineWeb-Edu** (ODC-By): MMLU 33 → 37 and ARC 46 → 57 for models *pretrained from scratch* on 350B tokens. That is
  pretraining scale, not a LoRA effect. Its filter was also trained on Llama-3-70B labels, so the owner needs to rule on
  whether that counts as a bigger model selecting our data.
- **Expected MMLU gain from adding textbook data to the LoRA: ~0–1 pt** (est.). Not recommended for facts.
- **What is worth doing:** knowledge-format rows built on facts the base already knows (verified by base thinking-mode
  agreement). These fix readout and alignment.
  - Sources: OpenStax (CC BY 4.0 for most titles; check each book), ARC (CC BY-SA 4.0), Claude-authored MCQs.
  - **Avoid:** SciQ (CC BY-NC 3.0, non-commercial), and Cosmopedia or NuminaMath solutions (generated by larger models,
    which breaks the no-big-teacher rule).

## 7. Recommended plan

| Step | What | Cost | Gate / expected |
|---|---|---|---|
| 1 | Forgetting test + LoRA-α sweep + base-thinking ceiling on non-DI dev sets; log KL(base‖C1) | free L4, inference only | Tells us whether forgetting matters (≤2 pts est.) and how much thinking adds per category |
| 2 | Think route v1: base weights, thinking with budget cap, rule + confidence router | free/cheap | Largest lever: most of the GPQA, GSM8K and CRUXEval gaps (est.); +3–20 s on routed items |
| 3 | Self-distill thinking-mode vote shares into the one-pass head (Known items only), keeping the anchor share | ~3–6 L4-h (est.) | +1–3 on the knowledge area (est.) |
| 4 | (Only if the budget grows) short-trace rejection-sampling SFT or Thinkless-style RL for the think route | ≥$40 (est.) | Lower think latency |

**Don't:**
- Put textbook facts into the LoRA.
- GRPO the one-pass head.
- Use any model bigger than 4B as teacher or filter without an owner ruling.
- Let DI items choose anything.

**Projection for the knowledge area (C1 51.2 vs Jev 68.9; est.)**
- Training-only fixes (steps 1 and 3): **+1–4**.
- With the think route: **plausibly +8–15**, which could close most of the gap. This is uncertain because the DI area
  composition, formats and per-benchmark weights are unknown to me.
- MMLU likely ends around ~85–88 at best vs Jev 92. That residual is capacity.

**Unknowns**
- Qwen3.5-4B non-thinking scores.
- Whether the Qwen3.5-4B card's 76.2 GPQA is thinking mode (very likely, not stated).
- Exact DI knowledge-area composition and formats (for example, whether GSM8K is scored as MCQ).
- Jev's size and architecture.
- vLLM throughput for Qwen3.5's hybrid Gated-DeltaNet on an L4.

## Sources

- Qwen3 Technical Report: https://arxiv.org/html/2505.09388 (Tables 7, 17, 18, 21; thinking-fusion/general-RL quote)
- Qwen3.5-4B model card: https://huggingface.co/Qwen/Qwen3.5-4B ; base card (arch: 32 layers, hidden 2560, FFN 9216, Apache-2.0): https://huggingface.co/Qwen/Qwen3.5-4B-Base
- Sprague et al., To CoT or not to CoT: https://arxiv.org/pdf/2409.12183
- MMLU-Pro: https://arxiv.org/pdf/2406.01574
- Physics of LMs 3.2 (Knowledge Manipulation): https://arxiv.org/pdf/2309.14402
- Physics of LMs 3.3 (Knowledge Capacity): https://arxiv.org/abs/2404.05405
- Deng et al., From Explicit CoT to Implicit CoT: https://arxiv.org/html/2405.14838v1
- Yu et al., Distilling System 2 into System 1: https://arxiv.org/pdf/2407.06023v2
- LoRA Learns Less and Forgets Less: https://arxiv.org/abs/2405.09673
- RL's Razor: https://arxiv.org/abs/2509.04259
- Retaining by Doing: https://arxiv.org/abs/2510.18874
- Does Math Reasoning Improve General LLM Capabilities?: https://arxiv.org/html/2507.00432
- SDFT (Self-Distillation Bridges Distribution Gap): https://arxiv.org/pdf/2402.13669
- Self-Distillation Enables Continual Learning: https://arxiv.org/html/2601.19897v1
- Self-Distilled Reasoner (OPSD): https://arxiv.org/pdf/2601.18734 ; Rethinking OPSD for Thinking Models: https://arxiv.org/html/2607.05184v1
- Spurious Forgetting: https://arxiv.org/pdf/2501.13453
- Speciality vs Generality (WiSE-FT for LLMs): https://scispace.com/pdf/speciality-vs-generality-an-empirical-study-on-catastrophic-44oixzw2bg.pdf
- Thinkless: https://arxiv.org/pdf/2505.13379
- General-Reasoner: https://arxiv.org/html/2505.14652v4
- Open-RS (RL for small LLMs, $42): https://arxiv.org/html/2503.16219v2
- Gekhman et al., Fine-tuning on new knowledge and hallucinations: https://arxiv.org/pdf/2405.05904
- Phi-4-mini report/card: https://arxiv.org/pdf/2503.01743 ; https://huggingface.co/microsoft/Phi-4-mini-instruct
- FineWeb / FineWeb-Edu: https://arxiv.org/html/2406.17557 ; https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu
