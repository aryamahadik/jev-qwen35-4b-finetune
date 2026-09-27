"""proc_multihop / people operations: leave, pay rules, rosters, eligibility
(Fenholt Distribution, Carraway Mutual, Saltire Bakeries, Ennerdale Council,
Vostok Games Studio, Ribbonfield Hospital Trust support services)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ hr01
# why: default carry-over 5 days; amendment raises to 10 only for staff under a
# company-imposed blackout, and the blackout list covers Warehouse and Transport only.
# Finance analyst -> carry 5, 3 forfeited (payout only on leaving).
# Twin: department Warehouse -> blackout -> carry all 8.
C("hr01", "How should HR process Sofia Brandt's unused leave at year end?",
"""
Fenholt Distribution — Annual Leave Policy (extract)

4.1 Up to 5 days of unused annual leave may be carried into the next leave year. Any further unused days are forfeited.
4.2 Unused leave is paid out only when employment ends.
4.3 (Amended September) An employee who could not take leave because of a company-imposed blackout may carry over up to 10 days.

Definitions
"Company-imposed blackout": a period listed in the Blackout Calendar during which leave requests from the listed departments are not accepted.

Blackout Calendar (this leave year)
| Period | Departments |
| 15 Nov - 31 Dec | Warehouse, Transport |
| 1 - 14 Apr | Transport |

Year-end leave report
Employee: Sofia Brandt — Department: Finance (management accounts)
Unused days: 8
Employee comment: "Year-end close ran through December, so I couldn't use my leave. Please carry all 8 days."
""",
[("carry_all_8", "She was unable to take leave during the December blackout because of year-end close, so up to 10 days can be carried over under 4.3."),
 ("carry_5_forfeit_3", "Finance is not a blackout department, so the standard 5-day limit applies and 3 days are forfeited."),
 ("pay_out_8", "Unused days that cannot be carried are paid out at year end.")],
"carry_5_forfeit_3", 2),

# ------------------------------------------------------------------ hr02
# why: week Sun-Sat. Monday 25 Aug is a public holiday -> 8 h double time. Footnote:
# double-time hours do not count toward 40. Non-holiday hours = 8*4 + 6 = 38 -> no
# time-and-a-half. Twin: Saturday 12 h -> 32 + 12 = 44 -> 4 h overtime.
C("hr02", "Which pay treatment applies to Owen Pike's timesheet for the week of 24 August?",
"""
Saltire Bakeries — Hourly Pay Rules

1. The pay week runs Sunday to Saturday.
2. Hours worked on a public holiday are paid at double time.
3. Hours worked beyond 40 in a pay week are paid at time-and-a-half.
Footnote to rule 3: hours paid at double time are left out when counting toward the 40-hour threshold.
4. Night premium (22:00-06:00): +15%, applied on top of any rate.

Public holidays this quarter: Monday 25 August.

Timesheet — Owen Pike (day shift, 05:00-13:00 start times vary)
| Day | Hours |
| Sun 24 Aug | 0 |
| Mon 25 Aug | 8.0 |
| Tue 26 Aug | 8.0 |
| Wed 27 Aug | 8.0 |
| Thu 28 Aug | 8.0 |
| Fri 29 Aug | 8.0 |
| Sat 30 Aug | 6.0 |
""",
[("holiday_double_plus_overtime", "The holiday hours are paid double, and the other hours still take the week beyond 40."),
 ("holiday_double_only", "The holiday hours are paid double, and once they are left out the rest of the week does not pass 40 hours."),
 ("overtime_only", "The week totals more than 40 hours, so the hours above 40 are paid at time-and-a-half and nothing else changes.")],
"holiday_double_only", 3,
twin=T([("| Sat 30 Aug | 6.0 |", "| Sat 30 Aug | 12.0 |")], "holiday_double_plus_overtime")),

# ------------------------------------------------------------------ hr03
# why: limit 20 working days/calendar year in approved countries (Veloria approved).
# Working days exclude home public holidays: 29 Jun-10 Jul = 10 weekdays minus 1 Jul
# (home holiday) = 9. Used 11 + 9 = 20 <= 20 -> approve. Twin: used 12 -> 21 -> tax review.
C("hr03", "What should the mobility team decide on Aoife Rennick's request to work from Veloria?",
"""
Vostok Games Studio — Working From Abroad Guidelines

