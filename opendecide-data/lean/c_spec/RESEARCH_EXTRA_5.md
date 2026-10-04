# RESEARCH_EXTRA_5: Interference between families and loss-term weights in one shared LoRA

Date: 3 Oct 2026. Targeted research 5 for C. CPU only, about 20 web fetches/searches, no paid calls.
Read-only use of `C_DATA_SPEC.md`, `C_TRAIN_RECIPE.md` and `LOCAL_GAPS.md` (none edited). One new local CPU check
(section 2) on `data/v14_parts/golden_train.jsonl` (C1's 500K training file; no OHS-3 file was opened).
"Estimate" marks our own arithmetic. "Hypothesis" marks a mechanism we inferred but have not tested.
Sources are listed at the end.

---

## 0. Bottom line

1. **Do not add a multi-task optimizer (PCGrad, GradNorm, MGDA, CAGrad, LoRAMoE).** Two NeurIPS 2022 audits find that a
   plain weighted sum of losses, properly tuned and regularized, matches or beats them. Kurin et al.: "none of the
   methods consistently outperforms unitary scalarization"; PCGrad ran **about 35x slower** on 40-task CelebA. Xin et
   al.: "no algorithm outperforms sampling with a well-chosen sampling ratio". The levers that matter are **mixture
   shares and loss weights**, and C already has both.
2. **Accuracy alone cannot show whether family X hurts family Y at the gate's resolution.** To see a -0.5 pp change
   per family with 80% power, you need about **18,500 paired rows per comparison** (estimate, section 3.1). The old
   slice has 2,000. A per-family signal therefore has to come from **gradients or margins**, not from accuracy counts.
3. **A cheap monitor exists and is well tested in a nearby setting.** Task Affinity Grouping (TAG) measures "does a
   step on X lower the loss on Y". It worked as well when computed every 10 steps as every step (5.13% vs 5.13%, 3.19x
   faster). Affinities on train and validation batches agreed (Pearson **0.98**). Affinities taken from only one
   quarter of training were worse (3.67-4.31%), so **read them at several points**. The first-order form of TAG is a
   gradient dot product. We propose a 4-read version on the L4 (section 3): step 0, 25%, 50% and 75%.
4. **The local "yes" symptom is not a label-prior problem (new local check).** C1's training yes/no rows are 49.7%
   "yes". Affirmative rows are 49.7%. 94.3% of yes/no rows come from sources with a 45-55% yes rate. KD teacher
   targets lean **"no"** on gold-no rows (mean P(yes) 0.092), not "yes". So the spec's yes-rate balancing is needed
   but **will not by itself remove** the 80.4 vs 85.4 gap. The cause is unknown. It is probably interference or a
   wording-level shortcut (hypothesis). This is why the monitor includes a **"yes-push" attribution** (section 3.4).
5. **Loss weights: keep C1's weights in round 1 and diagnose them, do not sweep them.** One sweep point costs a whole
   round (about $27-29), so a 3-point sweep of one weight (about $85) does not fit the $100 cap. Sweeps are also
   noisy: on a sparse grid, the spread of the best point had a standard deviation **6-7x** the seed SD (Xin et al.).
   Consistency-KL weights do matter on classification: in R-Drop on BERT, the best weight was 0.5 or 1.0, and 1.5 was
   worse on all four GLUE tasks shown (MNLI 84.48 at 0.5, 83.44 at 1.0, 82.27 at 1.5). C's `lam` 1.0 and `lam_inv`
   1.0 sit at the **top of the safe range**. They are the first weights to check. The rule is in section 4.
6. **Use of the monitor:** report-only in round 1. It may (a) give an attribution if round 1 fails R3/R4, and (b) give
   evidence for the existing bounded between-round weight update. Gradient evidence alone never changes a weight
   (section 3.6).

---

## 1. What the literature says

### 1.1 Weighted sums vs multi-task optimizers

