"""proc_trap / HR and finance operations: expenses, leave, pay, discipline,
payables, procurement, hiring (Dunmore Kline Engineering, Halvard Foods,
Sallowmere Council Services, Ostrander Media, Brackwell Pharmacy Group,
Tindall & Moss Architects)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ hf01
# why: base cap $220/night; amendment raises Port Anselm to $310 for stays from
# 1 Aug 2026. Stay 14-16 Jul (2 nights) -> old cap -> reimburse 2 x 220 = $440 of $578.
# Manager approval cannot exceed caps (E-7). Twin: 14-16 Sep -> $289 <= 310 -> in full.
C("hf01", "What should expense audit do with this hotel claim?",
"""
Dunmore Kline Engineering — Travel & Expense Policy

E-4. Hotel room rate cap: $220 per night, before taxes.
E-5. Claims above the cap are reimbursed up to the cap; the excess is the traveller's cost. The claim is not rejected.
E-7. A line manager's approval confirms the trip was for business. It cannot raise a cap. Only a CFO exception form can.

Amendment E-4a (effective for stays starting on or after 1 August 2026): for the high-cost cities Port Anselm and Veloria, the cap is $310 per night.

Claim EX-40922 — traveller Signe Aalto (structural engineer)
Hotel: Harbourline Hotel, Port Anselm
Stay: check-in 14 July 2026, check-out 16 July 2026 (2 nights)
Room rate: $289 per night before taxes; total claimed $578
Manager approval: "Approved — this client meeting was vital, please pay in full." (J. Moreau)
CFO exception form: none
""",
[("reimburse_in_full", "Port Anselm's $310 cap under E-4a applies to this stay, and $289 is below it."),
 ("reimburse_capped_440", "The stay began before 1 August, so the $220 cap applies and E-5 pays 2 × $220 = $440."),
 ("reimburse_manager_approved", "The line manager has approved payment in full because the meeting was vital, so the full $578 is paid."),
 ("reject_over_cap", "The nightly rate is over the $220 cap, so the hotel claim is rejected.")],
"reimburse_capped_440", 2,
twin=T([("check-in 14 July 2026, check-out 16 July 2026", "check-in 14 September 2026, check-out 16 September 2026")], "reimburse_in_full")),

# ------------------------------------------------------------------ hf02
# why: approval must come from the approver of record in the expense system (VP
# Marketing); forwarded emails, including a CEO's assistant's, are not approvals.
# -> route to approver of record. No twin.
C("hf02", "How should accounts payable process this sponsorship expense?",
"""
Ostrander Media — Expense Approval Standard (EAS-3)

3.1 Every expense over $1,000 must be approved in the expense system by the approver of record for the cost centre.
3.2 Emails, chat messages or verbal approvals, including those from senior executives or their assistants, are not approvals under 3.1. AP staff must not record them as such.
3.3 If the approver of record is absent for more than 5 working days, their named delegate in the system may approve.
3.4 Claims lacking a valid approval are routed to the approver of record; they are neither paid nor rejected.

Expense EXP-7713
Item: sponsorship of the Northfold Podcast Awards, $4,200
Cost centre: Marketing — approver of record: Adaeze Nwosu (VP Marketing), not absent
Status in system: awaiting approval
Submitter note: "CEO approved this personally — see the email from his executive assistant, attached. Please pay today so we keep the logo slot."
Attachment: email from the CEO's executive assistant: "Tomas says go ahead with the awards sponsorship."
""",
[("pay_ceo_approved", "The CEO's approval, relayed in writing by his assistant, outranks the VP and allows payment."),
 ("route_to_approver", "Under 3.2 the email is not an approval, so 3.4 sends it to Adaeze Nwosu."),
 ("reject_expense", "An expense without valid approval must be rejected and resubmitted from scratch."),
 ("route_to_delegate", "The approver of record is unavailable, so her delegate should approve under 3.3.")],
"route_to_approver", 1),

# ------------------------------------------------------------------ hf03
# why: immediate family includes grandparents of the employee's spouse/partner -> 5 days.
# Manager's view irrelevant. Twin: partner's aunt -> not listed -> 1 day.
C("hf03", "How much bereavement leave is this employee entitled to?",
"""
Halvard Foods — Leave Policy, section 9 (Bereavement)

9.1 Paid bereavement leave of 5 working days is given on the death of a member of the employee's immediate family.
9.2 "Immediate family" means: spouse or partner; child; parent; sibling; grandparent; grandchild; and the parent, sibling, grandparent or child of the employee's spouse or partner.
9.3 On the death of any other relative or close friend, 1 working day of paid leave is given.
9.4 A manager may add unpaid leave on request, but may not reduce paid leave below 9.1 or 9.3.

