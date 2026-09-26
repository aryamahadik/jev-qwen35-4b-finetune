"""reason_c / billing, subscriptions, credit and collections (Nimbrel Cloud,
Carrowfell Energy, Linkwave Broadband, Ashgrove Credit Union, Ferrocart SaaS)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ bl01
# why: cycle 1-30 Sep = 30 days. Upgrade on 21 Sep; remaining days counted including
# the upgrade day: 21..30 = 10 days. Charge = (60 - 30) x 10/30 = $10.00.
# Twin: upgrade 25 Sep -> 25..30 = 6 days -> 30 x 6/30 = $6.00.
C("bl01", "What pro-rated charge should appear for the plan upgrade?",
"""
Nimbrel Cloud — Billing FAQ (internal version for support agents)

Upgrades take effect immediately. We charge the price difference between the new and old plan for the rest of the current billing cycle: (new monthly price - old monthly price) x (days remaining / days in the cycle). Days remaining include the day of the upgrade.
Downgrades take effect at the next cycle; no credit is given for the current cycle.
Add-on storage is billed separately at the end of the cycle.

Ticket NC-44102
Customer: Harlow & Finch Design. Billing cycle: 1-30 September 2026 (30 days).
Old plan: Team, $30 per month. New plan: Studio, $60 per month.
Upgrade performed: 21 September 2026, 16:05.
Customer asks: "What exactly will the extra charge be this month?"
""",
[("$0.00", "no extra charge this cycle."), ("$6.00", "six dollars."), ("$9.00", "nine dollars."),
 ("$10.00", "ten dollars."), ("$11.00", "eleven dollars."), ("$20.00", "twenty dollars."), ("$30.00", "thirty dollars.")],
"$10.00", 2,
twin=T([("Upgrade performed: 21 September 2026", "Upgrade performed: 25 September 2026")], "$6.00")),

# ------------------------------------------------------------------ bl02
# why: fee applies only if payment is received MORE than 5 days after the due date.
# Due 10 Sep; received 16 Sep = 6 days after -> late fee -> yes.
# Twin: received 15 Sep = 5 days after -> not more than 5 -> no.
Y("bl02", "Should a late-payment fee be charged on this invoice?",
"""
Carrowfell Energy — Business account terms, clause 8

8.1 Invoices are due on the 10th of the month following the billing month.
8.2 A late-payment fee applies if payment is received more than 5 calendar days after the due date.
8.3 A bank transfer counts as received on the date the funds reach Carrowfell's account, not the date the customer sent it.
8.4 Customers on a hardship plan are never charged late fees.

Account CE-B-20715, Tollgate Tyres Ltd (not on a hardship plan)
Invoice for August 2026 usage: $2,400.00, due 10 September 2026.
Customer's bank transfer initiated: 14 September 2026.
Funds received in Carrowfell's account: 16 September 2026.
Customer email: "We paid on the 14th, which is within your 5-day allowance."
""",
[("Received date", "the date funds reach Carrowfell's account."),
 ("Late-payment fee", "charged when payment is received more than 5 calendar days after the due date.")],
1, 2,
twin=T([("Funds received in Carrowfell's account: 16 September 2026.", "Funds received in Carrowfell's account: 15 September 2026.")], 0)),

# ------------------------------------------------------------------ bl03
# why: fee = greater of $25 or 1.5% of the overdue balance, capped at $100.
# 1.5% of 1,200 = 18 < 25 -> $25. Twin: 2,400 -> 36 > 25 -> $36.
C("bl03", "What late-payment fee should be applied?",
"""
Carrowfell Energy — Business account terms, clause 9 (fee amount)

9.1 The late-payment fee is the greater of $25.00 or 1.5% of the overdue balance, but never more than $100.00.
9.2 Only one late-payment fee is charged per invoice.
9.3 The overdue balance excludes any amount under formal dispute.
9.4 Direct-debit customers whose collection fails because of a bank error are not charged a fee if they pay within 3 days of being told.
9.5 Interest on overdue amounts (clause 10) is charged separately and does not replace the fee.

