# F2 G0 spec: rule arithmetic, money, quantities and dates (v7, re-review round 4 and A16.1 (g) applied; frozen)

**XF (3 Oct 2026):** cross-family alignment applied. Section XF at the end governs where any earlier section differs;
the body text and the resolved-ambiguity tables have been edited to match it, so each rule is stated once.

Status: G0 spec v7 (4 Oct 2026), spec text only. **Frozen:** `G0_FROZEN.json` holds this file's sha256, and the
file is read-only for everyone from the freeze on. v1 was reviewed by a second session (59 ambiguities A01-A59, 20 spec
conflicts C01-C20; resolved in v2, listed in section 10). v2 was re-reviewed by a fresh session (30 ambiguities
R1-01 to R1-30, 7 spec conflicts SC1-SC7; resolved in v3, section 12). v3 was re-reviewed again (21 ambiguities R2-01
to R2-21, 4 spec conflicts SC8-SC11; resolved in v4, section 13). v4 was re-reviewed a third time (12 ambiguities
R3-01 to R3-12, 5 spec conflicts SC12-SC16; resolved in v5, section 14). Round 3's remaining items (12 ambiguities
R3-13 to R3-24, 2 spec conflicts SC17-SC18) are resolved in v6, also in section 14. v6 was re-reviewed a fourth time
(11 label-flip ambiguities R4-01 to R4-11 and 1 spec conflict SC19, `G0_OPEN_r3.json`), and the cross-family review r2
named F2 in one issue (XC-01, left-out keys; `G0_CROSS_ISSUES_r2.json`); all 13 are resolved in v7, section 15. v7 also
applies PREREG_FINAL amendment A16.1 (g) to every F2 choice row as rule CP1 (2.1). Every item is resolved in the body
below.
Where a later table changes an earlier row, the later table governs (15 over 14 over 13 over 12 over 10) and the earlier row
has been edited to the same rule. Conflicts are settled in favour of `C_DATA_SPEC.md`
v4. Items only the orchestrator can change (C_DATA_SPEC or register text) are in section 9. Section 11 holds the
1-page spec per generator that G0 asks for (SC7). Follows `C_DATA_SPEC.md` v4 (2.1, 2.2 F2, 2.4, 6, 7, 8, 10) and
`C_TRAIN_RECIPE.md` v4, with PREREG_FINAL amendments A15, A16 and A16.1.

**G14 order rule.** Until the sealed sha256 was committed (PREREG_FINAL A15, 3 Oct 2026), this file was the only F2
output: no generator code, rows, worked examples, domain packs, style or wording pools or codebooks existed. From A15
on they may exist, but no F2 generator runs before this G0 is frozen with 0 open label-flip ambiguities (A16).
Closed operator lexicons (meaning-bearing operator phrases mapped to SEM rows, no domain words, names or templates) are
G0 semantics and allowed before the freeze; they pass the 7.2 seed decontamination and the counts-only sealed template
compare before any use (XF17). Every `<...>` below is an abstract placeholder, not content.

**Status of the quoted clauses in section 2 (C15).** They are **meaning statements**: each fixes one semantics per
dimension, shared by solver A, solver B, the parser and the G0 reviewer. They are not a wording pool, a style pool or a
template set. Surface wordings are written only after the sealed freeze (format agents, step 4), and each must map to
the same SEM id in the parser lexicon (3.3). A meaning statement may itself be used as a surface wording only after it
passes the 7.2 #8 template check (dev and eval wordings, including dev_negwords and the blocked negation frames named in
C_DATA_SPEC F5) and the orchestrator's sealed template comparison (exact match and 8-grams). This file contains **no
question frames and no negation templates**: N1 and Q1 define semantics only. The truth frame (TF) of N1 is defined by
its meaning; the one phrase cited for it ("Is it true that <P>?") is XF10's own, and the phrases N1 and Q1 list are bans,
not a pool.

Builder inputs (allow-list): the two spec files, `LICENCE_REGISTER.md`, this folder. F2 never reads replay rows, dev,
eval, sealed, OHS or any Jev path; overlap checks against them are run by the QC program and the orchestrator (7).

---

## 1. Family summary

| Item | Value |
|---|---|
| Skill | Compute an amount, count or date under caps, floors, proration, tiers, stated rounding and exceptions, then decide a threshold or pick the value. Everything is decidable from card + text; no outside facts (no real tax rates, holidays, exchange rates, weekdays) |
| Decision forms | **choice** (value, date, count, band, named outcome, or inverted case list), **yes/no** (threshold or on-time decision; closed-world cards only), **abstain** ("<NEI option>" on every open-world row; "None of the listed" on some closed-world rows; never both on one row) |
| Ordinal | **No ordinal rows.** Band and named-outcome rows are not marked ordinal, by the rule C_DATA_SPEC 2.4 applies to F8 bins and UCI classes, and by its enumerated list (every F7 row, every commit Score row, replay rows with level numbers), which the recipe's A4 term was sized on (about 4,350 round-1 rows: F7 + commit Score). No option text carries a level number or "Level k"; masked IDs are unordered. The builder asserts that no row carries `meta.option_level` (C14). Fallback (SC4a): the builder also writes, per band and named-outcome row, the band order (option text to edge rank) to a side file outside `meta`, so that if the orchestrator rules these rows ordinal, `option_level` is added by program and G18 runs without regeneration |
| Labels | Hard labels only. No `gold_probs`; F2 is not in `kd_full_src` |
| Rows (r1 / r2) | 3,150 / 6,300 (7% of own rows); generate about 1.5x, then stratified selection by whole twin set (3.6, G9) |
| Cards (r1 / r2) | >= 80 / >= 150; rows per card max 128 (all variants of the card together), median about 40-45. **One F2 card per pack** (C_DATA_SPEC 2.1 read literally inside the family: any two F2 cards differ in pack and in label schema or rule set; SC4b), so F2 uses >= 80 / >= 150 distinct training packs from the shared pool (>= 200 / >= 300), plus separate held-out packs for S5 and the sweep. Clause-flip twins sit in planned flip variants of their base row's own card (3.6, 3.7). >= 5 wordings per card from a >= 30 pool (pool written after the freeze) |
| Label schemas | One per card (R1-19): YN-T yes/no threshold; YN-D yes/no on time or late; CH-V value choice; CH-D date choice; CH-C count choice; CH-B band choice; CH-O named-outcome choice; CL inverted case list (3.7) |
| World | Closed-world cards about 87%; open-world cards about 13% (r1 10-12, r2 18-22), choice-only (CH-V, CH-D, CH-C, CH-B, CH-O; never CL), from S1, S3 and S4 (3.5). S5 is closed-world only (R1-01) |
| Lengths | Counted with the real tokenizer on the trained and served prompt, `decoder_io.user_msg(row)` under cygnet + schema_branch_mark, where `instructions` and the option texts appear twice (A16.1 (g); CP1, 3.7). Median 500-900 tokens by this count; every row < 1,900 (builder check, 3.7), so no F2 row reaches 2,000 under any count that counts `instructions` twice |
| Licence | `meta.licence` = "CC0 1.0 (program-generated)". `persona_seed` (O*NET code) is copied from the pack when present; the pack declares O*NET (`gd_onet_occupation`) as a 3.H parent, whose `no_new_rows` class passes for persona seeds (C_DATA_SPEC 2.1 F4); O*NET is credited in the third-party notices file. Register note: section 9 (C16) |

### 1.1 Depth (one definition, used everywhere in this file)

