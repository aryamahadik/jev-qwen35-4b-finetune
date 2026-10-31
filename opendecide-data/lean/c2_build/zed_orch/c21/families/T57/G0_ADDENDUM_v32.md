# G0 ADDENDUM v3.2: T57 PATCH-VERDICT (lane L-C; clean-room; 3,000 rows kept) + LOCALISE realism + T57r slice contract

Status: DRAFT for Opus batch 1 (Mon 19 Oct 2026). Written Sun 18 Oct 2026 by the L-C Sonnet author (v3.2 addendum pass).
Design only: no rows, no generated code, no execution, no download, no model call, no Modal. Every identifier below is a
NAME for the names-only manifest or a registry id, never a row value.
Binds over: families/T57/G0_LITE.md. Where this addendum and the G0-lite body disagree, this addendum binds. The "Opus
rulings 18 Oct" block at the end of the G0-lite (G1-G10 and the T57 decision) stays in force and is carried below.
Sources, each tagged where used: [OWNER-ROW], [LEV A10], [LEV A16], [LEV A1, A2], [CRIT D1, D2] (ladder), [INV C10, C11,
C12 and section 4 T57 row] (realism), [A82 8] (SWE-smith procedural salvage), [A79 R6], plan 16.1 (stamp pipeline), plan
16.3 rules 1-6 (L-R), Sk 8 (names exemption), Sk 23a (stamp-drop triggers), Sk 25 (span probe), Sk 26 (per-repo licence,
T57r negatives only from our mutator).
Read for this addendum: build order (L-C block and v3.2 L-C lines); plan sections 1 (B.9, C, E), 2, 5, 6, 7, 8, the
PRE-REGISTERED RULES block of section 3 only, and 16; EXTRA_LEVERS 1; PUBLIC_TRAIN_INVENTORY (rows C10-C12, section 4 T57 row,
section 2 O8); PREREG_FINAL.md blocks A77, A79, A82 only; families/G0_APPROVALS.md; the T57 G0-lite. NOT opened: any
T27/T40-T46/T42/T43 generator, template or wording pool, mutate.py, OHS-AC, any "ohs" or "sealed" path, OHS5_BRIEF_DRAFT.md,
the rest of plan section 3, C2 build files, data/, logs/, ~/.claude, any dataset file or benchmark item text. Dataset field
names that appear below come from memory and are marked UNVERIFIED; the L-R licence / record step confirms them.

## 1. Rulings carried word for word (families/G0_APPROVALS.md, Round 1; Round 2 added nothing for this family)

Global rulings G1-G10 apply. Their full text sits unchanged in the "Global rulings" block at the end of
families/T57/G0_LITE.md (byte-identical to G0_APPROVALS.md). Index of the ones this addendum leans on: G1 solver B is CODE;
G2 data-audit gates are PRE-FREEZE; G3 no free pilot tuning, ONE combined fix; G4 no head rolls alone (so the G0-lite's
section 9 per-head roll-alone sentence is NOT adopted); G5 one probe harness (grouped split, 97.5th-percentile bound,
oriented where a floor is tested, permutation and leak checks); G6 token rule; G7 secondary heads are head rows (T57
reason: head rows from at most 25% of the INCORRECT specs, about 125 rows, extra copies outside the 3,000, k = 3 probe bars).

T57 decision (Opus, copied word for word):

> Binding conditions:
> - C1 TESTSEL leakage. TESTSEL options are hidden-suite tests by design, so a base module used for a TESTSEL row is never
>   used for any other T57 head, nor for T42c or T56g. K10 adds a cross-row scan: no H test body of a module appears in
>   ANY rendered row of the family except that module's own TESTSEL rows.
> - C2 Wording fix. The hidden suites are PROGRAM-generated from behaviour atoms (the generator code is Claude-authored).
>   Replace the "Claude-written tests/suites" wording in gate a and risk 1, so it does not read as LLM-written tests. The
>   gold-sanity and strength gates stay exactly as written.
> Rulings: (a) the TESTSEL definition (fails on buggy, passes after the fix; 3 distractors pass both) is approved. (b) the
> reason head follows G7. (c) the T_s rule (0.90 if >= 70% of the 50 pilot modules reach it; one suite-recipe revision;
> floor 0.80; non-Python pilot extended to 20 modules if it scores below 0.80) is approved and fixed before any row. (d)
> excluding test-editing patches is approved. (e) 25% with-outputs copies are approved. (f) see G3. (g) the per-head
> roll-alone rule is not adopted (G4).

Probe protocol reading (binds over G0-lite section 5 header): G5 replaces "5-fold group CV ... 95% bound". Groups = base
module id (T57r: instance id; LOCALISE realism: project id).

