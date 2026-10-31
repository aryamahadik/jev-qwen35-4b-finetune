# G0-LITE: T42c CODE-EXEC (clean-room; 3,000 rows; lane L-C)

Status: DRAFT for Opus approval (Mon 19 Oct). Written Sun 18 Oct 2026 by the L-C Sonnet author. Design only: no rows, no
generated code, no execution. Every identifier below is a NAME for the names-only manifest, never a row value.
Plan refs: v3.1 section 1 B.8, section 1 E (rules for every family), section 2 (toolchains, guards), section 8 (sandbox).

## 0. One-paragraph summary

A 4B reads application-style code (1-3 small files) and answers one of three question forms with one token: (A) which of
four listed outputs or exception classes the call produces, (B) whether two implementations are equivalent over a
declared input domain, (C) whether a stated test will fail. Every label is an execution witness stored in the row
manifest. Equivalence "yes" needs construction AND an exhaustive run; "no" needs a concrete distinguishing input. Three
runs agree or the row is dropped. 25% of rows are non-Python (JS/TS, Go, bash, each >= 8%).

## 1. Decision and label set

| Head | Share | Rows | Question form id | Label set |
|---|---|---|---|---|
| OUT4 output-or-exception | 40% | 1,200 | T42c-Q-OUT4 | one of 4 options (letters A-D, shuffled per row); each option is either a concrete output value or an exception class name |
| EQV2 equivalence | 30% | 900 | T42c-Q-EQV2 | YES (same observable result on every input of the declared domain) / NO |
| TFAIL2 will-this-test-fail | 30% | 900 | T42c-Q-TFAIL2 | YES (the stated test fails) / NO (it passes) |

Observable result (fixed in this G0-lite, used by B and C): the return value (compared by canonical repr), or the
exception CLASS NAME if one escapes; for stateful modules the ordered list of per-call results plus the module's
declared `snapshot` value after the call sequence. stdout is part of the observable only for OUT4 rows whose question
says "printed" and for bash rows. Message text is never compared unless authored by our own code (T42c-1).

Sub-structure inside heads (recorded in the manifest, never shown in the prompt):
- OUT4: exception-gold rows = 25% of OUT4 (300 rows); value-gold = 75% (900). Distractors are of three registered kinds:
  EXEC-NEARMISS (the executed output of a one-token mutant, verified different from gold and from each other),
  ARITH-PERTURB (gold value shifted by a small rule, verified different), EXC-SIBLING (another class from the closed
  per-language exception list). Each row carries >= 1 EXEC-NEARMISS distractor; no distractor kind is in more than 60%
  of rows' distractor slots.
- EQV2: YES = 450, NO = 450. YES constructions (registry ids EQ-YES-1..5): rename locals; reorder independent statements;
  loop/comprehension (or language-native iteration) swap; algebraic identity; early-return restructure. No construction
  above 30% of YES rows. NO sources: mutator operator classes (no class above 25% of NO rows) plus "hard-NO"
  (>= 20% of NO rows: the programs differ on <= 2% of the declared domain points, so a single random probe usually
  misses it).
- TFAIL2: FAIL = 450, PASS = 450. Test shapes: value assertion, expected-exception assertion, multi-assertion (1-4
  assertions), state-sequence test.

## 2. Gold method; solver A vs solver B

Gold = execution witness in the od-sbx1 sandbox (program/execution gold; no model writes or checks any label).

