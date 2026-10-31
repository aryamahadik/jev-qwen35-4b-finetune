"""packs-2 sector hr: human resources (Claude-written pack sources; invented employers and entities)."""

PACKS = [
dict(slot="hr-01", slug="leave-requests", sector="human_resources",
     sub="leave of absence desk applying eligibility and documentation rules",
     org="Corvane Distribution Company", desk="leave administration desk",
     setting="A distribution company grants leaves of absence for medical, family and personal reasons. The leave "
             "administration desk applies eligibility, notice, documentation and pay rules to each leave case.",
     decider="human resources assistant",
     roles="leave specialist; line manager; benefits clerk; payroll clerk; human resources business partner; "
           "occupational health nurse",
     docs="leave application; medical certification; eligibility notice; designation letter; return-to-work "
          "note; leave policy",
     scope=("site", "Central Warehouse; East Depot; Head Office; Returns Center"),
     money="dollars",
     ents=[
        dict(key="leave", singular="leave case", plural="leave cases", id="KV", aka="absence case",
             attrs="""
             months_employed | int | 0..360 months | aka=length of service
             hours_worked_last_year | int | 0..2600 hours | aka=hours worked in the last year
             weeks_requested | dec1 | 0.5..26.0 weeks | aka=weeks of leave sought
             weeks_used_this_year | dec1 | 0.0..26.0 weeks | aka=weeks already taken
             days_notice | int | 0..90 days | aka=notice given
             weekly_pay_continued | money | 0.00..3000.00 | aka=pay during leave
             leave_reason | cat | own health condition; new child; family care; military family; personal
             leave_pattern | cat | continuous; intermittent; reduced hours
             urgency | ord | foreseeable; short notice; emergency | aka=notice category
             certification_received | event | bad=0 | aka=medical form returned | grp=certification
             eligibility_notice_sent | event | bad=0 | aka=eligibility letter sent
             paid_time_off_applied | state | bad=0 | aka=paid time off used alongside
             key_employee | state | bad=1 | aka=named key employee
             return_date_confirmed | state | bad=0 | aka=return date agreed
             starts_on | date
             ends_on | date
             leave_tags | tag | adoption; surgery; elder care; deployment; bereavement; school event
             """),
        dict(key="employee", singular="employee", plural="employees", id="EM", names="person", role="person",
             attrs="""
             leave_cases_last_two_years | int | 0..6 items | aka=earlier leave cases
             job_family | cat | warehouse; driving; office; maintenance | aka=work group
             """),
        dict(key="manager", singular="line manager", plural="line managers", id="MG", names="person",
             role="person",
             attrs="""
             team_absences_now | int | 0..12 people | aka=team members out now
             """),
     ],
     outcomes=["approve protected leave; approve company leave; ask for certification*; send to business partner; "
               "reject leave*",
               "continuous leave; intermittent leave; reduced hours; postpone start*"],
     levels=["foreseeable; short notice; emergency", "low; medium; high"],
     words="""
     tenured: months_employed >= 12
     fledgling: months_employed < 3
     diligent: hours_worked_last_year >= 1250
     lengthy: weeks_requested >= 12
     exhausted: weeks_used_this_year >= 12
     sudden: days_notice < 2
     salaried: weekly_pay_continued > 0.5
     certified: certification_received
     notified: eligibility_notice_sent
     pivotal: key_employee
     settled: return_date_confirmed
     stretched: team_absences_now >= 4
     parental: leave_reason == new child
     """,
     cues="lacks the returned medical form => certification_received=false; was never sent an eligibility "
          "letter => eligibility_notice_sent=false; has no agreed return date => return_date_confirmed=false",
     links="leave > employee: covers / covered by; leave > manager: notifies / notified by",
     actions="approve = grant leave; designate = classify leave; extend = lengthen; recall = bring back",
     sources="leave application; medical provider fax; manager email; payroll report; employee phone call; "
             "time system",
     inert="""
     breakroom_microwave | cat | left microwave; right microwave
     safety_vest_size | cat | medium vest; large vest
     locker_bank | cat | bank A; bank B
     forklift_horn | cat | high horn; low horn
     corkboard_pin | cat | red pins; blue pins
     """,
     affix="uncertified => certification_received; unconfirmed => return_date_confirmed"),

dict(slot="hr-02", slug="training-compliance", sector="human_resources",
     sub="mandatory training compliance and certification renewals",
     org="Westlake Regional Transit Authority", desk="training compliance office",
     setting="A transit authority requires staff to complete safety and job certifications on a cycle. The "
             "training compliance office applies due dates, grace periods and work restrictions to each staff "
             "record.",
     decider="training and development manager",
     roles="training coordinator; safety officer; depot supervisor; course instructor; union steward; "
           "records clerk",
     docs="training matrix; certificate record; overdue report; restriction notice; course roster; "
          "grace period form",
     scope=("depot", "North Depot; South Depot; Rail Yard; Maintenance Base"),
     money="dollars",
     ents=[
        dict(key="training", singular="training file", plural="training files", id="TR",
             aka="certification file",
             attrs="""
             days_overdue | int | -90..180 days | aka=days past due | signed
             course_hours | dec1 | 0.5..40.0 hours | aka=course length
             attempts_used | int | 0..4 entries | aka=test attempts
             course_cost | money | 0.00..2500.00 | aka=course fee
             score_percent | dec1 | 0.0..100.0 percent | aka=last test score
             course_family | cat | safety; equipment operation; customer service; first aid; hazardous materials
             delivery | cat | classroom; online; on the job; simulator
             criticality | ord | advisory; required; safety critical | aka=course importance
             grace_extension_granted | event | bad=0 | aka=extra time approved | grp=grace
             practical_assessed | event | bad=0 | aka=hands-on check done
             supervisor_verified | event | bad=0 | aka=supervisor signed off
             on_restricted_duty | state | bad=1 | aka=work restriction in force
             seat_reserved | state | bad=0 | aka=place held in the next class
             completed_on | date
             due_on | date
             file_tags | tag | new hire; returning from leave; refresher; transfer; instructor led
             """),
        dict(key="employee", singular="staff member", plural="staff members", id="SM", names="person",
             role="person",
             attrs="""
             years_service | int | 0..40 years | aka=service length
             overdue_courses | int | 0..8 items | aka=other overdue courses
             """),
        dict(key="course", singular="course", plural="courses", id="CS",
             names=["Course Brake Systems Basics", "Course Passenger Care", "Course Track Safety", "Course Lift Operation", "Course First Response", "Course Fuel Handling", "Course Radio Protocol", "Course Night Driving"],
             attrs="""
             seats_per_session | int | 4..40 seats | aka=class size
             """),
     ],
     outcomes=["mark compliant; grant grace period; book retraining; restrict duties*; "
               "send to safety officer; suspend from role*",
               "classroom retake; online retake; practical retake; waive retake; remove from roster*"],
     levels=["advisory; required; safety critical", "low; medium; high"],
     words="""
     tardy: days_overdue > 0
     advanced: days_overdue < -30
     lengthy: course_hours >= 16
     struggling: attempts_used >= 2
     hefty: course_cost >= 1000
     proficient: score_percent >= 80
     extended: grace_extension_granted
     examined: practical_assessed
     endorsed: supervisor_verified
     sidelined: on_restricted_duty
     veteran: years_service >= 20
     lagging: overdue_courses >= 2
     vital: criticality == safety critical
     slotted: seat_reserved
     """,
     cues="lacks a supervisor sign-off => supervisor_verified=false; never had the hands-on check => "
          "practical_assessed=false; holds no place in the next class => seat_reserved=false",
     links="training > employee: concerns / concerned by; training > course: cites / cited by",
     actions="enrol = book seat; certify = mark complete; restrict = limit duties; extend = grant grace",
     sources="training matrix; course roster; supervisor email; overdue report; instructor note; "
             "depot notice board",
     inert="""
     classroom_whiteboard | cat | magnetic board; glass board
     depot_mascot | cat | owl; beaver
     instructor_lanyard | cat | orange lanyard; black lanyard
     coffee_machine | cat | pod machine; drip machine
     parking_bay | cat | bay 7; bay 9
     """,
     affix="unverified => supervisor_verified; unassessed => practical_assessed"),

dict(slot="hr-03", slug="contractor-extensions", sector="human_resources",
     sub="contingent workforce desk approving contractor extensions",
     org="Lumenridge Software Workforce Office", desk="contingent workforce desk",
     setting="A software company hires contractors through staffing agencies for fixed terms. The contingent "
             "workforce desk applies tenure limits, budget, rate and conversion rules to each extension.",
     decider="project management specialist",
     roles="workforce coordinator; hiring manager; procurement partner; staffing agency account manager; "
           "finance partner; legal reviewer",
     docs="extension form; statement of work; rate card; tenure report; budget forecast; conversion offer",
     scope=("department", "Engineering; Design; Customer Support; Data Team; Marketing"),
     money="dollars",
     ents=[
        dict(key="extension", singular="contract extension", plural="contract extensions", id="CE",
             aka="assignment extension",
             attrs="""
             months_on_assignment | int | 0..36 months | aka=tenure so far
             months_added | int | 1..12 months | aka=extension length
             hourly_bill_rate | money | 25.00..250.00 | aka=bill rate
             rate_increase_percent | dec1 | 0.0..30.0 percent | aka=rate rise sought
             budget_remaining | money | 0.00..900000.00 | aka=project budget left
             role_family | cat | software engineer; designer; support agent; data analyst; project coordinator
             engagement_type | cat | time and materials; fixed deliverable; staff augmentation
             performance_rating | ord | below target; on target; above target | aka=manager rating
             statement_of_work_signed | event | bad=0 | aka=work order signed | grp=paperwork
             conversion_offered | event | bad=0 | aka=permanent role offered
             budget_owner_approved | event | bad=0 | aka=budget holder approved
             badge_access_active | state | bad=0 | aka=building badge working
             tenure_cap_reached | state | bad=1 | aka=at the tenure limit
             started_on | date
             current_end_on | date
             extension_tags | tag | critical project; backfill; holiday cover; remote; offshore team
             """),
        dict(key="contractor", singular="contractor", plural="contractors", id="KN", names="person",
             role="person",
             attrs="""
             prior_assignments | int | 0..6 items | aka=earlier assignments here
             """),
        dict(key="agency", singular="staffing agency", plural="staffing agencies", id="SA",
             names="org: Staffing, Talent, Partners, Consulting",
             attrs="""
             markup_percent | dec1 | 10.0..80.0 percent | aka=agency markup
             """),
     ],
     outcomes=["approve extension; approve shorter extension; offer conversion; send to finance partner; "
               "end assignment*; pause extension*",
               "keep rate; raise rate; lower rate*"],
     levels=["below target; on target; above target", "low; medium; high"],
     words="""
     entrenched: months_on_assignment >= 18
     fledgling: months_on_assignment < 3
     lengthy: months_added >= 6
     premium: hourly_bill_rate >= 150
     greedy: rate_increase_percent >= 10
     tight: budget_remaining < 20000
     formalized: statement_of_work_signed
     courted: conversion_offered
     sanctioned: budget_owner_approved
     exhausted: tenure_cap_reached
     returning: prior_assignments >= 1
     pricey: markup_percent >= 50
     strong: performance_rating == above target
     resident: badge_access_active
     """,
     cues="lacks a signed work order => statement_of_work_signed=false; was never approved by the budget holder "
          "=> budget_owner_approved=false; has no working building badge => badge_access_active=false",
     links="extension > contractor: names / named by; extension > agency: contracts / contracted by",
     actions="extend = lengthen term; convert = hire permanently; offboard = end access; rerate = change rate",
     sources="extension form; hiring manager email; agency invoice; budget forecast; badge system; "
             "tenure report",
     inert="""
     laptop_sticker_theme | cat | space stickers; plant stickers
     standing_desk_height | cat | low desk; tall desk
     office_snack_shelf | cat | nuts; dried fruit
     monitor_brand | cat | brand M; brand N
     team_slack_emoji | cat | rocket emoji; taco emoji
     """,
     affix="unsigned => statement_of_work_signed; unapproved => budget_owner_approved"),

dict(slot="hr-04", slug="tuition-reimbursement", sector="human_resources",
     sub="tuition reimbursement program reviewing course claims",
     org="Pennbrook Health Partners Learning Office", desk="tuition assistance office",
     setting="A health system pays back part of employees' tuition for approved courses. The tuition assistance "
             "office applies the program's eligibility, grade, cap and repayment rules to each claim.",
     decider="training and development specialist",
     roles="program administrator; manager; benefits clerk; payroll clerk; education advisor; "
           "human resources director",
     docs="tuition claim; course approval form; grade report; receipt; repayment agreement; program policy",
     scope=("employee group", "Nursing Staff; Allied Health; Administration; Facilities Staff"),
     money="dollars",
     ents=[
        dict(key="claim", singular="tuition claim", plural="tuition claims", id="TQ", aka="reimbursement claim",
             attrs="""
             tuition_paid | money | 100.00..12000.00 | aka=tuition amount
             paid_this_year | money | 0.00..10000.00 | aka=already reimbursed this year
             credit_hours | int | 1..18 credits | aka=course credits
             days_since_course_end | int | 0..365 days | aka=time since the course ended
             months_employed | int | 0..400 months | aka=service length
             course_level | cat | certificate; associate; bachelor; master; doctoral
             job_relevance | cat | current role; career path; general skills
             grade_earned | ord | D; C; B; A | aka=final grade
             preapproval_granted | event | bad=0 | aka=course approved ahead | grp=approval
             receipt_attached | state | bad=0 | aka=receipt on file
             repayment_agreement_signed | event | bad=0 | aka=stay-or-repay agreement signed
             employer_grant_used | state | bad=0 | aka=outside grant also paid
             manager_endorsed | event | bad=0 | aka=manager supported it
             course_ended_on | date
             claimed_on | date
             claim_tags | tag | nursing degree; leadership course; online program; part-time study; licensure prep
             """),
        dict(key="employee", singular="employee", plural="employees", id="EE", names="person", role="person",
             attrs="""
             performance_band | ord | developing; solid; strong; outstanding | aka=last review band
             """),
        dict(key="school", singular="school", plural="schools", id="SH",
             names="org: College, University, Institute, Technical School",
             attrs="""
             accredited | state | bad=0 | aka=accredited school
             """),
     ],
     outcomes=["reimburse in full; reimburse partly; send to program administrator; return for grade report*; "
               "reject claim*",
               "pay with next paycheck; pay as one-time payment; apply to next term*"],
     levels=["D; C; B; A", "developing; solid; strong; outstanding"],
     words="""
     hefty: tuition_paid >= 5000
     thrifty: tuition_paid < 500
     capped: paid_this_year >= 5250
     heavy: credit_hours >= 12
     tardy: days_since_course_end >= 90
     tenured: months_employed >= 12
     sanctioned: preapproval_granted
     evidenced: receipt_attached
     committed: repayment_agreement_signed
     championed: manager_endorsed
     reputable: accredited
     excellent: grade_earned == A
     relevant: job_relevance == current role
     """,
     cues="lacks a receipt => receipt_attached=false; never got the course approved ahead => "
          "preapproval_granted=false; holds no stay-or-repay agreement => repayment_agreement_signed=false",
     links="claim > employee: pays / paid by; claim > school: cites / cited by",
     actions="reimburse = pay back; approve = clear claim; recover = claw back; review = check claim",
     sources="tuition claim; grade report; school receipt; manager email; payroll report; advisor note",
     inert="""
     graduation_gown_colour | cat | maroon gown; black gown
     campus_mascot | cat | falcon; lion
     textbook_cover | cat | red cover; blue cover
     study_lamp | cat | clip lamp; floor lamp
     backpack_colour | cat | grey pack; green pack
     """,
     affix="unapproved => preapproval_granted; unaccredited => accredited"),

dict(slot="hr-05", slug="life-events", sector="human_resources",
     sub="benefits enrolment desk for mid-year life event changes",
     org="Ostler and Vance Manufacturing Benefits Office", desk="benefits service desk",
     setting="Employees may change health and other benefit elections mid-year only after a qualifying life "
             "event. The benefits service desk applies event, timing and proof rules before changing an election.",
     decider="compensation and benefits manager",
     roles="benefits specialist; payroll clerk; carrier liaison; human resources generalist; employee; "
           "benefits analyst",
     docs="life event form; proof document; election confirmation; carrier enrolment file; payroll deduction "
          "notice; summary of benefits",
     scope=("benefit", "Medical; Dental; Vision; Life Insurance; Flexible Spending"),
     money="dollars",
     ents=[
        dict(key="event", singular="life event", plural="life events", id="KE", aka="qualifying event",
             attrs="""
             days_since_event | int | 0..120 days | aka=time since the event
             dependents_added | int | 0..5 people | aka=dependents added
             dependents_removed | int | 0..5 people | aka=dependents removed
             premium_change | money | -900.00..1500.00 | aka=change in monthly deduction | signed
             event_type | cat | marriage; birth; adoption; divorce; loss of other coverage; move out of area
             coverage_tier | ord | employee only; employee plus one; family | aka=coverage level
             proof_received | event | bad=0 | aka=proof document received | grp=proof
             election_consistent | state | bad=0 | aka=change fits the event
             carrier_file_sent | event | bad=0 | aka=enrolment sent to the carrier
             spouse_has_other_cover | state | bad=0 | aka=spouse covered elsewhere
             tobacco_attestation | state | bad=1 | aka=tobacco surcharge applies
             event_on | date
             reported_on | date
             event_tags | tag | twins; stepchild; court order; domestic partner; relocation
             """),
        dict(key="employee", singular="employee", plural="employees", id="EB", names="person", role="person",
             attrs="""
             salary_band | ord | band 1; band 2; band 3; band 4 | aka=pay band
             union_member | state | bad=0 | aka=covered by the union contract
             """),
        dict(key="carrier", singular="benefits carrier", plural="benefits carriers", id="BC",
             names="org: Health, Dental Plan, Vision Care, Life",
             attrs="""
             file_turnaround_days | int | 1..30 days | aka=carrier processing time
             carrier_region | cat | national; regional; local | aka=carrier reach
             """),
     ],
     outcomes=["approve change; approve partly; ask for proof*; send to benefits analyst; reject change*",
               "change from event date; change from next month; change at open enrolment*"],
     levels=["employee only; employee plus one; family", "band 1; band 2; band 3; band 4"],
     words="""
     prompt: days_since_event <= 30
     tardy: days_since_event > 60
     growing: dependents_added >= 1
     shrinking: dependents_removed >= 1
     steeper: premium_change >= 200
     thriftier: premium_change < 0
     proven: proof_received
     coherent: election_consistent
     relayed: carrier_file_sent
     unionized: union_member
     slow: file_turnaround_days >= 14
     familial: coverage_tier == family
     nuptial: event_type == marriage
     smoky: tobacco_attestation
     """,
     cues="lacks a proof document => proof_received=false; was never sent to the carrier => "
          "carrier_file_sent=false; has no change that fits the event => election_consistent=false",
     links="event > employee: concerns / concerned by; event > carrier: notifies / notified by",
     actions="enrol = add cover; drop coverage = remove cover; transmit = send file; verify = check proof",
     sources="life event form; benefits portal; carrier report; employee email; payroll deduction notice; "
             "proof document",
     inert="""
     wellness_fair_booth | cat | booth 3; booth 8
     brochure_artwork | cat | sunrise art; family art
     office_water_jug | cat | glass jug; plastic jug
     portal_banner | cat | green banner; blue banner
     pen_holder | cat | mesh holder; ceramic holder
     """,
     affix="unproven => proof_received; inconsistent => election_consistent"),

dict(slot="hr-06", slug="job-reclassification", sector="human_resources",
     sub="job reclassification and pay adjustment reviews",
     org="Marlow County Government Classification Unit", desk="classification and pay unit",
     setting="Managers ask the classification unit to review jobs whose duties have grown. The unit compares "
             "duties with the classification standards and pay ranges and decides whether a job is reclassified "
             "and how pay moves.",
     decider="compensation and job analysis specialist",
     roles="classification analyst; department head; budget officer; union representative; human resources "
           "director; payroll supervisor",
     docs="position description; desk audit report; classification standard; pay range table; budget impact "
          "form; decision letter",
     scope=("department", "Public Works; Library Services; Parks; Finance Office; Health Department"),
     money="dollars",
     ents=[
        dict(key="review", singular="classification review", plural="classification reviews", id="CR",
             aka="job review",
             attrs="""
             duties_changed_percent | dec1 | 0.0..100.0 percent | aka=share of duties that changed
             current_salary | money | 25000.00..180000.00 | aka=current pay
             proposed_increase_percent | dec1 | 0.0..25.0 percent | aka=pay rise proposed
             months_in_new_duties | int | 0..48 months | aka=time doing the new duties
             positions_affected | int | 1..30 people | aka=positions covered
             review_reason | cat | duties grown; reorganization; market gap; new license needed; supervisory duties
             proposed_grade_step | ord | same grade; one grade up; two grades up | aka=grade move
             desk_audit_done | event | bad=0 | aka=desk audit held | grp=audit
             department_head_endorsed | event | bad=0 | aka=department head supported it
             budget_funded | state | bad=0 | aka=money in the budget
             union_consulted | event | bad=0 | aka=union informed
             temporary_duties_only | state | bad=1 | aka=duties meant to be short-term
             submitted_on | date
             effective_on | date
             review_tags | tag | lead worker; certification; new program; vacancy; equity review
             """),
        dict(key="incumbent", singular="incumbent", plural="incumbents", id="CB", names="person", role="person",
             attrs="""
             years_in_position | int | 0..35 years | aka=time in the job
             bargaining_status | cat | represented; confidential; management | aka=union status
             """),
        dict(key="position", singular="position", plural="positions", id="PN",
             names=["Position Clerk Typist II", "Position Equipment Operator I", "Position Library Aide", "Position Accounts Technician", "Position Park Ranger I", "Position Program Assistant", "Position Inspector Trainee", "Position Office Coordinator"],
             attrs="""
             pay_range_max | money | 30000.00..200000.00 | aka=top of the range
             """),
     ],
     outcomes=["reclassify upward; keep classification*; grant temporary pay; send to human resources director; "
               "return for desk audit*",
               "raise to next step; raise to range minimum; hold pay*"],
     levels=["same grade; one grade up; two grades up", "low; medium; high"],
     words="""
     transformed: duties_changed_percent >= 50
     stable: duties_changed_percent < 10
     senior: current_salary >= 100000
     generous: proposed_increase_percent >= 10
     settled: months_in_new_duties >= 6
     sweeping: positions_affected >= 5
     examined: desk_audit_done
     championed: department_head_endorsed
     affordable: budget_funded
     briefed: union_consulted
     fleeting: temporary_duties_only
     veteran: years_in_position >= 15
     managerial: review_reason == supervisory duties
     """,
     cues="never had a desk audit => desk_audit_done=false; lacks department head support => "
          "department_head_endorsed=false; has no money in the budget => budget_funded=false",
     links="review > incumbent: names / named by; review > position: targets / targeted by",
     actions="classify = assign grade; audit = observe duties; adjust pay = change pay; inform union = tell union",
     sources="position description; desk audit report; department head memo; budget office email; "
             "union letter; payroll system",
     inert="""
     office_door_number | cat | door 210; door 315
     agenda_paper_colour | cat | white agenda; yellow agenda
     council_chamber_seat | cat | front seat; back seat
     building_wing | cat | east wing; west wing
     wall_portrait | cat | founder portrait; landscape
     """,
     affix="unaudited => desk_audit_done; unfunded => budget_funded"),

dict(slot="hr-07", slug="offer-approvals", sector="human_resources",
     sub="recruiting desk approving job requisitions and offers",
     org="Brindle Harbor Hospitality Group Talent Office", desk="talent acquisition desk",
     setting="A hospitality group opens job requisitions and makes offers to candidates. The talent acquisition "
             "desk applies headcount, pay range and pre-hire check rules before an offer is released.",
     decider="human resources specialist",
     roles="recruiter; hiring manager; compensation analyst; finance partner; onboarding coordinator; "
           "regional director",
     docs="job requisition; offer letter; pay range sheet; interview scorecard; reference check form; "
          "headcount plan",
     scope=("property", "Harbor Hotel; Lakeside Resort; City Suites; Airport Inn"),
     money="dollars",
     ents=[
        dict(key="offer", singular="job offer", plural="job offers", id="JF", aka="offer package",
             attrs="""
             base_salary | money | 22000.00..220000.00 | aka=offered pay
             range_position_percent | dec1 | 0.0..130.0 percent | aka=place in the pay range
             signing_bonus | money | 0.00..30000.00 | aka=sign-on bonus
             interviews_completed | int | 0..8 items | aka=interviews held
             days_req_open | int | 0..200 days | aka=time the job has been open
             job_level | cat | hourly staff; supervisor; manager; director
             employment_type | cat | full-time; part-time; seasonal
             scorecard_rating | ord | mixed; good; strong; exceptional | aka=interview rating
             headcount_approved | state | bad=0 | aka=position in the headcount budget | grp=headcount
             references_cleared | event | bad=0 | aka=references checked
             background_check_passed | event | bad=0 | aka=background check passed
             relocation_needed | state | bad=1 | aka=candidate must move
             counteroffer_present | state | bad=1 | aka=candidate holds a rival offer
             opened_on | date
             start_on | date
             offer_tags | tag | internal candidate; rehire; referral; visa transfer; campus hire
             """),
        dict(key="candidate", singular="candidate", plural="candidates", id="CD", names="person", role="person",
             attrs="""
             years_experience | int | 0..40 years | aka=experience
             """),
        dict(key="manager", singular="hiring manager", plural="hiring managers", id="HM", names="person",
             role="person",
             attrs="""
             open_reqs | int | 0..20 items | aka=jobs open on the team
             """),
     ],
     outcomes=["release offer; release after checks; send to compensation analyst; send to regional director; "
               "hold offer*; close requisition*",
               "standard package; add signing bonus; add relocation support; reduce package*"],
     levels=["mixed; good; strong; exceptional", "low; medium; high"],
     words="""
     lucrative: base_salary >= 120000
     modest: base_salary < 35000
     generous: range_position_percent > 100
     frugal: range_position_percent < 25
     sweetened: signing_bonus >= 5000
     thorough: interviews_completed >= 4
     stale: days_req_open >= 90
     sanctioned: headcount_approved
     vouched: references_cleared
     vetted: background_check_passed
     contested: counteroffer_present
     veteran: years_experience >= 10
     senior: job_level == director
     """,
     cues="holds no place in the headcount budget => headcount_approved=false; lacks checked references => "
          "references_cleared=false; never passed the background check => background_check_passed=false",
     links="offer > candidate: names / named by; offer > manager: credits / credited by",
     actions="extend offer = make offer; negotiate = adjust terms; rescind = withdraw offer; onboard = start hire",
     sources="job requisition; interview scorecard; candidate email; reference notes; background vendor report; "
             "finance approval",
     inert="""
     waiting_room_snack | cat | mints; water only
     lobby_music | cat | acoustic; lounge
     uniform_sample_colour | cat | navy sample; burgundy sample
     visitor_parking | cat | front lot; garage
     brochure_language | cat | english brochure; bilingual brochure
     """,
     affix="unbudgeted => headcount_approved; uncleared => background_check_passed"),

dict(slot="hr-08", slug="workplace-accommodations", sector="human_resources",
     sub="workplace accommodation case desk running the interactive process",
     org="Tessaly Financial Services Employee Relations", desk="accommodation case desk",
     setting="Employees ask for changes at work because of a health condition or religious practice. The "
             "accommodation desk runs the interactive process and applies the company's documentation, "
             "cost and effectiveness rules to each case.",
     decider="equal opportunity representative",
     roles="case manager; line manager; occupational health advisor; facilities coordinator; IT equipment clerk; "
           "employee relations lead",
     docs="accommodation form; medical information form; interactive meeting notes; cost estimate; "
          "decision letter; follow-up review",
     scope=("work setting", "Branch Office; Call Center; Operations Floor; Remote Work"),
     money="dollars",
     ents=[
        dict(key="case", singular="accommodation case", plural="accommodation cases", id="AC",
             aka="adjustment case",
             attrs="""
             estimated_cost | money | 0.00..25000.00 | aka=cost of the change
             days_open | int | 0..120 days | aka=time open
             meetings_held | int | 0..6 entries | aka=interactive meetings
             hours_change_per_week | dec1 | 0.0..20.0 hours | aka=change in weekly hours
             accommodation_type | cat | equipment; schedule change; remote work; leave time; job restructuring; religious observance
             duration_kind | cat | temporary; long-term; permanent
             complexity | ord | simple; moderate; complex | aka=case complexity
             medical_form_received | event | bad=0 | aka=health form returned | grp=documentation
             manager_consulted | event | bad=0 | aka=manager took part
             trial_period_set | state | bad=0 | aka=trial arrangement agreed
             essential_function_affected | state | bad=1 | aka=core duty affected
             alternative_offered | event | bad=0 | aka=another option offered
             opened_on | date
             review_on | date
             case_tags | tag | ergonomic; hearing; vision; pregnancy; prayer time; return from leave
             """),
        dict(key="employee", singular="employee", plural="employees", id="EP", names="person", role="person",
             attrs="""
             tenure_years | int | 0..40 years | aka=service length
             """),
        dict(key="manager", singular="line manager", plural="line managers", id="KM", names="person",
             role="person",
             attrs="""
             team_size | int | 2..80 people | aka=team size
             """),
     ],
     outcomes=["grant as asked; grant alternative; grant on trial; send to employee relations lead; "
               "ask for more information*; reject case*",
               "fund from department; fund from central budget; share cost*"],
     levels=["simple; moderate; complex", "low; medium; high"],
     words="""
     hefty: estimated_cost >= 5000
     thrifty: estimated_cost < 100
     lingering: days_open >= 45
     engaged: meetings_held >= 2
     substantial: hours_change_per_week >= 8
     documented: medical_form_received
     involved: manager_consulted
     provisional: trial_period_set
     fundamental: essential_function_affected
     flexible: alternative_offered
     veteran: tenure_years >= 10
     populous: team_size >= 30
     lasting: duration_kind == permanent
     devout: accommodation_type == religious observance
     """,
     cues="lacks a returned health form => medical_form_received=false; never had the manager take part => "
          "manager_consulted=false; has no trial arrangement agreed => trial_period_set=false",
     links="case > employee: concerns / concerned by; case > manager: notifies / notified by",
     actions="accommodate = put in place; meet = hold meeting; purchase = buy equipment; review = revisit",
     sources="accommodation form; meeting notes; occupational health letter; manager email; facilities ticket; "
             "employee message",
     inert="""
     lounge_art | cat | watercolour; photo print
     notebook_brand | cat | brand D; brand F
     tea_selection | cat | green leaf tea; chamomile
     floor_carpet_tile | cat | grey tile; blue tile
     window_view_side | cat | street side; courtyard side
     """,
     affix="undocumented => medical_form_received; unconsulted => manager_consulted"),

dict(slot="hr-09", slug="shift-swaps", sector="human_resources",
     sub="office supervisor approving shift swaps and overtime",
     org="Cardew Claims Processing Center", desk="shift supervision desk",
     setting="A claims processing center runs early, day and late shifts. The shift supervisor approves shift "
             "swaps and overtime under staffing minimums, rest rules and the overtime budget.",
     decider="office supervisor",
     roles="team lead; workforce planner; payroll clerk; operations manager; union steward; human resources partner",
     docs="swap form; shift roster; overtime log; staffing minimum sheet; rest period rule sheet; pay summary",
     scope=("shift", "Early Shift; Day Shift; Late Shift; Weekend Shift"),
     money="dollars",
     ents=[
        dict(key="swap", singular="shift change", plural="shift changes", id="SW", aka="swap or overtime case",
             attrs="""
             hours_rest_between | dec1 | 0.0..24.0 hours | aka=rest between shifts
             weekly_hours_after | dec1 | 10.0..70.0 hours | aka=week's hours after the change
             overtime_hours | dec1 | 0.0..20.0 hours | aka=overtime added
             overtime_cost | money | 0.00..2000.00 | aka=overtime pay
             staff_on_shift_after | int | 0..40 people | aka=staffing after the change
             change_kind | cat | swap; overtime; shift extension; split shift
             skill_match | ord | partial; full; exceeds | aka=skill fit of the partner
             partner_agreed | event | bad=0 | aka=other worker agreed | grp=agreement
             supervisor_notified_early | event | bad=0 | aka=told the supervisor two days ahead
             minimum_staffing_met | state | bad=0 | aka=minimum staffing still met
             overtime_budget_left | state | bad=0 | aka=overtime budget remains
             fatigue_flag | state | bad=1 | aka=fatigue rule triggered
             submitted_on | date
             shift_on | date
             swap_tags | tag | holiday; school run; training day; medical visit; peak week
             """),
        dict(key="worker", singular="claims processor", plural="claims processors", id="CP", names="person",
             role="person",
             attrs="""
             swaps_this_month | int | 0..10 items | aka=swaps this month
             team_name | cat | intake team; review team; payments team; correspondence team | aka=work team
             """),
        dict(key="partner", singular="swap partner", plural="swap partners", id="SP", names="person",
             role="person",
             attrs="""
             overtime_this_month | dec1 | 0.0..60.0 hours | aka=overtime already worked
             """),
     ],
     outcomes=["approve swap; approve overtime; approve with limit; send to operations manager; "
               "reject swap*; reject overtime*",
               "pay overtime; give time off in lieu; split pay and time*"],
     levels=["partial; full; exceeds", "low; medium; high"],
     words="""
     refreshed: hours_rest_between >= 11
     weary: hours_rest_between < 8
     heavy: weekly_hours_after >= 50
     surplus: overtime_hours >= 4
     hefty: overtime_cost >= 500
     thin: staff_on_shift_after <= 3
     willing: partner_agreed
     forewarned: supervisor_notified_early
     manned: minimum_staffing_met
     affordable: overtime_budget_left
     exhausted: fatigue_flag
     frequent: swaps_this_month >= 3
     overworked: overtime_this_month >= 30
     versatile: skill_match == exceeds
     """,
     cues="never had the other worker agree => partner_agreed=false; lacks overtime budget => "
          "overtime_budget_left=false; has no fatigue rule triggered => fatigue_flag=false",
     links="swap > worker: names / named by; swap > partner: pairs with / paired by",
     actions="approve = allow; roster = update shifts; pay = add overtime; cap overtime = limit extra hours",
     sources="swap form; shift roster; overtime log; worker message; workforce planner email; "
             "time clock report",
     inert="""
     headset_charging_bay | cat | bay one; bay two
     corner_fern | cat | monstera; pothos
     break_room_radio | cat | news radio; music radio
     cubicle_colour | cat | grey cubicle; blue cubicle
     coat_rack_side | cat | north wall; south wall
     """,
     affix="unstaffed => minimum_staffing_met; unfunded => overtime_budget_left"),

dict(slot="hr-10", slug="grievance-steps", sector="human_resources",
     sub="labor relations desk tracking grievances through contract steps",
     org="Saltmarsh Port Authority Labor Relations", desk="labor relations office",
     setting="A port authority's union contract sets steps and time limits for grievances. The labor relations "
             "office tracks each grievance, applies the contract's timelines and decides when a grievance moves "
             "up a step.",
     decider="labor relations specialist",
     roles="labor relations analyst; union steward; department manager; human resources director; legal counsel; "
           "arbitration clerk",
     docs="grievance form; step meeting notes; contract article; settlement agreement; arbitration demand; "
          "timeline tracker",
     scope=("bargaining unit", "Dock Workers; Maintenance Crafts; Clerical Unit; Security Officers"),
     money="dollars",
     ents=[
        dict(key="grievance", singular="grievance", plural="grievances", id="GV", aka="contract grievance",
             attrs="""
             days_since_incident | int | 0..180 days | aka=time since the incident
             days_to_respond | int | 0..30 days | aka=days left to answer
             step_reached | int | 1..4 units | aka=grievance step
             back_pay_claimed | money | 0.00..60000.00 | aka=back pay sought
             grievants | int | 1..60 people | aka=workers covered
             subject | cat | discipline; overtime allocation; seniority; pay; safety; work assignment
             remedy_sought | cat | rescind discipline; back pay; restore shift; policy change
             severity_level | ord | minor; moderate; serious | aka=issue seriousness
             filed_within_limit | state | bad=0 | aka=filed inside the time limit | grp=timeliness
             step_meeting_held | event | bad=0 | aka=step meeting took place
             written_answer_sent | event | bad=0 | aka=management answer sent
             past_practice_cited | state | bad=0 | aka=union cites past practice
             class_action | state | bad=1 | aka=covers a group of workers
             incident_on | date
             filed_on | date
             grievance_tags | tag | precedent; health and safety; night shift; probationary worker; outsourcing
             """),
        dict(key="steward", singular="union steward", plural="union stewards", id="UW", names="person",
             role="person",
             attrs="""
             open_grievances | int | 0..30 items | aka=cases carried
             """),
        dict(key="manager", singular="department manager", plural="department managers", id="DM", names="person",
             role="person",
             attrs="""
             grievances_this_year | int | 0..25 items | aka=grievances against the department this year
             """),
     ],
     outcomes=["settle at this step; move to next step; send to arbitration*; send to legal counsel; "
               "dismiss as late*; grant remedy",
               "full back pay*; partial back pay; restore shift only; written apology only"],
     levels=["minor; moderate; serious", "low; medium; high"],
     words="""
     stale: days_since_incident >= 60
     urgent: days_to_respond <= 3
     advanced: step_reached >= 3
     hefty: back_pay_claimed >= 10000
     collective: grievants >= 10
     punctual: filed_within_limit
     convened: step_meeting_held
     addressed: written_answer_sent
     customary: past_practice_cited
     busy: open_grievances >= 15
     contentious: grievances_this_year >= 8
     disciplinary: subject == discipline
     grave: severity_level == serious
     sweeping: class_action
     """,
     cues="was never filed inside the time limit => filed_within_limit=false; lacks a step meeting => "
          "step_meeting_held=false; has no management answer sent => written_answer_sent=false",
     links="grievance > steward: credits / credited by; grievance > manager: names / named by",
     actions="settle = resolve; advance = move up a step; arbitrate = send to arbitrator; answer = reply",
     sources="grievance form; step meeting notes; steward email; manager memo; timeline tracker; "
             "contract article",
     inert="""
     hall_coffee_strength | cat | strong coffee; weak coffee
     table_wood | cat | oak table; walnut table
     dock_crane_colour | cat | red crane; yellow crane
     parking_permit_colour | cat | green permit; white permit
     wall_calendar_theme | cat | ships; lighthouses
     """,
     affix="untimely => filed_within_limit; unanswered => written_answer_sent"),
]
