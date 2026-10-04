# RESEARCH: cross-domain / zero-shot generalization for instruction-following classifiers

Angle: how to make C (Qwen3.5-4B + LoRA, one-pass letter readout) win on domains it never saw.
Date: 3 Oct 2026. Web research only. CPU only. No GPU, no paid calls, no forbidden files.
Local files read (to fit advice to our code): the header docstrings of `train_decoder.py` and `batchcal.py` only.
Every number below has a source URL in the list at the end. "unknown" means I could not find or check it.

---

## 0. Bottom line (read this first)

1. **Breadth beats depth.** For a fixed budget, more distinct tasks with fewer rows each wins on held-out tasks. This holds in every study I found (Super-NI, Flan 2022, T0, Zhang 2024, Only-IF).
2. **The thresholds.** Held-out accuracy grows log-linearly with the number of distinct tasks, up to 1,836 tasks for a 3B model (Flan 2022). Gains per task flatten after about 64 rows per task (Super-NI). In a controlled study, fewer than 300 distinct instructions never generalized and 1,000 or more always did (Zhang 2024).
3. **Small models need more task variety, not less.** With about 40 tasks, instruction tuning *hurt* held-out accuracy at 8B and below (FLAN 2021). With 1,800+ tasks, 3B models kept improving (Flan 2022).
4. **Many wordings per task.** Training on more prompt wordings per dataset raised held-out medians (T0: 8 of 11 datasets going from 1 to 5.7 prompts per dataset). It matters most for small models: +1.9 to +5.6 ROUGE-L on average, and much larger worst-case gains, for Qwen3-0.6B, Qwen3-8B and Llama-1B (Sadrieh & Štefánik, Sep 2026).
5. **Make the model read the definitions.** Models lean on label *names*, not definitions (Codebook LLMs test). Fixes that worked: label-name masking, class dropout, definition paraphrase, and example instances inside definitions. Together they took GoLLIE from 42.3 to 55.3 F1 on unseen schemas.
6. **Balance the mixture.** Removing mixture balancing cost Flan-T5-XL 4.9 MMLU points and 11.1 BBH points. A long-tailed task distribution acts like having fewer tasks (Zhang 2024).
7. **Contrast pairs and ambiguous rows beat easy bulk.** Counterfactual twins gave +3.6 to +5.1 points out of domain at the same data size (Kaushik 2020). A 33% "ambiguous" subset beat 100% of the data on an OOD test (Dataset Cartography).
8. **Fancy invariance losses add little over simple data variety.** Consistency and contrastive losses (PPCL, CoIN) "often fail to outperform" plain multi-template training (2026). Domain-adversarial and other domain-generalization algorithms rarely beat plain training (ERM) by more than 1 point (DomainBed). The one strong exception is weight-space interpolation (WiSE-FT): +2 to +10 points out of distribution, and that is our step B.
9. **Our dev gate overstates far-domain transfer.** Leave-one-dataset-out testing was 8 to 16.5 AUC points below normal cross-validation (2026). Fine-tuned small models win in-distribution, but LLMs prompted with examples win out of distribution (BOSS). Our pattern fits both: dev +2.5, ejs-5 −0.4.
10. **Recommended mix for C (details in §4).** ≥1,500 distinct task cards in the ~90K own rows (about 40–60 rows each). At least 5 wordings per card and a pool of about 400 format styles. Cap every public dataset at about 3,000 rows and 500 rows per class. Flatten the replay. Put about 20–25% of own rows in contrast twins, 10–20% in inverted form and 5–10% in few-shot form. Also use 10–20% label masking and swaps, and keep step B (WiSE-FT).

---

## 1. Direct answer: what mix of tasks vs examples per task maximizes held-out-domain accuracy?

### 1.1 Evidence table (numbers as reported)