Leave request LR-2250
Employee: Teodor Brankovic, line supervisor, night shift
Reason: death of his partner's grandmother, funeral on Friday
Relationship recorded in HR: partner (registered cohabiting partner since 2019)
Manager comment: "It's his partner's grandmother, not his own. One day is plenty; we're short on nights."
""",
[("five_days_paid", "A grandparent of the employee's partner is named in 9.2, so 9.1 gives 5 days."),
 ("one_day_paid", "The deceased is a relative outside the 9.2 list, so 9.3 gives 1 working day."),
 ("one_day_manager_decision", "The manager decides bereavement leave for in-law relations and has chosen one day because of staffing."),
 ("three_days_paid", "In-law relations receive a reduced allowance of 3 working days.")],
"five_days_paid", 1,
twin=T([("Reason: death of his partner's grandmother", "Reason: death of his partner's aunt"),
        ("It's his partner's grandmother, not his own.", "It's his partner's aunt, not his own.")], "one_day_paid")),

# ------------------------------------------------------------------ hf04
# why: OT at 1.5x for hours over 40 for NON-EXEMPT; classification field decides, not
# salary. Non-exempt, 46 h -> 6 OT hours. Twin: Exempt -> no OT.
C("hf04", "How should payroll treat this week's hours?",
"""
Tindall & Moss Architects — Pay Rules (US office)

P-2. Employees classified Non-exempt are paid 1.5 times their regular rate for hours worked over 40 in a workweek (Sunday to Saturday).
P-3. Employees classified Exempt receive no overtime pay.
P-4. Being paid a salary does not make an employee Exempt. Classification is recorded by HR in the "FLSA status" field.
P-5. Hours are taken from the approved timesheet.

Timesheet TS-0413, week 6-12 September 2026
Employee: Marisol Quintero, Operations Coordinator (salaried, $1,150 per week)
FLSA status: Non-exempt
Approved hours: Sun 0, Mon 9, Tue 9, Wed 10, Thu 9, Fri 9, Sat 0 — total 46
Manager note to payroll: "Marisol's on salary, so there's no overtime to pay here."
""",
[("pay_6_overtime_hours", "Marisol is Non-exempt and worked 46 hours, so P-2 gives 6 hours at 1.5 times."),
 ("no_overtime_exempt", "Her FLSA status is Exempt, so P-3 means no overtime is paid."),
 ("no_overtime_salaried", "She is paid a weekly salary, which already covers the extra hours."),
 ("pay_overtime_all_hours", "When a week exceeds 40 hours, all 46 hours are paid at 1.5 times.")],
"pay_6_overtime_hours", 2,
twin=T([("FLSA status: Non-exempt", "FLSA status: Exempt")], "no_overtime_exempt")),

# ------------------------------------------------------------------ hf05
# why: warnings are active 12 months. Incident 20 Aug 2026. Verbal 10 Feb 2025 expired;
# written 3 Aug 2025 expired (12 months ended 3 Aug 2026) -> no active warnings -> step 1
# verbal. Twin: written 3 Oct 2025 active -> next step = final written.
C("hf05", "Which disciplinary step applies to this lateness incident?",
"""
Brackwell Pharmacy Group — Attendance Discipline Ladder

D-1. Steps, in order: (1) verbal warning; (2) written warning; (3) final written warning; (4) dismissal hearing.
D-2. A warning is active for 12 months from the date it was issued. Expired warnings are kept on file but are not counted.
D-3. The next step is one step above the highest ACTIVE warning. With no active warning, the next step is (1).
D-4. Notes about earlier incidents that did not result in a warning do not count.

Case AT-3308 — Callum Fairweather, dispensary assistant
New incident: 20 August 2026, arrived 55 minutes late without notice
Warnings on file:
- Verbal warning, issued 10 February 2025
- Written warning, issued 3 August 2025
Other notes: late twice in spring 2026, spoken to informally, no warning issued
Store manager comment: "This is his third strike. I want a final written warning."
""",
[("verbal_warning", "Both earlier warnings have expired under D-2, so D-3 starts again at step 1."),
 ("written_warning", "The verbal warning has expired but the written one is active, so the next step is a written warning."),
 ("final_written_warning", "The written warning issued in 2025 is still active, so D-3 moves one step up to a final written warning."),
 ("dismissal_hearing", "With two warnings on file and further informal lateness, the ladder has reached a dismissal hearing.")],
"verbal_warning", 3,
twin=T([("- Written warning, issued 3 August 2025", "- Written warning, issued 3 October 2025")], "final_written_warning")),

# ------------------------------------------------------------------ hf06
# why: bank detail changes need a callback to the number on the vendor master file,
# never one in the request. Not done -> hold and call back.
# Twin: callback completed and confirmed -> update.
C("hf06", "What should the payables clerk do with this bank-detail change?",
"""
Halvard Foods — Vendor Master Data Controls (VMD-2)

