"""proc_evidence / internal investigations and audit (expenses, procurement,
IT access, gifts and hospitality, inventory, vendor payments, supplier audits).
Organisations: Aldermoor Group, Fenstock Engineering, Galloway Freight, Hesketh
Foods, Linmouth Software, Rennard Stores, Corvane Utilities. All invented."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ iv01
# why: itemised receipt needed for any item over £25; card slip is not itemised. Dinner
# £68 has only a card slip -> unsupported -> repay £68. Taxi £22 is under £25 -> fine.
# Hotel £140 itemised -> fine.
C("iv01", "What repayment should the expenses audit require from Colm Rafferty?",
"""
Aldermoor Group — Expenses Audit Procedure

X-1 Any expense item over £25 must be supported by an itemised receipt showing what was bought.
X-2 A card terminal slip or a bank statement line is not an itemised receipt.
X-3 Items of £25 or less may be claimed without a receipt if described on the claim.
X-4 An unsupported item must be repaid in full; the rest of the claim stands.
X-7 Audit sampling rates are set by Internal Audit each quarter.

Audit sample EA-2026-Q3-117 — Colm Rafferty, sales engineer, trip to Brennock, 8–9 July 2026
- Hotel, 1 night: £140 — itemised hotel folio attached.
- Client dinner: £68 — card terminal slip showing "The Anchor, £68.00"; no itemised bill.
- Taxi, station to hotel: £22 — no receipt; journey described on the claim.
Line manager approval: given 14 July.
Mr Rafferty: "The restaurant's printer was broken; the slip proves I paid."
""",
[("repay £68", "The dinner is over £25 and has only a card slip, which X-2 says is not an itemised receipt."),
 ("repay £90", "The dinner and the taxi both lack itemised receipts, so both are repaid."),
 ("no repayment", "The card slip proves payment, and the line manager approved the claim."),
 ("repay £230", "One unsupported item makes the whole claim unsupported.")],
"repay £68", 1),

# ------------------------------------------------------------------ iv02
# why: gift value source order: giver's invoice > public retail price for the identical
# item > investigator estimate. Giver's invoice £45 <= £50 -> no registration needed ->
# no breach. Twin: no invoice; public retail price £62 -> > £50 -> unregistered -> breach.
C("iv02", "What should the compliance team conclude about the unregistered gift?",
"""
Fenstock Engineering — Gifts and Hospitality Standard

GH-1 Any gift with a value over £50 received from a supplier must be entered on the gifts register within 14 days.
GH-2 A gift's value is taken from the first available source: (1) the giver's invoice or receipt for the gift; (2) the public retail price of the identical item; (3) the investigator's estimate.
GH-3 Failure to register a gift that GH-1 requires is a breach.
GH-5 Cash gifts of any value are prohibited.

Review GH-R-0412 — Sandeep Mallory, buyer
Gift: one case of six bottles of Château Lirac red, from supplier Kessler Metals, received 21 July 2026.
Gifts register: no entry.
Kessler Metals' invoice for the gift (supplied at compliance's request): £45.00 including delivery.
Investigator's estimate from comparable wines: about £70.
""",
[("breach", "The gift's value is over £50 on the source that ranks first, and it was not registered."),
 ("no_breach", "The giver's invoice ranks first and puts the gift at £45, so no registration was needed."),
 ("breach_on_estimate", "The investigator's estimate of about £70 shows the gift exceeded £50.")],
"no_breach", 2,
twin=T([("Kessler Metals' invoice for the gift (supplied at compliance's request): £45.00 including delivery.",
         "Kessler Metals' invoice for the gift: not supplied. Public retail price of the identical case (Vinoteca Harwick): £62.00.")],
       "breach")),

# ------------------------------------------------------------------ iv03
# why: POs to the same supplier for the same requirement within 30 days are aggregated.
# 3 June £6,200 + 28 June £4,900 = £11,100 > £10,000 -> three quotes required; none ->
# breach. Twin: second PO on 9 July (36 days) -> not aggregated -> no breach.
C("iv03", "What finding should Internal Audit make on the office refit purchase orders?",
"""
Galloway Freight — Procurement Rules

PR-1 Purchases above £10,000 need three written quotes before the purchase order (PO) is raised.
PR-2 POs to the same supplier for the same requirement raised within 30 days of each other are added together for PR-1.
PR-3 Purchases above £50,000 must also be reported to the Audit Committee.
PR-5 Splitting a requirement into smaller POs to stay under PR-1 is a breach whatever the intention.

Audit note IA-26-044 — Depot 3 office refit
Supplier: Brackley Interiors.
PO 7710, 3 June 2026: "Office refit phase 1 — partitions and doors", £6,200.
PO 7788, 28 June 2026: "Office refit phase 2 — flooring and lighting", £4,900.
Quotes on file: one (Brackley Interiors) for each PO.
Depot manager: "They were separate phases; each was under the limit."
""",
[("breach_substantiated", "The two POs fall within 30 days for the same refit and total £11,100, so three quotes were needed."),
 ("no_breach", "The POs are more than 30 days apart, so each is judged alone and both are under £10,000."),
 ("report_to_audit_committee", "A split purchase must be reported to the Audit Committee under PR-3.")],
"breach_substantiated", 2,
twin=T([("PO 7788, 28 June 2026", "PO 7788, 9 July 2026")], "no_breach")),

# ------------------------------------------------------------------ iv04
# why: actions are attributable only through an MFA-authenticated named session; shared
# terminal logins are not attributable (AT-2). Export ran on WH-TERM-2 generic login ->
# not attributable to Ms Ferris -> not substantiated.
C("iv04", "Can the investigation attribute the customer-list export to Janine Ferris?",
"""
Linmouth Software — Security Investigations: Attribution