| Study | Setup | Tasks vs rows result |
|---|---|---|
| Super-NaturalInstructions / Tk-Instruct (Wang et al. 2022) | T5, 757 train tasks, 119 unseen eval tasks | 6→757 training tasks: ROUGE-L 43.7→54.3, log-linear. Rows per task: performance **saturates at 64 rows per task** (54.7) and more rows do not help. A T5-Large with 757 tasks (48.0) matches a T5-3B with 128 tasks (48.4). |
| Flan Collection (Longpre et al. 2023) | T5 Small→XXL, 8→1,836 tasks | Held-out MMLU grows **log-linearly up to all 1,836 tasks**. Only T5-Small peaks earlier. Held-in tasks peak near 200 tasks. |
| Flan-PaLM (Chung et al. 2022) | 8B / 62B / 540B, 9→1,836 tasks | 8B normalized average: 9 tasks 8.3 → 89 tasks 14.8 → 282 tasks 20.5 → 1,836 tasks 21.9. Most of the gain came by 282 tasks. Note: 9 narrow tasks *dropped* 8B BBH-direct from 30.8 to 19.8. |
| FLAN (Wei et al. 2021) | 137B, task clusters | More clusters improved held-out clusters. One vs four datasets per cluster: **about +10%**. 1, 4 or 10 templates per dataset: negligible effect at 137B. At ≤8B, tuning on about 40 tasks *hurt* held-out tasks ("capacity" explanation). |
| T0 (Sanh et al. 2021) | 11B, 39–55 datasets | Prompts per dataset 1 → 5.7 → 8.03: the median rose for 8/11 and then 9/11 held-out datasets, and the spread fell for 7/11 and then 8/11. Datasets 39→49→55: the median rose on all 5 tested. Non-original-task prompts (e.g., "given the answer, write the question") also helped. |
| Instruction Diversity Drives Generalization (Zhang et al. 2024) | Controlled string rewriting, fixed 10^6 rows | **<300 instructions never generalize; ≥1,000 always do**, even with only a few rows each. Sharp transition around 400–500 instructions. A long-tailed (power-law) row distribution hurts models near the threshold. Semantically narrow rule sets do not generalize to broad ones. |
| Only-IF (2024) | Code specialist (DeepSeek-Coder-6.7B, CodeQwen-7B) and generalist | Specialist: 15K core + 5K extra. Mixing 3K general + 2K CoT gave avg 67.1 vs 64.2 for 20K core-only (+4.6% relative). At 75K, the best mix gave 68.4 vs 66.4. **Peaked curve**: in their runs, about 20–25% of the budget as diverse out-of-domain data worked best, and more off-core data past the peak hurt. Generalist at a 40K total budget: mixed 47.59 vs 41.01 single-source. |
| Universal NLI classifier (Laurer et al. 2023) | DeBERTa-v3, 33 datasets, 389 classes | Held-out (leave-dataset-out) zero-shot **+9.4%** vs NLI-only. Caps used: **≤500 rows per class, ≤5,000 per dataset**. Some negative transfer: on a few datasets the mix made the model over- or under-predict classes. |
| FLAN mixing rule | — | ≤30K rows per dataset, examples-proportional mixing with a **max mixing rate of 3K**. |
| Expert LMs (Jang et al. 2023) | T0-3B | A *single-task* expert beat a 300+ task multitask model by 3.20% on 11 unseen datasets. **Diversity is not free**: negative transfer is real, and relevance and quality matter. |

### 1.2 What this means for a 4B decision model

- Count **distinct task cards**, not rows. A card is one decision schema: the rule or label set, the domain, and the wording family. Rows per card past about 50–64 buy little held-out accuracy.
- A 4B model is in the zone where Flan 2022 still gains from 1,800+ tasks. Our C1 has about 173 sources, which is far below that zone. Going to about 1,500–2,000 cards is about 3.2–3.5 doublings. The literature gives roughly +1 to +2 points per doubling of tasks early on, then less (Super-NI ~1.5 ROUGE-L per doubling; Chung 8B +1.4 normalized from 282 to 1,836). This is **a prior, not a promise**: those were new *tasks*, and ours are new *domains* within known skill families.
- Keep a core. Only-IF shows a peak, and too much off-core variety hurts the specialist. Our core is decision skills with a letter readout. Variety should come from domains, rules and wordings *inside* that core, not from off-core tasks like generation.
- Balance. Flatten long tails. Flan without mixture balancing: Held-In −2.6, MMLU −4.9, BBH −11.1 (T5-XL, zero-shot).