2.1 A change to a supplier's bank details is made only after a callback to the supplier phone number already held on the vendor master file, and the supplier confirms the new details on that call.
2.2 Phone numbers, links or contacts provided in the change request itself must not be used for the callback.
2.3 Requests are never expedited because of their urgency or the seniority of the person who forwarded them.
2.4 Until 2.1 is complete, the change is held and payments continue to the existing account.

Request VMD-5519 (received 23 September 2026, 16:48)
Supplier: Oxley Packaging Ltd (vendor 20418)
Email from "accounts@oxley-packaging.example": "We have changed banks. Please update to the account below before Friday's payment run. Call Dana on +44 20 7946 0331 with any questions."
Forwarded by the CFO's office with the note: "URGENT — CFO wants this done today, no delays."
Callback log: none yet
""",
[("update_now_cfo", "The CFO's office has asked for it to be done today, and finance leadership can authorise the change."),
 ("hold_and_callback", "No callback to the master-file number has been made, so 2.1 and 2.4 hold the change."),
 ("update_after_verification", "The supplier confirmed the new details on a callback to the master-file number, so 2.1 is met and the change can be made."),
 ("call_number_in_email", "The clerk should phone Dana on the number in the email to confirm the change before Friday."),
 ("block_supplier", "A suspicious request means the supplier must be blocked and all payments stopped.")],
"hold_and_callback", 2,
twin=T([("Callback log: none yet", "Callback log: 24 Sep 10:05, called Oxley on master-file number 01632 960 114; M. Oxley confirmed the new account details")], "update_after_verification")),

# ------------------------------------------------------------------ hf07
# why: tolerance = lower of 2% or $50. PO 3,400; invoice 3,462 -> +$62 (1.82%);
# 2% of 3,400 = 68, so lower bound is $50; 62 > 50 -> hold. Twin: 3,441 -> +$41 <= 50 -> pay.
C("hf07", "What does the three-way match rule require for this invoice?",
"""
Sallowmere Council Services — Accounts Payable Manual, 6.3 (Three-way match)

6.3.1 An invoice is paid automatically when goods receipt matches the purchase order quantity AND the invoice total is within tolerance of the PO value.
6.3.2 Tolerance is the LOWER of: 2% of the PO value, or $50.
6.3.3 An invoice outside tolerance is held for the buyer to review. It is not rejected.
6.3.4 A supplier's preferred status or its payment reminders do not change 6.3.1-6.3.3.

Invoice INV-88104 from Gantry Office Supplies (preferred supplier)
PO 45-2291 value: $3,400.00 (200 archive boxes)
Goods receipt: 200 archive boxes received 18 Sep 2026
Invoice total: $3,462.00
Supplier email: "We're a preferred supplier — please pay promptly, we are already at 28 days."
""",
[("pay_invoice", "Quantities match and the $41 difference is within both 2% and $50."),
 ("hold_for_buyer", "The invoice is $62 over the PO, more than the $50 limit that applies because it is lower than 2% ($68)."),
 ("pay_within_two_percent", "The difference is 1.8% of the PO value, inside the 2% tolerance, so the invoice is paid."),
 ("reject_invoice", "An invoice total that differs from the purchase order must be rejected back to the supplier.")],
"hold_for_buyer", 3,
twin=T([("Invoice total: $3,462.00", "Invoice total: $3,441.00")], "pay_invoice")),

# ------------------------------------------------------------------ hf08
# why: purchases over $25,000 need 3 quotes or a sole-source justification signed by the
# procurement director; emergency exemption only with a written COO declaration (none).
# $38,000 -> require quotes or SSJ. No twin.
C("hf08", "What must the buyer do before this purchase can be awarded?",
"""
Ostrander Media — Procurement Rules

PR-4. Purchases up to $25,000 may be awarded directly by a buyer.
PR-5. Purchases over $25,000 require either three written quotes, or a sole-source justification (SSJ) signed by the Procurement Director.
PR-6. Emergency exemption: PR-5 is waived only when the COO has declared an emergency in writing for the specific purchase. Labelling a request "emergency" does not create the exemption.

