"""proc_rubric / HR scoring: performance ratings, hiring loops, promotion, bonus, discipline, job
evaluation and selection matrices (Quenby Logistics, Marlow & Teague, Hestia Home Insurance, Corvane
Software, Pinfold Hospitality, Orrin Utilities, Saltmarsh Media)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ hr01
# why: 0.5*4 + 0.3*4 + 0.2*5 = 2.0 + 1.2 + 1.0 = 4.2 -> Strong. Warning 10 Feb 2026 live 6 months -> ended 10 Aug;
# review 15 Sept -> not live -> no cap.
C("hr01", "Which performance rating should be recorded for this employee?",
"""
Quenby Logistics — Annual Performance Review Guide 2026

Section 2 — Rating calculation
2.1 Objectives are scored 1–5: Delivery (weight 50%), Quality (30%), Collaboration (20%).
2.2 Weighted score = sum of weight x score.
2.3 Ratings: Outstanding 4.30+; Strong 3.50–4.29; Meets 2.50–3.49; Below under 2.50.

Section 3 — Caps
3.1 An employee with a written warning that is live on the review date cannot be rated above Meets.
3.2 A warning is live from the date of issue for the period stated on the warning letter.

Review record — Dana Kowalczyk, Warehouse Team Leader, Depot 4
Review date: 15 September 2026
Scores: Delivery 4, Quality 4, Collaboration 5
Warnings on file: first written warning issued 10 February 2026 (live for 6 months) — lateness.
Manager's comment: "Turned the night shift around after a difficult spring."
""",
[("outstanding", "The Collaboration score of 5 lifts the weighted score to at least 4.30."),
 ("strong", "The weighted score is 4.2, and the written warning was no longer live on the review date."),
 ("meets", "A written warning live on the review date caps the rating at Meets."),
 ("below", "Any written warning issued during the review year limits the rating to Below, whatever the scores.")],
"strong", 2),

# ------------------------------------------------------------------ hr02
# why: overall recs HM 3, A 4, B 1, Skip 4 -> avg 3.0; a strong no (1) from a non-HM interviewer -> debrief.
# Recruiter's fast-track request has no standing. Twin: HM 1, B 3 (avg still 3.0) -> HM veto -> reject.
C("hr02", "What should the recruiting coordinator do with this interview loop?",
"""
Corvane Software — Hiring Decision Rules (Engineering)

Each interviewer submits an overall recommendation: 4 strong yes, 3 yes, 2 no, 1 strong no.
D1. If the hiring manager's recommendation is 1, the candidate is rejected (hiring manager veto).
D2. Otherwise, if any other interviewer's recommendation is 1, or the average recommendation is 2.5–2.99, the loop goes to a debrief meeting before any decision.
D3. Otherwise, an average of 3.0 or more leads to an offer, and an average below 2.5 leads to rejection.

Candidate: Priyanka Raman — Senior Backend Engineer, req ENG-2291
Hiring manager (Tom Aldous): 3
Peer interviewer A (Keiko Hart): 4
Peer interviewer B (Luis Ferreira): 1 — "Could not reason about failure modes in the system design round."
Skip-level (Anneke Visser): 4

Recruiter note: "Candidate has a competing offer that expires Friday — please fast-track to offer."
""",
[("extend_offer", "The average recommendation is 3.0, which meets the offer bar, so the candidate can be made an offer now."),
 ("hold_debrief", "A strong no from an interviewer other than the hiring manager sends the loop to a debrief."),
 ("reject", "The hiring manager's strong no is a veto.")],
"hold_debrief", 2,
twin=T([("Hiring manager (Tom Aldous): 3", "Hiring manager (Tom Aldous): 1"),
        ("Peer interviewer B (Luis Ferreira): 1 — \"Could not reason about failure modes in the system design round.\"",
         "Peer interviewer B (Luis Ferreira): 3 — \"Solid on failure modes in the system design round.\"")], "reject")),

# ------------------------------------------------------------------ hr03
# why: effective 1 Oct 2026 -> amended 12-month rule; in grade since 1 Aug 2025 = 14 months; ratings Strong, Outstanding;
# panel 74 >= 70 -> yes. Twin: effective 1 Sept 2026 -> 18-month rule -> 13 months -> no.
Y("hr03", "Is the employee eligible for the proposed promotion?",
"""
Marlow & Teague — Promotion Policy (Professional Staff)

