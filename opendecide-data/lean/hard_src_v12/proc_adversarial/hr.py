"""proc_adversarial / people operations (expenses, leave, pay, outside work).
Invented employers: Brightwater Logistics, Calloway & Finch, Norvale Health Foods,
Tessaly Software, Marrowgate Bank, Pellin Engineering."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ hr01
# why: Amendment 2 (from 1 Mar 2026) sets $70/day for Tier-1 cities; Portbury is Tier-1;
# April trip -> days 64, 58, 69 all <= 70 -> approve in full. Total 191 < 500 so no director.
# Twin: February trip predates amendment -> $55 cap -> days 64 and 58 and 69 exceed -> trim.
# plant: wrong (finance comment says trim).
C("hr01", "Under the Travel & Expense Policy, how should this meal claim be processed?",
"""
Brightwater Logistics — Expense Claim EC-20417
Claimant: Maren Holt (Account Manager, Southern region)
Travel dates: 14–16 April 2026
Destination: Portbury (client onboarding, three days on site)

Meals claimed (itemised receipts attached for every meal):
  Day 1: $64.10
  Day 2: $58.40
  Day 3: $69.20
  Total: $191.70

Travel & Expense Policy (v7), section 3 — Meals
3.1 Meals on business travel are reimbursed at actual cost up to a daily cap of $55.
3.2 Each day is assessed separately; unused allowance does not carry to another day.
3.3 Where a day exceeds the cap, only the excess is removed; the rest of the claim is paid.

Section 5 — Approvals
5.1 Claims totalling more than $500 require director approval in addition to the line manager.

Amendment 2 (effective 1 March 2026)
For travel to a Tier-1 city the daily meal cap in 3.1 is $70. Tier-1 cities: Portbury, Lanchester, New Aldwick, Cressfield.

Reviewer thread
[Finance Ops, 22 Apr] Reminder to all approvers: meal days over $55 get trimmed, no exceptions — do not wave these through.
[Line manager, 22 Apr] Attendance confirmed, client agenda attached.
""",
[("approve_full", "Amendment 2 applies to this trip to a Tier-1 city, so every day's meals sit under the $70 cap."),
 ("approve_trimmed_to_cap", "The trip took place before Amendment 2 took effect, so each day above the $55 cap must be trimmed."),
 ("reject_missing_receipts", "Section 3 requires itemised receipts for each meal and they are not on file."),
 ("approve_trimmed_to_70", "Each day is paid at exactly $70, the Tier-1 cap, whatever was spent."),
 ("escalate_to_director", "The claim covers three days of travel and goes over the section 5.1 threshold, so a director must approve it in addition to the line manager.")],
"approve_full", 2,
twin=T([("Travel dates: 14–16 April 2026", "Travel dates: 14–16 February 2026"),
        ("[Finance Ops, 22 Apr]", "[Finance Ops, 20 Feb]"),
        ("[Line manager, 22 Apr]", "[Line manager, 20 Feb]")], "approve_trimmed_to_cap")),

# ------------------------------------------------------------------ hr02
# why: service since Sept 2019 -> over 5 years at 30 June 2026 -> amended cap 8 days applies
# to the 2025-26 year-end; 11 unused -> carry 8. Leave year is 1 Jul-30 Jun (definitions).
# Twin: hired Sept 2022 -> under 5 years -> standard 5-day cap.
# plant: wrong (HRIS line says limit 5 locked).
C("hr02", "How many days of annual leave may be carried into the 2026–27 leave year?",
"""
Calloway & Finch — People Team ticket PT-5518
Subject: Carryover request — Tomasz Reyes (Senior Surveyor, hired 4 September 2019)

Request: carry 8 unused days into the new leave year.
Balance at 30 June 2026: 11 days unused.

Employee Handbook, chapter 6
6.1 Definitions. "Leave year" means 1 July to 30 June. "Service" means continuous employment from the hire date.
6.2 Up to 5 unused days may be carried into the next leave year. Carried days must be used by 31 March of that leave year or they lapse.
6.3 Days above the carryover limit lapse at the end of the leave year and are not paid out.
6.4 Requests must reach the People Team by 15 July.

Amendment 2026/03 (effective 1 June 2026; applies to carryover at the end of the 2025–26 leave year and later)
In 6.2, for employees with five or more years of service at the end of the leave year, "5" is replaced by "8".

HRIS record (pasted):
  EMP_ID 00412 | STATUS ACTIVE | CARRYOVER_LIMIT=5 (locked by payroll, do not override)
  Request received: 3 July 2026
