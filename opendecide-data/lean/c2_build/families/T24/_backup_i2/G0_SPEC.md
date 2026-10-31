# G0-lite T24: revision materiality, does the edit change this case's outcome? (C2 everyday tier; spec 2.1, 3.12)

One page (C2_DATA_SPEC 6.2 item 3): a semantics table, one ambiguity listing, one resolution. **v2.2, FROZEN** on 14
Oct 2026: v2 after the one Haiku ambiguity pass (`c2-data-stage-a/amb:T24`; 45 points H1-H45, verbatim in
haiku/ambiguity/amb_T24.json; it read v1, sha 4f41cc72), v2.1 the Mode F writer rule, v2.2 the Stage B pilot fixes
F1-F4 (card text and placement, packs, role balance, skin deal; section 5). This file's sha is
`plugin.T24Plugin.G0_SHA256`;
`validate_plugin` refuses the plugin if the file changes, so a later change is a new version with a new sha and a
dated line in section 5. Target 600 selected rows (about 900 generated), wave 2. Ids (H37): R1-R20 are rows of the
semantics table, S1-S5 are samplers only, H1-H45 Haiku points. Terms from outside this page (H42): spec 3.0 (Mode T /
F, registers, wordings, packs; inverted, few-shot, masked-label and short cards), spec 4.1 (overlay: complement;
non-syntactic = antonym, implicit or option-framing complement; minimal-edit twin; equiv = the same facts in another
skin and container; a unit = a base row and its partners), spec 6.3 (G2 solver B, G3 parse round trip, G4 metamorphic,
G6 partial-input baselines, G11 diversity, G15 loader, G-SL, G-LEX, G-TW, G3-H, G5-H), spec 7.1 (mixdev = dev-only
rows), PREREG A38 (OHS-4 freeze), T23 (the family that owns "which version governs"), `c_src/common/negcount.py`
(R16), kit README (paradigms, `build_closed`, `rules.ast_equal`, `lexicon.parse_exact`, the error-model CATALOG),
plugin.py (`check_domain`, `_docs`, `_case`, `mode_of`).

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| R1 | Row | Two versions (original V1, revised V2) of one invented policy, one case record, one narrative, the card, one question. V2 = V1 with exactly ONE typed edit (R6) plus 0-2 cosmetic rewordings and an optional swap of two adjacent lines. A cosmetic row (edit kind "cosmetic") has NO typed edit: 1-2 rewordings plus the optional swap (H1) |
| R2 | Pack | title ("... policy"); case-id prefix (3 capitals); two date fields ("... date", d1 never after d2, never "request date"); one money field; 4-5 categories; 3 conditions; outcomes (POS, ALT, NEG). Every pack string (title, fields, categories, conditions, outcomes) is lower-case words, hyphens or apostrophes: no digit, comma, " and ", pipe, brace or negation cue (any negcount entry: k_all > 0) (H13); all distinct; no pack string holds a materiality label word (change, same, different, affect, matter ...) and no category, condition or field holds a generic outcome word (plugin LABEL_WORDS). `check_domain` tests it |
| R3 | Case facts | customer (name), case id, category, condition, amount (integer cents, USD), d1, d2, request date (calendar dates; d1 <= d2 <= request). Printed intermediates: days from d1 and from d2 to the request date (calendar days, >= 0) |
| R4 | Clauses | each kind at most once per version, only `win` always present (H2): `win` time limit N days counted from date field A; `amt` money rule: amount OP X, OP in {at least, more than, at most, less than}; `exc` category C excluded; `alt` condition K gets outcome O (O = the pack's ALT outcome name, printed in the clause; H14); `ovc` category C has time limit N instead; `ovd` cases whose date field A (the clause's OWN slot, d1 or d2, drawn apart from win.A; H3) lies in [S, E], both ends included, have time limit N instead. At most one of ovc / ovd. N: whole days (win 7-90, special 3-90, never the base N); S <= E calendar dates (S = E: one day); X: positive whole cents (H7) |
| R5 | Decision of one version | NEG if (category = exc.C) or late or (amt present and not amount OP X); else ALT if condition = alt.K; else POS. Day count = request date minus win.A's date in calendar days (win.A is day zero: day N on time, day N + 1 late; no business days or holidays; H4, H5). Late: day count > limit; limit = the special N when ovc (its category) or ovd (its own date in [S, E]) covers the case, else win.N. A special clause never moves the day count's date. Counts are one-sided: every date field is on or before the request (R3; H6) |
| R6 | Edit kinds (closed; H10) | anchor (win.A to the other field); limit (win.N); amount (X by a step; inclusivity ge<->gt / le<->lt; clause added, removed; never a direction reversal ge<->le); alt (K to another condition, added, removed; O never edited); excl = scope (C to another category, added, removed); override (ovc C or N, ovd window [S, E] or N, added, removed; never ovd.A, never ovc<->ovd); cosmetic (no typed edit, R1) |
| R7 | Cosmetic rewording | V2 writes a clause with another ADMITTED lexicon form of the same meaning, so solver A's AST is unchanged (`rules.ast_equal`). G-LEX admits a form at 2/2 independent blind extractions, 3/3 for lexicon kind "window" (win, ovc, ovd) (H12): spec 3.12's "2 independent extractions give an AST identical to V1's" plus spec 6.2's 3/3 for window rules |
| R8 | Materiality | changes iff outcome(V1) != outcome(V2), each version applied on its own to the same case; reworded text never counts, only outcomes (H20). Both versions apply to this case: "(before / after the update)" are headers, not effective dates (H11; effective dates are T23's) |
| R9 | Card | the boxes below, verbatim (H16): the outcome rule (NEG checks, ALT, POS), the special-limit rule ("replaces only the limit"), the day-count rule, the lists, "each version on its own", R17. Style per unit, label-blind, from the seed (every row of a unit alike): full 85%, short 15% (spec 3.0; no "none" style: the answer needs the rules). Placement: yes/no rows carry the card in `row.card` (the served prompt prints it once), choice rows in the instructions before the question (printed twice, the only place a choice row prints it) |
| R10 | Record | "Case record {CASE_ID}:" then category, condition, {money field}, {d1}, {d2}, request date, "days from the {d1} to the request date", "days from the {d2} to the request date". The deciding count is the one for the date the time-limit clause names; the card says so (H45) |
| R11 | Versions container | S1, S2 lines: "{Title}, original version:" / "{Title}, revised version:" + "- {clause}." bullets; S4 update: "Original version of the {title} (before the update):" / "Revised version of the {title} (after the update):", both versions in full (H18); S3 table: rows Time limit / Amount rule / Exclusion / Condition rule / Special time limit, each cell the whole clause (scope and N; H17), "(none)" when absent, a row absent in both left out; S5 diff (held out): V1 bullets + "Edits made in the revised version:" + "removed: ..." / "added: ..." lines: V2 = V1 minus the removed lines (exact whole-line match) plus the added lines after the kept ones; a reworded clause is a removed + added pair; a swap is not shown; line order never matters (each kind once; the card fixes the check order) (H19) |
| R12 | Block order | S1 narrative, versions, record; S2 record, versions, narrative; S3 versions (table), record, narrative; S4 narrative, record, versions (update); S5 narrative, versions (diff), record. One blank line between blocks; no skin holds a blank line |
| R13 | Question forms | predicate "material" = the outcome for this case differs between the versions: yn_changes (+), yn_dneg (+, "Is it not true that the revised version makes no difference to the outcome for this case?"), yn_same (antonym, -), yn_not_change (syntactic, -), yn_fail_change (implicit "fail to", -). ch_v2: the outcome under V2; options = outcome names {POS, NEG} plus ALT when either version has an alt clause (the set depends on the versions, never on the gold; when V2 removed the clause, ALT is a wrong option, often the output of `t24_removed_clause_kept`; H22); label-blind order (`build_closed` shuffle). No abstain option: both versions decide every case |
| R14 | Answers | yes/no: 1 = yes, 0 = no. yn_changes, yn_dneg: yes iff the outcomes differ; yn_same, yn_not_change, yn_fail_change: yes iff they are equal ("fail to change" = the outcome stays as it was; H21). ch_v2: the role key pos / alt / neg (option text = the pack's outcome name) |
| R15 | Error models (ch_v2) | One reading mistake each, applied to V2: `t24_original_version` (V1's outcome); `wrong_anchor`; `count_day0` (counts win.A as day 1: day N late); `off_by_one_late` (counts one day past the end as on time: day N + 1 on time; kit names, opposite directions; H28); `t24_ignore_time_limit`; `t24_ignore_special_limit`; `t24_special_limit_for_all`; `t24_special_date_as_anchor`; `t24_ignore_exclusion` (the excluded category); `ignore_exception` (kit name: the condition clause, the exception that gives ALT; H27); `t24_ignore_amount_rule`; `drop_inclusive_endpoint` / `add_exclusive_endpoint` (amount operator only: ge->gt, le->lt / gt->ge, lt->le; H29); `t24_amount_rule_reversed`; `t24_negative_rule_misread` ("... do not qualify" read as the requirement); `t24_condition_before_gates`; `t24_condition_scope_ignored`; `t24_condition_as_exclusion`; `t24_alternative_as_fallback`; `t24_removed_clause_kept`; `t24_default_outcome` (skips the NEG checks); `t24_qualifies_in_full` (POS). A model that does not apply returns nothing and one that gives the gold is not recorded; each wrong option records the models giving it (about 97%); one no model gives keeps the kit role `closed` (H30) |
| R16 | Negation counts | negcount: k_syn = core tokens (not, n't, no, none, nobody, nothing, nowhere, never, neither, nor); k_all = negation entries, implicit ones included ("fail to", "lack", "without", ...) (H26). yn_changes / yn_same / ch_v2: k_all 0; yn_not_change k_all 1, k_syn 1; yn_fail_change k_all 1, k_syn 0; yn_dneg k_all 2, k_syn 2. Complement pairs: yn_changes with yn_same (50%), yn_not_change (25%) or yn_fail_change (25%); yn_dneg with yn_not_change only |
| R17 | Closed world | every card ends "The two versions and the case record are complete: no other rule or fact applies." |
| R18 | Depth | 2: the outcome under each version, then their comparison; every day count printed. `meta.deep` = all five clause families across the versions: win, amt, exc, alt and a special (ovc or ovd, one family; H41); about 9%, cap 10% |
| R19 | Solver A = gold | `rules.RuleSet` per version (first_match: excluded, late_special / late, amount, condition; default POS) run by `rules.resolve` on the slots; clause values as Lit, case facts as Ref; `days_between` (paradigm ast_interpreter). Gold is solver A's answer (H31) |
| R20 | Solver B | its own parser (card regex; block headers; bullet / update / table / edit-list readers; every clause through `lexicon.parse_exact`, admitted forms only; record regex; skin template); sqlite: one SQL query per version (julianday counts checked against the printed counts, COALESCE of the special limits over the base, EXISTS for exclusion / amount / condition, CASE for the outcome) (paradigm sql_sqlite). G2: B = A on 100%, else the unit is dropped and counted (H31) |

R9, the card, full style (program text; {POS}, {ALT}, {NEG}, {title}, {money field} and the lists are pack constants):
```
Apply each version of the {title} to the case on its own.
- The outcome under each version is {NEG} if the case's category is excluded, the request is late, or the case fails a rule on the {money field}; otherwise {ALT} if a clause gives {ALT} for the case's condition; otherwise {POS}.
- A special time-limit clause replaces only the limit, for cases in its category or whose date it names lies in its window (both end dates included).
- Day counts are calendar days from the date named in the time-limit clause (day zero), printed in the record. Late means a day count above the limit.
- Categories: {c1, c2, ... and cn}. Conditions: {k1, k2 and k3}.
The two versions and the case record are complete: no other rule or fact applies.
```
R9, short style (the same rules and lists; no title line, `cards.variant_problems` checks each item against the full one):
```
- Outcome under each version: {NEG} if the case's category is excluded, the request is late, or the case fails a rule on the {money field}; otherwise {ALT} if a clause gives {ALT} for the case's condition; otherwise {POS}.
- A special time-limit clause replaces only the limit, for its category or for cases whose date it names lies in its window (both end dates included).
- Late means the day count (calendar days from the date named in the time-limit clause, day zero, printed in the record) is above the limit.
- Categories: {c1, c2, ... and cn}. Conditions: {k1, k2 and k3}.
The two versions and the case record are complete: no other rule or fact applies.
```
Value forms (kit slots; one seeded form order per kind per row, label-blind; H8, H9): dates `2026-03-05`, `5 March 2026`,
`March 5, 2026`, `5 Mar 2026`, or with a weekday, never a numeric d/m/y form; money `$1,234.50`, `1,234.50 USD` or
`$1,200` (whole dollars only), X in the same forms, never in cents; counts `14 days` / `fourteen days`. Values compare
by value, not by string (a narrative's {AMOUNT} is the record's slot); one cent = 1 in the integer value.

## 2. Samplers, shares, traps, balance

- **Samplers (H36).** They differ only by container and block order (R11, R12); all draw as below. S1 forward; S2
  boundary-first (every day, amount and window proposal on its boundary during the first 20 of the 40 docs draws); S3
  table-first; S4 update notice with the record before the versions; S5 held out (held-out packs, edit-list
  container, held-out skins, registers and wordings; mixdev only).
- **Cards and packs (H34, H35).** 8 cards per training sampler (32; card = seed mod 8) and 4 for S5 (card = seed mod
  4); about 28 rows each. One pack per card: card c of the i-th training sampler (S1-S4 = 0-3) uses training pack
  (8 i + c) mod P; S5 card c uses held-out pack c mod P. `T24Plugin()` deals the frozen pool (pools/packs.json, sha
  checked against pools/MANIFEST.json; 75 training + 4 held-out packs, a seeded split of the admitted packs, section
  3.4, in file order), so the 32 training cards use 32 different packs (>= 25 packs, spec 3.0). The 10 + 2 code
  stand-ins serve tests only (`packs=STANDIN_PACKS`). Per-card label-bit rate in [0.2, 0.8], antithetic pairs (mean
  exactly 0.5).
- **Skins (v2.2).** One narrative skin per unit, dealt stratified and label-blind from the seed and sampler only
  (register round robin, then the skin by cycle; Mode F documents share the deal): <= 6 rows per skin and <= 15% per
  register on a run of consecutive seeds (spec 3.0), Mode F <= 25% of rows. The card style (R9) is drawn the same way.
- **Draw order (H23).** Question form, then the row's label bit (yes/no rows: gold yes; ch_v2 rows: "the outcome
  changes"; the ch_v2 gold role is drawn later), both from a 3-d low-discrepancy sequence (label bit 50 +- 1
  percentage points within every form at 10,000 draws); then (edit kind, case mode) from the table of the
  materiality label; then the docs (clause set independent of the mode: each kind forces its own clause, a limit
  edit an unchanged special clause, and one more clause from its mask sources); then the target outcome under V2;
  then boundary-biased case values, kept only when they realise the mode and that outcome. Bounds (H32): 40 docs
  draws x 60 case proposals; the V2 target is dropped on the last 10 docs draws; if nothing fits, `sample` raises and
  the seed is skipped and logged. Target and mode are draw filters only; gold is solver A (R19, H31).
- **Modes (H33).** flip (outcome changes); untouched (the edited clause takes no part for this case in either version:
  other category, other condition, the date outside the special window, a special limit that covers the case for a
  base-limit edit); same (it takes part and its own check, late / amount fails / excluded / condition applies, gives
  one result in both versions); masked (that check differs but an unchanged clause makes both NEG); cosmetic. Anchor
  and amount edits are never untouched (the count always uses win.A; an amount rule always takes part).
- **Plan.** Changes: anchor 40, limit 12, amount 12, alt 12, excl 10, override 14 (all flip). No change: cosmetic 16;
  untouched alt 10, excl 10, override 16, limit 8; anchor same 12 / masked 8; limit same 4 / masked 2; amount same 6
  / masked 2; alt, excl masked 2 each; override same 1 / masked 1 (shares in % of each label).
- **Traps (shares of all rows, on 2,000 training specs).** The outcome changes on 50% (48-52%; H40). Cosmetic or
  untouched 30% (spec: 30%); anchor changes that flip 20% (spec: 20%); date window that excludes the case about 5%;
  masked about 8%; a day count on a boundary (limit or limit + 1) about 49%; an amount within one cent of a bound 47%.
- **Balance (H24).** Gold yes is 50 +- 2 percentage points of the yes/no rows (spec 3.0 cells; each form 50 +- 1 by
  construction, Draw order); yes/no rows are 45-55% of the family after partners; ch_v2 gold role (the outcome under
  V2) uniform within each option bucket k (2 or 3; k = 2: POS / NEG 50 / 50, k = 3: 1/3 each), within +-3 pp over all
  choice rows (bases, equiv partners, twins; v2.2: a role prior would beat the G6 bar), gold position uniform within
  each; a ch_v2 twin aims at a label-blind target role drawn from the roles V2 can give other than the base row's;
  P(change | outcome under V2) within 0.45-0.55 for POS and NEG. Edit length does not predict the label: changed lines, clause
  counts, their difference, row length and reordering each give a best single-threshold accuracy <= 0.55. Edit kind
  does: cosmetic is never a change (by definition), anchor edits change the outcome 67% of the time (the spec's 20%
  anchor-flip quota); recorded as an open issue for G6.
- **Overlay.** Complement on 40% of yes/no bases (>= 20% of yes/no rows; about 65% non-syntactic); minimal-edit twin
  tried on 48% of bases, kept when one slot flips the answer (20-25% of rows); equiv on 10% of bases (5-10% of rows;
  another skin and versions container). Units hold at most 3 rows. No attack twins (everyday tier).
- **Relations.** Twin (one slot; answer predicted from the edited construction): the request date onto a limit or one
  past it (skipped when it would fall before d2; H39), the amount onto a bound or one cent off, the category, the
  condition, or the revised value of the edited clause (limit, amount X, special N; never back to V1's value). G4
  (answer unchanged): rename the customer, shift every date by 35 days and every amount by 100 cents (clause S, E and X
  shift too; H38), reorder the revised version, swap an unmentioned category.

## 3. Haiku tasks (after A38; Haiku never sees a question, option or gold; files and counts in haiku/author/TASKS.json)

1. **Clause paraphrases** (lexicon forms, kinds window / comparator / other): one line, no period at the end, starts
   with a capital letter and never with a slot; keeps exactly the slots of its meaning: win {N, A}; amt {M, X};
   exc {C}; alt {K, O}; ovc {C, N}; ovd {A, S, E, N}. At least 6 admitted per meaning (G-LEX 2/2; 3/3 for win, ovc,
   ovd). Negative-surface amount forms ("cases whose ... do not qualify") are wanted. An ovd form states inclusivity
   itself ("both dates included", "inclusive", "through"): never a bare "from {S} to {E}", "between {S} and {E}" or
   "until {E}" (H15). A win form keeps day N on time (no "before {N} have passed"). Label words are forbidden.
2. **Narrative skins** (Mode T; >= 8 registers: memo, email, chat, ticket, JSON, YAML, letter, log, form; held out:
   transcript, voicemail): keep `{CUSTOMER}` and may use `{CASE_ID}`, `{CAT}`, `{COND}`, `{AMOUNT}`, `{REQ}` (never
   `{D1}` / `{D2}`: their meaning is pack-specific), which read the same as the record; add no fact; no blank line;
   no number, date, relative-time word, quantifier, modal, hedge, status word, negation, policy-version talk or label
   word (change, same, different, affect, matter, any outcome name). Mode F (<= 25% of rows): free-form documents
   from a brief holding the customer only (G-SL `lint_freeform`, G3-H). The customer is the person who raised the
   case: the document's writer or subject, never only its addressee (an e-mail or letter names them in its sign-off
   or a self-introduction, never in its greeting); G3-H field `customer` = that person (null when unnamed). A G3-H
   template is one register under one authoring prompt (its sha): >= 98% each, else quarantined (v2.1).
3. **Question wordings (H25).** One shared pool per form (no per-card pools). Each wording is <= 2% of the family's
   rows (spec 3.0, G11), so a form needs >= row share / 2% admitted training wordings: measured row shares ch_v2 50%,
   yn_changes 22%, yn_same 9%, yn_not_change 8%, yn_fail_change 7%, yn_dneg 6% need >= 25 / 11 / 5 / 4 / 4 / 3 (52,
   above the floor of 30); admission targets 40 / 16 / 8 / 8 / 8 / 6, each card's rows use >= 5, plus a held-out set
   per form for S5. No slot; each names the outcome for this case (H20); R16 counts kept; admitted by G-LEX to
   `q.t24.<form>`.
4. **Domain packs (H35).** T24's own pack tasks (80 everyday settings) in the R2 format, then `check_domain`,
   label-word collisions, dedup and G13-seed; a seeded split keeps 4 held out and >= 32 for training. The pack tasks
   forbid the materiality words and question strings but not outcome words, because a pack defines its outcome names.

## 4. Ambiguity listing

Own points (v1): (1) "within N days": is day N on time? (2) does a special clause move the count? (3) "below X do
not qualify" at X; (4) three inclusive window forms; (5) failed check + condition: NEG or ALT? (6) is a rewording a
change? (7) "fail to change"; (8) yn_dneg; (9) ch_v2 without V2's alt; (10) special limit for an excluded category;
(11) amount exactly at X. Haiku pass `amb:T24`: H1 cosmetic = zero or one edit; H2 clause multiplicity; H3 ovd.A vs
win.A; H4 day zero; H5 calendar days; H6 "within" two-sided; H7 N, S, E ranges; H8 money forms; H9 date forms;
H10 closed edit list; H11 "after the update"; H12 2/2 vs 3/3; H13 negation cues, which strings; H14 slot O; H15 bare
"from S to E"; H16 card text, bullets; H17 table special cell; H18 update notice in full; H19 diff rules; H20 object
of "changes"; H21 dneg / fail mapping; H22 never-gold ALT; H23 "gold" in draw order; H24 balance units, buckets;
H25 wording arithmetic; H26 k_syn, k_all; H27 ignore_exception; H28 count_day0 / off_by_one_late; H29 which
endpoints; H30 models that do not apply, role closed; H31 A / B / target disagree; H32 retry bounds; H33 "agrees",
untouched kinds; H34 S5 cards; H35 packs vs cards; H36 "record-first"; H37 S-id clash; H38 G4 constants; H39 twin
before d2; H40 change share; H41 five families; H42 outside terms; H43 freeze status; H44 parsers vs readers; H45
which printed count.

## 5. Resolution (Claude, 13 Oct 2026; v2)

- Own 1-3, 5-9, 11: R4-R5, R7-R8, R13-R14 as written; 4: section 3.1 (H15); 10: a generator invariant (`_docs`).
- **Code changes (v2):** the card's third and fourth bullets (R9 box; both solvers): the special-limit bullet names
  both scopes and the inclusive window (H3, H15); the day-count bullet says calendar days, printed in the record,
  counted from the time-limit date (H4, H5, H6, H45). `domain_for`: one pack per card (H35). `check_domain`: title,
  date-field and label-word checks (R2; the held-out stand-in title is now "booking amendment policy"). A new test
  asserts the construction outcome equals solver A (H31). Nothing else changed in the generator or the solvers.
- Stated in R1-R20 and the box: H1 (R1), H2, H3, H7, H14 (R4), H4, H5, H6 (R5, box), H8, H9 (value forms), H10 (R6),
  H11, H20 (R8), H12 (R7), H13 (R2), H16 (box), H17, H18, H19 (R11), H21 (R14), H22 (R13), H26 (R16), H27, H28, H29,
  H30 (R15), H31 (R19, R20, section 2), H41 (R18), H45 (R10, box).
- Stated in section 2: H23 (Draw order), H24 (Balance), H32 (Draw order), H33 (Modes), H34, H35 (Cards and packs),
  H36 (Samplers), H38, H39 (Relations), H40 (Traps). Section 3: H15 (3.1), H25 (3.3), H35 (3.4).
- H37: semantics rows are R1-R20; S1-S5 name samplers only. H42: the header names each outside term's source.
- H43: the freeze takes effect with this v2 (the post-pass text); the sha in the plugin is this file's.
- H44: G-LEX admission is a reading test by independent blind Haiku readers (each picks the meaning from the closed
  list, kit lexicon), not parser agreement; G5-H (two blind Haiku solvers, Claude adjudication) reads whole rows.
  No separate human check in v1.
- **v2.1 (13 Oct 2026, Claude; Mode F only, after the G3-H reads):** in 10 of the 20 v1 e-mails (task free-a) the
  customer's name is only the greeting's addressee ("Hi <name>,"), so the writer is unnamed and the correct read is
  null (10/20). Section 3.2 now states the writer rule and what a G3-H template is. In v1 one prompt serves every
  register, so template = register and the v1 e-mail template stays quarantined (all 20 dropped; nothing is re-read
  or re-scored). A new e-mail prompt (`redo2.py`, haiku/redo2/) is a new template that must reach 98% on its own.
  Gold, the G3-H field and its text, the G3-H read prompt and every bar are unchanged.

- **v2.2 (14 Oct 2026, Claude; Stage B pilot verdict F1-F4; no bar loosened, no label changed):** F1 packs: the pool
  is wired in (section 2). F2 length (mean 937.5 vs 800): the card is rewritten and placed (R9 boxes; "replaces only the
  limit" also states what reader B misread, row a0009) and a short style is drawn on 15% of units. F3 role balance: section
  2 Balance, the ch_v2 twin target role and the V2 outcome weights. F4: the skin deal (section 2). Wording polarity (kit
  item 3): yes/no wordings pass `c2_kit.polarity` P1-P3 with the family's antonym lexicon (same, unchanged, identical ...);
  the strict-frame review (P4) quarantines the one held-out yn_dneg wording "Would an auditor not agree that nothing ...
  changes ...?" (negative frame over an embedded negation) and keeps the 19 yn_not_change "Does the revision not change
  ...?" frames (one syntactic negation, polarity -1; both G5-H readers matched gold on every such row). R1-R8, R10-R20
  (R9: card text and placement only), the samplers, shares, Haiku tasks and every bar are unchanged; pools/ stays frozen
  at the v2.1 freeze (its MANIFEST records sha 652dd74a).

Recorded choices: one edit per pair (multi-edit revisions are not in v1); no version effective dates; inverted,
few-shot and masked-label variants are not in v1 (the short card is, from v2.2).