---

## 2. Evidence by topic

### 2.1 Label-description / definition-reading training
- **LabelDescTraining** (Gao, Ghosh, Gimpel, EMNLP 2023): fine-tuning only on short *descriptions of labels* (no real inputs) beat zero-shot by about 15–19 points absolute (abstract says 15–17, text says 17–19) on topic and sentiment tasks. It was also more robust to prompt pattern and verbalizer choice, and it transferred across text domains.
- **GoLLIE** (ICLR 2024): fine-tuned to follow annotation guidelines. Zero-shot F1 on unseen schemas was **42.3 (baseline) → 55.3**. Ablations (F1): without representative candidates (example instances in each definition) 49.9; without class dropout 54.0; without class-name masking 54.6; without guideline paraphrases 54.8; without class-order shuffling 55.9 (shuffling did not help there). So **examples inside definitions** mattered most.
- **Codebook LLMs** (Halterman & Keith, Political Analysis 2025): open 7–12B models did worse when label names were replaced with generic tags (LABEL_1) or swapped between definitions. This shows they rely on label *names* more than definitions. They also failed "exclusion criterion" minimal pairs. QLoRA instruction tuning on codebook data raised Mistral-7B from 0.53 to 0.82 weighted F1 (+55% relative). Gains on long documents were small.
- **Super-NI instruction elements**: Definition + 2 positive examples was among the best encodings (54.3). Explanations *lowered* scores for these model sizes. A model trained on examples only scored 22.1 on definition-only tests (vs 45.0 for a definition-trained model). A model trained on definitions only scored 31–38 on example-only tests (vs 44–50 for example-trained models). **Models trained on mixed encodings were robust to all of them.**
- **Kung & Peng 2023**: models trained on definitions stripped down to just the output space did about as well as models trained on full definitions. A random-guess-with-right-format baseline scored 42.6% exact match vs 43% for instruction tuning on low-resource classification. Instruction tuning often learns **format and label space**, not instruction meaning. **Webson & Pavlick 2022**: models learn as fast from irrelevant or misleading templates as from good ones.

Takeaway for C: definitions must be *necessary* to get the answer right. Use invented jargon, swapped names and masked names, and rules that override the prior meaning of a label word. Otherwise the model learns to ignore the card.

### 2.2 Instruction paraphrase and format augmentation; prompt sensitivity
- **Sclar et al. (ICLR 2024)**: up to **76 accuracy points** of spread across plausible formats (LLaMA-2-13B, few-shot). The spread survives larger models, more shots and instruction tuning.
- **Sun, Shaib, Wallace (ICLR 2024)**: semantically equivalent but *unseen* instruction wording cost Flan-T5-XXL **6.9 points** on average. A consistency objective helped "consistently but modestly."
- **Sadrieh & Štefánik (arXiv 2609.01217, Sep 2026)**: T0 split (48 training datasets, 11 unseen-task datasets), PromptSource templates, cap 10,240 rows per dataset. Models: Qwen3-0.6B, Qwen3-8B (LoRA), Llama-3.2-1B and Llama-3.1-8B (LoRA). Results:
  - Multi-template training vs single template: average ROUGE-L **+1.9 to +5.6** for three of the models (data-construction strategies), and −0.4 to +0.9 for Llama-3.1-8B.
  - Worst-template score: Qwen3-0.6B 0.308→0.449; Llama-1B 0.210→0.363 (one template per batch).
  - **One template per batch** was most reliable. Putting all templates of one example in the same batch caused gradient sign conflicts on 57–64% of weights, which hurt best-case scores.
  - Consistency (PPCL) and contrastive (CoIN) losses were "mostly matched or outperformed" by simple data construction. Their training-time gains did not carry over to held-out tasks.
  - Even the best method left a **40–57% best-to-worst gap**.