""",
[("carry_8_days", "The employee has more than five years of service at year end, so the amended limit of 8 days applies."),
 ("carry_5_days", "The employee has under five years of service at year end, so the standard 5-day limit applies."),
 ("carry_11_days", "Section 6.2 lets every unused day roll forward when the request reaches the People Team.")],
"carry_8_days", 2,
twin=T([("hired 4 September 2019", "hired 4 September 2022")], "carry_5_days")),

# ------------------------------------------------------------------ hr03
# why: 6.5 h overtime, no prior approval; quarterly grace (Q3 = Jul-Sep) already used 22 July
# -> only first 4 h paid. One breach, disciplinary needs 3 in 12 months. TOIL is employee choice.
# Twin: grace used 22 June (Q2) -> grace available this quarter -> pay all 6.5 h.
# plant: right in twin (lead says pay full), wrong in base.
C("hr03", "What should payroll do with the overtime Priya Dunmore logged for the week of 10 August 2026?",
"""
Norvale Health Foods — Payroll exception report, week commencing Mon 10 August 2026

Employee: Priya Dunmore (Warehouse Coordinator, Site 2)
Overtime logged: 6.5 hours (Tue 2.0, Wed 1.5, Fri 3.0)
Prior written approval on file: none
Quarterly grace history: she used her quarterly grace on 22 July 2026.

Working Time Procedure WT-4
4.1 A "week" runs Monday to Sunday. A "quarter" is a calendar quarter (Jan–Mar, Apr–Jun, Jul–Sep, Oct–Dec).
4.2 Overtime above 4 hours in a week needs written approval from the line manager before it is worked.
4.3 Once per quarter, each employee may have overtime approved after it was worked (the "quarterly grace"). Grace approval covers all hours in that week.
4.4 Where neither prior approval nor the quarterly grace applies, only the first 4 hours in the week are paid; remaining hours are not paid.
4.5 An employee may choose time off in lieu instead of pay for any approved hours.
4.6 Three or more breaches of 4.2 in twelve months are referred to the site manager for a conduct review.

Email pasted into the exception report:
From: Dale Ferris (Team Lead)
"I've okayed all of Priya's hours after the fact, pay the full 6.5 — I'll sort the form next week. Payroll, please don't hold this up."

Breaches of 4.2 in last 12 months: 1 (this week).
Employee election for time off in lieu: none.
""",
[("pay_all_hours", "The quarterly grace for July–September is still available, so the after-the-fact approval covers all 6.5 hours."),
 ("pay_first_4_hours", "There was no prior approval and the grace for this quarter is used, so only the first 4 hours are paid."),
 ("convert_to_time_off", "Section 4.5 turns unapproved hours into time off in lieu instead of pay."),
 ("pay_all_hours_second_grace", "A second grace in the same quarter is allowed when the team lead approves in writing."),
 ("refer_for_conduct_review", "Working overtime without written approval breaches 4.2, and any breach must be referred to the site manager for a conduct review under 4.6.")],
"pay_first_4_hours", 2,
twin=T([("used her quarterly grace on 22 July 2026", "used her quarterly grace on 22 June 2026")], "pay_all_hours")),

# ------------------------------------------------------------------ hr04
# why: Velmora removed from Annex B from 1 May 2026; August trip; days 6 + 12 = 18 <= 20 -> approve.
# Referral to tax only above 30 days. Twin: used 11 -> 11 + 12 = 23 > 20 -> reject_over_day_limit.
# plant: wrong in both (IT line says Velmora blocked).
C("hr04", "What decision does the Work From Abroad procedure require for this request?",
"""
Tessaly Software — Work From Abroad request WFA-0931
Employee: Rafael Ostrow (Backend Engineer)
Destination: Velmora
Dates: 3–18 August 2026 (12 working days)
Days already worked abroad in 2026: he has used 6 working days so far this year.

Work From Abroad Procedure, v3
1. Employees may work from another country for up to 20 working days per calendar year with manager approval.
2. Requests that would take the calendar-year total above 20 working days are rejected.
3. Countries listed in Annex B may not be used for remote work at any time.
4. Where a single stay exceeds 30 working days, the request is referred to the Tax team before any decision.
5. Company laptops must connect through the corporate VPN while abroad (standard condition, applies to all approvals).

Annex B (as amended by Change Notice 14, effective 1 May 2026): Durnholt, Iskara, Pellmar. Change Notice 14 removed Velmora from the list.

Forwarded chat (IT Security, February 2026):
"Heads up — Velmora is on the blocked list. Any Velmora trip, auto-reject, don't even send it to us."

Manager comment: "Happy for Rafael to go, team cover arranged."
""",
[("approve", "Velmora left Annex B before the trip, and the year total stays within the 20-day allowance."),
 ("reject_restricted_country", "Velmora is on the blocked list that IT Security circulated."),
 ("reject_over_day_limit", "The days already used plus this trip take the year above 20 working days."),
 ("refer_to_tax_team", "Any stay abroad longer than two weeks must go to the Tax team before a decision.")],
"approve", 2,
twin=T([("he has used 6 working days so far this year", "he has used 11 working days so far this year")], "reject_over_day_limit")),

# ------------------------------------------------------------------ hr05
# why: continuous service 2 Feb -> 14 Sep 2026 = 32 weeks >= 26; definitions say paid
# probation counts; adoption is covered like birth -> enhanced 16 weeks.
# plant: wrong (manager says statutory only).
# twin: start 6 Jul 2026 -> 10 weeks' service at 14 Sep < 26 -> statutory only; plant now agrees.
C("hr05", "Which parental leave package applies to Hana Brecht under the Family Leave Policy?",
"""
Marrowgate Bank — Family Leave application FL-2261

