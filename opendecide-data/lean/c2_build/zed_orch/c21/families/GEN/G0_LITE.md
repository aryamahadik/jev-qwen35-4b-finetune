# G0-LITE: GEN (general program-gold rows)

Lane L-G. Author: Sonnet 5.5 high. Written Sun 18 Oct 2026. Status: DRAFT for Opus G0-lite approval (Mon 19 Oct).
Read scope used: PLAN_TRAINING_SIDE.md (sections 1, 2, 5, 6, 7, 8, pre-registered rules block), LANE_L-G.md. Nothing else.
This file is a design only. No rows exist, no generator has run, no model was called, no generated code was executed.
Every identifier listed in section 9 is a NAME only (for the names-only manifest).

## 0. One-paragraph summary

About 7,000 Claude-authored general-reasoning rows with program gold, in five sub-blocks (multi-step arithmetic, logic,
causal, temporal, tables). Their job is to protect G (general ability) while C skills are added. They get NO hard-bin
upweight (weight 1.0). Gold is the output of a program that runs on a generated world state, never of a model. Each row
is solved by two independent programs (solver A in the generator, solver B written blind by a separate session) and kept
only if both agree and the rendered text parses back to the spec. Domains and names are disjoint from OHS-3/4/5 G by the
names-only list (checked by L-0, not by this author).

## 1. Decision and label set

The model reads a self-contained question and picks one option letter (C2's cross-entropy-on-option-letters format;
options shuffled per row; the 20 percent random non-identity-permutation copies are made at mix time by L-0, not here,
and are not counted in the sizes below).

| k | Meaning | Where used |
|---|---|---|
| 4 | one correct option of four | most forms |
| 3 | entailed / contradicted / undetermined (fixed three option texts, order shuffled) | form L1 only |
| 2 | yes / no (two fixed option texts, order shuffled) | forms AR-F2, LG-L4, CA-C5, TM-T4, TB-B4 |

Label = the letter of the option whose content equals the program answer. No ASK, no abstain, no free text.
INPUT VIEW (required by the plan): the question text only. No policy card, no tool calls, no tool outputs. Rendered
through C2's existing renderer as a general-type row (cygnet + schema_branch_mark layout kept). OPEN: I cannot see
C2's renderer; L-0 must confirm that a general-type row exists in C2's mix with this shape and give the field names.

## 2. Gold method (program, no execution of untrusted code)

GEN rows contain no code and no code execution. The generator builds a typed world state from a seed, computes the answer
with solver A, builds distractors by running error models on the same state, renders text, and stores spec + render map.

| Sub-block | World state (inputs) | Solver A (in the generator) | Solver B (independent, blind session) |
|---|---|---|---|
| ARITH | typed quantity DAG: base quantities (integers or exact decimals, at most 2 decimal places), operations {add, subtract, multiply, exact divide, percent-of, ratio split, min, max, stated rounding rule}, depth 3 to 8, fan-in at most 3, unit/dimension tracking | exact decimal evaluation in topological order | exact rational evaluation (fractions) written from the spec schema alone; plus a unit-dimension checker; any non-terminating or negative intermediate not declared in the spec = reject |
| LOGIC | universe of generated entities, unary/binary predicates, a rule base of Horn-style clauses (body implies a literal head, heads may be negated), explicit facts, at most 16 ground atoms; or an ordering/assignment puzzle over 4 to 6 items with typed constraints | unit propagation to fixpoint (L1, L2, L4); backtracking constraint solver (L3) | exhaustive model enumeration over all 2^n assignments (entailed = true in all models, contradicted = false in all, else undetermined); permutation brute force for puzzles |
| CAUSAL | structural causal model: 4 to 7 variables, acyclic graph, finite small domains, deterministic structural functions from a closed set (sum mod m, min, max, threshold, xor, clipped weighted sum), stated exogenous values | direct SCM evaluation with intervention/counterfactual re-evaluation; graph algorithms (role classification, backdoor test via path rules, d-separation via ball-passing) | SCM simulation by independent code; d-separation via moralised ancestral graph; adjustment-set validity by exhaustive subset enumeration |
| TEMPORAL | event lists on a pinned proleptic Gregorian calendar, 24-hour clock, no daylight-saving, optional fixed offsets; stated rules for month arithmetic (end-of-month clamp or roll-over, one stated per row), weekend set and holiday list stated in the row; task graphs with durations, dependencies and windows | calendar library arithmetic; critical-path computation | civil-day-number integer arithmetic (no calendar library), weekday by modular arithmetic; feasibility by time-stepped simulation |
| TABLE | one or two generated tables (4 to 20 rows, 3 to 7 columns; column types integer, 2-dp decimal, category, date), a query AST (select, where, group, aggregate, order, limit, join) | pure-Python evaluator over the AST | independent AST-to-SQL compiler run on an in-memory stdlib SQLite database; plus a table-carrier parser that reads the serialised table text back |