1. Staff may work remotely from an approved country for up to 20 working days in a calendar year without further review.
2. A request that would take the year's total above 20 working days must go to the tax and payroll review.
3. Requests for countries not on the approved list are declined.
4. Definitions: "working day" means a Monday to Friday that is not a public holiday in the employee's home office location.

Approved countries: Veloria, Ostmark, Pellan Islands.
Home office public holidays this summer: Wednesday 1 July.

Request WFA-88
Employee: Aoife Rennick (home office: Dunmere)
Destination: Veloria
Dates: Monday 29 June to Friday 10 July
Working days already spent abroad this calendar year: 11 (Ostmark, March).
""",
[("approve_request", "The trip adds 9 working days, bringing the year to exactly 20, which is within the limit."),
 ("refer_to_tax_review", "The trip would take her working days abroad this year above 20."),
 ("decline_country", "Veloria is not an approved country.")],
"approve_request", 3,
twin=T([("Working days already spent abroad this calendar year: 11 (Ostmark, March).",
         "Working days already spent abroad this calendar year: 12 (Ostmark, March).")], "refer_to_tax_review")),

# ------------------------------------------------------------------ hr04
# why: completion date = certificate issue date (10 Apr 2025). Leaving 15 Mar 2026 ->
# 11 months after completion -> within 12 -> 100%. Cost £2,400 > £1,000 (no exemption).
# Twin: certificate 1 Mar 2025 -> 12.5 months -> 50%.
C("hr04", "What repayment applies to Tomasz Werner's training funding?",
"""
Carraway Mutual — Study Support Agreement (standard terms)

1. Definitions: "completion date" means the date the awarding body issues the certificate, not the last day of teaching.
2. If the employee resigns and their last day of employment falls:
 (a) within 12 months of the completion date — repay 100% of the funded fees;
 (b) more than 12 and up to 24 months after the completion date — repay 50%;
 (c) more than 24 months after — no repayment.
3. (Amended 2024) Courses whose funded fees are below £1,000 are exempt from repayment.
4. Repayment is deducted from final pay where the employee agrees in writing.

Study record — Tomasz Werner
Course: Diploma in Insurance Practice (Kelbrook Institute)
Funded fees: £2,400
Teaching: 3 September 2024 - 20 February 2025
Certificate issued 10 April 2025

Resignation received 14 February 2026; last day of employment 15 March 2026.
""",
[("repay_100_percent", "His last day falls within 12 months of the certificate date, so the full fees are repaid."),
 ("repay_50_percent", "His last day falls between 12 and 24 months after completion, so half the fees are repaid."),
 ("no_repayment", "The course is exempt, or more than 24 months have passed, so nothing is repaid.")],
"repay_100_percent", 2,
twin=T([("Certificate issued 10 April 2025", "Certificate issued 1 March 2025")], "repay_50_percent")),

# ------------------------------------------------------------------ hr05
# why: Nadia has forklift cert (qualified). Consecutive: Mon-Fri = 5 (<= 6). Rest: Thu
# night ends 06:00 Fri, her Fri late starts 14:00 -> 8 h < 11 -> reject for rest.
# Twin: Fri late 17:00-01:00 -> 11 h rest -> meets minimum -> approve.
C("hr05", "Should the roster lead approve the cover request for Thursday night?",
"""
Fenholt Distribution — Rostering Rules (Goods-In)

R1. A shift may be covered only by someone qualified for its role (see skills matrix).
R2. Nobody may work more than 6 shifts in a row.
R3. There must be at least 11 hours' rest between the end of one shift and the start of the next.
R4. Cover requests are approved by the roster lead.

Skills matrix
| Name | Night loader (forklift) | Day picker |
| Nadia Farouk | yes | yes |
| Ben Ashdown | yes | yes |
| Ruth Kiely | no | yes |

Nadia Farouk's current roster (this week)
Mon: early 06:00-14:00
Tue: early 06:00-14:00
Wed: early 06:00-14:00
Thu: off
Fri: late 14:00-22:00
Sat, Sun: off

