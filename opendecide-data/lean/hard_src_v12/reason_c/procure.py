"""reason_c / procurement, approvals, vendor management and accounts payable
(Quillon Freight, Marrowby Health Trust, Ostrava Components, Halvard Group,
Selcombe University, Tanager Foods)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ pr01
# why: value = full-term total: $9,200 x 3 = $27,600 -> band $25,000.01-$100,000 ->
# Finance Director. Software -> IT Security review first (footnote a). Not capital.
# Twin: 2-year term -> $18,400 -> Department Head, still software -> IT Security first.
C("pr01", "Which approval path does this purchase request need?",
"""
Quillon Freight — Delegation of Authority, Schedule B (purchasing)

| Purchase value | Approver |
| up to $5,000 | Team Lead |
| $5,000.01 - $25,000 | Department Head |
| $25,000.01 - $100,000 | Finance Director |
| over $100,000 | CFO and CEO jointly |

Notes
(a) Any software, SaaS or IT hardware purchase, at any value, must pass IT Security review before it goes to the approver in the table.
(b) Capital equipment above $10,000 goes to the Capex Committee instead of the approver in the table.
(c) Purchase value is the total contract value over the full committed term, excluding sales tax.
(d) Marketing sponsorships follow Schedule D.

Purchase request PR-26-0918
Requester: Leona Birch (Operations Planning).
Item: RouteWise fleet-planning SaaS, 40 seats.
Price: $9,200 per year, 3-year committed term, billed annually. Sales tax extra.
Justification: replaces spreadsheets for depot scheduling.
Category selected by requester: Software subscription (operating expense).
""",
[("Team Lead", "approval by the requester's team lead only."),
 ("Department Head", "approval by the department head only."),
 ("Finance Director", "approval by the Finance Director only."),
 ("CFO and CEO jointly", "joint approval by the CFO and the CEO."),
 ("Capex Committee", "capital equipment approval by the committee."),
 ("IT Security review, then Department Head", "IT Security clears the purchase, then the Department Head approves."),
 ("IT Security review, then Finance Director", "IT Security clears the purchase, then the Finance Director approves."),
 ("IT Security review, then CFO and CEO", "IT Security clears the purchase, then the CFO and CEO approve jointly.")],
"IT Security review, then Finance Director", 3,
twin=T([("3-year committed term", "2-year committed term")], "IT Security review, then Department Head")),

# ------------------------------------------------------------------ pr02
# why: value includes delivery and installation, excludes tax: 9,850 + 240 = 10,090 >
# 10,000 -> three written quotes needed; only two on file, no sole-source form -> no.
# Twin: delivery $120 -> 9,970 <= 10,000 -> one quote enough -> yes.
Y("pr02", "Does this purchase meet the quotation requirement?",
"""
Marrowby Health Trust — Procurement Standing Orders, section 5

5.1 Purchase value means the price of the goods or services plus delivery and installation charges, excluding VAT.
5.2 Purchase value up to and including $10,000: one written quote.
5.3 Purchase value above $10,000 and up to $75,000: three written quotes, or an approved Sole-Source Justification (form SSJ-1).
5.4 Above $75,000: formal tender.
5.5 Framework-agreement call-offs are exempt from 5.2-5.4.

Requisition RQ-44810 (Estates department)
Item: two ceiling-mounted patient hoists for Ward 7.
Supplier chosen: Carrow Medical Lifts. Goods price $9,850 excluding VAT.
Delivery and installation: $240 (quoted separately on the same quote).
VAT: 20%, charged on top.
Quotes on file: Carrow Medical Lifts ($9,850 + $240) and Stellan Care Equipment ($10,400 + $300).
SSJ-1 form: none. Framework agreement: none covers hoists.
""",
[("Purchase value", "goods or services price plus delivery and installation, excluding VAT."),
 ("Quotation requirement", "one quote up to $10,000; three quotes or an approved SSJ-1 above $10,000 up to $75,000.")],
0, 2,
twin=T([("Delivery and installation: $240 (quoted separately on the same quote).",
         "Delivery and installation: $120 (quoted separately on the same quote)."),
        ("Carrow Medical Lifts ($9,850 + $240)", "Carrow Medical Lifts ($9,850 + $120)")], 1)),

# ------------------------------------------------------------------ pr03
# why: PO 200 x $14.50 = $2,900; received 200; invoiced 200 x $14.95 = $2,990.
# Over by $90. Tolerance = lower of 2% ($58) or $50 = $50. $90 > $50 -> price hold.
# Quantity matches. Twin: $14.70 -> $2,940, over by $40 <= $50 -> approve.
C("pr03", "What status should accounts payable give this invoice?",
"""
Ostrava Components — AP three-way match rules