Answer-uniqueness rules (all by program, 100 percent): exactly one option equals the answer; all options pairwise distinct
after normalisation; no tie in any argmax/argmin/order; no query depends on a missing cell (v1 has none); every needed
fact is inside the prompt (closed world; the only outside knowledge allowed is the declared UNIT-SET conversions and the
calendar).

Distractors are near-miss program negatives: each wrong option is the output of the same solver run on a mutated state
(error models, stored per option in metadata as trap_type). ARITH: omit one step, swap an operation, wrong precedence,
unit slip (by a power of ten or by 60), off-by-one inclusive count, percent of the wrong base, early rounding.
LOGIC: converse fallacy, ignored negation, over-chaining, treating undetermined as entailed. CAUSAL: ignore the
intervention, use the observed instead of the counterfactual value, role confusion. TEMPORAL: off-by-one day, wrong
leap handling, wrong clamp rule, inclusive/exclusive end. TABLE: wrong filter boundary, wrong aggregate, wrong group, join
fan-out. Rule: no trap_type above 35 percent of wrong-option slots within a form.

Render fidelity (solver B owns it): every spec slot (number, entity, date, rule) has a render-map entry; B parses the
final prompt text back and must recover the spec exactly. A row whose prompt does not round-trip is dropped and counted.

A versus B protocol: B is a separate Sonnet 5.5 high session. B receives this G0-lite and the row SCHEMA (field names,
types, semantics) only, never A's code, wording pools or output. B returns an answer and a parse-back for every
candidate row. Agreement is required on 100 percent of kept rows; disagreement rows are dropped and logged with the
sub-block and form. A spec ambiguity found by B during the build (before the 1,000-row pilot) is a build fix, not the
family's fix iteration.

## 3. Sub-blocks, forms, sizes and shares