Cover request CR-117: Ben Ashdown asks Nadia to cover his Thursday night loader shift, Thu 22:00 - Fri 06:00. Nadia has agreed.
""",
[("approve_cover", "Nadia is qualified, stays within six shifts in a row and keeps the minimum rest between shifts."),
 ("reject_rest_breach", "Her Friday shift would start less than 11 hours after the night shift ends."),
 ("reject_not_qualified", "The night loader role needs a forklift qualification that Nadia does not hold."),
 ("reject_too_many_in_row", "Adding Thursday gives her more than six consecutive shifts.")],
"reject_rest_breach", 2,
twin=T([("Fri: late 14:00-22:00", "Fri: late 17:00-01:00")], "approve_cover")),

# ------------------------------------------------------------------ hr06
# why: parent-in-law = parent of spouse or partner (immediate family -> 5 days). Amendment:
# partner includes cohabiting partner of 6+ months; cohabiting 14 months -> partner ->
# 5 days. Twin: cohabiting 4 months -> not a partner -> not immediate or extended family
# (extended list: grandparent, grandchild, aunt, uncle) -> annual leave only.
C("hr06", "How much bereavement leave can Callum Reyes take?",
"""
Ennerdale Council — Bereavement Leave Scheme

1. Immediate family: 5 days' paid leave.
2. Extended family: 2 days' paid leave.
3. Other losses: employees may book annual leave in the normal way.

Definitions
- Immediate family: spouse or partner, child, parent, sibling, and parent-in-law.
- Parent-in-law: a parent of the employee's spouse or partner.
- Extended family: grandparent, grandchild, aunt or uncle.
- Partner (amended 2025): a person the employee has lived with as a couple for at least 6 months, whether or not married.

Request, Monday
Callum Reyes (Highways, grade 4): "My girlfriend Maya's father died on Saturday. We're not married but have lived together for 14 months. I'd like time off for the funeral and to support her family."
Address history on file confirms a shared address since July of last year.
""",
[("five_days_paid", "Maya counts as his partner, so her father is a parent-in-law and falls under immediate family."),
 ("two_days_paid", "A girlfriend's parent is extended family because the couple are not married."),
 ("annual_leave_only", "Maya does not meet the definition of partner, so her father is neither immediate nor extended family.")],
"five_days_paid", 2,
twin=T([("have lived together for 14 months", "have lived together for 4 months"),
        ("confirms a shared address since July of last year", "confirms a shared address since four months ago")], "annual_leave_only")),

# ------------------------------------------------------------------ hr07
# why: start 3 Feb -> 6-month probation ends 2 Aug. Extension only if review held before
# the end; review held 5 Aug -> too late -> deemed passed -> confirm.
# Twin: review 29 Jul (before end) -> extension allowed -> extend 3 months.
C("hr07", "What outcome does the probation policy require for Idris Oyelaran?",
"""
Ribbonfield Hospital Trust — Probation Policy (support services)

1. New starters serve a 6-month probation period starting on their first day.
2. The line manager must hold a final probation review before the probation period ends.
3. At that review the manager may confirm the appointment, extend probation once by up to 3 months, or end employment.
4. If no final review is held before the end of the probation period, the employee is deemed to have passed probation and the appointment is confirmed.

Employee: Idris Oyelaran, Portering Supervisor
First day: 3 February
Final probation review held: 5 August
Manager's review note: "Attendance fine, rota planning still weak. I want to extend by 3 months with a support plan."
""",
[("extend_three_months", "The manager held the final review and chose a single 3-month extension, which rule 3 allows."),
 ("confirm_appointment", "The review took place after the probation period ended, so he is deemed to have passed."),
 ("end_employment", "Weak rota planning during probation is grounds to end employment.")],
"confirm_appointment", 2,
twin=T([("Final probation review held: 5 August", "Final probation review held: 29 July")], "extend_three_months")),

# ------------------------------------------------------------------ hr08
# why: full pay up to 10 days of jury service; amendment: part-timers pro rata by
# contracted days (10 x 3/5 = 6). Served 8 of her working days -> 6 full pay, then
# court allowance only. Twin: full-time -> 10 -> all 8 on full pay.
C("hr08", "How should payroll treat Greta Solberg's jury service days?",
"""
Carraway Mutual — Jury Service Pay