Account CE-B-31140, Marlow Street Dental (fee applies under clause 8)
Invoice for July 2026: total $1,450.00. Paid on time: $0.00.
Formal dispute open on the invoice: $250.00 (standing charge applied twice).
Overdue balance for fee purposes: $1,200.00.
Payment method: bank transfer (no direct debit on this account).
Account manager note: "Customer has been with us since 2019; first late payment."
""",
[("$0.00", "no fee."), ("$18.00", "eighteen dollars."), ("$21.75", "twenty-one dollars seventy-five."),
 ("$25.00", "twenty-five dollars."), ("$36.00", "thirty-six dollars."), ("$100.00", "one hundred dollars.")],
"$25.00", 2,
twin=T([("Invoice for July 2026: total $1,450.00.", "Invoice for July 2026: total $2,650.00."),
        ("Overdue balance for fee purposes: $1,200.00.", "Overdue balance for fee purposes: $2,400.00.")], "$36.00")),

# ------------------------------------------------------------------ bl04
# why: meter-reading dispute would go to Metering, but the customer mentions a home
# oxygen concentrator (medical device dependency) -> Priority Services Register team
# regardless. No disconnection notice. Twin: remove the device mention -> Metering.
C("bl04", "Which team should handle this customer contact?",
"""
Carrowfell Energy — Residential contact routing

- Disputed or estimated meter readings -> Metering.
- Questions about unit rates, standing charges or switching tariff -> Tariffs.
- Customer cannot afford to pay, asks for a payment plan -> Customer Assistance.
- A disconnection is scheduled within the next 5 days -> Disconnections Desk (urgent).
- Override: any contact where the customer or someone in the home depends on electrically powered medical equipment -> Priority Services Register team, whatever the reason for contact.
- Smart meter installation bookings -> Field Scheduling.

Web message, 24 September 2026, account CE-R-88210 (Nell Arbery)
"My bill for August says 'estimated' and it's nearly double last month. I took a photo of the meter on 1 September and the real reading is 40211, not the 41390 you guessed. I have to be careful with money because my dad lives with us and runs a home oxygen concentrator day and night. Please correct the bill."
Account status: no arrears, no disconnection scheduled.
""",
[("Metering", "disputed and estimated meter readings."),
 ("Tariffs", "rates, charges and tariff changes."),
 ("Customer Assistance", "affordability and payment plans."),
 ("Disconnections Desk", "disconnections scheduled within 5 days."),
 ("Priority Services Register team", "households that depend on powered medical equipment."),
 ("Field Scheduling", "smart meter installation bookings."),
 ("none of these", "no route applies.")],
"Priority Services Register team", 2,
twin=T([("I have to be careful with money because my dad lives with us and runs a home oxygen concentrator day and night.",
         "I have to be careful with money this month because the car needed repairs.")], "Metering")),

# ------------------------------------------------------------------ bl05
# why: moving home does not waive the ETF unless service is unavailable at the new
# address (coverage check shows available) and cooling-off long over -> fee payable -> yes.
# Twin: coverage check says unavailable, proof supplied -> waived -> no.
Y("bl05", "Is an early termination fee payable on this cancellation?",
"""
Linkwave Broadband — Minimum-term contracts, clause 5

5.1 Cancelling before the end of the minimum term incurs an early termination fee (ETF).
5.2 The ETF is waived if: (a) you cancel within the 14-day cooling-off period after the service goes live; or (b) you move to an address where Linkwave cannot provide service, shown by our coverage checker, and you give proof of the new address.
5.3 Moving to an address where Linkwave can provide service is not a reason to waive the ETF; you may transfer the contract instead.
5.4 Price rises: see clause 7.

