# G0-LITE: T57 PATCH-VERDICT (clean-room; 3,000 rows; lane L-C)

Status: DRAFT for Opus approval (Mon 19 Oct). Written Sun 18 Oct 2026 by the L-C Sonnet author. Design only: no rows, no
generated code, no execution. Every identifier below is a NAME for the names-only manifest, never a row value.
Plan refs: v3.1 section 1 B.9, section 1 E, section 2 (toolchains, licence bars, SWE-smith problem_statement bar),
section 8 (sandbox).

## 0. One-paragraph summary

Given a small multi-file module with one injected bug, the visible failing test, and one or four candidate patches
(unified diffs against the buggy code; patches never touch test files), the 4B answers: (VERDICT) does the patch fix the
failing test without breaking passing ones; (BEST4) which of four patches is correct; (TESTSEL) which of four tests
detects the fix; (LOCALISE) which of four functions holds the injected bug. Gold is a FOUR-GATE gold: gold-sanity,
mutation strength, differential execution, and two-solver agreement. Hidden suites are never rendered.

## 1. Decision and label set

| Head | Share | Rows | Question form id | Label set |
|---|---|---|---|---|
| VERDICT | 33.3% | 1,000 | T57-Q-VERDICT | primary: CORRECT / INCORRECT; auxiliary reason head over INCORRECT rows: PARTIAL / REGRESSION / NOFIX |
| BEST4 | 26.7% | 800 | T57-Q-BEST4 | letter A-D (exactly one correct patch among four, shuffled) |
| TESTSEL | 13.3% | 400 | T57-Q-TESTSEL | letter A-D (the one test that fails before and passes after the fix; three distractor tests pass both) |
| LOCALISE | 26.7% | 800 | T57-Q-LOCALISE | letter A-D (the function that contains the injected bug) |

Execution classes (fixed here; label of a candidate patch is the first rule that applies, in this precedence):
1. NOFIX: the visible failing test still fails after the patch.
2. REGRESSION: the visible failing test passes but at least one hidden test tagged PASS-TO-PASS now fails.
3. PARTIAL: the visible test passes, no pass-to-pass test fails, but another hidden test tagged with the target behaviour
   fails, OR the differential run finds a divergence from the reference inside the declared input domain.
4. CORRECT: all hidden tests pass AND the differential run finds no divergence over the declared domain.
VERDICT label = CORRECT vs the other three. Reason head = the class (INCORRECT rows only; train/report only if C2's
schema supports an auxiliary head; otherwise it stays a manifest field and a report line).
TESTSEL and LOCALISE have no INCORRECT class: their gold is the execution-defined unique option (see section 2).
Out of scope for P0 (stay in P1 T57r): real-repo patches, "symptom-only" from real gold patches, any SWE-smith or
SWE-Gym content. Patches that edit test files are excluded from T57 (they belong to T56g), so a "touches tests" flag is
constant here.

## 2. Gold method; solver A vs solver B

Gold = execution in the od-sbx1 sandbox on program-generated modules (reference R, buggy B, candidate C, visible test V,
hidden suite H, differential input set D). No external code. Four gates, all must hold for a row to be kept:

- GATE a, gold-sanity: every test of H and V passes on the reference R (2 runs, sandbox default). A module failing this
  is dropped and counted (the Claude-written-test risk is real; its size is unmeasured, so it is measured here).
- GATE b, strength: H kills at least T_s of the NON-EQUIVALENT mutants of R produced by an independent mutant pool
  (Python: mutmut BSD-3 or cosmic-ray MIT as OFFLINE scorers inside the sandbox image; non-Python: our own mutator with
  an operator-id partition disjoint from the operators used to inject bugs and build candidates). A mutant is
  non-equivalent only when a distinguishing input from D (or the exhaustive domain) proves it; mutants with no
  witness are "undecided", excluded from the denominator and counted. Proposal T_s = 0.90. The 50-module pilot (Sun 25
  Oct; 38 Python, 4 JS/TS, 4 Go, 4 bash) fixes T_s with this rule, written before the pilot: T_s = 0.90 if at least 70%
  of pilot modules reach 0.90 at the planned suite recipe; otherwise the suite recipe gets one revision (more boundary
  and pairwise cases from D) and the pilot is rerun on fresh modules; T_s never goes below 0.80. If a non-Python language
  scores below 0.80 on its 4 modules, that language's pilot is extended to 20 modules before any row. Modules below T_s
  are dropped; rows are never relabelled. T_s is recorded before any row exists.
