"""packs-2 sector lg: legal practice administration (Claude-written pack sources; invented firms and entities)."""

PACKS = [
dict(slot="lg-01", slug="filing-docket", sector="legal_practice_admin",
     sub="docketing desk that tracks court filing deadlines for a litigation practice",
     org="Hargrove Pell and Tannery LLP", desk="docketing desk",
     setting="A litigation firm records every court deadline in a central docket. The docketing desk computes due "
             "dates from the firm's calendaring rules and decides when a deadline is escalated to the responsible "
             "lawyer.",
     decider="legal secretary",
     roles="docketing clerk; responsible partner; associate; litigation support lead; records manager; "
           "conflicts analyst",
     docs="docket entry; court notice; deadline report; extension stipulation; calendaring rule sheet; "
          "filing receipt",
     scope=("court", "County Civil Court; District Court; Appeals Panel; Bankruptcy Court; Tax Tribunal"),
     money="dollars",
     ents=[
        dict(key="deadline", singular="docket deadline", plural="docket deadlines", id="DK", aka="court deadline",
             attrs="""
             days_to_due | int | 0..90 days | aka=days remaining
             response_period_days | int | 7..60 days | aka=response window
             extensions_granted | int | 0..3 entries | aka=extensions so far
             filing_fee | money | 0.00..450.00 | aka=court fee
             service_method | cat | personal delivery; mail; electronic service; publication
             deadline_kind | cat | answer; motion response; discovery response; appeal notice; brief; status report
             priority_tier | ord | standard; elevated; critical | aka=docket priority
             notice_received | event | bad=0 | aka=court notice logged | grp=notice
             extension_filed | event | bad=0 | aka=extension motion filed
             lawyer_acknowledged | event | bad=0 | aka=responsible lawyer confirmed
             holiday_in_window | state | bad=1 | aka=court holiday falls in the period
             tolling_order_active | state | bad=0 | aka=stay order in force
             served_on | date
             due_on | date
             deadline_tags | tag | jurisdictional; client approval; expert report; sealed filing; joint filing
             """),
        dict(key="matter", singular="matter", plural="matters", id="MT", names=["Matter Calloway Mills", "Matter Rosebank Freight", "Matter Ventry Holdings", "Matter Ashgrove Dairy", "Matter Pemmick Tools", "Matter Haldane Marine", "Matter Corvel Textiles", "Matter Quarrie Foods"],
             attrs="""
             open_deadlines | int | 0..25 items | aka=active deadlines
             matter_value | money | 5000.00..9000000.00 | aka=amount at stake
             """),
        dict(key="lawyer", singular="responsible lawyer", plural="responsible lawyers", id="RW", names="person",
             role="person",
             attrs="""
             docket_load | int | 0..60 items | aka=deadlines on desk
             seniority_band | ord | junior; mid-level; senior | aka=seniority
             """),
     ],
     outcomes=["calendar as computed; calendar with early warning; escalate to partner; ask court clerk; "
               "mark missed*",
               "file now; file after review; seek extension*"],
     levels=["standard; elevated; critical", "low; medium; high; urgent"],
     words="""
     imminent: days_to_due <= 3
     distant: days_to_due >= 45
     brisk: response_period_days <= 10
     extended: extensions_granted >= 1
     hefty: filing_fee >= 250
     heeded: lawyer_acknowledged
     triggered: notice_received
     frozen: tolling_order_active
     crowded: open_deadlines >= 12
     overloaded: docket_load >= 40
     veteran: seniority_band == senior
     appellate: deadline_kind == appeal notice
     weighty: matter_value >= 1000000
     festive: holiday_in_window
     pressing: priority_tier == critical
     postponed: extension_filed
     """,
     cues="was never acknowledged by the lawyer => lawyer_acknowledged=false; lacks a logged court notice => "
          "notice_received=false; has no stay order in force => tolling_order_active=false",
     links="deadline > matter: belongs to / owned by; deadline > lawyer: assigns / assigned by",
     actions="calendar = enter date; compute = calculate; remind = prompt; file = lodge",
     sources="court portal; docket report; partner email; clerk phone call; filing receipt; "
             "calendaring rule sheet",
     inert="""
     binder_ring_size | cat | one inch; two inch; three inch
     conference_room_art | cat | maps; portraits; abstract
     courier_jacket | cat | yellow; navy; red
     lobby_flowers | cat | lilies; tulips; roses
     water_cooler | cat | full; low
     """,
     affix="unacknowledged => lawyer_acknowledged; unlogged => notice_received"),

dict(slot="lg-02", slug="conflict-intake", sector="legal_practice_admin",
     sub="conflict check and new matter intake for a regional law firm",
     org="Fennick Ross Advocates", desk="new matter intake desk",
     setting="Before a new client matter is opened, a regional law firm searches its records for conflicts of "
             "interest. The intake desk applies the firm's conflict and engagement rules and decides whether the "
             "matter opens, waits or goes to the ethics partner.",
     decider="paralegal",
     roles="intake analyst; ethics partner; originating lawyer; billing coordinator; records clerk; "
           "practice group leader",
     docs="new matter form; conflict search report; engagement letter; waiver letter; client questionnaire; "
          "matter opening memo",
     scope=("practice group", "Employment; Real Property; Commercial Contracts; Family; Estates"),
     money="dollars",
     ents=[
        dict(key="intake", singular="new matter intake", plural="new matter intakes", id="NM", aka="matter opening",
             attrs="""
             search_hits | int | 0..40 items | aka=conflict search hits
             retainer_amount | money | 0.00..50000.00 | aka=retainer
             estimated_fees | money | 1000.00..400000.00 | aka=fee estimate
             days_open | int | 0..30 days | aka=days in intake
             adverse_parties | int | 1..12 people | aka=parties on the other side
             client_kind | cat | individual; small business; nonprofit; public body; corporation
             conflict_level | ord | clear; possible; direct | aka=conflict finding
             engagement_signed | event | bad=0 | aka=engagement letter signed | grp=engagement
             waiver_obtained | event | bad=0 | aka=conflict waiver received
             former_client_match | state | bad=1 | aka=adverse party was a client before
             retainer_received | event | bad=0 | aka=retainer deposited
             identity_checked | event | bad=0 | aka=client identity confirmed
             opened_on | date
             statute_date | date
             intake_tags | tag | referral; repeat client; pro bono; contingency; urgent filing; cross-border
             """),
        dict(key="client", singular="prospective client", plural="prospective clients", id="PQ", names="person",
             role="person",
             attrs="""
             prior_matters | int | 0..15 items | aka=earlier matters with the firm
             account_in_good_standing | state | bad=0 | aka=account in good order
             outstanding_invoice | money | 0.00..30000.00 | aka=old balance owed
             """),
        dict(key="lawyer", singular="originating lawyer", plural="originating lawyers", id="GW", names="person",
             role="person",
             attrs="""
             new_matters_this_quarter | int | 0..30 items | aka=matters opened this quarter
             partner_track | ord | associate; counsel; partner | aka=title band
             """),
     ],
     outcomes=["open matter; open after waiver; send to ethics partner; hold for retainer*; "
               "turn away matter*",
               "hourly billing; flat fee; contingency fee; prepaid retainer only*"],
     levels=["clear; possible; direct", "low; moderate; high"],
     words="""
     noisy: search_hits >= 10
     quiet: search_hits < 1
     sizable: estimated_fees >= 100000
     modest: estimated_fees < 5000
     funded: retainer_received
     excused: waiver_obtained
     contracted: engagement_signed
     stalled: days_open >= 14
     crowded: adverse_parties >= 5
     loyal: prior_matters >= 3
     indebted: outstanding_invoice > 1000
     busy: new_matters_this_quarter >= 15
     incorporated: client_kind == corporation
     compromised: conflict_level == direct
     entangled: former_client_match
     """,
     cues="lacks a signed engagement letter => engagement_signed=false; holds no conflict waiver => "
          "waiver_obtained=false; was never identified in person => identity_checked=false",
     links="intake > client: names / named by; intake > lawyer: credits / credited by",
     actions="search = run check; activate = switch on; engage = sign up; waive = consent",
     sources="conflict search report; client questionnaire; partner email; records system; intake call notes; "
             "billing system",
     inert="""
     pen_brand | cat | brand P; brand Q
     reception_coffee | cat | dark roast; light roast; decaf
     umbrella_colour | cat | black; tartan; clear
     lounge_view | cat | river; courtyard; street
     folder_tab_colour | cat | red tab; green tab
     """,
     affix="unsigned => engagement_signed; unfunded => retainer_received"),

dict(slot="lg-03", slug="file-retention", sector="legal_practice_admin",
     sub="records retention and destruction approvals for closed client files",
     org="Quillon Baird Solicitors", desk="records retention desk",
     setting="A law firm keeps closed client files for set periods and then destroys or returns them. The "
             "retention desk checks every closed file against the retention schedule and any legal holds before "
             "approving destruction.",
     decider="archivist",
     roles="records coordinator; risk partner; file room clerk; offsite storage liaison; client relations clerk; "
           "information governance lead",
     docs="retention schedule; destruction certificate; legal hold notice; file closing checklist; "
          "storage invoice; client consent letter",
     scope=("storage location", "Basement Vault; Offsite Depot; Branch Annex; Digital Archive"),
     money="pounds sterling",
     ents=[
        dict(key="file", singular="closed file", plural="closed files", id="CF", aka="archived file",
             attrs="""
             years_since_closing | int | 0..30 years | aka=age since closing
             retention_years | int | 3..25 years | aka=retention period
             boxes | int | 1..40 units | aka=box count
             storage_cost_per_year | money | 5.00..900.00 | aka=yearly storage charge
             matter_area | cat | conveyancing; probate; litigation; employment; corporate; family
             media_type | cat | paper; digital; mixed
             sensitivity_grade | ord | general; confidential; restricted | aka=sensitivity
             legal_hold_active | state | bad=1 | aka=hold in force | grp=hold
             original_deeds_inside | state | bad=1 | aka=contains original deeds
             client_consented | event | bad=0 | aka=client agreed to destruction
             partner_signed_off | event | bad=0 | aka=partner approval given
             closed_on | date
             review_due_on | date
             file_tags | tag | minor client; wills; trust deeds; court bundle; regulator query
             """),
        dict(key="client", singular="former client", plural="former clients", id="FC", names="person",
             role="person",
             attrs="""
             client_age_years | int | 18..100 years | aka=client age
             contact_current | state | bad=0 | aka=contact details up to date
             """),
        dict(key="depot", singular="storage depot", plural="storage depots", id="SD",
             names="org: Storage, Archives, Archive Depot",
             attrs="""
             capacity_used | dec1 | 10.0..100.0 percent | aka=fill level
             retrieval_hours | int | 2..72 hours | aka=retrieval time
             """),
     ],
     outcomes=["destroy file; return file to client; keep for another year; send to risk partner; "
               "keep permanently*",
               "shred onsite; shred offsite; delete digital copy; recall to office*"],
     levels=["general; confidential; restricted", "low; medium; high"],
     words="""
     ancient: years_since_closing >= 20
     fresh: years_since_closing <= 2
     bulky: boxes >= 10
     hefty: storage_cost_per_year >= 300
     frozen: legal_hold_active
     authorized: client_consented
     approved: partner_signed_off
     sensitive: sensitivity_grade == restricted
     electronic: media_type == digital
     traceable: contact_current
     crowded: capacity_used >= 90
     slow: retrieval_hours >= 48
     testamentary: matter_area == probate
     precious: original_deeds_inside
     enduring: retention_years >= 15
     """,
     cues="was never signed off by a partner => partner_signed_off=false; lacks client consent => "
          "client_consented=false; has no hold in force => legal_hold_active=false",
     links="file > client: concerns / concerned by; file > depot: stores at / chosen by",
     actions="destroy = shred; retain = keep; recall = bring back; certify = attest",
     sources="retention schedule; hold register; depot manifest; partner email; client letter; file room log",
     inert="""
     crate_print_font | cat | bold; italic; plain
     depot_gate_code_colour | cat | green; blue
     shelf_paint | cat | grey; cream
     trolley_wheel | cat | squeaky; smooth
     archive_room_light | cat | warm; cool
     """,
     affix="unsigned => partner_signed_off; unconsented => client_consented"),

dict(slot="lg-04", slug="title-search", sector="legal_practice_admin",
     sub="title search order desk that clears exceptions before a property closing",
     org="Marrowby Title and Abstract", desk="title search desk",
     setting="A title company searches public records on each property before a sale closes. The search desk "
             "lists liens and other exceptions and decides whether the title can be insured, needs curative work "
             "or goes to underwriting.",
     decider="title examiner",
     roles="abstractor; curative specialist; title underwriter; closing coordinator; lender liaison; "
           "escrow officer",
     docs="title commitment; chain of title report; lien release; payoff letter; survey; curative checklist",
     scope=("county", "Ashby County; Brennock County; Coldwater County; Durran County; Eskdale County"),
     money="dollars",
     ents=[
        dict(key="search", singular="title search", plural="title searches", id="TS", aka="search order",
             attrs="""
             years_searched | int | 10..60 years | aka=search depth
             open_liens | int | 0..8 items | aka=liens found
             lien_total | money | 0.00..450000.00 | aka=sum of liens
             sale_price | money | 40000.00..3500000.00 | aka=contract price
             days_to_closing | int | 0..60 days | aka=time to closing
             property_kind | cat | single family; condo unit; vacant land; duplex; commercial lot
             gap_in_chain | state | bad=1 | aka=break in the chain of title | grp=chain
             payoff_letter_received | event | bad=0 | aka=payoff letter in hand
             survey_current | state | bad=0 | aka=survey up to date
             easement_registered | state | bad=1 | aka=registered easement found
             probate_closed | event | bad=0 | aka=estate closed in probate court
             ordered_on | date
             closing_on | date
             search_tags | tag | estate sale; foreclosure; new construction; divorce; trust owner; boundary dispute
             exception_level | ord | standard; special; underwriter only | aka=exception class
             """),
        dict(key="owner", singular="title owner", plural="title owners", id="RW", names="person", role="person",
             attrs="""
             years_owned | int | 0..50 years | aka=length of ownership
             owner_count | int | 1..4 people | aka=number of owners
             """),
        dict(key="lender", singular="lender", plural="lenders", id="ND",
             names="org: Bank, Savings, Mortgage, Credit Union",
             attrs="""
             payoff_turnaround_days | int | 1..20 days | aka=payoff reply time
             lender_tier | ord | regional; national; portfolio | aka=lender class
             """),
     ],
     outcomes=["insure as is; insure with exceptions; send to curative; refer to underwriter; "
               "postpone closing*",
               "standard policy; extended policy; postpone policy*"],
     levels=["standard; special; underwriter only", "low; medium; high"],
     words="""
     deep: years_searched >= 40
     encumbered: open_liens >= 3
     heavy: lien_total >= 200000
     pricey: sale_price >= 1000000
     modest: sale_price < 100000
     rushed: days_to_closing <= 5
     fractured: gap_in_chain
     mapped: survey_current
     resolved: probate_closed
     established: years_owned >= 20
     shared: owner_count >= 2
     slow: payoff_turnaround_days >= 10
     barren: property_kind == vacant land
     burdened: easement_registered
     primed: payoff_letter_received
     """,
     cues="lacks a payoff letter => payoff_letter_received=false; has no current survey => survey_current=false; "
          "was never closed in probate court => probate_closed=false",
     links="search > owner: names / named by; search > lender: notifies / notified by",
     actions="search = run records; clear = cure; insure = issue policy; order = request survey",
     sources="county recorder index; probate court docket; lender payoff portal; survey firm email; "
             "closing coordinator note; tax office record",
     inert="""
     map_colour | cat | sepia; blue; green
     filing_queue_number | cat | ticket 1; ticket 2; ticket 3
     abstract_paper | cat | bond; linen
     office_dog_breed | cat | beagle; terrier; collie
     parking_meter | cat | coin; card
     """,
     affix="unsurveyed => survey_current; unsettled => probate_closed"),

dict(slot="lg-05", slug="pro-bono-intake", sector="legal_practice_admin",
     sub="pro bono program intake at a large law firm",
     org="Tavistock Greer and Holloway LLP", desk="pro bono intake desk",
     setting="A large firm takes pro bono cases referred by legal aid partners. The pro bono intake desk applies "
             "the program's eligibility, capacity and conflict rules and decides how each referral is placed.",
     decider="lawyer",
     roles="pro bono coordinator; supervising partner; volunteer associate; legal aid liaison; conflicts clerk; "
           "program counsel",
     docs="referral sheet; income worksheet; case acceptance memo; volunteer roster; closing report; "
          "partner agreement",
     scope=("case area", "Housing; Immigration; Veterans Benefits; Small Nonprofits; Guardianship"),
     money="dollars",
     ents=[
        dict(key="referral", singular="pro bono referral", plural="pro bono referrals", id="PB",
             aka="case referral",
             attrs="""
             household_income | money | 0.00..120000.00 | aka=yearly household income
             income_limit_percent | int | 100..400 percent | aka=income as a share of the guideline
             estimated_hours | int | 5..400 hours | aka=hours estimate
             days_to_hearing | int | 0..120 days | aka=time until hearing
             referring_partner | cat | city legal aid; tenant clinic; veterans center; bar association; law school clinic
             case_complexity | ord | simple; moderate; complex | aka=complexity
             conflict_cleared | event | bad=0 | aka=conflicts cleared | grp=conflict
             client_interviewed | event | bad=0 | aka=intake interview held
             documents_complete | state | bad=0 | aka=papers complete
             emergency_hearing | state | bad=1 | aka=hearing on short notice
             fee_generating | state | bad=1 | aka=case could earn fees
             received_on | date
             hearing_on | date
             referral_tags | tag | language access; elderly client; eviction; asylum; benefits appeal; board work
             """),
        dict(key="client", singular="applicant", plural="applicants", id="AQ", names="person", role="person",
             attrs="""
             household_members | int | 1..10 people | aka=household size
             earlier_pro_bono_cases | int | 0..5 items | aka=past pro bono cases
             """),
        dict(key="volunteer", singular="volunteer lawyer", plural="volunteer lawyers", id="VW", names="person",
             role="person",
             attrs="""
             pro_bono_hours_ytd | int | 0..300 hours | aka=hours this year
             experience_band | ord | first-year; mid-level; senior | aka=experience
             """),
     ],
     outcomes=["accept and staff; accept for advice only; refer back to partner; send to supervising partner; "
               "place on hold*; return referral*",
               "full representation; limited scope; brief advice*"],
     levels=["simple; moderate; complex", "low; medium; high; urgent"],
     words="""
     needy: income_limit_percent <= 125
     comfortable: income_limit_percent >= 300
     sprawling: estimated_hours >= 150
     quick: estimated_hours <= 20
     pressing: days_to_hearing <= 7
     vetted: conflict_cleared
     consulted: client_interviewed
     assembled: documents_complete
     populous: household_members >= 6
     familiar: earlier_pro_bono_cases >= 1
     dedicated: pro_bono_hours_ytd >= 100
     seasoned: experience_band == senior
     intricate: case_complexity == complex
     destitute: household_income < 15000
     frantic: emergency_hearing
     profitable: fee_generating
     """,
     cues="was never interviewed at intake => client_interviewed=false; lacks complete papers => "
          "documents_complete=false; has no conflicts clearance => conflict_cleared=false",
     links="referral > client: names / named by; referral > volunteer: staffs / staffed by",
     actions="accept = take on; staff = place; advise = counsel; close = wrap up",
     sources="referral sheet; partner portal; intake interview notes; conflicts report; volunteer roster; "
             "court calendar",
     inert="""
     brochure_colour | cat | teal; purple; orange
     lobby_table_shape | cat | round; square
     lanyard_style | cat | woven; plain
     ceiling_fan | cat | on; off
     framed_poster | cat | skyline; harbour; mountains
     """,
     affix="uninterviewed => client_interviewed; incomplete => documents_complete"),

dict(slot="lg-06", slug="mediation-center", sector="legal_practice_admin",
     sub="case administration at a community mediation center",
     org="Ravensholt Community Mediation Center", desk="case administration desk",
     setting="A community mediation center receives disputes from courts, landlords and neighbours. The case "
             "administration desk applies the center's intake, fee and session rules and decides how each case "
             "is booked.",
     decider="mediator",
     roles="case administrator; staff mediator; volunteer mediator; court liaison; program director; "
           "scheduling assistant",
     docs="case intake sheet; agreement to mediate; session notice; fee schedule; settlement memorandum; "
          "court referral order",
     scope=("venue", "Downtown Office; Library Annex; Courthouse Room; Video Session"),
     money="dollars",
     ents=[
        dict(key="case", singular="mediation case", plural="mediation cases", id="MC", aka="dispute file",
             attrs="""
             parties_count | int | 2..8 people | aka=number of parties
             amount_in_dispute | money | 0.00..60000.00 | aka=sum disputed
             session_fee | money | 0.00..400.00 | aka=fee per session
             sessions_held | int | 0..6 sessions | aka=sessions so far
             days_since_referral | int | 0..90 days | aka=age of the case
             dispute_kind | cat | neighbour; landlord and tenant; consumer; workplace; family; small claims
             intensity_level | ord | calm; tense; volatile | aka=tension level
             agreement_signed | event | bad=0 | aka=agreement to mediate signed | grp=agreement
             court_ordered | state | bad=0 | aka=sent by court order
             interpreter_arranged | event | bad=0 | aka=interpreter booked
             safety_screen_flagged | event | bad=1 | aka=safety screening flag raised
             fee_waiver_granted | event | bad=0 | aka=fee waiver approved
             referred_on | date
             session_on | date
             case_tags | tag | repeat parties; elder; youth; online only; multi-party; return to court
             """),
        dict(key="party", singular="party", plural="parties", id="PZ", names="person", role="person",
             attrs="""
             party_income | money | 0.00..150000.00 | aka=yearly income
             missed_sessions | int | 0..3 sessions | aka=sessions missed
             party_represented | state | bad=0 | aka=party has a lawyer
             """),
        dict(key="mediator", singular="mediator", plural="mediators", id="MD", names="person", role="person",
             attrs="""
             cases_mediated | int | 0..500 items | aka=career case count
             certification_grade | ord | apprentice; certified; senior certified | aka=mediator grade
             """),
     ],
     outcomes=["book joint session; book separate sessions; send to program director; return to court*; "
               "close case*",
               "charge full fee*; charge sliding fee; waive fee"],
     levels=["calm; tense; volatile", "low; medium; high"],
     words="""
     crowded: parties_count >= 4
     sizable: amount_in_dispute >= 10000
     trivial: amount_in_dispute < 200
     pricey: session_fee >= 150
     prolonged: sessions_held >= 3
     stale: days_since_referral >= 60
     committed: agreement_signed
     mandated: court_ordered
     alarming: safety_screen_flagged
     excused: fee_waiver_granted
     veteran: cases_mediated >= 200
     absent: missed_sessions >= 1
     domestic: dispute_kind == family
     heated: intensity_level == volatile
     """,
     cues="lacks a signed agreement to mediate => agreement_signed=false; was never sent by court order => "
          "court_ordered=false; holds no fee waiver => fee_waiver_granted=false",
     links="case > party: names / named by; case > mediator: assigns / assigned by",
     actions="book = set date; screen = vet; settle = record agreement; waive = forgive",
     sources="court referral order; intake call notes; mediator report; party email; fee ledger; session notice",
     inert="""
     tissue_box_pattern | cat | floral; plain; striped
     whiteboard_size | cat | small board; large board
     waiting_room_puzzle | cat | jigsaw; crossword; puzzle put away
     window_curtain | cat | open curtain; drawn curtain
     door_plaque_colour | cat | green sign; blue sign
     """,
     affix="unsigned => agreement_signed; unscreened => safety_screen_flagged"),

dict(slot="lg-07", slug="trust-disbursements", sector="legal_practice_admin",
     sub="client trust account disbursement checks at a small law firm",
     org="Dunmore and Achterberg Law Offices", desk="trust accounting desk",
     setting="A small law firm holds client money in a trust account and pays it out on instruction. The trust "
             "accounting desk checks each disbursement against the client's ledger balance and the firm's "
             "trust rules before releasing funds.",
     decider="bookkeeping clerk",
     roles="trust bookkeeper; managing partner; matter lawyer; bank liaison; compliance reviewer; "
           "accounts assistant",
     docs="disbursement request; client ledger card; three-way reconciliation; settlement statement; "
          "bank confirmation; trust audit note",
     scope=("trust account", "Main Trust Account; Real Estate Trust; Settlement Trust; Escrow Sub-Account"),
     money="dollars",
     ents=[
        dict(key="disbursement", singular="trust disbursement", plural="trust disbursements", id="TD",
             aka="payout",
             attrs="""
             payout_amount | money | 10.00..250000.00 | aka=amount to pay out
             ledger_balance | money | 0.00..300000.00 | aka=client ledger balance
             days_since_deposit | int | 0..60 days | aka=days since funds arrived
             payees | int | 1..6 people | aka=number of payees
             payment_channel | cat | wire; cheque; ACH transfer; internal transfer
             purpose_code | cat | settlement payout; fee transfer; cost reimbursement; closing funds; refund to client
             approval_level | ord | clerk; lawyer; partner | aka=approver needed
             funds_cleared | event | bad=0 | aka=deposit cleared the bank | grp=funds
             client_authorized | event | bad=0 | aka=client instruction received
             bill_issued | event | bad=0 | aka=invoice sent before transfer
             wire_callback_done | event | bad=0 | aka=phone callback completed
             reconciled_this_month | state | bad=0 | aka=account reconciled
             requested_on | date
             pay_on | date
             disbursement_tags | tag | third-party payee; medical lien; minor settlement; foreign payee; split fee
             """),
        dict(key="client", singular="client", plural="clients", id="CQ", names="person", role="person",
             attrs="""
             matters_open | int | 1..6 items | aka=open matters
             ledger_negative_before | state | bad=1 | aka=ledger went below zero before
             """),
        dict(key="payee", singular="payee", plural="payees", id="PE",
             names="org: Medical Group, Supply Co., Services, Partners",
             attrs="""
             payee_verified | event | bad=0 | aka=payee details checked
             payments_to_payee | int | 0..30 items | aka=earlier payments
             """),
     ],
     outcomes=["release funds; release after callback; hold until funds clear*; send to managing partner; "
               "return instruction to lawyer*",
               "pay by wire; pay by cheque; pay by transfer; stop payment*"],
     levels=["clerk; lawyer; partner", "low; medium; high"],
     words="""
     hefty: payout_amount >= 50000
     modest: payout_amount < 500
     flush: ledger_balance >= 100000
     fresh: days_since_deposit <= 2
     liquid: funds_cleared
     sanctioned: client_authorized
     charged: bill_issued
     squared: reconciled_this_month
     vetted: payee_verified
     familiar: payments_to_payee >= 3
     busy: matters_open >= 3
     scattered: payees >= 3
     telegraphic: payment_channel == wire
     vouched: wire_callback_done
     lofty: approval_level == partner
     """,
     cues="lacks a cleared deposit => funds_cleared=false; was never authorized by the client => "
          "client_authorized=false; has no completed callback => wire_callback_done=false",
     links="disbursement > client: charges / charged by; disbursement > payee: pays / paid by",
     actions="release = pay out; reconcile = balance; post = enter; callback = phone back",
     sources="client ledger card; bank portal; lawyer email; settlement statement; callback log; "
             "reconciliation report",
     inert="""
     cheque_stock_colour | cat | blue stock; green stock
     calculator_brand | cat | brand R; brand T
     ring_binder_colour | cat | black binder; maroon binder
     office_radio | cat | classical; news
     desk_drawer | cat | top drawer; middle drawer
     """,
     affix="unauthorized => client_authorized; unreconciled => reconciled_this_month"),

dict(slot="lg-08", slug="document-production", sector="legal_practice_admin",
     sub="document production centre that formats, assembles and stamps legal documents",
     org="Brennard Clyde LLP Document Centre", desk="document production centre",
     setting="A law firm's document centre prepares briefs, exhibits and contract sets for lawyers. The centre "
             "applies its turnaround and formatting rules to each job and decides when a job jumps the queue or "
             "goes back to the lawyer.",
     decider="word processor",
     roles="production lead; night shift typist; proofreader; requesting lawyer; legal assistant; "
           "print room operator",
     docs="job ticket; style sheet; exhibit index; proof copy; print order; turnaround report",
     scope=("shift", "Day Shift; Evening Shift; Night Shift; Weekend Shift"),
     money="dollars",
     ents=[
        dict(key="job", singular="production job", plural="production jobs", id="PJ", aka="document job",
             attrs="""
             page_count | int | 1..2500 pages | aka=pages in the job
             exhibits | int | 0..120 items | aka=exhibit count
             hours_to_deadline | int | 1..96 hours | aka=time left
             revision_rounds | int | 0..6 entries | aka=rounds of changes
             overtime_cost | money | 0.00..2400.00 | aka=overtime charge
             job_kind | cat | court brief; contract set; exhibit binder; letter batch; deposition transcript
             output_form | cat | print; electronic filing; both
             complexity_band | ord | light; standard; heavy | aka=job weight
             style_sheet_attached | state | bad=0 | aka=style sheet on file | grp=format
             lawyer_proof_approved | event | bad=0 | aka=proof signed off
             bates_stamped | event | bad=0 | aka=page stamping applied
             redlines_open | state | bad=1 | aka=changes still open
             received_on | date
             due_on | date
             job_tags | tag | filing deadline; client visible; confidential; oversized; colour print; tabbed
             """),
        dict(key="lawyer", singular="requesting lawyer", plural="requesting lawyers", id="RN", names="person",
             role="person",
             attrs="""
             jobs_this_week | int | 0..25 items | aka=jobs sent this week
             practice_area | cat | litigation; corporate; tax; real estate
             """),
        dict(key="operator", singular="operator", plural="operators", id="QP", names="person", role="person",
             attrs="""
             open_jobs | int | 0..15 items | aka=jobs on hand
             skill_grade | ord | trainee; operator; senior operator | aka=operator grade
             operator_certified | state | bad=0 | aka=operator cleared for court filings
             """),
     ],
     outcomes=["start now; queue normally; send proof to lawyer; return for missing style sheet*; "
               "escalate to production lead; refuse rush*",
               "print and bind; file electronically; print and file; reprint job*"],
     levels=["light; standard; heavy", "routine; priority; rush"],
     words="""
     massive: page_count >= 1000
     slim: page_count < 10
     voluminous: exhibits >= 40
     tight: hours_to_deadline <= 4
     relaxed: hours_to_deadline >= 48
     churned: revision_rounds >= 3
     hefty: overtime_cost >= 800
     blessed: lawyer_proof_approved
     branded: bates_stamped
     groomed: style_sheet_attached
     demanding: jobs_this_week >= 10
     loaded: open_jobs >= 8
     veteran: skill_grade == senior operator
     raw: redlines_open
     arduous: complexity_band == heavy
     """,
     cues="lacks a style sheet => style_sheet_attached=false; was never approved in proof => "
          "lawyer_proof_approved=false; has no page stamping => bates_stamped=false",
     links="job > lawyer: credits / credited by; job > operator: assigns / assigned by",
     actions="format = lay out; proof = check; stamp = number pages; bind = assemble",
     sources="job ticket; lawyer email; proof copy notes; print room log; shift handover note; "
             "turnaround report",
     inert="""
     binding_comb_colour | cat | black comb; white comb
     printer_nickname | cat | Big Bertha; Little Tom; Old Faithful
     shift_snack | cat | pretzels; fruit; muffins
     paper_supplier | cat | supplier A; supplier B
     room_thermostat | cat | cool setting; warm setting
     """,
     affix="unstamped => bates_stamped; unapproved => lawyer_proof_approved"),

dict(slot="lg-09", slug="fee-waivers", sector="legal_practice_admin",
     sub="small-claims clerk office reviewing filing fee waiver applications",
     org="Penhallow Municipal Small Claims Office", desk="clerk's counter",
     setting="A municipal small-claims office lets people file claims at zero fee when they meet the waiver "
             "rules. Clerks at the counter check each application, set the fee outcome and decide when a "
             "judge must review it.",
     decider="court clerk",
     roles="counter clerk; supervising clerk; magistrate; self-help center aide; cashier; records clerk",
     docs="fee waiver application; income statement; benefit letter; claim form; clerk worksheet; order on waiver",
     scope=("filing window", "Window 1; Window 2; Night Court Window; Online Filing"),
     money="dollars",
     ents=[
        dict(key="application", singular="waiver application", plural="waiver applications", id="WA",
             aka="fee application",
             attrs="""
             monthly_income | money | 0.00..9000.00 | aka=income per month
             household_size | int | 1..10 people | aka=people in the home
             claim_amount | money | 50.00..12500.00 | aka=amount claimed
             filing_fee | money | 30.00..300.00 | aka=fee owed
             days_since_filed | int | 0..30 days | aka=age of the application
             income_source | cat | wages; benefits; pension; self-employment; mixed
             form_version | ord | 2019 form; 2022 form; 2025 form | aka=application form edition
             benefit_letter_attached | state | bad=0 | aka=benefit letter on file | grp=proof
             signature_present | state | bad=0 | aka=signed by applicant
             earlier_waiver_this_year | event | bad=0 | aka=waiver granted earlier this year
             judge_review_ordered | event | bad=1 | aka=sent for judicial review
             filed_on | date
             hearing_on | date
             application_tags | tag | interpreter; self-help aide; online; walk-in; amended
             """),
        dict(key="applicant", singular="applicant", plural="applicants", id="AN", names="person", role="person",
             attrs="""
             claims_filed_this_year | int | 0..12 items | aka=claims filed this year
             address_confirmed | event | bad=0 | aka=address checked
             """),
        dict(key="clerk", singular="clerk", plural="clerks", id="CK", names="person", role="person",
             attrs="""
             applications_today | int | 0..60 items | aka=applications handled today
             clerk_grade | ord | clerk I; clerk II; senior clerk | aka=clerk grade
             """),
     ],
     outcomes=["grant full waiver; grant partial waiver; send to magistrate; return for signature*; "
               "charge full fee*",
               "file claim today; file after payment*; file after review"],
     levels=["clerk I; clerk II; senior clerk", "low; medium; high"],
     words="""
     modest: monthly_income < 1500
     comfortable: monthly_income >= 5000
     populous: household_size >= 5
     substantial: claim_amount >= 5000
     petty: claim_amount < 300
     pricey: filing_fee >= 150
     stale: days_since_filed >= 14
     documented: benefit_letter_attached
     attested: signature_present
     repeat: earlier_waiver_this_year
     litigious: claims_filed_this_year >= 4
     busy: applications_today >= 40
     current: form_version == 2025 form
     scrutinized: judge_review_ordered
     """,
     cues="lacks a benefit letter => benefit_letter_attached=false; has no signature => "
          "signature_present=false; was never checked at the listed address => address_confirmed=false",
     links="application > applicant: names / named by; application > clerk: assigns / assigned by",
     actions="grant = allow; refer = send up; stamp = mark filed; collect = take payment",
     sources="clerk worksheet; benefit agency letter; applicant statement; cashier log; magistrate note; "
             "online portal",
     inert="""
     counter_bell | cat | brass bell; silver bell
     queue_ticket_colour | cat | pink ticket; blue ticket
     lobby_poster | cat | recycling; history; parks
     pen_on_chain | cat | short chain; long chain
     floor_tile | cat | checkered; plain
     """,
     affix="unsigned => signature_present; undocumented => benefit_letter_attached"),

dict(slot="lg-10", slug="time-entry-review", sector="legal_practice_admin",
     sub="pre-bill time entry review and write-down approvals at a law firm",
     org="Corriveau Lambrecht LLP", desk="billing review desk",
     setting="Before invoices go out, a law firm reviews each lawyer's time entries against client billing "
             "guidelines. The billing review desk decides whether an entry is billed, reduced or sent to the "
             "relationship partner.",
     decider="administrative services manager",
     roles="billing specialist; relationship partner; timekeeper; collections clerk; e-billing analyst; "
           "finance director",
     docs="pre-bill; client billing guideline; write-down form; invoice; e-billing rejection notice; "
          "rate approval letter",
     scope=("client group", "Banking Clients; Insurance Clients; Tech Clients; Public Clients"),
     money="dollars",
     ents=[
        dict(key="entry", singular="time entry", plural="time entries", id="TE", aka="billing entry",
             attrs="""
             hours_billed | dec1 | 0.1..14.0 hours | aka=hours logged
             hourly_rate | money | 120.00..1500.00 | aka=rate charged
             days_since_work | int | 0..120 days | aka=age of the entry
             block_tasks | int | 1..8 items | aka=tasks in one entry
             task_code | cat | research; drafting; court time; travel; meeting; review
             timekeeper_class | cat | partner; associate; paralegal; clerk
             guideline_tier | ord | relaxed; standard; strict | aka=guideline strictness
             description_complete | state | bad=0 | aka=narrative complete | grp=narrative
             rate_approved | state | bad=0 | aka=rate cleared by client
             budget_exceeded | state | bad=1 | aka=matter over budget
             partner_reviewed | event | bad=0 | aka=partner looked at it
             edited_after_cutoff | event | bad=1 | aka=entry changed after the cutoff
             worked_on | date
             billed_on | date
             entry_tags | tag | block billed; vague narrative; travel time; internal conference; first-year time
             """),
        dict(key="client", singular="client", plural="clients", id="CN",
             names="org: Holdings, Bank, Insurance, Group",
             attrs="""
             write_down_rate | dec1 | 0.0..40.0 percent | aka=usual write-down share
             days_to_pay | int | 10..150 days | aka=average payment time
             """),
        dict(key="timekeeper", singular="timekeeper", plural="timekeepers", id="TK", names="person", role="person",
             attrs="""
             utilization | dec1 | 30.0..120.0 percent | aka=billable share
             late_entries_this_month | int | 0..30 items | aka=late entries
             billing_course_finished | event | bad=0 | aka=billing training done
             """),
     ],
     outcomes=["bill as entered; reduce hours; reduce rate; send to relationship partner; write off entry*; "
               "hold entry*",
               "bill this cycle; bill next cycle*; bill after client approval"],
     levels=["relaxed; standard; strict", "low; moderate; high"],
     words="""
     lengthy: hours_billed >= 8
     tiny: hours_billed < 0.5
     premium: hourly_rate >= 900
     stale: days_since_work >= 60
     blocky: block_tasks >= 3
     sanctioned: rate_approved
     thorough: description_complete
     extravagant: budget_exceeded
     vetted: partner_reviewed
     rigid: guideline_tier == strict
     sluggish: days_to_pay >= 90
     tardy: late_entries_this_month >= 10
     busy: utilization >= 100
     tampered: edited_after_cutoff
     itinerant: task_code == travel
     """,
     cues="lacks a complete narrative => description_complete=false; has no client rate approval => "
          "rate_approved=false; was never reviewed by the partner => partner_reviewed=false",
     links="entry > client: bills / billed by; entry > timekeeper: credits / credited by",
     actions="bill = invoice; reduce = trim; transfer = move entry; approve = sign off",
     sources="pre-bill; e-billing portal; partner email; timekeeper note; client guideline; collections report",
     inert="""
     letterhead_font | cat | font A; font B
     quiet_room | cat | north room; south room
     coffee_mug_logo | cat | firm crest; plain mug
     carpet_pattern | cat | dotted; striped
     reading_glasses | cat | round frames; square frames
     """,
     affix="unreviewed => partner_reviewed; unapproved => rate_approved"),
]