Cancellation request LW-C-6612
Customer: Dario Stavros. Service live since 5 February 2025; 24-month minimum term.
Reason: moving to 3 Heron Court, Wexby on 30 September 2026. Tenancy agreement provided as proof of address.
Coverage checker result for 3 Heron Court: "Linkwave Fibre 500 available."
Customer: "I don't want to transfer, I'll pick a provider there later."
""",
[("Early termination fee", "a charge for cancelling before the minimum term ends."),
 ("ETF waiver", "cancellation in the 14-day cooling-off period, or a move to an address Linkwave cannot serve, with proof of address.")],
1, 2,
twin=T([("Coverage checker result for 3 Heron Court: \"Linkwave Fibre 500 available.\"", "Coverage checker result for 3 Heron Court: \"No Linkwave service at this address.\""),
        ("Customer: \"I don't want to transfer, I'll pick a provider there later.\"", "Customer: \"I'd have stayed with you if I could.\"")], 0)),

# ------------------------------------------------------------------ bl06
# why: monthly periods start on the 5th; term 5 Feb 2025 - 4 Feb 2027. Cancel 20 Sep
# 2026: current period 5 Sep - 4 Oct is paid in full and not counted. Remaining whole
# periods start 5 Oct, 5 Nov, 5 Dec, 5 Jan -> 4 x $12 = $48.
# Twin: cancel 20 Oct -> current 5 Oct - 4 Nov; remaining 5 Nov, 5 Dec, 5 Jan -> $36.
C("bl06", "How much is the early termination fee?",
"""
Linkwave Broadband — ETF calculation (billing team guide)

ETF = $12 x the number of whole monthly billing periods left in the minimum term after the period in which the cancellation takes effect.
The billing period in which the cancellation takes effect is charged in full and is not counted in the ETF.
Billing periods begin on the same day of the month as the service live date.

Account LW-40022, Anouk Tessier
Service live: 5 February 2025. Minimum term: 24 months (last period 5 January 2027 - 4 February 2027).
Cancellation takes effect: 20 September 2026.
Discount received on sign-up: $50 (not clawed back under current terms).
""",
[("$0.00", "no fee."), ("$36.00", "thirty-six dollars."), ("$48.00", "forty-eight dollars."),
 ("$60.00", "sixty dollars."), ("$98.00", "ninety-eight dollars.")],
"$48.00", 3,
twin=T([("Cancellation takes effect: 20 September 2026.", "Cancellation takes effect: 20 October 2026.")], "$36.00")),

# ------------------------------------------------------------------ bl07
# why: open >= 6 months: 3 Mar -> 3 Sep 2026, request 25 Sep -> ok. June payment was
# 12 days late, which is not "missed" (> 30 days). Income verified. -> eligible -> yes.
# Twin: 34 days late -> missed payment in last 12 months -> no.
Y("bl07", "Is the member eligible for a credit limit increase?",
"""
Ashgrove Credit Union — Credit card limit increases (lending guide 4.3)

A member may be offered a limit increase when ALL of these are true on the request date:
 1. The card account has been open for at least 6 months.
 2. No missed payment in the last 12 months. A payment counts as missed only if it was more than 30 days late; payments 1-30 days late are recorded as "late" but not "missed".
 3. Income has been verified in the last 12 months.
 4. The account is not over its current limit.
Balance transfers are handled separately (guide 4.5).

Request CL-7710 (25 September 2026)
Member: Oluwaseun Adebayo. Card account opened: 3 March 2026. Current limit $2,000; balance $1,340.
Payment history: March-September all on time except June (paid 12 days after the due date).
Income verified: 1 March 2026 (payslips).
""",
[("Missed payment", "a payment more than 30 days late."),
 ("Limit-increase eligibility", "all four conditions in guide 4.3 are met on the request date.")],
1, 2,
twin=T([("except June (paid 12 days after the due date)", "except June (paid 34 days after the due date)")], 0)),

# ------------------------------------------------------------------ bl08
# why: monthly income 54,000 / 12 = 4,500. Debts 1,450 + new payment 380 = 1,830.
# DTI = 1,830 / 4,500 = 40.7% -> 36-43 band -> approve with conditions. Score 688 ok.
# Twin: income 63,000 / 12 = 5,250 -> 1,830 / 5,250 = 34.9% <= 36 -> approve.
C("bl08", "What decision does the lending policy give for this application?",
"""
Ashgrove Credit Union — Personal loan decision matrix

Step 1. Missing income documents -> request more information.
Step 2. Self-employed applicants -> refer to underwriter.
Step 3. Credit score below 580 -> decline.
Step 4. Debt-to-income (DTI) = total monthly debt payments INCLUDING the new loan payment / gross monthly income.
  DTI up to 36% -> approve.
  DTI above 36% and up to 43% -> approve with conditions (co-signer or reduced amount).
  DTI above 43% -> decline.
Car-loan and mortgage rates are published separately.