- GATE c, differential: reference vs candidate over D = program-generated inputs inside the spec-declared domain (our own
  typed-domain enumerator with boundary values taken from the spec's thresholds and pairwise combinations; exhaustive
  when the domain is <= 5,000 points; for stateful modules, call sequences up to length 4 over the declared operation
  set; Hypothesis is not used). Any divergence = witness for PARTIAL (or REGRESSION/NOFIX by precedence). A kept CORRECT
  row has zero divergences.
- GATE d, two-solver agreement: see below.

Gold per head:
- VERDICT / BEST4: execution class of each candidate (section 1). BEST4 keeps a row only if exactly one of four
  candidates is CORRECT and the other three have a stored execution class != CORRECT with a witness (failing test id or
  divergent input).
- TESTSEL: each of the four tests is run on pre-patch code (buggy B) and post-patch code (fixed R-equivalent). Exactly
  one fails on B and passes after; the three distractors pass on both. Distractors include >= 1 that executes the changed
  entity (by trace) yet passes both, and >= 1 from the same file as the changed function.
- LOCALISE (from our own mutator; one modifier per mutant): gold = the mutated function. Keep only if (i) at least one
  test fails only because of the mutation, (ii) the mutated entity is unique (a single operator class applied at sites
  inside one function), (iii) a killing test traverses that entity (trace). Distractor functions: >= 1 traversed by the
  killing test but unmutated; >= 1 from the same file; the rest from other files of the module. Planning guess: about
  2.5 mutant candidates generated per kept row (SWE-smith paper yield 40.2%); the realised yield is reported. The SWE-smith
  modifier lists (13 Python, 14 JS) are a checklist for coverage of operator classes; our own mutator and Go/bash
  analogues are written from scratch.

Candidate library (registry ids; labels come from execution, never from the intent of the operator): CAND-INVERSE
(exact inverse of the injected bug), CAND-ALTFIX (alternative correct rewrite, ALL ALTFIX candidates still pass the four
gates), CAND-HALFSITE (fixes one of several injected sites), CAND-NEARMISS (inverse plus one wrong token), CAND-HELPERSHIFT
(fix applied in a shared helper), CAND-NARROWGUARD (fix gated on a property of the failing input), CAND-WRONGPLACE
(plausible edit elsewhere). Bug injection uses mutator operators with MULTI-SITE variants inside one function so that a
half fix is possible without breaking the one-modifier LOCALISE rule.

Solver A = primary pipeline: module generator, mutator, candidate library, executor runs, class assignment, spec
expectation (for example CAND-INVERSE expected CORRECT; CAND-HALFSITE expected PARTIAL). An unexpected class is kept only
when the execution witness is complete (it is data about the operator, logged); unexpected classes in > 15% of an
operator's candidates send that operator back to the builder.
Solver B = separate Sonnet high session; sees only this G0-lite and the row-JSON schema. B recomputes the execution
class of every candidate, the TESTSEL pre/post table, and the LOCALISE gold from module files and hidden suites with its
own harness and its own differential enumerator. Agreement on 100% of kept rows (disagreements dropped, counted); block
trigger: > 2% disagreement returns the block. B's package imports only the standard library and the row schema.

## 3. Inputs, input view, state model

- INPUT VIEW (v3 rule): the primary view is code and tests only: task card (program-rendered statement of the intended
  behaviour from the behaviour spec, wordings from a Haiku-authored pool), buggy source (only the relevant files,
  trimmed by a program), the visible failing test, and candidate patch(es) as unified diffs. Tool outputs are stripped.
  A labelled variant WITH tool outputs adds the visible-test result text capped at 256 tokens per output (VERDICT, BEST4
  and LOCALISE only: the failure output of V on B, and for VERDICT the post-patch result of V). Hidden-suite output is never
  shown. Variant share: 25% of rows are rendered a second time as the with-outputs variant (extra copies, same gold).
  In the variant the T41c-style provenance rule applies (outputs are tool results, not instructions).
- Module model (shared with T42c and T56g, seed spaces disjoint per family; the builder owns one module generator):
  application-style, 1-4 files, in-memory state only, a behaviour spec of atoms (boundary rule, aggregate, filter, state
  update, formatting, dedup, rule table), a typed input domain, and a table-driven hidden suite tagged TARGET or
  PASS-TO-PASS. The visible failing test V is one TARGET case; the hidden suite H is the rest plus boundary and pairwise
  cases from D. No clocks, randomness, environment reads, network.
