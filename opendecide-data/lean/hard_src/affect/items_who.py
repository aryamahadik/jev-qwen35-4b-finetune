"""Affect hard items, batch who: which participant expresses a given emotion (options = people + none)."""
from common import W, T, NONE_LABEL

ITEMS = [
# W1 relief; hypothetical relief and attributed relief are traps; twin -> none
W("who_audit_relief",
"""#finance-team (Slack), Friday 16:31

Kofi Mensah: External auditors have signed off FY25. Management letter has two minor points, both about expense-claim approvals, nothing material.

Elena Rusu: Oh thank god. I've had a knot in my stomach since they asked for the Q3 revenue schedules again on Wednesday. I can finally stop checking my inbox every ten minutes.

Sanjay Pillai: I'd be relieved if the board approves next year's budget as smoothly, but I'm not counting on it. The capex line is going to get picked apart.

Maya Lindholm: Kofi must be so relieved, he's barely slept this week. Thanks for covering my reconciliations on Tuesday, by the way, Kofi.

Kofi Mensah: No problem. Drinks at the Anchor at 5:30 for anyone who wants them.""",
["Kofi Mensah", "Elena Rusu", "Sanjay Pillai", "Maya Lindholm"], "relief", "Elena Rusu", 2,
extra=["gratitude", "nervousness"],
twin=T([("Oh thank god. I've had a knot in my stomach since they asked for the Q3 revenue schedules again on Wednesday. I can finally stop checking my inbox every ten minutes.",
         "As expected. The Q3 revenue schedules they asked for again on Wednesday went over on Thursday morning. I'll file the signed report in the audit folder.")],
       NONE_LABEL)),

# W2 fear vs nervousness vs excitement
W("who_ridge_fear",
"""Group chat "Carn Dubh weekend", Saturday

11:02 Ines: Forecast for tomorrow's ridge day has changed to 40% chance of thunderstorms after 2pm. Keep wondering if we should bail on the ridge and do the valley loop instead. Not sure I'll sleep much tonight weighing it up.

11:05 Rafe: Honestly can't wait. First proper scramble since my knee op, I've had the route map on my wall for a month.

11:40 Tamsin: Rafe, Ines, I'm on the approach path under the east crag and rocks are coming down right now. Something big just went past me about ten metres to my left. I'm pressed against the wall under the overhang and I can't see where the next ones are coming from.

11:41 Rafe: Stay under the overhang!! Don't move till it stops. I'm calling mountain rescue.

11:44 Ines: Tamsin please keep your helmet on and text every five minutes.""",
["Ines", "Rafe", "Tamsin"], "fear", "Tamsin", 1, extra=["nervousness", "excitement", "caring"]),

# W3 admiration vs approval vs pride vs surprise
W("who_bookclub_admiration",
"""Minutes - Larchmont Library Book Group, 9 September
Book discussed: "The Salt Ledger" by (fictional) author Oona Veldt

Present: Harriet Coyle (chair), Desmond Achebe, Lin Yao, Petra Novak

Harriet opened by saying she agreed with the committee's decision to choose a shorter book for September, given the summer holidays; she thought it was the sensible choice.

Desmond said he was proud of himself for finishing it at all, since he usually abandons anything with more than two narrators.

Lin said she was completely taken aback by the final chapter and had not seen the twist about the harbour master coming.

Petra said the way the novel braids three timelines across two centuries without a single visible seam was extraordinary craftsmanship, and that she thought Veldt was one of the finest structural writers working today.

Next month: "Winter Orchard". Petra to bring the biscuits.""",
["Harriet Coyle", "Desmond Achebe", "Lin Yao", "Petra Novak"], "admiration", "Petra Novak", 2,
extra=["approval", "pride", "surprise"]),

# W4 disappointment; twin -> none
W("who_retro_disappointment",
"""Retrospective notes - Tidewater app beta, sprint 14
Facilitator: Ama Owusu

What happened: The public beta opened on 2 September. We set a goal of 500 sign-ups for the first two weeks. Actual: 120.

Comments round:
Ama Owusu: I'd really believed we'd get to 500 after the waitlist response in August. Seeing 120 was a let-down, I won't pretend it wasn't.
Rhys Carter: The landing page went down twice during launch week. That was irritating, especially the second time, when it was the same config mistake.
Nadia Hakimi: I'm sad Priya is leaving at the end of the month; the design system won't be the same without her.
Joel Brandt: Honestly I expected worse, given there was no marketing spend. Let's look at where the 120 came from.

Actions: Rhys to add a config check to the deploy pipeline; Joel to break down sign-up sources; Ama to set a revised target for October.""",
["Ama Owusu", "Rhys Carter", "Nadia Hakimi", "Joel Brandt"], "disappointment", "Ama Owusu", 2,
extra=["annoyance", "sadness"],
twin=T([("I'd really believed we'd get to 500 after the waitlist response in August. Seeing 120 was a let-down, I won't pretend it wasn't.",
         "For the record, the 500 figure was a stretch target I set without data. 120 is in the range the August waitlist numbers predicted.")],
       NONE_LABEL)),

# W5 gratitude vs relief vs admiration (feedback cards)
W("who_ward_cards",
"""Ward 9 (Orthopaedics) - patient and family feedback cards, week 36, transcribed by the ward clerk

Card 1 - Mr Samuel Otieno: "I was dreading the hip operation for months. It's done, it went fine, and I'm walking with the frame already. What a weight off."

Card 2 - Mrs Clara Jensen (daughter of patient in bay 4): "Nurse Bello is the most skilled and composed nurse I've ever watched work. The way she handled the emergency on Tuesday night was remarkable."

Card 3 - Mr Wiktor Nowak: "Thank you to the night porter, Denis, who sat with me at 3 a.m. when I couldn't sleep and brought me a cup of tea when he didn't have to."

Card 4 - Ms Rosa Delgado: "The car park charges are too high for families who visit every day. This should be reviewed."

Clerk's note: cards 1-4 forwarded to the ward manager. Card 4 also forwarded to Estates.""",
["Samuel Otieno", "Clara Jensen", "Wiktor Nowak", "Rosa Delgado"], "gratitude", "Wiktor Nowak", 2,
extra=["relief", "admiration", "disapproval"]),

# W6 embarrassment vs remorse vs amusement
W("who_dinner_party",
"""Group chat "Birthday dinner crew", Sunday morning after the party

Oskar: Morning all. Hosts' update: the rug is in the bath soaking. Hannah, the red wine has come out mostly, stop worrying.

Hannah: I still feel awful. It was your grandmother's rug and I was waving my glass about like an idiot. I'm so sorry, Oskar, I'll pay for the cleaners, please let me.

Bea: Can we talk about the karaoke. I introduced "my favourite song of all time", got the first line completely wrong in front of twelve people, and then tripped over the mic cable. I want to move to a different country. My face is still hot thinking about it.

Theo: The mic cable moment is the funniest thing I've seen all year, I'm still laughing.

Oskar: Bea, nobody's leaving the country. Hannah, if you insist, you can buy the next round.""",
["Oskar", "Hannah", "Bea", "Theo"], "embarrassment", "Bea", 2, extra=["remorse", "amusement"]),

# W7 annoyance vs anger vs disapproval; twin -> none
W("who_residents_annoyance",
"""Draft minutes - Calloway Court Residents' Association, extraordinary meeting, 18 September

Item 1: Fire door on the fourth floor
Mr Farouk Haddad said he was outraged that the managing agent, Pendle Estates, had ignored three written reports that the fourth-floor fire door did not close. He said the agent's director should resign and that he would be reporting the company to the fire authority himself.

Item 2: Parking
Ms June Okafor said that for the third week running delivery vans had blocked the bin store on Tuesdays, which meant the bins were missed again. She said it was a nuisance and she was tired of dragging her recycling to the street.

Item 3: Garden
Mr Colm Riley said he thought the plan to remove the two cherry trees was a poor decision and asked that it be deferred until the tree survey is published.

Actions: Secretary to write to Pendle Estates on items 1 and 2; garden item deferred to the October meeting.""",
["Farouk Haddad", "June Okafor", "Colm Riley"], "annoyance", "June Okafor", 2,
extra=["anger", "disapproval"],
twin=T([("She said it was a nuisance and she was tired of dragging her recycling to the street.",
         "She proposed asking the delivery firms to use the side entrance on Tuesdays.")],
       NONE_LABEL)),

# W8 pride vs admiration vs joy vs gratitude
W("who_concert_pride",
"""Group chat "Year 5 parents", Thursday 21:15, after the school spring concert

Leila: What a lovely evening. The hall looked beautiful with the lanterns and I haven't heard that many children singing together since before the pandemic.

Grant: That girl on the cello in the second half, Noor I think? Playing that solo at nine years old with the whole hall silent. Astonishing musicianship, honestly better than some adults I've heard.

Beth: Please pass on a massive thank you to Mr Achterberg for all the extra rehearsals at lunchtime, the kids would never have been ready without him.

Karim: Can I just say, my Jamie did the whole narration without a single script check. Six weeks ago he couldn't get through a page without freezing. I'm bursting.

Leila: Photos going in the shared folder tomorrow.""",
["Leila", "Grant", "Beth", "Karim"], "pride", "Karim", 2, extra=["admiration", "joy", "gratitude"]),

# W9 caring vs optimism vs neutral
W("who_colleague_caring",
"""Email thread: "Wednesday site visit"

From: Olu Adebanjo
Sent: Tuesday 17:10
Can someone confirm the site visit is still on for Wednesday at 10? I need to book the pool car before 6.

From: Greta Hollis
Sent: Tuesday 17:18
Still on as far as I know. Also, I heard Mateo went home from the office today with a migraine. Mateo, if you're reading this, please don't come in tomorrow. I'll take your part of the walkthrough, and if you need anything picked up from the pharmacy tonight I'm driving past it.

From: Priyesh Rao
Sent: Tuesday 17:25
Forecast says the rain should clear by mid-morning, so hopefully the ground won't be too bad by the time we're out there.

From: Olu Adebanjo
Sent: Tuesday 17:31
Booked. Meet at the east gate.""",
["Olu Adebanjo", "Greta Hollis", "Priyesh Rao"], "caring", "Greta Hollis", 1, extra=["optimism", "nervousness"]),

# W10 confusion vs curiosity vs annoyance; twin -> none
W("who_course_confusion",
"""Course forum - DATA 210 (Intro to Statistics), Assignment 2 thread

Post by Carmen Ruiz:
The brief says the word limit is 1,500 words "excluding appendices", but the rubric says "all written material counts toward the limit". So do the tables in my appendix count or not? I've read both documents three times and I genuinely can't work out which one we're meant to follow.

Post by Hamid Karimi:
Not about the assignment exactly, but the reading mentioned that Simpson's paradox shows up in admissions data. I'd love to learn more about real cases. Any recommended articles?

Post by Pia Lindqvist:
The submission portal logged me out twice while uploading. Mildly irritating but it went through in the end.

Post by the teaching assistant:
Carmen, I'll get the course lead to confirm the word-limit wording tomorrow. Hamid, see the optional reading list, week 6.""",
["Carmen Ruiz", "Hamid Karimi", "Pia Lindqvist"], "confusion", "Carmen Ruiz", 2, extra=["curiosity", "annoyance"],
twin=T([("So do the tables in my appendix count or not? I've read both documents three times and I genuinely can't work out which one we're meant to follow.",
         "The course lead confirmed in lecture that the brief takes priority, so appendix tables don't count. Posting here in case anyone missed it.")],
       NONE_LABEL)),

# W11 disgust vs disapproval vs anger
W("who_kitchen_disgust",
"""Shift handover log - The Copper Kettle, kitchen, Saturday close

Opening chef (Anya Petrov), 07:40: Walk-in fridge seal failed overnight. When I opened it the smell hit me before the light came on. The chicken thighs had gone grey and slimy and there was liquid pooling under the veg racks. I gagged twice clearing it and had to step out into the yard. Everything below shelf 3 binned; list attached.

Sous chef (Dario Conti), 15:10: Management's decision to cut the fridge maintenance contract last spring was a mistake, in my view. We should reinstate it.

Kitchen porter (Sione Taufa), 22:30: Replacement seal fitted by the engineer at 18:00, temp holding at 3 C. Deep-cleaned walk-in, logged in the HACCP book.

Manager's note: stock loss claim submitted to insurers.""",
["Anya Petrov", "Dario Conti", "Sione Taufa"], "disgust", "Anya Petrov", 1, extra=["disapproval", "anger"]),

# W12 realization vs surprise vs confusion
W("who_mystery_realization",
"""Transcript excerpt - "Murder at Pemberley Hall" online mystery game, voice chat, round 4

Game master: The final clue: the gardener's boots were found clean, although it rained all night.

Priti: What? The boots were clean? I did not see that coming at all. Wow.

Aleksander: Hold on. Clean boots after a night of rain means he never went outside. So the footprints by the greenhouse can't be his, and the only other person with size-ten shoes is the vicar. That's why the vicar asked about the weather at dinner. It was the vicar the whole time.

Mireille: I'm lost. Which footprints? I thought the greenhouse was locked, or was that the library?

Game master: Accusations close in two minutes.""",
["Priti", "Aleksander", "Mireille"], "realization", "Aleksander", 2, extra=["surprise", "confusion"]),
]
