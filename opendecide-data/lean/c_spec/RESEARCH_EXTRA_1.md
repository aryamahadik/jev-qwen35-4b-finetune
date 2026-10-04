# RESEARCH_EXTRA_1: training and calibrating for the expected-level readout on ordinal Score rows

Date: 3 Oct 2026. CPU only. No Modal, gcloud, ssh or paid calls.

What was read:
- ejs-5 run files `bench/ejs5/runs/{c1_main500k,e4b_pxE}/preds.jsonl` (probabilities only).
- The already-scored aggregates in `bench/ejs5/runs/scores_c1_4be.json`.
- The JevBench v1.5.4 scorer `bench/v154/v154lib.py`.
- Dev gate rows. These are our own dev data, and gold was used there.

What was not read:
- ejs-5 gold and item text. `bench/external_quarantine/` was never opened.
- Anything under data/ohs3*, prep89/dryrun/, or the C_DATA_SPEC / C_TRAIN_RECIPE files (read-only grep, no edits).

Pre-registration lines are in `progress_completeness.log`. They were written before the counts below were computed. The only change was one amendment adding T = 1.6, which was also logged before it was computed.

## TL;DR

1. **Both headline Score tests read the mean of our distribution, never its top option.**
   - On ejs-5 Size, the answer is `round_half_even(E)` (`ejs5lib.decide`).
   - On JevBench v1.5.4 Score, the grade is `|E - gold| / (K-1)` on the *unrounded* E (`v154lib.py:111`), plus an RPS calibration term.
   - Plain CE plus vote-share KD trains the top option and calibration. It does not train E.
2. **The main loss on ejs-5 Size is not the rounding. It is the top level.**
   - C1 outputs `large` on 4 of 360 rows with rounded E, and on 6 of 360 with argmax.
   - The author says the tasks are class-balanced (PREREG_ejs5 §1), so about 90 `large` rows are expected. About 86 of them are wrong whatever readout is used.
   - Rounding pushes answers to the middle: `tiny` 97 -> 34 and `small` 154 -> 230.
3. **The readout and temperature lever is small and its sign is unknown.**
   - On the ejs-5 select half (177 rows, counts only), T = 0.5 changes 30 rows. All 30 are adjacent moves (25 small->tiny, 5 small->medium). No T creates a `large`.
   - On 129 dev ordinal rows with gold, rounded E vs argmax differs by at most 4 rows: C1 51.2 vs 48.1, 4B-E 49.6 vs 50.4.
   - The literature says the same thing (RAFT, and the Jev rubric-judge paper). The decoding rule moves little. The trained probabilities move a lot.
4. **Danger: a calibration temperature makes this worse.**
   - The NLL-optimal T for C1 on dev ordinal rows is **1.6** (over-confident).
   - On the ejs-5 select half, T = 1.6 collapses Size to two levels: tiny 0, small 137, medium 40, large 0.
   - If recipe item 13 fits a per-type temperature, it must not touch the probabilities that feed E on Score rows.
5. **Cheapest real lever (training): add a mean term on ordinal rows only.**
   - The loss is `CE + 1.0 * (E - y)^2` on ordinal rows, plus a data lint that every ordinal training target satisfies `round_half_even(E_target) == gold`.
   - Evidence comes from in-domain studies. Gemma-2 2B on Amazon Wireless: RMSE 0.70 (CE + greedy) -> 0.67 (CE + expected value) -> **0.47 (RAFT loss)**. TRACT r = 0.557 -> 0.623 (no CoT). Mean-variance loss MAE 3.32 -> 2.51.
   - The effect on a far domain is **unknown**.
6. **2-view check: the reversed view does not flip the scale for C1.**
   - The two views agree on the argmax in 322 of 360 rows. Mean E is 1.147 in the given view and 1.180 in the reversed view. No row has |E1 - E2| >= 1.
   - 4B-E has a strong order effect: the views agree on only 136 of 360 rows (mean E 0.655 vs 0.996).

## 1. The readouts that grade Score rows (local code)

| Test | Rule | Where | What it rewards |
|---|---|---|---|
| ejs-5 Size (360 of 868 rows, 41%) | `LEVELS[max(0,min(3,int(round(E))))]`, E = sum i*p_i over [tiny, small, medium, large]; Python `round` = ties to even | `bench/ejs5/ejs5lib.py` `decide()` | E inside +-0.5 of the gold level |
| JevBench v1.5.4 Score (headline is Choice+Score) | nMAE = \|E - gold\|/(K-1) on unrounded E; score = 100*(1 - mean nMAE / mean chance nMAE); nRPS feeds the calibration column; `top_correct` (argmax) is reported beside it | `bench/v154/v154lib.py:104-141` | E close to gold (absolute error) |
| Jev's own Score primitive | returns the expected level, rounded to the nearest level, ties to even | arXiv 2609.29769 §3.1 | same as ejs-5 |

