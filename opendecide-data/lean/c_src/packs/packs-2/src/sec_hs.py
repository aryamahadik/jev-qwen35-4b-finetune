"""packs-2 sector hs: hospitality (Claude-written pack sources; invented venues and entities)."""

PACKS = [
dict(slot="hs-01", slug="rec-center-rentals", sector="hospitality",
     sub="recreation center program registration and facility rentals",
     org="Glenhaven Parks and Recreation Department", desk="recreation front desk",
     setting="A town recreation center registers residents for classes and rents out its gym, pool and party "
             "rooms. The front desk applies the center's residency, capacity, deposit and booking rules to each "
             "booking.",
     decider="recreation supervisor",
     roles="front desk attendant; aquatics coordinator; facility manager; program instructor; custodial lead; "
           "cashier",
     docs="booking form; rental agreement; facility calendar; insurance certificate; deposit receipt; "
          "incident log",
     scope=("facility", "Main Gym; Leisure Pool; Party Room; Outdoor Pavilion; Dance Studio"),
     money="dollars",
     ents=[
        dict(key="booking", singular="facility booking", plural="facility bookings", id="FB", aka="rental",
             attrs="""
             guests_expected | int | 5..300 guests | aka=headcount
             hours_booked | dec1 | 1.0..12.0 hours | aka=rental length
             rental_fee | money | 40.00..2400.00 | aka=rental charge
             days_before_event | int | 0..180 days | aka=lead time
             event_kind | cat | birthday party; sports league; community meeting; fitness class; wedding reception; fundraiser
             renter_type | cat | resident; out-of-town; local nonprofit; school group
             noise_level | ord | quiet; moderate; loud | aka=expected noise
             deposit_received | event | bad=0 | aka=deposit taken | grp=payment
             insurance_certificate_filed | state | bad=0 | aka=liability certificate on file
             lifeguard_needed | state | bad=1 | aka=pool staff needed
             food_served | state | bad=1 | aka=catering at the event
             walkthrough_done | event | bad=0 | aka=site visit completed
             booked_on | date
             event_on | date
             booking_tags | tag | holiday; repeat renter; youth group; alcohol service; after hours; decorations
             """),
        dict(key="renter", singular="renter", plural="renters", id="RT", names="person", role="person",
             attrs="""
             past_bookings | int | 0..40 items | aka=earlier rentals
             damage_charges_before | money | 0.00..1500.00 | aka=earlier damage bills
             """),
        dict(key="space", singular="rental space", plural="rental spaces", id="RS",
             names=["Space Maple Hall", "Space Cedar Court", "Space Lakeside Deck", "Space Studio B", "Space Pool Lanes", "Space Hilltop Room", "Space Garden Patio", "Space Gym Court 2"],
             attrs="""
             capacity | int | 20..400 guests | aka=room capacity
             cleaning_hours | dec1 | 0.5..6.0 hours | aka=cleanup time
             """),
     ],
     outcomes=["confirm booking; confirm with extra staff fee*; send to facility manager; hold for insurance*; "
               "offer another room; cancel booking*",
               "resident rate; out-of-town rate*; nonprofit rate"],
     levels=["quiet; moderate; loud", "low; medium; high"],
     words="""
     crowded: guests_expected >= 150
     intimate: guests_expected < 20
     lengthy: hours_booked >= 6
     pricey: rental_fee >= 1000
     rushed: days_before_event <= 7
     provident: days_before_event >= 90
     secured: deposit_received
     insured: insurance_certificate_filed
     inspected: walkthrough_done
     loyal: past_bookings >= 5
     rough: damage_charges_before >= 200
     roomy: capacity >= 200
     festive: event_kind == wedding reception
     rowdy: noise_level == loud
     aquatic: lifeguard_needed
     """,
     cues="lacks a liability certificate => insurance_certificate_filed=false; has no deposit taken => "
          "deposit_received=false; never completed the site visit => walkthrough_done=false",
     links="booking > renter: names / named by; booking > space: reserves / reserved by",
     actions="book = reserve; refund = repay; reassign = move room; invoice = bill",
     sources="facility calendar; renter email; front desk note; insurance agent fax; cashier log; "
             "custodial report",
     inert="""
     lobby_trophy_case | cat | swim medals; league cups
     whistle_colour | cat | orange whistle; silver whistle
     vending_snack | cat | granola bar; pretzels
     bulletin_flyer | cat | yoga flyer; chess flyer
     towel_stack_side | cat | left shelf; right shelf
     """,
     affix="uninsured => insurance_certificate_filed; uninspected => walkthrough_done"),

dict(slot="hs-02", slug="concierge-desk", sector="hospitality",
     sub="hotel concierge desk booking guest outings and complimentary amenities",
     org="The Halloran Grand Hotel", desk="concierge desk",
     setting="A city hotel's concierge desk books show tickets, cars and restaurant tables for guests and decides "
             "which guests receive complimentary amenities. It applies the hotel's booking, charge and amenity "
             "rules.",
     decider="concierge",
     roles="head concierge; front office manager; guest relations agent; bell captain; loyalty desk agent; "
           "night auditor",
     docs="guest booking card; amenity log; vendor voucher; folio charge slip; loyalty profile; "
          "guest feedback card",
     scope=("tower", "North Tower; South Tower; Garden Wing; Club Floors"),
     money="dollars",
     ents=[
        dict(key="booking", singular="guest booking", plural="guest bookings", id="GB", aka="concierge booking",
             attrs="""
             party_size | int | 1..12 people | aka=number in the party
             booking_cost | money | 15.00..3000.00 | aka=cost of the booking
             hours_until_outing | int | 1..168 hours | aka=time until the outing
             nights_in_stay | int | 1..21 nights | aka=stay length
             booking_kind | cat | theatre tickets; car service; restaurant table; museum tour; spa visit; harbour cruise
             occasion | cat | birthday; anniversary; business; honeymoon; leisure
             guest_tier | ord | member; silver; gold; platinum | aka=loyalty tier
             card_on_file | state | bad=0 | aka=payment card stored | grp=payment
             vendor_confirmed | event | bad=0 | aka=vendor accepted the booking
             complaint_logged | event | bad=1 | aka=guest complained earlier this stay
             repeat_guest | state | bad=0 | aka=stayed here before
             booked_on | date
             outing_on | date
             booking_tags | tag | surprise; accessibility; late night; children; rain backup; corporate account
             """),
        dict(key="guest", singular="guest", plural="guests", id="GT", names="person", role="person",
             attrs="""
             spend_this_stay | money | 0.00..20000.00 | aka=folio total
             stays_this_year | int | 0..30 items | aka=stays this year
             """),
        dict(key="vendor", singular="outside vendor", plural="outside vendors", id="XV",
             names="org: Car Service, Theatre Box Office, Bistro, Cruises",
             attrs="""
             commission_rate | dec1 | 0.0..20.0 percent | aka=hotel commission
             partner_agreement | state | bad=0 | aka=preferred vendor deal in place
             """),
     ],
     outcomes=["book and charge folio; book and pay at venue; offer complimentary amenity; "
               "send to front office manager; return booking to guest*; charge cancellation fee*",
               "fruit plate; welcome wine; late checkout; room upgrade; small note only*"],
     levels=["member; silver; gold; platinum", "low; medium; high"],
     words="""
     populous: party_size >= 6
     lavish: booking_cost >= 800
     last-minute: hours_until_outing <= 3
     extended: nights_in_stay >= 7
     secured: card_on_file
     assured: vendor_confirmed
     aggrieved: complaint_logged
     habitual: repeat_guest
     extravagant: spend_this_stay >= 5000
     frequent: stays_this_year >= 6
     favored: partner_agreement
     romantic: occasion in {anniversary, honeymoon}
     elite: guest_tier == platinum
     theatrical: booking_kind == theatre tickets
     nautical: booking_kind == harbour cruise
     """,
     cues="has no payment card stored => card_on_file=false; was never accepted by the vendor => "
          "vendor_confirmed=false; lacks a preferred vendor deal => partner_agreement=false",
     links="booking > guest: serves / served by; booking > vendor: books / booked by",
     actions="book = reserve; comp = gift; charge = post to folio; arrange = organise",
     sources="concierge log; guest phone call; vendor email; folio system; loyalty profile; night audit report",
     inert="""
     lobby_piano_tune | cat | waltz; jazz standard
     doorman_glove | cat | white gloves; grey gloves
     elevator_music | cat | strings; bossa nova
     brochure_rack | cat | rack one; rack two
     lobby_scent | cat | cedar; citrus
     """,
     affix="unsecured => card_on_file; unconfirmed => vendor_confirmed"),

dict(slot="hs-03", slug="attraction-groups", sector="hospitality",
     sub="group sales and season pass desk at a family attraction park",
     org="Starling Point Adventure Park", desk="group sales desk",
     setting="A family attraction park sells group tickets and season passes. The group sales desk applies the "
             "park's group pricing, chaperone and pass exception rules to each booking.",
     decider="recreation manager",
     roles="group sales agent; guest services lead; ticketing supervisor; school outreach coordinator; "
           "season pass clerk; operations manager",
     docs="group order; chaperone list; pass exception form; ticket invoice; ride closure notice; "
          "school field trip agreement",
     scope=("gate", "Main Gate; River Gate; Coaster Gate; Picnic Gate"),
     money="dollars",
     ents=[
        dict(key="order", singular="group order", plural="group orders", id="GQ", aka="group booking",
             attrs="""
             group_size | int | 10..400 people | aka=group headcount
             chaperones | int | 0..40 people | aka=adult chaperones
             ticket_price | money | 18.00..95.00 | aka=price per ticket
             days_before_visit | int | 0..120 days | aka=lead time
             group_type | cat | school; scout troop; company outing; church group; sports team; camp
             meal_package | cat | snack pack; lunch voucher; full meal; picnic area only
             group_tier | ord | small; medium; large; mega | aka=group size class
             deposit_paid | event | bad=0 | aka=group deposit paid | grp=payment
             waiver_forms_received | event | bad=0 | aka=release forms returned
             rain_date_chosen | state | bad=0 | aka=backup date set
             tax_exempt | state | bad=0 | aka=sales tax exemption on file
             ride_closure_affects | state | bad=1 | aka=a closed ride affects the visit
             ordered_on | date
             visit_on | date
             order_tags | tag | early entry; birthday group; overnight; fireworks night; accessible seating
             """),
        dict(key="leader", singular="group leader", plural="group leaders", id="GW", names="person", role="person",
             attrs="""
             past_visits | int | 0..20 visits | aka=earlier group visits
             phone_checked | event | bad=0 | aka=leader phone number confirmed
             """),
        dict(key="pass", singular="season pass", plural="season passes", id="SP",
             names=["Pass Comet", "Pass Meteor", "Pass Orbit", "Pass Rocket", "Pass Nebula", "Pass Quasar", "Pass Zenith", "Pass Aurora"],
             attrs="""
             visits_used | int | 0..120 visits | aka=pass visits
             pass_price | money | 80.00..450.00 | aka=pass cost
             """),
     ],
     outcomes=["confirm group rate; confirm standard rate*; send to operations manager; hold for deposit*; "
               "move to rain date",
               "extend pass; refund part of pass; keep pass terms*"],
     levels=["small; medium; large; mega", "low; medium; high"],
     words="""
     huge: group_size >= 200
     modest: group_size < 20
     supervised: chaperones >= 10
     pricey: ticket_price >= 70
     provident: days_before_visit >= 60
     rushed: days_before_visit <= 3
     committed: deposit_paid
     consented: waiver_forms_received
     privileged: tax_exempt
     loyal: past_visits >= 3
     devoted: visits_used >= 50
     scholastic: group_type == school
     hungry: meal_package == full meal
     disrupted: ride_closure_affects
     """,
     cues="lacks returned release forms => waiver_forms_received=false; has no deposit paid => "
          "deposit_paid=false; holds no sales tax exemption => tax_exempt=false",
     links="order > leader: names / named by; order > pass: cites / cited by",
     actions="confirm = lock in; reprice = adjust rate; extend = lengthen; refund = repay",
     sources="group order; leader email; ticketing system; operations bulletin; pass clerk note; school letter",
     inert="""
     mascot_on_duty | cat | otter suit; fox suit
     wristband_colour | cat | lime band; violet band
     picnic_bench_row | cat | row K; row T
     souvenir_of_month | cat | plush toy; keychain
     fountain_show | cat | morning show; evening show
     """,
     affix="unpaid => deposit_paid; unconsented => waiver_forms_received"),

dict(slot="hs-04", slug="spa-bookings", sector="hospitality",
     sub="resort spa appointment desk with cancellation and package rules",
     org="Solenne Springs Resort Spa", desk="spa reception",
     setting="A resort spa books treatments for hotel guests and day visitors. Spa reception applies the "
             "booking, cancellation, package and health-form rules to every appointment.",
     decider="spa manager",
     roles="spa receptionist; lead therapist; retail associate; hotel front desk agent; wellness director; "
           "attendant",
     docs="treatment booking; health intake form; package voucher; cancellation notice; therapist rota; "
          "retail receipt",
     scope=("treatment area", "Hydrotherapy Suite; Massage Rooms; Facial Studio; Couples Suite"),
     money="euros",
     ents=[
        dict(key="appointment", singular="spa appointment", plural="spa appointments", id="SA",
             aka="treatment booking",
             attrs="""
             treatment_minutes | int | 30..180 minutes | aka=treatment length
             treatment_price | money | 45.00..600.00 | aka=price
             hours_notice_of_change | int | 0..96 hours | aka=notice of change
             guests_in_booking | int | 1..4 people | aka=people booked
             treatment_kind | cat | massage; facial; body wrap; hydrotherapy; manicure; couples ritual
             guest_category | cat | hotel guest; day visitor; member; package holder
             intensity_choice | ord | gentle; medium; firm; deep | aka=pressure level
             health_form_signed | event | bad=0 | aka=health intake signed | grp=intake
             pregnancy_noted | state | bad=1 | aka=guest reported pregnancy
             package_voucher_used | event | bad=0 | aka=package voucher applied
             arrived_late | event | bad=1 | aka=came after the start time
             room_charge_allowed | state | bad=0 | aka=can charge to the room
             booked_on | date
             treatment_on | date
             appointment_tags | tag | gift card; birthday; wedding party; first visit; therapist request
             """),
        dict(key="guest", singular="spa guest", plural="spa guests", id="SG", names="person", role="person",
             attrs="""
             visits_this_year | int | 0..40 visits | aka=spa visits this year
             retail_spend | money | 0.00..900.00 | aka=product purchases
             """),
        dict(key="therapist", singular="therapist", plural="therapists", id="TH", names="person", role="person",
             attrs="""
             bookings_today | int | 0..10 items | aka=appointments today
             specialist_grade | ord | junior; senior; master | aka=therapist grade
             """),
     ],
     outcomes=["keep appointment; shorten treatment*; move to later slot; send to wellness director; "
               "charge cancellation fee*; cancel appointment*",
               "charge to room; charge card; redeem voucher; pay deposit first*"],
     levels=["gentle; medium; firm; deep", "junior; senior; master"],
     words="""
     lengthy: treatment_minutes >= 120
     quick: treatment_minutes <= 45
     luxurious: treatment_price >= 300
     abrupt: hours_notice_of_change < 24
     shared: guests_in_booking >= 2
     cleared: health_form_signed
     expecting: pregnancy_noted
     tardy: arrived_late
     trusted: room_charge_allowed
     regular: visits_this_year >= 10
     generous: retail_spend >= 200
     busy: bookings_today >= 7
     virtuoso: specialist_grade == master
     vigorous: intensity_choice == deep
     transient: guest_category == day visitor
     spoiled: package_voucher_used
     """,
     cues="lacks a signed health intake => health_form_signed=false; has no room charge permission => "
          "room_charge_allowed=false; never applied the package voucher => package_voucher_used=false",
     links="appointment > guest: books / booked by; appointment > therapist: assigns / assigned by",
     actions="book = reserve; reschedule = move; redeem = apply voucher; upsell = offer extra",
     sources="booking system; guest phone call; front desk message; therapist rota; health intake form; "
             "retail till",
     inert="""
     robe_colour | cat | white robe; sage robe
     candle_scent | cat | lavender; eucalyptus
     slipper_size_bin | cat | bin one; bin two
     relaxation_music | cat | ocean sounds; flute
     tea_offered | cat | mint tea; ginger tea
     """,
     affix="unsigned => health_form_signed; unredeemed => package_voucher_used"),

dict(slot="hs-05", slug="coach-tours", sector="hospitality",
     sub="coach tour reservation desk handling seats, changes and fees",
     org="Larchmont Coach Tours", desk="tour reservations desk",
     setting="A coach tour operator sells seats on day trips and multi-day tours. The reservations desk applies "
             "fare, change-fee, seat and minimum-booking rules to each reservation.",
     decider="reservation agent",
     roles="reservations clerk; tour manager; driver dispatcher; group sales agent; accounts clerk; "
           "customer care lead",
     docs="reservation record; tour manifest; change notice; fare sheet; seating chart; tour conditions",
     scope=("departure point", "City Terminal; Airport Stop; Harbour Car Park; North Station"),
     money="pounds sterling",
     ents=[
        dict(key="reservation", singular="tour reservation", plural="tour reservations", id="TR",
             aka="seat booking",
             attrs="""
             seats_booked | int | 1..12 seats | aka=seats reserved
             fare_total | money | 25.00..4200.00 | aka=total fare
             days_to_departure | int | 0..180 days | aka=time to departure
             changes_made | int | 0..4 entries | aka=changes so far
             tour_length | cat | half day; full day; weekend; five day; ten day
             booking_channel | cat | phone; website; travel agent; walk-in
             seat_class | ord | standard seat; extra legroom; front row | aka=seat grade
             balance_paid | event | bad=0 | aka=final balance received | grp=payment
             insurance_bought | event | bad=0 | aka=travel cover added
             mobility_assist | state | bad=1 | aka=needs boarding help
             passport_details_given | state | bad=0 | aka=travel document details on file
             booked_on | date
             departs_on | date
             reservation_tags | tag | single traveller; senior; school party; dietary note; window seat
             """),
        dict(key="traveller", singular="lead traveller", plural="lead travellers", id="KT", names="person",
             role="person",
             attrs="""
             tours_taken | int | 0..30 trips | aka=past tours
             loyalty_points | int | 0..5000 points | aka=points balance
             """),
        dict(key="tour", singular="tour departure", plural="tour departures", id="TD",
             names=["Tour Highland Lochs", "Tour Coastal Castles", "Tour Lakeland Loop", "Tour Valley Vineyards", "Tour Market Towns", "Tour Northern Lights", "Tour Garden Trail", "Tour Cathedral Cities"],
             attrs="""
             seats_left | int | 0..53 seats | aka=open seats
             minimum_to_run | int | 10..30 seats | aka=minimum bookings
             guaranteed_departure | state | bad=0 | aka=departure guaranteed to run
             """),
     ],
     outcomes=["confirm seats; confirm with change fee*; move to another departure; send to tour manager; "
               "cancel and refund; cancel with forfeit*",
               "standard seat; extra legroom; front row; waitlist only*"],
     levels=["standard seat; extra legroom; front row", "low; medium; high"],
     words="""
     populous: seats_booked >= 4
     hefty: fare_total >= 1500
     imminent: days_to_departure <= 3
     provident: days_to_departure >= 90
     fickle: changes_made >= 2
     solvent: balance_paid
     assured: insurance_bought
     papered: passport_details_given
     loyal: tours_taken >= 5
     rich: loyalty_points >= 2000
     packed: seats_left < 1
     epic: tour_length == ten day
     digital: booking_channel == website
     frail: mobility_assist
     privileged: seat_class == front row
     """,
     cues="has no final balance received => balance_paid=false; lacks travel cover => insurance_bought=false; "
          "never gave travel document details => passport_details_given=false",
     links="reservation > traveller: names / named by; reservation > tour: reserves / reserved by",
     actions="reserve = hold seats; rebook = move date; refund = repay; manifest = list passengers",
     sources="reservation record; traveller email; agent fax; tour manager note; accounts ledger; phone message",
     inert="""
     coach_livery | cat | green livery; maroon livery
     driver_cap | cat | flat cap; peaked cap
     onboard_film | cat | comedy film; nature film
     rest_stop_cafe | cat | cafe one; cafe two
     luggage_strap_colour | cat | yellow tag; red tag
     """,
     affix="uninsured => insurance_bought; unpaid => balance_paid"),

dict(slot="hs-06", slug="restaurant-reservations", sector="hospitality",
     sub="restaurant reservation book with deposits, table assignment and no-show rules",
     org="Brasserie Marchetti", desk="host stand",
     setting="A busy restaurant takes reservations by phone and online. The host stand applies table, deposit, "
             "large-party and missed-reservation rules to every booking.",
     decider="restaurant host",
     roles="head host; floor manager; server captain; events coordinator; chef de cuisine; reservations agent",
     docs="reservation book; deposit receipt; floor plan; large-party agreement; allergy card; shift log",
     scope=("dining area", "Main Room; Terrace; Private Room; Bar Counter"),
     money="euros",
     ents=[
        dict(key="reservation", singular="reservation", plural="reservations", id="RZ", aka="table booking",
             attrs="""
             covers | int | 1..24 covers | aka=party size
             deposit_amount | money | 0.00..500.00 | aka=deposit held
             minutes_late | int | 0..60 minutes | aka=minutes after the booked time
             days_ahead_booked | int | 0..90 days | aka=booking lead time
             seating_time | cat | early seating; peak seating; late seating
             occasion | cat | birthday; business dinner; date night; family meal; celebration
             spend_band | ord | casual; standard; tasting menu | aka=menu level
             deposit_taken | event | bad=0 | aka=deposit charged | grp=deposit
             allergy_flagged | state | bad=1 | aka=serious allergy noted
             confirmed_by_text | event | bad=0 | aka=guest confirmed by message
             accessible_table_needed | state | bad=1 | aka=step-free table needed
             high_chair_needed | state | bad=1 | aka=child seat needed
             booked_on | date
             dining_on | date
             reservation_tags | tag | regular guest; press; proposal; wine pairing; window table
             """),
        dict(key="guest", singular="guest", plural="guests", id="GU", names="person", role="person",
             attrs="""
             past_missed_bookings | int | 0..5 entries | aka=missed bookings before
             visits_this_year | int | 0..60 visits | aka=visits this year
             """),
        dict(key="table", singular="table", plural="tables", id="TB",
             names=["Table 1", "Table 4", "Table 7", "Table 12", "Table 15", "Table 21", "Table 24", "Table 30"],
             attrs="""
             seats_at_table | int | 2..14 seats | aka=table seats
             turn_minutes | int | 60..180 minutes | aka=expected table time
             """),
     ],
     outcomes=["seat as booked; seat at bar*; hold table ten minutes; send to floor manager; "
               "release table*; charge deposit*",
               "standard deposit; large party deposit*; zero deposit"],
     levels=["casual; standard; tasting menu", "low; medium; high"],
     words="""
     populous: covers >= 8
     intimate: covers <= 2
     hefty: deposit_amount >= 200
     tardy: minutes_late >= 15
     punctual: minutes_late < 5
     provident: days_ahead_booked >= 30
     guaranteed: deposit_taken
     assured: confirmed_by_text
     allergic: allergy_flagged
     flaky: past_missed_bookings >= 2
     habitual: visits_this_year >= 12
     roomy: seats_at_table >= 8
     bustling: seating_time == peak seating
     gourmet: spend_band == tasting menu
     romantic: occasion == date night
     """,
     cues="has no deposit charged => deposit_taken=false; never confirmed by message => "
          "confirmed_by_text=false; lacks a serious allergy note => allergy_flagged=false",
     links="reservation > guest: names / named by; reservation > table: holds / held by",
     actions="seat = place; hold = keep table; release = free up; charge = take deposit",
     sources="reservation book; guest text message; floor plan; manager note; deposit system; phone message",
     inert="""
     napkin_fold | cat | fan fold; pocket fold
     candle_dish | cat | glass; brass
     bread_basket | cat | sourdough; rye
     bill_folder_material | cat | leather; linen
     background_playlist | cat | jazz; bossa
     """,
     affix="unconfirmed => confirmed_by_text; unguaranteed => deposit_taken"),

dict(slot="hs-07", slug="group-travel", sector="hospitality",
     sub="travel agency group booking desk with deposit and name-change rules",
     org="Pemberton Wayfarer Travel", desk="group travel desk",
     setting="A travel agency books trips for clubs, choirs and alumni groups. The group desk applies deposit "
             "schedules, name-change fees and minimum group rules from each supplier contract.",
     decider="travel agent",
     roles="group travel consultant; supplier relations manager; accounts clerk; tour escort; "
           "agency owner; documents clerk",
     docs="group contract; deposit schedule; rooming list; name change form; final invoice; supplier terms",
     scope=("destination region", "Mediterranean; Alpine; Nordic; Atlantic Islands; Central Europe"),
     money="euros",
     ents=[
        dict(key="group", singular="group booking", plural="group bookings", id="GK", aka="group file",
             attrs="""
             travellers | int | 8..120 people | aka=group size
             deposit_due | money | 200.00..60000.00 | aka=deposit owed
             days_to_travel | int | 0..365 days | aka=time to departure
             name_changes | int | 0..15 entries | aka=names swapped
             trip_style | cat | cruise; rail tour; city break; pilgrimage; walking holiday
             supplier_type | cat | hotel chain; cruise line; rail operator; tour wholesaler
             contract_level | ord | basic; flexible; premium flex | aka=contract flexibility
             first_deposit_paid | event | bad=0 | aka=first deposit received | grp=deposits
             rooming_roster_sent | event | bad=0 | aka=room roster delivered
             escort_assigned | state | bad=0 | aka=tour escort in place
             visa_support_needed | state | bad=1 | aka=visa letters needed
             minimum_met | state | bad=0 | aka=group minimum reached
             contracted_on | date
             departs_on | date
             group_tags | tag | choir; alumni; sports club; faith group; seniors; students
             """),
        dict(key="organizer", singular="group organizer", plural="group organizers", id="GR", names="person",
             role="person",
             attrs="""
             trips_organized | int | 0..25 trips | aka=past trips run
             """),
        dict(key="supplier", singular="supplier", plural="suppliers", id="SU",
             names="org: Hotels, Cruises, Rail, Tours",
             attrs="""
             attrition_allowance | dec1 | 0.0..25.0 percent | aka=allowed drop in numbers
             release_days | int | 7..120 days | aka=days before space goes back to the supplier
             """),
     ],
     outcomes=["confirm group space; confirm with fee*; reduce allocation; send to agency owner; "
               "release space*; cancel group*",
               "accept name change; accept with fee*; refer to supplier"],
     levels=["basic; flexible; premium flex", "low; medium; high"],
     words="""
     populous: travellers >= 50
     modest: travellers < 15
     hefty: deposit_due >= 20000
     imminent: days_to_travel <= 30
     provident: days_to_travel >= 240
     fluid: name_changes >= 5
     funded: first_deposit_paid
     dispatched: rooming_roster_sent
     chaperoned: escort_assigned
     viable: minimum_met
     seasoned: trips_organized >= 5
     lenient: attrition_allowance >= 10
     maritime: trip_style == cruise
     foreign: visa_support_needed
     """,
     cues="has no first deposit received => first_deposit_paid=false; never sent the room list => "
          "rooming_roster_sent=false; lacks a tour escort => escort_assigned=false",
     links="group > organizer: names / named by; group > supplier: contracts / contracted by",
     actions="reserve = block space; rename = swap traveller; invoice = bill; release = hand back",
     sources="group contract; supplier email; organizer letter; accounts ledger; rooming list; escort report",
     inert="""
     brochure_paper | cat | glossy; matte
     agency_window_display | cat | beach scene; mountain scene
     office_globe | cat | antique globe; desk globe
     water_bottle_logo | cat | blue logo; green logo
     wall_clock_city | cat | Lisbon clock; Oslo clock
     """,
     affix="unsent => rooming_roster_sent; unescorted => escort_assigned"),

dict(slot="hs-08", slug="hotel-walks", sector="hospitality",
     sub="front desk room assignment, overbooking walks and upgrades",
     org="Kestrel Bay Hotel and Suites", desk="front desk",
     setting="When the hotel is overbooked, the front desk decides which arriving guests are relocated to a "
             "partner hotel and who receives an upgrade. It applies the hotel's walk, upgrade and compensation "
             "rules at check-in.",
     decider="hotel desk clerk",
     roles="front office manager; night manager; reservations agent; loyalty coordinator; bell desk; "
           "revenue manager",
     docs="arrivals list; walk letter; upgrade log; partner hotel voucher; rate confirmation; shift report",
     scope=("room type", "Standard King; Double Queen; Junior Suite; Accessible King"),
     money="dollars",
     ents=[
        dict(key="arrival", singular="arrival", plural="arrivals", id="AR", aka="incoming reservation",
             attrs="""
             nights_booked | int | 1..14 nights | aka=nights of stay
             nightly_rate | money | 89.00..899.00 | aka=room rate
             eta_hour | int | 0..23 hours | aka=arrival hour
             rooms_in_booking | int | 1..4 rooms | aka=rooms held
             rate_type | cat | corporate rate; package rate; advance purchase; group rate; flexible rate
             booking_source | cat | hotel website; phone; online agency; corporate travel desk
             loyalty_level | ord | basic; silver; gold; diamond | aka=loyalty status
             guaranteed_by_card | state | bad=0 | aka=card guarantee on file | grp=guarantee
             prepaid_nonrefundable | state | bad=0 | aka=paid in advance
             walked_before | event | bad=1 | aka=relocated on an earlier stay
             accessible_room_needed | state | bad=1 | aka=step-free room needed
             early_checkin_given | event | bad=0 | aka=early arrival granted
             booked_on | date
             arrives_on | date
             arrival_tags | tag | late arrival; honeymoon; long stay; crew; meeting attendee
             """),
        dict(key="guest", singular="guest", plural="guests", id="GS", names="person", role="person",
             attrs="""
             stays_last_year | int | 0..60 nights | aka=nights stayed last year
             """),
        dict(key="partner", singular="partner hotel", plural="partner hotels", id="PH",
             names="org: Inn, Suites, Lodge, Hotel",
             attrs="""
             distance_km | dec1 | 0.2..15.0 kilometres | aka=distance from the hotel
             partner_rate | money | 70.00..600.00 | aka=partner room rate
             """),
     ],
     outcomes=["assign booked room type; upgrade free; upgrade for a fee; walk to partner hotel*; "
               "send to front office manager",
               "pay first night elsewhere; pay first night and transport; give points only*"],
     levels=["basic; silver; gold; diamond", "low; medium; high"],
     words="""
     extended: nights_booked >= 5
     premium: nightly_rate >= 400
     budget: nightly_rate < 120
     nocturnal: eta_hour >= 22
     secured: guaranteed_by_card
     settled: prepaid_nonrefundable
     displaced: walked_before
     frequent: stays_last_year >= 25
     nearby: distance_km < 1
     remote: distance_km >= 8
     elite: loyalty_level == diamond
     businesslike: rate_type == corporate rate
     bulk: rooms_in_booking >= 2
     pampered: early_checkin_given
     assisted: accessible_room_needed
     """,
     cues="holds no card guarantee => guaranteed_by_card=false; was never relocated before => "
          "walked_before=false; has no early arrival granted => early_checkin_given=false",
     links="arrival > guest: names / named by; arrival > partner: relocates to / chosen for",
     actions="check in = register; upgrade = move up; relocate = walk; compensate = make good",
     sources="arrivals list; reservation system; guest phone call; partner hotel email; loyalty profile; "
             "night manager log",
     inert="""
     keycard_design | cat | seashell card; lighthouse card
     lobby_flowers | cat | orchids; lilies
     bellcart_colour | cat | gold cart; silver cart
     umbrella_rack | cat | full rack; empty rack
     welcome_cookie | cat | oatmeal; chocolate
     """,
     affix="unguaranteed => guaranteed_by_card; unwalked => walked_before"),

dict(slot="hs-09", slug="banquet-orders", sector="hospitality",
     sub="convention hotel banquet event orders and room block attrition",
     org="Meridale Convention Hotel", desk="conference services office",
     setting="A convention hotel hosts meetings and banquets under signed contracts. The conference services "
             "office applies guarantee, attrition and food-and-beverage minimum rules to each event order.",
     decider="event planner",
     roles="conference services manager; banquet captain; catering sales manager; audiovisual technician; "
           "room block coordinator; billing analyst",
     docs="banquet event order; group contract; attrition report; final guarantee form; audiovisual order; "
          "master bill",
     scope=("function space", "Grand Ballroom; Harbour Room; Executive Boardroom; Terrace Pavilion"),
     money="dollars",
     ents=[
        dict(key="event", singular="banquet event", plural="banquet events", id="BE", aka="function",
             attrs="""
             guarantee_count | int | 10..1200 people | aka=final guarantee
             fnb_minimum | money | 500.00..250000.00 | aka=food and beverage minimum
             room_nights_picked_up | int | 0..2000 nights | aka=rooms used
             room_nights_contracted | int | 10..2000 nights | aka=rooms in the contract
             hours_before_event_guarantee | int | 0..168 hours | aka=guarantee lead time
             meal_period | cat | breakfast; lunch; reception; dinner; break service
             service_style | cat | plated; buffet; stations; family style
             event_tier | ord | standard; signature; gala | aka=event level
             guarantee_submitted | event | bad=0 | aka=final count sent | grp=guarantee
             av_ordered | event | bad=0 | aka=audiovisual order placed
             outside_vendor_used | state | bad=1 | aka=outside caterer involved
             tax_exempt | state | bad=0 | aka=tax exemption on file
             contract_signed | state | bad=0 | aka=contract executed
             contracted_on | date
             event_on | date
             event_tags | tag | awards night; keynote; vegetarian heavy; late finish; outdoor backup
             """),
        dict(key="client", singular="meeting client", plural="meeting clients", id="MC",
             names="org: Association, Society, Corporation, Federation",
             attrs="""
             events_held_here | int | 0..30 items | aka=past events at the hotel
             """),
        dict(key="contact", singular="meeting planner", plural="meeting planners", id="MP", names="person",
             role="person",
             attrs="""
             changes_after_cutoff | int | 0..10 entries | aka=late changes
             """),
     ],
     outcomes=["accept guarantee; accept with overset; charge attrition fee*; charge minimum shortfall*; "
               "send to conference services manager",
               "plated service; buffet service; stations; boxed meals*"],
     levels=["standard; signature; gala", "low; medium; high"],
     words="""
     massive: guarantee_count >= 500
     modest: guarantee_count < 30
     lavish: fnb_minimum >= 50000
     tardy: hours_before_event_guarantee < 72
     committed: guarantee_submitted
     equipped: av_ordered
     privileged: tax_exempt
     binding: contract_signed
     loyal: events_held_here >= 5
     fickle: changes_after_cutoff >= 3
     casual: service_style == buffet
     glamorous: event_tier == gala
     morning: meal_period == breakfast
     visiting: outside_vendor_used
     """,
     cues="never sent the final count => guarantee_submitted=false; lacks an executed contract => "
          "contract_signed=false; has no tax exemption on file => tax_exempt=false",
     links="event > client: bills / billed by; event > contact: credits / credited by",
     actions="guarantee = lock count; reset = change setup; invoice = bill; release = hand back rooms",
     sources="banquet event order; planner email; room block report; catering note; billing system; "
             "audiovisual order",
     inert="""
     linen_colour | cat | ivory; charcoal
     centerpiece_flower | cat | peonies; hydrangeas
     stage_drape | cat | black drape; navy drape
     chair_sash | cat | sash; plain
     ballroom_chandelier | cat | crystal; bronze
     """,
     affix="unsigned => contract_signed; unsubmitted => guarantee_submitted"),

dict(slot="hs-10", slug="catering-orders", sector="hospitality",
     sub="catering kitchen order desk handling menu substitutions and allergen rules",
     org="Fennimore Hall Catering Kitchen", desk="catering order desk",
     setting="A catering kitchen prepares meals for offices, weddings and schools. The order desk applies the "
             "kitchen's lead time, minimum order, substitution and allergen rules to every order.",
     decider="head chef",
     roles="sous chef; catering coordinator; delivery driver; pastry chef; kitchen porter; account manager",
     docs="catering order; allergen matrix; prep list; delivery sheet; substitution notice; invoice",
     scope=("delivery zone", "City Center; Business Park; Riverside; University Quarter"),
     money="pounds sterling",
     ents=[
        dict(key="order", singular="catering order", plural="catering orders", id="KD", aka="food order",
             attrs="""
             portions | int | 10..800 covers | aka=servings
             order_value | money | 80.00..30000.00 | aka=order total
             hours_lead_time | int | 2..336 hours | aka=notice before delivery
             delivery_km | dec1 | 0.5..40.0 kilometres | aka=delivery distance
             menu_style | cat | sandwich platters; hot buffet; canapes; plated dinner; bento boxes
             dietary_mix | cat | standard; vegetarian; vegan; halal; kosher style
             spice_level | ord | mild; medium; hot | aka=heat level
             allergen_sheet_given | event | bad=0 | aka=allergen details provided | grp=allergen
             nut_free_kitchen_needed | state | bad=1 | aka=needs a separate nut-safe prep
             staff_service_booked | event | bad=0 | aka=serving staff ordered
             tasting_completed | event | bad=0 | aka=menu tasting held
             reusable_crockery | state | bad=0 | aka=uses returnable dishes
             ordered_on | date
             deliver_on | date
             order_tags | tag | breakfast; office lunch; wedding; school event; funeral reception
             """),
        dict(key="client", singular="catering client", plural="catering clients", id="KC",
             names="org: Partners, Group, College, Trust",
             attrs="""
             orders_this_year | int | 0..100 items | aka=orders this year
             account_terms_days | int | 0..60 days | aka=payment terms
             """),
        dict(key="dish", singular="menu item", plural="menu items", id="MN",
             names=["Item Roast Squash Tart", "Item Lemon Chicken", "Item Herb Couscous", "Item Beetroot Salad", "Item Lamb Kofta", "Item Berry Pavlova", "Item Smoked Trout Blini", "Item Chickpea Curry"],
             attrs="""
             cost_per_portion | money | 0.80..18.00 | aka=portion cost
             contains_nuts | state | bad=1 | aka=nut ingredient present
             """),
        dict(key="driver", singular="delivery driver", plural="delivery drivers", id="DV", names="person",
             role="person",
             attrs="""
             deliveries_today | int | 0..20 items | aka=drops today
             """),
     ],
     outcomes=["accept order; accept with substitutions; send to head chef; ask for allergen details*; "
               "reject order*",
               "cold delivery; hot delivery with staff; collection by client*"],
     levels=["mild; medium; hot", "low; medium; high"],
     words="""
     huge: portions >= 300
     modest: portions < 25
     lucrative: order_value >= 5000
     rushed: hours_lead_time < 24
     relaxed: hours_lead_time >= 168
     remote: delivery_km >= 20
     declared: allergen_sheet_given
     attended: staff_service_booked
     savored: tasting_completed
     frequent: orders_this_year >= 20
     nutty: contains_nuts
     pricey: cost_per_portion >= 10
     plant-based: dietary_mix == vegan
     fiery: spice_level == hot
     sustainable: reusable_crockery
     """,
     cues="lacks allergen details => allergen_sheet_given=false; never held a menu tasting => "
          "tasting_completed=false; has no serving staff ordered => staff_service_booked=false",
     links="order > client: bills / billed by; order > dish: lists / listed by",
     actions="accept = take order; substitute = swap dish; prep = cook ahead; deliver = drop off",
     sources="catering order; client email; allergen matrix; driver log; account manager note; prep list",
     inert="""
     van_number_plate_colour | cat | white plate; yellow plate
     apron_colour | cat | black apron; striped apron
     back_room_radio | cat | pop station; talk station
     whisk_brand | cat | brand W; brand Z
     wall_tiles | cat | white tiles; green tiles
     """,
     affix="untasted => tasting_completed; unstaffed => staff_service_booked"),
]
