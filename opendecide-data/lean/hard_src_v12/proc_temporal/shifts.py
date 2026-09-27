"""proc_temporal / shifts: overtime and holiday premiums, rest rules, clock
changes, on-call timers, payroll cut-offs across time zones, night and weekend
premiums, leave accrual, call-out minimums, probation dates, lateness counts
(Harbourline Care, Sorrel Rail Maintenance, Quenby Distribution, Axle & Ivy
Support, Norcott Water, Ferrisdale Hospital Trust estates and others)."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ sh01
# why: holiday hours paid at 2x and NOT counted toward the 40-hour threshold.
# Week: Mon 9, Tue 9, Wed 8 (public holiday), Thu 10, Fri 9, Sat 5 = 50; non-holiday 42
# -> 40 x 20 + 2 x 30 + 8 x 40 = 800 + 60 + 320 = 1,180.
# Twin: Wed not a holiday -> 50 counted -> 40 x 20 + 10 x 30 = 1,100.
C("sh01", "What gross pay should this week's payslip show?",
"""
Quenby Distribution — Hourly Pay Rules (warehouse operatives)

W1. Basic rate: 20.00 per hour.
W2. Hours worked in a pay week (Monday to Sunday) beyond 40 are paid at time-and-a-half (30.00).
W3. Hours worked on a public holiday are paid at double time (40.00). These hours are not counted toward the 40 hours in W2.
W4. Public holidays in 2026 (for this site): 1 Jan, 3 Apr, 6 Apr, 6 May, 25 May, 31 Aug, 25 Dec, 28 Dec.

Timesheet — Alban Kurtovic, week beginning Monday 4 May 2026
Monday 4 May: 9 h
Tuesday 5 May: 9 h
Wednesday 6 May: 8 h
Thursday 7 May: 10 h
Friday 8 May: 9 h
Saturday 9 May: 5 h
Total: 50 h
Shift manager's note: "50 hours, so 10 at time-and-a-half."
""",
[("pay_1180", "Wednesday's 8 holiday hours are paid at double and left out of the weekly count, leaving 42 hours: 40 basic and 2 at time-and-a-half."),
 ("pay_1100", "No public holiday fell in the week, so 50 hours give 40 at the basic rate and 10 at time-and-a-half."),
 ("pay_1020", "Wednesday's hours are left out of the weekly count but are paid at the basic rate: 40 basic, 2 at time-and-a-half and 8 basic."),
 ("pay_1420", "Wednesday is paid at double time and also counts toward the 40, so 10 hours are at time-and-a-half on top.")],
"pay_1180", 2,
twin=T([("6 May, 25 May", "25 May, 4 Jun")], "pay_1100")),

# ------------------------------------------------------------------ sh02
# why: at least 11 hours' rest between the end of one shift and the start of the next.
# Tue shift ends 23:00; Wed start 09:30 -> 10.5 h -> breach -> earliest start 10:00.
# Twin: Wed start 10:00 -> exactly 11 h -> compliant.
C("sh02", "What should the rota coordinator do with Wednesday's shift?",
"""
Harbourline Care — Rostering Standard for Home Care Workers

RS1. Every worker must have at least 11 consecutive hours of rest between the end of one shift and the start of the next.
RS2. A worker cannot waive RS1, even by written agreement.
RS3. If a draft rota breaches RS1, the coordinator moves the later shift to the earliest start time that complies. The earlier shift is not changed.
RS4. Travel time between visits is working time.

Draft rota — Ngozi Farrant, care worker
Tuesday 15 September 2026: 15:00–23:00 (last visit ends 22:40, travel home not counted)
Wednesday 16 September 2026: 09:30–17:30
Worker's message: "I'm fine starting at half nine, I'll sign whatever you need."
Coordinator's draft: "Move Wednesday to 11:00 to be safe."
""",
[("approve_as_rostered", "Tuesday's shift ends at 23:00 and Wednesday starts at 10:00, exactly 11 hours later, which meets the rule."),
 ("move_start_to_10_00", "From 23:00 to 09:30 is only 10.5 hours, so Wednesday moves to 10:00, the earliest start that gives 11 hours."),
 ("approve_with_waiver", "The worker has offered to sign a waiver, which allows the 09:30 start."),
 ("move_start_to_11_00", "The rest rule needs a margin, so Wednesday moves to 11:00, 12 hours after Tuesday ends.")],
"move_start_to_10_00", 1,
twin=T([("Wednesday 16 September 2026: 09:30–17:30", "Wednesday 16 September 2026: 10:00–18:00"),
        ("I'm fine starting at half nine", "I'm fine starting at ten")], "approve_as_rostered")),

# ------------------------------------------------------------------ sh03
# why: paid for hours actually worked. Clocks forward 1 h at 02:00 on Sun 29 Mar 2026:
# shift 22:00 Sat 28 Mar - 06:00 Sun 29 Mar on the wall clock = 7 actual hours.
# Twin: shift 22:00 Sat 24 Oct - 06:00 Sun 25 Oct; clocks back 1 h at 03:00 -> 9 hours.
C("sh03", "How many hours should payroll pay for this night shift?",
"""
Sorrel Rail Maintenance — Night Shift Pay Note NS-4

