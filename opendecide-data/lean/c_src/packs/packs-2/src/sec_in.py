"""packs-2 sector in: insurance operations (Claude-written pack sources; invented insurers and entities)."""

PACKS = [
dict(slot="in-01", slug="form-filings", sector="insurance_ops",
     sub="regulatory filing desk tracking policy form and rate filings",
     org="Granite Shoals Mutual Insurance", desk="regulatory filings desk",
     setting="A regional insurer must file new policy forms and rate changes with state regulators before use. The "
             "filings desk tracks each filing and decides when a product may launch, wait or be withdrawn.",
     decider="regulatory affairs specialist",
     roles="filings analyst; product manager; actuary; compliance counsel; state liaison; launch coordinator",
     docs="filing memorandum; objection letter; response letter; approval notice; product launch checklist; "
          "rate exhibit",
     scope=("state", "State of Avon; State of Brill; State of Corran; State of Dalby; State of Elster"),
     money="dollars",
     ents=[
        dict(key="filing", singular="regulatory filing", plural="regulatory filings", id="RF", aka="form filing",
             attrs="""
             days_since_submission | int | 0..365 days | aka=time with the regulator
             objections_open | int | 0..8 items | aka=open objection points
             rate_change_percent | dec1 | -15.0..25.0 percent | aka=proposed rate change | signed
             filing_fee | money | 0.00..1500.00 | aka=state filing fee
             days_to_launch | int | 0..180 days | aka=time to planned launch
             filing_kind | cat | new form; form revision; rate change; rule change; withdrawal
             review_regime | cat | prior approval; file and use; use and file; informational
             complexity | ord | routine; moderate; extensive | aka=review complexity
             deemer_period_passed | state | bad=0 | aka=automatic approval period has run | grp=approval
             approval_letter_received | event | bad=0 | aka=regulator approved | grp=approval
             response_sent | event | bad=0 | aka=reply to objection sent
             actuarial_memo_attached | state | bad=0 | aka=actuarial support included
             public_hearing_called | event | bad=1 | aka=regulator called a hearing
             submitted_on | date
             launch_on | date
             filing_tags | tag | homeowners; auto; small business; umbrella; endorsement only
             """),
        dict(key="product", singular="insurance product", plural="insurance products", id="NP",
             names=["Product HomeGuard Plus", "Product AutoShield Basic", "Product ShopSafe", "Product RentRight", "Product BoatCover", "Product Umbrella Max", "Product FarmKeep", "Product CondoCare"],
             attrs="""
             projected_premium | money | 10000.00..20000000.00 | aka=expected yearly premium
             states_approved | int | 0..20 items | aka=states already approved
             """),
        dict(key="analyst", singular="filings analyst", plural="filings analysts", id="FA", names="person",
             role="person",
             attrs="""
             open_filings | int | 0..60 items | aka=filings on desk
             """),
     ],
     outcomes=["launch product; launch in approved states only; reply to objection; send to compliance counsel; "
               "postpone launch*; withdraw filing*",
               "use new rates; keep old rates*; phase in rates"],
     levels=["routine; moderate; extensive", "low; medium; high"],
     words="""
     stale: days_since_submission >= 120
     fresh: days_since_submission <= 10
     contested: objections_open >= 3
     steep: rate_change_percent >= 10
     cut: rate_change_percent < 0
     pricey: filing_fee >= 500
     imminent: days_to_launch <= 14
     presumed: deemer_period_passed
     sanctioned: approval_letter_received
     rebutted: response_sent
     substantiated: actuarial_memo_attached
     widespread: states_approved >= 10
     strict: review_regime == prior approval
     """,
     cues="lacks a regulator approval => approval_letter_received=false; never sent a reply to the objection => "
          "response_sent=false; has no actuarial support included => actuarial_memo_attached=false",
     links="filing > product: covers / covered by; filing > analyst: assigns / assigned by",
     actions="file = submit to regulator; respond = answer objection; withdraw = pull filing; launch = release",
     sources="state portal; objection letter; actuary email; product manager note; filings tracker; "
             "approval notice",
     inert="""
     binder_clip_size | cat | small clip; large clip
     portal_theme | cat | dark theme; light theme
     cubicle_number | cat | cubicle 14; cubicle 22
     lunch_spot | cat | deli; salad bar
     map_on_wall | cat | state map; world map
     """,
     affix="unanswered => response_sent; unapproved => approval_letter_received"),

dict(slot="in-02", slug="endorsements", sector="insurance_ops",
     sub="policy service desk processing mid-term endorsements",
     org="Brackenridge Insurance Services", desk="policy service desk",
     setting="Policyholders change their cover mid-term: new cars, new drivers, higher limits or new addresses. "
             "The policy service desk processes each endorsement under the underwriting and premium rules and "
             "decides when underwriting must approve.",
     decider="policy processing clerk",
     roles="service clerk; underwriting assistant; agent; premium accountant; quality reviewer; "
           "team supervisor",
     docs="endorsement form; policy declarations; premium change notice; driver report; underwriting referral; "
          "agent email",
     scope=("line of business", "Personal Auto; Homeowners; Renters; Small Business Owners"),
     money="dollars",
     ents=[
        dict(key="endorsement", singular="policy endorsement", plural="policy endorsements", id="PE",
             aka="mid-term change",
             attrs="""
             premium_change | money | -1200.00..4000.00 | aka=premium difference | signed
             days_backdated | int | 0..60 days | aka=days the change is dated back
             drivers_after_change | int | 1..6 people | aka=drivers on the policy
             limit_increase_percent | dec1 | 0.0..300.0 percent | aka=increase in limits
             change_kind | cat | add vehicle; add driver; raise limits; change address; add coverage; remove coverage
             submitted_by | cat | policyholder; agent; lender
             referral_level | ord | auto-approve; supervisor; underwriter | aka=approval route
             signed_form_received | event | bad=0 | aka=signed change form in hand | grp=paperwork
             driving_history_clean | state | bad=0 | aka=driving history has zero violations
             claim_open | state | bad=1 | aka=claim in progress
             lender_notified | event | bad=0 | aka=loss payee informed
             vehicle_inspected | event | bad=0 | aka=inspection photos received
             received_on | date
             effective_on | date
             endorsement_tags | tag | teen driver; classic car; home business; new purchase; move out of state
             """),
        dict(key="policy", singular="policy", plural="policies", id="PQ",
             names=["Policy AU-4471", "Policy HO-2290", "Policy RN-8813", "Policy BO-5502", "Policy AU-7720", "Policy HO-6631", "Policy RN-1954", "Policy BO-3386"],
             attrs="""
             annual_premium | money | 150.00..18000.00 | aka=yearly premium
             years_in_force | int | 0..40 years | aka=policy age
             """),
        dict(key="agent", singular="agent", plural="agents", id="AG", names="person", role="person",
             attrs="""
             endorsements_this_month | int | 0..80 items | aka=changes sent this month
             """),
     ],
     outcomes=["process endorsement; process and bill difference; refer to underwriting; return for signature*; "
               "reject endorsement*",
               "bill next instalment; bill now*; refund now"],
     levels=["auto-approve; supervisor; underwriter", "low; medium; high"],
     words="""
     hefty: premium_change >= 500
     rebate: premium_change < 0
     retroactive: days_backdated >= 15
     crowded: drivers_after_change >= 4
     steep: limit_increase_percent >= 100
     authorized: signed_form_received
     exemplary: driving_history_clean
     contested: claim_open
     apprised: lender_notified
     examined: vehicle_inspected
     loyal: years_in_force >= 10
     lavish: annual_premium >= 5000
     busy: endorsements_this_month >= 40
     routine: referral_level == auto-approve
     escalated: referral_level == underwriter
     """,
     cues="lacks a signed change form => signed_form_received=false; never sent inspection photos => "
          "vehicle_inspected=false; has no claim in progress => claim_open=false",
     links="endorsement > policy: amends / amended by; endorsement > agent: credits / credited by",
     actions="endorse = amend policy; rate = price change; refer = send up; issue = produce documents",
     sources="endorsement form; agent email; driver report; underwriting note; billing system; lender letter",
     inert="""
     envelope_logo | cat | logo green; logo navy
     office_kettle | cat | kettle one; kettle two
     queue_dashboard_colour | cat | dashboard teal; dashboard grey
     wall_print | cat | lighthouse print; meadow print
     ceiling_light | cat | panel light; bulb light
     """,
     affix="unsigned => signed_form_received; uninspected => vehicle_inspected"),

dict(slot="in-03", slug="property-referrals", sector="insurance_ops",
     sub="underwriting referrals for small commercial property risks",
     org="Tollgate Commercial Underwriters", desk="underwriting referral desk",
     setting="Agents submit small commercial buildings for property cover. The underwriting referral desk "
             "applies the insurer's construction, protection, occupancy and loss-history rules and decides whether "
             "to quote, decline or refer.",
     decider="insurance underwriter",
     roles="underwriting assistant; senior underwriter; loss control inspector; agent; reinsurance analyst; "
           "underwriting manager",
     docs="property submission; inspection report; loss run; statement of values; underwriting guide; quote letter",
     scope=("territory", "Coastal Zone; Inland Zone; Mountain Zone; Metro Zone"),
     money="dollars",
     ents=[
        dict(key="submission", singular="property submission", plural="property submissions", id="PS",
             aka="risk submission",
             attrs="""
             building_value | money | 100000.00..30000000.00 | aka=insured value
             building_age_years | int | 0..150 years | aka=age of the building
             losses_last_five_years | int | 0..8 claims | aka=claims in five years
             distance_to_hydrant_m | int | 10..2000 units | aka=hydrant distance in metres
             sprinkler_coverage | dec1 | 0.0..100.0 percent | aka=share of floor area sprinklered
             construction_class | cat | frame; joisted masonry; steel frame; fire resistive
             occupancy | cat | office; retail shop; restaurant; light manufacturing; warehouse; church
             protection_class | ord | class 1-3; class 4-6; class 7-8; class 9-10 | aka=fire protection grade
             roof_updated_recently | event | bad=0 | aka=roof replaced in the last ten years | grp=roof
             alarm_central_station | state | bad=0 | aka=monitored fire alarm
             vacant_space_share_high | state | bad=1 | aka=large part of the building empty
             inspection_completed | event | bad=0 | aka=loss control visit done
             cooking_operations | state | bad=1 | aka=commercial cooking on site
             received_on | date
             effective_on | date
             submission_tags | tag | historic building; multi-tenant; flood zone; wildfire area; new venture
             """),
        dict(key="insured", singular="applicant business", plural="applicant businesses", id="AB",
             names="org: Holdings, Properties, Partners, Trading",
             attrs="""
             years_in_business | int | 0..80 years | aka=business age
             """),
        dict(key="agent", singular="producing agent", plural="producing agents", id="PG", names="person",
             role="person",
             attrs="""
             agency_loss_ratio | dec1 | 10.0..120.0 percent | aka=agency loss ratio
             """),
     ],
     outcomes=["quote standard terms; quote with surcharge*; quote with conditions; refer to senior underwriter; "
               "turn away submission*",
               "standard deductible; higher deductible*; wind deductible*; lower deductible"],
     levels=["class 1-3; class 4-6; class 7-8; class 9-10", "low; moderate; high; severe"],
     words="""
     grand: building_value >= 5000000
     modest: building_value < 500000
     venerable: building_age_years >= 60
     modern: building_age_years <= 5
     jinxed: losses_last_five_years >= 3
     remote: distance_to_hydrant_m >= 300
     doused: sprinkler_coverage >= 80
     reroofed: roof_updated_recently
     guarded: alarm_central_station
     surveyed: inspection_completed
     established: years_in_business >= 15
     sloppy: agency_loss_ratio >= 70
     wooden: construction_class == frame
     hollow: vacant_space_share_high
     """,
     cues="lacks a monitored fire alarm => alarm_central_station=false; never had the loss control visit => "
          "inspection_completed=false; has no recent roof replacement => roof_updated_recently=false",
     links="submission > insured: names / named by; submission > agent: credits / credited by",
     actions="quote = price risk; refer = send up; inspect = order survey; bind = put on cover",
     sources="property submission; inspection report; loss run; agent email; mapping tool; "
             "senior underwriter note",
     inert="""
     folder_colour_code | cat | red folder; blue folder
     underwriter_desk_lamp | cat | arc lamp; desk lamp
     photo_format | cat | jpeg; png
     map_pin_colour | cat | red pin; yellow pin
     meeting_room_name | cat | Room Oak; Room Ash
     """,
     affix="unmonitored => alarm_central_station; uninspected => inspection_completed"),

dict(slot="in-04", slug="premium-audit", sector="insurance_ops",
     sub="workers compensation premium audit reconciling estimated and actual payroll",
     org="Keystone Fold Workers Comp Insurance", desk="premium audit desk",
     setting="At policy end, a workers compensation insurer audits each employer's actual payroll by job class. "
             "The premium audit desk applies classification and audit rules and sets the additional or returned "
             "premium.",
     decider="financial examiner",
     roles="premium auditor; audit reviewer; policyholder bookkeeper; agent; collections clerk; "
           "classification specialist",
     docs="audit worksheet; payroll records; classification guide; audit billing notice; dispute form; "
          "certificate of subcontractor cover",
     scope=("audit method", "Field Audit; Phone Audit; Mail Audit; Virtual Audit"),
     money="dollars",
     ents=[
        dict(key="audit", singular="premium audit", plural="premium audits", id="PA", aka="payroll audit",
             attrs="""
             estimated_payroll | money | 10000.00..20000000.00 | aka=payroll estimated at the start
             audited_payroll | money | 0.00..25000000.00 | aka=payroll found at audit
             premium_difference | money | -50000.00..150000.00 | aka=additional or returned premium | signed
             days_since_policy_end | int | 0..240 days | aka=time since the policy ended
             subcontractors_used | int | 0..40 items | aka=subcontractors hired
             main_class | cat | clerical; construction; restaurant; trucking; retail; healthcare
             bookkeeping_quality | ord | poor; fair; good; excellent | aka=quality of the books
             books_provided | event | bad=0 | aka=books handed over | grp=books
             sub_certificates_on_file | state | bad=0 | aka=subcontractor cover proven
             owner_excluded | state | bad=0 | aka=owner payroll left out by election
             audit_contested | event | bad=1 | aka=employer challenged a past audit
             estimate_updated_midterm | event | bad=0 | aka=payroll estimate revised during the term
             policy_ended_on | date
             audit_on | date
             audit_tags | tag | multi-state; seasonal staff; new class; overtime heavy; leased employees
             """),
        dict(key="employer", singular="employer", plural="employers", id="EP",
             names="org: Construction, Diner, Freight, Clinic",
             attrs="""
             employees | int | 1..900 employees | aka=staff count
             years_insured | int | 0..30 years | aka=years with the insurer
             payroll_system | cat | spreadsheet; payroll service; accounting software; paper ledger | aka=how payroll is kept
             """),
        dict(key="auditor", singular="premium auditor", plural="premium auditors", id="PD", names="person",
             role="person",
             attrs="""
             audits_this_month | int | 0..60 items | aka=audits done this month
             """),
     ],
     outcomes=["bill additional premium*; return premium; close with zero change; send to audit reviewer; "
               "estimate audit*; reopen audit",
               "bill in one payment*; bill in instalments; credit next policy"],
     levels=["poor; fair; good; excellent", "low; medium; high"],
     words="""
     hefty: estimated_payroll >= 5000000
     modest: estimated_payroll < 50000
     owing: premium_difference > 1000
     refunded: premium_difference < 0
     tardy: days_since_policy_end >= 120
     reliant: subcontractors_used >= 10
     forthcoming: books_provided
     vouched: sub_certificates_on_file
     spared: owner_excluded
     combative: audit_contested
     amended: estimate_updated_midterm
     populous: employees >= 200
     hazardous: main_class == construction
     """,
     cues="never handed over the books => books_provided=false; lacks proof of subcontractor cover => "
          "sub_certificates_on_file=false; has no midterm estimate revision => estimate_updated_midterm=false",
     links="audit > employer: concerns / concerned by; audit > auditor: assigns / assigned by",
     actions="audit = examine; reclassify = change class; bill = invoice; reopen = start again",
     sources="audit worksheet; employer payroll ledger; agent email; bookkeeper phone call; subcontractor "
             "certificate; billing system",
     inert="""
     auditor_car_colour | cat | white car; red car
     laptop_bag | cat | backpack; shoulder bag
     coffee_on_site | cat | provided; brought own
     field_notebook | cat | spiral notebook; bound notebook
     reception_sign | cat | glass sign; wooden sign
     """,
     affix="unproven => sub_certificates_on_file; uncooperative => books_provided"),

dict(slot="in-05", slug="auto-damage", sector="insurance_ops",
     sub="auto physical damage appraisal review: repair, total loss or supplement",
     org="Riverbend Auto Insurance Claims", desk="damage appraisal desk",
     setting="After a car accident claim, appraisers write a repair estimate or declare a total loss. The damage "
             "appraisal desk applies the total-loss threshold, supplement and repair-shop rules to each estimate.",
     decider="auto damage appraiser",
     roles="desk appraiser; field appraiser; claims adjuster; salvage coordinator; body shop manager; "
           "rental desk agent",
     docs="repair estimate; total loss valuation; supplement request; photo set; salvage bid; rental authorization",
     scope=("claim office", "North Office; South Office; Central Office; Mobile Team"),
     money="dollars",
     ents=[
        dict(key="estimate", singular="damage estimate", plural="damage estimates", id="DE", aka="repair estimate",
             attrs="""
             repair_cost | money | 200.00..60000.00 | aka=estimated repair cost
             vehicle_value | money | 1000.00..90000.00 | aka=actual cash value
             salvage_bid | money | 0.00..30000.00 | aka=best salvage offer
             supplements_so_far | int | 0..5 entries | aka=supplements added
             rental_days | int | 0..45 days | aka=rental days used
             damage_area | cat | front end; rear end; side; roof; undercarriage; flood
             shop_type | cat | network shop; independent shop; dealer shop
             damage_severity | ord | cosmetic; moderate; heavy; structural | aka=severity
             airbags_deployed | event | bad=1 | aka=airbags went off | grp=impact
             frame_damage_found | state | bad=1 | aka=frame bent
             photos_complete | state | bad=0 | aka=full photo set received
             prior_damage_noted | state | bad=1 | aka=old damage seen
             drivable | state | bad=0 | aka=car can be driven
             towed_from_scene | event | bad=1 | aka=vehicle was towed
             loss_on | date
             estimate_on | date
             estimate_tags | tag | hail; deer strike; parking lot; rollover; hit and run
             """),
        dict(key="vehicle", singular="vehicle", plural="vehicles", id="VH",
             names=["Vehicle Carro Sedan", "Vehicle Tundro Pickup", "Vehicle Velta Hatchback", "Vehicle Moro Van", "Vehicle Strada Coupe", "Vehicle Arvo Wagon", "Vehicle Kepa SUV", "Vehicle Zeno Compact"],
             attrs="""
             vehicle_age_years | int | 0..30 years | aka=model age
             odometer_km | int | 0..400000 kilometres | aka=distance driven
             """),
        dict(key="shop", singular="repair shop", plural="repair shops", id="RS",
             names="org: Collision, Auto Body, Motors, Paint and Body",
             attrs="""
             average_cycle_days | int | 2..40 days | aka=repair turnaround
             """),
        dict(key="claimant", singular="claimant", plural="claimants", id="CM", names="person", role="person",
             attrs="""
             prior_claims | int | 0..6 claims | aka=earlier claims
             """),
     ],
     outcomes=["approve repair; approve with supplement; declare total loss*; send to field appraiser; "
               "send to claims adjuster; hold for photos*",
               "repair at network shop; repair at chosen shop; pay cash settlement; sell to salvage*"],
     levels=["cosmetic; moderate; heavy; structural", "low; medium; high"],
     words="""
     hefty: repair_cost >= 15000
     minor: repair_cost < 1000
     luxurious: vehicle_value >= 40000
     humble: vehicle_value < 5000
     lucrative: salvage_bid >= 8000
     reworked: supplements_so_far >= 2
     prolonged: rental_days >= 14
     triggered: airbags_deployed
     warped: frame_damage_found
     documented: photos_complete
     mobile: drivable
     venerable: vehicle_age_years >= 12
     slow: average_cycle_days >= 20
     battered: damage_severity == structural
     """,
     cues="lacks a full photo set => photos_complete=false; has no bent frame => frame_damage_found=false; "
          "never had its airbags go off => airbags_deployed=false",
     links="estimate > vehicle: concerns / concerned by; estimate > shop: assigns / assigned by",
     actions="appraise = value; supplement = add repairs; total = write off; reinspect = check again",
     sources="repair estimate; photo set; shop email; salvage auction bid; adjuster note; rental system",
     inert="""
     paint_code_family | cat | blues; reds; greys
     wrecker_firm_colour | cat | yellow truck; white truck
     appraiser_clipboard | cat | metal clipboard; plastic clipboard
     lounge_tv_channel | cat | sports; news
     lot_space | cat | space 12; space 30
     """,
     affix="undrivable => drivable; undocumented => photos_complete"),

dict(slot="in-06", slug="agent-licensing", sector="insurance_ops",
     sub="agent licensing and carrier appointment compliance",
     org="Sablewood Life and Casualty", desk="producer licensing desk",
     setting="An insurer may pay commission only to agents who hold a current license and appointment in each "
             "state. The producer licensing desk checks licenses, continuing education and appointments before "
             "commissions are released.",
     decider="compliance officer",
     roles="licensing specialist; commissions analyst; agency manager; compliance counsel; onboarding clerk; "
           "state liaison",
     docs="license lookup; appointment record; continuing education transcript; commission statement; "
          "termination notice; background report",
     scope=("state", "State of Fenwick; State of Gorran; State of Harlow; State of Ivers"),
     money="dollars",
     ents=[
        dict(key="producer", singular="producer file", plural="producer files", id="PR", aka="agent file",
             attrs="""
             commission_held | money | 0.00..80000.00 | aka=commission on hold
             ce_hours_completed | int | 0..48 hours | aka=continuing education hours
             ce_hours_required | int | 12..24 hours | aka=education hours needed
             days_to_license_expiry | int | -60..730 days | aka=time to license end | signed
             states_appointed | int | 0..15 items | aka=states with appointment
             line_of_authority | cat | life; health; property; casualty; variable products
             agent_type | cat | captive agent; independent agent; agency employee; broker
             compliance_tier | ord | clear; watch; restricted | aka=compliance standing
             license_active | state | bad=0 | aka=license current | grp=license
             appointment_filed | event | bad=0 | aka=carrier appointment submitted
             background_cleared | event | bad=0 | aka=background check passed
             complaint_open | state | bad=1 | aka=consumer complaint open
             errors_omissions_cover | state | bad=0 | aka=professional liability cover in place
             licensed_on | date
             renewal_due_on | date
             producer_tags | tag | new hire; out-of-state license; agency owner; part-time; reactivated
             """),
        dict(key="agency", singular="agency", plural="agencies", id="AY",
             names="org: Insurance Agency, Financial Group, Brokers, Associates",
             attrs="""
             producers_in_agency | int | 1..120 people | aka=agents in the agency
             """),
        dict(key="specialist", singular="licensing specialist", plural="licensing specialists", id="KS",
             names="person", role="person",
             attrs="""
             open_cases | int | 0..90 items | aka=cases on desk
             """),
     ],
     outcomes=["release commission; release after appointment; hold commission*; send to compliance counsel; "
               "terminate appointment*",
               "renew license; file new appointment; suspend selling*"],
     levels=["clear; watch; restricted", "low; medium; high"],
     words="""
     sizable: commission_held >= 20000
     diligent: ce_hours_completed >= 24
     expiring: days_to_license_expiry <= 30
     lapsed: days_to_license_expiry < 0
     widespread: states_appointed >= 5
     accredited: license_active
     empowered: appointment_filed
     vetted: background_cleared
     complained: complaint_open
     shielded: errors_omissions_cover
     populous: producers_in_agency >= 50
     swamped: open_cases >= 60
     curbed: compliance_tier == restricted
     loyal: agent_type == captive agent
     """,
     cues="holds no current license => license_active=false; never filed the carrier appointment => "
          "appointment_filed=false; lacks professional liability cover => errors_omissions_cover=false",
     links="producer > agency: works for / staffed by; producer > specialist: assigns / assigned by",
     actions="appoint = file appointment; release = pay commission; terminate = end appointment; renew = extend",
     sources="state license lookup; appointment record; education provider transcript; agency email; "
             "commission statement; complaint log",
     inert="""
     badge_photo_backdrop | cat | blue backdrop; white backdrop
     office_cactus | cat | ficus; aloe
     printer_paper_brand | cat | brand H; brand J
     elevator_side | cat | left lift; right lift
     wall_clock_frame | cat | wood frame; metal frame
     """,
     affix="unlicensed => license_active; unappointed => appointment_filed"),

dict(slot="in-07", slug="scheduled-valuables", sector="insurance_ops",
     sub="scheduled personal property endorsements for jewelry, art and collectibles",
     org="Whitcombe Fine Property Insurance", desk="valuables underwriting desk",
     setting="Homeowners list valuable items such as rings, paintings and instruments on a scheduled property "
             "endorsement. The valuables desk checks appraisals, storage and limits and decides how each item is "
             "covered.",
     decider="personal property appraiser",
     roles="valuables underwriter; independent appraiser; agent; vault liaison; claims specialist; "
           "underwriting manager",
     docs="appraisal certificate; schedule of items; photo record; vault receipt; bill of sale; endorsement",
     scope=("item class", "Jewelry; Fine Art; Musical Instruments; Collectibles; Silverware"),
     money="dollars",
     ents=[
        dict(key="item", singular="scheduled item", plural="scheduled items", id="SC", aka="valuable item",
             attrs="""
             appraised_value | money | 500.00..2000000.00 | aka=appraisal amount
             appraisal_age_years | int | 0..20 years | aka=age of the appraisal
             value_increase_percent | dec1 | 0.0..200.0 percent | aka=increase since last appraisal
             items_on_schedule | int | 1..60 items | aka=items already covered
             storage | cat | home safe; bank vault; displayed at home; worn daily; on loan to museum
             item_material | cat | gold; platinum; canvas; wood; silver; mixed media
             appraiser_grade | ord | basic; certified; master | aka=appraiser standing
             appraisal_certified | state | bad=0 | aka=certified appraisal on file | grp=appraisal
             photos_on_file | state | bad=0 | aka=item photographed
             alarm_in_home | state | bad=0 | aka=monitored burglar alarm
             travels_with_owner | state | bad=1 | aka=taken on trips
             theft_claim_last_five_years | event | bad=1 | aka=theft claim in five years
             jeweller_inspection_done | event | bad=0 | aka=clasp and setting check done
             appraised_on | date
             added_on | date
             item_tags | tag | heirloom; recent purchase; one of a kind; set or pair; certificate of origin
             """),
        dict(key="owner", singular="policyholder", plural="policyholders", id="PH", names="person", role="person",
             attrs="""
             total_scheduled_value | money | 0.00..10000000.00 | aka=value already scheduled
             """),
        dict(key="appraiser", singular="appraiser", plural="appraisers", id="AP", names="person", role="person",
             attrs="""
             appraisals_reviewed | int | 0..500 items | aka=appraisals checked by the insurer
             """),
     ],
     outcomes=["schedule at appraised value; schedule with vault condition; ask for new appraisal*; "
               "send to underwriting manager; reject item*",
               "agreed value; replacement cost; market value*"],
     levels=["basic; certified; master", "low; medium; high"],
     words="""
     precious: appraised_value >= 100000
     modest: appraised_value < 2000
     outdated: appraisal_age_years >= 5
     appreciated: value_increase_percent >= 50
     extensive: items_on_schedule >= 20
     authenticated: appraisal_certified
     pictured: photos_on_file
     guarded: alarm_in_home
     roaming: travels_with_owner
     burgled: theft_claim_last_five_years
     wealthy: total_scheduled_value >= 1000000
     sequestered: storage == bank vault
     artistic: item_material == canvas
     """,
     cues="lacks a certified appraisal => appraisal_certified=false; has no monitored burglar alarm => "
          "alarm_in_home=false; was never photographed => photos_on_file=false",
     links="item > owner: belongs to / owned by; item > appraiser: cites / cited by",
     actions="schedule = list item; reappraise = value again; condition = add a rule; quote = price cover",
     sources="appraisal certificate; agent email; vault receipt; owner letter; photo record; underwriter note",
     inert="""
     velvet_tray_colour | cat | black velvet; red velvet
     loupe_brand | cat | loupe A; loupe B
     gallery_lighting | cat | warm light; cool light
     catalogue_font | cat | serif catalogue; sans catalogue
     office_rug | cat | persian rug; plain rug
     """,
     affix="uncertified => appraisal_certified; unphotographed => photos_on_file"),

dict(slot="in-08", slug="cancellations", sector="insurance_ops",
     sub="customer service desk for policy cancellations and reinstatements",
     org="Hawthorne Plains Insurance", desk="policyholder service center",
     setting="Policyholders call to cancel, or to reinstate a policy that lapsed for missed payment. The service "
             "center applies notice, refund and reinstatement rules to each case.",
     decider="customer service representative",
     roles="service representative; billing specialist; retention specialist; underwriting assistant; "
           "team lead; agent",
     docs="cancellation notice; reinstatement form; refund calculation; no-loss statement; billing history; "
          "call notes",
     scope=("policy type", "Auto; Home; Renters; Motorcycle; Boat"),
     money="dollars",
     ents=[
        dict(key="case", singular="service case", plural="service cases", id="SV", aka="cancellation case",
             attrs="""
             days_since_lapse | int | 0..90 days | aka=time since the policy lapsed
             amount_overdue | money | 0.00..3000.00 | aka=missed premium
             refund_due | money | 0.00..4000.00 | aka=unearned premium to return
             days_into_term | int | 0..365 days | aka=days of the term used
             case_kind | cat | customer cancellation; lapse reinstatement; lender cancellation; rewrite
             refund_basis | cat | pro rata; short rate; flat
             retention_offer_level | ord | basic; enhanced; premium | aka=retention offer
             loss_free_statement_signed | state | bad=0 | aka=signed statement of zero losses | grp=reinstate
             payment_received | event | bad=0 | aka=missed payment made
             lienholder_on_policy | state | bad=1 | aka=lender named on the policy
             cancellation_in_writing | event | bad=0 | aka=written cancellation received
             earlier_lapse_this_year | event | bad=1 | aka=lapsed before this year
             lapsed_on | date
             called_on | date
             case_tags | tag | moved away; sold vehicle; found cheaper; financial hardship; deceased policyholder
             """),
        dict(key="policyholder", singular="policyholder", plural="policyholders", id="PY", names="person",
             role="person",
             attrs="""
             years_with_insurer | int | 0..40 years | aka=customer tenure
             """),
        dict(key="rep", singular="service representative", plural="service representatives", id="SR",
             names="person", role="person",
             attrs="""
             calls_today | int | 0..90 items | aka=calls handled today
             """),
     ],
     outcomes=["reinstate seamlessly; reinstate with gap*; cancel and refund; cancel with forfeited premium*; "
               "send to underwriting; offer retention discount",
               "refund by cheque; refund to card; apply to other policy; hold refund*"],
     levels=["basic; enhanced; premium", "low; medium; high"],
     words="""
     fresh: days_since_lapse <= 5
     stale: days_since_lapse >= 30
     indebted: amount_overdue >= 200
     generous: refund_due >= 1000
     initial: days_into_term <= 30
     waning: days_into_term >= 300
     attested: loss_free_statement_signed
     remitted: payment_received
     financed: lienholder_on_policy
     explicit: cancellation_in_writing
     repeat: earlier_lapse_this_year
     loyal: years_with_insurer >= 10
     busy: calls_today >= 60
     lavish: retention_offer_level == premium
     """,
     cues="lacks a signed statement of zero losses => loss_free_statement_signed=false; never made the missed "
          "payment => payment_received=false; has no written cancellation => cancellation_in_writing=false",
     links="case > policyholder: concerns / concerned by; case > rep: assigns / assigned by",
     actions="reinstate = restore; cancel policy = end policy; refund = repay; retain = keep customer",
     sources="call notes; billing history; policyholder letter; lender notice; agent email; payment system",
     inert="""
     hold_music_track | cat | track one; track two
     headset_colour | cat | black headset; grey headset
     carpet_tile_pattern | cat | floor 2; floor 3
     desk_photo | cat | dog photo; beach photo
     break_room_mug | cat | striped mug; spotted mug
     """,
     affix="unpaid => payment_received; unsigned => loss_free_statement_signed"),

dict(slot="in-09", slug="coi-requests", sector="insurance_ops",
     sub="certificate of insurance desk issuing proof-of-cover certificates",
     org="Dunlevy Business Insurance Agency", desk="certificate desk",
     setting="Business clients need certificates of insurance to show landlords, general contractors and event "
             "venues. The certificate desk checks each certificate against the policy terms and the holder's "
             "contract wording before issuing it.",
     decider="general office clerk",
     roles="certificate clerk; account manager; commercial lines manager; client contact; carrier "
           "underwriter; quality reviewer",
     docs="certificate form; holder contract excerpt; policy declarations; additional insured endorsement; "
          "waiver endorsement; certificate log",
     scope=("client segment", "Contractors; Event Vendors; Landlords; Professional Services"),
     money="dollars",
     ents=[
        dict(key="certificate", singular="certificate", plural="certificates", id="CT",
             aka="proof of insurance",
             attrs="""
             limit_required | money | 100000.00..10000000.00 | aka=limit the holder asks for
             limit_on_policy | money | 100000.00..10000000.00 | aka=limit the policy has
             days_to_policy_expiry | int | 0..365 days | aka=time until the policy ends
             hours_needed_in | int | 1..120 hours | aka=time until needed
             holder_type | cat | landlord; general contractor; event venue; municipality; lender
             coverage_line | cat | general liability; auto liability; workers compensation; umbrella; professional liability
             wording_difficulty | ord | standard; special; manuscript | aka=contract wording type
             additional_insured_endorsed | state | bad=0 | aka=holder can be added as insured | grp=endorsements
             waiver_endorsed | state | bad=0 | aka=waiver of recovery endorsement present | grp=endorsements
             policy_paid_current | state | bad=0 | aka=premium paid up
             holder_contract_received | event | bad=0 | aka=holder's contract wording received
             manager_reviewed | event | bad=0 | aka=account manager checked it
             asked_on | date
             issued_on | date
             certificate_tags | tag | one-day event; ongoing project; renewal reissue; notice of cancellation; primary wording
             """),
        dict(key="client", singular="business client", plural="business clients", id="BC",
             names="org: Builders, Catering, Properties, Consulting",
             attrs="""
             certificates_this_year | int | 0..300 items | aka=certificates issued this year
             """),
        dict(key="holder", singular="certificate holder", plural="certificate holders", id="CH",
             names="org: Realty, General Contractors, Event Center, City Council",
             attrs="""
             strictness | ord | relaxed; standard; strict | aka=holder strictness
             """),
        dict(key="contact", singular="client contact", plural="client contacts", id="KC", names="person",
             role="person",
             attrs="""
             asks_this_month | int | 0..40 items | aka=certificates asked for this month
             """),
     ],
     outcomes=["issue certificate; issue with note; send to account manager; ask carrier for endorsement; "
               "return to client*; reject certificate*",
               "email certificate; post to portal; mail certificate; hold certificate*"],
     levels=["standard; special; manuscript", "relaxed; standard; strict"],
     words="""
     stringent: limit_required >= 5000000
     ample: limit_on_policy >= 2000000
     expiring: days_to_policy_expiry <= 30
     rushed: hours_needed_in <= 4
     embraced: additional_insured_endorsed
     relinquished: waiver_endorsed
     solvent: policy_paid_current
     documented: holder_contract_received
     vetted: manager_reviewed
     busy: certificates_this_year >= 100
     rigid: strictness == strict
     civic: holder_type == municipality
     bespoke: wording_difficulty == manuscript
     vehicular: coverage_line == auto liability
     """,
     cues="lacks the additional insured endorsement => additional_insured_endorsed=false; never sent the holder's "
          "contract wording => holder_contract_received=false; has no paid-up premium => policy_paid_current=false",
     links="certificate > client: names / named by; certificate > holder: lists / listed by",
     actions="issue = produce certificate; endorse = add holder; review = check wording; send = deliver",
     sources="certificate log; client email; holder contract excerpt; carrier underwriter email; policy system; "
             "account manager note",
     inert="""
     paper_weight_used | cat | light paper; heavy paper
     agency_lobby_fish_tank | cat | goldfish; guppies
     staple_position | cat | top left; top right
     office_parking_permit | cat | permit A; permit B
     window_plant | cat | basil; mint
     """,
     affix="unendorsed => additional_insured_endorsed; unreviewed => manager_reviewed"),

dict(slot="in-10", slug="quote-to-bind", sector="insurance_ops",
     sub="sales desk quoting and binding renters and small shop policies",
     org="Cobblestone Insurance Agency", desk="new business sales desk",
     setting="An insurance agency quotes renters and small shop policies and binds them on the spot when the "
             "carrier's binding rules allow. The sales desk decides whether each quote can bind, needs referral or "
             "must be declined.",
     decider="insurance sales agent",
     roles="sales associate; agency principal; carrier underwriter; customer service clerk; marketing assistant; "
           "premium finance clerk",
     docs="quote worksheet; application; binding authority guide; payment receipt; binder; prior insurance proof",
     scope=("product", "Renters Policy; Small Shop Package; Home Business Rider; Contents Policy"),
     money="dollars",
     ents=[
        dict(key="quote", singular="insurance quote", plural="insurance quotes", id="QT", aka="new business quote",
             attrs="""
             quoted_premium | money | 80.00..12000.00 | aka=yearly premium quoted
             contents_value | money | 2000.00..400000.00 | aka=value of belongings or stock
             claims_last_three_years | int | 0..6 claims | aka=recent claims
             days_since_prior_cover_ended | int | 0..365 days | aka=gap in cover
             deductible_choice | money | 250.00..10000.00 | aka=deductible chosen
             occupancy_type | cat | apartment; house share; storefront; home office; market stall
             payment_plan | cat | paid in full; monthly; quarterly
             binding_tier | ord | agent binds; carrier review; carrier only | aka=binding authority
             prior_insurance_proven | event | bad=0 | aka=proof of earlier cover received | grp=prior
             first_payment_taken | event | bad=0 | aka=down payment received
             application_signed | event | bad=0 | aka=application signed
             dog_on_premises | state | bad=1 | aka=dog lives at the address
             sprinklered_building | state | bad=0 | aka=building has sprinklers
             quoted_on | date
             start_on | date
             quote_tags | tag | student renter; roommates; new business; seasonal shop; bundled auto
             """),
        dict(key="applicant", singular="applicant", plural="applicants", id="AN", names="person", role="person",
             attrs="""
             credit_tier | ord | thin file; fair; good; excellent | aka=credit-based tier
             """),
        dict(key="carrier", singular="carrier", plural="carriers", id="CR",
             names="org: Mutual, Assurance, Casualty, Indemnity",
             attrs="""
             bind_limit | money | 50000.00..1000000.00 | aka=most the agent may bind
             """),
     ],
     outcomes=["bind now; bind after payment; refer to carrier; turn away applicant*; requote with higher deductible*",
               "pay in full; monthly instalments; premium finance*"],
     levels=["agent binds; carrier review; carrier only", "thin file; fair; good; excellent"],
     words="""
     pricey: quoted_premium >= 2000
     thrifty: quoted_premium < 150
     affluent: contents_value >= 100000
     jinxed: claims_last_three_years >= 2
     lapsed: days_since_prior_cover_ended >= 30
     frugal: deductible_choice >= 2500
     evidenced: prior_insurance_proven
     remitted: first_payment_taken
     attested: application_signed
     canine: dog_on_premises
     doused: sprinklered_building
     generous: bind_limit >= 500000
     commercial: occupancy_type == storefront
     """,
     cues="lacks proof of earlier cover => prior_insurance_proven=false; never signed the application => "
          "application_signed=false; has no down payment received => first_payment_taken=false",
     links="quote > applicant: names / named by; quote > carrier: places with / chosen for",
     actions="quote = price; bind = put on cover; refer = send to carrier; finance = arrange instalments",
     sources="quote worksheet; carrier portal; applicant email; payment receipt; prior insurer letter; "
             "agency principal note",
     inert="""
     agency_pen_colour | cat | green pen; purple pen
     welcome_candy | cat | mints; toffee
     lobby_radio_station | cat | oldies; country
     window_decal | cat | star decal; shield decal
     doormat_text | cat | hello mat; welcome mat
     """,
     affix="unsigned => application_signed; unproven => prior_insurance_proven"),
]
