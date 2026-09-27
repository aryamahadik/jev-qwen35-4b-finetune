"""proc_rubric / academic marking, scholarships, admissions and exam boards (University of Wexmoor,
Calder Hythe College, Brantwood Institute, Pellow Sixth Form, Northmere University, Eskdale
Apprenticeship Board, Ravensholt University Students' Union)."""
from _lib import C, Y, T

ITEMS = [
# ------------------------------------------------------------------ ac01
# why: deadline Thu 12 Mar; penalty days = working days from Fri 13 to the submission day: Fri 13, Mon 16 = 2.
# 58 - 20 = 38, but floor 40 because unpenalised mark was a pass -> record 40. Extension was declined.
# Twin: submitted Tue 24 Mar = 8 working days (> 5) -> 0.
C("ac01", "Which mark should the module office record for this coursework?",
"""
University of Wexmoor — School of Social Sciences
Late Submission Policy (Assessment Regulations, section 11)

11.1 Penalty days are counted as the number of working days (Monday–Friday) from the day after the deadline up to and including the day of submission.
11.2 For up to five penalty days, the mark is reduced by 10 marks per penalty day. The penalty cannot reduce a mark below 40 if the unpenalised mark was 40 or more.
11.3 Work with more than five penalty days receives a mark of 0.
11.4 An approved extension moves the deadline. Requests that are pending or declined do not.

Coursework record — SOC2041 Essay 2
Student: 2419087
Deadline: Thursday 12 March 2026, 14:00
Submitted: Monday 16 March 2026, 10:00
Unpenalised mark (first marker, moderated): 58
Extension request: submitted 11 March 2026 — declined 12 March 2026 (no supporting evidence).
Personal tutor note: "Student has been working two jobs this term."
""",
[("record_58", "The student's extension request covers the late days, so the work counts as on time and no penalty applies."),
 ("record_48", "The work is one working day late, so it loses 10 marks."),
 ("record_40", "Two penalty days cost 20 marks, but the penalty cannot take a passing piece below 40."),
 ("record_38", "Two penalty days cost 20 marks, taking 58 to 38."),
 ("record_0", "The work has more than five penalty days, so it receives a mark of zero.")],
"record_40", 2,
twin=T([("Submitted: Monday 16 March 2026, 10:00", "Submitted: Tuesday 24 March 2026, 10:00")], "record_0")),

# ------------------------------------------------------------------ ac02
# why: 2026/27 cycle -> amended income limit £45,000; £43,500 eligible. Score 78 >= 75 -> full.
# Partial-only rule needs another award over £3,000; the bursary is £1,500.
C("ac02", "What scholarship outcome should the committee record?",
"""
Calder Hythe College — Access Scholarship Scheme

Eligibility
E1. Household income must be £42,000 or less (latest tax year).
Amendment (Governors, 5 May 2026): for applications in the 2026/27 cycle and later, the limit in E1 is £45,000.

Scoring
S1. Academic record (0–40) + Personal statement (0–30) + Interview (0–30).
S2. 75 or more: full scholarship (£6,000 a year). 60–74: partial scholarship (£2,500 a year). Below 60: no award.
S3. An applicant who already holds another award worth more than £3,000 a year may receive a partial scholarship at most.

Applicant file — AS-26-148, cycle 2026/27
Household income: £43,500
Scores: academic 32, statement 22, interview 24 — total 78
Other awards held: Tennant Trust bursary, £1,500 a year
Referee: "The most determined student I have taught in ten years."
""",
[("full_scholarship", "Household income is within the limit for this cycle and the score of 78 reaches the full band."),
 ("partial_scholarship", "Because the applicant already holds another award, only a partial scholarship can be made."),
 ("no_award", "Household income is above the limit that applies to this cycle.")],
"full_scholarship", 2),

# ------------------------------------------------------------------ ac03
# why: best three A levels only; AS excluded: A 48 + B 40 + C 32 = 120 -> 112-127 -> conditional.
# School not on the Access list. Twin: Oakbrook Academy is on the list -> bars lowered by 16 -> unconditional at 112+.
C("ac03", "Which admissions decision does the tariff rule give?",
"""
Brantwood Institute — BSc Environmental Management: Admissions Decision Rules 2026

Tariff points: A* = 56, A = 48, B = 40, C = 32, D = 24, E = 16.
T1. Only the applicant's best three A levels count. AS levels do not count toward the tariff.
T2. 128 points or more: unconditional offer. 112–127: conditional offer. Below 112: reject.
T3. Access Scheme: applicants from a school on the Access Scheme list have both thresholds in T2 lowered by 16 points.

Access Scheme list (2026): Oakbrook Academy; St Aidan's High School; Lowther Park College; Millfield Vale School.

Application BI-26-4471
School: Fernhill Community College
A levels: Geography A, Biology B, Economics C
AS level: Chemistry D
Personal statement: strong fieldwork interest; volunteer with a river trust.
Applicant's note: "My teacher said my AS should count toward the offer."
""",
[("unconditional_offer", "The applicant's school is on the Access Scheme list, so the lowered unconditional bar of 112 is met."),
 ("conditional_offer", "The best three A levels give 120 points, between 112 and 127, and no Access Scheme reduction applies."),
 ("reject", "Only A levels at grade B or above count, leaving 88 points.")],
"conditional_offer", 2,
twin=T([("School: Fernhill Community College", "School: Oakbrook Academy")], "unconditional_offer")),

# ------------------------------------------------------------------ ac04
# why: compensation needs failed mark 35-39, year average >= 50, failed credits <= 20: 37, 52, 20 -> yes.
# Last year's resit is history.
Y("ac04", "Can the exam board compensate the failed module?",
"""
Northmere University — Progression Regulations, Regulation 7 (Compensation)

7.1 A student who fails a module may have the failure compensated, and progress without reassessment, if ALL of the following hold:
 (a) the failed module mark is between 35 and 39 inclusive;
 (b) the student's credit-weighted average for the year is 50 or more;
 (c) the total credits failed in the year is 20 or fewer.
7.2 Compensation is applied automatically by the board; the student does not need to apply.
7.3 Modules marked "non-compensatable" in the programme specification are excluded.

Board papers — Student 2208813, BA Business Management, Year 2
Failed: BUS2203 Operations Analysis (20 credits), mark 37. Not listed as non-compensatable.
All other modules passed. Credit-weighted year average: 52.
Year 1: failed BUS1102 at first attempt, passed at resit (August 2025).
""",
[("compensate", "All three compensation conditions are met for this module."),
 ("do_not_compensate", "At least one compensation condition is not met for this module.")],
1, 1),

# ------------------------------------------------------------------ ac05
# why: examiners disagree (minor vs major); chair records no view -> less favourable = major corrections.
# Supervisor's view has no role (candidate's claim repeated in twin). Twin: chair supports the more favourable -> minor.
C("ac05", "Which doctoral examination outcome should the Research Degrees Office record?",
"""
University of Wexmoor — Doctoral Examination Code, section 9

9.1 Outcomes: (a) pass with no corrections; (b) minor corrections, within 3 months; (c) major corrections, within 12 months; (d) revise and resubmit; (e) fail.
9.2 Where the internal and external examiners recommend different outcomes, the outcome recorded is the less favourable recommendation, unless the independent chair's report supports the more favourable one, in which case that is recorded.
9.3 The supervisor attends the viva only as an observer and has no part in the recommendation.

Viva record — candidate Hannah Ekwueme, thesis "Tenancy law and informal housing"
Internal examiner: minor corrections.
External examiner: major corrections (chapter 4 method needs reworking).
Independent chair's report: "The examiners discussed their positions fully. I record no view on the outcome."

Email from candidate to the Research Degrees Office: "My supervisor says it should be minor corrections, so please record that."
""",
[("pass_no_corrections", "When examiners disagree, corrections are waived and the thesis passes as submitted."),
 ("minor_corrections", "The independent chair's report supports the more favourable recommendation."),
 ("major_corrections", "The examiners disagree and the chair takes no position, so the less favourable recommendation stands."),
 ("revise_and_resubmit", "Any disagreement between the internal and external examiners requires the thesis to be revised and resubmitted.")],
"major_corrections", 2,
twin=T([("I record no view on the outcome.", "I support the internal examiner's recommendation.")], "minor_corrections")),

# ------------------------------------------------------------------ ac06
# why: final = 0.4*72 + 0.6*31 = 28.8 + 18.6 = 47.4; exam 31 < 35 qualifying -> fail, capped at 39.
C("ac06", "What result should be entered for this student on the module?",
"""
Calder Hythe College — Module ACC301 Management Accounting: Assessment Scheme

Components: coursework 40%, examination 60%.
Rule 1. Final mark = 0.4 x coursework + 0.6 x examination, rounded to the nearest whole number.
Rule 2. Qualifying mark: the examination must be at least 35. If it is not, the module is failed and the final mark is recorded as the lower of the calculated final mark and 39.
Rule 3. Otherwise, a final mark of 40 or more is a pass.
Rule 4. Coursework has no qualifying mark.

Student record — 23-0719
Coursework: 72
Examination: 31
Attendance: 94%
Note from lecturer: "Excellent project work; the exam was sat two days after a family bereavement." (No extenuating-circumstances claim has been submitted.)
""",
[("record_pass_47", "The weighted final of 47 clears 40, which is all a pass requires."),
 ("record_pass_50", "The examination meets the 35 qualifying mark and the weighted final rounds to 50."),
 ("record_fail_39", "The examination is below the 35 qualifying mark, so the module fails with the mark capped at 39."),
 ("record_fail_31", "When the examination is below the qualifying mark, the examination mark alone is recorded.")],
"record_fail_39", 2),

# ------------------------------------------------------------------ ac07
# why: renewal needs GPA >= 3.0 and >= 24 credits completed; pass/fail credits count toward credits (not GPA).
# 21 graded + 4 P/F passed = 25 -> yes. Twin: P/F course failed -> no credit -> 21 -> no.
Y("ac07", "Should the scholarship be renewed for next year?",
"""
Brantwood Institute — Merit Scholarship Renewal Criteria

R1. Cumulative GPA for the year of at least 3.0.
R2. At least 24 credits completed in the year.
R3. Credits from courses taken pass/fail count toward the credit total in R2 but are not included in the GPA. A failed course, graded or pass/fail, earns no credits.
R4. Renewal is decided on these criteria only; the scholar's activities and references are not considered.

Scholar: Mateo Villanueva, Year 1 review (academic year 2025/26)
Graded courses: 21 credits, GPA 3.1
Pass/fail courses: FLD150 Field Skills (4 credits) — Pass
Activities: student ambassador; chess club treasurer.
Advisor note: "Took a lighter graded load in spring to manage a part-time job."
""",
[("renew", "The GPA is at least 3.0 and the credits that count under the rules reach 24."),
 ("do_not_renew", "The GPA or the countable credit total falls short of the renewal criteria.")],
1, 2,
twin=T([("FLD150 Field Skills (4 credits) — Pass", "FLD150 Field Skills (4 credits) — Fail")], 0)),

# ------------------------------------------------------------------ ac08
# why: similarity 44% minus 10 points properly quoted = 34% -> band 21-40% = 2 points; Year 2 = 1; prior case
# overturned = 0. Total 3 -> mark capped at 40. Twin: prior case upheld -> +2 -> 5 -> mark of zero.
C("ac08", "Which penalty does the academic misconduct tariff set for this case?",
"""
Northmere University — Academic Misconduct Tariff (Plagiarism), 2025 revision

Points
P1. Extent (similarity after exclusions): up to 20% = 1; 21–40% = 2; over 40% = 3.
P2. Level of study: Year 1 = 0; Year 2 = 1; Year 3 or postgraduate = 2.
P3. Earlier cases: none = 0; one = 2; two or more = 3. Only upheld cases count; cases overturned on appeal count as none.
Exclusions: text that is in quotation marks and correctly referenced is excluded from the similarity figure.

Penalty bands
0–2 points: formal warning, mark stands. 3–4: assessment mark capped at 40. 5–6: mark of 0 for the assessment. 7 or more: referral to the Misconduct Panel.

Case file AM-26-0311 — Year 2 student, module HIS2105
Similarity report: 44% overall. Marker's check: 10 percentage points of this are quotations correctly marked and referenced.
Earlier cases: AM-25-0102 (Year 1). Outcome: overturned on appeal (March 2025).
Student statement: "I didn't realise paraphrasing a website without citing it counted."
""",
[("warning_only", "Once quoted material is excluded, the similarity falls in the lowest band, so the case totals 2 points."),
 ("cap_mark_at_40", "Quoted text is excluded and the overturned case does not count, which gives 3 points."),
 ("mark_of_zero", "The student has an upheld earlier case, which with the similarity and level points makes 5."),
 ("refer_to_panel", "Any student with an earlier case on file is referred to the Misconduct Panel.")],
"cap_mark_at_40", 3,
twin=T([("Outcome: overturned on appeal (March 2025).", "Outcome: upheld (March 2025).")], "mark_of_zero")),

# ------------------------------------------------------------------ ac09
# why: waiver needs an English-taught degree completed within 5 years before 1 Oct 2026; Sept 2019 is 7 years -> no waiver.
# IELTS writing 6.0 < 6.5 -> language not met; interview 82 >= 70 -> conditional offer (rule 4).
# Twin: MSc completed Sept 2023 -> waiver -> unconditional offer.
C("ac09", "What decision should the doctoral admissions tutor make?",
"""
Ravensholt University — PhD Admissions: Decision Rules (programme start 1 October 2026)

1. Academic bar: interview panel score of 70 or more out of 100.
2. English language: IELTS overall 7.0 with no component below 6.5.
3. Waiver of rule 2: an applicant who completed a degree of at least one year, taught and assessed entirely in English, within the five years before the programme start date.
4. An applicant who meets the academic bar but not the English language requirement receives an offer conditional on meeting it before enrolment.
5. An applicant below the academic bar is rejected.

Applicant: Yuki Matsuda
Interview panel score: 82
IELTS (taken May 2026): overall 7.5; listening 8.0, reading 8.0, speaking 7.5, writing 6.0
Previous study: MSc Hydrology, University of Carrowgate (taught and assessed entirely in English), completed September 2019.
Supervisor's note: "Excellent candidate; I would like her to start in October."
""",
[("unconditional_offer", "The English-taught degree falls within the waiver window, and the interview score clears the academic bar."),
 ("conditional_offer_english", "The degree is too old for the waiver and IELTS writing is under 6.5, so the offer depends on English."),
 ("reject", "Failing the English language requirement rules the applicant out of this intake, whatever the interview score.")],
"conditional_offer_english", 2,
twin=T([("completed September 2019", "completed September 2023")], "unconditional_offer")),

# ------------------------------------------------------------------ ac10
# why: peer factor = X's score / group mean = 3.2 / 4.0 = 0.8 >= 0.7 -> mark 55*0.8 = 44 >= 40, no referral -> yes.
# Twin: X 2.4 and D 4.4 (mean still 4.0) -> factor 0.6 < 0.7 -> tutor review -> no.
Y("ac10", "Can Student X's component mark be recorded as a pass without tutor review?",
"""
Pellow Sixth Form — Extended Project (Group Component): Peer Moderation Rules

M1. The group receives a single group mark out of 100.
M2. Each member's peer score is the average of the ratings they received from teammates (scale 1–5).
M3. Peer factor = member's peer score ÷ group mean peer score.
M4. Individual mark = group mark x peer factor, capped at 100.
M5. If a member's peer factor is below 0.7, no individual mark is recorded; the case goes to tutor review.
M6. The pass mark for the component is 40.

Group 6 — group mark 55
Peer scores: A 4.4 | B 4.2 | C 4.6 | D 3.6 | X 3.2
Group mean peer score: 4.0
Tutor's log: "Student X missed two planning meetings in March but led the final presentation."
""",
[("record_pass", "The peer factor is at least 0.7 and the resulting individual mark is 40 or more."),
 ("do_not_record_pass", "The peer factor or the resulting individual mark does not allow a pass to be recorded without review.")],
1, 2,
twin=T([("D 3.6 | X 3.2", "D 4.4 | X 2.4")], 0)),

# ------------------------------------------------------------------ ac11
# why: M1 71 (first-class band) and M2 64 (upper second) fall in different bands -> third mark (72) is final -> first.
C("ac11", "Which classification should the dissertation receive?",
"""
Northmere University — Dissertation Marking Protocol (Undergraduate)

1. Each dissertation is marked independently by two markers.
2. If the two marks are less than 10 apart and fall in the same classification band, the final mark is their average, rounded to the nearest whole number.
3. If the two marks are 10 or more apart, or fall in different classification bands, the third marker's mark is final.
4. Bands: 70+ First; 60–69 Upper second; 50–59 Lower second; 40–49 Third.
5. The moderation system assigns a third marker to every dissertation on this programme as a sample check. A third mark is used only where point 3 applies.

Dissertation — BSc Psychology, candidate 20-3381
Marker 1: 71
Marker 2: 64
Third marker (sample check): 72
Supervisor's comment: "A careful piece of work; the literature review is exceptional."
""",
[("first_class", "The first two marks fall in different classification bands, so the third marker's 72 is final."),
 ("upper_second", "The first two marks are in the same band and less than 10 apart, so their rounded average stands."),
 ("lower_second", "When markers disagree, the lower of the first two marks is recorded.")],
"first_class", 2),

# ------------------------------------------------------------------ ac12
# why: GPA (4+4+3.7+4)/4 = 3.925 -> 3.93. An incomplete in a GRADED course makes the student ineligible for term honours -> no_honours.
C("ac12", "Which term honours designation should the registrar record?",
"""
Ravensholt University — Term Honours Policy

H1. Honours bands by term GPA: Highest Honours 3.90+; High Honours 3.75–3.89; Honours 3.60–3.74.
H2. The student must complete at least 12 graded credits in the term.
H3. An incomplete (I) grade in any graded course makes the student ineligible for honours that term.
H4. Incomplete grades in pass/fail courses do not affect honours.

Autumn 2025 transcript — student 70-44129
ECON 210 Intermediate Microeconomics (3 cr, graded) — A
MATH 221 Linear Algebra (3 cr, graded) — A
HIST 145 Atlantic Worlds (3 cr, graded) — A-
PSYC 230 Social Psychology (3 cr, graded) — A
ENVS 260 Field Methods (3 cr, graded) — I
LAB 101 Research Safety Lab (1 cr, pass/fail) — P
Term GPA (completed graded courses): 3.93 across 12 credits
""",
[("highest_honours", "The term GPA is above 3.90 and the only incomplete is in a pass/fail course."),
 ("high_honours", "An incomplete grade lowers the honours band by one level."),
 ("no_honours", "An incomplete in a graded course blocks honours for the term.")],
"no_honours", 1),

# ------------------------------------------------------------------ ac13
# why: credit-weighted average = (20*68 + 20*64 + 40*50 + 40*47)/120 = (1360+1280+2000+1880)/120 = 6520/120 = 54.33 < 55 -> no.
# Simple mean 57.25 is the trap. Twin: D 50 -> 6640/120 = 55.33 -> yes.
Y("ac13", "Is the student eligible for the placement year?",
"""
Calder Hythe College — BSc Software Engineering: Placement Year Eligibility

P1. Students may take a placement year if their Year 2 credit-weighted average is at least 55.
P2. Credit-weighted average = sum of (module credits x module mark) ÷ total credits.
P3. All Year 2 modules must be passed (40 or more).
P4. An offer from an employer is needed before the placement starts, but it does not affect eligibility.

Year 2 results — student 24-1182
SWE201 Web Systems — 20 credits — 68
SWE202 Team Project — 20 credits — 64
SWE203 Algorithms — 40 credits — 50
SWE204 Databases and Security — 40 credits — 47

Placement offer: Tollmarsh Games (conditional on eligibility).
Personal tutor: "Strong practical skills; the algorithms exam was a difficult paper this year."
""",
[("eligible", "The credit-weighted average is at least 55 and every module is passed."),
 ("not_eligible", "The credit-weighted average is below 55 or a module is not passed.")],
0, 2,
twin=T([("SWE204 Databases and Security — 40 credits — 47", "SWE204 Databases and Security — 40 credits — 50")], 1)),

# ------------------------------------------------------------------ ac14
# why: poster 6 + not first conference 0 + PhD year 3 = 4 -> 10 -> partial. Earlier award July 2026 is in
# AY 2025/26; application 15 Sept 2026 is AY 2026/27 -> no deduction.
C("ac14", "What award does the travel fund scoring give this applicant?",
"""
University of Wexmoor — Doctoral Conference Travel Fund: Scoring

Points
 Type of participation: paper presentation 10; poster 6; attending only 0.
 First conference ever attended: +4.
 Stage: PhD year 1–2 +2; year 3 or later +4.
 Deduction: −6 if the applicant has already received travel funding in the same academic year as the application date. The academic year runs 1 September to 31 August.
Awards: 12 or more — full award (£600); 8–11 — partial award (£300); below 8 — no award.

Application TF-26-051 (received 15 September 2026)
Applicant: Oluwaseun Adebayo, PhD year 3, School of Geography
Event: Coastal Futures Conference, Lisbon, November 2026 — accepted for a poster
Previous conferences: attended Moorland Ecology Symposium, 2025
Previous travel funding: £300 awarded 10 July 2026
""",
[("full_award", "Presenting at the conference earns 10 points and year three adds 4, which reaches 14 and the full award."),
 ("partial_award", "The earlier award fell in the previous academic year, so the poster and year-three points total 10."),
 ("no_award", "An award earlier in the same academic year costs 6 points, leaving 4.")],
"partial_award", 2),

# ------------------------------------------------------------------ ac15
# why: overall Distinction needs practical observation = distinction AND at least one other distinction.
# Observation is Pass -> overall Pass (test 83% distinction, discussion distinction do not suffice).
# Twin: observation distinction, discussion pass -> practical + test distinction -> Distinction.
C("ac15", "What overall grade should the end-point assessment record?",
"""
Eskdale Apprenticeship Board — Maintenance Technician (Level 3): End-Point Assessment Grading

Components
1. Knowledge test: fail below 60%; pass 60–79%; distinction 80% or more.
2. Practical observation: fail / pass / distinction (assessor judgement against the criteria sheet).
3. Professional discussion: fail / pass / distinction.

Overall grade
G1. Fail if any component is failed.
G2. Distinction if the practical observation is a distinction AND at least one other component is a distinction.
G3. Otherwise, Pass.
G4. Overall grades available: Fail, Pass, Distinction.

Assessment record — apprentice Callum Rees, employer Fordwick Packaging
Knowledge test: 83%
Practical observation: pass
Professional discussion: distinction
Employer comment: "Callum has been our best apprentice this intake."
""",
[("distinction", "The practical observation is a distinction and at least one other component is too."),
 ("merit", "Two of the three components are at distinction, which earns a merit."),
 ("pass", "The practical observation is not a distinction, so distinctions in the other components are not enough."),
 ("resit_observation", "An observation graded below distinction must be resat before any overall grade can be given to the apprentice.")],
"pass", 2,
twin=T([("Practical observation: pass", "Practical observation: distinction"),
        ("Professional discussion: distinction", "Professional discussion: pass")], "distinction")),

# ------------------------------------------------------------------ ac16
# why: results Fri 3 July 2026; appeal Tue 14 July = 7 working days (<= 10); evidence dated 20 June within the
# 1-26 June assessment period -> uphold (yes). The student's "automatically upheld" belief is repeated in the twin.
# Twin: note dated 2 July -> outside the assessment period -> no.
Y("ac16", "Can the extenuating-circumstances appeal be upheld?",
"""
Northmere University — Extenuating Circumstances (EC) Appeals, Regulation 14

14.1 An EC appeal may be upheld only if:
 (a) it is submitted within 10 working days of the publication of results; and
 (b) the supporting evidence is dated within the assessment period to which the appeal relates.
14.2 Evidence dated outside the assessment period cannot support an appeal for that period.
14.3 No category of evidence leads to an automatic outcome; each appeal is decided on 14.1.

Appeal EC-26-0917
Assessment period: 1–26 June 2026 (summer examinations)
Results published: Friday 3 July 2026
Appeal submitted: Tuesday 14 July 2026
Evidence: GP letter dated 20 June 2026 describing acute illness.

Student's covering letter: "I understand appeals with a medical note are automatically upheld, so please confirm mine."
""",
[("uphold", "The appeal is in time and its evidence is dated within the assessment period."),
 ("do_not_uphold", "The appeal is late or its evidence is dated outside the assessment period.")],
1, 2,
twin=T([("GP letter dated 20 June 2026", "GP letter dated 2 July 2026")], 0)),

# ------------------------------------------------------------------ ac17
# why: Paper 2 scaled +4: 70 -> 74; average (66 + 74)/2 = 70 -> First.
C("ac17", "Which classification should the candidate receive after the board's decision?",
"""
Brantwood Institute — Graduate Diploma in Law: Examination Board Minutes, 18 June 2026

Item 4. Paper 2 (Contract), sat 4 June 2026. Question 5 was misprinted. The board resolved that every candidate's Paper 2 raw mark is increased by 4 marks (capped at 100). Paper 1 is unaffected.

Classification rule: the final mark is the average of Paper 1 and Paper 2 (as adjusted), rounded to the nearest whole number. 70+ First; 60–69 Upper second; 50–59 Lower second; below 50 Fail.

Item 6. Candidates who were absent on 4 June will sit Paper 2 in August; no candidate who sat on 4 June needs to resit.

Candidate GDL-26-118
Paper 1: 66
Paper 2 (raw): 70
Personal tutor: "Consistently strong in seminars."
""",
[("first_class", "With the board's +4 adjustment to Paper 2, the average of the two papers reaches 70."),
 ("upper_second", "With the board's +4 adjustment to Paper 2, the average falls between 60 and 69."),
 ("resit_paper_2", "A misprinted question means the candidate must resit Paper 2 before being classified.")],
"first_class", 1),

# ------------------------------------------------------------------ ac18
# why: members = registered students: 21 - 3 = 18 >= 15 -> eligible. Award = lower of £1,500 and 50% of £2,600 (£1,300) -> £1,300.
C("ac18", "How much should the Students' Union award this society?",
"""
Ravensholt University Students' Union — Society Grants Policy 2026/27

G1. Eligibility: the society must have at least 15 members. "Members" means registered students of the University; associate members (staff, alumni, local residents) are not counted.
G2. Award limit: a society may receive no more than £1,500 or 50% of its projected costs for the year, whichever is lower.
G3. Awards are not reduced for societies that received a grant in earlier years.

Application — Ravensholt Astronomy Society
Membership list: 21 names (18 registered students; 3 associate members — two alumni and one member of staff)
Projected costs 2026/27: £2,600 (telescope servicing, dark-sky trip, speaker travel)
Request: £2,000
Previous grants: £900 (2024/25), £1,100 (2025/26)
Treasurer's note: "Our costs have gone up because the coach company raised its prices."
""",
[("award_2000", "The request is below the society's projected costs for the year, so it can be met in full."),
 ("award_1500", "The £1,500 ceiling is the limit that applies to this society."),
 ("award_1300", "With 18 student members it is eligible, and 50% of costs is the lower limit."),
 ("award_0", "Counting only registered students, the society has fewer than 15 members.")],
"award_1300", 2),
]
