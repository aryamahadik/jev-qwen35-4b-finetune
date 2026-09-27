"""proc_longpolicy / supplier contracts, SLAs, SOWs and data processing terms."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ vd01
# why: Change Order 2 (from 1 Jul 2025) sets 99.9% target, 99.5-99.9 -> 5%. August: 4 h
# maintenance notified 7 days ahead (>= 5) and within 8 h is excluded; 2 h unplanned over
# 740 h measured = 99.73% -> 5% of £20,000 = £1,000. Termination needs three consecutive
# months below 98%: May, June yes, July no. Twin: notified 3 days ahead -> not Scheduled
# Maintenance -> 6 h down / 744 = 99.19% -> 10% = £2,000.
C("vd01", "What does the contract require for August 2025?",
"""
MASTER SERVICES AGREEMENT — SCHEDULE 3: SERVICE LEVELS
Customer: Wexford Mutual Insurance. Supplier: Corvane Hosting Ltd. Service: policy administration platform.

1. DEFINITIONS
1.1 "Measurement Period" means a calendar month.
1.2 "Scheduled Maintenance" means downtime that the Supplier notified to the Customer at least 5 Business Days in advance and which, in total, does not exceed 8 hours in the Measurement Period.
1.3 "Availability" means the hours in the Measurement Period, less Scheduled Maintenance, during which the platform was usable, divided by the hours in the Measurement Period less Scheduled Maintenance, expressed as a percentage.
1.4 "Monthly Fee" means the platform fee for the month: £20,000.

2. SERVICE LEVEL AND CREDITS
2.1 Target Availability is 99.5%.
2.2 If Availability falls below target, the Supplier credits the Customer: (a) 99.0% to below 99.5%: 5% of the Monthly Fee; (b) 98.0% to below 99.0%: 10%; (c) below 98.0%: 20%.
2.3 Credits are the Customer's sole financial remedy for missed Availability, except under 3.1.
2.4 Credits are applied to the next invoice and are capped at 20% of the Monthly Fee.

3. CHRONIC FAILURE
3.1 If Availability is below 98.0% in three consecutive Measurement Periods, the Customer may terminate the affected service without charge.

4. REPORTING
4.1 The Supplier issues a service report within 10 Business Days after each Measurement Period.
4.2 Disputes about the report are raised at the monthly service review.

5. SUPPORT HOURS
5.1 Priority 1 incidents are handled 24/7. Priority 3 incidents are handled 08:00 to 18:00 on Business Days.

6. SERVICE REVIEWS
6.1 The parties meet monthly to review the service report, open incidents and planned changes.
6.2 Minutes are circulated within five Business Days and are not binding unless signed as a Change Order.

CHANGE ORDER 2 — signed 18 June 2025, effective for Measurement Periods from 1 July 2025
CO1. In 2.1, the target becomes 99.9%.
CO2. Clause 2.2 is replaced: (a) 99.5% to below 99.9%: 5% of the Monthly Fee; (b) 99.0% to below 99.5%: 10%; (c) below 99.0%: 20%.
CO3. Clause 3.1 is unchanged.

SERVICE REPORT — AUGUST 2025 (744 hours)
• Planned upgrade, 4 hours on Sunday 17 August, notified by email to the Customer 7 Business Days in advance.
• Unplanned outage on 22 August: 2 hours (storage controller failure).
• No other downtime.
Earlier months: May 2025 Availability 97.6%; June 2025 97.9%; July 2025 99.95%.

CUSTOMER'S VENDOR MANAGER
"Please tell me what we are entitled to for August under the contract as it now stands."
""",
[("credit_1000", "The upgrade counts as Scheduled Maintenance, so 2 hours over 740 gives 99.73%, which falls in the amended 5% band: £1,000."),
 ("credit_2000", "All six hours of downtime count, giving 99.19% Availability, which falls in the amended 10% band: £2,000."),
 ("no_credit", "Measured on the Schedule 3 formula, Availability of about 99.7% is above the 99.5% target in clause 2.1, so no service credit is due for August."),
 ("terminate_chronic_failure", "Availability fell below 98% in May and June and has missed target repeatedly, so the Customer may treat it as chronic failure and terminate under clause 3.1.")],
"credit_1000", 3,
twin=T([("notified by email to the Customer 7 Business Days in advance", "notified by email to the Customer 3 Business Days in advance")], "credit_2000")),

# ------------------------------------------------------------------ vd02
# why: precedence Change Order > SOW > MSA > PO; SOW-7 expressly varies MSA 8.2 (as 8.3
# requires) -> 30 days. Invoice 1 Sep, paid 10 Oct = 39 days -> late -> interest.
# Twin: SOW omits the express reference -> cannot vary 8.2 -> 45 days -> on time.
C("vd02", "Is late-payment interest due on invoice INV-2291?",
"""
MASTER SERVICES AGREEMENT — Harrowby Retail Group plc and Salient Data Consulting Ltd

1. INTERPRETATION
1.1 "SOW" means a statement of work signed by both parties under this Agreement.
1.2 "Change Order" means a signed variation to a SOW.
1.3 Order of precedence, highest first: (a) Change Orders; (b) SOWs; (c) this Agreement; (d) any purchase order issued by the Customer.
1.4 "Business Day" means a day other than a weekend or public holiday.

6. PERSONNEL
6.1 The Supplier names a Delivery Lead for each SOW, who may be replaced only with the Customer's consent.

8. CHARGES AND PAYMENT
8.1 The Supplier invoices monthly in arrears.
8.2 The Customer pays each undisputed invoice within 45 days of the invoice date.
8.3 A SOW may vary clause 8.2 only if it expressly identifies clause 8.2 as the clause being varied.
8.4 Late payments carry interest at 4% a year above base rate from the due date until payment.
8.5 Terms printed on a purchase order do not vary this Agreement.

11. INTELLECTUAL PROPERTY
11.1 Deliverables vest in the Customer on payment.

12. CONFIDENTIALITY
12.1 Each party keeps the other's confidential information secret for five years after termination.

14. LIABILITY
14.1 Each party's liability under a SOW is capped at the charges paid under that SOW in the previous 12 months.