Witness rules (v3.1 T42c-1, plus this G0-lite's concretisations):
- OUT4: value or exception class from the sandbox; THREE runs byte-identical on the observable. (The sandbox default is 2
  runs per execution; the plan's witness rule is 3 for T42c output rows and wins; cost goes into L-0's throughput
  figure.) Exception option = class name only; message only for classes authored by our own code.
- EQV2-NO: concrete distinguishing input inside the declared domain, found by execution; both programs run on it three
  times, observables identical within each program and different across them.
- EQV2-YES: (1) registered by-construction transform id AND (2) exhaustive run of both programs over the whole declared
  domain, observables equal at every point, 3 identical runs per program. The declared domain is finite and shown in
  the prompt (for example a bounded integer range, bounded-length sequences over a small value set, or call sequences up
  to length 3 over a declared operation set), 25 to 5,000 points, so the label is exact for the question as asked. Random
  testing alone never yields YES.
- TFAIL2: THREE runs agree; generator lint (CPU, static) bans clocks, randomness, environment reads, filesystem outside
  /work, and order-dependent printing unless sorted. Timeouts and nondeterminism are dropped, not labelled.
- Executed-step count (for trace-length bins) comes from a separate instrumented twin run, not from the three witness
  runs: Python line-event counter limited to the module files; bash command trace (xtrace) lines excluding the harness;
  JS/TS and Go via our own counter-insertion rewrite. UNVERIFIED: the per-language counters are not comparable in
  absolute terms; bins are therefore computed per language and the cross-language bin edges (<10, 10-40, >40) are a
  convention. Sonnet builder confirms on Python that counter-insertion and the line-event counter agree within 10% on 100
  programs.

Solver A = the primary pipeline: generator emits a row spec; executor runs the witnesses; labeller applies the rules
above. A also records the SPEC EXPECTATION where the generator knows one (transform id => expected YES; mutator class =>
expected NO or expected changed output); an unexpected execution result is dropped and counted (this is also how
equivalent mutants and generator bugs are caught).

Solver B = a separate Sonnet high session that sees only this G0-lite and the minimal row-JSON schema (never A's code).
B re-derives every label from the rendered row alone: its own driver scripts per language, its own domain enumerator for
EQV2, its own comparison of observables. Lint: B's package may import only the standard library and the row schema file.
Agreement requirement: labels of A (witness), B and (where present) the spec expectation agree on 100% of kept rows;
disagreements are dropped and counted. Block-level trigger: > 2% of a generation block dropped for disagreement returns
that block to the generator (counts toward the one fix iteration only after the G13 pilot, see section 9).

## 3. Inputs, input view, state model

- INPUT VIEW (v3 rule): there are no user messages or tool calls in this family; the primary and only view is the code
  carriers listed below. A "with tool outputs" variant is NOT BUILT for T42c by design: captured outputs are the answer
  and would leak the label. Stated here so the per-family view requirement is met.
- Carriers (rendered fields; C2's rendered layout cygnet + schema_branch_mark is kept, field mapping confirmed by L-0):
  SRC_FILE (1-3 files, path header + language tag), CALL_SPEC (OUT4), PROGRAM_PAIR + DOMAIN_DECL (EQV2), TEST_FILE
  (TFAIL2), OPTIONS (OUT4), QUESTION_FORM (>= 50 wordings per form, none above 2%).
- Module model: application-style, multi-function, small in-memory state (records, queues, counters, rule tables,
  text/format helpers). No clocks, randomness, environment reads, network, or filesystem beyond /work tmpfs. Hash seed
  fixed (Python `PYTHONHASHSEED=0`, `python -I`); locale and timezone fixed (`LC_ALL=C`, `TZ=UTC`).
- Program size: module text <= about 60 lines shown; token mean <= 800 per row, hard cap 1,536 on <= 10% of rows;
  EQV2 shows two bodies of the same function (not whole modules) to stay in budget.
- Anti-collection rule: no textbook algorithm tasks, no single-function puzzle style, no function named from a public
  benchmark pattern; application-style only (domain list in section 7). Identifier vocabulary is generic domain stems
  plus seeded-namespace suffixes; entity-like strings come from the seeded namespace with the TRAINING salt.

Execution pins (plan section 2; exact patch versions and image digests come from the L-0 sandbox image record and are
copied into every row manifest; no non-Python row before they are recorded):
| Item | Plan-level pin | Exact value comes from |
|---|---|---|
| Python | 3.12.x | L-0 image record |
| Node | 24.x LTS (type stripping for TS rows only if the self-test proves it; otherwise TS rows are folded into JS and the JS/TS share stays >= 8%) | L-0 image record + self-test |
| Go | 1.26.x with `GOFLAGS=-mod=vendor GOPROXY=off GOTOOLCHAIN=local`, `go test -count=1` style runs, `-vet=off` | L-0 image record |
| bash | version of the pinned base image; external commands only from an allow-list recorded in the manifest | L-0 image record |

## 4. Sizes and shares (3,000 rows; before drops)

| Axis | Target | Hard floor / cap (gate) |
|---|---|---|
| Python | 75% (2,250) | <= 75% |
| JS/TS | 9% (270) | >= 8% |
| Go | 8% (240) | >= 8% |
| bash | 8% (240) | >= 8% |
| Trace-length bin <10 / 10-40 / >40 | 30 / 40 / 30% | each >= 15% |
| Matched-pair rows | >= 30% | invariant ("same behaviour, different implementation") >= 15% of rows; one-token near-miss >= 10% of rows |
| YES rate (EQV2, TFAIL2) | 50% | 40-60% overall, per language, per trace bin, per similarity quintile |
| OUT4 gold letter | 25% each | 25% +/- 3 pp after shuffle |
| Exception-gold in OUT4 | 25% | 20-30% overall; >= 15% in each non-Python language where a stable class list exists |
| Order-invariance copies | +20% extra copies with a random non-identity option permutation (OUT4 only; binary heads use reversal) | plan section 5 |
Per-head language split follows the totals: OUT4 900/108/96/96, EQV2 675/81/72/72, TFAIL2 675/81/72/72 (Py/JS-TS/Go/bash).
Reuse limits: <= 4 rows per base module per head; <= 6 per base module overall (module-level memorisation guard).
Yield planning: generate 1.5x candidates per kept row (drop for mismatch, timeout, lint, G13, OUT collision); yield
below 80% of target (2,400 kept) triggers the fix iteration (builder proposal; Opus to confirm in approval).

## 5. Gates

Class legend: PRE-FREEZE KILL = CPU or sandbox execution, data only; POST-TRAINING REPORT = needs a trained model, never a
kill rule. Probe protocol for every PRE-FREEZE probe: 5-fold group cross-validation grouped by base module id; logistic
regression (TF-IDF or hand-built features, fixed regularisation, no tuning on the held-out fold); out-of-fold predictions
pooled; 95% bound from a 2,000-resample cluster bootstrap over base module ids with a fixed seed. Binary bar: AUC <= 0.55
and 95% upper bound <= 0.60. OUT4 (k = 4) bar: accuracy <= 28% and upper bound <= 31% (1/k + 3 pp and + 6 pp).
Each G0-lite value below is fixed before any pilot. A gradient-boosted tree on the same features is run as ADVISORY only
(reported, never a kill).

| Id | Gate | Bar | Class |
|---|---|---|---|
| T42c-K1 | Witness compliance: every kept row has a complete manifest (runs, hashes, versions, image id, step count, domain decl, distinguishing input where NO) | 100% | PRE-FREEZE KILL |
| T42c-K2 | EQV2-YES rule: transform id AND exhaustive-domain run recorded; EQV2-NO rule: distinguishing input recorded | 100% each | PRE-FREEZE KILL |
| T42c-K3 | Two-solver agreement (A witness, B, spec expectation) | 100% of kept rows; block drop > 2% returns block | PRE-FREEZE KILL |
| T42c-K4 | Trace-length bins: each of the three bins holds >= 15% of all rows | >= 15% each | PRE-FREEZE KILL |
| T42c-K5 | Length-only probe (executed steps, lines, tokens, loop count, call count): binary heads | AUC <= 0.55, upper <= 0.60 | PRE-FREEZE KILL |
| T42c-K6 | Length-only probe on OUT4 (option-level features: length, numeric magnitude rank, digit count, type; plus program length) | acc <= 28%, upper <= 31% | PRE-FREEZE KILL |
| T42c-K7 | OUT4 option-surface probe (option text only) and literal-overlap feature (option string appears in source) | acc <= 28%, upper <= 31% | PRE-FREEZE KILL |
| T42c-K8 | EQV2 pair-surface probe (token Jaccard, length ratio, edit distance, AST size delta, changed-line count, rename count). Balanced by design: YES and NO each drawn across similarity quintiles | AUC <= 0.55, upper <= 0.60; YES rate per quintile 40-60% | PRE-FREEZE KILL |
| T42c-K9 | TFAIL2 probes: test-text-only and function-only, plus a "expected literal occurs in function source" flag | each AUC <= 0.55, upper <= 0.60 | PRE-FREEZE KILL |
| T42c-K10 | Balance: YES rate 40-60% (head, language, trace bin); OUT4 letter 25% +/- 3 pp; exception-gold 20-30% | as stated | PRE-FREEZE KILL |
| T42c-K11 | Quotas: pairs >= 30%, invariant >= 15%, near-miss >= 10%; Python <= 75%, JS/TS, Go, bash each >= 8% | as stated | PRE-FREEZE KILL |
| T42c-K12 | Generator lint (clock, randomness, env, order-dependent printing, network, absolute paths): zero violations in kept rows | 100% | PRE-FREEZE KILL |
| T42c-K13 | Dedup: AST-normalised hash duplicate rate across the family (and across T57/T56g modules) | <= 1% | PRE-FREEZE KILL |
| T42c-K14 | Token mean <= 800; 1,536 cap on <= 10%; >= 50 wordings per question form, none above 2% | as stated | PRE-FREEZE KILL |
| T42c-K15 | Names guard: every language, runner, carrier, domain, exception name is on the closed manifest allow-list; seeded namespace with TRAINING salt for every entity string | 0 violations | PRE-FREEZE KILL |
| T42c-K16 | Standard pipeline gates: 200-row G13 pilot (<= 1% hit), A50 G6 at size, A49c, G5-H (two Haiku solvers on 300 rows; one Haiku read of 100% of free-form wording), G3-H, Opus A43(d) | per plan | PRE-FREEZE KILL |
| T42c-K17 | OHS-5 collisions dropped row by row | <= 5% of rows (above 5% = the fix iteration) | PRE-FREEZE KILL |
| T42c-R1 | Accuracy per trace-length bin against base 4B and trivial baselines | report (CI), no bar | POST-TRAINING REPORT |
| T42c-R2 | Accuracy per head and per language against base 4B, random, majority, option-position prior, length-only logistic | report (CI) | POST-TRAINING REPORT |
| T42c-R3 | Invariant-pair consistency (same prediction on both rows) and near-miss discrimination | report (CI) | POST-TRAINING REPORT |
| T42c-R4 | Order-invariance flip rate (OUT4), ECE, Brier, trap-slice ECE | report | POST-TRAINING REPORT |
| T42c-R5 | Public Tier-2 execution-prediction sets (report-only, from L-E; see G13 target names) | report | POST-TRAINING REPORT |

## 6. Clean-room notes

- Written without opening any T42/T43 generator, template or wording pool, mutate.py, OHS-AC, any "ohs"/"sealed" path,
  the v3 plan file itself, the skeptic file, or any benchmark's item text. Read only: PLAN_TRAINING_SIDE.md, LANE_L-C.md,
  excerpts/codeexec_s5.md.
- No item text, example id or name from CRUXEval, LiveCodeBench, REval, CodeMind, CoRE, SWE-Flux, EquiBench,
  CRUXEval-X was used; those are G13 TARGETS only (section 7). Matches are checked by program inside G13 and hit reports
  carry row ids, target name and method only.
- The mutator and transform library are written by the builder from the operator classes in this one-pager and from
  public AST knowledge; the SWE-smith modifier names are a checklist only, and nothing is copied from any existing
  repo mutator.
- Every entity-like string (module, class, field, record, constant string, domain value) is drawn from the seeded random
  namespace with the TRAINING salt. Generic English stems for verbs and nouns inside identifiers are a closed list in the
  manifest (domain vocabulary, not fake entity names).
- No external code or text corpus is used (P0 rule). The manifest records "no external source".
- No data row, example row or generated program appears in this file; operator and transform names are registry ids.

## 7. NAMES the family needs (for the names-only manifest)

- Languages: Python; JavaScript; TypeScript (conditional on self-test); Go; bash.
- Runners / harness names: python interpreter in isolated mode; `node --test` (node:test); `go test`; bash with POSIX
  `[` / `[[` test builtins; instrumented-twin counters (per language); own domain-enumeration harness (per language).
- Sandbox and tool names: od-sbx1; od-sbx-build; gVisor runsc; the executor; own AST mutator; own transform library;
  own instrumenter; exhaustive-domain enumerator.
- Question forms: T42c-Q-OUT4, T42c-Q-EQV2, T42c-Q-TFAIL2 (>= 50 wording ids each).
- Carriers: SRC_FILE, CALL_SPEC, PROGRAM_PAIR, DOMAIN_DECL, TEST_FILE, OPTIONS, QUESTION_FORM.
- Registry ids: EQ-YES-1..5 (rename locals; reorder independent statements; loop/comprehension swap; algebraic identity;
  early-return restructure); mutator operator classes MUT-01..MUT-14 (condition flip; boundary shift; operator swap;
  constant off-by-one; guard removal; argument swap; return alternative; loop bound shift; accumulator init change;
  state-update omission; key/index shift; string-format change; default-value change; early-exit removal); OUT4 distractor
  kinds EXEC-NEARMISS, ARITH-PERTURB, EXC-SIBLING.
- Exception labels (closed per-language lists of language-builtin names; builder fixes the exact list from the pinned
  runtimes' documentation): Python builtin classes (for example the lookup, value, type, zero-division, attribute and
  overflow families); JS builtin error classes; Go and bash use AUTHORED failure markers (a panic with an authored type
  name; an authored `exit` status) because their runtime error text is not version-stable. Custom exception classes are
  allowed in <= 20% of exception rows, named from the seeded namespace.
- Domains (generic application areas; domain rule 3 versus OHS-3/4/5 G is checked by the orchestrator): inventory and
  stock rules; invoice and ledger totals; discount and pricing rules; slot and capacity booking over given integers (no
  clocks); role and rule matching; record deduplication; retry and backoff state machines (no sleeping); text
  templating and field formatting; unit and currency conversion with given tables; pagination and windowing; config
  merging; route and adjacency lookup over given graphs; log-line tallying over given strings; queue and batch
  processing; validation of structured records.
- G13 targets to register before any row (names only): CRUXEval; LiveCodeBench including test-output prediction; REval
  (HumanEval, ClassEval); CodeMind sources (HumanEval, CRUXEval, ClassEval, Avatar); CoRE; SWE-Flux repos; EquiBench
  Python pairs; CRUXEval-X; plus the standing list (OHS-3, OHS-4, OHS-AC, OHS-5 once frozen, public eval targets).

## 8. Risks

1. Equivalence labels are exact only for the declared domain; the prompt must state it and the question must say
   "on every input of the declared domain". A reader might judge unrestricted equivalence; the YES rule (construction +
   exhaustion) keeps both readings aligned for rows kept, but cases where a construction is correct only on a smaller
   domain are dropped by exhaustion (counted).
2. Similarity shortcut in EQV2: YES pairs (rewrites) are naturally less similar than NO pairs (one-token mutants).
   Mitigation: low-similarity NO (restructured program plus a subtle bug) and high-similarity YES (renames) by design,
   stratified by similarity quintile (K8). Biggest generator-complexity risk of the family.
3. Option-surface and "medoid" shortcuts in OUT4 (gold value equals a literal in the source; gold is the option nearest
   to the others). Probes K6/K7 cover them; EXEC-NEARMISS distractors come from real executions.
4. Non-Python exception semantics are not stable across versions (Go, bash): authored markers only; this reduces
   naturalness; kept deliberately.
5. Step counters differ by language (UNVERIFIED comparability). Bins are per language; K4 uses overall rows; a
   per-language bin share under 10% is a warning, not a kill.
6. Sandbox cost: 3 runs per witness plus distractor derivation plus instrumented twin; throughput is a number L-0 owes
   (due Wed 21 Oct). A late sandbox sign-off (target Wed 21, risk line Fri 23 Oct) squeezes the 25 Oct to 2 Nov window.
7. Wide overlap with public execution-prediction sets by accident (short programs, common idioms); G13 pilot and the
   application-style rule are the control; "textbook algorithm" generators are not built.
8. TypeScript path depends on Node 24 type stripping in the sandbox image (UNVERIFIED); fallback folds TS into JS.
9. Bash rows are the least natural application code; keep bash modules to small text and counter pipelines.

## 9. The one fix iteration and the kill rule

- One fix iteration per family, shared by every gate. Pilot-stage tuning of generator parameters on the 1,000-row pilot
  (CPU gates K1-K15 are run on the pilot FIRST, before the G13 pilot is queued) is development and is logged; after the
  200-row G13 pilot every change consumes the fix iteration. (Interpretation, for Opus to confirm.) A G13 pilot with
  > 1% hits IS the fix iteration (plan rule); scaffolding-only hits and <= 5% OHS-5 collisions are not.
- Allowed fix levers: re-stratify and regenerate failing blocks (similarity quintile, trace bin, language); swap the
  distractor generator; tighten the lint; replace a failing non-Python language block with more Python while keeping the
  >= 25% non-Python rule only if the language itself is proven impossible (otherwise the family reports the shortfall);
  never relax a bar.
- Kill rule: failing any PRE-FREEZE KILL gate after the fix iteration, or not through all of them at the data freeze
  (Mon 2 Nov 23:59 UTC), rolls T42c to C2.2/C3 with the failing gate and numbers logged. POST-TRAINING lines are never
  kill rules. Plan floor reminder: at least one of T42c/T57 must pass.
- Order inside L-C (builder proposal): T42c first (simplest executor use), T57 second (mutation pilot on Sun 25 Oct),
  T56g third.

## 10. Items for Opus to confirm at approval

(a) 3-runs witness for OUT4 overrides the sandbox default of 2. (b) Step-counter definition per language. (c) Yield
floor of 80%. (d) Pilot-stage tuning versus the single fix iteration. (e) Exception labels for Go and bash as authored
markers. (f) GBT advisory probes are report-only.

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

### T42c CODE-EXEC: APPROVE

Rulings: (a) 3 identical runs for OUT4 and TFAIL2 witnesses override the sandbox default (the plan's witness rule wins).
(b) the per-language step counters are approved; the 10% Python agreement check on 100 programs is a CPU/sandbox test that
must pass before any row. (c) the yield floor (< 80% kept triggers the fix iteration) is approved. (d) see G3: not
approved as written; section 9 is rewritten to G3. (e) authored failure markers for Go and bash are approved. (f) GBT
probes are advisory (G5).
Note: the exact toolchain patch versions and image digests from the L-0 image record are appended to this G0-lite (and
to T57 and T56g) before the first non-Python row (plan section 2: "pins go into the G0-lites before any non-Python row").
