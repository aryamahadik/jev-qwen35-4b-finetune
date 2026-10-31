# G0 ADDENDUM v3.2: T55 RECOVER-ESCALATE (lane L-T)

Status: DRAFT by Sonnet 5.5 (high), Sun 18 Oct 2026, for Opus batch 1 approval Mon 19 Oct. Design only: no rows, no code run, no data,
no model call, no Modal. Every numeric bar is written BEFORE any pilot and is fixed once Opus approves.
Precedence: G0_LITE.md body < "Opus rulings 18 Oct" block at its end < THIS addendum (this file binds where it differs).
PART S (the lever library shared by T54, T55, T56: held-out draw, wrappers, perturbation, long-input slice, observation formats,
ladder protocol, stamp flow, exports) is in families/T54/G0_ADDENDUM_v32.md and is incorporated here by reference; the build skeptic and
the conformance writer read all three addenda. This file only states what is specific to T55.
Sources read: C2_1_BUILD_ORDER.md (L-T block, v3.2 additions), C2_1_PLAN_v3.md sections 1, 2, 5, 6, 7, 8, PRE-REGISTERED RULES block, 16;
C2_1_EXTRA_LEVERS.md (ADOPT NOW A10, A12, A14, A16; A24 held-out rule); T55 G0_LITE.md; families/G0_APPROVALS.md; stripped tools_s5.md;
l0/NAMES_MANIFEST_V1.json (names only). NOT opened: research_v4/hardest.md, any ohs/sealed path, T27 / T40-T46 generators, any
benchmark item text. LIMBO and ToolMaze are cited as ideas only.

## 0. What this addendum changes, in one table

| Item | Source | Change for T55 | Kind |
|---|---|---|---|
| LIMBO citation | plan 1 B.6 (CRIT H2) | corrected; class design UNCHANGED (section 3) | text |
| A16 observation-format perturbation | LEV A16 | 40% of output-bearing rows (about 1,080 of 2,700), 0 extra rows, 1 format held out | PRE-FREEZE KILL |
| A12 character perturbation | LEV A12 | 200 rows by substitution; transform families held out as dev-only | PRE-FREEZE KILL; held-out POST-TRAINING |
| A10 cue-invariance wrappers | LEV A10 | up to 150 rows, ONLY if the Fri 23 probe says build | PROOF-BEFORE-USE |
| A14 long-input slice | LEV A14 | up to 150 rows (5%), ONLY if the probe says build (GV3); G6 binds, no exemption (GV4): rows 1,100-1,536 tokens [Opus b1] | PROOF-BEFORE-USE |
| Difficulty ladder | plan 1 E | mechanisms m.t55.*, L1-L4, >= 25% at L3-L4, twin rule, C2 <= 70% on L4 | PRE-FREEZE FIX-TRIGGER |
| Check at generation | OWNER-ROW, plan 16.1 | every row answer-checked and G13-stamped when made; P-17 replaced | PRE-FREEZE KILL |
| Exports | build order L-T | ledger simulator exported read-only to L-K | infra |
Family size: T55 stays 3,000 rows; every lever is a substitution, never an addition. Kill granularity unchanged (G4): T55 is killed or kept whole.
The two held-out violation types of ruling 5 (seeded draw, dev-only, outside the 3,000) are unchanged.

## 1. Binding conditions carried (word for word from G0_APPROVALS.md)

T55 round 1: "Binding conditions (gold order fixed now, so solvers A and B cannot read it differently):
- C1 B3 is first-match in this order: (1) no violation = ACCEPT; (2) violation caused by the call's own arguments
  (visible) = FIX_ARGS; (3) violation on a WRITE = ASK; (4) READ, first occurrence = RETRY; (5) READ, recurrence =
  SWITCH_TOOL if an equivalent tool is listed, else ASK.