- Physical separation: V and H live in different files and different stores; H is never in a rendered prompt. A CPU leak
  check (K9) scans every rendered row for H test bodies (normalised) and fails on a hit. (TESTSEL options are H tests
  by design and are excluded from the scan for that head only.)
- Token budget: mean <= 800, cap 1,536 on <= 10% of rows. BEST4 shows four diffs of <= 15 changed lines each; module
  context is a program slice around the changed region.
- Execution pins: Python 3.12.x; Node 24.x LTS; Go 1.26.x with `GOFLAGS=-mod=vendor GOPROXY=off GOTOOLCHAIN=local`;
  bash from the pinned base image; exact patches and digests come from the L-0 image record and are copied into every
  manifest. Hidden suites run with language-native runners and the runner config passed by the executor (Python: an
  executor-owned empty ini file on a read-only path plus explicit `--rootdir`, `--noconftest`; Go: `-count=1`; JS:
  `node --test`; bash: an executor-owned driver). No package installs.

## 4. Sizes and shares (3,000 rows; before drops)

| Axis | Target | Gate floor / cap |
|---|---|---|
| Python | 75% | <= 75% |
| JS/TS | 9% | >= 8% |
| Go | 8% | >= 8% |
| bash | 8% | >= 8% |
| Per-head language split (Py/JS-TS/Go/bash) | VERDICT 750/90/80/80; BEST4 600/72/64/64; TESTSEL 300/36/32/32; LOCALISE 600/72/64/64 | |
| VERDICT CORRECT rate | 50% | 40-60% overall, per language |
| VERDICT reason mix among INCORRECT | PARTIAL 40 / REGRESSION 35 / NOFIX 25 | NOFIX <= 25%, none > 45% |
| BEST4 / TESTSEL / LOCALISE gold letter | 25% each | 25% +/- 3 pp |
| BEST4 correct option that is CAND-ALTFIX | >= 30% of BEST4 rows | breaks the "correct = medoid of the options" shortcut |
| Matched-pair rows | >= 30% | near-miss pairs (correct vs one-token-off incorrect on the same bug) >= 15%; rename twins or ALTFIX pairs >= 10% |
| Misleading-comment decoys | 15% of INCORRECT patches carry a comment or message claiming a fix | comment presence equal across labels within 3 pp (overall comment rate about 30% for both) |
| Rename twins | 10% of rows have a locals-renamed twin (same gold) | |
| Order-invariance copies | +20% extra copies with a random non-identity permutation of options | plan section 5 |
| Reuse limits | <= 4 rows per base module per head; <= 8 per base module overall | |
Candidate-count planning: about 2.5 generated mutants per kept LOCALISE row; about 4-5 generated candidates per kept BEST4
row; yield below 80% of target rows (2,400 kept) triggers the fix iteration.

## 5. Gates

Probe protocol (all PRE-FREEZE probes): 5-fold group cross-validation grouped by base module id; logistic regression with
fixed regularisation and no tuning on held-out folds; pooled out-of-fold predictions; 95% bound by cluster bootstrap over
module ids (2,000 resamples, fixed seed). Binary: AUC <= 0.55, upper <= 0.60. k-way: accuracy <= 1/k + 3 pp and upper <= 1/k
+ 6 pp (k=4: 28% and 31%; k=3 reason head: 36.3% and 39.3%). All values fixed before any pilot. GBT on the same features is
ADVISORY only.