N1. Night-shift staff are paid for the hours actually worked, measured in elapsed time, not by the times on the wall clock.
N2. Clock changes in 2026: clocks go forward one hour at 02:00 on Sunday 29 March (02:00 becomes 03:00); clocks go back one hour at 03:00 on Sunday 25 October (03:00 becomes 02:00).
N3. The scheduled hours on the roster are a planning figure only.
N4. The night premium (not asked about here) is added separately.

Shift record — track renewal, Kelby Junction
Worker: Declan Aroyo, track technician
Clock-on: Saturday 28 March 2026, 22:00 (wall clock)
Clock-off: Sunday 29 March 2026, 06:00 (wall clock)
Unpaid breaks: none (paid meal break on site)
Rostered hours: 8
Supervisor's note: "22:00 to 06:00 — eight hours, as rostered."
""",
[("pay_7_hours", "Clocks went forward one hour during the shift, so 22:00 to 06:00 on the wall clock is 7 hours elapsed."),
 ("pay_9_hours", "Clocks went back one hour during the shift, so 22:00 to 06:00 on the wall clock is 9 hours elapsed."),
 ("pay_8_hours", "The shift ran from 22:00 to 06:00 as rostered, which is 8 hours."),
 ("pay_8_hours_guaranteed", "Rostered hours are guaranteed, so 8 hours are paid whatever the clock change.")],
"pay_7_hours", 2,
twin=T([("Clock-on: Saturday 28 March 2026, 22:00", "Clock-on: Saturday 24 October 2026, 22:00"),
        ("Clock-off: Sunday 29 March 2026, 06:00", "Clock-off: Sunday 25 October 2026, 06:00")], "pay_9_hours")),

# ------------------------------------------------------------------ sh04
# why: P1 page must be acknowledged within 15 min (inclusive). Page 02:07:30 UTC.
# Ack shown on phone 07:52:40 IST (UTC+5:30) = 02:22:40 UTC -> 15 min 10 s -> late ->
# record missed acknowledgement. Twin: ack 07:52:20 IST = 02:22:20 UTC -> 14 min 50 s -> OK.
C("sh04", "What should the on-call report record for the primary engineer?",
"""
Axle & Ivy Support — On-Call Standard, P1 alerts

A1. The primary on-call engineer must acknowledge a P1 page within 15 minutes of the page time. Exactly 15 minutes is in time.
A2. If no acknowledgement is received within 15 minutes, the page escalates automatically to the secondary engineer.
A3. An acknowledgement after 15 minutes is recorded as a missed acknowledgement, even if the engineer then works the incident.
A4. All times in the report are UTC. Times from engineers' phones must be converted.

Incident INC-26-9913 (payments API down)
Page sent to primary (UTC): 02:07:30
Escalation to secondary (UTC): 02:22:30
Primary engineer: Ishaan Relwani, based in Pune (UTC+5:30)
Primary's acknowledgement, screenshot from his phone: 07:52:40 (local time)
Primary's comment: "I acked at 07:52, fifteen minutes after the page — within target."
""",
[("record_missed_ack", "The acknowledgement converts to 02:22:40 UTC, 15 minutes 10 seconds after the page, which is over 15 minutes."),
 ("record_in_time", "The acknowledgement converts to 02:22:20 UTC, 14 minutes 50 seconds after the page, inside 15 minutes."),
 ("record_in_time_worked", "The primary went on to work the incident, so no missed acknowledgement is recorded."),
 ("record_missed_local", "The page went out at 02:07 and the acknowledgement shows 07:52, more than five hours later.")],
"record_missed_ack", 2,
twin=T([("07:52:40 (local time)", "07:52:20 (local time)")], "record_in_time")),

# ------------------------------------------------------------------ sh05
# why: cut-off Monday 10:00 head-office time (UTC+0). Submitted Mon 12 Oct 17:30 UTC+8
# = 09:30 UTC -> in time -> current pay run. Twin: 18:30 UTC+8 = 10:30 UTC -> late ->
# next pay run.
C("sh05", "Which pay run should these overtime hours go into?",
"""
Norcott Water — Payroll Calendar Rules (all offices)

P1. Timesheets for the pay run are due by 10:00 on the Monday before pay day, head-office time (UTC+0).
P2. The submission time is the time stamped by the HR system. Staff abroad must convert their local time.
P3. Timesheets received after the cut-off are paid in the next pay run. They are not rejected.
P4. The October pay run cut-off is Monday 12 October 2026; the next run's cut-off is Monday 9 November 2026.

Timesheet TS-10-5512
Employee: Lucia Brennagh, project engineer, seconded to the Kuala Tembok office (UTC+8)
Overtime claimed: 11.5 hours (5–9 October)
HR system stamp, shown in the employee's local time: Monday 12 October 2026, 17:30
Payroll assistant's note: "Stamped half five in the afternoon, way after 10:00 — push to November."
""",
[("october_run", "17:30 in UTC+8 is 09:30 head-office time, before the 10:00 cut-off."),
 ("november_run", "The local stamp converts to after 10:00 head-office time, so the hours go into the next run."),
 ("reject_timesheet", "The timesheet missed the cut-off, so it is rejected and must be resubmitted."),
 ("november_by_local_time", "The stamp shows 17:30, which is after the 10:00 cut-off.")],
"october_run", 2,
twin=T([("Monday 12 October 2026, 17:30", "Monday 12 October 2026, 18:30"), ("Stamped half five", "Stamped half six")], "november_run")),

# ------------------------------------------------------------------ sh06
# why: shift 18:00-02:30 = 8.5 h minus 30-min unpaid break (22:00-22:30) = 8 paid h at
# 16 = 128. Night premium +25% (4.00/h) for PAID hours between 22:00 and 06:00:
# 22:30-02:30 = 4 h -> 16 -> total 144. Twin: break 20:00-20:30 -> night 22:00-02:30 =
# 4.5 h -> 18 -> 146.
C("sh06", "What should this evening shift pay?",
"""
Ferrisdale Hospital Trust — Estates Staff Pay (porters and domestic staff)