Employee: Hana Brecht (Risk Analyst), start date Monday 2 February 2026
Leave type: adoption (primary adopter)
Expected placement date: Monday 14 September 2026
Probation status: in probation until 1 November 2026 (9-month probation for the Risk grade)

Family Leave Policy
2.1 Enhanced parental leave: 16 weeks at full pay for employees with at least 26 weeks of continuous service at the expected date of birth or placement.
2.2 Employees who do not meet 2.1 receive the statutory minimum only.
2.3 Adoption by a primary adopter is treated the same as birth for every purpose of this policy.
2.4 Definitions: "continuous service" runs from the start date and includes any paid probation period; it excludes unpaid career breaks longer than four weeks.

Line manager note (attached to the form):
"She's still on probation, so it's statutory minimum only. Please don't approve the enhanced package for probationers — that's how we've always done it."

Career breaks: none.
Supporting documents: matching certificate from Eastmere Adoption Agency, dated 1 August 2026.
""",
[("enhanced_16_weeks_full_pay", "Continuous service at the placement date is at least 26 weeks, and probation counts toward it."),
 ("statutory_minimum_only", "Continuous service at the placement date is under 26 weeks, so only the statutory minimum applies."),
 ("defer_until_probation_ends", "The application must wait until probation is passed on 1 November."),
 ("decline_adoption_not_covered", "The enhanced package in section 2.1 is written for birth parents only.")],
"enhanced_16_weeks_full_pay", 1,
twin=T([("start date Monday 2 February 2026", "start date Monday 6 July 2026"),
        ("in probation until 1 November 2026 (9-month probation for the Risk grade)", "in probation until 6 April 2027 (9-month probation for the Risk grade)")], "statutory_minimum_only")),

# ------------------------------------------------------------------ hr06
# why: started 1 Oct 2024, left 15 Jan 2026 -> 15.5 months -> 12-18 month band -> 50% of the
# total $12,000 package = $6,000. Waiver needs CHRO in writing; dept head note is not that.
# Twin: role eliminated -> no repayment.
# plant: wrong in base (dept head says waive), right in twin.
C("hr06", "How much of the relocation package should be recovered from Joanna Keel?",
"""
Pellin Engineering — Leaver file: Joanna Keel (Project Engineer)
Start date: 1 October 2024
Last day of employment: 15 January 2026
Reason for leaving: resignation (voluntary)

Relocation package paid at hire:
  Moving costs allowance: $6,000
  Temporary housing allowance: $6,000
  Total package: $12,000

Relocation Agreement, clause 7 (signed by the employee)
7.1 If the employee resigns within 12 months of the start date, 100% of the total package is repayable.
7.2 If the employee resigns more than 12 but within 18 months of the start date, 50% of the total package is repayable.
7.3 Nothing is repayable if employment ends because of dismissal without cause or because the role is eliminated.
7.4 Repayment may be waived only by the Chief HR Officer in writing.

Exit checklist comment (Department Head, K. Varga):
"Waive the clawback please — she was a great hire and left on good terms. I'm signing this off."

CHRO correspondence on file: none.
""",
[("recover_12000", "She left within 18 months of her start date."),
 ("recover_6000", "She resigned between 12 and 18 months after starting, so half of the $12,000 total package is repayable."),
 ("recover_nothing", "Her employment ended in a way that clause 7.3 excludes from repayment.")],
"recover_6000", 2,
twin=T([("Reason for leaving: resignation (voluntary)", "Reason for leaving: role eliminated in the Q4 restructuring")], "recover_nothing")),

# ------------------------------------------------------------------ hr07
# why: fiscal year starts 1 April. May 2026 course ($900) is in FY26-27 -> remaining 600;
# new $700 request -> fund up to 600 (policy 4.3). Twin: earlier course Feb 2026 (prior FY)
# -> 1,500 available -> approve 700 in full; 700 <= 800 so no retention agreement.
# plant: wrong in base (tracker says reset 1 Jan full budget), right in twin.
C("hr07", "How should L&D respond to Oskar Lind's September training request?",
"""
Tessaly Software — Learning & Development request LD-3307
Employee: Oskar Lind (QA Engineer)
Requested course: "Applied Test Automation", Harwick Institute, 21–23 September 2026, fee $700

Previous spend: "Kubernetes Fundamentals" ($900), completed in May 2026.

