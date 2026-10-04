# RESEARCH: how a small model (1-9B) closes the gap to big ones

Angle: small-model intelligence. For: model C (Qwen3.5-4B + LoRA, one-pass letter readout).
Date: 3 Oct 2026. Web research and local CPU checks only. No GPU, Modal, OpenRouter or paid calls.
No test splits, OHS-3 files, preds_ohs* or quarantine files were opened.
Gains marked "estimate" are my estimates for our setup. They are not measured.

---

## 0. Bottom line

1. **Task variety beats row count.** Many distinct task templates help on unseen tasks. Many rows per template do not.
   - Super-NaturalInstructions: unseen-task score grows log-linearly with the number of training tasks. It plateaus at about **64 rows per task**. An 11B model beat 175B InstructGPT by **+9.9 ROUGE-L** on 119 unseen tasks.
   - Instruction-diversity study: generalization to unseen rules appears only after about **400-500 distinct instructions**.
   - Our ~90K own rows should therefore cover about **1,000+ distinct templates of 50-100 rows each**. They should not be 12 families of ~7.5K rows each.
2. **Diversity drives out-of-distribution (OOD) gains. Quality drives in-domain gains** (quality-diversity-complexity survey).
   - This matches what we saw: dev went up and ejs-5 did not.
   - Adding new seeds or sources beats generating more data from the same seeds once the budget is large (2026 source-expansion paper).
3. **The cheapest OOD levers need no extra training:**
   - Weight interpolation: WiSE-FT gives +4 to +6 pp OOD in vision. LM-Cocktail recovers general skill in LLMs.
   - Checkpoint averaging.
   - Option-position debiasing (PriDe).
   - A small multi-view ensemble at test time, using option permutations or instruction rewordings. Cost is K times inference. 4 views x 16.6 ms is about 66 ms, still under Jev's 70-500 ms.
4. **Use our own model as the critic.** No bigger teacher is needed.
   - JTT: upweight the first model's errors. Worst-group accuracy rises **+16.2 pp** on average, but average accuracy falls 4.2 pp.
   - Dataset Cartography: training on the 33% most "ambiguous" rows beat 100% of the data OOD (WSC **87.6 vs 86.0**).
   - Scoring a 90K-200K pool with C1 costs about **$1.7-3.8**.
5. **Do not spend budget on these** (for a one-token classifier with program labels):
   - Higher LoRA rank or full fine-tuning.
   - RL.
   - STaR/ReST-style self-training.
   - Curriculum ordering.
   - Chain-of-thought (CoT) at inference.

   The evidence says they give about 0 for our setup, or do not apply. Section 3 has the details.
6. **Hard limit.** A model stores about **2 bits of knowledge per parameter**. A 4B model will not beat Jev on MMLU-Pro, GPQA or HLE through fine-tuning. Win only on decisions where the needed information is in the card or context.
7. **Realistic total (estimate).** If the data levers and free levers all work, C could gain about **+2 to +5 pp** on far, unseen domains over C1.
   - That could close the ejs-5 gap (-4.4). It is not guaranteed.
   - BOSS (NeurIPS 2023) found that classic OOD tricks rarely beat plain fine-tuning by much.

---

## 1. Facts about our setup (checked locally, CPU only)

- **LoRA covers every layer, including the 24 linear-attention layers.**
  - From the public weight shapes: Qwen3.5-4B has 32 layers, 8 full-attention and 24 Gated-DeltaNet (`linear_attn.in_proj_qkv/z/a/b`, `out_proj`).
  - At r16, attention + MLP adapters = 21,233,664 params. Linear-attention adapters = 11,231,232 params.
  - Sum = **32,464,896**. This exactly matches `expect_trainable` in `runs/q35_4b_main.json` and the "trainable params" line in our logs.
  - Coverage is complete. No fix is needed.
- **C1 training config** (`runs/q35_4b_main.json`):
  - r16 / a32, lr 7e-5, batch 16, KD weight 0.5.
  - Permutation twin 0.3 plus symmetric consistency. These already train option-order invariance, so test-time permutation gains will be smaller than in the papers.
- **Training cost:** 2.72 s/step / 16.9 rows/step = 0.161 s/row, which is 22.4K rows/h or **$0.183 per 1K rows**.

  | Rows | Hours | Cost |
  |---|---|---|
  | 20K | 0.9 | $3.7 |
  | 150K | 6.7 | $27.4 |
  | 300K | 13.4 | $54.9 |

