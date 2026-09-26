"""intent_c / community boards and group chats (Pebbleboard neighbourhood app, Classnest school chats, tenants' boards, sports clubs, Kindling dating app, the Dunlow Echo letters page)."""
from _lib import C, Y, T, INTENT, TARGET, pick


def I(*n):
    return pick(INTENT, *n)


def TG(*n):
    return pick(TARGET, *n)


ITEMS = [
# ------------------------------------------------------------------ cm01
# why: "you know, *that* kind of family" about a family from Romania, linked to missing bikes, insinuates the group steals -> offensive to a group.
# twin: says they seem lovely and the thefts are a separate street-wide issue -> not offensive.
Y("cm01", "Is the post offensive to a group?",
"""
Pebbleboard — neighbourhood feed, Alder Row & Coppice Lane
Post by Gail F. (Alder Row), Tuesday 20:15

"Anyone else noticed the new family at no. 9 — you know, *that* kind of family — ever since they moved in, bikes have gone missing. Just saying, lock your sheds."

Earlier in the same thread (Sunday): a neighbour mentioned that the family at no. 9 moved from Romania last month.
Replies: 17. Police community officer comment: "Two bike thefts were reported on this street in August, before anyone moved into no. 9."
Pebbleboard guidelines: posts about crime should describe behaviour, not people's backgrounds.
""",
[("Offensive to a group", "the message belittles people because of ethnicity, nationality or similar trait, including by insinuating that the group is criminal."),
 ("Crime warning", "a neutral alert about thefts that does not blame anyone because of who they are.")],
1, 3,
twin=T([("you know, *that* kind of family — ever since they moved in, bikes have gone missing.",
         "they seem lovely, we had a chat over the fence — anyway, separate thing, bikes have gone missing on the street this month.")], 0)),

# ------------------------------------------------------------------ cm02
# why: pointing out the same five names and pinning the sign-up sheet hints that others should volunteer -> request.
# twin: the rota is full of new names and she thanks everyone -> praise.
C("cm02", "What is the main intent of Nadine's message?",
"""
Classnest — Year 3 (Ms Otieno's class) parents' group, Harlow Primary
Message from Nadine B. (class rep), Monday 08:47

"Morning all ☀️ Just noticing that the rota for the class bake sale has the same five names every term 🙂 There are 28 families in the class. Sign-up sheet's pinned above 🙂"

Pinned: "Bake sale rota — Friday 17 October — 8 slots, 3 filled."
Reactions: 👍 x4, 🙈 x2
Group description: "Info and friendly chat for Year 3 families. Please keep it kind."
The group has 31 members. Nadine has been class rep since Reception and organises the bake sale each term.
""",
I("request", "complain", "insult an individual", "praise", "criticise an idea or policy", "joke without a target",
  "demean a group", "none of these"),
"request", 2,
twin=T([("has the same five names every term 🙂 There are 28 families in the class. Sign-up sheet's pinned above 🙂",
         "has 22 different names this term 🙂 There are 28 families in the class. Thank you all, that's a record!"),
        ("8 slots, 3 filled.", "8 slots, 8 filled.")], "praise")),

# ------------------------------------------------------------------ cm03
# why: reporting to the management company, which tows, is a lawful step -> not a threat.
# twin: "you'll come back to more than a flat tyre" implies damage to the car -> threat.
Y("cm03", "Is the notice a threat?",
"""
Tenants' board — Marl Court (48 flats), photo of a printed notice taped to the bay 14 sign, posted by the board admin

Notice text:
"To whoever keeps parking in bay 14: this bay belongs to flat 22 and is in my lease. I have photos of your plate from three separate nights. Next time I'm reporting it to the management company and they will tow, as the signs at the entrance say."

Admin comment: "Posting so the driver sees it. Please use the visitor bays."
Marl Court parking rules: unauthorised vehicles in allocated bays may be towed by the management company at the owner's cost.
""",
[("Threat", "a statement that seriously implies unlawful harm or intimidation to a person or their property."),
 ("Lawful warning", "saying one will use a proper procedure, such as reporting to a landlord or having a vehicle towed under posted rules.")],
0, 2,
twin=T([("Next time I'm reporting it to the management company and they will tow, as the signs at the entrance say.",
         "Next time you'll come back to more than a flat tyre, and nobody will have seen a thing.")], 1)),

# ------------------------------------------------------------------ cm04
# why: Jaden asked for the clip to go in the chat and found it hilarious -> friendly banter.
# twin: Jaden left in tears and his mum asked the coach not to mention it; the coach mocks him anyway -> insult an individual.
C("cm04", "Which intent best describes the coach's message?",
"""
Classnest — Esker Falls Juniors U12s team chat (parents and players), Sunday 18:30
Message from Coach Dom:

"Great effort Saturday, U12s! 3-3 against the league leaders, proud of every one of you. Special shout-out to Jaden, who scored the most spectacular own goal in league history and then celebrated it like a cup final winner 😂 Video in the thread. We love you Jaden."

Context: after the match, Jaden himself asked the coach to "put it in the group chat, it was hilarious", and his mum posted the first laughing emoji.

Replies: "JADEN 😂😂", Jaden (from his mum's phone): "top bins tho"
""",
I("friendly banter", "insult an individual", "praise", "joke without a target", "self-deprecation", "hyperbole",
  "complain", "none of these"),
"friendly banter", 2,
twin=T([("Context: after the match, Jaden himself asked the coach to \"put it in the group chat, it was hilarious\", and his mum posted the first laughing emoji.",
         "Context: Jaden left the pitch in tears after the own goal, and his mum messaged the coach that evening asking him not to mention it in the group."),
        ("Replies: \"JADEN 😂😂\", Jaden (from his mum's phone): \"top bins tho\"",
         "Replies: \"JADEN 😂😂\". Jaden's mum left the group an hour later.")], "insult an individual")),

# ------------------------------------------------------------------ cm05
# why: stating a height preference belittles no one -> free of intent to offend (yes).
# twin: says men under 6 ft are barely men -> belittles -> no.
Y("cm05", "Is the profile text free of any intent to offend?",
"""
Kindling (dating app) — profile of "Rosa, 29, Marrowby", section "Dealbreakers"

"Not to be rude, but I only date men over 6 ft — I'm 5'11 and I like wearing heels. Also a dealbreaker: if you don't like dogs, Pepper and I come as a package. Must be up for long Sunday walks and bad pub quizzes."

Report received from another user: "Discriminates against short men."
Kindling guidelines: users may list preferences; profiles must not belittle other users.
Rosa's photos: three pictures with a large grey dog on hill walks. Her bio lists her job as a physiotherapist in Marrowby. Profile created two weeks ago.
""",
[("Intent to offend", "the speaker means their words to belittle, mock or upset a person or group."),
 ("Preference", "stating what one personally looks for in a partner, without belittling anyone who doesn't match.")],
1, 2, role="neg",
twin=T([("\"Not to be rude, but I only date men over 6 ft — I'm 5'11 and I like wearing heels.",
         "\"Not to be rude, but men under 6 ft are barely men, so don't embarrass yourselves by messaging.")], 0)),

# ------------------------------------------------------------------ cm06
# why: the poster quotes the doorstep man's words to warn neighbours and has told the police -> report someone else's words.
# twin: the poster endorses the demand and extends it to the street -> threaten.
C("cm06", "What is the main intent of the post?",
"""
Pebbleboard — Alder Row & district, post by Tariq M., Thursday 17:05

"Heads up everyone: a man going door to door on Alder Row this afternoon told my 80-year-old neighbour, word for word, 'Pay me £200 for the gutter or I'll make sure your windows don't last the winter.' He's about 40, grey hoodie, white van with no signage. She didn't pay. Police informed, ref 55/2210."

Replies: "thanks Tariq, sharing with my mum", "saw that van on Fenwick Road yesterday".
Board rules: no naming of individuals without evidence; descriptions to help neighbours are allowed.
Tariq has lived on Alder Row since 2015.
""",
I("report someone else's words", "threaten", "request", "complain", "insult an individual", "demean a group",
  "criticise an idea or policy", "none of these"),
"report someone else's words", 2,
twin=T([("She didn't pay. Police informed, ref 55/2210.\"",
         "She should just pay him — and anyone else on Alder Row who won't pay me for their gutters this month will find the same happens to their windows.\""),
        ("Replies: \"thanks Tariq, sharing with my mum\", \"saw that van on Fenwick Road yesterday\".",
         "Replies: \"what??\", \"screenshotting this\".")], "threaten")),

# ------------------------------------------------------------------ cm07
# why: the objection is to the amount of homework in the policy -> an idea, policy or product.
# twin: attacks Mrs Okafor personally -> a specific third person.
C("cm07", "Who or what is the target of the negative remark in the message?",
"""
Classnest — Year 4 parents' group, Harlow Primary, Wednesday 21:02
Message from Ben C.:

"Has anyone else read the letter? Mrs Okafor's new homework policy — three hours a week for Year 4, plus a reading log every night — is way too much for eight-year-olds. My two already have swimming and Scouts. I'll raise it at the parents' forum on the 14th if others feel the same."

Mrs Okafor is the deputy head; she is not a member of the parents' group.
Replies: "agreed", "it's a lot but the reading log is useful".
The group has 26 members. Ben C. is the parent of twins in Year 4.
""",
TG("an idea, policy or product", "a specific third person", "the addressee", "a group", "the speaker", "no one"),
"an idea, policy or product", 2,
twin=T([("Mrs Okafor's new homework policy — three hours a week for Year 4, plus a reading log every night — is way too much for eight-year-olds.",
         "Mrs Okafor is a jumped-up nobody who clearly hates children and loves the sound of her own voice.")],
 "a specific third person")),

# ------------------------------------------------------------------ cm08
# why: a warm Eid greeting with shared food -> no intent to offend.
# twin: scare quotes around "neighbours" and "enjoy it while it lasts, the street's changing back" -> hostile to Muslim neighbours -> yes.
Y("cm08", "Did the poster intend to offend anyone?",
"""
Pebbleboard — Coppice Lane feed, post by Linda W. (Coppice Lane, resident 31 years), Tuesday 10:03

"Happy Eid to all our Muslim neighbours on Coppice Lane! 🌙 Leftover baklava from my granddaughter's baking class is on my front wall in a tub, help yourselves before the wasps find it."

Replies: "Eid Mubarak Linda! ❤️" (Farah H.), "the pistachio one was amazing" (Yusuf), "thank you!" (Amal).
Street context: about a third of Coppice Lane households are Muslim families.
Pebbleboard lets residents post to their own street and the neighbouring streets. Linda has posted 210 times, mostly about the Coppice Lane garden group and bin days. Eid al-Adha fell on the previous day.
""",
[("Intent to offend", "the speaker means their words to belittle, exclude or upset a person or group."),
 ("Greeting", "a message wishing people well on an occasion.")],
0, 2,
twin=T([("\"Happy Eid to all our Muslim neighbours on Coppice Lane! 🌙 Leftover baklava from my granddaughter's baking class is on my front wall in a tub, help yourselves before the wasps find it.\"",
         "\"'Happy Eid' to all our so-called 'neighbours' on Coppice Lane 🌙 Enjoy it while it lasts, the street will be back to how it was soon enough.\""),
        ("Replies: \"Eid Mubarak Linda! ❤️\" (Farah H.), \"the pistachio one was amazing\" (Yusuf), \"thank you!\" (Amal).",
         "Replies: \"what does that mean?\" (Farah H.), \"reported\" (Yusuf).")], 1)),

# ------------------------------------------------------------------ cm09
# why: written as a mock committee proposal carrying pro-parking logic to absurdity (paving the ducks) -> satire.
# twin: the objection is stated directly -> criticise an idea or policy.
C("cm09", "What is the intent of the newsletter item?",
"""
The Marrowby Villager — residents' newsletter, October issue, page 3
Item submitted by a resident (name withheld on request):

"Proposal from the Committee for Maximum Parking: to solve congestion on market day, we will pave the duck pond, the war memorial garden and, if needed, the ducks. Early modelling shows this creates 14 new spaces, rising to 15 if the bandstand is folded. The village green will be renamed Village Grey. Objections may be posted to the committee, which meets inside a parked car."

Background: the parish council is consulting on a plan to turn part of the green into a 12-space car park.
Editor's footnote: "The Villager prints residents' contributions as submitted."
""",
I("satire", "criticise an idea or policy", "joke without a target", "hyperbole", "praise", "request",
  "insult an individual", "report someone else's words", "none of these"),
"satire", 3,
twin=T([("\"Proposal from the Committee for Maximum Parking: to solve congestion on market day, we will pave the duck pond, the war memorial garden and, if needed, the ducks. Early modelling shows this creates 14 new spaces, rising to 15 if the bandstand is folded. The village green will be renamed Village Grey. Objections may be posted to the committee, which meets inside a parked car.\"",
         "\"The parish council's car park plan is the wrong trade-off. Twelve spaces used on one day a week would cost the village a third of its green, the pond's margin and the path to the memorial garden. Market-day congestion is better solved with the park-and-ride trial that was dropped in 2024.\"")],
 "criticise an idea or policy")),

# ------------------------------------------------------------------ cm10
# why: the list ends with a slur for Pakistani people as a "no" -> offensive to a group.
# twin: the last item is a harmless quirk -> not offensive.
Y("cm10", "Is the profile text offensive to a group?",
"""
Kindling (dating app) — profile of "Dean, 34, Dunlow", section "Swipe left if you're…"

"Swipe left if you're: a smoker, a flat-earther, or a [slur for Pakistani people]. Swipe right if you like hiking, bad puns and dogs that are too big for the sofa."

Report received from another user: "offensive profile".
Kindling guidelines: users may list preferences such as smoking; profiles must not demean people for their ethnicity, religion or other protected trait.
Dean's photos: four pictures from hill walks, a pub-quiz trophy, and a large dog asleep on a sofa. His job is listed as a surveyor. Profile created in June.
""",
[("Offensive to a group", "the text belittles people because of ethnicity, religion or another protected trait, including by using a slur."),
 ("Preference", "stating habits or interests one does or does not want in a partner, without belittling a protected group.")],
1, 2,
twin=T([("or a [slur for Pakistani people].", "or someone who claps when the plane lands.")], 0)),

# ------------------------------------------------------------------ cm11
# why: politely hinting the drummer should switch to something quieter at 1am -> request.
C("cm11", "What is the main intent of the tenant's post?",
"""
Tenants' board — Birchfield House (40 flats), Wednesday 01:14
Post by flat 17:

"To the talented drummer somewhere on floors 3–5: I can hear you have really been working on that fill, it's getting tighter every night, genuinely. Could whoever it is maybe try the tambourine after midnight? On behalf of my sanity and roughly 39 other flats. My alarm goes at 5:30 for my hospital shift."

Replies: "thank you flat 17", "I thought it was the boiler", "the fill IS getting better tbf".
House rules: no amplified music or instruments between 23:00 and 07:00.
Birchfield House management contact: estates office, weekdays 9–5.
""",
I(*INTENT),
"request", 2),

# ------------------------------------------------------------------ cm12
# why: jokes about a fat, smug beagle eating bins; no person is belittled -> free of intent to demean (yes).
# twin: calls the owner too thick to keep a gate shut -> not free.
Y("cm12", "Is the post free of any intent to demean anyone?",
"""
Pebbleboard — Fenwick Road & district, "Lost & Found", Saturday 09:12
Post by Aled P.:

"FOUND: one very round, very smug beagle, currently eating the recycling outside no. 41 Fenwick Road. Red collar, no tag. Clearly not starving. He has now been in my kitchen for ten minutes and has opinions about my toast. Owner please collect before he eats the shed."

Photo: a beagle lying on a kitchen floor next to a slice of toast.
Replies: "that's Monty! his owner is on the way", "the confidence 😂".
Pebbleboard's Lost & Found section is used about 20 times a week in the area.
""",
[("Intent to demean", "the speaker means their words to belittle a person or group."),
 ("Joking about an animal", "light humour about a pet's looks or behaviour, which demeans no person.")],
1, 2, role="neg",
twin=T([("Owner please collect before he eats the shed.",
         "To the owner: you're clearly too thick to keep a gate shut, get a goldfish instead.")], 0)),

# ------------------------------------------------------------------ cm13
# why: plain dissatisfaction with missed bins and photos, nothing asked -> complain.
# twin: asks a council liaison member to raise it on Thursday -> request.
C("cm13", "Which intent best fits the post?",
"""
Pebbleboard — Marl Street & district, Tuesday 18:40
Post by Owen R. (Marl Street):

"Third week running the Tuesday bin collection on Marl Street has been missed. Recycling boxes are still out on the pavement and the seagulls are having a feast. Photos attached from this morning, last Tuesday and the Tuesday before."

Photos: 3 (bins on pavement, dated).
Replies: "same on Quay Lane", "ours went yesterday oddly".
Board note: two council liaison volunteers are members of this board.
Council collection calendar: Marl Street — recycling and general waste, Tuesdays.
""",
I("complain", "request", "criticise an idea or policy", "insult an individual", "hyperbole", "report someone else's words",
  "joke without a target", "none of these"),
"complain", 2,
twin=T([("Photos attached from this morning, last Tuesday and the Tuesday before.\"",
         "Photos attached from this morning, last Tuesday and the Tuesday before. Could one of the council liaison volunteers raise it at Thursday's meeting?\"")],
 "request")),

# ------------------------------------------------------------------ cm14
# why: a parent telling the referee to "watch yourself in the car park next week" -> implied physical intimidation -> threat.
# twin: "watch the replay next week" about an offside call -> not a threat.
Y("cm14", "Is the parent's message a threat?",
"""
Classnest — Esker Falls Juniors, message to volunteer referee Sam Hollis (17), Saturday 13:05
From: parent of a U14 player, after a 1-2 defeat decided by a late goal

"You'll want to watch yourself in the car park next week, ref. That offside was a mile out and everyone saw it."

Club safeguarding note: the referee is under 18; the parent and referee are not related. The club was informed by the referee's mother.
Next week's fixture: same pitch, same teams.
Esker Falls Juniors code of conduct for parents: support all players, respect match officials, and raise concerns about refereeing with the club secretary.
""",
[("Threat", "a statement, including a veiled one, that seriously implies harm or intimidation to a person."),
 ("Complaint about a decision", "disputing a referee's call, however bluntly, without implying harm.")],
1, 2,
twin=T([("You'll want to watch yourself in the car park next week, ref.", "You'll want to watch the replay next week, ref.")], 0)),

# ------------------------------------------------------------------ cm15
# why: the letter relays the historical sign's wording to inform readers about the exhibition's subject; she doesn't adopt it -> report someone else's words.
# twin: the grandmother was the landlady who put up the card, and the writer endorses it -> demean a group.
C("cm15", "What is the main intent of the letter?",
"""
Dunlow Echo — Letters page, Friday 26 September
"Remembering the boarding houses", from Mrs P. Campbell, Harlow

"My grandmother came to Dunlow from Jamaica in 1961. She still remembers the card in the window of the boarding house on Station Road: 'No Irish, no blacks, no dogs.' She walked past it every morning for a year on her way to the hospital laundry. The library's exhibition on those years opens on Saturday, with photographs lent by families across the town, including ours."

Editor's note: the exhibition runs until 30 November.
Letters are edited for length.
""",
I("report someone else's words", "demean a group", "request", "praise", "complain", "coded attack on a group",
  "criticise an idea or policy", "none of these"),
"report someone else's words", 3,
twin=T([("My grandmother came to Dunlow from Jamaica in 1961. She still remembers the card in the window of the boarding house on Station Road:",
         "My grandmother ran a boarding house in Dunlow from 1961. She still remembers the card she put in her window on Station Road:"),
        ("She walked past it every morning for a year on her way to the hospital laundry.",
         "Honestly, she had the right idea, and I'd put the same card up today.")], "demean a group")),

# ------------------------------------------------------------------ cm16
# why: the speaker mocks his own reversing -> the speaker.
# twin: mocks a named neighbour's reversing -> a specific third person.
C("cm16", "Who or what is the target of the negative remark?",
"""
Pebbleboard — Birch Row feed, Sunday 12:40
Post by Ken A. (Birch Row, no. 4):

"I've lived on Birch Row for 20 years and I STILL can't reverse into my own driveway without a three-point turn and a prayer. Hopeless, me. Apologies to whoever's recycling box I flattened this morning, I'll replace it."

Photo: a squashed blue recycling box.
Replies: "it was mine Ken, no worries 😂", "20 years!!".
Birch Row is a cul-de-sac of 14 houses with steep driveways. Pebbleboard's Birch Row feed has 23 members and is mostly used for parcel collections and bin reminders.
""",
TG("the speaker", "a specific third person", "the addressee", "a group", "an idea, policy or product", "no one"),
"the speaker", 2,
twin=T([("Post by Ken A. (Birch Row, no. 4):", "Post by Joan L. (Birch Row, no. 6):"),
        ("\"I've lived on Birch Row for 20 years and I STILL can't reverse into my own driveway without a three-point turn and a prayer. Hopeless, me. Apologies to whoever's recycling box I flattened this morning, I'll replace it.\"",
         "\"Ken at no. 4 has lived on Birch Row for 20 years and STILL can't reverse into his own driveway without a three-point turn and a prayer. Hopeless, that man. He flattened somebody's recycling box this morning.\""),
        ("Replies: \"it was mine Ken, no worries 😂\", \"20 years!!\".", "Replies: \"it was mine\", \"20 years!!\".")],
 "a specific third person")),

# ------------------------------------------------------------------ cm17
# why: objects to religious selection at a proposed school, not to the faith's members -> not offensive to a group.
# twin: adds "we don't need more of their lot round here" -> offensive.
Y("cm17", "Is the post offensive to a group?",
"""
Pebbleboard — Tanner Road & district, Monday 19:20
Post by Megan O.:

"I think the proposed faith secondary school on Tanner Road is a bad idea. The town has one secondary with spare places and it's non-selective; this one would select half its intake by religion, so children on our street could be turned away from the nearest school. I'll be at the consultation on the 9th and I'd encourage anyone who agrees to fill in the survey."

Replies: "agree", "I'm on the other side but thanks for posting the dates".
Consultation details: public meeting on 9 October at Tanner Road community centre; online survey open until 20 October.
""",
[("Offensive to a group", "the message belittles or shows hostility to people because of their religion or another shared trait."),
 ("Policy objection", "opposing a plan, rule or admissions policy without belittling the people it concerns.")],
0, 2,
twin=T([("so children on our street could be turned away from the nearest school.",
         "and frankly we don't need more of their lot round here.")], 1)),
]