15. TERM
15.1 This Agreement runs for three years from 1 January 2024 and may be extended by agreement.
15.2 Termination of this Agreement ends all SOWs, unless the parties agree otherwise in writing.

SOW-7 — Loyalty Analytics Phase 2 (signed 2 June 2025)
Scope: redesign of loyalty data model and dashboards.
Charges: time and materials, capped at £180,000.
Payment terms: 30 days from invoice date (varying clause 8.2 of the Agreement).
Delivery Lead: Imran Castell.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

CHANGE ORDER 1 TO SOW-7 (signed 14 July 2025)
Adds a churn model workstream; increases the cap to £205,000. No other change.

PURCHASE ORDER PO-55810 (issued by Harrowby for SOW-7)
Printed terms on reverse: "Supplier invoices are payable 60 days from receipt."

PAYMENT HISTORY
• INV-2291 for August work, £21,600, dated 1 September 2025; not disputed.
• Paid by Harrowby on 10 October 2025.

HARROWBY ACCOUNTS PAYABLE EMAIL
"We pay everything on our PO terms, so we're comfortably inside the window. Please withdraw the interest claim."
""",
[("interest_due", "SOW-7 expressly varies clause 8.2 and outranks the Agreement, so payment was due in 30 days and payment on day 39 attracts interest."),
 ("no_interest_msa_terms", "The SOW does not validly vary clause 8.2, so the 45-day term applies and payment on day 39 was on time."),
 ("no_interest_po_terms", "The purchase order's printed terms allow 60 days from receipt of the invoice, and Harrowby paid on 10 October, well within that window, so no interest can be claimed."),
 ("interest_from_change_order", "Change Order 1 sits at the top of the order of precedence and replaced SOW-7's commercial terms from 14 July, so interest runs under the Change Order instead.")],
"interest_due", 2,
twin=T([("Payment terms: 30 days from invoice date (varying clause 8.2 of the Agreement).", "Payment terms: 30 days from invoice date.")], "no_interest_msa_terms")),

# ------------------------------------------------------------------ vd03
# why: Amendment 3 (events from 1 Jan 2025) sets a 150% cap for data-protection breaches:
# 1.5 x 240,000 = 360,000. Lost profits excluded (14.1): 410,000 - 60,000 = 350,000 < cap
# -> 350,000. Twin: claim arises from delayed delivery -> 125% cap = 300,000 -> 300,000.
C("vd03", "What is the maximum the supplier must pay on the Customer's claim?",
"""
SOFTWARE SERVICES AGREEMENT — Palisade Health Trust (Customer) and Tessellate Systems Ltd (Supplier)

1. DEFINITIONS
1.1 "Charges" means sums paid by the Customer under this Agreement, excluding VAT.
1.2 "Contract Year" means each 12-month period from 1 April.
1.3 "Data Protection Breach" means a breach by the Supplier of its data protection obligations in clause 19.
1.4 "Losses" means losses, damages, costs and expenses.

7. DELIVERY
7.1 The Supplier delivers each module by the date in the Implementation Plan.
7.2 Delay caused by the Customer extends the delivery date day for day.

14. LIMITATION OF LIABILITY
14.1 Neither party is liable for loss of profits, revenue or anticipated savings, whether direct or indirect.
14.2 Subject to 14.1 and 14.3, each party's total liability arising from events in a Contract Year is limited to 125% of the Charges paid in the 12 months before the event.
14.3 Nothing limits liability for death or personal injury caused by negligence, or for fraud.
14.4 Each party must take reasonable steps to mitigate its Losses.

19. DATA PROTECTION
19.1 The Supplier processes personal data only on the Customer's documented instructions.

22. DISPUTES
22.1 Disputes go first to the Contract Managers, then to mediation.

23. INSURANCE
23.1 The Supplier holds professional indemnity cover of £5 million and cyber cover of £2 million.
23.2 The level of insurance does not affect the limits in clause 14.

24. TERM
24.1 The Agreement runs for five years from 1 April 2022.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

AMENDMENT No. 3 — signed 9 December 2024
Applies to claims arising from events on or after 1 January 2025.
A1. New clause 14.2A: "For Losses arising from a Data Protection Breach, the limit in 14.2 is 150% of the Charges paid in the 12 months before the event."
A2. Clause 14.1 applies to all claims, including those under 14.2A.

CLAIM FILE — CL-0317
• Event: data protection breach on 11 March 2025, when the Supplier's misconfigured export exposed appointment data.
• Charges paid in the 12 months before 11 March 2025: £240,000.
• Customer's claim: £410,000, made up of forensic investigation and notification costs £350,000, and lost income from cancelled private clinics £60,000.
• No death or personal injury is alleged. Mitigation steps were taken promptly.

SUPPLIER'S IN-HOUSE COUNSEL
"Our standard position is 125%. Before we reply I want the figure the Agreement actually supports."
""",
[("pay_350000", "Without the £60,000 lost income the claim is £350,000, which is inside the 150% limit of £360,000 that governs this event."),
 ("pay_300000", "Liability is capped at 125% of the £240,000 Charges, so the most payable is £300,000."),
 ("pay_360000", "Once lost income is included, the claim of £410,000 exceeds the 150% limit, so the Supplier must pay the full data-protection cap of £360,000."),
 ("pay_410000", "Clause 14.3 removes the cap for serious breaches of this kind, so the whole £410,000 claim, including lost clinic income, is payable.")],
"pay_350000", 2,
twin=T([("Event: data protection breach on 11 March 2025, when the Supplier's misconfigured export exposed appointment data.",
         "Event: delayed delivery of the reporting module, due on 11 March 2025, which forced the Customer to run manual processes.")],
       "pay_300000")),

# ------------------------------------------------------------------ vd04
# why: Amendment (from 1 Mar 2025) cuts non-renewal notice to 60 days and requires it at
# legal@. Term ends 30 Sep 2025; notice to legal@ on 20 Jul = 72 days before -> valid ->
# contract ends 30 Sep. Twin: sent 8 Aug = 53 days -> too late -> renews 12 months.
C("vd04", "What happens to the contract at the end of September 2025?",
"""
SUBSCRIPTION AGREEMENT — Marlow Freight Services (Customer) and Routeplan Software Ltd (Supplier)