| Id | Gate | Bar | Class |
|---|---|---|---|
| T57-K1 | Gate a gold-sanity: H and V all pass on R | 100% of kept modules | PRE-FREEZE KILL |
| T57-K2 | Gate b strength: kill share of non-equivalent mutants per module | >= T_s (proposal 0.90, set by the 50-module pilot under the rule in section 2; floor 0.80); at least 85% of generated modules clear T_s or the module generator returns to the builder | PRE-FREEZE KILL |
| T57-K3 | Gate c differential run recorded for every candidate; CORRECT rows have zero divergences | 100% | PRE-FREEZE KILL |
| T57-K4 | Gate d two-solver agreement | 100% of kept; block drop > 2% returns block | PRE-FREEZE KILL |
| T57-K5 | Style-only probe, VERDICT (patch length, line counts, hunks, comment ratio, identifier statistics) | AUC <= 0.55, upper <= 0.60 | PRE-FREEZE KILL |
| T57-K6 | Style-only probe, BEST4 (per-option features, argmax per row), including medoid feature (mean edit distance to the other options) | acc <= 28%, upper <= 31% | PRE-FREEZE KILL |
| T57-K7 | Reason-head probe (style-only) on INCORRECT rows | acc <= 36.3%, upper <= 39.3% | PRE-FREEZE KILL |
| T57-K8 | Comment-only probe (comment text and commit-message text alone) and comment-presence gap | AUC <= 0.55, upper <= 0.60; gap <= 3 pp | PRE-FREEZE KILL |
| T57-K9 | LOCALISE option probe (function size, position in file, call depth, traversed-by-test flag, name stem class) and TESTSEL option probe (test length, names the changed entity flag, same-file flag) | each acc <= 28%, upper <= 31% | PRE-FREEZE KILL |
| T57-K10 | Hidden-suite leak scan on rendered rows (not TESTSEL options) | 0 hits | PRE-FREEZE KILL |
| T57-K11 | Balance: CORRECT rate 40-60%; reason mix; letters 25% +/- 3 pp | as stated | PRE-FREEZE KILL |
| T57-K12 | Quotas: pairs >= 30% (near-miss >= 15%); decoys 15% with comment-rate parity; Python <= 75%, JS/TS, Go, bash each >= 8%; ALTFIX >= 30% of BEST4 correct options | as stated | PRE-FREEZE KILL |
| T57-K13 | LOCALISE rules (i)-(iii) and one-modifier uniqueness | 100% of kept rows | PRE-FREEZE KILL |
| T57-K14 | Dedup (AST-normalised, across T42c/T57/T56g modules) | <= 1% | PRE-FREEZE KILL |
| T57-K15 | Token mean <= 800; cap 1,536 on <= 10%; >= 50 wordings per question form, none above 2% | as stated | PRE-FREEZE KILL |
| T57-K16 | Names guard against the closed manifest | 0 violations | PRE-FREEZE KILL |
| T57-K17 | Standard pipeline: 200-row G13 pilot (<= 1% hit), A50 G6, A49c, G5-H (two Haiku solvers on 300 rows; Haiku read of 100% free-form wording), G3-H, Opus A43(d); OHS-5 collisions <= 5% not a fix iteration | per plan | PRE-FREEZE KILL |
| T57-R1 | Accuracy per head and reason class against base 4B, random (50% / 25%), majority class, patch-size baseline, touches-tests flag (constant here, stated), always-CORRECT | report (CI) | POST-TRAINING REPORT |
| T57-R2 | Invariance: rename-twin flip rate, option-order flip rate, decoy slice vs no-decoy slice accuracy | report (CI) | POST-TRAINING REPORT |
| T57-R3 | Accuracy per language and per head, with-outputs variant vs primary view | report | POST-TRAINING REPORT |
| T57-R4 | ECE, Brier, trap-slice ECE | report | POST-TRAINING REPORT |
| T57-R5 | Observed weak-suite rate (candidates that pass H but diverge in D) as a diagnostic of the Claude-written suites | report | POST-TRAINING REPORT (computed from data pre-freeze, reported only) |
No claim about SWE-bench Verified verdicts is made. Fresh-month Tier-2 slices (SWE-bench-Live / SWE-rebench) are L-E's
report-only business; their labels inherit weak-suite error rates.

## 6. Clean-room notes

- Written without opening any T27/T40-T46 generator, template or wording pool, mutate.py, OHS-AC, any "ohs"/"sealed" path,
  the v3 plan file, the skeptic file, or any benchmark's item text. Read only: PLAN_TRAINING_SIDE.md, LANE_L-C.md,
  excerpts/codeexec_s5.md.
- SWE-smith: problem_statement text is BARRED (LM-written, arXiv 2504.21798v2 section 2.1); no SWE-smith, SWE-Gym or
  SWE-rebench content is used in P0 at all (those are P1 T57r, conditional). Only the paper's modifier names serve as a
  coverage checklist for the builder's own mutator.
- Licence bars respected: mutmut (BSD-3) and cosmic-ray (MIT) are offline scorers only and appear in no row;
  Hypothesis (MPL-2.0) is not used or vendored; bashlex and other barred tools are not used; sqlglot is not needed here.