M1 Quantity: invoiced quantity must not exceed the quantity received on the goods receipt. If it does: HOLD-QTY.
M2 Price: the invoice total may exceed (PO unit price x invoiced quantity) by no more than the LOWER of 2% or $50. If it exceeds that tolerance: HOLD-PRICE.
M3 Missing goods receipt: HOLD-GR.
M4 If M1-M3 pass: APPROVE for the next payment run.
M5 Freight lines are matched separately against the freight contract and ignored for M2.

Invoice INV-77120 from Brandt Fasteners
PO 4500-3318: 200 boxes of M10 hex flange bolts at $14.50 per box.
Goods receipt GR-99021: 200 boxes received 8 September 2026.
Invoice lines: 200 boxes at $14.95 = $2,990.00; freight $85.00 (separate line).
Buyer note on PO: "Supplier warned of steel surcharges this quarter."
""",
[("APPROVE", "all match rules pass; pay in the next run."),
 ("HOLD-QTY", "more was invoiced than was received."),
 ("HOLD-PRICE", "the invoice exceeds the price tolerance."),
 ("HOLD-GR", "no goods receipt exists for the PO."),
 ("REJECT", "the invoice is returned to the supplier as invalid.")],
"HOLD-PRICE", 3,
twin=T([("200 boxes at $14.95 = $2,990.00", "200 boxes at $14.70 = $2,940.00")], "APPROVE")),

# ------------------------------------------------------------------ pr04
# why: 2/10 net 30: invoice date 3 Sep = day 0; discount if paid by day 10 = 13 Sep.
# Payment run 14 Sep = day 11 -> no discount -> $8,400.00. Late fee only after day 30.
# Twin: run on 11 Sep = day 8 -> 2% off -> 8,400 x 0.98 = $8,232.00.
C("pr04", "What amount should be released in the payment run?",
"""
Halvard Group — AP desk instruction 12 (supplier discounts)

Terms "2/10 net 30" mean: pay within 10 days of the invoice date and deduct 2%; otherwise the full amount is due within 30 days. The invoice date is day 0; the payment run date is the payment date.
Terms "1/15 net 45": pay within 15 days and deduct 1%; otherwise due in 45 days.
Late payment: suppliers may charge 1.5% of the invoice amount if paid after the net due date.
Credit notes are applied before any discount is calculated.

Invoice from Pemberly Packaging
Invoice number PP-30194. Invoice date: 3 September 2026. Amount: $8,400.00. Terms: 2/10 net 30.
Credit notes open for this supplier: none.
Scheduled payment run: 14 September 2026.
Treasury note: "Cash is fine this month, take every discount we're entitled to."
""",
[("$8,232.00", "pay the invoice less a 2% discount."),
 ("$8,316.00", "pay the invoice less a 1% discount."),
 ("$8,400.00", "pay the full invoice amount."),
 ("$8,274.00", "pay the invoice less a 1.5% deduction."),
 ("$8,526.00", "pay the invoice plus a 1.5% late charge.")],
"$8,400.00", 2,
twin=T([("Scheduled payment run: 14 September 2026.", "Scheduled payment run: 11 September 2026.")], "$8,232.00")),

# ------------------------------------------------------------------ pr05
# why: sanctions screening valid 90 days. Screened 20 Jun, activation 23 Sep:
# 20 Jun->20 Jul 30, ->20 Aug 31, ->20 Sep 31, +3 = 95 days > 90 -> expired -> cannot
# activate. Spend $38k < $50k so no financial check needed. Twin: screened 25 Jul ->
# 25 Jul->25 Aug 31 + 29 = 60 days -> valid -> yes.
Y("pr05", "Can the supplier be activated for payment on 23 September 2026?",
"""
Selcombe University — Supplier onboarding checklist (Finance Operations)