Target kept TRAIN rows 7,000 (about 18 percent of about 38K new rows). Plus 600 DEV rows (120 per sub-block) from
held-out domains and held-out wording groups, never trained on (the dev share follows L-0's mixdev rule; flagged).
Candidates generated: 8,850 (about 16 percent buffer for G13, OHS-5 collision drops up to 5 percent, A-vs-B drops, A50
and A49c trims). Buffer is a plan for drops, not a cut of scope.

| Id | Form | k | Train rows |
|---|---|---|---|
| AR-F1 | value of the final quantity | 4 | 1,100 |
| AR-F2 | threshold test on the final quantity | 2 | 300 |
| AR-F3 | first wrong line in a given worked solution (exactly one injected error) | 4 | 200 |
| LG-L1 | entailed / contradicted / undetermined | 3 | 500 |
| LG-L2 | which statement must be true | 4 | 500 |
| LG-L3 | which arrangement satisfies every constraint | 4 | 300 |
| LG-L4 | does the conclusion follow | 2 | 200 |
| CA-C1 | outcome under an intervention | 4 | 450 |
| CA-C2 | counterfactual outcome | 4 | 300 |
| CA-C3 | role of a variable for a stated pair (confounder, mediator, collider, none) | 4 | 250 |
| CA-C4 | which set is a valid adjustment set | 4 | 150 |
| CA-C5 | must X and Y be independent given Z | 2 | 150 |
| TM-T1 | date after an offset | 4 | 450 |
| TM-T2 | duration between two timestamps | 4 | 300 |
| TM-T3 | how two intervals relate (four plain-language relations) | 4 | 250 |
| TM-T4 | is the schedule feasible / do these overlap | 2 | 300 |
| TB-B1 | filter and aggregate | 4 | 500 |
| TB-B2 | which entity ranks first | 4 | 350 |
| TB-B3 | two-table join aggregate | 4 | 250 |
| TB-B4 | is the claim true for this table | 2 | 200 |
| | **Total** | | **7,000** (ARITH 1,600; LOGIC 1,500; CAUSAL 1,300; TEMPORAL 1,300; TABLE 1,300) |

Binary forms total 1,150 rows (16.4 percent); the one 3-way form 500; the rest 4-way.

Other shape rules (all PRE-FREEZE data checks, section 6):
- At least 30 percent of rows in every sub-block are in matched minimal pairs (same state, one slot edited so the answer
  changes; pair_id stored; both rows go to the same split). Pairs are counted over rows, not over pairs.
- Difficulty bin by program (step count / graph depth / table size, never by a model read): easy at most 25 percent,
  hard at most 30 percent of each sub-block. NO hard-bin upweight on any GEN row (plan section 2, planner decision).
  C2 reads of GEN rows (pipelined on od-l4b) may inform which rows are kept inside those shares; they never change a
  row's weight and are not a kill gate.
- Tokens: mean at most 800 per sub-block, 1,536 hard cap on at most 10 percent of rows.
- At least 50 wordings per question form (20 forms, so at least 1,000 wordings), no wording above 2 percent of its form.
  Wordings are Claude-authored (Haiku 5.5 medium), closed pools, hashed at export, re-exported at every change.
- Option letters: each letter 25 percent plus or minus 2 pp over the family, plus or minus 3 pp per sub-block (A49c style).
  Binary forms: yes-side share 40 to 60 percent per form. L1: each of the three answers 33.3 percent plus or minus 5 pp.
- Held-out groups for dev and for probe splits: domains D23 and D24 (dev only) and 10 percent of wording groups per form.

## 4. State model details that matter for gold

- Numbers are exact. ARITH final values are integers or 2-dp decimals; the row states the rounding rule when one applies.
- Quantity names, entity names, variable names and event names come from the seeded random namespace with the TRAINING
  salt (no hand-picked fake names). Domain words give flavour only and are chosen from the closed domain vocabularies
  in section 9.
- LOGIC uses plain, formal quantifier wording ("at least one", "every", "none"); the row states in one sentence that
  only the given statements may be used. No "some" implicature, no real-world facts.
- CAUSAL answers refer to the stated model only. The row says that the functions and values given are the whole model.
- TEMPORAL states the month-arithmetic rule, weekend set and holiday list it needs. No time-zone names, no daylight-saving.
- TABLE serialisation (carrier) is chosen per row from the five table carriers; a row with a column-order or
  whitespace ambiguity under its carrier is dropped.

## 5. Spans metadata for the voice lane

Every GEN row stores `decision_spans` (all numbers, quantities, units, dates, negation words, rule words that the answer
depends on) so VOICE can use the row as a source. Only AR-F1, AR-F2 and TM-T1/T2 stems with at most 60 words and no
table are voice-eligible (VOICE caps GEN at 5 percent of kept voice rows).

## 6. Gates

Class key: PK = PRE-FREEZE KILL (CPU, data only; failing it after the one fix iteration rolls the sub-block). PR =
POST-TRAINING REPORT (needs a trained model; never a kill rule). Probe settings, fixed here before any pilot: features
and model are TF-IDF (word 1-2 grams, char 3-5 grams) plus L2 logistic regression, and a gradient-boosted tree on
numeric-structure features; split grouped by (domain, wording group, pair_id); 5 group folds; 95 percent upper bound by a
cluster bootstrap (2,000 resamples) over groups. Binary bars: held-out AUC at most 0.55 with upper bound at most 0.60.
k-way bars: held-out accuracy at most 1/k + 3 pp with upper bound at most 1/k + 6 pp (k=4: 28.0 and 31.0 percent;
k=3: 36.3 and 39.3 percent). CONFIRM RULE (my addition, fixed now): a probe that exceeds the point bar is re-run once on
an independent fresh sample of twice the size from a new seed; it fails the gate only if the re-run also exceeds the
point bar or exceeds the upper-bound bar. Reason: about 40 probes at a 95 percent bound would otherwise give a
non-trivial chance of a false kill. The re-run is logged and is not the fix iteration.

| Gate | Class | Numeric bar | Applies at |
|---|---|---|---|
| G-A1 Solver A vs B agreement | PK | 100 percent on kept rows; disagreement at most 1.0 percent per sub-block of candidates in the 1,000-row pilot (above that = generator defect = fix iteration) | pilot and full |
| G-A2 Render parse-back (B parses prompt to spec) | PK | 100 percent of kept rows; dropped fraction at most 2 percent per sub-block | pilot and full |
| G-A3 Uniqueness: one correct option, distinct options, no ties, closed-world | PK | 100 percent (program) | every row |
| G-A4 Label shape: letter balance, binary yes share, L1 thirds | PK | bars in section 3 | pilot and full |
| G-A5 Size and shape: minimal pairs at least 30 percent per sub-block; difficulty shares; no trap_type above 35 percent; wording at most 2 percent; at least 50 wordings per form; tokens mean at most 800, cap 1,536 on at most 10 percent | PK | as listed | pilot and full |
| G-S1 Option-only probe (strip the stem; predict the correct letter from option texts and values) on each 4-option form pooled by sub-block | PK | k=4 bars: 28.0 / 31.0 percent | pilot and full |
| G-S2 Option-heuristic panel: median value, largest, smallest, closest to the option mean, most shared digits, longest string, option equal to the sum or difference of two others, option nearest a number in the stem | PK | each heuristic: k=4 bars; for the 3-way and the 2-way forms the analogous "answer-class vs surface" heuristic uses its k bars | pilot and full |
| G-S3 Stem-only probe for binary and 3-way forms (predict answer class without the table, facts or numbers that decide it: stem wording, domain, length, pair_id excluded) | PK | binary: AUC 0.55 / 0.60; L1: 36.3 / 39.3 percent | pilot and full |
| G-S4 Length-only probe (prompt tokens, option lengths) for every form | PK | binary AUC 0.55 / 0.60; k-way as above | pilot and full |
| G-S5 Template/wording-id probe (does the wording id or template id predict the answer class) | PK | binary AUC 0.55 / 0.60; k-way bars | pilot and full |
| G-S6 Pair-leak probe (given a row, does being the "first" or "second" row of a pair predict the answer) | PK | binary AUC 0.55 / 0.60 | full |
| G-D1 Domain and name disjointness from OHS-3/4/5 G | PK | zero overlap on the names-only list (L-0 runs it); entity/variable names 100 percent from the TRAINING-salt namespace | before pilot and at row start |
| G-D2 Row-start guard: any domain, unit set, carrier or name outside the closed allow-list refuses the row | PK | 0 rows pass outside the list | every row |
| G-G1 200-row G13 pilot (OHS-3, OHS-4, OHS-AC, OHS-5 once frozen, every public eval target, attack-string literals, A61(a) recorded-HIT sources such as gsm8k-style problem sets) | PK | more than 1 percent of 200 hit by any method = fix iteration (exempt: hits traced only to sha-bound scaffolding; OHS-5 collisions dropped row by row, at most 5 percent of the family not a fix iteration) | pilot, then final mix |
| G-G2 A50 G6 at size; A49c balance | PK | the values fixed in the A50 / A49c records (not in my read scope; not restated here) | pilot and full |
| G-H1 G5-H: two Haiku 5.5 medium solvers on 300 rows (60 per sub-block, stratified by form), plus one Haiku read of 100 percent of the WORDING POOL (GEN rows are program-composed from wording pools, so the free-form text is the pool, not the row) | PK (data only, no trained model) with a program tie-break | A reader disagreement is never a gold change. A flag counts only if Sonnet 5.5 medium adjudication and the Opus A43(d) confirmation both call it a real defect AND a CPU re-execution of the spec reproduces it. Fix iteration if confirmed defects exceed 1.0 percent of the 300 (4 rows or more) or if two or more confirmed defects share a template | pilot, once per family |
| G-H2 G3-H (as adopted; I do not know its bar) | PK (data only) | the bar in the G3-H record | pilot |
| G-R1 Pipeline C2 reads of GEN rows on od-l4b | not a gate | used only for selection inside the section 3 shares; queued reads at the data freeze do not block the family | after full generation |
| P-1 Dev accuracy per sub-block and form vs init and vs base 4B, with CI, and next to trivial baselines (random 1/k, majority letter, best heuristic of G-S2, best probe of G-S1) | PR | no bar (report) | after training |
| P-2 Flip rate under random non-identity option permutation, with CI | PR | report; 1 percent is the dev target of the plan, not a claim | after training |
| P-3 ECE (bin count stated), Brier, trap-slice ECE | PR | report; pooled G ECE bar of 3.5 percent is the plan's, not tested here | after training |
| P-4 Accuracy by difficulty bin and by held-out vs in-domain (D23/D24 vs rest) | PR | flag amber if the held-out gap exceeds 5 pp (report only) | after training |
| P-5 Snapshot-stop line: general slice vs init at 25 and 50 percent snapshots | PR (the plan's existing stop rule, init minus 1.5 pp at both) | owned by L-0, listed for completeness | during training |
| P-6 Causal statement | PR | NO claim that GEN protects G unless a no-GEN arm exists; the report says so | after training |

## 7. Clean-room notes

- GEN has no external source. No dataset, benchmark, textbook, or competitor text is read, quoted or paraphrased.
  Arithmetic word-problem stems must not follow any recorded A61(a) source's frame (G13 enforces; recorded HITs bar a
  source under any form). Question forms are the ones in section 3; their wordings are Claude-authored and original.
- No benchmark item text is in this file. No example row is in this file.
- Names: the seeded random namespace with the TRAINING salt only. I have not hand-picked any entity, variable, event or
  column name. Domain labels in section 9 are flavour labels for the manifest and are subject to L-0's intersection check.
- Standard library tools only (decimal, fractions, itertools, stdlib SQLite for solver B). No package install, no network.
- No model is in the loop for gold, distractors or rendering. Haiku writes wording pools; Haiku/Sonnet read and
  adjudicate; none of them writes a label.
- GEN rows never carry a voice flag; VOICE builds variants from them (VOICE G0-lite).
- OHS-5 collision handling and the literal-ban list are G13's job; this file never shows or needs them.

## 8. Risks

1. Unknown G format. G is sealed from this lane. GEN may not look like G, so any protective effect is unproven. Mitigation:
   five different reasoning families, many domains, held-out domains in dev, no claim of transfer (P-6).
2. Option shortcuts in numeric distractors (median option, nearest-to-mean). Covered by G-S1/G-S2 with the confirm rule.
3. Ambiguity in natural-language logic and in calendar rules. Covered by stated rules in each row, solver B's blind
   parse, and G-H1 (wording pool read 100 percent).
4. Difficulty mismatch: too easy teaches nothing, too hard yields noisy gradients. Difficulty bins by program steps;
   no upweight; no tuning from model reads.
5. Template memorisation by a 4B LoRA: 20 forms, at least 1,000 wordings, 24 domains (2 held out), random namespace.
6. Token budget: tables and logic rule bases can exceed 800 tokens. Caps on table size (20 rows) and clause count.
7. Throughput of the CPU generator is small; no GPU is used. G13 is serial on the Mac and yields to C2.
8. Reader disagreement noise: hard multi-step rows will make Haiku solvers wrong; hence flags need Sonnet, Opus and a
   CPU re-execution before they count.
9. 600 dev rows may duplicate L-0's mixdev rule; L-0 decides.
10. A sub-block may fail alone (e.g. TABLE carrier ambiguity); rolling it shrinks GEN below 7,000 (see section 10).

## 9. NAMES for the names-only manifest (names only; no rows)

```
FAMILY: GEN
POLICY_CARDS: none
TOOLS_IN_ROWS: none
LANGUAGES_RUNNERS_IN_ROWS: none (no code in rows)
SOLVER_SIDE_TOOLS (not in rows): python-3.12-stdlib, decimal, fractions, itertools, sqlite3-stdlib
NAMESPACE: NS-TRAIN (seeded random namespace, TRAINING salt) for entity, variable, event, column and category names
CARRIERS:
  TBL-PIPE, TBL-CSV, TBL-TSV, TBL-KV, TBL-JSON,
  TXT-PROSE, TXT-BULLET, TXT-NUMBERED, TXT-TIMELINE, TXT-LEDGER
UNIT-SET: gram, kilogram, litre, metre, kilometre, second, minute, hour, day, week, percent, count (plain count noun from NS-TRAIN)
DOMAINS (train): 
  D01 warehouse pallet staging
  D02 ferry and bus timetable
  D03 greenhouse irrigation
  D04 clinic appointment scheduling
  D05 bakery batch production
  D06 library loan circulation
  D07 sensor calibration logs
  D08 festival stage logistics
  D09 community garden plots
  D10 freight container yard
  D11 museum exhibit rotation
  D12 laboratory sample queue
  D13 apartment utility billing
  D14 relay race timing
  D15 print shop job queue
  D16 marina berth allocation
  D17 seed bank inventory
  D18 tournament scheduling
  D19 call centre shift roster
  D20 solar array output logs
  D21 vineyard harvest tracking
  D22 cable car maintenance rounds
DOMAINS (dev only, held out): D23 data centre rack power budget, D24 theatre costume store
PREDICATE_VOCAB: per-domain closed word lists for LOGIC (to be authored by Haiku, hashed), plus nonsense predicate stems from NS-TRAIN for about half of LOGIC rows
FORM_IDS: AR-F1 AR-F2 AR-F3 LG-L1 LG-L2 LG-L3 LG-L4 CA-C1 CA-C2 CA-C3 CA-C4 CA-C5 TM-T1 TM-T2 TM-T3 TM-T4 TB-B1 TB-B2 TB-B3 TB-B4
CALENDAR: proleptic-gregorian, 24h-clock, no-DST, fixed-UTC-offsets
```
Domains are my proposals; I do not know OHS G's domains. L-0 must intersect this list with the G names-only list and
return replacements; any replacement is a name-only change and does not restart the G0-lite.

## 10. Fix iteration and kill rule

- One fix iteration for the family. Triggers: more than 1 percent of the 200-row G13 pilot hit (with the stated
  exemptions); a PK gate failing at pilot; A-vs-B disagreement above 1.0 percent per sub-block of the 1,000-row pilot;
  G-H1 confirmed defects above the bar; OHS-5 collisions above 5 percent of a sub-block.
- A fix is allowed to change generator code, distractor error models, carriers or wording pools. After a fix the
  hash export is re-run and the 1,000-row pilot, the 200-row G13 pilot and all PK gates run again.
- Kill rule: a sub-block that fails any PK gate after its one fix iteration, or is not through all PK gates at the data
  freeze (Mon 2 Nov 23:59 UTC), rolls to C2.2/C3 with the failing gate and numbers logged. Sub-blocks are independent
  (my proposal; Opus to rule): GEN ships with the sub-blocks that pass, at their sizes, and the shortfall is not
  back-filled from other sub-blocks above +25 percent of that sub-block's own target. POST-TRAINING lines are never kill rules.
- GEN is not one of the 9 P0 families and does not count toward the 6-of-9 floor. In the shed order it is third
  (after P1 and the voice pool).

## 11. Timeline and build checklist (design items only)

- Sun 18: this file; domain names to L-0 (section 9 block).
- Mon 19: Opus approval; names in the manifest draft.
- Mon 19 to Wed 21: generator and solver A (Sonnet high); CPU tests listed below.
- Wed 21 to Fri 23: solver B (separate Sonnet high), build skeptic (fresh Sonnet high), wording pool authoring
  (Haiku medium), hash export (Sonnet medium).
- After the OHS-5 FREEZE record exists (and not before): 1,000-row pilot (Haiku low runs the script), probes, then the
  200-row G13 pilot (orchestrator queues on the Mac), G5-H/G3-H, full generation (rows from Sun 25 Oct as planned).
- CPU tests to write (names only): determinism per seed; uniqueness; no-tie; exactness of arithmetic; closed-world
  check; namespace-only names; allow-list refusal; parse-back; pair integrity; split integrity (pairs and groups never
  cross a split); data/ohs3* and ohs3_parts/ skipped in every data/** glob.

## 12. Open points for Opus

1. May the section 6 confirm rule (one re-run on a fresh 2x sample) stand? It protects against false kills among about 40 probes.
2. G5-H and G3-H are blind reads by models. I marked them PK (data only) but made reader flags count only after Sonnet,
   Opus and a CPU re-execution agree. If skeptic-6 means "no model read is ever a kill", these become report lines.
3. Sub-block independence in the kill rule (section 10).
4. Dev rows (600) versus L-0's mixdev rule.
5. L-0 must confirm C2's general-type render shape (section 1).
6. GEN as a 5 percent voice source (VOICE file) is optional; default include.


---

## Opus rulings 18 Oct (copied word for word from families/G0_APPROVALS.md by the lane builder, Sun 18 Oct 2026; the build skeptic checks the code against this addendum; where the body text above says otherwise, this addendum binds)

### Global rulings G1-G10 (bind every family)

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

### GEN general rows: APPROVE

Binding condition C1. CA-C4 (adjustment set) and CA-C5 (conditional independence) are graph questions. With
deterministic functions and fixed exogenous values, "independent given Z" is not defined. Rows of these two forms state
that the exogenous variables are independent random inputs and that the question is about the stated graph. They give
no fixed exogenous values. Gold = d-separation / backdoor validity on the graph (A and B as written).
Rulings: 1 the confirm rule is approved for GEN (G5), and GEN's GBT probes count as written. 2 see G2 (the G-H1 rule as
written is approved). 3 sub-block independence is approved (GEN is not P0; G4). 4 the 600 dev rows are never trained on;
L-0 decides whether they merge into mixdev. 5 L-0 confirms C2's general-type render shape before generator code
freezes. 6 GEN as a VOICE source (<= 5%) is included by default. The domain list is name-only and L-0 may replace items
after the G-name intersection without re-approval.

### Round 2 lines for GEN (verbatim)

- All 8: "Solver B = separate Sonnet high session" means CODE written by that session (G1).
- GEN: C1 (CA-C4/CA-C5 rows state independent random exogenous inputs; graph gold).
