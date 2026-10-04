# Competitor lessons for C (data and recipe)

Angle: what the strongest open decision models did, where they win and lose against Jev, and what we should copy or avoid in C.
Date: 3 Oct 2026. Web research only. CPU only. No paid calls.
Numbers are as published by each author or board. "Unknown" means not published.
Reference numbers are in brackets, like [12]. The full source list with URLs is at the end.

---

## 0. Bottom line (read this first)

1. **No open 4B matches Jev on broad, unseen tasks.**
   - Decision Index 0.2.1 (38 benchmarks): Jev 57.91. Best 4B is JPT-4B at 43.04. A frozen Qwen3.5-4B scores 32.35. [1]
   - On pooled raw accuracy across 32 Index benchmarks, Jev is 73.9% and the best 4B is 66.5%. That is a gap of about 7 pp. [1]
   - Our ejs-5 result (C1 54.1 vs Jev 58.5, -4.4) is normal for this field. It is not a special failure.
2. **Most big 4B wins over Jev are in-distribution.**
   - Most of the large wins come from models that trained on a split of the same source, or on a near copy of the task.
   - Examples: lev on BANKING77 (+7.0), JPT-4B on ContractNLI (+8.0), Jet on CLINC150 and When2Call. [1][6][8][9]
   - Two wins look like real Jev weak spots rather than leakage: SATA-Bench (multi-select), where 8 of 18 small models beat Jev, and PhishNChips. [1]
   - Gains on public sets often vanish on sealed or new-family sets. Plumb-4B reached 80.2% on the public hard tier, but its JevBench Intelligence score is 55.8 against Jev's 72.0. [2][13]
3. **Jev's lead is biggest on new task families and on knowledge.**
   - On Kev-v9's 390 new decisions, Jev scores 85.6%. Winnow-12B and Kev-9B score about 69%. [4]
   - Knowledge is set by the base model. Jev scores 82.7 on MMLU-Pro. The best 4B scores 51.6. [1][7]
   - Data cannot close the knowledge gap at 4B. Breadth of decision skills can close part of the far-domain gap.
4. **Breadth of training data is the lever that moved transfer.** This is Kev's strongest finding. [7]
   - On the same base and the same method, broad data gave +9.1 pp on Kev's panel and +2.9 pp on short states.
   - Switching from LoRA to full weights on the same data gained nothing and cost 3.0 to 3.7 pp.
   - More rows from the same generator saturate fast: +26 pp from the first 6,000 hard-v1 rows, then only +5 pp from the next 12,000.
5. **Specific data types fixed specific failures.**
   - **Yes/no questions where "yes" is the bad outcome:** lev's aegis2 score went from below chance to equal to Jev. [8]
   - **Word-swap negatives:** PAWS 0.612 → 0.716. [8]
   - **State-tracking logs:** decider-12b's fresh yes/no score went 58.8 → 71.6 (chance-corrected). [5]
   - **Stating day counts:** date items 0.65 → 1.00. [7]
   - **Real documents:** they beat buried synthetic states for long-document work. [7]
6. **Teacher agreement filters are universal, and labelled teacher data is the norm.** Every leader used one.
   - Winnow uses the teacher distribution only when the teacher agrees with gold. [3]
   - Eikos, imajev and pplx keep only items where blind relabels agree. [10][12][14]
   - The decider teacher agreed with only 72% of its own labels. [5]
   - Our rule (Claude writes the items; programs or human gold give the labels) fits this pattern. Program gold is stronger than their 27B-teacher votes.
7. **Replay helps at 4B, but anchoring toward the old model is mixed.**
   - decider v2.1 used a KL loss toward v1 on replay rows. It recovered sampled-play skills (+14.1) but lost 2.7 pp on the JevBench hard tier and worsened calibration. [5]
   - Kev lists "anchoring toward the base's answers" and WiSE-FT among its negative results. [7]
   - Keep the C1 anchor small. Gate it on hard and new-domain suites.
8. **Pick checkpoints early, and use a held-out-domain dev set to pick them.**
   - pplx-decider picked update 200 of 286 (70% of one epoch). [14]
   - Jet picked step 250 of 1,000. [9]
   - Bosun picked epoch 2 of 3. [15]
   - Kev and pplx both split domains three ways: train, calibration and confirmation. [7][14]
9. **Fit temperature on held-out datasets, per question type.**
   - A temperature fitted on held-out items from the training sources is in-distribution and fails on new data. Kev measured breadth ECE 0.059 with that fit, and 0.0085 to 0.017 with a fit on held-out datasets. [7]
   - Per-type temperatures help yes/no: decider's yes/no ECE went 0.146 → 0.101. [5]
10. **Licence and contamination hygiene decide whether a model can ship.**
    - JPT is CC BY-NC because of its data. Hopper's 4B adapters are research-only because they used RACE. [6][16]
    - The Decision Index counts trained test items as wrong. It removed reflex-4B, which had trained on 800 MMLU-Pro test items (65.8% on those items vs 52.1% on held-out items). [1]

---

## 1. Caveats on the numbers

- **JevBench has many versions and scorers.**
  - v1.2 and v1.4 report public-set accuracy (231 items: 48 easy, 72 standard, 111 hard).
  - v1.5.x scores Intelligence on 1,624 decisions. Of these, 720 are sealed, and the sealed items make up half of the Intelligence score. [2][19]
  - Under v1.4.1, Jev scored 86.6% on public items and only 36.7% on sealed items. [19]
  - Public-set accuracies from model cards are not comparable to board Intelligence scores.
- **The Decision Index uses a "skill" score:** (score − chance) / (1 − chance), averaged over 5 equal-weight areas. [1]
  - Unanswered rows count as wrong. Declared training overlap counts as wrong.
  - We pulled the full board file (`data/index.json`, generated 2026-09-28) from the Hugging Face Space. All per-benchmark numbers below come from that file.
- **Most model-card numbers are self-reported.** The authors' own suites are often in-family. Bosun says so openly. [15]
- **Model sizes:** "4B" here means Qwen3.5-4B (4.66B served parameters on the board).

---

## 2. Scoreboards

### 2.1 Decision Index 0.2.1 (Jev and selected entrants) [1]

Area skill scores in %: K = Knowledge and Reasoning, L = Language, R = Retrieval and Classification, T = Tools and Automation, A = Arts and Human Taste. ECE is pooled over 32 benchmarks.