E1. Basic rate: 16.00 per hour.
E2. Night premium: 25% of the basic rate (4.00 per hour) for paid hours worked between 22:00 and 06:00.
E3. Breaks are unpaid and do not earn any premium.
E4. Shifts of more than 6 hours include one 30-minute unpaid break at the time shown on the roster.
E5. Uniform laundering allowance (2.10 per shift) is paid monthly and is not part of shift pay.

Shift record — Ottilie Marsh, porter
Date: Thursday 10 September 2026
Shift: 18:00 to 02:30 (next day)
Break: 22:00–22:30 (as rostered)
Porter's query: "Four and a half hours after ten at night — that's my night premium, right?"
""",
[("pay_144_00", "Eight paid hours at 16.00, plus the premium on 4 paid night hours (22:30 to 02:30) because the break fell at 22:00."),
 ("pay_146_00", "Eight paid hours at 16.00, plus the premium on 4.5 paid night hours (22:00 to 02:30) because the break fell before 22:00."),
 ("pay_154_00", "All 8.5 hours are paid at 16.00, plus the premium on 4.5 night hours."),
 ("pay_160_00", "The shift ran into the night, so the whole 8 paid hours earn the 25% premium.")],
"pay_144_00", 2,
twin=T([("Break: 22:00–22:30 (as rostered)", "Break: 20:00–20:30 (as rostered)")], "pay_146_00")),

# ------------------------------------------------------------------ sh07
# why: accrual 25/12 days per COMPLETE calendar month worked in the leave year.
# Start 15 Mar 2026 -> March incomplete; Apr-Dec = 9 months -> 18.75 -> rounded UP to
# the nearest half day -> 19.0. Twin: start 1 Mar -> 10 months -> 20.83 -> 21.0.
C("sh07", "How many days of annual leave does this new starter get for 2026?",
"""
Pellbrook Surveyors — Staff Handbook, section 5 (Annual leave)

5.1 The leave year runs from 1 January to 31 December.
5.2 Full-time staff receive 25 days' leave per year.
5.3 Staff who join during the year receive 25 ÷ 12 days for each complete calendar month of employment in that leave year. A month in which the employee started on any day other than the 1st is not complete.
5.4 The result is rounded up to the nearest half day.
5.5 Public holidays are in addition to 5.2 and 5.3.

HR record
Employee: Rosalind Achebe-Hart, assistant surveyor (full-time)
Start date: 15 March 2026
HR assistant's draft offer letter: "Leave for 2026: 25 × 9.5/12 = 19.8, so 20 days."
""",
[("leave_19_0", "Nine complete months (April to December) give 18.75 days, which rounds up to 19.0."),
 ("leave_21_0", "Ten complete months (March to December) give 20.83 days, which rounds up to 21.0."),
 ("leave_20_0", "Nine and a half months are worked, giving 19.8 days, rounded up to 20."),
 ("leave_18_5", "Nine complete months give 18.75 days, which rounds to the nearest half day, 18.5.")],
"leave_19_0", 2,
twin=T([("Start date: 15 March 2026", "Start date: 1 March 2026")], "leave_21_0")),

# ------------------------------------------------------------------ sh08
# why: break needed if WORKING TIME is more than 6 h. Paid handover 07:45-08:00 is
# working time -> 07:45-14:00 = 6 h 15 min -> break of 20 min required.
# Twin: no handover (starts 08:00) -> exactly 6 h -> not more than 6 -> no break needed.
C("sh08", "Does this shift pattern need a rest break added?",
"""
Kestrel Retail Group — Working Time Guidance for Store Managers

K1. A worker whose working time on a shift is more than 6 hours must have an uninterrupted break of at least 20 minutes during the shift.
K2. Working time includes paid handovers, briefings and cash-up at the end of a shift.
K3. Time spent travelling from home to the store is not working time.
K4. A break must not be scheduled in the first or last hour of the shift.

Rota check — Harlow Road store
Worker: Tamsin Okoro, sales assistant (age 24)
Paid handover briefing: 07:45–08:00
Shop-floor shift: 08:00–14:00
No breaks rostered.
Store manager's note: "It's a six-hour shift — no break needed."
""",
[("add_20_min_break", "With the paid handover, working time is 6 hours 15 minutes, more than 6 hours."),
 ("no_break_needed", "Working time on the shift is 6 hours, which is not more than 6 hours."),
 ("add_break_first_hour", "A break is needed and should go at 08:00, right after the handover."),
 ("add_30_min_break", "Any shift of 6 hours or more needs a 30-minute break.")],
"add_20_min_break", 1,
twin=T([("Paid handover briefing: 07:45–08:00", "Paid handover briefing: none (store opens with no briefing)")], "no_break_needed")),

# ------------------------------------------------------------------ sh09
# why: 72 hours from AWARENESS, defined as confirmation by the security lead (Fri 16:30),
# not the first alert (Fri 09:00). Deadline Mon 16:30. Notified Mon 15:10 -> in time.
# Twin: notified Mon 17:05 -> late -> record late notification with reasons.
C("sh09", "How should the privacy office log this regulator notification?",
"""
Wensley Building Society — Personal Data Incident Procedure

