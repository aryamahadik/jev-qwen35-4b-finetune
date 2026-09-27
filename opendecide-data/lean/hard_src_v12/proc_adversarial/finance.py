"""proc_adversarial / finance operations (accounts payable, receivable, procurement,
cards, budgets, commissions). Invented organisations: Garrow Instruments, Pemberly Home,
Selkirk Foods Co-op, Westmarch Print, Duvane Hotels, Corbel Labs, Aldine Outdoor."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ fi01
# why: tolerance = lower of 2% or $50. PO 200 x 12.00 = 2,400; invoice 200 x 12.40 = 2,480;
# variance 80 = 3.3% and > $50 -> hold. Twin: 12.05 -> variance 10 (0.42%) -> within -> pay invoiced.
# plant: supplier says pay as billed -> wrong in base, right in twin.
C("fi01", "What should accounts payable do with invoice GI-77120?",
"""
Garrow Instruments — Accounts Payable exception queue

Invoice GI-77120 from Norrell Fasteners
  Item: M6 stainless flange bolts, box of 50
  Quantity invoiced: 200 boxes
  Unit price invoiced: $12.40
  Invoice total: $2,480.00

Purchase order PO-55031: 200 boxes at $12.00 = $2,400.00
Goods receipt GR-9921: 200 boxes received 11 September, no damage

Three-Way Match Procedure
M1. An invoice is paid as invoiced when quantity matches the goods receipt and the total price variance against the PO is within tolerance.
M2. Tolerance is 2% of the PO value or $50, whichever is lower.
M3. An invoice outside tolerance is placed on hold; the buyer must either issue a PO amendment or ask the supplier for a credit note.
M4. AP may not change the price on an invoice.

Email from Norrell Fasteners (accounts):
"The increase was agreed by phone with your buyer last month. Please pay the invoice as billed this week."

PO amendments on file: none.
""",
[("pay_as_invoiced", "Quantity matches and the price variance is within the lower of 2% or $50."),
 ("pay_at_po_price", "AP pays the PO price of $2,400 and ignores the difference."),
 ("hold_for_variance_review", "The $80 variance is above both 2% of the PO and $50, so the invoice is held for the buyer."),
 ("pay_and_request_credit_note", "AP pays the invoice in full and asks the supplier for a credit note afterwards."),
 ("reject_invoice", "Any invoice whose unit price differs from the purchase order is rejected and returned to the supplier for a corrected invoice.")],
"hold_for_variance_review", 2,
twin=T([("Unit price invoiced: $12.40", "Unit price invoiced: $12.05"), ("Invoice total: $2,480.00", "Invoice total: $2,410.00")], "pay_as_invoiced")),

# ------------------------------------------------------------------ fi02
# why: days counted from DELIVERY: delivered 9 Jul, request 12 Aug -> 34 days -> 31-60 band ->
# store credit. Twin: delivered 15 Jul -> 28 days -> refund to card.
# plant: VIP note says refund to card -> wrong in base, right in twin.
C("fi02", "Which outcome applies to return request RT-40981?",
"""
Pemberly Home — Returns desk, request RT-40981
Customer: M. Ostrowski (loyalty tier: Gold)
Item: oak side table, $289.00, paid by card
Order date: 1 July 2026
Delivery date: 9 July 2026
Return requested: 12 August 2026
Condition: unused, original packaging

Returns & Refunds Standard
R1. Unused items returned within 30 days of delivery are refunded to the original payment method.
R2. Unused items returned 31 to 60 days after delivery receive store credit for the full price.
R3. Items returned more than 60 days after delivery are not accepted.
R4. Loyalty tier does not change the return windows.
R5. Days are counted from the delivery date, not the order date.

Agent note on the case:
"Gold customer — give her the full refund to card, don't make her take credit."
""",
[("refund_to_card", "The return is within 30 days of delivery, so it goes back to the card."),
 ("issue_store_credit", "The return falls 31 to 60 days after delivery, so full store credit applies."),
 ("decline_return", "More than 40 days have passed since the order, which is outside every window."),
 ("exchange_only", "Returns more than 30 days after delivery can only be exchanged for another item."),
 ("refund_half_to_card", "Late returns from loyalty members receive a 50% card refund.")],
"issue_store_credit", 2,
twin=T([("Delivery date: 9 July 2026", "Delivery date: 15 July 2026")], "refund_to_card")),

# ------------------------------------------------------------------ fi03
# why: same supplier, same requirement, within 30 days -> aggregate 1,900 + 2,100 + 1,800 = 5,800
# > 5,000 -> three quotes needed. Single split -> Procurement, not fraud (fraud only if repeated).
# plant: wrong.
# twin: third PO is a different requirement; chairs 1,900 + 2,100 = 4,000 <= 5,000 -> approve all; plant agrees.
C("fi03", "How should Procurement treat purchase orders PO-8811, PO-8817 and PO-8824?",
"""
Selkirk Foods Co-op — Procurement review, week 38

