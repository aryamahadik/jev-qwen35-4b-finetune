# RESEARCH_EXTRA_2: what causes C1's -4.4 pp on ejs-5? Split the gap by cause before spending the $100

Scope: CPU only. I read only `bench/ejs5/runs/{c1_main500k,e4b_pxE}/preds.jsonl` (probabilities only, with no gold and no
text), the aggregates in `bench/ejs5/runs/scores_c1_4be.json`, and the published table in `bench/ejs5/PREREG_ejs5.md` §5
(Jev, GPT-5.6 Terra and Opus 5: all rows and late rows). I did **not** open `bench/external_quarantine/`, so nothing here
uses per-row gold. Numbers marked **(derived)** come from aggregates plus one stated assumption. Numbers marked
**(measured)** come straight from the files. Section 7 gives a counts-only script and the rules for reading it; it pins down
what I can only bound here.

---

## 0. Bottom line

1. **Most of the gap is on early rows, and that pattern comes from Jev, not from C1.**
   - C1 is 39 items behind Jev on the 600 early rows and 1 item ahead on the 268 late rows (measured).
   - Every other system gains on Jev from early rows to late rows: C1 +6.9 pp, 4B-E +4.2, GPT-5.6 +3.4 and Opus 5 +8.8
     (derived from the PREREG table).
   - Jev drops the most from early rows to late rows: -18.3 pp, against -9.4 to -14.9 for the others.
   - So Jev has an early-row edge of about 6 pp over the field. Over 600 rows that is about 20-41 of the 38 missing items.
   - The 95% interval is wide: the SE of the DiD is about 3.6 pp, so the interval runs from about 0 to all of the gap.
2. **The time effect is almost all in Score (Size).**
   - Score: C1 vs Jev is -10.6 pp on early rows and +7.0 pp on late rows, a swing of +17.6 pp. That is 7.3 of the
     task-mix-weighted DiD of 7.8 pp.
   - Triage swings +4.0 pp.
   - **Gate goes the other way:** -4.4 early and -12.1 late. The gate gap is not about time.
   - 4B-E shows the same pattern: score +10.0, triage +9.1, gate -3.8.
   - **Untested confound:** C1 answers "small" on 230 of 360 Score rows. If the late Score rows hold more true "small"
     items, the "time" swing could be a label-mix effect. Only the counts-only step A in §7 can separate the two.
3. **Label-prior shift is real but explains little.**
   - On Gate (Risk), C1 says "yes" on only 36 of 180 rows (20%). Mean P(yes) is 0.312.
   - In-domain, C1 leans "yes" (REVIEW_methods S8), so the yes/no prior flips on this far domain.
   - Assuming the 90/90 balance the PREREG states, C1's Gate ranking is weak (derived): AUC about 0.58. The best
     threshold would reach about 57-60%. Jev's 63.9% needs AUC ≥ about 0.69.
   - So a prior or threshold fix recovers at most about 4-6 of Gate's 13 missing items. The rest is skill.
4. **The Score readout matters less than it looks.**
   - The rounded expected level differs from argmax on 78/360 rows (C1) and 120/360 rows (4B-E).
   - C1 is 17.5 pp overconfident on Score: it expects 49.7% and gets 32.2%.
   - Natural experiment: C1 and 4B-E predict very different Score label mixes and disagree on 127/360 rows, yet their
     scores differ by only 3 items (116 vs 119). Moving predictions around on a near-chance task is a wash.
   - Estimate: the readout is worth 0 to about 5 of Score's 18 missing items.
5. **Gate is the one deficit that is a real, time-independent skill gap**: 13 items, worse on late rows, and seen in both 4B
   adapters. It is also where the C data plan has an **input-form mismatch**:
   - ejs-5 shows **commit prose only**, with paths and giveaway terms stripped (PREREG_ejs5 §7).
   - The spec's commit block shows **message + diff + numstat** (C_DATA_SPEC §4.2).
   - A model trained to read diffs and numstat is learning a different skill from the one ejs-5 Gate and Score test.
6. **Implication for the $100:**
   - The breadth-heavy plan is not aimed at what drives the ejs-5 full-set number. That number is driven mostly by
     Jev's early-row edge (time) and by near-chance Score.
   - Breadth may still help the sealed suite and OHS-style tests. But "the sealed gain will show on ejs-5 full" should be
     dropped as an expectation.
   - The data lever with the best evidence is **Gate-style yes/no risk judgement from short technical prose, with varied
     base rates**.
   - Run §7 ($0, CPU, about 1 minute) before the C mix is frozen.

---

## 1. Gap accounting: C1 minus Jev, in items (measured)

Source: `scores_c1_4be.json` (`vs_jev.per_task`, `late_per_task`). Early = 868 - 268 = 600 rows, including the 1 undated
row.