A new supplier may be activated for payment only when all of these are on file and current:
1. Tax registration form (TR-2), signed.
2. Bank confirmation letter on the bank's letterhead, or a verified call-back record.
3. Sanctions and debarment screening result "clear", dated no more than 90 days before the activation date.
4. For expected annual spend above $50,000: a financial stability check.
Insurance certificates are requested by the contracting department, not by Finance Operations, and do not affect activation.

Supplier file: Ferncastle Lab Supplies Ltd
- TR-2: received 2 June 2026, signed.
- Bank letter: received 4 June 2026, on letterhead.
- Sanctions and debarment screening: clear, run 20 June 2026.
- Expected annual spend: $38,000.
- Public liability certificate: not yet received.
Activation requested for: 23 September 2026.
""",
[("Current screening", "a clear sanctions and debarment result dated no more than 90 days before activation."),
 ("Activation", "setting the supplier live so invoices can be paid.")],
0, 2,
twin=T([("clear, run 20 June 2026", "clear, run 25 July 2026")], 1)),

# ------------------------------------------------------------------ pr06
# why: precedence: signed amendments > MSA > SOW > PO. Draft amendment is unsigned
# -> ignored. MSA net 45 beats PO net 30. Invoice 1 Sep + 45 days = 16 Oct.
# Twin: amendment signed -> net 60 -> 1 Sep + 60 = 31 Oct.
C("pr06", "What is the payment due date for this invoice?",
"""
Tanager Foods — Contract precedence note for AP (legal-approved)

Where documents conflict on the same point, apply them in this order: (1) amendments signed by both parties; (2) the Master Services Agreement; (3) the Statement of Work; (4) purchase-order terms. Unsigned drafts and email correspondence have no effect. Due dates are counted in calendar days from the invoice date.

Supplier: Brightfield Pest Control
- MSA (signed 10 January 2025), clause 7.2: payment within 45 days of invoice date.
- SOW 2026-03: silent on payment terms.
- PO 5510-2291 printed terms: net 30.
- Amendment No. 1 (unsigned draft, circulated 4 May 2026): changes clause 7.2 to 60 days.
- Email from Brightfield's account manager, 6 May 2026: "we're fine with 60 days going forward."

Invoice BPC-8812, invoice date 1 September 2026, $3,260.00, quarterly site treatments.
""",
[("1 October 2026", "30 days after the invoice date."),
 ("15 October 2026", "44 days after the invoice date."),
 ("16 October 2026", "45 days after the invoice date."),
 ("31 October 2026", "60 days after the invoice date."),
 ("1 November 2026", "61 days after the invoice date.")],
"16 October 2026", 3, ordered=True,
twin=T([("Amendment No. 1 (unsigned draft, circulated 4 May 2026)", "Amendment No. 1 (signed by both parties on 4 May 2026)")], "31 October 2026")),

# ------------------------------------------------------------------ pr07
# why: translation is a service -> P-card excluded (services) -> purchase order;
# no personal data -> no privacy review. Twin: documents contain customer names and
# addresses -> personal data -> privacy review then PO.
C("pr07", "Through which buying channel must this request go?",
"""
Halvard Group — How to buy (Purchasing guide, 2026)

- Catalogue: items listed in the punch-out catalogue must be bought there.
- P-card: goods not in the catalogue, under $2,500 per transaction. Never for services, travel or software.
- Purchase order: goods of $2,500 or more, and all services of any value.
- Travel portal: flights, hotels, rail and car hire.
- Privacy review, then purchase order: any service where the supplier will receive or process personal data about customers or staff.
- Petty cash: sundries under $50, receipts required.

