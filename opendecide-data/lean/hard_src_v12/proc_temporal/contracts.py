"""proc_temporal / contracts: cure periods, liquidated damages, indexation, notice
periods, force majeure notices, uptime credits, payment terms, renewals,
retentions, quotes, commitments, lease breaks, cooling-off, liability caps
(Vantage Kiln Systems, Corbridge Build, Ferrant Facilities, Thornaby Logistics,
Meridan Hosting, Oakhollow Estates and others)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ ct01
# why: 15 business days after Mon 7 Dec 2026, skipping 25 Dec, 28 Dec, 1 Jan:
# 8,9,10,11,14,15,16,17,18,21,22,23,24,29,30 -> cure period ends Wed 30 Dec.
# Cured 29 Dec -> within -> no right to terminate. Ignoring holidays -> 28 Dec (wrong).
# Twin: cured 31 Dec -> after 30 Dec -> may terminate.
C("ct01", "Can the customer terminate the maintenance contract for this breach?",
"""
Master Services Agreement — Vantage Kiln Systems Ltd and Harrowden Brickworks plc

Clause 1 (Definitions)
"Business Day": a day other than a Saturday, a Sunday, 25 December, 28 December 2026 or 1 January 2027 (the substitute bank holidays that apply to this Agreement).

Clause 18 (Termination for breach)
18.1 If a party commits a material breach, the other party may serve a breach notice.
18.2 The party in breach has 15 Business Days after the day the notice is received to cure the breach.
18.3 If the breach is not cured by the end of that period, the other party may terminate with immediate effect by written notice.
18.4 A breach cured within the period gives no right to terminate, whatever the history of earlier breaches.

Contract manager's file
Breach: failure to attend kiln 3 within the 48-hour call-out time on three occasions in November 2026
Breach notice received by Vantage: Monday 7 December 2026
Cure: dedicated on-call engineer appointed and call-out met in full, confirmed in writing: 29 December 2026
Harrowden's operations director: "Three failures in a month. We've had enough — terminate on 4 January."
""",
[("no_right_to_terminate", "Skipping the 25 and 28 December holidays, the 15 Business Days ended on Wednesday 30 December, and the cure came within that period."),
 ("may_terminate", "Skipping the 25 and 28 December holidays, the 15 Business Days ended on Wednesday 30 December, and the cure came after that."),
 ("terminate_holidays_ignored", "Fifteen weekdays from 7 December end on Monday 28 December, so the 29 December cure was too late."),
 ("terminate_repeated_breach", "Three failures in one month show a pattern of breach, which allows termination whatever the cure.")],
"no_right_to_terminate", 3,
twin=T([("confirmed in writing: 29 December 2026", "confirmed in writing: 31 December 2026")], "may_terminate")),

# ------------------------------------------------------------------ ct02
# why: LDs 0.5% of contract price per FULL week of delay after the (extended)
# completion date, cap 10%. EOT of 12 days -> 30 Jun + 12 = 12 Jul. Actual 20 Aug ->
# 39 days late -> 5 full weeks -> 2.5% x 480,000 = 12,000.
# Twin: EOT rejected -> date stays 30 Jun -> 51 days -> 7 full weeks -> 3.5% = 16,800.
C("ct02", "How much in liquidated damages should the employer deduct?",
"""
Building Contract — Corbridge Build Ltd for the Linthorpe Medical Practice extension

Contract particulars
Contract sum: 480,000
Date for completion: 30 June 2026
Liquidated damages: 0.5% of the contract sum for each full week by which completion is later than the date for completion (as extended). Part weeks are not charged. Total LDs are capped at 10% of the contract sum.

Clause 2.28 — Extensions of time
The contract administrator may fix a later date for completion by a written extension of time. An extension, once granted, moves the date for completion for all purposes, including LDs.

Contract administrator's record
Extension of time EOT-02 (exceptionally adverse weather, 12 days): granted in writing on 3 July 2026
Practical completion certified: 20 August 2026
Employer's finance team: "Late from 30 June to 20 August is 51 days — seven weeks and a bit, round up to eight."
""",
[("deduct_12000", "The extension moves completion to 12 July; 39 days late is 5 full weeks at 0.5% of 480,000."),
 ("deduct_16800", "No extension moved the date, so completion is 51 days after 30 June, 7 full weeks at 0.5% of 480,000."),
 ("deduct_19200", "Counting from 30 June and rounding the part week up gives 8 weeks at 0.5% of 480,000."),
 ("deduct_14400", "The extension moves completion to 12 July, and 39 days is 6 weeks once the part week is counted.")],
"deduct_12000", 2,
twin=T([("granted in writing on 3 July 2026", "rejected in writing on 3 July 2026")], "deduct_16800")),

# ------------------------------------------------------------------ ct03
# why: increase = CPI change March-to-March, floor 0%, cap 4%. 124.9 / 118.4 = +5.49%
# -> capped at 4% -> 36,000 x 1.04 = 37,440.
# Twin: March 2026 index 121.36 -> +2.5% -> 36,900.
C("ct03", "What annual fee should the renewal invoice show?",
"""
Facilities Services Agreement — Ferrant Facilities and the Kingsmere Academy Trust

Schedule 4 (Charges)
4.1 Year 1 annual fee: 36,000 (1 April 2025 to 31 March 2026).
4.2 On each anniversary, the annual fee changes by the percentage change in the Consumer Price Index (CPI) between the March index of the previous year and the March index of the current year.
4.3 The change is subject to a floor of 0% and a cap of 4%.
4.4 Additional services ordered during the year are invoiced separately and are not indexed.