1. Employees summoned for jury service receive full pay for up to 10 working days of service in any one summons.
2. After that, the employee claims the court's loss-of-earnings allowance and the company pays nothing further.
3. (Amended 2025) For part-time employees, the 10-day limit in rule 1 is reduced pro rata to contracted days per week (full-time = 5 days).
4. Evidence: the court's attendance certificate.
5. Employees must tell their manager within 5 working days of receiving a summons. Deferral requests to the court are the employee's own decision.
6. Days of service falling on non-contracted days are not paid by the company.

Employee: Greta Solberg, Complaints Handler
Contract: part-time, 3 days a week (Mon, Tue, Wed)
Court attendance certificate: attended on 8 of her contracted working days (summons JS-2291).
""",
[("full_pay_all_days", "All 8 attended days fall within the 10-day full-pay limit."),
 ("full_pay_then_allowance", "Her pro-rata limit is 6 days, so 6 days are on full pay and the rest go to the court allowance."),
 ("allowance_only", "Part-time staff claim the court allowance for every day of jury service.")],
"full_pay_then_allowance", 2,
twin=T([("Contract: part-time, 3 days a week (Mon, Tue, Wed)", "Contract: full-time, 5 days a week")], "full_pay_all_days")),

# ------------------------------------------------------------------ hr09
# why: night of Mon 25 Aug is a public holiday -> amendment: treat as weekend -> weekend
# standby. Callout = remote login or site attendance; 40-min remote session -> callout
# with 2-hour minimum. Twin: 10-min phone advice only -> no callout -> weekend standby only.
C("hr09", "Which on-call payment applies to Nell Hargreaves for the night of Monday 25 August?",
"""
Vostok Games Studio — On-Call Payments (Live Operations)

1. Standby: £40 per weekday night; £60 per weekend night (Friday, Saturday, Sunday nights).
2. (Amended April) A night that falls on a public holiday is paid as a weekend night.
3. Callout: paid per hour with a minimum of 2 hours. A callout means the engineer logged in remotely or attended site. Phone advice alone is not a callout.

Public holidays: Monday 25 August.

On-call log — Nell Hargreaves
| Night | Event |
| Sun 24 Aug | no pages |
| Mon 25 Aug | 01:12 paged, match servers lagging; remote login 01:15-01:55, restarted matchmaker |
| Tue 26 Aug | no pages |
""",
[("weekday_standby_only", "Monday is a weekday night and the page was handled quickly, so only weekday standby is due."),
 ("weekday_standby_plus_callout", "Monday is a weekday night, so the weekday standby rate applies, and the remote login counts as a callout paid with the 2-hour minimum."),
 ("weekend_standby_only", "The holiday night is paid at the weekend rate, and there was no callout that night."),
 ("weekend_standby_plus_callout", "The holiday night is paid at the weekend rate, and the remote login counts as a callout with the 2-hour minimum.")],
"weekend_standby_plus_callout", 2,
twin=T([("remote login 01:15-01:55, restarted matchmaker", "gave phone advice for 10 minutes; the shift lead restarted the matchmaker")], "weekend_standby_only")),

# ------------------------------------------------------------------ hr10
# why: 8 weeks' notice needed. Notice 20 Mar, start 1 May = 6 weeks -> manager may
# postpone to 8 weeks after notice = 15 May. Not an early birth. Twin: notice 1 Mar ->
# 8 weeks 4 days before 1 May -> approve.
C("hr10", "What should the manager do with Leon Achterberg's parental leave notice?",
"""
Saltire Bakeries — Parental Leave Procedure

1. Employees give at least 8 weeks' written notice of the start date of parental leave.
2. If less notice is given, the company may postpone the start to the date 8 weeks after the notice was received, unless rule 3 applies.
3. Where a child is born earlier than the expected week of childbirth, leave may start on the birth date regardless of notice.
4. Parental leave cannot be refused, only postponed as in rule 2.

Notice received: Friday 20 March
From: Leon Achterberg, Dispatch
"Our baby is due in the week of 27 April. I'd like parental leave to begin on Friday 1 May, for four weeks."
Manager note: dispatch is short-staffed in early May due to the spring promotion.
""",
[("approve_start_date", "He gave at least 8 weeks' notice before his chosen start date."),
 ("postpone_to_15_may", "His notice is shorter than 8 weeks, so the start can be moved to 8 weeks after the notice arrived."),
 ("refuse_leave", "Staff shortages in early May allow the request to be refused.")],
"postpone_to_15_may", 2,
twin=T([("Notice received: Friday 20 March", "Notice received: Friday 27 February")], "approve_start_date")),

# ------------------------------------------------------------------ hr11
# why: 5 years' continuous service; contractor periods do not count. Employee since
# 6 Jan 2020; request 1 Nov 2024 -> 4 y 10 m -> not eligible. Twin: request 1 Mar 2025
# -> 5 y 2 m -> eligible (manager's business-need note is not a criterion).
C("hr11", "How should HR answer Dmitri Vale's sabbatical application?",
"""
Vostok Games Studio — Sabbatical Scheme

