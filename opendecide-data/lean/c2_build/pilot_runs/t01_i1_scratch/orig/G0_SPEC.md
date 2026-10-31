# G0-lite T01: rolling windows and anchored deadlines (absorbs T02 rolling sums and T16 cutoffs)

C2_DATA_SPEC 2.1 (T01, 1,600 selected rows, wave 1, everyday tier) and 3.10; rules for every family in 3.0 and 4.1.
Status: frozen v3 (sha256 in plugin.py G0_SHA256): v2 (c0fadca9...) resolved the Haiku ambiguity pass
c2-data-stage-a/amb:T01 (it read v1, 749c85b4...; H1-H41); v3 adds H42-H47 (section 8). Code: plugin.py (solver A),
solver_b.py (solver B), fixtures.py, haiku_author.py (section 7). DF1-DF14: semantics rows; S1-S6: samplers only (H2).

## 1. Semantics (exact; every rule is printed on the card; DF11 says why the card is closed-world)
| # | Item | Semantics |
|---|---|---|
| DF1 | Kinds | `rolling` (samplers S1, S5), `anchor` (S2, S5), `waiting` (S3), `purchase` and `cash` (S4, 50 / 50), `addon` and `cutoff` (S6, 40 / 60). One kind per card; the card fixes the pack (labels, perils, vendors, office offset and cutoff clock) and the comparator |
| DF2 | Values | Dates: calendar dates in a kit form that is ISO or names the month (2026-03-05, 5 March 2026, March 5, 2026 ...), never numeric d/m/y (H30). Times: fixed-offset datetimes in whole minutes (no zone name, no DST). Amounts: whole-dollar sums held as integer cents, shown in a kit cents form ($4,500.00, 4,500.00 USD, $4,500); no rounding is ever needed (H28). Day counts: count slots (day / days), always calendar days, and every card that counts days says so (H3). Every number, date, name and id is a slot |
| DF3 | Questions | One predicate per kind. Yes/no base forms ask it (polarity +1); complements ask its negation (antonym, implicit or syntactic). Choice forms ask the kind's value: the answer is exactly one printed option (options distinct, one equals the gold; ISO dates, cents and counts are internal keys; H31). Options print counts as "N days", amounts in the cents form of the row's request amount (H29), dates in the row's date form. Yes/no rows never abstain; T01 has no abstain option (gold share 0%) |
| DF4 | rolling | Stays are inclusive of entry and exit (d1..d2 is d2 - d1 + 1 days present). The window is the M days ending on the reference date R: R - (M - 1) .. R, the only window checked (H4); its first day is printed. present = the number of distinct days present inside it (H5). `over` iff present > N, `within` iff present <= N (H8). ch_days = present (H32). Invariants: stays are >= 1 empty day apart (never a shared day) and end on or before R; the printed whole-stay length is never clipped (H6) |
| DF5 | anchor | Two dated events A and B (pack labels); day zero = the later of the two, the earlier plays no part. Final day = later + N (H10). `timely` iff filing <= later + N. ch_deadline = later + N, the last day still in time (H35). Invariant: the filing is on or after the later event (H1) |
| DF6 | waiting | Start = the policy start, or the rider's effective date for a peril added by a rider; one W either way (H15). Start = day zero; waiting days 1..W; final day = start + W (H12). `covered` iff loss - start > W. ch_first_day = start + W + 1, the first covered day (H34). Invariants: one peril per record, the loss's (H14); a rider starts after the policy start; the loss is after the start of its own cover, so "during the waiting period" is the exact complement (H13) |
| DF7 | purchase | Window = the M days ending on the request date Q, both ends included; its first day is printed. total = new request + every earlier purchase dated in [Q - (M - 1), Q - 1]. `quotes` iff total CMP threshold (cmp.gt: >, cmp.ge: >=). ch_total = total, new request included (H33). Invariants: every log line is from the header vendor (H17); no earlier purchase is dated on or after Q (H16) |
| DF8 | cash | Per day, deposits and withdrawals are summed separately (never netted, never mixed across days). `report` iff deposits(D) CMP threshold or withdrawals(D) CMP threshold, for the day under review D (it always has a transaction). ch_cash_which: in / out / both / neither, printed "Only the deposit total" / "Only the withdrawal total" / "Both totals" / "Neither total" (H19) |
| DF9 | addon | Day zero = the notice date (H23). reached = notice + N (+ K if sent by post; hand delivery and email add nothing). A reached day that is a listed closure moves forward one day at a time to the first unlisted day; due = that day. The office is open on every unlisted day. The record prints notice + N, labelled "before any postal add-on or closure" (H24). ch_due = due (H37) |
| DF10 | cutoff | Every response is electronic and arrives when sent (H25). Office time = the offset of the printed cutoff; the due date is an office date (H27). At or before the cutoff clock time of its office-time date: received that day; after it: the next day. `on_time` iff received <= due date (= sent instant <= the cutoff instant on the due date). The record always restates the sending time in office time, in literal square brackets (H26). ch_receipt_day = the counts-as-received day (H36) |
| DF11 | Closed world | Every card ends with "The listed rules and records are complete: no other rule, record or note changes the answer." The DF4-DF7 invariants are facts each record shows, not rules: no row breaks one (a negative printed day count cannot be rendered; solver B refuses the rest), so the sentence is exact (H1). Narrative skins change nothing |
| DF12 | Identity | People, references, labels, perils and vendors are exact strings, distinct within a row. The record's role noun (traveller, party, holder, kept by, teller, notice to) and the card's "person named in the record" name the row's one PERSON (H41) |
| DF13 | Depth | At most 2 unstated operations per row (rolling: clip + count; anchor: pick the later date + compare; waiting: pick the start + compare; purchase: filter + sum / compare; cash: two sums + compare; addon: add-on + roll; cutoff: cutoff + compare). Printed intermediates: stay lengths, window first days, day counts to the filing or loss, the plain N-day date, the office-time restatement. No deep rows (`meta.deep` false on 100%) |
| DF14 | Gold | Solver A (`integer_arithmetic`): proleptic day ordinals, closed-form overlap max(0, min(b, R) - max(a, R - M + 1) + 1), later-anchor ordinals, integer-cent sums, integer office minutes. Solver B (`day_bitmap`): its own parser, then sets of present days built day by day, day lists from day zero, per-day cent ledgers, a calendar walk past closures, epoch minutes. G2 is 100%: an A / B disagreement or a B refusal drops the whole unit and is logged; A never decides alone (H39). A third, construction-only ledger predicts twins and tags traps; it never sets gold |