Published CPI (all items)
March 2025: 118.4
March 2026: 124.9

Ferrant's draft renewal invoice: "CPI up 5.5% — Year 2 fee 37,980."
Trust business manager's reply: "We budgeted for no increase at all this year."
""",
[("fee_37_440", "CPI rose about 5.5%, above the 4% cap, so the fee rises by 4%: 36,000 × 1.04."),
 ("fee_36_900", "CPI rose 2.5%, inside the 0% to 4% range, so the fee rises by 2.5%: 36,000 × 1.025."),
 ("fee_37_980", "The fee follows the full CPI change of about 5.5%."),
 ("fee_36_000", "The Trust budgeted for no increase, so the Year 1 fee continues.")],
"fee_37_440", 1,
twin=T([("March 2026: 124.9", "March 2026: 121.36"), ("CPI up 5.5% — Year 2 fee 37,980.", "CPI up 2.5% — Year 2 fee to follow.")], "fee_36_900")),

# ------------------------------------------------------------------ ct04
# why: termination for convenience takes effect at the end of the first calendar month
# that ends at least 90 days after notice is received. 15 Aug + 90 = 13 Nov -> end of
# November -> 30 Nov 2026. Twin: notice 2 Sep -> +90 = 1 Dec -> 31 Dec 2026.
C("ct04", "On what date does this termination for convenience take effect?",
"""
Logistics Services Agreement — Thornaby Logistics and Pellow Garden Centres

Clause 22 (Termination for convenience)
22.1 Either party may end this Agreement for convenience by giving written notice.
22.2 Termination takes effect on the last day of the first calendar month that ends at least 90 days after the day the notice is received.
22.3 The day the notice is received is not counted in the 90 days.
22.4 Charges continue to the termination date. No early termination fee applies to termination under this clause.

Clause 23 (Notices) — notices must be sent by recorded delivery to the registered office and are received on the date of the delivery signature.

Notice file
Notice from Pellow Garden Centres, recorded delivery, signed for at Thornaby's registered office: 15 August 2026
Pellow's letter: "We give three months' notice, ending on 15 November 2026."
Thornaby's account manager: "Ninety days from the 15th is 13 November, so that's the end date."
""",
[("ends_30_november", "The 90th day after receipt is 13 November, and November is the first month ending on or after it."),
 ("ends_31_december", "The 90th day after receipt is 1 December, so December is the first month that ends at least 90 days later."),
 ("ends_15_november", "The letter gives three months' notice ending on 15 November, which the customer is free to choose."),
 ("ends_13_november", "The Agreement ends on the 90th day after the notice was received.")],
"ends_30_november", 2,
twin=T([("signed for at Thornaby's registered office: 15 August 2026", "signed for at Thornaby's registered office: 2 September 2026"),
        ("ending on 15 November 2026", "ending on 2 December 2026"),
        ("Ninety days from the 15th is 13 November", "Ninety days from the 2nd is 1 December")], "ends_31_december")),

# ------------------------------------------------------------------ ct05
# why: FM notice within 5 business days after the event starts. Strike began Wed
# 3 Jun 2026: Thu 4 (1), Fri 5 (2), Mon 8 (3), Tue 9 (4), Wed 10 (5). Notice sent Wed
# 10 Jun -> on time -> delay excused for the FM period. Twin: Thu 11 Jun -> late ->
# cannot rely on FM -> delay not excused.
C("ct05", "Can the supplier rely on force majeure for the late shipments?",
"""
Supply Agreement — Oristano Tiles S.p.A. and Wexcombe Interiors Ltd

Clause 15 (Force majeure)
15.1 Neither party is liable for delay caused by events beyond its reasonable control, including strikes by third parties, port closures and natural disasters.
15.2 A party wishing to rely on 15.1 must notify the other party in writing within 5 Business Days after the event begins. The day the event begins is not counted.
15.3 A party that does not give notice within that time cannot rely on 15.1 for that event.
15.4 "Business Day" means Monday to Friday, other than public holidays in England. There are no English public holidays between 26 May and 31 August 2026.

Facts from the correspondence file
Event: dock workers' strike at the Port of Salvenna, began Wednesday 3 June 2026, ended 19 June 2026
Oristano's written notice of force majeure: emailed Wednesday 10 June 2026
Shipments affected: 6 containers, delivered 8 to 16 days late
Wexcombe's buyer: "They told us nothing for a week. That's too late — charge the late-delivery penalties."
""",
[("delay_excused", "Counting weekdays after 3 June, 10 June is the fifth Business Day, so notice came in time and clause 15.1 applies."),
 ("delay_not_excused", "The fifth Business Day after 3 June was 10 June, and notice came after it, so clause 15.3 bars reliance."),
 ("not_excused_calendar_week", "A full calendar week passed before notice, which is more than 5 days."),
 ("excused_regardless", "A port strike is plainly beyond the supplier's control, so the timing of notice does not matter.")],
"delay_excused", 2,
twin=T([("emailed Wednesday 10 June 2026", "emailed Thursday 11 June 2026")], "delay_not_excused")),

# ------------------------------------------------------------------ ct06
# why: availability = (43,200 - unplanned downtime) / 43,200 (30-day month).
# Maintenance announced >= 5 days ahead is excluded. Announced 7 days ahead -> excluded.
# Unplanned 38 + 22 = 60 min -> 99.861% -> below 99.9, not below 99.5 -> 10% of 5,000 =
# 500. Twin: announced 3 days ahead -> 240 min counts -> 300 min -> 99.306% -> below
# 99.5, not below 99.0 -> 25% = 1,250.
C("ct06", "What service credit is due for September?",
"""
Meridan Hosting — Service Level Agreement, Enterprise tier