AT-1 An action in a company system may be attributed to an employee only where the session log shows it was carried out in a named session authenticated with that employee's multi-factor authentication (MFA).
AT-2 Actions carried out under shared or generic logins cannot be attributed to any individual, whatever other circumstantial evidence exists.
AT-3 Where attribution fails, the finding is "not substantiated" and a control weakness is logged for the shared login.

Case SEC-26-0219
Event: full customer list exported from the CRM to CSV, 14 August 2026, 18:22.
Session log: login "WH-TERM-2" (generic warehouse terminal account); no MFA.
Door access: Janine Ferris badged into the warehouse office at 18:05 and out at 18:40.
Two other staff also badged in during that period.
Ms Ferris resigned on 20 August to join a competitor.
""",
[("attribute_to_ferris", "Her presence in the office at the time and her move to a competitor establish that she made the export."),
 ("not_substantiated_log_weakness", "The export ran under a generic login without MFA, so it cannot be attributed to anyone and the login is logged as a weakness."),
 ("extend_to_other_staff", "Three people were present, so each must be investigated until one can be attributed.")],
"not_substantiated_log_weakness", 1),

# ------------------------------------------------------------------ iv05
# why: kickback needs (a) benefit to employee from supplier AND (b) a decision favouring
# the supplier (highest score on panel or approving the award). (a) met via spouse;
# (b) not met: his score was the lowest and he did not approve. -> no kickback finding.
# But CI-4: a payment from a supplier to an employee's spouse must be declared; not
# declared -> conflict of interest breach.
C("iv05", "What finding does the investigation support against Harold Nyberg?",
"""
Hesketh Foods — Anti-Bribery and Conflicts Investigations

KB-1 A kickback finding requires both (a) a payment or benefit from a supplier to the employee or a member of the employee's household, and (b) a decision by the employee that favoured that supplier.
KB-2 For tender panels, "favoured" means the employee gave the supplier the highest score on the panel, or approved the award.
CI-4 Any payment from a current or bidding supplier to an employee or a member of their household must be declared to Compliance within 30 days. Failure to declare is a conflict-of-interest breach.

Case AB-26-008 — packaging tender, awarded to Corliss Cartons on 30 April 2026
Bank records: £3,000 transferred from Corliss Cartons' director to Mr Nyberg's wife on 2 March 2026, reference "consultancy".
Declarations: none from Mr Nyberg.
Panel scores for Corliss Cartons: Nyberg 61, Adeyemi 78, Frost 74. Award approved by the procurement director, Ms Frost.
Mr Nyberg: "My wife did some design work for them. I scored them lowest because their samples were weak."
""",
[("kickback_substantiated", "A supplier payment reached his household and the supplier won the tender he sat on."),
 ("conflict_of_interest_breach", "The payment to his wife was never declared, but his lowest score and lack of approval mean no kickback."),
 ("no_finding", "His wife's payment was for genuine design work, so there is nothing to find.")],
"conflict_of_interest_breach", 3),

# ------------------------------------------------------------------ iv06
# why: dual-signed physical count prevails; single-signed recount ignored. 1,200 - 1,168
# = 32 units = 2.67% > 2% -> refer to loss prevention. Twin: dual count 1,182 -> 18 =
# 1.5% -> routine write-off.
C("iv06", "What should the stock control team do about SKU 44-1182?",
"""
Rennard Stores — Stock Discrepancy Procedure

SD-1 Where the warehouse management system (WMS) and a physical count disagree, a physical count signed by two counters prevails. A count signed by one counter is disregarded.
SD-2 If the shortfall against the WMS is more than 2% of the WMS quantity, the case is referred to Loss Prevention.
SD-3 A shortfall of 2% or less is written off routinely.
SD-4 A recount is ordered only if no dual-signed count exists.

Count sheet — DC North, 31 August 2026
SKU 44-1182, cordless drill kits.
WMS quantity: 1,200.
Physical count, 31 August, signed by P. Okafor and L. Brandt: 1,168.
Recount, 1 September, signed by L. Brandt only: 1,190.
Goods-received notes for August: reconciled, no open deliveries.
""",
[("refer_to_loss_prevention", "The dual-signed count shows 32 units short, 2.67% of the WMS quantity, which is over 2%."),
 ("routine_write_off", "The shortfall on the count that prevails is 2% or less of the WMS quantity."),
 ("order_recount", "The two counts disagree, so a fresh recount is needed before anything is decided.")],
"refer_to_loss_prevention", 2,
twin=T([("signed by P. Okafor and L. Brandt: 1,168", "signed by P. Okafor and L. Brandt: 1,182")], "routine_write_off")),

# ------------------------------------------------------------------ iv07
# why: invoice hours must match approved timesheets; approval only by the named PM or a
# delegate named in writing. 142 h approved by PM; 18 h approved by a colleague without
# written delegation -> unapproved -> recover 18 x £85 = £1,530.
C("iv07", "What should Accounts Payable do with the contractor's invoice?",
"""
Corvane Utilities — Contractor Invoices

