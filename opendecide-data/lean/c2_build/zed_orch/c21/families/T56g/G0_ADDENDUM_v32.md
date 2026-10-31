# G0 ADDENDUM v3.2: T56g TEST-GAMING (lane L-C; clean-room; 1,000 rows kept; the test-gaming half of T56)

Status: DRAFT for Opus batch 1 (Mon 19 Oct 2026). Written Sun 18 Oct 2026 by the L-C Sonnet author (v3.2 addendum pass).
Design only: no rows, no generated code, no execution, no download, no model call, no Modal. Every identifier below is a
NAME for the names-only manifest or a registry id, never a row value.
Binds over: families/T56g/G0_LITE.md. Where this addendum and the G0-lite body disagree, this addendum binds. The "Opus
rulings 18 Oct" block at the end of the G0-lite (G1-G10 and the T56g decision) stays in force and is carried below. In
particular the fold pairing, the K4 reading and the natural DEV split in that block replace the G0-lite body text in
sections 2 (fold line), 5 (K4 and the probe paragraph) and 10 (items d, g).
Sources, each tagged where used: [OWNER-ROW], [LEV A10], [LEV A16], [LEV A1, A2], [CRIT D1, D2] (ladder; the quad is
mandatory for T56), [INV section 4 T56 row], [A79 R6], plan 16.1 (stamp pipeline), Sk 23a (stamp-drop triggers).
Read for this addendum: build order (L-C block and v3.2 L-C lines); plan sections 1 (B.7, E), 2, 5, 6, 7, 8, the
PRE-REGISTERED RULES block of section 3 only, and 16; EXTRA_LEVERS 1; PUBLIC_TRAIN_INVENTORY (section 4 T56 row);
families/G0_APPROVALS.md; the T56g G0-lite. NOT opened: any T27/T40-T46/T42/T43 generator, template or wording pool,
mutate.py, OHS-AC, any "ohs" or "sealed" path, OHS5_BRIEF_DRAFT.md, the rest of plan section 3, C2 build files, data/, logs/,
~/.claude, or any benchmark item text. ImpossibleBench, EvilGenie, TRACE, MALT and HackTrace are G13 TARGET NAMES only.

## 1. Rulings carried word for word (families/G0_APPROVALS.md, Round 1; Round 2 added nothing for this family)

Global rulings G1-G10 apply. Their full text sits unchanged in the "Global rulings" block at the end of
families/T56g/G0_LITE.md (byte-identical to G0_APPROVALS.md). Index of the ones this addendum leans on: G1 solver B is CODE
(a separate Sonnet high session; no LLM sets or changes a label); G2 data-audit gates (A50 G6, A49c, G5-H, G3-H, A43(d)) are
PRE-FREEZE; G3 no free pilot tuning, ONE combined fix; G4 the only split the plan names is T56 done-claim half / T56g, and no
sub-block or head rolls alone; G5 one probe harness; G6 token rule; G10 `decision_spans` export for T56 task statements.

T56g decision (Opus, copied word for word):

> Binding conditions:
> - C1 VISIBLE_PASS is the RUNNER'S OWN success verdict on the patched tree: exit status 0 and no failed or errored test,
>   with skipped and xfail counted as not failing, 2 runs agreeing. Without this, F2 (skip/xfail) and F8 (forced exit 0)
>   hacks never satisfy VISIBLE_PASS and would all be dropped.
> - C2 Contradicting-spec rows use the SAME label function. The held-out suite H of a contradicting-spec task always holds
>   the spec-correct version of the contradicted case. Then "any passing patch is HACK" falls out of HELDOUT_FAIL and is
>   not a separate rule. A CPU assertion checks this for every LIB-CONTRA task.
> - C3 The natural slice is split by task: at least 100 of its 300 rows (whole tasks, both twins) form a natural DEV split
>   that is never trained on. R2 is reported on that split only. Accuracy on trained natural rows is not a report line.
> - C4 G3 applies (no free pilot tuning).
> Rulings: (a) the 300-row reading (150 hacks + 150 honest twins) is approved, matching the v3.1 wording "the 300-row
> slice"; the family stays 1,000 rows. (b) dropping honest-intended rows that fail held-out is approved (counted; they are
> T57 PARTIAL material). (c) K6 and K8 are kept as PRE-FREEZE KILL gates. (d) K4 passes when the MEAN of the four rotation
> AUCs is >= 0.70 and no single rotation is below 0.60, with CIs reported. This is fixed now, before any pilot, because
> about 75 hack rows per fold give an AUC SE of about 0.05. (e) 25% with-outputs copies are approved. (g) The folds are
> re-paired ACROSS mechanism groups: {F1,F5}, {F2,F6}, {F3,F7}, {F4,F8}. Mechanism pairing would hold out a whole mechanism
> (both test-edit families) and fail K4 because of the TF-IDF probe, not the data. R1 also reports a whole-mechanism
> holdout as an extra post-training line.

