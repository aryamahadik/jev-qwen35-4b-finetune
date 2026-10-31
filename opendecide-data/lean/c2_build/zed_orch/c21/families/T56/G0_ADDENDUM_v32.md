# G0 ADDENDUM v3.2: T56 DONE-CLAIM, done-claim half (lane L-T; the test-gaming half T56g is lane L-C's and is not touched)

Status: DRAFT by Sonnet 5.5 (high), Sun 18 Oct 2026, for Opus batch 1 approval Mon 19 Oct. Design only: no rows, no code run, no data,
no model call, no Modal, no generated code executed. Every numeric bar is written BEFORE any pilot and is fixed once Opus approves.
Precedence: G0_LITE.md body < "Opus rulings 18 Oct" block at its end < THIS addendum (this file binds where it differs).
PART S (the lever library shared by T54, T55, T56: held-out draw, wrappers, perturbation, long-input slice, observation formats, ladder
protocol, stamp flow, exports) is in families/T54/G0_ADDENDUM_v32.md and is incorporated here by reference; the build skeptic and the
conformance writer read all three addenda. This file states what is specific to T56.
Sources read: C2_1_BUILD_ORDER.md (L-T block, v3.2 additions), C2_1_PLAN_v3.md sections 1, 2, 5, 6, 7, 8, PRE-REGISTERED RULES block,
16; C2_1_EXTRA_LEVERS.md (ADOPT NOW A7, A10, A12, A14, A16; A24 held-out rule); T56 G0_LITE.md; families/G0_APPROVALS.md; stripped
tools_s5.md; l0/NAMES_MANIFEST_V1.json (names only). NOT opened: research_v4/hardest.md, any ohs/sealed path, T27 / T40-T46 generators,
T56g files (lane L-C), any benchmark item text. Runner output is rendered by our own formatter; nothing is copied from a runner manual.

## 0. What this addendum changes, in one table

| Item | Source | Change for T56 | Kind |
|---|---|---|---|
| A7 verification-relevance near-misses | LEV A7 | new sub-block D6, 400 rows (200 pairs), five output-only faults | PRE-FREEZE KILL (data) |
| Alarming/calm x risk-present/resolved quad | plan 1 E (mandatory for T56) | four cells over D1, D2, D4, D6 (1,600 rows) | PRE-FREEZE KILL |
| A16 observation-format perturbation | LEV A16 | 40% of rows (about 800) in non-default formats, 0 extra rows, 1 format held out | PRE-FREEZE KILL |
| A12 character perturbation | LEV A12 | 200 rows by substitution on task statement + claim; transform families held out as dev-only | PRE-FREEZE KILL; held-out POST-TRAINING |
| A10 cue-invariance wrappers | LEV A10 | up to 100 rows, ONLY if the Fri 23 probe says build | PROOF-BEFORE-USE |
| A14 long-input slice | LEV A14 | up to 100 rows (5%), ONLY if the probe says build (GV3); G6 binds, no exemption (GV4): rows 1,100-1,536 tokens [Opus b1] | PROOF-BEFORE-USE |
| Difficulty ladder | plan 1 E, CRIT D1, D2 | mechanisms m.t56.*, L1-L4, >= 25% at L3-L4, twin rule, C2 <= 70% on L4 | PRE-FREEZE FIX-TRIGGER |
| Check at generation | OWNER-ROW, plan 16.1 | every row answer-checked and G13-stamped when made; P-17 replaced | PRE-FREEZE KILL |
Family size: T56 done-claim half stays 2,000 rows; every lever is a substitution. Kill granularity unchanged (G4): this half is killed or
kept whole; T56 counts as passed for the floor when this half passes (T56g is L-C's).

## 1. Binding conditions carried (word for word from G0_APPROVALS.md)

T56 round 1: "Rulings: 1 the evidence-sufficiency invariant and the hidden-truth A vs visible-evidence B design are approved (a strong
design). 2 single-fault generation with the fixed precedence is approved. 3 the D5 exception is approved (the claim text
is still byte-identical). 4 P-8 is adopted as a PRE-FREEZE KILL gate: the outputs-only probe on the hard bin passes at AUC
<= 0.65 AND upper bound <= 0.70 (a sanity bar that relation faults are not keyword-readable, not a near-chance bar). 5
the optional D3 sandbox check is approved only after the L-0 sandbox sign-off. 6 the reason head follows G7 (head rows),
P-7 stays a kill gate, and per-class recall is report-only. 7 pairs >= 60% is approved. 8-9 see G5, G2, G6."
Round 2: "T56: the section 9 drop-only question is not adopted (G4). P-8 is a PRE-FREEZE KILL gate." "All 8: 'Solver B = separate Sonnet
high session' means CODE written by that session (G1)." Global rulings G1-G10 bind unchanged.