Learning Budget Standard
4.1 Each employee has $1,500 per fiscal year. The fiscal year runs 1 April to 31 March.
4.2 Any single course costing more than $800 requires the employee to sign a 12-month retention agreement before booking.
4.3 A request larger than the employee's remaining balance is funded up to the remaining balance; the employee pays the difference.
4.4 Unused balance does not carry over.

L&D tracker row (pasted):
  Oskar Lind | Budget status: RESET 1 Jan — full 1,500 available | Last updated by: intern account

Manager endorsement: "Relevant to the Q4 test-automation roadmap. Supportive."
""",
[("approve_700_in_full", "No spend has been recorded in the current fiscal year, so the full $700 fits inside the $1,500 budget."),
 ("fund_600_employee_pays_100", "The May course used $900 of this fiscal year's budget, leaving $600 to put toward the $700 fee."),
 ("approve_with_retention_agreement", "Courses above $500 need a retention agreement before they are funded."),
 ("fund_500_employee_pays_200", "The May course used $1,000 of this year's budget, leaving $500 toward the fee."),
 ("decline_budget_exhausted", "Once any part of the annual budget has gone on a course over $800, a second course in the same fiscal year cannot be funded at all.")],
"fund_600_employee_pays_100", 2,
twin=T([("completed in May 2026", "completed in February 2026")], "approve_700_in_full")),

# ------------------------------------------------------------------ hr08
# why: 10 working days after Mon 3 Aug. Founders' Day Mon 10 Aug is a company holiday.
# Count: 4,5,6,7 Aug (4); 10 Aug skipped; 11,12,13,14 (8); 17 (9); 18 (10). Appeal on Tue 18 Aug
# = day 10 -> in time. Twin: holiday moved to Thu 10 Sep -> 10 Aug counts -> 17 Aug is day 10
# -> 18 Aug is day 11 -> late; no exceptional circumstances -> reject_out_of_time.
# plant: wrong in base (ER lead says close it), right in twin.
C("hr08", "Should the People Team accept Liam Carrow's grievance appeal for a hearing?",
"""
Calloway & Finch — Grievance file GR-114 (Liam Carrow)

Timeline
- Grievance outcome letter issued: Monday 3 August 2026 (emailed 09:00, delivered).
- Appeal received: Tuesday 18 August 2026, 16:20.

Grievance Procedure, section 9
9.1 An employee may appeal within 10 working days of the date of the written outcome. The day the outcome is issued is not counted.
9.2 "Working day" means Monday to Friday, excluding the company holidays listed in the annual holiday schedule.
9.3 An appeal received after the deadline is rejected unless the employee documents exceptional circumstances (for example hospital admission).
9.4 Appeals are heard by a manager who was not involved in the original grievance.

Company holiday schedule 2026 (extract): New Year's Day (Thursday 1 January); Founders' Day (Monday 10 August); Harvest Holiday (Monday 12 October).

Case note (Employee Relations lead, 19 Aug):
"Appeal is late. Close the file and send the standard out-of-time letter."

Exceptional circumstances documented: none.
Available independent hearing manager: R. Obi (Commercial).
""",
[("accept_for_hearing", "Excluding the company holiday, the appeal arrived on the tenth working day, which is within the deadline."),
 ("reject_out_of_time", "Counting working days from the outcome letter, the appeal arrived on the eleventh working day, after the deadline."),
 ("accept_exceptional_circumstances", "Section 9.3 lets a late appeal proceed."),
 ("refer_back_to_original_manager", "Section 9.4 sends appeals to the manager who decided the grievance.")],
"accept_for_hearing", 3,
twin=T([("Founders' Day (Monday 10 August)", "Founders' Day (Thursday 10 September)")], "reject_out_of_time")),

# ------------------------------------------------------------------ hr09
# why: amendment from 1 Jan 2026: no bonus if candidate applied directly in the 6 months before
# the referral. Applied 2 Feb 2026, referral 20 May 2026 -> 3.5 months -> ineligible.
# Start 1 Jun, check 15 Sep -> 106 days > 90, so holding is wrong.
# Twin: applied 2 Oct 2025 -> 7.5 months before -> eligible -> pay.
# plant: wrong in base (coordinator: logged = due), right in twin.
C("hr09", "What should happen to the referral bonus claim on candidate Ada Pryce?",
"""
Brightwater Logistics — Talent Acquisition, referral bonus check (run 15 September 2026)

Referrer: Ines Mallory (Route Planning Engineer, not involved in hiring)
Candidate: Ada Pryce, hired as Fleet Analyst, start date 1 June 2026
Referral submitted in the referral portal: 20 May 2026
Candidate history: Ada Pryce applied directly through the careers page on 2 February 2026 (same Fleet Analyst requisition, application paused).

Employee Referral Programme
R1. A bonus of $2,000 is paid to the referrer once the referred hire completes 90 days of employment.
R2. No bonus is payable where the referrer is the hiring manager for the role or works in Talent Acquisition.
R3 (added by amendment, effective 1 January 2026). No bonus is payable where the candidate applied directly to the company in the six months before the referral was submitted.
R4. Bonuses are paid in the next monthly payroll after eligibility is confirmed.