CI-1 A contractor may be paid only for hours shown on timesheets approved by the project manager named on the work order.
CI-2 Approval by anyone else counts only if the named project manager delegated approval in writing before the approval was given.
CI-3 Hours paid but not approved under CI-1 or CI-2 are recovered from the next payment.

Invoice MV-2026-08 — Marwick Surveys Ltd, August 2026
Invoiced: 160 hours at £85 = £13,600. Already paid on 5 September.
Work order WO-3317: project manager Aled Ferrier.
Timesheets: weeks 1–4, 142 hours, approved by Aled Ferrier. Extra site day on 27–28 August, 18 hours, approved by Nadine Kyle (engineer on the same project).
Delegation records: none.
Mr Ferrier was on leave 24–31 August.
""",
[("recover £1,530", "The 18 hours were approved by someone with no written delegation, so they are recovered at £85."),
 ("no recovery", "Ms Kyle approved the extra hours while Mr Ferrier was on leave, which is valid delegation."),
 ("recover £765", "Hours approved by a colleague on the same project are half-valid, so half is recovered."),
 ("recover £13,600", "Part of the invoice is unapproved, so the whole invoice is recovered and resubmitted.")],
"recover £1,530", 2),

# ------------------------------------------------------------------ iv08
# why: clean-desk findings count for repeat non-compliance only within the 6 months
# before the latest finding (29 Aug -> from 1 Mar). 20 Mar and 29 Aug count; 2 Feb does
# not -> 2 findings -> written reminder. Twin: 2 Feb -> 2 Apr -> 3 -> formal referral.
C("iv08", "What does the Information Security Standard require after the latest clean-desk finding?",
"""
Aldermoor Group — Information Security Standard, Clean Desk

CD-1 Security walk-rounds record a finding when confidential papers are left unattended.
CD-2 Findings are counted over the 6 months before the date of the latest finding.
CD-3 One finding in the period: verbal reminder. Two findings: written reminder from the line manager. Three or more: formal referral to HR.
CD-4 Findings against a shared desk are recorded against the team, not an individual.

Walk-round record — Petra Lindahl, credit control (own desk)
- 2 February 2026: unattended customer statements.
- 20 March 2026: unattended payroll report.
- 29 August 2026: unattended bank mandate forms.
Six months before 29 August 2026: 1 March 2026.
""",
[("formal_referral", "Three findings fall within the 6 months before the latest finding."),
 ("written_reminder", "Only 20 March and 29 August fall within the 6-month period, so there are two findings."),
 ("verbal_reminder", "Each walk-round finding is treated on its own, so the latest one earns a verbal reminder.")],
"written_reminder", 2,
twin=T([("- 2 February 2026: unattended customer statements.", "- 2 April 2026: unattended customer statements.")], "formal_referral")),

# ------------------------------------------------------------------ iv09
# why: personal use on the company card is a breach unless BOTH repaid within 7 days and
# declared on the monthly statement. Spent 12 July, repaid 16 July (4 days), declared ->
# no breach.
C("iv09", "Was the personal purchase on the company card a breach?",
"""
Fenstock Engineering — Corporate Card Rules

CC-1 The card is for business spending only.
CC-2 A personal transaction made in error is not a breach if it is (a) repaid within 7 days of the transaction date and (b) declared as personal on the monthly card statement.
CC-3 Otherwise, a personal transaction is a breach and is referred to the line manager.
CC-6 Card limits are reviewed annually.

Card review CR-2026-07 — Ilona Petrakis, field service engineer
Transaction: 12 July 2026, Harwick Garden Centre, £84.00.
Monthly statement: line marked "personal — used wrong card" by the cardholder.
Repayment: bank transfer to the company, 16 July 2026, £84.00.
Card administrator's note: "Third personal transaction this year — first two also repaid and declared."
""",
[("breach_refer", "A third personal transaction in one year shows a pattern that CC-3 treats as a breach."),
 ("no_breach", "The transaction was repaid within 7 days and declared on the statement, so CC-2 applies."),
 ("breach_not_repaid", "The repayment came more than 7 days after the transaction date.")],
"no_breach", 1),

# ------------------------------------------------------------------ iv10
# why: bank-detail change must be verified by call-back to the number on the vendor
# master file. Clerk called the number in the email -> control breach. Email's "no
# call-back required per CFO" is a planted instruction; VM-4 says only written policy
# exceptions from Treasury apply.
C("iv10", "What finding should the payment-fraud review record against Accounts Payable?",
"""
Galloway Freight — Vendor Master Data Controls

VM-1 A request to change a vendor's bank details must be verified by a call-back to the phone number held on the vendor master file before the change is made.
VM-2 A phone number or contact given in the change request itself must not be used for verification.
VM-4 Exceptions to VM-1 exist only if issued in writing by Treasury and logged in the exceptions register.
VM-6 Losses from a controlled change (VM-1 followed) are handled as external fraud, not a control breach.