**Which distributions can output an end level under rounded E** (K = 4, levels 0..3):

- `large` needs E > 2.5 (2.5 rounds to 2). That means **3*p(tiny) + 2*p(small) + p(medium) < 0.5**, so p(large) must be above 0.5 even in the best case.
- `tiny` needs **p(small) + 2*p(medium) + 3*p(large) <= 0.5**.
- Argmax, by contrast, can output `large` at p(large) = 0.3.
- C1's median top probability on Size is **0.51** (`scores_c1_4be.json` calibration bins: 121 rows at 0.4-0.5 conf, 113 at 0.5-0.6).
- So the end levels are almost unreachable under rounded E. **Under this readout the model must be sharp on end-level items, and its mean must be right on middle items.**

## 2. Local CPU checks

### 2a. ejs-5 Size, full 360 rows, T = 1. Counts only (reproduces the task's numbers)

| Run | rounded-E histogram (tiny/small/medium/large) | argmax histogram | rounded-E != argmax | mean E | median top p |
|---|---|---|---|---|---|
| C1 | 34 / 230 / 92 / 4 | 97 / 154 / 103 / 6 | **78** (21.7%) | 1.164 | 0.513 |
| 4B-E | 73 / 263 / 24 / 0 | 184 / 143 / 33 / 0 | **120** | 0.826 | 0.477 |

Size task accuracy, from the already-scored aggregates:

| System | Size accuracy |
|---|---|
| C1 | 32.2 |
| 4B-E | 33.1 |
| Jev 1.13 | 37.2 |
| GPT-5.6 Terra | 40.0 |
| Opus 5 | 45.8 |

C1 minus Jev on Size is -5.0 pp [-10.8, +0.8], which is 18 rows.

Even Opus 5 gets 45.8%, so how far commit size can be inferred from this text is limited. **Unknown how much is inferable; the item text was not opened.**

From an earlier gold-free count in this session (scratchpad `goldfree_out.json`): C1's mean probability per level is tiny 0.277, small 0.363, medium 0.279, **large 0.081**. Under a balanced task that would be 0.25 each. The model's top-level probability is far too low. Rounding is a second, smaller effect.

### 2b. Temperature on the SELECT half only (sha256(id) last hex digit even; 177 rows; counts only)

T is applied per view (`softmax(logit/T)` = `p^(1/T)/Z`; view 2 = 2*probs - probs_1v, min 0.0106 > 0), and then the two views are averaged. That is exactly what `decoder_io.to_probs(temp=T)` + 2view would give. The confirm half was not computed.

| Run | T | rounded-E histogram | rounded-E != argmax | rows changed vs T=1 | moves |
|---|---|---|---|---|---|
| C1 | 1.0 | 17 / 116 / 44 / 0 | 50 | - | - |
| C1 | 0.7 | 32 / 98 / 47 / 0 | 32 | 18 | small->tiny 15, small->medium 3 |
| C1 | 0.5 | 42 / 86 / 49 / 0 | 20 | 30 | small->tiny 25, small->medium 5 |
| C1 | 1.6 (amendment) | **0 / 137 / 40 / 0** | 71 | 21 | tiny->small 17, medium->small 4 |
| 4B-E | 1.0 | 30 / 144 / 3 / 0 | 70 | - | - |
| 4B-E | 0.5 | 75 / 97 / 5 / 0 | 22 | 47 | small->tiny 45, small->medium 2 |
| 4B-E | 1.6 | 2 / 172 / 3 / 0 | 98 | 28 | tiny->small 28 |

How to read this:
- T < 1 moves rounded E toward argmax. With T -> 0 it becomes argmax.
- The lever is bounded by the 50 rows (of 177) where rounded E and argmax already differ.
- It never creates `large` (0 at every T).
- **Accuracy is unknown, because no gold was read.** Under PREREG_ejs5 §2 and REVIEW_rules N6, ejs-5 cannot choose T.

### 2c. 2-view check on ordered scales (all 360 rows; counts only)

