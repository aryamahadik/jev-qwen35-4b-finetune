"""packs-2 sector hc: healthcare administration (Claude-written pack sources; invented organisations and entities)."""

PACKS = [
dict(slot="hc-01", slug="ride-vouchers", sector="healthcare_admin",
     sub="ride voucher desk that books trips to clinic visits",
     org="Tamberlin Community Health Network", desk="ride voucher desk",
     setting="A community health network pays for rides so that enrolled patients reach clinic visits. Workers at "
             "the voucher desk check each trip against the program's ride rules before a vendor is booked.",
     decider="community health worker",
     roles="voucher coordinator; clinic scheduler; dispatch lead; outreach supervisor; patient navigator; "
           "ride vendor liaison",
     docs="voucher request form; ride log; vendor invoice; appointment confirmation; outreach visit note; "
          "program bulletin",
     scope=("service zone", "North Basin; Mill District; Lakeshore; Old Quarry; Cedar Flats"),
     money="dollars",
     ents=[
        dict(key="trip", singular="voucher request", plural="voucher requests", id="VR", aka="ride request",
             attrs="""
             trip_miles | dec1 | 0.5..42.0 miles | aka=trip distance
             fare_quote | money | 4.00..180.00 | aka=quoted fare
             days_until_visit | int | 0..30 days | aka=lead time
             riders_in_party | int | 1..4 people | aka=party size
             visit_type | cat | primary care; dialysis; prenatal; behavioral health; physical therapy; pharmacy pickup
             mobility_need | ord | walks unaided; cane or walker; wheelchair; stretcher | aka=mobility level
             appointment_confirmed | state | bad=0 | aka=visit confirmation on file | grp=visit_check
             address_verified | event | bad=0 | aka=pickup address checked
             escort_approved | event | bad=0 | aka=escort cleared
             late_cancellation_logged | event | bad=1 | aka=prior late cancellation | grp=history
             trip_received_on | date
             visit_date | date
             trip_tags | tag | first ride; repeat rider; out of zone; holiday; after hours; group trip
             """),
        dict(key="patient", singular="patient", plural="patients", id="PT", names="person", role="person",
             attrs="""
             rides_used_this_month | int | 0..12 trips | aka=monthly ride count
             household_size | int | 1..8 people
             enrollment_tier | ord | basic; extended; full support | aka=program tier
             program_enrolled | state | bad=0 | aka=active ride-program enrollment
             """),
        dict(key="vendor", singular="ride vendor", plural="ride vendors", id="RV", names="org: Cab Co., Transit, Shuttles, Rides",
             attrs="""
             vendor_rating | dec1 | 1.0..5.0 points | aka=vendor score
             on_time_rate | dec1 | 60.0..99.9 percent | aka=punctuality rate
             vendor_contract_active | state | bad=0 | aka=contract in force
             """),
     ],
     outcomes=["issue one-way voucher; issue round-trip voucher; offer bus pass; send to supervisor review; "
               "return to clinic for details*; reject voucher*",
               "book standard car; book accessible van; book stretcher transport; place on standby list*"],
     levels=["routine; priority; urgent", "low; medium; high; very high"],
     words="""
     outlying: trip_miles > 25
     nearby: trip_miles < 3
     pricey: fare_quote >= 60
     thrifty: fare_quote < 12
     rushed: days_until_visit <= 1
     leisurely: days_until_visit >= 14
     crowded: riders_in_party >= 3
     frequent: rides_used_this_month >= 8
     assured: appointment_confirmed
     pinpointed: address_verified
     wheeled: mobility_need in {wheelchair, stretcher}
     dependable: on_time_rate >= 95
     populous: household_size >= 6
     renal: visit_type == dialysis
     flaky: late_cancellation_logged
     """,
     cues="lacks a visit confirmation => appointment_confirmed=false; was never checked at the listed address => "
          "address_verified=false; holds no active ride-program enrollment => program_enrolled=false",
     links="trip > patient: names / named by; trip > vendor: books / booked by",
     actions="issue = grant; reroute = redirect; reimburse = pay back; verify = confirm",
     sources="dispatch log; clinic calendar; patient phone call; vendor portal; outreach visit note; "
             "front-desk sign-in sheet",
     inert="""
     clipboard_colour | cat | red; white; black
     van_paint | cat | white; silver; dark blue
     radio_station_in_van | cat | news; jazz; talk
     favourite_season | cat | spring; summer; autumn; winter
     bench_by_the_door | cat | bench A; bench B; bench C
     """,
     affix="unconfirmed => appointment_confirmed; unverified => address_verified"),

dict(slot="hc-02", slug="study-stipends", sector="healthcare_admin",
     sub="participant stipend and travel reimbursement desk at a research clinic",
     org="Orrinvale Clinical Research Unit", desk="participant payments desk",
     setting="A hospital research unit pays study participants a stipend per completed visit and reimburses travel. "
             "Coordinators check each payment line against the study's payment schedule before it is released.",
     decider="clinical research coordinator",
     roles="payments clerk; study nurse; site budget analyst; principal investigator; visit coordinator; "
           "finance approver",
     docs="visit completion log; stipend payment sheet; travel receipt; participant ledger; study payment schedule; "
          "monitor visit letter",
     scope=("study site", "Main Campus; East Annex; Harbour Clinic; Westfield Suite"),
     money="dollars",
     ents=[
        dict(key="payline", singular="payment line", plural="payment lines", id="PY", aka="stipend line",
             attrs="""
             stipend_amount | money | 25.00..400.00 | aka=visit stipend
             travel_claimed | money | 0.00..220.00 | aka=travel claim
             visit_number | int | 1..14 visits | aka=visit sequence number
             days_since_visit | int | 0..120 days | aka=age of the line
             visit_window_days | int | 1..14 days | aka=allowed visit window
             visit_kind | cat | screening; baseline; dosing; follow-up; extension; closeout
             payment_method | cat | prepaid card; bank transfer; cheque
             visit_completed | event | bad=0 | aka=visit done | grp=visit
             receipt_attached | state | bad=0 | aka=receipt on file
             overnight_stay | event | bad=0 | aka=stayed overnight
             line_paid_before | event | bad=1 | aka=duplicate payment found
             visit_on | date
             line_created_on | date
             line_tags | tag | parking; mileage; meal; hotel; companion; train
             """),
        dict(key="participant", singular="participant", plural="participants", id="SP", names="person", role="person",
             attrs="""
             year_to_date_paid | money | 0.00..3600.00 | aka=paid this year
             consent_version | ord | v1; v2; v3; v4 | aka=consent form version
             tax_form_on_file | state | bad=0 | aka=tax form received
             withdrawn_from_study | event | bad=1 | aka=left the study | grp=status
             """),
        dict(key="study", singular="study", plural="studies", id="ST", names=["Study Kestrel", "Study Amberline", "Study Tidewater", "Study Quillon", "Study Marrowby", "Study Fennick", "Study Rowanmere", "Study Galloway"],
             attrs="""
             per_visit_cap | money | 50.00..450.00 | aka=stipend cap
             enrolled_count | int | 4..240 people | aka=enrolment
             """),
     ],
     outcomes=["release payment; release stipend only; hold for receipt; route to principal investigator; "
               "void payment line*",
               "pay by card; pay by transfer; pay by cheque; suspend payments*"],
     levels=["minor; moderate; major; critical", "first; second; third; final"],
     words="""
     generous: stipend_amount >= 250
     modest: stipend_amount < 60
     extravagant: travel_claimed > 150
     stale: days_since_visit > 90
     fresh: days_since_visit <= 7
     tight: visit_window_days <= 2
     advanced: visit_number >= 10
     initial: visit_number <= 2
     documented: receipt_attached
     lodged: overnight_stay
     current: consent_version == v4
     closing: visit_kind == closeout
     prosperous: year_to_date_paid >= 2500
     doubled: line_paid_before
     """,
     cues="lacks a travel receipt => receipt_attached=false; never completed the visit => visit_completed=false; "
          "has no tax form on file => tax_form_on_file=false",
     links="payline > participant: pays / paid by; payline > study: cites / cited by",
     actions="release = disburse; reverse = undo; reconcile = balance; approve = sign off",
     sources="visit completion log; study nurse email; card vendor statement; finance system; monitor report; "
             "participant phone call",
     inert="""
     snack_offered | cat | crackers; fruit; granola; juice
     waiting_room_chair | cat | blue chair; grey chair; red chair
     binder_spine_colour | cat | alpha; beta; gamma
     courier_van_colour | cat | white; green; orange
     lobby_plant | cat | fern; palm; ficus
     """,
     affix="incomplete => visit_completed; undocumented => receipt_attached"),

dict(slot="hc-03", slug="clinic-scheduling", sector="healthcare_admin",
     sub="specialty clinic scheduling desk with late-cancellation and no-show rules",
     org="Pellbrook Specialty Clinics", desk="scheduling desk",
     setting="A group of specialty clinics books, moves and closes appointments. The scheduling desk applies the "
             "clinic's booking, late-cancellation and missed-visit rules to each appointment.",
     decider="medical secretary",
     roles="front-desk lead; clinic manager; scheduling clerk; nurse triage line; billing liaison; "
           "patient advocate",
     docs="appointment book; booking confirmation; late-cancellation notice; clinic policy sheet; reminder log; "
          "provider template",
     scope=("clinic", "Cardiology Wing; Dermatology Suite; Orthopedic Center; Sleep Lab; Allergy Clinic"),
     money="dollars",
     ents=[
        dict(key="appointment", singular="appointment", plural="appointments", id="AP", aka="visit slot",
             attrs="""
             notice_hours | int | 0..336 hours | aka=hours of notice given
             slot_minutes | int | 10..90 minutes | aka=slot length
             reschedules_so_far | int | 0..6 entries | aka=times moved
             late_fee | money | 0.00..150.00 | aka=cancellation charge
             visit_category | cat | new patient; follow-up; procedure; telehealth; test review
             booking_channel | cat | phone; portal; walk-in; referral desk
             reminder_sent | event | bad=0 | aka=reminder delivered
             arrived_on_time | event | bad=0 | aka=checked in on time | grp=attendance
             interpreter_booked | state | bad=0 | aka=interpreter arranged
             prepayment_received | state | bad=0 | aka=deposit paid
             booked_on | date
             appointment_on | date
             slot_tags | tag | first of day; last of day; double slot; overbook; holiday week
             """),
        dict(key="patient", singular="patient", plural="patients", id="PN", names="person", role="person",
             attrs="""
             missed_visits_last_year | int | 0..9 visits | aka=missed visit count
             account_balance | money | 0.00..2400.00 | aka=open balance
             portal_active | state | bad=0 | aka=portal account in use
             """),
        dict(key="provider", singular="provider", plural="providers", id="PV", names="person", role="person",
             attrs="""
             open_slots_this_week | int | 0..40 seats | aka=free slots
             provider_grade | ord | resident; attending; senior attending | aka=provider seniority
             """),
     ],
     outcomes=["keep booking; move to next open slot; charge late fee*; send reminder; flag for clinic manager; "
               "close booking*",
               "waive fee; apply half fee; apply full fee*"],
     levels=["green; amber; red", "low; medium; high"],
     words="""
     abrupt: notice_hours < 24
     generous: notice_hours >= 72
     brief: slot_minutes <= 15
     lengthy: slot_minutes >= 60
     fickle: reschedules_so_far >= 3
     secured: prepayment_received
     nudged: reminder_sent
     prompt: arrived_on_time
     chronic: missed_visits_last_year >= 3
     indebted: account_balance > 500
     remote: visit_category == telehealth
     busy: open_slots_this_week <= 2
     eminent: provider_grade == senior attending
     penalized: late_fee >= 50
     multilingual: interpreter_booked
     virtual: booking_channel == portal
     """,
     cues="failed to arrive on time => arrived_on_time=false; lacks a deposit => prepayment_received=false; "
          "was never sent a reminder => reminder_sent=false",
     links="appointment > patient: books / booked by; appointment > provider: lists / listed by",
     actions="book = reserve; reschedule = move; check in = register arrival; waive = forgive",
     sources="appointment book; reminder log; front-desk note; patient portal message; phone message; "
             "provider template",
     inert="""
     magazine_rack_theme | cat | travel; gardening; cooking; sports
     reception_music | cat | piano; strings; quiet
     umbrella_stand | cat | full; half full; empty
     clock_style | cat | round; square; digital
     window_blinds | cat | open; half; closed
     """,
     affix="unpaid => prepayment_received; unannounced => reminder_sent"),

dict(slot="hc-04", slug="class-enrolment", sector="healthcare_admin",
     sub="enrolment desk for a hospital's diabetes self-care class series",
     org="Wrenfield General Hospital Education Office", desk="class enrolment desk",
     setting="A hospital education office runs a series of self-care classes for adults managing diabetes. The "
             "enrolment desk places each referral into a class cohort under the program's seat and readiness rules.",
     decider="health education specialist",
     roles="class registrar; program dietitian; nurse educator; outreach clerk; cohort facilitator; "
           "program director",
     docs="class referral; cohort roster; readiness checklist; attendance sheet; program handbook; waitlist report",
     scope=("venue", "Hospital Auditorium; Library Room; Northside Clinic; Online Studio"),
     money="dollars",
     ents=[
        dict(key="referral", singular="class referral", plural="class referrals", id="CR", aka="enrolment referral",
             attrs="""
             a1c_value | dec1 | 5.0..14.0 percent | aka=latest A1C
             days_in_queue | int | 0..120 days | aka=queue days
             sessions_attended_before | int | 0..8 sessions | aka=earlier sessions attended
             class_fee | money | 0.00..240.00 | aka=series fee
             preferred_language | cat | English; Spanish; Vietnamese; Somali; Tagalog
             session_format | cat | in person; online; hybrid
             readiness_stage | ord | considering; preparing; acting; maintaining | aka=readiness level
             physician_signed | event | bad=0 | aka=referral signed by a physician
             meter_supplied | state | bad=0 | aka=glucose meter in hand
             fee_assistance_granted | event | bad=0 | aka=fee help approved
             caregiver_attending | state | bad=0 | aka=family member joining
             referred_on | date
             cohort_start | date
             referral_tags | tag | newly diagnosed; insulin user; pregnancy; senior; shift worker; returning
             """),
        dict(key="learner", singular="learner", plural="learners", id="KN", names="person", role="person",
             attrs="""
             age_years | int | 18..90 years | aka=age
             travel_minutes | int | 5..120 minutes | aka=travel time
             contact_verified | event | bad=0 | aka=phone number checked
             """),
        dict(key="cohort", singular="cohort", plural="cohorts", id="CH", names=["Cohort Larch", "Cohort Maple", "Cohort Birch", "Cohort Rowan", "Cohort Aspen", "Cohort Hazel", "Cohort Alder", "Cohort Linden"],
             attrs="""
             seats_left | int | 0..20 seats | aka=open seats
             cohort_size_cap | int | 8..24 seats | aka=seat cap
             """),
     ],
     outcomes=["enrol in next cohort; enrol in online cohort; add to waitlist*; send to nurse educator; "
               "return to referrer*",
               "charge full fee*; charge reduced fee; waive fee"],
     levels=["considering; preparing; acting; maintaining", "beginner; intermediate; advanced"],
     words="""
     elevated: a1c_value >= 9.0
     controlled: a1c_value < 7.0
     patient: days_in_queue >= 60
     seasoned: sessions_attended_before >= 2
     complimentary: class_fee < 1
     endorsed: physician_signed
     equipped: meter_supplied
     accompanied: caregiver_attending
     elderly: age_years >= 75
     distant: travel_minutes >= 60
     packed: seats_left <= 1
     virtual: session_format == online
     ready: readiness_stage >= acting
     subsidized: fee_assistance_granted
     bilingual: preferred_language in {Spanish, Vietnamese, Somali, Tagalog}
     """,
     cues="lacks a physician signature => physician_signed=false; has no glucose meter => meter_supplied=false; "
          "was never reached at the listed number => contact_verified=false",
     links="referral > learner: enrols / enrolled by; referral > cohort: targets / targeted by",
     actions="enrol = register; waitlist = queue; transfer = move over; remind = nudge",
     sources="referral fax; cohort roster; nurse educator note; phone call log; patient portal; registrar email",
     inert="""
     handout_paper_colour | cat | cream; white; light blue
     whiteboard_pen | cat | black; blue; red
     room_temperature_setting | cat | cool; mild; warm
     facilitator_mug | cat | striped; plain; dotted
     snack_table_side | cat | left side; right side
     """,
     affix="unsigned => physician_signed; unsupported => caregiver_attending"),

dict(slot="hc-05", slug="preregistration", sector="healthcare_admin",
     sub="pre-registration and coverage check interviews before planned hospital visits",
     org="Castlemont Regional Hospital", desk="pre-registration desk",
     setting="Before a planned hospital visit, interviewers call the patient to collect demographic and coverage "
             "details. The pre-registration desk then sets the visit's account status under the hospital's intake "
             "rules.",
     decider="intake interviewer",
     roles="patient access lead; coverage specialist; financial counselor; unit clerk; admitting supervisor; "
           "registration auditor",
     docs="pre-registration worksheet; coverage response; deposit estimate; consent packet; call log; "
          "account summary",
     scope=("service line", "Surgery; Imaging; Maternity; Infusion; Rehabilitation"),
     money="dollars",
     ents=[
        dict(key="account", singular="visit account", plural="visit accounts", id="VA", aka="registration account",
             attrs="""
             estimated_charges | money | 200.00..48000.00 | aka=estimate of charges
             patient_share_estimate | money | 0.00..9000.00 | aka=out-of-pocket estimate
             days_before_visit | int | 0..45 days | aka=days until the visit
             call_attempts | int | 0..6 entries | aka=call attempts made
             coverage_type | cat | employer plan; marketplace plan; public program; self-pay; workers compensation
             visit_class | cat | outpatient; observation; inpatient; day surgery
             coverage_confirmed | event | bad=0 | aka=coverage response received | grp=coverage
             deposit_collected | event | bad=0 | aka=deposit taken
             consent_packet_signed | state | bad=0 | aka=consent packet complete
             identity_document_seen | event | bad=0 | aka=ID checked
             second_coverage_present | state | bad=0 | aka=second policy on file
             interview_on | date
             visit_on | date
             account_tags | tag | language line; guardian; new patient; transfer; international
             """),
        dict(key="patient", singular="patient", plural="patients", id="PR", names="person", role="person",
             attrs="""
             prior_balance | money | 0.00..6000.00 | aka=earlier balance
             visits_last_year | int | 0..20 visits
             contact_preference | cat | phone; text; email; mail
             """),
        dict(key="payer", singular="payer", plural="payers", id="PA", names="org: Health Plan, Mutual, Benefit Trust, Care Plan",
             attrs="""
             payer_tier | ord | out of network; tier 2; tier 1 | aka=network tier
             response_hours | int | 1..96 hours | aka=reply time
             """),
     ],
     outcomes=["mark ready; mark ready with deposit; send to financial counselor; hold visit for coverage*; "
               "reschedule visit*",
               "collect full deposit*; collect partial deposit; collect at visit"],
     levels=["low; moderate; high; very high", "bronze; silver; gold"],
     words="""
     hefty: estimated_charges >= 15000
     minor: estimated_charges < 1000
     burdensome: patient_share_estimate >= 2500
     imminent: days_before_visit <= 2
     leisurely: days_before_visit >= 21
     persistent: call_attempts >= 4
     insured: coverage_confirmed
     secured: deposit_collected
     identified: identity_document_seen
     agreed: consent_packet_signed
     owing: prior_balance > 100
     frequent: visits_last_year >= 6
     favored: payer_tier == tier 1
     slow: response_hours >= 48
     private: coverage_type == self-pay
     admitted: visit_class == inpatient
     """,
     cues="lacks a coverage response => coverage_confirmed=false; failed to show an ID document => "
          "identity_document_seen=false; has no deposit on the account => deposit_collected=false",
     links="account > patient: registers / registered by; account > payer: bills / billed by",
     actions="verify = check coverage; estimate = price; counsel = advise; release = clear",
     sources="call log; payer web response; unit clerk note; patient voicemail; financial counselor email; "
             "worksheet",
     inert="""
     headset_model | cat | model A; model B; model C
     booth_number | cat | booth 1; booth 2; booth 3
     hold_music | cat | piano; guitar; harp
     wall_calendar_picture | cat | lighthouse; meadow; harbour
     chair_wheel_squeak | cat | loud; faint; silent
     """,
     affix="unsigned => consent_packet_signed; unconfirmed => coverage_confirmed"),

dict(slot="hc-06", slug="imaging-authorization", sector="healthcare_admin",
     sub="prior authorization desk for outpatient imaging orders",
     org="Velmora Outpatient Imaging Partners", desk="authorization desk",
     setting="An outpatient imaging network checks each scan order against payer coverage rules before the scan is "
             "booked. The authorization desk decides whether an order can proceed, needs records or goes to review.",
     decider="health services manager",
     roles="intake coordinator; utilization reviewer; scheduling lead; ordering clinician; payer liaison; "
           "medical director",
     docs="order requisition; payer coverage bulletin; authorization log; determination letter; peer-to-peer note; "
          "clinical summary",
     scope=("site", "Northgate; Riverside; Elm Park; Harbor View"),
     money="dollars",
     ents=[
        dict(key="order", singular="imaging order", plural="imaging orders", id="RQ", aka="scan order",
             attrs="""
             estimated_cost | money | 150.00..4800.00 | aka=quoted cost
             therapy_weeks | int | 0..16 weeks | aka=weeks of conservative care
             days_since_order | int | 0..60 days | aka=order age
             prior_scans_12_months | int | 0..5 items | aka=scans in the last year
             modality | cat | MRI; CT; ultrasound; PET; nuclear scan | aka=scan type
             body_region | cat | head; spine; chest; abdomen; joint; pelvis
             clinical_notes_attached | state | bad=0 | aka=chart notes on file | grp=records
             urgent_flag_set | event | bad=0 | aka=marked urgent
             peer_review_held | event | bad=0 | aka=peer-to-peer done | pre=peer_review_offered | grp=review
             peer_review_offered | event | bad=0 | aka=peer-to-peer offered | grp=review
             contrast_needed | state | bad=0 | aka=uses contrast
             ordered_on | date
             scan_window_end | date
             order_tags | tag | repeat; post-surgical; sports; oncology follow-up; pediatric; second opinion
             """),
        dict(key="clinician", singular="ordering clinician", plural="ordering clinicians", id="CK", names="person",
             role="person",
             attrs="""
             approval_rate | dec1 | 40.0..99.0 percent | aka=past approval rate
             gold_card_status | state | bad=0 | aka=exempt from review
             """),
        dict(key="payer", singular="payer", plural="payers", id="PB", names="org: Health Plan, Assurance, Care Network",
             attrs="""
             review_turnaround_days | int | 1..15 days | aka=decision time
             plan_category | ord | basic; standard; premium | aka=plan level
             """),
     ],
     outcomes=["authorize; pend for records*; refer to medical director; offer peer-to-peer; "
               "return to ordering clinic*",
               "book scan now; book after approval; cancel order*"],
     levels=["routine; expedited; urgent; emergent", "low; medium; high"],
     words="""
     stale: days_since_order > 30
     hefty: estimated_cost >= 2000
     thrifty: estimated_cost < 400
     tried: therapy_weeks >= 6
     recurrent: prior_scans_12_months >= 2
     substantiated: clinical_notes_attached
     pressing: urgent_flag_set
     debated: peer_review_held
     trusted: gold_card_status
     reliable: approval_rate >= 90
     slow: review_turnaround_days >= 10
     deluxe: plan_category == premium
     spinal: body_region == spine
     magnetic: modality == MRI
     enhanced: contrast_needed
     challenged: peer_review_offered
     """,
     cues="lacks chart notes => clinical_notes_attached=false; was never offered a peer-to-peer call => "
          "peer_review_offered=false; holds no exemption from review => gold_card_status=false",
     links="order > clinician: names / named by; order > payer: bills / billed by",
     actions="authorize = clear; pend = park; escalate = refer up; submit = send",
     sources="payer portal; intake log; clinician note; scheduling system; fax cover sheet; phone memo",
     inert="""
     fax_machine_tray | cat | upper; lower
     waiting_area_tv | cat | news; weather; cooking show
     receptionist_scarf | cat | plaid; solid; floral
     courtyard_fountain | cat | running; off for cleaning
     lobby_carpet | cat | grey; blue; brown
     """,
     affix="undocumented => clinical_notes_attached; unreviewed => peer_review_held"),

dict(slot="hc-07", slug="records-release", sector="healthcare_admin",
     sub="medical records release desk handling copy and disclosure requests",
     org="Brightharrow Health System", desk="release-of-information desk",
     setting="A health system's records office receives requests for copies of patient records from patients, "
             "lawyers, insurers and other providers. The release desk checks each request against the disclosure "
             "and fee rules before records go out.",
     decider="file clerk",
     roles="release specialist; privacy officer; records supervisor; copy service liaison; legal desk clerk; "
           "patient advocate",
     docs="release request; signed authorization; fee invoice; disclosure log; copy cover letter; records index",
     scope=("records office", "Central Records; North Campus; South Campus; Clinic Archive"),
     money="dollars",
     ents=[
        dict(key="release", singular="release request", plural="release requests", id="RR", aka="chart copy request",
             attrs="""
             pages_requested | int | 1..1800 pages | aka=page count
             copy_fee | money | 0.00..380.00 | aka=fee quoted
             days_open | int | 0..60 days | aka=days since received
             date_span_years | int | 1..25 years | aka=years of history covered
             requester_type | cat | patient; attorney; insurer; provider; court; family member
             delivery_format | cat | paper; secure email; portal download; disc
             authorization_signed | state | bad=0 | aka=signed authorization on file | grp=authorization
             authorization_expired | state | bad=1 | aka=authorization past its end date | grp=authorization
             identity_verified | event | bad=0 | aka=identity of the asker checked
             sensitive_notes_included | state | bad=1 | aka=includes protected notes
             fee_paid | event | bad=0 | aka=payment received
             received_on | date
             due_on | date
             release_tags | tag | rush; subpoena; continuity of care; deceased patient; minor patient; amendment
             """),
        dict(key="patient", singular="patient", plural="patients", id="PC", names="person", role="person",
             attrs="""
             age_years | int | 0..99 years | aka=age
             restriction_on_file | state | bad=1 | aka=disclosure restriction filed
             """),
        dict(key="requester", singular="requester", plural="requesters", id="RQ", names="person", role="person",
             attrs="""
             requests_this_year | int | 1..40 entries | aka=requests filed this year
             requester_standing | ord | new; familiar; preferred | aka=requester history level
             """),
     ],
     outcomes=["release records; release with redactions; hold for payment*; send to privacy officer; "
               "return for new authorization*",
               "charge per page*; charge flat fee; release at zero cost"],
     levels=["routine; priority; rush", "low; moderate; high; critical"],
     words="""
     bulky: pages_requested >= 500
     slim: pages_requested < 20
     hefty: copy_fee >= 150
     overdue: days_open > 30
     fresh: days_open <= 3
     sweeping: date_span_years >= 10
     sanctioned: authorization_signed
     stale: authorization_expired
     authenticated: identity_verified
     remitted: fee_paid
     delicate: sensitive_notes_included
     juvenile: age_years < 18
     prolific: requests_this_year >= 12
     legal: requester_type in {attorney, court}
     """,
     cues="lacks a signed authorization => authorization_signed=false; failed to prove identity => "
          "identity_verified=false; has no payment on file => fee_paid=false",
     links="release > patient: concerns / concerned by; release > requester: lists / listed by",
     actions="release = send out; redact = black out; log = record; invoice = bill",
     sources="disclosure log; request fax; privacy officer email; payment system; patient phone call; "
             "copy service report",
     inert="""
     scanner_lid_colour | cat | grey; black
     archive_box_brand | cat | brand A; brand B
     corridor_painting | cat | seascape; forest; city
     elevator_bank | cat | east elevators; west elevators
     desk_lamp | cat | brass; chrome; white
     """,
     affix="unsigned => authorization_signed; unverified => identity_verified"),

dict(slot="hc-08", slug="specialist-referrals", sector="healthcare_admin",
     sub="referral coordination for specialist visits from a primary care practice",
     org="Hollins Ferry Family Practice", desk="referral coordination desk",
     setting="A family practice sends patients to outside specialists. The referral desk decides how each referral "
             "is routed, what must be attached and whether the payer's referral rules are met before it is sent.",
     decider="medical assistant",
     roles="referral coordinator; practice manager; primary physician; specialist office contact; payer liaison; "
           "nurse care manager",
     docs="referral form; visit summary; specialist acceptance note; payer referral notice; tracking sheet; "
          "loop-closure letter",
     scope=("specialty", "Cardiology; Neurology; Gastroenterology; Dermatology; Orthopedics; Endocrinology"),
     money="dollars",
     ents=[
        dict(key="referral", singular="referral", plural="referrals", id="RF", aka="specialist referral",
             attrs="""
             days_waiting | int | 0..90 days | aka=wait so far
             visits_authorized | int | 1..12 visits | aka=authorized visits
             distance_miles | dec1 | 0.5..85.0 miles | aka=travel distance
             copay_amount | money | 0.00..120.00 | aka=specialist copay
             referral_priority | ord | routine; soon; urgent | aka=referral urgency
             plan_kind | cat | gatekeeper plan; open access plan; public plan; self-pay
             summary_attached | state | bad=0 | aka=visit summary on file | grp=attachments
             specialist_accepted | event | bad=0 | aka=specialist office accepted
             payer_number_issued | event | bad=0 | aka=payer referral number received
             report_returned | event | bad=0 | aka=consult report back
             second_referral_sent | event | bad=1 | aka=referral sent twice
             sent_on | date
             valid_until | date
             referral_tags | tag | new problem; follow-up; second opinion; procedure consult; imaging attached
             """),
        dict(key="patient", singular="patient", plural="patients", id="PF", names="person", role="person",
             attrs="""
             open_referrals | int | 0..5 items | aka=referrals in progress
             transport_access | ord | limited; fair; good | aka=access to transport
             """),
        dict(key="specialist", singular="specialist office", plural="specialist offices", id="SQ",
             names="org: Specialists, Medical Group, Clinic, Associates",
             attrs="""
             next_open_days | int | 1..120 days | aka=next opening
             network_member | state | bad=0 | aka=in the payer network
             """),
     ],
     outcomes=["send referral; send after payer number; route to care manager; hold for summary*; "
               "redirect to another office; close referral*",
               "book by phone; book by fax; book through portal; return to sender*"],
     levels=["routine; soon; urgent", "low; medium; high"],
     words="""
     stalled: days_waiting >= 30
     prompt: days_waiting <= 3
     remote: distance_miles >= 40
     nearby: distance_miles < 5
     pricey: copay_amount >= 60
     generous: visits_authorized >= 6
     annotated: summary_attached
     welcomed: specialist_accepted
     ticketed: payer_number_issued
     concluded: report_returned
     busy: next_open_days >= 45
     covered: network_member
     pressing: referral_priority == urgent
     redundant: second_referral_sent
     """,
     cues="lacks a visit summary => summary_attached=false; was never accepted by the specialist office => "
          "specialist_accepted=false; holds no payer referral number => payer_number_issued=false",
     links="referral > patient: names / named by; referral > specialist: targets / targeted by",
     actions="send = transmit; track = follow; redirect = reroute; close = finish",
     sources="tracking sheet; specialist office call; payer portal; fax confirmation; care manager note; "
             "patient message",
     inert="""
     sticky_pad_colour | cat | yellow; pink; green
     potted_plant | cat | cactus; spider plant; ivy
     stapler_brand | cat | brand X; brand Y
     coat_hook | cat | hook 1; hook 2; hook 3
     radio_volume | cat | low; medium; loud
     """,
     affix="unaccepted => specialist_accepted; unreturned => report_returned"),

dict(slot="hc-09", slug="dictation-queue", sector="healthcare_admin",
     sub="transcription queue for clinician dictations with turnaround and quality rules",
     org="Ashcombe Medical Documentation Services", desk="transcription queue desk",
     setting="A documentation service turns clinician dictations into typed reports for several clinics. The queue "
             "desk routes each dictation, applies turnaround targets and decides when a report needs quality "
             "review.",
     decider="medical transcriptionist",
     roles="queue lead; quality editor; account manager; clinic office manager; dictating clinician; "
           "turnaround analyst",
     docs="dictation ticket; typed report; quality score sheet; turnaround report; client contract summary; "
          "style guide",
     scope=("client clinic", "Fairhaven Clinic; Kesley Orthopedics; Millbank Pediatrics; Tolland Surgical"),
     money="dollars",
     ents=[
        dict(key="dictation", singular="dictation", plural="dictations", id="DC", aka="voice file",
             attrs="""
             audio_minutes | dec1 | 0.5..45.0 minutes | aka=audio length
             hours_in_queue | int | 0..96 hours | aka=queue time
             line_count | int | 5..600 lines | aka=report lines
             accuracy_score | dec1 | 80.0..100.0 percent | aka=quality score
             line_rate | money | 0.06..0.25 | aka=charge per line
             report_type | cat | operative note; consult note; discharge summary; clinic letter; procedure note
             audio_quality | ord | poor; fair; good; clear | aka=sound quality
             dictation_device | cat | desk phone; mobile app; handheld voice unit; web portal | aka=capture device
             stat_flag_set | event | bad=0 | aka=marked stat
             gaps_left | state | bad=1 | aka=report has gaps | grp=completeness
             clinician_signed | event | bad=0 | aka=signed by the clinician
             template_applied | state | bad=0 | aka=clinic template used
             received_on | date
             due_on | date
             dictation_tags | tag | accented speech; background noise; new client; long report; addendum
             """),
        dict(key="clinician", singular="dictating clinician", plural="dictating clinicians", id="DR", names="person",
             role="person",
             attrs="""
             dictations_this_month | int | 0..300 items | aka=monthly dictations
             speaks_quickly | state | bad=1 | aka=fast speaker
             """),
        dict(key="transcriber", singular="transcriber", plural="transcribers", id="TR", names="person", role="person",
             attrs="""
             experience_years | int | 0..30 years | aka=years of experience
             queue_load | int | 0..40 items | aka=open files
             """),
     ],
     outcomes=["deliver report; send to quality editor; return to transcriber*; hold for clinician*; "
               "escalate to account manager",
               "bill standard rate; bill stat rate*; bill zero"],
     levels=["poor; fair; good; excellent", "routine; priority; stat"],
     words="""
     lengthy: audio_minutes >= 20
     brief: audio_minutes < 2
     overdue: hours_in_queue > 48
     fresh: hours_in_queue <= 2
     sprawling: line_count >= 300
     accurate: accuracy_score >= 98
     sloppy: accuracy_score < 90
     urgent: stat_flag_set
     endorsed: clinician_signed
     standardized: template_applied
     prolific: dictations_this_month >= 150
     veteran: experience_years >= 10
     swamped: queue_load >= 25
     surgical: report_type == operative note
     muffled: audio_quality == poor
     """,
     cues="was never signed by the clinician => clinician_signed=false; lacks the clinic template => "
          "template_applied=false; has no gaps left in it => gaps_left=false",
     links="dictation > clinician: credits / credited by; dictation > transcriber: assigns / assigned by",
     actions="route = direct; proofread = revise; deliver = send; flag = mark",
     sources="queue dashboard; quality score sheet; clinic office email; clinician voicemail; turnaround report; "
             "transcriber chat",
     inert="""
     keyboard_layout | cat | layout A; layout B
     foot_pedal_model | cat | pedal 1; pedal 2
     headphone_colour | cat | black; white; red
     desk_fan | cat | on; off
     wallpaper_theme | cat | waves; stripes; plain
     """,
     affix="unsigned => clinician_signed; untemplated => template_applied"),

dict(slot="hc-10", slug="chart-deficiency", sector="healthcare_admin",
     sub="chart completion and coding query tracking in a hospital records department",
     org="Larkspur Valley Medical Center", desk="chart completion desk",
     setting="After discharge, a hospital's records department checks each chart for missing signatures and open "
             "coding queries. The chart completion desk sets each chart's status and decides when a clinician is "
             "placed on the delinquent list.",
     decider="health information technologist",
     roles="chart analyst; coding specialist; physician advisor; records director; unit secretary; "
           "medical staff office clerk",
     docs="deficiency report; coding query; delinquency notice; discharge abstract; signature log; "
          "medical staff letter",
     scope=("unit", "Medical Floor; Surgical Floor; Maternity; Intensive Care; Short Stay"),
     money="dollars",
     ents=[
        dict(key="chart", singular="chart", plural="charts", id="CT", aka="patient chart",
             attrs="""
             days_since_discharge | int | 0..90 days | aka=days after discharge
             open_deficiencies | int | 0..12 items | aka=outstanding items
             open_queries | int | 0..6 items | aka=coding queries open
             expected_payment | money | 800.00..95000.00 | aka=expected reimbursement
             stay_days | int | 1..40 days | aka=stay length
             chart_type | cat | inpatient; observation; outpatient surgery; emergency
             severity_class | ord | minor; moderate; major; extreme | aka=severity
             discharge_summary_signed | event | bad=0 | aka=discharge summary signed | grp=signatures
             operative_report_present | state | bad=0 | aka=operative report filed
             query_answered | event | bad=0 | aka=coding query answered | grp=queries
             final_coded | event | bad=0 | aka=chart coded
             history_on_file | state | bad=0 | aka=history and physical filed
             discharged_on | date
             query_sent_on | date
             chart_tags | tag | readmission; transfer in; death; newborn; teaching case; audit sample
             """),
        dict(key="physician", singular="attending physician", plural="attending physicians", id="AT", names="person",
             role="person",
             attrs="""
             delinquent_charts | int | 0..30 items | aka=overdue charts
             suspension_warnings | int | 0..4 entries | aka=warnings this year
             """),
        dict(key="coder", singular="coder", plural="coders", id="CD", names="person", role="person",
             attrs="""
             charts_coded_today | int | 0..60 items | aka=daily output
             credential_level | ord | trainee; certified; senior certified | aka=coder credential
             """),
     ],
     outcomes=["mark complete; send signature notice; send coding query; place on delinquent list*; "
               "send to physician advisor; hold billing*",
               "bill now; bill after query; rebill*"],
     levels=["minor; moderate; major; extreme", "green; yellow; orange; red"],
     words="""
     tardy: days_since_discharge > 30
     fresh: days_since_discharge <= 2
     cluttered: open_deficiencies >= 5
     clean: open_deficiencies < 1
     probed: open_queries >= 1
     lucrative: expected_payment >= 40000
     extended: stay_days >= 10
     endorsed: discharge_summary_signed
     resolved: query_answered
     finalized: final_coded
     chronic: delinquent_charts >= 10
     cautioned: suspension_warnings >= 2
     veteran: credential_level == senior certified
     critical: severity_class == extreme
     surgical: operative_report_present
     """,
     cues="lacks a signed discharge summary => discharge_summary_signed=false; was never answered by the "
          "physician => query_answered=false; has no history and physical filed => history_on_file=false",
     links="chart > physician: names / named by; chart > coder: assigns / assigned by",
     actions="query = ask; complete = finish; suspend = pause privileges; abstract = summarize",
     sources="deficiency report; signature log; coder worklist; medical staff office email; unit secretary note; "
             "query system",
     inert="""
     folder_thickness | cat | thin; medium; thick
     scanner_station | cat | station 1; station 2; station 3
     break_room_snack | cat | pretzels; apples; cookies
     window_view | cat | parking lot; garden; street
     wall_clock_brand | cat | brand M; brand N
     """,
     affix="unsigned => discharge_summary_signed; unanswered => query_answered"),
]
