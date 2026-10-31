# G0-LITE: T56 DONE-CLAIM, done-claim half (2,000 rows; the test-gaming half T56g is lane L-C's)

Status: DRAFT by Sonnet 5.5 (high), Sun 18 Oct 2026, for Opus G0-lite approval Mon 19 Oct. Design only: no rows, no generator run,
no data, no model call, no code executed. Numeric bars are written before any pilot. Angle brackets are placeholders.
Sources read: PLAN_TRAINING_SIDE.md (sections 1 B.7, 1 E, 2, 5, 8), LANE_L-T.md, excerpts/tools_s5.md (stripped).
Scope boundary: T56g (HACK vs honest fix, transform library, held-out suite execution) is NOT in this file. T56 counts as passed for the
training floor when this done-claim half passes.

## 0. One-line purpose

An agent says it is finished. Decide from the task, the agent's tool calls and the tool outputs whether to accept the claim (DONE) or
send the agent back (CONTINUE), say why, and judge whether the work is ready to commit or open a pull request. Motivation: premature
stopping and unsupported success claims are a measured agent failure mode.

## 1. Decision and label set

Primary decision (every row): DONE vs CONTINUE (binary readout; two lettered options, order shuffled; 20% extra non-identity copies at
mix time, which for two options equals reversal, not counted).
Sub-block D4 uses READY vs NOT_READY (the commit/PR gate) with the same binary shape.
Reason head (second head, trained on CONTINUE/NOT_READY rows; 8 classes + `none` on DONE):
`unmet_criterion`, `short_coverage`, `stale_evidence`, `wrong_target`, `ledger_mismatch`, `dead_or_demo_only`, `unverified`, `stray_change`.
Output to the product: DONE/CONTINUE plus reason.

Class definitions (own wording):
- DONE: every acceptance criterion stated in the task is satisfied AND the visible evidence in the trajectory shows it.
- CONTINUE with reason: unmet_criterion (a criterion is visibly unmet); short_coverage (the check ran fewer items than the criterion
  requires, or skipped some); stale_evidence (the passing check ran before the last change to the thing it checks); wrong_target (the
  check ran against something other than the deliverable); ledger_mismatch (an effect is duplicated or missing in the ledger);
  dead_or_demo_only (the behaviour exists only in a path the shipped entrypoint does not reach); unverified (no check was run; claim
  rests on assertion); stray_change (D4: files or changes outside the declared scope are present).

## 2. Inputs and state model

INPUT VIEW. Primary = task statement (with acceptance criteria written in prose) + the agent's tool calls + the relevant tool OUTPUTS
(capped at 256 tokens each; at most the last 6 tool turns) + the agent's closing claim. T56 is a "done row": per the plan it sees the
relevant tool outputs; the variant with outputs stripped is NOT built (claim vs evidence needs the outputs). The T41c taint rules apply to
outputs: they are rendered from a data-field grammar with no imperative or second-person text (CPU lint P-13).

SIMULATED ENVIRONMENT (no code execution for gold in the main path):
- Stores: typed key-value stores, counters, a ledger of effects (with keys), file trees with revision stamps (`rev`), a working-tree
  state (tracked-modified, untracked, staged) for D4, and a symbolic module graph (D3: modules, imports, entrypoint, flags, reachability).
- Tools (engine-generated, names from the namespace): mutating ops, read ops, a `check` op that evaluates a declared subset of predicates
  and prints a summary (counts + per-item lines) in one of several output styles (section 8), a `ledger` read op, a `status`/`diff` op for D4.
- Acceptance predicates are a closed library: `exists`, `absent`, `equals`, `count_eq`, `exactly_once`, `status_is`, `unchanged`,
  `reachable` (D3). The task states them in prose; the engine knows them as predicates.
- TRAJECTORY: a plan DAG (tool_engine.dag) is executed by the engine; a FAULT from the manifest (section 3.1) is injected; every output is
  rendered from the resulting environment state; `rev` stamps give order information inside outputs only.