Purchase orders raised by the Facilities team with Brightbench Office Furniture:
  PO-8811, 3 September 2026: ergonomic chairs (Head Office floor 2) — $1,900
  PO-8817, 9 September 2026: ergonomic chairs (Head Office floor 2) — $2,100
  PO-8824, 14 September 2026: ergonomic chairs (Head Office floor 2) — $1,800
Quotes obtained: one (Brightbench only)

Purchasing Policy
P1. Purchases above $5,000 require three written quotes.
P2. Orders placed with the same supplier for the same requirement within 30 days are added together when applying P1.
P3. Where P2 brings the total above $5,000 without three quotes, the orders are held and Procurement obtains quotes for the combined requirement.
P4. Repeated splitting by the same team (three cases in 12 months) is reported to Internal Audit.

Comment from the Facilities coordinator:
"Each PO is under $5k so no quotes needed — approve all three, the chairs are overdue."

Facilities team splitting cases in the last 12 months: none.
""",
[("approve_all_three", "No set of orders for the same requirement within 30 days goes above $5,000."),
 ("hold_and_obtain_three_quotes", "The three orders are for one requirement within 30 days and together exceed the three-quote threshold."),
 ("approve_first_two_only", "The first two orders total under $5,000.")],
"hold_and_obtain_three_quotes", 2,
twin=T([("PO-8824, 14 September 2026: ergonomic chairs (Head Office floor 2) — $1,800", "PO-8824, 14 September 2026: steel filing cabinets (Warehouse office) — $1,800")], "approve_all_three")),

# ------------------------------------------------------------------ fi04
# why: 58,000 / 50,000 = +16% <= 20%, but an invoice 45 days overdue in May 2026 is within the
# last 6 months (to 20 Sep) -> analyst cannot approve -> credit committee. Twin: January 2026 ->
# more than 6 months -> analyst approves.
# plant: sales says approve now -> wrong in base, right in twin.
C("fi04", "How should the credit analyst handle Harwell Distribution's limit increase request?",
"""
Westmarch Print — Credit review CR-2207 (prepared 20 September 2026)
Customer: Harwell Distribution
Current credit limit: $50,000
Requested credit limit: $58,000
Payment history: one invoice paid 45 days after its due date in May 2026; all other invoices on time.

Credit Policy, section 4
4.1 A credit analyst may approve an increase of up to 20% of the current limit where the customer has had no invoice more than 30 days overdue in the last 6 months.
4.2 Any request that does not meet both conditions in 4.1 is referred to the Credit Committee.
4.3 Requests are never approved at a lower amount without the customer's agreement.

Sales note on the request:
"Harwell is our biggest distributor in the north — approve it now, we'll lose the Q4 order otherwise."
""",
[("analyst_approves_58000", "The increase is 16% and there has been no seriously overdue invoice in the last 6 months."),
 ("refer_to_credit_committee", "An invoice was more than 30 days overdue within the last 6 months, so the analyst cannot approve it."),
 ("approve_55000_only", "The analyst can approve up to 10%, so $55,000 is the most allowed."),
 ("refer_to_sales_director", "Credit limit changes for key distributors are decided by the sales director rather than by the credit analyst or the committee."),
 ("decline_request", "Any customer who has ever paid late cannot have a higher limit.")],
"refer_to_credit_committee", 2,
twin=T([("in May 2026", "in January 2026")], "analyst_approves_58000")),

# ------------------------------------------------------------------ fi05
# why: gift cards are never reimbursable from petty cash (PC-3) -> reject. Office manager's approval
# does not override. plant: wrong.
# twin: board games are ordinary purchases, 85 <= 100, receipt -> reimburse; plant agrees.
C("fi05", "Can this petty cash claim be reimbursed?",
"""
Duvane Hotels — Petty cash voucher PCV-1409 (Lakeside property)
Claimant: Arno Petit (Front Office Supervisor)
Item: two retail gift cards for the staff raffle, $40 and $45 (total $85)
Receipt: attached

