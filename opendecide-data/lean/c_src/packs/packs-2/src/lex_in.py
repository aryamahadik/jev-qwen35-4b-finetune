"""packs-2 lexicons, sector in (Claude-written, v1.1 review fix). Line format: see src/lex_ed.py."""

LEX = {
"in-01": """
days_since_submission | syn: time under review, days with the regulator | say: {E} has been with the regulator for {v}
objections_open | syn: open objections, points awaiting answer | say: {E} has {v} of objections open
rate_change_percent | syn: rate change, proposed rate move | say: {E} proposes a rate change of {v}
filing_fee | syn: state fee, submission fee | say: {E} carries a filing fee of {v}
days_to_launch | syn: days to launch, launch lead | say: {E} is {v} from launch
filing_kind | syn: kind of filing, filing type | say: {E} is a {v} filing
review_regime | syn: review system, approval regime | say: {E} falls under {v} review
complexity | syn: review complexity, filing difficulty | say: {E} is rated {v}
deemer_period_passed | syn: deemer period over, automatic approval period run | pos: {E} has passed its deemer period | neg: {E} has not passed its deemer period | br: approval by lapse of time | nr: sixty days with zero objection | imp: product may launch
approval_letter_received | syn: regulator approval letter, approval received | pos: {E} has an approval letter received | neg: {E} does not have an approval letter received | br: regulatory approval | nr: signed approval notice | imp: launch cleared
response_sent | syn: objection reply sent, answer filed | pos: {E} has had its response sent | neg: {E} has not had its response sent | br: regulator dialogue | nr: reply letter uploaded | imp: review clock restarts
actuarial_memo_attached | syn: actuarial support included, rate memo attached | pos: {E} has an actuarial memo attached | neg: {E} has no actuarial memo attached | br: rate justification | nr: loss trend exhibit | imp: rate support shown
public_hearing_called | syn: hearing called, public hearing set | pos: {E} has had a public hearing called | neg: {E} has not had a public hearing called | br: regulator scrutiny | nr: hearing notice issued | imp: longer review
submitted_on | syn: submission date, date filed | say: {E} was submitted on {v}
launch_on | syn: launch date, go-live date | say: {E} targets a launch on {v}
filing_tags | syn: filing labels, filing markers | say: {E} carries the filing tags {v} | none: {E} carries none of the filing tags
projected_premium | syn: yearly premium projected, premium forecast | say: {E} projects premium of {v} a year
states_approved | syn: states cleared, approvals so far | say: {E} is approved in {v}
open_filings | syn: filings on the desk, open caseload | say: {E} has {v} open
""",
"in-02": """
premium_change | syn: premium difference, cost change | say: {E} changes the premium by {v}
days_backdated | syn: backdating, days dated back | say: {E} is backdated by {v}
drivers_after_change | syn: drivers on the policy, covered drivers | say: {E} leaves {v} on the policy
limit_increase_percent | syn: limit rise, increase in limits | say: {E} raises limits by {v}
change_kind | syn: kind of change, change type | say: {E} is a change to {v}
submitted_by | syn: who sent it, submitter | say: {E} came from the {v}
referral_level | syn: approval route, referral tier | say: {E} routes to {v}
signed_form_received | syn: signed change form, signature received | pos: {E} has a signed form received | neg: {E} does not have a signed form received | br: written consent | nr: e-signature on the change form | imp: change authorized
driving_history_clean | syn: clean motoring history, tidy driving history | pos: {E} has a clean driving history | neg: {E} does not have a clean driving history | br: driver quality | nr: zero tickets in three years | imp: preferred rating
claim_open | syn: claim in progress, open claim | pos: {E} has a claim open | neg: {E} has no claim open | br: active loss | nr: collision claim being adjusted | imp: underwriting caution
lender_notified | syn: loss payee informed, lender informed | pos: {E} has had the lender notified | neg: {E} has not had the lender notified | br: lender communication | nr: lienholder notice mailed | imp: lender files current
vehicle_inspected | syn: inspection photos received, car inspected | pos: {E} has had the vehicle inspected | neg: {E} has not had the vehicle inspected | br: vehicle condition check | nr: four corner photos | imp: damage on file before cover
received_on | syn: date received, intake date | say: {E} came in on {v}
effective_on | syn: effective date, change date | say: {E} takes effect on {v}
endorsement_tags | syn: endorsement labels, endorsement markers | say: {E} carries the endorsement tags {v} | none: {E} carries none of the endorsement tags
annual_premium | syn: yearly premium, policy premium | say: {E} costs {v} a year
years_in_force | syn: policy age, years active | say: {E} has been in force for {v}
endorsements_this_month | syn: changes this month, monthly endorsements | say: {E} has sent {v} this month
""",
"in-03": """
building_value | syn: insured value, property value | say: {E} insures a building worth {v}
building_age_years | syn: building age, years since construction | say: {E} concerns a building {v} old
losses_last_five_years | syn: claims in five years, loss count | say: {E} shows {v} in five years
distance_to_hydrant_m | syn: hydrant distance, metres to a hydrant | say: {E} sits {v} from a hydrant
sprinkler_coverage | syn: sprinkler share, floor area sprinklered | say: {E} has {v} of floor area sprinklered
construction_class | syn: building construction, construction type | say: {E} is of {v} construction
occupancy | syn: building use, tenant type | say: {E} is used as a {v}
protection_class | syn: fire protection grade, protection rating | say: {E} sits in {v}
roof_updated_recently | syn: new roof, roof replaced | pos: {E} has a recently updated roof | neg: {E} does not have a recently updated roof | br: building upkeep | nr: roof replaced six years ago | imp: lower wind and leak hazard
alarm_central_station | syn: monitored alarm, central alarm | pos: {E} has a central station alarm | neg: {E} does not have a central station alarm | br: fire detection | nr: alarm company contract | imp: faster fire response
vacant_space_share_high | syn: much empty space, large empty share | pos: {E} has a large vacant share | neg: {E} does not have a large vacant share | br: occupancy hazard | nr: half the floors empty | imp: vandalism hazard
inspection_completed | syn: loss control visit done, site inspection done | pos: {E} has had an inspection completed | neg: {E} has not had an inspection completed | br: hazard review | nr: inspector photographed the wiring | imp: report on file
cooking_operations | syn: commercial cooking, kitchen on site | pos: {E} has cooking operations | neg: {E} does not have cooking operations | br: fire hazard | nr: deep fryer in use | imp: hood system needed
received_on | syn: date received, intake date | say: {E} arrived on {v}
effective_on | syn: effective date, start of cover | say: {E} is for cover starting {v}
submission_tags | syn: submission labels, submission markers | say: {E} carries the submission tags {v} | none: {E} carries none of the submission tags
years_in_business | syn: business age, trading years | say: {E} has been in business for {v}
agency_loss_ratio | syn: loss ratio, agency loss experience | say: {E} runs a loss ratio of {v}
""",
"in-04": """
estimated_payroll | syn: payroll estimate, starting payroll | say: {E} began with a payroll estimate of {v}
audited_payroll | syn: actual payroll, payroll found | say: {E} found payroll of {v}
premium_difference | syn: audit adjustment, premium change | say: {E} changes premium by {v}
days_since_policy_end | syn: days after the policy ended, audit lag | say: {E} comes {v} after the policy ended
subcontractors_used | syn: subcontractors hired, outside crews | say: {E} shows {v} used
main_class | syn: main class code, business class | say: {E} is mainly {v}
bookkeeping_quality | syn: quality of the books, ledger quality | say: {E} rates the books {v}
books_provided | syn: books handed over, ledgers supplied | pos: {E} had the books provided | neg: {E} did not have the books provided | br: audit cooperation | nr: payroll journals sent | imp: audit can finish
sub_certificates_on_file | syn: subcontractor certificates held, subcontractor cover proven | pos: {E} has subcontractor certificates on file | neg: {E} has no subcontractor certificates on file | br: cover proof | nr: certificate for each crew | imp: subcontractor payroll excluded
owner_excluded | syn: owner left out by election, owner exclusion | pos: {E} has the owner excluded | neg: {E} does not have the owner excluded | br: election on file | nr: exclusion form | imp: owner pay ignored
audit_contested | syn: past audit challenged, earlier audit dispute | pos: {E} comes from an employer who contested a past audit | neg: {E} comes from an employer who has not contested a past audit | br: dispute history | nr: appeal of last year's bill | imp: careful documentation
estimate_updated_midterm | syn: estimate revised midterm, mid-term payroll revision | pos: {E} had its estimate updated mid-term | neg: {E} did not have its estimate updated mid-term | br: exposure update | nr: revised payroll report | imp: smaller audit gap
policy_ended_on | syn: policy end date, expiry date | say: {E} covers a policy that ended on {v}
audit_on | syn: audit date, date audited | say: {E} took place on {v}
audit_tags | syn: audit labels, audit markers | say: {E} carries the audit tags {v} | none: {E} carries none of the audit tags
employees | syn: staff count, headcount | say: {E} employs {v}
years_insured | syn: years with the insurer, policy history | say: {E} has been insured for {v}
payroll_system | syn: payroll method, how payroll is kept | say: {E} keeps payroll by {v}
audits_this_month | syn: audits done this month, monthly audits | say: {E} has done {v} this month
""",
"in-05": """
repair_cost | syn: estimate total, repair estimate | say: {E} puts repairs at {v}
vehicle_value | syn: cash value, car value | say: {E} values the car at {v}
salvage_bid | syn: salvage offer, scrap bid | say: {E} shows a salvage bid of {v}
supplements_so_far | syn: supplements added, extra estimates | say: {E} has {v} of supplements
rental_days | syn: rental days used, loaner days | say: {E} shows {v} of rental
damage_area | syn: damaged area, impact area | say: {E} shows damage to the {v}
shop_type | syn: kind of shop, body shop type | say: {E} comes from a {v}
damage_severity | syn: severity, damage grade | say: {E} rates the damage {v}
airbags_deployed | syn: airbags went off, airbag deployment | pos: {E} shows the airbags deployed | neg: {E} shows the airbags did not deploy | br: severe impact | nr: driver and side curtain airbags | imp: higher repair cost
frame_damage_found | syn: frame bent, structural damage | pos: {E} shows frame damage | neg: {E} shows no frame damage | br: structural harm | nr: unibody rail kinked | imp: total loss talk
photos_complete | syn: full photo set, photo set complete | pos: {E} has a complete photo set | neg: {E} does not have a complete photo set | br: visual evidence | nr: odometer and plate photos | imp: desk review possible
prior_damage_noted | syn: old damage seen, earlier damage | pos: {E} notes prior damage | neg: {E} does not note prior damage | br: pre-existing harm | nr: rust on the old dent | imp: deduction from the payment
drivable | syn: roadworthy, can be driven | pos: {E} is drivable | neg: {E} is not drivable | br: vehicle usability | nr: car drove to the shop | imp: fewer rental days
towed_from_scene | syn: vehicle towed, tow from the scene | pos: {E} was towed from the scene | neg: {E} was not towed from the scene | br: severe crash | nr: tow truck invoice | imp: storage fees
loss_on | syn: loss date, accident date | say: {E} concerns a loss on {v}
estimate_on | syn: estimate date, date written | say: {E} was written on {v}
estimate_tags | syn: estimate labels, estimate markers | say: {E} carries the estimate tags {v} | none: {E} carries none of the estimate tags
vehicle_age_years | syn: model age, car age | say: {E} is {v} old
odometer_km | syn: distance driven, odometer reading | say: {E} shows {v} on the odometer
average_cycle_days | syn: repair turnaround, shop cycle time | say: {E} takes {v} on average
prior_claims | syn: earlier claims, claim history | say: {E} has made {v} before
""",
"in-06": """
commission_held | syn: commission on hold, withheld commission | say: {E} has {v} of commission on hold
ce_hours_completed | syn: education hours completed, course hours earned | say: {E} has completed {v} of continuing education
ce_hours_required | syn: education hours needed, course hours due | say: {E} needs {v} of continuing education
days_to_license_expiry | syn: days to licence expiry, licence time left | say: {E} has a licence that ends in {v}
states_appointed | syn: appointed states, states with appointments | say: {E} is appointed in {v}
line_of_authority | syn: licence line, product line authority | say: {E} holds {v} authority
agent_type | syn: kind of agent, distribution type | say: {E} works as a {v}
compliance_tier | syn: compliance standing, compliance grade | say: {E} stands at {v}
license_active | syn: licence current, active licence | pos: {E} has an active license | neg: {E} does not have an active license | br: legal authority to sell | nr: state lookup shows active | imp: sales allowed
appointment_filed | syn: carrier appointment filed, appointment submitted | pos: {E} has an appointment filed | neg: {E} does not have an appointment filed | br: carrier authority | nr: state appointment fee paid | imp: commission can flow
background_cleared | syn: background check passed, screening cleared | pos: {E} has a cleared background check | neg: {E} does not have a cleared background check | br: fitness to sell | nr: fingerprint report back | imp: appointment allowed
complaint_open | syn: consumer complaint open, complaint under review | pos: {E} has a complaint open | neg: {E} has no complaint open | br: conduct concern | nr: department of insurance inquiry | imp: compliance watch
errors_omissions_cover | syn: professional liability cover, errors and omissions policy | pos: {E} has errors and omissions cover | neg: {E} does not have errors and omissions cover | br: professional protection | nr: certificate of cover | imp: client harm covered
licensed_on | syn: licence date, first licensed | say: {E} was first licensed on {v}
renewal_due_on | syn: renewal date, licence renewal date | say: {E} is due for renewal on {v}
producer_tags | syn: producer labels, producer markers | say: {E} carries the producer tags {v} | none: {E} carries none of the producer tags
producers_in_agency | syn: agents in the agency, agency headcount | say: {E} has {v}
open_cases | syn: cases on desk, open workload | say: {E} has {v} open
""",
"in-07": """
appraised_value | syn: appraisal amount, item value | say: {E} is appraised at {v}
appraisal_age_years | syn: appraisal age, years since appraisal | say: {E} rests on an appraisal {v} old
value_increase_percent | syn: value rise, increase since the last appraisal | say: {E} has risen in value by {v}
items_on_schedule | syn: items already covered, schedule size | say: {E} joins a schedule of {v}
storage | syn: storage place, how it is kept | say: {E} is kept in a {v}
item_material | syn: material, item make-up | say: {E} is made of {v}
appraiser_grade | syn: appraiser standing, appraiser rank | say: {E} was appraised by a {v} appraiser
appraisal_certified | syn: certified appraisal, appraisal on file | pos: {E} has a certified appraisal | neg: {E} does not have a certified appraisal | br: value proof | nr: gemologist report | imp: value accepted
photos_on_file | syn: item photographed, photo evidence | pos: {E} has photos on file | neg: {E} has no photos on file | br: identification evidence | nr: close-up of the hallmark | imp: easier claim proof
alarm_in_home | syn: home alarm, burglar alarm | pos: {E} is kept in a home with an alarm | neg: {E} is kept in a home with no alarm | br: theft protection | nr: monitored motion sensors | imp: lower theft hazard
travels_with_owner | syn: taken on trips, worn while travelling | pos: {E} travels with its owner | neg: {E} does not travel with its owner | br: exposure away from home | nr: ring worn abroad | imp: higher loss chance
theft_claim_last_five_years | syn: theft claim, burglary claim | pos: {E} has an owner with a theft claim in five years | neg: {E} has an owner with no theft claim in five years | br: loss history | nr: stolen necklace claim | imp: tighter terms
jeweller_inspection_done | syn: setting check done, clasp inspection | pos: {E} has had a jeweller inspection | neg: {E} has not had a jeweller inspection | br: condition check | nr: prongs tightened | imp: stone loss less likely
appraised_on | syn: appraisal date, date appraised | say: {E} was appraised on {v}
added_on | syn: date added, schedule date | say: {E} was added on {v}
item_tags | syn: item labels, item markers | say: {E} carries the item tags {v} | none: {E} carries none of the item tags
total_scheduled_value | syn: value already scheduled, schedule total | say: {E} already schedules {v}
appraisals_reviewed | syn: appraisals checked, reviewed appraisals | say: {E} has had {v} reviewed
""",
"in-08": """
days_since_lapse | syn: days after the lapse, lapse age | say: {E} is {v} past the lapse
amount_overdue | syn: missed premium, overdue premium | say: {E} has {v} overdue
refund_due | syn: refund owed, premium to return | say: {E} owes a refund of {v}
days_into_term | syn: days of the term used, term elapsed | say: {E} is {v} into the term
case_kind | syn: kind of case, service type | say: {E} is a {v}
refund_basis | syn: refund method, return basis | say: {E} refunds on a {v} basis
retention_offer_level | syn: retention offer, save offer tier | say: {E} carries a {v} retention offer
loss_free_statement_signed | syn: zero-loss statement signed, statement of zero losses | pos: {E} has a signed statement of zero losses | neg: {E} does not have a signed statement of zero losses | br: reinstatement condition | nr: signed affidavit | imp: reinstatement possible
payment_received | syn: missed payment made, payment arrived | pos: {E} has the payment received | neg: {E} does not have the payment received | br: account cured | nr: card payment posted | imp: balance cleared
lienholder_on_policy | syn: lender named on the policy, loss payee named | pos: {E} has a lienholder on the policy | neg: {E} has no lienholder on the policy | br: financed vehicle | nr: bank as loss payee | imp: lender must be told
cancellation_in_writing | syn: written cancellation received, cancellation letter | pos: {E} has the cancellation in writing | neg: {E} does not have the cancellation in writing | br: proper notice | nr: signed cancellation form | imp: cancel date fixed
earlier_lapse_this_year | syn: earlier lapse, prior lapse this year | pos: {E} had an earlier lapse this year | neg: {E} did not have an earlier lapse this year | br: payment history problem | nr: lapse in March | imp: reinstatement caution
lapsed_on | syn: lapse date, date lapsed | say: {E} lapsed on {v}
called_on | syn: call date, contact date | say: {E} was opened by a call on {v}
case_tags | syn: case labels, case markers | say: {E} carries the case tags {v} | none: {E} carries none of the case tags
years_with_insurer | syn: customer tenure, years insured here | say: {E} has been insured for {v}
calls_today | syn: calls handled today, daily calls | say: {E} has taken {v} today
""",
"in-09": """
limit_required | syn: required limit, limit the holder wants | say: {E} needs a limit of {v}
limit_on_policy | syn: policy limit, limit carried | say: {E} shows a policy limit of {v}
days_to_policy_expiry | syn: days to expiry, policy time left | say: {E} faces a policy ending in {v}
hours_needed_in | syn: turnaround needed, hours until needed | say: {E} is needed in {v}
holder_type | syn: kind of holder, holder category | say: {E} goes to a {v}
coverage_line | syn: line of cover, coverage type | say: {E} proves {v}
wording_difficulty | syn: wording type, contract wording grade | say: {E} uses {v} wording
additional_insured_endorsed | syn: additional insured endorsement, holder added as insured | pos: {E} has an additional insured endorsement | neg: {E} does not have an additional insured endorsement | br: holder protection | nr: blanket additional insured form | imp: holder covered
waiver_endorsed | syn: waiver of recovery endorsement, subrogation waiver | pos: {E} has a waiver endorsement | neg: {E} does not have a waiver endorsement | br: contract compliance | nr: blanket waiver form | imp: insurer gives up recovery
policy_paid_current | syn: premium paid up, policy current | pos: {E} has a policy paid up to date | neg: {E} does not have a policy paid up to date | br: cover in force | nr: last instalment cleared | imp: certificate honest
holder_contract_received | syn: holder contract wording received, contract copy in | pos: {E} has the holder's contract received | neg: {E} does not have the holder's contract received | br: wording check possible | nr: lease insurance clause | imp: terms can be matched
manager_reviewed | syn: account manager checked it, manager review | pos: {E} has been reviewed by the manager | neg: {E} has not been reviewed by the manager | br: quality check | nr: manager initials | imp: release approved
asked_on | syn: date asked, ask date | say: {E} was asked for on {v}
issued_on | syn: issue date, date issued | say: {E} was issued on {v}
certificate_tags | syn: certificate labels, certificate markers | say: {E} carries the certificate tags {v} | none: {E} carries none of the certificate tags
certificates_this_year | syn: certificates issued this year, yearly certificates | say: {E} has had {v} this year
strictness | syn: holder strictness, demands level | say: {E} is {v}
asks_this_month | syn: certificates asked for this month, monthly asks | say: {E} has asked for {v} this month
""",
"in-10": """
quoted_premium | syn: premium quoted, yearly price | say: {E} quotes {v} a year
contents_value | syn: value of belongings, stock value | say: {E} covers contents worth {v}
claims_last_three_years | syn: recent claims, claims in three years | say: {E} shows {v} in three years
days_since_prior_cover_ended | syn: gap in cover, days since the old cover ended | say: {E} follows a gap of {v}
deductible_choice | syn: deductible, excess chosen | say: {E} carries a deductible of {v}
occupancy_type | syn: kind of premises, occupancy | say: {E} is for a {v}
payment_plan | syn: billing plan, payment schedule | say: {E} is {v}
binding_tier | syn: binding authority, bind route | say: {E} binds by {v}
prior_insurance_proven | syn: proof of earlier cover, prior policy proven | pos: {E} has prior insurance proven | neg: {E} does not have prior insurance proven | br: continuous cover | nr: declarations page from the old insurer | imp: continuous cover discount
first_payment_taken | syn: down payment received, first instalment taken | pos: {E} has its first payment taken | neg: {E} does not have its first payment taken | br: payment commitment | nr: card charged for the deposit | imp: policy can start
application_signed | syn: signed application, applicant signature | pos: {E} has a signed application | neg: {E} does not have a signed application | br: applicant attestation | nr: e-signed form | imp: answers confirmed
dog_on_premises | syn: dog at the address, resident dog | pos: {E} has a dog on the premises | neg: {E} has no dog on the premises | br: liability exposure | nr: large breed dog | imp: bite claim hazard
sprinklered_building | syn: building with sprinklers, sprinkler system | pos: {E} is in a sprinklered building | neg: {E} is not in a sprinklered building | br: fire protection | nr: ceiling sprinkler heads | imp: lower fire hazard
quoted_on | syn: quote date, date quoted | say: {E} was quoted on {v}
start_on | syn: start date, cover start | say: {E} starts on {v}
quote_tags | syn: quote labels, quote markers | say: {E} carries the quote tags {v} | none: {E} carries none of the quote tags
credit_tier | syn: credit band, credit grade | say: {E} has a {v} credit tier
bind_limit | syn: binding limit, most the agent may bind | say: {E} lets the agent bind up to {v}
""",
}