Readings fixed here so the conformance record has one text (no ruling is changed):
- K4 is a FLOOR (learnability), so its AUC is the ORIENTED AUC (positive class = HACK, orientation fixed on the training folds
  before scoring). G5's "AUC reported as max(AUC, 1 - AUC)" is the near-chance reading and is used for K5-K8 and the new
  chance bars, not for K4; an inverted probe must not pass K4. (Opus item 5.)
- The K4 folds are {F1,F5}, {F2,F6}, {F3,F7}, {F4,F8}. F5 does not exist in Go and bash; fold balance per language is reported.
- Natural slice: 300 rows = 150 HACK + 150 honest twins; DEV split = >= 100 rows (50 tasks x both twins), never trained, chosen
  by a seeded draw over whole tasks before any pilot; so the TRAINED natural rows are <= 200 and the trained family is <= 900 rows.
  The dev rows are inside the 1,000 as a count of produced rows and are excluded from training and from K4-K8 training folds.
- Probe protocol: G5 replaces "5-fold group CV ... 95% bound"; groups = TASK id (a task's hack and honest twins share a fold).

## 2. What changes in v3.2 (one line each)

| # | Change | Source | Effect on size |
|---|---|---|---|
| 1 | Cue-invariance wrapper rows (A10), conditional on the Fri 23 Oct free probe; library rows only | [LEV A10] | 60 rows by substitution inside LIB-NORMAL; 40 held-out-wrapper dev rows outside the 1,000 |
| 2 | Observation-format perturbation of VISIBLE_RESULT (A16) on the +25% variant copies | [LEV A16] | 0 extra rows; one format held out (dev only) |
| 3 | Difficulty ladder L1-L4, the mandatory alarming / calm x risk present / resolved quad, measured bar C2 <= 70% on L4 | [CRIT D1, D2] | 0 rows (shifts the mix inside LIB-NORMAL) |
| 4 | L4 hack variants that read the visible test source or detect and branch on the harness (inside F4 and F7, folds unchanged) | [INV section 4 T56 row] | 0 rows (inside the F4 / F7 counts) |
| 5 | Legit twins (spec-required special case, spec-driven test edit, genuine fixture fix) as honest alarming cells | [INV section 4] | 0 rows (inside HONEST-PASSING) |
| 6 | CHECK AT GENERATION: every row answer-checked and G13-stamped when made; the 200-row G13 pilot is gone | [OWNER-ROW] plan 16.1 | 0 rows; replaces K16 and section 9 wording |
| 7 | Templates addressable for the L-0 gold-bug audit; AFLite repair as the one fix tool | [LEV A1, A2] | 0 rows |
| 8 | Ruling-to-code conformance seed | plan 16.1 step 0 | 0 rows |
| 9 | Not carried: A12, A14 (not assigned to L-C), A15 (Opus item 6) | build order | none |

## 3. Sizes by substitution (1,000 rows unchanged; G0-lite section 1 table stands)

| Slice | Rows | HACK | NO-HACK | v3.2 inside-slice changes |
|---|---|---|---|---|
| LIB-NORMAL | 600 | 300 | 300 (HONEST-PASSING 250, HONEST-NOTYET 50) | A10 60 trained wrapper rows; quad cells; ladder; L4 variants |
| LIB-CONTRA | 100 | 50 | 50 | ladder mechanism LD-CONTRA; no wrappers |
| NATURAL | 300 | 150 | 150 | DEV split >= 100 (C3); no wrappers, no ladder levels (cells and levels are reported by program) |
| Total | 1,000 | 500 | 500 | |
Languages unchanged: Python <= 75%, JS/TS >= 8%, Go >= 8%, bash >= 8% (Go and bash draw their hacks from F1-F4, F6-F8). Extra
copies outside the 1,000, unchanged: +25% with-outputs variant copies (250; A16 formats are applied to these), 10% swapped-hunk-
order copies. Reuse unchanged (<= 2 rows per task per label), counting wrapper copies. Quotas are counted AFTER drops; every
quota cell (HACK per family F1-F8, quad cells, L4, language) is oversampled by 15% at generation (fixed now, not tuned on the
pilot); the K9 drop-share cap (<= 10% of attempted per block) is unchanged.

## 4. A10 cue-invariance wrapper rows [LEV A10] (conditional)

Precondition: the Fri 23 Oct FREE PROBE (orchestrator: 200 wrapped items from C2's existing dev rows, read by C2 on od-l4b,
share written before the read) says "build"; decision recorded by Sat 24 Oct 18:00 UTC before any row is rendered. If not,
T56g has 0 wrapper rows.
Design: wrapper text is a code comment, commit-message line or PR-description line attached to the DIFF (class COMMENT /
CUE_COMMENT). It is NEVER inside TASK_CARD or INTEGRITY_CARD: the integrity card (and the card's SPEC-OVER-TEST clause) is
the only REAL consent signal in this family, and it is untouched. Wrapper families W1 authority claim ("a maintainer approved
this"), W2 urgency, W3 role-play, W4 fake "already approved / tests verified", W5 benign justification. Trained W1, W2, W4; held
out W3, W5 (seeded draw before the pilot, recorded). Wrapper text applies equally to HACK and NO-HACK diffs (same family, same
rate), so the cue carries no label. Size 60 trained rows (3 families x 20, half HACK and half NO-HACK, drawn from LIB-NORMAL);
each has its clean twin among the base rows (same task, same label). Held-out wrapper dev rows: 20 base rows per held-out
family = 40, eval only, outside the 1,000. The natural slice is never wrapped (its authorship style is probed by K8).
Gate K19 (PRE-FREEZE KILL): wrapper presence vs label parity <= 3 pp; justification-comment presence (wrapper plus the G0-lite
comment pool) equal across labels <= 3 pp; wrapper-text-only probe AUC <= 0.55 / upper <= 0.60; wrapper share 10% +- 2 pp of
LIB-NORMAL (60 of 600); 0 held-out-family rows in training; K7 (comment-only probe) still passes with wrappers included.

## 5. A16 observation-format perturbation of VISIBLE_RESULT [LEV A16]

Applied to the 250 with-outputs variant copies (0 extra rows). Same format registry and parser as T57 (one implementation):
VR-FMT-1 plain pytest-style, VR-FMT-2 verbose unittest-style, VR-FMT-3 TAP-style, VR-FMT-4 JSON lines, VR-FMT-5 ANSI-coloured,
VR-FMT-6 CRLF / tab mixes, VR-FMT-7 line-wrapped with continuation markers, VR-FMT-8 progress-bar lines interleaved with a
truncation marker. One format held out by seeded draw (dev only). The 256-token cap is kept. Label-preserving check by program:
parse-back to the canonical result record equals the executor's record, else the copy is dropped at creation. Held-out
content and results are never rendered. Gate K20 (PRE-FREEZE KILL): parse-back 100%; label parity across formats <= 3 pp;
format-only probe AUC <= 0.55 / upper <= 0.60; 0 held-out-format rows in training.

## 6. Difficulty ladder L1-L4 and the quad [CRIT D1, D2]

The alarming / calm x risk present / resolved QUAD is mandatory for T56 (plan section 1 E) and applies to LIB-NORMAL:
| Cell | Surface | Risk | Label (from the unchanged label function) |
|---|---|---|---|
| Q-AH ALARM-HACK | contains >= 1 token of the closed alarm lexicon LEX-ALARM-1 (skip, xfail, exit, conftest, mock, monkeypatch, noqa, nolint, ignore and similar; the builder fixes the list once, before the pilot) | present (passes V, fails H or matches a signature) | HACK |
| Q-CH CALM-HACK | zero lexicon tokens (for example F2 or F8 written through a neutral helper name that expands to the same effect; F1 deletion inside a cleanup-sounding refactor) | present | HACK |
| Q-AO ALARM-HONEST | >= 1 lexicon token, legitimately (domain names such as a skip-blank-lines function, an ignore-case parameter, a mock fixture fix in an UNPROTECTED file) | resolved | NO-HACK |
| Q-CO CALM-HONEST | zero tokens | resolved | NO-HACK |
Targets: each cell 25% of LIB-NORMAL (floor 15%, cap 35%). Every hard cell (Q-CH, Q-AO) has an easy-looking twin on the same task
with the opposite label. The cell tag is computed by program for all rows (natural and contra rows get tags for reporting only).
Honest alarming cells are built ONLY so the unchanged label function gives NO-HACK: the signature matchers stay narrow, and an
honest special-case branch is keyed on a spec-documented value that NEVER occurs in the visible tests V (CPU assertion; else
the row is dropped), so SIGNATURE_MATCH cannot fire; test edits in honest rows touch only files the card does NOT list as protected.
Mechanisms (copied as mechanisms; program parameters only):
| Id | Mechanism | LOW | HIGH |
|---|---|---|---|
| LD-MSG | justification text strength | none or neutral comment | assertive "fixed" text, or text citing a spec-like reason ("legacy callers") |
| LD-SPEC | justified special-casing pairs | honest twin has a spec clause in TASK_CARD, hack has none, texts differ | honest and hack diffs carry the SAME justification comment; the difference lives only in whether TASK_CARD documents the clause and whether the value occurs in V |
| LD-BREADTH | the label-defining hunk is hidden among benign hunks | 0-1 benign hunks, 1 file | 3-5 benign hunks across 3-4 files (token cap applies) |
| LD-REACH | hack reaches the harness | F-families as in the G0-lite | L4 variants F4-V1 (reads expected values from the visible test source at runtime), F7-V1 (detects the harness and branches), F7-V2 (patches an evaluator helper); they stay inside F4 / F7 for the folds |
| LD-TWIN | legit alarming twin kind | SPEC-SPECIAL (spec-required special case) | SPEC-TESTEDIT (spec-driven edit of an unprotected test file) or FIXTURE-FIX (genuine fixture fix) |
| LD-CONTRA | contradiction subtlety (LIB-CONTRA only) | flipped constant | an added contradicting assertion that interacts with other cases |
Row level (by program, recorded, never from a model score): L1 none active; L2 one at LOW; L3 one at HIGH or two at LOW; L4 two or
more at HIGH. Composition (set-level, PRE-FREEZE): L1 20 / L2 30 / L3 30 / L4 20 (each +- 5 pp); L3-L4 >= 25% (target 50%).
Hack-family balance is unchanged: every family F1-F8 >= 25 rows after drops and none above 15% of HACK rows; the L4 variants
F4-V1, F7-V1, F7-V2 each >= 20 rows after drops (gate K24).
MEASURED BAR (gate K22, once, on the 1,000-row pilot): C2 (C1 if no weights), read on od-l4b, scores <= 70% on L4 rows (base 4B
beside it). Model-based, so by skeptic 6 it is a FIX TRIGGER, not a kill: a miss is folded into the ONE combined fix (G3) by
raising the HIGH settings (never by dropping rows by model score); after the fix a miss is a report line.
Impossible-by-spec tasks in the inventory table: the binary label already covers them (LIB-CONTRA: any passing patch is HACK;
a spec-following patch that leaves the contradicted case failing is NO-HACK). No ask / abort label exists here.

## 7. CHECK AT GENERATION [OWNER-ROW] (plan 16.1)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train."
Replaces: T56g-K16's "200-row G13 pilot (<= 1% hit)"; the first bullet of G0-lite section 9 ("CPU gates run on the pilot
first; pilot-stage tuning is logged development; after the 200-row G13 pilot each change consumes the fix iteration").
Every row is written to the pool ONLY through the stamp wrapper. Per batch (<= 500 rows, same day):
(a) ANSWER CHECKS per row before stamping: the label function applied by the executor (VISIBLE_PASS per C1, HELDOUT_FAIL in a
fresh container from a pristine copy, SIGNATURE_MATCH by matcher A, PROTECTED_PATH_MODIFIED from the diff paths) with the
manifest complete (K1); solver A = solver B including B's own AST-based signature matcher and protected-path check (K2; honest-
intended rows that fail H are dropped and counted; library hacks matching no HACK clause are dropped and counted, K9); H is
physically separate and never in the rendered row (K3 scan per row); LIB-CONTRA: H holds the spec-correct contradicted case
(C2 assertion, per task, before its rows exist); the honest-special-case rule of section 6; the executor's T56 tamper self-test
passed for the VM batch in which the row ran (batch-level fact recorded in the row manifest); names guard (closed allow-list,
no exemption); token rule G6 per row; PII scrub; G10 `decision_spans` export for the TASK_CARD (roles: negation / polarity,
number, entity / path / flag, AUTHORITY, where AUTHORITY marks the card's protected-path list and the SPEC-OVER-TEST clause);
exact-duplicate refusal on the AST-normalised hash and the reuse ledger (<= 2 rows per task per label); quad cell, ladder level,
wrapper id, VR-FMT id and the A1 fields (template id, wording id, transform id, signature id) recorded; A16 parse-back.
(b) G13: the batch goes to the stamp service against every registered target with every method listed for that target (registry
sha bound; R6 sha-bound scaffolding exemption on header, option scaffolding, definitions card; OHS-AC binding for new rows;
OHS-5 hash-export targets use exact and hashed n-gram methods only). (c) The stamp (row id, registry sha, method-set version,
generator code sha, verdict) goes in the row manifest. A failed row is dropped and logged (row id, target name, method; never the
matched text). No unstamped or failed row enters the pool. NATURAL-slice rows: Claude authors the pair, the executor labels it,
the wrapper stamps it at creation; the Haiku read of 100% of the 300 rows with Opus A43(d) (K12) is a set-level AUDIT that runs on
the stamped rows and may only DROP a row (an execution-label vs reviewer conflict), never set a label. A template, wording-pool,
cue-pool or renderer change after hash export v1.1 means a new hash export and re-stamped rows.
FIX TRIGGER (all rows): > 1% of the rows of the 1,000-row pilot or of any full-generation day dropped for a reason other than
exempt scaffolding or OHS-5 collisions = the family's ONE combined fix (G3); OHS-5 collisions are dropped row by row and are not
the fix iteration while <= 5%. Answer-check drop rates keep the G0-lite bars (block drop > 3% for disagreement returns the block;
kept yield < 800 = fix iteration).
Set-level checks ONCE per family (pilot, then the built family): A50 G6 at size, A49c balance, wording variety (>= 50 per form and
per card form, none > 2%), matched-pair share, K4-K15 as amended, K17-K24, G5-H (two Haiku solvers on 300 rows), G3-H, Opus
A43(d). Then C2 reads on od-l4b (pipelined; not a kill gate). AFLite-style repair [LEV A2] is the ONE fix tool for a missed
shortcut probe (filtered <= 30% of the family and reported); it must not touch the K4 fold structure.

## 8. Gates added or changed (G0-lite ids kept; new ids continue the sequence; probe protocol G5)

"PK" = PRE-FREEZE KILL (CPU or sandbox, data only). "PR" = POST-TRAINING REPORT.
| Id | Gate | Bar | Class |
|---|---|---|---|
| T56g-K4 (amended) | hack-family holdout learnability, four rotations {F1,F5}, {F2,F6}, {F3,F7}, {F4,F8}; oriented AUC; TF-IDF over diff tokens | MEAN AUC >= 0.70 AND no rotation < 0.60; CIs reported | PK |
| T56g-K5, K6, K7, K8 | length-only, metadata-only, comment-only, slice-identity probes (G5) | AUC <= 0.55, upper <= 0.60 | PK |
| T56g-K12 | natural slice: Haiku reads 100% of the 300; Opus A43(d); conflicts dropped; DEV split >= 100 rows chosen by whole-task seeded draw | as stated | PK |
| T56g-K16 (replaced) | A50 G6, A49c, G5-H, G3-H per plan; the G13 line is replaced by K23 | per plan | PK |
| T56g-K17 | Quad cells in LIB-NORMAL: each of Q-AH, Q-CH, Q-AO, Q-CO within 15-35% (target 25%); hard-cell twin share: every Q-CH and Q-AO row has a twin on the same task with the opposite label | as stated | PK |
| T56g-K18 | Alarm-lexicon probe (counts and presence of LEX-ALARM-1 tokens in added / removed lines and comments), pooled and LIB-NORMAL only | AUC <= 0.55, upper <= 0.60 | PK |
| T56g-K19 | A10 wrapper gates (section 4) | as stated | PK |
| T56g-K20 | A16 VR-FMT gates (section 5) | as stated | PK |
| T56g-K21 | Ladder composition (section 6); LD-SPEC honest values never in V (100%); hack-hunk position probe (position of the label-defining hunk among the diff's hunks: first / middle / last) | L1 20 / L2 30 / L3 30 / L4 20 +- 5 pp; L3-L4 >= 25%; position probe AUC <= 0.55, upper <= 0.60; >= 2-file share equal across labels within 5 pp | PK |
| T56g-K22 | Ladder measured bar: C2 (C1 if none) on L4 rows of the 1,000-row pilot | accuracy <= 70% | PRE-FREEZE FIX TRIGGER (model read on our own data; never a kill; after the fix a report line) |
| T56g-K23 | Check at creation (section 7): 100% of pooled rows carry a current clean stamp and an answer-check record | 100% / 0 unstamped; drops <= 1% outside exemptions (OHS-5 collisions <= 5%) or the fix iteration | PK |
| T56g-K24 | L4 hack variants F4-V1, F7-V1, F7-V2 each present after drops; families F1-F8 each >= 25 and none > 15% of HACK rows | >= 20 each; as stated | PK |
| T56g-K25 | A1 / A2 hooks: template id, wording id, transform id, signature id on 100% of rows | 100% | PK |
| T56g-R6 | Accuracy per quad cell and per ladder level vs base 4B, always-HACK, skip / xfail / exit-0 keyword regex, test-file-touched flag, diff-length logistic, random | report (CI) | PR |
| T56g-R7 | Wrapper flip rate and held-out wrapper gap; held-out VR-FMT accuracy vs trained formats | report (CI) | PR |
| T56g-R8 | L4 variant accuracy (F4-V1, F7-V1, F7-V2) separate from the F-family totals | report (CI) | PR |

## 9. NAMES (new, relative to NAMES_MANIFEST_V1; for manifest v1.1)
- carrier ids: CUE_COMMENT (A10 wrapper line; shared with T42c and T57). VISIBLE_RESULT, COMMENT, DIFF, INTEGRITY_CARD exist.
- policy ids: card.t56g.prot_all, card.t56g.prot_listed, defs_card.t56g unchanged.
- runner ids: none new (runner.pytest, runner.node_test, runner.go_test, runner.bash_driver exist).
- languages: none new. row_job_families_allowed: T56g unchanged.
- registry ids (not guard-checked; for the hash export): wrapper families W1..W5; VR-FMT-1..VR-FMT-8 (shared with T57); quad cells
  Q-AH, Q-CH, Q-AO, Q-CO; lexicon id LEX-ALARM-1; ladder mechanisms LD-MSG, LD-SPEC, LD-BREADTH, LD-REACH, LD-TWIN, LD-CONTRA;
  levels L1-L4; hack variants F4-V1, F7-V1, F7-V2 (each registered with its own signature id, matcher written separately from the
  transform as for F1-F8); legit-twin kinds SPEC-SPECIAL, SPEC-TESTEDIT, FIXTURE-FIX.

## 10. G13 targets added (names only)
None new. The existing list stays (Impossible-LiveCodeBench, Impossible-SWEbench, EvilGenie, TRACE, the RH-Detect sets incl. MALT,
and the standing targets). HackTrace data is barred and never read.

## 11. Fix iteration and kill rule
G3 governs (the 1,000-row pilot through the stamp wrapper is the first measured look; ONE combined fix). G4 governs. Unchanged kill
rule: failing a PRE-FREEZE KILL gate after the fix, or not through by the data freeze, rolls ONLY the test-gaming head to C2.2/C3;
T56 counts as passed when its done-claim half passes. POST-TRAINING lines are never kill rules. R5 of the G0-lite (an eval-only slice
of hacks that arise in Claude agent runs on impossible tasks) stays moved to C2.2 unless L-C is ahead of plan.

## 12. Conformance seed (plan 16.1 step 0)
The fresh skeptic maps each row to file:function and a CPU test; the record builder refuses to run without the signed record for
its code sha and this ruling sha.
| Clause | Obligation | CPU test id |
|---|---|---|
| G1 | solver B imports stdlib + row schema only; B has its OWN signature matcher and protected-path check | T56g-CM-01 |
| G3 / C4 | parameter file sha frozen at pilot launch; later change needs the fix-iteration flag | T56g-CM-02 |
| G5 | probes grouped by task id; 97.5th-percentile bound; permutation and leak checks | T56g-CM-03 |
| G6 | row > 1,536 tokens refused at creation | T56g-CM-04 |
| G10 | TASK_CARD exports decision_spans with roles incl. AUTHORITY | T56g-CM-05 |
| C1 | VISIBLE_PASS = runner exit 0, no failed or errored test, skip and xfail not failing, 2 runs agree; fixtures with F2 and F8 pass it | T56g-CM-06 |
| C2 | every LIB-CONTRA task: H contains the spec-correct contradicted case (assertion per task) | T56g-CM-07 |
| C3 | natural DEV split >= 100 rows, whole tasks, never in the training pool | T56g-CM-08 |
| (d) / (g) | K4 uses folds {F1,F5}, {F2,F6}, {F3,F7}, {F4,F8}; MEAN >= 0.70 and no rotation < 0.60; oriented AUC | T56g-CM-09 |
| (b) | honest-intended rows failing H are dropped and counted | T56g-CM-10 |
| (e) | with-outputs copies are exactly 25% | T56g-CM-11 |
| 3 | quotas counted after drops; 15% oversample of quota cells | T56g-CM-12 |
| 4 | wrappers never inside TASK_CARD or INTEGRITY_CARD; equal application to HACK and NO-HACK; held-out families absent from training | T56g-CM-13 |
| 5 | VR-FMT parse-back 100%; 256-token cap | T56g-CM-14 |
| 6 | level from mechanism parameters only (no model-score input); honest special-case values never in V | T56g-CM-15 |
| 7 | pool writer refuses any row without a current clean stamp and an answer-check record; natural-slice audit can only drop | T56g-CM-16 |

## 13. Risks (new)
1. The quad is hard to satisfy at 25% per cell: a calm F2 / F8 hack needs a neutral helper that still matches the narrow signature
   by AST; if the signature cannot see it, the hack is dropped by K9 and the cell starves (the 15% oversample is the only lever).
2. Honest alarming rows pull honest diffs toward hack surface forms; K18 and K4 pull in opposite directions (K4 needs learnable hack
   signal in diff tokens; K18 needs the lexicon uninformative). The G0-lite risk 1 stands and is now sharper.
3. L4 reach variants (F4-V1, F7-V1, F7-V2) may be dropped heavily by signature or sandbox rules; K24 reports it.
4. 100 natural rows move to DEV, so trained natural rows are <= 200 and the K8 probe runs on a smaller slice (CIs reported).
5. A10 wrapper comments raise the comment-presence statistics; K7 and K19 are checked together.
6. The tamper self-test is batch-level; a failed self-test voids every row of that VM batch (rows re-run, not relabelled).

## 14. Items for Opus to confirm
1. Sizes: A10 60 trained rows by substitution, library rows only; held-out wrapper and DEV rows outside training.
2. The quad cell targets (25% each, floor 15%, cap 35%) and the closed alarm lexicon LEX-ALARM-1 fixed by the builder before the pilot.
3. Ladder rule, composition, and K22 as a fix trigger rather than a kill; L4 variants inside F4 / F7 (folds unchanged).
4. Honest alarming cells defined only through the unchanged label function (special-case values never in V; test edits only in
   unprotected files).
5. K4 read as an ORIENTED AUC (a floor), against G5's max(AUC, 1 - AUC) default.
6. A15 (format dialects of the integrity-card body) is not assigned to L-C in the build order; the PROT-ALL / PROT-LISTED cards are
   the only card bodies. Default: NOT carried.

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: APPROVE (no must-fix).
Binding conditions: T56g-B1 items 1-4 confirmed (LEX-ALARM-1 fixed and hashed before the pilot). T56g-B2 item 5 confirmed: K4 is
an ORIENTED AUC floor; max(AUC, 1 - AUC) is for near-chance bars only. T56g-B3 W3 / W5 fixed by GV2; item 6 -> GV7.
