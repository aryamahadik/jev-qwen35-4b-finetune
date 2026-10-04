# RESEARCH: expert-question design for the C golden dataset

Angle: how to build expert-level, verifiable, program-labelled decision data with no label noise and no shortcuts. Output: a QC checklist (section 3) and a family-weighting method (section 4).

Scope: web research plus a read of our own allowed scripts (`decontam.py`, `flag_labels.py`, `FINETUNE_PLAN.md`). CPU only. No paid calls. No test splits opened. Written 3 Oct 2026.

---

## 0. Bottom line (read this first)

1. **Program labels are the right base.** In a 15-benchmark clean-up, programmatically generated logic sets had "few or no errors". Human-written sets had about 5% (GSM8K) and up to 30% (reading comprehension) bad items ([Platinum, arXiv 2502.03461](https://arxiv.org/abs/2502.03461)). LLM-written data is worse: only 54% of Self-Instruct rows were fully valid ([arXiv 2212.10560](https://arxiv.org/abs/2212.10560)).
2. **Program generators bring their own shortcuts.** BERT trained on one sampler of a logic task scored 99.9% in-distribution. On a second sampler of the same problem space it fell to 57.3% at depth 6 ([Zhang et al., arXiv 2205.11502](https://arxiv.org/abs/2205.11502)). Every family needs at least 2 samplers. One sampler must be held out as a test.
3. **One solver is not enough. Two solvers by the same author share bugs.** 27 independent human programs failed together far more often than chance ([Knight & Leveson 1986](https://dl.acm.org/doi/10.1109/TSE.1986.6312924)). AI coding agents behave the same way. Majority-of-3 cut mean failures from 387 to 131 per 1M tests, but did not remove them ([arXiv 2606.20158](https://arxiv.org/abs/2606.20158)). Most shared failures come from **ambiguous specs**. So: write the spec first, then use a second solver of a different kind, metamorphic tests, and a blind re-solve from the rendered text.
4. **Selecting items "because models fail" collects label errors.** Humanity's Last Exam kept only items that frontier models failed. FutureHouse found 29% ± 3.7% of its chem/bio answers conflict with the literature. The HLE team's own follow-up found about 18% ([FutureHouse](https://www.futurehouse.org/research/hle-exam)). AFLite-style filtering also oversamples low-agreement items ([Phang et al., arXiv 2111.08181](https://arxiv.org/abs/2111.08181)). Rule: any item that all our checkpoints get wrong must be re-derived before we keep it.
5. **LLM-written text carries strong artifacts.** On NLI data written by GPT-4, Llama-2 or Mistral, a hypothesis-only model scores 86-96% ([arXiv 2410.08996](https://arxiv.org/abs/2410.08996)). In 1,850 GPT-written MCQs, only 15-18% passed every item-writing check ([Arif et al., L@S 2024](https://public.websites.umich.edu/~kevynct/pubs/L_S_2024_WorkInProgress_Question_Generation_CRFinal2.pdf)). LLMs also skew the answer letter: Qwen favours B, and D is under-used ([arXiv 2605.01846](https://arxiv.org/html/2605.01846v1)). Claude-written surface text must pass partial-input baselines and a z-test.
6. **Breadth of distinct tasks beats rows per task.** Generalization to unseen tasks grows log-linearly with the number of training tasks, up to 757. It saturates at about 64 instances per task ([Super-NaturalInstructions, arXiv 2204.07705](https://arxiv.org/abs/2204.07705)). Below about 15 tasks, multi-task pre-finetuning hurts ([Muppet, arXiv 2101.11038](https://arxiv.org/abs/2101.11038)). Our ejs-5 loss (54.1 vs 58.5) fits a breadth problem, not a volume problem. **The ~90K rows should come from at least 700-1,400 distinct task specs (64-128 rows each), not from 12 big templates.**
7. **Format variety matters a lot.** Prompt format alone moved LLaMA-2-13B by up to 76 accuracy points ([Sclar et al., arXiv 2310.11324](https://arxiv.org/abs/2310.11324)). Mixed prompt settings gave 2%+ in FLAN ([arXiv 2301.13688](https://arxiv.org/abs/2301.13688)).
8. **Decontamination must go beyond n-grams.** A 13B model trained on rephrased MMLU test items rose from 54.8 to 85.9, and n-gram checks did not catch it ([Yang et al., arXiv 2311.04850](https://arxiv.org/abs/2311.04850)). LLM-generated sets can carry benchmark items: 12.8% of HumanEval overlapped CodeAlpaca. Our `decontam.py` checks only 10-gram overlap with JevBench public. That is not enough for C.
9. **Mixing methods rarely beat a well-capped uniform mix.** Aioli found that no published mixing method consistently beat stratified sampling ([arXiv 2411.05735](https://arxiv.org/abs/2411.05735)). Our own ledger agrees: in-family up-weighting did not transfer (A18, G2 in `FINETUNE_PLAN.md`). Use UniMax-style weights (uniform with an epoch cap) as the default. Allow one bounded, pre-registered update between round 1 and round 2 (section 4).
10. **Easy and medium items are worth keeping.** Training on easy data closed 70-100% of the gap to hard data. Hard data is noisier and costs more ([Hase et al., arXiv 2401.06751](https://arxiv.org/abs/2401.06751)). In s1, picking by difficulty alone or by diversity alone lost to picking by quality + difficulty + diversity together (AIME24 33.3 / 26.7 vs 50.0) ([arXiv 2501.19393](https://arxiv.org/abs/2501.19393)).

---

## 1. Evidence by topic (numbers and sources)

### 1.1 How noisy are labels in practice?

| Source | Error rate | Note |
|---|---|---|
| 10 common ML test sets ([Northcutt et al. 2021](https://arxiv.org/abs/2103.14749)) | 3.3% on average; 6% of ImageNet val (2,916) | Found with confident learning. 54% of the flagged candidates were confirmed by humans. |
| MMLU ([Gema et al., arXiv 2406.04127](https://arxiv.org/abs/2406.04127)) | 6.49% overall; 57% of sampled Virology | Errors changed model rankings. |
| Humanity's Last Exam chem/bio ([FutureHouse](https://www.futurehouse.org/research/hle-exam)) | 29% ± 3.7%; HLE team's own check about 18% | Cause: items kept only if frontier models failed. Experts were not required to verify answers that took more than 5 minutes. |
| GSM8K, SVAMP, reading comprehension ([Platinum, arXiv 2502.03461](https://arxiv.org/abs/2502.03461)) | GSM8K about 5%; reading comprehension up to 30% | About 75% of model "errors" on SVAMP were on bad items. Unanswerable SQuAD 2.0 items were often ambiguous or nonsensical. Logic sets had few or no errors because they were program-generated. |
| Self-Instruct (LLM-generated) ([arXiv 2212.10560](https://arxiv.org/abs/2212.10560)) | Output correct 58%; all fields valid 54% (200 sampled) | LLM labels are not gold. |
| Our own data (`FINETUNE_PLAN.md` risk 13) | 1.3-2.7% wrong; replay about 6% | Estimate only. |

What this means for us: program labels remove random noise. The remaining risk is **systematic** error: a rendering bug, an ambiguous word, or a wrong rule. Systematic errors are worse than random noise, because the model learns the wrong rule. So the QC targets generator bugs, not single rows.

### 1.2 Program-labelled generators: what works and what breaks

- **Works:** RuleTaker models scored 99% on held-out items and 95%+ on chains deeper than any seen in training. They transferred to paraphrased rulebases ([arXiv 2002.05867](https://arxiv.org/abs/2002.05867)). Note: these are one-pass classifiers with no chain-of-thought, like our readout.
- **Works at LLM scale:** Additional Logic Training on FLD×2 raised LLaMA-3.1-70B by up to 30 points on logic, up to 10 on math and code, and 5 on BBH, across 31 benchmarks ([Morishita et al., NeurIPS 2024, arXiv 2411.12498](https://arxiv.org/abs/2411.12498)). Their four design rules map straight onto our families:
  1. reason over **unknown facts**, so memory cannot answer (our "invented jargon defined in the card");
  2. use **diverse reasoning rules**;
  3. use **diverse wording**;
  4. add **hard distractors** (irrelevant facts and rules).
  Code: [hitachi-nlp/FLD](https://github.com/hitachi-nlp/FLD), Apache-2.0.
- **Breaks:** the sampler paradox. BERT trained on sampler RP scored 99.9 in-distribution but 57.3 on sampler LP at depth 6. Trained on LP, it scored 66.9 on RP at depth 1. Trained on both, it still fell to 55.2 on a slightly changed LP* ([arXiv 2205.11502](https://arxiv.org/abs/2205.11502)). Cause: labels correlated with simple statistics such as the number of rules.
- **Breaks:** irrelevant clauses. One added, seemingly relevant clause cut accuracy by up to 65% ([GSM-Symbolic, arXiv 2410.05229](https://arxiv.org/abs/2410.05229)). So "seemingly relevant but inert" sentences belong in training cards, with labels unchanged.
- **Reusable code:** Reasoning Gym has 100+ generators with verifiers, Apache-2.0 ([GitHub](https://github.com/open-thought/reasoning-gym), [arXiv 2505.24760](https://arxiv.org/abs/2505.24760)). It is useful for state tracking, logic and table puzzles, after we re-render the items as decision cards.

### 1.3 Independent re-derivation checks

- **N-version programming.** Knight & Leveson had 27 programmers implement one spec, tested on 1M inputs. There were 1,255 coincident failures, far above what independence predicts ([IEEE TSE 1986](https://dl.acm.org/doi/10.1109/TSE.1986.6312924)).
- **The same holds for AI agents.** Across 48 agent-written versions of the same spec, failures overlapped. Majority-of-3 cut the mean failure count from 387.44 to 130.99 per 1M tests. Shared failures came mostly from spec ambiguity ([arXiv 2606.20158](https://arxiv.org/abs/2606.20158)).
- **Metamorphic testing.** Define input changes with a known effect on the output (for example, shuffle the options and the label moves with them). This tests a program without knowing the true answer for each input. A survey covers 119 papers ([Segura et al., TSE 2016](https://eprints.whiterose.ac.uk/id/eprint/110335/1/segura16-tse.pdf)).
- **Execution feedback works for synthetic SFT data.** AutoIF cross-checks generated instructions against generated verifier code and unit tests, and uses rejection sampling ([arXiv 2406.13542](https://arxiv.org/abs/2406.13542)). Numbers: not read.

What this means for us. A label is accepted only if all of these agree:
1. the generator's constructive label;
2. a second solver of a **different paradigm** (brute force or SAT/z3 vs. forward rules; SQL vs. pandas; event replay vs. direct simulation);
3. that second solver run on a structure **parsed back from the rendered text**, which catches rendering bugs;
4. a blind re-solve by a separate Claude session that sees only the card, on a sample.

### 1.4 Artifact detection (shortcuts)

| Test | Evidence | Use for us |
|---|---|---|
| Hypothesis-only / partial-input baseline | 10 NLI sets. SNLI hypothesis-only scored 69% vs 34% majority ([Poliak et al. 2018](https://aclanthology.org/S18-2023/)) | Question-only, card-only and options-only baselines per family |
| Same, on LLM-written data | GPT-4 / Llama-2 / Mistral NLI: 86-96% hypothesis-only. "swimming in a pool" appeared in more than 10,000 GPT-4 contradictions ([arXiv 2410.08996](https://arxiv.org/abs/2410.08996)) | Claude-written text needs this test most |
| Choices-only (MCQ) | Beat the majority baseline in 11 of 12 cases (3 datasets × 4 LLMs), by up to 0.33 accuracy ([Balepur et al., ACL 2024](https://arxiv.org/abs/2402.12483)) | Options-only baseline on our letter tasks |
| A passing baseline proves little | A hypothesis-only model plus trivial premise patterns solved 15% of "hard" SNLI ([Feng et al. 2019](https://arxiv.org/abs/1905.05778)) | Also run a metadata-only baseline (section 3, G6d) |
| Feature z-test ("competency problems") | One-sided binomial test per feature. p0 = 1/(number of labels). α = 0.01 with Bonferroni over the vocabulary (28K on SNLI) ([Gardner et al., EMNLP 2021](https://aclanthology.org/2021.emnlp-main.135.pdf)) | Run per family on uni/bigrams and generator metadata |
| z-filtering | Generate data, then drop items that create high-z feature-label links. Trained models beat the originals on every debiased, OOD and adversarial test used ([Wu et al., ACL 2022](https://arxiv.org/abs/2203.12942)) | Fix the generator first. Use z-filtering second. |
| Heuristic-breaking sets (HANS) | MNLI models leaned on lexical overlap and failed when it pointed the wrong way ([McCoy et al., ACL 2019](https://arxiv.org/abs/1902.01007)) | Our hard yes/no (C1 47.4%, at or below chance) may be a learned heuristic that points the wrong way |
| Contrast sets | Small label-flipping edits lowered accuracy by up to 25% across 10 datasets ([Gardner et al. 2020](https://arxiv.org/abs/2004.02709)) | Every family gets minimal-edit twins |
| Pointwise V-information (PVI) | Finds artifacts by scoring transformed inputs, such as the hypothesis alone ([Ethayarajh et al., ICML 2022](https://arxiv.org/abs/2110.08420)) | Optional, using our own 4B |

Worked threshold (z-test, yes/no, p0 = 0.5, 50K features, α = 0.01/50K, z* = 5.07). A feature is a shortcut if it appears:
- 200 times with at least 67.9% one label;
- 1,000 times with at least 58.0% one label;
- 5,000 times with at least 53.6% one label.
(Computed locally with scipy.)

### 1.5 Adversarial filtering (AFLite) and what came after

- **AFLite.** Train many linear classifiers on frozen embeddings over random splits. Drop items whose label is predicted too often. SNLI settings: m = 64 partitions, t = 50K train size, k = 10K slice, τ = 0.75. Features came from RoBERTa fine-tuned on a 10% warm-up split that is never reused. The best SNLI model fell from 92% to 62%, and humans stayed high. Models trained on the filtered data matched or beat the full data out of distribution ([Le Bras et al., ICML 2020](https://arxiv.org/abs/2002.04108)). WinoGrande: about 44K problems; the AFLite-debiased subset has 12,282 (9,248 train) ([Sakaguchi et al., AAAI 2020](https://arxiv.org/abs/1907.10641)).
- **Dataset cartography.** For each item, track the mean confidence in the gold label and its variability across epochs. On WinoGrande (ID / WSC OOD):

  | Training set | ID | WSC OOD |
  |---|---|---|
  | 100% of data | 79.7 | 86.0 |
  | 33% random | 73.3 | 85.6 |
  | 33% AFLite | 76.8 | 86.6 |
  | 33% most ambiguous | 78.7 | 87.6 |

  The hard-to-learn region holds most mislabeled items ([Swayamdipta et al., EMNLP 2020](https://arxiv.org/abs/2009.10795)).
- **Caveats.**
  - Rankings after AFLite were unstable and depended on the adversary model.
  - Filtering oversampled low-agreement items and hurt the adversary model most ([Phang et al. 2021](https://arxiv.org/abs/2111.08181)).
  - For our training data, fix the generator when AFLite finds a cue. Do not just delete rows: deletion shifts the distribution, and it raises the share of ambiguous items.
- **IRT with an "artificial crowd".** Fit IRT difficulty from many models' answers. Machine-based difficulties correlated medium-to-large with human ones, and sampling training data by difficulty beat the baselines ([Lalor et al., EMNLP 2019](https://aclanthology.org/D19-1434/)). Our crowd: base Qwen3.5-4B, 2B, 4B-E, C1. All are ≤4B, so this is allowed.

### 1.6 Distractor and option design

- **Item-writing rules.** Haladyna, Downing & Rodriguez list 31 guidelines (14 on writing the choices). Key ones: make distractors plausible, keep options similar in length and grammar, avoid "all/none of the above", and do not cue the key ([Appl. Meas. Educ. 2002](https://eric.ed.gov/?id=EJ660246)).
- **Three good options beat more weak ones.** A meta-analysis of 80 years of research found 3 options optimal. People mostly guess between 2-3 plausible options anyway ([Rodriguez 2005](https://doi.org/10.1111/j.1745-3992.2005.00006.x)). For us: every distractor must be functional, meaning a specific error leads to it. Pad with filler only when the format needs many options (we train 2-20+).
- **LLM-written MCQ flaws** (1,850 rule-checked items; [Arif et al. 2024](https://public.websites.umich.edu/~kevynct/pubs/L_S_2024_WorkInProgress_Question_Generation_CRFinal2.pdf)). Share of items with each flaw:

  | Flaw | GPT-3.5 | GPT-4 |
  |---|---|---|
  | More than one correct option | 27% | 3% |
  | Implausible distractor | 24% | 17% |
  | Longest option is correct | 13% | 18% |
  | Passed every check | 15% | 18% |

- **Bias in generating the answer letter.** LLaMA favours A. Qwen3 and DeepSeek favour B. Gemini favours B/C. D is under-used by nearly every model. A "balance the letters" instruction helped but did not fix it ([arXiv 2605.01846](https://arxiv.org/html/2605.01846v1)). Fix: shuffle options in code after writing, never in the prompt.
- **Bias in selecting the answer letter.** 20 LLMs prefer some option IDs (token bias) ([Zheng et al., arXiv 2309.03882](https://arxiv.org/abs/2309.03882)). Our permutation relation loss already targets this. The data must still have uniform letter positions.
- **"Not enough information" (NEI) items.** SQuAD 2.0 added more than 50K unanswerable questions written to look like answerable ones. A strong system fell from 86 to 66 F1 ([arXiv 1806.03822](https://arxiv.org/abs/1806.03822)). But Platinum found many such human-written items ambiguous. Build NEI rows by **removing exactly one necessary premise from an answerable twin**, and have the program verify that neither answer follows.
- **Negation.**
  - CondaQA: 14,182 QA pairs, 200+ negation cues, and edits that paraphrase the negation, shift its scope, or make it affirmative. Best model consistency 42% vs human 81% ([arXiv 2211.00295](https://arxiv.org/abs/2211.00295)).
  - Negation in NLI benchmarks is rare and often does not matter to the label ([Hossain et al., EMNLP 2020](https://aclanthology.org/2020.emnlp-main.732/)).
  - Models fine-tuned on about 400K negation sentences still used surface cues that did not transfer ([García-Ferrero et al., EMNLP 2023](https://aclanthology.org/2023.emnlp-main.531/)).
  - "Negation Neglect": training on documents that call a claim false raised belief in the claim from 2.5% to 88.6%, when the negation sat in a separate sentence. Local negation was learned correctly ([arXiv 2605.13829](https://arxiv.org/abs/2605.13829)).
  - For us: keep negation local and label-critical. Build matched sets so the number of negations does not predict the label. Our golden_train has only 0.34% double-negation rows.

### 1.7 Difficulty calibration

- **Easy data:** easy-to-hard training recovered 70-100% of the supervision gap, for models up to 70B ([Hase et al.](https://arxiv.org/abs/2401.06751)).
- **Selection:** s1K, chosen by quality + difficulty + diversity, scored AIME24 50.0, MATH500 93.0, GPQA 57.6. Using only one criterion lost: random 36.7 / 90.6 / 52.0, diverse-only 26.7 / 91.2 / 54.6, longest-only 33.3 / 90.4 / 59.6 ([arXiv 2501.19393](https://arxiv.org/abs/2501.19393)). Note: s1 used teacher traces. We copy only the selection lesson.
- **Expert-question protocol (GPQA):** expert writer, then expert validator, then non-expert validator with the web. Experts scored 65% (74% after removing self-admitted mistakes). Non-experts scored 34% after 30+ minutes with the web. GPT-4 scored 39% ([arXiv 2311.12022](https://arxiv.org/abs/2311.12022)). Our version:
  - program writer = expert writer;
  - independent solvers = expert validator;
  - "weak solvers fail" (partial-input baselines and the base 4B without the card) = the non-expert check;
  - "Google-proof" = card-necessary: the answer must not be knowable without reading the card.
- **One-pass limit (inference).** Our readout has no chain-of-thought. Transformers learned implicit composition only after very long training, and failed on unseen compositions out of distribution. Comparison generalized ([Wang et al., NeurIPS 2024, arXiv 2405.15071](https://arxiv.org/abs/2405.15071)). That study is about facts stored in weights. With facts in context, RuleTaker reached depth 5. Practical rule: set each family's depth cap to the depth where C1 still learns. Measure it with a depth sweep in round 1. Do not fill the set with unlearnable items.

### 1.8 Diversity and the pitfalls of LLM-written data

- **Breadth beats depth:** see Super-NI and Muppet in section 0.6.
- **Format robustness:** up to 76 points of spread from format alone ([Sclar et al.](https://arxiv.org/abs/2310.11324)). Mixing formats in demonstrations reduced this ([MOF, NAACL SRW 2025](https://aclanthology.org/2025.naacl-srw.51/)).
- **Attribute-conditioned prompting:** prompts with sampled attributes (topic, style, length and so on) matched simple class prompts at 5% of the query cost. Simple prompts showed bias, for example regional bias ([AttrPrompt, NeurIPS 2023](https://arxiv.org/abs/2306.15895)).
- **Personas:** synthetic prompts are less diverse than human ones. Fine-grained personas added little over simply varying a length cutoff ([arXiv 2505.17390](https://arxiv.org/abs/2505.17390)).
- **Homogeneity:**
  - Recursive training on synthetic text lowers lexical, syntactic and semantic diversity ([Guo et al., NAACL Findings 2024](https://arxiv.org/abs/2311.09807)).
  - Synthetic data from several sources reduces distribution collapse ([Schaffelder & Gatt, ACL Findings 2026](https://aclanthology.org/2026.findings-acl.360.pdf)). We have one author (Claude), so diversity must come from programs, sampled attributes, real commercial-licence source text, and many separate sessions.
  - A measured diversity score correlated with SFT performance at 350M-1.4B ([arXiv 2410.15226](https://arxiv.org/abs/2410.15226)).
- **Subjective labels:** models trained on LLM-made data do worse as task subjectivity rises ([Li et al., EMNLP 2023](https://arxiv.org/abs/2310.07849)). Keep subjective decisions (moral norms and similar) on human vote-share sources. Never give them Claude labels.
- **Collapse:** replacing real data with synthetic data collapses models. Keeping the real data and adding synthetic data does not ([Gerstgrasser et al., arXiv 2404.01413](https://arxiv.org/abs/2404.01413)). Our 60% replay fits this.
- **Metrics to report:**
  - compression ratio, self-repetition of long n-grams, Self-BLEU, and BERTScore homogenization, from the `diversity` package, Apache-2.0 ([Shaib et al., arXiv 2403.00553](https://arxiv.org/abs/2403.00553));
  - Vendi score, the effective number of distinct items: exp of the entropy of the eigenvalues of K/n, MIT ([Friedman & Dieng](https://github.com/vertaix/Vendi-Score));
  - Self-Instruct's rule: add a new seed only if its ROUGE-L to every existing seed is below 0.7 ([arXiv 2212.10560](https://arxiv.org/abs/2212.10560)).

### 1.9 Deduplication and decontamination

- **Exact and near duplicates:**
  - Lee et al. used exact 50-token substrings plus MinHash on 5-grams, with 9,000 hashes (b = 20 bands, r = 450 rows). A pair counted as a duplicate when the MinHash match was confirmed by edit similarity above 0.8.
  - Results: 10x less memorized output, and 4% of standard validation sets overlapped train ([ACL 2022, arXiv 2107.06499](https://arxiv.org/abs/2107.06499)).
  - Tool: [datasketch](https://github.com/ekzhu/datasketch), MIT.
- **Semantic duplicates:** SemDeDup removed 50% of web data with minimal loss ([arXiv 2303.09540](https://arxiv.org/abs/2303.09540)).
- **Decontamination rules in use:**
  - GPT-3: any 13-gram overlap ([Brown et al. 2020, App. C](https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf)).
  - Tülu 3: an eval item is contaminated if more than 50% of its tokens fall in 8-grams shared with one training item. A training set is dropped if it overlaps more than 2% of an eval ([arXiv 2411.15124](https://arxiv.org/abs/2411.15124)).
- **Paraphrases slip through:**
  - Rephrased MMLU test items lifted Llama-2-13B from 54.8 to 85.9 and passed n-gram checks ([Yang et al.](https://arxiv.org/abs/2311.04850)).
  - On semantic contamination, n-gram and embedding methods reached F1 0.17-0.49, against 0.76 for a layered method (token → semantic → reasoning pattern → performance cliff) ([arXiv 2511.17602](https://arxiv.org/abs/2511.17602)).
- **Structural overlap:** in open-domain QA, 60-70% of test answers appeared in train, and about 30% of test questions had a near-paraphrase in train ([Lewis et al., arXiv 2008.02637](https://arxiv.org/abs/2008.02637)). For template data, the risk is the **same problem structure** with new names. So add a canonical structure hash.

### 1.10 Data-mixing laws (for choosing family weights)

| Method | Result | Fit for us |
|---|---|---|
| DoReMi ([arXiv 2305.10429](https://arxiv.org/abs/2305.10429)) | A 280M proxy with Group DRO on excess loss over a reference set weights for an 8B model: +6.5 points average few-shot accuracy, 2.6x fewer steps | The idea (weight by excess loss over a reference) carries over. A separate proxy run is too costly. |
| RegMix ([arXiv 2407.01492](https://arxiv.org/abs/2407.01492)) | 512 models of 1M parameters × 1B tokens; regression picks the mixture. Best of 64 at 1B. About 10% of DoReMi's compute. Interactions are often counter-intuitive. | Proxies need eval power we do not have (see 4.5) |
| Data mixing laws ([arXiv 2403.16952](https://arxiv.org/abs/2403.16952)) | Loss is a predictable function of the proportions (exponential form). 1B model on 100B tokens equal to default +48% steps. Also predicts the replay share that avoids forgetting. | Supports a fixed replay share |
| Aioli ([arXiv 2411.05735](https://arxiv.org/abs/2411.05735)) | No existing method consistently beat stratified sampling. Aioli beat it on 6/6 by 0.27 perplexity on average; others were up to 6.9 worse. | **Strong default: stratified/uniform** |
| UniMax ([arXiv 2304.09151](https://arxiv.org/abs/2304.09151)) | Uniform over groups, with a cap on repeats per group. Beat temperature sampling, and held at scale. | **Our default** |
| Temperature sampling ([mT5](https://ar5iv.labs.arxiv.org/html/2010.11934)) | p ∝ size^α with α = 0.3 | Fallback if unique sizes differ a lot |
| SFT composition ([Dong et al., ACL 2024, arXiv 2310.05492](https://arxiv.org/abs/2310.05492)) | Skills scale differently. Mixing helps at low data and conflicts at high data. | Watch for per-family conflicts |
| Skill-It ([arXiv 2307.14430](https://arxiv.org/abs/2307.14430)) | Skill ordering: +36.5 points on synthetic LEGO, −13.6% loss on Natural Instructions | Optional. Not proven for our case. |
| Data mixing optimisation for SFT ([ICML 2025, arXiv 2508.11953](https://arxiv.org/abs/2508.11953)) | Fits a scaling-law model from small mixtures. Within 0.66% per-domain loss of grid search. | Needs many small runs |
| Repetition ([Muennighoff et al., arXiv 2305.16264](https://arxiv.org/abs/2305.16264)) | Up to 4 epochs ≈ unique data (pretraining) | For template SFT data, cap at 2 epochs (Super-NI saturation) |

---

## 2. Gaps in our current pipeline (from allowed local files)

1. `decontam.py` drops rows that share any 10-word n-gram with **JevBench public only**. It does not cover:
   - the dev gate, the sealed new-domains suite, ejs-5, LongBench v2, OHS-1/2/3 and the Jev Decision Index tasks;
   - paraphrases, through embeddings;
   - structure, through a canonical problem hash.
2. `flag_labels.py` audits **4B-E teacher labels against gold**. For program-labelled C data, the label is the program's. A disagreement points to a generator bug or an ambiguous spec, so the same group-level rule applies: if 15 or more of 30 audited rows are wrong, fix the rule and regenerate (precedent D6).
3. Our plan already says "never drop rows automatically" and "in-family up-weighting did not transfer" (A18, G2). The method below keeps both rules: fix generators, not rows, and use a bounded near-uniform mix.
4. No partial-input, metadata-only, z-test or AFLite check exists yet for generated families. No diversity metrics are tracked.

---

## 3. QC checklist (gates every family must pass before training)

Each gate gives its pass rule, its tool, and its cost. "Family" means one of the ~12 skill families. "Spec" means one generator × domain pack × format group. All gates are CPU-only except G9 and G15.

**G0 Spec first (before any code)**
- Write a 1-page spec per generator, with a semantics table covering:
  - closed vs open world. This decides when "not enough information" is gold. ProofWriter-style data ships both versions.
  - the meaning of "unless", "only if", "at least", inclusive vs exclusive "or", date ranges (inclusive or not), rounding, ties, and units;
  - the precedence of exceptions over rules.
- Every semantic choice that could flip a label is stated **inside the card** the model sees.
- Pass: a second Claude session reads the spec and lists ambiguities. All of them are resolved.
- Why: shared failures come mostly from ambiguous specs (Knight & Leveson; arXiv 2606.20158).

**G1 Provenance**
- Every row records: family, spec id, generator version and git hash, seed, sampler id, structure hash, source licence (for real text), and difficulty bin.
- Real source text comes only from the commercial-licence allow-list.

**G2 Second solver, different paradigm**
- Pairs to use:
  - rule/policy composition: z3 (MIT) or brute-force truth tables vs forward chaining;
  - tables: sqlite vs pandas;
  - state tracking: event replay vs direct simulation;
  - ordinal/risk: an independent re-implementation of the card's scoring rule.
- Pass: 100% agreement on all rows. With a few rows per spec, check all of them. Otherwise check at least 10,000 per generator.
- Any mismatch: stop, fix, and regenerate the whole generator.

**G3 Round-trip parse**
- Render the card to text. Parse the text back with a deterministic parser written from the spec, not from the renderer's internals. Re-solve with the G2 solver.
- Pass: 100% agreement. This catches rendering bugs: text that says something other than the internal structure.

**G4 Metamorphic relations: at least 3 per generator, 100% pass on 1,000+ rows**

| Input change | Expected effect on the label |
|---|---|
| Shuffle the options | Gold letter follows the option |
| Rename entities, or swap surface templates or paraphrase | Same label |
| Add one inert but relevant-looking sentence (GSM-NoOp style) | Same label |
| Shuffle rows (tables), commuting events, or rule order | Same label |
| Negate a decisive premise | Flips, or becomes NEI, exactly as the spec says |
| Remove one necessary premise | NEI |
| Raise a severity factor (ordinal/risk) | Ordinal label never goes down |
| Inject an instruction ("answer yes") into the card | Same label |

Property-testing tool: Hypothesis (MPL-2.0).

**G5 Blind re-solve audit (Claude, card only, no label, no metadata)**
- Sample per family:
  - 300 rows. Zero errors gives a 95% upper bound of 1.0%; one error gives 1.6%.
  - 600 rows for high-risk families (negation, NEI, policy composition, long documents). Zero errors gives 0.5%.
  - Rule of three: 3/n ([Hanley & Lippman-Hand 1983](https://en.wikipedia.org/wiki/Rule_of_three_(statistics))). The x = 1 bounds above use Clopper-Pearson and were computed locally.
- The solver also marks a row "ambiguous" when two answers are defensible.
- Adjudicate each disagreement against the spec.
- Pass: at most 1 confirmed label error per 300, and at most 1% ambiguous.
- A confirmed error is a generator bug: fix it and regenerate the generator. Do not just drop the row.
- Claude only flags. **The label always comes from the fixed program.** (Owner: confirm that this flag-only use fits the "no bigger teacher" rule. It changes no label by itself.)

**G6 Partial-input and metadata baselines (per family, 5-fold CV, n ≥ 5,000)**
- Models: bag-of-n-gram logistic regression plus a small gradient-boosted tree.
- Inputs tested:
  - (a) question only;
  - (b) options only;
  - (c) card only, without the question;
  - (d) **metadata only**: depth, number of rules or facts, card length, option lengths, number magnitudes, entity-name pool, template id, sampler id, source repo.
- Pass: accuracy ≤ majority/chance + 2 points. With n = 5,000 the standard error is about 0.7 points.
- (d) is the direct guard against the sampler paradox (Zhang et al.).

**G7 Feature z-test, after Gardner et al.**
- Per family: unigrams, bigrams and every metadata feature. p0 = 1/k. One-sided α = 0.01 with Bonferroni over the number of features.
- Pass: no feature above the threshold (see the worked table in 1.4).
- If a feature fails, rebalance it by construction (matched twins). Use z-filtering only as a second step.

**G8 AFLite-lite**
- Embeddings: a frozen small encoder on CPU (all-MiniLM-L6-v2, Apache-2.0, 22M parameters) or mean-pooled base Qwen3.5-4B states.
- Settings: m = 64 partitions, linear classifiers, τ = 0.75.
- Report the share of each family predictable at τ.
- Pass: under 10%. If over, inspect the top items, find the cue, and fix the generator. Do not delete in bulk (Phang caveat).

**G9 Difficulty calibration, artificial crowd (paid GPU, an owner GO point)**
- Score every new row with base Qwen3.5-4B, 2B, 4B-E and C1 (one-pass readout), then fit a 2PL IRT model.
- Cost: about 90K rows × 4 models. At 16.6 ms per decision on H100 that is about 1.5 h, or $6-10 (long-document rows cost more).
- Bins per family: easy (all 4 models right, p > 0.9), medium, hard (at most 1 right).
- Targets: easy at most 20% (kept as anchors), medium at least 50%, hard at most 30%.
- **Every all-wrong row goes to G5 re-derivation before it is kept** (HLE lesson).
- Pass: difficulty does not predict the label. Chi-square of label × bin gives p > 0.01.

**G10 Balance**
- Yes rate 50% ± 1% per family × difficulty bin × template.
- Gold letter position uniform per family and option-count bucket (chi-square p > 0.01).
- "Longest option is correct" rate within ±2 points of 1/k.
- **Special options** ("not enough information", "none of these") appear as **wrong** answers in at least 50% of the rows that show them. Otherwise their presence is a cue.
- "Attack present" is uncorrelated with the label.
- Options are shuffled in code after writing, never by the LLM.

**G11 Diversity**
Per family:
- at least 60 specs in round 1 (at most 128 rows per spec, about 83 on average);
- no single surface template above 2% of rows;
- at least 30 domain packs;
- at least 5 instruction formats, 3 label-definition styles, and option counts spread over 2-4 / 5-9 / 10-19 / 20+;
- every Claude-written seed has ROUGE-L below 0.7 to all other seeds;
- report compression ratio, Self-BLEU and Vendi score. Each must be no worse than the same family's slice in golden_train.

For prose, sample attributes in code (domain, role, document type, register, locale, length cutoff), as AttrPrompt does. Use many separate Claude sessions, not one long one.

**G12 Deduplication**
- Exact: hash the normalized text. Zero duplicates allowed.
- Near: MinHash on 5-grams with Jaccard ≥ 0.8, confirmed by edit similarity ≥ 0.8. Keep one.
- Structure: a canonical hash of the problem (rule graph + facts + query, with names abstracted). At most one surface form per structure, except planned twins and format variants.
- Semantic: embedding cosine. Set the threshold by hand-checking 100 pairs at 0.85 / 0.90 / 0.95.

**G13 Decontamination, run blind**
- Compare against every eval: dev gate, sealed suite, JevBench public, ejs-5, LongBench v2, OHS-1/2/3, and the Jev Decision Index tasks.
- Rules:
  - any 13-gram overlap;
  - the Tülu-3 8-gram rule (more than 50% of an eval item's tokens covered);
  - embedding top-5 above the G12 threshold;
  - a structure-hash match;
  - a domain keyword block-list for the sealed suite's domains.
- The script runs in a sealed process and **prints only train ids to drop and counts**. No agent sees test text. (Owner: approve this blind mode for test splits. Our rules forbid opening them.)
- Extra risk: Claude may recall benchmark items, as with CodeAlpaca vs HumanEval at 12.8%. So decontaminate every Claude-written seed, not only the final rows.

**G14 Sealed-suite separation**
- Build the sealed new-domains suite **before** generating training data, with separate generator code and separate templates.
- Freeze its domain list. Never use it to choose weights; use the mix-tuning dev in section 4 for that.
- The family-weighting step never reads the sealed suite.

**G15 Post-round-1 cartography (uses training logs, about $0 extra)**
- Log per-row gold probability at 4-6 checkpoints during round 1.
- Rows with low confidence and low variability are the "hard-to-learn" region, where mislabeled rows collect (Swayamdipta). Audit 30 per family from that region with G5.
- If 15 or more of 30 are wrong, fix the generator before round 2.

Family-specific notes, by key risk:

| Family | Second solver (G2) | Key twin / metamorphic relation | Main shortcut to block |
|---|---|---|---|
| Indirect-evidence yes/no | Brute-force entailment over the parsed facts | Break one hop: "no" or NEI, per spec | Lexical overlap with the question (HANS) |
| Rule/policy composition | z3 vs forward chaining | Swap rule order; add an inert rule; exception precedence stated in the card | Number of rules, or exception words, predicting the label (Zhang) |
| State tracking | Event replay vs direct simulation | Insert no-op events; reorder commuting events | Last-event recency |
| Ordinal judgment | Independent rubric code | Adjacent-level distractors; monotonicity | Extreme words ("severe") mapping straight to the top level |
| Risk prediction (card-defined scoring) | Independent scorer | Drop one factor: label shifts as computed | Count of risk words |
| Table/fact reasoning | sqlite vs pandas | Row shuffle; column rename | Answer in the first row; number magnitude |
| Close distractors | Solver checks that exactly one option is valid | Options differ on one attribute; position of the decisive attribute uniform | Longest or most specific option |
| Invented jargon in the card | Definition-substitution solver | Swap definitions: label follows (our defswap) | Morphology hints ("-phobia" = bad). Check invented words against a dictionary. |
| Hard/negated yes/no | Logic solver on the parsed polarity | Quadruple: affirmative, negated, double-negated, scope-shifted. p(label given number of negations) = 0.5. 200+ cue types, including implicit ("fail to", "lack", "refuse"). | Counting negation words (parity) |
| Not enough information | OWA solver proves neither answer | Built from an answerable twin by removing one premise | NEI option shown only when NEI is correct (G10) |
| Attack-resistant variants | The clean twin's solver | Inject an instruction: same label | "Attacked" predicting "no" |
| Long documents | Solver on the evidence span | Evidence position uniform across deciles; remove the evidence: NEI; same-domain distractor documents | Evidence near the start or end; document length |
| Commit decisions (other repos) | Human gold from repo history | Time-based split; strip hash, author and date | Repo id, author, file path (metadata-only baseline); cap each repo at 5% of the family |

---

## 4. Family-weighting method

Goal: pick how many of the new rows (about 40% of each round) each family gets, in a way that carries over to **unseen domains**.

### 4.1 Unit of weighting
- Weight **families**. Inside a family, weight specs equally.
- Cap each spec at 128 rows in round 1. Super-NI saturates at 64 per task; we allow up to 2x because soft targets and twins add value. Raise the cap to 256 only if the spec count runs out.
- Minimum specs per family = family rows / 128. Example: 5,000 rows needs at least 40 specs. G11 asks for 60, which is about 83 rows per spec.

### 4.2 Round 1 prior: UniMax (default, no tuning)
- Start with w_f = 1/K for K families.
- Cap each family at E_max × U_f rows, where U_f is its unique rows after G12. E_max = 1 in round 1, and at most 2 over both rounds.
- Give any overflow equally to the uncapped families.
- Add a token cap: long documents take at most a fixed share of new **tokens**. Set this from the budget, because steps are bounded by micro_tokens.
- Worked example, round 1. 150K rows × 40% = 60K new rows. K = 12, so 5,000 per family and 60 specs each (G11), about 720 specs in total. With 90K unique rows overall, E_max = 1 holds.

### 4.3 Optional bounded headroom tilt (round 1; default off)
DoReMi-style "excess loss vs reference", using C1 as the reference:
- Headroom h_f = max(0, C1 error on the family's far-domain probe − floor_f). The floor is the audited ambiguity plus label-error rate, about 1%.
- New weight w_f ∝ (1/K) · (h_f / mean h)^β. Clip to [0.5/K, 2/K]. Renormalize.
- Default β = 0, which is pure uniform, because of local evidence A18 and G2. Use β = 0.5 only if the probe is truly far-domain (not in-family dev). Pre-register the choice.

### 4.4 One bounded update before round 2 (pre-registered before round 1 results exist)
- Measure, paired against C1:
  - Δ_f on each family's far-domain probe (n ≥ 400 per family);
  - the overall change on a **mix-tuning dev** (n ≥ 2,000). It is new-domain but separate from the sealed suite.
- Update rule (multiplicative, bounded, like the exponentiated-gradient step in DoReMi and Aioli):
  - Δ_f significantly > 0 (paired p < 0.05) and h_f still > 3 points: weight × 1.5.
  - Δ_f ≤ 0, or h_f < 1 point (saturated): weight × 0.67.
  - Otherwise: × 1.
  - Floor every family at 0.5/K to protect against forgetting. Renormalize.
- If the overall mix-tuning-dev change is negative, freeze the weights and look for a data bug (G15) before round 2.
- Round 2 (300K × 40% = 120K new rows) gets **new specs**, not more repeats. Keep E_max ≤ 2 overall.

### 4.5 Why not RegMix or DoReMi proxies here (power check)
- Paired accuracy difference: SE ≈ √(d/n), where d is the share of items on which the two runs disagree.
  - n = 400, d = 15%: SE 1.94, so the minimum detectable effect is about 3.8 points.
  - n = 2,000, d = 10%: SE 0.71, so the minimum detectable effect is about 1.4 points.
- Mixture effects inside a 40% slice of fine-tuning data are likely around 1 point or less. Aioli found that most methods do not beat stratified sampling.
- Six to eight proxy runs at about $1.6 each (500 steps × 2.72 s on H100) would cost about $13 plus eval, and still could not separate the mixtures.
- **Advice: skip proxies. Spend the money on more specs and on G9.**
- Revisit only if a family probe shows a gap of 4 points or more.

### 4.6 Within-family weights
- Difficulty mix from G9: easy ≤ 20%, medium ≥ 50%, hard ≤ 30%.
- Labels balanced (G10).
- Format groups equal.
- Depth capped at the depth where the round-1 depth sweep still shows learning (1.7).

---

## 5. Owner decisions needed

1. **Blind decontamination** (G13): a sealed script reads the test splits and prints only drop ids and counts. Is this allowed under "never open test splits"? If not, we can only decontaminate against what we may read, and must say so in claims.
2. **Claude as a flag-only blind solver** (G5): it never sets labels. Confirm this fits the no-bigger-teacher rule.
3. **G9 artificial-crowd scoring**: about $6-10 of H100 time. This is a paid GPU step, so it is a GO point.
4. **β for the round-1 tilt** (4.3): default 0, pure uniform.
5. **The mix-tuning dev set** (about 2,000 items, new domains, separate from the sealed suite): build it now so weights are never tuned on the sealed suite.

---

## 6. Unknowns
- Exact gains for z-filtering, AutoIF and PVI: not read in full here. The direction is reported above.
- How much our one-pass readout gains from deeper program-generated reasoning (FLD-style) without chain-of-thought: unknown. Measure with the round-1 depth sweep.
- Licences: CondaQA, and the FLD dataset files as opposed to the FLD code (Apache-2.0): not checked.

## 7. Tool licences (checked on GitHub / Hugging Face, 3 Oct 2026)

| Tool | Licence |
|---|---|
| datasketch | MIT |
| cleanlab | Apache-2.0 |
| diversity (Shaib) | Apache-2.0 |
| Vendi-Score | MIT |
| z3 | MIT |
| Hypothesis | MPL-2.0 |
| reasoning-gym | Apache-2.0 |
| FLD code | Apache-2.0 |
| all-MiniLM-L6-v2 | Apache-2.0 |
