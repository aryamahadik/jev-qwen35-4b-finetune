# G0-lite T06: consumer return rights, non-waivable floor vs posted policy (C2 everyday tier; C2_DATA_SPEC 2.1, 3.13)

One page, as C2_DATA_SPEC 6.2 item 3 asks: a semantics table, one ambiguity listing, one resolution, then frozen (sha in
`plugin.T06Plugin.G0_SHA256`; `validate_plugin` refuses the plugin if this file changes). v2, frozen 13 Oct 2026 after
the one blind Haiku ambiguity pass (section 7): any later edit needs a new sha, a rerun of the family tests and a note in
section 7. Target 900 selected rows (about 1,350 generated), wave 1. `solver_b.py` takes its semantics from this page and
its parsing from the kit API (c2_build/README.md), never from `plugin.py`. All jurisdictions, stores, statutes and notices
are invented; no UK or EU text.

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| S1 | Facts (slots) | CUSTOMER, STORE (names); ORDER_ID (id); ITEM (name, from the pool of its type of goods); JURIS (name, invented); N_REJ, N_WD (counts of days; training {14, 21, 28, 30} / {7, 10, 14}, S5 {20, 35} / {12, 15}); GOODS (category: standard goods / made to the buyer's specification / perishable goods / sealed hygiene goods); SEAL (hygiene goods only: intact / broken after delivery); HANDOVER (handed to the buyer at delivery / delivered to a parcel locker and collected by the buyer later / delivered to a neighbour and collected by the buyer later); REASON (faulty / change of mind); ORDER_DATE < DELIVERY_DATE <= POSSESSION_DATE < REQUEST_DATE as generated (possession = delivery iff handed over at delivery, else 1-6 days later; a request is never generated on the possession day, H1); POLICY (lexicon clause, S9); P_DAYS (count of days, notices with a promise only). One item per order, bought online by a private buyer (the customer); the request covers that whole order |
| S2 | Counting | calendar days (every style says so). The day number of date D from event E is D - E in whole days (E is day zero, the next day is day one). A period of N days from E holds on day numbers 0..N: day N is in time, day N + 1 is late. A right is used on REQUEST_DATE. Notice periods count the same way |
| S3 | Printed intermediates | D_ORDER, D_DELIV, D_POSS = day numbers of REQUEST_DATE from ORDER_DATE, DELIVERY_DATE, POSSESSION_DATE, printed in the record on every row except deep rows (S19). Solver B re-walks each one day by day |
| S4 | Rejection right (reject) | gives a full refund iff REASON = faulty and D_DELIV <= N_REJ (anchor: delivery = the record's "delivered on" date, the day the goods reached the buyer, the locker or the neighbour; never order or possession). No exclusion ever limits it |
| S5 | Withdrawal right (withdraw) | gives a full refund iff the goods are not excluded (S6) and D_POSS <= N_WD (anchor: possession). Any reason, so a faulty return can also use it |
| S6 | Exclusions (withdrawal only) | made to the buyer's specification; perishable goods; sealed hygiene goods with SEAL = broken after delivery. Hygiene goods with SEAL = intact are NOT excluded (the seal condition) |
| S7 | Floor | a store notice cannot remove or shorten S4 or S5 (a stricter notice never wins); a full refund the notice itself promises (S9) is owed as well (a more generous notice applies) |
| S8 | Outcome | a full refund is owed iff S4, S5 or the notice promise holds. "Full refund" is the cards' own term: no amount, delivery charge, postage or deduction exists in any case. Store credit or an exchange is not a full refund |
| S9 | Notice meanings (lexicon sems; quoted after "{STORE} posted this notice at its checkout and on its website:") | `pol.t06.final`, `pol.t06.credit`, `pol.t06.nocustom`: no promise (kind deontic, 2/2 extraction). `pol.t06.faulty_order` {P}: faulty returns, P days from the purchase (order) date; `pol.t06.mind_order` {P}: change of mind, P from the purchase date; `pol.t06.any_order` {P}: any reason, P from the purchase date; `pol.t06.any_delivery` {P}: any reason, P from delivery (kind window, 3/3). Every promise form says "full refund" or "refund(ed) in full", names its start with purchase / order / bought or delivery / delivered, and names no type of goods, condition or other number, so a promise covers every type of goods. G-LEX lists add never-generated decoys (deontic: a full refund on some returns; window: credit or an exchange within P days; returns within P days, remedy unstated; P days from receipt or collection); a form read as a decoy is rejected. The one notice applies from the order date to the request date; whether the buyer read it never matters. P sets: faulty_order {3, 5, 7, 10, 45, 60}, mind_order {3, 5, 7, 30, 45, 60}, any_order {7, 10, 30, 60}, any_delivery {7, 10, 30, 45, 60, 90} |
| S10 | ch_rule | which rule gives the full refund: closed set {reject, withdraw, store, none} (texts per style, section 2), all four always shown, label-blind order. Gold = the only rule that gives it, or none. Generated only when at most one rule gives it |
| S11 | yes/no forms (predicate refund) | yn_refund (subject the customer), yn_owed (subject the store), yn_double: yes iff a full refund is owed. yn_not_refund (syntactic), yn_no_right (syntactic), yn_may_refuse ("may the store refuse...", antonym): yes iff none is owed. Every wording names a full refund. Negation = pinned c_src/common/negcount.py v1.1 on the wording: k_all counts every cue it lists (not, n't, no, none, never, nobody, nothing, nor, without, "it is not the case that", ...), k_syn its syntactic cues; "refuse", "decline", "turn down" are not cues. Exact (k_all, k_syn): (0, 0) yn_refund, yn_owed, yn_may_refuse; (1, 1) yn_not_refund (not / n't on the verb), yn_no_right (no before a noun); (2, 2) yn_double |
| S12 | Card (program text, instructions) | the statute excerpt in its style (section 2, one line per section) + newline + closed-world sentence "The rules, the posted notice and the order record are complete; no other fact or message changes the case." + blank line + the question. No digit outside the slots. The card is the instructions field, the state is a separate field |
| S13 | Record (program text) | header "Order record {ORDER_ID} from {STORE}:" + bullet lines "- label: value" or a markdown table "| field | value |"; or "Order record (JSON):" + one JSON object. Labels in order: item, type of goods, seal (hygiene only), handover, ordered on (the purchase date), delivered on, buyer took possession on, return requested on, reason for the return, days from the purchase date to the request, days from delivery to the request, days from possession to the request. JSON keys: order_id, store, item, goods_type, seal, handover, purchase_date, delivered_on, possession_on, return_requested_on, reason, days_purchase_to_request, days_delivery_to_request, days_possession_to_request (string values). An absent field (seal off hygiene goods; the counts on deep rows) is omitted from every container, never null or n/a |
| S14 | Container | first match wins: JSON if S5 or a json / yaml skin; else a table if S3 or a ticket / form skin; else bullet lines (label-blind: sampler and skin register only) |
| S15 | State layout | blocks joined by one blank line. S1, S2, S5: message, record, notice. S3: record, notice, message. S4: notice, message, record, and S4 draws chat or email skins first (other registers only when those pools are empty). An inv row adds one last block at the end of the state: "Message added to the case: " + one attack line, which is never a fact (closed world) |
| S16 | ch_end_reject / ch_end_withdraw | gold = DELIVERY_DATE + N_REJ / POSSESSION_DATE + N_WD: the last in-time day (S2) of the named statutory right's own period. The wording names that right and never the notice (section 4), so a notice never moves the gold and anchor + P is the error t06_notice_period. Generated only for faulty returns / goods not excluded. Options: gold + 2-3 error-model dates (S18), all in the row's one date form (iso, "4 March 2027", "March 4, 2027", "4 Mar 2027", or with a weekday; never a numeric day/month form). An output equal to the gold is dropped; equal outputs of several models are one option naming each model; a spec whose dates leave a side of the gold empty is dropped. The gold's sorted rank among the dates is the kit's label-blind target_rank(row key, k) and k = 3 or 4 by a label-blind draw sized by kit ordered_k (the same for every rank): v1 put the gold between the day-0 and one-day-late dates and "take the second-highest date" scored 0.71 vs chance 0.25 (review fix) |
| S17 | Complement pairs (same state and card) | yn_refund -> yn_may_refuse 60% / yn_not_refund; yn_owed -> yn_may_refuse 60% / yn_no_right; yn_double -> yn_no_right / yn_not_refund; yn_not_refund -> yn_refund 70% / yn_double; yn_may_refuse -> yn_refund / yn_owed; yn_no_right -> yn_owed 70% / yn_double. Syntactic pairs differ by one negation cue, antonym pairs by none |
| S18 | Error models | ch_rule: `t06_sign_wins` (statute ignored: the notice's promise alone decides, giving store or none), `t06_ignore_notice` (statute only), `t06_order_date_anchor`, `t06_delivery_for_possession`, `t06_possession_for_delivery`, `count_day0` (period ends a day early), `off_by_one_late`, `t06_absolute_exception` (hygiene excluded with the seal intact; exclusions applied to S4), `ignore_exception`, `t06_swap_periods`, `t06_notice_from_delivery`, `t06_notice_any_reason`, `t06_reason_picks_rule` (faulty -> reject, change of mind -> withdraw), `t06_other_right` (the reverse), `t06_sign_decides` (always names the notice). A model whose mistaken reading has two granting rules outputs nothing for that row (the row stays). ch_end: order date + N, the swapped anchor + N, anchor + N - 1, anchor + N + 1, anchor + the other period, `t06_both_ends_early` / `_late` (anchor + N - 2 / anchor + N + 2), `t06_business_days` (N weekdays), `t06_notice_period` (anchor + the notice's days). Every wrong option names >= 1 model |
| S19 | Depth | 2 unstated operations: which rights (and the notice) can apply by reason, exclusion and notice scope; compare the printed count with the period. Deep rows (6% of yes/no and ch_rule base specs, so about 5% of all rows: ch_end is never deep; meta.deep) omit the S3 counts: 3 operations, counting across month ends and leap days. ch_end: 2 (anchor, date + N) |
| S20 | Solver A | decision tables on day ordinals: exclusion table (goods, seal); rejection table (reason, in time); withdrawal table (excluded, in time); notice table (sem, reason) -> anchor date; outcome table over the three grant bits -> (refund, deciding rule); question table. Paradigm decision_table |
| S21 | Solver B | own parser (four card templates, three record readers, notice through `lexicon.parse_exact` on admitted forms, message through `skin.parse_skin`, wording template); each period is the list of its calendar days built day by day (`brute.window_days`) and a right holds iff REQUEST_DATE is in that list; printed counts are re-walked with `brute.day_list`; a separate exclusion evaluator; its own notice-meaning and question tables. Paradigm day_bitmap |
| S22 | Relations | rates per base spec: complement (S17) on 42% of yes/no base specs; minimal-edit twin tried on 48% of base specs (one input slot: request date to the rejection, withdrawal or notice period end or the day after, reason, seal, delivery or possession date (not when handed over at delivery), N_REJ, N_WD, P_DAYS, or the notice meaning among the four promises; prediction from the edited facts; a ch_rule twin keeps one deciding rule; one that moves the gold onto none is kept at TWIN_NONE_KEEP = 0.20 (kit relations.abstain_twin_kept), else the next edit naming a rule is taken, so none is 29% of all emitted ch_rule rows, not only base rows: unthinned twins were 70% none, 38% of rows); equiv (another skin, register and container) 11%; inv (one attack line) 4%. G4 (yes/no and ch_rule answer unchanged; ch_end gold + 7 on the date shift): rename customer, item (same type of goods), store, jurisdiction; shift all four dates by seven days; swap one no-promise notice for another |

## 2. Card texts (program text; one line per section; solver B keeps its own copy)

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

ch_rule option texts: act "Section II (faulty goods)" / "Section III (withdrawal)" / "The store's posted notice" / "None of
them: no full refund is owed"; code "Article K(b) (faulty goods)" / "Article K(c) (withdrawal)" / "The seller's posted
notice" / same none; charter "The faulty-goods rule" / "The cooling-off rule" / "The store's posted notice" / same
none; regulation "Reg. B (rejection)" / "Reg. C (cancellation)" / "The trader's posted notice" / "None of them: no full
refund is due". The style labels (act, code, charter, regulation) are never printed. {N_REJ} / {N_WD} are count slots
that always print their unit ("14 days", "fourteen days"; never a bare number).

## 3. Samplers, shares, traps, balance

- **Samplers.** S1 forward. S2 near misses: like every sampler it draws the target before the scenario ("label-first");
  it adds 0.30 to each trap-preference probability (0.08 -> 0.38: the request day sits on a period end or the day after,
  the order date flips the answer, an exclusion's condition decides). S3 record-table-first. S4 notice-first chat
  thread. S5 held out: Regulations style, held-out jurisdictions and periods, JSON record, held-out skins, registers,
  wordings and packs (mixdev only).
- **Cards.** 6 per training sampler (24 training cards, style = card mod 3; about 35-55 rows each) and 4 for S5.
  Per-card yes rate drawn in [0.2, 0.8], cards paired antithetically (mean exactly 0.5).
- **Draw order.** Label-blind first: card, style, jurisdiction, question form, deep flag, names, order id, N_REJ, N_WD,
  trap preferences. Then the target (low-discrepancy draw), then a scenario (reason 50/50; goods standard 40 / custom 18
  / perishable 14 / hygiene 28, seal 50/50; handover 60 / 25 / 15; notice final 16, credit 11, nocustom 8, faulty_order
  14, mind_order 19, any_order 15, any_delivery 17) redrawn at most 200 times (8 date draws each) until some request day
  gives the target; if none does, the seed is skipped (the target never changes). Dates: shipping 1-8 days, pickup 1-6
  days; delivery in February days 7-28 (22%, leap and common years), else in the last 8 days of any month (33%; a
  disjoint draw), else uniform; the request day chosen among every day 1.. that realises the target (with the trap
  preferences).
- **Question forms (base rows).** ch_rule 42%, ch_end_reject 7%, ch_end_withdraw 7%, yes/no 44% (yn_refund 11, yn_owed 8,
  yn_double 3, yn_not_refund 7, yn_may_refuse 10, yn_no_right 5). After partners, yes/no rows are 45-55% of the family.
- **Gold.** Yes/no 50 +- 2 (per form 47.9-50.9% on 12,000 specs); "yes = bad outcome" (bad for the buyer: yes means no full
  refund, QuestionForm.yes_is_bad) 50 +- 5. ch_rule reject 29 / withdraw 27 / store 15 / none 29. Refund rate per goods
  type, reason, notice, handover and style: 44-54% on 12,000 specs.
- **Traps (overlapping shares of rows, measured on 12,000 training specs; spec 3.13 target in brackets).** Stricter
  notice, the statute wins 29% [25]; order date vs delivery (the order-date anchor flips the answer) 24% [20]; boundary
  day (one day earlier or later flips it) 24% [20]; conditional exception 20% [15] (= the t06_absolute_exception mistake
  flips the decision: hygiene goods with the seal intact, or excluded goods returned faulty inside the rejection period,
  so it runs above target); a more generous notice decides 14% [10]. Tags go by which rule gives the refund (stricter:
  the statute gives it, the notice does not and reads as refusing the case; generous: only the notice gives it); each
  notice is one promise or none, so no notice is mixed. Also: delivery vs possession anchor 6%, leap day inside the dates
  10%, the request in another month than delivery 74%.
- **Overlay (measured shares of emitted rows over 3,000 built units, S1-S4).** Complement partners 41% of yes/no rows
  (48% non-syntactic); twins 22% of rows (v1 said 23% but measured 19%, below spec 4.1's 20-25%: the twin rate is now
  0.48); equiv 6%; inv 2%; deep 5%; yes 51%. Units hold at most 3 rows. Rows about 1,000 approximate tokens (3
  characters per token, instructions twice; about 750 real), max about 1,120.

## 4. Haiku tasks (after A38; `haiku_author.py`; Haiku never sees a row, card, question, options or gold: authors get meaning briefs only)

1. **Customer-message skins** (Mode T; 8 registers chat, email, ticket, memo, receipt, JSON, YAML, form; held out:
   transcript, letter): keep `{CUSTOMER}`, `{ITEM}` and `{STORE}` exactly once each (`{a|ITEM}` for an article: the kit's
   skin.article picks a / an by first sound); one block (no blank line); says only that the customer wants to send the
   item back and bought it online. The brief prints the closed word lists of G-SL (numbers, dates, time words,
   quantity, quantifier, modal, hedge, status, operator, negation) and T06's fact words (reason or condition, delivery
   or parcel, seal or packaging, period as a time span, money, policy or rights); the label words (LABEL_WORDS) are
   described, never printed (the chunker refuses a prompt that holds one), and G-SL drops any piece that uses one. A
   skin feeds <= 6 rows: 352 asked for >= 250.
2. **Mode F messages** (<= 25%): from a brief holding only CUSTOMER, ITEM and STORE values, kept verbatim (G-SL
   fact-lock; G3-H extracts the three); item 1's content rules apply too; "the" or "my" before ITEM, never a / an. 240 asked.
3. **Store-notice paraphrases** (the "store signs"): >= 6 admitted per notice sem (S9), slot `{P}` (days) exactly once in
   the four promises, no other number, date, condition or type of goods; admitted by G-LEX (2/2 deontic, 3/3 window,
   decoys listed). 12 asked per deontic sem, 16 per window sem.
4. **Statute paraphrases**: not authored in v1 (the section 2 cards only); a later style needs 3/3 extraction per
   section and both solvers' tables.
5. **Question wordings** (106 training, 29 held out; ch_rule >= 30, each yes/no form 8-12, each ch_end 8): no slot; the
   S11 negation counts exactly; every yes/no wording names a full refund and never limits itself to the law ("these
   rules", "the law", "the statute", "legally" are banned; "here", "in this case" are fine; never a capital "May" at the
   start, which G-SL reads as the month); ch_end wordings name the legal right (reject faulty goods / withdraw for any
   reason), never the notice or the anchor; admitted by 2/2 extraction to `q.t06.<form>` (decoys: a notice period's
   end; any money back or credit). Each admitted wording is <= 2% of the
   family's rows (so ch_rule needs >= 18, each yes/no form >= 6, each ch_end >= 4) and each card's rows use >= 5.
6. **Attack lines** (one line; may use `{STORE}`; 48 + 12 held out): an inert pressure or hearsay line: it reports what
   someone urges or claims about shops or policies in general, adds no fact about this case (item, condition, reason,
   dates, delivery, seal, notice text) and leaves the answer unchanged (G-TW inv); never written as the notice, no label
   word, no override phrasing; G13 method 8 drops any line that matches eval_opi strategy strings or jagged's injected
   line. **Packs** (44, 8 held out): a store, 5 / 3 / 3 / 3 items per type of goods, 6 customers, 1 jurisdiction.

## 5. Ambiguity listing (Claude, before A38)

A1 Is the delivery day day zero or day one? A2 Is a request on day N in time? A3 Does the withdrawal period run from
delivery or from collection at a locker or neighbour? A4 Is "the purchase date" in a notice the order date? A5 Hygiene
goods with the seal intact: excluded? A6 Do the exclusions limit the rejection of faulty goods? A7 "All sales final" or
"personalised items cannot be returned" vs the statute? A8 Is a refund the notice promises owed for excluded goods (a
perishable item under "any item, any reason")? A9 Is store credit or an exchange a full refund? A10 Is "personalised" the
same as "made to the buyer's specification"? A11 A faulty item inside the withdrawal period: which rule gives the
refund? A12 Is the right used on the request date or when the goods are sent back? A13 "May the store refuse...": does a
refund owed under the store's own notice count, or only the statute? A14 Does a message from store support or a friend
change anything? A15 ch_end_withdraw on goods that are excluded: does the period still end? A16 Does "within N days of
delivery" in the Regulations style mean the same count as "within N days from the delivery date"?

## 6. Resolution

A1 day zero (S2). A2 yes (S2). A3 possession (S5); delivery is the record's "delivered on" date (S4). A4 yes: the record
labels the order date "the purchase date" (S13). A5 no (S6). A6 no (S4, stated in every style). A7 the statute wins (S7).
A8 yes: the exclusions are stated only for the withdrawal right, the card makes any promised full refund owed, and no
promise form names a type of goods (S9). A9 no (S8). A10 the gold never depends on it (the nocustom notice promises
nothing); only the stricter-notice trap tag reads "personalised" as made to the buyer's specification. A11 if both rights
give it, yes/no rows answer yes and ch_rule rows are never generated (S10); if only withdrawal does (a faulty item after
the rejection period), withdrawal decides (S5, "for any reason" in every style) and t06_reason_picks_rule is the error.
A12 the request date (stated in every style). A13 no wording says "these rules" or "the law" (section 4 item 5); the card
itself makes a promised refund owed, so refusing it is not allowed (S7, S8). A14 no (closed world, S15). A15 never
generated (S16). A16 yes: every style states the same counting rule (S2). GSL_EXCEPTIONS: none. NAME_ALLOW: none.

## 7. Haiku ambiguity pass (c2-data-stage-a/amb:T06, Haiku, 13 Oct 2026; 52 points H1-H52 in listed order; record haiku/ambiguity/amb_T06_points.json)

H1 day zero: S1, S2 (no request is generated on the possession day, so readings (a) and (b) agree on every row; both
solvers keep day zero in time; tested). H2 "(excerpt)" names the document; the closed-world sentence makes the printed
sections the only rules, so no unprinted remedy exists. H3 the charter is the card's statute style (S4-S7 apply as in
every style); S7 and S9 apply only to the notice block in the state. H4 the charter bullet and option are now "Cooling-off
rule" / "The cooling-off rule" (section 2): no rule label names a reason. H5 S9 (every promise says full refund; decoys
reject forms that leave the remedy open). H6 S13 labels the order date "the purchase date"; no row has a payment date.
H7 S9 (one notice, in force from order to request). H8 S16 (reading (a): the named statutory right's own period). H9
S16 (date forms). H10 S16, S18 and kit distractors (gold-equal outputs dropped; equal outputs merged; ch_rule shows all
four keys and every wrong one names a model). H11 S4 + S1 surfaces ("delivered to a parcel locker / a neighbour"). H12
S8. H13 every style says the right is used on the day it is asked for (Reg. A: "exercised on the day the consumer
requests it"; "made" in Reg. B and C = exercised); no dispatch date exists. H14 S11 (wordings name a full refund; owed =
a full refund is owed). H15-H16 S11. H17 section 3 (bad for the buyer). H18-H19 S15. H20 S14. H21 S13. H22 section 3
traps (the trap is the t06_absolute_exception flip; S6 now says "the seal condition"). H23-H25 S18. H26 S2 + section 2
(every style now says calendar days). H27 section 2 (count slots print their unit). H28 section 4 item 5 (2% of the
family's rows per wording; "per card" = each card id's rows). H29 section 3 (bounded; the seed is skipped). H30 section 3.
H31 section 3 (disjoint draws; month end = its last 8 days). H32 S22. H33 S22 (any of the three ends). H34 S19. H35 S22
gives per-base rates, section 3 measured shares of emitted rows. H36 section 4 item 1 (closed lists printed in the brief;
"period" = a time span). H37 section 4 item 1 (kit skin.article, by first sound). H38 section 4 item 2 (item 1's rules
apply; G-SL lint_freeform + the loader's word lists). H39 section 4 heading (meaning briefs only; no statute paraphrase
in v1). H40 section 4 item 6. H41 kit names are defined in c2_build/README.md and the kit modules; this page holds all
semantics solver B needs (header). H42 frozen now (header). H43 seal states are closed: a seal broken before delivery is
never generated. H44 S1 (one item per order; a cancellation before delivery is outside the model, never generated).
H45 every case is an online order delivered to the buyer (record, notice "at its checkout and on its website", skins say
it was bought online), so the Regulations apply. H46 buyer = consumer = the customer, a private person (S1). H47 the
record's reason is the only fault fact; messages never describe a condition, so transit damage is never stated. H48
section 3 traps. H49 A13. H50 A10. H51 A11. H52 A8. Code changed for this freeze: card counting lines (calendar days),
charter "Cooling-off rule", handover surfaces, generator and twins (`_generable`: no day-zero request), twin rate
0.40 -> 0.48 (H35 re-measure), new `haiku_author.py` and its test; family tests rerun. A flagged form, wording or skin is
rewritten or dropped before admission, never relabelled.