| Task | All rows | Early rows | Late rows | Early pp | Late pp | Late - early (pp) |
|---|---|---|---|---|---|---|
| route (n 180 / 142 / 38) | 0 | -2 | +2 | -1.4 | +5.3 | +6.7 |
| triage (148 / 99 / 49) | -7 | -6 | -1 | -6.1 | -2.0 | +4.0 |
| score (360 / 245 / 115) | **-18** | **-26** | **+8** | -10.6 | +7.0 | **+17.6** |
| gate (180 / 114 / 66) | **-13** | -5 | **-8** | -4.4 | -12.1 | **-7.7** |
| **pooled (868 / 600 / 268)** | **-38** | **-39** | **+1** | -6.5 | +0.4 | +6.9 (task-mix-weighted +7.8) |

The same table for 4B-E (`q35_4b_pxE`): route +1 / +1 / 0; triage -9 / -9 / 0; score -15 / -18 / +3; gate -12 / -6 / -6.
Both adapters show the same pattern, so it is a property of the base model plus ejs-5, not adapter noise.

---

## 2. Cause (b): time and pretraining exposure

### 2.1 The early-vs-late drop for each system (derived from the PREREG_ejs5 §5 table and `scores_c1_4be.json`)

Hits are reconstructed from the published accuracies (e.g. Jev 58.53% × 868 = 508; late 45.90% × 268 = 123).

| System | Early 600 | Late 268 | Drop | Gap vs Jev, early | Gap vs Jev, late | DiD vs Jev |
|---|---|---|---|---|---|---|
| Jev 1.13 | 64.2 | 45.9 | **-18.3** | - | - | - |
| GPT-5.6 Terra | 65.7 | 50.7 | -14.9 | +1.5 | +4.9 | +3.4 |
| Opus 5 | 71.0 | 61.6 | -9.4 | +6.8 | +15.7 | +8.8 |
| C1 (4B) | 57.7 | 46.3 | -11.4 | -6.5 | +0.4 | **+6.9** |
| 4B-E (4B) | 58.8 | 44.8 | -14.1 | -5.3 | -1.1 | +4.2 |

How to read the table:
- Late rows are harder for everyone, which comes from row mix and difficulty.
- Jev is the outlier. Every system, from a 4B LoRA up to Opus 5, gains on Jev on late rows.
- C1's DiD (+6.9) is close to the mean of the two frontier models (+6.1). So C1 behaves like the field over time, and Jev
  has an early-row edge of about 6 pp.
- In items:
  - 6.1 pp × 600 ≈ 37 items, using the field mean;
  - 3.4 pp × 600 ≈ 20, using GPT alone;
  - 6.9 pp × 600 ≈ 41, using C1's own DiD.
- That is 20 to 41 of the 38 missing items.
- The SE of one DiD is about 3.6 pp (REVIEW_methods S4: z ≈ 1.9), so each interval includes 0. The four DiDs all share
  Jev, so they are not independent evidence.

### 2.2 Is "Jev saw n8n's history" plausible? What the literature says

- **Time splits do expose contamination in code.**
  - LiveCodeBench (Jain et al., arXiv 2403.07974, ICLR 2025): DeepSeek models "starkly drop" on LeetCode problems
    released after their Sept 2023 release, and GPT-4o drops after its Nov 2023 cutoff. They used monthly windows,
    May 2023 to Feb 2024. https://arxiv.org/abs/2403.07974
  - Roberts et al. (ICLR 2024, arXiv 2310.10628) fit `DV ~ (Difficulty + GitHub presence) × postCutoff`.
    - Before the cutoff, each log-unit of GitHub presence raises GPT-4's pass odds by **4.5%** on Codeforces and
      **47.8%** on Project Euler (GPT-3.5: 2.5% and 27.7%).
    - After the cutoff the association is **not significant**.
    - Project Euler had 73 post-cutoff problems; no model solved any of them.
    - Difficulty stays significant after the cutoff, so a performance drop alone does not prove contamination. The
      **interaction** is the evidence. https://arxiv.org/abs/2310.10628
- **Repository-specific memorization is large for path-like labels.**
  - In "The SWE-Bench Illusion" (arXiv 2506.12286), models name the buggy file path from the issue text alone **76%** of
    the time on SWE-Bench Verified, against **≤53%** on repos outside the benchmark.
  - Verbatim 5-gram function reproduction: **35%** vs **18%**.
  - All four ejs-5 labels are commit metadata: package tree, commit prefix, churn bucket and files touched (PREREG §7).
    A model that memorized n8n's history can recover them.
  - https://arxiv.org/abs/2506.12286
