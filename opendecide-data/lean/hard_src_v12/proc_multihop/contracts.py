"""proc_multihop / commercial contracts and supplier management (Brightwater
Hosting, Kinloch Estates, Halberd Systems, Merrow Packaging, Orla Facilities,
Sennet Analytics, Thornbury Construction)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ ct01
# why: June = 30 days = 43,200 min. Excluded: maintenance announced >= 72 h ahead
# (M1, 96 h). Counted: incident 180 + M2 120 (announced 24 h) = 300 min.
# Uptime = 1 - 300/43,200 = 99.31% -> below 99.5, not below 99.0 -> 10%.
# Twin: M2 announced 80 h ahead -> excluded -> 180 min -> 99.58% -> 5%.
C("ct01", "What service credit does Brightwater owe Kinloch Estates for June?",
"""
Brightwater Hosting — Master Services Agreement, Schedule 3 (Service Levels)

1. Definitions
1.1 "Monthly Uptime" = (minutes in the month − Downtime minutes) ÷ minutes in the month.
1.2 "Downtime": minutes in which the Hosted Service is unavailable, excluding Scheduled Maintenance.
1.3 "Scheduled Maintenance": maintenance announced to the Customer at least 72 hours before it starts.

2. Service credits (percentage of that month's hosting fee)
| Monthly Uptime | Credit |
| 99.9% or above | none |
| below 99.9% | 5% |
| below 99.5% | 10% |
| below 99.0% | 25% |

3. Credits are the Customer's sole remedy for availability failures.

Kinloch Estates — availability log, June (30 days)
| Event | Duration | Notice given |
| M1: database upgrade | 240 min | announced 96 hours before |
| INC-311: network outage | 180 min | none (unplanned) |
| M2: storage firmware patch | 120 min | announced 24 hours before |
""",
[("no_credit", "Every event except the network outage was maintenance, and one outage cannot bring uptime below 99.9%."),
 ("credit_5_percent", "Only the unplanned outage counts as downtime, which leaves uptime below 99.9% but not below 99.5%."),
 ("credit_10_percent", "The outage and the short-notice patch count as downtime, putting uptime below 99.5% but not below 99.0%."),
 ("credit_25_percent", "All three events count as downtime because the customer was affected by each of them, putting uptime below 99.0%.")],
"credit_10_percent", 3,
twin=T([("| 120 min | announced 24 hours before |", "| 120 min | announced 80 hours before |")], "credit_5_percent")),

# ------------------------------------------------------------------ ct02
# why: notice >= 90 days before 1 Jan 2027 (i.e. by 3 Oct 2026), in writing to the
# clause 18 address; email is not valid notice unless confirmed by letter, and the notice
# date is the letter's delivery. Letter delivered 10 Oct -> 83 days -> late -> renews.
# Twin: letter delivered 25 Sep -> 98 days -> terminates 31 Dec.
C("ct02", "What is the status of the Merrow Packaging supply agreement after Halberd's notice?",
"""
Merrow Packaging — Supply Agreement with Halberd Systems (extract)

Clause 3 (Term): The Agreement runs until 31 December 2026 and then renews automatically for successive 12-month periods unless either party gives notice of non-renewal at least 90 days before the renewal date (1 January).

Clause 18 (Notices)
18.1 Notices must be in writing and delivered by hand or recorded post to the address below.
18.2 A notice takes effect on the day it is delivered.
18.3 Email is not valid notice unless it is confirmed by a letter under 18.1, in which case the notice takes effect when the letter is delivered.
Address for Merrow: Legal Department, Merrow Packaging, 4 Quayside Road, Portlan.

Correspondence file
- 15 September 2026, email from Halberd procurement: "Please treat this as our notice of non-renewal."
- 10 October 2026, recorded-post letter from Halberd confirming the email, delivered to 4 Quayside Road the same day.
""",
[("terminates_31_december", "Halberd's notice took effect more than 90 days before 1 January, so the agreement ends on 31 December."),
 ("renews_for_12_months", "The notice only took effect when the letter arrived, which was less than 90 days before 1 January."),
 ("renews_month_to_month", "A late notice converts the agreement into a rolling monthly contract.")],
"renews_for_12_months", 2,
twin=T([("- 10 October 2026, recorded-post letter", "- 25 September 2026, recorded-post letter")], "terminates_31_december")),

# ------------------------------------------------------------------ ct03
# why: start 1 Mar 2025, 36 months (to 29 Feb 2028). Termination effective 31 Oct 2026 =
# end of month 20 -> after month 18 -> amendment: 25%. Remaining months Nov 2026-Feb 2028 =
# 16 x £4,000 = £64,000 -> £16,000.
# Twin: effective 31 Jul 2026 = end of month 17 -> 50% of 19 x £4,000 = £76,000 -> £38,000.
C("ct03", "What termination fee does Sennet Analytics owe under the Orla Facilities contract?",
"""
Orla Facilities — Services Contract with Sennet Analytics

Clause 2: Term of 36 months from 1 March 2025. Monthly fee £4,000.
Clause 14 (Termination for convenience)
14.1 The Customer may terminate for convenience on 60 days' written notice.
14.2 On such termination the Customer pays a fee equal to 50% of the monthly fees that would have fallen due for the rest of the term after the termination date.
14.3 Termination for Orla's material breach carries no fee.

Amendment No. 2 (signed 5 January 2026): in clause 14.2, "50%" is replaced by "25%" where the termination date falls after the end of the 18th month of the term.

Notice from Sennet (received 1 September 2026): "We terminate the contract for convenience with effect from 31 October 2026. The service has been fine; our needs have changed."
""",
[("fee_16000", "Termination falls after month 18, so 25% of the 16 remaining monthly fees is due."),
 ("fee_19000", "Termination falls after month 18, so 25% of the 19 remaining monthly fees is due."),
 ("fee_32000", "Clause 14.2 applies as written: 50% of the 16 remaining monthly fees."),
 ("fee_38000", "Termination falls before the end of month 18, so 50% of the 19 remaining monthly fees is due."),
 ("no_fee", "A termination with proper notice carries no fee.")],
"fee_16000", 3,
twin=T([("with effect from 31 October 2026", "with effect from 31 July 2026"), ("(received 1 September 2026)", "(received 1 May 2026)")], "fee_38000")),

# ------------------------------------------------------------------ ct04
# why: increase notice needs 60 days before the 1 Sep anniversary; received 20 June
# (73 days) -> valid. Increase = lower of CPI and 4%, CPI taken for the month three months
# before the anniversary (June) = 3.1% -> 3.1%. July's 5.2% is the wrong month.
C("ct04", "Which price increase should Kinloch Estates accept from Brightwater on 1 September?",
"""
Brightwater Hosting — Order Form 7 (Kinloch Estates), Pricing Terms

P1. Fees may be increased once a year, on the anniversary date of 1 September.
P2. Any increase may not exceed the lower of (a) CPI and (b) 4%.
P3. "CPI" means the annual change in the consumer price index published for the month three months before the anniversary date.
P4. Brightwater must give written notice of an increase at least 60 days before the anniversary date; if it does not, no increase applies that year.

Published CPI (annual change)
| Month | CPI |
| May | 2.8% |
| June | 3.1% |
| July | 5.2% |

Letter from Brightwater, received 20 June: "Owing to higher energy costs, fees will rise by 6.0% from 1 September."
""",
[("increase_6_0", "Brightwater gave notice in time and the rise reflects its actual costs."),
 ("increase_4_0", "CPI for the latest month is above 4%, so the rise is capped at 4%."),
 ("increase_3_1", "The reference CPI is below 4%, and notice was in time, so the rise is limited to that CPI."),
 ("no_increase", "The notice arrived too late, so no increase applies this year.")],
"increase_3_1", 2),

# ------------------------------------------------------------------ ct05
# why: billable users = named human users who signed in within the last 30 days before
# quarter end; service accounts excluded. Active 214 - service 6 = 208; committed 200 ->
# true-up 8 seats. Twin: service accounts 16 -> 198 -> below commitment -> no true-up
# (no credit for under-use).
C("ct05", "What should Halberd invoice Sennet for the Q2 seat true-up?",
"""
Halberd Systems — Subscription Terms (Sennet Analytics)

S1. Sennet commits to 200 seats per quarter.
S2. "Billable User": a named human user who signed in at least once in the 30 days before quarter end. Service accounts and API integrations are not Billable Users.
S3. If Billable Users at quarter end exceed the commitment, the excess is invoiced as a true-up for that quarter.
S4. No credit is given if Billable Users fall below the commitment.

Q2 usage report (quarter end 30 June)
| Metric | Count |
| Accounts provisioned | 260 |
| Accounts signed in during last 30 days | 214 |
| of which service accounts | 6 |
""",
[("true_up_60_seats", "Provisioned accounts exceed the commitment by 60."),
 ("true_up_14_seats", "Accounts active in the last 30 days exceed the commitment by 14."),
 ("true_up_8_seats", "After removing service accounts, active human users exceed the commitment by 8."),
 ("no_true_up", "Billable Users do not exceed the 200-seat commitment.")],
"true_up_8_seats", 2),

# ------------------------------------------------------------------ ct06
# why: due = 30 days from receipt at ap@ (1 Mar -> 31 Mar). £9,000 paid 15 Apr -> late ->
# interest. £3,000 disputed by notice on 8 Mar (within 10 days of receipt) -> no interest
# while disputed. -> interest on the undisputed part only.
C("ct06", "Should Merrow charge late-payment interest on invoice INV-8841, and on what?",
"""
Merrow Packaging — Standard Terms of Sale

7.1 Invoices are due 30 days after receipt. An invoice is received when it is delivered to the buyer's accounts payable address (ap@).
7.2 Interest at 8% above base rate accrues on overdue amounts from the day after the due date until payment.
7.3 A buyer may dispute part of an invoice by written notice within 10 days of receipt, giving reasons. Interest does not accrue on a properly disputed amount while the dispute is open.
7.4 Undisputed amounts must be paid by the due date.

INV-8841 to Thornbury Construction: £12,000
Delivered to ap@thornbury.example: 1 March
Thornbury notice, 8 March: "We dispute £3,000 (line 4, 600 pallets short-delivered). Delivery notes attached."
Payment received: 15 April, £9,000.
Dispute status: open.
""",
[("interest_on_full_amount", "The invoice was paid late, so interest runs on the whole £12,000."),
 ("interest_on_undisputed_part", "The £9,000 was paid after the due date, and the £3,000 was disputed properly in time."),
 ("no_interest", "Part of the invoice is in dispute, so no interest can be charged until it is resolved.")],
"interest_on_undisputed_part", 2),

# ------------------------------------------------------------------ ct07
# why: warranty 24 months from installation (10 Oct 2024) -> to 10 Oct 2026; fault
# 5 Sep 2026 -> in warranty. Ambient logged 38 C <= 40 C spec -> no exclusion -> repair.
# Twin: ambient 44 C -> outside spec -> exclusion -> chargeable repair.
C("ct07", "How should Halberd treat service call SC-2217 on chiller unit HC-40?",
"""
Halberd Systems — Equipment Warranty (standard)

W1. Each unit is warranted against defects for 24 months from the installation date shown on the commissioning certificate (not the delivery date).
W2. The warranty does not cover faults caused by operating the unit outside the Operating Specification.
W3. A unit with three or more warranty failures in 12 months is replaced rather than repaired.

Operating Specification (HC-40)
| Parameter | Limit |
| ambient temperature | 5 °C to 40 °C |
| supply voltage | 400 V ± 10% |

Unit HC-40, serial 88-1041, at Thornbury site office
Delivered: 20 August 2024
Commissioning certificate: installed 10 October 2024
Previous warranty failures: none
SC-2217, 5 September 2026: compressor tripped repeatedly. Controller log: highest ambient in last 90 days 38 °C; voltage within limits.
""",
[("repair_under_warranty", "The unit is inside 24 months from installation and was run within its specification."),
 ("chargeable_repair", "The warranty no longer covers this fault, either because of the unit's age or because it ran outside its specification."),
 ("replace_unit", "Repeated trips count as multiple failures, so the unit is replaced.")],
"repair_under_warranty", 2,
twin=T([("highest ambient in last 90 days 38 °C", "highest ambient in last 90 days 44 °C")], "chargeable_repair")),

# ------------------------------------------------------------------ ct08
# why: force majeure excludes labour disputes involving the supplier's own workforce
# (definition). Strike at Merrow's own plant -> not FM -> delay LDs apply.
C("ct08", "How should Thornbury respond to Merrow's delayed delivery?",
"""
Thornbury Construction — Purchase Contract with Merrow Packaging

Clause 11 (Delay): If delivery is late, Merrow pays liquidated damages of 1% of the order value per week of delay, up to 10%.
Clause 12 (Force majeure)
12.1 Neither party is liable for delay caused by a Force Majeure Event, provided the affected party notifies the other within 5 business days of its start.
12.2 "Force Majeure Event": an event beyond the reasonable control of the affected party, such as flood, fire, war or a strike at a third-party port. It does not include a labour dispute involving the affected party's own employees or subcontractors.
12.3 If a Force Majeure Event lasts over 60 days, either party may terminate.

Letter from Merrow, dated Tuesday 3 March (delivery was due 2 March)
"A strike by our own warehouse staff at the Portlan plant began on Monday 2 March. We declare force majeure under clause 12 and will deliver once the strike ends."
""",
[("apply_liquidated_damages", "A strike by Merrow's own staff is not a Force Majeure Event, so clause 11 applies to the delay."),
 ("accept_force_majeure", "Merrow notified within 5 business days of a strike, which is a Force Majeure Event."),
 ("terminate_contract", "A force majeure delay allows Thornbury to terminate straight away.")],
"apply_liquidated_damages", 1),

# ------------------------------------------------------------------ ct09
# why: completion due 1 Mar, extension of time 14 days (VO-3) -> revised date 15 Mar.
# Actual 5 Apr -> 21 days late = 3 complete weeks -> 3 x 0.5% = 1.5% of £480,000 =
# £7,200 (cap 10% = £48,000 not reached).
C("ct09", "What liquidated damages should Kinloch deduct from Thornbury's final account?",
"""
Kinloch Estates — Building Contract with Thornbury Construction (extract)

Contract price: £480,000
Completion date: 1 March
Clause 21 (Liquidated damages): 0.5% of the contract price for each complete week by which completion is later than the Completion Date, up to a maximum of 10% of the contract price.
Clause 22 (Extensions): where the Employer grants an extension of time, the Completion Date moves by that period.

Variation and extension register
| Ref | Detail | Extension granted |
| VO-1 | extra car-park lighting | none |
| VO-3 | late design change to roof plant | 14 days |
| VO-4 | client request for extra doors | refused |

Practical completion certified: 5 April.
""",
[("ld_7200", "After the 14-day extension the works finished three complete weeks late."),
 ("ld_12000", "The works finished five complete weeks after the original 1 March Completion Date, so five weeks of damages apply."),
 ("ld_48000", "Late completion triggers the 10% maximum."),
 ("ld_nil", "Once extensions are granted the Completion Date no longer applies.")],
"ld_7200", 2),

# ------------------------------------------------------------------ ct10
# why: assignment to an Affiliate needs no consent; Affiliate = controls, controlled by or
# under common control, control = more than 50% of voting rights. Halberd Holdings owns
# 45% of Novaline -> not an Affiliate -> consent required. Supplier's own view is not
# decisive.
C("ct10", "Does Halberd need Orla's consent to assign the contract to Novaline Services?",
"""
Orla Facilities — Framework Agreement with Halberd Systems

Clause 25 (Assignment)
25.1 Neither party may assign this Agreement without the other party's prior written consent, not to be unreasonably withheld.
25.2 Either party may assign to an Affiliate without consent, on written notice.
Clause 1 (Definitions)
"Affiliate": an entity that controls, is controlled by, or is under common control with a party.
"Control": ownership of more than 50% of the voting rights.

Letter from Halberd, 12 May
"Halberd Systems will assign the Agreement to Novaline Services Ltd from 1 July. Novaline is a Halberd group business: Halberd Holdings (our parent, owning 100% of Halberd Systems) holds 45% of Novaline's voting shares. Our legal team's view is that no consent is needed."
""",
[("notice_only_affiliate", "Novaline is a group business sharing Halberd's parent company, so it is an Affiliate and assignment needs only written notice."),
 ("consent_required", "The parent holds 50% or less of Novaline's votes, so Novaline is not an Affiliate and Orla must consent."),
 ("assignment_prohibited", "The Agreement cannot be assigned to anyone.")],
"consent_required", 2),

# ------------------------------------------------------------------ ct11
# why: Schedule 1 lists the service desk as a Core Service -> subcontracting needs prior
# written approval. Pendle is in-region, so the offshore bar does not apply.
C("ct11", "What does the contract require before Brightwater moves its first-line support to Pendle Contact?",
"""
Brightwater Hosting — Master Services Agreement (Kinloch Estates)

Clause 9 (Subcontracting)
9.1 Brightwater may not subcontract any Core Service without Kinloch's prior written approval.
9.2 Brightwater may subcontract other services on 30 days' written notice.
9.3 No Customer Data may be processed outside the United Region by Brightwater or any subcontractor.

Schedule 1 (Core Services): hosting and infrastructure; the first-line service desk; backup and restore.
Schedule 2 (Other Services): training; account management; document translation.

Brightwater notice, 4 February
"From 1 March our first-line service desk will be run by Pendle Contact Ltd from its centre in Harwick (United Region). This notice is given under clause 9.2."
""",
[("notice_is_sufficient", "Brightwater gave more than 30 days' written notice and Pendle is inside the United Region, which is all clause 9.2 requires."),
 ("obtain_kinloch_approval", "The service desk is a Core Service, so Kinloch must approve in writing first."),
 ("not_permitted_offshore", "Customer Data would be processed outside the United Region.")],
"obtain_kinloch_approval", 1),

# ------------------------------------------------------------------ ct12
# why: rejection is valid only if made within 10 business days of the delivery notice
# (2 Mar -> by 16 Mar) AND lists failures against the acceptance criteria. 13 Mar email
# gives no criteria -> not a valid rejection -> deemed accepted after 16 Mar -> invoice.
# Twin: email lists failures against AC-4 and AC-7 -> valid rejection -> fix and resubmit.
C("ct12", "On 17 March, what is the correct next step for Milestone 3?",
"""
Sennet Analytics — Statement of Work SOW-4 (Thornbury Construction)

A1. When a milestone deliverable is ready, Sennet issues a Delivery Notice.
A2. Thornbury may reject the deliverable within 10 business days of the Delivery Notice. A rejection must identify which acceptance criteria (AC) are not met.
A3. A deliverable not validly rejected within that period is deemed accepted, and Sennet may invoice the milestone.
A4. After a valid rejection, Sennet fixes the failures and issues a new Delivery Notice.

Milestone 3 — project cost dashboard. Acceptance criteria AC-1 to AC-8 (Appendix B).
Delivery Notice issued: Monday 2 March.
Email from Thornbury, Friday 13 March: "We're not happy with the look and feel of the dashboard. Please rework it before we sign off."
No other correspondence.
""",
[("invoice_milestone", "No valid rejection arrived within 10 business days, so the milestone is deemed accepted."),
 ("rework_and_redeliver", "Thornbury validly rejected the deliverable in time, so Sennet must fix it and issue a new notice."),
 ("wait_for_sign_off", "The milestone cannot be invoiced until Thornbury signs it off.")],
"invoice_milestone", 3,
twin=T([("\"We're not happy with the look and feel of the dashboard. Please rework it before we sign off.\"",
         "\"We reject Milestone 3: AC-4 (cost codes do not match the ledger) and AC-7 (export to spreadsheet fails) are not met.\"")], "rework_and_redeliver")),

# ------------------------------------------------------------------ ct13
# why: authority by cumulative change-order value: 60,000 + 45,000 + 30,000 = 135,000 =
# 6.75% of £2,000,000 -> over 5%, up to 15% -> Commercial Director.
# Twin: prior 40,000 + 20,000 -> 90,000 = 4.5% -> Project Manager.
C("ct13", "Who can approve change order CO-07 on the Thornbury depot project?",
"""
Kinloch Estates — Change Control Procedure (Thornbury depot contract)

1. Contract value: £2,000,000.
2. Approval authority depends on the cumulative value of all approved change orders on the contract including the one being approved:
 - up to 5% of contract value: Project Manager;
 - over 5% and up to 15%: Commercial Director;
 - over 15%: contract amendment signed by both chief executives.
3. Omissions (negative changes) are recorded separately and do not reduce the cumulative value.

Change order register
| CO | Description | Value | Status |
| CO-03 | additional drainage | £60,000 | approved |
| CO-05 | upgraded roller doors | £45,000 | approved |
| CO-06 | omit external canopy | −£25,000 | approved |
| CO-07 | extra EV charging bays | £30,000 | awaiting approval |
""",
[("project_manager", "CO-07 on its own is well under 5% of the contract value."),
 ("commercial_director", "Cumulative approved changes including CO-07 come to more than 5% but not more than 15% of contract value."),
 ("both_chief_executives", "The cumulative changes exceed 15% of contract value.")],
"commercial_director", 2,
twin=T([("| CO-03 | additional drainage | £60,000 | approved |", "| CO-03 | additional drainage | £40,000 | approved |"),
        ("| CO-05 | upgraded roller doors | £45,000 | approved |", "| CO-05 | upgraded roller doors | £20,000 | approved |")], "project_manager")),

# ------------------------------------------------------------------ ct14
# why: general cap = 125% of fees paid in the 12 months before the event = £750,000.
# Data-protection breach claims have their own £2,000,000 cap instead. Loss £1.4m is a
# data breach -> within super-cap -> recover £1.4m. Loss is direct (forensics, notices).
C("ct14", "How much of its loss can Orla recover from Sennet for incident DP-5?",
"""
Orla Facilities — Data Services Agreement with Sennet Analytics

Clause 16 (Limitation of liability)
16.1 Each party's total liability in any 12-month period is capped at 125% of the fees paid in the 12 months before the event giving rise to the claim.
16.2 Neither party is liable for indirect or consequential loss, including loss of profit.
16.3 Despite 16.1, liability for breach of Clause 10 (Data Protection) is capped at £2,000,000.

Fees paid by Orla in the 12 months before the incident: £600,000.

Incident DP-5: Sennet misconfigured a storage bucket, exposing Orla's staff records in breach of Clause 10.
Orla's direct losses (forensic investigation, notification letters, credit monitoring): £1,400,000.
Orla's claimed loss of profit on a delayed tender: £300,000 (claimed separately).
""",
[("recover_1_4m", "The breach falls under the £2,000,000 data protection cap, which covers the full direct loss."),
 ("recover_750k", "Liability is capped at 125% of the £600,000 fees paid."),
 ("recover_1_7m", "Both the direct loss and the lost profit fall within the £2,000,000 cap."),
 ("recover_nothing", "Data breaches are excluded as indirect loss.")],
"recover_1_4m", 2),

# ------------------------------------------------------------------ ct15
# why: disclosure permitted to Affiliates and professional advisers (defined: lawyers,
# auditors, accountants). A marketing consultant is neither -> needs the discloser's prior
# written consent; signing an NDA does not substitute.
C("ct15", "May Kinloch's asset manager share Brightwater's pricing schedule with Fennick Consulting?",
"""
Brightwater Hosting — Mutual Non-Disclosure Agreement with Kinloch Estates

4. Permitted disclosure. The Recipient may disclose Confidential Information only:
 (a) to its employees and Affiliates who need to know it and are bound by equivalent obligations;
 (b) to its professional advisers, who are bound by professional duties of confidentiality;
 (c) to anyone else with the Discloser's prior written consent.
1. Definitions: "Professional advisers" means lawyers, auditors and accountants.
5. Exclusions: information that is public, or already known to the Recipient without restriction, is not Confidential Information.

Email from Kinloch's asset manager
"I'd like to send Brightwater's pricing schedule (marked Confidential) to Fennick Consulting, the marketing consultancy helping us benchmark IT costs. Fennick will sign our standard NDA first."
""",
[("share_freely", "Pricing schedules are commercial information that falls outside the NDA."),
 ("share_after_fennick_signs_nda", "Once Fennick signs Kinloch's standard NDA it is bound by equivalent confidentiality obligations, so the disclosure is allowed."),
 ("get_brightwater_written_consent", "Fennick is neither an Affiliate nor a professional adviser, so Brightwater must consent in writing first.")],
"get_brightwater_written_consent", 2),

# ------------------------------------------------------------------ ct16
# why: disputes after 15 days are barred, but manifest errors (arithmetic errors and
# duplicate charges) can be corrected within 6 months. Same PO line billed twice =
# duplicate -> credit note. Twin: complaint that the agreed rate is too high -> not a
# manifest error -> out of window.
C("ct16", "How should Merrow's credit control team respond to Thornbury's query on INV-8790?",
"""
Merrow Packaging — Standard Terms of Sale

8.1 The buyer must raise any dispute about an invoice within 15 days of the invoice date. After that the invoice is treated as accepted.
8.2 Despite 8.1, a manifest error may be corrected within 6 months of the invoice date.
8.3 "Manifest error" means an arithmetic error or a duplicate charge for the same goods.
8.4 Corrections are made by credit note.

INV-8790, dated 2 February, £18,240 (6 lines)
Query from Thornbury accounts, received 14 March:
"Lines 2 and 5 are both for PO-7741 line 3 (1,200 printed cartons). We have been billed twice for the same delivery. Please correct."
Merrow's delivery records: one delivery against PO-7741 line 3.
""",
[("issue_credit_note", "A duplicate charge is a manifest error, which can be corrected within 6 months."),
 ("decline_out_of_time", "The query came more than 15 days after the invoice date, so the invoice stands."),
 ("hold_for_manager_review", "Any query after 15 days has to be approved by a manager before action.")],
"issue_credit_note", 2,
twin=T([("\"Lines 2 and 5 are both for PO-7741 line 3 (1,200 printed cartons). We have been billed twice for the same delivery. Please correct.\"",
         "\"Line 5 (1,200 printed cartons) is priced at £2.40 each; we think the rate is too high compared with last year. Please reduce it.\""),
        ("Merrow's delivery records: one delivery against PO-7741 line 3.", "Merrow's records: line 5 matches the agreed price list.")], "decline_out_of_time")),

# ------------------------------------------------------------------ ct17
# why: 2% discount if payment is received (funds in Merrow's account) within 10 days of
# invoice date. Invoice 1 Apr; funds received 12 Apr (day 11) -> no discount. Short-paid
# £368 > £50 write-off limit -> request shortfall.
# Twin: funds received 10 Apr -> discount valid -> accept.
C("ct17", "What should credit control do about Kinloch's short payment on INV-8902?",
"""
Merrow Packaging — Credit Control Manual

1. Early settlement discount: 2% if payment is received within 10 days of the invoice date.
2. "Received" means cleared funds in Merrow's bank account, not the date the customer sends the payment.
3. If a customer takes a discount it has not earned, request the shortfall unless it is £50 or less, in which case write it off.
4. Accounts more than 60 days overdue are placed on stop and referred to the credit manager.
5. Statements are sent on the first working day of each month.

INV-8902 to Kinloch Estates: £18,400, dated 1 April.
Remittance advice from Kinloch: "Payment made 9 April, less 2% early settlement."
Bank statement: £18,032.00 credited 12 April.
""",
[("accept_discounted_payment", "The payment reached Merrow's account within 10 days of the invoice date, so the discount is earned."),
 ("request_shortfall", "The funds cleared after the 10-day window and the £368 shortfall is above the write-off limit."),
 ("write_off_difference", "The shortfall is small enough to write off.")],
"request_shortfall", 2,
twin=T([("£18,032.00 credited 12 April.", "£18,032.00 credited 10 April.")], "accept_discounted_payment")),

# ------------------------------------------------------------------ ct18
# why: MFN applies only to a Comparable Customer: same product, same region, annual volume
# within +/- 20% of Kinloch's (1,000). The other customer buys 1,300 (+30%) -> not
# comparable -> no adjustment. Audit right already used this year.
C("ct18", "Is Kinloch entitled to a price reduction under the most-favoured-customer clause?",
"""
Merrow Packaging — Supply Agreement with Kinloch Estates

Clause 6 (Most favoured customer)
6.1 Merrow will not charge Kinloch more than it charges any Comparable Customer for the same product.
6.2 "Comparable Customer": a customer in the same sales region buying the same product in an annual volume within 20% (above or below) of Kinloch's annual volume.
6.3 Kinloch may audit Merrow's pricing records once per calendar year.

Kinloch annual volume (product MP-12 storage crates): 1,000 units.
Audit already carried out this year: yes (February).

Kinloch's letter: "We have learned that Aspley Retail, also in the Northern region, pays 8% less than us for MP-12 crates. Aspley buys about 1,300 units a year. Please apply the same price to us."
""",
[("apply_price_match", "Aspley pays less for the same product in the same region, so Kinloch's price must match."),
 ("no_adjustment_not_comparable", "Aspley's volume is more than 20% above Kinloch's, so it is not a Comparable Customer."),
 ("audit_merrow_records", "Kinloch should audit Merrow's pricing records to verify Aspley's price.")],
"no_adjustment_not_comparable", 2),
]