1. Availability for a month = (minutes in the month − counted downtime) ÷ minutes in the month.
2. Counted downtime is all downtime except planned maintenance announced to the customer at least 5 days in advance.
3. Credits (percentage of the monthly fee):
   availability below 99.9%: 10%
   availability below 99.5%: 25%
   availability below 99.0%: 50%
   Only the highest applicable credit is given.
4. September has 30 days (43,200 minutes).

Customer: Quillfeather Publishing — monthly fee 5,000

September 2026 incident log
Incident A (unplanned, storage fault): 38 minutes
Incident B (unplanned, network): 22 minutes
Planned maintenance (database upgrade): 240 minutes on 19 September; announced to the customer on 12 September
Customer's email: "Five hours of outage in one month is unacceptable. We expect the 50% credit."
""",
[("credit_500", "The maintenance was announced 7 days ahead and is excluded, so 60 counted minutes give about 99.86%, below 99.9%."),
 ("credit_1250", "The maintenance was announced fewer than 5 days ahead and counts, so 300 minutes give about 99.31%, below 99.5%."),
 ("credit_2500", "Five hours of outage in the month takes availability below 99.0%."),
 ("credit_none", "Unplanned downtime was only an hour, so availability stays above the SLA.")],
"credit_500", 3,
twin=T([("announced to the customer on 12 September", "announced to the customer on 16 September")], "credit_1250")),

# ------------------------------------------------------------------ ct07
# why: "30 days end of month": due 30 days after the last day of the invoice month.
# Invoice 12 Aug -> 31 Aug + 30 = 30 Sep. Paid 28 Sep -> on time -> no late charge.
# Twin: paid 1 Oct -> after 30 Sep -> late charge 40.
C("ct07", "Is a late-payment charge due on this invoice?",
"""
Purchase Terms — Kilnsey Packaging Ltd (supplier) and Ardlow Foods (buyer)

P1. Payment terms are "30 days end of month": each invoice is due 30 days after the last day of the month in which it is dated.
P2. A payment received after the due date carries a fixed late charge of 40 per invoice.
P3. Payment is received on the date the funds reach the supplier's account.
P4. Disputed invoices are not due until the dispute is resolved (no dispute on this invoice).

Invoice KP-26-08812
Invoice date: 12 August 2026
Amount: 7,318.40
Funds received in Kilnsey's account: 28 September 2026

Kilnsey's credit controller, email of 14 September: "Your invoice was due on 11 September — 30 days from the invoice date. Please pay now; a late charge will apply."
""",
[("no_late_charge", "The invoice was due 30 days after 31 August, on 30 September, and funds arrived by then."),
 ("late_charge_40", "The invoice was due on 30 September, 30 days after the end of August, and the funds arrived after that."),
 ("late_charge_by_invoice_date", "The invoice was due 30 days after its 12 August date, so the September payment was late."),
 ("late_charge_80", "The payment was more than two weeks late, so the fixed charge is doubled.")],
"no_late_charge", 1,
twin=T([("Funds received in Kilnsey's account: 28 September 2026", "Funds received in Kilnsey's account: 1 October 2026")], "late_charge_40")),

# ------------------------------------------------------------------ ct08
# why: non-renewal notice must be RECEIVED at least 90 days before expiry (30 Apr 2027).
# 90 days before = 30 Jan 2027. Courier sent Fri 29 Jan, received Mon 1 Feb -> 88 days
# before -> too late -> contract renews. Twin: sent Thu 28 Jan, received Fri 29 Jan ->
# 91 days -> valid -> expires 30 Apr 2027.
C("ct08", "Does this contract renew on 1 May 2027?",
"""
Cleaning Services Contract — Brightwater Cleaning and the Oakhollow Estates office portfolio

8.1 The contract runs until 30 April 2027 and then renews automatically for 12 months.
8.2 Either party may prevent renewal by written notice received by the other party at least 90 days before the expiry date. The number of days is the expiry date minus the date of receipt.
8.3 A notice is received on the date it is delivered to the addressee, as shown by the courier's proof of delivery. The date of sending does not matter.
8.4 Renewal prices are set under Schedule 2.

Correspondence log (Oakhollow Estates)
Non-renewal notice sent by courier: Friday 29 January 2027
Courier proof of delivery at Brightwater: Monday 1 February 2027, 09:14
Brightwater's reply: "We received your notice after the deadline. The contract renews on 1 May 2027."
Oakhollow's property manager: "We sent it on the 29th, 91 days before — we're fine."
""",
[("renews_1_may", "The notice was received on 1 February, 88 days before the 30 April expiry, which is short of 90 days."),
 ("expires_30_april", "The notice was received 90 or more days before the 30 April expiry, so the contract ends."),
 ("expires_by_sending_date", "The notice was sent on 29 January, 91 days before expiry, which meets the 90-day rule."),
 ("renews_by_reply", "Brightwater has already written to say the contract renews, which settles it.")],
"renews_1_may", 2,
twin=T([("sent by courier: Friday 29 January 2027", "sent by courier: Thursday 28 January 2027"),
        ("Monday 1 February 2027, 09:14", "Friday 29 January 2027, 09:14"),
        ("We sent it on the 29th, 91 days before", "We sent it on the 28th and it arrived on the 29th, 91 days before")], "expires_30_april")),

# ------------------------------------------------------------------ ct09
# why: retention 5%; half (2.5%) released at practical completion (done); the second
# half at the end of the 12-month defects period, IF all notified defects are remedied.
# PC 14 Sep 2025 -> period ends 14 Sep 2026. All 3 defects remedied by 10 Sep ->
# release 2.5% x 640,000 = 16,000. Twin: one defect outstanding -> withhold.
C("ct09", "What should the employer do with the remaining retention?",
"""
Building Contract — Ashgrove Housing Co-operative and Pennard Construction