| Finding | Numbers | Source | Meaning for C |
|---|---|---|---|
| Unitary scalarization + standard regularization matches specialized multi-task optimizers (SMTOs) | Multi-MNIST, CelebA (40 tasks), Cityscapes, RL: "none of the methods consistently outperforms unitary scalarization"; PCGrad about **35x** slower than unitary on CelebA; MGDA, IMTL, GradDrop 1.05-2.4x; RLW about 5% overhead | Kurin et al. 2022 | No PCGrad etc. Per-term or per-family gradients at **every step** would multiply C's cost by the number of groups (6-20x) |
| SMTOs mostly act as regularizers | Their ablation suggests SMTOs reduce overfitting; dropout 0.25-0.5, early stopping or L2 (grid {0, 1e-4, 1e-3}) closes the gap | Kurin et al. 2022 | If C shows interference, first reach for **regularization and shares** (C1 anchor, LR 5e-5, replay 60%), not a new optimizer |
| Scalarization weights trace the whole trade-off curve; MTO methods just pick a point on it | En->{Ro, Fr}: no Pareto frontier on test; weights (0.3, 0.7) were globally best and beat all MTO methods; "no algorithm outperforms sampling with a well-chosen sampling ratio" | Xin et al. 2022 | Mixture shares (sampling ratios) are the main knob. Spec 2.1 already fixes them, plus a bounded between-round update |
| Hyperparameter-grid effects are larger than optimizer effects | Sparse LR grid: SD of the best result 6-7x the seed SD; grid choices are "orders of magnitude larger than the MTO effect size" | Xin et al. 2022 | Do not read a one-run weight change as a win. Any weight change needs a pre-registered comparison |
| Grouping beats gradient tricks; tricks add little on top | CelebA: uncertainty weighting, GradNorm and PCGrad were worse than TAG or HOA groupings; PCGrad on top of TAG groups gave +0.85 / +0.18 / -0.08 % (2/3/4 splits) | Fifty et al. 2021 (TAG) | One shared adapter is fine. If a family conflicts, cut its share; do not add gradient surgery |

### 1.2 Interference is real, but depends on the regime

| Finding | Numbers | Source | Meaning for C |
|---|---|---|---|
| Mixing helps when data is scarce and conflicts when data is plentiful | LLaMA 7B/13B/33B, full SFT, math + code + general: mixed sources gain at 1/256 of the data and conflict at 100%; turning point between **1/64 and 1/16**; "amount of composition data influences performance more than the composition ratio"; DMT (specialist first, then mix with 1/256 specialist) raised 7B GSM8K 32.6 -> 41.92 and HumanEval 15.24 -> 17.68 vs mixed sequential | Dong et al. 2024 (ACL) | C is in the "plentiful" regime for replay (C1 saw 500K) and the "scarce" regime for each new family (round 1: about 3,500 own rows per family, estimate from 45,250 / 13). Expect new families to help each other a little, and the risk to sit on **old rows**. That is what the old slice and the anchor watch |
| Negative transfer between task pairs is common and directional | 22 NLP tasks, about 25,000 runs: about 46% of 210 pairs negative (intermediate-task transfer, T5 / GPT-2 / RoBERTa); 5 source tasks best, 10 worse, 21 "drops considerably" | Kim et al. 2023 (TaskWeb) | Pairwise affinity is **asymmetric** (X hurts Y does not mean Y hurts X), so the monitor must be directional. Caution: sequential transfer to small targets, not a 60/40 joint mix |
| A source's label balance moves other tasks a lot | Llama-3.2-3B, LoRA r64, single-source fine-tunes: balancing Flipkart (negatives 20% -> 50%) moved Pile 39.10 -> 50.05 and IMDB 77.15 -> 57.80; MetaMath fine-tuning cost Flipkart -17.45 and Amazon -10.20; "class distribution, generation length" predicted transfer better than surface similarity | Latent Traits 2025 (2509.13624) | Supports the spec's per-family yes-rate balance (50% +/- 2 per cell). Mixing dilutes the effect; how much is unknown. See section 2: C1's data was already balanced |
| Large instruction data can erase world knowledge stored in the base | Stated in abstract; numbers not extracted (unknown) | LoRAMoE (Dou et al. 2023) | Architecture change (several LoRA experts plus a router) means new code and a serving change. Not for C |

### 1.3 Ways to measure affinity cheaply