P1. Time in grade: at least 18 months in the current grade on the promotion effective date.
P2. Performance: the last two annual ratings must be Strong or Outstanding.
P3. Promotion panel score: at least 70 out of 100.
P4. Amendment (People Committee, 30 June 2026): for promotions effective on or after 1 October 2026, the period in P1 is 12 months.

Promotion case — Rhiannon Beaumont, Associate (Grade 4) to Senior Associate (Grade 5)
In current grade since: 1 August 2025
Proposed effective date: 1 October 2026
Annual ratings: 2024 Strong; 2025 Outstanding
Panel score: 74
Line manager: "Has run two client audits on her own this year."
""",
[("eligible", "Time in grade meets the rule that applies on the effective date, and both other criteria are met."),
 ("not_eligible", "At least one criterion fails under the rule that applies on the effective date.")],
1, 2,
twin=T([("Proposed effective date: 1 October 2026", "Proposed effective date: 1 September 2026")], 0)),

# ------------------------------------------------------------------ hr04
# why: £60,000 x 10% = £6,000 x 0.8 company x 1.1 (Strong) = £5,280 x 9/12 (joined 1 Apr) = £3,960.
C("hr04", "What 2025 bonus should payroll pay this employee?",
"""
Hestia Home Insurance — Annual Bonus Plan 2025 (plan year 1 January – 31 December 2025)

B1. Bonus = base salary x target % x company multiplier x individual multiplier x proration.
B2. Company multiplier for 2025, set by the Board: 0.8. It applies to all plan participants.
B3. Individual multipliers: Outstanding 1.5; Strong 1.1; Meets 1.0; Below 0.
B4. Proration: employees who joined during the plan year receive (full months employed ÷ 12).
B5. Employees who joined after 1 October 2025 are not eligible for a 2025 bonus.

Payroll extract — employee 40517, Claims Handler Team Lead
Base salary: £60,000. Target bonus: 10%.
Start date: 1 April 2025.
2025 rating: Strong.
Note: employee moved from a contractor role to permanent staff on the start date above.
""",
[("pay_3960", "£6,000 target x 0.8 company x 1.1 individual, prorated for nine full months."),
 ("pay_5280", "Proration applies only to leavers, so the full-year figure is paid."),
 ("pay_4950", "The company multiplier applies only to directors, so it is left out."),
 ("pay_0", "The employee joined after 1 October 2025 and is not eligible.")],
"pay_3960", 2),

# ------------------------------------------------------------------ hr05
# why: serious 3 + customer impact 1 - self-reported 1 = 3 -> first written warning. Earlier warning issued
# 12 Aug 2025, live 12 months -> expired 12 Aug 2026 < incident 2 Sept 2026 -> no aggravation.
# Twin: issued 12 Oct 2025 -> live on 2 Sept 2026 -> +1 -> 4 -> final written warning.
C("hr05", "Which sanction does the disciplinary matrix give?",
"""
Pinfold Hospitality — Disciplinary Sanction Matrix (Policy HR-07, Appendix B)

Severity points: minor misconduct 1; serious misconduct 3; gross misconduct 5.
Aggravating factors (+1 each): a warning that is live on the incident date; direct impact on guests or customers.
Mitigating factors (−1 each): the employee reported the issue themselves; five or more years' service with no sanctions.
Warnings are live for 12 months from the date of issue.

Total points → sanction
 1 or less: informal note
 2–3: first written warning
 4–5: final written warning
 6 or more: dismissal

