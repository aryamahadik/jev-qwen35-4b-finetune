# Why narrow fine-tuning made C2 overconfident, and the cheapest fixes that keep accuracy (research v5, 18 Oct 2026)

Scope: C2 (LoRA r16, 59,340 rows, 23,736 new + 35,604 replay) kept dev accuracy flat (-0.48 pp pooled) but its sealed-look yes/no ECE went 4.1% (C1) to 13.2% (C2), Brier +0.0098 (`c2_build/train/L1_RESULT.json`, keys `report_only.ece_yesno_G+R+X`, `verdict.S4`). This file answers: why, what is proven to fix it without hurting accuracy, in what order, and what exact settings to write down before C2.1 data freeze.

Rules kept: I opened no path containing ohs, sealed, quarantine, longbench, jevbench, ejs, c_spec/sealed_brief, c_build/preread, no Jev output file, nothing under ~/.claude. I did not recompute or open any sealed read; the sealed numbers above are quoted from the task statement and from two keys of `L1_RESULT.json` (ECE, Brier). Everything marked OURS-DEV was computed by me on non-sealed dev reads that C2's pre-gate already used. Only file written outside the scratchpad: this file and `calibration_dev_scripts/` next to it.

Tags: OURS-DEV = my computation on C2 dev reads (scripts in `calibration_dev_scripts/`, reproducible, accuracy reproduces the C2 report exactly: C1 69.17 / C2 64.33 on the 600 transfer rows; T19 63.0 / 51.67; T21 75.33 / 77.0). AUTH = paper authors ran it. IND = independent third party. DERIVED = my arithmetic or judgement, not a measurement on our model. UNVERIFIED = not confirmed in a primary source I could read, or a mechanism that is a hypothesis for our model.

---

## 0. Bottom line (read this first)

1. **C2's calibration damage is mostly a distribution-shift effect, and a large part of the sealed gap is probably a temperature-fit artifact, not only "training made it overconfident".** On dev, the C2 minus C1 yes/no ECE gap is +0.25 pt on the general pool but +4.8 pt on the transfer rows at T=1, and +12.2 pt at the frozen L1 temperatures (C1 flattened with T 1.3, C2 sharpened with T 0.8). The sealed gap was +9.1 pt. (OURS-DEV, section 2.3; the sealed link is DERIVED/UNVERIFIED.)
2. **The L1 temperature rule picked the wrong direction for C2.** `L1_T_FROZEN.json`: C2 T = 0.8 (yes/no) and 0.95 (choice) from a median-over-138-small-groups NLL on trained-family mixdev. The pooled optimum on the same 2,795 rows is 1.10 / 1.05 (OURS-DEV), 1.15 on the general pool, 1.75 on the transfer rows, 3.25 on T19. In the one PLM study that fits both (Desai and Durrett) the OOD value is about 2x the ID value (ID 0.99-1.39, OOD 1.25-3.61); the opposite error also exists (Rafe and Das: a T fitted on few-option tasks over-flattened 150-option tasks), so the direction is task dependent but an in-distribution T does not transfer. A temperature below 1 should not ship for a model that will meet unseen types unless a held-out-family check supports it.
3. **Scalar temperature cannot finish the job.** Fitting T on the other held-out domains (leave-one-domain-out) cuts C2's mean-domain ECE from 10.64 to 8.09 (-2.55 pt, 11 domains) but C1 sits at 6.2, and T19 stays at 28 because T19 needs T near 3. Ranking also degraded and T does not change ranking: AURC general 6.21 to 6.90, transfer 15.94 to 19.09, T19 28.21 to 36.93 (OURS-DEV).
4. **Mean confidence rose about +3.3 pp (CI +3.2 to +3.6) on the general pool while accuracy moved -0.5 pp.** That "confidence grows, accuracy does not" signature is what the literature ties to continued NLL fitting after accuracy saturates (Guo 2017; Chen et al. ACL 2023; Zhu et al. 2023; CogCalib 2025).
5. **The C2.1 plan has a concrete risk the C2 report does not:** `C2_1_PLAN_v3.md:919` says "Epochs: 2 over the mix", while C2 ran one pass (0.9901 epochs, `C2_REPORT.md:44`). The plan's own cost line ($26-28 for 112.5K rows) matches ONE pass at C2's measured $0.221 per 1K row-passes ($13.14 / 59,340), not two (about $50). The plan does say "unless the cost cap binds; then fewer", and at C2's measured rate two passes (about $50) will bind the $30 cap, so the plan's own rule lands near 1.0-1.2 epochs; pre-register 1.0 now instead of letting it fall out of a late cost check, because extra passes over narrow program rows are the most direct way to repeat the C2 confidence growth (M1).
6. **Ranking of fixes (evidence x cost), details in section 4:** (1) temperature protocol on a held-out-family pool, floor T >= 1, $0; (2) one pass plus calibration-based snapshot selection, $0-2; (3) abstain-share caps and a predicted/gold abstain-ratio gate, $0; (4) post-hoc calibration-replay buffer and conformal ASK band, $0; (5) blending toward the parent (partial only); (6) label smoothing (mixed evidence, hurts ranking in the one study that tests it, all-or-nothing in a single run, pilot only); (7) focal loss (no decoder-LLM evidence, pilot only); (8) replay-ratio changes (no evidence for calibration); (9) soups/last-K averaging (no calibration benefit measured, here or in the literature).
7. **Honest expectation (DERIVED):** item 1 alone is measured at -1.4 to -2.5 pt of mean-domain ECE on dev; items 2-4 are unmeasured, so the realistic range for 1-4 together is about 1.5-4 pt on shifted looks. They do not by themselves put C2.1 at or below C1, and they do not touch the "confidently wrong on an unseen family" failure (T19: 76 of 98 verdicts answered "Cannot be determined" with 84.4% mean confidence and 34.2% precision). That needs data balance (section 4, item 3) and held-out families in selection.