| Method | How it works | Numbers | Source |
|---|---|---|---|
| TAG lookahead affinity | Z(i->j) = 1 - L_j(after a step on task i's gradient) / L_j(before), same batch | Every 10 steps = every step (5.13%), 3.19x faster; every 50 steps 3.73%; first/middle/final 25% only: 3.67 / 4.31 / 4.02%; train vs validation affinity Pearson **0.9804**; 11.6x faster than the prior SOTA grouping (22x vs HOA on CelebA) | Fifty et al. 2021 |
| Group gradient cosine (CS baseline in TAG) | cos(mean grad of i, mean grad of j) | Worse than TAG for grouping on CelebA. TAG's theory links its score to cosine when gradient norms are equal | Fifty et al. 2021 |
| LoRA gradient features (LESS) | Per-row LoRA gradients, Rademacher random projection to d = 8,192, **cosine** (not dot product, because token-averaged gradients favor short rows), Adam-aware, several checkpoints | N = 4 checkpoints beat N = 1 (49.3 vs 47.8 avg); 48 GPU-h for features of 270K rows x 4 checkpoints (about 0.16 s per row-checkpoint, estimate; GPU type not extracted); 17.7 GB store | Xia et al. 2024 |
| Raw LoRA-gradient cosines are tiny | Code vs biomedical on one LoRA: cos = -0.002 +/- 0.003 over 20 trials (75% < 0); one MoE expert layer -0.42 | Preprint, single source, MoE models (Phi-tiny-MoE, OLMoE-1B-7B) | 2609.03150 |
| Auxiliary-loss gating by gradient cosine | Use an auxiliary loss only when cos(aux grad, main grad) > 0 (or weight it by the cosine); converges to critical points of the main task | Numbers not extracted (unknown) | Du et al. 2018 |
| Gradient size is not gain | Multi-task RL post-training, Qwen2.5-3B/7B, Llama-3.2-3B: code gradients up to **15x** math; arithmetic up to 33x squared norm, yet lowest gains | 2510.19178 | Big-gradient families steer the adapter without helping. Log the norm share per group |

Takeaways for the design:
- Raw cosines can be tiny (about 0.002), so they need a **noise ceiling**. Normalize by the within-group split-half
  cosine (section 3.3).
- Rows vary in length (C's tok50 is about 590-880; some rows exceed 2,000), so use **cosine or per-row normalized**
  gradients, as LESS does.
- Read at **several points**. TAG shows one-window affinities are worse, and LESS shows that more checkpoints help.

### 1.4 Loss-term weights

| Finding | Numbers | Source | Meaning for C |
|---|---|---|---|
| Consistency-KL weight is sensitive, and best values differ by task | BERT-base GLUE, alpha in {0.1, 0.5, 1.0, 1.5}: MNLI 84.20 / **84.48** / 83.44 / 82.27; QNLI 91.21 / 91.92 / **92.01** / 91.12; MRPC 84.30 / 86.03 / **86.51** / 85.78; SST-2 92.54 / 92.77 / **93.02** / 92.43. "alpha = 1.0 is a good choice for most tasks"; NMT best alpha 5 of {1, 3, 5, 7, 10} | Liang et al. 2021 (R-Drop) | C's `lam` 1.0 (complement / equiv) and `lam_inv` 1.0 sit at the top of the safe range for classification. The largest dataset (MNLI, 393K) preferred 0.5, and 1.5 was worse everywhere (-0.4 to -2.2 pp). R-Drop's KL is between dropout views, not relation pairs, so this is an analogy |
| Cosine gating of auxiliary losses | see 1.3 | Du et al. 2018 | Diagnostic: an auxiliary term whose gradient points against the held-out task gradient at several reads is a candidate to halve |
| No paper found that ablates our exact stack (CE + LS + KD + relation KL + permutation KL + selective old-model anchor) on an LLM decision readout | - | unknown | The weights were inherited from C1. We found no record of a C1 sweep (unknown). Treat them as untested, not tuned |

---

## 2. Local check: where does C1's "yes" drift come from? (new, CPU, about 1 s per pass)

Script: scratchpad `yesrate.py`, `rolerate.py`, `teach2.py` (read-only over `data/v14_parts/golden_train.jsonl`,
501,732 rows; `qtype` "noul" = yes/no, gold "1" = yes).

| Check | Result |
|---|---|
| Yes rate, all yes/no rows (323,868) | **49.7%** |
| Yes rate by role | aff 49.7% (263,684), neg 49.4%, attacked 50.0%, dneg 52.0%, para 50.5% |
| Sources by yes rate (183 sources with yes/no rows) | 45-55%: 164 sources, **94.3%** of rows; 30-45%: 15 sources, 4.1%; 55-60%: 3 sources, 1.6%; none above 60% |
| KD teacher targets on yes/no rows (53,120 rows with a teacher dict) | gold no: mean teacher P(yes) **0.092** (aff gold no: 0.066), 94.9% of them below 0.5; gold yes: 0.846 |

What this means:
- The symptom (LOCAL_GAPS 4.3): on affirmative yes/no questions, C1 is better when gold is "yes" (84.6 vs 80.3) and
  worse when gold is "no" (81.4 vs 86.5), against 4B-E. On seen sources, gold no is 80.4 vs 85.4. Overall, C1 says
  "yes" on 50.4% of rows (gold 50.0%). So this is a **threshold shift on affirmative questions**, not a global prior.
- Neither the training label prior (source, role) nor the KD teacher explains a "yes" lean. Weight-preservation's
  advice to match C1's yes rate is already met by C1's own data, and C's spec balances new rows. **Balancing is
  necessary but not sufficient.**
- Note that the comparison is C1 vs 4B-E, a sibling model trained on different data. It is not C1 vs its own start.
  The gap may be partly something 4B-E learned rather than C1 drift (unknown).
- Remaining hypotheses (untested): (a) **cross-family interference**: families whose "yes" rows share surface
  features with other sources' gold-no rows (for example "Is the correct answer X?" with a plausible X); (b)
  **per-wording priors**: yes rate balanced per source but not per instruction wording; (c) **relation-loss
  coupling**: complement / equiv KL ties aff and neg answers, so one side's error can drag the other. Section 3.4
  attributes (a) and (c) directly. Hypothesis (b) is a CPU check on the C data: yes rate per wording (spec G10
  already requires 50% +/- 2 per family x wording cell for new rows; replay is not checked per wording).

---

## 3. Proposed monitor for round 1: family affinity + yes-push (FAM-1)

Report-only. It runs on the L4 at **step 0 (C1 itself, before launch)** and on the **25 / 50 / 75% snapshots** that
the recipe already reads. No training-code change: it loads a snapshot adapter and runs extra forward/backward passes
with dropout 0. No optimizer step.

### 3.1 Why gradients and not accuracy

- Paired SE on n old rows is about sqrt(d / n), where d is the share of rows where C and C1 disagree. With d = 6%
  (estimate; wise090 vs C1 disagreed on only 1.4%, but a 150K-row fine-tune moves more), n = 2,000 gives SE about
  **0.55 pp**. A per-family split of about 200 rows gives about 1.7 pp.
- Detecting -0.5 pp at 80% power needs SE <= 0.18 pp, so n >= 0.06 / 0.0018^2, about **18,500 rows** per comparison.
- Continuous signals (gold log-odds margin, P(yes) on gold-no rows, and gradients) have far smaller SE per row. The
  recipe's P(yes) drift stop at 0.02 already uses one.

### 3.2 Groups and rows

| Group | Rows | Count |
|---|---|---|
| Each of the 13 new families (training rows, mixed cards) | 64 each, as 4 quarters of 16 | 832 |
| Replay clusters: about 8 clusters by `fam` in `golden_train_sources.csv` (fact_tables, qa_decisions, NLI / entailment, sentiment / emotion, safety / hate, security, extraction, other) | 64 each | 512 |
| Target T_old: old-slice rows (held out of replay), CE gradient | 256 | 256 |
| Target T_no: old-slice affirmative yes/no rows with gold "no" from seen sources, margin gradient | 256 (or all available) | 256 |
| Target T_new: mix-tuning dev, new families, CE gradient | 256 | 256 |
| Loss-term batch: one fixed batch of 64 training units with relation pairs, inv pairs and perm twins; gradient of each term separately | 64 units | about 200 row-passes |
| Controls (never trained): **positive control** = 64 rows of one new family relabelled all "yes"; **negative control** = 64 rows with random labels | 128 | 128 |

Total about **2,450 row backward passes per read** (estimate).

### 3.3 What is computed

For each group X, the trainer's own loss on those rows gives g_X = mean LoRA gradient (fp32, 32,464,896 values). Keep the
4 quarter-means in fp16 on the host (about 65 MB each; 21 groups x 4, about 5.5 GB). No random projection: at
d = 8,192, projection noise is about 1 / sqrt(8192), about **0.011**. That is above the 0.002 cosines seen in 1.3, so
full-dimension means are safer (estimate).

1. **Normalized affinity onto each target** T in {T_old, T_new}:
   rho(X->T) = cos(g_X, g_T) / sqrt(rel_X x rel_T), with rel = mean split-half cosine of the group's quarter-means
   (attenuation correction). rho near 1: X pulls the same way as T, as far as noise allows. Near 0: unrelated.
   **Below 0: a step on X raises T's loss (first-order TAG).** Jackknife the 4 quarters for a 95% CI.
2. **Pairwise matrix** rho(X->Y) over the 21 groups (directional, because TaskWeb found transfer non-commutative; use
   the raw dot product scaled by ||g_X|| for direction). Report only.
3. **Norm share**: ||g_X|| x row share of X, divided by the sum over groups. Compare with the row share.
   (A family with a 3% row share and a 20% norm share steers the adapter. 2510.19178 shows that does not mean it
   helps.)
4. **Lookahead check (exact TAG, top 3 only)**: for the 3 groups with the most negative rho onto T_old or the largest
   yes-push, apply one step theta' = theta - s x g_X / ||g_X||. Set s to the measured mean adapter movement over 100
   training steps between snapshots, ||theta_50% - theta_25%|| x 100 / steps. Re-read T_old and T_no losses and
   P(yes) (forward only). Z = 1 - L_after / L_before. This checks the first-order sign at a realistic step size.

### 3.4 Yes-push attribution (targets the local symptom)

- v = gradient of the mean (logit "yes" - logit "no") over T_no rows. Map letters to the semantic yes/no option,
  because cygnet-style rows randomize the Yes/No letter order.
- push(X) = -cos(g_X, v). **Positive push: a step on X raises the yes margin on old gold-no rows.**
- Contribution(X) = push(X) x ||g_X|| x row share(X). This ranks who drives the drift.
- Do the same for each loss term (section 4): push(term) tests hypothesis (c) in section 2.
- **Validity rule:** the positive control must show push > 0 with its jackknife CI above 0, and the negative control
  must have a CI that covers 0. If either fails at step 0, the yes-push output is reported as invalid for that run.

### 3.5 Cost (estimate)

- H100 training: 2.72 s per step of 16 units, about 0.17 s per row forward+backward. An L4 has roughly 1/8 of H100
  bf16 compute and about 1/11 of its memory bandwidth, so plan for about **1-2 s per row**. 2,450 rows is about
  **40-80 min per read** and 4 reads is about **3-5 L4-hours** on Google credit. Modal spend: **$0**.
- Snapshots are about 1.7 h apart (2,220 steps x 2.72 s, estimate), so each read finishes before the next snapshot.
  If the step-0 read takes more than 50 min, halve the rows per group (32, as 4 x 8) for later reads. The jackknife CI
  shows the cost in width.
- Memory: 4B in bf16 is about 8 GB. Gradient checkpointing is needed on rows over 2,000 tokens (24 GB L4). Cap
  monitor rows at 2,000 tokens.

### 3.6 What FAM-1 may decide (proposed pre-registration text)

- **Round 1: nothing.** No mid-run reweighting (one pass, one pre-registered candidate). Stop rules stay as in the
  recipe (old slice -1.5 pp at 25% and 50%; P(yes) drift > 0.02).
- **Between rounds (only if round 2 runs, about 13%):** the existing bounded per-family weight update (mix-tuning dev,
  >= 400 items per family, p < 0.05) may also cut a family's share **within the same bounds** only if all of these
  hold:
  (i) rho(X->T_old) < 0 with the jackknife CI below 0 at >= 2 of the 3 snapshot reads;
  (ii) the exact lookahead (3.3 step 4) agrees in sign;
  (iii) the old-slice accuracy on the replay clusters with the most negative rho(X->cluster) is below C1, in
  direction only.
  Gradient evidence alone never moves a weight. This follows Xin et al.: act only on the shares and confirm on outcomes.
- **If round 1 fails R3 (no harm) or R4 (retention):** FAM-1's tables go into the owner's diagnosis, ranking the
  groups and terms most likely responsible. Any change needs an amendment.
- **Step-0 read before launch** also serves as a pre-flight. If one new family already shows rho(X->T_old) below
  -0.2 or a yes-push ranked first by a wide margin at C1, flag it to the owner **before** round 1. The threshold is
  our choice; no literature number exists.

---

## 4. Loss weights: what to validate and how

The recipe's stack, unchanged from C1: CE with label smoothing 0.05 (MNLI 0.08); KD mix 0.5 (target = 0.5 smoothed
gold + 0.5 teacher; the C1 anchor reuses this path); complement / equiv `lam` 1.0 (symmetric); injection invariance
`lam_inv` 1.0; permutation twins `perm_twin` 0.3, `lam_p` 0.5; base anchor `beta` 0.

| Term | Weight | Risk for C | Evidence | Diagnostic at each FAM-1 read (fixed 64-unit batch) |
|---|---|---|---|---|
| Relation consistency (complement / equiv) | 1.0 | **Highest.** Top of the safe range; may couple aff and neg errors (section 2, hypothesis c) | R-Drop: 1.5 worse on all 4 GLUE tasks; MNLI best at 0.5 | Norm share; cos with g_T_new and g_T_old; push(term) |
| Injection invariance | 1.0 | Medium. Applies only to `inv` pairs; protects security | Same analogy | Same; also the security guard D-split in the gate |
| C1 anchor (via KD targets, confident and right rows plus protected skills) | 0.5 of the target | Medium. Near-zero gradient at step 0 (p = p_C1, apart from the two-view disclosure); grows as C drifts. Too strong, and it blocks learning; a competitor lost 2.7 pp with KL to its previous version | Recipe 3; DER++ equal weights | Norm share over time; cos(anchor, g_T_new). Anchor share rising while T_new rho falls means it is fighting new learning |
| KD 0.5 (teacher rows) | 0.5 | Low. Teacher targets lean "no" on gold no (0.092), so not a yes source (section 2) | Local check | push(term) |
| Permutation twins | 0.3 / 0.5 | Low. Small weight, choice rows only | - | Norm share; cos with g_T_new |
| Label smoothing | 0.05 | Low. Affects calibration more than accuracy | - | Not monitored separately |

**Flag rule (proposed, for round 2 or a later amendment only):** a term is flagged if, at >= 2 of 3 snapshot reads,
(a) cos(g_term, g_T_new) < 0 **and** cos(g_term, g_T_old) <= 0, each with its CI below or touching 0, or
(b) its yes-push is positive with a CI above 0 **and** P(yes) on old gold-no rows rose. A flagged term gets **one**
pre-registered change: **halve its weight** (for relation terms: 1.0 -> 0.5, R-Drop's best for the largest
classification set). Never two changes at once. A term with a large norm share (> 50%, our threshold) but no sign
conflict is reported, not flagged. Size alone is not harm (2510.19178).

**Why no sweep in C:** one round-1 run costs about $27-29. A 3-point sweep of one weight costs about $85 and would
need 3 extra looks at the select set. Xin's sparse-grid noise (6-7x seed SD) means a 2-point comparison could mislead.
If the owner wants a weight test later, the cheapest valid design is a small paired run: two arms at about 20K rows
each, same seed and same rows, differing only in the one flagged weight, read on the mix-tuning dev and the old slice
(about $8 for both arms, estimate from 2.72 s/step).

---

## 5. What not to do

- No PCGrad / GradNorm / MGDA / CAGrad / Nash-MTL: per-group gradients at every step cost 6-20x, and the audits show no
  reliable gain (Kurin; Xin; TAG + PCGrad +0.85 / +0.18 / -0.08%).
- No LoRAMoE or per-family adapters in C: new code, a serving change, and new failure modes (the router preprint
  2609.03150 shows conflict persists inside each adapter).
- No affinity read from only one window (TAG: first / middle / final 25% each worse than all-training averages).
- No action on raw cosines without the split-half ceiling. Raw LoRA cosines can be about 0.002.
- No per-family accuracy claims on the 2,000-row old slice (SE about 1.7 pp per 200-row cluster).
- Do not assume yes-rate balancing fixes the "yes" drift. C1's data was already balanced (section 2).

---

## 6. Unknowns

- How strongly C's 13 families interfere with replay at a 60/40 mix: no paper measures a 4B LoRA decision readout
  in this setting.
- L4 time per monitor row (1-2 s is an estimate; measure at the step-0 read).
- Whether snapshots keep Adam state. If they do, use Adam-preconditioned gradients as LESS does (better per LESS;
  their exact gain was not extracted). If not, plain gradients (first-order SGD view) are used. Say which in the report.
- Typical split-half reliability of 64-row group gradients on a 4B LoRA (unknown until the step-0 read). If rel < 0.1
  for most groups, raise the rows per group or merge groups.
- Whether C1's loss weights were ever swept (no record found).
- The cause of the "yes" drift. Section 2 rules out the label prior and the KD teacher, but not interference, wording
  priors or relation coupling.
- Du et al. 2018, DoGE and LoRAMoE quantitative results were not extracted (abstract-level only).

---

## 7. Lines for ADDENDUM_research.md (for the addendum writer)

- R5-1: No multi-task optimizer. Weighted sum plus mixture shares is the evidence-backed choice (Kurin 2022; Xin 2022).
- R5-2: Add FAM-1 (report-only): group-gradient affinity with split-half normalization, yes-push attribution,
  term-gradient diagnostics, top-3 exact lookahead. Reads at step 0, 25, 50 and 75% on the L4, about 3-5 L4-h, $0 Modal.
- R5-3: Between-round share cuts may use FAM-1 only together with lookahead agreement and old-slice direction, inside
  the existing bounds.
- R5-4: Keep C1's loss weights in round 1. The first flag candidate is relation `lam` 1.0. The only allowed change is
  to halve it, by amendment.
- R5-5: C1's training data is yes/no balanced (49.7% yes; aff 49.7%; KD teacher P(yes) on gold-no 0.092). The yes
  drift needs attribution, not just balancing. Add a CPU check of replay yes rate **per instruction wording**.

---

## Sources

- Fifty et al. 2021, Efficiently Identifying Task Groupings for Multi-Task Learning (TAG), NeurIPS: https://arxiv.org/abs/2109.04617
- Kurin et al. 2022, In Defense of the Unitary Scalarization for Deep Multi-Task Learning, NeurIPS: https://arxiv.org/abs/2201.04122
- Xin et al. 2022, Do Current Multi-Task Optimization Methods in Deep Learning Even Help?, NeurIPS: https://arxiv.org/abs/2209.11379
- Yu et al. 2020, Gradient Surgery for Multi-Task Learning (PCGrad): https://arxiv.org/abs/2001.06782
- Dou et al. 2023, LoRAMoE: https://arxiv.org/abs/2312.09979
- Dong et al. 2024, How Abilities in LLMs are Affected by SFT Data Composition, ACL: https://arxiv.org/abs/2310.05492
- Kim et al. 2023, TaskWeb, EMNLP: https://arxiv.org/abs/2305.13256
- Latent Traits and Cross-Task Transfer (2025): https://arxiv.org/abs/2509.13624
- Xia et al. 2024, LESS: https://arxiv.org/abs/2402.04333
- Routing Is Not Enough: Intra-Adapter Subspace Contention in MoE+LoRA (preprint 2026): https://arxiv.org/html/2609.03150v1
- Du et al. 2018, Adapting Auxiliary Losses Using Gradient Similarity: https://arxiv.org/abs/1812.02224
- Liang et al. 2021, R-Drop, NeurIPS: https://arxiv.org/abs/2106.14448
- Imbalanced Gradients in RL Post-Training of Multi-Task LLMs (2025): https://arxiv.org/html/2510.19178v1
- Fan et al. 2023, DoGE (abstract only): https://arxiv.org/abs/2310.15393
- Local: `LOCAL_GAPS.md` 4.3 and item 6; `RESEARCH_weight-preservation.md` (yes-rate advice, KL alert); `C_TRAIN_RECIPE.md`
  0, 3, 4, 5, 6.3; `C_DATA_SPEC.md` 2.1, 10, G10.