Application PL-26-3310
Applicant: Hedda Sorensen, employed (hospital pharmacist). Payslips and employer letter: received.
Gross annual salary: $54,000.
Existing monthly debt payments: $1,450 (mortgage $1,210, car $240).
Requested loan: $15,000 over 48 months; monthly payment $380.
Credit score: 688.
""",
[("approve", "approve the loan as requested."),
 ("approve with conditions", "approve only with a co-signer or a reduced amount."),
 ("decline", "decline the application."),
 ("request more information", "income documents are missing."),
 ("refer to underwriter", "self-employed applicants are reviewed by an underwriter.")],
"approve with conditions", 3,
twin=T([("Gross annual salary: $54,000.", "Gross annual salary: $63,000.")], "approve")),

# ------------------------------------------------------------------ bl09
# why: max 2 payment holidays over the loan term; 2 already taken -> not eligible -> no.
# Six on-time payments since last holiday and no arrears are met but irrelevant.
# Twin: 1 taken -> eligible -> yes.
Y("bl09", "Can the member take a payment holiday in November?",
"""
Ashgrove Credit Union — Loan payment holidays

- A payment holiday lets a member skip one monthly repayment; interest continues to accrue.
- Eligibility: (1) the loan is not in arrears; (2) the last 6 monthly repayments were made on time; (3) no more than 2 payment holidays in total over the life of the loan (the requested one included).
- Requests must be made at least 10 days before the repayment date.

Request PH-2211 (received 20 October 2026)
Member: Wendell Price. Loan: $12,000, 60 months, started July 2023.
Arrears: none. Last 6 repayments (May-October 2026): all on time.
Payment holidays taken so far: 2 (December 2023 and August 2025).
Requested holiday: the 5 November 2026 repayment.
""",
[("Payment holiday", "skipping one monthly repayment while interest accrues."),
 ("Holiday limit", "no more than 2 payment holidays over the life of the loan, including the one requested.")],
0, 2,
twin=T([("Payment holidays taken so far: 2 (December 2023 and August 2025).", "Payment holidays taken so far: 1 (August 2025).")], 1)),

# ------------------------------------------------------------------ bl10
# why: closed account overrides the open-account bands: credit >= $10 on a closed
# account -> cheque. $86 -> cheque. Twin: account open -> $10-$500 band -> refund
# to original payment method.
C("bl10", "How should the credit balance on this account be handled?",
"""
Ferrocart SaaS — Credit balance procedure (finance operations)

Closed accounts (checked first): credits of $10.00 or more are refunded by cheque to the billing address; credits under $10.00 are written off.
Open accounts:
 - credit under $10.00: keep as account credit for the next invoice;
 - $10.00 to $500.00: refund automatically to the original payment method;
 - over $500.00: needs Finance Manager approval before refund.
Credits created by a chargeback are never refunded (see chargeback policy).

Account FC-2291, Marisol Ortega Studio
Account status: closed on 31 August 2026 (customer cancelled).
Credit balance: $86.00 from an annual plan overpayment (not a chargeback).
Original payment method: Visa ending 4410 (still valid).
""",
[("keep as account credit", "leave the credit on the account for the next invoice."),
 ("refund to original payment method", "refund automatically to the card or account used."),
 ("Finance Manager approval", "hold the refund until a Finance Manager approves it."),
 ("refund by cheque", "post a cheque to the billing address."),
 ("write off", "remove the credit with no refund.")],
"refund by cheque", 2,
twin=T([("Account status: closed on 31 August 2026 (customer cancelled).", "Account status: open (renewed 31 August 2026).")],
       "refund to original payment method")),

# ------------------------------------------------------------------ bl11
# why: 8 extra seats (58 - 50) added in August; billed for the remaining contract
# months counting the month of addition: Aug, Sep, Oct, Nov, Dec = 5.
# 8 x $20 x 5 = $800. Twin: added in October -> Oct, Nov, Dec = 3 -> $480.
C("bl11", "What is the true-up charge for the additional seats?",
"""
Ferrocart SaaS — Enterprise order form OF-2026-118 (Keswick Freight)

Term: 1 January 2026 to 31 December 2026. Committed seats: 50 at $20 per seat per month, prepaid annually.
True-up: seats above the committed number are billed at the same unit price for each remaining month of the term, counting the month in which they were added as a full month. Seats removed later in the term are not credited.
Support: Premier, included.