| Run | argmax agree (given vs reversed view) | mean E given / reversed | rows with \|E1-E2\| >= 1 | median \|E1-E2\| | argmax histogram given -> reversed |
|---|---|---|---|---|---|
| C1 | **322 / 360** (89.4%) | 1.147 / 1.180 | **0** | 0.078 | tiny 110->90, small 143->164 |
| 4B-E | 136 / 360 (37.8%) | 0.655 / 0.996 | 0 | 0.341 | tiny 258->73, small 85->231 |

- C1 does not read the reversed view as a reversed scale. Its 10.6% argmax flips are within the 8.5-19.5% range that arXiv 2608.08869 reports for reversed label orders under greedy decoding.
- Averaging two views that disagree makes the distribution flatter, and a flatter distribution pulls E toward the middle. This explains 4B-E's 263 `small`. For C1 the effect is small.

### 2d. Dev ordinal rows, with gold (dev is allowed for calibration and selection under N6)

Of 157 rows flagged ordinal (`feat.py` ORD rule), 129 could be ordered by level (Low/Medium/High, "k:", Level/Tier k, Minor/Major/Critical). Those 129 rows have K = 3 (54), 4 (49), 5 (20), 6 (5) and 7 (1). The probabilities are the stored dev-gate readout.

| Model | T | rounded-E acc | argmax acc | end-level preds: rounded E / argmax / gold |
|---|---|---|---|---|
| C1 | 1.0 | **51.2** | 48.1 | **34** / 55 / 52 |
| C1 | 0.7 | 48.8 | 48.1 | 43 / 55 / 52 |
| C1 | 0.5 | 48.8 | 48.1 | 47 / 55 / 52 |
| 4B-E | 1.0 | 49.6 | 50.4 | 28 / 51 / 52 |
| 4B-E | 0.5 | 51.9 | 50.4 | 41 / 51 / 52 |

- All accuracy differences are 1 to 4 rows of 129. That is noise, and there is no consistent sign.
- The pull to the middle is real: at T = 1, rounded E gives 34 end-level answers where gold has 52.
- NLL-optimal T on these rows is **1.6 for C1** (NLL 1.129 -> 1.075; nMAE of E 0.227 -> 0.229, i.e. unchanged) and 1.25 for 4B-E.

## 3. Literature: numbers that matter here

**Mean vs mode for LLM judges.**
- Source: "Improving LLM-as-a-Judge Inference with the Judgment Distribution", EMNLP 2025 Findings, https://arxiv.org/abs/2503.03064.
- The mean beats the mode in **42 of 48** settings. GPT-4o pointwise on RewardBench goes from 84.0 (mode) to 88.0 (mean).
- But "the top pointwise methods are the continuous ones (mean, ram, qt, ps)". The rounded mean is a *discrete* method and is not among the winners.
- CoT collapses the spread. Llama-3.1-8B: mode 69.6 -> 72.2 and mean 72.7 -> 79.3 when CoT is removed. "No-CoT always has a greater standard deviation."
- **For us:** their gain comes from the unrounded mean breaking ties on continuous or pairwise metrics. It does not show that the rounded mean beats argmax on exact-level accuracy. Our dev check (2d) shows no gap.

**Decision theory (standard).**
- For exact-match (0-1) loss, the argmax of a calibrated posterior is optimal.
- For absolute error, the posterior median is optimal. For squared error, the posterior mean is optimal.
- Rounding the mean is optimal for none of them. It behaves like the squared-error optimum, which is why it pulls toward the middle.
- So the model has to make its *distribution* fit the readout. Changing the readout is not an option on ejs-5, because it is fixed by the PREREG.

**RAFT (Lukasik et al., ICLR 2025).**
- Source: https://proceedings.iclr.cc/paper_files/paper/2025/file/ae3bb0adcdce28afb5f7e86a79b6cffa-Paper-Conference.pdf
- Loss: `(y* - sum_y p(y|x) * y)^2`, i.e. squared error on the expected value over candidate score tokens.
- Table 3 RMSE, given as CE+greedy / CE+expected value (RAIL) / RAFT:

| Model, dataset | CE+greedy | CE+RAIL | RAFT |
|---|---|---|---|
| Gemma-2 2B, Amazon Wireless | 0.70 | 0.67 | **0.47** |
| Gemma-2 2B, Personal care | 0.77 | 0.74 | 0.49 |
| Gemma-2 2B, Music | 1.16 | 0.88 | 0.50 |
| Gemma-2 9B, STSB | 0.58 | 0.53 | 0.51 |

- **For us:** switching the decoding rule on a CE-trained model gives a small gain. Training the expected value directly gives a large one.

