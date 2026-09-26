"""intent_c / reviews and customer-service chats (Oriel Reviews, Staywise, Pantry & Pan delivery, Ledgerly bank)."""
from _lib import C, Y, T, INTENT, TARGET, pick


def I(*n):
    return pick(INTENT, *n)


def TG(*n):
    return pick(TARGET, *n)


ITEMS = [
# ------------------------------------------------------------------ rv01
# why: plain dissatisfaction with the room and breakfast, no action asked -> complain.
# twin: adds a personal slur-free insult of the named night manager; tagging rule puts insult above other intents.
C("rv01", "Using the tagging rule, what intent should be tagged for the review?",
"""
Staywise — review of The Anchor Inn, Marrowby (2 stars), posted by "DerekT", stayed 2 nights in September

"Room 214 smelled of damp from the moment we opened the door, the shower only ran cold after 7 a.m., and breakfast finished at 8:30 on a Sunday, which nobody told us at check-in. The bed was comfortable and the location is handy for the harbour. Two stars."

Tagging rule for review moderators: tag one intent; if a review insults a named or identifiable member of staff, tag that above any other intent except a threat.

Hotel response: none yet.
Stay dates: 13–15 September. Rate paid: £168 for two nights.
""",
I("complain", "insult an individual", "request", "criticise an idea or policy", "praise", "threaten",
  "hyperbole", "none of these"),
"complain", 2,
twin=T([("The bed was comfortable and the location is handy for the harbour.",
         "The night manager, Brian, is a smug little weasel who should never be let near a customer again.")], "insult an individual")),

# ------------------------------------------------------------------ rv02
# why: telling the Chamber of Commerce about one's experience is a lawful step -> not a threat.
# twin: implies damage to the owner's van unless refunded -> threat.
Y("rv02", "Is the customer's message a threat?",
"""
Pantry & Pan — customer chat transcript, order #PP-58120 (catering tray, £184)

Customer (Mrs H. Obi): The tray arrived 90 minutes late for my mother's 80th and half the sandwiches were soggy. Your agent yesterday promised a callback that never came. Refund me by Friday. If I don't hear back, I'll be telling everyone at the Marrowby Chamber of Commerce exactly how you treat customers, and I'll post the photos on Oriel Reviews.

Agent (Callum): I'm very sorry, Mrs Obi. I've escalated this to our catering manager.

Escalation note: customer has ordered 14 times since 2024; no previous disputes.
Pantry & Pan policy: refunds for late catering orders are assessed by the catering manager within 5 working days.
""",
[("Threat", "a statement that seriously implies unlawful harm or intimidation to a person, their safety, property or livelihood."),
 ("Lawful step", "announcing a complaint, honest review, report to a trade body or legal claim; this is not a threat.")],
0, 2,
twin=T([("If I don't hear back, I'll be telling everyone at the Marrowby Chamber of Commerce exactly how you treat customers, and I'll post the photos on Oriel Reviews.",
         "If I don't hear back, I know where your owner parks that white van on Quay Street, and it won't have four tyres by Saturday.")], 1)),

# ------------------------------------------------------------------ rv03
# why: the pigeon joke frames a hint that the courier should bring the order -> request is the main point.
# twin: the order turned up and she is just sharing the funny moment -> joke without a target.
C("rv03", "What is the main intent of the customer's chat message?",
"""
Pantry & Pan — customer chat, order #PP-61277 (lamb curry, garlic naan), Friday 19:52

App status at 19:10: "Delivered — left at door".

Customer (Jess Kowal): "Hi! The app says my order was left at my door 40 minutes ago, but the only thing on my doorstep is a very confused pigeon. I don't think he's got my curry, he looks guilty but not that guilty. If a courier happened to be passing Flat 3, 18 Birch Row with a lamb curry, that would honestly make my week. 🐦"

Agent: typing…
Account: 31 orders, no previous missing-item claims.
Agent guidance: respond within 3 minutes; missing-order claims are checked against the courier's GPS trace. Courier GPS for this order shows a stop outside 18 Birch Row at 19:09.
""",
I("request", "complain", "joke without a target", "hyperbole", "insult an individual", "threaten",
  "report someone else's words", "praise", "none of these"),
"request", 2,
twin=T([("The app says my order was left at my door 40 minutes ago, but the only thing on my doorstep is a very confused pigeon. I don't think he's got my curry, he looks guilty but not that guilty. If a courier happened to be passing Flat 3, 18 Birch Row with a lamb curry, that would honestly make my week. 🐦",
         "Curry's here! When I opened the door there was a very confused pigeon sitting next to the bag, guarding it like a bouncer. I've named him Naan. 🐦"),
        ("App status at 19:10: \"Delivered — left at door\".", "App status at 19:10: \"Delivered — left at door\" (customer confirmed receipt at 19:15).")],
 "joke without a target")),

# ------------------------------------------------------------------ rv04
# why: the reviewer reports the waiter's discriminatory words and left in protest -> free of intent to demean (yes).
# twin: calls it the best service all year -> approves the exclusion of hijab-wearers -> not free.
Y("rv04", "Is the review free of any intent to demean a group?",
"""
Oriel Reviews — review of Casa Verlane, Dunlow (1 star), posted by "fenwick_foodie"

"Booked for four at 8pm. While we were waiting to be seated, the waiter told the couple ahead of us 'we don't serve your sort here' after looking at the woman's hijab. They were turned away even though half the tables were empty. We left without ordering."

Photos: none.
Business response: "We are investigating this with our staff."
Oriel moderator note: review flagged by the business as "defamatory".
Reviewer profile: 64 reviews since 2021, average rating 3.9. Casa Verlane has 212 reviews on Oriel with an average of 4.2.
""",
[("Intent to demean a group", "the reviewer's own words belittle, or approve of treating people badly because of, their religion, ethnicity or similar trait."),
 ("Reporting discrimination", "describing someone else's discriminatory words or acts without endorsing them.")],
1, 2, role="neg",
twin=T([("We left without ordering.\"", "Best service I've had all year. Five stars from me.\""),
        ("(1 star)", "(5 stars)")], 0)),

# ------------------------------------------------------------------ rv05
# why: the negative remarks are all about the loyalty scheme's terms -> an idea, policy or product.
# twin: the remarks are about one identifiable barista -> a specific third person.
C("rv05", "Who or what is the target of the reviewer's negative remarks?",
"""
Oriel Reviews — review of Bramble & Bean café, Esker Falls (2 stars), posted by "morningperson_mo"

"The coffee is still good, but the new loyalty scheme is a con. You now need 400 points for a free coffee, which works out at about 45 drinks, and the points expire after 30 days, so unless you drink two a day you'll never get one. The old stamp card gave you a free drink after nine. Bring it back."

The review is addressed to other customers; the café replied: "Thanks for the feedback, we're reviewing the scheme."
Reviewer profile: 19 reviews, mostly of cafés in Esker Falls. Bramble & Bean has an average rating of 4.4 from 380 reviews.
""",
TG("an idea, policy or product", "a specific third person", "the addressee", "a group", "the speaker", "no one"),
"an idea, policy or product", 2,
twin=T([("but the new loyalty scheme is a con. You now need 400 points for a free coffee, which works out at about 45 drinks, and the points expire after 30 days, so unless you drink two a day you'll never get one. The old stamp card gave you a free drink after nine. Bring it back.",
         "but the new barista on weekends, the tall one with the nose ring, is a con artist. He short-changed me twice and then smirked when I counted it. Keep an eye on him.")],
 "a specific third person")),

# ------------------------------------------------------------------ rv06
# why: the "five stars" and "loved" are sarcastic; every detail is a failure and she "can't wait to never return" -> complain (sarcastically), not praise.
C("rv06", "Which intent does the review express?",
"""
Oriel Reviews — review of The Gilded Spoon, Marrowby (5 stars), posted by "annika_eats"

"Five stars. Loved waiting three hours for a table we'd booked a month ago; it really gave me time to reflect on my life choices. The cold soup (it was meant to be hot) was a bold artistic statement. The waiter vanishing for 50 minutes kept the mystery alive. Charging us £12 for 'table service' was the cherry on top. Can't wait to never come back."

Oriel note: the star rating field defaults to 5 on the mobile app unless changed.
Business response: none.
Reviewer profile: 120 reviews, average rating given 3.1.
""",
I("complain", "praise", "insult an individual", "hyperbole", "request", "joke without a target",
  "threaten", "none of these"),
"complain", 3),

# ------------------------------------------------------------------ rv07
# why: a polite apology and refund -> no intent to offend.
# twin: "manage to read a menu… bless you" is condescending sarcasm aimed at the reviewer -> intent to offend.
Y("rv07", "Did the owner intend to offend the reviewer?",
"""
Oriel Reviews — review of Harbour Grill, Esker Falls (2 stars), by "Mr G. Pell"
"Lamb was overcooked and the waiter didn't mention it was served well done. Disappointing for £26."

Owner response (posted by "Harbour Grill — Owner", two days later):
"Thank you for your feedback, Mr Pell. We're sorry the lamb wasn't cooked the way you wanted. Our menu does list it as slow-roasted and served well done, but our staff should have checked with you. We've refunded the main course to your card."

Mr Pell later edited his review to 3 stars.
Harbour Grill has 96 reviews on Oriel, average 4.1.
""",
[("Intent to offend", "the speaker means their words to belittle, mock or upset the person addressed."),
 ("Condescension", "talking down to someone as though they were foolish, often through mock-polite wording.")],
0, 2,
twin=T([("Our menu does list it as slow-roasted and served well done, but our staff should have checked with you. We've refunded the main course to your card.",
         "Our menu does list it as slow-roasted and served well done, so perhaps next time you could manage to read a menu before ordering, bless you."),
        ("Mr Pell later edited his review to 3 stars.", "Mr Pell later edited his review to 1 star.")], 1)),

# ------------------------------------------------------------------ rv08
# why: "great food for a place run by women" is a backhanded compliment that belittles women -> demean a group.
# twin: "for a place that only opened last month" -> sincere praise.
C("rv08", "What is the intent of the review?",
"""
Oriel Reviews — review of Sorrel Kitchen, Dunlow (4 stars), posted by "ian_h_eats"

"Honestly great food for a place run by women. The pork belly was crisp, the portions are big and the lemon tart is the best I've had in the county. Service was quick even on a busy Saturday. Would come back."

Background: Sorrel Kitchen is owned and run by two chefs, Mae Tran and Rosa Ilić.
Moderation guideline: if a review contains any remark belittling a group, tag that intent above any other.
Business response: "Thanks for coming in."
Reports on the review: 2.
Reviewer profile: 12 reviews.
""",
I("demean a group", "praise", "insult an individual", "joke without a target", "complain", "coded attack on a group",
  "criticise an idea or policy", "friendly banter", "none of these"),
"demean a group", 3,
twin=T([("Honestly great food for a place run by women.", "Honestly great food for a place that only opened last month.")], "praise")),

# ------------------------------------------------------------------ rv09
# why: blames staff being foreign for not understanding -> offensive to a group (nationality/ethnicity).
# twin: blames a broken card machine -> not offensive.
Y("rv09", "Is the review offensive to a group?",
"""
Oriel Reviews — review of QuickFix Phone Repair, Marrowby (1 star), posted by "craig_d_1979"

"Went in to get a cracked screen replaced on a Saturday. The staff were clearly all foreign and couldn't understand a simple order, so I waited 40 minutes for nothing. Left without the repair. Went to the shop on the high street instead and was sorted in half an hour."

Business response: "We're sorry for the wait. Our Saturday team speaks English, Polish and Tamil and is happy to help."
Reviewer profile: 7 reviews since 2023, all of phone and electronics shops. QuickFix Phone Repair has an average rating of 4.5 from 210 reviews.
""",
[("Offensive to a group", "the message blames or belittles people because of nationality, ethnicity or a similar shared trait."),
 ("Service complaint", "dissatisfaction with waiting times, equipment or outcomes that does not belittle a group.")],
1, 2,
twin=T([("The staff were clearly all foreign and couldn't understand a simple order, so I waited 40 minutes for nothing.",
         "The card machine was down and nobody could take payment for a simple order, so I waited 40 minutes for nothing.")], 0)),

# ------------------------------------------------------------------ rv10
# why: a chargeback and small-claims court are lawful steps; the main point is getting the refund -> request.
# twin: bricks through van windscreens -> threaten.
C("rv10", "What is the main intent of the customer's message?",
"""
Coldmere Appliances — customer email, case CA-22714

"Hello,

I ordered one Frostline FX-60 fridge freezer on 2 September (order CM-88104). My bank statement shows two payments of £649 on 3 September. I have one fridge. I've phoned twice (4 and 11 September) and been told both times that it would be 'looked into'.

Refund the duplicate £649 within 7 days or I will file a chargeback with my bank and a claim at the small claims court.

Regards,
Nia Probert"

Attachments: bank statement extract, order confirmation.
Coldmere Appliances policy: duplicate payments are refunded within 10 working days of being confirmed by the payments team.
""",
I("request", "threaten", "complain", "insult an individual", "hyperbole", "criticise an idea or policy",
  "report someone else's words", "none of these"),
"request", 2,
twin=T([("or I will file a chargeback with my bank and a claim at the small claims court.",
         "or I'll come down to your Dunlow depot and put a brick through every van windscreen in the yard.")], "threaten")),

# ------------------------------------------------------------------ rv11
# why: a self-described fat woman celebrating jeans "for us fat girls" -> free of intent to offend (yes).
# twin: mocks other shoppers' bodies -> not free.
Y("rv11", "Is the review free of any intent to offend?",
"""
Oriel Reviews — review of the "Harbour Straight" jeans by Loomwell (5 stars), posted by "curvy_carys"

"Finally a brand that makes jeans for us fat girls with actual thighs! I'm a size 22 and I've given up on jeans for years. These have a proper rise, the fabric has stretch without going baggy by lunchtime, and the pockets hold a phone. Ordered a second pair in black."

Reviewer profile: "plus-size and proud, reviewing clothes that actually fit".
Helpful votes: 212.
Loomwell sizes run from 6 to 28. The product page shows the jeans on three models of different sizes.
""",
[("Intent to offend", "the speaker means their words to belittle, mock or upset a person or group."),
 ("Self-description", "a speaker describing their own body or identity in plain terms, including words others sometimes use unkindly.")],
1, 2, role="neg",
twin=T([("\"Finally a brand that makes jeans for us fat girls with actual thighs! I'm a size 22 and I've given up on jeans for years.",
         "\"Shame the shop was full of fat girls squeezing into jeans they've no business wearing, it put me right off. I'm a size 8 and I've never had trouble finding jeans."),
        ("Reviewer profile: \"plus-size and proud, reviewing clothes that actually fit\".", "Reviewer profile: \"honest reviews, no filter\".")], 0)),

# ------------------------------------------------------------------ rv12
# why: the reviewer relays the comedian's material and says she walked out; she does not adopt it -> report someone else's words.
# twin: she agrees with the joke and adds her own claim about Polish people -> demean a group.
C("rv12", "What is the main intent of the review?",
"""
Oriel Reviews — review of The Laughing Gull comedy club, Marrowby (2 stars), posted by "ella_p"

"The two openers were sharp and properly funny. Then the headliner, Rick Danvers, did twenty minutes of jokes about Polish people all being thieves, including a bit where he pretended to nick a woman's handbag in the front row because of her accent. Half the room laughed. I walked out."

Business response: "Our comedians' views are their own."
Helpful votes: 88.
Reviewer profile: 41 reviews of venues in Marrowby, average rating 3.8. The Laughing Gull hosts comedy nights every Friday and Saturday.
""",
I("report someone else's words", "demean a group", "praise", "insult an individual", "criticise an idea or policy",
  "coded attack on a group", "joke without a target", "request", "none of these"),
"report someone else's words", 3,
twin=T([("Half the room laughed. I walked out.\"",
         "Half the room laughed, and so did I, because he's right — every Polish lad I've hired has nicked something from my van.\"")],
 "demean a group")),

# ------------------------------------------------------------------ rv13
# why: "we know where you live now… we'll see you soon" unless the review is removed -> threat.
# twin: a refund and invitation back -> not a threat.
Y("rv13", "Is the business owner's reply a threat?",
"""
Oriel Reviews — review of Kestrel Car Wash, Dunlow (1 star), by "Ms F. Adeyemi"
"They scratched my passenger door with the brush and denied it on camera."

Reply from "Kestrel Car Wash — Owner":
"We've looked up your booking, Ms Adeyemi. We know where you live now. Remove the review or we'll see you soon."

Booking records at Kestrel Car Wash include customers' home addresses for the collection service.
Ms Adeyemi flagged the reply to Oriel the same evening.
Kestrel Car Wash has 58 reviews on Oriel. Oriel rules: businesses may reply once to each review; replies must not harass reviewers.
""",
[("Threat", "a statement, including a veiled one, that seriously implies harm or intimidation to a person, their home or property."),
 ("Business reply", "a response that apologises, explains, disputes the facts or offers a remedy.")],
1, 2,
twin=T([("We know where you live now. Remove the review or we'll see you soon.",
         "We've checked the camera footage, agree the brush caught your door, and have emailed you a repair voucher. We'd welcome you back.")], 0)),

# ------------------------------------------------------------------ rv14
# why: argues against the redesign that hides cancellation -> criticise; the precedence note only applies if a person is insulted.
# twin: calls the named designer a spineless liar -> insult an individual takes precedence.
C("rv14", "What is the main intent of the app review? If an individual is insulted, that takes precedence over any criticism.",
"""
App store review — "Ledgerly: Budget & Bank" (1 star), posted by "sanjay.k"

"The October redesign buried the 'cancel subscription' button four menus deep, under Settings > Account > Plan > Manage > More. Before the update it was one tap from the home screen. Hiding the exit so people keep paying is a dark pattern and it's dishonest design. I've stopped recommending the app to friends."

Developer response: "We've passed this on to our product team."
Helpful votes: 1,033.
Credits page lists the redesign lead as Priti Nair.
The app has 4.1 stars from 88,000 ratings.
""",
I("criticise an idea or policy", "insult an individual", "request", "demean a group", "threaten", "praise",
  "satire", "none of these"),
"criticise an idea or policy", 2,
twin=T([("Hiding the exit so people keep paying is a dark pattern and it's dishonest design.",
         "Whoever did it, Priti Nair according to the credits, is a spineless liar who should be embarrassed to show her face.")],
 "insult an individual")),

# ------------------------------------------------------------------ rv15
# why: "absolute legend… real professional" after the order was thrown over the gate is sarcasm meant to belittle the driver -> yes.
# twin: he ran through rain to the door -> sincere praise -> no.
Y("rv15", "Did the reviewer intend to demean the delivery driver?",
"""
Pantry & Pan — driver rating comment, order #PP-70331, driver "Kemal A."
Rating given: 1 of 5

Comment: "Driver Kemal was an absolute legend — threw my order over the gate and drove off before I'd even reached the door, food everywhere. Real professional."

Order log: delivered 19:42; photo proof shows a bag on the ground inside the gate.
Driver history: 4.8 average over 2,100 deliveries.
Pantry & Pan shows driver comments to the driver and to the support team. The customer has placed 22 orders since March and has rated previous drivers 4 or 5 stars. Weather at 19:40: heavy rain, according to the delivery log.
""",
[("Intent to demean", "the reviewer means their words to belittle or mock the driver."),
 ("Sarcasm", "praise that means the opposite of what it says, judged from the events described and the rating.")],
1, 2,
twin=T([("threw my order over the gate and drove off before I'd even reached the door, food everywhere. Real professional.",
         "ran through a downpour to the door and even waited while I found my keys. Real professional."),
        ("Rating given: 1 of 5", "Rating given: 5 of 5"),
        ("photo proof shows a bag on the ground inside the gate.", "photo proof shows the bag handed over at the door.")], 0)),

# ------------------------------------------------------------------ rv16
# why: a guest mid-stay mentions the radiator stuck on full -> hinted request to fix it.
# twin: the guest has checked out and is only leaving feedback -> complain.
C("rv16", "Which intent best describes the guest's message?",
"""
Staywise — in-app message to The Linden Hotel, Esker Falls, from guest in room 305
Booking: 3 nights, 24–27 September. Message sent: 25 September, 22:10 (guest in residence).

"Hi there, just a small thing — the radiator in 305 seems to be stuck on full and the dial doesn't turn. We're melting a bit 🥵 Otherwise the room is lovely and the view of the river is gorgeous."

Front desk staffing overnight: one receptionist, one porter.
Hotel notes: room 305 had a heating fault logged in March, marked fixed.
The Linden Hotel has 42 rooms; room 305 is on the top floor, facing the river.
""",
I("request", "complain", "hyperbole", "praise", "insult an individual", "threaten", "joke without a target",
  "none of these"),
"request", 2,
twin=T([("Message sent: 25 September, 22:10 (guest in residence).", "Message sent: 29 September, 10:00 (two days after check-out)."),
        ("\"Hi there, just a small thing — the radiator in 305 seems to be stuck on full and the dial doesn't turn. We're melting a bit 🥵 Otherwise the room is lovely and the view of the river is gorgeous.\"",
         "\"Now that we're home: the radiator in 305 was stuck on full our whole stay and the dial didn't turn, so we slept badly all three nights. We're not after anything, just wanted you to know.\"")],
 "complain")),

# ------------------------------------------------------------------ rv17
# why: all negative remarks concern the bank's fraud-freeze rule and its handling -> an idea, policy or product.
C("rv17", "Who or what is the target of the negative remarks in the review?",
"""
Oriel Reviews — review of Ledgerly Bank (1 star), posted by "harriet.w"

"Your fraud team froze my current account for nine days over a single £30 transfer to my own savings account. Nobody on the phone could tell me why, and I was told the rule is that frozen accounts can't be discussed until the review finishes. I couldn't pay rent. A rule that leaves customers unable to pay rent without any explanation is absurd. To be fair, Sophie on the complaints line was kind and did her best."

Bank response: "We're sorry to hear this, please DM us your reference."
""",
TG("an idea, policy or product", "the addressee", "a specific third person", "a group", "the speaker", "no one"),
"an idea, policy or product", 3),
]