Seat usage report
Jan-Jul 2026: 50 active seats.
August 2026: 8 seats added (58 active).
September-December 2026: 58 active seats (no change).
Quarterly true-up invoice being prepared on 1 October 2026 for all seats added so far.
""",
[("$0.00", "no true-up charge."), ("$480.00", "four hundred and eighty dollars."), ("$640.00", "six hundred and forty dollars."),
 ("$800.00", "eight hundred dollars."), ("$960.00", "nine hundred and sixty dollars."), ("$1,920.00", "one thousand nine hundred and twenty dollars.")],
"$800.00", 3,
twin=T([("August 2026: 8 seats added (58 active).\nSeptember-December 2026: 58 active seats (no change).\nQuarterly true-up invoice being prepared on 1 October 2026 for all seats added so far.",
         "August-September 2026: 50 active seats.\nOctober 2026: 8 seats added (58 active), remaining at 58 to year end.\nTrue-up invoice being prepared on 1 November 2026 for all seats added so far.")], "$480.00")),

# ------------------------------------------------------------------ bl12
# why: scheduled maintenance announced >= 5 days ahead is excluded. August = 31 days =
# 44,640 min. Unplanned 50 min -> uptime = 1 - 50/44,640 = 99.888% < 99.9% -> credit.
# Claim 25 Sep, within 30 days after 31 Aug (deadline 30 Sep) -> yes.
# Twin: unplanned 40 min -> 99.910% >= 99.9 -> no credit -> no.
Y("bl12", "Is the customer entitled to a service credit for August 2026?",
"""
Nimbrel Cloud — Service Level Agreement (Business tier)

- Monthly uptime = 1 - (unplanned downtime minutes / total minutes in the month).
- Scheduled maintenance announced at least 5 days in advance is not downtime.
- Uptime below 99.9%: 10% service credit. Uptime below 99.0%: 25% service credit.
- The customer must claim within 30 days after the end of the affected month.

Service credit claim SC-0831, Rennet & Ash Cheesemakers, submitted 25 September 2026
Nimbrel incident log for the customer's region, August 2026:
 - 9 August: scheduled maintenance, 20 minutes (announced 2 August).
 - 17 August: unplanned outage, 50 minutes (storage controller failure).
No other incidents.
""",
[("Unplanned downtime", "outage minutes that are not announced scheduled maintenance."),
 ("Service credit", "10% if monthly uptime is below 99.9%, 25% if below 99.0%, claimed within 30 days after the month ends.")],
1, 3,
twin=T([("unplanned outage, 50 minutes", "unplanned outage, 40 minutes")], 0)),

# ------------------------------------------------------------------ bl13
# why: June = 30 days = 43,200 min. 99.0% allows 432 min. Unplanned 480 min -> uptime
# 98.89% < 99.0% -> 25% of $3,200 = $800.
# Twin: 400 min -> 99.07% (below 99.9, not below 99.0) -> 10% -> $320.
C("bl13", "What service credit is due for June?",
"""
Nimbrel Cloud — Service Level Agreement (Enterprise tier)

- Monthly uptime = 1 - (unplanned downtime minutes / total minutes in the month).
- Uptime below 99.9%: credit 10% of that month's fee. Below 99.0%: 25%. Below 95.0%: 50%.
- Credits are applied to the next invoice and are the customer's only remedy for downtime.
- Claims must be made within 30 days after the end of the affected month (this claim was on time).

Account: Gallowtree Games (Enterprise tier). Monthly fee: $3,200.
June 2026 incident log (all unplanned):
 - 4 June: database failover, 180 minutes.
 - 19 June: network partition, 300 minutes.
""",
[("$0.00", "no credit."), ("$320.00", "three hundred and twenty dollars."),
 ("$800.00", "eight hundred dollars."), ("$1,600.00", "one thousand six hundred dollars."), ("$3,200.00", "the whole monthly fee.")],
"$800.00", 3, ordered=True,
twin=T([("network partition, 300 minutes", "network partition, 220 minutes")], "$320.00")),

# ------------------------------------------------------------------ bl14
# why: response deadline = 20 calendar days after the notification date. Notified
# 2 Sep -> deadline 22 Sep. Sent 21 Sep -> in time -> yes.
# Twin: sent 23 Sep -> late -> no.
Y("bl14", "Did the merchant respond to the chargeback in time?",
"""
Ferrocart Payments — Merchant chargeback guide