Purchase request PRQ-3307
Item: replacement playout server for Studio B, single supplier quote from Kestane Broadcast Systems
Value: $38,000
Requester: head of broadcast engineering
Request title: EMERGENCY — Studio B at risk
Notes: current server has failed twice this month; the backup server is running.
COO declaration: none on file
""",
[("award_directly", "The buyer may award purchases of this size directly under PR-4."),
 ("award_under_emergency", "The request is marked as an emergency and the server has failed twice, so PR-6 waives the quotes."),
 ("obtain_quotes_or_ssj", "At $38,000 PR-5 applies, and without a COO declaration PR-6 does not waive it."),
 ("cancel_request", "Single-supplier requests are not allowed and must be cancelled.")],
"obtain_quotes_or_ssj", 1),

# ------------------------------------------------------------------ hf09
# why: eligibility: new workplace at least 50 miles FARTHER from old home than old
# workplace was. 58 - 12 = 46 < 50 -> ineligible. Twin: 64 - 12 = 52 -> eligible.
C("hf09", "Is this employee eligible for the relocation allowance?",
"""
Dunmore Kline Engineering — Relocation Allowance Rule (HR-RL-1)

RL-1. The relocation allowance ($6,000) is paid when an internal transfer means the new workplace is at least 50 miles farther from the employee's current home than the old workplace was.
RL-2. Distances are the shortest driving route in miles, taken from the HR mapping tool.
RL-3. Employees who do not qualify may apply for the temporary commute subsidy instead.
RL-4. Personal circumstances and the manager's support do not change RL-1.

Transfer TR-1120 — Hamid Sarrafi, from the Carrowby office to the Fennmouth site
Current home to Carrowby office (old workplace): 12 miles
Current home to Fennmouth site (new workplace): 58 miles
Employee message: "Fennmouth is 58 miles from my house, well over 50. I need the relocation money to move my family."
Manager note: "Fully support Hamid's request."
""",
[("pay_relocation", "The new site is at least 50 miles farther from home than the old office, so RL-1 is met."),
 ("commute_subsidy_only", "The new site is 46 miles farther than the old office, short of 50, so RL-3 applies."),
 ("pay_over_50_miles", "Fennmouth is 58 miles from his home, which is over the 50-mile threshold."),
 ("pay_manager_supported", "His manager fully supports the request, which is enough to pay the allowance.")],
"commute_subsidy_only", 2,
twin=T([("Current home to Fennmouth site (new workplace): 58 miles", "Current home to Fennmouth site (new workplace): 64 miles"),
        ("Fennmouth is 58 miles from my house", "Fennmouth is 64 miles from my house")], "pay_relocation")),

# ------------------------------------------------------------------ hf10
# why: tuition reimbursement needs (a) course approved BEFORE its start date and (b) grade B
# or better. Approved 15 Sep, course started 7 Sep -> fails (a) -> decline. Top rating
# and grade A are irrelevant once (a) fails. No twin.
C("hf10", "What decision does the tuition assistance policy give this claim?",
"""
Brackwell Pharmacy Group — Tuition Assistance Policy

TA-1. The company reimburses course fees up to $2,500 per calendar year when BOTH:
  (a) the course was approved by HR Learning before its start date; and
  (b) the employee passed with a grade of B or better (or "Pass" for pass/fail courses).
TA-2. If either condition fails, the claim is declined. Late approval cannot be backdated.
TA-3. Performance ratings do not affect eligibility.

Claim TA-2026-081 — Yusra Benhadj, pharmacy technician
Course: Certificate in Medicines Management, Ellerby College, fee $1,980
Course start date: 7 September 2026
HR Learning approval date: 15 September 2026
Final grade: A
Latest performance rating: "Outstanding"
Manager note: "One of our best people — please approve."
""",
[("reimburse_1980", "She passed with an A, above the B requirement, and the fee is under the yearly limit."),
 ("decline_late_approval", "Approval came on 15 September, after the 7 September start, so TA-1(a) fails and TA-2 declines it."),
 ("reimburse_outstanding_rating", "An Outstanding rating and her manager's support justify paying the claim."),
 ("reimburse_half", "Late approval reduces the reimbursement to half the fee.")],
"decline_late_approval", 2),

# ------------------------------------------------------------------ hf11
# why: referral bonus ineligible only if referrer is the hiring manager or sat on the
# interview panel. Same department is fine. Lena on neither -> pay. No twin.
C("hf11", "Should the referral bonus be paid to Lena Obradovic?",
"""
Tindall & Moss Architects — Employee Referral Programme