- Task statements are program-rendered from behaviour atoms; wording pools come from Haiku and are shared only through the
  template/wording-pool hash export. No LLM writes a label, a patch, or a test (candidate patches are program-built from
  the registry).
- Entity-like strings from the seeded namespace with the TRAINING salt; closed vocabulary stems for generic identifier
  parts. No external identifiers (no CVE/GHSA ids, no repository names, no issue text).
- No data row, example patch or generated code appears in this file.

## 7. NAMES the family needs (for the names-only manifest)

- Languages: Python; JavaScript; TypeScript (conditional on the self-test); Go; bash.
- Runners: pytest-style Python runner invoked with executor-owned config (names: `--noconftest`, `--rootdir`, empty ini on
  a read-only path); `node --test`; `go test -count=1`; bash driver with POSIX `[`.
- Tools (all tool-only, never in rows): own module generator; own AST mutator (operator classes MUT-01..MUT-14 as in
  T42c, plus multi-site variants MS-01..MS-04); own candidate library CAND-INVERSE, CAND-ALTFIX, CAND-HALFSITE,
  CAND-NEARMISS, CAND-HELPERSHIFT, CAND-NARROWGUARD, CAND-WRONGPLACE; own typed-domain enumerator; mutmut; cosmic-ray;
  gVisor runsc; od-sbx1; od-sbx-build; executor.
