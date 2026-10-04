# RESEARCH_EXTRA_3: calibration and committed answers under domain shift

Date: 3 Oct 2026. Targeted research 3 of the completeness pass. CPU only, $0.
Writes only this file. `C_DATA_SPEC.md` and `C_TRAIN_RECIPE.md` were read, not edited.
Data rules kept: no ohs3 file, no `prep89/dryrun/`, no `bench/external_quarantine/` was opened. No temperature was fitted on OHS, JevBench, ejs-5 or the sealed suite.

Scope: four gaps the earlier reports left open.
1. Calibration under growing shift.
2. Temperatures for tasks the model has never seen (the sealed suite and ejs-5).
3. Label-prior correction from unlabelled data when classes are not balanced.
4. How averaging K views interacts with the JevBench v1.5.4 abstention band (0.2 < P(yes) < 0.8 is scored wrong), and with E on Score rows.

Local numbers come from scratch scripts run on existing prediction files (C1 = `q35_4b_main500k`). They are report-only and were not used to select anything.

---

## TL;DR (decisions for C)

1. **A temperature fitted in-distribution will not hold on new domains.** Ovadia et al. found that temperature scaling gives the lowest ECE at small shift, but its ECE "increases significantly as the shift increases". On Criteo, temperature scaling even had a *worse* Brier than no calibration. Ensembles held up best. Locally, C1 is already calibrated on dev: a refit gives T = 0.95 for yes/no and 1.05 for choice, and the gain is about 0. The miscalibration shows up only on shifted sets, and **its direction flips**:
   - OHS-1 yes/no: confidence 81.5 vs accuracy 78.3, so +3.2 overconfident.
   - OHS-2 yes/no: 88.7 vs 93.6, so -4.9 underconfident.
   - No single global T fixes both. D4 (dev Brier) cannot see this.
2. **Fit T across held-out families, not within them.** In Thermometer's leave-one-task-out MMLU test (LLaMA-2-7B):

   | Method | ECE |
   |---|---|
   | No calibration | 0.260 |
   | One T fitted on the other tasks (TS-CV) | 0.119 |
   | Thermometer (predicts T per task) | 0.078 |
   | Oracle T, fitted on the task's own labels | 0.062 |

   Plain cross-task fitting already captures about 71% of the possible gain, and it costs $0. **Use leave-one-family-out per-type T on the mix-tuning-dev families.** A Thermometer-style T predictor is optional and report-only (section 2).
3. **Label-prior correction: use EM with bias-corrected calibration, as a secondary readout only.** Alexandari et al. found that EM with BCTS or vector scaling is "hard to beat". BBSE and RLLS did not beat EM when probabilities were well calibrated. Plain TS leaves a systematic class bias that hurts EM. Two limits for us:
   - It needs a batch of unlabelled target rows, but JevBench serves one decision per request.
   - Batch calibration's balanced-class assumption stays "risky".

   So no prior adaptation goes into the shipped or headline readout. At most, it is a pre-registered secondary readout on whole benchmark sets.
4. **Averaging views pulls yes/no probabilities toward 0.5, and averaging in probability space pulls hardest.**
   - The v1.5 band then turns some of those answers into abstentions, scored wrong. A synthetic K = 4 test with view noise SD 1.0 on the logit scale:

     | Aggregation | Rows in band | v1.5 committed accuracy |
     |---|---|---|
     | Prob-mean | 33.4% | 61.3 |
     | Logit-mean | 27.4% | 66.3 |

     At SD 1.5 the band shares are 42.2% (prob-mean) vs 29.2% (logit-mean).
   - The literature agrees: averaging calibrated members gives an underconfident ensemble (Wu & Gales), and averaging logits raises confidence (Tassi et al.; ECE 12.03% → 5.44% for an underconfident model).
   - On C1's real 2-view, the yes/no letter-swap views barely differ (mean |dP| 0.0043), so the choice of aggregation does not matter there.
5. **Decisions on aggregation:**
   - Yes/no stays a **single read** (A5). If yes/no views are ever added, use **logit-mean**.
   - Choice keeps the pre-registered **2-view prob-mean**. On C1 dev, prob-mean vs logit-mean differ by 0.001 ECE and 0.0007 NLL, with the same accuracy.
   - Score rows use **prob-mean**, so E stays linear (see 4.4).
   - Fixed order of operations: **aggregate → T fitted on the aggregated dev output → band edge (JevBench only)**.
   - D4 Brier must be computed on that exact served pipeline, never on the 1-view read.