CLAUSE LIST for the ruling-to-code conformance record (plan 16.1 step 0; fresh Sonnet high maps, Opus signs; proposed test ids)
| Clause | Text (short) | Test |
|---|---|---|
| Rl-1 | A (hidden truth) vs B (visible evidence only) agreement; evidence-sufficiency invariant | [t56_rl1_a_vs_b_invariant] |
| Rl-2 | single-fault generation; fixed precedence unverified > unmet_criterion > wrong_target > stale_evidence > short_coverage > ledger_mismatch > dead_or_demo_only, with stray_change after stale_evidence for D4 | [t56_rl2_precedence] |
| Rl-3 | D5 is the ONLY pair that may differ by the existence of a verification call; claim text byte-identical | [t56_rl3_d5_exception] |
| Rl-4 | P-8 kill gate: outputs-only probe on the hard bin, AUC <= 0.65 and bound <= 0.70 | [t56_rl4_p8] |
| Rl-5 | D3 execution cross-check only after sandbox sign-off | [t56_rl5_d3_exec_gate] |
| Rl-6 | reason head as head rows (G7), P-7 kill gate, per-class recall report-only | [t56_rl6_head_rows] |
| Rl-7 | pairs >= 60% of the family | [t56_rl7_pair_share] |
| G1 | solver B = code written from G0-lite + addendum | [t56_solverB_independent] |
| G3 | no pilot tuning; ONE combined fix | [t56_fix_log_single_iteration] |
| G5 | one probe harness; permutation and injected-leak sanity checks | [t56_probe_harness_sanity] |
| G6 | mean <= 800; none > 1,536; > 1,024 on <= 10% (A14: T54 addendum 11.1) | [t56_token_rule_g6] |
| G10 | decision_spans with roles; wrapper_spans separate | [t56_decision_spans_roles] |
| E1-E6 | the section 3 evidence conditions (A and B implement them identically) | [t56_e1_e6_truth_table] |
| V32-1..V32-15 | the new gates in section 7 | [t56_p32_*] |
Part S clauses S.2-S.9 as in the T54 addendum.

## 2. Sizes by substitution (the family stays 2,000; DONE / READY 1,000 and CONTINUE / NOT_READY 1,000)

D6 is a new sub-block; its 400 rows are taken from D1 (-250), D2 (-50), D4 (-50) and D5 (-50) of the body (section 4). Everything else is
unchanged in kind. Reason mixes scale with their sub-block.
| Sub-block | Rows | Share | Label mix | CONTINUE / NOT_READY reason mix | Pairs |
|---|---|---|---|---|---|
| D1 EVIDENCE | 650 | 32.5% | DONE 325 / CONTINUE 325 | unmet_criterion 87, short_coverage 119, stale_evidence 65, wrong_target 54 | 80% |
| D2 LEDGER-MISMATCH | 300 | 15.0% | DONE 150 / CONTINUE 150 | ledger_mismatch: dup 77, missing 73 | 100% |
| D3 DEMO-ONLY / DEAD-CODE | 250 | 12.5% | DONE 125 / CONTINUE 125 | dead_or_demo_only: four variants 31 / 31 / 31 / 32 | 100% |
| D4 COMMIT/PR READY | 250 | 12.5% | READY 125 / NOT_READY 125 | stray_change 63, stale_evidence 29, unmet_criterion 33 | 80% |
| D5 UNVERIFIED pairs | 150 (75 pairs) | 7.5% | DONE 75 / CONTINUE 75 | unverified 75 | 100% |
| D6 VERIFY-RELEVANCE (lever A7) | 400 (200 pairs) | 20.0% | DONE 200 / CONTINUE 200 | short_coverage 130 (f_zero_collected 45, f_filter_excl 45, f_toplevel_only 40), unverified 40 (f_exit_masked), wrong_target 30 (f_unrelated_tests) | 100% |
| Total | 2,000 | 100% | 1,000 / 1,000 | | >= 60% required (design about 91%) |
Lever quotas (exclusive lever_tag per row, S.1; D6 rows are the `lever.a7` rows; A16 stacks):
| Sub-block | A12 perturbed | A10 wrapped (cond.) | A14 long (cond.) | Plain rows (all levers built) |
|---|---|---|---|---|
| D1 | 100 | 50 | 40 | 460 |
| D2 | 40 | 20 | 30 | 210 |
| D3 | 0 | 0 | 0 | 250 |
| D4 | 40 | 20 | 30 | 160 |
| D5 | 20 | 10 | 0 | 120 |
| D6 | 0 | 0 | 0 | 0 (400 are a7) |
| Total | 200 (10%) | 100 (5%) | 100 (5%) | 1,200 (+ 400 a7 = 2,000) |
D3 takes no perturbation, wrapper or long view (it is symbolic and code-shaped). If the Fri 23 probe says do not build A10 / A14, the
quotas revert to plain rows. DONE share per sub-block stays 45-55%; stage strata 30-37% per sub-block (D6 included); languages for the
runner-style rendering of D3 and D6 are python 40 / javascript 20 / go 20 / bash 20 (non-Python 60%), D1, D2, D4, D5 language-neutral.
Dev-only held-out rows (S.2) are extra and outside the 2,000: 80 rows (4%): wrapper 20, transform 20, format 20, layout 20 (wrapper and
layout only if A10 / A14 are built). They are never in the mix manifest.