Request from Nils Aarden (Marketing), 22 September 2026
"We need a freelance translator (Irma Kovač, sole trader) to translate our autumn product brochure and three internal marketing one-pagers into Czech and Polish. Quote is $1,800 flat. The documents are internal marketing copy with no personal data. Can I just put it on my P-card? It's under the limit."
Catalogue search for "translation": no results.
""",
[("Catalogue", "order through the punch-out catalogue."),
 ("P-card", "pay with the requester's purchasing card."),
 ("Purchase order", "raise a purchase order through procurement."),
 ("Travel portal", "book through the travel portal."),
 ("Privacy review, then purchase order", "the privacy team reviews the data handling before a purchase order is raised."),
 ("Petty cash", "pay from the office float and claim with a receipt.")],
"Purchase order", 2,
twin=T([("The documents are internal marketing copy with no personal data.",
         "The documents are customer complaint letters that include names, home addresses and order histories.")],
       "Privacy review, then purchase order")),

# ------------------------------------------------------------------ pr08
# why: owner of the vendor is Dana's brother-in-law (spouse's brother) -> listed
# relative -> Dana must declare and recuse -> may not approve -> no.
# Twin: former classmate, no financial ties -> no recusal needed -> yes.
Y("pr08", "May Dana Whitlow approve this purchase herself?",
"""
Quillon Freight — Code of Conduct, section 3 (conflicts of interest)

3.1 A relative means a spouse or partner, parent, child, sibling, or the spouse of a sibling or a sibling of a spouse (in-laws).
3.2 An employee must declare, and may not request, evaluate or approve, any purchase from a business owned or run by a relative.
3.3 Friends and former colleagues do not require recusal unless the employee holds a financial interest in the business, in which case 3.2 applies.
3.4 Gifts above $75 must be logged in the gifts register.

Purchase request PR-26-1044
Approver of record: Dana Whitlow, Depot Manager, Eastgate (approval limit $25,000).
Vendor: Kellan Yard Services (sole owner: Rhys Morton). Value: $6,400 for pallet-racking inspection.
Declaration form filed by Dana on 18 September 2026: "Rhys Morton is my husband's brother. I have no shares or role in his business."
""",
[("Relative", "spouse or partner, parent, child, sibling, or an in-law as defined in 3.1."),
 ("Recusal", "the employee may not request, evaluate or approve the purchase.")],
0, 2,
twin=T([("\"Rhys Morton is my husband's brother. I have no shares or role in his business.\"",
         "\"Rhys Morton was my classmate at university. I have no shares or role in his business.\"")], 1)),

# ------------------------------------------------------------------ pr09
# why: capitalise only if unit cost >= $3,000 AND useful life > 1 year. Laptops
# $1,450 each -> below threshold -> IT equipment non-capital (not supplies).
# Twin: workstations $3,650 each, life 4 yrs -> Fixed assets - computer equipment.
C("pr09", "Which general-ledger account should this purchase be coded to?",
"""
Selcombe University — Chart of accounts guidance (extract)

1510 Fixed assets — computer equipment: individual items costing $3,000 or more per unit with a useful life of more than one year.
6120 IT equipment — non-capital: computers, monitors and peripherals below the capitalisation threshold.
6130 Software subscriptions: licences and SaaS fees.
6200 Office supplies: stationery and consumables.
6410 Repairs and maintenance: fixing existing equipment.
1400 Prepaid expenses: payments covering future periods of more than 12 months.
Note: the threshold is applied per unit, not to the invoice total. Delivery charges follow the item they relate to.

Invoice from Kovalent Systems, 17 September 2026
12 laptops at $1,450 each ($17,400 total). Useful life: 4 years.
Delivery: $180. Pre-installed operating system licence included in the unit price.
Requested by: School of Engineering teaching labs.
""",
[("1510 Fixed assets — computer equipment", "capitalised computer equipment at or above the threshold."),
 ("6120 IT equipment — non-capital", "expensed computer hardware below the threshold."),
 ("6130 Software subscriptions", "licences and SaaS fees."),
 ("6200 Office supplies", "stationery and consumables."),
 ("6410 Repairs and maintenance", "repair of existing equipment."),
 ("1400 Prepaid expenses", "prepayments for periods beyond 12 months.")],
"6120 IT equipment — non-capital", 2,
twin=T([("12 laptops at $1,450 each ($17,400 total).", "4 GPU workstations at $3,650 each ($14,600 total).")],
       "1510 Fixed assets — computer equipment")),

# ------------------------------------------------------------------ pr10
# why: notice must be RECEIVED at least 60 days before the end date (31 Dec) ->
# latest 1 Nov (31 Dec - 30 = 1 Dec, - 30 = 1 Nov). Email is not valid notice.
# Courier letter received 3 Nov -> late -> renewal not stopped -> no.
# Twin: letter received 30 Oct -> in time -> yes.
Y("pr10", "Did the customer's notice prevent the automatic renewal?",
"""
Ostrava Components — Services Agreement with Lumen Cleaning Co. (extract)