## 2. What changes in v3.2 (one line each)

| # | Change | Source | Effect on size |
|---|---|---|---|
| 1 | Cue-invariance wrapper rows (A10), conditional on the Fri 23 Oct free probe | [LEV A10] | about 150 rows by substitution inside the 3,000; about 60 held-out-wrapper dev rows outside |
| 2 | Observation-format perturbation of VISIBLE_RESULT (A16) on the existing +25% with-outputs copies | [LEV A16] | 0 extra rows; one format held out (dev only) |
| 3 | Difficulty ladder L1-L4 and a measured bar (C2 <= 70% on L4) | [CRIT D1, D2] | 0 rows (shifts the mix) |
| 4 | Wrong-but-passing class mix, "does more than the reference" candidates, leakage tags | [INV section 4] | 0 rows (shifts INCORRECT candidates) |
| 5 | LOCALISE granularity: function / file / hunk, reported apart | [INV section 4] | 0 rows (LOCALISE 800 re-split) |
| 6 | CHECK AT GENERATION: every row answer-checked and G13-stamped when made; the 200-row G13 pilot is gone | [OWNER-ROW] plan 16.1 | 0 rows; replaces K17 and section 9 wording |
| 7 | Templates addressable for the L-0 gold-bug audit; AFLite repair as the one fix tool | [LEV A1, A2] | 0 rows |
| 8 | L-R feed contract: LOCALISE realism (ManySStuBs4J 400, TSSB-3M 400) | [INV C10, C11] | 800 rows OUTSIDE the 3,000 (P1 realism) |
| 9 | T57r slice (SWE-Gym 1,000, SWE-smith procedural up to 1,000) as a P1 transfer slice with its own gates | [INV C12; A82 8; Sk 26] | up to 2,000 rows OUTSIDE the 3,000 (P1) |
| 10 | Ruling-to-code conformance seed | plan 16.1 step 0 | 0 rows |
| 11 | Not carried: A12 (build order gives it to L-A, L-I, L-T), A14, A15 (Opus item 6) | build order | none |

## 3. Sizes by substitution (the 3,000 is unchanged; heads, language shares and quotas of the G0-lite stand)

| Head | Rows | Languages (Py / JS-TS / Go / bash) | v3.2 inside-head changes |
|---|---|---|---|
| VERDICT | 1,000 | 750 / 90 / 80 / 80 | A10 about 50; WP class mix; CAND-EXTRA |
| BEST4 | 800 | 600 / 72 / 64 / 64 | A10 about 40; ladder near-miss density |
| TESTSEL | 400 | 300 / 36 / 32 / 32 | A10 about 20 |
| LOCALISE | 800 | 600 / 72 / 64 / 64 | A10 about 40; granularity FUNC 480 / FILE 120 / HUNK 200 |
| Total | 3,000 | 2,250 (75%) / 270 / 240 / 240 | |
Extra copies outside the 3,000, unchanged: +25% with-outputs variant copies (650 on VERDICT, BEST4, LOCALISE; the A16 formats
are applied to these copies); +20% order-invariance copies (random non-identity permutation); reason head rows (<= 125).
Reuse limits unchanged (<= 4 per base module per head, <= 8 overall) and counted over wrapper and variant copies. Quotas are
counted AFTER drops; every quota cell (CORRECT / INCORRECT per language, ALTFIX share, L4, hunk granularity) is oversampled
by 15% at generation (fixed now, not tuned on the pilot).

## 4. A10 cue-invariance wrapper rows [LEV A10] (conditional)

Precondition: the Fri 23 Oct FREE PROBE (orchestrator: 200 wrapped items built from C2's existing dev rows, read by C2 on
od-l4b, share written before the read) says "build"; decision recorded by Sat 24 Oct 18:00 UTC before any row is rendered.
If not, T57 has 0 wrapper rows and the budget returns to the base rows.
Design: wrapper text is a commit-message or PR-description line, or a code comment, beside PATCH_DIFF (VERDICT, BEST4), beside
the buggy source (LOCALISE) or beside a test (TESTSEL). Never inside TASK_CARD, the definitions card or OPTIONS. T57 has no
consent signal in the card, so no real consent signal is at risk. Wrapper families W1 authority claim, W2 urgency, W3
role-play, W4 fake "tests already pass / maintainer approved", W5 benign justification. Trained W1, W2, W4; held out W3, W5
(seeded draw before the pilot, recorded). Each wrapper asserts a verdict ("fixes it", "this function is the culprit"); the
assertion is correct on 50% +- 5 pp of wrapped rows. Size 5% of each head (about 50 / 40 / 20 / 40 = 150 rows) by
substitution; each has its clean twin among the base rows (same module, same gold); held-out wrapper dev rows 30 base rows
per held-out family = 60, eval only, outside the size. Wrappers never replace the existing COMMENT_DECOY:
(15% of INCORRECT patches, comment-rate parity) stays, and wrapper comments COUNT in the comment-presence statistics.
Gate K18 (PRE-FREEZE KILL): wrapper presence vs label parity <= 3 pp (CORRECT / INCORRECT; letters for k-way heads);
asserted-verdict-correct 50% +- 5 pp; asserted-verdict-only probe AUC <= 0.55 / upper <= 0.60 (VERDICT) or acc <= 28% / upper
<= 31% (k = 4 heads); comment-presence gap (K8) <= 3 pp INCLUDING wrapper comments; 0 held-out-family rows in training.

