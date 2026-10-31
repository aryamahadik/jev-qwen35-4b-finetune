# F5 G0 spec: hard and negated yes/no (resolved after the G0 ambiguity review and re-review rounds 1-5; FROZEN)

**XF (3 Oct 2026):** cross-family alignment applied and folded into sections 0-10, which now state each XF rule
directly; section XF at the end records the shared rules. No earlier text states a different rule.

Date: 3 Oct 2026. Author: G0 drafter, family F5; resolver pass the same day (all 38 review ambiguities F5-A01 to
F5-A38 and all 19 spec conflicts K01-K19 resolved); second resolver pass the same day (re-review round 1: all 19
ambiguities F5-R1-01 to F5-R1-19 and all 4 spec conflicts SC1-SC4 resolved); third resolver pass the same day
(re-review round 2: all 21 ambiguities F5-R2-01 to F5-R2-21 and spec conflicts SC5-SC6 resolved; tables at the end,
after the XF alignment); fourth resolver pass the same day (re-review round 3: all 12 ambiguities F5-R3-01 to
F5-R3-12 and spec conflicts SC7-SC8 resolved in the body); fifth resolver pass the same day (re-review round 4: all 7
ambiguities F5-R4-01 to F5-R4-07 and spec conflicts SC9-SC10 resolved in the body); cross-family fixes CF-3 and CF-4
the same day; final resolver pass (re-review round 5: all 8 ambiguities F5-R5-01 to F5-R5-08 and spec conflict SC11;
cross-family issues CF-4 (rewritten: XF18 closed with no amendment) and CF-5 (XF10); PREREG ruling A16.1 (g) as
F5-R5-09; the CF table and the round-5 table at the end), after which this file is **frozen** (`c_src/F5/G0_FROZEN.json` holds its sha256; read-only for
everyone). Section 0 is the
1-page G0 spec; sections 1-10 are its normative annex. Inputs: `C_DATA_SPEC.md` v4 (0-2, 2.1, 2.2
F5, 2.3, 2.4, 3.1-3.H, 5, 6, 7, 8, 9 isolation rules, 10, 11, 12), `C_TRAIN_RECIPE.md` (3, 7.2),
`LICENCE_REGISTER.md` rows 1-3, 16, 17 and sections 3, 6, `PREREG_FINAL.md` amendments A15, A16 and A16.1, the
formats-1 card module (`fmt1/card.py`: `render_and_check`, `loader_check`), `decoder_io.py` and
`train_decoder.check_rows`. Where this file and `C_DATA_SPEC.md` v4 disagree, the spec
wins; the few places where the spec's own rules cannot all hold for F5 are listed in the K and SC tables with the
reading used.
**Status: G0 final (frozen).** G14 is met (PREREG A15: the sealed suite's sha256 was committed before any C data).
Packs, cue templates, card renderings, wording and style pools, generator code and rows are built after this freeze
and follow it; none of them may change this file. Section 3 states
*meanings*; the card sentences that carry them are written after G14 (section 3.3). Placeholders: `<P>` a base
proposition, `<A>`/`<B>` entities or conditions, `<E>` an entity, `<X>` an action or event, `<Z>` a possession,
`<N>`/`<q>`/`<m>`/`<T>`/`<C>` numbers (`<q>` a stated count in a quantifier or graded cue), `<D>` a date, `<S>` the
authoritative source, `<v1..vn>` listed values.

**Symbols (each has one meaning in this file; F5-R1-19).** **k** = the question-side negation-cue count (sidecar field
`k_neg`; section 4); it is never a value count or a quantifier number. **n_vals** = the size of a SEM-17 value set.
**t_txt** = the number of text-side negation-cue instances in the rendered text (section 4). **j_q** / **j_t** =
surface L_neg entries in the question / text (3.4). **r_card** = a card's drawn row-level yes rate; **a_card** = the
A-row v(P) rate and V-row gold rate that realizes it; **f_card** = the card's share of training bases with an attack
twin V'; **p_card** = the card's share of bases in contrast pairs (all section 8). **Base depth** = per-sampler depth (section 5).
**k_syn** / **k_all** = the shared negcount counts (XF02): k_syn = L_core tokens in the question, k_all = j_q.
**Row bin** = a row's own crowd difficulty bin (`meta.difficulty_bin`); **base bin** = the bin of the base's hardest
row (sidecar `base_bin`; section 8).

---

## 0. One-page spec (the G0 deliverable; sections 1-10 are its normative annex)

- **Generator.** F5, hard and negated yes/no, one generator in `c_src/F5/` (code after this freeze only). Every row is
  a yes/no row (raw `qtype` "noul", `gold` 1 = Yes, 0 = No; the loader shows the options Yes / No); no abstain, no
  choice, no ordinal rows, so the card is always printed whole and every row passes fmt1 `loader_check` (F5-R5-09).
  Only determined bases (every model of the record plus the card
  axioms agrees); undetermined or inconsistent bases are rejected, never relabelled.
- **Samplers (shares of bases).** S1 rule-case incl. F2 amount and date shapes 22%; S2 event log 20%; S3 fact graph
  20%; S4 records, closed only 20%; S6 public human-gold text (SQuAD 2.0, MuSiQue, 2Wiki, GHC, EDOS) 18%; S5 thread,
  held out (mix-tuning dev only). Base depth 1-2 by default; 3 is deep.
- **Rows per base (4.2).** Unit 1 (one `call_id`): A affirmative (k = 0, j_q = 0); N `complement` (k = 1); D `equiv`
  (k = 2). Unit 2 (own `call_id`): V, a scope-shift or implicit-cue variant (k = 0-3), plus attack twin V' (`inv`) on
  a per-card share f_card of training bases (about 20% overall). Held-out S5 bases have no V' (4 rows each).
  **Contrast pairs (XF03):** about 29% of S1-S4 bases come in pairs whose second base changes one input fact and
  flips the gold of every A, N, D and V row; about 22.5% of F5 rows (asserted 20-25%) sit in these contrast sets.
- **Gold.** Yes iff the question's logical form is true of the structure under the card's semantics. Solver A and an
  independent solver B of a different paradigm agree on 100% of rows, after a round-trip parse of the rendered text.
- **Size.** r1 3,600 rows (about 860 bases). r2 cumulative placeholder 7,200 at x1 (round 2 is a superset); the probe
  sets the multiplier (x0.67 / x1 / x1.5) and F5 stays <= 12% of own rows, so no sampler reaches 2,500 rows at its target share (the cap is asserted on the
  final selected set, section 8).
- **Balance.** P(yes | k) = 0.50 +/- 0.02 for k = 0-3; G10 aggregate 50 +/- 2 per wording x row bin x k_all (XF02);
  double negation (negcount k_all >= 2, XF02) about 40%, 2.1 quotas on negcount k_syn; per-card r_card drawn
  uniformly from 20-80% and realized exactly (section 8); "Yes = bad" 50 +/- 5 of all yes/no rows by monotone polarity, no-polarity rows <= 5% through the section-8
  no-polarity budget (XF04); easy <= 25%, medium >= 45%, hard <= 30% (row bins, final set).

**Semantics table (every line below is printed on the card whenever its trigger fires; full wording in section 3.2).**

| Topic (spec G0 list) | One semantics, as the card states it | Key |
|---|---|---|
| World | Closed: the record is complete, names every <entity type>, gives or marks not recorded every number, date and category detail, and lists every statement made; an unstated positive statement is false, and a statement made negative by "not" or a negative prefix holds exactly when its positive form does not. Open: facts may be missing, but the record names every <entity type>; unstated facts are unknown. In both worlds, whether an action is required or permitted is set by the deontic line, ahead of the world line; in a role and action table, "required" = must (so also permitted), "permitted" = may and need not, "forbidden" = must not | SEM-02, SEM-03, SEM-24 |
| "unless" (rule text only) | B false gives A; B true says nothing about A, so A's atom is then set by the other rules and the world line, and a required or permitted status by SEM-24 | SEM-05, SEM-24 |
| "only if" (rule text only) | B false gives not-A; B true does not by itself give A (A's atom, or a deontic status, then set as for "unless"); an "only if" rule carries no "unless" or "except when" | SEM-06, SEM-24 |
| "if ... then" (rule text only) | B is enough for A; no biconditional; a rule's conditions are the parts of its "if" clause joined by "and" | SEM-07 |
| "at least" and other bounds | at least / no fewer than / N or more include N; more than / over / above exclude N; between includes both ends | SEM-08, SEM-09 |
| "or" | inclusive; "either ... or ..., but not both" is exclusive; bare "either ... or" is never used | SEM-10 |
| Date ranges | whole days; before / after exclude <D>; by / on or before / through include <D>; "as of <D>" = end of <D>; "<N> days after <D>" = the <N>th day after <D>; a range in a question about an event asks whether at least one such event falls on some day of it (one is enough), and a "not" over it says that no such event does; a range over a single date asks whether that date falls in it; a state is asked only "as of <D>" or with no stated time | SEM-11 |
| Log states, renewals | holder, status and validity are separate states; an entry counts from its date and changes only the state it names; a state holds through the day before the next entry that changes the same state; an item has no status before its first status entry; validity comes only from a renewal, runs through its last valid day, and a newer-dated renewal replaces the last valid day; a lapse changes neither holder nor status; an entry saying something never happened, no longer holds or still holds is a statement and sets no state | SEM-33, SEM-17, SEM-26 |
| Missing values | "not recorded" or null = some value the record does not give, on a complete record too (never decisive: also against other records' values, every value the case names and one unused value); a blank yes/no entry on a complete record = no; closed records never omit a key or attribute | SEM-04, SEM-02 |
| Rounding | none; values compared exactly as written | SEM-12 |
| Ties | "more than" false on equal; superlatives shared by every tied member; superlatives only as "has the highest <X>" or "the only one with the highest <X>" | SEM-13 |
| Units | every quantity has its unit; only same-unit comparisons | SEM-14 |
| Exception precedence | an exception ("unless" or "except when" attached to an "if ... then" rule, or "except when" attached to a rule with no condition) stops its rule only; it never gives the opposite outcome; no two rules conflict | SEM-15 |
| Groups | quantifiers, "only", "other than", superlatives range over exactly the group the question names; "Did any ...?" and "someone / anyone other than <A>" = at least one ("any" only in a direct question or in "not / hardly / scarcely any") | SEM-13, SEM-22, SEM-23 |
| Time scope | in a question, "never" = no day from the period start through the asked day ("as of <D>" sets it; default <D_end>); in the record, "never" and "failed / refused to" without "by <D>" (anywhere, dated entries included) = no day of the covered period; "lacks / is without / is free of" only on cards with no dated entries | SEM-19, SEM-26, SEM-27 |
| Authority and stance | only <S> makes facts true; each CORRECTION or VOID names an entry by its own author; a correction changes only a value in the entry or message it names, which keeps its own date, and is not itself a message about the fact; a statement about <P> states <P> or that <P> is false; a stance question never names <S> and asks about the party's latest remaining statement after its own retractions and corrections | SEM-16, SEM-20, SEM-31 |
| Answer convention | answer Yes iff the question's statement, read exactly as worded, is true | SEM-01 |

---

## 1. Skill, decision form, size

- **Skill.** Answer yes/no correctly when the question or the text carries negation, double negation, scope shifts,
  implicit negation (fail to, lack, deny, refuse, rule out, hardly, no fewer than, unless, other than), quantifiers or
  modal negation. The hard part is polarity, not reasoning depth: every base is shallow (base depth 1-2; 3 = deep;
  base depth is defined per sampler in section 5, and `meta.depth` / `meta.deep` in section 8).
- **Decision form: yes/no only (F5-R5-09, PREREG A16.1 (g)).** Every F5 row is a raw yes/no row: `qtype` "noul",
  `gold` 1 (Yes) or 0 (No) as a number (never the string "Yes" / "No", which `train_decoder.check_rows` refuses), no
  `options` list; `decoder_io` shows the options Yes / No and the trainer draws the letter order. No choice rows, no
  abstain option, no ordinal rows, no `option_level`. A base whose truth value is
  undetermined is never an F5 base (it belongs to F6). Label-check form: 0 rows.
- **Where each part goes (A16.1 (g)).** F5 has no choice rows (inverted cards are yes/no rows, K05), so the A16.1 (g)
  choice-row placement (only "- option: definition" card lines are shown) never applies to F5. On a yes/no row the
  served layout (`decoder_io`, cygnet, `schema_branch_mark`) prints the card whole under "Definitions:", so: the card
  (the SEM lines, few-shot examples, and on inverted cards the case or record list and the named rule) goes in
  `card`; the record M (rules, log, facts, records, the S6 wrapper and quoted source, any attack span) goes in
  `state`; the instruction wording and the question (truth frame plus cue templates) go in `instructions`. No card
  line starts with "- Yes: " or "- No: " (decoder_io would glue it to an option). Every row is built through fmt1
  `card.render_and_check` (qtype "noul") and passes `loader_check` with its `must_show` strings and
  `train_decoder.check_rows`; a row that fails is a generator bug (fix, regenerate). Training rows take format styles
  only through `pool.training_style` (the formats-1 held-out styles go only to S5 and the probe, never to a training
  row).
- **Size.** r1 3,600 rows, about 860 bases. **Round 2 is a superset of round 1** (spec 0, spec 2.2, recipe 7.1), so
  every r2 figure in this file is **cumulative** and includes round 1's 3,600 rows. r2 = 7,200 rows (about 1,710
  bases) is a **placeholder** for x1. The r2 share is 8% x the probe multiplier m, applied to all round-2 own rows
  (cumulative reading; F5-R1-18): F5 r2 total = 8% x m x 90,000 before clipping = 4,824 rows at x0.67 (1,224 new),
  7,200 at x1 (3,600 new), 10,800 at x1.5 (7,200 new). It is then clipped to [0.5/13, 12%] of round-2 own rows
  (90,500: 3,481 to 10,860 rows) and renormalized (recipe 7.2), and the final F5 share stays <= 12% of own rows
  (spec 2.1 per-family maximum); the clip and renormalization are re-applied until every family is inside
  its bounds. **Per-sampler cap** (2,500 rows over both rounds, i.e. of the cumulative r2 total, spec 2.1): at the
  12% maximum (10,860 rows) the largest sampler, S1 at 22%, has 2,389 rows at its target share, so no sixth sampler
  is needed; selection drift (+/- 2 pp) could carry S1 past 2,500 only at that maximum, so the cap is asserted per
  sampler on the final selected set, with the section-8 remedy (F5-R2-14). Rows per base: about 4.2 (attack twins on
  a per-card share f_card of training bases, about 20% overall, section 8; S5 has 4.0). Generate 1.5x bases. Cards >= 80 / 150. Packs >= 80 / 150, one per card: no two F5 cards share a pack (XF09).
- **Row length.** Every row < 1,900 real tokens, counted on the served prompt (`decoder_io.user_msg`, cygnet,
  `schema_branch_mark`), which prints `instructions` twice (A16.1 (g): token caps count `instructions` twice), plus
  the card, the state and the layout lines; a base that would exceed is skipped, never cut. Reason (spec 2.1,
  G15): unit 1 holds 3 rows, and a unit with any row of 2,000 tokens or more may hold at most 2 rows; 100 tokens are
  margin. So F5 has no long units.
- **Units.** Each base gives one shared `group_id` (one per contrast pair, below) and two relation units:
  - unit 1 (one `call_id`, 3 rows): **A** affirmative `<P>`; **N** negated, `complement` of A; **D** double-negated,
    `equiv` to A;
  - unit 2 (own `call_id`): **V**, a scope-shift or implicit-cue variant labelled by the program, no relation term
    (the allowed V forms per sampler and dataset are listed in section 4, "V rows").
    On a per-card share f_card of training bases (about 20% overall; never S5; section 8) V gets an attack twin **V'**
    (`inv`, label unchanged) in the same unit, so unit 2 has 2 rows there (K04). That gives the spec-2.1 attack quota of
    about 5% of rows.
  - **Contrast pairs (XF03, CF-4).** On S1-S4, a share p_card of each non-inverted card's bases (section 8) comes in pairs: base B
    and its twin base B', which keeps B's card, wording, question templates for A, N, D and V, and every input except
    one change to M (section 8) that flips the gold of all four rows. Each base keeps its own two units and
    `call_id`s; the pair shares one `group_id`. These pairs are F5's contrast sets in the XF03 sense.
- **Code layout (after this freeze only).** One generator in `c_src/F5/`: five training base samplers (S1-S4, S6) + held-out
  S5, one polarity transformer, one renderer, an independent parser, solver B. F5 re-implements shallow versions of the
  F1-F4 and F9 structure types named in spec 2.2 (F1 and F2 in S1, F3 in S2, F4 in S3, F9 in S4; F2 as the S1 amount
  sub-shape and the S2 date offsets, section 5); it imports no other family's generator, so a bug there cannot reach
  F5 labels. Shared
  code is limited to `c_src/common/` (loader, deny-list, provenance, record ledger, negcount), the formats-1 `fmt1`
  module (styles, card rendering, `render_and_check`, `loader_check`) and, for G15 only, `decoder_io` and
  `train_decoder` (F5-R5-09).

## 2. What the program computes as gold

1. A sampler draws a structure M (rules, log, facts, table, or a public record) and a base proposition `<P>` with a
   determined value v(P) under the card's semantics (section 3). **Determined** means every model of M plus the
   card's axioms gives P the same value (the solver-B criterion), in both worlds. M must be satisfiable and its rule
   graph acyclic (asserted by both solvers). Solver A must decide the base too; a base solver A cannot decide is
   dropped (logged count), never labelled by solver B alone.
2. **Text side vs question side.** Negation cues in the text (rules, log entries, facts, records) are part of
   rendering M: they fix v(P) through M and never enter the question's operator chain. The polarity transformer
   builds the question's logical form LF = a chain of question-side operators applied to `<P>`. Each operator comes
   from a cue template (section 4) with a declared LF signature, a declared negation-cue count and a declared
   monotonicity per argument slot. Per row the sidecar records **k** (`k_neg`, question-side negation-cue count,
   section 4), **t_txt** (text-side negation-cue instances, section 4), **j_q** and **j_t** (surface L_neg entries in
   question and text, 3.4) and the base depth (section 5).
3. **Gold** = Yes iff LF is true of M under the card's semantics. Solver A and solver B each evaluate LF directly on
   M (S1-S5) or by truth table over the human base label (S6). For chains of truth-functional operators (contradictory
   NOT, negative implicatives, privatives, affixal negation on SEM-18 predicates) the identity gold = v(P) XOR (k mod
   2) is asserted as a check; it is never the labelling method. For N and D the generator also asserts gold(N) = 1 -
   gold(A) and gold(D) = gold(A) by direct evaluation. Structural operators (quantifiers, bounds, dates, exceptives,
   modals, connectives, value sets, aspect, "barely", decoys) are evaluated on M only and are allowed only on S1-S5.
4. **Soft rows.** In round 1 every S6 base is hard (section 5, S6): no F5 row carries `meta.teacher`. The rule for any
   later amendment that admits vote shares: `gold` = 1 if p' > 0.5 else 0, `meta.teacher` = {"yes": p'} (the yes/no
   form `train_decoder` reads), p' = p when k is even and 1 - p when k is odd (`teacher_src` "human_votes"; spec 2.2
   "the negated row gets 1 - p").
5. **Undetermined or inconsistent guard.** If KB and LF and KB and not-LF are both satisfiable (undetermined), or both
   unsatisfiable (inconsistent KB), the base is rejected; at row level either case fails G2. Never relabelled.

## 3. Semantics table

### 3.1 How lines reach the card
- **Print by trigger, never by decisiveness.** A SEM key is printed when its **trigger** fires. A trigger is either
  (a) a phrase use that the trigger table below maps to the key, found by the G3 parsers in the **program-written
  text or question** of any row of the base (rendered M, questions, 2Wiki declaratives), or (b) one of the structural
  triggers below. **Card lines never trigger a key, and quoted source text (S6 passages, paragraphs, posts and the
  quoted source question) never triggers a key** (F5-R2-07, F5-R2-08), so the trigger set needs no fixed point. S6
  wrapper text holds no trigger-table phrase, number or date (asserted). Whether the line actually decided the label
  never changes what is printed.