12.1 Term: 1 January 2026 to 31 December 2026.
12.2 The agreement renews automatically for 12 months unless either party gives written notice of non-renewal that is received by the other party at least 60 days before the end of the current term.
12.3 Written notice means a signed letter delivered by courier or registered post to the address in clause 20. Email is not written notice under this agreement.
12.4 Price increases on renewal are capped at 4%.

Correspondence log (Ostrava Facilities)
- 28 October 2026: email sent to Lumen's account manager: "We will not renew in 2027."
- 29 October 2026: signed non-renewal letter sent by courier to Lumen's clause-20 address.
- 3 November 2026: courier confirmation — letter received and signed for by Lumen reception.
- 6 November 2026: Lumen replies that the contract "has already renewed for 2027."
""",
[("Valid notice", "a signed letter by courier or registered post, received at least 60 days before the term ends."),
 ("Automatic renewal", "the agreement continues for 12 more months when no valid notice is received in time.")],
0, 3,
twin=T([("- 3 November 2026: courier confirmation", "- 30 October 2026: courier confirmation")], 1)),

# ------------------------------------------------------------------ pr11
# why: Dunmere late -> excluded. Beldon tech 58 < 60 -> disqualified. Lowest compliant
# price = Corrin 110,000. Arvo: price 110/120x100 = 91.67 x .40 = 36.67; tech 82 x .35
# = 28.70; delivery 70 x .15 = 10.50; sust 60 x .10 = 6.00 -> 81.87. Corrin: 100 x .40
# = 40.00; 75 x .35 = 26.25; 85 x .15 = 12.75; 90 x .10 = 9.00 -> 88.00 -> Corrin wins.
# Twin: Corrin tech 59 -> disqualified; Arvo only compliant -> Arvo (price 100: 40 +
# 28.70 + 10.50 + 6.00 = 85.20).
C("pr11", "Which bidder should be awarded the contract under the evaluation rules?",
"""
Marrowby Health Trust — Tender MHT-2026-17 (patient transport scheduling software)

Evaluation rules
- Bids received after the deadline (12:00, 4 September 2026) are excluded.
- A bid scoring below 60 on Technical is disqualified.
- Price score = (lowest price among bids that are not excluded or disqualified) / (bid price) x 100.
- Weighted total = Price 40% + Technical 35% + Delivery 15% + Sustainability 10%.
- Award to the highest weighted total. If no bid remains, re-tender.

Bid register (scores out of 100)
| Bidder | Received | Price | Technical | Delivery | Sustainability |
| Arvo Systems | 3 Sep 16:20 | $120,000 | 82 | 70 | 60 |
| Beldon Tech | 4 Sep 09:05 | $100,000 | 58 | 90 | 80 |
| Corrin Ltd | 4 Sep 11:48 | $110,000 | 75 | 85 | 90 |
| Dunmere Group | 4 Sep 12:07 | $95,000 | 88 | 90 | 85 |
""",
[("Arvo Systems", "award to Arvo Systems."),
 ("Beldon Tech", "award to Beldon Tech."),
 ("Corrin Ltd", "award to Corrin Ltd."),
 ("Dunmere Group", "award to Dunmere Group."),
 ("re-tender", "no bid can be awarded; run the tender again.")],
"Corrin Ltd", 3,
twin=T([("| $110,000 | 75 |", "| $110,000 | 59 |")], "Arvo Systems")),

# ------------------------------------------------------------------ pr12
# why: same need, same supplier, same day -> one transaction: 70 + 60 = 130 > 100 ->
# over the petty-cash cap -> cannot be paid as submitted -> no.
# Twin: second receipt $25 -> 95 <= 100 -> yes.
Y("pr12", "Can this petty-cash claim be reimbursed as submitted?",
"""
Tanager Foods — Petty cash rules (site offices)

