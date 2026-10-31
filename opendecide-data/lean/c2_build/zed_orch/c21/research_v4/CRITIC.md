# C2.1 COMPLETENESS CRITIC (research_v4)

Author: Opus 5.5 critic subagent. Date: Sun 18 Oct 2026. Task: find what the C2.1 training-side plan
(training_inputs/PLAN_TRAINING_SIDE.md, v3.1) and the research (research_v3/*.md, research_v4/*.md) MISSED for the
best possible C2.1.

Read: PLAN_TRAINING_SIDE.md (whole), l0/G13_TARGET_REGISTRY_DRAFT.md, l0/R5_CANDIDATES_CHECK.md, research_v3
(OWNER_GOALS, ORCHESTRATION_RULES, THINK_MODE_MEASURED, ALREADY_TESTED_C1_OPT whole; recipe and landscape sections 5-6;
the other v3 angle files by heading and keyword search), research_v4 (decision_index whole; code, nlu, safety, tools,
hardest: headline, counts, verification and owner sections, plus keyword search over the full text). Web: 8 fetches or
searches on 18 Oct 2026 (cited inline). Not opened: any "ohs"/"sealed" path, any Jev output, ~/.claude, any dataset
item. No download, no model run, no model API.

Severity: HIGH = C2.1 cannot meet the owner's 18 Oct goals without the fix; MEDIUM = measurable loss or rule risk;
LOW = hygiene. "Evidence" cites a local file and section, or a URL with the fetch date.

---

## 0. The short version (for the owner)

1. The plan has NO public-train-split data at all. P0 is "ONLY CLAUDE-AUTHORED GENERATORS" (plan section 2), the general
   block is 7K Claude-authored rows, and the R5 check released nothing (R5_CANDIDATES_CHECK.md: "ALLOW 0, DENY 13").
   The v4 research then found about 70 candidate public TRAIN sets (after refuters) but none of it is in the plan, the
   names manifest, the mix or the schedule. This is the biggest gap against the owner's "cover all public data,
   train splits only" instruction and the biggest general-accuracy lever (Perplexity Decider v1.2: "A large part of the
   gains are thanks to the tasksource data", research_v4/decision_index.md section 6).
2. The test-split exclusion is not yet safe for the public datasets we would add. Most of the "about 80" Decision
   Index / Nimble / JevBench benchmarks (decision_index.md: 78 rows plus AA-Omniscience = 79) are NOT registered as G13
   targets, and the split-aware tool by default denies a whole dataset once any split is registered
   (R5_CANDIDATES_CHECK.md finding 3). So today the pipeline either leaks (unregistered tests) or blocks every train
   split (registered tests under the strict default). The owner must rule once on split-scoped release.
3. Several decision types a coding agent makes every day have no family: ask-or-proceed is only P1, and there is
   nothing for delegate / compaction-keep / plan-vs-act, merge-conflict choice, compile/type/lint outcome,
   hallucinated-package or nonexistent-API checks, IaC/config review, DB-migration safety, breaking-change (semver),
   dependency-licence compatibility, commit-message-vs-diff, CI-log triage.
4. "Hardest-question projection" exists only as research (hardest.md); it is not in any family spec, and no family has
   a measured difficulty target. The general/NLU side has no hard-extension generators at all.
5. Five cross-file contradictions in verdicts and one wrong citation in the plan (LIMBO numbers) must be fixed before
   anything is built on them.

---

## 1. Gap list

### A. Public TRAIN-split data (owner: "all that data set family should be covered")

A1 (HIGH). No public-data block exists in the plan.
- Evidence: plan section 2 "P0 USES ONLY CLAUDE-AUTHORED GENERATORS ... No external code or text corpus in P0"; MIX "New
  rows about 38K: P0 about 28K; general program-gold about 7K; voice about 3K"; R5 is OWNER-RESERVED (section 2 STATUSES
  CLOSED). R5_CANDIDATES_CHECK.md "R5 releases nothing on today's list". OWNER_GOALS_18OCT.md names "the A61 (b)
  split-aware deny-list for public TRAIN splits" as a lever the planner must list. THINK_MODE_MEASURED.md: "General-
  accuracy levers are data-side only (public train splits if the owner approves, ...)".
- What v4 found that the plan does not use (post-refuter ALLOW-R5 counts): decision_index.md 13; nlu.md 30;
  code.md 12; safety.md 7; tools.md 6; hardest.md 4 (heavy overlap; distinct names about 60-70, UNVERIFIED exact
  dedup count).
- Fix: add a new lane "L-R (public train splits)" and a mix block "R" to sections 2, 5 and 8:
  (a) names manifest v2 with one record per dataset (never a catalogue: R5 check reason CATALOGUE_PER_MEMBER_REQUIRED);
  (b) per dataset: train split only, licence quote, label provenance enum, the A61(b) record, pre-mapper 8.5 PASS,
      guards F1-F10, full-row G13 (see B3), A46-style noise screen (see A5);
  (c) a mapper that recasts each set into C2's rendered Choice / yes-no format with option shuffling, matching
      Perplexity v1.1's "human-labelled public datasets that we converted into Choice and Noul decisions"
      (decision_index.md section 6);
  (d) per-dataset row cap (proposal: at most 3K rows or 5% of block R, whichever is smaller) and a block size set from
      measured usage, not an estimate (memory rule "decide on measured usage"); a G-dev check before and after block R.
  (e) schedule: owner R5 ruling in the Mon 19 Oct message, manifest v2 by Wed 21, mappers by the data freeze.

A2 (HIGH). The tasksource route (the one pool that the top open decision models share) has no plan path.
- Evidence: decision_index.md E1: tasksource-jev-typed-decisions 1M default / 2.58M full rows, per-row licence and
  `license_use` columns; README "Labels come from human annotation or from procedures that verify them" but the card
  shows cc-by-nc-4.0 and "CC BY-NC-SA 4.0 (DPI)" rows and no provenance column. Strands Decider used "119 sources from
  tasksource-jev-typed-decisions" (decision_index.md section 6). R5 check denied it as a catalogue.
- Fix: never take it whole. Build a per-SOURCE allow-list (verified human/program label, permissive licence on the
  source's own page, not an eval corpus, not barred), then pull only those sources' train rows. Each source becomes
  its own manifest-v2 name. Budget a Haiku licence-scout pass over the 751 source values with Sonnet verification of
  every promoted source.

A3 (HIGH). Code realism sets with human code and execution or judge gold are not used anywhere.
- Evidence: code.md section 0 point 1: CodeContests, CodeNet (accept/WA verdicts), APPS train, SWE-Gym, ManySStuBs4J,
  TSSB-3M, LogChunks (only plain ALLOW-R5), Juliet (CC0), DataDog malicious packages. Plan names only SWE-Gym/SWE-smith/
  CommitPackFT (P1) and none of the others (keyword count: LogChunks, Juliet, CodeNet, DataDog, ManySStuBs, TSSB all 0
  in the plan).
- Fix: add P1 transfer slices with program gold only:
  - T58 SOLUTION-VERDICT: "does this human submission pass?" from judge verdicts (CodeNet / CodeContests correct and
    incorrect solutions). Gates: problem-level G13 against EquiBench OJ pairs, CodeMind sources and LiveCodeBench;
    date cut-off 2022-11-30 (code.md cross-cutting risk 2); APPS without Kattis (CC BY-SA).
    CodeNet data licence is still UNVERIFIED at a primary page: the GitHub repo shows only "Apache-2.0 license" for
    the tools (https://github.com/IBM/Project_CodeNet, fetched 18 Oct 2026); secondary reports say CDLA-Permissive-2.0
    (https://www.opensourceforu.com/2021/07/linux-launches-new-license-agreement-for-open-source-datasets/, searched
    18 Oct 2026). CDLA-Permissive-2.0 is not on the owner's list by name: owner question.
  - T62 FLAKY-OR-REAL gets LogChunks (CI failure chunks, CC BY 4.0) and FlakeFlagger labels (decision_index.md E12).
  - T63 DEP-RISK gets DataDog malicious-package labels (labels/metadata only).
  - T65 VULN-SYNTH gets Juliet (synthetic CWE good/bad functions, CC0; F2 no CVE ids).
  - T57 LOCALISE realism from ManySStuBs4J / TSSB-3M single-statement fixes (diffs only).

A4 (MEDIUM). General program-gold generators already exist under Apache-2.0 and are ignored.
- Evidence: nlu.md C26 and hardest.md 1.11: Reasoning Gym, 100+ tasks, program verifiers, Apache-2.0; exclude
  gsm_symbolic (GSM8K-derived, so the barred A61(a) gsm8k HIT) and codeio ("transformed by an LLM"). bAbI generator
  (C25), FLD (C24), DeepMind Mathematics (D2), BoardgameQA (E7), CLadder generator (OWNER; drop the GPT-4 nonsense
  variant). Plan section 2 general rows are Claude-authored only.
- Fix: allow vetted third-party GENERATORS (code, not item files) in the general block under a per-task allow-list:
  every task that wraps a public dataset (ARC-style, GSM-style, any benchmark-derived task) is excluded; difficulty
  set by program parameters (hardest.md 1.11 target 1). Register Reasoning Gym task names as a manifest-v2 entry.

A5 (MEDIUM). The A46 replay noise screen covers only C2 replay rows, not new public human-label rows.
- Evidence: memory/A46 "screen ALL human-label replay rows before training; drop only"; plan section 2 "Replay of C2's
  mix with drop-only steps (A46, p_g < 0.2 human rows, pg_anchor)". tools.md row 82: BANKING77 "about 14% reported
  label noise". code.md: CommitPackFT selection heuristics.
- Fix: apply the same drop-only screen (C2 reads on od-l4b, p_g < 0.2) to every block-R human-label row; log drops per
  dataset; a dataset losing more than 15% of rows goes to Opus review.

A6 (MEDIUM). Large-label-set and multi-label formats are not designed.
- Evidence: BANKING77 is 77-way, CLINC150 150 intents + OOS, MASSIVE 60 intents (decision_index.md rows 6-7, N-2);
  DI 0.3 includes SATA-Bench select-all-that-apply (row 18); JevBench types "Choice, Noul, and Score" weighted equally
  (decision_index.md 2.4, BenchLM). Plan readout is "yes/no or pick-one" and says nothing about k > letters, multi-
  label or Score (ordinal) outputs.
- Fix: G0-lite rule for big label sets: present the gold plus k-1 hard distractor labels chosen by program (nearest
  intents by label-name or train-set confusion), k in {4, 8}, rotating; add a yes/no-per-option recast for multi-label;
  confirm whether C2's renderer already supports Score items (UNVERIFIED from files I may read) and, if not, add an
  ordinal-bucket Choice recast.

### B. Test-split exclusion (owner: "all the public data set, but not the testing data set")

B1 (HIGH). Most of the ~80 benchmark test splits are not registered as G13 targets.
- Evidence: G13 registry sections A-C hold 32 eval names, mostly agent/security; decision_index.md section 1 item 6:
  only When2Call, BFCL, CRUXEval, WildGuardTest, LiveCodeBench, JevBench coding are present; missing HLE,
  AA-Omniscience-Public, every DI 0.3 tested split, the 13 Nimble subsets, all JevBench variants. safety.md section 0
  point 6 adds XSTest, OR-Bench, JBB-Behaviors, HarmBench, StrongREJECT, SORRY-Bench, AgentHarm, ASB, Agent-SafetyBench,
  ASSEBench, TS-Bench, OS-Harm, SafeArena, RedCode, SABER, Aegis test, ToxicChat test, BeaverTails test, Lakera b3/PINT,
  BrowseSafe test, PromptShield eval. tools.md section 5 adds AppWorld, ToolBeHonest, ACEBench, ToolTalk, API-Bank eval,
  ToolSandbox, MCPMark, LiveMCPBench, Toolathlon, WildToolBench, Live API-Bench dev, ParamBench test. hardest.md
  section 2 adds ProcCtrlBench, CodeSense, LIMBO, Ambig-SWE, SWE-ABS, UTBoost, SWE-bench+, MAST-Data, BBEH, ZebraLogic.
  code.md section 4 adds EquiBench pair ids and CodeMind source ids at problem level.
- Fix: L-E registers all of these (names, versions, URLs, exact split names) BEFORE manifest v2 is frozen; the
  row-start guard refuses any block-R job until the registry sha includes them. One merged list, deduplicated by
  Haiku, confirmed by Opus.

B2 (HIGH). The split-scope rule is undecided and its default blocks everything the owner wants.
- Evidence: R5_CANDIDATES_CHECK.md finding 3: "a registry entry that targets only named splits of a larger dataset ...
  denies the whole dataset by default"; `--split-scoped-release` "is tested but off". Owner's 18 Oct words: use public
  data, not the testing data.
- Fix: put one explicit ruling in the Mon 19 Oct owner message: "release the TRAIN split of a dataset whose test/dev
  split is an eval target, if (i) the train split is disjoint from every registered test/dev item by full-row G13,
  (ii) the dataset is not one of the A61(a) HITs, and (iii) any eval on that dataset is reported as 'train split seen'".
  Default recommended: YES with these three conditions (it is what Perplexity v1.2 did: "decontaminated against the
  test sets", decision_index.md section 6).

B3 (HIGH). G13 as planned is a 200-row pilot; public data needs full-row checking.
- Evidence: plan section 1E "a 200-row G13 pilot before full generation"; section 2 "more than 1% of rows hit ... sends
  the generator back". That design fits generators, not imported corpora where a few copied test items are the
  failure. Known cross-dataset routes: HoVer is built from HotpotQA (nlu.md 0.5), Lila contains GSM8K, MuSiQue from
  SQuAD/NQ (decision_index.md row 44), Reasoning Gym gsm_symbolic, APPS/CodeContests share 3,392 problems (code.md).
- Fix: every block-R row and every C2 replay row goes through G13 against the full registry (not a sample), with
  near-duplicate methods, and also against train-to-test transitive sources (e.g. HotpotQA train vs HoVer dev).
  Measure Mac G13 throughput on 10K rows first (single-resource lock, ORCHESTRATION_RULES rule 3) and publish the
  queue length; if it binds, add a second G13 host rather than sampling.

B4 (MEDIUM). Replay rows were never checked against the new targets.
- Evidence: plan section 5 MIX: replay ratio 1.0x-1.5x of C2's mix; G13 targets added in C2.1 (OHS-5, AmPermBench,
  injection environments, and the B1 list above) postdate C2's G13.
- Fix: run the new-target G13 over the whole replay set once, drop-only, log per family.

B5 (MEDIUM). "Train split seen" reporting is not in the plan.
- Evidence: THINK_MODE_MEASURED.md separates "sets seen in training" from "unseen sets" on Nimble (+0.0 vs +4.7);
  JevBench (fstandhartinger) README: "Training on the public split must be disclosed" (decision_index.md 2.4).
- Fix: every public-benchmark report row carries a seen/unseen flag; headline claims rest only on OHS-5 and unseen
  sets.

B6 (LOW). Manifest v1 misses three A61(a) names.
- Evidence: R5_CANDIDATES_CHECK.md finding 1: md_worldbank, md_usgs, md_cma absent from
  `excluded_even_if_R5_adopted`; finding 2: md_* alias keys are guesses.
- Fix: add them in manifest v2; Opus checks aliases against the A61(a) record.

### C. Decision types an AI coding agent makes that have no family

Plan taxonomy G1-G8 is good on safety, but these everyday coding-agent decisions have no P0 or P1 family. Each fix
below is a Claude-authored generator with program or execution gold (allowed under the rules).

C1 (HIGH). Ask-or-proceed is only P1 (T59), and G4's delegate / compaction-keep / plan-vs-act / next-step have no
family at all.
- Evidence: plan section 1A G4 lists them; section 1B P0 has none; hardest.md section 0: "No published difficulty study
  was found for: plan mode vs act, deny-and-continue vs escalate thresholds, argument grounding ..., commit/PR
  readiness, and 'what to keep at compaction'". Owner strategy: "#1 decision model for coding agents"
  (memory strategy-agentic-coding).
- Fix: promote T59 ASK-OR-PROCEED to P0 (gold: a generated spec with k admissible interpretations; ASK iff the
  interpretations lead to different actions with non-reversible cost); add T60 CONTROL-NEXT (delegate vs do; keep vs
  drop at compaction with gold = whether a later step depends on the fact; plan vs act with gold from a generated
  task-risk spec). Keep both inside the TRAINING FLOOR count or state explicitly that they do not count.

C2 (MEDIUM). Compile / type-check / lint outcome ("will this build pass?") is missing.
- Evidence: T42c covers runtime output, exceptions, equivalence and test failure only (plan section 1B item 8).
- Fix: add a T42c sub-head "will it compile / type-check" with gold from the pinned toolchains already in the plan
  (Python 3.12 + a permissive type checker, Node 24 tsc, Go 1.26 vet). mypy is MIT (code.md mentions only its mixed
  component licence: UNVERIFIED which components). Never ShellCheck or hadolint as gold (both GPL-3.0, from memory:
  UNVERIFIED today).

C3 (MEDIUM). Hallucinated package / nonexistent API decisions are missing.
- Evidence: plan has T63 DEP-RISK (typosquat) only. USENIX Security 2025 "We Have a Package for You!": 19.7% of samples
  contained a hallucinated package, open models about 21.7% vs commercial 5.2%, 43% of hallucinated names repeat on
  every rerun (secondary summaries only: https://labs.cloudsecurityalliance.org/research/csa-research-note-slopsquatting-ai-supply-chain-20260419/,
  searched 18 Oct 2026; primary paper not read, UNVERIFIED); a 2026 replication reports 4.62-6.10% for newer models
  (https://www.alphaxiv.org/abs/2605.17062.md, search snippet only, UNVERIFIED).
- Fix: T63 sub-family "EXISTS?": does package P / symbol S exist in registry snapshot R or library version V; gold from
  an offline snapshot of names we generate in the seeded namespace plus introspection of the pinned toolchain's own
  standard libraries. Conflation-style and cross-registry near-misses as hard negatives.

C4 (MEDIUM). Infrastructure-as-code and config review is missing.
- Evidence: G1 covers infra ACTIONS (shell), not reviewing a Terraform plan, Kubernetes manifest, Dockerfile or CI
  workflow before apply. Keyword count for Terraform/Dockerfile/Checkov in plan and research: 0. Checkov is
  "Apache-2.0 license" and scans Terraform (incl. plan JSON), Kubernetes, Helm, Dockerfile, GitHub Actions and more
  (https://github.com/bridgecrewio/checkov, fetched 18 Oct 2026).
- Fix: T67 IAC-GATE: generated specs (resource, change type destroy/replace/update, exposure, privilege), rendered to
  Terraform plan JSON / manifests / workflows; label from our own rule table; Checkov used only as a round-trip
  validator (as tree-sitter-bash is for T50). Labels like "destroy in production lane" reuse T50's reason head.

C5 (MEDIUM). Database migration safety is missing.
- Evidence: plan uses sqlglot for SQL parsing; no family judges a schema migration (table lock, NOT VALID, concurrent
  index). squawk "Apache-2.0, MIT" checks lock-taking migration operations
  (https://github.com/sbdchd/squawk, fetched 18 Oct 2026).
- Fix: fold a MIGRATION sub-block into T50 or T67 (ALLOW / ASK / BLOCK by lock class and table size spec); squawk as a
  validator only.

C6 (MEDIUM). Merge-conflict resolution, breaking-change (semver) and commit-message-vs-diff decisions are missing.
- Evidence: keyword count 0 for merge conflict and semver across plan and research; CommitPackFT appears only as a
  P1 source (plan section 2) with no family attached.
- Fix: T66 REVIEW-GATE (P1) gains three heads: (a) pick the correct resolution of a generated conflict (gold = the
  resolution under which both sides' tests pass, executed on od-sbx1); (b) "is this change breaking for callers?"
  (gold = a generated caller suite run on old vs new API); (c) "does this commit message describe this diff?" from
  CommitPackFT with a permissive-licence whitelist (decision_index.md E9), negatives by swapping messages across
  same-repo commits.

C7 (LOW). Dependency-licence compatibility is missing.
- Evidence: a common agent decision ("may I add this dependency?"); keyword count 0. SPDX license-list-data does not
  state a data licence on its README ("Please see the respective repositories for licensing information",
  https://github.com/spdx/license-list-data, fetched 18 Oct 2026): UNVERIFIED.
- Fix: small T63 head with gold from an Opus-written compatibility table over licence IDs only (IDs are facts; no
  SPDX text copied).

C8 (LOW). Phishing / malicious link verdicts and direct (user-turn) injection are thin.
- Evidence: DI 0.3 includes PhishNChips (decision_index.md row 9, DENY as data); T41c is indirect injection only;
  K/X static-attack ASR is a gate (plan section 3) but no family trains direct attacks; safety.md ALLOW-R5 has
  Gandalf ignore-instructions and summarization (MIT, human prompts).
- Fix: T41c gets a direct-injection slice from Gandalf (attack positives) with Claude-authored benign twins at 50%;
  T53's destination-cue machinery gets a phishing-URL head.

### D. Difficulty ("projection of the hardest question in that family")

D1 (HIGH). hardest.md mechanisms are not in any G0-lite.
- Evidence: hardest.md was written 18 Oct after plan v3.1; plan keyword count for its mechanisms (scope inversion,
  contextual warning, equivalent-effect channels, first-wrong-step) is 0. hardest.md 1.12 cross-cutting patterns
  (alarming/calm surface x risk present/resolved quads; decisive-variable-only edits).
- Fix: each P0 G0-lite gets a "difficulty ladder" section that names its hardest.md mechanisms, a level parameter per
  mechanism, and a target share at the top level (proposal at least 25% of rows at the top two levels), with the
  1.12 quad structure mandatory for T50/T51/T53/T41c/T56.

D2 (HIGH). No measured difficulty target; hard rows are found only after the fact.
- Evidence: plan section 5 HARD NEGATIVES: hard bin from C2's errors (A42-D 6), hard at most 30%, easy at most 25%;
  no family states what base-4B / C2 accuracy its pilot must show.
- Fix: in every 1,000-row pilot, read base 4B and C2 on od-l4b and require the top difficulty level to sit below a
  pre-written accuracy (proposal: C2 at most 70% on the top level, the BBEH-style bar of hardest.md 1.11 applied to
  OUR own model, which the no-big-teacher rule allows). If a level is easy, raise its program parameter, do not
  filter by model (keeps "no model-in-the-loop difficulty", hardest.md 1.11 target 1).

D3 (HIGH). The general / NLU side has no hard-extension generators.
- Evidence: general rows list only "multi-step arithmetic, logic, causal and temporal reasoning, tables" (plan section
  2). DI 0.3 areas include Language Understanding 25.8% and Retrieval and Classification 20.0%
  (decision_index.md 2.2). Owner: public data plus synthetic data that projects the hardest questions per family.
- Fix: for each block-R family, one Claude-authored hard-extension generator that keeps the public format and pushes
  the documented hard mechanism, with two independent Claude solvers plus Opus adjudication where program gold is
  impossible (owner rule: Claude authors the data):
  - NLI / claim verification: one-edit negation, quantifier, scope and date flips (CONDAQA's mechanism, nlu.md B21).
  - Intent / OOS: near-domain out-of-scope queries and confusable-intent pairs (CLINC150 OOS idea).
  - Reading QA / abstain: unanswerable twins whose answer span is removed (SQuAD 2.0 mechanism, built on our own
    passages, never Wikipedia SA text).
  - Faithfulness: summary or answer with one unsupported claim injected at a known span (RAGTruth / SummEval
    mechanism; both DENY as data, decision_index.md rows 31, N-11).
  - Reasoning: first-wrong-step traces, conflicting rules with a genuine "unknown" (hardest.md 1.11 targets 2-3).
  - Select-all-that-apply, ordinal severity and enum extraction formats (SATA-Bench row 18; JevBench families,
    decision_index.md 2.4).

### E. General-accuracy levers inside the rules (owner: at most 2-3 points behind Jev on G)

E1 (HIGH). The plan gives no projected G gap with and without block R.
- Evidence: OWNER_GOALS_18OCT.md requires "(2) give the projected gap with and without the owner-reserved levers".
  THINK_MODE_MEASURED.md: Decision Index sample C1 54.83 vs Jev 59.51 (-4.7); Nimble unseen sets 70.4 (C1 fast path).
  Plan section 3 G ship rule: Jev - C2.1 <= 4.0 pp.
- Fix: before GO #1, measure base 4B, C1 and C2 on a G-dev made of unseen public sets, then project the gap for
  (a) no block R, (b) block R with permissive sets only, (c) plus the SA ruling. Honest range only; no claim.

E2 (MEDIUM). Abstention / non-hallucination behaviour is not trained.
- Evidence: AA Decision Index = 50% knowledge-and-abstain (Omniscience 12.5 accuracy + 12.5 non-hallucination; HLE)
  with no train split (decision_index.md 2.1 and section 1 item 2); memory: JevBench v1.5.4 "soft yes/no = abstain
  penalty". Plan has no "insufficient information" option outside T54/T55.
- Fix: an ABSTAIN head across general rows: an explicit "cannot be decided from the given information" option at a
  controlled 10-15% rate, gold by construction (needed fact removed), plus CLINC150 OOS and Qasper unanswerable
  (ALLOW-R5 in nlu.md). Calibrated temperature per type already exists; add a per-type abstain-threshold report.

E3 (MEDIUM). LoRA target modules: the "parity" reason for not touching the linear-attention layers is weak.
- Evidence: plan section 5: "q/k/v/o LoRA touches only 8 of 32 layers ... keep C2's set for parity"; the serving path
  uses MERGED bf16 weights (section 6), so extra LoRA targets do not change the S1 serving graph. recipe.md section 6
  open question: "Should DeltaNet in_proj/out_proj be LoRA targets? ... ask the person who built C2."
- Fix: record C2's actual module list; if it lacks the 24 linear-attention layers' projections, run one cheap
  ablation inside the R1 cap (or state why not). Gain UNVERIFIED.

E4 (MEDIUM). Multilingual decisions are absent.
- Evidence: Nimble tests MASSIVE de-DE as well as en-US (decision_index.md N-2); MASSIVE text is CC BY 4.0 for every
  locale (tools.md row 84, nlu.md F3; SLURP audio is CC BY-NC and stays out). Plan and voice are English-only.
- Fix: ask the owner whether non-English is in scope; if yes, add MASSIVE non-English train text (block R) and report
  per-language. If no, say so in the claims.

E5 (LOW). Long-document handling for imported sets is unspecified.
- Evidence: plan token mean at most 800, cap 1,536 on at most 10% (section 1E); ContractNLI full NDAs, Qasper papers,
  CUAD contracts are far longer (nlu.md rows; sizes UNVERIFIED).
- Fix: mapper rule: program span selection (gold-bearing span plus distractor spans), never truncation that can cut
  the evidence; log rows dropped by length.

### F. Eval coverage

F1 (HIGH). No general-accuracy public eval exists besides the sealed OHS-5 G.
- Evidence: G13 registry A-C hold no general NLU set (nlu.md section 0 item 1); plan claims rest on OHS-5 G (section
  3). Plan section 4 is outside my read scope, so this is checked only against the registry.
- Fix: add a report-only "public-G panel" of UNSEEN public sets (never trained on, per B5) to L-E, with Jev read once
  by our client; it is the early-warning signal for E1 before the sealed look.

F2 (MEDIUM). Several P0 families have no public eval at all.
- Evidence: Tier-1 list (G13 A1-A6) is When2Call, AgentDojo, InjecAgent, NotInject, ATBench-Codex, ATBench. No public
  set exists for T50 (AmPermBench is C1 "NC or unclear"), T55 (LIMBO, ToolMaze barred as data; hardest.md moved LIMBO
  to DENY), T56 done-claim (code.md section 0 point 5: "no public human-labelled claim vs evidence set").
- Fix: state per family "OHS-5 only" in the report; register CredLeakBench (T53), Impossible-* and EvilGenie (T56g),
  SWE-bench-family patch verdicts (T57) as report-only where licences allow; never invent a public number.

F3 (MEDIUM). Vision is a goal dimension with no C2.1 data and no v4 research angle.
- Evidence: ALREADY_TESTED_C1_OPT.md: vision side-bench C1 77.7 vs Jev 1.14 85.1; "image decision data later";
  OWNER_GOALS_18OCT.md: "On everything else C2.1 must beat Jev". Plan section 7: "Images: attached unchanged".
  research_v4 angles: code, decision_index, hardest, nlu, safety, tools (no vision).
- Fix: either run a vision licence/train-split research angle now (same rules) or write in the plan that C2.1 does
  not target the vision gap and the claim excludes vision. Owner decision.

### G. Licence and provenance rulings the plan has not bundled

G1 (HIGH). One bulk owner question set is needed before any block-R mapper.
- Evidence: nlu.md section 0 item 3 (CC BY-SA blocks SNLI, MNLI, BoolQ, SQuAD, HotpotQA, ARC, DROP, FEVER, VitaminC,
  AmbigQA, Spider); decision_index.md section 11 (tasksource, When2Call train, WildGuardMix train, SA sets, LLM-output-
  with-human-label sets); safety.md section 9; code.md section 4 item 2 and cross-cutting risk 1 (competitive-
  programming site terms); nlu.md 9.4 (PAWS custom notice, PIQA AFL-3.0); Wikipedia text inside "permissive" sets
  (nlu.md 0.4; decision_index.md rows 44, E4); CDLA-Permissive-2.0 (A3).
- Fix: one owner message, one line each, with a recommended default:
  (1) split-scoped release (B2) YES with conditions; (2) CC BY-SA train data: owner choice, default NO (not on list);
  (3) Wikipedia-derived passages inside CC-BY/Apache sets: default NO unless the passages can be replaced;
  (4) human labels on LLM-written inputs (HelpSteer2, Aegis, RAGTruth): default NO (rule as written);
  (5) When2Call train / WildGuardMix train: default NO (rule as written; they are the two biggest AA levers, so ask);
  (6) custom permissive notices (PAWS, PIQA AFL-3.0, CDLA-Permissive-2.0): default YES only for CDLA-Permissive-2.0
      and the PAWS notice if the owner agrees they are permissive; (7) competitive-programming problem statements:
      owner choice; (8) tasksource per-source route (A2): default YES.

### H. Contradictions and errors to fix before building

H1 (MEDIUM). Verdict conflicts across v4 files (same dataset, different verdict):
- BANKING77: ALLOW-R5 (decision_index.md row 6; nlu.md F1) vs OWNER (tools.md row 82, label provenance UNVERIFIED,
  ~14% label noise).
- CONDAQA: ALLOW-R5 (nlu.md B21) vs OWNER (decision_index.md E4: Wikipedia passages are CC BY-SA).
- Civil Comments: ALLOW-R5 (decision_index.md N-7; safety.md S140) vs OWNER (nlu.md F6: it is one of the Nimble eval
  sets, so A61(b)).
- CodeContests: ALLOW-R5 conditional (code.md) vs OWNER (decision_index.md E8, third-party problem rights).
- HackAPrompt: ALLOW-R5 (safety.md S40) vs OWNER (hardest.md: labels depend on OpenAI/FlanT5 completions).
- SWE-smith: P1-conditional (plan section 2) and ALLOW-R5 narrow (hardest.md) vs OWNER (code.md row 28).
- FLD: ALLOW-R5 (nlu.md C24) vs OWNER (decision_index.md E6, FLD.v2 card states no licence): different versions;
  name the exact one.
- decision_index.md section 9 still prints the superseded researcher list (MuSiQue, CONDAQA, FOL-nli, CodeContests as
  "ALLOW-R5 unconditional").
- Fix: a Sonnet merge pass writes one table, strictest verdict wins until Opus rules; the manifest v2 uses only that
  table.

H2 (MEDIUM). Plan T55 cites LIMBO wrongly.
- Evidence: plan section 1B item 6: "frontier models duplicated a lost-ack write in 56-74% of cases"; hardest.md
  section 5 refuter: "the plan's 56-74% is late commit (56%) and redelivery (74%); lost-ack is 0.5%".
- Fix: correct the sentence; the AMBIGUOUS-WRITE class design is unchanged.

H3 (LOW). nlu.md says nine Nimble sets are unknown, but decision_index.md section 5 lists them.
- Evidence: nlu.md 9.5 vs decision_index.md section 5 (N-1..N-11 plus rows already in section 4).
- Fix: intersect nlu.md's ALLOW list with the Nimble list (MASSIVE, Civil Comments, PAWS, BoolQ, SQuAD 2.0,
  MultiNLI, PubMedQA, VitaminC, Aegis, HelpSteer2, SummEval) and mark those "eval corpus, A61(b)".

### I. Process

I1 (MEDIUM). 8.5 is a single orchestrator step "once before any mapper"; with about 60-70 new sources it becomes the
critical path.
- Evidence: plan section 2 8.5 PROCEDURE; ORCHESTRATION_RULES table (8.5 is Opus orchestrator work).
- Fix: batch 8.5 by source group, publish a schedule with the measured time per source from the first batch.

I2 (MEDIUM). The shed order sheds general rows third (plan section 8 USAGE), which is the block that most moves the
owner's binding G rule.
- Fix: put block R and general rows after wave-C (P1) families and the voice pool, but before training lanes only if
  measured G-dev says they help (E1).

I3 (LOW). Research completeness: angles never run in v4: vision (F3), multilingual (E4), coding-agent everyday
decisions outside security (section C), code-review human preference (code.md 1G exists but is not summarised as
a candidate list). code.md section 3 also lists about 18 names "not opened at all" (PySStuBs, D2A, Bears, Vul4J,
Avatar, BigCloneBench, POJ-104, DeepFix, GHALogs, Defexts, Megadiff, CanItEdit, SWE-Fixer, SWE-Factory,
CodeSearchNet, OpenCodeReasoning ...).
- Fix: one more Sonnet research pass on exactly these names and angles, same rules, refuter included.

---

## 2. Coverage matrix for the ~80 Decision Index / Nimble / JevBench rows (route per benchmark)

Totals after refuters (decision_index.md section 9): 78 rows + AA-Omniscience = 79; ALLOW-R5 13, OWNER 24, DENY 41.
Every row gets exactly one route. Test/dev splits are G13 targets in every route.

| Route | Benchmarks (examples from decision_index.md) | What C2.1 does |
|---|---|---|
| R-train (ALLOW-R5) | BANKING77 (after H1), CLINC150+OOS, Amazon ESCI (train ids minus the kit's selected rows), ChessBench, ContractNLI (EDGAR docs only), WinoGrande, MASSIVE text, New Yorker captions (text), BoardgameQA, Juliet, CommitPackFT (whitelist) | Block R, train split only, full G13, A46-style screen, "seen" flag in reports |
| Owner ruling | SA sets (BoolQ, SQuAD 2.0, VitaminC, MultiNLI, ARC, AmbigQA, SGD), LLM-input sets (HelpSteer2, Aegis, RAGTruth, HellaSwag), When2Call train, WildGuardMix train, tasksource, PAWS, PubMedQA, CLadder, NLI4CT, Humicroedit, FLD.v2, FOL-nli, CodeContests, MuSiQue, CONDAQA, CFPB, GLUE | G1 bundle; default NO except where marked |
| Skill analogue (DENY as data; test-only, NC, LLM-made or barred) | BFCL and When2Call test -> T54; home-appliance simulator -> our own device-control simulator generator (clean-room); BRIGHT/ESCI-style relevance -> a reasoning-relevance generator; BBH/BBEH-style -> Reasoning Gym tasks minus excluded ones + hardest.md 1.11 targets; MuSR -> our own multi-step narrative generator with program truth; SATA-Bench -> select-all format (D3); CRUXEval -> T42c; RAGTruth / SummEval -> faithfulness generator (D3); PhishNChips -> phishing head (C8); FinEntity / ACOS / VAST -> Claude-authored targeted-sentiment and stance items (two-solver gold); GSM8K, HoVer, iSarcasmEval -> nothing derived from them (A61(a) barred) | Clean-room; mechanism only, never items, entity names, ID patterns or phrasing |
| Not coverable by data | HLE, AA-Omniscience, GPQA, MMLU-Pro (knowledge), private 80% of DI 0.3 | Abstain head (E2) and calibration only; report honestly |

## 3. What is NOT a gap (checked, already handled)

Think tier (removed, THINK_MODE_MEASURED.md); FP8 and serving dials (ALREADY_TESTED and R8/R12); option-order
invariance; trivial baselines; shortcut probes with numeric bars; clean-room against benchmark items; barred-tool list
(bashlex, TruffleHog, AgentTrust); sandbox spec; voice recipe and V2-lite; agent-trajectory safety data (safety.md
confirms none passes the rules, so Claude-authored T50/T51/T53/T41c stays right); tool-calling corpora (tools.md
confirms all are LLM-made, so clean-room T54/T55/T56 stays right).