Retention
R1. The employer holds retention of 5% of the contract sum (contract sum: 640,000).
R2. Half of the retention is released on practical completion.
R3. The other half is released at the end of the defects period of 12 months after practical completion, but only once every defect notified in that period has been remedied.
R4. If any notified defect is still outstanding, the second half is held until it is remedied.

Contract administrator's record
Practical completion: 14 September 2025; first half of retention (16,000) released 30 September 2025
Defects notified during the defects period: 3
    D1 — sticking fire door, flat 4: remedied 2 June 2026
    D2 — gutter leak, block B: remedied 19 August 2026
    D3 — cracked paving slab, courtyard: remedied 10 September 2026
Date of this review: 21 September 2026
Co-operative treasurer: "Let's hold on to all 32,000 for another year, just in case."
""",
[("release_16000", "The defects period ended on 14 September 2026 and every notified defect has been remedied, so the second 2.5% is released."),
 ("withhold_second_half", "A notified defect is still outstanding, so the second half of the retention is held until it is remedied."),
 ("release_32000", "The defects period has ended, so the whole 5% retention of 32,000 is released now."),
 ("hold_for_another_year", "The employer may keep the retention for a further year as a precaution.")],
"release_16000", 2,
twin=T([("D3 — cracked paving slab, courtyard: remedied 10 September 2026", "D3 — cracked paving slab, courtyard: not yet remedied (booked for 5 October 2026)")], "withhold_second_half")),

# ------------------------------------------------------------------ ct10
# why: quote valid for 30 days after the quote date (quote date = day 0): 14 Aug + 30 =
# 13 Sep. Acceptance 13 Sep -> valid -> honour quoted price. Twin: 14 Sep -> lapsed ->
# re-quote at current list. Rep's email ("held to end of September") is not a signed
# variation.
C("ct10", "What price should order entry apply to this acceptance?",
"""
Harlan Forge Machinery — Quotation Q-26-4410 and Standard Terms of Quotation

Quotation (dated 14 August 2026)
Customer: Tresco Engineering Ltd
Item: 2 × HF-900 CNC press brakes
Quoted price: 118,500 (current list price from 1 September 2026: 126,000)

Standard Terms of Quotation
Q1. A quotation is valid for 30 days after its date. The quotation date is day 0.
Q2. An acceptance received within the validity period is honoured at the quoted price.
Q3. After the validity period, the quotation lapses. Any order is re-quoted at the list price current on the day of acceptance.
Q4. The validity period may be extended only by a written variation signed by the sales director.

Acceptance: signed purchase order emailed by Tresco, received Sunday 13 September 2026, 16:30
Sales rep's earlier email to Tresco (22 August): "No rush — I can hold these prices until the end of September."
Signed variation from sales director: none
""",
[("honour_118500", "The acceptance arrived on day 30 after the 14 August quotation, still within the validity period."),
 ("requote_126000", "The acceptance arrived after day 30, so the quotation lapsed and the current list price applies."),
 ("honour_by_rep_email", "The sales rep promised to hold the prices to the end of September, so the quoted price stands."),
 ("requote_weekend", "An acceptance received on a Sunday counts from Monday, after the validity period.")],
"honour_118500", 2,
twin=T([("received Sunday 13 September 2026, 16:30", "received Monday 14 September 2026, 09:05")], "requote_126000")),

# ------------------------------------------------------------------ ct11
# why: minimum 1,200 units per contract year (1 Jan-31 Dec 2026). Purchases 1,130.
# Orders placed within 10 days after year end count toward the prior year if the
# customer elects in writing: order 3 Jan 2027 (90 units), election made -> 1,220 ->
# no shortfall. Twin: order 12 Jan -> outside 10 days -> 1,130 -> 70 short x 15 = 1,050.
C("ct11", "Is a minimum-purchase shortfall fee due for 2026?",
"""
Distribution Agreement — Selby Filtration and Garrowby Pumps

Schedule 3 (Minimum purchase commitment)
3.1 The distributor must buy at least 1,200 units in each contract year (1 January to 31 December).
3.2 Units returned for credit in the year are deducted from purchases for that year.
3.3 Orders placed within 10 days after the end of a contract year count toward that year if the distributor elects this in writing when placing the order.
3.4 Any shortfall is charged at 15 per unit short, invoiced in February.