1. DEFINITIONS
1.1 "Initial Term" means two years from 1 October 2023, ending on 30 September 2025.
1.2 "Renewal Term" means each successive period of 12 months.
1.3 "Notice Address" means the address in clause 18.2.

3. TERM AND RENEWAL
3.1 This Agreement starts on 1 October 2023 and continues for the Initial Term.
3.2 It then renews automatically for successive Renewal Terms unless either party gives written notice of non-renewal at least 90 days before the end of the then-current term.

4. FEES
4.1 Fees are £4,200 a month, invoiced quarterly in advance. Fees for a Renewal Term may increase by no more than 5%.

16. TERMINATION
16.1 Either party may terminate for material breach not remedied within 30 days of notice.
16.2 The Customer may terminate for convenience during a term by paying the fees for the rest of that term.

18. NOTICES
18.1 Notices must be in writing and are effective on receipt.
18.2 Notices to the Supplier go to its registered office, marked for the attention of the Company Secretary.

19. SUPPORT
19.1 Support is available 07:00 to 19:00 on weekdays. Critical faults are answered within one hour.
19.2 Planned releases are notified two weeks in advance.

20. CONSEQUENCES OF ENDING
20.1 On expiry or termination the Supplier makes the Customer's data available for export for 30 days, then deletes it.
20.2 Fees paid in advance for any period after expiry are refunded.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

AMENDMENT — signed 20 February 2025, effective 1 March 2025
M1. In clause 3.2, "90 days" is replaced by "60 days".
M2. Clause 18.2 is replaced: "Notices to the Supplier go by email to legal@routeplan.example and are effective on the day sent."
M3. Nothing else changes.

CUSTOMER FILE
• 20 July 2025: Marlow's Head of Procurement emails legal@routeplan.example: "Please accept this as notice that Marlow will not renew the Agreement at the end of the Initial Term."
• 21 July 2025: automated acknowledgement received from legal@routeplan.example.
• 4 August 2025: email from Routeplan's account manager: "Our records show non-renewal needs 90 days, so you're renewed for another year. Happy to discuss a discount."
• Marlow has already signed with a replacement supplier starting 1 October 2025.
""",
[("contract_ends_30_september", "The amended clause needs only 60 days' notice to legal@, and notice given on 20 July was 72 days before the term ended, so the Agreement expires."),
 ("renews_for_12_months", "Notice of non-renewal did not arrive early enough before the end of the term, so the Agreement renewed automatically."),
 ("ends_on_payment_of_remaining_fees", "Marlow's email ends the Agreement early for convenience rather than by non-renewal, so under clause 16.2 it must pay the fees for the rest of the current term."),
 ("renews_invalid_notice_address", "Clause 18.2 requires notices to reach the registered office marked for the Company Secretary, so an email to a legal mailbox was not valid notice and the Agreement renewed.")],
"contract_ends_30_september", 2,
twin=T([("20 July 2025: Marlow's Head of Procurement", "8 August 2025: Marlow's Head of Procurement"),
        ("21 July 2025: automated acknowledgement", "9 August 2025: automated acknowledgement"),
        ("4 August 2025: email from Routeplan's account manager", "12 August 2025: email from Routeplan's account manager")],
       "renews_for_12_months")),

# ------------------------------------------------------------------ vd05
# why: order 10 Feb 2025 -> amendment (orders from 1 Jan 2025) gives 18 months from Delivery
# (= acceptance, 20 Mar 2025) -> ends 20 Sep 2026; failure 5 Sep 2026 inside -> repair; the
# supplier chooses repair or replace. Twin: ordered 10 Dec 2024 -> 12 months -> ended 20 Mar
# 2026 -> expired.
C("vd05", "How should the supplier handle the customer's claim for the failed pump?",
"""
SUPPLY AGREEMENT — Brenlow Water Services (Buyer) and Kestrin Pumps Ltd (Seller)

1. DEFINITIONS
1.1 "Products" means the pumps and spare parts listed in Schedule 1.
1.2 "Delivery" means the date the Buyer accepts the Products after inspection under clause 5, not the date of dispatch.
1.3 "Defect" means a failure in materials or workmanship, excluding fair wear of consumable seals and damage from use outside the operating manual.
1.4 "Order Date" means the date of the Buyer's purchase order.

5. INSPECTION AND ACCEPTANCE
5.1 The Buyer inspects Products within 20 Business Days after arrival and issues an acceptance certificate or a rejection notice.

9. WARRANTY
9.1 The Seller warrants that the Products will be free of Defects for 12 months from Delivery.
9.2 During the warranty period the Seller will, at its option, repair or replace a defective Product free of charge.
9.3 Warranty repairs do not extend the warranty period.
9.4 Outside the warranty period, repairs are chargeable at the rates in Schedule 4.

10. SPARES
10.1 The Seller keeps spare parts available for 10 years after the last supply of each model.

11. LIABILITY
11.1 The Seller is not liable for loss of production, however caused.

12. DELIVERY TERMS
12.1 Products are delivered carriage paid to the Buyer's nominated site. Risk passes on delivery to site; title passes on payment.

13. PRICE
13.1 Prices are fixed for each calendar year and may rise by no more than the change in the producer price index.

14. VARIATION
14.1 Any change to this Agreement must be in writing and signed by both parties.

COUNTERPARTS AND ELECTRONIC SIGNATURE
This document and any amendment to it may be signed electronically and in counterparts, each of which is an original and which together form one instrument.

WARRANTY AMENDMENT — agreed 5 December 2024
Applies to Products with an Order Date on or after 1 January 2025.
W1. In clause 9.1, "12 months" is replaced by "18 months".
W2. Clause 9.2 is unchanged.