| System | Base | Method | Index | K | L | R | T | A | ECE |
|---|---|---|---|---|---|---|---|---|---|
| **Jev 1.13.0** | undisclosed | hosted | **57.91** | 51.4 | 62.0 | 55.4 | 75.1 | 37.7 | 0.074 |
| Surogate Rune 26B-A4B v3 | Gemma-4-26B-A4B | full FT | 57.44 | 43.4 | 63.1 | 63.5 | 71.2 | 41.9 | 0.120 |
| Decider chat (no training) | Gemma-4-31B | prompt only | 57.33 | 44.3 | 60.4 | 63.1 | 75.6 | 38.3 | 0.047 |
| pplx-decider-v1-27b | Qwen3.8-27B | full FT | 56.40 | 40.9 | 63.5 | 54.9 | 79.3 | 39.4 | 0.018 |
| simple-jev (no training) | Qwen3.8-27B | prompt only | 55.74 | 36.6 | 62.1 | 63.2 | 76.2 | 36.5 | 0.113 |
| Jebadiah 27B | Qwen3.8-27B | LoRA | 54.67 | 38.8 | 60.7 | 53.9 | 78.1 | 38.7 | 0.014 |
| Eikos-27B | Qwen3.8-27B | LoRA | 53.13 | 39.9 | 54.3 | 55.9 | 74.4 | 39.8 | 0.057 |
| Winnow-12B | Gemma-4-12B | LoRA | 50.02 | 33.8 | 56.0 | 54.0 | 71.0 | 30.0 | 0.168 |
| JPT-9B | Qwen3.5-9B | LoRA | 46.89 | 31.7 | 56.7 | 44.6 | 67.0 | 28.6 | 0.077 |
| **JPT-4B** | Qwen3.5-4B | LoRA | **43.04** | 28.7 | 52.5 | 45.0 | 57.2 | 25.8 | 0.079 |
| Jet v6.2 | Qwen3.5-4B | LoRA | 42.60 | 28.7 | 43.9 | 48.2 | 62.9 | 27.0 | 0.141 |
| Hopper (G) 1.2 | Qwen3.5-4B | LoRA | 40.77 | 25.2 | 44.8 | 45.4 | 60.1 | 26.0 | 0.093 |
| Decider 4B | Qwen3.5-4B | full FT + LoRA | 40.70 | 25.7 | 46.0 | 44.7 | 58.6 | 25.0 | 0.084 |
| JevK5 | Qwen3.5-4B | LoRA | 38.81 | 23.5 | 43.3 | 46.2 | 52.1 | 27.8 | 0.027 |
| lev | Qwen3.5-4B | LoRA + head | 38.54 | 22.0 | 38.5 | 47.9 | 57.5 | 28.0 | 0.064 |
| Intern-Decision-4B | Qwen3.5-4B | full FT | 37.81 | 23.7 | 41.9 | 40.3 | 55.7 | 26.1 | 0.028 |
| Kev 4B (old checkpoint) | Qwen3.5-4B | LoRA + head | 34.64 | 22.9 | 35.3 | 41.0 | 52.6 | 17.9 | 0.176 |
| Jobe (frozen, no training) | Qwen3.5-4B | prompt only | 32.35 | 17.7 | 34.5 | 36.7 | 48.8 | 25.7 | 0.123 |
| Bosun v3.1 1.7B | Qwen3-1.7B | LoRA + head | 20.10 | 4.7 | 12.4 | 42.8 | 34.8 | 7.5 | 0.130 |

What this shows:
- **Fine-tuning adds about +11 index points at 4B** (frozen 32.35 vs best 43.04).
- **At 27-31B, fine-tuning adds about 0 points.** A prompted Gemma-4-31B (57.33) almost ties Jev. The full-weight pplx fine-tune scores 56.40.
- **Pooled raw accuracy (1-in-6 sample, 32 benchmarks):** Jev 73.9%; JPT-4B 66.5%; Jet 66.0%; Decider-4B 64.9%; JevK5 64.8%; frozen 4B 60.7%.
- **Jev is not the best-calibrated system.**
  - Jev's pooled ECE is 0.074. JevK5 (0.027), Intern-Decision-4B (0.028), pplx (0.018) and Jebadiah (0.014) are all better calibrated.
  - Jev's weakest calibration is on Retrieval (ECE 0.154).
- **Systems that score far above Jev use test-time reasoning, which we do not use:**
  - GLiDE claims 64.81, with Tools 83.5 vs Jev's 75.1 and Knowledge 62.9 vs 51.4. [17]
  - Rune with thinking scores 59.2. It thinks on about 1 question in 10 (when confidence is below 0.7, up to 512 tokens, about 5 s). [11]

### 2.2 Per benchmark: best of 18 Qwen3.5 2B/4B entrants vs Jev (raw score) [1]

**Where a small model beats Jev**, and the likely reason:

| Benchmark | Jev | Best small model | Gap | Small models above Jev | Likely reason |
|---|---|---|---|---|---|
| ContractNLI | 0.717 | JPT-4B 0.797 | +8.0 | 4/18 | ContractNLI is in JPT's training list [6] |
| PhishNChips | 0.625 | JevK5 0.700 | +7.5 | 3/18 | Phishing detection. Jev looks weak here |
| BANKING77 | 0.797 | lev 0.868 | +7.0 | 4/18 | banking77 train split in lev's mix; skips split label codes [8] |
| When2Call | 0.810 | Jet v6.2 0.868 | +5.8 | 1/18 | tool-routing partitions in Jet's mix [9] |
| SATA-Bench (select all) | 0.264 | Decider 4B 0.316 | +5.2 | 8/18 | Jev is weak on multi-select whole-case items |
| FinEntity | 0.870 | JPT-4B 0.919 | +4.9 | 2/18 | JPT's reason unknown; entity-sentiment training is common (Jet trains SEntFiN; Eikos trained on FinEntity itself and is scored 0) |
| CLINC150 | 0.893 | Jet v6.2 0.911 | +1.8 | 2/18 | intent train splits |
| iSarcasmEval | 0.505 | JPT-4B 0.517 | +1.2 | 1/18 | Jet trains on iSarcasm train data |

**Where every small model loses** (gap of the best small model to Jev):

| Benchmark | Gap | Benchmark | Gap |
|---|---|---|---|
| GPQA Diamond | -34.2 | ANLI | -10.3 |
| MMLU-Pro | -31.1 | ACOS (aspect extraction) | -9.5 |
| BBH | -28.8 | API-Bank | -9.1 |
| CRUXEval | -22.1 | HoVer (multi-hop fact check) | -8.3 |
| Home appliances (tool calls, whole case) | -21.6 | New Yorker (humour) | -7.2 |
| WinoGrande | -11.2 | GSM8K | -7.1 |
| CLadder (causal) | -6.8 | NLI4CT (clinical NLI) | -5.5 |

Reading:
- The large losses are knowledge, code execution, multi-step reasoning, adversarial NLI and multi-hop evidence. A 4B in one pass cannot fix knowledge.
- **ANLI, HoVer, NLI4CT, ACOS and Home appliances are decision skills, not knowledge.** These are where better data can still move us.

### 2.3 JevBench v1.5.4 board (Intelligence counts sealed items as half) [2][19]

| System | Intelligence | Calibration | Base |
|---|---|---|---|
| Winnow-12B Q8 | **74.4** | 84.1 | Gemma-4-12B LoRA |
| Jev 1.13.0 | 72.0 | 88.0 | undisclosed |
| Cygnet | 71.1 | 87.0 | frozen Gemma-4-12B-it, no training |
| Surogate Rune 26B-A4B v3 | 69.7 | 88.3 | Gemma-4-26B-A4B |
| djev | 72.3 | 80.4 | DiffusionGemma-26B-A4B |
| JevK5 v0.3 | 56.3 | 88.3 | Qwen3.5-4B |
| Plumb-4B | 55.8 | 87.4 | JevK5 v0.2 + 5.15k hard rows |
| Decision 4B v1.2 | 53.7 | 88.6 | Qwen3.5-4B |
| Imajev-4B | 53.5 | 88.1 | Qwen3.5-4B |

- **The 4B models cluster at 54-56 Intelligence, against about 71-74 for 12B+.** This matches our memory note.
- **A frozen 12B with a good prompt, a letter readout and one temperature (Cygnet) is level with Jev.** At 12B, the base does most of the work.

### 2.4 Unseen-family evidence (the closest public analogue to ejs-5)