- EVIDENCE-SUFFICIENCY INVARIANT: the visible trajectory must entail the status (met / unmet / unknown) of every acceptance predicate.
  Hidden truth never decides a label that evidence cannot show. This is checked by solver B (section 3.3).
- Stage stratification (analogy only; the cited work studies progress reports): stage = number of required predicates in the task:
  early 1-2, mid 3-4, finish 5+. Each stage holds 30-37% of every sub-block.
- Claims: a pool of closing-claim wordings (>= 50, reworded by Haiku medium under slot round trip), each used with both labels.

## 3. Gold method

### 3.1 Fault manifest (the perturbations that make CONTINUE rows)
| Fault id | Reason class | How it appears (only in tool outputs unless noted) |
|---|---|---|
| `f_unmet` | unmet_criterion | the `check` output shows an unmet item among those the task lists |
| `f_count_short` | short_coverage | the `check` summary count is lower than the number of items the criterion lists |
| `f_skipped` | short_coverage | a declared item is reported skipped/not run |
| `f_stale_run` | stale_evidence | the check's `rev` stamp is older than the last mutation's `rev` for the checked thing |
| `f_wrong_target` | wrong_target | the check output names a different target than the deliverable |
| `f_ledger_dup` | ledger_mismatch | the ledger read shows the effect twice |
| `f_ledger_missing` | ledger_mismatch | the ledger read shows the effect absent while the agent claims it |
| `f_demo_only` | dead_or_demo_only | the module graph shows the tested behaviour is not reachable from the declared entrypoint (variants: import not wired, flag default off, unreachable branch, helper never called) |
| `f_no_check` | unverified | the trajectory has no check/verification call (D5 only) |
| `f_stray` | stray_change | D4: working-tree state shows an untracked or modified path outside the declared scope |
| `f_stale_final` | stale_evidence | D4: the last full check precedes the last edit |
| `f_failing_prior` | unmet_criterion | D4: a previously passing item now fails in the last full check |
| `f_none` | none | DONE row: every predicate met, evidence fresh, targeted, complete |
HARD BIN (>= 40% of CONTINUE rows): faults whose signal is a RELATION (count vs listed items, rev order, target name vs deliverable,
ledger count vs claim) rather than a keyword such as a failure word. Easy bin: a literal failing item. Every DONE row also carries
distractor oddities (a warning line, a skipped optional item, a long output) so "unusual output" is not a cue.

### 3.2 Gold
- Label = function of the environment state and the visible evidence: DONE iff all predicates are met AND (for each) the evidence is
  present, fresh (check rev >= last mutation rev of the checked thing), on the right target, and complete (count equals listed items).
  Otherwise CONTINUE with the reason of the first failing condition in the fixed precedence `unverified` > `unmet_criterion` >
  `wrong_target` > `stale_evidence` > `short_coverage` > `ledger_mismatch` > `dead_or_demo_only`; each CONTINUE row injects exactly one
  fault (single reason), so precedence only matters for the validation of mixed cases, which are not generated in P0.
- D4 READY iff all of: acceptance predicates met with fresh targeted complete evidence; no untracked or modified path outside the
  declared scope; the last full check follows the last edit and passes. NOT_READY reason by the same precedence with `stray_change` after
  `stale_evidence`.
- MATCHED PAIRS. In a pair the closing-claim text is byte-identical in the true and false rows, the task statement is identical, the
  tool-call skeleton (names and arguments) is identical, and the difference lives ONLY in tool outputs. One declared exception: D5 pairs
  differ by the existence of a verification call and its output (claim text still identical).
- Haiku only rewords the task statement and the claim pool entry under slot round trip; labels and outputs are program-made.