CLAIM WR-8841
• Product: KP-420 booster pump, serial 42-19077.
• Order Date: 10 February 2025. Dispatched: 1 March 2025. Acceptance certificate: 20 March 2025.
• Failure: 5 September 2026; motor winding burnt out.
• Kestrin engineer's report: "Pump operated within the manual's limits. Insulation failure in the winding, a manufacturing fault."
• Brenlow's email: "We insist on a brand-new pump under warranty, not a repair."
• Kestrin's service desk asks for a decision.
""",
[("repair_under_warranty", "The 18-month period from the 20 March 2025 acceptance runs to 20 September 2026, so the Defect is covered and Kestrin may choose to repair."),
 ("chargeable_repair_expired", "The warranty period that applies to this pump, counted from Delivery, had ended before the failure, so repair is chargeable."),
 ("replace_with_new_pump", "Within the warranty period the Buyer may insist on a brand-new replacement for a defective Product, so Kestrin must supply a new pump rather than repair this one."),
 ("refuse_not_a_defect", "A burnt-out motor winding is wear from normal use, which the definition of Defect excludes, so the claim is refused and any repair is chargeable.")],
"repair_under_warranty", 2,
twin=T([("Order Date: 10 February 2025.", "Order Date: 10 December 2024.")], "chargeable_repair_expired")),

# ------------------------------------------------------------------ vd06
# why: Nimbra hosts in Estmark (Approved Region); v2 consent rule applies only outside the
# Approved Region; notice 2 Jun, 30 days elapsed by 10 Jul, no objection within 14 days ->
# may use. Silence-as-consent line in the notice is irrelevant. Twin: Qaravel (outside) ->
# prior written consent needed.
C("vd06", "What is the position on 10 July 2025 regarding the Processor's use of Nimbra Cloud?",
"""
DATA PROCESSING AGREEMENT — Orchard Lane Pharmacies (Controller) and Brightfile Records Ltd (Processor)

1. DEFINITIONS
1.1 "Sub-processor" means any third party engaged by the Processor to process Controller personal data.
1.2 "Approved Region" means the countries listed in Annex 4: Estmark, Norland, Vesterholm and the Lune Islands.
1.3 "Notice" means written notice to the Controller's privacy mailbox.

6. SUB-PROCESSORS
6.1 The Processor may use the Sub-processors listed in Annex 3.
6.2 To add a Sub-processor, the Processor must give at least 30 days' Notice before the Sub-processor begins processing.
6.3 The Controller may object on reasonable data protection grounds within 14 days of the Notice. If it objects, the Processor must not use the proposed Sub-processor for Controller data.
6.4 The Processor remains fully liable for its Sub-processors.

7. SECURITY
7.1 The Processor maintains the measures in Annex 2, including encryption at rest and annual penetration testing.

9. AUDIT
9.1 The Controller may audit once a year on 30 days' notice.

10. BREACH NOTIFICATION
10.1 The Processor notifies the Controller of any personal data breach without undue delay and in any event within 36 hours.

11. RETURN AND DELETION
11.1 At the end of the services the Processor returns or deletes Controller data, at the Controller's choice, within 30 days.

DATA PROTECTION
Personal information collected under this document is used only to administer it, is kept no longer than necessary, and may be shared with service providers who process it on the organisation's behalf. Individuals may ask for a copy of the information held about them.

12. VARIATION
12.1 This DPA may be varied only in writing signed by both parties. Statements in a Notice do not vary it.

DPA VERSION 2 — effective 1 May 2025
V1. New clause 6.5: "Where a proposed Sub-processor would process Controller personal data outside the Approved Region, the Processor must obtain the Controller's prior written consent; Notice alone is not enough."
V2. Clauses 6.2 to 6.4 continue to apply.

NOTICE RECEIVED — 2 June 2025, privacy mailbox
From Brightfile: "We intend to add Nimbra Cloud as a Sub-processor for backup storage. Nimbra will store Controller data in its data centre in Estmark. Processing will start no earlier than 3 July 2025. Silence will be taken as consent to this and to all future Sub-processors we may appoint."

CONTROLLER'S RECORDS
• No objection was sent. The privacy team discussed the notice on 10 June and took no action.
• 4 July 2025: Brightfile confirms backups have started with Nimbra.
• Today is 10 July 2025. The Head of Privacy asks what the DPA says about Nimbra now.
""",
[("may_use_after_notice", "Nimbra stores data inside the Approved Region, 30 days' Notice was given and no objection was made in time, so the Processor may use it."),
 ("needs_written_consent", "Nimbra would process data outside the Approved Region, so clause 6.5 requires the Controller's prior written consent, which was not given."),
 ("must_stop_objection_window_open", "The Controller can still object at any time before processing starts, so the Processor must stop until the privacy team decides."),
 ("consent_to_all_future_subprocessors", "By staying silent the Controller accepted Nimbra and any future Sub-processors named by Brightfile.")],
"may_use_after_notice", 2,
twin=T([("in its data centre in Estmark", "in its data centre in Qaravel")], "needs_written_consent")),

# ------------------------------------------------------------------ vd07
# why: Delivery Date moved to 17 Mar by Change Note 1; delivered 2 Apr = 16 days late = 2 weeks
# + part week -> 3 weeks x 0.5% = 1.5% of €240,000 = €3,600 (cap 5% not reached). FM notice
# for 20 Mar (Thu) flood sent 3 Apr, after the 5 Business Day limit (27 Mar) -> no relief.
# Twin: FM notice 24 Mar -> valid -> 9.4 removes LDs.
C("vd07", "What liquidated damages, if any, may the buyer deduct for order PO-7731?",
"""
EQUIPMENT SUPPLY CONTRACT — Alderbrook Foods (Buyer) and Hesketh Conveyors Ltd (Supplier)

1. DEFINITIONS
1.1 "Delivery Date" means the date stated in the purchase order, as changed by any signed Contract Change Note.
1.2 "Order Value" means the price of the order excluding VAT and installation.
1.3 "Business Day" means Monday to Friday excluding public holidays; there were no public holidays in March or April 2025.
1.4 "Force Majeure Event" means an event beyond a party's reasonable control, including flood and fire.

8. DELIVERY
8.1 The Supplier delivers the equipment to the Buyer's Leswick plant on the Delivery Date.
8.2 Delivery before the Delivery Date requires the Buyer's consent.