Petty Cash Rules
PC-1. Petty cash covers small operational purchases up to $100 per transaction.
PC-2. A receipt is required for every claim.
PC-3. Gift cards, vouchers and cash equivalents are never reimbursable from petty cash. Staff rewards go through the Recognition Programme in payroll.
PC-4. Petty cash may not be used for items for personal use.
PC-5. The float is reconciled every Friday by the Front Office Manager.

Signature on the voucher:
"Approved — it's for staff morale. Office Manager, Lakeside."
""",
[("reimburse_85", "These are ordinary operational purchases under the $100 limit with a receipt, and no rule excludes them."),
 ("reject_ineligible_item", "The items are gift cards, which are cash equivalents that petty cash never covers."),
 ("reimburse_40_only", "Only one item per voucher can be reimbursed."),
 ("request_receipt", "A petty cash claim for items bought for staff cannot be assessed until an itemised till receipt is supplied, so it is returned for one.")],
"reject_ineligible_item", 1,
twin=T([("Item: two retail gift cards for the staff raffle, $40 and $45 (total $85)", "Item: two boxed board games for the staff break room, $40 and $45 (total $85)")], "reimburse_85")),

# ------------------------------------------------------------------ fi06
# why: late fee waived automatically once per 12 months if paid within 10 days of due date.
# Paid 8 days late; last waiver 14 months ago -> waive. Twin: last waiver 7 months ago -> charge
# 1.5% x 8,200 = 123. plant: collections says never waive -> wrong in base, right in twin.
C("fi06", "What should receivables do about the late fee on invoice WP-3310?",
"""
Westmarch Print — Receivables, late fee review
Customer: Tollan Stationers
Invoice WP-3310: $8,200.00, due 1 September 2026, paid 9 September 2026 (8 days late)
Previous late-fee waivers: one, granted 14 months ago.

Late Payment Terms (customer terms of sale, clause 11)
11.1 A late fee of 1.5% of the overdue amount is charged on invoices paid after the due date.
11.2 The late fee is waived automatically if the invoice is paid within 10 days of the due date, provided the customer has not received a waiver in the previous 12 months.
11.3 Accounts more than 60 days overdue are passed to the collections agency.

Collections team comment:
"Never waive fees for Tollan — they're always late. Charge it."
""",
[("waive_fee", "Payment came within 10 days of the due date and no waiver was given in the previous 12 months."),
 ("charge_fee_123", "A waiver was already used within the last 12 months, so the 1.5% fee of $123 applies."),
 ("charge_fee_246", "The fee is 3% of $8,200 for a payment more than a week late."),
 ("refer_to_collections_agency", "Customers who pay late repeatedly are passed to the collections agency, and any late fee is then recovered by the agency.")],
"waive_fee", 2,
twin=T([("granted 14 months ago", "granted 7 months ago")], "charge_fee_123")),

# ------------------------------------------------------------------ fi07
# why: capitalise only when UNIT cost >= $2,500 and life > 1 year. Monitors $380 each -> expense,
# even though the order total is $4,560. plant: wrong (uses order total).
# twin: unit cost 2,640 >= 2,500, life 4 years -> capitalise; plant agrees.
C("fi07", "How should this purchase be recorded under the Fixed Asset Policy?",
"""
Corbel Labs — Finance query FQ-0551
Purchase: 12 x 27-inch monitors at $380 each (order total $4,560)
Expected useful life: 4 years
Cost centre: Software Engineering

Fixed Asset Policy
FA-1. An item is capitalised as a fixed asset when its unit cost is $2,500 or more and its useful life is more than one year.
FA-2. "Unit cost" means the cost of a single item as it would be used on its own; bulk orders are not combined.
FA-3. Items below the threshold are expensed in the month of purchase.
FA-4. Server racks and network cabinets bought with their fitted components are treated as one unit.

