# C2.1 PUBLIC TRAIN-SPLIT INVENTORY (synthesis of research_v4)

Author: Opus 5.5 synthesis subagent. Date: Sun 18 Oct 2026.
Inputs read in full: research_v4/CRITIC.md, decision_index.md, nlu.md, code.md, safety.md, tools.md, hardest.md (refuter-
corrected rows only), training_inputs/PLAN_TRAINING_SIDE.md (v3.1), l0/G13_TARGET_REGISTRY_DRAFT.md,
l0/R5_CANDIDATES_CHECK.md. Not opened: any "ohs"/"sealed" path, any Jev output, ~/.claude, any dataset item.
No download, no model run, no model API. One extra web check today (BANKING77, below).

Citation rule used here. Every licence quote and provenance claim is copied from the refuter-corrected row of the named
research_v4 file, where the researcher fetched the URL on 18 Oct 2026; the URL is repeated here with that date. "UNVERIFIED"
is kept wherever the research file kept it. Numbers marked DERIVED are my arithmetic on plan figures, not measurements.

Merge rule (critic H1): when two research files disagree on a dataset, the STRICTER verdict is used here until Opus rules.
Resolved conflicts are listed in section 5, item H1.

New check today (18 Oct 2026): https://ar5iv.labs.arxiv.org/html/2003.04807 (BANKING77 paper). The page says only "The new
banking77 dataset comprises 13,083 customer service queries labeled with 77 intents" and does not say who wrote or labelled
the queries. BANKING77 therefore stays OWNER (tools.md row 82 verdict kept; decision_index.md row 6 and nlu.md F1 overruled).

---

## 0. Short version (owner)

1. ALLOW-R5 after the strictest merge: **41 datasets or generators**. 19 are clean now (tier A); 7 are clean but their test
   or dev split is a benchmark we read (Decision Index 0.3 or Nimble), so they need ONE owner ruling on split-scoped release
   (tier B2); 15 need a mechanical check before use (tier C: read a licence file, filter rows by repo licence, drop fields).
2. OWNER table: **13 lines**, each with a recommended default (section 2). The most important are line O1 (split-scoped
   release, unlocks 8 sets), O2 (CC BY-SA, about 20 sets, default NO) and O5 (When2Call / WildGuardMix train, default NO).
3. DENY: about 365 named datasets across the six files, not de-duplicated (section 3), grouped by reason. The barred A61(a) sources (gsm8k,
   hover, isarcasmeval, tydiqa, md_fdc, md_peps, md_worldbank, md_usgs, md_cma) and everything derived from them are DENY
   under any id or form.
4. The big public tool-calling and agent-safety training corpora are all LLM-made, so T50/T51/T53/T41c/T54/T55/T56 stay
   Claude-authored generators with program gold. Public data mostly helps the GENERAL score (intent, evidence, abstain,
   commonsense) and gives realism slices to P1 code families.
5. Rows (DERIVED): about 12K block-R rows plus 5K P1 code realism rows plus about 4K from new P0 families. With C2 as init
   and replay held at 38K, the mix is about 99.5K rows and $23.6-29.4: it fits the 100K / $30 cap, with almost no room
   left. With C1 as init (replay 57K) it does NOT fit without an owner or Opus change (section 6).
6. About 80% of the Jev Decision Index is private, and the AA index has no usable train split under our rules. No public
   train split can "cover" those parts. Abstain behaviour and calibration are the only levers there (section 5, E2).

---

## 1. ALLOW-R5 list (train split only)

What ALLOW-R5 means here: the strictest refuter-corrected verdict is ALLOW-R5. It is still only "not barred". Before any
mapper, every row below also needs: a manifest-v2 name (one record per dataset, never a catalogue); the A61(b) split-aware
record; a pre-mapper 8.5 PASS; guards F1-F10; full-row G13 against the whole registry, including the registry additions in
section 5 B1 (not a 200-row sample, see B3); the A46-style drop-only noise screen (A5); and a "seen in training" flag on
every report row that touches the dataset (B5).

Conversion rule for all rows (critic A1c, A6): recast the dataset's OWN label into C2's rendered Choice or yes/no layout,
shuffle the options and add the 20% permutation copies (plan section 5). For large label sets, show the gold plus k-1 hard
distractor labels picked by program (nearest label names, or the train-set confusion matrix), with k in {4, 8} rotating.
For multi-label sets, ask one yes/no question per option. For long documents, a program selects the gold-bearing span plus
distractor spans; text is never cut in a way that drops the evidence (E5). No LLM writes or labels any block-R row. Claude
writes only the benign twins named in the safety rows and the hard extensions in section 4.

Legend for "B2": YES = the dataset's test/dev split is a benchmark we read or report (DI 0.3 / Nimble). It is blocked until
the owner answers O1 = YES. If the owner does not answer, it is excluded.

### 1A. Tier A: clean now (19)