Case DC-26-044 — Front-of-house supervisor, Harbour Street Hotel
Incident date: 2 September 2026
Finding: serious misconduct — left the reception desk unstaffed for 50 minutes; two guests could not check in.
The supervisor reported the lapse to the duty manager the same evening.
Service: 3 years 2 months.
Previous sanctions: first written warning issued 12 August 2025 (timekeeping).
""",
[("informal_note", "Reporting the lapse themselves halves the severity points, which leaves the case at the informal-note level."),
 ("first_written_warning", "Serious misconduct plus one aggravating and one mitigating factor totals 3; the old warning had lapsed."),
 ("final_written_warning", "The earlier warning was still live on the incident date, which adds a point for a total of 4."),
 ("dismissal", "Guest impact on a serious case turns it into gross misconduct.")],
"first_written_warning", 2,
twin=T([("first written warning issued 12 August 2025 (timekeeping)", "first written warning issued 12 October 2025 (timekeeping)")], "final_written_warning")),

# ------------------------------------------------------------------ hr06
# why: probation = 6 months from start (3 Mar -> 3 Sept 2026); request 20 Aug 2026 -> probation not completed -> no.
# Twin: request 10 Sept 2026 -> completed; on-site 15% < 20%, rating Meets -> yes.
Y("hr06", "Should the hybrid working request be approved?",
"""
Orrin Utilities — Hybrid Working Standard (HWS-2)

H1. An employee is eligible for a hybrid pattern (up to 3 days a week at home) if ALL of the following hold on the date of the request:
 (a) on-site essential tasks make up less than 20% of the role's contracted hours, as recorded in the role profile;
 (b) the employee's most recent performance rating is Meets or higher;
 (c) the employee has completed probation. Probation lasts six months from the start date.
H2. Managers may not approve requests from ineligible employees, even on a trial basis.

Request HW-26-381
Employee: Samir Haddad, Billing Analyst. Start date: 3 March 2026.
Role profile: on-site essential tasks 15% of hours (meter-data room access).
Most recent rating: Meets (probation mid-point review).
Date of request: 20 August 2026.
Manager's email: "I'm happy to support this — Samir has settled in well."
""",
[("approve", "Every eligibility condition holds on the date of the request."),
 ("decline", "At least one eligibility condition does not hold on the date of the request.")],
0, 1,
twin=T([("Date of request: 20 August 2026.", "Date of request: 10 September 2026.")], 1)),

# ------------------------------------------------------------------ hr07
# why: 180 + 110 + 90 + 70 = 450 -> Grade 5. +60 needs 5+ direct reports; contractors excluded -> 4 -> no.
# 450 is 50 from a boundary, not within 10 -> no panel.
C("hr07", "Which grade does the job evaluation give this role?",
"""
Saltmarsh Media — Job Evaluation Scheme (points-factor), Guide v4

Factors and maxima: Knowledge 200; Problem solving 150; Accountability 150; Communication 100.
Line-management addition: roles with five or more direct reports receive an extra 60 points under Accountability (this may take Accountability above its maximum).
Definition: "direct reports" are employees on the Saltmarsh payroll who report to the role. Contractors, agency workers and dotted-line reports are excluded.
Grades by total points: Grade 4 300–399; Grade 5 400–499; Grade 6 500–599.
Totals within 10 points of a grade boundary are reviewed by the evaluation panel before grading.

Evaluation — Role SM-DIG-014, Digital Production Lead
Knowledge 180 | Problem solving 110 | Accountability 90 | Communication 70
Reporting lines: 4 employees report directly; 2 freelance contractors also report to the role.
Requesting manager: "This role manages six people day to day and should be Grade 6."
""",
[("grade_4", "Communication points are capped at 50, which brings the total below 400."),
 ("grade_5", "The factor points total 450, and the role has fewer than five direct reports as defined."),
 ("grade_6", "The role has at least five direct reports as defined, which adds 60 points for a total of 510."),
 ("refer_to_panel", "A total that is a round 50 points from a grade boundary must go to the evaluation panel.")],
"grade_5", 2),

# ------------------------------------------------------------------ hr08
# why: deal cancelled on day 40 (< 90) -> clawed back. Recognised = 120 + 60 + 40 = 220k.
# 200k x 8% = 16,000 + 20k x 12% = 2,400 -> 18,400. Twin: cancelled day 120 -> counts -> 270k -> 16,000 + 8,400 = 24,400.
C("hr08", "What Q2 commission is the sales representative owed?",
"""
Marlow & Teague Software Sales — Commission Plan FY2026

C1. Quarterly quota: £200,000 of recognised revenue.
C2. Commission: 8% on recognised revenue up to quota; 12% on recognised revenue above quota, in the same quarter.
C3. Clawback: a deal cancelled within 90 days of signature is removed from recognised revenue. Cancellations after 90 days do not affect commission.
C4. Commission is paid in full at the end of the month after the quarter.