D1. A notifiable incident must be reported to the regulator within 72 hours of the Society becoming aware of it.
D2. "Becoming aware" means the moment the Head of Security confirms that personal data has been affected. An automated alert is not awareness.
D3. A report made within 72 hours is logged as timely.
D4. A report made after 72 hours is logged as late, and the reasons for delay must be sent with it.
D5. The 72 hours run continuously, including weekends.

Incident PDI-26-044
Automated alert (unusual export from CRM): Friday 11 September 2026, 09:00
Head of Security confirms personal data affected: Friday 11 September 2026, 16:30
Report submitted to regulator: Monday 14 September 2026, 15:10
Compliance analyst's note: "Alert was 09:00 Friday, so our 72 hours ran out 09:00 Monday. We're late."
""",
[("log_timely", "The 72 hours run from confirmation at 16:30 Friday to 16:30 Monday, and the report went in before that."),
 ("log_late_with_reasons", "The 72 hours from confirmation at 16:30 Friday ended at 16:30 Monday, and the report went in after that."),
 ("log_late_from_alert", "The 72 hours run from the 09:00 Friday alert, which makes the Monday afternoon report late."),
 ("log_timely_business_days", "Only business hours count, so the deadline is not until Wednesday.")],
"log_timely", 2,
twin=T([("Report submitted to regulator: Monday 14 September 2026, 15:10", "Report submitted to regulator: Monday 14 September 2026, 17:05")], "log_late_with_reasons")),

# ------------------------------------------------------------------ sh10
# why: swap request must be made at least 48 h before the start of the earlier of the
# two shifts (Fri 18:00). Request Wed 20:00 -> 46 h -> too late -> decline.
# Twin: Wed 17:30 -> 48.5 h -> approve.
C("sh10", "Should the duty manager approve this shift swap?",
"""
Brackwater Leisure Centre — Shift Swap Rules (lifeguards)

S1. Two lifeguards may swap shifts if both hold a current pool lifeguard qualification.
S2. The swap request must be made in the rota app at least 48 hours before the start of the earlier of the two shifts.
S3. Requests made later than that are declined, unless a manager is covering the shift personally.
S4. A swap must not cause either lifeguard to work more than 5 shifts in a week.

Swap request SW-0914
From: Idris Baptiste (Friday 18 September, 18:00–22:00)
To: Clara Voss (Saturday 19 September, 09:00–13:00)
Both qualifications current: yes
Shifts that week after the swap: Idris 4, Clara 5
Request made in app: Wednesday 16 September 2026, 20:00
Manager cover offered: no
Colleague's comment: "It's two days ahead — fine by me."
""",
[("approve_swap", "The request came at least 48 hours before Friday's 18:00 shift, both are qualified and neither goes over 5 shifts."),
 ("decline_swap", "The request came 46 hours before Friday's 18:00 shift, less than 48 hours, and no manager is covering."),
 ("decline_shift_count", "Clara would work 5 shifts in the week, which breaks the limit."),
 ("approve_two_days", "The request came two calendar days before the shift, which meets the notice rule.")],
"decline_swap", 1,
twin=T([("Request made in app: Wednesday 16 September 2026, 20:00", "Request made in app: Wednesday 16 September 2026, 17:30")], "approve_swap")),

# ------------------------------------------------------------------ sh11
# why: clock times rounded to the nearest quarter hour. In 08:52 -> 08:45 (7 min vs 8).
# Out 17:08 -> 17:15 (7 min vs 8). 08:45-17:15 = 8.5 h - 0.5 h unpaid lunch = 8.00 h.
# Twin: out 17:07 -> 17:00 (7 vs 8) -> 8.25 - 0.5 = 7.75 h.
C("sh11", "How many paid hours should the timesheet show for this day?",
"""
Garland Print Works — Timekeeping Rules

G1. Clock-in and clock-out times are rounded to the nearest quarter hour (:00, :15, :30, :45). A time 7 minutes or less from a quarter hour rounds to it.
G2. The unpaid lunch break is 30 minutes and is deducted from every shift longer than 6 hours.
G3. Paid hours = rounded clock-out − rounded clock-in − unpaid lunch.
G4. Rounding applies to everyone equally and is reviewed each year for fairness.

