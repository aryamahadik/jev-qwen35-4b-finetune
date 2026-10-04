# RESEARCH: commercial-licence public training data for C (angle: licensed data)

Date: 3 Oct 2026. CPU-only web research. No GPU, Modal, OpenRouter or paid calls.
I downloaded no training data. I read only licence files, dataset cards and metadata. The exceptions are the MTOP zip, opened only to read its LICENSE.txt and count English train lines, and the TRAM label file, used only to count its rows. I opened no eval test split. I did not open any OHS-3, preds_ohs, prep89 or external_quarantine path.

Key:
- (V): licence checked at the upstream source in this session (LICENSE file, official page, Zenodo, figshare or UCI).
- (H): Hugging Face licence tag only.
- SA: share-alike. NC: non-commercial. S: better kept for the sealed new-domains suite (see section 8).
- DI: Jev Decision Index 0.2.1 suite. Its benchmark table is at https://github.com/sinanuozdemir/decision-index/blob/main/docs/suite.md.

---

## 0. Bottom line

1. The ranked list in section 3 has **50 usable datasets**. 5 ranked rows carry an **S** flag (#47-50, plus the hotels half of #40), and 3 unranked extras do too. That leaves 45 ranked rows fully for training. Every licence allows commercial use. SA and caveats are flagged per row.
2. The biggest weaknesses have good licensed fixes:
   - Far domain (software commits; ejs-5 C1 54.1 vs Jev 58.5): **CodeReviewer diff-quality** (CC BY 4.0, real reviewer signal), **CommitChronicle** (10.7M commits, permissive repos only) and **CommitPackFT** (MIT, 702K).
   - Hard yes/no: **CSQA2**, **CREAK**, **StrategyQA**, **PAWS**, plus human minimal pairs from **CAD-SNLI**.
   - Not enough information (NEI) and rules: **ShARC**, **SQuAD 2.0**, **MuSiQue-Full**.
   - Long documents: **QuALITY**, **Qasper**, **DocFinQA**, and the RULER/BABILong generators.
3. **No commercial-licence human dataset with double negation exists outside OHS-1** (ScoNe and This-is-not-a-Dataset are both OHS-1). CondaQA is already in C1. Double negation must come from program transforms of licensed human yes/no items (section 7). Today golden_train has 0.34%, about 1.7K of its 501,732 rows.
4. **C1's replay has licence and contamination problems** (section 2). Fix them before the 60% replay:
   - Yelp: 676 rows under a non-commercial agreement.
   - LogiQA 2.0: 441 rows under CC BY-NC-SA 4.0.
   - Yahoo Answers: 538 rows with unknown licence (Webscope source).
   - MuSR: 298 rows that are **DI test items**. DI scores all 756 MuSR items, and C1 loaded all 3 splits.
   - CaseHOLD: 6,000 golden rows. CaseHOLD is part of LexGLUE, an OHS-1 source dataset per FREEZE.md.
5. **Hugging Face licence tags are often wrong.** I found 5 mismatches against upstream:
   - ContractNLI: HF says CC BY-NC-SA 4.0, official is CC BY 4.0.
   - LogiQA 2.0: HF says MIT, official is CC BY-NC-SA 4.0.
   - FOLIO: HF says MIT, GitHub says CC BY-SA 4.0.
   - QuAC: HF says MIT, official is CC BY-SA 4.0.
   - FeTaQA: HF says MIT, GitHub says CC BY-SA 4.0.

   Longpre et al. 2023 audited dataset hosting sites. They found licence omission of 70%+ and error rates of 50%+ (https://arxiv.org/abs/2310.16787). Rule: always record the upstream licence URL, never the mirror tag.
6. **Tool-calling data:** the big public sets have fine licences but **LLM-made labels** (xLAM, ToolACE, Glaive, Hermes, SPML; When2Call train text is by Mixtral-8x22B). That conflicts with the no-big-teacher rule. Use only their API schemas as option cards, and make the labels with our own programs (section 5).

---

## 1. Method

- Hugging Face: I read API metadata (licence tag, gated flag, split sizes from datasets-server) for about 120 dataset ids.
- GitHub: I read the licence through the `gh` API for about 90 upstream repos. I also read LICENSE.txt files where GitHub returned NOASSERTION.
- Other sources: the official pages for ContractNLI, QuALITY, QuAC, PIQA, UCI, OSHA and ASRS; the Zenodo API (CodeReviewer); the figshare API (Wikipedia Talk Labels); and the Yelp dataset agreement PDF.
- Overlap checks:
  - The DI suite table, linked above.
  - JevBench v1.5.4 THIRD-PARTY.md (`bench/jevbench_v154/THIRD-PARTY.md`). It has 72 original items, 146 router/adequacy items from fstandhartinger/auto-model-router (upstream datasets not named) and 24 held-out items.
  - The OHS lists in the task.
  - Our dev/eval sources, read from `build_data.py`, `build_dev_*.py` and `build_v11_devnc.py` (FORBIDDEN_SOURCE_PAT and SKIPPED_SUBSETS).
  - C1's training sources: `golden_src/MANIFEST.jsonl` (105 golden parts) and the per-source counts of `data/v14_parts/golden_train.jsonl` (501,732 rows).
- My web-search quota ran out partway through. All later checks used direct fetches of primary pages, which is the stronger check anyway.

---

## 2. Problems in what C would replay from C1 (fix first)

| C1 source (rows in golden_train) | Problem | Evidence | Action |
|---|---|---|---|
| `yelp` (303), `yelp5` (373) | **Non-commercial.** Yelp Dataset Agreement: "solely for non-commercial use … You may not … use the Data in connection with any commercial purpose". | https://s3-media3.fl.yelpcdn.com/assets/srv0/engineering_pages/bea5c1e92bf3/assets/vendor/yelp-dataset-agreement.pdf (linked from the HF card of Yelp/yelp_review_full, `license_details: yelp-licence`) | Drop from replay. |
| `logiqa2` (441) | **CC BY-NC-SA 4.0** at the official repo. The HF mirror datatune/LogiQA2.0 wrongly says MIT. `build_ohr.py` itself notes "research licence". | https://github.com/csitfun/LogiQA2.0 (README licence badge) | Drop. |
| `yahoo` (538) | HF licence "unknown". The source is Yahoo! Answers via Webscope (research terms). | https://huggingface.co/datasets/community-datasets/yahoo_answers_topics | Drop unless Webscope terms are confirmed commercial (unlikely). |
| `musr_murder_mysteries` (111), `musr_object_placements` (96), `musr_team_allocation` (91) | **DI test overlap.** `build_ohr.py` loads all 3 splits of TAUR-Lab/MuSR (250 + 256 + 250 = 756 items). DI scores MuSR "All, 756". MuSR has no train split. Licence is fine (CC BY 4.0). | DI suite.md row 32; `build_ohr.py` lines 75-83 | Drop from replay. Do not claim a clean DI MuSR score for C1. |
| `bbh_mistake` (golden, 1,671) | BIG-Bench-Mistake reuses BBH task inputs, and DI scores BBH (5,507). The task differs (find the CoT mistake), but question text overlaps. | DI suite.md row 58 | Keep only after a 12-gram check against BBH. Disclose. |
| `casehold_yn` (golden, 6,000) | CaseHOLD is a LexGLUE task. FREEZE.md lists LexGLUE among the OHS-1 source datasets. Item 12-gram decontam ran, but source-level "unseen" may be broken. | FREEZE.md step 1; golden MANIFEST | Check whether OHS-1 used case_hold. If yes, drop. |
| `mrpc` (632), `rte` (952) | Licence unknown (GLUE card says "other"). | https://huggingface.co/datasets/nyu-mll/glue | Verify or drop (small). |
| `tb_label_nli` (1,288) | tasksource zero-shot-label-nli is a mix of many datasets, licence "other". Some components may be NC. | https://huggingface.co/datasets/tasksource/zero-shot-label-nli | Keep only components with a verified licence. |
| `banking77` (2,300), `clinc150` (2,651) | Our dev sources **and** DI benchmarks. DI uses BANKING77 "All 3,080" (= test) and CLINC "All 5,500". The training split is legal and test-disjoint, but it is in-domain for DI. | DI suite.md rows 4-5 | Keep train only. Disclose. Never add more. |
| `amazon_polarity` (754) | HF says Apache-2.0. The underlying Amazon reviews' terms are not stated. | https://huggingface.co/datasets/fancyzhx/amazon_polarity | Low risk. Keep, with a note. |

---

## 3. Ranked list: 50 usable datasets

Ranking weighs these factors:
- (a) Does it hit a measured weakness (far domain / commits, hard and negated yes/no, NEI, long documents, indirect evidence)?
- (b) Label quality: human or program labels; vote shares are a bonus for KD.
- (c) A clean licence, with no NC (SA is allowed but flagged).
- (d) No overlap with DI, JevBench, OHS or our dev.
- (e) Novelty against C1.

"Exclude" means the split to keep out of training. Hidden test splits need no action.

### 3a. Software commits (far-domain fix for ejs-5)

| # | Dataset | Licence | NC/SA | Train size | Exclude | Overlap / flags | Labels |
|---|---|---|---|---|---|---|---|
| 1 | **CodeReviewer: Diff Quality Estimation** (Microsoft, Li et al. 2022) | CC BY 4.0 (V): https://zenodo.org/records/6900648 | no | about 266K diff hunks (paper figure, verify; file Diff_Quality_Estimation.zip is 2.8 GB); about 1.1K repos, 9 languages (paper figures, verify) | test and valid | Hosted on Zenodo. OHS-3 lists "Zenodo" as a source, so run decontam. **Repo list may include n8n (unknown): content-filter** (section 6). Not on DI or JevBench. | Real human signal: did a reviewer comment on this hunk. Maps to ejs-5 "gate". |
| 2 | **CommitChronicle** (JetBrains) | Card says "other". Only repos under Apache, BSD-3 or MIT; per-commit `license` field (V): https://huggingface.co/datasets/JetBrains-Research/commit-chronicle | no (keep attribution) | 7.66M train (10.7M commits, 11.9K repos, 20 languages, collected 9 Feb 2023) | test 1.49M, validation 1.55M | n8n uses the Sustainable Use License, so it is not in the permissive set. Still drop any repo matching /n8n/i. | Human messages. Program labels for route / triage / score / gate (section 6). |
| 3 | **CommitPackFT** (BigCode) | MIT (H, card): https://huggingface.co/datasets/bigcode/commitpackft | **Filter:** per-sample `license` includes agpl-3.0, lgpl-2.1, mpl-2.0, epl-1.0 and unknown. Keep only mit, apache-2.0, bsd-2/3, isc, cc0, unlicense. | 702,062 single-file commits, 277 languages | none (all train) | Apply the n8n filter. | Program labels from the message (fix / add / refactor / docs …) with the label word hidden. |

### 3b. Hard yes/no, NEI, indirect evidence, logic

| # | Dataset | Licence | NC/SA | Train | Exclude | Overlap / flags | Labels |
|---|---|---|---|---|---|---|---|
| 4 | **CommonsenseQA 2.0 (CSQA2)** | CC BY 4.0 (V): https://github.com/allenai/csqa2/blob/master/LICENSE | no | 9,282 | test 2,517 (no answers); dev 2,544 can join our dev | none | Players wrote yes/no questions that fooled T5; human-validated. Hard yes/no. |
| 5 | **ShARC** | CC BY-SA 3.0 (H): https://huggingface.co/datasets/UCLNLP/sharc | SA | 21,890 | test hidden; dev 2,270 | none | Human. Applies government rule text to a user scenario: Yes / No / Irrelevant / ask follow-up. Policy application + NEI. |
| 6 | **CREAK** | MIT (V): https://github.com/yasumasaonoe/creak/blob/main/LICENSE.txt | no | 10,176 | test hidden; dev 1,371; contrast set (500) for eval only | none | Crowd-written true/false entity claims. |
| 7 | **StrategyQA** | MIT (V): https://github.com/eladsegal/strategyqa/blob/main/LICENSE | no | 2,290 | test 490 (hidden) | none | Implicit multi-hop yes/no with evidence paragraphs. Indirect evidence. |
| 8 | **SQuAD 2.0** (as "does the passage answer this?") | CC BY-SA 4.0 (H): https://huggingface.co/datasets/rajpurkar/squad_v2 | SA | 130,319 (about 43K unanswerable) | dev 11,873; test hidden | QNLI (in C1) comes from SQuAD 1.1 passages: dedupe by passage | Human. Program turns it into an answerable / NEI decision. |
| 9 | **MuSiQue** (Ans + Full) | CC BY 4.0 (V): https://github.com/StonyBrookNLP/musique/blob/main/LICENSE | no | 19,938 answerable; Full adds unanswerable contrast twins | test hidden | Hops come from HotpotQA/2Wiki: dedupe against C1's hotpotqa_yesno | Human-checked composition. Multi-hop + NEI. |
| 10 | **WANLI** | CC BY 4.0 (H): https://huggingface.co/datasets/alisawuffles/WANLI | no | 102,885 | test 5,000 | MNLI-seeded | GPT-3 wrote the pairs; crowdworkers revised and labelled them. Labels are human. Disclose LLM text. |
| 11 | **CAD-SNLI** (counterfactually augmented, Kaushik et al. 2020) | Apache-2.0 (V): https://github.com/acmi-lab/counterfactually-augmented-data/blob/master/LICENSE; SNLI text is CC BY-SA 4.0 | SA (via SNLI) | about 8.3K train pairs (paper) | test | SNLI | Human minimal edits that flip the label. Real fact-flip twins. |
| 12 | **δ-NLI** (defeasible inference) | MIT (V): https://github.com/rudinger/defeasible-nli/blob/main/LICENSE. Premises come from SNLI and Social-Chem-101 (both CC BY-SA 4.0) and ATOMIC. | SA (parts) | 200,692 (atomic 35,002; snli 88,674; social 77,016; HF tasksource mirror) | test (4,138 / 1,837 / 9,439) | The social part shares situations with sc101 in C1: dedupe | Crowd. "Does this update strengthen or weaken the claim?" Indirect evidence. |
| 13 | **PAWS-Wiki** | Google: "may be freely used for any purpose" (V): https://github.com/google-research-datasets/paws/blob/master/LICENSE | no (Wikipedia text underneath) | 49,401 | test 8,000; dev 8,000 | MRPC (C1) is a different dataset | Human. Same words, different meaning: close distractors. |
| 14 | **FOLIO** | CC BY-SA 4.0 (V): https://github.com/Yale-LILY/FOLIO/blob/main/LICENSE (the HF mirror says MIT; use GitHub) | SA | about 1.0K | test not public; validation about 200 | none | Expert-written, FOL-checked True / False / Unknown. |
| 15 | **2WikiMultihopQA** | Apache-2.0 (V): https://github.com/Alab-NII/2wikimultihop/blob/main/LICENSE | no | 167,454 | dev 12,576; test 12,576 | Wikipedia / Wikidata | Template + Wikidata. Comparison yes/no. Nearly program-labelled. |
| 16 | **FEVER** | CC BY-SA 3.0 + Wikipedia terms (H): https://huggingface.co/datasets/fever/fever; https://fever.ai/dataset/fever.html | SA | 145,449 claims | test 19,998 | **VitaminC (OHS-1)** shares Wikipedia sentences and claim style: strict 12-gram decontam. FEVEROUS is already in C1. | Crowd. Supports / Refutes / NEI. |
| 17 | **SciTail** | Apache-2.0 (V): https://github.com/allenai/scitail/blob/main/LICENSE | no | 23,596 | test 2,126 | Built from school science questions. DI scores ARC test: run a 12-gram check against ARC. | Crowd. |

### 3c. Long documents

| # | Dataset | Licence | NC/SA | Train | Exclude | Overlap / flags | Labels |
|---|---|---|---|---|---|---|---|
| 18 | **QuALITY** | CC BY 4.0 (V): https://nyu-mll.github.io/quality/ (the GitHub repo has no LICENSE; each article has a `license` field) | no | 2,523 questions (articles average about 5K tokens) | test hidden; dev 2,086 | none (not in LongBench v2) | Human writers + speed validators; has a hard subset. |
| 19 | **Qasper** | CC BY 4.0 (H): https://huggingface.co/datasets/allenai/qasper | no | 888 papers (about 2.6K questions) | test 416 papers | Papers are 2020 or earlier; OHS-1 has "arXiv 2026", so no date overlap. | NLP practitioners. Yes/no + unanswerable over full papers. |
| 20 | **DocFinQA** | MIT (H): https://huggingface.co/datasets/kensho/DocFinQA | no | 5,735 | test 922 | Built on FinQA (C1 used the FinQA train split; keep the same split) | Expert / program numeric answers. Convert to threshold or choice decisions. Very long SEC filings. |
| 21 | **RULER + BABILong generators** | Apache-2.0 (V): https://github.com/NVIDIA/RULER/blob/main/LICENSE, https://github.com/booydar/babilong/blob/main/LICENSE. BABILong uses PG-19 (Apache-2.0) and bAbI (BSD). | no | unlimited (program) | Do not train on their published benchmark configs; use our own seeds and lengths. | Both are long-context **eval** suites: never report them as clean after this. | Program labels at any length up to 8K+ tokens. |
| 22 | **DROP** | CC BY-SA 4.0 (H): https://huggingface.co/datasets/ucinlp/drop | SA | 77,400 | validation 9,535; test hidden | none | Crowd. Numbers over passages. |

### 3d. Tables, numbers, rules, risk

| # | Dataset | Licence | NC/SA | Train | Exclude | Overlap / flags | Labels |
|---|---|---|---|---|---|---|---|
| 23 | **UCI Car Evaluation + Nursery** | CC BY 4.0. Car Evaluation checked on its UCI page (V): https://archive.ics.uci.edu/dataset/19/car+evaluation. Nursery uses the UCI default, still to verify: https://archive.ics.uci.edu/dataset/76/nursery | no | 1,728 + 12,960 | none | none | Labels **come from published DEX hierarchical decision rules**: exact rule-composition tasks. |
| 24 | **UCI credit risk** (Default of Credit Card Clients, Statlog German Credit) | CC BY 4.0 (UCI): https://archive.ics.uci.edu/dataset/350, https://archive.ics.uci.edu/dataset/144 | no | 30,000; 1,000 | none (make our own) | Adult is already in C1 (binj_adult) | Real outcomes. Noisy (high Bayes error): use calibrated or soft targets. |
| 25 | **HybridQA** | MIT (V): https://github.com/wenhuchen/HybridQA/blob/master/LICENSE | no | 62,682 | test 3,463 | Wikipedia tables: 12-gram decontam against **TabFact (OHS-2)** | Human. |
| 26 | **WikiSQL** (execute the SQL to get answers) | BSD-3 (V): https://github.com/salesforce/WikiSQL/blob/master/LICENSE | no | 56,355 | test 15,878 | Wikipedia tables: decontam against TabFact | **Program labels** from SQL execution (for example "is the count above 3?"). |
| 27 | **MultiHiertt** | MIT (V): https://github.com/psunlpgroup/MultiHiertt/blob/main/LICENSE | no | 7,830 | test 1,566 | Finance; FinQA-adjacent | Expert. |
| 28 | **ConvFinQA** | MIT (V): https://github.com/czyssrs/ConvFinQA/blob/main/LICENSE | no | 3,037 conversations | test 434 | Same filings as FinQA (C1): keep the FinQA split | Expert. Multi-turn state tracking over numbers. |
| 29 | **OSHA Severe Injury Reports** | US federal work, public domain (17 U.S.C. §105); the page states no extra terms: https://www.osha.gov/severe-injury-reports | no | 1 Jan 2015 to 30 Nov 2025 (record count not stated) | none | Same OIICS code book as C1's oiics_event (NIOSH), but new narratives | Coded by OSHA staff: severity (hospitalised / amputation / eye), event, nature, body part. |

### 3e. Norms, safety, moderation (soft labels)

| # | Dataset | Licence | NC/SA | Train | Exclude | Overlap / flags | Labels |
|---|---|---|---|---|---|---|---|
| 30 | **Scruples** (Anecdotes + Dilemmas) | Apache-2.0 (V): https://github.com/allenai/scruples/blob/master/LICENSE | no (Reddit text) | 27,766 + 8,000 (paper) | test 2,500 / 1,000 | Moral Stories (OHS-2) is different; moral norms is the family where Jev led on OHS-2 | **Community vote distributions: soft KD targets.** |
| 31 | **Measuring Hate Speech** (UC Berkeley D-Lab) | CC BY 4.0 (H): https://huggingface.co/datasets/ucberkeley-dlab/measuring-hate-speech | no | 135,556 annotations on 39,565 comments | no split: make one and hold out 10% | HateCheck (OHS-1) is different | IRT hate score + per-annotator labels: ordinal and soft. |
| 32 | **Wikipedia Talk Labels** (personal attacks, toxicity, aggression) | CC0 (V, figshare API): https://figshare.com/articles/dataset/Wikipedia_Talk_Labels_Personal_Attacks/4054689 (and 4563973) | no (comments are CC BY-SA Wikipedia text) | 115,864 (attack), 159,686 (toxicity) comments, about 10 raters each | rows with `split = test` | civil_comments (C1) is a different source | Crowd vote shares. |
| 33 | **ProsocialDialog** | CC BY 4.0 (H): https://huggingface.co/datasets/allenai/prosocial-dialog | no | 120,236 rows | test 25,029 | none | GPT-3 contexts with human safety labels on 5 levels (casual … needs intervention): ordinal risk. |
| 34 | **ETHICS** | MIT (H): https://huggingface.co/datasets/hendrycks/ethics | no | about 96K across 5 configs | test and test-hard | The AITA part overlaps Scruples sources: dedupe | Crowd. |
| 35 | **DynaHate** | CC BY 4.0 (README): https://github.com/bvidgen/Dynamically-Generated-Hate-Speech-Dataset | no | 41,144 | rows with the test split | Same authors as HateCheck (OHS-1): decontam its templates | Human adversarial items. |
| 36 | **HateXplain** | MIT (V): https://github.com/hate-alert/HateXplain/blob/master/LICENSE | no (tweets/Gab text) | 15,383 | test 1,924 | none | 3 raters each: soft. |
| 37 | **Aegis 2.0** (expand C1's 2,451 rows) | CC BY 4.0 (H): https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0 | no | 30,007 | test 1,964 | already a C1 source (more rows) | Human, 13 risk categories + safe. |
| 38 | **HH-RLHF red-team attempts** | MIT (H): https://huggingface.co/datasets/Anthropic/hh-rlhf | no | 38,961 transcripts | main config test 8,552 | none | Red-teamer self-rating of attack success (0-4): ordinal risk. |

### 3f. Intent routing, commonsense, stance, sentiment, figurative

| # | Dataset | Licence | NC/SA | Train | Exclude | Overlap / flags | Labels |
|---|---|---|---|---|---|---|---|
| 39 | **MTOP (English)** | CC BY-SA 4.0 (V, LICENSE.txt inside https://dl.fbaipublicfiles.com/mtop/mtop.zip) | SA | 15,666 | test 4,386; eval 2,235 | Same TOP family as TOPv2 (C1): dedupe. Not on DI. | Expert. 11 domains, 117 intents, 78 slots. |
| 40 | **NLU++** | CC BY 4.0 (V): https://github.com/PolyAI-LDN/task-specific-datasets/blob/master/LICENSE | no | 3,080 (banking 2,071 / 48 intents; hotels 1,009 / 40 intents) | no official split | The repo also holds BANKING77 (our dev, DI). **Banking half: domain-adjacent to dev. Hotels half: S.** | Expert, multi-label. |
| 41 | **PIQA** | AFL-3.0 (V): https://yonatanbisk.com/piqa/ | no | 16,113 | test 3,084 (hidden) | none | Crowd. |
| 42 | **Social IQa** | CC BY 4.0 (H, card text): https://huggingface.co/datasets/allenai/social_i_qa | no | 33,410 | test hidden; dev 1,954 | none | Crowd. |
| 43 | **CosmosQA** | CC BY 4.0 (H): https://huggingface.co/datasets/allenai/cosmos_qa | no | 25,262 | test 6,963 (hidden) | none | Crowd. |
| 44 | **e-CARE** | MIT (V): https://github.com/Waste-Wood/e-CARE/blob/main/LICENSE | no | about 14.9K | test | COPA-style (COPA is in C1) | Crowd. Causal choice. |
| 45 | **args.me** | CC BY 4.0 (H): https://huggingface.co/datasets/webis/args_me | no | 387,606 arguments | no split | Debate-portal text | Pro/con from portal structure (author-assigned). |
| 46 | **DynaSent, Round 2 only** | CC BY 4.0 (card): https://huggingface.co/datasets/dynabench/dynasent | no | 13,065 (R2 train) | test 720 | **Round 1 sentences are taken from the Yelp Academic Dataset (per the DynaSent paper): skip R1 (Yelp non-commercial).** | 5 crowd votes each: soft targets. |
| 47 | **FLUTE** (figurative NLI: sarcasm, simile, metaphor, idiom) | AFL-3.0 (H): https://huggingface.co/datasets/ColumbiaNLP/FLUTE | no | 7,534 | none published | iSarcasmEval (DI) is different; TweetEval irony is our dev | GPT-3 drafts + expert edits; label by construction. **S** |
| 48 | **PUBHEALTH** | MIT (V): https://github.com/neemakot/Health-Fact-Checking/blob/master/LICENSE | no | 9,832 | test 1,235 | Not PubMedQA (OHS-1) or SciFact (OHS-2) | Fact-checker verdicts (true / false / mixture / unproven). **S** |
| 49 | **RumourEval 2019** | CC BY 4.0 (H): https://huggingface.co/datasets/strombergnlp/rumoureval_2019 | no (tweet/Reddit text; platform terms) | 4,879 | test 1,675 | none | Crowd. Support / deny / query / comment. **S** |
| 50 | **MITRE TRAM** (ATT&CK technique per sentence) | Apache-2.0 (V): https://github.com/center-for-threat-informed-defense/tram/blob/main/LICENSE.txt | no (report text from security vendors) | 5,089 single-label sentences, 50 techniques (I counted this); plus multi_label.json | no split | NVD (OHS-3) is a different source | Human. Security routing. **S** |

Also usable, with lower value or with caveats (not ranked):
- Commonsense and QA:
  - OpenBookQA, Apache-2.0 (V), 4,957 train.
  - αNLI/ART, Apache-2.0 (V), 169,654 train. Built on ROCStories, whose terms are unclear.
  - SWAG, MIT (V), 73,546 train. Partly LSMDC movie text with research terms.
  - Quoref, CC BY 4.0 (H).
  - Natural Questions, CC BY-SA 3.0 (H), 307K train. Document-level NEI.
  - TyDi QA, Apache-2.0 (H).
- Tables and SQL:
  - SQA, MS-PL (H), 6,066 sequences.
  - Spider, CC BY-SA 4.0 (H), 7,000 train. Program labels via SQL.
- Documents and dialogue:
  - MultiDoc2Dial, Apache-2.0 (V). **S**
  - UCI Bank Marketing, CC BY 4.0, 45,211. **S**
  - UCI Diabetes 130-US, CC BY 4.0 (V), 101,766. **S**
- Intent and preference:
  - Bitext customer support, CDLA-Sharing-1.0 (H), 26,872 rows. Synthetic, share-alike.
  - HINT3, ODbL + DbCL (V). Database share-alike.
  - lmarena arena-human-preference-55k, Apache-2.0 (H), 57,477 human votes. Contains commercial-LLM outputs; JevBench adequacy-adjacent.
- Sarcasm and NLI:
  - MUStARD, MIT (V), 690 items.
  - SARC, MIT code (V). Reddit text; labels from the "/s" marker.
  - SNLI, CC BY-SA 4.0 (H), 550,152 train. Low novelty next to MNLI.

---

## 4. DI-adjacent training splits (legal, but in-domain for a DI benchmark)

Use these only with a cap. Disclose them, and report DI scores both with and without these benchmarks.

| Dataset | Licence | Train | DI uses | Note |
|---|---|---|---|---|
| When2Call | CC BY 4.0 (H): https://huggingface.co/datasets/nvidia/When2Call | train_sft 15,000; train_pref 9,000 | test MCQ 3,652 | Train is built from xLAM-60k. Question variants were written by **Mixtral-8x22B** (README). The category (call / ask / unable / answer) comes from the construction. That clashes with the no-big-teacher rule for text; see section 5. |
| HoVer | CC BY-SA 4.0 (H) | 18,171 | dev 4,000 | SA. Multi-hop claim verification. |
| Amazon ESCI | Apache-2.0 (V): https://github.com/amazon-science/esci-data/blob/main/LICENSE | 2,027,874 rows (tasksource mirror) | stratified 5,000 | Product relevance E / S / C / I. |
| GSM8K | MIT (H) | 7,473 | test | Convert to threshold decisions. |
| HellaSwag | MIT (H) | 39,905 | validation 10,042 | **The GitHub repo rowanz/hellaswag was DMCA-blocked on 14 Sep 2026 over wikiHow text** (https://github.com/github/dmca/blob/master/2026/09/2026-09-14-wikihow.md). Avoid. |
| WinoGrande, RAGTruth, ARC, BANKING77, CLINC150 | already in C1 | | validation / test / all | Keep as is; add nothing. |
| ContractNLI | CC BY 4.0 (V): https://stanfordnlp.github.io/contract-nli/ | 607 NDAs | test 123 | **Exclude:** DI test **and** LegalBench (OHS-1) contract_nli tasks. |

---

## 5. Tool calling / when-to-call: licence OK, labels not OK

| Dataset | Licence | Size | Who made the labels |
|---|---|---|---|
| Salesforce xlam-function-calling-60k | CC BY 4.0 (H), gated | 60,000 | APIGen pipeline: LLM generation plus format, execution and semantic checks |
| MadeAgents xlam-irrelevance-7.5k | CC BY 4.0 (H) | 7,500 | derived from xLAM (LLM) |
| Team-ACE ToolACE | Apache-2.0 (H) | 11,300 | LLM pipeline; the card says "rule-based and model-based checks" |
| glaiveai glaive-function-calling-v2 | Apache-2.0 (H) | 112,960 | synthetic (model not stated) |
| NousResearch hermes-function-calling-v1 | Apache-2.0 (H) | about 11.5K across 5 configs | synthetic |
| ibm-research nestful | Apache-2.0 (H) | 1,861 | eval-sized |
| reshabhs SPML prompt injection | MIT (H) | 16,012 | **GPT-4** wrote the system prompts and attacks (card); label by construction. Provider terms may restrict use: needs a legal check. |
| Salesforce APIGen-MT-5k | **CC BY-NC 4.0** | 5,000 | exclude |

Recommendation:
- Use only the **API catalogs** (function names, descriptions and parameter schemas) as option cards.
- Our programs then build the decision rows:
  - The query fills one tool's required parameters: gold = that tool.
  - A required parameter is missing: gold = ask.
  - No tool fits: gold = unable.
  - The question is answerable without a tool: gold = answer.
- This copies When2Call's construction without a big teacher.
- BFCL, API-Bank, ToolRet and RouterBench are DI eval-only: never use them.

---

## 6. Commit data: label recipes and the n8n guard

ejs-5 has 868 rows over 622 n8n commits (from `bench/ejs5/README.md`): route 180, triage 148, score 360, gate 180. Matching licensed sources:

- **route** (CommitChronicle): the area or package from the top-level changed path. Show the diff body and the message; hide the file headers.
- **triage** (CommitChronicle, CommitPackFT): the conventional-commit type from the message prefix (feat, fix, docs, refactor, perf, test, build, ci, chore, revert). Strip the prefix from the shown message.
- **score** (CommitChronicle): an ordinal size or risk from lines and files changed, plus sensitive paths (lockfiles, migrations, auth, CI config).
- **gate**:
  - CodeReviewer's "reviewer commented on this hunk" label.
  - "Later reverted" in CommitChronicle history: a later commit with `Revert "<subject>"` / `This reverts commit <sha>` means hold.
- **Dev split by repo** (unseen repos), never by commit.

n8n guard (ejs-5 is n8n; we never train on n8n):
1. Drop any repo whose name matches `/n8n/i`, including forks.
2. Content filter on diffs and paths: `packages/nodes-base`, `packages/workflow`, `packages/core`, `n8n-workflow`, `n8n-core`, `INodeType`, `INodeExecutionData`.
3. Add ejs-5 states to `held_out_grams` with a counts-only script that hashes 12-grams and never prints item text. This follows the ejs-5 kit rules.
4. CodeReviewer may lack a repo field (unknown). For it, steps 2 and 3 are the only guard.

---

## 7. Hard and negated yes/no from licensed human items (program labels)

Licensed human negation sets are either OHS-1 (ScoNe, This-is-not-a-Dataset) or already in C1 (CondaQA, Apache-2.0). Build the rest by program from human gold:

Base items:
- CSQA2: 9,282
- CREAK: 10,176
- StrategyQA: 2,290
- ShARC yes/no turns
- SQuAD 2.0 answerability: 130K
- PAWS: 49K
- BoolQ (already in C1)

Transforms:

| Transform | Label rule |
|---|---|
| Negated question | flips |
| Double negation ("Is it not the case that X is not …") | unchanged |
| Negated-evidence twin (CAD-style; human pairs from #11) | flips |
| Evidence-deleted twin | NEI, or "no" under a closed-world card |

Use the existing `complement` / `equiv` relations in train_decoder.py.

Current level: golden_train had 0.34% double-negation rows (about 1.7K of 501,732), and C1 flips 8.9% of double negations. Several thousand such rows are cheap with these sources.

---

## 8. Sealed new-domains suite: candidates (never train on these)

These are licensed, have decision-shaped labels, and fit none of C1's families closely:
- ASRS aviation incident reports, coded by NASA analysts. US government data; the page states no terms; export capped at 10K per search (https://asrs.arc.nasa.gov/search/database.html).
- MultiDoc2Dial (government service documents).
- NLU++ hotels half.
- RumourEval 2019.
- FLUTE.
- PUBHEALTH.
- MITRE TRAM.
- UCI Diabetes 130-US.
- UCI Bank Marketing.
- CommitChronicle repos in 2 held-out languages (for example Rust and Swift), for software.

Pick about 10, take about 200 items each (about 2,000 total), and remove those sources from every training mix.

---

## 9. Excluded

**Non-commercial (verified this session):**

| Dataset | Licence | Other notes |
|---|---|---|
| Financial PhraseBank | CC BY-NC-SA 3.0 (H) | also our dev_nc source |
| gtfintechlab FOMC | CC BY-NC 4.0 | |
| CommitBench | CC BY-NC 4.0 | |
| APIGen-MT-5k | CC BY-NC 4.0 | |
| Tobi-Bueck customer-support-tickets | CC BY-NC 4.0 | |
| climatebert climate_* | CC BY-NC-SA 4.0 | also our dev |
| SciQ | CC BY-NC 3.0 | |
| QuanTemp | CC BY-NC 4.0 (README) | |
| FinanceBench | CC BY-NC 4.0 | |
| LogiQA 2.0 | CC BY-NC-SA 4.0 | |
| ANLI | CC BY-NC 4.0 | also DI test |
| All Yelp-derived text | Yelp agreement | |
| SLURP audio | CC BY-NC 4.0 | the text is CC BY 4.0, but see below |

**Licence unknown or unclear:**
- No licence stated: Climate-FEVER; MC-TACO; Com2Sense; WIQA; AmbiFC; SPIRS; WT-WT; ApacheJIT; ACID.
- Perspectrum: "Creative Commons", version not stated.
- SST-2, Rotten Tomatoes, TweetEval: HF says "unknown". All three are also our dev.
- IMDb: HF says "other". It is also our eval.
- Yahoo Answers Topics: HF says "unknown".
- FinGPT sentiment, auditor_sentiment: no licence, and built on FPB.
- TimKoornstra financial tweets: MIT tag, but aggregated, so it may contain FPB or TFNS.
- PatchDB: HF says Apache-2.0, but download is gated with an agreement ("copyright … owned by SunLab"). Its NVD-based part overlaps OHS-3.
- Devign / CodeXGLUE defect: C-UDA, over GPL/LGPL code. Needs a legal check.

**Eval, dev or C1 overlap:**
- LegalBench family (OHS-1): CUAD (CC BY 4.0), MAUD, ContractNLI, PrivacyQA, OPP-115, Unfair-ToS.
- LexGLUE (OHS-1 per FREEZE.md): CaseHOLD, ECtHR, SCOTUS, EUR-LEX, LEDGAR.
- SufficientFacts (MIT): contains a VitaminC-based part (OHS-1).
- CVEfixes, BigVul, MoreFixes: NVD (OHS-3).
- SLURP and HWU64: MASSIVE (in C1) is a translation of SLURP, so these are near-duplicates.
- IBM Claim Stance (CC BY 3.0): same IBM Debater topics as IBM ArgQ (OHS-2).
- SMS Spam (CC BY 4.0) and Twitter Financial News Sentiment (MIT): both are our eval sources in `build_data.py`. Skip TFN Topic too (same tweet pool).
- Our dev/eval sources, found in the builders:
  - Topic and news: AG News, BBC News, CapSOTU, Manifesto.
  - Sentiment and emotion: Rotten Tomatoes, IMDb, dair-ai emotion, SST, TweetEval (hate, irony, sentiment), climatebert, app_reviews.
  - Spam: Enron spam, Deysi spam.
  - NLI, faithfulness and dialogue: SuperGLUE CB, TrueTeacher, EmpatheticDialogues.
  - Bias and finance: Social Bias Frames, Financial PhraseBank.
  - Intent: BANKING77, CLINC150.
- DI eval-only:
  - Language and NLI: VAST, ACOS, FinEntity, iSarcasmEval, NLI4CT, CLadder.
  - Tools and retrieval: BFCL, API-Bank, ToolRet, RouterBench, BRIGHT, PhishNChips.
  - Knowledge and reasoning: SATA-Bench, CRUXEval, GPQA, MMLU, MMLU-Pro, HLE, BBH, MuSR, SimpleBench, ChessBench.
  - Arts and taste: ForecastBench, Habermas Machine, New Yorker, Humicroedit, POP909, cfcolor, BPoMP, the home-appliance simulator.
- JevBench: no named public dataset is a source. The 146 router/adequacy items come from auto-model-router with upstream datasets not named, so keep the 12-gram decontam.

---

## 10. Licence hygiene for the private sources file

1. Per source, record the upstream licence URL **and** the commit or record id. Never rely on the HF tag alone.
2. Keep the per-row `meta.licence` field (the golden builder already has it). Drop any row with NC or unknown at build time.
3. CC BY and Apache-2.0 require attribution or NOTICE, so keep an ATTRIBUTION list.
4. SA sources (CC BY-SA, ODbL, CDLA-Sharing): fine for private training. Never publish rows derived from them. Whether trained weights count as "adapted material" is legally unsettled, so keep the list.
5. Platform-text caveats (Reddit, X/Twitter, YouTube) apply to Scruples, ETHICS (AITA part), Measuring Hate Speech, HateXplain, RumourEval and SARC. Licence-wise they are low risk for training; record them anyway.
6. Decontam every new source against OHS-1/2/3, JevBench public, ejs-5 (hashed) and the DI tests (hashed, counts-only).

---

## 11. Open items (unknown, verify before use)

- CodeReviewer diff-quality: the exact train size, whether rows carry a repo field, and how repos were chosen (licence filter unknown).
- CommitChronicle: whether the train/test split is by repo (unknown; split by repo ourselves anyway).
- UCI licences for German Credit, Default of Credit Card Clients, Nursery and Bank Marketing (UCI default is CC BY 4.0; I checked the Car Evaluation, Diabetes 130 and SMS pages).
- Exact sizes for Scruples, e-CARE, CAD-SNLI and FOLIO (taken from the papers).
- Whether OHS-1 used LexGLUE's case_hold. This decides the fate of the 6,000 casehold_yn rows.
- Whether Aegis 2.0 labels had any LLM assistance (unknown).
