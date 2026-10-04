# RESEARCH_EXTRA_4: Gradient, influence and target-aware selection vs random + diversity

Date: 3 Oct 2026. Targeted research 4 for C. CPU only, 18 web fetches/searches, no paid calls.
Read-only use of `C_DATA_SPEC.md` and `C_TRAIN_RECIPE.md` (not edited). Sources are listed at the end.
"Estimate" marks our own arithmetic. "Hypothesis" marks a mechanism we inferred but have not tested.

---

## 0. Bottom line

1. **The big wins from smart selectors come from keeping only 1-5% of a pool, scored on a test that matches the target.**
   C keeps about 67% of its own generated rows (spec 2.1 generates 1.5x the target). Even LESS's own follow-ups show it
   falls **below random** at 10-15% budgets (BIDS Table 1). Expected gain for C's own rows: about 0.
2. **At scale, random is hard to beat.** On 1M-row pools, no selector beat random significantly (all p > 0.05;
   2410.09335). On a 5.8M pool, 4 of 7 methods got **worse** as the pool grew (Ivison et al. 2025).
3. **Target-aware selection overfits the target's answer format.** Gradient attribution tracks answer format,
   not task. LESS selections "over-represent the target's own answer format" (2609.19589). For our letter readout,
   this means option count and the yes/no shape. With C1 leaning "yes", a target gradient also pushes toward the
   gold-"no" side (hypothesis, section 3.2). Methods S8 already found this risk for difficulty selection.
4. **No paper we found shows that gradient-targeted selection improves accuracy on unseen domains over random +
   diversity.** The closest result: Ivison used non-eval queries (Arena Hard) as targets and lost only 0.5 points
   (50.4 vs 50.9). That shows the targets don't need to be the eval. It doesn't show unseen-domain gains over random.
   **So whether this helps unseen domains is unknown. For C, the likely gain is 0 or negative.**