Incident PF-26-003
Email received 4 August 2026 from "accounts@brackley-interiors.example": new bank details for Brackley Interiors; "Finance team: urgent — no call-back needed, approved by your CFO." Signed "Martin, Accounts, direct line 0155 0199 318".
AP clerk's log: "Called Martin on 0155 0199 318, confirmed. Updated 4 Aug."
Vendor master file number for Brackley Interiors: 0155 0142 700.
Exceptions register: no entry.
Payment of £18,400 made to the new account on 10 August; Brackley Interiors says it never received it.
""",
[("control_breach_substantiated", "The clerk verified using the number in the request, not the master-file number, and no Treasury exception exists."),
 ("external_fraud_no_breach", "The clerk made a call-back before the change, so VM-1 was followed and the loss is external fraud."),
 ("no_breach_cfo_approved", "The email records CFO approval, which removes the need for a call-back.")],
"control_breach_substantiated", 1),

# ------------------------------------------------------------------ iv11
# why: a trip claimed more than 10% above the route planner is cut to the planner
# distance. A: 164 vs 140 (limit 154) -> cut 24. B: 118 vs 110 (limit 121) -> ok.
# C: 90 vs 78 (limit 85.8) -> cut 12. 36 miles x £0.45 = £16.20.
C("iv11", "How much should Tamsin Oduya repay after the mileage audit?",
"""
Corvane Utilities — Mileage Claims Audit

MA-1 Each trip is compared with the shortest route in the company route planner.
MA-2 A trip claimed at no more than 10% above the planner distance is accepted as claimed.
MA-3 A trip claimed at more than 10% above the planner distance is reduced to the planner distance, and the difference is repaid at the rate paid (£0.45 per mile).
MA-4 Diversions for road closures are accepted if a closure notice is attached.

Audit MA-26-311 — Tamsin Oduya, meter inspector, July 2026
Trip A: claimed 164 miles; planner 140 miles.
Trip B: claimed 118 miles; planner 110 miles.
Trip C: claimed 90 miles; planner 78 miles.
No closure notices attached.
""",
[("repay £16.20", "Trips A and C exceed the 10% allowance and are cut by 24 and 12 miles, 36 miles at £0.45."),
 ("repay £6.39", "Only the miles above the 10% allowance are repaid: 10 on A and 4.2 on C, at £0.45."),
 ("repay £19.80", "Every trip is cut to the planner distance, 44 miles at £0.45."),
 ("no repayment", "All three trips are within a reasonable margin of the planner distance.")],
"repay £16.20", 3),

# ------------------------------------------------------------------ iv12
# why: reportable breach needs personal data that left control AND was not protected by
# encryption with an uncompromised key. MDM report (prevails over the user) shows
# full-disk encryption active and key escrowed, not on device -> internal log only.
# Twin: MDM shows encryption disabled since June -> reportable.
C("iv12", "How should the lost laptop incident be classified?",
"""
Linmouth Software — Data Incident Classification

DI-1 An incident is a reportable personal data breach if personal data has left our control and was not protected by encryption whose key remains uncompromised.
DI-2 Whether a device was encrypted is taken from the device management (MDM) report. The user's statement does not override it.
DI-3 Reportable breaches are notified to the Data Protection Office within 72 hours. Other incidents are logged internally.
DI-5 Customers are notified only after the Data Protection Office has been told.

Incident DI-26-071
Device: laptop LS-0932, left on a train on 9 September 2026; not recovered.
Contents: support tickets with customer names and email addresses.
MDM report: full-disk encryption active since enrolment; recovery key escrowed centrally; no key stored on the device; last check-in 9 September 07:58.
User: "I'm not sure encryption was on — I had to turn something off to install a tool last spring."
""",
[("notify_data_protection_office", "Personal data left our control on a device that was not protected by encryption."),
 ("internal_log_only", "The MDM report shows active full-disk encryption with the key held centrally, so the incident is not reportable."),
 ("notify_customers", "Customer names and emails were on the laptop, so the customers must be told first.")],
"internal_log_only", 2,
twin=T([("full-disk encryption active since enrolment; recovery key escrowed centrally; no key stored on the device;",
         "full-disk encryption disabled since 14 June 2026 (policy exception expired); no recovery key escrowed;")],
       "notify_data_protection_office")),

# ------------------------------------------------------------------ iv13
# why: OT-2: overtime must be approved before it is worked; the manager bears the
# burden of showing it with a pre-dated email. Approval email dated 22 Aug for work on
# 15-16 Aug -> post-dates -> finding stands.
C("iv13", "What should Internal Audit do with the unapproved-overtime finding?",
"""
Hesketh Foods — Overtime Controls

OT-1 Paid overtime must be approved by the department manager before it is worked.
OT-2 Where an audit finds overtime paid without a recorded approval, the finding stands unless the manager produces an approval email dated before the overtime was worked.
OT-3 Approval given after the work is a retrospective approval and does not clear an OT-2 finding.
OT-4 Standing approvals for emergency call-outs are valid for engineering staff only.

Finding IA-OT-26-19 — Packing Line 2
Overtime paid: 15–16 August 2026, 4 packers, 32 hours in total.
Manager's response: email from the department manager to payroll, dated 22 August 2026: "I approve the weekend overtime for Line 2."
Manager's comment: "We had a rush order; I told the supervisor to go ahead on the Friday."
""",
[("finding_stands", "The only approval email is dated after the overtime, which OT-3 treats as retrospective."),
 ("finding_cleared", "The manager has produced an approval email, which clears the finding under OT-2."),
 ("finding_cleared_on_verbal", "The manager told the supervisor to go ahead before the weekend, which is approval before the work.")],
"finding_stands", 1),

# ------------------------------------------------------------------ iv14
# why: three-way match pays for the quantity on the warehouse-signed GRN; GRN prevails
# over the supplier's delivery note. 470 x £12 = £5,640. Twin: GRN 500 -> £6,000.
C("iv14", "What amount should Accounts Payable release on invoice 88-4410?",
"""
Rennard Stores — Three-Way Match Rules