### 1.1 Cards (program text + CW; solver B full-matches its own copy). Instructions = card + blank line + question
- rolling: "Stay rule: the person named in the record may be present on {WIN_CLAUSE}. Day counts are calendar days, and
  entry and exit days both count as days present. Only one {M_WIN:adj} window is checked: the one that ends on the
  reference date, both ends included; its first day is printed with the record. The person is over the limit if the
  number of days present inside that window is more than {N_MAX}, and within the limit if it is {N_MAX} or fewer."
- anchor: "Filing rule: the {ACTION} must be filed {AN_CLAUSE}: the {EVA_LABEL} and the {EVB_LABEL}. Day zero is the
  later of those two dates, and the earlier date plays no part. Day counts are calendar days, and the final day of the
  period is {N_DAYS} after day zero. A filing made on any day up to and including that final day is in time; a filing
  after it is late."
- waiting: "Cover rule: a loss is covered only after {WAIT_CLAUSE}. That start date is the policy start date or, for a
  peril added by a rider, the rider's effective date; the same waiting period applies either way. Day counts are
  calendar days. The start date itself is day zero, the waiting period begins on the next day, and its final day is
  {W_DAYS} after the start date. A loss that happens after that final day is covered; a loss on or before it is not."
- purchase: "Purchase rule: every purchase in the log is from the vendor the log names. Add up the new request and every
  earlier purchase made inside the {M_WIN:adj} window that ends on the request date; day counts are calendar days, and
  both ends of the window count. If that total is {CMP}, written quotes are required; otherwise the small-purchase path
  applies."
- cash: "Cash rule: for each day, add up that day's cash deposits and, separately, that day's cash withdrawals; never
  net one against the other, and never mix days. A cash report is required for a day if its deposit total or its
  withdrawal total is {CMP}, and not otherwise."
- addon: "Response rule: a response is due {N_DAYS} after the notice date, counted in calendar days with the notice date
  as day zero. If the notice was sent by post, add {K_DAYS} to that date. The date this gives is the day reached. If the
  day reached is a day the office is closed, the due date moves forward to the next day the office is open; otherwise
  the day reached is the due date. The office is open on every day except the listed closures."