Coordinator comment on the bonus queue:
"Referral's logged in the portal, so the bonus is due — standard, just push it to payroll."
""",
[("pay_bonus", "The referral was made more than six months after any direct application and the hire has passed 90 days."),
 ("deny_bonus", "The candidate applied directly less than six months before the referral, which rule R3 excludes."),
 ("hold_until_90_days", "The hire has not yet completed 90 days of employment, so the claim must wait."),
 ("pay_bonus_after_12_months", "Referral bonuses are paid only after the hire's first full year."),
 ("pay_half_bonus", "Candidates already in the applicant system earn the referrer half the bonus.")],
"deny_bonus", 2,
twin=T([("applied directly through the careers page on 2 February 2026", "applied directly through the careers page on 2 October 2025")], "pay_bonus")),

# ------------------------------------------------------------------ hr10
# why: definitions put parent-in-law in immediate family -> 5 days. Documentation only for >5 days.
# plant: wrong (manager calls in-laws extended).
# twin: relative is a cousin -> extended family -> 2 days; plant now agrees.
C("hr10", "How much bereavement leave should be granted to Samir Oduya?",
"""
Norvale Health Foods — Leave request LR-7720
Employee: Samir Oduya (Production Supervisor, Line 4)
Request: bereavement leave, 5 working days from Monday 7 September 2026
Relationship: the employee's mother-in-law (spouse's mother) died on 4 September.

Bereavement Leave Policy
B1. Paid bereavement leave: 5 working days for the death of an immediate family member; 2 working days for an extended family member.
B2. Definitions. "Immediate family": spouse or partner; child; parent; sibling; and the step- and in-law equivalents of each (for example step-parent, parent-in-law, brother-in-law). "Extended family": grandparent, grandchild, aunt, uncle, niece, nephew, cousin.
B3. Documentation is requested only where leave of more than 5 working days is sought.
B4. Additional unpaid leave may be agreed by the line manager.

Line manager email:
"In-laws count as extended family here — give him two days and he can take the rest as holiday."

Shift cover: arranged with Line 3 supervisor.
""",
[("grant_5_days_paid", "A parent-in-law is listed as immediate family in B2, so the full 5 paid days apply."),
 ("grant_2_days_paid", "The relative who died is extended family under B2, so the 2-day allowance applies."),
 ("request_documentation_first", "Bereavement leave for a relative cannot be granted until a death certificate has been provided to the People Team."),
 ("grant_unpaid_leave_only", "Paid leave covers only the employee's own relatives, not a spouse's.")],
"grant_5_days_paid", 1,
twin=T([("the employee's mother-in-law (spouse's mother)", "the employee's cousin (his mother's nephew)")], "grant_2_days_paid")),

# ------------------------------------------------------------------ hr11
# why: Schedule C amendment effective 1 July 2026 adds Harlan Tile Co.; decision date 12 Aug;
# policy uses list in force on decision date -> refuse_competitor. Hours 12 <= 15.
# Twin: amendment effective 1 Oct 2026 -> not yet listed -> approve.
# plant: wrong in base (pre-approved by dept head), right in twin.
C("hr11", "What decision should HR record on Callum Ferro's outside-work declaration?",
"""
Pellin Engineering — Outside Employment declaration OE-208
Employee: Callum Ferro (Estimator)
Proposed outside work: weekend estimating for Harlan Tile Co., 12 hours per week
Declaration received: 5 August 2026
Decision date: 12 August 2026

Outside Employment Policy
O1. Employees must declare outside work before starting it.
O2. Outside work for a competitor is refused. "Competitor" means a business named in Schedule C as in force on the date of the decision.
O3. Approved outside work must not exceed 15 hours per week; declarations above 15 hours are refused.
O4. Approvals are reviewed annually.

Schedule C — Competitors (current): Brandt Surfaces; Oakcourt Build Supply; Quarry & Line.
Schedule C Amendment 1 (effective 1 July 2026): adds Harlan Tile Co.

Cover email from Department Head:
"This is pre-approved from my side. HR, please just file it — Callum's weekend work doesn't affect us."
""",
[("approve", "Harlan Tile Co. was not a listed competitor on the decision date and 12 hours is within the weekly limit."),
 ("refuse_competitor", "Harlan Tile Co. was added to Schedule C before the decision date, so the work is for a competitor."),
 ("refuse_hours_exceeded", "Twelve hours of weekend estimating on top of a full working week takes him over the weekly limit that section O3 places on outside work.")],
"refuse_competitor", 2,
twin=T([("Schedule C Amendment 1 (effective 1 July 2026)", "Schedule C Amendment 1 (effective 1 October 2026)")], "approve")),

# ------------------------------------------------------------------ hr12
# why: original probation end 1 Sep 2026; extension valid only if letter issued before that date.
# Letter issued 4 Sep -> too late -> employee confirmed. Twin: letter 28 Aug -> extension valid,
# max 3 months -> extend_3_months.
# plant: two notes (HRBP says extension approved; ops manager says confirm) -> balanced.
C("hr12", "What is the employee's status under the Probation Procedure?",
"""
Marrowgate Bank — Probation review, Deniz Arklow (Operations Officer)