- Question forms: T57-Q-VERDICT, T57-Q-BEST4, T57-Q-TESTSEL, T57-Q-LOCALISE (>= 50 wording ids each); definitions card
  per head (C2's scaffolding, sha-bound).
- Carriers: TASK_CARD, SRC_FILE, VISIBLE_TEST, PATCH_DIFF, OPTIONS, VISIBLE_RESULT (variant only), COMMENT_DECOY.
- Domains: same generic application-area list as T42c (inventory and stock rules; invoice and ledger totals; discount and
  pricing; capacity booking over integers; role and rule matching; deduplication; retry state machines; templating and
  formatting; unit conversion with given tables; pagination; config merging; route lookup over given graphs; log tallying
  over given strings; queue and batch processing; record validation). Domain rule 3 versus OHS-3/4/5 G is checked by the
  orchestrator.
- G13 targets (names only): SWE-bench Verified; SWE-bench-Live; SWE-rebench; SWE-smith; SWE-Gym; PatchDiff; UTBoost
  patch sets; CodeJudgeBench; R2E-Gym; plus the standing list.

## 8. Risks

1. Claude-written hidden suites may be weak or wrong (the 2606.16062 audit warning). Mitigated by gates a, b, c; the weak
   suite rate is measured (R5) and not assumed.
2. Mutant pool independence: bug injection and strength scoring must not use the same operators, or "strong" means
   "kills what I injected". Partition enforced; Python uses external scorers.
3. Equivalent mutants: a mutant with no distinguishing witness is "undecided" and excluded, which can inflate the kill
   share. The undecided share per module is reported; > 25% undecided drops the module.
4. Medoid / similarity shortcuts in BEST4 (wrong patches are mutations of the correct one). ALTFIX >= 30% and probe K6.
5. Comment decoys can create a "comment = wrong" cue if comment presence differs by label. Parity gate K8.
6. TESTSEL is the builder's reading of the plan's bare label "TEST-SELECTION": confirm with Opus (section 10).
7. Non-Python mutation tooling is our own, which weakens the independence claim for JS/TS, Go, bash; reported per language.
8. Pilot size for non-Python strength is thin (4 modules each) and may force a pilot extension on Sun 25 Oct.
9. Throughput: four patches per BEST4 row, three-way suites, differential runs; the sandbox queue is the bottleneck for
   25 Oct to 2 Nov. Sequence T42c, T57, T56g.
10. Overlap with T56g (special-casing visible inputs): T57 never edits tests and CAND-NARROWGUARD gates on a property of
    the input, not on literals of V; T56g owns literal special-casing. Module seed spaces are disjoint.

## 9. The one fix iteration and the kill rule

- One fix iteration per family, shared by all gates. Run every CPU gate (K1-K16) on the 1,000-row pilot first; pilot-stage
  tuning is logged development; after the 200-row G13 pilot each change consumes the fix iteration (a pilot with > 1%
  hits IS the fix iteration; scaffolding-only hits and <= 5% OHS-5 collisions are not). Interpretation for Opus to confirm.
- Fix levers: add suite cases from D and rerun gate b; retire or re-tune an operator whose realised classes disagree with
  its expectation; rebalance reasons; replace a failing head's distractor generator; raise ALTFIX share; never relax a
  bar and never lower T_s below 0.80.
- Kill rule: fail any PRE-FREEZE KILL gate after the fix iteration, or not through all by the data freeze (Mon 2 Nov
  23:59 UTC) => T57 rolls to C2.2/C3, logged with the failing gate and numbers. A head (for example TESTSEL) that alone
  fails after the fix iteration may roll alone, leaving the other heads (Opus ruling at the freeze); the family still
  counts for the floor only if VERDICT and LOCALISE or BEST4 pass. POST-TRAINING lines are never kill rules. Plan floor:
  at least one of T42c/T57 passes.
- Schedule: the 50-module mutation pilot is Sun 25 Oct, rows start after sandbox sign-off (target Wed 21 Oct; if not by Fri
  23 Oct, report the risk, keep coding).

## 10. Items for Opus to confirm at approval

(a) TESTSEL definition. (b) Reason head as auxiliary only. (c) T_s rule and the 0.80 floor, plus the pilot extension for
non-Python. (d) Excluding test-editing patches from T57. (e) 25% with-outputs variant copies. (f) Pilot-stage tuning versus
the single fix iteration. (g) Per-head roll-alone rule at the freeze.

## Opus rulings 18 Oct (appended word for word from families/G0_APPROVALS.md by the L-C builder, Sun 18 Oct 2026)

The Round 2 table (G0_APPROVALS.md, 'Round 2') lists this family as: APPROVE (round 1 stands), no new binding conditions; the round-1 addendum below was NOT in the file when Round 2 ran and is appended now by the lane builder.

Where the body text above says otherwise, this addendum binds. Global rulings G1-G10 apply to every family and are repeated below word for word; the family decision follows.

## Global rulings (bind every family; each family addendum cites them by number)

G1 SOLVER B IS A PROGRAM. In every family, "solver B = separate Sonnet session" means CODE written by a separate Sonnet
high session from the G0-lite (and the row schema) only. No LLM reads rows one by one to produce or check labels. LLM
reads (G5-H, G3-H, A43(d)) are audits: they never set or change a gold label. A confirmed defect is fixed in the generator
or the rule table, never by relabelling a row.

G2 DATA-AUDIT GATES ARE PRE-FREEZE. A50 G6, A49c, G5-H, G3-H and A43(d) read data, not a trained C2.1 model, so they are
PRE-FREEZE gates under the standard pipeline. Skeptic 6 bars only gates that need the TRAINED model. A G5-H flag counts
only after Sonnet medium adjudication and Opus A43(d) confirmation, and (where the family has a program solver) after a
program re-run reproduces it. Their bars are the values in the A50/A49c/G5-H/G3-H records, supplied by L-0. (Answers T50
O4, T51 O3, T53 O4, T41c O6, the T54/T55/T56 flag, GEN point 2, VOICE V-H1.)

G3 NO FREE PILOT TUNING. The 1,000-row pilot is the first measured look at every PRE-FREEZE gate. Run the family's CPU
gates and its 200-row G13 pilot on that first pilot, then make ONE combined fix if anything fails: that is the fix
iteration. Changing generator parameters after seeing pilot gate numbers and "re-running for free" is not allowed. Before
the pilot, defects found by unit tests, the build skeptic or solver A/B disagreement on CPU test fixtures are build fixes.
The plan's two exemptions stay (scaffolding-only G13 hits; OHS-5 collision drops up to 5%). (Answers T42c (d), T57 (f),
T56g (f).)

G4 KILL GRANULARITY. P0 families are killed or kept as a whole (plan section 8). The only split the plan names is T56
(done-claim half) / T56g. No sub-block or head "rolls alone" in C2.1. If an orchestrator wants that, it is a plan change
for the orchestrator, not a G0-lite choice. GEN (not a P0 family, no floor) may roll sub-blocks alone (GEN point 3
approved). VOICE keeps its lane rule. (Answers T54 item 7, T55, T56, T57 (g).)

G5 ONE PROBE HARNESS. L-0 builds one CPU probe harness for all families, and every family uses it with its own features
and groups:
- grouped split by the family's pair/spec/module/task group (no group in both train and held-out);
- L2 logistic regression with fixed or inner-CV regularisation (never tuned on held-out);
- AUC is reported as max(AUC, 1 - AUC);
- the upper bound is the 97.5th percentile of 2,000 cluster-bootstrap resamples over held-out groups (the stricter
  reading of "95% upper bound"; T50, T51 and T53 change from the one-sided 95th percentile);