- **Inference cost:** about $0.019 per 1K decisions. This is an upper bound: it assumes 16.6 ms each, run one at a time. Batched throughput is unknown and probably cheaper.
- **Capacity check** (Thinking Machines' argument):
  - The LoRA can hold about 2 bits/param x 32.5M = **~65 Mbit**.
  - 500K one-token labels carry about 2 bits each = **~1 Mbit**. Soft KD targets add a little more.
  - The adapter has roughly 60x more capacity than the labels need. Rank is not our bottleneck.

---

## 2. Why small models can beat big ones (and where they cannot)

| Finding | Number | Source |
|---|---|---|
| Fine-tuned 4-bit LoRA models vs GPT-4 on 31 tasks | **+10 pts** over GPT-4 on average; +34 over base | [LoRA Land](https://arxiv.org/abs/2405.00732) |
| Fine-tuned "small" LLMs vs zero-shot GPT-3.5/4 and Claude Opus on text classification | small fine-tuned models win consistently | [Bucher & Martini 2024](https://arxiv.org/abs/2406.08660) |
| Multitask training, 11B T0 vs 175B GPT-3, zero-shot | matches or beats it on **9 of 11** held-out datasets (16x smaller); more prompts per dataset gives a higher median and lower variance | [T0](https://arxiv.org/abs/2110.08207) |
| 11B Tk-Instruct vs 175B InstructGPT on unseen tasks | **+9.9 ROUGE-L** | [Sup-NatInst](https://arxiv.org/abs/2204.07705) |
| Prompt ensembles: GPT-J-6B vs few-shot GPT-3-175B | matches or beats it on **15 of 20**; **+10.2%** average over few-shot | [AMA prompting](https://arxiv.org/abs/2210.02441) |
| Curated and synthetic pretraining data: Phi-3-mini 3.8B | **69% MMLU**, close to Mixtral 8x7B | [Phi-3](https://arxiv.org/abs/2404.14219) |
| Phi-4 14B beats its teacher GPT-4o | GPQA 56.1 vs 50.6; MATH 80.4 vs 74.6 (400B synthetic tokens across 50 dataset types) | [Phi-4](https://arxiv.org/abs/2412.08905) |
| Test-time search (needs generation and a reward model) | 1B beats 405B on MATH-500; 3B beats 405B | [Liu et al. 2025](https://arxiv.org/abs/2502.06703) |
| Trend | capability per parameter doubles about every 3.3-3.5 months | [Densing law](https://arxiv.org/abs/2412.04315) |
| **Limit:** knowledge capacity | about **2 bits/param** (a 4B model holds about 8 Gbit) | [Allen-Zhu & Li](https://arxiv.org/abs/2404.05405) |
| **Limit:** high-quality "annealing" data | Llama-3 8B: +24.0% GSM8K, +6.4% MATH; **405B: negligible gain** | [Llama 3](https://arxiv.org/abs/2407.21783) |
| **Limit:** OOD | fine-tuned small models win in-domain; LLM in-context learning often wins OOD; 5 classic OOD methods gave no significant gain over plain fine-tuning | [BOSS, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/b6b5f50a2001ad1cbccca96e693c4ab4-Abstract-Datasets_and_Benchmarks.html) |

How this applies to us:
- Small models win when the task is narrow, the information is in the input, and training covers many task forms.
- They lose on stored knowledge and on unseen task forms.
- The Llama-3 annealing result shows that targeted high-quality data helps small models much more than big ones. That is the lever we have.

---

## 3. Levers: evidence, fit to C, cost

### 3.1 Task and format diversity. Highest value; costs authoring time, not GPU
- **Number of tasks.** [Sup-NatInst](https://arxiv.org/abs/2204.07705): gains are log-linear in task count up to 757 tasks, and saturate at 64 rows per task. [Flan-PaLM](https://arxiv.org/abs/2210.11416): most of the gain came from the first **282 of 1,836** tasks.
- **Instruction variety.** [Zhang et al. 2024](https://arxiv.org/abs/2402.10891): unseen-rule generalization appears at about **400-500** distinct instructions, even with few rows each.
- **Template mixing.** [Flan Collection](https://arxiv.org/abs/2301.13688):
  - Mixed zero-shot, few-shot and CoT templates gave **+2%+** in every setting, even at 3B.
  - Input inversion and source balancing were "critical".
  - Flan-T5 beat prior work by 3-17%.
- **Format brittleness.** [Sclar et al. 2024](https://arxiv.org/abs/2310.11324): up to **76 accuracy points** spread across meaning-preserving formats (LLaMA-2-13B). The sensitivity remains after instruction tuning.
  - Training on diverse formats reduces it ([Mixture of Formats, NAACL 2025](https://aclanthology.org/2025.naacl-srw.51/)).
  - [Sun et al. 2023](https://arxiv.org/abs/2306.11270): instruction-tuned models are not robust to rephrased instructions.
- **Fit:** very high. ejs-5 is a new task form, and dev gains did not transfer to it.
- **Cost:** about $0 extra GPU; it reshapes the same row budget.
- **Gain (estimate):** +1 to +3 pp on far domains.

### 3.2 Data quality and synthetic data without a bigger teacher
- **Phi and Cosmopedia lessons:** curate hard; make diversity explicit through seeds, topics, audiences and styles.
  - [Cosmopedia](https://huggingface.co/blog/cosmopedia): 25B tokens, 30M+ files, 34K+ topics.
  - Most of its prompts were seeded from web data; it varied audience and style to avoid duplicates.
- **Nemotron pipeline:** [Nemotron-4 340B](https://arxiv.org/abs/2406.11704) made **98%+** of its alignment data synthetic, from about 20K human rows. Its key step was filtering by a reward model.
  - For us, the program label is the verifier. That is stronger than a reward model.
- **Synthetic data scaling:** [SynthLLM](https://arxiv.org/abs/2503.19551) follows a rectified scaling law, with gains plateauing near **300B tokens** (pretraining scale).
  - [Source expansion vs fixed-source synthesis (2026)](https://arxiv.org/abs/2607.01727): at large budgets, **new seeds beat more responses per seed**. Fixed-source synthesis saturates.
- **Where synthetic classification data fails.** [Li et al., EMNLP 2023](https://arxiv.org/abs/2310.07849):
  - Real data beat zero-shot synthetic data by **16.9 pp** macro-F1 (RoBERTa), and beat few-shot (seeded) synthetic data by **6.7 pp**.
  - Seeding generation with real examples gave **+10.3 pp** macro-F1.
  - On the 6 most subjective tasks, the zero-shot synthetic loss was **-27.4 pp** macro-F1.
  - So: use Claude-authored, program-labelled rows for objective skills. Use human-labelled public splits for subjective decisions. Seed every own question with a real document or record.
- **Quality, diversity, complexity.** [Havrilla et al. 2024](https://arxiv.org/abs/2412.02980): quality matters most in-domain, diversity matters most OOD, and complexity helps both.
- **Personas for diversity.** [Persona Hub](https://arxiv.org/abs/2406.20094): 1.07M persona-seeded math problems took Qwen2-7B to **64.9% MATH**. That used a GPT-4 author, so only the diversity method transfers to us.
- **Model collapse.** [Gerstgrasser 2024](https://arxiv.org/abs/2404.01413): collapse happens when synthetic data *replaces* real data. *Accumulating* real plus synthetic data keeps test error bounded.
  - So keep human-gold rows in the replay. Never train C on C1's own hard labels as if they were gold.
  - Multi-source synthetic data keeps the output distribution broader ([Schaffelder & Gatt, ACL Findings 2026](https://aclanthology.org/2026.findings-acl.360/)). Vary author personas and styles.
- **Do not teach new facts.** [Gekhman et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.444/): rows with knowledge the model lacks are learned slowly, and once learned they *increase* hallucination.
  - Every own question must be decidable from the card plus common knowledge.
- **Small, curated sets can match big ones.** [LIMA](https://arxiv.org/abs/2305.11206) used 1K rows. [Deita](https://arxiv.org/abs/2312.15685) matched baselines with 6K rows (10x less) by selecting on complexity, quality and diversity.

### 3.3 Hard examples chosen by our own model. No teacher needed
- [JTT](https://arxiv.org/abs/2107.09044): train once, then upweight the errors.
  - Worst-group accuracy **+16.2 pp** on average (MultiNLI worst group 72.6%), but average accuracy **-4.2 pp**.
  - The error set held worst-group rows at **2.2x-15.9x** their base rate.
- [Dataset Cartography](https://arxiv.org/abs/2009.10795): the "ambiguous" rows (high variability across checkpoints) drive OOD gains.
  - On WinoGrande, the 33% most ambiguous rows reached **87.6 OOD vs 86.0** for 100% of the data. In-domain fell (78.7 vs 79.7).
  - On NLI, it stayed within 0.2 pp in-domain and gained OOD. Some easy rows are still needed for convergence.
- **Fit:** high. We have C1 and its snapshots (`snap_fracs`).
  - Score new candidate rows with C1. Keep all errors and ambiguous rows (p_true about 0.3-0.7). Downsample very easy rows (p_true > 0.95) instead of removing them.
  - Use mild weights (about 2-3x). JTT-strength weights cost in-domain accuracy.
- **Cost:** about $1.7 per 90K rows scored, sequential upper bound.
- **Gain (estimate):** +0.5 to +1.5 pp.

### 3.4 Minimal pairs, contrast sets, negation
- **Contrast sets.** [Gardner et al. 2020](https://arxiv.org/abs/2004.02709): models drop **up to 25%** on minimally edited inputs.
- **Counterfactual data needs varied edits.**
  - [Kaushik et al.](https://arxiv.org/abs/1909.12434) introduced counterfactually augmented data.
  - A follow-up reports **+1.0 to +5.9 pp** OOD ([2310.06666](https://arxiv.org/abs/2310.06666)).
  - [Joshi & He, ACL 2022](https://aclanthology.org/2022.acl-long.256/): edits that are not diverse limit OOD gains, and can make spurious cues worse.
  - So cover at least 10 edit types: negation, quantifier, scope, threshold, date or order, actor swap, exception clause, unit, double negation, distractor option.
- **Negation.**
  - Fine-tuning on negated sentences helps, but generalization stays weak ([Language models are not naysayers](https://arxiv.org/abs/2306.08189); [This is not a Dataset](https://arxiv.org/abs/2310.15941)).
  - Negation-focused tasks gave **+1.8 to +9.1%** on CondaQA ([2502.07717](https://arxiv.org/abs/2502.07717)).
  - Pairing each negated row with an affirmative paraphrase helps ([2406.07492](https://arxiv.org/abs/2406.07492)).
  - Our relation losses (complement / equivalence / inverse) already fit this pattern.
- **Fit:** high for the hard yes/no gap (47.4 vs 57.9) and the 8.9% double-negation flips. golden_train has only 0.34% double-negation rows.
- **Gain (estimate):** +3 to +8 pp on the hard yes/no slice; +0.3 to +1 pp overall.

### 3.5 Self-training, rejection sampling, RL (no bigger teacher)
- **STaR** ([2203.14465](https://arxiv.org/abs/2203.14465)): GPT-J 6B reached **72.5%** on CommonsenseQA, vs 73.0% for fine-tuned GPT-3 (30x larger).
- **ReST-EM** ([2312.06585](https://arxiv.org/abs/2312.06585)): beat SFT on human data for MATH and APPS. Gains shrink after a few iterations (overfitting).
- **SFT vs RL** ([Chu et al., ICML 2025](https://arxiv.org/abs/2501.17161)): RL generalizes to unseen rule variants; SFT memorizes. These are multi-step generation tasks.
- **Fit: low.** All of these need sampled reasoning traces. Our readout is one token, with exact program labels. Rejection sampling adds no information beyond the label we already have.
  - RL on a one-token action mostly sharpens confidence. [Thinking Machines](https://thinkingmachines.ai/blog/lora/): RL carries about 1 bit per episode.
  - The useful part of the idea is "train on what the model gets wrong". Section 3.3 covers that more cheaply.
- **Gain:** about 0. Skip.

### 3.6 Curriculum ordering
- [Wu, Dyer, Neyshabur, ICLR 2021](https://arxiv.org/abs/2012.03107): on standard data, curricula give only marginal benefit, and random order matches them. Curricula help with a very small time budget or noisy labels.
- Our labels are program-exact and the budget is not tiny.
- **Gain:** about 0. Skip, except keep a "stay close to C1" warm-up.

### 3.7 Longer training vs more diverse data; repetition; replay share
- **Repetition.** [Muennighoff et al.](https://arxiv.org/abs/2305.16264): up to **4 epochs** of repeated data is about as good as unique data. Value fades by about 16 epochs and is gone around 40. Replaying C1's rows is a 2nd epoch, which is safe.
- **OOD robustness fades with long training.** [Andreassen et al.](https://arxiv.org/abs/2106.15831): models are more robust OOD mid-training, and the advantage vanishes at convergence.
  - So prefer fewer steps on more diverse rows. Keep snapshots and average or interpolate them.
- **Replay share.** [Ibrahim et al. 2024](https://arxiv.org/abs/2403.08763): **5% replay** (weak shift) or **25%** (strong shift), plus LR re-warm and re-decay, matched full retraining at 10B.
  - Our 60% replay is very safe, but it spends about 60% of the budget on rows C1 has already seen.
  - Option: keep 60% in round 1. If the dev gate holds, use about 35-40% replay in round 2 and fund about 60K more new rows.
  - Inside the replay, prefer human-gold and C1-error rows over a uniform sample.

### 3.8 LoRA vs full fine-tuning vs higher rank
- [Thinking Machines, "LoRA Without Regret" (2025)](https://thinkingmachines.ai/blog/lora/):
  - LoRA matches full fine-tuning when it covers all layers (MLP matters most) and is not capacity-limited.
  - The best LoRA learning rate is about **10x** the full fine-tuning rate.
  - LoRA is more sensitive to large batches.
- [Biderman et al. 2024, "LoRA Learns Less and Forgets Less"](https://arxiv.org/abs/2405.09673):
  - Full fine-tuning learns weight changes of 10-100x higher rank, and wins on code/math continued pretraining.
  - LoRA forgets less than weight decay or dropout do. For OOD, forgetting less is a feature.
- **Fit:** our LoRA already covers all 32 layers (Section 1). Capacity is about 60x the label information.
- **Gain from higher rank or full fine-tuning:** about 0, plus more forgetting risk. Skip. Keep lr 7e-5 to 1e-4 and batch 16.

### 3.9 Stay close to the base or C1 (anchors, interpolation, averaging)
- **WiSE-FT** ([2109.01903](https://arxiv.org/abs/2109.01903)): interpolating the zero-shot and fine-tuned weights gave **+2 to +10 pp** OOD, with in-domain about +1 (CLIP). Added to standard fine-tuning, it gave **+4 to +6 pp** OOD.
- **LP-FT** ([2202.10054](https://arxiv.org/abs/2202.10054)): fine-tuning distorts features. LP-FT was **+1% in-domain and +10% OOD** vs full fine-tuning.
- **LM-Cocktail** ([2311.13534](https://arxiv.org/abs/2311.13534)), Llama-2-7B:
  - Fine-tuning on AG News took the task from 40.8 to 94.4, but general tasks fell from 46.8 to 38.6.
  - Merging with the base kept AG News at **94.5** and brought general tasks back to **47.7**.
- **SDFT** ([2402.13669](https://arxiv.org/abs/2402.13669)): self-distillation targets reduce forgetting at equal task accuracy. Our "stay close to C1" KL anchor is this idea.
- **Soups and EMA.**
  - [Model soups](https://arxiv.org/abs/2203.05482): T5-base greedy soup +0.1 to +0.8 on GLUE tasks.
  - [EMA](https://arxiv.org/abs/2411.18704): better generalization, calibration and robustness to noisy labels.
- **Fit:** very high. Step B already tests weight-softening of C1. Apply the same to C: average late snapshots, then use a pre-registered alpha between C and C1 chosen on the dev gate.
- **Cost:** evaluation only, about $1-3 per sweep.
- **Gain (estimate):** 0 to +1.5 pp OOD.

### 3.10 Rationales as an extra training task (still no CoT at inference)
- [Distilling Step-by-Step](https://arxiv.org/abs/2305.02301): a 770M T5 beat 540B PaLM using 80% of the labels. On ANLI it beat standard fine-tuning by **+8%** on average.
  - It used multi-task learning with separate label and rationale prefixes. Inference needs the label only.
- [Explanation-based fine-tuning, ACL 2023](https://aclanthology.org/2023.acl-long.242/): smaller accuracy drop under spurious cues: ComVE **+1.2**, CREAK **+9.1**, e-SNLI **+15.4**, SBIC **+6.5**.
  - It worked with human or model-written explanations. Effects were larger on bigger models.
- **Fit:** medium. Our programs can write template rationales, so no teacher is needed. The effect at 4B with template text is unknown.
- **Cost:** a pilot of about 20K rows costs about $3.7 plus evaluation.
- **Gain (estimate):** -0.5 to +1.5 pp. Run a pilot only. Keep it only if it wins on the dev gate by a margin pre-registered beforehand.

### 3.11 Long documents
- [ProLong](https://arxiv.org/abs/2410.02660):
  - Long data must be mixed with high-quality short data (about 60% long / 40% short in continued pretraining). 100% long data hurts.
  - Training beyond the evaluation length helps.
  - For SFT, short instruction data alone gave strong long-context results, and **adding even 1% synthetic long SFT data hurt**.
- **Fit:** medium.
  - Cost per row grows with length. Our mean row length is unknown here; compute it from golden_train. If the mean is ~0.5-1K tokens, a 16K-token row costs about 16-32 average rows.
  - Use real long documents only (no synthetic padding), at about 3-5% of rows, aimed at the LongBench-style skills.
- **Gain (estimate):** +2 to +5 pp on long-doc evals; small overall.

### 3.12 Test-time compute for a one-pass classifier
| Option | Evidence | Cost | Fit to C1 |
|---|---|---|---|
| Cyclic option permutations, averaging probabilities | [PriDe paper](https://arxiv.org/abs/2309.03882), 0-shot MMLU: llama-2-13B 50.8 to **54.7**, gpt-3.5 67.2 to **69.8**; CSQA llama-2-13B 57.0 to **66.6** | n x inference | smaller gain likely: C1 already trains a permutation twin |
| PriDe: estimate the option-ID prior on 5% of inputs | +1.0 (llama-2-13B MMLU) at **1.15x** cost | about 1.15x | first measure C1's recall std over letters on dev |
| Batch calibration (remove the batch-mean bias) | +8% / +6% over in-context learning on 13 tasks (PaLM 2-S/L) | about 0 | **risky**: assumes balanced classes; real decision base rates vary |
| Input rewording ensembles | 2026: semantic rephrasing gave **about 1.8x more accuracy per dollar** than self-consistency, winning 5/6 tasks ([2608.09351](https://arxiv.org/abs/2608.09351)); text test-time augmentation +0.6 to +0.9 pp ([2206.13607](https://arxiv.org/abs/2206.13607)) | K x | good; we train on rewordings already |
| AMA-style prompt ensembles | GPT-J-6B matches or beats GPT-3 few-shot on 15/20 | K x | good |
| Negated-twin view: average p(yes given q) with 1 - p(yes given not-q) | uses our complement-relation training; no paper with our exact setup | 2x | test on dev; may hurt if the negation view is weak |
| CoT or test-time search | CoT +12-14% only on math/symbolic, **+0.7% elsewhere** ([Sprague et al.](https://arxiv.org/abs/2409.12183)); 1B > 405B needs process-reward search | 10-100x and generation | skip: breaks our speed win |

- **Gain (estimate)** for a pre-registered 2-4 view readout: +0.3 to +1.5 pp.
- The latency budget allows it: 4 x 16.6 ms is about 66 ms, below Jev's 70 ms floor.
- Report 1-view and K-view results side by side. Never pick views per benchmark.

### 3.13 Label quality and soft labels
- [Northcutt et al. 2021](https://arxiv.org/abs/2103.14749): public test sets have about **3.3%** label errors on average (6%+ for ImageNet validation). Small model rankings flip with about 5-6% more mislabeled rows.
  - Audit public training splits with C1 disagreement plus a program or human re-check before use.
- [Peterson et al. 2019](https://openaccess.thecvf.com/content_ICCV_2019/papers/Peterson_Human_Uncertainty_Makes_Classification_More_Robust_ICCV_2019_paper.pdf): human soft labels gave better generalization under strong shift and more robustness. This supports keeping vote-share KD targets wherever human votes exist.

---

## 4. Ranking: OOD gain per dollar (about $90 budget)

| # | Lever | Extra GPU $ | Far-domain gain (estimate) | Evidence | Do it? |
|---|---|---|---|---|---|
| 1 | Template/task diversity in the new rows (1,000+ templates, 50-100 rows each, 30+ wordings per family) | ~0 | +1 to +3 | strong (Sup-NatInst, T0, Flan, Zhang) | **Yes** |
| 2 | Weight interpolation C to C1, plus snapshot averaging | ~1-3 (eval) | 0 to +1.5 | strong in vision; medium in LLMs | **Yes**, pre-registered alpha |
| 3 | C1-scored hard/ambiguous selection (JTT-lite, 2-3x weights) | ~2-4 | +0.5 to +1.5 | medium-strong (JTT, Cartography) | **Yes** |
| 4 | Varied minimal pairs and negation (3-5% double negation, affirmative twins) | ~0 (row reshuffle) | +0.3 to +1 overall; +3 to +8 on hard yes/no | medium | **Yes** |
| 5 | Real-document seeding; subjective tasks from human public splits | ~0 | +0.5 to +1 | strong (Li 2023) | **Yes** |
| 6 | 2-4 view test-time readout (permutations or rewordings) | inference only | +0.3 to +1.5 | medium | **Yes**, report both |
| 7 | Prior/position debias (PriDe-style) | ~0 | 0 to +1 | medium | measure first |
| 8 | Replay 60% to ~35-40% in round 2 (more new rows) | ~0 | +0.3 to +1 (estimate) | medium (Ibrahim) | if round-1 gate holds |
| 9 | Program-written rationale auxiliary task | ~4 pilot | -0.5 to +1.5 | medium (other scales) | pilot only |
| 10 | Long-doc rows (real, 3-5%) | high per row | small overall | medium (ProLong) | small dose |
| 11 | Higher rank / full fine-tuning | more | ~0 | strong (capacity, forgetting) | No |
| 12 | RL / STaR / ReST | more | ~0 here | does not apply | No |
| 13 | Curriculum ordering | 0 | ~0 | strong (null) | No |
| 14 | CoT at inference | huge latency | ~0.7 outside math | strong | No |

---

## 5. Concrete rules for the C dataset (from the evidence)

1. **Templates.**
   - Target 1,000+ distinct task templates across the ~12 families.
   - Use 50-100 rows per template. Stop adding rows to a template after about 100.
2. **Format variety on every family:**
   - 30+ instruction wordings;
   - 3+ label-definition styles;
   - option counts from 2 to 10;
   - exact answer-letter balance;
   - few-shot-in-card in about 5-10% of rows (Flan: about 10% few-shot templates help zero-shot);
   - input-inversion variants (e.g., "which rule produced this outcome").
3. **Vary yes/no base rates** from 20-80% across templates. This stops the model from learning a fixed prior.
4. **Seed each own question with a real document or record** that has a commercial licence. Zero-shot synthetic data loses 7-17 pp.
5. **Decidable from the card.** A program checks that each answer follows from the card plus common knowledge. No new world facts.
6. **Subjective decisions** (tone, harm, preference) come only from human-labelled public training splits, using vote-share soft labels where available.
7. **Minimal pairs** make up about 15-20% of own rows, covering at least 10 edit types. Double negation is 3-5% of new rows, each with an affirmative-paraphrase twin.
8. **Score all candidate rows with C1** before the final mix:
   - Keep every error and ambiguous row.
   - Keep about 30% of very easy rows.
   - Upweight errors 2-3x.
   - Re-check every C1-disagreement row against the program or gold label. This catches label bugs.
9. **Replay** prioritizes human-gold and C1-error rows. Keep the KL anchor to C1.
10. **Persona and style variety** for Claude-authored text (multi-source effect). Run a dedupe or near-duplicate check (embedding cosine threshold, as in Deita) before freezing.
11. **Training:**
    - LoRA r16 on all layers, already verified.
    - lr 7e-5 to 1e-4, batch 16.
    - Keep snapshots for averaging.
    - Do not run longer than planned. OOD robustness fades at convergence.
12. **Evaluation discipline:**
    - Pick alpha, views and weights on the dev gate only.
    - Measure the sealed new-domain suite once per candidate.
    - Report 1-view next to K-view.

---

## 6. Unknowns to measure first (cheap)

- C1's letter-position bias on dev (recall std per letter). This decides whether PriDe is worth it.
- C1's yes/no prior shift on far domains. Is the ejs-5 loss one-directional (yes-bias or no-bias)? This decides between calibration and data fixes.
- Mean token length of golden_train rows. This sets the true cost of long-doc rows.
- The real batched inference throughput on H100. The scoring costs here are upper bounds.
- How large the gains in WiSE-FT, LP-FT and JTT are for a 4B decoder LoRA. Most of that evidence comes from vision or encoder models.

---

## Sources
- Sup-NatInst: https://arxiv.org/abs/2204.07705
- T0: https://arxiv.org/abs/2110.08207
- Flan-PaLM scaling: https://arxiv.org/abs/2210.11416
- Flan Collection: https://arxiv.org/abs/2301.13688
- Instruction diversity: https://arxiv.org/abs/2402.10891
- LoRA Land: https://arxiv.org/abs/2405.00732
- Bucher & Martini: https://arxiv.org/abs/2406.08660
- AMA prompting: https://arxiv.org/abs/2210.02441
- Phi-3: https://arxiv.org/abs/2404.14219
- Phi-4: https://arxiv.org/abs/2412.08905
- Cosmopedia: https://huggingface.co/blog/cosmopedia
- Nemotron-4 340B: https://arxiv.org/abs/2406.11704
- SynthLLM: https://arxiv.org/abs/2503.19551
- Source expansion vs fixed-source synthesis: https://arxiv.org/abs/2607.01727
- Li et al. 2023 (synthetic data for classification): https://arxiv.org/abs/2310.07849
- Quality/diversity/complexity survey: https://arxiv.org/abs/2412.02980
- Persona Hub: https://arxiv.org/abs/2406.20094
- Model collapse, accumulate vs replace: https://arxiv.org/abs/2404.01413
- Multi-source synthetic data: https://aclanthology.org/2026.findings-acl.360/
- Gekhman (new knowledge): https://aclanthology.org/2024.emnlp-main.444/
- LIMA: https://arxiv.org/abs/2305.11206
- Deita: https://arxiv.org/abs/2312.15685
- JTT: https://arxiv.org/abs/2107.09044
- Dataset Cartography: https://arxiv.org/abs/2009.10795
- Contrast sets: https://arxiv.org/abs/2004.02709
- Counterfactually augmented data: https://arxiv.org/abs/1909.12434
- CAD follow-up: https://arxiv.org/abs/2310.06666
- Joshi & He: https://aclanthology.org/2022.acl-long.256/
- Negation: https://arxiv.org/abs/2306.08189 , https://arxiv.org/abs/2310.15941 , https://arxiv.org/abs/2502.07717 , https://arxiv.org/abs/2406.07492
- STaR: https://arxiv.org/abs/2203.14465
- ReST-EM: https://arxiv.org/abs/2312.06585
- SFT vs RL: https://arxiv.org/abs/2501.17161
- Curricula: https://arxiv.org/abs/2012.03107
- Data-constrained scaling: https://arxiv.org/abs/2305.16264
- OOD robustness during fine-tuning: https://arxiv.org/abs/2106.15831
- Continual pretraining replay: https://arxiv.org/abs/2403.08763
- LoRA Without Regret: https://thinkingmachines.ai/blog/lora/
- LoRA Learns Less and Forgets Less: https://arxiv.org/abs/2405.09673
- Knowledge capacity: https://arxiv.org/abs/2404.05405
- WiSE-FT: https://arxiv.org/abs/2109.01903
- LP-FT: https://arxiv.org/abs/2202.10054
- LM-Cocktail: https://arxiv.org/abs/2311.13534
- SDFT: https://arxiv.org/abs/2402.13669
- Model soups: https://arxiv.org/abs/2203.05482
- EMA of weights: https://arxiv.org/abs/2411.18704
- Distilling step-by-step: https://arxiv.org/abs/2305.02301
- Explanation-based fine-tuning: https://aclanthology.org/2023.acl-long.242/
- ProLong: https://arxiv.org/abs/2410.02660
- PriDe: https://arxiv.org/abs/2309.03882
- Batch calibration: https://arxiv.org/abs/2309.17249
- Format sensitivity: https://arxiv.org/abs/2310.11324
- Mixture of Formats: https://aclanthology.org/2025.naacl-srw.51/
- Instruction rephrasing robustness: https://arxiv.org/abs/2306.11270
- Text test-time augmentation: https://arxiv.org/abs/2206.13607
- Test-time augmentation for LLMs (2026): https://arxiv.org/abs/2608.09351
- To CoT or not: https://arxiv.org/abs/2409.12183
- 1B vs 405B test-time scaling: https://arxiv.org/abs/2502.06703
- Densing law: https://arxiv.org/abs/2412.04315
- Llama 3 (annealing): https://arxiv.org/abs/2407.21783
- BOSS: https://proceedings.neurips.cc/paper_files/paper/2023/hash/b6b5f50a2001ad1cbccca96e693c4ab4-Abstract-Datasets_and_Benchmarks.html
- Label errors: https://arxiv.org/abs/2103.14749
- Human soft labels: https://openaccess.thecvf.com/content_ICCV_2019/papers/Peterson_Human_Uncertainty_Makes_Classification_More_Robust_ICCV_2019_paper.pdf
- Qwen3.5-4B architecture (public config and weight index): https://huggingface.co/Qwen/Qwen3.5-4B