- When a cardholder disputes a payment, we notify the merchant by email. The notification date is the date of that email.
- The merchant must upload its response and evidence no later than 20 calendar days after the notification date.
- Responses received after the deadline are not sent to the card issuer and the dispute is lost.
- Evidence should include proof of delivery and the customer's order confirmation.

Dispute DP-50228
Merchant: Tidewell Candles. Payment: $148.00, order 30112.
Notification email sent: 2 September 2026.
Merchant response uploaded: 21 September 2026, with courier proof of delivery and order confirmation.
""",
[("Response deadline", "20 calendar days after the notification date."),
 ("In time", "the response was uploaded on or before the deadline.")],
1, 2,
twin=T([("Merchant response uploaded: 21 September 2026", "Merchant response uploaded: 23 September 2026")], 0)),

# ------------------------------------------------------------------ bl15
# why: no payment plan, no dispute. Due 15 Jun; 20 Sep: 15 Jun -> 15 Jul 30 days,
# -> 15 Aug 31 (61), -> 15 Sep 31 (92), +5 = 97 days past due -> over 90 -> agency.
# Twin: due 15 Jul -> 31 + 31 + 5 = 67 -> 61-90 -> final demand.
C("bl15", "Which collections stage should the account be placed in on 20 September 2026?",
"""
Carrowfell Energy — Collections stages (commercial accounts)

Checked first:
 - Account with an active payment plan -> Payment Plan Monitoring.
 - Balance under formal dispute -> Dispute Hold.
Otherwise by days past the invoice due date:
 - 1-30 days: Reminder.
 - 31-60 days: Second Notice (late fee applies).
 - 61-90 days: Final Demand.
 - over 90 days: Collection Agency referral.
Days past due are calendar days counted from the day after the due date; the stage is set by the oldest unpaid invoice.
Residential accounts follow the separate vulnerability-first procedure.

Account CE-B-40418, Halsey Joinery
Oldest unpaid invoice: $3,870.00, due 15 June 2026.
Payment plan: none. Dispute: none raised.
Contact history: two reminder emails, one phone call (no answer).
""",
[("Reminder", "1-30 days past due."), ("Second Notice", "31-60 days past due."),
 ("Final Demand", "61-90 days past due."), ("Collection Agency referral", "more than 90 days past due."),
 ("Payment Plan Monitoring", "accounts with an active payment plan."), ("Dispute Hold", "accounts with a balance under formal dispute.")],
"Collection Agency referral", 2,
twin=T([("due 15 June 2026", "due 15 July 2026")], "Final Demand")),

# ------------------------------------------------------------------ bl16
# why: precedence: signed order form > price list > renewal notice. Order form locks
# $18,000 for the first two renewal terms; this is the 2nd renewal -> $18,000, not
# $21,000 -> no. Twin: lock covers the first renewal only -> 2nd renewal at current
# list price $21,000 -> yes.
Y("bl16", "Should this renewal be invoiced at $21,000?",
"""
Ferrocart SaaS — Renewal pricing check (deal desk)

Precedence for renewal pricing: (1) a price lock in the signed order form; (2) the current published price list; (3) the amount printed on the automatic renewal notice, which is only a template estimate.

Customer: Brightmoor Veterinary Group
Signed order form OF-2024-077: initial term 1 Nov 2024 - 31 Oct 2025 at $18,000 per year. Clause 4: "The annual fee of $18,000 is locked for the first two renewal terms."
Renewal history: first renewal 1 Nov 2025 - 31 Oct 2026 invoiced at $18,000.
Upcoming renewal: 1 Nov 2026 - 31 Oct 2027 (second renewal term).
Current published price list for the same package: $21,000 per year.
Automatic renewal notice sent 1 September 2026 shows: $21,000.
""",
[("Price lock", "a signed order-form clause fixing the fee for stated renewal terms."),
 ("Renewal price", "the fee set by the highest-precedence source that covers the renewal term.")],
0, 3,
twin=T([("\"The annual fee of $18,000 is locked for the first two renewal terms.\"", "\"The annual fee of $18,000 is locked for the first renewal term.\"")], 1)),

# ------------------------------------------------------------------ bl17
# why: exemption certificate expired 31 Aug; invoice dated 15 Sep -> tax applies.
# Credit applied before tax: (5,000 - 300) x 1.08 = 4,700 x 1.08 = $5,076.00.
# Twin: certificate valid to 31 Dec 2026 -> exempt -> $4,700.00.
C("bl17", "What is the correct total for this invoice?",
"""
Ferrocart SaaS — Invoicing rules (US customers)

