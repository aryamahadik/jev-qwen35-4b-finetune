# Ruling A58 (draft)

This is a draft for the orchestrator to append to `lean/PREREG_FINAL.md` after the Freeze addendum. The file is
append-only: lines 2356-2825, the A42-D block hashed as `cbdc29d9…`, are not edited. Opus 5.5 ruling draft,
17 Oct 2026.

Inputs read:
- PREREG A42-D through the Freeze addendum;
- `teach1/C2_DATA_SPEC.md` 5.1-5.5, 6.3-6.5 and 7.1;
- `golden_src/GOLDEN_SPEC.md`, the hard rules and the output format;
- `c_spec/LICENCE_REGISTER.md`, the header and the replay table;
- the canonical deny-list `c_build/denylist.json` (clear entries only) and `golden_src/forbidden_label_nli.json`;
- `c2_build/replay_c2_write.json` (its drops);
- `c2_build/gblock/checks/c1_source_names.json`;
- System One Bench's `build_suites.py`, `build_arabic.py` and `data.lock.json`;
- the three scout reports;
- the upstream licence pages, read on 17 Oct: cardiffnlp/xlm-t, iabufarha/ArSarcasm and ArSarcasm-v2,
  mahmoudnabil/ASTD, elnagara/HARD, the Magdy resources page (ArSAS), Mendeley m88gg52wp7, UCI dataset 293,
  latynt/ans and google-research-datasets/tydiqa.

No "ohs" or "sealed" path was opened. The `denylist.py` CLI was not run, because its build step reads
`ohs3/used_sources.json` in-process. The deny-list results below come from alias matching on the already-built clear
entries. They are a pre-check only: the binding pass is item (c) 3.

**Summary.** None of the scouts' first-choice sources passes the project's standing source rules: SST, XNLI train,
the Arabic SNLI/MNLI translation, cardiffnlp/mteb Arabic tweets and BoolQ are each blocked by a deny-list taint, a
licence rule or both. This ruling therefore swaps in admissible sources where one exists and leaves a block out where
none does. No rule is relaxed to make room.

| Block | Include | Source (train side only) | Max train rows | Own dev |
|---|---|---|---|---|
| SB1 5-level sentiment | **NO** (C3) | none admissible | 0 | none |
| SB4 Arabic NLI | **YES, conditional** on (c) 1-4 | ANS, Arabic News Stance (latynt/ans), stance pairs, train split | 750 | 150, from the ANS dev split |
| SB5 Arabic tweet sentiment | **YES** | UCI 293, Twitter Data Set for Arabic Sentiment Analysis (Abdulla 2013), CC BY 4.0 | 750 | 150, a seeded held-out part of the same 2,000 tweets |
| SB6 short yes/no reading | **YES, conditional** on its yield | TyDi QA primary task, English, train split, YES/NO minimal answers only | 2,400 | 300, from the TyDi English dev split |

SB4 + SB5 ≤ 1,500 Arabic training rows, which is the owner's cap.

---

