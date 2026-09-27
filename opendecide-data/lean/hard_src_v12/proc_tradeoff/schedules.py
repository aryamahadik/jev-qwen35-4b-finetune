"""proc_tradeoff / schedules, windows, rosters and slot choices. Weekdays for
2026 dates were checked with a calendar (22 Sep 2026 = Tuesday, 3 Oct =
Saturday, 12 Oct = Monday, 26 Oct = Monday, 7 Nov = Saturday). All
organisations, people and places are invented."""
from _lib import C, T

ITEMS = [
# ------------------------------------------------------------------ sc01
# why: notice sent Tue 22 Sep. Clear business days before a Saturday window:
# Sat 3 Oct -> Wed 23 Sep..Fri 2 Oct = 23,24,25,28,29,30,1,2 = 8 < 10 -> fail.
# Sat 10 Oct -> 13 business days -> ok. Sat 21 Nov in freeze (15 Nov-5 Jan).
# Wed 7 Oct not a window. Earliest compliant = 10 Oct.
# Twin: notice 5 business days -> 8 >= 5 -> 3 Oct.
C("sc01", "Which maintenance window should the database upgrade be booked into?",
"""
Change request CHG-40718 — Order database upgrade (v12 to v14)
Raised: Tuesday 22 September 2026. Customer notice sent the same day.
Duration: 3 hours including rollback test.

Change Management Standard
CM-1. Production maintenance may only take place in a standard window: Saturdays 01:00-05:00.
CM-2. Change freeze: no production changes from 15 November to 5 January inclusive.
CM-3. Book the earliest window that satisfies every rule and contract.

Customer contract (Kesterfield Retail, Schedule 4, para 2)
Planned maintenance requires at least 10 business days' notice. Business days are Monday to Friday, counted from the day after notice is given up to the last business day before the maintenance. There are no public holidays before December.

Candidate windows proposed by the DBA team
- Saturday 3 October, 01:00-04:00
- Wednesday 7 October, 01:00-04:00 (DBA team's preference: "quieter than weekends")
- Saturday 10 October, 01:00-04:00
- Saturday 21 November, 01:00-04:00

Other note: the reporting replica will be rebuilt separately next month.
""",
[("sat_3_oct", "3 October is the earliest standard window outside the freeze that gives the required business days of notice."),
 ("wed_7_oct", "Wednesday nights are quieter than weekends, which makes 7 October the lowest-risk slot."),
 ("sat_10_oct", "3 October gives only 8 business days' notice, so 10 October is the earliest window meeting every rule."),
 ("sat_21_nov", "21 November allows the most notice and testing time before the upgrade.")],
"sat_10_oct", 2,
twin=T([("Planned maintenance requires at least 10 business days' notice.", "Planned maintenance requires at least 5 business days' notice.")], "sat_3_oct")),

# ------------------------------------------------------------------ sc02
# why: shift Thu 1 Oct 06:00-14:00, forklift licence needed. Dalia: Wed 14:00-22:00 ->
# 8 h rest < 11 -> out. Tomas: worked Sat 26-Wed 30 (5 days) -> Thu = 6th -> out.
# Bram: licence expired 31 Aug -> out. Ines: last shift Mon 28 Sep 22:00, rest ok,
# licence valid -> only eligible -> Ines.
# Twin: Bram licence valid to 31 Aug 2027 -> eligible, 6 h OT < Ines 12 h -> Bram.
C("sc02", "Who should be asked to cover the open Thursday shift?",
"""
Rushby Distribution Centre — Shift cover request
Open shift: Thursday 1 October 2026, 06:00-14:00, goods-in (forklift work).

Working Time and Safety Rules
W1. At least 11 hours' rest between the end of one shift and the start of the next.
W2. No more than 5 consecutive working days.
W3. Forklift shifts need a forklift licence valid on the shift date.
W4. Offer the shift to the eligible colleague with the fewest overtime hours so far this month; for this shift, "this month" means September.

Candidates
| Colleague | Recent shifts | Overtime in September | Forklift licence |
| Dalia Voss | Wed 30 Sep 14:00-22:00 | 4 h | valid to 2027 |
| Tomas Reyk | Sat 26 Sep to Wed 30 Sep, 06:00-14:00 daily | 10 h | valid to 2028 |
| Ines Harlan | Mon 28 Sep 14:00-22:00, then off | 12 h | valid to 2027 |
| Bram Oduya | off since Sun 27 Sep | 6 h | expired 31 August 2026 |

Supervisor's note: "Dalia says she's happy to come straight back in; she's done it before."
""",
[("dalia_voss", "Dalia has the fewest overtime hours, and she has agreed to the short turnaround."),
 ("tomas_reyk", "Tomas knows the goods-in area best and Thursday would only be his fifth day this week."),
 ("ines_harlan", "Ines meets the rest, consecutive-day and licence rules and has the fewest overtime hours of those who do."),
 ("bram_oduya", "Bram meets the rest, consecutive-day and licence rules and has the fewest overtime hours among eligible colleagues.")],
"ines_harlan", 2,
twin=T([("| 6 h | expired 31 August 2026 |", "| 6 h | valid to 31 August 2027 |")], "bram_oduya")),

# ------------------------------------------------------------------ sc03
# why: start Mon 21 Sep. A: 14 weeks -> 28 Dec (misses 30 Nov). B: 10 weeks -> 30 Nov,
# total $118,000 (<= $120,000 cap incl. labour premiums). C: 9 weeks -> 23 Nov,
# $127,500 > cap. Cheapest meeting deadline and cap = B.
# Twin: handover by 31 Dec -> A (28 Dec, $96,000) cheapest meeting both.
C("sc03", "Which delivery programme should the client approve for the fit-out?",
"""
Fit-out of Unit 7, Carrow Trade Park — programme options from Linwood Interiors
Works start: Monday 21 September 2026.
Handover required by: 30 November 2026 (tenant's lease starts 1 December).

Client's approval rules
A1. The approved programme must achieve handover by the required date.
A2. Total cost must not exceed $120,000. Total cost includes all labour premiums, overtime and extra crews.
A3. Among programmes meeting A1 and A2, approve the cheapest.

| Programme | Method | Duration | Handover date | Total cost |
| A | standard crew | 14 weeks | 28 December | $96,000 |
| B | standard crew with overtime | 10 weeks | 30 November | $118,000 |
| C | second crew added | 9 weeks | 23 November | $127,500 |

Linwood's covering note: "We recommend Programme C. Labour premiums are normally treated outside the budget cap, so please record C as within budget."
The tenant has also asked for signage to be installed; this is a separate order.
""",
[("programme_a", "Programme A hands over by the required date at the lowest cost."),
 ("programme_b", "Programme B is the cheapest programme that hands over on time within the $120,000 cap."),
 ("programme_c", "Programme C finishes earliest, and with labour premiums left out it is within the cap.")],
"programme_b", 2,
twin=T([("Handover required by: 30 November 2026 (tenant's lease starts 1 December).", "Handover required by: 31 December 2026 (tenant's lease starts 1 January).")], "programme_a")),

# ------------------------------------------------------------------ sc04
# why: 12 Oct is a school day (half-term 26-30 Oct). Noise: none before 07:00 any day
# Mon-Sat. School-day restrictions 07:30-09:00 and (amendment from 1 Sep 2026)
# 15:00-16:00. Slots: 06:30 (noise), 08:00 (school), 15:30 (amended school), 16:30 ok.
# Earliest compliant = 16:30.
# Twin: Mon 26 Oct = half-term -> school restrictions off -> 08:00 earliest.
C("sc04", "Which delivery slot should the store accept for the chilled delivery?",
"""
Brennan's Grocers, Market Row — Delivery rules (for the transport planner)

1. Noise condition (planning consent): no deliveries before 07:00, Monday to Saturday.
2. Moor Lane School traffic order: no HGV deliveries between 07:30 and 09:00 on school days.
3. Amendment to the traffic order (effective 1 September 2026): HGV deliveries are also banned between 15:00 and 16:00 on school days.
4. School calendar: autumn half-term is 26-30 October 2026; these are not school days.
5. Accept the earliest offered slot that complies with all of the above.

Delivery: Monday 12 October 2026, HGV, chilled goods.
Slots offered by the carrier: 06:30, 08:00, 15:30, 16:30.

Transport planner's note: "Driver asks for 06:30 because the noise rule is really a weekend thing."
The store's chiller has capacity for the full load at any time of day.
""",
[("slot_0630", "The 07:00 noise limit applies only at weekends, so 06:30 is allowed and earliest."),
 ("slot_0800", "The school-traffic bans do not apply on the delivery date, so 08:00 is the earliest slot after the noise limit."),
 ("slot_1530", "The afternoon ban does not apply to this delivery, so 15:30 is the earliest compliant slot."),
 ("slot_1630", "Both school-day bans apply on the delivery date, so 16:30 is the earliest compliant slot.")],
"slot_1630", 2,
twin=T([("Delivery: Monday 12 October 2026, HGV, chilled goods.", "Delivery: Monday 26 October 2026, HGV, chilled goods.")], "slot_0800")),

# ------------------------------------------------------------------ sc05
# why: major release: CAB Thu 24 Sep, then >= 5 days -> from 29 Sep. Quarter-end
# freeze: last 3 business days of Q3 (Mon 28, Tue 29, Wed 30 Sep) + first 2 of Q4
# (Thu 1, Fri 2 Oct). 29, 30 Sep frozen -> earliest listed allowed = Tue 6 Oct.
# Twin: minor release -> no CAB, freeze-exempt -> Tue 29 Sep (not a Friday).
C("sc05", "On which date should the release be deployed?",
"""
Release Management Policy (Orrin Payments), extract
RM-1. Major releases need approval at the weekly Change Advisory Board (CAB), held on Thursdays. Deployment may take place no earlier than 5 calendar days after CAB approval.
RM-2. No production deployments on Fridays.
RM-3. Quarter-end freeze: no releases on the last 3 business days of a calendar quarter or the first 2 business days of the next quarter.
RM-4. Minor releases (patch level) need no CAB approval and are exempt from RM-3, but RM-2 still applies.
RM-5. Deploy on the earliest candidate date the rules allow.

Release record REL-2026-118
Release class: major (v5.0)
Today: Monday 21 September 2026. Next CAB: Thursday 24 September (approval expected).
Candidate dates: Tuesday 29 September, Wednesday 30 September, Tuesday 6 October, Wednesday 7 October.

Product owner's note: "Sales want it before quarter end for the Deltaview demo."
""",
[("tue_29_sep", "As a patch-level release it needs no CAB and is exempt from the freeze, so 29 September, the earliest date, is allowed."),
 ("wed_30_sep", "The quarter-end freeze covers only the final business day, so 30 September is available."),
 ("tue_6_oct", "The quarter-end freeze blocks 29 and 30 September, so 6 October is the earliest allowed date."),
 ("wed_7_oct", "After a freeze, releases must wait a full business week, so 7 October is the first allowed date.")],
"tue_6_oct", 2,
twin=T([("Release class: major (v5.0)", "Release class: minor (v4.9.3)")], "tue_29_sep")),

# ------------------------------------------------------------------ sc06
# why: panel needs >= 1 member from outside the hiring department (Engineering) and
# >= 1 currently trained interviewer; candidate available Tue-Thu only. Training:
# Hana valid, Olek valid, Sanjay valid, Ruth not trained.
# Tue: Hana+Olek both Eng -> fail. Wed: Hana (Eng, trained) + Ruth (Finance) -> ok.
# Thu: Olek (Eng, trained) + Sanjay (Mkt) -> ok. Fri: candidate unavailable.
# Earliest = Wed. Twin: Hana's training lapsed -> Wed has no trained member -> Thu.
C("sc06", "Which interview slot should be confirmed with the candidate?",
"""
Recruitment Standard (Tamber Robotics), section 5: interview panels
5.1 Every panel must include at least one member from outside the hiring department.
5.2 Every panel must include at least one interviewer whose structured-interview training is current.
5.3 Book the earliest slot that meets 5.1 and 5.2 and suits the candidate.

Vacancy: Senior Firmware Engineer (hiring department: Engineering).
Candidate availability: Tuesday to Thursday next week only.

Training register
- Hana Brightwater (Engineering): current, valid until March 2027.
- Olek Varga (Engineering): current, valid until January 2027.
- Ruth Achebe (Finance): never trained.
- Sanjay Mehrotra (Marketing): current, valid until May 2027.

Available panels
| Slot | Panel |
| Tuesday 10:00 | Hana Brightwater, Olek Varga |
| Wednesday 14:00 | Hana Brightwater, Ruth Achebe |
| Thursday 09:00 | Olek Varga, Sanjay Mehrotra |
| Friday 11:00 | Sanjay Mehrotra, Ruth Achebe |

Hiring manager: "Tuesday is ideal; Hana and Olek know the role better than anyone."
""",
[("tuesday_1000", "Tuesday is earliest and both panel members are trained, which is what the standard requires."),
 ("wednesday_1400", "Wednesday is the earliest slot whose panel has an outside member and a currently trained interviewer."),
 ("thursday_0900", "Thursday is the earliest slot that has both an outside member and a currently trained interviewer on the panel."),
 ("friday_1100", "Friday's panel is entirely from outside Engineering, which gives the fairest interview.")],
"wednesday_1400", 2,
twin=T([("- Hana Brightwater (Engineering): current, valid until March 2027.", "- Hana Brightwater (Engineering): lapsed in June 2026, refresher not yet booked.")], "thursday_0900")),

# ------------------------------------------------------------------ sc07
# why: T2 (reserve >= $500k at all times) takes precedence over T1 (take discounts).
# Day 10 payment = 150,000 * 0.98 = 147,000; cash 620,000 - 147,000 = 473,000 < 500k
# -> breach. Day 30: receipt of 400k on day 20 -> 1,020,000 - 150,000 = 870,000 ok.
# Never pay after due date (day 45 out). -> pay on day 30.
# Twin: cash 680,000 -> 680 - 147 = 533k >= 500k -> take discount on day 10.
C("sc07", "When should the Halvard Steel invoice be paid?",
"""
Treasury Policy (Corrin Fabrications), payment timing
T1. Take early-payment discounts whenever the annualised return exceeds 12%. (Terms of 2/10 net 30 give about 36.7%.)
T2. The operating account balance must never fall below $500,000. T2 takes precedence over T1.
T3. Invoices must not be paid after their due date.

Invoice HS-20931, Halvard Steel
Amount: $150,000. Invoice date: 1 October 2026. Terms: 2/10 net 30 (2% discount if paid by day 10; otherwise the full amount by day 30).

Cash position
Operating account balance today (1 October): $620,000.
Expected receipts: $400,000 from Pellman Construction on day 20.
No other payments are scheduled before day 30.

AP note: "Halvard accepted payment at 45 days during the 2024 slowdown, so we could stretch again."
""",
[("pay_day_10", "The discount beats the 12% hurdle, and paying on day 10 keeps the account above the $500,000 minimum."),
 ("pay_day_30", "Paying on day 10 would take the balance below the $500,000 minimum, so the invoice is paid in full on day 30."),
 ("pay_day_45", "Halvard has accepted 45-day payment before, and paying later keeps the most cash in hand, which protects the $500,000 minimum best.")],
"pay_day_30", 3,
twin=T([("Operating account balance today (1 October): $620,000.", "Operating account balance today (1 October): $680,000.")], "pay_day_10")),

# ------------------------------------------------------------------ sc08
# why: finance team of 14 must attend one session together before 31 Oct deadline,
# outside month-end blackout (last 2 business days + first 3 business days of month:
# Thu 1, Fri 2, Mon 5 Oct). S1 1 Oct blackout; S2 14 Oct capacity 12 < 14; S3 20 Oct
# capacity 16 ok; S4 3 Nov after deadline. -> S3.
# Twin: team of 12 -> S2 fits and is earlier -> S2.
C("sc08", "Which training session should the finance team be booked on?",
"""
Compliance Training Notice — Annual Anti-Money-Laundering refresher
All staff must complete the 2026 refresher by 31 October 2026.

Booking rules for teams
B1. A team attends together in a single session.
B2. Finance staff may not attend training during the month-end blackout: the last 2 business days of a month and the first 3 business days of the next month.
B3. Book the earliest session that satisfies B1 and B2, has enough seats and falls before the deadline.

Team: Group Finance (14 people). Manager: Leopold Asante.

Sessions available
| Session | Date | Seats left |
| S1 | Thursday 1 October | 20 |
| S2 | Wednesday 14 October | 12 |
| S3 | Tuesday 20 October | 16 |
| S4 | Tuesday 3 November | 30 |

Trainer's note: "S2 could squeeze in a couple more if people don't mind standing."
Online self-study is available only for staff on long-term leave.
""",
[("session_s1", "S1 is the earliest session with enough seats for the whole team."),
 ("session_s2", "S2 is the earliest session outside the blackout with enough seats for the team before the deadline."),
 ("session_s3", "S3 is the first session after the blackout that seats the whole team before the deadline."),
 ("session_s4", "S4 has the most seats, and the deadline can slip for a team booking made in good time.")],
"session_s3", 2,
twin=T([("Team: Group Finance (14 people).", "Team: Group Finance (12 people).")], "session_s2")),

# ------------------------------------------------------------------ sc09
# why: weekend 24-25 Oct. Max 2 primary weekends per calendar month: Asha has 2 -> out.
# First 60 days: Ben joined 10 Sep -> 44 days on 24 Oct -> out. Chioma on leave 23-26 Oct
# -> out (0 weekends). Dmitri eligible (1 weekend). -> Dmitri.
# Twin: Ben joined 10 Aug -> 75 days -> eligible with 0 weekends < Dmitri 1 -> Ben.
C("sc09", "Who should be primary on-call for the weekend of 24-25 October?",
"""
Platform Team — On-call rota rules (v3)
R1. Nobody may be primary on-call for more than 2 weekends in one calendar month.
R2. Engineers in their first 60 days after joining cannot be primary; count days from the joining date to the Saturday of the weekend.
R3. Engineers on approved leave on either day of the weekend cannot be primary.
R4. Among eligible engineers, choose the one with the fewest primary weekends so far this month; break ties alphabetically.

October so far
| Engineer | Joined | Primary weekends in October | Leave |
| Asha Pemberton | 2021 | 2 (3-4 Oct, 10-11 Oct) | none |
| Ben Okafor | 10 September 2026 | 0 | none |
| Chioma Lund | 2023 | 0 | approved 23-26 Oct |
| Dmitri Salo | 2019 | 1 (17-18 Oct) | none |

Team lead's comment: "Asha knows the payment services inside out; I'd feel safest with her."
""",
[("asha_pemberton", "Asha has the deepest knowledge of the services, and the cap counts only weekends she volunteered for."),
 ("ben_okafor", "Ben has passed his first 60 days by 24 October and has the fewest primary weekends among eligible engineers."),
 ("chioma_lund", "Chioma has no primary weekends yet this month, and approved leave can be moved to cover on-call."),
 ("dmitri_salo", "Dmitri is the eligible engineer with the fewest primary weekends this month.")],
"dmitri_salo", 2,
twin=T([("| Ben Okafor | 10 September 2026 | 0 | none |", "| Ben Okafor | 10 August 2026 | 0 | none |")], "ben_okafor")),

# ------------------------------------------------------------------ sc10
# why: notice sent Thu 1 Oct; 14 clear days exclude the notice day and meeting day.
# 14 Oct: clear days 2-13 = 12 -> fail. 16 Oct: 2-15 = 14 ok but chair absent and the
# budget meeting must be chaired by the chair (Art. 9 overrides Art. 8 vice-chair).
# 19 Oct: 4 directors incl. chair (quorum 4) -> ok. Earliest valid = 19 Oct.
# Twin: chair available 16 Oct -> 16 Oct.
C("sc10", "Which date should be fixed for the budget board meeting?",
"""
Kilnworth Community Energy Ltd — Articles of Association (extract)
Art. 6: Board meetings require at least 14 clear days' written notice. "Clear days" excludes the day notice is given and the day of the meeting.
Art. 7: The quorum is 4 of the 7 directors.
Art. 8: In the chair's absence, the vice-chair presides.
Art. 9: Despite Art. 8, the meeting that approves the annual budget must be chaired by the chair.

Company secretary's note: notice of the 2027 budget meeting will be sent on Thursday 1 October 2026. Choose the earliest date that satisfies the Articles.

Director availability poll
| Date | Directors available | Chair (Imogen Treharne) |
| Wednesday 14 October | 6 | available |
| Friday 16 October | 5 | travelling, not available |
| Monday 19 October | 4 | available |
| Thursday 22 October | 6 | available |

Vice-chair's email: "Happy to chair on the 16th if Imogen can't make it."
""",
[("wed_14_oct", "Notice on 1 October gives the required 14 days by 14 October, and six directors can attend."),
 ("fri_16_oct", "16 October is the earliest date with 14 clear days' notice, a quorum and the chair present."),
 ("mon_19_oct", "The chair cannot attend on 16 October, so 19 October is the earliest date meeting the notice, quorum and chair rules."),
 ("thu_22_oct", "22 October has the most directors available, which gives the most secure quorum for approving a budget of this size.")],
"mon_19_oct", 2,
twin=T([("| Friday 16 October | 5 | travelling, not available |", "| Friday 16 October | 5 | available |")], "fri_16_oct")),

# ------------------------------------------------------------------ sc11
# why: gusts must be < 20 mph (amended from 25 on 3 Aug); footpath closure permit
# needed (lift over footpath); operator needed. Mon gust 22 -> fail. Tue permit
# refused -> fail. Wed 17 mph, permit, operator -> ok. Thu no operator. -> Wed.
# Twin: Tue permit granted -> Tue (18 mph) earliest.
C("sc11", "On which day should the rooftop plant lift be scheduled?",
"""
Lift Plan LP-22 — Rooftop chiller replacement, 14 Carden Street
The crane will swing the chiller over the public footpath on Carden Street.

Site rules
S1. Lifts may proceed only if the forecast maximum gust for the lift period is below 20 mph. (Amended on 3 August 2026 after the Kirkby Yard incident; the previous limit was 25 mph.)
S2. Any lift over a public footpath needs a footpath closure permit from the council for that day.
S3. The appointed crane operator must be available.
S4. Schedule the lift on the earliest day that meets S1-S3.

Planning table (week of 12 October)
| Day | Forecast max gust | Footpath permit | Crane operator |
| Monday | 22 mph | granted | available |
| Tuesday | 18 mph | refused (clashes with market day) | available |
| Wednesday | 17 mph | granted | available |
| Thursday | 12 mph | granted | on leave |

Crane hire company: "Our cranes are rated to 30 mph, so Monday is no problem for us."
""",
[("monday", "Monday's 22 mph gusts are within the crane's rating and the earlier 25 mph limit, so the lift can go ahead."),
 ("tuesday", "Tuesday is the first day with gusts under 20 mph, a footpath permit and an operator available."),
 ("wednesday", "Wednesday is the first day meeting the gust limit, the permit rule and operator availability."),
 ("thursday", "Thursday has the calmest forecast, and a relief operator can be found.")],
"wednesday", 1,
twin=T([("| Tuesday | 18 mph | refused (clashes with market day) | available |", "| Tuesday | 18 mph | granted | available |")], "tuesday")),

# ------------------------------------------------------------------ sc12
# why: one slot left (max 2 of 6 off; Ravi approved). Priority by submission date,
# but anyone off Christmas week last year goes to the back. Lars (12 Jul) was off in
# 2025 -> back. Next: Keira (3 Aug) before Mei (20 Aug) -> Keira.
# Twin: Keira was off in 2025 instead -> Lars (earliest, not off) -> Lars.
C("sc12", "Whose request for the Christmas week should be approved?",
"""
Customer Care Team B — Annual leave rules (Christmas period)
L1. No more than 2 of the team's 6 members may be on leave on any working day.
L2. Requests are ranked by submission date, earliest first.
L3. Rotation: anyone who had leave during the Christmas week last year moves to the back of the queue, behind all other requesters.
L4. Remaining unused leave is used only to break ties on the same submission date.

Week of 21-25 December 2026
Already approved: Ravi Mendes.
Pending requests for the full week:
- Lars Nygaard, submitted 12 July 2026, 9 days unused.
- Keira Doyle, submitted 3 August 2026, 6 days unused.
- Mei Tanaka, submitted 20 August 2026, 14 days unused.

Christmas 2025 rota: Lars was off 22-26 Dec. Mei and Keira worked.
Team lead's note: "Mei has loads of leave left; she really should take some."
""",
[("approve_lars", "Lars submitted first and was not off last Christmas, so he is at the front of the queue."),
 ("approve_keira", "Keira is the earliest requester who was not on leave last Christmas week."),
 ("approve_mei", "Mei has the most unused leave, and unused leave decides between requests."),
 ("approve_two_more", "The limit is raised to three people in December, so two more requests can be approved.")],
"approve_keira", 1,
twin=T([("Christmas 2025 rota: Lars was off 22-26 Dec. Mei and Keira worked.", "Christmas 2025 rota: Keira was off 22-26 Dec. Mei and Lars worked.")], "approve_lars")),

# ------------------------------------------------------------------ sc13
# why: last A-check 1 Jun 2026; limit 120 days -> 29 Sep 2026 (Jun 1 + 29 = Jun 30,
# +31 Jul, +31 Aug, +29 Sep = 120). Hours: 512 at 06:00 on 26 Sep, 8 h/day -> 88 h
# left = 11 flying days (26 Sep-6 Oct) -> 600 reached end of 6 Oct. Due = earlier =
# 29 Sep. Last slot on or before due = 28 Sep.
# Twin: last check 20 Jun -> 120 days = 18 Oct; hours limit end of 6 Oct first ->
# 6 Oct 06:00 slot (592 h) is last slot within.
C("sc13", "Which hangar slot should be booked for the A-check?",
"""
Maintenance Control — Tail VH-QRL (Tessel 320)
Maintenance Programme, task A-CHK: an A-check is due every 600 flight hours or 120 days, whichever comes first, counted from the last A-check.
Planning rule MC-4: book the last available hangar slot that falls on or before the due point, so the full interval is used. All slots start at 06:00, before the day's flying.

Status
Last A-check completed: 1 June 2026.
Flight hours since last A-check, at 06:00 on 26 September 2026: 512.
Planned utilisation: 8 flight hours per day, every day.

Hangar slots offered (Brisk Aero, Vellan base): 28 September, 2 October, 6 October.

Scheduler's note: "Commercial would love the 6th; the aircraft is booked for the Lakeside charter on the 1st and 2nd."
Cabin interior refresh (task C-INT) is not due until 2027.
""",
[("slot_28_sep", "The 120-day limit comes first, on 29 September, so 28 September is the last slot inside the interval."),
 ("slot_2_oct", "120 days after 1 June is 2 October, making 2 October the last slot inside the interval, and the hour limit is not reached until later."),
 ("slot_6_oct", "The hour limit comes before the day limit, so 6 October is the last slot inside the interval.")],
"slot_28_sep", 3,
twin=T([("Last A-check completed: 1 June 2026.", "Last A-check completed: 20 June 2026.")], "slot_6_oct")),

# ------------------------------------------------------------------ sc14
# why: internal score 9.1 -> Severity 1 (>= 9.0) -> patch within 72 h of vendor fix
# (Mon 21 Sep 09:00 -> by Thu 24 Sep 09:00). Monthly window Sat 3 Oct too late ->
# emergency change. Vendor label "High" irrelevant (policy uses internal score).
# Twin: score 8.6 -> Severity 2 -> within 14 days (by 5 Oct) -> 3 Oct window meets;
# emergency only when no window meets deadline -> monthly window.
C("sc14", "How should the file-transfer server vulnerability be patched?",
"""
Security ticket SEC-3391 — Vulnerability in Ferrox MFT server
Vendor fix released: Monday 21 September 2026, 09:00. Vendor advisory severity label: "High".
Internal risk score (our scoring model, exposure-adjusted): 9.1.

Vulnerability Management Standard
V1. Severity is set by the internal risk score, not by vendor labels: 9.0 or above = Severity 1; 7.0-8.9 = Severity 2.
V2. Severity 1: patch within 72 hours of the vendor fix. Severity 2: patch within 14 days of the vendor fix.
V3. Patches are applied in the next monthly maintenance window unless that would miss the V2 deadline, in which case an emergency change is raised.
Next monthly window: Saturday 3 October 2026.

Options
- Emergency change: patch Tuesday 22 September, 23:00.
- Monthly window: Saturday 3 October.
- Wait for vendor service pack SP4 (planned November), which bundles this fix.

Comment pasted from a vendor forum: "Customers can safely defer until SP4."
""",
[("emergency_patch", "At Severity 1 the 72-hour deadline ends before the monthly window, so an emergency change is needed."),
 ("monthly_window", "At Severity 2 the fix is due within 14 days, which the 3 October window meets without an emergency change."),
 ("wait_for_sp4", "The vendor community says deferral is safe, and bundling the fix into SP4 reduces change risk.")],
"emergency_patch", 2,
twin=T([("Internal risk score (our scoring model, exposure-adjusted): 9.1.", "Internal risk score (our scoring model, exposure-adjusted): 8.6.")], "monthly_window")),

# ------------------------------------------------------------------ sc15
# why: late opening to 23:30 needs 2 keyholders at close; under-18s not after 22:00.
# X: 1 keyholder (Ana) and Joel (17) to 23:00 -> fail. Y: Ana + Kofi keyholders,
# Joel to 21:30 -> ok. Z: only Kofi is a keyholder -> fail. -> Y.
# Twin: Kofi not yet a keyholder -> no plan has 2 keyholders -> escalate.
C("sc15", "Which staffing plan should be used for the late-night opening?",
"""
Fenmore Books, Harbour Street — Late opening, Thursday 10 December, 16:00-23:30

Store operating rules
O1. At closing time at least 2 keyholders must be on site.
O2. Staff under 18 may not work after 22:00.
O3. If no plan meets O1 and O2, the store manager must ask the area manager to provide cover.

Staff
- Ana Ruiz — keyholder.
- Kofi Asante — keyholder since June 2026.
- Joel Mbeki — age 17.
- Ruth Kaplan — not a keyholder.
- Sam Idris — not a keyholder.

Proposed plans
- Plan X: Ana 15:30-23:45; Joel 16:00-23:00; Ruth 16:00-23:45.
- Plan Y: Ana 15:30-23:45; Kofi 16:00-23:45; Joel 16:00-21:30.
- Plan Z: Kofi 16:00-23:45; Ruth 16:00-23:45; Sam 16:00-23:45.

Deputy manager: "Plan Z gives us the most people at close, which feels safest."
""",
[("plan_x", "Plan X has a keyholder at close, and a 17-year-old may work until 23:00 on late-opening nights."),
 ("plan_y", "Plan Y has two keyholders at close and ends the under-18's shift before 22:00."),
 ("plan_z", "Plan Z has three staff at close, which more than meets the two-person rule."),
 ("ask_area_manager", "No plan has two keyholders at close, so the area manager must be asked for cover.")],
"plan_y", 1,
twin=T([("- Kofi Asante — keyholder since June 2026.", "- Kofi Asante — keyholder training booked for January 2027.")], "ask_area_manager")),

# ------------------------------------------------------------------ sc16
# why: access from 1 Nov; move must finish >= 10 days before lease end 30 Nov (by
# 20 Nov); payroll freeze 18th-22nd bars 21-22 Nov; removal firm booked 7-8 Nov.
# Weekends: 7-8 (firm unavailable), 14-15 ok, 21-22 (freeze + too late), 28-29 (too
# late). -> 14-15 Nov. Twin: firm available 7-8 Nov -> 7-8 Nov earliest.
C("sc16", "Which weekend should the office move take place?",
"""
Office Relocation Plan — Pettigrew & Lowe Accountants
Old office lease ends: Monday 30 November 2026. New office keys available: Sunday 1 November 2026.

Move rules (agreed by the partners)
M1. The move and IT cutover need one full weekend (Saturday-Sunday).
M2. The move must be completed at least 10 days before the old lease ends, to leave time for snagging and the landlord's inspection.
M3. No IT cutover that affects the finance systems may take place during the payroll freeze, which runs from the 18th to the 22nd of every month. This move includes the finance systems.
M4. Pick the earliest weekend that satisfies M1-M3 and the removal firm's availability.

Removal firm (Castell Removals) availability
- 7-8 November: already booked by another client.
- 14-15 November: available.
- 21-22 November: available.
- 28-29 November: available.

Office manager's note: "The payroll freeze is for the payroll clerks, surely? We could do 21-22."
""",
[("weekend_7_8_nov", "7-8 November is the earliest weekend after the keys that the removal firm can do, outside the payroll freeze."),
 ("weekend_14_15_nov", "The removal firm cannot do 7-8 November, so 14-15 November is the earliest workable weekend."),
 ("weekend_21_22_nov", "The payroll freeze only restricts the payroll clerks, so 21-22 November is fine."),
 ("weekend_28_29_nov", "Moving on the final weekend gets the most use from the old lease.")],
"weekend_14_15_nov", 2,
twin=T([("- 7-8 November: already booked by another client.", "- 7-8 November: available.")], "weekend_7_8_nov")),

# ------------------------------------------------------------------ sc17
# why: embargo on high streets 20 Nov-4 Jan (amended start, previously 1 Dec), day
# and night. Carrow Street classified high street -> 23-25 Nov and 28-30 Dec blocked
# -> 7-9 Jan. Twin: local residential street -> no embargo -> earliest 23-25 Nov.
C("sc17", "Which three-night slot should the resurfacing crew book?",
"""
Kelworth Borough Highways — Street Works Permit Scheme (extract)
SW-4. Festive embargo: no planned works on streets classified as high streets from 20 November to 4 January inclusive. The embargo applies day and night. (Amended in 2025; the embargo previously started on 1 December.)
SW-6. Resurfacing needs three consecutive nights.
SW-9. Book the earliest slot allowed.

Scheme: resurfacing of Carrow Street between Mill Lane and the station.
Street classification (Network Register): high street (Schedule 2).

Slots offered by the contractor
- nights of 23, 24 and 25 November 2026
- nights of 28, 29 and 30 December 2026
- nights of 7, 8 and 9 January 2027

Contractor's note: "We work 20:00-05:00 when the shops are shut, so the embargo shouldn't matter."
Bus diversion: Route 14 will be diverted via Mill Lane on work nights.
""",
[("nights_23_nov", "The embargo does not cover this street, so the earliest offered slot is allowed."),
 ("nights_28_dec", "The embargo protects Christmas shopping and lifts after Christmas Day, so late December is open for night works on any street."),
 ("nights_7_jan", "Carrow Street is a high street, so the embargo from 20 November to 4 January rules out the earlier slots.")],
"nights_7_jan", 1,
twin=T([("Street classification (Network Register): high street (Schedule 2).", "Street classification (Network Register): local residential street.")], "nights_23_nov")),

# ------------------------------------------------------------------ sc18
# why: logged 10:00, arrive by 14:00; Class G licence for all gas work.
# Ola free 11:30 + 3 h = 14:30 fail. Pim free 12:00 + 1.5 h = 13:30 ok (travel 1.5).
# Quinn unlicensed. Rhea 10:00 + 2 h = 12:00 ok (travel 2). Shortest travel among
# licensed & in SLA -> Pim. Twin: Pim free 12:45 -> 14:15 fail -> Rhea only.
C("sc18", "Which technician should be dispatched to the boiler fault?",
"""
Dispatch board — job J-77104, gas boiler not firing, Brook Terrace care office
Logged: 10:00. Contract SLA: engineer on site within 4 hours of logging.

Dispatch rules
D1. Any work on gas appliances, repair or installation, needs a Class G licence.
D2. Only technicians who can arrive within the SLA may be assigned.
D3. Among technicians meeting D1 and D2, assign the one with the shortest travel time (mileage costs).

Technicians
| Name | Class G | Free from | Travel time to site |
| Ola Brandt | yes | 11:30 | 3 h 00 |
| Pim Castell | yes | 12:00 | 1 h 30 |
| Quinn Adair | no | now (10:00) | 1 h 00 |
| Rhea Solberg | yes | now (10:00) | 2 h 00 |

Controller's note: "Quinn is closest and free now; it's only a repair, not an install."
""",
[("ola_brandt", "Ola has the most experience with this boiler model and can be there the same afternoon."),
 ("pim_castell", "Pim is licensed, arrives within the SLA, and has the shortest travel time of those who do."),
 ("quinn_adair", "Quinn arrives first, and the licence is only needed for installations."),
 ("rhea_solberg", "Rhea is the only licensed technician who can arrive within the 4-hour SLA.")],
"pim_castell", 2,
twin=T([("| Pim Castell | yes | 12:00 | 1 h 30 |", "| Pim Castell | yes | 12:45 | 1 h 30 |")], "rhea_solberg")),

# ------------------------------------------------------------------ sc19
# why: cut-off Tue 22 Sep 12:00 for payday Fri 25 Sep; claim approved 13:15 -> missed.
# Time limit: submitted within 3 months of overtime (worked 30 Jun-2 Jul, submitted
# 18 Sep -> within). -> next run. Employee's note is not a rule.
# Twin: approved 11:40 -> this run.
C("sc19", "In which pay run should the overtime claim be paid?",
"""
Payroll Calendar and Rules (Glenrothy Council)
P1. Claims approved by 12:00 on the Tuesday before payday are paid in that month's run. Claims approved later go into the next month's run.
P2. Overtime claims must be submitted within 3 months of the date the overtime was worked; later claims are rejected.
P3. Payroll staff may not make exceptions to P1 for individual claims.

September run: payday Friday 25 September 2026; cut-off Tuesday 22 September, 12:00.
October run: payday Friday 23 October 2026.

Claim OT-5512 (Jonah Pryce, Parks team)
Overtime worked: 30 June to 2 July 2026 (storm clean-up).
Submitted: 18 September 2026.
Approved by line manager: Tuesday 22 September 2026, 13:15.

Email from Jonah to payroll: "My manager says it's fine to squeeze this into September; please make sure it goes in."
""",
[("september_run", "The claim was approved before the Tuesday 12:00 cut-off and was submitted within three months."),
 ("october_run", "The claim missed the Tuesday 12:00 cut-off but was submitted within three months, so it goes in the next run."),
 ("reject_claim", "The overtime was worked more than three months before the claim was submitted, so it is out of time under P2 and cannot be paid.")],
"october_run", 1,
twin=T([("Approved by line manager: Tuesday 22 September 2026, 13:15.", "Approved by line manager: Tuesday 22 September 2026, 11:40.")], "september_run")),

# ------------------------------------------------------------------ sc20
# why: mandatory offices Varn (UTC+2) and Oskel (UTC-5); whole 60-min meeting within
# 08:00-18:00 local. 12:00 UTC -> Oskel 07:00 fail. 13:30 UTC -> Oskel 08:30-09:30,
# Varn 15:30-16:30 ok. 15:00 UTC -> Oskel 10:00, Varn 17:00-18:00 ok but later.
# Earliest compliant = 13:30. Tamura Bay optional. Oskel lead's offer does not
# override the working-hours rule.
# Twin: Oskel UTC-4 -> 12:00 UTC = 08:00 Oskel, 14:00 Varn -> 12:00 earliest.
C("sc20", "Which slot should the programme review call be booked in?",
"""
Meeting Standard (Quellwater Group), section 2
2.1 A meeting must start and finish within 08:00-18:00 local time for every mandatory attendee's office. Individual offers to attend outside these hours do not change this rule.
2.2 Book the earliest candidate slot that meets 2.1.
2.3 Optional attendees are invited where possible but do not affect slot choice.

Programme review call — 60 minutes
Mandatory: Varn office (UTC+2), Oskel office (UTC-5).
Optional: Tamura Bay office (UTC+8).

Candidate slots (UTC): 12:00, 13:30, 15:00.

Message from the Oskel lead (Mara Tull): "Happy to dial in before my hours start if that helps — just book the first slot."
PMO note: agenda circulated on Monday; recordings will be shared with Tamura Bay.
""",
[("slot_1200_utc", "At 12:00 UTC both mandatory offices are inside working hours, and it is the earliest slot."),
 ("slot_1330_utc", "12:00 UTC is before Oskel's working day starts, so 13:30 is the earliest slot within hours for both offices."),
 ("slot_1500_utc", "15:00 UTC is the slot closest to Tamura Bay's working day, so more people can join, and that should decide between compliant slots.")],
"slot_1330_utc", 2,
twin=T([("Oskel office (UTC-5)", "Oskel office (UTC-4)")], "slot_1200_utc")),

# ------------------------------------------------------------------ sc21
# why: hot work permit: weekdays only, work between 08:00 and 16:00 (start and finish),
# 60-min fire watch after; fire watchers on site until 17:00. 3 h job:
# 07:30 start before 08:00 -> fail; 13:00-16:00 + watch to 17:00 -> ok; 14:00-17:00
# finishes after 16:00 -> fail; Saturday -> permit invalid. -> 13:00.
C("sc21", "What start time should be approved for the welding job?",
"""
Permit-to-Work Procedure (Dunmore Business Park), hot work
H1. Hot work permits are valid Monday to Friday only.
H2. Hot work must start no earlier than 08:00 and finish no later than 16:00.
H3. A trained fire watcher must stay for 60 minutes after hot work ends. Fire watchers are on site until 17:00.
H4. Approve the proposed start time that meets H1-H3.

Job: welding repair to the plant-room steel frame, Unit 12. Estimated duration: 3 hours. Requested day: Wednesday 14 October.

Proposed start times from the contractor (Forde Fabrication)
- Wednesday 07:30
- Wednesday 13:00
- Wednesday 14:00
- Saturday 17 October 09:00

Contractor's email: "We'll start at 07:30 to beat the traffic — the permit desk said that's fine."
Unit 12 tenant asks that noisy work avoid 10:00-11:00 on Wednesday (staff briefing); this is a request, not a permit condition.
""",
[("wed_0730", "Starting at 07:30 is fine because the permit desk agreed and the window only limits when the work finishes."),
 ("wed_1300", "A 13:00 start finishes at 16:00 and the fire watch ends at 17:00, so it meets every permit condition."),
 ("wed_1400", "The 08:00-16:00 window governs only the start time, so a 14:00 start is allowed."),
 ("sat_0900", "Saturday is quieter, and hot work is safest when the park is empty.")],
"wed_1300", 1),
]