---

## 1. What I read and ran

Project files read (non-forbidden paths only): `c2_build/C2_REPORT.md` (whole), `c2_build/C2_RESULTS.json` (calibration keys), `c2_build/train/L1_T_FROZEN.json` (whole), `c2_build/train/L1_RESULT.json` (only `report_only.ece_yesno_G+R+X` and `verdict.S4`), `zed_orch/c21/C2_1_PLAN_v3.md` (lines 904-1100, 1265-1305 and grep), `research_v3/recipe.md`, `research_v4_levers/calibration.md`, `C2_1_EXTRA_LEVERS.md` (grep), the per-row dev reads `lean/preds_c2_transfer_dev/`, `preds_c2_mixdev/`, `preds_{dev,dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card}/` with gold from `lean/data/*.jsonl`. C1 = `q35_4b_main500k_c2.jsonl`, C2 = `q35_4b_c2.jsonl` (the official copy of final_a10, A97); alpha/last-K/early-late grid = `q35_4b_c2grid_*.jsonl`. A sibling agent's `c2_dev_diagnostics.md` (same folder) independently reports the same fitted temperatures (C2 1.10 / 1.05, C1 1.55 / 1.35, lines 37 and 342) and T19 ECE 14.2 to 31.4, so the numbers here are cross-checked on two code paths.

Papers: I downloaded the PDFs from arxiv.org into the scratchpad and read the cited passages with pdftotext (Guo, Muller, Desai and Durrett, Ovadia, Mukhoti, Huang et al., Xiao et al., Zhu et al. x2, Chen et al., Wortsman x2, Laplace-LoRA, LoRA ensembles, CogCalib, Rafe and Das, Gekhman, Bianchi, Tomani, Yu et al., SWAG, Shihab et al., Dong et al.). Items I could only see in abstracts or search summaries are marked.

Metric definitions used (stated because the sealed number is a different metric): **top-label ECE** = 10 equal-mass bins on max-probability (the protocol of Rafe and Das, arXiv 2610.00346, used in plan v3.2 section 3); **yes/no ECE** = 10 equal-width bins on P(yes). The sealed 4.1% / 13.2% is a yes/no ECE over parts G+R+X; the dev "report-only" 2.96 / 2.61 in `C2_REPORT.md:102` is the same family of metric. Cluster bootstrap = resample `group_id` clusters, 400 draws (not 10,000), so CIs are indicative.

---

## 2. What happened to C2's calibration (OURS-DEV)

### 2.1 C1 vs C2 by set (T = 1, top-label ECE, 10 equal-mass bins)

| Set | n | acc C1 / C2 | mean conf C1 / C2 | conf - acc C1 / C2 | ECE C1 / C2 | T_opt (in-sample) C1 / C2 | ECE at T_opt C1 / C2 | AURC C1 / C2 |
|---|---|---|---|---|---|---|---|---|
| General dev pooled (9 splits) | 8,143 | 81.46 / 80.98 | 82.24 / 85.56 | +0.78 / +4.59 | **2.78 / 5.46** | 1.00 / 1.15 | 2.78 / 4.47 | 6.21 / 6.90 |
| Transfer dev (T19 + T21) | 600 | 69.17 / 64.33 | 82.16 / 85.09 | +13.0 / +20.8 | **13.34 / 21.20** | 1.45 / 1.75 | 6.91 / 11.38 | 15.94 / 19.09 |
| T19 (compliance) | 300 | 63.00 / 51.67 | 77.16 / 83.02 | +14.2 / +31.4 | 14.16 / 31.36 | 1.85 / 3.25 | 8.78 / 10.16 | 28.21 / 36.93 |
| T21 | 300 | 75.33 / 77.00 | 87.17 / 87.16 | +11.8 / +10.2 | 13.05 / 12.82 | 1.30 / 1.20 | 9.23 / 11.55 | n/a |
| c2_mixdev, all 3,386 rows | 3,386 | 68.81 / 78.62 | 78.05 / 83.42 | +9.2 / +4.8 | 9.23 / 6.27 | 1.40 / 1.15 | 5.28 / 5.24 | n/a |

Paired cluster bootstrap, C2 minus C1: general ECE **+2.68 [+1.87, +3.16]**, mean confidence **+3.3 [+3.2, +3.6]** pp, accuracy -0.48 [-1.04, +0.10] pp; transfer ECE **+7.86 [+3.75, +11.55]**, accuracy -4.8 [-8.6, -1.2], confidence +2.9 [+1.8, +4.1]. Where C2 gained accuracy (trained-family mixdev, 68.8 to 78.6) its ECE fell (9.23 to 6.27): the damage is out of distribution, not in it. General-pool ECE by split (C1 to C2): dev 4.05 to 3.92, dev_claims 4.83 to 4.92, dev_negwords 3.95 to 4.58, devp_card 2.71 to 4.58, pg_dev 2.46 to 4.70, taskbank 6.83 to 8.96, hard_dev 7.08 to 8.16, **dev_nc 2.59 to 8.94, devzs 6.68 to 11.92**. The two biggest jumps are the zero-shot and no-card sets, the splits least like the training rows.

**Decomposition (DERIVED from the table).** conf - acc grew by +3.8 pt on the general pool (+3.3 from higher confidence, +0.5 from lower accuracy) and by +7.8 pt on transfer (+2.9 confidence, +4.8 accuracy loss). So on transfer the dominant term is accuracy lost at unchanged confidence ("confidently wrong"); on general the dominant term is a uniform confidence uplift of about +3 pp.