`meta.depth` = the number of **unstated arithmetic operations**, computed by program from the canonical operation graph
(never hand-assigned per sampler). A node whose result the text prints is "stated" and does not count. Parallel
branches all count (for example X3's "compute each exception alone" counts every branch), with one exception: on an
inverted case-list row each case is a separate problem, so **depth = the maximum over cases** of the per-case depth,
and the selection-step cap applies per case; the row logs `edge` "cases:<n>" (R1-11). **Every case on one case-list
row falls in the same row group below** (A asserts; R2-21), and the row counts in that group for the section 6 depth
shares: `meta.deep` = true only for group (d), "stated_intermediate" only for group (c), and "ops:<n>" with n = the
largest per-case total. Every row has **at least 1 unstated operation** (R1-12): a row whose answer needs no
arithmetic (a band lookup on a stated amount, an on-time check against a fixed "by <D>" date) is not generated. Node
list (fixed):

| Node | Counts |
|---|---|
| add or subtract (a sum of k terms = k - 1 nodes) | 1 each |
| multiply; divide | 1 |
| percent-of (base x p/100); percent-off (base x (1 - p/100), R8); rate change by points or by percent (R6) | 1 |
| scale by a/b (proration: amount x days used / n; the price before a fee backed out of an inclusive price: listed x 100 / (100 + p), X7) | 1 |
| unit conversion; currency exchange | 1 |
| width of a band part (hi - lo, or amount - lo) | 1 (0 when lo = 0) |
| date +/- N calendar days; month addition (D8; forward only, R4-11); calendar day count (D5); business-day count (D14); an act's day offset from the last allowed day on an S4 window row (act date - last allowed day, one node however many windows the table has; R2-06) | 1 |
| date + N business days (D6b) | 1 if N <= 10 and the window holds <= 1 holiday; otherwise 2. A 2-operation addition appears **only in deep items and sweep items**; non-deep rows never contain one (R1-13) |
| weekday of a date (always stated: D9 states it for every anchor and listed holiday, and the calendar strip states it for every candidate date whenever D6a is shown, R1-14, R3-08); comparison with T; min / max (cap, floor); rounding; band lookup; partial-unit rule; roll rule; exception switch; tie-break | 0 (selection steps) |

Selection steps are capped at 3 per non-deep row (per case on case lists) and logged as `edge` "sel:<k>".

**Printed day counts are stated inputs (R1-15).** A day count printed under the day-count rule below counts in neither
`meta.depth` nor the "total operations" of the row groups: the reader is given it, like any other input. B re-checks it
like a printed intermediate (a mismatch is a render bug). Example of the arithmetic: a proration with printed days used
and one scale step has total operations 1 and depth 1.

**Row groups (disjoint; C5, A30).** C_DATA_SPEC F2: "at most 2 operations, or more operations only when the text states
each intermediate value". "Total operations" counts every node of the table above except printed day counts. So:
- (a) plain depth 1: total operations 1, nothing stated except printed day counts;
- (b) plain depth 2: total operations 2, nothing stated except printed day counts;
- (c) stated-intermediate rows: 3-5 total operations and **every** intermediate result printed (only the final
  operation is unstated), so `meta.depth` = 1, `edge` "stated_intermediate" and "ops:<n>". Solver B re-checks every
  printed intermediate; a mismatch is a render bug. **Intermediate** = the output of every arithmetic node of the
  table above except the final one (R2-13). On these rows **every number that enters an arithmetic node is printed in
  the text** (a stated input or rule value, or a printed intermediate). So a selection step may sit between two
  arithmetic nodes only when its output is always one of its printed inputs (a cap or floor, a rate or value picked by
  an exception gate, a band lookup or a D13 date, a tie-break); a selection step that makes a new number (rounding, a
  roll, a month-end clamp outside a month-add node) sits only after the final arithmetic node, and X8 acts only on the
  final amount (R4-08). Partial-unit rules (R5, U3) never occur on group (c) rows: they act first on a line's own
  quantity, before its pricing node (R4-04), so their output would be an unprinted number entering an arithmetic node.
  Selection outputs are not printed. A asserts this (R2-13). **Printed intermediates are
  exact (R2-03):** each is its node's exact value, and A asserts that it is exactly representable at display
  precision (R7); otherwise the structure is resampled. A printed intermediate is never rounded for display;
- (d) deep items: 3-4 unstated operations, `meta.deep` = true, <= 10% of F2 rows (target 8%). They are training rows.
  The depth sweep (5) uses the same generator settings at depth 1-5 but its items are **separate instances** (held-out
  packs and styles, disjoint structure hashes), never training rows (C_DATA_SPEC 10; SC5).
No row has 3 or more total operations with only some intermediates printed.

**Day counts (C4, A11, A31).** C_DATA_SPEC F2: "State day counts when the card's rule needs them". So:
- Every day count that a later **arithmetic** step uses (days used in a proration, days late times a per-day charge,
  days in a sub-span) is printed as a number in the text. A computes it under the card's own D5 / D10 / D14 rules; it
  is a stated input (above). When the text also shows that count's endpoint dates, the card shows the matching D5 or
  D14 clause.
- A day offset that only a comparison or a window lookup reads is not a printed count: on S4 named-outcome rows the
  window is found by comparing the act date with the window's edge dates (S4, R2-06), and no days-late count is
  printed. Printing it would leave the row with no unstated operation (R1-12).
- A day count that is itself the asked target is never printed (it is the answer). Non-deep count-target rows span
  <= 31 days.
- A date offset (anchor + N days, or + M months) is not a day count: N comes from the rule, and the resulting date is
  1 operation. The resulting date is **never stated as the result**; it may appear unmarked in a calendar strip,
  among other dates (R1-26).

**Calendar strip (R1-14, R1-26).** A list of consecutive dates, each with its weekday, with no date marked. It is an
aid (`edge` "aid:strip"), not a stated intermediate, and the parser reads it as weekday facts only.
- When: (i) a day-offset (D4), business-day (D6b) or day-count (D5, D14) window is longer than 14 calendar days or
  crosses a month end; or (ii) the card shows D6a (business days are used, or D7 appears; R3-08), at any window
  length, so the weekday of every candidate date is stated. A month offset (D8) gets no strip unless D7 applies to it.
- Span: from the earliest relevant date minus m1 days to the latest relevant date plus m2 days, with m1 and m2 drawn
  independently and uniformly from 3-10. Relevant dates: the anchor (not on D8 rows), every act date, every option
  date, every listed holiday in range, the gold date, every named-error date of 3.4 (shown or not) and, on S4 window
  rows, every window edge date (R2-06), so the strip's ends never mark the answer.
- Length: at most 45 dates. If the span is longer, the anchor leaves the relevant set (a local strip; D9 still states
  the anchor's weekday); if it is still longer, the structure is resampled.
- Business-day additions follow the node table. The N <= 10, <= 1 holiday rule wins over the 14-day rule: such a window
  is 1 operation however many calendar days it spans.

### 1.2 Samplers (shapes differ: formula-first, label-first, table-first, calendar-first, statement)

| Sampler | Shape | Rows r1 / r2 | Cards r1 / r2 | Yes/no share |
|---|---|---|---|---|
| S1 | Forward formula graphs (formula first, prose memo) | 800 / 1,600 | 21 / 40 | 45% |
| S2 | Target-first boundary placement (label first, back-solved) | 850 / 1,700 | 21 / 40 | 70% |
| S3 | Tiered rate tables (table first) | 750 / 1,500 | 19 / 35 | 40% |
| S4 | Calendar and business-day rules (date rule first) | 750 / 1,500 | 19 / 35 | 50% |
| S5 (held out) | Line-item statements, payroll style | 0 (dev only: 400 + 60 sweep) | held-out packs | 50% |
| **Total** | | **3,150 / 6,300** | **80 / 150** | **51.7%** (inside 45-55%) |

Every training sampler stays under the 2,500-row cap over both rounds. The cap counts **selected training rows only**
(r2 totals include r1's rows); generated candidates and the >= 5,000-row QC sample do not count (A56).

---

## 2. Semantics table (G0)

### 2.1 Card clause sets and the presence rule (A03, A04, A47, C1, C9)

A card's text is fixed per **card variant** (3.7): every row of a variant sees the same clauses. A card has one base
variant and at most 2 flip variants, each one SEM switch away from the base variant (3.6).
- **Relevant (card level; R1-17).** A dimension is relevant to a card when the card's formula type contains the step it
  governs. Every "Shown when" condition of 2.2 is evaluated **per card**, over the card's formula type and the value
  ranges its sampler can draw for it: "can this condition hold for any admissible row of this card?" (for example R1
  "whenever rounding can change the label or a displayed value", X1 "whenever reordering can change the value of an
  askable node or a comparison's outcome", D7 "whenever the deadline can land on a non-business day", R5 "whenever a
  quantity is not whole", X8 "whenever the final amount could go below 0" (R4-08); D8 is shown on every card with a month offset,
  with no condition, SC17). If yes, the clause is relevant and a full card shows
  it. Row-level facts never add or remove a clause; they only drive row admission below.
- **Full cards** (definition styles one-line, one-line + examples, numbered decision list; about 85% of rows) show the
  clause of every relevant dimension.
- **Short cards** (about 15% of rows) show W0, the world clause, every clause whose Omission entry is "never", every
  dimension planned for one of the card's flip variants (3.6; R2-14), and each other relevant dimension with
  probability 0.5 (drawn once per card; every variant of the card omits the same ones). So the base variant and its
  flip variants all show a flipped dimension, and a base row on it can have that dimension decisive. R2, R3 and R4
  refer to R1's rounding, so they are shown only together with R1: a short card that drops R1 drops them too, and then
  every row on it is exact at display precision (R7 assertion; R1-18). On every row, R1 shown or not, the final value,
  the asked target node, every option and hook value and the value the question reads are on the display grid (R7;
  R3-13). **F2 has no no-card rows**, so every clause that
  can flip a label is in the card itself (C_DATA_SPEC G0): in the `card` field on yes/no rows and in `instructions` on
  choice rows (CP1, below).
- **Card vs document (R2-12).** The document holds **values only**: numbers, dates, names, category lists, yes/no
  facts, and tables or lists of them (rates, cap and floor amounts, band edges as plain numbers, N, holiday dates,
  line items). Every sentence or phrase that carries a SEM meaning of 2.2 (a world or calendar clause W0-W3, D1; a
  connective UN1, O1-O3, OR1, OR2; a comparator or range CMP1-CMP4, D2, D3, B1, B4; a date rule D4-D17 (D6a, D6b included); the OP money clause; a rounding, unit, exception or adjustment rule R1-R8,
  U3, U5, X1-X10, M3, M4, P1, T1) is in the card, and refers to document values by name ("the cap in the schedule",
  "the rate in row <ID>"). Inert additions follow the same rule: an inert line is a value line, never a rule
  sentence, and it is inert only through an attribute the card's rules already read (another entity, a date outside
  every period a rule reads, a line type or row ID that no rule names; 3.6, R3-12). The question carries its own
  comparator (CMP1-CMP3 only), outcome predicate and cues (OP, N1, Q1); option text carries no SEM phrase. The parser
  rejects a SEM phrase found in the document (a G3 failure).
- **Card placement in the prompt (CP1; PREREG_FINAL A16.1 (g)).** C trains and serves with decoder_io's cygnet style
  and schema_branch_mark layout, which prints the `card` field whole only on yes/no rows; on a choice row it shows only
  card lines "- <option text>: <definition>", appended to their options, and it prints `instructions` twice (before
  and after the text). "The card" in this file is the card text wherever that prompt shows it. Every F2 row is rendered
  by fmt1 `card.render_row_text` and passes fmt1 `card.loader_check` (must_show = fmt1 `card.must_show` over the card
  IR, question, wording and note) on 100% of rows before G3.
  - **Yes/no rows (YN-T, YN-D).** The card is the row's `card` field, printed whole; `instructions` holds the wording,
    the question and the answer note. No card line starts "- Yes: " or "- No: " (A asserts).
  - **Choice rows (CH-V, CH-D, CH-C, CH-B, CH-O, CL).** F2 writes **no option-definition line**: the `card` field is
    empty (null), and the card IR holds no entry named like an option text (A asserts), so nothing is routed to option
    lines. Every card block (W0-W3, every SEM clause of 2.2, the OP money clause, the CH-O outcome table, fragment
    examples, the few-shot block, the inverted frame and the task line) is laid out in the card style inside
    `instructions`, before the wording and the question (`render_row_text(qtype="choice", choice_card="move")`;
    under IP4 / IP5 the task line is the first / last part of `instructions`).
  - **State.** `state` holds the document only (values, R2-12): the record, S3 band tables (each band's name, masked
    ID or swapped word with its edges and rate, which are the band definitions of CH-B rows), the holiday line and the
    calendar strip, and on CL rows each case's values (3.4). Attack and inert lines go in `state` only (3.6).
  - **Options** carry only their own text: a value, date or count, a band or outcome name (or its masked ID or
    swapped word), a case reference (CL, 3.4), or an abstain option.
  - **Token caps** count `instructions` twice, because the layout repeats them after the text (3.7 length budget).
  A card has one schema (3.7), so its text sits in the same field on every row of every variant, and the presence
  rule below holds unchanged.
- **Rendering of absent and unknown values (R3-11).** On every F2 card the only blank cells are M3 amount blanks
  (closed-world cards only) and B1 edge blanks; on an M3 line the quantity and rate cells hold the XF06 zero marker
  "none" (SC19, 2.2 M3). Closed-world cards: an absent line item, condition or W3 field is left
  out (JSON and YAML: no key) or printed as a value ("0", "no", false); it is never written as "not recorded",
  "unknown", null or a blank. **A left-out key or field never means unknown on any F2 card (XC-01):** on closed-world
  cards it is absent (W1) or takes the stated W3 default, and open-world cards leave out no field a rule reads. Open-world cards: the one unknown field is the literal text "not recorded" in every
  container (JSON and YAML: the string "not recorded"), never null, "unknown", a blank cell or a left-out key; no
  field a rule reads is left out (W2). F2 never renders null or "unknown". **Holiday line (R3-23).** On every card that
  shows D6a, in both worlds, the document has exactly one holiday line, never left out: it lists the holiday dates (each
  with its weekday, D9) or, when the row has none, holds the value "none" (XF06's zero marker). The holiday line is a
  rule value, never the unknown field. A asserts; the parser rejects other forms (3.3).
- **Row admission.** A row may join a card only if (i) every dimension decisive for the row is shown, and (ii) the
  **joint invariance filter** passes: solver A recomputes the row's label under every combination (Cartesian product)
  of the filter alternatives of **all** omitted relevant dimensions together, and every combination gives the gold
  label. A row that fails goes to another card or is resampled. (At most a few thousand evaluations per row; CPU.)
- **Decisive.** Dimension d is decisive for a row when A's alt-label under some listed alternative of d (all other
  dimensions canonical) differs from gold. Decisive dimensions are logged as `edge` "sem:<ID>".
- **Printed numbers are held fixed (R1-16).** Every alt-label (decisive test, invariance filter, NEI status under an
  alternative) recomputes every **unstated** node under the alternative and holds every **printed** number fixed:
  printed inputs, printed intermediates, printed day counts and strip weekdays, because the reader is given them. A
  dimension whose whole effect is absorbed by printed numbers (for example D10 on a span whose sub-span counts are
  printed) is therefore not decisive on that row and may be omitted from a short card. Clause-flip twins (3.6) are made
  only where the flip changes no printed number, so a twin's label equals the base's alt-label.
- **Alt-label.** Yes/no: the yes/no label under the alternative. Value, date and count choice: the shown option whose
  value equals the alternative value exactly (nothing is rounded for display; an alternative value off the display grid
  equals no option, R3-13); if none, the "None of the listed" option if shown, else "no option". Band and named-outcome rows: the band or outcome of the alternative value if it is a shown option, else
  "no option". Case lists: the set of qualifying cases. Open-world rows: the NEI status and option label (3.5).
- **Presence never marks the trap.** A shown clause is shown on every row of its variant, decisive for that row or
  not. Tags that belong to a clause (the OR1 "(either or both)" tag, T1) are part of it and appear whenever the clause
  does, whatever the row's state. G7 tests the presence of every SEM clause against the label.
- **One governing rule per outcome (R1-04).** Each <B> (an outcome, an exception or a charge) is governed by exactly
  one connective rule: one UN1, O1, O2 or O3 rule (the conditions inside it may use OR1, OR2, "and"). Several conditions
  for one <B> are joined inside that one rule, never spread over two rules. A asserts this on the structure, and the
  parser rejects a rendered text with a second governing rule for the same <B>. So "only if" and "if" or "unless" never
  govern the same <B>.

### 2.2 The table

Columns: **Alternatives** lists the alternative readings; "T" marks the ones used for clause_flip twins; "filter" lists
what the invariance filter tests when the clause is omitted. **Omission**: "never" = shown whenever relevant (the
clause is the rule itself or a frame); "filter" = may be left out of a short card only under 2.1; "renderer" = a
rendering rule, not a card clause. Every "Shown when" condition is evaluated per card, over the card's formula type
and value ranges (2.1, R1-17).

| ID | Dimension | Card clause (meaning statement) | Solver meaning | Alternatives | Shown when / omission |
|---|---|---|---|---|---|
| W0 | Rule completeness (both worlds) | "These are all the rules. No other fee, discount, cap or exception applies, and an <item> is <due> only when a listed rule makes it <due>." | Rule set complete; an item no listed rule makes due is not due; only case fields can be unknown | none | every card; never |
| W1 | Closed world | "The record lists every <charge, payment and event> that happened: a <charge> it does not list was not made, and a condition it does not mention did not happen." | Absent listed-type line item (charge, payment, deduction) = 0; absent condition = false. No other numeric field is absent without W3 (A06). Absent means left out or printed as "0", "no" or false, never "not recorded", "unknown", null or blank (2.1; R3-11). W1 says what happened; which listed lines enter a computed amount is set by the rule that names its inputs (3.6; R3-12) | none (F2 has no world twins; the world never changes inside a card or a twin set; R2-10) | every closed-world card; never. One world switch per card (A21) |
| W2 | Open world | "Every <charge, payment and event> that happened is listed, and every other fact the rules use is given or shown as \"not recorded\". A field shown as \"not recorded\" is unknown: an unknown amount can be any amount of 0 or more, to the <display unit>; an unknown count any whole number of 0 or more; an unknown date any calendar date, except where a sentence of the record bounds that date; an unknown <category> any listed <category>; an unknown yes/no fact either. If the answer depends on an unknown field, choose \"<NEI option>\"." | Admissible domain and NEI rule of 3.5 (A01, A02). Every case field a rule reads (categories, numeric attributes, dates, yes/no facts) is printed or shown as "not recorded"; exactly one is "not recorded"; A asserts this, mirroring A06 (R1-05). An unknown field has explicit bounds only, never implied ones (3.5, R1-06), and A asserts that the NEI status and the label do not change when the row's natural precedences are added as bounds (3.5, R4-10). **Only an amount, a count, a date, a category or a yes/no fact can be unknown**; other quantities (durations, weights, distances, hours) are always printed (A asserts; R2-07). **The unknown field is never whether a <charge, payment or event> of a type the W2 clause names happened, and never a count of such items** (W2's "every ... that happened is listed" settles both): an unknown yes/no fact or count is an attribute of the entity or of a listed item (for example "member", "units used"); a listed event's date may be unknown, the event itself never (A asserts; R3-17). Every category field a rule reads on an open-world card has one explicit list of all its values in the card or the document ("<category> is one of: <values>"), with at least one value that no rule names; "listed" in the clause means that list, and the list is the domain (A asserts; the parser extracts it; R2-08). The unknown is always the literal text "not recorded", in every container (JSON and YAML: the string "not recorded"), never null, "unknown", a blank cell or a left-out key (2.1; R3-11) | none (no world twins; R2-10) | every open-world card; never. Open-world cards are choice-only (A24) |
| W3 | Stated default (closed world) | "If <field> is not given, use <D>." | absent field = D; "not given" = the field is left out (JSON and YAML: no key), never "not recorded", "unknown", null or blank (R3-11) | none | every closed-world card on which any field other than a listed line item or a condition may be absent; never. A asserts the coverage (A06) |
| UN1 | "unless" | "<Rule R> applies unless <C>. If <C>, <R> does not apply and <alternative or nothing> applies instead." | R applies exactly when C is false | none (misreading "unless" as "if" is distractor E-unless) | whenever used; never |
| O1 | "only if" with "and" | "<B> is <due> only if <c1> and <c2>. When all of these conditions hold, <B> is <due>." | B iff (c1 and c2) | none | whenever used; never. Conjunctions only (A08) |
| O3 | "only if" with "or" | "<B> is <due> only if <c1> or <c2> (either or both). When at least one of these holds, <B> is <due>." | B iff (c1 or c2) | none | whenever used; never. Mixed and/or never appears under "only if"; such a structure is not generated, since one <B> has one governing rule (A08, R1-04) |
| O2 | plain "if" | "<B> is <due> if <C>." | C is sufficient; each <B> has exactly one governing rule (2.1, R1-04), so with W0's default B is due exactly when C holds (A07) | none | whenever used; never |
| CMP1 | Inclusive comparators (lexicon meaning) | "at least <X>", "no less than <X>", "no fewer than <X>", "<X> or more", "reaches <X>"; card rules only: "a minimum of <X>" | >= X | CMP2 (T) | part of the rule or question; never. "a minimum of <X>" never in a question (Q1; R3-22) |
| CMP2 | Exclusive comparators (lexicon meaning) | "more than <X>", "over <X>", "above <X>", "exceeds <X>" ; "less than <X>", "under <X>", "below <X>", "fewer than <X>", "falls short of <X>", "fails to reach <X>" | > X ; < X | CMP1 (for >) / CMP3 (for <) (T) | as CMP1 |
| CMP3 | Upper inclusive (lexicon meaning) | "at most <X>", "no more than <X>", "does not exceed <X>", "<X> or less"; card rules only: "up to <X>", "a maximum of <X>" | <= X ("up to <X>" in a card rule is always inclusive) | CMP2 (T) | as CMP1. "up to <X>" and "a maximum of <X>" never in a question (Q1; R3-22) |
| CMP4 | Ranges | "between <X> and <Y>, both included" / "from <X> up to but not including <Y>" | X <= v <= Y / X <= v < Y. A bare "between" or "until" never appears | swap the two forms (T) | whenever a range is used; never. Card rules only: a question never carries a CMP4, D2, D3, OR1 or OR2 phrase (Q1; R3-01) |
| OR1 | Inclusive "or" | "<c1> or <c2> (either or both)" | c1 or c2 | OR2 (T) | whenever used; never. The tag is always present, whatever the row's state (A47) |
| OR2 | Exclusive "or" | "either <c1> or <c2>, but not both" | c1 xor c2 | OR1 (T) | whenever used; never |
| D1 | Calendar | "All dates are calendar dates in one time zone; the time of day does not matter." | Gregorian proleptic dates, no times | none | every card with dates; never |
| D2 | Before / by / after | "by <D>" / "on or before <D>" / "no later than <D>" ; "before <D>" ; "after <D>" ; "on or after <D>" | <= D ; < D ; > D ; >= D | inclusive vs exclusive swap (T) | part of the rule; never. Never in a question (Q1; R3-01) |
| D3 | Date range | "from <D1> to <D2>, both days included" / "from <D1> up to but not including <D2>" | [D1, D2] / [D1, D2) | swap (T) | whenever used; never. Never in a question (Q1; R3-01) |
| D4 | Offset deadline (XF13; R3-09, R3-10) | Base form D4a: "<Act> must happen no later than <N> calendar days after <event>. The day of <event> is not counted, so the last allowed day is <N> calendar days after it." Flip form D4b: "<Act> must happen on or before the <N>th calendar day, counting the day of <event> as day 1." (D4a's "no later than <N> calendar days after" keeps XF13's meaning: any day up to event + N, no lower bound, as D2. D4b never uses the XF13 phrase, so no F2 card gives that phrase another meaning. F2 never uses "within ... after". "calendar" is always written) | D4a: last = event + N; D4b: last = event + N - 1 | D4a <-> D4b, the whole clause (T); no filter alternative | every card whose deadline is a calendar-day offset; never. The shown form is always whole (both D4a sentences together) |
| D15 | On time (new) | "An <act> on or before the last allowed day is on time, also when it is on or before the day of <event>; an <act> after the last allowed day is late." | on time iff act date <= last allowed day | none | every on-time / late row and every "missed its deadline" row; never (A09). Round 1 places no act on or before the event day. **Every last allowed day is on or after the day of <event>**, after every extension and roll (A asserts; R4-11), so the clause's second part never covers a day after the last allowed day |
| D16 | Window edges (new, R2-06; R3-09) | "<k> calendar days after the last allowed day is the date <k> calendar days later; the last allowed day itself is not counted." ("calendar" is always written, also when the deadline counts business days) | edge = L + k (k whole, >= 1); S4 window tables are B1 tables read on dates (S4) | none (an off-by-one edge is distractor E-day) | every S4 window table; never |
| D17 | Settlement date (S5 only; new, R4-09) | "The settlement date is <N> calendar days after <period end>; the day of <period end> is not counted. If the settlement date falls on a day that is not a business day, the roll rule applies to it." | settlement = period end + N (N whole, >= 1), then D7's one roll (forward, back or none, as the card's D7 form says) | none (counting the day of <period end> as day 1 is distractor E-day; a wrong roll is E-roll) | every S5 card with a settlement date; never. Always with D6a and D7 (D7 never omitted there); never with D4, D6b or D8 (R3-08) |
| D5 | Calendar day count | "Count <D2> but not <D1>." / "Count both <D1> and <D2>." | D2 - D1 / D2 - D1 + 1 | swap (T) | every calendar count-target row, and every printed count whose endpoint dates are shown; never |
| D14 | Business-day count (new) | "Count the business days after <D1> up to and including <D2>." | business days in (D1, D2] | T: "Count the business days from <D1> to <D2>, both included." ([D1, D2]) | every business-day count row; never (A10) |
| D6a | Business days: definition (R3-08, R3-23) | One form on every card: "A business day is <Monday to Friday> that is not a holiday. The holidays are exactly the dates on the <record>'s holiday line; when that line says \"none\", there are no holidays." | Weekend set as stated; holiday set = the dates on the document's one holiday line, empty when it says "none" (2.1; the line is never left out, on any row of the card, whatever the row's holiday count). **No listed holiday falls on a weekend day** (generator constraint; A and B assert, A12) | none | whenever business days are used (D6b, D12 in business days, D14), and whenever D7 appears (A13); never. It defines business days only and sets no deadline |
| D6b | Business-day offset deadline (R3-08) | "<Act> must happen no later than <N> business days after <event>. Counting starts on the day after <event>; the <N>th business day is the last allowed day." | day 1 = first business day after the event (also when the event day is not a business day); last = the N-th business day | none (calendar days is distractor E-bday) | every card whose deadline adds business days; never; always with D6a. **Never shown on a card whose deadline is a calendar-day (D4) or month (D8) offset, or on an S5 settlement card** (A asserts; the parser rejects a second deadline rule, 3.3) |
| D7 | Roll rule | "If <the last allowed day; on S5 cards, the settlement date (D17; R4-09)> falls on a day that is not a business day, it moves to the next business day." / "... moves to the previous business day." / "... it does not move." | forward / back / none | any other of the three (T; filter: both others) | whenever the deadline can land on a non-business day; filter. Always with D6a (A13); with D6b only when the deadline adds business days (R3-08); never omitted on an S5 card with a settlement date (D17) |
| D8 | Month addition | "<M> months after <D> is the same day number <M> months later, also when <D> is the last day of its month; if that month has no such day, use the last day of that month. Then apply the roll rule, if there is one." | civil month addition with end-of-month clamp, then one roll (A17). Month offsets go forward only: "<M> months before <D>" is not generated in round 1 (R4-11). The day number is kept also when <D> is the last day of its month (28 February + 1 month = 28 March; 30 April + 1 month = 30 May) | none for the filter (D8 is never omitted). Listed for hooks only: overflow into the next month (the extra days carry over); end-of-month kept (a last day of a month maps to the last day of the target month). Both are distractor E-eom (= E-alt:D8) | every card with a month offset, whatever the anchor's day number; never (SC17, R3-21) |
| D9 | Weekdays and holidays | The text states the weekday of every anchor date and of every listed holiday, and (through the calendar strip, 1.1) of every candidate date whenever D6a is shown | Weekday comes from the text; B checks it against the calendar (a mismatch is a render bug). The weekday of a computed date is never left for the reader to derive (R1-14) | none | renderer; whenever weekends, business days or holidays matter |
| D10 | Effective dates (spans and governing dates) | "The new <rate> applies to <days or dates> on or after <D>; earlier <days or dates> use the old <rate>." | split the span at D, or pick the rate for a governing date; printed sub-span counts follow this form (1.1) | T and filter: "... applies to <days or dates> after <D>; <days or dates> up to and including <D> use the old <rate>." | whenever a rate changes inside a span; filter. **Always shown, as "never", on every card that shows D13** (R1-07) |
| D13 | Governing date for one-off charges (new) | "A one-off <charge> uses the <rate> in force on <the day of <event> or the <invoice> date>." | the named date picks the rate; the boundary case (governing date = change date) is settled by D10's shown form | another named date (T) | whenever two rates exist and a one-off charge or a band lookup uses one; never (A18). Always with D10's boundary sentence for that change (R1-07); on about 30% of D13 rows the governing date equals the change date, so D10's form is decisive there. S3's second table names its governing date with D13 |
| D11 | Age / elapsed years | "Age is the number of full years completed on <date>; a birthday counts as completed on the day itself." | completed years | none | whenever used; never (29 Feb births are never generated) |
| D12 | Extension (new) | "If <C>, the last allowed day moves <K> <calendar days or business days> later. Count the <K> days from the last allowed day found before any roll; then apply the roll rule once." | extension added to the pre-roll deadline; one roll at the end (A17). **At most one D12 rule per card**, with one <K>; several conditions for it are joined inside that one rule (R1-04). A asserts; the parser rejects a second extension rule (R3-24) | T: "Count the <K> days from the last allowed day after the roll; then apply the roll rule again." | whenever an extension exists; never. "Calendar" or "business" is always stated |
| R1 | Rounding mode | "Round <quantity> to the nearest <unit>; an exact half rounds up." / "...; an exact half rounds to the even <unit>." / "Always round <quantity> down to a whole number of <unit>s; a value that is already a whole number of <unit>s does not change." / "Always round <quantity> up to a whole number of <unit>s; a value that is already a whole number of <unit>s does not change." (R4-01) | half-up (toward the larger value) / half-even / floor / ceiling (Decimal FLOOR / CEILING: a value already on the unit grid is unchanged). Rounding units are 10^k of the display unit only (k >= 0; for example 0.01, 1, 100); rounding never applies to a value that can be negative (A asserts; A25). **Half-even is shown (on a base or flip variant) only when the rounding unit is at most one whole unit of the quantity** (0.01, 0.1 or 1 of a currency unit or other unit; A asserts; R4-02), so an exact half always has one even neighbour; as a filter or hook alternative on a coarser unit it means the multiple of the unit whose number of units is even | any other mode (T; filter: all three others) | whenever rounding can change the label or a displayed value (card level, 2.1); filter. When R1 is not shown, R2-R4 are not shown either and every row is exact (R7; R1-18) |
| R2 | Rounding stage | "Round only the final <amount>." / "Round each line as the rounding rule says, then add the lines." | stage of rounding. R1 gives the mode and unit and R2 only the stage: per-line rounding always uses R1's mode and unit (half-up, half-even, floor or ceiling), never "nearest" by default (R2-01). When R2 is shown, R1's <quantity> names the kind of amount rounded and R2 says which ones | swap (T; filter) | whenever the stage changes the result (card level); filter. Only together with R1 (R1-18) |
| R3 | Compare after rounding (R2-02) | "Every comparison made after <amount> is rounded (with <T>, a band or outcome edge, a condition, a cap or a minimum) uses the rounded <amount>." | every comparison (YN-T threshold, band or named-outcome edge, exception or gate condition on a computed amount, cap or floor min / max) reads the value at its own position in the card's step order (X1), with every earlier rounding step applied and no later one | T: "Every comparison uses the <amount> computed with no rounding step at all; rounding changes only the reported <amount>." Operational meaning, for A, B and every alt-label and E-alt:R3 hook (R3-15): (1) run the card's steps in their order with every rounding step skipped; every branch decision (a gate or condition on a computed amount, which side of a cap or minimum binds, a band or outcome lookup, the question's comparison) is taken from this unrounded run; (2) the reported value and every arithmetic node then follow the card's steps with each rounding step at its X1 position, taking the branches fixed in (1). **R3 flip variants are planned only on YN-T cards whose questions are all CMP1-CMP3 threshold questions (never an OP money predicate, R3-14) and on which the question's comparison is the only comparison after a rounding step** (A asserts), so on every card that shows the T form both steps give one reading | every card that shows R1 and has any comparison after a rounding step (card level); never (it is dropped only together with R1, R1-18) |
| R4 | No hidden rounding | "Do not round any step except where a rule says so." | intermediates are exact | filter (both tested, R3-21): every intermediate rounded half-up to display precision; every intermediate rounded in R1's mode to R1's unit | every card that shows R1; filter. Only together with R1 (R1-18) |
| R5 | Partial units (R4-03, R4-04) | "For each <line>, each started <unit> is charged as a full <unit>." / "For each <line>, only complete <units> are charged." / "For each <line>, the <quantity> is charged exactly as stated; no part of a <unit> is rounded." (<line> names the record's line kind: line, session, visit, item) | ceiling / floor / exact, applied to **each line's own quantity**, before that quantity is priced, summed, banded, compared or split by B4. A asserts: each line holds one quantity of the kind; every band edge and B4 threshold X that splits such a quantity is a whole number of <unit>s; the quantity before and after the rule falls in the same band and on the same side of every threshold or condition of a card rule that reads it (the question's own comparison reads its Q1 target node). So every order of the rule against a split, lookup or rule comparison gives gold (R4-04) | any other (T; filter: both others) | whenever a quantity **not governed by U3** is not whole (card level); filter. Never shown for, or applied to, a U3 quantity (R1-09). The scope phrase is always written |
| R6 | Percent vs points (R4-05) | "<p>% of <base>" ; "the rate rises by <k> percentage points" ; "the rate rises by <k>%". On every card on which a rate that is itself a percent rises (in either form), the card also carries: "A rise of <k>% in a percentage rate multiplies it by (100 + <k>)/100; a rise of <k> percentage points adds <k> to it." | base x p/100 ; rate + k ; rate x (1 + k/100) | none (mix-up is E-pct) | part of the rule; never. The definition sentence: every card on which a percent rate rises; never |
| R8 | Single discount (new) | "A <p>% discount on <base> means paying (100 - <p>)% of <base>." | base x (1 - p/100); the base is named per X6 | none (E-pct, E-base are distractors) | whenever a discount is used; never (A26) |
| R7 | Display | Stated amounts and options use the pack's precision (2 decimals or whole units); options are distinct at that precision | **Nothing is ever rounded for display**: only the card's own rounding steps (R1, at R2's stage and X1's position) round a value. **On every row, R1 shown or not (R3-13)**, A asserts that each of these values, computed under the card's own steps, is exactly representable at display precision: the final value; the asked target node (Q1, including a "before <step>" value); every option value; every hook value offered as a distractor (an off-grid hook value is not eligible, 3.4); and the value that the question's comparison, OP predicate or band / outcome lookup reads (on an R3 T-form variant, the value that comparison reads is the one computed with no rounding step, as the card says, R3-15). Gold = that exact final value. When R1 is **not shown on the card** (not relevant, or dropped from a short card), A also asserts that every value any rule's comparison reads is on the grid (A51, R1-18). Otherwise the structure is resampled | none | renderer; always |
| T1 | Ties in argmin / argmax | "If two <items> give the same <amount>, choose the one with the <lower ID number or earlier date>." | stable tie-break; **never list position** (A14). Keys are ID numbers or dates only; F2 has no priority keys. **ID numbers (XF05; R3-18, SC18)**: every item of a card has an ID of the same fixed width (same prefix, if any, and the same number of digits, with leading zeros), compared as numbers, so numeric and text order agree. Any two tied items differ in the key (A asserts; the parser rejects IDs of mixed width) | the reverse direction (higher ID number, later date) or the other key (T) | every card with an argmin, argmax or best-option rule, whether or not a tie occurs; never (A47) |
| T2 | Equal to threshold | governed by CMP1-CMP4 | no separate tie rule | - | - |
| B1 | Band edges (one form per table; a card sentence, R2-12) | Upper-inclusive: "Each band covers the <amounts> over its lower edge up to and including its upper edge; the lowest band covers every <amount> up to and including its upper edge, and the highest band every <amount> over its lower edge." Lower-inclusive: "Each band covers the <amounts> from its lower edge up to but not including its upper edge; the lowest band covers every <amount> under its upper edge, and the highest band every <amount> of its lower edge or more." Both forms end: "A blank edge cell means the band has no edge on that side." | every value belongs to exactly one band. The B1 sentence is always in the card; a band table in the document gives edges as plain numbers only, with the lowest band's lower-edge cell and the highest band's upper-edge cell blank (a card-defined blank, XF06; these two blanks are governed by B1 alone, never by M3). **Shared edges (R3-06):** each band's lower-edge cell holds the same number as the previous band's upper-edge cell (and in card-written tables and S4 windows each band starts at the previous band's end value), so a value on an edge has one candidate edge; gapped edges (1,000 then 1,001, or 1,000.01) are never rendered (A and the parser assert). **Marginal tables over whole-unit counts use the upper-inclusive form only** (A asserts; R3-05); the lower-inclusive form appears on flat tables, named-outcome and window tables, and marginal tables over money or other non-count amounts. A table written inside the card (named outcomes) may use the same meanings per band ("up to and including <hi>", "over <lo> up to and including <hi>", "over <lo>" / "under <hi>", "from <lo> up to but not including <hi>", "<lo> or more"). S4 window tables read these on dates (S4; R2-06) | the other form, whole table at once (T); never flipped on a marginal table over counts (R3-05) | every band table; never. Each form on 50 +/- 5% of band tables and of on-edge rows (A27, A46); "band tables" here include S1 / S2 named-outcome tables and S4 window tables, and on-edge rows include S4 window rows whose act date is an edge date (R2-06). The builder draws forms on the other tables so that the split holds with marginal count tables fixed to upper-inclusive (R3-05) |
| B2 | Band mode | Marginal: "Each rate applies only to the part of the <amount> inside its band: the part above the band's lower edge, up to its upper edge (for the lowest band, from 0 up to its upper edge)." / Flat: "The rate of the band that the whole <amount> falls in applies to the whole <amount>." | marginal: part in a band = min(amount, hi) - lo when amount > lo, else 0 (lo = 0 for the lowest band, no hi for the highest), a measure, never a count of numbered units (R3-05) / flat. **Flat-fee band rates appear only on flat-mode tables**; a marginal table's rates are percents or per-unit rates only (A asserts; R3-20). A B2 flip variant, B2's alt-label and the E-mode hook exist only on tables whose rates are percents or per-unit rates (on a flat-fee table B2 is never decisive) | swap (T) | every band table; never |
| B3 | Banding variable | "Bands are set by the <amount> <before or after> <adjustment>." | which value selects the band. <adjustment> is never a rounding step: whether a band lookup reads a rounded value is governed by R3 alone (R2-02) | swap (T) | whenever an adjustment comes before the lookup; never |
| B4 | Part above a threshold (new) | Whole units: "In each <scope>, units up to and including the <X>th are paid at the base rate; each unit after the <X>th is paid at <m> times the base rate." Other quantities: "In each <scope>, the part of <quantity> over <X> is paid at <m> times the base rate." <scope> is named as in X4: <line, claim, calendar week (Monday to Sunday), calendar month or calendar year (1 January to 31 December)> | units after the X-th (or the part over X) in each scope get the multiplier. **When the scope is wider than a line, each scope holds at most one line of that quantity** (A asserts; R3-19), so no line split arises. When the quantity is governed by R5 or U3, X lies on that rule's grid (a whole number of <unit>s, or a multiple of k; R4-04) | whole units, T: "... from the <X>th unit on ..." | whenever a multiplier applies above a threshold; never. Never phrased as a comparator (A19). The scope phrase is always written |
| X10 | Category band exception (new; flat mode only) | "<Category> pays the rate of the band with the next lower edges than the band its <amount> falls in; in the lowest band nothing changes. Band edges do not change." | flat mode: the whole amount at the next-lower band's rate | none (ignoring it is E-exc) | whenever used; never. Never used in marginal mode (A15) |
| U1 | Units | Every quantity carries a unit. Built-in facts are only: the Gregorian calendar (7-day week, month lengths, leap years, 12 months a year), 24 hours a day, 60 minutes an hour. Every other conversion is stated ("1 <unit A> = <k> <unit B>") | no outside conversion; A asserts that every conversion used is built-in or stated (A28) | none (missing conversion is E-unit) | whenever two units appear; never |
| U2 | Currency | One currency per row; any exchange is stated ("1 <A> = <r> <B>", exact decimal) | no outside rate | none | whenever two currencies appear (rare); never |
| U3 | Per-k pricing (R4-04) | "For each <line>, <price> per <k> <units>; a part of <k> is charged <pro rata or as a full k>." | applied to each line's own quantity first, as R5 (R4-04); A asserts that every band edge and B4 threshold that splits a U3 quantity is a multiple of k, and that the quantity before and after a full-k rounding falls in the same band and on the same side of every threshold or condition of a card rule that reads it. Pro rata: price x quantity / k, with the quantity exactly as stated (it may be non-whole); as a full k: price x (quantity / k rounded up to a whole number). U3 is the **only** partial-unit rule for its quantity: R5 never applies to it (A asserts; R1-09) | T: swap of the two card forms. Filter (R3-21): both other readings of pro rata, as a full k, and complete blocks only (price x (quantity / k rounded down to a whole number); filter and hook only, never a card form) | whenever used; filter |
| U4 | Number format | "," thousands separator optional, "." decimal point, never "," as decimal; dates as "<weekday>, <day> <Month> <year>", "<Month> <day>, <year>" or ISO; never numeric D/M forms | parser grammar | none | renderer |
| U5 | Deduction sign (new) | "Deduction lines are listed as positive amounts and are subtracted." | deductions subtracted; no minus signs or parentheses on any amount | none | every statement or table with deduction lines; never (A58) |
| X1 | Order of steps | "Apply the steps in this order: <step 1>, then <step 2>, then <cap>, then rounding." | stated order. Rounding sits where R1 and R2 put it (R1's named <quantity> as soon as it is computed; each line, or the final amount); when X1 is shown, its stated position for rounding agrees with R2's stage (A asserts). **Askable nodes (R3-16):** the final value, every "before <step>" or other named target node that any row of the card can ask (Q1; "the <amount> before <step>" = the value that enters <step> in the card's step order) and every printed intermediate. When X1 is not shown, every order the card's rules allow gives the same value at every askable node and the same outcome for every comparison (program check), so the order is immaterial (R2-02). **Permuted steps (R4-08):** the program check permutes exactly the card's adjustment steps (caps and minimums, X4; discounts, R8 and X5; percentage fees and charges, X6 and X7; added fixed amounts and subtracted deductions, U5; exception switches, X2 and X3; waivers, X9) in every order that data dependencies and stated orders allow (X6's named base, B3, X4's minimum after the cap, M4's pricing before rounding, caps and minimums). Steps with a fixed place are never permuted: partial-unit rules (R5, U3: first, on each line's quantity), M4 line pricing, rounding (R1 at R2's stage) and X8 (last, on the final amount). When X1 is shown, its order names every adjustment step of the card | any other order that changes an askable node's value or a comparison's outcome (T; filter) | whenever reordering can change the value of any askable node or the outcome of any comparison (program check, card level); filter |
| X2 | Specific vs general | "When <exception E> applies, it replaces the <general rate>." / "...is added to the <general charge>." | replace = sets the current <rate>; add = adds to the current <charge>. With one applicable exception, "current" is the general one | swap (T) | every exception; never |
| X3 | Several exceptions | "If more than one exception applies, compute the final <amount> with each one alone and use the one that gives the <lower or higher> final <amount>; if two give the same final <amount>, use the one with the lower rule number." / "If more than one exception applies, apply all of them in rule-number order; each one acts on the <rate or charge> left by the ones before it, so a later replacing rule replaces the rate an earlier one set." | first form: the compared amount is the final target with only that exception applied and every other step unchanged (A16). Second form: a left-to-right fold in rule-number order on the current value: each replace sets the current rate (so the last applicable replace wins), each add adds to the current charge (R1-03). **On a card with the second form every exception that can apply is of one kind** (all replace, with "<rate or charge>" written "rate"; or all add, written "charge", without the "so a later replacing rule ..." clause); a card whose exceptions mix replace and add uses the first form (A asserts; R2-05). Rule numbers move with their rules under MR4 (A35) | swap (T) | whenever >= 2 exceptions can apply to a row of the card; never |
| X4 | Cap and floor scope | "The cap of <X> is per <claim, line, calendar week (Monday to Sunday), calendar month, or calendar year (1 January to 31 December)>." ; "The minimum charge of <Y> is per <...>." ; if both: "The minimum is applied after the cap." | scope with named boundaries, and order; rolling windows are never used (A20). **Cap and minimum together (R4-07):** a card shows both only when, on every variant, the minimum's scope equals the cap's or is a union of whole cap scopes (cap per line with minimum per claim or per total; cap per calendar month with minimum per calendar year); never a minimum narrower than the cap, never weeks against months or years (A asserts), so the minimum always reads scope totals that the cap fully defines. **No allocation inside a wider scope (R3-19):** when a cap's or minimum's scope can hold more than one line (per total, per claim with several lines, per calendar week, month or year), no question asks for, and no option or hook is, one line's or one item's share of the capped or floored amount; questions ask for a scope total or a value computed from scope totals (A asserts). A card with an X4 flip variant asks only for totals over every line of the wider scope, which are defined under both forms | per-line vs per-total swap (T) | every cap or floor; never |
| X5 | Successive vs added discounts | "Discounts are applied one after the other, each to the amount left after the previous one." / "Discount percentages are added together and applied once." | stated | swap (T) | whenever >= 2 discounts apply; never |
| X6 | Base of a percentage | "The <fee> is <p>% of the <amount> after <step>." / for a fee included in a listed price: "The <fee> is <p>% of the price before <fee>." | the base is always named, including "the price before <fee>" (R1-02) | before / after swap (T) | every percent-of and every discount; never |
| X7 | Gross vs net | Include form: "Listed prices include <fee>. The price before <fee> is the listed price x 100 / (100 + <p>), and the <fee> is the listed price minus the price before <fee>." / Before form: "Listed prices are before <fee>; the <fee> is <p>% of the listed price and is added to it." | include: net = listed x 100 / (100 + p) (1 scale node), fee = listed - net (1 subtract node); before: fee = listed x p / 100, total = listed + fee. Whenever a backed-out value is not exact at display precision, R1 (and R2's stage) is shown and applies (R7); A's exactness guard (3.1) covers the inexact division (R1-02) | swap (T). Taking p% of the listed price as the included fee is distractor E-gross | whenever a fee sits on a listed price; never |
| X8 | Floor at zero (R4-08) | "The final <amount> owed cannot go below 0." | max(0, v) on the final amount only, after every other step and before a final rounding step if there is one (the order against that rounding is immaterial; rounding never sees a negative value, A25). A asserts that every other amount node (money, quantity, count; date offsets exempt) is >= 0 on every row, so flooring an earlier node would change nothing | filter: a negative final amount allowed | whenever the final amount could go below 0 (card level); filter |
| X9 | Waiver | "A waived <fee> counts as 0." | stated | none | whenever a waiver exists; never |
| M1 | Missing data, closed | via W1 and W3 | as W1, W3 | none | as W1 |
| M2 | Missing data, open | via W2 | NEI rule (3.5) | none | as W2 |
| M3 | Blank amount cells (closed world only; R3-07) | "A blank cell in the <amount> column means nothing was charged on that line." (<amount> names the line-amount column of the table or statement) | 0. **M3 covers blank cells of the named amount column only**: B1 edge blanks are governed by B1 alone. **Open-world cards have no blank amount cell** (their one unknown is "not recorded", W2; R3-11), so M3 has one form and never means unknown (A asserts; A21). **A blank amount appears only on a line that shows no quantity and no rate** (A asserts; R1-01). **Such a line's quantity and rate cells hold the XF06 zero marker "none"** in every container that has those cells (the S5 statement; CSV, markdown, HTML and fixed-width tables), never a blank and never "0"; the parser reads "none" in both cells as no quantity and no rate, never as 0 x rate, and rejects a blank or "0" there (A asserts; SC19). A line with a quantity and a rate never has a blank amount: its amount is printed or carries the M4 marker | none (F2 has no world twins, R2-10) | every closed-world table or statement with a blank cell in its amount column; never. Not shown for B1 edge blanks |
| M4 | Computed cells (new, R1-01; R2-04) | "An <amount> shown as \"<computed-cell marker>\" is the line's amount worked out from its <quantity> and <rate> by the card's pricing rule for that line (<the B4, partial-unit or per-k rule>, or else <quantity> x <rate>), before any rounding, cap or minimum; rounding, caps and minimums then apply to it as to a printed <amount>." | marked amount = the line's pricing: quantity x rate (1 multiply node), or the B4, R5 or U3 computation on the line's quantity and rate (their own nodes, 1.1); all unstated. A B4 split on a marked line is the split of the line's B4 scope, which holds only that line of the quantity (B4; R3-19). Per-line R2 rounding and per-line X4 caps and minimums then apply in the card's step order (X1), as to a printed line amount. The clause names only the pricing rules the card has. **No exception changes a marked line's quantity or rate** (the rate column is the rate charged; A asserts). The marker is never blank and never read as 0 | none (reading the marker as 0 is distractor E-blank) | every table or statement with a marked cell; never. The marker's surface text is written after the freeze, like every wording |
| P1 | Proration basis | "Prorate by days: <amount> x days used / days in the <period>. <Period> has <n> days." / "Prorate by days: <amount> x days used / 30; every month counts as 30 days." | actual (n stated) / 30-day. Days used are always printed as a number (1.1) | swap (T) | every proration; never. Every row on a card with the 30-day form, and every base row with a P1 clause-flip twin, prorates a span that lies inside one calendar month and contains no month-end day (so never day 31): printed days used <= 29 and the result is below the full amount (A asserts; R1-08) |
| Q1 | Question scope | Every question names its target node: the final value, a named value before a named step (the value that enters that step in the card's step order; X1's program check covers it, R3-16), the last allowed day, or a count; the target is on the display grid (R7; R3-13) and, under a multi-line cap, minimum or B4 scope, is a scope total or a value computed from scope totals (X4; R3-19). A question carries at most one comparator, from CMP1-CMP3 except "up to <X>", "a maximum of <X>" and "a minimum of <X>" (card rules only; R3-22), written whole and contiguous in its lexicon form (so "does not exceed" appears only inside a TF complement, never split as "Does ... not exceed"), or one OP predicate. It never carries a CMP4, D2, D3, OR1 or OR2 phrase (those sit in card rules only), never "not more than", "not less than", "not before" or "not after", and never "or not", "whether or not" or "yes or no". The answer instruction ("answer yes or no" and the like) is a separate sentence outside the question and is never counted (R3-01, R3-02) | target node | none | renderer; every question. A asserts; the parser rejects violations (3.3) |
| N1 | Negated questions (yes/no only; XF10) | One or two N1 cues (3.8) inside the complement P of a **truth frame** (TF): a question frame that only asks whether a declarative proposition P is true, with no negation, judgement or acceptance word of its own (meaning only; XF10 cites "Is it true that <P>?"; surface forms come from the post-freeze pool, map to one lexicon entry and pass 7.2 #8 and XF10's lint) | each N1 cue inverts the answer once; double negation = affirmative. N1 cues, one closed list: not, n't, no, none, nothing, never, the operator "it is not the case that" at the start of P, and "fail to" only in "fail to meet <its> deadline" (= missed its deadline). In P a cue negates P's main predicate (the comparison or the OP predicate) or is that operator; never inside an entity description (R2-09). CMP1-CMP3 phrases (the only comparators a question carries, Q1) keep their CMP meaning and are not cues, also when they contain a negation word ("negcmp"); OP predicates are propositions. Never: a negated main-question auxiliary ("Isn't", "Doesn't", "Wasn't", "Didn't" and the like), a negated frame ("Is it not true that"), a cue outside P, "or not", "whether or not", "yes or no"; never the other F5 implicit cues (hardly, unless, other than, lack, deny, refuse, rule out) or any other negcount L_neg entry (without, except, few, barely, ...) in a question. Choice and case-list questions carry no N1 cue (R3-01, R3-02, R3-03) | none | negation rows (XF02: k_syn >= 1 on >= 10% of yes/no rows; k_syn >= 2 with the affirmative twin on >= 2%; k_syn from the shared negcount). Every row with an N1 cue uses a TF; affirmative yes/no rows use a TF on 50 +/- 5% of rows, drawn independently of the label (tag "tf:1") |
| OP | Outcome predicates (new, R1-10; R3-04) | A closed list of outcome meanings that a question may ask about: on time; late (= after the last allowed day, D15); met its deadline (= on time); missed its deadline (= late); due; owed; charged; falls in <band or named outcome>. Card clause for the money predicates: "An <item> is <charged> (or <owed>) when its <amount> worked out under these rules, after every rounding, cap, minimum, discount and waiver, is more than 0. An <item> is <due> when a listed rule makes it <due>." | each is the proposition itself (inverting count 0), never a cue that inverts a base proposition. charged / owed: the question's named amount (Q1), final under the card's rules (the reported amount, after every rounding step; on the display grid, R7), is > 0. **On every row that asks charged or owed, A asserts that the named amount computed with no rounding step is > 0 exactly when the reported amount is > 0**, else resample; and no card whose questions use an OP money predicate has an R3 flip variant (R3-14). So R3's two forms never give different labels on an OP row, and the T form never stands on a card with this clause. due: the item's one governing rule (UN1, O1-O3; W0) makes it due. **On every row whose question asks "due", A asserts that the item's amount is > 0 exactly when its rule makes it due** (no waiver to 0, floor at 0, cap of 0, 100% discount or zero-day proration of a due item), else the structure is resampled, so the rule reading and the amount reading of "due" never differ on a row. **Owed and payments (R4-06):** no row of a card whose questions use "owed" lists a payment line of the row's entity (A asserts), so "owed" read before or after payments is one amount. falls in: B1 membership of the named value. No outcome predicate is built from a C_DATA_SPEC F5 cue word; the only F5 implicit cue an F2 question uses is "fail to", in N1's one frame "fail to meet <its> deadline" (and inside CMP2's "fails to reach"). A, B and the parser share this list | none | money clause: every card whose questions use due, owed or charged; never. The list: renderer; every yes/no and inverted question |
| A1 | Abstain options | "<NEI option>" on every open-world row; "None of the listed <items>" on some closed-world rows; never both on one row (A22); an abstain option is shown only at k >= 3 (XF01) | NEI per 3.5. "None" gold: value, date and count rows: no shown option equals the computed value (which is on the display grid, R7); case lists: no listed case meets the rule; band and named-outcome rows: "none" is never shown (gold is always shown) (A23). On a row with k shown options (abstain included), the abstain option is gold with probability 1/k (SC2); G10 checks it at 1/k +/- 2 pp per k bucket and per abstain option, NEI and "None of the listed" separately (XF01; SC12) | none | abstain rows (6) |

**Parser lexicon rule (A54, R1-10, R3-01, R3-09, R3-10, R4-09).** Phrase matching is longest-match and context-specific:
"up to but not including <Y>" (CMP4, D3) beats "up to <X>" (CMP3); "no later than <N> calendar days after <event>"
(D4a) and "no later than <N> business days after <event>" (D6b) are separate entries from D2's "no later than <D>" and
"after <D>"; "on or before the <N>th calendar day, counting the day of <event> as day 1" (D4b) beats D2's "on or
before <D>"; "<k> calendar days after the last allowed day" (D16: an S4 window edge = the last allowed day + k, R2-06)
is its own entry; "<N> calendar days after <period end>" (D17, the S5 settlement date; R4-09) is its own entry;
"fails to reach <X>" (CMP2) beats the N1 cue "fail to"; "fail to meet <its> deadline" is the one N1
"fail to" entry; the TF entry is its own entry; outcome predicates (OP) are their own entries, kept apart from N1 cue
entries by longest match. Question-side entries are CMP1-CMP3 (without "up to <X>", "a maximum of <X>" and "a minimum
of <X>", which are card-rule entries only; R3-22), OP, TF and N1 only (Q1). The G0 reviewer checks these entries when
the lexicon is built (after the freeze).

---

## 3. Shared machinery (all samplers)

### 3.1 Solver A (generator logic)
- Runs on the generator's in-memory structure (before rendering). Python `decimal.Decimal` (C_DATA_SPEC F2; local
  context, precision 50), `datetime.date` / `timedelta`, business days by **day-by-day iteration** over the stated
  weekend and holiday sets, bands evaluated **band by band**, rounding by `quantize` with HALF_UP, HALF_EVEN, FLOOR,
  CEILING to 10^k units.
- **Exactness guard (A37).** A traps the Decimal `Inexact` signal per operation. When any value is inexact, every later
  decision that depends on it (comparison with T, min / max, rounding boundary, band edge, option equality) must have a
  margin > 10^-20; otherwise the structure is rejected. Solver B works in exact rationals, so G2 catches any residue.
- Outputs per row: target value; yes/no label after comparator and polarity; gold option; the value under **every
  named error** (3.4); the alt-label under **every listed alternative** of each relevant dimension, with printed
  numbers held fixed (2.1, R1-16); the joint invariance result for omitted dimensions; NEI status and witness pair
  (3.5); depth, total operations and selection-step counts (1.1; per case on case lists); structure hash (3.8); the
  `has:`, `bind:` and `dec:` tags (3.8).
- **Assertions** (any failure rejects the structure): no listed holiday on a weekend day (A12); every rounded value
  >= 0 and every rounding unit 10^k of the display unit (A25); R7 representability on every row (final value, target
  node, options, hooks, the value the question reads; R3-13) and, when R1 is not shown, of every compared value (A51,
  R1-18);
  W1 / W3 default coverage on closed-world cards (A06); open-world coverage: every case field a rule reads is printed
  or "not recorded", exactly one is "not recorded", and it is read by at least one rule (R1-05, R1-27); no implied bound
  on the unknown field (R1-06); M3 only on closed-world cards, no blank amount cell on an open-world card (A21,
  R3-07); no blank amount on a line with a quantity or a rate (R1-01);
  exactly one governing rule per <B> (R1-04); no R5 on a U3 quantity (R1-09); 30-day proration spans inside one month
  with no month-end day (R1-08); a 2-operation business-day addition only on deep or sweep items (R1-13); at least 1
  unstated operation per row (R1-12); no clause refers to list or display position (A14, A35); conversions built-in or
  stated (A28); at most one abstain option per row (A22); open-world cards carry no yes/no and no case-list rows (A24,
  R1-19); each base row in at most one relation unit (A48); every distractor comes from exactly one named error, and a
  clause-flip twin's options are valid under both vectors (3.4, SC3, R1-21); no option text carries a level number
  (C14). Added in v4: every printed intermediate exact at display precision, and on group (c) rows every number that
  enters an arithmetic node printed (1.1; R2-03, R2-13); every case of a case-list row in one row group (R2-21); no
  exception changes a marked M4 line's quantity or rate (R2-04); X3 second-form cards have exceptions of one
  kind (R2-05); X1's rounding position agrees with R2 (R2-02); the unknown field is an amount, count, date, category or
  yes/no fact, and an unknown category has an explicit value list with at least one value no rule names (R2-07,
  R2-08); no SEM phrase in the document (2.1; R2-12); negation cues only at proposition scope (3.8; R2-09); a
  premise_removed twin's options are all admissible E-assume values (3.4; R2-11). Added in v5: questions carry
  CMP1-CMP3 or OP only, never a CMP4, D2, D3, OR1 or OR2 phrase, "not more than / less than / before / after", "or
  not", "whether or not" or "yes or no" (Q1; R3-01, R3-02); N1 cues only inside a TF complement, from N1's closed
  list, on yes/no rows only, and "fail to" only in "fail to meet <its> deadline" (N1; R3-02, R3-03); on "due" rows
  the amount is > 0 exactly when the rule makes the item due (OP; R3-04); marginal tables over counts are
  upper-inclusive (B1; R3-05); adjacent bands share edges (B1; R3-06); D6b never on a calendar-day, month or S5
  settlement card (R3-08); absent and unknown values rendered as 2.1 says ("not recorded" only, never null or
  "unknown"; R3-11); every inert line or GSM-NoOp fact outside every rule's named inputs by entity, period, line type
  or row ID (3.6; R3-12). Added in v6: on charged / owed rows the amount computed with no rounding step is > 0 exactly
  when the reported amount is > 0, and no card with an OP money predicate has an R3 flip variant (R3-14); R3 flip
  variants only on YN-T threshold cards whose question's comparison is the only comparison after a rounding step
  (R3-15); X1 omitted only when every allowed order gives the same value at every askable node (R3-16); the unknown
  field is never the occurrence or count of a charge, payment or event of a W2-listed type (R3-17); T1 keys are
  fixed-width ID numbers or dates, distinct between tied items (R3-18, SC18); under a cap, minimum or B4 scope wider
  than a line, no question, option or hook is one line's share, and a B4 scope wider than a line holds at most one
  line of its quantity (R3-19); flat-fee band rates only on flat-mode tables (R3-20); no "up to", "a maximum of" or "a
  minimum of" in a question (R3-22); exactly one holiday line, never left out, on every card that shows D6a (R3-23); at
  most one D12 rule per card (R3-24). Added in v7: R1 floor and ceiling leave on-grid values unchanged, and half-even is shown only
  with rounding units of at most one whole unit (R4-01, R4-02); each R5 / U3 line holds one quantity, every band edge and
  B4 threshold that splits such a quantity is on the rule's grid, and the quantity before and after the rule falls in the
  same band and on the same side of every threshold or condition of a card rule that reads it (R4-04); a percent rate that rises carries
  R6's definition sentence (R4-05); no payment line of the row's entity on a card whose questions use "owed" (R4-06);
  cap and minimum together only when the minimum's scope equals the cap's or is a union of whole cap scopes (R4-07); X8
  only on the final amount, and every other amount node >= 0 (R4-08); D17 with D6a and D7 on every S5 settlement card
  (R4-09); NEI status and label unchanged under the row's natural precedences (R4-10); every last allowed day on or after
  the event day after every extension and roll, and no backward month offset (R4-11); an M3 line's quantity and rate
  cells hold "none" (SC19); no left-out key means unknown (XC-01); choice rows have an empty `card` field and a card IR
  with no entry named like an option, no yes/no card line starts "- Yes: " or "- No: ", and every row passes fmt1
  `loader_check` (CP1).

### 3.2 Solver B (G2, different paradigm)
- Written by a different session **from this file only**; never reads A's code. Input = parser output from the
  rendered text (3.3), not A's structure.
- **Integers only.** Every number literal is parsed into an exact reduced fraction (numerator, denominator) of Python
  ints by B's own code; there is no grid, so any stated precision (rates, exchange rates, conversion factors) is held
  exactly (A38). Rounding by integer divmod with explicit half rules. Calendar: day ordinals by a from-scratch
  civil-to-days formula, weekday = ordinal mod 7 (cross-checked against the stated weekday). Business days in **closed
  form** (full weeks x workdays + remainder, minus stated holidays in range; valid because no listed holiday falls on a
  weekend day, which B asserts and fails on otherwise). Bands by **cumulative closed form** (charge at band start + one
  partial band).
- **Open-world rows: z3 (MIT)** over integers in display units and day ordinals, on the admissible domain of 3.5
  (type domain plus every parsed explicit bound sentence; R1-06). NEI iff at least 2 distinct option-level labels
  (including "no option") are satisfiable; determined iff exactly one is (A39).
- Forbidden imports in B: `decimal`, `fractions`, `datetime`, `calendar`, `dateutil`, `numpy`, `pandas`, `holidays`.
- **G2 pass:** 100% agreement with A on target value, yes/no label, canonical gold option, NEI status, every printed
  intermediate and every printed day count. Any mismatch: stop, fix, regenerate the whole generator.

### 3.3 Round-trip parse plan (G3)
- Parser written from this file (grammar of section 2 and the containers below), not from renderer code. It owns the
  **phrase lexicon** (surface phrase -> SEM id; longest match, 2.2), built after the sealed freeze. Every wording-pool
  phrase must parse through it. Lexicon entries are reviewed against section 2 by the G0 reviewer.
- **Where the parser reads the card (CP1).** Yes/no rows: the card is the `card` field, and `instructions` holds the
  wording, question and note. Choice rows: the `card` field must be empty; the card text is the block that
  `instructions` holds before the wording, question and note (after the IP4 task line, before the IP5 one), split by
  the instruction position of the row's format style (its order and joiner, read from fmt1 pool data, not renderer
  code); the card style's titles and headings are container boilerplate. Q1, N1 and the question-side lexicon apply
  to the question sentence only; SEM phrases in the card block are card text.
- Extracts: inputs (name, value, unit); rules (operations, caps, floors, bands with edges, form and mode, exceptions
  with connectives and rule numbers, order sentence); SEM switch vector; dates with stated weekdays; calendar strips
  (as weekday facts); holiday and weekend sets (the holiday set from the one holiday line, empty on "none"; R3-23);
  printed intermediates and day counts; blank cells (M3) and computed-cell
  markers (M4); question (target, comparator, threshold, outcome predicate, truth frame, negation cues and polarity); options
  (values, dates, CL case references with each case's values from `state`, names, abstain options); "not recorded" fields and their explicit bound sentences (R1-06).
- Rejects (a parse failure, so G3 fails): a second governing rule for the same <B> (R1-04); a blank amount on a line
  with a quantity or a rate (R1-01); a SEM phrase of 2.2 in the document (R2-12); a negation cue or C_DATA_SPEC F5 cue
  word inside an entity description rather than at proposition scope (R2-09). Added in v5: an N1 cue outside a TF
  complement, on a negated main-question auxiliary or in a negated frame, or in a choice or case-list question; an F5
  implicit cue other than "fail to" (or "fail to" outside "fail to meet <its> deadline" and CMP2's "fails to reach")
  or any other L_neg entry of negcount in a question; a CMP4, D2, D3, OR1 or OR2 phrase, "not more than", "not less
  than", "not before", "not after", "or not", "whether or not" or "yes or no" in a question, or a split "Does ... not
  exceed" (Q1, N1; R3-01 to R3-03); a band table whose adjacent edge cells differ (R3-06); a blank cell other than an
  M3 amount blank on a closed-world card or a B1 edge blank; null or "unknown" anywhere; "not recorded" on a
  closed-world card; a left-out field that a rule reads on an open-world card (R3-07, R3-11); D6b on a card whose
  deadline is a calendar-day or month offset, or two deadline rules for one act (R3-08). Added in v6: "up to <X>", "a
  maximum of <X>" or "a minimum of <X>" in a question (R3-22); a card that shows D6a with no holiday line, or with
  more than one (R3-23); a second D12 extension rule on a card (R3-24); T1 IDs of different widths on one card (R3-18).
  Added in v7: a blank or "0" in the quantity or rate cell of an M3 line (SC19); a backward month offset or a last
  allowed day before the event day (R4-11); an S5 settlement clause other than D17's (R4-09); on a choice row, a
  non-empty `card` field (CP1).
- Extracts category value lists ("<category> is one of: ...") as the admissible domain of an unknown category (R2-08).
- Containers: prose, memo, email thread, key-value record, JSON, YAML, CSV, markdown table, HTML table, fixed-width
  text, bullet SOP (S1-S4); line-item statement (S5 only). Numbers as digits; counts <= 20 may be words.
- **Line accounting (A36).** The parser classifies every line as structure, container boilerplate (defined by the
  container grammar: headers, greetings, sign-offs, table borders) or **unparsed**, and reports the unparsed lines. It
  never sees the attack bank. G3 asserts: on clean rows the unparsed set is empty; on an attacked twin it is exactly
  the line(s) the generator inserted (QC compares line hashes with the twin record), and the rest parses to the clean
  twin's structure.
- **G3 pass:** on 100% of rows, (a) parsed structure hash == A's structure hash, (b) B on the parsed structure == A's
  label, and (c) the line accounting above holds. A parse failure counts as a failure: fix the parser, lexicon or
  template, regenerate; never edit a row.

### 3.4 Named-error distractors (C3, A53)
**Every wrong option on every F2 choice row comes from exactly one named error** (C_DATA_SPEC 2.1 and F2). There are no
"natural closed sets": calendar grids and full band lists are never used as option lists (a band table still shows
every band; the options list a subset).
- Hooks in A (recomputed by B): E-cap (missed cap), E-floor (missed floor), E-capval (cap or floor value picked when it
  does not bind), E-round (wrong mode), E-stage (rounded at the wrong stage), E-exc (ignored exception), E-unless
  ("unless" read as "if"), E-tier (adjacent band: one hook value for the band below and one for the band above; which
  are shown is drawn under the rank rule below), E-mode (marginal <-> flat), E-unit (missing
  conversion), E-pct (percent vs points), E-add (added vs successive discounts), E-base (wrong percentage base),
  E-order (wrong step order), E-day (off by one day), E-bday (calendar days for business days), E-roll (wrong roll),
  E-eom (wrong month-end clamp: overflow, or end-of-month kept; D8), E-hol (holiday ignored), E-ext (extension ignored, or counted from the rolled
  deadline), E-prorate (wrong period length), E-partial (wrong partial-unit rule), E-gross (gross vs net), E-copy (a
  stated input copied as the answer), E-blank (an M4 computed cell read as 0), E-alt:<ID> (the value under one
  specific other listed alternative of SEM dimension <ID>, all other dimensions canonical; R2-16), E-assume (an
  unknown field filled with an assumed value; open-world rows only).
- **E-alt:<ID> is a general hook (R2-16)** on every choice row: one hook per listed alternative of each SEM dimension
  shown on the card, under the one-hook-per-value rule below. Where the dimension has its own hook (E-round for R1,
  E-stage for R2, E-roll for D7, E-mode for B2, E-add for X5, E-base for X6, E-gross for X7, E-order for X1, E-partial
  for R5 and U3, E-prorate for P1, E-ext for D12, E-eom for D8), E-alt:<ID> for an alternative is that same hook, logged once under
  the alternative's E-alt id, so a value both give counts as one hook. Dimensions with no own hook (CMP, OR1 / OR2,
  B1, D4, D5, D10, D13, D14, T1, the X3 form) have E-alt only. In a clause-flip twin, the base's gold is the
  E-alt:<ID> value of the flipped dimension (R1-21).
- **Exactly one named error per distractor (SC3).** A display value is eligible as a distractor only when exactly one
  hook gives it (and it differs from gold). A value that two or more hooks give is not shown. Each distractor logs its
  one error id. Too few eligible values: resample the structure, never pad.
- **Ordered options and gold rank (R2-17).** Numeric options are ordered by value, date options by date, and band and
  named-outcome options by edge rank (S4 windows by date). On every row with ordered options, gold is the smallest
  and the largest of them each with probability 1/k_ord +/- 2 pp (k_ord = the row's ordered options, abstain options
  excluded), checked per option bucket (6).
- **Value, date and count rows.** Options = gold + eligible hook values. A hook value is eligible only when it is
  exactly on the display grid; it is never rounded for display (R7; R3-13). Pick k_ord - 1 hooks so that gold's rank
  among the ordered options is uniform.
- **Band and named-outcome rows.** Options = gold + the bands or outcomes that hook values fall in, each band or
  outcome reached by exactly one hook; 2-9 options. E-tier contributes the band or outcome just below gold, just
  above, or both, drawn so that gold's edge rank among the options meets the rank target above (an end band or
  outcome can have only one neighbour).
- **Case lists (inverted rows; closed-world cards only, R1-19).** Exactly one case qualifies, or none ("None of the
  listed" gold). Each other case is built to qualify under exactly one named error, logged per case.
  **Placement (CP1).** Options are case references from fmt1 `case_refs` (one reference scheme per card), plus "None
  of the listed <cases>" when shown; each case's values are one value line or table row in `state`, keyed by its
  reference, and `state` lists exactly the shown cases. Whether a CL card's rows can show "None of the listed" is
  fixed per card. A card whose rows never show it may carry one fmt1 inverted frame whose cases are in the text
  (IVC04-IVC07); a card whose rows can show it carries no frame sentence, because every such fmt1 frame presumes that
  a case meets the rule. No CL question states how many cases meet the rule.
- **Large buckets.** 10-19 options: hook-rich structures with >= 9 distinct hook values, or case lists of 10-19 cases.
  20-60 options: case lists of 20-30 cases (the token cap, 3.7, bounds the list). A shortfall in a bucket is filled
  with more case-list rows on inverted cards, never with arbitrary values.
- **Abstain options are not hooks.** The option-count bucket k counts every shown option, abstain included; gold-rank
  uniformity is computed over ordered options only. On NEI-gold rows **every** non-abstain option (value, date, band or
  outcome) is an E-assume value: the value, or the band or outcome of the value, under one admissible completion (a
  witness of 3.5), exactly on the display grid and distinct, with no other hook compounded on it (SC3, R3-13). At least 2 completions
  with different labels exist by definition of NEI; the row shows 1 or more such options, as its bucket k needs.
- **Premise_removed twins keep the base's options (R2-11).** When an open-world base row has a premise_removed twin
  (3.6), A builds the base's option list so that every non-abstain option is, besides being gold or an eligible hook
  value under the base, also an E-assume value of the field the twin shows as "not recorded" (the value under one
  admissible completion of that field, nothing compounded). The twin keeps the list unchanged, logging each option as
  "err:E-assume". If no such list exists, the row gets no premise_removed twin.
- **Clause-flip twins keep the base's options (R1-21).** When the base row has a clause-flip twin, A builds the base's
  option list so that every option is gold or an eligible named-error value under **both** the base vector and the
  twin vector (the base's gold is E-alt:<ID> in the twin). If no such list exists, the row gets no clause-flip twin.
- Distractor error ids are logged in `edge` ("err:<id>").

### 3.5 Open world, NEI and missing data (A01, A02, A22, A24, A39)
- **Cards.** Open-world cards are about 13% of F2 cards, **choice-only** (schemas CH-V, CH-D, CH-C, CH-B, CH-O; never
  CL case lists), from S1, S3 and S4. Yes/no rows and case-list rows exist only on closed-world cards (yes/no cannot
  abstain; R1-19).
- **Rendering.** Every open-world row shows **exactly one** field as the literal text "not recorded" (in every
  container; never null, "unknown", a blank cell or a left-out key; R3-11), and every other case field a rule reads is
  printed (R1-05). Every open-world row has **k >= 3** shown
  options, NEI included (XF01: no abstain option on a k = 2 row). The field is **needed** with probability 1/k per
  row, k = the row's shown options, NEI included (gold NEI; SC2; premise_removed twins count in this rate, and the base
  rows' draw is adjusted so each k bucket's NEI-gold share matches its mean 1/k within +/- 2 pp, XF01), and **inert** on the rest (NEI
  shown and wrong). So "not recorded" appears on every open-world row and does not mark NEI. Only case fields can be unknown (W0); rates,
  rule values (the holiday line included, R3-23) and any field used as a denominator are never unknown. The unknown is
  never whether a charge, payment or event of a W2-listed type happened, nor a count of such items (W2's completeness
  settles both); unknown yes/no facts and counts are attributes of the entity or of a listed item (W2; R3-17).
- **The unknown field is always read by a rule (R1-27).** On needed rows it sits on a live decision path. On inert rows
  it is read by at least one rule but is off every decision path because another condition of that rule (or of the
  gate above it) fails for every admissible value. An unknown field that no rule reads is never generated, so "the
  unknown field is named in a rule" is true on every open-world row and predicts nothing.
- **Admissible domain** (from the text and the field type only, never the pack range): amounts: multiples of the
  display unit, >= 0; counts: whole numbers >= 0; dates: searched over 1901-2099; Booleans: both values; categories:
  every value of the field's explicit value list (W2; R2-08); plus every **explicit bound sentence** for that field
  that the parser extracts (a stated range for it, or a stated order between its date and another stated date). The
  unknown field is always one of these five types; durations, weights, distances, hours and other quantities are never
  unknown (R2-07).
- **No implied bounds (R1-06).** An unknown field is never a part of a stated total or whole (a line of a stated sum,
  returned items of stated shipped items), never a sub-span of a stated span, and the renderer never puts sequencing
  words ("then", "later", "before that" and the like) next to an event whose date is unknown. Any order the reader needs
  is stated as an explicit bound sentence. A asserts this on the structure; A's witnesses and z3 satisfy every explicit
  bound.
- **Status.** NEI iff at least 2 distinct option-level labels (shown option, or "no option") are reachable over the
  domain; determined iff exactly one is, and it must be a shown option.
- **A (witness search).** A evaluates a finite candidate set: 0, one display unit, every breakpoint of the label as a
  function of the unknown field (threshold, caps, floors, band edges, rounding boundaries, option values; back-solved
  on the grid) and one unit either side of each, and a sentinel of 10^9 units; for dates, 1901-01-01, 2099-12-31 and
  each constraint or breakpoint date +/- 1 day; every candidate satisfies the explicit bounds. A **needed** field is on
  a decision path and has a witness pair with different labels. An **inert** field is on no decision path for any
  value. A also checks that the status is unchanged when dates are restricted to **the row's own stated year range**:
  2031-2049 for every F2 sampler (S1-S5 state every date inside 2031-2049), and that range shifted with the row under
  MR5 (2059-2077 after +28 years). Otherwise the row is rejected (R1-25). **Natural precedence check (R4-10).** A also
  recomputes the status and the label with every natural precedence of the row's events added as a bound: a
  consequence (an act, payment, refund, return or the like) is not dated before the event that its rule counts from
  or that it answers, and a date listed under a period of the record lies inside that period. Both must be
  unchanged, otherwise the row is rejected, so a reader who applies such an order still gets gold. These bounds are
  a check only: explicit bound sentences stay the only bounds of A's domain and of z3.
- **B.** z3 over the same domain (3.2).
- **Not generated in round 1:** a field on a decision path whose absence leaves the label fixed (z3 finds one label;
  for example a cap that binds for every admissible value).
- **Closed world.** Absent listed-type line items are 0 and absent conditions false (W1). Any other absent field needs
  W3; A asserts this. S4 yes/no rows always print the act date (A05).
- **Never both abstain options on one row.** "None of the listed" appears only on closed-world rows, and only on rows
  with k >= 3 (XF01).

### 3.6 Twins, relation units and selection (A48, A59, C6, C13)

| Twin | Change | Label | Unit |
|---|---|---|---|
| boundary | one decisive input moved by one resolution unit across T | flips (A predicts) | own `call_id` |
| clause_flip | one decisive SEM switch set to a "T" alternative of 2.2 (for example CMP1/CMP3 <-> CMP2, R1 modes, B1 form, B2, D4, D5, D7, D14, OR1 <-> OR2, P1, X5; R3 only on the YN-T threshold cards of 2.2 R3, R3-14, R3-15; X4 only on cards that ask totals over the wider scope, R3-19; B2 only on percent or per-unit tables, R3-20). The twin row sits in a **planned flip variant of the base row's own card** (same `card_id`, pack, schema, instruction family, world, formula type and wordings; one SEM switch apart; its examples follow the variant's vector). Made only where the flip changes no printed number (2.1, R1-16) and the twin keeps the base's option list (3.4, R1-21) | flips to A's alt-label, which must be a shown non-abstain option other than the base's gold (yes/no: the other label; case lists: exactly one shown case other than the base's) | own `call_id` |
| neg / dneg | negated question; double negation | complement / equal | one `call_id`, <= 3 rows (affirmative, `complement`, `equiv`) |
| premise_removed | on an open-world card: the base's inert unknown field is recorded, and a needed field is shown as "not recorded" instead; the twin keeps the base's option list (3.4, R2-11). This is F2's only open-world twin: **F2 has no world twins** (no twin changes W1 <-> W2; R2-10) | NEI | own `call_id` |
| inert | inert value line added (another entity's record, a line dated outside every period a rule reads, a line of a type or row ID that no rule names; values only, never a rule sentence, 2.1; inertness rule below, R3-12) | unchanged | 2-row `equiv` unit |
| attack | injected instruction line, in `state` only (from the format agents' attack bank; never OPI or jagged wording, 7.2 #8; CP1) | unchanged | 2-row `inv` unit |

- **One unit per base.** Each base row joins at most one relation unit (neg/dneg, inert or attack). It may also have
  own-`call_id` twins (boundary, clause_flip, premise_removed), which point to it through `twin_of`.
- **Flip variants (R1-20).** Clause-flip twins link only pre-planned flip variants of the base's own card. Each card
  plans at most 2 flip variants (one dimension each), fixed when the card is built; a dimension is flipped only where
  such a variant is planned. Variants count inside their card: the card count (80 / 150), the one-card-per-pack rule
  and the 128-rows-per-card cap all count the card once, with all its variants' rows. A flip variant also carries its
  own base rows (at least as many as its twins), so being on a flip variant never marks a twin row. Rows log `edge`
  "var:0|1|2" (0 = base variant).
- **Selection by whole twin set (C_DATA_SPEC 2.1 applied to units; SC1).** A selection unit = a base row with its
  relation unit and all its own-`call_id` twins. Its bin = the hardest member's crowd bin (hard > medium > easy).
  1. C_DATA_SPEC's first step ("keep all medium and hard rows and 30% of easy rows"): every unit with a medium or hard
     member is kept whole, so every medium and hard row is kept. All-easy units are drawn at random so that the kept
     easy rows, counting the easy members of kept mixed units, are 30% of generated easy rows. If the easy members of
     mixed units alone exceed 30%, no all-easy unit is kept and the excess is logged (orchestrator item, 9).
  2. C_DATA_SPEC's second step: downsample inside each family x gold label x wording x difficulty-bin cell, with cells
     counted at row level from each row's own label, wording and bin, dropping whole units only (greedy or integer
     program, fixed seed). **Yes/no rows are celled further by k_all** (the shared negcount surface count, F2's
     "cue:"; R2-19, SC13), so equalising yes and no inside each cell meets the G10 yes-rate check of 3.8; the crowd
     bins exist only after scoring, so this check is met here, not at generation. "neg:" is not a selection stratum
     (XF02: polarity logic only).
  3. G10 balance and the difficulty targets (easy <= 25%, medium >= 45%, hard <= 30%) are re-checked at row level after
     selection; a failure re-runs step 2, never splits a unit.
- **Shares (C_DATA_SPEC 2.1; XF03).** Rows in a **label-flip twin set** = 20-25% of F2 rows: a set is a base row plus
  its boundary, clause_flip and premise_removed twins (every member counts). neg / dneg units count **only** toward the
  negation quotas, never toward the 20-25%; boundary, clause_flip and premise_removed sets are raised so that they
  alone reach 20-25%. Attack and inert
  shares count **only the twin rows**, never their bases (R1-28): attacked twin rows are about 5% of F2 rows (C_DATA_SPEC
  "attack twins about 5% of own rows"), inert twin rows at most 5%. About 20-30% of rows also carry one inert but
  relevant-looking fact inside the row (GSM-NoOp control), counted separately.
- **Inertness (R3-12).** An inert twin line and a GSM-NoOp fact are inert only through an attribute that the card's
  rules already read: (i) another entity's record (the question and every rule name the row's entity); (ii) a line or
  fact dated outside every period a rule reads (each rule names its period); (iii) a line of a type outside every
  summing rule's listed types (each rule that sums lines lists its line types by name, so the line is visibly outside
  the sum), or a rate in a row ID that no rate reference names (each rate reference names its row ID or its table's
  governing date). On any card that can carry such a line, A asserts that every summing rule names its entity, period
  and line types. W1 governs only what happened: an inert charge line happened, but it enters a computed amount only
  if a rule's listed inputs include it, and none does; W0 then gives it no effect, and no question asks about it.
  Never used as inert: a line on a card whose sum is not defined by listed line types (a total of "all charges" or
  "the record's total"), a second rate that the card's reference cannot tell apart from the one it uses (a
  "superseded" rate with no row ID or date that the reference reads), or a line that changes any printed number. A
  asserts that the inert line is outside every rule's listed inputs and that the label and every printed number are
  unchanged without it.

### 3.7 Cards, wordings, styles (A47, A49, A50, A57, C1, C2, C12)
- **Card identity (C_DATA_SPEC 2.1).** `card_id` = (F2, sampler, pack, label schema, instruction family), C_DATA_SPEC's
  own tuple. The card's **rule set** = (formula type, SEM switch vector, world) of its base variant. A card has one
  base variant and at most 2 flip variants (3.6); variants share the card_id, pack, schema, instruction family, world,
  formula type and wordings, and differ from the base variant in exactly one SEM switch each. Few-shot and inverted
  cards are separate instruction families.
- **Card difference (C_DATA_SPEC 2.1 read literally inside F2; SC4b, supersedes C12).** Any two F2 cards differ in the
  domain pack **and** in the label schema or rule set. So F2 puts **one card on each pack** (r1: 80 cards on 80 distinct
  training packs; r2: 150 on 150), and no two F2 cards share the same (label schema, rule set). This is feasible: the
  shared pool holds >= 200 / >= 300 packs, and C_DATA_SPEC's ">= 40 packs" (r1 >= 30) is a minimum. Held-out S5 and
  sweep packs are separate from these.
- **Label schemas (R1-19).** Exactly one per card: YN-T (yes/no threshold), YN-D (yes/no on time or late), CH-V
  (value choice), CH-D (date choice), CH-C (count choice), CH-B (band choice), CH-O (named-outcome choice), CL
  (inverted case list). The per-card yes rate p (20-80%) exists only on YN-T and YN-D cards. **p is the probability that
  a row's affirmative proposition** (its question with every inverting cue removed: the threshold comparison, or the
  OP predicate "on time" / "late") **is true** (R2-19); the row's label is that truth value, inverted once per
  inverting cue ("neg:"). So on one card affirmative and double-negated rows have yes rate p, single-negated rows
  1 - p. "The label is drawn first from the card's yes rate" (S1-S5) means: the affirmative truth value is drawn from
  p first, then the label follows from "neg:", and the structure is placed to give it. Open-world cards use CH-V,
  CH-D, CH-C, CH-B or CH-O only; CL, YN-T and YN-D cards are closed-world. "None of the listed" appears only on CH-V,
  CH-D, CH-C and CL rows of closed-world cards.
- **Definition styles** (>= 3, C_DATA_SPEC 2.1): one-line (one sentence per relevant dimension), one-line + 1-2 worked
  examples (about 50% of cards), numbered decision list, and short cards (about 15% of rows, 2.1). No no-card rows.
- **Definition examples vs few-shot cards (R1-29).** A definition-style example illustrates **one clause on a
  fragment**: a single number, date or band applied to that clause, with no document and no question. A **few-shot
  card** (a separate instruction family, 5-10% of cards) contains 1-3 **complete solved rows** (short document +
  question + answer) in the row's own schema and container, and uses the one-line or numbered style with no fragment
  examples, so the two kinds never overlap. Each few-shot example row is <= 200 tokens; a few-shot card is <= 700
  tokens on yes/no cards and <= 500 tokens with 1-2 example rows on choice cards, whose card text is printed twice
  (CP1); every row on it still stays < 1,900 tokens. A few-shot answer is the option text (a value, date, count, band
  or outcome name, case reference or abstain option) or Yes / No, never an option letter (fmt1).
- **Worked examples** (fragments and few-shot rows) are generated by program after the freeze, per card variant, from
  fresh structures under that variant's own SEM vector and world, so a flip variant's examples follow its own clauses.
  Every example's structure hash enters G12 (distinct from every row) and G13 method 6.
- Few-shot cards 5-10% of cards; inverted (CL) cards 10-15% of cards (they carry the case-list rows).
- **Named-option rows and name quotas (C_DATA_SPEC 2.1 quotas, applied to all F2 choice rows).** Band-choice rows (S3)
  and **named-outcome rows** (S1, S2, S4: the card defines 3-6 named outcomes by B1-form ranges of one computed value,
  or, on S4, by date windows whose edges are dates relative to the last allowed day, in B1 forms read on dates; S4,
  R2-06) make up about 30% of F2 choice rows. Masked neutral
  IDs on about 40% of named-option rows (= 10-15% of all F2 choice rows); swapped names (a familiar word that the card
  defines differently) on about 17% (= about 5%). Neutral IDs are unordered and carry no level number. **Where the
  names are defined (CP1):** on CH-B rows by the band table in `state` (each band's name, ID or word with its edges
  and rate); on CH-O rows by the outcome table in the card text, which on choice rows sits in `instructions`; never by
  option-definition lines. Numeric, date and count options are their own text; CL options are case references (3.4).
- **Length budget (CP1; A16.1 (g)).** The builder measures every row with the trainer's real tokenizer (CPU) on the
  rendered prompt `decoder_io.user_msg(row)` (cygnet, schema_branch_mark), in which `instructions` and the option
  texts appear twice, and resamples any row at >= 1,900 tokens. Card caps count the card text once: a card with
  fragment examples is <= 450 tokens on yes/no cards and <= 350 on choice cards; a few-shot card is <= 700 / <= 500
  tokens (R1-29), because a choice card's text sits in `instructions` and is printed twice. Case lists of 20-30 cases
  use <= 4 attributes and <= 25 tokens per case line in `state`, and sit only on cards without fragment or few-shot
  examples; a calendar strip has <= 45 dates (1.1).
- Label-check form: 0 rows. Equality yes/no ("is the <amount> exactly <X>") is not generated; yes/no rows always use a
  comparator (CMP1-CMP3), an on-time / late decision, or an OP money predicate (due, owed, charged; R3-04).

### 3.8 Provenance (2.4) and counting definitions (A32, A33, A52)
`meta.family` "F2"; `sampler`; `depth`; `deep`; `difficulty_bin`, `crowd_pg`; `twin_of`, `twin_kind`; `structure_hash`;
`persona_seed` when present. No `option_level`, no `gold_probs`.

`edge` uses this **closed vocabulary**: "boundary:at|below1|above1|far", "sem:<ID>",
"has:<x>", "bind:<x>", "dec:<x>" (x in cap|floor|exc|round|roll|clamp|partial|hol|ext), "sel:<k>", "ops:<n>",
"cases:<n>", "stated_intermediate", "aid:strip", "nei:needed|inert", "abst:nei|none", "err:<E-id>" (E-alt:<ID>
included), "mech:round|capfloor|exc|partial|plain", "cmp:incl|excl|date|op", "pol:bad_yes|good_yes", "neg:0|1|2",
"syn:<n>", "cue:<n>", "negcmp", "tf:0|1", "world:closed|open", "money:whole|dec2", "b1:upper|lower", "cliff", "tie",
"named:plain|masked|swapped", "short_card", "var:0|1|2". QC computes every section 6 target from `meta` and `edge`
alone.

- **Adjustment tags (R1-24, R2-12, R2-18).** "has:<x>": the row's card states rule x (a cap, floor, exception,
  rounding rule, roll rule, month-end clamp, partial-unit rule or extension; its values may sit in the document, 2.1)
  or, for x = hol, the card or document lists at least one holiday. "bind:<x>": x changes the computed value on this
  row. "dec:<x>": x changes the label on this row (A's label without x differs from gold; on CL rows, the set of
  qualifying cases changes). Both are logged on every row. "has:<x>" is the single denominator of every section 6
  adjustment target. **Which tag a target uses is fixed per schema (R2-18):** "bind:" on value schemas CH-V, CH-D and
  CH-C; "dec:" on label schemas YN-T, YN-D, CH-B, CH-O and CL.
