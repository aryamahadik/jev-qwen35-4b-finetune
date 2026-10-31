"""packs-2 lexicons, sector re (Claude-written, v1.1 review fix). Line format: see src/lex_ed.py."""

LEX = {
"re-01": """
appraised_value | syn: appraisal value, opinion of value | say: {E} gives a value of {v}
contract_price | syn: agreed sale price, purchase price | say: {E} relates to a contract price of {v}
net_adjustment_percent | syn: net adjustments, adjustment share | say: {E} shows net adjustments of {v}
comps_within_one_mile | syn: nearby comparable sales, close comparables | say: {E} uses {v} of comparables within one mile
oldest_comp_months | syn: age of the oldest comparable, comparable age | say: {E} uses a comparable sale {v} old
property_type | syn: kind of property, home type | say: {E} covers a {v}
report_form | syn: report type, inspection scope | say: {E} is an {v} report
condition_rating | syn: condition grade, condition score | say: {E} rates the condition {v}
photos_included | syn: required photos present, photo pages included | pos: {E} includes the required photos | neg: {E} does not include the required photos | br: visual support | nr: kitchen and street photos | imp: reviewer can see the home
repairs_required | syn: appraiser named required repairs, repairs called for | pos: {E} calls for repairs | neg: {E} does not call for repairs | br: condition problem | nr: broken handrail noted | imp: value subject to repairs
appraiser_licensed_state | syn: appraiser licensed in the state, state licence held | pos: {E} comes from an appraiser licensed in the state | neg: {E} comes from an appraiser not licensed in the state | br: appraiser qualification | nr: state board lookup | imp: report acceptable
sent_back_before | syn: report returned once already, earlier revision | pos: {E} was sent back before | neg: {E} was not sent back before | br: quality history | nr: revision letter last month | imp: delay to closing
field_review_done | syn: second appraiser visited, field review completed | pos: {E} has had a field review | neg: {E} has not had a field review | br: independent check | nr: reviewer drove by the home | imp: value tested
inspected_on | syn: inspection date, visit date | say: {E} reflects an inspection on {v}
report_on | syn: report date, signature date | say: {E} is dated {v}
appraisal_tags | syn: appraisal labels, appraisal markers | say: {E} carries the appraisal tags {v} | none: {E} carries none of the appraisal tags
reports_reviewed_this_year | syn: reviewed report tally, review count | say: {E} has had {v} reviewed this year
revision_rate | syn: share sent back, revision share | say: {E} has had {v} of reports sent back
loan_to_value | syn: loan as a share of value, LTV | say: {E} borrows at {v} of value
""",
"re-02": """
offer_price | syn: price offered, bid price | say: {E} offers {v}
asking_price | syn: seller's price, asking figure | say: {E} is for a home priced at {v}
earnest_money | syn: deposit offered, good faith deposit | say: {E} puts down {v} as earnest money
days_to_close | syn: closing timeline, days to closing | say: {E} closes in {v}
competing_offers | syn: other offers on the table, rival bids | say: {E} competes with {v}
financing_type | syn: loan type, funding type | say: {E} is paid by {v}
contingency_mix | syn: contingencies, conditions in the offer | say: {E} carries {v}
offer_strength | syn: agent's strength grade, offer grade | say: {E} is graded {v}
preapproval_attached | syn: lender letter attached, pre-approval letter | pos: {E} has a preapproval attached | neg: {E} has no preapproval attached | br: financing proof | nr: bank pre-approval letter | imp: seller trusts the funding
proof_of_funds_attached | syn: bank statement attached, funds proof | pos: {E} has proof of funds attached | neg: {E} has no proof of funds attached | br: cash evidence | nr: brokerage account statement | imp: seller sees the money
disclosure_acknowledged | syn: buyer signed the disclosure, disclosure receipt | pos: {E} has the disclosure acknowledged | neg: {E} does not have the disclosure acknowledged | br: informed buyer | nr: signed seller disclosure form | imp: fewer later disputes
showing_completed | syn: buyer toured the home, viewing done | pos: {E} follows a completed showing | neg: {E} does not follow a completed showing | br: property seen | nr: second walk-through | imp: buyer saw the condition
escalation_clause | syn: automatic increase clause, escalator | pos: {E} has an escalation clause | neg: {E} has no escalation clause | br: bidding strategy | nr: raises by two thousand over rivals | imp: higher final price
written_on | syn: date written, offer date | say: {E} was written on {v}
expires_on | syn: expiry date, deadline for acceptance | say: {E} expires on {v}
offer_tags | syn: offer labels, offer markers | say: {E} carries the offer tags {v} | none: {E} carries none of the offer tags
offers_made_before | syn: earlier offers written, offer history | say: {E} has made {v} before
days_on_market | syn: time on the market, market days | say: {E} has been for sale for {v}
price_cuts | syn: price reductions, markdowns | say: {E} has had {v} of price cuts
""",
"re-03": """
loan_amount | syn: amount borrowed, loan size | say: {E} is for a loan of {v}
monthly_income | syn: verified monthly income, income per month | say: {E} shows income of {v} a month
debt_to_income | syn: debt share of income, DTI | say: {E} shows a debt to income ratio of {v}
months_of_reserves | syn: savings cushion, reserve months | say: {E} shows {v} of reserves
documents_outstanding | syn: documents still owed, open conditions | say: {E} awaits {v}
employment_type | syn: kind of employment, job type | say: {E} comes from a {v} borrower
occupancy | syn: home use, occupancy type | say: {E} is for a {v}
file_grade | syn: file status, file stage | say: {E} is {v}
employment_verified | syn: employer confirmed the job, job verified | pos: {E} has employment verified | neg: {E} does not have employment verified | br: income check | nr: verbal check with the employer | imp: income trusted
large_deposit_explained | syn: large deposit sourced, deposit source letter | pos: {E} has its large deposit explained | neg: {E} does not have its large deposit explained | br: funds sourcing | nr: letter on a bonus deposit | imp: funds acceptable
gift_letter_on_file | syn: gift letter signed, donor letter | pos: {E} has a gift letter on file | neg: {E} has no gift letter on file | br: gift documentation | nr: parent donor letter | imp: gift funds usable
credit_report_pulled | syn: credit report ordered, credit check run | pos: {E} has a credit report pulled | neg: {E} does not have a credit report pulled | br: credit review | nr: tri-merge report | imp: score on hand
bankruptcy_last_four_years | syn: recent bankruptcy, bankruptcy in four years | pos: {E} shows a bankruptcy in the last four years | neg: {E} shows no bankruptcy in the last four years | br: severe credit event | nr: chapter seven discharge | imp: waiting period rules
applied_on | syn: application date, date applied | say: {E} was opened on {v}
rate_lock_ends_on | syn: lock expiry, rate lock end | say: {E} has a rate lock ending on {v}
file_tags | syn: file labels, file markers | say: {E} carries the file tags {v} | none: {E} carries none of the file tags
credit_score | syn: credit rating, bureau score | say: {E} has a credit score of {v}
years_at_job | syn: time at current job, job tenure | say: {E} has been at the job for {v}
files_in_pipeline | syn: files on desk, pipeline count | say: {E} has {v} in the pipeline
""",
"re-04": """
household_income | syn: yearly income, family earnings | say: {E} earns {v} a year
area_median_percent | syn: income share of the area median, median percent | say: {E} sits at {v} of area median income
savings | syn: money saved, savings balance | say: {E} has saved {v}
grant_sought | syn: grant asked for, assistance sought | say: {E} seeks a grant of {v}
counseling_hours | syn: hours of counseling, coaching hours | say: {E} has had {v} of counseling
household_size | syn: people in the home, household members | say: {E} counts {v}
target_area | syn: area sought, search area | say: {E} is looking in the {v}
home_type_sought | syn: kind of home wanted, home type | say: {E} wants a {v}
readiness_stage | syn: buyer stage, readiness | say: {E} is at the {v} stage
class_certificate_earned | syn: finished the buyer class, class completion | pos: {E} has earned the class certificate | neg: {E} has not earned the class certificate | br: buyer education | nr: eight-hour course | imp: grant eligibility
owned_home_last_three_years | syn: owned a home recently, recent homeowner | pos: {E} owned a home in the last three years | neg: {E} did not own a home in the last three years | br: first-time status | nr: sold a condo last year | imp: grant rules apply
budget_completed | syn: household budget done, spending sheet finished | pos: {E} has its budget completed | neg: {E} does not have its budget completed | br: financial readiness | nr: monthly budget sheet | imp: payment target set
preapproval_received | syn: lender pre-approval received, pre-approval letter | pos: {E} has a preapproval received | neg: {E} does not have a preapproval received | br: financing readiness | nr: partner lender letter | imp: buying power set
veteran_household | syn: veteran in the household, service member family | pos: {E} includes a veteran | neg: {E} does not include a veteran | br: veteran benefit eligibility | nr: discharge papers seen | imp: added grant
intake_on | syn: intake date, first meeting | say: {E} started on {v}
contract_on | syn: contract date, purchase contract date | say: {E} signed a contract on {v}
household_tags | syn: household labels, household markers | say: {E} carries the household tags {v} | none: {E} carries none of the household tags
active_clients | syn: caseload, clients served | say: {E} serves {v}
grant_loans_closed | syn: grant-backed loans closed, assisted closings | say: {E} has closed {v}
""",
"re-05": """
estimated_cost | syn: repair estimate, job cost | say: {E} is estimated at {v}
hours_open | syn: time open, age of the order | say: {E} has been open for {v}
floor_number | syn: floor, storey | say: {E} is on floor {v}
repeat_calls_30_days | syn: repeat calls this month, callbacks | say: {E} follows {v} of repeat calls
system | syn: building system, equipment type | say: {E} concerns {v}
cause | syn: root cause, reason for failure | say: {E} is due to {v}
priority | syn: priority grade, urgency | say: {E} is marked {v}
tenant_caused | syn: tenant caused the damage, tenant fault | pos: {E} was caused by the tenant | neg: {E} was not caused by the tenant | br: chargeback basis | nr: broken glass from a tenant move | imp: tenant pays
under_warranty | syn: warranty in force, covered by warranty | pos: {E} is under warranty | neg: {E} is not under warranty | br: manufacturer cover | nr: compressor warranty | imp: vendor pays parts
life_safety_issue | syn: safety hazard present, life safety concern | pos: {E} is a life safety issue | neg: {E} is not a life safety issue | br: urgent hazard | nr: blocked fire exit | imp: immediate response
vendor_dispatched | syn: outside vendor sent, contractor sent | pos: {E} has a vendor dispatched | neg: {E} does not have a vendor dispatched | br: outside repair | nr: plumber on site | imp: vendor invoice
after_hours_call | syn: reported outside business hours, night call | pos: {E} came in after hours | neg: {E} did not come in after hours | br: overtime work | nr: weekend leak call | imp: higher labour rate
reported_on | syn: report date, date raised | say: {E} was raised on {v}
closed_on | syn: close date, completion date | say: {E} was closed on {v}
workorder_tags | syn: work order labels, work order markers | say: {E} carries the work order tags {v} | none: {E} carries none of the work order tags
leased_square_feet | syn: leased area, tenant area | say: {E} leases {v}
lease_type | syn: kind of lease, lease structure | say: {E} holds a {v}
open_orders | syn: orders assigned, open jobs | say: {E} has {v} open
""",
"re-06": """
gross_commission | syn: total commission, commission amount | say: {E} pays out a gross commission of {v}
agent_split_percent | syn: agent's share, split rate | say: {E} gives the agent {v}
referral_fee_percent | syn: referral share, referral cut | say: {E} sends {v} to a referral partner
days_since_closing | syn: time since closing, days after closing | say: {E} comes {v} after closing
outstanding_documents | syn: file items outstanding, open paperwork | say: {E} has {v} of documents outstanding
side | syn: deal side, representation side | say: {E} is for the {v}
transaction_type | syn: deal type, kind of sale | say: {E} is a {v} deal
agent_tier | syn: agent rank, production tier | say: {E} goes to a {v}
file_complete | syn: transaction file complete, paperwork finished | pos: {E} has a complete file | neg: {E} does not have a complete file | br: compliance readiness | nr: all signatures collected | imp: audit ready
funds_received | syn: commission funds arrived, check received from title | pos: {E} has its funds received | neg: {E} does not have its funds received | br: cash in hand | nr: wire from the title company | imp: payout possible
referral_agreement_signed | syn: referral agreement in file, referral contract signed | pos: {E} has a signed referral agreement | neg: {E} does not have a signed referral agreement | br: referral paperwork | nr: signed agreement with the other brokerage | imp: referral fee payable
dual_agency_disclosed | syn: dual role disclosed in writing, dual agency notice | pos: {E} has dual agency disclosed | neg: {E} does not have dual agency disclosed | br: agency disclosure | nr: signed consent from both parties | imp: lawful dual role
agent_owes_fees | syn: agent owes desk fees, agent debt | pos: {E} goes to an agent who owes fees | neg: {E} goes to an agent who owes no fees | br: agent debt | nr: unpaid desk rent | imp: offset from the payout
closed_on | syn: closing date, settlement date | say: {E} closed on {v}
paid_on | syn: payment date, payout date | say: {E} was paid on {v}
disbursement_tags | syn: disbursement labels, disbursement markers | say: {E} carries the disbursement tags {v} | none: {E} carries none of the disbursement tags
closings_this_year | syn: yearly closing count, deals closed | say: {E} has closed {v} this year
cap_paid_so_far | syn: company share paid this year, cap progress | say: {E} has paid {v} toward the cap
sale_price | syn: price paid, sale amount | say: {E} sold for {v}
""",
"re-07": """
draw_amount | syn: amount asked for, draw size | say: {E} asks for {v}
percent_complete | syn: work finished per inspector, completion share | say: {E} shows {v} of the work complete
percent_disbursed_after | syn: share paid after this draw, disbursed share | say: {E} brings disbursement to {v}
retainage_percent | syn: holdback rate, retainage | say: {E} holds back {v}
draw_number | syn: draw sequence, draw count | say: {E} is draw {v}
stage | syn: build stage, construction phase | say: {E} covers the {v} stage
builder_grade | syn: builder standing, builder rank | say: {E} comes from a {v}
inspection_passed | syn: site inspection passed, inspector approval | pos: {E} has passed inspection | neg: {E} has not passed inspection | br: work verified | nr: inspector photos of framing | imp: draw supported
lien_waivers_received | syn: subcontractor waivers in hand, waivers received | pos: {E} has lien waivers received | neg: {E} does not have lien waivers received | br: lien protection | nr: conditional waiver from the roofer | imp: title stays clean
title_update_clear | syn: clean title update, title shows zero new liens | pos: {E} has a clear title update | neg: {E} does not have a clear title update | br: title protection | nr: date-down search | imp: safe to fund
change_order_open | syn: unapproved change order open, open change order | pos: {E} has a change order open | neg: {E} has no change order open | br: scope change | nr: upgraded windows order | imp: budget revision
budget_line_exceeded | syn: a budget line is over, line overrun | pos: {E} has a budget line exceeded | neg: {E} does not have a budget line exceeded | br: cost overrun | nr: framing line over by ten percent | imp: reallocation talk
submitted_on | syn: submission date, date sent | say: {E} was submitted on {v}
inspected_on | syn: inspection date, site visit date | say: {E} was inspected on {v}
draw_tags | syn: draw labels, draw markers | say: {E} carries the draw tags {v} | none: {E} carries none of the draw tags
projects_with_bank | syn: past projects with the bank, bank history | say: {E} has built {v} with the bank
trade_specialty | syn: builder focus, specialty | say: {E} focuses on {v} work
inspections_this_week | syn: visits this week, weekly inspections | say: {E} has made {v} this week
""",
"re-08": """
project_cost | syn: cost of the change, project budget | say: {E} costs {v}
fence_height_ft | syn: fence height in feet, fence height | say: {E} proposes a fence {v} high
setback_ft | syn: distance from the property line, setback | say: {E} sits {v} from the property line
days_since_submitted | syn: time under review, review days | say: {E} has been under review for {v}
neighbors_objecting | syn: neighbour objections, objecting neighbours | say: {E} faces {v} objecting
project_kind | syn: kind of project, change type | say: {E} is for a {v}
visibility | syn: visibility from the street, street visibility | say: {E} is {v}
drawings_attached | syn: drawings included, design sheets attached | pos: {E} has drawings attached | neg: {E} has no drawings attached | br: design detail | nr: site sketch with measures | imp: committee can review
contractor_licensed | syn: contractor holds a licence, licensed builder | pos: {E} uses a licensed contractor | neg: {E} does not use a licensed contractor | br: workmanship assurance | nr: state contractor number | imp: permit possible
work_started_early | syn: work began before approval, early start | pos: {E} had work start early | neg: {E} did not have work start early | br: rule breach | nr: fence started before the decision | imp: violation notice
neighbor_signoff | syn: adjacent owner signed, neighbour consent | pos: {E} has neighbour sign-off | neg: {E} does not have neighbour sign-off | br: neighbour agreement | nr: signed shared-fence form | imp: fewer objections
dues_current | syn: association dues paid up, dues paid on time | pos: {E} comes from an owner with dues current | neg: {E} comes from an owner with dues not current | br: good standing | nr: quarterly dues paid | imp: application can proceed
submitted_on | syn: submission date, date sent | say: {E} was submitted on {v}
decision_due_on | syn: decision date, review deadline | say: {E} is due for a decision on {v}
application_tags | syn: application labels, application markers | say: {E} carries the application tags {v} | none: {E} carries none of the application tags
violations_last_year | syn: rule breaches last year, past violations | say: {E} had {v} last year
fines_owed | syn: open fines, fines balance | say: {E} owes {v} in fines
membership_class | syn: owner category, membership type | say: {E} is a {v}
lot_size_sq_ft | syn: lot area, parcel size | say: {E} covers {v}
""",
"re-09": """
monthly_rent | syn: rent for the unit, monthly charge | say: {E} is for a unit renting at {v}
income_to_rent_ratio | syn: income over rent, rent coverage | say: {E} shows income at {v} times rent
occupants | syn: people moving in, residents | say: {E} names {v}
holding_deposit | syn: deposit to hold the unit, reservation deposit | say: {E} comes with a holding deposit of {v}
months_at_last_address | syn: time at last address, residence length | say: {E} lived {v} at the last address
pet_type | syn: kind of pet, animal type | say: {E} brings a {v}
lease_term | syn: lease length, term | say: {E} asks for a {v} lease
screening_result | syn: screening band, screening outcome | say: {E} falls in the {v}
landlord_reference_positive | syn: good reference from the last landlord, positive landlord reference | pos: {E} has a positive landlord reference | neg: {E} does not have a positive landlord reference | br: rental history | nr: on-time rent letter | imp: lower deposit
eviction_history_found | syn: eviction found in screening, past eviction | pos: {E} shows an eviction history | neg: {E} shows no eviction history | br: rental history problem | nr: court judgment for possession | imp: approval harder
guarantor_signed | syn: guarantor form signed, co-signer signed | pos: {E} has a signed guarantor | neg: {E} does not have a signed guarantor | br: added security | nr: parent as guarantor | imp: rent backed
renters_insurance_proof | syn: renters cover shown, tenant insurance proof | pos: {E} has proof of renters insurance | neg: {E} does not have proof of renters insurance | br: liability protection | nr: declarations page | imp: lease rule met
employed_currently | syn: currently working, in work | pos: {E} is currently employed | neg: {E} is not currently employed | br: income stability | nr: recent pay stubs | imp: steady rent
applied_on | syn: application date, date applied | say: {E} was submitted on {v}
move_in_on | syn: move-in date, start date | say: {E} names {v} as the move-in date
application_tags | syn: application labels, application markers | say: {E} carries the application tags {v} | none: {E} carries none of the application tags
credit_score | syn: credit rating, bureau score | say: {E} has a credit score of {v}
days_vacant | syn: days empty, vacancy days | say: {E} has stood empty for {v}
""",
"re-10": """
monthly_rate | syn: monthly rent, unit rate | say: {E} pays {v} a month
balance_due | syn: amount owed, open balance | say: {E} owes {v}
days_late | syn: days past due, lateness | say: {E} is {v} late
unit_size_sq_ft | syn: unit area, unit size | say: {E} rents a unit of {v}
months_rented | syn: tenure, rental months | say: {E} has rented for {v}
unit_type | syn: kind of unit, unit category | say: {E} rents a {v} unit
payment_method | syn: payment route, how rent is paid | say: {E} pays by {v}
delinquency_stage | syn: collections stage, overdue stage | say: {E} is at the {v} stage
overlock_applied | syn: office lock placed, overlock on the unit | pos: {E} has an overlock applied | neg: {E} does not have an overlock applied | br: access restriction | nr: red lock on the door | imp: tenant must pay to enter
lien_notice_sent | syn: lien notice mailed, lien letter sent | pos: {E} has had a lien notice sent | neg: {E} has not had a lien notice sent | br: lien process | nr: certified letter mailed | imp: auction can follow
contents_protection_active | syn: contents cover in force, goods protection | pos: {E} has contents protection active | neg: {E} does not have contents protection active | br: goods cover | nr: protection plan on the invoice | imp: damage claims covered
military_tenant | syn: active-duty tenant, service member tenant | pos: {E} is held by a military tenant | neg: {E} is not held by a military tenant | br: legal protections | nr: deployment orders | imp: lien sale barred
gate_code_active | syn: gate access works, active access code | pos: {E} has an active gate code | neg: {E} does not have an active gate code | br: site access | nr: keypad code valid | imp: tenant can enter
moved_in_on | syn: move-in date, start date | say: {E} began on {v}
paid_through | syn: paid-through date, coverage date | say: {E} is paid through {v}
account_tags | syn: account labels, account markers | say: {E} carries the account tags {v} | none: {E} carries none of the account tags
accounts_held | syn: units rented, accounts open | say: {E} holds {v}
street_rate | syn: advertised rate, current rate | say: {E} is advertised at {v}
""",
}