9. DELAY
9.1 If delivery is late, the Supplier pays liquidated damages of 0.5% of the Order Value for each week, or part of a week, of delay after the Delivery Date.
9.2 Liquidated damages are capped at 5% of the Order Value.
9.3 The Buyer may deduct liquidated damages from sums due to the Supplier.
9.4 No liquidated damages are payable for delay caused by a Force Majeure Event, provided the Supplier notifies the Buyer in writing within 5 Business Days after the event begins.

10. ACCEPTANCE TESTING
10.1 The Buyer runs acceptance tests within 10 Business Days after installation.

12. PAYMENT
12.1 60% of the Order Value is paid on delivery and 40% on acceptance.

13. TITLE AND RISK
13.1 Risk passes on delivery; title passes on payment of the delivery instalment.

14. VARIATION
14.1 Changes to scope, price or Delivery Date are made only by a Contract Change Note signed by both parties.

15. WARRANTY
15.1 The equipment is warranted for 24 months from acceptance.

16. DISPUTES
16.1 Disputes are referred first to the parties' project directors and then to expert determination.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

CONTRACT CHANGE NOTE 1 — signed 20 February 2025
Order PO-7731: the Delivery Date is changed from 3 March 2025 to 17 March 2025 to allow a design change to the incline section.

ORDER PO-7731
Order Value: €240,000. Actual delivery to Leswick: 2 April 2025.

SUPPLIER CORRESPONDENCE
• Letter dated 3 April 2025: "Our Brackton assembly hall flooded on 20 March 2025, a Force Majeure Event which delayed dispatch. We therefore claim relief under clause 9.4."
• Buyer's project engineer confirms the flood happened and was reported in the local press.
""",
[("deduct_3600", "Delay runs from the changed 17 March Delivery Date: 16 days is three weeks or part weeks at 0.5%, which is 1.5% of €240,000."),
 ("deduct_6000", "Delay is counted from the original 3 March Delivery Date, giving 30 days late, which is five weeks or part weeks at 0.5%, so 2.5% of €240,000 is deducted."),
 ("deduct_2400", "Clause 9.1 charges only for complete weeks of delay, and 16 days after 17 March is two complete weeks, so 1% of €240,000 is deducted."),
 ("no_deduction_force_majeure", "The Supplier gave notice of the flood within the time clause 9.4 allows, so no liquidated damages are payable.")],
"deduct_3600", 3,
twin=T([("Letter dated 3 April 2025", "Letter dated 24 March 2025")], "no_deduction_force_majeure")),

# ------------------------------------------------------------------ vd08
# why: invoice 10 May 2025 (issued after 1 Apr) -> 30-day dispute window; dispute 2 Jun = 23
# days -> valid; only disputed amount may be withheld -> pay undisputed £12,400.
# Twin: dispute 12 Jun = 33 days -> deemed accepted -> pay in full.
C("vd08", "How should accounts payable deal with invoice 5518?",
"""
FACILITIES SERVICES CONTRACT — Greyfield University (Client) and Cleanmark Services Ltd (Contractor)

1. DEFINITIONS
1.1 "Invoice Date" means the date printed on the invoice.
1.2 "Disputed Amount" means the part of an invoice that the Client disputes in a Dispute Notice.
1.3 "Dispute Notice" means a written notice identifying the invoice, the Disputed Amount and the reasons.

11. INVOICING AND PAYMENT
11.1 The Contractor invoices monthly for services delivered in the previous month.
11.2 The Client pays undisputed amounts within 30 days of the Invoice Date.
11.3 The Client may dispute an invoice by giving a Dispute Notice within 15 days of the Invoice Date. An invoice not disputed within that period is deemed accepted in full.
11.4 The Client may withhold only the Disputed Amount; the rest of the invoice must be paid on time.
11.5 Disputes are referred to the contract managers, who must meet within 10 days.

12. PERFORMANCE
12.1 Performance is measured against the key performance indicators in Schedule 2. Failures lead to service credits, not to withholding of payment.

13. STAFF
13.1 Contractor staff must hold a valid site induction card.

14. TERM
14.1 The contract runs for three years from 1 August 2023, with an option to extend by up to two years.

15. EXTRA WORKS
15.1 Work outside the routine specification must be ordered through a works request raised by the Client's estates helpdesk.
15.2 Extra works carried out without a works request are at the Contractor's risk.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

VARIATION No. 2 — effective for invoices issued on or after 1 April 2025
V1. In clause 11.3, "15 days" is replaced by "30 days".
V2. Clause 11.4 is unchanged.

INVOICE 5518 — Cleanmark Services Ltd
Invoice Date: 10 May 2025. Period: April 2025.
Line 1: routine cleaning, 12 buildings — £12,400.
Line 2: deep clean of the Harlan Library after flooding — £3,800.
Total: £15,200.

CLIENT RECORDS
• Dispute Notice sent to Cleanmark on 2 June 2025, disputing line 2 in full: "Deep clean was not ordered through a works request."
• Line 1 is not disputed.
• Contract managers are due to meet on 11 June 2025.
• Estates manager's note: "Hold the whole invoice until they sort out the library charge — that'll focus their minds."
""",
[("pay_undisputed_withhold_rest", "The Dispute Notice came within the 30 days now allowed, so line 2 may be withheld but the £12,400 undisputed amount must be paid."),
 ("pay_in_full_deemed_accepted", "The Dispute Notice came after the period the contract allows, so the invoice is deemed accepted and payable in full."),
 ("withhold_entire_invoice", "Once a valid Dispute Notice is given, the Client may hold the whole invoice until the contract managers resolve the dispute at their meeting."),
 ("withhold_as_service_credit", "The library deep clean is a performance issue under Schedule 2, so the Client deducts a service credit from line 1 and pays the rest of the invoice.")],
"pay_undisputed_withhold_rest", 1,
twin=T([("Dispute Notice sent to Cleanmark on 2 June 2025", "Dispute Notice sent to Cleanmark on 12 June 2025"),
        ("Contract managers are due to meet on 11 June 2025.", "Contract managers are due to meet on 20 June 2025.")],
       "pay_in_full_deemed_accepted")),

# ------------------------------------------------------------------ vd09
# why: Change Value counts all phases: 22k + 16k = 38k. Amendment raising the PM threshold to
# £50k is effective 1 Sep 2025; CR-14 approved 20 Aug 2025 -> £25k threshold -> needs JSC.
# Twin: approved 3 Sep 2025 -> £50k threshold -> PM approval suffices.
C("vd09", "What is the approval status of Change Request CR-14?",
"""
PROGRAMME AGREEMENT — Kellaway District Council (Authority) and Stratum Digital Ltd (Contractor)
Programme: Resident Services Portal