- **Bigger models memorize more, even with the same cutoff.**
  - Carlini et al. (arXiv 2202.07646): "a ten fold increase in model size corresponds to an increase in memorization of
    19 percentage points".
  - Larger models in one family memorize 2-5× more.
  - Jev's size is unknown; the memory note estimates ≤30B active. So even if Qwen3.5-4B saw the same early commits, Jev
    would recall more of them.
  - https://arxiv.org/abs/2202.07646
- **C1's base date:** Qwen3.5-4B was released on **2 Mar 2026** (https://llm-stats.com/models/qwen3.5-4b). Its exact cutoff
  is not published, so it is unknown. Late rows (from 1 Jun 2026) are therefore after C1's base, while early rows may be
  inside it. Jev 1.13's cutoff and the run date are **unknown**.
- **Caution: a time split also changes the distribution.**
  - Duan et al. (arXiv 2402.07841): MIAs on same-distribution members barely beat chance (AUC ≈ 0.5). Earlier "success"
    came from a **temporal distribution shift**.
  - Das et al. (arXiv 2406.16201): **blind** baselines that never look at the model beat state-of-the-art MIAs on 8
    date-split datasets.
  - Implications:
    - (i) A single model's early-vs-late drop says nothing about memorization. Only the **between-system DiD** nets out
      the shift.
    - (ii) A Min-K%-style probe on Qwen3.5-4B over early vs late commit text would be confounded. Do not spend on it.
  - https://arxiv.org/abs/2402.07841 , https://arxiv.org/abs/2406.16201
- **Black-box detection on Jev is not available to us.**
  - "Time Travel in LLMs" (Golchin & Surdeanu, arXiv 2308.08493) asks the model to complete a test instance given the
    dataset name and partition. It reached 92-100% accuracy against human judgement.
  - It needs new Jev calls. Our rules forbid them, so it is out. https://arxiv.org/abs/2308.08493

### 2.3 The confound I cannot rule out on CPU without gold: label mix inside Score

- C1's Score predictions under the official readout: small 230, medium 92, tiny 34, large 4 (measured, gold-free).
- 4B-E's: small 263, tiny 73, medium 24.
- The full set is balanced by construction (90 per level), but the late subset need not be.
- If late Score rows are, say, 40% "small", a small-heavy predictor gains on late rows mechanically. That would look like
  a time effect while actually being a prior-times-mix effect.
- Late Score has low C1-vs-Jev discordance: the bootstrap CI width suggests about 16% of rows, against about 40% on
  early rows (derived from the CI widths). That fits both systems giving the same majority answer on late rows.
- Step A of §7 settles this with counts only, by standardizing late rows to the early gold mix.

---

## 3. Cause (c): label-prior shift

### 3.1 Gold-free facts (measured from preds; T = 1, 2-view readout)

| Task | C1 predicted mix | If gold is balanced (PREREG §7) | Mean predicted probability |
|---|---|---|---|
| route | backend 112 / frontend 68 | 90 / 90 | backend 0.578 |
| triage | feat 46, refactor 46, fix 34, test 22 | 37 each | test 0.165 |
| score | small 230, medium 92, tiny 34, large 4 | 90 each | large 0.081 |
| gate | **yes 36 / no 144** | 90 / 90 | **P(yes) 0.312**; median 0.236; 90th percentile 0.651 |

- **The yes/no prior flips sign across domains.**
  - In-domain, C1 leans "yes": REVIEW_methods S8 says C1-difficulty selection breaks yes/no balance for that reason.
  - On ejs-5 Gate it says "yes" 20% of the time. 4B-E does the same: 39/180 "yes", mean P(yes) 0.384.
  - This answers the open question in RESEARCH_small-model §6: **the ejs-5 Gate loss is one-directional (a no-bias).**
  - It also means the 50/50 yes/no rule in the spec does not protect against far-domain prior drift.
