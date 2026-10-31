"""packs-2 lexicons, sector fo (Claude-written, v1.1 review fix). Line format: see src/lex_ed.py."""

LEX = {
"fo-01": """
notional | syn: face amount, principal amount | say: {E} is for a notional of {v}
tenor_days | syn: tenor, term to maturity | say: {E} runs for {v}
limit_used_after | syn: limit usage, share of the limit used | say: {E} takes limit usage to {v}
trades_with_bank_today | syn: deals with the bank today, same-day deal count | say: {E} comes after {v} with the bank today
instrument | syn: product type, deal type | say: {E} is a {v}
trade_currency | syn: deal currency, currency of the trade | say: {E} is in {v}
rating_band | syn: credit rating band, bank grade | say: {E} faces a bank rated {v}
confirmation_matched | syn: confirmation agreed, confirms matched | pos: {E} has its bank confirmation matched | neg: {E} does not have its bank confirmation matched | br: trade verification | nr: swift confirmation paired | imp: confirmation received
board_exception_granted | syn: board waiver, exception approved by the board | pos: {E} has a board exception granted | neg: {E} has no board exception granted | br: governance approval | nr: board resolution passed | imp: limit waiver
rating_watch_negative | syn: negative watch, downgrade watch | pos: {E} faces a bank on negative rating watch | neg: {E} faces a bank not on negative rating watch | br: credit deterioration | nr: agency outlook cut | imp: downgrade signal
netting_agreement | syn: master netting in place, netting contract | pos: {E} is covered by a netting agreement | neg: {E} is not covered by a netting agreement | br: exposure offset | nr: signed master agreement | imp: reduced net exposure
breach_last_quarter | syn: earlier limit breach, breach in the prior quarter | pos: {E} faces a bank whose limit was breached last quarter | neg: {E} faces a bank whose limit was not breached last quarter | br: limit history problem | nr: breach memo filed | imp: excess exposure earlier
traded_on | syn: trade date, deal date | say: {E} was dealt on {v}
matures_on | syn: maturity date, end date | say: {E} matures on {v}
trade_tags | syn: trade labels, deal markers | say: {E} carries the trade tags {v} | none: {E} carries none of the trade tags
total_limit | syn: bank limit, counterparty ceiling | say: {E} has a total limit of {v}
years_relationship | syn: banking relationship length, years with the bank | say: {E} has banked with the group for {v}
dealer_limit | syn: dealing authority, dealer ceiling | say: {E} deals up to {v}
trades_this_month | syn: monthly deal count, deals this month | say: {E} has dealt {v} this month
""",
"fo-02": """
adjustment_amount | syn: correction amount, pay change | say: {E} adjusts pay by {v}
hours_corrected | syn: corrected hours, hours amended | say: {E} corrects {v}
days_since_pay_date | syn: time since the pay date, days after payday | say: {E} comes {v} after the pay date
periods_affected | syn: periods touched, pay cycles affected | say: {E} touches {v}
adjustment_kind | syn: correction type, kind of adjustment | say: {E} is a {v} adjustment
payment_route | syn: payment method, payout route | say: {E} goes out by {v}
approval_tier | syn: sign-off level, approver level | say: {E} needs sign-off at {v} level
timesheet_attached | syn: timesheet supplied, hours sheet attached | pos: {E} has a timesheet attached | neg: {E} has no timesheet attached | br: hours evidence | nr: signed weekly timesheet | imp: hours documented
manager_signed | syn: manager approval, supervisor sign-off | pos: {E} carries the line manager's signature | neg: {E} does not carry the line manager's signature | br: management approval | nr: manager initials on the form | imp: manager review
garnishment_active | syn: wage order in force, earnings attachment active | pos: {E} concerns pay under an active garnishment | neg: {E} concerns pay with no active garnishment | br: court deduction | nr: child support order | imp: deduction priority
employee_terminated | syn: employee departed, employment ended | pos: {E} concerns an employee who has left | neg: {E} concerns an employee who has not left | br: separation | nr: final paycheck issued | imp: account closed in payroll
tax_year_closed | syn: tax year ended, year-end filed | pos: {E} falls in a closed tax year | neg: {E} does not fall in a closed tax year | br: filed year | nr: year-end forms sent | imp: amended filing needed
error_confirmed_by_payroll | syn: payroll confirmation of the error, error acknowledged by payroll | pos: {E} has the error confirmed by payroll | neg: {E} does not have the error confirmed by payroll | br: error validation | nr: payroll audit note | imp: correction justified
reported_on | syn: report date, date raised | say: {E} was raised on {v}
pay_date | syn: payday, original pay date | say: {E} relates to the pay date of {v}
adjustment_tags | syn: adjustment labels, correction markers | say: {E} carries the adjustment tags {v} | none: {E} carries none of the adjustment tags
hourly_rate | syn: wage rate, rate per hour | say: {E} earns {v} an hour
adjustments_this_year | syn: corrections this year, yearly adjustment count | say: {E} has had {v} this year
team_size | syn: direct reports, headcount managed | say: {E} manages {v}
""",
"fo-03": """
total_value | syn: order value, spend amount | say: {E} totals {v}
quotes_received | syn: bids received, quote count | say: {E} has {v} of quotes
days_needed_in | syn: lead time, days until delivery wanted | say: {E} is needed in {v}
budget_left_percent | syn: budget headroom, share of budget left | say: {E} leaves {v} of the budget
category | syn: spend category, purchase type | say: {E} is for {v}
buying_route | syn: purchase route, sourcing route | say: {E} goes by {v}
approval_level | syn: signing level, authority level | say: {E} needs approval at {v} level
contract_on_file | syn: supply contract held, contract in place | pos: {E} has a vendor contract on file | neg: {E} has no vendor contract on file | br: contract coverage | nr: framework agreement | imp: agreed pricing
sole_source_justified | syn: single source justified, sole source approved | pos: {E} has a sole-source justification approved | neg: {E} has no sole-source justification approved | br: competition waiver | nr: single-source form signed | imp: one supplier only
budget_checked | syn: funds checked, budget review done | pos: {E} has had its budget checked | neg: {E} has not had its budget checked | br: funds control | nr: budget line confirmed | imp: funds reserved
capital_item | syn: capital asset, fixed asset purchase | pos: {E} is for a capital item | neg: {E} is not for a capital item | br: asset spend | nr: equipment above the asset threshold | imp: depreciation
split_order_suspected | syn: split order, threshold splitting | pos: {E} looks split to dodge a threshold | neg: {E} does not look split to dodge a threshold | br: procurement abuse | nr: two orders on the same day | imp: approval avoidance
raised_on | syn: date raised, creation date | say: {E} was raised on {v}
needed_by | syn: delivery date wanted, need date | say: {E} is needed by {v}
requisition_tags | syn: requisition labels, requisition markers | say: {E} carries the requisition tags {v} | none: {E} carries none of the requisition tags
on_time_rate | syn: punctual delivery rate, delivery reliability score | say: {E} delivers on time {v} of the time
vendor_approved | syn: vetted vendor, supplier approval | pos: {E} is an approved vendor | neg: {E} is not an approved vendor | br: supplier vetting | nr: vendor onboarding complete | imp: vendor master entry
requisitions_this_month | syn: monthly requisition count, orders raised this month | say: {E} has raised {v} this month
""",
"fo-04": """
balance_overdue | syn: past-due balance, arrears | say: {E} has {v} overdue
days_past_due | syn: days in arrears, age of the debt | say: {E} is {v} past due
arrangements_broken | syn: broken arrangements, failed payment plans | say: {E} shows {v} broken
notices_sent | syn: notice count, reminders sent | say: {E} has received {v}
customer_class | syn: customer type, account class | say: {E} is a {v} account
contact_result | syn: contact outcome, outreach result | say: {E} shows the last contact result as {v}
hardship_level | syn: hardship band, hardship grade | say: {E} is rated {v} for hardship
medical_certificate | syn: medical hold, medical protection | pos: {E} has medical protection on file | neg: {E} has no medical protection on file | br: protected customer status | nr: doctor's letter | imp: shutoff hold
winter_protection | syn: cold-weather hold, winter hold | pos: {E} is in a winter protection period | neg: {E} is not in a winter protection period | br: seasonal protection | nr: cold snap rule | imp: shutoff hold
promise_kept_last_time | syn: last promise honoured, prior promise kept | pos: {E} kept its last payment promise | neg: {E} did not keep its last payment promise | br: payment reliability | nr: promised amount paid on the day | imp: good faith history
autopay_enrolled | syn: automatic payment set up, direct debit active | pos: {E} is enrolled in autopay | neg: {E} is not enrolled in autopay | br: automatic billing | nr: bank draft on file | imp: regular payments
dispute_open | syn: billing dispute, dispute under review | pos: {E} has a billing dispute open | neg: {E} has no billing dispute open | br: contested charges | nr: meter reading challenge | imp: collection pause
payment_received_this_week | syn: payment this week, recent payment arrived | pos: {E} received a payment this week | neg: {E} did not receive a payment this week | br: recent payment | nr: card payment posted | imp: balance reduced
last_payment_on | syn: last payment date, most recent payment | say: {E} last paid on {v}
next_notice_on | syn: next notice date, upcoming notice | say: {E} is due its next notice on {v}
account_tags | syn: account labels, account markers | say: {E} carries the account tags {v} | none: {E} carries none of the account tags
years_as_customer | syn: customer tenure, years served | say: {E} has been a customer for {v}
deposit_held | syn: security deposit, held deposit | say: {E} has {v} held as a deposit
accounts_assigned | syn: caseload, assigned accounts | say: {E} handles {v}
""",
"fo-05": """
credit_sought | syn: credit line asked, credit amount wanted | say: {E} asks for a credit line of {v}
years_trading | syn: trading history, business age | say: {E} has traded for {v}
trade_references | syn: supplier references, reference count | say: {E} supplies {v} of references
expected_monthly_spend | syn: projected monthly buying, monthly purchase estimate | say: {E} projects monthly purchases of {v}
business_form | syn: legal form, entity type | say: {E} is a {v}
industry | syn: sector, line of business | say: {E} is a {v} business
terms_tier | syn: payment terms, credit terms | say: {E} is offered {v} terms
tax_certificate_valid | syn: valid tax certificate, exemption certificate current | pos: {E} has a valid tax exemption certificate | neg: {E} has no valid tax exemption certificate | br: tax exemption | nr: resale certificate | imp: sales tax waived
guarantee_signed | syn: personal guarantee signed, owner guarantee given | pos: {E} has a signed owner guarantee | neg: {E} has no signed owner guarantee | br: credit security | nr: guarantee form witnessed | imp: owner liability
bank_reference_received | syn: bank letter received, banker's reference | pos: {E} has a bank reference received | neg: {E} has no bank reference received | br: credit evidence | nr: bank opinion letter | imp: account conduct reported
address_matches_registry | syn: registry address match, address confirmed by the registry | pos: {E} gives an address that matches the registry | neg: {E} gives an address that does not match the registry | br: identity check | nr: company registry lookup | imp: verified trading address
prior_account_closed_for_debt | syn: earlier debt closure, prior bad account | pos: {E} had an earlier account closed for debt | neg: {E} did not have an earlier account closed for debt | br: bad credit history | nr: written-off balance | imp: collections history
applied_on | syn: application date, date applied | say: {E} was submitted on {v}
first_order_on | syn: first order date, opening order date | say: {E} names {v} as the first order date
application_tags | syn: application labels, application markers | say: {E} carries the application tags {v} | none: {E} carries none of the application tags
other_businesses | syn: other firms, other companies owned | say: {E} owns {v} besides this one
accounts_opened_this_quarter | syn: quarterly account openings, accounts signed up this quarter | say: {E} has opened {v} this quarter
""",
"fo-06": """
project_cost | syn: project budget, capital cost | say: {E} costs {v}
payback_months | syn: payback time, months to recover cost | say: {E} pays back in {v}
budget_remaining | syn: capital headroom, budget still free | say: {E} faces {v} left in the capital budget
quotes_attached | syn: bids attached, vendor quotes | say: {E} has {v} attached
project_type | syn: kind of project, project category | say: {E} is a {v} project
funding_source | syn: source of funds, money source | say: {E} is funded from {v}
urgency_grade | syn: urgency rating, priority grade | say: {E} is graded {v}
safety_mandated | syn: safety order, inspection requirement | pos: {E} is mandated by a safety inspection | neg: {E} is not mandated by a safety inspection | br: compliance need | nr: fire marshal order | imp: legal duty to act
board_approved | syn: board sign-off, approved by the board | pos: {E} has board approval | neg: {E} does not have board approval | br: governance approval | nr: board minute signed | imp: funding release
in_annual_budget | syn: budgeted this year, part of the annual budget | pos: {E} is in this year's budget | neg: {E} is not in this year's budget | br: planned spend | nr: budget line reserved | imp: funds set aside
landlord_consent | syn: landlord approval, owner consent | pos: {E} has the landlord's consent | neg: {E} does not have the landlord's consent | br: lease permission | nr: landlord letter signed | imp: works allowed on site
overspend_on_last_project | syn: last project overspent, cost overrun last time | pos: {E} comes from a sponsor whose last project overspent | neg: {E} comes from a sponsor whose last project did not overspend | br: cost control problem | nr: invoice above the approved budget | imp: budget overrun
submitted_on | syn: submission date, date sent | say: {E} was submitted on {v}
start_on | syn: start date, work start | say: {E} begins on {v}
request_tags | syn: project labels, project markers | say: {E} carries the project tags {v} | none: {E} carries none of the project tags
weekly_sales | syn: weekly revenue, sales each week | say: {E} sells {v} a week
site_age_years | syn: site age, years open | say: {E} opened {v} ago
projects_sponsored | syn: projects led, sponsored project count | say: {E} has sponsored {v}
""",
"fo-07": """
current_limit | syn: credit line now, existing limit | say: {E} has a current limit of {v}
limit_sought | syn: new limit wanted, limit asked for | say: {E} seeks a limit of {v}
average_days_to_pay | syn: payment speed, average payment days | say: {E} pays in {v} on average
agency_score | syn: credit score, bureau score | say: {E} holds an agency score of {v}
current_ratio | syn: liquidity ratio, assets to liabilities | say: {E} has a current ratio of {v}
review_trigger | syn: review reason, cause of review | say: {E} was opened for a {v}
statement_type | syn: kind of accounts, financial evidence | say: {E} is supported by {v}
score_band | syn: hazard band, agency band | say: {E} sits in the {v} band
insurer_cover_granted | syn: credit insurance cover, insurer approval | pos: {E} has credit insurer cover granted | neg: {E} has no credit insurer cover granted | br: credit protection | nr: insurer limit letter | imp: covered loss
statements_received | syn: accounts received, financials in | pos: {E} has the customer's statements received | neg: {E} does not have the customer's statements received | br: financial evidence | nr: audited accounts in hand | imp: ratio analysis possible
parent_guarantee | syn: parent company guarantee, group guarantee | pos: {E} is backed by a parent guarantee | neg: {E} is not backed by a parent guarantee | br: credit support | nr: signed group letter | imp: parent liability
legal_action_open | syn: court claim open, lawsuit against the customer | pos: {E} concerns a customer facing open legal action | neg: {E} concerns a customer facing no open legal action | br: legal trouble | nr: county court claim | imp: credit hazard
over_limit_now | syn: above limit today, limit exceeded today | pos: {E} concerns a customer over the limit today | neg: {E} concerns a customer not over the limit today | br: credit excess | nr: order held at dispatch | imp: overdue exposure
reviewed_on | syn: review date, date reviewed | say: {E} was reviewed on {v}
next_review_on | syn: next review date, follow-up date | say: {E} sets the next review for {v}
review_tags | syn: review labels, review markers | say: {E} carries the review tags {v} | none: {E} carries none of the review tags
annual_purchases | syn: yearly purchases, spend per year | say: {E} buys {v} a year
years_trading_with_us | syn: trading relationship, years as a customer | say: {E} has traded with us for {v}
approval_authority | syn: signing authority, personal approval limit | say: {E} approves up to {v}
""",
"fo-08": """
transaction_amount | syn: charge value, purchase amount | say: {E} is for {v}
monthly_spend_so_far | syn: spend this month, month-to-date spend | say: {E} comes after {v} spent this month
card_limit | syn: monthly limit, card ceiling | say: {E} is on a card with a limit of {v}
hours_until_travel | syn: time before the trip, hours to departure | say: {E} comes {v} before travel
merchant_category | syn: merchant type, vendor category | say: {E} is at a {v} merchant
purchase_country | syn: country of purchase, purchase location | say: {E} was made in a {v}
policy_tier | syn: card tier, card class | say: {E} is on a {v}
manager_preapproved | syn: approved in advance, manager pre-clearance | pos: {E} was approved in advance by the manager | neg: {E} was not approved in advance by the manager | br: prior approval | nr: approval email from the manager | imp: spend authorised
receipts_up_to_date | syn: receipts current, expense receipts filed | pos: {E} comes from a cardholder with receipts up to date | neg: {E} comes from a cardholder with receipts not up to date | br: expense compliance | nr: last month's receipts uploaded | imp: clean expense history
fraud_alert_open | syn: issuer fraud alert, fraud flag on the card | pos: {E} is on a card with an open fraud alert | neg: {E} is on a card with no open fraud alert | br: card security problem | nr: suspicious charge hold | imp: card freeze
trip_booked_through_agency | syn: booked through the travel agency, agency booking | pos: {E} is for a trip booked through the agency | neg: {E} is not for a trip booked through the agency | br: travel policy compliance | nr: agency itinerary number | imp: negotiated fare
personal_use_flag | syn: personal charge found, private use flag | pos: {E} comes after a personal use flag on the card | neg: {E} comes after no personal use flag on the card | br: policy breach | nr: grocery charge on the card | imp: repayment owed
charged_on | syn: charge date, transaction date | say: {E} was charged on {v}
statement_closes_on | syn: statement close date, cycle end | say: {E} falls in a statement that closes on {v}
authorization_tags | syn: authorization labels, authorization markers | say: {E} carries the authorization tags {v} | none: {E} carries none of the authorization tags
late_expense_reports | syn: late reports, overdue expense reports | say: {E} has filed {v} late this year
years_with_card | syn: card tenure, cardholding years | say: {E} has held a card for {v}
blocked_category | syn: barred merchant type, restricted category | pos: {E} is in a category blocked by policy | neg: {E} is not in a category blocked by policy | br: policy restriction | nr: gambling merchant | imp: automatic block code
""",
"fo-09": """
entry_amount | syn: journal value, posting amount | say: {E} posts {v}
lines_in_entry | syn: line count, journal lines | say: {E} has {v}
hours_after_cutoff | syn: time after cutoff, delay past cutoff | say: {E} came in {v} after the cutoff
unreconciled_difference | syn: open difference, reconciling gap | say: {E} leaves a reconciling difference of {v}
entry_type | syn: journal type, kind of entry | say: {E} is a {v}
account_class | syn: account group, ledger class | say: {E} hits {v} accounts
materiality_band | syn: materiality grade, size grade | say: {E} is rated {v}
support_attached | syn: backup attached, workpaper attached | pos: {E} has support attached | neg: {E} has no support attached | br: audit evidence | nr: invoice copy attached | imp: entry documented
second_reviewer_signed | syn: second review done, independent sign-off | pos: {E} carries a second reviewer's signature | neg: {E} does not carry a second reviewer's signature | br: segregation of duties | nr: controller initials | imp: entry reviewed
auto_reversing | syn: reverses next month, automatic reversal set | pos: {E} is set to reverse automatically | neg: {E} is not set to reverse automatically | br: temporary entry | nr: accrual reversal flag | imp: next-period reversal
posted_by_preparer | syn: preparer posted it, self-posted entry | pos: {E} was posted by its own preparer | neg: {E} was not posted by its own preparer | br: control weakness | nr: same user prepared and posted | imp: duties conflict
prior_period_impact | syn: earlier period affected, closed period touched | pos: {E} affects a closed period | neg: {E} does not affect a closed period | br: restatement concern | nr: change to last quarter | imp: period reopening
prepared_on | syn: preparation date, date drafted | say: {E} was prepared on {v}
period_end | syn: period close date, end of period | say: {E} belongs to the period ending {v}
journal_tags | syn: journal labels, journal markers | say: {E} carries the journal tags {v} | none: {E} carries none of the journal tags
journals_this_close | syn: entries this close, journals prepared this close | say: {E} has prepared {v} this close
corrections_last_quarter | syn: entries corrected, correction count last quarter | say: {E} had {v} corrected last quarter
balance_variance_percent | syn: balance swing, month-on-month swing | say: {E} moved by {v} month on month
""",
"fo-10": """
invoice_total | syn: invoice value, bill amount | say: {E} totals {v}
price_variance_percent | syn: price gap, unit price difference | say: {E} differs from the order price by {v}
quantity_variance_units | syn: quantity gap, unit difference | say: {E} differs from the received quantity by {v}
days_until_due | syn: days to the due date, payment window | say: {E} falls due in {v}
early_pay_discount | syn: early payment discount, cash discount | say: {E} offers {v} off for early payment
invoice_kind | syn: invoice type, bill type | say: {E} is a {v} invoice
receipt_status | syn: goods receipt state, delivery state | say: {E} shows the goods {v}
tolerance_class | syn: tolerance band, match band | say: {E} uses a {v} tolerance
receipt_posted | syn: goods receipt posted, delivery booked in | pos: {E} has a goods receipt posted | neg: {E} has no goods receipt posted | br: delivery evidence | nr: warehouse scan of the pallet | imp: goods arrived
po_approved | syn: order approved, purchase order signed off | pos: {E} has an approved purchase order | neg: {E} has no approved purchase order | br: purchasing authority | nr: buyer approval on the order | imp: committed spend
duplicate_suspected | syn: apparent repeat invoice, duplicate flag | pos: {E} looks like a duplicate | neg: {E} does not look like a duplicate | br: double payment hazard | nr: same invoice number twice | imp: payment hold
bank_details_changed | syn: supplier bank change, new remittance account | pos: {E} comes from a supplier whose bank details changed recently | neg: {E} comes from a supplier whose bank details did not change recently | br: payment fraud signal | nr: new account number on the letterhead | imp: callback check
tax_correct | syn: tax lines correct, tax agrees with the order | pos: {E} has correct tax lines | neg: {E} does not have correct tax lines | br: tax compliance | nr: sales tax rate matches | imp: input tax claimable
invoiced_on | syn: invoice date, billing date | say: {E} was issued on {v}
due_on | syn: due date, payment due date | say: {E} falls due on {v}
invoice_tags | syn: invoice labels, invoice markers | say: {E} carries the invoice tags {v} | none: {E} carries none of the invoice tags
invoices_this_month | syn: monthly invoice count, bills sent this month | say: {E} has sent {v} this month
open_orders | syn: open purchase orders, live orders | say: {E} has {v} open
""",
}