### 3.3 Solver A vs independent solver B
- Solver A (builder, Sonnet high): the gold function over the HIDDEN environment state: it re-evaluates every acceptance predicate on the
  final simulated state (this is the "hidden acceptance tests executed" step, done by the program), plus freshness and coverage from state.
- Solver B (separate Sonnet high session, written from THIS FILE only): a VISIBLE-EVIDENCE-ONLY evaluator. It parses the rendered
  task, calls, outputs and claim (deterministic parser, no model) and decides DONE/CONTINUE plus reason from the text alone, never seeing
  the hidden state. Agreement of A (hidden truth) and B (visible evidence) enforces the evidence-sufficiency invariant. Rows with A != B
  are dropped and logged; pilot disagreement above 1.0% = spec/renderer ambiguity = the fix iteration.
- Optional execution validation (CONDITIONAL): D3's symbolic reachability gold can be cross-checked by running a small Python-only
  slice in the disposable sandbox ONLY after the L-0 executor self-test passes and Opus signs it off; mismatches are dropped and
  counted. If the sandbox is not available, D3 ships on symbolic gold alone and the report says "symbolic gold, no execution check".
  No generated code is executed by this file or by the lane before that sign-off.

## 4. Sizes and shares

Total 2,000 rows (done-claim half). DONE share 50% overall (target 1,000 DONE / 1,000 CONTINUE-or-NOT_READY).
| Sub-block | Rows | Share | Label mix | CONTINUE reason mix | Pair rows |
|---|---|---|---|---|---|
| D1 EVIDENCE | 900 | 45.0% | DONE 450 / CONTINUE 450 | unmet_criterion 120, short_coverage 165, stale_evidence 90, wrong_target 75 | 80% |
| D2 LEDGER-MISMATCH | 350 | 17.5% | DONE 175 / CONTINUE 175 | ledger_mismatch (dup 90, missing 85) | 100% |
| D3 DEMO-ONLY / DEAD-CODE | 250 | 12.5% | DONE 125 / CONTINUE 125 | dead_or_demo_only (4 variants about 31 each) | 100% |
| D4 COMMIT/PR READY | 300 | 15.0% | READY 150 / NOT_READY 150 | stray_change 75, stale_evidence 35, unmet_criterion 40 | 80% |
| D5 UNVERIFIED pairs | 200 (100 pairs) | 10.0% | DONE 100 / CONTINUE 100 | unverified 100 | 100% |
Family minimal pairs >= 60% required for T56 (design ~90%; plan floor 30%). Per-sub-block DONE share 45-55%.
Languages: the rendered text of D3 uses file-extension and import-syntax tags for python 40%, javascript 20%, go 20%, bash 20% (non-
Python 60%); D1, D2, D4 are language-neutral. D3 is the only subfamily with code-shaped content and is symbolic (no bodies shown).
Token budget: mean <= 800; max 1,536 on <= 10% of rows; > 1,024 on <= 10% (reading to be confirmed by Opus).
Wordings: >= 50 claim wordings and >= 50 per question form; no wording > 2% of the family; each claim wording has 40-60% DONE share when
used >= 20 times.

## 5. Gates

Bars: binary probes pass at held-out AUC <= 0.55 with 95% upper bound <= 0.60; k-way probes at balanced accuracy <= 1/k + 3 pp with
bound <= 1/k + 6 pp (reason head k = 8: <= 15.5% / <= 18.5% on CONTINUE rows). Protocol: grouped split by pair id and scenario-template id,
80/20, five repeats, 2,000-resample cluster bootstrap 97.5th percentile as the bound; TF-IDF (1-2 grams, min_df 3) + L2 logistic regression.