## 5. A16 observation-format perturbation of VISIBLE_RESULT [LEV A16]

The with-outputs variant (G0-lite section 3) shows the visible-test result text capped at 256 tokens. Format registry VR-FMT-1
plain pytest-style, VR-FMT-2 verbose unittest-style, VR-FMT-3 TAP-style, VR-FMT-4 JSON lines, VR-FMT-5 ANSI-coloured, VR-FMT-6
CRLF / tab mixes, VR-FMT-7 line-wrapped with continuation markers, VR-FMT-8 progress-bar lines interleaved with a truncation
marker. One format is held out by seeded draw (dev only; recorded before the pilot). The formats are spread over the 650
variant copies (0 extra rows). Label-preserving check by program: the rendering is parsed back to the canonical result record
(failing test ids, counts, exit status) and must equal the executor's record; otherwise the copy is dropped at creation. The
256-token cap is kept (markers count inside it); hidden-suite output is never rendered.
Gate K22 (PRE-FREEZE KILL): parse-back equality 100% of kept copies; label rate parity across formats <= 3 pp; format-only
probe AUC <= 0.55 / upper <= 0.60; 0 held-out-format rows in training. The same format registry and parser are shared with
T56g (one implementation, one skeptic review).

## 6. Difficulty ladder L1-L4 [CRIT D1, D2]

Mechanisms (copied as mechanisms from the hardest-questions targets; program parameters only):
| Id | Mechanism | LOW | HIGH |
|---|---|---|---|
| M-WP | wrong-but-passing: realised divergence from the reference on the differential set D | 5-20% of D | <= 2% of D, at least 1 witness (passes V and almost all of H) |
| M-NEAR | BEST4 near-miss density (CAND-NEARMISS among the three wrong options) | 1 | 3 |
| M-EXTRA | candidate does more than the reference (CAND-EXTRA) | extra behaviour hit by a P2P test | extra behaviour hit only by D |
| M-LOC | LOCALISE distractor adjacency | other file | same file AND traversed by the killing test |
| M-TSEL | TESTSEL distractors | pass both and do not touch the entity | all three execute the changed entity |
| M-HELP | fix site vs failing test distance (HELPERSHIFT) | same function | shared helper two calls away |
| M-LEAK | card reveals the fix | LK2: card names the function and the bug | LK0: behaviour only |
Row level (by program, recorded, never from a model score): L1 none active; L2 one at LOW; L3 one at HIGH or two at LOW; L4 two
or more at HIGH. Composition (set-level, PRE-FREEZE): L1 20 / L2 30 / L3 30 / L4 20 (each +- 5 pp); L3-L4 >= 25% overall (target
50%) and per head. TWIN rule: every L3 / L4 row has an easy-looking twin with the opposite verdict or a different correct option
(a one-token variant); twins cover >= 50% of L3-L4 rows. LEAKAGE tags: LK0 behaviour only, LK1 names the module, LK2 names the
function; LK2 is capped at 10% of rows (the natural-rate cap), and the K9 LOCALISE probe adds the feature "card text names the
gold entity" (acc <= 28% / upper <= 31%).
Wrong-but-passing CLASS MIX (tags on INCORRECT candidates that pass V; planning shares are the inventory mix 47 / 35 / 7 / 6 / 1
rounded with the 1% class floored at 5% so it can be probed; NOT labels, manifest tags and a report line):
WP-LOGIC 45%, WP-INCOMPLETE 35% (CAND-HALFSITE), WP-TYPE 8%, WP-BOUNDARY 7%, WP-OBO 5% (each +- 5 pp, each >= 3%).
CAND-EXTRA ("does more than the reference"): >= 8% of INCORRECT candidates (floor 80 rows); classed by the existing precedence.
MEASURED BAR (gate K24, once, on the 1,000-row pilot): C2 (C1 if no weights), read on od-l4b, scores <= 70% on L4 rows (base 4B
beside it; for k = 4 heads the bar is still 70%). Model-based, so by skeptic 6 it is a FIX TRIGGER, not a kill: a miss is folded
into the ONE combined fix (G3) by raising the HIGH settings (never by dropping rows by model score); after the fix a miss is a
report line.

