# G0-LITE T62 FLAKY-OR-REAL (L-R-fed slices only: LogChunks 700 + FlakeFlagger 200) (lane L-P wave C; P1; clean-room; draft for Opus approval, due Fri 23 Oct 2026, written early)

Author: Sonnet 5.5 high (L-P G0-lite writer), Sun 18 Oct 2026. Design only: no rows, no mapper code, no download, no execution, no model call, no Modal.
Status: DRAFT 1. Every number below is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus.
Scope (plan 16.9): "only the slice fed by LogChunks 700 + FlakeFlagger 200; needed before those L-R rows map (by Fri 23)". The generated half of the v2 T62 idea ("same error text, different rerun history") is NOT designed here (section 12, O-T62-5).
Read for this file: PLAN_TRAINING_SIDE.md (sections 1 C and E, 2, 5, 8, 16.1, 16.3, 16.4, 16.9), LANE_L-P.md, families/LR/G0_LITE.md (rows LR-05, LR-06, rules R5-R16, LR-B2, LR-B8, LR-B10), families/T42c addendum and T50 G0-lite (format), families/G0_APPROVALS_v32.md (GV1-GV9), C2_1_PUBLIC_TRAIN_INVENTORY.md (A15, C9, section 4 T62 row), l0/NAMES_MANIFEST_V1_1.json (structure only). NOT opened: any path containing "ohs" or "sealed", C2_1_PLAN_v3.md, any plan SKEPTIC file, OHS5_BRIEF_DRAFT.md, any dataset file or log, any generator, wording pool, benchmark item text, ~/.claude. Dataset field names that appear below come from memory and are marked UNVERIFIED; the L-R S-pre / record step confirms them.
Shared rulings carried (index): G1 solver B is CODE; G2 data-audit gates are PRE-FREEZE; G3 no free pilot tuning, ONE combined fix; G4 no head or sub-block rolls alone (the dataset-level L-R rules decide each slice: section 11); G5 one probe harness; G6 tokens; G7 secondary heads (none); G9 not applicable (T62 labels facts, not permissions); G10 not applicable (no natural-language user utterance); GV1-GV4 (A10 / A14 not carried; GV4 binds); GV5 (a G13 hit row is dropped and its source record is never re-sampled); GV6, GV7 (not applicable); GV8; GV9.

## 0. One-paragraph summary

T62 is a P1 REALISM family: it contains only rows that L-R maps from two public train-split datasets, so every gold label is the dataset's own human or execution label through an Opus-approved recast table. (CHUNK) from LogChunks: the 4B sees a CI build log cut into lettered segments and picks the segment that explains the failure (a real failure that can look like noise sits among distractors that look like failure boilerplate). (CAT) failure category, only if the dataset carries a human category field. (FLAKY) from FlakeFlagger labels and metrics only: is this test flaky, from static test metrics (and, if the package ships per-run outcomes, a short rerun sample). Nothing is generated, so there is no solver A generator and no ladder parameter; the family's gates are slice-level set checks, the span probe, and the L-R dataset rules.

## 1. Decision and label set

