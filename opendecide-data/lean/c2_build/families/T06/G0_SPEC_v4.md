# G0-lite T06 v4: consumer return rights, non-waivable floor vs posted policy (C2 everyday tier; C2_DATA_SPEC 2.1, 3.13)

One page, as C2_DATA_SPEC 6.2 item 3 asks: a semantics table, then frozen (sha in `plugin.T06Plugin.G0_SHA256`;
`validate_plugin` refuses the plugin if this file changes). **v4, frozen 14 Oct 2026, Stage B pilot fix iteration 2** (section 9; v4 = v3 plus S10, S22, section 9 and the G4 partner cards of section 2b; sha256 of v3 was 2d97b12f...). v3 (section 8):
v2 (`G0_SPEC.md`, sha256 4f6b322a..., frozen 13 Oct after the one blind Haiku ambiguity pass) stays the text every pools_v2
task, answer and manifest was authored against (`plugin.G0_SHA256_AUTHORED`); its sections 4 (Haiku tasks), 5 (ambiguity
listing), 6 (resolution) and 7 (Haiku pass H1-H52) are unchanged and are not repeated here. v3 changes S10, S11, S12, S13,
S16, S22, the card texts (section 2) and the samplers' request-day and gold rules (section 3). Any later edit needs a new
sha and a pilot re-run. Target 900 selected rows (about 1,350 generated), wave 1. `solver_b.py` takes its semantics from this
page and its parsing from the kit API (c2_build/README.md), never from `plugin.py`. All jurisdictions, stores, statutes and
notices are invented; no UK or EU text.

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Facts (slots) | CUSTOMER, STORE (names); ORDER_ID (id); ITEM (name, from the pool of its type of goods); JURIS (name, invented); N_REJ, N_WD (counts of days; training {14, 21, 28, 30} / {7, 10, 14}, S5 {20, 35} / {12, 15}); GOODS (category: standard goods / made to the buyer's specification / perishable goods / sealed hygiene goods); SEAL (hygiene goods only: intact / broken after delivery); HANDOVER (handed to the buyer at delivery / delivered to a parcel locker and collected by the buyer later / delivered to a neighbour and collected by the buyer later); REASON (faulty / change of mind); ORDER_DATE < DELIVERY_DATE <= POSSESSION_DATE < REQUEST_DATE as generated (possession = delivery iff handed over at delivery, else 1-6 days later; a request is never generated on the possession day, H1); POLICY (lexicon clause, S9); P_DAYS (count of days, notices with a promise only). One item per order, bought online by a private buyer (the customer); the request covers that whole order. ch_rule rows draw their periods by S10 instead (not from these sets)  |
| S2 | Counting | calendar days (every style says so). The day number of date D from event E is D - E in whole days (E is day zero, the next day is day one). A period of N days from E holds on day numbers 0..N: day N is in time, day N + 1 is late. A right is used on REQUEST_DATE. Notice periods count the same way |
| S3 | Printed intermediates | D_ORDER, D_DELIV, D_POSS = day numbers of REQUEST_DATE from ORDER_DATE, DELIVERY_DATE, POSSESSION_DATE, printed in the record on every row except deep rows (S19). Solver B re-walks each one day by day |
| S4 | Rejection right (reject) | gives a full refund iff REASON = faulty and D_DELIV <= N_REJ (anchor: delivery = the record's "delivered on" date, the day the goods reached the buyer, the locker or the neighbour; never order or possession). No exclusion ever limits it |
| S5 | Withdrawal right (withdraw) | gives a full refund iff the goods are not excluded (S6) and D_POSS <= N_WD (anchor: possession). Any reason, so a faulty return can also use it |
| S6 | Exclusions (withdrawal only) | made to the buyer's specification; perishable goods; sealed hygiene goods with SEAL = broken after delivery. Hygiene goods with SEAL = intact are NOT excluded (the seal condition) |
| S7 | Floor | a store notice cannot remove or shorten S4 or S5 (a stricter notice never wins); a full refund the notice itself promises (S9) is owed as well (a more generous notice applies) |
| S8 | Outcome | a full refund is owed iff S4, S5 or the notice promise holds. "Full refund" is the cards' own term: no amount, delivery charge, postage or deduction exists in any case. Store credit or an exchange is not a full refund |
| S9 | Notice meanings (lexicon sems; quoted after "{STORE} posted this notice at its checkout and on its website:") | `pol.t06.final`, `pol.t06.credit`, `pol.t06.nocustom`: no promise (kind deontic, 2/2 extraction). `pol.t06.faulty_order` {P}: faulty returns, P days from the purchase (order) date; `pol.t06.mind_order` {P}: change of mind, P from the purchase date; `pol.t06.any_order` {P}: any reason, P from the purchase date; `pol.t06.any_delivery` {P}: any reason, P from delivery (kind window, 3/3). Every promise form says "full refund" or "refund(ed) in full", names its start with purchase / order / bought or delivery / delivered, and names no type of goods, condition or other number, so a promise covers every type of goods. G-LEX lists add never-generated decoys (deontic: a full refund on some returns; window: credit or an exchange within P days; returns within P days, remedy unstated; P days from receipt or collection); a form read as a decoy is rejected. The one notice applies from the order date to the request date; whether the buyer read it never matters. P sets: faulty_order {3, 5, 7, 10, 45, 60}, mind_order {3, 5, 7, 30, 45, 60}, any_order {7, 10, 30, 60}, any_delivery {7, 10, 30, 45, 60, 90} |
| S10 | ch_rule | which rule gives the full refund. Options = the rules the record's coarse facts leave open plus "none" (the abstain option; texts per style, section 2): reject iff REASON = faulty; withdraw iff the goods are not excluded (S6); store iff the notice promises a refund for this REASON (S9); at least two rules are shown, so k = 3 or 4, in one label-blind order of the row key; a twin shows the same options as its base. Gold = the only rule that gives the refund, or none; generated only when at most one rule gives it. The display size k is set by the record's coarse facts (before any target). The shown options sit in one label-blind order of the row key (a function of the key and the display alone, so a twin shows the same list in the same order), the kit ChoicePlan of the row key (closed set of the shown rules, abstain shown) plans the gold's position (uniform over the k places by construction), and the target is the option AT that position: the position is scheduled, never left to the draw, and "none" (or any rule) is gold on 1 / k of the rows (kit choiceplan abstain band). Windows: the target's window ends on a day drawn from 9..34 days after possession (S5: 35..45), every other window 1..3 days earlier (a refusal: all windows end within 3 days of one another, the request after the last); each period is its window's end minus its anchor lag (reject: end + days from delivery to possession; withdraw: end; notice: end + days from its anchor to possession), so no printed number says which rule wins. The request is one of the last 4 days of the target's window (refusal: one of the first 4 days after the last window) |
| S11 | yes/no forms (predicate refund) | yn_refund (subject the customer), yn_owed (subject the store), yn_double: yes iff a full refund is owed. yn_not_refund (syntactic), yn_no_right (syntactic), yn_may_refuse ("may the store refuse...", antonym): yes iff none is owed. Every wording names a full refund. Negation = pinned c_src/common/negcount.py v1.1 on the wording: k_all counts every cue it lists (not, n't, no, none, never, nobody, nothing, nor, without, "it is not the case that", ...), k_syn its syntactic cues; "refuse", "decline", "turn down" are not cues. Exact (k_all, k_syn): (0, 0) yn_refund, yn_owed, yn_may_refuse; (1, 1) yn_not_refund (not / n't on the verb), yn_no_right (no before a noun); (2, 2) yn_double. Wording polarity (kit polarity.py P1-P3, POLARITY_CHECK; P4 off): a wording negates a positive predicate or uses an antonym word (refuse, decline, turn down, deny, withhold), never both; yn_double has two syntactic negations over a positive predicate |
| S12 | Rules (program text) | the statute excerpt in its style (section 2, one line per section) + newline + closed-world sentence "The rules, the posted notice and the order record are complete; no other fact or message changes the case.". On yes/no rows this is `row.card` (printed once); on choice rows it is the head of the instructions, before the question (kit cards.place_rules). Variant per row from the row key: full 25% / compact 60% / short 15% of training rows (S5: full only); compact and short keep every slot, number, operator word and negation count of full (kit cards.CardSpec problems() = []). Then a blank line and the question. No digit outside the slots. The state is a separate field; `meta.defs_style` = rules_in_card_<variant> |
| S13 | Record (program text) | header "Order record {ORDER_ID} from {STORE}:" + bullet lines "- label: value" or a markdown table "| field | value |"; or "Order record (JSON):" + one JSON object. Labels in order: item, type of goods, seal (hygiene only), handover, ordered on (the purchase date), delivered on, buyer took possession on, return requested on, reason for the return, days from the purchase date to the request, days from delivery to the request, days from possession to the request. JSON keys: order_id, store, item, goods_type, seal, handover, purchase_date, delivered_on, possession_on, return_requested_on, reason, days_purchase_to_request, days_delivery_to_request, days_possession_to_request (string values). An absent field (seal off hygiene goods; the counts on deep rows) is omitted from every container, never null or n/a. The three printed day counts are always written in digits ("27 days"), on every row, so the number of numerals says nothing about how late the request is |
| S14 | Container | first match wins: JSON if S5 or a json / yaml skin; else a table if S3 or a ticket / form skin; else bullet lines (label-blind: sampler and skin register only) |
| S15 | State layout | blocks joined by one blank line. S1, S2, S5: message, record, notice. S3: record, notice, message. S4: notice, message, record, and S4 draws chat or email skins first (other registers only when those pools are empty). An inv row adds one last block at the end of the state: "Message added to the case: " + one attack line, which is never a fact (closed world) |
| S16 | ch_end_reject / ch_end_withdraw | gold = DELIVERY_DATE + N_REJ / POSSESSION_DATE + N_WD: the last in-time day (S2) of the named statutory right's own period. The wording names that right and never the notice (section 4), so a notice never moves the gold and anchor + P is the error t06_notice_period. Generated only for faulty returns / goods not excluded. Options: gold + 2-3 error-model dates (S18), all in the row's one date form (iso, "4 March 2027", "March 4, 2027", "4 Mar 2027", or with a weekday; never a numeric day/month form). An output equal to the gold is dropped; equal outputs of several models are one option naming each model; a spec whose dates leave a side of the gold empty is dropped. The option count k = 3 or 4 and the gold's position and sorted rank among the dates come from the kit's ChoicePlan of the row key (build_options plan=; twins strict_plan False), with no abstain option; an option equal to a date the record prints is not allowed (another structure is drawn, never another option) (v1 put the gold between the day-0 and one-day-late dates and "take the second-highest date" scored 0.71 vs chance 0.25) |
| S17 | Complement pairs (same state and card) | yn_refund -> yn_may_refuse 60% / yn_not_refund; yn_owed -> yn_may_refuse 60% / yn_no_right; yn_double -> yn_no_right / yn_not_refund; yn_not_refund -> yn_refund 70% / yn_double; yn_may_refuse -> yn_refund / yn_owed; yn_no_right -> yn_owed 70% / yn_double. Syntactic pairs differ by one negation cue, antonym pairs by none |
| S18 | Error models | ch_rule: `t06_sign_wins` (statute ignored: the notice's promise alone decides, giving store or none), `t06_ignore_notice` (statute only), `t06_order_date_anchor`, `t06_delivery_for_possession`, `t06_possession_for_delivery`, `count_day0` (period ends a day early), `off_by_one_late`, `t06_absolute_exception` (hygiene excluded with the seal intact; exclusions applied to S4), `ignore_exception`, `t06_swap_periods`, `t06_notice_from_delivery`, `t06_notice_any_reason`, `t06_reason_picks_rule` (faulty -> reject, change of mind -> withdraw), `t06_other_right` (the reverse), `t06_sign_decides` (always names the notice). A model whose mistaken reading has two granting rules outputs nothing for that row (the row stays). ch_end: order date + N, the swapped anchor + N, anchor + N - 1, anchor + N + 1, anchor + the other period, `t06_both_ends_early` / `_late` (anchor + N - 2 / anchor + N + 2), `t06_business_days` (N weekdays), `t06_notice_period` (anchor + the notice's days). Every wrong option names >= 1 model |
| S19 | Depth | 2 unstated operations: which rights (and the notice) can apply by reason, exclusion and notice scope; compare the printed count with the period. Deep rows (6% of yes/no and ch_rule base specs, so about 5% of all rows: ch_end is never deep; meta.deep) omit the S3 counts: 3 operations, counting across month ends and leap days. ch_end: 2 (anchor, date + N) |
| S20 | Solver A | decision tables on day ordinals: exclusion table (goods, seal); rejection table (reason, in time); withdrawal table (excluded, in time); notice table (sem, reason) -> anchor date; outcome table over the three grant bits -> (refund, deciding rule); question table. Paradigm decision_table |
| S21 | Solver B | own parser (four card templates, three record readers, notice through `lexicon.parse_exact` on admitted forms, message through `skin.parse_skin`, wording template); each period is the list of its calendar days built day by day (`brute.window_days`) and a right holds iff REQUEST_DATE is in that list; printed counts are re-walked with `brute.day_list`; a separate exclusion evaluator; its own notice-meaning and question tables. Paradigm day_bitmap |
| S22 | Relations | rates per base spec: complement (S17) on 42% of yes/no base specs; minimal-edit twin tried on 48% of base specs (one input slot: request date to the rejection, withdrawal or notice period end or the day after, reason, seal, delivery or possession date (not when handed over at delivery), N_REJ, N_WD, P_DAYS, or the notice meaning among the four promises; prediction from the edited facts; a ch_rule twin keeps one deciding rule; one that moves the gold onto none is kept at 0.22 (k = 3) / 0.05 (k = 4) (kit relations.abstain_twin_kept; else the next edit naming a rule is taken), so none is 1 / k of ALL emitted ch_rule rows in each k cell, not only base rows); equiv (another skin, register and container) 11%; inv (one attack line) 4%. G4 (yes/no and ch_rule answer unchanged; ch_end gold + 7 on the date shift): rename customer, item (same type of goods), store, jurisdiction; shift all four dates by seven days; swap one no-promise notice for another. G4 added in v4 (metamorphic: checked by solver A, solver B and every row gate; never emitted; only proposed where the gold really flips; prediction from the edited facts): rule-swap (same facts, the notice rule of section 2b flipped; gold flips where the statute alone gave the refund), rule-deleted (the withdrawal rule and its exclusions removed from the card; the gold becomes no refund, or the option "none", where withdrawal alone gave the refund; hash rates 0.55 and 0.60 of base specs), nonce vocabulary (customer, store, item and jurisdiction names replaced by invented words, 10% of base specs; answer unchanged) |

## 2. Card texts (program text; one line per section; solver B keeps its own copy)

Three variants (S12). `full` is the frozen v2 card, unchanged; `compact` and `short` only drop filler. S5 uses the regulation card (full only).

full (25%):

```
act: Consumer Sales Act of {JURIS} (excerpt)
Section I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and the period includes its last day.
Section II (faulty goods). A buyer may reject faulty goods and get a full refund within {N_REJ} from the delivery date.
Section III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within {N_WD} from the day the buyer took possession of the goods. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.
Section IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.
code: Civil Code of {JURIS}, consumer sales, Article K (extract)
(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the limit still counts.
(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts {N_REJ}, counted from the date of delivery.
(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts {N_WD}, counted from the date the buyer took possession of the goods.
(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.
(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.
charter: Buyer's Rights Charter of {JURIS} (summary every store must display)
- Counting days: you use a right on the day you ask for it. Periods count calendar days: a period's event day is day zero, the next day is day one, and the last day of the period still counts. Store notices count days the same way.
- Faulty-goods rule: you can reject faulty goods and get a full refund within {N_REJ} from the day they were delivered.
- Cooling-off rule: for any reason, you can withdraw from a purchase and get a full refund within {N_WD} from the day you took possession of the goods. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery. These exclusions never limit the faulty-goods rule.
- Store notices: a store notice cannot take away or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.
regulation (S5 only): Distance Sales Regulations of {JURIS}, Part R (extract)
Reg. A (periods). A right is exercised on the day the consumer requests it. A period counts whole calendar days from its event: the event day is day zero, the next day is day one, and the final day is included. A trader's notice counts days the same way.
Reg. B (rejection). A consumer may reject faulty goods and is due a full refund if the rejection is made within {N_REJ} of delivery.
Reg. C (cancellation). A consumer may cancel a purchase for any reason and is due a full refund if the cancellation is made within {N_WD} of taking possession of the goods. Reg. C does not apply to goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery. Reg. B is not limited by these exclusions.
Reg. D (notices). A trader's notice cannot exclude or shorten these rights. A trader may promise more, and a full refund its posted notice promises is due.
```

compact (60%):

```
act: Consumer Sales Act of {JURIS} (excerpt)
Section I (counting days). A right is used on the day the buyer asks for it. Periods in this Act or in a store notice run in calendar days from an event: the event's day is day zero, and the last day counts.
Section II (faulty goods). A buyer may reject faulty goods and get a full refund within {N_REJ} of delivery.
Section III (withdrawal). A buyer may withdraw for any reason and get a full refund within {N_WD} from the day the buyer took possession. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.
Section IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.
code: Civil Code of {JURIS}, consumer sales, Article K (extract)
(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, and the final day still counts.
(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts {N_REJ} from the date of delivery.
(c) A buyer may withdraw for any reason and be refunded in full; this right lasts {N_WD} from the date the buyer took possession.
(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.
(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.
charter: Buyer's Rights Charter of {JURIS} (summary every store must display)
- Counting days: you use a right on the day you ask for it. Periods count calendar days: a period's event day is day zero, and the last day still counts. Store notices count days the same way.
- Faulty-goods rule: you can reject faulty goods and get a full refund within {N_REJ} from the day they were delivered.
- Cooling-off rule: for any reason, you can withdraw and get a full refund within {N_WD} from the day you took possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery. These exclusions never limit the faulty-goods rule.
- Store notices: a store notice cannot take away or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.
```

short (15%):

```
act: Consumer Sales Act of {JURIS} (excerpt)
Section I. A right is used on the day the buyer asks for it. Periods in this Act or in a store notice are calendar days from an event: the event's day is day zero, the last day counts.
Section II. A buyer may reject faulty goods for a full refund within {N_REJ} of delivery.
Section III. A buyer may withdraw for any reason for a full refund within {N_WD} of taking possession. It does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.
Section IV. A store notice cannot remove or shorten these rights. A store may promise more; a full refund its posted notice promises is owed.
code: Civil Code of {JURIS}, consumer sales, Article K (extract)
(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the final day still counts.
(b) A buyer may reject faulty goods and be refunded in full; the right lasts {N_REJ} from delivery.
(c) A buyer may withdraw for any reason and be refunded in full; the right lasts {N_WD} from taking possession.
(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.
(e) A seller's notice cannot remove or shorten these rights. A seller may promise more; a full refund its posted notice promises is owed.
charter: Buyer's Rights Charter of {JURIS} (summary every store must display)
- Counting days: you use a right on the day you ask for it. Periods are calendar days: the event day is day zero, the last day still counts. Store notices count the same way.
- Faulty-goods rule: you can reject faulty goods for a full refund within {N_REJ} of delivery.
- Cooling-off rule: for any reason, you can withdraw for a full refund within {N_WD} of taking possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions never limit the faulty-goods rule.
- Store notices: a store notice cannot take away or shorten these rights. A store may promise more; a full refund its posted notice promises is owed.
```

ch_rule option texts: act "Section II (faulty goods)" / "Section III (withdrawal)" / "The store's posted notice" / "None of
them: no full refund is owed"; code "Article K(b) (faulty goods)" / "Article K(c) (withdrawal)" / "The seller's posted
notice" / same none; charter "The faulty-goods rule" / "The cooling-off rule" / "The store's posted notice" / same
none; regulation "Reg. B (rejection)" / "Reg. C (cancellation)" / "The trader's posted notice" / "None of them: no full
refund is due". The style labels (act, code, charter, regulation) are never printed. {N_REJ} / {N_WD} are count slots
that always print their unit ("14 days", "fourteen days"; never a bare number).

## 2b. G4 partner cards (v4; program text; never an emitted row)

Rule-swap: the last rule line of the card (the notice rule) is replaced by
act `Section IV (store notices). A store notice replaces these rights: the buyer gets a full refund only if the store's posted notice promises one.`;
code `(e) A seller's notice replaces these rights: the buyer gets a full refund only if the seller's posted notice promises one.`;
charter `- Store notices: a store notice replaces these rights: you get a full refund only if the store's posted notice promises one.`;
regulation `Reg. D (notices). A trader's notice replaces these rights: the consumer is due a full refund only if the trader's posted notice promises one.`
Rule-deleted: the withdrawal line is dropped (act Section III; code (c) and (d); charter the cooling-off rule; regulation Reg. C);
no refund is owed under a right the card does not state (the closed-world sentence stays). Every other line and variant is unchanged.

## 3. Samplers, shares, traps, balance

- **Samplers.** S1 forward. S2 near misses: like every sampler it draws the target before the scenario ("label-first");
  it adds 0.30 to each trap-preference probability (0.08 -> 0.38: the request day sits on a period end or the day after,
  the order date flips the answer, an exclusion's condition decides). S3 record-table-first. S4 notice-first chat
  thread. S5 held out: Regulations style, held-out jurisdictions and periods, JSON record, held-out skins, registers,
  wordings and packs (mixdev only).
- **Cards.** 6 per training sampler (24 training cards, style = card mod 3; about 35-55 rows each) and 4 for S5.
  Per-card yes rate drawn in [0.2, 0.8], cards paired antithetically (mean exactly 0.5). Fix i3: the yes gold is drawn label-first (stateless error diffusion over each 4,096-seed block, card rate and form half tracked) and the wording is a round-robin over the rank within (form, yes), so every form and every (form, wording) cell is 50% yes.
- **Request day (yes/no rows).** Never uniform over the days that hit the target: a refund is one of the last 4 days of an applicable window (a random one of them); a refusal with an applicable rule is one of the first 4 days after the latest window; a refusal with no applicable rule is one of the last 4 days of a period the case does not use. So the size of the printed day counts is the same in both classes (v2: refund rate 0.35 in the top decile of the mean numeral magnitude).
- **Draw order.** Label-blind first: card, style, jurisdiction, question form, deep flag, names, order id, N_REJ, N_WD,
  trap preferences. Then the target (low-discrepancy draw), then a scenario (reason 50/50; goods standard 40 / custom 18
  / perishable 14 / hygiene 28, seal 50/50; handover 60 / 25 / 15; notice final 16, credit 11, nocustom 8, faulty_order
  14, mind_order 19, any_order 15, any_delivery 17) redrawn at most 200 times (8 date draws each) until some request day
  gives the target; if none does, the seed is skipped (the target never changes). Dates: shipping 1-8 days, pickup 1-6
  days; delivery in February days 7-28 (22%, leap and common years), else in the last 8 days of any month (33%; a
  disjoint draw), else uniform; the request day chosen among the days that realise the target and lie near a window end (see above; with the trap
  preferences).
  (yes/no and ch_end rows; a ch_rule row draws its display, then the target uniformly over it, then lags, delivery and the windows of S10.)
- **Question forms (base rows).** ch_rule 42%, ch_end_reject 7%, ch_end_withdraw 7%, yes/no 44% (yn_refund 11, yn_owed 8,
  yn_double 3, yn_not_refund 7, yn_may_refuse 10, yn_no_right 5). After partners, yes/no rows are 45-55% of the family.
- **Gold.** Yes/no 50 +- 2 (per form 47.9-50.9% on 12,000 specs); "yes = bad outcome" (bad for the buyer: yes means no full
  refund, QuestionForm.yes_is_bad) 50 +- 5. ch_rule: uniform over the display (S10): none 1 / k, each shown rule (1 - 1 / k) /
  (k - 1). Refund rate per goods type, reason, notice, handover and style: 44-54% on 12,000 specs.
- **Traps (overlapping shares of rows, measured on 12,000 training specs; spec 3.13 target in brackets).** Stricter
  notice, the statute wins 27% [25]; order date vs delivery (the order-date anchor flips the answer) 31% [20]; boundary
  day (one day earlier or later flips it) 48% [20] (v3: every request sits within 4 days of a window end); conditional
  exception 16% [15] (= the t06_absolute_exception mistake flips the decision: hygiene goods with the seal intact, or
  excluded goods returned faulty inside the rejection period); a more generous notice decides 16% [10]. Tags go by which
  rule gives the refund (stricter: the statute gives it, the notice does not and reads as refusing the case; generous:
  only the notice gives it); each notice is one promise or none, so no notice is mixed. Also: delivery vs possession
  anchor 12%, leap day inside the dates 11%, the request in another month than delivery 81%.
- **Overlay (measured shares of emitted rows; pilot dry run of 1,001 rows, S1-S4).** Complement partners 40% of yes/no rows
  (59% non-syntactic pairs); twins 20% of rows (spec 4.1: 20-25; twin rate 0.48); equiv 6%; inv 2%; deep 5%; yes 49%. Units
  hold at most 3 rows. Real tokens (pinned tokenizer, rules in row.card on yes/no rows): mean about 777, max about 1,054.

## 4-7. Unchanged from v2

Haiku tasks, the ambiguity listing (A1-A16), its resolution and the Haiku ambiguity pass (H1-H52) are as in `G0_SPEC.md` (v2, sha256
4f6b322adab8a1810ac165686a2305d28607de558131118780c52da5f0e59563) sections 4-7; the frozen pools_v2 were authored against v2. Of the
v2 rulings only those that name a ch_rule display (H10: "all four keys") and the card line placement change, as S10 and S12 say. No
frozen wording, skin, notice form or attack line changes; the polarity screen (S11) finds no frozen yes/no wording to quarantine.

## 8. Stage B pilot fix iteration 1 (14 Oct 2026; iteration-0 verdict G6, G10 and spec 3.0 failed; no bar loosened, no label touched)

1. Rules in `row.card` on yes/no rows, three variants (S12): spec 3.0 token mean 926.8 (iteration 0; bar 800) now about 777.
2. ch_rule (S10): v2 showed all four keys, drew the periods before the target, and the coarse facts alone predicted the key
   (card view LR 0.367 vs chance 0.262 at iteration 0). Now display = the open rules + none, target uniform over it, windows label-first; none is 1 / k
   (abstain band), twins thinned per k; periods and printed counts carry no rule cue (card view at chance).
3. Yes/no request day near a window end and counts always digits (S13, section 3): the metadata view (0.551 at iteration 0) no longer separates the labels.
4. ch_end (S16): kit ChoicePlan for k, position and rank; options equal to a printed date are never used. G10 gold-is-longest (+2.87 pp at iteration 0): none is 1 / k in every k cell (S22).
5. Polarity (S11): kit polarity check on; solver B and the tests read the new cards (G0 v3 section 2).
G6 is also reported at 6,000 rows (PREREG A43): pilot_i1/G6_AT_6000.json.

## 9. Stage B pilot fix iteration 2 (14 Oct 2026; iteration-1 verdict FIX: G3-H item article, G10 gold_position; no bar loosened, no label touched)

1. G3-H: the extraction schema's item field now says the item is the name of the goods without any article or possessive before
   it (leave out the, my, a, an). Mode F (v2 section 4 item 2) still writes "the" or "my" before ITEM; the generator's item value is the bare name.
2. G10 gold_position (chi-square p 0.0096 at k = 3, 6,000 rows; bar p > 0.01): the ch_rule gold position is scheduled by construction
   (S10: the kit ChoicePlan's position from the row key; the target is the option at that position of the key's fixed order).
3. G4 relation set (S22, section 2b): rule-swap, rule-deleted and nonce-vocabulary relations (FINAL_PLAN section 2 item 5).
