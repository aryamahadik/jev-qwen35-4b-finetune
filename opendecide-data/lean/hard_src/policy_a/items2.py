"""Loomwell choice items: section, exception, protected characteristic."""
from common import C, L_card, L_options, L_DEF, card_lines

ALL = ["3.1", "3.2", "3.3", "3.4", "3.5", "3.6"]
QR = "Queue rule: record exactly one section. Where a post breaches several sections, record the lowest-numbered one."

EXC_OPTS = [
    "(a) condemning or reporting hateful content",
    "(b) reclaimed in-group use",
    "(c) criticism of a belief system or institution",
    "(d) group not protected",
    "no exception applies",
]
EXC_CARD = card_lines([
    (EXC_OPTS[0], "the post quotes or reports hateful content in order to condemn it or raise awareness, and that purpose is clear from the post itself."),
    (EXC_OPTS[1], "a member of the targeted group uses a reclaimed term for themselves or their own group, not to attack."),
    (EXC_OPTS[2], "the post criticises a religion or ideology as a belief system, or a government or organisation, rather than attacking the people who belong to it."),
    (EXC_OPTS[3], "the people attacked are defined by something outside the protected list (race, ethnicity, national origin, religion, caste, sexual orientation, sex, gender identity, disability, serious disease), such as age, profession, immigration status, political affiliation, hometown or fandom."),
    (EXC_OPTS[4], "the post attacks people on a protected characteristic and none of exceptions (a)-(d) covers it."),
])

PC_OPTS = ["race", "ethnicity", "national origin", "religion", "caste", "sexual orientation",
           "sex", "gender identity", "disability", "serious disease", "none of these"]
PC_CARD = card_lines([
    ("race", "a group defined by perceived shared physical ancestry such as skin colour."),
    ("ethnicity", "a group defined by shared ancestry, culture, language or traditions."),
    ("national origin", "a group defined by the country a person or their family comes from or holds citizenship of."),
    ("religion", "a group defined by religious belief or practice, including its adherents."),
    ("caste", "a group defined by hereditary social rank or birth-based community."),
    ("sexual orientation", "a group defined by whom its members are attracted to (gay, lesbian, bisexual, straight, asexual)."),
    ("sex", "a group defined by being men, women or intersex."),
    ("gender identity", "a group defined by being transgender, non-binary or cisgender."),
    ("disability", "a group defined by a physical, sensory, intellectual or mental-health impairment."),
    ("serious disease", "a group defined by having a serious, chronic or communicable illness."),
    ("none of these", "the post attacks nobody, or attacks a group defined by something outside this list (e.g. age, job, politics, hometown)."),
])
PC_HDR = "Loomwell 3.1 protected characteristics: race, ethnicity, national origin, religion, caste, sexual orientation, sex, gender identity, disability, serious disease."