- C2 B6 is first-match in this order: (1) changed and calls_used < P_cap = KEEP_POLLING; (2) changed and calls_used >=
  P_cap = ESCALATE; (3) not changed for < L calls = KEEP_POLLING; (4) not changed for >= L and an alternative exists =
  BREAK_LOOP_ALT; (5) not changed for >= L and the card marks the goal non-waitable = STOP; (6) otherwise ESCALATE.
- C3 P-4 is widened. The exhaustive truth-table test (rule table = A's evaluator = B's evaluator, 100%) covers B1, B3, B5
  and B6 as well as B2."
"Rulings: 1-2 the tables and escalation cards are approved with C1-C3. 3 the observability check P-10 with a 2% pilot drop
tolerance is approved. 4 the B5 thresholds are approved (both published settings present, each card <= 25%). 5 the two
held-out violation types are drawn by seeded draw before any pilot. Their rows are dev-only, outside the 3,000. 6
approved (k_eff bars as written; G5). 7 see G2. Sub-block drop is not adopted (G4). The with-tool-outputs primary view
is accepted, because the error is the content."
Round 2: "T55: the section 9 sub-block drop question is not adopted (G4). The C1-C3 gold orders go into 3.2." "All 8: 'Solver B =
separate Sonnet high session' means CODE written by that session (G1)." Global rulings G1-G10 bind unchanged.

NOTE (a reading the build skeptic checks): the body's 3.2 text still lists the B3 and B6 rules in the pre-ruling order. C1 and C2
above REPLACE that order; the code and both solvers implement C1 / C2, and the truth-table test (C3) pins it.

CLAUSE LIST for the ruling-to-code conformance record (plan 16.1 step 0; fresh Sonnet high maps, Opus signs; proposed test ids)
| Clause | Text (short) | Test |
|---|---|---|
| C1 | B3 first-match order ACCEPT, FIX_ARGS, ASK(write), RETRY(read, first), SWITCH_TOOL / ASK (read, recurrence) | [t55_c1_b3_order] |
| C2 | B6 first-match order (six rules) | [t55_c2_b6_order] |
| C3 | exhaustive truth tables: rule table = A = B for B1, B2, B3, B5, B6 (B2 also = two-world simulation) | [t55_c3_truth_tables] |
| Rl-3 | P-10 observability, pilot drop > 2% = fix | [t55_p10_observability] |
| Rl-4 | B5 cards: both published settings present; each card <= 25% of B5 | [t55_p19_card_diversity] |
| Rl-5 | two held-out violation types by seeded draw before any pilot; dev-only | [t55_heldout_viol_types] |
| G1 | solver B = code written from G0-lite + addendum; B2 replay event-sourced | [t55_solverB_independent] |
| G3 | no pilot tuning; ONE combined fix | [t55_fix_log_single_iteration] |
| G5 | one probe harness; permutation and injected-leak sanity checks | [t55_probe_harness_sanity] |
| G6 | mean <= 800; none > 1,536; > 1,024 on <= 10% (A14: T54 addendum 11.1) | [t55_token_rule_g6] |
| G10 | decision_spans with roles; wrapper_spans separate | [t55_decision_spans_roles] |
| LIMBO | no LIMBO number in any row, card, pool or bar | [t55_no_limbo_numbers_in_pools] |
| INV | gold labels are invariant to lever fields (wrapper, transform, format, layout) | [t55_rules_ignore_lever_fields] |
| V32-1..V32-12 | the new gates in section 6 | [t55_p32_*] |
Part S clauses S.2-S.9 as in the T54 addendum.

## 2. Sizes by substitution (the family stays 3,000)

