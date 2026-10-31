"""packs-2 lexicons, sector hr (Claude-written, v1.1 review fix). Line format: see src/lex_ed.py."""

LEX = {
"hr-01": """
months_employed | syn: service length in months, time with the company | say: {E} concerns an employee with {v} of service
hours_worked_last_year | syn: hours in the past year, annual hours worked | say: {E} shows {v} worked in the past year
weeks_requested | syn: leave length, weeks of leave asked | say: {E} asks for {v} of leave
weeks_used_this_year | syn: leave already taken, weeks taken this year | say: {E} shows {v} already taken this year
days_notice | syn: notice period, advance notice | say: {E} was raised with {v} of notice
weekly_pay_continued | syn: pay during leave, continued wages | say: {E} keeps {v} of weekly pay
leave_reason | syn: reason for leave, cause of leave | say: {E} is for {v}
leave_pattern | syn: leave schedule type, leave shape | say: {E} is taken as {v} leave
urgency | syn: notice category, leave urgency | say: {E} is classed as {v}
certification_received | syn: medical certification returned, doctor's form back | pos: {E} has its certification received | neg: {E} does not have its certification received | br: medical support | nr: physician form signed | imp: leave reason proven
eligibility_notice_sent | syn: eligibility letter issued, rights notice sent | pos: {E} has had its eligibility notice sent | neg: {E} has not had its eligibility notice sent | br: employer notice duty | nr: letter emailed within five days | imp: employee informed
paid_time_off_applied | syn: paid leave used alongside, vacation applied | pos: {E} has paid time off applied | neg: {E} does not have paid time off applied | br: wage replacement | nr: vacation days drawn | imp: pay continues
key_employee | syn: designated key employee, top earner role | pos: {E} concerns a key employee | neg: {E} does not concern a key employee | br: restoration exception | nr: highest paid tenth of staff | imp: job restoration at stake
return_date_confirmed | syn: return date agreed, back-to-work date set | pos: {E} has a confirmed return date | neg: {E} has no confirmed return date | br: return planning | nr: manager agreed the date | imp: cover can end
starts_on | syn: leave start date, first day of leave | say: {E} starts on {v}
ends_on | syn: leave end date, last day of leave | say: {E} ends on {v}
leave_tags | syn: leave labels, leave markers | say: {E} carries the leave tags {v} | none: {E} carries none of the leave tags
leave_cases_last_two_years | syn: earlier leave cases, past leaves | say: {E} has had {v} in two years
job_family | syn: job group, work group | say: {E} works in {v}
team_absences_now | syn: team members away, current absences | say: {E} has {v} away now
""",
"hr-02": """
days_overdue | syn: days past the due date, lateness | say: {E} is {v} past due
course_hours | syn: course length, training hours | say: {E} takes {v}
attempts_used | syn: test tries, attempts taken | say: {E} has used {v}
course_cost | syn: course fee, training cost | say: {E} costs {v}
score_percent | syn: test score, assessment score | say: {E} scored {v}
course_family | syn: course area, training area | say: {E} is a {v} course
delivery | syn: delivery mode, training format | say: {E} is delivered by {v}
criticality | syn: course importance, compliance weight | say: {E} is graded {v}
grace_extension_granted | syn: grace period approved, deadline extension | pos: {E} has a grace extension granted | neg: {E} has no grace extension granted | br: deadline relief | nr: thirty extra days approved | imp: later due date
practical_assessed | syn: practical check done, skills check passed | pos: {E} has had a practical assessment | neg: {E} has not had a practical assessment | br: hands-on competence | nr: observed vehicle check | imp: skills proven
supervisor_verified | syn: supervisor sign-off, verified by the supervisor | pos: {E} has been verified by a supervisor | neg: {E} has not been verified by a supervisor | br: supervisory approval | nr: supervisor initials on the sheet | imp: completion accepted
on_restricted_duty | syn: duty restriction, work limitation | pos: {E} concerns staff on restricted duty | neg: {E} concerns staff not on restricted duty | br: fitness limit | nr: barred from driving routes | imp: reduced duties
seat_reserved | syn: class seat held, place booked | pos: {E} has a seat reserved in the next class | neg: {E} has no seat reserved in the next class | br: training booking | nr: roster spot confirmed | imp: retraining arranged
completed_on | syn: completion date, finish date | say: {E} was completed on {v}
due_on | syn: due date, deadline | say: {E} is due on {v}
file_tags | syn: file labels, training markers | say: {E} carries the file tags {v} | none: {E} carries none of the file tags
years_service | syn: service years, years employed | say: {E} has served {v}
overdue_courses | syn: late courses, courses past due | say: {E} has {v} overdue
seats_per_session | syn: class size, places per session | say: {E} seats {v} per session
""",
"hr-03": """
months_on_assignment | syn: time on assignment, assignment length | say: {E} has run {v} so far
months_added | syn: extension length, added term | say: {E} adds {v}
hourly_bill_rate | syn: billing rate, rate per hour | say: {E} bills at {v} an hour
rate_increase_percent | syn: rate rise, increase asked | say: {E} raises the rate by {v}
budget_remaining | syn: budget left, project funds left | say: {E} draws on a budget with {v} left
role_family | syn: role type, job family | say: {E} is for a {v}
engagement_type | syn: contract model, engagement model | say: {E} runs on {v} terms
performance_rating | syn: manager rating, performance grade | say: {E} is rated {v}
statement_of_work_signed | syn: work order signed, SOW signed | pos: {E} has a signed statement of work | neg: {E} does not have a signed statement of work | br: contract paperwork | nr: countersigned work order | imp: scope agreed
conversion_offered | syn: permanent offer made, conversion offer | pos: {E} has had a conversion offered | neg: {E} has not had a conversion offered | br: hiring path | nr: offer letter for a staff role | imp: contractor may leave the agency
budget_owner_approved | syn: budget holder approval, cost owner sign-off | pos: {E} has the budget owner's approval | neg: {E} does not have the budget owner's approval | br: financial approval | nr: cost center owner email | imp: funds committed
badge_access_active | syn: building access live, badge working | pos: {E} has active badge access | neg: {E} does not have active badge access | br: site access | nr: door reader accepts the badge | imp: contractor on site
tenure_cap_reached | syn: tenure limit hit, maximum tenure reached | pos: {E} has reached the tenure cap | neg: {E} has not reached the tenure cap | br: co-employment concern | nr: eighteen-month ceiling hit | imp: break in service needed
started_on | syn: start date, assignment start | say: {E} began on {v}
current_end_on | syn: current end date, present end | say: {E} currently ends on {v}
extension_tags | syn: extension labels, extension markers | say: {E} carries the extension tags {v} | none: {E} carries none of the extension tags
prior_assignments | syn: earlier assignments, past placements here | say: {E} has had {v} here before
markup_percent | syn: agency margin, markup | say: {E} charges a markup of {v}
""",
"hr-04": """
tuition_paid | syn: tuition cost, course tuition | say: {E} shows tuition of {v}
paid_this_year | syn: reimbursed this year, yearly payout so far | say: {E} has already received {v} this year
credit_hours | syn: course credits, credit load | say: {E} covers {v}
days_since_course_end | syn: days after the course, time since the course | say: {E} was filed {v} after the course ended
months_employed | syn: months of service, time with the employer | say: {E} comes from an employee with {v} of service
course_level | syn: degree level, program level | say: {E} is for a {v} course
job_relevance | syn: link to the job, job fit | say: {E} relates to the {v}
grade_earned | syn: course grade, final mark | say: {E} shows a grade of {v}
preapproval_granted | syn: approved ahead, advance approval | pos: {E} had preapproval granted | neg: {E} did not have preapproval granted | br: program approval | nr: course form approved before enrolment | imp: course eligible
receipt_attached | syn: proof of payment attached, receipt supplied | pos: {E} has a receipt attached | neg: {E} has no receipt attached | br: payment evidence | nr: school invoice marked paid | imp: tuition cost proven
repayment_agreement_signed | syn: stay-or-repay signed, clawback agreement signed | pos: {E} has a signed repayment agreement | neg: {E} does not have a signed repayment agreement | br: retention commitment | nr: two-year stay clause | imp: repayment owed on early exit
employer_grant_used | syn: outside grant paid, other funding used | pos: {E} is also covered by an outside grant | neg: {E} is not also covered by an outside grant | br: double funding | nr: state scholarship paid | imp: reduced reimbursement
manager_endorsed | syn: manager supported it, manager approval | pos: {E} carries the manager's endorsement | neg: {E} does not carry the manager's endorsement | br: management support | nr: manager signature on the claim | imp: business need shown
course_ended_on | syn: course end date, last class date | say: {E} is for a course that ended on {v}
claimed_on | syn: claim date, filing date | say: {E} was filed on {v}
claim_tags | syn: claim labels, claim markers | say: {E} carries the claim tags {v} | none: {E} carries none of the claim tags
performance_band | syn: review band, performance grade | say: {E} sits in the {v} band
accredited | syn: recognized school, school accreditation | pos: {E} is accredited | neg: {E} is not accredited | br: quality assurance | nr: regional accreditor approval | imp: credits transferable
""",
"hr-05": """
days_since_event | syn: days after the event, time since the change | say: {E} was reported {v} after it happened
dependents_added | syn: new dependents, people added | say: {E} adds {v}
dependents_removed | syn: dependents dropped, people removed | say: {E} removes {v}
premium_change | syn: deduction change, cost change | say: {E} changes the monthly deduction by {v}
event_type | syn: kind of event, change type | say: {E} is a {v}
coverage_tier | syn: coverage level, enrolment tier | say: {E} moves to {v} coverage
proof_received | syn: supporting document received, evidence received | pos: {E} has proof received | neg: {E} does not have proof received | br: event evidence | nr: birth certificate copy | imp: change can be checked
election_consistent | syn: election matches the event, change consistent | pos: {E} has an election consistent with the event | neg: {E} does not have an election consistent with the event | br: rule compliance | nr: spouse added after marriage | imp: change allowed
carrier_file_sent | syn: carrier file transmitted, enrolment sent | pos: {E} has its file sent to the carrier | neg: {E} does not have its file sent to the carrier | br: carrier update | nr: weekly feed included the change | imp: carrier informed
spouse_has_other_cover | syn: spouse insured elsewhere, spouse's own insurance | pos: {E} involves a spouse with other cover | neg: {E} involves a spouse with no other cover | br: other insurance | nr: spouse's employer plan | imp: spousal surcharge question
tobacco_attestation | syn: tobacco surcharge, tobacco declaration | pos: {E} carries a tobacco attestation | neg: {E} does not carry a tobacco attestation | br: surcharge trigger | nr: smoker box ticked | imp: higher premium
event_on | syn: event date, date of the change | say: {E} happened on {v}
reported_on | syn: report date, date reported | say: {E} was reported on {v}
event_tags | syn: event labels, event markers | say: {E} carries the event tags {v} | none: {E} carries none of the event tags
salary_band | syn: pay band, salary grade | say: {E} sits in {v}
union_member | syn: union-covered, bargaining unit member | pos: {E} is a union member | neg: {E} is not a union member | br: collective coverage | nr: dues deducted | imp: contract benefits apply
file_turnaround_days | syn: processing time, carrier turnaround | say: {E} processes files in {v}
carrier_region | syn: carrier reach, service area | say: {E} is a {v} carrier
""",
"hr-06": """
duties_changed_percent | syn: share of duties changed, duty change | say: {E} shows {v} of duties changed
current_salary | syn: present pay, current pay rate | say: {E} concerns a current salary of {v}
proposed_increase_percent | syn: proposed raise, pay rise asked | say: {E} proposes a rise of {v}
months_in_new_duties | syn: time in new duties, months doing the work | say: {E} shows {v} in the new duties
positions_affected | syn: positions covered, posts affected | say: {E} covers {v}
review_reason | syn: reason for review, review cause | say: {E} was opened for {v}
proposed_grade_step | syn: grade change, step change | say: {E} proposes {v}
desk_audit_done | syn: desk audit held, job audit completed | pos: {E} has had a desk audit | neg: {E} has not had a desk audit | br: job analysis | nr: analyst observed the work | imp: duties documented
department_head_endorsed | syn: department head support, director endorsement | pos: {E} carries the department head's endorsement | neg: {E} does not carry the department head's endorsement | br: management support | nr: signed endorsement memo | imp: department backing
budget_funded | syn: money in the budget, funds set aside | pos: {E} is funded in the budget | neg: {E} is not funded in the budget | br: financial cover | nr: salary line reserved | imp: raise affordable
union_consulted | syn: union informed, union notice given | pos: {E} has had the union consulted | neg: {E} has not had the union consulted | br: labor consultation | nr: steward meeting held | imp: bargaining duty met
temporary_duties_only | syn: short-term duties, interim duties | pos: {E} concerns temporary duties only | neg: {E} does not concern temporary duties only | br: acting assignment | nr: cover for a vacancy | imp: temporary pay instead
submitted_on | syn: submission date, date sent | say: {E} was submitted on {v}
effective_on | syn: effective date, start of new pay | say: {E} takes effect on {v}
review_tags | syn: review labels, review markers | say: {E} carries the review tags {v} | none: {E} carries none of the review tags
years_in_position | syn: years in the job, time in post | say: {E} has held the job for {v}
bargaining_status | syn: union status, bargaining unit | say: {E} is {v}
pay_range_max | syn: range maximum, top of the pay range | say: {E} tops out at {v}
""",
"hr-07": """
base_salary | syn: offered pay, salary offered | say: {E} offers a base salary of {v}
range_position_percent | syn: place in the range, range position | say: {E} sits at {v} of the pay range
signing_bonus | syn: sign-on bonus, joining bonus | say: {E} adds a signing bonus of {v}
interviews_completed | syn: interviews held, interview rounds | say: {E} follows {v} of interviews
days_req_open | syn: days the job has been open, vacancy age | say: {E} fills a job open for {v}
job_level | syn: role level, job grade | say: {E} is for a {v} role
employment_type | syn: work pattern, contract type | say: {E} is for a {v} job
scorecard_rating | syn: interview rating, panel rating | say: {E} follows a {v} rating
headcount_approved | syn: headcount in budget, approved position | pos: {E} has approved headcount | neg: {E} does not have approved headcount | br: budget approval | nr: position number assigned | imp: hire allowed
references_cleared | syn: references checked, reference checks done | pos: {E} has references cleared | neg: {E} does not have references cleared | br: candidate vetting | nr: two former managers called | imp: work history confirmed
background_check_passed | syn: background check cleared, screening passed | pos: {E} has a background check passed | neg: {E} does not have a background check passed | br: candidate screening | nr: criminal check returned | imp: safe to hire
relocation_needed | syn: candidate must move, move needed | pos: {E} needs the candidate to relocate | neg: {E} does not need the candidate to relocate | br: added hiring cost | nr: cross-country move | imp: relocation package
counteroffer_present | syn: rival offer, competing offer | pos: {E} faces a counteroffer | neg: {E} faces no counteroffer | br: candidate leverage | nr: current employer raise | imp: pressure to raise pay
opened_on | syn: opening date, date the job opened | say: {E} was opened on {v}
start_on | syn: start date, first day | say: {E} begins on {v}
offer_tags | syn: offer labels, offer markers | say: {E} carries the offer tags {v} | none: {E} carries none of the offer tags
years_experience | syn: work experience, career years | say: {E} has {v} of experience
open_reqs | syn: open jobs, jobs open on the team | say: {E} has {v} open
""",
"hr-08": """
estimated_cost | syn: cost estimate, change cost | say: {E} is estimated at {v}
days_open | syn: case age, time open | say: {E} has been open for {v}
meetings_held | syn: meetings so far, interactive sessions | say: {E} has had {v}
hours_change_per_week | syn: weekly hours change, schedule change in hours | say: {E} changes weekly hours by {v}
accommodation_type | syn: kind of adjustment, adjustment type | say: {E} asks for {v}
duration_kind | syn: duration, length of the arrangement | say: {E} is {v}
complexity | syn: case complexity, difficulty | say: {E} is rated {v}
medical_form_received | syn: health form returned, medical paperwork in | pos: {E} has its medical form received | neg: {E} does not have its medical form received | br: medical support | nr: provider questionnaire returned | imp: need shown
manager_consulted | syn: manager took part, manager input given | pos: {E} has had the manager consulted | neg: {E} has not had the manager consulted | br: interactive process step | nr: manager joined the meeting | imp: job needs reviewed
trial_period_set | syn: trial arrangement agreed, pilot period set | pos: {E} has a trial period set | neg: {E} has no trial period set | br: phased approach | nr: thirty-day trial | imp: follow-up review
essential_function_affected | syn: core duty affected, essential task affected | pos: {E} affects an essential function | neg: {E} does not affect an essential function | br: job redesign issue | nr: lifting duty removed | imp: hardship question
alternative_offered | syn: another option offered, substitute arrangement | pos: {E} has had an alternative offered | neg: {E} has not had an alternative offered | br: good faith effort | nr: different chair offered | imp: choice for the employee
opened_on | syn: opening date, intake date | say: {E} was opened on {v}
review_on | syn: review date, follow-up date | say: {E} comes up for review on {v}
case_tags | syn: case labels, case markers | say: {E} carries the case tags {v} | none: {E} carries none of the case tags
tenure_years | syn: years of service, service length | say: {E} has worked {v} here
team_size | syn: team headcount, direct reports | say: {E} leads {v}
""",
"hr-09": """
hours_rest_between | syn: rest gap, rest hours between shifts | say: {E} leaves {v} of rest between shifts
weekly_hours_after | syn: hours in the week after the change, weekly total | say: {E} brings the week to {v}
overtime_hours | syn: extra hours, overtime added | say: {E} adds {v} of overtime
overtime_cost | syn: overtime pay, extra pay cost | say: {E} costs {v} in overtime
staff_on_shift_after | syn: staffing after the change, people on shift | say: {E} leaves {v} on the shift
change_kind | syn: kind of change, change type | say: {E} is a {v}
skill_match | syn: skill fit, partner fit | say: {E} has a {v} skill match
partner_agreed | syn: other worker agreed, swap partner consent | pos: {E} has the partner's agreement | neg: {E} does not have the partner's agreement | br: mutual consent | nr: partner signed the form | imp: swap runs both ways
supervisor_notified_early | syn: two days' notice given, early supervisor notice | pos: {E} was raised with the supervisor two days ahead | neg: {E} was not raised with the supervisor two days ahead | br: advance notice | nr: message sent two days before | imp: roster can adjust
minimum_staffing_met | syn: minimum staffing kept, staffing floor met | pos: {E} keeps minimum staffing | neg: {E} does not keep minimum staffing | br: service coverage | nr: three processors on the floor | imp: queue covered
overtime_budget_left | syn: overtime funds remain, overtime money left | pos: {E} has overtime budget left | neg: {E} has no overtime budget left | br: cost headroom | nr: monthly overtime allowance | imp: overtime affordable
fatigue_flag | syn: fatigue rule triggered, tiredness alert | pos: {E} triggers the fatigue rule | neg: {E} does not trigger the fatigue rule | br: health and safety concern | nr: shift after a night shift | imp: rest needed
submitted_on | syn: submission date, date sent | say: {E} was submitted on {v}
shift_on | syn: shift date, day of the shift | say: {E} is for a shift on {v}
swap_tags | syn: swap labels, swap markers | say: {E} carries the swap tags {v} | none: {E} carries none of the swap tags
swaps_this_month | syn: monthly swaps, swaps so far this month | say: {E} has made {v} this month
team_name | syn: work team, unit | say: {E} works on the {v}
overtime_this_month | syn: overtime so far, monthly overtime | say: {E} has worked {v} of overtime this month
""",
"hr-10": """
days_since_incident | syn: days after the incident, incident age | say: {E} was filed {v} after the incident
days_to_respond | syn: answer window left, response days left | say: {E} has {v} left for an answer
step_reached | syn: grievance step, contract step | say: {E} has reached step {v}
back_pay_claimed | syn: back wages sought, pay claimed | say: {E} claims {v} in back pay
grievants | syn: workers covered, grievant count | say: {E} covers {v}
subject | syn: topic, issue type | say: {E} concerns {v}
remedy_sought | syn: remedy asked, relief sought | say: {E} seeks {v}
severity_level | syn: seriousness, issue severity | say: {E} is rated {v}
filed_within_limit | syn: filed in time, inside the time limit | pos: {E} was filed within the time limit | neg: {E} was not filed within the time limit | br: procedural compliance | nr: filed inside ten working days | imp: case can proceed
step_meeting_held | syn: step meeting took place, hearing held | pos: {E} has had its step meeting held | neg: {E} has not had its step meeting held | br: contract procedure | nr: meeting minutes signed | imp: management heard the case
written_answer_sent | syn: management answer sent, written reply sent | pos: {E} has a written answer sent | neg: {E} does not have a written answer sent | br: management response | nr: answer letter dated | imp: clock for appeal starts
past_practice_cited | syn: union cites practice, past practice argued | pos: {E} cites past practice | neg: {E} does not cite past practice | br: custom argument | nr: ten years of the same rota | imp: practice binding question
class_action | syn: group grievance, covers many workers | pos: {E} is a class grievance | neg: {E} is not a class grievance | br: collective dispute | nr: whole shift named | imp: wider remedy
incident_on | syn: incident date, date of the incident | say: {E} concerns an incident on {v}
filed_on | syn: filing date, date filed | say: {E} was filed on {v}
grievance_tags | syn: grievance labels, grievance markers | say: {E} carries the grievance tags {v} | none: {E} carries none of the grievance tags
open_grievances | syn: cases carried, open cases | say: {E} carries {v}
grievances_this_year | syn: grievances this year, yearly grievance count | say: {E} has faced {v} this year
""",
}