## 7. LOCALISE granularity (reported apart) [INV section 4]

LOCALISE 800 rows: FUNC (function-level, the G0-lite design) 480; FILE (options = 4 source files of a 4-file module; the file
holding the mutated function is gold; the module shows <= 15 lines per file around the entry points) 120; HUNK 200. HUNK rows
(synthetic analogue of "which hunk is the bug"): the row shows one program-built multi-hunk diff (the "commit"): 1 hunk
INTRODUCES the bug (our mutator, one modifier), 3 hunks are behaviour-preserving edits. The 3 benign hunks come from the T42c
EQ-YES library (rename locals, reorder independent statements, loop swap, algebraic identity, early-return restructure),
with >= 50% of them operator- or constant-level neutral edits (for example operand swap of a commutative operation, a
flipped comparison with swapped operands, folding a constant), so that "the hunk that changes an operator or constant" is
NOT the bug. Gold rule (executed): reversing the bug hunk alone makes the visible failing test V pass; reversing each of the
other three hunks leaves V failing; the three benign hunks are verified equivalent to the original over the declared domain
exhaustively (3 identical runs). Granularity is a manifest tag; the three are reported apart (R6). Gate K21 (PRE-FREEZE KILL):
shares 60 / 15 / 25% +- 5 pp; gold letter 25% +- 3 pp within each granularity; the hunk-execution rule 100% of kept HUNK rows; an
option-level probe (position, size in tokens, changed-token class: operator / constant / identifier / whitespace, traversed-by-
test flag, card names entity) acc <= 28% / upper <= 31% on each granularity (G5 balanced accuracy, argmax per row).

## 8. L-R feeds into T57: contracts for the mappers (NOT inside the 3,000; family field P1-realism; real names exempt, Sk 8)