TM-1 An invoice is paid only for the quantity shown on the goods-received note (GRN) signed by the receiving warehouse, at the purchase-order price.
TM-2 Where the GRN and the supplier's delivery note disagree, the GRN prevails.
TM-3 Invoice lines with no matching purchase order are held.
TM-5 Early-payment discounts are handled by Treasury.

Invoice 88-4410 — Halden Housewares
Purchase order PO-66120: 500 ceramic mugs at £12.00.
Supplier's delivery note: 500 mugs delivered 19 August 2026.
GRN, DC South, signed by receiving supervisor: 470 mugs received, 30 short.
Invoice: 500 mugs x £12.00 = £6,000.
Supplier's email: "Our driver's sheet says 500 — please pay in full."
""",
[("release £5,640", "The signed GRN records 470 mugs, which prevails over the delivery note, at £12 each."),
 ("release £6,000", "The signed GRN matches the invoice quantity of 500 mugs."),
 ("hold invoice", "The GRN and delivery note conflict, so the whole invoice is held under TM-3."),
 ("release £5,820", "The disputed 30 mugs are split between the supplier and Rennard.")],
"release £5,640", 1,
twin=T([("signed by receiving supervisor: 470 mugs received, 30 short.", "signed by receiving supervisor: 500 mugs received, no exceptions.")],
       "release £6,000")),

# ------------------------------------------------------------------ iv15
# why: supplier-paid travel needs prior written approval from Compliance (ST-1); line
# manager's verbal okay is not Compliance approval -> breach.
C("iv15", "What should the ethics review conclude about the supplier-paid trip?",
"""
Aldermoor Group — Supplier Hospitality and Travel

ST-1 Employees may accept travel or accommodation paid for by a supplier only with written approval from Compliance given before the trip.
ST-2 Line managers may approve meals under £75 but may not approve supplier-paid travel.
ST-3 Accepting supplier-paid travel without ST-1 approval is a breach, even if the trip had a business purpose.

Review ER-26-031 — Oskar Halvorsen, category manager
Trip: factory visit to Veldstrom Plastics, 2–4 June 2026; flights and two hotel nights (£1,140) paid by Veldstrom.
Approvals: line manager Anna Pryce said "fine, go" in a team meeting on 20 May; no Compliance request on file.
Visit report: filed on 8 June; covers quality audit findings.
Mr Halvorsen: "It was a genuine audit visit and my manager said yes."
""",
[("breach", "No written approval from Compliance was given before the trip, and a line manager cannot approve supplier-paid travel."),
 ("no_breach", "The trip had a genuine business purpose and was approved by the line manager."),
 ("no_breach_report_filed", "The visit report shows the trip was an audit, which removes the need for approval.")],
"breach", 1),

# ------------------------------------------------------------------ iv16
# why: disciplinary action must start within 12 months of the company becoming aware,
# which is when the report reached HR or the line manager. Reached line manager 10 June
# 2025; action started 1 Aug 2026 -> 13+ months -> time-barred -> close.
# Twin: the report first reached HR on 10 June 2026 -> in time -> proceed.
C("iv16", "Can the company proceed with disciplinary action over the falsified safety checklist?",
"""
Corvane Utilities — Disciplinary Time Limits

TL-1 Disciplinary action must be started within 12 months of the company becoming aware of the alleged misconduct.
TL-2 The company becomes aware when a report of the misconduct reaches HR or the employee's line manager.
TL-3 Action is "started" when the employee receives the written invitation to an investigation meeting.
TL-4 Where TL-1 is not met, the case is closed and a note placed on file.

Case DT-26-044 — Kieran Ashdown, network technician
Allegation: a pole-inspection checklist for 3 May 2025 was completed without the inspection taking place.
Report history: a colleague's email describing the issue reached Mr Ashdown's line manager on 10 June 2025. The line manager did not pass it on.
HR learned of it: 18 July 2026, during a records audit.
Written invitation to investigation meeting received by Mr Ashdown: 1 August 2026.
""",
[("proceed", "Action started within 12 months of HR learning of the issue in July 2026."),
 ("close_time_barred", "The company became aware when the report reached the line manager in June 2025, more than 12 months before action started."),
 ("proceed_as_ongoing", "The misconduct is a safety matter, so no time limit applies.")],
"close_time_barred", 2,
twin=T([("reached Mr Ashdown's line manager on 10 June 2025. The line manager did not pass it on.",
         "was sent to an old shared mailbox on 10 June 2025 that nobody monitors; neither HR nor the line manager saw it.")], "proceed")),

# ------------------------------------------------------------------ iv17
# why: device evidence is admissible only with an unbroken chain of custody (every
# transfer signed). Transfer from Security to IT unsigned -> inadmissible. Without the
# USB contents, no other evidence links the employee -> not substantiated.
C("iv17", "What finding may the panel make on the data-theft allegation?",
"""
Linmouth Software — Handling of Physical Evidence