### 2.2 The temperature that shipped was sharper than the data supports

`L1_T_FROZEN.json`: rule = one T per model and question type, M(T) = median over groups (sampler + pack + register, 138 groups for yes/no, 130 for choice) of NLL, T = clip(argmin, 0.8, 1.3), fitted on the 2,795 trained-family mixdev rows only.

| | yes/no | choice | note |
|---|---|---|---|
| C1 frozen T | 1.30 | 1.25 | C1 flattened |
| **C2 frozen T** | **0.80** | **0.95** | C2 sharpened (T_raw 0.8 / 0.95; pack-only fit gives T_raw 0.4 / 0.6) |
| C2 family-level fit (report-only in the file) | 1.05 | 1.05 | same rows, 14 / 13 groups |
| C2 pooled-NLL optimum, same 2,795 rows (OURS-DEV) | 1.10 | 1.05 | |
| C2 pooled optimum, general dev pool | 1.15 (single T) | | |
| C2 optimum on transfer / T19 | 1.75 / 3.25 | | |

The median-over-many-small-groups aggregator is dominated by easy, near-perfect groups where sharpening lowers NLL; the pooled NLL is dominated by the confident errors that matter for calibration. That is a protocol defect, visible as a 0.8 versus 1.10 split on identical rows. Effect on dev (C2 top-label ECE): general 5.46 at T=1 to 6.98 at frozen T; transfer 21.20 to 23.22.

**Leave-one-domain-out test of the fitting protocol (OURS-DEV; 11 domains = 9 general splits + T19 + T21; mean of per-domain ECE; the weighted-by-n mean is in brackets).**

| T used on each held-out domain | C2 | C1 |
|---|---|---|
| T = 1 (no scaling) | 9.53 [7.64] | 6.22 [4.83] |
| L1-style frozen T (0.8 / 0.95 for C2, 1.3 / 1.25 for C1) | 10.64 [8.83] | 7.02 [6.52] |
| T fitted on trained-family mixdev (pooled NLL: C2 1.10 / 1.05, C1 1.55 / 1.35) | 8.84 [7.06] | 8.67 [8.48] |
| **T fitted on the other held-out domains (leave-one-domain-out, pooled NLL)** | **8.09 [6.59]** | **6.20 [4.99]** |
| Per-domain oracle (in-sample, optimistic) | 6.47 [5.72] | 5.08 [4.16] |

Domain-balanced variant (each domain equal weight, 12 domains incl. mixdev): C2 9.18 at T=1 to 8.27 with leave-one-domain-out T (T values 1.1-1.3 everywhere); C1 6.53 to 6.60 (no change). So: a trained-family-only T is the worst choice for the model that is NOT in-distribution there (C1 +2.5 pt worse than T=1), and a held-out-pool T is the best non-oracle choice. It buys about -1.4 to -2.5 pt for C2 and leaves C2 about 1.9 pt above C1 (8.09 vs 6.20); T19 stays at 27.9-28.5 because no other domain asks for T near 3.

### 2.3 Why the sealed gap was probably larger than the dev general gap (yes/no ECE, P(yes), 10 equal-width bins)

| | n | C1 / C2 at T=1 | gap | C1 / C2 at frozen T | gap |
|---|---|---|---|---|---|
| General dev, yes/no rows | 4,329 | 2.86 / 3.11 | +0.25 | 4.96 / 6.11 | +1.15 |
| Transfer dev, yes/no rows | 282 | 12.99 / 17.80 | **+4.81** | 9.57 / 21.79 | **+12.22** |
| Trained-family mixdev, yes/no rows | 1,579 | 10.95 / 5.93 | -5.0 | 7.40 / 7.39 | 0.0 |
| Sealed look (G+R+X, `L1_RESULT.json`) | | 4.1 / 13.2 (as shipped) | +9.1 | | |

Two readings. (a) The dev "report-only" yes/no ECE (2.61 vs 2.96, +0.35 pt) had no power to see the problem; only the transfer rows did. (b) On the transfer rows the T asymmetry (C1 flattened, C2 sharpened) turns a +4.8 pt gap into +12.2 pt, which is the same size as the sealed +9.1. DERIVED, UNVERIFIED on sealed: a large part of the sealed 13.2% may be removed by T = 1 or a held-out-pool T. The owner/Opus could settle it for free by re-scoring the already-taken L1 reads under T=1 and under the section 5 protocol as a **report-only, labelled post-hoc** table (CPU, no new read, no bar or verdict changed). I did not do this (sealed rule).

### 2.4 The abstain failure on T19 (OURS-DEV; reproduces the report's 76 vs 26 vs 54)

Verdict rows n = 98, gold "Cannot be determined from the records" (CBD) = 26. C1 predicts CBD on 54 (precision 23/54 = 42.6%, mean confidence 75.3%); **C2 on 76 (precision 26/76 = 34.2%, mean confidence 84.4%)**. Predicted-to-gold CBD ratio: C1 2.08, C2 2.92. This is a class-prior drift plus overconfidence, not just a scale problem, and no temperature touches it (T19 ECE 31.4 to 29.8 under the best trained-family T, sibling file line 37).

### 2.5 Blending, last-K averaging, early+late averaging (OURS-DEV, 18 grid candidates, selected rows)