> **Ruling A58 (17 Oct 2026; orchestrator ruling, Opus, under the owner's 17 Oct approval of four post-freeze,
> training-only public real-text blocks driven by C1's System One Bench gaps, and the owner's binding constraint that
> Arabic gets only a little data so the model understands it at a basic level; no gate, cap or bar is loosened).**
>
> - **(a) Source rules that bind every SB block.** All are already in force; this ruling only names them.
>   1. **Allowed licences.** The licence must be on GOLDEN_SPEC rule 3's allowed list and **V**: read in an official
>      record (the creator's repo LICENSE or README, the project page, or an official repository page such as UCI),
>      never only on an HF card or a mirror (LICENCE_REGISTER decision 6). The licence allows commercial use.
>   2. **Text through another dataset.** Text that comes through another licensed dataset needs that dataset's
>      licence V too (LICENCE_REGISTER header).
>   3. **Human labels only.** Human-written text and human labels only. No LLM-written, LLM-labelled,
>      machine-translated or emoji-labelled data (GOLDEN_SPEC rule 2; A42-D 14).
>   4. **Train split only.** Never a test split, and never any split, item or parallel item that System One Bench
>      scores (GOLDEN_SPEC rule 4).
>   5. **Deny-list.** A taint verdict from `c_src/common/denylist.py check --fail-on-taint` on the source's full
>      provenance removes the source. The query lists every upstream dataset or shared task the text or labels come
>      from. There is no override.
>   6. **Not used elsewhere.** The source is not in C1's sources (`c1_source_names.json`), and it is not a G-proxy
>      source (A42-D 8.3, A48 e).
>   7. **Sealed-side check.** The source's identifiers go to the A42-D 8.5 sealed-side source-name check before any
>      builder code is written, and again on the final mix. It returns PASS or HIT per source only. A HIT removes the
>      source.
>
> - **(b) Block decisions.**
>   - **SB1, 5-level sentiment and intensity: NOT included. It moves to C3.**
>     - Every candidate is blocked:
>       - SetFit/sst5 and stanfordnlp/sst: deny-list taint `dev_eval` (SST fine-grained) and `forbidden_task`
>         (glue/sst2); licence not V.
>       - Yelp review full: taint `forbidden_task` and `licence`.
>       - Amazon MARC / amazon_reviews_multi: taint `licence`.
>       - ArSenTD-LEV and LABR: no licence.
>     - Separately, spec 5.2's cap "no new ordinal rows" (asserted by `mix_c2.py`; A42-D 1.5) forbids a new score
>       head.
>     - Recasting the 5 levels as a nominal choice to get around that cap is not allowed.
>     - The bench's sst5 suite stays out of distribution for C2.
>   - **SB4, Arabic NLI: included, conditional on (c) 1-4 passing.**
>     - **Source:** ANS (Khouja, FEVER 2020; github.com/latynt/ans, pinned commit), stance version, train split.
>       - The text is human-written: annotators paraphrased or contradicted Arabic news headlines.
>       - The labels are human 3-class stance labels: agree, disagree, other.
>     - **Licence:** an Apache-2.0 statement in the creator's own README. That counts as a statement in an official
>       file if the G1 verifier quotes the raw `readme.md` at the pinned commit with its sha256.
>     - **Headlines from the ANT corpus.** The ANS paper says part of the headlines come from the ANT corpus.
>       - If the paper or the data marks ANT-origin rows, those rows are dropped unless ANT's licence is V.
>       - If ANT-origin rows cannot be told apart and ANT's licence is not V, SB4 is out.
>     - **Rejected sources:**
>       - facebook/xnli train: CC BY-NC 4.0, upstream LICENSE, and MultiNLI-derived.
>       - LLMXperts/Arabic-NLi-Pair-Class: an SNLI derivative (taint `ohs3_avoid`), new MultiNLI rows (`no_new_rows`
>         already_used) and an unstated machine translation.
>       - ArEntail: binary, test only, no licence.
>       - ArNLI: not released.
>     - **No fallback.** If SB4 fails, no other Arabic NLI source is substituted, and the block moves to C3.
>   - **SB5, Arabic short-text sentiment: included.**
>     - **Source:** UCI ML Repository dataset 293 (DOI 10.24432/C5F31B; donated by N. Abdulla).
>       - Licence: CC BY 4.0 on the UCI page, which is the official record.
>       - 2,000 tweets with full text, MSA and Jordanian dialect.
>       - Labels: 1,000 positive and 1,000 negative, assigned by two native-speaker experts, with a third expert
>         breaking ties.
>       - It has no splits, so it counts as train (GOLDEN_SPEC rule 4).
>     - **No neutral class.** The source has no neutral label, so a 3-option row would never have neutral as gold and
>       would teach "never neutral". SB5 therefore uses the yes/no head of (d). It teaches Arabic polarity. It does not
>       claim to teach the neutral boundary; this is reported.
>     - **Rejected sources:**
>       - cardiffnlp and mteb tweet_sentiment_multilingual: XLM-T says "restrictions may apply to individual
>         datasets", the upstream SemEval-2017 Task 4 terms are not V, the provenance hits the deny-list alias
>         `semeval 2017 task 4` (forbidden_task), and the pool is the one the bench draws from.
>       - ArSarcasm v1 and v2: the text comes through SemEval-2017 and through ASTD, which is GPL-2.0 and not on the
>         list; v2 has no source column.
>       - ASTD: GPL-2.0.
>       - ArSAS, HARD, ArSenTD-LEV and arbml/Syria_Tweet_Sentiment: no licence.
>       - Mendeley m88gg52wp7: CC BY 4.0, but the label method and tweet source are not stated, so it fails rule 3.
>       - tyqiangz/multilingual-sentiments: HF card only, probably a repack of cardiffnlp.
>   - **SB6, short yes/no reading comprehension: included, conditional on its yield.**
>     - **Source:** TyDi QA primary task (google-research-datasets/tydiqa, pinned commit; Apache-2.0 in the official
>       repo; the text is Wikipedia, third-party text under a clean dataset licence).
>       - English train split only.
>       - Only examples whose annotated yes/no answer is YES or NO, with the passage that holds the answer.
>       - The questions were written by people who had not seen the answer.
>     - **English only:** TyDi's Arabic rows are excluded so the Arabic cap in (e) holds.
>     - **Rejected sources:**
>       - BoolQ (google/boolq, super_glue/boolq): taint `forbidden_task`. C2 replay already dropped BoolQ's 896 rows for
>         this reason.
>       - StrategyQA, MultiRC, CondaQA, WikiQA, ShARC: forbidden or tainted.
>     - **The polarity half of SB6 has no source.** SST-2, IMDb, Rotten Tomatoes, amazon_polarity, Yelp polarity and
>       tweet_eval are all `forbidden_task`.
>       - Negation polarity stays with the A42-D item 7 twins and the G-block.
>       - Hedges and sarcasm are not covered; this is reported.
>     - **Yield.** If fewer than 500 SB6 rows survive (c) and the balance rules, SB6 still enters at its realised size.
>       Nothing is refilled (spec 5.3).
>
> - **(c) Order of work and binding checks, per included block.** Each step starts when the one before it is complete.
>   No bar is changed.
>   1. **G1 provenance.** A Sonnet verifier reads each official record and logs, in `meta.licence`:
>      - the URL, the pinned commit or DOI, the file sha256 and the quoted licence line;
>      - the label-method quote from the paper.
>
>      Any (a) 1-3 failure removes the source.
>   2. **8.5 sealed-side source-name check.** PASS is required.
>   3. **Deny-list pass.** `denylist.py check --fail-on-taint` on the full provenance query, run by the orchestrator. No
>      taint verdict is allowed. The C1-source and G-proxy-source checks also run here.
>   4. **Bench exclusion (program).**
>      - The decontamination program rebuilds System One Bench's text cases at the pinned revisions
>        (`build_suites.py`, `build_arabic.py`) and checks them against `data.lock.json` with `data_lock.py`.
>      - No builder agent reads bench item text. As with JevBench, only the decontamination program does.
>      - It then drops every source row whose normalised state, or premise or hypothesis, is an exact match or a
>        near-exact match (MinHash) of any item in the **full scored splits**:
>        - sst5 test, 2,210;
>        - sst2 validation, 872;
>        - boolq validation, 3,270;
>        - xnli test ar/en/fr, 5,010 each, parallel items included;
>        - mteb tweet_sentiment_multilingual arabic test, 256;
>        - the MIRACL-ar dev queries and passages used by `ar_miracl_*`;
>        - every other `cases.jsonl` text suite.
>      - The drops are counted per block.
>   5. **Build.**
>      - The Sonnet builder writes the rows in GOLDEN_SPEC v14 raw format, with defs, and converts them with the same
>        path that made C1's golden_train rows.
>      - Rows are deterministic, CPU-only, seed 20261013.
>      - **Format gates at 100%:** schema; the options are exactly the block's set and gold is one of them; G12 (exact
>        duplicates 0, MinHash keeps one, one row per source record); G15 loader round trip; every row ≤ 2,000 tokens
>        and the block mean ≤ 800 (instructions counted twice, spec 3.0).
>      - **G2, G3, G3-H, G4, G-SL, G-TW and the 3.3 reseed audit do not apply.** There is no program gold, no slot
>        template and no generator. The A46 screen in step 6 is the label check.
>      - **No bench wording.** No instruction or definition string shares an 8-gram with any bench instruction or
>        criteria string.
>   6. **A46 label-noise screen** on every candidate row **and** every own-dev row, as A46 sets it:
>      - two independent blind Haiku reads, on gold-free task files of ≤ 50 items, under the G5-H answer contract
>        and the file-access audit;
>      - both reads disagree, or one disagrees and the other abstains → Sonnet first pass → Opus confirms every
>        wrong-gold or ambiguous call;
>      - only confirmed rows are dropped. Rows are never relabelled.
>      - Per-block read, flagged, confirmed and dropped counts go into the training-GO request.
>   7. **G6 shortcut probes: report only, with the reason stated.**
>      - There is no generator, so there is no ≥ 5,000-row QC build. The spec 6.3 G6 is defined and calibrated only
>        on such builds (A50), and human-label rows in replay never carried G6.
>      - Instead, each block reports a partial-input baseline with the G6 model set: 5-fold CV on all its source
>        train rows, against the majority share. SB4: hypothesis only. SB5: a short-text length and lexicon baseline.
>        SB6: question only, and passage only.
>      - These numbers never admit or drop a row. They are in the training-GO request.
>   8. **G10 balance on the selected rows (A49 c).**
>      - SB4: no class above 40%.
>      - SB5 and SB6: yes share 45-55%.
>      - Gold position is uniform by a seeded option shuffle.
>      - Balancing is seeded down-sampling only.
>   9. **G13 seed and candidates.** Run against every registry target (OHS-4 and OHS-AC exports counts-only, public
>      anchors, the G-proxy, the C2 dev targets under A53), with 0 hits after drops.
>      - The A53 waiver does not apply to SB rows.
>      - The SB own-dev sets join the C2-side dev targets.
>   10. **C1 crowd read and selection.**
>       - Candidates are up to 1.5 × each block's max (A42-D 1.3).
>       - G9 is C1-only (A18.2 readout; the SGLang path if A49 f passed). Same bins: easy ≤ 25%, hard ≤ 30%.
>       - Rows with p_g < 0.05 go to the G9 re-read, through the step-6 cascade, drop only.
>       - Then a seeded selection (20261013), stratified by label, down to the max.
>       - C1 output is never a label.
>   11. **One joint SB pilot, under A42-D 4's rules.** It runs only if at least one block reaches this step.
>       - One short LoRA pass from C1 on all selected SB rows, no replay, recipe A37 (i), seed 20261013, ≤ $0.5, inside
>         the $40 cap.
>       - **(ii) Existing dev:** the drop must be ≤ 0.5 pt.
>       - **(iii) G-proxy:** the change must not be rejected under 4.3.
>       - (ii) and (iii) bind on the joint pass. If either fails, every SB block moves to C3. There is no re-pilot.
>       - **(i) Own dev:** each block's gain over C1 on its own dev must be ≥ +2.0 pt (point). A block that misses it
>         moves to C3.
>       - The verdict is due Mon 19 Oct 23:59 UTC (A42-D 1.6). The gates are due by the 21 Oct cutoff.
>       - System One Bench is never read by the pilot.
>   12. **Mix, then G13 on the final all-block mix (every block, not just SB).**
>       - The step-4 bench text target (all `cases.jsonl` text suites plus the full scored splits named there) is added
>         as a G13 eval target, with 13-gram and exact or near-exact methods.
>       - 0 hits after drops. A hit in any block drops its unit, counted per block.
>       - Like every other target, it is never a selection signal.
>
> - **(d) Row format and heads.**
>   - The options are each block's natural label set, with definitions written for this project. The bench's criteria
>     text is not copied.
>   - Instructions are in English and the content keeps its source language.
>   - Each block has at least 4 instruction wordings, assigned by a seeded draw, none above 35% of the block.
>   - Edge cases are tagged in `meta.edge` (negation, sarcasm, missing_info, and so on).
>   - **SB4: choice head**, options `entailment`, `contradiction`, `neutral`.
>     - State: `{premise: <ANS evidence headline>, hypothesis: <ANS claim>}`.
>     - Mapping: agree → entailment, disagree → contradiction, other → neutral (the premise does not settle the
>       hypothesis).
>     - The mapping is written into the defs before any read. A46 decides doubtful rows; they are never relabelled.
>   - **SB5: yes/no head.**
>     - State: `{tweet: <text>}`.
>     - Each tweet gets one seeded question type: "Does the writer express a negative opinion or feeling?" or "Does
>       the writer express a positive opinion or feeling?".
>     - The gold follows from the expert label. The two types are seeded 50/50.
>   - **SB6: yes/no head.**
>     - State: `{passage: <TyDi answer passage, clipped at sentence ends to ≤ 1,500 tokens>, question: <question>}`.
>     - Gold: YES → yes, NO → no.
>
> - **(e) Sizes, the 125K cap and the trim order.**
>   - **Maximum training rows:** SB1 0; SB4 750; SB5 750; SB6 2,400 (the spec 5.2 one-family cap).
>   - **Arabic cap:** SB4 + SB5 ≤ 1,500 (the owner's cap). Rows a failed Arabic block frees are never moved to the
>     other Arabic block or to SB6.
>   - SB rows are new rows. Each gets replay of floor(1.5 × realised rows), drawn by `replay_sample.py` (spec 5.3,
>     5.4). The most this adds is 3,900 new + 5,850 replay rows, inside A40 (d)'s 125,000 and the 40/60 split. SB rows
>     are not in the agent tier.
>   - **Place in the A42-D 2.3 trim order:**
>     - After step 2 (wave 2) and before step 3 (item 8's tail), a new **step 2b** removes SB6 rows above 1,200, as
>       seeded whole units, with their replay.
>     - SB4 and SB5 are trimmed only in step 4's proportional trim.
>     - The 50,000-row floor and every other 2.3 rule are unchanged.
>   - **Own dev, never trained.** Each set is disjoint from the training rows (grouped by source record, headline or
>     article, then checked by G13) and from the bench (step 4).
>     - SB4: ≤ 150 rows from the ANS dev split. The ANS test split is not used.
>     - SB5: 150 rows, a seeded (20261013) label-stratified hold-out from the 2,000 tweets, drawn before any read.
>     - SB6: ≤ 300 rows from the TyDi English dev split, YES/NO examples only.
>   - **Pooled own dev.** The pooled SB own dev joins A42-D 9.3's "pooled own dev splits of the new families that
>     entered C2" for the item 9 score.
>
> - **(f) How reports label System One Bench after C2.**
>   - The bench is report-only for C2. It never selects a row, block, candidate, dial or stage (A42-D 14 applies to it
>     as to Jev).
>   - Every C2 bench table marks the following suites **"in-family after C2: the task was trained on other sources;
>     test items excluded by G13"**:
>     - `xnli_ar`, if SB4 enters;
>     - `ar_sentiment` and `img_ar_sentiment`, if SB5 enters; their "zero-shot for every model" note no longer holds
>       for C2;
>     - `boolq`, if SB6 enters.
>   - `xnli_en` and `xnli_fr` keep their existing C1 labels (English NLI was already in C1's replay).
>   - `sst5` and `sst2` are unaffected.
>   - The 16-suite text average is reported twice: all suites, and without the in-family-after-C2 suites.
>   - A C2-vs-Jev or C2-vs-C1 statement about an in-family suite must carry the label.
>   - The SB5 neutral-class gap and the SB6 hedge and sarcasm gap are stated.
>
> - **(g) Unchanged.**
>   - A42-D 1-14 and A43-A57: every gate, cap and bar.
>   - The $40 and $34 caps and T_max.
>   - Both owner GO points.
>   - The usage stop at 96% and the 98% ceiling (A47).
>   - The never-open rules (spec 6.5; AC_SEALED_BRIEF).
>   - The A42-D block text and its sha256.
>   - SB1 and any failed SB block go to C3 with their reasons. The training-GO request lists every SB block's
>     realised rows, drops by step, probe reports and pilot verdict.