Q2 statement — rep Eliska Novak
Deal A — Brookhaven Clinics: £120,000, signed 4 April
Deal B — Tinwell Hotels: £60,000, signed 22 April
Deal C — Carrick Freight: £50,000, signed 15 May; customer cancelled 40 days after signature
Deal D — Orla Opticians: £40,000, signed 20 June
Sales director's note: "Eliska was the top performer in the region this quarter."
""",
[("pay_16000", "Revenue above quota is paid in the following quarter, so only the 8% portion is due now."),
 ("pay_17600", "A single 8% rate applies to all recognised revenue."),
 ("pay_18400", "The deal cancelled within 90 days is removed, leaving £220,000, of which £20,000 earns 12%."),
 ("pay_24400", "No deal was cancelled inside the 90-day window, so all £270,000 counts.")],
"pay_18400", 2,
twin=T([("customer cancelled 40 days after signature", "customer cancelled 120 days after signature")], "pay_24400")),

# ------------------------------------------------------------------ hr09
# why: pass needs all three objectives at least Partly met, at least two Met, and no conduct case.
# Met, Partly met, Met -> yes.
Y("hr09", "Does the employee pass probation?",
"""
Quenby Logistics — Probation Review Form (office roles)

Rule: probation is passed if (i) every objective is rated at least "Partly met", (ii) at least two objectives are rated "Met", and (iii) there is no open conduct case. Otherwise probation is extended by up to three months or ended, as HR advises.

Employee: Marcus Oyelaran, Transport Planner. Probation: 6 months ending 30 September 2026.
Objective 1 — Build weekly trunking plans for the North region: Met
Objective 2 — Reduce empty running on two routes by 5%: Partly met (3.5% achieved)
Objective 3 — Complete TMS system training: Met
Conduct cases: none.
Manager's comment: "Good attitude. I extended the previous planner's probation last year, so I've been watching closely."
""",
[("pass_probation", "Every objective is at least Partly met, two or more are Met, and there is no conduct case."),
 ("do_not_pass", "One of the three probation conditions is not satisfied.")],
1, 1),

# ------------------------------------------------------------------ hr10
# why: J: tenure 7 -> capped 5 + Strong 3 + skills 4 + approved hardship 3 = 15. K: 3 + 4 + 6 + 0 (not approved) = 13.
# L: 5 + 3 + 5 + 0 = 13 -> J. Twin: J's hardship pending -> 12; K and L tie 13 -> longer tenure L (5 vs 3).
C("hr10", "Which candidate should be offered the internal transfer?",
"""
Orrin Utilities — Internal Transfer Scoring (Field Operations)

Points
 Tenure: 1 point per complete year of service, maximum 5.
 Latest rating: Outstanding 4; Strong 3; Meets 2.
 Skills match (assessed by the hiring manager): 0–6.
 Hardship: 3 points only if a hardship request has been approved by HR. Requests that are pending or declined score 0.
The highest total is offered the role. If totals tie, the candidate with the longer tenure (in years of service, uncapped) is offered it. The role is readvertised only if no candidate scores 10 or more.

Candidates — Senior Field Technician, Kettering depot
J — Ade Okonkwo: 7 years' service; Strong; skills 4; hardship request (carer for parent near Kettering) approved by HR 2 July.
K — Bella Stroud: 3 years' service; Outstanding; skills 6; hardship request submitted 1 August, not approved.
L — Chris Pellow: 5 years' service; Strong; skills 5; no hardship request.
""",
[("select_j", "Candidate J has the highest total once only approved hardship points are counted."),
 ("select_k", "Candidate K's hardship request adds 3 points, which gives K the highest total."),
 ("select_l", "Candidates K and L tie for the highest counted total, and L has the longer tenure."),
 ("readvertise", "A tie between candidates means the role must be readvertised.")],
"select_j", 3,
twin=T([("hardship request (carer for parent near Kettering) approved by HR 2 July.", "hardship request (carer for parent near Kettering) submitted 2 July, decision pending.")], "select_l")),

# ------------------------------------------------------------------ hr11
# why: peers have only 2 responses (< 3) -> peer group excluded; remaining groups equally weighted: (4.4 + 4.0)/2 = 4.2 >= 4.0 -> nominate.
C("hr11", "What should the talent team decide on the leadership programme nomination?",
"""
Corvane Software — Emerging Leaders Programme: Nomination Rule