| Candidate | general mean conf | general ECE T=1 | general ECE at T_opt | general AURC | transfer acc | transfer ECE T=1 | transfer ECE at T_opt | transfer AURC |
|---|---|---|---|---|---|---|---|---|
| C1 | 82.24 | 2.78 | 2.78 | 6.21 | 69.17 | 13.34 | 6.91 | 15.94 |
| final_a05 | 84.31 | 4.33 | 3.68 | 6.44 | 67.83 | 16.37 | 9.41 | 16.85 |
| final_a07 | 84.88 | 4.97 | 4.27 | 6.59 | 66.17 | 18.47 | 9.75 | 17.71 |
| final_a10 (C2) | 85.56 | 5.46 | 4.47 | 6.90 | 64.33 | 21.20 | 11.38 | 19.09 |
| last3_a10 | 85.48 | 5.28 | 4.47 | 6.90 | 64.67 | 20.28 | 10.70 | 19.46 |
| earlylate_a10 | 85.51 | 5.91 | 5.36 | 7.08 | 64.33 | 19.49 | 9.23 | 20.26 |

Calibration, ranking (AURC) and transfer all degrade nearly linearly with alpha, as the C2 report found for accuracy (`C2_REPORT.md:143`). Alpha 0.5 removes about 40% of the extra general ECE at T=1 (5.46 to 4.33) and 0.8 pt at the oracle T (4.47 to 3.68), but stays above C1 (2.78). Last-K and early+late averaging do nothing for calibration (+-0.2 pt, or worse for early+late). Blending is a partial rollback, not a calibration fix.

### 2.6 An output-level "label smoothing" analogue (OURS-DEV, DERIVED weakly)

Mixing the output with the uniform distribution, p' = (1-e) p + e/K, is not the same as training with label smoothing (training changes the representation) but bounds what a "cap the top probability" effect can do. C2 transfer ECE: 21.20 (e=0) to 20.46 (0.02), 18.80 (0.05), 18.08 (0.10); general 5.46 to 5.24 / 5.29 / 5.25. C1 general gets WORSE (2.78 to 4.14 at e=0.10). The miscalibration sits at 80-95% confidence on wrong answers, not at the 99% extreme that smoothing caps; the oracle temperature reaches 11.4 on the same rows. This is why label smoothing ranks below temperature protocol here.

---

## 3. Why narrow fine-tuning inflates confidence (mechanisms, with evidence)

| # | Mechanism | Evidence (quantified) | Tag | Fit to C2 |
|---|---|---|---|---|
| M1 | NLL keeps rewarding confidence after accuracy saturates | Guo et al. 2017 (arXiv 1706.04599): "NLL can be further minimized by increasing the confidence of predictions"; on CIFAR-100 test error fell 29% to 27% in the region where NLL overfit. Chen et al. (arXiv 2211.00151, ACL 2023): in the over-fitted state "PLMs' confidence continues to increase steadily with little change in performance"; more tunable parameters or training longer raise confidence on wrong predictions too. Zhu et al. (arXiv 2311.13240, EMNLP Findings 2023): ECE "rapidly becomes worse in later epochs"; LoRA degrades far less than full FT (often 0.001 per epoch). | AUTH | Fits: +3.3 pp confidence at flat accuracy. Single pass limits M1 for rows seen once, but program-generated families repeat the same rule with new surface text, so the rule is seen thousands of times (hypothesis, UNVERIFIED). |
| M2 | Data the model already knows drives confidence growth | CogCalib (arXiv 2505.20903): "the model quickly assimilates known data, leading to continued confidence growth even after accuracy plateaus" (accuracy plateau at about 200 steps, Llama3-8B OBQA); even a 4:1 unknown:known ratio worsens calibration; but simply deleting known data "fails to consistently improve calibration". Gekhman et al. (arXiv 2405.05904): unknown examples are fitted slower; best dev performance at the point where most known and few unknown are fitted. | AUTH | 60% of C2 was replay C1 already knew (C1 92.15% on the old slice). Replay with KD 0.5 anchors the replay region but does not stop uplift elsewhere. Mixed evidence: not a clean lever. |
| M3 | Fine-tuned LLMs get worse under shift; ECE roughly doubles to triples | Laplace-LoRA (arXiv 2308.13111, ICLR 2024), LLaMA2-7B LoRA on OBQA, MAP ECE: ID 16.1; smaller shift 22.2 / 15.8; larger shift 34.2 / 38.4 / 35.2 / 34.2. Desai and Durrett (arXiv 2003.07892): RoBERTa out-of-box ECE ID 1.76-2.33, OOD HellaSWAG 11.93. Guard models (arXiv 2609.36477, Sep 2026): ECE ".004 to .196" clean to adversarial (WildGuard), as recorded in `research_v3/recipe.md:30`. | AUTH | Fits exactly: C2 general 5.5, transfer 21.2, T19 31.4, sealed 13.2. |
| M4 | Temperature fitted in distribution does not transfer | Ovadia et al. (arXiv 1906.02530): "temperature scaling achieves low ECE for low values of shift, the ECE increases significantly as the shift increases". Desai and Durrett Table 4: learned T ID 0.99-1.39; OOD 1.25-3.61 (about 1.9-2.2x). SWAG (arXiv 1902.02476): TS "not effective when the test data distribution differs from train". Tomani et al. (arXiv 2012.10988, CVPR 2021): "existing post-hoc calibration methods yield highly overconfident predictions under domain shift". Yu et al. (arXiv 2206.02757, NeurIPS 2022) RxRx1 OOD per-domain ECE: MSP 26.22, TS 13.78, domain-aware TS 5.25. Rafe and Das (arXiv 2610.00346, IND): Kev-9B stored T 2.30 took CLINC-150 ECE from 0.051 (T=1) to 0.377 as shipped. | AUTH + IND | **The cleanest explanation of the T = 0.8 error** (section 2.2). |
| M5 | Fine-tuned small decision models need T above 1 | Rafe and Das Table 7 (IND, Qwen3.5-based fine-tuned decision models; Kev adds LoRA r16 plus a pointer head): stored T 1.30-2.35; pooled unseen-task ECE as shipped 0.125-0.331, after one T fitted on a disjoint slice 0.026-0.038; hosted Jev 0.251 to 0.038. | IND | Supports the floor T >= 1 for CE-trained models. |
| M6 | Uncertainty reliability degrades before accuracy under sequential fine-tuning | Shihab et al. (arXiv 2604.23987, Apr 2026): conformal coverage loss about 3.4x accuracy loss (+-0.5x); worst case coverage 0.92 to 0.61 at accuracy within 3 pts; a task-specific buffer of m = 200 refit after each update restores coverage within 2 pts. | AUTH | Matches: ranking (AURC) and coverage degrade more than accuracy. |
| M7 | Small hidden size with huge vocabulary leaves LLMs unable to concentrate smoothing | Huang et al. (arXiv 2508.00264, ICML 2025) Remark 4.3: label smoothing "cannot help" such models (D small, vocabulary large); Qwen3.5-4B hidden 2560, vocab 248,320 (`research_v3/recipe.md:32`). Counter-evidence in the same paper: Gemma2-2B (same regime) went .341 to .020. | AUTH | Unresolved; and our readout is a restricted option softmax, a different regime (UNVERIFIED either way). |
| M8 | Synthetic data per se | I found NO study showing synthetic (LLM- or program-written) data causes overconfidence. Zhang and Pavlick (arXiv 2502.07164) found synthetic NLI data did NOT reinforce a shortcut (a search summary said the opposite; the abstract says "does not reinforce blindspots in the way we expected"). Zhu et al. 2023 presume dataset diversity matters (OA beat Alpaca) but do not test it. | AUTH, weak | Do not claim a synthetic-data cause. Narrowness and shift, not authorship, are what the evidence supports. |