Clock record — Wiktor Szalay, press operator, Tuesday 8 September 2026
Clock-in: 08:52
Clock-out: 17:08
Operator's note: "I was in before nine and out after five — at least eight hours, I hope."
""",
[("paid_8_00", "The clock-in rounds to 08:45 and the clock-out to 17:15, giving 8.5 hours less 30 minutes of lunch."),
 ("paid_7_75", "The clock-in rounds to 08:45 and the clock-out to 17:00, giving 8.25 hours less 30 minutes of lunch."),
 ("paid_7_77", "Actual time from 08:52 to 17:08 less 30 minutes of lunch is 7 hours 46 minutes."),
 ("paid_8_50", "Rounded times of 08:45 and 17:15 give 8.5 hours, and lunch is not deducted.")],
"paid_8_00", 2,
twin=T([("Clock-out: 17:08", "Clock-out: 17:07")], "paid_7_75")),

# ------------------------------------------------------------------ sh12
# why: notice must be at least twice the number of leave days requested. 5 days leave
# starting Mon 12 Oct needs 10 days' notice, counted as calendar days from the request
# day to the first leave day (request day excluded). Request Sat 3 Oct -> 9 days -> short
# -> manager may refuse. Twin: request Fri 2 Oct -> 10 days -> must be considered normally.
C("sh12", "How should the team leader treat this holiday request?",
"""
Wickford Contact Centre — Annual Leave Procedure

L1. Staff must give notice of at least twice as many calendar days as the number of leave days requested.
L2. Notice is counted from the day after the request to the first day of leave, including that first day.
L3. If the notice is sufficient, the request is approved unless the approved-leave cap for that week (4 staff) would be exceeded.
L4. If the notice is short, the team leader may refuse the request for that reason alone.

Leave request LV-1003
Employee: Magnus Olufemi-Grey, adviser, team 6
Leave requested: 5 days, Monday 12 to Friday 16 October 2026
Request submitted: Saturday 3 October 2026
Approved leave already booked for that week: 2 staff
Colleague's note: "He asked more than a week ahead — that's normal notice."
""",
[("approve_request", "From 3 to 12 October is 10 days' notice, twice the 5 leave days, and the weekly cap has room."),
 ("may_refuse_short_notice", "From 4 to 12 October is only 9 days' notice, less than twice the 5 leave days."),
 ("refuse_cap_reached", "The approved-leave cap for that week has already been reached."),
 ("approve_week_notice", "More than a week's notice was given, which is the normal standard.")],
"may_refuse_short_notice", 2,
twin=T([("Request submitted: Saturday 3 October 2026", "Request submitted: Friday 2 October 2026")], "approve_request")),

# ------------------------------------------------------------------ sh13
# why: no more than 6 consecutive working days; mandatory training counts as a working
# day. Thu 1 - Wed 7 Oct with training on Sun 4 Oct -> 7 consecutive -> breach -> rota
# must change. Twin: Sun 4 Oct a rest day -> runs of 3 and 3 -> compliant.
C("sh13", "Does this rota comply with the consecutive-days rule?",
"""
Norcott Water — Operations Rota Rules (treatment works)

R1. No operator may work more than 6 consecutive days.
R2. A "working day" is any day on which the operator does any work for the company, including mandatory training, however short.
R3. A rota that breaches R1 must be changed before publication. Overtime approval cannot override R1.
R4. Voluntary social events are not work.

Draft rota — Deepa Holloway, process operator, 1–7 October 2026
Thursday 1: shift 07:00–15:00
Friday 2: shift 07:00–15:00
Saturday 3: shift 07:00–15:00
Sunday 4: mandatory chlorine-handling refresher, 09:00–13:00
Monday 5: shift 07:00–15:00
Tuesday 6: shift 07:00–15:00
Wednesday 7: shift 07:00–15:00
Thursday 8: rest day
Rota planner's note: "Sunday is only training, not a shift, so she gets a break."
""",
[("change_rota", "Sunday's mandatory training is a working day, so Thursday 1 to Wednesday 7 is 7 consecutive working days."),
 ("publish_rota", "Sunday is a day without any work, so no run of working days is longer than 6."),
 ("publish_training_not_shift", "Training is not a shift, so Sunday breaks the run of working days."),
 ("publish_with_overtime_approval", "The run is 7 days, but overtime approval allows the extra day.")],
"change_rota", 1,
twin=T([("Sunday 4: mandatory chlorine-handling refresher, 09:00–13:00", "Sunday 4: rest day (voluntary team barbecue in the evening)")], "publish_rota")),

# ------------------------------------------------------------------ sh14
# why: company sick pay from day 4 of an absence (days 1-3 unpaid waiting days,
# calendar days). Absences linked if the gap between the end of one and the start of the
# next is 56 days or fewer: no new waiting days. Absence 1 ended 7 Aug; absence 2 began
# 21 Sep -> gap 45 days -> linked -> all 4 days paid (21-24 Sep).
# Twin: absence 1 ended 7 Jul -> gap 76 days -> not linked -> days 1-3 waiting -> 1 paid.
C("sh14", "How many days of company sick pay are due for the September absence?",
"""
Ashwell Foods — Sickness Absence Policy, section 7 (Company sick pay)

7.1 Company sick pay is paid from the fourth day of a period of absence. The first three days are waiting days and are unpaid. Days are calendar days.
7.2 Two absences are linked if the second starts 56 days or fewer after the first ended. Linked absences are one period: no new waiting days apply.
7.3 Company sick pay is limited to 20 paid days in a rolling 12 months.
7.4 A fit note is needed for absences over 7 days.