- **The gold-free estimators fail here, and that is expected.**
  - Saerens EM (Neural Computation 14(1):21-41, 2002) run on C1's ejs-5 probabilities collapses: Gate prior → 100% "no";
    Score → 91% "small".
  - BBSE (Lipton et al. 2018, https://arxiv.org/abs/1802.03916) needs label shift (p(x|y) fixed) and a source confusion
    matrix for the same task. Neither holds: ejs-5 is a new task form, not the same task with new priors.
  - Garg et al. 2020 (https://arxiv.org/abs/2003.07554) show that MLLS/EM is consistent only for a **calibrated**
    classifier with an invertible confusion matrix. C1 is 17.5 pp overconfident on Score (§4).
  - **Do not use EM or BBSE as a gold-free fix or a gold-free diagnosis on ejs-5.**
  - The valid test is the gold-based oracle in §7 (step C).
- **Gold-free flip counts are upper bounds on any change.** A flip can gain at most 1 item.

| Correction (C1, 2-view) | route | triage | score | gate |
|---|---|---|---|---|
| Batch calibration (divide by test-mean probability; Zhou et al., arXiv 2309.17249) | 1 | 6 | 66 | 26 |
| Force the known balanced prior (Sinkhorn) | 9 | 14 | 104 (192 with argmax) | 36 |
| Gate: cut at the median P(yes) (90/90) | - | - | - | 54 |
| Gap to Jev (items) | 0 | -7 | -18 | -13 |

  - These bounds cannot rule out prior shift on Score or Gate. They do rule it out for Route, which has no gap, and they cap
    Triage at about 6-14 items.

### 3.2 Gate: the ranking is weak, so a threshold fix recovers little (derived)

Method:
- The author's calibration bins (in `scores_c1_4be.json`) bin rows by confidence |P(yes) - 0.5| × 2.
- I split each bin into yes-predictions and no-predictions from the preds file. The bin counts match exactly, which checks
  the binning.
- Bins 0.7-0.8 contain only "no" predictions (29 rows, P(yes) 0.077-0.145), with accuracy 0.522 and 0.833. So 12 of the
  29 rows C1 is surest are "no" are gold "yes".

Assuming 90/90 gold (PREREG §7, "class-balanced by construction"), C1's Gate breaks down as follows:

| P(yes) group | Rows | Gold yes (derived) | Share |
|---|---|---|---|
| top (predicted yes, P ≥ 0.5) | 36 | 24 | 67% |
| middle (0.2 ≤ P < 0.5) | 78 | about 41 | about 53% |
| bottom (P < 0.2) | 66 | about 25 | about 38% |

- The confusion matrix is TP 24, FP 12, TN 78, FN 66. Accuracy = (54 + 2·TP)/180 = 56.7%, matching the reported figure.
- The coarse AUC is about **0.58**.
- The best step threshold, predicting "yes" on top + middle = 114 rows, gives TP 65 and TN 41, so **58.9%**. That is +4
  items. Under an equal-variance binormal ROC at AUC 0.6, the most it could reach is about 57%.
- Jev's 63.9% needs AUC ≥ about **0.69** under the same model.
- **Gate verdict: about 4-6 of the 13 missing items are prior or threshold. At least 7 are discrimination (skill).** The
  skill part persists on late rows (-12.1 pp, n 66).
- Route note: under 90/90, C1's backend recall is 88/90 and its frontend recall 66/90. A balanced-prior correction could
  add up to 9 Route items, but Route is not part of the gap.

### 3.3 Score: a natural experiment says the prior is a wash (measured)

- C1 and 4B-E predict very different Score label mixes:
  - C1: tiny 34, small 230, medium 92, large 4.
  - 4B-E: tiny 73, small 263, medium 24, large 0.
- They disagree on **127/360** rows, yet their accuracies are 116 vs 119 hits.
- On a class-balanced test, accuracy equals the mean per-class recall. When predictions carry little signal, moving the
  predicted mix trades recall between classes at nearly zero net.
- C1's Score accuracy sits close to chance everywhere except a small confident slice:

| C1 confidence bin | Rows | Accuracy |
|---|---|---|
| 0.2-0.5 | 297 | 25.6-31.8% |
| 0.6-0.7 | 61 | 55.7% |

- Chance is 25%, Jev gets 37.2% and Opus 45.8%.

---

## 4. Cause (d): the Score readout

Measured, gold-free except for the published bins.
- The rounded expected level (official; also the author's rule for Jev) differs from argmax on **78/360** rows for C1
  (81 with the 1-view read) and **120/360** for 4B-E.
- Argmax spreads predictions out: C1 tiny 97, small 154, medium 103, large 6.
- **Self-expected accuracy**, the mean probability of the chosen level:

| Readout | Self-expected accuracy |
|---|---|
| official | 49.7% |
| argmax | 52.3% |
| actual (official) | 32.2% |

  - Argmax could add at most +2.6 pp (≈ 9 items), and only if C1 were calibrated.
  - C1 is **17.5 pp overconfident** on Score, so the real gain is smaller.
- All 20 rows in bins 0.1-0.2 are readout-differs rows, and they score 30%. Agree-rows at confidence 0.5-0.6 (113) score
  27.4%. Neither is far from chance.
- **Estimate: the readout explains 0 to about 5 of Score's 18 missing items.** EXTRA_1 owns the readout research. The
  readout can only change through dev and sealed gates, because ejs-5 never chooses a setting (PREREG_ejs5 §2).

---

## 5. Cause (a): task type, skill and input form

- **Route has no gap.** Triage (-7) is mostly early rows (-6) and so mostly time-linked.
- **Score (-18)** is near chance for everyone, and its gap is entirely early rows (-26 early, +8 late). The best guess is
  time or label mix (§2.3), not skill. Even Opus only reaches 45.8%, so data can buy little here.
- **Gate (-13)** is the one deficit that holds across periods and across both adapters. It is mostly discrimination
  (§3.2), so this is the deficit data can fix.
- **Input-form mismatch, which the C spec should hear about now:**
  - ejs-5's model input is commit **prose only**, with paths and giveaway terms stripped (PREREG_ejs5 §7).
  - C_DATA_SPEC §4.2 commit rows show "the message and a diff truncated to ≤1,500 tokens", with the **numstat line shown**
    for Score, as REVIEW_methods S3 advised.
  - That trains reading diffs and counting churn, a different skill from inferring risk or size from prose.
  - For the sealed suite and real users this is fine, maybe better. For **ejs-5 transfer**, a share of commit rows must be
    **message-only** (diff hidden) with program labels.
  - This copies no ejs-5 item or wording. It matches only the input form, and the owner has ruled ejs-5 in-domain.
- **Slice discovery is not worth it here.**
  - Domino (arXiv 2203.14960) recovers **36% of 1,235** planted slices, with precision@10 = 0.639. It needs item
    embeddings, and we may not read item text.
  - Use the 4 metadata axes instead: task × period × gold label × C1 confidence tercile, about 60 cells.

---

## 6. Current best split of the 38-item gap (ranges; the causes overlap, so they do not add to 38)

| Cause | Items (range) | Share | Basis | Can C's data fix it? |
|---|---|---|---|---|
| Jev's early-row edge (time or exposure, Jev-specific) | 20-41 point; 95% interval about 0-all | 50-100% | §2.1 DiD vs 4 systems | **No** (it is n8n history; we never train on n8n) |
| ...of which could be Score label mix (untested) | 0-26 | ? | §2.3 | No (a readout or prior issue) |
| Prior/threshold on Gate and Triage | 4-12 | 10-30% | §3.1-3.2 | Partly: base-rate variation in data plus a readout fix |
| Score readout | 0-5 | 0-13% | §4 | No (readout, gated on dev) |
| Gate discrimination (skill) | ≥7 (late Gate -8) | ≥18% | §3.2, §1 | **Yes**: Gate-style prose risk judgement |

**Prediction registered before §7 runs:** the label-mix-standardized Score DiD stays ≥ +10 pp, and the pooled
standardized DiD stays ≥ +5 pp. Prior plus readout on the confirm half closes ≤ 10 items, and Gate keeps ≥ 7 items of
residual. If §7 contradicts any of these, §8 changes as the rules say.

---

## 7. Protocol to pin it down ($0, CPU, about 1 min; report-only; needs the owner's counts-only OK because it reads gold in quarantine)

Pre-register it as a PREREG_FINAL amendment, like A13, **before** running. The amendment must say:
- the result is report-only;
- it never chooses a model, readout or setting on ejs-5 (PREREG_ejs5 §2);
- it may shape C's commit mix, which is acceptable because ejs-5 is already "in-domain" for C (C_DATA_SPEC §4).

The amendment also fixes the script sha256, the split seed and the rules below.

**Split.** Halves are by commit: `select = int(sha256("decomp-v1|" + group_id), 16) % 2 == 0`; the rest is confirm. All of
a commit's rows go to one half. Fit only on select; report confirm.

**Steps.** The script prints aggregates only, never ids, text or per-row labels.
- **A. Label mix:** gold counts per task × period, and predicted counts per system (C1, 4B-E, Jev, GPT, Opus) per task ×
  period. This checks the 90/90 assumption and the late Score mix.
- **B. DiD with standardization:** accuracy per system × task × period.
  - DiD = (sys - Jev)_late - (sys - Jev)_early, using a commit-stratified paired bootstrap: early and late commits are
    resampled separately, B = 10,000, seed 0.
  - Report it crude and also **label-mix standardized**: late rows are weighted within each task so their gold mix equals
    the early mix, with the same weights for both systems.
  - Formal version, following Roberts et al.: a logistic `correct ~ system × late + task:gold_label` with commit-clustered
    SEs. The `system × late` odds ratio is the evidence.
- **C. Oracle prior correction:**
  - Per task, add a logit bias vector b (first class fixed at 0) to log p, then use the official readout.
  - Fit b on select:
    - k = 2: grid from -3 to 3 in steps of 0.05;
    - k = 4: coordinate ascent over the 3 biases, grid from -2 to 2 in steps of 0.1, 3 passes;
    - objective: hits.
  - Apply b on confirm. Report Δhits on confirm × 2 (scaled to the full set), plus in-sample Δhits on all rows as the
    optimistic ceiling.
  - Reference: logit adjustment z' = z - log π_s + log π_t is Bayes-optimal for a balanced target (Menon et al.,
    arXiv 2007.07314).
- **D. Oracle readout (Score):** argmax vs the official readout, Δhits on confirm × 2. Also report b plus argmax.
- **E. Gold-free references:** Batch Calibration Δhits and Gate median-cut Δhits on all rows. These are report-only and are
  never a candidate readout here.
- **F. Shares:** for G = 38:
  - T = 600 × standardized DiD (with CI);
  - P = C;
  - R = D;
  - residual = G - max(T, 0) - max(P + R, 0).
  - Report the sequential attribution in both orders: (P, R, T) and (T, P, R).

**Script sketch** (save as `bench/ejs5/decomp_ejs5.py`; it reuses the kit's loaders, so gold stays inside the process):

```python
import hashlib, json, math, itertools, numpy as np
from collections import Counter, defaultdict
import ejs5lib as E, score_ejs5 as S
rows = E.read_jsonl(E.ROWS); fns = E.author_functions(E.QUAR / "run_public_bench.py")
pub, _ = S.check_published(rows, E.QUAR, fns["summarize"], quiet=True)
runs = {n: {p["id"]: p for p in E.read_jsonl(E.RUNS / n / "preds.jsonl")} for n in ("c1_main500k", "e4b_pxE")}
half = lambda r: int(hashlib.sha256(f"decomp-v1|{r['group_id']}".encode()).hexdigest(), 16) % 2  # 0 select, 1 confirm
gold = lambda r: E.row_label(r); task = lambda r: r["meta"]["task"]; late = lambda r: bool(r["meta"]["late"])
def ours(n, r, bias=None, readout="official"):
    keys, ps = E.norm_probs(r, runs[n][r["id"]]["probs"])
    if bias is not None:
        z = [math.log(max(p, 1e-12)) + b for p, b in zip(ps, bias)]; m = max(z)
        ps = [math.exp(x - m) for x in z]; s = sum(ps); ps = [x / s for x in ps]
    if readout == "argmax" or r["meta"]["kind"] == "choice": return keys[max(range(len(ps)), key=ps.__getitem__)]
    if r["meta"]["kind"] == "noul": return "yes" if ps[0] >= .5 else "no"
    ev = sum(i * p for i, p in enumerate(ps)); return keys[max(0, min(3, int(round(ev))))]
def pubpred(m, r):
    rec = pub[m][task(r)].get(r["group_id"]); return rec.get("pred") if rec else None
SYS = {"c1": lambda r: ours("c1_main500k", r), "e4b": lambda r: ours("e4b_pxE", r),
       **{m: (lambda r, m=m: pubpred(m, r)) for m in ("jev", "gpt", "opus")}}
hit = {s: [int(f(r) == gold(r)) for r in rows] for s, f in SYS.items()}
out = {"A_gold_mix": Counter(f"{task(r)}|{'late' if late(r) else 'early'}|{gold(r)}" for r in rows),
       "A_pred_mix": {s: Counter(f"{task(r)}|{'late' if late(r) else 'early'}|{f(r)}" for r in rows) for s, f in SYS.items()}}
# B: crude + label-mix-standardized DiD vs Jev, commit-stratified bootstrap
def weights(idx_late, idx_early):
    w = {}
    for t in E.TASKS:
        e = Counter(gold(rows[i]) for i in idx_early if task(rows[i]) == t); l = Counter(gold(rows[i]) for i in idx_late if task(rows[i]) == t)
        ne, nl = sum(e.values()), sum(l.values())
        for i in idx_late:
            if task(rows[i]) == t: w[i] = (e[gold(rows[i])] / ne) / (l[gold(rows[i])] / nl) if l[gold(rows[i])] and ne else 0.0
    return w
def did(s, sel=lambda r: True, std=False, B=10000, seed=0):
    L = [i for i, r in enumerate(rows) if sel(r) and late(r)]; Ea = [i for i, r in enumerate(rows) if sel(r) and not late(r)]
    w = weights(L, Ea) if std else {i: 1.0 for i in L}
    def stat(Li, Ei):
        dl = sum(w[i] * (hit[s][i] - hit["jev"][i]) for i in Li) / max(1e-9, sum(w[i] for i in Li))
        de = sum(hit[s][i] - hit["jev"][i] for i in Ei) / len(Ei); return dl - de
    cl, ce = defaultdict(list), defaultdict(list)
    for i in L: cl[rows[i]["group_id"]].append(i)
    for i in Ea: ce[rows[i]["group_id"]].append(i)
    rng = np.random.default_rng(seed); kl, ke = list(cl), list(ce); draws = []
    for _ in range(B):
        Li = [i for k in rng.choice(kl, len(kl)) for i in cl[k]]; Ei = [i for k in rng.choice(ke, len(ke)) for i in ce[k]]
        draws.append(stat(Li, Ei))
    d = np.sort(draws); return {"did": stat(L, Ea), "ci95": [float(d[int(.025 * B)]), float(d[int(.975 * B) - 1])]}
out["B_did"] = {f"{s}|{t}|{'std' if std else 'crude'}": did(s, (lambda r, t=t: t == "all" or task(r) == t), std, B=2000)
                for s in ("c1", "e4b", "gpt", "opus") for t in ("all",) + E.TASKS for std in (False, True)}
# C/D: oracle prior bias + Score argmax, fit on select, report confirm (x2) and in-sample ceiling
def hits(n, R, bias=None, readout="official"): return sum(int(ours(n, r, bias, readout) == gold(r)) for r in R)
def fit_bias(n, R, k, readout="official"):
    grid = np.arange(-3, 3.001, .05) if k == 2 else np.arange(-2, 2.001, .1); b = [0.0] * k
    for _ in range(1 if k == 2 else 3):
        for j in range(1, k):
            b[j] = max(grid, key=lambda g: hits(n, R, b[:j] + [g] + b[j + 1:], readout))
    return b
res = {}
for n in ("c1_main500k", "e4b_pxE"):
    for t in E.TASKS:
        sel = [r for r in rows if task(r) == t and half(r) == 0]; con = [r for r in rows if task(r) == t and half(r) == 1]
        allr = sel + con; k = len(E.norm_probs(sel[0], runs[n][sel[0]["id"]]["probs"])[0]); base = hits(n, con)
        b = fit_bias(n, sel, k); res[f"{n}|{t}|prior_confirm_x2"] = 2 * (hits(n, con, b) - base)
        res[f"{n}|{t}|prior_insample_ceiling"] = hits(n, allr, fit_bias(n, allr, k)) - hits(n, allr)
        if t == "score":
            res[f"{n}|score|argmax_confirm_x2"] = 2 * (hits(n, con, None, "argmax") - base)
            ba = fit_bias(n, sel, k, "argmax"); res[f"{n}|score|prior+argmax_confirm_x2"] = 2 * (hits(n, con, ba, "argmax") - base)
out["CD_oracle"] = res
out["G_items_c1_minus_jev"] = sum(hit["c1"]) - sum(hit["jev"])
print(json.dumps(out, indent=1, default=dict))
```

Cost: the bias grid for k = 4 is about 3 × 3 × 41 × 180 reads per task per model, a few seconds. The bootstrap above
uses B = 2,000 to stay under 1 minute; use 10,000 for the final run if time allows. Stall guard: run each step separately
if any step exceeds 2 minutes.

**Rules** (fixed in the amendment before running; G = 38 items):
1. **Time-linked** if the standardized pooled DiD for C1 has CI lower bound > 0, **or** the standardized Score DiD has
   z ≥ 2.5 (Bonferroni over 4 tasks), with point T ≥ 19 items.
   - Power note: the pooled DiD SE is about 3.6 pp, so the pooled rule fires only if the true DiD is ≥ about 7 pp. The
     Score DiD (SE about 5.5 pp, point +17.6) is the test with power.
   - Then:
     - (i) the ejs-5 readout for C = late rows plus Gate, with the full set reported but not targeted;
     - (ii) cut commit-block Score from 25% to ≤ 10% and move the share to Gate and the message-only variant;
     - (iii) no extra spend on commit data to chase the full-set number.
2. **Readout/prior** if P + R ≥ 10 items on confirm × 2:
   - the fix goes through the readout research (EXTRA_1) and the dev and sealed gates, not through more rows;
   - also vary yes/no base rates per card, 20-80% (REVIEW_methods N7), so the model stops learning a fixed prior.
3. **Gate skill** if Gate's residual after its own prior correction stays ≥ 5 items **and** the late Gate gap is ≤ -5 pp.
   Then keep Gate at ≥ 30-35% of the commit block (REVIEW_methods S3) and add the message-only input variant (§5).
4. **None fires (all intervals include 0):**
   - treat the gap as unexplained noise plus time;
   - keep the plan;
   - set the expected ejs-5 gain to about +1 pp (REVIEW_methods S4);
   - ejs-5 must not drive C's mix.

---

## 8. What this means for C now (proposals for the spec and recipe owners; I did not edit either file)

1. **Expectation:** stop writing "breadth closes the ejs-5 gap".
   - On the current evidence, about 50-100% of the full-set gap is a Jev-specific early-row edge (point estimates, with a
     wide CI). Our data cannot buy that, because we never train on n8n.
   - Report ejs-5 as **late rows (headline for C) + full set + Gate**. Full-set ejs-5 success for C is a tie, not a win.
2. **Commit block, input form:** make **30-50% of commit rows message-only**, with the diff hidden and labels from
   program metadata, so they match ejs-5's input. Keep diff-shown rows for the rubric skills.
3. **Commit block, task shares:** raise Gate to 35%. Hold Score at ≤ 15% until §7 says whether Score's gap is time or
   label mix. Score is near chance even for Opus (45.8%), and the readout, not data, moves it most.
4. **Yes/no prior:**
   - Add **per-card base-rate variation (20-80%)** in Gate-like and other yes/no families.
   - Add a **gold-free yes-rate drift monitor** to the sealed suite and dev: mean P(yes) and the predicted yes-share per
     domain, logged for every candidate.
   - C1 goes from leaning "yes" in-domain to 20% "yes" on ejs-5, which is the drift the 50/50 rule cannot catch.
   - Alarm if any domain's predicted yes-share is outside 30-70% on a set that is 50/50 by construction.
5. **Do not ship any test-time prior fix** (Batch Calibration, EM, median cut) because of ejs-5.
   - EM collapses here, and BBSE's assumptions fail.
   - Batch Calibration needs a same-task batch at inference, which a single-call decision API lacks.
   - Domain-context calibration (Fei et al., arXiv 2305.19148; up to +37% macro-F1 on tasks with strong domain-label bias,
     no labels) is a candidate for **future readout research on dev and sealed only**.
6. **Gate is the honest target for the ejs-5 part of the $100.** The data should be prose-only risk judgements (hold or
   ship) over real commit and change text with program labels and varied base rates. Size the claim from the late-row
   Gate gap: -12.1 pp on n = 66, with a CI of about ±13 pp. One round may show nothing; say so in advance.

---

## 9. Unknowns

- The true gold mix by period, and whether Gate is exactly 90/90. Step A settles both. All derived Gate numbers (§3.2)
  assume 90/90.
- The cutoffs of Jev 1.13, GPT-5.6 Terra and Opus 5, and the exact pretraining cutoff of Qwen3.5-4B. Only the release
  date (2 Mar 2026) is known.
- Whether Jev's published answers carry probabilities. A Jev-side prior or readout analysis needs them, and step A shows
  only Jev's predicted mix.
- The commit date range of the early rows. If many fall after Qwen3.5's cutoff, C1's own exposure is lower than assumed.
- LiveCodeBench's per-window pass@1 values come from figures, not text. I cite the direction only.

## Sources

- LiveCodeBench, Jain et al. 2024: https://arxiv.org/abs/2403.07974
- Roberts et al., "To the Cutoff... and Beyond?" ICLR 2024: https://arxiv.org/abs/2310.10628 (odds ratios from §5, Table 1)
- Golchin & Surdeanu, "Time Travel in LLMs": https://arxiv.org/abs/2308.08493
- "The SWE-Bench Illusion": https://arxiv.org/abs/2506.12286
- Carlini et al., "Quantifying Memorization Across Neural Language Models": https://arxiv.org/abs/2202.07646
- Duan et al., "Do Membership Inference Attacks Work on LLMs?": https://arxiv.org/abs/2402.07841
- Das et al., "Blind Baselines Beat Membership Inference Attacks for Foundation Models": https://arxiv.org/abs/2406.16201
- Lipton et al., BBSE: https://arxiv.org/abs/1802.03916
- Garg et al., "A Unified View of Label Shift Estimation": https://arxiv.org/abs/2003.07554
- Saerens, Latinne & Decaestecker, Neural Computation 14(1):21-41, 2002 (EM prior adjustment)
- Zhou et al., Batch Calibration: https://arxiv.org/abs/2309.17249
- Fei et al., "Mitigating Label Biases for In-context Learning": https://arxiv.org/abs/2305.19148
- Menon et al., logit adjustment: https://arxiv.org/abs/2007.07314
- Eyuboglu et al., Domino: https://arxiv.org/abs/2203.14960
- Qwen3.5-4B release date: https://llm-stats.com/models/qwen3.5-4b
- Local: `bench/ejs5/runs/scores_c1_4be.json`, `bench/ejs5/runs/{c1_main500k,e4b_pxE}/preds.jsonl`,
  `bench/ejs5/PREREG_ejs5.md` §5/§7, `c_spec/REVIEW_methods.md` S3/S4/S8/N7, `c_spec/C_DATA_SPEC.md` §4.2. The gold-free
  diagnostics script is `goldfree_decomp.py` in this session's scratchpad (not in the repo).
