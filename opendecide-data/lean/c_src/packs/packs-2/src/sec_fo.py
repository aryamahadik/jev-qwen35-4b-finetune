"""packs-2 sector fo: finance operations (Claude-written pack sources; invented companies and entities)."""

PACKS = [
dict(slot="fo-01", slug="counterparty-limits", sector="finance_ops",
     sub="treasury desk monitoring counterparty exposure limits for deposits and hedges",
     org="Ardent Vale Manufacturing Group Treasury", desk="treasury risk desk",
     setting="A manufacturing group's treasury places cash deposits and currency hedges with several banks. The "
             "treasury risk desk checks each new trade against counterparty limits and rating rules before it is "
             "booked.",
     decider="financial risk specialist",
     roles="treasury analyst; treasurer; trade settlements clerk; group controller; bank relationship manager; "
           "internal auditor",
     docs="trade ticket; limit report; rating watch notice; board limit policy; confirmation statement; "
          "breach memo",
     scope=("treasury entity", "Group Holding; European Hub; Asia Hub; Americas Hub"),
     money="euros",
     ents=[
        dict(key="trade", singular="treasury trade", plural="treasury trades", id="TT", aka="deal",
             attrs="""
             notional | money | 50000.00..80000000.00 | aka=trade amount
             tenor_days | int | 1..730 days | aka=maturity in days
             limit_used_after | dec1 | 0.0..150.0 percent | aka=limit usage after the trade
             trades_with_bank_today | int | 0..20 items | aka=same-day trades with the bank
             instrument | cat | term deposit; currency forward; money market fund; repo; interest rate swap
             trade_currency | cat | EUR; USD; GBP; CHF; JPY
             rating_band | ord | sub-investment; lower investment; upper investment; top tier | aka=bank rating band
             confirmation_matched | event | bad=0 | aka=bank confirmation agrees | grp=confirmation
             board_exception_granted | event | bad=0 | aka=board approved an exception
             rating_watch_negative | state | bad=1 | aka=bank on rating watch
             netting_agreement | state | bad=0 | aka=master netting agreement in place
             breach_last_quarter | event | bad=1 | aka=limit breached last quarter
             traded_on | date
             matures_on | date
             trade_tags | tag | month end; hedge rollover; new bank; group internal; collateralized
             """),
        dict(key="bank", singular="counterparty bank", plural="counterparty banks", id="CB",
             names="org: Bank, Banque, Bancorp, Savings Bank",
             attrs="""
             total_limit | money | 1000000.00..250000000.00 | aka=approved limit
             years_relationship | int | 0..40 years | aka=relationship length
             """),
        dict(key="dealer", singular="treasury dealer", plural="treasury dealers", id="TD", names="person",
             role="person",
             attrs="""
             dealer_limit | money | 100000.00..50000000.00 | aka=personal dealing limit
             trades_this_month | int | 0..200 items | aka=trades this month
             """),
     ],
     outcomes=["book trade; book and report to treasurer; split across banks; send to group controller; "
               "block trade*; close out trade*",
               "keep within limit; temporary limit increase; reduce exposure*"],
     levels=["sub-investment; lower investment; upper investment; top tier", "green; amber; red"],
     words="""
     jumbo: notional >= 20000000
     modest: notional < 250000
     protracted: tenor_days >= 365
     overnight: tenor_days < 2
     stretched: limit_used_after >= 90
     excessive: limit_used_after > 100
     busy: trades_with_bank_today >= 5
     reconciled: confirmation_matched
     exempted: board_exception_granted
     shaky: rating_watch_negative
     offset: netting_agreement
     enduring: years_relationship >= 15
     derivative: instrument in {currency forward, interest rate swap}
     """,
     cues="lacks a matching bank confirmation => confirmation_matched=false; has no netting agreement => "
          "netting_agreement=false; was never granted a board exception => board_exception_granted=false",
     links="trade > bank: places with / chosen for; trade > dealer: credits / credited by",
     actions="book = enter trade; confirm = affirm; terminate = close out; report = escalate",
     sources="trade ticket; bank confirmation; rating agency notice; treasurer email; limit report; "
             "settlement system",
     inert="""
     wall_screen_side | cat | left screen; right screen
     treasury_mug | cat | blue mug; grey mug
     terminal_keyboard | cat | black keys; white keys
     window_blind_angle | cat | open blinds; tilted blinds
     wall_ticker_colour | cat | green ticker; amber ticker
     """,
     affix="unmatched => confirmation_matched; unnetted => netting_agreement"),

dict(slot="fo-02", slug="payroll-adjustments", sector="finance_ops",
     sub="payroll desk processing adjustments and off-cycle payments",
     org="Brightwater Logistics Payroll Office", desk="payroll adjustments desk",
     setting="A logistics company's payroll office corrects pay errors and issues off-cycle payments between "
             "regular runs. The adjustments desk applies the company's pay rules, approval limits and cut-off "
             "times to each adjustment.",
     decider="payroll clerk",
     roles="payroll specialist; payroll manager; human resources partner; line manager; benefits clerk; "
           "finance controller",
     docs="adjustment form; timesheet; pay statement; off-cycle register; approval matrix; garnishment order",
     scope=("pay group", "Weekly Hourly; Biweekly Hourly; Monthly Salaried; Drivers"),
     money="dollars",
     ents=[
        dict(key="adjustment", singular="pay adjustment", plural="pay adjustments", id="PJ", aka="pay correction",
             attrs="""
             adjustment_amount | money | -5000.00..15000.00 | aka=amount to adjust | signed
             hours_corrected | dec2 | 0.25..80.00 hours | aka=hours fixed
             days_since_pay_date | int | 0..365 days | aka=age of the error
             periods_affected | int | 1..12 items | aka=pay periods touched
             adjustment_kind | cat | missed overtime; wrong rate; shift premium; retro raise; overpayment recovery; bonus
             payment_route | cat | next regular run; off-cycle direct deposit; manual cheque
             approval_tier | ord | supervisor; payroll manager; controller | aka=approval level
             timesheet_attached | state | bad=0 | aka=timesheet on file | grp=evidence
             manager_signed | event | bad=0 | aka=line manager approved
             garnishment_active | state | bad=1 | aka=court-ordered deduction in place
             employee_terminated | state | bad=1 | aka=employee has left
             tax_year_closed | state | bad=1 | aka=year-end already filed
             error_confirmed_by_payroll | event | bad=0 | aka=payroll confirmed the error
             reported_on | date
             pay_date | date
             adjustment_tags | tag | union rate; night shift; holiday pay; travel time; training hours
             """),
        dict(key="employee", singular="employee", plural="employees", id="EM", names="person", role="person",
             attrs="""
             hourly_rate | money | 14.00..95.00 | aka=pay rate
             adjustments_this_year | int | 0..15 items | aka=earlier corrections
             """),
        dict(key="manager", singular="line manager", plural="line managers", id="MG", names="person",
             role="person",
             attrs="""
             team_size | int | 2..60 people | aka=direct reports
             """),
     ],
     outcomes=["pay on next run; pay off-cycle; recover over three periods; send to payroll manager; "
               "return for timesheet*; hold adjustment*",
               "direct deposit; manual cheque; pay card; offset against next pay*"],
     levels=["supervisor; payroll manager; controller", "low; medium; high"],
     words="""
     hefty: adjustment_amount >= 2000
     repayment: adjustment_amount < 0
     lengthy: hours_corrected >= 20
     stale: days_since_pay_date >= 90
     fresh: days_since_pay_date <= 7
     sweeping: periods_affected >= 4
     documented: timesheet_attached
     endorsed: manager_signed
     seized: garnishment_active
     gone: employee_terminated
     lucrative: hourly_rate >= 50
     repeat: adjustments_this_year >= 3
     retroactive: adjustment_kind == retro raise
     belated: tax_year_closed
     """,
     cues="lacks a timesheet => timesheet_attached=false; was never approved by the line manager => "
          "manager_signed=false; has no court-ordered deduction => garnishment_active=false",
     links="adjustment > employee: pays / paid by; adjustment > manager: cites / cited by",
     actions="post = enter; recover = claw back; reissue = pay again; approve = sign off",
     sources="adjustment form; timesheet system; manager email; employee phone call; pay register; "
             "garnishment notice",
     inert="""
     payslip_paper | cat | white stock; blue stock
     office_printer_name | cat | printer orchid; printer cobalt
     stamp_ink | cat | red ink; black ink
     calendar_picture | cat | trucks; bridges
     desk_fan_speed | cat | slow fan; fast fan
     """,
     affix="unsigned => manager_signed; undocumented => timesheet_attached"),

dict(slot="fo-03", slug="purchase-requisitions", sector="finance_ops",
     sub="purchasing desk approving requisitions under quote and approval rules",
     org="Calder Ridge Regional Hospital Purchasing", desk="purchasing desk",
     setting="A hospital's purchasing department turns staff requisitions into purchase orders. The purchasing "
             "desk applies spend thresholds, competitive quote rules and contract checks before a purchase order is "
             "issued.",
     decider="purchasing agent",
     roles="buyer; department head; budget analyst; contracts manager; receiving clerk; finance chief",
     docs="requisition; quote summary; contract register; sole-source form; purchase order; budget report",
     scope=("cost center", "Surgery; Pharmacy; Facilities; Information Technology; Nutrition Services"),
     money="dollars",
     ents=[
        dict(key="requisition", singular="purchase requisition", plural="purchase requisitions", id="PR",
             aka="requisition",
             attrs="""
             total_value | money | 25.00..900000.00 | aka=requisition value
             quotes_received | int | 0..6 items | aka=number of quotes
             days_needed_in | int | 1..120 days | aka=time until needed
             budget_left_percent | dec1 | 0.0..100.0 percent | aka=budget remaining
             category | cat | medical supplies; equipment; software; services; furniture; food
             buying_route | cat | catalog; contract item; spot buy; emergency buy
             approval_level | ord | department head; director; finance chief; board | aka=approval tier
             contract_on_file | state | bad=0 | aka=vendor contract exists | grp=contract
             sole_source_justified | event | bad=0 | aka=single-source form approved
             budget_checked | event | bad=0 | aka=budget check done
             capital_item | state | bad=0 | aka=counts as a capital asset
             split_order_suspected | state | bad=1 | aka=looks split to dodge a threshold
             raised_on | date
             needed_by | date
             requisition_tags | tag | recall replacement; grant funded; pilot; urgent patient need; recurring
             """),
        dict(key="vendor", singular="vendor", plural="vendors", id="VN",
             names="org: Medical Supply, Systems, Furnishings, Services",
             attrs="""
             on_time_rate | dec1 | 50.0..100.0 percent | aka=delivery reliability
             vendor_approved | state | bad=0 | aka=an approved vendor
             """),
        dict(key="requester", singular="requisitioner", plural="requisitioners", id="RQ", names="person",
             role="person",
             attrs="""
             requisitions_this_month | int | 0..40 items | aka=requisitions this month
             """),
     ],
     outcomes=["issue purchase order; obtain more quotes; buy from contract vendor; send to finance chief; "
               "return to department*; reject requisition*",
               "standard delivery; expedited delivery*; split delivery"],
     levels=["department head; director; finance chief; board", "low; medium; high"],
     words="""
     major: total_value >= 100000
     petty: total_value < 500
     competitive: quotes_received >= 3
     rushed: days_needed_in <= 3
     tight: budget_left_percent < 10
     bound: contract_on_file
     warranted: sole_source_justified
     scrutinized: budget_checked
     durable: capital_item
     suspicious: split_order_suspected
     dependable: on_time_rate >= 95
     accredited: vendor_approved
     digital: category == software
     frantic: buying_route == emergency buy
     """,
     cues="lacks a vendor contract => contract_on_file=false; has no approved single-source form => "
          "sole_source_justified=false; was never budget checked => budget_checked=false",
     links="requisition > vendor: names / named by; requisition > requester: credits / credited by",
     actions="issue = raise order; quote = seek bids; source = choose vendor; reject = turn back",
     sources="requisition system; vendor quote; contract register; department head email; budget report; "
             "receiving log",
     inert="""
     dock_door_number | cat | door 3; door 6
     pallet_wrap_colour | cat | clear wrap; black wrap
     office_fern_pot | cat | jade plant; snake plant
     office_whiteboard | cat | tidy board; crowded board
     catalogue_binder | cat | green binder; red binder
     """,
     affix="unjustified => sole_source_justified; unchecked => budget_checked"),

dict(slot="fo-04", slug="collections", sector="finance_ops",
     sub="accounts receivable collections and payment arrangements",
     org="Hollowmere Utilities Billing Office", desk="collections desk",
     setting="A utility billing office follows up overdue customer accounts. The collections desk applies "
             "notice, payment-arrangement, hardship and service-limit rules to each overdue account.",
     decider="account collector",
     roles="collections agent; credit supervisor; hardship caseworker; field service dispatcher; "
           "customer service lead; billing analyst",
     docs="overdue notice; payment arrangement agreement; hardship application; account statement; "
          "final notice; call log",
     scope=("service region", "Northern District; Southern District; Valley Towns; Coastal Towns"),
     money="dollars",
     ents=[
        dict(key="account", singular="overdue account", plural="overdue accounts", id="AC", aka="past-due account",
             attrs="""
             balance_overdue | money | 20.00..9000.00 | aka=overdue balance
             days_past_due | int | 1..365 days | aka=days overdue
             arrangements_broken | int | 0..5 entries | aka=broken payment plans
             notices_sent | int | 0..6 items | aka=notices so far
             customer_class | cat | residential; small business; nonprofit; government
             contact_result | cat | promise to pay; left message; wrong number; spoke to customer
             hardship_level | ord | standard; moderate; severe | aka=hardship band
             medical_certificate | state | bad=0 | aka=medical protection on file | grp=protection
             winter_protection | state | bad=0 | aka=cold-weather protection period
             promise_kept_last_time | event | bad=0 | aka=last promise honoured
             autopay_enrolled | state | bad=0 | aka=automatic payments set up
             dispute_open | state | bad=1 | aka=billing dispute under way
             payment_received_this_week | event | bad=0 | aka=payment arrived this week
             last_payment_on | date
             next_notice_on | date
             account_tags | tag | elderly; landlord account; seasonal; repeat delinquency; new account
             """),
        dict(key="customer", singular="customer", plural="customers", id="CU", names="person", role="person",
             attrs="""
             years_as_customer | int | 0..50 years | aka=tenure
             deposit_held | money | 0.00..800.00 | aka=security deposit
             """),
        dict(key="agent", singular="collections agent", plural="collections agents", id="AG", names="person",
             role="person",
             attrs="""
             accounts_assigned | int | 20..900 items | aka=caseload
             """),
     ],
     outcomes=["offer payment arrangement; send final notice*; refer to hardship program; send to credit supervisor; "
               "limit service*; write off balance*",
               "six-month plan; twelve-month plan; pay in full*"],
     levels=["standard; moderate; severe", "low; medium; high"],
     words="""
     hefty: balance_overdue >= 1500
     trifling: balance_overdue < 100
     chronic: days_past_due >= 90
     fresh: days_past_due <= 15
     erratic: arrangements_broken >= 2
     pestered: notices_sent >= 4
     shielded: medical_certificate
     wintry: winter_protection
     trustworthy: promise_kept_last_time
     automated: autopay_enrolled
     contested: dispute_open
     enduring: years_as_customer >= 10
     commercial: customer_class == small business
     """,
     cues="lacks a medical protection certificate => medical_certificate=false; never honoured the last promise "
          "=> promise_kept_last_time=false; has no automatic payments set up => autopay_enrolled=false",
     links="account > customer: belongs to / owned by; account > agent: assigns / assigned by",
     actions="arrange = set plan; remind = chase; refer = pass on; settle = close balance",
     sources="call log; account statement; hardship caseworker note; customer letter; payment system; "
             "field service report",
     inert="""
     headset_cushion | cat | foam cushion; leather cushion
     call_queue_music | cat | piano loop; guitar loop
     stress_ball_colour | cat | red ball; yellow ball
     envelope_window_side | cat | left window; right window
     office_carpet | cat | grey carpet; blue carpet
     """,
     affix="unprotected => medical_certificate; unenrolled => autopay_enrolled"),

dict(slot="fo-05", slug="business-accounts", sector="finance_ops",
     sub="new business customer account opening with credit application checks",
     org="Torvald Wholesale Distributors", desk="new accounts desk",
     setting="A wholesale distributor opens trading accounts for business customers. The new accounts desk "
             "checks each application's documents, references and tax status before setting payment terms.",
     decider="new accounts clerk",
     roles="credit clerk; credit manager; sales representative; tax compliance clerk; customer master data "
           "analyst; branch manager",
     docs="credit application; trade reference letter; tax exemption certificate; bank reference; "
          "account set-up form; personal guarantee",
     scope=("branch", "Northside Depot; Southport Depot; Eastfield Depot; Online Desk"),
     money="dollars",
     ents=[
        dict(key="application", singular="account application", plural="account applications", id="AA",
             aka="credit application",
             attrs="""
             credit_sought | money | 500.00..250000.00 | aka=credit line asked for
             years_trading | int | 0..80 years | aka=time in business
             trade_references | int | 0..5 items | aka=references supplied
             expected_monthly_spend | money | 100.00..120000.00 | aka=projected monthly purchases
             business_form | cat | sole trader; partnership; limited company; cooperative; public body
             industry | cat | restaurant; contractor; retailer; school; clinic; hotel
             terms_tier | ord | cash on delivery; net 15; net 30; net 60 | aka=payment terms
             tax_certificate_valid | state | bad=0 | aka=tax exemption certificate current | grp=tax
             guarantee_signed | event | bad=0 | aka=owner guarantee signed
             bank_reference_received | event | bad=0 | aka=bank reference arrived
             address_matches_registry | state | bad=0 | aka=address agrees with the registry
             prior_account_closed_for_debt | event | bad=1 | aka=earlier account closed owing money
             applied_on | date
             first_order_on | date
             application_tags | tag | franchise; seasonal business; government buyer; export; new owner
             """),
        dict(key="owner", singular="business owner", plural="business owners", id="BW", names="person",
             role="person",
             attrs="""
             other_businesses | int | 0..6 items | aka=other firms owned
             """),
        dict(key="rep", singular="sales representative", plural="sales representatives", id="SR",
             names="person", role="person",
             attrs="""
             accounts_opened_this_quarter | int | 0..40 items | aka=new accounts this quarter
             """),
     ],
     outcomes=["open with requested terms; open with lower credit line; open cash on delivery*; "
               "send to credit manager; return for documents*; reject application*",
               "charge sales tax; exempt from sales tax; hold first order*"],
     levels=["cash on delivery; net 15; net 30; net 60", "low; medium; high"],
     words="""
     ambitious: credit_sought >= 50000
     modest: credit_sought < 2000
     established: years_trading >= 10
     fledgling: years_trading < 2
     vouched: trade_references >= 3
     lavish: expected_monthly_spend >= 20000
     privileged: tax_certificate_valid
     backed: guarantee_signed
     solvent: bank_reference_received
     consistent: address_matches_registry
     tainted: prior_account_closed_for_debt
     prolific: accounts_opened_this_quarter >= 15
     civic: business_form == public body
     """,
     cues="lacks a current tax exemption certificate => tax_certificate_valid=false; never signed the owner "
          "guarantee => guarantee_signed=false; has no bank reference => bank_reference_received=false",
     links="application > owner: names / named by; application > rep: credits / credited by",
     actions="activate = set up account; set terms = assign terms; verify = check references; reject = turn down",
     sources="credit application; bank letter; registry search; sales rep email; tax certificate; "
             "reference call notes",
     inert="""
     brochure_stand | cat | wire stand; wooden stand
     depot_forklift_colour | cat | yellow forklift; orange forklift
     counter_bell_tone | cat | high tone; low tone
     lobby_rug | cat | striped rug; plain rug
     desk_calendar_theme | cat | harbours; forests
     """,
     affix="unsigned => guarantee_signed; unbanked => bank_reference_received"),

dict(slot="fo-06", slug="capex-requests", sector="finance_ops",
     sub="capital expenditure request review for a restaurant group",
     org="Saffron Lane Restaurant Group", desk="capital budget office",
     setting="A restaurant group funds kitchen equipment, refits and new sites from a yearly capital budget. The "
             "capital budget office reviews each capital request against payback, budget and approval rules.",
     decider="financial manager",
     roles="finance analyst; operations director; site general manager; facilities lead; chief executive; "
           "procurement lead",
     docs="capital request form; payback schedule; vendor quote; capital budget tracker; board paper; "
          "post-completion review",
     scope=("brand", "Saffron Lane Bistro; Copper Kettle Diner; Harbour Noodle Bar; Garden Bakery"),
     money="pounds sterling",
     ents=[
        dict(key="request", singular="capital request", plural="capital requests", id="CX", aka="capex request",
             attrs="""
             project_cost | money | 2000.00..2500000.00 | aka=total cost
             payback_months | int | 3..120 months | aka=payback period
             budget_remaining | money | 0.00..5000000.00 | aka=capital budget left
             quotes_attached | int | 0..5 items | aka=quotes on file
             project_type | cat | kitchen equipment; dining room refit; new site; technology; safety upgrade
             funding_source | cat | annual budget; reserve fund; lease finance; landlord contribution
             urgency_grade | ord | discretionary; important; essential; safety critical | aka=urgency
             safety_mandated | state | bad=0 | aka=required by a safety inspection | grp=safety
             board_approved | event | bad=0 | aka=board sign-off given
             in_annual_budget | state | bad=0 | aka=included in this year's budget
             landlord_consent | event | bad=0 | aka=landlord agreed
             overspend_on_last_project | event | bad=1 | aka=last project ran over
             submitted_on | date
             start_on | date
             request_tags | tag | energy saving; brand refresh; replacement; growth; compliance
             """),
        dict(key="site", singular="restaurant site", plural="restaurant sites", id="RS",
             names="org: Kitchen, Bistro, Diner, Bakery",
             attrs="""
             weekly_sales | money | 8000.00..180000.00 | aka=sales per week
             site_age_years | int | 0..40 years | aka=age of the site
             """),
        dict(key="sponsor", singular="project sponsor", plural="project sponsors", id="PS", names="person",
             role="person",
             attrs="""
             projects_sponsored | int | 0..20 items | aka=earlier projects led
             """),
     ],
     outcomes=["approve request; approve phased spend; send to board; return for more quotes*; "
               "defer to next year*; reject request*",
               "fund from budget; fund by lease; fund from reserve; wait for next budget*"],
     levels=["discretionary; important; essential; safety critical", "low; medium; high"],
     words="""
     major: project_cost >= 250000
     minor: project_cost < 10000
     lucrative: payback_months <= 18
     sluggish: payback_months >= 60
     tight: budget_remaining < 50000
     tendered: quotes_attached >= 3
     compulsory: safety_mandated
     endorsed: board_approved
     anticipated: in_annual_budget
     sanctioned: landlord_consent
     busy: weekly_sales >= 80000
     weathered: site_age_years >= 20
     expansive: project_type == new site
     spendthrift: overspend_on_last_project
     """,
     cues="lacks board sign-off => board_approved=false; has no landlord agreement => landlord_consent=false; "
          "was never included in this year's budget => in_annual_budget=false",
     links="request > site: targets / targeted by; request > sponsor: credits / credited by",
     actions="approve = sign off; phase = stage spend; defer = postpone; fund = allocate money",
     sources="capital request form; vendor quote; operations director email; budget tracker; board minutes; "
             "landlord letter",
     inert="""
     presentation_template | cat | template blue; template white
     meeting_biscuits | cat | shortbread; ginger
     projector_remote | cat | remote A; remote B
     boardroom_chair | cat | mesh chair; leather chair
     whiteboard_pen_colour | cat | black marker; green marker
     """,
     affix="unbudgeted => in_annual_budget; unapproved => board_approved"),

dict(slot="fo-07", slug="trade-credit", sector="finance_ops",
     sub="trade credit limit reviews for an industrial supplier's customers",
     org="Ironbridge Fasteners Credit Department", desk="credit review desk",
     setting="An industrial supplier sells on account to contractors and manufacturers. The credit review desk "
             "sets and revises each customer's credit limit using payment history, financial statements and "
             "credit agency scores.",
     decider="credit analyst",
     roles="credit controller; sales director; collections clerk; finance manager; account manager; "
           "credit insurance broker",
     docs="credit review memo; financial statements; agency score report; aged debt report; credit insurance "
          "notice; limit change letter",
     scope=("customer segment", "Contractors; Manufacturers; Distributors; Public Sector"),
     money="dollars",
     ents=[
        dict(key="review", singular="credit review", plural="credit reviews", id="KR", aka="limit review",
             attrs="""
             current_limit | money | 0.00..2000000.00 | aka=existing credit limit
             limit_sought | money | 1000.00..3000000.00 | aka=new limit asked for
             average_days_to_pay | int | 5..150 days | aka=days to pay
             agency_score | int | 1..100 points | aka=credit agency score
             current_ratio | dec2 | 0.20..5.00 points | aka=current assets over liabilities
             review_trigger | cat | annual review; limit increase; overdue balance; agency alert; ownership change
             statement_type | cat | audited accounts; management accounts; tax return; statement promised
             score_band | ord | high hazard; elevated; moderate; low; minimal | aka=agency band
             insurer_cover_granted | event | bad=0 | aka=credit insurer covers the limit | grp=insurance
             statements_received | event | bad=0 | aka=accounts received
             parent_guarantee | state | bad=0 | aka=parent company guarantee in place
             legal_action_open | state | bad=1 | aka=court claim against the customer
             over_limit_now | state | bad=1 | aka=balance above the limit today
             reviewed_on | date
             next_review_on | date
             review_tags | tag | new parent; seasonal peak; large project; export sales; key account
             """),
        dict(key="customer", singular="trade customer", plural="trade customers", id="TC",
             names="org: Construction, Engineering, Fabrication, Supplies",
             attrs="""
             annual_purchases | money | 1000.00..10000000.00 | aka=yearly spend
             years_trading_with_us | int | 0..40 years | aka=relationship length
             """),
        dict(key="analyst", singular="credit analyst", plural="credit analysts", id="CN", names="person",
             role="person",
             attrs="""
             approval_authority | money | 10000.00..500000.00 | aka=personal approval limit
             """),
     ],
     outcomes=["raise limit as asked; raise limit partly; keep limit; reduce limit*; send to finance manager; "
               "stop credit*",
               "standard terms; shorter terms*; cash in advance*; longer terms"],
     levels=["high hazard; elevated; moderate; low; minimal", "low; medium; high"],
     words="""
     generous: current_limit >= 500000
     ambitious: limit_sought >= 1000000
     sluggish: average_days_to_pay >= 75
     prompt: average_days_to_pay <= 30
     strong: agency_score >= 80
     weak: agency_score < 30
     liquid: current_ratio >= 1.50
     strained: current_ratio < 1.00
     assured: insurer_cover_granted
     sheltered: parent_guarantee
     sued: legal_action_open
     loyal: years_trading_with_us >= 10
     flagged: review_trigger == agency alert
     """,
     cues="lacks credit insurer cover => insurer_cover_granted=false; has no parent company guarantee => "
          "parent_guarantee=false; never sent its accounts => statements_received=false",
     links="review > customer: concerns / concerned by; review > analyst: assigns / assigned by",
     actions="raise = increase limit; reduce = lower limit; stop = freeze account; review = assess",
     sources="credit agency report; aged debt report; sales director email; customer accounts; "
             "insurer notice; collections note",
     inert="""
     report_binder_tab | cat | yellow tab; orange tab
     corner_plant | cat | rubber plant; palm
     printer_toner | cat | toner one; toner two
     office_window | cat | river view; car park view
     desk_organiser | cat | wire organiser; wood organiser
     """,
     affix="uninsured => insurer_cover_granted; unguaranteed => parent_guarantee"),

dict(slot="fo-08", slug="card-authorizations", sector="finance_ops",
     sub="corporate card program desk authorizing transactions and limit exceptions",
     org="Northmere Engineering Corporate Card Program", desk="card program desk",
     setting="An engineering firm issues corporate cards to staff for travel and purchases. The card program "
             "desk decides on declined-transaction overrides and temporary limit raises under the card policy.",
     decider="credit authorizer",
     roles="card program administrator; travel manager; cost center manager; expense auditor; "
           "card issuer liaison; finance director",
     docs="card policy; authorization log; limit exception form; merchant category list; expense report; "
          "card statement",
     scope=("business unit", "Civil Projects; Energy Projects; Design Studio; Corporate Office"),
     money="dollars",
     ents=[
        dict(key="authorization", singular="card authorization", plural="card authorizations", id="CA",
             aka="override",
             attrs="""
             transaction_amount | money | 1.00..60000.00 | aka=charge amount
             monthly_spend_so_far | money | 0.00..80000.00 | aka=spend this month
             card_limit | money | 1000.00..100000.00 | aka=monthly card limit
             hours_until_travel | int | 0..240 hours | aka=time until the trip
             merchant_category | cat | airline; hotel; car rental; software; office supplies; restaurant; equipment rental
             purchase_country | cat | home country; neighbouring country; overseas
             policy_tier | ord | standard card; travel card; purchasing card | aka=card type
             manager_preapproved | event | bad=0 | aka=manager approved ahead | grp=approval
             receipts_up_to_date | state | bad=0 | aka=past receipts submitted
             fraud_alert_open | state | bad=1 | aka=issuer fraud alert on the card
             trip_booked_through_agency | event | bad=0 | aka=trip booked via the travel agency
             personal_use_flag | event | bad=1 | aka=earlier personal charge found
             charged_on | date
             statement_closes_on | date
             authorization_tags | tag | conference; client entertainment; site visit; emergency repair; relocation
             """),
        dict(key="cardholder", singular="cardholder", plural="cardholders", id="CH", names="person", role="person",
             attrs="""
             late_expense_reports | int | 0..10 items | aka=late reports this year
             years_with_card | int | 0..25 years | aka=card tenure
             """),
        dict(key="merchant", singular="merchant", plural="merchants", id="MR",
             names="org: Airways, Hotels, Rentals, Supplies",
             attrs="""
             blocked_category | state | bad=1 | aka=merchant type blocked by policy
             """),
     ],
     outcomes=["approve override; approve with temporary limit; send to finance director; "
               "ask for manager approval*; reject transaction*; suspend card*",
               "one-time raise; raise for the month; keep limit*"],
     levels=["standard card; travel card; purchasing card", "low; medium; high"],
     words="""
     hefty: transaction_amount >= 5000
     trivial: transaction_amount < 50
     heavy: monthly_spend_so_far >= 20000
     generous: card_limit >= 50000
     imminent: hours_until_travel <= 12
     cleared: manager_preapproved
     tidy: receipts_up_to_date
     suspicious: fraud_alert_open
     sanctioned: trip_booked_through_agency
     tardy: late_expense_reports >= 3
     veteran: years_with_card >= 10
     foreign: purchase_country == overseas
     aerial: merchant_category == airline
     errant: personal_use_flag
     """,
     cues="lacks manager approval => manager_preapproved=false; has no up-to-date receipts => "
          "receipts_up_to_date=false; was never booked through the agency => trip_booked_through_agency=false",
     links="authorization > cardholder: charges / charged by; authorization > merchant: pays / paid by",
     actions="authorize = clear charge; raise = lift limit; suspend = freeze card; review = audit",
     sources="authorization log; issuer alert; manager email; expense system; travel agency record; "
             "card statement",
     inert="""
     plastic_finish | cat | silver design; navy design
     wallet_colour | cat | brown wallet; black wallet
     lobby_screen_logo | cat | logo one; logo two
     keyring_shape | cat | round keyring; square keyring
     desk_phone_model | cat | model K; model Q
     """,
     affix="unapproved => manager_preapproved; unsanctioned => trip_booked_through_agency"),

dict(slot="fo-09", slug="journal-review", sector="finance_ops",
     sub="month-end close journal entry review and reconciliation sign-off",
     org="Quarrington Retail Holdings Finance", desk="close and consolidation desk",
     setting="At month end, a retail group's accountants post manual journal entries and reconcile balance sheet "
             "accounts. The close desk reviews each manual entry against the journal policy and decides whether it "
             "posts.",
     decider="accountant",
     roles="general ledger accountant; financial controller; internal auditor; accounts payable lead; "
           "tax accountant; reporting analyst",
     docs="journal entry form; support schedule; reconciliation workbook; close checklist; audit query; "
          "journal policy",
     scope=("ledger entity", "UK Retail; Ireland Retail; Online Store; Property Company"),
     money="pounds sterling",
     ents=[
        dict(key="journal", singular="manual journal", plural="manual journals", id="JE", aka="journal entry",
             attrs="""
             entry_amount | money | 1.00..5000000.00 | aka=journal amount
             lines_in_entry | int | 2..200 lines | aka=journal lines
             hours_after_cutoff | int | 0..72 hours | aka=time after the close cutoff
             unreconciled_difference | money | -50000.00..50000.00 | aka=open reconciliation difference | signed
             entry_type | cat | accrual; reclassification; correction; intercompany; provision; reversal
             account_class | cat | revenue; cost of sales; payroll; fixed assets; cash; tax
             materiality_band | ord | trivial; minor; material; highly material | aka=size band
             support_attached | state | bad=0 | aka=supporting workpaper attached | grp=support
             second_reviewer_signed | event | bad=0 | aka=independent reviewer approved
             auto_reversing | state | bad=0 | aka=set to reverse next month
             posted_by_preparer | event | bad=1 | aka=preparer also posted it
             prior_period_impact | state | bad=1 | aka=affects a closed period
             prepared_on | date
             period_end | date
             journal_tags | tag | year end; audit adjustment; recurring; top-side; foreign currency
             """),
        dict(key="preparer", singular="preparer", plural="preparers", id="PP", names="person", role="person",
             attrs="""
             journals_this_close | int | 0..80 items | aka=entries this close
             corrections_last_quarter | int | 0..15 items | aka=entries corrected last quarter
             """),
        dict(key="account", singular="ledger account", plural="ledger accounts", id="GK",
             names=["Account 1200 Cash at Bank", "Account 2100 Trade Creditors", "Account 4000 Store Sales", "Account 5100 Stock Purchases", "Account 6200 Wages", "Account 1500 Fixtures", "Account 2400 Accruals", "Account 8000 Tax Charge"],
             attrs="""
             balance_variance_percent | dec1 | 0.0..300.0 percent | aka=month-on-month change
             """),
     ],
     outcomes=["post entry; post after second review; return for support*; send to financial controller; "
               "reverse entry*; reject entry*",
               "post in current period; post in next period*; post as audit adjustment"],
     levels=["trivial; minor; material; highly material", "low; medium; high"],
     words="""
     huge: entry_amount >= 1000000
     trifling: entry_amount < 1000
     sprawling: lines_in_entry >= 50
     tardy: hours_after_cutoff >= 24
     punctual: hours_after_cutoff < 1
     substantiated: support_attached
     vetted: second_reviewer_signed
     fleeting: auto_reversing
     conflicted: posted_by_preparer
     retrospective: prior_period_impact
     busy: journals_this_close >= 40
     volatile: balance_variance_percent >= 50
     significant: materiality_band >= material
     remedial: entry_type == correction
     """,
     cues="lacks a supporting schedule => support_attached=false; was never approved by an independent reviewer "
          "=> second_reviewer_signed=false; has no reversal set => auto_reversing=false",
     links="journal > preparer: credits / credited by; journal > account: debits / debited by",
     actions="post = book; reverse = back out; reconcile = tie out; review = check entry",
     sources="journal entry form; reconciliation workbook; controller email; audit query; close checklist; "
             "ledger report",
     inert="""
     wall_chart_colour | cat | purple calendar; teal calendar
     spreadsheet_font | cat | font serif; font sans
     office_snack_drawer | cat | biscuits; nuts
     monitor_stand | cat | arm stand; block stand
     headphones_style | cat | over-ear; in-ear
     """,
     affix="unsupported => support_attached; unreviewed => second_reviewer_signed"),

dict(slot="fo-10", slug="invoice-matching", sector="finance_ops",
     sub="accounts payable three-way match of supplier invoices",
     org="Pellham Foods Accounts Payable", desk="invoice matching desk",
     setting="A food manufacturer pays supplier invoices only when they agree with the purchase order and the "
             "goods receipt. The invoice matching desk applies tolerance, approval and payment-hold rules to each "
             "invoice.",
     decider="procurement clerk",
     roles="payables clerk; buyer; receiving supervisor; payables manager; supplier relations analyst; "
           "treasury clerk",
     docs="supplier invoice; purchase order; goods receipt note; price variance report; payment run list; "
          "credit note",
     scope=("plant", "Bakery Plant; Dairy Plant; Frozen Foods Plant; Distribution Center"),
     money="dollars",
     ents=[
        dict(key="invoice", singular="supplier invoice", plural="supplier invoices", id="SV", aka="bill",
             attrs="""
             invoice_total | money | 10.00..750000.00 | aka=invoice amount
             price_variance_percent | dec1 | -20.0..20.0 percent | aka=price difference | signed
             quantity_variance_units | int | -500..500 units | aka=quantity difference | signed
             days_until_due | int | -30..90 days | aka=time to the due date | signed
             early_pay_discount | dec1 | 0.0..3.0 percent | aka=prompt payment discount
             invoice_kind | cat | goods; services; freight; utilities; credit adjustment
             receipt_status | cat | fully received; partly received; awaiting receipt
             tolerance_class | ord | tight; standard; wide | aka=match tolerance
             receipt_posted | event | bad=0 | aka=goods receipt posted | grp=receipt
             po_approved | state | bad=0 | aka=purchase order approved
             duplicate_suspected | state | bad=1 | aka=looks like a repeat invoice
             bank_details_changed | event | bad=1 | aka=supplier bank details changed recently
             tax_correct | state | bad=0 | aka=tax lines agree with the order
             invoiced_on | date
             due_on | date
             invoice_tags | tag | freight added; currency invoice; partial delivery; contract price; one-time vendor
             """),
        dict(key="supplier", singular="supplier", plural="suppliers", id="SP",
             names="org: Mills, Packaging, Dairies, Logistics",
             attrs="""
             invoices_this_month | int | 0..200 items | aka=invoices this month
             """),
        dict(key="buyer", singular="buyer", plural="buyers", id="BY", names="person", role="person",
             attrs="""
             open_orders | int | 0..300 items | aka=open purchase orders
             """),
     ],
     outcomes=["pay on due date; pay early for discount; hold for receipt*; send to buyer; "
               "ask for credit note*; block payment*",
               "include in next run; include in urgent run; exclude from run*"],
     levels=["tight; standard; wide", "low; medium; high"],
     words="""
     hefty: invoice_total >= 100000
     petty: invoice_total < 100
     overpriced: price_variance_percent > 2
     skimpy: quantity_variance_units < 0
     overdue: days_until_due < 0
     leisurely: days_until_due >= 30
     attractive: early_pay_discount >= 2
     delivered: receipt_posted
     authorized: po_approved
     suspicious: duplicate_suspected
     accurate: tax_correct
     prolific: invoices_this_month >= 50
     haulage: invoice_kind == freight
     """,
     cues="lacks a goods receipt => receipt_posted=false; has no approved purchase order => po_approved=false; "
          "was never checked for tax lines => tax_correct=false",
     links="invoice > supplier: pays / paid by; invoice > buyer: cites / cited by",
     actions="match = reconcile; release = pay; block = stop pay; credit = adjust down",
     sources="supplier invoice; purchase order system; receiving log; buyer email; supplier statement; "
             "bank change form",
     inert="""
     mailroom_tray_name | cat | queue red; queue blue
     letter_knife | cat | brass opener; steel opener
     inbox_tray_colour | cat | grey tray; black tray
     office_door_plaque | cat | sign A; sign B
     staple_remover | cat | claw remover; pen remover
     """,
     affix="unapproved => po_approved; unreceived => receipt_posted"),
]