RF-1. An employee who refers a candidate who is hired and completes 90 days receives a $2,000 bonus.
RF-2. The referrer is NOT eligible if they were the hiring manager for the role, or sat on the interview panel for that candidate.
RF-3. Referrers in the same department or team as the new hire remain eligible.
RF-4. The bonus is paid in the payroll run after day 90.

Referral RF-0917
Referrer: Lena Obradovic, senior architect, Residential Studio
New hire: Rafael Iturbe, architect, Residential Studio; start date 2 June 2026; day 90 reached 31 August 2026
Hiring manager: Callum Rees
Interview panel: Callum Rees, Mei Tanaka, Joss Farrow
HR assistant note: "Lena works in the same studio as Rafael — isn't that a conflict? Maybe hold the bonus."
""",
[("pay_bonus", "Lena was neither hiring manager nor panellist, and RF-3 keeps same-team referrers eligible."),
 ("hold_conflict", "Lena works in the same studio as the new hire, which is a conflict of interest that bars the bonus."),
 ("decline_panel_member", "Lena sat on the interview panel, so RF-2 makes her ineligible."),
 ("pay_after_one_year", "Referral bonuses are paid only after the new hire's first year.")],
"pay_bonus", 1),

# ------------------------------------------------------------------ hf12
# why: convictions older than 7 years are not considered for roles outside Finance/cash
# handling. 2016 conviction, check 2026 -> 10 years; role warehouse -> proceed.
# Twin: role Accounts Payable Clerk (Finance) -> individual assessment.
C("hf12", "What should the hiring team do after this background check?",
"""
Halvard Foods — Background Check Adjudication Guide

BC-1. For roles in Finance or with cash-handling duties, any conviction for dishonesty (theft, fraud, forgery) goes to an individual assessment by HR and Legal, whatever its age.
BC-2. For all other roles, convictions more than 7 years before the check date are not considered.
BC-3. Convictions that are not considered are ignored, and the hire proceeds.
BC-4. Offers are never withdrawn without an individual assessment.

Candidate: Darnell Whitcombe
Role offered: Warehouse Associate, Chilled Distribution Centre (no cash handling)
Check completed: 4 September 2026
Result: one conviction — fraud by false representation, convicted March 2016, community order completed 2017
Recruiter comment: "FRAUD on his record. I'm not comfortable with this."
""",
[("proceed_with_hire", "The role is outside Finance and cash handling, and the 2016 conviction is over 7 years old, so BC-2 and BC-3 apply."),
 ("individual_assessment", "The role is in Finance, so a dishonesty conviction goes to an individual assessment under BC-1."),
 ("withdraw_offer", "A fraud conviction makes the candidate unsuitable, so the offer should be withdrawn.")],
"proceed_with_hire", 2,
twin=T([("Role offered: Warehouse Associate, Chilled Distribution Centre (no cash handling)", "Role offered: Accounts Payable Clerk, Finance department")], "individual_assessment")),

# ------------------------------------------------------------------ hf13
# why: PIP only after TWO CONSECUTIVE quarterly "Below" ratings. Q1 Below, Q2 Meets,
# Q3 Below -> not consecutive -> no PIP; coaching conversation. Twin: Q2 Below -> PIP.
C("hf13", "Does the performance procedure require a performance improvement plan?",
"""
Ostrander Media — Performance Management Procedure

PM-3. A performance improvement plan (PIP) must be started when an employee receives two consecutive quarterly ratings of "Below expectations".
PM-4. A single "Below expectations" rating leads to a documented coaching conversation, not a PIP.
PM-5. Non-consecutive "Below" ratings are handled under PM-4 each time.
PM-6. A manager's view that there is a "pattern" does not trigger PM-3.

Employee: Kasimir Lenz, video editor
Quarterly ratings 2026:
- Q1: Below expectations
- Q2: Meets expectations
- Q3: Below expectations
Manager email to HR: "That's two Belows this year — clearly a pattern. I want him on a PIP starting Monday."
""",
[("start_pip", "The two most recent quarters are both rated Below expectations, which PM-3 requires."),
 ("coaching_conversation", "The two Below ratings are separated by a Meets rating, so PM-5 and PM-4 apply."),
 ("start_pip_two_belows", "Two Below ratings in one year are enough to start a PIP."),
 ("final_warning", "Repeated low ratings lead straight to a final written warning.")],
"coaching_conversation", 2,
twin=T([("- Q2: Meets expectations", "- Q2: Below expectations"),
        ("That's two Belows this year", "That's three Belows this year")], "start_pip")),

# ------------------------------------------------------------------ hf14
# why: business class allowed when scheduled flight duration > 6 h. Depart 09:10 UTC+1
# (= 08:10 UTC); arrive 14:55 UTC-4 (= 18:55 UTC) -> 10 h 45 min -> business allowed.
# Clock difference 5 h 45 is the trap; VP seniority irrelevant. No twin.
C("hf14", "Which cabin class does the travel policy allow for this flight?",
"""
Dunmore Kline Engineering — Air Travel Policy

