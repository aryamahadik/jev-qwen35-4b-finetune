"""packs-2 sector re: real-estate administration (Claude-written pack sources; invented firms and entities)."""

PACKS = [
dict(slot="re-01", slug="appraisal-review", sector="real_estate_admin",
     sub="lender appraisal review desk checking home appraisals before loan approval",
     org="Fairmount Home Lending Appraisal Review", desk="appraisal review desk",
     setting="A mortgage lender reviews each home appraisal before a loan is approved. The appraisal review desk "
             "checks comparable sales, adjustments and report completeness and decides whether the value is "
             "accepted.",
     decider="real estate appraiser",
     roles="review appraiser; loan processor; appraisal management coordinator; underwriter; staff appraiser; "
           "quality control analyst",
     docs="appraisal report; comparable sales grid; review checklist; revision letter; field review; "
          "valuation policy",
     scope=("market area", "Old Town; Lakeside Estates; Ridge Heights; Meadow Park; River Flats"),
     money="dollars",
     ents=[
        dict(key="appraisal", singular="appraisal report", plural="appraisal reports", id="AR",
             aka="home appraisal",
             attrs="""
             appraised_value | money | 60000.00..3000000.00 | aka=value given
             contract_price | money | 60000.00..3000000.00 | aka=agreed sale price
             net_adjustment_percent | dec1 | 0.0..40.0 percent | aka=net adjustments
             comps_within_one_mile | int | 0..6 items | aka=nearby comparable sales
             oldest_comp_months | int | 0..24 months | aka=age of the oldest comparable
             property_type | cat | detached house; townhouse; condominium; two-unit; manufactured home
             report_form | cat | full interior; exterior only; desktop
             condition_rating | ord | C6; C5; C4; C3; C2; C1 | aka=condition grade
             photos_included | state | bad=0 | aka=required photos present | grp=report
             repairs_required | state | bad=1 | aka=appraiser named required repairs
             appraiser_licensed_state | state | bad=0 | aka=appraiser licensed in the state
             sent_back_before | event | bad=1 | aka=report returned once already
             field_review_done | event | bad=0 | aka=second appraiser visited
             inspected_on | date
             report_on | date
             appraisal_tags | tag | new construction; rural; waterfront; accessory unit; declining market
             """),
        dict(key="appraiser", singular="appraiser", plural="appraisers", id="AP", names="person", role="person",
             attrs="""
             reports_reviewed_this_year | int | 0..200 items | aka=reports reviewed this year
             revision_rate | dec1 | 0.0..60.0 percent | aka=share sent back
             """),
        dict(key="borrower", singular="borrower", plural="borrowers", id="BR", names="person", role="person",
             attrs="""
             loan_to_value | dec1 | 30.0..100.0 percent | aka=loan as a share of value
             """),
     ],
     outcomes=["accept value; accept with conditions; ask for revision*; order field review; "
               "send to underwriter; reject appraisal*",
               "use appraised value; use contract price; use reviewed value*"],
     levels=["C6; C5; C4; C3; C2; C1", "low; medium; high"],
     words="""
     luxury: appraised_value >= 1000000
     modest: appraised_value < 150000
     pricey: contract_price >= 750000
     doctored: net_adjustment_percent >= 15
     sparse: comps_within_one_mile < 2
     stale: oldest_comp_months >= 12
     photographed: photos_included
     flawed: repairs_required
     accredited: appraiser_licensed_state
     reworked: sent_back_before
     audited: field_review_done
     leveraged: loan_to_value >= 90
     remote: report_form == desktop
     """,
     cues="lacks the required photos => photos_included=false; holds no license in the state => "
          "appraiser_licensed_state=false; never had a second appraiser visit => field_review_done=false",
     links="appraisal > appraiser: credits / credited by; appraisal > borrower: names / named by",
     actions="review = check report; revise = send back; accept = approve value; order = commission review",
     sources="appraisal report; sales database; appraiser email; loan processor note; field review report; "
             "photo set",
     inert="""
     cover_logo_shape | cat | logo square; logo round
     office_coffee_blend | cat | black coffee; latte
     monitor_count | cat | two monitors; three monitors
     office_aquarium | cat | angelfish; tetras
     window_shade | cat | roller shade; venetian blind
     """,
     affix="unlicensed => appraiser_licensed_state; unreviewed => field_review_done"),

dict(slot="re-02", slug="showings-offers", sector="real_estate_admin",
     sub="brokerage transaction desk booking showings and submitting offers",
     org="Brightmoor Realty Group", desk="transaction coordination desk",
     setting="A residential brokerage books property showings and sends buyers' offers to listing agents. The "
             "transaction desk applies showing, disclosure and offer-checklist rules before anything goes out.",
     decider="real estate sales agent",
     roles="transaction coordinator; listing agent; buyer agent; managing broker; showing service clerk; "
           "escrow liaison",
     docs="showing log; offer checklist; purchase agreement; seller disclosure; proof of funds letter; "
          "pre-approval letter",
     scope=("office", "Downtown Office; Northshore Office; Valley Office; Lakeview Office"),
     money="dollars",
     ents=[
        dict(key="offer", singular="purchase offer", plural="purchase offers", id="PF", aka="buyer offer",
             attrs="""
             offer_price | money | 50000.00..4000000.00 | aka=price offered
             asking_price | money | 50000.00..4000000.00 | aka=seller's price
             earnest_money | money | 0.00..200000.00 | aka=deposit offered
             days_to_close | int | 7..120 days | aka=closing timeline
             competing_offers | int | 0..15 items | aka=other offers on the table
             financing_type | cat | cash; conventional loan; government loan; seller financing
             contingency_mix | cat | inspection and financing; inspection only; financing only; waived all
             offer_strength | ord | weak; fair; strong; very strong | aka=agent's strength grade
             preapproval_attached | state | bad=0 | aka=lender letter attached | grp=funds
             proof_of_funds_attached | state | bad=0 | aka=bank statement attached | grp=funds
             disclosure_acknowledged | event | bad=0 | aka=buyer signed the disclosure
             showing_completed | event | bad=0 | aka=buyer toured the home
             escalation_clause | state | bad=0 | aka=automatic increase clause
             written_on | date
             expires_on | date
             offer_tags | tag | first-time buyer; investor; relocation; estate sale; new build
             """),
        dict(key="buyer", singular="buyer", plural="buyers", id="BY", names="person", role="person",
             attrs="""
             offers_made_before | int | 0..12 items | aka=earlier offers written
             """),
        dict(key="property", singular="property for sale", plural="properties for sale", id="KT",
             names=["Home at 14 Larch Way", "Home at 207 Mill Road", "Home at 9 Harbour Row", "Home at 51 Quarry Lane", "Home at 88 Cedar Court", "Home at 3 Orchard Rise", "Home at 120 Elm Street", "Home at 16 Kestrel Close"],
             attrs="""
             days_on_market | int | 0..365 days | aka=time on the market
             price_cuts | int | 0..5 entries | aka=price reductions
             """),
     ],
     outcomes=["send offer now; send after documents; send to managing broker; hold offer*; "
               "withdraw offer*",
               "accept counter; make counter; walk away*"],
     levels=["weak; fair; strong; very strong", "low; medium; high"],
     words="""
     bold: offer_price >= 1000000
     modest: offer_price < 100000
     generous: earnest_money >= 50000
     quick: days_to_close <= 21
     contested: competing_offers >= 3
     approved: preapproval_attached
     solvent: proof_of_funds_attached
     informed: disclosure_acknowledged
     acquainted: showing_completed
     climbing: escalation_clause
     stale: days_on_market >= 90
     discounted: price_cuts >= 2
     liquid: financing_type == cash
     brave: contingency_mix == waived all
     """,
     cues="lacks a lender letter => preapproval_attached=false; never toured the home => "
          "showing_completed=false; has no signed disclosure => disclosure_acknowledged=false",
     links="offer > buyer: names / named by; offer > property: targets / targeted by",
     actions="submit = send offer; counter = respond; book showing = reserve tour; withdraw = pull back",
     sources="showing log; buyer email; listing agent text; lender letter; disclosure portal; broker note",
     inert="""
     lockbox_colour | cat | black lockbox; grey lockbox
     yard_board_style | cat | post sign; frame sign
     car_model_driven | cat | sedan; hatchback
     open_house_cookie | cat | oatmeal; sugar
     brochure_paper | cat | glossy flyer; matte flyer
     """,
     affix="unfunded => proof_of_funds_attached; unacknowledged => disclosure_acknowledged"),

dict(slot="re-03", slug="mortgage-documents", sector="real_estate_admin",
     sub="mortgage application intake desk checking the document checklist",
     org="Silverbrook Community Credit Union Mortgage Center", desk="mortgage intake desk",
     setting="A credit union's mortgage center collects documents from loan applicants. The intake desk applies "
             "the document checklist, income and asset rules and decides when a file is ready for underwriting.",
     decider="loan interviewer",
     roles="loan processor; underwriter; loan officer; closing coordinator; member services clerk; "
           "quality control reviewer",
     docs="loan application; pay stubs; bank statements; tax returns; verification of employment; "
          "document checklist",
     scope=("loan program", "Fixed Rate; Adjustable Rate; First-Time Buyer; Refinance; Home Equity"),
     money="dollars",
     ents=[
        dict(key="file", singular="loan file", plural="loan files", id="KF", aka="mortgage file",
             attrs="""
             loan_amount | money | 20000.00..1500000.00 | aka=amount borrowed
             monthly_income | money | 1000.00..60000.00 | aka=verified monthly income
             debt_to_income | dec1 | 5.0..65.0 percent | aka=debt share of income
             months_of_reserves | dec1 | 0.0..36.0 months | aka=savings cushion
             documents_outstanding | int | 0..12 items | aka=documents still owed
             employment_type | cat | salaried; hourly; self-employed; retired; contract worker
             occupancy | cat | primary home; second home; rental property
             file_grade | ord | started; partial; complete; underwriter ready | aka=file status
             employment_verified | event | bad=0 | aka=employer confirmed the job | grp=verification
             large_deposit_explained | state | bad=0 | aka=large deposit has a written source
             gift_letter_on_file | state | bad=0 | aka=gift letter signed
             credit_report_pulled | event | bad=0 | aka=credit report ordered
             bankruptcy_last_four_years | event | bad=1 | aka=bankruptcy in the last four years
             applied_on | date
             rate_lock_ends_on | date
             file_tags | tag | co-borrower; gift funds; recent job change; foreign national; condo project
             """),
        dict(key="applicant", singular="applicant", plural="applicants", id="AN", names="person", role="person",
             attrs="""
             credit_score | int | 500..850 points | aka=credit score
             years_at_job | dec1 | 0.0..40.0 years | aka=time at current job
             """),
        dict(key="processor", singular="loan processor", plural="loan processors", id="KP", names="person",
             role="person",
             attrs="""
             files_in_pipeline | int | 0..80 items | aka=files on desk
             """),
     ],
     outcomes=["send to underwriting; ask for documents*; send to loan officer; suspend file*; "
               "close file as withdrawn*",
               "lock rate now; float rate; extend rate lock*"],
     levels=["started; partial; complete; underwriter ready", "low; medium; high"],
     words="""
     jumbo: loan_amount >= 750000
     modest: loan_amount < 60000
     stretched: debt_to_income >= 43
     comfortable: debt_to_income < 30
     padded: months_of_reserves >= 6
     thin: months_of_reserves < 1
     cluttered: documents_outstanding >= 4
     vouched: employment_verified
     accounted: large_deposit_explained
     endowed: gift_letter_on_file
     strong: credit_score >= 760
     fledgling: years_at_job < 1
     busy: files_in_pipeline >= 50
     ruined: bankruptcy_last_four_years
     autonomous: employment_type == self-employed
     """,
     cues="lacks a written source for the large deposit => large_deposit_explained=false; never had the job "
          "confirmed by the employer => employment_verified=false; has no gift letter => gift_letter_on_file=false",
     links="file > applicant: names / named by; file > processor: assigns / assigned by",
     actions="verify = confirm; condition = list needs; submit = send to underwriting; suspend = pause file",
     sources="loan application; employer phone call; bank statements; applicant email; credit report; "
             "processor note",
     inert="""
     folder_printer | cat | label printer A; label printer B
     branch_lobby_tv | cat | weather channel; rates screen
     member_pen | cat | blue pen; branded pen
     lobby_chair | cat | green chair; orange chair
     wall_art | cat | barn painting; lake painting
     """,
     affix="unverified => employment_verified; unexplained => large_deposit_explained"),

dict(slot="re-04", slug="buyer-counseling", sector="real_estate_admin",
     sub="first-time buyer counseling and down payment assistance eligibility",
     org="Harborlight Housing Counseling Agency", desk="buyer counseling office",
     setting="A housing counseling agency prepares first-time buyers and awards down payment assistance grants. "
             "The counseling office applies class, budget and grant eligibility rules to each household.",
     decider="personal financial advisor",
     roles="housing counselor; grant administrator; class instructor; lender partner; intake clerk; "
           "program manager",
     docs="intake budget; class certificate; grant application; credit summary; lender pre-approval; "
          "program guidelines",
     scope=("program", "City Grant; County Grant; Employer Assistance; Savings Match"),
     money="dollars",
     ents=[
        dict(key="household", singular="buyer household", plural="buyer households", id="HH",
             aka="client household",
             attrs="""
             household_income | money | 10000.00..250000.00 | aka=yearly income
             area_median_percent | int | 20..200 percent | aka=income as a share of the area median
             savings | money | 0.00..120000.00 | aka=money saved
             grant_sought | money | 1000.00..40000.00 | aka=grant asked for
             counseling_hours | dec1 | 0.0..20.0 hours | aka=hours of counseling
             household_size | int | 1..9 people | aka=people in the home
             target_area | cat | city core; inner suburb; outer suburb; rural county
             home_type_sought | cat | condo; townhouse; detached house; manufactured home | aka=kind of home wanted
             readiness_stage | ord | early; building; ready; under contract | aka=buyer stage
             class_certificate_earned | event | bad=0 | aka=finished the buyer class | grp=education
             owned_home_last_three_years | event | bad=1 | aka=owned a home recently
             budget_completed | state | bad=0 | aka=household budget done
             preapproval_received | event | bad=0 | aka=lender pre-approval received
             veteran_household | state | bad=0 | aka=veteran in the household
             intake_on | date
             contract_on | date
             household_tags | tag | single parent; teacher; health worker; accessible home; multigenerational
             """),
        dict(key="counselor", singular="housing counselor", plural="housing counselors", id="HC", names="person",
             role="person",
             attrs="""
             active_clients | int | 0..120 people | aka=caseload
             """),
        dict(key="lender", singular="partner lender", plural="partner lenders", id="PK",
             names="org: Bank, Credit Union, Mortgage, Savings",
             attrs="""
             grant_loans_closed | int | 0..300 items | aka=grant-backed loans closed
             """),
     ],
     outcomes=["award grant; award reduced grant; send to program manager; continue counseling*; "
               "refer to other program; close file*",
               "pay grant at closing; pay grant to escrow; hold grant*"],
     levels=["early; building; ready; under contract", "low; medium; high"],
     words="""
     needy: area_median_percent <= 50
     workaday: area_median_percent <= 80
     comfortable: area_median_percent >= 120
     thrifty: savings >= 20000
     ambitious: grant_sought >= 20000
     mentored: counseling_hours >= 8
     populous: household_size >= 5
     certified: class_certificate_earned
     organized: budget_completed
     preapproved: preapproval_received
     soldierly: veteran_household
     swamped: active_clients >= 90
     pastoral: target_area == rural county
     """,
     cues="never finished the buyer class => class_certificate_earned=false; lacks a lender pre-approval => "
          "preapproval_received=false; has no completed household budget => budget_completed=false",
     links="household > counselor: assigns / assigned by; household > lender: borrows from / lent to",
     actions="award = grant funds; counsel = advise; refer = pass on; certify = issue certificate",
     sources="intake budget; class roster; lender email; grant application; counselor note; credit summary",
     inert="""
     workshop_snack | cat | fruit tray; cookies
     classroom_projector | cat | ceiling projector; cart projector
     agency_logo_colour | cat | teal logo; orange logo
     handout_staple | cat | corner staple; side staple
     lobby_magazine | cat | home magazine; garden magazine
     """,
     affix="uncertified => class_certificate_earned; unbudgeted => budget_completed"),

dict(slot="re-05", slug="work-orders", sector="real_estate_admin",
     sub="commercial building work orders and tenant chargebacks",
     org="Merriton Office Park Management", desk="building operations desk",
     setting="An office park's management team handles tenant repair calls. The building operations desk sets "
             "each work order's priority, decides who pays under the lease and when a vendor is called.",
     decider="facilities manager",
     roles="building engineer; property manager; tenant coordinator; vendor dispatcher; accounts clerk; "
           "chief engineer",
     docs="work order; lease summary; vendor invoice; tenant chargeback notice; preventive maintenance log; "
          "inspection report",
     scope=("building", "Building A; Building B; Building C; Parking Structure"),
     money="dollars",
     ents=[
        dict(key="workorder", singular="work order", plural="work orders", id="WK", aka="repair ticket",
             attrs="""
             estimated_cost | money | 20.00..60000.00 | aka=repair estimate
             hours_open | int | 0..720 hours | aka=time open
             floor_number | int | 0..20 units | aka=floor
             repeat_calls_30_days | int | 0..6 entries | aka=repeat calls this month
             system | cat | heating and cooling; plumbing; electrical; elevator; roofing; doors and locks
             cause | cat | wear and tear; tenant damage; storm; vendor error; under investigation
             priority | ord | routine; urgent; emergency | aka=priority grade
             tenant_caused | state | bad=1 | aka=tenant caused the damage
             under_warranty | state | bad=0 | aka=equipment warranty in force
             life_safety_issue | state | bad=1 | aka=safety hazard present
             vendor_dispatched | event | bad=0 | aka=outside vendor sent
             after_hours_call | event | bad=1 | aka=reported outside business hours
             reported_on | date
             closed_on | date
             workorder_tags | tag | common area; tenant suite; recurring; inspection finding; capital item
             """),
        dict(key="tenant", singular="tenant", plural="tenants", id="TN",
             names="org: Analytics, Dental Group, Law Office, Design Studio",
             attrs="""
             leased_square_feet | int | 500..60000 square feet | aka=leased area
             lease_type | cat | gross lease; modified gross; triple net
             """),
        dict(key="engineer", singular="building engineer", plural="building engineers", id="BE", names="person",
             role="person",
             attrs="""
             open_orders | int | 0..40 items | aka=orders assigned
             """),
     ],
     outcomes=["fix in-house; send vendor; charge tenant*; claim warranty; send to property manager; "
               "defer to next budget*",
               "absorb cost; bill tenant*; split with tenant*; bill as common area cost"],
     levels=["routine; urgent; emergency", "low; medium; high"],
     words="""
     hefty: estimated_cost >= 5000
     minor: estimated_cost < 100
     neglected: hours_open >= 168
     chronic: repeat_calls_30_days >= 2
     upstairs: floor_number >= 10
     culpable: tenant_caused
     warranted: under_warranty
     hazardous: life_safety_issue
     contracted: vendor_dispatched
     sprawling: leased_square_feet >= 20000
     burdened: lease_type == triple net
     swamped: open_orders >= 25
     vertical: system == elevator
     nocturnal: after_hours_call
     weathered: cause == storm
     """,
     cues="has no warranty in force => under_warranty=false; never had an outside vendor sent => "
          "vendor_dispatched=false; lacks any safety hazard => life_safety_issue=false",
     links="workorder > tenant: concerns / concerned by; workorder > engineer: assigns / assigned by",
     actions="dispatch = send vendor; repair = fix; charge = bill back; inspect = check site",
     sources="work order system; tenant email; engineer note; vendor invoice; lease summary; inspection report",
     inert="""
     engineer_uniform | cat | navy uniform; khaki uniform
     lobby_fountain_mode | cat | still; flowing
     loading_dock_door | cat | dock 1; dock 2
     elevator_music_genre | cat | soft rock; classical
     mailroom_shelf | cat | top shelf; bottom shelf
     """,
     affix="unwarranted => under_warranty; undispatched => vendor_dispatched"),

dict(slot="re-06", slug="commission-disbursement", sector="real_estate_admin",
     sub="brokerage commission disbursement and listing compliance review",
     org="Cresthaven Real Estate Brokerage", desk="broker compliance desk",
     setting="After each closing, a brokerage splits the commission among the agents involved. The broker "
             "compliance desk checks the transaction file and applies the brokerage's split and file-completeness "
             "rules before paying agents.",
     decider="real estate broker",
     roles="compliance coordinator; managing broker; agent; office accountant; referral partner; "
           "transaction coordinator",
     docs="commission disbursement authorization; closing statement; transaction file checklist; referral "
          "agreement; listing agreement; agent split plan",
     scope=("brokerage office", "Central Office; Coastal Office; Hill Office; Online Team"),
     money="dollars",
     ents=[
        dict(key="disbursement", singular="commission disbursement", plural="commission disbursements", id="KD",
             aka="commission payout",
             attrs="""
             gross_commission | money | 1000.00..250000.00 | aka=total commission
             agent_split_percent | dec1 | 50.0..100.0 percent | aka=agent's share
             referral_fee_percent | dec1 | 0.0..35.0 percent | aka=referral share
             days_since_closing | int | 0..90 days | aka=time since closing
             outstanding_documents | int | 0..10 items | aka=file items outstanding
             side | cat | seller side; buyer side; both sides
             transaction_type | cat | resale home; new construction; land; lease; commercial
             agent_tier | ord | new agent; producing agent; top producer | aka=agent tier
             file_complete | state | bad=0 | aka=transaction file complete | grp=file
             funds_received | event | bad=0 | aka=commission funds arrived
             referral_agreement_signed | event | bad=0 | aka=referral agreement in file
             dual_agency_disclosed | state | bad=0 | aka=dual role disclosed in writing
             agent_owes_fees | state | bad=1 | aka=agent owes desk fees
             closed_on | date
             paid_on | date
             disbursement_tags | tag | team deal; referral out; referral in; cap reached; mentor split
             """),
        dict(key="agent", singular="agent", plural="agents", id="AG", names="person", role="person",
             attrs="""
             closings_this_year | int | 0..80 items | aka=closings this year
             cap_paid_so_far | money | 0.00..30000.00 | aka=company share paid this year
             """),
        dict(key="property", singular="property", plural="properties", id="PY",
             names=["Property 22 Willow Bend", "Property 140 Bay Street", "Property 7 Fern Hollow", "Property 63 Dock Road", "Property 310 Summit Way", "Property 18 Mill Pond", "Property 95 Garden Row", "Property 4 Lantern Court"],
             attrs="""
             sale_price | money | 50000.00..5000000.00 | aka=price paid
             """),
     ],
     outcomes=["pay agent now; pay after file complete*; send to managing broker; hold disbursement*; "
               "offset agent fees*",
               "pay by direct deposit; pay by cheque; pay referral partner first; freeze payout*"],
     levels=["new agent; producing agent; top producer", "low; medium; high"],
     words="""
     lucrative: gross_commission >= 50000
     modest: gross_commission < 3000
     generous: agent_split_percent >= 90
     allied: referral_fee_percent >= 25
     tardy: days_since_closing >= 30
     messy: outstanding_documents >= 3
     tidy: file_complete
     liquid: funds_received
     pledged: referral_agreement_signed
     transparent: dual_agency_disclosed
     indebted: agent_owes_fees
     prolific: closings_this_year >= 20
     saturated: cap_paid_so_far >= 20000
     rookie: agent_tier == new agent
     """,
     cues="lacks a complete transaction file => file_complete=false; has no commission funds yet => "
          "funds_received=false; never disclosed the dual role in writing => dual_agency_disclosed=false",
     links="disbursement > agent: pays / paid by; disbursement > property: cites / cited by",
     actions="disburse = pay out; audit = check file; offset = deduct fees; approve = sign off",
     sources="closing statement; transaction file checklist; agent email; accounting ledger; referral partner "
             "letter; title company wire",
     inert="""
     office_awning_colour | cat | blue sign; red sign
     meeting_cookie_jar | cat | full jar; half jar
     printer_tray_paper | cat | letter tray; legal tray
     name_badge_metal | cat | gold badge; silver badge
     lobby_couch | cat | leather couch; fabric couch
     """,
     affix="incomplete => file_complete; undisclosed => dual_agency_disclosed"),

dict(slot="re-07", slug="construction-draws", sector="real_estate_admin",
     sub="construction loan draw request review",
     org="Granitefield Bank Construction Lending", desk="construction draw desk",
     setting="A bank pays out construction loans in stages as building work is finished. The draw desk checks "
             "each draw against the inspector's report, lien waivers and the budget before releasing funds.",
     decider="loan officer",
     roles="draw administrator; site inspector; builder; title officer; construction lending manager; "
           "loan servicing clerk",
     docs="draw request form; inspection report; lien waiver; budget tracker; title update; change order",
     scope=("project type", "Custom Home; Townhome Row; Small Apartment; Retail Shell"),
     money="dollars",
     ents=[
        dict(key="draw", singular="draw request", plural="draw requests", id="DW", aka="construction draw",
             attrs="""
             draw_amount | money | 5000.00..2000000.00 | aka=amount asked for
             percent_complete | dec1 | 0.0..100.0 percent | aka=work finished per inspector
             percent_disbursed_after | dec1 | 0.0..100.0 percent | aka=share of the loan paid after this draw
             retainage_percent | dec1 | 0.0..15.0 percent | aka=holdback rate
             draw_number | int | 1..12 items | aka=draw sequence
             stage | cat | foundation; framing; roofing; mechanicals; drywall; finishes; final
             builder_grade | ord | new builder; approved builder; preferred builder | aka=builder standing
             inspection_passed | event | bad=0 | aka=site inspection passed | grp=inspection
             lien_waivers_received | event | bad=0 | aka=subcontractor waivers in hand
             title_update_clear | state | bad=0 | aka=title update shows zero new liens
             change_order_open | state | bad=1 | aka=unapproved change order open
             budget_line_exceeded | state | bad=1 | aka=a budget line is over
             submitted_on | date
             inspected_on | date
             draw_tags | tag | weather delay; material price rise; owner upgrade; final draw; reallocation
             """),
        dict(key="builder", singular="builder", plural="builders", id="BD",
             names="org: Homes, Construction, Builders, Development",
             attrs="""
             projects_with_bank | int | 0..40 items | aka=past projects with the bank
             trade_specialty | cat | residential; multifamily; commercial; mixed use | aka=builder focus
             """),
        dict(key="inspector", singular="site inspector", plural="site inspectors", id="SN", names="person",
             role="person",
             attrs="""
             inspections_this_week | int | 0..30 items | aka=visits this week
             """),
     ],
     outcomes=["release full draw; release reduced draw; hold for waivers*; order reinspection; "
               "send to lending manager; reject draw*",
               "pay builder; pay subcontractors directly; pay into escrow; hold in suspense*"],
     levels=["new builder; approved builder; preferred builder", "low; medium; high"],
     words="""
     hefty: draw_amount >= 250000
     modest: draw_amount < 20000
     advanced: percent_complete >= 75
     front-loaded: percent_disbursed_after >= 80
     cautious: retainage_percent >= 10
     mature: draw_number >= 8
     sound: inspection_passed
     discharged: lien_waivers_received
     pristine: title_update_clear
     fluid: change_order_open
     bloated: budget_line_exceeded
     experienced: projects_with_bank >= 5
     concluding: stage == final
     """,
     cues="never passed the site inspection => inspection_passed=false; lacks subcontractor lien waivers => "
          "lien_waivers_received=false; has no open change order => change_order_open=false",
     links="draw > builder: pays / paid by; draw > inspector: cites / cited by",
     actions="release = fund draw; reinspect = send inspector; reallocate = move budget; hold = pause funds",
     sources="draw request form; inspection report; builder email; title company update; budget tracker; "
             "subcontractor letter",
     inert="""
     hard_hat_colour | cat | white hat; yellow hat
     trailer_position | cat | trailer north; trailer south
     pickup_colour | cat | red truck; blue truck
     radio_channel_used | cat | channel 2; channel 6
     porta_toilet_vendor | cat | vendor P; vendor Q
     """,
     affix="uncleared => title_update_clear; uninspected => inspection_passed"),

dict(slot="re-08", slug="hoa-review", sector="real_estate_admin",
     sub="homeowners association architectural review and violation desk",
     org="Willowmere Commons Homeowners Association", desk="community management office",
     setting="A homeowners association approves exterior changes and enforces its rules. The community "
             "management office applies the covenants, design guidelines and fine schedule to each application "
             "and violation.",
     decider="community association manager",
     roles="architectural committee chair; board treasurer; compliance inspector; homeowner liaison; "
           "landscaping contractor; office administrator",
     docs="architectural application; design guidelines; violation notice; fine schedule; hearing notice; "
          "board minutes",
     scope=("neighbourhood section", "Willow Court; Heron Lake; Maple Ridge; Foxglove Row"),
     money="dollars",
     ents=[
        dict(key="application", singular="architectural application", plural="architectural applications",
             id="AA", aka="design application",
             attrs="""
             project_cost | money | 100.00..120000.00 | aka=cost of the change
             fence_height_ft | dec1 | 0.0..10.0 units | aka=fence height in feet
             setback_ft | dec1 | 0.0..40.0 units | aka=distance from the property line in feet
             days_since_submitted | int | 0..120 days | aka=time under review
             neighbors_objecting | int | 0..8 people | aka=neighbour objections
             project_kind | cat | fence; paint colour; deck; solar panels; shed; landscaping; addition
             visibility | ord | hidden; partly visible; street facing | aka=visibility from the street
             drawings_attached | state | bad=0 | aka=drawings included | grp=submission
             contractor_licensed | state | bad=0 | aka=contractor holds a license
             work_started_early | event | bad=1 | aka=work began before approval
             neighbor_signoff | event | bad=0 | aka=adjacent owner signed
             dues_current | state | bad=0 | aka=association dues paid up
             submitted_on | date
             decision_due_on | date
             application_tags | tag | corner lot; lakefront; historic facade; energy upgrade; resubmission
             """),
        dict(key="owner", singular="homeowner", plural="homeowners", id="HM", names="person", role="person",
             attrs="""
             violations_last_year | int | 0..10 items | aka=violations last year
             fines_owed | money | 0.00..5000.00 | aka=open fines
             membership_class | cat | resident owner; absentee owner; builder owner | aka=owner category
             """),
        dict(key="lot", singular="lot", plural="lots", id="KT",
             names=["Lot 14 Willow Court", "Lot 27 Heron Lake", "Lot 3 Maple Ridge", "Lot 41 Foxglove Row", "Lot 8 Willow Court", "Lot 19 Heron Lake", "Lot 32 Maple Ridge", "Lot 50 Foxglove Row"],
             attrs="""
             lot_size_sq_ft | int | 2000..40000 square feet | aka=lot area
             """),
     ],
     outcomes=["approve application; approve with conditions; send to architectural committee; return for plans*; "
               "reject application*; issue fine*",
               "first notice; second notice*; hearing*; fine and lien*; close violation"],
     levels=["hidden; partly visible; street facing", "low; medium; high"],
     words="""
     hefty: project_cost >= 20000
     tall: fence_height_ft >= 6
     tight: setback_ft < 5
     overdue: days_since_submitted >= 45
     opposed: neighbors_objecting >= 2
     illustrated: drawings_attached
     accredited: contractor_licensed
     premature: work_started_early
     endorsed: neighbor_signoff
     solvent: dues_current
     repeat: violations_last_year >= 2
     indebted: fines_owed >= 500
     conspicuous: visibility == street facing
     sunny: project_kind == solar panels
     """,
     cues="lacks attached drawings => drawings_attached=false; holds no contractor license => "
          "contractor_licensed=false; never got the adjacent owner's signature => neighbor_signoff=false",
     links="application > owner: names / named by; application > lot: concerns / concerned by",
     actions="approve = grant; inspect = visit site; fine = penalize; schedule hearing = set hearing",
     sources="architectural application; inspector photos; homeowner email; neighbour letter; board minutes; "
             "dues ledger",
     inert="""
     clubhouse_flower_bed | cat | tulips; marigolds
     mailbox_post_style | cat | cedar post; iron post
     pool_umbrella | cat | striped umbrella; plain umbrella
     newsletter_font | cat | serif newsletter; sans newsletter
     entrance_arch | cat | stone sign; wood sign
     """,
     affix="unlicensed => contractor_licensed; unendorsed => neighbor_signoff"),

dict(slot="re-09", slug="rental-applications", sector="real_estate_admin",
     sub="apartment leasing office screening rental applications and holding deposits",
     org="Bellhaven Apartments Leasing Office", desk="leasing office",
     setting="An apartment community's leasing office screens rental applications. It applies income, rental "
             "history and holding-deposit rules and decides whether each applicant is approved, conditioned or "
             "turned away.",
     decider="leasing receptionist",
     roles="leasing agent; community manager; screening analyst; maintenance supervisor; accounts clerk; "
           "regional manager",
     docs="rental application; screening report; holding deposit receipt; lease agreement; guarantor form; "
          "income documents",
     scope=("floor plan", "Studio; One Bedroom; Two Bedroom; Three Bedroom"),
     money="dollars",
     ents=[
        dict(key="application", singular="rental application", plural="rental applications", id="RA",
             aka="lease application",
             attrs="""
             monthly_rent | money | 600.00..6000.00 | aka=rent for the unit
             income_to_rent_ratio | dec1 | 0.5..8.0 points | aka=income over rent
             occupants | int | 1..8 people | aka=people moving in
             holding_deposit | money | 0.00..1000.00 | aka=deposit to hold the unit
             months_at_last_address | int | 0..240 months | aka=time at last address
             pet_type | cat | cat; dog; small caged animal; fish only; service animal
             lease_term | cat | six months; twelve months; fifteen months; month to month
             screening_result | ord | decline band; conditional band; approve band | aka=screening band
             landlord_reference_positive | event | bad=0 | aka=good reference from last landlord | grp=references
             eviction_history_found | event | bad=1 | aka=eviction found in screening
             guarantor_signed | event | bad=0 | aka=guarantor form signed
             renters_insurance_proof | state | bad=0 | aka=renters cover shown
             employed_currently | state | bad=0 | aka=currently working
             applied_on | date
             move_in_on | date
             application_tags | tag | student; relocating; corporate lease; housing voucher; transfer
             """),
        dict(key="applicant", singular="applicant", plural="applicants", id="AP", names="person", role="person",
             attrs="""
             credit_score | int | 300..850 points | aka=credit score
             """),
        dict(key="unit", singular="apartment unit", plural="apartment units", id="UN",
             names=["Unit 101", "Unit 214", "Unit 305", "Unit 412", "Unit 118", "Unit 226", "Unit 330", "Unit 408"],
             attrs="""
             days_vacant | int | 0..180 days | aka=days empty
             """),
     ],
     outcomes=["approve; approve with extra deposit*; approve with guarantor; send to community manager; "
               "turn away*; hold unit for documents",
               "refund holding deposit; apply deposit to rent; keep holding deposit*"],
     levels=["decline band; conditional band; approve band", "low; medium; high"],
     words="""
     pricey: monthly_rent >= 3000
     affordable: monthly_rent < 900
     comfortable: income_to_rent_ratio >= 3
     strained: income_to_rent_ratio < 2
     crowded: occupants >= 5
     settled: months_at_last_address >= 24
     recommended: landlord_reference_positive
     ousted: eviction_history_found
     backed: guarantor_signed
     insured: renters_insurance_proof
     earning: employed_currently
     strong: credit_score >= 720
     lingering: days_vacant >= 60
     canine: pet_type == dog
     """,
     cues="lacks a good reference from the last landlord => landlord_reference_positive=false; never showed "
          "renters cover => renters_insurance_proof=false; holds no current job => employed_currently=false",
     links="application > applicant: names / named by; application > unit: targets / targeted by",
     actions="screen = vet; approve = accept; hold unit = reserve; refund = repay deposit",
     sources="rental application; screening report; landlord phone call; employer letter; guarantor email; "
             "leasing agent note",
     inert="""
     model_flat_scent | cat | vanilla; linen
     pool_hours_board | cat | blue sign; white sign
     key_fob_colour | cat | green tag; red tag
     office_snack_bowl | cat | pretzels; candy
     lobby_rug_pattern | cat | diamonds; stripes
     """,
     affix="unemployed => employed_currently; uninsured => renters_insurance_proof"),

dict(slot="re-10", slug="self-storage", sector="real_estate_admin",
     sub="self-storage rentals, late fees and lien process",
     org="Stowfield Self Storage", desk="rental counter",
     setting="A self-storage facility rents units by the month. The rental counter applies move-in, late-fee, "
             "overlock and lien rules to each tenant account.",
     decider="rental clerk",
     roles="facility manager; assistant manager; district manager; auction coordinator; maintenance tech; "
           "call center agent",
     docs="rental agreement; late notice; overlock log; lien notice; auction listing; move-out form",
     scope=("facility", "Highway Site; Riverside Site; Airport Site; Downtown Site"),
     money="dollars",
     ents=[
        dict(key="account", singular="storage account", plural="storage accounts", id="ST", aka="tenant ledger",
             attrs="""
             monthly_rate | money | 25.00..600.00 | aka=monthly rent
             balance_due | money | 0.00..4000.00 | aka=amount owed
             days_late | int | 0..120 days | aka=days past due
             unit_size_sq_ft | int | 25..400 square feet | aka=unit area
             months_rented | int | 0..120 months | aka=tenure
             unit_type | cat | drive-up; climate controlled; locker; vehicle space; wine locker
             payment_method | cat | autopay card; cash; cheque; online
             delinquency_stage | ord | current; late; overlocked; pre-lien; lien | aka=collections stage
             overlock_applied | event | bad=1 | aka=office lock placed on the unit | grp=collections
             lien_notice_sent | event | bad=1 | aka=lien notice mailed | grp=collections
             contents_protection_active | state | bad=0 | aka=contents cover in force
             military_tenant | state | bad=0 | aka=active-duty tenant
             gate_code_active | state | bad=0 | aka=gate access works
             moved_in_on | date
             paid_through | date
             account_tags | tag | business tenant; vehicle stored; student; moving soon; promotional rate
             """),
        dict(key="tenant", singular="storage tenant", plural="storage tenants", id="TT", names="person",
             role="person",
             attrs="""
             accounts_held | int | 1..6 items | aka=units rented
             """),
        dict(key="unit", singular="storage unit", plural="storage units", id="SU",
             names=["Unit A12", "Unit B07", "Unit C33", "Unit D18", "Unit E05", "Unit F21", "Unit G09", "Unit H40"],
             attrs="""
             street_rate | money | 25.00..650.00 | aka=current advertised rate
             """),
     ],
     outcomes=["take payment; apply late fee*; place overlock*; send lien notice*; send to facility manager; "
               "waive fee once",
               "keep rate; raise rate*; offer discount"],
     levels=["current; late; overlocked; pre-lien; lien", "low; medium; high"],
     words="""
     pricey: monthly_rate >= 300
     thrifty: monthly_rate < 50
     indebted: balance_due >= 200
     tardy: days_late >= 10
     chronic: days_late >= 45
     spacious: unit_size_sq_ft >= 200
     loyal: months_rented >= 24
     sealed: overlock_applied
     warned: lien_notice_sent
     shielded: contents_protection_active
     enlisted: military_tenant
     multiple: accounts_held >= 2
     chilled: unit_type == climate controlled
     """,
     cues="has no contents cover in force => contents_protection_active=false; was never sent a lien notice => "
          "lien_notice_sent=false; lacks gate access => gate_code_active=false",
     links="account > tenant: belongs to / owned by; account > unit: rents / rented by",
     actions="collect = take payment; overlock = lock unit; auction = sell contents; rerate = change rate",
     sources="tenant ledger; gate access log; tenant phone call; lien notice log; call center note; "
             "auction listing",
     inert="""
     hand_truck_count | cat | two dollies; four dollies
     counter_bell | cat | brass bell; chrome bell
     hallway_light | cat | motion light; timer light
     box_display | cat | small box display; wardrobe box display
     driveway_paint | cat | yellow lines; white lines
     """,
     affix="unprotected => contents_protection_active; unlocked => overlock_applied"),
]