1. DEFINITIONS
1.1 "Change Request" means a proposal to change scope, timetable or price, submitted on the form in Schedule 6.
1.2 "Change Value" means the total additional price of a Change Request, including every phase or stage into which the Change Request is divided.
1.3 "Project Managers" means the Authority's and the Contractor's named project managers acting together.
1.4 "Joint Steering Committee" or "JSC" means the committee in clause 20, which meets monthly.

19. CHANGE CONTROL
19.1 A Change Request with a Change Value up to £25,000 may be approved by the Project Managers.
19.2 A Change Request with a Change Value above £25,000 must be approved by the JSC.
19.3 A Change Request may not be implemented until it has been approved at the right level.
19.4 Approved Change Requests are recorded in the change log within five Business Days.

20. GOVERNANCE
20.1 The JSC comprises two Authority directors and the Contractor's account director.
20.2 The JSC may delegate any approval by a written resolution.

21. RISK REGISTER
21.1 The Contractor maintains the risk register and reviews it weekly with the Authority.

22. PAYMENT MILESTONES
22.1 Charges are paid on completion of each milestone in Schedule 4, subject to the Authority's acceptance.

23. KEY PERSONNEL
23.1 The Contractor may not replace the named delivery lead without the Authority's consent.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

24. VARIATION
24.1 This Agreement may be varied only in writing signed by both parties; a variation takes effect on the date it states.

25. REPORTING
25.1 The Contractor submits a monthly highlight report covering progress, risks, issues and the change log.
25.2 Items raised in a highlight report are not approvals of any Change Request.

VARIATION AGREEMENT — signed 12 August 2025, effective 1 September 2025
VA1. In clauses 19.1 and 19.2, "£25,000" is replaced by "£50,000".
VA2. Clause 20.2 is unchanged.

CHANGE REQUEST CR-14 — Council Tax direct-debit journey
Phase A (design and build): £22,000. Phase B (integration testing): £16,000.
Approval: signed by both Project Managers on 20 August 2025.
JSC: not presented. No written delegation from the JSC exists.
Contractor's delivery manager: "Each phase is under the limit and anyway the threshold's going up — can we start Phase A on Monday?"
""",
[("valid_pm_approval", "CR-14 was approved when the £50,000 limit applied, so the Project Managers' signatures are enough and work can start."),
 ("refer_to_jsc", "The Change Value is £38,000 and on 20 August the Project Managers' limit was still £25,000, so CR-14 needs JSC approval before any work."),
 ("proceed_phase_a_only", "Phase A alone is under the Project Managers' limit, so it may proceed while Phase B waits for the JSC."),
 ("reject_and_resubmit", "A Change Request may not be split into phases, so CR-14 must be rejected and resubmitted as one item.")],
"refer_to_jsc", 2,
twin=T([("signed by both Project Managers on 20 August 2025", "signed by both Project Managers on 3 September 2025")], "valid_pm_approval")),

# ------------------------------------------------------------------ vd10
# why: amended 9.1 allows one audit per Contract Year (from 1 Apr) -> Nov 2024 audit was in
# 2024/25, so an August 2025 audit is allowed. Notice: 20 Business Days from Fri 1 Aug 2025 ->
# 4-8, 11-15, 18-22, 25-29 Aug -> earliest date 29 Aug; 18 Aug is too early -> offer 29 Aug.
C("vd10", "How should the supplier respond to the customer's audit request?",
"""
OUTSOURCED PAYROLL AGREEMENT — Linthorpe Housing Group (Customer) and Paysmith Bureau Ltd (Supplier)

1. DEFINITIONS
1.1 "Contract Year" means each 12-month period starting on 1 April.
1.2 "Business Day" means Monday to Friday excluding public holidays; there are no public holidays in August 2025 in the Supplier's jurisdiction.
1.3 "Audit" means an inspection of the Supplier's records, systems and premises relating to the services.
1.4 "Security Incident" means a confirmed unauthorised access to Customer data.

9. AUDIT
9.1 The Customer may carry out one Audit in any period of 12 months, on at least 30 days' written notice.
9.2 After a Security Incident the Customer may carry out an additional Audit on 5 Business Days' notice.
9.3 Each party bears its own costs of an Audit, unless the Audit reveals a material breach.
9.4 Auditors must sign the Supplier's visitor confidentiality form.

10. BUSINESS CONTINUITY
10.1 The Supplier tests its continuity plan twice a year and shares the summary results.

11. SUBCONTRACTING
11.1 The Supplier may not subcontract payroll calculation without consent.

12. CONFIDENTIALITY
12.1 Audit findings are confidential and may be shared only with the Customer's regulators and auditors.

13. SERVICE CREDITS
13.1 Late payroll runs attract a credit of 10% of the monthly fee.

14. TERM
14.1 The Agreement runs until 31 March 2028.

15. DATA SUBJECT REQUESTS
15.1 The Supplier helps the Customer answer requests from employees for their payroll data within five Business Days.

16. RECORDS
16.1 Payroll records are kept for six years after the end of the tax year to which they relate.
16.2 The Supplier keeps an access log for every system holding Customer data.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

AMENDMENT No. 1 — effective 1 April 2025
A1. Clause 9.1 is replaced: "The Customer may carry out one Audit in each Contract Year, on at least 20 Business Days' written notice."
A2. Clause 9.2 is unchanged.

AUDIT HISTORY
• Last Audit: 12–13 November 2024.
• No Security Incident has been reported in 2025.