**TRACT (ACL 2025).**
- Source: https://arxiv.org/abs/2503.04381
- Loss: `lambda * (sum_y p(y)*y - y*)^2 - log p(...)`, with **lambda = 1**, scores 1-5, Mistral-7B and Llama-3.1-8B.
- Pearson r: CE only 0.557, RAFT without CoT **0.623**, with self-CoT 0.650.
- We use no CoT at inference, so the no-CoT row is the one that applies.

**Jev vs LLMs as rubric judges.**
- Source: https://arxiv.org/html/2609.29769v1
- Jev Score is the expected level, rounded with ties to even. Exact accuracy, Jev Choice vs Jev Score:

| Panel | Jev Choice | Jev Score |
|---|---|---|
| FED-Turn | 56.2 | 66.7 |
| USR-TC | 62.0 | 66.2 |
| ELLIPSE | 13.4 | 15.3 |
| HelpSteer2 | 48.6 | 44.4 |

- Score has higher within-one accuracy on all 7 panels.
- Re-decoding each primitive's probabilities with the other's rule shows "most or all of the difference comes from the probabilities ... little or none from the decoding rules".
- Judges place items lower than the labels on 6 of 7 panels. On ELLIPSE, Jev Choice is 86.1% below the label, an offset of -1.25 levels. The labels put 36.3% at the top two levels, and no judge puts more than 4.2% there.
- **For us:** Jev's Score probabilities appear to be shaped for the mean readout. How Jev trains them is unknown. Top-level suppression is a shared failure (our `large` 4 of 360), not ours alone.

**Mean-variance loss (Pan et al., CVPR 2018).**
- Source: https://vipl.ict.ac.cn/research/biometric/hylw/202205/W020220526349470642776.pdf
- Loss: `L = CE + (lambda1/2)(m - y)^2 + lambda2 * Var`, with **lambda1 = 0.2, lambda2 = 0.05**.
- Inference is **round(sum_j j*p_j)**, which is our ejs-5 rule.
- MORPH II MAE: 3.324 -> 2.514 (RS protocol) and 4.043 -> 3.086 (SE protocol).
- Setting lambda1 = 0 or lambda2 = 0 is worse. The mean term matters more than the variance term.
- Their scale is ages (K ~ 100). On our K = 3-7 scales, (m - y)^2 <= 36, so the weights need re-scaling. **Unknown for LLMs.**

**CORAL and CORN.**
- Sources: https://arxiv.org/abs/1901.07884 , https://arxiv.org/abs/2111.08851
- CORN Table 3 MAE, CE / CORAL / CORN:

| Dataset | CE | CORAL | CORN |
|---|---|---|---|
| MORPH-2 | 3.73 | 2.99 | 2.98 |
| AFAD | 3.28 | 2.99 | 2.81 |
| Fireman | 0.80 | 0.82 | 0.76 |

- These methods need K-1 binary heads, which our one-pass letter readout does not have.
- A data-side analog is possible: auxiliary "is it at least level k?" yes/no rows. This is **untested for LLMs**.

**SORD soft labels (Diaz & Marathe, CVPR 2019).**
- Source: https://openaccess.thecvf.com/content_CVPR_2019/papers/Diaz_Soft_Labels_for_Ordinal_Regression_CVPR_2019_paper.pdf (403 on fetch; formula from secondary sources).
- Targets are `softmax(-phi(y, i))`. Computed here for K = 4, gold = 0:
  - Gaussian phi = alpha*(i-y)^2 needs **alpha > 0.526**. Otherwise the target's own E is >= 0.5, and a perfectly fitted model answers `small`. At alpha = 0.5, E = 0.519.
  - |i-y| distance needs alpha > 1.012.
  - Uniform label smoothing needs eps < 1/3 (K = 4) or eps < 1/6 (K = 7). C1's 0.05 and 0.08 are safe.