1. Employees with at least 5 years' continuous service may take an unpaid sabbatical of 1 to 3 months.
2. Continuous service counts from the first day as an employee. Time worked as a contractor or through an agency does not count. A gap of up to one month between contracts of employment does not break continuity.
3. Approval may be delayed (not refused) by up to 6 months for release planning.

Employment history — Dmitri Vale
| Period | Status |
| Jan 2019 - Dec 2019 | contractor via Tessellate Talent |
| 6 Jan 2020 - present | employee, Senior Animator |

Application received 1 November 2024: sabbatical for February and March 2025.
Manager note: "Fine by me, the Q1 milestone is covered."
""",
[("approve_sabbatical", "His service as an employee alone reaches 5 years by the application date."),
 ("decline_insufficient_service", "His employee service began in January 2020, so he does not yet have 5 years' continuous service."),
 ("delay_for_release_planning", "The request can be delayed up to 6 months because of the Q1 milestone.")],
"decline_insufficient_service", 2,
twin=T([("Application received 1 November 2024: sabbatical for February and March 2025.",
         "Application received 1 March 2025: sabbatical for June and July 2025.")], "approve_sabbatical")),

# ------------------------------------------------------------------ hr12
# why: fortnightly pay periods from Mon 5 Jan 2026: P1 5-18 Jan, P2 19 Jan-1 Feb,
# P3 2-15 Feb, P4 16 Feb-1 Mar. Shift 22 Jan in P2 -> deadline = end of 2nd period after
# (P4) = 1 Mar. Submitted 27 Feb -> in time -> next payroll.
# Twin: submitted 3 Mar -> late -> HR Director late-claim route.
C("hr12", "Where should timesheet correction TC-470 go?",
"""
Ennerdale Council — Timesheet Corrections

1. Pay periods are fortnightly, Monday to Sunday, starting Monday 5 January 2026.
2. A correction is processed in the next payroll if it is submitted no later than the last day of the second pay period after the period in which the shift was worked.
3. A later correction is a late claim and needs HR Director approval.
4. Corrections are never rejected solely for lateness; they follow rule 3.
5. Overtime corrections also need the budget holder's sign-off.

TC-470
Employee: Harriet Moss (Refuse Collection, crew 3)
Shift: Thursday 22 January 2026, 06:00-14:00 — recorded as absence in error.
Correction submitted: Friday 27 February 2026.
Type: standard hours (not overtime).
""",
[("process_next_payroll", "The correction arrived before the end of the second pay period after the one containing 22 January."),
 ("route_as_late_claim", "The correction arrived after the end of the second pay period following the one in which the shift was worked, so it is a late claim."),
 ("reject_as_late", "Corrections for shifts more than a month old are rejected.")],
"process_next_payroll", 3,
twin=T([("Correction submitted: Friday 27 February 2026.", "Correction submitted: Tuesday 3 March 2026.")], "route_as_late_claim")),

# ------------------------------------------------------------------ hr13
# why: 18 months in current role; "current role" runs from last job-code change; a grade
# change within the same job code does not reset. Job code since 1 Jun 2022 -> 51 months
# on 1 Sep 2026 -> ok. Reviews 3 and 4 -> meets or above. Eligible.
# Twin: 1 Apr 2025 was a lateral move to a new job code -> 17 months -> ineligible.
C("hr13", "Is Farah Qureshi eligible to apply for the Brenmoor secondment?",
"""
Carraway Mutual — Internal Secondment Rules

1. To apply, an employee must have (a) at least 18 months in their current role and (b) a rating of "meets expectations" or higher in each of their last two annual reviews.
2. Definitions
 - Current role: the role held since the employee's most recent change of job code. A change of pay grade within the same job code does not start a new role.
 - Ratings: 1 = below, 2 = partially meets, 3 = meets, 4 = exceeds, 5 = outstanding.
