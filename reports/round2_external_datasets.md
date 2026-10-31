# Round 2: external public datasets for 8 families (7 Oct 2026)

Scope: F1, F2, F6, F8, F10, F12, F13 and COMMIT (C_DATA_SPEC v4 section 2.2 / 4). Method: about 20 web searches, 3 page
fetches, and licence fields read from GitHub, Hugging Face and Zenodo APIs. Every candidate name (and its known parents)
was run through `c_src/common/denylist.py check` (hit / no-hit only). No sealed, OHS-3, bench or Jev file was opened.

Legend. Licence: **C** = commercial use OK; **NC/RO** = non-commercial or research-only; **?** = no licence record
found. Labels: **P** = program, **H** = human, **L** = LLM. Effort is a rough estimate of one builder agent's time,
including the licence record, deny-list and G13: Low = about 0.5 day, Med = 1-2 days, High = 3 or more days.

**Read first: two rule conflicts.**
1. The owner says NC is fine (model not commercial), but spec 3.1 says NC or research-only data is "study only, never
   a training row". NC rows need a PREREG/spec amendment before they enter a mix. NC sets are marked below.
2. Spec 3.1 also says a creator's own HF card is not an official licence record ("unverified means out"). Sets whose
   only licence record is an HF card are marked "(HF card)".

## Deny-list results (names and parents, run 7 Oct)

| Verdict | Datasets |
|---|---|
| **DENY** (taint) | WinoDict (parent WinoGrande = Decision Index test), QuAIL, AQuA-RAT, MathQA, DocNLI (and ANLI), TRAM (parent MC-TACO, forbidden), API-Bank (DI test), BIG-bench, LogicBench / Multi-LogiEval, LogicNLI, CLUTRR / PARARULE-Plus, FewRel, SciFact |
| **No new rows** (already used in C1) | ProofWriter / RuleTaker, ABCD, STAR, MultiWOZ, Taskmaster 1-3, MultiNERD; MedQA (a parent of some MedCalc-Bench notes) |
| **Pass** | every other dataset named below |

Also out by spec 3.G, so they were not re-checked: When2Call, xLAM, ToolACE, Glaive, Hermes FC (LLM-written);
LegalBench / LexGLUE family (this includes SARA statute reasoning); CUAD, ContractNLI, PrivacyQA / OPP-115 (and so
PolicyQA); SNLI and FEVER derivatives; GSM8K, ESCI, HoVer; CodeReviewer. LongBench v2 is sealed and must never be used.

## F1 Policy composition and precedence