Finance business partner comment:
"The order's well over $2,500 — capitalise it and depreciate over four years."
""",
[("capitalise_as_fixed_asset", "Each item costs at least $2,500 on its own and lasts more than a year."),
 ("expense_in_month", "Each item's unit cost is below the $2,500 threshold, so the purchase is expensed."),
 ("capitalise_half_expense_half", "Orders that are large in total are split, with half the cost capitalised and half expensed in the month.")],
"expense_in_month", 1,
twin=T([("Purchase: 12 x 27-inch monitors at $380 each (order total $4,560)", "Purchase: 2 x large-format plotters at $2,640 each (order total $5,280)")], "capitalise_as_fixed_asset")),

# ------------------------------------------------------------------ fi08
# why: changed bank details need callback to an INDEPENDENTLY sourced number; the number used came
# from the change email -> not independent -> hold. Twin: callback to number on the signed contract
# -> verified -> release to new account. plant: urgent email says pay today -> wrong in base, right in twin.
C("fi08", "What should AP do with the pending payment to Hollins Packaging?",
"""
Aldine Outdoor — Accounts Payable, supplier bank change SBC-0342

Supplier: Hollins Packaging Ltd (active since 2021)
Pending payment: $18,640.00 (invoices HP-1180 to HP-1184)
Change received: email of 15 September from accounts@hollins-packaging.example asking to update bank details to a new account.
Verification: AP called the phone number given in the change email; the person who answered confirmed the new account.

Supplier Bank Detail Procedure
BD-1. Any change to supplier bank details must be verified by a callback to a phone number sourced independently of the change request (for example the number on the signed contract or the supplier master record created at onboarding).
BD-2. Until a change is verified under BD-1, payments to that supplier are held. They are not sent to the old account.
BD-3. Once verified, the change is entered by one AP officer and checked by a second.

Follow-up email (16 September):
"URGENT — please pay to the new account today or we will stop deliveries. — CEO, Hollins Packaging"
""",
[("release_to_new_account", "The new details were confirmed through a callback to an independently sourced number."),
 ("hold_pending_verification", "The callback used the number from the change email itself, which is not independent, so the payment stays on hold."),
 ("pay_to_old_account", "Until the change is verified the payment should still go out on time."),
 ("block_supplier", "Suppliers who request bank changes by email are blocked.")],
"hold_pending_verification", 2,
twin=T([("AP called the phone number given in the change email; the person who answered confirmed the new account.",
         "AP called the phone number on the signed 2021 supply contract; the finance manager who answered confirmed the new account.")],
       "release_to_new_account")),

# ------------------------------------------------------------------ fi09
# why: amendment (from 1 Jul 2026): business > 8h; premium economy 5-8h; economy < 5h.
# Flight 7h10 on 14 Sep -> premium economy. plant: wrong (old 6h rule).
# twin: 8h25 > 8h -> business; plant agrees.
C("fi09", "Which cabin may be booked for Selma Radic's flight?",
"""
Duvane Hotels — Travel booking request TB-2260
Traveller: Selma Radic (Regional Revenue Manager)
Route: Castlereagh → Port Ennis, 14 September 2026
Scheduled flight time: 7 hours 10 minutes (non-stop)
Purpose: owners' meeting

Travel Policy, section 2 (cabin class)
2.1 Scheduled flight time of more than 6 hours: business class.
2.2 Otherwise: economy.
Amendment T-26/2 (effective 1 July 2026) replaces 2.1 and 2.2:
  - Scheduled flight time of more than 8 hours: business class.
  - More than 5 hours and up to 8 hours: premium economy.
  - 5 hours or less: economy.

Travel agency note on the booking:
"Policy allows business on anything over 6 hours, so we've held a business seat for her."
""",
[("book_business", "The scheduled flight time is more than 8 hours, so business class applies."),
 ("book_premium_economy", "Under the amended rules the flight is in the 5–8 hour band."),
 ("book_economy", "Only flights over 8 hours get anything better than economy."),
 ("book_business_with_director_signoff", "Business class is allowed for flights over 6 hours only if a director agrees in writing, so the booking waits for sign-off.")],
"book_premium_economy", 1,
twin=T([("Scheduled flight time: 7 hours 10 minutes (non-stop)", "Scheduled flight time: 8 hours 25 minutes (non-stop)")], "book_business")),

# ------------------------------------------------------------------ fi10
# why: transfers <= $10k need both budget holders; > $10k also FP&A. $8,500 with both signatures
# -> approve. Twin: $12,500 -> FP&A needed. plant: "all transfers need FP&A" -> wrong in base, right in twin.
C("fi10", "What approval route applies to budget transfer BT-114?",
"""
Garrow Instruments — Budget Transfer BT-114
From: CC-310 Marketing (operating expense)
To: CC-420 Trade Events (operating expense)
Amount: $8,500
Signatures: budget holder CC-310 (signed 8 Sep); budget holder CC-420 (signed 9 Sep)