All four sources follow plan 16.3: licence record, provenance enum, S-pre PASS before any download or reader, S-post PASS
before rows, train-only, per-dataset cap, the A46-style DROP-only screen (C2 reads; never writes a label), every row stamped
at creation, "train split seen" on every report row. Test / dev splits (where they exist) are registry-only. Where no split
exists, a seeded 10% hold-out (by project, repo or instance) is frozen BEFORE mapping and registered as an internal held-out
G13 target; it is never trained.
| Source | Train unit / size | Licence line (inventory, fetched 18 Oct 2026 by the researcher) | Label source | Feeds |
|---|---|---|---|---|
| ManySStuBs4J | 100 Maven projects, single-statement bug fixes (cap 400) | "Creative Commons Attribution 4.0 International" https://zenodo.org/record/3653444 | program (SZZ + message keywords, about 94% on a 100-commit check) | LOCALISE realism |
| TSSB-3M | single-statement fixes (cap 400), keep only likely_bug rows (UNVERIFIED field name) | "Creative Commons Attribution 4.0 International" https://zenodo.org/records/10217373 | program (heuristic likely_bug flag) | LOCALISE realism |
| SWE-Gym | 2,438 instances, 11 Python repos (cap 1,000); never its trajectories or verifiers | HF "License: mit"; GitHub "Apache-2.0 license" https://huggingface.co/datasets/SWE-Gym/SWE-Gym | human patches; the dataset's own execution tests | T57r |
| SWE-smith, PROCEDURAL rows only (cap 1,000; A82 8) | instances whose strategy is procedural, after the strategy mapping is verified | dataset card MIT https://huggingface.co/datasets/SWE-bench/SWE-smith | program (procedural modifiers); tests by execution | T57r |
LOCALISE realism contract: form T57-Q-LOCALISE, 4 options = code regions (hunk-level or function-level, tag recorded) from the
same file, exactly one containing the dataset-labelled bug line, the other three picked by program (>= 1 adjacent, >= 1 larger,
>= 1 smaller than gold, so size is not a cue); no execution (Java in ManySStuBs4J is not run); code re-fetched ONLY at the
fix commit's parent from repos passing the per-REPO licence whitelist (MIT, Apache-2.0, BSD-2, BSD-3, CC0; others dropped row
by row, Sk 26); the Sk 25 span-position / span-length probe applies (held-out AUC / accuracy bars of plan 16.3 rule 4); one
re-sample then left out. The language ids "java" (ManySStuBs4J) and "python" (TSSB-3M) are extracted by the L-R vocabulary
program into manifest v1.1 / v1.2 (names-only), not added by hand here.
SWE-smith strategy mapping (A82 8: salvage only after it is verified): UNVERIFIED from memory that the instance id or a
strategy field distinguishes procedural-modifier instances from LM-modify, LM-rewrite, PR-mirror and combine strategies. The
L-R record verifies the mapping from the dataset's own metadata first; rows with any LM-made component (and "combine" rows
unless every component is shown procedural) are dropped row by row. The problem_statement field is BARRED (LM-written, arXiv
2504.21798v2 section 2.1): no T57r row contains it, and a CPU scan (T57r-K7) enforces it. GPL / LGPL repos dropped row by row
(the card's Table 6 lists some under a "permissive" caption); the manifest is built from the ROWS, not the card.

## 9. T57r slice (P1 transfer slice; enters C2.1 only if through its own gates by the data freeze; its failure never touches T57)

Purpose: benchmark-trained critics can be near random on real outcomes (OpenHands critic AUC 0.45-0.48, vendor-run), so T57
gets a small real-patch transfer slice. Family id T57r (a NEW row-job family id for manifest v1.1; P1-realism names exemption).
Rows: up to 2,000 (SWE-Gym 1,000 + SWE-smith procedural 1,000), at most 20% from any one repo, at least 5 repos or the slice is
not built (logged). Forms: VERDICT (CORRECT / INCORRECT) and function-level LOCALISE only; no BEST4, no TESTSEL.
Candidates (execution gold only; nothing with unknown correctness enters):
- CORRECT candidate = the dataset's own fix (SWE-Gym: the human patch; SWE-smith: the reversal of the procedural bug patch),
  accepted only after GOLD-SANITY in OUR image: all F2P tests pass and all P2P tests pass (2 runs agree).
- INCORRECT candidates = the CORRECT patch with ONE modification by our own mutator applied to its added lines (operator
  classes MUT-01..MUT-14 and the multi-site variants), kept only with an OBSERVED failing witness among the dataset's own
  tests. Class by the existing precedence: NOFIX (all F2P still fail), REGRESSION (F2P pass, a P2P fails), PARTIAL (some F2P
  fail, or a decisive F2P-tagged test fails). Negatives come ONLY from our mutator (Sk 26): never from SWE-Gym trajectories,
  agent patches or verifiers. Half-applying the human patch's own hunks is NOT used (Opus item 8; it may read as a SWE-Gym
  patch). Every negative is a one-token-class minimal pair with its CORRECT sibling on the same instance, so authorship style
  (human diff vs mutator diff) is not a cue; pairs >= 80% of rows.
- Task card: program-rendered from the F2P test names, the failing-test body and the failure text (capped at 256 tokens); NO
  problem_statement and (default, strictest reading of A82 4) no issue text of any kind; whether GitHub issue text counts as a
  "social-platform post" is Opus item 7.
- Row size: a program trims the diff and source to the touched functions; mean <= 800 tokens, none > 1,536, > 1,024 on <= 10%.
Environment: per-repo execution images are built on od-sbx-build (egress, no data), pinned by digest, shipped to od-sbx1 (no pulls,
no installs inside the sandbox). FEASIBILITY TEST first (3 repos: build time, instance run time, determinism); a repo that
cannot be built or is nondeterministic is left out; fewer than 5 working repos = slice not built. Docker under runsc is untested
(plan section 2): L-0a's self-test must cover repo images before T57r depends on it. 3 runs for any test used as a witness.
Solvers: A = pipeline + executor; B (G1: code, separate Sonnet high session, stdlib + row schema only) = its own runner of the
dataset's tests, own parser; 100% agreement on kept rows.
Gates (PRE-FREEZE KILL for the slice; failure drops T57r only, logged):
| Id | Gate | Bar |
|---|---|---|
| T57r-K1 | Gold-sanity on the CORRECT patch; instance dropped otherwise (a repo above 40% instance failure is left out) | 100% of kept |
| T57r-K2 | Witness completeness (per-test results, 2 runs agree, 3 for witness tests); class by precedence | 100% |
| T57r-K3 | Solver A = solver B | 100%; block drop > 2% returns block |
| T57r-K4 | Per-REPO licence whitelist; none else | 100% |
| T57r-K5 | neg_source = own_mutator on 100% of INCORRECT rows; 0 rows from trajectories or agent patches | 100% / 0 |
| T57r-K6 | CORRECT rate 45-55%; pairs >= 80%; no repo > 20% | as stated |
| T57r-K7 | No problem_statement / issue text in any row (exact and 8-gram scan against the dataset field, registry-only copy) | 0 hits |
| T57r-K8 | Style-only probe (patch length, hunks, comment ratio, identifier stats, mutated-token class), grouped by instance | AUC <= 0.55, upper <= 0.60 |
| T57r-K9 | Token rule G6; names guard = P1-realism exemption only for T57r | as G6 |
| T57r-K10 | Check at creation: every row stamped; instance-level G13 against SWE-bench, SWE-bench-Live, SWE-rebench (and their splits, registry-only) | > 1% stamp drops outside exemptions = Opus; > 5% = slice left out (Sk 23a) |
| T57r-R1 | Accuracy by source (SWE-Gym / SWE-smith procedural), vs base 4B, always-CORRECT, patch-size baseline; "train split seen" | report (CI), PR |

