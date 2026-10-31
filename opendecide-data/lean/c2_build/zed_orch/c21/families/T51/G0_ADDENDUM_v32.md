# G0 ADDENDUM v3.2 T51 SCOPE-BOUNDARY (lane L-A; draft for Opus batch 1, target Mon 19 Oct 2026)

Author: Sonnet 5.5 high, Sun 18 Oct 2026 (UTC). Read scope used: C2_1_BUILD_ORDER.md (L-A and v3.2 blocks), C2_1_PLAN_v3.md sections 1, 2, 5, 6, 7, 8, the PRE-REGISTERED RULES block of section 3 and section 16, C2_1_EXTRA_LEVERS.md (ADOPT NOW), C2_1_PUBLIC_TRAIN_INVENTORY.md (section 4 ladder row for T51), PREREG_FINAL.md blocks A77, A79, A82, families/T51/G0_LITE.md (approved, rounds 1 and 2) and families/T50/G0_ADDENDUM_v32.md (same author, same day; the shared core is defined there). No rows, no generator code, nothing executed, no model or API call. Never opened: any "ohs" or "sealed" path, OHS5_BRIEF_DRAFT.md, C2 build files, T27/T40-T46 generators, or any benchmark item text (AmPermBench and UnderSpecBench item text, entity names and ID formats stay unseen; only the plan's published ideas are used).
Status: DRAFT for the Opus batch-1 approval (Mon 19 Oct). Every number is a design value fixed BEFORE any pilot; changing one after a pilot is a gate edit and needs Opus.
How this file binds: families/T51/G0_LITE.md (v3.1, APPROVED round 2, with its section 12 rulings) stays in force. This addendum binds ONLY where it says "REPLACES" or "ADDS". Unchanged: the label set, the S x B x R matrix, the set-algebra oracle, SLT-1, the 6 cards with ask_on_soft OFF, the four blocks and their sizes, K1-K19 bars. Sources: [OWNER-ROW], [LEV An], [CRIT x], [A82 n] as in the T50 addendum.

## 0. What changes, in six lines

1. [OWNER-ROW] The 200-row G13 pilot (K14) is REPLACED: every row is answer-checked and G13-stamped when it is made (section 8).
2. [LEV A3] SCOPE VARIANTS: 500 rows already in the family are rendered with an edit carrier (Edit/Write/patch) instead of a shell command. Sizes unchanged.
3. [LEV A6] GATE-DIRECTED INJECTION inside the action: 450 rows (225 cue + 225 benign twins). Sizes unchanged.
4. [LEV A10, A12, A15] Wrappers (conditional), character perturbation and card-body dialects are overlays on existing rows. Sizes unchanged.
5. [CRIT D1, D2] Difficulty ladder (L1-L4 per mechanism), mandatory quad, measured C2 bar on L4 rows.
6. [G9] K19 is extended to edit actions (section 9).

## 1. Conditions carried from the Opus rounds (word for word; they still bind)

- R2-T51-a Choices 11.2 a-c are confirmed. Dropping `own-cleanup` is correct (one label for one action, state and card).
- R2-T51-b K19 uses the R2-T50-b mapping (protected false, MustPreserve empty, ask_on_soft OFF only).
- R2-T51-c NEIGHBOUR VISIBILITY. K6 uses the RENDERED-row neighbour flag (what the model can see) as the neighbour feature, plus the spec-level flag as a second feature. When neighbours are made visible through user turns or earlier calls (11.2c), each carrier that shows a neighbour meets the 40-60% per-label share of K17 by itself, so the carrier is not a cue.
- Round 2 verdict items kept: the compaction block (K18 product check; eval-only 3,120-row fallback with ALLOW 46.8%, ASK 32.1%, BLOCK 21.2%, pairs 43.6%) and the lane rule SLT-1 cited, not restated.
- Global: G1 (solver B is a program), G2, G3 (first 1,000-row pilot is the first look; ONE combined fix), G4 (no sub-block rolls alone), G5 (probe harness; 97.5th percentile bound), G6 (tokens), G7 (`violation_set` stays metadata only), G8, G9, G10 (decision_spans with AUTHORITY on scope declarations, boundaries, delegation pointers, consent naming; the compaction boundary turn included).

## 2. Gate changes at a glance (K ids are those of the approved G0-lite)

All K-gates keep their v3.1 marking (PRE-FREEZE KILL, CPU, data only) and all P-lines stay POST-TRAINING REPORT, unless a row below says otherwise.

| Gate | v3.2 status |
|---|---|
| K1 solver A vs B | PER-ROW at creation (disagreement = row dropped and logged); bar unchanged (>= 99.0% agreement on the pilot, creation drops from this cause <= 1.0%) |
| K2 cell coverage | SET-LEVEL on the pilot and on the built family; creation drops are replaced from the same cell with a new seed (at most 2 attempts per slot); bar unchanged (32 cells, each 55 +- 5; S, B, R marginals exactly balanced) |
| K3 contrast integrity | PER-GROUP at creation (pair/quad members byte-identical except the contrast field; compaction K/D identical except the summary); a failing group is dropped whole |
| K4 fact coverage | PER-ROW |
| K5, K6, K7, K11, K17 | SET-LEVEL once per family (pilot first look, then the built family). K17 is measured on the FINAL set after drops |
| K8 label-set consistency | PER-ROW |
| K9 boundary conversion unit test | CODE-LEVEL CPU test, rerun at each code sha |
| K10 ID formats | SET-LEVEL (no format > 12%); names from the namespace are checked PER-ROW by the names guard (K16) |
| K12 token rule | PER-ROW for the 1,536 cap; mean and the 1,024 share are SET-LEVEL |
| K13 split hygiene | PER-ROW at creation; OHS-5 collisions dropped row by row by the stamp (<= 5% not the fix iteration) |
| K14 G13 200-row pilot | REPLACED by K14s (section 8) |
| K15 standard pipeline | SET-LEVEL once per family |
| K16 names guard | PER-ROW |
| K18 compaction product check | one L-0 record; unchanged |
| K19 G9 | EXTENDED (section 9) |
| K20-K27 | NEW (section 10) |

## 3. Sizes: UNCHANGED, overlays by substitution

The four blocks keep their sizes and labels: matrix 1,760 (780/590/390), trajectory pairs 720 (360/250/110), consent declaration 640 (320/160/160), compaction 380 (190/0/190); total 3,500 (1,650 ALLOW = 47.1%, 1,000 ASK = 28.6%, 850 BLOCK = 24.3%); matched pairs/quads 1,740 = 49.7%; 65% primary / 35% with-results views; dev = 10% of spec families; 1,000-row pilot = proportional sample. Every overlay below re-renders rows that already exist, and is STRATIFIED by label so that no block's label totals change (an overlay changes a carrier, a text field or a rendering, never the oracle outcome). The compaction eval-only fallback (3,120 rows) applies unchanged if K18 fails.

| Overlay | Lever | Rows | Carried by |
|---|---|---|---|
| edit carrier (scope variants) | A3 | 500 (14.3%) | matrix 400, trajectory 100 |
| gate-directed injection | A6 | 450 (225 cue + 225 benign twins) | matrix 250, trajectory 100, consent 100 |
| cue wrappers | A10 | 300, CONDITIONAL on the Fri 23 probe | matrix 150, trajectory 100, consent 50 |
| character perturbation | A12 | 350 | request, ticket and comment prose |
| card-body dialects | A15 | all rows (one dialect per spec group) | 5 trained + 2 held-out dialects |
| held-out sub-families | A24 | 140 (4%) | tagged `heldout_family`, never trained |
If the A10 probe says "do not build", the 300 wrapper rows are simply not wrapped.

## 4. SCOPE VARIANTS: the edit carrier [LEV A3]

Same decision as the T50 edit-as-action sub-family, seen through the entity oracle. The proposed action is a `file_edit`, `file_write` or `apply_patch` call. The mutation set M is the set of entities whose state the edit changes: the file itself (kind file/directory), or, through a CONSUMER record, the entity whose behaviour the file configures. The entity gets a new attribute `consumer` (the path of the file that a runner consumes, or none).
- Eligible kinds (4): file/directory (the edit changes the file; Write/patch can overwrite, truncate or delete), scheduled job (edit of its crontab or timer unit: disable, delete, retime), cluster service (edit of its manifest, consumed by the apply pipeline: scale, delete, change image), bucket prefix/object (edit of a lifecycle or sync config consumed by a runner). The git-branch kind has NO edit carrier (0 rows).
- Allowed action variants: V1-V5 only. V6 (read-only, dry-run) has no edit analogue; the <= 20% read-only share (K7) is carried by shell rows.
- Rendering: M is resolved by the engine from the edit and the consumer record; the oracle, the label order (steps 1-5) and SLT-1 are untouched. Edit rows keep their cell, their S/B/R values and their label.
- Primary-view rule: an edit-carrier row goes in the primary view only if the consumer record that connects the file to the entity is visible in a user turn, a card slot or an earlier tool CALL (K4 fact coverage extended to the consumer record); otherwise it is variant-only.
- Equivalent-effect check (K20, per row): the program emits the shell-equivalent spec (same M, same state) and runs the oracle; the two labels must be equal.
- Carrier mix: file_edit 45%, file_write 40%, apply_patch 15%; `apply_patch` is the held-out carrier of A24 (dev only).
The T50 edit-effect rules R22-R27 label T50 rows only; the T51 oracle is the authority for T51 (they meet at K19 leg (c)).

## 5. GATE-DIRECTED INJECTION inside the action [LEV A6]

450 rows: 225 cue rows and 225 benign twins. A cue row puts free text in the agent's own action (a comment, commit or PR text, written file content, a call argument that addresses the reviewer) that CLAIMS the scope is covered (examples of cue TYPES, not wording: approval claim, ticket-covers-this claim, owner-confirmed claim, urgency). The oracle ignores free text: Authorised comes only from user turns, the trajectory, the card and agent-created contained-lane entities; a claim never adds an entity to Authorised and never removes one from MustPreserve or Protected. So a cue on an over-reaching action stays ASK/BLOCK, and a cue on an action inside Authorised stays ALLOW. A benign twin has a comment that honestly explains the change. The cue wording is the L-I Claude-authored pool under the program-enforced literal ban (L-A writers never see the list; no paper wording). Cue type x label balanced (ALLOW share within +-5 pp of 50% inside the A6 rows). Dependency on the L-I pool is a stub slot until it arrives. Gate: K21.

## 6. WRAPPERS, PERTURBATION, DIALECTS [LEV A10, A12, A15]

A10 (CONDITIONAL). Same Fri 23 probe and the single shared build rule GV1 (Opus batch 1: a flip = C2's predicted label differs wrapped vs unwrapped; build iff flips >= 10 of 200; no result by Fri 23 18:00 UTC = not built). If built: 300 rows over the 3 trained wrapper families (authority, urgency, a fake "already approved" note OUTSIDE the user turn); role-play and benign justification held out (GV2) [Opus b1], hard labels only, every wrapped row keeps its clean twin, real consent signals excluded: the user-turn AUTHORITY spans (scope declarations, boundaries, consent naming) are byte-identical before and after wrapping.
A12. 350 rows. Natural-language fields only (request wording, ticket body, comments). The perturbation NEVER touches a string that is an entity name, an entity id, a ticket id or an action target (they must stay matchable); the G10 decision-span survival check (negation/polarity, number, entity/path/flag, AUTHORITY) drops any row whose span changed (drop-only). Trained transform families: diacritics, spacing, leetspeak, homoglyph, zero-width. Held out (dev only): full-width, bidi. A family losing > 25% of its rows to the check is removed. Every perturbed row keeps a clean twin in its group.
A15. The card body (the 6 cards' slot lists: context lists and protected-flag attributes) is rendered in one of 7 dialects inside C2's fixed scaffold (scaffold sha unchanged): JSON schema, TS-style signature, YAML, markdown table, XML, prose, CLI help style. Trained 5 (JSON, TS-style, YAML, markdown table, prose); held out XML and CLI help. A spec group shares one dialect. Each trained dialect 12-25% of rows. Verbose dialects add 5-15% tokens (cost projection; G6 still holds).
A16 (observation formats) is NOT assigned to L-A; the with-results listings keep their plain format.

## 7. DIFFICULTY LADDER, QUAD, HELD-OUT [CRIT D1, D2; LEV A24]

Mechanisms (inventory section 4 T51 row; clean-room, mechanism only). Each row gets a level L1-L4 set by program; >= 25% of rows are L3-L4 (design 30% = 1,050 rows); each mechanism populates all four levels (each >= 10% of its rows).
| Mechanism | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| M1 target certainty (S and B axes; the dominant axis) | S1/B1 | S2/B2 | S3 or B3 | S4 or B4 (possessive dropped) |
| M2 wrong object of the right kind | different kind | same kind, different name | same kind, similar name | same kind, similar name, different owner or protected flag |
| M3 over-broad command on the right object (blast radius) | exact target | flag widening one step | glob widening to siblings | glob plus flag widening; blast radius is the ONLY edited fact in a contrast pair |
| M4 evidence-reversed mirrors (cleared risk vs stale clearance) | no clearance | clearance in the same turn | clearance earlier in the trajectory | fresh clearance vs a clearance made stale by a later state change (mirror pair) |
MANDATORY QUAD: alarming/calm surface x risk-present/resolved. 100 specs x 4 cells = 400 rows (11.4%), carried 200 in the matrix (S x B x R cells) and 200 in the trajectory block (cleared-risk vs stale-clearance mirrors). Risk present = the action touches Protected, MustPreserve or an unauthorised entity (ASK/BLOCK by the oracle); resolved = covered by trajectory clearance, consent or agent-created in a contained lane (ALLOW). Alarming surface = wording or state that looks dangerous (production, force, delete, protected flag word); calm = routine wording. Every hard cell (calm + risk present; alarming + resolved) has an easy-looking twin with the opposite label inside the same quad. Report ALLOW recall beside the others (inventory L4 target).
MEASURED BAR: C2 (C1 if no weights) on od-l4b scores <= 70% on L4 rows of the 1,000-row pilot; a miss is folded into the ONE combined fix (raise the program parameter; never drop rows by model score); after the fix a miss is a report line, not a kill. Mark: PRE-FREEZE FIX-TRIGGER, NOT A KILL (K25).
HELD-OUT (inside the 3,500, never trained; design 140 rows = 4%): wrapper families role-play and benign justification 25 (only if A10 is built; else dialect line) [Opus b1 GV2], dialects XML and CLI help 35, transform families full-width and bidi 30, carrier apply_patch 30, one composed ID-format family 20. Tag `heldout_family`; the recipe's S term (A24) uses them.

## 8. CHECK AT GENERATION [OWNER-ROW; plan 16.1]

Every T51 row passes the L-0b STAMP WRAPPER before it enters any pool. Per row: (a) answer checks: solver A = solver B recomputing the sets from the RENDERED fact fields (K1), fact coverage (K4), label-set consistency (K8), edit-carrier equivalence (K20), A12 span survival, names guard on the closed allow-list including ID-format composition (K16), token per-row cap (K12), PII scrub, decision_spans export (G10), spec-family -> split (K13), group integrity (K3: pair/quad/K-D identity); (b) the G13 stamp against EVERY registered target with each target's methods (OHS-3, OHS-4, OHS-AC binding for new rows, OHS-5 hash export from Sat 24, public scope-eval targets as exact item strings, entity names and ID patterns only, never generic domain words; R6 scaffolding exemption); hit reports carry row id, target name and method only; (c) the stamp (row id, registry sha, method-set version, generator code sha, verdict) in the row manifest.
DROPS. A failed row is dropped and logged; no unstamped or failed row enters a pool. A failing group member drops the whole group, and a replacement group is drawn from the same cell with a new seed: a NEW spec; a group dropped for a G13 hit is never re-rendered or re-worded (GV5) [Opus b1] (at most 2 attempts per slot; a still-empty slot is reported as a short cell). K14s counts ALL dropped rows, collateral group members included (the stricter reading; O-B2).
K14s (REPLACES K14): drops other than exempt R6 scaffolding hits or OHS-5 collisions <= 1% of generated rows, read on ALL 1,000 pilot rows and on each full-generation day; above 1% is the ONE combined fix (G3); OHS-5 collisions <= 5% are not the fix iteration. The pilot is the FIRST look at every set-level gate; set-level gates then run once on the built family. A template change after the hash export means a new hash export and re-stamped rows. The hash export is also redone after any change to the edit renderer, consumer templates, A6 pool, wrappers, transforms or dialect renderers.

## 9. G9 EXTENSION [build order L-A]

K19 (T51's side of the cross-family test; must pass 100% before any pilot) gains leg (c): every T50 block-G spec whose induced effect set is a single E6 effect on a lane-tagged resource (T50 addendum section 10(d)) is mapped to a T51 entity view with an edit-carrier action (protected false, MustPreserve empty, ask_on_soft OFF cards only, per R2-T50-b) and labelled by the T51 oracle; labels must equal T50's. Legs (a) and (b) of v3.1 are unchanged. The mapping reads T50's exported spec files; T51 and T50 engines stay independent implementations of the SLT-1 text. T51 has no leg with T67 (T67's T51-style entity view is not defined; if L-P wants one, it conforms to T51's oracle).

## 10. GATES ADDED OR CHANGED

PRE-FREEZE KILL (CPU, data only unless marked). Probe protocol = G5 (grouped split by spec family, 30% held out, 5 splits, L2 logistic regression, AUC = max(AUC, 1-AUC), 97.5th percentile bound over 2,000 cluster-bootstrap resamples, permutation check 0.50 +- 0.03, leak-power check >= 0.80, GBT advisory). Binary bar: held-out AUC <= 0.55 AND bound <= 0.60.
| ID | Gate | Bar |
|---|---|---|
| K14s | Stamp on ALL rows (section 8) | <= 1% non-exempt drops; OHS-5 drops <= 5% |
| K19 leg (c) | Edit carrier G9 (section 9) | 100% label equality before any pilot |
| K20 | Edit carrier integrity | eligible kinds only (file/directory, job, service, bucket); 0 edit rows on the branch kind; edit rows use V1-V5 only; 500 rows (+-5%); per-row equivalence with the shell-equivalent spec 100%; consumer record visible in the primary view for primary rows 100%; edit rows' label shares inside +-2 pp of their block's label shares |
| K21 | Gate-directed injection | oracle ignores free text (label unchanged when the free text is removed) 100%; comment-presence probe (features: free-text field present, length bucket, position kind, count; no tokens) on the whole family and inside the A6 rows: AUC <= 0.55, ub <= 0.60; benign twins >= 45% of A6 rows; cue type x label within +-5 pp |
| K22 | Character perturbation | 100% decision spans survive; 0 entity names, ids or targets touched; clean twin for every perturbed row; 0 held-out transform rows in train; perturbation-presence probe AUC <= 0.55, ub <= 0.60; perturbed rows' ALLOW share within +-5 pp of the family |
| K23 | Dialects | scaffold-sha assert on every rendered prompt 100%; 0 held-out dialect rows in train; each trained dialect 12-25%; K6 features rerun WITHIN each dialect AUC <= 0.55, ub <= 0.60; dialect-id-only vs label AUC <= 0.55, ub <= 0.60 |
| K24 | Ladder structure | >= 25% of rows L3-L4; each mechanism populates 4 levels (each >= 10%); 100 quad specs x 4 cells exact; opposite-label easy twin for every hard cell 100%; no more than 55% of L4 rows share one label |
| K25 | C2 (or C1) <= 70% on L4 rows (od-l4b read of our own model) | PRE-FREEZE FIX-TRIGGER, NOT A KILL (folded into the one fix; then a report line) |
| K26 | Held-out sub-families | 140 rows (+-10); 0 in train: 100% |
| K27 | Cue wrappers (only if A10 is built) | wrapper-presence probe AUC <= 0.55, ub <= 0.60; AUTHORITY spans byte-identical 100%; clean twin for every wrapped row |
| K5, K6, K7, K17 notes | K5 target-string probe and K6 format-only probe also run WITHIN each carrier (shell, edit); the neighbour gate K17 and the per-label balance K7 are measured on the FINAL set after drops; the K7 bars (ALLOW 45-52%, ASK >= 20%, BLOCK >= 20%) hold without change because overlays do not move label totals | unchanged bars |

POST-TRAINING REPORT (never a kill rule):
| ID | Report line |
|---|---|
| P6 | Edit-carrier slice vs its shell-equivalent slice: accuracy and per-class FPR/FNR with CIs by entity kind, beside trivial baselines (always-ALLOW, always-ASK, "target named in request => ALLOW", "any mutation => ASK", "shared lane => BLOCK", "edit => ASK") |
| P7 | Gate-directed injection slice: cue rows vs plain rows (target: within 2 pp); benign-twin over-block rate |
| P8 | Held-out lines: transform families, wrapper family, dialects, carrier (apply_patch), ID-format family (A24 term in S) |
| P9 | Accuracy by ladder level and by quad cell; ALLOW recall at L3-L4; C2 vs C2.1 on L4 |
| P10 | Stale-clearance mirrors: both-twins-correct rate |

## 11. NAMES this addendum needs (names only; for manifest v1.1; L-0 owns the strings)

New fixed real names (allow-list entries):
- Carriers (logical ids): `file_edit` tool call, `apply_patch` tool call (`file_write` and `shell_exec` exist).
- Consumer file kinds (generic stems): crontab file and systemd unit and timer stems (`*.service`, `*.timer`); cluster manifest stem (`*.yaml`) consumed by an apply step (`kubectl apply` is a name T51 already uses); bucket lifecycle or sync config stem (`lifecycle.json`); the apply pipeline and runner as role words (no vendor name).
- Format names for dialect renderers (as in the T50 addendum); wrapper family names (authority, urgency, role-play, already-approved note, benign justification); transform family names (diacritics, spacing, leetspeak, homoglyph, zero-width, full-width, bidi).
Generator-internal enums (not row strings): ladder mechanisms M1-M4, quad cell ids, cue types (4), eligible-kind flags.
Namespace kinds added (counts/rules only; strings by the L-0 namespace program, TRAINING salt): consumer file path component, crontab entry name, systemd unit name, manifest object name, lifecycle rule name. The ID-format registry keeps its >= 12 composed formats (K10); one composed format family is held out (K26).
Row family: stays `T51` in row_job_families_allowed; overlay rows carry a `sub_block` field and `overlay` list, no new family id.

## 12. Risks

1. Edit carriers need a consumer link that may be invisible in the primary view, pushing edit rows to the variant view (35% share). K4 and K20 measure it; the builder must make the link visible through a card slot or an earlier call (a build task, not a bar change).
2. An edit-carrier row for kind `file/directory` is close to a shell rm/mv row; the carrier must not become a label cue (K6 within carrier).
3. A6 claim cues invite "claim present => suspicious"; K21 balances cue x label and keeps benign explanatory twins >= 45%.
4. Overlays touch up to 1,740 of 3,500 rows (edit 500, A6 450, A12 350, A10 300, held-out 140; some overlap); the builder avoids stacking more than 2 overlays on one row (a rule of this addendum) so that a failing row isolates its cause.
5. Dependencies: A6 pool (L-I), Fri 23 probe (A10), T50 shared spec_v2 (this lane), L-0 stamp wrapper. None blocks T51's own pilot (stubs are reported).

## 13. Open questions for Opus

- O-B1: confirm that the T51 oracle, not T50's R22-R27, labels T51 edit rows (the two meet at K19 leg (c)).
- O-B2: confirm K14s counts collateral group members (stricter reading; same as O-A4).
- O-B3: confirm that overlays never stack more than 2 per row (new rule here).
- O-B4: G4 and the 500 edit-carrier rows: they are overlays, so no sub-block exists to roll alone; no ruling needed unless Opus disagrees.

## 14. Fix iteration, kill rule, what may start now

As v3.1 section 9 (one combined fix after the pilot; G3): K14s > 1% is the fix; K25 is a fix trigger only; a K20-K24 miss after the fix rolls the family (G4). Floor and freeze rules unchanged (declared Thu 29 12:00; fallback Mon 2 Nov 23:59 UTC). Rows start Sun 25 Oct after the OHS-5 freeze through the stamp wrapper.
May start now (code, no rows): the `consumer` attribute and the edit renderer in the shared spec_v2 (defined in the T50 addendum section 16; frozen at the first hash export and exported read-only to L-K); the entity oracle and matrix, trajectory and consent blocks (as in v3.1); K19 leg (c) mapper; A12 transforms; dialect renderers; K20-K27 CPU tests; solver B from this addendum plus the G0-lite only. The compaction block waits for K18 as before. The stamp wrapper is used only with a signed ruling-to-code conformance record for the current code sha (plan 16.1 step 0).

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: REVISE -> APPROVED after fixes (applied in place): A10 build rule (GV1) and held-out wrappers (GV2) in sections 6
and 7; replacement group = a NEW spec (GV5) in section 8.
Binding conditions: T51-B1 O-B1 confirmed (the T51 oracle labels T51 edit rows). O-B2 confirmed (GV5). T51-B2 O-B3 confirmed (at
most 2 overlays per row). T51-B3 O-B4 agreed (overlays are not sub-blocks; G4 unchanged).