| Head | Question form id | Rows (cap) | Labels | Gold |
|---|---|---|---|---|
| CHUNK | T62-Q-CHUNK | up to 700 (560 if CAT is built) | pick-one of k lettered segments, k = 4 (70%) or 6 (30%) | LogChunks human-labelled failure chunk (validated with developers, per the dataset page; UNVERIFIED wording) |
| CAT (conditional) | T62-Q-CAT | up to 140 (taken out of the 700) | pick-one of k = 4 failure categories | LogChunks human category field IF the S-pre record shows one (UNVERIFIED that it exists); else not built |
| FLAKY | T62-Q-FLAKY | up to 200 | YES (flaky) / NO | FlakeFlagger test-level label from 10,000 reruns per project (execution; program) |
Total cap 900. A dataset smaller than its cap enters whole (L-R rule 5). [Opus b1b T62-M1] There is NO row-count floor: the former "fewer than 300 usable rows = left out" rule is deleted (FLAKY's cap is 200, so it would always have been left out, and L-R rule 5 says a smaller dataset enters whole); a small slice is guarded by its gates, whose 97.5th-percentile bounds widen with fewer groups, and a slice that cannot meet them is left out by the gate (logged with numbers). All three heads are FACT questions; no ALLOW / ASK / BLOCK option appears (K13). Binary heads shuffle option order; 20% order-invariance copies are mix-level, not counted.

## 2. Gold method; solver A and independent solver B

Gold is never produced by a model. The L-R mapper applies a per-dataset recast table (hashed, Opus-approved before any row): LogChunks (source record) -> segmented log with the labelled chunk as one segment; FlakeFlagger (source record) -> flaky yes / no from the dataset's own test-level label. Solver A = the mapper's output for the record. Solver B = a PROGRAM written by a separate Sonnet high session from THIS file, the recast table and the row schema only: it re-reads the SOURCE record with its own parser, re-derives the label (CHUNK: which segment contains the labelled chunk by exact line-range or exact substring match; FLAKY: the label field) and re-checks every row construction rule (segment count, distractor kinds, length matching, hold-out exclusion, sample construction). Agreement on 100% of kept rows; disagreements dropped and counted; a block with > 2% dropped for disagreement returns to the mapper. No LLM reads rows to produce or check a label (G1). The A46-style drop-only noise screen (LR R14) applies to the human-label CHUNK and CAT rows (C2 reads on od-l4b, drop where p_g < 0.2; loss > 15% goes to Opus; it never writes or changes a label); FLAKY is exempt (exact program label).

## 3. Inputs, carriers, row construction

3.1 Input view: no user messages or tool calls (single view; recorded for the per-family view requirement). Carriers (section 9): LOG_SEGMENTS (lettered segments as the options), TEST_METRICS_RECORD, RERUN_SAMPLE, QUESTION_FORM, OPTIONS.
3.2 Splits: only the TRAIN side is used. LogChunks and FlakeFlagger ship no train / test split, so a seeded program freezes an internal 10% hold-out BEFORE mapping: by repository for LogChunks (80 repos, so 8 held out), by project for FlakeFlagger (24 projects; [Opus b1b, O-T62-6] the 10% is rounded UP and the hold-out has at least 3 groups, so 3 projects are held out, reported). The hold-out is an internal held-out target, never trained (L-R rule 2). Dev = 10% of the remaining groups (repos / projects), inside the cap.
3.3 CHUNK construction (program): split the log into lines; the gold segment is the labelled chunk's exact span (located by dataset offsets if shipped, else by exact substring match; the locate rate is a gate, K4). Distractor segments are other spans of the SAME log (LR-B10), non-overlapping with the gold span and with each other; at least one distractor is drawn from the log's tail region (where the generic build-failed boilerplate sits) and at least one from the head region; distractor lengths are sampled from the gold-length distribution so length is not a cue; the gold letter is uniform over positions (+- 3 pp). A segment longer than the row budget is NOT cut: the row is dropped (length drop logged, never a cut that drops evidence). No keyword field of the dataset (the developers' search keywords, UNVERIFIED) is shown or used as a feature.
3.4 CAT construction: the gold category plus k - 1 program-chosen nearest categories (train-set confusion), k = 4; the log is shown as one block or as the gold segment, chosen once per dataset before the pilot (design value: the gold segment plus two distractor segments).
3.5 FLAKY construction: FLAKY-A (all rows): a TEST_METRICS_RECORD with the dataset's test-level metrics and test identifier tokens (class and method names; NO Java source lines, because the 24 project licences are unchecked: K1). FLAKY-B (100 of the 200, only if the data package ships per-run outcomes; UNVERIFIED): FLAKY-A plus a RERUN_SAMPLE of k = 5 or 10 outcomes drawn by a seeded program from the test's real per-run outcomes, independent of the label. A mixed sample is decisive for YES; an all-pass sample is NOT decisive (a non-flaky test, or a flaky test with a rare failure). If per-run outcomes are not shipped, all 200 rows are FLAKY-A. Balance is by project: every project contributes equal YES and NO within +- 10 pp; no project above 15% of the FLAKY rows. Real project, test and class names are used (P1-realism exemption, Sk 8).
3.6 Levers: A10, A12, A14, A15, A16 are NOT carried by L-P; GV7. A1 / A2 hooks: mapper rule id, wording id and segment-kind ids on every row.

## 4. Sizes and shares

| Block | Rows | Notes |
|---|---|---|
| CHUNK k = 4 | up to 490 (392 if CAT is built) | gold letter 25% +- 3 pp |
| CHUNK k = 6 | up to 210 (168 if CAT is built) | gold letter 1/6 +- 3 pp |
| CAT | up to 140 | only if the field exists; at most 2 rows per log across CHUNK and CAT |
| FLAKY-A | 100 (200 if FLAKY-B is not shippable) | YES 50% +- 3 pp |
| FLAKY-B | 100 | YES 50% +- 3 pp; decisive share among YES 20-60% |
Reuse: at most 2 rows per log; at most 1 FLAKY row per test. Pilot: not applicable (rows come from the L-R mapper; set-level checks run ONCE per built dataset slice per LR rule 6; the fix iteration is per slice).

## 5. Difficulty strata (no ladder gate)

CRIT D1 names two mechanisms for this family: a REAL failure that looks like noise, and a FLAKY failure that looks deterministic. No program parameter can set them on dataset rows. They are therefore REPORTED STRATA assigned by program from stated features: CHUNK-S1 gold segment contains none of a closed list of failure keywords (looks like noise); CHUNK-S2 gold segment is not in the tail region; CHUNK-S3 a tail distractor contains failure boilerplate; FLAKY-S1 (FLAKY-B) YES row with an all-pass sample; FLAKY-S2 NO row with the metric profile of the YES rows (nearest-neighbour profile, program-computed). Strata are reported (T62-R2); there is no composition bar and no C2 <= 70% fix trigger for T62 (recorded, O-T62-4).

## 6. CHECK AT GENERATION [OWNER-ROW] (plan 16.1; applies to every mapper)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train." Every row is written ONLY through the L-0b stamp wrapper, per batch (<= 500 rows, same day):
(a) ANSWER CHECKS per row: train side only and hold-out id absent; licence record present (CC BY 4.0 quote + attribution flag); label = the dataset's own label through the hashed recast table; solver A = solver B; construction rules of section 3 (segment kinds, length matching, non-overlap, gold letter, sample independence); FLAKY: no source line; names handling (P1-realism family field); token rule G6 (> 1,536 refused); PII scrub (logs can contain e-mail addresses, tokens and host names: a program scrub with a hit list is applied and reported; a log whose scrub changes the gold segment's meaning is dropped); exact-duplicate refusal and the reuse ledger; A1 fields.
(b) G13: the stamp service checks the row against every registered target with every listed method (registry sha bound; R6 scaffolding exemption; OHS-5 hash-export targets: exact and hashed n-gram methods only).
(c) The stamp is written to the row manifest. A failed row is dropped and logged (row id, target name, method). No unstamped or failed row enters the pool.
GV5: a G13-hit row is dropped and its source log or test is NEVER re-sampled into another rendering; > 1% stamp drops outside exemptions in a slice goes to Opus; > 5% leaves the dataset out (L-R Sk 23a). Set-level checks ONCE per built slice: A50 G6 at size, A49c balance, wording variety (>= 50 per form, none > 2%), the section 7 probes, duplicates, G5-H (two Haiku solvers on 300 rows plus one Haiku read of 100% of free-form wording; for this family the 300-row read is the whole CAT / FLAKY slice or a sample of CHUNK), G3-H, Opus A43(d). Then C2 reads on od-l4b: not a kill gate.

## 7. Gates

Probe protocol = G5 (groups: repository for CHUNK / CAT, project for FLAKY). PRE-FREEZE KILL = CPU or data-only, a miss after the slice's one fix rolls the SLICE (dataset left out, section 11). POST-TRAINING REPORT = needs the trained model, never a kill.

PRE-FREEZE KILL
| ID | Gate | Bar |
|---|---|---|
| T62-K1 | Provenance and licence: record per dataset with licence quote, URL, fetch date (CC BY 4.0 for both; attribution flag in the report); label provenance enum human (LogChunks) or program (FlakeFlagger); FLAKY rows contain NO source-code line (statement-like line scan) | 100% / 0 lines |
| T62-K2 | Hold-out frozen before mapping; no hold-out id in the output (CPU test) | 100% |
| T62-K3 | Solver A = solver B on kept rows (per row at creation) | 100%; block drop > 2% returns the block |
| T62-K4 | CHUNK locate rate: the labelled chunk is located exactly in its log | >= 98% of candidate logs; otherwise Opus (the locate failures are dropped, counted) |
| T62-K5 | CHUNK span probe (Sk 25): option index, line count, token count, distance from the log end (fraction), digit fraction, timestamp-line fraction; no content tokens; balanced accuracy per k | <= 1/k + 3 pp and ub <= 1/k + 6 pp (k = 4: 28% / 31%; k = 6: 19.7% / 22.7%); a failing dataset re-samples span order and lengths ONCE (its one fix), else left out; GV8: pooled across k on the first read, per k binds on the built slice |
| T62-K6 | CHUNK distractor design asserts: every row has a tail and a head distractor; distractor length medians within 10% of gold's, 10th and 90th percentiles within 25%; gold letter uniform +- 3 pp | 100% / as stated |
| T62-K7 | CAT probes (if built): category-prior-only and option-order balanced accuracy | <= 1/4 + 3 pp, ub <= 1/4 + 6 pp |
| T62-K8 | FLAKY balance and shortcuts: YES 50% +- 3 pp overall and +- 10 pp per project; no project > 15%; project-id-only probe; format-only probe (record layout, field order, field count, row length, wording id; no metric values) | AUC <= 0.55, ub <= 0.60 for both probes |
| T62-K9 | FLAKY-B sample: drawn independent of the label (permutation test of sample vs label given the real outcomes); decisive share among YES rows | 20-60%; sample k balanced 5 / 10 within 5 pp across labels |
| T62-K10 | Duplicates: log hash duplicates and test-id duplicates | <= 1% |
| T62-K11 | A46-style screen on CHUNK / CAT (drop-only); loss | <= 15% (above: Opus; without OK the dataset is LEFT OUT) |
| T62-K12 | Token rule G6 (mean <= 800, none > 1,536, > 1,024 on <= 10%); >= 50 wordings per question form, none > 2%; A50 G6, A49c, G5-H, G3-H, A43(d) per pipeline (G2) | per pipeline |
| T62-K13 | Scope asserts: no ALLOW / ASK / BLOCK option; names: P1-realism family field with the CPU test that other families stay on the closed list; vocabulary extraction BY PROGRAM recorded | 0 violations |
| T62-K14 | Check at creation (section 6): 100% of pooled rows carry a current clean stamp and an answer-check record; stamp drops outside exemptions | 100%; <= 1% (> 1% to Opus, > 5% left out) |
| T62-K15 | A1 hooks: mapper rule id, wording id, segment-kind ids on 100% of rows | 100% |

POST-TRAINING REPORT (never a kill)
| ID | Report line |
|---|---|
| T62-R1 | Accuracy per head with CI against base 4B and baselines: CHUNK last-segment rule, keyword-count rule, option-position prior; CAT category prior; FLAKY always-NO and project prior |
| T62-R2 | Accuracy by stratum (section 5) |
| T62-R3 | Accuracy on the internal hold-outs (held-out repos / projects), C2 vs C2.1 (LR report line RP3) |
| T62-R4 | FLAKY-B accuracy by sample decisiveness; ECE and Brier per head (the irreducible-noise rows make calibration the main read) |
| T62-R5 | Order-invariance flip rate with CI |
Every report row says "no official split; internal hold-out used".

## 8. Clean-room notes

- Built only from the plan, LANE_L-P and the approved G0 files. No dataset file, log, test name or metric was opened. LogChunks and FlakeFlagger are L-R train-side sources; their hold-outs and any public CI-log failure or flaky-test sets found by the registry scout are G13 TARGETS.
- No Java source text from the 24 FlakeFlagger projects enters a row; only identifiers and metrics. CI log text is used under the dataset's CC BY 4.0 record; logs are scrubbed by program for e-mail addresses, token-like strings and host names (reported).
- The dataset's keyword fields (if any) are not features and are not shown. Writers (Haiku wording pools) get the question forms and slots, never the literal-ban list. G13 hit reports carry row ids, target name and method only.

## 9. NAMES this family needs (names only; for manifest v1.2, due Fri 23 12:00; family id T62 must be ADDED to row_job_families_allowed in v1.2)

- Languages / runners: none (no execution). Programs: none.
- Definition cards: defs_card.t62.chunk, defs_card.t62.category, defs_card.t62.flaky.
- Carriers: LOG_SEGMENTS, TEST_METRICS_RECORD, RERUN_SAMPLE; reused: OPTIONS, QUESTION_FORM.
- Registry ids (hash export): T62-Q-CHUNK, T62-Q-CAT, T62-Q-FLAKY (>= 50 wording ids each); segment kinds SEG-GOLD, SEG-D-HEAD, SEG-D-TAIL, SEG-D-MID; strata ids T62-S1..T62-S5; recast table ids T62-RT-CHUNK, T62-RT-CAT, T62-RT-FLAKY.
- Real vocabulary (repository, project, test, class, tool and CI-service names): extracted BY PROGRAM after the L-R S-pre PASS (plan 16.3 rule 4), not listed by hand.
- Namespace slot kinds: none used (all real).
- G13 targets to register before any row (names only): the LogChunks and FlakeFlagger internal hold-outs; public CI-log failure-explanation sets and public flaky-test datasets found by the L-0b registry scout (candidate names from memory, existence and licence UNVERIFIED: iDFlakies, IDoFT); the standing list.
- R5 candidate list (names only): LogChunks, FlakeFlagger (already LR-05, LR-06).

## 10. Risks

1. Dataset fields are UNVERIFIED (offsets of the labelled chunk, per-run outcomes, categories); S-pre decides which heads exist. The family shrinks, it does not break.
2. CHUNK tail / head shortcuts: a gold chunk usually sits near the log end; the distractor rules and K5 target this; a residual position cue is measured and the single re-sample is the fix.
3. FLAKY from static metrics is a noisy task (published flaky-test predictors are far from perfect); the rows teach calibration more than accuracy. The family is small (200) and reports ECE.
4. Project-level base rates: balanced per project; with 24 projects and a 2-project hold-out the hold-out reading is weak (reported as such).
5. Logs can hold personal or secret-like text: program scrub plus the G13 stamp; a scrub that damages the gold segment drops the row.
6. LogChunks is a Travis-CI-era corpus; the domain is narrower than 2026 CI (reported, not fixed).

## 11. One fix iteration and kill rule

- G3 / L-R rule 6 govern: each built slice gets ONE combined fix (for CHUNK the span re-sample of K5; for FLAKY the balance or sampling parameters); NOT the bars.
- Kill (standard P1 rule, applied per dataset slice because T62 holds no generated rows; O-T62-2): a slice that fails any PRE-FREEZE gate after its fix, or is not through by the data freeze (Mon 2 Nov 23:59 UTC; stretch Fri 30 Oct), is LEFT OUT as a dataset (logged with numbers). T62 as a family is out only if every slice is out. POST-TRAINING lines are never kill rules. First in the usage shed order after the research pass (P1 realism slices shed with their families).
- Timeline: approval by Fri 23 (needed before the LR-05 / LR-06 mappers run); rows only after the OHS-5 freeze, the registry sha, manifest v1.2, a signed stamp service and a signed conformance record (Sat 24 18:00 rules unchanged).

## 12. Open questions for Opus

- O-T62-1 CAT is conditional on a human category field in LogChunks; confirm "not built if absent", and that CAT rows come out of the 700 (at most 2 rows per log).
- O-T62-2 T62 consists only of L-R slices. Confirm the per-dataset leave-out reading (a slice left out does not roll the other) against G4, and the 300-row floor per slice.
- O-T62-3 FLAKY-B depends on per-run outcomes in the FlakeFlagger package (UNVERIFIED). Confirm the fallback: all 200 rows FLAKY-A.
- O-T62-4 No difficulty ladder and no C2 <= 70% fix trigger for dataset-gold slices; strata are report lines. Confirm.
- O-T62-5 The v2 generated component ("same error text, different rerun history") is not designed; a separate addendum with its own gold and size would be needed, outside the Fri 23 deadline. Default: none in C2.1.
- O-T62-6 Hold-out of 2 FlakeFlagger projects is small; accept, or hold out 3 (12.5%)?

## 13. Conformance seed (plan 16.1 step 0)

| Clause | Obligation | CPU test id |
|---|---|---|
| G1 | solver B imports stdlib + row schema only; no model client | T62-CM-01 |
| G3 | mapper parameter file sha frozen at first read; later change needs the fix-iteration flag | T62-CM-02 |
| G5 | probe calls: grouped split, 97.5th-percentile bound, permutation and leak checks | T62-CM-03 |
| G6 / GV4 | row > 1,536 tokens refused at creation | T62-CM-04 |
| GV5 | a G13-hit row is dropped; its source is never re-sampled | T62-CM-05 |
| 2 | label = dataset label through the hashed recast table; no model label | T62-CM-06 |
| 3.2 | hold-out frozen before mapping; no hold-out id in output | T62-CM-07 |
| 3.3 | segment construction, non-overlap, tail / head distractors, no cut that drops evidence | T62-CM-08 |
| 3.5 | no source line in FLAKY rows; sample independent of label | T62-CM-09 |
| K13 | no permission option; P1-realism names exemption scoped by the family field | T62-CM-10 |
| 6 | pool writer refuses any row without a current clean stamp and an answer-check record | T62-CM-11 |
| 3.6 | A10 / A12 / A14 / A15 / A16 not carried; A1 hook fields present | T62-CM-12 |

## Opus batch-1b rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; families/G0_APPROVALS_v32.md "Batch 1b")

VERDICT: REVISE -> APPROVED after the 1 fix below (applied in this file, marked "[Opus b1b ...]"). Recast-table drafts,
mapper, solver B and probe CODE may start only after each source's S-pre 8.5 PASS (plan 16.3 rule 1, Sk 5); the recast
tables go to Opus in the code-realism source-group batch; rows only after the OHS-5 freeze, the registry sha, manifest
v1.2, a signed stamp service and a signed conformance record (Sat 24 18:00 rules unchanged). T62 is added to
row_job_families_allowed in manifest v1.2.

Must-fix (applied):
- T62-M1 the 300-row per-slice floor is deleted (section 1). Reason: it would leave FLAKY out by construction (cap 200),
  contradicts L-R rule 5 and the owner's "all data" rule, and the G5 bounds already guard small slices.

Binding conditions:
- T62-B1 O-T62-1 confirmed: CAT is built only if the S-pre record shows a human category field; CAT rows come out of the
  700; at most 2 rows per log.
- T62-B2 O-T62-2 -> GV11: each slice is an L-R dataset (left out by its own gates, one correction each); T62 is out only
  if every slice is out.
- T62-B3 O-T62-3 confirmed: without shipped per-run outcomes all 200 FLAKY rows are FLAKY-A; a RERUN_SAMPLE is never
  simulated.
- T62-B4 O-T62-4 confirmed: dataset-gold slices have no ladder and no C2 <= 70% fix trigger (same reading as T63 MAL,
  T66 MSG-REAL, T65 Juliet); the strata are report lines.
- T62-B5 O-T62-5: no generated T62 component in C2.1 (plan 16.9 scope).
- T62-B6 O-T62-6: 3 FlakeFlagger projects held out (section 3.2 as amended); LogChunks 8 repos.
- T62-B7 PII SCRUB RULE (program, replaces "changes the gold segment's meaning"): a log is dropped if any scrub hit falls
  inside the gold segment or inside any span the row shows as an option; scrub hits elsewhere are replaced by a fixed
  placeholder and counted.
- T62-B8 FLAKY rows show identifiers (class and method names) and metrics only; no source line (K1), no repository URL.