N1. The candidate's 360 result is the equal-weighted average of the rater-group averages (manager, peers, direct reports).
N2. The peer and direct-report groups count only if they have at least 3 responses; a group with fewer responses is left out, and the remaining groups are averaged with equal weight. The manager group always counts.
N3. A 360 result of 4.0 or more (out of 5) qualifies the candidate for nomination. Below 4.0: not nominated this cycle.
N4. Incomplete 360s are not rerun; N2 is applied instead.

360 summary — Jonah Whitfield, Engineering Manager
Manager: 4.4 (1 response)
Peers: 3.2 (2 responses; 3 invited)
Direct reports: 4.0 (4 responses)
HRBP note: "Jonah was nominated for the programme in 2024 but withdrew for paternity leave."
""",
[("nominate", "With too few peer responses, the peer group is left out, and the other two groups average 4.2."),
 ("do_not_nominate", "All three rater groups count, and their equal-weighted average is below 4.0."),
 ("defer_to_next_cycle", "Missing peer responses make the 360 incomplete, so it has to be rerun in the next cycle before any nomination.")],
"nominate", 2),

# ------------------------------------------------------------------ hr12
# why: needs 6 months in post by 1 April 2026: joined 10 Oct 2025 -> 5 months 22 days -> no step.
# Twin: joined 25 Sept 2025 -> over 6 months -> yes.
Y("hr12", "Does the employee receive a pay step on 1 April 2026?",
"""
Saltmarsh Media — Pay Progression Rules (Band C)

S1. On 1 April each year, an employee moves up one pay step if (a) they have been in post for at least six months on 1 April and (b) their latest rating is Meets or higher.
S2. Employees already at the top step receive a one-off 2% payment instead of a step.
S3. Time on secondment within Saltmarsh counts as time in post.

Employee: Freya Lindqvist, Sound Editor (Band C, step 2 of 6)
Joined Saltmarsh: 10 October 2025
Latest rating: Strong (probation review, February 2026)
Manager's note: "Freya covered the whole podcast slate during the winter shutdown."
""",
[("pay_step", "The employee has been in post for six months by 1 April and is rated Meets or higher."),
 ("no_pay_step", "One of the pay-step conditions is not met on 1 April.")],
0, 1,
twin=T([("Joined Saltmarsh: 10 October 2025", "Joined Saltmarsh: 25 September 2025")], 1)),

# ------------------------------------------------------------------ hr13
# why: window 16 Sept 2025 - 15 Sept 2026. Exclude spell 1 (outside window) and spell 4 (adjustment plan).
# S = 4, D = 1+2+1+2 = 6 -> 16 x 6 = 96 -> no action.
# Twin: spell 4 is ordinary sickness -> S = 5, D = 9 -> 25 x 9 = 225 -> stage 1. (All six: 36 x 13 = 468 trap.)
C("hr13", "Which absence management step does the trigger score require?",
"""
Pinfold Hospitality — Attendance Policy, Section 5 (trigger score)

5.1 Trigger score = S x S x D, where S is the number of separate absence spells and D is the total days absent, both counted over the rolling 52 weeks up to the review date.
5.2 Absences recorded under an agreed disability adjustment plan are excluded from S and D.
5.3 Score 200–399: stage 1 meeting. 400–649: stage 2 meeting. 650 or more: stage 3 meeting. Below 200: no action.

Review date: 15 September 2026
Employee: Housekeeping Supervisor, Riverside Hotel

Absence record
1. 18–21 August 2025 — 4 days — gastroenteritis
2. 3 November 2025 — 1 day — migraine
3. 12–13 January 2026 — 2 days — flu
4. 9–11 March 2026 — 3 days — disability-related, recorded under adjustment plan AP-14
5. 27 May 2026 — 1 day — dental emergency
6. 6–7 August 2026 — 2 days — back strain