REQUEST — email from Linthorpe's internal audit, Friday 1 August 2025
"We plan to audit payroll controls at your Norcaster office on Monday 18 August 2025. Please confirm attendance by your compliance lead."

SUPPLIER'S COMPLIANCE LEAD, INTERNAL NOTE
"They were here nine months ago — surely they can't come again until November."
""",
[("offer_date_from_29_august", "This is the first Audit of the 2025/26 Contract Year, but 20 Business Days' notice from 1 August runs to 29 August, so the date must move."),
 ("refuse_until_november", "Only one Audit is allowed in any 12 months, and the last was in November 2024, so no Audit may take place before November 2025."),
 ("confirm_18_august", "The Customer gave written notice and has not audited in this Contract Year, so the visit on 18 August must be accepted."),
 ("require_security_incident", "An Audit within a year of the previous one is allowed only after a Security Incident, and none has occurred.")],
"offer_date_from_29_august", 3),

# ------------------------------------------------------------------ vd11
# why: invoice footnotes cannot vary the MSA (2.3). Initial Term = 24 months from 1 Jan 2024,
# ending 31 Dec 2025; termination effective 5 Mar 2026 is after it -> no fee.
# Twin: Initial Term 36 months -> termination within Initial Term -> two months' fee.
C("vd11", "What does the customer owe on terminating the managed print services?",
"""
MANAGED PRINT SERVICES AGREEMENT — Caldmoor College (Customer) and Inkwell Office Systems Ltd (Supplier)

1. DEFINITIONS
1.1 "Initial Term" means 24 months from the Start Date of 1 January 2024.
1.2 "Monthly Charge" means the fixed monthly service charge of £3,150.
1.3 "Change Order" means a variation signed by authorised signatories of both parties.

RIGHTS OF THIRD PARTIES
No person other than the parties named in this document has any right to enforce its terms, except where the document expressly says otherwise.

2. ENTIRE AGREEMENT AND VARIATION
2.1 This Agreement is the entire agreement between the parties.
2.2 It may be varied only by a Change Order.
2.3 Terms or conditions printed on or attached to invoices, delivery notes or quotations have no effect.

8. SERVICES
8.1 The Supplier provides 42 multifunction devices, toner, maintenance and a help desk.
8.2 Engineers attend within 8 working hours of a fault report.

17. TERMINATION
17.1 Either party may terminate on 30 days' written notice.
17.2 If termination for convenience by the Customer takes effect during the Initial Term, the Customer pays a termination fee equal to two Monthly Charges.
17.3 On termination the Supplier removes the devices within 20 working days at its own cost.

18. DATA
18.1 Device hard drives are wiped to the recognised standard before removal, and a certificate is provided.

19. PAYMENT
19.1 The Customer pays invoices within 30 days. Payment of an invoice is not acceptance of anything other than the charges it lists.

20. NOTICES
20.1 Notices are given by email to the addresses in Schedule 1 and are effective on the next working day.

21. CONSUMABLES
21.1 Toner and maintenance kits are included in the Monthly Charge; paper is not.
21.2 Pages above 60,000 a month are charged at 0.4p mono and 3.1p colour.

22. RENEWAL
22.1 After the Initial Term the Agreement continues month to month until terminated under clause 17.

INVOICE FOOTNOTE — on Inkwell invoices since October 2025
"By paying this invoice the Customer accepts Inkwell's updated terms, including a termination fee of three Monthly Charges on any termination for convenience."

CUSTOMER RECORDS
• Caldmoor paid the October, November and December 2025 invoices on time.
• No Change Order has been signed since the Start Date.
• Termination notice for convenience sent on 3 February 2026; termination effective 5 March 2026.
• Inkwell's reply: "Under our current terms a fee of £9,450 is due."
""",
[("no_fee_payable", "Termination takes effect after the Initial Term ended, and invoice footnotes cannot vary the Agreement, so no termination fee is due."),
 ("pay_two_months_fee", "Termination takes effect within the Initial Term, so clause 17.2 requires a fee of two Monthly Charges, £6,300."),
 ("pay_three_months_fee", "By paying three invoices carrying the footnote without objection, the College accepted Inkwell's updated terms, so the three-month fee of £9,450 is due."),
 ("pay_charges_to_term_end", "A customer that terminates for convenience must keep paying the Monthly Charges for the rest of the current term, so Caldmoor owes the charges to term end.")],
"no_fee_payable", 2,
twin=T([("\"Initial Term\" means 24 months from the Start Date of 1 January 2024.", "\"Initial Term\" means 36 months from the Start Date of 1 January 2024.")], "pay_two_months_fee")),

# ------------------------------------------------------------------ vd12
# why: Site Rules update (from 1 Jun 2025): work at height needs £10m public liability; roof-top
# work with £5m cover -> refuse access until cover raised. Twin: ground-floor units -> no work at
# height -> £5m suffices -> grant access.
C("vd12", "What should the site security desk decide on the contractor's access request?",
"""
BRAYFORD LOGISTICS PARK — CONTRACTOR SITE RULES (issue 4)
Applies to all contractors working at any building on the Park.

1. DEFINITIONS
1.1 "Work at Height" means work in any place where a person could fall a distance liable to cause injury, including roofs, mezzanine edges and ladders above 2 metres.
1.2 "Certificate" means a current insurance certificate naming the contractor and showing the limit of cover.
1.3 "Permit" means a permit to work issued by the Park's facilities team.

2. INSURANCE
2.1 Every contractor must hold public liability insurance of at least £5 million per occurrence.
2.2 Contractors employing staff must hold employers' liability insurance of at least £10 million.
2.3 A Certificate must be produced at the security desk before first access.

3. PERMITS
3.1 A Permit is required for hot works, Work at Height, confined spaces and electrical isolation.
3.2 Permits are valid for one shift only.

4. VEHICLES
4.1 The site speed limit is 10 mph. Reversing requires a banksman.

5. INDUCTION
5.1 All contractor staff must complete the Park's 30-minute induction video before starting work.

6. WASTE
6.1 Contractors remove their own waste. Refrigerant must be recovered by a certified technician and recorded on a waste transfer note.