---

## 4. Ranked fixes (evidence strength x cost)

Evidence grade: **A** = our own dev measurement plus at least two independent or author-run LLM/PLM studies that agree; **B** = one LLM/PLM study or our measurement alone; **C** = non-text (vision/tabular) studies only or mixed; **D** = no direct evidence or contradicted. "Single run" matters: C2.1 has ONE Modal run; a training-side lever cannot be an arm of the 18-point grid (those are weight merges of one run), so it is all-or-nothing unless a pilot is funded.

| Rank | Lever | Grade | Cost | Published effect | Expected effect for us (DERIVED unless OURS-DEV) | Risk to accuracy | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | **Temperature protocol**: per question type, fitted on a held-out-family pool, pooled/domain-balanced NLL, floor T >= 1.0, never a trained-family-only fit | **A** | $0, CPU | OOD optimum T about 2x ID (Desai); TS on i.i.d. validation fails under shift (Ovadia, SWAG, Tomani); domain-aware TS RxRx1 13.78 to 5.25 (Yu) | OURS-DEV: mean-domain ECE 10.64 (frozen) to 8.09 (-2.55); vs T=1 -1.4; remaining gap to C1 +1.9 | none (argmax unchanged) | **ADOPT, first** |
| 2 | **One pass, 12 snapshots, select on held-out-family NLL/ECE** (early stopping on calibration) | **A** (direction), B (size) | $0 plus L4 reads; possibly saves about half of stage-A money | Guo 2017 (NLL overfits while accuracy still improves); Chen 2023; Zhu 2023; Gekhman (early-stop 43.0 vs convergence 38.8 accuracy); Granite Guardian picked min validation CE (`research_v3/recipe.md:21`); sibling cites "best OOD is early in training" (arXiv 2509.12235, UNVERIFIED by me) | Unknown size; removes the second pass that the plan currently has. Cost arithmetic: $0.221 per 1K row-passes x 112.5K = $24.9 per pass (OURS from `C2_REPORT.md:15,44`) | an early snapshot may lose a little trained-family accuracy; selection rule below protects it | **ADOPT** |
| 3 | **Abstain/"cannot determine" balance**: cap abstain-gold share, pair every unresolvable item with a resolvable twin, gate the predicted/gold abstain ratio per held-out verdict family | B | $0 (data rule plus monitor) | Bianchi et al. (arXiv 2309.07875, ICLR 2024; LLaMA 7B/13B LoRA 4 epochs on 20K Alpaca): 500-1,000 safety rows (2.5-5%) cut harm; 2,000 rows (9%) gave over 50% exaggerated refusals on XSTest. Gekhman: relabelling unknown examples to "I don't know" raised accuracy on answered questions. Qwen3Guard (`research_v3/recipe.md:20`): doubling Safe share made the model more permissive (vendor, class mix is an operating-point lever). | Targets the T19 failure (ratio 2.92 vs C1 2.08); no temperature can | small if twins are program-built | **ADOPT** |
| 4 | **Calibration replay buffer + conformal ASK band** (A29): hold out m = 200 rows per type, refit T and the conformal threshold on the final served weights | B | $0, CPU | Shihab et al.: coverage restored to within 2 pts at m = 200 (<1% of replay memory); ConformalGuard (`research_v4_levers/calibration.md` C5) | Gives a stated guarantee and a principled ASK trigger; does not improve ranking | none | **ADOPT** (already A29) |
| 5 | **Blend toward the parent** (alpha grid) with calibration-aware eligibility, not just S | B (OURS-DEV only; no LLM paper reports ECE vs interpolation) | $0, in the grid | none found for language models (WiSE-FT papers report accuracy) | OURS-DEV: alpha 0.5 general ECE 5.46 to 4.33 (T=1), 4.47 to 3.68 (T_opt); costs -2.8 pp of the trained gain (+12.31 to +9.55); never reaches C1 | trades gain for calibration | keep in grid; use the eligibility filter |
| 6 | **Label smoothing** e = 0.05, on the restricted option softmax, new-family rows only (not KD rows) | **C** (mixed) | $0 extra compute in the final run, but a pilot costs about $2.2 per arm (10K rows x $0.221/1K) | Huang 2025 Table 1 (e = 0.1, MMLU after SFT): Gemma2-2B .343 to .125 / .341 to .020 / .353 to .016; LLaMA3-8B .113 to .073 / .050 to .012 / .038 to .016; Mistral-7B .096 to .028; accuracy -0.8 to +1.1 pt. Muller 2019: ImageNet ECE .071 to .035 (TS .022), CIFAR-100 .150 to .024 at e = .05. Desai and Durrett: OOD HellaSWAG ECE 11.93 to 2.14 (they report "5.8x") BUT in-domain MLE+TS (0.76-0.88) beats LS (8.7-11.4) and "temperature scaling hurts LS in many cases". Xiao 2022: LS and Brier lower OOD ECE. **Against:** Zhu et al. ECCV 2022 (arXiv 2303.02970): LS raised AURC 9.94 to 24.50 and cut AUROC 90.76 to 81.89 (CIFAR-10 ResNet-110); Muller: LS erases logit information (hurts distillation). | OURS-DEV analogue (2.6): a cap-type effect gives -3.1 pt on transfer and -0.2 pt on general; ranking is the product's ASK band, so an AURC loss costs more than it buys | accuracy -0.8 to +1.1 pt (Huang Table 1, MMLU) | **NOT in the default run.** Pilot only (rule in section 5, PR-6) |
| 7 | **Focal loss** (FLSD-53: gamma 5 for p < 0.2, 3 otherwise) | C/D | pilot about $2.2 per arm | Mukhoti 2020 (arXiv 2002.09437): CIFAR-100 ResNet-50 ECE 17.52 (CE) to 5.13 (FL-3) / 4.5 (FLSD-53), error 23.3 to 22.75 / 23.22; text is mixed: SST Tree-LSTM CE 7.37, FL-3 16.05, FLSD-53 9.19; 20 Newsgroups CE 17.92, FL-3 8.67, FLSD 6.92, LS-0.05 4.79. Zhu 2022: focal leaves AURC about unchanged (9.94 to 10.70). Xiao 2022 (BERT-base, same gamma schedule): "Focal Loss is the most compelling" but figure-only. | No decoder-LLM, no option-readout evidence. With 60% easy replay rows and 2-6 options, gamma 3 weights a row with p = 0.9 by 0.001: it silently drops the easy rows | unknown | **SKIP** (pilot only if the owner wants a second arm) |
| 8 | **Change the replay/mix ratio for calibration** | **D** | $0 | I found no study that varies the replay ratio and reports ECE (UNVERIFIED absence: my searches only). Dong et al. (arXiv 2310.05492): data amount matters more than composition ratio for ability; CogCalib: removing known data does not consistently help; Shihab: sequential FT harms coverage even with standard CL methods. | Keep C2's replay design (KD 0.5 on replay, 38K rows at C2 init); do not expect calibration from the ratio | n/a | **NO CHANGE** |
| 9 | **Model soups / checkpoint averaging as a calibration lever** | D for calibration; B for accuracy | $0 | Wortsman et al. (arXiv 2203.05482) Fig. B.2: "model soups improve accuracy, but unlike model ensembling, model soups do not improve calibration" (CLIP ViT-B/32, 20 seeds). Counter-signal: SWA in CNNs improved failure prediction and ECE (Zhu 2022 Table 2: CIFAR-10 ResNet-110 AURC 9.94 to 6.38, ECE 4.14 to 1.33), but that is high-LR trajectory averaging, not end-of-cosine averaging. LoRA ensembles (arXiv 2310.00035) help calibration but need M = 5 trainings. | OURS-DEV: last-3 average changes ECE by -0.2 and AURC by 0.0; early+late +0.45 worse | none | Keep A22/A23 for accuracy only; do not count them toward the calibration gate |

