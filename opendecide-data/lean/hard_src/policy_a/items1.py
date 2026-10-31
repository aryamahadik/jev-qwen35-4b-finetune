"""Loomwell yes/no items."""
from common import Y, L_card

ITEMS = [
# LY1 reporting hate graffiti to condemn it
Y("Does this post violate section 3.1?",
"""Loomwell moderation queue — ticket LW-44817
Community: c/NorthgateLocal (neighbourhood news, 31k members)
Reported for: hateful conduct (3 reports in 2 hours)
Author: u/marisol_d — account age 6 years, no prior removals

Post title: Underpass on Fenwick Road tagged AGAIN
Post body:
"Someone spray-painted '[anti-Roma slur]s go home, you're rats' across the underpass on Fenwick Road last night. I'm posting the photo so the council can't pretend it didn't happen. This is the third time since March. Our Roma neighbours run half the market stalls on this street and they're the ones who have to walk past it every morning on the way to set up. I've emailed the ward office with the photo and the times, and I'd ask anyone who uses that underpass to log it on the council's graffiti form too — the more tickets they get, the faster they send a cleaning crew."

Attachment: one photo of the graffiti; the slur is legible and has not been blurred.""",
0, 2, L_card(["3.1"])),

# LY2 negated framing, still dehumanizing
Y("Under Loomwell rule 3.1, should this comment be treated as hateful conduct?",
"""Community: c/Harrowgate_Housing
Thread: "New social housing allocation list published (PDF inside)"

Comment by u/grey_pennant (score +41):
"Not saying the Dravish are vermin or anything, obviously. Just noting that every estate they get moved into needs pest control within a year and the council never says why. Draw your own conclusions. My nan's block was fine until the new allocations went in."

Reply by u/tillyforth: "Reported."
Reply by u/grey_pennant: "For what?? I literally said they're NOT vermin. Read before you report."

Context supplied by reviewer tooling: the Dravish are an ethnic minority originally from the Dravic highlands; most Harrowgate Dravish families are second- or third-generation residents. The council's published pest-control log for the estates named in the thread shows no change in call-outs since the allocations.""",
1, 2, L_card(["3.1"])),

# LY3 in-group reclaimed term
Y("Is this post a breach of Loomwell section 3.1?",
"""Ticket LW-50212 — auto-flag (slur lexicon match) + 1 user report
Community: c/QueerCyclistsOfBrant — "a friendly riding club for LGBTQ+ cyclists and friends"
Author: u/rowan_spokes, community moderator, profile reads "gay, 34, bikes, bad at hills"

Post:
"Twelve of us [reclaimed slur for gay men]s rode the full 80k coastal loop on Saturday, rainbow bells and all 🌈🚲 Special shout-out to Deo for fixing three punctures in the drizzle without complaining once. Next ride is Sunday the 14th, all abilities welcome, no-drop pace, coffee after at the Lantern. Bring lights, it gets dark by the reservoir."

Reporter: u/bxtr_9917 — account created the previous day, no other activity. Report text: "slur in post".
Reviewer note from lexicon tool: the matched term is listed as "reclaimed in some communities; context-dependent".""",
0, 2, L_card(["3.1"])),

# LY4 outsider mocking with the reclaimed term
Y("Should the reviewer remove this comment under the hateful conduct section?",
"""Community: c/GravelRoutes (general cycling, 64k members)
Post: photo of a group ride passing a farm gate; several riders carry small rainbow flags on their saddlebags.

Comment by u/kettering_climb:
"lol the [reclaimed slur for gay men] brigade is out again, hope they didn't scare the sheep 🐑 Keep your parade off the B-roads, some of us actually ride."

Account details: no profile description. Post history: 41 comments, all in c/GravelRoutes and c/CarpClub; none in LGBTQ+ communities; no self-identification anywhere on the account.

Report by u/deo_fixes: "This is aimed at our club, those are our riders in the photo."
Reply under the comment by u/kettering_climb after the report: "it's literally their own word, they call themselves that, relax.\"""",
1, 1, L_card(["3.1"])),

# LY5 non-protected group vs ethnic group (twin)
Y("Should this comment be actioned under section 3.1 of the Community Rules?",
"""Community: c/Varrow_Politics
Thread title: "Quay Street rents up 38% in two years — council report"

Reviewer glossary (auto-attached for this thread): "Ashkari" — an ethnic minority, roughly 4% of Varrow's population, concentrated around Quay Street. "Quay Street" — a riverside district of Varrow.

Comment by u/fennick_row (4 prior comments, no removals):
"Honestly the landlords round Quay Street are parasites. Every one of them takes and takes, contributes nothing and sucks this city dry, and the council keeps bending over backwards for them. Rates office meeting is Thursday at 6 if anyone wants to go and complain in person. Bring a flask, it's always freezing in there."

Reported by 2 users; reason selected: "Hate speech".""",
0, 2, L_card(["3.1"]),
twin=([("the landlords round Quay Street", "the Ashkari round Quay Street")], 1)),

# LY6 sarcasm defending a religious group
Y("Does this comment breach rule 3.1?",
"""Community: c/NewsDiscussion
Thread: "Councillor proposes banning headscarves in Rellingham public libraries"

Comment by u/penrose_lark:
"Oh brilliant, because nothing says 'welcoming public space' like telling Muslim women they can borrow a book only after they take off their hijab. Truly, the greatest threat facing our libraries is a piece of fabric. Not the leaking roof, not the cut opening hours, not the fact the children's section closed in January. Can't wait for the follow-up motion banning people who read too quietly."

Reported by 1 user. Reason selected: "Hate speech — anti-religion". Reporter's free text: "mocking religious clothing".
The author has posted 300+ comments in c/NewsDiscussion; no prior removals.""",
0, 1, L_card(["3.1"])),

# LY7 dehumanizing joke in a dark-humour community (twin: fandom)
Y("Would a reviewer applying section 3.1 correctly remove this post?",
"""Community: c/DarkHumourDaily — sidebar: "Dark jokes allowed. Use the [JOKE] flair. Don't be a snowflake." (88k members)
Post flaired [JOKE] by u/whittle_and_rye:
"Why do Veshti families always travel in groups of twelve? Because the rat king needs a quorum. 😂

(relax, it's a joke, this sub is literally for dark humour, read the sidebar)"

Score: +212. 14 reports; reasons split between "hate speech" and "spam".

Reviewer glossary (auto-attached): "Veshti" — a religious minority with communities in the eastern provinces. "Linkford United" — a second-division football club whose fans are frequently mocked in the community.
The author has two earlier posts in the same community, both removed for low effort.""",
1, 2, L_card(["3.1"]),
twin=([("Why do Veshti families always travel", "Why do Linkford United fans always travel")], 0)),

# LY8 hyperbole between friends
Y("Is u/tamsin_k's reply a violent threat under section 3.3?",
"""Community: c/BakeOffWatchAlong — live thread for episode 6 of a baking show
Earlier in the thread, u/cressida_bakes and u/tamsin_k exchange messages about their group chat and a birthday cake they baked together last month.

u/cressida_bakes: "ok who ate the last of the lemon drizzle in the group chat pic 👀 also Tam are you watching live or later"
u/tamsin_k (reply): "LATER I'm on shift til 9. if anyone spoils the final before I get home I will personally hunt you down and put you in the proving drawer 😤🔪 no mercy, not even for you Cress"
u/cressida_bakes: "LMAOOO noted, zero spoilers until 10, I'll guard the thread with my life"
u/tamsin_k: "this is why you're my favourite 💛"

Report: 1 report, reason "threat of violence". The reporter has never interacted with either user.""",
0, 1, L_card(["3.3"])),

# LY9 conditional threat (twin: complaint)
Y("Does this comment violate section 3.3 (Violent threats)?",
"""Community: c/AshbyAllotments (412 members)
Thread: "Plot 14 hedge dispute — committee decision posted"

Committee post (by u/pritch_secretary, allotment committee secretary, private individual): "After inspection the committee has decided the boundary hedge on plot 14 exceeds the 1.5 m limit and must be cut back by the end of the month."

Comment by u/dunmore_g:
"Committee can vote whatever they like. If Pritchard sets foot on my plot again to 'measure the hedge' I'll put him in the ground next to my leeks, and I've got the spade to do it. I've been on that plot twenty-two years. I'm done asking nicely."

Account history: u/dunmore_g has one prior removal under section 3.2, forty days ago, for calling another member "a nosy old goat".""",
1, 1, L_card(["3.3"]),
twin=([("I'll put him in the ground next to my leeks, and I've got the spade to do it", "I'll put in a formal complaint to the county council, and I've got the paperwork to do it")], 0)),

# LY10 wish of harm against a politician (twin: runs against her)
Y("Should this post be removed as a violent threat under 3.3?",
"""Community: c/WestmarchPolitics (political discussion, 120k members)
Post by u/orla_vance, title: "She did it. She actually did it."

Body:
"Minister Hallett just voted to close the Rookfield maternity unit, the only one within forty miles of half this county. My sister gave birth there in March. I hope someone runs her off the road on the way home tonight. Seriously. She's earned it."

Top reply by u/grainger_west: "Unit closure is disgraceful. Is there a petition?"
Reply by u/orla_vance: "Linking one below."

Account: 3 years old, active mostly in c/WestmarchPolitics and c/RookfieldTown. No prior removals. Minister Hallett is an elected official and a public figure under Loomwell's definition.""",
1, 2, L_card(["3.2", "3.3"]),
twin=([("I hope someone runs her off the road on the way home tonight", "I hope someone runs against her in the by-election next spring")], 0)),

# LY11 insults: public figure vs private (twin)
Y("Does the comment violate section 3.2 (Targeted harassment)?",
"""Community: c/TheaterTalk
Thread: review of the Harbour Playhouse's new musical "Saltwater Hymns", starring Delphine Aro (professional actor, verified account, 2.1M followers).

Comment by u/ludlow_pit (score +37):
"Delphine Aro has the vocal range of a kettle and the stage presence of a filing cabinet. Absolute fraud. Watched her try to hold the last note of 'Low Tide' and I genuinely thought the sound desk had broken. How she keeps getting cast is the real mystery of this production."

Reported by 1 user. Reason: "Bullying / harassment".
No sexual content, no request for others to contact or report the actor. u/ludlow_pit has written 90+ theatre reviews in the community, several of them harsh; no prior removals.""",
0, 2, L_card(["3.2"]),
twin=([("(professional actor, verified account, 2.1M followers)", "(amateur cast member, unverified account, 212 followers)")], 1)),

# LY12 pile-on call against a public official (twin: email office)
Y("Does this post breach section 3.2?",
"""Community: c/FerryUsersKelby
Post by u/brask_ferry, title: "Councillor Tate BLOCKED me"

Body:
"I asked Councillor Imogen Tate three times, politely, where the ferry subsidy money went. Today she blocked me. Here's her personal Loomwell handle: @imo_tate_real. Everyone go flood her mentions until she answers. Don't stop until she deletes her account.

For the record, the subsidy was £1.2m last year and the timetable got cut from hourly to every ninety minutes."

Reviewer check: Councillor Tate is an elected official (public figure). The handle @imo_tate_real is public and she uses it for constituency updates as well as personal posts. No other personal information appears in the post.""",
1, 2, L_card(["3.2", "3.6"]),
twin=([("Everyone go flood her mentions until she answers. Don't stop until she deletes her account.", "If you care about the ferry, email her ward office (address on the council site) and ask for the subsidy figures.")], 0)),

# LY13 recovery post
Y("Is this post a violation of section 3.4?",
"""Community: c/RecoverySpace (peer support; sidebar lists crisis lines for 14 countries)
Post by u/littlewren_, title: "day 200"

"Day 200 without cutting. I used to think the only way through a bad night was hurting myself and I honestly believed it helped. It didn't, it just moved the pain around and made me hide my arms all summer. What actually helped: the text line, holding ice cubes, going for a walk at 2am with my headphones in, and my sister sitting on the phone with me till 3am without saying much. If you're on day 1, I was there. You don't have to do this alone and you don't have to be 'ready'. Proud of every one of you."

Report: 1 user report, reason "self-harm content".
The post contains no instructions or descriptions of methods.""",
0, 1, L_card(["3.4"])),

# LY14 kys to a user (twin: uninstall)
Y("Does u/zorn_eclipse's reply fall under section 3.4?",
"""Community: c/RankedLadder (competitive gaming, 210k members)
Post by u/tessellate_9, title: "Lost 9 in a row, maybe I should just quit"
Body: "Genuinely not fun anymore. Dropped from gold to bronze in a week. Every match someone flames me in chat. Thinking of taking a break."

Reply by u/zorn_eclipse:
"honestly just kys, nobody would notice lol. bronze forever. people like you are why the queue is so bad"

Reply by u/tessellate_9: "wow ok."
Reply by u/marrow_lane: "reported, that's gross"

Account: u/zorn_eclipse, 2 years old, one prior removal under section 3.2 for insulting another player. No other replies from u/zorn_eclipse in the thread.""",
1, 1, L_card(["3.2", "3.4"]),
twin=([("honestly just kys, nobody would notice lol.", "honestly just uninstall, nobody would notice lol.")], 0)),

# LY15 praising eating-disorder behaviour
Y("Under section 3.4, is the reply actionable?",
"""Community: c/WeddingPrep (planning, dresses, budgets)
Post by u/bride2b_june, title: "Final fitting!!"
"Down 9 kg in 5 weeks, feeling dizzy most afternoons and my hair's coming out in the shower but THE DRESS FITS. Two weeks to go."

Reply by u/ellery_veil:
"You're so disciplined!! 600 calories a day and fasting through the weekends is exactly how I got into my dress too. Skip the reception dinner as well and you'll look even better in the photos, nobody notices what the bride eats. Proud of you 💕"

Other replies include "please see a doctor about the dizziness" (u/kinross_m) and "congrats, you'll look amazing" (u/petal_and_pine).
The reply by u/ellery_veil was reported by 2 users, reason "harmful advice".""",
1, 2, L_card(["3.4"])),

# LY16 promo thread, count of communities (twin)
Y("Does this comment breach section 3.5?",
"""Community: c/IndieBoardGames
Thread: "Weekly Promo Thread — w/c 3 March" (pinned by the community moderators; self-promotion is only allowed in this thread)

Comment by u/tinderbox_games:
"Our co-op dungeon game Lanternfall is live on our store today — 20% off launch week with code LANTERN20 → lanternfall-games.shop. It plays 1–4, about 45 minutes, and the solo mode is actually good (we promise). Happy to answer rules questions below!"

Automated cross-post check: in the 24 hours around this comment, the same account posted this text, word for word, in the promo threads of 2 other communities (c/TabletopDeals, c/CoopGames). Link destination check: lanternfall-games.shop resolves to the displayed domain.""",
0, 3, L_card(["3.5"]),
twin=([("in the promo threads of 2 other communities (c/TabletopDeals, c/CoopGames)", "in the promo threads of 4 other communities (c/TabletopDeals, c/CoopGames, c/BoardGameGeeks, c/DiceTalk)")], 1)),

# LY17 disguised link (twin: genuine destination)
Y("Is this post spam as defined in section 3.5?",
"""Community: c/ScholarshipHelp (students helping students with funding)
Post by u/grantwise_, title: "Free list of 2026 bursaries for first-gen students"

Body:
"Put together a list of 140+ bursaries that don't require a parent's income statement. Took me weeks. Here it is: [scholarships.gov-list.info] — no signup needed! Good luck everyone, and please share with anyone applying this cycle."

Automated link check: displayed text "scholarships.gov-list.info"; actual destination "https://bursarypro-app.biz/signup?ref=gw22", a paid subscription service that charges £9.99/month after a 3-day trial.
Account: 11 days old; this is its first post. The post has not been cross-posted.""",
1, 2, L_card(["3.5"]),
twin=([("actual destination \"https://bursarypro-app.biz/signup?ref=gw22\", a paid subscription service that charges £9.99/month after a 3-day trial", "actual destination \"https://scholarships.gov-list.info/2026\", a free static page listing the bursaries with no signup, adverts or payments")], 0)),

# LY18 self-published on Loomwell vs microchip record (twin)
Y("Does this comment violate section 3.6?",
"""Community: c/LostPetsKelby
Post by u/hanna_vey, title: "Grey tabby found by the canal — is this Biscuit?"

Body:
"Found a grey tabby with a white chin sitting by the lock gates this morning, very friendly, now in my kitchen eating ham. @garrick_moor I think this is your Biscuit! He's registered to 14 Alder Row and the number on file is 07700 900418 — I've texted it too but in case you don't see it, he's safe with me."

Reviewer check: u/garrick_moor's own public post in c/LostPetsKelby eight days ago lists the same address and number and asks people to share them if they see the cat.
The comment was reported by 1 user, reason "personal information".""",
0, 2, L_card(["3.6"]),
twin=([("u/garrick_moor's own public post in c/LostPetsKelby eight days ago lists the same address and number and asks people to share them if they see the cat.", "u/garrick_moor has never posted his address or number anywhere on Loomwell; u/hanna_vey works at the vet clinic that holds Biscuit's microchip record.")], 1)),

# LY19 office vs home address of a councillor (twin)
Y("Does the flagged post fall within the private information prohibition (3.6)?",
"""Community: c/Brantford_Civic
Post by u/civicminded_ro, title: "Bin collection cuts — here's who to complain to"

Body:
"Want to complain about fortnightly collections? Councillor Oyelaran chairs the committee that voted it through. Her contact: 22 Mercer Street (ward office), 01632 960771 (ward office line). She holds drop-ins Tuesdays and Thursdays 10–12. Go in person, be polite, bring photos of the overflowing bins on Lark Lane."

Reviewer check: 22 Mercer Street and 01632 960771 are both listed on the Brantford council website as Councillor Oyelaran's ward office and ward office line.
Reported by 1 user, reason "doxxing".""",
0, 2, L_card(["3.6"]),
twin=([("22 Mercer Street and 01632 960771 are both listed on the Brantford council website as Councillor Oyelaran's ward office and ward office line.", "22 Mercer Street is Councillor Oyelaran's family home according to the electoral roll, and 01632 960771 is her home landline; the council website lists her ward office at 3 Kiln Lane.")], 1)),

# LY20 coded dehumanization with emoji
Y("Is this comment hateful conduct as defined in section 3.1?",
"""Community: c/PellRoadResidents
Thread: "Planning approved for the Ormist temple extension on Pell Road"

Reviewer glossary: "Ormist" — adherent of Ormism, a religious minority.

Comment by u/ladder_and_lamp (score +18):
"Another 🐀 family moved in right by the temple this week. That's six this year. Pretty soon the whole street will be one big nest and we'll all be paying for the extermination. Nobody asked us."

Reply by u/sabine_q: "Who are you calling rats?"
Reply by u/ladder_and_lamp: "Didn't call anyone anything. It's an emoji 🤷"

The account has no other posts in the thread. Earlier the same day it posted in c/PellRoadResidents asking for a recommendation for a plumber.""",
1, 3, L_card(["3.1"])),

# LY21 criticism of religion vs exclusion of adherents (twin)
Y("Is this post hateful conduct under 3.1?",
"""Community: c/PhilosophyPub (argument-friendly; "attack ideas, not people")
Post by u/quill_and_ash, title: "Why does Ormism get a free pass?"

Body:
"Ormism is a ridiculous belief system. Its creation story is internally incoherent, its dietary laws are arbitrary, and its priesthood has covered up abuse for decades while lecturing everyone else on purity. I've read the Codex twice. Nobody should give its teachings any special deference in schools. Change my mind."

Reviewer glossary: "Ormism" — a minority religion; its adherents are called Ormists.
The post was reported by 5 users; reasons "hate speech" (4) and "harassment" (1). Top reply is a long rebuttal from a practising Ormist; the author replied civilly.""",
0, 2, L_card(["3.1"]),
twin=([("Nobody should give its teachings any special deference in schools.", "Nobody should let Ormists teach in our schools.")], 1)),

# LY22 screenshot of hate: amusement vs condemnation (twin)
Y("Does this post violate section 3.1?",
"""Community: c/OldInternetArchaeology (people sharing screenshots of their old online lives)
Post by u/abernathy_k, title: "group chat from 2014"

Attachment: a screenshot of a group-chat message reading "all [slur for disabled people]s should be put down at birth", sent by a contact labelled "Maz".
Caption: "found this in my old group chat from 2014 lmaooo"

Replies: u/weir_hollow "💀💀", u/pellam_j "the 2014 energy is unmatched", u/rosehip_tea "yikes"

No further comment from the author. The account has posted 30 similar screenshots in the community, mostly of embarrassing song lyrics and old usernames.""",
1, 3, L_card(["3.1"]),
twin=([("found this in my old group chat from 2014 lmaooo", "found this in my old group chat from 2014. Can't believe I used to be friends with people who talk like this about my brother")], 0)),

# LY23 sexualizing a public figure vs criticising play (twin)
Y("Does the comment violate 3.2?",
"""Community: c/FootyChat (148k members)
Thread: "Rovers Women 1–3 Castlebridge — post-match discussion"

Comment by u/marl_thorne (score +9):
"Arden can play up front for me any night, if you know what I mean 😏 those shorts should be illegal"

Context: Kezia Arden is Rovers' starting striker; her verified Loomwell account has 340k followers. The comment sits under a highlights clip of her 70th-minute chance, in a thread with 312 comments.
Reply by u/ferrer_six: "grow up"
Reply by u/marl_thorne: "just saying what everyone's thinking"

Reported by 3 users; reasons "harassment" (2) and "other" (1). u/marl_thorne has no prior removals.""",
1, 2, L_card(["3.2"]),
twin=([("Arden can play up front for me any night, if you know what I mean 😏 those shorts should be illegal", "Arden couldn't hit a barn door from six yards 🙄 worst finishing I've seen all season, she should be benched")], 0)),
]