1. Promotional credits are deducted from the subtotal before sales tax is calculated.
2. Sales tax at the customer's local rate is added unless the customer holds a tax-exemption certificate that is valid on the invoice date.
3. Late fees are billed on a separate invoice.
4. Rounding: to the nearest cent.
5. Multi-year prepayments are invoiced in full on the first invoice date.
6. Purchase-order numbers supplied by the customer must be printed on the invoice.

Invoice draft INV-26-9140
Customer: Pinecrest School District. Invoice date: 15 September 2026.
Subtotal (licences): $5,000.00. Promotional credit: $300.00.
Local sales tax rate: 8%.
Customer PO number: PSD-26-1180 (printed).
Tax-exemption certificate on file: TX-EX-4471, valid 1 September 2025 to 31 August 2026.
""",
[("$4,700.00", "four thousand seven hundred dollars."), ("$5,000.00", "five thousand dollars."),
 ("$5,076.00", "five thousand and seventy-six dollars."), ("$5,100.00", "five thousand one hundred dollars."),
 ("$5,400.00", "five thousand four hundred dollars.")],
"$5,076.00", 3,
twin=T([("valid 1 September 2025 to 31 August 2026", "valid 1 September 2025 to 31 December 2026")], "$4,700.00")),

# ------------------------------------------------------------------ bl18
# why: invoice Fri 18 Dec 2026; count business days after the invoice date, skipping
# weekends and the listed holidays (Fri 25 Dec, Mon 28 Dec, Fri 1 Jan):
# Mon 21 (1), Tue 22 (2), Wed 23 (3), Thu 24 (4), Tue 29 (5), Wed 30 (6), Thu 31 (7),
# Mon 4 Jan (8), Tue 5 Jan (9), Wed 6 Jan (10) -> due Wed 6 Jan 2027.
# Twin: 28 Dec not a holiday -> 21,22,23,24,28,29,30,31,4 Jan,5 Jan -> Tue 5 Jan 2027.
C("bl18", "By which date must the payment be received?",
"""
Carrowfell Energy — Trade supplier terms (Harwen region), clause 3

3.1 Payment is due within 10 business days after the invoice date.
3.2 Business days are Monday to Friday, excluding public holidays in the Harwen region. The invoice date itself is not counted.
3.3 Public holidays in the Harwen region, December 2026 - January 2027: Friday 25 December; Monday 28 December (substitute day for Boxing Day); Friday 1 January.
3.4 Invoices under $100 are consolidated and billed quarterly.

Invoice CE-T-99014 to Harwen Pipe & Valve
Invoice date: Friday 18 December 2026. Amount: $6,215.40.
Customer asked: "Our finance office is closed 24 December - 4 January. What is the real deadline?"
""",
[("Wednesday 30 December 2026", "30 December 2026."),
 ("Thursday 31 December 2026", "31 December 2026."),
 ("Monday 4 January 2027", "4 January 2027."),
 ("Tuesday 5 January 2027", "5 January 2027."),
 ("Wednesday 6 January 2027", "6 January 2027."),
 ("Thursday 7 January 2027", "7 January 2027."),
 ("Friday 8 January 2027", "8 January 2027."),
 ("Monday 11 January 2027", "11 January 2027.")],
"Wednesday 6 January 2027", 3, ordered=True,
twin=T([("Friday 25 December; Monday 28 December (substitute day for Boxing Day); Friday 1 January.",
         "Friday 25 December; Friday 1 January. (Monday 28 December is a normal business day in Harwen.)")],
       "Tuesday 5 January 2027")),
]