Items from `research_v4_levers/calibration.md` that remain valid and are not repeated: C1 (bias-corrected scaling for the reported probability), C2 (option-count bucket T with clip audit), C3 (aligned ECE protocol), C4/C5 (conformal and risk control), C8 (score choice by AURC), C9 (CPU correctness head), C16 (per-slice risk-coverage). Rejected there and still rejected: Laplace/LoRA ensembles/BLoB for serving (C17).

A second cheap training-side idea with direct evidence, not in the table because it is an optimizer choice the plan has not discussed: very large weight decay on the LoRA **B** matrix only (lambda 1e2-1e3 in AdamW) with a 5-member ensemble gave cqa ECE 0.153 (single LoRA) to 0.029 (LLaMA-13B, accuracy 0.808 to 0.818; few-shot 0.054 at 0.613). Regularizing A did not fix overconfidence; both matrices lost accuracy (arXiv 2310.00035, Appendix B). The ensemble is the expensive part; B-only decay alone is untested at 4B and untested with a cosine one-pass schedule (UNVERIFIED), so it is a pilot candidate, not a recommendation.

---

## 5. Exact settings to pre-register (write before any C2.1 row is rendered; none of this changes a C2 bar)

Bars below are PROPOSALS for the planner and Opus, each calibrated so that **C2 as measured on dev would fail it** (so the bar has teeth) and written before any C2.1 look. They are not retroactive.

