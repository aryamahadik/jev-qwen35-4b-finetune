"""nli_c / chats, support tickets and forms."""
from _lib import C, Y, T, NLI3, REL5, ESTABLISH, FACTIVE, PRESUP, IMPLICATIVE, QUANT, EXCEPT, MODAL, COND, REPORTED

CHAT = ("Chat evidence", "what a participant writes is that participant's claim; a line posted by a bot or system log records what the system did.")

ITEMS = [
# ------------------------------------------------------------------ ct01
# why: only Jonas says he is "pretty sure" it was rolled back; no bot line -> not established -> no.
#      Twin: the deploy bot posts "rollback of 4.2 completed" -> yes.
Y("ct01", "Does the transcript establish that release 4.2 of the checkout service was rolled back?",
"""
#checkout-oncall — Thursday 17 September

[13:48] Mira Castell: checkout error rate is at 3.1% since the 4.2 release went out at 13:20. normal is under 0.5%
[13:50] Jonas Albrecht: looking. the new tax module is throwing on addresses without a postcode
[13:55] Mira Castell: do we roll back or hotfix?
[13:57] Jonas Albrecht: roll back, the hotfix needs a schema change
[14:04] Jonas Albrecht: I kicked it off from my laptop but my VPN dropped halfway, I'm pretty sure it got rolled back though
[14:06] Mira Castell: error rate still 2.8% on my dashboard, but it lags about ten minutes
[14:07] deploy-bot: status for checkout-service — no rollback recorded in the last hour; current version 4.2
[14:09] Jonas Albrecht: reconnecting now, will check the pipeline
[14:12] Priyam Das: joining. customer support has 40 tickets about failed payments, mostly overseas addresses
[14:13] Mira Castell: ok, let's post a status page update either way
""",
[ESTABLISH, CHAT], 0, 2,
twin=T([("[14:07] deploy-bot: status for checkout-service — no rollback recorded in the last hour; current version 4.2",
         "[14:07] deploy-bot: rollback of checkout-service 4.2 completed at 14:05; current version 4.1.3")], 1)),

# ------------------------------------------------------------------ ct02
# why: the misdelivery is only what the customer says; the agent notes no scan data yet ->
#      attributed only. Twin: the courier's GPS scan (agent's own statement of the record) shows
#      delivery to No. 14 instead of No. 41 -> entailed.
C("ct02", 'Hypothesis: "Parcel PX-55812 was delivered to the wrong address." Which description fits the ticket?',
"""
Ticket #HD-208817 — Brisklane Couriers — Customer Support
Channel: phone, then email
Agent: Tove Lindahl
Status: pending courier investigation

Summary of contact (Tuesday 22 September, 10:15):
Ms Farida Oyelaran called about parcel PX-55812 (a laptop, declared value £1,149). The tracking page shows it as "delivered 21 Sept, 16:42, left with neighbour". Ms Oyelaran says the parcel was delivered to the wrong address: she lives at 41 Elm Row, and she has asked both of her neighbours, neither of whom took it in. She says she was at home all afternoon and nobody knocked.

Actions taken:
- Opened a lost-in-transit investigation with the depot (ref LIT-7740).
- Requested the driver's photo and GPS scan for the delivery. These usually take 24–48 hours to arrive from the depot.
- Explained the claims process and sent the claim form by email.

Next update due: Thursday 24 September by 17:00.

Internal note: the driver on this route is a temporary agency driver who started last week.
""",
REL5, "attributed only", 2,
twin=T([("Requested the driver's photo and GPS scan for the delivery. These usually take 24–48 hours to arrive from the depot.",
         "Checked the driver's GPS scan for the delivery: the parcel was scanned as delivered at 14 Elm Row, not 41 Elm Row.")], "entailed")),

# ------------------------------------------------------------------ ct03
# why: the return date is conditional on the surgery date not moving, which is unresolved ->
#      the form leaves the return date unestablished -> yes. Twin: return date stated
#      unconditionally -> established -> no.
Y("ct03", "Does the leave request leave it unestablished that Samir Aziz will be back at work on 2 November?",
"""
LEAVE REQUEST FORM — Halloway Engineering Ltd (HR-07)

Employee: Samir Aziz          Staff no.: 40218
Team: Structural Design (Line manager: Petra Holm)
Type of leave: Medical leave (planned procedure)

First day of absence: Monday 12 October
Expected return to work: Monday 2 November, unless the hospital moves my surgery date, in which case I will let Petra know the new dates as soon as I have them.
Pre-admission appointment: 5 October (morning only, will make up the hours)

Handover arrangements: My two live projects (Kingsgate footbridge and Alder Park car park) will be covered by Wen Li. I will brief her on 8 October. Drawings are saved in the usual project folders.

Fit note: will be provided by the hospital after the procedure.

Employee signature: S. Aziz        Date: 21 September

Line manager decision: Approved — P. Holm, 22 September. Comment: "Take the time you need. Please keep me posted if the date changes."
""",
[ESTABLISH, COND], 1, 2, role="neg",
twin=T([("Expected return to work: Monday 2 November, unless the hospital moves my surgery date, in which case I will let Petra know the new dates as soon as I have them.",
         "Return to work: Monday 2 November (the procedure took place early, on 14 September, and this is the confirmed date agreed with occupational health).")], 0)),

# ------------------------------------------------------------------ ct04
# why: two charges of £34.99 in September, and these are the only September charges ->
#      £69.98 > £65 -> entailment. Twin: the second charge was declined -> total £34.99 ->
#      "more than £65" is false -> contradiction.
C("ct04", 'Hypothesis: "Mr Karlsson was charged more than £65 in total for his subscription in September." What is its relation to the ticket?',
"""
Ticket #BL-44190 — Lumo Streaming — Billing Support
Agent: Haruto Mori
Opened: 6 October, via in-app chat

Customer: Nils Karlsson (Premium plan, £34.99 per month, billed on the 3rd)

Customer's message: "I've been charged twice for September. Please refund the extra one."

Agent notes:
Checked the payment log for this account. There are two card payments for the subscription in September: £34.99 on 3 September and £34.99 on 4 September. These are the only subscription charges in September. The duplicate was caused by a known retry fault on 4 September that affected about 1,200 accounts; engineering fixed it on 5 September.

Refund of £34.99 issued to the original card on 6 October (refund ref RF-99017). Customer told that refunds take 3–5 working days to appear.

Also applied a £5 goodwill credit to the account, which will be used against the November bill.

Ticket status: resolved.
""",
NLI3, "entailment", 2,
twin=T([("There are two card payments for the subscription in September: £34.99 on 3 September and £34.99 on 4 September. These are the only subscription charges in September. The duplicate was caused by",
         "There is one card payment for the subscription in September: £34.99 on 3 September. A second attempt on 4 September was declined by the bank, and these are the only September attempts. The second attempt was caused by"),
        ("Refund of £34.99 issued to the original card on 6 October (refund ref RF-99017). Customer told that refunds take 3–5 working days to appear.",
         "No refund is due. Customer shown the declined attempt in the payment log.")], "contradiction")),

# ------------------------------------------------------------------ ct05
# why: "everyone except Bea and Kwesi" is on the Saturday rota -> Lior is on it; Bea is not.
#      Only Lior's Saturday shift is established among the options. Twin: Lior is added to the
#      exceptions -> Lior not on the rota; Saturday count is 5 (base) / 4 (twin), never 6; Sunday
#      names not yet posted -> twin gold "none of these".
C("ct05", "Which one of these statements does the manager's message establish?",
"""
Pinned message in #front-of-house — Saltmarsh Kitchen (posted by Esther Lamb, general manager)

Hi team, the rota for the Harvest Festival weekend (Saturday 3 and Sunday 4 October):

Saturday: everyone on the front-of-house team works the evening service (17:00–23:00) except Bea and Kwesi, who are running our stall at the festival itself from 11:00 to 18:00.

Sunday: brunch service only (10:00–15:00). I need four people. I'll post the Sunday names by Wednesday once I know who's available; please reply in the thread if you can do it.

Front-of-house team this season: Bea, Kwesi, Lior, Nadia, Oscar, Ruth and Tamsin.

Uniform: festival aprons are in the office. Please collect yours before Friday.

Tips from the festival stall will go into the usual tip pool.

Thanks all — it's going to be a busy one!
Esther
""",
[("Lior works Saturday evening", "Lior works the Saturday evening service."),
 ("Bea works Saturday evening", "Bea works the Saturday evening service."),
 ("Kwesi works Sunday brunch", "Kwesi works the Sunday brunch service."),
 ("Nadia works Sunday brunch", "Nadia works the Sunday brunch service."),
 ("six work Saturday evening", "Exactly six people work the Saturday evening service."),
 ("none of these", "The message establishes none of the statements above.")],
"Lior works Saturday evening", 3,
twin=T([("except Bea and Kwesi, who are running our stall", "except Bea, Kwesi and Lior, who are running our stall")], "none of these")),

# ------------------------------------------------------------------ ct06
# why: "returned ... for a second time" presupposes a first return -> yes.
#      Twin: "for the first time" -> no earlier return -> no.
Y("ct06", "Does the ticket establish that the customer had returned a Vortex 700 blender before this return?",
"""
Returns Ticket #RT-31055 — Cobble & Pine Home Store
Agent: Delphine Okonkwo
Date: 15 September

Customer: Ruairi Byrne (loyalty member since 2021)
Product: Vortex 700 high-speed blender, bought in-store at Kilbarron on 2 June

Summary: Mr Byrne returned the blender to the Kilbarron store for a second time on 14 September, saying the motor cuts out after about 20 seconds on high speed. Store staff tested the unit and reproduced the fault. The unit has been sent to the manufacturer's repair centre under warranty (repair ref VX-5530).

Customer request: a full refund instead of a repair.

Agent decision: under our returns policy, refunds after 30 days are at the manager's discretion for items under warranty. Escalated to the store manager, Colm Ahearn, with a recommendation to offer a refund or a different model, given the customer's experience.

Customer informed by email that a decision will follow within five working days.
""",
[ESTABLISH, PRESUP], 1, 2,
twin=T([("returned the blender to the Kilbarron store for a second time on 14 September", "returned the blender to the Kilbarron store for the first time on 14 September"),
        ("given the customer's experience.", "given the length of time the customer had been without a working blender.")], 0)),

# ------------------------------------------------------------------ ct07
# why: the Wednesday visit holds only if the part arrives Tuesday (unresolved) -> conditional only.
#      Twin: the part arrived on Tuesday, so the visit is on Wednesday -> entailed.
C("ct07", 'Hypothesis: "The engineer will visit Ms Petrakis on Wednesday." Choose the description that fits the ticket.',
"""
Service Ticket #SV-66021 — Heatwise Boiler Care
Engineer coordinator: Callum Fry
Updated: Monday 28 September, 16:20

Customer: Eleni Petrakis, 9 Fairholme Gardens
Appliance: Calder 28 combination boiler (installed 2019), covered by the Heatwise Gold plan

Fault: boiler locks out with code E-133 (ignition failure) several times a day. Engineer Joel Hart attended on Friday 25 September, replaced the ignition electrode and found that the gas valve was also faulty.

Parts: gas valve ordered from the manufacturer on Friday. Supplier's estimated delivery: Tuesday 29 September.

Next visit: if the replacement gas valve arrives on Tuesday, the engineer will visit on Wednesday morning (08:00–12:00 slot) to fit it. The customer has been told that the boiler can be reset in the meantime and that a temporary electric heater can be delivered if needed.

Customer vulnerability flag: none recorded.
""",
REL5, "conditional only", 2,
twin=T([("Next visit: if the replacement gas valve arrives on Tuesday, the engineer will visit on Wednesday morning",
         "Next visit: the replacement gas valve arrived on Tuesday, so the engineer will visit on Wednesday morning")], "entailed")),

# ------------------------------------------------------------------ ct08
# why: "should be here by 8" is an expectation; nothing records arrival -> the chat fails to
#      establish it -> yes. Twin: the door-access bot logs the crew's badge-in at 07:46 -> no.
Y("ct08", "Does the chat fail to establish that the cleaning crew arrived at the office before 08:00?",
"""
#office-ops — Monday 21 September

[07:31] Ingrid Fosse: morning! reminder the deep-clean crew from Sparkline is booked for the 3rd floor today before the board meeting at 10
[07:33] Ingrid Fosse: they should be here by 8, per the booking confirmation
[07:40] Theo Nakamura: I'm in already, 3rd floor kitchen is a bit of a disaster after Friday drinks, fyi
[07:52] Ingrid Fosse: 😬 thanks, I'll mention it to them
[07:58] door-access-bot: 3rd floor badge-ins since 07:00 — T. Nakamura (07:38), K. Oduya (07:55)
[08:04] Ingrid Fosse: has anyone seen them at reception?
[08:06] Theo Nakamura: not me, I'm heads down on the board pack
[08:15] Kemi Oduya: the parking bay by the loading door is empty, so no van yet I think
[08:16] Ingrid Fosse: calling Sparkline now
""",
[ESTABLISH, CHAT, MODAL], 1, 2, role="neg",
twin=T([("[07:58] door-access-bot: 3rd floor badge-ins since 07:00 — T. Nakamura (07:38), K. Oduya (07:55)",
         "[07:58] door-access-bot: 3rd floor badge-ins since 07:00 — T. Nakamura (07:38), Sparkline cleaning crew x3 (07:46), K. Oduya (07:55)"),
        ("[08:04] Ingrid Fosse: has anyone seen them at reception?\n[08:06] Theo Nakamura: not me, I'm heads down on the board pack\n[08:15] Kemi Oduya: the parking bay by the loading door is empty, so no van yet I think\n[08:16] Ingrid Fosse: calling Sparkline now",
         "[08:04] Ingrid Fosse: great, they're in. has anyone shown them the kitchen?\n[08:06] Theo Nakamura: not me, I'm heads down on the board pack\n[08:15] Kemi Oduya: I'll go and show them\n[08:16] Ingrid Fosse: thanks Kemi")], 0)),

# ------------------------------------------------------------------ ct09
# why: "Was anyone injured? Not known" -> the form leaves injuries open -> neutral.
#      Twin: "No — the car was empty and nobody else was involved" -> entailment.
C("ct09", 'Given the claim form, how should the hypothesis "Nobody was injured in the incident" be classified?',
"""
MOTOR CLAIM NOTIFICATION — Fairway Mutual Insurance
Policy no.: FM-2210-88341     Policyholder: Adebola Mensah
Vehicle: 2021 Corvan Estate, registration ending 7KX

Date and time of incident: Saturday 19 September, between 14:00 and 16:30
Location: Pay-and-display car park, Harbour Road, Tellmouth

Was the vehicle parked and unattended? Yes
Description: I returned to the car to find the rear bumper and tailgate dented and the rear window cracked. There was no note on the windscreen. A man at the ticket machine said he had seen a white van reversing near my car, but he left before I could take his details.

Were the police informed? Yes — crime ref TL/26/51127
Was anyone injured? Not known — I was not there when it happened.
Third-party details: unknown
Is the vehicle driveable? Yes, but the rear window is taped.

Photos attached: 6
Declaration signed: A. Mensah, 20 September
""",
NLI3, "neutral", 2,
twin=T([("Was anyone injured? Not known — I was not there when it happened.",
         "Was anyone injured? No — the car park attendant who saw it happen confirmed the van driver drove off unhurt, and nobody else was nearby.")], "entailment")),

# ------------------------------------------------------------------ ct10
# why: "Ana escalated the ticket to Ben; he refunded the order" - "he" can only be Ben (Ana and
#      the customer Mrs Obi are referred to as "she"/"her") -> Ben refunded -> yes.
#      Twin: "she refunded the order" -> Ana refunded it -> Ben's refund not established -> no.
Y("ct10", "Does the ticket history establish that Ben Hallett refunded order 77-4031?",
"""
Ticket #WS-90412 — Wicker & Stone Garden Furniture — history view

19 Sep 09:12 — Customer (Mrs Grace Obi): "The rattan sofa arrived with a split frame on the left arm. I'd like a refund rather than a replacement, please."
19 Sep 09:40 — Agent Ana Ferreira: Asked the customer for photos. Mrs Obi sent four photos at 10:05 showing the split frame clearly.
19 Sep 11:20 — Ana Ferreira: Refunds over £500 need a team lead, so Ana escalated the ticket to Ben Hallett, team lead. Collection of the sofa booked for 24 September.
19 Sep 15:02 — Ben Hallett reviewed the photos. As the damage was clearly caused in transit, he refunded order 77-4031 in full (£749) and raised a claim against the carrier.
19 Sep 15:10 — Automated email sent to customer: "Your refund has been processed."
24 Sep 12:31 — Carrier confirms collection completed.
24 Sep 12:40 — Ticket closed.
""",
[ESTABLISH, ("Pronoun reference", "a pronoun refers to the person the passage makes the only suitable antecedent.")], 1, 2,
twin=T([("19 Sep 15:02 — Ben Hallett reviewed the photos. As the damage was clearly caused in transit, he refunded order 77-4031 in full (£749) and raised a claim against the carrier.",
         "19 Sep 15:02 — Ben Hallett was on leave, so the ticket went back to Ana. As the damage was clearly caused in transit, she refunded order 77-4031 in full (£749) under a one-off approval from the duty manager and raised a claim against the carrier.")], 0)),

# ------------------------------------------------------------------ ct11
# why: change CHG-5512: approved 16 Sep; window 20 Sep 01:00-03:00; implemented 01:10; health check
#      failed 01:40; rolled back 01:55; rescheduled "provisionally" for 27 Sep. Established:
#      "rolled back within the window". Twin: rollback completed 03:25 -> after window closed ->
#      "rolled back after the window".
C("ct11", "Which one of these statements does the change record establish?",
"""
CHANGE RECORD CHG-5512 — Northvale Building Society IT
Title: Upgrade of the branch teller application from version 7.4 to 7.5
Change type: Normal       Risk: Medium
Approved by Change Advisory Board: 16 September

Planned window: Sunday 20 September, 01:00–03:00 (branches closed)

Implementation log:
01:10 — Upgrade script started on the application servers.
01:32 — Upgrade script completed.
01:40 — Post-upgrade health check failed: teller terminals at the test branch could not print passbooks.
01:45 — Decision by the change manager, Oona Marsh, to roll back.
01:55 — Rollback completed; version 7.4 restored; health check passed.

Outcome: Unsuccessful — rolled back. Branch services were not affected.

Follow-up: vendor ticket raised about the passbook printer driver. The change will provisionally be attempted again on Sunday 27 September, subject to the vendor's fix and fresh CAB approval.
""",
[("rolled back within the window", "The rollback was completed before the planned window closed."),
 ("rolled back after the window", "The rollback was completed after the planned window closed."),
 ("upgrade succeeded", "Version 7.5 is in service after the change."),
 ("started before the window", "The upgrade script started before the planned window opened."),
 ("re-run on 27 September", "The change will be attempted again on 27 September."),
 ("none of these", "The record establishes none of the statements above.")],
"rolled back within the window", 2,
twin=T([("01:55 — Rollback completed; version 7.4 restored; health check passed.", "03:25 — Rollback completed; version 7.4 restored; health check passed.")], "rolled back after the window")),

# ------------------------------------------------------------------ ct12
# why: 40 seats; 33 confirmed + 5 maybes = 38 <= 40 -> enough seats is established -> "fail to
#      establish?" = no. Twin: 37 confirmed + 5 = 42 > 40 -> not guaranteed -> yes.
Y("ct12", "Does the chat fail to establish that the coach has enough seats for everyone who has confirmed plus everyone who is a maybe?",
"""
Group chat: Fernhill Ramblers — Autumn coach trip 🚌

Moira (organiser): Coach for Saturday's trip to Crag Hollow is booked — 40 passenger seats, no standing allowed.
Moira (organiser): Current list: 33 confirmed and paid, 5 maybes who haven't paid yet. Nobody else has been in touch.
Dev: Put me down as confirmed, I paid last night (already counted? 🙂)
Moira (organiser): Yes Dev, you're in the 33.
Hana: Is there a toilet on the coach?
Moira (organiser): Yes. And we stop at the Beacon Café on the way.
Colin: My neighbour might come, but only if the weather's decent — can she be a maybe?
Moira (organiser): She's already one of the 5, she messaged me this morning.
Hana: 👍
Moira (organiser): Payment deadline for maybes is Thursday at 18:00. After that, seats go to the waiting list.
""",
[ESTABLISH, ("Enough seats", "the number of seats is at least the number of people counted.")], 0, 2, role="neg",
twin=T([("Current list: 33 confirmed and paid", "Current list: 37 confirmed and paid"), ("you're in the 33.", "you're in the 37.")], 1)),

# ------------------------------------------------------------------ ct13
# why: the agent (writer) states the warranty does not cover accidental damage -> the hypothesis
#      is contradicted. Twin: the agent only records the customer's belief and asks the warranty
#      team -> attributed only.
C("ct13", 'Hypothesis: "The Aurel X5 warranty covers accidental damage." Which description fits the ticket?',
"""
Ticket #AU-71730 — Aurel Audio Customer Care
Agent: Beatriz Nunes
Date: 26 September

Customer: Kasper Lund
Product: Aurel X5 wireless headphones (bought 11 March, online store)

Issue: The customer dropped the headphones on a tiled floor and the right hinge snapped. He sent two photos. The customer believes the warranty covers accidental damage because the product page mentions "two years' peace of mind". The two-year warranty covers manufacturing defects only; accidental damage is not covered.

Options offered:
1. Paid hinge repair at the Lisbon service centre: €39 plus return postage.
2. 20% discount code on a new pair (code valid 30 days).

Customer response: considering option 1; will reply by email.

Follow-up: product-page wording flagged to the web team, as it has caused confusion in at least three other tickets this month.
""",
REL5, "contradicted", 2,
twin=T([("The two-year warranty covers manufacturing defects only; accidental damage is not covered.",
         "I have asked the warranty team to confirm exactly what the two-year cover includes.")], "attributed only")),

# ------------------------------------------------------------------ ct14
# why: counterfactual "If you had registered ... within 30 days, the extended warranty would have
#      applied" presupposes she did not register in time -> yes. Twin: "Because you registered ...
#      within 30 days, the extended warranty applies" -> no.
Y("ct14", "Does the reply establish that the customer did not register her mower within 30 days of purchase?",
"""
Email reply — Ticket #GM-52207 — Greenmere Garden Machinery

Dear Ms Varga,

Thank you for your message about your Greenmere RM-46 lawnmower (serial 46-208813), bought from Hollins Garden Centre on 12 April 2024, which no longer starts.

Our standard warranty on the RM-46 is two years from the date of purchase and therefore ended on 12 April 2026. If you had registered the mower on our website within 30 days of purchase, the extended warranty would have applied, giving three years' cover in total.

We can still help. An approved service agent near you, Kelso Mowers in Tarnbury, can inspect the mower for a fixed fee of £35, which is deducted from the repair cost if you go ahead. The most common cause of this fault is a blocked carburettor, which usually costs between £60 and £90 to fix.

Please reply if you would like us to arrange the inspection.

Kind regards,
Rhona Tait
Customer Service, Greenmere Garden Machinery
""",
[ESTABLISH, COND], 1, 3,
twin=T([("Our standard warranty on the RM-46 is two years from the date of purchase and therefore ended on 12 April 2026. If you had registered the mower on our website within 30 days of purchase, the extended warranty would have applied, giving three years' cover in total.\n\nWe can still help. An approved service agent near you, Kelso Mowers in Tarnbury, can inspect the mower for a fixed fee of £35, which is deducted from the repair cost if you go ahead.",
         "Our standard warranty on the RM-46 is two years from the date of purchase. Because you registered the mower on our website within 30 days of purchase, the extended warranty applies, giving three years' cover in total, until 12 April 2027.\n\nAn approved service agent near you, Kelso Mowers in Tarnbury, can inspect and repair the mower free of charge under the extended warranty.")], 0)),

# ------------------------------------------------------------------ ct15
# why: "everyone on the team except Mo and Tilly will be in the office"; Rashid is on the team
#      list -> in the office -> entailment. Twin: Rashid is one of the exceptions, at the Leeds
#      client site -> not in the office -> contradiction.
C("ct15", 'Hypothesis: "Rashid will be in the Carden Street office on Thursday." What is the relation between the post and the hypothesis?',
"""
Team channel post — Brightfold Analytics, Client Insights team
Posted by: Harriet Owusu (team lead), Monday 28 September, 09:05

Hi all — quick logistics for Thursday 1 October.

Everyone on the team except Mo and Tilly will be in the Carden Street office on Thursday for the quarterly planning day; the two of them are at the Leeds client site all day for the Brambleton workshop.

Team list for reference: Mo, Tilly, Rashid, Signe, Graham, Noor and me.

Planning day runs 09:30–16:00 in Room 4B, with lunch provided (please add dietary needs to the sheet by Tuesday). We'll dial Mo and Tilly in for the last half hour so they can share how the workshop went.

Parking at Carden Street is limited on Thursdays because of the building's fire drill; the multi-storey on Tanner Lane is the best option.

Thanks!
Harriet
""",
NLI3, "entailment", 2,
twin=T([("except Mo and Tilly will be in the Carden Street office on Thursday for the quarterly planning day; the two of them are at the Leeds client site",
         "except Mo, Tilly and Rashid will be in the Carden Street office on Thursday for the quarterly planning day; the three of them are at the Leeds client site")], "contradiction")),

# ------------------------------------------------------------------ ct16
# why: "the customer had already opened a chargeback before the refund was issued" establishes
#      the order -> "leave unestablished?" = no. Twin: the ticket says the timing relative to the
#      refund cannot be seen -> yes.
Y("ct16", "Does the ticket leave it unestablished whether the chargeback was opened before the refund was issued?",
"""
Payments Dispute Ticket #PD-12087 — Orla & Finch Online
Handler: Mateus Ribeiro, Payments Team
Date: 30 September

Order: OF-558210 — two linen duvet sets, £212.00, paid by card on 2 September.

Background: The customer, Mr Idris Vale, contacted customer service on 14 September to say that one of the duvet sets had arrived with a torn seam. Customer service agreed a full refund of £212.00 on 18 September, and the refund was issued to the card on 19 September.

Dispute: On 25 September we received notice from the card processor of a chargeback for £212.00 on the same order. The customer had already opened the chargeback with his bank on 16 September, before the refund was issued.

Risk: If both the refund and the chargeback are paid out, the customer would receive £424.00 in total.

Action: Evidence of the refund (processor ref RFD-40911) submitted to the card processor today so that the chargeback can be reversed. Customer emailed to explain.

Status: awaiting processor decision (usually 10–15 working days).
""",
[ESTABLISH, ("Temporal order", "a passage establishes that A happened before B only if it gives times or order words that fix the sequence.")], 0, 2, role="neg",
twin=T([("The customer had already opened the chargeback with his bank on 16 September, before the refund was issued.",
         "The processor notice does not say when the customer opened the chargeback with his bank.")], 1)),

# ------------------------------------------------------------------ ct17
# why: mileage 146 x 0.45 = 65.70; parking 8.50; lunch 9.80 -> total 84.00. Under the £90 cap
#      for day trips without receipts approval. Established: "total under £90". Also check:
#      mileage > parking+lunch (65.70 > 18.30) is not an option. Twin: 186 miles -> 83.70 + 18.30
#      = 102.00 -> "total over £100".
C("ct17", "Which one of these statements does the expense form establish?",
"""
EXPENSE CLAIM — Rowanbank District Council (Form FIN-12)

Claimant: Tobias Engel, Environmental Health Officer
Cost centre: EH-204
Purpose: food-hygiene inspections at three premises in Ashcombe and Lower Wick
Date of travel: Tuesday 15 September

Mileage (own car, business insurance confirmed): 146 miles at 45p per mile
Parking: £8.50 (Ashcombe Market car park, receipt attached)
Subsistence: lunch £9.80 (receipt attached)
Other: none

Total claimed: calculated automatically on submission

Declaration: I confirm that these expenses were wholly incurred on council business and have not been claimed elsewhere.
Signed: T. Engel, 16 September

Approver: Lucy Stavrou, Environmental Health Manager — approval pending
""",
[("total under £90", "The total of the amounts claimed is less than £90."),
 ("total between £90 and £100", "The total of the amounts claimed is at least £90 and no more than £100."),
 ("total over £100", "The total of the amounts claimed is more than £100."),
 ("claim approved", "The claim has been approved."),
 ("no receipts attached", "No receipts are attached to the claim."),
 ("none of these", "The form establishes none of the statements above.")],
"total under £90", 2,
twin=T([("146 miles at 45p per mile", "186 miles at 45p per mile")], "total over £100")),
]