- Maximum $100.00 per transaction, receipts required.
- Purchases from the same supplier on the same day for the same need count as one transaction; splitting a purchase to stay under the limit is not allowed.
- Alcohol, gift cards and personal items are never reimbursed from petty cash.
- Claims must be submitted within 30 days of purchase.

Claim PC-0931, Brennan Street office, submitted 12 October 2026 by Hana Petrov
Receipt 1: 9 October 2026, Pastry Loft, $70.00 — sandwich platters for the 9 October board meeting.
Receipt 2: 9 October 2026, Pastry Loft, $60.00 — fruit bowls and juice for the 9 October board meeting.
Note: "Paid at the counter in two goes because the platters were ready first."
""",
[("Transaction", "all purchases from one supplier on one day for the same need."),
 ("Petty-cash limit", "at most $100.00 per transaction.")],
0, 2,
twin=T([("Pastry Loft, $60.00", "Pastry Loft, $25.00")], 1)),

# ------------------------------------------------------------------ pr13
# why: bank details on the invoice differ from the vendor master -> rule 1 overrides
# entity routing -> Vendor Master team. Twin: bank details match -> EUR invoice to
# Halvard Europe B.V. with PO -> AP-EU.
C("pr13", "Which queue should this incoming invoice be sent to?",
"""
Halvard Group — Invoice intake routing (shared service centre)

Rule 1 (checked first): if the bank details on an invoice differ from the vendor master record, send the invoice to the Vendor Master team for call-back verification. Do not route it anywhere else until verified.
Rule 2: invoices without a valid PO number go to the Requester Confirmation queue.
Rule 3: otherwise route by billed entity:
  Halvard Inc. (USD) -> AP-US
  Halvard Europe B.V. (EUR) -> AP-EU
  Halvard UK Ltd (GBP) -> AP-UK
Rule 4: invoices that mention a legal claim or lawsuit are copied to Legal (in addition to the queue above).

Incoming invoice (scanned 24 September 2026)
Supplier: Veltmann Logistik GmbH (vendor ID 200417).
Billed entity: Halvard Europe B.V. Currency: EUR. Amount: EUR 14,820.00.
PO number: 4700-88213 (valid, open).
Bank details on invoice: IBAN ending 7731 (vendor master record: IBAN ending 2210).
Cover note: "Please note our new bank account for all future payments."
""",
[("AP-US", "accounts payable team for Halvard Inc."),
 ("AP-EU", "accounts payable team for Halvard Europe B.V."),
 ("AP-UK", "accounts payable team for Halvard UK Ltd."),
 ("Requester Confirmation", "invoices without a valid PO, sent to the requester to confirm."),
 ("Vendor Master team", "verification of changed supplier bank details by call-back."),
 ("Legal", "invoices mentioning legal claims."),
 ("none of these", "no rule routes the invoice.")],
"Vendor Master team", 2,
twin=T([("Bank details on invoice: IBAN ending 7731 (vendor master record: IBAN ending 2210).",
         "Bank details on invoice: IBAN ending 2210 (vendor master record: IBAN ending 2210)."),
        ("Cover note: \"Please note our new bank account for all future payments.\"",
         "Cover note: \"Thank you for your business.\"")], "AP-EU")),

# ------------------------------------------------------------------ pr14
# why: term 48 months > 36 -> General Counsel signs instead of the value-based
# signatory. Twin: 36 months (not exceeding 36), value $30,000 -> band $25,000.01-
# $150,000 -> Finance Director.
C("pr14", "Who must sign this contract?",
"""
Selcombe University — Contract signing authority (Council resolution 2025/14)

Value-based signatories (total value over the full term, excluding tax):
- up to $25,000: Procurement Manager
- $25,000.01 to $150,000: Finance Director
- over $150,000: Vice-Chancellor
Overrides (the override signatory signs instead of the value-based signatory):
- Any contract with a term exceeding 36 months: General Counsel.
- Any contract with uncapped liability or indemnity: General Counsel.
Research grants and sponsored-research agreements are signed by the Research Office regardless of value.

