# ADDENDUM_research: what RESEARCH_EXTRA_1-6 change in C

Date: 3 Oct 2026. CPU only, $0. This file does not edit `C_DATA_SPEC.md` or `C_TRAIN_RECIPE.md`. Another job is
editing them now, and the spec and recipe owner applies the ADOPT rows below.

**v4 sync note (3 Oct, after the verifier pass).** Spec and recipe v4 win where this file differs. Commit types are
equal shares, 20% each (spec 4.2), so commit Score is **20%** (1,200 r1 rows), not 25% (rows A4 and B7 below). A4's
mean term covers about **4,350** round-1 ordinal rows (F7 3,150 + commit Score 1,200), not 4,650. B7 never fires
(B6 is not run; section I).

Verdicts:
- **ADOPT**: apply before the round-1 freeze.
- **CONSIDER**: apply only if the stated condition holds, or after an owner OK or amendment.
- **REJECT**: do not do this in C.

Every row was checked against the owner rules:
- no teacher bigger than 4B (C1 as its own anchor is the only teacher);
- commercial licences only;
- skill-based families;
- the sealed suite stays untouched;
- Jev outputs are never an input;
- ejs-5 never chooses a setting.

"Unknown" means no evidence exists for our setup.

---

## 0. Do these first (ranked by value per cost; all $0 on Modal)

1. **A1. Ordinal target lint.** No training target may round to the wrong level.
2. **A3. Score temperature fixed at 1.** A calibration temperature must never feed the expected-level readout.
3. **A4. Mean term on ordinal rows**, `((E−y)·4/(K−1))²` with weight 1.0. This is the only lever aimed at the
   largest ejs-5 Size loss (C1 says `large` on only 4 of 360 rows).
4. **B1. Message-only commit rows.** These match ejs-5's prose-only input and go on the one real skill gap (Gate).
5. **B2 + B3. Per-rule yes base rate (20-80%) on commit Gate rows, plus a gold-free yes-share drift alarm.**
6. **C1-C3. Temperature fitting.** Fit one temperature per type, leaving one held-out group out at a time, on the
   served pipeline and inside [0.8, 1.3].
7. **F2. Rendered-prompt sha assert.**
8. **E1 + E2. FAM-1 step-0 read on the L4, plus a CPU check of the replay yes rate per wording.** These look for the
   source of the "yes" drift. Balancing alone will not remove it.

The expected effect on ejs-5 changes (section B, row B5). On current evidence, about 20-41 of the 38 missing items
come from an early-row edge only Jev has, and C's data cannot buy that. For C, a tie on the full ejs-5 set is the
realistic best case. Report the late rows and Gate next to it.

---

## A. Score rows and ordinal readout (EXTRA_1)

Both Score tests read the expected level E, not the top pick:
- ejs-5 rounds E with ties going to the even level (`ejs5lib.decide`).
- JevBench v1.5.4 grades |E − gold| on the unrounded E (`v154lib.py:111`).

