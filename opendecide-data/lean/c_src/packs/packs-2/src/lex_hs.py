"""packs-2 lexicons, sector hs (Claude-written, v1.1 review fix). Line format: see src/lex_ed.py."""

LEX = {
"hs-01": """
guests_expected | syn: attendance expected, guest count | say: {E} expects {v}
hours_booked | syn: rental hours, booking length | say: {E} books the space for {v}
rental_fee | syn: hire charge, room fee | say: {E} carries a rental fee of {v}
days_before_event | syn: booking lead, days ahead | say: {E} was made {v} before the event
event_kind | syn: kind of event, event type | say: {E} is for a {v}
renter_type | syn: renter category, hirer type | say: {E} comes from a {v} renter
noise_level | syn: noise expected, loudness | say: {E} is rated {v} for noise
deposit_received | syn: deposit paid, booking deposit in | pos: {E} has its deposit received | neg: {E} does not have its deposit received | br: payment security | nr: card deposit charged | imp: date held
insurance_certificate_filed | syn: liability insurance on file, insurance proof | pos: {E} has an insurance certificate filed | neg: {E} has no insurance certificate filed | br: liability cover | nr: event policy certificate | imp: risk transferred
lifeguard_needed | syn: pool guard required, lifeguard required | pos: {E} needs a lifeguard | neg: {E} does not need a lifeguard | br: water safety staffing | nr: pool use in the booking | imp: extra staff cost
food_served | syn: catering present, meals served | pos: {E} has food served | neg: {E} does not have food served | br: kitchen use | nr: buffet at the party | imp: cleaning fee
walkthrough_done | syn: site visit done, space tour completed | pos: {E} has had a walkthrough | neg: {E} has not had a walkthrough | br: renter orientation | nr: tour of the hall | imp: layout agreed
booked_on | syn: booking date, date booked | say: {E} was made on {v}
event_on | syn: event date, day of the event | say: {E} is for an event on {v}
booking_tags | syn: booking labels, booking markers | say: {E} carries the booking tags {v} | none: {E} carries none of the booking tags
past_bookings | syn: earlier rentals, booking history | say: {E} has made {v} before
damage_charges_before | syn: past damage bills, earlier damage costs | say: {E} has paid {v} in damage charges before
capacity | syn: room capacity, maximum occupancy | say: {E} holds up to {v}
cleaning_hours | syn: cleanup time, turnover hours | say: {E} needs {v} of cleaning
""",
"hs-02": """
party_size | syn: guests in the party, party count | say: {E} is for {v}
booking_cost | syn: outing cost, booking price | say: {E} costs {v}
hours_until_outing | syn: hours to the outing, booking lead | say: {E} comes {v} before the outing
nights_in_stay | syn: stay length, nights booked | say: {E} belongs to a stay of {v}
booking_kind | syn: kind of booking, outing type | say: {E} is for {v}
occasion | syn: reason for the trip, celebration type | say: {E} marks a {v}
guest_tier | syn: loyalty tier, membership level | say: {E} comes from a {v} member
card_on_file | syn: card stored, payment card held | pos: {E} has a card on file | neg: {E} has no card on file | br: payment guarantee | nr: card tokenized at check-in | imp: charges can post
vendor_confirmed | syn: vendor accepted, supplier confirmation | pos: {E} has the vendor's confirmation | neg: {E} does not have the vendor's confirmation | br: booking secured | nr: confirmation number from the theatre | imp: seats held
complaint_logged | syn: earlier complaint, guest grievance this stay | pos: {E} comes from a guest who complained earlier this stay | neg: {E} comes from a guest who did not complain earlier this stay | br: service recovery case | nr: noise complaint at the desk | imp: goodwill gesture
repeat_guest | syn: returning guest, past guest | pos: {E} comes from a repeat guest | neg: {E} does not come from a repeat guest | br: guest loyalty | nr: third stay this year | imp: guest history on file
booked_on | syn: booking date, date booked | say: {E} was made on {v}
outing_on | syn: outing date, day of the outing | say: {E} is for an outing on {v}
booking_tags | syn: booking labels, booking markers | say: {E} carries the booking tags {v} | none: {E} carries none of the booking tags
spend_this_stay | syn: folio total, spend during the stay | say: {E} has spent {v} this stay
stays_this_year | syn: visits this year, yearly stays | say: {E} has stayed {v} this year
commission_rate | syn: hotel commission, commission share | say: {E} pays a commission of {v}
partner_agreement | syn: preferred vendor deal, partner contract | pos: {E} has a partner agreement | neg: {E} has no partner agreement | br: supplier relationship | nr: signed preferred rate sheet | imp: commission paid
""",
"hs-03": """
group_size | syn: headcount, group count | say: {E} brings {v}
chaperones | syn: adult supervisors, chaperone count | say: {E} brings {v} as chaperones
ticket_price | syn: price per ticket, admission price | say: {E} pays {v} per ticket
days_before_visit | syn: booking lead, days ahead | say: {E} was placed {v} before the visit
group_type | syn: kind of group, group category | say: {E} is a {v} group
meal_package | syn: food package, meal plan | say: {E} includes a {v}
group_tier | syn: size class, group band | say: {E} falls in the {v} class
deposit_paid | syn: group deposit paid, deposit received | pos: {E} has its deposit paid | neg: {E} does not have its deposit paid | br: payment commitment | nr: check for the deposit cleared | imp: date held
waiver_forms_received | syn: release forms returned, waivers in | pos: {E} has its waiver forms received | neg: {E} does not have its waiver forms received | br: liability paperwork | nr: signed parent waivers | imp: riders cleared to ride
rain_date_chosen | syn: backup date chosen, weather date set | pos: {E} has a rain date chosen | neg: {E} has no rain date chosen | br: weather contingency | nr: second date in May | imp: visit can move
tax_exempt | syn: exempt from sales tax, tax exemption | pos: {E} is tax exempt | neg: {E} is not tax exempt | br: tax status | nr: school exemption form | imp: sales tax waived
ride_closure_affects | syn: closed ride affects the visit, ride outage | pos: {E} is affected by a ride closure | neg: {E} is not affected by a ride closure | br: attraction outage | nr: coaster closed for repairs | imp: partial refund talk
ordered_on | syn: order date, date ordered | say: {E} was placed on {v}
visit_on | syn: visit date, park day | say: {E} is for a visit on {v}
order_tags | syn: order labels, order markers | say: {E} carries the order tags {v} | none: {E} carries none of the order tags
past_visits | syn: earlier group visits, visit history | say: {E} has led {v} before
phone_checked | syn: phone confirmed, contact number checked | pos: {E} has a checked phone number | neg: {E} does not have a checked phone number | br: reachable leader | nr: call-back answered | imp: day-of contact possible
visits_used | syn: pass visits, uses so far | say: {E} has been used for {v}
pass_price | syn: pass cost, season pass price | say: {E} cost {v}
""",
"hs-04": """
treatment_minutes | syn: treatment length, session minutes | say: {E} lasts {v}
treatment_price | syn: treatment cost, session price | say: {E} costs {v}
hours_notice_of_change | syn: change notice, hours of warning | say: {E} was changed with {v} of notice
guests_in_booking | syn: people booked, guests booked | say: {E} is for {v}
treatment_kind | syn: kind of treatment, therapy type | say: {E} is a {v}
guest_category | syn: guest type, visitor category | say: {E} comes from a {v}
intensity_choice | syn: pressure level, intensity | say: {E} asks for {v} pressure
health_form_signed | syn: intake form signed, health questionnaire signed | pos: {E} has a signed health form | neg: {E} does not have a signed health form | br: guest screening | nr: allergy questions answered | imp: treatment cleared
pregnancy_noted | syn: guest is pregnant, pregnancy reported | pos: {E} notes a pregnancy | neg: {E} does not note a pregnancy | br: treatment caution | nr: second trimester noted | imp: treatment limits
package_voucher_used | syn: voucher applied, package credit used | pos: {E} uses a package voucher | neg: {E} does not use a package voucher | br: prepaid value | nr: spa day voucher | imp: zero balance at the desk
arrived_late | syn: came after the start, late arrival | pos: {E} had the guest arrive late | neg: {E} did not have the guest arrive late | br: punctuality problem | nr: ten minutes after the slot | imp: treatment cut short
room_charge_allowed | syn: can charge to the room, room billing allowed | pos: {E} allows room charges | neg: {E} does not allow room charges | br: billing route | nr: folio open for spa charges | imp: pay at checkout
booked_on | syn: booking date, date booked | say: {E} was booked on {v}
treatment_on | syn: treatment date, appointment day | say: {E} is set for {v}
appointment_tags | syn: appointment labels, appointment markers | say: {E} carries the appointment tags {v} | none: {E} carries none of the appointment tags
visits_this_year | syn: spa visits this year, yearly visits | say: {E} has visited {v} this year
retail_spend | syn: product spend, shop purchases | say: {E} has spent {v} on products
bookings_today | syn: appointments today, today's load | say: {E} has {v} today
specialist_grade | syn: therapist grade, skill grade | say: {E} is a {v} therapist
""",
"hs-05": """
seats_booked | syn: seats held, seat count | say: {E} holds {v}
fare_total | syn: total fare, booking price | say: {E} totals {v}
days_to_departure | syn: days before departure, booking lead | say: {E} departs in {v}
changes_made | syn: changes so far, amendment count | say: {E} has had {v} of changes
tour_length | syn: trip length, tour duration | say: {E} is a {v} tour
booking_channel | syn: booking route, sales channel | say: {E} was booked by {v}
seat_class | syn: seat grade, seat type | say: {E} is in a {v}
balance_paid | syn: final payment received, balance settled | pos: {E} has its balance paid | neg: {E} does not have its balance paid | br: full payment | nr: final instalment cleared | imp: tickets released
insurance_bought | syn: travel cover added, insurance purchased | pos: {E} includes travel insurance | neg: {E} does not include travel insurance | br: trip protection | nr: cancellation cover | imp: refund route through the insurer
mobility_assist | syn: boarding help needed, mobility support | pos: {E} needs boarding help | neg: {E} does not need boarding help | br: accessibility need | nr: wheelchair lift needed | imp: front seat assignment
passport_details_given | syn: travel document details on file, passport data supplied | pos: {E} has passport details given | neg: {E} does not have passport details given | br: border readiness | nr: passport number entered | imp: manifest complete
booked_on | syn: booking date, date booked | say: {E} was booked on {v}
departs_on | syn: departure date, travel date | say: {E} departs on {v}
reservation_tags | syn: reservation labels, reservation markers | say: {E} carries the reservation tags {v} | none: {E} carries none of the reservation tags
tours_taken | syn: past tours, tour history | say: {E} has taken {v}
loyalty_points | syn: points balance, reward points | say: {E} holds {v}
seats_left | syn: open seats, seats remaining | say: {E} has {v} left
minimum_to_run | syn: minimum bookings, run threshold | say: {E} needs {v} to run
guaranteed_departure | syn: departure guaranteed, sure to run | pos: {E} is guaranteed to run | neg: {E} is not guaranteed to run | br: departure certainty | nr: minimum reached early | imp: travellers can book flights
""",
"hs-06": """
covers | syn: party size, diners | say: {E} is for {v}
deposit_amount | syn: deposit held, table deposit | say: {E} holds a deposit of {v}
minutes_late | syn: lateness in minutes, minutes after booking time | say: {E} arrived {v} after the booked time
days_ahead_booked | syn: booking lead, days in advance | say: {E} was made {v} ahead
seating_time | syn: sitting, service slot | say: {E} is for the {v}
occasion | syn: reason for dining, celebration type | say: {E} marks a {v}
spend_band | syn: menu level, spend tier | say: {E} is for the {v} menu
deposit_taken | syn: deposit charged, card deposit taken | pos: {E} has had a deposit taken | neg: {E} has not had a deposit taken | br: booking guarantee | nr: card charged at booking | imp: table held
allergy_flagged | syn: serious allergy noted, allergy alert | pos: {E} flags a serious allergy | neg: {E} does not flag a serious allergy | br: kitchen safety need | nr: shellfish allergy | imp: chef briefing
confirmed_by_text | syn: text confirmation, message reply received | pos: {E} was confirmed by text | neg: {E} was not confirmed by text | br: guest commitment | nr: reply to the reminder message | imp: guest likely to arrive
accessible_table_needed | syn: step-free table needed, wheelchair table | pos: {E} needs an accessible table | neg: {E} does not need an accessible table | br: access need | nr: ground floor table | imp: table choice limited
high_chair_needed | syn: child seat needed, baby chair needed | pos: {E} needs a high chair | neg: {E} does not need a high chair | br: family seating | nr: toddler in the party | imp: space by the table
booked_on | syn: booking date, date booked | say: {E} was made on {v}
dining_on | syn: dining date, date of the meal | say: {E} is for dinner on {v}
reservation_tags | syn: reservation labels, reservation markers | say: {E} carries the reservation tags {v} | none: {E} carries none of the reservation tags
past_missed_bookings | syn: missed-booking history, earlier missed bookings | say: {E} has missed {v} before
visits_this_year | syn: visits so far this year, yearly visits | say: {E} has dined {v} this year
seats_at_table | syn: table size, chairs at the table | say: {E} seats {v}
turn_minutes | syn: table time, sitting length | say: {E} turns in {v}
""",
"hs-07": """
travellers | syn: group size, passenger count | say: {E} carries {v}
deposit_due | syn: deposit owed, amount due as deposit | say: {E} owes a deposit of {v}
days_to_travel | syn: days to departure, booking lead | say: {E} travels in {v}
name_changes | syn: names swapped, passenger swaps | say: {E} has made {v} of name changes
trip_style | syn: kind of trip, trip type | say: {E} is a {v}
supplier_type | syn: kind of supplier, supplier category | say: {E} books through a {v}
contract_level | syn: contract flexibility, terms tier | say: {E} holds a {v} contract
first_deposit_paid | syn: first deposit received, initial payment made | pos: {E} has its first deposit paid | neg: {E} does not have its first deposit paid | br: payment commitment | nr: wire for the deposit cleared | imp: space held
rooming_roster_sent | syn: room roster delivered, room assignments sent | pos: {E} has its rooming roster sent | neg: {E} does not have its rooming roster sent | br: hotel readiness | nr: names and bed types sent | imp: rooms assigned
escort_assigned | syn: tour escort in place, guide assigned | pos: {E} has an escort assigned | neg: {E} has no escort assigned | br: group supervision | nr: named tour leader | imp: on-trip support
visa_support_needed | syn: visa letters needed, entry letters required | pos: {E} needs visa support | neg: {E} does not need visa support | br: entry paperwork | nr: invitation letters for the embassy | imp: longer lead time
minimum_met | syn: group minimum reached, minimum numbers met | pos: {E} meets the group minimum | neg: {E} does not meet the group minimum | br: viability | nr: forty travellers signed up | imp: group rate holds
contracted_on | syn: contract date, date signed | say: {E} was contracted on {v}
departs_on | syn: departure date, travel date | say: {E} departs on {v}
group_tags | syn: group labels, group markers | say: {E} carries the group tags {v} | none: {E} carries none of the group tags
trips_organized | syn: past trips run, trips led | say: {E} has organized {v}
attrition_allowance | syn: allowed drop, attrition share | say: {E} allows {v} attrition
release_days | syn: release lead, days before release | say: {E} takes space back {v} before travel
""",
"hs-08": """
nights_booked | syn: nights of stay, nights reserved | say: {E} is for {v}
nightly_rate | syn: room rate, rate per night | say: {E} pays {v} a night
eta_hour | syn: arrival hour, expected arrival time | say: {E} arrives at hour {v}
rooms_in_booking | syn: rooms held, room count | say: {E} holds {v}
rate_type | syn: rate plan, price plan | say: {E} is on a {v}
booking_source | syn: booking channel, sales source | say: {E} came through {v}
loyalty_level | syn: loyalty status, member tier | say: {E} holds {v} status
guaranteed_by_card | syn: card guarantee, card-held booking | pos: {E} is guaranteed by card | neg: {E} is not guaranteed by card | br: booking security | nr: card details taken at booking | imp: late arrival covered
prepaid_nonrefundable | syn: paid in advance, prepaid fare | pos: {E} is prepaid | neg: {E} is not prepaid | br: payment certainty | nr: advance purchase rate charged | imp: zero balance due
walked_before | syn: relocated before, walked on an earlier stay | pos: {E} comes from a guest walked before | neg: {E} comes from a guest not walked before | br: past service failure | nr: sent to a partner hotel last year | imp: guest sensitivity
accessible_room_needed | syn: step-free room needed, mobility room needed | pos: {E} needs an accessible room | neg: {E} does not need an accessible room | br: access need | nr: roll-in shower room | imp: room choice limited
early_checkin_given | syn: early arrival granted, early check-in | pos: {E} was given early check-in | neg: {E} was not given early check-in | br: arrival courtesy | nr: room ready by ten | imp: room taken off sale early
booked_on | syn: booking date, date booked | say: {E} was booked on {v}
arrives_on | syn: arrival date, check-in date | say: {E} arrives on {v}
arrival_tags | syn: arrival labels, arrival markers | say: {E} carries the arrival tags {v} | none: {E} carries none of the arrival tags
stays_last_year | syn: nights last year, stay history | say: {E} stayed {v} last year
distance_km | syn: distance away, kilometres from the hotel | say: {E} lies {v} from the hotel
partner_rate | syn: partner room rate, relocation rate | say: {E} charges {v} a night
""",
"hs-09": """
guarantee_count | syn: final count, guaranteed covers | say: {E} guarantees {v}
fnb_minimum | syn: food and beverage minimum, catering minimum | say: {E} carries a minimum of {v}
room_nights_picked_up | syn: rooms used, block pickup | say: {E} picked up {v}
room_nights_contracted | syn: contracted rooms, room block size | say: {E} contracted {v}
hours_before_event_guarantee | syn: guarantee lead time, hours of notice for the count | say: {E} sent its count {v} before the event
meal_period | syn: meal time, service period | say: {E} is a {v} function
service_style | syn: service format, style of service | say: {E} is served {v}
event_tier | syn: event level, function grade | say: {E} is a {v} event
guarantee_submitted | syn: final count sent, guarantee sent | pos: {E} has its guarantee submitted | neg: {E} does not have its guarantee submitted | br: count commitment | nr: signed count form | imp: kitchen orders set
av_ordered | syn: audiovisual order placed, AV booked | pos: {E} has audiovisual ordered | neg: {E} does not have audiovisual ordered | br: technical setup | nr: projector and microphones booked | imp: AV charges
outside_vendor_used | syn: outside caterer involved, external vendor | pos: {E} uses an outside vendor | neg: {E} does not use an outside vendor | br: third-party service | nr: outside cake supplier | imp: service charge for outside food
tax_exempt | syn: tax exemption on file, exempt from tax | pos: {E} is tax exempt | neg: {E} is not tax exempt | br: tax status | nr: exemption letter | imp: tax waived on the bill
contract_signed | syn: contract executed, agreement signed | pos: {E} has a signed contract | neg: {E} does not have a signed contract | br: binding agreement | nr: client countersigned | imp: terms enforceable
contracted_on | syn: contract date, date signed | say: {E} was contracted on {v}
event_on | syn: event date, function date | say: {E} takes place on {v}
event_tags | syn: event labels, event markers | say: {E} carries the event tags {v} | none: {E} carries none of the event tags
events_held_here | syn: past events here, event history | say: {E} has held {v} here
changes_after_cutoff | syn: late changes, changes past the cutoff | say: {E} has made {v} after the cutoff
""",
"hs-10": """
portions | syn: servings, portion count | say: {E} is for {v}
order_value | syn: order total, order price | say: {E} totals {v}
hours_lead_time | syn: notice before delivery, lead hours | say: {E} gives {v} of notice
delivery_km | syn: delivery distance, kilometres to the venue | say: {E} goes {v} for delivery
menu_style | syn: menu format, kind of menu | say: {E} is for {v}
dietary_mix | syn: diet type, dietary style | say: {E} is {v}
spice_level | syn: heat level, spice rating | say: {E} is cooked {v}
allergen_sheet_given | syn: allergen details provided, allergen form supplied | pos: {E} has an allergen sheet given | neg: {E} does not have an allergen sheet given | br: allergy information | nr: guest allergy form | imp: kitchen can plan safe dishes
nut_free_kitchen_needed | syn: nut-safe prep needed, separate prep area | pos: {E} needs nut-safe preparation | neg: {E} does not need nut-safe preparation | br: allergen control | nr: separate tools and boards | imp: extra prep time
staff_service_booked | syn: serving staff ordered, servers booked | pos: {E} has service staff booked | neg: {E} does not have service staff booked | br: event staffing | nr: two servers for the buffet | imp: staffing charge
tasting_completed | syn: menu tasting held, sample tasting done | pos: {E} has had a tasting | neg: {E} has not had a tasting | br: menu approval | nr: client tasted the canapes | imp: menu locked
reusable_crockery | syn: returnable dishes, washable china | pos: {E} uses reusable crockery | neg: {E} does not use reusable crockery | br: dish return logistics | nr: china hire | imp: collection trip
ordered_on | syn: order date, date ordered | say: {E} was placed on {v}
deliver_on | syn: delivery date, event date | say: {E} is for delivery on {v}
order_tags | syn: order labels, order markers | say: {E} carries the order tags {v} | none: {E} carries none of the order tags
orders_this_year | syn: yearly orders, orders so far this year | say: {E} has ordered {v} this year
account_terms_days | syn: payment terms, credit days | say: {E} pays on {v} terms
cost_per_portion | syn: portion cost, cost per serving | say: {E} costs {v} per portion
contains_nuts | syn: nut ingredient present, includes nuts | pos: {E} contains nuts | neg: {E} does not contain nuts | br: allergen content | nr: almond crust | imp: allergen label
deliveries_today | syn: drops today, delivery runs today | say: {E} has made {v} today
""",
}