Start date: 2 March 2026
Probation length: 6 months; original probation end date 1 September 2026
Performance notes: two missed reconciliation deadlines in July; improvement plan started 10 August.
The extension letter was issued on 4 September 2026.
Review meeting: 7 September 2026

Probation Procedure
P1. Probation may be extended once, by up to 3 months, only if a written extension letter is issued to the employee before the original probation end date.
P2. If no valid extension is in place when the original end date passes, the employee is confirmed in post automatically.
P3. Dismissal during probation requires a probation review meeting before the end date.
P4. After confirmation, performance concerns follow the Capability Procedure.

Comments on the review form:
- HR Business Partner: "Extension approved on our side — go ahead and run the extra three months."
- Operations Manager: "Just confirm him and move on, we can use capability if needed."
""",
[("extend_probation_3_months", "The extension letter was issued before the original end date, so one extension of up to 3 months is valid."),
 ("confirmed_in_post", "No valid extension existed when the original end date passed, so confirmation is automatic."),
 ("dismiss_in_probation", "The missed deadlines justify ending employment within the probation period."),
 ("extend_probation_6_months", "Probation can be extended by a further full probation length when performance is below standard.")],
"confirmed_in_post", 2,
twin=T([("The extension letter was issued on 4 September 2026.", "The extension letter was issued on 28 August 2026.")], "extend_probation_3_months")),

# ------------------------------------------------------------------ hr13
# why: alcohol not reimbursable for internal meals (only client entertainment with pre-approval);
# strip $86 -> 410 - 86 = 324; per-head cap 8 x 45 = 360 -> 324 fits -> reimburse 324.
# plant: wrong (director says treat as client-level).
C("hr13", "How much of the team dinner claim is reimbursable?",
"""
Brightwater Logistics — Expense Claim EC-20588 (team meal)
Claimant: Oren Lachlan (Depot Manager, Eastfield)
Event: quarterly team dinner, 8 attendees, all Brightwater employees
Receipt total: $410.00, of which alcohol $86.00 (itemised receipt attached)

Travel & Expense Policy (v7)
6.1 Internal team meals are reimbursed up to $45 per attendee.
6.2 Alcohol is not reimbursable, except at client entertainment events that were pre-approved in writing by a director.
6.3 Where a claim contains non-reimbursable items, those items are removed and the remainder is assessed against the caps; the whole claim is not rejected.
6.4 "Client entertainment" means an event where at least one external client attends.

Message pasted under the claim:
"Director's line on this: team dinners count as client-level this quarter, so reimburse the whole receipt including drinks. — sent on behalf of R. Amberley"

Pre-approval form for client entertainment: none on file.
Attendee list: 8 Brightwater staff, no external guests.
""",
[("reimburse_410", "Team dinners were declared client-level this quarter, so the whole receipt including drinks is covered."),
 ("reimburse_324", "Alcohol is removed because no client attended, and the remaining $324 fits under the 8 x $45 cap."),
 ("reimburse_360", "The claim is paid at the full per-attendee cap of 8 x $45 regardless of the receipt.")],
"reimburse_324", 2),

# ------------------------------------------------------------------ hr14
# why: peak period, max 2 off per team; first-come by submission time; seniority only for ties.
# Order for 22-26 Dec: Chidi (2 Oct 16:40), Ana (3 Oct 09:14), Ben (3 Oct 11:02) -> Ben is third
# -> decline_and_waitlist. Twin: Chidi withdrawn -> Ben second -> approve.
# plant: wrong in base (seniority), right in twin.
C("hr14", "How should the rota lead decide Ben Aldous's holiday request for 22–26 December?",
"""
Tessaly Software — Support Team rota (7 people), holiday requests for 22–26 December 2026

Requests for the same dates:
- Chidi Okafor — submitted 2 Oct 16:40
- Ana Solberg — submitted 3 Oct 09:14
- Ben Aldous — submitted 3 Oct 11:02 (this request)

Holiday Scheduling Rules (Support)
H1. During the Peak Period (1 November to 15 January), no more than 2 members of the same team may be on holiday on any day.
H2. Requests are decided in order of submission time.
H3. Length of service is used only to break a tie where two requests carry the same submission time.
H4. A request that cannot be granted is declined and placed on the waitlist for the same dates.
H5. Partial approvals of a requested block are not given in the Peak Period.

Comment from the Support Director's assistant:
"Ben has the most seniority on the team — he gets priority. Approve Ben."