Sub-block totals and label mixes of the body (section 4) are UNCHANGED. Levers take rows inside the sub-blocks; the plain rows they
replace are drawn pro rata by label and 2x2 cell so the label mixes, the 2x2 cell shares (each >= 8% of the family) and the pair shares
hold on the whole sub-block and on each lever slice (6.1 V32-5). One lever_tag per row (S.1); A16 stacks.
| Sub-block | Rows | A12 perturbed | A10 wrapped (cond.) | A14 long (cond.) | Plain rows (all levers built) |
|---|---|---|---|---|---|
| B1 CLASSIC | 900 | 70 | 50 | 40 | 740 |
| B4 BLIND-RETRY (pairs) | 400 | 60 (30 pairs) | 30 (15 pairs) | 0 | 310 |
| B2 AMBIGUOUS-WRITE | 600 | 0 | 40 | 20 | 540 |
| B3 IMPLICIT-ERROR | 500 | 40 | 30 | 30 | 400 |
| B5 DENY-ESCALATE | 300 | 30 | 0 | 0 | 270 |
| B6 LOOP-POLL | 300 | 0 | 0 | 60 | 240 |
| Total | 3,000 | 200 (6.7%) | 150 (5.0%) | 150 (5.0%) | 2,500 |
If the Fri 23 probe says do not build A10 and/or A14, those quotas revert to plain rows. A12 is unconditional. Pair members carry the
same lever tag and the same wrapper / transform / layout (S.3, S.4). Dev-only held-out rows (S.2) are extra and outside the 3,000:
120 rows (4%): wrapper 30, transform 30, format 30, layout 30 (wrapper and layout exist only if A10 / A14 are built), plus the
body's held-out violation-type rows.
A16 covers output-bearing rows = every sub-block except B5 (B5 is the stripped `view.primary` variant): 2,700 rows, 40% in a
non-default training format.

## 3. LIMBO citation correction (class design unchanged)

CORRECTION [CRIT H2; arXiv 2609.29095, fetched 18 Oct 2026; plan 1 B.6]: LIMBO's rates are lost-ack 0.5%, misleading HTTP 500 8%, late
commit 56%, redelivery 74%. The earlier sentence "frontier models duplicated a lost-ack write in 56-74% of cases when read-back cannot
show the outcome; keys cut duplicates 28% to 4%" is WITHDRAWN. Consequences, all binding:
(i) No LIMBO number drives a decision, a size, a share, a bar or a report threshold in T55.
(ii) B2 is unchanged: the AMBIGUOUS-WRITE class and its gold (the cheapest action that yields exactly one effect in every world consistent
with the visible facts) come from our own ledger simulation; the key-first, then read-back, then ask order is a POLICY the card states
(body risk 3), not an empirical claim.
(iii) Body sections 3.2 (B2 "Idea source") and 6: the words "the key/read-back finding" are read as "the key / read-back design idea".
(iv) No row, card line, wording pool entry or doc string cites LIMBO or a percentage from it (CPU lint over the pools: 0 matches).
(v) FLAG for the orchestrator: the stripped excerpt training_inputs/excerpts/tools_s5.md item 8 still contains the withdrawn
56-74% / 28% -> 4% sentence. It belongs to L-0 and was not edited here; the lane builder does not use that sentence.

## 4. How the levers apply to T55 (specs in PART S)

- A12 (S.4): perturbs the user turn and the `detail` / phrase channel text of B1, B3, B4, B5 rows. Never the code field, error-class
  tokens carried in the code channel, counters, thresholds, ids, `retry_after`, or any number. In a B4 pair the shared leading phrase is
  perturbed identically in both members; the pair edit (the `detail` field) is perturbed with the same transform family where present;
  gate P-8 (identical code and leading phrase, only detail differs) is evaluated AFTER perturbation on the normalised text and also
  on raw bytes for the code field.
- A16 (S.6): the formats re-render the outputs of B1, B2, B3, B4, B6 (`view.with_outputs`). The record-level channel set (code / phrase /
  hint) is preserved: B's normaliser must recover the same channel set, so P-9 holds on rendered rows. Decoration lines (progress bars,
  pagination footers) carry no number that is not already in a data field of the same output with the same value, so B6's `progress`
  signal is never duplicated by a conflicting decoration.
- A10 (S.3): wrapper before or after the user message of B1, B2, B3, B4. Wrappers contain no instruction about retrying, stopping,
  asking, polling or continuing (lint), so RETRY / FIX_ARGS / SWITCH_TOOL / ASK / STOP labels are unchanged.
