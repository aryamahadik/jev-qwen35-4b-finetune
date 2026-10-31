"""packs-2 lexicons, sector ed (Claude-written, v1.1 review fix): F10 attribute lexicons and statements, F7 concept sets.

Line format (parsed by build_packs.parse_lex): `key | syn: a, b | say: <frame with {E} and {v}>` for value attributes;
booleans `| pos: <positive fact> | neg: <negative fact, value word no/not> | br: .. | nr: .. | imp: ..`; tag attributes
`| say: .. | none: <the "none" statement>`. {E} is the entity reference and {v} the value as rendered with its unit.
`@fill:` lines add F7 filler Booleans (name/e = event, name/s = state).
"""

LEX = {
"ed-01": """
contact_hours | syn: instruction hours, course hours | say: {E} covers {v} of instruction
credits_claimed | syn: credit amount, credits applied for | say: {E} asks for {v}
course_fee | syn: course price, tuition for the course | say: {E} shows a course fee of {v}
days_since_completion | syn: time after the course, gap since finishing | say: {E} is dated {v} after the course ended
provider_type | syn: provider format, kind of provider | say: {E} gives the provider type as {v}
subject_link | syn: subject area, teaching subject | say: {E} relates to {v}
relevance_level | syn: duty relevance, relevance to teaching | say: {E} is rated {v} for relevance to teaching duties
certificate_attached | syn: certificate supplied, proof of completion attached | pos: {E} has a completion certificate attached | neg: {E} has no completion certificate attached | br: proof of completion | nr: signed certificate uploaded | imp: course completion
principal_endorsed | syn: principal approval given, principal sign-off | pos: {E} carries the principal's endorsement | neg: {E} does not carry the principal's endorsement | br: school approval | nr: principal signature added | imp: principal review
district_paid_fee | syn: fee paid by the district, district funding of the fee | pos: {E} had its fee paid by the district | neg: {E} did not have its fee paid by the district | br: district funding | nr: district purchase order issued | imp: fee settled
hours_verified | syn: attendance verified, hours checked | pos: {E} had its attendance hours verified | neg: {E} did not have its attendance hours verified | br: proof of attendance | nr: sign-in sheet checked | imp: attendance confirmed
counted_elsewhere | syn: hours reused, double-counted hours | pos: {E} uses hours already counted toward another credit | neg: {E} does not use hours counted toward another credit | br: duplicate credit | nr: same course claimed twice | imp: earlier credit award
completed_on | syn: completion date, course end date | say: {E} shows the course ending on {v}
submitted_on | syn: submission date, filing date | say: {E} was filed on {v}
claim_tags | syn: claim labels, claim markers | say: {E} carries the claim tags {v} | none: {E} carries none of the claim tags
credits_this_cycle | syn: cycle credit total, credits earned so far | say: {E} has earned {v} this cycle
salary_step | syn: step on the salary scale, pay grade step | say: {E} sits {v} up the salary scale
tenure_status | syn: tenure standing, contract standing | say: {E} holds {v} status
district_approved | syn: district-endorsed provider, provider approval | pos: {E} is approved by the district | neg: {E} is not approved by the district | br: provider vetting | nr: provider contract signed | imp: district review of the provider
courses_run | syn: course count, courses delivered | say: {E} shows a course count of {v}
""",
"ed-02": """
gpa | syn: grade average, academic average | say: {E} shows a grade point average of {v}
field_hours_completed | syn: field hours, practice teaching hours | say: {E} has completed {v} of field work
commute_minutes | syn: commute time, travel minutes | say: {E} shows a commute of {v}
program_fee | syn: placement charge, program charge | say: {E} carries a placement fee of {v}
certification_area | syn: licence area, teaching field | say: {E} seeks certification in {v}
grade_band | syn: grade range, age band taught | say: {E} asks for a placement in {v}
readiness_rating | syn: readiness score, readiness band | say: {E} is rated {v} for readiness
background_check_cleared | syn: background screening passed, criminal check cleared | pos: {E} has passed the background check | neg: {E} has not passed the background check | br: safety clearance | nr: fingerprint check returned | imp: clearance letter issued
tb_test_on_file | syn: tuberculosis test on file, health screening done | pos: {E} has a tuberculosis test on file | neg: {E} has no tuberculosis test on file | br: health clearance | nr: skin test read | imp: medical screening
licensure_exam_passed | syn: licensing exam passed, subject test passed | pos: {E} has passed the licensure exam | neg: {E} has not passed the licensure exam | br: subject competence | nr: passing score report | imp: exam attempt
has_own_transport | syn: own car, own vehicle | pos: {E} has its own transport to the school | neg: {E} has no own transport to the school | br: travel autonomy | nr: driving licence and car | imp: able to reach the school
relative_at_school | syn: family tie at the school, relative employed there | pos: {E} has a relative working at the school | neg: {E} has no relative working at the school | br: personal conflict of interest | nr: parent on the school staff | imp: family connection
applied_on | syn: application date, date applied | say: {E} was submitted on {v}
term_starts_on | syn: term start date, first day of term | say: {E} is for a term starting on {v}
placement_tags | syn: placement labels, placement markers | say: {E} carries the placement tags {v} | none: {E} carries none of the placement tags
earlier_placements | syn: prior placements, previous school stints | say: {E} has had {v} before
credits_completed | syn: credits finished, credit total | say: {E} has completed {v}
years_teaching | syn: teaching years, years of teaching service | say: {E} has taught for {v}
mentor_trained | syn: mentor course completed, mentor preparation done | pos: {E} has completed mentor training | neg: {E} has not completed mentor training | br: mentor readiness | nr: mentor workshop attended | imp: mentor certificate
""",
"ed-03": """
hours_notice | syn: lead time, warning given | say: {E} was posted with {v} of notice
days_long | syn: absence length, duration of the absence | say: {E} runs for {v}
periods_to_cover | syn: periods needing cover, lessons to cover | say: {E} needs {v} covered
daily_rate | syn: day rate, daily pay | say: {E} pays {v} per day
subject_area | syn: subject taught, teaching subject | say: {E} is in {v}
absence_reason | syn: reason for absence, cause of absence | say: {E} is due to {v}
coverage_urgency | syn: cover urgency, fill urgency | say: {E} is marked {v} for cover
lesson_materials_left | syn: lesson notes left, handover materials ready | pos: {E} has lesson materials left by the teacher | neg: {E} has no lesson materials left by the teacher | br: teacher handover | nr: worksheets on the desk | imp: lesson plan prepared
license_required | syn: licence needed, certified substitute needed | pos: {E} requires a licensed substitute | neg: {E} does not require a licensed substitute | br: qualification rule | nr: special education licence needed | imp: certified cover
filled_by_noon | syn: cover found by noon, filled before midday | pos: {E} was filled by noon | neg: {E} was not filled by noon | br: timely cover | nr: substitute confirmed in the morning | imp: substitute assigned
internal_cover_offered | syn: in-house cover offered, colleague volunteered | pos: {E} had internal cover offered | neg: {E} did not have internal cover offered | br: school-based cover | nr: teacher gave up a free period | imp: internal volunteer
posted_on | syn: posting date, date posted | say: {E} was posted on {v}
starts_on | syn: start date, first day of absence | say: {E} begins on {v}
absence_tags | syn: absence labels, absence markers | say: {E} carries the absence tags {v} | none: {E} carries none of the absence tags
days_worked_this_year | syn: days of service this year, assignments this year | say: {E} has worked {v} this year
rating_average | syn: average rating, principal score | say: {E} holds an average rating of {v}
certified_teacher | syn: licensed teacher, teaching certificate held | pos: {E} holds a teaching licence | neg: {E} does not hold a teaching licence | br: professional qualification | nr: state teaching certificate | imp: teacher training completed
vacancies_today | syn: absences open today, open posts today | say: {E} has {v} open today
priority_band | syn: staffing priority, staffing tier | say: {E} is in the {v} band
""",
"ed-04": """
days_past_deadline | syn: days after the deadline, lateness | say: {E} was filed {v} after the deadline
credits_after_change | syn: resulting credit load, credits after the change | say: {E} sets the credit load at {v}
section_seats_left | syn: seats left in the section, open places | say: {E} targets a section with {v} left
late_fee | syn: late charge, late add fee | say: {E} carries a late fee of {v}
petition_kind | syn: kind of petition, petition reason | say: {E} is a {v} petition
class_standing | syn: student year, academic year | say: {E} comes from a {v} student
instructor_approved | syn: instructor sign-off, instructor consent | pos: {E} has the instructor's approval | neg: {E} does not have the instructor's approval | br: faculty consent | nr: instructor signature on the form | imp: instructor review
advisor_approved | syn: advisor sign-off, advisor consent | pos: {E} has the advisor's approval | neg: {E} does not have the advisor's approval | br: academic advising | nr: advisor signature on the form | imp: advising meeting
attended_first_week | syn: in class in week one, first-week attendance | pos: {E} shows the student attended the first week | neg: {E} shows the student did not attend the first week | br: class participation | nr: roll call answered in week one | imp: early attendance
financial_hold | syn: account hold, bursar hold | pos: {E} has a financial hold on the account | neg: {E} has no financial hold on the account | br: account restriction | nr: unpaid tuition balance | imp: billing problem
academic_probation | syn: probation status, academic warning | pos: {E} concerns a student on academic probation | neg: {E} concerns a student not on academic probation | br: academic standing problem | nr: low term grades | imp: probation letter sent
filed_on | syn: filing date, date filed | say: {E} was filed on {v}
term_start | syn: term start date, first day of classes | say: {E} is for a term that began on {v}
petition_tags | syn: petition labels, petition markers | say: {E} carries the petition tags {v} | none: {E} carries none of the petition tags
gpa | syn: grade average, academic average | say: {E} holds a grade point average of {v}
petitions_this_year | syn: petitions this year, yearly petition count | say: {E} has filed {v} this year
enrolled_count | syn: enrolment count, students in the section | say: {E} has {v} enrolled
queue_length | syn: queue size, students in line | say: {E} has {v} in the queue
delivery_mode | syn: teaching format, class format | say: {E} is taught {v}
""",
"ed-05": """
lending_fee | syn: lender charge, loan fee | say: {E} carries a lending fee of {v}
pages_to_copy | syn: pages to scan, scan length | say: {E} needs {v} scanned
days_needed_by | syn: time until needed, days to deadline | say: {E} is needed within {v}
renewals_used | syn: renewal count, renewals taken | say: {E} has used {v}
item_format | syn: material type, format of the item | say: {E} is for a {v}
patron_class | syn: borrower class, patron type | say: {E} comes from a {v} borrower
delivery_speed | syn: shipping speed, delivery tier | say: {E} asks for {v} delivery
owned_locally | syn: held in the local collection, copy on our shelves | pos: {E} is for an item the library already owns | neg: {E} is for an item the library does not own | br: local holding | nr: copy on the open shelves | imp: catalogue match
copyright_limit_reached | syn: copy limit reached, copying cap reached | pos: {E} has reached the copyright limit for the journal | neg: {E} has not reached the copyright limit for the journal | br: copyright restriction | nr: fifth article copy this year | imp: fee for further copies
partner_confirmed | syn: lender agreed, partner acceptance | pos: {E} has a confirmed lending partner | neg: {E} has no confirmed lending partner | br: lender commitment | nr: shipping notice from the lender | imp: loan accepted
item_returned_late_before | syn: earlier late return, past overdue loan | pos: {E} comes from a patron who returned a loan late before | neg: {E} comes from a patron who has not returned a loan late before | br: borrowing history problem | nr: overdue partner loan | imp: late return notice
submitted_on | syn: submission date, date sent in | say: {E} was sent in on {v}
due_back_on | syn: loan due date, date the loan ends | say: {E} is due back on {v}
loan_tags | syn: loan labels, loan markers | say: {E} carries the loan tags {v} | none: {E} carries none of the loan tags
open_loans | syn: loans out, current loans | say: {E} has {v} out
fines_owed | syn: fines balance, money owed in fines | say: {E} owes {v} in fines
fill_rate | syn: filled share, success rate | say: {E} fills {v} of loans
reciprocal_agreement | syn: mutual lending agreement, reciprocal deal | pos: {E} has a reciprocal agreement with us | neg: {E} has no reciprocal agreement with us | br: partnership terms | nr: consortium membership | imp: fee waiver for loans
""",
"ed-06": """
points_contested | syn: points in question, contested score | say: {E} contests {v}
days_extension_sought | syn: extension length, extra days | say: {E} seeks {v} of extension
hours_before_due | syn: hours ahead of the due time, lead time | say: {E} was filed {v} before the due time
assignment_weight | syn: grade weight, weight in the final grade | say: {E} concerns work worth {v} of the grade
makeup_exam_fee | syn: makeup fee, resit charge | say: {E} carries a makeup fee of {v}
petition_kind | syn: kind of petition, petition reason | say: {E} is a {v} petition
evidence_kind | syn: kind of evidence, supporting document type | say: {E} is backed by a {v}
grade_band | syn: current band, mark band | say: {E} comes from a student in the {v} band
rubric_error_found | syn: rubric line wrong, wrong rubric line used | pos: {E} shows a rubric error by the grader | neg: {E} shows no rubric error by the grader | br: grading error | nr: points taken under the wrong criterion | imp: score adjustment
accommodation_on_file | syn: formal accommodation, access arrangement in place | pos: {E} comes from a student with a formal accommodation on file | neg: {E} comes from a student with no formal accommodation on file | br: support arrangement | nr: extra-time letter | imp: access office approval
submitted_on_time | syn: filed in time, timely filing | pos: {E} was filed before the deadline | neg: {E} was not filed before the deadline | br: timely petition | nr: filed the same week | imp: deadline met
earlier_extension_granted | syn: prior extension, extension already given | pos: {E} comes after an earlier extension this term | neg: {E} does not come after an earlier extension this term | br: repeat leniency | nr: second extension | imp: past petition approved
filed_on | syn: filing date, date filed | say: {E} was filed on {v}
assignment_due | syn: due date, assignment deadline | say: {E} concerns work due on {v}
petition_tags | syn: petition labels, petition markers | say: {E} carries the petition tags {v} | none: {E} carries none of the petition tags
petitions_this_term | syn: petitions so far this term, term petition count | say: {E} has filed {v} this term
course_average | syn: running grade, course mark | say: {E} holds a course average of {v}
papers_graded | syn: papers marked, grading load | say: {E} has graded {v}
calibration_done | syn: calibration finished, grading calibration completed | pos: {E} has finished grader calibration | neg: {E} has not finished grader calibration | br: grading consistency | nr: sample papers marked together | imp: calibration session
""",
"ed-07": """
placement_score | syn: test score, intake score | say: {E} shows a placement score of {v}
weeks_waiting | syn: waiting weeks, time waiting | say: {E} has waited {v}
free_hours_weekly | syn: weekly free hours, hours free per week | say: {E} has {v} free each week
materials_fee | syn: book charge, materials charge | say: {E} carries a materials fee of {v}
preferred_time | syn: class time wanted, time slot | say: {E} prefers {v} classes
learner_goal | syn: study goal, reason for study | say: {E} gives the goal as {v}
placement_level | syn: course level, class band | say: {E} places the learner at {v}
test_completed | syn: placement test done, intake test finished | pos: {E} shows the placement test completed | neg: {E} shows the placement test not completed | br: assessment done | nr: listening and reading sections scored | imp: test score issued
childcare_needed | syn: needs childcare, childcare required | pos: {E} needs childcare to attend | neg: {E} does not need childcare to attend | br: family care barrier | nr: young child at home | imp: childcare referral
residency_proof_seen | syn: proof of address seen, residence document checked | pos: {E} has had proof of residency seen | neg: {E} has not had proof of residency seen | br: eligibility check | nr: utility bill checked | imp: local address confirmed
returning_learner | syn: past learner, former student | pos: {E} is for a returning learner | neg: {E} is not for a returning learner | br: prior enrolment | nr: studied here last year | imp: past attendance history
employer_sponsored | syn: paid by employer, workplace sponsorship | pos: {E} is sponsored by an employer | neg: {E} is not sponsored by an employer | br: outside funding | nr: employer voucher | imp: employer agreement
intake_on | syn: intake date, sign-up date | say: {E} opened on {v}
class_starts_on | syn: class start date, first class day | say: {E} is for a class starting on {v}
enrolment_tags | syn: enrolment labels, enrolment markers | say: {E} carries the enrolment tags {v} | none: {E} carries none of the enrolment tags
years_schooling | syn: schooling years, years in school | say: {E} has {v} of schooling
attendance_rate | syn: attendance share, past attendance rate | say: {E} attended {v} of past classes
seats_open | syn: open seats, places free | say: {E} has {v} open
class_hours_weekly | syn: weekly class hours, contact hours per week | say: {E} meets for {v} each week
""",
"ed-08": """
child_age_months | syn: child's age, age of the child | say: {E} is for a child aged {v}
family_income | syn: household earnings, yearly income | say: {E} shows a family income of {v}
days_in_queue | syn: queue time, days queued | say: {E} has been in the queue for {v}
days_per_week | syn: care days, weekly days of care | say: {E} asks for care {v} a week
monthly_tuition | syn: monthly fee, tuition each month | say: {E} carries monthly tuition of {v}
age_group | syn: room group, age room | say: {E} is for the {v}
subsidy_band | syn: subsidy tier, aid level | say: {E} falls in the {v} band
immunizations_current | syn: vaccinations current, shots current | pos: {E} shows immunizations up to date | neg: {E} shows immunizations not up to date | br: health clearance | nr: vaccine card checked | imp: health form complete
sibling_enrolled | syn: brother or sister enrolled, sibling at the center | pos: {E} has a sibling already enrolled | neg: {E} has no sibling already enrolled | br: family priority | nr: older child in the preschool room | imp: sibling priority
staff_child | syn: child of an employee, staff family | pos: {E} is for a staff member's child | neg: {E} is not for a staff member's child | br: employee benefit | nr: teacher's child | imp: staff priority
deposit_paid | syn: deposit received, enrolment payment made | pos: {E} has its deposit paid | neg: {E} does not have its deposit paid | br: financial commitment | nr: first deposit cleared | imp: seat held
tour_completed | syn: visit made, site tour done | pos: {E} shows the family toured the center | neg: {E} shows the family did not tour the center | br: family orientation | nr: classroom walk-through | imp: center visit
applied_on | syn: application date, date applied | say: {E} was submitted on {v}
start_wanted_on | syn: wanted start date, hoped start | say: {E} asks for a start on {v}
application_tags | syn: application labels, application markers | say: {E} carries the application tags {v} | none: {E} carries none of the application tags
children_in_care | syn: children enrolled, kids in care | say: {E} has {v} in care
balance_due | syn: outstanding balance, past amount owed | say: {E} owes {v}
home_language | syn: family language, language at home | say: {E} speaks {v} at home
open_spots | syn: free spaces, open places | say: {E} has {v} open
ratio_children_per_adult | syn: child to adult ratio, children for each adult | say: {E} runs at {v} for each adult
""",
"ed-09": """
fines_balance | syn: fine total, money owed | say: {E} owes {v} in fines
items_overdue | syn: overdue count, late items | say: {E} has {v} overdue
days_most_overdue | syn: longest lateness, oldest overdue days | say: {E} has an item {v} overdue
holds_waiting | syn: holds ready, reserved items waiting | say: {E} has {v} waiting on the hold shelf
card_type | syn: kind of card, card class | say: {E} holds a {v}
contact_method | syn: contact channel, notice method | say: {E} is reached by {v}
account_tier | syn: borrowing level, card tier | say: {E} sits at the {v} tier
address_updated | syn: address refreshed, address confirmed this year | pos: {E} had its address updated this year | neg: {E} did not have its address updated this year | br: contact details current | nr: new address form | imp: mail bounced before the update
lost_item_billed | syn: lost item charge, replacement bill sent | pos: {E} was billed for a lost item | neg: {E} was not billed for a lost item | br: account charge | nr: replacement cost invoice | imp: item declared lost
guardian_signed | syn: guardian signature, parent signature | pos: {E} has a guardian signature on file | neg: {E} has no guardian signature on file | br: guardian consent | nr: parent signed the card form | imp: minor account
collections_referral | syn: sent to collections, collection agency referral | pos: {E} has been referred to collections | neg: {E} has not been referred to collections | br: debt recovery | nr: agency letter mailed | imp: large unpaid balance
card_renewed | syn: card refreshed, renewal done | pos: {E} had its card renewed on time | neg: {E} did not have its card renewed on time | br: account upkeep | nr: renewal at the desk | imp: valid card
last_visit_on | syn: last visit date, most recent visit | say: {E} was last used on {v}
card_expires_on | syn: card expiry date, expiry | say: {E} holds a card that expires on {v}
account_tags | syn: account labels, account markers | say: {E} carries the account tags {v} | none: {E} carries none of the account tags
patron_age | syn: age of the patron, borrower age | say: {E} is {v} old
items_borrowed_this_year | syn: loans this year, yearly borrowing | say: {E} has borrowed {v} this year
replacement_cost | syn: cost to replace, replacement price | say: {E} costs {v} to replace
loan_period_days | syn: loan length, borrowing period | say: {E} lends for {v}
""",
"ed-10": """
credits_earned | syn: credit total, credits passed | say: {E} shows {v} earned
credits_required | syn: credits needed, credit target | say: {E} requires {v} to graduate
service_hours | syn: volunteer hours, service time | say: {E} shows {v} of community service
math_credits | syn: mathematics credits, math units | say: {E} shows {v} in mathematics
cap_and_gown_fee | syn: gown fee, ceremony charge | say: {E} carries a cap and gown fee of {v}
diploma_track | syn: diploma type, graduation track | say: {E} is for a {v}
exit_exam_result | syn: exit exam score band, final exam band | say: {E} shows an exit exam result of {v}
senior_project_done | syn: capstone done, senior project complete | pos: {E} shows the senior project done | neg: {E} shows the senior project not done | br: graduation project | nr: capstone presentation given | imp: project grade entered
recovery_course_active | syn: credit recovery under way, recovery class open | pos: {E} has a credit recovery course in progress | neg: {E} has no credit recovery course in progress | br: credit shortfall | nr: online recovery module | imp: failed course earlier
transcript_from_transfer_received | syn: transfer transcript received, prior school transcript in | pos: {E} has the transfer transcript received | neg: {E} does not have the transfer transcript received | br: prior coursework | nr: sealed transcript from the old school | imp: transfer credits
fees_cleared | syn: fees settled, school fees paid | pos: {E} shows school fees cleared | neg: {E} shows school fees not cleared | br: account in good standing | nr: lab fee paid | imp: zero fee balance
parent_meeting_held | syn: family meeting held, parent conference done | pos: {E} shows a parent meeting held | neg: {E} shows no parent meeting held | br: family contact | nr: conference with the counselor | imp: parent informed
audited_on | syn: audit date, review date | say: {E} was audited on {v}
ceremony_on | syn: ceremony date, graduation day | say: {E} is for a ceremony on {v}
audit_tags | syn: audit labels, audit markers | say: {E} carries the audit tags {v} | none: {E} carries none of the audit tags
attendance_rate | syn: attendance share, presence rate | say: {E} attended {v} of school days
gpa | syn: grade average, academic average | say: {E} holds a grade point average of {v}
post_graduation_path | syn: plan after school, next step after graduation | say: {E} names {v} as the next step
caseload | syn: student load, assigned students | say: {E} carries a caseload of {v}
years_in_role | syn: counseling years, years as a counselor | say: {E} has worked {v} in the role
""",
}