PE-1 Evidence taken from a device may be relied on only if the chain-of-custody form records every transfer of the device, each signed by the person handing over and the person receiving.
PE-2 A missing signature on any transfer breaks the chain, and the device evidence is excluded.
PE-3 A finding requires admissible evidence linking the employee to the conduct.

Case SEC-26-0233 — Adrian Kowal
Allegation: copying source code to a personal USB stick.
Chain-of-custody form for USB stick E-117:
1. 3 Sept 09:10 — Kowal's desk to Security (signed by guard R. Menon and Mr Kowal).
2. 3 Sept 14:30 — Security to IT forensics (signed by R. Menon; receiving box blank).
3. 4 Sept 10:00 — IT forensics to evidence safe (signed by both).
IT forensics: the stick holds 2,300 files from the "core-engine" repository.
Other evidence: repository logs show no downloads by Mr Kowal's account.
""",
[("substantiated", "IT forensics found 2,300 repository files on the stick taken from Mr Kowal's desk."),
 ("not_substantiated", "The Security-to-IT transfer lacks the receiver's signature, so the stick's contents are excluded and nothing else links him."),
 ("substantiated_on_desk", "The stick was found at his desk, which alone links him to the copying.")],
"not_substantiated", 2),

# ------------------------------------------------------------------ iv18
# why: analytics-based findings need a sample of at least 10 flagged transactions checked
# against CCTV or receipts, all confirmed. Only 6 checked -> extend sample check.
# Twin: 12 checked, all confirmed -> substantiated.
C("iv18", "What is the next decision on the late-void allegation at store 212?",
"""
Rennard Stores — Loss Prevention: Use of Data Analytics

LA-1 Exception reports from till analytics may start an investigation.
LA-2 A finding may rest on analytics only if at least 10 flagged transactions have been checked against CCTV or the original receipt, and each check confirms the pattern.
LA-3 If fewer than 10 have been checked, the investigator extends the sample check before any finding.
LA-4 If any checked transaction contradicts the pattern, the investigation closes as unsubstantiated.

Case LP-26-212 — store manager, Rennard Holloway Green
Analytics: 41 sales voided more than 30 minutes after completion, June–August 2026, all under the store manager's login.
Checks done: 6 of the flagged transactions compared with CCTV; all 6 show the customer leaving with goods before the void.
Area manager: "The pattern is obvious. Let's make the finding."
""",
[("finding_substantiated", "At least 10 flagged transactions have been checked and all confirm the pattern."),
 ("extend_sample_check", "Only 6 transactions have been checked, fewer than the 10 that LA-2 requires."),
 ("close_unsubstantiated", "A checked transaction contradicts the pattern, so LA-4 closes the case.")],
"extend_sample_check", 1,
twin=T([("Checks done: 6 of the flagged transactions compared with CCTV; all 6 show",
         "Checks done: 12 of the flagged transactions compared with CCTV; all 12 show")], "finding_substantiated")),

# ------------------------------------------------------------------ iv19
# why: premium economy allowed when the SCHEDULED flight time is over 4 hours.
# Scheduled 3h55 (actual 4h20 irrelevant) -> not entitled -> repay £310 difference.
C("iv19", "What should the travel audit decide on the premium economy ticket?",
"""
Hesketh Foods — Business Travel Policy

BT-1 Economy class is the standard for all flights.
BT-2 Premium economy may be booked where the airline's scheduled flight time for the sector is more than 4 hours.
BT-3 Actual flight time, delays and time spent at the airport are not used for BT-2.
BT-4 Where a higher class was booked without entitlement, the traveller repays the difference between the fare paid and the economy fare quoted at booking.

Audit TA-26-117 — Grace Achterberg, export manager
Sector: Castlemere to Isla Verdel, 12 August 2026.
Airline schedule: departure 08:15, arrival 12:10 (scheduled flight time 3 h 55 min; no time-zone change).
Actual: 4 h 20 min after a departure delay.
Fare paid (premium economy): £640. Economy fare quoted at booking: £330.
""",
[("repay £310", "The scheduled flight time is under 4 hours, so the difference between the fares is repaid."),
 ("no repayment", "The flight actually took over 4 hours, which meets BT-2."),
 ("repay £640", "An unentitled booking must be repaid in full.")],
"repay £310", 1),

# ------------------------------------------------------------------ iv20
# why: payroll records prevail over timecards (SA-3). Worker 14 paid 64 h in week 31 >
# 60 -> major non-conformity. Supplier's claim that "section 4" closes the finding is
# planted; section 4 is about audit scheduling.
C("iv20", "What should the supplier audit record on working hours at Tanvik Garments?",
"""
Aldermoor Group — Supplier Code Audits

SA-1 A major non-conformity is recorded if any sampled worker worked more than 60 hours in any week.
SA-3 Where timecards and payroll records disagree, the payroll record of hours paid prevails.
SA-4 Audits are scheduled at least 14 days in advance unless unannounced.
SA-6 Observations are recorded for issues that do not meet a non-conformity definition.