- **Trigger table (F5-R2-08; G3's card parser uses the same table).** Each phrase use maps to exactly one key. Phrases
  are matched longest first, as in 3.4, and each use is classed by its parsed role (status value, stance verb, rule
  connective, quantifier, ...), never by the bare string:
  - SEM-01: truth frames; C1 "not" / "no" as sentential or verbal negation; C2 frames; "false".
  - SEM-05: "unless" in a rule with no "if" clause (the form "<A> unless <B>"). SEM-15: "except when" attached to any
    rule (with or without an "if" clause), and "unless" attached to an "if ... then" rule (F5-R4-07). SEM-06: "only
    if". An "only if" rule carries no "unless" and no "except when", and a rule holds at most one "unless" or "except
    when" (lint at bank build; asserted by the S1 generator), so every exception phrase fires exactly one of SEM-05
    and SEM-15. SEM-07: "if ... then", and "of the conditions of <rule>" in a question (F5-R3-08; its "at least <q>"
    still fires SEM-08).
  - SEM-08: the numeric bound words of SEM-08, "no fewer than", "no more than", "not less than" and "not more than"
    included. SEM-09: "at least half", "more than half".
  - SEM-10: "or", "either ... or ..., but not both", "neither ... nor", "not both ... and".
  - SEM-11: every SEM-11 date phrase ("no earlier than", "no later than", "not before", "not after" and "<N> days after
    <D>" included); the
    "by <D>" of a C3 cue belongs to SEM-19 (its date still fires SEM-11, below).
  - SEM-13: superlatives, "the only one with the highest (lowest)", two-entity comparisons ("more / fewer <X> than
    <B>").
  - SEM-16: CORRECTION, VOID. SEM-17: "one of" and value tests on a value-set attribute. SEM-18: a pack-declared affixed
    word, litotes.
  - SEM-19: the C3, C4 and C5 phrases. SEM-20: a stance verb ("denied", "ruled out", "confirmed") with a named party
    and a proposition, and any statement attributed to a named party. SEM-21: a value of a status field from the
    card's declared status list ("denied", "refused", "rejected" as status values).
  - SEM-22: "every", "all", "some", "any", "no" as a determiner, "none of", "not any", "not every", "not all", "No <A> is
    <B>". SEM-23: "only", "other than", "all except". SEM-24: the SEM-24 modal phrases, and the cell values
    "required", "permitted" and "forbidden" of an S1 role and action table (F5-R5-03). SEM-25: "hardly any",
    "scarcely any", "few", "barely". SEM-26: "never", "no longer", "still". SEM-27: "as of <D>". SEM-28: "not only ...
    but also". SEM-33: "<renewed / valid> for <N> days" and state-setting log entries.
  - S6 overrides: on SQuAD 2.0 and MuSiQue cards the SEM-29 phrases and the C3, C5 and C6 cues ("fails to answer",
    "lacks an answer to", "is unanswerable from") map to SEM-29 only; on 2Wiki cards "before", "after", "older",
    "younger" and "first" in the declarative map to SEM-32 only. S6 program-written text holds no number or date
    (asserted), so every S6 card, full or short, prints exactly SEM-01 plus SEM-29, SEM-30 or SEM-32.
- **Structural triggers (F5-R1-07).** These keys have no operator word, so they print on structure:
  - SEM-01: every card. World line (SEM-02 or SEM-03): every S1-S5 card.
  - SEM-16 and SEM-20: every S2 card (any log has unauthored entries, which SEM-16 assigns to <S>, and may hold
    notices). SEM-20: every S5 card, and any S1, S3 or S4 card whose text holds a statement attributed to a named
    party (the S1, S3 and S4 generators assert they hold none, so in practice SEM-20 prints on S2 and S5 only).
  - SEM-33 and SEM-27: every S2 card. SEM-27 and SEM-31: every S5 card. SEM-27 also on any card where a C3 or C4
    phrase or a SEM-26 phrase occurs, or whose text holds a dated entry (an S2 log entry or an S5 message); a C5 phrase
    alone does not print SEM-27 (F5-R2-05).
  - SEM-04: any blank, "not recorded" or null entry in the text (XF06: "-", "n/a", "N/A", "TBD" and "?" are banned in
    every family).
  - SEM-11: any date in the program-written text or question.
  - SEM-12: any number in the program-written text or question that is a value (a quantity, count, amount, threshold,
    <q>, <N> or day count); digits inside a date, an ID or a name are not numbers (F5-R2-08). SEM-14: any quantity with
    a unit in the program-written text or question.
  - SEM-17: any attribute whose values come from a declared value set (one SEM-17 line per such attribute).
  - SEM-24: any card whose text has a role and action table (F5-R5-03).
  - SEM-29 / SEM-30 / SEM-32: every S6 card of the matching dataset.
- **"Used" means "triggered".** The generator, the card parser (section 6) and G10 all work with the trigger set; no
  check ever asks which key a solver used.
- **Card form is chosen once per base.** All rows of a base (A, N, D, V, V') show the identical card, so twins differ
  only in the question. **Full card** (about 85% of bases): SEM-01, the world line, and every SEM key that the card's
  sampler and cue families can use (a fixed set per card; the generator asserts that the base's trigger set is inside
  it). **Short card** (about 15% of bases, so about 15% of rows): SEM-01, the world line and every key triggered by any
  row of the base. F5 has no no-card rows (spec 2.1 allows "short or no"). A contrast pair (section 8) is treated as
  one base here: one card form, and on a short card every key triggered by any row of either base, so both bases show
  the identical card.
- **Card rule set (SC10; spec 2.1: two cards must differ in the domain pack and in the label schema or rule set).**
  Every F5 card has the same label schema (Yes / No), so any two F5 cards differ in their pack (XF09) and in their rule
  set. A card's **rule set** = its sampler; its world line (closed or open; on S6 the dataset line SEM-29, SEM-30 or
  SEM-32); its full key set (above; it follows from the card's own cue-family set, drawn per card); and its card
  constants: each declared value set (its values and n_vals), the declared status list (S2), the deontic table's role
  x action cells (S1), the SEM-25 constants <q> and <m> (S4, numeric S1), and on S6 its definition variant (the card's
  registered rendering of the dataset line, 3.3, and on GHC and EDOS its SEM-30 summary D; every variant has the same
  label function). Asserted at card build: no two F5 cards share a rule set, and two cards with the same sampler and
  world line differ in their full key set or in a card constant beyond pack words (n_vals of a value set, the size of
  the status list, a deontic-table cell, <q> or <m>); a clash redraws a card constant. Two S6 cards of one dataset
  differ in their definition variant, so a dataset has at most as many S6 cards as registered variants (more are
  written as in 3.3 when needed). Section 10 item 15 logs this reading.
- **World line.** S1-S5 cards show SEM-02 or SEM-03. S6 cards show no world line: SEM-29 (SQuAD 2.0, MuSiQue), SEM-30
  (GHC, EDOS) or SEM-32 (2Wiki) takes its place, and S6 is its own world cell in G10.
- **Lexicons.** Every operator word in program-written text comes from the closed lexicons in 3.4; anything else fails
  the template lint at bank build.

### 3.2 Table (normative meanings; the card must state exactly this meaning)

| Key | Topic | Normative meaning stated on the card | Generator rule / label effect |
|---|---|---|---|
| SEM-01 | Answer convention | Answer Yes if the statement in the question, read exactly as worded (every "not" and every negative word included), is true of the case; otherwise answer No. | Every row. *gen*: the matrix interrogative clause contains no L_core word (3.4): no "Isn't / Doesn't / Did ... not / Is it not the case / Has ... never / Is there no ...?" and no tag questions. **Only L_core negation must be embedded** (F5-R1-13): an L_core word sits only inside an embedded declarative after a truth frame. **The rule is per token** (F5-R2-09): an L_core token inside a multiword L_neg entry ("no fewer than", "no more than", "not less than", "not more than", "no earlier than", "no later than", "not before", "not after", "no longer", "none of", "not any", "not every", "not all", "neither ... nor", "not both", "need not", "must not", "may not", "is not permitted to", "does not have to", "is not required to", "did not manage to", "not only ... but also") is embedded too. The **matrix interrogative clause** is all of the question outside that embedded declarative, relative clauses included (F5-R2-17). Whether such tokens count toward k_syn is fixed once in the shared negcount (XF02), not here. Every other L_neg cue (one with no L_core token) may sit in the matrix clause ("Did <E> fail to <X>?", "Does <E> lack <Z>?", "Did anyone other than <A> <X>?", "Did <X> deny that <P>?"). **Truth frames** are a closed list of >= 8 frames of the shape "<frame> <embedded declarative>?" (e.g. "Is it true that ...?", "Is the following statement true: ...?"); the list is written after G14. A frame holds no L_neg entry (C2 cues are separate operators). Each frame is used on A rows as well as on N, D and V rows: the framed share per row type is equal within +/- 3 pp, the yes rate per frame is 50 +/- 3 (by construction), each frame passes 7.2 method 8 (a hit drops and replaces it), and G11's 2% limit applies to the full question template (frame x cue template). No conditional, hypothetical, "would", "could" or "should" in any question. Lint at bank build |
| SEM-02 | Closed world | The record is complete. It names every <entity type> in the case, gives every number, date and category detail of each of them or marks it not recorded, and lists every statement each party made. A positive statement that the record does not state, and that no rule makes true, is false: it did not happen and does not hold. A statement made negative by "not" or by a negative prefix (non-, un-, in-, dis-) holds exactly when its positive form (the same statement with that negation taken out) does not hold. A statement it does not list was not made. The one exception is a value the record marks as not recorded: it has some value the record does not give. | P false iff P is not in the least model; an unrecorded value is a free variable (SEM-04), never a closed-world atom. Rule graphs acyclic and stratified, so Clark completion (solver B) equals the least model (solver A). **Atom level** (F5-R4-01): what a rule gives when it applies is an atom or the negation of an atom, whatever the polarity of its written head ("<E> is not eligible unless <B>" gives not-eligible when <B> is false; "<E> is not charged only if <B>" gives charged when <B> is false). Only a rule that gives a positive atom makes it true; a rule that gives a negated atom never makes an atom true, and the generator asserts that the least model satisfies it (no rule gives the positive atom for the same case; SEM-15), so completion still equals the least model and, on a closed card, a non-deontic atom holds iff some rule gives it. **The card states this** (F5-R5-01): closed-world falsity applies to positive statements, and a statement negated by "not" or a negative prefix holds exactly when its positive form does not, so "<E> is not eligible unless <B>" with <B> true and no other rule gives not eligible for every reader. **Rule heads** (lint at bank build; F5-R5-01): the written head of an S1 rule ("if ... then", "unless", "only if" or unconditional) is a positive atom, that atom with "not", its SEM-18 affixed form, or a SEM-24 modal head; no other negative word ("no", "never", a C3, C4 or C5 cue) stands in an S1 rule head, so every negative head is covered by the card sentence. S3's "No <A> is <B>" universals are quantified statements read by SEM-22, not rule heads. Deontic status is set only by SEM-24 (below). Card-level choice; label balanced per world. **No omitted key or attribute** (F5-R3-07): on closed cards every number, date and category (value-set) attribute of every case (S1 prose included) and every field of every record or log entry (S2, S4; markdown, CSV, JSON, YAML, key-value and log lines alike) is rendered as a value or as "not recorded" / null, except the structural fields, which always hold a value in both worlds: an S2 entry's date, entry type, item ID and (on an action entry) named actor, and an S5 message's date and sender (F5-R5-05; the parser rejects an unrecorded, null or blank structural field, so no entry or message date is ever a SEM-04 free variable); a yes/no field in a record container is a value, null or blank (SEM-04); no key, column or such attribute is ever left out (G3 rejects an omission). A yes/no fact in prose (S1 case text, S3 facts) is a closed-world atom: stated, or false by this line. **Deontic status** (F5-R3-01): whether an action is required or permitted is set by SEM-24, whose card line says it applies ahead of this line; completion never decides "permitted" or "required" by itself |
| SEM-03 | Open world | The record may be incomplete about facts and events. It names every <entity type> in the case; only facts about them may be missing. Something it does not state, and that does not follow from what it states and the rules, is unknown, not false. | P (or not-P) is determined iff every model of the KB agrees. **Domain closure** (F5-R1-04): both solvers ground universals, quantifiers, counts, superlatives and exceptives over exactly the entities the record names, and solver B's determinacy check uses exactly that domain (no fresh individuals). Not-P can follow from an explicit negative fact, a listed value set (SEM-17), "only if" with the condition false, a "No <A> is <B>" statement, or the contrapositive of a strict rule. Undetermined bases rejected (section 2). No stance question (C7, question side) on an open card (F5-R1-01). An attribute an open card does not mention is unstated, so unknown by this line (F5-R3-07). Deontic status is set by SEM-24, whose card line says it applies ahead of this line, so an action no listed rule forbids is permitted, not unknown (F5-R3-01); it is unknown only when whether a listed rule forbids or requires it for the case is itself unknown, and such a base is rejected |
| SEM-04 | Missing data (XF06) | An entry marked "not recorded" (or null) has some value that the record does not give, on a complete record too: nothing in the record makes a statement about that value true or false. On an open card, a blank entry means the same. On a complete record, a blank yes/no entry means no. | *gen*: the cross-family marker table governs; "-", "n/a", "N/A", "TBD" and "?" never appear. On closed cards an unrecorded value of any kind is written "not recorded" or null, never blank, so a blank on a complete record is only a yes/no "no" (as in every family). **Unrecorded = an unconstrained variable over the attribute's domain** (F5-R2-01), in both solvers and both worlds: Clark completion (solver B) and negation as failure (solver A) apply to stated facts and rule-defined predicates only, never to a comparison on an unrecorded value. An unrecorded entry (both worlds) and a blank yes/no entry on an open card are never decisive: the label is the same for every value in the domain, asserted by re-solving over a test set: every listed value for a SEM-17 attribute; for a number or date, each value it is compared with and one step below and one step above each, where the compared values are every threshold or date in the rules or the question **and every value of the same field or attribute of every other member of the comparison set** (other records' or cases' values of that field in counts, "only" and "exactly" items; F5-R3-06); for a category without a value set, every category value named in the question, its filters or the rules, every value of that field of every other member of the record, and one fresh value used nowhere in the case (F5-R4-05); for an unrecorded yes/no entry, and a blank yes/no entry on an open card, both yes and no (F5-R4-05). A base is rejected if any test value gives a different label. Both solvers re-solve (solver B re-runs its own evaluation, S4's compiled SQL included, once per test value substituted for the unrecorded entry). **An unrecorded entry never sits in the measured field of any member of the comparison set of a superlative or a two-entity comparison** (asserted; F5-R3-06), so no "highest", "lowest", "most", "fewest" or "more / fewer <X> than <B>" label depends on an unrecorded value. For an unrecorded number, date or category without a value set, the generator also asserts the same label when every positive statement about the value is taken as false (so, by the SEM-02 line, a statement negating it holds), and rejects the base otherwise, so no reader of the closed-world line can reach another label. Solver B's SQL compiler uses COALESCE(flag, FALSE) for blank yes/no columns on closed cards |
| SEM-05 | unless (text only) | "<A> unless <B>" means: when <B> is false, <A> holds. When <B> is true, this sentence neither makes <A> hold nor makes it fail. | Read at the atom level (SEM-02, F5-R4-01). B false: the rule gives its head (an atom, a negated atom, or a deontic status). B true, non-deontic head: the rule gives nothing, so on closed cards the head's positive atom holds iff another rule gives it and is false otherwise (SEM-02), whatever the head's polarity ("<E> is not eligible unless <B>" with <B> true and no other rule: not eligible); on open cards the atom is undetermined unless another rule or fact decides it, and an undetermined base is rejected. Deontic head (a SEM-24 modal): never this fallback; the status always comes from the SEM-24 closure, in both worlds, so an open card does not reject when the closure decides it. "Unless" rule heads are only non-deontic atoms or "must", "is required to", "must not", "may not", "is not permitted to", "cannot" (lint; SEM-24). Never in a question |
| SEM-06 | only if (text only) | "<A> only if <B>" means <A> does not hold when <B> is false. <B> being true does not by itself make <A> hold. | Read at the atom level (SEM-02, F5-R4-01). B false gives not-A in both worlds (for "<E> is not charged only if <B>", charged; for "<R> may <X> only if <B>", not permitted, which SEM-24 counts as a listed rule forbidding <X>). B true, non-deontic head: the rule gives nothing, so on closed cards the head's positive atom holds iff another rule gives it and is false otherwise (SEM-02), whatever the head's polarity; on open cards it is undetermined unless another rule or fact decides it, and an undetermined base is rejected. Deontic head: never this fallback; the status comes from the SEM-24 closure in both worlds, so an open card does not reject when the closure decides it. "Only if" rule heads are only non-deontic atoms or "may" / "is permitted to" (lint; SEM-24). An "only if" rule carries no "unless" and no "except when" (lint; F5-R4-07). Never in a question |
| SEM-07 | if (text only) | "If <B>, then <A>" means <B> is enough for <A>; so if <A> is false, <B> is false. It says nothing about <A> when <B> is false. The conditions of a rule are the parts of its "if" clause joined by "and"; an "unless" or "except when" part is not a condition. A condition is met when what it says is true of the case, so a condition written with "not" or another negative word is met when the thing it denies is false. "At least <q> of the conditions of <rule>" means at least <q> of them are met. | No biconditional reading. The contrapositive is used by both solvers in both worlds. "If ... then" never in a question. **Condition counts** (F5-R3-08): the question form "at least <q> of the conditions of <rule>" (S1 V rows) is used only on an "if ... then" rule whose "if" clause is a flat conjunction of 2-4 literals (each an atomic statement or its negation, joined only by "and"; no "or", "neither ... nor", "not both", quantifier or nested clause) and which carries no attached exception (asserted); never on "only if" or "unless" rules. Solver B counts met literals from its own parse of the rule |
| SEM-08 | Numeric bounds | "At least N", "no fewer than N", "not less than N", "N or more", "reaches N" and "meets N" include N. "At most N", "no more than N", "not more than N" and "up to N" include N. "More than N", "over N", "above N" and "exceeds N" exclude N. "Fewer than N", "less than N", "under N" and "below N" exclude N. "Between N1 and N2" includes both. "Exactly N" means equal to N. | Closed lexicon (3.4). 30% of bound items sit exactly at N; the rest one step away, where a step is one unit of the value's last displayed digit (integers 1; two decimals 0.01). **Tier tables partition their range** (F5-R3-12, S1 amount sub-shape): tiers are written only as "up to <N1>", "more than <N1> and up to <N2>", ..., "more than <Nk>" (no "between", "at least" or "under" in a tier table), so under this line's inclusivity every value falls in exactly one tier; the parser asserts the partition (no overlap, no gap) on every rendered table, and a table that fails is rejected |
| SEM-09 | half | "At least half" includes exactly half. "More than half" does not. | Even group sizes on 50% of these items. "Most of", "majority" and "minority" are banned (3.4) |
| SEM-10 | or / nor / both | "Or" means at least one, possibly both. "Either <A> or <B>, but not both" means exactly one. "Neither <A> nor <B>" means both are false. "Not both <A> and <B>" means at least one is false. | Bare "either ... or" (without "but not both") is banned, and so is "not" directly governing a bare "or" / "and"; negated connectives appear only as "neither ... nor" and "not both ... and". The both-true case on >= 25% of "or" items |
| SEM-11 | Dates | Each date is a whole calendar day. "On <D>" means that day. "Before <D>" and "after <D>" exclude <D>. "On or before <D>", "by <D>", "no later than <D>" and "not after <D>" include <D>. "On or after <D>", "no earlier than <D>" and "not before <D>" include <D>; these four negated phrases are date words like "on or before" and "on or after", not a "not" over a statement. "Between <D1> and <D2>", "from <D1> to <D2>" and "<D1> through <D2>" include both dates. "In <month> <year>" or "in <year>" means any day of that month or year. "<N> days after <D>" means the <N>th day after <D> (1 day after <D> is the next day). "Within <N> days after <D>" means from the day after <D> through the <N>th day after <D>. "As of <D>" means at the end of <D>, counting every entry dated <D>. A date range in a question about an event asks whether at least one such event falls on some day of the range; one is enough. A "not" over such a statement means that no such event falls on a day of the range. A date range in a question about a single date asks whether that date falls on some day of the range. | **Range words apply only to events and single-date attributes** (F5-R2-03): in a question, "on <D>", "before", "after", "on or before", "by", "no later than", "not after", "on or after", "no earlier than", "not before", "between", "from ... to", "through", "in <month/year>" and "within <N> days after" take an event (existential, as the card states: at least one such event on some day of the range; a C1 / C2 negation over it denies every such event, wide scope) or an attribute with exactly one date. **One side of each boundary** (F5-R4-02): on every event-in-range base, every listed event of the asked kind for the asked entity (for a question over a named group, for every member; F5-R5-02) lies on one side of each boundary date that any row of the base asks (asserted, both worlds), so on closed cards the existential, a universal or "the event" reading, and the wide and narrow scope of a "not" all give the stored label; on open cards the card line decides. **At least one such event** (F5-R5-02): every event-in-range base (each has an N row, a C1 / C2 "not" over the range) has, for the asked entity (for an agent-free question, the asked item; for a question over a named group, every member of the group), at least one remaining listed event of the asked kind (a VOIDed entry does not count; asserted in both worlds by both solvers), so no range claim is vacuous, and on closed cards, with one side of each boundary, the existential and universal readings, both scopes of a "not" and either reading of a negated date word (a date word, as the card says, or a "not" over "before" / "after") give the stored label; on open cards the card line, which names these four phrases as date words, decides; a question about a state (a status, validity, holding, a stance under SEM-20, and the SEM-26 aspect states) states no time other than "as of <D>" (lint). Closed date-phrase lexicon (3.4: "until", "since", "prior to", "earlier than", "later than", "during", "within N days of / before" are banned). Dates as YYYY-MM-DD or with a month name, never all-numeric day/month; no times of day or time zones. 30% of date items at a boundary day. **Stated offsets** (F5-R3-12): a computed date in S1 rule text is written only as "<N> days after <D>" (or, in S2, with the SEM-33 renewal wording); "<N> days before <D>" is not used; the offset phrase is text-side only |
| SEM-12 | Rounding | Values are compared exactly as written. Nothing is rounded. | F5 never needs a rounded value. The only computations are counts read off a table (S4), the comparison itself, and a date plus a stated day count (SEM-11 "<N> days after <D>" in S1; SEM-33 renewals in S2). In the S1 amount sub-shape (F2 structure) every capped, floored or tiered amount is stated in the text (F2's own rule for stated intermediate values) |
| SEM-13 | Ties | "More than <B>" and "fewer than <B>" are false when the two are equal. "Highest", "largest" and "the most <X>" mean no other has more; "lowest", "smallest", "the fewest <X>" and "the least <X>" mean no other has less. When several share that value, each of them has it. "The only one with the highest (lowest)" means no other shares that value. A superlative compares exactly the members of the group the question names ("Among the <group>, ..."). | "Most" only as the superlative of a count. **Superlative forms** (F5-R3-10): only the predicative "<E> has the highest / lowest / largest / smallest / most / fewest / least <X>" and "<E> is the only one with the highest (lowest) <X>"; definite descriptions ("the <entity> with the highest <X>", "the one with the highest <X>", "Is <E> the highest ...?", "the top <entity>") are banned (lint, 3.4), so a tie never meets a uniqueness reading. Every superlative question names its group explicitly, and the comparison set is exactly that group: the S4 filtered subset or the full <entity type> (F5-R1-05). Tie cases on about 15% of superlative and comparison items |
| SEM-14 | Units | Every quantity is given with its unit. Questions compare only quantities in the same unit. | No unit conversion in F5 |
| SEM-15 | Exceptions on rules | An exception attached to a rule ("unless <B>", "except when <B>") means the rule does not apply when <B> holds. It does not make the opposite outcome hold; another rule may still give the outcome. No two rules on this card give opposite outcomes for the same case. | Weak reading for every rule-attached exception. **Where exceptions attach** (F5-R4-07): "except when" attaches to an "if ... then" rule or to a rule with no condition; "unless" as an attached exception attaches only to an "if ... then" rule (in a rule with no "if" clause it is the SEM-05 form); an "only if" rule carries neither, and a rule holds at most one "unless" or "except when" (lint at bank build; asserted by the S1 generator). Every rule-attached exception fires SEM-15 (3.1), so this line is on every card, full or short, whose text has one. Solver A asserts no residual conflict. "Except" never appears in rule text and in a claim on the same card |
| SEM-16 | Corrections (logs) | Entries with no named author are records by <S>. Each CORRECTION or VOID names one entry by its own author. A CORRECTION replaces a value in the entry it names (a holder, a status, a number of days or a stated value), as if that entry had always said the corrected value; the corrected entry keeps its own date, its kind and its item. A VOID cancels the entry it names: treat it as never written. Both apply whatever their own date, also to times before it. Voiding a CORRECTION restores the entry it corrected. Only <S>'s entries make facts true, so a CORRECTION or VOID by anyone else changes no fact; it changes only what its author stated. | One mechanism for facts and stance (F5-R2-04): a CORRECTION or VOID names an entry by its own author (asserted), so <S> never voids or corrects another party's notice and no party touches <S>'s entries. Chains of depth <= 2 only (CORRECTION or VOID of a plain entry; VOID of a CORRECTION); each entry is named by at most one CORRECTION or VOID. **Correctable fields** (F5-R4-06): a CORRECTION changes only value fields of the named entry (the holder of a creation or transfer, the status of a status entry, the <N> of a renewal, the value in a notice's statement); never its date, its entry type, its item ID or its named actor (asserted by the generator; both solvers parse the CORRECTION and reject one that names another field; F5-R5-07), so every entry takes effect on its listed date (SEM-33), the newest-dated renewal is fixed by listed dates, and the one-entry-per-day assertion (SEM-33) holds after corrections. <S> never makes two conflicting statements about a timeless fact in a log (asserted); state changes go through dated entries (SEM-33) |
| SEM-17 | Value sets | For a case or record attribute (S1, S4): Each <entity type> has exactly one <attribute> at a time, one of: <v1>, <v2>, ..., <vn>. For a status set by log entries (S2): An <item> has no <attribute> before the first entry that sets it; from that entry's date on, it has exactly one <attribute> at a time, one of: <v1>, <v2>, ..., <vn>. | **Log statuses** (F5-R4-04): S2 cards print the second form; "the first entry that sets it" is the first remaining status entry (a VOIDed entry counts as never written, SEM-16). Status entries are dated on or after the item's creation, and every status question (A, N, D, V and C17 rows, with "as of <D>" or no stated time) and every value test on a status asks only a day on or after the item's first remaining status entry (asserted); an item whose status entries are all VOIDed gets no status question. So "not <v1>" and "one of" the other listed values agree on every asked day (MR8), and "never <v1>" over a status counts the days before the first status entry as days without <v1>, as the card line says. Solver B adds the matching domain axiom (no status before the first remaining status entry; exactly one listed status from then on), so its KB agrees with replay and SEM-02. "Not <v1>" = any other listed value (on a day the item has the attribute). An antonym (<v2>) is not the negation of <v1> when n_vals >= 3 (n_vals = the number of listed values). Used in V rows only (never N or D). Printed for every value-set attribute in the text (3.1) |
| SEM-18 | Binary predicates, affixal negation | <P> has two states only: "<non-P>" (or "<un-P>") means exactly "not <P>". | Affixal (un-, in-, non-, dis-) and litotes ("not non-P") only on predicates with this line; never on gradable words. On S6 only for the answerability predicate, whose affixed form ("is unanswerable from") SEM-29 defines, so SEM-18 never prints on S6 (3.1 trigger table); "non-hateful" and "non-sexist" are never used |
| SEM-19 | Implicative and privative cues | "Failed to", "neglected to", "omitted to" and "did not manage to" <do X>, with no "by <D>", mean X did not happen on any day of the period the record covers, wherever the phrase appears (a dated log entry, a sentence or a question) and whatever the entry's own date; they do not say whether X was required. "Failed to <do X> by <D>" means X did not happen on any day from the start of the covered period through <D>. "Refused to <do X>", "declined to <do X>" and "was prevented from <doing X>" mean X did not happen on any day of the period the record covers. "Managed to <do X>" means X happened. "Lacks <Z>", "is without <Z>" and "is free of <Z>" mean does not have <Z>. | Whole-period reading (F5-R1-02). "Is missing" and "unable to" are banned. Refusal and prevention cues (C4) appear in text only. **Privatives (C5) are timeless** (F5-R2-05): they appear only on cards with no dated entries (S1, S3, S4; S6 SQuAD 2.0 and MuSiQue as SEM-29 phrases), never in S2 logs or S5 threads or their questions (lint), so "does not have <Z>" never needs a day. When the text uses a failure or refusal cue about <E> and <X> **without "by <D>"**, in a dated entry or not (F5-R2-06), no <X> entry for <E> (an entry naming <E> as its actor, SEM-33, F5-R5-07) exists anywhere in the covered period, before or after the cue (asserted; both solvers apply this to every such cue); with "by <D>", no <X> entry for <E> on or before <D> (asserted). A question that uses C3 states no other time or range: no "as of", "before", "after", "between", "from ... to", "through", "in <month/year>", "on <D>" besides C3's own "by <D>" (lint; F5-R1-03). A C3 or C4 phrase also prints SEM-27's covered period (3.1); a C5 phrase alone does not |
| SEM-20 | Report verbs, authority | Statements by <S> are true. Statements by anyone else are only claims: they make nothing true or false. "<X> denied that <P>" and "<X> ruled out <P>" mean <X> stated that <P> is false. "<X> confirmed <P>" means <X> stated that <P> is true. A question about what <X> stated asks about <X>'s latest remaining statement about <P> dated on or before the asked day; "latest" means the latest date. A statement about <P> is one that states <P> or states that <P> is false. <X>'s own VOID or retraction of one of its statements removes that statement, and <X>'s own CORRECTION or correction replaces what that statement says, as if it had always said that, whatever the date of the VOID or correction. Nobody else can change what <X> stated. | A question about a fact uses only <S>'s statements; a stance question ("did <X> deny ...") asks what <X> stated, under the latest-remaining-statement rule (F5-R1-01). **Stance questions appear only on closed cards**, where SEM-02 says the record lists every statement; on open cards C7 is text-side only. No party makes two statements about one fact on the same date, and no retraction or correction by a party shares a date with a statement by that party about that fact (asserted, S2 and S5; F5-R3-05). **Literal <P>** (F5-R3-11, F5-R4-03): every statement the asked party made about the entity and attribute of <P>, of any date, literally states <P> or literally states that <P> is false (by "denied" or "ruled out"), or the asked party made no statement about that entity and attribute (asserted; solver B checks it on its own parse), so no stance label depends on whether a statement entails <P> or not-<P> (a different value of a SEM-17 attribute, a state at another date, a day inside an asked month). **Asked party and <P>** (F5-R4-03): a stance question never names <S> as the asked party (<S>'s unauthored log entries are records that set states, SEM-16, SEM-33), and its <P> is a timeless fact or an event, never a SEM-33 state (asserted; solver B checks both). For a stance question (an S2 V row, an S5 base), the asked party's remaining statements about <P> up to the asked day all have one polarity (asserted), so "latest" and "any" give the same label. If <X> made no remaining statement about <P>, both "did <X> confirm" and "did <X> deny" are No. "Refuted" is banned. **No stance question about <P> to a party that has a VOID, CORRECTION, retraction or correction of any date about <P>** (S2 and S5; F5-R2-04), so no stance label depends on these rules; solver B applies the same rule |
| SEM-21 | Status words vs speech acts | In this record, "<status word>" is a status: it means the outcome was <value>, not that anyone made a statement. | A card uses each of "denied / refused / rejected" in one sense only. A status word is a value of a status field from the card's declared status list; that use triggers SEM-21 only, never SEM-19 or SEM-20 (3.1 trigger table) |
| SEM-22 | Quantifiers | Quantifiers range over the members of the named group, and the record names every member. "Every" and "all" mean each member, with no exception. Every group named in a question has at least one member. "Some" means at least one, possibly all. A direct question "Did any <A> ...?" asks whether at least one <A> did. "No <A>", "none of the <A>" and "not any <A>" mean zero. "Not every <A>" and "not all <A>" mean at least one <A> does not. | Never the scope-ambiguous "every/all ... not"; never "not ... because"; restrictor sets non-empty (asserted). **Where "any" may stand** (F5-R3-02): "any", "anyone" and "anything" appear only (a) in the matrix interrogative clause of a question ("Did any of the <group> ...?", "Did anyone other than <A> <X>?"), or (b) inside the L_neg entries "not any", "hardly any" and "scarcely any". Never in a positive declarative, so never in the embedded declarative of a truth frame outside (b), and never in rule, modal or other text; there the existential is written "some" / "someone other than <A>" (lint per template at bank build) |
| SEM-23 | only / other than / except | The group is exactly the group the question names ("Among the <group>, ..."). "Only <A> <did X>" means <A> did X and no other member of the group did X. "Did anyone other than <A> <do X>?" and "someone other than <A> <did X>" are about whether at least one member of the group other than <A> did X; <A>'s own status does not matter. "All except <A>" means every member of the group other than <A> did it, and <A> did not. | Every "only", "other than" and "all except" question names its group explicitly; the comparison set is exactly that group (the S4 filtered subset or the full <entity type>), and <A> is a member of it (asserted; F5-R1-05). "Only" only as pre-subject "Only <A>" with <A> one named entity. No outer negation of "only"; the idiom "not only ... but also" (SEM-28) is exempt. **"All except"** (F5-R5-08): no L_core word stands directly before "all except <A>", and "all" or "every" never combines with "except" or "other than" in one noun phrase other than "all except <A>" itself (lint at bank build); a negation over "all except <A>" is written only with a C2 frame ("it is not the case that all except <A> ...", "it is false that all except <A> ..."), so "not all except <A>" never appears and the 3.4 longest match never finds "not all" inside it |
| SEM-24 | Modal / deontic | "Must" and "is required to" mean required. "Must not", "may not", "is not permitted to" and "cannot" mean not permitted. "Need not", "does not have to" and "is not required to" mean not required; they say nothing about whether it is permitted. "May" and "is permitted to" mean permitted. The rules listed are all the rules about these actions: an action that no listed rule forbids for the case is permitted, and an action that no listed rule requires for the case is not required. This line decides whether an action is required or permitted, on complete and incomplete records alike, ahead of the line on whether the record is complete. In a table of roles and actions, "required" means the role must do the action (so it is also permitted), "permitted" means the role may do it and need not, and "forbidden" means the role must not do it; each cell holds in every case, and no other rule is about a role and action that the table lists. | **Role and action table** (S1; F5-R5-03): each cell is an unconditional rule ("required" = "<R> must <X>", "permitted" = "<R> may <X>", "forbidden" = "<R> must not <X>"), and no listed rule, with or without a condition, has a head about a (role, action) pair that the table lists (asserted, both solvers), so a "permitted" cell gives permitted and not required, a "required" cell required and permitted, and a "forbidden" cell neither, in every case, whether a reader takes the table as exclusive categories or as rules under the closure. Solver B encodes the cells as these unconditional rules. Closure applies on every card that shows this line, in both worlds (F5-R3-01): the card line itself states its precedence over the world line (SEM-02 / SEM-03), and SEM-24 prints on every card whose text or questions use a modal phrase (3.1), so no deontic question meets a card without it. **What forbids and what requires** (F5-R4-01): a listed rule forbids <X> for the case when it applies and gives "not permitted": a "must not", "may not", "is not permitted to" or "cannot" head of a rule that applies (an "if ... then" rule whose conditions are met and whose exception does not hold, a rule with no condition and no exception that holds, or an "unless" rule whose <B> is false), or "<R> may / is permitted to <X> only if <B>" with <B> false. A listed rule requires <X> when a "must" or "is required to" head of a rule that applies gives it. Nothing else forbids or requires: "may", "is permitted to", "need not", "does not have to" and "is not required to" heads never do. Deontic heads never use the SEM-05 / SEM-06 closed-world fallback; their status always comes from this closure, in both worlds. **Deontic rule shapes** (lint at bank build): "if ... then" rules and rules with no condition take any modal head; "unless" rules take only "must", "is required to", "must not", "may not", "is not permitted to" or "cannot"; "only if" rules take only "may" or "is permitted to". An applying "may" / "is permitted to" head never meets an applying prohibition, and an applying "need not" / "does not have to" / "is not required to" head never meets an applying requirement, for one role, action and case (asserted; SEM-15). Solver A computes forbidden / required by its usual chaining and sets permitted = not forbidden, not required = not required by any rule. Solver B adds the closure as definitions **before** Clark completion (permitted(r, x) iff no listed rule forbids x for r in the case; required(r, x) iff some listed rule requires it), so completion and negation as failure apply to the rule bodies only, never to "permitted" or "required" directly; on open cards the status is determined only when every model agrees whether a listed rule forbids or requires it, else the base is rejected. "May not" is always prohibition. Required implies permitted; no action is both required and forbidden for one role and case (asserted). "Cannot" only in deontic rule text; never in questions |
| SEM-25 | Graded negatives and "barely" | "Hardly any", "scarcely any" and "few" <X> mean fewer than <q> <X>. "<E> barely met <T>" means <E>'s value was at least <T> and no more than <m> above <T>. "<E> barely stayed within <C>" means <E>'s value was at most <C> and no more than <m> below <C>. | Structural (comparison), never XOR. Only with stated <q> / <m>. "Barely": S4 and numeric S1 only. "A few" is banned |
| SEM-26 | Temporal aspect | In a question, "never" means on no day from the start of the period the record covers through the asked day; in the record, "never" means on no day of the covered period. "No longer" means held on some day before the asked day in that period and does not hold on the asked day. "Still" means held on some day before the asked day in that period and holds on the asked day. In a dated record entry, "no longer" and "still" refer to the entry's date in place of the asked day. An entry in the record that says something never happened, no longer holds or still holds is a statement by its author about the record: it sets no state and changes none. | Only never / no longer / still (3.4 bans again, stopped, started, not yet, already, ever). "No longer" and "still" are asked only when the earlier part is true (asserted). In the text, "no longer" and "still" appear only in dated entries. **Text side** (F5-R5-04): text-side "never", "no longer" and "still" appear only in S2 log entries, never in S5 messages (lint); such an entry is dated on a day with no other entry for the same item and state (asserted); one by <S> is true of the log under SEM-33 replay of the state-setting entries and the remaining listed events (on its date for "no longer" / "still"; over the covered period for "never"; asserted in both worlds by both solvers, else the base is rejected), so it never decides a label against replay; one by another party is a claim (SEM-20) and makes nothing true. Both solvers parse such entries as statements, never as state-setting entries (SEM-33). The only stated time a question may combine with never / no longer / still is "as of <D>", which sets the asked day (SEM-27); never "before", "after", "between", "from ... to", "through", "in <month/year>", "on <D>" or "by <D>" in the same question (lint; F5-R1-03). With no stated time the asked day is <D_end>, so "never" then covers the whole period |
| SEM-27 | Covered period, asked time | This record covers <D_start> to <D_end>, both included. A question with no stated time asks about the end of <D_end>. "As of <D>" in a question makes <D> the asked day. | Printed on every S2 and S5 card, on any card where a C3 or C4 phrase or a SEM-26 phrase occurs, and on any card whose text holds a dated entry (an S2 log entry or an S5 message); a C5 phrase alone does not print it (3.1; F5-R2-05). <D> in "as of <D>" lies inside the covered period (asserted) |
| SEM-28 | Decoys | "Not only <A> but also <B>" means both <A> and <B> are true. | <B> is a determined-true, non-decisive proposition from M (asserted; solver B checks it is true). LF = A AND B. S1-S5 only. Counts in j, never in k |
| SEM-29 | Answerability (S6 SQuAD 2.0, MuSiQue) | "The passage answers the question" means the passage itself states the answer; outside knowledge does not count. "Does not answer", "fails to answer", "lacks an answer to" and "is unanswerable from" all mean the passage does not state the answer. (MuSiQue: "the paragraphs together state ...") | Human gold (SQuAD 2.0 `is_impossible`, MuSiQue answerable flag). Replaces the world line |
| SEM-30 | Judgement (S6 GHC, EDOS) | <D: a Claude-written summary of the dataset's published label definition>. The label is <GHC: "hateful" if the annotators' majority marked an assault on human dignity or the majority marked a call for violence> / <EDOS: the annotators' unanimous judgement> under this definition. | D states exactly the label function the gold uses (G5 dataset-level read checks narrowing or widening). No guideline text is copied. Replaces the world line |
| SEM-31 | Threads (S5) | Only <S>'s messages make facts true or false. Each retraction or correction names a message by its own sender. A retraction cancels the message it names, as if never sent. A correction replaces the value in the message it names, as if that message had always said it; the corrected message keeps its own date. Retractions and corrections apply whatever their own date, and they are not themselves messages about the fact. Of <S>'s remaining messages about one fact, the latest one counts; "latest" means the latest date. Another party's retraction or correction changes only what that party stated. | Solver B's z3 constraints implement exactly this: a correction rewrites the value of the named message at that message's date, and retractions and corrections never enter the latest-message comparison (F5-R3-05). Each retraction or correction names a message by its own sender (asserted; F5-R2-04), the same mechanism as SEM-16. No two messages by one party about one fact share a date, no retraction or correction by a party shares a date with a message by that party about that fact, and a retraction or correction is dated after the message it names (asserted; F5-R1-06, F5-R3-05). On a fact base, a correction by <S> about the asked fact names <S>'s latest message about that fact (asserted; F5-R3-05), so a reader who dated the correction at its own date would still reach the stored label. Listed order is never used to order messages (MR5 reorders them). Every message's date and sender always hold a value (never "not recorded", null or blank; F5-R5-05) |
| SEM-32 | Comparisons (S6 2Wiki) | A comparison is true only if the paragraphs state facts that make it true. Values are compared as the paragraphs give them; "before", "after", "older", "younger" and "first" are false when the two values are equal. | **Paragraph-grounded gold** (F5-R3-03): for each entity the converter finds the compared value (a date or other value) in the kept supporting paragraphs with its own deterministic parser and computes the gold from these paragraph-stated values only. The evidence triples are a cross-check: a base is kept only when (a) each entity's value is stated in its kept supporting paragraph, (b) that value matches the triple's value at the paragraph's precision, (c) both compared values are stated at the same precision (both full dates, both month and year, or both years), (d) across all kept paragraphs (supporting and distractor) each entity has exactly one stated value for the attribute, (e) the values are not equal (no tie), and (f) the paragraph-computed answer equals the dataset answer; any failure skips the base. "Mismatch", "precision" and "exactly one value" are all judged on the paragraph text, never on the triples alone. "Same <attribute>" items only under (a)-(d) and (f). Rendered comparisons use only "before", "after", "older", "younger" and "first" ("earlier" and "later" are not used; 3.4). Replaces the world line on 2Wiki cards |
| SEM-33 | Log states (S2) | Each item has three separate states: its holder, its status and whether it is valid. An entry takes effect on its date and counts for that date. A creation or a transfer sets the holder, a status entry sets the status, and a "<renewed / valid> for <N> days" entry sets validity; no entry changes any other state. A state set by an entry holds from that entry's date through the day before the next entry that changes the same state. "<Renewed / valid> for <N> days" dated <D> makes the item valid from <D> through its last valid day, the <N>th day after <D>; this replaces any last valid day set by an entry dated before <D>, even one further on, and no other kind of entry moves the last valid day. From the day after its last valid day the item has lapsed (it is not valid), and a renewal dated after that day makes it valid from the renewal's date. A lapse changes neither the holder nor the status. | **Renewal rule** (F5-R2-02): the newest-dated renewal sets the last valid day, also when it shortens the current one. **Separate states** (F5-R3-04): transfers, creations and other entries leave the last valid day as it is; holding never lapses. Generator asserts: an item with a renewal entry has no status entries, and the card's declared status list holds no validity word ("valid", "lapsed", "expired", "active", "inactive", "current"), so status and validity never meet on one item; a question about validity asks only "valid" ("Is <item> valid as of <D>?"), never "active", "expired" or "current" (lint); an item with no renewal entry is never valid (closed cards, by SEM-02); a creation entry that states a duration is rendered as two entries' meanings in one line ("created for <holder>, valid for <N> days") and both solvers parse it as a holder entry plus a renewal on the same date. The meaning avoids "until", "later" and "again" (F5-R2-18), so the 3.4 bans hold for card text with no exemption. Closed cards: states persist as stated. Open cards: a state on a day is determined only by an explicit "as of <D>" status statement by <S> for that day. **"As of" statements agree with replay** (F5-R5-06): in both worlds, every <S> "as of <D>" statement about a state (holder, status or validity) is about a day on or after the remaining entry that first sets that state, and it equals the SEM-33 replay of the remaining listed entries for that item, state and day (asserted by both solvers; a base where one differs is rejected); so on open cards the printed persistence line, read on the listed entries, gives the stored label too, and on closed cards no "as of" statement contradicts replay. Such statements set no state. **Named actors** (F5-R5-07): every S2 entry that records an action names the party that did it ("<E> renewed <item> for <N> days", "<E> transferred <item> to <F>", "<E> filed <Z>"); for a renewal or a transfer that party is the item's holder on the entry's date (for a transfer, the holder before it), asserted on the log after CORRECTIONs and VOIDs; the named actor is never a CORRECTION target (SEM-16). A creation entry names the new holder and no actor, and no question or cue names an agent of a creation. "<E> <X>" in a question or cue (C3, C4 and the SEM-19 assertions included) is true of an entry exactly when that entry names <E> as its actor; an agent-free question ("Was <item> renewed ...?") counts every entry of that kind for the item. Because the actor of a renewal or a transfer is the holder, a reader who counts the holder's actions reaches the same label. The validity a creation entry states ("created for <E>, valid for <N> days") is not a renewal event: no question or cue about renewing is asked about an item whose creation entry states a duration (asserted). **Structural fields** (F5-R5-05): every entry's date, entry type, item ID and (on an action entry) named actor always hold a value, in both worlds (SEM-02). Never two entries on one day for the same entity and attribute (asserted); listed order is never used to order events. "Its date" is always the entry's listed date: a CORRECTION never changes an entry's date, type, item or named actor (SEM-16, F5-R4-06, F5-R5-07). An item has no status before its first remaining status entry, and status questions ask only days on or after it (SEM-17 log form, F5-R4-04). Printed on every S2 card (3.1) |

### 3.3 Card renderings (written after G14; rules fixed now)
- The meanings above are normative and do not change. The sentences that carry them are templates, written after G14
  by the format and generator agents: **>= 3 renderings per key**, at least one per definition style (spec 2.1): one
  line; one line + 1-2 examples (about 50% of cards; examples use other entities of the pack, never the row's base);
  rubric or decision-list table. All renderings sit in a frozen registry (sha256 logged) that the card parser reads.
- Every rendering passes the 7.2 template check and the spec-9 counts-only sealed comparison. A hit drops that
  rendering; a new rendering with the same meaning replaces it, is re-checked and re-registered, and every affected
  row is regenerated (K08).
- G11's "no surface template above 2% of a family" applies to question cue templates and text templates. SEM
  renderings are definition text: they follow the definition-style quota, like instruction wordings follow the >= 30
  wording pool (both necessarily exceed 2% each). G6 (c) and the per-key yes-rate check (section 8) cover them.

### 3.4 Closed lexicons (lint at bank build; meanings in 3.2)
- **L_core** (banned in the matrix interrogative clause per token, also inside a multiword entry, SEM-01 and
  F5-R2-09; counted in j): not, n't, no, none, nobody, nothing, nowhere, never, neither, nor.
- **L_neg** (surface negation lexicon for j_q and j_t; F5-R1-09). Entries are matched **by lemma**, so every inflection
  counts (deny / denies / denied / denying; refuse, decline, prevent, neglect, omit, fail, lack, rule out likewise).
  - Single entries: the L_core words; without; lack; fail to; neglect to; omit to; refuse to; decline to; prevent
    from; deny; rule out; hardly; scarcely; few; barely; except; unless; cannot; false; free of.
  - Multiword entries (each one entry): no longer; need not; not only (... but also); neither ... nor; not both; no
    fewer than; no more than; not less than; not more than; not before; not after; no earlier than; no later than
    (F5-R2-10); not every; not all; not any; none
    of; must not; may not; is not permitted to; does not have to; is not required to; did not manage to; it is not the
    case that; it is false that; all except; except when; other than.
  - Plus the SEM-18 affixed words each pack declares (each word one entry).
- **Counting rule for j (F5-R1-09).** j = the number of matched L_neg entries, found longest match first, left to
  right, without overlap; each match counts 1 whatever its length. So "no longer", "need not", "neither ... nor", "no
  fewer than" and "it is not the case that" count 1 each, and litotes "not non-<P>" counts 2 ("not" + the affixed
  word). "Fewer" and "fewest" are not "few" and do not count. "False" counts wherever it is a word in the question or
  text, data values included, as "no" does. j_q counts the question; j_t counts the text (program-written and quoted
  source text alike); card lines are not counted. A quoted S6 source question counts in j_q, but a base whose quoted
  source question holds any L_neg entry is skipped (F5-R1-10), so every A row keeps j_q = 0.
- **Allowed operator words (F5-R1-12)**: exactly (a) every phrase quoted in the card column of SEM-01 to SEM-33,
  among them "if ... then", "unless" and "only if" (SEM-05/06/07, rule text only), "except when" (SEM-15), CORRECTION
  and VOID (SEM-16), the value-set wording (SEM-17), the affixed words each pack declares (SEM-18), the SEM-29
  phrases, "before", "after", "older", "younger" and "first" (SEM-32, 2Wiki declaratives only) and "<renewed / valid>
  for <N> days" (SEM-33); (b) the L_neg entries above; (c) the truth frames (SEM-01). Each phrase may appear only on the
  side, samplers and datasets its SEM row and cue family allow. Anything else fails the template lint.
- **Where the bans and the operator lint apply (F5-R1-11).** Only to program- or template-written text: cards,
  Claude-written wrapper packs and SEM-30 definitions, rendered M (rules, logs, facts, records), questions, and 2Wiki
  declaratives. Quoted source text (S6 passages, paragraphs, posts and the quoted source question) is exempt from the
  bans, the lint and the SEM triggers (3.1) and is never edited; it still counts in j_t (passages, posts) and j_q (quoted question), the quoted
  source question must hold no L_neg entry (base skipped otherwise), and quoted text still passes 7.2
  decontamination.
- **Banned in program-written text and questions**: tag questions; any L_core word in a matrix interrogative;
  "should", "ought", "can", "could", "has to" anywhere; "if", "unless", "would" in questions; bare "either ... or";
  "not" governing a bare "or"/"and"; "every/all ... not"; "not ... because"; outer negation of "only" (except "not only
  ... but also"); group or post-verbal "only"; "any" in rule or modal text; bare generics and "typically / usually /
  generally"; "most of", "majority", "minority", "a few"; "is missing", "unable to", "refuted"; ability or epistemic
  "cannot" ("cannot attend", "cannot be determined"); "until", "since", "prior to", "during", "within <N> days of /
  before"; "earlier", "later", "earlier than" and "later than" except inside "no earlier than" and "no later than"
  (SEM-11); times of day, time zones, all-numeric dates; "again", "stopped", "started", "not yet", "already", "ever";
  "non-hateful", "non-sexist"; "any", "anyone" and "anything" outside a matrix interrogative clause and outside "not
  any", "hardly any" and "scarcely any" (SEM-22, F5-R3-02); definite superlative descriptions ("the <entity> with the
  highest / lowest / most / fewest <X>", "the one with the highest <X>", "Is <E> the highest ...?", "the top
  <entity>"; "the only one with the highest (lowest)" is allowed; SEM-13, F5-R3-10); "meet(s) <rule>", "satisfy" and
  "qualify under <rule>" in an inverted-card question (section 8, F5-R3-09); "<N> days before <D>" (SEM-11,
  F5-R3-12); "active", "expired" and "current" as validity words, and any validity word in a declared status list
  (SEM-33, F5-R3-04); "not" or any other L_core word directly before "all except", and "all" / "every" with
  "except" or "other than" in one noun phrase other than "all except <A>" (SEM-23, F5-R5-08); "no", "never" or a C3,
  C4 or C5 cue in an S1 rule head (SEM-02, F5-R5-01); text-side "never", "no longer" and "still" outside S2 log entries
  (SEM-26, F5-R5-04); the shared negation-frame lint (XF10): no question wraps a negated or negatable
  proposition in an outer judgement or acceptance predicate ("wrong", "right", "reject", "accept", "should / would
  ... be"), which covers the frame class "should / would the statement ... be rejected / accepted" and any "reject /
  accept the statement" wording (F5's SEM-01 rule, which keeps every L_core word out of the matrix interrogative
  clause, so "Is it not the case that ...?" is never a matrix frame in F5 and C2 "it is not the case that" sits inside
  a truth frame while "Is it false that ...?" may be one, is a family-local rule and is not cited as XF10; CF-5); "only non-<X>" with an outer "be rejected"; every dev or eval negation
  wording (7.2 method 8); OPI and jagged attack strings.

## 4. Cue families (logical signatures only; templates are written after G14)

- **Bank.** >= 250 question-side templates in >= 12 families (C4 is text-side only and does not count). Text-side
  rendering templates are a separate list. Every template declares: family id, side (question / text), LF signature,
  negation-cue count k_template (rule below), the monotonicity of each argument slot (table below), L_neg entries,
  and whether it may build N or D. The cue parser checks every declaration at bank build (100%); declared
  monotonicity is also checked by a property test on random small models (Hypothesis, 100%).
- **Negation-cue count k** (sidecar `k_neg`; spec 2.2 "number of negation cues"; question side only). Counted
  operators: sentential NOT and meta-truth cues (C1, C2), negative implicatives (C3: failed / neglected / omitted to,
  did not manage to), privatives (C5), affixal negation (C6; litotes "not non-P" = 2), negative quantifiers (no, none
  of, not any, not every, not all), negated connectives (neither ... nor, not both), negated comparison words (no
  fewer / no more / not less / not more / not before / not after / no earlier than / no later than; F5-R2-10),
  negated modals (must not, may not, is not permitted
  to, need not, does not have to, is not required to), negative aspect (never, no longer), graded negatives (hardly
  any, scarcely any, few), exceptives (other than, all except). Each counts 1 per occurrence in the LF as written.
  Not counted (0): plain comparisons (at least, at most, more than, fewer than, before, after, between, exactly),
  "managed to", "only", "still", decoys, "barely", antonyms and value tests. Stance verbs: "denied that P" and "ruled
  out P" count 1 (stated(NOT P)), "confirmed P" counts 0. A row's k = sum over its question-side operators. **k is a
  cue count, not a polarity** (F5-R1-15): exceptives and stance verbs count 1 but are not antitone in <P>, and some
  k = 0 operators are non-monotone, so polarity always comes from the monotonicity table, never from k parity.
- **A rows** have k = 0 and j_q = 0: an A row's base operator holds no counted operator and no L_neg entry (asserted).
  So "none", "no", "not every" and every other counted or L_neg operator are never A-row base operators; "none" is
  reached only as the N row of a "some" base (F5-R1-08).
- **Monotonicity table (F5-R1-15, F5-R2-11; part of the cue bank, filled per template after G14).** Each
  question-side operator declares, per argument slot, one of: up (monotone), down (antitone), non-monotone, opaque.
  Slots: a quantifier or count bound has a restrictor slot (the named group or filter) and a scope slot; a connective
  or decoy has one slot per conjunct; every other operator has one embedded slot. The classes are fixed now, and
  **every question-side operator of the 3.4 allowed list has exactly one row below; an operator or slot without a
  declared class fails the bank lint**:
  - up: identity; truth frames; "as of <D>"; "managed to"; "still" (in <P>); "some" / "any" (both slots); "every" /
    "all" (scope); "not every" / "not all" (restrictor); "at least / no fewer than / not less than / <q> or more / more
    than / over / above <q>" (both slots); "at least half" / "more than half" (scope); "at least <q> of the
    conditions" (scope); "anyone other than <A>" and "someone other than <A>" (scope); the inverted-card form "<case>
    is among the cases that are <outcome>" (identity over the outcome; F5-R3-09); "or", "and"; both slots of "not only <A> but also <B>"; the
    positive modals "must", "is required to", "may", "is permitted to" (over the action); **date words over an event**
    (existential: some such event on some day of the range): "on <D>", "before", "after", "on or before", "by", "no
    later than", "not after", "on or after", "no earlier than", "not before", date "between", "from ... to",
    "through", "in <month/year>", "within <N> days after <D>";
  - down: NOT (C1, C2); C3 (with or without "by <D>"); C5; C6; "every" / "all" (restrictor); "no" / "none of" / "not
    any" (both slots); "not every" / "not all" (scope); "neither ... nor" and "not both" (each conjunct); "never";
    "hardly any", "scarcely any", "few" (both slots); "at most / no more than / not more than / up to / fewer than /
    less than / under / below <q>" (both slots); the negated modals "must not", "may not", "is not permitted to",
    "need not", "does not have to", "is not required to" (over the action); the bound complement (section 4, V rows),
    relative to the base's atom;
  - non-monotone: "only"; "exactly <q>" (both slots); **numeric** "between" (both slots); "at least half" / "more than
    half" (restrictor); "barely"; superlatives and "the only one with the highest (lowest)"; two-entity comparisons
    ("more / fewer <X> than <B>") with respect to <X>; "all except <A>"; "either ... or ..., but not both"; "no
    longer";
  - opaque: stance verbs ("denied", "ruled out", "confirmed"), and value tests over a value set (C17: antonym, "one
    of") with respect to the base's own value;
  - atom (no embedded slot): a comparison on one single-valued number or date (the SEM-08 bound words and "reaches",
    "meets", "exceeds" applied to one value; SEM-11 date words on an attribute with exactly one date), the SEM-29
    answerability predicate and SEM-32 comparisons; a pack tag applies to the atom as a whole.
  Text-side-only phrases have no class and fail the lint in a question: "if ... then", "unless", "only if", "except
  when", CORRECTION, VOID, "<renewed / valid> for <N> days", "<N> days after <D>" as a stated offset (not inside "within <N> days after <D>"; F5-R3-12),
  "cannot", the C4 refusal and prevention cues and the value-set declaration.
  The **polarity** of a slot in a row's LF = the parity of down operators on the path from the root to that slot,
  defined only when every operator on the path is up or down; otherwise the slot has no polarity. MR7 (section 7) and
  yes-is-bad (section 8) use only this polarity.
- **N and D** are built only from exact contradictory or identity compositions: C1, C2, C3, C5, C6 (SEM-18
  predicates), and from C8 and C13 in their exact-contradictory forms (every vs not every, some vs no, A or B vs
  neither A nor B, both vs not both). N has k = 1, D has k = 2. Antonyms, graded cues, "barely", bounds, dates, modals,
  aspect and decoys go only into V.
- **Text side.** **t_txt** = the number of instances, in the rendered text, of text-side cue templates that declare at
  least one L_neg entry, counted whether or not the instance is on the decisive path (F5-R1-19).

| # | Family | Signature | Side | N/D | Bases |
|---|---|---|---|---|---|
| C1 | Plain sentential / verbal "not", "no" | NOT | q | yes | all |
| C2 | Meta-truth frames ("it is false / not the case that") | NOT | q | yes | all |
| C3 | Implicative verbs (SEM-19; whole-period scope, no other stated time in a C3 question) | NOT(event) / identity (managed to) | q, t | yes | S1-S5; S6 SQuAD, MuSiQue ("fails to answer") |
| C4 | Refusal and prevention (SEM-19) | text rendering of NOT(event) | t only | no | S1-S5 |
| C5 | Privative / absence (SEM-19; timeless, never on dated cards) | NOT(has) | q, t | yes | S1, S3, S4; S6 SQuAD, MuSiQue ("lacks an answer to") |
| C6 | Affixal negation and litotes on binary predicates (SEM-18) | NOT | q, t | yes | S1-S5; S6 SQuAD, MuSiQue |
| C7 | Report verbs with authority (SEM-20; latest remaining statement) | stance: stated(X, P or NOT P) | q (closed cards only), t | no | S2, S5 |
| C8 | Quantifier negation (SEM-22) | scope | q | exact forms | S1, S3, S4 |
| C9 | Numeric bounds (SEM-08/09) | comparison | q, t | no | S1, S4 |
| C10 | Date bounds (SEM-11; in a question only on events and single-date attributes, never on states) | comparison | q, t | no | S1, S2 |
| C11 | Exceptives and "only" (SEM-23; a negation over "all except" only by C2, F5-R5-08); conditionals are text-side rule renderings (SEM-05/06/07) | exception | q (exceptives), t (conditionals) | no | S1, S3, S4 |
| C12 | Modal / deontic negation (SEM-24) | deontic | q, t | no | S1 |
| C13 | Connective negation (SEM-10) | De Morgan | q | exact forms | S1, S3 |
| C14 | Graded negatives and "barely" with stated cut (SEM-25) | comparison | q, t | no | S4; "barely" also numeric S1 |
| C15 | Temporal aspect: never / no longer / still (SEM-26; text side only in S2 log entries, as statements that set no state, F5-R5-04) | temporal | q, t | no | S2, S5 |
| C16 | Decoys: "not only ... but also" (SEM-28) | conjunction with a true <B> | q, t | no | S1-S5 |
| C17 | Antonym or "one of" over a listed value set with n_vals >= 3 (SEM-17) | value test | q | no | S1, S2, S4 |

- **S6 operators** by dataset: SQuAD 2.0 and MuSiQue C1, C2, C3, C5, C6; 2Wiki, GHC and EDOS C1, C2 only. No
  structural cue and no decoy on S6.
- **V rows (spec 2.2 "a scope-shift or implicit-cue variant"; F5-R1-14).** Every V row is one of these, and nothing
  else is generated as V:
  - S1-S5, k = 1-3: a counted cue (section-4 list) that is not N's or D's composition on that base: an implicative,
    privative, exceptive, stance, negated modal, negative aspect or graded cue, or a negated quantifier or connective at
    a different scope than in N.
  - S1-S5, k = 0, only these listed forms: an antonym or "one of" over a value set (C17); "barely" (C14); a decoy
    (C16); "only" (C11); "still" (C15); or the exact complement of the base's bound, which is an implicit negation of
    the base ("at least <q>" vs "fewer than <q>", or "at most <q - 1>" on integer counts; "at most <q>" vs "more than
    <q>"; "on or before <D>" vs "after <D>"; "on or after <D>" vs "before <D>"). **The bound complement is used only on
    a single-valued number or date and on counts** (F5-R2-19), never on an event-in-range claim, where under the
    existential reading both bounds can hold at once (on open cards; F5-R4-02). A k = 0 V row built from any other plain comparison is not generated.
  - S6 SQuAD 2.0 and MuSiQue: C3, C5 or C6 ("fails to answer", "lacks an answer to", "is unanswerable from"), alone or
    under C1/C2; k = 1-3.
  - S6 2Wiki, GHC and EDOS (C1/C2 only): a C1/C2 chain whose negation sits at a different syntactic position than in
    N and D (sentential frame vs verbal "not" vs both: a scope-position shift), k = 1, 2 or 3; V never repeats N's or
    D's exact template sequence on that base (asserted). These datasets keep 4.2 rows per base (spec 2.2's 4 rows in 2
    units); their k = 3 V rows are deep items.
  - The V k-mix in section 8 is pooled over all samplers; S6 V rows have no k = 0.
- **Probe hold-out.** 25 question-side templates, drawn by a stratified seeded draw: at most 1/3 of any family's
  templates, at least 1 from each of at least 10 families; frozen with sha256 logged before any training row.
- **Never trained (program block, 7.2 method 8):** everything in the 3.4 banned list that is a dev, eval or attack
  wording; the dev held-out template family (`dev_negwords`). CondaQA and BoolQ (forbidden list) are never a template
  or base source.

## 5. Samplers

Shares are of bases (r2 rows in brackets are cumulative, at the x1 placeholder). The per-sampler cap of 2,500 rows
over both rounds counts the cumulative r2 total: at x1, S1 has 1,584 rows, S2-S4 1,440 each and S6 1,296; at the 12%
maximum (10,860 rows), S1 has 2,389, S2-S4 2,172 each and S6 1,955 at target shares; the cap is asserted per
sampler on the final selected set, and the section-8 remedy handles drift (F5-R2-14). Shares are checked on the final
selected set (+/- 2 pp, section 8).
S1-S5: invented entities from a domain pack (O*NET persona seed, never PersonaHub).
S6: real text and entities; the pack slot holds a Claude-written wrapper pack (setting, role, document framing; O*NET
seed), so S6 cards still differ in pack and in rule set (dataset line x definition variant; 3.1, SC10). Decisive item position
uniform. Per-card base rate as in section 8.

**Base depth (F5-R1-16)** is defined per sampler below; default 1-2, depth 3 = deep (section 8).

**S1 Rule-case, forward (22%, about 1,580 r2 rows).**
- Structure: 2-6 rules over 3-8 case attributes (yes/no, threshold, date, category with SEM-17 value set), 0-2
  weak exceptions (SEM-15; attached only to "if ... then" rules or, as "except when", to rules with no condition;
  F5-R4-07), optional role and action table (role x action -> required / permitted / forbidden): each cell is an
  unconditional "must" / "may" / "must not" rule, and no listed rule is about a (role, action) pair the table lists
  (asserted), as the SEM-24 card line states (F5-R5-03). Rules are read at the atom level, written rule heads are
  positive, "not"-negated, SEM-18 affixed or SEM-24 modal (F5-R5-01), and deontic rules use only the
  SEM-24 shapes (SEM-02, SEM-05, SEM-06, SEM-24; F5-R4-01). Rule graph acyclic and stratified; KB satisfiable
  (asserted). Base: an outcome or deontic status. World: closed 60%, open 40%.
  On closed cards the case text gives every number, date and category attribute a value or "not recorded" (SEM-02,
  F5-R3-07); a yes/no attribute in prose is stated or false.
- Solver A: forward chaining with weak exceptions; closed cards by negation as failure (a rule that gives a negated
  atom is checked as a constraint, never used to derive; F5-R4-01); open cards by unit
  propagation over the ground clauses (modus ponens and modus tollens, so contrapositives and "only if" are used);
  then a direct LF model check; deontic status by the SEM-24 closure (permitted = not forbidden). Solver B: z3 (MIT)
  on the parsed rules; on every card that shows SEM-24 the closure is added as definitions before completion
  (SEM-24, F5-R3-01); closed cards then add Clark completion (over stated facts and rule-defined predicates, never
  over "permitted" or "required"; an unrecorded value stays a free domain variable, SEM-04); gold = Yes iff KB and
  not-LF is unsat, No iff KB and LF is unsat; both sat or both unsat fails G2.
- **Amount sub-shape (F2 structure, spec 2.2; about 25% of S1 bases).** A rule sets an amount or a date for the case
  through a cap, a floor, a tier table or a stated day offset. The case value follows by comparison only (min / max /
  tier lookup, or a date plus a stated day count); no multiplication, proration or rounding (SEM-12). The base is a
  bound or date claim on that value (SEM-08, SEM-11). Tier tables partition their range ("up to <N1>", "more than
  <N1> and up to <N2>", ..., "more than <Nk>"; asserted, SEM-08) and day offsets are written "<N> days after <D>"
  (SEM-11), so the boundary items (30%) have one tier and one date (F5-R3-12).
- Base depth: the number of rule applications on the decisive derivation of the base value (1-2; 3 = deep).
- V variants: modal shift, "at least <q> of the conditions" (only on rules whose "if" clause is a flat conjunction of
  2-4 literals with no attached exception; SEM-07, F5-R3-08), connective negation, antonym over the value set,
  "barely", the bound complement (section 4, V rows).

**S2 Event log, target-first (20%, about 1,440 r2 rows).**
- Structure: 5-20 dated entries on 2-6 entities (create, renew with duration, transfer, CORRECTION, VOID, implicative
  entries, notices from authoritative and non-authoritative sources). States per SEM-33 (holder, status and validity
  are separate states; an item with a renewal entry has no status entries; F5-R3-04; an item has no status before its
  first remaining status entry, and every status question asks a day on or after it, SEM-17, F5-R4-04), corrections
  per SEM-16 (a CORRECTION changes only value fields, never a date, entry type, item ID or named actor; F5-R4-06),
  covered period printed (SEM-27). Every action entry names its actor, and the actor of a renewal or transfer is the
  item's holder (SEM-33, F5-R5-07). Every entry's date, entry type, item ID and (on an action entry) actor always hold a value, in both
  worlds (F5-R5-05). On closed cards every entry gives every field of its entry type (SEM-02, F5-R3-07). Text-side
  "never", "no longer" and "still" entries are statements that set no state, and those by <S> agree with replay
  (SEM-26, F5-R5-04).
  Pick v(P) first, place the decisive entry at a uniform position, then add look-alike-ID distractors. Base: a state
  at the asked time or an event inside a date range (existential, SEM-11; every listed event of the asked kind for the
  asked entity lies on one side of each asked boundary date, asserted, F5-R4-02; at least one such remaining listed
  event exists, asserted, F5-R5-02); training S2 has **no stance bases** (a stance question is
  opaque, so it is asked only as a V row, inside the section-8 no-polarity budget; SC7). World: closed 70%, open
  30%. Open cards decide an event-in-range claim Yes from an <S> entry and No only from an explicit <S> statement that
  no such event occurred in the range; they decide a state only from an "as of" statement by <S>, which equals the
  SEM-33 replay of the listed entries for that day (asserted in both worlds, F5-R5-06).
- Date offsets ("<renewed / valid> for <N> days", SEM-33) are the F2 calendar shape in F5; the day count is always
  stated. Failure or refusal cues without "by <D>", dated entries included, follow SEM-19 (no <X> entry for that
  entity anywhere in the covered period, asserted for every such cue; F5-R2-06). No privative (C5) in S2 text or
  questions (SEM-19). Each CORRECTION or VOID names an entry by its own author (SEM-16). Stance questions (C7,
  question side) only on closed S2 cards, never naming <S> as the asked party, never about a <P> on which the asked
  party has a VOID or CORRECTION, only with a <P> that is a timeless fact or an event (never a SEM-33 state), and
  only when every statement the asked party made about that entity and attribute literally states <P> or literally
  states that <P> is false, or the party made none (SEM-20, F5-R3-11, F5-R4-03). No party makes two statements about one fact on one date (asserted). A state question states no time
  other than "as of <D>"; range words go only with events and single-date attributes (SEM-11).
- Base depth: 1 + the number of CORRECTION / VOID links followed from the decisive entry (0-2), so 1-3; a VOID of a
  CORRECTION (depth 3) is deep.
- Solver A: forward event replay. Solver B: backward version-graph resolver (follows CORRECTION / VOID pointers from
  the query) on the parsed log, with its own LF evaluator.
- V variants: temporal aspect, date bounds (on an event claim a negated date word, k = 1; the bound complement only on
  a single-valued date, section 4), report-verb stance vs fact (no-polarity, inside the section-8 budget),
  implicative swap.

**S3 Fact graph, label-first (20%, about 1,440 r2 rows).**
- Structure: ground atoms, 2-6 strict universal statements with an explicit quantifier ("Every <A> is <B>", "No <A>
  is <B>"; no bare generics), explicit negative facts, 1-2 hops, distractor facts and rules, one inert relevant-looking
  sentence on 30% of bases. At most 18 ground atoms after grounding every universal over every entity of the base
  (larger bases rejected). Pick v(P), build its proof, assert the opposite is not derivable. Claim-text lexical
  overlap is balanced against the label (HANS control). World: open 60%, closed 40%.
- Solver A: forward chainer (stratified negation on closed cards; unit propagation with contrapositives on open
  cards). Solver B: model enumeration (truth tables) on the parsed text; closed cards enumerate models of the
  completion.
- Base depth: the number of universal-statement applications in the proof of the decisive value (1-2 hops; 3 = deep).
- V variants: quantifier scope, contrapositive form, privative or affixal cue.

**S4 Records, table-first (20%, about 1,440 r2 rows).**
- Structure: 5-30 records x 3-8 fields (category, number with unit, date, yes/no, some blanks per SEM-04) as markdown,
  CSV, JSON, YAML, key-value or log lines. Every record renders every field: a value, "not recorded" / null, or (yes/no
  only) blank; no key, column or field is ever omitted (SEM-02, F5-R3-07; G3 rejects an omission). Base: a quantified
  claim over a filtered subset: all, some, at least / at most <q>, more than half (polar operators), and exactly <q>,
  highest, lowest, only (non-monotone operators: together <= 1.5% of all F5 bases, about 7.5% of S4 bases, inside the
  section-8 no-polarity budget; SC7). "None" and every other negative operator are not A-row
  base operators (section 4, A rows); "none" is the N row of a "some" base. Every question names its filtered subset
  explicitly, and that subset is the comparison set for quantifiers, counts, "only", "other than" and superlatives
  (SEM-13, SEM-22, SEM-23). <q> sits at the true count on 30% of items.
  **World: closed 100%** (open S4 is dropped: an extract decides "some" only as Yes and "every" only as No).
- Solver A: Python set comprehension on the generator's records. Solver B: sqlite on the parsed table, LF compiled to
  SQL by an independent compiler (COUNT, NOT EXISTS; yes/no blanks COALESCE to FALSE). The parser keeps a blank
  distinct from "not recorded" / null; an unrecorded entry is a free domain variable, asserted non-decisive
  (SEM-04): solver B re-runs the compiled SQL once per SEM-04 test value substituted for each unrecorded entry (for a
  number or date, the thresholds and dates of the question and every other member's value of that field, each with
  one step on either side; for a category, every category value the question or its filters name, every other
  record's value of that field and one fresh value; for a yes/no entry, yes and no; F5-R4-05) and must get one
  answer, and no unrecorded entry sits in the measured field of a superlative's or two-entity comparison's comparison
  set (F5-R3-06).
- Base depth: the number of filter conditions that define the subset (1-2; 3 = deep).
- V variants: "no" vs "not any", the bound complement ("fewer than <q>" or "at most <q - 1>" for an "at least <q>"
  base), "other than", "only", graded negatives, the "barely" form.

**S6 Public human-gold bases, text-first (18%, about 1,300 r2 rows; <= 30% from any one dataset; GHC + EDOS <= 35%;
2Wiki <= 1.5% of all F5 bases, about 8% of S6, because its comparisons have no polarity (section-8 budget, SC7)).**
- Sources: SQuAD 2.0 (answerability, SEM-29), MuSiQue (answerable vs unanswerable, SEM-29), 2WikiMultihopQA
  (comparison and yes/no types only; a program converts the template question to a declarative `<P>` from its type,
  finds each compared value in the kept supporting paragraphs, computes the answer from those paragraph-stated values,
  and skips anything it cannot parse or whose paragraph values do not reproduce the dataset answer; SEM-32,
  F5-R3-03), GHC and EDOS
  (SEM-30). Bases whose quoted source question or program-converted claim holds any L_neg entry (3.4, lemma match)
  are skipped (F5-R1-10).
- Base depth: SQuAD 2.0, GHC and EDOS 1; 2Wiki 2; MuSiQue the record's hop count, with 2-hop records as the default
  and 3- or 4-hop records counted as deep. V rows as in section 4 ("V rows").
- **Labels (all hard in round 1).** GHC: the builder reads `ghc_train.tsv` only (spec 3.2 #16; never the
  annotator-level file, which holds test-split annotations); P = "hateful" = the file's HD label or its CV label. The
  builder confirms from the dataset's own README that these columns are the annotator-majority labels; if not, GHC
  leaves S6 and its share moves to the other S6 datasets. EDOS: both labelled CSVs are read only through the
  `split == train` filter; P = sexist; only unanimous posts (p = 0 or 1) are bases, so the 1/3 and 2/3 votes are
  skipped. SQuAD 2.0, MuSiQue, 2Wiki: the dataset's own label.
- Rules: train split only; Wikipedia sets on the train side of the page split; passages deduped against C1's `qnli`,
  `gd_answer_equiv`, `gd_hotpotqa_yesno`, `gd_feverous`, `gd_totto_claims`, `gd_wtq` and `boolq` (spec 3.1; a hit drops
  the base); unused records only (not in golden_train, not in any other C row) through the record ledger shared with
  the public and codebook builders; SQuAD ids on MuSiQue's dev/test drop list are dropped; GHC and EDOS deduped vs
  HateXplain and Social Bias Frames. MuSiQue / 2Wiki keep every supporting paragraph and only as many whole
  distractor paragraphs as fit the token cap.
- **Caps.** Every F5 S6 row counts toward its dataset's 3,000-row cap and toward the per-class cap in the record's
  original human class (answerable / unanswerable, hateful / not, sexist / not, 2Wiki answer). The ledger holds each
  dataset's room after the public block and the codebook rows have reserved their allocations; F5 takes only the room
  left, and a dataset with no room passes its S6 share to the other S6 datasets, then to S1-S4.
- Solver A: human label from the generator's record + LF truth table. Solver B: reads the original record by id with
  its own loader (not the generator's cache), parses the rendered question to LF with the cue grammar, evaluates by
  truth table.
- **Not used:** QuALITY and Qasper. Spec rules block them: their articles and papers exceed 2,000 tokens, so a 3-row
  unit 1 is not allowed (2.1, G15); turning a QuALITY option into a yes/no claim needs the banned label-check form or
  LLM-written text (3.1); Qasper questions are free-form and need a model to negate. Their share goes to the five
  sources above. They return only by a PREREG amendment that answers these rules.
- Deny-list parents declared: SQuAD 2.0 -> Wikipedia; MuSiQue -> SQuAD, T-REx, Natural Questions, MLQA, Zero Shot RE,
  Wikipedia; 2Wiki -> Wikipedia, Wikidata; GHC -> Gab posts; EDOS -> Gab (pushshift), Reddit. The builder refuses to
  run on any `taint` hit (3.H).

**S5 Held-out: correspondence thread (mix-tuning dev only, 400 items = 100 bases x 4 rows; never a training row).**
- Rows per base: A, N, D and V only; **S5 has no attack twin V'** (F5-R2-21). MR10 is tested on training samplers.
- Shape: 4-12 messages among 2-5 invented parties. The card names <S> and shows SEM-31 and SEM-27. Messages assert,
  deny, retract and correct facts. Base: a fact or a stance at thread end (stance = the party's latest remaining
  statement, SEM-20; stance bases only on closed S5 cards, never about a <P> on which the asked party has a retraction
  or correction, never naming <S> as the asked party, and only with a literal <P>: every message of the asked party
  about that entity and attribute states <P> or that <P> is false, or it sent none; F5-R3-11, F5-R4-03). No two messages by one party about one fact share a date, no
  retraction or correction by a party shares a date with a message by that party about that fact, each retraction or
  correction names a message by its own sender, a retraction or correction is dated after the message it names, and
  on a fact base a correction by <S> about the asked fact names <S>'s latest message about it (asserted, SEM-31,
  F5-R3-05). A corrected message keeps its own date; retractions and corrections are not messages about the fact.
  No privative (C5) in S5 text or questions (SEM-19), and no text-side "never", "no longer" or "still" (SEM-26,
  F5-R5-04); every message's date and sender always hold a value (F5-R5-05). Base depth: 1 + the number of
  retraction or correction links followed (report only). Training cue templates only (minus the 25 probe templates),
  held-out packs, the 50 held-out format styles.
- Solver A: thread replay with the SEM-31 rules. Solver B: z3 over the parsed statements with the SEM-31 constraints.

**Hard-negation probe (400 items, report only; sizes F5 for round 2).** S1-S4 base shapes with held-out packs and
styles. Every item contains at least one of the 25 held-out templates, and no other cue in the item comes from that
template's family; template ids are logged per item (16 items per template). Yes rate 50% per template and per k.
Probe and S5 share no item, pack or style with training.

## 6. Round-trip parse plan (G3, 100%)

1. **Structure parser**, written from this spec (not from the renderer): prose grammar for rules, logs and facts;
   standard readers for CSV, JSON, YAML and markdown tables; a line grammar for logs. S6: the quoted source block equals
   the source's kept paragraphs, each byte-equal to the normalized source paragraph, in source order; the kept
   paragraph ids are logged. Attack spans (MR10) sit outside the quoted block. On closed cards the parser rejects any
   omitted key, column, field or case attribute (SEM-02, F5-R3-07); it rejects any tier table that does not partition
   its range under SEM-08 (F5-R3-12); on 2Wiki it re-finds each compared value in the kept paragraphs with its own
   parser and must reach the stored values and gold (SEM-32, F5-R3-03). In both worlds it rejects an S2 entry whose
   date, entry type, item ID or named actor, or an S5 message whose date or sender, is unrecorded, null or blank
   (F5-R5-05); it reads each action entry's named actor (F5-R5-07) and parses "as of" statements and text-side
   "never" / "no longer" / "still" entries as statements, never as state-setting entries (F5-R5-04, F5-R5-06).
2. **Question parser**: a cue grammar written from the section-4 signatures and the 3.4 lexicons. It maps the question
   to LF (operator chain + reference to `<P>`) and recomputes k, j_q (3.4 counting rule) and the polarity of every
   slot (section 4 monotonicity table). At bank build every template must parse to its declared LF, k and slot
   directions (template lint, 100%; a failing template is dropped, never patched by hand).
3. **Card parser**: maps each card line to its SEM key through the frozen rendering registry (3.3); recomputes the
   base's trigger set (3.1: the trigger table over the parsed program-written text and questions of every row of the
   base, plus the structural triggers; card lines and quoted source text never trigger) and checks that every
   triggered key is printed, that a short card prints exactly SEM-01, the world line and the triggered keys, and that
   all rows of the base (both bases of a contrast pair) carry the identical card. "Used" means "triggered"; no check asks which key a solver used.
4. Solver B re-solves (parsed structure, parsed LF, parsed SEM bundle) and must equal the stored gold on 100% of rows.
   Any mismatch stops the generator (fix, regenerate all).
5. **Loader round-trip (G15; F5-R5-09).** Every row passes fmt1 `loader_check` (cygnet, `schema_branch_mark`, the
   pinned `decoder_io` and `train_decoder.check_rows`) with its `must_show` strings: the card is printed whole, no
   card line is "- Yes: " / "- No: ", gold 1 / 0 maps back to the Yes / No option under a random letter order, and the
   served prompt (instructions counted twice) is < 1,900 real tokens (section 1). Any failure stops the generator.

## 7. Metamorphic relations (G4: 100% pass on >= 1,000 rows per sampler; Hypothesis property tests)

| MR | Change | Expected | Samplers |
|---|---|---|---|
| MR1 | Insert one contradictory NOT at the outermost scope | Gold flips | all |
| MR2 | Insert a NOT-NOT pair ("not non-P") on a SEM-18 predicate | Unchanged | S1-S5; S6 SQuAD, MuSiQue |
| MR3 | Swap a cue for another template with the same signature and k | Unchanged | all |
| MR4 | Add an inert sentence with a negation cue that restates a fact of M, or states a fact about an entity outside every restrictor set, count and superlative domain of LF (asserted) | Unchanged | S1-S5 |
| MR5 | Rename entities / IDs; reorder rules, records, or log entries in the listing (dates unchanged); change container | Unchanged | S1-S5 |
| MR6 | Add a SEM-28 decoy with a determined-true <B> in an inert clause | Unchanged | S1-S5 |
| MR7 | Lower <q> in "at least <q>", raise it in "at most <q>", widen a date range on an existential claim | Run only when every operator on the path from the LF root to the changed operator is up or down in the section-4 monotonicity table (no non-monotone or opaque operator of that table, so never under "only", "exactly", numeric "between", "barely", superlatives, two-entity comparisons, "all except", "no longer", a stance verb or a value test). Even polarity (an even number of down operators on that path): never Yes -> No; odd polarity: never No -> Yes | S1, S2, S4 |
| MR8 | Replace NOT(<v1>) with "one of" the other listed values | Unchanged; replacing it with one antonym <v2> is unchanged iff the true value is <v1> or <v2> | S1, S2, S4 |
| MR9 | Closed -> open card with every minimal support set of the decisive value (positive or negative) stated explicitly | Unchanged; deleting one member of every minimal support set on the open card must make the generator reject the base | S1-S3 (stance rows excluded: they exist on closed cards only) |
| MR10 | Inject an attack instruction (S6: only in a wrapper field outside the quoted source block) | Unchanged (`inv`) | S1-S4, S6 (training samplers; S5 has no V') |
| MR11 | Remove a non-supporting paragraph | Unchanged | S6 MuSiQue, 2Wiki |

## 8. Balance targets (G10) and selection

- **Cue count.** Spec 2.2's P(yes | number of negation cues) = 0.50 +/- 0.02 is checked with the shared negcount
  k_all (= j_q; XF02) under "Surface tokens" below. F5's own operator count k (`k_neg`) is a family-local count kept
  for polarity logic (N / D construction, the XOR identity, the V k-mix) and checked in addition: P(yes | k) = 0.50
  +/- 0.02 for k = 0, 1, 2, 3; it never replaces a negcount count in any quota or G10 cell (SC8). V and V' rows, **pooled over all samplers**
  (F5-R1-14): k = 0 about 10% (only the listed k = 0 forms of section 4, all from S1-S5; S6 V rows have k >= 1), 1 about
  40%, 2 about 30%, 3 about 20%. Overall: k = 0 about 27%, 1 about 35%, 2 about 32%, 3 about 6%. P(yes | t_txt) = 0.50
  +/- 0.03 in buckets 0, 1, 2, 3, 4+ (F5-R2-20).
- **Count buckets (F5-R2-20).** j_q, j_t and t_txt are checked in buckets 0, 1, 2, 3, 4+. A bucket cell needs >= 200
  rows; a smaller bucket is pooled with the adjacent bucket toward 0 (bucket 0 with bucket 1) for the check, and the
  pooling is logged.
- **Depth and deep items (F5-R1-16).** `meta.depth` = the base depth (section 5, per sampler); `meta.deep` = true iff
  k = 3 or base depth >= 3. Bases of depth >= 3 (incl. 3- and 4-hop MuSiQue) are <= 4% of bases, so deep rows stay
  <= 10% of rows (asserted; spec 2.1). **Depth-cap lever** (spec 2.1: more than 30% hard rows after the G5 re-read
  lowers the cap), applied in this order and logged: (1) drop bases of depth >= 3 (3- and 4-hop MuSiQue included); (2) lower the
  default maximum base depth from 2 to 1 **on S1-S4 only** (F5-R2-16; S6 depths are fixed by dataset, so 2Wiki and
  2-hop MuSiQue bases stay, and S5 is held out); (3) drop k = 3 V rows (their share moves to k = 2).
- **Double negation (XF02, SC8)** = a row with negcount **k_all >= 2** (it always has its A row as affirmative twin);
  spec 2.2's floor "at least 25% of F5 rows are double negation" is checked on this count, on the final selected set.
  Every counted operator carries its own L_neg entry, so k_all >= k on every row (asserted per template at bank build
  and per row by negcount): all D rows (k = 2) give 23.8%, V and V' rows with k >= 2 add about 14 pp, and k = 1 rows
  with a second L_neg entry (a decoy, "barely") add a little more, so about 40%; the generator asserts >= 30%.
- **Spec 2.1 negation quotas (XF02, SC8)** use negcount **k_syn**: k_syn >= 1 on >= 10% of F5 yes/no rows, and k_syn
  >= 2 with an affirmative twin on >= 2%. Because C3, C5, C6, comparator entries and "it is false that" have k_syn 0,
  the generator builds the D row of >= 15% of bases (about 3.6% of rows) from two L_core-bearing cues (C1 "not" /
  "no", or C2 "it is not the case that"; never a comparator entry or "neither ... nor", so the open negcount N1
  question cannot move it); both quotas are asserted on the final selected set.
- **Surface tokens.** P(yes | j_q) = 0.50 +/- 0.02 for j_q = 0, 1, 2, 3, 4+; P(yes | j_t) = 0.50 +/- 0.03 in the same
  buckets (count buckets above). Decoys (question or
  text) on >= 10% of rows (all from S1-S5).
- **Balance cells.** P(yes) = 0.50 +/- 0.02 per row type (A, N, D, V), per sampler, and per instruction wording (the
  2.1 wording pool; balanced by construction across cards). +/- 0.03 per cue family (cells >= 200 rows; per-template
  v(P) balanced by construction), per world cell (closed, open, S6), per negation location (none / question only / text
  only / both, by j_q and j_t; text-side negation on >= 30% of rows), per SEM key printed, and on A rows per (base
  operator type x world).
- Verbatim-overlap control (F5-R2-20): of the rows with j_q >= 1, >= 15% have the question's negated clause (the
  clause under its L_neg entry) also verbatim in the text; yes rate on those rows 50% +/- 3.
- **"Yes = bad outcome" (XF04)** 50% +/- 5 over **all F5 yes/no rows** (the v4 2.1 denominator, as every family reads
  it). Packs tag every predicate good / bad / neutral. The S6 predicates are tagged: "unanswerable" (SEM-29),
  "hateful" (GHC) and "sexist" (EDOS) are adverse (bad); their opposites are good. Rows with no polarity (a neutral
  predicate such as a 2Wiki comparison, or <P> under a non-monotone or opaque operator of the section-4 table) are capped at **5% of
  F5 yes/no rows** (the training rows; S5 dev items are not C rows) and count as not-bad. **No-polarity budget (SC7)**,
  set so the cap holds by design, each item a share checked on the final selected set:
  (a) 2Wiki bases <= 1.5% of bases (S6 section); (b) S4 bases whose base operator is non-monotone ("exactly <q>",
  "highest", "lowest", "only") <= 1.5% of bases, their S4 share going to "all", "some", "at least / at most <q>" and
  "more than half" (S4 section); (c) no stance bases in training (stance is opaque; S2 section); (d) no-polarity V and
  V' rows on otherwise polar bases (C17 antonym and "one of", "barely", "only", "all except", "no longer", "exactly",
  "either ... or ..., but not both", superlatives, two-entity comparisons, numeric "between", stance) <= 1.5% of
  rows; (e) every S1-S4 base <P> uses a predicate its pack tags good or bad, never neutral (asserted), so S1-S4 add
  no neutral-predicate rows. All rows of a base in (a) or (b) have no polarity, so (a)-(d) sum to at most 4.5% of
  rows, leaving 0.5 pp for selection drift. The generator asserts <= 4.5% on the generated set; on the final set a
  share above 5% drops whole no-polarity bases (most easy rows first) and replaces them with polar bases of the same
  sampler, then selects again. F5 therefore needs no 2.1 amendment and never sets its own denominator. **A row is yes-is-bad
  when a "Yes" answer asserts that the bad predicate holds or that the good predicate fails** (F5-R1-15): with the
  polarity of <P> in the row's LF from the section-4 monotonicity table, yes-is-bad = (<P> bad and even polarity) or
  (<P> good and odd polarity). k parity is never used. Rows where <P> has no polarity (it sits under a non-monotone or
  opaque operator of the section-4 table) are no-polarity rows: inside the 5% cap and the budget above, counted as
  not-bad (XF04).
- **Antonym-is-not-negation cases (F5-R2-12).** C17 V rows use value sets with n_vals >= 3. On at least half of the
  C17 rows whose gold is No (so about 25% of C17 rows), the true value is a third listed value: neither the base value
  nor any value the question names. A-row value tests and N and D rows do not count (C17 is V only). Bound and date
  items: >= 30% exactly at the boundary.
- **Per-card yes rate (K01, SC3, F5-R2-15, CF-4).** Each training card draws its row-level yes rate **r_card uniformly
  from 20-80%** (spec 2.1) and realizes it exactly, in antithetic pairs (r_card, 1 - r_card). Every F5 card has its own
  pack (XF09), so pairs are formed over the card list, inside each (sampler, world cell, inverted or not) cell; the
  training card count is even and the leftover cards of odd cells are paired with each other (seeded draw), so every
  card has an antithetic partner and every r_card is uniform on 20-80%. Two levers realize r_card:
  (1) **attack share** f_card = max(0.15, 1/r_card - 4, (4 r_card - 3)/(1 - r_card)): 15% of the card's training
  bases get a V' when r_card is in 24.1-75.9%, rising to 100% at 20% and 80%; which bases get a V' is a seeded draw,
  independent of v(P) and V gold; (2) **gold rate** a_card = (r_card (4 + f_card) - 1)/(2 + f_card), set as both the
  A-row v(P) rate and the V-row gold rate (exactly 0 or 1 in the end ranges), exact to one base on the generated set.
  N and D follow from A (spec 2.2), so the realized row-level rate is (1 + a_card (2 + f_card))/(4 + f_card) = r_card
  on the whole 20-80% range (at 20%, every base has a V' and only its N row is Yes). Antithetic partners share f_card
  and have a_card(1 - r) = 1 - a_card(r), so V' rows, like every row type, are 50% Yes over the family (G10: attack
  present uncorrelated with the label). Over the card list E[f_card] = 0.204, so about 20% of training bases carry a
  V' and attack rows are about 4.9% of rows (spec 2.1 "about 5%"). Paired bases (below) count in these rates like any
  base. **S5 dev cards** (not C rows; no V') draw r_card uniformly from 25-75%, which 4-row bases reach exactly with a_card =
  (4 r_card - 1)/2.
  **G7 row cap (F5-R2-15).** Every pack word is unique to its card, so it sees the card's realized rate. A card keeps at
  most the number of selected rows n at which a feature present on every row at that rate still passes G7's one-sided
  Bonferroni binomial with F5's feature count (about 65 rows at 20% or 80%, about 90 at 24% or 76%, with 50K
  features, inside the spec's 128 maximum); a card above its n drops whole bases (whole pairs), most easy rows first.
  **G10 aggregate:** 50% +/- 2 per family x wording x row bin x negation count, where the negation count is k_all
  (= j_q; XF02); F5's own P(yes | k) check above also holds. No amendment is needed (CF-4).
- **Contrast pairs (XF03; CF-4).** On every non-inverted S1-S4 card a share p_card = min(c, 2 a_card, 2 (1 - a_card)) of the
  card's bases are in contrast pairs (a pair gives one Yes and one No on every row type, so a card whose a_card is near
  0 or 1 cannot hold more and still realize its rate; its unpaired bases carry the rest of a_card). c is one seeded
  constant for all cards (about 0.42), set on the generated set so that 22.5% +/- 1 of training rows sit in contrast
  sets, about 29% of S1-S4 bases. S6 bases (real text and human gold; quoted source is never edited), S5 bases and
  probe items are never paired, and neither are inverted cards (their case or record list is in the card, which a
  pair keeps). **Building B'.** From base B, change exactly one input of M, from this closed list: S1
  one case attribute (a yes/no fact, a category value, or a number or date moved across an asked boundary); S2 one
  entry's value field (a holder, a status, a number of days), one entry's date moved across an asked boundary date, or
  one entry removed that no CORRECTION or VOID names; S3 one ground fact switched between stated and stated-negative
  (closed cards: also removed); S4 one field value of one record. The change must flip v(P) and the gold of every A,
  N, D and V row; B' keeps B's card, wording, question templates and every other input, and it is a full base: it
  passes every base assertion of sections 2-5 and both solvers (G2, G3). A change that fails any of these is redrawn;
  if none works, B stays unpaired. V' is drawn per base as above. **Counting (XF03).** The A, N, D and V rows of both
  bases sit in the contrast set: each is a label-flip twin, with its own `call_id`, of the same-template row of the
  other base, built by an input change. V' rows count only toward the attack quota, and the complement / equiv links
  inside a base only toward the negation quotas. Unpaired V rows are built by a question change, not an input change,
  so they are not contrast twins. Contrast-set share = 4 x (paired bases) / (F5 training rows), about 22.5%; 20-25%
  is asserted on the final selected set. **Meta.** The pair shares one `group_id`; B''s A row has `twin_of` = B's A
  row and `twin_kind` "fact_flip"; B''s N, D, V and V' rows point inside B' as in any base; the sidecar holds
  `pair_id` and the change made. **G12:** the two bases are planned twins (spec G12) and are never dropped as
  near-duplicates of each other.
- Attack rows about 5% (per-card f_card above), label-independent over the family. Few-shot cards 5-10%. Definition styles >= 3 (3.3). Short cards on about
  15% of bases (chosen per base, 3.1), so about 15% of rows. **Inverted cards 10-15% of cards** (S1 and S4): the
  yes/no per-case form of "which of these cases meets rule X?": the card lists the cases (S1) or records (S4) and the
  rule that gives <outcome> (on S4 one "if ... then" rule over the record fields, SEM-07), and the question names the outcome itself, never the rule: "Is <case> among the cases
  that are <outcome>?" (F5-R3-09). Gold = whether the outcome holds for the case under the card's semantics (any
  rule, exceptions per SEM-15). "Meet(s) <rule>", "satisfy" and "qualify under <rule>" are not used in these questions
  (lint, 3.4). The generator also asserts, on every inverted card, that for every listed case the outcome holds iff
  the conditions of the named rule hold (no exception fires and no other rule gives the outcome), so a reader who
  reads the question as "the rule's conditions hold" reaches the same label. A negated inverted row puts its negation
  inside a truth frame with C1 or C2 ("Is it true that <case> is not among the cases that are <outcome>?"), never in
  a relative clause of the matrix question (SEM-01; F5-R2-17; lint). Labels are computed as on any S1/S4 row.
- **Selection** (spec 2.1 applied to whole bases, so units stay intact). All rows of a base use one instruction
  wording, drawn per base from the card's >= 5. The crowd scores every row. Base bin = the
  bin of the base's hardest row (lowest crowd p_g), V' included (sidecar `base_bin`; a selection device only). A contrast pair is one selection atom: its two bases share the wording, its bin is the hardest row of either base, it is kept or dropped as a whole, and it is downsampled in its own cells (wording x pair bin x "pair"), since it already holds both v(P) values and both V golds. Keep every base that has a medium or hard row (this
  keeps all medium and hard rows); keep 30% of all-easy bases (all rows, V' included, have p_g > 0.97). Then downsample
  whole bases inside cells of instruction wording x base bin x (v(P), V gold), which is the base-level form of the
  spec's family x gold x wording x bin cell; cue mix = the sorted tuple of cue families in N, D and V is spread evenly
  inside each cell. **Gates use row bins (F5-R2-13):** `meta.difficulty_bin` = the row's own crowd bin, and the
  difficulty quotas, G9's label x bin chi-square and G10's cells all run on row bins. Row-level quotas after
  selection: easy <= 25%, medium >= 45%, hard <= 30%, and G9's label x row-bin chi-square p > 0.01. **Remedy when a row-level difficulty quota fails (F5-R1-17)**, inside the spec's own downsampling
  step and without changing the spec's 30% keep rate for all-easy bases: (1) inside each cell, the downsampling drops
  whole kept bases with the most easy rows first (ties by seeded draw) until easy <= 25%, or until the cell reaches its
  row floor; (2) if medium < 45% or hard > 30%, or step 1 empties a cell below its floor, generate more bases for that
  cell (from cue families and samplers whose bases score medium) and select again. If a G10 cell (wording x row bin
  x k_all x gold) fails, generate bases whose rows land in that cell (chosen by the sampler, cue family and row type
  whose scored rows fall there) and select again. Never drop single rows from a unit, or one base of a pair. Rows with crowd p_g < 0.05
  enter the G5 re-read.
- **Targets are checked on the final selected set (F5-R2-14),** never on the generated bases, with these tolerances:
  sampler shares of bases +/- 2 pp (S6 per-dataset caps unchanged); world shares per sampler +/- 3 pp; short cards
  15% +/- 3 of bases; inverted cards 10-15% of cards; cards >= 80 / 150; each card's realized row-level yes rate
  within +/- 5 pp of its r_card (within one base for a card with fewer than 20 selected bases); deep rows
  <= 10%; depth >= 3 bases <= 4%; attack rows 4-6% of rows; contrast-set share 20-25% of rows (XF03; below 20%,
  generate more pairs for the short cells and select again; above 25%, the downsampling drops pairs before unpaired
  bases in the cells where it drops). Every drop inside a cell (the F5-R1-17 easy-first drops included) is spread over
  cards in proportion to their kept bases; inside one card the stated order applies (most easy rows first, ties by
  seeded draw). A miss is fixed by generating more bases for the short sampler, world, card form or card and selecting
  again. **Per-sampler cap:** asserted on the final cumulative selected set; a sampler above 2,500 rows (only S1 can
  get there, at the 12% maximum with +2 pp drift) drops whole bases, most easy rows first, down to 2,500, and the
  room goes to S2-S4 bases generated and selected the same way.

## 9. Shortcut controls and other gates (F5 specifics)

- **G6** metadata features add: row type, k, t_txt, j_q, j_t, cue families, negation location, world cell, decoy
  present, base depth, deep, card form (full / short), truth frame present, template id, sampler, yes-is-bad, SEM keys
  printed, attack twin present on the base, contrast-pair member. Folds are grouped by `card_id` (a card's rows never
  span folds), because per-card yes rates vary 20-80% by design (spec 2.1, G10) and a card's own rate is not a
  transferable shortcut; random-fold accuracy is reported, not gated. Per-template and per-wording balance by
  construction keeps question-only and pack words at chance across cards.
- **G5.** 600 program rows (S1-S4): zero confirmed wrong golds; ambiguous <= 1%; readers get the card and text only.
  **S6 rows (SC2)** are judged under the spec's public rule, dataset-level only: 100 rows per S6 dataset, 300 for
  SQuAD 2.0 (spec G5 and 3.2 #1); when F5 holds fewer rows of a dataset than that (for example about 190 SQuAD 2.0
  rows in round 1), the read is a census of all of them. Drop bars: SQuAD 2.0 if > 5% of rows are **wrong or
  ambiguous** (spec 3.2 #1, the dataset-specific and stricter rule); every other S6 dataset if > 8% clearly wrong
  (spec G5). A drop is a decision about the dataset ("drop the set", spec 3.2 #1): a failure in F5's read **or** in
  the public block's read of the same dataset drops that dataset's F5 S6 rows and, through the orchestrator (section
  10), its public rows; F5 drops only its own rows itself, and its share moves to the other S6 datasets, then to
  S1-S4. A flagged S6 row whose error traces to the polarity transform, the parse or the conversion (not the human base
  label) is a generator bug: zero tolerance.
- **Provenance.** S1-S4, S5 `meta.licence` "CC0 1.0 (program-generated)". S6 rows: the dataset licence, `text_source`
  {dataset, record_id, split: "train"}, SA flag where it applies (SQuAD 2.0 and every MuSiQue row SA; 2Wiki Wikipedia
  text SA; GHC CC BY 4.0; EDOS CC0), notices-file entries. SEM-30 definitions are Claude-written summaries, so no
  guideline text is copied and no guideline licence is needed.
- **Row format 2.4 unchanged.** Raw fields as in section 1 (F5-R5-09): `qtype` "noul", `gold` 1 / 0, no `options`
  list; `state`, `card` and `instructions` as placed there. `meta.twin_kind` uses the spec-2.1 vocabulary: "negation"
  for N, D and V; "attack" for V'; "fact_flip" for the A row of a contrast pair's B'. `twin_of`: N, D and V point to
  the A row of their base; V' points to V; an A row has none, except B''s A row, which points to B's A row (section 8).
  `meta.depth` = base depth and `meta.deep`
  = (k = 3 or base depth >= 3) (section 8). `meta.difficulty_bin` = the row's own crowd bin (F5-R2-13). The polarity record (row type, k_neg, t_txt, j_q, j_t, families, template
  ids, truth frame id, polarity of <P>, location, world cell, card form, SEM keys printed (trigger set), base depth,
  v(P), yes-is-bad, base id, base_bin, pair_id and the pair's change) goes in the sidecar
  `data/c_parts/F5_polarity.jsonl`, keyed by row id; r_card, f_card, a_card, p_card and c go in the same sidecar, keyed
  by card id. The QC allow-list for G6, G7 and G10 names this file; the mixer
  never copies it into training rows.
- **Cross-family G12 (XF11).** F5 keeps its independence: it re-implements the shallow F1-F4 and F9 structures it needs
  and imports no other family's generator (F1 reserves no seed range for F5; F9 writes no export). Because structure
  hashes are family-local, the orchestrator runs a cross-family pass: exact text hash plus MinHash of F5 rows against
  F1, F2, F3, F4 and F9 rows. Each near-duplicate pair is dropped from F5.
- **F14 exclusion lint (XF16).** No F5 row poses <F14 task> (bank-build lint and QC check; the orchestrator names F14's
  skill and structure type before generator code and fills in the lint then; provisional instance: no row asks for a
  feasible slot or assignment for several items under pairwise constraints).

## 10. Items for the orchestrator's log (F5 has a default for each and waits for none)

**Items 8-11: closed with no amendment (XF18; CF-4).** PREREG_FINAL A16 and A16.1 record no XF18 amendment, so F5 now
meets v4 2.1 and 2.2 as written instead of waiting for one: the per-card yes rate is realized exactly on the whole
20-80% draw (item 8), 20-25% of F5 rows sit in XF03 contrast sets (item 10), and items 9 and 11 are readings of 2.2
under which nothing is broken. No amendment ID is needed and no F5 row waits for the orchestrator.

1. LICENCE_REGISTER section 3 needs a row: "F5 S6 real-text rows (about 650 / 1,300): the source dataset's licence
   (sets 1, 2, 3, 16, 17)" (K13). This builder does not edit the register.
2. Spec 2.2 ("unit 2 (1 row)") and spec 6 ("a 1-row unit") should read "1 row, or 2 with its attack twin" (K04);
   F5 puts its 2.1 attack twins (`inv`, same `call_id`, about 5% of rows) in unit 2, on a per-card share f_card of
   bases (section 8).
3. GHC is hard-labelled from `ghc_train.tsv` (K11). Soft GHC targets need an amendment that names the annotator-level
   file and a train-id filter applied before any read.
4. G6 fold unit: F5 groups folds by card (K01); the QC agent may apply the same reading to every family.
5. The public block's SQuAD 2.0 allocation (900 per class in r2) already exceeds the generic 500-per-class cap; the
   ledger value is the public builders' call. F5 only consumes the room left (K15).
6. (Replaces the old S7 item; SC1.) No S7 is needed: with round 2 cumulative and F5 <= 12% of own rows, no F5 sampler
   reaches the 2,500-row cap at its target share; selection drift is handled inside F5 (section 8 remedy, F5-R2-14)
   (section 1, K19).
7. G5 dataset-level drops (SC2): if F5's read or the public block's read drops an S6 dataset, the orchestrator applies
   the drop to both blocks; F5 logs every F5-side drop here. SQuAD 2.0's bar is spec 3.2 #1 (> 5% wrong or ambiguous).
8. Spec 2.1 per-card yes rate 20-80% (SC3, K01, CF-4): met as written. Each card draws r_card uniformly from 20-80% and
   realizes it exactly through its attack share f_card and gold rate a_card (section 8); no tail is clipped.
9. Spec 2.2 names QuALITY and Qasper among F5's base sources (SC3, K03, CF-4): met as written. 2.2 lists the sources
   bases may come from and sets no share for any of them, so using five of them breaks no rule; the spec-2.1 / G15,
   3.1 and label-check-form rules (section 5) are why these two are not used. Logged so the public block knows F5
   takes no QuALITY or Qasper record.
10. Spec 2.1 twin quota 20-25% (SC3, K06, CF-4): met as written under XF03. About 22.5% of F5 rows (asserted 20-25% on
    the final set) sit in contrast pairs built by one input change (section 8); the complement / equiv links of the
    spec-2.2 quadruple count only toward the negation quotas and V' toward the attack quota, as XF03 says for every
    family. The QC agent counts F5 like every other family.
11. Spec 2.2 F5 "Labels: a polarity-logic program over the base label" and unit 2 "labelled by polarity logic" (SC5,
    K22, CF-4): met as written. F5's label program composes the question's operator chain over the base proposition
    and evaluates it on the base (on M for S1-S5, by truth table over the human base label for S6); on
    truth-functional chains this is gold = v(P) XOR (k mod 2), asserted on every such row, and the structural
    operators that 2.2's own skill list names (scope shifts, quantifiers, "no fewer than", modal negation) are
    evaluated on the base, which a program over the bare label could not do. Solver B re-derives the LF, and so the
    polarity, from the parsed question, as 2.2 asks.
12. MARKERS.md section 3, F5 row, "Missing key" column (orchestrator-owned; F5-R3-07): it reads "not specified" and
    should read "closed cards: never (every key, field and number / date / category attribute is rendered; G3 rejects
    an omission); open cards: an attribute the text does not mention is unstated, so unknown (SEM-03); both worlds:
    S2 entry dates, types, item IDs and actors and S5 message dates and senders are never 'not recorded' or null
    (F5-R5-05)". This builder does not edit the marker table.
13. XF02 reading for spec 2.2's F5 floor (SC8): "at least 25% of F5 rows are double negation" is checked with negcount
    k_all >= 2 (about 40%, asserted >= 30%), the count XF02 uses for every "number of negation cues" cell; the 2.1
    quotas use k_syn (section 8). A k_syn reading of the floor would need nearly every D row and many k >= 2 V rows
    built only from C1 / C2 cues (D rows alone give at most 23.8%), which removes implicit-cue double negation, the
    family's skill; it would need a spec 2.2 amendment, and F5 keeps k_all until one exists.
14. XF04 (SC7): F5 meets the 5% no-polarity cap by design through the section-8 budget (2Wiki <= 1.5% of bases,
    non-monotone S4 base operators <= 1.5%, no training stance bases, no-polarity V / V' rows <= 1.5% of rows), so
    F5 does not trigger the XF04 amendment. Logged so the orchestrator knows F5's 2Wiki share is about 8% of S6.
15. Spec 2.1 card definition (SC10): "two cards must differ in the domain pack and in the label schema or rule set".
    Every F5 card has the Yes / No label schema, so F5 reads "rule set" as the card rule set of 3.1 (sampler, world or
    dataset line, full key set from the card's cue-family set, and card constants: value sets, status list, deontic
    table, <q> / <m>, S6 definition variant) and asserts that no two F5 cards share one, with cards of one sampler and
    world differing beyond pack words. On S6 the label function is the dataset's, so two cards of one dataset differ
    only in definition variant (same label function, different registered definition text). The QC agent may apply
    the same reading to other single-schema families; an amendment should confirm it.
16. XF07 effect for F5 (SC9): F5's "stricter unanimity rule" is its EDOS rule only. GHC is hard-labelled by the
    majority labels in `ghc_train.tsv` (spec 3.2 #16; K11, item 3); unanimity cannot be applied to GHC without the
    annotator-level file, which F5 never opens. The XF07 rule text may name EDOS when it is next edited.

---

## Resolved ambiguities

| ID | Resolution (one semantics) | Where |
|---|---|---|
| F5-A01 | LF operators are question-side only; text-side cues are part of rendering M and set v(P), never XORed. k = question-side reversals (used for P(yes given k)); t = text-side cue count; both in the sidecar. "Text only" rows have k = 0 | 2.2, 4, 8, 9; amended by F5-R1-15, F5-R1-19 |
| F5-A02 | N and D only from C1, C2, C3, C5, C6 and the exact-contradictory forms of C8 and C13; gold(N) = 1 - gold(A) and gold(D) = gold(A) asserted by direct LF evaluation, never by XOR alone. Antonyms, graded cues, "barely" and every other structural cue go only into V | 2.3, 4 |
| F5-A03 | "Not only <A> but also <B>" = A AND B, with B a determined-true, non-decisive proposition of M (asserted; solver B checks). Evaluated as a conjunction. Banned on S6; MR6 is S1-S5 | SEM-28, 4, 7 |
| F5-A04 | "Barely" is structural (S4 and numeric S1 only): "barely met T" = T <= value <= T + m; "barely stayed within C" = C - m <= value <= C; "meets / reaches N" include N. Never labelled by XOR | SEM-25, SEM-08, 4 |
| F5-A05 | No L_core word anywhere in the matrix interrogative clause (contracted or not, inside a multiword entry too); L_core negation only inside an embedded declarative after a truth frame from the closed list ("Is it true that ...?", "Is the following statement true: ...?", ...); other L_neg cues may sit in the matrix clause. Lint at bank build | SEM-01, 3.4; amended by F5-R1-13, F5-R2-09 |
| F5-A06 | Conditionals, "unless" and "only if" appear only in text (rules); no conditional or hypothetical question, no "would / could / should" in questions | SEM-01, SEM-05/06/07, 3.4 |
| F5-A07 | Bare "either ... or" banned; "or" is inclusive; "not" never directly governs a bare "or"/"and"; negated connectives only as "neither ... nor" and "not both ... and" | SEM-10, 3.4 |
| F5-A08 | Weak reading for every rule-attached exception (the rule does not apply; nothing else follows); SEM-15 no longer says "overrides". Strong reading only for the claim quantifier "all except <A>", which no L_core word directly precedes and which is negated only by C2 (F5-R5-08); "except" never in rule text and claims on one card. Exceptions attach only to "if ... then" rules, or as "except when" to rules with no condition; never to "only if" rules; at most one per rule; each fires SEM-15 (F5-R4-07) | SEM-15, SEM-23; amended by F5-R4-07, F5-R5-08 |
| F5-A09 | Determined iff every model of the KB agrees (solver-B criterion). Solver A uses classical inference on open cards (unit propagation with modus tollens, "only if", negative universals); a base solver A cannot decide is dropped | 2.1, SEM-03, 5 |
| F5-A10 | Rule graphs acyclic and stratified; KB satisfiable (asserted by both solvers). "Both unsat" fails G2 like "both sat" | 2.1, 2.5, S1 |
| F5-A11 | Card (SEM-04): "not recorded" or null = some value the record does not give, on a complete record too; on an open card a blank means the same; on a complete record a blank yes/no entry means no. Never decisive = same label for every domain value, including each threshold and date of the rules or question and every other member's value of the same field (each with one step either side), plus, for a category without a value set, every category value the question, filters or rules name, every other member's value and one fresh value, and for a yes/no entry both yes and no (F5-R4-05), plus the all-statements-false check for values without a value set; no unrecorded value in the measured field of a superlative's or two-entity comparison's comparison set. SQL uses COALESCE(flag, FALSE) for blank yes/no columns on closed cards. Closed cards never omit a key or attribute; S2 entry and S5 message dates (and the other structural fields) are never unrecorded, so they are never SEM-04 variables (F5-R5-05) | SEM-04, S4; amended by F5-R2-01, F5-R3-06, F5-R3-07, F5-R4-05, F5-R5-05 |
| F5-A12 | Refusal and prevention cues (C4) are text-only renderings of NOT X. Question-side C3 means exactly NOT X. "Failed to X by D" = X did not happen on or before D. For a failure or refusal cue without "by D" (dated entries included), no X entry naming that entity as its actor exists anywhere in the covered period (asserted; F5-R5-07). "Failed to" does not imply X was required | SEM-19, 4; amended by F5-R1-02, F5-R1-03, F5-R2-06, F5-R5-07 |
| F5-A13 | "Is missing" dropped from SEM-19. "Cannot" only in deontic rule text on cards that show SEM-24; ability and epistemic "cannot", "can", "could", "unable to" banned everywhere in F5 | SEM-19, SEM-24, 3.4 |
| F5-A14 | Unauthored log entries are records by <S>; each CORRECTION or VOID names an entry by its own author; only <S>'s change facts, and any party's own change only what it stated; they apply retroactively whatever their date; voiding a CORRECTION restores the corrected entry; chains of depth <= 2 only; no conflicting <S> statements about a timeless fact in a log (asserted). A CORRECTION changes only value fields of the named entry, which keeps its date, type, item and named actor (card line; F5-R4-06, F5-R5-07) | SEM-16; amended by F5-R2-04, F5-R4-06, F5-R5-07 |
| F5-A15 | New SEM-33: holder, status and validity are separate states; an entry takes effect on its date, counts for that date and changes only the state it names; a state holds through the day before the next entry that changes the same state; validity comes only from a "for N days" entry, which dated D makes the item valid from D through the Nth day after D, replacing any last valid day set by an entry dated before D even when it shortens it; no other entry moves the last valid day; a lapse changes neither holder nor status. No two entries on one day for one entity and attribute. On open cards a state is determined only by an "as of" statement by <S>, which in both worlds equals SEM-33 replay of the listed entries for that day (F5-R5-06). An item has no status before its first remaining status entry, and status questions ask only days on or after it (SEM-17 log form; F5-R4-04). Action entries name their actor, the holder for renewals and transfers (F5-R5-07); entry dates are never unrecorded (F5-R5-05) | SEM-33, S2; amended by F5-R2-02, F5-R2-18, F5-R3-04, F5-R4-04, F5-R5-05, F5-R5-06, F5-R5-07 |
| F5-A16 | Closed date-phrase lexicon with stated inclusivity ("until", "since", "prior to", "earlier / later than", "during", "within N days of / before" banned). Covered period printed as "This record covers <D_start> to <D_end>, both included" | SEM-11, SEM-27, 3.4; amended by F5-R1-12 |
| F5-A17 | Closed numeric lexicon: "between" includes both ends; "up to", "reaches", "meets", "N or more" include; "above", "below", "exceeds" exclude; "exactly" = equal. Offset step = one unit of the value's last displayed digit | SEM-08 |
| F5-A18 | Tie rule mirrored for lowest / smallest / fewest / least. "Most" only as a count superlative; "most of", "majority", "minority" banned | SEM-13, SEM-09, 3.4 |
| F5-A19 | "Need not X" = X not required, nothing about permission. Deontic closure (rules listed are all the rules) is stated in SEM-24 and applies in both worlds, ahead of the world line (the SEM-24 card line says so); solver B gets it in both, as definitions before completion. Deontic heads never use the SEM-05 / SEM-06 closed-world fallback; which rules forbid or require, and which modal heads each rule form takes, are fixed in SEM-24 (F5-R4-01). Closed modal lexicon; "should", "ought", "has to", "can", "could" banned. A role and action table's cells are unconditional "must" / "may" / "must not" rules about pairs no listed rule mentions, as the SEM-24 card line says (F5-R5-03) | SEM-24, 3.4; amended by F5-R3-01, F5-R4-01, F5-R5-03 |
| F5-A20 | "Any" / "anyone" only in the matrix interrogative clause of a question ("Did any ...?" = at least one) or inside "not any" (= zero), "hardly any", "scarcely any"; never in a positive declarative (so never in a truth frame's embedded clause outside those entries, where "some" / "someone other than" is used), rule or modal text. "Only" only as pre-subject "Only <A>" with one named entity. "Not only ... but also" exempt from the outer-negation ban | SEM-22, SEM-23; amended by F5-R3-02 |
| F5-A21 | C15 restricted to never / no longer / still; "earlier" = a day before the asked day inside the covered period; again, stopped, started, not yet, already, ever banned | SEM-26, 3.4; amended by F5-R1-03 |
| F5-A22 | S3 general statements are strict universals with "Every" / "No" only; bare generics and "typically / usually / generally" banned. The 18-atom limit counts ground atoms after grounding every universal over every entity | S3, 3.4; amended by F5-R1-04 |
| F5-A23 | New SEM-31 for S5 threads: only <S> makes facts true; each retraction or correction names a message by its own sender; retraction cancels the named message; correction replaces its value as if always said, and the corrected message keeps its own date; retractions and corrections are not messages about the fact; of <S>'s remaining messages on a fact the latest counts; another party's own retraction or correction changes only what it stated. Solver B implements exactly this | SEM-31, S5; amended by F5-R1-06, F5-R2-04, F5-R3-05 |
| F5-A24 | S6 has no world line: SEM-29 / SEM-30 / SEM-32 replace it, and S6 is its own G10 world cell. New SEM-32 for 2Wiki (true only if the paragraphs make it true; equal values make "before / first" false; the converter computes gold from the values stated in the kept paragraphs and skips ties, paragraph-vs-triple mismatches, different precision in the paragraphs, more than one stated value, and any answer that differs from the dataset's). GHC P = the file's HD label or CV label | 3.1, SEM-30, SEM-32, S6; amended by F5-R3-03 |
| F5-A25 | MR4 inert sentence restates a fact or concerns an entity outside every restrictor, count and superlative domain (asserted). MR7 direction depends on polarity parity above the operator. MR1 inserts at outermost scope only. MR9 decisive = every minimal support set | 7 |
| F5-A26 | Lines printed by trigger (the 3.1 trigger table over program-written text and questions, plus structural triggers; card lines and quoted source text never trigger), never by decisiveness. Full card = every key the card's sampler and cue families can use; short card = SEM-01 + world line + keys triggered by any row of the base. G10 checks yes rate 50 +/- 3 per SEM key printed | 3.1, 8; amended by F5-R1-07, F5-R2-07, F5-R2-08 |
| F5-A27 | Per-template declared k (checked by the cue parser) under the 4 counting rule; closed L_neg lexicon; j counted separately for question (j_q) and text (j_t). A rows have k = 0 and j_q = 0 | 3.4, 4; amended by F5-R1-08, F5-R1-09 |
| F5-A28 | Double negation = a row with negcount k_all >= 2 (k_all >= k on every row). D 23.8% + V/V' with k >= 2 about 14% + a little more = about 40% (asserted >= 30%); the 2.1 quotas use k_syn | 8; amended by SC8 |
| F5-A29 | "Wording" = instruction wording (spec 2.1 sense), balanced by construction across cards. Per cue template v(P) balanced by construction; checked pooled by cue family at +/- 3 | 8 |
| F5-A30 | Base bin = bin of the base's hardest row (of either base for a contrast pair, which is one selection atom; CF-4), a selection device only; all-easy means every row of the base (of both bases of a pair), V' included; cue mix = sorted tuple of cue families in N, D, V; medium >= 45% added. Quotas, G9 and G10 use row bins (`meta.difficulty_bin` = the row's own bin) | 8; amended by F5-R2-13 |
| F5-A31 | Packs tag every predicate good / bad / neutral. Yes-is-bad = a "Yes" asserts that the bad predicate holds or that the good predicate fails, from the polarity of <P> in the row's LF (section-4 monotonicity table). The 50 +/- 5 check runs on all F5 yes/no rows; no-polarity rows are capped at 5% through the section-8 budget and count as not-bad | 8; amended by F5-R1-15, XF04, SC7 |
| F5-A32 | Open-world S4 dropped (S4 closed 100%). Open S2 decides events both ways only through explicit <S> statements, and states only through "as of" statements. G10 adds A-row yes rate 50 +/- 3 per (base operator type x world) | S2, S4, 8 |
| F5-A33 | S6 attack text goes only into a wrapper field outside the quoted source block (so source byte-equality holds). V' has twin_of = V, twin_kind "attack" | 6, 7, 9 |
| F5-A34 | Gold is 1 (Yes) or 0 (No) in the raw yes/no form (`qtype` "noul"; for any later soft row, 1 iff p' > 0.5, with `meta.teacher` {"yes": p'}). EDOS bases need unanimous annotators (1/3 and 2/3 skipped); in round 1 no F5 row is soft | 1, 2, 2.4, S6; amended by F5-R5-09 |
| F5-A35 | Probe hold-out by stratified seeded draw: at most 1/3 of any family's templates, at least 1 from each of >= 10 families; sha256 logged | 4 |
| F5-A36 | Probe items contain at least one held-out template and no other cue from that template's family; template ids logged per item | S5 probe |
| F5-A37 | S6 exempt from invented entities. S6 card = (F5, S6, Claude-written wrapper pack, Yes / No label schema, rule set = dataset line x definition variant (3.1, SC10), instruction family); format style varies inside the card | 5; amended by SC10 |
| F5-A38 | SEM-18 allowed on S6 only for the answerability predicate; SEM-29 defines "fails to answer", "lacks an answer to", "is unanswerable from". GHC and EDOS use C1 and C2 only; "non-hateful" and "non-sexist" banned and on the 7.2 template check list | SEM-18, SEM-29, 3.4, 4 |

**Spec conflicts (resolved in favour of `C_DATA_SPEC.md` v4)**

| ID | Conflict | Resolution |
|---|---|---|
| K01 | Per-card yes rate 25-75% vs spec 20-80%; balanced base values per card | (Revised by SC3 and CF-4.) Each card draws r_card uniformly from 20-80% as the spec says (antithetic pairs; every card has a partner) and realizes it exactly through its attack share f_card = max(0.15, 1/r_card - 4, (4 r_card - 3)/(1 - r_card)) and its A-row v(P) and V gold rate a_card = (r_card (4 + f_card) - 1)/(2 + f_card); N and D are fixed by spec 2.2 (section 8). Nothing is clipped, and attack rows stay about 5% (E[f_card] = 0.204). "Balanced base values per card" dropped; question-only chance rests on per-template and per-wording balance by construction and card-grouped G6 folds (sections 8, 9). Section 10 item 8: no amendment |
| K02 | Whole-base selection vs the 2.1 row rule | Spec rule applied with the base as the atom (a contrast pair is one atom, CF-4; 2.1 relation units forbid splitting): keep every base with a medium or hard row (= all medium and hard rows), 30% of all-easy bases, downsample inside wording x bin x gold-pattern cells; row-level quotas and G9 chi-square checked after (section 8) |
| K03 | QuALITY and Qasper listed as F5 bases | Not used: spec 2.1/G15 (3-row unit needs rows < 2,000 tokens), 3.1 (no LLM-written text) and the 0-row label-check form block them. The < 1,900-token row cap follows from 2.1/G15, not a deviation (section 1, S6). Spec 2.2 lists the sources F5 bases may come from and sets no share for any, so using five of them breaks no rule (CF-4; section 10 item 9: no amendment) |
| K04 | Unit 2 has 1 row in 2.2/6 vs V + V' | Kept 2 rows on the bases that carry a V' (a per-card share f_card, about 20% of training bases overall; section 8): the 2.1 attack quota (about 5%, `inv`, same `call_id`) and the 2.1 unit rule (<= 3 rows) are binding; 2.2/6 text amendment requested (section 10 item 2) |
| K05 | Inverted cards (choice form) vs a yes/no-only family | 10-15% of cards (spec quota) as the per-case yes/no form of "which of these cases meets rule X?" on S1 and S4; the question names the outcome ("Is <case> among the cases that are <outcome>?"), never "meets <rule>" (section 8; F5-R3-09) |
| K06 | 20-25% twin quota vs 100% in F5 | (Revised by CF-4.) Counted by XF03 like every family: the quadruple's complement / equiv links count only toward the negation quotas and V' toward the attack quota; F5's contrast sets are S1-S4 contrast pairs (one input change flips every A, N, D and V gold), about 22.5% of rows, asserted 20-25% on the final set (sections 1, 8). Section 10 item 10: no amendment |
| K07 | >= 3 definition styles, short/no cards vs fixed SEM sentences | Meanings fixed, renderings vary: >= 3 renderings per key, one per definition style; short cards about 15% of rows; no-card rows 0. G11's 2% rule applies to question and text templates (3.3) |
| K08 | Sealed hit drops the C template vs immutable SEM lines | A hit drops that rendering; a new rendering with the same meaning replaces it and is re-checked; affected rows regenerated (3.3) |
| K09 | G14: exact card text before the sealed sha256 | Section 3 now states normative meanings only; renderings are written after G14 and pass 7.2 and the spec-9 comparison (3.3) |
| K10 | Zero-wrong G5 bar vs dataset-level rule for real text | 600 program rows at zero wrong; S6 judged by the dataset-level bars: SQuAD 2.0 > 5% wrong or ambiguous (spec 3.2 #1), others > 8% clearly wrong (spec G5); census when F5 holds fewer rows than the read size; a drop from F5's read or the public read drops the dataset from both blocks (SC2); zero tolerance for transform, parse or conversion errors (section 9) |
| K11 | GHC p from the annotator-level file vs "`ghc_train.tsv` only" | `ghc_train.tsv` only; GHC is hard-labelled (HD or CV); the annotator file is never opened. Soft GHC needs an amendment (section 10) |
| K12 | S6 byte identity vs trimming, MR6 and MR10 | Byte identity per kept paragraph, whole distractor paragraphs only removed; decoys banned on S6 (MR6 = S1-S5); attacks only outside the quoted block (6, 7) |
| K13 | Licence register lacks F5 S6 rows; guideline text licence | S6 rows carry the dataset licence like 2.3 codebook rows; register row requested (section 10). SEM-30 definitions are Claude-written summaries, no guideline text copied |
| K14 | Spec 3.1 passage dedupe missing | Added: S6 Wikipedia passages deduped against `qnli`, `gd_answer_equiv`, `gd_hotpotqa_yesno`, `gd_feverous`, `gd_totto_claims`, `gd_wtq`, `boolq`; a hit drops the base (S6) |
| K15 | 500-per-class cap and "class" for F5 rows | Class = the record's original human class; every F5 S6 row counts toward it and toward the 3,000 cap through the shared ledger; F5 takes only the room left after public and codebook allocations (S6) |
| K16 | Double-negation share 23.8% < 25% | Double negation = negcount k_all >= 2 (XF02, SC8); V/V' with k >= 2 bring it to about 40% (section 8) |
| K17 | Sidecar and twin_kind values vs 2.4 / 2.1 | twin_kind uses the spec vocabulary ("negation", "attack"); polarity fields in a sidecar in `data/c_parts/`, named on the QC allow-list; row format unchanged (section 9) |
| K18 | Medium >= 45% missing | Added to the selection rule (section 8) |
| K19 | Fixed r2 size vs probe-set share and per-sampler cap | (Revised by SC1.) r2 figures are cumulative placeholders (round 2 is a superset: spec 0, 2.2, recipe 7.1); the multiplier applies to all round-2 own rows; F5 stays <= 12% of own rows (spec 2.1), so at most 10,860 rows and S1 at most 2,389 < 2,500 at its target share: no S7 is needed; the cap is asserted on the final selected set, and drift past it is handled by the section-8 remedy (F5-R2-14) (sections 1, 5, 8, 10) |
| K20 | Spec 2.2 names F1-F4 and F9 structures as F5 bases; the F2 structure was absent (SC3) | F2 is now covered inside S1 (amount sub-shape: caps, floors, tier lookup, stated day offsets; comparison only, no rounding) and S2 (stated-day-count offsets), so no deviation and no amendment item (sections 1, 5, SEM-12) |
| K21 | Spec G0 asks for a 1-page spec per generator; this file is long (SC4) | Section 0 is the 1-page spec, with the G0 semantics table (world, unless, only if, at least, or, date ranges, rounding, ties, units, exception precedence); sections 1-10 are its normative annex. Section 0 adds no rule of its own; if a summary line ever reads differently from the annex row it cites, that annex row governs |
| K22 | Spec 2.2 F5: "Labels: a polarity-logic program over the base label" and unit 2 "labelled by polarity logic"; F5 labels every row by direct evaluation (SC5) | F5's label program composes the question's operator chain over the base proposition and evaluates it on the base: on truth-functional chains (C1, C2, C3, C5, C6) this is gold = v(P) XOR (k mod 2), asserted on every such row; structural operators (bounds, dates, quantifiers, modals, aspect, "barely", decoys, value sets), which 2.2's own skill list requires and which a program over the bare label cannot evaluate, are evaluated on M (S1-S5); S6 uses a truth table over the human base label. Solver B re-derives the LF (and so the polarity) from the parsed question, as spec 2.2 asks. A reading of 2.2, not a deviation (CF-4; section 10 item 11: no amendment) |

---

## Resolved ambiguities (re-review round 1: F5-R1-01 to F5-R1-19, and spec conflicts SC1-SC4)

Each row states the one semantics now used and, where it reaches a reader, the card text that carries it.

| ID | Resolution (one semantics; card text where it applies) | Where |
|---|---|---|
| F5-R1-01 | Card (SEM-20): a question about what <X> stated asks about <X>'s latest remaining statement about <P> dated on or before the asked day; <X>'s own VOID or retraction removes a statement and its own CORRECTION or correction replaces what it says, whatever their date; nobody else can change what <X> stated; "latest" = latest date. No stance question about a <P> on which the asked party has a VOID, CORRECTION, retraction or correction (F5-R2-04). Card (SEM-02): the closed record lists every statement each party made; an unlisted statement was not made. Stance questions only on closed cards (C7 text-side only on open cards), so "did <X> deny" can be No. Asserted: no party makes two statements about one fact on one date; the asked party's remaining statements about <P> share one polarity, so "latest" and "any" agree; no statement of <X> about <P> gives No to both "confirm" and "deny"; a statement about <P> states <P> or that <P> is false, and every statement the asked party made about the entity and attribute of <P> literally states <P> or that <P> is false, or it made none (F5-R3-11, F5-R4-03); a stance question never names <S>, and its <P> is a timeless fact or an event, never a SEM-33 state (F5-R4-03) | SEM-02, SEM-03, SEM-20, C7, S2, S5, MR9; amended by F5-R3-11, F5-R4-03 |
| F5-R1-02 | Whole-period reading. Card (SEM-19): "failed / neglected / omitted to", "did not manage to", "refused / declined to", "was prevented from" <X> without "by <D>" means <X> did not happen on any day of the covered period, wherever it appears and whatever the entry's date; "failed to <X> by <D>" means no <X> from the period start through <D>. Asserted: a failure or refusal cue without "by <D>" in the text, dated entry or not, means no <X> entry for that entity anywhere in the period (before or after the cue); with "by <D>", none on or before <D> | SEM-19, S2; amended by F5-R2-06 |
| F5-R1-03 | Card (SEM-26): in a question, "never" = on no day from the start of the covered period through the asked day; in the record, "never" = on no day of the covered period, and dated-entry "no longer" / "still" refer to the entry's date. Card (SEM-27): "as of <D>" in a question makes <D> the asked day; no stated time = end of <D_end>. Lint: never / no longer / still combine only with "as of <D>"; a C3 question states no time other than its own "by <D>"; no "before / after / between / from ... to / through / in <month/year> / on <D>" with either | SEM-19, SEM-26, SEM-27, C3, C15; amended by F5-R5-04 (text-side "never" / "no longer" / "still" entries are statements that set no state) |
| F5-R1-04 | Domain closure. Card (SEM-02 and SEM-03): the record names every <entity type> in the case; on open cards only facts about them may be missing. Card (SEM-22): quantifiers range over the members of the named group. Both solvers ground over exactly the named entities, and solver B's determinacy check uses that domain (no fresh individuals) | SEM-02, SEM-03, SEM-22 |
| F5-R1-05 | Every "only", "other than", "all except", superlative and count question names its group ("Among the <group>, ..."); card (SEM-13, SEM-23): the comparison set is exactly the named group. <A> is a member of it (asserted). On S4 the named group is the filtered subset. Superlatives only in the predicative form ("<E> has the highest <X>", "the only one with the highest <X>"; F5-R3-10) | SEM-13, SEM-22, SEM-23, S4; amended by F5-R3-10 |
| F5-R1-06 | Card (SEM-31): "latest" = latest date; a corrected message keeps its own date, and retractions and corrections are not messages about the fact (F5-R3-05). Asserted for S5 (and S2 statements): no two messages by one party about one fact share a date; no retraction or correction by a party shares a date with a message by that party about that fact; a retraction or correction is dated after the message it names. Listed order is never used (MR5 holds) | SEM-31, S5, MR5; amended by F5-R3-05 |
| F5-R1-07 | Keys print by trigger: a trigger-table phrase use in program-written text or a question (card lines and quoted source text never trigger), or a structural trigger. SEM-16, SEM-20, SEM-27, SEM-33 on every S2 card; SEM-20, SEM-27, SEM-31 on every S5 card; SEM-20 on any card with an attributed statement; SEM-04 on any blank, "not recorded" or null entry; SEM-11 on any date; SEM-12 on any value number (not digits in dates, IDs or names); SEM-14 on any quantity with a unit; SEM-17 per value-set attribute; SEM-27 also on any C3, C4 or SEM-26 phrase and any dated entry (not on a C5 phrase alone). "Used" = "triggered". Card form (full or short) is chosen once per base, and all rows of a base carry the identical card; a short card = SEM-01 + world line + every key triggered by any row of the base | 3.1, 6 (step 3), 8; amended by F5-R2-05, F5-R2-07, F5-R2-08 |
| F5-R1-08 | A-row base operators hold no counted operator and no L_neg entry (asserted). "None" removed from the S4 base list; it is reached only as the N row of a "some" base, so A has k = 0 and j_q = 0, N k = 1 | 4 (A rows), S4 |
| F5-R1-09 | j = number of matched L_neg entries, longest match first, left to right, no overlap, 1 per match; multiword entries ("no longer", "need not", "not only", "neither ... nor", "no fewer than", "it is not the case that") count once; matching by lemma (all inflections); "fewer" / "fewest" are not "few"; "false" (incl. "it is false that" and data values) and "free of" added to L_neg, so every C2 and C5 N row has j_q >= 1 | 3.4 |
| F5-R1-10 | S6 bases whose quoted source question (or program-converted claim) holds any L_neg entry are skipped, so every A row has j_q = 0 | 3.4, S6 |
| F5-R1-11 | Bans and the operator lint apply only to program- or template-written text (cards, wrapper packs, SEM-30 definitions, rendered M, questions, 2Wiki declaratives). Quoted source text is exempt (from SEM triggers too) and never edited, still counts in j_t / j_q, and still passes 7.2 decontamination | 3.4; amended by F5-R2-07 |
| F5-R1-12 | Allowed operator words = every phrase quoted in the card column of SEM-01 to SEM-33 (incl. if ... then, unless, only if, except when, CORRECTION / VOID, value-set wording, affixed words, SEM-29 phrases, SEM-32 before / after / older / younger / first, SEM-33 "for <N> days"), the L_neg entries and the truth frames, each only on its allowed side and samplers. "Earlier" removed from SEM-32; "earlier", "later", "earlier than", "later than" banned except inside "no earlier than" / "no later than" (SEM-11) | 3.4, SEM-32 |
| F5-R1-13 | Only L_core negation must sit inside an embedded declarative after a truth frame, per token (also inside a multiword entry; F5-R2-09); the matrix clause includes relative clauses (F5-R2-17); L_neg cues with no L_core token may sit in the matrix clause. Truth frames: a closed list of >= 8 (written after G14), no L_neg entry in a frame, used on A rows as on N, D and V rows (framed share equal +/- 3 pp per row type), yes rate 50 +/- 3 per frame, each passing 7.2 method 8; G11's 2% applies to frame x cue template | SEM-01 |
| F5-R1-14 | V forms listed per sampler and dataset. 2Wiki, GHC, EDOS: V = a C1/C2 chain with the negation at a different syntactic position than N and D (scope-position shift), k = 1-3, never N's or D's template sequence; 4.2 rows per base kept (spec 2.2). k = 0 V rows only as antonym / "one of", "barely", decoy, "only", "still", or the exact bound complement of the base (single-valued numbers and dates and counts only; "at most <q - 1>" on integer counts); other plain-comparison k = 0 V rows are not generated. V k-mix pooled over samplers | 4 (V rows), 8; amended by F5-R2-19 |
| F5-R1-15 | Every template declares per-slot monotonicity (up / down / non-monotone / opaque, or atom; classes fixed in section 4 with a row for every question-side operator (F5-R2-11), checked by property test). k is a cue count, not polarity. MR7 runs only on all-up/down paths, direction from the parity of down operators on the path. Yes-is-bad = (<P> bad and even polarity) or (<P> good and odd polarity); rows with no polarity for <P> count as not-bad, capped at 5% of all F5 yes/no rows (XF04) through the section-8 no-polarity budget (SC7) | 4, 7 (MR7), 8; amended by SC7 |
| F5-R1-16 | Base depth per sampler: S1 rule applications on the decisive derivation; S2 1 + CORRECTION / VOID links followed; S3 universal applications in the proof; S4 filter conditions; S6 SQuAD / GHC / EDOS 1, 2Wiki 2, MuSiQue hop count; S5 1 + retraction / correction links. meta.depth = base depth; meta.deep = (k = 3 or base depth >= 3); depth >= 3 bases <= 4% of bases. Cap lever: drop depth >= 3 bases, then lower max base depth to 1 on S1-S4 only (S6 depths fixed by dataset), then drop k = 3 V rows | 5, 8, 9; amended by F5-R2-16 |
| F5-R1-17 | When a row-level difficulty quota fails, the spec's downsampling step drops whole kept bases with the most easy rows first inside each cell (the 30% all-easy keep rate is unchanged); if medium < 45% or hard > 30% remains, or a cell falls below its floor, generate more bases for that cell and select again | 8 |
| F5-R1-18 | Cumulative reading: the probe multiplier applies to all round-2 own rows. F5 r2 total = 4,824 (x0.67), 7,200 (x1), 10,800 (x1.5) before clipping to [0.5/13, 12%] of 90,500 and renormalizing, F5 <= 12% after | 1 |
| F5-R1-19 | k (`k_neg`) only for the question-side negation-cue count; n_vals for value-set size (SEM-17); <q> for quantifier and graded-cue numbers (SEM-25, S1, S4, MR7); t_txt = text-side negation-cue instances (templates declaring an L_neg entry, decisive or not); r_card / a_card for per-card rates | header, SEM-17, SEM-25, 4, 5, 7, 8, 9 |

**Spec conflicts (round 1; resolved in favour of `C_DATA_SPEC.md` v4)**

| ID | Conflict | Resolution |
|---|---|---|
| SC1 | Per-sampler cap computed on r1 + r2 = 10,800 rows, but spec 0 / 2.2 / recipe 7.1 make round 2 a superset (r2 7,200 includes r1) | All r2 figures are cumulative. At x1: S1 1,584, S2-S4 1,440, S6 1,296; at the 12% maximum (10,860): S1 2,389, S2-S4 2,172, S6 1,955 at target shares, so no S7 is needed; the cap is asserted on the final selected set with the section-8 drift remedy (F5-R2-14); the "r2 <= 7,750" cap and the S7 condition are removed (sections 1, 5, 10; K19) |
| SC2 | G5 on S6: "> 5% clearly wrong" vs spec 3.2 #1 "> 5% wrong or ambiguous"; relation to the public read; too few F5 SQuAD rows for a 300-row read | SQuAD 2.0 uses spec 3.2 #1 (> 5% wrong or ambiguous); others > 8% clearly wrong; census when F5 has fewer rows than the read size; a drop from either F5's or the public block's read drops the dataset from both (orchestrator item 7) (section 9; K10) |
| SC3 | Deviations from spec 2.1 / 2.2 without section-10 items: QuALITY / Qasper (K03), missing F2 structures, per-card 34-66% (K01), 100% twin coverage (K06) | (Final form by CF-4.) Section-10 items 8-10 log how F5 meets the spec as written: per-card rate drawn uniformly from 20-80% and realized exactly (K01); QuALITY / Qasper unused under a source list with no shares (K03); contrast pairs give 20-25% of rows in XF03 contrast sets (K06). F2 structures added (S1 amount sub-shape, S2 day offsets; K20), so no deviation |
| SC4 | Spec G0 asks for a 1-page spec per generator | Section 0 is the 1-page spec with the G0 semantics table; sections 1-10 are its annex (K21) |

---

## XF. Cross-family alignment (orchestrator fixes, 3 Oct 2026)

The cross-family consistency review (18 issues over F1-F13 and COMMIT) set one rule for every family where families
differed. Every XF rule below is now stated directly in sections 0-10 and in the resolved-ambiguity tables (the F5
resolver round-2 pass edited the earlier text), so no earlier line states a different rule; if one ever does, this
section governs. No label of an existing
row changes, because no C row exists yet (G14). Code named here (`c_src/common/...`) is orchestrator-owned and is
written only after the sealed sha256 commit.

| ID | Rule (same text in every family that carries it) | Effect in F5 |
|---|---|---|
| XF01 | **Abstain gold = 1/k (display-then-gold).** Draw k (abstain slots included), then the display, then the gold slot uniformly over the displayed slots; reject structures whose gold class does not match. An abstain option (NEI, CBD, None, 'none of these', 'no record', tie options) is shown only when k >= 3 and only on rows where it can be gold; no always-wrong abstain display. Each abstain option is gold with probability exactly 1/k; G10 checks 1/k +/- 2 pp per k bucket and per abstain option, so G6(b) and G7 (p0 = 1/k) sit at chance. The ~10% NEI aggregate is only a mixer count; no family tunes toward it. | No change: F5 rows are yes/no only and never show an abstain option. |
| XF02 | **One negation counter.** Every family uses the orchestrator-owned `c_src/common/negcount.py` (not written by any family builder). k_syn = number of F5 L_core tokens in the question (not, n't, no, none, nobody, nothing, nowhere, never, neither, nor). k_all = F5 L_neg surface count (longest match; comparator phrases such as 'no fewer than' and implicit cues included; C_DATA_SPEC 2.2 F5). 2.1 quotas use k_syn: k_syn >= 1 on >= 10% of yes/no rows; k_syn >= 2 with an affirmative twin on >= 2%. G10 yes-rate negation-count cells use k_all. Whether an L_core token inside a matched multiword comparator entry (the 'no' of 'no fewer than') counts toward k_syn is fixed once inside negcount, never per family. A family-local cue list may stay for polarity logic only. | The shared negcount implements F5's own 3.4 lexicons: k_syn = L_core tokens in the question, k_all = the L_neg surface count (F5's j_q). Every F5 count check uses negcount (SC8): the 2.1 quotas use k_syn (k_syn >= 1 on >= 10%; k_syn >= 2 with an affirmative twin on >= 2%, met by C1 / C2 two-L_core D rows on >= 15% of bases); spec 2.2's double-negation floor (>= 25%) uses k_all >= 2; spec 2.2's P(yes \| number of negation cues) and section 8's G10 aggregate cell (wording x row bin x negation count) use k_all. F5's family-local operator count k stays for polarity logic (N / D construction, XOR identity, V k-mix) and as an extra P(yes \| k) check that never replaces a negcount count; every other family counts the same way. |
| XF03 | **Twin-set count.** A row counts toward 2.1's 20-25% only if it sits in a contrast set: a base plus label-flip twins with their own `call_id`, built by a change to the input text or structure (fact, boundary, premise, clause, definition or world flip, or deletion to NEI). `complement`/`equiv` negation units, `inv` attack units and `equiv` inert units count only toward the negation, attack (~5%) and inert (<= 5%) quotas. | F5 is counted like every family (CF-4): its contrast sets are S1-S4 contrast pairs, where one input change flips the gold of every A, N, D and V row, about 22.5% of rows, asserted 20-25% on the final set (sections 1, 8); the spec-2.2 quadruple's complement / equiv links count only toward the negation quotas and V' toward the attack quota. No exemption and no amendment. |
| XF04 | **'Yes = bad outcome' denominator.** All yes/no rows of the family. Rows with no polarity are <= 5% of the family's yes/no rows and count as not-bad. No family-chosen subset denominator. | Section 8 'Yes = bad' now uses all F5 yes/no rows. S6 predicates are tagged (unanswerable, hateful, sexist = adverse); no-polarity rows (neutral predicates such as 2Wiki comparisons, and <P> under a non-monotone or opaque operator) are capped at 5% and count as not-bad. F5 meets the cap by design through the section-8 no-polarity budget (SC7: 2Wiki <= 1.5% of bases; non-monotone S4 base operators <= 1.5%; no training stance bases; no-polarity V / V' rows <= 1.5% of rows; S1-S4 base predicates always tagged good or bad), so it does not trigger the XF04 amendment. One-page balance line and F5-A31 updated. |
| XF06 | **Missing-value markers.** One cross-family marker table, orchestrator-owned in `c_src/common/`, enforced by every parser. Unknown: 'not recorded', 'unknown', JSON/YAML null. Zero or absent: '0', 'none', 'no', false. Banned in every family: '-', 'n/a', 'N/A', 'TBD', '?'. Blank cells stay card-defined (a definition-following contrast) and appear only on rows whose card states the blank's meaning. Unknowns on closed or local cards use word markers or null, never blanks, so a blank on a complete record means none/no wherever it appears. | SEM-04 no longer lists '-' or 'n/a' (trigger line and table). Unknowns are 'not recorded' or null; on closed cards an unrecorded number, date or category is never rendered blank, so a blank on a complete record is only a yes/no 'no'. No label changes (such cells were never decisive). |
| XF07 | **EDOS / real-text codebook targets (orchestrator ruling X3, recommended).** 2.3 codebook rows carry hard labels in F10 and F11 (no soft `meta.teacher` on S7 EDOS rows). Eligibility for both: exactly 3 annotator rows, and >= 2 of the 3 annotators' own vectors map to the gold code. F5 keeps its stricter unanimity rule (it negates bases). To be recorded in C_DATA_SPEC 2.3. | No change (SC9): F5's stricter unanimity rule is its EDOS rule: EDOS bases are unanimous posts only (p = 0 or 1; F5 negates bases). GHC is hard-labelled by the annotators' majority from `ghc_train.tsv` (HD or CV; spec 3.2 #16), because unanimity needs the annotator-level file, which F5 never opens (K11, section 10 items 3 and 16). F10 and F11 use the shared 3-annotator, >= 2 of 3 filter. |
| XF09 | **One pack per card.** Within a family, no two cards share a domain pack (round 1 >= 80 packs for >= 80 cards, round 2 >= 150; F12 and F13 follow their own card counts). Different families may use the same pack. | Packs >= 80 / >= 150, one per card (was >= 30 / 40 with sharing); the shared-pack clause of the per-card yes-rate draw is deleted, so antithetic pairs are drawn over the card list, inside (sampler, world cell, inverted or not) cells (section 8, F5-R2-15). |
| XF10 | **Shared negation-frame lint (from F5).** No question wraps a negated or negatable proposition in an outer judgement or acceptance predicate ('wrong', 'right', 'reject', 'accept', 'should/would ... be'). Negation is written as truth-frame syntactic negation ('Is it true that ... does not ...?'). **Scope (cross-family fix, 3 Oct):** the shared lint bans only these outer judgement or acceptance predicates; the truth frames 'Is it true that', 'Is it not the case that' and 'Is it false that' over an affirmative claim are allowed, and a family may ban more on its own, as a family-local rule that it does not cite as XF10. | F5's banned-frame class (3.4: 'should / would the statement ... be rejected / accepted', 'reject / accept the statement') is now the shared negation-frame lint for every family. F5's own SEM-01 rule (no L_core word in the matrix interrogative clause, so 'Is it not the case that ...?' is never a matrix frame in F5 and C2 'it is not the case that' sits inside a truth frame, while 'Is it false that ...?' may be one) is family-local and is not cited as XF10 (CF-5). |
| XF11 | **F5 interface and cross-family G12.** F5 stays independent (it re-implements the shallow structures it needs and imports no other family's generator). F1 reserves no seed range for F5; F9 has no export for F5 (X4 = no export). The orchestrator adds a cross-family G12 pass: exact text hash plus MinHash over F5 rows against F1, F2, F3, F4 and F9 rows, and over F13 rows against F1, F3, F6 and F9 rows; each near-duplicate pair is dropped from F5 or F13. | Section 9 adds the cross-family G12 pass: F5 rows against F1, F2, F3, F4 and F9 rows (exact hash plus MinHash); each near-duplicate is dropped from F5. F5's independence (no imported generator) is kept. |
| XF16 | **F14 exclusion lint.** 'No row poses <F14 task>.' The orchestrator names F14's skill and structure type before step 5 (generator code) and fills in the lint then. Provisional instance (constraint scheduling): no row asks for a feasible slot or assignment for several items under pairwise constraints. The QC agent's F14 builder checks, by structure type, that no C training row matches F14's structure, and logs the result. | Lint added (bank-build lint and QC check, section 9): no F5 row poses <F14 task>. |
| XF17 | **G14 and operator lexicons (orchestrator ruling, recommended default).** Closed operator lexicons (meaning-bearing operator phrases only, each mapped to a SEM row, with no domain words, entity names or templates) are G0 semantics and allowed before the sealed freeze. They pass the 7.2 Claude-seed decontamination and the counts-only sealed template compare before any use. If the orchestrator rules the other way, closed lexicons move to step 4 and only the SEM meaning rows stay in G0. | Confirms F5's reading: the 3.4 closed lexicons (L_core, L_neg, operator classes) are G0 semantics, allowed before the freeze. |

---

## Resolved ambiguities (re-review round 2: F5-R2-01 to F5-R2-21, and spec conflicts SC5-SC6)

Written after the XF alignment; each row states the one semantics now used and, where it reaches a reader, the card
text that carries it. Earlier rows that these change were edited in place (marked "amended by F5-R2-..").

| ID | Resolution (one semantics; card text where it applies) | Where |
|---|---|---|
| F5-R2-01 | Card (SEM-04): an entry marked "not recorded" (or null) has some value that the record does not give, on a complete record too; nothing in the record makes a statement about that value true or false; on an open card a blank means the same; on a complete record a blank yes/no entry means no. Card (SEM-02) names this as the one exception to "unstated = false". Both solvers encode an unrecorded value as an unconstrained variable over its domain (completion and negation as failure never apply to it). Asserted: same label for every domain value, and, for numbers, dates and categories without a value set, the same label when every positive statement about the value is taken as false (F5-R5-01: a statement negating it then holds); otherwise the base is rejected. The value set tested includes every other member's value of the same field (F5-R3-06), and for a category without a value set also every category value the case names and one fresh value, and for a yes/no entry both yes and no (F5-R4-05); closed cards never omit a key or attribute (F5-R3-07) | SEM-02, SEM-04, S1, S4; amended by F5-R3-06, F5-R3-07, F5-R4-05 |
| F5-R2-02 | Card (SEM-33): "<renewed / valid> for <N> days" dated <D> sets the last valid day to the <N>th day after <D>, replacing any last valid day set by an entry dated before <D>, even one further on. So the newest-dated renewal governs, also when it shortens validity. Only renewals move the last valid day; holder and status are separate states (F5-R3-04) | SEM-33; amended by F5-R3-04 |
| F5-R2-03 | Card (SEM-11): a date range in a question about an event asks whether at least one such event falls on some day of the range (one is enough), a "not" over it means no such event does, and a range over a single date asks whether that date falls in it (wording as amended by F5-R4-02). Lint: range words take only events and single-date attributes; a state question (a stance under SEM-20 included) states no time other than "as of <D>" | SEM-11, C10, S2; amended by F5-R4-02, F5-R5-02 |
| F5-R2-04 | Card (SEM-16): each CORRECTION or VOID names one entry by its own author; only <S>'s change facts; any party's own changes only what it stated. Card (SEM-20): <X>'s own VOID or retraction removes a statement, its own CORRECTION or correction replaces what the statement says, whatever their date; nobody else can change what <X> stated. Card (SEM-31): each retraction or correction names a message by its own sender. Generator and solver B: no stance question about a <P> on which the asked party has a VOID, CORRECTION, retraction or correction of any date (S2 and S5) | SEM-16, SEM-20, SEM-31, S2, S5 |
| F5-R2-05 | Privatives (C5: "lacks", "is without", "is free of") are timeless: allowed only on cards with no dated entries (S1, S3, S4; on S6 SQuAD 2.0 and MuSiQue as SEM-29 phrases), never in S2 or S5 text or questions (lint). Card meaning unchanged ("does not have <Z>"). A C5 phrase alone does not print SEM-27 | SEM-19, 3.1, C5, S2, S5 |
| F5-R2-06 | The whole-period assertion applies to every failure or refusal cue without "by <D>", dated entries included; both solvers apply it to every such cue. Section-0 and S2 wording changed from "undated" to "without 'by <D>'" | SEM-19, S2, section 0 |
| F5-R2-07 | Triggers are computed only on program-written text and questions (rendered M, questions, 2Wiki declaratives). Card lines and quoted source text never trigger; S6 wrapper text holds no trigger phrase, number or date (asserted). On SQuAD 2.0 and MuSiQue the SEM-29 phrases and the C3 / C5 / C6 cues map to SEM-29 only, so every S6 card prints exactly SEM-01 plus SEM-29, SEM-30 or SEM-32 | 3.1, 3.4, SEM-18, 6 |
| F5-R2-08 | A trigger table maps each phrase use, classed by parsed role, to one key: status values from the card's declared status list -> SEM-21; stance verbs with a named party and a proposition -> SEM-20; "unless" in a rule with no "if" -> SEM-05, attached to an "if ... then" rule -> SEM-15; "except when" attached to any rule -> SEM-15; "only if" rules carry no exception (F5-R4-07); SEM-32 words on 2Wiki -> SEM-32; C3 "by <D>" -> SEM-19. Card lines never trigger, so no fixed point is needed. Dates fire SEM-11; SEM-12 fires on value numbers only (digits in dates, IDs and names are not numbers). G3 uses the same table | 3.1, SEM-21, 6; amended by F5-R4-07 |
| F5-R2-09 | The L_core rule is per token: an L_core token inside a multiword L_neg entry ("no fewer than", "no longer", "need not", "must not", "not every", "none of", "neither ... nor", "not only ... but also", ...) also sits only inside an embedded declarative after a truth frame. Whether such tokens count toward k_syn is fixed once in the shared negcount (XF02) | SEM-01, 3.4 |
| F5-R2-10 | "No earlier than" and "no later than" are L_neg multiword entries (j = 1) and negated comparison words (k = 1), like "not before" / "not after"; as questions they sit inside a truth frame (F5-R2-09) | 3.4, 4 |
| F5-R2-11 | Every question-side operator of the 3.4 allowed list has a class row (up / down / non-monotone / opaque / atom) per slot: the negated comparison words, date words over events (up, existential), "at least half" / "more than half" (scope up, restrictor non-monotone), positive modals (up), C17 "one of" (opaque), numeric "between" (non-monotone) apart from date "between" over an event (up), two-entity comparisons (non-monotone), single-valued comparisons (atoms). Text-side-only phrases fail the lint in a question; an operator without a class fails the bank lint. MR7 and yes-is-bad cite the table, not a short list | 4, 7, 8 |
| F5-R2-12 | Quota restated on its feasible denominator: C17 V rows use value sets with n_vals >= 3, and on at least half of the C17 rows whose gold is No (about 25% of C17 rows) the true value is a third listed value (neither the base value nor a value the question names). A-row value tests and N / D rows do not count | 8, C17 |
| F5-R2-13 | `meta.difficulty_bin` = the row's own crowd bin; the difficulty quotas, G9's label x bin chi-square and G10's family x wording x bin x negation-count cells use row bins. Base bin (sidecar `base_bin`) is a selection device only. A failing G10 cell (wording x row bin x k_all x gold) is filled by generating bases whose rows land in it and selecting again | 8, 9 |
| F5-R2-14 | Sampler, world, short-card, inverted-card, card-count, per-card-rate and depth targets are checked on the final selected set with stated tolerances (sampler +/- 2 pp, world +/- 3 pp, short cards 15 +/- 3%, per-card rate +/- 5 pp or one base). The 2,500-row cap is asserted on the final cumulative selected set; a sampler above it (only S1 at the 12% maximum can get there) drops whole bases, most easy rows first, and the room goes to S2-S4 | 1, 5, 8, 10 |
| F5-R2-15 | XF09 (one pack per card) settles pack sharing. Antithetic pairs are formed inside (sampler, world cell, inverted or not) cells; the training card count is even and the leftover cards of odd cells are paired with each other, so every card has a partner and every r_card is uniform on 20-80% (CF-4). G7 row cap: a card keeps at most the rows at which a feature on every row at its realized rate passes G7 (about 65 rows at 20% / 80%, about 90 at 24% / 76%, with 50K features); no amendment needed | 8; amended by CF-4 |
| F5-R2-16 | The depth-cap lever's step 2 (maximum base depth 2 -> 1) applies to S1-S4 only; S6 depths are fixed by dataset (2Wiki 2, MuSiQue 2-hop stay), and step 1 already drops 3- and 4-hop MuSiQue | 8, F5-R1-16 |
| F5-R2-17 | A negated inverted row puts its negation inside a truth frame with C1 or C2 ("Is it true that <case> is not among the cases that are <outcome>?"); the matrix clause includes relative clauses, so "Is <case> among the cases that are not <outcome>?" fails the lint | 8, SEM-01; amended by F5-R3-09 |
| F5-R2-18 | SEM-33's meaning is worded without "until", "later" and "again": a state "holds from that entry's date through the day before the next entry that changes the same state"; validity runs "through its last valid day", and "from the day after its last valid day the item has lapsed" (wording as amended by F5-R3-04). The 3.4 bans apply to card text with no exemption | SEM-33, 3.4; amended by F5-R3-04 |
| F5-R2-19 | The k = 0 bound-complement V form is used only on single-valued numbers and dates and on counts, never on event-in-range claims; "at most <q - 1>" (integer counts) is added to the section-4 list, matching S4. S2 date-bound V rows on events use a negated date word (k = 1) | 4, S2, S4 |
| F5-R2-20 | j_q, j_t and t_txt are checked in buckets 0, 1, 2, 3, 4+; a bucket cell needs >= 200 rows, else it is pooled with the adjacent bucket toward 0 (logged). Verbatim-overlap denominator = rows with j_q >= 1 | 8 |
| F5-R2-21 | S5 has no V': 100 bases x 4 rows (A, N, D, V) = 400 items. MR10 is tested on the training samplers (S1-S4, S6) | 0, 1, S5, 7 |

**Spec conflicts (round 2; resolved in favour of `C_DATA_SPEC.md` v4)**

| ID | Conflict | Resolution |
|---|---|---|
| SC5 | Spec 2.2 labels F5 by "a polarity-logic program over the base label"; F5 labels every row by direct evaluation, and structural V rows have no polarity-logic label; the deviation had no K row or section-10 item | K22 added; section 10 item 11 logs the reading (CF-4): F5's label program is the polarity logic of the question's operator chain evaluated on the base, with the XOR identity asserted on truth-functional chains; no amendment |
| SC6 | Spec 2.1 requires two cards to differ in the domain pack; F5's old per-card rule let cards share a pack | Settled by XF09: no two F5 cards share a pack (>= 80 / 150 packs, one per card), which meets the pack half of spec 2.1; the shared-pack clause is gone from section 8. The rule-set half is SC10 (3.1 card rule set) |

---

## Resolved ambiguities (re-review round 3: F5-R3-01 to F5-R3-12, and spec conflicts SC7-SC8)

Each row states the one semantics now used and, where it reaches a reader, the card text that carries it. Earlier rows
that these change were edited in place (marked "amended by F5-R3-.." or "amended by SC7 / SC8").

| ID | Resolution (one semantics; card text where it applies) | Where |
|---|---|---|
| F5-R3-01 | Card (SEM-24): "an action that no listed rule forbids for the case is permitted, and an action that no listed rule requires for the case is not required. This line decides whether an action is required or permitted, on complete and incomplete records alike, ahead of the line on whether the record is complete." SEM-24 prints on every card whose text or questions use a modal phrase, so a deontic question never meets a card without it. Solver A: permitted = not forbidden. Solver B adds the closure as definitions before Clark completion; completion never decides "permitted" or "required" directly; on open cards the status is unknown (base rejected) only when whether a listed rule forbids or requires the action for the case is itself unknown. Deontic heads never use the SEM-05 / SEM-06 fallback (F5-R4-01) | SEM-02, SEM-03, SEM-24, S1; amended by F5-R4-01 |
| F5-R3-02 | Card (SEM-22): "A direct question 'Did any <A> ...?' asks whether at least one <A> did." Card (SEM-23): "'Did anyone other than <A> <do X>?' and 'someone other than <A> <did X>' are about whether at least one member of the group other than <A> did X." Lint per template: "any", "anyone", "anything" only in the matrix interrogative clause or inside "not any", "hardly any", "scarcely any"; never in a positive declarative, so a truth frame's embedded clause uses "some" / "someone other than <A>". "Someone other than <A>" is scope-up in the monotonicity table | SEM-22, SEM-23, 3.4, 4 |
| F5-R3-03 | 2Wiki gold comes from the kept paragraphs: the converter finds each compared value in the kept supporting paragraphs with its own parser and computes the gold from those values. Skip unless each value is stated there, matches the triple at the paragraph's precision, both values share one precision, each entity has exactly one stated value across all kept paragraphs, the values are not tied, and the paragraph answer equals the dataset answer. G3 re-finds the values independently. Card (SEM-32) unchanged: "A comparison is true only if the paragraphs state facts that make it true" | SEM-32, S6, 6 |
| F5-R3-04 | Card (SEM-33): "Each item has three separate states: its holder, its status and whether it is valid ... A creation or a transfer sets the holder, a status entry sets the status, and a '<renewed / valid> for <N> days' entry sets validity; no entry changes any other state ... this replaces any last valid day set by an entry dated before <D>, even one further on, and no other kind of entry moves the last valid day. From the day after its last valid day the item has lapsed (it is not valid), and a renewal dated after that day makes it valid from the renewal's date. A lapse changes neither the holder nor the status." On closed cards an item with no renewal entry is not valid by SEM-02 (the card line does not say it, so open cards keep SEM-03) Asserted: an item with a renewal has no status entries; no validity word in a status list; validity is asked only as "valid" ("active", "expired", "current" banned as validity words) | SEM-33, S2, 3.4, section 0 |
| F5-R3-05 | Card (SEM-31): "A correction replaces the value in the message it names, as if that message had always said it; the corrected message keeps its own date. Retractions and corrections apply whatever their own date, and they are not themselves messages about the fact." Asserted: no retraction or correction by a party shares a date with that party's message about the fact; on a fact base a correction by <S> names <S>'s latest message about the asked fact, so both readings agree. Solver B never puts a retraction or correction into the latest-message comparison | SEM-31, SEM-20, S5, F5-R1-06 |
| F5-R3-06 | Non-decisive check for an unrecorded number or date: test values = each threshold or date of the rules or the question and every other member's value of the same field in the comparison set (counts, "only" and "exactly" items), each with one step either side; both solvers re-solve per test value (S4 solver B re-runs its SQL). An unrecorded entry never sits in the measured field of a superlative's or two-entity comparison's comparison set (asserted). Categories without a value set and yes/no entries get their own test values (F5-R4-05) | SEM-04, S4; amended by F5-R4-05 |
| F5-R3-07 | Card (SEM-02): the complete record "gives every number, date and category detail of each of them or marks it not recorded". Closed cards render every number, date and category attribute of every case and every field of every record or log entry, in every container: a value, "not recorded" / null, or (yes/no fields in containers) blank; no key or attribute is omitted (G3 rejects). A yes/no fact in prose is a closed-world atom (stated or false). Open cards: an unmentioned attribute is unknown (SEM-03). MARKERS.md F5 "missing key" cell to be updated by the orchestrator (section 10 item 12) | SEM-02, SEM-03, S1, S2, S4, 6, 10 |
| F5-R3-08 | Card (SEM-07): "The conditions of a rule are the parts of its 'if' clause joined by 'and'; an 'unless' or 'except when' part is not a condition. A condition is met when what it says is true of the case, so a condition written with 'not' or another negative word is met when the thing it denies is false. 'At least <q> of the conditions of <rule>' means at least <q> of them are met." The form is used only on "if ... then" rules whose "if" clause is a flat conjunction of 2-4 literals with no attached exception (asserted). Trigger: "of the conditions of <rule>" fires SEM-07 | SEM-07, 3.1, S1 |
| F5-R3-09 | Inverted questions name the outcome: "Is <case> among the cases that are <outcome>?" (negated: "Is it true that <case> is not among the cases that are <outcome>?"); gold = whether the outcome holds under the card's semantics. "Meet(s) <rule>", "satisfy", "qualify under <rule>" are banned there. Asserted on every inverted card: for every listed case the outcome holds iff the named rule's conditions hold, so both readings coincide. Monotonicity: identity over the outcome | 8, 3.4, 4, K05, F5-R2-17 |
| F5-R3-10 | Superlatives only as the predicative "<E> has the highest / lowest / most / fewest <X>" or "<E> is the only one with the highest (lowest) <X>"; definite descriptions ("the <entity> with the highest <X>", "the one with the highest <X>", "Is <E> the highest ...?", "the top <entity>") are banned (lint). SEM-13's card meaning (ties shared) is unchanged | SEM-13, 3.4, section 0, F5-R1-05 |
| F5-R3-11 | Card (SEM-20): "A statement about <P> is one that states <P> or states that <P> is false." Asserted: every stance question's <P> is literally the proposition of one of the asked party's statements (as true, or as false through "denied" / "ruled out"), or the party made no statement about that entity and attribute, so no stance label depends on entailment (another SEM-17 value, a day inside an asked month). Strengthened by F5-R4-03: every statement of the asked party about that entity and attribute states <P> or that <P> is false; <S> is never the asked party; <P> is never a SEM-33 state | SEM-20, S2, S5; amended by F5-R4-03 |
| F5-R3-12 | Tier tables are written only as "up to <N1>", "more than <N1> and up to <N2>", ..., "more than <Nk>" and must partition their range under SEM-08 (parser-asserted; a failing table is rejected). Card (SEM-11): "'<N> days after <D>' means the <N>th day after <D> (1 day after <D> is the next day)." S1 offsets use only this phrase (text side); "<N> days before <D>" is banned | SEM-08, SEM-11, SEM-12, S1, 3.4, 4, 6 |

**Spec conflicts (round 3; resolved in favour of `C_DATA_SPEC.md` v4 and the XF section)**

| ID | Conflict | Resolution |
|---|---|---|
| SC7 | XF04 caps no-polarity rows at 5% of all yes/no rows, but F5's design (2Wiki up to about 5% of rows, 4 of 9 S4 base operators non-monotone, stance bases, non-monotone V forms) would put about 15-20% of rows there | Cap met by design (section 8 no-polarity budget): 2Wiki <= 1.5% of bases (S6); S4 bases with "exactly <q>", "highest", "lowest" or "only" <= 1.5% of bases, their share moved to polar operators (S4); no stance bases in training, stance asked only as V rows (S2; S5 dev keeps stance bases and is not C rows); no-polarity V / V' rows <= 1.5% of rows; every S1-S4 base predicate tagged good or bad. Sum <= 4.5%, 0.5 pp drift margin, re-selection on a miss. No XF04 amendment is triggered (section 10 item 14). F5-A31, F5-R1-15 and the XF04 effect row updated |
| SC8 | XF02 says a family-local cue list may stay for polarity logic only, but F5 checked spec 2.2's 25% double-negation floor with its own k | Every F5 count check uses negcount: the 25% floor uses k_all >= 2 (k_all >= k on every row, so about 40%, asserted >= 30%); spec 2.2's P(yes \| number of negation cues) and the G10 cell use k_all; the 2.1 quotas use k_syn (k_syn >= 2 with an affirmative twin from C1 / C2 two-L_core D rows on >= 15% of bases). F5's k stays for polarity logic and as an extra check only. Section 0, section 8, F5-A28, K16 and the XF02 effect row updated; section 10 item 13 logs the reading |

---

## Resolved ambiguities (re-review round 4: F5-R4-01 to F5-R4-07, and spec conflicts SC9-SC10)

Each row states the one semantics now used and, where it reaches a reader, the card text that carries it. Earlier rows
that these change were edited in place (marked "amended by F5-R4-.." or "amended by SC10").

| ID | Resolution (one semantics; card text where it applies) | Where |
|---|---|---|
| F5-R4-01 | Rules are read at the atom level: what a rule gives when it applies is an atom or a negated atom, whatever the polarity of its written head; only a rule that gives a positive atom makes it true, and a rule that gives a negated atom is a constraint (asserted satisfied). So on closed cards, with <B> true and no other rule, the head's positive atom is false by SEM-02: "<E> is not eligible unless <B>" gives not eligible, never "not-A" of a negative head. Deontic heads never use the SEM-05 / SEM-06 fallback; their status always comes from the SEM-24 closure in both worlds, so an open card does not reject when the closure decides. SEM-24 fixes what forbids (an applying "must not / may not / is not permitted to / cannot" head, or "may / is permitted to <X> only if <B>" with <B> false) and what requires (an applying "must / is required to" head), and the rule shapes: "unless" takes only "must", "is required to", "must not", "may not", "is not permitted to", "cannot"; "only if" takes only "may", "is permitted to"; "if ... then" and unconditional rules take any modal (lint). The SEM-02 card line now states the atom-level reading (F5-R5-01: closed-world falsity applies to positive statements, and a statement negated by "not" or a negative prefix holds exactly when its positive form does not); with SEM-05 / SEM-06 ("neither makes <A> hold nor makes it fail"; "<B> being true does not by itself make <A> hold") and SEM-24 (closure, ahead of the world line) the card gives these labels. Both solvers encode it | section 0, SEM-02, SEM-05, SEM-06, SEM-24, S1; amended by F5-R5-01 |
| F5-R4-02 | Card (SEM-11): "A date range in a question about an event asks whether at least one such event falls on some day of the range; one is enough. A 'not' over such a statement means that no such event falls on a day of the range. A date range in a question about a single date asks whether that date falls on some day of the range." Asserted on every event-in-range base: every listed event of the asked kind for the asked entity lies on one side of each boundary date any row of the base asks, and at least one such remaining listed event exists (F5-R5-02), so on closed cards the existential, universal and "the event" readings and both scopes of "not" give the stored label; on open cards the card line decides | section 0, SEM-11, 4 (V rows), S2, F5-R2-03; amended by F5-R5-02 |
| F5-R4-03 | Asserted (S2 and S5 stance questions, checked by solver B): every statement the asked party made about the entity and attribute of <P>, of any date, literally states <P> or literally states that <P> is false, or the party made none; a stance question never names <S> as the asked party; its <P> is a timeless fact or an event, never a SEM-33 state. So no stance label depends on entailment, on another value or date of the same attribute, or on whether an <S> record counts as a statement. Card (SEM-20) unchanged | section 0, SEM-20, S2, S5, F5-R1-01, F5-R3-11 |
| F5-R4-04 | Card (SEM-17), log-status form on S2: "An <item> has no <attribute> before the first entry that sets it; from that entry's date on, it has exactly one <attribute> at a time, one of: <v1>, ..., <vn>." Case and record attributes (S1, S4) keep "Each <entity type> has exactly one <attribute> at a time, one of: ...". Asserted: status entries dated on or after the item's creation; every status question and value test (A, N, D, V, C17) asks a day on or after the item's first remaining status entry; an item whose status entries are all VOIDed gets no status question. Solver B adds the matching domain axiom, so its KB agrees with replay and SEM-02 | section 0, SEM-17, SEM-33, S2, MR8, F5-A15 |
| F5-R4-05 | SEM-04 test set extended: for an unrecorded category without a value set, every category value named in the question, its filters or the rules, every other member's value of that field and one fresh value used nowhere in the case; for an unrecorded yes/no entry (and a blank yes/no entry on an open card), both yes and no. Both solvers re-solve per test value (S4 solver B re-runs its SQL); a base where any test value changes the label is rejected. Card (SEM-04) unchanged | section 0, SEM-04, S4, F5-A11, F5-R2-01, F5-R3-06 |
| F5-R4-06 | Card (SEM-16): "A CORRECTION replaces a value in the entry it names (a holder, a status, a number of days or a stated value), as if that entry had always said the corrected value; the corrected entry keeps its own date, its kind and its item." Asserted, both solvers: a CORRECTION never changes an entry's date, type, item ID or named actor (F5-R5-07), so every entry takes effect on its listed date, the newest-dated renewal is fixed by listed dates and the one-entry-per-day assertion holds after corrections | section 0, SEM-16, SEM-33, S2, F5-A14 |
| F5-R4-07 | Trigger table: "except when" attached to any rule fires SEM-15; "unless" fires SEM-05 in a rule with no "if" clause and SEM-15 when attached to an "if ... then" rule. An "only if" rule carries no "unless" and no "except when", and a rule holds at most one "unless" or "except when" (lint at bank build; asserted by the S1 generator). So every exception phrase prints SEM-05 or SEM-15 on full and short cards alike, and the weak reading is always on the card | section 0, 3.1, SEM-06, SEM-15, S1, F5-A08, F5-R2-08 |

**Spec conflicts (round 4; resolved in favour of `C_DATA_SPEC.md` v4 and the XF section)**

| ID | Conflict | Resolution |
|---|---|---|
| SC9 | The XF07 effect row said F5's S6 GHC / EDOS rows keep the unanimity rule, but section 5 hard-labels GHC by the majority labels in `ghc_train.tsv` (spec 3.2 #16) and never opens the annotator-level file, so unanimity cannot be applied to GHC | Spec 3.2 #16 governs: GHC is hard-labelled by majority from `ghc_train.tsv` (HD or CV; K11); F5's stricter unanimity rule, which XF07 keeps, is its EDOS rule (unanimous posts only). XF07 effect row rewritten; section 10 item 16 logs it. No label changes |
| SC10 | Spec 2.1: two cards must differ in the domain pack and in the label schema or rule set; every F5 card has the Yes / No schema and F5 never said what its rule set is | 3.1 defines a card's rule set (sampler, world or dataset line, full key set from the card's own cue-family set, card constants: value sets, status list, deontic table, <q> / <m>, S6 definition variant). Asserted at card build: no two F5 cards share a rule set, and cards of one sampler and world differ beyond pack words; S6 cards of one dataset differ in definition variant. Section 5 (S6 line), F5-A37 and SC6 updated; section 10 item 15 logs the reading |

## Cross-family fixes (3 Oct, after rounds 4 and 5; from the cross-family checks of all 14 G0 specs)

| ID | Issue | Resolution |
|---|---|---|
| CF-3 | XF10 scope: COMMIT read the shared lint as banning "Is it not the case that" and "Is it false that", which F5 lists as allowed C2 meta-truth frames (3.4) | The XF10 rule text (same in all 14 specs) now says the shared lint bans only outer judgement or acceptance predicates and allows "Is it true that", "Is it not the case that" and "Is it false that" over an affirmative claim; a family may ban more on its own. F5's C2 frames and its 3.4 banned-frame class are unchanged |
| CF-4 | XF18 (cross-family check r2, issue 4): F5's v4 2.1 breaks (section 10 items 8-11: realised per-card yes rate 23.8-76.2%, QuALITY / Qasper not used, 100% twin coverage, polarity-logic scope) waited on one orchestrator amendment, and no F5 row could exist before it | PREREG_FINAL A16 and A16.1 (read for this pass) record no XF18 amendment, so F5 now meets v4 2.1 and 2.2 as written and waits for nothing: (8) r_card is drawn uniformly from 20-80% and realized exactly through a per-card attack share f_card and gold rate a_card (section 8), attack rows staying about 5%; (10) S1-S4 contrast pairs (one input change flips every A, N, D and V gold) put about 22.5% of rows, asserted 20-25%, in XF03 contrast sets (sections 1, 8); (9) and (11) are readings of 2.2 under which nothing is broken (2.2 lists base sources with no shares; F5's label program is the polarity logic of the question's operators evaluated on the base). The section-10 gate, the `<XF18 amendment ID>` slot and the XF03 exemption are removed; K01, K03, K06, K22, SC3, SC5 and F5-R2-15 are rewritten to this one rule |
| CF-5 | XF10 scope (cross-family check r2, issue 3): if the shared lint followed COMMIT's list, it would reject the truth frames F5 lists as allowed C2 meta-truth frames | XF10's scope sentence (truth frames over an affirmative claim are allowed; a family may ban more on its own) already holds in F5's XF10 cell (CF-3). F5's stricter rule, that no L_core word stands in the matrix interrogative clause (SEM-01), keeps "Is it not the case that ...?" out of the matrix and puts C2 "it is not the case that" inside a truth frame, while "Is it false that ...?" may be a matrix C2 frame; this is family-local and is not cited as XF10 (3.4 and the XF10 cell say so). No rule changes |

## Resolved ambiguities (re-review round 5: F5-R5-01 to F5-R5-08, spec conflict SC11, and PREREG ruling A16.1 (g) as F5-R5-09)

Final pass before the freeze. Each row states the one rule now used and, where it reaches a reader, the card text that
carries it. Earlier rows that these change were edited in place (marked "amended by F5-R5-.." or "amended by CF-4"),
so no earlier row states a different rule.

| ID | Resolution (one rule; card text where it applies) | Where |
|---|---|---|
| F5-R5-01 | Card (SEM-02): "A positive statement that the record does not state, and that no rule makes true, is false: it did not happen and does not hold. A statement made negative by 'not' or by a negative prefix (non-, un-, in-, dis-) holds exactly when its positive form (the same statement with that negation taken out) does not hold." So with "<E> is not eligible unless <B>" (or "<E> is ineligible unless <B>"), <B> true and no other rule on a closed card, "eligible" is unstated and no rule makes it true, so <E> is not eligible for the solver and for every reader of the card; "only if" with <B> true reads the same way. Lint: the written head of an S1 rule is a positive atom, that atom with "not", its SEM-18 affixed form or a SEM-24 modal head; no "no", "never" or C3 / C4 / C5 cue stands in an S1 rule head (S3 "No <A> is <B>" universals are SEM-22 statements, not rule heads). Solvers unchanged (atom level, F5-R4-01) | section 0, SEM-02, 3.4, S1, F5-R4-01 |
| F5-R5-02 | Asserted in both worlds by both solvers: every event-in-range base (each has an N row, a C1 / C2 "not" over the range) has, for the asked entity (for an agent-free question, the asked item; for a question over a named group, every member of the group), at least one remaining listed event of the asked kind. With F5-R4-02 (one side of each boundary, which now also covers every member of a named group) no range claim is vacuous, so on closed cards the existential and universal readings, both scopes of "not" and both readings of "not before", "no earlier than", "not after" and "no later than" give the stored label. Card (SEM-11) adds: "these four negated phrases are date words like 'on or before' and 'on or after', not a 'not' over a statement", which decides open cards | SEM-11, S2, F5-R2-03, F5-R4-02 |
| F5-R5-03 | Card (SEM-24) adds: "In a table of roles and actions, 'required' means the role must do the action (so it is also permitted), 'permitted' means the role may do it and need not, and 'forbidden' means the role must not do it; each cell holds in every case, and no other rule is about a role and action that the table lists." Asserted by both solvers: each cell is an unconditional "must" / "may" / "must not" rule, and no listed rule has a head about a tabled (role, action) pair, so a "permitted" cell gives permitted and not required whether a reader takes the table as categories or as rules under the closure. A role and action table prints SEM-24 (structural trigger), and its cell values are SEM-24 trigger phrases | 3.1, SEM-24, S1, F5-A19 |
| F5-R5-04 | Card (SEM-26) adds: "An entry in the record that says something never happened, no longer holds or still holds is a statement by its author about the record: it sets no state and changes none." Text-side "never", "no longer" and "still" appear only in S2 log entries, never in S5 messages (lint), each on a day with no other entry for the same item and state. One by <S> is asserted true under SEM-33 replay and the remaining listed events (on its date; over the covered period for "never"), else the base is rejected; one by another party is a claim (SEM-20). Both solvers parse them as statements, never as state-setting entries | SEM-26, SEM-33, 3.4, C15, S2, S5, 6, F5-R1-03 |
| F5-R5-05 | Structural fields always hold a value, in both worlds (asserted; the parser rejects otherwise): an S2 entry's date, entry type, item ID and (on an action entry) named actor, and an S5 message's date and sender. "Not recorded" / null applies only to value fields, so replay order, "latest", the one-entry-per-day assertion and every SEM-04 test set never involve an unknown date | SEM-02, SEM-04, SEM-31, SEM-33, S2, S5, 6, 10 item 12, F5-A11 |
| F5-R5-06 | Asserted in both worlds by both solvers: every <S> "as of <D>" statement about a state is about a day on or after the remaining entry that first sets that state, and it equals the SEM-33 replay of the remaining listed entries for that item, state and day; such statements set no state. On open cards a state base is kept only when such a statement for the asked day exists, so the printed persistence line (SEM-33) gives the stored label too; on closed cards no statement contradicts replay. Card unchanged | SEM-33, S2, F5-A15, F5-R3-04 |
| F5-R5-07 | Every S2 entry that records an action names its actor ("<E> renewed <item> for <N> days", "<E> transferred <item> to <F>"); for a renewal or a transfer the actor is the item's holder on the entry's date (for a transfer, the holder before it), asserted on the log after CORRECTIONs and VOIDs, and the actor is never a CORRECTION target. A creation entry names the new holder and no actor, and no question or cue names an agent of a creation. "<E> <X>" in a question or cue, and in the SEM-19 "no <X> entry for <E>" assertions, is true of an entry exactly when it names <E> as its actor; an agent-free question counts every entry of that kind for the item. No question or cue about renewing an item whose creation entry states a duration. Because the actor is the holder, the holder-based reading gives the same label. Card unchanged | SEM-16, SEM-19, SEM-33, S2, F5-A12, F5-A14, F5-R4-06 |
| F5-R5-08 | Lint at bank build: no L_core word directly before "all except <A>"; "all" / "every" never combine with "except" or "other than" in one noun phrase other than "all except <A>" itself; a negation over "all except <A>" uses only a C2 frame ("it is not the case that all except <A> ...", "it is false that all except <A> ..."). So "not all except <A>" (NOT(all except <A>) vs "not all" of the others) never appears | SEM-23, 3.4, C11, F5-A08 |
| F5-R5-09 | PREREG A16.1 (g). F5 has no choice rows (inverted cards are yes/no rows, K05), so A16.1 (g)'s choice-row placement (only "- option: definition" card lines are shown) has no F5 target. Every row is a raw yes/no row: `qtype` "noul", `gold` 1 / 0 (never the string "Yes" / "No"), no `options` list, later soft rows `meta.teacher` {"yes": p'}. The card (SEM lines, few-shot examples, inverted-card case lists) goes in `card` and is printed whole; M goes in `state`; the wording and question go in `instructions`; no card line starts "- Yes: " or "- No: ". Every row passes fmt1 `render_and_check` / `loader_check` and `train_decoder.check_rows`, and the < 1,900-token cap counts the served prompt, `instructions` twice. Training rows use formats-1 training styles only; S5 and the probe use the held-out styles; S5 is never a training row; F14 is never trained (XF16) | section 0, 1, 2, 6 (step 5), 9, F5-A34 |

**Spec conflict (round 5; resolved in favour of `C_DATA_SPEC.md` v4 section 8, G0)**

| ID | Conflict | Resolution |
|---|---|---|
| SC11 | Spec 8 G0: "every choice that could flip a label is stated in the card". Three label-deciding F5 rules were on no card line: the atom-level reading of negative and affixed rule heads; the open-card S2 rule that states come only from <S> "as of" statements while SEM-33 prints persistence with no world qualifier; the meaning of a deontic table's "permitted" cell | (1) SEM-02's card line now states the reading (F5-R5-01). (2) A generator restriction removes the case: <S> "as of" statements equal replay in both worlds and an open-card state base needs one, so the printed persistence line gives the stored label (F5-R5-06). (3) SEM-24's card line now states the table's meaning, and tabled pairs are disjoint from the rules (F5-R5-03). No label-deciding choice is left off the card |
