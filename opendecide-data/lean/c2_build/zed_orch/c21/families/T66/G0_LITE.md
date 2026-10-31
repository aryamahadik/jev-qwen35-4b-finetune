# G0-LITE T66 REVIEW-GATE: merge head, semver head, message head (+ CommitPackFT realism slice) (lane L-P; P1 wave A; clean-room; draft for Opus approval, target Mon 19 Oct 2026)

Author: Sonnet 5.5 high (L-P G0-lite writer), Sun 18 Oct 2026. Design only: no rows, no generator code, no download, no execution, no model call, no Modal.
Status: DRAFT 1. Every number below is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus.
Read for this file: PLAN_TRAINING_SIDE.md (sections 1 B.8-B.9 and C, 2, 5, 8, 16), LANE_L-P.md, excerpts/codeexec_s5.md, families/T42c G0-lite and addendum (witness rules, ladder, check-at-generation), families/T57 header, families/T50/G0_LITE.md (format), families/G0_APPROVALS_v32.md (GV1-GV9), families/LR/G0_LITE.md (rows LR-11, LR-B3), C2_1_PUBLIC_TRAIN_INVENTORY.md (C13, section 4 T66 row), l0/NAMES_MANIFEST_V1_1.json (structure only). NOT opened: any path containing "ohs" or "sealed", C2_1_PLAN_v3.md, any plan SKEPTIC file, OHS5_BRIEF_DRAFT.md, any T27/T40-T46/T42/T43 generator, template or wording pool, mutate.py, any dataset file (CommitPackFT or other), benchmark item text, ~/.claude. Dataset field names that appear below come from memory and are marked UNVERIFIED.
Shared rulings carried (index): G1 solver B is CODE; G2 data-audit gates are PRE-FREEZE; G3 no free pilot tuning, ONE combined fix; G4 no head or sub-block rolls alone; G5 one probe harness (97.5th-percentile bound, permutation 0.50 +- 0.03 and leak-power >= 0.80 checks, GBT advisory); G6 tokens; G7 secondary heads (T66 has none); G9 cross-family label consistency (T66 is not an action gate; not in the test); G10 decision_spans (no natural-language user utterance; nothing to export); GV1-GV4 (A10 / A14 not carried; GV4 binds); GV5 (a G13 hit retires the spec and the whole group); GV6, GV7 (not applicable); GV8; GV9.

## 0. One-paragraph summary

A 4B reads a small code-review situation and answers one question with one token: (MERGE) does this proposed resolution of a merge conflict make BOTH sides' tests pass; (SEMVER) is this API change breaking for the callers shown; (MSG) does this commit message describe this diff. Gold is execution in the od-sbx1 sandbox (MERGE, SEMVER, and the behaviour probe that marks a hunk substantive for MSG) or construction (MSG pairs by message swap). A realism slice of 800 CommitPackFT rows (via L-R, per-repo licence whitelist) feeds the message head with human text and diffs. No label is ever set or changed by a model.

## 1. Decision and label set