| ID | Verdict | Change (what, how much, where) | Expected effect + evidence | Risk |
|---|---|---|---|---|
| A1 | **ADOPT** | **Ordinal target lint (data builder, mixer).** Builders emit `meta.option_level` (option to level index). For every ordinal row, compute E of the *actual* training target after label smoothing, KD and the C1 anchor, and require `round_half_even(E_target) == gold`. On failure, drop the KD or anchor part for that row and fall back to smoothed gold; drop the row if it still fails. The pass rate must be 100% before the freeze. | Stops targets that teach the wrong level. Vote shares 0.55/0.35/0.10 on a `tiny` row give E 0.55, which reads as `small`. An anchor with p_top 0.8 and 0.2 on the far end gives E 0.6, also wrong. SORD limits: a Gaussian soft label needs α > 0.526; C1's smoothing of 0.05/0.08 is safe (limit 1/3 at K=4). | ~0. CPU only. |
| A2 | **ADOPT** | **Level balance with real end levels.** F7 already has uniform gold, so keep it. Add to commit Score rubrics (§4.2): stratify each rubric so every level, both ends included, is ≥ 1/K − 5 pp of its rows. Add cut-point rubrics inside F7's 7%: a stated quantity binned by stated cut points, with the top level as common as the others. No commit-size items copied from ejs-5. | Targets the pull toward middle levels. On dev, rounded E gives 34 end-level answers where gold has 52. On ejs-5, C1's mean P(large) is 0.081 (0.25 if balanced). arXiv 2609.29769: judges rarely place items at the top levels. Check: on dev ordinal rows, the ratio of end-level predictions to end-level gold goes from 0.65 to ≥ 0.9. | Commit rubrics with a natural skew may run short of end-level rows. Then raise the generation ratio; never relabel. |
| A3 | **ADOPT** | **Score temperature is 1, always.** Recipe item 13 (per-type temperature) is fitted for choice and yes/no only. Score rows feed E at T = 1, and readout code asserts it. | On dev, the NLL-optimal T for C1 on ordinal rows is 1.6. On the ejs-5 select half, T = 1.6 collapses Size to tiny 0 / small 137 / medium 40 / large 0. nMAE of E barely moves (0.227 → 0.229), so the calibration gain is not worth the collapse. | None. |
| A4 | **ADOPT** (fallback: drop it if the unit test or pre-flight fails) | **Mean term on ordinal rows only (trainer loss).** `L += λ·((E − y)·4/(K−1))²`, with λ = 1.0. E is taken over the letter probabilities mapped through `meta.option_level`, and the rescaling puts every K on TRACT's 1-5 range. No variance term. It applies to about 4,650 round-1 rows (F7 3,150 + commit Score 1,500), plus replay rows with level numbers (the mixer counts these). It uses the existing 20% ramp. A CPU unit test on fixed logits must pass, and the term must be finite in the memory pre-flight. | In-domain evidence is strong: RAFT on Gemma-2 2B, RMSE 0.70 (CE, top pick) → 0.67 (CE, expected value) → **0.47** (trained on E). TRACT without CoT, r 0.557 → 0.623 at λ = 1. Mean-variance loss, MAE 3.32 → 2.51. On ejs-5 Size (18 of the 38 missing items), the effect is **unknown**. Even Opus 5 reaches only 45.8%. | It is a code change in a one-candidate round and is untested with a letter readout. λ is borrowed from TRACT. It touches only ordinal rows (a few % of the mix). Watch ordinal Brier/nRPS on dev. |
| A5 | **ADOPT** (rule) | **No T < 1 lever, and no readout change chosen on ejs-5.** Keep the shipped 2-view Score readout (given + reversed order, probability mean). | On dev, T = 0.5 gives 48.8 vs 51.2 at T = 1. On ejs-5, T = 0.5 moves 30 of 177 rows, all to a neighbouring level, and never creates `large`. C1's two views agree on 322 of 360 rows (no flip of the scale). | None. |
| A6 | CONSIDER | Show ordinal scales only in natural or fully reversed order in training permutations, never shuffled. This is a trainer change, applied only if the round-1 run shows view agreement on dev ordinal rows below 89%. | Competitor lesson J. C1 already reaches 89.4% agreement under random shuffles, so the gain is likely small. | Trainer code change. |
| A7 | REJECT | Variance term (Pan et al. λ2), CORAL/CORN-style "at least level k?" yes/no rows, SORD soft labels. | Variance term: hurts calibration (JevBench nRPS, OHS Brier). Level-k rows: untested for LLMs, and they add yes/no rows that could feed the yes bias. SORD labels: risk targets that fail the A1 lint. | - |

## B. ejs-5 gap: commit block and expectations (EXTRA_2)