- **Winnow's report** (Kev-v9 "new-v9 additions", 390 items) [4]:
  - Jev 85.64%, Winnow-12B 69.23%, Kev-9B 68.97%, Kev-4B 63.59%.
  - On the 231 public JevBench items, Winnow ties Jev at 85.71%.
  - A tie on public items can hide a gap of about 16 pp on new families.
- **Kev breadth-v1 test index** (14 held-out datasets, never trained on) [7]:
  - Jev 54.0, Kev-27B 52.3, Kev-9B 41.0, Kev-4B 38.0.
  - Nearly all of the Kev-27B gap is Retrieval and Classification.
- **Kev transfer-v9 dev:** Jev 0.854, Kev-27B 0.822, AutoJev-27B 0.812. [7]

---

## 3. Competitor notes

Each block covers: base, method, data, readout and calibration, results, then lessons for us.

### Cygnet (blockbrain) [18][2]
- **Base and method:** frozen Gemma-4-12B-it with no fine-tuning, served on stock vLLM 0.30.0.
- **Readout:** options shown as letters A, B, C...; one answer position; logits masked to the option letters; duplicate letter tokens summed, then renormalised.
- **Calibration:** one temperature, T = 3.4, fitted on 241 items they wrote themselves. Public items were used only to measure.
  - Cross-validated: ECE 0.101 calibrated vs 0.140 raw.
- **Yes/no:** options always show "false" first.
- **Many options:** groups of up to 20 options, then the winners are re-read.
  - BANKING77 (20 intents): 87.0% grouped vs 86.5% single pass. All 150 CLINC intents: 91.25%.
- **Results:** public 203/231 (87.9%); hard 85/111. v1.5.4 Intelligence 71.1, Calibration 87.0. p50 latency 66 ms on an A6000.
- **Lessons:**
  - The readout and a temperature fitted on our own items are cheap, solid wins.
  - Present yes/no options in a fixed order.
  - Use a grouped or knockout read for more than 20 options.

### Winnow-12B (EldanRing) [3][4]
- **Base and method:** Gemma-4-12B-it; LoRA r32/a64 on all 7 projections, dropout 0, merged.
- **Data:** private. Synthetic scenarios, teacher-supervised examples and labelled semantic tasks.
  - Families: routing, policy and rule application, evidence selection, workflow decisions, ordinal judgments, entailment, paraphrase and answerability.
  - Contrastive examples vary facts that should change an answer.
- **Training:** an initial decision fine-tune, then a 26,000-example refinement mix with replay.
  - The release was picked after 19,200 presentations. Effective batch 8; 8,192-token cap.