**PR-1 Calibration pool and temperature fit (post-hoc, replaces the L1 median-of-groups rule for C2.1)**
- Calibration pool = (a) held-out families never trained, at least 3, at least 1,000 rows in total, one of them a verdict/compliance-type family with a resolvable gold; (b) the unseen-source general dev (D2, 3,847 rows) and the zero-shot / no-card splits (devzs, dev_nc); (c) trained-family mixdev, weight capped at one third of pool rows.
- One T per question type (yes/no, choice); per option-count bucket for choice only if each bucket has at least 300 pool rows (plan A28).
- Objective = domain-balanced mean NLL (each domain equal weight; domains with fewer than 30 rows of that type skipped), grid 0.25-10.00 step 0.05 (same grid as C2), argmin (first on ties).
- **Floor T >= 1.00 for any CE-trained candidate** (C2 evidence: pooled optima 1.05-3.25 on every set; leave-one-domain-out values 1.1-1.3; Rafe and Das stored T 1.30-2.35). The floor is a safety rule with a small price: C1's per-set optima go as low as 0.85 (devp_card ECE 2.71 at T=1 vs 2.18 at its optimum), so it can cost up to about 0.5 pt on sets where a model is mildly underconfident. If a label-smoothing arm is ever adopted the floor becomes 0.80 (smoothed models can be underconfident, Desai and Durrett). Ceiling 2.00 with a clip audit: if any type's pooled optimum exceeds 2.00, or max/min of per-domain optima exceeds 2.0, report it and ask Opus whether the family is out of scope for a scalar T (C2: T19 3.25 vs 1.1-1.3 elsewhere). The plan's [0.8, 1.3] bound (`C2_1_PLAN_v3.md:1027`) is replaced by [1.00, 2.00]; the reason is C2's measured failure, written down now.
- Never fit T on sealed data, never on a single family set, never on the median of sub-100-row groups.
- Report for every model in one table, same rows: ECE at T=1, at the shipped T, and at 5-fold cluster-disjoint cross-fitted T (plan v3.2 A27), top-label (10 equal-mass bins) AND yes/no P(yes) (10 equal-width bins), both with paired cluster-bootstrap CIs, plus Brier, NLL, AURC, E-AURC and mean-confidence-minus-accuracy.

**PR-2 Training length and snapshots**
- Epochs = 1.00 over the final mix (C2 ran 0.9901). The plan's "Epochs: 2" (`C2_1_PLAN_v3.md:919`) is replaced. A second pass is allowed only if a pre-registered pilot shows held-out-family NLL (post-T) still falling at the end of pass 1 on the pilot mix; otherwise not. This is an epoch-count choice, not a data-scope cut: every approved row stays in the mix.
- Peak LR and alpha/r no higher than C2's (lr 5e-5 cosine, r16 / alpha 32, batch 16 per `C2_REPORT.md:44`); the plan's fallback "LR 1e-4" (`:917`) applies only if a C2 value is missing, which it is not.
- Save LoRA states at 8%, 17%, 25%, 33%, 42%, 50%, 58%, 67%, 75%, 83%, 92%, 100% of steps (12 states). Read at least the 25%, 42%, 58%, 75%, 100% states on L4 (free) over the calibration pool.