Account review for contract year 2026
Units purchased 1 January–31 December 2026: 1,130
Returns for credit in 2026: none
Order GP-27-0003 for 90 units: placed 3 January 2027, with a written election: "Please count this order toward our 2026 commitment."
Selby account manager's draft: "Shortfall of 70 units × 15 = 1,050. The January order belongs to 2027."
""",
[("no_shortfall_fee", "The 3 January order falls within 10 days after year end and was elected in writing, so 2026 purchases reach 1,220."),
 ("shortfall_fee_1050", "The January order falls outside the 10-day window, so 2026 purchases stay at 1,130, which is 70 short."),
 ("shortfall_by_calendar", "Only orders placed in the calendar year count, so 2026 is 70 units short."),
 ("shortfall_fee_1800", "The shortfall is charged on the full 1,200-unit commitment at 1.50 per unit.")],
"no_shortfall_fee", 2,
twin=T([("placed 3 January 2027, with a written election", "placed 12 January 2027, with a written election")], "shortfall_fee_1050")),

# ------------------------------------------------------------------ ct12
# why: break date 24 Jun 2027; notice must be received at least 6 months before, i.e.
# on or before 24 Dec 2026. Received 23 Dec 2026 -> valid. Arrears condition is on the
# break date; earlier arrears cleared do not matter. Twin: received 29 Dec -> invalid.
C("ct12", "Is the tenant's break notice valid?",
"""
Lease — Unit 7, Kelsall Trade Park (landlord: Oakhollow Estates; tenant: Brewin Print Ltd)