7. INCIDENTS
7.1 All accidents and near misses are reported to the security desk before the contractor leaves site.

8. BREACH OF RULES
8.1 The security desk may refuse or withdraw access from any contractor who does not comply with these Rules.

9. WORKING HOURS
9.1 Contractors may work from 07:00 to 19:00 Monday to Saturday. Other hours need written approval from facilities.

10. FIRE SAFETY
10.1 Contractors must know the nearest assembly point and must not obstruct fire exits or disable detectors without a Permit.

CONFIDENTIALITY OF RECORDS
Case files and correspondence relating to decisions under this document are kept confidential and are disclosed only to those who need them to make or review a decision, or where the law requires.

RULES UPDATE — effective 1 June 2025
U1. New clause 2.4: "Contractors carrying out Work at Height must hold public liability insurance of at least £10 million per occurrence."
U2. Clauses 2.1 to 2.3 are unchanged.

ACCESS REQUEST — 16 July 2025
Contractor: Ardent Climate Services Ltd.
Work: replacing roof-top HVAC units on Warehouse 3, using a scissor lift and roof edge protection.
Certificates produced: public liability £5 million per occurrence; employers' liability £10 million.
Permit: requested from facilities, pending.
Staff: four engineers, all inducted.
Note from Ardent's supervisor: "We've worked here since 2022 on the same insurance and never had a problem."
""",
[("refuse_until_cover_raised", "Under the June 2025 update this job involves Work at Height, which needs £10 million public liability, so access must wait until cover is raised."),
 ("grant_access", "The contractor's certificates meet the insurance levels required for this job, so access can be granted once the Permit is issued."),
 ("grant_access_past_record", "Ardent has worked at the Park since 2022 on the same £5 million cover without incident, so its existing Certificates remain acceptable for this job."),
 ("refuse_employers_liability", "Employers' liability cover of £10 million falls short of the level the Rules demand of contractors employing staff, so access must be refused until it is raised.")],
"refuse_until_cover_raised", 1,
twin=T([("replacing roof-top HVAC units on Warehouse 3, using a scissor lift and roof edge protection",
         "replacing ground-floor HVAC units in the plant room of Warehouse 3, working from floor level")], "grant_access")),

# ------------------------------------------------------------------ vd13
# why: 2025 purchases use the amended tiers (3% >= €400k, 5% >= €900k) on the whole amount.
# Net = 960,000 - 30,000 freight - 40,000 returns = 890,000 -> 3% = 26,700.
# Twin: returns €5,000 -> net 925,000 -> 5% = 46,250.
C("vd13", "What annual volume rebate is the distributor owed for 2025?",
"""
DISTRIBUTION AGREEMENT — Tarrant Garden Wholesale (Distributor) and Veltro Irrigation SpA (Manufacturer)

1. DEFINITIONS
1.1 "Rebate Year" means a calendar year.
1.2 "Annual Purchases" means the total invoiced value of Products bought by the Distributor in a Rebate Year, excluding freight charges and after deducting the value of Products returned for credit in that year.
1.3 "Products" means the irrigation products in Schedule A.

7. REBATE
7.1 The Manufacturer pays a rebate on Annual Purchases as follows: 2% if Annual Purchases are €500,000 or more; 4% if €1,000,000 or more.
7.2 The rebate rate applies to the whole of the Annual Purchases once a threshold is reached.
7.3 The rebate is paid by credit note by 31 March following the Rebate Year.

8. MARKETING SUPPORT
8.1 The Manufacturer contributes 50% of approved co-branded marketing costs, up to €15,000 a year. Marketing support is not part of Annual Purchases.

9. TERRITORY
9.1 The Distributor may not actively market the Products outside the Territory in Schedule B.

10. ORDERS AND DELIVERY
10.1 Orders are placed through the Manufacturer's trade portal. Freight is charged at cost on each invoice.
10.2 Products may be returned for credit within 90 days if unopened.

11. PAYMENT
11.1 Invoices are payable within 60 days. Overdue invoices do not affect the rebate.

12. TERM
12.1 This Agreement runs until 31 December 2027.

13. MINIMUM STOCK
13.1 The Distributor keeps a minimum stock of the core range listed in Schedule C.

14. REPORTING
14.1 The Distributor reports sell-out volumes by product each quarter. Sell-out figures do not affect Annual Purchases.

REBATE AMENDMENT — signed 28 November 2024, applying to the 2025 Rebate Year onwards
R1. Clause 7.1 is replaced: "The Manufacturer pays a rebate on Annual Purchases as follows: 3% if Annual Purchases are €400,000 or more; 5% if €900,000 or more."
R2. Clause 7.2 is unchanged.

2025 ACCOUNT SUMMARY — prepared by Veltro's credit control
Total invoiced to Tarrant in 2025: €960,000.
Of which freight charges: €30,000.
Products returned for credit in 2025: €40,000.
Marketing support paid in 2025: €12,000.

WAIVER
A failure or delay in enforcing any provision is not a waiver of it, and a waiver on one occasion does not apply to any other occasion or to any other provision.

TARRANT'S CLAIM LETTER
"Our invoices for the year came to €960,000, over the top tier. We expect a 5% rebate of €48,000."
""",
[("rebate_26700", "Net Annual Purchases are €890,000 after freight and returns, below the €900,000 tier, so 3% on the whole amount gives €26,700."),
 ("rebate_48000", "Invoices to Tarrant totalled €960,000 in 2025, above the top €900,000 tier, so the 5% rate applies to the whole amount and gives €48,000."),
 ("rebate_17800", "Annual Purchases of €890,000 fall in the 2% band, which gives €17,800."),
 ("rebate_14700", "Under clause 7.2 the 3% rate applies only to the slice of purchases above the €400,000 threshold, so 3% of €490,000 gives €14,700."),
 ("rebate_46250", "Net Annual Purchases of €925,000 reach the €900,000 tier, so 5% on the whole amount gives €46,250.")],
"rebate_26700", 2,
twin=T([("Products returned for credit in 2025: €40,000.", "Products returned for credit in 2025: €5,000.")], "rebate_46250")),
]