- **Loss:** gold-label CE plus teacher-distribution CE, applied only when the teacher agrees with gold.
- **Calibration:** T = 1.0, no fitted map. The board ECE is the worst of the top group (0.168).
- **Results:**
  - v1.5.4 Intelligence 74.4 (#1).
  - Public 231: 85.71% (= Jev). Kev-v9 clean: 81.55% vs Jev 87.00%. New-v9 additions: 69.23% vs Jev 85.64%.
- **Lessons:**
  - Contrastive minimal pairs plus gated soft targets give the best Intelligence on the JevBench board.
  - Skipping temperature fitting costs calibration.
  - Even this model loses about 16 pp to Jev on unseen families.

### Surogate Rune 26B-A4B v3 (Invergent) [11][1]
- **Base and method:** Gemma-4-26B-A4B MoE (8 of 128 experts active); full fine-tune. Data not disclosed.
- **Readout:** softmax over option-letter logits at the first generated position.
- **Calibration:** overconfident at T = 1. At T = 2, ECE goes 12.5% → 2.2%.
- **Yes/no confidence:** reported as max(p, 1−p).
- **Optional thinking:** when one-pass confidence is below 0.7, it reasons for up to 512 tokens.
  - About 1 question in 10 triggers it. Latency goes 0.2 s → about 5 s. Index goes 53.39 → 54.89.
  - Biggest gains: GSM8K +15.2, CRUXEval +11.4, CLadder +10.4, BBH +8.0.
  - It hurts ForecastBench by 9.8 skill points, because probabilities become more extreme.
- **Results:** Index 57.44 (59.2 with thinking). Ahead of Jev on Language, Retrieval and Arts. Behind on Knowledge (-8.0) and Tools (-3.9).
- **Lessons:**
  - Confidence-gated reasoning is how open models pass Jev on the Index. It is outside our no-CoT design.
  - It could become a later product option for low-confidence items. It is not part of C.

### pplx-decider-v1-27b and AutoJev-27B (Perplexity) [14][7]
- **Base and method:** Qwen3.8-27B, full-weight SFT.
  - The pplx repo ships the `autojev` training code. Its recipe file records the same curated 73,000-row run that Kev describes for AutoJev-27B.
- **Recipe (from `configs/training.json`):**
  - lr 2e-6; weight decay 0.01; effective batch 256; max length 8,192; one epoch.
  - The selected checkpoint is update 200 of 286, which is 51,200 examples or 70% of the epoch.
  - Temperature 2.21, fitted on 3,500 rows.
  - CE loss that accepts soft target vectors. Yes/no targets are a probability. Options are reshuffled every batch.
- **Data generator:**
  - Families: NLI 18k, intent 10k, numeric 10k, news 8k, evidence 4k.
  - Each family has 8-10 named "phenomena". NLI examples: quantifier scope, negation, exceptions, temporal change, missing premise, necessary vs sufficient.
  - Evidence examples: plan vs completed, partial support, scope, date or entity mismatch, missing record.
  - Six render styles (message, dialogue, form, bullet list, report, table) and three length bands.
  - Up to 3 instruction rewordings per family, and label definitions written as criteria.
  - Domains are split three ways. Train uses 12 domains. Calibration uses 4 different domains (museums, agricultural co-ops, sports facilities, publishing). Confirmation uses 4 more (maritime, observatories, wildlife reserves, theatre).
  - Items are written by a frontier API model ("gpt-5.6-sol"). Labels come from "same-model blind agreement; not human gold".
  - An eval-set generator adds conditions: clean, noisy, negated, long, shifted_prior.
- **Results:**
  - Index 56.40, ECE 0.018. Tools 79.3, above Jev's 75.1.
  - Card: 85.71% vs Jev 84.51% over 11 benchmarks, ahead on 7. Behind on JevBench public hard (70.30 vs 73.27).
  - AutoJev vs Kev-27B: hard-v1 +4.9 pp; scienthoon -2.7 pp. [7]
  - The board notes that pplx used WinoGrande, BBH and RAGTruth rows for checkpoint selection. [1]
- **Lessons for C (the most directly copyable recipe):**
  - Use phenomenon lists per family. Make the same item shape in many render styles and lengths.
  - Keep train, calibration and confirmation domains disjoint.
  - Use a very low learning rate and pick the checkpoint early.
  - Only about 51K examples were needed at 27B. Quality and breadth matter more than volume.

### Decider family (Mapika) [5]
- **decider-4b stage 1 (full fine-tune):**
  - 1.89M items, 742M tokens.
  - 60%: about 95 public datasets, agent trajectories, Mind2Web, teacher-written questions, and "Jev's input shapes".
  - 8%: 26 more public sets. These cover code defects, logs (HDFS, BGL), legal (LEDGAR, Unfair-ToS, CaseHOLD, SCOTUS, ECtHR), tables (TabFact, WikiTQ, FeTaQA, InfoTabs, TAT-QA), multilingual sets, MC-TACO, TRACIE, TimeQA, ProofWriter, RuleTaker and LogiQA 2.
  - 32%: 10 programmatic families with verifiable gold: code, dates and times, logs, long documents, plans, policies, probability, schedules, tables and tools.
  - Settings: lr 1e-5 cosine, 26,729 steps of 32,768 tokens.
- **decider-4b stage 2 (v2.1, LoRA r64/a128, lr 1e-4, 2 epochs):** 29,325 rows.
  - 8,000 generated rows with gold from the generating code.
  - 11,356 document questions written by Qwen3.5-27B, kept when 2+ independent answers agreed (89-91% kept).
  - 3,293 human-labelled public rows.
  - 6,676 replay rows trained with KL toward v1's distribution.
- **Measured deltas:**
  - v1 → v2 (hard labels everywhere): JevBench hard 0.550 → 0.676 (+12.6). Sampled bag-draw -18.7. Logits sharpened, so T rose to 1.935.
  - v2 → v2.1 (KL replay toward v1): sampled bag-draw +14.1; hard -2.7 (0.676 → 0.649). ECE on held-out generated families 0.046 → 0.147.
  - bf16 AdamW with no fp32 master copy beat fp32 master weights by 3.3 held-out points (0.791 vs 0.758).
  - Per-type temperatures (choice 1.110, yes/no 1.560, score 1.287): yes/no ECE 0.146 → 0.101; score ECE 0.140 → 0.108.
- **decider-12b v2:**
  - LoRA r32. 6,000 generated state-tracking decisions plus 4,000 replay rows. One epoch, lr 5e-5.
  - The state-tracking data are event logs from 7 invented domains, with rejected entries, VOID and CORRECTION entries, aliases and out-of-order exports.
  - They are rendered as logs, tables, prose and JSON. Gold comes from replaying the log; 101 of 104 blind checks agreed.
  - Fresh yes/no test (chance-corrected): 58.8 → 71.6. Held-out yes/no 38.7 → 57.1. JevBench hard 81 → 79 of 111.
  - Yes/no temperature 0.05, so only about 1% of answers fall in the 0.2-0.8 band.
- **Stated weaknesses:**
  - One pass cannot do multi-step arithmetic.
  - Rules written into the question are not followed at this size. On a form-filling probe, a one-sentence question scores 0.67 and a paragraph of rules scores 0.24.
  - Picking a record by position from a long JSON array is the weakest input shape (0.51 with 64 records vs 0.70 with one).
- **Lessons:**
  - Program-gold families are a third of a strong recipe.
  - State-tracking logs fix yes/no reasoning.
  - Train rule conventions into the data rather than relying on rule paragraphs in the question.
  - KL-anchored replay trades hard-tier accuracy and calibration for retention.

### Kev family (jaredpalmer) [7]
- **Base and method:** Qwen3.5-0.8B, 4B and 9B, each with a LoRA r16 (attention, MLP and DeltaNet) plus a pointer head. Kev-27B v2 is a full-weight SFT.
- **Data:**
  - decision-v7: 10,000 rows from 10 public datasets, 896 generated policy rows and 1,680 rows from 60 generated rule structures.
  - Later deltas: documents-v1 (real CFPB complaints), hard-v1, devtools-v1, and dates/unknowable data.
  - The 27B run used 65,667 synthetic records written and labelled by open models (a question is kept only if 2 blind labellers agree with the intended answer), plus about 58K tasksource rows.
- **Kev-4B results:**
  - hard-v1 test 0.540 → 0.803; devtools-v1 test 0.623 → 0.756.
  - JevBench public 0.758, hard 0.541.
  - Validated context is 8,192 (16k costs 3.4 pp).
- **Lessons ("What we have learned", numbered as in Kev's PLAN.md):**
  1. Real-document and skill data are the largest levers: +7 to +30 pp in distribution. Kev-4B also gained +9.0 pp on the JevBench hard tier.
  2. The cost of a skill delta grows with model size. It was free at 4B.
  3. More rows from the same generator have diminishing returns (+26 pp, then +5 pp).
  4. Replay stops helping at 9B.
  5. A temperature fitted on in-distribution rows does not transfer. Fit it on held-out datasets.
  7. Broad data carries the gains. Full weights instead of LoRA on the same data cost 3.0 pp on short states and 3.7 pp on scienthoon, and gained nothing.
  8. Knowledge is set by the base model.
  9. LoRA erodes date arithmetic. Stating the day count fixes it (0.65 → 1.00 at 4B).
  10. Continue training with soft targets only where labels are genuinely ambiguous. Soft targets beat hard ones there (Brier -0.011, accuracy +1.1). Softened MNLI targets cost 2.0 pp on WANLI.
  11. Burying a state in 1-4k tokens of filler cost 22-43 pp. Training recovered 17-20 pp of that, but moved real long documents by only ±1 pp.
  12. Seed noise is about ±1 pp on short sets and ±2 pp on long panels. A 1-point lead from one seed is noise.
  13. Negative results: calibration losses (label smoothing, CE + Brier, focal), question-side LoRA, checkpoint averaging, a reliability head, self-distillation, anchoring toward the base model's answers, and WiSE-FT. Option-permutation KL (`perm_kl`) and the ordinal-loss weight (`ord_w`) also did not help.
- **Lesson:** Kev is the most rigorous public log. Its findings 1, 3, 5, 7, 9, 10 and 11 map directly onto C.

### JPT-4B and JPT-9B (kirp) [6][1]
- **Base and method:** Qwen3.5-4B; LoRA r16 on all attention, DeltaNet and MLP projections.
- **Loss:** multi-class Brier over option labels, with Qwen's chat template and thinking disabled.
- **Data:** 49,221 questions in 32,835 records; one epoch over two option-shuffled copies.
  - Public sets: ContractNLI, MAUD, LegalBench, ConditionalQA, ShARC, TAT-QA, MultiHiertt, MuSiQue, BEIR, Mind2Web, AgentTraj and ToolACE.
  - Also 20 game environments, programmatic rule-arithmetic items, and 1,289 long policy, contract and regulation documents (4,471 questions) written by an LLM.
  - 8-gram overlap check against the evals.
- **Calibration:** one temperature, T = 1.036, fitted once on a held-out split.
- **Results:**
  - Best 4B on the Index (43.04). JevBench v1.4 public 0.879, hard 0.784.
  - JPT-9B is worse on the hard tier (0.730) despite lower training loss; the author has not found why.
- **Licence:** CC BY-NC 4.0 because of the training data.
- **Lessons:**
  - Legal, table and multi-hop sources plus long documents explain JPT's language-area lead.
  - Lower loss did not mean better hard-tier accuracy.
  - NC data makes the model unsellable. We must not repeat that.

### Jet v6.2 (michaljach) [9][1]
- **Base and method:** Qwen3.5-4B, rank-16 LoRA on a frozen bf16 backbone.
- **Data:**
  - Public partitions: relevance, entailment, stance, sarcasm, intent, commonsense, tool routing and tool-response preference.
  - Generators for arithmetic, Boolean rules and code behaviour.
  - An optional "jet-distill" set of Claude-invented questions.
- **v6.2 continuation:** 4,000 rows (800 BANKING77 train, 800 SEntFiN, 400 iSarcasm, 2,000 retention).
  - Two learning rates were tried (3e-6 and 8e-6). Step 250 of 1,000 at 3e-6 was picked, on 70% focus metrics + 30% retention.
- **Calibration:** temperatures per question type, not refitted for v6.2. Board ECE is 0.141, which is poor.
- **Results:** Index 42.60. Best small model on CLINC150 (0.911), When2Call (0.868) and cfcolor.
- **Lessons:**
  - Small focused continuations at a very low lr, with a retention guard, can add a skill.
  - Skipping recalibration shows on the board.

### lev (Interfaze) [8]
- **Base and method:** Qwen3.5-4B; LoRA r32 plus a candidate-path head for large option sets.
- **Data and training:** 200,000 examples from 29 sources (26 public HF datasets). 3 epochs; 18,750 steps of 32; about 7.8 h on an H100.
- **Readout:** single-token label codes, skipping codes that split into two tokens. Choice and binary yes/no are averaged over two option orders.
- **Calibration:** temperatures per question type, readout mode and option-count band, picked by leave-one-family-out ECE.
- **Results:** S1Bench macro 0.689 vs Jev 0.761 (13 subsets). Index 38.54. BANKING77 0.868 (> Jev).
- **Findings with numbers:**
  - **Yes/no polarity failure:**
    - On aegis2, lev scored 0.312, below any constant predictor.
    - Asking the same 120 states both ways ("unsafe?" vs "safe?") gave 0.308 vs 0.775.
    - mean(p_unsafe + p_safe) was 0.713, and 89 of 120 pairs differed by less than 0.10. The model was ignoring the question.
    - Cause: all yes/no supervision had yes = good (IMDB, Rotten Tomatoes).
    - Fix: add yes/no questions whose "yes" is the bad outcome. aegis2 then reached Jev (0.832), and later 0.864.
  - **PAWS:** paraphrase data (MRPC, QQP) taught a word-overlap shortcut. Word-swapped negatives raised PAWS 0.612 → 0.716.
  - **VitaminC did not move** despite FEVER training (0.751 → 0.738). It needs minimal-edit evidence pairs, where one number or date flips the verdict.
  - **Label-corruption bug:** a question cache keyed on sorted payloads gave 35-45% of shuffled choice rows the wrong target in the training loop. The files on disk were correct.
    - clinc_oos fell 0.865 → 0.055 and emotion fell to 0.605.
    - With the reader fixed: clinc_oos 0.976, emotion 0.860.
  - **Label codes:** skipping split codes lifted banking77 0.818 → 0.980. Using the chat-template prompt lifted the frozen model 0.653 → 0.710.
  - **Rating collapse:** fine-tuning cut summeval-consistency from 0.826 (frozen) to 0.271. The model learned to rate one level too low. The cause was rating-source label bias.
- **Lessons:**
  - Add yes/no polarity balance.
  - Add word-swap and minimal-edit pairs.
  - After shuffling, re-verify every training target exactly as the loader reads it.
  - Check the label distributions of rating data.

### JevK5 and Plumb-4B [13][2]
- **JevK5 v0.3:**
  - Base: Qwen3.5-4B, LoRA r16 on attention projections.
  - Teacher data: 17,408 questions. Qwen3.6-27B wrote 3,270. A large API model wrote 14,138, of which 94% matched independent answers.
  - Public replay: 30,052 rows from 26 datasets, train splits only.
  - One epoch over 47,460 rows; lr 3e-5; 2,048-token cap; letter CE.
  - Calibration: T 1.22 (ECE 0.050 → 0.035). Knockout readout for more than 16 options.
- **JevK5 results and weaknesses:**
  - JevBench v1.2 hard 0.784. v1.5.4 Intelligence 56.3, Calibration 88.3. Index 38.81.
  - 980 MMLU-Pro test items were trained on; the board counts them as wrong.
  - Dates and numbers are the weakest family (0.47). Score questions are weak (0.409).
- **Plumb-4B:**
  - Built on JevK5 v0.2 plus 5.15k hard decisions written and double-checked by a 27B model. Questions the model got wrong or was unsure of were weighted up.
  - Public hard 89/111 (80.2%) vs 82/111: 8 items fixed, 1 broken.
  - But v1.5.4 Intelligence is 55.8, no better than JevK5.
  - v5.2 adds a deterministic yes/no commit for v1.5 scoring: probabilities in 0.2-0.8 commit to the nearest boundary.
- **Lessons:**
  - Hard-example upweighting moves the public hard tier but not sealed accuracy.
  - Never judge C on public JevBench items.
  - Yes/no answers should commit; this matches our v1.5.4 note.

### Intern-Decision-4B (InternLM) [20][21][1]
- **Base and method:** Qwen3.5-4B, full fine-tune of the language backbone; the vision tower is frozen.
- **Readout:** a JSON skeleton with one `<decision>` placeholder per field. The logit just before each placeholder predicts that field. Training CE uses the full vocabulary.
- **Calibration:** T 1.992, fitted by NLL on 1,728 calibration cases.
- **Data:** not disclosed.
- **Results (own 7 suites):** average 90.02 vs Jev 88.74.
  - JevBench hard 73.87 vs Jev 72.07.
  - Typed Decision 80.55 vs 73.35.
  - ToolACE 96.45 vs 91.29.
  - Loses on WildJailBreak: 89.86 vs 96.29.
  - Index 37.81 (ECE 0.028).
- **Lesson:** own-suite wins of +1 to +7 do not show up on the broad Index. Jev stays strong on jailbreak detection.

### Eikos-4B and Eikos-27B (caiovicentino) [10][1]
- **Base and method:** Qwen3.5-4B and Qwen3.8-27B; LoRA r64, 1 epoch, lr 1e-4.
- **Loss:**
  - soft CE on option letters with option-order permutation;
  - an auxiliary rationale loss, weight 0.3;
  - Portuguese↔English view consistency (symmetric KL 0.5);
  - light JEPA losses (0.2).
  - The released 4B is a model soup of two recipes.
- **Data:**
  - Writer and teacher (GLM-5.3-Flash, blind) labels; an item is kept only if the teacher equals gold.
  - Programmatic items: probability, temporal, finance, trade, rules (including held-out new-domain rules), TAT-QA, GSM8K-train judging and FinEntity.
  - Long dossiers up to 64k tokens.
  - 8-gram decontamination against public JevBench items.
  - The held-out family, topic and language (Spanish) are never trained on.
- **Results:**
  - Eikos-4B public hard 72.1 vs Jev 73.0.
  - Error at ≥90% confidence: 2.4% vs Jev 5.9%.
  - With the decision hidden in 64k tokens: 74.2%.
  - Eikos-27B Index 53.13, with all FinEntity rows counted wrong because 979 test documents were in its training data.
- **Lessons:**
  - A rationale auxiliary loss and cross-view consistency are cheap.
  - Decontaminate by document as well as by item. Eikos lost a whole benchmark.

### Bosun v3.1 (Hanno Labs) [15][1]
- **Base and method:** Qwen3-1.7B; LoRA r16/a32 plus decision slots.
- **Data:** 130,000 rows; 3 epochs, epoch 2 picked on macro-family accuracy.
- **Results:** own DecisionBench 84.90% vs Jev 72.03%. The card itself says the eval is in-family. Index 20.10.
- **Lesson:** in-family benchmarks overstate quality by tens of points.

### Hopper (hopit-ai) [16]
- **Base and method:** Qwen3.5-4B LoRA r16.
- **Licence:** the 4B adapters are research-only because RACE was in the training data.
- **Calibration:** per-type temperatures (choice 0.790, yes/no 0.753, score 0.900). Tournament readout for more than 26 options.
- **Hopper 12B:** stage 2 continued with 5,000 replay rows. Document and rule decisions +16.1. Retention +0.8.
- **Stated weakness:** abstention and missing-information cases.
- **Results:** Index 40.77; v1.5.5 Intelligence 49.9.

### Jebadiah 27B [22]
- **Base and method:** Qwen3.8-27B, LoRA r16/a32. 15,813 questions; 1 epoch; lr 1e-4; 2,048-token cap.
- **Calibration:** per-type T (choice 1.23, yes/no 1.30, score 0.76). The score T was refitted on hard labels rather than on the smoothed training target.
- **Results:** public 0.866 (= Jev). Index 54.67 with ECE 0.014, the best on the board.
- **Lesson:** per-type temperatures fitted on hard labels give excellent calibration.

### imajev [23]
- **Data:** about 994K decisions in 3 stages.
  - About 500K human-labelled decisions from licence-checked public datasets.
  - 416K photo and text decisions.
  - About 23K hard questions, kept only where all three teachers agree.
- **Yes/no:** P(yes) plus half the "unknown" mass, described as "as in Jev".
- **Calibration:** T fitted on 150 template-generated JevBench-style items.
- **Results:** v1.4.2.2 composite #1 (67.37); v1.5.4 Intelligence 53.5.
- **Lesson:** licence-checked human-labelled public data at large scale is feasible.

---

## 4. What is public about how Jev was trained

| Claim | Source |
|---|---|
| "a new model architecture, parallel sampler for maximum efficiency, and training method we call Reinforcement Learning for Calibrated Decisions (RLCD)" | TypeSafe launch blog [24] |
| RLCD rewards stated probabilities that match outcomes ("answers given 90% probability should be right about 90% of the time"). The reward formula is unpublished. | [24][25][26] |
| "trained exclusively on synthetic data". "We made an early bet that we will be making all of our data". "Half of [our company] is a lab that basically owns this entire subfield of statistically well-understood synthetic data". | TechCrunch interview [27] |
| Data experts study "the cognitive core" to "find the jaggednesses, and then address them surgically". They avoid real-world and user data because of bias. Data targets "futuristic use cases". | Latent Space podcast [28] |
| "Jev is not trained on customer requests or responses"; "not fine-tuned or LoRA-adapted with customer data"; English is the primary language. | TypeSafe docs [29] |
| 64k tokens per request; 32k for state plus the longest question; up to 255 options; questions are evaluated independently. | [29][24] |
| "neither small nor an LLM". Outside observers suspect an open-weight LLM base. No paper, no weights, no public benchmark claims from TypeSafe. | [27][30] |
| The founder previously worked at OpenAI on ChatGPT and RLHF. | [27] |

Our inference, labelled as inference:
- Jev's one-pass knowledge scores are MMLU-Pro 0.827, GPQA 0.786 and BBH 0.929.
- The best open entrant up to 31B reaches MMLU-Pro 0.672 (Rune) and GPQA 0.505.
- So Jev's base is likely much stronger than any open 27-31B model. We cannot match that at 4B.
- What we can copy is the recipe idea: expert-written synthetic data aimed at measured weak spots, with a proper-scoring objective. Our Claude-authored, program-labelled families are exactly this.

Measured weak spots of Jev (from the boards), which are good targets for C:
- **SATA-Bench (select all that apply):** 0.264. 8 of 18 small models beat it.
- **PhishNChips:** 0.625.
- **ContractNLI:** 0.717.
- **BANKING77:** 0.797.
- **Home appliances (whole-case tool calls):** 0.523.
- **Calibration on Retrieval:** ECE 0.154.
- **Arts area:** 37.7.
- **Strong spots:** WildJailBreak 96.29, Tools 75.1, and knowledge. [1][21]

---

## 5. Cross-cutting lessons, with evidence

### A. Data breadth and domain-disjoint evaluation (our ejs-5 problem)
- **Broad data, not method, carried transfer.** On Kev's own corpus: Kev panel +9.1 pp, short states +2.9 pp. [7]
- **Same-generator saturation:** +26 pp from the first 6k rows, +5 pp from the next 12k. [7]
  - Cap rows per template. Prefer more templates and more families over more rows.
- **Domain-disjoint splits:**
  - pplx uses 12 train domains, 4 calibration domains and 4 confirmation domains. [14]
  - Kev keeps a whole held-out-dataset panel (breadth-v1) that is never trained on. [7]
- **Public-set wins do not transfer.**
  - Plumb: public hard +6.3 pp, but sealed-weighted Intelligence did not move. [13][2]
  - Winnow: ties Jev on public items, -16 pp on new families. [4]

### B. Contrastive and minimal-edit data
- **Winnow:** "Contrastive examples vary facts that should change an answer." It has the top JevBench Intelligence. [3]
- **lev, word-swap negatives:** PAWS +10.4 pp. [8]
- **lev, VitaminC:** no gain from FEVER-style data. It needs pairs where one number or date flips the verdict. [8]
- **lev and Jet:** the remaining failure mode is "inputs that differ by one swapped word or number". [8]

### C. Yes/no questions: polarity, negation, commitment
- **Polarity:** about half of yes/no training questions should have "yes" = the undesirable or negative outcome. Without this, the model learns a state prior and ignores the question. [8]
- **Probe for diagnosis:** ask each state both ways.
  - Healthy: mean(p_q + p_notq) ≈ 1.
  - Broken: |p_q − p_notq| is small (the question is ignored).
  - We can run this probe on C1's double-negation failures.
- **Negation-trained yes/no** lifted aegis2 from below chance to Jev level. [8]
- **State-tracking logs** (VOID, CORRECTION, aliases, out-of-order exports) lifted fresh yes/no from 58.8 to 71.6. [5]
- **Commitment:** JevBench v1.5 penalises soft yes/no answers.
  - Plumb commits probabilities in 0.2-0.8. decider-12b uses yes/no T 0.05 (only about 1% of answers fall in the band). [13][5]
  - Train yes/no on hard targets, except for truly ambiguous items.
- **Yes/no calibration differs from choice calibration.**
  - decider: yes/no T 1.56 vs choice 1.11. Hopper: 0.753 vs 0.790. Jebadiah: 1.30 vs 1.23. [5][16][22]

### D. Soft targets and teacher gating
- **Winnow:** teacher-distribution CE only when the teacher's top answer equals gold. [3]
- **Kev:** soft targets only where labellers genuinely disagree. Softening clean NLI labels hurt WANLI by 2.0 pp. [7]
- **Agreement filters everywhere:**
  - decider: kept items where 2+ answers agree (89-91% kept); its teacher agreed with only 72% of its own generic labels.
  - imajev: same answer under 2 option orders with p ≥ 0.6, or all 3 teachers agree.
  - Eikos and pplx: blind relabel must equal gold.
  - [5][23][10][14]
- **For us:**
  - Program gold needs no vote.
  - For Claude-authored items without program gold, use a second blind Claude labelling pass under a shuffled option order. Keep only exact agreement.
  - Keep human vote-share KD targets only on sources with real annotator splits.

### E. Replay and anchors
- **Replay is free at 4B and stops helping at 9B.** [7]
- **decider KL-to-v1 replay:** retention +14.1; hard tier -2.7; held-out ECE 0.046 → 0.147. [5]
- **Kev:** anchoring toward the base model's answers and WiSE-FT were negative. [7]
- **Hopper 12B:** 5,000 replay rows; retention +0.8 with documents and rules +16.1. [16]
- **Jet:** used a 30% retention term in checkpoint selection. [9]
- **For us:**
  - Keep the 60% replay.
  - Make the C1 anchor weak. Apply it only to replay rows, and skip rows where C1 is wrong against gold.
  - Read hard yes/no and sealed new-domain results before trusting any anchor weight.

### F. Hard-example mining
- **Plumb** upweighted wrong or unsure items: public hard +8/-1 items, sealed flat. [13]
- **Kev hard-v1 deltas:** large in-distribution gains, and +9.0 pp on JevBench hard at 4B. [7]
- **For us:** mine C1's errors per family to choose which families to write. Then write new items. Do not upweight the same items.

### G. Long documents
- **Buried filler is not a real document.** Burying a state cost 22-43 pp; training recovered 17-20 pp of that, but moved real documents by only ±1 pp. [7]
- **4B context ceiling:** Kev-4B validated context is 8,192 tokens (-3.4 pp at 16k). Kev-27B holds 64k (-2.4 pp). [7]
- **Long-document sources others used:**
  - JPT: 1,289 long policy, contract and regulation documents, 4,471 questions. [6]
  - Eikos: 64k dossiers, scoring 74.2% at 4B. [10]
  - Decision Index longest rows: 33,135 tokens. [1]
- **For us:**
  - Use real long public documents with commercial licences (for example CUAD, CC BY 4.0, used by Hopper and Kev).
  - Add Claude-written long cards whose answer is fixed by a program.
  - Train up to about 8k tokens. Report 16k separately.

### H. Rules, policies and state
- **Rules in the question are ignored at small size:** one sentence 0.67 vs a rule paragraph 0.24. [5]
  - Train many rule lengths and formats, so the model learns to apply written rules.
- **Real gains from rule and document data:**
  - Hopper 12B documents and rules +16.1. [16]
  - Kev documents +7 to +24 pp. [7]
  - Eikos holds out new-domain rule families for testing. [10]
- **Picking a record by position from a long JSON array is the weakest input shape** (0.51 at 64 records vs 0.70 at one). Add record-lookup families. [5]

### I. Dates, numbers and arithmetic
- **One pass cannot do multi-step arithmetic.** [5][6]
- **Dates and numbers are the weakest families:** JevK5 0.47; Kev deadline items 0.35 to 0.725 vs Jev 0.95. [13][7]
- **Stating the day count fixes the readout** (0.65 → 1.00). [7]
- **For us:** numeric and date items should need at most one comparison or one operation on stated values. Or give the computed value in the card. Do not train multi-step arithmetic in one pass.

### J. Options, tokens and readout
- **Single-token label codes.** Skipping split codes lifted banking77 0.818 → 0.980. [8]
- **Grouped or knockout reads** for more than 16-20 options. [18][13][16]
- **Train with large label sets too:** massive +4.5 pp. [8]
- **Reshuffle options every time a row is drawn.** pplx shuffles per batch; JPT used two shuffled copies; Eikos permutes order. We already do this. [14][6][10]
- **Average over two orders for choice and binary yes/no only.** Do not reverse ordered score scales. [8]
- **Use the chat-template prompt:** frozen 0.653 → 0.710. [8]
- **Two prompt layouts** (state-first and schema-first, 50/50) at decider. [5]

### K. Calibration
- **Fit one temperature per question type on held-out datasets or domains.**
  - Kev: in-distribution fit gave T 0.955 and breadth ECE 0.059. A held-out-dataset pool gave T 1.41-1.59 and ECE 0.0085-0.017. [7]
- **Calibration losses did not help:** label smoothing, CE + Brier and focal loss all failed against a matched CE control. [7]
  - JPT uses a Brier loss, but has no matched ablation. [6]
- **Fit temperature on hard labels, not smoothed targets.** Jebadiah's score temperature went 1.14 → 0.76. [22]

### L. Recipe numbers others used (4B unless noted)

| Model | Method | LR | Epochs | Rows | Seq cap | Picked at |
|---|---|---|---|---|---|---|
| JevK5 v0.3 | LoRA r16 (attn) | 3e-5 | 1 | 47,460 | 2,048 | end |
| Kev-4B | LoRA r16 + head | 5e-5 | 2 | ~12.6K + deltas | ≤384 (most rows) | registered rule |
| JPT-4B | LoRA r16 (all) | unknown (9B: 5e-5) | 1 over 2 shuffled copies | 49,221 Q | unknown | end |
| Eikos-4B | LoRA r64 | 1e-4 | 1 | unknown | 64k dossiers | soup of 2 recipes |
| decider-4b stage 2 | LoRA r64/a128 | 1e-4 | 2 | 29,325 | unknown | end |
| lev | LoRA r32 + head | unknown | 3 | 200,000 | ~128 tok per row (budget figure) | end |
| Jet v6.2 | LoRA r16 | 3e-6 | - | 4,000 | 16,384 | step 250 / 1,000 |
| pplx 27B | full FT | 2e-6 | 1 | 73,000 | 8,192 | 70% of epoch |
| Winnow 12B | LoRA r32/a64 | unknown | - | 26,000 (refine) | 8,192 | 19,200 seen |
| Bosun 1.7B | LoRA r16/a32 | unknown | 3 | 130,000 | unknown | epoch 2 |

Other recipe evidence:
- **bf16 AdamW without an fp32 master copy:** +3.3 held-out points at decider. [5]
- **LoRA vs full weights on the same data:** full weights gained nothing and cost 3.0-3.7 pp. [7]

### M. Hygiene
- **Licences:**
  - NC sources forced JPT to CC BY-NC. RACE forced Hopper's 4B adapters to research-only. lev's training sets include NC licences. [6][16][8]
  - Keep a per-row licence field and an allow-list.
- **Contamination:** the Index counts declared overlap as wrong.
  - reflex-4B was removed (65.8% on the 800 trained items vs 52.1% held-out).
  - open-jev trained on 9,542 MMLU-Pro test items (+31 pp gap).
  - Eikos had 979 FinEntity test documents in its training data. [1]
  - Screen with 8-grams, as Eikos and JPT do, and also screen by document, against every suite we report.
- **Verify the training reader:** lev's shuffle and cache bug silently corrupted 35-45% of shuffled targets. [8]
- **Noise:** a 1-point lead from one seed is noise. On 656 questions the 95% CI is about ±1.7 pp. [7]
  - Our ~2,000-item sealed suite needs paired bootstraps with record clusters.

---

## 6. Concrete recommendations for the C dataset and recipe

Each item is tied to the evidence above. None needs a bigger teacher, Jev outputs or NC data.

1. **Breadth first.**
   - For each of the ~12 skill families, write at least 15-25 distinct templates or "phenomena" (pplx style).
   - Cap each template at about 1-1.5k rows. Kev saw saturation after about 6k rows from one generator.
   - Spread the ~90K across at least 40 invented domains.
2. **Hold out domains, not just items.**
   - Split invented domains three ways: train, temperature-fit and confirmation.
   - The sealed new-domains suite must use domains and source datasets that appear in no split (pplx, Kev).
3. **Minimal-edit twins in every family.**
   - For each item, add a twin that changes one number, date, entity, quantifier or negation and flips the label.
   - Put both twins in train, with no twin pairs crossing splits (Winnow, lev).
4. **Yes/no polarity balance.**
   - Make about 50% of yes/no questions have yes = bad outcome.
   - Write each state both ways, as positive and negated questions, and add double negations.
   - Raise double negation from 0.34% to about 3-5% of yes/no rows.
   - Use lev's probe as a gate: mean(p_q + p_notq) close to 1 on dev (lev, decider).
5. **State-tracking family** in decider-12b style: event logs with VOID and CORRECTION entries, aliases and out-of-order rows. Render them as log, table, prose and JSON. Gold comes from replaying the log in code.
6. **Rule application with varied rule length** (1 sentence to a paragraph, and nested exceptions), plus record lookup in long JSON arrays (decider weak shapes).
7. **Numbers and dates:**
   - Each item needs at most one operation.
   - Give explicit day counts or computed intermediates when more is needed. Never ask for multi-step arithmetic (Kev, decider).
8. **Long documents:**
   - Use real commercial-licence documents (for example CUAD, CC BY 4.0) plus Claude-written long cards with program-fixed answers.
   - Do not rely on padding a short state with filler (Kev). Train up to about 8k tokens.
9. **Multi-select / exhaustive checks**, as a set of yes/no questions over one state. This is a measured Jev weak spot: SATA-Bench 0.264 [1].
10. **Format variety:**
    - 3+ instruction rewordings per family; criteria-style label definitions; 6 render styles; 3 length bands; option counts from 2 to 60+.
    - Use single-token labels only, and reshuffle options every draw (pplx, lev).
11. **Labels:**
    - Program gold where possible.
    - Otherwise, a second blind Claude pass with options shuffled; keep only exact agreement.
    - Use vote-share soft targets only on genuinely ambiguous human-annotated sources (Winnow, Kev). Never soften clean NLI or clean yes/no.
12. **Replay and anchor:**
    - Keep the 60% replay.
    - Use a small anchor KL toward C1, only on replay rows where C1 is right.
    - If step B's weight-softening wins, prefer it over a heavy anchor. Kev found anchoring and WiSE-FT negative at LoRA; decider found KL replay costs hard-tier accuracy.
13. **Training:**
    - Keep LoRA (Kev: full weights gained nothing).
    - Evaluate snapshots at about 25/50/75/100% of each round on the sealed suite. Others often won early (pplx at 70%, Jet at 25%, Bosun at epoch 2 of 3).
    - Optional cheap ablation if budget allows: bf16 AdamW without fp32 master (decider +3.3).
14. **Calibration:**
    - Refit per-type temperatures (choice, yes/no, score) on the temperature-fit domains, not on dev items of the training sources.
    - Keep the committed yes/no readout for JevBench v1.5 scoring.
15. **Hygiene gates before any training:**
    - Per-row licence allow-list.
    - 8-gram and document-level screens against JevBench public, ejs-5, the sealed suite, our dev gate and the Decision Index benchmarks.
    - A loader round-trip check: for every row, read the target back through the exact training reader after shuffling (lev's bug).
16. **Set expectations honestly.**
    - On knowledge-heavy and multi-step tasks, a 4B will stay 7-34 pp behind Jev.
    - Parity is realistic only on decision-skill benchmarks with strong families in C.
    - Judge C on the sealed new-domains suite, never on public JevBench.

---

## 7. Unknowns

- Training data for Rune, Intern-Decision, GLiDE, Winnow (private), AutoJev's exact 73K corpus, and Jev.
- The RLCD reward function and Jev's base model and size.
- Whether any competitor measured a commit-decision domain like ejs-5. We found none.
- JPT-4B's exact learning rate and full per-source row counts.
- Whether the board's "full FT" labels for Rune and Intern-Decision mean all weights or only the language backbone.

---

## Sources

1. Jev Decision Index 0.2.1 board, Hugging Face Space (`data/index.json`, `data/methodology.json`, generated 2026-09-28): https://huggingface.co/spaces/multimodalart/jev-decision-index
2. JevBench v1.5.4 official ranking (Benchmark Heaven): https://benchmarkheaven.com/jev-models/v1.5.4 and https://benchmarkheaven.com/jev-models
3. Winnow-12B model card: https://huggingface.co/EldanRing/Winnow-12B
4. Winnow-12B benchmark report: https://huggingface.co/EldanRing/Winnow-12B/blob/main/docs/BENCHMARKS.md
5. Decider (Mapika): https://github.com/Mapika/decider ; https://huggingface.co/Mapika/decider-4b ; https://huggingface.co/Mapika/decider-12b
6. JPT-4B / JPT-9B: https://huggingface.co/kirp/jpt-4b ; https://huggingface.co/kirp/jpt-9b
7. Kev (README, PLAN.md "What we have learned", AutoJev head-to-head): https://github.com/jaredpalmer/kev ; https://github.com/jaredpalmer/kev/blob/main/PLAN.md
8. lev (Interfaze) README and FINDINGS: https://github.com/InterfazeAI/lev ; https://github.com/InterfazeAI/lev/blob/main/docs/FINDINGS.md ; https://huggingface.co/interfaze-ai/lev
9. Jet v6.2: https://huggingface.co/michaljach/jet ; https://github.com/michaljach/jet
10. Eikos: https://github.com/caiovicentino/eikos
11. Surogate Rune 26B-A4B: https://huggingface.co/surogate/rune-26b-a4b-GGUF ; https://huggingface.co/michaelfeil/rune-26b-a4b
12. imajev report (label-agreement rules): https://mohit67890.github.io/imajev/report/
13. JevK5 and Plumb-4B: https://huggingface.co/alibiserikbay/JevK5 ; https://huggingface.co/crh225/plumb-4b
14. pplx-decider-v1-27b card and source (`source/configs/training.json`, `source/src/autojev/*.py`): https://huggingface.co/perplexity-ai/pplx-decider-v1-27b ; AutoJev-27B: https://huggingface.co/denis-pplx/autojev-27b
15. Bosun v3.1 1.7B: https://huggingface.co/Hanno-Labs/bosun-v3.1-1.7b
16. Hopper: https://github.com/hopit-ai/hopper
17. GLiDE (Fastino): https://fastino.ai/blog/introducing-glide-the-first-thinking-decision-model
18. Cygnet recipe and JevBench issue: https://github.com/blockbrain-ai/cygnet-recipe ; https://github.com/fstandhartinger/jevbench/issues/71
19. JevBench repo and sealed-vs-public analysis: https://github.com/fstandhartinger/jevbench ; https://stackness.dev/blog/how-do-you-benchmark-a-system-one-model-what-jevbench-scores-and-what-calibration-says-it-cannot
20. Intern-Decision repo: https://github.com/internlm/Intern-Decision
21. Intern-Decision-4B card: https://huggingface.co/internlm/Intern-Decision-4B
22. Jebadiah 27B: https://huggingface.co/frontier-infra/jebadiah-27b
23. imajev 1.0 report: https://mohit67890.github.io/imajev/report/
24. TypeSafe launch blog: https://typesafe.ai/blog/introducing-system-one-models-and-jev
25. OpenRouter "What is Jev": https://openrouter.ai/blog/insights/what-is-jev/
26. OrcaRouter "RLCD explained": https://www.orcarouter.ai/blog/rlcd-explained
27. TechCrunch, 18 Sep 2026: https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/
28. Latent Space podcast with Diogo Almeida: https://www.latent.space/p/jev
29. TypeSafe model docs: https://docs.typesafe.ai/models
30. flaviocopes "A deep dive into Jev": https://flaviocopes.com/jev/
