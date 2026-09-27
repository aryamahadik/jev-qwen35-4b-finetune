"""proc_adversarial / commercial contracts (renewal, service levels, warranties, pricing,
assignment, damages, termination, notices, leases). All parties are invented:
Harrowgate Freight, Solace Telecom, Fenmoor Pumps, Brisk Catering, Oldmere Council,
Tamsin Road Properties, Kingsway Analytics, Lorne Cloud Services and others."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ ct01
# why: Amendment No. 1 changes notice to 90 days before 31 Dec 2026 -> deadline 2 Oct 2026.
# Notice 15 Oct -> late -> renews 12 months. Twin: notice 25 Sep -> in time -> terminates at term end.
# plant: paralegal (60-day rule) says terminated -> wrong in base, right in twin.
C("ct01", "What is the status of the Lorne Cloud Services agreement after 31 December 2026?",
"""
Harrowgate Freight — Contract register entry CR-0441
Counterparty: Lorne Cloud Services
Agreement: Master Hosting Agreement dated 1 January 2024; initial term ends 31 December 2026

Clause 14 (Term and renewal)
14.1 On expiry of the initial term the agreement renews automatically for successive periods of 12 months.
14.2 Either party may prevent renewal by written notice given at least 60 days before the end of the then-current term.

Amendment No. 1 (signed by both parties, 3 March 2026)
In clause 14.2, "60 days" is replaced by "90 days". All other terms are unchanged.

Correspondence log
- Harrowgate non-renewal notice sent by courier and email: 15 October 2026 (receipt confirmed same day).
- Lorne reply: acknowledgement only.

Paralegal note in the register:
"Notice went out well over 60 days before year end — record the agreement as terminated on 31 Dec."
""",
[("terminates_31_december", "Notice was given at least 90 days before the end of the term, so the agreement ends on 31 December."),
 ("renews_for_12_months", "Under the amended 90-day clause the deadline was 2 October, so the October notice was late and the agreement renews."),
 ("renews_month_to_month", "A late notice converts the agreement to a monthly rolling term."),
 ("renews_for_36_months", "A late non-renewal notice renews the agreement for another full initial term."),
 ("terminates_on_notice", "A non-renewal notice ends the agreement on the day it is received.")],
"renews_for_12_months", 2,
twin=T([("Harrowgate non-renewal notice sent by courier and email: 15 October 2026", "Harrowgate non-renewal notice sent by courier and email: 25 September 2026")],
       "terminates_31_december")),

# ------------------------------------------------------------------ ct02
# why: August = 31 days = 44,640 minutes. Scheduled maintenance notified 7 days ahead (>= 5) is
# excluded. Unplanned 95 min -> uptime 1 - 95/44,640 = 99.787% -> below 99.9 but not below 99.5 -> 5%.
# Twin: unplanned 250 min -> 99.44% -> below 99.5 -> 10%.
# plant: customer claims 10% -> wrong in base, right in twin.
C("ct02", "What service credit does Solace Telecom owe for August 2026?",
"""
Solace Telecom — Managed WAN Agreement with Brisk Catering, Schedule 3 (Service Levels)