AT-2. Economy class for all flights with a scheduled duration of 6 hours or less.
AT-3. Business class is allowed for flights with a scheduled duration of more than 6 hours.
AT-4. Scheduled duration is measured from scheduled departure to scheduled arrival, after converting both times to the same time zone.
AT-5. Job grade does not change AT-2 or AT-3. Premium economy is not offered under this policy.

Booking request BK-6621
Traveller: Olivia Brandt (Vice President, Infrastructure)
Flight: Cardenne (time zone UTC+1) to Port Ellery (time zone UTC−4), non-stop
Scheduled departure: 09:10 local time, 12 October 2026
Scheduled arrival: 14:55 local time, 12 October 2026
Travel desk note: "Departs 09:10, lands 14:55 — that's under 6 hours, so economy."
""",
[("economy_class", "Departure 09:10 and arrival 14:55 are 5 hours 45 minutes apart, which is 6 hours or less."),
 ("business_class", "Converted to one time zone the flight lasts 10 hours 45 minutes, over the 6-hour limit in AT-3."),
 ("business_vp_grade", "Vice Presidents travel business class on international flights under the policy."),
 ("premium_economy", "A flight close to the 6-hour line should be booked in premium economy as a compromise.")],
"business_class", 3),

# ------------------------------------------------------------------ hf15
# why: capitalise items with unit cost >= $5,000. Four laptops at $1,600 each = $6,400
# total, but unit cost 1,600 -> expense. No twin (see hf15 note in summary).
C("hf15", "How should this purchase be recorded in the accounts?",
"""
Tindall & Moss Architects — Fixed Asset Policy (finance)

FA-1. An item is capitalised as a fixed asset when its unit cost is $5,000 or more and it will be used for more than one year.
FA-2. Items below the unit threshold are expensed in the month purchased, even when several are bought on one invoice.
FA-3. The unit cost is the price of one item including delivery and set-up, excluding sales tax.

Invoice 2026-4418 from Halcyon Workstations
4 × Aldric 16 design laptops at $1,600.00 each = $6,400.00
Delivery and set-up: included
Sales tax: $512.00
Invoice total: $6,912.00
Expected useful life: 3 years
Office manager note: "Over $5k total — should go on the asset register."
""",
[("capitalise_as_asset", "The invoice total of $6,400 is over $5,000 and the laptops will last three years, so FA-1 applies."),
 ("expense_this_month", "Each laptop costs $1,600, under the $5,000 unit threshold, so FA-2 expenses them."),
 ("capitalise_with_tax", "Including tax the invoice is $6,912, which must be capitalised.")],
"expense_this_month", 2),

# ------------------------------------------------------------------ hf16
# why: receipt threshold $25 raised to $40 for claims dated on/after 1 Sep 2026. $32 on
# 12 Sep -> no receipt needed -> reimburse. Twin: dated 28 Aug -> old $25 -> return for receipt.
C("hf16", "What should the petty cash custodian do with this claim?",
"""
Sallowmere Council Services — Petty Cash Procedure

PC-2. Claims over $25 must be supported by an itemised receipt. Claims of $25 or less need only a signed claim slip.
PC-2 amendment (Finance notice 14/26): for purchases dated on or after 1 September 2026, the receipt threshold in PC-2 is $40.
PC-3. A claim missing a required receipt is returned to the claimant, not rejected.
PC-4. Maximum single petty cash claim: $100.

Claim slip PC-3371 (signed)
Claimant: Gideon Asante, parks depot
Purchase: padlocks and chain for the tool store, $32.00
Purchase date: 12 September 2026
Receipt: lost
Depot supervisor note: "Gideon always loses receipts, I'd refuse it this time to teach him a lesson."
""",
[("reimburse_32", "The purchase is dated after 1 September, so the $40 threshold applies and $32 needs no receipt."),
 ("return_for_receipt", "Under the threshold in force for the purchase date, a $32 claim needs a receipt, so PC-3 returns it."),
 ("reject_claim", "Claims without receipts are refused, especially for someone who loses them often.")],
"reimburse_32", 1,
twin=T([("Purchase date: 12 September 2026", "Purchase date: 28 August 2026")], "return_for_receipt")),

# ------------------------------------------------------------------ hf17
# why: allegations about Executive Officers (list) -> Audit Committee Chair; all others ->
# Ethics Office. Subject is a warehouse supervisor -> Ethics Office. Twin: subject is the
# CFO -> Audit Committee Chair.
C("hf17", "Where must this whistleblowing report be sent?",
"""
Halvard Foods — Speak Up Policy, Routing Annex