Line manager: "Attendance has been a problem on this team generally."
""",
[("no_action", "Excluding the adjustment-plan spell and the one older than 52 weeks leaves 4 spells and 6 days: 96."),
 ("stage_1_meeting", "Counting every spell in the rolling 52 weeks gives 5 spells and 9 days, a score of 225."),
 ("stage_2_meeting", "Counting all six spells on file, including the older one, gives 6 spells and 13 days, a trigger score of 468.")],
"no_action", 3,
twin=T([("3 days — disability-related, recorded under adjustment plan AP-14", "3 days — chest infection")], "stage_1_meeting")),

# ------------------------------------------------------------------ hr14
# why: essential criterion 1 met by equivalent experience (3+ years in a comparable role; 60% duty match >= 50%).
# 4 years -> met; right to work evidenced -> shortlist. Twin: 2 years -> not met -> no.
Y("hr14", "Should the applicant be shortlisted?",
"""
Hestia Home Insurance — Shortlisting Rules: Pricing Analyst (req PA-0613)

Essential criteria (all must be met to shortlist)
E1. A degree in a numerate subject OR equivalent experience. "Equivalent experience" means at least 3 years in a comparable role. A role is comparable if the screener assesses that at least 50% of its duties match the key tasks in the job description.
E2. Advanced spreadsheet skills (evidenced in the application).
E3. Right to work in the UK (evidence seen by the recruiter).
Desirable criteria are used only to rank shortlisted applicants.

Screening record — Applicant 118
Degree: none
Experience: 4 years as Assistant Analyst, Pellam Motor Finance. Screener's assessment: 60% of duties match the key tasks.
Spreadsheet skills: evidenced (built rate-change models; examples described).
Right to work: passport seen 2 September 2026.
Note: applied for a Hestia claims role in 2024 and was not shortlisted.
""",
[("shortlist", "Every essential criterion is met, including E1 through equivalent experience."),
 ("do_not_shortlist", "At least one essential criterion is not met.")],
1, 2,
twin=T([("Experience: 4 years as Assistant Analyst", "Experience: 2 years as Assistant Analyst")], 0)),

# ------------------------------------------------------------------ hr15
# why: intake Feb 2027 -> amendment applies (presentation counts double): (4 + 4 + 2*2 + 4)/5 = 16/5 = 3.2 -> reserve.
# No score of 1.
C("hr15", "Which outcome does the assessment centre rubric give this graduate candidate?",
"""
Quenby Logistics — Graduate Scheme Assessment Centre: Decision Rubric

A1. Four exercises, each scored 1–5: group exercise, case study, presentation, interview.
A2. The overall score is the average of the exercise scores (equal weights).
A3. Any exercise scored 1: reject. Otherwise: overall 3.5 or more — make offer; 3.0–3.49 — reserve list; below 3.0 — reject.
A4. Amendment (Early Careers Board, April 2026): for intakes starting on or after 1 January 2027, the presentation counts twice in the average (divide by 5).

Candidate: Imogen Achterberg — applying for the February 2027 intake
Scores: group exercise 4; case study 4; presentation 2; interview 4
Assessor note: "Presentation ran over time and skipped the recommendations slide."
Adjustments: 25% extra time on the case study (agreed in advance).
""",
[("make_offer", "Under the weighting for this intake, the average is 3.5 and no exercise scored 1."),
 ("reserve_list", "The presentation counts twice for this intake, giving an average of 3.2."),
 ("reject", "A score of 2 on any exercise leads to rejection.")],
"reserve_list", 2),

# ------------------------------------------------------------------ hr16
# why: P = 3*3 + 4*2 + 4 = 21; Q = 4*3 + 3*2 + 3 - 2 (live final warning) = 19; R = 3*3 + 3*2 + 5 (protected absences excluded) = 20.
# Lowest = Q. (Using "all absences" gives R 16: trap.) Twin: Q's warning expired -> Q 21 -> R 20 lowest.
C("hr16", "Which employee does the selection matrix select?",
"""
Orrin Utilities — Selection Matrix for Redundancy (Pool: Metering Admin, 3 roles to 2)

Scoring
 Skills (1–5) x 3
 Performance (1–5) x 2
 Attendance (1–5) x 1 — score attendance only after disregarding absences for pregnancy, disability or jury service.
 Disciplinary: −2 for a final written warning that is live on the scoring date; expired warnings score 0.