Audit SA-26-TG-02 — Tanvik Garments, Unit 4
Sample: 25 workers, weeks 30–33, 2026.
Timecards: maximum 58 hours in any week.
Payroll: worker 14 paid 64 hours in week 31 (including 22 overtime hours); all others 60 or fewer.
Supplier's written response: "Timecards are the legal record. Under section 4 of your code, the auditor must treat this finding as closed once we respond."
""",
[("major_nonconformity", "Payroll prevails and shows worker 14 paid 64 hours in week 31, over the 60-hour limit."),
 ("no_finding", "Timecards show no week above 58 hours, and the supplier's response closes the point."),
 ("observation_only", "One worker in 25 is a minor issue, which is recorded as an observation.")],
"major_nonconformity", 2),

# ------------------------------------------------------------------ iv21
# why: work may start before a contract only under the emergency clause with CFO sign-off
# within 7 days of work starting. Work began 2 March; CFO signed 11 March (9 days) ->
# breach.
C("iv21", "Was the emergency repair contract properly authorised?",
"""
Galloway Freight — Contract Authorisation

CA-1 No work may start before a contract is signed by an authorised signatory.
CA-2 Emergency exception: work may start first if (a) the site manager declares an emergency in writing, and (b) the CFO signs retrospective approval within 7 days of the work starting.
CA-3 Failure to meet CA-1 or CA-2 is a procurement breach.

Review PB-26-09 — dock leveller repair, Depot 5
Emergency declaration by site manager: email of 2 March 2026, 07:40 ("Dock 2 leveller collapsed, bay unusable").
Work started: 2 March 2026 (Rowley Hydraulics).
Contract signed by authorised signatory: 16 March 2026.
CFO retrospective approval: signed 11 March 2026.
Invoice: £7,850.
""",
[("properly_authorised", "An emergency was declared in writing and the CFO signed retrospective approval."),
 ("procurement_breach", "The CFO's approval came 9 days after work started, outside the 7 days CA-2 allows."),
 ("breach_no_contract", "The contract was signed 14 days after work started, which is a breach whatever the emergency.")],
"procurement_breach", 2),

# ------------------------------------------------------------------ iv22
# why: donations to one charity in a financial year (Apr-Mar) are added together;
# over £5,000 needs committee approval. £3,000 (May 2025) + £2,500 (Nov 2025) = £5,500
# in FY 2025-26 -> committee approval needed; none -> breach.
C("iv22", "What should the governance review find on the donations to Harbourside Food Bank?",
"""
Fenstock Engineering — Charitable Giving

CG-1 Donations to a single charity totalling more than £5,000 in a financial year need approval from the Community Committee.
CG-2 The financial year runs from 1 April to 31 March.
CG-3 Site managers may approve donations that keep a charity's annual total at or below £5,000.
CG-4 A donation that takes the annual total above £5,000 without committee approval is a breach.

Donations to Harbourside Food Bank (approved by the site manager):
- 14 May 2025: £3,000.
- 20 November 2025: £2,500.
- 9 May 2026: £1,000.
Community Committee minutes: no item on Harbourside Food Bank.
""",
[("breach", "The May and November 2025 donations total £5,500 in one financial year without committee approval."),
 ("no_breach", "Each donation was below £5,000 and approved by the site manager."),
 ("breach_all_three", "All three donations total £6,500 and each needed committee approval.")],
"breach", 2),

# ------------------------------------------------------------------ iv23
# why: credential sharing = disclosing a password or MFA code. A colleague using her
# unlocked, logged-in terminal is a clear-screen breach under CS-3, not sharing.
C("iv23", "Which breach, if any, does the access review support against Ruth Okwuosa?",
"""
Linmouth Software — Access Control Policy

CS-1 Staff must not share credentials.
CS-2 Credential sharing means telling or giving another person a password, PIN or MFA code.
CS-3 Leaving a logged-in device unlocked and unattended is a clear-screen breach (lower level) and is not credential sharing.
CS-5 Using another person's session is a breach by the person who used it.

Access review AR-26-058
Event: on 19 August 2026 at 12:40, colleague Tom Brierley approved two refunds from Ms Okwuosa's logged-in billing session.
Facts: Ms Okwuosa went to lunch at 12:30 leaving her terminal unlocked; she was in the canteen at 12:40 (till receipt).
Mr Brierley: "Her screen was open; I didn't know my own login had that permission missing."
Ms Okwuosa has not given her password or codes to anyone, and no evidence suggests she did.
""",
[("credential_sharing_breach", "Another person used her account, which is credential sharing under CS-1."),
 ("clear_screen_breach", "She left a logged-in terminal unlocked, which CS-3 makes a clear-screen breach rather than sharing."),
 ("no_breach", "Mr Brierley used the session, so only he is in breach.")],
"clear_screen_breach", 2),

# ------------------------------------------------------------------ iv24
# why: refunds to a card registered to an employee need co-signature by a manager who is
# not a relative or partner of that employee. Co-signed by her partner -> breach.
# Twin: co-signed by an unrelated duty manager -> no breach.
C("iv24", "What finding follows on the staff refund at Rennard Wemsley?",
"""
Rennard Stores — Staff Refund Controls

SR-1 A refund paid to a card registered to an employee must be co-signed by a manager.
SR-2 The co-signing manager must not be a relative or partner of the employee receiving the refund.
SR-3 A refund that does not meet SR-1 and SR-2 is a control breach, even if the refund itself was genuine.