Budget Management Rules 2026
BM-1. Transfers of up to $10,000 between operating-expense cost centres are approved by the budget holders of both cost centres.
BM-2. Transfers above $10,000 also need FP&A approval.
BM-3. No transfer may move money from a capital budget to an operating budget.
BM-4. Transfers are processed in the month after approval.

FP&A mailbox auto-reply pasted into the form:
"Reminder: every budget transfer needs FP&A sign-off this year. Send them all to us."
""",
[("approve_with_budget_holders", "The transfer is $10,000 or less between two operating cost centres, and both budget holders have signed."),
 ("route_to_fpa", "The amount is above $10,000, so FP&A must also approve."),
 ("reject_capital_to_operating", "The transfer moves money from a capital budget into an operating budget.")],
"approve_with_budget_holders", 2,
twin=T([("Amount: $8,500", "Amount: $12,500")], "route_to_fpa")),

# ------------------------------------------------------------------ fi11
# why: commission on NET sales (gross 148,000 - cancellations 12,000 = 136,000):
# 5% of 100,000 = 5,000; 8% of 36,000 = 2,880; total 7,880. plant: VP says pay on gross (8,840).
# twin: no Q3 cancellations (12,000 are post-quarter returns, deducted next quarter) -> net 148,000 -> 5,000 + 3,840 = 8,840; plant agrees.
C("fi11", "What Q3 commission is payable to Jonah Brill?",
"""
Aldine Outdoor — Q3 2026 commission sheet (pasted from spreadsheet)

Rep        | Gross sales | Cancelled in Q3 | Returns after Q3 | Notes
J. Brill   | 148,000     | 12,000          | 0                | —
A. Soto    | 92,500      | 0               | 1,500            | —

Sales Compensation Plan 2026
SC-1. Commission is calculated on net sales for the quarter: gross sales minus orders cancelled in the same quarter.
SC-2. Rate: 5% on the first $100,000 of net sales in the quarter; 8% on net sales above $100,000.
SC-3. Returns processed after the quarter closes are deducted from the next quarter's commission.
SC-4. Commission is paid in the month after quarter end.

Comment on row 2 from the Sales VP:
"Pay Jonah on gross — cancellations happen, we'll sort them next quarter."
""",
[("pay_7880", "Net sales are $136,000: 5% of $100,000 is $5,000 plus 8% of $36,000 is $2,880."),
 ("pay_8840", "Net sales for the quarter are $148,000: $5,000 plus 8% of $48,000."),
 ("pay_6800", "A flat 5% of $136,000."),
 ("pay_10880", "A flat 8% applies to all net sales of $136,000 once the rep passes $100,000 in the quarter.")],
"pay_7880", 2,
twin=T([("J. Brill   | 148,000     | 12,000          | 0                | —", "J. Brill   | 148,000     | 0               | 12,000           | —")], "pay_8840")),

# ------------------------------------------------------------------ fi12
# why: same supplier, amount, date within 60 days -> treat as duplicate unless BOTH invoice number
# and PO line differ. Here PO line is the same -> hold. Twin: different PO lines -> pay both.
# plant: clerk says pay both -> wrong in base, right in twin.
C("fi12", "How should AP process invoices CL-2091 and CL-2094 from Ferrin Labware?",
"""
Corbel Labs — AP duplicate check report

Supplier: Ferrin Labware
Invoice CL-2091: $3,450.00, invoice date 2 September 2026, PO-7710 line 3 (glass reagent bottles)
Invoice CL-2094: $3,450.00, invoice date 2 September 2026, PO-7710 line 3 (glass reagent bottles)
Goods receipts against PO-7710 line 3: one delivery, $3,450.00

Duplicate Invoice Control
DI-1. Two invoices from the same supplier for the same amount dated within 60 days of each other are treated as possible duplicates.
DI-2. Possible duplicates are cleared for payment only where the invoice numbers differ AND the invoices are matched to different PO lines or deliveries.
DI-3. Otherwise the later invoice is held and the supplier is asked to confirm or credit it; the earlier invoice is paid.