| # | Dataset (exact release) | Train split, size | Licence (quote; URL; fetched 18 Oct 2026) | Label provenance | Feeds | Becomes (own labels) | Never touch |
|---|---|---|---|---|---|---|---|
| A1 | HWU64 (upstream xliuhw/NLU-Evaluation-Data, not the DeepPavlov mirror) | train portion, 8,954 (mirror count) | "All data are released under the Creative Commons Attribution 4.0 International License (CC BY 4.0)" https://github.com/xliuhw/NLU-Evaluation-Data (nlu.md F4) | MTurk workers typed answers to written prompts; no machine text (arXiv 1903.05566) | general: intent routing; T54 tool pick analogue | pick-one intent among k program-chosen confusable intents | its test folds |
| A2 | SNIPS NLU 2017-06-custom-intent-engines only | train per intent (size UNVERIFIED) | repo LICENSE "CC0 1.0 Universal" https://github.com/snipsco/nlu-benchmark (tools.md row 83) | "generated for each intent with crowdsourcing methods" (folder README); 2016-12 and 2018-01 folders excluded (provenance UNVERIFIED) | general intent; T54 sequence (our own grammar rebuild, API-BLEND idea) | pick-one intent; slot "which value fills X" | its validation files |
| A3 | ABCD (asappresearch) | train of >10K dialogues | "MIT License / Copyright (c) 2021 ASAPP Research" https://github.com/asappresearch/abcd (tools.md row 85); MIT covers data by implication only | human-human (MTurk customers, certified agents); flow labels program-derived | G4 next step; T59 ask-or-proceed; T60 control-next | per-turn pick-one: take_action / retrieve_utterance / end_conversation; which of 30 actions | dev, test |
| A4 | MultiWOZ 2.2 corrections | train (10,438 dialogues total) | "released ... under the MIT License" https://github.com/budzianowski/multiwoz (tools.md row 86; LICENSE text not shown) | human-human Wizard-of-Oz; system acts hand-annotated (use these only; user acts are heuristic) | T59 ask missing slot vs act | yes/no "a required slot is missing, so ask" from system acts | dev 1k, test 1k |
| A5 | Taskmaster TM-1, TM-2, TM-3 (TM-4 excluded) | train where a split file exists (split UNVERIFIED) | "made available under the Creative Commons Attribution 4.0 License" (each folder README) https://github.com/google-research-datasets/Taskmaster (tools.md row 88) | crowd Wizard-of-Oz and self-dialogs | T59, low | ask vs act from annotated turns | any dev/test file; if none, our own frozen 10% hold-out is never trained |
| A6 | SciFact | claims_train.jsonl (about 809 claims) | "Claims: CC BY 4.0 ... Abstracts: Open Data Commons Attribution License 1.0 ... Code: Apache License 2.0" https://raw.githubusercontent.com/allenai/scifact/master/LICENSE.md (nlu.md A11) | expert-written claims; no LM text (arXiv 2004.14974) | G8 claim vs evidence (T56 analogue); abstain head | SUPPORTS / REFUTES / NOT ENOUGH INFO pick-one | dev (benchmark), test |
| A7 | Qasper | train 888 papers / 2,593 questions | "[CC BY 4.0]" https://huggingface.co/datasets/allenai/qasper (nlu.md B13); papers limited to CC-BY arXiv papers | NLP practitioners; no model text | abstain head; evidence yes/no | yes / no / unanswerable; program span selection | dev, test |
| A8 | CommonsenseQA (original release, not the Google-snippet variant) | train 9,741 | maintainer: "Our dataset is licensed under an MIT license." https://github.com/jonathanherzig/commonsenseqa/issues/5 (nlu.md C7) | crowd questions; one ConceptNet distractor, one worker-written | general reasoning | 5-way pick-one | dev (standard benchmark), test |
| A9 | ETHICS, MTurk subsets only (justice, deontology, virtue, utilitarianism, SHORT commonsense) | train: 18,164 / 21,791 / 28,245 / 13,737 / short part of 13,910 | card "license: mit" https://huggingface.co/datasets/hendrycks/ethics (nlu.md F16) | MTurk-written; long commonsense rows are Reddit AITA and are EXCLUDED | G1 policy/norm judgement analogue | allowed / not allowed yes/no; utilitarian pair pick-one | test, hard test |
| A10 | BoardgameQA | train file | paper footnote "License: CC BY" https://ar5iv.labs.arxiv.org/html/2306.07934; mirror "cc-by-4.0" https://huggingface.co/datasets/tasksource/Boardgame-QA (decision_index.md E7) | programmatic (backward story generation, manual templates, defeasible solver); no LLM | general: reasoning with conflicting rules (hardest.md 1.11 target 2) | proved / disproved / unknown | dev, test |
| A11 | bAbI tasks generator (code only; fresh rows) | generated on demand | "BSD License / For bAbI tasks software" https://raw.githubusercontent.com/facebookarchive/bAbI-tasks/master/LICENSE.md (nlu.md C25) | program | general, low | pick-one answer; fresh seeds only | the published bAbI test files |
| A12 | Reasoning Gym generators, per-task allow-list | procedural | "Apache License / Version 2.0" https://raw.githubusercontent.com/open-thought/reasoning-gym/main/LICENSE (nlu.md C26; hardest.md row 58) | program generators with verifiers | general block (inside the 7K, section 6) | pick-one / yes-no with difficulty by program parameter | EXCLUDE gsm_symbolic (gsm8k, A61(a)), codeio ("transformed by an LLM"); review rush_hour, arc_1d, knights_knaves; exclude any task wrapping a public benchmark |
| A13 | DeepMind Mathematics generator (regenerate; not the HF mirror) | 2M per module if pre-generated | "Apache License / Version 2.0" https://raw.githubusercontent.com/google-deepmind/mathematics_dataset/master/LICENSE (nlu.md D2) | program-generated exact answers | general block | pick-one among program-made near-miss answers | interpolation/extrapolation test files |
| A14 | Juliet Test Suite 1.3 (C/C++; Java/C# same terms) | whole suite (64,099 C/C++ cases), no split | "not subject to copyright protection and is in the public domain"; foreign rights "CC0 1.0 Public Domain License" https://samate.nist.gov/SARD/test-suites/112 (code.md row 80; decision_index.md E11) | synthetic good/bad functions by CWE (NSA CAS) | T65 VULN-SYNTH (P1) | "is this function the vulnerable variant?" yes/no; which CWE class pick-one | guard F2 (no CVE ids); our own frozen hold-out by CWE family |
| A15 | LogChunks | 797 Travis CI logs, 80 repos | "Creative Commons Attribution 4.0 International" https://zenodo.org/records/3632351 (code.md row 76) | human-labelled failure chunk, validated with developers | T62 FLAKY-OR-REAL; G6 CI-log triage | "which chunk explains the failure" pick-one; failure category | our own hold-out by repo |
| A16 | DataDog malicious-software-packages-dataset (labels, manifests, metadata ONLY) | 29,847 packages | "This dataset is released under the Apache-2.0 license." https://github.com/DataDog/malicious-software-packages-dataset (code.md row 79); payload code keeps its original licence, never used | "manually triaged by a human" (publisher claim) | T63 DEP-RISK (P1) | malicious yes/no from manifest features; benign negatives must come from our seeded namespace | never open or execute payload ZIPs |
| A17 | Aya Red-teaming, English rows | 7,419 prompts total (split names not stated) | card "License: apache-2.0" https://huggingface.co/datasets/CohereLabs/aya_redteaming (safety.md S15) | paid native speakers (arXiv 2406.18682) | G1 harmful-request recognition (T50/T53 chat-side slice) | harmful yes/no; Claude writes an equal number of benign twins | any rephrased/augmented mix |
| A18 | Gandalf ignore_instructions (Lakera) | train 777 | "gandalf_ignore_instructions is distributed under the MIT License." https://huggingface.co/datasets/Lakera/gandalf_ignore_instructions (safety.md S42) | player prompts; selected by an embedding-similarity rule (no LLM labeller; "a few ... might not be real prompt injections") | T41c direct-injection slice (critic C8) | injection yes/no with Claude benign twins at 50% | validation 111, test 112 |
| A19 | Gandalf summarization (Lakera) | train 114 | "gandalf_summarization is distributed under the MIT License." https://huggingface.co/datasets/Lakera/gandalf_summarization (safety.md S43) | successful-guess prompts plus manual review; the ChatGPT `answer` field is never used | T41c indirect (summarise) slice | injection yes/no with benign twins | validation 13, test 13 |

### 1B. Tier B2: clean, but the test/dev split is a benchmark we read (blocked until O1 = YES) (7)

| # | Dataset | Train split, size | Licence (quote; URL; 18 Oct 2026) | Label provenance | Feeds | Becomes | Never touch (and register in G13) |
|---|---|---|---|---|---|---|---|
| B1 | CLINC150 + OOS (data_full) | 15,000 in-scope + 100 OOS | LICENSE "Creative Commons Legal Code / Attribution 3.0 Unported" https://raw.githubusercontent.com/clinc/oos-eval/master/LICENSE (decision_index.md row 7) | crowd ("We used crowdsourcing to generate the dataset") | general intent; abstain head (OOS = "none of these") | pick-one among k intents plus "out of scope" | test 4,500 + 1,000 OOS (DI 0.3 tested); val 3,000 + 100 OOS |
| B2 | MASSIVE 1.1, en-US text only | train 11,514 | NOTICE.md "The MASSIVE dataset is licensed under CC BY 4.0" https://github.com/alexa/massive; card cc-by-4.0 https://huggingface.co/datasets/AmazonScience/massive (decision_index.md N-2) | professional/MTurk localisation of SLURP; SLURP AUDIO is CC BY-NC and is never used | general intent; T54 argument grounding (slots) | intent pick-one; slot-value pick-one | test 2,974 (Nimble), dev 2,033; other locales wait for O11 |
| B3 | ContractNLI, document_type sec-text / sec-html only | 423 train NDAs x 17 hypotheses | "Our dataset is released under CC BY 4.0." https://stanfordnlp.github.io/contract-nli/ (decision_index.md row 22) | one researcher + two MTurk workers; paralegal-reviewed hypotheses | G1/G6 policy-card reading | entailed / contradicted / not mentioned, with program span selection | test 123 docs (DI 0.3 tested), dev 61; search-pdf documents excluded |
| B4 | WinoGrande winogrande_xl | train 40,398 | "The dataset is licensed under CC-BY." https://github.com/allenai/winogrande (decision_index.md row 24) | MTurk-written twin sentences; AFLite only filters | general | 2-way pick-one | validation 1,267 (DI 0.3 tested), test |
| B5 | ChessBench (searchless_chess action_value) | train shards (2,148) | "Some portions ... CC0 license from lichess.org"; "The remainder ... Creative Commons Attribution 4.0 (CC-BY)" https://github.com/google-deepmind/searchless_chess (decision_index.md row 16) | program (Stockfish 16 action values) | general, low | best move pick-one among 4 legal moves ranked by value | test action_value (DI 0.3 tested) |
| B6 | Amazon ESCI (Shopping Queries), train only, minus every query id in the DI kit's selected-rows file | small 33,804 / large 99,684 queries | "This project is licensed under the Apache-2.0 License." https://github.com/amazon-science/esci-data (decision_index.md row 10) | trained human annotators, at least 3 per pair, majority vote | general relevance, low | E / S / C / I pick-one | test; the DI kit's 5,000 sampled pairs (which split it samples is UNVERIFIED, so drop by query id) |
| B7 | Civil Comments (Jigsaw) | train 1,804,874 | "This dataset is released under CC0, as is the underlying comment text." https://huggingface.co/datasets/google/civil_comments (nlu.md F6; safety.md S140) | crowd raters (rater counts not published; card sections empty) | G1-adjacent moderation, low | toxic yes/no at a fixed threshold rule on rater fractions; ambiguous band (0.3-0.7) dropped | test 97,320 (Nimble samples 300), validation |

### 1C. Tier C: allowed after a named mechanical check (15)

Each check is pass/fail and done by Haiku with Sonnet verification; a failed check moves the row to DENY (no owner question
needed). New Yorker captions is also B2.

| # | Dataset | Train split, size | Licence (quote; URL; 18 Oct 2026) | Label provenance | Feeds | Becomes | Check before use | Never touch |
|---|---|---|---|---|---|---|---|---|
| C1 | CUAD | train (about 22K QA, 510 contracts; from memory) | HF YAML "license: cc-by-4.0"; Atticus site "CC BY 4.0"; GitHub repo has NO licence file https://huggingface.co/datasets/theatticusproject/cuad (nlu.md B23) | law students checked by lawyers | G1/G6 clause yes/no | "does the contract contain clause X" yes/no | licence statement readable on a primary page (Atticus) | test |
| C2 | e-CARE | train 14,928 | repo label "MIT license" (text not read) https://github.com/Waste-Wood/e-CARE (nlu.md C19) | crowd premises/hypotheses; explanations from GenericsKB (CC BY 4.0 on mirrors only) | general causal | 2-way cause/effect pick-one (no explanation text) | read LICENSE file; do not use GenericsKB explanations | dev 2,132, test 4,264 |
| C3 | Social IQa | train 33,410 | card "CC-BY-4.0" (card only) https://huggingface.co/datasets/allenai/social_i_qa (nlu.md C9) | human handwritten wrong answers (paper refutes the card's "machine-generated" wording) | general: intent/social decisions | 3-way pick-one | ATOMIC-2019 licence readable and permissive | dev, test |
| C4 | QuaRTz | train 2,696 | card "licensed under Creative Commons Attribution 4.0 International" https://huggingface.co/datasets/allenai/quartz (nlu.md C3) | crowd | general | 2-way pick-one | licence on a primary AI2 page | dev, test |
| C5 | QASC | train 8,134 | "We release the data under CC BY license" https://github.com/allenai/qasc (nlu.md C2) | MTurk crowd; BERT only filtered | general | 8-way pick-one (no retrieval corpus) | CK-12 and WorldTree seed-fact terms are not NC; if NC, DENY | dev, test |
| C6 | FLD (hitachi-nlp/FLD-corpus GitHub release; NOT the FLD.v2 HF card) | 30,000 per config | GitHub corpus "CC-BY-4.0 license" https://github.com/hitachi-nlp/FLD-corpus (nlu.md C24); FLD.v2 HF card states no licence (decision_index.md E6) | program (proof trees + templates), no LLM | general logic | proved / disproved / unknown | read the corpus LICENSE file | its test files |
| C7 | StrategyQA (original release, never the BIG-bench copy, guard F5) | train (about 2.3K, from memory) | code LICENSE MIT https://raw.githubusercontent.com/eladsegal/strategyqa/main/LICENSE; data licence UNVERIFIED (allenai.org redirects) (nlu.md C18) | MTurk questions; RoBERTa only rejected easy items | general yes/no | question-only yes/no (no Wikipedia paragraphs) | data licence on a primary page | dev, test |
| C8 | FinQA | train (about 6.2K, from memory) | LICENSE "MIT License / Copyright (c) 2021 Zhiyu Chen" https://raw.githubusercontent.com/czyssrs/FinQA/main/LICENSE; source reports "CDLA-Permissive" (nlu.md E5) | 11 finance professionals (UpWork) | general tables/numeric | pick-one among program-made near-miss answers | owner line O7 (CDLA) = YES | test |
| C9 | FlakeFlagger (Zenodo 4450723), labels and metrics only | test-level labels, 24 Java projects | "Creative Commons Attribution 4.0 International" https://zenodo.org/records/4450723 (decision_index.md E12) | execution (10,000 reruns per project) | T62 FLAKY-OR-REAL | flaky yes/no from run statistics and test metadata | no Java source text until the 24 project licences are checked | our hold-out by project |
| C10 | ManySStuBs4J | 100 Maven / top-1000 variants | "Creative Commons Attribution 4.0 International" https://zenodo.org/record/3653444 (code.md row 61) | program (SZZ + message keywords, about 94% on 100 commits) | T57 LOCALISE realism (P1) | "which hunk is the bug" pick-one | per-repo permissive filter (MIT/Apache/BSD/ISC/CC0) on any re-fetched code; A46 screen | n/a |
| C11 | TSSB-3M | >3M single-statement fixes (no code shipped) | "Creative Commons Attribution 4.0 International" https://zenodo.org/records/10217373 (code.md row 62) | program (heuristic "likely_bug" flag) | T57 LOCALISE realism | same as C10 | same as C10; keep only likely_bug rows | n/a |
| C12 | SWE-Gym (2,438 instances only; never its trajectories or verifiers) | train 2,438, 11 Python repos | HF "License: mit" https://huggingface.co/datasets/SWE-Gym/SWE-Gym; GitHub "Apache-2.0 license" https://github.com/SWE-Gym/SWE-Gym (code.md row 27) | human issues and patches; execution tests; ~200 human hours of setup | T57r transfer slice (P1) | patch fixes/doesn't (with the four-gate gold), localise | per-repo licence of moto, MONAI, pandas, mypy, dask, dvc, conan, pydantic, hydra, bokeh, modin; instance-level G13 vs SWE-bench, SWE-bench-Live, SWE-rebench (K9) | everything in B11/C6 |
| C13 | CommitPackFT, licence whitelist only | 702,062 samples before filter | card "Each sample comes from a code repository with a permissive license" but its license field lists agpl-3.0, lgpl-2.1, unknown https://huggingface.co/datasets/bigcode/commitpackft (code.md row 71) | human commit messages; rule filters (GPT-4 only categorised tasks for a figure) | T66 REVIEW-GATE head "does this message describe this diff" (critic C6c) | yes/no; negatives by swapping messages across same-repo commits | keep only mit, apache-2.0, bsd-2-clause, bsd-3-clause, cc0-1.0 rows; 8.5 PASS | n/a |
| C14 | MBPP (full config, train split only) | train 374 | "CC-BY-4.0" https://huggingface.co/datasets/google-research-datasets/mbpp (code.md row 2) | Google internal crowdsourcing | T42c realism, tiny | will-this-test-pass yes/no on human solutions plus program mutants | problem-level G13 vs CodeMind sources (D24) and REval | test 500, validation 90, prompt 10 |
| C15 | New Yorker caption contest, `matching`, text only (also B2) | train 2.34K | "cc-by-4.0" https://huggingface.co/datasets/jmhessel/newyorker_caption_contest (decision_index.md row 37) | crowd descriptions (MTurk HIT, paper 2209.06293) | general taste, low | pick-one caption | caption text rights statement found; O1 = YES | matching test 528 (DI 0.3 tested), validation |

Tier totals: A 19, B2 7, C 15 = **41**. Most rows feed the general block; the rest feed T59/T60, T41c, the G1 chat-side
slice, T62, T57/T57r, T63, T65, T66 and T42c (see the Feeds column).

---

## 2. OWNER list (answer once; one line each)

| # | Question | What it unlocks (examples) | Why it matters | Risk | Default if no answer |
|---|---|---|---|---|---|
| O1 | Release the TRAIN split of a dataset whose test/dev split we read, if (i) full-row G13 shows the train split is disjoint from every registered test/dev item, (ii) it is not an A61(a) HIT, (iii) every report on that dataset says "train split seen"? | CLINC150, MASSIVE, ContractNLI, WinoGrande, ChessBench, ESCI, Civil Comments, New Yorker (tier B2); later any O2 set that is also a Nimble set | Without it the split-aware tool denies the whole dataset (R5 check finding 3); Perplexity Decider v1.2 did exactly this ("decontaminated against the test sets", https://huggingface.co/perplexity-ai/pplx-decider-v1.2, 18 Oct 2026) | those benchmarks stop being "unseen"; headline claims must use only OHS-5 and unseen sets | YES with the 3 conditions |
| O2 | Accept CC BY-SA training data? | SNLI, MultiNLI (minus FICTION), BoolQ, SQuAD 1.1/2.0, HotpotQA, Natural Questions, ARC, DROP, FEVER, VitaminC, AmbigQA, SGD, Spider, FOLIO, WikiTableQuestions, QuAC, CREAK, Social Chemistry, e-SNLI | Without it there is no large NLI, boolean-QA or reading-comprehension set (nlu.md section 9 item 1) | share-alike is not on the owner's list; possible obligations on derived data | NO |
| O3 | Accept third-party text inside a permissively licensed set? (a) Wikipedia passages; (b) social-platform posts; (c) contest and exam problem statements | (a) CondaQA, MuSiQue, 2WikiMultihopQA, Quoref, TabFact, HybridQA; (b) GoEmotions, Measuring Hate Speech, HateXplain; (c) CodeContests, APPS minus Kattis, Project CodeNet, Codeflaws, MATH, AQuA-RAT, MathQA, MedMCQA | (a) negation, multi-hop, table entailment; (c) the best human right/wrong code verdict data (judge verdicts) | the dataset authors cannot relicense text they do not own (decision_index.md rows 44, E4, E8; code.md cross-cutting risk 1) | (a) NO, unless passages can be replaced; (b) NO; (c) NO |
| O4 | Accept human labels on LLM-written inputs? | HelpSteer2, Aegis 1.0/2.0, HH-RLHF harmless/red-team | answer-adequacy and harm labels at scale | the inputs are other LLMs' outputs; HH-RLHF card says "not meant for fine-tuning"; Aegis has no per-row prompt-origin field | NO |
| O5 | Reopen the no-LLM-data rule for When2Call train, WildGuardMix train, WildJailbreak? | the two biggest levers on the AA index (25% each) | When2Call answers are exactly T54; WildGuardMix is the AA safety component's own pipeline | Mixtral/GPT-4 made; xLAM "research purposes only" upstream; GPT-4 labels; near-duplicates of the AA test sets | NO |
| O6 | Use tasksource-jev-typed-decisions through a per-SOURCE allow-list (never the whole catalogue)? | up to 751 sources; Strands Decider used 119 | "A large part of the gains are thanks to the tasksource data" (Perplexity v1.2 card, 18 Oct 2026) | per-row licences include cc-by-nc-4.0 and BY-NC-SA; no provenance column (https://huggingface.co/datasets/tasksource/tasksource-jev-typed-decisions, 18 Oct 2026) | YES: each promoted source gets its own row in this inventory first |
| O7 | Accept licences that are permissive but not on the list by name: CDLA-Permissive-2.0; Google's PAWS notice "may be freely used for any purpose"; AFL-3.0 | FinQA (FinTabNet), Project CodeNet (if O3c), PAWS-Wiki labeled (also machine-made text), PIQA | paraphrase and physical-commonsense sets; CodeNet verdicts | PAWS text is word-swap/back-translation machine text | YES for CDLA-Permissive-2.0 only |
| O8 | Field-level or slice-level salvage of mixed sets (drop the LLM-made fields or rows)? | SWE-smith procedural rows (if the strategy mapping is verified), CLadder generator minus the GPT-4 nonsense variant, open-r1/codeforces human fields, SWE-bench train with a per-repo filter, HackAPrompt `user_input` only | patch-verdict realism; causal reasoning | mapping UNVERIFIED (SWE-smith); HackAPrompt has no usable label once completions are dropped | YES only for SWE-smith procedural (after mapping) and CLadder minus nonsense; NO for the rest |
| O9 | Accept LLM-made carriers with program labels for injection? | BrowseSafe-Bench (Claude Sonnet rewrites), prodnull repo injections (Ollama paraphrases), AgentDrift (Llama-3.3-70B) | closest public shapes to T41c | LLM-made; AgentDrift hits the no-bigger-teacher rule | NO |
| O10 | Promote sets whose licence or label provenance is unverified, once a primary page confirms it (no new owner line needed then)? | BANKING77 (paper silent on authorship, ~14% reported label noise), CosmosQA (licence by email), OpenBookQA, ProofWriter/RuleTaker data zip, NLI4CT, Humicroedit, WikiSQL data, FLD.v2 card, Samsung CredData (per-file licences), ParamBench | intent routing (BANKING77 is a DI test set too), logic | licence or authorship unconfirmed | NO until confirmed; then they enter tier C automatically |
| O11 | Is non-English in scope for C2.1? | MASSIVE other locales (Nimble also tests de-DE), Aya non-English | Nimble de-DE subset | none on licence (CC BY 4.0 text) | NO; claims say "English only" |
| O12 | Does C2.1 target the vision gap (C1 77.7 vs Jev 1.14 85.1)? | a vision licence/train-split research pass | owner goal "on everything else beat Jev" | no v4 research exists on vision data | NO; claims exclude vision |
| O13 | Raise the $30 training cap or lower C1-init replay if C2 does not ship? | block R plus new families at C1 init (section 6) | at C1 init the planned mix already reaches about 95K before any public data | spend; forgetting | NO raise; Opus re-sizes block R to fit |

---

## 3. DENY list (with reasons)

Grouped by reason. Each name is DENY in its refuter-corrected row; the file is given for the detail.

1. **Barred A61(a) HITs, any id or form**: gsm8k and every derivative (GSM-Plus, GSM-Symbolic, MetaMath, Reasoning Gym
   gsm_symbolic, Lila, ToolQA's GSM8K domain, MAST-Data's GSM-Plus part), hover, isarcasmeval, tydiqa, md_fdc, md_peps,
   md_worldbank, md_usgs, md_cma, DI-TS inputs, SB6 (R5_CANDIDATES_CHECK.md; nlu.md D7/D9, H1-H4; tools.md row 67).
2. **Test-only or eval targets (no train split, or the "train" name is a loader default)**: BFCL, MMLU-Pro, MMLU, BBH, BBEH,
   GPQA, HLE, AA-Omniscience, SimpleBench, MuSR, SATA-Bench, CRUXEval(-X), LiveCodeBench, EquiBench, CodeMind, CoRE, REval,
   HumanEvalPack, SWE-bench test/dev/Pro/PolyBench/Live, Multi-SWE-bench, Impossible-*, EvilGenie, Defects4J, BugsInPy,
   QuixBugs, Bugs.jar, BugsJS, home-appliance simulator, BRIGHT, SummEval, BPoMP, Habermas Machine, ForecastBench,
   MCP-Atlas, MCP-Universe, MCP-Bench, MCPMark, LiveMCPBench, Toolathlon, ToolHop, NESTFUL, ACEBench, ToolBeHonest, RoTBench,
   ToolEyes, T-Eval, UltraTool, GTA, ToolTalk, ToolSandbox, RestBench, WildToolBench, HiL-Bench, API-Bank eval, tau/tau2-bench,
   AgentDojo, InjecAgent, AgentDyn, ASB, MSB, MCPTox, MCPSecBench, Lakera b3, promptprotection agent-security, ARPIbench,
   CodeIPI, LogJack, R-Judge, ATBench(-Codex), TS-Bench, ASSEBench, Agent-SafetyBench, AgentHarm (also "refrain from using
   ... for training"), ToolEmu, OS-Harm, OpenAgentSafety, SafeArena, ShieldAgent-Bench, MT-AgentRisk, TraceSafe, BLINDSPOT,
   SABER, ClawSafety, RedCode, CyberSecEval, XSTest, OR-Bench, JBB-Behaviors, HarmBench, StrongREJECT, AdvBench, SORRY-Bench,
   JailBreakV-28K, SimpleSafetyTests, HEx-PHI, CatQA, the MaliciousInstruct/ALERT/DecodingTrust groups, OKTest/SGXSTest/
   HiXSTest, AmPermBench, UnderSpecBench, SteerBench-Work, CredLeakBench, ProcCtrlBench, Ambig-SWE, ZebraLogic, CodeSense,
   ClimateFEVER, MCTACO, SVAMP, HANS, PAWS-X, LIMBO (nothing released), JevBench (all variants: no train, partly LLM-written).
3. **NC or research-only licences**: ANLI, XNLI, SICK, WiC, ReClor, RACE, SciQ, ASDiv, MS MARCO, CLUTRR, TabMWP, xCodeEval,
   KodCode, APIGen-MT-5k, NexusRaven eval, BeaverTails, PKU-SafeRLHF, ToxicChat, Do-Not-Answer (text says NC-SA),
   SafetyInstructions, QHarm, MaliciousInstructions, FalseReject, Qwen3GuardTest, WASP, IssueTrojanBench, cfcolor, POP909,
   emotion (dair-ai), AG News / Yahoo Answers / Yelp (per the Strands card), MedNLI (credentialed), SHP (revocable Reddit
   licence), CAR-bench (NC paper), ClarifyBench, SWE-Stream, TaskTracker/SecAlign (no licence, Alpaca lineage).
4. **GPL/AGPL or copyleft inside**: CuBERT (ETH Py150 GPL/LGPL repos), MutantBench (GPL-3.0), AgentTrust (AGPL), OpenSWE
   (AGPL), SGBench (GPL), ALFWorld expert plans (Fast Downward GPL; also OWNER-lean-DENY in tools.md). Copyleft rows inside
   CommitPackFT and SWE-smith are dropped row by row (tier C13, O8).
5. **LLM-made or LLM-labelled data (no-LLM rule; distillation)**: When2Call (unless O5), xLAM/APIGen, ToolACE, ToolBench,
   StableToolBench, ToolAlpaca, API-Bank train, Seal-Tools, Glaive, Hermes FC and reasoning tool use, Toucan, Nemotron
   tool_calling/Agentic/SWE/RL-IPI/Safety Guard v3, Qwen3.6 tool-calling, UltraData, Agent-FLAN, AgentInstruct, SatoHub,
   DeepNLP, unified-tool-calls, obaydata, nano-tool-calling, Hammer irrelevance (xLAM inputs), ToolRet, API Pack, TinyAgent,
   APIBench, MTU-Bench, TaskBench, MetaTool, ToolDial, MI4ToolCalling, ShortcutsBench, IN3, ComplexFuncBench, KOPA/EDGE, E-Bench,
   UserBench, NoisyToolBench, HumanMCP and siblings, COVERT/CAMPHOR/ToolGrad family, CoALM-IT, AgentProcessBench/ToolPRMBench,
   AgentGym, WANLI, ToxiGen, DocNLI, HellaSwag (also WikiHow NC-SA contexts), SWAG, RAGTruth, MuSR, MAST-Data, developer-agent
   episodes, School of Reward Hacks, TRACE, Terminal Wrench, HackTrace, MALT, RH-Detect, BAITBENCH, Open-SWE-Traces,
   Nemotron-SWE, SWE-Dev, SWE-Flow, SWE-Universe, R2E-Gym, TACO (GPT-4 test inputs), Code-Contests-Plus, PIE (ChatGPT
   translations), codeforces-cots, GuardReasonerTrain (also NC upstreams), PolyGuardMix, DynaGuard, Qwen3Guard training,
   SALAD, UltraSafety, SafetyPrompts (thu-coai), HarmfulQA, AgentAlign, StepGuard, StepSafe, AgentDoG data, IH-Challenge,
   PIDS-Bench, NotInject, xTRam1 safe-guard, jackhhao jailbreak-classification, PromptShield (Alpaca/UltraChat benign),
   OASST1/OASST2 (OWNER-low in their files; ChatGPT text admitted inside), WildChat (moderation-model labels),
   RealToxicityPrompts/PolygloToxicityPrompts (classifier labels), ProsocialDialog (GPT-3 turns), CoCoNot pref (GPT-4).
6. **No licence or unusable terms**: FinEntity, ACOS, VAST, IDoFT, ClariQ, ToolMaze, AgentDyn data, TensorTrust, MCPTox,
   ImpossibleBench HF data, Petke patch set (artefact not found), BugsInPy, Toolathlon, m&m's, SWE-smith-js, SecretBench
   (access on request), MuTual, LogiQA (exam text, no licence), TriviaQA (copyright not owned), NewsQA (CNN terms).
7. **Barred by the plan or registry**: CVEfixes, PrimeVul, BigVul, MoreFixes (guard F2), Atomic Red Team and anything built
   on it (CARE corpus, AgentJailbreak skill files), GTFOBins, NL2Bash, tldr-pages, human-written MCP schemas, CodeReviewer,
   CodeReviewQA, LLMail-Inject (registered literal target D8), BIPIA (D3), SWE-rebench (B11 eval source), CodeXGLUE (C-UDA,
   Devign CVE family), ConDefects (CC BY-SA and LiveCodeBench window).
8. **Competitor outputs** (never data, label or filter): Jev, Nimble data and weights (CC BY-NC, all labels model-made),
   Strands Decider, Perplexity Decider, AgentDoG, every detector (E45-E52b), BigCodeReward and Copilot Arena (competitor
   completions; OpenRAIL-M).

Counts (from the six files after their refuter passes; overlaps between files are not de-duplicated, UNVERIFIED exact
distinct count): decision_index 41 rows DENY; nlu 27 rows (18 + 9); code 52; safety 118 datasets; tools 77; hardest 50.

---

## 4. Per-family hardest-question targets (what to generate; clean-room)

Rules for every target (hardest.md section 0 and 1.12; plan section 1E):
- Copy the MECHANISM only, never an item, entity name, ID pattern, phrasing, tool name or server name from any benchmark;
  every name comes from the seeded random namespace with the training salt; G13 checks every row.
- Difficulty is set by a program parameter, never by filtering against another model (no-big-teacher rule).
- Ladder rule (critic D1): each G0-lite names its mechanisms, gives each a level parameter (L1-L4) and puts at least 25%
  of rows at L3-L4. The quad structure (alarming vs calm surface) x (risk present vs resolved) is mandatory for T50, T51,
  T53, T41c and T56.
- Measured bar (critic D2): in every 1,000-row pilot, read base 4B and C2 on od-l4b; the top level must sit at or below a
  pre-written accuracy (proposal: C2 <= 70% on L4). If it is easier, raise the program parameter, never drop rows by model
  score. This is a pre-freeze check on our own models, allowed by the rules.
- Each hard cell has an easy-looking twin with the opposite label, so the model cannot learn "hard surface = BLOCK".

| Family | Hardest mechanisms to project (source: hardest.md section) | Top-level (L4) generator target |
|---|---|---|
| T50 SHELL-GATE | single precise target on an unauthorised object (94.4% FNR); same effect through a direct state-file edit instead of the CLI (92.9% FNR on cleanup); warning visible + safe path exists (SABER 82.5% harmful); benign dual-use in production lanes over-blocked (29.5-34.8% FPR); obfuscated benign = obfuscated dangerous (1.1) | quads of equivalent-effect channels; scope inversion pairs (precise unauthorised = ASK/BLOCK, wide batch inside authorised set = ALLOW); production rollout with authorisation in the trajectory = ALLOW; never generate rows on the subjective high/critical boundary |
| T51 SCOPE-BOUNDARY | target certainty is the dominant axis (Safe Success 67.9% to 8.6%); wrong object of the right kind; over-broad command on the right object; evidence-reversed mirrors (63.8% vs 98.5%) (1.2) | blast radius as the ONLY edited fact in a contrast pair; same-type object with a different owner or protected flag; glob/flag widening on the correct target; cleared-risk vs stale-clearance mirrors; report ALLOW recall |
| T53 EGRESS-SECRET | plain transport on the correct host (90.6% leak); second-page field escalation; recovery via a trusted route (0-24%); stdout/log/temp-file/shell-history channels (75.8% of leaks via stdout/stderr) (1.3) | host string identical, only the scheme differs; follow-up form asks for more fields; trusted full address earlier in context vs domain-only; non-"send" channels with provenance gold; odd-looking but allow-listed hosts = ALLOW (at least as many as BLOCK); phishing-URL head (critic C8) |
| T41c TAINT | helpful ambient instructions (login, OTP, invite, attachment, merge-conflict message, TODO) are the hard benign class; trigger-word density; tail placement; prerequisite / term-redefinition / conditional / authority framing (1.4) | carrier x placement x framing grid, a third at the tail; delegated-instruction pairs differing only in the user turn; benign text with 3+ security words = ALLOW_BENIGN and malicious text with 0 trigger words; held-out wrapper styles; direct-injection slice from Gandalf (tier A18-A19) with 50% Claude benign twins |
| T54 TOOL-NEED/PICK | near-miss tools that overlap on every word but one capability; three different "not callable" causes; policy eligibility just inside / just outside; confirmation-handling; two entities match = premature action (1.5) | same-namespace near-miss sets; missing tool vs missing parameter (ask) vs missing prior RESULT (say so), call/no-call 40-60% per sub-block; eligibility computed from a generated record at the boundary; confirmation present/absent pairs |
| T55 RECOVER-ESCALATE | implicit, well-formed but wrong results (recovery collapses by 37.15 points); lost-ack write where read-back cannot resolve; retry-until-success with no bound; polling looks like looping (1.6) | 2x2 explicit/implicit x transient/permanent with invariant types the card does not name; ledger cases (key offered / read path / neither = escalate); state-change predicate decides loop vs poll; A-B-A-B oscillation; neutral-but-harmless vs harmful step pairs. Fix the plan's LIMBO citation (section 5 H2) |
| T56 DONE-CLAIM + T56g | partial state reported as complete (22.58% of real episodes); detectors win on confident closing words and action volume (AUROC <= 0.65 for LLM judges); justified special-casing ("backward compatibility"); multi-file diffs with plausible messages (monitors 42-65%) (1.7, 1.8) | identical claim text, n of m items verified; surface-cue probe on tool-output length/closing words; question-treated-as-permission edits; hacks that read grader state or patch the evaluator; legit twins (spec-required special case, spec-driven test edit, genuine fixture fix) = ALLOW; impossible-by-spec rows with an ask/abort gold |
| T42c CODE-EXEC | 15-40 executed steps, exact string assembly, misleading names, off-by-one compare; aliasing through two names; post-loop values; dead-code removal that depends on state (EquiBench DCE at chance); similarity bias (1.9) | output items at 15-40 steps; equivalence pairs crossed (structure change x one-token inequivalence) with a text-similarity-only probe; helper-two-calls-away test failures; NEW sub-head "will it compile / type-check" with gold from the pinned toolchains (critic C2; never ShellCheck/hadolint as gold) |
| T57 PATCH-VERDICT | wrong-but-passing classes: logic 47%, incomplete fix 35%, type mismatch 7%, boundary 6%, off-by-one 1%; "does more than the reference"; solution leakage in the issue text; implicit naming requirements (1.10) | each class passes visible tests and is killed by the four-gate hidden suite, weighted by the measured mix; extra-side-behaviour patches; leakage tagged and capped at the natural rate with a CPU "answer in issue" probe; file-level and hunk-level LOCALISE reported apart; realism from tier C10-C12 |
| T59 ASK-OR-PROCEED (promote to P0, critic C1) | target certainty, intent clarity, missing slot (UnderSpecBench axes; MultiWOZ/ABCD mechanisms) | spec with k admissible interpretations; ASK iff interpretations lead to different actions with non-reversible cost; contrast pairs where only one detail is removed; tier A3-A5 real dialogues as a realism slice |
| T60 CONTROL-NEXT (new, critic C1) | NO-PUBLISHED-STUDY (hardest.md section 0) | delegate vs do; keep vs drop at compaction (gold = whether a later step depends on the fact); plan vs act from a generated task-risk spec; distractor facts that look important but no later step uses |
| T62 FLAKY-OR-REAL (P1) | real failure that looks like noise; flaky failure that looks deterministic | run-statistics features from tier C9 plus generated logs; failing-chunk pick-one from tier A15; same error text, different rerun history |
| T63 DEP-RISK (P1) | hallucinated package names that repeat (43% repeat, secondary, UNVERIFIED); cross-registry near-miss; typosquat | "EXISTS?" sub-family against an offline snapshot in the seeded namespace plus the pinned stdlib; conflation and cross-registry negatives; licence-compatibility head from an Opus-written table of licence IDs (critic C7); malicious-manifest labels from tier A16 |
| T65 VULN-SYNTH (P1) | good/bad twins that differ by one sanitising call | tier A14 Juliet twins plus Claude-authored application-style variants; no CVE ids (F2) |
| T66 REVIEW-GATE (P1) | message describes a different same-repo diff; breaking change hidden in a minor bump; conflict resolutions that compile but break one side | commit-message swap negatives (tier C13); generated caller suite run on old vs new API; conflict resolution whose gold is "both sides' tests pass" on od-sbx1 (critic C6) |
| T67 IAC-GATE (new P1, critic C4/C5) | destroy/replace hidden in a long plan; public exposure; privilege widening; lock-taking DB migration on a large table | generated specs rendered to Terraform plan JSON, manifests, CI workflows; our own rule table labels; Checkov (Apache-2.0) and squawk (Apache-2.0/MIT) as round-trip validators only (CRITIC.md C4/C5, fetched 18 Oct 2026) |
| General: NLI / claim (block R: SciFact, ContractNLI, ETHICS) | one-edit negation, quantifier, scope and date flips (CONDAQA mechanism); conflicting evidence | Claude-authored passages, one decisive edit per pair, two independent Claude solvers + Opus adjudication where no program gold exists |
| General: intent / OOS (CLINC150, MASSIVE, HWU64, SNIPS) | near-domain out-of-scope queries; confusable intent pairs | k-way rows with program-chosen nearest intents; OOS twins that share every content word with an in-scope intent |
| General: reading / abstain (Qasper, CUAD, StrategyQA) | unanswerable twin with the answer span removed (SQuAD 2.0 mechanism on our own passages) | abstain option at a controlled 10-15% rate, gold by construction (critic E2) |
| General: faithfulness | one unsupported claim injected at a known span (RAGTruth/SummEval mechanism; both DENY as data) | summary/answer pairs differing by one injected span |
| General: reasoning (BoardgameQA, FLD, Reasoning Gym, DM Math) | first wrong step in a trace; genuine "unknown"; search-space size (ZebraLogic); operators defined in the prompt (1.11) | program-made traces with one injected error; solver-computed unknown at a fixed rate; complexity by program parameter |
| General: formats | select-all-that-apply; ordinal severity; enum extraction (SATA-Bench; JevBench families) | yes/no-per-option recast; ordinal-bucket Choice recast (whether C2's renderer supports Score items is UNVERIFIED: check first, critic A6) |

---

## 5. Critic gaps: fix and place in the build order

Build-order slots used: **S0** = before the Mon 19 Oct owner message; **S1** = by Wed 21 Oct (registry + manifest v2);
**S2** = G0-lite and generator code, before the OHS-5 freeze; **S3** = 1,000-row pilots and 200-row G13 pilots;
**S4** = binding G13, selection, mix, data freeze; **S5** = GO #1 packet; **S6** = post-training report.

| Gap | Sev. | Fix | Slot |
|---|---|---|---|
| A1 no public-data block | HIGH | new lane L-R and mix block R (this file's section 1), manifest v2 one record per dataset, per-dataset cap, G-dev check before and after block R | S1 manifest; S2 mappers; S4 mix |
| A2 tasksource has no path | HIGH | owner O6; Haiku licence scout over the 751 source values, Sonnet verifies each promoted source; each becomes a manifest-v2 name and a row in section 1 | S0 ask; S1-S2 scout |
| A3 code realism sets unused | HIGH | tier C9-C14 and A14-A16 as P1 transfer slices (T57r, T62, T63, T65, T66); CodeContests/CodeNet/APPS wait for O3c and O7 | S2 (P1 wave) |
| A4 third-party generators ignored | MEDIUM | Reasoning Gym, DM Math, bAbI inside the general block with a per-task allow-list (tier A11-A13) | S1 manifest; S2 |
| A5 noise screen only on replay | MEDIUM | same A46 drop-only screen (C2 reads on od-l4b, p_g < 0.2) on every block-R human-label row; a dataset losing >15% goes to Opus | S3-S4 |
| A6 big label sets / multi-label / Score | MEDIUM | k in {4, 8} program distractors; yes/no per option; check renderer Score support | S2 |
| B1 ~80 benchmark test splits unregistered | HIGH | register in G13 before manifest v2: HLE, AA-Omniscience-Public, every DI 0.3 tested split (BANKING77, CLINC150, MASSIVE, WinoGrande, ContractNLI, ChessBench, ESCI kit rows, New Yorker matching, Civil Comments ...), the 13 Nimble subsets, all JevBench variants; safety.md 0.6 list; tools.md 5 list; hardest.md 2 list; EquiBench and CodeMind at problem-id level; Codeforces/AtCoder date rule (before 2022-11-30). One merged list (Haiku dedupe, Opus confirm); row-start guard refuses block-R jobs until the registry sha includes them | S1 |
| B2 split-scope undecided | HIGH | owner O1 in the Mon 19 message; turn on `--split-scoped-release` only after YES | S0 |
| B3 G13 is a 200-row pilot | HIGH | full-row G13 for every block-R and replay row, near-duplicate methods, transitive sources (HotpotQA vs HoVer, MuSiQue vs SQuAD/NQ, APPS vs CodeContests); measure Mac throughput on 10K rows first; add a second G13 host rather than sample | S1 measure; S4 run |
| B4 replay not checked against new targets | MEDIUM | one new-target G13 pass over all replay rows, drop-only, logged per family | S4 |
| B5 no "train split seen" flag | MEDIUM | every report row carries seen/unseen; headline only on OHS-5 and unseen sets | S6 (defined at S1) |
| B6 manifest misses 3 A61(a) names | LOW | add md_worldbank, md_usgs, md_cma to manifest v2; Opus checks md_* aliases | S1 |
| C1 ask-or-proceed P1 only; delegate/compaction/plan-vs-act missing | HIGH | promote T59 to P0; add T60 CONTROL-NEXT; state whether they count toward the training floor (proposal: they count only as extra, the 6-of-9 floor is unchanged) | S2 |
| C2 compile/type/lint missing | MEDIUM | T42c sub-head with pinned toolchain gold; check mypy component licences (UNVERIFIED) | S2 |
| C3 hallucinated package/API missing | MEDIUM | T63 "EXISTS?" sub-family | S2 (P1) |
| C4 IaC/config review missing | MEDIUM | T67 IAC-GATE, Checkov validator only | S2 (P1) |
| C5 DB migration safety missing | MEDIUM | MIGRATION sub-block in T67 (or T50), squawk validator only | S2 (P1) |
| C6 merge conflict / semver / commit message missing | MEDIUM | three T66 heads; CommitPackFT whitelist (tier C13) | S2 (P1) |
| C7 dependency-licence compatibility missing | LOW | small T63 head from an Opus licence-ID table | S2 (P1) |
| C8 phishing and direct injection thin | LOW | T41c direct slice (tier A18-A19 + twins); T53 phishing-URL head | S2 |
| D1 hardest mechanisms not in G0-lites | HIGH | ladder section per G0-lite (section 4) | S2 |
| D2 no measured difficulty target | HIGH | C2 <= 70% on L4 in each pilot; raise parameters, never model-filter | S3 |
| D3 no NLU hard extensions | HIGH | general-block hard-extension generators (section 4 "General" rows) | S2 |
| E1 no projected G gap with/without block R | HIGH | before GO #1 measure base 4B, C1, C2 on a G-dev of UNSEEN public sets; project the gap for (a) no block R, (b) block R tier A+C, (c) plus B2 (O1); honest range only | S3-S5 |
| E2 abstention not trained | MEDIUM | abstain head 10-15% across general rows; CLINC150 OOS, Qasper unanswerable; per-type abstain-threshold report | S2; S6 report |
| E3 LoRA modules on linear-attention layers | MEDIUM | record C2's actual module list; one cheap ablation inside the cap or a written reason not to (gain UNVERIFIED) | S5 |
| E4 multilingual absent | MEDIUM | owner O11 | S0 |
| E5 long documents | LOW | program span selection; log length drops | S2 |
| F1 no public general eval besides sealed G | HIGH | report-only "public-G panel" of UNSEEN public sets (never in block R) in L-E; Jev read once by our client | S1 define; S5 read |
| F2 families with no public eval | MEDIUM | say "OHS-5 only" per family; register CredLeakBench, Impossible-*, EvilGenie, SWE-bench-family verdicts report-only where licences allow | S1; S6 |
| F3 vision has no data or research | MEDIUM | owner O12 | S0 |
| G1 licence rulings not bundled | HIGH | section 2 table (O1-O13), one owner message | S0 |
| H1 verdict contradictions | MEDIUM | resolved here by strictest verdict: BANKING77 OWNER (O10; confirmed today); CONDAQA OWNER (O3a); Civil Comments ALLOW but B2 (licence clean, Nimble eval corpus); CodeContests OWNER (O3c); HackAPrompt OWNER (O8); SWE-smith OWNER (O8); FLD = FLD-corpus GitHub ALLOW tier C6, FLD.v2 HF card OWNER (O10); WikiSQL OWNER (O10, data licence unknown); MuSiQue OWNER (O3a); FOL-nli OWNER (GPT-4 predicates, O8 default NO); decision_index.md section 9 researcher list is superseded | done here; Opus confirms at S1 |
| H2 plan cites LIMBO wrongly | MEDIUM | replace "duplicated a lost-ack write in 56-74%" with: lost-ack 0.5%, misleading HTTP 500 8%, late commit 56%, redelivery 74% (hardest.md row 31, https://arxiv.org/html/2609.29095, 18 Oct 2026); class design unchanged | S2 (T55 G0-lite) |
| H3 Nimble sets "unknown" in nlu.md | LOW | Nimble list is decision_index.md section 5; Nimble intersections marked B2 or O1/O2 here (MASSIVE, Civil Comments, PAWS, BoolQ, SQuAD 2.0, MultiNLI, PubMedQA, VitaminC, Aegis, HelpSteer2, SummEval) | done here |
| I1 8.5 is a single step | MEDIUM | batch 8.5 by source group; publish measured time per source from the first batch | S1-S2 |
| I2 shed order sheds general rows third | MEDIUM | put block R and general rows after P1 and voice in the shed order; keep them only if G-dev (E1) says they help | S1 (plan edit) |
| I3 angles never researched | LOW | one more Sonnet research pass with refuter on: vision, multilingual, coding-agent everyday decisions, code-review human preference, and the code.md "not opened" names (PySStuBs, D2A, Bears, Vul4J, Avatar, BigCloneBench, POJ-104, DeepFix, GHALogs, Defexts, Megadiff, CanItEdit, SWE-Fixer, SWE-Factory, CodeSearchNet, OpenCodeReasoning) | S1-S2 |

Coverage of the ~80 Decision Index / Nimble / JevBench rows (decision_index.md section 9: 78 rows + AA-Omniscience = 79):
- trained through block R (if O1 = YES): CLINC150, MASSIVE, ContractNLI, WinoGrande, ChessBench, ESCI, Civil Comments, New
  Yorker; plus BoardgameQA, Juliet, CommitPackFT, FlakeFlagger from the model-card lists (13 names in all).
- waiting on owner lines: BANKING77 (O10), SA sets (O2), LLM-input sets (O4), When2Call/WildGuardMix (O5), tasksource
  (O6), PAWS (O7), CLadder (O8), NLI4CT/Humicroedit/FLD.v2 (O10), CodeContests/MuSiQue/CONDAQA (O3).
- skill analogue only (clean-room mechanism, never data): BFCL/When2Call test -> T54; home-appliance simulator -> our own
  device-control generator; BRIGHT/ESCI-style -> relevance generator; BBH/BBEH -> Reasoning Gym tasks + section 4; MuSR ->
  our narrative generator; SATA-Bench -> select-all format; CRUXEval -> T42c; RAGTruth/SummEval -> faithfulness generator;
  PhishNChips -> T53 phishing head; FinEntity/ACOS/VAST -> two-solver targeted sentiment/stance; GSM8K/HoVer/iSarcasmEval ->
  nothing.
- not coverable by any data: HLE, AA-Omniscience, GPQA, MMLU-Pro, and the private 80% of DI 0.3: abstain head and
  calibration only, reported honestly.

---

## 6. Rows added and fit (DERIVED)

Per-row cost DERIVED from the plan's own projection ("about $18-28 for 76-95K rows", plan section 5): $18 / 76K = $0.237
per 1K rows, $28 / 95K = $0.295 per 1K rows (2 epochs, token mean <= 800). At $0.295 per 1K the $30 cap allows about 101K
rows (DERIVED). The plan replaces this projection with C2's measured s/step before GO #1. Block-R mappers must keep the
token mean <= 800; otherwise cost grows with tokens.

Proposed new rows (caps are per dataset; the final size is set from the E1 G-dev measurement, not from this estimate):

| Block | Rows | Make-up |
|---|---|---|
| Block R core (public train, sections 1A-1C general/safety rows) | 12,000 | intent/OOS 3,000 (CLINC150 1,200, MASSIVE 900, HWU64 500, SNIPS 400); dialogue ask/act 1,500 (ABCD 700, MultiWOZ 500, Taskmaster 300); evidence/abstain 2,500 (SciFact 500, Qasper 800, ContractNLI 700, CUAD 500); reasoning/norms 3,800 (WinoGrande 700, CommonsenseQA 400, Social IQa 400, e-CARE 400, QuaRTz 200, QASC 200, StrategyQA 300, ETHICS 600, BoardgameQA 400, FLD 200); safety text 800 (Aya 300, Gandalf-ignore 400, Gandalf-summ 100); low relevance 400 (Civil Comments 200, ESCI 100, ChessBench 100) |
| P1 code realism slices | 5,000 | Juliet 700, DataDog 500, LogChunks 700, FlakeFlagger 200, ManySStuBs4J 400, TSSB-3M 400, SWE-Gym 1,000, CommitPackFT 800, MBPP 300; they count inside their P1 families and enter only if those families pass gates by the freeze |
| New P0 families (critic C1) | 4,000 | T59 promoted 2,000; T60 CONTROL-NEXT 2,000 |
| New P1 heads (critic C3-C7) | 2,500 | T67 IAC-GATE + migration 1,000; T63 EXISTS 500 + licence 200; T66 merge/semver heads 800 |
| Third-party generators (Reasoning Gym, DM Math, bAbI) | 0 net | about 2,000 inside the existing 7K general block; the other 5,000 are the Claude-authored hard extensions of section 4 |
| Benign twins for A17-A19 | 0 net | counted inside T50/T41c sizes |

Without the B2 sets (O1 = NO), block R falls by 3,500 (CLINC150, MASSIVE, ContractNLI, WinoGrande, ChessBench, ESCI,
Civil Comments rows) to about 8,500; the freed rows go to tier A/C caps or are left out (no cut is needed).

Fit (plan: P0 28K + general 7K + voice 3K = 38K new):

| Scenario | New rows | Replay | Total | Cost at $0.237-0.295 per 1K | Fits 60-100K and $30? |
|---|---|---|---|---|---|
| Init C2, replay held at 38K (the plan's 1.0x of 38K) | 38 + 12 + 5 + 4 + 2.5 = 61.5K | 38K | 99.5K | $23.6-29.4 | YES, with almost no room; other P1 families' own generated rows need room taken from block-R caps |
| Init C2, replay scaled 1.0x to all new rows | 61.5K | 61.5K | 123K | $29.2-36.3 | NO at the high rate |
| Init C1, replay held at 57K (1.5x of 38K) | 61.5K | 57K | 118.5K | $28.1-35.0 | NO; needs O13 or an Opus re-size (to reach 100K, 18.5K must go: e.g. all of block R plus most new P1 heads) |
| Init C2, only P0 + general + voice + block R core | 50K | 38K | 88K | $20.9-26.0 | YES |

Recommendation (for Opus, not decided here): fix replay as a COUNT (38K at C2 init), not as a ratio of the new rows, because
block R is itself general-skill data that protects G; start block R at 12K and keep or shrink it on the measured G-dev
result (E1) and the measured s/step; put block R and the general rows after P1 and voice in the shed order (I2). At C1
init the mix does not fit without an owner answer on O13.

---

## 7. Counts

- ALLOW-R5: 41 (tier A 19, tier B2 7, tier C 15).
- OWNER: 13 lines covering about 70 named datasets.
- DENY: about 365 named datasets across the six files (41 + 27 + 52 + 118 + 77 + 50; not de-duplicated).
- Critic gaps placed: 38 (A1-A6, B1-B6, C1-C8, D1-D3, E1-E5, F1-F3, G1, H1-H3, I1-I3), all with a fix and a slot.
- Hardest-question targets: 22 rows (9 P0 families, T59 and T60, 5 P1 families, 6 general/format blocks).
- Rows added (DERIVED): about 23.5K (12K block R + 5K P1 realism + 4K new P0 + 2.5K new P1); about 99.5K total at C2 init
  with replay held at 38K, $23.6-29.4.