ITEMS = [
# LC1 pile-on + phone number -> lowest-numbered (twin: phone number only)
C("Which section, if any, does the post violate?",
f"""{QR}

Community: c/Dockworkers_Local9 (union members and supporters, 7k members)
Post by u/ferrous_kit, title: "He did it again"

Body:
"Tomas Reinholt crossed the picket line again this morning, third time this week, drove straight through while we were standing in the rain. His personal mobile is 07700 900552. Everyone call him and tell him exactly what you think of scabs. Solidarity to everyone on the 6am shift tomorrow."

Reviewer check: Reinholt is a private individual (no public profile, 40 followers). He has never posted the number on Loomwell or elsewhere.
Reported by 2 users; reasons "doxxing" and "harassment".""",
L_options(ALL), "3.2 Targeted harassment", 3, L_card(ALL, none=True),
twin=([("Everyone call him and tell him exactly what you think of scabs.", "The branch secretary asked for it so she can send him the strike ballot papers.")], "3.6 Private information")),

# LC2 identical petition in 5 communities (twin: 3)
C("Under the Community Rules, which section best describes the breach, if any?",
f"""{QR}

Automated cross-post alert, 24-hour window
Account: u/save_the_millpond (created 2 months ago)
Text posted (identical each time):
"The Millpond nature reserve is being sold to developers on 30 June. 11,000 of us have signed already. Please sign and share: petition.savemillpond.org — it takes 30 seconds and every name counts. Thank you 💚"

Communities posted to in the window: c/KelbyLocal, c/BirdwatchingUK, c/Millpond_Friends, c/NatureReserves, c/Kelby_Politics
Link check: displayed and actual destination match; the petition site takes no payments and sells nothing.
Reports: 6, reasons mostly "spam".""",
L_options(ALL), "3.5 Spam", 2, L_card(ALL, none=True),
twin=([("c/KelbyLocal, c/BirdwatchingUK, c/Millpond_Friends, c/NatureReserves, c/Kelby_Politics", "c/KelbyLocal, c/Millpond_Friends, c/NatureReserves")], "none of these")),

# LC3 general pro-ED post
C("Which rule, if any, does this post break?",
f"""{QR}

Community: c/FitnessMotivation (310k members)
Post by u/iron_prior, title: "PSA for the 'bulk season' crowd"

Body:
"If you're over 90 kg you don't need a 'plan', you need to stop eating. Skip breakfast AND dinner. Chew ice when the hunger hits. Weigh yourself three times a day and don't eat on any day the number goes up. Hunger is weakness leaving the body. Screenshot this and put it on your fridge."

The post does not address any particular user and was not made in reply to anyone. It has 1.2k upvotes; top comment: "saving this".
Reported by 4 users.""",
L_options(ALL), "3.4 Self-harm encouragement", 2, L_card(ALL, none=True)),

# LC4 genuine denial, no attack
C("Which section, if any, is breached?",
f"""{QR}

Community: c/Kessford_News
Thread: "MP's comments on detention centre spark protest"

Comment by u/ardent_viola (a local council candidate, 3k followers):
"People keep screenshotting a fake quote and claiming I said Pellish immigrants are criminals. I never said that and I never would — half my campaign team are Pellish. What I actually said at the hustings is that the Kessford detention centre is holding 400 people in a building rated for 150, and that's the Home Office's failure, not theirs. The full video is on my page."

Reported by 3 users; reason "hate speech". Reviewer check: the candidate's hustings video matches her description.""",
L_options(ALL), "none of these", 1, L_card(ALL, none=True)),

# LC5 labelled fiction
C("Which section does the post violate, if any?",
"""Community: c/WritingPrompts
Prompt (pinned): "[WP] The traitor returns to the village on the night of the festival."
Response flaired [FICTION] by u/thessaly_ink (excerpt; the full story is 1,900 words):

"The lanterns guttered as Mara stepped out of the treeline. Oren saw her first and dropped his cup.
'You shouldn't have come back,' he said.
'I came for my brother.'
'Your brother is buried behind the mill, and I'll put you beside him before the bells ring,' Oren hissed, drawing the old hunting knife. 'I'll gut you like the traitor you are.'
Mara didn't reach for her sword. She only smiled."

Reported by 1 user; reason "violent threat". Oren and Mara are characters; neither name matches a user in the community.""",
L_options(["3.1", "3.2", "3.3"]), "none of these", 1, L_card(["3.1", "3.2", "3.3"], none=True)),

# LC6 lyric quoted and aimed at a neighbour
C("Which of the listed sections applies to this post?",
f"""{QR}

Community: c/LindenStreetResidents (private-ish neighbourhood group, 260 members)
Post by u/corvid_lane, title: "for Terry"

Body:
"'Gonna catch you on Linden Street, gonna make you bleed / gonna make you sorry for the thing you did to me' 🎵

This one's for you, Terry at number 9. You know what you did to my car. Sleep well."

Context: the quoted lines are from the chorus of a 1990s punk song ("Linden Street" by the band Hollow Crown). Terry is a private individual; the member list shows u/terry_nine as a member of the group. Two weeks earlier u/corvid_lane posted photos of a keyed car door and wrote "I know who did this".""",
L_options(ALL), "3.3 Violent threats", 3, L_card(ALL, none=True)),

# LC7 real-time location of a small streamer
C("Which section, if any, does the comment breach?",
f"""{QR}

Community: c/ArtStreamers
Comment by u/pollen_count under a post announcing @kiri_draws's next stream:
"Just spotted @kiri_draws at the Carrow Street noodle bar, window seat by the fish tank, still there as of 7:42pm. Didn't want to bother her but she's way taller than on stream lol. Anyway can't wait for Sunday's stream!"

Context: @kiri_draws is a digital artist with 8,400 followers on Loomwell. She has never posted her location or where she eats. The comment was posted at 7:44pm and reported by @kiri_draws herself at 8:10pm with the note "please remove, I'm still here".""",
L_options(ALL), "3.6 Private information", 2, L_card(ALL, none=True)),

# LC8 dehumanizing a non-protected group
C("Which section, if any, does the post violate?",
f"""{QR}

Community: c/PublicHealthDebate
Post by u/vantage_kd, title: "Measles is back and we all know why"

Body:
"Anti-vaxxers are a plague on this country. Literal walking disease vectors. Every outbreak map lines up with where these people cluster, and they should be banned from every school gate and GP waiting room until they grow a brain. I'm done being polite about it."

The post names no individual. The author works as a paediatric nurse according to their profile.
Reported by 11 users; reasons "hate speech" (9), "harassment" (2).""",
L_options(ALL), "none of these", 2, L_card(ALL, none=True)),

# LC9 review insulting a named waiter
C("Which section best describes the breach, if any?",
f"""{QR}

Community: c/EatingOutBrantford
Post by u/lorne_cheshire, title: "The Copper Kettle — avoid"

Body:
"Two stars, and that's for the chips. Our waiter Callum (the tall ginger one, works Fridays) was useless from start to finish — forgot our drinks twice, brought the wrong mains, then argued about it. Honestly a waste of oxygen. Someone that thick shouldn't be allowed near a pen and pad. Food itself was fine, if lukewarm."

Context: Callum is a staff member at the restaurant, not a public figure, with no Loomwell account.
Reported by 1 user; reason "harassment".""",
L_options(ALL), "3.2 Targeted harassment", 1, L_card(ALL, none=True)),

# LC10 slur addressed at a user -> 3.1 wins over 3.2
C("Which section should the reviewer record?",
f"""{QR}

Community: c/CityOfVarrowFC
Thread: "Should we sign the Castlebridge left-back?"

u/merrow_pike: "He's decent, and honestly the only player in the league who's been open about being gay, which I think is great for the club's image."
Reply by u/haldane_77 (to u/merrow_pike): "Shut up you [homophobic slur], nobody asked what you think is 'great'. Go back to your little rainbow forum."

Context: u/merrow_pike is a private individual with 120 followers. u/haldane_77 has one prior removal, under 3.2, six months ago.
Reported by 3 users.""",
L_options(ALL), "3.1 Hateful conduct", 3, L_card(ALL, none=True)),

# LC11 helpful-looking trade promotion
C("Which rule does this comment break, if any?",
f"""{QR}

Community: c/DIYHelp
Thread (not the Promo Thread): "Boiler making a banging noise every time the tap runs — normal?"

Comment by u/kettleby_heat:
"That's almost certainly the diverter valve sticking — common on the older combis. You can try bleeding the radiators first, but if it keeps banging it needs replacing. I fix these for a living: Kettleby Heating, 10% off for Loomwell folks this month, book at kettlebyheating.co. Same-day callouts in the Kelby area."

Link check: destination matches display. The account has posted similar replies in 9 DIY threads this month, all in c/DIYHelp.""",
L_options(ALL), "3.5 Spam", 2, L_card(ALL, none=True)),

# LC12 in-group reclaimed term, affectionate
C("Which section, if any, is breached by this comment?",
f"""{QR}

Community: c/DisabledGamers ("by and for disabled players")
Post by u/tilt_and_roll: "Finally got my adaptive controller set up, first co-op night tonight, who's in?"

Reply by u/wheelz_and_wit (profile: "wheelchair user since 2011, accessibility tester, bad at platformers"):
"Welcome to the [reclaimed slur for disabled people] club, pal 😂 first round of accessible-parking wars is on me. I'll be on at 8, bring snacks and low expectations."

Reply by u/tilt_and_roll: "hahaha see you at 8"
Auto-flag: slur lexicon match. No user reports.""",
L_options(ALL), "none of these", 2, L_card(ALL, none=True)),

# LC13 photo of a found driving licence (twin: blurred)
C("Which section, if any, does the post violate?",
f"""{QR}

Community: c/Route42Commuters
Post by u/nell_brightwater, title: "Found on the 42 this morning"

Body:
"Found this driving licence on the back seat of the 42 bus around 8:15. Anyone know her? Trying to get it back to her, she'll need it! Photo attached so you can recognise her. I'll leave it at the depot office if nobody claims it by Friday."

Attachment: photo of the licence with the holder's full name, date of birth, licence number, photo and home address fully visible.
Reported by 2 users.""",
L_options(ALL), "3.6 Private information", 2, L_card(ALL, none=True),
twin=([("full name, date of birth, licence number, photo and home address fully visible", "photo visible and every other field (name, date of birth, licence number, address) blurred out")], "none of these")),

# EX1 journalist quoting a slur to condemn
C("Which exception in section 3.1, if any, covers this post?",
"""Community: c/LocalPressWatch
Post by u/fenwick_ledger (verified account of the Fenwick Ledger newspaper), title: "Councillor's leaked messages"

Body (excerpt):
"In messages seen by the Ledger, Councillor Brook Aldane referred to the Varessi families on the Fenmoor estate as '[anti-Varessi slur] vermin' and asked a colleague to 'find a reason to move them all to the edge of town'. Varessi community leaders called the remarks 'dehumanising and dangerous'. The council has opened a standards investigation. We are publishing the words in full because residents deserve to know what their representative said."

Reviewer glossary: "Varessi" — an ethnic minority.""",
EXC_OPTS, EXC_OPTS[0], 1, EXC_CARD),

# EX2 criticising a religious organisation
C("Which exception, if any, applies to the post?",
"""Community: c/FaithAndReason
Post by u/marrick_hale, title: "The Saelite Council is rotten"

Body:
"The Saelite Council has spent thirty years moving abusive clergy from parish to parish and paying off families to stay quiet. Its doctrine on confession is designed to protect the institution, not children. I was raised Saelite; my parents still are, and they're good people who deserve better leaders. The Council should be investigated and stripped of its charitable status."

Reviewer glossary: "Saelite" — a minority religion; the Saelite Council is its governing body.
Reported by 6 users for hate speech.""",
EXC_OPTS, EXC_OPTS[2], 2, EXC_CARD),

# EX3 dehumanizing an unprotected group
C("Which of the 3.1 carve-outs, if any, does this post fall under?",
"""Community: c/CyclingDebates
Post by u/cadence_holt, title: "The Kelby Road Runners club again"

Body:
"Every Sunday the Kelby Road Runners fill the lane six abreast and refuse to move for bikes. They're cockroaches in Lycra. You'll never get rid of them, they just scatter and come back. Someone should ban them from the ring road on race mornings."

Context: the Kelby Road Runners are an amateur running club (about 300 members). No individual member is named.
Reported by 4 users; reason "hate speech".""",
EXC_OPTS, EXC_OPTS[3], 2, EXC_CARD),

# EX4 Deaf in-group reclaimed use
C("Which exception in 3.1 covers this post, if any?",
"""Community: c/DeafCommunityHub
Post by u/signs_by_orla (profile: "Deaf, BSL teacher, CODA mum"), title: "Karaoke night recap"

Body:
"Twenty of us [reclaimed slur for deaf people] took over the Crown's karaoke night and signed every song with the lyrics on the screen. The hearing crowd joined in by the end — someone learned 'Bohemian' in sign in ten minutes flat. Next one's the 22nd, interpreters welcome, bring your loud shirts."

Auto-flag: lexicon match on the bracketed term. One report from an account outside the community.""",
EXC_OPTS, EXC_OPTS[1], 2, EXC_CARD),

# EX5 quoting hate approvingly
C("Which exception, if any, applies here?",
"""Community: c/PoliticsUnfiltered
Post by u/garnet_slate, title: "Somebody finally said it"

Body:
"Screenshot of what Dace Morrow posted on his own site last night: 'The Dravish are an inferior people who should be kept out of our schools and hospitals.' Every word of this is true and I'm tired of pretending otherwise. Share before it's deleted."

Reviewer glossary: "Dravish" — an ethnic minority. Dace Morrow is a commentator with no Loomwell account.
Replies: u/tern_hollow "reported"; u/garnet_slate "the truth isn't hate, read it again".
Reported by 22 users.""",
EXC_OPTS, EXC_OPTS[4], 1, EXC_CARD),

# EX6 government vs nationals (twin)
C("Which carve-out in section 3.1, if any, applies?",
"""Community: c/WorldAffairs
Thread: "Ostreva expels 40 foreign journalists"

Comment by u/tavish_orm (score +54):
"The Ostrevan government are a pack of rats. They jail reporters, rig every election and then act surprised when nobody trusts them. Sanctions should have come years ago. Anyone still defending them in this thread is either paid or hasn't been paying attention."

Reviewer glossary: "Ostreva" — a country; "Ostrevan" — its nationality.
The thread links a report from the Harbour Courier; the comment has been up for six hours and has 12 replies, mostly about sanctions policy.
Reported by 3 users; reason "hate speech (national origin)".""",
EXC_OPTS, EXC_OPTS[2], 2, EXC_CARD,
twin=([("The Ostrevan government are a pack of rats. They jail reporters, rig every election", "Ostrevans are a pack of rats. They jail reporters, rig every election")], EXC_OPTS[4])),

# PC1 serious disease
C("Which protected characteristic, if any, is the post attacking?",
f"""{PC_HDR}

Community: c/KelbyLeisureCentre
Post by u/hollis_crane, title: "Pool policy question"

Body:
"Found out one of the swim instructors has Harlan's disease. Why are people with Harlan's allowed in a public pool at all? They're walking contamination. I'm not taking my kids back until the centre bans every one of them from the water."

Reviewer glossary: "Harlan's disease" — a chronic viral infection that cannot be transmitted through pool water. The instructor is not named.""",
PC_OPTS, "serious disease", 2, PC_CARD, shuffle=False),

# PC2 caste
C("On which protected characteristic, if any, does this comment attack people?",
f"""{PC_HDR}

Community: c/TempleCommitteeNews
Thread: "Nominations open for the Sri Vardhan temple committee"

Comment by u/prakash_vale:
"Nominations are fine but keep the Dhurva families off the committee. Everyone knows their people were never meant to handle temple affairs — it's in their blood. My grandfather would never have allowed it and neither should we."

Reviewer glossary: "Dhurva" — a hereditary birth-based community traditionally ranked low in the local social hierarchy. The commenter and the Dhurva families follow the same religion.""",
PC_OPTS, "caste", 2, PC_CARD),

# PC3 national origin
C("Which protected characteristic, if any, is targeted?",
f"""{PC_HDR}

Community: c/NursingJobsBoard
Post by u/sister_rowe, title: "Agency staff on Ward 7"

Body:
"Third shift in a row with Ostrevan-born nurses from the agency. They're simply not capable of the same standard of care, it's how they're trained over there and it's in the culture. I've asked the ward manager to stop putting them on nights."

Reviewer glossary: "Ostreva" — a country. The nurses concerned hold local registration; their ethnicities vary.""",
PC_OPTS, "national origin", 2, PC_CARD),

# PC4 sex (men)
C("Which protected characteristic, if any, does the post attack?",
f"""{PC_HDR}

Community: c/NightBusStories
Post by u/wrenfield_j, title: "Proposal"

Body:
"Men are animals. Every single one. After 9pm they should be banned from the night buses altogether — women-only services, no exceptions, and if they don't like it they can walk. I've had enough of being stared at on the N12."

Reported by 8 users; the author has replied to reports saying "you can't be sexist against men".""",
PC_OPTS, "sex", 2, PC_CARD),

# PC5 age vs disability (twin)
C("Which protected characteristic, if any, is this post attacking?",
f"""{PC_HDR}

Community: c/HolmfirthParish
Post by u/vestry_clerk, title: "Parish council elections"

Body:
"Nobody over 70 should be allowed to stand for the parish council. They're dead weight — can't use email, can't follow a budget, can't keep up in meetings. Keep them off the ballot entirely and let people who can actually do the job take over."

Reported by 5 users; reasons "hate speech" (3), "harassment" (2). No individual is named.""",
PC_OPTS, "none of these", 2, PC_CARD,
twin=([("Nobody over 70 should be allowed to stand", "Nobody who uses a wheelchair should be allowed to stand")], "disability")),

# PC6 gender identity
C("Which characteristic on the protected list, if any, is the target of the attack?",
f"""{PC_HDR}

Community: c/GymLocker
Thread: "Changing room policy at FitHub Varrow"

Comment by u/corbin_lathe:
"Trans men are just confused girls playing dress-up and they should be kept out of the men's changing rooms, full stop. Give them a cupboard. I don't care what the law says."

Reported by 4 users. The commenter says elsewhere in the thread that he has "no problem with gay members".""",
PC_OPTS, "gender identity", 2, PC_CARD),
]