- cutoff: "Receipt rule: the office dates every response by office time. Office time is the UTC offset shown with the
  office cutoff, and the due date is a date in office time; the record also gives the sending time in office time, in
  square brackets. Every response here is sent electronically and arrives at the instant it is sent. A response that
  arrives at or before the daily cutoff time counts as received that day; one that arrives after it counts as received
  on the next day. The cutoff is the same office clock time every day. A response is on time if it counts as received on
  or before the due date, and late otherwise."

Clauses: admitted lexicon forms (window, 3/3: win.rolling_cap {N, M:adj}, win.later_anchor {N}, win.wait_after {W};
comparator, 2/2: cmp.gt / cmp.ge {X cents}). Solver B accepts only these sems per kind and checks that {M_WIN}, {N_MAX},
{N_DAYS}, {W_DAYS} outside the clause equal its values.

### 1.2 Record block (state = narrative skin + blank line + block). List style on S1-S4, S6; table style on S5.
| Kind | Lines (program templates; lines marked "yes/no:" only on yes/no cards, which carry the filing or the loss) |
|---|---|
| rolling list | `Stay record {REF} for {PERSON}:` / `- entry day {SI}, exit day {SO} (whole stay: {SD})` per stay / `Reference date: {REF_DATE}` / `Window checked: {WIN_START} to {REF_DATE}, both included.` |
| rolling table | `Travel log {REF}, traveller {PERSON}:` / `\| Entry day \| Exit day \| Whole stay \|` / `\| --- \| --- \| --- \|` / `\| {SI} \| {SO} \| {SD} \|` per stay / the same two closing lines |
| anchor list | `Case {REF}, party {PERSON}:` / `- {EVA_LABEL}: {EVENT_A}` / `- {EVB_LABEL}: {EVENT_B}` / yes/no: `- {ACTION} filed on: {FILED_DATE}`, `- days from the {EVA_LABEL} to the filing: {ELAPSED_A}`, same for B |
| anchor table | `Court notice, case {REF}, party {PERSON}:` / `\| Date \| Event \|` / `\| --- \| --- \|` / `\| {EVENT_A} \| {EVA_LABEL} \|` / B / yes/no: `\| {FILED_DATE} \| {ACTION} filed \|`, `Days from the {EVA_LABEL} to the filing: {ELAPSED_A}. Days from the {EVB_LABEL} to the filing: {ELAPSED_B}.` |
| waiting | `Policy {REF}, holder {PERSON}:` / `- policy start date: {START_DATE}` / `- {PERIL} cover: added by a rider effective {RIDER_DATE}` or `- {PERIL} cover: part of the base policy` / yes/no: `- {PERIL} loss on: {LOSS_DATE}`, `- days from the policy start date to the loss: {EL_START}`, rider rows also `- days from the rider effective date to the loss: {EL_RIDER}` |
| purchase | `Purchase log {REF}, kept by {PERSON}, vendor {VENDOR}:` / `- earlier purchase on {PD}: {PA}` per purchase (date order) / `- new request on {REQ_DATE}: {REQ_AMT}` / `Window checked: {WIN_START} to {REQ_DATE}, both included.` |
| cash | `Cash ledger {REF}, teller {PERSON}:` / `- {TD}: {TT} of {TA}` per transaction (TT = deposit / withdrawal) / `Day under review: {DAY}` |
| addon | `Notice {REF} to {PERSON}:` / `- notice date: {NOTICE_DATE}` / `- sent by: {METHOD}` (post / hand delivery / email) / `- {N_DAYS} after the notice date, before any postal add-on or closure: {BASE_DATE}` / `Office closures: {CL_1}; {CL_2}.` (or `none.`) |
| cutoff | `Notice {REF} to {PERSON}:` / `- response due date: {DUE_DATE}` / `- office cutoff on the due date: {CUTOFF}` / `- response sent: {SENT} [same instant in office time: {SENT_OFFICE}]` (literal brackets, always printed) |

## 2. Samplers (>= 4 training shapes + held-out S5); cards: (sampler, kind, card 0-7) = 56 training cards
| Sampler | Shape | Values |
|---|---|---|
| S1 | rolling, forward to a target count | (N, M) in (90,180) (60,120) (45,90) (30,90) (21,60) (14,30); 1-3 stays (<= 3), straddle 45% (80% on ch_days), an early stay 35-50% |
| S2 | anchor, label-first (target day count from the later event) | N in 10-90; events 1-45 days apart (wider to set the earlier-anchor trap); later event A or B 50 / 50 |
| S3 | waiting, label-first | W in 7-90; rider 50% (effective 10-209 days after the start) |
| S4 | purchase ledger / cash ledger, label-first totals | windows 30-120; thresholds $3,000-$25,000; cmp.ge on 1 card in 4 |
| S6 | addon (closure list) / cutoff (offset conversion) | N 10-30, K 2 / 3 / 5; 0-3 closures; office offsets -05:00 .. +09:00, cutoffs 12:00-23:30 |
| S5 | held out (mixdev only): table style, rolling (75,150) (40,100) or anchor N 20 / 35, held-out skins and registers | never a training row |