- **PAFT (EMNLP 2025)**: trained on 400 LLM-written prompt variants and tested on 50 unseen ones. Mean accuracy was +1.4 to +5.8 over the best baselines, and the spread across prompts shrank from ±1.7–8.0 to ±0.6–2.2.
- **Flan Collection**: mixing in **≥5% few-shot templates** "dramatically" improved zero-shot. Both zero-shot and few-shot peaked at 10–90% few-shot. Removing few-shot templates cost 3.0 zero-shot MMLU points and 13.7 few-shot MMLU points. **Input inversion** (swap input and output roles, mixed at a 30% rate) was the single biggest held-out lever. Removing it cost **8.6 MMLU and 7.8 BBH** zero-shot points.
- **Mixture of Formats** (NAACL-SRW 2025, prompting only): diverse format styles in the examples cut format-induced spread, e.g., by 46% on one task (Llama-2-13b).

### 2.3 Invariance / consistency training
- **Swarm distillation** (Zhou et al. 2022) applies prompt consistency on *unlabeled* inputs of a new task. It beat T0-3B on 9 of 11 datasets, with up to +10.6 points (RTE).
- **BCT** (Chua et al. 2024, GPT-3.5-Turbo): consistency between clean and bias-augmented prompts. Biased reasoning fell by 86% on held-out tasks and by 37% on average on held-out bias types.
- **But** (2026): in a controlled comparison, consistency regularization did not beat simple template variety on held-out tasks.
- **Our code** already has complement / equiv / inv relation losses, keeps related rows in the same batch, and re-shuffles options every draw (`train_decoder.py` docstring). The literature says the *data* part (twins, paraphrases) carries most of the value. The *loss* part needs a sealed-suite ablation before we trust it for far domains.

### 2.4 Domain-adversarial and domain-generalization algorithms
- **DomainBed** (Gulrajani & Lopez-Paz, ICLR 2021): with fair tuning, **no algorithm beat ERM by more than 1 point** on average. That includes DANN (domain-adversarial).
- **AFTER** (domain-adversarial fine-tuning, Vernikos et al. 2020): +0.7 to +3.2 points, but *in-domain* (GLUE-style tasks), not on new domains.
- **When Benchmarks Lie** (arXiv 2602.14161, 2026): normal cross-validation reported a pooled AUC **8.0–16.5 points higher** than leave-one-dataset-out (per-dataset gaps of 1–25 points). A probe could guess the source dataset with 96.6% accuracy, and 28–44% of the top features were shortcuts. Adversarial training, subspace projection, reweighting and class balancing **failed to close the gap**.
- Takeaway: skip domain-adversarial losses. Use "domain randomization in the data" instead: invented domains, invented jargon and many surface styles. Use a dataset-identity probe only as a shortcut *diagnostic*.

### 2.5 Hard negatives / close distractors / contrast sets
- **Counterfactually augmented data** (Kaushik et al., ICLR 2020), BERT trained on 3.4K rows: originals + 1:1 human-edited label-flipping twins vs 3.4K originals alone. Out of domain: Amazon **85.1 vs 80.0**, Twitter **82.9 vs 79.3**, Yelp **89.4 vs 85.3**. For NLI, augmented SNLI did *not* generalize better (Huang et al. 2020). Gains are biggest when the label-flipping edit is the true cause of the label.
- **Dataset Cartography** (Swayamdipta et al., EMNLP 2020), RoBERTa-large on WinoGrande. 100% of the training data: ID 79.7 / WSC (OOD) 86.0. The 33% most **ambiguous** rows (high variability across epochs): ID 78.7 / OOD **87.6**. "Hard-to-learn" rows are often **mislabeled**.
- **AFLite** (Le Bras et al., ICML 2020): training on adversarially filtered data (artifacts removed) generalized better out of domain. Exact numbers not extracted (unknown).
- **Contrast-set fine-tuning** (arXiv 2501.02683, ELECTRA-small, a single-author preprint, so weak evidence): contrast-set accuracy rose from 75% to about 90% while SNLI stayed at about 90%.
- **Option-position bias**: LLMs prefer certain option IDs, mostly because of *token* bias toward the ID letters and partly because of position (Zheng et al., ICLR 2024). PriDe removes this prior at inference without labels. PA-GRPO (ACL 2026) trains for consistency across option permutations. We already re-shuffle options. A letter-prior check on the sealed suite is cheap.