Absence record — Caius Merriweather, production line
Absence 1: Monday 3 August to Friday 7 August 2026 (5 days), back-pain; 2 days paid under 7.1
Absence 2: Monday 21 September to Thursday 24 September 2026 (4 days), flu
Paid sick days in the last 12 months: 2
Line manager's note: "New absence, new waiting days — pay 1 day."
""",
[("pay_4_days", "Absence 2 started 45 days after absence 1 ended, within 56 days, so it is linked and has no waiting days."),
 ("pay_1_day", "Absence 2 started more than 56 days after absence 1 ended, so the first three days are waiting days."),
 ("pay_0_days", "Only absences over 7 days with a fit note attract company sick pay."),
 ("pay_2_days", "Waiting days are counted in working days, and Monday to Thursday leaves 2 paid days after the first two.")],
"pay_4_days", 2,
twin=T([("Absence 1: Monday 3 August to Friday 7 August 2026", "Absence 1: Friday 3 July to Tuesday 7 July 2026")], "pay_1_day")),

# ------------------------------------------------------------------ sh15
# why: minimum 3 hours per call-out; a call-out starting within 3 h of the START of the
# previous one is merged. C1 01:10-01:50; C2 03:40-05:00 starts 2 h 30 after 01:10 ->
# merged -> 01:10-05:00 = 3 h 50 -> paid 3.83 h x 30 = 115.00.
# Twin: C2 04:20-05:40 -> starts 3 h 10 after -> separate -> 3 h min each -> 6 h -> 180.
C("sh15", "What call-out pay is due for this night?",
"""
Kettering Lane Water Pumping — Standby and Call-Out Agreement

CO1. Call-out work is paid at 30.00 per hour.
CO2. Each call-out is paid for a minimum of 3 hours, or the actual time if longer.
CO3. If a call-out starts within 3 hours of the start of the previous call-out, the two are merged. The merged call-out runs from the start of the first to the end of the second and is paid under CO2 as one call-out.
CO4. The standby allowance is paid separately.

Call-out log — Ruairi Delacroix, standby technician, night of 17–18 September 2026
Call-out 1: 01:10–01:50 (pump 3 trip)
Call-out 2: 03:40–05:00 (same pump, bearing temperature alarm)
Technician's claim: "Two call-outs, three-hour minimum each: 6 hours = 180.00."
""",
[("pay_115_00", "Call-out 2 started within 3 hours of 01:10, so the two merge into 01:10 to 05:00, 3 hours 50 minutes at 30.00."),
 ("pay_180_00", "Call-out 2 started more than 3 hours after 01:10, so each call-out gets its own 3-hour minimum."),
 ("pay_90_00", "Actual time worked is 2 hours, so a single 3-hour minimum applies."),
 ("pay_60_00", "Only the time actually worked is paid: 40 minutes plus 80 minutes.")],
"pay_115_00", 3,
twin=T([("Call-out 2: 03:40–05:00", "Call-out 2: 04:20–05:40")], "pay_180_00")),

# ------------------------------------------------------------------ sh16
# why: probation ends the day before the 6-month anniversary: start 2 Mar -> 1 Sep 2026.
# Absence of MORE than 10 consecutive working days extends probation by its calendar
# length. Absence Mon 11 May - Fri 29 May = 15 working days, 19 calendar days ->
# 1 Sep + 19 = 20 Sep. Twin: absence 11-22 May = 10 working days -> not more than 10 ->
# no extension -> 1 Sep.
C("sh16", "By what date must this employee's probation review be completed?",
"""
Tollbridge Housing — Probation Policy

PR1. Probation lasts six months. It ends at the end of the day before the six-month anniversary of the start date.
PR2. If the employee is absent for more than 10 consecutive working days during probation, probation is extended by the number of calendar days of that absence (first to last day, inclusive).
PR3. The final probation review must be completed on or before the last day of probation (as extended).
PR4. Working days are Monday to Friday. There were no public holidays between 1 May and 31 May 2026 in this policy's calendar.

Employee: Beatrix Nkemelu, income officer
Start date: 2 March 2026
Absence: sick leave, Monday 11 May to Friday 29 May 2026
Manager's calendar note: "Probation review due 2 September."
""",
[("review_by_20_september", "The absence ran 15 working days, over 10, so probation extends by its 19 calendar days from 1 September."),
 ("review_by_1_september", "The absence was not more than 10 working days, so probation ends on 1 September without extension."),
 ("review_by_22_september", "Probation extends by the 15 working days of absence, counted as working days from 1 September."),
 ("review_by_2_september", "Probation ends on the six-month anniversary of the start date.")],
"review_by_20_september", 3,
twin=T([("Monday 11 May to Friday 29 May 2026", "Monday 11 May to Friday 22 May 2026")], "review_by_1_september")),

# ------------------------------------------------------------------ sh17
# why: each hour is paid at the rate for the day in which it is worked. Shift Sat 20:00 -
# Sun 04:00: 4 h Sat (+20% = 3.00/h), 4 h Sun (+50% = 7.50/h). Base 8 x 15 = 120 + 12
# + 30 = 162. Twin rule: all hours at the rate for the day the shift STARTS -> Saturday ->
# 120 + 8 x 3 = 144.
C("sh17", "What should this weekend shift pay?",
"""
Callow Street Distribution — Weekend Enhancement Rules

WE1. Basic rate: 15.00 per hour.
WE2. Saturday enhancement: +20% (3.00 per hour). Sunday enhancement: +50% (7.50 per hour).
WE3. Hours are paid at the rate for the day in which each hour is worked.
WE4. Bank holiday rules are separate and do not apply to this shift.