### 5.1 PRE-FREEZE KILL gates (CPU, data only)
| ID | Gate | Bar |
|---|---|---|
| P-1 | Solver A (hidden truth) vs B (visible evidence only) agreement, pilot and full | 100% target; A != B dropped; pilot disagreement > 1.0% = fix iteration |
| P-2 | Sizes, label mixes, reason mixes, DONE shares | within +-2 pp (family) / +-3 pp (mix); DONE 45-55% per sub-block |
| P-3 | CLAIM TEXT IDENTICAL across true/false pairs: byte-identical closing claim, task statement, call skeleton in 100% of pairs (D5: claim and task only) | 100% |
| P-4 | CLAIM-ONLY probe: TF-IDF + LR on the closing-claim text alone -> DONE vs CONTINUE (binary), pooled and per sub-block | AUC <= 0.55, bound <= 0.60 |
| P-5 | Task-text-only probe (task statement + criteria, no outputs, no claim) -> label (binary) | AUC <= 0.55, bound <= 0.60 |
| P-6 | Structure-only probe (token length, number of calls, number of output lines, output length, stage, wording id, template id, option letter) -> label | binary AUC <= 0.55 / bound <= 0.60 |
| P-7 | Reason-head probe on claim text + task text only (no outputs) -> reason (8-way on CONTINUE rows) | balanced acc <= 15.5% / bound <= 18.5% |
| P-8 | Hard-bin share and keyword control: outputs-only TF-IDF probe on the HARD BIN only (CONTINUE hard rows vs matched DONE rows) | PROPOSED ADD (Opus to confirm): AUC <= 0.65 on the hard bin (relation faults must not be readable from keywords) |
| P-9 | Wording: per-claim DONE share 40-60% (wordings with >= 20 uses); >= 50 wordings; none > 2% | pass |
| P-10 | Stage stratification: each stage 30-37% within each sub-block; DONE share 40-60% within each stage | pass |
| P-11 | Evidence-sufficiency assertion (solver B recovers status of every predicate) | 100% of kept rows |
| P-12 | Fault coverage: each fault id >= 5% of its sub-block's CONTINUE rows; hard bin >= 40% of CONTINUE rows | pass |
| P-13 | Output lint: no imperative or second-person clause in rendered outputs | 0 violations |
| P-14 | Token budget | mean <= 800; max <= 1,536; > 1,024 on <= 10% |
| P-15 | Haiku reword slot round trip (counts, rev numbers, targets, predicate names, negations) | 100% else drop-only |
| P-16 | Name guard: 100% of names (tools, entities, modules, runners, languages, carriers) on the frozen allow-list; 0 exact G13 target strings | 0 violations |
| P-17 | 200-row G13 pilot (orchestrator, serial on the Mac) | <= 1% hit; scaffolding-only hits exempt |
| P-18 | Collisions with frozen OHS-5 | dropped row by row; <= 5% not the fix iteration |
| P-19 | Gold-letter share (two options) | 50% +-3 pp |
| P-20 | D3 only: module-graph reachability gold equals an independent graph search (BFS vs DFS) on 100% of rows; if the sandbox slice runs, symbolic vs executed agreement | 100% / 100% of the executed slice (mismatches dropped, > 2% = fix iteration) |

Standard pipeline gates (A50 G6, A49c, G5-H, G3-H): orchestrator-run, not redefined; FLAG FOR OPUS identical to T54 (Haiku-read data audits).

### 5.2 POST-TRAINING REPORT (never a kill rule)
| ID | Report line |
|---|---|
| R-1 | Accuracy per sub-block and per stage (early/mid/finish) with Wilson CI beside baselines: always-DONE, always-CONTINUE, failure-keyword regex on outputs, claim-only TF-IDF (trained on the train split), random, base 4B |
| R-2 | False-DONE rate (accept where gold CONTINUE) and over-CONTINUE rate (reject where gold DONE), separate, per reason class |
| R-3 | Reason-head accuracy per class with confusion matrix |
| R-4 | Easy-bin vs hard-bin accuracy |
| R-5 | The claim-only probe score vs the trained model on the validation split (the shortcut-margin check from the research note, reported) |
| R-6 | Flip rate under option permutation; ECE, Brier, trap-slice ECE |