- A14 (S.5): `view.long`: up to 12 turns of outputs (the body's "last 4 turns" cap is lifted for this slice only). B6: the call-history
  list of 20-60 calls; the evidence position (`ev_pos`) is where the LAST state change sits in the history (tail = normal; middle / head =
  progress long ago and a stall now = the hard BREAK_LOOP case; interleaved / split = two changes separated by identical calls).
  B1 / B3: the diagnostic output sits among earlier coherent steps. B2: the key / read-path facts sit in a tool list of up to 25 tools.

## 5. Difficulty ladder (plan 1 E; CRIT D1, D2)

| Mechanism id | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| m.t55.channel (B1, B4) | class in code + phrase + hint (3 channels) | 2 channels | 1 channel, phrase only | 1 channel, phrase only, on a recurrence row whose class token appears only in the previous attempt's output |
| m.t55.attempt | attempt a <= R_cap - 2 | a = R_cap - 1 | a = R_cap | a = R_cap and the label flips with each of two visible facts (equivalent tool listed; idempotent / key offered) |
| m.t55.implicit (B3; the 6 trained violation types) | negative_value, empty_when_count_stated | duplicate_in_unique_list, order_violation | id_not_in_prior_list, scale_mismatch | stale_echo, parts_total_mismatch (comparison or arithmetic needed) |
| m.t55.ambig (B2) | key offered | read path only | neither (ASK) | step 2 (read-back shown) among >= 3 read tools of which one reads the affected fact |
| m.t55.deny (B5) | counters >= 2 below thresholds | n_c = K_c - 1 | n_t or n_w at its threshold, n_c below | two thresholds near + a hard-rule goal + an alternative path (rule order decides) |
| m.t55.loop (B6) | monotone progress | identical calls WITH progress | cosmetically varied arguments, NO progress | progress only in a secondary field among >= 3 fields, or the last change far back in a long history |
| m.t55.length | < 500 tokens | 500-800 | 800-1,024 | > 1,024 |
Protocol in S.7; the alarming/calm x risk-present/resolved quad is NOT mandatory for T55 (it is for T50, T51, T53, T41c, T56). The twin
rule applies: B3's valid-but-odd ACCEPT rows (>= 30% of B3) are the easy-looking opposite-label twins of the hard implicit-error rows.

## 6. Gates (IDs V32-n; bars are the body's: binary AUC <= 0.55 with bound <= 0.60; k-way balanced accuracy <= 1/k + 3 pp with
bound <= 1/k + 6 pp, k_eff as in the body; grouped by scenario-template id and pair id)