Shift record — Yusra Deveraux, picker
Shift: Saturday 12 September 2026, 20:00 to Sunday 13 September 2026, 04:00
Breaks: none (paid 15-minute rest breaks only)
Picker's query: "Half of it was on a Sunday. Do I get Sunday rate for all of it?"
Team leader's reply: "No — it started on Saturday, so it's all Saturday rate."
""",
[("pay_162_00", "Four hours on Saturday earn +3.00 each and four hours on Sunday earn +7.50 each, on top of 8 hours at 15.00."),
 ("pay_144_00", "All hours are paid at the rate for the day the shift started, so 8 hours at 15.00 plus 3.00 each."),
 ("pay_180_00", "Most of the shift's night hours fell on Sunday, so all 8 hours earn the Sunday enhancement."),
 ("pay_120_00", "Night shifts across midnight get no weekend enhancement.")],
"pay_162_00", 2,
twin=T([("WE3. Hours are paid at the rate for the day in which each hour is worked.", "WE3. All hours of a shift are paid at the rate for the day on which the shift starts.")], "pay_144_00")),

# ------------------------------------------------------------------ sh18
# why: routing by the engineer's LOCAL day/time (UTC+9). Incident Fri 23:30 UTC = Sat
# 08:30 local -> weekend -> global weekend rota. Twin: Fri 13:30 UTC = Fri 22:30 local ->
# weekday, outside 09:00-18:00 -> APAC night on-call.
C("sh18", "Which team should the APAC queue page for this incident?",
"""
Axle & Ivy Support — APAC Routing Rules (region time: UTC+9)

AR1. All routing decisions use the day and time in the region's time zone, not UTC.
AR2. Monday to Friday, 09:00–18:00 region time: APAC day team.
AR3. Monday to Friday, outside 09:00–18:00 region time: APAC night on-call.
AR4. Saturday and Sunday (any time, region time): global weekend rota.
AR5. P1 incidents also page the incident commander, whatever the team.
AR6. Customer-facing language preferences (Japanese, Korean, English) are handled by the translation desk and do not change routing.
AR7. The on-call handover times published in the wiki are for information only and never override AR1–AR4.

Incident INC-26-10442 (P2, customer: Hinode Freight, Yokomura)
Created (UTC): Friday 25 September 2026, 23:30
Queue bot suggestion: "Friday in UTC → APAC night on-call."
""",
[("global_weekend_rota", "23:30 UTC on Friday is 08:30 on Saturday in region time, so the weekend rota takes it."),
 ("apac_night_on_call", "In region time the incident falls on a weekday outside 09:00–18:00."),
 ("apac_day_team", "08:30 is close to the start of business hours, so the day team takes it."),
 ("apac_night_by_utc", "The incident was created on a Friday in UTC, so the weekday night on-call takes it.")],
"global_weekend_rota", 2,
twin=T([("Created (UTC): Friday 25 September 2026, 23:30", "Created (UTC): Friday 25 September 2026, 13:30")], "apac_night_on_call")),

# ------------------------------------------------------------------ sh19
# why: no more than 12 h of work in any rolling 24 h. Mon 06:00-14:00 (8) + Mon 22:00-Tue
# 02:00 (4) + proposed Tue 04:00-05:00 (1): window Mon 06:00-Tue 06:00 = 13 -> breach ->
# decline. Twin: call-out Tue 06:00-07:00: every 24-h window holds at most 12 (e.g. Mon
# 07:00-Tue 07:00 = 7 + 4 + 1 = 12) -> allowed.
C("sh19", "Can the controller assign this extra call-out to the engineer?",
"""
Sorrel Rail Maintenance — Fatigue Management Standard FM-2

F1. No person may be on duty for more than 12 hours in any 24-hour period. The 24-hour period is rolling: every possible 24-hour window counts, not just calendar days.
F2. Travel to and from site in a company vehicle counts as duty.
F3. A controller who cannot staff a task within F1 must assign another person or defer the task.
F4. Exactly 12 hours in a window is allowed.

Duty record — Priyanka Solberg, signalling engineer
Monday 14 September 2026: 06:00–14:00 (day shift, including travel)
Monday 14 September 22:00 to Tuesday 15 September 02:00: emergency repair (including travel)
Proposed call-out: Tuesday 15 September, 04:00–05:00 (including travel)
Controller's note: "She's done 8 hours Monday and the night job was only 4. Tuesday is a new day."
""",
[("reassign_or_defer", "The window from 06:00 Monday to 06:00 Tuesday would hold 8 + 4 + 1 = 13 hours of duty, over 12."),
 ("assign_call_out", "No 24-hour window would hold more than 12 hours of duty, so the call-out is allowed."),
 ("assign_new_calendar_day", "Tuesday is a new calendar day, so the Monday hours do not count."),
 ("reassign_night_rule", "Nobody may do two duty periods in one night, whatever the hours.")],
"reassign_or_defer", 3,
twin=T([("Proposed call-out: Tuesday 15 September, 04:00–05:00", "Proposed call-out: Tuesday 15 September, 06:00–07:00")], "assign_call_out")),

# ------------------------------------------------------------------ sh20
# why: late = more than 5 minutes after shift start. Rolling 30 days before and including
# 29 Sep: 30 Aug-29 Sep. Clock-ins (09:00 starts): 3 Sep 09:05 (not late), 15 Sep 09:07
# (late), 29 Sep 09:12 (late); 21 Aug 09:20 is outside the window. 2 lates -> record
# only. Twin: 3 Sep 09:06 -> late -> 3 in window -> written warning.
C("sh20", "What action does the attendance policy require after today's clock-in?",
"""
Pennant Insurance Services — Attendance and Punctuality Policy