## 6. Clean-room notes

- Not built from any benchmark item. Ideas only: trajectory-level false-success research (claim-text vs evidence), ledger mismatch (LIMBO
  as T55), demo-only/dead-code (an observation from agents seeing an oracle; n is small, so D3 is 12.5% of the family and flagged weak).
- Names: every tool, entity, module, symbol and store name from the seeded namespace with the TRAINING salt; no hand-picked fake names.
  Languages and runners are the only real names (section 8), each on the allow-list.
- Runner output styles are rendered by our own formatter, modelled on the structure of a summary line plus per-item lines; no output text
  is copied from any runner documentation or benchmark; style ids in section 8.
- Haiku rewords only. No LLM writes labels or outputs.
- No external source in P0.
- Builder never opens any T27, T40-T46 generator, template, wording pool or OHS-AC; T56g files belong to lane L-C and are not read.

## 7. Risks

1. Text shortcut in outputs: failure words ("failed", "error") make easy rows trivial. Mitigation: hard bin >= 40%, distractor oddities on
   DONE rows, P-8 proposal.
2. Evidence-sufficiency may make rows too clean: a real harness sees partial evidence. The unverified/short-coverage classes cover part
   of it; C2.2 can add partial-evidence rows.
3. D5's pair differs by a call, which breaks "difference only in outputs"; declared exception; claim text still identical.
4. D3 is symbolic: a real executable repo may behave differently; optional execution validation is conditional on the sandbox.
5. Stage stratification evidence is an analogy only; reported, not claimed.
6. Reason head has 8 classes with some tiny ones (about 30 per D3 variant); per-class recall reported; no reason-head kill gate.
7. Hand-off boundary with T56g: this family never contains diffs of tests or test-gaming; a DONE row never includes a modified test file.
8. Precedence conflicts if two faults ever co-occur: P0 generates single faults only.
9. D4 stray_change depends on the declared scope statement being visible; observability checked by solver B.

## 8. NAMES (names only; for the names-only manifest)

Namespace: `ns.train` (TRAINING salt, value held by L-0), kinds `ns.noun.entity`, `ns.noun.field`, `ns.noun.module`, `ns.noun.symbol`,
`ns.noun.path_segment`; per-family bucket `bucket.t56`; each noun reused in at most 3 scenarios.
- Policy / acceptance cards (4): `card.t56.evidence_required`, `card.t56.fresh_run_required`, `card.t56.scope_declared`, `card.t56.entrypoint_reach`.
- Domain archetypes (10): `arch.records`, `arch.schedule`, `arch.messages`, `arch.files`, `arch.jobs`, `arch.inventory`, `arch.accounts`,
  `arch.tickets`, `arch.queue`, `arch.catalogue`.
- Tool verbs (closed list, 24): `get`, `list`, `read`, `check`, `count`, `verify`, `create`, `add`, `update`, `set`, `remove`, `delete`, `move`,
  `rename`, `send`, `export`, `sync`, `status`, `diff`, `ledger`, `commit`, `stage`, `run`, `inspect`. Surface tool name = `<verb>_<ns.noun.entity>`.
- Languages and runners (D3 rendering only): languages `python`, `javascript`, `go`, `bash`; runners `pytest` (python), `node:test` (Node 24 LTS
  built-in), `go test` (Go 1.26), `plain script exit status` (bash; no external runner). Toolchain pins follow the plan (Python 3.12.x exact patch,
  Node 24.x, Go 1.26.x). Rendered by own formatter; no execution on this path.
- Output styles (own formatters): `fmt.summary_counts`, `fmt.per_item_lines`, `fmt.ledger_rows`, `fmt.tree_status`, `fmt.module_graph`.
- Predicate library ids: `exists`, `absent`, `equals`, `count_eq`, `exactly_once`, `status_is`, `unchanged`, `reachable`.
- Fault ids: `f_unmet`, `f_count_short`, `f_skipped`, `f_stale_run`, `f_wrong_target`, `f_ledger_dup`, `f_ledger_missing`, `f_demo_only`, `f_no_check`,
  `f_stray`, `f_stale_final`, `f_failing_prior`, `f_none`. Reason ids: as section 1.