6.1 PRE-FREEZE KILL (CPU, data only)
| ID | Gate | Bar |
|---|---|---|
| V32-1 | A12 survival: every decision span of a kept perturbed row restored by the recorded inverse (S.4); no code / number / id / counter / closed-vocabulary span touched | 100% of kept rows; > 20% of attempted drops = transform parameters revised in the one fix (design value) |
| V32-2 | A16 label preservation: B's label on the normalised render equals A's; channel set recovered equals the record's; 256-token cap after formatting; format-id -> label probe | 100% kept; 0 over cap; AUC <= 0.55 / bound <= 0.60; each trained non-default format 3-8% of output-bearing rows |
| V32-3 | A10 (only if built): wrapper lint 0 violations; clean twin present for 100%; wrapper-family -> label probe (binary where the sub-block has two outcome groups, else k_eff of the sub-block) | AUC <= 0.55 / bound <= 0.60; k-way bars as in the body |
| V32-4 | A14 (only if built): B's label on the long render equals A's; `ev_pos` -> label probe; length-only -> label probe; token budget S.5 | 100%; AUC <= 0.55 / bound <= 0.60 each |
| V32-5 | Lever slices: sizes vs section 2 (+-2 pp of family); label mix within +-5 pp of the sub-block for slices >= 100 rows; lever_tag -> label probe pooled; 2x2 cells each >= 8% of the family after substitution | pass; AUC <= 0.55 / bound <= 0.60 |
| V32-6 | Ladder: tags on 100% of rows; L3-L4 >= 25% of the family and >= 20% of each sub-block; L4 >= 8% of the family (design values for the last two); twin rule >= 80% of L3-L4 rows | pass |
| V32-7 | Held-out hygiene: dev-only rows (levers and the two violation types) tagged `split.dev_only`; absent from every pool and from the mix manifest | 0 leaks (mix guard test) |
| V32-8 | Stamp drop trigger (replaces body P-17): drops for reasons other than exempt scaffolding or OHS-5 collisions, on ALL pilot rows and each full-generation day | <= 1% of rows; > 1% = the one combined fix; OHS-5 collisions dropped row by row, <= 5% of family not the fix |
| V32-9 | Hash export: all templates, wording pools, wrapper pools, filler programs, layouts, format renderers in the Thu 22 export v1.1; any later change = new export + re-stamp (16.1 step 6) | 0 unexported templates at the first row |
| V32-10 | Lever invariance: the rule functions of B1-B6 take no lever field (wrapper, transform, format, layout, ladder) as input; a label recomputed from the lever-stripped normalised record equals A's | 100%; [t55_rules_ignore_lever_fields] |
| V32-11 | Structure-only probe (body P-5) with the feature set EXTENDED by format id, wrapper family, transform family, layout, `ev_pos` and ladder level | same bars as P-5 (k=5 <= 23% / <= 26%; B5 / B6 k_eff as in the body) |
6.2 PRE-FREEZE FIX-TRIGGER (model read; never a kill)
| V32-12 | C2 (C1 if C2 has no weights) accuracy on L4 rows, once on the 1,000-row pilot (L4 >= 80 rows) | <= 70%; a miss is folded into the ONE combined fix by raising the m.t55 parameters; after the fix a report line |
6.3 POST-TRAINING REPORT (needs the trained C2.1; never a kill)
| ID | Report line | Pre-registered comparison |
|---|---|---|
| R32-1 | Held-out lines: held-out wrapper, held-out transform families, held-out format, held-out layout vs in-family accuracy (Wilson CIs) | report, labelled "our dev rows" |
| R32-2 | Ladder: accuracy per level and per mechanism | report |
| R32-3 | A16 formats: accuracy per trained format and for the held-out format; explicit-minus-implicit gap (body R-3) per format | report |
| R32-4 | Body lines R-1..R-7 unchanged (R-4 held-out violation types stays) | as written |
Evaluation scope note (not a bar change): the sub-block probes P-5, P-6, P-7 are computed POOLED across sub-blocks of equal k on the
1,000-row pilot (B5 has 300 rows, B6 300) and per sub-block on the fully built family. Opus please confirm.

## 7. Check at generation (OWNER RULE; replaces the "200-row G13 pilot" everywhere in this family)