6. **Shift fills the band.** C1 yes/no has 26.3% of rows in the 0.2-0.8 band on dev, and **37.9% on OHS-1**. Jev has 43.1% on OHS-1. The band-edge readout already turns these rows into committed answers (it keeps the argmax). Its cost is calibration: Brier is about +0.006 on dev, more under shift.

---

## 1. Calibration degrades as shift grows (evidence)

| Finding | Number / quote | Source |
|---|---|---|
| Uncertainty quality falls with shift for every method | "the quality of uncertainty consistently degrades with increasing dataset shift regardless of method" | [Ovadia et al. 2019](https://arxiv.org/abs/1906.02530), section 5 |
| In-distribution TS does not transfer | TS "achieves low ECE for low values of shift, the ECE increases significantly as the shift increases ... calibration on the i.i.d. validation dataset does not guarantee calibration under distributional shift" | same, CIFAR-10-C / ImageNet-C |
| TS can be worse than nothing | Criteo: "temperature scaling has a worse Brier score than Vanilla ... post-hoc calibration on the validation set actually harms calibration under dataset shift" | same, section 4.4 |
| Text (20 Newsgroups, shifted classes, LM1B) | "Ensembles significantly outperform all other methods"; TS "does not appear to increase uncertainty significantly on the shifted data" | same, section 4.3 |
| Ensembles are most robust; small K is enough | "relatively small ensemble size (e.g. M = 5) may be sufficient" | same |
| Softmax confidence is overconfident out of domain | selective QA trained on SQuAD: the softmax answers 48% of questions at 80% accuracy; a calibrator trained on source + *other* known OOD data answers **56%** | [Kamath, Jia, Liang 2020](https://arxiv.org/abs/2006.09462) |
| Held-out-dataset T fit beats in-source fit (competitor) | Kev breadth ECE 0.059 (in-source fit) vs 0.0085-0.017 (fit on held-out datasets) | `RESEARCH_competitor-lessons.md` lesson 9 |

**Local check (report-only, CPU, existing preds).** Raw P(yes), all rows of each set:

| Set | Model | yes/no n | acc | mean conf | conf - acc | Brier | in 0.2-0.8 band |
|---|---|---|---|---|---|---|---|
| dev (9 splits) | C1 | 4,329 | 85.2 | 84.9 | -0.3 | 0.1096 | 26.3% |
| OHS-1 | C1 (A5 readout) | 2,972 | 78.3 | 81.5 | **+3.2** | 0.1516 | **37.9%** |
| OHS-1 | Jev guard | 2,972 | 80.5 | 79.8 | -0.7 | 0.1331 | 43.1% |
| OHS-2 | C1 (A5 readout) | 360 | 93.6 | 88.7 | **-4.9** | 0.0570 | 14.2% |
| OHS-2 | Jev guard | 360 | 96.1 | 90.2 | -5.9 | 0.0372 | 12.2% |

- C1 choice rows show the same flip: OHS-1 is -1.8 (underconfident) and OHS-2 is +3.7 (overconfident).
- The OHS-2 Brier values (0.057 vs 0.037) match the recipe. For OHS-1, my recompute on all 2,972 yes/no rows gives 0.152 vs 0.133, not the recipe's 0.140 vs 0.114. That headline probably uses a different row set or readout. **Not reconciled.**
- Jev's choice numbers from `jev_guard.jsonl` look like a label-key mismatch (accuracy 29-35%), so I ignored them.
- **Meaning:** under shift, C1's errors are not one fixed temperature away from calibrated. The sign changes by set and by type. A global T refit can at best trade one set against another. This fits Ovadia's result that epistemic methods, not post-hoc scaling, hold up.

## 2. Temperatures for unseen tasks

**Thermometer** ([Shen et al., ICML 2024](https://arxiv.org/abs/2403.08819); numbers from the [HTML version](https://arxiv.org/html/2403.08819)):
- **What it is:** a small MLP that maps last-layer features of a task's inputs to a temperature. It is trained on many tasks and tested leave-one-task-out on MMLU, BIG-bench and MRQA.
- **ECE, LLaMA-2-Chat 7B (Thermometer / no calibration / oracle TS):**
  - MMLU: 0.078 / 0.260 / 0.062.
  - BIG-bench: 0.090 / 0.233 / 0.044.
  - MRQA: 0.065 / 0.127 / 0.029.
  - FLAN-T5-XL MMLU: 0.080 vs 0.181 with no calibration.
- **Cross-task single T (TS-CV, fitted on the other K-1 tasks):** MMLU ECE 0.119 ± 0.014.
- **Cost:** about 0.5% slower inference. Performance is stable at test batch sizes 1, 16 and 128, so it can run per request. A predictor trained on 7B transferred to 13B and 70B.
- It does not change accuracy (it only rescales).

**"The Well-Tempered Classifier"** ([Mattei & Loureiro 2026](https://arxiv.org/abs/2602.14862)). This is theory only, with no shift numbers. Two facts are relevant to us:
- Temperature scaling is "the only linear scaler that does not change the hard predictions". So T can never move v1.5 Intelligence when we use argmax or band edge. It only moves the Calibration axis and Brier (D4).
- Higher T means higher entropy.

**What C should do ($0, CPU):**
1. **Fit T on the data.** Fit per-type T (choice, yes/no, score) by **leave-one-family-out** over the mix-tuning-dev families. These are new families, held-out samplers, packs and formats, already in the recipe's 6.4 refit rule. Choose T by the **median per-family NLL**, not pooled NLL, so that one large family cannot set it. This is the TS-CV analogue: about 71% of the oracle ECE gain in Thermometer's MMLU test.
2. **Bound T.** Keep T inside [0.8, 1.3] unless the leave-one-family-out evidence is clear. Locally, dev fits are 0.95 (yes/no) and 1.05 (choice), and the gain is about 0 (choice ECE on the eval half: 0.0330 raw, 0.0349 after T). A large T fitted on a few families can make things worse on the flipped-direction sets above.
3. **Optional, report-only Thermometer-lite.** Regress log T on unlabelled per-family features from saved probabilities:
   - mean max-prob;
   - mean entropy;
   - share of rows in the band;
   - option count;
   - mean input length.

   Fit it leave-one-family-out across the dev and mix-tuning-dev families. Promote it only if it beats the single cross-family T on held-out families by a pre-registered margin. **Unknown:** whether we have enough families. Thermometer used dozens of tasks (MMLU alone has 57 subjects). We have 9 dev splits plus the C mix-tuning-dev families.
4. **Keep three disjoint roles.** Train, calibration and confirm stay separate (Kev/pplx three-way split; recipe rule 16). The calibration families must not be in training. Otherwise the T fit is in-distribution, and that fit is exactly the one that failed for Kev (0.059 vs 0.0085-0.017).

## 3. Label-prior correction when classes are not balanced

| Method | What it needs | Numbers | Fit for us |
|---|---|---|---|
| **EM (Saerens 2002) + BCTS / vector scaling** | calibrated p(y given x) on source, plus an **unlabelled target batch** | Alexandari et al.: EM "achieves state-of-the-art results when used with an appropriate type of calibration"; BBSL and RLLS "did not tend to outperform EM when the probabilities were well-calibrated". Plain TS has "large systematic biases"; class-specific bias terms fix this. Tested with n up to 2,000 val + 8,000 target, Dirichlet shift alpha 0.1-10 | best choice **if** a batch exists; handles imbalance by design |
| BBSE (Lipton 2018) / RLLS | confusion matrix on source, target batch | lose to EM+BCTS above | no |
| **UCPA / SUCPA** (LLM text classification) | 10-600 unlabelled in-domain queries; SUCPA also needs a known class prior | beats no adaptation on 3 of 4 datasets with as few as 10 samples; on 14-class DBpedia, SUCPA was **worse** than baseline under 80 samples; if the true prior is uniform, assuming uniform beats estimating it | yes/no: fine at n >= about 50; 20-60-label taxonomies need hundreds |
| **OTTER** (optimal transport to a target label distribution) | an **estimate of the target label distribution** + unlabelled batch | +15.9% average accuracy on text, +4.8% on images; beats prior matching on 17 of 21 datasets; has error bounds for a misspecified prior | needs a prior we do not have for unseen tasks |
| Batch calibration | balanced classes | +8% / +6% over ICL (PaLM 2) | stays **risky** (`RESEARCH_small-model` 3.12) |
| Weighted conformal (Tibshirani et al. 2019) | likelihood ratio dP_test/dP_train, "known or ... estimated accurately with access to a large set of unlabeled data" | coverage guarantee under covariate shift | no: we serve one request at a time, and our endpoint is not set coverage |

Sources: [Alexandari et al. 2020](https://arxiv.org/abs/1901.06852), [UCPA, Estienne 2023](https://arxiv.org/abs/2307.06713), [OTTER](https://arxiv.org/abs/2404.08461), [Tibshirani et al. 2019](https://arxiv.org/abs/1904.06019).

**Why it stays secondary:**
- JevBench v1.5 Speed and Cost are measured "serial, one decision per request", and a batched view "does not enter the v1.5 composite" (METHOD-v1.5 section 5).
- Any prior adapted on the test batch uses the test set's own label mix. That is transductive, so it must not become the headline.

**Concrete rule:** at most one pre-registered **secondary** readout, "EM + BCTS prior-adapted, per whole set". The yes/no prior is fitted on that set's unlabelled rows, and BCTS is fitted on dev. It is reported next to the plain readout on the sealed suite and ejs-5, and never used for selection.

**A data lever instead (no serving change):**
- Make the C training mix's yes/no prior near 50/50 *within each family*. C1's dev yes/no is already 225/225 on `dev`.
- Vary the per-family gold-NEI rate, so the model does not learn one fixed prior per format. Its prior then stays close to the "assume uniform" case that UCPA found best when the true prior is unknown.

## 4. Multi-view averaging, the v1.5 band, and E on Score rows

### 4.1 Mechanism
- **Yes/no.** If two views agree in sign, the mean of their sigmoids is nearer 0.5 than the sigmoid of their mean logit. So prob-mean is always the softer of the two.
  - Example: views 0.95 and 0.60 give prob-mean **0.775** (in the band, so an abstention, scored wrong) and logit-mean **0.842** (committed yes).
- **Ensembles of calibrated members are underconfident.** "ensembling multiple calibrated models decreases the confidence of final prediction". The fix is to calibrate the *ensemble output*, not the members ([Wu & Gales 2021](https://arxiv.org/abs/2101.05397)).
- **Logit vs probability averaging** ([Njieutcheu Tassi et al. 2022](https://ceur-ws.org/Vol-3215/19.pdf)):
  - Logit averaging keeps accuracy (85.36%) and raises confidence (73.35% → 80.04%).
  - ECE improves for underconfident models (MC dropout CIFAR-10: 12.03% → 5.44%).
  - ECE worsens for overconfident ones (3.03% → 7.40%).
  - They recommend probability averaging where telling true from false predictions matters most.
- **Prompt and permutation ensembles calibrate overconfident instruction-tuned LLMs without training** (CAPE, ICML 2023 workshop, [OpenReview](https://openreview.net/pdf?id=L0dc4wqbNs)). I could not read the full text (bot wall), so **no CAPE numbers are claimed here**.

### 4.2 Local measurements, C1 dev (`q35_4b_main500k` + its seeded `_perm` read)

| Readout | yes/no in band | v1.5 committed acc (no band edge) | argmax acc | Brier | ECE | Brier / ECE after band edge |
|---|---|---|---|---|---|---|
| 1-view | 26.3% | 67.6 | 85.2 | 0.1096 | 0.0264 | 0.1157 / 0.0577 |
| 2-view prob-mean | 26.2% | 67.7 | 85.0 | 0.1096 | 0.0271 | 0.1167 / 0.0598 |
| 2-view logit-mean | 26.2% | 67.7 | 85.0 | 0.1096 | 0.0275 | 0.1167 / 0.0598 |

- The yes/no views (letter swap) differ by a mean |dP| of 0.0043 (p99 0.048). Only 12 rows enter the band and 16 leave it. **C1 is letter-order-robust on yes/no, so a second yes/no view adds nothing.** This agrees with A5's yes/no 2-view result of -0.18 to -0.28.

| Choice readout (3,814 rows) | acc | mean conf | ECE | NLL | T refit (fit half → eval half ECE) |
|---|---|---|---|---|---|
| 1-view | 77.14 | 0.792 | 0.0318 | 0.6274 | 1.05 → 0.0349 |
| 2-view prob-mean | 77.37 | 0.790 | 0.0380 | 0.6224 | 1.05 → 0.0361 |
| 2-view logit-mean | 77.37 | 0.791 | 0.0369 | 0.6231 | 1.05 → 0.0346 |

- The choice views disagree more: mean TVD 0.034, argmax flips 4.6%.
- 2-view gains +0.23 accuracy and improves NLL, but ECE gets about 0.005-0.006 worse, which is the Wu & Gales effect. A refitted T does not fix it on dev.
- Prob-mean and logit-mean are within noise of each other.

### 4.3 Synthetic stress (when views really disagree, for example paraphrase views)
Setup: K = 4 views made from C1's dev yes/no logits plus independent Gaussian noise of SD s on the logit scale. This is an upper-bound model, because real views are correlated.

| s | readout | in band | v1.5 committed acc | argmax acc | Brier | ECE | Brier / ECE after band edge |
|---|---|---|---|---|---|---|---|
| 0.5 | one noisy view | 27.2% | 66.4 | 84.5 | 0.1143 | 0.012 | 0.1216 / 0.046 |
| 0.5 | K=4 prob-mean | 27.7% | 66.3 | 85.2 | 0.1108 | 0.024 | 0.1161 / 0.051 |
| 0.5 | K=4 logit-mean | 26.2% | 67.5 | 85.2 | 0.1108 | 0.022 | 0.1162 / 0.050 |
| 1.0 | one noisy view | 30.9% | 61.9 | 82.7 | 0.1278 | 0.018 | 0.1358 / 0.054 |
| 1.0 | K=4 prob-mean | **33.4%** | **61.3** | 84.2 | 0.1155 | 0.024 | 0.1241 / 0.036 |
| 1.0 | K=4 logit-mean | **27.4%** | **66.3** | 84.4 | 0.1146 | **0.007** | 0.1226 / 0.042 |
| 1.5 | K=4 prob-mean | **42.2%** | **53.2** | 83.8 | 0.1239 | 0.037 | 0.1291 / 0.023 |
| 1.5 | K=4 logit-mean | **29.2%** | **64.1** | 83.9 | 0.1211 | 0.014 | 0.1267 / 0.042 |

**Reading:**
- Without band edge, prob-mean over disagreeing views loses 5-11 points of v1.5 committed yes/no accuracy relative to logit-mean, at the same argmax accuracy. That is the soft-answer penalty.
- With band edge (JevBench only), Intelligence equals argmax accuracy for both, so the difference moves to the Calibration axis. Band edge after prob-mean snaps more rows to 0.8/0.2. In this sim that hurt Brier slightly (+0.002) but sometimes lowered ECE, so the effect has no consistent sign.
- **The commit and band-edge rules must be refitted on dev after any change to aggregation.** No band-edge result from a 1-view read carries over.

### 4.4 Score rows (E = expected level)
- v1.5 scores Score rows by the nMAE of the **expected position** when a distribution is returned (METHOD-v1.5 section 3.1).
- **Prob-mean:** E of the averaged distribution = the mean of per-view E. By the triangle inequality, |mean E_k - gold| <= mean |E_k - gold|. So the averaged nMAE is never worse than the average single-view nMAE. (It can still be worse than one particular view.)
- **Logit-mean (geometric mean, renormalised):** E is not the mean of per-view E. The distribution sharpens toward the levels the views share, so E shifts nonlinearly.
- Averaging also flattens the distribution, which moves normalised RPS and top-level ECE, the v1.5 Score calibration parts.
- **Rule:** Score rows use prob-mean, if views are used at all. Any T for score rows is fitted after aggregation. No Score views are pre-registered now, so this applies only if a future amendment adds them.

### 4.5 Pipeline rule (proposed amendment text, for the owner)
1. **Views:** choice = 2-view (given + exact reversal), prob-mean, as in A5. Yes/no = single read. Score = single read.
2. **Temperature:** per type, fitted **on the aggregated dev or mix-tuning-dev output of the exact served pipeline**, leave-one-family-out, median-family NLL, bounded to [0.8, 1.3].
3. **Band edge** (JevBench only, disclosed): P(yes) in (0.5, 0.8) → 0.8 and P(yes) in (0.2, 0.5] → 0.2, applied *after* step 2. Never applied on OHS or sealed Brier endpoints.
4. **D4 and the Brier report** use steps 1-2 exactly as served. Add a report-only Brier and over/underconfidence gap on the **unseen-family** mix-tuning dev, because dev-wide D4 is blind to shift miscalibration (section 1).
5. If K is ever above 2 or yes/no views are added, aggregate by **logit-mean** for yes/no, then redo steps 2-3 from scratch.

## 5. What this means for the C data and recipe (actionable, all $0)

| # | Lever | Expected effect | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Hold out >= 8 whole families or sources as calibration-only (not train, not confirm) | ECE on unseen tasks: TS-CV keeps about 71% of the oracle gain | Thermometer TS-CV 0.119 vs 0.260 vs oracle 0.062; Kev 0.059 → 0.0085-0.017 | USE |
| 2 | Leave-one-family-out per-type T, median-family NLL, bounded | avoids a T driven by one family; accuracy 0 | Ovadia (in-distribution TS fails under shift); local direction flips | USE |
| 3 | Fit T after aggregation, on the served pipeline | removes the 2-view ECE drift (0.032 → 0.038) from D4 noise | Wu & Gales; local table 4.2 | USE |
| 4 | Yes/no single read; logit-mean if yes/no views ever appear | protects v1.5 committed accuracy (+5 to +11 vs prob-mean at view SD 1-1.5) | local sim 4.3; Tassi | USE |
| 5 | Keep soft vote-share labels and KD, plus band edge on JevBench only | keeps Brier; band edge commits the 26-38% of rows in the band | READOUT_DEV (3): band edge Brier +0.004 to +0.006 on dev | USE (as A5) |
| 6 | Per-family 50/50 yes/no prior and varied NEI rates in C data | keeps the prior near the "assume uniform" optimum | UCPA (uniform beats estimating when the prior is unknown or small n) | USE (data rule) |
| 7 | EM + BCTS per-set prior adaptation | gain unknown on our sets; may help imbalanced sets | Alexandari; UCPA; OTTER | report-only secondary |
| 8 | Thermometer-lite T predictor | possibly ECE 0.119 → 0.078-like, if enough families | Thermometer | report-only, until it beats item 2 on held-out families |
| 9 | Selective calibrator trained on source + known OOD (Kamath) | coverage 48% → 56% at 80% accuracy (SQuAD) | Kamath 2020 | not applicable: our endpoints have no abstain/coverage axis; skip |
| 10 | Batch calibration, OTTER, weighted conformal at serve time | needs batches or label priors we do not have per request | sources above | NO |

## 6. Unknowns
- Whether C's held-out families are enough (count and diversity) for a Thermometer-style predictor. Thermometer's exact per-benchmark task counts were not extracted, apart from MMLU's 57 subjects.
- C1's real paraphrase-view disagreement (the 4.3 sim assumes independent noise, which is an upper bound). It needs a paraphrase read, which is a GPU step and not done here.
- Why the OHS-1 Brier in the recipe (0.140 vs 0.114) differs from my recompute on all yes/no rows (0.152 vs 0.133).
- Whether the sealed JevBench half shifts calibration the same way. v1.5 pools open and sealed items for the Calibration axis, so shift there feeds straight into the axis.
- CAPE's exact ECE numbers (OpenReview blocked the fetch).

## Sources
- Ovadia et al. 2019, Can You Trust Your Model's Uncertainty?: https://arxiv.org/abs/1906.02530
- Thermometer (ICML 2024): https://arxiv.org/abs/2403.08819, numbers from https://arxiv.org/html/2403.08819
- The Well-Tempered Classifier (2026): https://arxiv.org/abs/2602.14862
- OTTER: https://arxiv.org/abs/2404.08461
- Alexandari, Kundaje, Shrikumar (ICML 2020), EM + BCTS: https://arxiv.org/abs/1901.06852
- Estienne 2023, UCPA / SUCPA: https://arxiv.org/abs/2307.06713
- Kamath, Jia, Liang 2020, Selective QA under domain shift: https://arxiv.org/abs/2006.09462
- Tibshirani et al. 2019, weighted conformal: https://arxiv.org/abs/1904.06019
- Wu & Gales 2021, Should ensemble members be calibrated?: https://arxiv.org/abs/2101.05397
- Njieutcheu Tassi et al. 2022, averaging logits vs probabilities: https://ceur-ws.org/Vol-3215/19.pdf
- CAPE (prompt ensembles): https://openreview.net/pdf?id=L0dc4wqbNs
- Local: `bench/jevbench_v154/docs/METHOD-v1.5.md` (3.1, 5); `prep89/READOUT_DEV.md` (3), (4); `bench/v154/RESULTS_30sep.md`.
- Scratch scripts (not in repo): `agg_sim.py`, `agg_ch_T.py` in the session scratchpad. Inputs: `preds_dev*/q35_4b_main500k{,_perm}.jsonl`, `preds_ohs*/q35_4b_main500k_b100_a5.jsonl`, `preds_ohs*/jev_guard.jsonl`, `data/{dev splits, ohs, ohs2}.jsonl`.