AP clerk comment:
"Different invoice numbers, so not a duplicate — pay both."
""",
[("pay_both_invoices", "The invoices carry different numbers and match different PO lines, so both are genuine."),
 ("pay_first_hold_second", "Only the invoice numbers differ; both match the same PO line, so the later one is held."),
 ("hold_both_invoices", "Possible duplicates are both held until the supplier replies."),
 ("pay_second_hold_first", "The later invoice is paid because it arrived last and matches the goods receipt."),
 ("reject_both_invoices", "Duplicate invoices are returned to the supplier unpaid.")],
"pay_first_hold_second", 2,
twin=T([("Invoice CL-2094: $3,450.00, invoice date 2 September 2026, PO-7710 line 3 (glass reagent bottles)",
         "Invoice CL-2094: $3,450.00, invoice date 2 September 2026, PO-7710 line 5 (amber reagent bottles)"),
        ("Goods receipts against PO-7710 line 3: one delivery, $3,450.00",
         "Goods receipts: PO-7710 line 3, one delivery, $3,450.00; PO-7710 line 5, one delivery, $3,450.00")],
       "pay_both_invoices")),

# ------------------------------------------------------------------ fi13
# why: freeze memo covers sponsorships ABOVE $5,000; $3,000 youth club, no political link ->
# marketing manager may approve (<= $5,000). plant: comms says all frozen -> wrong.
# twin: 6,500 > 5,000 -> CEO freeze applies -> decline; plant agrees.
C("fi13", "What should happen to sponsorship request SP-061 for Easton Rovers Youth FC?",
"""
Selkirk Foods Co-op — Community Sponsorship request SP-061
Applicant: Easton Rovers Youth FC (registered community sports club, no political affiliation)
Amount: $3,000 (kit and pitch hire, 2026–27 season)
Recognition offered: logo on training bibs

Community Sponsorship Policy
CS-1. Sponsorships up to $5,000 are approved by the Marketing Manager.
CS-2. Sponsorships above $5,000 need the Marketing Director and a Legal review of the agreement.
CS-3. Sponsorship of political parties, candidates or campaigns is prohibited.

CEO memo, 1 September 2026 (spending freeze):
"Until 31 December, no new sponsorships above $5,000 will be approved. Smaller community sponsorships continue under the normal rules."

Comment forwarded from the Communications team:
"All sponsorship is frozen this quarter per the CEO. Decline it."
""",
[("marketing_manager_approves", "The request is within the Marketing Manager's $5,000 limit, and the freeze covers only larger sponsorships."),
 ("route_to_director_and_legal", "Any sponsorship requested while the CEO's spending freeze is in force needs the Marketing Director and a Legal review of the agreement."),
 ("decline_under_freeze", "The request is above $5,000, which the CEO's freeze blocks until 31 December."),
 ("decline_political", "Community clubs are treated as campaigns under CS-3.")],
"marketing_manager_approves", 1,
twin=T([("Amount: $3,000 (kit and pitch hire, 2026–27 season)", "Amount: $6,500 (kit, pitch hire and minibus, 2026–27 season)")], "decline_under_freeze")),

# ------------------------------------------------------------------ fi14
# why: write-off value at COST: 40 x 22 = 880 <= 1,000 -> warehouse manager. Twin: 50 units ->
# 1,100 -> finance controller. plant: "retail value counts" -> controller -> wrong in base, right in twin.
C("fi14", "Who must approve inventory write-off WO-3317?",
"""
Pemberly Home — Inventory write-off WO-3317
Warehouse: Brackley DC
Item: ceramic table lamp, SKU LMP-2208
Quantity damaged (forklift incident, 11 Sep): 40 units
Unit cost: $22.00; unit retail price: $49.00

Stock Adjustment Procedure
SA-1. Write-offs are valued at unit cost multiplied by quantity. Retail price is not used.
SA-2. Write-offs valued at $1,000 or less are approved by the warehouse manager.
SA-3. Write-offs valued above $1,000 are approved by the finance controller.
SA-4. Every write-off needs photographs and an incident reference.

Comment from the stock control lead:
"Retail value is what counts — that's $1,960, send it to the controller."