| Dataset | Link | Size | Licence | Labels | Fit (skill / format) | Effort | Overlap risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| BoardgameQA | [zip](https://storage.googleapis.com/gresearch/BoardgameQA/BoardgameQA.zip), [paper](https://arxiv.org/abs/2306.07934) | 1K train / 500 val / 1K test per variation; many variations (depth, conflicts, distractors, missing info) | CC BY 4.0 (paper) **C** | P (defeasible solver), balanced labels | Facts, conflicting rules and **pairwise rule preferences**, with gold proved / disproved / unknown. This is exactly precedence. Native 3-way choice; yes/no is easy | Low | Pass. Its test split is used in BIG-Bench Extra Hard: use train only | **Take** (best F1 match) |
| RuleArena | [GitHub](https://github.com/skyriver-2000/RuleArena) | 816 problems (airline 300, NBA 216, tax 300); real rules of about 377 tokens each | MIT **C** | P (reference calculators) | Real airline baggage, NBA salary-cap and US tax rules: fee / eligibility. F1 and F2. Yes/no thresholds and value choice | Med | Pass. It is a benchmark with no train split: run their calculators on **new** cases instead of copying the 816 | **Take** as rule cards plus a case generator |
| ConditionalQA | [GitHub](https://github.com/haitian-sun/ConditionalQA), [paper](https://arxiv.org/abs/2110.06884) | 3,102 Q on 436 gov.uk documents (test answers hidden) | README says "ONLY for NLP research"; no licence file. **RO** (document text gov.uk, OGL v3) | H (trained annotators) | Eligibility yes/no that depends on conditions; not-answerable questions; long policy pages (F1, F6 and F13) | Med | Pass | **Take if** the NC/RO amendment is signed |
| tau-bench policies | [GitHub](https://github.com/sierra-research/tau-bench) | 2 domains, about 165 tasks | MIT **C** | Mixed. User turns are LLM-simulated (flag) | Airline and retail policy documents | Low | Pass. Well-known agent benchmark | Card seeds only, no rows |

## F2 Rule arithmetic, money, quantities, dates

| Dataset | Link | Size | Licence | Labels | Fit | Effort | Overlap risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| RuleArena | see F1 | 816 problems | MIT **C** | P | Fee, cap and tax arithmetic under real rules | Med | as F1 | **Take** (generator) |
| MedCalc-Bench | [HF](https://huggingface.co/datasets/ncbi/MedCalc-Bench), [GitHub](https://github.com/ncbi-nlp/MedCalc-Bench) | 10,053 train / 1,047 test; 55 calculators | CC BY-SA 4.0 (README, based on the authors' own reasoning) **C/SA**. Notes come from PMC-Patients (NC-SA), MedQA and TREC: partly **NC** | P (calculator code), but labels have **known errors** (see the [Verified fork](https://github.com/nikhilk7153/MedCalc-Bench-Verified) and [label audit](https://github.com/junzeye/validate-medcalc-labels)) | Equation calculators (dosing, GFR, date rules such as due dates): threshold yes/no and value-bin choice. F2 and F8 | Med | Pass. Parent MedQA is already used, so drop MedQA-sourced notes. Popular benchmark: train only | **Take**, but only with re-verified labels and no MedQA notes |
| Test of Time (arithmetic) | [HF](https://huggingface.co/datasets/baharef/ToT) | 2,800 arithmetic (test only) | CC BY 4.0 **C** | P | Date, duration and time-zone arithmetic | Low | Pass, but it is test-only, and the spec forbids benchmark test items | Use the idea only, not rows |
| TAT-DQA | [HF](https://huggingface.co/datasets/next-tat/TAT-DQA) | 16,558 Q, 2,758 one-page financial documents (about 80% train) | CC BY 4.0 (HF card) **C?** | H | Numeric questions on real reports. Thresholds as yes/no | Med | Pass. Sibling of TAT-QA, which is already in replay: dedupe by report | Maybe |

## F6 Not enough information / abstain as gold

| Dataset | Link | Size | Licence | Labels | Fit | Effort | Overlap risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| BoardgameQA ("unknown" class) | see F1 | 1/3 of rows are unknown | CC BY 4.0 **C** | P | Gold NEI on half-proved theories. Card semantics are explicit | Low | as F1 | **Take** |
| FLD.v2 | [HF](https://huggingface.co/datasets/hitachi-nlp/FLD.v2), [code](https://github.com/hitachi-nlp/FLD) | 30K train | Code Apache-2.0; data licence **not stated (?)** | P (prover) | Proved / disproved / unknown with distractor facts (F6 and F4) | Low | Pass. F4 already copies FLD's idea (own implementation), so it adds little new style | Maybe (licence unverified) |
| ConditionalQA (not-answerable) | see F1 | part of 3,102 | **RO** | H | Real NEI on long policy pages | Med | Pass | **Take if** amended |
| IIRC | [paper](https://arxiv.org/abs/2011.07127) | about 13K Q, many unanswerable | **?** (the AI2 data page now redirects to the paper) | H | Answer needs a linked page that is not given, so NEI | Med | Pass. Wikipedia text: page-split against SQuAD, MuSiQue and 2Wiki | Maybe (licence) |

## F8 Risk and probability (spec: no real-outcome labels)

| Dataset | Link | Size | Licence | Labels | Fit | Effort | Overlap risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| MedCalc-Bench, points-score subset | see F2 | the rule-based calculators (for example CHA2DS2-VASc, HAS-BLED, Wells, CURB-65, Centor, HEART) | as F2 | P (noisy, re-verify) | **A card-defined points table, then a risk tier.** This is F8's exact skill. Hard 0/1 yes/no plus tier choice | Med | as F2 | **Take** (same build as F2) |
| QUITE | [GitHub](https://github.com/boschresearch/quite-emnlp24), [paper](https://arxiv.org/abs/2410.10449) | small (about 1K question-evidence pairs; check) | Repo AGPL-3.0; no separate data licence (copyleft: fine for private training, never publish derived rows) | P (ProbLog) on human-written premises | Bayesian posteriors: probability-bin choice (soft `gold_probs` on choice rows only, per spec) | Low | Pass | **Take**, small share |
| Corr2Cause | [GitHub](https://github.com/causalNLP/corr2cause) | about 200K (paper) | MIT **C** | P (causal discovery) | Correlations: "does X cause Y?" as yes/no | Low | Pass by name, but it is the same task family as CLadder (DI test). Disclose "similar design" | Maybe, small share |
| BLInD / choices13k | [paper](https://arxiv.org/abs/2402.09614) / [GitHub](https://github.com/jcpeterson/choices13k) | about 900 / 13K gambles | **?** / no licence file **?** | P / human choice rates (not gold) | Bayes networks with dummy events; expected value of gambles | Low | Pass | Skip (licence; program-built F8 already covers this) |

## F10 Invented jargon and definition following

| Dataset | Link | Size | Licence | Labels | Fit | Effort | Overlap risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| WinoDict | [HF](https://huggingface.co/datasets/tasksource/winodict) | 1K-10K | CC BY 4.0 | P (rewrites) | Invented words with definitions (perfect fit) | - | **DENY**: parent WinoGrande is a Decision Index test | **Do not use** |
| Codebook LLMs data (CCC protests, BFRS Pakistan violence, Manifesto) | [paper](https://arxiv.org/abs/2407.10747) | 3 real codebooks plus human-coded texts | Per source, **not read** (Manifesto may be NC) | H (expert coders) | Real codebooks whose definitions override label words: the 30% real-text codebook rows (2.3) | High | Pass | Maybe (the only good real-codebook source found) |
| redefine-math (Inverse Scaling) | [HF](https://huggingface.co/datasets/inverse-scaling/redefine-math) | under 1K | CC BY-SA 4.0 (HF) | Template | "Redefine pi as 462": a definition beats common meaning | Low | Name pass, but our `eval_redef` tests this skill. Run G13 before any use. It is a known eval | Only after G13, tiny share |
| GoLLIE guidelines | [GitHub](https://github.com/hitz-zentroa/GoLLIE) | guidelines for about 20 IE schemas | Code Apache-2.0; underlying sets mixed (ACE05 is LDC, not free) | H | Following annotation guidelines | High | Pass | Skip. Keep program-built F10 |

**Verdict for F10:** no strong external set. Keep F10 program-built (invented words checked by program). Use real
codebooks only through the Codebook LLMs data, if its licences clear.

## F12 Tool and action selection (human-made only; spec bans LLM-written tool sets)

| Dataset | Link | Size | Licence | Labels | Fit | Effort | Overlap risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| Mind2Web | [HF](https://huggingface.co/datasets/osunlp/Mind2Web), [GitHub](https://github.com/OSU-NLP-Group/Mind2Web) | 2,350 tasks, 137 sites (about 1K train tasks; thousands of action steps) | CC BY 4.0 (HF card); code MIT **C** | H (crowd demonstrations) | Choose the right element and operation from candidates: **native multiple-choice action selection** | Med (trim HTML to 1.5K tokens or less; 5-8 candidates) | Pass. Famous agent benchmark: train only | **Take** |
| AndroidControl | [README](https://github.com/google-research/google-research/tree/master/android_control) | 15,283 demonstrations, 833 apps | Apache-2.0 (README) **C** | H (raters) | Step instruction to the right action (click / type / scroll / open app / back) | Med-High (text accessibility tree) | Pass | **Take** |
| tldr-pages | [GitHub](https://github.com/tldr-pages/tldr) | 5K or more command pages | CC BY 4.0 **C** | H (community-written) | "Which command or flag does X?" (choice); "Is this call right for X?" (yes/no) | Low | Pass | **Take** |
| NL2Bash | [GitHub](https://github.com/TellinaTool/nl2bash) | about 9K text-to-bash pairs | GPL-3.0 (copyleft, private OK) | H | Command selection | Low | Pass | Maybe |

Skip: ShortcutsBench (queries are LLM-written); API-Bank (DI test); ABCD, STAR, MultiWOZ, Taskmaster (already used);
ToolTalk (MIT, but only 78 conversations).

## F13 Long documents (4-8K tokens) with decisions

| Dataset | Link | Size | Licence | Labels | Fit | Effort | Overlap risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| ConditionalQA | see F1 | 436 documents | **RO** | H | Real long policy pages with conditional yes/no and NEI. Join linked pages to reach 4-8K tokens | Med | Pass | **Take if** amended |
| More QuALITY / Qasper | already in 3.2 | currently 1,200 / 700 rows, under a cap of 3,000 each | already cleared **C** | H | Real long documents (QuALITY 2-6K tokens) | Low | Already decontaminated | **Cheapest F13 lift**: add new framings up to the cap |
| NarrativeQA (Gutenberg part) | [GitHub](https://github.com/google-deepmind/narrativeqa) | 1,567 stories, 46.8K Q | Apache-2.0 annotations; Gutenberg text public domain (movie scripts unclear, so drop them) | H, free-form | Answer-equivalence choice over 8K chunks | High | Pass | Maybe |
| TAT-DQA | see F2 | - | - | - | Only 1-page documents, so **not long** | - | - | Not for F13 |

DocNLI is DENIED. The other famous long sets (LongBench, ∞Bench, L-Eval, LooGLE, NovelQA, SCROLLS) are benchmarks and
risk contamination with the sealed LongBench v2. Do not use them.

## COMMIT (CommitChronicle and CommitPackFT already used)

| Dataset | Link | Size | Licence | Labels | Fit | Effort | Overlap risk | Recommendation |
|---|---|---|---|---|---|---|---|---|
| CCSBench | [HF](https://huggingface.co/datasets/CSU-OSS/CCSBench), [ICSE'25](https://conf.researchr.org/details/icse-2025/icse-2025-research-track/28/A-First-Look-at-Conventional-Commits-Classification) | 93,807 commits, 119 repos; train 74,581 (temporal split) | Apache-2.0 (HF card) **C** | P from the conventional-commit prefix, with "verified" types and **scopes** (check how they were verified; drop it if LLM-verified) | **Triage** (type) and **route** (scope = area) | Low | Pass. Dedupe repos against CommitChronicle and CommitPackFT; respect held-out repos and languages | **Take** |
| CommitBench | [HF](https://huggingface.co/datasets/Maxscha/commitbench), [Zenodo](https://zenodo.org/record/10497442) | 1.66M commits, 6 languages | CC BY-NC 4.0 **NC** | H messages; labels by our program | Match (message vs diff), triage | Low | Pass. Heavy repo overlap with CommitChronicle | Maybe (NC; mostly redundant) |
| ApacheJIT | [Zenodo](https://zenodo.org/records/5907002) | 106,674 commits (28,239 bug-inducing), 14 Apache projects | CC BY 4.0 **C** | P (SZZ, **noisy**) | Gate: "is this change risky?" | Med (diffs must be pulled from git) | Pass | Low priority (noisy, like the banned "later reverted" labels) |
| NLBSE issue classification | [GitHub](https://github.com/nlbse2023/issue-report-classification) | large (2023) / small (2024); check | Repo AGPL-3.0 / unstated | P (GitHub labels) | Bug / feature / question triage for **issues**, not commits | Low | Pass | Maybe (off-target) |

## Ranked shortlist (top 8)

| # | Dataset | Families | Licence | Effort | Why |
|---|---|---|---|---|---|
| 1 | BoardgameQA | F1, F6 | CC BY 4.0 | Low | Rule preferences (precedence) plus a gold "unknown"; program labels; clean licence |
| 2 | Mind2Web | F12 | CC BY 4.0 | Med | Human multiple-choice action selection; no LLM text |
| 3 | MedCalc-Bench (re-verified, no MedQA notes) | F2, F8 | CC BY-SA (+ NC notes) | Med | Real points tables and formulas with program labels |
| 4 | CCSBench | COMMIT | Apache-2.0 | Low | Verified commit types and scopes for triage and route |
| 5 | tldr-pages | F12 | CC BY 4.0 | Low | Human command and flag selection; cheap |
| 6 | RuleArena (fresh cases from its calculators) | F1, F2 | MIT | Med | Real long rules with exact program answers |
| 7 | ConditionalQA | F1, F6, F13 | Research-only | Med | The only real long policy set with conditions and NEI |
| 8 | AndroidControl | F12 | Apache-2.0 | Med-High | Human step-level action choice |

Alternates: QUITE (F8), FLD.v2 (F6), more QuALITY / Qasper rows (F13), CommitBench (NC).

Rough build time for the top 8: about 9 agent-days. With the spec's 3 public-data agents and 1 commit agent working in
parallel, that is about 3 days of wall time (estimate). F10 stays program-built.

## Risks (honest note)

- **Label noise.** MedCalc-Bench has documented wrong golds, so re-verify by program and drop disagreements. ApacheJIT
  uses SZZ labels (noisy). CCSBench's "verified" method is unconfirmed. ConditionalQA's conditions can be ambiguous, so
  do a strict G5 read (as for SQuAD 2.0) and drop the set if more than 5% of rows are wrong.
- **Contamination.** BoardgameQA test items sit in BIG-Bench Extra Hard. Mind2Web and MedCalc-Bench are popular
  benchmarks (train splits only). RuleArena and ToT have no train split, so never copy their items. redefine-math
  matches our `eval_redef` skill. Corr2Cause matches CLadder's (DI) design. The deny-list check is by name only, so G13
  n-gram and embedding decontamination (OHS-1/2/3, sealed exports, DI, JevBench, Nimble) must run before any freeze.
  The Nimble suite list was not checked here.
- **Licence.** NC and research-only sets (ConditionalQA, CommitBench, PMC-Patients notes) need an owner-signed spec 3.1
  amendment. Several licences rest only on HF cards (Mind2Web data, CCSBench, TAT-DQA), so the builder must find an
  upstream record first. FLD.v2, IIRC, BLInD and choices13k have no licence record. GPL and AGPL sets are fine for
  private training, but never publish derived rows.
- **LLM labels.** No candidate above uses gold labels from an LLM larger than 4B. tau-bench user turns and ShortcutsBench
  queries are LLM-written, so they are seeds only or skipped.