| ID | Verdict | Change | Expected effect + evidence | Risk |
|---|---|---|---|---|
| B1 | **ADOPT** | **Message-only commit rows (§4.2).** For 30% of Gate, Triage and Route commit rows, show the commit message only, with diff and numstat hidden. Labels still come from the program over the real commit. Keep a row only if the decisive fact is stated in the message (program check on the rule's trigger entity, then the G5 re-read). Drop failures; never relabel them. Score rows keep numstat shown (rubric skill). | ejs-5 inputs are prose only (PREREG_ejs5 §7). The spec shows message + diff + numstat, which trains a different skill. Gate (-13 items) is the one gap that holds in both periods and both adapters, and at least 7 of the 13 items are discrimination (estimated AUC 0.58; Jev's accuracy needs about 0.69). Late Gate n = 66 (CI about ±13 pp), so one round may show nothing on ejs-5. Sealed B1 commits are the earlier read. | The trigger check may leak a keyword shortcut. Fix: include rows that mention the trigger where gold is "no" (for example "migration + test added"). Copies no ejs-5 item or wording. |
| B2 | **ADOPT** | **Per-rule yes base rate on commit Gate and Match rows:** each rule draws its rate uniformly from 20-80%, aggregate 50 ± 2 (the same rule as own families, spec 2.1/G10). §4.2 today lists Gate as 50/50 with no per-rule spread. | C1 says "yes" on only 36 of 180 ejs-5 Gate rows, and its mean P(yes) is 0.312. In-domain it leans "yes". The prior flips across domains, and a fixed 50/50 per rule cannot teach the model to ignore it. A threshold fix alone is worth about 4-6 items. | Low. |
| B3 | **ADOPT** | **Gold-free yes-share drift alarm**, report-only. On the mix-tuning dev per domain at each snapshot, and on each sealed set at its existing looks only: log mean P(yes) and the predicted yes share. Alarm if any domain that is 50/50 by construction falls outside 30-70%. | Catches the drift the 50/50 data rule cannot see (ejs-5 Gate went to 20% "yes"). | None. No new looks. |
| B4 | **ADOPT** (rule) | **No test-time prior fix ships** (Batch Calibration, EM, BBSE, median cut). | Run on C1's ejs-5 probabilities, EM collapses: Gate goes 100% "no" and Score 91% "small". BBSE's assumptions fail on a new task form. Serving is one request at a time. | - |
| B5 | **ADOPT** (expectation) | Report ejs-5 as **full set + late rows + Gate**. Write into C's expectations that a tie on the full set is the realistic best case. Changing a registered endpoint needs an amendment. | Every system gains on Jev from early to late rows: C1 +6.9 pp, 4B-E +4.2, GPT-5.6 +3.4, Opus 5 +8.8. Jev drops the most (-18.3 pp). Its early-row edge is about 20-41 of the 38 items (SE about 3.6 pp, so the interval runs from about 0 to all 38). C1 already ties on late rows (46.3 vs 45.9). | It is a framing change, so disclose it in advance. |
| B6 | CONSIDER (needs the owner's counts-only OK and a PREREG_FINAL amendment like A13, written before the run) | **ejs-5 decomposition (EXTRA_2 §7).** Commit-split select and confirm halves. Steps: label mix by period; DiD vs Jev, also standardized to the early label mix; an oracle prior bias fitted on select and scored on confirm; Score argmax vs the official readout. Aggregates only. About 1 min of CPU. Report-only. | Tells time apart from label mix before the commit mix is frozen. The prediction is logged in EXTRA_2 §6: standardized Score DiD ≥ +10 pp, prior + readout ≤ 10 items, Gate residual ≥ 7 items. | It reads ejs-5 gold (counts only), and this job may not. It must never choose a model or readout. |
| B7 | CONSIDER (only if B6 runs and its "time-linked" rule fires) | Cut commit Score from 25% to ≤ 10% and move the share to message-only Gate (B1). Otherwise keep 25%. | Score is near chance for everyone (C1 32.2, Jev 37.2, Opus 45.8). Its gap is all early rows (-26 early, +8 late). | Hurts sealed B1 / JevBench Score practice if cut without cause. |
| B8 | REJECT | Slice discovery (Domino), memorization probes on Qwen3.5-4B, black-box contamination tests on Jev. | Domino finds 36% of planted slices and needs item text. MIA probes are confounded by time shift (Duan 2024; Das 2024). Jev calls are forbidden. | - |

## C. Calibration under shift (EXTRA_3)

| ID | Verdict | Change | Expected effect + evidence | Risk |
|---|---|---|---|---|
| C1 | **ADOPT** | **Recipe item 13 refined.** Fit one temperature per type (choice, yes/no; Score excluded per A3). Fit it leaving one group out at a time, where the groups are the mix-tuning dev's held-out sampler, pack, format and repo groups plus F14. Choose T by the **median-group NLL**, bounded to **[0.8, 1.3]**. | Fitting T on familiar data fails under shift (Ovadia 2019; on Criteo, TS gave a worse Brier than no calibration). A cross-task single T keeps about 71% of the possible ECE gain (Thermometer, MMLU: 0.260 → 0.119, best possible 0.062). C1's dev refit is 0.95 / 1.05 for about 0 gain. | Accuracy 0. Few groups → keep the bound. |
| C2 | **ADOPT** | **Fixed order:** aggregate views → fit T on the aggregated output of the exact served pipeline → band edge (JevBench only). D4 Brier is measured on that same pipeline, never on the 1-view read. | Choice 2-view ECE goes 0.032 → 0.038 (Wu & Gales effect). A T fitted on the 1-view read is fitted on the wrong thing. | None. |
| C3 | **ADOPT** | Add a report-only Brier and over/underconfidence gap on the **unseen-group** mix-tuning dev. | The direction of C1's miscalibration flips under shift: OHS-1 yes/no +3.2 (overconfident), OHS-2 -4.9 (underconfident). Dev-wide D4 cannot see this. | None. |
| C4 | **ADOPT** (rule) | Yes/no stays a single read. If yes/no views are ever added, average **logits**, then refit everything. | Synthetic test, view noise SD 1.0: rows in the band 33.4% (probability mean) vs 27.4% (logit mean); committed accuracy 61.3 vs 66.3. C1's real letter-swap views differ by only 0.0043. | - |
| C5 | CONSIDER | Vary the gold-NEI rate per card (0-20%), keeping the ~10% aggregate (spec F6 target). | The model does not learn one fixed NEI prior per format. UCPA: assuming a uniform prior beats estimating it when the prior is unknown. | Low. |
| C6 | **ADOPT** ($0 CPU) | Reconcile the OHS-1 yes/no Brier (recompute 0.152 vs 0.133; the recipe cites 0.140 vs 0.114) before the recipe cites it again. | Doc correctness. | None. |
| C7 | REJECT | EM+BCTS per-set prior readout, Thermometer-style T predictor, batch calibration, OTTER, weighted conformal. | They need test batches or label priors we lack per request. EM collapses on ejs-5 (B4). There are too few groups for a T predictor (Thermometer used dozens of tasks). | - |

## D. Data selection (EXTRA_4)

| ID | Verdict | Change | Expected effect + evidence | Risk |
|---|---|---|---|---|
| D1 | **ADOPT** (no change) | Keep spec 2.1's stratified selection for own rows and replay. No LESS, influence, IFD or targeted selection in round 1 or 2. Replay stays representative, keeping the existing rule that drops human-labelled replay rows with C1 p_g < 0.2. | C keeps about 67% of its own rows and 19-40% of replay. LESS falls below random at 10-15% budgets (BIDS: 44.4 vs 44.9; 45.2 vs 45.7). On 1M-row pools, no selector beat random (2410.09335). Gradient picks copy the target's answer format (2609.19589). | - |
| D2 | CONSIDER (only if the G9 L4 crowd pass can log C1's pooled hidden states at no extra time; pre-register before any C row exists) | Pick public rows (3A-3E) by facility location on those hidden states, per dataset × label cell. Coverage only, with a per-document cap and the P5 checks after selection (label × bin chi-square, option-count shares ±2 pp, near-duplicate rate). | Small gain, mostly in the worst case (QDIT). Only these pools have a low keep ratio. | Code in the G9 pass. |
| D3 | REJECT | LESS or RDS+ targeting; a new selection-target split; copying LIMO or s1. | No evidence that targeting beats random on unseen domains. LESS costs about 20-30 L4-h. LIMO and s1 need bigger teachers and CoT. | - |

## E. Interference and loss weights (EXTRA_5)

| ID | Verdict | Change | Expected effect + evidence | Risk |
|---|---|---|---|---|
| E1 | **ADOPT** step-0 read; CONSIDER the 25/50/75% reads (only if the measured step-0 read is ≤ 50 min) | **FAM-1 monitor, report-only, on the L4** (Google credit, $0 Modal). Group-gradient affinity onto old and new targets, normalized by split-half reliability. Yes-push attribution per family and per loss term. Positive and negative controls. Exact lookahead for the top 3 suspects. Groups are 13 families + ~8 replay clusters, 64 rows each. | It finds what drives the "yes" drift. On affirmative questions with gold "no", C1 scores 80.4 vs 85.4 for 4B-E. C1's training data is already balanced (49.7% yes; KD teacher P(yes) on gold-no rows 0.092), so balancing alone will not fix it. TAG: affinity measured on train and validation batches agrees, Pearson 0.98. | About 40-80 min per read (estimate). The output is invalid if the controls fail. It never moves a weight by itself. |
| E2 | **ADOPT** ($0 CPU) | Check the replay yes rate **per instruction wording** (G10 checks wording only for new rows). Re-stratify any wording cell outside 50 ± 5%. | Tests the wording-prior hypothesis for the yes drift. | None. |
| E3 | **ADOPT** (rule) | Keep C1's loss weights in round 1. No PCGrad, GradNorm or LoRAMoE. The first flag candidate is relation `lam` 1.0. A flagged term (EXTRA_5 §4 flag rule, at ≥ 2 of 3 reads) gets exactly one change, halving its weight, by amendment and before round 2 only. | Kurin 2022 and Xin 2022: a tuned weighted sum matches the multi-task optimizers. R-Drop: a consistency weight of 1.5 is worse on all 4 GLUE tasks shown, and MNLI is best at 0.5. A 3-point weight sweep costs about $85, which does not fit the cap. | - |
| E4 | CONSIDER (only if round 2 runs) | Recipe 7.2 share cuts may use FAM-1 only when the jackknife CI is below 0 at ≥ 2 reads, the exact lookahead agrees in sign, and the old slice points the same way. Inside the existing bounds. | Xin: act on shares and confirm on outcomes. | Needs an amendment. |

## F. Qwen3.5 hybrid and recipes (EXTRA_6)

| ID | Verdict | Change | Expected effect + evidence | Risk |
|---|---|---|---|---|
| F1 | **ADOPT** (no change) | Keep `targets: QWEN35` (all 32,464,896 LoRA params) and C1's adapter as the starting point. | Recall lives in the 8 attention layers (Qwen3.5-4B: 0.89 with only the attention cache vs 0.00 with only the DeltaNet state). But the attention-only LoRA result (+10.2 vs +7.8) comes from 0.8B, 1 seed and 128-256 items. | - |
| F2 | **ADOPT** ($0 CPU) | Pre-flight assert: sha256 of the **rendered** prompt is identical in training, dev gate and serving for 3 fixed rows. The `decoder_io.prompt` fallback must raise for Qwen3.5. External servers pass `enable_thinking: false`. | Blocks silent template drift. Tulu 3: templates alone spread results by 1.4 pts. Locally, the chat-template prompt took a frozen model from 0.653 to 0.710. | None. |
| F3 | **ADOPT** (inside F13's 4.5%; low confidence) | F13 "aggregate" sub-type, about 20% of F13 rows. The answer needs facts from 2-3 sections (counts, latest valid version, totals split across sections), with program labels. | Olmo 3: program-made aggregation questions inside real documents beat plain long documents. Effect on LongBench v2: +0 to +2 pp, because most of it is beyond our 7.9K cap. | Generator work only. |
| F4 | **ADOPT** | Persona seeds for Claude-written scenarios: O*NET occupation titles (CC BY 4.0, LICENCE_REGISTER line 176). **Never** PersonaHub (CC-BY-NC-SA-4.0). | Diversity. Tulu 3: removing the persona sets cost 1.5 points on average. | None. |
| F5 | REJECT | Blending C with C1, averaging snapshots, seed soups. | Recipe 6.2 allows no blend or snapshot as a candidate. Step B (A11) found softened adapters flat or worse. Tulu 3: a seed soup equals the best seed at SFT scale (60.2 vs 60.1). If a blend is ever wanted later, the math rule is: blend the LoRA products (rank-32 concatenated adapter or an fp32 merge), never the A and B factors separately. | - |

---

## G. Open questions from the user's message

- **"B1: flag the weights and test on L4"** is Step B (A11). It ran and is closed: no softened C1 passed its confirm
  (`logs/b_wiseft_result.json`, commit 599c513).
  - a = 0.9 failed the unseen-source check: 84.33 vs 84.43, with +0.5 required.
  - Lower values were worse on select-unseen: 83.38 / 82.69 / 82.06 vs C1 83.53.
  - Decision: C starts from C1 at full strength.
  - The only live "flag a weight" path is now E3/E4: FAM-1 on the L4 flags a loss term or family. It is report-only
    in round 1, and the only allowed action is halving one weight by amendment before round 2.
  - (Sealed part "B1", the 300 held-out commits, is a separate thing. It stays a read-only P3 guard.)
- **The stopped "debug research" and its flow** are not covered by this addendum or by RESEARCH_EXTRA_1-6. They need
  their own task.

## H. Unknowns that matter for the ADOPT rows

- A4: the right λ for a 4B LoRA with a letter readout; its effect off-domain.
- B1: how often a commit message states the decisive fact (the measured keep rate sets the real row count).
- B5/B6: the gold mix by period, and whether Gate is exactly 90/90 (all the Gate numbers derived here assume 90/90).
- E1: L4 time per monitor row, and the split-half reliability of 64-row groups.
- C1: whether there are enough held-out groups for a stable median-group T.

---

## I. Orchestrator decisions (3 Oct ~15:00 UTC, before any C row exists)

- **B6 is NOT run, and B7 therefore never fires.** ejs-5 stays a clean final check, and nothing reads its gold for
  diagnosis. Commit Score keeps the share in the spec. This keeps the owner rule "never tune on held-out tests".
- **Every ADOPT row stands on dev or external evidence alone.** The ejs-5 numbers quoted in A2, A3, A5, B1 and B2 come
  from gold-free predictions and published aggregates, and they are context only.
  - A3 keeps Score T = 1 because that is the shipped A5 readout (`prep89/READOUT_DEV.md`). ejs-5 did not choose it.
  - B1 follows ejs-5's public input format (prose only, PREREG_ejs5 §7). It uses no ejs-5 item or wording.
- **Section G:** the owner's "debug research" was this deep research (a voice-transcription slip). It is complete
  (RESEARCH_*, RESEARCH_EXTRA_1-6, reviews, this addendum). No separate task is needed.
- **A4 is the only new trainer-loss term in round 1.** It must pass the CPU unit test and the memory pre-flight.
  Ordinal Brier/nRPS on dev is a report-only guard, and the frozen gate still decides shipping.
