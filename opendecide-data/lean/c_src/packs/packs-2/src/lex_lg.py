"""packs-2 lexicons, sector lg (Claude-written, v1.1 review fix). Line format: see src/lex_ed.py."""

LEX = {
"lg-01": """
days_to_due | syn: days left, time to the due date | say: {E} falls due in {v}
response_period_days | syn: response period, answer period | say: {E} allows a response period of {v}
extensions_granted | syn: extensions so far, deadline extensions | say: {E} has had {v} of extensions
filing_fee | syn: court fee, filing charge | say: {E} carries a filing fee of {v}
service_method | syn: method of service, delivery method | say: {E} was served by {v}
deadline_kind | syn: kind of deadline, filing type | say: {E} is for an {v}
priority_tier | syn: docket priority, urgency tier | say: {E} is marked {v}
notice_received | syn: court notice logged, notice in hand | pos: {E} has its court notice received | neg: {E} does not have its court notice received | br: trigger document | nr: electronic filing notice | imp: deadline computed
extension_filed | syn: extension motion filed, motion for more time | pos: {E} has an extension filed | neg: {E} does not have an extension filed | br: deadline relief | nr: stipulated extension | imp: new due date sought
lawyer_acknowledged | syn: responsible lawyer confirmed, lawyer sign-off | pos: {E} has been acknowledged by the responsible lawyer | neg: {E} has not been acknowledged by the responsible lawyer | br: accountability | nr: reply to the docket email | imp: lawyer aware
holiday_in_window | syn: court holiday in the period, closure day in range | pos: {E} has a court holiday in its window | neg: {E} has no court holiday in its window | br: date computation issue | nr: court closed for a holiday | imp: due date shifts
tolling_order_active | syn: stay order in force, tolling in effect | pos: {E} is under an active tolling order | neg: {E} is not under an active tolling order | br: paused clock | nr: court stay order | imp: deadline suspended
served_on | syn: service date, date served | say: {E} was served on {v}
due_on | syn: due date, deadline date | say: {E} is due on {v}
deadline_tags | syn: deadline labels, deadline markers | say: {E} carries the deadline tags {v} | none: {E} carries none of the deadline tags
open_deadlines | syn: active deadlines, deadlines open | say: {E} has {v} open
matter_value | syn: amount at stake, claim value | say: {E} has {v} at stake
docket_load | syn: deadlines on desk, docket count | say: {E} carries {v}
seniority_band | syn: seniority, lawyer level | say: {E} is a {v} lawyer
""",
"lg-02": """
search_hits | syn: conflict search hits, name matches | say: {E} returned {v} of search hits
retainer_amount | syn: retainer, advance deposit | say: {E} asks for a retainer of {v}
estimated_fees | syn: fee estimate, expected fees | say: {E} estimates fees of {v}
days_open | syn: days in intake, intake age | say: {E} has been open for {v}
adverse_parties | syn: parties on the other side, opponents | say: {E} names {v} on the other side
client_kind | syn: client type, kind of client | say: {E} is for a {v}
conflict_level | syn: conflict finding, conflict grade | say: {E} shows a {v} conflict finding
engagement_signed | syn: engagement letter signed, retainer agreement signed | pos: {E} has a signed engagement | neg: {E} does not have a signed engagement | br: client agreement | nr: countersigned engagement letter | imp: terms agreed
waiver_obtained | syn: conflict waiver received, waiver letter in | pos: {E} has a conflict waiver obtained | neg: {E} does not have a conflict waiver obtained | br: informed consent | nr: signed waiver from both clients | imp: conflict cured
former_client_match | syn: adverse party was a client, former client hit | pos: {E} matches a former client as an adverse party | neg: {E} does not match a former client as an adverse party | br: duty to a former client | nr: old file for the opponent | imp: waiver needed
retainer_received | syn: retainer deposited, advance received | pos: {E} has its retainer received | neg: {E} does not have its retainer received | br: funding in place | nr: trust deposit cleared | imp: work can start
identity_checked | syn: client identity confirmed, ID verified | pos: {E} has had the client's identity checked | neg: {E} has not had the client's identity checked | br: client due diligence | nr: passport copy checked | imp: money rules met
opened_on | syn: opening date, intake date | say: {E} was opened on {v}
statute_date | syn: limitation date, statute deadline | say: {E} faces a limitation date of {v}
intake_tags | syn: intake labels, intake markers | say: {E} carries the intake tags {v} | none: {E} carries none of the intake tags
prior_matters | syn: earlier matters, matter history | say: {E} has had {v} with the firm
account_in_good_standing | syn: account in good order, clean account | pos: {E} has an account in good standing | neg: {E} does not have an account in good standing | br: client reliability | nr: invoices paid on time | imp: credit allowed
outstanding_invoice | syn: old balance owed, open bill | say: {E} owes {v} on old invoices
new_matters_this_quarter | syn: matters opened this quarter, quarterly intake | say: {E} has opened {v} this quarter
partner_track | syn: title band, firm rank | say: {E} holds the title of {v}
""",
"lg-03": """
years_since_closing | syn: age since closing, years closed | say: {E} closed {v} ago
retention_years | syn: retention period, keep period | say: {E} has a retention period of {v}
boxes | syn: box count, cartons | say: {E} fills {v}
storage_cost_per_year | syn: yearly storage charge, storage fee | say: {E} costs {v} a year to store
matter_area | syn: practice area, area of law | say: {E} is a {v} file
media_type | syn: storage media, file media | say: {E} is held on {v}
sensitivity_grade | syn: sensitivity, confidentiality grade | say: {E} is graded {v}
legal_hold_active | syn: hold in force, litigation hold | pos: {E} is under an active legal hold | neg: {E} is not under an active legal hold | br: preservation duty | nr: hold notice from counsel | imp: destruction barred
original_deeds_inside | syn: contains original deeds, deeds inside | pos: {E} holds original deeds | neg: {E} does not hold original deeds | br: client property inside | nr: signed title deed | imp: return to the client first
client_consented | syn: client agreed to destruction, client consent | pos: {E} has the client's consent to destroy | neg: {E} does not have the client's consent to destroy | br: client authority | nr: consent letter signed | imp: destruction allowed
partner_signed_off | syn: partner approval given, partner sign-off | pos: {E} has partner sign-off | neg: {E} does not have partner sign-off | br: firm approval | nr: partner initials on the schedule | imp: destruction cleared
closed_on | syn: closing date, date closed | say: {E} was closed on {v}
review_due_on | syn: review date, next review | say: {E} is due for review on {v}
file_tags | syn: file labels, file markers | say: {E} carries the file tags {v} | none: {E} carries none of the file tags
client_age_years | syn: client age, years of age | say: {E} is {v} old
contact_current | syn: contact details up to date, reachable client | pos: {E} has current contact details | neg: {E} does not have current contact details | br: client reachable | nr: email bounced back | imp: consent can be sought
capacity_used | syn: fill level, space used | say: {E} is {v} full
retrieval_hours | syn: retrieval time, fetch time | say: {E} retrieves boxes in {v}
""",
"lg-04": """
years_searched | syn: search depth, years examined | say: {E} covers {v} of title history
open_liens | syn: liens found, unpaid liens | say: {E} found {v}
lien_total | syn: sum of liens, lien balance | say: {E} shows liens totalling {v}
sale_price | syn: contract price, purchase price | say: {E} is for a sale at {v}
days_to_closing | syn: time to closing, closing lead | say: {E} has {v} to closing
property_kind | syn: property type, kind of property | say: {E} covers a {v}
gap_in_chain | syn: break in the chain of title, title gap | pos: {E} shows a gap in the chain of title | neg: {E} shows no gap in the chain of title | br: title defect | nr: deed from a stranger to the chain | imp: curative work
payoff_letter_received | syn: payoff letter in hand, payoff statement received | pos: {E} has a payoff letter received | neg: {E} does not have a payoff letter received | br: lien clearance step | nr: lender payoff figure | imp: lien can be paid at closing
survey_current | syn: survey up to date, recent survey | pos: {E} has a current survey | neg: {E} does not have a current survey | br: boundary evidence | nr: surveyor's plat this year | imp: survey exception removable
easement_registered | syn: registered easement found, easement on the register | pos: {E} shows a registered easement | neg: {E} shows no registered easement | br: encumbrance | nr: utility right of way | imp: exception on the policy
probate_closed | syn: estate closed, probate finished | pos: {E} shows the probate closed | neg: {E} shows the probate not closed | br: estate settled | nr: final probate order | imp: heirs can sell
ordered_on | syn: order date, date ordered | say: {E} was ordered on {v}
closing_on | syn: closing date, settlement date | say: {E} is for a closing on {v}
search_tags | syn: search labels, search markers | say: {E} carries the search tags {v} | none: {E} carries none of the search tags
exception_level | syn: exception class, exception tier | say: {E} carries {v} exceptions
years_owned | syn: length of ownership, ownership years | say: {E} has owned the property for {v}
owner_count | syn: number of owners, co-owners | say: {E} counts {v}
payoff_turnaround_days | syn: payoff reply time, payoff turnaround | say: {E} replies to payoffs in {v}
lender_tier | syn: lender class, lender type | say: {E} is a {v} lender
""",
"lg-05": """
household_income | syn: yearly household income, family income | say: {E} reports household income of {v}
income_limit_percent | syn: income share of the guideline, guideline percent | say: {E} sits at {v} of the guideline
estimated_hours | syn: hours estimate, expected hours | say: {E} is estimated at {v}
days_to_hearing | syn: time until hearing, days to court | say: {E} has a hearing in {v}
referring_partner | syn: referral source, partner agency | say: {E} came from {v}
case_complexity | syn: complexity, difficulty grade | say: {E} is rated {v}
conflict_cleared | syn: conflicts cleared, conflict check passed | pos: {E} has conflicts cleared | neg: {E} does not have conflicts cleared | br: ethics clearance | nr: search run on the landlord | imp: firm can act
client_interviewed | syn: intake interview held, client met | pos: {E} has had the client interviewed | neg: {E} has not had the client interviewed | br: case assessment | nr: phone interview | imp: facts gathered
documents_complete | syn: papers complete, documents in | pos: {E} has its documents complete | neg: {E} does not have its documents complete | br: case readiness | nr: lease and notices supplied | imp: review can start
emergency_hearing | syn: hearing on short notice, urgent hearing | pos: {E} has an emergency hearing | neg: {E} does not have an emergency hearing | br: time pressure | nr: hearing next week | imp: quick staffing
fee_generating | syn: case could earn fees, fee-earning case | pos: {E} is fee generating | neg: {E} is not fee generating | br: commercial potential | nr: damages claim with fee shifting | imp: refer to paid counsel
received_on | syn: date received, intake date | say: {E} arrived on {v}
hearing_on | syn: hearing date, court date | say: {E} has a hearing on {v}
referral_tags | syn: referral labels, referral markers | say: {E} carries the referral tags {v} | none: {E} carries none of the referral tags
household_members | syn: household size, people at home | say: {E} lives with {v} in the household
earlier_pro_bono_cases | syn: past pro bono cases, earlier free cases | say: {E} has had {v} before
pro_bono_hours_ytd | syn: hours this year, volunteer hours so far | say: {E} has given {v} this year
experience_band | syn: experience, career stage | say: {E} is a {v} lawyer
""",
"lg-06": """
parties_count | syn: number of parties, people in the dispute | say: {E} involves {v}
amount_in_dispute | syn: sum disputed, money at issue | say: {E} disputes {v}
session_fee | syn: fee per session, session charge | say: {E} charges {v} per session
sessions_held | syn: sessions so far, meetings held | say: {E} has held {v}
days_since_referral | syn: case age, days since the referral | say: {E} is {v} old
dispute_kind | syn: kind of dispute, dispute type | say: {E} is a {v} dispute
intensity_level | syn: tension level, conflict temperature | say: {E} is rated {v}
agreement_signed | syn: agreement to mediate signed, mediation agreement | pos: {E} has a signed agreement to mediate | neg: {E} does not have a signed agreement to mediate | br: party consent | nr: both parties signed | imp: sessions can start
court_ordered | syn: sent by court order, court referral | pos: {E} was ordered by a court | neg: {E} was not ordered by a court | br: mandatory mediation | nr: judge's referral order | imp: report back to court
interpreter_arranged | syn: interpreter booked, language support arranged | pos: {E} has an interpreter arranged | neg: {E} has no interpreter arranged | br: language access | nr: Spanish interpreter booked | imp: both parties understood
safety_screen_flagged | syn: safety flag raised, screening concern | pos: {E} has a safety screening flag | neg: {E} has no safety screening flag | br: safety concern | nr: history of threats | imp: parties kept apart
fee_waiver_granted | syn: fee waiver approved, fees waived | pos: {E} has a fee waiver granted | neg: {E} has no fee waiver granted | br: cost relief | nr: income-based waiver | imp: zero fee
referred_on | syn: referral date, date referred | say: {E} was referred on {v}
session_on | syn: session date, meeting date | say: {E} meets on {v}
case_tags | syn: case labels, case markers | say: {E} carries the case tags {v} | none: {E} carries none of the case tags
party_income | syn: yearly income, earnings | say: {E} earns {v} a year
missed_sessions | syn: sessions missed, skipped sessions | say: {E} has missed {v}
party_represented | syn: party has a lawyer, legal representation | pos: {E} has a lawyer | neg: {E} does not have a lawyer | br: legal support | nr: attorney attends sessions | imp: lawyer review of the agreement
cases_mediated | syn: career case count, cases handled | say: {E} has mediated {v}
certification_grade | syn: mediator grade, certification level | say: {E} is a {v} mediator
""",
"lg-07": """
payout_amount | syn: amount to pay out, disbursement amount | say: {E} pays out {v}
ledger_balance | syn: client ledger balance, trust balance | say: {E} draws on a ledger balance of {v}
days_since_deposit | syn: days since funds arrived, deposit age | say: {E} comes {v} after the deposit
payees | syn: number of payees, recipients | say: {E} pays {v}
payment_channel | syn: payment rail, transfer method | say: {E} goes by {v}
purpose_code | syn: payment purpose, reason code | say: {E} is a {v}
approval_level | syn: approver needed, sign-off level | say: {E} needs approval at {v} level
funds_cleared | syn: deposit cleared the bank, cleared funds | pos: {E} draws on funds that have cleared | neg: {E} draws on funds that have not cleared | br: good funds | nr: bank shows the deposit final | imp: payout safe
client_authorized | syn: client instruction received, client approval | pos: {E} has the client's authorization | neg: {E} does not have the client's authorization | br: client consent | nr: signed settlement statement | imp: payout allowed
bill_issued | syn: invoice sent, bill sent before transfer | pos: {E} follows an issued bill | neg: {E} does not follow an issued bill | br: fee transparency | nr: invoice emailed to the client | imp: fee transfer allowed
wire_callback_done | syn: phone callback completed, callback verification | pos: {E} has had a wire callback | neg: {E} has not had a wire callback | br: fraud control | nr: call to a trusted number | imp: wire details confirmed
reconciled_this_month | syn: account reconciled, monthly reconciliation done | pos: {E} is reconciled this month | neg: {E} is not reconciled this month | br: trust compliance | nr: three-way match signed | imp: balances trusted
requested_on | syn: date raised, instruction date | say: {E} was raised on {v}
pay_on | syn: payment date, value date | say: {E} pays on {v}
disbursement_tags | syn: disbursement labels, disbursement markers | say: {E} carries the disbursement tags {v} | none: {E} carries none of the disbursement tags
matters_open | syn: open matters, active matters | say: {E} has {v} open
ledger_negative_before | syn: ledger went below zero, earlier overdraw | pos: {E} has had a negative ledger before | neg: {E} has not had a negative ledger before | br: trust breach history | nr: shortfall last year | imp: closer review
payee_verified | syn: payee details checked, payee confirmed | pos: {E} has been verified | neg: {E} has not been verified | br: payee due diligence | nr: bank letter for the payee | imp: correct account
payments_to_payee | syn: earlier payments, payment history | say: {E} has received {v} before
""",
"lg-08": """
page_count | syn: pages in the job, length in pages | say: {E} runs to {v}
exhibits | syn: exhibit count, attachments | say: {E} includes {v} of exhibits
hours_to_deadline | syn: time left, hours to the deadline | say: {E} is due in {v}
revision_rounds | syn: rounds of changes, edit rounds | say: {E} has been through {v} of revisions
overtime_cost | syn: overtime charge, after-hours cost | say: {E} carries an overtime cost of {v}
job_kind | syn: kind of job, job type | say: {E} is a {v}
output_form | syn: output, delivery form | say: {E} goes out as {v}
complexity_band | syn: job weight, complexity | say: {E} is rated {v}
style_sheet_attached | syn: style sheet on file, format guide attached | pos: {E} has a style sheet attached | neg: {E} has no style sheet attached | br: formatting guidance | nr: court formatting rules | imp: consistent output
lawyer_proof_approved | syn: proof signed off, lawyer approval of the proof | pos: {E} has a proof approved by the lawyer | neg: {E} does not have a proof approved by the lawyer | br: quality gate | nr: initialled proof copy | imp: job can be finished
bates_stamped | syn: page stamping applied, page numbers stamped | pos: {E} has been Bates stamped | neg: {E} has not been Bates stamped | br: production numbering | nr: prefix and number on each page | imp: pages traceable
redlines_open | syn: changes still open, open edits | pos: {E} has redlines open | neg: {E} has no redlines open | br: drafting still under way | nr: tracked changes in clause four | imp: proof still in draft
received_on | syn: date received, intake date | say: {E} arrived on {v}
due_on | syn: due date, deadline | say: {E} is due on {v}
job_tags | syn: job labels, job markers | say: {E} carries the job tags {v} | none: {E} carries none of the job tags
jobs_this_week | syn: jobs sent this week, weekly jobs | say: {E} has sent {v} this week
practice_area | syn: practice group, area of law | say: {E} works in {v}
open_jobs | syn: jobs on hand, workload | say: {E} has {v} on hand
skill_grade | syn: operator grade, skill level | say: {E} is a {v}
operator_certified | syn: cleared for court filings, filing certification | pos: {E} is certified for court filings | neg: {E} is not certified for court filings | br: filing competence | nr: e-filing course passed | imp: can submit to court
""",
"lg-09": """
monthly_income | syn: income per month, monthly earnings | say: {E} reports income of {v} a month
household_size | syn: people in the home, household members | say: {E} supports {v}
claim_amount | syn: amount claimed, sum sued for | say: {E} claims {v}
filing_fee | syn: fee owed, court fee | say: {E} faces a filing fee of {v}
days_since_filed | syn: application age, days waiting | say: {E} has waited {v}
income_source | syn: source of income, kind of income | say: {E} lives on {v}
form_version | syn: form edition, application edition | say: {E} uses the {v}
benefit_letter_attached | syn: benefit letter on file, award letter attached | pos: {E} has a benefit letter attached | neg: {E} has no benefit letter attached | br: income proof | nr: food assistance letter | imp: automatic eligibility
signature_present | syn: signed by the applicant, applicant signature | pos: {E} carries the applicant's signature | neg: {E} does not carry the applicant's signature | br: sworn statement | nr: signature under penalty of perjury | imp: form valid
earlier_waiver_this_year | syn: waiver granted earlier, earlier fee waiver | pos: {E} follows an earlier waiver this year | neg: {E} does not follow an earlier waiver this year | br: repeat relief | nr: waiver in March | imp: closer look at income
judge_review_ordered | syn: sent for judicial review, judge review | pos: {E} has been sent for judicial review | neg: {E} has not been sent for judicial review | br: judicial scrutiny | nr: magistrate review order | imp: slower decision
filed_on | syn: filing date, date filed | say: {E} was filed on {v}
hearing_on | syn: hearing date, court date | say: {E} is set for a hearing on {v}
application_tags | syn: application labels, application markers | say: {E} carries the application tags {v} | none: {E} carries none of the application tags
claims_filed_this_year | syn: claims this year, yearly filings | say: {E} has filed {v} this year
address_confirmed | syn: address checked, address verified | pos: {E} has had the address confirmed | neg: {E} has not had the address confirmed | br: contact check | nr: utility bill matched | imp: notices reach the applicant
applications_today | syn: applications handled today, daily caseload | say: {E} has handled {v} today
clerk_grade | syn: clerk level, job grade | say: {E} works as a {v}
""",
"lg-10": """
hours_billed | syn: hours logged, time billed | say: {E} bills {v}
hourly_rate | syn: rate charged, billing rate | say: {E} bills at {v} an hour
days_since_work | syn: entry age, days after the work | say: {E} was entered {v} after the work
block_tasks | syn: tasks in one entry, bundled tasks | say: {E} bundles {v}
task_code | syn: activity code, task type | say: {E} is coded as {v}
timekeeper_class | syn: timekeeper type, staff class | say: {E} comes from a {v}
guideline_tier | syn: guideline strictness, billing rule tier | say: {E} falls under {v} guidelines
description_complete | syn: narrative complete, full description | pos: {E} has a complete description | neg: {E} does not have a complete description | br: billing clarity | nr: task and purpose spelled out | imp: client can follow the bill
rate_approved | syn: rate cleared by the client, approved rate | pos: {E} uses an approved rate | neg: {E} does not use an approved rate | br: client pricing terms | nr: rate letter on file | imp: bill passes e-billing
budget_exceeded | syn: matter over budget, budget overrun | pos: {E} falls in a matter over budget | neg: {E} does not fall in a matter over budget | br: cost overrun | nr: fees above the estimate | imp: client approval needed
partner_reviewed | syn: partner looked at it, partner review done | pos: {E} has been reviewed by a partner | neg: {E} has not been reviewed by a partner | br: billing oversight | nr: partner edits on the pre-bill | imp: entry final
edited_after_cutoff | syn: changed after the cutoff, late edit | pos: {E} was edited after the cutoff | neg: {E} was not edited after the cutoff | br: billing control issue | nr: hours changed after month end | imp: audit question
worked_on | syn: work date, date worked | say: {E} covers work on {v}
billed_on | syn: billing date, invoice date | say: {E} was billed on {v}
entry_tags | syn: entry labels, entry markers | say: {E} carries the entry tags {v} | none: {E} carries none of the entry tags
write_down_rate | syn: usual write-down share, discount habit | say: {E} usually writes down {v}
days_to_pay | syn: average payment time, payment days | say: {E} pays in {v} on average
utilization | syn: billable share, utilization rate | say: {E} runs at {v} utilization
late_entries_this_month | syn: late entries, delayed entries | say: {E} has made {v} late this month
billing_course_finished | syn: billing training done, billing course completed | pos: {E} has finished the billing course | neg: {E} has not finished the billing course | br: billing competence | nr: online billing module | imp: fewer entry errors
""",
}