## 3. Traps (tags in `meta.edge`; measured on 2,400 specs; the tests assert floors on 2,004; overlapping)
| Tag | Measured | Construction |
|---|---|---|
| `boundary` | 32% of rows | target exactly at the edge: present N / N+1, day count N / N+1 or W / W+1, total at threshold +- $1, cutoff +- 0-5 minutes |
| `straddle`, `pre_window_stay`, `window_edge`, `calendar_trap` | rolling 65 / 33 / 13 / 39% | a stay crossing the window's first day; a stay wholly before it (or ending the day before); the calendar-year count gives the other verdict |
| `earlier_trap` | 43% of anchor yes/no rows | in time from the later date, late from the earlier one |
| `rider_trap` | 16% of waiting rows | inside the rider's waiting period, outside the policy's |
| `window_edge`, `request_alone_trap`, `ignore_window_trap` | purchase 53 / 50 / 33% | a purchase on the window's first day or the day before; the request alone or every purchase gives the other verdict |
| `netting_trap`, `other_day_trap` | cash 53 / 46% | netting, or adding other days, changes the label |
| `closure_roll`, `double_roll`, `post_addon` | addon 49 / 16 / 52% | the reached day is a closure; two closures in a row; postal add-on |
| `conversion_trap`, `date_crosses`, `evening_before` | cutoff 21 / 26 / 5% | the wall clock read as office time flips the verdict; the office date differs from the sender's; after the cutoff on the eve of the due date (still in time) |

## 4. Balance targets (generator level; c2_select tightens to the spec 3.0 cells)
- Yes/no: 43% of bases (cutoff 72%, addon 0%); 45-55% of family rows with relations (measured 50%). Gold yes 50% on
  every yes/no base form, exact over seed pairs (label-first target bit; complements mirror it).
- Gold shares: ch_cash_which in 30%, out 30%, both 15%, neither 25%; ch_receipt_day after the daily cutoff 50%.
- Gold position uniform per option count; on ORDERED open sets (dates, counts, cents) the gold's sorted rank is the
  kit's label-blind target_rank(row key, k), so "take the middle option" scores chance (k = 3 or 4 drawn label-blind,
  sized by ordered_k: k = 2 on 20% of ch_days, 100% of ch_receipt_day, 54% of ch_total; drops <= 0.2%). ch_total never
  shows t01_request_only with t01_prior_only (their sum is the gold).
- yes = bad: yn_over, yn_late, yn_fail_time, yn_not_timely, yn_in_waiting, yn_not_covered, yn_quotes, yn_cash_report,
  yn_late_cut, yn_not_on_time. Complements are proposed on 70% of good-outcome and 30% of bad-outcome bases (50 +- 5).
  Length: real-token mean (instructions twice) 435, max 554 with stand-in skins (cap 2,000; family mean <= 800).

## 5. Error models (every wrong option is the output of one; family names carry the prefix `t01_`)
ch_days: `calendar_year`, `t01_whole_stays`, `t01_straddle_dropped`, `t01_straddle_full`, `drop_inclusive_endpoint`
(exit days not counted), `t01_window_one_long` / `_short`, `t01_exit_extra_day`. ch_deadline: `earlier_anchor`,
`count_day0` (later + N - 1), `off_by_one_late` (+ N + 1), `t01_both_ends_early` / `_late` (+ N -+ 2),
`t01_business_days` (N weekdays). ch_first_day: `count_day0` (start + W), `off_by_one_late` (start + W + 2),
`wrong_anchor` (policy start on rider rows), `t01_both_ends_early` / `_late`, `t01_business_days`. ch_total:
`t01_request_only`, `t01_prior_only` (never together), `t01_ignore_window`, `drop_inclusive_endpoint`,
`add_exclusive_endpoint`, `t01_double_request`, `t01_last_prior_only`. ch_cash_which: `netting`, `t01_sum_across_days`,
`more_than_as_at_least`, `at_least_as_more_than`. ch_due: `t01_skip_addon`, `t01_addon_not_post`, `t01_ignore_closure`,
`wrong_roll_direction`, `count_day0`, `off_by_one_late`, `t01_both_ends_early` / `_late`, `t01_business_days`.
ch_receipt_day: `t01_ignore_cutoff`, `skip_offset_conversion`, `off_by_one_late`, `t01_due_date_read`,
`drop_inclusive_endpoint`, `t01_always_next_day`, `t01_sender_date`, `t01_utc_date`, `t01_early_previous_day`. The
day-count models are misreadings the printed card text rules out (H3, H10, H12).

