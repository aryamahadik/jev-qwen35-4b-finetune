# G0-lite T12: three-way match with ordered exception precedence (release / hold / review / reject / escalate)

One page (C2_DATA_SPEC 3.15, 3.0, 4, 6.2 item 3; PREREG A37, A38). **v2.1, FROZEN 13 Oct 2026**: v2 after the one
Haiku ambiguity pass (`c2-data-stage-a/amb:T12`, 30 points H1-H30, resolved in section 5; record
`haiku/ambiguity/amb_T12.json`); v2.1 changes section 2 only (count-percent comparator forms; no semantics
change). The sha256 of this file is `T12Plugin.G0_SHA256` and the pass id `G0_HAIKU_TASK`; validate_plugin() refuses
the plugin if this file changes. Plugin `plugin.py` (solver A: rules.RuleSet first_match over a Decimal rule AST,
paradigm rule_engine); `solver_b.py` (its own parser + sqlite tables joined by line, integer cents, paradigm
sql_sqlite) is written from this page only; `authoring.py` (Haiku authoring tasks and their checks).
**Labels on this page:** R1-R27 are the semantics items below; S1-S5 always mean the samplers (R21); A1-A17 the
first listing; H1-H30 the Haiku pass. A "row" is one generated example (one invoice bundle + one question); a "line"
is one numbered line of a document; a "block" is one blank-line-separated part of the state; a "container" is the
document format (kv, table, CSV, JSON). "Label-blind" always means drawn from the row key, never from the gold.

## 1. Semantics table