### 2.6 Why fine-tuned models overfit familiar task families
- **Capacity**: small models fill their capacity with the training tasks (FLAN 2021, ≤8B hurt). With 9 narrow tasks, 8B BBH-direct fell from 30.8 to 19.8 (Chung 2022).
- **Format specialization** (ProMoT, ICLR 2024): single-task fine-tuning overfits the task *format* very early in training and loses in-context ability on other formats.
- **Superficial patterns**: the model learns the output space and guessing, not the instructions (Kung & Peng; Webson & Pavlick).
- **Feature distortion** (Kumar et al., ICLR 2022, LP-FT): across 10 shifts, full fine-tuning was +2% in-distribution but **−7% out-of-distribution** vs a linear probe. Fine-tuning changes features only along the training-data directions.
- **Dataset shortcuts** (When Benchmarks Lie): the model learns "which dataset is this" features.
- **Accuracy-on-the-line** (Miller et al., ICML 2021): ID and OOD accuracy usually move together, but the line can break under some shifts. Our dev→ejs-5 result looks like a broken line. The dev gate is "unseen source" but the *same families*. ejs-5 is a new family and a new surface.
- **BOSS** (NeurIPS 2023 D&B): fine-tuned small models win in-distribution, and prompted LLMs win on OOD instances. That is the same split as C1 vs Jev.
- **SFT vs RL** (Chu et al., ICML 2025): on rule-variant tasks with multi-step generation, RL gave up to +11% out of distribution and SFT fell by up to −79.5%. Whether this holds for a *single-token* readout is **unknown**. It is not a priority inside this plan.

### 2.7 Keeping the gains: weight-space and anchor methods
- **WiSE-FT** (Wortsman et al., CVPR 2022): linear interpolation between the original and fine-tuned weights. OOD **+2 to +10 points** on five ImageNet shifts, and +2 to +23 on six others, with ID about +1. For LoRA, scaling the adapter by a ∈ (0,1) is *exactly* this interpolation. That is our step B (a = 0.6–0.9).
- **LoRA learns less and forgets less** (Biderman et al., TMLR 2024): LoRA and full fine-tuning lie on the same learn-vs-forget curve. Low rank gives less forgetting at matched learning only in some cases.
- **Forgetting scaling law** (arXiv 2502.06042): injecting just **1% pretraining data** into fine-tuning stopped forgetting of the pretraining set. Our 60% replay plus the KL anchor is probably far above what forgetting needs. It mainly protects C1's specific skills.

### 2.8 Inference-time levers with no training (single pass kept)
- **Domain-context calibration** (Fei et al., ACL 2023): up to **+37 macro-F1** on tasks with large domain-label bias (GPT-J / GPT-3 in-context learning).
- **Batch Calibration** (Zhou et al., ICLR 2024): inference-only and nearly free. Tested on PaLM 2 and CLIP across 10+ tasks; exact gains not extracted (unknown). We already have `batchcal.py` (per-task label prior from unlabeled questions, used when there are ≥20 questions per task). A per-card running prior in serving is an option for far domains with shifted label priors (possibly ejs-5). It must be judged on the sealed suite only.

---

## 3. Our C1 pattern, explained by the literature

| Our fact | Best-matching evidence | Implication |
|---|---|---|
| Dev +2.5 (C1 vs 4B-E) but ejs-5 −0.4 and −4.4 vs Jev | When Benchmarks Lie (CV overstates by 8–16.5 AUC); BOSS; broken accuracy-on-the-line | The dev gate measures the *same families*. A leave-family-out dev split is needed to see real transfer. |
| 173 sources, 502K rows | Flan/Super-NI/Zhang: breadth > depth; 4B still gains up to ~1,800 tasks | Our task count is the main limit, not our row count. |
| Hard / negated yes/no 47.4 vs 57.9; 0.34% double-negation rows | CAD twins; Codebook exclusion minimal pairs; cartography | Rare skills need explicit contrast twins spread across *many* cards, not one source. |
| Wins on in-family classification (BANKING77, CLINC, ContractNLI) | Fine-tuned small models win ID (BOSS) | Keep the replay and the anchor. Do not trade these wins away. |
| Letter readout over shuffled options | PriDe token bias; PA-GRPO | Already mitigated by shuffles. Add a letter-prior audit on the sealed suite. |