## 6. Relations (spec 4.1; G-TW 100%)
- Complement on 70% (good-outcome base) or 30% (bad-outcome base) of yes/no bases: yn_over -> within (antonym 60%) /
  not_over (syntactic 40%); yn_timely -> late (antonym) / fail_time (implicit "fail to") / not_timely (syntactic);
  yn_covered -> in_waiting (antonym) / not_covered; yn_quotes -> quotes_without (implicit) / no_quotes; yn_cash_report
  -> cash_without (implicit) / cash_no_report; yn_on_time -> late_cut (antonym) / not_on_time. Measured: complements on
  52% of yes/no rows, non-syntactic 57-61% of pairs.
- Minimal-edit twin (proposed on 42% of bases; measured 24% of rows): one input slot moves and the prediction comes from
  the ledger and the move, never from solver A: rolling the last stay's exit (present to N / N+1, or +- 1-3 on ch_days);
  anchor the filing date (to day N / N+1) or N (to e or e - 1, where e = filing - later, H40; ch_deadline N +- 1-5);
  waiting the loss date (to day W / W+1) or W (to e or e - 1, e = loss - start; ch_first_day W +- 1-5); purchase the
  request amount (to the threshold edge) or one earlier purchase across the window's first day (keeping date order);
  cash one same-day amount (to the edge); addon the sending method; cutoff the sending time (across the cutoff by 0-5
  minutes). Derived lines move with their input.
- equiv on 12% of bases (another skin and register); no attack twins (agent tier only). G4 (checked, never emitted;
  answer the same unless said): rename the person or the peril; shift every date and time by 7 days (date answers +7);
  add a stay or purchase before the window, a large deposit on another day or a closure after the due date; swap the two
  events; rewrite the sending time in another offset.

## 7. What Haiku writes (after A38; haiku_author.py builds the tasks, <= 40 chunks; never a question, option or gold)
- Packs (80, of which 16 held out for the 16 S5 cards): an everyday setting with 6 people (first + last name), one topic
  per kind (rolling, anchor, waiting, purchase, cash, notice), a filing noun with two event labels ending in "date", 3
  perils, 3 invented vendors. One pack per card; the program expands them.
- Narrative skins (Mode T): 56 per training register (memo, email, chat, ticket, json, yaml, log, transcript) and 28 per
  held-out register (faq, letter; S5 only). Slots PERSON (name), REF (id), TOPIC (name), each exactly once; they say who
  sent which file about what, in neutral words that fit every kind; never a date, number, rule, record, question,
  outcome, deadline, limit, window, cutoff, office or day type (G-SL plus the loader's T01 list; H38).
- Mode F (<= 25%): 120 short documents (memo, email, chat, ticket, transcript) from a facts-only brief (PERSON, REF,
  TOPIC verbatim; TOPIC after "the"); G-SL lint_freeform, then G3-H.
- Question wordings (287 asked; >= 30 admitted, each <= 2% of rows): 12 per yes/no base form, 14 per choice form, 9 per
  complement form; lexicon kind `question`, sem q.t01.<qform>, 2/2. Slots: PERSON, REF and the kind's own (REF_DATE
  rolling, ACTION anchor, PERIL waiting, DAY cash), each at most once. Negation exact (negcount k_all, k_syn): (0, 0) on
  bases, antonyms and choice forms, (1, 0) on implicit forms (fail to, without), (1, 1) on syntactic forms. No
  relative-time or day-type word (today, now, this week, recently, weekday, working / business day; H38), no label-check
  form, "the office" only on addon / cutoff forms; briefs fix the section 8 meanings.
- Rule paraphrases, no negation word in any: kind `window` (3/3 to the same sem; 14 per sem) for win.rolling_cap {N,
  M:adj} (a rolling period, never a calendar year), win.later_anchor {N} (names the later of the two dates and reads
  before ": the X and the Y"; H9), win.wait_after {W} (the waiting period starts the day after its start date; ends with
  "its start date"); kind `comparator` (2/2; 12 per sem) for cmp.gt / cmp.ge {X}: plain about a total of exactly X; bare
  over / above / exceeds / in excess of are never admitted (H18).
