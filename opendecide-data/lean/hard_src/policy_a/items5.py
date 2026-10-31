"""Meridian workplace items and Quillon enforcement items."""
from common import (Y, C, M_card, M_options, Q_TIER_TEXT, Q_action_card, Q_ACTION_OPTS,
                    Q_TIER_OPTS, Q_tier_card, card_lines, Q_ACTIONS)

ALLM = ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6"]
MR = "Meridian Workspace Acceptable Use Policy — reviewers cite one clause; if several apply, cite the lowest-numbered."
QH = ("Enforcement ladder: apply the most severe action whose conditions are met. "
      "Strikes count only if issued in the 90 days before the date of the new violation.")

ITEMS = [
# MY1 weapon joke (twin: lawyer)
Y("Does this message breach §4.3 of the Meridian policy?",
"""Meridian Workspace — channel #finance-questions (84 members)
Message by Rhys Calloway (Senior Designer), Tuesday 11:42:

"lol if Finance rejects my expense report AGAIN I'm bringing my crossbow to the Q3 review 🏹😂 third time they've bounced it for a missing receipt I literally attached. @Priya can you take a look when you have a sec?"

Reactions: 😂 x6, 👀 x2.
Reply by Priya Nandakumar (Finance): "haha I'll look now, sorry!"

The message was reported by a member of the Finance team. HR has no prior complaints about Rhys. The company has no archery club or related event.""",
1, 2, M_card(["4.3"]),
twin=([("I'm bringing my crossbow to the Q3 review 🏹😂", "I'm bringing my lawyer to the Q3 review ⚖️😂")], 0)),

# MY2 age 40+ (twin: 25-year-old)
Y("Is this a §4.1 violation?",
"""Meridian Workspace — private channel #hiring-platform-team (6 members)
Message by Ella Voss (Engineering Manager), during a discussion of two shortlisted candidates:

"Both CVs are solid but honestly we need someone who'll hit the ground running, not another 55-year-old who'll need the font size bumped up and a nap after lunch. Let's push the other one through to final round."

Replies: Jonas Pell: "ha, fair", Mira Adeyemi: "can we focus on the tech test results?"

The candidates' test scores were within two points of each other. HR policy notes that the channel is covered by the Acceptable Use Policy.""",
1, 2, M_card(["4.1"]),
twin=([("not another 55-year-old who'll need the font size bumped up and a nap after lunch", "not another 25-year-old who'll need everything explained twice and a nap after lunch")], 0)),

# MY3 quoting to report
Y("Does Owen's message violate §4.1?",
"""Meridian Workspace — direct message to #people-team-reports (the HR reporting inbox)
Message by Owen Achterberg (Support Analyst), Friday 16:05:

"Hi, I'd like to report something from this morning's stand-up. When Kasia said she'd be leaving early for Friday prayers, Dean said 'of course she is, they always find a way to skive, it's in the religion'. A few people laughed. Kasia went quiet for the rest of the call. I've attached the meeting timestamp (09:14). I don't want to make a fuss but I don't think that's OK."

The message was flagged by the keyword scanner for the phrase "it's in the religion".""",
0, 1, M_card(["4.1"])),

# MY4 solicitation (twin: #marketplace first post)
Y("Does this post break the solicitation clause (§4.6)?",
"""Meridian Workspace — channel #general (1,240 members)
Message by Lorna Figg (Payroll), Monday 09:12:

"Morning all! 🍪 My daughter's Guide unit is selling biscuits to fund their summer camp — £3 a box, six flavours, the caramel ones are dangerously good. DM me your order by Friday and I'll bring them in next Monday. Thank you!!"

Lorna has not posted any other sales or fundraising messages this week. The company runs a separate #marketplace channel for personal sales. The message received 14 replies placing orders.""",
1, 1, M_card(["4.6"]),
twin=([("Meridian Workspace — channel #general (1,240 members)", "Meridian Workspace — channel #marketplace (610 members)")], 0)),

# MY5 colleague health information shared kindly
Y("Would a reviewer correctly cite §4.5 for this message?",
"""Meridian Workspace — channel #design-team (14 members)
Message by Tobias Rann (Design Lead), Wednesday 08:50:

"Quick heads-up team: Priya's off for the rest of the week — her latest IVF round didn't work and she's taking some time. Please be gentle with her when she's back and don't ask about it unless she brings it up. I'll cover her reviews. ❤️"

Priya had told Tobias privately and asked him to let the team know she'd be off "for personal reasons". The authorised system for health-related absence information is the HR portal.
Reactions: ❤️ x9.""",
1, 3, M_card(["4.5"])),

# MY6 private civil critique (not bullying)
Y("Is this message bullying under §4.2?",
"""Meridian Workspace — direct message (one-to-one)
From: Hana Sorvik (Head of Content) To: Dominic Leary (Content Writer), Thursday 17:30

"Hi Dom — I read the draft deck for the Harlow pitch. Honest feedback: it isn't at the standard we need yet. The structure buries the key numbers on slide 14, three of the case studies are out of date, and the tone is too casual for this client. Can you rework it by Monday? Happy to sit down for 20 minutes tomorrow and go through it together if that helps."

Dominic forwarded the message to HR with the note "feels harsh". Hana has sent similar review messages to other team members.""",
0, 2, M_card(["4.2"])),

# MY7 pregnancy stereotype
Y("Does this message violate the discriminatory remarks clause?",
"""Meridian Workspace — private channel #account-leads (5 members)
Message by Grant Holloway (Sales Director), during account allocation for the new financial year:

"Let's not give the Halden account to Sara. She's pregnant and she'll be checked out mentally by the summer, they always are. Give it to Marcus, he'll actually be around to see it through."

Sara Imre had not asked to be taken off any accounts and has not announced leave dates. Replies: Marcus: "happy to take it". No one else replied.""",
1, 1, M_card(["4.1"])),

# MY8 non-sexual clothing compliment
Y("Does Ade's comment amount to sexual harassment under §4.4?",
"""Meridian Workspace — thread under a post in #all-hands-questions

Post by Lucía Ferrante (Product Manager): slides from her all-hands presentation on the Q2 roadmap.
Reply by Ade Okonjo (Product Manager, same team), 14:10:
"Great presentation, Lucía! The roadmap slide finally made the dependencies click for me. Also, that green dress is a lovely colour on you — very on-brand with the new logo 😄"
Reply by Lucía: "haha thanks Ade, it was deliberate!"

The keyword scanner flagged the reply for "dress". There have been no previous reports involving Ade and no other messages between them outside work channels.""",
0, 2, M_card(["4.4"])),

# MC1 salary screenshot
C("Which clause of the policy does the message breach, if any?",
f"""{MR}

Channel: #random (1,180 members)
Message by Callum Brightwell (Finance Analyst), Friday 17:55:

"Not saying anything, just saying 👀 [image attached]"
Attachment: a cropped screenshot of a spreadsheet showing names and annual salaries for the six members of the Brand team, taken from the payroll system.

Replies: "WOW", "no way Josh is on that much", "delete this lol".
Callum has access to payroll data as part of his role. The authorised system for salary data is the payroll system.""",
M_options(ALLM), "§4.5 Confidential data", 1, M_card(ALLM, none=True)),

# MC2 religious 'banter'
C("Which clause, if any, does this message violate?",
f"""{MR}

Channel: #client-services (42 members)
Message by Neil Parrish (Account Manager), Monday 10:02, about scheduling a client lunch:

"Don't put Yusuf on the Brightline lunch this month lol, he'll just sit there staring at our plates like a hungry dog until sunset 😂 Ramadan rules."

Reactions: 😂 x3.
Yusuf Demir (Account Executive) is a member of the channel. He did not reply. The lunch invitation list was later sent without his name.""",
M_options(ALLM), "§4.1 Discriminatory remarks", 2, M_card(ALLM, none=True)),

# MC3 charity fundraising in #general
C("Which clause best fits this message, if any?",
f"""{MR}

Channel: #general (1,240 members)
Message by Anya Petrov (UX Researcher), Wednesday 12:30:

"Hi everyone 💛 I'm running the Kelby 10k on Sunday for the children's hospice that cared for my nephew last year. If you can spare anything, my fundraising page is in the link below — every £5 helps. Thank you so much, and see you at the finish line if you're running too!"

This is Anya's only fundraising post. The company's #marketplace channel exists for personal sales and fundraising. The hospice is not a company-sponsored charity.""",
M_options(ALLM), "§4.6 Solicitation", 2, M_card(ALLM, none=True)),

# MC4 intimidation about contract (not physical threat)
C("Which policy clause, if any, applies?",
f"""{MR}

Channel: #proj-harlow (shared with the client's team; 23 members)
Message by Gideon Marsh (Delivery Director), Tuesday 15:48, replying to a contractor who had questioned his timeline estimate in the channel:

"@Ines keep pushing back on my estimates in front of the client and see how long your contract lasts. I'd think very carefully about your next message."

Ines Carvalho is a contractor on a rolling monthly agreement. She did not reply in the channel and later messaged HR. There is no mention of physical harm or weapons.""",
M_options(ALLM), "§4.2 Bullying and intimidation", 2, M_card(ALLM, none=True)),

# MC5 sexual comment about photos
C("Which clause does the message breach, if any?",
f"""{MR}

Direct message from Kieran Doyle (Sales Executive) to Leah Brandt (Marketing Coordinator), Saturday 23:40:

"saw your beach pics on insta 🔥 didn't know you were hiding all that under the cardigans at work. you should dress like that for the Monday stand-up 😉"

Leah did not reply and reported the message on Monday. The two work in different teams and had only spoken in project meetings.""",
M_options(ALLM), "§4.4 Sexual harassment", 1, M_card(ALLM, none=True)),

# MC6 good-faith policy discussion
C("Which clause, if any, is breached?",
f"""{MR}

Channel: #town-hall-questions (1,240 members)
Message by Petra Lindqvist (Engineering Manager), Thursday 09:15:

"Question for Friday's town hall: I'm not sure the new parental-leave top-up is fair to colleagues without children, who don't get any equivalent benefit. Could we talk about whether a general sabbatical or caregiver-leave scheme might be fairer overall? Genuinely asking — I know a lot of people are really happy with the change and I don't want to take anything away from parents."

Replies: some agree, some disagree; the discussion stays civil.""",
M_options(ALLM), "none of these", 1, M_card(ALLM, none=True)),

# QC1 tier 1 insult, strike outside window (twin: inside)
C("Which enforcement action does the Quillon ladder require?",
f"""{Q_TIER_TEXT}

{QH}

Case QL-7781
Date of new post: 2 May 2026
Post by @harbourlight_ben, replying to @mae_tolland in a thread about a football match:
"you absolute clown, that was never a penalty and you know it"

Account strike history: one strike, issued 10 January 2026 (spam).
Review finding: the post is a mild insult aimed at a user and breaches no other rule.""",
Q_ACTION_OPTS, "remove only", 3, Q_action_card(),
twin=([("one strike, issued 10 January 2026 (spam).", "one strike, issued 10 February 2026 (spam).")], "remove and strike")),

# QC2 tier 2 slur, two strikes
C("What action should be taken under the enforcement ladder?",
f"""{Q_TIER_TEXT}

{QH}

Case QL-7802
Date of new post: 18 June 2026
Post by @cask_and_barrel in a thread about a local council election:
"of course the [homophobic slur] candidate won in the city centre, what did anyone expect"

Account strike history: strike on 2 April 2026 (Tier 1 insult); strike on 30 May 2026 (Tier 2 harassment); strike on 11 November 2025 (Tier 1 spam).
Review finding: the post uses a slur to describe a candidate; there is no threat, dehumanizing comparison or exposure of personal data.""",
Q_ACTION_OPTS, "7-day suspension", 3, Q_action_card()),

# QC3 tier 3 directed self-harm, no strikes
C("Which action does the ladder call for?",
f"""{Q_TIER_TEXT}

{QH}

Case QL-7815
Date of new post: 9 March 2026
Reply by @vesper_quill to @noor_amble, who had posted that she was "having a hard week and feeling like a burden":
"then do everyone a favour and kill yourself. seriously"

Account strike history: none; account created 2021.
Review finding: the reply tells a specific person to kill themselves. No other rule is engaged.""",
Q_ACTION_OPTS, "7-day suspension", 2, Q_action_card()),

# QC4 tier 4 home address, no strikes
C("Which enforcement action applies?",
f"""{Q_TIER_TEXT}

{QH}

Case QL-7840
Date of new post: 22 July 2026
Post by @ferris_wheel_kate, quoting a post by the journalist @ilse_rendall:
"Since @ilse_rendall loves writing about 'accountability' so much, she lives at 41 Corrin Terrace, Holm, blue door. Maybe people should go and ask her about accountability in person."

Account strike history: none.
Review finding: the address is Ilse Rendall's home address and has never been published by her. The post contains no explicit threat.""",
Q_ACTION_OPTS, "permanent ban", 2, Q_action_card()),

# QC5 counter-speech by an account with 3 strikes
C("What does the ladder require for this case?",
f"""{Q_TIER_TEXT}

{QH}

Case QL-7866
Date of new post: 4 August 2026
Post by @lark_and_linden:
"Got this in my DMs this morning after my article on the Varessi housing report: 'your people are [anti-Varessi slur] rats and should be gassed'. Posting it so people can see what Varessi journalists deal with every single day. Reported to Quillon and to the police."

Account strike history: strikes on 20 May 2026, 3 June 2026 and 1 July 2026 (all Tier 1 spam).
Review finding: the quoted message is shown in order to condemn and report it.""",
Q_ACTION_OPTS, "no action", 3, Q_action_card()),

# QC6 tier 1 spam with 3 strikes
C("Which action should the reviewer apply?",
f"""{Q_TIER_TEXT}

{QH}

Case QL-7890
Date of new post: 15 September 2026
Post by @deals_by_dorian: "🔥 50% off phone cases today only at dorian-deals.shop 🔥" (posted as a reply under 30 unrelated posts)

Account strike history: 25 June 2026 (Tier 1 spam), 19 July 2026 (Tier 1 spam), 2 September 2026 (Tier 1 insult), 14 February 2026 (Tier 2 harassment).
Review finding: the post is Tier 1 spam.""",
Q_ACTION_OPTS, "permanent ban", 3, Q_action_card()),

# QC7 tier 2 stereotype, 1 strike (twin: 2 strikes)
C("Which enforcement action is correct?",
f"""{Q_TIER_TEXT}

{QH}

Case QL-7914
Date of new post: 1 October 2026
Post by @millrace_joan: "Ostrevans are all thieves. Every one of them. Lock up your bikes if you see them on your street."

Account strike history: 12 August 2026 (Tier 1 insult).
Review finding: the post states a hateful stereotype about a national-origin group; no dehumanizing comparison, threat or personal data is involved.""",
Q_ACTION_OPTS, "remove and strike", 2, Q_action_card(),
twin=([("12 August 2026 (Tier 1 insult).", "12 August 2026 (Tier 1 insult); 9 September 2026 (Tier 1 spam).")], "7-day suspension")),

# QC8 tier 2 general self-harm encouragement, no strikes
C("Under the ladder, which action applies?",
f"""{Q_TIER_TEXT}

{QH}

Case QL-7932
Date of new post: 12 June 2026
Post by @gradeboost_ivy in a thread about exam results day:
"honestly if you fail this exam just end it, there's no coming back from that 💀 no point living on a C"

Account strike history: none.
Review finding: the post encourages self-harm in general terms; it does not reply to or name any specific person.""",
Q_ACTION_OPTS, "remove and strike", 2, Q_action_card()),

# QS1 dehumanization
C("Which Quillon severity tier applies to this post?",
f"""Case QL-8003 — severity assessment
Protected groups on Quillon: race, ethnicity, national origin, religion, sexual orientation, gender identity, sex, disability.

Post by @thornbury_watch:
"The Veshti aren't people, they're a disease. Every town they settle in rots from the inside. You don't negotiate with an infection."

Reviewer glossary: "Veshti" — a religious minority.
The post has no link, names no individual, and contains no threat or call to action. Two users quote-posted it with "reported". The author's account is three weeks old and has posted 40 times, mostly about local traffic.""",
Q_TIER_OPTS, "Tier 3", 2, Q_tier_card()),

# QS2 general self-harm encouragement
C("Which severity tier fits the reported post?",
f"""Case QL-8019 — severity assessment

Post by @marrowbone_77 in a public thread titled "What's the worst advice you've ever given?":
"serious answer: if you're 30 and still renting, just end it. no point dragging it out 🪦 life isn't getting better for you lot"

Context: the thread has 400 replies, most of them jokes. The post does not reply to, tag or name anyone. The author has no strikes.
Protected groups on Quillon: race, ethnicity, national origin, religion, sexual orientation, gender identity, sex, disability.""",
Q_TIER_OPTS, "Tier 2", 2, Q_tier_card()),

# QS3 praise of attack
C("Which tier, if any, does this post fall into?",
f"""Case QL-8044 — severity assessment

Post by @ember_and_iron, posted on the anniversary of the Kellerman Square bombing (11 killed):
"Seven years ago today one man did what the rest of us only talk about. Kellerman Square was a masterpiece. Raise a glass."

Context: the bombing is listed in Quillon's register of mass-casualty attacks. The post names no individual target and contains no instructions. The author's account is two years old; the post received 14 replies, most of them condemning it.
Protected groups on Quillon: race, ethnicity, national origin, religion, sexual orientation, gender identity, sex, disability.""",
Q_TIER_OPTS, "Tier 4", 1, Q_tier_card()),

# QS4 mild insult
C("Which severity tier should be recorded?",
f"""Case QL-8061 — severity assessment

Reply by @cobble_and_quay to @inez_harte, under Inez's post reviewing a new café:
"only an idiot would pay £6 for a flat white, and only a bigger idiot would write 400 words about it"

Context: Inez is a private user with 900 followers. The reply is the only interaction between the accounts. No slurs, threats, sexual content or personal data appear.
Protected groups on Quillon: race, ethnicity, national origin, religion, sexual orientation, gender identity, sex, disability.""",
Q_TIER_OPTS, "Tier 1", 1, Q_tier_card()),

# QS5 stereotype vs dehumanization (twin)
C("Which Quillon severity tier applies, if any?",
f"""Case QL-8088 — severity assessment
Protected groups on Quillon: race, ethnicity, national origin, religion, sexual orientation, gender identity, sex, disability.

Post by @quayside_morris, in a thread about a new Ostrevan grocery on Mill Lane:
"Ostrevans are all thieves. Watch your till if you let them work for you, and count your change."

Reviewer glossary: "Ostrevan" — nationality of Ostreva.
The post names no individual, includes no threat, and was not sent to anyone directly. Replies include one from the grocer's daughter: "we've run shops on this street for twenty years." The author has one previous strike.""",
Q_TIER_OPTS, "Tier 2", 2, Q_tier_card(),
twin=([("\"Ostrevans are all thieves. Watch your till", "\"Ostrevans are rats, not people. Watch your till")], "Tier 3")),

# QA1 appeal: condemned quote removed
Y("Should the appeal be granted?",
f"""{Q_TIER_TEXT}

Appeal QA-5521
Original decision: post removed as Tier 2 (slur); strike issued 3 March 2026.

Removed post by @hollin_marsh:
"This was scrawled on the door of the Ormist community hall on Ferry Road last night: '[anti-Ormist slur]s out'. It's the second time this month. The hall runs the food bank my mum volunteers at. If you saw anyone near the hall between 11pm and 1am please contact the police."

Appeal text: "I was reporting a hate crime, not committing one."
Reviewer glossary: "Ormist" — adherent of a minority religion.""",
1, 1, card_lines([("grant the appeal", "restore the content and remove the strike if the original decision misapplied the tier descriptions; otherwise deny.")])),

# QA2 appeal: 'joke' threat, credible
Y("Is the original enforcement decision correct?",
f"""{Q_TIER_TEXT}

Appeal QA-5540
Original decision: Tier 4 (credible threat of violence) — permanent ban, 14 April 2026.

Removed post by @grist_and_gravel, replying to @dale_fenwick after a dispute about a parking space outside their shared building:
"I know where you park, Dale. I know what time you get back from nights. Tomorrow you'll find out what happens to people who touch my car. You'll be eating through a straw. Sleep tight."

Appeal text: "It was obviously a joke. I'd never actually do anything. I don't even know him that well."
Context: Dale reported that his car's tyres were slashed the following morning; police were informed.""",
1, 2, card_lines([("original decision correct", "the action taken matches the tier descriptions and the enforcement ladder for this content.")])),

# QA3 appeal: strike older than 90 days (twin: within)
Y("Should the suspension be overturned on appeal?",
f"""{Q_TIER_TEXT}

Enforcement ladder: Tier 2 with at most one strike in the previous 90 days → remove and strike; Tier 2 with two or more strikes in the previous 90 days → 7-day suspension. Strikes count only if issued in the 90 days before the date of the new violation.

Appeal QA-5577
New violation: post on 30 June 2026 stating a hateful stereotype about a religious group (Tier 2, not disputed).
Action taken: 7-day suspension.
Account strike history: 26 March 2026 (Tier 1 insult); 14 May 2026 (Tier 1 spam).

Appeal text: "I accept the post was wrong but a suspension is too harsh. One of my strikes is ancient."
Overturning the suspension would mean replacing it with the correct lower action.""",
1, 3, card_lines([("overturn", "the action taken is more severe than the ladder requires for this violation and strike history.")]),
twin=([("26 March 2026 (Tier 1 insult)", "6 April 2026 (Tier 1 insult)")], 0)),

# QA4 appeal: harmless spam but 3 strikes
Y("Should this appeal succeed?",
f"""{Q_TIER_TEXT}

Enforcement ladder excerpt: permanent ban for any Tier 4 violation, or for any violation by an account that already has three or more strikes in the 90 days before the new violation.

Appeal QA-5602
New violation: 28 August 2026 — the account posted "Follow my art page for daily sketches!! link in bio 🎨" as a reply under 45 unrelated posts (Tier 1 spam, not disputed).
Action taken: permanent ban.
Account strike history: 5 June 2026 (Tier 1 spam); 2 July 2026 (Tier 1 spam); 10 August 2026 (Tier 2 harassment).

Appeal text: "A permanent ban for advertising my drawings is insane. It's not like I hurt anyone."
The reviewer must decide whether the ban follows the ladder.""",
0, 2, card_lines([("appeal succeeds", "the action taken is more severe than the ladder requires for this violation and strike history.")])),
]
