# G0 ADDENDUM v3.2: T54 TOOL-NEED/PICK (lane L-T; also carries PART S, the lever library shared by T54, T55 and T56)

Status: DRAFT by Sonnet 5.5 (high), Sun 18 Oct 2026, for Opus batch 1 approval Mon 19 Oct. Design only: no rows, no code run,
no data, no model call, no Modal. Every numeric bar is written BEFORE any pilot and is fixed once Opus approves.
Precedence: G0_LITE.md body < "Opus rulings 18 Oct" block at its end < THIS addendum. Where this file differs, it binds
(plan 16.9: each addendum also copies in the round-1 / round-2 binding conditions; section 1 below does that).
Sources read: C2_1_BUILD_ORDER.md (L-T block, v3.2 additions, KILL RULE, v3.2 pipeline), C2_1_PLAN_v3.md sections 1, 2, 5, 6, 7,
8, the PRE-REGISTERED RULES block of section 3, section 16 (16.1, 16.2, 16.4-16.9), C2_1_EXTRA_LEVERS.md (ADOPT NOW A7, A8, A10,
A12, A14, A16 and A24-A25 for the held-out rule), T54 / T55 / T56 G0_LITE.md, families/G0_APPROVALS.md, training_inputs/excerpts/
tools_s5.md (stripped), l0/NAMES_MANIFEST_V1.json (names only, to list what is NEW). NOT opened: research_v4/hardest.md (no
stripped excerpt is in my read scope, so the ladder below is built from program parameters; the mapping to hardest.md mechanism
names is an open item, see 11.6), any ohs/sealed path, T27 / T40-T46 generators, any benchmark item text.

## 0. What this addendum changes, in one table

| Item | Source | Change for T54 | Kind |
|---|---|---|---|
| A8 smelly-description operators | LEV A8 | 500 rows by substitution (S1-S6), program operators, drop-only dependency check | PRE-FREEZE KILL (data) |
| A10 cue-invariance wrappers | LEV A10 | up to 200 rows, ONLY if the Fri 23 free probe says build; 1 wrapper family held out | PROOF-BEFORE-USE, then PRE-FREEZE KILL; held-out line POST-TRAINING |
| A12 character perturbation | LEV A12 | 300 rows; transform families held out as dev-only rows | PRE-FREEZE KILL (span survival); held-out line POST-TRAINING |
| A14 long-input slice | LEV A14 | up to 200 rows (5%), ONLY if the Fri 23 free probe says build (GV3); G6 binds, no exemption (GV4): rows 1,100-1,536 tokens [Opus b1] | PROOF-BEFORE-USE |
| A16 observation-format perturbation | LEV A16 | re-render of 40% of rows that carry the with-outputs view; 0 extra rows; 1 format held out | PRE-FREEZE KILL (label-preserving check) |
| Difficulty ladder | plan 1 E, CRIT D1, D2 | mechanisms m.t54.*, levels L1-L4, >= 25% at L3-L4, twin rule, C2 <= 70% on L4 | PRE-FREEZE FIX-TRIGGER (becomes a report line after the fix) |
| Check at generation | OWNER-ROW, plan 16.1 | every row answer-checked and G13-stamped when made; P-15 (200-row G13 pilot) is replaced | PRE-FREEZE KILL |
| Exports | build order L-T | DAG builder exported read-only to L-K (T59 / T60) | infra |
| A15 format dialects | LEV A15 | NOT in the L-T assignment (11.4) | none |
| Family size | plan 16.2 | 4,000 rows unchanged; every lever is a substitution, never an addition | rule |

Kill granularity is unchanged (G4): T54 is killed or kept whole. No lever and no sub-block rolls alone.

## 1. Binding conditions carried (word for word from G0_APPROVALS.md; the conformance record maps each clause)

T54 round 1, binding condition C1 (gold must be program-checkable): "ANSWER gold only when the answer content is present in the
rendered context or card, and a program locates it (a span or fact id in the record). Delete 'general knowledge the card
allows' from the label meaning. A 'definitional' ANSWER must point to a card or context span."
T54 round 1 rulings: "1. the idempotent-write rule (S4: unobserved + idempotent = WRITE) is approved as a card-stated policy. 2. R-1
floor and margin are approved as written (recall >= 80% per class, <= 2 pp below init, |gap| <= 8 pp, offset <= 0.50
nats; post-training report). 3. see G2. 4. the call-bearing definition is approved (S2, S5 and S6 use their own balance
gates). 5. see G5 (already compliant). 6. see G6 (already compliant). 7. sub-block drop is not adopted (G4)."
Round 2: "T54: the ANSWER meaning 'general knowledge the card allows' (section 1) is deleted (C1). The section 9 / item 7
sub-block drop is not adopted (G4)." "All 8: 'Solver B = separate Sonnet high session' means CODE written by that session (G1)."
Global rulings G1-G10 bind unchanged (text in G0_LITE.md, last block).