AP1. A clock-in more than 5 minutes after the rostered start is a late arrival.
AP2. Three late arrivals within any rolling 30-day period (the day of the latest arrival and the 29 days before it) lead to a written warning.
AP3. Fewer than three: the late arrival is recorded only.
AP4. Lateness caused by a documented public transport strike is not counted.

Attendance record — Farida Oyinlola, claims handler (rostered start 09:00)
21 August 2026: clock-in 09:20
3 September 2026: clock-in 09:05
15 September 2026: clock-in 09:07
29 September 2026 (today): clock-in 09:12
Documented transport strikes: none
Team leader's note: "That's four times she's been late. Written warning."
""",
[("record_only", "In the 30 days to 29 September only 15 and 29 September are late arrivals; 09:05 is not more than 5 minutes late."),
 ("written_warning", "Three late arrivals (3, 15 and 29 September) fall within the 30 days to 29 September."),
 ("written_warning_four", "Four late clock-ins appear on the record, which is more than three."),
 ("record_only_strike", "The lateness is treated as transport-related, so it is not counted.")],
"record_only", 2,
twin=T([("3 September 2026: clock-in 09:05", "3 September 2026: clock-in 09:06")], "written_warning")),

# ------------------------------------------------------------------ sh21
# why: TOIL expires at the end of the day three months after the day earned. Earned
# Sun 14 Jun 2026 -> expires end of 14 Sep. Requested for Mon 14 Sep -> valid -> approve.
# Twin: requested for Tue 15 Sep -> lapsed -> decline (no pay-out allowed).
C("sh21", "Should the manager approve this time-off-in-lieu request?",
"""
Tollbridge Housing — Time Off in Lieu (TOIL) Rules

T1. Staff who work approved extra hours earn TOIL hour for hour.
T2. TOIL must be taken on or before the day three months after the day it was earned. After that it lapses.
T3. Lapsed TOIL is not paid out and cannot be carried forward.
T4. TOIL requests are approved if the TOIL is still valid and the team has cover.

Request TOIL-0914
Employee: Gideon Achterberg, repairs surveyor
TOIL earned: 6 hours, Sunday 14 June 2026 (emergency flood response)
TOIL requested for: Monday 14 September 2026 (6 hours)
Team cover that day: confirmed
HR assistant's note: "Three months is about ninety days, and 14 June plus 90 is 12 September — so it's gone."
""",
[("approve_toil", "The TOIL is valid up to and including 14 September, three months after 14 June, and cover is confirmed."),
 ("decline_lapsed", "The requested day is after 14 September, three months after the TOIL was earned, so it has lapsed."),
 ("decline_ninety_days", "Three months is 90 days, which ended on 12 September."),
 ("pay_out_toil", "The TOIL is about to lapse, so it should be paid out instead of taken.")],
"approve_toil", 2,
twin=T([("TOIL requested for: Monday 14 September 2026 (6 hours)", "TOIL requested for: Tuesday 15 September 2026 (6 hours)")], "decline_lapsed")),

# ------------------------------------------------------------------ sh22
# why: double time only for hours worked ON the public holiday date (25 Dec).
# Shift 20:00 24 Dec - 06:00 25 Dec: 4 h on 24 Dec at 20 = 80; 6 h on 25 Dec at 40 =
# 240 -> 320. Twin: shift 16:00 24 Dec - 02:00 25 Dec -> 8 h x 20 = 160 + 2 h x 40 = 80
# -> 240.
C("sh22", "What should the Christmas night shift pay?",
"""
Marlowe Bay Hotel — Seasonal Pay Rules (night reception)

H1. Basic rate: 20.00 per hour.
H2. Hours worked on a public holiday are paid at double time (40.00 per hour). Public holidays run from 00:00 to 24:00 on the holiday date.
H3. 24 December is not a public holiday. 25 and 28 December 2026 are.
H4. Hours on other days are paid at the basic rate, whatever day the shift started.

Shift record — Aurelio Fontaine, night receptionist
Shift: Thursday 24 December 2026, 20:00 to Friday 25 December 2026, 06:00
Breaks: paid, taken at the desk
Receptionist's query: "The whole shift is the Christmas night shift — double time for all 10 hours?"
Duty manager's reply: "It starts on Christmas Eve, which isn't a holiday, so it's all basic."
""",
[("pay_320", "Four hours fall on 24 December at the basic rate and six on 25 December at double time."),
 ("pay_240", "Eight hours fall on 24 December at the basic rate and two on 25 December at double time."),
 ("pay_400", "It is the Christmas night shift, so all 10 hours are at double time."),
 ("pay_200", "The shift started on Christmas Eve, which is not a holiday, so all 10 hours are basic.")],
"pay_320", 2,
twin=T([("Thursday 24 December 2026, 20:00 to Friday 25 December 2026, 06:00", "Thursday 24 December 2026, 16:00 to Friday 25 December 2026, 02:00")], "pay_240")),
]