- Program-written record lines; no attack lines (everyday tier); no held-out wordings (S5 is held out by sampler, packs,
  skins and registers). G-SL exceptions: none; clause slots: H43; the redo2 round: H42-H47.

## 8. Resolution of the Haiku pass (amb:T01; H<n> in the order raised; no gate bar loosened; (x) = reading kept)
H1 unprinted invariants: record facts (DF4-DF7, DF11); a breaking row cannot be rendered (negative day count) or B
refuses it (a). H2 DF rows vs samplers. H3 printed "Day counts are calendar days" on every day-counting card (a). H4
printed "Only one M-day window is checked: the one that ends on the reference date" (a). H5 shared day: never built
(stays >= 1 empty day apart; B refuses one); the card counts "the number of days present" (a). H6 stay length: the
record prints "whole stay" (full length); the reader clips it (a). H7 exit: "entry day" / "exit day", and the card says
both count (a). H8 within: printed "within the limit if it is N or fewer" (a). H9 anchor: printed "Day zero is the later
of those two dates, and the earlier date plays no part" whatever the clause; win.later_anchor paraphrases must still
name the later date (3/3) (a). H10 final day: printed "N after day zero" (a). H11 fail to file: every yes/no anchor row
prints a filing; yn_fail_time = filed after the final day (a). H12 waiting: printed "the start date itself is day zero,
the waiting period begins on the next day, and its final day is W after the start date" (a). H13 rider loss: always
after the start of its own cover (DF6) (a). H14 one peril per record (a). H15 printed "the same waiting period applies
either way" (a). H16 same-day purchase: never built, B refuses (DF7). H17 printed "every purchase in the log is from the
vendor the log names" (a). H18 comparators: equality must be plain; more / greater than = gt, at least / or more / or
above = ge (a; fixtures follow). H19 cash options renamed (DF8): "Only the deposit total" = only that total meets the
test (a); "Neither total" = neither meets it (a). H20 / H21 cash_without, quotes_without: requirement questions, "does
the rule let ... without" (a). H22 late_cut: late = counts as received after the due date (card); wordings never mention
the clock (a). H23 addon: printed "with the notice date as day zero" (a). H24 BASE line: "before any postal add-on or
closure"; the day reached = that date + K for post, then closures (a). H25 printed "Every response here is sent
electronically" (a). H26 brackets: literal, always printed, named on the card (a); section 1.2 marks optional lines
"yes/no:". H27 printed "the due date is a date in office time" (a). H28 whole dollars (a). H29 options use the request
amount's cents form, never raw cents (b). H30 no numeric dates. H31 one printed option, exactly one correct (b). H32-H37
choice wordings (briefs, G-LEX meanings): days present inside the checked window; the compared total, new request
included; the first covered date; the last date still in time; the counts-as-received date; the due date under the
response rule (a). H38: section 7 bans. H39 A / B disagreement: unit dropped (b). H40 e: section 6. H41 one PERSON per
row; the card says "the person named in the record" (a). v3 (T01 lead, after the extraction round; no gate bar, gold,
card text or G-LEX meaning text changed): H42 G-LEX collisions (late / fail_time / not_timely, within / not_over,
in_waiting / not_covered, quotes_without / no_quotes, cash_without / cash_no_report, late_cut / not_on_time) are one
proposition each by design; exact negcount fixes the construction, and a collision can only reject. Rejected forms stay
out (no re-vote); meaning texts stay (a new text voids every recorded read); section 7 per-form counts are asked counts
(floor >= 30 admitted). H43 window and comparator clauses are clause slots in the program card: G-SL role program (each
slot once; check_row never lints clause text); G-LEX and check_lexicon gate their words; wording-role hits ("later" H9,
"next" H12, a word after {N}) are logged flags. H44 briefs say "final" or "latest", never "last". H45 confirmation
reads glex-r1b, -r2b (admitted forms) and -r3b (window) fill realistic values (pack values, kind refs, card ranges); a
form is used only when all its reads, old and new, pick its sem; new forms get the same reads. H46 pack redo: taken
names listed, initials A-L / M-Z per chunk, full word bans; one pack per card. H47 documents: one g3h-r1 read; admitted
iff g3h.compare matches person, ref and topic (a mismatch drops it).