CLAUSE LIST for the ruling-to-code conformance record (plan 16.1 step 0; a fresh Sonnet high writes the map, Opus signs; the
stamp wrapper for T54 refuses to run without it). Proposed CPU test ids in brackets.
| Clause | Text (short) | Test |
|---|---|---|
| C1 | ANSWER gold has a span / fact id in the record; no "general knowledge" label meaning | [t54_c1_answer_span_pointer] |
| Rl-1 | S4 unobserved + idempotent = WRITE, stated in the card | [t54_s4_idempotent_card_text] |
| Rl-4 | call-bearing = CALL, WRITE, READ_FIRST (S1, S3, S4); S2, S5, S6 use own balance gates | [t54_callbearing_def] |
| G1 | solver B is code written from the G0-lite + addendum only; no LLM sets a label | [t54_solverB_independent_import_graph] |
| G3 | no pilot tuning; ONE combined fix | [t54_fix_log_single_iteration] |
| G5 | one probe harness; permutation and injected-leak sanity checks | [t54_probe_harness_sanity] |
| G6 | mean <= 800; none > 1,536; > 1,024 on <= 10% (see 11.1 for the A14 slice) | [t54_token_rule_g6] |
| G7 | no secondary head in T54 | [t54_no_head_rows] |
| G9 | label oracle function exported for the T59 hook | [t54_g9_oracle_export] |
| G10 | decision_spans with roles; wrapper_spans separate | [t54_decision_spans_roles] |
| S1-S6 | rule tables 3.2 of the body (first-match order, uniqueness assertions, levels) | [t54_rule_tables_truth] |
| V32-1..V32-12 | the new gates in section 6 | [t54_p32_*] |
Part S clauses: S.2 (held-out draw), S.3 (wrapper lint), S.4 (transform survival), S.5 (layout and token budget), S.6 (format
check), S.7 (ladder), S.8 (stamp flow), S.9 (exports).

## 2. Sizes by substitution (the family stays 4,000)

Sub-block totals and label mixes of the body (section 4) are UNCHANGED. Levers take rows INSIDE the sub-blocks; the plain rows they
replace are drawn pro rata by label and N-bin cell from one quota table, so the label mix, N-bin shares and call-bearing shares of
the body hold on the whole sub-block and on every lever slice (6.4). Each row carries at most one `lever_tag` (S.1); A16 is a
re-render and stacks on any output-bearing row.