Clause 9 (Tenant's break option)
9.1 The tenant may end this lease on 24 June 2027 (the "break date").
9.2 The tenant must give the landlord written notice received on or before 24 December 2026, being at least 6 months before the break date.
9.3 The break takes effect only if, on the break date, the tenant has paid all rent due. Arrears at earlier times that have been paid off do not affect the break.
9.4 Time is of the essence for 9.2. Notice received late is of no effect.

Landlord's file
Break notice from Brewin Print: received by recorded delivery on Wednesday 23 December 2026
Rent history: one quarter's rent paid 19 days late in 2025; account clear since then
Asset manager's note: "They've been in arrears before. Let's reject the notice."
""",
[("valid_notice", "The notice was received on or before 24 December 2026, and past arrears that were paid off do not matter."),
 ("invalid_late_notice", "The notice was received after 24 December 2026, and time is of the essence."),
 ("invalid_past_arrears", "The tenant paid rent late in 2025, so it cannot use the break."),
 ("valid_until_arrears_check", "The notice is conditional until the landlord checks rent in December 2026.")],
"valid_notice", 1,
twin=T([("received by recorded delivery on Wednesday 23 December 2026", "received by recorded delivery on Tuesday 29 December 2026")], "invalid_late_notice")),

# ------------------------------------------------------------------ ct13
# why: cooling-off 14 days from the LATER of policy start (1 Sep) and receipt of
# documents (5 Sep) -> until 19 Sep. Cancel 18 Sep -> within -> full refund 365.
# Twin: documents received 3 Sep -> cooling-off until 17 Sep -> 18 Sep outside ->
# pro rata: 1-18 Sep = 18 days used at 1.00/day -> 347 - 25 admin = 322.
C("ct13", "What refund should the insurer pay on this cancelled policy?",
"""
Kettlewell Insurance — Pet Policy Terms, section 3 (Cancellation)

3.1 Cooling-off: you may cancel within 14 days after the later of (a) the policy start date and (b) the day you receive your policy documents. You get a full refund.
3.2 After cooling-off, you may cancel at any time. We refund the premium for the unused days (daily rate = annual premium ÷ 365), minus a 25 administration fee. Days used run from the start date to the cancellation date, both included.
3.3 No refund is paid if a claim has been made in the policy year.

Policy KI-PET-661029
Policyholder: Lorcan Whitfield (dog: "Bramble")
Annual premium: 365.00, paid in full
Start date: 1 September 2026
Policy documents received (email read receipt): 5 September 2026
Cancellation received: 18 September 2026
Claims made: none
Agent's note: "More than 14 days since the start — pro rata minus admin."
""",
[("refund_365_full", "Cooling-off runs 14 days from 5 September, the later date, so the 18 September cancellation falls within it."),
 ("refund_322_pro_rata", "Cooling-off ended 14 days after 3 September, so 18 days used leave 347, minus the 25 fee."),
 ("refund_323_from_start", "Cooling-off runs from the 1 September start date and has ended, so 17 days used leave 348, minus the 25 fee."),
 ("refund_none", "The dog was insured for part of the month, so no refund is due.")],
"refund_365_full", 2,
twin=T([("Policy documents received (email read receipt): 5 September 2026", "Policy documents received (email read receipt): 3 September 2026")], "refund_322_pro_rata")),

# ------------------------------------------------------------------ ct14
# why: on-time window = scheduled date minus 1 up to plus 1 business day. Due Fri 29 May
# 2026; +1 business day = Mon 1 Jun -> delivered Mon 1 Jun -> on time; full quantity ->
# OTIF met -> no penalty. Twin: delivered Tue 2 Jun -> +2 business days -> late ->
# 3% of 42,600 = 1,278.
C("ct14", "Does this delivery trigger the late-delivery penalty?",
"""
Supplier Performance Schedule — Dunmore Kline Engineering and Tessaly Castings

SP1. A delivery is on time if it arrives from 1 business day before to 1 business day after the scheduled date.
SP2. A delivery is in full if at least 98% of the ordered quantity arrives.
SP3. A delivery that is late (outside SP1) carries a penalty of 3% of the purchase-order value. Deliveries short of SP2 carry a separate 2% penalty.
SP4. Business days are Monday to Friday. There are no holidays between 25 May and 30 June 2026 under this contract.

Purchase order PO-DK-77140
Item: pump housings, 1,000 units; PO value 42,600
Scheduled delivery date: Friday 29 May 2026
Goods received note: Monday 1 June 2026, 1,000 units, 0 rejected
Goods-in supervisor: "Three days after the due date — that's late. Apply the 3%."
""",
[("no_penalty", "Monday 1 June is 1 business day after Friday 29 May, inside the on-time window, and the full quantity arrived."),
 ("penalty_1278", "The goods arrived more than 1 business day after Friday 29 May, outside the on-time window: 3% of 42,600."),
 ("penalty_calendar_days", "The goods arrived three calendar days after the scheduled date, which is late."),
 ("penalty_852", "The goods arrived after the scheduled date, which is a 2% penalty on 42,600.")],
"no_penalty", 2,
twin=T([("Goods received note: Monday 1 June 2026", "Goods received note: Tuesday 2 June 2026"), ("Three days after", "Four days after")], "penalty_1278")),

# ------------------------------------------------------------------ ct15
# why: 20 h/month retainer; unused hours roll to the NEXT month only, capped at 10.
# July used 14 -> 6 roll -> August available 26; used 29 -> 3 over x 150 = 450.
# Twin: July used 8 -> 12 unused -> cap 10 -> August available 30 >= 29 -> no overage.
C("ct15", "What overage should the August invoice include?",
"""
Consulting Retainer — Pinfold Data Advisory and Lysander Travel Group

Retainer terms
T1. The retainer includes 20 hours of consulting each calendar month for a fixed fee of 3,000.
T2. Unused hours roll over to the following month only. No more than 10 hours may roll over. Rolled hours expire at the end of that following month.
T3. Hours beyond the month's available total (20 plus any rolled hours) are billed at 150 per hour.
T4. Travel time is not counted as consulting hours.

Timesheet summary
June 2026: 20.0 h used (no rollover into July)
July 2026: 14.0 h used
August 2026: 29.0 h used (plus 3.5 h travel)

Client's finance manager: "We've barely used our hours over the summer — there shouldn't be any overage."
Pinfold's billing assistant draft: "August overage 9 h × 150 = 1,350."
""",
[("overage_450", "July left 6 unused hours to roll over, so August had 26 available, and 29 used is 3 over at 150."),
 ("no_overage", "July left more than 10 unused hours, so 10 rolled over, and August's 30 available covered the 29 used."),
 ("overage_1350", "Each month stands alone at 20 hours, so August is 9 hours over at 150."),
 ("overage_975", "August's travel time counts too, making 32.5 hours against 26 available, 6.5 over at 150.")],
"overage_450", 2,
twin=T([("July 2026: 14.0 h used", "July 2026: 8.0 h used")], "no_overage")),

# ------------------------------------------------------------------ ct16
# why: offer lapses 17:00 Halvorsen time (UTC-3) on 30 Oct 2026 = 20:00 UTC. Acceptance
# effective when received by the offeror's server; stamp 20:05 UTC -> 17:05 UTC-3 -> after
# lapse -> no contract; treat the acceptance as a new offer. Twin: 19:55 UTC -> 16:55 ->
# contract formed.
C("ct16", "Has a contract been formed on these terms?",
"""
Offer letter — Halvorsen Timber Co. (Brandvik office, UTC−3) to Castlereagh Joinery (Dunmurry, UTC+0)

"We offer 180 m³ of kiln-dried larch at 412 per m³, delivered. This offer lapses at 17:00 Brandvik time on Friday 30 October 2026."

Halvorsen standard conditions (incorporated)
C1. An acceptance is effective when it is received by Halvorsen's mail server, as shown by the server timestamp (UTC).
C2. An acceptance received after the offer lapses is not an acceptance. Halvorsen treats it as a new offer from the buyer, which Halvorsen may accept or decline.
C3. Oral acceptances are not valid.

Mail server log (UTC)
Email from Castlereagh Joinery, subject "ACCEPTANCE — larch 180 m³": received 2026-10-30 20:05 UTC

Castlereagh's director (phone, 31 October): "I sent it just after eight in the evening our time, well within your working day — we have a deal."
""",
[("contract_formed", "The server stamp converts to 16:55 Brandvik time, before the 17:00 lapse, so the acceptance was effective."),
 ("treat_as_new_offer", "The server stamp converts to 17:05 Brandvik time, after the offer lapsed, so the email is a new offer from the buyer."),
 ("contract_formed_sender_time", "The buyer sent the email a little after 20:00 in Dunmurry, within Halvorsen's working day."),
 ("no_contract_oral_needed", "The acceptance should have been confirmed by phone, which happened only on 31 October.")],
"treat_as_new_offer", 3,
twin=T([("received 2026-10-30 20:05 UTC", "received 2026-10-30 19:55 UTC"), ("just after eight in the evening", "just before eight in the evening")], "contract_formed")),

# ------------------------------------------------------------------ ct17
# why: upward-only indexation. Indexed rent = 48,000 x new/old index. Index fell 102.0 ->
# 99.45 -> 46,800 < 48,000 -> rent stays 48,000. Twin: index 104.55 -> x 1.025 -> 49,200.
C("ct17", "What rent applies from the review date?",
"""
Lease — Ground floor, 3 Tollgate Square (tenant: Marigold & Finch Opticians)

Schedule 5 (Rent review)
5.1 On each review date the rent becomes the greater of (a) the rent payable immediately before the review date and (b) that rent multiplied by the Review Index for the review date divided by the Review Index for the previous review date.
5.2 The Review Index is the published Commercial Rents Index for the month two months before the review date.
5.3 The reviewed rent is payable from the review date, even if agreed later.

Review file
Rent before review: 48,000 per year
Previous review date: 25 March 2021 — Review Index 102.0
Current review date: 25 March 2026 — Review Index 99.45
Tenant's letter: "The index has fallen. We look forward to a lower rent."
Landlord's surveyor: "Rent rises to 50,000 — that's the market level now."
""",
[("rent_48000", "The index fell, so the indexed figure of 46,800 is lower, and the rent stays at the higher pre-review rent."),
 ("rent_49200", "The index rose by 2.5%, so the rent rises to 48,000 × 1.025."),
 ("rent_46800", "The index fell by 2.5%, so the rent falls to 48,000 × 0.975."),
 ("rent_50000", "The surveyor puts market rent at 50,000, so that becomes the rent.")],
"rent_48000", 2,
twin=T([("Review Index 99.45", "Review Index 104.55"), ("The index has fallen. We look forward to a lower rent.", "The index has hardly moved. We expect the rent to stay the same.")], "rent_49200")),

# ------------------------------------------------------------------ ct18
# why: defects notice window = 12 months from ACCEPTANCE (10 Oct 2025), not delivery
# (22 Sep 2025) -> ends 10 Oct 2026. Notice 1 Oct 2026 -> in time -> remedy at supplier's
# cost. Twin: notice 12 Oct 2026 -> outside -> chargeable repair.
C("ct18", "Who pays to fix the conveyor fault?",
"""
Equipment Supply Contract — Ruddock Conveyors and Pellham Distribution Centre

Clause 1 (Definitions)
"Acceptance Date": the date the buyer signs the acceptance certificate after site tests. It is not the delivery date.

Clause 14 (Defects)
14.1 The supplier must remedy at its own cost any defect notified in writing within 12 months after the Acceptance Date (the notice period ends on the first anniversary of the Acceptance Date).
14.2 Defects notified after that are remedied only on a chargeable basis at the supplier's current rates.
14.3 Wear parts (belts, rollers) are excluded from 14.1 in any event.

Project file
Delivery to site: 22 September 2025
Site tests passed; acceptance certificate signed: 10 October 2025
Defect: drive gearbox on line 2 overheating and seizing (not a wear part)
Written defect notice sent by Pellham: 1 October 2026
Ruddock's service manager: "Delivery was over a year ago, so it's chargeable."
""",
[("supplier_remedies_free", "The notice came before the first anniversary of the 10 October 2025 Acceptance Date, and the gearbox is not a wear part."),
 ("chargeable_repair", "The notice came after the first anniversary of the 10 October 2025 Acceptance Date, so the repair is chargeable."),
 ("chargeable_from_delivery", "The 12 months run from delivery on 22 September 2025, so the period had ended."),
 ("excluded_wear_part", "Gearbox faults count as wear and are excluded from free remedy.")],
"supplier_remedies_free", 2,
twin=T([("Written defect notice sent by Pellham: 1 October 2026", "Written defect notice sent by Pellham: 12 October 2026")], "chargeable_repair")),

# ------------------------------------------------------------------ ct19
# why: right to reject only if delivery MORE than 10 business days late. Due Mon 2 Nov
# 2026; delivered Tue 17 Nov. Business days after due up to delivery, skipping Wed 11 Nov
# (listed holiday): 3,4,5,6,9,10,12,13,16,17 = 10 -> not more than 10 -> accept with LDs.
# Twin: holiday list lacks 11 Nov -> 11 business days -> may reject.
C("ct19", "Can the buyer reject this late consignment?",
"""
Framework Agreement — Callander Furniture (supplier) and the Wextable Hotels group

F7. Delivery dates are set in each call-off order.
F8. For each business day of delay, the supplier pays liquidated damages of 0.2% of the call-off value.
F9. If delivery is more than 10 business days late, the buyer may reject the goods and cancel the call-off instead of claiming F8 damages.
F10. Business days exclude Saturdays, Sundays and the following holidays: 11 November 2026 (Remembrance Holiday), 25 December 2026, 28 December 2026.
F11. Days of delay are counted from the day after the delivery date to the day of delivery, inclusive.

Call-off CO-WH-1182: 64 bedroom chairs for the Wextable Harbour hotel, value 28,160
Delivery date: Monday 2 November 2026
Delivered: Tuesday 17 November 2026
Hotel's project manager: "Over two weeks late. We're sending them back."
""",
[("accept_with_damages", "Skipping 11 November, the delay is exactly 10 business days, which is not more than 10, so only F8 damages apply."),
 ("may_reject", "The delay is 11 business days, more than 10, so the buyer may reject and cancel."),
 ("reject_calendar_days", "Delivery was 15 calendar days after the due date, which is over two weeks."),
 ("accept_no_damages", "Delivery was within three weeks, which is a reasonable time, so no damages apply.")],
"accept_with_damages", 3,
twin=T([("11 November 2026 (Remembrance Holiday), 25 December 2026", "25 December 2026")], "may_reject")),

# ------------------------------------------------------------------ ct20
# why: 24-month term from 1 Mar 2025 (to 28 Feb 2027); early termination fee = 50% of
# the monthly fees for the months after the termination date. Terminate effective 31 Oct
# 2026 -> Mar 2025-Oct 2026 = 20 months used -> 4 remaining x 600 x 50% = 1,200.
# Twin: effective 31 Aug 2026 -> 18 used -> 6 remaining -> 1,800.
C("ct20", "What early termination fee is payable?",
"""
Managed Print Agreement — Tessaly Office Systems and Harwick Family Law LLP

1. Term: 24 months from 1 March 2025 to 28 February 2027.
2. Monthly fee: 600, invoiced on the 1st of each month.
3. The customer may end the agreement early by giving 30 days' notice, with effect from the last day of a calendar month.
4. Early termination fee: 50% of the monthly fees that would have been payable for the months after the termination date up to the end of the term.
5. Toner and click charges are billed separately and are not part of the fee.

Termination notice from Harwick Family Law: received 24 September 2026, termination effective 31 October 2026
Tessaly's account manager: "Four months left — that's 2,400 they owe us."
""",
[("fee_1200", "Four monthly fees (November to February) remain after 31 October, and half of 4 × 600 is 1,200."),
 ("fee_1800", "Six monthly fees (September to February) remain after 31 August, and half of 6 × 600 is 1,800."),
 ("fee_2400", "Four monthly fees remain, and all of them are payable: 4 × 600."),
 ("fee_1500", "Counting from the notice date in September, five monthly fees remain, and half of 5 × 600 is 1,500.")],
"fee_1200", 1,
twin=T([("received 24 September 2026, termination effective 31 October 2026", "received 28 July 2026, termination effective 31 August 2026"),
        ("Four months left — that's 2,400", "Six months left — that's 3,600")], "fee_1800")),

# ------------------------------------------------------------------ ct21
# why: cap = fees paid in the 12 months before the claim event. Event 15 Jul 2026 ->
# window 15 Jul 2025 - 14 Jul 2026 -> payments 1 Oct 2025 (9,000), 1 Jan 2026 (12,000),
# 1 Apr (12,000), 1 Jul (12,000) = 45,000; claim 50,000 -> pay 45,000.
# Twin: event 30 Jun 2026 -> window 30 Jun 2025 - 29 Jun 2026 -> 1 Jul 2025 (9,000) +
# 9,000 + 12,000 + 12,000 = 42,000.
C("ct21", "How much of this damages claim is within the liability cap?",
"""
Software Services Agreement — Corrigan Ledger Systems and the Wardle Veterinary Group

Clause 12 (Limitation of liability)
12.1 Each party's total liability for any claim is limited to the fees paid by the customer in the 12 months before the event giving rise to the claim.
12.2 "The 12 months before the event" means from the same calendar date one year earlier up to the day before the event.
12.3 The cap does not apply to death or personal injury caused by negligence, or to fraud (neither is alleged).

Fees paid by Wardle (quarterly in advance)
1 July 2025: 9,000
1 October 2025: 9,000
1 January 2026: 12,000 (price change)
1 April 2026: 12,000
1 July 2026: 12,000

Claim: data-migration failure on 15 July 2026 caused lost appointment records; Wardle claims 50,000 in losses
Corrigan's legal team: "Cap is fees in calendar year 2026 to date — 36,000."
""",
[("pay_45000", "Payments from 15 July 2025 to 14 July 2026 are the October, January, April and July quarters, totalling 45,000."),
 ("pay_42000", "Payments from 30 June 2025 to 29 June 2026 are the July 2025, October, January and April quarters, totalling 42,000."),
 ("pay_36000", "The cap is the fees paid in calendar year 2026 so far."),
 ("pay_50000", "The claim is below total fees ever paid (54,000), so it is paid in full.")],
"pay_45000", 2,
twin=T([("data-migration failure on 15 July 2026", "data-migration failure on 30 June 2026")], "pay_42000")),

# ------------------------------------------------------------------ ct22
# why: claim notice within 30 days of awareness: aware 5 Oct -> day 30 = 4 Nov 2026.
# Email received after 17:00 recipient time is deemed received next business day.
# Sent 18:20 UTC+0 = 20:20 recipient time (UTC+2) -> deemed received Thu 5 Nov -> late ->
# claim barred. Twin: sent 14:20 UTC+0 = 16:20 UTC+2 -> received 4 Nov -> in time.
C("ct22", "Was the warranty claim notified in time?",
"""
Share Purchase Agreement — sale of Brisewood Tooling Ltd (seller: Idris Varnell; buyer: Ostrava Holdings, UTC+2)

Clause 10 (Warranty claims)
10.1 The buyer must notify the seller of any warranty claim within 30 days after becoming aware of the facts giving rise to it. Day 1 is the day after the buyer becomes aware.
10.2 A claim not notified within that period is barred.

Clause 20 (Notices)
20.1 Notices may be given by email to the seller's nominated address.
20.2 An email is received when it arrives, unless it arrives after 17:00 in the place of receipt, or on a non-business day, in which case it is received at 09:00 on the next business day.
20.3 The seller has nominated his office in Vienna (UTC+2) as the place of receipt.

Buyer's file
Facts discovered (unpaid tax liability of Brisewood): 5 October 2026
Claim email sent from the buyer's London team (UTC+0): Wednesday 4 November 2026, 18:20 London time
Seller's lawyer: "The notice was out of time."
""",
[("claim_in_time", "The email reached Vienna at 16:20 local time on 4 November, day 30, before the 17:00 cut-off."),
 ("claim_barred", "The email reached Vienna at 20:20 local time, after 17:00, so it counts as received on 5 November, day 31."),
 ("claim_in_time_sent", "The email was sent on 4 November, which is day 30 after awareness."),
 ("claim_barred_day_29", "Day 30 was 3 November, because the day of awareness counts as day 1.")],
"claim_barred", 3,
twin=T([("Wednesday 4 November 2026, 18:20 London time", "Wednesday 4 November 2026, 14:20 London time")], "claim_in_time")),
]