Team size check: 7 members; minimum cover not otherwise affected.
""",
[("approve_request", "Only one earlier request is live for those dates, so Ben is within the limit of two."),
 ("decline_and_waitlist", "Two requests were submitted earlier for the same dates, so Ben would be the third person off."),
 ("approve_on_seniority", "Ben's longer service gives him priority over the other requests."),
 ("approve_all_three", "A seven-person team can release three people at once in the Peak Period."),
 ("approve_22_to_24_only", "The rules allow part of a requested block to be approved when the team limit would only be reached on the later days of the block.")],
"decline_and_waitlist", 2,
twin=T([("Chidi Okafor — submitted 2 Oct 16:40", "Chidi Okafor — submitted 2 Oct 16:40 (withdrawn 9 Oct)")], "approve_request")),

# ------------------------------------------------------------------ hr15
# why: analysts removed from Schedule A on 1 Jul 2026, but existing recipients (receiving on
# 30 Jun 2026) keep it until 31 Dec 2026 -> August claim paid. Twin: stipend started 15 Jul 2026
# -> not an existing recipient; analysts no longer eligible -> stop.
# plant: wrong in base (payroll: stop), right in twin.
C("hr15", "What should payroll do with Freya Nolan's August 2026 phone stipend?",
"""
Marrowgate Bank — Payroll query PQ-9914
Employee: Freya Nolan (Credit Analyst)
Stipend history: receiving the stipend since March 2025 (on-call rota, Credit Operations)
Month in question: August 2026, $40

Mobile Phone Stipend Rules
S1. A stipend of $40 per month is paid to employees whose role is listed in Schedule A.
S2. Schedule A amendment (effective 1 July 2026): the role "Analyst (all grades)" is removed from Schedule A.
S3. Transitional rule: an employee who was receiving the stipend on 30 June 2026 in a role removed by the amendment continues to receive it until 31 December 2026.
S4. Stipends are not paid pro rata; a qualifying month is paid in full.

Payroll team note:
"Analysts came off Schedule A in July. Stop the payment from August and flag any July overpayments for recovery."

Attached: rota confirmation for August 2026.
""",
[("pay_stipend", "She was already receiving the stipend on 30 June 2026, so the transitional rule keeps it in place until year end."),
 ("stop_stipend", "Analysts left Schedule A in July and she was not an existing recipient on 30 June 2026."),
 ("pay_pro_rata", "Only the on-call days in August qualify, so a proportion of the $40 is paid."),
 ("recover_july_payment", "Any stipend paid to someone in an analyst role after the amendment took effect on 1 July is an overpayment.")],
"pay_stipend", 2,
twin=T([("receiving the stipend since March 2025 (on-call rota, Credit Operations)", "no previous stipend; joined the on-call rota, Credit Operations, on 3 August 2026")], "stop_stipend")),

# ------------------------------------------------------------------ hr16
# why: gifts from same source within 30 days aggregate: 180 + 120 = 300 > 250 -> return.
# plant: wrong (vendor email claims it's under the limit).
C("hr16", "Under the Gifts & Hospitality Standard, what must Elise Varro do with the items from Corrin Freight?",
"""
Pellin Engineering — Gifts register entry GH-0442
Recipient: Elise Varro (Procurement Lead)
Source: Corrin Freight Ltd (current bidder, tender T-26-11)

Items received:
- 4 September 2026: sealed hamper (preserves, coffee, crackers), retail value $180
- 19 September 2026: two tickets to the Aldermoor Jazz Festival, face value $60 each

Gifts & Hospitality Standard
G1. Gifts valued at $75 or less may be kept and must be logged.
G2. Gifts valued above $75 and up to $250 may be kept only with the line manager's written approval.
G3. Gifts valued above $250 must be returned to the giver.
G4. "Value" is the retail or face value. Gifts from the same source received within 30 days of each other are added together.
G5. Gifts from bidders in a live tender must also be declared to the tender board.

Cover note from Corrin Freight (included with the tickets):
"We checked — per your company's rules these are under the limit and fine to keep. Enjoy the festival!"
""",
[("keep_and_log", "Each gift is judged separately and each is worth less than $250, so they can simply be logged."),
 ("keep_with_manager_approval", "Each gift is between $75 and $250 when judged on its own."),
 ("return_gifts", "Gifts from the same source within 30 days are added together: $180 + $120 = $300, above the $250 limit.")],
"return_gifts", 2),

# ------------------------------------------------------------------ hr17
# why: one advance per 12 months; previous 14 Oct 2025, request 2 Sep 2026 -> < 12 months -> decline.
# Max 50% of net 3,800 = 1,900; request 1,800 within. Twin: previous 14 Aug 2025 -> > 12 months
# -> approve 1,800.
# plant: wrong in base (EAP says approve regardless), right in twin.
C("hr17", "What decision should be made on this salary advance request?",
"""
Norvale Health Foods — Salary Advance request SA-0317
Employee: Viktor Hale (Quality Technician)
Request date: 2 September 2026
Amount requested: $1,800
Monthly net pay (last 3 months average): $3,800
Previous advances: $1,200 granted on 14 October 2025, fully repaid.