3. Secondments last 6 to 12 months.

Employee record — Farah Qureshi
| Date | Change | Job code |
| 1 June 2022 | joined as Claims Analyst | CL-204 |
| 1 April 2025 | promotion to grade 6, same role | CL-204 |
Reviews: 2024 rating 3; 2025 rating 4.

Application date: 1 September 2026.
""",
[("eligible_forward_application", "She has more than 18 months under her current job code and both recent ratings are at least 3."),
 ("ineligible_time_in_role", "Her current role started less than 18 months before the application date."),
 ("ineligible_ratings", "One of her last two ratings is below meets expectations.")],
"eligible_forward_application", 2,
twin=T([("| 1 April 2025 | promotion to grade 6, same role | CL-204 |", "| 1 April 2025 | lateral move to Underwriting Assistant | UW-118 |")], "ineligible_time_in_role")),

# ------------------------------------------------------------------ hr14
# why: 10-year award counts service with acquired company Brenwick only for employees on
# the transfer list. Farrow is on it -> service from 1 Oct 2016 -> 10 years on
# 1 Oct 2026 -> award. Twin: not on list (hired separately in 2021) -> no award yet.
C("hr14", "What long-service action applies to Ellis Farrow in October 2026?",
"""
Saltire Bakeries — Long Service Awards

1. Awards: 10 years' service — 3 extra days of leave and a £250 voucher; 20 years — 5 extra days and a £500 voucher.
2. Awards are made in the month of the service anniversary.
3. Service counts from the start of continuous employment with Saltire.
4. (Added after the 2020 acquisition) Service with Brenwick Foods counts as Saltire service for employees named on the Brenwick transfer list of 1 March 2020.

Brenwick transfer list (extract): R. Aldous; E. Farrow; M. Gideon; S. Petrov.

Employee record — Ellis Farrow
Brenwick Foods: 1 October 2016 - 29 February 2020 (production operative)
Saltire: 1 March 2020 - present (production supervisor)
""",
[("make_10_year_award", "His Brenwick service counts, so he reaches 10 years' service on 1 October 2026."),
 ("no_award_yet", "His Saltire service began in March 2020, so he has not yet reached 10 years of continuous service with Saltire."),
 ("make_20_year_award", "Combined service across both companies qualifies him for the higher award.")],
"make_10_year_award", 1),

# ------------------------------------------------------------------ hr15
# why: routing: harassment (defined: unwanted conduct related to a protected
# characteristic, incl. national origin) goes to Dignity at Work whoever it is about.
# Comments on accent/origin -> harassment -> Dignity at Work.
# Twin: complaint about director cutting training budget -> not harassment -> about a
# director -> HR Director.
C("hr15", "To whom should grievance G-26-014 be routed?",
"""
Ennerdale Council — Grievance Procedure: routing table

Step 1. If the grievance alleges harassment, it goes to the Dignity at Work team, whoever it concerns.
Step 2. Otherwise, a grievance about a director goes to the HR Director.
Step 3. Any other grievance goes to the line manager's own manager.

Definitions
- Harassment: unwanted conduct related to a protected characteristic (including age, disability, race, national origin, religion, sex and sexual orientation) that violates dignity or creates a hostile environment.
- Director: a member of the Corporate Leadership Team.

Grievance G-26-014
From: Anika Draper, Planning Officer
About: Julian Fairweather, Director of Place (member of the Corporate Leadership Team)
Summary: "In three team meetings Julian mimicked my accent and made remarks about where my family comes from. Colleagues laughed along. I feel I can't speak up in meetings any more."
""",
[("line_managers_manager", "The grievance is about the person above her in the reporting line, so it goes one level higher."),
 ("hr_director", "The grievance concerns a member of the Corporate Leadership Team, so step 2 sends it to the HR Director whatever the complaint is."),
 ("dignity_at_work_team", "The conduct described relates to national origin and is unwanted, so step 1 routes it to Dignity at Work.")],
"dignity_at_work_team", 1),

# ------------------------------------------------------------------ hr16
# why: April review includes staff who started before 1 October last year (15 Sep ok).
# Excluded if a final written warning is live on 1 April; warnings expire 12 months after
# issue: 20 Mar last year -> expired 20 Mar this year -> include.
# Twin: warning 20 May last year -> live on 1 April -> exclude.
C("hr16", "Should Rory Tennant be included in this year's April pay review?",
"""
Fenholt Distribution — Annual Pay Review Rules