Contract for signature — CS-2026-221
Counterparty: Brookmere Grounds Ltd. Subject: campus tree survey and maintenance.
Term: 48 months from 1 November 2026.
Total contract value: $40,000 (fixed $10,000 per year).
Liability: capped at the total contract value. Indemnity: capped at $250,000.
""",
[("Procurement Manager", "signs contracts up to $25,000."),
 ("Finance Director", "signs contracts from $25,000.01 to $150,000."),
 ("Vice-Chancellor", "signs contracts over $150,000."),
 ("General Counsel", "signs contracts caught by an override."),
 ("Research Office", "signs research grants and sponsored research.")],
"General Counsel", 2,
twin=T([("Term: 48 months from 1 November 2026.", "Term: 36 months from 1 November 2026."),
        ("Total contract value: $40,000", "Total contract value: $30,000")], "Finance Director")),

# ------------------------------------------------------------------ pr15
# why: due 15 Sep; grace 5 calendar days -> on time through 20 Sep. Paid 19 Sep ->
# on time -> no interest. Twin: paid 22 Sep -> 7 days after due -> late -> interest.
Y("pr15", "Is the supplier entitled to late-payment interest on this invoice?",
"""
Quillon Freight — Supplier payment charter

- Undisputed invoices are paid by their due date.
- A grace period of 5 calendar days after the due date applies; a payment made on or before the fifth day after the due date is treated as on time.
- Late payments (after the grace period) on undisputed invoices attract interest at 8% a year from the due date.
- Disputed invoices do not attract interest while the dispute is open.

Supplier claim letter from Garnet Tyres, 1 October 2026
"Invoice GT-5521 for $12,300 was due on 15 September 2026. Your remittance shows payment on 19 September 2026. We are claiming late-payment interest under your charter."
AP record: GT-5521 — no dispute raised; paid 19 September 2026 (bank value date).
""",
[("Grace period", "5 calendar days after the due date during which payment counts as on time."),
 ("Late-payment interest", "8% a year, due only on undisputed invoices paid after the grace period.")],
0, 2,
twin=T([("Your remittance shows payment on 19 September 2026.", "Your remittance shows payment on 22 September 2026."),
        ("paid 19 September 2026 (bank value date)", "paid 22 September 2026 (bank value date)")], 1)),

# ------------------------------------------------------------------ pr16
# why: class set by the longest single segment's scheduled time: 4h40 and 7h15 ->
# 7h15 -> 6-10 hours band -> premium economy. Director grade gets no uplift.
# Twin: second segment 10h25 -> over 10 hours -> business.
C("pr16", "Which cabin class does the travel policy allow for this trip?",
"""
Tanager Foods — Travel policy, section 2 (air travel)

2.1 Cabin class is set by the scheduled flight time of the longest single segment on the itinerary (connections and layovers are not added together):
  - under 6 hours: economy
  - 6 hours to 10 hours inclusive: premium economy
  - over 10 hours: business
2.2 First class is never reimbursed.
2.3 Executive Committee members may fly business on any segment over 4 hours.
2.4 Hotel limits are in section 3.

Travel request TR-9920
Traveller: Colm Dresner, Director of Sourcing (not on the Executive Committee).
Itinerary: Brennport -> Halstad, 4 h 40 min; 3 h 05 min layover; Halstad -> Qarim Bay, 7 h 15 min.
Purpose: supplier audits, 12-16 October 2026.
Traveller comment: "Total journey is almost 15 hours door to door, so I've requested business."
""",
[("economy", "economy class on all segments."),
 ("premium economy", "premium economy class."),
 ("business", "business class."),
 ("first", "first class."),
 ("CFO exception needed", "the trip falls outside the policy and needs a CFO exception.")],
"premium economy", 2,
twin=T([("Halstad -> Qarim Bay, 7 h 15 min", "Halstad -> Qarim Bay, 10 h 25 min")], "business")),

# ------------------------------------------------------------------ pr17
# why: emergency purchase $12,300 <= $15,000, safety-critical -> allowed, but must be
# ratified within 2 business days after the purchase day. Purchase Fri 18 Sep ->
# business days Mon 21, Tue 22 -> deadline Tue 22 Sep. Submitted Wed 23 Sep -> late ->
# refer to Internal Audit. Twin: submitted Tue 22 Sep -> ratify.
C("pr17", "What should the Finance Controller do with this ratification request?",
"""
Ostrava Components — Emergency purchasing procedure EP-1