- AMOL "center-class hedging" (https://arxiv.org/html/2609.10752, tabular only):
  - Abalone QWK: CE 0.693, SORD 0.717, AMOL 0.735.
  - Center-hedging rate: CE 0.074 -> 0.000.

**Label-order reversal.**
- Source: https://arxiv.org/html/2608.08869
- Reversing the label order flips 8.5-19.5% of greedy predictions. Averaging over both orders changed accuracy by -1.1%.

**G-Eval.**
- Source: https://arxiv.org/abs/2303.16634
- Probability-weighted scores on SummEval: average Spearman 0.514 vs 0.502 without probabilities, but Kendall 0.418 vs 0.446. A small and mixed effect.

## 4. Recommendations for C (ranked; none edits the spec or recipe here)

| # | What | Where | Cost | Evidence | Check |
|---|---|---|---|---|---|
| R1 | **Ordinal target lint.** For every ordinal training row, map options to level index (the recipe says ordinal labels carry their level number). Compute E of the *actual training target* (CE target after smoothing, KD target, vote shares). Require `round_half_even(E_target) == gold`; repair or drop failures. Example: vote shares 0.55/0.35/0.10 on gold `tiny` give E = 0.55, which reads as `small`. A C1 KD anchor with p_top = 0.8 and 0.2 on the far end gives E = 0.6, which is wrong. | data builder | $0 | 3 (SORD thresholds) | lint pass rate = 100% |
| R2 | **Level balance with real end levels.** In F7 ordinal rubrics and any score rows, gold is spread evenly over levels, ends included (>= 1/K each). Add numeric cut-point rubrics: a quantity binned by stated thresholds, where the evidence is indirect, and where the top level is as common as the others. Do not build commit-size items. That would teach to the test. | C_DATA_SPEC F7 | $0 extra rows (inside F7's 7%) | 2a (large 4/360), 2d (ends 34 vs 52), 2609.29769 (top-level suppression) | dev ordinal: end-level preds / gold-end ratio from 0.65 -> >= 0.9 |
| R3 | **Mean term on ordinal rows only:** `L = CE(+KD) + lambda * (E - y)^2`. E is taken over the letter probabilities mapped to level index, y is the gold level index, and **lambda = 1.0** (TRACT default; 1-5 scale, similar to our K = 3-7). Use **no variance term**, to keep calibration for JevBench nRPS/Brier and OHS Brier. It only applies to rows with level numbers, about 7% of the mix. | C_TRAIN_RECIPE losses | small code change, no extra GPU | RAFT 0.67 -> 0.47; TRACT 0.557 -> 0.623; MV 3.32 -> 2.51 | dev ordinal rounded-E acc and nMAE(E); sealed-suite select half Score slice; far-domain effect **unknown** |
| R4 | **Never apply a calibration T > 1 to Score probabilities that feed E.** If recipe item 13 refits a per-type T, either exclude score/ordinal rows or apply T only to the *reported confidence*. | recipe item 13 | $0 | 2b: T = 1.6 gives 0 tiny and 0 large on 177 rows | assert in readout code |
| R5 | **Do not use T < 1 as a lever.** Dev shows no gain (C1 48.8 at T = 0.5 vs 51.2 at T = 1), and ejs-5 cannot choose T. If it is ever tried, fit on dev or the sealed select half only, pre-register, and keep ejs-5 report-only. | - | $0 | 2b, 2d | - |
| R6 | **Keep the shipped 2-view readout.** For C1 the reversed view does not flip the scale (2c). In training permutations, show an ordinal scale only in natural or fully reversed order, never shuffled (competitor lesson J: "do not reverse ordered score scales"). Track view agreement on ordinal rows: C1 89.4%; 4B-E 37.8% is the warning case. | recipe perm twins | $0 | 2c, 2608.08869 | dev ordinal 2-view agreement >= 89% |
| R7 | **No CoT at inference** for Score (already the design). | - | $0 | 2503.03064: CoT collapses the spread | - |

**Expected size of the effect.**
- Rounded E vs argmax alone: about 0 on dev, and at most ~30 rows per ejs-5 half, sign unknown.
- R1 + R3 directly target the end-level reachability that costs the most rows. How many of the 18 Size rows they recover on ejs-5 is **unknown**. All loss evidence is in-domain, and how much of `large` can be inferred from the text is unknown.
- Cost is $0 extra data and no extra GPU budget. It fits the one-candidate rule as part of the C recipe, not as a separate arm.

## 5. Unknowns

- Whether the ejs-5 Size text contains enough signal for `large`. It was not opened. The best published model, Opus 5, gets 45.8%.
- How Jev's Score primitive is trained. The paper only shows that its probabilities, not its rule, make the difference.
- The right lambda for R3 on a 4B LoRA with a letter readout. No LLM paper uses this readout. lambda = 1 is borrowed from TRACT.
- The exact class counts on ejs-5 Size. "Class-balanced" is the author's statement (PREREG_ejs5 §1), not verified by us.

## Files

- Scripts (scratchpad, read-only on repo):
  - `/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/73bb87c6-8519-454d-98bb-7961fcde73b9/scratchpad/tcheck.py`, `tcheck2.py` (ejs-5 counts)
  - `devord.py`, `devord2.py`, `devord3.py` (dev ordinal)
- Output: `tcheck_out.json`.
