"""Affect hard items, batch intent: service-request intents for invented services (with none of these)."""
from common import I, T, NONE_LABEL

POLICY = ("Routing policy: assign the one intent that matches what the customer is asking us to do in this message. "
          "Background details, things already resolved, and features merely mentioned do not decide the intent. "
          "If no intent covers the request, choose none of these.")
SAFETY = ("Routing policy: assign the one intent that matches what the guest needs from us in this message. Any "
          "message that reports a present danger at the property goes to urgent safety issue, whatever else it "
          "contains. If no intent covers the request, choose none of these.")
LUMEN = ("Routing policy: route by what the customer is asking Lumen Grid to do. A report of a gas smell or leak "
         "always goes to gas emergency, whatever else the message contains. If no intent covers the request, "
         "choose none of these.")

QCU = "Quillfeather Credit Union"
TP = "Tandem Pantry"
DS = "Driftwood Stays"
LG = "Lumen Grid Energy"
PW = "Parcelwise"
KM = "Kestrel Mobile"
SC = "Stackhouse Cloud"

ITEMS = [
# I1 can't find card, expects to find it -> freeze; twin: gone for good -> report lost or stolen
I("in_qcu_card_coat",
POLICY + """

Quillfeather Credit Union - secure message
Member: Rohan Das | Received: Friday 19:12

Hi, I can't find my debit card. I'm fairly sure it's in the pocket of my other coat, which I left at my sister's in Harlow on Wednesday, and I'm seeing her on Sunday. Could you stop it working until then, just in case I'm wrong and it's somewhere else? Please don't cancel it or send a new one, because my rent and two subscriptions are set up on that card number and changing them all is a nightmare. I'll switch it back on myself in the app once I have it.

Thanks, Rohan""",
QCU, ["freeze card", "report lost or stolen card", "card not arrived", "card declined", "change PIN",
      "update contact details", "dispute a charge", "raise card limit"], "freeze card", 2,
twin=T([("I'm fairly sure it's in the pocket of my other coat, which I left at my sister's in Harlow on Wednesday, and I'm seeing her on Sunday. Could you stop it working until then, just in case I'm wrong and it's somewhere else? Please don't cancel it or send a new one, because my rent and two subscriptions are set up on that card number and changing them all is a nightmare. I'll switch it back on myself in the app once I have it.",
         "I thought it was in the pocket of my other coat at my sister's in Harlow, but she has turned her flat upside down and it isn't there; the last place I had it was on the 42 bus on Wednesday. Please cancel it for good and send me a new one. I'll update my rent and two subscriptions with the new number when it comes.")],
       "report lost or stolen card")),

# I2 pending hold question -> pending charge query; twin: posted double charge -> dispute
I("in_qcu_hotel_hold",
POLICY + """

Quillfeather Credit Union - chat transcript (member side only)
Member: Beatriz Salgado | Channel: app chat | Monday 10:03

Beatriz: Hi, quick question. There's a $148.20 charge from Harbour Lights Hotel on my card that is still showing as pending. I checked out on Tuesday and paid my bill of $112.60 at the front desk with the same card, which has gone through. I assume the pending one is the deposit hold they put on at check-in? How long does that usually take to drop off? I'm not disputing anything at this point, I'd just like to know what it is and when it goes.""",
QCU, ["pending charge query", "dispute a charge", "card declined", "exchange rate query", "transfer not received",
      "freeze card", "raise card limit"], "pending charge query", 2,
twin=T([("that is still showing as pending. I checked out on Tuesday and paid my bill of $112.60 at the front desk with the same card, which has gone through. I assume the pending one is the deposit hold they put on at check-in? How long does that usually take to drop off? I'm not disputing anything at this point, I'd just like to know what it is and when it goes.",
         "that posted yesterday as a completed charge. I checked out on Tuesday and paid my bill of $112.60 at the front desk with the same card, which has also gone through, so I've been charged twice for one stay. The hotel says to take it up with my bank. I want the $148.20 taken back, please.")],
       "dispute a charge")),

# I3 declined abroad although travel notice already filed -> card declined
I("in_qcu_lisbon_declined",
POLICY + """

Quillfeather Credit Union - secure message
Member: Keisha Morrow | Received: Thursday 08:47 (member's local time: Lisbon)

Hello, I'm in Lisbon for a conference. This morning my Quillfeather Visa was refused at a pharmacy and then again at a cash machine near the hotel. I did the travel notice in the app last Monday before I flew, and it shows as "active" for Portugal from the 14th to the 21st, so it isn't that. The exchange rate on yesterday's dinner looked fine too. Nothing else has changed on my account that I know of. Can you tell me why it's being refused and get it working today? I have about €20 in cash.""",
QCU, ["card declined", "travel notice", "exchange rate query", "freeze card", "report lost or stolen card",
      "raise card limit", "change PIN", "pending charge query", "cash not dispensed", "card not arrived"],
"card declined", 2),

# I4 ATM gave no cash -> cash not dispensed (not dispute)
I("in_qcu_atm_no_cash",
POLICY + """

Quillfeather Credit Union - phone call summary written by the agent before transfer
Caller: Mr Florian Weiss | Verified: yes | Time: Saturday 16:20

Caller used the ATM outside the Corran Street branch at about 15:50. He requested $200. The machine kept the card for longer than usual, made grinding noises, returned the card and printed a receipt showing $200 withdrawn, but no notes came out. His balance in the app already shows the $200 taken. He wants the money put back. He specifically asked whether he needs to "dispute" it; told him the right team would advise. He has the receipt and a photo of the machine's screen, which showed "Transaction complete". No other issues with the card.""",
QCU, ["cash not dispensed", "dispute a charge", "card declined", "pending charge query", "transfer not received",
      "raise card limit"], "cash not dispensed", 2),

# I5 add joint holder -> none of these
I("in_qcu_joint_holder",
POLICY + """

Quillfeather Credit Union - branch enquiry form (typed by member at kiosk)
Member: Olufemi Adeyemi | Branch: Harrow Road | Tuesday 11:30

I would like to add my daughter, Mira Adeyemi, as a joint owner on my Everyday Savings account (ending 4471). She is 19 and lives with me at the same address, so my contact details don't need changing. I don't want to close the account or open a new one, and I don't need a card for her yet. Please tell me what documents she needs to bring and whether we both need to come to the branch together.""",
QCU, ["close account", "update contact details", "freeze card", "change PIN", "raise card limit", "travel notice",
      "card not arrived", "transfer not received", "exchange rate query", "report lost or stolen card",
      "dispute a charge"], NONE_LABEL, 2),

# I6 different product, substitutions switched off -> wrong item
I("in_tp_oat_milk",
POLICY + """

Tandem Pantry - Help centre message
Customer: Lior Ben-Ami | Order #TP-558120 | Delivered Wednesday 18:40

Hi, I ordered 2 x Hearth Oat Drink (unsweetened, 1L). What came is 2 x Hearth Oat Drink Barista Edition, which has added sugar and oil. My account has "no substitutions" ticked for dairy alternatives because of my son's diet, and I didn't get any substitution message or photo at the door. Everything else in the order was right and in perfect condition, and the driver was on time. Could I get the two cartons refunded? I'm happy to leave them out for collection if you need them back.""",
TP, ["wrong item", "missing item", "damaged item", "substitution preferences", "refund status", "driver feedback",
     "late delivery", "promo code problem"], "wrong item", 2),

# I7 set a standing preference -> substitution preferences; twin: preference ignored this order -> wrong item
I("in_tp_eggs_pref",
POLICY + """

Tandem Pantry - Help centre message
Customer: Harriet Oyelowo | Account: Pantry Plus member | Sent: Sunday 21:05

Hello. On my last three orders, when the free-range organic eggs were out of stock, the shopper put caged eggs in instead. I don't blame the shoppers, it's probably the default setting. For all my future orders, please never substitute eggs with anything; if the free-range organic ones aren't there, just leave eggs out altogether. The same goes for chicken. I've looked in the app settings and can't see where to set this per product.

Many thanks, Harriet""",
TP, ["substitution preferences", "wrong item", "missing item", "membership billing", "add to order",
     "damaged item", "cancel order", "refund status"], "substitution preferences", 2,
twin=T([("On my last three orders, when the free-range organic eggs were out of stock, the shopper put caged eggs in instead. I don't blame the shoppers, it's probably the default setting. For all my future orders, please never substitute eggs with anything; if the free-range organic ones aren't there, just leave eggs out altogether. The same goes for chicken. I've looked in the app settings and can't see where to set this per product.",
         "Tonight's order came with caged eggs in place of the free-range organic ones, even though my account has been set to \"never substitute eggs\" since last month and nobody asked me at the door. I don't want them. Please refund the caged eggs; they're in the porch if the driver wants them back.")],
       "wrong item")),

# I8 past window, mentions going out -> late delivery (not change slot)
I("in_tp_late_order",
POLICY + """

Tandem Pantry - live chat (customer messages)
Customer: Ewan McCrae | Order #TP-559004 | Slot booked: Friday 18:00-19:00

19:41 Ewan: Hi, my delivery was booked for 6 to 7 this evening. It's now twenty to eight and nothing has arrived. The tracking has said "Your driver is on the way" since 18:15 and the map hasn't moved. I have to go out at half eight for a work thing, so I can't just sit here all night. Where is it, and is it actually coming? It has frozen stuff in it so I don't want it left on the step.""",
TP, ["late delivery", "change delivery slot", "cancel order", "driver feedback", "missing item", "refund status",
     "add to order"], "late delivery", 2),

# I9 approved refund not received -> refund status (not missing item)
I("in_tp_salmon_refund",
POLICY + """

Tandem Pantry - Help centre message
Customer: Dagny Solberg | Order #TP-551377 | Sent: Thursday 09:15

Hello again. Last Tuesday I reported that the smoked salmon (£6.99) was missing from my order, and your agent Priya confirmed in the chat that it would be refunded to my card within 3 to 5 working days. It is now working day 8 and nothing has appeared on my card statement; I've checked both the pending and posted transactions. I'm not reporting a new problem, the rest of the order was fine. I just want to know when the £6.99 will actually arrive, or whether something has gone wrong with it.""",
TP, ["refund status", "missing item", "promo code problem", "membership billing", "wrong item", "damaged item",
     "driver feedback", "substitution preferences", "cancel order", "late delivery", "add to order",
     "change delivery slot"], "refund status", 1),

# I10 praise for driver -> driver feedback
I("in_tp_driver_kemal",
POLICY + """

Tandem Pantry - feedback form (free text)
Customer: Gwendolyn Price | Order #TP-560231 | Delivered Monday 11:05

Nothing wrong with the order at all: the eggs weren't cracked, the frozen peas were still frozen, and every item was there. I just want to say that the driver, Kemal, carried all nine bags up four flights of stairs because the lift in our block is broken again, and then went back down and brought up my elderly neighbour's parcel from the lobby too, without being asked. Please make sure this gets to him and his manager. He was an absolute star.""",
TP, ["driver feedback", "damaged item", "missing item", "late delivery", "refund status", "wrong item"],
"driver feedback", 1),

# I12 gas smell plus unresponsive host -> urgent safety issue
I("in_ds_gas_cabin",
SAFETY + """

Driftwood Stays - guest message
Guest: Tomasz Wrobel | Booking: DS-88214, "Pinecrest Cabin" | Received: Saturday 21:34

We arrived about an hour ago and there's been a smell of gas in the kitchen the whole time, stronger near the cooker. We've opened all the windows and haven't switched anything on or off. My two kids are asleep upstairs. I've messaged the host three times and rung twice and there's no answer. The listing photos also showed a hot tub which isn't here, but that can wait. What should we do?""",
DS, ["urgent safety issue", "host unresponsive", "listing not as described", "cleanliness complaint",
     "check-in instructions", "cancel reservation", "noise complaint", "refund status"], "urgent safety issue", 1),

# I13 fewer bedrooms than advertised -> listing not as described
I("in_ds_third_bedroom",
SAFETY + """

Driftwood Stays - guest message
Guest: Chiamaka Obi | Booking: DS-88790, "Harbour View House" | Received: Friday 17:20

Hi. The listing says "three bedrooms, sleeps 6", and we booked it for six adults for that reason. The third "bedroom" turns out to be a sofa bed in the lounge, with no door and the kitchen right next to it. To be clear, the house is spotless, the host met us personally and has been lovely, and the check-in was easy. But one of us is now sleeping in the living room for a week. We'd like this looked at, please: either a partial refund or a move to a property that actually has three bedrooms.""",
DS, ["listing not as described", "cleanliness complaint", "host unresponsive", "change reservation dates",
     "add guests", "cancel reservation", "refund status", "security deposit query", "noise complaint"],
"listing not as described", 2),

# I14 ask to get in early -> early check-in; twin: can't get in (blank code) -> check-in instructions
I("in_ds_early_arrival",
SAFETY + """

Driftwood Stays - guest message
Guest: Sven Aaltonen | Booking: DS-89002, "Old Mill Loft" | Stay: 14-18 October | Received: 9 October

Hello! Our flight lands at 9 AM on the 14th, and we'll be at the loft by about 10:30. I can see check-in is from 3 PM. Would there be any chance of getting in at 11 instead? We're happy to pay a fee if there is one, or to wait if the cleaners need the time. Our dates stay exactly the same and it's still just the two of us.

Thanks, Sven""",
DS, ["early check-in or late checkout", "check-in instructions", "change reservation dates", "add guests",
     "host unresponsive", "cancel reservation", "payment failed", "security deposit query", "urgent safety issue",
     "listing not as described", "cleanliness complaint", "noise complaint", "refund status"],
"early check-in or late checkout", 2,
twin=T([("I can see check-in is from 3 PM. Would there be any chance of getting in at 11 instead? We're happy to pay a fee if there is one, or to wait if the cleaners need the time.",
         "I can see check-in is from 3 PM, which is fine, we'll get lunch first. But the lockbox code field in the app is blank and the listing doesn't say where the key box is. How do we get in when we arrive?")],
       "check-in instructions")),

# I15 hold still on card after checkout -> security deposit query (not refund status)
I("in_ds_deposit_hold",
SAFETY + """

Driftwood Stays - guest message
Guest: Aigerim Sultanova | Booking: DS-87555, "Larchwood Cottage" | Checked out: 10 days ago

Hi there. We checked out of Larchwood Cottage ten days ago. The host inspected the cottage the same morning, messaged to say everything was fine and thanked us for leaving it so tidy, and gave us five stars. But the $300 hold that was taken at booking is still showing on my credit card. I haven't asked for any refund of the booking itself; we had a great stay. Could you tell me when the $300 will be released?""",
DS, ["security deposit query", "refund status", "payment failed", "cancel reservation", "host unresponsive",
     "cleanliness complaint"], "security deposit query", 2),

# I16 noise, thinking about leaving but asks about noise -> noise complaint
I("in_ds_party_upstairs",
SAFETY + """

Driftwood Stays - guest message
Guest: Marek Nowicki | Booking: DS-88111, "Canal Street Apartment 2B" | Received: Wednesday 08:12

Good morning. The flat above ours has had a party every night since we arrived on Sunday, music and shouting until 3 AM. Last night someone from the party knocked on our door at 2 asking for "Dom", obviously the wrong flat. We're here for three more nights. We're honestly thinking of cutting the stay short, but before we look at cancelling anything we'd like to know whether you or the host can do something about the noise. The apartment itself is great and very clean.""",
DS, ["noise complaint", "cancel reservation", "change reservation dates", "urgent safety issue",
     "host unresponsive", "listing not as described", "refund status", "cleanliness complaint",
     "early check-in or late checkout", "add guests"], "noise complaint", 2),

# I17 moving within area, keep account -> transfer; twin: moving out of area -> stop service
I("in_lg_moving",
LUMEN + """

Lumen Grid Energy - web form "Moving home"
Customer: Priscilla Tan | Account: 5520-118-7 | Submitted: 3 October

We're moving out of 14 Fern Avenue on 31 October. Our new home is 3 Hollow Road, also in Riverside. We'd like to keep our Lumen Grid account going at the new address with the same tariff and the same direct debit, if that's possible. Final meter readings at Fern Avenue will be taken on the day we leave; I'll send photos. The new owners of Fern Avenue will be setting up their own account, and the estate agent has their details.""",
LG, ["transfer service", "stop service", "start service", "submit meter reading", "direct debit setup",
     "change tariff", "high bill query"], "transfer service", 2,
twin=T([("Our new home is 3 Hollow Road, also in Riverside. We'd like to keep our Lumen Grid account going at the new address with the same tariff and the same direct debit, if that's possible.",
         "We're moving to our daughter's in Glasgow, which is outside your area, so we'll need to close our Lumen Grid account and cancel the direct debit once the final bill is paid.")],
       "stop service")),

# I18 outage plus gas smell -> gas emergency
I("in_lg_outage_gas",
LUMEN + """

Lumen Grid Energy - emergency line, call note typed by the first-line agent
Caller: Mr Idris Farah, 12 Tolland Street | Time: 19:52

Caller says the power has been off on the whole of Tolland Street since about 6 PM; neighbours on both sides confirm. He wanted to know how long it will be. While on the call he mentioned that when he went outside to look at the street, he noticed a hissing noise and a strong smell of gas near the meter box on the front wall of number 12. He doesn't know if it's connected to the power cut. He has no gas appliances on. Advised him to stay on the line while transferring.""",
LG, ["gas emergency", "report power outage", "vegetation near lines", "high bill query", "start service",
     "payment arrangement", "change tariff", "submit meter reading"], "gas emergency", 1),

# I19 sends reading to avoid estimate -> submit meter reading
I("in_lg_reading",
LUMEN + """

Lumen Grid Energy - email to customer service
From: Bartholomew Nkemelu | Account: 5520-440-2 | Sent: 29 September, 08:14

Good morning,

Your letter dated 22 September says my next bill will be estimated unless I send an up-to-date meter reading before 1 October. Here it is: 48213, taken this morning at 8 AM. A photo of the meter is attached so you can see the serial number as well. My last few bills have been perfectly reasonable and I have no complaint about them; I just don't want an estimate this time.

Regards,
B. Nkemelu""",
LG, ["submit meter reading", "high bill query", "direct debit setup", "payment arrangement", "change tariff",
     "solar export credit", "stop service", "transfer service", "start service", "report power outage",
     "vegetation near lines"], "submit meter reading", 1),

# I20 behind on payments, offers instalments -> payment arrangement
I("in_lg_arrears",
LUMEN + """

Lumen Grid Energy - web chat (customer side)
Customer: Shona Mackintosh | Account: 5520-903-1 | Tuesday 14:10

Hi. I was off work for most of August after an operation and I've fallen behind: my account says I owe £310. My direct debit for the normal monthly amount is still going out fine, I don't want to change that. What I'm hoping is that I can pay the £310 off at £60 a month on top of the normal payments, starting in November when I'm back on full pay. Is that something you can set up? I'd rather sort it now than get another red letter.""",
LG, ["payment arrangement", "direct debit setup", "high bill query", "change tariff", "stop service",
     "submit meter reading"], "payment arrangement", 2),

# I21 solar installation quote -> none (solar export credit is a trap)
I("in_lg_solar_install",
LUMEN + """

Lumen Grid Energy - web form "Other enquiries"
Customer: Ansel Moreau | Account: 5520-221-9 | Submitted: 12 September

Hello. We're thinking about putting solar panels on our roof, probably a 4 kW system. Do you install panels yourselves, and if so, could someone come out and give us a quote? We don't have any panels yet, so I don't have questions about export credits at this stage, although I'm sure I will later. Our roof faces south-west and there's a big oak at the back that might shade it in the afternoon.

Thanks, Ansel""",
LG, ["solar export credit", "change tariff", "start service", "vegetation near lines", "transfer service",
     "high bill query", "direct debit setup", "submit meter reading", "report power outage"], NONE_LABEL, 2),

# I22 marked delivered, not received -> report lost; twin: out for delivery all day -> track parcel
I("in_pw_delivered_not_received",
POLICY + """

Parcelwise - customer message
Customer: Nadia Farouk | Tracking: PW-4471-9920-GB | Received: Tuesday 08:30

Hi. Tracking says my parcel was delivered yesterday at 14:02 and "left in safe place". There was nothing at my door when I got home at 5, nothing behind the bins or in the porch, and both neighbours say they haven't taken anything in. There's no photo on the tracking page. It's a birthday present for my mum and it was supposed to be with me by Wednesday. What happens now?""",
PW, ["report lost parcel", "track parcel", "proof of delivery request", "rebook missed delivery",
     "redirect delivery", "driver complaint", "report damaged parcel"], "report lost parcel", 2,
twin=T([("Tracking says my parcel was delivered yesterday at 14:02 and \"left in safe place\". There was nothing at my door when I got home at 5, nothing behind the bins or in the porch, and both neighbours say they haven't taken anything in. There's no photo on the tracking page.",
         "Tracking has said \"out for delivery\" since 7:40 this morning and it's now after 3, with no time slot shown. I'm at home and I haven't gone out, so I haven't missed it.")],
       "track parcel")),

# I23 leave with neighbour tomorrow -> redirect delivery (not missed delivery)
I("in_pw_neighbour",
POLICY + """

Parcelwise - customer message
Customer: Joaquín Herrera | Tracking: PW-4471-3310-GB | Received: Wednesday 21:48

Hello, my parcel is showing as due tomorrow between 10 and 2. I'll be at work all day, and last time I missed a delivery it went back to the depot and took a week to sort out, so I'd like to avoid that. Can you leave it with my neighbour at number 9 instead? Her name is Mrs Ruth Adler and she is home all day. Or, if that isn't possible, in the green box by my back gate.""",
PW, ["redirect delivery", "rebook missed delivery", "track parcel", "schedule pickup", "cancel shipment",
     "proof of delivery request", "report lost parcel", "driver complaint", "customs charge query"],
"redirect delivery", 2),

# I24 seller wants the photo/signature -> proof of delivery request
I("in_pw_seller_pod",
POLICY + """

Parcelwise Business - account message
Sender: Fernhollow Ceramics (business account 77120) | Tracking: PW-5520-1184-GB | Received: Monday 11:05

Hello. One of our customers, Ms Adaeze Nwosu, says she never received the mug set we sent her last week. Your tracking shows it as delivered on Thursday at 16:40. Before we decide whether to refund her or send a replacement, could you send us whatever the driver recorded at the door: a photo, a signature, or the GPS location? We're not reporting it lost ourselves at this stage, we just need to see the evidence.

Thanks, Fern at Fernhollow""",
PW, ["proof of delivery request", "report lost parcel", "track parcel", "driver complaint", "report damaged parcel",
     "schedule pickup", "customs charge query", "redirect delivery", "cancel shipment", "rebook missed delivery"],
"proof of delivery request", 2),

# I26 switching provider, keep number -> port out; twin: new number, end service -> cancel contract
I("in_km_orca_switch",
POLICY + """

Kestrel Mobile - chat transcript (customer side)
Customer: Lindiwe Dube | Account: KM-3019-448 | Friday 12:40

Hi. I'm moving to Orca Telecom next week because their plan includes calls to South Africa, where my family is. I want to keep my current mobile number when I move over; I've had it for eleven years and everyone has it. What do I need to get from you so Orca can bring my number across? My contract with you finished in June, so I don't think there's an early-termination fee, but please tell me if there is.""",
KM, ["port number out", "cancel contract", "downgrade plan", "bill dispute", "roaming setup", "unlock device",
     "replace SIM or eSIM", "add a line"], "port number out", 2,
twin=T([("I want to keep my current mobile number when I move over; I've had it for eleven years and everyone has it. What do I need to get from you so Orca can bring my number across?",
         "Orca are giving me a new number and I'm happy to let this one go; I only got it last year. What do I need to do to end my service with you completely?")],
       "cancel contract")),

# I27 calls fine, data dead -> mobile data not working
I("in_km_data",
POLICY + """

Kestrel Mobile - community forum post (escalated to support)
User: pete_marsh_77 | Posted: Tuesday 18:25

Since the phone updated on Sunday night, mobile internet has stopped working completely. I've got full bars, I can make and receive calls, and texts go through fine, but nothing loads over 4G or 5G anywhere: at home, in town, at work on the other side of Hollins. Wi-Fi works normally. I've restarted the phone about ten times and toggled airplane mode. My colleague is also on Kestrel and hers works fine in the same office, so I don't think it's a mast problem.""",
KM, ["mobile data not working", "no signal or outage", "roaming setup", "replace SIM or eSIM", "unlock device",
     "upgrade plan", "bill dispute", "block lost or stolen phone", "port number out", "cancel contract",
     "add a line", "downgrade plan"], "mobile data not working", 1),

# I28 stolen phone, wants it barred -> block lost or stolen phone (not replace SIM)
I("in_km_stolen_phone",
POLICY + """

Kestrel Mobile - call-back request (typed by customer on a friend's phone)
Customer: Anaïs Leclerc | Account: KM-5520-091 | Submitted: Saturday 13:55

My phone was taken off the table at a café on Market Square about an hour ago while I was paying. The police have given me a crime reference (CR-2210-44). Please make sure nobody can use the phone or my number: no calls, no data, nothing charged to my account. I'll sort out a new handset and a SIM myself next week once the insurance claim is in. Please call me back on this number, which is my friend Juliette's.""",
KM, ["block lost or stolen phone", "replace SIM or eSIM", "cancel contract", "bill dispute", "unlock device",
     "no signal or outage", "add a line"], "block lost or stolen phone", 2),

# I29 phishing site on Stackhouse -> report abuse (not site down, not SSL)
I("in_sc_phishing",
POLICY + """

Stackhouse Cloud - support ticket
Submitted by: Security team, Brannock Building Society (not a Stackhouse customer) | Priority: high

A site hosted on your network, hollin-brannock-secure.net (IP in your range 203.0.113.0/24), is serving a copy of our online-banking login page and harvesting customer passwords. Our customers have received text messages linking to it since this morning. It has a valid SSL certificate, so browsers show a padlock, and it is up and responding normally. We are not your customer and have no account with you. Please take it down as a matter of urgency. Screenshots and message headers attached.""",
SC, ["report abuse", "site down", "SSL certificate problem", "DNS or domain setup", "account access",
     "cancel plan", "billing charge query"], "report abuse", 2),

# I30 certificate error, site up -> SSL certificate problem
I("in_sc_cert_warning",
POLICY + """

Stackhouse Cloud - support ticket
Customer: Birchwood Bakery Ltd (plan: Starter) | Submitted by: Hamish Grant | 06:58, Monday

Since about 6 this morning, customers visiting birchwoodbakery.example get a big red "Your connection is not private" warning. If they click through the warning, the site loads fine and orders go through, and the admin panel works. Nothing has been changed on our side; we didn't touch the domain settings. We get most of our pre-orders on Monday mornings, so we'd like this sorted as soon as possible. I'm not sure if it's related, but last month's invoice was a bit higher than usual.""",
SC, ["SSL certificate problem", "site down", "DNS or domain setup", "billing charge query", "account access",
     "restore from backup", "increase resource quota", "report abuse", "migrate site in", "cancel plan"],
"SSL certificate problem", 2),
]