Owner, 18 Oct (binding): "If you're building one row, check that row at that same point and that's it ... then train."
Every T55 row is written ONLY through the stamp wrapper (plan 16.1 step 2). Per batch (<= 500 rows, same day):
(a) ANSWER CHECKS (each a per-row drop with a logged reason code): solver A = solver B on the record for B1, B3, B4, B5, B6; for B2 the rule
table label = the five-option two-world simulation = B's event-sourced replay, RUN PER ROW (the ledger simulation is cheap), in addition to
the exhaustive truth-table test at conformance (C3); the B3 invariant checker per row, with cause observability; observability
assertion P-10 (B's parser recovers every fact the label needs from the rendered row; drops counted; > 2% in the pilot = fix, ruling 3);
render-fidelity (the re-parsed record gives the same label); names guard (P-15); output lint (P-14; also covers decoration lines);
token rule G6; PII scrub; Haiku-reword slot round trip (P-13: numbers, counters, ids, thresholds, negations survive, else drop-only);
decision_spans export (G10) and the A12 survival check; A16 normaliser check; A10 lint; A14 label-preservation.
(b) G13 STAMP against EVERY registered target with every G13 method listed for that target (R6 scaffolding exemption; OHS-AC binding for
new rows; OHS-5 export loaded from Sat 24).
(c) The stamp (row id, registry sha, method-set version, generator code sha, verdict) goes into the row manifest.
A failed row is dropped and logged (row id, target, method; never the matched text); no unstamped or failed row enters a pool.
Quota-driven generation, pair closure (partner stays, marked orphan), pilot rows are real rows, rows from template ids changed by the
fix are regenerated: exactly as T54 addendum section 7. Orphans are counted against the pair-share bars (P-16 >= 30%; B4 100% by design,
gate = kept pairs).
(d) FIX TRIGGER ON ALL ROWS: ALL 1,000 pilot rows and each full-generation day.
(e) SET-LEVEL CHECKS ONCE per family, on the pilot and on the fully built family: A50 G6 at size, A49c balance, wording variety (>= 50 per
question form, none > 2%), matched-pair share, ladder + V32-12, the G5 probe harness (P-5, P-6, P-7, P-9, P-19, V32-2..V32-11), G5-H /
G3-H reads (two Haiku medium solvers on 300 rows, one read of 100% of free-form rows, Sonnet medium adjudicates, Opus high A43(d); a flag
counts only after adjudication, confirmation and a program re-run, G2). Not repeated at the mix.
GATE DISPOSITION (body 5.1 under v3.2): P-1 kept (per row and set); P-2 kept; P-3 kept; P-4 kept and widened (C3; conformance test, re-run
on every code sha change); P-5 kept with V32-11 extension; P-6 kept; P-7 kept; P-8 kept (see section 4); P-9 kept (record level and
rendered); P-10 kept (per row); P-11 kept; P-12 token budget kept; P-13 kept (per row); P-14 kept (per row); P-15 kept (per row); P-16 kept;
P-17 SUPERSEDED by V32-8; P-18 kept at the stamp; P-19 kept.
Body section 9 fix menu additions: V32-1 / V32-2 fail -> revise transform / format parameters; V32-8 fail -> generator change for the
template ids in the hit report (row ids and method only); V32-12 fail -> raise the m.t55 level parameters. The body's P-4 fix entry
(ledger simulator or rule table corrected: a bug) is unchanged.

## 8. Exports

LEDGER SIMULATOR (tool_engine.ledger, state-machine form A): exported READ-ONLY to L-K (T59 "tool failure / risk appearing mid-run"
triggers, T60 keep / drop). Contract: module path, API (new_world(spec), commit / lose_ack / read_back / offer_key, effects list), code
sha, CPU test ids; a change after export is a new export with a notice to L-K. Solver B's event-sourced replay is NOT exported.
G10: decision_spans (roles) for user turns; wrapper_spans separate.

## 9. NAMES needed (names only, for manifest v1.1; v1 is frozen)

T55-specific: ladder mechanisms `m.t55.channel`, `m.t55.attempt`, `m.t55.implicit`, `m.t55.ambig`, `m.t55.deny`, `m.t55.loop`,
`m.t55.length`. No new card, verb, parameter role, error class, violation type, field key, language or runner. Existing T55 names unchanged.
Shared L-T lever names, identical to the T54 addendum section 9 (L-0b dedupes): carrier formats `obsfmt.plain_kv`, `obsfmt.json`,
`obsfmt.yaml`, `obsfmt.ansi`, `obsfmt.crlf_tab`, `obsfmt.wrapped`, `obsfmt.paginated`, `obsfmt.progress_noise`,
`obsfmt.truncation_marker`, `obsfmt.key_order_shuffle`; layouts `layout.head`, `layout.tail`, `layout.middle`, `layout.interleaved`,
`layout.split`, `layout.rep_flood`; fillers `filler.coherent`, `filler.neutral`; `view.long`; `bucket.filler`; wrapper families
`wrap.authority`, `wrap.urgency`, `wrap.roleplay`, `wrap.fake_approval`, `wrap.benign_justification`, positions `wrap_pos.prefix`,
`wrap_pos.suffix`; transforms `xform.diacritics`, `xform.spacing`, `xform.leetspeak`, `xform.homoglyph`, `xform.zero_width`, held out
`xform.fullwidth`, `xform.bidi`, `xform.upside_down`; row metadata `lever.a10`, `lever.a12`, `lever.a14`, `lever.none`,
`split.dev_only`, `ladder.l1`..`ladder.l4`. External sources: none.

## 10. Timeline for this family (UTC)

Sun 18: this addendum. Mon 19: Opus approval; seeded held-out draws recorded (S.2) and the body's violation-type draw recorded, before
any pilot. Tue 20: ledger simulator (state-machine form A) and the B1-B6 evaluators, format renderers and normaliser, transform and
wrapper libraries (code, CPU tests, no rows); solver B session starts (event-sourced ledger replay, stand-alone evaluators, from the
G0-lite + this addendum). Wed 21-Thu 22: build skeptic; conformance map in a SEPARATE fresh session; hash export v1.1 Thu 22 (includes
A10 / A14 pools either way). Fri 23: orchestrator's free probes. Sat 24 18:00: conformance record signed, else no T55 rows. Sun 25: pilot
through the stamp wrapper; Mon 26 readout; ONE combined fix by Wed 28; full generation Tue 27-Wed 28; set-level gates once on the built
family; kill rule at the data freeze.

## 11. Items for Opus (checklist) and flags

1. G6 and A14 (T54 addendum 11.1): the same exemption question; T55 adds the `view.long` lift of the "last 4 turns" cap for the slice.
2. Dev-only held-out rows are outside the 3,000 (ruling 5 precedent): confirm 120 rows plus the body's violation-type rows.
3. V32-11 extends the P-5 structure feature set with lever fields (so format or wrapper leaks are caught): confirm.
4. Evidence position for B6 is "the last state change" (section 4): confirm.
5. Design values needing OK: L3-L4 floor 20% per sub-block, L4 floor 8%, twin rule 80%, A12 drop trigger 20%, slice sizes 200 / 150 / 150.
6. Sub-block probes pooled on the pilot, per sub-block on the built family (section 6): confirm.
7. A15 (format dialects) is not in the L-T assignment (T54 addendum 11.4); T55 renderers take a `dialect` parameter, default = current.
8. The excerpt tools_s5.md item 8 still carries the withdrawn LIMBO sentence (section 3 (v)): L-0 owns the file.
9. hardest.md mechanism names were not available (no stripped excerpt in my scope); the ladder is program parameters.

---

## Opus batch-1 rulings v3.2 (Opus 5.5 high, Sun 18 Oct 2026 UTC; source: families/G0_APPROVALS_v32.md; binds over this file)

Global rulings GV1-GV9 of families/G0_APPROVALS_v32.md bind this file (GV1 one A10 build rule: flip = predicted label differs
wrapped vs unwrapped, build iff >= 10 of 200, no result by Fri 23 18:00 UTC = not built; GV2 role-play and benign justification
held out in every lane; GV3 one A14 build rule: >= 5 pp gap and bootstrap lower bound > 0; GV4 G6 binds A14, no exemption; GV5 a
G13-hit row retires its spec and its whole group, never re-worded, triggers read first-pass drops incl. collateral; GV6 one
perturbation library pert.*, zero_width = U+200B only, fullwidth / bidi / upside_down held out everywhere; GV7 A15 dialect rows in
L-A only; GV8 pilot-pooled sub-block probes, built-family read binds; GV9 held-out dev rows never trained, mix guard excludes them).
VERDICT: REVISE -> APPROVED after fix (applied in place): section 0 A14 line -> GV3 / GV4.
Binding conditions: T55-B1 items 2-5 confirmed (120 dev rows outside; V32-11 extension; ev_pos = the last state change; design
values). T55-B2 item 8: L-0 removes the withdrawn LIMBO sentence from tools_s5.md (orchestrator task). T55-B3 items 1, 6, 7, 9 ->
GV4, GV8, GV7, name-only.