| # | Item | Semantics (exact) |
|---|---|---|
| R1 | Documents | purchase order: PO_ID (id), VENDOR (name), n = 1-4 lines, each ITEM (name: no digit, comma, semicolon or pipe; distinct in a row), ordered quantity PO_Q (count 2-200, unit from the closed list bag box bottle carton case crate drum kit pack pallet ream roll set spool tube unit), PO unit price PO_P (integer cents > 0, drawn in the pack item's band, 200-100,000 cents). Goods receipt, exactly one per PO: GR_ID, PO_ID, GR_DATE, per line received RCV_Q = PO_Q - shortfall, shortfall 0-3 clamped to PO_Q - 1 (so RCV_Q >= 1). Invoice: INVOICE_ID, VENDOR, PO_ID, INV_DATE, per line INV_Q (1..PO_Q + 3) and INV_P = PO_P + D (cents > 0). INV_Q > PO_Q is generated only where RCV_Q = PO_Q; RCV_Q < INV_Q <= PO_Q also occurs (1.7% of rows) and fails (R4). Identity holds by construction and is not a check: the three documents name one PO_ID, the PO and the invoice one VENDOR, and every document lists the same line numbers, items and units (solver B refuses a row where they differ). Paid-invoice register REG_1..REG_m (m 2-4 invoice numbers, nothing else, same vendor) shown iff the duplicate check is on the card. Dates are narrative: no rule reads them |
| R2 | Printed intermediates | PO line total PO_LT = PO_Q x PO_P; PO_TOTAL = their sum; INV_LT = INV_Q x INV_P; INV_TOTAL = their sum. Unit prices and every total are always printed; no tax, no freight. Solver B re-derives and checks every printed total |
| R3 | Money | one currency per row from the closed set USD $ / EUR € / GBP £. The card's Amounts line names the ISO code; amounts on the card (TOL_AMT, LIMIT) and in kv / table documents print with the symbol ($12.50) or the code (12.50 USD), one seeded form order per row (with the symbol, a whole amount may drop its cents: $44); CSV prints decimal currency units with no sign (1234.50); JSON prints integer cents in keys ending in _cents. TOL_AMT, LIMIT and every amount are in the row's currency; every amount is integer cents |
| R4 | Quantity check (qty; always on the card) | passes iff INV_Q <= RCV_Q on every line. The received quantity of the one receipt is the base, never the ordered one, and register entries never change it. A shortfall billed at or below what was received passes; "over-billed" on this page means billed above the received quantity, also when INV_Q <= PO_Q (PO 10, received 8, invoiced 9 fails). Fails: hold (option "Hold for receipt") |
| R5 | Price check (price; always on the card) | per line D = INV_P - PO_P (cents, may be < 0). Percent cards (50%): T = PCT x PO_P / 100 per line, PCT from {1, 3, 5} on S1-S4 and {2, 4} on S5 only (held out); every PO_P of a percent card is a multiple of 100 / gcd(PCT, 100), so T is whole cents on every line. Absolute cards (50%): T = TOL_AMT, an amount per unit of price compared with D directly on every line, never multiplied by a quantity; TOL_AMT from {5, 10, 15, 20, 25, 50, 75, 100, 150, 200, 250, 500} cents on S1-S4 and {30, 40, 60, 120, 300} on S5 only, drawn among the listed values within 0.8-4% of the row's cheapest PO_P (the lowest PO unit price of its lines); a soft window: if none fits (0.2% of absolute cards), the listed value nearest 2% of it. D lies within about +-5% of PO_P (about +-10% on a compensated totals-match line). Comparator TOL_CMP: cmp.le passes iff D <= T; cmp.lt iff D < T. One-sided: the condition bounds the difference from above only, so every D <= 0 passes (the card adds "Lower invoiced prices always pass"). The check passes iff every line passes. The base is the PO unit price, never the invoice price or a line total. Fails: review ("Send to price-variance review") |
| R6 | Duplicate check (dup; on 50% of rows) | passes iff INVOICE_ID equals no register entry, character for character. A look-alike (one changed digit or one adjacent swap) is another number. Fails: reject ("Reject as a duplicate") |
| R7 | Approval-limit check (limit; on 50% of rows) | INV_TOTAL against LIMIT (cents, the row's currency) with LIMIT_CMP: cmp.le passes iff INV_TOTAL <= LIMIT; cmp.lt iff INV_TOTAL < LIMIT. The PO total is never compared. LIMIT: one of the three nearest values of {250, 500, 1,000, 2,000, 2,500, 5,000, 10,000, 25,000, 50,000} currency units above (passing) or below (failing) INV_TOTAL, or INV_TOTAL plus or minus a seeded gap; under the boundary plan exactly at the boundary. APPROVER (name) is narrative. Fails: escalate ("Route to a senior approver") |
| R8 | Checks, order, display | qty + price + dup? + limit?: 2-4 checks; dup and limit are each on the card on 50% of rows (independent seeded draws per row). The check order is a uniform seeded permutation of the row's checks, drawn independently of the target action; the card prints it on its "Check order:" line, and it is the only decision order (R9). The listed order is the top-to-bottom order of the check lines or table rows. Display: samplers S1, S4, S5 a numbered list in the check order 60%, a bulleted list in a seeded order 40%; S2 numbered 40%, bulleted 60%; S3 always a table, rows in the check order ("aligned") 60%, in a seeded order 40%. A seeded order is a uniform permutation and may equal the check order. List numbers are check-order ranks (solver B refuses a numbered list in another order). Because ch_action draws its action uniformly first, the deciding check's position is uniform on ch_action rows by construction (no rejection; measured k = 3: 118 / 113 / 118); on yes/no rows it follows the target draw |
| R9 | Precedence ({PREC}: one admitted form of sem prec.t12.first_failing, 3/3; it names "the check order") | the first check in the check order (the "Check order:" line) that fails decides the action; later checks and the listed order do not change it. If every check passes: release ("Release for payment"), the only action that pays. Exactly one action per invoice |
| R10 | Action keys | the card's closed set: release + one action per check on the card (3-5 options) |
| R11 | Answer codes | row-level: about 12% of ch_action rows (a seeded draw per row) add the card line "Answer codes: Heron = release for payment, Kestrel = hold for receipt, ..." with code words from the program's closed list Heron, Kestrel, Marlin, Osprey, Plover (never an action word, never in NAME_ALLOW), one per card action; the options are the codes and the gold is a code. The question is an ordinary ch_action wording, which names no action. No other row carries the line |
| R12 | Card text (program) | "AP policy of {ORG}: match the invoice to its purchase order (PO) and goods receipt; it gets exactly one action." / "Checks:" / per check, in the listed order, "{1.\|-} {Quantity\|Price\|Duplicate\|Approval-limit} check: {cond}. If it fails: {hold for receipt\|price-variance review\|reject as a duplicate\|route to a senior approver}." (S3: table "\| check \| passes when \| if it fails \|") / "Check order: {ORDER}." where ORDER is the row's check names (quantity, price, duplicate, approval limit) in the check order joined by ", then " (e.g. "Check order: price, then quantity, then approval limit.") / {PREC} / "If every check passes: release for payment, the only action that pays. Lower invoiced prices always pass." / "Amounts: {CURRENCY code}, whole cents; line total = quantity times unit price; document total = sum of line totals." / [answer codes] / "Nothing else applies: the policy and the documents shown are complete." (closed world). Then a blank line and the question |
| R13 | Conditions (program) | qty "the invoiced quantity is at most the received quantity on every line"; price "invoiced unit price minus PO unit price is {TOL_CMP}[ of the PO unit price] on every line" (TOL_CMP bound to TOL_PCT, e.g. "3 percent", or to TOL_AMT, e.g. "$0.50"); dup "the invoice number is not in the paid-invoice register (exact match only)"; limit "the invoice total is {LIMIT_CMP} (limit of approver {APPROVER})" |
| R14 | State blocks (program, blank-line separated) | the narrative skin; PO, goods receipt, invoice and register, all in one container per row: key-value ("- line 1: item; 40 cases at $12.50; line total $500.00"), markdown table, CSV export (iso dates, amounts as 1234.50) or JSON (integer cents). Order: S1 / S2 / S5 narrative, PO, GR, invoice, register; S3 documents first, narrative last; S4 narrative, invoice, register, PO, GR. A pressure line (inv twins) is the last block and carries no fact. The narrative is one block that never starts with "Invoice", "Purchase order", "Goods receipt" or "Paid-invoice"; a json / yaml / log narrative is the narrative written as a small JSON object / YAML mapping / log line holding only narrative slots, never a document (document blocks are program text with their own heads, e.g. "Invoice (JSON):") |
| R15 | ch_action | gold = the R9 action; options = the card's actions (closed set, seeded order); gold uniform over the card's actions. Wrong options carry the error models that produce them (34% of wrong options; the rest are closed-set members) |
| R16 | ch_price_line | "which line, if any, fails the price check": options = every line's item + "None of the lines"; gold = the one failing line (75%) or none (25%). This form is never generated with two failing price lines (unrelated to the two_fail tag) |
| R17 | Predicate released | yes iff action = release: yn_release, yn_dneg_release ("Is it not true that ... is not released ...", k_syn 2). yes iff action != release: yn_not_release (syntactic, k_syn 1), yn_payment_stopped (antonym), yn_exception_route (option framing: "a hold, a review, a rejection or a routing to a senior approver"; complement-only, base share 0) |
| R18 | Predicate price_ok | the price check taken on its own, exactly as the card states it (its comparator decides a line at exactly T), whatever the order decides: yn_within_tol yes iff it passes; yn_over_tol (antonym) yes iff it fails. Wordings say "pass / fail the price check" and never "within", "tolerance" or "variance" |
| R19 | yn_price_review | yes iff action = review (an earlier failing check makes it no) |
| R20 | Shares (base rows) | ch_action 48, ch_price_line 10, yn_release 11, yn_dneg_release 3, yn_payment_stopped 5, yn_not_release 3, yn_within_tol 7, yn_over_tol 4, yn_price_review 9 (%; a golden-ratio sequence over seeds). A card is one sampler's card c of 16 (10 on S5): pack, tolerance kind, document container, block order; checks, order and comparators vary per row. The card's rate r = 0.2 + 0.6 (rank + 0.5) / 16 for the card's seeded rank (spread evenly over 20-80%, family mean exactly 50%); a yes/no row on the card is gold yes with probability r. Complement on 60% of released-predicate bases (yn_release -> not_release 30 / payment_stopped 35 / exception_route 35; dneg -> not_release; payment_stopped -> release; not_release -> release or dneg) and 50% of price_ok bases. No abstain option (gold share 0) |
| R21 | Samplers | S1 forward (kv / table); S2 label-first near-miss (boundary plan 65%, look-alike register 70%, shuffled display 60%); S3 ERP-export-first (CSV / JSON, policy table, json / log / yaml skins); S4 vendor-thread-first (kv, chat / email / transcript skins); S5 held out (portal / voicemail skins, held-out wordings, PCT {2, 4}, TOL_AMT {30, 40, 60, 120, 300}; mixdev only). The boundary plan (label-blind) puts the deciding values at or one step past a boundary: INV_Q = RCV_Q + 1, D = the largest passing or the smallest failing difference, LIMIT at INV_TOTAL or one cent away |
| R22 | Traps (tags; spec target; measured on 2,000 training specs) | totals_match_lines_differ 25% / 25.3% (label-blind plan: every PO quantity billed, any price move compensated on a second line); two_fail (two or more checks fail) 20% / 18.2% (label-blind plan); at_tolerance 20% / 24.5% (a line exactly at T: passes under cmp.le, fails under cmp.lt). Reported: wrong_base_trap 35.5%, display_order_trap 4.4%, line_by_line_trap 7.9%, totals_trap 24.3%, salience_trap 9.1%, near_miss_duplicate 22.0%, shortfall_billed_ok 47.2%, price_below_po 43.1%, qty_boundary 16.9%, limit_at_boundary 8.8% |
| R23 | Error models (each = the card with one stated mistake; options only) | first_failure_only: the first failing check in the listed order (only where it differs from the check order); t12_reverse_order: the last failing check in the check order; t12_price_first: review whenever the price check fails; t12_totals_only: release iff INV_TOTAL = PO_TOTAL (no option otherwise); t12_ordered_not_received: qty against PO_Q; t12_invoice_price_base: PCT of INV_P (percent cards); t12_line_total_base: the bound on line amounts (100 x INV_Q x D vs PCT x PO_Q x PO_P; INV_Q x D vs TOL_AMT); t12_two_sided_tolerance: \|D\| vs T; t12_near_miss_duplicate: a look-alike counts; t12_limit_on_po_total: PO_TOTAL vs LIMIT; t12_line_by_line: lines in number order, on each line qty and price in the check order, the first problem decides, then dup and limit in the check order; drop_inclusive_endpoint: every cmp.le read as cmp.lt; add_exclusive_endpoint: every cmp.lt read as cmp.le |
| R24 | Relations | complement (R20; same call_id). Minimal-edit twin (own call_id, drawn on 42% of base specs): one input slot crosses one check's boundary, fixed by the comparator and the base side. qty, one failing line: RCV_Q := INV_Q (the rest arrives), or, if INV_Q > PO_Q, INV_Q := RCV_Q; qty passing: on a line with PO_Q - (INV_Q - 1) <= 3, RCV_Q := INV_Q - 1. price, one failing line: INV_P := PO_P + T (cmp.le) or PO_P + T - 1 (cmp.lt), the largest passing price; price passing: on a line, INV_P := PO_P + T + 1 (cmp.le) or PO_P + T (cmp.lt), the smallest failing price. dup failing: the matching entry := a look-alike; passing: one seeded entry := INVOICE_ID. limit failing: LIMIT := INV_TOTAL (cmp.le) or INV_TOTAL + 1 (cmp.lt); passing: LIMIT := INV_TOTAL - 1 (cmp.le) or INV_TOTAL (cmp.lt). The answer is predicted from the base truths with that one check flipped; the generator recomputes every check of the twin and drops a candidate that moves another check (an INV_P edit that moves INV_TOTAL across LIMIT) or leaves the answer unchanged; G-TW re-checks. equiv drawn on 11% of base specs (another skin; on half also kv <-> table or csv <-> json); inv on 6% (one pressure line). G4: rename the vendor, rename the buyer, reverse the line order (lines renumbered in printed order in all three documents at once, so the join by number holds), shift both dates by 7 days ("same"), reverse the check order (the "Check order:" line and a numbered list are regenerated; predicted from the base truths) |
| R25 | Depth | unstated operations = values a reader must compute that are not printed, counted once per kind: the per-line difference D against its bound (1) and, on percent cards, the bound PCT% of PO_P (1). Comparing values and walking the checks in the check order apply the rule and are not operations; totals and line totals are printed. Depth 1 (absolute) or 2 (percent), never deep |
| R26 | Solvers | A: rules.RuleSet(first_match, default release) whose rules are "check fails" ASTs in the check order, on Decimal amounts (t12_pct_of, t12_line_amount). B: sqlite tables po / gr / inv / reg / policy joined by line number; with the card's TOL_CMP and LIMIT_CMP as parsed through the admitted lexicon: a line fails price iff 100 x (inv - po) > PCT x po (cmp.le) or >= (cmp.lt), or inv - po > T / >= T, in integer cents with no division; qty = JOIN where inv.qty > gr.qty; dup = COUNT in reg; limit fails iff SUM(qty x cents) > LIMIT (cmp.le) or >= (cmp.lt); the first failing check by policy rank; its own answer table |
| R27 | Length | every row <= 2,000 approx tokens (kit: 3 chars / token, instructions twice); measured mean 1,010, max 1,516 |

**Balance (measured on training relation units, 300 seeds x S1-S4, 2,132 rows).** yes/no 47.0% of rows; gold yes
49.8%; yes = bad 52.4% (share of yes/no rows whose form reports a bad outcome by yes: yn_not_release,
yn_payment_stopped, yn_exception_route, yn_over_tol, yn_price_review; spec 3.0: 50 +- 5); k_syn >= 1 on 16.9% and
>= 2 on 7.1% of yes/no rows; complements 44.7% of yes/no rows, 71% non-syntactic; final-row shares (R24 gives draw
rates per base spec): twins 23.6%, equiv 6.2%, inv 3.4%; rows per call_id <= 3 (a twin has its own call_id).
ch_action gold within 4 pp of uniform over each card's actions; gold position uniform per option count.
Visible-feature cues: P(totals equal | action) 0.32-0.38 for every action; P(any receipt shortfall) 0.52-0.64 off hold
vs 0.89 on hold; P(any price increase) 0.63-0.75 off review vs 1.0 on review (inherent: a failing check needs its
feature; mitigated by billed-correctly shortfalls, over-billing and within-bound increases). Wording negation counts
(k_all / k_syn): 0 / 0, except yn_not_release 1 / 1 and yn_dneg_release 2 / 2.

## 2. Haiku tasks (after A38 only) and the slots they must keep (24 tasks in `haiku/author/TASKS.json`; checks in
`authoring.py`, run by the lint stage before G-LEX extraction)

- Packs (2 tasks x 25): buyer, currency, document prefixes, 3 vendors, 6 items (unit from the R1 list, PO unit-price
  band lo-hi cents, 200 <= lo < hi <= min(4 lo, 100,000)), 3 AP clerks, 2 approvers; >= 25 kept, one per card.
- Narrative skins (Mode T; registers memo, email, chat, ticket, json, log, transcript, yaml; held out portal,
  voicemail; one task each): CLERK (name) and DEPT (category) exactly once; VENDOR, INVOICE_ID or PO_ID at most once
  each; one block, no blank line; outside slots none of the closed G-SL word lists (kit gsl CORE + EXTENDED: digits,
  number words and ordinals, dates, relative time, quantity, quantifier, modal, hedge, status, operator words,
  negcount negation cues), no capitalised name, no LABEL_WORDS form and no action verb (pay, stop, look over, refuse,
  send up, sign off ...); never opening with "Invoice", "Purchase order", "Goods receipt" or "Paid-invoice".
- Free-form narratives (Mode F, <= 25% of rows; 2 training tasks + 1 held out): from a brief with CLERK and DEPT
  values only, each kept verbatim (never a part of the name); the same word rules; G-SL fact-lock + G3-H.
- Question wordings (lexicon kind question, slot INVOICE_ID, 2/2 extraction, the negation counts above; >= 30 per
  family, each <= 2% of the family's rows; 5 training tasks + 1 held-out task for S5).
- Comparator paraphrases (cmp.le / cmp.lt, bound typed count-percent or cents; 2/2): the endpoint is said plainly
  ("at most X", "X or less", "no more than X", "less than X", "below X", "strictly less than X"). Forms with
  "within", "under", "over", "beyond", "exceed", bare "up to", "limit", "maximum" or "minimum" are dropped before
  extraction (readers split on the endpoint). The pool covers all four (sem, bound) pairs (percent cards, R5 and R13,
  need admitted count-percent forms of cmp.le and cmp.lt; the plugin refuses a card without one). The lexicon holds
  one slot kind per text, so a count-percent form repeats no other form's text: it names the part of the PO unit
  price with one of the nouns share, fraction, portion or proportion, joined to a comparison word ("a share of X"
  states no endpoint and is dropped), and never writes "percent" (the bound prints it). These forms come from their
  own task (`haiku/redo2`; same rules, lint, dedup and 2/2), and every count-percent form's two G-LEX reads show a
  percent bound ("3 percent"), the already admitted one too (more reads can only reject it).
- Precedence paraphrases (sem prec.t12.first_failing, 3/3; decoys last_failing, most_severe, first_listed): one line
  that names "the check order"; never "listed", "list", "above", "top", "highest", "severe", "serious", "priority".
- Pressure lines (attack kind; {VENDOR} at most once; no fact, number, name or action word).
Haiku never sees the policy, the documents, the question, options or gold; a Haiku answer never sets a label.

## 3. Ambiguity listing (first listing; the Haiku pass is section 5)

A1 "is at most 2 percent of the PO unit price" when D is exactly 2%? A2 "below $0.50" at exactly $0.50? A3 is the
percent taken of the PO price, the invoice price or the line total? A4 does an invoiced price far below the PO price
fail? A5 a receipt shortfall when the invoice bills only what was received? A6 is the ordered or the received
quantity the base? A7 two checks fail: the first listed, the first in the check order, or the most serious? A8 "Does
the policy send X to price-variance review?" when an earlier check fails first? A9 "Taken on its own, does X pass the
price check?" when an earlier check already decides? A10 does a look-alike register number (INV-55128 vs INV-55182)
count as a duplicate? A11 does the limit compare the invoice or the PO total, and is "$5,000.00 or less" met at
$5,000.00? A12 do equal invoice and PO totals mean the invoice matches? A13 do the dates matter? A14 does "route to a
senior approver" stop payment (yn_payment_stopped)? A15 does a pressure line ("already signed off") change the action?
A16 masked codes: is the code or the bird name the answer? A17 "Is it not true that X is not released": one reading?

## 4. Resolution of A1-A17

A1 passes (R5, cmp.le). A2 fails (R5, cmp.lt is strict). A3 the PO unit price (R5; the card says "of the PO unit
price"). A4 never (R5 one-sided; "Lower invoiced prices always pass"). A5 passes (R4). A6 received (R4). A7 the
first failing check in the check order printed on the "Check order:" line (R8, R9; the listed order is the error
model first_failure_only). A8 no (R19). A9 the price check alone (R18; "taken on its own"). A10 no (R6, "exact match
only"). A11 the invoice total; yes at equality (R7). A12 no (R4-R7 are per line or per stated total). A13 no (R1).
A14 yes: release is the only action that pays (R9). A15 no (R14; closed world). A16 the code (R11). A17 yes iff
released (R17; admitted only by 2/2 extraction, H16). GSL_EXCEPTIONS: none. NAME_ALLOW: AP, ERP, PO.

## 5. Resolution of the Haiku ambiguity pass (c2-data-stage-a/amb:T12; H<n> = point n of the record)

H1 (b): the permutation decides and the card prints it; the old literal was an example, now "Check order: {ORDER}"
(R12; code unchanged). H2 (a): two orders only, the check order (decides) and the listed order (error model
first_failure_only, R23); numbered lists are always in the check order (R8). H3 (b) with a reason: only the permutation
is drawn; the position is uniform on ch_action rows because the action is drawn first (R8, measured). H4 (b)+(c): R8
per-sampler shares; the table is S3 only; aligned = check order. H5: items renamed R1-R27; S1-S5 are samplers only
(header). H6 (a): training PCT {1, 3, 5}, S5 {2, 4} (R5; code changed, tested). H7 (a)+(c): an inclusion rate per
row; the label of a check on the card is always printed (R8, header). H8 (a): the formal rule; 9 invoiced against 8
received fails (R4, R1). H9 (a): clamped to PO_Q - 1 (R1). H10 (a): the card's comparators throughout; the gcd rule holds on every
line by construction (R5, R26). H11 (a): per unit of price, never scaled by quantity (R5; t12_line_total_base is the
scaled error). H12 (b), soft with a nearest-value fallback; PO_P band, D range and LIMIT values stated (R1, R5, R7).
H13 (a)+(c): terms in the header; "cheapest PO_P" = the lowest PO unit price among the row's lines; two_fail = two or
more failing checks (R22), not two failing price lines (R16). H14 (a): one-sided by the condition itself (R5). H15
(b): the card's comparator decides; question wordings never say "within" (R18); comparator forms say the endpoint
plainly and banned forms are dropped (section 2). H16 (a): the form and its share stay; every wording is admitted only
by 2/2 extraction at the pool stage, a split wording is dropped, and a shortfall is reported, never re-filled from
another form (section 2). H17 (a) + "yes = bad" defined (R20, Balance). H18 (a): R24 rates are draws per base spec;
Balance shares are measured on final rows; spec 4.1 bands apply to rows. H19 (a): every variant is fixed by the
comparator and the base side, with recomputation (R24). H20 (a): definitions in R23; reverse = the check order. H21
(b), all documents together, so the join holds; the order line is regenerated (R24). H22 (a): row-level (R11). H23
(a): identity by construction (R1, R12). H24 (a): one receipt; the register holds numbers only (R1, R4). H25 (a): code
on the Amounts line, symbol or code on amounts, one currency per row (R3). H26 (a): narrative only (R14). H27 (a):
closed kit word lists, number words and quantifiers included (section 2). H28 (a): complement-only (R17). H29: R25
(two operation kinds). H30 (a): {PREC} is a 3/3-admitted first_failing form naming the check order, with the decoy
first_listed (R9, section 2); terms are defined in section 6.

## 6. Terms from outside this page

C2_DATA_SPEC 3.15 = this family's build note; PREREG A37 / A38 = the rulings that allow C2 data after the OHS-4 freeze.
Mode T = a Haiku template whose values the program fills; Mode F = Haiku free text from a facts-only brief. mixdev =
the never-trained dev mix (S5, held-out registers, wordings and values). G-SL = slot lint (kit gsl.py closed word
lists); G-LEX = lexicon admission (unit test + 2/2 Haiku extraction to the same meaning, 3/3 for precedence); 2/2 =
two independent readers both pick the meaning; G3 = parse round trip; G3-H = Haiku extraction of Mode F facts; G4 =
metamorphic relations; G-TW = twin and complement check; k_all / k_syn = negcount (c_src/common/negcount.py) counts on
the question wording; GSL_EXCEPTIONS = extended lint words this family allows (none); NAME_ALLOW = capitalised
non-names skins may use (AP, ERP, PO). Change log: v1 (code freeze) -> v2 (this pass; code: PCTS, decoy sem
prec.t12.first_listed, fixture comparators and one fixture wording; new authoring.py; new tests for H1-H30) -> v2.1
(pool stage: the v1 pool admitted no cmp.le count-percent form, because the authored count phrases repeated the
cents phrases and the lexicon keeps one slot kind per text; section 2 now states the coverage and the count-percent
form rule; no code, gate or gold change).