- Carriers: `carrier.task_statement`, `carrier.tool_output_check`, `carrier.tool_output_ledger`, `carrier.tool_output_tree`, `carrier.closing_claim`.
- View tag: `view.with_outputs`. Sub-block ids: `d1_evidence`, `d2_ledger`, `d3_demo_only`, `d4_ready`, `d5_unverified`.
- External sources: none.

## 9. The one fix iteration and kill rule

- One family-level fix iteration (Opus rules first), triggered by ANY failed PRE-FREEZE gate (5.1) on pilot or full generation, or a G13 pilot
  above 1%. Pre-declared menu: P-4/P-5/P-6 fail -> re-balance claim wording and task text by template (claim pool per label) and regenerate;
  P-7 fail -> remove reason-leaking phrases from the task template; P-8 fail -> move more faults to relation-only rendering; P-1/P-11 fail -> Opus
  rules the renderer/spec ambiguity; P-20 fail -> fix the graph model; P-17 fail -> generator change (row ids and method only).
- After the fix: rerun all PRE-FREEZE gates on a fresh 1,000-row pilot with new seeds. Any failure, or not through all gates by the DATA FREEZE
  (Mon 2 Nov 23:59 UTC), rolls the done-claim half to C2.2/C3 with the failing gate and numbers logged. Floor effect: T56 counts as passed when this
  half passes; if only T56g fails, only the test-gaming head rolls.
- POST-TRAINING lines never kill.
- Open question for Opus: drop-only sub-block alternative (as T54); default strict.

## 10. Items for Opus approval (checklist)

1. Evidence-sufficiency invariant and the hidden-truth vs visible-evidence solver design. 2. Fault precedence and single-fault generation.
3. D5 exception to the outputs-only difference. 4. P-8 proposed hard-bin keyword gate. 5. Optional execution validation conditional on the
sandbox sign-off. 6. Reason head with 8 classes. 7. Pair share >= 60% for this family. 8. Probe protocol and the G5-H/G3-H flag. 9. Token reading.


## Opus rulings 18 Oct (appended by the L-T builder from families/G0_APPROVALS.md, word for word; the build skeptic checks the code against this addendum; where the body text above says otherwise, this addendum binds)

### Round 1 decision for this family (verbatim)

### T56 DONE-CLAIM (done-claim half): APPROVE

Rulings: 1 the evidence-sufficiency invariant and the hidden-truth A vs visible-evidence B design are approved (a strong
design). 2 single-fault generation with the fixed precedence is approved. 3 the D5 exception is approved (the claim text
is still byte-identical). 4 P-8 is adopted as a PRE-FREEZE KILL gate: the outputs-only probe on the hard bin passes at AUC
<= 0.65 AND upper bound <= 0.70 (a sanity bar that relation faults are not keyword-readable, not a near-chance bar). 5
the optional D3 sandbox check is approved only after the L-0 sandbox sign-off. 6 the reason head follows G7 (head rows),
P-7 stays a kill gate, and per-class recall is report-only. 7 pairs >= 60% is approved. 8-9 see G5, G2, G6.

### Round 2 (verbatim lines that concern this family)

| T54, T55, T56, T56g, T42c, T57, GEN, VOICE | APPROVE (round 1 stands) | n/a | none new; the round-1 addendum is NOT yet in any of the 8 files (see below) |

- All 8: "Solver B = separate Sonnet high session" means CODE written by that session (G1).
- T56: the section 9 drop-only question is not adopted (G4). P-8 is a PRE-FREEZE KILL gate.

### Global rulings that bind every family (verbatim)

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