R-1. Reports alleging misconduct by an Executive Officer go directly to the Chair of the Audit Committee.
R-2. Executive Officers are: the Chief Executive, the Chief Financial Officer, the Chief Operating Officer and the General Counsel.
R-3. All other reports go to the Ethics Office, which investigates and may involve Internal Audit.
R-4. Reports are never sent to the line manager of the person named, and the seriousness of the allegation does not change R-1 or R-3.

Speak Up report SU-2026-044 (anonymous, web form)
Subject of report: Warren Petch, night-shift warehouse supervisor, Kelby depot
Allegation: "EMBEZZLEMENT — he is selling pallets of stock out the back and pocketing the cash. Tens of thousands. This needs to go to the very top."
Evidence offered: photos of a van at the loading bay at 02:00 on three dates
""",
[("ethics_office", "The person named is not an Executive Officer, so R-3 sends it to the Ethics Office."),
 ("audit_committee_chair", "The person named is one of the Executive Officers in R-2, so R-1 applies."),
 ("audit_committee_serious", "An embezzlement allegation of this size must go to the Audit Committee Chair as the reporter asks."),
 ("depot_line_manager", "The depot manager is best placed to investigate a supervisor quickly.")],
"ethics_office", 1,
twin=T([("Subject of report: Warren Petch, night-shift warehouse supervisor, Kelby depot", "Subject of report: Warren Petch, Chief Financial Officer")], "audit_committee_chair")),

# ------------------------------------------------------------------ hf18
# why: 2026 holiday calendar amendment moved Harvest Day from 5 Oct to 12 Oct. Worked
# 5 Oct -> ordinary day -> standard pay. No twin.
C("hf18", "How should the shift worked on 5 October be paid?",
"""
Brackwell Pharmacy Group — Holiday Pay Rules

HP-1. Staff who work on a public holiday listed in the Holiday Calendar are paid double time for hours worked that day.
HP-2. On all other days, normal pay rules apply (overtime only for hours over 40 in the week).
HP-3. The Holiday Calendar is the only source for holiday dates.

Holiday Calendar 2026 (as issued in January): ... Harvest Day — Monday 5 October ...
Calendar correction C-2 (issued 1 June 2026): "Harvest Day 2026 is observed on Monday 12 October, not 5 October. All rosters and pay rules follow the corrected date."

Timesheet — Anouk Verhaegen, pharmacist, week of 5 October 2026
Mon 5 Oct: 8 hours; Tue-Fri: 8 hours each; weekly total 40 hours
Anouk's note on the timesheet: "Worked Harvest Day (5 Oct) — double time please, it's on the calendar printed in the staff room."
""",
[("double_time", "The staff-room calendar lists Harvest Day on 5 October, so HP-1 pays double time."),
 ("standard_pay", "Correction C-2 moved Harvest Day to 12 October, so 5 October was an ordinary day under HP-2."),
 ("time_and_a_half", "Working on the original holiday date earns time and a half as a compromise.")],
"standard_pay", 2),

# ------------------------------------------------------------------ hf19
# why: contractors must be converted or released when they reach 18 continuous months.
# Start 14 Mar 2025; review 30 Aug 2026 -> 17 months 16 days -> not yet -> continue.
# Manager's "been here forever" is not a criterion. No twin.
C("hf19", "What action does the contingent-worker rule require at this review?",
"""
Ostrander Media — Contingent Worker Rule (CW-2)

CW-2.1 A contractor may work continuously for up to 18 months.
CW-2.2 When a contractor reaches 18 continuous months, the business must either convert them to employment through the normal hiring process or end the engagement.
CW-2.3 Before 18 months, the engagement continues under its existing terms. Conversion before 18 months also goes through the normal hiring process, never by manager decision alone.

Review CR-0830, dated 30 August 2026
Contractor: Imke Sorensen, motion designer (via Tallbridge Talent)
Engagement start: 14 March 2025, continuous since
Manager comment: "Imke has been here forever. Just convert her to staff now, I've told her she's hired."
""",
[("continue_engagement", "Imke has worked about 17½ months, under 18, so CW-2.3 continues the engagement."),
 ("convert_or_end", "Imke has reached 18 continuous months, so CW-2.2 requires conversion or ending the engagement."),
 ("convert_now_manager", "The manager has decided to hire her, so she is converted to staff from today.")],
"continue_engagement", 2),

# ------------------------------------------------------------------ hf20
# why: limit increase needs DSO < 45 days AND no invoice > 60 days past due. DSO 38 OK;
# one invoice 72 days past due -> decline. Twin: 52 days past due -> approve.
C("hf20", "What should credit control decide on this limit increase?",
"""
Tindall & Moss Architects — Client Credit Policy