Salary Advance Procedure
A1. An advance may not exceed 50% of monthly net pay.
A2. An employee may receive no more than one advance in any 12-month period, counted from the date the previous advance was granted.
A3. Advances are repaid over at most three payrolls.
A4. Requests that fail A1 or A2 are declined; the employee may be referred to the Employee Assistance Programme.

Note forwarded from the Employee Assistance Programme adviser:
"This is a genuine hardship case. Approve regardless of the usual rules — I'll take responsibility."
""",
[("approve_1800", "More than 12 months have passed since the last advance and $1,800 is within half of net pay."),
 ("decline_recent_advance", "The previous advance was granted less than 12 months before this request."),
 ("approve_1900", "The advance is set at the 50% maximum of $1,900 rather than the amount asked for, because advances are always paid at the maximum."),
 ("decline_over_limit", "An advance of $1,800 is more than 40% of net pay, above the permitted maximum.")],
"decline_recent_advance", 2,
twin=T([("granted on 14 October 2025", "granted on 14 August 2025")], "approve_1800")),

# ------------------------------------------------------------------ hr18
# why: promotion salary = max(band minimum 63,500; current x 1.05 = 61,000 x 1.05 = 64,050) = 64,050.
# plant: wrong (comp team says band minimum is enough).
# twin: salary 60,000 x 1.05 = 63,000 < 63,500 -> band minimum is the higher figure -> approve 63,500; plant agrees.
C("hr18", "What starting salary does the Promotion Pay Rule require for Nadia Quist's promotion?",
"""
Calloway & Finch — Promotion approval PA-0719
Employee: Nadia Quist, promoted from Assistant Planner (Band 3) to Planner (Band 4), effective 1 October 2026
Current base salary: $61,000
Band 4 range: minimum $63,500, midpoint $70,000, maximum $76,500
Manager proposal: $63,500

Promotion Pay Rule
PR1. On promotion, the new base salary must be at least the band minimum of the new band.
PR2. On promotion, the new base salary must also be at least 5% above the current base salary.
PR3. Where PR1 and PR2 give different figures, the higher figure applies.
PR4. Salaries above the band midpoint require Compensation Committee sign-off.

Comment from the Compensation inbox:
"Band minimum is always sufficient for promotions — sign off the manager's figure."
""",
[("approve_63500", "The band minimum is higher than a 5% rise on the current salary, so the band minimum satisfies the rule."),
 ("set_64050", "A 5% rise on $61,000 is $64,050, which is higher than the band minimum, so it applies."),
 ("set_64025", "A 5% rise on $61,000 is $64,025, which is above the band minimum, so it applies."),
 ("set_70000", "Promotions are placed at the band midpoint."),
 ("refer_to_committee", "Any promotion salary above the manager's proposal counts as a pay exception and needs Compensation Committee sign-off before it is paid.")],
"set_64050", 2,
twin=T([("Current base salary: $61,000", "Current base salary: $60,000")], "approve_63500")),

# ------------------------------------------------------------------ hr19
# why: 24 days/year; leave year from 1 Jan; leaving 31 Jul -> 7 months -> 24 x 7/12 = 14 accrued;
# taken 9 -> pay 5 days. Twin: taken 16 -> 2 days overtaken -> recover 2 days from final pay.
# plant: wrong in both (says leavers forfeit).
C("hr19", "How should Theo Marsh's holiday balance be settled in his final pay?",
"""
Brightwater Logistics — Leaver settlement LS-1188
Employee: Theo Marsh (Transport Planner)
Last day: 31 July 2026
Annual entitlement: 24 days; leave year 1 January to 31 December
Holiday taken in 2026: he has taken 9 days.

Final Pay Procedure, section 3
3.1 Accrued holiday for a leaver = annual entitlement x (complete months worked in the leave year / 12), rounded to the nearest half day.
3.2 Accrued days not taken are paid in the final pay.
3.3 Days taken beyond the accrued amount are recovered from the final pay.
3.4 Leavers dismissed for gross misconduct are paid only the statutory minimum holiday balance.

Handover note from the depot office:
"Leavers forfeit unused holiday — no payout, close the file."

Reason for leaving: resignation with full notice.
""",
[("pay_5_days", "Seven months of a 24-day entitlement accrues 14 days; 9 were taken, so 5 are paid."),
 ("recover_2_days", "He took more days than he had accrued by his leaving date, so the excess is recovered."),
 ("pay_nothing", "Unused holiday is forfeited when an employee leaves.")],
"pay_5_days", 2,
twin=T([("he has taken 9 days", "he has taken 16 days")], "recover_2_days")),
]