S3.1 Availability is measured per calendar month in minutes.
S3.2 Excluded from downtime: scheduled maintenance notified to the customer at least 5 days in advance.
S3.3 Service credits (percentage of that month's charge):
   availability below 99.9% — 5%
   availability below 99.5% — 10%
   availability below 99.0% — 25%
S3.4 Only the single highest applicable band is paid.

August 2026 service report
- Unplanned outage, 12 August: 95 minutes
- Scheduled maintenance, 22 August: 120 minutes (notified to Brisk Catering on 15 August)
- Monthly charge: $24,000

Email from Brisk Catering's IT manager:
"Your outages hurt us badly this month. We're claiming the 10% credit — please confirm."
""",
[("credit_5_percent", "Excluding the notified maintenance, availability was about 99.79%, below 99.9% but not below 99.5%."),
 ("credit_10_percent", "Excluding the notified maintenance, availability fell below 99.5%."),
 ("credit_25_percent", "Counting all downtime, availability fell below 99.0%."),
 ("credit_15_percent", "When availability falls below 99.9%, the 5% and 10% bands are added together, giving a combined 15% credit."),
 ("no_credit", "Availability stayed at or above 99.9% for the month.")],
"credit_5_percent", 3,
twin=T([("Unplanned outage, 12 August: 95 minutes", "Unplanned outage, 12 August: 250 minutes")], "credit_10_percent")),

# ------------------------------------------------------------------ ct03
# why: failure at 20 months (< 24); earlier repair by Delta Pumps, which IS an approved service
# partner -> not unauthorised -> warranty applies. plant: supplier claims desk says void -> wrong.
# twin: repairer not in Schedule 4 -> unauthorised repair -> reject; plant agrees.
C("ct03", "How should Fenmoor Pumps handle warranty claim WC-5510?",
"""
Fenmoor Pumps — Warranty claim WC-5510
Customer: Oldmere Council (Leisure Services)
Product: FP-40 circulation pump, serial 40-88213
Delivered: 15 January 2025
Failure reported: 12 September 2026 (bearing seizure, about 20 months after delivery)
Service history: seal replaced in March 2026 by Delta Pumps Ltd.

Supply Terms, clause 9 (Warranty)
9.1 Products are warranted against defects for 24 months from delivery.
9.2 The warranty does not cover damage caused by misuse, or any product that has undergone an unauthorised repair.
9.3 "Unauthorised repair" means a repair carried out by anyone other than Fenmoor Pumps or an approved service partner listed in Schedule 4.
Schedule 4 — Approved service partners: Delta Pumps Ltd; Norland Fluid Services; Ashcombe Mechanical.

Claims desk note:
"Third-party repair on record — warranty void. Reject."
""",
[("repair_under_warranty", "The failure is within 24 months and the earlier repair was by an approved service partner."),
 ("reject_unauthorised_repair", "The earlier repair was by a company that is not an approved service partner."),
 ("reject_warranty_expired", "The warranty period in clause 9.1 runs for 18 months from delivery.")],
"repair_under_warranty", 2,
twin=T([("seal replaced in March 2026 by Delta Pumps Ltd.", "seal replaced in March 2026 by Brookside Hydraulics.")], "reject_unauthorised_repair")),

# ------------------------------------------------------------------ ct04
# why: increase limited to CPI, capped at 4%, with 60 days notice. Notice 20 Aug for 1 Nov = 73 days
# (ok). CPI 5.2% -> capped at 4%. Twin: CPI 3.1% -> CPI rate applies.
# plant: supplier claims full 6% -> wrong in both.
C("ct04", "What price increase must Brisk Catering accept from Hollis Dairy from 1 November 2026?",
"""
Brisk Catering — Supplier contract file: Hollis Dairy (milk and cream supply)

Clause 7 (Price adjustment)
7.1 The supplier may increase prices once per contract year.
7.2 Any increase may not exceed the annual Consumer Price Index figure most recently published before the notice, and in any case may not exceed 4%.
7.3 The supplier must give at least 60 days' written notice before the increase takes effect.
7.4 Increases that breach 7.2 take effect only up to the permitted amount.

Letter from Hollis Dairy, dated 20 August 2026:
"We will increase all prices by 6% from 1 November 2026. Your contract permits our full adjustment given rising feed costs."

Latest published annual CPI before 20 August 2026: 5.2%
Previous increase: November 2025 (contract year runs November to October).
""",
[("accept_6_percent", "The supplier's rising feed costs justify the full increase notified in its letter."),
 ("accept_4_percent_cap", "CPI is above 4%, so the increase is capped at 4%."),
 ("accept_cpi_rate", "CPI is below the 4% cap, so the increase is limited to the CPI figure."),
 ("reject_short_notice", "Notice of less than 90 days means no increase can take effect.")],
"accept_4_percent_cap", 2,
twin=T([("Latest published annual CPI before 20 August 2026: 5.2%", "Latest published annual CPI before 20 August 2026: 3.1%")], "accept_cpi_rate")),

# ------------------------------------------------------------------ ct05
# why: assignment to an affiliate (> 50% control) needs notice only; Quill is 40% owned by the
# supplier -> not an affiliate -> consent required. plant: "intra-group transfer" -> wrong.
# twin: Morrow holds 60% -> controls Quill -> Affiliate -> notice only (10 Sep -> 15 Oct = 35 days); plant agrees.
C("ct05", "How should Kingsway Analytics respond to the supplier's assignment notice?",
"""
Kingsway Analytics — Legal inbox, matter LG-2291
Agreement: Data Services Agreement with Morrow Research Ltd (supplier)

Clause 21 (Assignment)
21.1 Neither party may assign this agreement without the other party's prior written consent.
21.2 Either party may assign to an Affiliate by giving 30 days' written notice, without consent.
21.3 "Affiliate" means an entity that controls, is controlled by, or is under common control with the party; "control" means holding more than 50% of the voting shares.

Notice from Morrow Research, 10 September 2026:
"We are assigning the Data Services Agreement to Quill Services Ltd with effect from 15 October. As this is an intra-group transfer, no consent is required on your part."

Company registry extract attached by Kingsway's paralegal: Quill Services Ltd — shareholders: Morrow Research Ltd 40%; Parkland Ventures 60%.
""",
[("accept_assignment_on_notice", "Morrow controls Quill, so Quill is an Affiliate and 30 days' notice is enough."),
 ("consent_required_before_assignment", "Morrow does not control Quill, so Quill is not an Affiliate and prior written consent is needed."),
 ("agreement_terminates", "An attempted assignment to another company ends the agreement automatically on the date the assignment takes effect.")],
"consent_required_before_assignment", 2,
twin=T([("Morrow Research Ltd 40%; Parkland Ventures 60%", "Morrow Research Ltd 60%; Parkland Ventures 40%")], "accept_assignment_on_notice")),

# ------------------------------------------------------------------ ct06
# why: LDs 0.5% of price per COMPLETE week, cap 10%. Due 1 Jun, delivered 10 Jul = 39 days = 5 complete
# weeks -> 2.5% x 400,000 = 10,000. Twin: delivered 20 Aug = 80 days = 11 weeks -> 5.5% = 22,000.
# plant: supplier says 10,000 at most -> right in base, wrong in twin.
C("ct06", "What liquidated damages are due from Carrick Switchgear for late delivery?",
"""
Oldmere Council — Contract OC-2026-17, supply of substation switchgear
Contract price: $400,000
Contractual delivery date: 1 June 2026
Actual delivery date: 10 July 2026
Drawings approved by the Council: 14 March 2026 (on the date required by the programme)

Clause 18 (Delay)
18.1 If delivery is late, the supplier pays liquidated damages of 0.5% of the contract price for each complete week of delay.
18.2 Liquidated damages are capped at 10% of the contract price.
18.3 No damages are payable for delay caused by the Council.

Letter from Carrick Switchgear:
"We accept we were late. By our count liquidated damages come to $10,000 at most."
""",
[("ld_10000", "Delivery was 39 days late, which is 5 complete weeks, so 2.5% of $400,000 is due."),
 ("ld_22000", "Delivery was 80 days late, which is 11 complete weeks, so 5.5% of $400,000 is due."),
 ("ld_12000", "Delay is rounded up to 6 weeks, giving 3% of the contract price."),
 ("ld_11143", "Part weeks count pro rata: 39 days is about 5.57 weeks, giving about 2.79% of the price."),
 ("ld_40000", "Any late delivery triggers the full 10% cap.")],
"ld_10000", 2,
twin=T([("Actual delivery date: 10 July 2026", "Actual delivery date: 20 August 2026")], "ld_22000")),

# ------------------------------------------------------------------ ct07
# why: disclosure allowed to professional advisers only; prospective investors need consent.
# plant: CFO says investors are advisers -> wrong.
C("ct07", "May Kingsway share the Orbis licence agreement with Tenfold Capital?",
"""
Kingsway Analytics — Request from the CFO's office, 8 September 2026
Document: Software Licence Agreement with Orbis Mapping (contains pricing and service terms)
Proposed recipient: Tenfold Capital, a prospective investor in Kingsway's Series B round

Clause 12 (Confidentiality)
12.1 Each party keeps the terms of this agreement confidential.
12.2 A party may disclose the terms without consent to its professional advisers (lawyers, accountants, auditors) who are bound by a duty of confidence.
12.3 Any other disclosure, including to actual or prospective investors or lenders, requires the other party's prior written consent.
12.4 Redaction does not remove the need for consent under 12.3.

CFO email:
"Investors are advisers in all but name — send Tenfold the full agreement today."
""",
[("share_now", "Investors act as professional advisers during a funding round."),
 ("obtain_orbis_consent_first", "A prospective investor is not a professional adviser, so Orbis must consent in writing before disclosure."),
 ("share_redacted_copy_now", "A redacted copy can be shared without consent."),
 ("refuse_permanently", "The agreement's terms can never be shown to anyone outside Kingsway.")],
"obtain_orbis_consent_first", 1),

# ------------------------------------------------------------------ ct08
# why: termination for convenience after 6 months on 30 days notice; fee of 3 months' charges if
# effective within the first contract year. Start 1 Mar 2026, notice 20 Sep 2026 -> effective 20 Oct 2026
# (within year 1) -> terminate with fee. Twin: start 1 Aug 2025 -> beyond year 1 -> no fee.
# plant: vendor says fee applies -> right in base, wrong in twin.
C("ct08", "On what terms can Tamsin Road Properties end its facilities-software subscription?",
"""
Tamsin Road Properties — Notice to Brightdesk Software, sent 20 September 2026
"We give 30 days' notice to terminate the subscription for convenience."

Subscription Agreement (commencement date: 1 March 2026)
10.1 After the first 6 months from commencement, the customer may terminate for convenience on 30 days' written notice.
10.2 If termination for convenience takes effect within the first 12 months from commencement, the customer pays a termination fee equal to 3 months' subscription charges.
10.3 No fee is payable for termination taking effect after the first 12 months.
10.4 Monthly subscription charge: $2,300.

Brightdesk account manager reply:
"Happy to process it, but note the early termination fee applies."
""",
[("terminate_with_fee", "Termination takes effect within the first 12 months, so 3 months' charges are payable."),
 ("terminate_without_fee", "Termination takes effect after the first 12 months, so no fee is due."),
 ("cannot_terminate_yet", "The first 6 months from commencement have not passed, so termination for convenience is not yet available."),
 ("terminate_with_6_month_fee", "Termination in the first year costs six months' subscription charges."),
 ("terminate_immediately", "A convenience notice ends the subscription on the day it is sent.")],
"terminate_with_fee", 2,
twin=T([("(commencement date: 1 March 2026)", "(commencement date: 1 August 2025)")], "terminate_without_fee")),

# ------------------------------------------------------------------ ct09
# why: disputes must be raised within 15 days of the invoice date; raised 22 days after -> deemed
# accepted -> invoice stands. plant: customer controller says hold everything -> wrong.
C("ct09", "How should Harrowgate Freight's receivables team treat invoice HF-9920?",
"""
Harrowgate Freight — Receivables case file
Customer: Pellow Garden Supplies
Invoice HF-9920: $14,380.00, invoice date 1 September 2026, due 1 October 2026
Customer dispute email received: 23 September 2026 (22 days after invoice date), disputing a $2,100 detention charge

Customer Terms of Carriage, clause 16
16.1 The customer must notify any dispute about an invoice in writing within 15 days of the invoice date, stating the amount disputed and the reason.
16.2 Invoices not disputed under 16.1 are deemed accepted and payable in full by the due date.
16.3 Timely disputes suspend payment of the disputed amount only; undisputed amounts remain payable by the due date.

Email from Pellow Garden Supplies' financial controller:
"We never pay invoices with disputed items. Hold the whole invoice until you've reviewed it."
""",
[("invoice_stands_payable_in_full", "The dispute came after the 15-day window, so the invoice is deemed accepted in full."),
 ("hold_disputed_2100_only", "The disputed $2,100 is suspended and the rest is payable."),
 ("hold_whole_invoice", "A dispute about any line of an invoice suspends payment of the whole invoice until the review is finished."),
 ("cancel_and_reissue_invoice", "Disputed invoices are cancelled and reissued.")],
"invoice_stands_payable_in_full", 2),

# ------------------------------------------------------------------ ct10
# why: helpdesk is listed as CORE in Schedule 2 -> subcontracting needs prior written consent ->
# none -> issue breach notice. Twin: printing and postage (non-core) -> permitted without consent.
# plant: supplier says no consent needed -> wrong in base, right in twin.
C("ct10", "What should the contract manager do about Solace Telecom's subcontracting notice?",
"""
Oldmere Council — Contract management log, Managed Services Contract MS-09 (supplier: Solace Telecom)

Clause 11 (Subcontracting)
11.1 The supplier may subcontract Non-Core Services without consent, giving written notice.
11.2 The supplier may not subcontract Core Services without the Council's prior written consent.
11.3 Subcontracting Core Services without consent is a material breach; the Council issues a breach notice requiring remedy within 30 days.

Schedule 2 — Core Services: network operations; first-line helpdesk; security monitoring. Non-Core Services: printing and postage; courier; catering at service reviews.

Solace notice, 2 September 2026:
"From 1 October our first-line helpdesk will be delivered by Ravel Contact Centres. This is routine and doesn't need your consent."

Consent requests received from Solace: none.
""",
[("accept_notice_permitted", "The subcontracted work is a Non-Core Service, which only needs notice."),
 ("issue_breach_notice", "First-line helpdesk is a Core Service and no consent was sought, which is a material breach."),
 ("terminate_contract_immediately", "Subcontracting any service without the Council's consent allows it to terminate the contract immediately.")],
"issue_breach_notice", 2,
twin=T([("From 1 October our first-line helpdesk will be delivered by Ravel Contact Centres.",
         "From 1 October our printing and postage will be delivered by Ravel Print & Mail.")],
       "accept_notice_permitted")),

# ------------------------------------------------------------------ ct11
# why: FM notice within 7 days of the event becoming known; flood known 2 Sep, notice 16 Sep = 14
# days -> relief only from the date of notice. plant: supplier claims everything since the flood -> wrong.
# twin: notice 6 Sep = 4 days after the flood -> full relief; plant agrees.
C("ct11", "Which missed deliveries are excused under the force majeure clause?",
"""
Brisk Catering — Supplier incident file: Kerrow Bakery (bread and rolls)

Event: Kerrow's main bakery flooded on 2 September 2026; Kerrow's operations manager was on site that morning.
Force majeure notice from Kerrow: received 16 September 2026
Missed deliveries: every scheduled delivery from 3 September to 25 September (daily)

Supply Agreement, clause 19 (Force majeure)
19.1 A party is not liable for failure to perform caused by a force majeure event (including flood) if it notifies the other party in writing within 7 days after becoming aware of the event.
19.2 If notice is given later than 7 days after the party becomes aware of the event, relief applies only from the date the notice is received.
19.3 Either party may terminate if a force majeure event continues for more than 60 days.

Kerrow's cover email:
"Force majeure covers everything since the flood, so none of the missed deliveries count against us."
""",
[("all_missed_deliveries_excused", "Notice arrived within 7 days of Kerrow learning of the flood, so every missed delivery is excused."),
 ("excused_from_16_september_only", "Notice came more than 7 days after Kerrow knew of the flood, so relief runs only from the date the notice was received."),
 ("no_relief_at_all", "Notice later than 7 days removes all force majeure relief, so every missed delivery since 3 September counts against the supplier."),
 ("agreement_terminated", "A flood at the supplier's main site ends the agreement.")],
"excused_from_16_september_only", 2,
twin=T([("Force majeure notice from Kerrow: received 16 September 2026", "Force majeure notice from Kerrow: received 6 September 2026")], "all_missed_deliveries_excused")),

# ------------------------------------------------------------------ ct12
# why: net 45 from receipt of a VALID invoice (must quote the PO). Original 1 Aug lacked PO; corrected
# invoice 20 Aug -> due 4 Oct. Paid 25 Sep -> not late -> no interest. Twin: original quoted the PO ->
# due 15 Sep -> paid 25 Sep late -> interest due.
# plant: supplier claims late -> wrong in base, right in twin.
C("ct12", "Is Fenmoor Pumps entitled to late-payment interest on invoice FP-3312?",
"""
Oldmere Council — Accounts payable query AQ-771
Supplier: Fenmoor Pumps
Invoice FP-3312: $9,600.00
First received: 1 August 2026 — the invoice did not quote a purchase order number.
Corrected invoice quoting PO-26-1180 received: 20 August 2026
Paid: 25 September 2026

Contract terms, clause 6 (Payment)
6.1 Payment is due 45 days after the Council receives a valid invoice.
6.2 A valid invoice must quote the Council's purchase order number.
6.3 Interest at 4% above base rate accrues on amounts paid after the due date.
6.4 Invoices are sent to the Council's accounts payable mailbox, not to individual officers.

Supplier email:
"We sent the invoice on 1 August. You paid late — please add interest to the next remittance."
""",
[("no_interest_due", "The valid invoice arrived on 20 August, making payment due on 4 October, so the 25 September payment was on time."),
 ("interest_due", "A valid invoice arrived on 1 August, making payment due on 15 September, so the 25 September payment was late."),
 ("interest_due_from_1_august", "Interest runs from the day any invoice is first received."),
 ("interest_due_from_20_august", "Interest runs from the date the corrected invoice arrived."),
 ("dispute_invoice", "Invoices without a purchase order number are void.")],
"no_interest_due", 2,
twin=T([("First received: 1 August 2026 — the invoice did not quote a purchase order number.", "First received: 1 August 2026 — the invoice quoted PO-26-1180."),
        ("Corrected invoice quoting PO-26-1180 received: 20 August 2026", "Duplicate copy of the same invoice received: 20 August 2026")],
       "interest_due")),

# ------------------------------------------------------------------ ct13
# why: variations above $25,000 are payable only with a change order signed by the named Client
# Representative BEFORE the work; site engineer's email is not that -> claim rejected. plant: wrong.
# twin: 22,000 <= 25,000 -> site engineer's written instruction suffices -> pay; plant agrees.
C("ct13", "How should the Council respond to Delcourt Civils' variation claim VC-08?",
"""
Oldmere Council — Contract OC-2025-31 (Harbour Road drainage), Delcourt Civils
Variation claim VC-08: additional culvert lining, 40 metres, $31,000
Work carried out: 3–14 August 2026
Instruction relied on: email from the Council's site engineer, 1 August: "Go ahead with the extra lining, it needs doing."

Clause 22 (Variations)
22.1 Variations valued at $25,000 or less may be instructed in writing by the Council's site engineer.
22.2 Variations valued above $25,000 are payable only if a change order signed by the Client Representative (named in Schedule 1: Director of Highways) is issued before the work starts.
22.3 Work carried out outside 22.1 or 22.2 is at the contractor's own risk and is not paid.

Site engineer's follow-up email, 18 August:
"I told them to go ahead — just pay it."

Change orders issued for VC-08: none.
""",
[("pay_claim_in_full", "The variation is within the site engineer's written authority, and he instructed it in writing before work started."),
 ("pay_first_25000_only", "The site engineer's authority covers the first $25,000 of any variation, so that part is paid and anything above it is not paid."),
 ("reject_claim", "The variation is above $25,000 and no change order signed by the Director of Highways was issued before the work."),
 ("refer_to_adjudication", "Any disputed variation must go to adjudication before a decision.")],
"reject_claim", 2,
twin=T([("Variation claim VC-08: additional culvert lining, 40 metres, $31,000", "Variation claim VC-08: additional culvert lining, 28 metres, $22,000")], "pay_claim_in_full")),

# ------------------------------------------------------------------ ct14
# why: processor must notify within 48 hours of becoming aware. Aware Mon 7 Sep 09:00; notified
# Wed 9 Sep 11:00 = 50 hours -> late -> record breach. Twin: notified Wed 08:00 = 47 hours -> compliant.
# plant: supplier says "two business days = compliant" -> wrong in base, right in twin.
C("ct14", "How should Kingsway record Lorne Cloud Services' breach notification under the processing agreement?",
"""
Kingsway Analytics — Supplier incident review SI-19
Processor: Lorne Cloud Services
Incident: misconfigured storage bucket exposed a customer export file
Lorne became aware: Monday 7 September 2026, 09:00 (per Lorne's own incident timeline)
Lorne notified Kingsway: Wednesday 9 September 2026, 11:00

Data Processing Agreement, clause 8
8.1 The processor must notify the controller of a personal data breach within 48 hours of becoming aware of it.
8.2 Late notification is recorded as a breach of this agreement and reported to the controller's vendor risk committee.
8.3 Notification must describe the data affected and the containment steps taken.

Lorne's covering note:
"We notified within two business days, so we're fully compliant with clause 8."
""",
[("notification_compliant", "Lorne notified within 48 hours of becoming aware."),
 ("record_late_notification", "Lorne notified 50 hours after becoming aware, beyond the 48-hour limit."),
 ("terminate_agreement", "Any personal data breach by a processor ends the processing agreement.")],
"record_late_notification", 2,
twin=T([("Wednesday 9 September 2026, 11:00", "Wednesday 9 September 2026, 08:00")], "notification_compliant")),

# ------------------------------------------------------------------ ct15
# why: clause requires public liability of at least $5m "including any excess layers"; $2m primary
# + $3m excess = $5m -> compliant. plant: procurement says suspend -> wrong.
C("ct15", "Does Brisk Catering's insurance meet the requirement in its catering concession?",
"""
Tamsin Road Properties — Supplier compliance check, Brisk Catering (café concession, Atrium Building)

Concession Agreement, clause 15 (Insurance)
15.1 The concessionaire must maintain public liability insurance with a limit of indemnity of not less than $5,000,000 for any one occurrence, which may be met by a primary policy together with any excess layers.
15.2 Certificates must be current and provided annually.
15.3 If cover falls short, the concessionaire must remedy within 14 days; the landlord may suspend trading only if it is not remedied.

Certificates received 3 September 2026 (both current to 31 August 2027):
- Primary public liability, Ardmore Insurance: $2,000,000 any one occurrence
- Excess layer, Castlebay Underwriting: $3,000,000 in excess of $2,000,000

Procurement comment:
"Primary is only $2m — suspend their trading until they fix it."
""",
[("compliant_no_action", "The primary policy and excess layer together give $5,000,000, which the clause allows."),
 ("suspend_trading", "Primary cover below $5,000,000 means trading is suspended at once."),
 ("request_remedy_within_14_days", "The primary policy alone is short of the $5,000,000 limit."),
 ("terminate_concession", "Insufficient insurance is grounds for immediate termination.")],
"compliant_no_action", 2),

# ------------------------------------------------------------------ ct16
# why: upward-only review: new rent is the higher of passing rent and market rent -> stays $48,000.
# Twin: clause allows upward or downward -> market $41,000 applies.
# plant: tenant claims drop -> wrong in base, right in twin.
C("ct16", "What is the rent from the 1 September 2026 review date?",
"""
Tamsin Road Properties — Lease file, Unit 4 Canal Yard (tenant: Pellow Garden Supplies)
Passing rent: $48,000 a year
Rent review date: 1 September 2026
Independent valuer's market rent at the review date: $41,000 a year

Lease, clause 5 (Rent review)
5.1 The rent is reviewed on every third anniversary of the term start.
5.2 From each review date, the rent is the higher of the rent payable immediately before the review date and the market rent at the review date.
5.3 Market rent is set by an independent valuer if the parties do not agree.

Tenant's letter, 4 September 2026:
"Market rent is lower, so our rent drops to $41,000 from the review date."
""",
[("rent_stays_48000", "The review can only keep rent the same or raise it, and market rent is lower."),
 ("rent_falls_to_41000", "The review resets rent to market rent, which is $41,000."),
 ("rent_rises_by_cpi", "When market rent is lower, rent rises by CPI instead."),
 ("rent_set_at_44500", "Where market rent is lower, the new rent is set halfway between the two figures."),
 ("review_postponed", "A lower valuation postpones the review to the next anniversary.")],
"rent_stays_48000", 2,
twin=T([("5.2 From each review date, the rent is the higher of the rent payable immediately before the review date and the market rent at the review date.",
         "5.2 From each review date, the rent is the market rent at the review date, whether higher or lower than the rent payable before it.")],
       "rent_falls_to_41000")),

# ------------------------------------------------------------------ ct17
# why: non-solicit bars soliciting; responses to general public job ads are expressly not
# solicitation -> proceed. Placement fee only on breach. plant: former supplier -> wrong.
C("ct17", "May Harrowgate Freight go ahead with hiring Tomas Irving?",
"""
Harrowgate Freight — Recruitment file
Candidate: Tomas Irving, formerly a route analyst at Kingsway Analytics
Source: applied on 10 September 2026 through Harrowgate's public job advert on its careers site
Kingsway services contract with Harrowgate: ended 30 April 2026

Services Contract, clause 25 (Non-solicitation)
25.1 During the contract and for 12 months after it ends, neither party may solicit for employment any person employed by the other party who was involved in the services.
25.2 Hiring a person who responds to a general advertisement not targeted at the other party's staff is not solicitation.
25.3 If 25.1 is breached, the party in breach pays a fee equal to 25% of the person's first-year salary.

Email from Kingsway's operations director:
"Hiring our ex-staffer breaches the non-solicit. Withdraw the offer or we'll invoice you."
""",
[("proceed_with_hire", "He applied through a general public advert, which the clause says is not solicitation."),
 ("withdraw_offer", "The 12-month non-solicitation period after the contract ended has not run out."),
 ("proceed_and_pay_placement_fee", "Hiring within 12 months is allowed only on payment of the 25% fee.")],
"proceed_with_hire", 2),

# ------------------------------------------------------------------ ct18
# why: audit needs 30 days' written notice, max once per 12 months. Last audit Aug 2025 (> 12 months
# before 15 Sep 2026). Notice 1 Sep for 15 Sep = 14 days -> too short -> reschedule. Twin: notice
# 10 Aug = 36 days -> proceed. plant: audit lead says notice fine -> wrong in base, right in twin.
C("ct18", "Can Oldmere Council's audit of Solace Telecom go ahead on 15 September 2026?",
"""
Oldmere Council — Supplier audit plan
Supplier: Solace Telecom (Managed Services Contract MS-09)
Proposed audit date: 15 September 2026
Written audit notice sent to Solace: 1 September 2026
Previous audit under this contract: 12–13 August 2025

Clause 27 (Audit)
27.1 The Council may audit the supplier's records relating to the contract no more than once in any 12-month period.
27.2 The Council must give at least 30 days' written notice of an audit.
27.3 If notice is too short, the audit is rescheduled to a date that satisfies 27.2; it is not cancelled.

Council audit lead's note on the plan:
"Notice is fine — keep the 15th, the team is booked."
""",
[("proceed_on_15_september", "At least 30 days' written notice was given and the last audit was more than 12 months earlier."),
 ("reschedule_audit", "Notice was given only 14 days before the audit date, so it must move to a later date."),
 ("cancel_audit_annual_limit", "An audit was already held within the last 12 months."),
 ("proceed_on_audit_lead_approval", "The audit lead's sign-off on the plan replaces the notice requirement.")],
"reschedule_audit", 2,
twin=T([("Written audit notice sent to Solace: 1 September 2026", "Written audit notice sent to Solace: 10 August 2026")], "proceed_on_15_september")),
]