---

## 4. Concrete recommendations for the C dataset (this angle only)

Numbers are starting points backed by §1–2. "Own" means Claude-authored, program-labelled rows.

**A. Task-card breadth (the biggest lever)**
1. Target **≥1,500 distinct task cards** across the ~90K own rows (≈40–60 rows each). Aim for ≥120 cards per skill family × 12 families. Each card gets its own invented or real domain, its own rule or label schema, and its own label names. Evidence: Zhang (≥1,000), Super-NI (64/task saturation), Flan (log-linear to 1,836).
2. Rows per card: **median about 50, max about 120**. Do not let any family exceed about 12% of own rows. Evidence: long tails shrink effective diversity (Zhang). Mixture balancing: −4.9 MMLU and −11.1 BBH without it (Flan).
3. Public commercial training splits: **cap at about 3,000 rows per dataset and 500 rows per class** (FLAN max mixing 3K; Laurer 500/class and 5K/dataset). Prefer more datasets over more rows. Give each dataset ≥3 instruction wordings.
4. Replay of C1's 500K: sample with a per-source cap or a square-root flattening (UniMax-style capped repeats) instead of raw proportions. Rely on the KL anchor to keep C1 behaviour. Check the dev gate for any drop on the head sources.
5. Track a **diversity metric** for each build: count of unique cards and unique wordings, plus an embedding novelty score. NovelSum correlated with instruction-tuning results at r = 0.97–0.98 (ACL 2025).

**B. Wording and format variety**
6. **≥5 instruction wordings and ≥3 definition styles per card**, drawn from a global pool of **about 400 format styles** (PAFT used 400). Styles cover headings vs prose, bullet vs table definitions, label order, option count, card length and instruction position. **Hold out ≥50 styles** that appear only in the sealed suite, so unseen-format accuracy can be measured.
7. **5–10% few-shot cards** (1–3 worked examples inside the card). Flan: ≥5% few-shot templates improved zero-shot. Super-NI: definition plus examples was the most robust encoding.
8. **10–20% input-inverted cards**: "which of these situations meets rule X?", with options being texts. The same letter readout works. Flan's biggest held-out lever (−8.6 MMLU without it), mixed there at 30%.
9. Batching: avoid packing many paraphrases of the *same* item into one step (gradient conflict, 2026). Keep relation twins together, because the losses need it, but limit each item to at most 2–3 variants per step.

**C. Force definition reading**
10. **Class-name masking** on 10–15% of choice rows (neutral IDs such as "Category K7" with the definition kept). **Swapped-name rows** on about 5%: familiar label words paired with *different* definitions, so the gold answer follows the definition. Evidence: GoLLIE masking (−0.7 F1 without); Codebook swap and generic-label failures.
11. **Class dropout**: randomly drop non-gold options (4+ option cards) so schemas vary. If the gold option is dropped, the program must relabel the row, e.g., to not-enough-information.
12. **1–2 representative instances inside each label definition** for about 50% of cards. This was GoLLIE's largest single component (−5.4 F1 without).

**D. Contrast and difficulty**
13. **20–25% of own rows as minimal-pair twins**: one fact, negation or condition changed, and the label flips (CAD used 1:1 pairs). Spread twins over *all* families and many cards, not one "negation source". The 0.34% double-negation share in C1 is the counter-example to avoid.
14. **Close distractors**: every choice card has ≥1 option that differs from the gold option by one condition.
15. **Difficulty selection with C1 as a scorer, not a labeler**: run C1 on candidate rows and keep extra rows where C1 is wrong or unsure (cartography: the ambiguous third gave the best OOD). Send C1's "hard-to-learn" rows to a program-bug audit first, because they are often label errors.