5. **Recommendation:** keep spec 2.1's stratified selection for own rows and replay. Do not add LESS, influence or
   IFD selection in round 1 or round 2. Only use diversity (facility location on C1's own hidden states) where the keep
   ratio is low and diversity is not built in: the licensed public pools. Any target-aware selection would need a
   new, separate selection-target split (section 4) and pre-registration before any C data exists.

---

## 1. Evidence table

| Method (paper) | Setting | Keep ratio | Result vs random / full | Source |
|---|---|---|---|---|
| **LESS** (LoRA-gradient cosine to few-shot target, Adam train grads, SGD target grads, 8,192-dim random projection, 4 warm-up checkpoints) | Llama-2-7B; pool about 270K (Flan v2, CoT, Dolly, OASST1); targets: MMLU 285, TydiQA 9, BBH 69 examples | **5%** | MMLU 50.2 vs random 46.5 vs full 51.6. TydiQA 56.2 / 52.7 / 54.0. BBH 41.5 / 38.9 / 43.2. Baselines on MMLU: BM25 47.6, DSIR 46.1, RDS 45.0 | [2402.04333](https://arxiv.org/abs/2402.04333) Tables 2-3 |
| LESS transfer (LESS-T) | Llama-2-7B selects for Llama-2-13B | 5% | TydiQA 57.5 vs full 54.3 | same |
| LESS cost | 270K pool | | 66 h warm-up + 48 h gradient features, selection < 1 min, **17.7 GB** datastore (GPU type not captured in our fetch) | same, Table 4 |
| LESS limitation (own text) | | | "Minimizing loss does not monotonically increase performance". Inner product is biased by completion length, so it uses cosine | same |
| **BIDS** (LESS + per-target column normalization + iterative selection) | Llama-3-8B; UltraInteract; 7 targets (HumanEval, MBPP, BBH, MMLU, GSM-Plus, MATH, IFEval) | 5 / 10 / 15% | Macro avg, LESS vs random: **43.9 vs 43.4; 44.4 vs 44.9; 45.2 vs 45.7** (LESS below random at 10% and 15%). LESS hurts BBH vs random by 2.1-3.0 pts (62.7 vs 64.8; 62.0 vs 65.0; 63.2 vs 65.2). BIDS 44.6 / 46.0 / 46.1; full 1 epoch 46.9. RDS, S2L and DEITA **below random at every budget** | [2501.12147](https://arxiv.org/abs/2501.12147) / [EMNLP-F 2025](https://aclanthology.org/2025.findings-emnlp.373.pdf) Tables 1-2 |
| BIDS on Mistral-7B | same | 5 / 10 / 15% | Random 40.2 / 41.0 / 41.4; LESS 41.0 / 41.4 / 41.8; BIDS 41.0 / 42.5 / 42.6 | same, Table 3 |
| **Rethinking selection at scale** | Llama3-8B, Qwen2-7B; OpenHermes2.5 (>1M), WildChat-1M; picks 10K / 50K | about 1-5% | OpenHermes 10K (Llama3-8B): random about 52.9; LESS 50.79; IFD 48.69; SelectIT 51.79; entropy 47.59. None above random (p > 0.05). "Diversity ... more significant than quality". Token-length filter: 56.23, and on WildChat 55.51 vs full 54.58. DiverseEvol and DQ needed > 1 TB RAM | [2410.09335](https://arxiv.org/abs/2410.09335) |
| **RDS+** (cosine on the model's own pooled hidden states) at scale | Tulu 2 unfiltered 5.8M; 10K single-task, 326K multi-task | 0.2% / 5.6% | 10K from 5.8M: RDS+ **50.5** vs best other (GTR embed) 46.4. Pool 200K to 5.8M: RDS+ 46.4 to 50.5; IFD 38.7 to 35.8; PPL-top 34.2 to 30.4. LESS at 200K: 44.2 (too costly to run at 5.8M). Multi-task round-robin **50.9 vs mean-max 47.9**. Non-eval queries (Arena Hard) as targets: 50.4 vs 50.9. RDS+ beat the hand-built Tulu 2 mix 49.5 | [2503.01807](https://arxiv.org/abs/2503.01807) |
| **Influence Distillation** (2nd-order, JVP embeddings from first 4 blocks, 4,096 random landmarks) | Llama2-7B, Llama3.2-3B, Qwen2.5-1.5B/3B; 10K of 200K Tulu V2; 6 targets with 8-500 examples | 5% | Over uniform: Llama2-7B **+2.30** (RDS+ +1.85); Qwen2.5-1.5B **+6.52** (RDS+ +4.28). Selection cost 872 TFLOPs vs RDS+ 2,800 (up to 3.5x faster) | [2505.19051](https://arxiv.org/abs/2505.19051) |
| **TSDS** (optimal-transport match + kernel-density diversity term) | task-specific fine-tuning | **1%** | Often beats full data; +1.5 F1 over baseline selectors on average. Built because top-k similarity picks **near-duplicates** | [2410.11303](https://arxiv.org/abs/2410.11303) |
| **QDIT** (facility-location diversity + quality, greedy, alpha trade-off) | Alpaca 52K, Dolly 15K, Ultrachat 1.3M, LMSYS 1M, Mixed 270K; pick 1K-10K | about 1-20% | Ultrachat 10K, worst-10% HH score: random 2.620, quality-only 3.405, QDIT 3.497. Average HH +11.6% vs random. Quality-only **hurt worst case vs random in 2 of 5 settings**. Best alpha in {0.5, 0.7, 0.9}; alpha 0.1 and 1.0 both drop. Selecting from millions takes "a few hours" (lazy greedy + subsampling) | [2311.14736](https://arxiv.org/abs/2311.14736) |
| **IFD / Cherry LLM** (conditioned answer loss / unconditioned answer loss) | Alpaca, WizardLM | 5-10% | 10% beats full data. **IFD > 1 = misaligned or noisy; exclude** | [2308.12032](https://arxiv.org/abs/2308.12032) |
| **LIMO** | Qwen2.5-32B-Instruct; tens of millions of problems, then 2,125, then **800** | about 0.001% | OOD avg 78.1 vs OpenThoughts-114k 58.3, NuminaMath-100k 32.3. Advanced-500 51.5 vs Simple-500 35.5 on AIME24. 400 rows: 57.5. Base model matters: Qwen1.5-32B 9.2 vs 63.3. Difficulty set by a **32B** model (1-3 of 32 correct) and long chains from stronger models | [2502.03387](https://arxiv.org/abs/2502.03387) |
| **Form over content** | gradient attribution across checkpoints, scales and families | n/a | Benchmarks with the same answer format: gradient cosine about 0.4. Same benchmarks in different formats: about **0.0**. LESS picks over-represent the target's own answer format | [2609.19589](https://arxiv.org/abs/2609.19589) (2026 preprint) |
| **Long-term effects of selection** | random, loss, gradient, diversity, quality and utility-diversity selectors over several fine-tuning stages | n/a | "Rank reversal": short-term selectors help the current stage but slow later learning and **increase forgetting**. Numbers not captured (abstract only) | [2605.30537](https://arxiv.org/abs/2605.30537) (2026 preprint) |
| Survey | | | Background only | [Albalak et al. 2402.16827](https://arxiv.org/abs/2402.16827) |

Code licence: LESS repo is **MIT** ([github.com/princeton-nlp/LESS](https://github.com/princeton-nlp/LESS)). Defaults:
`PERCENTAGE=0.05`, `GRADIENT_TYPE=adam` for train, SGD for validation, `DIMS=8192`. Licences of the BIDS, RDS+,
Influence Distillation and QDIT code: **unknown** (not checked).

---

## 2. Why the published gains likely do not carry over to C

1. **Keep ratio.** Every positive result above keeps 0.001-5% of the pool. C's ratios (estimate, from spec 0 and 2.1):
   - Own program-labelled rows: about **67%** (1.5x generated, then cut). Rows are kept by bin: all medium, all hard,
     30% of easy. At 10-15% budgets, LESS already loses to random (BIDS Table 1). At 67%, any selector can only reorder
     about one row in three.
   - Replay: 90K of about 455-470K eligible = about **19-20%** (round 1); 180K = about **38-40%** (round 2).
   - Licensed public splits: 8,750 rows (r1) / 17,500 (r2) from 14-17 datasets. Pool sizes vary, so the ratio is
     likely < 10% for the big ones (exact ratio unknown here). **This is the only place where selection can matter.**
2. **Wrong objective.** LESS, RDS+ and Influence Distillation optimize loss on a known target. C's goal is accuracy on
   **unseen** domains (sealed part A, ejs-5). By rule, none of these may be a target (section 4).
3. **One candidate per round.** The recipe allows one candidate per round, with no A/B of selectors. So we must pick
   the selector with the best prior: on the evidence above, stratified random plus built-in diversity.
4. **Diversity is already built by construction.** Spec 2.x requires >= 1,050 cards (r1), >= 300 packs,
   about 400 styles (50 held out), >= 30 wordings per family, <= 128 rows per card, and G12 structure-hash dedupe.
   That is the strategy that wins at scale ("diversity > quality", 2410.09335; QDIT worst case).
5. **No transfer need.** LESS's "small selector transfers" result (7B to 13B) is not needed: our selector would be C1,
   the same model we train from. That also means its gradients encode **C1's current errors**, including its "yes" lean.

---

## 3. Failure modes specific to our one-pass letter readout

1. **Format capture (documented).** Gradient similarity follows answer format (cosine about 0.4 within a format,
   about 0.0 across formats; 2609.19589). Targeting a dev set copies its mix of option counts and yes/no vs choice.
   That breaks spec 2.1's option-count table (2-4: 35%, 5-9: 35%, 10-19: 15%, 20-60: 15%).
2. **Label-prior shift (hypothesis, untested).** With a loss on the answer letter only, the gradient on the logits is
   (softmax - one-hot gold). If C1's target-set errors are mostly "yes" on gold-"no" items, the mean target gradient
   points toward "no". Then cosine top-k favours gold-"no" rows and rows C1 gets wrong. That is the same balance break
   as Methods S8, in the other direction. Cheap test if ever needed: on the free L4, take about 2K stratified rows,
   compute the cosine to a target mean gradient, and check gold-label shares in the top 20%.
3. **Hard picks collect label errors.** Without normalization, gradient size grows with (1 - p_g). So inner-product
   influence works like difficulty selection, and it picks up label errors (expert-question 0.4: HLE about 18-29%
   wrong labels). IFD's own rule drops IFD > 1 rows as noisy. Cosine reduces this, but does not remove it.
4. **Task-scale imbalance (documented).** Some targets carry far more influence. In BIDS, LESS loses 2-3 points on
   BBH and wins on IFEval. Fixes: per-target normalization plus iterative or round-robin picks (round-robin 50.9 vs
   mean-max 47.9; Ivison). Our 13 families would need per-family normalization.
5. **Near-duplicates (documented).** Top-k similarity picks clusters of near-duplicates (TSDS). Our template
   generators make exactly such clusters (same card, same structure). Any target-aware pick needs per-card and
   per-structure caps.
6. **Pool growth hurts score-based selectors (documented).** IFD, PPL and NV-Embed got worse as the pool grew
   (Ivison). Round 2 doubles the pool.
7. **Forgetting (documented, no numbers).** Short-term selectors can raise forgetting (2605.30537). C's gate allows
   almost no regression (recipe D-rules, KL anchor), so this risk counts more for C than for the papers.

---

## 4. Leakage map: which targets are allowed

| Candidate target | Allowed? | Why |
|---|---|---|
| Sealed suite (part A select or confirm, B1, P) | **No** | G14 sealed separation; selecting toward it is training on the test |
| ejs-5, OHS-1/2, JevBench public / v1.5.4, Jev Decision Index items | **No** | They are the yardsticks (recipe 16: practice and report sets). DI items are already excluded from training |
| DI task *descriptions* only (names or one-line summaries) | Not advised | Ivison shows proxy targets work (50.4 vs 50.9), but DI results would then have to be reported as "selection-targeted" |
| Mix-tuning dev | **No** | It drives the round-2 rule (R2: CAND - C1 >= +3.0 pp) and temperature refit. Selecting toward it biases a gate |
| F14 hold-out family | **No** | It is the leave-family-out probe; targeting it destroys that role |
| Jev outputs | **Never** | Recipe 16 |
| **New "selection-target" split**: about 1,000 items from held-out packs and styles, written by the format agents, disjoint from all of the above | **Yes** (only valid option) | It adds one more held-out set to build and audit; it must exist and be hashed before any C row is generated |

---

## 5. Cost on our hardware (estimates)

- **RDS+-style embeddings: about 0 extra GPU.** Save C1's pooled last-layer hidden state during the G9 crowd pass on
  the free L4 (spec G9: 3 models, about 20-28 h). Storage is about rows x d_model x 2 bytes. Example: 68K rows x 2,560
  x 2 B = about 0.35 GB. (2,560 is Qwen3-4B's width; check Qwen3.5-4B's config.) Selection on CPU takes minutes.
- **LESS with 1 checkpoint (C1, so no warm-up needed): about 20-30 L4-hours** (estimate). One G9 model pass is about
  7-9 h, and forward + backward is about 3x a forward pass. Add the projection to 8,192 dims. The datastore is about
  1.1 GB for 68K rows and 1.6 GB for 100K. LESS's 4-checkpoint default would be about 4x that. Unknown: whether C1's
  Adam optimizer states were saved. LESS needs them for Adam train gradients; without them, use SGD gradients.
- **Facility location (QDIT-style) on CPU:** lazy greedy within each stratified cell. Cells are a few hundred to a
  few thousand rows, so this takes seconds to minutes per cell. QDIT reports a few hours for million-row pools.

---

## 6. Proposals for the spec owner (for `ADDENDUM_research.md`; nothing edited here)

- **P1. Keep spec 2.1 as is for own rows and replay.** Stratified selection inside family x gold label x wording x
  difficulty-bin cells, then uniform picks inside each cell. Do not add LESS, influence, IFD or RDS+ selection in
  round 1 or round 2. Reasons: 67% keep ratio; LESS below random at 10-15% (BIDS); random about equal at scale
  (2410.09335); the format and label-prior risks in section 3; one candidate per round.
- **P2. Diversity-aware picks only for licensed public pools (3A-3E).** In each dataset x label cell, use greedy
  facility location on C1 pooled hidden states (logged in the G9 pass). Pure coverage (alpha = 0); every row has
  already passed the licence and quality gates. Cap rows per source document. Facility location is preferred over
  k-center because it favours representative rows and does not seek out outliers, which are more often bugs or
  label errors. Expected effect: small, mainly on the worst case (QDIT). Pre-register it before any C row exists.
- **P3. Replay stays representative.** Stratified random, plus the existing S1 rule (drop human-labelled replay with
  C1 p_g < 0.2). Do not target replay toward any dev: its job is to stop forgetting across all skills, and targeted
  selectors can raise forgetting (2605.30537).
- **P4. If target-aware selection is still wanted later (round 3 or a later project):** use RDS+ (cosine on C1
  hidden states), not LESS. Rationale: same or better results at far lower cost, and it scales with pool size.
  Target only the new selection-target split (section 4). Use round-robin across target groups, run it only inside
  the spec 2.1 cells, and cap targeted picks at <= 25% of each cell (the rest stays uniform). Keep the mix-tuning dev
  and F14 untouched as the judges.
- **P5. Post-selection checks (apply to P2 and P4, CPU only):**
  - label x bin chi-square p > 0.01 (G9);
  - option-count bucket shares within +/- 2 pp of the spec 2.1 table;
  - gold-letter positions uniform;
  - <= 128 rows per card;
  - the share of rows with crowd p_g < 0.05 does not rise after selection;
  - G8 AFLite predictable share is unchanged;
  - MinHash near-duplicate rate is unchanged.
- **P6. Do not copy LIMO or s1's tiny-set result.** They rely on long chains from stronger models, a 32B difficulty
  filter and chain-of-thought at inference. Our readout is a single letter, and there is no teacher above 4B. The
  only transferable lesson, keeping mostly medium and hard items, is already in spec 2.1's bins.

---

## 7. Unknowns

- Direct evidence on target-aware vs random selection for **unseen-domain classification or multiple-choice
  accuracy** at a 4B scale: none found.
- Whether the label-prior shift in 3.2 is real for C1: untested (an L4 test is possible; not run, since CPU only).
- Numbers for forgetting and OOD in 2605.30537, and the experiment details in 2609.19589: abstracts only.
- LESS Table 4 GPU type; Qwen3.5-4B hidden size; whether C1's optimizer states exist; pool sizes per public dataset
  (spec 3A-3E).
- Code licences for BIDS, RDS+, Influence Distillation and QDIT.

---

## Sources

- LESS: https://arxiv.org/abs/2402.04333 (HTML v3 tables) ; code https://github.com/princeton-nlp/LESS (MIT)
- BIDS (EMNLP Findings 2025): https://arxiv.org/abs/2501.12147 ; https://aclanthology.org/2025.findings-emnlp.373.pdf
- Rethinking Data Selection at Scale: https://arxiv.org/abs/2410.09335
- Large-Scale Data Selection for Instruction Tuning (RDS+): https://arxiv.org/abs/2503.01807
- Influence Distillation: https://arxiv.org/abs/2505.19051
- TSDS: https://arxiv.org/abs/2410.11303
- QDIT: https://arxiv.org/abs/2311.14736
- IFD / Cherry LLM: https://arxiv.org/abs/2308.12032
- LIMO: https://arxiv.org/abs/2502.03387
- Form Over Content in Gradient-Based Data Attribution: https://arxiv.org/abs/2609.19589
- Long-Term Effects of Data Selection in LLM Fine-Tuning: https://arxiv.org/abs/2605.30537
- Data-selection survey (Albalak et al. 2024): https://arxiv.org/abs/2402.16827