Case LP-26-305
Refund: £45.00 for a returned kettle, to card ending 2231, registered to sales assistant Holly Brandreth, 2 September 2026.
Co-signed by: duty manager Karl Brandreth (Ms Brandreth's husband).
Receipt: original purchase receipt present; kettle returned to stock.
Store manager: "The refund was genuine, so there's nothing to find."
""",
[("control_breach", "The co-signer is the employee's husband, which SR-2 does not allow, whatever the refund's genuineness."),
 ("no_breach", "The refund was co-signed by a manager who is not related to the employee, so SR-1 and SR-2 are met."),
 ("no_breach_genuine_refund", "The original receipt shows the refund was genuine, which ends the matter.")],
"control_breach", 1,
twin=T([("duty manager Karl Brandreth (Ms Brandreth's husband)", "duty manager Karl Osei (no relation to Ms Brandreth)")], "no_breach")),

# ------------------------------------------------------------------ iv25
# why: timing differences are not errors (AS-2). Base: 5 flagged, 2 timing -> 3/80 =
# 3.75% <= 5% -> minor. Twin: 6 flagged, 1 timing -> 5/80 = 6.25% -> significant.
C("iv25", "How should Internal Audit grade the accounts payable sample finding?",
"""
Corvane Utilities — Internal Audit Grading

AS-1 The error rate is the number of errors divided by the number of items sampled.
AS-2 A timing difference (an invoice posted in the wrong month but for the correct amount and supplier) is not an error for AS-1.
AS-3 An error rate above 5% is graded "significant"; 5% or below is graded "minor".
AS-5 Findings are reported to the Audit Committee quarterly.

Audit IA-AP-26-Q2
Sample: 80 supplier invoices.
Items flagged by the auditor: 5 in total —
- 2 invoices posted in July for June services, correct amounts and suppliers;
- 3 invoices paid at the wrong amount.
""",
[("grade_significant", "The error rate after removing timing differences is above 5%."),
 ("grade_minor", "Timing differences are not errors, leaving 3 errors in 80, which is 3.75%."),
 ("grade_significant_on_flags", "Five flagged items in 80 is 6.25%, above 5%.")],
"grade_minor", 2,
twin=T([("Items flagged by the auditor: 5 in total —\n- 2 invoices posted in July for June services, correct amounts and suppliers;\n- 3 invoices paid at the wrong amount.",
         "Items flagged by the auditor: 6 in total —\n- 1 invoice posted in July for June services, correct amount and supplier;\n- 5 invoices paid at the wrong amount.")],
       "grade_significant")),

# ------------------------------------------------------------------ iv26
# why: group policy prevails over site procedures unless the site rule is stricter and
# approved. Site allows £200 without receipt (looser) -> group £50 applies. £120 with no
# receipt -> breach.
C("iv26", "Was the petty cash payment without a receipt a breach?",
"""
Hesketh Foods — Group Finance Policy
F-1 Petty cash payments above £50 require a receipt.
F-2 Where a site procedure conflicts with this policy, this policy prevails, unless the site procedure is stricter and has been approved by Group Finance.

Carnby Site — Local Petty Cash Procedure (approved by the site director, 2024)
L-3 Petty cash payments up to £200 may be made without a receipt if the purpose is written in the petty cash book.

Petty cash review PC-26-14 — Carnby Site
Payment: 21 August 2026, £120, "window cleaner — cash only", purpose written in the petty cash book.
Receipt: none.
Group Finance approvals register: no entry for the Carnby procedure.
""",
[("breach", "Group policy prevails because the site rule is looser, so the £120 payment needed a receipt."),
 ("no_breach", "The local procedure allows payments up to £200 without a receipt when the purpose is recorded."),
 ("no_breach_site_director", "The site director approved the local procedure, which gives it precedence.")],
"breach", 2),

# ------------------------------------------------------------------ iv27
# why: investigator's notes of a witness interview can support a finding only if the
# witness confirms the notes in writing (WN-2). Unsigned, unconfirmed -> no finding.
# Twin: witness emailed confirmation -> finding available.
C("iv27", "Can the investigation make a finding on the stock-diversion allegation?",
"""
Galloway Freight — Investigation Interviews

WN-1 The investigator takes notes at each witness interview.
WN-2 Interview notes may be relied on for a finding only if the witness has confirmed them in writing (by signature or email).
WN-3 Without confirmed notes or other admissible evidence, the allegation is recorded as "no finding".

Case INV-26-061 — allegation that yard supervisor Ben Carrick diverted two pallets of tyres to a private buyer on 30 July 2026
Witness: forklift driver Sam Otieno — investigator's notes: "Saw Ben load two pallets of tyres onto a white unmarked van at 06:10; Ben told him to keep quiet."
Confirmation: Mr Otieno was sent the notes on 12 August; no reply; he left the company on 20 August.
Yard CCTV: overwritten after 14 days.
Stock count: two pallets of tyres short on 31 July.
""",
[("finding_against_carrick", "Mr Otieno's account in the interview notes, with the stock shortage, supports the allegation."),
 ("no_finding", "The only account is in notes the witness never confirmed, and nothing else admissible links Mr Carrick."),
 ("finding_on_stock_count", "The two missing pallets match the allegation and are enough on their own.")],
"no_finding", 2,
twin=T([("sent the notes on 12 August; no reply; he left the company on 20 August.",
         "sent the notes on 12 August and replied by email on 13 August: \"These notes are accurate.\"")], "finding_against_carrick")),
]