## 3. A7 verification-relevance near-misses (sub-block D6)

Idea: a check can run and still prove nothing about the claim (EXTRA_LEVERS A7: zero tests collected, a filter that skips the changed
module, an exit code masked by a pipe, only top-level names listed, an unrelated test file run). All rows are program-built, gold from a
SYMBOLIC run simulator (module tool_engine.runsim: modules with named items and pass / fail / skip states, a selection filter, a pipe
window, a revision counter); nothing is executed ("symbolic gold, no execution check" is printed in the report for D6).
3.1 Faults (all differences live in tool OUTPUTS; task statement, closing claim and call skeleton are byte-identical in each pair):
| Fault id | Reason (no new class) | Visible signal in the output (a RELATION; f_filter_excl, f_toplevel_only, f_exit_masked and f_unrelated_tests are HARD BIN; f_zero_collected is a LITERAL-value fault and is NOT in the hard bin [Opus b1 T56-M1]) | DONE twin |
|---|---|---|---|
| f_zero_collected | short_coverage | `collected` = 0 (no per-item lines, passed = failed = 0, exit = 0) while the task's criterion lists L > 0 items | `collected` = L, all pass |
| f_filter_excl | short_coverage | the `selected` module list does not contain the module that the earlier mutation calls changed | the changed module is in the list |
| f_toplevel_only | short_coverage | the `listing` shows top-level names only while the criterion enumerates nested items | nested items listed |
| f_exit_masked | unverified | both calls pipe the run through a tail window (`prog.tail`, K lines) and print the LAST stage's `exit` = 0; in the fault row the run has more than K lines, so the summary line (first line in `fmt.summary_first`) is cut off and no status is visible | the run has exactly K lines, so the summary is inside the window |
| f_unrelated_tests | wrong_target | the output `target` differs from the deliverable's test target by one path segment or one namespace-noun suffix (a near miss; D1's wrong_target uses unrelated entities) | correct target |
f_exit_masked is output-only through a WORLD PROPERTY: the module's item count n differs between the pair members (n + 1 > K vs n + 1 = K),
the task statement states no count in these pairs, and K and the pipe are identical in both calls. Only line-preserving formats
(obsfmt.plain_kv, .crlf_tab, .ansi) are applied to f_exit_masked rows, because the window is defined on the plain line structure.
`fmt.summary_first` is used by both members of every f_exit_masked pair AND by 50% of D6 rows overall and 25% of all other T56 rows, so
neither the layout nor the pipe is tied to a label (gate V32-3).
3.2 Gold v3.2 (extends the body's rule; the approved precedence is UNCHANGED). A row is DONE iff every acceptance predicate is met AND, for
each predicate's evidence E:
 E1 present: a verifying call exists (else `unverified`; D5).
 E2 attributable: the run's summary status is visible; if the call contains a pipe stage and the summary line is absent from the visible
    window, the status is unknown (else `unverified`). An exit status read after a pipe is not evidence.
 E3 on target: E.target equals the deliverable's target, near misses included (else `wrong_target`).
 E4 fresh: check rev >= last mutation rev of the checked thing (else `stale_evidence`).
 E5 covers: the selected module set contains the changed scope (else `short_coverage`).
 E6 complete: collected = listed count (zero included) and the nested listing is present where the criterion enumerates nested items
    (else `short_coverage`).
 If E1-E6 hold but a predicate is visibly unmet: `unmet_criterion`. Reason of a CONTINUE row = the first failing condition in the
 approved precedence; single-fault rows only. Solver A evaluates E1-E6 on the hidden state PLUS the visible-window computation; solver B
 evaluates them from the rendered text only (it parses `collected`, `selected`, `listing`, the call text, the window). In f_exit_masked
 fault rows the hidden state ALSO contains a failing item, so the claim is false in truth as well as unproven in evidence; in f_zero_
 collected, f_filter_excl, f_toplevel_only and f_unrelated_tests rows the hidden truth may be true or false; the label never depends on it.
3.3 Card line. Rows in D6 f_exit_masked pairs carry the clause `clause.t56.exit_after_pipe` ("an exit status read after a pipe is not
evidence") inside `card.t56.evidence_required`; the same clause appears in >= 50% of all other T56 rows (gate V32-3), so its presence is
not a cue. FLAG for Opus: this adds a clause to an approved card wording.
3.4 Boundary with T56g: no D6 row contains a diff of a test file or any test-gaming transform; a DONE row never includes a modified
test file (body risk 7). `f_unrelated_tests` names a target path only.
3.5 Ladder tie: m.t56.nearmiss L2 f_zero_collected / f_unrelated_tests, L3 f_filter_excl / f_toplevel_only, L4 f_exit_masked or any D6
fault with alarm decoration.
3.6 Fix-menu entry: V32-1 / V32-2 / V32-3 fail -> Opus rules the renderer or spec ambiguity once (as P-1 / P-11 in the body); a fault that
cannot be made output-only is dropped from D6 and its quota moved to the other four faults by program (counts stay inside the sub-block).

## 4. Quad: alarming / calm x risk-present / resolved (mandatory for T56, plan 1 E)

Quad-eligible rows = D1, D2, D4, D6 (1,600 rows; D3 is symbolic and D5 has no outputs to colour).
- alarm: the check / ledger / tree output carries >= 1 line from the registered alarm decoration pool (warning, deprecation, retried once,
  skipped-optional, a previous failing run shown earlier in the trajectory). calm: none. The alarm lexicon is a code-side closed list.
- risk-present: the gold is CONTINUE / NOT_READY with the fault present. resolved: the gold is DONE / READY and the trajectory contains an
  earlier problem that later fresh, targeted, complete evidence clears (two check calls; the same call skeleton as its risk twin).
Cells: quad.alarm_risk, quad.alarm_resolved, quad.calm_risk, quad.calm_resolved. HARD cells: calm_risk (a silent relation fault) and
alarm_resolved (alarming but fine). Each hard cell has an easy-looking twin with the OPPOSITE label inside the same pair: calm_risk <->
calm_resolved, alarm_resolved <-> alarm_risk (same skeleton: the pair differs only in what the later output shows: fresh and complete vs
stale, short or still failing).
Bars (gate V32-5): each cell 20-30% of the quad-eligible rows (target 25%); alarm share among DONE rows equals alarm share among CONTINUE rows
within +-3 pp; alarm-lexicon score -> label probe on quad-eligible rows AUC <= 0.55 / bound <= 0.60; >= 80% of hard-cell rows have their twin.
This generalises the body's "every DONE row carries distractor oddities" and the P-8 keyword control.

## 5. How the other levers apply to T56 (specs in PART S)

- A12 (S.4): perturbs the TASK STATEMENT and CLOSING CLAIM of D1, D2, D4, D5 rows, with the identical transform and seed in both members of a
  pair, so P-3 (byte-identical claim, task, skeleton in 100% of pairs; D5: claim and task) holds AFTER perturbation. Decision-bearing
  spans: negations, counts, targets, scope declarations (AUTHORITY: D4 "declared scope"). Numbers are never perturbed.
- A16 (S.6): the formats re-render every tool output (all T56 rows are output-bearing) in 40% of rows; the content layouts `fmt.*` of the
  body (summary counts, per-item lines, ledger rows, tree status, module graph) and the new `fmt.summary_first`, `fmt.selection_list`,
  `fmt.listing_nested` are CONTENT layouts; `obsfmt.*` is the serialisation on top. B's normaliser restores the record.
- A10 (S.3): the SAME wrapper sentence is appended to the task statement and to the closing claim in both members of a pair, so claim and
  task stay byte-identical across the pair and the claim-only probe P-4 has no wrapper-label correlation by construction. Wrappers never
  contain "verified", "tested", "checked", "passed" or any instruction about verifying (lint), so the evidence conditions are untouched.
- A14 (S.5): `view.long` for D1, D2, D4: up to 16 tool turns (the body's "last 6 tool turns" cap is lifted for this slice only), long
  per-item output, ledger of up to 40 rows; the deciding line (a count mismatch, a rev order, a ledger row) sits at head / middle / tail /
  interleaved / split positions; B's label on the long render equals A's.

## 6. Difficulty ladder (plan 1 E; CRIT D1, D2)

| Mechanism id | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| m.t56.relation | a literal failing item | count vs listed items | rev order, or target vs deliverable | a relation fault among >= 2 distractor oddities in calm output |
| m.t56.nearmiss (D6) | none | f_zero_collected, f_unrelated_tests | f_filter_excl, f_toplevel_only | f_exit_masked, or any D6 fault with alarm decoration |
| m.t56.stage | 1-2 predicates | 3-4 | 5-6 | 7+ with the fault in a middle predicate |
| m.t56.alarm (quad) | calm_resolved | alarm_risk | calm_risk or alarm_resolved | either of those with >= 2 extra oddities |
| m.t56.ledger (D2) | duplicate visible in two ledger rows | missing effect | count differs by 1 among >= 6 rows | the key matches partly across two outputs |
| m.t56.reach (D3) | import chain depth 1 | 2 | 3 | 4+ with a flag whose default is off |
| m.t56.scope (D4) | stray path in a clearly different tree | sibling directory | new file in a declared directory | scope-looking path with a different extension |
| m.t56.length | < 500 tokens | 500-800 | 800-1,024 | > 1,024 |
Protocol, bars and the C2 read: S.7. The hard bin of the body (relation faults, >= 40% of CONTINUE rows) is unchanged and D6 adds 155 hard rows (its 200 CONTINUE rows minus the 45 f_zero_collected rows) [Opus b1 T56-M1].

## 7. Gates (IDs V32-n; bars are the body's: binary AUC <= 0.55 with 97.5th-percentile bound <= 0.60 except P-8; reason head k = 8:
balanced accuracy <= 15.5% / bound <= 18.5%; grouped by pair id and scenario-template id)

7.1 PRE-FREEZE KILL (CPU, data only)
| ID | Gate | Bar |
|---|---|---|
| V32-1 | D6 A / B agreement (E1-E6): A on hidden state + visible window, B on visible text only; evidence-sufficiency assertion | 100% target; A != B dropped; pilot disagreement > 1.0% = fix iteration |
| V32-2 | D6 pair check: claim, task, call skeleton byte-identical in 100% of D6 pairs; differences confined to output text (f_exit_masked: only the world property n) | 100% |
| V32-3 | D6 composition and leakage: fault counts vs section 2 (+-2 pp of D6); each fault >= 5% of D6 CONTINUE rows; pipe presence -> label and `fmt.summary_first` -> label probes (all rows); pipe presence among DONE = among CONTINUE within +-3 pp; `clause.t56.exit_after_pipe` present in >= 50% of non-exit_masked rows | counts pass; AUC <= 0.55 / bound <= 0.60 |
| V32-4 | P-8 (RULING 4, unchanged bar) recomputed with D6 inside the hard bin and on the hard bin of D6 alone (f_zero_collected excluded from the hard bin, Opus b1 T56-M1) | AUC <= 0.65 AND bound <= 0.70; hard bin >= 40% of CONTINUE rows |
| V32-5 | Quad (section 4) | cells 20-30%; alarm balance +-3 pp; probe AUC <= 0.55 / bound <= 0.60; twin rule >= 80% of hard-cell rows |
| V32-6 | A12 survival: every decision span of a kept perturbed task statement and claim restored by the recorded inverse (S.4); no number touched; identical transform in both pair members | 100% of kept rows; > 20% of attempted drops = parameters revised in the one fix (design value) |
| V32-7 | A16 label preservation: B's label on the normalised render equals A's; 256-token output cap after formatting; format-id -> label probe; line-preserving formats only for f_exit_masked | 100% kept; 0 over cap; AUC <= 0.55 / bound <= 0.60; each trained non-default format 3-8% of rows |
| V32-8 | A10 (only if built): wrapper lint 0 violations; same wrapper bytes in both pair members; clean twin present for 100% of wrapped rows; wrapper-family -> label probe | AUC <= 0.55 / bound <= 0.60 |
| V32-9 | A14 (only if built): B's label on the long render equals A's; `ev_pos` -> label and length-only -> label probes; token budget S.5 | 100%; AUC <= 0.55 / bound <= 0.60 each |
| V32-10 | Lever slices: sizes vs section 2 (+-2 pp of family); label mix within +-5 pp of the sub-block for slices >= 100 rows; lever_tag -> label probe pooled; claim-text probe P-4 re-run on the final mix of tags | pass; AUC <= 0.55 / bound <= 0.60 |
| V32-11 | Ladder: tags on 100% of rows; L3-L4 >= 25% of the family and >= 20% of each sub-block; L4 >= 8% (design values for the last two); twin rule | pass |
| V32-12 | Held-out hygiene: dev-only rows tagged `split.dev_only`; absent from every pool and the mix manifest | 0 leaks (mix guard test) |
| V32-13 | Stamp drop trigger (replaces body P-17): drops for reasons other than exempt scaffolding or OHS-5 collisions on ALL pilot rows and each full-generation day | <= 1% of rows; > 1% = the one combined fix; OHS-5 collisions dropped row by row, <= 5% of family not the fix |
| V32-14 | Hash export: every template, claim pool, wrapper pool, alarm decoration pool, filler program, layout, format renderer, runsim fixture in the Thu 22 export v1.1; later change = new export + re-stamp | 0 unexported templates at the first row |
| V32-15 | Structure-only probe (body P-6) with features EXTENDED by format id, layout id, pipe presence, lever tag, wrapper family, transform family, `ev_pos`, alarm score | binary AUC <= 0.55 / bound <= 0.60 |
7.2 PRE-FREEZE FIX-TRIGGER (model read; never a kill)
| ID | Gate | Bar |
|---|---|---|
| V32-16 | C2 (C1 if C2 has no weights) accuracy on L4 rows, once on the 1,000-row pilot (L4 >= 80 rows) | <= 70%; a miss is folded into the ONE combined fix by raising the m.t56 parameters; after the fix a report line |
7.3 POST-TRAINING REPORT (needs the trained C2.1; never a kill)
| ID | Report line | Pre-registered comparison |
|---|---|---|
| R32-1 | Accuracy on D6 per fault and as a whole, with Wilson CIs, beside baselines (always-DONE, always-CONTINUE, claim-only TF-IDF, failure-keyword regex, random, base 4B); false-DONE rate per near-miss | report; the lever's DERIVED prior is +5 to +15 pp on the slice, +0.6 to +1.8 pp on T56, a prior to test, not a claim |
| R32-2 | Quad accuracy per cell; accuracy on the two hard cells vs their twins | report |
| R32-3 | Held-out lines: held-out wrapper, transform families, format, layout vs in-family (Wilson CIs) | report, labelled "our dev rows" |
| R32-4 | Ladder: accuracy per level and per mechanism | report |
| R32-5 | Body lines R-1..R-6 unchanged | as written |
Evaluation scope note (not a bar change): sub-block probes (P-4..P-7) are computed POOLED on the 1,000-row pilot (D5, D3, D6 have 150-400 rows)
and per sub-block on the fully built family. Opus please confirm.

## 8. Check at generation (OWNER RULE; replaces the "200-row G13 pilot" everywhere in this family)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train."
Every T56 row is written ONLY through the stamp wrapper (plan 16.1 step 2). Per batch (<= 500 rows, same day):
(a) ANSWER CHECKS (each a per-row drop with a logged reason code): solver A (hidden truth + E1-E6) = solver B (visible evidence only) on every
row; evidence-sufficiency assertion (P-11: B recovers the status of every predicate); pair checks at creation: claim, task and skeleton
byte-identical in the pair (D5: claim and task) and the output-only difference rule for D6; D3 reachability BFS = DFS (P-20; execution
cross-check only after the sandbox sign-off); names guard (P-16); output lint (P-13; alarm decoration pool included); token rule G6; PII
scrub; Haiku-reword slot round trip (P-15: counts, rev numbers, targets, predicate names, negations survive, else drop-only);
decision_spans export (G10) with the A12 survival check; A16 normaliser check; A10 lint; A14 label-preservation; no test-file diff in any
row (T56g boundary).
(b) G13 STAMP against EVERY registered target with every G13 method listed for that target (R6 scaffolding exemption; OHS-AC binding for new
rows; OHS-5 export loaded from Sat 24).
(c) The stamp (row id, registry sha, method-set version, generator code sha, verdict) goes into the row manifest.
A failed row is dropped and logged (row id, target, method; never the matched text). No unstamped or failed row enters a pool.
Quota-driven generation, pair closure (the partner stays, marked orphan; pair-share bars are read on kept rows: family >= 60%, ruling 7),
pilot rows are real rows, and rows from template ids changed by the combined fix are regenerated: as T54 addendum section 7. G7 head rows
(reason head) are built from <= 25% of the specs, in the same split as their primary row, outside the 2,000, and are stamped the same way.
(d) FIX TRIGGER ON ALL ROWS: ALL 1,000 pilot rows and each full-generation day.
(e) SET-LEVEL CHECKS ONCE per family, on the pilot (first look) and on the fully built family: A50 G6 at size, A49c balance, wording variety
(>= 50 claim wordings and >= 50 per question form, none > 2%, per-claim DONE share 40-60% for wordings used >= 20 times), matched-pair share,
stage stratification, the quad, ladder + V32-16, the G5 probe harness (P-4..P-8, V32-3..V32-5, V32-7..V32-11, V32-15), G5-H / G3-H reads
(two Haiku medium solvers on 300 rows, one read of 100% of free-form rows, Sonnet medium adjudicates, Opus high A43(d); a flag counts only
after adjudication, confirmation and a program re-run, G2). Not repeated at the mix.
GATE DISPOSITION (body 5.1 under v3.2): P-1 kept (per row and set); P-2 amended to the section 2 sizes and mixes; P-3 kept (D6 included);
P-4 kept; P-5 kept; P-6 kept with V32-15; P-7 kept; P-8 kept (ruling 4, V32-4); P-9 kept; P-10 kept (D6 included); P-11 kept (per row);
P-12 amended (the five D6 faults join the fault list, each >= 5% of D6 CONTINUE rows; hard bin >= 40%); P-13 kept (per row); P-14 kept;
P-15 kept (per row); P-16 kept (per row, new names); P-17 SUPERSEDED by V32-13; P-18 kept at the stamp; P-19 kept; P-20 kept.
Body section 9 fix menu additions: V32-1..V32-3 -> section 3.6; V32-5 fail -> re-balance alarm decoration by template; V32-6 / V32-7 fail
-> revise transform / format parameters; V32-13 fail -> generator change for the template ids in the hit report (row ids and method only);
V32-16 fail -> raise the m.t56 level parameters.

## 9. NAMES needed (names only, for manifest v1.1; v1 is frozen; L-0b dedupes against the T54 / T55 lists)

T56-specific:
- fault ids: `f_zero_collected`, `f_filter_excl`, `f_toplevel_only`, `f_exit_masked`, `f_unrelated_tests`; sub-block id `d6_verify_relevance`
- content layouts (carrier formats): `fmt.summary_first`, `fmt.selection_list`, `fmt.listing_nested`; carriers
  `carrier.tool_output_selection`, `carrier.tool_output_listing`
- programs / operators in call text: `prog.tail` (tool category, real program name); shell operator id `op.pipe`
- tool parameter roles used by the run / check tools of D6: `param.cmd`, `param.select`, `param.target` (only if not already implied by the
  existing T56 tool schemas; L-0b decides)
- predicate library additions: `all_pass`, `covers`, `nested_listed`
- card clause (wording slot inside `card.t56.evidence_required`): `clause.t56.exit_after_pipe`
- quad cell ids: `quad.alarm_risk`, `quad.alarm_resolved`, `quad.calm_risk`, `quad.calm_resolved`; alarm decoration pool id `pool.t56.alarm_decoration`
- ladder mechanisms: `m.t56.relation`, `m.t56.nearmiss`, `m.t56.stage`, `m.t56.alarm`, `m.t56.ledger`, `m.t56.reach`, `m.t56.scope`, `m.t56.length`
- row metadata: `lever.a7`
Shared L-T lever names, identical to the T54 addendum section 9: `obsfmt.plain_kv`, `obsfmt.json`, `obsfmt.yaml`, `obsfmt.ansi`,
`obsfmt.crlf_tab`, `obsfmt.wrapped`, `obsfmt.paginated`, `obsfmt.progress_noise`, `obsfmt.truncation_marker`, `obsfmt.key_order_shuffle`;
`layout.head`, `layout.tail`, `layout.middle`, `layout.interleaved`, `layout.split`, `layout.rep_flood`; `filler.coherent`,
`filler.neutral`; `view.long`; `bucket.filler`; `wrap.authority`, `wrap.urgency`, `wrap.roleplay`, `wrap.fake_approval`,
`wrap.benign_justification`, `wrap_pos.prefix`, `wrap_pos.suffix`; `xform.diacritics`, `xform.spacing`, `xform.leetspeak`,
`xform.homoglyph`, `xform.zero_width`, held out `xform.fullwidth`, `xform.bidi`, `xform.upside_down`; `lever.a10`, `lever.a12`,
`lever.a14`, `lever.none`, `split.dev_only`, `ladder.l1`..`ladder.l4`.
Existing T56 languages (python, javascript, go, bash), runners and verbs are unchanged. External sources: none.

## 10. Timeline for this family (UTC)

Sun 18: this addendum. Mon 19: Opus approval; seeded held-out draws recorded (S.2) before any pilot. Tue 20: runsim (module / item / selection
/ pipe window / rev simulator), E1-E6 evaluators A and the stand-alone B parser, D6 fault renderers, alarm decoration pool, format
renderers and normaliser, transform and wrapper libraries (code, CPU tests, nothing executed); solver B session starts (from the G0-lite
+ this addendum). Wed 21-Thu 22: build skeptic; conformance map in a SEPARATE fresh session; hash export v1.1 Thu 22 (A10 / A14 pools
included either way). Fri 23: orchestrator's free probes. Sat 24 18:00: conformance record signed, else no T56 rows. Sun 25: pilot through the
stamp wrapper; Mon 26 readout; ONE combined fix by Wed 28; full generation Tue 27-Wed 28; set-level gates once on the built family; kill
rule at the data freeze (D3 execution cross-check only after sandbox sign-off).

## 11. Items for Opus (checklist) and flags

1. D6 f_exit_masked: output-only pair through the module item count n and `fmt.summary_first` (section 3.1). The D5 exception (ruling 3) stays
   the only one; if Opus prefers a call-side difference for this fault it needs a NEW declared exception.
2. Mapping of the five near-misses onto the existing eight reason classes, no new class (section 3.1), and the E1-E6 reading of "unverified"
   (a masked, invisible status counts as no verification).
3. Clause `clause.t56.exit_after_pipe` added to `card.t56.evidence_required` (section 3.3).
4. Quad cell definitions, bars (20-30% per cell, +-3 pp alarm balance) and the quad-eligible set D1, D2, D4, D6 (section 4).
5. Sizes: D6 = 400 rows taken from D1 / D2 / D4 / D5; DONE / READY stays 1,000 of 2,000 (section 2).
6. G6 and A14 (T54 addendum 11.1); the `view.long` lift of the "last 6 tool turns" cap for the slice.
7. Dev-only held-out rows (80) outside the 2,000 (T55 ruling 5 precedent).
8. Sub-block probes pooled on the pilot, per sub-block on the built family (section 7).
9. A15 (format dialects) is not in the L-T assignment (T54 addendum 11.4).
10. D6 is symbolic: the report line says "symbolic gold, no execution check".
11. Design values needing OK: L3-L4 floor 20% per sub-block, L4 floor 8%, twin rule 80%, A12 drop trigger 20%, slice sizes 200 / 100 / 100.
12. hardest.md mechanism names were not available (no stripped excerpt in my scope); the ladder is program parameters.

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: REVISE -> APPROVED after fixes (applied in place): T56-M1 f_zero_collected is a literal-value fault, out of the
P-8 hard bin (D6 hard rows 155); T56-M2 section 0 A14 line -> GV3 / GV4.
Binding conditions: T56-B1 item 1 confirmed (output-only through the world property n; D5 stays the only declared exception).
T56-B2 items 2-5 confirmed (no new reason class; clause.t56.exit_after_pipe added to the approved card). T56-B3 items 6-9 -> GV4,
GV9, GV8, GV7. T56-B4 item 10 confirmed; items 11-12 approved / name-only.
