"""packs-2 lexicons, sector hc (Claude-written, v1.1 review fix). Line format: see src/lex_ed.py."""

LEX = {
"hc-01": """
trip_miles | syn: ride length, mileage | say: {E} covers a trip distance of {v}
fare_quote | syn: ride price, fare estimate | say: {E} carries a quoted fare of {v}
days_until_visit | syn: days to the visit, booking lead | say: {E} comes {v} before the visit
riders_in_party | syn: passengers, people riding | say: {E} carries {v}
visit_type | syn: appointment type, kind of visit | say: {E} is for a {v} visit
mobility_need | syn: mobility support, rider mobility | say: {E} gives the rider's mobility as {v}
appointment_confirmed | syn: appointment verified, visit booking confirmed | pos: {E} has a confirmed appointment | neg: {E} has no confirmed appointment | br: visit readiness | nr: clinic called back to confirm | imp: appointment booked
address_verified | syn: pickup address confirmed, address check done | pos: {E} had its pickup address verified | neg: {E} did not have its pickup address verified | br: pickup readiness | nr: map check of the address | imp: driver can find the rider
escort_approved | syn: companion approved, escort permission | pos: {E} has an approved escort | neg: {E} has no approved escort | br: companion travel | nr: caregiver seat granted | imp: extra rider allowed
late_cancellation_logged | syn: late cancel on file, prior late cancel | pos: {E} comes from a rider with a late cancellation logged | neg: {E} comes from a rider with no late cancellation logged | br: rider history problem | nr: cancel within an hour of pickup | imp: wasted trip
trip_received_on | syn: date received, intake date | say: {E} came in on {v}
visit_date | syn: appointment date, clinic date | say: {E} is for a visit on {v}
trip_tags | syn: trip labels, ride markers | say: {E} carries the trip tags {v} | none: {E} carries none of the trip tags
rides_used_this_month | syn: rides this month, monthly trips | say: {E} has used {v} this month
household_size | syn: household members, family size | say: {E} lives in a household of {v}
enrollment_tier | syn: benefit tier, support tier | say: {E} is enrolled at the {v} tier
program_enrolled | syn: enrolled in the ride program, ride benefit active | pos: {E} is enrolled in the ride program | neg: {E} is not enrolled in the ride program | br: benefit eligibility | nr: enrollment card issued | imp: rides covered
vendor_rating | syn: vendor grade, service score | say: {E} holds a rating of {v}
on_time_rate | syn: punctual share, on-time share | say: {E} arrives on time {v} of the time
vendor_contract_active | syn: vendor agreement current, contract live | pos: {E} has an active contract | neg: {E} does not have an active contract | br: vendor eligibility | nr: signed service agreement | imp: trips can be booked
""",
"hc-02": """
stipend_amount | syn: visit payment, participant stipend | say: {E} pays a stipend of {v}
travel_claimed | syn: travel costs claimed, travel reimbursement | say: {E} claims {v} for travel
visit_number | syn: visit sequence, visit count | say: {E} is for visit {v}
days_since_visit | syn: time since the visit, days after the visit | say: {E} comes {v} after the visit
visit_window_days | syn: visit window, allowed window | say: {E} allows a visit window of {v}
visit_kind | syn: visit phase, kind of study visit | say: {E} is for a {v} visit
payment_method | syn: payout method, way of paying | say: {E} is paid by {v}
visit_completed | syn: visit finished, study visit done | pos: {E} shows the visit completed | neg: {E} shows the visit not completed | br: protocol compliance | nr: case report form signed | imp: stipend earned
receipt_attached | syn: proof of expense, receipt supplied | pos: {E} has a receipt attached | neg: {E} has no receipt attached | br: expense evidence | nr: parking stub attached | imp: travel cost proven
overnight_stay | syn: night away, hotel stay | pos: {E} includes an overnight stay | neg: {E} does not include an overnight stay | br: extended visit | nr: hotel night booked | imp: lodging cost
line_paid_before | syn: duplicate payment, line already paid | pos: {E} was paid once before | neg: {E} was not paid before | br: payment error | nr: same line paid twice | imp: overpayment
visit_on | syn: visit date, date of visit | say: {E} is for a visit on {v}
line_created_on | syn: creation date, line date | say: {E} was created on {v}
line_tags | syn: line labels, expense markers | say: {E} carries the line tags {v} | none: {E} carries none of the line tags
year_to_date_paid | syn: paid so far this year, yearly total paid | say: {E} has been paid {v} this year
consent_version | syn: consent edition, form version | say: {E} signed consent version {v}
tax_form_on_file | syn: tax paperwork received, tax form held | pos: {E} has a tax form on file | neg: {E} has no tax form on file | br: tax compliance | nr: taxpayer number form | imp: payments reportable
withdrawn_from_study | syn: left the study, study withdrawal | pos: {E} has withdrawn from the study | neg: {E} has not withdrawn from the study | br: participation ended | nr: withdrawal letter | imp: visits stopped
per_visit_cap | syn: visit cap, maximum stipend | say: {E} caps stipends at {v} per visit
enrolled_count | syn: participants enrolled, enrolment size | say: {E} has {v} enrolled
""",
"hc-03": """
notice_hours | syn: lead time, warning given | say: {E} was changed with {v} of notice
slot_minutes | syn: slot length, visit length | say: {E} takes a slot of {v}
reschedules_so_far | syn: times rebooked, rebooking count | say: {E} has been moved {v}
late_fee | syn: cancellation charge, late cancel fee | say: {E} carries a late fee of {v}
visit_category | syn: kind of visit, appointment kind | say: {E} is a {v} visit
booking_channel | syn: booking route, booking source | say: {E} was booked by {v}
reminder_sent | syn: reminder delivered, reminder call made | pos: {E} had a reminder sent | neg: {E} did not have a reminder sent | br: patient outreach | nr: text reminder sent | imp: patient informed
arrived_on_time | syn: punctual arrival, checked in on time | pos: {E} shows the patient arrived on time | neg: {E} shows the patient did not arrive on time | br: attendance | nr: kiosk check-in before the slot | imp: visit started on time
interpreter_booked | syn: interpreter arranged, language support booked | pos: {E} has an interpreter booked | neg: {E} has no interpreter booked | br: language access | nr: phone interpreter line reserved | imp: visit in the patient's language
prepayment_received | syn: deposit taken, advance payment | pos: {E} has a prepayment received | neg: {E} has no prepayment received | br: financial commitment | nr: card deposit charged | imp: slot secured
booked_on | syn: booking date, date booked | say: {E} was booked on {v}
appointment_on | syn: appointment date, visit date | say: {E} is set for {v}
slot_tags | syn: slot labels, slot markers | say: {E} carries the slot tags {v} | none: {E} carries none of the slot tags
missed_visits_last_year | syn: skipped visits last year, missed appointments | say: {E} missed {v} last year
account_balance | syn: open balance, amount owed | say: {E} owes {v}
portal_active | syn: portal in use, online account active | pos: {E} uses the patient portal | neg: {E} does not use the patient portal | br: digital access | nr: portal login this month | imp: online messages possible
open_slots_this_week | syn: free slots, openings this week | say: {E} has {v} open this week
provider_grade | syn: seniority, clinician grade | say: {E} is a {v}
""",
"hc-04": """
a1c_value | syn: glucose average, hemoglobin test value | say: {E} shows a latest A1C of {v}
days_in_queue | syn: queue time, days queued | say: {E} has been queued for {v}
sessions_attended_before | syn: past sessions, sessions already attended | say: {E} has attended {v} before
class_fee | syn: course fee, series charge | say: {E} carries a class fee of {v}
preferred_language | syn: language of teaching, class language | say: {E} prefers classes in {v}
session_format | syn: class format, delivery format | say: {E} asks for {v} sessions
readiness_stage | syn: change stage, readiness phase | say: {E} places the learner at the {v} stage
physician_signed | syn: doctor signature, physician sign-off | pos: {E} carries a physician's signature | neg: {E} does not carry a physician's signature | br: medical authorization | nr: doctor signed the referral form | imp: clinical approval
meter_supplied | syn: glucose meter supplied, meter on hand | pos: {E} has a glucose meter supplied | neg: {E} has no glucose meter supplied | br: self-testing readiness | nr: meter and strips given | imp: home testing possible
fee_assistance_granted | syn: fee help approved, financial aid granted | pos: {E} has fee assistance granted | neg: {E} has no fee assistance granted | br: cost support | nr: charity care approval | imp: reduced fee
caregiver_attending | syn: family member attending, support person joining | pos: {E} has a caregiver attending | neg: {E} has no caregiver attending | br: family support | nr: spouse joining the class | imp: extra seat used
referred_on | syn: referral date, date referred | say: {E} was referred on {v}
cohort_start | syn: cohort start date, first class date | say: {E} is for a cohort starting {v}
referral_tags | syn: referral labels, referral markers | say: {E} carries the referral tags {v} | none: {E} carries none of the referral tags
age_years | syn: learner age, years of age | say: {E} is {v} old
travel_minutes | syn: travel time, trip minutes | say: {E} travels {v} to class
contact_verified | syn: phone checked, contact details confirmed | pos: {E} has verified contact details | neg: {E} does not have verified contact details | br: reachable learner | nr: call-back answered | imp: reminders possible
seats_left | syn: free seats, places left | say: {E} has {v} left
cohort_size_cap | syn: seat cap, class cap | say: {E} is capped at {v}
""",
"hc-05": """
estimated_charges | syn: charge estimate, expected bill | say: {E} estimates charges of {v}
patient_share_estimate | syn: patient portion, out-of-pocket amount | say: {E} estimates the patient share at {v}
days_before_visit | syn: lead time, days to the visit | say: {E} was opened {v} before the visit
call_attempts | syn: calls made, outreach attempts | say: {E} shows {v} of calls
coverage_type | syn: insurance type, plan type | say: {E} is covered by a {v}
visit_class | syn: visit category, admission class | say: {E} is for a {v} visit
coverage_confirmed | syn: eligibility confirmed, insurance check done | pos: {E} has coverage confirmed | neg: {E} does not have coverage confirmed | br: insurance clearance | nr: eligibility reply from the payer | imp: benefits on hand
deposit_collected | syn: deposit received, upfront payment | pos: {E} has a deposit collected | neg: {E} has no deposit collected | br: financial clearance | nr: card deposit taken | imp: lower balance at the visit
consent_packet_signed | syn: consent forms signed, paperwork complete | pos: {E} has a signed consent packet | neg: {E} does not have a signed consent packet | br: legal readiness | nr: financial policy signed | imp: forms complete
identity_document_seen | syn: identity checked, photo ID seen | pos: {E} has had an identity document seen | neg: {E} has not had an identity document seen | br: identity proofing | nr: driver licence scanned | imp: patient identity confirmed
second_coverage_present | syn: secondary insurance, second policy | pos: {E} has a second coverage on file | neg: {E} has no second coverage on file | br: coordination of benefits | nr: spouse plan added | imp: two payers
interview_on | syn: interview date, call date | say: {E} was interviewed on {v}
visit_on | syn: visit date, date of service | say: {E} is for a visit on {v}
account_tags | syn: account labels, account markers | say: {E} carries the account tags {v} | none: {E} carries none of the account tags
prior_balance | syn: earlier balance, old balance | say: {E} carries an earlier balance of {v}
visits_last_year | syn: past visits, visit count last year | say: {E} visited {v} last year
contact_preference | syn: preferred contact, contact channel | say: {E} prefers contact by {v}
payer_tier | syn: network tier, plan network level | say: {E} sits in the {v} band
response_hours | syn: response time, reply hours | say: {E} replies in {v}
""",
"hc-06": """
estimated_cost | syn: scan cost, cost estimate | say: {E} is quoted at {v}
therapy_weeks | syn: weeks of therapy, conservative care weeks | say: {E} follows {v} of conservative care
days_since_order | syn: order age, days after ordering | say: {E} is {v} old
prior_scans_12_months | syn: recent scans, scans in the past year | say: {E} follows {v} in the past year
modality | syn: imaging method, scan modality | say: {E} is for a {v}
body_region | syn: body part, part scanned | say: {E} covers the {v}
clinical_notes_attached | syn: chart notes attached, clinical documentation | pos: {E} has clinical notes attached | neg: {E} has no clinical notes attached | br: medical evidence | nr: office visit note | imp: medical need documented
urgent_flag_set | syn: urgent marker set, priority flag | pos: {E} is flagged urgent | neg: {E} is not flagged urgent | br: clinical priority | nr: same-day scan order | imp: faster review
peer_review_held | syn: peer-to-peer held, clinician review call | pos: {E} has had a peer review held | neg: {E} has not had a peer review held | br: clinical appeal | nr: call with the payer doctor | imp: peer review offered
peer_review_offered | syn: peer-to-peer offered, review call offered | pos: {E} has had a peer review offered | neg: {E} has not had a peer review offered | br: appeal route | nr: payer letter offering a call | imp: chance to discuss
contrast_needed | syn: contrast dye needed, contrast study | pos: {E} needs contrast | neg: {E} does not need contrast | br: added preparation | nr: kidney function check | imp: higher cost
ordered_on | syn: order date, date ordered | say: {E} was ordered on {v}
scan_window_end | syn: last day for the scan, window end date | say: {E} has a scan window ending on {v}
order_tags | syn: order labels, order markers | say: {E} carries the order tags {v} | none: {E} carries none of the order tags
approval_rate | syn: past approval share, approval history | say: {E} has had {v} of orders approved
gold_card_status | syn: gold card, review exemption | pos: {E} holds gold card status | neg: {E} does not hold gold card status | br: trusted ordering | nr: payer gold card letter | imp: authorization waived
review_turnaround_days | syn: turnaround, decision days | say: {E} decides in {v}
plan_category | syn: plan tier, coverage level | say: {E} offers a {v} plan
""",
"hc-07": """
pages_requested | syn: pages to copy, copy volume | say: {E} asks for {v}
copy_fee | syn: copying charge, release fee | say: {E} carries a copy fee of {v}
days_open | syn: days since receipt, age of the release | say: {E} has been open for {v}
date_span_years | syn: years of history, span of years | say: {E} covers {v} of history
requester_type | syn: kind of requester, asking party | say: {E} comes from a {v}
delivery_format | syn: release format, delivery method | say: {E} goes out by {v}
authorization_signed | syn: signed release form, signed consent | pos: {E} has a signed authorization | neg: {E} has no signed authorization | br: patient consent | nr: notarized release form | imp: disclosure allowed
authorization_expired | syn: lapsed authorization, release form out of date | pos: {E} has an expired authorization | neg: {E} does not have an expired authorization | br: consent problem | nr: end date passed | imp: new form needed
identity_verified | syn: identity confirmed, asker checked | pos: {E} has the requester's identity verified | neg: {E} does not have the requester's identity verified | br: identity proofing | nr: photo ID matched | imp: safe release
sensitive_notes_included | syn: protected notes included, sensitive content | pos: {E} includes sensitive notes | neg: {E} does not include sensitive notes | br: extra privacy rules | nr: therapy notes | imp: special consent needed
fee_paid | syn: payment made, fee settled | pos: {E} has its fee paid | neg: {E} does not have its fee paid | br: payment complete | nr: check cleared | imp: release can proceed
received_on | syn: date received, intake date | say: {E} arrived on {v}
due_on | syn: due date, deadline | say: {E} is due on {v}
release_tags | syn: release labels, release markers | say: {E} carries the release tags {v} | none: {E} carries none of the release tags
age_years | syn: patient age, age in years | say: {E} is {v} old
restriction_on_file | syn: disclosure restriction, sharing restriction | pos: {E} has a disclosure restriction on file | neg: {E} has no disclosure restriction on file | br: privacy limit | nr: restriction letter | imp: partial release
requests_this_year | syn: requests filed this year, yearly volume | say: {E} has filed {v} this year
requester_standing | syn: requester history, standing with the office | say: {E} is a {v} requester
""",
"hc-08": """
days_waiting | syn: time waiting, wait so far | say: {E} has waited {v}
visits_authorized | syn: approved visits, visit allowance | say: {E} authorizes {v}
distance_miles | syn: travel distance, miles to the office | say: {E} sends the patient {v} away
copay_amount | syn: copay, visit charge | say: {E} carries a copay of {v}
referral_priority | syn: urgency, referral grade | say: {E} is marked {v}
plan_kind | syn: insurance plan type, plan model | say: {E} falls under a {v}
summary_attached | syn: visit notes attached, summary supplied | pos: {E} has a visit summary attached | neg: {E} has no visit summary attached | br: clinical handoff | nr: problem summary sent | imp: specialist briefed
specialist_accepted | syn: office accepted, specialist agreed | pos: {E} has been accepted by the specialist | neg: {E} has not been accepted by the specialist | br: care handoff | nr: acceptance note faxed back | imp: appointment can be made
payer_number_issued | syn: authorization number issued, payer number received | pos: {E} has a payer number issued | neg: {E} has no payer number issued | br: payer approval | nr: number on the payer portal | imp: visit covered
report_returned | syn: consult report back, specialist letter back | pos: {E} has its consult report returned | neg: {E} does not have its consult report returned | br: loop closure | nr: specialist note in the chart | imp: visit happened
second_referral_sent | syn: duplicate referral, referral sent twice | pos: {E} was sent a second time | neg: {E} was not sent a second time | br: duplicate work | nr: second fax to the office | imp: confusion between offices
sent_on | syn: date sent, send date | say: {E} was sent on {v}
valid_until | syn: expiry date, end of validity | say: {E} stays valid until {v}
referral_tags | syn: referral labels, referral markers | say: {E} carries the referral tags {v} | none: {E} carries none of the referral tags
open_referrals | syn: active referrals, referrals in progress | say: {E} has {v} open
transport_access | syn: transport access, travel options | say: {E} has {v} access to transport
next_open_days | syn: next opening, wait for a slot | say: {E} next has an opening in {v}
network_member | syn: in-network office, network participation | pos: {E} is in the payer network | neg: {E} is not in the payer network | br: payer contract | nr: network directory entry | imp: lower copay
""",
"hc-09": """
audio_minutes | syn: audio length, audio duration | say: {E} runs {v} of audio
hours_in_queue | syn: queue time, waiting hours | say: {E} has waited {v} in the queue
line_count | syn: report length, typed lines | say: {E} produced {v}
accuracy_score | syn: quality score, accuracy rating | say: {E} scored {v} for accuracy
line_rate | syn: per-line charge, line price | say: {E} is billed at {v} per line
report_type | syn: document type, report kind | say: {E} is a {v}
audio_quality | syn: sound quality, audio clarity | say: {E} has {v} audio
dictation_device | syn: capture device, dictation tool | say: {E} came in by {v}
stat_flag_set | syn: stat marker set, rush flag | pos: {E} is flagged stat | neg: {E} is not flagged stat | br: rush priority | nr: same-hour turnaround | imp: queue jump
gaps_left | syn: gaps in the report, empty spots left | pos: {E} has gaps left in the report | neg: {E} has no gaps left in the report | br: report completeness problem | nr: garbled word flagged | imp: clinician review needed
clinician_signed | syn: signed by the clinician, author signature | pos: {E} carries the clinician's signature | neg: {E} does not carry the clinician's signature | br: authentication | nr: electronic signature applied | imp: report final
template_applied | syn: clinic template used, report template applied | pos: {E} has the clinic template applied | neg: {E} does not have the clinic template applied | br: format compliance | nr: header block filled | imp: uniform look
received_on | syn: date received, intake date | say: {E} arrived on {v}
due_on | syn: due date, deadline | say: {E} is due on {v}
dictation_tags | syn: dictation labels, dictation markers | say: {E} carries the dictation tags {v} | none: {E} carries none of the dictation tags
dictations_this_month | syn: monthly dictations, dictation volume | say: {E} has dictated {v} this month
speaks_quickly | syn: fast speaker, rapid speech | pos: {E} speaks quickly | neg: {E} does not speak quickly | br: hard audio | nr: words run together | imp: more editing time
experience_years | syn: years of experience, transcribing years | say: {E} has {v} of experience
queue_load | syn: open files, current queue | say: {E} has {v} open
""",
"hc-10": """
days_since_discharge | syn: days after discharge, time since discharge | say: {E} is {v} past discharge
open_deficiencies | syn: outstanding items, chart gaps | say: {E} has {v} outstanding
open_queries | syn: queries open, coding questions open | say: {E} has {v} open
expected_payment | syn: expected reimbursement, payment estimate | say: {E} carries a reimbursement estimate of {v}
stay_days | syn: stay length, days in hospital | say: {E} covers a stay of {v}
chart_type | syn: encounter type, kind of chart | say: {E} is an {v} chart
severity_class | syn: severity, illness severity | say: {E} is rated {v}
discharge_summary_signed | syn: discharge summary authenticated, summary signature | pos: {E} has a signed discharge summary | neg: {E} does not have a signed discharge summary | br: chart authentication | nr: physician e-signature on the summary | imp: summary final
operative_report_present | syn: operative report filed, surgery report in the chart | pos: {E} has an operative report filed | neg: {E} has no operative report filed | br: surgical documentation | nr: dictated operative note | imp: surgery documented
query_answered | syn: coding query answered, query response received | pos: {E} has its coding query answered | neg: {E} does not have its coding query answered | br: documentation clarification | nr: physician reply in the query tool | imp: coding can finish
final_coded | syn: coding complete, chart coded | pos: {E} has been final coded | neg: {E} has not been final coded | br: billing readiness | nr: codes assigned and locked | imp: claim can drop
history_on_file | syn: history and physical filed, admission history in the chart | pos: {E} has a history and physical on file | neg: {E} has no history and physical on file | br: admission documentation | nr: signed admission note | imp: chart foundation complete
discharged_on | syn: discharge date, date of discharge | say: {E} was discharged on {v}
query_sent_on | syn: query date, date queried | say: {E} had a query sent on {v}
chart_tags | syn: chart labels, chart markers | say: {E} carries the chart tags {v} | none: {E} carries none of the chart tags
delinquent_charts | syn: overdue charts, late charts | say: {E} has {v} overdue
suspension_warnings | syn: warnings this year, privilege warnings | say: {E} has had {v} this year
charts_coded_today | syn: daily output, charts done today | say: {E} has coded {v} today
credential_level | syn: coder credential, certification level | say: {E} holds a {v} credential
""",
}