- k-way probes use balanced accuracy (mean per-class recall) against 1/k + 3 pp and 1/k + 6 pp;
- every probe run includes a label-permutation sanity check (AUC 0.50 +- 0.03) and an injected-leak power check (as T41c
  K7: a planted one-feature leak must reach AUC >= 0.80), else the run is invalid and is repeated (not a fix iteration).
GBT probes are advisory in every family except GEN, where both probe models count as written (a GEN gate passes only if
both pass). The GEN/VOICE "confirm rule" (one re-run on a fresh sample twice the size, and the re-run decides) is
approved for GEN and VOICE only, because they run about 40 probes each. It is recorded and is not a fix iteration.

G6 TOKEN RULE READING. Mean <= 800 tokens per family; no row above 1,536; rows above 1,024 tokens <= 10% of the family.
T50 and T41c change their 1,000 line to 1,024.

G7 SECONDARY HEADS. The loss is on option letters and C2's layout is kept (plan section 5). A secondary head (T50
reason+tier, T53 reason+tier, T56 reason, T57 reason) is built as HEAD ROWS: the same rendered context with a separate
question form and its own lettered options, gold from the same rule table, in the same split as its primary row. Head
rows are extra copies outside the family size and come from at most 25% of the family's specs per head. They get the
family's k-way probe bars. If L-0 finds that C2's layout cannot carry a second question form, the head stays a manifest
field plus a report line. No new output token or suffix field is added. T51 violation_set stays metadata only (O1).

G8 SHARED NAMES. L-0 keeps ONE host-TLD list and ONE raw-IP pool in the names-only manifest, used by T50, T51, T53 and
T41c alike: reserved TLDs plus a generic list, and documentation/private IP ranges, with the deny-list collision check
against real brands and registered names. T41c moves from its reserved-only list to the shared list. This keeps the
families from showing a "which family am I" cue.

G9 CROSS-FAMILY LABEL CONSISTENCY. The same action in the same state under the same card must get the same label in
every family. L-A owns ONE shared effects-to-label table (in T50/G0_LITE.md section 3) that T51 and T53 cite instead of
restating their own rule. A CPU test runs every T50 spec whose effect class overlaps T51 (shared/production-lane mutation)
or T53 (egress) through the other family's engine and asserts equal labels. It must pass 100% before any pilot. T41c is a
carrier-directive decision, not an action gate, so it is not in this test, but its HARD/SOFT list must not contradict the
shared table (spot-checked by the L-I build skeptic).

G10 VOICE METADATA EXPORT. Every family with a natural-language user utterance (T50, T51, T53, T41c, T54, T55, T56 task
statements, GEN voice-eligible forms) exports `decision_spans` with a ROLE per span. Roles: negation/polarity, number,
entity/path/flag, and AUTHORITY. AUTHORITY marks any span whose presence in the user turn creates or limits permission:
consent naming, scope declarations, boundaries, delegation pointers, values whose source is the user turn. Families also
export `spoken_view` where they have one. L-0 routes this. It is a code requirement, not a gate.

### T57 PATCH-VERDICT: APPROVE

Binding conditions:
- C1 TESTSEL leakage. TESTSEL options are hidden-suite tests by design, so a base module used for a TESTSEL row is never
  used for any other T57 head, nor for T42c or T56g. K10 adds a cross-row scan: no H test body of a module appears in
  ANY rendered row of the family except that module's own TESTSEL rows.
- C2 Wording fix. The hidden suites are PROGRAM-generated from behaviour atoms (the generator code is Claude-authored).
  Replace the "Claude-written tests/suites" wording in gate a and risk 1, so it does not read as LLM-written tests. The
  gold-sanity and strength gates stay exactly as written.
Rulings: (a) the TESTSEL definition (fails on buggy, passes after the fix; 3 distractors pass both) is approved. (b) the
reason head follows G7. (c) the T_s rule (0.90 if >= 70% of the 50 pilot modules reach it; one suite-recipe revision;
floor 0.80; non-Python pilot extended to 20 modules if it scores below 0.80) is approved and fixed before any row. (d)
excluding test-editing patches is approved. (e) 25% with-outputs copies are approved. (f) see G3. (g) the per-head
roll-alone rule is not adopted (G4).
