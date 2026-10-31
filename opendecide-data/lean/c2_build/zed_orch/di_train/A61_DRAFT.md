# Ruling A61 (draft)

Draft for the orchestrator to append to `lean/PREREG_FINAL.md` after the last adopted ruling. The file is append-only:
lines 2356-2825 (the A42-D block, sha256 `cbdc29d9…`) are not edited. Opus 5.5 ruling draft, Sat 17 Oct 2026 ~04:50 UTC.

**Inputs read.**
- PREREG A42-D through A56, the Freeze addendum and A55.
- Drafts A57 (`zed_orch/A57_DRAFT.md`) and A58 (`zed_orch/sb_blocks/A58_DRAFT.md`); the HANDOFF entries for A58-A60.
- `golden_src/GOLDEN_SPEC.md` rules 1-6.
- `c_build/denylist.json`: the `entries` list only, by name, class, category and scope.
- `c2_build/gblock/checks/c1_source_names.json`.
- `c_build/decontam_g13.py`: the `targets()` registry, `QUARANTINE_OK` and the `OHS_SRC_HF` name constant.
- `c2_build/g13_c2.py`: how it uses the registry.
- `c2_build/zed_orch/MIX_A42D_NOTES.md`; the constants in `mix_c2.py`.
- The DI quarantine metadata, without opening any item text:
  - `bench/external_quarantine/decision_index/repo/hub/manifest.json` (sha256 b4e78359…);
  - `repo/docs/suite.md` (84b42c8a…);
  - `work/artifacts/benchmark-suite/release-v1-rebuilt/manifest.json` (7759d0fe…);
  - `rebuild.sh` and `rebuild_finish.log`.
- The two scout reports given in the task. The tasksource report was cut off after about 28 of its 79 rows.

No path containing "ohs" or "sealed" was opened. No item text in `selected-rows.jsonl` was read.

**What `di_test` is.** The existing G13 target `di_test` (decontam_g13.py line 862; `QUARANTINE_OK[1]`) is **not**
the DI 0.3 public suite.
- It is a local rebuild (3 Oct 2026, kit commit `52a6989`, 21 Sep) of the kit's **"release-v1"** frozen suite.
  - It has 36 benchmarks and 131,909 requests.
  - HLE (catalog 45, 513 requests) was skipped because it is gated.
  - Selected-rows sha256 is `3eb7aa1e…`. The published sha is `288d372…`, so the rebuild is not byte-identical.
  - The hub manifest it rebuilds lists 37 benchmarks and 132,422 requests. That is where the "~132,422" figure comes
    from.