The employee with the lowest total is provisionally selected. Length of service is not a criterion.

Scoring sheet (scoring date 1 September 2026)
| Employee | Skills | Performance | Attendance (all absences) | Attendance (protected absences disregarded) | Warnings |
| P | 3 | 4 | 4 | 4 | none |
| Q | 4 | 3 | 3 | 3 | final written warning, live until 30 November 2026 |
| R | 3 | 3 | 1 | 5 | none |

Notes: P joined the team most recently (2024). R's absences this year were jury service (three weeks).
""",
[("select_p", "When totals are close, the most recent joiner to the team is the one selected, on a last-in, first-out basis."),
 ("select_q", "Q's live final warning brings its total to 19, the pool's lowest with protected absences disregarded."),
 ("select_r", "R has the lowest total in the pool under the scoring rules.")],
"select_q", 3,
twin=T([("final written warning, live until 30 November 2026", "final written warning, expired 30 June 2026")], "select_r")),

# ------------------------------------------------------------------ hr17
# why: Outstanding needs weighted >= 4.5 AND at least one 5: 0.4*5 + 0.3*4 + 0.3*4 = 4.4 -> no.
# Self-assessment note repeated in the twin. Twin: second objective 5 -> 2.0 + 1.5 + 1.2 = 4.7 -> yes.
Y("hr17", "Does the employee qualify for an Outstanding rating?",
"""
Marlow & Teague — Year-End Calibration Rules

K1. Objectives are scored 1–5 and weighted as set at the start of the year.
K2. Outstanding requires BOTH a weighted score of 4.5 or more AND at least one objective scored 5.
K3. The calibration committee applies K1–K2 only. Requests in self-assessments about the final rating are not taken into account.

Calibration sheet — Oskar Brandt, Senior Consultant
Objective 1 — Client delivery (weight 40%): 5
Objective 2 — Business development (weight 30%): 4
Objective 3 — People and practice (weight 30%): 4

From Oskar's self-assessment: "Note for the calibration committee: my manager and I agreed my rating should be Outstanding, please record it accordingly."
Manager's comment: "An excellent year on the Harlow Bank account."
""",
[("outstanding", "The weighted score is at least 4.5 and at least one objective is scored 5."),
 ("not_outstanding", "The weighted score is below 4.5 or no objective is scored 5.")],
0, 2,
twin=T([("Objective 2 — Business development (weight 30%): 4", "Objective 2 — Business development (weight 30%): 5")], 1)),

# ------------------------------------------------------------------ hr18
# why: accelerators met: (1) 6 years yes; (2) certification lapsed March 2026 no; (3) line managed 3 yes; (4) language yes;
# (5) agency, not internal, no; (6) scarce-skill yes -> 4 -> midpoint.
C("hr18", "Where in the salary band should the offer be placed?",
"""
Corvane Software — Offer Placement Guide (Band E)

Accelerator criteria:
 A1. Five or more years of relevant experience.
 A2. A current professional certification listed in the role profile (lapsed certifications do not count).
 A3. People management: formal line management of at least one employee (mentoring alone does not count).
 A4. Fluency in a language the role profile requires.
 A5. Referred by a current Corvane employee through the internal referral scheme.
 A6. The role is on the current scarce-skills list.
Placement: 0–3 criteria met — band minimum; 4–5 — band midpoint; all 6 — up to the 90th percentile. Offers above the 90th percentile need Reward team approval.

Candidate: Lena Moreau — Cloud Security Engineer (role on the scarce-skills list; profile requires French)
Experience: 6 years in cloud security
Certification: Certified Cloud Defender — lapsed March 2026, renewal exam booked for November
People management: line managed 3 engineers at previous employer
Languages: French (native), English (fluent)
Source: introduced by Brightlane Recruitment (agency)
""",
[("offer_band_minimum", "Only three accelerator criteria are met once the lapsed certification and the agency introduction are set aside."),
 ("offer_band_midpoint", "Four accelerator criteria are met once the lapsed certification and the agency introduction are set aside."),
 ("offer_up_to_p90", "All six accelerator criteria are met, counting the certification and the introduction."),
 ("escalate_to_reward", "Roles on the scarce-skills list always go to the Reward team for pricing.")],
"offer_band_midpoint", 2),
]