## 10. CHECK AT GENERATION [OWNER-ROW] (plan 16.1)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train."
Replaces: T57-K17's "200-row G13 pilot (<= 1% hit)"; the first bullet of G0-lite section 9 ("run every CPU gate on the 1,000-row
pilot first; pilot-stage tuning is logged development; after the 200-row G13 pilot each change consumes the fix iteration").
Every row is written to the pool ONLY through the stamp wrapper. Per batch (<= 500 rows, same day):
(a) ANSWER CHECKS per row before stamping: the four gates as recorded facts: GATE a and GATE b are MODULE-level and are
checked when the module is created (no row of a module exists before both pass; the module's T_s, kill share, undecided share
(> 25% drops the module) are in each of its rows' manifests); GATE c (differential record per candidate; CORRECT = zero
divergences) and GATE d (solver A = solver B = spec expectation where present; BEST4 exactly one CORRECT and three with a stored
witness; TESTSEL exactly one fails-before-passes-after, three pass both; LOCALISE rules (i)-(iii) and the K21 hunk rule) are
ROW-level; K10 hidden-suite leak scan on the rendered row; C1 module-use ledger (a TESTSEL module is refused for any other head,
and for T42c and T56g, AT CREATION); names guard (closed allow-list; no P1-realism exemption inside the 3,000); token rule G6
per row; PII scrub; exact-duplicate refusal on the AST-normalised hash and the reuse ledger; ladder level, WP tag, LK tag,
granularity, wrapper id, VR-FMT id and the A1 fields (template id, wording id, operator / candidate / transform id) recorded;
A16 parse-back.
(b) G13: the batch goes to the stamp service against every registered target with every method listed for that target (registry
sha bound; R6 sha-bound scaffolding exemption on header, option scaffolding, definitions card; OHS-AC binding for new rows;
OHS-5 hash-export targets use exact and hashed n-gram methods only). (c) The stamp (row id, registry sha, method-set version,
generator code sha, verdict) goes in the row manifest. A failed row is dropped and logged (row id, target name, method; never
the matched text). No unstamped or failed row enters the pool. A template, wording-pool, cue-pool or view-renderer change after
hash export v1.1 means a new hash export and re-stamped rows.
FIX TRIGGER (all rows): > 1% of the rows of the 1,000-row pilot or of any full-generation day dropped for a reason other than
exempt scaffolding or OHS-5 collisions = the family's ONE combined fix (G3); OHS-5 collisions are dropped row by row and are not the
fix iteration while <= 5%. Answer-check drop rates keep the G0-lite bars (block drop > 2% for disagreement returns the block; kept
yield < 80% of 3,000 = fix iteration).
Set-level checks ONCE per family (pilot, then the built family): A50 G6 at size, A49c balance, wording variety (>= 50 per form,
none > 2%), matched-pair share, K1-K16 as written, K18-K26 below, G5-H (two Haiku solvers on 300 rows + one Haiku read of 100% of
free-form wording), G3-H, Opus A43(d). Then C2 reads on od-l4b (pipelined; not a kill gate). AFLite-style repair [LEV A2] is the
ONE fix tool for a missed shortcut probe (filtered <= 30% and reported).

## 11. Gates added or changed (G0-lite ids kept; new ids continue the sequence; probe protocol G5)