1. A site manager may buy goods or services up to $15,000 without prior approval when the purchase is needed to remove an immediate safety risk.
2. The site manager must submit a ratification request within 2 business days after the day of purchase (Monday to Friday; there are no public holidays in the period covered here).
3. Requests received in time that meet rule 1 are ratified by the Finance Controller.
4. Requests received after the deadline are referred to Internal Audit, whatever the amount.
5. Purchases above $15,000 or not safety-related are rejected and handled as policy breaches.

Ratification request ER-0412
Site: Ostrava Components, Kelby plant. Site manager: Anouk Ferris.
Purchase: replacement coolant pump for the stamping press after a leak made the floor unsafe; $12,300 from Haldane Pumps.
Purchase date: Friday 18 September 2026.
Ratification request received by Finance: Wednesday 23 September 2026.
""",
[("ratify", "the Finance Controller approves the emergency purchase after the event."),
 ("refer to Internal Audit", "the request is sent to Internal Audit for review."),
 ("reject as a policy breach", "the purchase did not qualify as an emergency purchase."),
 ("ratify with a late-submission note", "ratify the purchase and record on file that the request was late."),
 ("return for more information", "the request lacks facts needed to decide.")],
"refer to Internal Audit", 2,
twin=T([("received by Finance: Wednesday 23 September 2026", "received by Finance: Tuesday 22 September 2026")], "ratify")),

# ------------------------------------------------------------------ pr18
# why: the payment covers 1 Oct 2026 - 31 Mar 2028 = 18 months, i.e. a future period of
# more than 12 months -> 1400 Prepaid expenses (guidance note). Twin: 12-month cover
# (1 Oct 2026 - 30 Sep 2027) -> not more than 12 months -> 6130 Software subscriptions.
C("pr18", "Which account should the invoice be coded to under the chart-of-accounts guidance?",
"""
Quillon Freight — Chart of accounts guidance (AP coders)

1510 Fixed assets — computer equipment: hardware items of $3,000 or more per unit.
1520 Fixed assets — vehicles: trucks, vans and trailers.
1400 Prepaid expenses: any single payment that covers a future service period of more than 12 months. Takes precedence over the expense accounts below.
6120 IT equipment — non-capital: hardware below $3,000 per unit.
6130 Software subscriptions: licences, SaaS and software support for periods of 12 months or less.
6140 IT consultancy: implementation and advisory services billed by time.
6200 Office supplies: stationery and consumables.
6310 Vehicle maintenance: servicing and repair of fleet vehicles.
6320 Fuel: diesel and AdBlue.
6410 Building repairs and maintenance.
6500 Insurance premiums.
6610 Training and conferences.

Invoice FT-55091 from Telvara Software
Description: "Depot Manager Pro — enterprise licence and support, service period 1 October 2026 to 31 March 2028."
Amount: $46,800, single payment due 15 October 2026.
Requester: Head of Depot Operations.
""",
[("1510 Fixed assets — computer equipment", "capital hardware."),
 ("1520 Fixed assets — vehicles", "capital vehicles."),
 ("1400 Prepaid expenses", "single payments covering more than 12 months of future service."),
 ("6120 IT equipment — non-capital", "hardware below the threshold."),
 ("6130 Software subscriptions", "software, SaaS and support for 12 months or less."),
 ("6140 IT consultancy", "time-billed IT services."),
 ("6200 Office supplies", "stationery and consumables."),
 ("6310 Vehicle maintenance", "fleet servicing and repairs."),
 ("6320 Fuel", "diesel and AdBlue."),
 ("6410 Building repairs and maintenance", "repairs to buildings."),
 ("6500 Insurance premiums", "insurance costs."),
 ("6610 Training and conferences", "courses and events.")],
"1400 Prepaid expenses", 3,
twin=T([("service period 1 October 2026 to 31 March 2028", "service period 1 October 2026 to 30 September 2027"),
        ("Amount: $46,800", "Amount: $31,200")], "6130 Software subscriptions")),
]