**E. Training-side (only what this angle supports)**
16. Keep **step B (WiSE-FT / LoRA scaling)**. It is the best-evidenced OOD lever outside data.
17. Keep relation losses **only if** a sealed-suite ablation shows a gain. The 2026 evidence says they add little over data variety on held-out tasks.
18. Skip domain-adversarial losses, IRM-style objectives and contrastive representation losses (DomainBed ≤1 point; LODO paper: failed).
19. Optional, low priority: a small prompt-token LM loss (Weighted Instruction Tuning: optimal prompt weight was non-zero in 56% of 75 settings, but all of them were *generation* tasks). Effect on a single-token readout: unknown.

**F. Measurement (so we see real transfer)**
20. Build a **leave-family-out dev split** in addition to the unseen-source gate. Report mean **and worst-format** accuracy.
21. Add behavioral tests from Codebook LLMs: **generic-label accuracy, swapped-label accuracy, exclusion minimal pairs**. Also add a **permutation-consistency rate** and a **letter-prior** check.
22. Optionally, a dataset-identity probe on hidden states. If it reaches >90% source accuracy, shortcuts are likely (96.6% in the 2026 paper).

---

## 5. Expected effects (a prior, not a promise)

These are rough ranges for the **sealed new-domains suite**, carried over from different setups. Confidence is low to medium. Effects overlap and will not simply add up.

| Lever | Literature effect | Plausible effect for C | Confidence |
|---|---|---|---|
| 173 → ≥1,500 task cards | ~+1–2 points per task doubling early, smaller later | +1 to +3 | medium |
| Wording/format variety (≥5 per card, 400 styles) | mean +2–6; worst-case +10–15 | mean +0.5 to +2; worst-format +5 or more | medium |
| Input inversion + few-shot cards | Flan: 3–9 points held-out | +0.5 to +1.5 | low |
| Definition-reading regularizers | GoLLIE +13 F1 total (from a weak baseline) | +0.5 to +2 | low–medium |
| Contrast twins / close distractors | +3.6 to +5.1 OOD (sentiment); ~0 (NLI) | overall +0.5 to +1.5; hard yes/no subset +5 to +10 | medium |
| Step B WiSE-FT | +2 to +10 OOD (vision) | +0 to +2 | medium |
| Calibration at serving | up to +37 macro-F1 on biased tasks (ICL) | 0 to +2 on label-shifted domains | low |

Rough total on far domains: **+2 to +5 points** over C1 if the data is clean, with wide uncertainty. On ejs-5 specifically, commit data from other repos is a *target-related* task (task-similarity selection helps; numbers for INSTA unknown). Closing the −4.4 gap is plausible but not assured. Expect a range of about −2 to +3 vs Jev.

---

## 6. Unknowns and cautions
- Most task-scaling studies count new *tasks*. Transfer to new *domains* within known skills may be larger or smaller (unknown).
- Most format-robustness studies use generation metrics (ROUGE-L). The effect on a calibrated single-token readout is unknown, but likely in the same direction.
- RL vs SFT for single-token decisions: unknown.
- Jang 2023 shows negative transfer from badly chosen tasks. Every new family should pass a dev check before scaling.
- Licences: all evidence papers are research. Using a *method* has no licence issue. Training data must still pass the commercial-licence allow-list.

---