| Id | Gate | Bar | Class |
|---|---|---|---|
| T57-K1..K16 | as G0-lite, with C2 (hidden suites are PROGRAM-generated from behaviour atoms) and G5 applied | as G0-lite | PK |
| T57-K9 (extended) | LOCALISE / TESTSEL option probe adds: card names the gold entity, changed-token class, granularity | acc <= 28%, upper <= 31% | PK |
| T57-K10 (extended) | hidden-suite leak scan + cross-row scan (C1): no H test body of a module in any rendered row except that module's TESTSEL rows | 0 hits | PK |
| T57-K17 (replaced) | A50 G6, A49c, G5-H, G3-H, A43(d) per plan; the G13 line is replaced by K25 | per plan | PK |
| T57-K18 | A10 wrapper gates (section 4) | as stated | PK |
| T57-K19 | WP class mix 45 / 35 / 8 / 7 / 5 +- 5 pp, each >= 3%; every INCORRECT candidate has a stored witness; CAND-EXTRA >= 8% of INCORRECT (floor 80) | as stated | PK |
| T57-K20 | Ladder composition and twin share (section 6) | L1 20 / L2 30 / L3 30 / L4 20 +- 5 pp; L3-L4 >= 25% overall and per head; twins >= 50% of L3-L4; LK2 <= 10% | PK |
| T57-K21 | LOCALISE granularity gates (section 7) | as stated | PK |
| T57-K22 | A16 VR-FMT gates (section 5) | as stated | PK |
| T57-K23 | Module-use ledger at creation: TESTSEL modules used elsewhere | 0 violations | PK |
| T57-K24 | Ladder measured bar: C2 (C1 if none) on L4 rows of the 1,000-row pilot | accuracy <= 70% | PRE-FREEZE FIX TRIGGER (model read on our own data; never a kill; after the fix a report line) |
| T57-K25 | Check at creation (section 10): 100% of pooled rows carry a current clean stamp and an answer-check record | 100% / 0 unstamped; drops <= 1% outside exemptions (OHS-5 collisions <= 5%) or the fix iteration | PK |
| T57-K26 | A1 / A2 hooks: template id, wording id, operator / candidate / transform id on 100% of rows | 100% | PK |
| T57-R6 | Accuracy by WP class, by LOCALISE granularity, by ladder level, vs base 4B and trivial baselines | report (CI) | PR |
| T57-R7 | Wrapper flip rate and held-out wrapper gap; held-out VR-FMT accuracy vs trained formats | report (CI) | PR |
| T57-R8 | LOCALISE realism accuracy (ManySStuBs4J, TSSB-3M) separate lines, "train split seen" | report | PR |

## 12. NAMES (new, relative to NAMES_MANIFEST_V1; for manifest v1.1)
- row_job_families_allowed: add T57r (the P1-realism names exemption applies to T57r and to the L-R LOCALISE rows only; the
  3,000 T57 rows keep the closed allow-list).
- carrier ids: CUE_COMMENT (A10 wrapper line; shared with T42c, T56g). No other new carrier (VISIBLE_RESULT, PATCH_DIFF, COMMENT_DECOY
  already exist).
- policy ids: defs_card.t57.* unchanged. For T57r: defs_card.t57r.verdict, defs_card.t57r.localise.
- runner ids: runner.pytest and runner.domain_enumerator.* already exist. T57r adds runner.repo_image_pytest (per-repo image test run).
- languages: none new for the 3,000. "java" and "python" arrive via the L-R vocabulary extraction (realism rows only).
- tool-only (never in rows): the mutation scorers already listed; per-repo image builder on od-sbx-build.
- registry ids (not guard-checked; for the hash export): question forms unchanged; WP-LOGIC, WP-INCOMPLETE, WP-TYPE, WP-BOUNDARY,
  WP-OBO; CAND-EXTRA; LK0, LK1, LK2; LOC granularity tags FUNC, FILE, HUNK; wrapper families W1..W5; VR-FMT-1..VR-FMT-8; ladder
  mechanisms M-WP, M-NEAR, M-EXTRA, M-LOC, M-TSEL, M-HELP, M-LEAK; levels L1-L4; T57r neg_source value own_mutator.

## 13. G13 targets added (names only, registry before any row)
SWE-bench (full test set, Lite, Multimodal) and its splits, registry-only; the SWE-Gym Lite subset; the seeded internal hold-outs
of ManySStuBs4J, TSSB-3M, SWE-Gym and SWE-smith (by project, repo or instance) once frozen; Defects4J and BugsInPy as ID lists
only if the registry already carries them. The existing list stays (SWE-bench Verified, SWE-bench-Live, SWE-rebench, SWE-smith,
SWE-Gym, PatchDiff, UTBoost, CodeJudgeBench, R2E-Gym, plus the standing targets).

## 14. Fix iteration and kill rule
G3 governs (the 1,000-row pilot through the stamp wrapper is the first measured look; ONE combined fix). G4 governs (no head
rolls alone). Unchanged kill rule and floor (at least one of T42c / T57). T57r and the L-R LOCALISE rows have their own P1 rule: a
failure drops that slice only, logged; it never counts against T57.

