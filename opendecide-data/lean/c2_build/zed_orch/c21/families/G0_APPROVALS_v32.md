# C2.1 G0 APPROVALS v3.2 (Opus batch 1; Opus 5.5 high; Sun 18 Oct 2026 UTC)

Read for this approval: families/LR/G0_LITE.md (the only NEW G0-lite on disk), the 12 families/*/G0_ADDENDUM_v32.md files
(T50, T51, T53, T41c, T54, T55, T56, T42c, T57, T56g, GEN, VOICE), the T50 G0-lite sections 1-5 (shared core, SLT-1), the
round 1 / round 2 file families/G0_APPROVALS.md, C2_1_PLAN_v3.md section 16 (16.1-16.9), C2_1_BUILD_ORDER.md (header, global
order, standard and v3.2 pipelines, kill rule, v3.2 lane additions L-0 to L-P and the v3.2-r checklists), PREREG_FINAL.md
blocks A77, A79, A82 only, and l0/NAMES_MANIFEST_V1.json. NOT opened: any path containing "ohs" or "sealed", OHS5_BRIEF_DRAFT.md,
SEALED_DELTA_v32.md, plan section 3, C2 build files, data/, logs/, ~/.claude, any generator, wording pool, dataset file or
benchmark item text. No rows, no code run, no model or API call, no Modal.

NOT YET WRITTEN (plan 16.9), so not reviewed here and not in manifest v1.1 except as family ids (plan Sk 24): the G0-lites of
T59, T60 (L-K), T63, T66, T67 (L-P) and T62, T65 (L-P wave C, due Fri 23). Each needs its own Opus approval before code.

## Owner rule check (18 Oct, binding: "If you're building one row, check that row at that same point and that's it ... then train.")

Every one of the 13 files routes every row through the L-0b stamp wrapper (answer checks + G13 against EVERY registered target
+ manifest stamp) at creation, removes the 200-row G13 pilot, reads the 1% trigger on ALL pilot rows and each generation day,
runs set-level checks once per family (pilot first look, then built family, never at the mix), uses only clean-stamped rows
in the mix and leaves the binding G13 as one confirming pass. Replay clean-up once (plan 16.1 step 5) is L-0b's and is cited
correctly where touched (GEN, VOICE source rule). The ruling-to-code conformance gate (plan 16.1 step 0) is in every file.
One gap was found and closed by GV5 below (re-wording a G13-hit row until it passes would launder a leak past the check).

## Verdict table

| File | Lane | Verdict | Must-fix (applied in the file by this session) | Binding conditions |
|---|---|---|---|---|
| LR/G0_LITE.md (NEW) | L-R | REVISE -> APPROVED after fixes | 8 (LR-M1 to LR-M8) | LR-B1 to LR-B12 |
| T50/G0_ADDENDUM_v32.md | L-A | REVISE -> APPROVED after fixes | 3 (GV1, GV2, GV5 text) | T50-B1 to T50-B6 |
| T51/G0_ADDENDUM_v32.md | L-A | REVISE -> APPROVED after fixes | 3 (GV1, GV2, GV5 text) | T51-B1 to T51-B3 |
| T53/G0_ADDENDUM_v32.md | L-A | REVISE -> APPROVED after fixes | 4 (sinks withdrawn; GV1, GV2, GV5 text) | T53-B1 to T53-B4 |
| T41c/G0_ADDENDUM_v32.md | L-I | REVISE -> APPROVED after fixes | 2 (GV5 regeneration; GV2 held-out cue family) | T41c-B1 to T41c-B5 |
| T54/G0_ADDENDUM_v32.md (+ PART S) | L-T | REVISE -> APPROVED after fixes | 6 (GV1, GV2, GV3, GV4, GV5, GV6 text in Part S) | T54-B1 to T54-B5 |
| T55/G0_ADDENDUM_v32.md | L-T | REVISE -> APPROVED after fix | 1 (A14 condition, GV4) | T55-B1 to T55-B3 |
| T56/G0_ADDENDUM_v32.md | L-T | REVISE -> APPROVED after fixes | 2 (f_zero_collected out of the hard bin; A14 condition) | T56-B1 to T56-B4 |
| T42c/G0_ADDENDUM_v32.md | L-C | APPROVE | 0 | T42c-B1 to T42c-B5 |
| T57/G0_ADDENDUM_v32.md | L-C | APPROVE | 0 | T57-B1 to T57-B5 |
| T56g/G0_ADDENDUM_v32.md | L-C | APPROVE | 0 | T56g-B1 to T56g-B3 |
| GEN/G0_ADDENDUM_v32.md | L-G | APPROVE | 0 | GEN-B1 to GEN-B6 |
| VOICE/G0_ADDENDUM_v32.md | L-G | REVISE -> APPROVED after fix | 1 (dictionary licence list) | VOICE-B1 to VOICE-B5 |

Meaning: every must-fix item is design text and was applied in place by this session (each edit is listed below and marked
"[Opus b1 ...]" in the file). No third round is needed: the fixes are exact text taken from this file. Each of the 13 files
also carries an appended block "Opus batch-1 rulings v3.2" with its verdict, the fixes and its binding conditions; the build
skeptic checks code against that block and refuses a code review without it. Generator, mapper and solver CODE may start in
every reviewed lane now. ROWS still start only after the OHS-5 freeze, the registry sha, manifest v1.1, a signed stamp
service and a signed conformance record (Sat 24 18:00 rules unchanged).

Clean checks every file passed: gold is program, execution or the dataset's own label through an Opus-approved table (no LLM
sets or changes a label; G1); every PRE-FREEZE gate has a numeric bar; model-based ladder reads (C2 <= 70% on L4) are fix
triggers, never kills; one combined fix per family (G3); G4 whole-family kill kept (GEN sub-blocks and VOICE lane rule as
approved); no NC / GPL / AGPL component; held-out material never trained; every lever is by substitution (no P0 size moved);
names come from the TRAINING-salt namespace except the scoped L-R / P1-realism exemption (plan 16.3 rule 4, Sk 8).

## Global rulings v3.2 (GV1-GV9; bind every lane and every file; cited by number)

GV1 ONE A10 BUILD RULE (answers T50 O-A6; replaces the three different proposals: T50/T51/T53 "> 5%, 11 or more", T41c ">= 10",
T54 Part S "3.0%, 6 of 200"). Fixed now, Sun 18 Oct, before any read. On the ONE shared Fri 23 probe (200 wrapped items built
from C2's existing dev rows, eval-only, registered as internal held-out targets), a FLIP is: C2's predicted label on the
wrapped item differs from C2's predicted label on its unwrapped original. A10 is built in every lane iff flips >= 10 of 200
(5.0%; an exact one-sided binomial test against a 2% noise rate gives p < 0.01). Fewer than 10, or no result by Fri 23 18:00
UTC, means A10 is not built in any lane; its quotas revert to plain rows; the templates stay in the Thu 22 hash export.

GV2 ONE HELD-OUT WRAPPER SET (A10, A24). Role-play and benign justification are held out in EVERY lane, fixed, not drawn:
L-A and L-T wrap.roleplay + wrap.benign_justification; L-I the cue family cue.persona (= wrap.role_play +
wrap.benign_justification); L-C W3 + W5 (already so). Trained wrapper families: authority, urgency, fake "already approved"
(plus T41c's other cue families). Reason: a family held out in one lane but trained in another is not held out for the model;
the A24 term and every held-out wrapper report line would be inflated.

GV3 ONE A14 BUILD RULE (T41c 5.1 and Part S S.5 agree; now fixed for all lanes). On the shared Fri 23 buried-payload probe:
build iff short-input recall minus buried-payload recall >= 5 pp AND the paired-bootstrap 95% lower bound of that gap > 0.
Otherwise, or no result by Fri 23 18:00 UTC, A14 is not trained in any lane.

GV4 G6 BINDS A14 (answers T54 11.1, T55 item 1, T56 item 6, T41c Q1). No G6 exemption in C2.1: every trained row is <= 1,536
tokens; mean <= 800 and > 1,024 on <= 10% per family. A14 trained rows: T41c 1,000-1,500, L-T 1,100-1,536. The 1.5-3K and
3-8K forms are eval-only (LS block, L-E). Reason: G6 is an approved global ruling and no measured trainer max-length record
exists that shows longer rows are trained without truncation; a lever cannot loosen it. C2.2 item.

GV5 G13 HITS RETIRE THE SPEC (gap found in this batch; stricter only). A row dropped by the G13 stamp (any non-exempt method
hit; R6 scaffolding and OHS-5 collisions keep their own rules) retires its spec / skeleton / scenario: the replacement is a NEW
spec drawn for the same cell with a new seed. A G13-hit spec is never re-worded, re-rendered or regenerated on the same
skeleton, and when any member of a pair, quad or group is G13-dropped the WHOLE group is dropped. Same-skeleton regeneration
and orphan partners stay allowed only for NON-G13 answer-check drops (A/B disagreement, parse-back, survival, layout,
label-preserving checks). L-R: a hit row is dropped; its source row is never re-sampled into another rendering. Every trigger
reads FIRST-PASS drops and counts collateral group members (stricter reading; answers O-A4, O-B2, O-C3). Reason: re-wording
until G13 passes would carry a leaked structure past the leak check.

GV6 ONE PERTURBATION LIBRARY (A12; answers T41c 4.2). Canonical shared ids: trained pert.diacritics, pert.spacing,
pert.leetspeak, pert.homoglyph, pert.zero_width; held out in EVERY lane pert.fullwidth, pert.bidi, pert.upside_down (a lane
that does not generate a held-out family still never trains it). pert.zero_width = ZERO WIDTH SPACE U+200B inside a word;
no ZWJ / ZWNJ, no Tags block U+E0000-E007F, no variation selectors in any lane (A11 strips or flags those at serving). L-T's
`xform.*` and L-A's prose names are aliases of these ids; job manifests use pert.*. A12 totals are about 2,000 rows over the
gate lanes plus L-K (plan "about 3,000" is DERIVED; no row-count bar); reported, not a gate.

GV7 A15 SCOPE (answers T54 11.4, T55 item 7, T56 item 9, T41c Q4, T42c item 6, T57 item 6, T56g item 6). In C2.1 only L-A builds
dialect rows (plan 16.9 is the binding scope list); other lanes carry the renderer's `dialect` parameter at its default. An
extension is an orchestrator ruling before the Thu 22 hash export, never later.

GV8 PILOT-POOLED SUB-BLOCK PROBES (answers T54 6.4, T55 item 6, T56 item 8). On the 1,000-row pilot a per-sub-block probe may be
pooled across sub-blocks of equal k; the per-sub-block read on the fully built family is the binding one. Bars unchanged.

GV9 HELD-OUT DEV ROWS AND ACCOUNTING. Each family's own statement binds (inside the size: T50, T51, T53, T56g natural DEV;
outside: T41c HO/BD/LS, T54, T55, T56, T42c, T57 wrapper/format dev rows). The mix builder excludes every row tagged
heldout_family or split.dev_only (CPU test) and the money projection counts only trained rows.

## Per-file decisions

### LR G0-LITE (block R): REVISE -> APPROVED after the 8 fixes below

Checked against plan 16.3 rules 1-8, 16.1, 16.5 (A1-A6, B1-B5, E5), the build order L-R block, A79 R5 and A82 1-9.
Arithmetic re-checked: non-code caps 22,100 (safety 400, intent/dialogue 5,000, NLI 5,100, reading 5,300, tables 1,700,
reasoning 4,400, low relevance 200); code-realism caps 6,000 incl. MBPP.
Must-fix (applied):
- LR-M1 E5 and section 10 missed SB6, which manifest v1 lists as excluded even if R5 is adopted. Added.
- LR-M2 E2 would DENY two tier-A sets the inventory clears: SciFact abstracts (ODC-By 1.0) and Juliet (US-government public
  domain with a CC0 foreign-rights grant). Both named in E2; no other class added.
- LR-M3 Code-licence whitelist made ONE list (Sk 26: MIT, Apache-2.0, BSD-2, BSD-3, CC0) for all re-fetched or shipped code:
  LR-07 listed ISC; LR-10 dropped only GPL / LGPL (MPL, unknown and others would have passed). Fixed; matches T57 section 8.
- LR-M4 E3 did not say which datasets need the A82 1 split-scoped release. Now: tier B2 plus the four Nimble sets (MultiNLI,
  VitaminC, SQuAD 2.0, BoolQ), whose test/dev split is one we read; others need the A61(b) record and per-row stamps only.
- LR-M5 ChessBench "default LEFT OUT" rested on an estimate (owner rule: decide on measured usage, never cut from an estimate).
  Now decided by the Wed 21 measured throughput x the record's measured train-split size; left out (logged with numbers) only
  if that measured pass cannot finish in Mac windows by Thu 29 12:00. Same rule for ESCI.
- LR-M6 R14 exemption list now includes MBPP (execution gold) and the LR-01 / LR-02 twins (benign by construction).
- LR-M7 MBPP accounting was inconsistent (section 1 put it in P1 families; OQ-R7 in block R; T42c section 10 used another
  form). Now: family id LR-code, tag P1-realism, counted in block R and outside T42c's 3,000, question form T42c-Q-TFAIL2 per
  the T42c contract, shed with the P1 realism slices (money shed step 6). Section 1 sums corrected (22,400 + 3,000 = 25,400;
  twins +400).
- LR-M8 LR-09 / LR-10: no GitHub issue text and no problem_statement in any row (strict A82 4 reading, as T57 item 7).
Binding conditions (copy into the code review; the conformance map covers each):
- LR-B1 "Large label set" = more than 8 labels; a set with <= 8 labels shows all its labels (SNIPS 2017-06 has 7 intents).
- LR-B2 Gold-position balance per dataset: the gold letter's share at each position within 1/k +- 3 pp (added to R5).
- LR-B3 Swap negatives must be wrong by program: Spider swap negatives only where the swapped query's execution result on the
  shipped SQLite database differs from the gold query's result (CPU, no model; else the pair is dropped); CommitPackFT swap
  pairs dropped where either message has < 4 tokens or the two messages have token Jaccard >= 0.5.
- LR-B4 FinQA near-miss distractors that equal the gold after rounding to the dataset's answer precision are not used (R5).
- LR-B5 DataDog (LR-04, OQ-R3): its rows are T63 realism rows (family T63, P1-realism), not block R. Negatives are T63
  generator rows under T63's gold by construction; LR-04 maps nothing before the T63 G0-lite is approved; R7 balance and the
  T63 name-shape probe are measured on the COMBINED slice (DataDog positives + T63 negatives); the record lists every field
  read and confirms none comes from inside the payload ZIPs.
- LR-B6 OQ-R1: question-stem wording pools are allowed (no data, no label); recorded in the conformance record as wording, not
  block-R content; they are hash-exported, under the literal ban, and G13-stamped as row content (the R6 scaffolding exemption
  does NOT cover them). The Sk 6 sentence "the twins are the only Claude-authored block-R text" refers to content text.
- LR-B7 OQ-R2: the twins (about 400) are block-R rows with family id LR-safety, counted in block R; the mix builder is told.
- LR-B8 OQ-R5 approved: ONE set-level correction per dataset for R7, R8 or R9 (same rules, new seed or added wordings), logged,
  then pass or left out; it is that dataset's one fix. R10 keeps its own single re-sample (Sk 25).
- LR-B9 OQ-R6 approved with LR-M6. The screen also reaches heuristic-label rows (ManySStuBs4J, TSSB-3M): a stricter, drop-only
  extension of A46, recorded as such in the conformance record.
- LR-B10 OQ-R8 approved: distractor spans come only from the same example's own document or paragraph set; every annotated
  supporting span is kept (multi-hop sets keep all supporting paragraphs).
- LR-B11 ESCI whole-split G13 covers the train split of every release version the mapper draws from.
- LR-B12 The HotpotQA 8.5 ruling, the A61(d) two-stage ruling, the A82 1 strict-reading ruling and the Gandalf selection-rule
  record are Opus batch-2 items (plan 16.7, Mon 19); nothing here pre-empts them. LR's S-pre batch 1 waits for A61(d).

### T50 SHELL-GATE addendum: REVISE -> APPROVED after fixes

Arithmetic re-checked: blocks sum to 4,000 / 2,039 / 674 / 1,287; block G 1,600 (980 / 200 / 420); parity 490 of 800 ALLOW
on each side (61.25%); K10 holds (50.98% / 16.85% / 32.18%); A6 rows over L-A = 700 + 450 + 350 = 1,500 (plan floor).
Must-fix (applied): A10 threshold text -> GV1; held-out wrapper -> GV2 (section 8 and section 9 held-out line); section 11
replacement group -> a NEW spec, GV5.
Binding conditions:
- T50-B1 O-A1: K10 and the A3 ">= 60% ALLOW" rule stay as written; K6 runs within each carrier; the carrier-only probe K33 is a
  REPORT line with its number published. P8 adds the baseline "edit carrier => ALLOW" and reports recall on state-bearing
  non-ALLOW edits against it. Reason: shell-side ALLOW cannot rise above about 45.8% under K10's 52% cap, so the gap cannot be
  closed inside approved bars; within carrier the contrast pairs carry the signal.
- T50-B2 O-A2 confirmed: K21 leg (e) is a pre-pilot gate of T67; T50's hashed table is authoritative; T67 conforms.
- T50-B3 O-A3 confirmed: R27 clears a soft induced effect only when the user names BOTH the induced operation and the target.
- T50-B4 O-A5: Option 1 binds (G4: T50 is kept or killed whole). Option 2 is a plan change only the orchestrator can make;
  flagged to the orchestrator, not ruled here.
- T50-B5 Ladder M4 L4 "scoped and authorised = ALLOW": "authorised" means the SLT-1 clearing condition computed by the oracle
  (user names operation and target); the ladder parameter never sets a label; under ask_on_soft C4 stays BLOCK (R2-T50-c).
- T50-B6 The real file stems of section 13 go to the manifest as names (v1.1 fixed_real_path_stems); lockfile package names stay
  seeded (no real third-party package names in P0 rows).

### T51 SCOPE-BOUNDARY addendum: REVISE -> APPROVED after fixes

Must-fix (applied): A10 threshold -> GV1; held-out wrapper -> GV2 (sections 6 and 7); section 8 replacement group -> GV5.
Binding conditions: T51-B1 O-B1 confirmed (the T51 oracle labels T51 edit rows; R22-R27 label T50 only; they meet at K19 leg
(c)). T51-B2 O-B3 confirmed (no more than 2 overlays per row). T51-B3 O-B4 agreed (overlays are not sub-blocks; G4 unchanged).

### T53 EGRESS-SECRET addendum: REVISE -> APPROVED after fixes

Must-fix (applied):
- T53-M1 O-C1: the stdout_echo, temp_file and shell_history sinks are NOT added in C2.1. Reason (G9): T50 R02 labels a
  user-named credential read ALLOW (soft, named), and secret content written to a file is decided by SLT-2 rule 7 through its
  visibility record (T50 R26). Treating stdout, temp files and shell history as rule-6 "log or telemetry" sinks (secret =>
  BLOCK / hard) would give the same action two labels across T50 and T53 and would change an approved hard rule. Rule 6 stays
  log / telemetry only; no `sink` attribute; K32 withdrawn; ladder M4 rewritten to indirection levels on existing channels;
  names and report lines updated. A C2.2 item (needs a shared SLT-2 row agreed with T50 first).
- A10 threshold -> GV1; held-out wrapper -> GV2; replacement group -> GV5.
Binding conditions:
- T53-B1 O-C2 confirmed: the 4-way phishing head, 300 rows, 75 x 4. The head drawer stratifies the six K31 string features
  (length, label count, digits, hyphens, IP-literal flag, punycode flag) so their distributions match across the four classes
  before K31 runs (UNRELATED hosts carry subdomains, digits and hyphens at the lookalike rates; TRUSTED odd forms carry raw IPs
  and punycode at the LOOKALIKE rates).
- T53-B2 O-C3 confirmed (GV5). T53-B3 O-C4 confirmed: the head rolls with the family (G4).
- T53-B4 The A6 total across L-A is exactly the plan floor (1,500); a creation shortfall below 1,500 is reported, not back-filled
  from other blocks.

### T41c TAINT addendum: REVISE -> APPROVED after fixes

Must-fix (applied): 1.3 same-skeleton regeneration after a G13 drop -> GV5 (G13 drops retire the skeleton and the group);
3.2 and section 15 held-out cue family -> cue.persona fixed (GV2).
Binding conditions: T41c-B1 Q1 -> GV4 (as written). T41c-B2 Q2 confirmed with GV2 (three new base styles approved). T41c-B3 Q3
confirmed (50% / 50%, |diff| <= 5 pp). T41c-B4 Q5, Q6, Q7, Q8 confirmed as written (Q6: the raw-view K3 gap is published). Q4 ->
GV7. Q9: N is the orchestrator's (from T41's C2 status) and is recorded before the Thu 22 hash export. T41c-B5 The A10 decision
rule of 3.1 is GV1 (same numbers); the Fri 23 decision toggles sampling only.

### T54 TOOL-NEED/PICK addendum (and PART S for T54, T55, T56): REVISE -> APPROVED after fixes

Must-fix (applied, Part S binds T55 and T56 too): S.3 threshold and flip definition -> GV1; S.2 wrapper draw -> GV2 fixed; S.5
margin -> GV3 and tokens -> GV4; section 0 A14 line -> GV4; S.4 zero_width definition -> GV6; section 7 pair closure after a
G13 drop -> GV5; section 9 transform ids -> canonical pert.* (GV6).
Binding conditions:
- T54-B1 Section 8 / 11.3 G9 tension with T59 approved as proposed: T54 cards state "ask when a required value has no source";
  T59's G0-lite must carry a visible card line "proceed with the most likely value when the action can be undone"; the G9 test
  treats them as different cards, and on a T54 card T59's oracle must give T54's label (binding on the T59 G0-lite).
- T54-B2 11.2 confirmed (GV9). 11.5 -> GV8. 11.4 -> GV7. 11.6: renaming ladder ids later is a name-only change.
- T54-B3 11.7 design values approved (sub-block L3-L4 floor 20%, L4 floor 8%, twin rule 80%, A8 dep-drop trigger 40%, A12 drop
  trigger 20%, slices 500 / 300 / 200 / 200).
- T54-B4 The S.6 obsfmt.* ids are L-T's own observation-format ids (they differ in kind from T41c's obs.* operators); both are
  recorded lane-scoped in the manifest.
- T54-B5 `card.t54.schema_binds` is a new policy id (manifest v1.1).

### T55 RECOVER-ESCALATE addendum: REVISE -> APPROVED after fix

Must-fix (applied): section 0 A14 line -> GV3 / GV4 (the old text made A14 depend on an exemption that is not granted).
Binding conditions: T55-B1 items 2, 3, 4, 5 confirmed (120 dev rows outside; V32-11 extension; ev_pos = the last state change;
design values). T55-B2 item 8: L-0 removes the withdrawn LIMBO sentence from the stripped excerpt tools_s5.md (orchestrator
task; the lane does not edit it). T55-B3 items 6, 7, 9 -> GV8, GV7, name-only.

### T56 DONE-CLAIM (done half) addendum: REVISE -> APPROVED after fixes

Must-fix (applied):
- T56-M1 f_zero_collected is a LITERAL-value fault (the zero count is visible as a token while every DONE twin shows a non-zero
  count), so it is not a relation fault and leaves the P-8 hard bin; the hard bin keeps f_filter_excl, f_toplevel_only,
  f_exit_masked and f_unrelated_tests (155 D6 rows). P-8 (ruling 4) keeps its meaning: relation faults are not keyword-readable.
- T56-M2 section 0 A14 line -> GV3 / GV4.
Binding conditions: T56-B1 item 1 confirmed (output-only through the world property n; D5 stays the only declared exception).
T56-B2 items 2, 3, 4, 5 confirmed (no new reason class; the clause `clause.t56.exit_after_pipe` is added to the approved card).
T56-B3 items 7, 8, 9 -> GV9, GV8, GV7. T56-B4 item 10 confirmed (report says "symbolic gold, no execution check").

### T42c CODE-EXEC addendum: APPROVE

Binding conditions:
- T42c-B1 Items 1, 3, 5 confirmed (COMPILE2 300 = 120 / 90 / 90; bash 0; ladder 20 / 30 / 30 / 20; K27 fix trigger; A16 source
  views 5%).
- T42c-B2 Item 2: G4 binds (a COMPILE2-only failure rolls T42c). The licence fallback (Python rows move to TS / Go, or revert)
  is approved: the checker is a missing input, not a failed gate.
- T42c-B3 4.3 MPL-2.0 ruling: an MPL-2.0 component of a checker that is RUN unmodified as an offline tool is allowed (no MPL
  file is modified, vendored or rendered; no tool text in any row, K23); recorded in the licence record. GPL / LGPL / AGPL / NC /
  unknown stay out. (Hypothesis was barred because it would be vendored into rows.)
- T42c-B4 Item 4 with LR-M7: MBPP rows are family LR-code, P1-realism, block R, outside the 3,000, T42c-Q-TFAIL2 form.
- T42c-B5 A10 held-out W3 / W5 are fixed by GV2 (the "seeded draw" words are superseded); A12, A14 not carried (16.9 scope).

### T57 PATCH-VERDICT addendum: APPROVE

Binding conditions:
- T57-B1 Items 1-5 confirmed (A10 150; LOCALISE 480 / 120 / 200 with the executed HUNK rule; WP 45 / 35 / 8 / 7 / 5; CAND-EXTRA
  >= 8%; realism and T57r outside the 3,000 and never against T57; T57r CORRECT / INCORRECT definitions).
- T57-B2 Item 7: GitHub issue text is treated as a social-platform post (strict A82 4 reading): no issue text in any T57r or
  LR-09 / LR-10 row.
- T57-B3 Item 8: a partial subset of the human patch's hunks is not used (it reads as a SWE-Gym patch under Sk 26).
- T57-B4 T57r is a new row-job family id (manifest v1.1) with the P1-realism names exemption; the 3,000 keep the closed list.
- T57-B5 A10 held-out W3 / W5 fixed by GV2; item 6 -> GV7.

### T56g TEST-GAMING addendum: APPROVE

Binding conditions: T56g-B1 items 1-4 confirmed (A10 60; quad 25% each, floor 15%, cap 35%; LEX-ALARM-1 fixed by the builder
before the pilot and hashed; honest alarming cells only through the unchanged label function). T56g-B2 Item 5 confirmed: K4 is
an ORIENTED AUC (a floor); max(AUC, 1 - AUC) stays the reading for near-chance bars only. T56g-B3 W3 / W5 fixed by GV2; item 6
-> GV7.

### GEN addendum: APPROVE

Binding conditions:
- GEN-B1 Point 1: the split stands (TP 2,000 + HX 1,100 from the five sub-blocks; ARITH loses most because TP-DM is arithmetic).
- GEN-B2 Point 2 confirmed: task-defined classes (LG-L1 undetermined, HX-E not stated, HX-U does not say) are in the mix;
  NOTA-GENERIC is built and stays out.
- GEN-B3 Point 3: yes, each TP generator runs S-pre and S-post 8.5 like an L-R source; its 8.5 input is a fixed seeded sample of
  generated instances (2,000 per generator) written before the stage, run once per stage, no re-run.
- GEN-B4 Point 4: no names exemption for TP rows in C2.1. If fewer than 8 RG tasks are admissible, G-T3 fails and TP-RG rolls
  alone (sub-block independence); its rows return to the original sub-blocks within +25% of their targets.
- GEN-B5 Points 5, 6 confirmed (pooled L4 read on the pilot as in every family; the gap rule may be tightened before the look,
  never loosened). Point 7 is L-0's.
- GEN-B6 The RG allow-list, DM module list and bAbI task list are names-only additions due by Fri 23 12:00 (manifest v1.2).

### VOICE addendum: REVISE -> APPROVED after fix

Must-fix (applied): VOICE-M1 the dictionary licence list said "CC", which admits CC BY-NC and CC BY-ND. Now: MIT / Apache /
BSD / CC0 / CC BY / CC BY-SA only; any NC or ND term, GPL / LGPL or unknown = not used (section 1 and V-C11).
Binding conditions: VOICE-B1 Point 1 confirmed: ctx_recoverable_enabled = False in C2.1 (round-1 C1 "OFF by default").
VOICE-B2 Point 2 confirmed: the L4 bar is a report line for VOICE (band shares are fixed by the plan). VOICE-B3 Points 3, 4, 5
confirmed (A 50 / B 30 / C 20; no L-R row as a source; C off -> A 55 / B 45). VOICE-B4 The section 2 mix-entry rule supersedes
the round-1 "stay OUT until R11" sentence (A79 R11 answered). VOICE-B5 Voice stays <= 8% of new rows.

## Flags for the orchestrator (no ruling here)

1. T50 O-A5 option 2 (block G may fall back alone to the v3.1 block table) is a plan change; Option 1 binds until you rule.
2. T41c N (2,000 or 3,000) from T41's C2 status, before the Thu 22 hash export.
3. tools_s5.md item 8 still holds the withdrawn LIMBO sentence (L-0 file).
4. The G0-lites for T59, T60, T63, T66, T67 (and T62, T65 by Fri 23) are not written yet; manifest v1.1 lists their family ids
   only (plan Sk 24); their names arrive in v1.2.
5. Batch 2 (separate fresh session, plan 16.7): A61(d), A82 1 strict reading, HotpotQA 8.5, Gandalf selection-rule record,
   rule-3 / A46 note.

## Names manifest v1.1

Built by this session from v1 plus every new name in the approved files above (names only): l0/NAMES_MANIFEST_V1_1.json,
frozen true, frozen 2026-10-18T07:33:17Z, file sha256 1567ee8a66c100228c9d833879d4c1caa1c7744402574f64d511204a44866593 (in
l0/NAMES_MANIFEST_V1_1.sha256), names_block_sha256 0dacaa39024174a0ab0775bdf1c7cb6ba4c70e55447989bce17d2a740c8940ea. It supersedes
v1 (file sha 04732bdb..., unchanged on disk). Every v1 name is kept; nothing removed or renamed.
- Guard names added: 35 (policy 7, tool 16, language 0, runner 4, carrier 8); union 287 -> 322.
- Row-job families added: 16 (T57r, T59, T60, T63, T66, T67, LR-safety, LR-intent, LR-dialogue, LR-nli, LR-reading, LR-tables,
  LR-reasoning, LR-lowrel, LR-tasksource, LR-code); 12 -> 28. Listing a family does not start it (no approved G0-lite = no
  conformance record = refused). T62, T65 are v1.2.
- Non-guard name records: 59 L-R dataset records, 11 waiting-set names, 21 excluded names, 13 A61(a) barred names (6 new vs v1:
  md_worldbank, md_usgs, md_cma and the three DI-TS member sources), 18 R5 close-sibling names, 3 GEN external generators, 12
  namespace slot kinds, 32 fixed real path stems, plus lane metadata ids (shared lever ids, per-family ladder / head / pool ids).
- Not added on purpose: T53 sink names (withdrawn, T53-M1), runner.go_build (conditional, unused by default), any hand-listed
  real L-R vocabulary (program extraction, v1.2).
- Pending for v1.2 (Fri 23 12:00, names-only copy to L-S the same day): T59 / T60 / T63 / T66 / T67 / T62 / T65 names, the L-R
  real-name vocabulary, the GEN RG / DM / bAbI lists, promoted tasksource sources.
Hand-off: L-0b repins row_start_guard to v1.1 and adds the family-field check and the L-R / P1-realism scoped exemption with CPU
tests; the orchestrator sends the names-only v1.1 copy to the sealed side (this session wrote nothing on the sealed side).

## Batch 1b: the seven new G0-lites (Opus 5.5 high; Sun 18 Oct 2026 UTC)

Read for this batch: families/T59, T60, T63, T66, T67, T62, T65 G0_LITE.md (whole files), this file (GV1-GV9 and the
batch-1 rulings), families/G0_APPROVALS.md (G1-G10, round 1 and 2), training_inputs/PLAN_TRAINING_SIDE.md (incl. section
16), LANE_L-K.md, LANE_L-P.md, families/LR/G0_LITE.md (rows LR-03..LR-12, LR-19, R13, R14, OQ-R3), T50 G0_LITE.md (rule
table R09-R21, SLT-1, K21) and G0_ADDENDUM_v32.md (block G, K21 leg (e)), T55 G0_LITE.md (label sets B1-B6), T51
G0_LITE.md (violation_set line), l0/NAMES_MANIFEST_V1_1.json. NOT opened: any path containing "ohs" or "sealed" (the one
sealed-side file below was WRITTEN, nothing there was read), C2_1_PLAN_v3.md, any skeptic file, any generator, wording
pool, mutate.py, dataset file or benchmark item text, ~/.claude. No rows, no model or API call, no Modal, no training.

### Verdict table (Batch 1b)

| File | Lane | Verdict | Must-fix (applied in the file, marked "[Opus b1b ...]") | Binding conditions |
|---|---|---|---|---|
| T59/G0_LITE.md | L-K | REVISE -> APPROVED after fixes | 3 (T59-M1 K24 widened (GV13); M2 create undoable only if not external; M3 R-SAME explicit) | T59-B1 to T59-B12 |
| T60/G0_LITE.md | L-K | REVISE -> APPROVED after fixes | 2 (T60-M1 leg (c) ALLOW on every W-REPO step (GV13); M2 two-way round trip incl. order statements (GV12)) | T60-B1 to T60-B11 |
| T63/G0_LITE.md | L-P | REVISE -> APPROVED after fixes | 5 (M1 T8 clause; M2 MAL = L-R dataset gate (GV11); M3 MAL learnability precondition; M4 LIC purity bar replaced; M5 MAL 500 + 500 if built) | T63-B1 to T63-B9 |
| T66/G0_LITE.md | L-P | REVISE -> APPROVED after fixes | 2 (M1 MSG-REAL gates = L-R dataset gates (GV11); M2 repo hold-out and "train part seen") | T66-B1 to T66-B9 |
| T67/G0_LITE.md | L-P | REVISE -> APPROVED after fixes | 5 (M1 O-T67-1: M02 card-gated, dev and shared only; M2 X03 conforms to SLT-1; M3 full-engine G9 legs + leg (b'); M4 X04 visible data_class, no new T53 channel; M5 S12-S14 are M01 forms) | T67-B1 to T67-B10 |
| T62/G0_LITE.md | L-P wave C | REVISE -> APPROVED after fix | 1 (M1 300-row slice floor deleted) | T62-B1 to T62-B8 |
| T65/G0_LITE.md | L-P wave C | REVISE -> APPROVED after fixes | 2 (M1 JUL-CWE is an L-R question form, not a G7 head; M2 Juliet scrub over every token class) | T65-B1 to T65-B7 |

Meaning as in batch 1: every must-fix is design text, applied in place by this session; no further round is needed.
Each file carries an appended block "Opus batch-1b rulings v3.2"; the build skeptic refuses a code review without it.
CODE may start in L-K and L-P now (builder launch still only under the measured burn projection, Sk 21). ROWS start only
after the OHS-5 freeze, the registry sha, manifest v1.2 (below), a signed stamp service and a signed conformance record
(Sat 24 18:00 rules unchanged). L-R-fed slices also wait for their source's S-pre PASS and the Opus recast-table batch.

Clean checks every file passed: gold is program, execution, an Opus-approved table or the dataset's own label (no LLM sets
or changes a label; G1); solver B is code from a separate session; every PRE-FREEZE gate has a numeric bar; model reads
(C2 <= 70% on L4) are fix triggers, never kills; one combined fix (G3); check-at-creation through the L-0b stamp wrapper
with GV5 group retirement; G6 / GV4 token rule; GV2 held-out wrappers and GV6 perturbation ids where A10 / A12 are
carried (L-K only; L-P carries no A10-A16, GV7); no NC / GPL / AGPL component (git is not invoked; MPL-2.0 only under the
T42c-B3 offline-tool rule); held-out material never trained; real names only under the scoped P1-realism exemption.
Read-scope note: the T59 and T60 authors record one search over C2_1_BUILD_ORDER.md and sibling LANE files outside their
read list; it is training-side text and nothing sealed was touched; no action.

### Global rulings added in Batch 1b (GV10-GV13; bind every lane; cited by number)

GV10 PILOT SIZE FOR FAMILIES UNDER 2,000 GENERATED ROWS (answers O-T63-6, O-T66-5, O-T67-7, O-T65-5). The first-look pilot
is a seeded proportional sample of 50% of the family's GENERATED trained-row target, floor 300, cap 1,000 (T63 600, T66
400, T67 500, T65 300; T59 and T60 keep 1,000). The post-fix re-read uses a fresh sample of the same size with new seeds.
Pilot rows enter the built family only if no fix follows; after a fix they are discarded (counted) and the family is
built with the fixed parameters. L-R-fed slices have no pilot: set-level checks run once per built dataset slice (16.3
rule 6).

GV11 P1-REALISM SLICES ARE L-R DATASETS FOR KEEP / LEAVE-OUT (answers O-T63-3, O-T62-2, O-T65-2 and the T66 kill text). The
DataDog (T63 MAL), CommitPackFT (T66 MSG-REAL), LogChunks and FlakeFlagger (T62) and Juliet (T65) slices are judged by
L-R dataset rules (16.3 rules 1-6, Sk 23a, LR R13 / R14, one set-level correction per LR-B8): failing them leaves THAT
dataset out (logged with numbers) and never rolls the host family; the host family's gates are read WITHOUT the slice,
so a slice cannot make the host pass or fail. Reverse: if the host family is killed, its slices go with it (they are
counted in it and their negatives, pairs or question forms are host designs), except T62, which has no generated part
and is out only if every slice is out. G4 is not loosened: it binds generated heads and sub-blocks; the dataset rule is a
plan rule (precedents T57-B1 "never against T57", LR-M7). Gate tables mark such gates "L-R dataset gate (leave-out)".

GV12 SLOT ROUND TRIP IS TWO-WAY (gap found in this batch; stricter only; binds every lane that lets Haiku reword text).
After rewording, (a) every decision-bearing span of the spec survives verbatim AND (b) no decision-bearing span is ADDED
(a value, count, negation, qualifier, delegation line, order statement, consent naming, operation or target name, or a
word of the family's closed cue lexicon), checked by solver B's parse plus a closed-lexicon scan; failure is drop-only.
Reason: a one-way check lets a rewording add "first ... then", "either is fine" or a target name and change the gold
while the spec, and so solver A, stay unchanged. Lanes approved in batch 1 add the (b) check to their existing round
trip before the Thu 22 hash export (no other change).

GV13 SAME-ACTION CONFORMANCE (G9 extension; T50-B2 generalised). Where a new family's row shows an action or a change that
a P0 gate family (T50, T51, T53) also labels, the new family's label must equal the P0 engine's label on the same visible
action and state under a card with the same slots, unless a VISIBLE card clause that the P0 cards never carry makes the
difference (T54-B1 precedent). Every G9 leg runs the new family's FULL engine (every rule), never a chosen subset, and a
disagreement is a defect of the new family. Applied: T59-M1, T60-M1, T67-M1 to M4.

### Per-file notes (rulings in full in each file's "Opus batch-1b rulings v3.2" block)

- T59: O-K1 to O-K10 confirmed (B1-B10); the L-R dialogue recast does not reuse T59's question form, defs card or pools
  (B8). D3 as amended is the shared IRREV text for T60.
- T60: O-L1 to O-L9 confirmed (H3 conjunction kept; order statements carry AUTHORITY); quad edits limited to four markers
  (B10).
- T63: MAL is built only if the measured LR-04 field record shows a visible label-bearing field outside the payloads
  (expected NOT to hold: then the slice is left out, logged, C2.2 item with real benign negatives from a licensed
  registry index). The licence table and its hash are a separate fresh Opus session's job, before any LIC row.
- T66: 3-run witnesses, pilot 400, MSG-REAL pair accounting 1 YES + 1 NO per commit (B7).
- T67: lock layer only under `clause.t67.lock_review`, dev and shared only; production and clause-OFF cards follow T50
  R10 / R11 verbatim; X03 tightens the contained lane only; the lock table is a separate fresh Opus session's job (S1-S11,
  S15 only). Real IaC / CI / SQL vocabulary is a closed family list in the Thu 22 hash export (not a guard category).
- T62: no slice floor; 3 FlakeFlagger projects held out; program PII-scrub drop rule (B7).
- T65: keep 600 generated rows; static-only classes accepted; Juliet languages as a scoped non-guard list; canary
  conditions (B6).

### Flags for the orchestrator (no ruling here)

1. GV12 asks the batch-1 lanes (L-A, L-I, L-T, L-C, L-G) to add the "nothing added" half of the round trip before the Thu
   22 hash export; please relay.
2. Two Opus tables are now on the critical path and must be written by SEPARATE fresh Opus sessions: T63-LIC-TABLE
   (before any LIC row) and T67-LOCK-TABLE (before any MIGRATION row).
3. Manifest v1.2 is frozen NOW on your instruction, but plan Sk 19 made v1.2 ("at most") the Fri 23 12:00 manifest that
   should also carry PROGRAM-extracted vocabularies that do not exist yet: L-R / P1-realism real names (after S-pre
   PASS), GEN RG / DM / bAbI lists (GEN-B6), promoted tasksource sources, the T63 stdlib export and DataDog vocabulary,
   T65 sink / sanitiser API names, T67 fixed IaC / CI / SQL vocabulary. They are not guard categories, but their
   names-only record to L-S needs a version after v1.2. Either rule a v1.3 (same Fri 23 12:00 deadline, plan wording
   change) or rule them out of C2.1; this batch does neither.
4. T63 MAL is likely to be left out under T63-M3 (the DataDog files are expected to carry no signal field outside the
   payloads); the money projection should not count its 1,000 rows until the LR-04 field record decides.
5. During this session a Claude Code safety check REFUSED one shell removal (an `rm` of files in a scratch folder this
   session had made; nothing was deleted). Nothing in this batch depended on it; no removal was retried.

### Names manifest v1.2

Built BY PROGRAM from v1.1 plus the names of the seven approved files (names only): l0/NAMES_MANIFEST_V1_2.json, frozen
true, frozen 2026-10-18T08:30:53Z, file sha256 887670015f483dfe1ae9ecfae935eec0a98c76d6b3633adef9f214d92c3d03c5 (in
l0/NAMES_MANIFEST_V1_2.sha256), names_block_sha256 278368ed279c27015ac93cc9d4b4c366a07230b26c327fe44b2df390e390a509. It
supersedes v1.1 (file sha 1567ee8a..., unchanged on disk). Every v1.1 name is kept; nothing removed or renamed. Program
asserts: names = union of per_family_names; no duplicate inside or across the five guard categories; every reused name
already in v1.1; additions exactly the expected set.
- Guard names added: 79 (policy 41, tool 0, language 0, runner 6, carrier 32); union 322 -> 401 (policy 90, tool 160,
  language 10, runner 27, carrier 114). per_family_names 13 -> 20 families.
- row_job_families_allowed 28 -> 30 (T62, T65 added).
- Non-guard records added (v1_2_additions): family metadata ids for the seven families, clause ids, card slot names,
  fixed_real_licence_ids (T63 SPDX set, T66 CommitPackFT spellings), p1_realism_language_labels (c, cpp, java, csharp;
  scoped), tool-only dependencies (Checkov, squawk, tree-sitter JS/TS, Python ast, Go go/parser), G13 target names
  requested for the L-0b registry. No new R5 candidate name (all five P1-realism sources were already v1.1 records).
- Names-only copy for the sealed side written to ohs5_sealed/inputs/TRAINING_NAMES_V1_2.json (the five guard categories,
  general domains, R5 candidate dataset names; header carries version, freeze time and source shas only): file sha256
  0ebe6fbef882f8a14e4b1cc844050da5bd95a9fec6d540ed167f9751771e259c, content sha256
  eddcd15cbd22c507fa07755b75036c691c487fef9a3e1b562e3f9ca23b8e6124. Nothing under ohs5_sealed was read.
Hand-off: L-0b repins row_start_guard to v1.2 (file sha above) with its CPU tests (family field incl. T62 / T65; P1-realism
scope incl. T62 / T65 realism rows).

- [2026-10-18 19:59 UTC] Opus Q7b (T63 K10 amendment, pre-pilot): K10 format-only probe -> K10-F construction assert (PRE-FREEZE KILL 100%);
  probe report-only. Source RULINGS_T59_T60_T63.md "Q7b". Owner to be informed in the C2.1 report.
- [2026-10-18 20:13 UTC] OWNER A102: T60 K21 twin rule scoped to rows whose decisive mechanism is L3-L4 (Opus Q6 follow-up);
  55% design withdrawn, 30% (T60-B9) stands. Disclose in the C2.1 report.