| Sub-block | Rows | A8 smelly | A12 perturbed | A10 wrapped (conditional) | A14 long (conditional) | Plain rows (all levers built) |
|---|---|---|---|---|---|---|
| S1 NEED4 | 1,000 | 150 | 100 | 80 | 60 | 610 |
| S2 PICK | 800 | 150 | 0 | 0 | 0 | 650 |
| S3 LIMIT | 800 | 100 | 80 | 70 | 50 | 500 |
| S4 PRECOND | 500 | 50 | 50 | 50 | 40 | 310 |
| S5 ARGGROUND | 500 | 25 | 70 | 0 | 0 | 405 |
| S6 PARSEQ | 400 | 25 | 0 | 0 | 50 | 325 |
| Total | 4,000 | 500 (12.5%) | 300 (7.5%) | 200 (5.0%) | 200 (5.0%) | 2,800 |
If the Fri 23 probe says do not build A10 and/or A14, those quotas revert to plain rows; no sub-block is resized. A8 and A12 are
unconditional. Dev-only held-out rows (S.2) are extra and are NOT part of the 4,000: 160 rows (4%): wrapper 40, transform 40,
format 40, layout 40 (the wrapper and layout 40s exist only if A10 / A14 are built). They are never in the mix manifest.
Matched pairs (body section 4): pair types A-E unchanged; a lever row keeps its pair partner's lever tag identical except that
the partner may carry the clean render (an A8 / A10 / A12 / A14 row's clean twin is a plain row of the same scenario id).

## 3. A8 smelly-description operators (T54 program operators)

Idea: real tool descriptions are often missing, truncated, boilerplate or stale (EXTRA_LEVERS A8; "97.1% of 856 MCP tools have a
smell", vendor-independent count from the research row). We copy no description text; operators are programs on our own rendered
descriptions.

3.1 Description anatomy (engine change; module tool_engine.render). Each tool description is a list of tagged sentences:
`sent.purpose` (verb + entity statement), `sent.params` (one clause per parameter: role, type, unit), `sent.safety` (read-only /
idempotent / destructive flags, which is where the S4 idempotent flag and the read / write flag are RENDERED), `sent.returns`.
The renderer records, for every input field the gold rule reads, its RENDER LOCATIONS (tool name, typed schema, each sentence kind).
3.2 Operators (closed list; ids in section 9):
| Op | Effect | Allowed on |
|---|---|---|
| smell.purpose_removed | delete `sent.purpose` | all sub-blocks |
| smell.param_docs_dropped | delete `sent.params`, keep the typed schema | all |
| smell.truncated | cut the description at k words (k in 4..9), after the schema | all |
| smell.near_duplicate_tool | add 1-3 tools whose description copies the target's, differing only in schema-visible fields (a parameter type, requiredness or the verb); the S2 uniqueness assertion must still hold | S1, S2, S3, S5 |
| smell.boilerplate_prefix | prepend one sentence from a closed pool (>= 30 generic strings, Claude-authored under the G13 literal ban, writers never see the ban list) to EVERY tool description of the row | all |
| smell.stale_description | description mentions a parameter that the schema does not have, or omits one it has | S1, S2, S3, S5 |
3.3 Dependency rule (this IS the lever's "drop any row whose gold needs the removed text", at creation): an operator may remove a
render location only if every gold input stored there is still rendered in at least one other location (tool name or typed schema,
or another sentence kind). If not, the row is DROPPED and counted as `a8_dep_drop` (never repaired by relabelling). The S4 flags in
`sent.safety` have no second location by design, so on S4 rows no operator may remove `sent.safety`, cut it off (truncated keeps it
inside the first k words) or contradict it (stale_description may only touch `sent.params`). Solver B check
(CODE, G1): B re-parses the SMELLY render, recovers the record fields from the remaining text only, applies the section 3.2 rule
tables of the body, and its label must equal A's. This run is the check-at-generation answer check for A8 (section 7).
3.4 Policy line. When the description and the schema disagree (stale_description), the schema binds. This is a visible card
line (`card.t54.schema_binds`), present in every row that carries smell.stale_description and in >= 50% of all other T54 rows, so
the line is not itself a cue (gate V32-2). The body rule tables are untouched: the schema is what S1-S6 already read.
3.5 Ladder tie: m.t54.smell level = number of operators on the row (L1 none, L2 one, L3 two, L4 three or near_duplicate + stale).
3.6 Fix-menu entry (added to body section 9): V32-1 fail -> revise the operator parameters (k range, near-duplicate count) once;
V32-2 fail -> re-balance operator-to-label quotas by program.

## 4. How the other levers apply to T54 (specs are in PART S below)

- A12 (S.4): perturbs the request text of S1, S3, S4, S5 rows (user turn only). decision_spans (G10) are re-exported with the new
  offsets. Tool names, parameter names, schema keys, numbers and ids are never perturbed.
- A10 (S.3): wrapper prefix or suffix on the final user turn of S1, S3, S4 rows. Wrappers state no value and no instruction about
  asking, confirming or proceeding, so CALL / ASK / NO_TOOL / ANSWER, and the S4 branches, are unchanged. Real consent signals are
  excluded by lint.
- A14 (S.5): `view.long`: multi-turn history up to 16 turns (coherent filler = earlier steps of the same scenario; neutral filler =
  unrelated records), and tool lists up to N = 25. The decision-bearing source of a parameter value (S1 CALL vs ASK, S3 PARAM, S4
  state) or the DAG node inputs (S6) sit at head / middle / tail / interleaved / split positions.
- A16 (S.6): applies ONLY to rows with the with-outputs view (S3-RESULT rows, S4 rows with observed state; about 500 rows, DERIVED
  from the body label mixes). 40% of them render in a non-default training format.

## 5. Difficulty ladder (plan 1 E; CRIT D1, D2)

Level parameters L1-L4 per mechanism (all program parameters; T54 has no published difficulty study, so these are our own).
| Mechanism id | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| m.t54.distractors | N 2-3 | N 4-6 | N 7-16 | N 17-25 |
| m.t54.hardneg | none | one same-verb OR one same-namespace negative | both kinds | both + parameter-name overlap + a negative whose schema differs from the target in ONE type or requiredness |
| m.t54.reference | value stated verbatim | one pronoun, one antecedent | pronoun, 2+ candidate values, one matches by role and type | antecedent only in an earlier output (with-outputs view) vs absent (CALL vs ASK pairs) |
| m.t54.deletion (S3) | TOOL deleted | PARAM deleted, card forbids default | RESULT deleted | any deletion + a near-substitute tool that fails only on a required-parameter type |
| m.t54.precond (S4) | observed fact | unobserved + idempotent | unobserved + non-idempotent + a read tool among >= 4 same-namespace tools | the L3 case + a smell operator or the long view |
| m.t54.grounding (S5) | verbatim in user turn | declared transformation | same string present only in another role's field | wrong-role + declared transformation |
| m.t54.dag (S6) | depth 2 | depth 3 | depth 4 + one equivalence group | depth >= 5 + >= 2 equivalence groups + a ready-looking decoy node |
| m.t54.smell | none | one operator | two operators | three operators or near_duplicate + stale |
| m.t54.length | < 500 tokens | 500-800 | 800-1,024 | > 1,024 |
Protocol, bars and the C2 read are in S.7. T54 does NOT use the mandatory alarming/calm x risk-present/resolved quad (it is
mandatory only for T50, T51, T53, T41c and T56); the twin rule of S.7 applies.

## 6. Gates (IDs continue the body's P- series; numbering V32-n)

Bars are the body's: binary probes AUC <= 0.55 with 97.5th-percentile cluster-bootstrap bound <= 0.60 (G5); k-way balanced accuracy
<= 1/k + 3 pp with bound <= 1/k + 6 pp; grouped splits by scenario-template id and pair id.
6.1 PRE-FREEZE KILL (CPU, data only)
| ID | Gate | Bar |
|---|---|---|
| V32-1 | A8 label preservation: B on the smelly render equals A's label; dependency rule 3.3 | 100% of kept A8 rows; `a8_dep_drop` rate reported; > 40% of attempted A8 rows dropped = operator parameters revised in the one fix (design value) |
| V32-2 | A8 balance: per operator (>= 100 rows, else pooled by m.t54.smell level) call-bearing share in S1, S3, S4; operator-id -> label probes | share 40-60%; operator-id -> call-bearing AUC <= 0.55 / bound <= 0.60; operator-id -> S1 4-way balanced acc <= 28% / bound <= 31%; `card.t54.schema_binds` present in >= 50% of non-stale rows |
| V32-3 | Lever slice sizes and balance: each lever slice (A8, A12, A10, A14) vs section 2; label mix within +-5 pp of its sub-block (slices >= 100 rows); lever_tag -> label probe pooled | sizes +-2 pp of family; AUC <= 0.55 / bound <= 0.60 |
| V32-4 | A12 survival: every kept perturbed row, every decision span restored by the recorded inverse (S.4); no number / id / closed-vocabulary span touched | 100% of kept rows; survival drops counted; > 20% of attempted drops = transform parameters revised in the one fix (design value) |
| V32-5 | A16 label preservation by the format-aware normaliser (S.6); 256-token output cap after formatting; format-id -> label probe (on with-outputs rows) | 100% kept; 0 over cap; AUC <= 0.55 / bound <= 0.60; each trained non-default format 3-8% of with-outputs rows |
| V32-6 | A10 (only if built): wrapper lint 0 violations; clean twin present for 100% of wrapped rows; wrapper-family -> label probe | AUC <= 0.55 / bound <= 0.60 |
| V32-7 | A14 (only if built): label preservation (B on the long render); evidence-position -> label probe; length-only -> label probe; token budget S.5 | 100%; AUC <= 0.55 / bound <= 0.60 each; budget as S.5 |
| V32-8 | Ladder: share at L3-L4 (family and each sub-block), L4 share, twin rule, tags present on 100% of rows | family >= 25%; each sub-block >= 20% (design value); L4 >= 8% of the family (design value, so the C2 read has n >= 80 on a 1,000-row pilot); twin rule >= 80% of L3-L4 rows |
| V32-9 | Held-out hygiene: dev-only rows tagged `split.dev_only`, held-out ids absent from every training pool and from the mix manifest (mix guard test) | 0 leaks |
| V32-10 | Stamp drop trigger (replaces body P-15): drops for reasons other than exempt sha-bound scaffolding or OHS-5 collisions, on ALL pilot rows and on each full-generation day | <= 1% of rows; > 1% = the one combined fix; OHS-5 collisions dropped row by row, <= 5% of the family is not the fix |
| V32-11 | Hash export: every template, wording pool, wrapper pool, boilerplate pool, filler program and layout is in the Thu 22 export v1.1; any later change = a new export + re-stamp of affected rows (16.1 step 6) | 0 unexported templates at the first row |
6.2 PRE-FREEZE FIX-TRIGGER (model read on od-l4b; never a kill)
| ID | Gate | Bar |
|---|---|---|
| V32-12 | C2 (C1 if C2 has no weights) accuracy on L4 rows, once on the 1,000-row pilot | <= 70%. A miss is folded into the ONE combined fix by RAISING the program parameters (never by dropping rows by model score); after the fix a miss is a report line |
6.3 POST-TRAINING REPORT (needs the trained C2.1; never a kill)
| ID | Report line | Pre-registered comparison |
|---|---|---|
| R32-1 | A8: accuracy on the smelly slice vs its clean twins (Wilson CIs), per operator | report; the lever's DERIVED prior is +1 to +4 pp on the smelly slice, a prior to test, not a claim |
| R32-2 | Held-out lines: held-out wrapper family, held-out transform families, held-out format, held-out layout vs in-family | report with CIs, labelled "our dev rows" |
| R32-3 | Ladder: accuracy per level L1-L4 and per mechanism | report |
| R32-4 | Body lines R-1..R-7 unchanged | as written |
6.4 Evaluation scope note (not a bar change): body probes P-5a..P-5e that are defined per sub-block are computed POOLED across the
sub-blocks of equal k on the 1,000-row pilot (a sub-block of 250 pilot rows cannot meet a 0.60 upper bound by sampling noise alone)
and per sub-block on the fully built family. Opus please confirm (11.5).

## 7. Check at generation (OWNER RULE; replaces the "200-row G13 pilot" everywhere in this family)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train."
Every T54 row is written ONLY through the stamp wrapper (plan 16.1 step 2). At creation, per batch of <= 500 rows, same day:
(a) ANSWER CHECKS, each a per-row drop with a logged reason code: solver A = solver B on the record (P-1); B's re-parse of the RENDERED
prompt gives the same label (render-fidelity); S2 / S6 uniqueness assertions (exactly one option equals the gold after
canonicalisation); C1 answer-span pointer for ANSWER rows; names guard against the closed allow-list (P-13); output lint (no imperative
or second-person clause in rendered outputs, P-14); token rule G6 (row <= 1,536 tokens, or the S.5 exemption); PII scrub; Haiku-reword
slot round trip (P-11); decision_spans export with roles (G10) and, for A12 rows, the survival check; A8 dependency + B-on-smelly
check (3.3); A16 format check (S.6); A10 lint (S.3); A14 label-preservation (S.5).
(b) G13 STAMP: the row goes to the stamp service (single Mac job) and is checked against EVERY registered target with every G13
method listed for that target (R6 scaffolding exemption; OHS-AC binding for new rows).
(c) The stamp (row id, registry sha, method-set version, generator code sha, verdict) is written into the row manifest.
A failed row is dropped and logged (row id, target name, method; never the matched text). No unstamped or failed row enters a pool.
Quota-driven generation: seeds advance until every cell quota is filled with stamped rows; drops are counted by reason; no cell is
back-filled by relabelling or by a row of another cell. Pair closure: when a member of a matched pair is dropped by a NON-G13 answer
check, the partner STAYS (marked `orphan`); when a member is dropped by the G13 stamp, the whole pair is dropped and its scenario is
retired, never re-worded (GV5) [Opus b1]; pair-share bars (body P-12, >= 30%) are evaluated on kept rows, and a sub-block that ends below its bar is a fix item.
Pilot rows are real rows (same wrapper, same stamps): after the combined fix, rows built from template ids the fix changed are
discarded and regenerated (logged); all others stay.
(d) FIX TRIGGER ON ALL ROWS (16.1 step 3): drop rate counted on ALL 1,000 pilot rows and on each full-generation day.
(e) SET-LEVEL CHECKS RUN ONCE per family, on the pilot (first look) and on the fully built family: A50 G6 at size, A49c balance,
wording variety (>= 50 per question form, none > 2%), matched-pair share, the ladder and V32-12, the G5 probe harness (P-5a..e, P-6,
P-7, P-8, P-9, V32-2..V32-8), G5-H / G3-H reads (two Haiku medium solvers on 300 rows, one read of 100% of free-form rows, Sonnet
medium adjudicates, Opus high A43(d)); a flag counts only after adjudication, Opus confirmation and a program re-run (G2). Not
repeated at the mix.
GATE DISPOSITION (body section 5.1 under v3.2): P-1 kept (per row at creation and per set); P-2 kept (set level); P-3 kept; P-4 kept;
P-5a-e kept (see 6.4); P-6 kept; P-7 kept; P-8 kept; P-9 kept; P-10 kept (per row cap + set level); P-11 kept (per row); P-12 kept;
P-13 kept (per row); P-14 kept (per row); P-15 SUPERSEDED by V32-10 (G13 on every row, read on all pilot rows); P-16 kept, measured at
the stamp.
Body section 9 fix menu additions: V32-4 / V32-5 fail -> revise transform / format parameters; V32-10 fail -> back to the generator
for the template ids named in the hit report (row ids and method only); V32-12 fail -> raise the m.t54 level parameters.

## 8. Exports and cross-family hooks

- DAG builder (tool_engine.dag, with the S6 Kahn-levels evaluator): exported READ-ONLY to L-K (T59, T60). Export contract: module
  path, API (build_dag(scenario_record) -> levels, equivalence groups), the code sha, the CPU test ids; any change = a new export
  and a notice to L-K. Solver B's longest-path evaluator is NOT exported.
- G9 hook (CRIT C1, plan 16.4 T59 row): `t54_label_oracle(record, card) -> label` is exported read-only so L-K can run the
  cross-family CPU test. KNOWN TENSION for Opus (11.3): T54 S1 rule 3 gives ASK whenever a required parameter has no source (and the
  card forbids defaults), while T59's gold is PROCEED when every interpretation has a reversible cost. "Same action, same state,
  same card, same label" holds only if the two families' cards differ VISIBLY on this point. Proposal: the T54 cards state "ask when
  a required value has no source"; the T59 G0-lite carries a card line "proceed with the most likely value when the action can be
  undone"; the G9 test treats them as different cards.
- G10: decision_spans (roles) for every user turn; wrapper_spans exported as a separate list (not a decision role).

## 9. NAMES needed (names only, for manifest v1.1; v1 is frozen; every id is an identifier, never row text)

T54-specific:
- policy: `card.t54.schema_binds`
- smell operators: `smell.purpose_removed`, `smell.param_docs_dropped`, `smell.truncated`, `smell.near_duplicate_tool`,
  `smell.boilerplate_prefix`, `smell.stale_description`, `smell.none`; pool id `pool.t54.boilerplate_prefix`
- description sentence kinds: `sent.purpose`, `sent.params`, `sent.safety`, `sent.returns`
- ladder mechanisms: `m.t54.distractors`, `m.t54.hardneg`, `m.t54.reference`, `m.t54.deletion`, `m.t54.precond`, `m.t54.grounding`,
  `m.t54.dag`, `m.t54.smell`, `m.t54.length`
Shared L-T lever names (identical in the T55 and T56 lists; L-0b dedupes):
- carrier formats: `obsfmt.plain_kv`, `obsfmt.json`, `obsfmt.yaml`, `obsfmt.ansi`, `obsfmt.crlf_tab`, `obsfmt.wrapped`,
  `obsfmt.paginated`, `obsfmt.progress_noise`, `obsfmt.truncation_marker`, `obsfmt.key_order_shuffle`
- layouts: `layout.head`, `layout.tail`, `layout.middle`, `layout.interleaved`, `layout.split`, `layout.rep_flood`; fillers
  `filler.coherent`, `filler.neutral`; view tag `view.long`; namespace bucket `bucket.filler`
- wrapper families (row-manifest metadata): `wrap.authority`, `wrap.urgency`, `wrap.roleplay`, `wrap.fake_approval`,
  `wrap.benign_justification`; positions `wrap_pos.prefix`, `wrap_pos.suffix`; wrapper pool ids `pool.wrap.<family>`
- transform families (metadata): trained `xform.diacritics`, `xform.spacing`, `xform.leetspeak`, `xform.homoglyph`, `xform.zero_width`;
  held out `xform.fullwidth`, `xform.bidi`, `xform.upside_down` (aliases of the canonical shared ids `pert.*`; job manifests use
  `pert.*`, Opus b1 GV6)
- row metadata: `lever.a7`, `lever.a8`, `lever.a10`, `lever.a12`, `lever.a14`, `lever.none`, `split.dev_only`, `ladder.l1`..`ladder.l4`
Existing T54 names are unchanged. No new language, runner, tool verb or parameter role. External sources: none.

## 10. Timeline for this family (UTC; follows build order v3.2-r Day-3 and plan 16.7)

Sun 18: this addendum. Mon 19: Opus approval; seeded held-out draws recorded (S.2) before any pilot. Tue 20: DAG builder + S1-S6
evaluators, A8 operators and sentence-tagged renderer, wrapper / transform / format / layout libraries (code, CPU tests, no rows);
solver B session starts (from G0-lite + this addendum). Wed 21-Thu 22: build skeptic; conformance map in a SEPARATE fresh session;
hash export v1.1 Thu 22 (includes the A10 and A14 pools whether or not they are later built). Fri 23: orchestrator's free probes
(A10, A14); Sat 24 18:00: conformance record signed, else no T54 rows. Sun 25: 1,000-row pilot through the stamp wrapper; set-level
gates once; Mon 26: pilot readout; ONE combined fix by Wed 28; full generation Tue 27-Wed 28; set-level gates once on the built
family; kill rule at the data freeze.

## 11. Items for Opus (checklist) and flags

1. [RULED Opus b1 GV4: no exemption; the default 1,100-1,536 tokens applies.] G6 vs A14. A14 rows are 1.5-3K tokens, but G6 says "no row above 1,536". Ask: exempt the A14 slice from the row cap (slice <= 5%,
   family mean still <= 800, A14 rows count inside the ">1,024 tokens on <= 10%" budget, so all other T54 rows above 1,024 are
   <= 5% of the family: the body's "N 17-25 bin reaches the cap" is then limited to half of that bin). Default if no exemption:
   the slice is built at 1,100-1,536 tokens.
2. Held-out rows are dev-only and OUTSIDE the 4,000 (T55 ruling 5 precedent; EXTRA_LEVERS A24 "-3 to -5% rows"): confirm.
3. G9 tension with T59 (section 8).
4. A15 (format dialects of card body and tool schemas) is "all lanes" in plan 16.2 but is absent from the L-T assignment (build order
   L-T line; plan 16.9 table). The renderer takes a `dialect` parameter (default = current) so A15 is cheap to add; no dialect rows
   are built and no dialect is held out unless the orchestrator extends the assignment.
5. Evaluation scope of sub-block probes on the pilot (6.4).
6. hardest.md mechanism names: the ladder uses program parameters. A stripped hardest.md excerpt for T54 would let the mechanism ids
   be renamed; it changes names only, not parameters.
7. Design values proposed here and needing Opus OK: sub-block L3-L4 floor 20%, L4 floor 8%, twin rule 80%, A8 dep-drop trigger 40%,
   A12 drop trigger 20%, A8 slice 500, A12 slice 300, A10 slice 200, A14 slice 200.
8. The Fri 23 A10 and A14 probe thresholds are the orchestrator's, written before the read (S.3, S.5 give proposals only).

---------------------------------------------------------------------------------------------------------------------

# PART S: SHARED L-T LEVER LIBRARY (binds T54, T55 and T56; incorporated by reference in the other two addenda)

S.1 ROW TAGS. Every row manifest carries `lever_tag` in {lever.a7 (T56 only), lever.a8 (T54 only), lever.a10, lever.a12, lever.a14,
lever.none} (at most one), `a16` (bool), `ladder_level`, `ladder_mechs`, `split` (train | split.dev_only), `held_out` (none | wrapper |
xform | format | layout | viol_type), `pair_id`, `orphan` (bool), `twin_of` (scenario id of the clean twin, or null). Tags are written
by the generator, read by the gates, and never rendered.

S.2 HELD-OUT DRAW (A24 prerequisite; one draw for T54, T55 and T56; recorded with its seed and sha in a ladder file BEFORE any pilot;
the orchestrator may overwrite it with a global draw before the pilot). Wrapper: wrap.roleplay and wrap.benign_justification are held
out, FIXED by Opus batch 1 (GV2), no draw. Transforms: the
three lever-named families xform.fullwidth, xform.bidi, xform.upside_down are held out (no draw); the five others are trained.
Format: 1 of {obsfmt.yaml, obsfmt.paginated, obsfmt.ansi, obsfmt.progress_noise} by seeded draw. Layout: 1 of the 5 positions by seeded
draw (layout.rep_flood is never trained and is dev-only). Held-out material is generated by the same machinery into rows tagged
`split.dev_only`; CPU test: no dev-only id appears in any training pool or the mix manifest.

S.3 A10 CUE-INVARIANCE WRAPPERS (conditional; proof before use).
- FREE PROBE FIRST (orchestrator, Fri 23): 200 wrapped items built from C2's existing dev rows, read by C2 on od-l4b. Build rule FIXED
  by Opus batch 1 (GV1): a flip = C2's predicted label on the wrapped item differs from its prediction on the unwrapped original;
  build iff flips >= 10 of 200 (5.0%); no result by Fri 23 18:00 UTC = not built.
- The wrapper pools and code are written, tested and hash-exported on Thu 22 either way; the probe decides only whether rows are made.
- Families: wrap.authority, wrap.urgency, wrap.fake_approval (trained); wrap.roleplay, wrap.benign_justification (held out, GV2). Each pool >= 20 sentences,
  programme seeds reworded by Haiku medium, under the G13 literal ban (writers never see the ban list).
- A wrapped row = the clean row + ONE wrapper sentence as prefix or suffix of the final user turn (T54, T55) or of both the task
  statement and the closing claim (T56, identically in both members of a pair). Label and every gold field unchanged; the clean row
  stays in the family (`twin_of`).
- LINT (code; the deny patterns live in code and are not shown to writers): a wrapper contains no digit, quoted string, id-like or
  path-like token (no value-bearing span), no consent-naming (operation + target), and no instruction about asking, confirming,
  retrying, stopping, continuing, polling or verifying. Real consent signals are excluded. Wrapper spans are exported as
  `wrapper_spans`, not as decision_spans.
- Balance: within each wrapper family, label shares within +-5 pp of the sub-block (slices >= 100 rows); wrapper-family -> label
  probe AUC <= 0.55 / bound <= 0.60 pooled.

S.4 A12 CHARACTER PERTURBATION (unconditional).
- Applies to free text in the USER TURN (T54, T55), the TASK STATEMENT and CLOSING CLAIM (T56, identically in both members of a pair),
  and the `detail` / phrase channel of T55 tool outputs. Never to: numbers, ids, tool and parameter names, JSON / YAML keys, the closed
  code vocabulary (`status`, `code`, field keys), error-class tokens carried in the code channel.
- Transforms (trained): xform.diacritics, xform.spacing (single spaces inside one registered word), xform.leetspeak (map
  a4 e3 i1 o0 s5 t7), xform.homoglyph (a small safe confusable set), xform.zero_width (= pert.zero_width: ZERO WIDTH SPACE U+200B
  inserted inside words; no ZWJ / ZWNJ, no Tags block, no variation selectors; Opus b1 GV6).
  Held out (dev-only): xform.fullwidth, xform.bidi, xform.upside_down.
- ROLE x TRANSFORM matrix (G10 roles): negation / polarity: all trained transforms except spacing, at most 1 changed character;
  entity / path / flag: diacritics, zero_width; AUTHORITY: diacritics, zero_width; number: NONE. Other words: any trained transform
  within an edit budget of <= 25% of characters per perturbed word and <= 30% of words in the text.
- SURVIVAL (the lever's "drop at creation if a decision span does not survive"): each transform records its operations, has an
  inverse, and the check is invert(apply(span)) == span exactly, with the perturbed span inside the edit budget. A span that fails is
  a drop (`xform_drop`), counted by role.
- Balance: perturbation presence and transform family are balanced against label (+-5 pp, slices >= 100 rows; presence -> label probe
  AUC <= 0.55 / bound <= 0.60).

S.5 A14 LONG-INPUT SLICE (conditional; proof before use; money shed step 2).
- FREE PROBE FIRST (Fri 23, orchestrator): C2 on a buried-evidence eval slice vs its short-input recall on od-l4b. Build rule FIXED by
  Opus batch 1 (GV3): build iff short-input recall minus buried-evidence recall >= 5 pp AND the paired-bootstrap 95% lower bound of
  that gap > 0; no result by Fri 23 18:00 UTC = not built.
- Layouts: layout.head, .tail, .middle, .interleaved, .split (decision-bearing facts at two positions >= 3 turns apart), plus
  layout.rep_flood (dev-only). Fillers: filler.coherent (earlier steps of the same scenario, consistent state), filler.neutral (data-
  field records from the separate bucket `bucket.filler`; lint: contains no value or term of the row's decision-bearing set).
  `view.long`: up to 16 turns, each tool output still <= 256 tokens.
- Share: fixed 5.0% of the family, by substitution. TOKENS: G6 binds, no exemption (Opus b1 GV4): the slice is built at 1,100-1,536
  tokens and counts inside the ">1,024 on <= 10%" rule; the 1.5-3K form exists only as an eval slice.
  The slice is tagged `lever.a14` so it can be dropped from the mix by tag (money shed step 2) with no re-render; 3-8K tokens exists
  only as an eval slice built by L-E / L-0 from the same layout code.
- Checks: B's label on the long render equals A's; evidence-position (`ev_pos`) -> label probe and length-only -> label probe
  AUC <= 0.55 / bound <= 0.60; the decision-bearing source appears in every layout with equal label shares.

S.6 A16 OBSERVATION-FORMAT PERTURBATION (unconditional; 0 extra rows).
- Applies to rendered TOOL OUTPUTS only (never user turns, task statements or claims).
- Formats: default obsfmt.plain_kv (60% of output-bearing rows); trained non-default obsfmt.json, .yaml, .ansi, .crlf_tab, .wrapped,
  .paginated, .progress_noise, .truncation_marker (together 40%; each 3-8% of output-bearing rows); obsfmt.key_order_shuffle is an
  independent switch (30% of rows). One format is held out (S.2) into dev-only rows.
- LABEL-PRESERVING CHECK (CODE, solver B): a format-aware normaliser (strip ANSI, normalise CRLF / tabs, join wrapped lines, merge
  pages, drop registered decoration lines, parse JSON / YAML, undo key order) maps the rendered output back to the record; B's label
  on the normalised record equals A's; otherwise drop (`fmt_drop`). Decoration lines (progress bars, pagination footers) carry no number
  that is not already present in a data field of the same output with the same value. Truncation markers come only after the
  decision-bearing fields.
- 256-token cap per output AFTER formatting. An over-cap output is re-rendered once in obsfmt.plain_kv, else dropped.
- Balance: format id -> label probe AUC <= 0.55 / bound <= 0.60; label shares per format within +-5 pp of the sub-block.

S.7 DIFFICULTY LADDER PROTOCOL (plan 1 E; CRIT D1, D2). Each family names its mechanisms with level parameters L1-L4. A row's level =
the maximum mechanism level on the row, except that L4 is assigned only when at least two mechanisms are at L3 or above (else the row
is L3). Required: >= 25% of rows at L3-L4 (each sub-block >= 20%, design value); L4 >= 8% of the family (design value); each L3-L4
row has an easy-looking twin with the OPPOSITE label (same scenario-id prefix, level <= L2, token count within +-15%, same alarm-word
presence) for >= 80% of L3-L4 rows. MEASURED BAR: C2 (C1 if C2 has no weights) scores <= 70% on L4 rows, once, on the 1,000-row
pilot (od-l4b read run by the orchestrator's pipeline; the lane never calls a model). A miss is folded into the family's ONE combined
fix by raising the program parameter; rows are never dropped by model score; after the fix a miss is a report line, not a kill.

S.8 STAMP FLOW. As T54 addendum section 7, with the family's own answer checks. Fix trigger and exemptions are the plan's: > 1% of
rows dropped for reasons other than exempt scaffolding or OHS-5 collisions (<= 5% of the family, row by row) = the ONE combined fix (G3).
The record builder (stamp wrapper) refuses to run without a signed ruling-to-code conformance record for its current code sha and
ruling sha (16.1 step 0).

S.9 EXPORTS. T54: DAG builder. T55: ledger simulator. Both read-only to L-K, each with module path, API, sha and CPU tests; a change
after export is a new export with a notice to L-K. Solver B code is never exported.

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: REVISE -> APPROVED after fixes (applied in place; PART S binds T55 and T56 too): S.3 A10 rule (GV1); S.2 wrappers
held out fixed (GV2); S.5 A14 rule (GV3) and tokens (GV4); section 0 A14 line (GV4); S.4 zero_width = U+200B (GV6); section 7 pair
closure after a G13 drop (GV5); section 9 transform ids alias pert.* (GV6). Item 11.1 -> GV4; 11.2 -> GV9; 11.4 -> GV7; 11.5 -> GV8.
Binding conditions: T54-B1 the T59 G9 tension is solved by visible card lines as proposed; binding on the T59 G0-lite (on a T54
card T59 must give T54's label). T54-B2 11.6: renaming ladder ids later is name-only. T54-B3 11.7 design values approved.
T54-B4 obsfmt.* ids are L-T's own; recorded lane-scoped in the manifest. T54-B5 card.t54.schema_binds is a new policy id (v1.1).