| Head | Question form id | Generated rows | Labels | Gold |
|---|---|---|---|---|
| MERGE | T66-Q-MERGE | 300 | YES (both sides' shown tests pass on the resolved file) / NO | sandbox execution: side-A tests and side-B tests on the candidate, 3 identical runs |
| SEMVER | T66-Q-SEMVER | 300 | BREAKING (at least one shown caller fails on the new API) / SAFE | caller suite generated from the shown call sites, run on the old and the new API, 3 identical runs |
| MSG | T66-Q-MSG | 200 | YES (describes) / NO | construction: own message vs a swapped message; "substantive hunk" fixed by execution (section 2.3) |
| MSG-REAL (P1-realism, L-R LR-11) | T66-Q-MSG | 800 | YES / NO | the dataset's own message vs a message swapped from another commit of the same repo (both dataset text); counted in T66, outside the 800 generated |
Binary heads shuffle the option order per row; 20% extra order-invariance copies are mix-level, not counted.
No secondary head (G7). The product maps these facts to review actions elsewhere; T66 labels no permission, so no ALLOW / ASK / BLOCK option appears (K21).

## 2. Gold method; solver A and independent solver B

### 2.1 MERGE

Spec: a base module (application-style, 20-45 lines, seeded names), a side-A change and a side-B change that conflict textually (conflict kinds CF-1 adjacent-line edits, CF-2 same-line edit by both, CF-3 one side renames a symbol the other uses, CF-4 one side changes a signature the other calls, CF-5 both add to the same list / table / dispatch, CF-6 reorder vs edit, CF-7 one side deletes a block the other edits), a reference merge (generator-built, RK5), and one candidate resolution per row from registered kinds: RK1 take A, RK2 take B, RK3 keep both, A first, RK4 keep both, B first, RK5 reference merge, RK6 reference merge with a behaviour-preserving rewrite (rename of locals, reorder of independent statements; transform ids reused from the T42c EQ-YES list, written again here by the L-P builder), RK7 semantic break (a guard, condition, field or ordering of one side altered or dropped; parses and runs, breaks one side), RK8 syntax or compile break.
Tests: SIDE_TEST_A (<= 14 lines) exercises side A's NEW behaviour; SIDE_TEST_B exercises side B's. Both are SHOWN in the row, and they are exactly what is executed, so the label is derivable from the row. Strength rules (K2): A-tests fail on the base and on the B-only version and pass on the A-only version; B-tests likewise; both suites pass on RK5.
Witness: both suites run on the candidate three times in the sandbox (runner.pytest / runner.node_test / runner.go_test / runner.bash_posix_test from the L-0 image record); YES iff every test of both suites passes on all three runs; three identical outcomes or the row is dropped. The spec EXPECTATION is recorded where the generator knows one (RK5 expects YES; RK1, RK2 expect NO unless the conflict kind makes one side a no-op; RK3 / RK4 expectation depends on the conflict kind); an unexpected result is dropped and counted (this also catches generator bugs).
Solver B = a program from a separate Sonnet high session that sees only this file and the row schema: it parses the RENDERED row (conflict view, tests, resolution), rebuilds the resolved file and both suites with its own driver per language (different working-directory layout, test order reversed, environment scrubbed independently), executes through the same sandbox interface, and compares. Agreement among A, B and the spec expectation on 100% of kept rows; disagreements dropped and counted.

### 2.2 SEMVER

Spec: an old API (function or small class, 6-20 lines, with a short docstring and the declared contract), a new API, 2-5 caller call sites shown as CALLER_SNIPPETS (each written against the OLD API and turned by program into an assertion test), optionally a declared version bump (patch / minor / major) in 50% of rows. Change kinds SV-C1..SV-C12: renamed parameter; reordered parameters; new required parameter; new optional parameter (SAFE); changed default; return shape changed (tuple to mapping, narrowed or widened type); exception class changed; edge-input behaviour changed (a shown caller hits it, or does not); function removed or moved; stricter validation (breaking only if a shown caller passes a now-rejected value); internal refactor (SAFE); added overload or alias (SAFE).
Witness: the caller suite passes on the old API (gold-sanity) and runs on the new API three times; BREAKING iff at least one shown caller test fails on all three runs; SAFE iff all pass on all three runs. The label is about THE SHOWN CALLERS (the question says so); hidden callers do not exist in the row.
Declared bump (when shown) is a decoy: its agreement with the truth (bump major <=> BREAKING) is 50% +- 5 pp, so the bump is not a cue (K6). Solver B = program that rebuilds the callers' tests from the rendered snippets with its own harness and runs old and new in a fresh container; 100% agreement.

### 2.3 MSG (generated) and MSG-REAL

Generated diffs: a base module with a change spec of exactly ONE substantive hunk plus 0-2 trivial hunks (formatting, comment, import order). Registered change kinds CH-1..CH-10 (add guard, fix off-by-one, rename symbol, extract helper, change default, add parameter, remove dead branch, change message text, add logging call, change constant). "Substantive" is fixed by EXECUTION: each hunk is applied alone and a generated behaviour probe (program-made inputs, 3 identical runs) must differ for the substantive hunk and be identical for each trivial hunk; a hunk that fails this is dropped from the spec.
Messages: wording-pool messages built from the substantive hunk's (verb class, object) slots (Haiku wording pools, >= 50 wordings per form; no model sets a label). YES row: the diff with its own message. NO row: the same diff with a message taken from ANOTHER change spec of the same base-module group, chosen by a DERANGEMENT within the diff-size quintile of the group, with token Jaccard < 0.5 against the true message, >= 4 tokens, and its (verb class, object) different from the substantive hunk AND from every trivial hunk's description. A message that describes only a trivial hunk of the same diff is also a NO kind (CH-trivial, >= 25% of NO rows). Every diff appears once with its true message (YES) and once with a swapped message (NO): message marginals are identical across labels by construction.
MSG-REAL (L-R LR-11): CommitPackFT rows, keep ONLY mit, apache-2.0, bsd-2-clause, bsd-3-clause, cc0-1.0 checked per repo (copyleft and unknown rows dropped row by row); YES = the commit's own message; NO = another commit's message of the SAME repo chosen by derangement within the diff-size quintile, token Jaccard < 0.5, both messages >= 4 tokens [LR-B3]; both parts are dataset text, no model text. [Opus b1b T66-M2] CommitPackFT ships no test split, so (L-R rule 2) a seeded program freezes an internal 10% hold-out BY REPOSITORY before mapping; it is an internal held-out G13 target and is never trained; MSG-REAL rows come only from the other 90% of repos. Real names are exempt (Sk 8, P1-realism). Solver B for MSG-REAL = program re-deriving pair membership and the quintile / Jaccard / token constraints from the source record ids.
Solver A for MSG = spec construction; solver B = program that rebuilds the (verb class, object) of the message from the wording id's slot record and of the diff by AST-normalised hunk analysis, and re-runs the behaviour probe independently. 100% agreement.

## 3. Inputs, carriers, generator design

3.1 Input view: no user messages or tool calls (single view; recorded for the per-family view requirement). Carriers (section 9): CONFLICT_VIEW (BASE, OURS, THEIRS hunks, rendered by our own 3-way renderer; git is never invoked), RESOLUTION, SIDE_TEST_A, SIDE_TEST_B (TEST_FILE), API_PAIR (PROGRAM_PAIR), CALLER_SNIPPETS, DIFF, COMMIT_MESSAGE, BUMP_FIELD, QUESTION_FORM.
3.2 Languages: Python, JS/TS, Go, bash (bash modules kept to small text and counter pipelines). Per-head split follows section 4. Pins (Python 3.12.x, Node 24.x, Go 1.26.x with GOFLAGS=-mod=vendor GOPROXY=off GOTOOLCHAIN=local, bash) come from the L-0 image record and are appended to this file before the first non-Python row.
3.3 Application-style rule: no textbook algorithm tasks; domains as the T42c list; entity strings from the seeded namespace, TRAINING salt.
3.4 Splits: dev = 10% of GROUPS (a group = one base module with all its conflict / API / diff variants); never split across dev and train (K16).
3.5 Levers: A10, A12, A14, A15, A16 are NOT carried by L-P (build order assigns them elsewhere; GV7). Extension = an orchestrator ruling before the Thu 22 hash export. A1 / A2 hooks carried: template id, wording id and construction id (CF-*, RK*, SV-C*, CH-*) on every row.

## 4. Sizes and shares (rows before drops; quotas counted AFTER drops, every quota cell oversampled by 15% at generation)

| Head | Rows | Python | JS/TS | Go | bash | Labels |
|---|---|---|---|---|---|---|
| MERGE | 300 | 216 | 30 | 30 | 24 | YES 150 / NO 150 |
| SEMVER | 300 | 216 | 30 | 30 | 24 | BREAKING 150 / SAFE 150 |
| MSG | 200 | 144 | 20 | 20 | 16 | YES 100 / NO 100 |
| Total generated | 800 | 576 (72%) | 80 (10%) | 80 (10%) | 64 (8%) | |
| MSG-REAL | 800 | (real repos, mixed languages) | | | | YES 400 / NO 400 |
MERGE composition: NO kinds RK1 + RK2 <= 25% of NO, RK3 + RK4 (with a wrong-order or duplicate effect) >= 25% of NO, RK7 >= 40% of NO, RK8 <= 10% of NO; YES kinds include RK6 and rewritten RK5 so that >= 40% of YES rows keep < 100% of the side lines verbatim. CF-1..CF-7 each 8-20%.
SEMVER composition: SV-C1..SV-C12 each >= 3% and no kind > 20% of BREAKING rows; at least 5 BREAKING kinds look small (default change, edge input, exception class) and at least 5 SAFE kinds look large (internal refactor, overload, new optional parameter with a long body).
Matched pairs: MERGE >= 60% of rows in a pair (same conflict, different resolution kind, opposite labels); SEMVER >= 40% (same old API, a one-token change of the new API flips the label); MSG 100% (diff with true and with swapped message); family >= 30%.
Reuse: <= 4 rows per base module per head, <= 6 per module overall (counting T42c / T57 / T56g modules for cross-family duplicates, K13). Pilot (G3 first look) = seeded proportional 50% of each head (floor 300, cap 1,000; O-T66-5).

## 5. Difficulty ladder L1-L4 [CRIT D1, D2]

Mechanisms (source: the inventory's "conflict resolutions that compile but break one side", "breaking change hidden in a minor bump", "message describes a different same-repo diff"; program parameters only).
| Id | Mechanism | LOW | HIGH |
|---|---|---|---|
| M-SEMB | semantic break is subtle (MERGE RK7) | break visible in the first shown test | break visible only on one edge input of one shown test |
| M-ORDER | order of kept lines matters (MERGE RK3 / RK4) | order irrelevant or obviously wrong | order matters through a state dependency |
| M-FAR | cross-side dependency (MERGE) | same function | the dependency is two definitions away |
| M-LOOK | looks safe / looks breaking (SEMVER) | the diff looks like what it is | breaking change in a small diff; safe change in a large diff |
| M-BUMP | declared bump disagrees with the truth (SEMVER) | agrees | disagrees |
| M-MULTI | trivial hunks next to the substantive one (MSG) | 0 trivial hunks | 2 trivial hunks and the NO message describes one of them |
| M-OVL | lexical overlap inverted (MSG) | true message shares identifiers | true message shares none (describes the intent); the swapped message shares identifiers |
Row level: L1 none; L2 one LOW; L3 one HIGH or two LOW; L4 two or more HIGH. Composition (PRE-FREEZE): L1 20% / L2 30% / L3 30% / L4 20% (each +- 5 pp); L3-L4 >= 25% overall and per head. TWIN rule: every L3 / L4 row has an easy-looking twin of the opposite label differing by <= 1 token or <= 1 short line; twins cover >= 50% of L3-L4 rows (inside the matched-pair share). MEASURED BAR (K20, once, on the pilot): C2 (C1 if none), read on od-l4b, scores <= 70% on L4 rows. Model-based, so NOT a kill: a miss is folded into the ONE combined fix by raising HIGH settings (never by dropping rows by model score); afterwards a report line. MSG-REAL has no ladder (dataset text).

## 6. CHECK AT GENERATION [OWNER-ROW] (plan 16.1)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train." Every row is written ONLY through the L-0b stamp wrapper, per batch (<= 500 rows, same day):
(a) ANSWER CHECKS per row: manifest complete (K1: image id, runsc and kernel versions, runner, 3 run hashes, resolved-file or API hash); witness rule of its head (MERGE both suites 3 identical runs; SEMVER gold-sanity + 3 runs; MSG behaviour probe 3 runs, derangement / quintile / Jaccard constraints); strength and sanity (K2); solver A = solver B = spec expectation (K3); generator lint (K12); names guard (K15); token rule G6; PII scrub; exact-duplicate refusal and reuse ledger at creation; ladder level and A1 fields; for MSG-REAL: per-repo licence on the whitelist, LR-B3 constraints, source record ids.
(b) G13: the stamp service checks the row against every registered target with every listed method (registry sha bound; R6 scaffolding exemption; OHS-5 hash-export targets: exact and hashed n-gram methods only).
(c) The stamp is written into the row manifest. A failed row is dropped and logged (row id, target name, method). No unstamped or failed row enters the pool.
GV5: a G13-dropped row retires its spec; the whole conflict group / API pair / MSG pair is dropped with it; the replacement is a NEW spec with a new seed. Same-skeleton regeneration only for NON-G13 answer-check drops (A/B disagreement, expectation mismatch, strength failure, timeout, lint). For MSG-REAL a hit row is dropped and its source commit is never re-sampled into another pair.
FIX TRIGGER (all rows): > 1% of the pilot rows (or of any full-generation day) dropped for a reason other than exempt scaffolding or OHS-5 collisions (<= 5%) = the ONE combined fix. Answer-check drop rates use the bars of section 7. Code-idiom note: short idiomatic programs can match public code sets by accident; per-method drop counts are reported; if idiom-driven drops exceed 1%, the ONE fix may raise module distinctiveness, never relax a bar.
SET-LEVEL checks run ONCE per family on the pilot and once on the built family, never at the mix: A50 G6 at size, A49c balance, wording variety, matched-pair share, ladder and measured bar, section 7 probes, G5-H (two Haiku solvers on 300 rows plus one Haiku read of 100% of free-form wording), G3-H, Opus A43(d). Then C2 reads on od-l4b (trap selection, A1 audit): not a kill gate.

## 7. Gates

Probe protocol = G5 (groups: base module for generated heads; repo for MSG-REAL). PRE-FREEZE KILL = CPU or sandbox, data only; a miss after the one fix rolls the family. POST-TRAINING REPORT = needs the trained model, never a kill.

PRE-FREEZE KILL
| ID | Gate | Bar |
|---|---|---|
| T66-K1 | Witness compliance: complete manifest, 3 identical runs, versions and image id | 100% |
| T66-K2 | Gold-sanity and strength: MERGE A-tests fail on base and B-only, pass on A-only (B symmetric), both pass on RK5; SEMVER caller suite passes on the old API; BREAKING rows fail >= 1 caller on all 3 runs; SAFE rows pass all; MSG substantive hunk differs under the behaviour probe, trivial hunks do not | 100% of kept rows |
| T66-K3 | Solver A = solver B = spec expectation (per row at creation) | 100% of kept rows; block drop > 2% returns the block; per construction id an expectation mismatch rate > 10% returns that id to the builder |
| T66-K4 | Diff-length-only probe, per head (hunk / diff tokens and lines, files touched, candidate or message length, side lengths, ratios, language; no content tokens) | AUC <= 0.55, ub <= 0.60 each (MERGE, SEMVER, MSG, MSG-REAL) |
| T66-K5 | MERGE resolution-surface probe (kept-A fraction, kept-B fraction, marker residue, line count vs sides, A / B line order, duplicate count) and composition rules of section 4 | AUC <= 0.55, ub <= 0.60; composition as stated |
| T66-K6 | SEMVER surface probe (declared bump, changed / removed line counts, changed-parameter count, return-annotation change flag, new / removed symbol flags, change-kind id excluded) and bump-cue assert | AUC <= 0.55, ub <= 0.60; bump agreement with truth 50% +- 5 pp |
| T66-K7 | MSG probes: message-only; diff-only; joint length (message length x diff length, ratio); lexical-overlap probe on the hard stratum (>= 30% of MSG rows: true message overlap below the median and swapped-message overlap above it); derangement and quintile matching asserted | each AUC <= 0.55, ub <= 0.60; matching 100% |
| T66-K8 | MSG-REAL contract (LR-11 / LR-B3) [Opus b1b T66-M1, GV11: an L-R DATASET gate of LR-11, together with the MSG-REAL legs of K4 and K7; failing after the slice's ONE set-level correction (LR-B8) leaves MSG-REAL out, logged; it never rolls T66, and K9, K10, K11, K19 are read on the 800 generated rows only]; repo hold-out frozen before mapping and absent from output (T66-M2); per-repo licence whitelist (mit, apache-2.0, bsd-2-clause, bsd-3-clause, cc0-1.0); both messages >= 4 tokens; token Jaccard < 0.5; same repo; quintile match; K4 and K7 probes on the slice; copyleft / unknown rows dropped and counted | 100% / 100% / AUC <= 0.55, ub <= 0.60 |
| T66-K9 | Balance: YES (or BREAKING) 45-55% per head, per language; kind quotas of section 4 | as stated |
| T66-K10 | Matched-pair shares | MERGE >= 60%, SEMVER >= 40%, MSG 100%, family >= 30% |
| T66-K11 | Language quotas on the 800 generated rows | Python <= 75%; JS/TS, Go, bash each >= 8% |
| T66-K12 | Generator lint (clock, randomness, environment, network, filesystem outside /work, order-dependent printing, absolute paths) | 0 violations in kept rows |
| T66-K13 | Dedup: AST-normalised hash duplicate rate across T66 and against T42c / T57 / T56g modules; reuse ledger | <= 1%; <= 4 per module per head, <= 6 overall |
| T66-K14 | Token rule G6; >= 50 wordings per question form and for message wording pools, none > 2%; A50 G6, A49c, G5-H, G3-H, A43(d) per pipeline (G2) | per pipeline |
| T66-K15 | Names guard: generated rows on the closed allow-list with seeded entity strings; MSG-REAL exempt by family field (P1-realism) with the CPU test that others stay on the list | 0 refusals |
| T66-K16 | Split hygiene: no base module in both dev and train; OHS-5 collision drops | 100% / <= 5% of rows (above 5% IS the fix iteration) |
| T66-K17 | Check at creation (section 6): 100% of pooled rows carry a current clean stamp and an answer-check record | 100% / 0 unstamped; drops <= 1% outside exempt scaffolding and OHS-5 collisions, else the fix iteration |
| T66-K18 | A1 / A2 hooks: template id, wording id, construction id on 100% of rows | 100% |
| T66-K19 | Ladder composition and twin share (section 5) | L1 20 / L2 30 / L3 30 / L4 20 +- 5 pp; L3-L4 >= 25% overall and per head; twins >= 50% of L3-L4 |
| T66-K20 | Ladder measured bar: C2 (C1 if none) on the L4 rows of the pilot | accuracy <= 70% (FIX TRIGGER, never a kill; after the fix a report line) |
| T66-K21 | Scope asserts: no ALLOW / ASK / BLOCK option in any T66 form; generators never run generated code locally (execution only through the sandbox executor); git is never invoked | 0 violations (CPU) |

POST-TRAINING REPORT (never a kill)
| ID | Report line |
|---|---|
| T66-R1 | Accuracy per head with CI against base 4B and baselines: always-YES, majority, kept-fraction rule (MERGE), "bump says major" rule (SEMVER), lexical-overlap rule (MSG) |
| T66-R2 | Accuracy by resolution kind RK*, conflict kind CF*, change kind SV-C*, CH* and by language |
| T66-R3 | MSG-REAL separately and per-repo spread; the line says "train part seen; no official split; internal repo hold-out used" and reports accuracy on the held-out repos (LR RP3) [Opus b1b T66-M2] |
| T66-R4 | Accuracy by ladder level L1-L4 vs base 4B and trivial baselines |
| T66-R5 | Invariant-pair consistency (same prediction on both rows of a pair) and near-miss discrimination |
| T66-R6 | Order-invariance flip rate with CI; ECE and Brier per head |

## 8. Clean-room notes

- Built only from the plan, LANE_L-P, the stripped codeexec excerpt and the approved G0 files. No original generator, template, wording pool, mutate.py or OHS file was opened. No public merge-conflict, semantic-versioning, commit-message or code-review benchmark item text was seen; their names (when known) are G13 TARGETS only.
- Conflict views are rendered by our own 3-way renderer; the git binary (a copyleft tool) is never used. No SWE-smith modifier library is copied; operator classes are written from the lists in this file.
- MSG-REAL uses dataset text only for rows from whitelisted permissive repos; issue text, pull-request text and review comments are not used (A82 4 strict reading as T57).
- Every entity string in generated rows is from the seeded namespace, TRAINING salt. Writers (Haiku wording pools) get the question forms and slots, never the literal-ban list. G13 hit reports carry row ids, target name and method only.
- Execution only in the signed-off od-sbx1 sandbox; never on od-cpu1 or any data host.

## 9. NAMES this family needs (names only; for manifest v1.2 due Fri 23 12:00; family id T66 is already on row_job_families_allowed)

- Languages: python, javascript, typescript (conditional on the Node type-stripping self-test; otherwise folded into JS and the JS/TS share stays >= 8%), go, bash. Runners (existing ids): runner.pytest, runner.node_test, runner.go_test, runner.bash_posix_test, runner.python_isolated. No new runner id; the 3-run driver and the solver-B driver are harness names listed in the L-0 image record.
- Definition cards: defs_card.t66.merge, defs_card.t66.semver, defs_card.t66.message.
- Carriers: CONFLICT_VIEW, RESOLUTION, SIDE_TEST_A, SIDE_TEST_B (TEST_FILE form), API_PAIR (PROGRAM_PAIR form), CALLER_SNIPPETS, COMMIT_MESSAGE, BUMP_FIELD; reused: DIFF, TEST_FILE, SRC_FILE, QUESTION_FORM.
- Registry ids (hash export, not guard-checked): T66-Q-MERGE, T66-Q-SEMVER, T66-Q-MSG (>= 50 wording ids each, plus message wording pools); CF-1..CF-7; RK1..RK8; SV-C1..SV-C12; CH-1..CH-10; CH-trivial; M-SEMB, M-ORDER, M-FAR, M-LOOK, M-BUMP, M-MULTI, M-OVL; levels L1-L4.
- Fixed real names (category fixed_real_licence_ids, proposed in T63 section 9): mit, apache-2.0, bsd-2-clause, bsd-3-clause, cc0-1.0 (the CommitPackFT whitelist spellings, as the dataset writes them; UNVERIFIED).
- Namespace slot kinds used (all existing): ns.noun.module, ns.noun.symbol, ns.noun.entity, ns.noun.field, ns.variable, ns.path_stem, ns.handle, ns.repo. No new kind.
- MSG-REAL vocabulary (real repo, tool and entity names): extracted BY PROGRAM after the LR-11 S-pre PASS (plan 16.3 rule 4), not listed by hand.
- G13 targets to register before any row (names only): public commit-message-generation and merge-conflict-resolution sets found by the L-0b registry scout (candidate names from memory, existence and licence UNVERIFIED: CommitBench, CommitChronicle, MCMD); CodeReviewer and CodeReviewQA are already out of every tier and stay G13 targets; the standing list.
- R5 candidate list (names only): CommitPackFT (already LR-11).

## 10. Risks

1. MERGE tests are written by the generator and shown; a candidate could pass both suites while being wrong in a way no test sees. The label is defined as "both shown suites pass" and the question says so; the report does not claim merge correctness beyond the shown tests.
2. SEMVER label depends on the shown callers, not the real world; the question and defs_card say so.
3. Lexical-overlap shortcut in MSG: positives share identifiers with the diff. Mitigation: the hard stratum (>= 30%) inverts overlap; K7 probes it; R1 reports the overlap baseline.
4. Derangement matching can leave short-diff groups too small; groups with < 6 members are merged by the generator before the pilot (parameter, fixed now).
5. Bash and Go app-style modules are less natural; kept small. Node type stripping is UNVERIFIED (fallback in section 9).
6. Sandbox cost: 3 runs x 2 suites per MERGE row, 3 runs per SEMVER row, behaviour probes for MSG. Throughput is a number L-0 owes by Wed 21; rows start Sun 25 after the sandbox sign-off.
7. CommitPackFT: card says "permissive" while the field lists agpl-3.0, lgpl-2.1 and unknown; only the whitelist is kept, checked per repo. Short or generic messages are removed by the >= 4 tokens rule; true-but-generic pairs ("update file") are filtered by Jaccard and quintile rules but a residual noise rate exists; the A46 drop-only screen (LR R14) applies to this human-label slice.
8. Model-based fix triggers (K20) are not kills; a CPU-only family could still look easy to C2 (not a failure).

## 11. One fix iteration and kill rule

- G3 governs. Allowed fix levers: generator parameters, quotas, kind mix, group sizes, wording pools, AFLite-style repair (filtered <= 30% of the family, reported), raising ladder HIGH settings; NOT the bars. Defects found before the pilot by unit tests, the build skeptic or A/B disagreement on CPU fixtures are build fixes.
- Kill (standard P1 rule): any PRE-FREEZE gate failing after the fix, or not through all of them by the data freeze (Mon 2 Nov 23:59 UTC; stretch Fri 30 Oct) -> T66 rolls to C2.2 / C3 with the failing gate and numbers logged. G4: no head rolls alone inside T66 (a MSG-only failure rolls T66). MSG-REAL failing its dataset-level L-R rules (K8 and the MSG-REAL legs of K4 / K7) is left out as a dataset (logged) and does not roll T66; if T66 is killed, MSG-REAL goes with it (GV11) [Opus b1b T66-M1]. POST-TRAINING lines are never kill rules. First in the usage shed order after the research pass.
- Timeline: approval Mon 19; builder under the measured burn projection (Sk 21); MSG (generated) and MSG-REAL need no sandbox beyond the behaviour probe; MERGE / SEMVER rows after the sandbox sign-off (Wed 21) and the Sat 24 18:00 stamp-service rules; rows from Sun 25.

## 12. Open questions for Opus

- O-T66-1 Witness runs: 3 identical runs for MERGE, SEMVER and the MSG behaviour probe (the T42c ruling (a) pattern, the plan's will-this-test-fail rule). Confirm (sandbox default is 2).
- O-T66-2 MSG-REAL counted in T66, outside the 800 generated, shed with the P1 realism slices (as MBPP under LR-M7). Confirm.
- O-T66-3 Definition of "describes": message matches the single substantive hunk; a message that describes only a trivial hunk is NO. Confirm (this is a policy definition, written in defs_card.t66.message).
- O-T66-4 SEMVER truth is relative to the SHOWN callers. Confirm.
- O-T66-5 Pilot size for families under 1,000 rows: 50%, floor 300, cap 1,000.
- O-T66-6 TypeScript in the generated rows depends on the Node type-stripping self-test; fallback folds TS into JS.

## 13. Conformance seed (plan 16.1 step 0)

| Clause | Obligation | CPU test id |
|---|---|---|
| G1 | solver B imports stdlib + row schema only; no model client | T66-CM-01 |
| G3 | parameter file sha frozen at pilot launch; later change needs the fix-iteration flag | T66-CM-02 |
| G5 | probe calls: grouped split, 97.5th-percentile bound, permutation and leak checks | T66-CM-03 |
| G6 / GV4 | row > 1,536 tokens refused at creation | T66-CM-04 |
| GV5 | G13 drop retires the spec and the whole conflict group / API pair / MSG pair | T66-CM-05 |
| 2.1 | MERGE witness: both suites, 3 identical runs, strength rules, expectation per kind | T66-CM-06 |
| 2.2 | SEMVER witness, gold-sanity, bump-cue assert | T66-CM-07 |
| 2.3 | MSG construction: derangement, quintile, Jaccard, >= 4 tokens, behaviour probe | T66-CM-08 |
| 2.3 / K8 | MSG-REAL per-repo licence whitelist and LR-B3 constraints | T66-CM-09 |
| K21 | no permission option; no local execution of generated code; no git | T66-CM-10 |
| 6 | pool writer refuses any row without a current clean stamp and an answer-check record | T66-CM-11 |
| 3.5 | A10 / A12 / A14 / A15 / A16 not carried; A1 / A2 hook fields present | T66-CM-12 |

## Opus batch-1b rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; families/G0_APPROVALS_v32.md "Batch 1b")

VERDICT: REVISE -> APPROVED after the 2 fixes below (applied in this file, marked "[Opus b1b ...]"). Generator, solver,
renderer and probe CODE may start now; MERGE / SEMVER / MSG execution rows only after the od-sbx1 sign-off; every row only
after the OHS-5 freeze, the registry sha, manifest v1.2, a signed stamp service and a signed conformance record (Sat 24
18:00 rules unchanged).

Must-fix (applied):
- T66-M1 (GV11) K8 and the MSG-REAL legs of K4 / K7 are LR-11 dataset gates (leave-out), not T66 kills, and the family
  gates are read on the generated rows. Reason: the gate table listed K8 as a PRE-FREEZE KILL while section 11 said the
  slice is left out alone; the builder would read two rules.
- T66-M2 CommitPackFT has no split: L-R rule 2 (seeded 10% repo hold-out before mapping, never trained) now binds the
  slice, and R3 reports "train part seen" with the hold-out line. Reason: plan 16.3 rules 2 and 6 bind every L-R dataset;
  "does not apply" left the slice with no held-out reading.

Binding conditions:
- T66-B1 O-T66-1 confirmed: 3 identical runs for MERGE, SEMVER and the MSG behaviour probe (T42c ruling (a) pattern).
- T66-B2 O-T66-2 confirmed: MSG-REAL counted in T66, outside the 800 generated, shed with the P1 realism slices (step 6).
- T66-B3 O-T66-3 confirmed ("describes" = the single substantive hunk; a trivial-hunk message is NO; defs_card says so).
- T66-B4 O-T66-4 confirmed (SEMVER truth relative to the SHOWN callers; question and defs_card say so).
- T66-B5 O-T66-5 -> GV10: pilot = 50% of the 800 generated rows = 400, proportional by head; MSG-REAL has no pilot (set-level
  checks once per built dataset slice, L-R rule 6).
- T66-B6 O-T66-6 confirmed (TypeScript only after the Node type-stripping self-test; fallback folds TS into JS).
- T66-B7 MSG-REAL PAIR ACCOUNTING: each kept commit contributes its diff to exactly one YES and one NO row and its message
  to exactly one YES and one NO row (derangement over commits of the same repo and diff-size quintile, LR-B3 constraints),
  so message-only and diff-only probes are at chance by construction, as in the generated MSG block.
- T66-B8 git is never invoked (stricter than the T42c-B3 offline-tool rule); our own 3-way renderer only.
- T66-B9 Toolchain pins and image digests from the L-0 image record are appended to this file before the first non-Python
  row (as the round-1 T42c note).