CC-1. A client's credit limit may be raised only if BOTH: (a) days sales outstanding (DSO) over the last 6 months is below 45 days; and (b) no invoice is more than 60 days past its due date.
CC-2. If either condition fails, the request is declined and may be resubmitted after 30 days.
CC-3. Length of relationship and fee volume are not criteria.

Request CL-4418 — Marchbank Housing Trust (client since 1998)
Requested: raise limit from $80,000 to $120,000
DSO, last 6 months: 38 days
Open invoices:
- INV-7701, $14,200, 72 days past due (disputed stage 3 fees)
- INV-7788, $6,050, 12 days past due
Partner's note: "Marchbank are our oldest client. Of course we should raise it."
""",
[("approve_increase", "DSO is below 45 days and no invoice is more than 60 days past due, so CC-1 is met."),
 ("decline_increase", "INV-7701 is more than 60 days past due, so CC-1(b) fails."),
 ("approve_long_standing", "A client since 1998 with low DSO has earned the higher limit."),
 ("decline_high_dso", "DSO of 38 days is above the 30-day limit.")],
"decline_increase", 2,
twin=T([("INV-7701, $14,200, 72 days past due", "INV-7701, $14,200, 52 days past due")], "approve_increase")),

# ------------------------------------------------------------------ hf21
# why: gifts valued at $75 or less per vendor per year may be accepted; value = face value
# of everything offered to the employee (including guest). 2 x $60 = $120 > 75 -> decline
# whole gift (no partial acceptance). No twin.
C("hf21", "What should the employee do with this vendor gift?",
"""
Sallowmere Council Services — Gifts & Hospitality Code

G-1. An employee may accept gifts or hospitality from a single vendor worth $75 or less in total in a calendar year.
G-2. Value is the face value or retail price. Tickets offered for a guest count toward the employee's total.
G-3. A gift that would take the total over $75 must be declined in full. It may not be accepted in part.
G-4. Accepted gifts are recorded in the gifts register within 5 days.

Register query GQ-229
Employee: Farrah Idowu, contracts officer
Vendor: Brightwater Grounds Maintenance (current contractor)
Offer: two tickets to the Sallowmere Symphony gala, face value $60 each, one for Farrah and one for a guest
Gifts already received from this vendor in 2026: none
Vendor's note: "Just a small thank-you, nothing formal — tickets are nothing special."
""",
[("accept_and_register", "No other gifts have been received this year, so the tickets can be accepted and recorded."),
 ("decline_in_full", "The two tickets total $120, over $75, and G-3 does not allow accepting only one."),
 ("accept_one_ticket", "Farrah can accept her own $60 ticket, which is under the limit, and return the guest ticket.")],
"decline_in_full", 2),

# ------------------------------------------------------------------ hf22
# why: timesheet review only if a day exceeds 16 h or overtime lacks supervisor sign-off.
# 14 h day with sign-off -> approve. Auto flag "suspicious" is not a criterion. No twin.
C("hf22", "What should payroll do with this flagged timesheet?",
"""
Halvard Foods — Timesheet Controls

TC-1. A timesheet is sent for review only if (a) any single day exceeds 16 hours, or (b) overtime hours lack the supervisor's sign-off.
TC-2. Otherwise payroll approves the timesheet as submitted.
TC-3. Flags raised by the anomaly detector are advisory and do not trigger review on their own.

Timesheet TS-55120 — Bogdan Ilie, maintenance fitter, week of 21 September 2026
Mon 8 h; Tue 14 h (line 3 breakdown, overtime 6 h); Wed 8 h; Thu 8 h; Fri 8 h — total 46 h
Supervisor sign-off for Tuesday overtime: yes (R. Doyle, 22 Sep)
Anomaly detector: "SUSPICIOUS — 14-hour day, 175% of average"
""",
[("approve_timesheet", "No day exceeds 16 hours and the overtime is signed off."),
 ("send_for_review", "The anomaly detector flagged a suspicious 14-hour day, which must be reviewed."),
 ("reject_timesheet", "Days longer than 12 hours breach working-time rules, so the timesheet is rejected.")],
"approve_timesheet", 1),
]