- **Comparator family (R1-23).** "cmp:incl" or "cmp:excl" on yes/no threshold rows (YN-T), from the comparator's CMP
  meaning. "cmp:date" on on-time and late rows (YN-D), whose decision is always D15's inclusive "on or before the last
  allowed day". "cmp:op" on YN-T rows that ask an OP money predicate (due, owed, charged; R3-04), which have no CMP
  comparator. The section 6 comparator targets apply to "cmp:incl|excl" rows only.
- **Negation counts (R1-10, SC6; v5: R3-01 to R3-03, SC13, SC14, SC16).** Three counts, all logged; only "neg:" is
  F2's own, and it is used for polarity logic only (XF02):
  - "neg:<n>" (**inverting count**; polarity logic only): the N1 cues of a yes/no question, from N1's one closed list:
    the syntactic negators not, n't, no, none, nothing, never; the operator "it is not the case that" at the start of
    a TF complement (one cue); and "fail to" only in "fail to meet <its> deadline". Each sits inside the complement P
    of a truth frame (TF, N1), which itself carries no cue, at proposition scope: it negates P's main predicate (the
    comparison or the OP predicate) or is that operator, never inside an entity description (no "the <item> that was
    not <returned>"), never on a fronted main-question auxiliary ("Isn't", "Doesn't", "Wasn't", "Didn't") and never in
    "or not", "whether or not" or "yes or no" (all banned in questions, Q1). So every counted cue inverts the
    proposition. Not cues, and never in an F2 question: the other F5 implicit cues (hardly, unless, other than, lack,
    deny, refuse, rule out) and every other L_neg entry of negcount. **F2 has no falsity predicates** (no "false",
    "untrue", "incorrect" or the like; R2-09). F2 questions use no other F5 L_core token, so never "neither ... nor".
    The only comparators a question carries are CMP1-CMP3 phrases (Q1; CMP4, D2, D3, OR1 and OR2 sit in card rules
    only); a CMP1-CMP3 phrase that contains a negation word ("no less than", "no fewer than", "no more than", "does
    not exceed", "fails to reach") counts 0 here and the row is tagged "negcmp". OP predicates count 0. Choice and
    case-list questions carry no N1 cue, so "neg:0". A's and B's polarity logic and the neg / dneg twin labels use this
    count; **it is not a quota count, a selection stratum, a G10 cell or a G6 / G7 feature** (XF02).
  - "syn:<n>" = **k_syn** of the shared `c_src/common/negcount.py`, called directly on the question sentence (the
    answer instruction, card, options and document are not passed). The 2.1 negation quotas use it: k_syn >= 1 on
    >= 10% of yes/no rows, k_syn >= 2 with the affirmative twin on >= 2%. Under the rules above, k_syn equals the
    number of L_core cues among the N1 cues (negcount exempts the negcmp phrases of CMP1-CMP3 from k_syn).
  - "cue:<n>" = **k_all** of the shared negcount, called directly on the question sentence, with **no F2 list of its
    own** (SC14). It is the G10 "negation count" cell (XF02). Under the rules above, k_all = "neg:" + 1 when the row is
    "negcmp", else "neg:"; QC never derives "cue:" from F2 lists, it reads negcount's output.
  - G10 checks the yes rate 50 +/- 2 per wording x bin x k_all, nothing else for negation (SC13). Bins exist only after
    crowd scoring, so the check is met by the selection step: yes/no cells of 3.6 step 2 include k_all, and yes and
    no are equalised inside each cell (R2-19); G10 re-checks after selection. The cross-family counter is settled
    (XF02; section 9 item 7).
- **Polarity tag (R1-30, R2-20).** Question templates are written against an abstract role side: "the party that pays"
  or "the party that is paid" (for date rows: "the party that must act" or "the party that waits"). Each pack maps its
  decider role to one side. The tag of a row's **affirmative proposition** comes from this fixed table, which never
  looks at the card's charges or other rules; each inverting cue ("neg:") swaps it (bad_yes <-> good_yes):

  | Affirmative proposition | pays | is paid | must act | waits |
  |---|---|---|---|---|
  | the amount is above or at least T ("more than", "at least", ...), or it is "due", "owed" or "charged" | bad_yes | good_yes | not used | not used |
  | the amount is below or at most T ("less than", "at most", ...) | good_yes | bad_yes | not used | not used |
  | "on time", "met its deadline" | not used | not used | good_yes | good_yes |
  | "late", "missed its deadline" | not used | not used | bad_yes | bad_yes |

  "The amount" is always the amount that flows from the paying side to the paid side, so the two money columns are
  mirror images. Lateness is bad for both date sides, also when the card gives the waiting party a late charge. A
  template whose proposition has no entry for its side ("not used") is not used. Logged per row as "pol:<tag>".
- **Structure hash (SC4c).** sha256 of the canonical problem as C_DATA_SPEC 7.2 #6 defines it (rule graph + facts +
  query, names abstracted): the operation graph (node types and edges in a canonical topological order), SEM switch
  vector, world, input values as exact reduced fractions in display units, dates as ISO dates, weekend and holiday
  sets, question target, comparator and threshold; entity, pack and unit names replaced by role ids. This definition
  is self-contained, so the orchestrator can apply it to sealed part P in its own process (C_DATA_SPEC 7.2 blind mode:
  counts and F2 training ids to drop only). F2 builders never see part P. F2 passes G13 method 6 when that run reports
  zero hits after drops (orchestrator item, 9).

---

## 4. Samplers

### S1. Forward formula graphs (training)
- **Shape.** Formula first. Document: a prose memo, request or service note; the document may hold rule values (a
  values section: rates, caps, minimums, N), and every rule sentence is in the card, referring to those values by
  name (2.1; R2-12).
- **Structure.** 2-6 inputs (money, counts, durations, distances, weights, rates) and a formula graph in the 1.1 row
  groups. Formula types (abstract): per-unit charge with a partial-unit rule; percent-of a named base; single discount
  (R8); reimbursement = min(cap, rate x quantity); fee = max(minimum, p% x amount); net = gross - deductions (U5)
  floored at 0; successive or added discounts; per-k pricing. 0-2 exceptions gated by case attributes, joined by
  "unless", "only if", "or", "and". 0-3 inert facts.
- **Decision forms.** Value choice (hook options; 60% of S1 choice rows); named-outcome choice; threshold yes/no
  (closed world): the label is drawn from the card's yes rate (3.7), then T is placed on the side that gives that label, with
  abs(R - T) log-uniform in [2 units, 0.5 R]; structures with R < 8 resolution units are resampled (A43); inverted case
  list (3-30 cases, 3.4).
- **Gold.** A evaluates the graph under the card's SEM vector; comparator and polarity give yes/no; the gold option is
  the option whose value equals the final value, which is on the display grid (R7; R3-13).
- **Metamorphic (G4).** MR1 option shuffle, MR2 consistent rename, MR3 inert addition, MR4 reorder of
  position-independent clauses only (rules keep their numbers; A35), MR6 exact unit restatement, MR7 monotonicity
  (applied only where A confirms that the operation graph is monotone non-decreasing in that input: no input-gated
  exception, no subtraction of that input, no flat table with a falling rate; tested on the compared value; allowed
  flip: no -> yes for > or >=, yes -> no for < or <=, reversed by each negation; A34), MR8 threshold monotonicity, MR9
  negation, MR12 premise removal (open world), MR13 attack.
- **Balance (A44, R1-24, R2-18).** CH-V rows: each adjustment (cap, floor, exception, partial unit) **binds**
  ("bind:<x>") on 50 +/- 5% of the rows tagged "has:<x>". YN-T, CH-O and CL rows: each is **decisive** ("dec:<x>") on
  50 +/- 5% of the "has:<x>" rows, so its naive solver agrees with gold on 50 +/- 5% of them (the same check). The rounding target uses only
  "has:round" rows whose rounding step can reach T (abs(R - T) <= the rounding unit); S1 far rows are exempt and S2
  carries rounding (A43).

### S2. Target-first boundary placement (training)
- **Shape.** Label first, back-solved. Document: a case file or review sheet with one decisive computed quantity and a
  threshold rule in the card. Closed-world cards only.
- **Procedure.** (1) draw the card's yes rate p (uniform 20-80%), then the row's affirmative truth value from p and its
  label from "neg:" (3.7); (2) draw the boundary relation delta
  in {-1, 0, +1} resolution units with P(0) = 0.30, P(-1) = P(+1) = 0.35 (unit = cent, whole currency unit, day or item,
  from the pack); (3) draw the comparator family conditional on delta, label and the parity of "neg:" (polarity logic: it maps
  the label to the affirmative truth value; XF02) so that, per sampler,
  P(yes | inclusive) = 50 +/- 2, P(yes | exclusive) = 50 +/- 2, inclusive share 50 +/- 3, and inclusive share at delta 0
  = 50 +/- 2; the builder asserts all four (A41); (4) draw the decisive mechanism, about 20% each: rounding decides;
  **cap or floor decides** (A40): if the label needs R to satisfy the comparison, the unadjusted value is drawn on the
  failing side of T and the adjustment that moves it to R is used (a floor for > or >=, a cap for < or <=); if the label
  needs R to fail, the reverse; the adjustment value equals R, so the label differs without it; exception decides;
  partial-unit rule decides; plain arithmetic; (5) set R = T + delta x unit and back-solve one free input on its
  integer grid inside the pack range (the pack range is used for generation only, never for NEI) so the forward result
  is exactly R (reject if none); (6) forward-verify with A.
- **Decision forms.** Yes/no 70% (including all negation and double-negation units of S2); value choice 30% with
  near-miss options (E-round, E-stage, E-partial, E-day, E-capval), mostly 2-4 options; named-outcome rows inside the
  choice share.
- **Gold.** Forward value from A; label from comparator and polarity. Clause-flip twins come mainly from S2.
- **Metamorphic (G4).** MR1, MR2, MR7 (as S1), MR8, MR9, MR10 boundary twin (moving the decisive input one unit flips
  the label exactly as A predicts), MR11 clause-flip twin, MR13.
- **Balance.** Delta mix as above per card; mechanism mix within +/- 3 pp; comparator targets of step (3).

### S3. Tiered rate tables (training)
- **Shape.** Table first. A band table (markdown, CSV, HTML, fixed-width or JSON list) with 3-8 bands (10-19 bands on
  <= 10% of S3 rows); each band has its edges as plain numbers and a rate (percent or per unit; a flat fee only on
  flat-mode tables, B2, R3-20); the B1 form
  (one per table) and the B2 mode are card sentences (2.1; R2-12); optional minimum and maximum charge (X4); optional
  category exception (X10, flat mode only); optional second, effective-dated table with its governing date (D10 / D13;
  inert or decisive).
- **Depth.** Computed by program from the node table (1.1); no hand-assigned depths (A29). Examples on a **stated**
  banding amount (allowed on CH-V, YN-T and "pays more than <T>" case-list rows): flat lookup + 1 multiply = depth 1, +
  a fixed fee = depth 2; marginal inside band 1 = depth 1. A computed banding amount (always on band-choice rows, below)
  adds its own nodes: quantity x unit price, then a flat lookup + 1 multiply = depth 2. Marginal across bands with
  every per-band part printed = stated-intermediate row; marginal across bands with nothing printed = deep when >= 3
  unstated operations (R2-15).
- **Edge placement.** Band-choice rows: amount exactly on an edge 30%, one unit below 35%, one unit above 35%. B1 form
  split 50 +/- 5 on the on-edge rows, so "an option equals the amount" is no cue (A46).
- **Decision forms.** Which band (options per 3.4; masked and swapped names per 3.7). **On band-choice rows (CH-B, and
  CL rows that ask "which case falls in <band>") the banding amount is always computed** (at least 1 unstated
  operation, for example quantity x unit price, or the amount after a B3 adjustment); a band lookup on a stated amount
  is not generated there (R1-12, R2-15). Total-charge, threshold and "pays more than <T>" rows may band a stated
  amount, since their charge computation supplies the unstated operation. Total charge (choice; E-tier, E-mode, E-cap, E-floor,
  E-round, E-exc, E-base); threshold yes/no; inverted ("which case falls in <band>" or "pays more than <T>").
- **Threshold placement (R1-22).** On threshold yes/no rows the label is drawn first from the card's yes rate (3.7). On 50%
  of these rows T is near: delta in {-1, 0, +1} resolution units drawn as S2 step 2 (P(0) = 0.30, P(-1) = P(+1) =
  0.35), R = T + delta x unit, and the comparator family drawn as S2 step 3 (conditional on delta, label and negation
  count). On the other 50% T is far: abs(R - T) log-uniform in [2 units, 0.5 R] on the side the label needs
  (structures with R < 8 units resampled), comparator family drawn as S2 step 3.
- **Gold.** A walks bands one by one; B uses the cumulative closed form.
- **Metamorphic (G4).** MR1, MR2, MR3, MR4 (band rows shuffled; edges carry the meaning; X10 refers to edges, not to
  row position), MR6, MR7 (only where A confirms monotonicity, as S1; flat tables with a falling rate have cliffs by
  design), MR9, MR11, MR13.
- **Balance.** Gold band uniform over band positions per table size (+/- 2 pp); cliff rows (flat, falling rate, amount
  just above an edge) about 15% of flat-mode rows, with yes rate 50%. B2: marginal on 30 +/- 3% of S3 rows, flat on the
  rest (exempt from the per-dimension uniform rule of section 6, because marginal rows add depth and the deep share is
  capped; A45).

### S4. Calendar and business-day rules (training)
- **Shape.** Date rule first. Document: a notice, schedule, correspondence log or calendar strip. Years 2031-2049 for
  every stated date; weekday of every anchor and holiday stated (D9); a calendar strip whenever the card shows D6a
  (business days are used, or D7 appears), and for long or month-crossing windows (1.1; R1-14, R3-08); holidays invented and listed with dates and weekdays, **only on
  weekdays** (A12). 0-3 holidays are listed per row, on the one holiday line that every card showing D6a prints on
  every row (the value "none" when the row has 0; 2.1, D6a, R3-23). On non-deep rows a business-day addition has N <= 10 and at most 1
  listed holiday inside its window (the others fall outside it); N > 10 or 2-3 holidays inside the window only on deep
  and sweep items (R1-13).
- **Rule types.** N calendar days (D4a, or D4b on a flip variant, + D15); N business days (D6a + D6b + D7 + D15); M months forward with clamp, then roll (D8; R4-11); day
  count between dates (D5) and business-day count (D14); proration by days with at most 1 money operation and days
  used printed (P1); effective-date split (D10) and one-off charges (D13, always with D10's boundary sentence);
  at most one extension rule per card, of K days if <condition> (D12, with UN1 / O1 / O3 / OR connectives inside that
  one rule; R3-24). The last allowed day always comes from
  an offset rule (D4, D6b or D8, possibly with D12) and is on or after the event day after every extension and roll
  (R4-11), so every on-time, late and date row has at least 1 unstated
  operation; a fixed "by <D>" or "before <D>" date (D2) appears only as an effective date or a condition, never as
  the deadline itself or as a window edge (R1-12, R2-06).
- **Decision forms.** Last allowed day (date choice: 2-9 hook options; 10-19 only with >= 9 distinct hook values);
  on-time yes/no ("on time?" and "late?" question kinds; closed world; the act date is always printed, A05); count
  choice (business-day or calendar counts); named-outcome rows (date windows, below);
  inverted ("which of these <acts> missed its deadline?": exactly one, or none; every other act is judged late under
  exactly one named error). No calendar grids as option lists (3.4).
- **Date windows (named outcomes; R2-06).** The card defines 3-6 named outcomes as a B1 table on the act date, with
  every edge a date relative to the last allowed day L, and shows D16 (2.2). So "<k> calendar days after the last
  allowed day" = L + k (k whole, >= 1; L itself is "the last allowed day", and "1 calendar day after" is the first
  late day). Adjacent windows share their edge dates (B1, R3-06).
  The B1 sentence of 2.2 is read on dates ("under" = before, "over" = after, "or more" = on or after; "up to and
  including" and "up to but not including" as written), one B1 form per table; these tables count in B1's 50 +/- 5
  split of tables and of on-edge rows (an on-edge row has the act date on an edge date). The window is found by
  comparing the act date with the edge dates: no days-late count is printed (1.1); the canonical graph has one node
  for the act's offset from L (1.1 node table), so a D4 deadline plus a window lookup is depth 2. The act date is
  always printed; window edges are never fixed dates (D2).
- **Edge placement (A42).** The label is drawn first from the card's yes rate (3.7), through the question kind (yes on "on
  time?" = on time; yes on "late?" = late). On-time acts: on the last allowed day 60%, 1-3 days earlier 40%. Late acts:
  on the first late day 60%, 2-4 days after the last allowed day 40%. Each question kind's aggregate yes rate is
  50 +/- 2. On-time and late rows are tagged "cmp:date" (D15 is always inclusive) and are **exempt from the section 6
  comparator targets** (inclusive share, P(yes | family), at-boundary inclusive share); they count in the boundary-zone
  target through their 60% placements within 1 day (R1-23).
- **Gold.** A iterates days; B uses ordinals and the closed form; both use only the stated weekend and holiday sets.
- **Metamorphic (G4).** MR1, MR2, MR3 (a holiday outside the window; another party's deadline), MR5 shift every date and
  holiday by +28 years (inside 1901-2099 weekdays and leap years repeat; stated weekdays unchanged; label unchanged;
  the 3.5 year-window check shifts with the row to 2059-2077, R1-25), MR8 (a later action date can flip only on-time
  -> late), MR9, MR10, MR11 (D4, D5, D7, D12, D14 flips), MR12, MR13.
- **Balance.** Roll direction, clamp, holiday and extension change the row's target on 50 +/- 5% of the rows tagged
  "has:<x>", by the per-schema tag of 3.8 ("bind:<x>" on CH-D and CH-C rows; "dec:<x>" on YN-D, CH-O and CL rows; R1-24,
  R2-18); D7's three alternatives uniform +/- 5 over its decisive rows; the calendar-days naive solver
  agrees with gold on 50 +/- 5% of business-day yes/no rows.

### S5. Line-item statements (held out; mix-tuning dev only)
- **Shape.** A statement with columns description | quantity | rate | amount. Each amount is either printed, or
  carries the M4 computed-cell marker (quantity and rate shown; the line amount is the line's pricing: quantity x rate,
  1 unstated operation, or B4's split on that line; rounding and caps then apply to it; R2-04), or is blank under M3
  ("A blank cell in the <amount> column means nothing was charged on that line"), which is allowed only on a line
  with no quantity and no rate, whose quantity and rate cells read "none" (R1-01, R3-07, SC19). S5 cards are closed-world only. Deduction lines positive and
  subtracted (U5). Rules: a multiplier on the part above a stated threshold (B4, never a
  comparator; A19; its scope always named, and a scope wider than a line holds at most one line of the quantity,
  R3-19), an allowance with a cap (X4 with named boundaries; under a multi-line scope only scope totals are asked,
  R3-19), a percentage deduction with a floor or cap,
  per-line vs total rounding (R2), a settlement date = period end + N **calendar** days, the clause always saying
  "calendar days", stated by D17 (the day of the period end is not counted; the roll rule applies to the settlement date), with D7 and
  D6a (never D6b; A58, R3-08, R3-09, R4-09). All rates invented and stated; no real payroll or tax rule.
- **Use.** 400 mix-tuning-dev items + 12 per depth level in the sweep (5). Held-out packs and the 50 held-out styles.
  Never a training row; its structure hashes are disjoint from every training row (G12, G13 method 6). The statement
  container is never used by S1-S4, so S5 measures transfer to a new shape.
- **Gold, solvers, parse.** Same A, B, parser (statement container) and SEM table.
- **Metamorphic (G4).** MR1, MR2, MR3, MR4 (line reorder), MR5, MR6, MR7 (as S1), MR9, MR13.
- **Balance.** Yes/no 50%, yes 50%; threshold placement on yes/no rows as S3 (50% near with S2's delta mix and
  comparator draw, 50% far; R1-22); every training-family G10 target applies.

---

## 5. Mix-tuning dev and depth sweep
- Dev: 400 S5 items (C_DATA_SPEC 10). Depth sweep: 5 levels x 60 = 300 items, levels = depth 1, 2, 3, 4, 5 (depth 5 is
  sweep-only, never trained); per level 12 items from each of S1-S5, held-out packs and styles, yes/no 50% with yes
  50%, structure hashes disjoint from training.
- **Sweep items are separate instances (SC5).** C_DATA_SPEC 2.1 says deep items "form the depth sweep"; C_DATA_SPEC 10
  says no mix-tuning-dev item shares text with a C training row. F2 reads both together: deep **training** rows and
  sweep items come from the same generator settings, but sweep items are separate instances (held-out packs and
  styles, structure hashes disjoint from training, no shared text). No deep training row is ever a sweep item.
- Sweep items have **no printed intermediate results**. Printed day counts are allowed, because they are stated inputs
  (1.1), so depth = unstated operations = total operations (1.1 node table) (A55, R1-15). S4 sweep items with
  proration or sub-spans are therefore valid.
- **Chance** for a level = the mean over its items of 1/k, with k = the shown options (2 for yes/no) (A55).
- Round-2 depth cap = the deepest level where CAND - C1 >= +3 pp and CAND >= chance + 15 pp (C_DATA_SPEC 10; recipe
  7.2).

## 6. Balance targets (G10) and shortcut guards (G6-G8), F2

Terms (A44, R1-24, R2-18): **binds** ("bind:<x>") = the adjustment changes the computed value, used on the value
schemas CH-V, CH-D and CH-C; **decisive** ("dec:<x>") = it changes the label, used on the label schemas YN-T, YN-D,
CH-B, CH-O and CL (on CL: the set of qualifying cases changes). The single denominator for both is the rows tagged
**"has:<x>"**: rows whose card states rule x (its values may sit in the document), or for holidays rows whose card or
document lists one (3.8; R2-12).

| Target | Value |
|---|---|
| Yes/no share | 45-55% of F2 rows (planned 51.7%); yes/no rows on closed-world cards only |
| Yes rate | per card p uniform 20-80% (YN-T and YN-D cards; p = P(affirmative proposition true), 3.7, R2-19); aggregate 50 +/- 2 per wording x difficulty bin x negation count, the count being k_all ("cue:<n>", the G10 cell count of XF02) only; "neg:" is not checked here (XF02, SC13); met through the 3.6 step-2 cells (R2-19); S4's two question kinds each 50 +/- 2 |
| "Yes = bad outcome" | 50 +/- 5 of all yes/no rows (XF04; 3.8 polarity table, per affirmative proposition and role side, swapped by each inverting cue; R2-20) |
| Negation (XF02, XF10) | >= 10% of yes/no rows have k_syn >= 1 ("syn:", shared negcount); k_syn >= 2 on >= 2% with its affirmative twin in the unit. Every N1 cue sits in a truth-frame complement (N1). "neg:" stays for polarity logic only |
| Boundary zone | rows with abs(R - T) <= 1 unit (1 day on "cmp:date" rows) are >= 40% of yes/no rows (planned about 59% of training yes/no rows: S2 all, S3 half, S4 60%; S5 dev items half); at-boundary rows tagged "cmp:incl" or "cmp:excl" inclusive 50 +/- 2 |
| Comparators | over "cmp:incl" and "cmp:excl" rows only (S4 "cmp:date" rows and OP money "cmp:op" rows exempt, R1-23, R3-04): inclusive vs exclusive 50 +/- 3; P(yes given inclusive) and P(yes given exclusive) each 50 +/- 2 per sampler (A41) |
| Adjustments and naive solvers (one check) | label schemas (YN-T, YN-D, CH-B, CH-O, CL): each of cap, floor, exception, rounding, roll, clamp, partial unit, holiday, extension is "dec:<x>" on 50 +/- 5% of its "has:<x>" rows, which is the same as its naive solver (no-cap, no-exception, no-rounding, calendar-for-business-day, ...) agreeing with gold on 50 +/- 5% of them; value schemas (CH-V, CH-D, CH-C): "bind:<x>" on 50 +/- 5% of "has:<x>" rows (R2-18). Rounding on YN-T rows: denominator = "has:round" rows with abs(R - T) <= the rounding unit (A43); OP money rows ("cmp:op") are outside it, since rounding never changes their label (R3-14) |
| Decisive semantics | >= 40% of rows carry >= 1 "sem:*". For each dimension, on rows where it is decisive, its alternatives (as used by that sampler, 2-4) are uniform +/- 5 pp (A45). Exemption: B2 marginal / flat 30 / 70 +/- 3 on S3 |
| B1 forms | each form 50 +/- 5 of band tables and of on-edge band rows; S1 / S2 named-outcome tables and S4 window tables count as band tables (R2-06) |
| Clause presence | G7 tests the presence of every SEM clause against the label; no presence feature may fail |
| Option buckets (choice) | 2-4: 35%; 5-9: 35%; 10-19: 15%; 20-60: 15% (large buckets from hook-rich rows and case lists, 3.4) |
| Gold position | letter uniform per bucket (chi-square p > 0.01); rank uniform over ordered options (numeric by value, dates by date, bands and named outcomes by edge rank; gold smallest and largest each 1/k_ord +/- 2 pp; 3.4, R2-17); longest option gold within 1/k +/- 2 pp |
| Verbatim copy | P(gold value appears in the text) within +/- 3 pp of the mean distractor rate (E-capval and E-copy supply the matching distractors; printed intermediates and strips are counted as text) |
| Abstain options (C11, SC2; XF01) | NEI on every open-world row (about 27% of F2 choice rows; every open-world row has k >= 3); "None of the listed" on about 10% of closed-world choice rows (CH-V, CH-D, CH-C, CL), only rows with k >= 3, display drawn before gold; never both on one row. On each row the abstain option is gold with probability **1/k** (k = shown options, abstain included), so "pick the abstain option" scores exactly chance; G10 checks the observed abstain-gold rate against 1/k (the mean of 1/k over the bucket's rows) within **+/- 2 pp, per k bucket and per abstain option**, NEI and "None of the listed" checked separately (XF01, SC12). Expected gold rates: NEI about 20% of open-world rows (k 3-19; XF01), "none" about 15-20% of rows that show it. Each is wrong on >= 50% of the rows that show it (1 - 1/k >= 0.5; C_DATA_SPEC F6). F2 abstain gold about 7% of F2 choice rows (C_DATA_SPEC F6's all-family "about 10%" is carried mostly by F6) |
| Named-option rows | about 30% of F2 choice rows; masked 10-15% and swapped about 5% of all F2 choice rows (C_DATA_SPEC 2.1) |
| Depth (disjoint groups, 1.1) | plain depth 1 about 30%, plain depth 2 about 45%, stated-intermediate about 17%, deep <= 10% (target 8%). Every row has >= 1 unstated operation (R1-12); printed day counts are stated inputs and count in no group's total (R1-15); every case of a case-list row is in one group, which the row counts in, with depth = the per-case maximum (R1-11, R2-21) |
| World | closed about 87% / open about 13% of cards |
| Money format | whole-unit vs two-decimal amounts 50/50 over money rows |
| Difficulty (crowd) | easy <= 25%, medium >= 45%, hard <= 30%; selection inside family x label x wording x bin cells (yes/no rows also x k_all; R2-19, SC13), by whole twin set (3.6, SC1) |
| Twins (3.6) | label-flip twin sets 20-25% of rows; attacked twin rows about 5% of rows; inert twin rows <= 5% of rows (twin rows only, bases not counted; R1-28) |

G6 (>= 5,000-row separate QC sample from the same generators) and G7 add these F2 features to the metadata baseline:
threshold magnitude, result magnitude, sign(T - largest stated amount), sign(T - naive sum), number of stated amounts,
roundness of T, rounding mode, comparator family ("cmp:"), mechanism, sampler, pack currency and units, cents vs whole,
B1 form, presence of each SEM clause, short card, card variant ("var:"), world, "not recorded" present, number of rules
that read the unknown field, named-option style, number of options, case count, calendar strip present, "syn:" (k_syn) and "cue:" (k_all)
counts, truth frame present ("tf:"), "negcmp". Each must sit at chance + 2 pp (G6) and pass the z-test (G7). G8 AFLite < 10%.

**G6 chance (SC2).** Yes/no rows: 0.5. Choice rows: the mean over the rows of 1/k, k = the row's shown options with
any abstain option included, computed per option bucket. G7's p0 = 1/k per row as C_DATA_SPEC states. Because the
abstain option is gold with probability 1/k on every row that shows it, neither "pick the abstain option" nor "not
recorded present" beats chance on any k.

## 7. Gate map for F2
G0 this file (v7, frozen) + all second-session ambiguity lists, all resolved (10, 12, 13, 14, 15; 0 open label-flip ambiguities, A16), and the 1-page spec per
generator with its semantics table (11, SC7); orchestrator items in 9 are outside F2. G1 meta, licence, persona-seed
parent. G2 100% (3.2). G3 100% (3.3, incl. line accounting and the R1-01 / R1-04 / R2-09 / R2-12 / R3 (v5, v6) / v7 rejections). G4 >= 3 relations per sampler,
100% on >= 1,000 rows each, Hypothesis (MPL-2.0) for property tests (4). G5 300 rows, flag-only reader, zero confirmed
wrong golds. G6-G8 (6). G9 crowd on the free L4. G10 (6). G11 no surface template above 2% of F2; seeds ROUGE-L < 0.7;
one card per pack. G12 one surface form per structure except planned twins and format variants; worked-example
structures included. G13 section 7 incl. structure hash vs the mix-tuning dev (F2's own run) and vs sealed part P (the
orchestrator applies the 3.8 canonical form in its own process; F2 passes when that run reports zero hits after drops;
SC4c, 9) and the template check vs dev and eval wordings (program only). G14 nothing but this file before the sealed
commit. G15 loader round-trip: fmt1 `card.loader_check` on 100% of rows (also a G0 / G3 gate line, run before G3; CP1),
plus the relation-unit and real-tokenizer length checks (3.7). G16 optional. G17 cartography. G18 not applicable (no F2 ordinal rows); the F2 builder
asserts that no row carries `option_level`; if the orchestrator rules band and named-outcome rows ordinal, the side
file of section 1 supplies `option_level` and G18 runs (SC4a).

## 8. v1 open questions: decisions
1. Depth counts arithmetic operations only, from the fixed node table; selection steps are capped at 3 separately
   (1.1). **Decided.**
2. The named-error rule binds **every** F2 choice row (C_DATA_SPEC); the natural-closed-set exception is dropped; large
   buckets come from hook-rich rows and case lists (3.4). **Decided (C3).**
3. Masked and swapped quotas apply to all F2 choice rows, met through named-option rows (3.7). **Decided (C2).**
4. F2 uses short cards, never no-card rows; every label-flipping clause is in the card (2.1). **Decided (C1).**
5. Depth sweep: depth 1-5, 12 items per sampler per level, S1-S5, no printed intermediate results (printed day counts
   allowed, R1-15), separate instances from training (SC5), chance = mean 1/k (5).
   **Decided.**
6. Open-world rows where a field on a decision path cannot change the label are left out of round 1 (3.5).
   **Decided.**
7. Equality yes/no is not generated, as a proxy of the label-check form (3.7). **Decided.**
8. S5's statement container is excluded from S1-S4 (4, S5). **Decided.**
9. Business-day addition is 1 operation only for N <= 10 with <= 1 holiday, and this rule wins over the 14-day rule
   (1.1). **Decided.**
10. F2 abstain gold is about 7% of F2 choice rows (abstain gold with probability 1/k per row), inside the about-10%
    all-family target that F6 carries (6). **Decided (C11; changed in v3 by SC2).**

## 9. Items for the orchestrator (C_DATA_SPEC or register text that F2 cannot change)
1. **LICENCE_REGISTER section 3 (C16, SC4d).** Section 3 still reads "no third-party text" for own program rows. F2
   follows C_DATA_SPEC v4 F4 (persona seeds) and register section 4 (`gd_onet_occupation` KEEP). Text fix: add that
   own-row packs may carry O*NET occupation-title persona seeds (CC BY 4.0, parent `gd_onet_occupation`, class
   `no_new_rows`, which passes for persona seeds), credited in the notices file. F2 rows keep `meta.licence` "CC0 1.0
   (program-generated)".
2. **Structure hash vs sealed part P (C17, SC4c).** C_DATA_SPEC 7.2 #6 and 9 (d) need the comparison to run; the sealed
   agent never reads C specs. F2's canonical form (3.8) is self-contained. Request: the orchestrator applies it to the
   sealed part-P export in its own process (blind mode: counts and F2 training ids to drop only). Until that run exists,
   F2's G13 is "pending" (not passed); F2 passes G13 when the run reports zero hits after drops.
3. **C_DATA_SPEC 2.4 ordinal list (C14, SC4a).** F2 follows C_DATA_SPEC's enumerated list and the A4 sizing (F7 +
   commit Score + replay), so F2 band and named-outcome rows are not ordinal. Request: list them next to F8 bins. If
   the orchestrator rules them ordinal instead, F2 adds `option_level` from its side file (section 1) and runs G18; no
   regeneration is needed.
4. **Card difference (C12, SC4b): no action needed.** v3 adopts C_DATA_SPEC 2.1's literal pairwise reading inside F2
   (one F2 card per pack; 3.7). Pool dependency: F2 needs 80 / 150 distinct training packs plus its held-out S5 and
   sweep packs from the shared pool (>= 200 / >= 300).
5. **Selection overflow (SC1).** F2 applies C_DATA_SPEC's "keep all medium and hard rows, 30% of easy rows" to whole
   twin sets (3.6). If the easy members of mixed sets alone exceed 30% of generated easy rows, F2 keeps them (units are
   never split) and logs the excess. Request: confirm this deviation, which only ever arises in that case.
6. **Deep items vs the depth sweep (SC5).** C_DATA_SPEC 2.1 ("deep items form the depth sweep") and 10 ("no item shares
   text with a C training row") need one reading. F2 uses: same generator settings, separate instances (5). Request:
   state this reading in C_DATA_SPEC 2.1.
7. **One cross-family negation counter for G10 (SC6). Settled (XF02; v5: SC13, SC14).** F2 logs "syn:<n>" = k_syn
   and "cue:<n>" = k_all, both read from `c_src/common/negcount.py` called directly on the question sentence (no F2
   list), and its own inverting count "neg:<n>" for polarity logic and twin labels only. The 2.1 quotas use k_syn and
   the G10 cells k_all; "neg:" is in no cell, quota or check. No action needed.
8. **G0 format (SC7).** Section 11 adds the 1-page spec per generator with its semantics table; the long body stays as
   the shared reference. Request: accept this layout as meeting G0.
9. **Marker table row for F2 (XF06; R3-07, R3-11).** `c_src/common/MARKERS.md` section 3 lists F2's blank as "M3 closed =
   0, M3 open = unknown" and "Stricter than the table: none". v5 narrows F2: M3 is closed-world only (a blank cell in
   the named amount column = nothing charged); F2's only unknown marker is "not recorded" (every container); F2 never
   renders null or "unknown" and its parser rejects them; a left-out key on a closed-world card means absent (W1 / W3),
   and no rule-read key is left out on an open-world card. This is a narrowing inside the table, not a conflict.
   Request: update the F2 row (blank: "M3 = 0, closed-world amount column only; B1 = no edge"; missing key: "closed:
   absent (W1, W3); open: never for a rule-read field"; stricter: "null and 'unknown' never rendered"). **Done in MARKERS v1.1.**
10. **MARKERS F2 row and sha refresh (SC19; v7).** v7 puts the XF06 zero marker "none" in the quantity and rate cells
    of an M3 line (2.2 M3). Request: MARKERS v1.2 adds it to the F2 row (zero / absent: "none" in an M3 line's
    quantity and rate cells) and records F2's v7 sha256 in `markers.json` after re-reading F2's marker references
    (2.1 rendering rule incl. XC-01, W1, W2, W3, M3, M4, B1, R1-01, R1-05, R3-07, R3-11, SC19). `test_markers.py`
    fails on the v7 sha until then.
11. **Left-out keys, MARKERS M4 (XC-01; cross issues r2, issue 1).** F2 already follows the recommended "no" ruling:
    a left-out key on a closed-world card is absent (W1) or the W3 default, never unknown, and no rule-read field is
    left out on an open-world card (2.1). No F2 change is needed under either ruling.
12. **A16.1 (g) placement (CP1).** Applied in v7 (2.1, 3.3, 3.4, 3.7, 7). No orchestrator action needed.

---

## 10. Resolved ambiguities (v2 review)

**v3 note.** Section 12 governs wherever it changes a row below. Rows changed in v3: A01 (explicit bounds only, year
window per row: R1-06, R1-25), A11 (30-day spans: R1-08), A29-A30 (printed day counts are stated inputs; at least 1
unstated operation: R1-12, R1-15), A31 (strip rule: R1-14, R1-26), A32 (two negation counts: R1-10, SC6), A33
(polarity per template and role side: R1-30), A39 (explicit bounds in z3: R1-06), A44 (has / bind / dec: R1-24), A47
and A50 (card text and examples per card variant: R1-20), A49 and C12 (one card per pack; flip variants: SC4b, R1-20),
A53 (one hook per distractor: SC3), A55 (sweep: R1-15, SC5), A59 (twin rows only: R1-28), C11 (abstain gold 1/k: SC2),
C13 (selection: SC1), C17 (part-P path: SC4c).

**v4 note.** Rows whose text was out of date have been edited in place to the current rule (each carries a "[v4: ...]"
tag naming the source), so no row below states a superseded number or rule: A31, C04 (printed counts: R2-06), A32 (XF02),
A33 (R2-20), A44 (R2-18), A47 (R2-14), A49, C12 (XF09), A53 (SC3), A59, C06 (XF03), C11 (SC2, XF01).

**v5 note.** Rows edited in place to the round-3 rules (tag "[v5: ...]"): A02 (R3-07, R3-11), A13 (R3-08), A21
(R3-07), A27 (R3-05, R3-06), A32 (SC13, SC14), A54 (R3-01, R3-09, R3-10), A58 (R3-08, R3-09), C11 (XF01, SC12).

**v6 note.** Rows edited in place to round 3's remaining items (tag "[v6: ...]"): A03 (SC17, R3-21), A04 (R3-13), A13
(R3-23), A14 (R3-18, SC18), A17 (R3-24, SC17), A19 and A20 (R3-19), A51 (R3-13), A54 (R3-22); in 12.1 R1-09 (R3-21)
and R1-18 (R3-13); in 13.1 R2-02 (R3-15) and R2-07 (R3-17); in 14.1 R3-04 (R3-14), R3-08 and R3-11 (R3-23).

**v7 note.** Rows edited in place to round 4 and CP1 (tag "[v7: ...]"): A01 (R4-10), A17 (R4-11), A25 (R4-01,
R4-02), A57 (CP1), A58 (R4-09); in 12.1 R1-01 (SC19), R1-06 (R4-10), R1-29 (CP1); in 13.1 R2-12 (R4-09), R2-13
(R4-04, R4-08); in 14.1 R3-04 (R4-06), R3-09 (R4-09).

### 10.1 Ambiguities A01-A59 (one semantics each)

| ID | Resolution | Where |
|---|---|---|
| A01 | Admissible completions come from the text and the field type only, never the pack range: amounts in display units >= 0, counts whole >= 0, dates limited only by explicit bound sentences (searched 1901-2099, with a check that the status is unchanged on 2031-2049) [v7: R4-10: W2 says "any calendar date, except where a sentence of the record bounds that date"; status and label are also checked unchanged under natural precedences], Booleans both, categories as listed, plus bounds the text states. A's witness search and B's z3 use this same domain; the round-1 exclusion is evaluated on it | 2.2 W2, 3.5 |
| A02 | The W2 clause bounds the unknowns: every charge, payment and event that happened is listed; only a field shown as "not recorded" is unknown [v5: R3-07, R3-11: M3 has no open form; the unknown is the literal "not recorded" in every container, never null, "unknown", a blank or a left-out key]. Exactly one such field per open-world row | 2.2 W2, 3.5 |
| A03 | The invariance filter runs over the Cartesian product of the filter alternatives of all omitted dimensions together. Dimensions with no testable alternative are "never" omitted (W0, world clause, UN1, O1-O3, D1, D11, R6, U1, U2, X9, and others marked "never"); R4 (round every step) and X8 (negatives allowed) get real filter alternatives [v6: SC17, R3-21: D8 is now "never" on every month-offset card, so it has no filter alternative; R4's filter tests intermediates rounded half-up to display precision and intermediates rounded in R1's mode and unit; U3's filter tests pro rata, as a full k and complete blocks only] | 2.1, 2.2 |
| A04 | Alt-label for choice rows = the shown option whose value equals the alternative value exactly [v6: R3-13: nothing is rounded for display; an off-grid alternative value equals no option], else "None of the listed" if shown, else "no option"; band/outcome rows use the alternative value's band or outcome; case lists use the qualifying set. Decisive iff alt-label differs from gold | 2.1 |
| A05 | The act date is never omitted on S4 yes/no rows (and every act on an inverted S4 row has a date) | 3.5, S4 |
| A06 | The zero default covers only listed-type line items (charges, payments, deductions); absent conditions are false. Any other absent numeric field on a closed-world card needs the new W3 clause "If <field> is not given, use <D>."; A asserts coverage | 2.2 W1, W3, 3.1 |
| A07 | W0 now ends "an <item> is <due> only when a listed rule makes it <due>", so plain "if" (O2) gives "due exactly when at least one listed rule makes it due" | 2.2 W0, O2 |
| A08 | O1 is for conjunctions only. New O3 for "only if <c1> or <c2> (either or both)" with the second sentence "When at least one of these holds, ...". Mixed and/or never appears under "only if" | 2.2 O1, O3 |
| A09 | New D15: an act on or before the last allowed day is on time, including one on or before the event day; after it is late. Shown on every on-time/late row; round 1 places no act on or before the event day | 2.2 D15, S4 |
| A10 | New D14 business-day count: "Count the business days after <D1> up to and including <D2>." (twin: both included); never omitted on business-day count rows | 2.2 D14 |
| A11 | [v3: 30-day spans restricted, R1-08] Days used in a proration are always printed as a number (C_DATA_SPEC "state day counts"), so endpoint inclusion and the day-31 / February questions do not arise; the 30-day basis only sets n = 30 | 1.1, 2.2 P1 |
| A12 | No listed holiday ever falls on a weekend day (generator constraint; A and B both assert), so A's loop and B's closed form agree and no substitute day is implied | 2.2 D6, 3.1, 3.2, S4 |
| A13 | Whenever D7 appears, D6a, the business-day definition (weekend set plus the holidays of the document's one holiday line, which says "none" when there are none [v6: R3-23]), appears too [v5: R3-08: D6's counting sentence is now D6b, shown only when the deadline adds business days] | 2.2 D6a, D6b, D7 |
| A14 | Tie-breaks use stable attributes only (lower ID number, earlier date; [v6: R3-18, SC18] fixed-width ID numbers compared as numbers, no priority keys), never list position; MR4 and the option shuffle cannot change the gold | 2.2 T1, 3.1 |
| A15 | New X10: "<Category> pays the rate of the band with the next lower edges ...; in the lowest band nothing changes. Band edges do not change." Flat mode only; never in marginal mode | 2.2 X10, S3 |
| A16 | X3's compared amount is the final target computed with only that exception applied and every other step unchanged; equal results go to the lower rule number | 2.2 X3 |
| A17 | New D12 extension: K calendar or business days (always stated), counted from the last allowed day before any roll; the roll rule is applied once at the end (twin: count from the rolled day, roll again). [v6: R3-24] At most one D12 rule per card. D8: clamp first, then one roll; [v7: R4-11] month offsets go forward only, so "M months before" is not generated [v6: SC17: D8 shown on every month-offset card; the day number is kept also from a month's last day] | 2.2 D8, D12 |
| A18 | New D13: a one-off charge or band lookup uses the rate in force on a named date (event day or invoice date); S3's second table names its governing date | 2.2 D13, S3 |
| A19 | New B4 [v6: R3-19: scope phrase added]: "In each <scope>, units up to and including the <X>th are paid at the base rate; each unit after the <X>th ..." (other quantities: "In each <scope>, the part of <quantity> over <X>"); a scope wider than a line holds at most one line of the quantity; never phrased as a comparator. S5 uses B4 | 2.2 B4, S5 |
| A20 | X4 always names the period boundaries (claim, line, calendar week Monday to Sunday, calendar month, calendar year 1 January to 31 December); rolling windows are never used [v6: R3-19: under a scope that can hold several lines, only scope totals (or values computed from them) are asked; no allocation rule exists] | 2.2 X4 |
| A21 | One world switch per card; M3 has no separate twin. [v5: R3-07] M3 is closed-world only: "A blank cell in the <amount> column means nothing was charged on that line"; open-world cards have no blank amount cell; B1 edge blanks are never M3's; A asserts | 2.2 M3, 3.1 |
| A22 | Never both abstain options on one row: NEI only on open-world rows, "None of the listed" only on closed-world rows. NEI is defined over option-level labels with "no option" included | 2.2 A1, 3.5 |
| A23 | "None" per form: value/date/count = no shown option equals the value; case list = no listed case meets the rule; bands and named outcomes = never shown; calendar grids are not used | 2.2 A1, 3.4 |
| A24 | Open-world cards are choice-only; yes/no rows exist only on closed-world cards | 1, 2.2 W2, 3.5 |
| A25 | Rounding units are 10^k of the display unit only; rounding never applies to a value that can be negative (A asserts), so half-up = toward the larger value. Coarser steps such as quarter hours are partial-unit rules (R5) on a stated unit [v7: R4-01, R4-02: floor and ceiling leave on-grid values unchanged; half-even only with rounding units of at most one whole unit] | 2.2 R1, 3.1 |
| A26 | New R8: "A <p>% discount on <base> means paying (100 - <p>)% of <base>." Base named per X6; 1 operation | 2.2 R8, 1.1 |
| A27 | B1 gives both full forms (upper-inclusive: "up to and including / over ... up to and including / over"; lower-inclusive: "under / from ... up to but not including / or more"); one form per table; twins flip the whole table [v5: R3-05, R3-06: adjacent bands share edge values (no gapped edges); marginal tables over whole-unit counts use the upper-inclusive form only, and B2's marginal clause states the measure] | 2.2 B1, B2 |
| A28 | Built-ins are listed: Gregorian calendar (7-day week, month lengths, leap years, 12 months a year), 24 hours a day, 60 minutes an hour. Every other conversion is stated; A asserts | 2.2 U1, 3.1 |
| A29 | Depth is computed by program from a fixed node table (percent-off 1, scale a/b 1, month add 1, weekday derivation 0, comparison 0, band-part width 1 unless lo = 0, ...); per-sampler hand labels are dropped | 1.1, S3 |
| A30 | meta.depth = unstated operations. Non-deep rows: at most 2 total operations, or 3-5 with every intermediate printed (depth 1, "stated_intermediate", "ops:<n>"). Section 6 depth groups are disjoint | 1.1, 6 |
| A31 | [v3: strip rule, R1-14 and R1-26; v4: arithmetic steps only, R2-06] What is printed: every day count a later arithmetic step uses (as a number); never the resulting deadline, and never a day offset that only a comparison or window lookup reads. Long or month-crossing windows get an unmarked calendar strip (aid, not an intermediate). The N <= 10, <= 1 holiday business-day rule wins over the 14-day rule | 1.1 |
| A32 | [v3: two counts, R1-10 and SC6] Negation count = cues in the question outside the fixed CMP1-CMP3 comparator phrases; comparator phrases with negation words count 0 and are tagged "negcmp". [v4: XF02; v5: SC13, SC14] Used by A's and B's polarity logic, `edge` "neg:<n>" and the neg / dneg twin labels only (no G10 check, selection cell or G6 / G7 feature); the 2.1 quotas use k_syn ("syn:") and the G10 cells use k_all ("cue:"), both read directly from the shared negcount [v5: R3-01: questions carry CMP1-CMP3 only, so no other comparator phrase needs exclusion] | 3.8 |
| A33 | [v3: per template and role side, R1-30; v4: fixed table, R2-20] Every question template has a polarity tag ("bad_yes" / "good_yes") from the fixed 3.8 table, per affirmative proposition and the decider's role side, swapped by each inverting cue; templates without an entry for their side are not used | 3.8, 6 |
| A34 | MR7 applies only where A confirms monotonicity in that input (no input-gated exception, no subtraction of it, no falling-rate flat table), is tested on the compared value, and its flip direction comes from comparator and polarity | S1, S3, S5 |
| A35 | MR4 reorders only position-independent clauses; every position reference is replaced by rule numbers or IDs that move with their rules | 2.2 T1, X3, X10, S1, S3 |
| A36 | The parser classifies every line (structure, container boilerplate, unparsed) and reports unparsed lines; G3 asserts none on clean rows and exactly the inserted line(s) on attacked twins | 3.3 |
| A37 | A keeps Decimal (C_DATA_SPEC) with an Inexact trap: any decision downstream of an inexact value needs a margin > 10^-20 or the structure is rejected; B is exact | 3.1 |
| A38 | B holds every number literal as an exact reduced fraction parsed from its decimal text; there is no input grid | 3.2 |
| A39 | z3: NEI iff >= 2 distinct option-level labels (including "no option") are satisfiable over the A01 domain; determined iff exactly one | 3.2, 3.5 |
| A40 | S2 "cap or floor decides": the adjustment equals R and the unadjusted value is drawn on the other side of T (floor or cap chosen by the comparator direction and the label), so the label differs without it; works for delta -1, 0, +1 | S2 |
| A41 | S2 draws the comparator family conditional on delta, label and negation so that P(yes given inclusive) and P(yes given exclusive) are each 50 +/- 2 per sampler (builder asserts), with inclusive 50 +/- 2 at delta 0 | S2, 6 |
| A42 | S4 draws the label first from the card's yes rate through the question kind, then places the act: on time on the last allowed day 60% / 1-3 days early 40%; late on the first late day 60% / 2-4 days after 40% | S4 |
| A43 | S1 far rows: the side of T comes from the drawn label; structures with R < 8 resolution units are resampled; the no-rounding naive target applies only to rows where rounding can reach T (S1 far rows exempt) | S1, 6 |
| A44 | [v3: has / bind / dec tags, R1-24; v4: per schema, R2-18] "Binds" (value changes) is used on CH-V, CH-D and CH-C rows and "decisive" (label changes) on YN-T, YN-D, CH-B, CH-O and CL rows, stated once in section 6 | S1, S4, 6 |
| A45 | Per-dimension target: on rows where the dimension is decisive, its alternatives are uniform +/- 5 pp over the 2-4 alternatives the sampler uses; B2 is exempt at 30 / 70 +/- 3 (depth cap) | 6, S3 |
| A46 | Each B1 form is used on 50 +/- 5% of band tables and of on-edge rows; G7 tests "an option equals the amount" | 2.2 B1, S3, 6 |
| A47 | [v3: per card variant, R1-20] Card text is fixed per card: shown clauses appear on every row of the card; the OR1 tag and T1 always appear with their clause; one-line style = all relevant clauses; short cards keep each optional dimension with p = 0.5 per card, except that a dimension planned for a flip variant is always shown [v4: R2-14] | 2.1, 3.7 |
| A48 | Each base row joins at most one relation unit; own-call_id twins point to it. Selection keeps or drops a base row with all its units and twins | 3.6 |
| A49 | [v4: rewritten to SC4b, R1-20 and XF09] card_id = C_DATA_SPEC's tuple (F2, sampler, pack, schema, instruction family); the rule set (formula type + SEM vector + world) is a card property. One F2 card per pack (no two F2 cards share a pack); clause-flip twins sit in flip variants of their base row's own card | 3.7 |
| A50 | [v3: per card variant, R1-20] Worked examples are generated per card under that card's own SEM vector and world, so a twin's card has matching examples; example structure hashes enter G12 and G13 | 3.7 |
| A51 | When R1 is absent, A asserts that every final, displayed or compared value is exactly representable at display precision; otherwise the row is resampled (a structure that needs rounding goes on a card that shows R1). [v6: R3-13] On every row, R1 shown or not, the final value, the asked target node, every option and hook value and the value the question reads are on the display grid under the card's own steps; nothing is rounded for display; otherwise resample | 2.2 R7, 3.1 |
| A52 | The closed edge vocabulary adds mech, cmp, pol, neg, negcmp, world, money, b1, cliff, tie, named, short_card, ops, aid, abst, so QC computes every section 6 target from meta and edge | 3.8 |
| A53 | [v4: rewritten to SC3 and R2-17] Abstain options are not hooks; bucket k counts every shown option; gold-rank uniformity is over ordered options (values, dates, bands and outcomes). A value that two or more hooks give is not shown; each shown distractor has exactly one hook id | 3.4 |
| A54 | The lexicon uses longest-match, context-specific entries ("up to but not including" before "up to"; [v5: R3-09, R3-10] D4a's "no later than <N> calendar days after <event>", D6b's "... business days after <event>" and D4b's "on or before the <N>th calendar day, counting the day of <event> as day 1" separate from D2's phrases; "fails to reach" before the cue "fail to"; [v5: R3-01] question-side entries CMP1-CMP3, OP, TF and N1 only; [v6: R3-22] "up to <X>", "a maximum of <X>" and "a minimum of <X>" are card-rule entries only); the G0 reviewer checks them | 2.2 (parser lexicon rule), 3.3 |
| A55 | [v3: printed day counts allowed in sweep items, R1-15] Sweep chance = the mean of 1/k over the level's items; sweep items have no stated intermediates, so depth = total operations | 5 |
| A56 | The 2,500-row sampler cap counts selected training rows over both rounds only, not candidates or the QC sample | 1.2 |
| A57 | Every row is measured with the real tokenizer and resampled at >= 1,900 tokens; large case lists use <= 4 attributes and <= 25 tokens per case; cards with examples <= 450 tokens [v7: CP1: measured on the rendered prompt, `instructions` and options counted twice; choice cards with fragment examples <= 350 and few-shot choice cards <= 500; case values in `state`] | 3.7 |
| A58 | New U5: deduction lines are positive amounts that are subtracted (no minus signs or parentheses). S5 settlement uses calendar days, always written "calendar days", with D7 (and D6a, never D6b; [v5: R3-08, R3-09]), so the roll rule matters [v7: R4-09: the settlement clause is D17] | 2.2 U5, S5 |
| A59 | [v3: twin rows only, R1-28; v4: XF03] The 20-25% share counts label-flip twin sets only (base + boundary, clause_flip, premise_removed); neg / dneg units count only toward the negation quotas; attack twin rows (about 5%) and inert twin rows (<= 5%) are counted separately | 3.6, 6 |

### 10.2 Spec conflicts C01-C20 (settled in favour of C_DATA_SPEC v4)

| ID | Conflict (short) | Resolution | Where |
|---|---|---|---|
| C01 | G0 "every label-flipping choice in the card" vs short / no-card rows with clauses in the document | F2 has no no-card rows; short cards (about 15% of rows) carry every decisive clause; v1's 10 open questions are closed | 2.1, 3.7, 8 |
| C02 | Masked / swapped quotas over all choice rows vs F2 applying them to band and outcome rows only | Quotas apply to all F2 choice rows. Named-outcome rows are defined (S1, S2, S4); named-option rows are about 30% of choice rows, masked on about 40% and swapped on about 17% of them (10-15% and about 5% of all choice rows) | 3.7, 6 |
| C03 | "Each wrong option from one named error" vs natural closed sets on 10-60-option rows | Every wrong option on every choice row comes from one named error. Calendar grids and full band lists are dropped as option lists; large buckets come from hook-rich rows and case lists | 3.4, S3, S4 |
| C04 | "State day counts when the card's rule needs them" vs unstated short day counts | [v4: R2-06] Every day count that a later arithmetic step uses is printed; only an asked count is unprinted (it is the answer); offsets are not day counts, and a day offset that only a comparison or window lookup reads is not printed | 1.1 |
| C05 | Depth: "each intermediate stated" vs "every intermediate beyond the second" | C_DATA_SPEC's strict reading: rows with 3 or more operations print every intermediate | 1.1 |
| C06 | Twin share: label-flip twins vs F2 counting neg/dneg, inert and attack together | Label-flip sets (base + boundary, clause_flip, premise_removed) count toward 20-25%; [v4: XF03] neg / dneg units count only toward the negation quotas; attack about 5% and inert twins counted separately | 3.6, 6 |
| C07 | Per-card yes rate 20-80% vs S1 "sign balanced" and S4 30/35/35 placement | Labels are drawn first from the card's yes rate (S1, S4); S4 placement is symmetric around the boundary; each S4 question kind is 50 +/- 2 | S1, S4, 6 |
| C08 | G6/G7 vs the comparator-family cue in S2 and the B1 edge cue in S3 | S2 comparator drawn conditional on the label (P(yes given family) 50 +/- 2); B1 forms split 50/50 on tables and on-edge rows | S2, S3, 6 |
| C09 | Presence rule (c) / G7 vs one-line "decisive only", OR1 tag only when both hold, T1 only on ties | Card text is fixed per card; the OR1 tag and T1 always appear with their clause; G7 tests clause presence | 2.1, 2.2 |
| C10 | Section 6 internal inconsistencies (B2 30%, binds vs decisive) | Binds / decisive defined once; per-dimension uniform rule; B2 exempt at 30/70 | 6 |
| C11 | Abstain shown on about 15% vs NEI on every open-world row | [v4: rewritten to SC2 and XF01] Open-world cards cut to about 13% and made choice-only; NEI shown on every open-world row; "none" on about 10% of closed-world choice rows; an abstain option only on rows with k >= 3; on each row it is gold with probability 1/k (NEI about 20% of open-world rows, "none" about 15-20%), so both are wrong on >= 50% of rows that show them; F2 abstain gold about 7% of choice rows; [v5: SC12] G10 checks 1/k +/- 2 pp per k bucket and per abstain option | 3.5, 6 |
| C12 | "Two cards differ in pack and in schema or rule set" read pairwise vs >= 40 packs for >= 80 cards | [v4: rewritten to SC4b and XF09] The literal pairwise reading is adopted: one F2 card per pack (80 / 150 distinct training packs), and no two F2 cards share (schema, rule set); no orchestrator action needed | 3.7, 9 |
| C13 | Row-level stratified selection vs relation-unit integrity | [v3: refined by SC1] Strata at row level from the base row's cell; sampling keeps or drops whole twin sets; G10 re-checked after | 3.6 |
| C14 | 2.4 "ordinal row" definition literally covers F2 bands | F2 band and named-outcome rows are not ordinal, by C_DATA_SPEC's own F8-bins rule (A4's sized row set); no level numbers in options; builder asserts no option_level; orchestrator to list F2 next to F8 | 1, 3.1, 9 |
| C15 | G14 order rule vs concrete canonical clauses and question frames | Quoted clauses are meaning statements, not a pool; they pass 7.2 #8 and the sealed template comparison before any surface use; N1 and Q1 question frames are removed | header, 2.2 N1, Q1 |
| C16 | Licence: O*NET persona seeds vs "no third-party text" in register section 3 | Packs declare O*NET as a 3.H parent (`no_new_rows` passes for persona seeds); O*NET is credited in the notices file; the register note is an orchestrator item | 1, 9 |
| C17 | G13 method 6 needs a hash scheme shared with the sealed agent | [v3: path in SC4c] F2 hashes the canonical problem as 7.2 #6 defines it; the shared part-P scheme is an orchestrator item; until then part P is "not checkable" and F2 cannot pass G13 | 3.8, 7, 9 |
| C18 | MR4 vs position-dependent clauses (T1, X3, band below) and the option shuffle | All position references replaced by IDs, rule numbers or band edges; MR4 reorders only position-independent clauses | 2.2 T1, X3, X10, S1, S3 |
| C19 | B's closed-form business-day count vs A's loop when a holiday falls on a weekend | Weekend holidays are never generated; A and B assert | 2.2 D6, 3.2 |
| C20 | Owner rules (no model above 4B, no Jev path, no paid calls, z3 and Hypothesis as named, no sealed or OHS input) | No conflict; unchanged | header, 7 |

---

## 11. One-page spec per generator (G0 format; SC7)

C_DATA_SPEC G0 asks for a 1-page spec per generator with a semantics table. Each page below is that summary; the
sections it cites hold the full rules. Every row of every semantics table is a SEM id of 2.2, so solver A, solver B,
the parser and the G0 reviewer read one meaning. Shared by all five: W0 on every card; one governing rule per <B>
(2.1); CMP1-CMP4 for every comparison in card rules, and only CMP1-CMP3 or an OP predicate in a question (T2 has no
separate tie rule; Q1); negation cues only in yes/no questions, inside a truth-frame complement, from N1's closed list
(N1, 3.8; XF10); U1 built-ins only (Gregorian calendar, 24 h,
60 min), every other conversion stated; U4 number and date formats; R7 display precision (final value, target node,
options, hooks and the value the question reads on the grid on every row; nothing rounded for display; R3-13); T1 keys
are fixed-width ID numbers or dates (R3-18); abstain gold with
probability 1/k (A1); every distractor from exactly one named error (3.4); depth from the 1.1 node table; every SEM
sentence in the card, values only in the document (2.1, R2-12); every comparison after rounding reads the rounded
value (R3, R2-02); gold rank uniform over ordered options (3.4, R2-17); unknowns only as "not recorded", absent values
left out, null and "unknown" never rendered (2.1, R3-11); inert lines inert by entity, period, line type or row ID
(3.6, R3-12); card placement CP1 (yes/no rows: the `card` field; choice rows: no option-definition line, the card text
in `instructions`, document values and CL case values in `state`; fmt1 loader_check on every row; lengths on the
rendered prompt, `instructions` counted twice).

### 11.1 S1: forward formula graphs (training; 800 / 1,600 rows; 21 / 40 cards)
- **Draws.** 2-6 inputs and one formula type (per-unit charge with partial units; percent-of a named base; single
  discount; min(cap, rate x quantity); max(minimum, p% x amount); gross - deductions floored at 0; successive or added
  discounts; per-k pricing; fee on a listed price), 0-2 exceptions, 0-3 inert facts. Row groups of 1.1.
- **Schemas.** YN-T (45% of S1 rows; T far, log-uniform), CH-V, CH-O, CL. Open-world cards: CH-V and CH-O only.
- **Gold / checks.** A: Decimal graph under the card's SEM vector. B: integer fractions on the parsed text. G4: MR1,
  MR2, MR3, MR4, MR6, MR7 (monotone inputs only), MR8, MR9, MR12, MR13.

| Dimension | SEM ids | How S1 uses it |
|---|---|---|
| Open or closed world | W0, W1, W3 / W2; M3 (closed-world amount column only), M4 in table containers | closed on most cards; open cards choice-only, one "not recorded" field read by a rule (an amount, count, date, listed category or yes/no fact; R2-07, R2-08); no world twins |
| "unless" | UN1 | exception gates; R applies exactly when C is false |
| "only if" | O1 (and), O3 (or, either or both); O2 plain "if" | exception and charge gates; biconditional; never mixed and/or |
| "at least" and other comparators | CMP1-CMP4 | YN-T thresholds; exception gates on amounts |
| Inclusive or exclusive "or" | OR1 (tag always shown), OR2 | inside one gate rule |
| Date ranges | D1, D3; D10 with D13 when a rate changes | rare: only when a rate changes on a date |
| Rounding | R1 mode, R2 stage (per line in R1's mode), R3 every later comparison reads the rounded value, R4 no hidden rounding, R5 partial units per line (not U3 quantities; R4-04) | R2-R4 only with R1; when R1 is not shown every row is exact |
| Ties | T1 | every card with a best-option rule; X3 ties go to the lower rule number |
| Units | U1, U2, U3, U5 | stated conversions and exchange rates only; per-k pricing is U3's own partial rule |
| Exception precedence | X1 order, X2 replace / add, X3 each alone or all in order (fold on the current value; all-in-order cards have exceptions of one kind, R2-05), X4 cap / floor scope and order, X5, X6 base, X7 gross / net (back-out formula), X8 floor at 0 (final amount only, R4-08), X9 waiver, R8 discount | every exception and adjustment named; no position references |

### 11.2 S2: target-first boundary placement (training; 850 / 1,700 rows; 21 / 40 cards)
- **Draws.** Label first (card yes rate p 20-80% on the affirmative proposition, 3.7); delta in {-1, 0, +1} (P(0) = 0.30); comparator family conditional on
  delta, label and negation; one decisive mechanism (rounding, cap or floor, exception, partial unit, plain, about
  20% each); back-solve one input so the forward result is exactly R = T + delta x unit.
- **Schemas.** YN-T (70%; all S2 neg / dneg units), CH-V (near-miss options), CH-O. Closed-world cards only.
- **Gold / checks.** A forward-verifies the back-solved structure; B re-solves the parsed text. G4: MR1, MR2, MR7, MR8,
  MR9, MR10 boundary twin, MR11 clause-flip twin, MR13. Main source of clause-flip twins (flip variants, 3.6).

| Dimension | SEM ids | How S2 uses it |
|---|---|---|
| Open or closed world | W0, W1, W3 | closed only; no abstain except "None of the listed" on some CH-V rows |
| "unless" | UN1 | exception-decides mechanism |
| "only if" | O1, O3; O2 | exception gates |
| "at least" and other comparators | CMP1-CMP4 | the decisive comparison; inclusive 50 +/- 3, P(yes given family) 50 +/- 2 |
| Inclusive or exclusive "or" | OR1, OR2 | exception gates |
| Date ranges | D1, D2, D3 | only when the decisive quantity is a day count or a date |
| Rounding | R1-R5 | rounding-decides mechanism; R3 always with a threshold when R1 is shown |
| Ties | T1 | when a best-option rule appears |
| Units | U1, U2, U3, U5 | the resolution unit (cent, whole unit, day, item) comes from the pack |
| Exception precedence | X1-X9, R8 | cap or floor decides with the adjustment value equal to R |

### 11.3 S3: tiered rate tables (training; 750 / 1,500 rows; 19 / 35 cards)
- **Draws.** A band table with 3-8 bands (10-19 on <= 10% of rows), one B1 form per table with shared edges (R3-06;
  upper-inclusive on marginal tables over counts, R3-05), B2 mode (marginal 30%; the marginal clause states the measure;
  flat-fee rates on flat tables only, R3-20),
  optional minimum and maximum (X4), optional X10 category exception (flat only), optional second dated table (D10 +
  D13). On band-choice rows (CH-B; CL "which case falls in <band>") the banding amount is always computed (>= 1
  unstated operation); other rows may band a stated amount (R2-15). Document tables give edges as plain numbers; the
  B1 form and B2 mode are card sentences (R2-12).
- **Schemas.** CH-B, CH-V (total charge), YN-T (40%; T near on half, far on half), CL. Open-world cards: CH-B, CH-V.
- **Gold / checks.** A walks bands one by one; B uses the cumulative closed form. G4: MR1, MR2, MR3, MR4 (band rows
  shuffled), MR6, MR7 (monotone tables only), MR9, MR11, MR13.

| Dimension | SEM ids | How S3 uses it |
|---|---|---|
| Open or closed world | W0, W1, W3 / W2; M3, M4 | blank amount cells follow M3 (closed world only); computed cells follow M4; blank edge cells are B1's "no edge", never M3's (R3-07) |
| "unless" | UN1 | category exceptions |
| "only if" | O1, O3; O2 | category exceptions |
| "at least" and other comparators | CMP1-CMP4; B1 edges; B4 part above a threshold | band edges are read only through the card's B1 sentence, never bare comparators; edges in the document are plain numbers |
| Inclusive or exclusive "or" | OR1, OR2 | exception gates |
| Date ranges | D1, D10, D13 | the second table's governing date; boundary sentence always shown |
| Rounding | R1-R4 | per-band (R2 "each line", in R1's mode) or final rounding; a band lookup after rounding reads the rounded amount (R3) |
| Ties | T1 | when a best-option rule appears |
| Units | U1, U2, U3 | per-unit and per-k band rates; U3 per line, band edges that split a U3 quantity are multiples of k (R4-04) |
| Exception precedence | B2 mode, B3 banding variable, X10 next-lower band (flat only), X2, X3, X4 min / max scope and order, X6 | X10 refers to band edges, never to row position |

### 11.4 S4: calendar and business-day rules (training; 750 / 1,500 rows; 19 / 35 cards)
- **Draws.** Years 2031-2049; anchor with stated weekday; an offset rule (D4a calendar days, or D4b on a flip variant;
  D6a + D6b business days, with D7;
  or D8 months forward with clamp then roll, D8 always shown; the last allowed day on or after the event day, R4-11), at most one extension rule (D12; R3-24), 0-3 listed weekday
  holidays on the one holiday line ("none" when 0; R3-23) (non-deep rows: N <=
  10 and <= 1 holiday inside a business-day window); day and business-day counts (D5, D14); proration with printed
  days used (P1); effective-date splits (D10) and one-off charges (D13). Calendar strip whenever D6a is shown or a
  window is long. D4, D16 and D12 always say "calendar days" or "business days" (R3-09).
- **Schemas.** YN-D (50%; on time or late, "cmp:date"), CH-D (last allowed day), CH-C (counts), CH-O (date windows),
  CL ("which act missed its deadline"). Open-world cards: CH-D, CH-C, CH-O.
- **Gold / checks.** A iterates days; B uses day ordinals and the closed form. G4: MR1, MR2, MR3, MR5 (+28 years; year
  window shifts), MR8, MR9, MR10, MR11, MR12, MR13.

| Dimension | SEM ids | How S4 uses it |
|---|---|---|
| Open or closed world | W0, W1, W3 / W2 | open cards: one unknown field read by a rule; explicit date bounds only |
| "unless" | UN1 | extension conditions |
| "only if" | O1, O3; O2 | extension conditions |
| "at least" and other comparators | D2 forms, D15 on time (inclusive), CMP1-CMP4 for counts, B1 forms read on dates for windows | on-time and late rows are exempt from comparator targets |
| Inclusive or exclusive "or" | OR1, OR2 | extension conditions |
| Date ranges | D1, D3, D4 (D4a / D4b), D5, D6a, D6b, D10, D13, D14, D16 | every range states both-ends or up-to-but-not-including; CH-O windows have D16 edges (last allowed day + k calendar days) in one B1 form per table with shared edges, found from dates, no printed days-late count (R2-06, R3-06, R3-09); D6b only when the deadline adds business days (R3-08) |
| Rounding | R1-R4 (proration only), P1 | 30-day spans inside one month with no month-end day |
| Ties | T1 | earliest-date or ID tie-breaks when a best-option rule appears |
| Units | U1 (calendar built-ins), D9 weekdays stated | no outside holidays or weekdays |
| Exception precedence | D7 roll, D8 clamp then one roll, D12 extension before the roll, X2, X3 | the roll rule applies once, at the end |

### 11.5 S5: line-item statements (held out; mix-tuning dev only: 400 items + 12 per sweep level)
- **Draws.** A statement (description | quantity | rate | amount); amounts printed, marked computed (M4: the line's
  pricing, quantity x rate or B4's split, before rounding and caps; R2-04), or blank on lines with no quantity and no
  rate (M3, closed: nothing charged; their quantity and rate cells read "none", SC19). Rules: B4 multiplier above a threshold (scope named; one line per scope wider
  than a line; R3-19), an allowance with a cap (X4; only scope totals asked under a multi-line scope, R3-19), a percentage deduction with a floor or cap, R2 stage, a settlement date by D17 (period end + N
  calendar days, always written "calendar days", the period end not counted, then the roll) with D7 and D6a, never D6b
  (R3-08, R3-09, R4-09).
- **Schemas.** YN-T (50%; yes 50%; T near on half, far on half), CH-V, CH-D. Closed-world only. Held-out packs and
  styles; structure hashes disjoint from training; the statement container is never used by S1-S4.
- **Gold / checks.** Same A, B, parser (statement container) and SEM table. G4: MR1, MR2, MR3, MR4 (line reorder),
  MR5, MR6, MR7, MR9, MR13.

| Dimension | SEM ids | How S5 uses it |
|---|---|---|
| Open or closed world | W0, W1, W3; M3 closed form; M4 | closed only |
| "unless" | UN1 | allowance and deduction conditions |
| "only if" | O1, O3; O2 | allowance conditions |
| "at least" and other comparators | CMP1-CMP4; B4 (never a comparator) | YN-T thresholds |
| Inclusive or exclusive "or" | OR1, OR2 | allowance conditions |
| Date ranges | D1, D2, D3, D6a, D7, D17 | settlement date (D17: calendar days, the period end not counted) with a roll |
| Rounding | R1-R4 | per-line vs total rounding is the main switch; per-line rounding uses R1's mode (R2-01) |
| Ties | T1 | when a best-option rule appears |
| Units | U1, U2, U5 | deductions positive and subtracted |
| Exception precedence | X1, X2, X3, X4 (cap scope and order), X6, X8 | as S1 |

---

## 12. Resolved ambiguities (re-review round 1: R1-01 to R1-30, SC1-SC7)

Each row states the one semantics F2 now uses, in card terms where it is a card clause. Section 12 governs over
section 10 where they differ.

### 12.1 Ambiguities R1-01 to R1-30

| ID | Resolution (one semantics) | Where |
|---|---|---|
| R1-01 | M3 blank amounts appear only on a line with no quantity and no rate; closed world [v5: R3-07: closed world only, and the clause names the amount column]: "A blank cell in the <amount> column means nothing was charged on that line." A line with a quantity and a rate is never blank: its amount is printed or carries the new M4 marker, whose meaning is fixed in 2.2 M4 [v4: R2-04: the line's pricing (quantity x rate, 1 multiply node, or the card's B4, partial-unit or per-k rule for that line), before any rounding, cap or minimum, which then apply to it] (misreading it as 0 is E-blank). S5 is closed-world only. A asserts; the parser rejects a blank amount on a line with a quantity or a rate [v7: SC19: such a line's quantity and rate cells read "none"] | 2.2 M3, M4; 3.1; 3.3; 3.4; S5; 11.5 |
| R1-02 | X7 include form: "Listed prices include <fee>. The price before <fee> is the listed price x 100 / (100 + <p>), and the <fee> is the listed price minus the price before <fee>." (1 scale + 1 subtract node). X6 can name the base "the price before <fee>". R1 is shown and applies whenever a backed-out value is inexact (R7); A's exactness guard covers the division. Taking p% of the listed price is E-gross | 1.1 node table; 2.2 X6, X7 |
| R1-03 | X3 "apply all" form: "... apply all of them in rule-number order; each one acts on the <rate or charge> left by the ones before it, so a later replacing rule replaces the rate an earlier one set." A replace sets the current rate (the last applicable replace wins); an add adds to the current charge. [v4: R2-05] A card with this form has exceptions of one kind only (all replace or all add); mixed cards use the "each alone" form | 2.2 X2, X3 |
| R1-04 | Each <B> (outcome, exception or charge) is governed by exactly one connective rule (UN1, O1, O2 or O3); several conditions are joined inside that rule. "Only if" and "if" / "unless" never govern the same <B>. A asserts; the parser rejects a second governing rule | 2.1; 2.2 O2; 3.1; 3.3 |
| R1-05 | On open-world cards W2 now says "every other fact the rules use is given or shown as \"not recorded\"": every case field a rule reads (categories, numeric attributes, dates, yes/no facts) is printed or "not recorded", exactly one is "not recorded". A asserts (mirror of A06) | 2.2 W2; 3.1; 3.5 |
| R1-06 | The admissible domain uses explicit bound sentences only (a stated range, or a stated order between dates), which the parser extracts. An unknown field never has an implied bound: never a part of a stated total, never a sub-span of a stated span, no sequencing words next to an event whose date is unknown. W2 [v7: R4-10]: "an unknown date any calendar date, except where a sentence of the record bounds that date"; A also checks that the status and label do not change under natural precedences. A asserts; A's witnesses and z3 satisfy every explicit bound | 2.2 W2; 3.1; 3.2; 3.3; 3.5 |
| R1-07 | Whenever D13 is shown, D10's boundary sentence for that change is shown too, as "never": "The new <rate> applies to <days or dates> on or after <D>; earlier <days or dates> use the old <rate>." (or its T form). On about 30% of D13 rows the governing date equals the change date, so the boundary form is decisive there | 2.2 D10, D13; S4; 11.3 |
| R1-08 | Under the 30-day basis (and on every base row with a P1 clause-flip twin) the prorated span lies inside one calendar month and contains no month-end day, so never day 31: printed days used <= 29 and the result is below the full amount. A asserts | 2.2 P1; 3.1; 11.4 |
| R1-09 | U3 is the only partial-unit rule for its quantity: pro rata = price x quantity / k with the quantity as stated; as a full k = price x (quantity / k rounded up). R5 is never shown for, or applied to, a U3 quantity. A asserts [v6: R3-21: when U3 is omitted, the filter also tests complete blocks only, price x (quantity / k rounded down); it is never a card form] | 2.2 U3, R5; 3.1 |
| R1-10 | New OP list of outcome predicates (on time, late, met its deadline, missed its deadline, due, owed, charged, falls in <band or outcome>): each is the proposition itself (inverting count 0). No outcome predicate uses a C_DATA_SPEC F5 cue word [v5: R3-03, R3-04: the only F5 implicit cue in an F2 question is "fail to" in "fail to meet <its> deadline"; charged / owed = the named amount > 0 (card clause); due = a rule makes it due, with the amount > 0 exactly then on every "due" row]. The lexicon keeps OP and N1 entries apart by longest match; A, B and the parser share the list | 2.2 N1, OP, parser lexicon rule; 3.8 |
| R1-11 | On case-list rows depth = the maximum over cases of the per-case depth; each case obeys the 3-selection-step cap on its own; [v4: R2-21] every case falls in the same 1.1 row group, and the row counts in it; `edge` "cases:<n>" | 1.1; 3.8; 6 |
| R1-12 | Every row has at least 1 unstated operation. S3 band-choice rows (CH-B; CL "falls in <band>") always compute the banding amount [v4: R2-15]; S4 deadlines always come from an offset rule (D4, D6b [v5: R3-08], D8, with optional D12); a fixed D2 date is never itself the deadline | 1.1; 3.1; S3; S4; 6 |
| R1-13 | Option (b): non-deep S4 rows have N <= 10 and at most 1 listed holiday inside any business-day addition window (up to 3 holidays may be listed, the others outside it). The 2-operation addition (N > 10 or >= 2 holidays inside) appears only in deep and sweep items | 1.1 node table; 3.1; S4 |
| R1-14 | Whenever D6a is shown (business days used, or D7 appears; [v5: R3-08]), the text shows a calendar strip covering every candidate date, so the weekday of a computed date is always stated and the weekday node stays 0. D9 states anchor and holiday weekdays as before | 1.1 (strip rule, node table); 2.2 D9; S4 |
| R1-15 | Printed day counts are stated inputs: they count in neither `meta.depth` nor any row group's total operations. Sweep items may print day counts (not intermediate results), so sweep depth = unstated operations = total operations, and S4 sweep items with proration or sub-spans are valid | 1.1; 5; 6 |
| R1-16 | Alt-labels recompute every unstated node and hold every printed number fixed (inputs, intermediates, day counts, strip weekdays). A dimension fully absorbed by printed numbers is not decisive and may be omitted from a short card. Clause-flip twins are made only where the flip changes no printed number, so the twin's label equals the base's alt-label (MR11 checks it) | 2.1; 3.1; 3.6 |
| R1-17 | Every "Shown when" condition is evaluated per card, over the card's formula type and the value ranges its sampler can draw ("can it matter for any admissible row of this card?"); full cards show the clause exactly then. Row-level facts only drive row admission | 2.1; 2.2 (column note, R1, R2, R5) |
| R1-18 | "R1 absent" = R1 not shown on the card (not relevant, or dropped from a short card). R2, R3 and R4 are shown only together with R1; a short card that drops R1 drops them too, and A asserts every row on it is exact at display precision (R7) [v6: R3-13: on every row, R1 shown or not, the final value, target node, options, hooks and the value the question reads are on the grid; nothing is rounded for display] | 2.1; 2.2 R1-R4, R7; 3.1 |
| R1-19 | F2 label schemas, one per card: YN-T, YN-D, CH-V, CH-D, CH-C, CH-B, CH-O, CL. Per-card yes rates exist on YN cards only. Open-world cards use CH-V, CH-D, CH-C, CH-B or CH-O; CL (case lists), YN-T and YN-D cards are closed-world, so NEI never meets "exactly one or none qualifies" | 1; 3.4; 3.5; 3.7 |
| R1-20 | Clause-flip twins sit in pre-planned flip variants of the base row's own card (same card_id, pack, schema, instruction family, world, formula type, wordings; one SEM switch apart; at most 2 per card). Variants count inside their card (80 / 150 cards, one card per pack, 128-row cap). A flip variant also carries its own base rows, so it never marks twins. `edge` "var:<k>", k = 0 (base variant), 1 or 2. A dimension is flipped only where a variant is planned | 2.1; 3.6; 3.7; 3.8 |
| R1-21 | A choice-row clause-flip twin keeps the base's option list. It is made only when the alt-label is a shown non-abstain option other than the base's gold; A builds the base's options so that every option is gold or an eligible named-error value under both vectors, and the base's gold is logged as E-alt:<ID> in the twin. Otherwise no clause-flip twin | 3.4; 3.6 |
| R1-22 | S3 and S5 threshold yes/no rows: label drawn first; on 50% T is near (delta in {-1, 0, +1} drawn as S2 step 2, comparator drawn as S2 step 3), on 50% far (abs(R - T) log-uniform in [2 units, 0.5 R], R < 8 units resampled, comparator drawn as S2 step 3) | S3; S5; 6; 11.3; 11.5 |
| R1-23 | S4 on-time and late rows carry `edge` "cmp:date" (D15 is always inclusive) and are exempt from the comparator targets (inclusive share, P(yes given family), at-boundary inclusive share); they count in the boundary-zone target through their within-1-day placements | 3.8; S4; 6 |
| R1-24 | New tags: "has:<x>" ([v4: R2-12] the card states rule x, whose values may sit in the document; for holidays, the card or document lists one), "bind:<x>" (it changes the value), "dec:<x>" (it changes the label). "has:<x>" is the single denominator of every adjustment target; the decisive target and the naive-solver target are one check; [v4: R2-18] "bind:" targets apply on CH-V, CH-D, CH-C rows and "dec:" targets on YN-T, YN-D, CH-B, CH-O, CL rows | 3.1; 3.8; S1; S4; 6 |
| R1-25 | A's year-window check uses the row's own stated year range: 2031-2049 for every F2 sampler (all stated dates lie there), shifted with the row under MR5 (2059-2077) | 3.5; S4 |
| R1-26 | The resulting date is "never stated as the result"; it may appear unmarked in a strip. The strip spans the earliest to the latest relevant date (anchor except on D8 rows, acts, options, holidays, gold, every named-error date and [v4: R2-06] every S4 window edge date) with independent 3-10-day margins on both sides, at most 45 dates (local strip without the anchor if longer, else resample). D8 offsets get a strip only when D7 applies | 1.1 |
| R1-27 | Every unknown field is read by at least one rule. Needed rows: on a live decision path. Inert rows: read by a rule but off every path because another condition fails for every admissible value. So "the unknown field is named in a rule" holds on every open-world row and predicts nothing; G6 / G7 add "number of rules that read the unknown field" | 3.1; 3.5; 6 |
| R1-28 | Attack and inert shares count only the twin rows, never their bases: attacked twin rows about 5% of F2 rows (C_DATA_SPEC 2.1), inert twin rows <= 5% | 3.6; 6 |
| R1-29 | Definition-style examples illustrate one clause on a fragment (no document, no question). Few-shot cards (a separate instruction family, 5-10% of cards) contain 1-3 complete short solved rows (<= 200 tokens each; card <= 700 tokens [v7: CP1: <= 500 tokens with 1-2 example rows on choice cards]) and no fragment examples, so the two never overlap | 3.7 |
| R1-30 | The polarity tag is set per (template, role side). Templates are written against an abstract side ("the party that pays" / "the party that is paid"; for dates "the party that must act" / "the party that waits"); each pack maps its decider to a side; the tag is logged per row as "pol:<tag>". [v4: R2-20] The tag comes from the fixed 3.8 table per affirmative proposition and side, swapped by each inverting cue | 3.8; 6 |

### 12.2 Spec conflicts SC1-SC7 (settled in favour of C_DATA_SPEC v4)

| ID | Conflict (short) | Resolution | Where |
|---|---|---|---|
| SC1 | C_DATA_SPEC "keep all medium and hard rows and 30% of easy rows, then downsample in cells" vs F2 selecting whole twin sets by the base row's cell | A selection unit (base + relation unit + own-call_id twins) takes its hardest member's bin. Every unit with a medium or hard member is kept whole, so every medium and hard row is kept; all-easy units are drawn so kept easy rows (ride-along easy twins included) are 30% of generated easy rows; then downsampling in row-level cells drops whole units only; G10 and difficulty re-checked after. The only deviation (easy ride-alongs above 30%) is logged and sent to the orchestrator | 3.6; 6; 9 item 5 |
| SC2 | NEI gold 35% and "none" gold 40% vs G6 chance + 2 pp and G7 p0 = 1/k | The abstain option is gold with probability 1/k on every row that shows it (k = shown options, abstain included). G6 chance for choice rows = mean 1/k per bucket. Expected NEI gold about 20% of open-world rows, "none" about 15-20%, F2 abstain gold about 7% of choice rows; [v4: XF01] an abstain option is shown only at k >= 3, so F6's >= 50%-wrong rule holds with margin (1 - 1/k >= 2/3) | 2.2 A1; 3.5; 6; 8 item 10 |
| SC3 | "Each distractor from one named error" vs NEI rows compounding hooks on completions and merged equal hooks | A display value is a distractor only when exactly one hook gives it; values two hooks give are not shown. NEI-gold rows use E-assume values only (one admissible completion each, nothing compounded) | 3.1; 3.4 |
| SC4a | C_DATA_SPEC 2.4's ordinal definition vs F2 band and named-outcome rows | F2 follows C_DATA_SPEC's enumerated ordinal list and the A4 sizing (F7 + commit Score + replay): no F2 row is ordinal and no row carries `option_level`. A side file keeps the band order so that, if the orchestrator rules otherwise, `option_level` is added by program and G18 runs | 1; 7; 9 item 3 |
| SC4b | C_DATA_SPEC 2.1 "two cards must differ in the domain pack and in the label schema or rule set" vs F2's per-pack reading | Literal reading adopted inside F2: one F2 card per pack (80 / 150 distinct training packs; the shared pool of >= 200 / >= 300 makes this feasible), and no two F2 cards share (schema, rule set). card_id = C_DATA_SPEC's tuple; clause-flip twins live in flip variants of the same card. Supersedes C12 and A49 | 1; 3.6; 3.7; 9 item 4 |
| SC4c | G13 method 6 vs sealed part P without a shared structure-hash scheme | F2's canonical form (3.8) is written to be self-contained so the orchestrator can apply it to part P in its own process (counts and ids only). F2's G13 is "pending" until that run exists and passes on zero hits after drops; F2 never relaxes G13 | 3.8; 7; 9 item 2 |
| SC4d | LICENCE_REGISTER section 3 "no third-party text" vs O*NET persona seeds | F2 follows C_DATA_SPEC v4 F4 and register section 4 (`gd_onet_occupation` KEEP); the section 3 text fix stays an orchestrator item | 1; 9 item 1 |
| SC5 | C_DATA_SPEC 2.1 "deep items form the depth sweep" vs C_DATA_SPEC 10 "no item shares text with a C training row" | Deep training rows and sweep items share generator settings only; sweep items are separate instances (held-out packs and styles, disjoint hashes, no shared text). Orchestrator to state this reading | 1.1; 5; 9 item 6 |
| SC6 | C_DATA_SPEC F5 counts "no fewer than" as a negation cue vs F2 counting comparator phrases as 0 | F2 logs both: "cue:<n>" = k_all of the shared negcount (comparator phrases with negation words count 1), used for the G10 negation-count cells [v5: SC14: read directly from negcount, no F2 list]; "neg:<n>" = the inverting count, used for polarity logic and the neg / dneg twin labels only [v5: SC13: no extra G10 check, no selection cell]. [v4: XF02] The 2.1 negation quotas use k_syn ("syn:") from the shared negcount, not "neg:"; the cross-family counter is settled | 3.8; 6; 9 item 7 |
| SC7 | G0 "1-page spec per generator with a semantics table" vs one long F2 spec | Section 11 adds a 1-page spec with a semantics table for each of S1-S5; the long body stays as the shared reference | 7; 11; 9 item 8 |

---

## 13. Resolved ambiguities (re-review round 2: R2-01 to R2-21, SC8-SC11)

Each row states the one semantics F2 now uses, in card terms where it is a card clause. Section 13 governs over
sections 10 and 12, and section XF over all; every earlier row it changes has been edited to the same rule (tag
"[v4: R2-..]"). No row was settled by XF alone; XF02 settles SC8. Section 14 (v5, v6) and section 15 (v7) govern over this section; rows
it changes carry "[v5: ...]" or "[v6: ...]".

### 13.1 Ambiguities R2-01 to R2-21

| ID | Resolution (one semantics) | Where |
|---|---|---|
| R2-01 | R2's per-line form is mode-neutral: "Round each line as the rounding rule says, then add the lines." R1 gives the mode and unit, R2 only the stage; per-line rounding always uses R1's mode and unit (half-up, half-even, floor or ceiling) | 2.2 R1, R2; 11.1; 11.3; 11.5 |
| R2-02 | R3: "Every comparison made after <amount> is rounded (with <T>, a band or outcome edge, a condition, a cap or a minimum) uses the rounded <amount>." Each comparison reads the value at its position in the card's step order with every earlier rounding applied. T alternative [v6: R3-15: reworded, with an operational meaning (branches from the run with no rounding step; reported and arithmetic values with the card's rounding steps), and R3 flips only on YN-T threshold cards whose question's comparison is the only comparison after rounding]: "Every comparison uses the <amount> computed with no rounding step at all; rounding changes only the reported <amount>." R3 is shown on every card that shows R1 and has any comparison after a rounding step. Rounding sits where R1 / R2 put it; X1 is shown whenever reordering can change the value or any comparison's outcome, and its rounding position agrees with R2 (A asserts). B3's adjustment is never a rounding step | 2.2 R3, X1, B3; 3.1; 11 |
| R2-03 | Every printed intermediate is its node's exact value; A asserts it is exactly representable at display precision, otherwise the structure is resampled. Printed intermediates are never rounded for display (R7 holds; B's check is exact) | 1.1 (c); 3.1 |
| R2-04 | M4: "An <amount> shown as \"<computed-cell marker>\" is the line's amount worked out from its <quantity> and <rate> by the card's pricing rule for that line (<the B4, partial-unit or per-k rule>, or else <quantity> x <rate>), before any rounding, cap or minimum; rounding, caps and minimums then apply to it as to a printed <amount>." Per-line R2 and X4 apply after it in the step order. No exception changes a marked line's quantity or rate (A asserts). Depth: 1 multiply node, or the B4 / R5 / U3 nodes | 2.2 M4; 3.1; S5; 11.5 |
| R2-05 | X3's "apply all in rule-number order" form is used only on cards whose applicable exceptions are all of one kind (all replace: "<rate or charge>" = "rate", last applicable replace wins; or all add: "charge", each added). A card mixing replace and add uses the "each alone" form (A asserts) | 2.2 X3; 3.1; 11.1 |
| R2-06 | New D16 [v5: R3-09: "calendar" always written]: "<k> calendar days after the last allowed day is the date <k> calendar days later; the last allowed day itself is not counted." (edge = L + k, k >= 1; L itself is "the last allowed day"). S4 named outcomes are B1 tables read on dates ("under" = before, "over" = after, "or more" = on or after), one B1 form per table, counted in B1's 50 +/- 5 split of tables and on-edge rows. The window is found by comparing the act date with the edge dates; no days-late count is printed (1.1 prints only counts that a later arithmetic step uses); the canonical graph has one node for the act's offset from L. Window edges are never fixed D2 dates; edge dates join the strip's relevant dates | 1.1; 2.2 B1, D16, lexicon rule; 3.7; S4; 6; 11.4 |
| R2-07 | Only an amount (display grid), a count, a date, a category or a yes/no fact can be the unknown field; durations, weights, distances, hours and other quantities are always printed (A asserts) [v6: R3-17: never the occurrence or count of a charge, payment or event of a W2-listed type; unknown yes/no facts and counts are attributes] | 2.2 W2; 3.1; 3.5 |
| R2-08 | Every category field a rule reads on an open-world card has one explicit list of all its values in the card or the document ("<category> is one of: <values>"), with at least one value no rule names; "any listed <category>" in W2 means that list, which is the admissible domain (A asserts; the parser extracts it) | 2.2 W2; 3.1; 3.3; 3.5 |
| R2-09 | F2 has no falsity predicates. The inverting count uses one closed list [v5: R3-02, R3-03, SC16]: not, n't, no, none, nothing, never, the operator "it is not the case that", and "fail to" only in "fail to meet <its> deadline" (never "neither ... nor"; hardly, unless, other than, lack, deny, refuse and rule out are not F2 question cues and never appear in a question). Cues sit only at proposition scope inside a truth-frame complement, never inside an entity description or on a fronted main-question auxiliary; A asserts and the parser rejects other cases, so every counted cue inverts the proposition | 2.2 N1; 3.1; 3.3; 3.8 |
| R2-10 | F2 has no world twins: W1, W2, M1, M2 and M3 have no "T" alternative, the world never changes inside a card or twin set, and premise_removed is F2's only open-world twin | 2.2 W1, W2, M1-M3; 3.6; 11.1 |
| R2-11 | A premise_removed twin keeps the base's option list. A builds the base's list so that every non-abstain option is also an E-assume value of the field the twin removes (one admissible completion, nothing compounded); the twin logs each as "err:E-assume". If no such list exists, the base gets no premise_removed twin. On every NEI-gold row, every non-abstain option (value, date, band or outcome) is an E-assume value | 3.1; 3.4; 3.6 |
| R2-12 | Every sentence or phrase that carries a SEM meaning (world and calendar clauses W0-W3, D1; connectives UN1, O1-O3, OR1, OR2; comparators and ranges CMP1-CMP4, D2, D3, B1, B4; date rules D4-D16 [v7: R4-09: and D17]; rounding, unit, exception and adjustment rules R1-R8, U3, U5, X1-X10, M3, M4, P1, T1) is in the card and refers to document values by name. The document holds values only (numbers, dates, names, category lists, yes/no facts, tables of them); band tables show edges as plain numbers and the card's B1 sentence defines them; inert additions are value lines. The parser rejects a SEM phrase in the document. "has:<x>" = the card states rule x (holidays: listed anywhere) | 2.1; 2.2 B1; 3.3; 3.6; 3.8; S1; S3; 6; 11 |
| R2-13 | An intermediate is the output of every arithmetic node except the final one. On group (c) rows every number entering an arithmetic node is printed (stated input or rule value, or printed intermediate); a selection step sits between arithmetic nodes only when its output is always one of its printed inputs (cap, floor, a rate picked by a gate, band lookup or D13 date, a tie-break); rounding, rolls and other number-making selections sit only after the final arithmetic node [v7: R4-08: X8 acts only on the final amount; R4-04: partial-unit rules never occur on group (c) rows]. Selection outputs are not printed. A asserts | 1.1 (c); 3.1 |
| R2-14 | A dimension planned for one of the card's flip variants is excluded from the short-card omission draw: the base and flip variants both show it | 2.1; 3.6 |
| R2-15 | S3's "banding amount is always computed" covers band-choice rows only (CH-B, and CL rows asking which case falls in a band). Total-charge, threshold and "pays more than <T>" rows may band a stated amount, since their charge computation is the unstated operation. Typical depths restated: on a stated banding amount, flat lookup + 1 multiply = 1, + fee = 2, marginal in band 1 = 1; a computed banding amount adds its own nodes | S3; 11.3; 12.1 R1-12 |
| R2-16 | E-alt:<ID> is a general hook on every choice row, one per listed alternative of each SEM dimension shown on the card, under the one-hook-per-value rule. For a dimension with its own hook (E-round, E-stage, E-roll, E-mode, E-add, E-base, E-gross, E-order, E-partial, E-prorate, E-ext; [v6: SC17] E-eom for D8) it is that same hook; dimensions without one (CMP, OR1 / OR2, B1, D4, D5, D10, D13, D14, T1, X3 form) have E-alt only, so choice-row clause-flip twins exist for them | 3.4 |
| R2-17 | Gold rank is uniform over ordered options: numeric options by value, dates by date, band and named-outcome options by edge rank; gold is the smallest and the largest each 1/k_ord +/- 2 pp per bucket. E-tier contributes the band below gold, above it, or both, drawn to meet this target | 3.4; 6 |
| R2-18 | Target tag per schema: "bind:<x>" on CH-V, CH-D, CH-C; "dec:<x>" on YN-T, YN-D, CH-B, CH-O and CL (on CL: the set of qualifying cases changes). Both tags are logged on every row | 3.8; 6; S1; S4 |
| R2-19 | (a) The card's yes rate p is P(the affirmative proposition is true); the label is that truth value inverted once per inverting cue, so single-negated rows on a card have yes rate 1 - p. (b) Yes/no rows' step-2 selection cells add k_all [v5: SC13: "neg:" removed, XF02] to family x label x wording x bin; yes and no are equalised inside each cell after crowd binning, and G10 re-checks. "By construction" is dropped | 3.6; 3.7; 3.8; 6; S2; 11.2 |
| R2-20 | Fixed polarity table per affirmative proposition and side: amount above / at least T, due, owed, charged = bad_yes for the paying side, good_yes for the paid side; amount below / at most T = the reverse; on time / met its deadline = good_yes for both date sides; late / missed its deadline = bad_yes for both date sides, whatever charges the card sets. Each inverting cue swaps the tag | 3.8; 6 |
| R2-21 | Every case on a case-list row falls in the same 1.1 row group (A asserts); the row counts in that group, `meta.deep` only for group (d), "stated_intermediate" only for group (c), "ops:<n>" = the largest per-case total; depth = the per-case maximum | 1.1; 3.1; 6; 12.1 R1-11 |

### 13.2 Spec conflicts SC8-SC11 (settled in favour of C_DATA_SPEC v4 and XF)

| ID | Conflict (short) | Resolution | Where |
|---|---|---|---|
| SC8 | C_DATA_SPEC 2.1 "syntactic negation >= 10% of yes/no rows" vs F2's "neg:" count, which also counts implicit cues | Settled by XF02: the 2.1 quotas use k_syn (F5 L_core tokens) from the shared `c_src/common/negcount.py`: k_syn >= 1 on >= 10% of yes/no rows, k_syn >= 2 with the affirmative twin on >= 2%. "neg:" is for polarity logic and twin labels only; falsity predicates are dropped (R2-09) | 2.2 N1; 3.8; 6 |
| SC9 | C_DATA_SPEC G0 "every choice that could flip a label is stated in the card" vs exception and rule sentences sitting in the document | Every SEM sentence is in the card; the document holds values only; the parser rejects a SEM phrase in the document (R2-12) | 2.1; 3.3; S1; S3 |
| SC10 | C_DATA_SPEC F2 "block answer = largest or smallest option" vs rank uniformity on numeric options only | Rank uniformity covers every ordered option (values, dates, bands, named outcomes); E-tier sides are drawn to meet it (R2-17) | 3.4; 6 |
| SC11 | C_DATA_SPEC F2 "more operations only when the text states each intermediate value" vs unprinted values after selection steps on group (c) rows | On group (c) rows every number entering an arithmetic node is printed; selections that make a new number sit only after the final arithmetic node; printed intermediates are exact (R2-13, R2-03) | 1.1; 3.1 |

---

## 14. Resolved ambiguities (re-review round 3: R3-01 to R3-24, SC12-SC18)

Each row states the one semantics F2 now uses, in card terms where it is a card clause. Section 14 governs over
sections 10, 12 and 13, section 15 (v7) over it, and section XF over all; every earlier row and body rule it changes has been edited to the same
rule (tag "[v5: R3-..]" or "[v5: SC..]"; round 3's remaining items R3-13 to R3-24 and SC17-SC18, resolved in v6, carry
"[v6: ...]"), so no superseded wording remains for a generator author to follow.

### 14.1 Ambiguities R3-01 to R3-24

| ID | Resolution (one semantics) | Where |
|---|---|---|
| R3-01 | A question carries at most one comparator, from CMP1-CMP3 (written whole and contiguous, so "does not exceed" is never split by a fronted auxiliary), or one OP predicate. CMP4, D2, D3, OR1 and OR2 phrases sit in card rules only and never in a question; "not more than", "not less than", "not before" and "not after" are never in a question. So "neg:" excludes exactly the CMP1-CMP3 phrases; one with a negation word ("no less than", "no fewer than", "no more than", "does not exceed", "fails to reach") counts 0 and tags the row "negcmp" (negcount gives each k_syn 0, k_all 1). A asserts; the parser rejects violations | 2.1; 2.2 CMP4, D2, D3, Q1, N1, lexicon rule; 3.1; 3.3; 3.8 |
| R3-02 | Negation cues sit only inside the complement P of a truth frame (TF): a frame that only asks whether a declarative P is true and has no negation, judgement or acceptance word of its own (meaning only; XF10 cites "Is it true that <P>?"; surface forms post-freeze). In P a cue negates P's main predicate, or is the operator "it is not the case that" at P's start. Never: a negated main-question auxiliary ("Isn't", "Doesn't", "Wasn't", "Didn't"), a negated frame ("Is it not true that"), "or not", "whether or not", "yes or no" in a question; the answer instruction is a separate sentence and is never counted. Only yes/no questions carry cues; choice and case-list questions carry none. Every negated row uses a TF; affirmative rows use one on 50 +/- 5%, independent of the label ("tf:"; G6 / G7 feature). A asserts; the parser rejects violations | 2.2 Q1, N1, lexicon rule; 3.1; 3.3; 3.8; 6 |
| R3-03 | N1's closed cue list: not, n't, no, none, nothing, never, "it is not the case that", and "fail to" only in "fail to meet <its> deadline" (= missed its deadline). Hardly, unless, other than, lack, deny, refuse and rule out are not F2 question cues and never appear in an F2 question ("unless" still appears in card rules, UN1); no other negcount L_neg entry appears in a question. k_all still counts what is there, through negcount | 2.2 N1, OP; 3.1; 3.3; 3.8 |
| R3-04 | Card clause on every card whose questions use due, owed or charged: "An <item> is <charged> (or <owed>) when its <amount> worked out under these rules, after every rounding, cap, minimum, discount and waiver, is more than 0. An <item> is <due> when a listed rule makes it <due>." Charged / owed = the question's named amount, final (the reported amount, after every rounding step, on the display grid), > 0 [v6: R3-14: on charged / owed rows A asserts that the amount computed with no rounding step is > 0 exactly when the reported amount is; no card with an OP money predicate has an R3 flip variant]. Due = the item's governing rule makes it due; on every row asking "due", A asserts that the amount is > 0 exactly when the rule makes it due (no waiver to 0, floor at 0, cap of 0, 100% discount or zero-day proration of a due item), else resample. YN-T rows that ask an OP money predicate carry "cmp:op" and are outside the comparator targets [v7: R4-06: no payment line of the row's entity on a card whose questions use "owed"] | 2.2 OP; 3.1; 3.7; 3.8; 12.1 R1-10 |
| R3-05 | B2 marginal clause: "Each rate applies only to the part of the <amount> inside its band: the part above the band's lower edge, up to its upper edge (for the lowest band, from 0 up to its upper edge)." The part is a measure, min(amount, hi) - lo, never a count of numbered units. Marginal tables over whole-unit counts use the upper-inclusive B1 form only (A asserts), where numbered units and the measure agree; B1 forms are drawn on the other tables so the 50 +/- 5 split holds | 2.2 B1, B2; 3.1; 10.1 A27; 11.3 |
| R3-06 | Adjacent bands share edges: each band's lower-edge cell holds the same number as the previous band's upper-edge cell (card-written outcome tables and S4 windows likewise start each band at the previous band's end value). Gapped edges (1,000 / 1,001, 1,000.01) are never rendered; A and the parser assert. A value on an edge has one candidate edge | 2.2 B1; 3.1; 3.3; S4; 10.1 A27; 11.3; 11.4 |
| R3-07 | M3 is closed-world only and names its column: "A blank cell in the <amount> column means nothing was charged on that line." It is shown only when a closed-world table or statement has a blank cell in that column, never for B1 edge blanks (B1's own "no edge" sentence covers those). Open-world cards have no blank amount cell; their one unknown is "not recorded" (R3-11), so "exactly one unknown field" holds on every S3 card | 2.2 M3, B1; 3.1; 3.3; 3.5; S5; 10.1 A02, A21; 12.1 R1-01; 11.1; 11.3; XF06 row; 9 item 9 |
| R3-08 | D6 is split. D6a (definition; [v6: R3-23] one form: "A business day is <Monday to Friday> that is not a holiday. The holidays are exactly the dates on the <record>'s holiday line; when that line says \"none\", there are no holidays.") is shown whenever business days are used or D7 appears. D6b ("<Act> must happen no later than <N> business days after <event>. Counting starts on the day after <event>; the <N>th business day is the last allowed day.") is shown only on cards whose deadline adds business days; A asserts it never appears on a calendar-day (D4), month (D8) or S5 settlement card, and the parser rejects two deadline rules for one act. The strip and D9 key on D6a | 1.1; 2.2 D6a, D6b, D7, D9; 3.1; 3.3; S4; S5; 10.1 A13, A58; 12.1 R1-12, R1-14; 11.4; 11.5 |
| R3-09 | D4, D16 and S5's settlement clause always write "calendar days" (D4a: "no later than <N> calendar days after <event>"; D16: "<k> calendar days after the last allowed day"; S5: "<N> calendar days after <period end>" [v7: R4-09: D17's whole settlement clause]), on every card, so no day count can be read as business days. D12 already states "calendar" or "business" | 2.2 D4, D16, lexicon rule; S4; S5; 10.1 A54, A58; 13.1 R2-06; 11.4; 11.5 |
| R3-10 | D4 has two whole forms. D4a (base): "<Act> must happen no later than <N> calendar days after <event>. The day of <event> is not counted, so the last allowed day is <N> calendar days after it." (last = event + N). D4b (flip form, T): "<Act> must happen on or before the <N>th calendar day, counting the day of <event> as day 1." (last = event + N - 1). D4b never uses the XF13 phrase; D4 has no filter alternative and is never shortened (the shown form is always whole) | 2.2 D4, lexicon rule; S4; 10.1 A54; 11.4; XF13 row |
| R3-11 | Rendering of absent and unknown values. Open-world: the one unknown is the literal text "not recorded" in every container (JSON and YAML: the string "not recorded"), never null, "unknown", a blank cell or a left-out key; no rule-read field is left out. Closed-world: an absent line item, condition or W3 field is left out (JSON and YAML: no key) or printed as "0", "no" or false; never "not recorded", "unknown", null or a blank. The only blank cells on any F2 card are M3 amount blanks (closed world) and B1 edge blanks. F2 never renders null or "unknown". [v6: R3-23] On every card that shows D6a, both worlds, the one holiday line is always printed (dates, or "none"); it is never left out and never unknown. A asserts; the parser rejects other forms | 2.1; 2.2 W1, W2, W3, M3; 3.1; 3.3; 3.5; 10.1 A02; XF06 row; 9 item 9 |
| R3-12 | An inert twin line or GSM-NoOp fact is inert only through an attribute the card's rules already read: another entity's record; a date outside every period a rule reads; a line type outside every summing rule's listed types; a rate in a row ID that no rate reference names. Each summing rule lists its entity, period and line types (A asserts on any card that can carry an inert line). W1 says only that the line happened; it enters a computed amount only through a rule's listed inputs, so W0 gives it no effect, and no question asks about it. Never inert: a line on a card whose sum is not defined by listed types, a second rate the card's reference cannot tell apart ("superseded" with no row ID or date the reference reads), or a line that changes a printed number. A asserts the line is outside every rule's listed inputs and that label and printed numbers are unchanged without it | 2.1; 2.2 W1; 3.1; 3.6 |
| R3-13 | R7 display grid on every row. Nothing is ever rounded for display: only the card's own rounding steps (R1 at R2's stage and X1's position) round a value. On every row, R1 shown or not, A asserts that the final value, the asked target node (including a "before <step>" value), every option value, every hook value offered as a distractor and the value the question's comparison, OP predicate or band / outcome lookup reads are exactly on the display grid as computed under the card's own steps (on an R3 T-form variant the question's comparison reads the value computed with no rounding step, as that card states); otherwise resample. An off-grid hook value is not eligible; an off-grid alternative value equals no option in an alt-label. When R1 is not shown, every value any rule's comparison reads is on the grid too (A51) | 2.1 (short cards, alt-label); 2.2 R7, Q1, A1; 3.1; 3.4; S1; 10.1 A04, A51; 12.1 R1-18; 11 |
| R3-14 | OP money predicates vs R3's T form. Charged / owed read the reported amount (after every rounding step). On every charged / owed row A asserts that the amount computed with no rounding step is > 0 exactly when the reported amount is > 0, else resample; no card whose questions use an OP money predicate has an R3 flip variant. So the T form never stands on a card with the OP money clause, and R3's two forms give one label on every OP row. OP rows are outside the rounding "dec:" denominator | 2.2 OP, R3; 3.1; 3.6; 6; 14.1 R3-04 |
| R3-15 | R3's T form: "Every comparison uses the <amount> computed with no rounding step at all; rounding changes only the reported <amount>." Operational meaning for A, B, every alt-label and the E-alt:R3 hook: (1) run the card's steps in order with every rounding step skipped and take every branch decision there (gates and conditions on computed amounts, which side of a cap or minimum binds, band and outcome lookups, the question's comparison); (2) compute the reported value and every arithmetic node with each rounding step at its X1 position, taking the branches fixed in (1). R3 flip variants are planned only on YN-T cards whose questions are all CMP1-CMP3 threshold questions and on which the question's comparison is the only comparison after a rounding step (A asserts), so the T form has one reading wherever a reader sees it | 2.2 R3; 3.1; 3.6; 13.1 R2-02 |
| R3-16 | X1's program check covers every askable node: the final value, every "before <step>" or other named target node any row of the card can ask ("the <amount> before <step>" = the value that enters <step> in the card's step order) and every printed intermediate, plus every comparison's outcome. X1 is relevant, and its filter tests other orders, whenever reordering can change any of these | 2.1; 2.2 X1, Q1; 3.1 |
| R3-17 | The open-world unknown field is never whether a charge, payment or event of a type the W2 clause names happened, and never a count of such items, since W2's "every ... that happened is listed" settles both. Unknown yes/no facts and counts are attributes of the entity or of a listed item ("member", "units used"); a listed event's date may be unknown, the event itself never. A asserts | 2.2 W2; 3.1; 3.5; 13.1 R2-07 |
| R3-18 | T1 card clause: "If two <items> give the same <amount>, choose the one with the <lower ID number or earlier date>." Keys are ID numbers or dates only (no priority keys). Every item of a card has an ID of one fixed width (same prefix, same digit count with leading zeros), compared as numbers, so numeric and text order agree; tied items always differ in the key. T alternatives: the reverse direction or the other key. A asserts; the parser rejects mixed-width IDs | 2.2 T1; 3.1; 3.3; 10.1 A14; XF05 row |
| R3-19 | Multi-line scopes. When a cap's or minimum's scope can hold more than one line (per total, per claim with several lines, per calendar week, month or year), no question asks for, and no option or hook is, one line's or item's share of the capped or floored amount; questions ask for a scope total or a value computed from scope totals; no allocation rule exists. A card with an X4 flip variant asks only for totals over every line of the wider scope. B4 always names its scope ("In each <line, claim, calendar week (Monday to Sunday), calendar month or calendar year>, units up to and including the <X>th ..."), and a scope wider than a line holds at most one line of that quantity, so no line split arises (an M4 marked line's B4 split is its scope's split). A asserts | 2.2 B4, X4, M4, Q1; 3.1; 3.6; S5; 10.1 A19, A20; 11.5 |
| R3-20 | Flat-fee band rates appear only on flat-mode tables; marginal tables use percent or per-unit rates only. A B2 flip variant, B2's alt-label and the E-mode hook exist only on tables whose rates are percents or per-unit rates. A asserts | 2.2 B2; 3.1; 3.6; S3; 11.3 |
| R3-21 | Filter alternatives widened. U3 (when omitted): pro rata, as a full k, and complete blocks only (price x (quantity / k rounded down)), the last a filter and hook reading only, never a card form. R4 (when omitted): every intermediate rounded half-up to display precision, and every intermediate rounded in R1's mode to R1's unit. D8 is never omitted (SC17) and its clause now says the day number is kept "also when <D> is the last day of its month", so it needs no filter; its overflow and end-of-month-kept readings are E-eom hook values only | 2.2 U3, R4, D8; 3.4; 10.1 A03; 12.1 R1-09 |
| R3-22 | "up to <X>", "a maximum of <X>" and "a minimum of <X>" sit in card rules only; no question carries them (so "is not up to <X>" never arises). Question-side comparators are the remaining CMP1-CMP3 phrases. A asserts; the parser rejects them in a question | 2.2 CMP1, CMP3, Q1, lexicon rule; 3.1; 3.3; 10.1 A54 |
| R3-23 | D6a has one form on every card: "A business day is <Monday to Friday> that is not a holiday. The holidays are exactly the dates on the <record>'s holiday line; when that line says \"none\", there are no holidays." Every card that shows D6a prints exactly one holiday line on every row, in both worlds: the 0-3 holiday dates with weekdays, or the value "none" (XF06's zero marker). The line is a rule value: never left out, never "not recorded". "This period" is no longer used. A asserts; the parser rejects a missing or second holiday line | 2.1; 2.2 D6a; 3.1; 3.3; 3.5; S4; 10.1 A13; 11.4; 14.1 R3-08, R3-11 |
| R3-24 | At most one D12 extension rule per card, with one <K>; several conditions for the extension are joined inside that one rule (R1-04). A asserts; the parser rejects a second extension rule | 2.2 D12; 3.1; 3.3; S4; 10.1 A17; 11.4 |

### 14.2 Spec conflicts SC12-SC18 (settled in favour of C_DATA_SPEC v4 and XF)

| ID | Conflict (short) | Resolution | Where |
|---|---|---|---|
| SC12 | XF01 "G10 checks 1/k +/- 2 pp per k bucket and per abstain option" vs F2's +/- 3 pp per option bucket with NEI and "None" pooled | G10 checks the observed abstain-gold rate against 1/k (the mean of 1/k over the bucket's rows) within +/- 2 pp, per k bucket and per abstain option (NEI and "None of the listed" separately) | 2.2 A1; 3.5; 6; 10.2 C11; XF01 row |
| SC13 | XF02 "a family-local cue list may stay for polarity logic only" vs "neg:" in the 3.6 step-2 selection cells, an extra G10 yes-rate check and the G6 / G7 feature list | "neg:" is used only by A's and B's polarity logic and the neg / dneg twin labels. Selection cells and the G10 yes-rate check use k_all only; the G6 / G7 features are "syn:" (k_syn), "cue:" (k_all), "tf:" and "negcmp" | 3.6; 3.8; 6; 9 item 7; 10.1 A32; 12.2 SC6; 13.1 R2-19; XF02 row |
| SC14 | XF02 (k_all = negcount's L_neg surface count) vs F2's own "cue:" list from C_DATA_SPEC F5's short list, which differs from negcount (without, except, few, false, cannot, need not, none of, ... are missing) | "cue:<n>" is negcount's k_all, read directly on the question sentence, with no F2 list; "syn:<n>" is negcount's k_syn. Under R3-01 to R3-03, k_all = "neg:" + 1 on "negcmp" rows, else "neg:", but QC always reads negcount's output | 3.8; 9 item 7; 10.1 A32; 12.2 SC6; XF02 row |
| SC15 | XF13 ("no later than <N> days after <D>" = up to D+N, every family) vs D4's flip and filter alternative "the day of <event> counts as day 1" (D+N-1) under the same first sentence | D4b rewords the whole clause ("on or before the <N>th calendar day, counting the day of <event> as day 1"), and D4 has no filter alternative, so the XF13 phrase always means D+N in F2 (R3-10) | 2.2 D4; S4; XF13 row |
| SC16 | XF10 ("negation is written as truth-frame syntactic negation") not carried into F2's N1, 3.8 and G3 | Every N1 cue sits inside a truth-frame complement; negated main-question auxiliaries, negated frames, "or not", "whether or not" and "yes or no" are banned in questions; the G3 parser rejects violations (R3-02) | 2.2 N1, Q1; 3.3; 3.8; XF10 row |
| SC17 | C_DATA_SPEC v4 section 8 G0 ("every choice that could flip a label is stated in the card") vs D8 "relevant whenever the day number is > 28", which leaves D8 off a card whose month-end anchor has day number <= 28 (28 February in a common year), where the end-of-month reading gives 31 March against A's 28 March | D8 is shown, as "never", on every card with a month offset, whatever the anchor's day number. Its clause says the day number is kept "also when <D> is the last day of its month" (28 February + 1 month = 28 March), so the end-of-month reading is excluded by stated text; D8 has no filter alternative, and its overflow and end-of-month-kept readings are E-eom hook values only (R3-21) | 2.1; 2.2 D8; 3.4; 10.1 A03, A17; 11.4 |
| SC18 | XF05 (a tie rule names a stated stable key, for example "the lower <ID number>", fixed-width IDs) vs T1 "lower ID" with no ID format (numeric vs text order differ for "C-9" and "C-12") and "higher priority number" (larger number vs top priority) | T1 uses XF05's form: "the <lower ID number or earlier date>", every item's ID of one fixed width, compared as numbers; priority keys are dropped (R3-18) | 2.2 T1; 3.1; 3.3; 10.1 A14; XF05 row |

---

## 15. Resolved ambiguities (re-review round 4: R4-01 to R4-11, SC19; cross issues r2: XC-01; A16.1 (g): CP1)

Sources: `G0_OPEN_r3.json` (11 label-flip ambiguities, numbered R4-01 to R4-11 in the order listed there, and 1 spec
conflict, SC19) and `G0_CROSS_ISSUES_r2.json` (the one issue that names F2, XC-01). CP1 applies PREREG_FINAL amendment
A16.1 (g). Each row states the one semantics F2 now uses, in card terms where it is a card clause. Section 15 governs
over sections 10, 12, 13 and 14, and section XF over all; every body rule and earlier row it changes has been edited to
the same rule (tag "[v7: ...]" in the earlier tables), so no superseded wording remains. With this section F2 has 0 open
label-flip ambiguities (A16), and v7 is the frozen G0.

### 15.1 Ambiguities R4-01 to R4-11

| ID | Resolution (one semantics) | Where |
|---|---|---|
| R4-01 | R1's directional forms say that a value already on the unit grid stays: "Always round <quantity> down to a whole number of <unit>s; a value that is already a whole number of <unit>s does not change." / "Always round <quantity> up to a whole number of <unit>s; a value that is already a whole number of <unit>s does not change." (Decimal FLOOR / CEILING). "Next" is dropped, so 12.00 rounded up to whole units stays 12 | 2.2 R1; 3.1; 10.1 A25 |
| R4-02 | Half-even is shown (on a base or flip variant) only when the rounding unit is at most one whole unit of the quantity (0.01, 0.1 or 1 of the currency or other unit), where an exact half always has exactly one even neighbour; A asserts. Cards with coarser rounding units (10, 100, ...) show half-up, floor or ceiling; as a filter or hook alternative there, half-even means the multiple of the unit whose number of units is even | 2.2 R1; 3.1; 10.1 A25 |
| R4-03 | R5's exact form is "For each <line>, the <quantity> is charged exactly as stated; no part of a <unit> is rounded." It names no sub-unit, so no reader first cuts the quantity to whole sub-units | 2.2 R5 |
| R4-04 | R5 and U3 always name their scope, the line: "For each <line>, ..." (<line> = the record's line kind: line, session, visit, item). Each applies to each line's own quantity before that quantity is priced, summed, banded, compared or split. A asserts: each line holds one quantity of the kind; every band edge and every B4 threshold X that splits such a quantity lies on the rule's grid (a whole number of <unit>s for R5, a multiple of k for U3); and the quantity before and after the rule falls in the same band and on the same side of every threshold or condition of a card rule that reads it (the question's own comparison reads its Q1 target node). So applying the rule per band or B4 part, to the whole line before a split, or before or after a lookup or comparison all give gold. Partial-unit rules therefore never occur on group (c) rows (1.1) | 1.1 (c); 2.2 R5, U3, B4; 3.1; 11.1; 11.3; 13.1 R2-13 |
| R4-05 | On every card on which a rate that is itself a percent rises, in either R6 form, the card carries: "A rise of <k>% in a percentage rate multiplies it by (100 + <k>)/100; a rise of <k> percentage points adds <k> to it." A rise of a rate that is not a percent ("the price rises by <k>%") needs no sentence. Reading points for percent stays distractor E-pct | 2.2 R6; 3.1 |
| R4-06 | "Owed" keeps the OP clause (the named amount after every rounding, cap, minimum, discount and waiver is more than 0). No row of a card whose questions use "owed" lists a payment line of the row's entity (A asserts), so "owed" read before or after payments is one amount | 2.2 OP; 3.1; 14.1 R3-04 |
| R4-07 | A card shows both a cap and a minimum only when, on every variant, the minimum's scope equals the cap's scope or is a union of whole cap scopes (cap per line with minimum per claim or per total; cap per calendar month with minimum per calendar year); never a minimum narrower than the cap, never weeks against months or years. A asserts; other structures are not generated. So "the minimum is applied after the cap" always reads scope totals that the cap fully defines, and no line share is needed | 2.2 X4; 3.1 |
| R4-08 | X1's program check permutes a closed set, the card's adjustment steps: caps and minimums (X4), discounts (R8, X5), percentage fees and charges (X6, X7), added fixed amounts and subtracted deductions (U5), exception switches (X2, X3) and waivers (X9), in every order that data dependencies and stated orders allow (X6's named base, B3, X4's minimum after the cap, M4's pricing before rounding, caps and minimums). Steps with a fixed place are never permuted: partial-unit rules (first, R4-04), M4 line pricing, rounding (R1 at R2's stage) and X8. X8's clause is "The final <amount> owed cannot go below 0.": max(0, v) on the final amount only, before a final rounding step if there is one; A asserts every other amount node (money, quantity, count; date offsets exempt) is >= 0 on every row, so flooring an earlier node would change nothing. When X1 is shown, its order names every adjustment step of the card | 1.1 (c); 2.1; 2.2 X1, X8; 3.1; 11.1; 13.1 R2-13 |
| R4-09 | New D17 for the S5 settlement date: "The settlement date is <N> calendar days after <period end>; the day of <period end> is not counted. If the settlement date falls on a day that is not a business day, the roll rule applies to it." (settlement = period end + N, then one D7 roll). On S5 cards D7's clause names the settlement date, D7 is never omitted, and D6a is always shown. Its lexicon entry is its own (longest match). Counting the day of the period end as day 1 is distractor E-day | 2.2 D7, D17, lexicon rule; 3.1; 3.3; S5; 11.5; 10.1 A58; 13.1 R2-12; 14.1 R3-09 |
| R4-10 | W2 now reads "... an unknown date any calendar date, except where a sentence of the record bounds that date ...". A also recomputes the NEI status and the label with every natural precedence of the row's events added as a bound (a consequence such as an act, payment, refund or return not dated before the event its rule counts from or that it answers; a date listed under a period of the record inside that period) and rejects the row if either changes. Explicit bound sentences stay the only bounds of A's domain and of z3 | 2.2 W2; 3.1; 3.5; 10.1 A01; 12.1 R1-06 |
| R4-11 | Round 1 has no backward deadline. Month offsets go forward only ("<M> months before <D>" is not generated), and A asserts that every last allowed day is on or after the day of <event>, after every extension and roll ("previous business day" rolls included); the parser rejects a backward month offset. So D15's second clause ("also when it is on or before the day of <event>") never covers a day after the last allowed day, and "Round 1 places no act on or before the event day" holds on every card | 1.1 node table; 2.2 D8, D15; 3.1; 3.3; S4; 10.1 A17; 11.4 |

### 15.2 Spec conflict SC19 (settled in favour of C_DATA_SPEC v4 and XF06)

| ID | Conflict (short) | Resolution | Where |
|---|---|---|---|
| SC19 | 2.1, R3-11, M3 and R1-01 vs XF06: an M3 line shows no quantity and no rate, but table containers with quantity and rate columns had no allowed form for those two cells (a blank there is card-undefined; '-' and 'n/a' are banned; '0' could read as a priced line) | On an M3 line the quantity and rate cells hold the XF06 zero marker "none", in every container that has those cells, never a blank and never "0". R1-01's "a line that shows no quantity and no rate" means both cells read "none"; the parser reads them so (never as 0 x rate) and rejects a blank or "0" there. The only F2 blanks stay M3 amount blanks and B1 edge blanks. MARKERS F2 row update requested (9 item 10) | 2.1; 2.2 M3; 3.1; 3.3; S5; 11.5; 12.1 R1-01; XF06 row; 9 item 10 |

### 15.3 Cross-family issue XC-01 and ruling CP1

| ID | Issue (short) | Resolution | Where |
|---|---|---|---|
| XC-01 | Cross issues r2, issue 1 (MARKERS M4): a left-out key on a closed card means unknown in F6 but absent or the default in F2 and other families | F2 already uses the recommended "no" reading, now stated once in 2.1: a left-out key or field never means unknown on any F2 card; on closed-world cards it is absent (W1) or the W3 default, and open-world cards leave out no field a rule reads. No F2 change is needed under either orchestrator ruling | 2.1; 3.1; 9 item 11; XF06 row |
| CP1 | PREREG_FINAL A16.1 (g): on choice rows everything a row needs goes in `instructions`, `state` or "- option: definition" card lines; schema_branch_mark shows only option-definition lines from the card on choice rows; every row passes loader_check; token caps count `instructions` twice | Yes/no rows keep the card in the `card` field. Choice rows have an empty `card` field and no option-definition line: every card block goes to `instructions` (fmt1 `render_row_text`, choice_card "move"); the document, S3 band tables (the CH-B band definitions) and CL case values go in `state`; options carry only their own text (CL: case references from fmt1 `case_refs`). CH-O outcome tables, masked IDs and swapped words are defined in the card text, so in `instructions`. Every row passes fmt1 `loader_check` before G3. Lengths are measured on the rendered prompt (`instructions` and option texts twice), with smaller example caps on choice cards. CL frames: case-in-text frames (IVC04-IVC07) only on cards that never show "None of the listed"; few-shot answers are option text | 1; 2.1; 3.3; 3.4; 3.6; 3.7; 7; 9 item 12; 11; 10.1 A57; 12.1 R1-29 |

---

## XF. Cross-family alignment (orchestrator fixes, 3 Oct 2026)

The cross-family consistency review (18 issues over F1-F13 and COMMIT) set one rule for every family where families
differed. **This section governs over every earlier section of this file**, including the resolved-ambiguity tables;
earlier text and rows it supersedes have been edited to the same rule (v4), so no conflicting number or rule remains. No label of an existing
row changes, because no C row exists yet (G14). Code named here (`c_src/common/...`) is orchestrator-owned and is
written only after the sealed sha256 commit.

| ID | Rule (same text in every family that carries it) | Effect in F2 |
|---|---|---|
| XF01 | **Abstain gold = 1/k (display-then-gold).** Draw k (abstain slots included), then the display, then the gold slot uniformly over the displayed slots; reject structures whose gold class does not match. An abstain option (NEI, CBD, None, 'none of these', 'no record', tie options) is shown only when k >= 3 and only on rows where it can be gold; no always-wrong abstain display. Each abstain option is gold with probability exactly 1/k; G10 checks 1/k +/- 2 pp per k bucket and per abstain option, so G6(b) and G7 (p0 = 1/k) sit at chance. The ~10% NEI aggregate is only a mixer count; no family tunes toward it. | F2 already used display-then-gold with abstain gold 1/k. Added: an abstain option is shown only at k >= 3, so every open-world (NEI) row has k >= 3 and 'None of the listed' appears only on closed-world rows with k >= 3 (no abstain on k = 2 rows, where 1/k = 50% sat on the floor). G10 checks 1/k +/- 2 pp per k bucket and per abstain option (NEI and 'None of the listed' separately; v5, SC12). 3.5, A1 and the section 6 abstain row updated. |
| XF02 | **One negation counter.** Every family uses the orchestrator-owned `c_src/common/negcount.py` (not written by any family builder). k_syn = number of F5 L_core tokens in the question (not, n't, no, none, nobody, nothing, nowhere, never, neither, nor). k_all = F5 L_neg surface count (longest match; comparator phrases such as 'no fewer than' and implicit cues included; C_DATA_SPEC 2.2 F5). 2.1 quotas use k_syn: k_syn >= 1 on >= 10% of yes/no rows; k_syn >= 2 with an affirmative twin on >= 2%. G10 yes-rate negation-count cells use k_all. Whether an L_core token inside a matched multiword comparator entry (the 'no' of 'no fewer than') counts toward k_syn is fixed once inside negcount, never per family. A family-local cue list may stay for polarity logic only. | The 2.1 quotas use k_syn ('syn:') and the G10 cells k_all ('cue:'), both read directly from the shared negcount on the question sentence, with no F2 list (v5, SC14). 'neg:' stays for A/B polarity logic and neg/dneg labels only: it is no selection cell, G10 check or G6 / G7 feature (v5, SC13). 3.6 step 2, 3.8, section 6 and section 9 item 7 (settled) updated. |
| XF03 | **Twin-set count.** A row counts toward 2.1's 20-25% only if it sits in a contrast set: a base plus label-flip twins with their own `call_id`, built by a change to the input text or structure (fact, boundary, premise, clause, definition or world flip, or deletion to NEI). `complement`/`equiv` negation units, `inv` attack units and `equiv` inert units count only toward the negation, attack (~5%) and inert (<= 5%) quotas. | 3.6 shares: neg/dneg members no longer count toward 20-25%; boundary, clause_flip and premise_removed sets are raised to reach 20-25% alone. |
| XF04 | **'Yes = bad outcome' denominator.** All yes/no rows of the family. Rows with no polarity are <= 5% of the family's yes/no rows and count as not-bad. No family-chosen subset denominator. | No change: every F2 yes/no row carries 'pol:bad_yes\|good_yes'; denominator is all yes/no rows. |
| XF05 | **Ties never by position.** A tie between equal quantities is never broken by document, listing or table position. A tie rule names a stated stable key (for example 'the lower <ID number>', fixed-width IDs) or the generator makes no ties. 'Tie broken by position' is a wrong reading in the convention checks. Option labels are exempt; card-stated rule precedence (a decision list, an entry-number order) is not a positional tie-break. | T1 ties are never broken by list position. v6 (R3-18, SC18): T1 uses XF05's key form: "the <lower ID number or earlier date>", with every item's ID of one fixed width (same prefix, same digit count) compared as numbers; priority keys are dropped; tied items always differ in the key. |
| XF06 | **Missing-value markers.** One cross-family marker table, orchestrator-owned in `c_src/common/`, enforced by every parser. Unknown: 'not recorded', 'unknown', JSON/YAML null. Zero or absent: '0', 'none', 'no', false. Banned in every family: '-', 'n/a', 'N/A', 'TBD', '?'. Blank cells stay card-defined (a definition-following contrast) and appear only on rows whose card states the blank's meaning. Unknowns on closed or local cards use word markers or null, never blanks, so a blank on a complete record means none/no wherever it appears. | No conflict. v5 (R3-07, R3-11): F2's blanks are card-defined and never unknowns: M3 (closed-world cards only) = nothing charged in the named amount column; B1 edge blanks = no edge. F2's one unknown marker is the literal 'not recorded' in every container (JSON and YAML: the string); F2 never renders null or 'unknown' (stricter than the table); closed-world absent values are left out or printed as '0', 'no', false. The parser enforces the shared table and these F2 limits; '-', 'n/a', 'N/A', 'TBD', '?' never appear. MARKERS row update requested (9 item 9; done in MARKERS v1.1). v7 (SC19, XC-01): an M3 line's quantity and rate cells hold the zero marker 'none', and no left-out key means unknown on any F2 card; F2 row update and sha refresh requested (9 item 10). |
| XF09 | **One pack per card.** Within a family, no two cards share a domain pack (round 1 >= 80 packs for >= 80 cards, round 2 >= 150; F12 and F13 follow their own card counts). Different families may use the same pack. | No change: one pack per card (flip variants count inside their card). |
| XF10 | **Shared negation-frame lint (from F5).** No question wraps a negated or negatable proposition in an outer judgement or acceptance predicate ('wrong', 'right', 'reject', 'accept', 'should/would ... be'). Negation is written as truth-frame syntactic negation ('Is it true that ... does not ...?'). **Scope (cross-family fix, 3 Oct):** the shared lint bans only these outer judgement or acceptance predicates; the truth frames 'Is it true that', 'Is it not the case that' and 'Is it false that' over an affirmative claim are allowed, and a family may ban more on its own, as a family-local rule that it does not cite as XF10. | Added to the 7.2 #8 / G3 wording checks: no outer judgement or acceptance predicate around a negated or negatable proposition. v5 (R3-02, SC16): the truth-frame rule is carried into N1, 3.8 and the G3 rejections: every N1 cue sits inside the complement of a truth frame that carries no cue; no negated main-question auxiliary, no negated frame, no 'or not' / 'whether or not' / 'yes or no' in a question. |
| XF11 | **F5 interface and cross-family G12.** F5 stays independent (it re-implements the shallow structures it needs and imports no other family's generator). F1 reserves no seed range for F5; F9 has no export for F5 (X4 = no export). The orchestrator adds a cross-family G12 pass: exact text hash plus MinHash over F5 rows against F1, F2, F3, F4 and F9 rows, and over F13 rows against F1, F3, F6 and F9 rows; each near-duplicate pair is dropped from F5 or F13. | F2 rows are a comparison set in the cross-family G12 pass against F5 rows; drops fall on F5. |
| XF13 | **Window phrases.** 'within <N> days after <D>' = D+1 through D+N (anchor excluded; F5 SEM-11, F9 T18). 'the <N> days ending on <D>' = D-N+1 through D (N days; F9 T16). 'within N days of D' = D through D+N (F7, F13). 'no later than <N> days after <D>' = any day up to D+N inclusive, no lower bound (F2 D2). | D4a: '<Act> must happen no later than <N> calendar days after <event>' (inclusive, no lower bound, as D2; inserting 'calendar' keeps the XF13 meaning); D15 unchanged. F2 no longer uses 'within ... after'. v5 (R3-10, SC15): D4's flip form D4b ('on or before the <N>th calendar day, counting the day of <event> as day 1') never uses the XF13 phrase, and D4 has no filter alternative, so no F2 card gives 'no later than <N> days after' any meaning but D+N. |
| XF16 | **F14 exclusion lint.** 'No row poses <F14 task>.' The orchestrator names F14's skill and structure type before step 5 (generator code) and fills in the lint then. Provisional instance (constraint scheduling): no row asks for a feasible slot or assignment for several items under pairwise constraints. The QC agent's F14 builder checks, by structure type, that no C training row matches F14's structure, and logs the result. | Lint added (G3 and QC check): no F2 row poses <F14 task> (for example, S4 calendar rows never ask for a feasible slot or assignment for several items under pairwise constraints). |
| XF17 | **G14 and operator lexicons (orchestrator ruling, recommended default).** Closed operator lexicons (meaning-bearing operator phrases only, each mapped to a SEM row, with no domain words, entity names or templates) are G0 semantics and allowed before the sealed freeze. They pass the 7.2 Claude-seed decontamination and the counts-only sealed template compare before any use. If the orchestrator rules the other way, closed lexicons move to step 4 and only the SEM meaning rows stay in G0. | 'lexicon entries' removed from the G14 forbidden list in the header; closed operator lexicons are G0 semantics. |