**PR-3 Selection with calibration (extends plan A25/A28; eligibility filter, not a searched weight)**
A candidate (snapshot, alpha point, last-K, soup) is eligible only if ALL hold on the calibration pool, using PR-1 leave-one-domain-out T:
- (E1) mean-domain top-label ECE <= C1's mean-domain ECE + 1.0 pt (dev measurement for C1 under the same protocol: 6.2-6.6; C2: 8.1-8.3, so C2 would fail by about +1.9);
- (E2) mean confidence minus C1's mean confidence <= (accuracy minus C1's accuracy) + 1.0 pt on the pool (C2: +3.3 vs -0.5, fails);
- (E3) held-out-family accuracy >= C1 - 1.0 pp (C2's transfer was -4.8) and AURC (pool) <= C1's AURC + 0.4 (C2: +0.69 general, fails);
- (E4) the abstain ratio of PR-4 is within bound.
Among eligible candidates take the highest S (plan v3.2 S: general dev + C/R mixdev + held-out sub-family score). If none is eligible, ship nothing from C2.1 for the calibration claim and say so; do not relax (E1)-(E4) after the reads.

**PR-4 Abstain balance (data rules and a monitor)**
- For every family with an abstain-type gold ("Cannot be determined", ASK, none of these): abstain-gold share at most 33% for 3-way verdicts and at most 10% of all training rows in total (Bianchi: 2.5-5% effective, 9% over-refused); every abstain item has a program-built resolvable twin with the same surface form and a different gold; no family's abstain-gold share below its measured test rate minus 10 pp.
- Monitor at every read snapshot, on every held-out verdict family: predicted-abstain count over gold-abstain count. Ineligible if above C1's ratio (T19 dev: 2.08; C2 2.92); target at most 1.5.

**PR-5 Calibration replay buffer (post-hoc, A29)**
- m = 200 rows per question type held out of training and of the T-pool (disjoint), refit T and split-conformal thresholds on the served merged weights after the last parity-relevant change (Shihab: coverage back within 2 pts at m = 200). Print every guarantee with its ASK rate, as plan A29 already requires.

**PR-6 Pilot rule for loss changes (only if the owner funds it; about $2.2 per arm on 10K rows, DERIVED from C2's $13.14 / 59,340)**
- Arms on identical 10K-row subsets, same seed, one pass: CE (control); LS e = 0.05 on the restricted option softmax over new rows only (KD rows untouched, floor 0.80 for this arm). Optional third arm: B-matrix-only decay (not a recommendation).
- Adopt LS only if ALL: leave-one-domain-out pool ECE improves by at least 1.5 pt vs control; pool AURC not worse by more than 0.3; accuracy within -0.3 pp; PR-4 ratio not worse. Otherwise plain CE. Focal: no arm unless the owner asks.

**PR-7 Report-only items that cost nothing**
- Re-score the already-taken C2 L1 reads under T=1 and PR-1 T, labelled "post-hoc, report-only, not a verdict" (see 2.3).
- Keep the 3.5% ECE ship gate as is (plan v3.2 section 3) and the stricter aligned-ECE claim rule for "better calibrated than Jev" (<= 3.0%, target 2.5%); none of PR-1 to PR-5 is expected to reach 3.0% on a shifted pool by itself (DERIVED: C1 itself is 2.78 on the general pool and 6.9 on the transfer pool at oracle T).

---

## 6. Corrections and flags for the existing plan and report

1. `C2_1_PLAN_v3.md:919` "Epochs: 2 over the mix unless C2's measured s/step makes the cost cap bind; then fewer, stated" vs C2's 0.9901 epochs (`C2_REPORT.md:44`); the plan's cost line (`:969`, "$0.23-0.25 per 1K rows at 2 epochs ... stage A about $26-28") is a one-pass figure at C2's measured rate: 112.5K rows / batch 16 = 7,031 steps per pass x $3.58 per 1K steps ($13.14 / 3,673 steps) = $25.2 per pass, about $50 for two. Which basis the plan means is UNVERIFIED; resolve before GO #1 and pre-register the epoch count (PR-2).
2. `C2_1_PLAN_v3.md:1027` T bound [0.8, 1.3] and "fit on mixdev including the hard bin": for C2 this produced the sharper-than-data T. See PR-1.
3. `C2_REPORT.md:162` already says "S cannot see transfer". The same is true of the report-only yes/no ECE on general dev (+0.35 pt) versus the sealed +9.1 pt. Calibration must be gated on held-out families (PR-3).
4. `research_v3/recipe.md:49` says "no label smoothing ... simplicity/Modal-cost choice, not evidence-driven". That stands; this file adds the ranking reason: smoothing hurt failure prediction in the one study that tests it (AURC 9.94 to 24.50) and the output-level analogue gave -3.1 pt on transfer versus -11 pt for oracle temperature.
5. `research_v4_levers/calibration.md` C11 recommended skipping focal loss; the Mukhoti text numbers (SST CE 7.37 vs FL-3 16.05) support that for text.

---

## 7. Unverified, weak or unfinished (do not quote these as facts)

- The sealed-look decomposition (how much of 13.2% is T): UNVERIFIED, DERIVED from a dev analogue only.
- Whether label smoothing, focal loss or B-only decay behave on a 4B Qwen3.5 with a restricted option readout: no source measured it. All "expected effect" cells for those are published numbers from other models or tasks.
- That repeated program-rule exposure (rather than epochs) drives the confidence uplift: hypothesis, consistent with M1/M2, not tested.
- Absence claims ("no study varies replay ratio and reports ECE", "no study shows synthetic data causes overconfidence") come from my web searches only.
- Dev ECE caveats: 10-bin ECE on n = 208-600 is upward-biased by roughly 1-2 pt; every comparison above is paired on identical rows; domain results for T19 (n = 300, 98 verdict rows) are noisy; bootstrap used 400 draws.
- SWA vs soups: the image-classifier gain from SWA (Zhu 2022) does not transfer automatically to LoRA with cosine decay.
- Sibling-file claims I did not check: arXiv 2509.12235 (best OOD early in SFT); 2510.00526 ("-p" objective).
- Jev's calibration under the independent protocol (3.2-3.3% on typed decisions, arXiv 2610.00346 Table 7) is read from that paper's table; Jev 1.14 may differ.

---

## 8. Sources

Project: `c2_build/C2_REPORT.md:15,44,102,142-143,147,162`; `c2_build/train/L1_T_FROZEN.json`; `c2_build/train/L1_RESULT.json` (two keys); `zed_orch/c21/C2_1_PLAN_v3.md:917-919,951-963,969,1024-1031`; `zed_orch/c21/research_v3/recipe.md:20-21,30-32,49`; `zed_orch/c21/research_v4_levers/calibration.md`; `zed_orch/c21/research_v5_c2lessons/c2_dev_diagnostics.md:36-37,342`; reads in `lean/preds_*`; scripts in `research_v5_c2lessons/calibration_dev_scripts/`.

Papers (arXiv, all opened as PDFs unless noted): Guo et al. 1706.04599; Muller et al. 1906.02629; Desai and Durrett 2003.07892; Ovadia et al. 1906.02530; Mukhoti et al. 2002.09437; Huang et al. 2508.00264 (ICML 2025); Xiao et al. 2210.04714; Zhu et al. 2303.02970 (ECCV 2022); Zhu et al. 2311.13240 (EMNLP Findings 2023); Chen et al. 2211.00151 (ACL 2023); Yu et al. 2206.02757 (NeurIPS 2022); Tomani et al. 2012.10988; Maddox et al. SWAG 1902.02476; Wortsman et al. soups 2203.05482 and WiSE-FT 2109.01903; Laplace-LoRA 2308.13111; LoRA ensembles 2310.00035; CogCalib 2505.20903; Gekhman et al. 2405.05904; Bianchi et al. 2309.07875; Dong et al. 2310.05492; Shihab et al. 2604.23987; Rafe and Das 2610.00346; Hong et al. 2609.36477 and Liu et al. 2410.10414 (guards; numbers via `research_v3/recipe.md`); Zhang and Pavlick 2502.07164 (abstract only); ConformalGuard 2610.14365 (via `research_v4_levers/calibration.md`, not re-read).
