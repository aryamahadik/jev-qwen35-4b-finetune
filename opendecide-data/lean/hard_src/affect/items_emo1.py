"""Affect hard items, batch emo1: single-label emotion with close pairs (items 1-20)."""
from common import E, T

ITEMS = [
# 1 annoyance vs anger (explicit "not angry" keyword trap); twin -> anger
E("emo_badge_reader",
"""#office-ops (Slack), Tuesday 09:42

Dev Okonkwo: Third time this month the badge reader on the east door has decided I don't exist. Stood out there in the drizzle for five minutes until someone from payroll came through and I could tailgate in behind her. Can someone nudge facilities again? I'm not angry, it's just tedious.

Rosa Lindqvist: Logged it again, ticket FAC-3310. They said a tech is booked for Thursday morning. If it fails before then, the west door reader is fine and the loading bay intercom goes straight to security.

Dev Okonkwo: Thursday it is. Thanks Rosa, appreciate you chasing it.

Hannah Brandt: Same thing happened to me yesterday, fwiw. I thought my badge had been deactivated after the reorg and nearly emailed HR about it.

Rosa Lindqvist: Added your name to the ticket, Hannah.""",
"annoyance", 2, near=["anger", "gratitude", "disapproval", "disappointment"], t="Dev's first message",
twin=T([("I'm not angry, it's just tedious.",
         "Facilities swore in writing that it was fixed. They lied to us, and I want whoever signed it off named at the all-hands.")],
       "anger")),

# 2 nervousness vs fear (future uncertain vs present danger); twin -> fear
E("emo_flood_levee",
"""Harrow Valley Neighbours board - posted Tuesday 11:52 PM by millrace_jo

Update for people on Mill Race Lane: the county forecast says the river could crest near the top of the levee on Thursday night, depending on how much rain falls upstream. We've moved the photo albums and the dog's things upstairs and the car is parked up at my sister's on Kestrel Hill. I keep refreshing the gauge page as if that changes anything. Stomach in knots. Tom is on the phone to his brother about borrowing a pump.

If anyone on the high side of the lane has spare sandbags we'd gladly take a few, and we can return the favour with the trailer. The council depot on Farrow Road was out of bags by four o'clock today.

Will post again when I know more.""",
"nervousness", 2, near=["fear", "caring", "sadness"], t="the author's post",
twin=T([("the county forecast says the river could crest near the top of the levee on Thursday night, depending on how much rain falls upstream",
         "the levee behind number 14 gave way ten minutes ago and water is spreading across the back gardens toward our door")],
       "fear")),

# 3 approval vs admiration; twin -> admiration
E("emo_science_fair",
"""Linwood Primary Parents (community group) - post by Aoife Brennan

Re: the science fair

For those who missed it: the power went out in the gym an hour before judging. The committee moved all forty-two projects to the library and pushed judging back by forty minutes. Moving it rather than cancelling was the correct decision, and I'd have voted for the same thing.

My son's volcano survived the trip across the playground.

Housekeeping: photos are in the shared album under "Science Fair 2026". The librarian asks that anyone who borrowed an extension cord or a folding table from the library return it by Friday, and the lost-property box (one lab coat, two water bottles, a small plastic skeleton) is at the office.""",
"approval", 2, near=["admiration", "amusement", "relief", "gratitude"], t="Aoife's post",
twin=T([("Moving it rather than cancelling was the correct decision, and I'd have voted for the same thing.",
         "Whoever on the committee relabelled forty-two projects by hand and had the library ready in under an hour is a genuine marvel of organisation.")],
       "admiration")),

# 4 relief vs nervousness; twin -> nervousness
E("emo_lipoma",
"""Brightwater Pet Owners forum > Health & Vet Visits
Thread: Lump on my beagle's back leg
Post #14 by sable_and_biscuit

Update for everyone who asked after Biscuit.

Since the appointment last Wednesday I've been doing that thing where you sit up at 2 AM reading every horror story on the internet about soft-tissue tumours in older dogs. The vet phoned at lunch: the needle sample shows a fatty lipoma, benign, and she doesn't think surgery is needed. Tonight I might actually sleep.

For anyone who finds this thread later with a similar lump: the aspirate took about five minutes, Biscuit didn't need sedation, and the clinic charged a flat fee for the cytology. Ask for the cytology report in writing so you have it for the next vet.

Biscuit, for the record, has been completely unbothered throughout.""",
"relief", 2, near=["nervousness", "joy", "gratitude", "fear"], t="the author's update",
twin=T([("the needle sample shows a fatty lipoma, benign, and she doesn't think surgery is needed. Tonight I might actually sleep.",
         "the needle sample was inconclusive, so it's gone to the specialist lab and results come Friday. So, more 2 AM reading until then.")],
       "nervousness")),

# 5 disappointment (unmet expectation), traps: anger, sadness
E("emo_lakeview",
"""Annotation guideline (excerpt): Label the single emotion the author most directly expresses. If none of the listed emotions is expressed, use neutral.

Guest review - Larkspur Inn, Room 12 - rating 2 of 5 - "Not the room we booked"

We booked Larkspur for our tenth anniversary specifically because every listing photo shows the lake from the balcony, and the booking page said "lake-view room guaranteed". We'd been looking forward to that balcony since March. We got a room facing the car park and the kitchen bins. When we asked at the desk, the manager checked and said all lake-view rooms were taken by a wedding party.

In fairness: the staff were polite, the bed was comfortable, and breakfast was fine, especially the smoked trout. We didn't make a fuss because it was our anniversary and we didn't want to spend it at reception.

It just wasn't the weekend we had pictured, and that's what I'll remember about it.""",
"disappointment", 1, near=["sadness", "anger", "disapproval", "annoyance"], t="the reviewer"),

# 6 embarrassment vs remorse; twin -> remorse
E("emo_pineapple_hat",
"""From: Callum Reyes
To: Priyanka Shah
Subject: re: Thursday's all-hands

Hi Priyanka,

Just a note to say sorry for the chaos when my screen share opened on my holiday album instead of the Q3 slides. Nobody was hurt by it except my dignity; forty people have now seen me in a sunhat shaped like a pineapple. I've been replaying it all morning and wincing every time.

The Q3 deck is attached for anyone who wants to look at it properly. The numbers on slide 6 have been updated since the call: churn is 3.1%, not 3.4%, because the April cancellations were double-counted.

If there's time at the next all-hands I can walk through the retention section again, or I can record a short video and put it in the channel instead, whichever you prefer.

Callum""",
"embarrassment", 2, near=["remorse", "amusement", "nervousness", "sadness"], t="Callum's email",
twin=T([("Nobody was hurt by it except my dignity; forty people have now seen me in a sunhat shaped like a pineapple.",
         "The album included the photos from Dana's hospital stay that she asked me to keep private, and now forty people have seen them.")],
       "remorse")),

# 7 curiosity vs confusion; twin -> confusion
E("emo_starter_smell",
"""Breadcraft Forum > Starters & Levains
Posted by crumbshot

Why does my starter smell like nail-polish remover around day 5 but like plain yogurt by day 9? Same flour (stoneground rye), same jar, same spot on the counter at about 22 C, fed 1:1:1 twice a day.

I've read that it's to do with the early acetone-producing bacteria getting outcompeted once the lactic acid bacteria take over, and I'd love to know more. Which microbes are actually doing that? Does feeding temperature change which ones win, and could you keep a starter deliberately in the "nail polish" phase if you wanted to?

Photos of the day-5 and day-9 jars are below. Not a problem at all, the loaves have been great, I'm just nerdily interested.""",
"curiosity", 2, near=["confusion", "surprise", "desire"], t="the poster",
twin=T([("I've read that it's to do with the early acetone-producing bacteria getting outcompeted once the lactic acid bacteria take over, and I'd love to know more. Which microbes are actually doing that? Does feeding temperature change which ones win, and could you keep a starter deliberately in the \"nail polish\" phase if you wanted to?",
         "I've now read three explanations (acetone bacteria, \"hooch\", and the flour going off) and they contradict each other, so I honestly can't tell what's happening in my jar or which advice applies to me.")],
       "confusion")),

# 8 realization (penny drops), traps: annoyance, surprise
E("emo_date_format",
"""#billing-eng thread, Wednesday

Lena Park: Still seeing the "invoice date invalid" failures in the import log. 214 of them yesterday, none the day before.

Marco Silvestri: I checked the supplier template again, nothing obviously wrong. Same columns, same order.

Lena Park: And it's not every supplier. Harlow & Beck are fine, Duarte Metals fail every time.

Ines Kovac: OH. The new Duarte template writes dates as day/month and our importer reads month/day. So anything dated the 13th or later can't be parsed, and everything from the 1st to the 12th goes in silently with the day and month swapped. That's why the first half of every month looked clean. It was never "some suppliers", it's one template and the calendar.

Marco Silvestri: ...which means some of the "clean" ones are wrong too.

Ines Kovac: Yep. Writing it up for the wiki now, then I'll pull the list.""",
"realization", 2, near=["surprise", "annoyance", "confusion", "excitement"], t="Ines's first message"),

# 9 grief (death), traps: sadness, optimism keywords
E("emo_odile",
"""Evening Light Bereavement Circle - members' board
Post by Henrik A.

It's been six weeks since Odile died. People at church keep telling me it gets easier and that I'll be all right in time, and I nod, because what else do you say.

Today I opened the fridge and her shopping list was still stuck to the door with the lemon magnet: "eggs, stamps, call Marit about June". Her handwriting, slanting the way it always did when she was in a hurry. I sat down on the kitchen floor and I don't know how long I was there. The kettle had gone cold when I got up.

I haven't taken the list down. I don't think I can. Forty-one years, and the house is so quiet that I've started leaving the radio on in every room.""",
"grief", 1, near=["sadness", "love", "optimism", "disappointment"], t="Henrik's post"),

# 10 admiration vs pride (stranger vs own child); twin -> pride
E("emo_chess_final",
"""Weekend recap posted to the Corran Chess Club mailing list by Thomas Ekwueme (club secretary)

Quick notes from the Regional Open on Saturday, for members who couldn't make the trip:

The final board was the one to watch. The winner was a twelve-year-old from Alder Vale playing her first open tournament, up against the second seed. On move 19 she gave up her queen for a rook and a pawn, everyone around the board assumed she'd blundered, and eleven moves later the second seed resigned into a mating net. The calculation behind that sacrifice would be beyond most adults in this club, me included, and she played it in under four minutes.

Other results: our A team finished fifth of twelve; the juniors finished third. Entry fees for the autumn league are due by 1 October, and the club sets need new clocks, so please bring any spares.""",
"admiration", 2, near=["pride", "surprise", "excitement", "joy"], t="Thomas's recap",
twin=T([("The winner was a twelve-year-old from Alder Vale playing her first open tournament",
         "The winner was my daughter Ada, twelve, playing her first open tournament")],
       "pride")),

# 11 disgust (physical), traps: anger, disapproval
E("emo_salad_bar",
"""Customer comment form - Greenleaf Market, Pellham Road branch
Submitted: Saturday 13:05 | Contact requested: no

I went to use the salad bar at lunch. When I lifted the lid on the chickpea tray there was a grey furry film across the whole top layer, and behind the crouton bin there was a little pile of what I'm fairly sure were mouse droppings, with a trail of them along the back edge of the counter. The smell when the lid came up was like a drain.

I put the lid back and had to go and stand outside for a minute because I thought I was going to bring up my breakfast. I can still smell it.

I have shopped here for years and I'm not writing to get anyone in trouble; I just think someone needs to look at that counter today.""",
"disgust", 1, near=["anger", "disapproval", "fear", "surprise"], t="the customer's comment"),

# 12 excitement, traps: desire, joy, nervousness
E("emo_coastal_loop",
"""Group chat "Solstice Rail Crew", Wednesday

Priya: THREE DAYS. Bags half packed. I got the window seat for the Coastal Loop leg and I've watched the drone footage of the Haverly viaduct about forty times. When we come round that bend and the whole bay opens up I'm going to be unbearable, I'm warning you all now.

Sam: lol you already are

Priya: Also I've downloaded the route map so I can shout out every lighthouse. There are nine. NINE.

Joe: Reminder that the train leaves Fenwick Central at 06:10, not 06:40. The 06:40 is the stopping service and doesn't connect.

Priya: 06:10, got it. I'll be there at 5:30 vibrating.""",
"excitement", 1, near=["joy", "desire", "nervousness", "amusement"], t="Priya's messages"),

# 13 optimism vs nervousness; twin -> nervousness
E("emo_investor_update",
"""Quarterly note to investors - Tallow Robotics, Q3
From: Nadia Osei, co-founder and CEO

Numbers first. Revenue for the quarter was $212k, down 9% on Q2, because the Marston pilot ended early when Marston was acquired. Burn was $390k a month. Cash in the bank at 30 September: $3.1M.

Pipeline. The pilot with Fennick Foods converts to a paid contract in January if we hit the pick-rate target, which we have hit for the last six weeks. Two hospital groups have moved us to their procurement stage. We have not closed either yet.

Team. We hired a second field engineer and lost our head of sales to a competitor.

My read: I genuinely think next year is the one where this works. The product finally does what customers need it to do, and they are telling us so.

Board meeting is 14 November; papers will go out a week before.""",
"optimism", 2, near=["nervousness", "desire", "pride", "disappointment"], t="Nadia's note",
twin=T([("My read: I genuinely think next year is the one where this works. The product finally does what customers need it to do, and they are telling us so.",
         "My read: I honestly don't know whether we make it through next year. Everything now hangs on two procurement decisions I can't control, and I'm not sleeping well waiting on them.")],
       "nervousness")),

# 14 caring, trap: disapproval of a third party
E("emo_after_review",
"""Direct message, Thursday 17:48

From: Joanna Pike
To: Arjun Das

Hey, I noticed you went quiet after the launch review. Whatever Gerard said in there about the rollout isn't on you: the timeline was set before you joined the team, and everyone in that room knows it.

If you want to take a walk at lunch tomorrow and talk it through, I'm around. Or if you'd rather not think about it at all, I can cover your 9:30 standup so you can sleep in; just send me your notes tonight. And please don't stay late re-doing the slides, they were fine.

Either way, eat something that isn't from the vending machine tonight.

J""",
"caring", 1, near=["disapproval", "love", "sadness", "anger"], t="Joanna's message"),

# 15 love (for a place), traps: sadness, pride, disapproval
E("emo_corran_flat",
"""Corran Street Oral History Project - transcript excerpt, interview 23
Interviewee: Edda Ferreira, 78, resident since 1986

Interviewer: What would you say to someone moving into the street now?

Edda Ferreira: Oh, I'd tell them to look up. People walk down Corran Street looking at their phones and they miss the plasterwork over the old bank. But you asked about the flat. I've lived above the bakery for forty years. I know every stair that creaks and which window sticks in August. The kitchen floor slopes so much a marble would roll to the sink. It's draughty and the boiler has a personality. And I adore it. I adore every crooked inch of it. My son keeps sending me brochures for bungalows by the sea, and I keep putting them in the recycling. They'll carry me out of this flat.

Interviewer: And the bakery?

Edda Ferreira: The bakery is why the flat is always warm in winter.""",
"love", 1, near=["pride", "joy", "sadness", "amusement"], t="Edda's answers"),

# 16 amusement vs embarrassment (laughs at own blunder)
E("emo_keys_in_slot",
"""Voicemail transcript - Fairhaven Public Library, front desk line - received 07:58, Monday

"Hi, good morning, this is Ottilie Varga, my library card ends in 4471. I'm calling because I returned my book through the outside return slot about ten minutes ago, and it seems I posted my car keys along with it. [laughs] I heard them clunk and just stood there staring at the slot. My husband thinks this is the funniest thing that has ever happened to anyone and, honestly, he's right, I can't stop laughing either.

"Could somebody fish them out of the return bin when you open at nine? They're on a keyring with a little plastic lobster, you can't miss it. I'll be the woman in the grey car in the car park, still giggling at herself. Thank you, bye.\"""",
"amusement", 2, near=["embarrassment", "joy", "surprise", "annoyance"], t="the caller"),

# 17 surprise, traps: joy, excitement, confusion
E("emo_surprise_hall",
"""From a message Beatrix Holm posted in her village's community group, Sunday evening

Some of you will already know this, but I only found out at six o'clock tonight.

I was asked to go down to the parish hall "to count the folding chairs for the jumble sale". I walked in, reached for the light switch, and forty people jumped up and shouted my name. My sister had come over from Rotterdam without telling me. My old headmaster from the primary school was there, and he must be ninety. I actually screamed, and then I just stood there with my mouth open for what my grandson says was a full minute. I had no idea. None. Not a single person let it slip for three months.

I'm told there are photographs of my face. I have asked that they be destroyed.""",
"surprise", 2, near=["joy", "gratitude", "embarrassment", "confusion"], t="Beatrix's post"),

# 18 neutral under past-resolved rule; twin -> relief
E("emo_router_followup",
"""Annotation guideline (excerpt): Label the emotion the author expresses at the time of writing. Feelings the author reports having had earlier and describes as over are not labelled. If no listed emotion is expressed at the time of writing, use neutral.

Message to annotate - Brookline Broadband support, reply on ticket #5521:

"Following up on this ticket. When the router dropped for the third time during my client call last week I was furious, I won't pretend otherwise. Since the engineer replaced the unit on Monday it has been stable: no drops in five days, speed tests at 480-520 Mbps. Please close the ticket. The old unit is in its box by the front door if the courier needs to collect it; I'm home on weekdays after 3 PM. Account number 88-1204.\"""",
"neutral", 3, near=["anger", "relief", "remorse", "annoyance"], t="the customer's reply",
twin=T([("Since the engineer replaced the unit on Monday it has been stable: no drops in five days, speed tests at 480-520 Mbps.",
         "Since the engineer replaced the unit on Monday it has been stable, and what a weight off; I'd been dreading every call and I can finally work from home again without holding my breath.")],
       "relief")),

# 19 neutral: emotions belong to others (caseworker note); twin -> caring
E("emo_caseworker_note",
"""Annotation guideline (excerpt): Label only emotions that the author of the note expresses. Emotions the author reports other people as having are not labelled. If the author expresses no listed emotion, use neutral.

Riverside Tenants' Advice Service - contact note
Caseworker: M. Adeyemi | Client ref: RT-2217 | Contact: phone, 14:20

Client reports that the landlord's dog got through the broken side fence on Saturday and chased her son (age 7) across the courtyard. Client states her son was terrified and has not wanted to play outside since. Client is angry that the fence was reported in March and not repaired. Client requests that we contact the landlord (Harwick Lettings) about the fence and asks whether she can withhold rent. Advised client not to withhold rent; explained the repair-notice process. Letter to Harwick Lettings to be sent by Friday. Follow-up call booked for next Wednesday.""",
"neutral", 2, near=["fear", "anger", "caring", "sadness"], t="the caseworker's note",
twin=T([("Follow-up call booked for next Wednesday.",
         "I'm concerned for the boy and will call the family myself on Wednesday to check he's all right and offer the children's support line.")],
       "caring")),

# 20 disapproval (no hostility), traps: fear, anger
E("emo_towpath_scooters",
"""Letter to the Wendlebury Moorings Residents' Newsletter, September issue

Dear editor,

At the August meeting the residents' committee voted to allow e-scooters on the towpath between the marina and the Holt Lane bridge. I think this is a mistake. The path narrows to 1.4 metres at the lock, it has no lighting after the boatyard, and on weekend mornings it is full of families with pushchairs and people walking dogs. A scooter at 15 mph has nowhere to go at the lock if someone steps off a boat.

I'm not suggesting anyone on the committee acted in bad faith, and I understand that some residents commute to the station and want a quicker route. But I don't think the decision weighed those risks properly, and I'll be asking at the AGM for it to be reconsidered, perhaps with a speed limit or a dismount zone at the lock.

Yours,
Graham Oduya, berth 31""",
"disapproval", 2, near=["anger", "fear", "nervousness", "annoyance"], t="Graham's letter"),
]