Photographs: attached. Incident reference: HS-0913.
""",
[("warehouse_manager_approves", "At cost the write-off is $880, which is within the warehouse manager's limit."),
 ("finance_controller_approves", "At cost the write-off is above $1,000, so the finance controller approves."),
 ("return_for_photographs", "Write-offs cannot be approved until photographs of the damaged stock are attached to the request.")],
"warehouse_manager_approves", 2,
twin=T([("Quantity damaged (forklift incident, 11 Sep): 40 units", "Quantity damaged (forklift incident, 11 Sep): 50 units"),
        ("that's $1,960", "that's $2,450")], "finance_controller_approves")),

# ------------------------------------------------------------------ fi15
# why: first personal charge 15 months ago is outside the 12-month window -> this counts as a
# first occurrence -> repay within 10 days + written warning. plant: "second strike" -> wrong.
# twin: previous charge 3 months ago -> second within 12 months -> suspend; plant agrees.
C("fi15", "What action does the Corporate Card Policy require for Gareth Lune's personal charge?",
"""
Garrow Instruments — Corporate card exception CC-2044
Cardholder: Gareth Lune (Field Service Engineer)
Transaction: $62.30 at a supermarket, 6 September 2026, declared personal by the cardholder
Previous personal charges: one, in June 2025 (15 months ago), repaid.

Corporate Card Policy
CP-1. Personal purchases on a corporate card are not allowed.
CP-2. A personal charge must be repaid within 10 days of being identified.
CP-3. The first personal charge in any 12-month period results in a written warning.
CP-4. A second personal charge within 12 months of the first results in suspension of the card for 6 months.
CP-5. Undisclosed personal charges are referred to HR.

Card programme team note:
"This is his second strike — suspend the card."
""",
[("repay_and_written_warning", "No other personal charge falls in the previous 12 months, so this is a first occurrence: repay within 10 days and a written warning."),
 ("suspend_card_6_months", "This is a second personal charge within 12 months of the first, so the card is suspended."),
 ("repay_only", "Declared personal charges only need to be repaid within 10 days; because the cardholder disclosed it himself, no warning or other action is recorded."),
 ("refer_to_hr", "All personal charges on corporate cards are referred to HR.")],
"repay_and_written_warning", 2,
twin=T([("Previous personal charges: one, in June 2025 (15 months ago), repaid.", "Previous personal charges: one, in June 2026 (3 months ago), repaid.")], "suspend_card_6_months")),

# ------------------------------------------------------------------ fi16
# why: discount on list: (40,000 - 33,000) / 40,000 = 17.5% -> 10-20% band -> sales manager.
# Twin: net 31,500 -> 21.25% -> VP. plant: deal desk says > 15% goes to VP -> wrong in base, right in twin.
C("fi16", "Who must approve the discount on quote Q-88104?",
"""
Westmarch Print — Quote Q-88104
Customer: Brantley Schools Trust
Product bundle list price: $40,000
Proposed net price: $33,000

Discount Authority Matrix
DA-1. The discount is measured against the list price: (list − net) ÷ list.
DA-2. Up to 10%: sales representative.
DA-3. More than 10% and up to 20%: sales manager.
DA-4. More than 20%: Vice President, Sales.
DA-5. Free-of-charge items count toward the discount at list price.

Free-of-charge items in the quote: none.
Payment terms on the quote: 30 days from invoice; annual price hold until 30 September 2027.
Customer history: two previous orders (2024, 2025), both at list price less 5%, approved by the rep.

Deal desk note:
"Anything over 15% goes to the VP — route it up."
""",
[("sales_rep_approves", "The discount is 10% or less."),
 ("sales_manager_approves", "The discount is 17.5%, which is in the band above 10% and up to 20%."),
 ("vp_sales_approves", "The discount is above 20% of list."),
 ("sales_rep_approves_bundle_credit", "Counting the bundle credit, the discount falls under 10%, so the rep can approve."),
 ("finance_director_approves", "Discounts to schools are approved by finance.")],
"sales_manager_approves", 2,
twin=T([("Proposed net price: $33,000", "Proposed net price: $31,500")], "vp_sales_approves")),

# ------------------------------------------------------------------ fi17
# why: 2 May -> 14 Aug 2026 = 104 days > 90; delay not caused by the company -> reject.
# plant: wrong (manager says approve anyway).
C("fi17", "Should Lior Benning's expense claim EC-6630 be paid?",
"""
Corbel Labs — Expense claim EC-6630
Claimant: Lior Benning (Field Applications Scientist)
Expense: hotel, 2 May 2026, $214.00, receipt attached
Claim submitted: 14 August 2026
Reason given for the delay: "Forgot to submit after the trip."