1. The pay review takes effect on 1 April.
2. Employees who started before 1 October of the previous year are eligible.
3. An employee with a live final written warning on 1 April is excluded from the review.
4. Disciplinary warnings expire 12 months after the date of issue and are then disregarded.
5. Employees on long-term sick leave are included.
6. Review increases are pro-rated for part-time staff.

Employee record — Rory Tennant (Transport planner)
Start date: 15 September last year
Disciplinary history: final written warning issued 20 March last year (late submission of tachograph data).
Absence: none this year.
""",
[("include_in_review", "He started before 1 October last year and his final warning expired before 1 April."),
 ("exclude_started_too_late", "He started less than a year before the review date."),
 ("exclude_live_warning", "His final written warning is still live on 1 April.")],
"include_in_review", 2),

# ------------------------------------------------------------------ hr17
# why: min 3 of 5 agents per day. Wed 18 Jun already has 1 approved absence -> 4 in.
# Colm (1 Jun) is earlier than Rana (2 Jun); approving Colm -> 3; Rana would make 2 ->
# decline Rana. Twin: the existing leave is for Thursday -> 5 in -> both fit (3 left).
C("hr17", "What decision should the team lead make on Rana Petit's leave request?",
"""
Carraway Mutual — Contact Centre Leave Rules (Team Blue, 5 agents)

1. At least 3 agents must be working on every weekday.
2. Requests are decided in the order they were submitted.
3. Leave already approved is not revisited to make room for new requests.
4. Training days count as working days.

Approved leave, week of 16 June
| Agent | Date |
| J. Obi | Wed 18 June |

Pending requests
| Agent | Date requested | Submitted |
| Colm Brady | Wed 18 June | 1 June |
| Rana Petit | Wed 18 June | 2 June |

Rana's note: "It's my sister's graduation, I really need this one."
""",
[("approve_request", "Approving Rana still leaves at least three agents working that day."),
 ("decline_minimum_staffing", "Once the earlier request is approved, granting Rana's would leave fewer than three agents that day."),
 ("approve_and_cancel_obi_leave", "A family event takes priority, so J. Obi's leave can be withdrawn to cover.")],
"decline_minimum_staffing", 2,
twin=T([("| J. Obi | Wed 18 June |", "| J. Obi | Thu 19 June |")], "approve_request")),

# ------------------------------------------------------------------ hr18
# why: car scheme needs grade 7+ OR business mileage > 10,000 a year; business mileage
# excludes commuting. Grade 6; 12,400 - 3,100 = 9,300 -> not eligible -> mileage
# reimbursement only (cash allowance only for eligible staff who opt out).
# Twin: commuting 1,900 -> 10,500 -> eligible; she opts for cash -> cash allowance.
C("hr18", "What car benefit should Marta Lindgren receive?",
"""
Ribbonfield Hospital Trust — Car Benefit Scheme

1. Eligibility: grade 7 or above, or business mileage above 10,000 miles in the last 12 months.
2. Eligible staff choose either a lease car or a monthly cash allowance.
3. Staff who are not eligible claim mileage reimbursement for business journeys only.
4. Definitions: "business mileage" means journeys made for work, excluding travel between home and the usual workplace.
5. Lease cars are replaced every 4 years or 80,000 miles, whichever comes first.

Mileage log — last 12 months — Marta Lindgren, Community Equipment Coordinator (grade 6)
Total miles claimed: 12,400
Of which home-to-base commuting: 3,100

Marta's form: "I'd prefer the cash allowance rather than a lease car."
""",
[("lease_car", "Her total mileage is above 10,000, so she qualifies and a lease car is the default."),
 ("cash_allowance", "Her business mileage is above 10,000, so she is eligible and may take the cash allowance she chose."),
 ("mileage_reimbursement_only", "Once commuting is removed her business mileage is below the threshold and she is below grade 7.")],
"mileage_reimbursement_only", 2,
twin=T([("Of which home-to-base commuting: 3,100", "Of which home-to-base commuting: 1,900")], "cash_allowance")),
]