## Sources
- Super-NaturalInstructions / Tk-Instruct — https://arxiv.org/abs/2204.07705 (ACL: https://aclanthology.org/2022.emnlp-main.340/)
- Flan Collection (Longpre et al. 2023) — https://arxiv.org/abs/2301.13688
- Scaling Instruction-Finetuned LMs (Chung et al. 2022) — https://arxiv.org/abs/2210.11416
- FLAN (Wei et al. 2021) — https://arxiv.org/abs/2109.01652
- T0 (Sanh et al. 2021) — https://arxiv.org/abs/2110.08207
- Instruction Diversity Drives Generalization (Zhang et al. 2024) — https://arxiv.org/abs/2402.10891
- Only-IF (2024) — https://arxiv.org/abs/2410.04717
- Universal NLI classifiers (Laurer et al. 2023) — https://arxiv.org/abs/2312.17543
- Expert LMs vs instruction tuning (Jang et al. 2023) — https://arxiv.org/abs/2302.03202
- Do Models Really Learn to Follow Instructions? (Kung & Peng 2023) — https://arxiv.org/abs/2305.11383
- Do Prompt-Based Models Understand Their Prompts? (Webson & Pavlick 2022) — https://aclanthology.org/2022.naacl-main.167/
- Label-Description Training (Gao et al. 2023) — https://arxiv.org/abs/2305.02239
- GoLLIE (Sainz et al. 2024) — https://arxiv.org/abs/2310.03668
- Codebook LLMs (Halterman & Keith 2025) — https://arxiv.org/abs/2407.10747
- FormatSpread (Sclar et al. 2024) — https://arxiv.org/abs/2310.11324
- Zero-shot robustness of instruction-tuned LMs (Sun et al. 2024) — https://arxiv.org/abs/2306.11270
- Prompt-Robust LMs: Which Training Strategies Work? (Sadrieh & Štefánik, Sep 2026) — https://arxiv.org/abs/2609.01217
- PAFT (2025) — https://arxiv.org/abs/2502.12859
- Mixture of Formats (Ngweta et al. 2025) — https://aclanthology.org/2025.naacl-srw.51/
- Prompt Consistency / swarm distillation (Zhou et al. 2022) — https://arxiv.org/abs/2205.00049
- Bias-augmented consistency training (Chua et al. 2024) — https://arxiv.org/abs/2403.05518
- Consistency training vs sycophancy/jailbreaks (2025) — https://arxiv.org/abs/2510.27062
- ProMoT, format specialization (Wang et al. 2024) — https://arxiv.org/abs/2211.00635
- LP-FT, feature distortion (Kumar et al. 2022) — https://arxiv.org/abs/2202.10054
- WiSE-FT (Wortsman et al. 2022) — https://arxiv.org/abs/2109.01903
- LoRA Learns Less and Forgets Less (Biderman et al. 2024) — https://arxiv.org/abs/2405.09673
- Scaling laws for forgetting with pretraining-data injection (2025) — https://arxiv.org/abs/2502.06042
- DomainBed (Gulrajani & Lopez-Paz 2021) — https://arxiv.org/abs/2007.01434
- AFTER, domain-adversarial fine-tuning (Vernikos et al. 2020) — https://arxiv.org/abs/2009.13366
- When Benchmarks Lie, LODO (2026) — https://arxiv.org/abs/2602.14161
- BOSS OOD benchmark (Yuan et al. 2023) — https://arxiv.org/abs/2306.04618
- Accuracy on the Line (Miller et al. 2021) — https://proceedings.mlr.press/v139/miller21b/miller21b.pdf
- Counterfactually augmented data (Kaushik et al. 2020) — https://arxiv.org/abs/1909.12434
- CAD for SNLI does not help OOD (Huang et al. 2020) — https://openreview.net/pdf?id=CSRgLEqVeLZ
- Dataset Cartography (Swayamdipta et al. 2020) — https://aclanthology.org/2020.emnlp-main.746/
- AFLite (Le Bras et al. 2020) — https://arxiv.org/abs/2002.04108
- Contrast-set fine-tuning (2025, weak) — https://arxiv.org/abs/2501.02683
- LLMs are not robust MC selectors / PriDe (Zheng et al. 2024) — https://arxiv.org/abs/2309.03882
- PA-GRPO (2026) — https://arxiv.org/abs/2603.21016
- SFT Memorizes, RL Generalizes (Chu et al. 2025) — https://arxiv.org/abs/2501.17161
- Domain-context calibration (Fei et al. 2023) — https://arxiv.org/abs/2305.19148
- Batch Calibration (Zhou et al. 2024) — https://arxiv.org/abs/2309.17249
- UniMax sampling (Chung et al. 2023) — https://arxiv.org/abs/2304.09151
- NovelSum diversity metric (ACL 2025) — https://arxiv.org/abs/2502.17184
- Weighted Instruction Tuning (2025) — https://arxiv.org/abs/2507.07817
- INSTA task selection (Lee et al. 2024) — https://aclanthology.org/2024.emnlp-main.1036/
- Generalization of fine-tuned LLMs (Yang et al. 2024) — https://aclanthology.org/2024.naacl-long.51/
- Controlling OOD gaps for genre classification (2024) — https://arxiv.org/abs/2412.20595