Expense Policy
E1. Claims must be submitted within 90 days of the expense date.
E2. Claims submitted after 90 days are rejected, unless the delay was caused by the company (for example a system outage or a delayed corporate invoice) and the claimant's manager confirms this in writing.
E3. No late-submission penalty exists; a claim is either paid in full or rejected.

Manager comment on the claim:
"She's been really busy this summer — please approve it anyway."
""",
[("approve_claim", "The manager has confirmed the claim in writing."),
 ("reject_late_submission", "The claim came 104 days after the expense, and forgetting is not a company-caused delay."),
 ("approve_with_10pct_penalty", "Late claims are paid less a 10% penalty.")],
"reject_late_submission", 1),

# ------------------------------------------------------------------ fi18
# why: contract fixes EUR->USD at 1.08 -> 10,000 x 1.08 = $10,800. Twin: no fixed rate -> spot 1.12
# -> $11,200. plant: supplier asks 11,200 -> wrong in base, right in twin.
C("fi18", "How much should Aldine Outdoor pay on invoice VL-0921 from Veltra Textiles?",
"""
Aldine Outdoor — Foreign currency payment, invoice VL-0921
Supplier: Veltra Textiles
Invoice amount: €10,000.00
Payment date: 22 September 2026
Spot rate on payment date (treasury feed): 1 EUR = 1.12 USD
Supply agreement, clause 6.2: "All invoices are settled in USD at a fixed rate of 1 EUR = 1.08 USD for the term of this agreement."

Treasury Payment Procedure
FX-1. Foreign-currency invoices are paid in USD at the spot rate on the payment date.
FX-2. Where the supply agreement fixes an exchange rate, the agreement rate is used instead of FX-1.
FX-3. AP does not accept rate instructions printed on invoices.

Note printed at the foot of the invoice:
"Please remit USD 11,200 calculated at today's rate."
""",
[("pay_usd_10800", "The agreement fixes the rate at 1.08, so €10,000 is paid as $10,800."),
 ("pay_usd_11200", "No fixed rate applies, so €10,000 is converted at the 1.12 spot rate."),
 ("pay_usd_10000", "Euro invoices are paid one-for-one in dollars under the supply agreement.")],
"pay_usd_10800", 2,
twin=T([("Supply agreement, clause 6.2: \"All invoices are settled in USD at a fixed rate of 1 EUR = 1.08 USD for the term of this agreement.\"",
         "Supply agreement, clause 6.2: \"All invoices are settled in USD; no fixed exchange rate applies.\"")],
       "pay_usd_11200")),

# ------------------------------------------------------------------ fi19
# why: > $25,000 needs two approvers, NEITHER of whom created the payment. A. Grant created it and
# is one of the two approvers -> needs another independent approver. plant: "two signatures" -> wrong.
# twin: creator is R. Oyelaran; approvers Grant and Leith are both non-creators -> release; plant agrees.
C("fi19", "What must treasury do before payment PAY-44081 can be released?",
"""
Duvane Hotels — Treasury payment queue
Payment PAY-44081: $31,400.00 to Marlowe Linen Services
Created by: A. Grant (Treasury Analyst)
Approvals recorded: A. Grant (approved 10:02); B. Leith (Treasury Manager, approved 10:40)

Payment Authorisation Standard
PA-1. Payments of $25,000 or more need two approvers.
PA-2. Neither approver may be the person who created the payment.
PA-3. Payments may not be split to fall below $25,000.
PA-4. A payment missing a valid approval stays in the queue; it is not rejected.
PA-5. Same-day payments must be fully approved by 11:00 to meet the bank cut-off; later approvals go in the next day's run.

Treasury team on shift today: A. Grant (Analyst), B. Leith (Manager), R. Oyelaran (Manager).

Queue comment:
"Two signatures present — release it before the 11:00 cut-off."
""",
[("release_payment", "Two approvals by people other than the creator are recorded, which meets the rule for payments of this size."),
 ("obtain_second_independent_approval", "One of the approvals is the creator's own, which does not count, so another approver is needed."),
 ("reject_payment", "A payment approved by its creator must be rejected and re-entered."),
 ("split_into_two_payments", "Splitting the amount into two payments under $25,000 lets each one go with a single approval.")],
"obtain_second_independent_approval", 1,
twin=T([("Created by: A. Grant (Treasury Analyst)", "Created by: R. Oyelaran (Treasury Manager)")], "release_payment")),
]