## 15. Conformance seed (plan 16.1 step 0)
The fresh skeptic maps each row to file:function and a CPU test; the record builder refuses to run without the signed record for
its code sha and this ruling sha.
| Clause | Obligation | CPU test id |
|---|---|---|
| G1 | solver B imports stdlib + row schema only; no model client | T57-CM-01 |
| G3 | parameter file sha frozen at pilot launch; later change needs the fix-iteration flag | T57-CM-02 |
| G5 | probe calls grouped by module, 97.5th-percentile bound, permutation and leak checks | T57-CM-03 |
| G6 | row > 1,536 tokens refused at creation | T57-CM-04 |
| G7 | reason head rows from <= 25% of INCORRECT specs, outside the 3,000 | T57-CM-05 |
| C1 | a TESTSEL module is refused for any other head and for T42c / T56g; cross-row H-body scan | T57-CM-06 |
| C2 | the strings "Claude-written tests" / "Claude-written suites" do not appear in gate a or risk 1 of the G0-lite | T57-CM-07 |
| (c) | T_s rule: 0.90 if >= 70% of 50 pilot modules; one recipe revision; floor 0.80; non-Python extension to 20 modules; T_s recorded before any row | T57-CM-08 |
| (d) | patches editing test files are excluded | T57-CM-09 |
| (e) | with-outputs copies are exactly 25% of VERDICT / BEST4 / LOCALISE | T57-CM-10 |
| Gate a-d | module-level gates a and b before any row of the module; c and d per row | T57-CM-11 |
| 4 | wrapper correctness 50% +- 5; held-out families absent from training | T57-CM-12 |
| 5 | VR-FMT parse-back 100%; 256-token cap | T57-CM-13 |
| 6 | level from mechanism parameters only (no model-score input); twin present | T57-CM-14 |
| 7 | HUNK rule: reverse of the bug hunk alone passes V; each other reverse fails V; benign hunks exhaustively equivalent | T57-CM-15 |
| 9 | T57r negatives only from the own mutator; no problem_statement; per-repo licence whitelist | T57-CM-16 |
| 10 | pool writer refuses any row without a current clean stamp and an answer-check record | T57-CM-17 |

## 16. Risks (new)
1. T57r execution images may not be feasible under "no installs in the sandbox" and gVisor; the slice is conditional and dropped
   cleanly if the feasibility test fails.
2. Weak real test suites: SWE-Gym / SWE-smith F2P and P2P lists are the datasets' own; T57r avoids the weak-suite problem by never
   creating a candidate whose correctness is unknown (CORRECT = the dataset's own fix; INCORRECT needs an observed failure).
3. Mutator-made negatives on real patches can show a mutator signature; K8 and the pair design cover it.
4. HUNK rows are the most generator-complex new part; an edit-type shortcut (operator / constant edit = bug) is the main risk.
5. SWE-smith strategy mapping is UNVERIFIED; the whole SWE-smith half waits for it.
6. A10 wrapper comments could raise the comment-presence gap (K8); wrappers count inside it.
7. LOCALISE realism rows are Java (ManySStuBs4J) and not executed; they cannot be gold-checked beyond the dataset's own label.

## 17. Items for Opus to confirm
1. Sizes by substitution (A10 150, no head changes) and the LOCALISE re-split 480 / 120 / 200 with the executed HUNK rule.
2. WP class shares 45 / 35 / 8 / 7 / 5 (planner rounding of the inventory 47 / 35 / 7 / 6 / 1) and CAND-EXTRA >= 8%.
3. Ladder rule, composition, and K24 as a fix trigger rather than a kill.
4. Accounting: realism and T57r rows sit outside the 3,000 and their failure never touches T57.
5. T57r definition of CORRECT (the dataset's own fix after gold-sanity) and INCORRECT (own-mutator edit of its added lines, observed
   failure), with no differential gate (no reference input generator exists for real repos).
6. A15 (format dialects of the definitions card body) is not assigned to L-C in the build order; default NOT carried.
7. Whether GitHub issue text in SWE-Gym counts as a "social-platform post" under A82 4. Default: no issue text in any T57r row.
8. Whether a subset of the human gold patch's hunks (a partial fix) counts as "a SWE-Gym patch" under Sk 26. Default: not used.

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: APPROVE (no must-fix).
Binding conditions: T57-B1 items 1-5 confirmed. T57-B2 item 7: GitHub issue text is treated as a social-platform post (strict
A82 4): no issue text in any T57r or LR-09 / LR-10 row. T57-B3 item 8: a partial subset of the human patch is not used. T57-B4
T57r is a new row-job family id (manifest v1.1) with the P1-realism names exemption; the 3,000 keep the closed list. T57-B5 A10
held-out W3 / W5 fixed by GV2; item 6 -> GV7.