- Its benchmark list is the 0.2-era list:
  - it includes MMLU, ARC-Easy/Challenge, SimpleBench, RouterBench and ForecastBench;
  - it has catalog ids ≤ 50 only;
  - it has no MMLU-Pro, BBH, HoVer (DI #61), PhishNChips, RAGTruth or New Yorker, and GSM8K is in its 0.2 form.
- The scout's 0.3 public list (kit `hub/0.3/manifest.json`) differs in exactly these ways.
- So `di_test` stays as it is, and the 0.3 public suite is added as a new target (item e).

**Verdict.** The DI-train block enters C2 as three blocks, under every standing source rule (A58 a):
- **DI-KR:** GSM8K.
- **DI-LANG:** HoVer and iSarcasmEval-English.
- **DI-TS:** a tasksource subset.

The DI-RC and DI-TOOLS blocks are empty. Each of their candidate sources is blocked by a standing rule: already used by
C1, a dev or eval source here, an OHS source, a non-commercial licence, LLM-written data, or no train split. Their
tasks move to C2.1.

The C2 mix limits become:
- whole mix ≤ **150,000** rows;
- core ≤ 125,000 rows, unchanged;
- DI part ≤ 25,000 rows.

The money limits become:
- C2 Modal ≤ **$45**, which is the goal's existing hard stop;
- training ≤ **$39**;
- relay through the reserve accounts after mahadikarya2 and mahadikarya3, and never aryamhd.

| Block | Include | Sources (TRAIN split only) | Max train rows | Own dev |
|---|---|---|---|---|
| DI-KR | YES | GSM8K main train (openai/grade-school-math, MIT) | 2,400 | 300 |
| DI-LANG | YES, conditional per source | HoVer train (CC BY-SA 4.0) ≤ 2,400; iSarcasmEval task A/C English train (MIT, if V) ≤ 1,200 | 3,600 | 300 (150 + 150) |
| DI-TS | YES, conditional per task | tasksource tasks that pass (a) and (b): ≤ 600 per task | 4,000 | 300 |
| DI-RC | NO (C2.1) | none admissible | 0 | 0 |
| DI-TOOLS | NO (C2.1) | none admissible | 0 | 0 |
| **Total new** | | | **10,000** (+ replay 15,000 = 25,000) | 900 |

---

> **Ruling A61 (17 Oct 2026; orchestrator ruling, Opus, under the owner's decision of 17 Oct ~04:40 UTC, verbatim:
> "Yes. Add the DI-train block to C2 now (commercial-licence train splits + tasksource subset, DI public suite as a
> leak-check target), raise the mix to about 150K rows and use the Modal reserve for the extra training. Put the
> harder same-style families and the head/loss ideas in C2.1." No gate, bar, probe threshold or isolation rule is
> loosened. DI suite items are never trained.)**
>
> - **(a) Source rules that bind every DI source.** These are the A58 (a) rules, all already in force; this ruling
>   only names them.
>   1. **Licence.** The licence is on GOLDEN_SPEC rule 3's allowed list and allows commercial use. It must be **V**:
>      quoted from an official record (the creator's repo LICENSE or README, the project page, or an official
>      repository page) with the URL, the pinned commit and the file sha256. A licence stated only on an HF card,
>      in tasksource metadata or on a mirror is not V.
>   2. **Text through another dataset.** Text or labels that come through another dataset need that dataset's
>      licence V too. For example, recast tasks built on CoNLL, FactBank or SemEval data.
>   3. **Human labels, or program labels by construction.** Human-written text with human labels, or third-party
>      program-generated rows whose label follows by construction (a template or a logic or arithmetic check).
>      These are not allowed:
>      - LLM-written or LLM-labelled data;
>      - data made by big models (A42-D 14);
>      - machine-translated data;
>      - distant-supervision labels;
>      - engine estimates, such as Stockfish values.
>   4. **Train split only.** Never a test split. Never a split, item or record that any DI edition scores, or that
>      another benchmark uses as its test (GOLDEN_SPEC rule 4).
>   5. **Deny-list.** `c_src/common/denylist.py check --fail-on-taint`, run by the orchestrator on the full
>      provenance query (dataset, config, split, every upstream source). A taint verdict removes the source, with no
>      override. A `di_test` taint scoped to a split blocks only that split. That is the owner's decision, and the
>      deny-list already scopes it that way. A `di_test` taint scoped to a dataset (MMLU, ChessBench, ForecastBench,
>      Habermas) still removes the whole dataset.
>   6. **Not used elsewhere.** The source is not:
>      - in C1's sources (`c1_source_names.json`);
>      - a dev or eval source here;
>      - a G-proxy source (A48 e);
>      - one of the 11 metadata-block sources;
>      - an SB source of A58.
>   7. **Sealed-side source-name check.** The A42-D 8.5 check runs before any builder code is written and again on
>      the final mix. It returns PASS or HIT per source only. A HIT removes the source. No C2-side agent opens an
>      "ohs" path.
>
> - **(b) Block decisions.**
>   - **DI-KR (knowledge and reasoning): GSM8K, YES.**
>     - Source: openai/grade-school-math, `main`, train (7,473 problems). The licence is MIT, made V from the repo
>       LICENSE. Problems and solutions are human-written.
>     - The deny-list taints only its test split (`3G#25.1`, `di:GSM8K`).
>     - Rejected:
>       - ARC and WinoGrande: `no_new_rows already_used`.
>       - HellaSwag: `llm_written`.
>       - MMLU and its auxiliary train: `test_split`, and RACE-derived.
>       - ChessBench: dataset-scoped `di_test`; its Stockfish labels also fail (a) 3. Chess moves to C2.1 as a
>         program-gold family.
>       - MMLU-Pro, BBH, GPQA, HLE, CRUXEval, MuSR, SATA-Bench, CLadder and SimpleBench: no train split, and canary
>         or no-training terms where stated.
>       - Corr2Cause: no licence.
>   - **DI-LANG (language understanding): HoVer and iSarcasmEval-English, YES, each conditional on (c) 1-4.**
>     - **HoVer** (hover-nlp, pinned commit; CC BY-SA 4.0 if V).
>       - Train split: 18,171 human-written claims with human SUPPORTED / NOT_SUPPORTED labels, built on HotpotQA.
>       - The Wikipedia evidence text comes from the HotpotQA 2017 abstracts dump (CC BY-SA 4.0, V needed by (a) 2).
>         It must fit inside the ~2 GB free-download cap.
>       - **If the evidence text cannot be fetched, HoVer is out.** A claim-only row would be a different,
>         unanswerable task.
>       - The deny-list taints only its DI split (`3G#25.2`).
>     - **iSarcasmEval** (iabufarha/iSarcasmEval, pinned commit; MIT if V on the repo LICENSE).
>       - English train only. The labels and rephrases were written by the tweets' own authors.
>       - Arabic rows are excluded, so A58 (e)'s Arabic cap of 1,500 is untouched.
>       - The deny-list taints only its DI split.
>     - Rejected:
>       - ANLI: CC BY-NC 4.0.
>       - ContractNLI: `ohs_source`.
>       - Humicroedit: `forbidden_task`.
>       - NLI4CT: SemEval terms, not V.
>       - RAGTruth: non-commercial contexts.
>       - VAST and ACOS: no licence.
>       - FinEntity: its only split is DI's scored set.
>       - PhishNChips: academic terms.
>       - New Yorker: licence not V.
>   - **DI-TS (tasksource subset), YES, per task.** Each task passes (a) 1-7 on its own upstream record, not on
>     tasksource's metadata.
>     - **Candidates, pending (a):**
>       - tasksource/lonli;
>       - tasksource/SpaceNLI;
>       - tasksource/logical-entailment;
>       - tasksource/tracie;
>       - tasksource/temporal-nli, if (a) 2 holds for its source corpora;
>       - tasksource/resnli;
>       - tasksource/wice, with Wikipedia text;
>       - the tasksource/recast subsets megaveridicality, verbnet, factuality and puns, each only if (a) 2 holds;
>       - every later row of the scout's 79-task list that passes the same filter mechanically.
>     - **Out:**
>       - recast_ner: CoNLL / Reuters text fails (a) 2.
>       - stanfordnlp/snli and breaking_nli: SNLI and its derivatives, `ohs3_avoid`.
>       - WANLI: `llm_written`.
>       - probability_words_nli usnli, 1hop and 2hop: `forbidden_task`.
>       - defeasible-nli atomic, social and snli: `forbidden_task` or `derived`.
>       - scinli: `label_quality`.
>       - MSciNLI: distant labels, (a) 3.
>       - monotonicity-entailment and equate: `test_split`.
>       - ruletaker: `already_used`.
>       - scone: OHS source.
>       - babi_nli: a C1 source.
>       - Every task whose source is a DI benchmark (the scout's exclusion list stands).
>   - **DI-RC (retrieval and classification): NO, to C2.1.**
>     - BANKING77 and CLINC150: C1 sources, dev and eval sources here, and BANKING77 is also `forbidden_task`.
>     - Amazon ESCI: `no_new_rows other_subset_used`.
>     - SGD / SGD-X: an OHS source (`schema_guided_dstc8`).
>     - BRIGHT: no train split.
>     - RouterBench: model outputs.
>   - **DI-TOOLS: NO, to C2.1.**
>     - BFCL: no train split.
>     - ToolRet train, API-Bank train, Glaive v2, Hermes FC v1, ToolACE and xLAM: LLM-generated (A42-D 14) or
>       research-only.
>     - When2Call train: named in A42-D 14.
>     - MASSIVE, Taskmaster, TOPv2 and MultiWOZ: `already_used` or `non_human_labels`.
>     - Tool decisions stay with T40-T45 in C2. Program-gold DI-style tool families are C2.1.
>
> - **(c) Order of work and binding checks, per source.** Each step starts when the one before it is complete. Every
>   bar is unchanged.
>   1. **G1 provenance.** A Sonnet verifier logs in `meta.licence` the URL, the pinned commit or revision, the file
>      sha256, the quoted licence line and the label-method quote. Any failure of (a) 1-3 removes the source.
>   2. **(a) 7, the sealed-side source-name check.** PASS is required.
>   3. **(a) 5 and (a) 6.** The deny-list check and the use-elsewhere checks.
>   4. **DI exclusion, by G13-seed.** The source pool is checked against `di03_public`, `di_test` and
>      `di_src_splits` (item e) before any row is built. Any hit drops the whole source record. No builder agent
>      opens `bench/external_quarantine/**` or reads DI item text; only the decontamination program does.
>   5. **Build.**
>      - Rows are in GOLDEN_SPEC v14 raw format with defs, converted by the same path that made C1's golden_train
>        rows. The build is deterministic and CPU-only, with seed 20261013. English instructions only.
>      - **Format gates at 100%:**
>        - schema;
>        - options exactly the block's label set, with gold one of them;
>        - G12: exact duplicates 0, MinHash keeps one, **one row per source record**, and no row duplicates a C1 or
>          replay row;
>        - G15 loader round trip;
>        - every row ≤ 2,000 tokens and block mean ≤ 800, with instructions counted twice (spec 3.0);
>        - ≥ 4 instruction wordings per block, assigned by a seeded draw, none above 35%;
>        - gold position uniform by a seeded shuffle.
>      - **No DI wording.** No instruction or definition shares an 8-gram with any DI request prompt or criteria
>        string. This is a program check inside the G13 templates method.
>      - **No truncation that could change gold.** A row over the token cap is dropped. HoVer evidence is cut only
>        at sentence ends, and only if every gold supporting sentence stays.
>   6. **A46 label-noise screen** on every candidate row **and** every own-dev row, as A46 sets it. This includes
>      third-party program-label rows, because none of our program gates ran on them.
>      - Two independent blind Haiku reads, on gold-free task files of ≤ 50 items, under the G5-H answer contract and
>        the file-access audit.
>      - If both reads disagree with gold, or one disagrees and the other abstains, the row goes to a Sonnet first
>        pass. Opus confirms every wrong-gold or ambiguous call.
>      - Only confirmed rows are dropped. No row is ever relabelled, and Haiku only flags.
>      - Per-source read, flagged, confirmed and dropped counts go into the GO #1 request.
>   7. **Program checks and probes.**
>      - **GSM8K gold check (drop only).** A pure-arithmetic AST evaluator (no names, no `eval`) re-computes every
>        `<<expr=value>>` in the human solution, and the chain must reach the `####` answer. Any mismatch drops the
>        problem.
>      - **GSM8K distractors are program-made**, so the A42-D 3.2 options-only and formatting-only probes **bind**
>        at chance ± 3 pp (two-sided) with the G6 model set, on the full train build (≥ 5,000 rows). The A50
>        four-build mean is taken over seed bases 20261013, 11,000,000, 12,000,000 and 13,000,000, fixed now.
>      - For every other DI source there is no generator, so G6 is **report only** (A58 c7). It is a partial-input
>        baseline, 5-fold CV against the majority share:
>        - HoVer: claim only;
>        - iSarcasmEval: length and lexicon;
>        - DI-TS: hypothesis only.
>        These numbers never admit or drop a row.
>   8. **G10 balance on the selected rows (A49 c).**
>      - Yes/no sources: yes share 45-55%.
>      - Choice sources: no class above 40%, or above 55% for 2-way tasks.
>      - Balancing is seeded down-sampling only.
>   9. **G13 on candidates** against every registry target, with item (e) added. 0 hits after drops; a hit drops its
>      whole unit. The A53 waiver does not apply to DI rows. The DI own-dev sets join the C2-side dev targets.
>   10. **C1 crowd read and selection.**
>       - Candidates are ≤ 1.5 × each source's max (A42-D 1.3).
>       - G9 is C1-only: A18.2 readout, or the SGLang path if A49 (f) passed. Bins: easy ≤ 25%, hard ≤ 30%.
>       - Rows with p_g < 0.05 are re-read through the step 6 cascade, drop only.
>       - Then a seeded (20261013) selection, stratified by label and by task, down to the max.
>       - C1 output is never a label.
>   11. **One joint DI pilot** under A42-D 4.
>       - One short LoRA pass from C1 on a seeded, stratified sample of ≤ 1,500 selected rows per block. No replay,
>         recipe A37 (i), seed 20261013, ≤ $1, on mahadikarya44 and then arya-mahadik-ai, inside the $45.
>       - **(ii) Existing dev:** drop ≤ 0.5 pt.
>       - **(iii) G-proxy:** not rejected under 4.3.
>       - (ii) and (iii) bind on the joint pass. If either fails, every DI block moves to C2.1. There is no re-pilot.
>       - **(i) Own dev:** each block's gain over C1 on its own dev must be ≥ +2.0 pt (point). A block that misses it
>         moves to C2.1.
>       - The pilot never reads any DI suite.
>   12. **Final mix and final all-block G13.** The run is set for Mon 19 Oct ~14:00 UTC. Item (e)'s targets apply to
>       **every** block of the final mix, not only DI. 0 hits after drops, counted per block.
>   - **Deadlines.** A DI block enters only if all of these hold. Otherwise it moves to C2.1, and nothing is
>     refilled (spec 5.3):
>     - its candidates are in the final all-block G13 run with 0 hits after drops;
>     - its pilot verdict is logged by **Mon 19 Oct 23:59 UTC** (A42-D 1.6);
>     - it passes every gate by the Wed 21 Oct cutoff.
>
>     DI blocks never count toward the 10 program families, and their absence never blocks training.
>
> - **(d) Row format.**
>   - **GSM8K: choice head.**
>     - State: the problem.
>     - Options: gold plus 3 distractors, drawn by a seed, numerically distinct and in one number format.
>     - Distractors come from two pools: the problem's own intermediate calculator values (the hard pool), and the
>       golds of other train problems of similar magnitude (the 0.3 style). The share of each is fixed by the seed.
>     - The probes in (c) 7 bind on this design.
>   - **HoVer: yes/no head.**
>     - State: the claim plus its gold supporting sentences, under their titles.
>     - Question: "Do the passages fully support the claim?". SUPPORTED → yes, NOT_SUPPORTED → no.
>   - **iSarcasmEval: one row per source record.**
>     - Task A: yes/no, "Is the author being sarcastic?".
>     - Task C: a 2-option choice, "Which text is sarcastic?". The sarcastic tweet is paired with its author's
>       rephrase. Task C is ≤ 40% of the source's rows.
>   - **DI-TS: choice head.** The options are each task's natural label set, with definitions written for this
>     project.
>   - **General rules.**
>     - Content keeps its source language (English).
>     - Edge cases are tagged in `meta.edge`.
>     - Claude writes only definitions, instructions and wording. It never writes a label (GOLDEN_SPEC 5, A42-D 14).
>     - No complement twins are made from DI rows in C2.
>
> - **(e) G13 target specification (the "DI public suite as a leak-check target").**
>   1. **`di_test` stays as it is.**
>      - It is the release-v1 rebuild: 36 benchmarks, 131,909 requests, sha `3eb7aa1e…`.
>      - It is not the 0.3 public suite (see the note above the ruling).
>   2. **New target `di03_public`: the DI 0.3 public suite.**
>      - Pin: the kit commit whose `hub/0.3/manifest.json` and `docs/suite.md` were read, with both sha256 values
>        logged.
>      - Source, primary path: the kit's published 0.3 frozen file, with its sha256 checked against that manifest.
>      - Fallback: `decision_index suite rebuild` at that commit, run in a new
>        `bench/external_quarantine/decision_index_03/`. Byte-identity is reported. A non-identical rebuild binds as
>        "rebuilt", like `di_test`, with per-benchmark counts against the manifest logged.
>      - The file path is added to `QUARANTINE_OK`, read as `blind=True`. Its path and sha256 go into the never-train
>        manifest, so `MixInputLog` refuses it.
>      - **HLE is gated.** If HLE cannot be fetched, the target records the coverage gap "HLE not scanned (gated)".
>        That gap is accepted only under this ruling (tag `A61-HLE`), because:
>        - HLE has no train split;
>        - no DI-train source derives from HLE;
>        - every other HLE use is already banned.
>        The gap is stated in the GO #1 request. Any other gap makes the target incomplete.
>   3. **New target `di_src_splits`.**
>      - It holds the **full** DI-scored split of every DI benchmark whose source feeds a DI block: GSM8K test
>        (1,319, both the 0.2 and the 0.3 forms of the item), HoVer's DI-scored split in full, and iSarcasmEval test
>        (all tracks).
>      - Each is fetched upstream at the suite.md pins.
>      - It covers the whole split, not only the sampled public items, because the 80% private part may draw from
>        the same splits.
>   4. **Methods.**
>      - Every registry method: exact full, segment and short; substring; 10- and 12-gram; tulu8; minhash; and
>        structure.
>      - Plus a record-id match: GSM8K question hash, HoVer uid and its origin-claim group, iSarcasm tweet text hash.
>      - Plus the 8-gram instruction check of (c) 5.
>      - A hit drops the whole unit. A unit is never reworded or resubmitted.
>   5. **Stages.**
>      - Seed (c 4), then candidates (c 9), then the final all-block mix (c 12), with 0 hits after drops at each.
>      - Like Jev, the DI suite is never a selection signal (A42-D 14).
>   6. **Readiness.** If `di03_public` or `di_src_splits` is not complete before the Mon 19 Oct ~14:00 UTC run:
>      - no DI block enters C2;
>      - the core mix still runs against every other target, including `di_test`.
>
> - **(f) Sizes, the 150,000 cap and the trim order. Changes A40 (d) and A42-D 1.4.**
>   - **Caps.**
>     - Whole mix ≤ **150,000** rows, every twin included.
>     - The **core** (every non-DI block with its replay) stays ≤ **125,000**, so A40 (d) and A42-D 1.4 are unchanged
>       for it.
>     - The **DI part** (DI rows and their replay) is ≤ **25,000**, which means DI new rows ≤ 10,000.
>   - **Replay.**
>     - DI rows are new rows. Each gets replay floor(1.5 × realised), drawn by `replay_sample.py`, so the 40/60 split
>       holds.
>     - DI rows are not in the agent tier.
>     - Every spec 5.2 cap is asserted per source on realised rows:
>       - one source or task ≤ 2,400 rows, and DI-TS ≤ 600 per task;
>       - free-form ≤ 25%;
>       - no ordinal rows;
>       - ≤ 64 rows per card;
>       - yes/no 45-55% of all new rows.
>   - **A46 replay extension.**
>     - The extra replay comes only from A46-screened rows. The provisional A46 draw is extended (seeded 20261013) to
>       the new largest replay size and screened under A46 before the final draw.
>     - If that screen is not complete by the cutoff, DI new rows are scaled down until their replay fits the
>       screened pool. The replay ratio is never lowered.
>   - **Trim order (A42-D 2.3 and A58 e).**
>     - The core is trimmed against T_core (item g), in the existing order: steps 1, 2, 2b, 3 and 4, unchanged.
>     - Then the DI part is trimmed against T_max minus the core's realised projection, in this order:
>       - **D1:** DI-TS rows above 2,000, removed as seeded whole tasks with their replay;
>       - **D2:** a proportional trim across the DI blocks and sources, keeping every balance rule and their replay.
>     - Both steps use seeded (20261013) whole-unit removal.
>     - The 50,000-row floor (stop and ask) is unchanged.
>   - **Own dev, never trained.**
>     - 300 rows per block: DI-KR 300; DI-LANG 150 HoVer + 150 iSarcasm; DI-TS 300, stratified by task.
>     - Each is a seeded (20261013) hold-out of the train split, grouped by source record, drawn before any read:
>       - a GSM8K problem;
>       - a HoVer origin-claim group (mutated claims stay with their origin);
>       - a tweet together with its rephrase;
>       - a tasksource premise.
>     - Each is disjoint from training (by the grouping, and by G13 as a C2 dev target) and from every DI edition
>       (G13 against item e).
>     - The pooled DI own dev joins A42-D 9.3's pooled own dev for the item 9 score.
>
> - **(g) Money and accounts. Changes A42-D 2.1-2.4 under this owner decision ("use the Modal reserve").**
>   - **Caps.**
>     - C2 Modal total ≤ **$45**, which is the goal's existing hard stop. That stop is unchanged and now binds
>       directly.
>     - Training ≤ **$39**.
>     - Every other A42-D 2.1 line counts inside the $45: evaluation ≤ $4, SPEED-3 ≤ $2, reserve ≥ $2 at the
>       training GO, and the DI pilot ≤ $1.
>   - **Ceilings,** fixed at the training GO:
>     - **T_max = min($39, $37 − C2 Modal spend to date)**, where $37 = $45 − $4 − $2 − $2.
>     - **T_core = min($34, $32 − spend)**, as before.
>     - The DI part may use T_max − (the core's realised projection), which is ≈ $5 when the core sits at T_core.
>       `mix_c2.py` projects from real padded tokens (spec 5.5).
>     - A37 (k)'s steps 100-300 stop-and-ask uses this T_max.
>     - After training, each later line runs only if spend to date plus its projection is ≤ $45. SPEED-3 runs last, in
>       full or not at all.
>   - **Relay order.** Free credit only, with balances read live and logged before launch (the 16 Oct figures are
>     planning numbers):
>     1. **mahadikarya2** ($19.09)
>     2. **mahadikarya3** ($13.84)
>     3. **jaypatil-duke** ($8.96)
>     4. **atmosphor** ($3.47)
>     5. **arya-mahadik-ai** ($2.55)
>     6. **mahadikarya44** (~$3, after the DI pilot)
>   - **Covering the later lines.** Evaluation and SPEED-3 take the credit left after training, in the same order. If
>     live free credit cannot cover T_max plus those lines and the $2 reserve, T_max is lowered to fit, and the trim
>     order of (f) applies.
>   - **aryamhd is not in the relay.** It has no free credit and no approved use. This ruling grants none. A card use
>     needs a new owner ruling that names the amount (A42-D 2.4).
>   - **At GO #1,** the request states:
>     - any DI trim from (f);
>     - the dollar figure that would avoid it;
>     - the live balance per account.
>     The owner decides at that GO.
>
> - **(h) How reports label the Decision Index after C2.**
>   - The DI is report-only for C2. It never selects a row, block, candidate, dial, adoption or stage (A42-D 14,
>     as for Jev).
>   - Every C2 DI table marks the **public part** "in-distribution after C2". Two kinds apply:
>     - **in-family:** "same-source train split trained; DI items and their full scored splits excluded by G13".
>       This covers GSM8K, HoVer and iSarcasmEval, for each one that entered.
>     - **task-type:** "same task type trained via DI-TS". This covers the NLI benchmarks ANLI, ContractNLI and
>       NLI4CT, if DI-TS entered.
>   - The public-part average is reported twice: over all benchmarks, and without the in-family ones.
>   - Any C2-vs-Jev or C2-vs-C1 statement about the public part carries the label.
>   - **The 80% private part stays the fair measure** of DI generalisation. A private-part score needs a
>     submission, and that happens only on an owner decision.
>   - The `di_test` (release-v1) numbers of C1 keep their own labels.
>
> - **(i) C2.1 (out of C2 scope, recorded only).**
>   - **Harder same-style program-gold families,** where Claude writes the items and gold comes from a program, never
>     from Claude:
>     - GSM8K-style multi-step math;
>     - CLadder-style causal queries;
>     - MuSR-style narrative logic;
>     - BFCL / When2Call-style tool decisions;
>     - BRIGHT-style reranking;
>     - long-document legal NLI;
>     - chess by construction, such as legal move, mate-in-1 and check, with python-chess.
>   - **The DI-RC and DI-TOOLS tasks.**
>   - **Head and loss ideas:** a Brier term, label-smoothed CE, a calibration temperature, and a decision or readout
>     head.
>   - The C2 recipe (A37 i) is unchanged.
>
> - **(j) Unchanged.**
>   - A42-D 1-14 and A43-A60: every gate, cap and bar, except the row and money caps named in (f) and (g).
>   - The 40/60 split and 1.5× replay.
>   - Both owner GO points.
>   - The 96% usage stop and the 98% ceiling (A47).
>   - The never-open rules (spec 6.5; AC_SEALED_BRIEF; `bench/external_quarantine/**` is readable only by the
>     decontamination program).
>   - The A42-D block text and its sha256.
>   - The GO #1 request lists, for every DI block and source:
>     - realised rows;
>     - drops by step;
>     - the A46 counts;
>     - probe reports;
>     - the pilot verdict;
>     - G13 drops per target;
>     - the HLE gap.
>   - **What this ruling changes:**
>     - A40 (d) and A42-D 1.4: the row cap (f);
>     - A42-D 2.1-2.4: the money caps, T_max, the trim order and the accounts (f, g);
>     - the G13 target registry, which gains `di03_public` and `di_src_splits` (e).
