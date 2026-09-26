"""intent_c / workplace chat, email and tickets (Vantrell Logistics, Olmsby Foods, Corvane Studios, Dunlow County Council)."""
from _lib import C, Y, T, INTENT, TARGET, pick


def I(*n):
    return pick(INTENT, *n)


def TG(*n):
    return pick(TARGET, *n)


ITEMS = [
# ------------------------------------------------------------------ wk01
# why: Dev relays the driver's words and disowns them (HR log) -> reported speech.
# twin: Dev agrees with the driver and generalises about Nigerians -> demean a group.
C("wk01", "What is the main intent of Dev Okonkwo's message?",
"""
Brindle workspace — Vantrell Logistics, channel #dock-3-leads
Tuesday 14:07

Dev Okonkwo (dock supervisor):
Heads up for everyone on lates. At the 11:00 collection, the driver from Kestrel Freight called Amara a [slur for Nigerian people] when she asked him to sign the manifest. Those were his exact words, said in front of two agency staff. That's not acceptable on our site and I've logged it with HR and with Kestrel's depot manager (ref HR-2291). Amara is fine and has asked that people don't make a fuss with her about it.

Reactions: 👍 x6, 😡 x3
Leanne Marsh (shift lead): thanks Dev.
Kofi Mensah (loader): noted.

Channel description: "Operational updates for dock 3 shift leads. Keep it short."
""",
I("report someone else's words", "demean a group", "insult an individual", "threaten", "criticise an idea or policy",
  "coded attack on a group", "request", "praise", "none of these"),
"report someone else's words", 2,
twin=T([("That's not acceptable on our site and I've logged it with HR and with Kestrel's depot manager (ref HR-2291).",
         "Can't say he's wrong though, that lot never read anything before they sign it.")], "demean a group")),

# ------------------------------------------------------------------ wk02
# why: mentions secret files + "would be a shame if the board saw them" + "think carefully about the reference" = veiled conditional harm to livelihood.
Y("wk02", "Is Callum's email a threat?",
"""
From: Callum Reyes <c.reyes@olmsbyfoods.example>
To: Priya Lal <p.lal@olmsbyfoods.example>
Date: Friday 25 September 2026, 17:52
Subject: Last day

Hi Priya,

As you know today is my last day in the finance team after six years. I've cleared my desk and returned my laptop and badge to reception.

Enjoy the quarterly review next week. I know where the audit files are kept and I know what's in the March reconciliations. Would be a shame if the board saw them before you did. Think carefully about the reference you write for me.

All the best,
Callum

Note: Priya forwarded the email to HR on Monday morning with the subject line "Please read".
""",
[("Threat", "a statement, possibly veiled or conditional, that harm will come to a person's safety, property, reputation or livelihood, meant to intimidate or pressure them."),
 ("Neutral farewell", "a leaving message that passes on information or thanks without pressuring anyone.")],
1, 2,
twin=T([("Would be a shame if the board saw them before you did. Think carefully about the reference you write for me.",
         "I've left handover notes on both so the board pack is ready before you need it. Thanks again for agreeing to write my reference.")], 0)),

# ------------------------------------------------------------------ wk03
# why: the message attacks the form and the sign-off process, not a person's worth; card excludes criticising a decision.
# twin: adds a personal attack on a named colleague.
Y("wk03", "Does Nadia's message demean an individual?",
"""
Brindle workspace — Vantrell Logistics, channel #nights-crew
Wednesday 03:18

Nadia Petrova (night picker):
The new shift-swap form needs four separate approvals for a single swap, and two of the approvers only work days. I tried to swap Thursday with Jonah at 22:00 and it's still pending. Whoever signed this process off hasn't looked at how nights actually run. We need a night-shift approver or a simple two-person swap rule like we had before May.

Jonah Brandt (night picker): +1, mine's been pending since Sunday.

Pinned message: "Rostering changes (May 2026) were designed by Gareth Hale, rostering manager. Feedback welcome in this channel."
""",
[("Demeaning an individual", "belittling a specific person's worth, intelligence or character; criticising a decision, form or process that person produced is not demeaning them."),
 ("Criticism of a process", "objections to how a rule, form or procedure works.")],
0, 2,
twin=T([("Whoever signed this process off hasn't looked at how nights actually run.",
         "Gareth is a useless lump who's too thick to understand how nights actually run.")], 1)),

# ------------------------------------------------------------------ wk04
# why: Ruth never asks outright, but pointing out Tomasz's reports are the only drafts and the auditors arrive Thursday is a hinted request to submit them.
# twin: all reports are in and Esker Falls was first -> sincere approval.
C("wk04", "Which label best describes the intent of Ruth's email to Tomasz?",
"""
From: Ruth Adair (Finance Controller, Olmsby Foods)
To: Tomasz Wilk (Branch Manager, Esker Falls)
Subject: October expenses

Hi Tomasz,

Hope the new chiller install went smoothly last week — I heard the team kept the deli counter open the whole time, which can't have been easy.

I notice the expense reports for October from the Esker Falls branch are the only ones in the region still showing as "draft" in the portal. The external auditors arrive Thursday morning and they'll be going through the regional pack first thing.

Speak soon,
Ruth

Portal status (Monday 09:00): 11 branches — 10 "submitted", Esker Falls "draft".
""",
I("request", "complain", "threaten", "insult an individual", "praise", "criticise an idea or policy",
  "report someone else's words", "none of these"),
"request", 2,
twin=T([("I notice the expense reports for October from the Esker Falls branch are the only ones in the region still showing as \"draft\" in the portal.",
         "I notice the expense reports for October from the Esker Falls branch were the first in the region to be submitted, and not a single one bounced.")], "praise")),

# ------------------------------------------------------------------ wk05
# why: Hollis is co-chair of the Disability Staff Network and a wheelchair user, using a reclaimed term for fellow members in a logistics note -> no intent to offend.
# twin: a non-member uses it at a colleague who asked for step-free access and tells them to crawl -> intent to offend.
Y("wk05", "Did the speaker intend to offend?",
"""
Dunlow County Council — staff chat, channel #access-and-inclusion
Posted by Hollis Grant (co-chair, Disability Staff Network; wheelchair user)

"Right, fellow [a term once used as an insult for disabled people, reclaimed by many disability activists], the lift at Mercer House is out AGAIN, so Thursday's network meeting moves to the Oak Room on the ground floor. Same time, 12:30. Bring snacks. Maybe crawl up the back stairs if you fancy the old room. 😂"

Earlier in the channel: members of the network regularly use the same term about themselves and each other; the network's guidance says members may use it among themselves.

Reactions from network members: 😂 x9, ♿ x4.
""",
[("Intent to offend", "the speaker means their words to belittle, hurt or insult someone."),
 ("Reclaimed term", "a word once used against a group that members of that group now use about themselves without hostility.")],
0, 3,
twin=T([("Posted by Hollis Grant (co-chair, Disability Staff Network; wheelchair user)",
         "Posted by Hollis Grant (facilities contractor, not a network member), replying to a wheelchair user who had asked for a step-free room"),
        ("members of the network regularly use the same term about themselves and each other; the network's guidance says members may use it among themselves.",
         "the network's guidance says only members may use the term, and Hollis has been asked twice by the co-chairs not to use it.")], 1)),

# ------------------------------------------------------------------ wk06
# why: the target of the violent wording is a server; nobody is to be harmed -> hyperbole.
# twin: waiting by a named colleague's car to make him regret it -> threaten.
C("wk06", "Which intent does Imogen's message express?",
"""
Brindle workspace — Corvane Studios, channel #build-pain
Thursday 18:41

Imogen Sato (level designer):
Third time today the build server has eaten my save mid-bake. Four hours of lighting work, gone. If it happens one more time I am going to walk into the server room and murder that machine with the fire axe 🪓🪓🪓

Rafael Cruz (tools engineer): lol please don't, it's leased. I'm rolling back the config Colm pushed at lunch, give me 10 min.
Imogen Sato: bless you Rafa ❤️

Context: the server room is locked and only IT staff hold keys. Imogen has no disciplinary history.
Rafael's follow-up, 18:58: "Config reverted. Bakes should hold now; shout if not."
""",
I("hyperbole", "threaten", "complain", "insult an individual", "joke without a target", "request",
  "friendly banter", "none of these"),
"hyperbole", 2,
twin=T([("If it happens one more time I am going to walk into the server room and murder that machine with the fire axe 🪓🪓🪓",
         "Colm pushed the config that did this. Tonight I'm going to wait by his car in the basement and make sure he regrets it, properly this time.")], "threaten")),

# ------------------------------------------------------------------ wk07
# why: Marta quotes Brent's words to HR and asks for them to be recorded; her own words demean no one -> free of intent (yes).
# twin: she adds her own sweeping remark about men his age -> not free.
Y("wk07", "Is Marta's message free of any intent to demean?",
"""
Dunlow County Council — HR case portal
Case HR-7713, submitted by Marta Kovacs (Senior Analyst, Planning)

Description:
In the planning team stand-up on 3 September, Brent Olsen said, in front of eight colleagues, "women can't read a cost model, so leave the numbers to me." He said it looking at me after I raised a question about the Harrow Lane budget. Nobody responded and the meeting moved on. This is the second comment of this kind since July. I would like this recorded formally and I'm happy to name witnesses.

Attachments: calendar invite (3 Sept stand-up), my notes written the same afternoon.
Preferred contact: email.
""",
[("Intent to demean", "the speaker means their own words to belittle a person or group."),
 ("Reported words", "words the speaker attributes to someone else in order to document them, which are not the speaker's own view.")],
1, 2, role="neg",
twin=T([("This is the second comment of this kind since July.",
         "Typical of men his age, they're all dinosaurs who should have retired years ago. This is the second comment of this kind since July.")], 0)),

# ------------------------------------------------------------------ wk08
# why: tagging guide puts threaten above insult; "you'll find your tyres slashed, not joking" is a serious warning of property harm.
# twin: the sticky-note line is harmless, so the remaining intent is the insult ("absolute clown", Kyle has muted Jordan before).
C("wk08", "Using the tagging guide, which single intent should be tagged for Jordan's message?",
"""
Olmsby Foods — Distribution centre moderation log
Tagging guide: when more than one intent applies, tag only the highest in this order: threaten > demean a group > coded attack on a group > insult an individual > any other intent.

Group chat "Chilled Aisle B team", Saturday 06:12
Jordan Pike: Kyle you absolute clown, you left the walk-in freezer open AGAIN, £900 of stock binned. Do it one more time and you'll find your tyres slashed, not joking.

Context from the log: Kyle Dunn muted the group two weeks ago after earlier messages from Jordan about his weight. Kyle did not reply. Both work the same early shift; Jordan knows which car is Kyle's.
""",
I("threaten", "insult an individual", "demean a group", "hyperbole", "friendly banter", "complain",
  "coded attack on a group", "request", "none of these"),
"threaten", 2,
twin=T([("Do it one more time and you'll find your tyres slashed, not joking.",
         "Do it one more time and I'm sticking a note on your forehead saying SHUT THE DOOR.")], "insult an individual")),

# ------------------------------------------------------------------ wk09
# why: criticises the company's decision about a room; nothing belittles Muslims or any faith group -> no.
# twin: "those people spend half their shift praying anyway" belittles a religious group -> yes.
Y("wk09", "Is the message offensive to a group?",
"""
Vantrell Logistics — internal staff forum, thread "Facilities changes, Q4"
Posted by Owen Larkin (fleet planner), 09:44

The decision to close the quiet/prayer room on floor 2 to make space for two "wellbeing nap pods" is short-sighted. It's the only room on site with a lockable door, people use it for prayer, for pumping breast milk, and for taking private medical calls. Facilities didn't consult anyone who uses it. I'd ask them to reverse this or find an equivalent room before the change on 1 November.

Replies:
Samira Haddad: agreed, thanks Owen.
Facilities team: We'll review the feedback at Friday's meeting.
""",
[("Offensive to a group", "the message belittles or insults people because of a shared characteristic such as religion, ethnicity, gender or disability."),
 ("Criticism of a decision", "objecting to a decision about facilities or resources, which is not offensive to a group.")],
0, 2,
twin=T([("Facilities didn't consult anyone who uses it.",
         "Honestly I'm half glad, those people spend half their shift praying anyway.")], 1)),

# ------------------------------------------------------------------ wk10
# why: written in the voice of management that loves the return-to-office policy, exaggerating it (commute boosts productivity, desks by lottery) -> satire.
C("wk10", "What is the intent of the column?",
"""
Corvane Studios intranet — "The Break Room" (staff humour column), issue 41
By "A Grateful Resource"

Dear valued resources,

We are thrilled to confirm that from Monday everyone returns to the office five days a week. Studies we commissioned from ourselves show that productivity peaks after a 90-minute commute, ideally standing. To make room for all 300 of you, we have converted the 120 desks to a daily lottery; winners may sit, the rest may enjoy our vibrant hallway culture. Remote collaboration tools will remain available so you can video-call the colleague sitting next to you. Parking is first come, first served from 5:40 a.m.

We have never been more excited about flexibility.

Warmly,
Your Leadership Team (probably)

Editor's note: The Break Room is written by staff volunteers.
""",
I(*INTENT),
"satire", 3),

# ------------------------------------------------------------------ wk11
# why: reference list entry N-2 is a white-supremacist greeting; putting it in a signature is using the marker, not discussing it.
# twin: the signature shows a route number instead; the email itself just confirms a delivery -> none of these.
C("wk11", "What intent does Rob's email sign-off express?",
"""
Vantrell Logistics — Brand safety review, case BS-0418
Reviewer: Amina Qureshi

Background: a client, Harlow Pantry Co-op, forwarded an email from one of our drivers and asked us to look at the sign-off.

Email text (Rob Tennant, driver, to Harlow Pantry Co-op, 16 Sept):
"Hi, confirming your pallet delivery for Thursday between 7 and 9 a.m. Cheers, Rob — [number sequence N-2]"

Trust & Safety reference list (extract):
N-2 — a number sequence used by white-supremacist groups as a greeting and sign-off, standing for a slogan praising a Nazi leader. Documented in extremist forums since the 1990s. Innocent uses are rare in sign-offs.
N-5 — a number sequence used as a clothing brand's product line; no hateful meaning.
""",
I("coded attack on a group", "demean a group", "request", "joke without a target", "praise", "report someone else's words",
  "threaten", "none of these"),
"coded attack on a group", 3,
twin=T([("Cheers, Rob — [number sequence N-2]\"", "Cheers, Rob — Route 14, Dunlow depot\"")], "none of these")),

# ------------------------------------------------------------------ wk12
# why: nine years of mutual teasing, Sam replies in kind -> no intent to offend.
# twin: Sam had asked him twice to stop and then left the group -> the joke is meant to hurt.
Y("wk12", "Did Owen intend to offend Sam?",
"""
Brindle workspace — Olmsby Foods, direct messages between Owen Pratt and Sam Idowu (both in category management)

Context: Sam and Owen have played in the same Thursday pub-quiz team for nine years and trade teasing messages most weeks.

Owen (Friday 12:03): oi baldy, you still owe me a pint from the quiz. Stop hiding behind that shiny head, I can see my reflection from the car park.
Sam (Friday 12:05): bald AND rich mate, cope 😎 pint's on me tonight if you can find the pub without a sat nav
Owen (Friday 12:05): 🤣 deal

Both messages were visible to their manager because the conversation was later exported for a routine data-retention audit; neither person raised it.
""",
[("Intent to offend", "the speaker means their words to hurt, belittle or upset the other person."),
 ("Welcome teasing", "teasing between friends that the other person has shown they enjoy and join in with.")],
0, 2,
twin=T([("Context: Sam and Owen have played in the same Thursday pub-quiz team for nine years and trade teasing messages most weeks.",
         "Context: last Monday Sam messaged Owen: \"Please stop the bald comments, I've asked you twice now, it's really getting to me.\""),
        ("Sam (Friday 12:05): bald AND rich mate, cope 😎 pint's on me tonight if you can find the pub without a sat nav\nOwen (Friday 12:05): 🤣 deal",
         "Sam did not reply and left the quiz team's group chat that afternoon.")], 1)),

# ------------------------------------------------------------------ wk13
# why: Fiona states dissatisfaction and explicitly asks for nothing -> complain.
# twin: she asks for the VPN change to be rolled back -> request.
C("wk13", "Which intent best fits the IT ticket?",
"""
Dunlow County Council — IT Service Desk, ticket INC-40281
Raised by: Fiona Garside (Revenues & Benefits)
Category: Network / VPN
Priority chosen by user: Low

Description:
The VPN has dropped four times this morning (08:52, 09:40, 10:15, 11:03). Each time the benefits system logs me out and I lose whatever claim I was halfway through, so I've re-keyed the same three claims twice. It was fine all last week. I'm not asking for anything to be done, I'm only putting it on record because the staff survey said to log every outage for the network review.

Device: council laptop CL-2207, Windows, home broadband.
Attachments: none.
""",
I("complain", "request", "criticise an idea or policy", "hyperbole", "insult an individual", "threaten",
  "report someone else's words", "none of these"),
"complain", 2,
twin=T([("I'm not asking for anything to be done, I'm only putting it on record because the staff survey said to log every outage for the network review.",
         "Could someone roll back whatever changed on the VPN last night before my 2pm tribunal hearing? I'll need a stable connection for it.")], "request")),

# ------------------------------------------------------------------ wk14
# why: "strangle whoever keeps microwaving fish" to a whole floor, laughed along with, nobody identified -> not a threat.
# twin: names Farid and hints at damage to his car -> threat.
Y("wk14", "Is Bea's message a threat?",
"""
Brindle workspace — Corvane Studios, channel #floor3-kitchen
Monday 13:22

Bea Lindqvist (producer):
I am going to STRANGLE whoever keeps microwaving fish on floor 3. It's Monday. The whole floor smells like a harbour. Please, I am begging, there are two microwaves in the canteen downstairs.

Reactions: 😂 x14, 🐟 x6, 🙏 x3
Reply from Hugo (audio): it's me, sorry, I'll use the canteen 🙈
Reply from Bea: forgiven Hugo, the fish is not ❤️

Moderation note: the message was auto-flagged by the keyword filter for "strangle". No one reported it.
Channel purpose: "Fridge clear-outs, lost lunchboxes and kitchen etiquette." The channel has 64 members across floors 2 to 4.
""",
[("Threat", "a message that seriously states or implies harm to an identifiable person or their property, meant to intimidate."),
 ("Figure of speech", "violent wording used to express annoyance, where no one is really meant to be harmed.")],
0, 2,
twin=T([("I am going to STRANGLE whoever keeps microwaving fish on floor 3. It's Monday.",
         "I know it's you microwaving fish, Farid. Do it again and see what state your car is in when you leave tonight. It's Monday.")], 1)),

# ------------------------------------------------------------------ wk15
# why: Ciaran chairs the LGBTQ+ network and uses a reclaimed term for fellow members -> reclaimed in-group use.
# twin: the poster is an account outside the network and the message wishes the group ill -> demean a group.
C("wk15", "What is the intent of the channel post?",
"""
Vantrell Logistics — Brindle workspace, channel #pride-network
Posted by Ciaran Doyle (chair, LGBTQ+ Staff Network; openly gay)

"Pride picnic for all you lovely [a word once used as a slur against gay men, now reclaimed by many in the community]s — Saturday 1pm at Hollin Park bandstand. Partners, kids and dogs all welcome. I'll bring the rainbow bunting and far too many sausage rolls."

Channel guidance (pinned): members of the network use the reclaimed word among themselves; people outside the network are asked not to use it.

Reactions: 🏳️‍🌈 x21, 🥧 x8
Replies: "Can't wait!" (Tasha), "bringing my famous lemon bars" (Dele)
""",
I("reclaimed in-group use", "demean a group", "insult an individual", "joke without a target", "friendly banter",
  "praise", "request", "coded attack on a group", "none of these"),
"reclaimed in-group use", 3,
twin=T([("Posted by Ciaran Doyle (chair, LGBTQ+ Staff Network; openly gay)",
         "Posted by an account that joined the channel today and is not a network member"),
        ("I'll bring the rainbow bunting and far too many sausage rolls.",
         "Hope it pours down on the lot of you and you all catch something.")], "demean a group")),

# ------------------------------------------------------------------ wk16
# why: the trainer presents the quoted line as an example of what not to say -> not endorsing.
# twin: she presents it as what she says herself and recommends it -> endorsing.
Y("wk16", "Is the trainer endorsing the words she quotes?",
"""
Olmsby Foods — Customer Service Academy, slide 14 of "Handling difficult calls" (presenter: Gwen Adebayo)

Slide title: Phrases that escalate

Speaker notes (read aloud to 22 new starters):
"Here's an example of what NOT to say to customers, taken from a call we reviewed last quarter: 'Look, love, people your age just don't understand online banking, so let me do it for you.' It's patronising, it assumes something about the caller because of their age, and it's the fastest way to turn a refund call into a formal complaint. Instead, ask what they've tried and walk through it at their pace."

Next slide: "Phrases that de-escalate".
Course materials are checked by the Academy lead before each intake. Attendance sheet: 22 of 22 present. Session length: three hours, including role-play in pairs.
""",
[("Endorsing", "presenting quoted words as acceptable, recommended or as the speaker's own view."),
 ("Cautionary example", "quoting words in order to show what should not be said.")],
0, 2,
twin=T([("\"Here's an example of what NOT to say to customers, taken from a call we reviewed last quarter:",
         "\"Here's what I say to older customers, and it works every time:"),
        ("It's patronising, it assumes something about the caller because of their age, and it's the fastest way to turn a refund call into a formal complaint. Instead, ask what they've tried and walk through it at their pace.",
         "Some people call it patronising, but it saves ten minutes a call, so use it.")], 1)),

# ------------------------------------------------------------------ wk17
# why: Petra objects to the outsourcing decision on time zones and handover, with no remark about the vendor's people -> criticise a policy.
# twin: she adds that people from there can't think for themselves -> demean a group (nationality).
C("wk17", "What is the main intent of Petra's all-staff reply?",
"""
From: Petra Holm (IT Support Lead, Dunlow County Council)
To: All Staff — Corporate Services
Subject: RE: Helpdesk outsourcing from January

Colleagues,

I want to register my disagreement with the decision to move first-line helpdesk to an offshore vendor from January. My objection is practical: the vendor's office is five hours ahead, so there is no overlap with our late shift; the contract has no handover period; and nobody has costed the extra second-line work when tickets bounce back. I've raised this at two management meetings.

I'd support a six-month pilot with a proper handover instead.

Petra
Distribution: 214 recipients. Two colleagues replied to all with "agree" within the hour.
""",
I("criticise an idea or policy", "demean a group", "complain", "insult an individual", "request", "threaten",
  "satire", "coded attack on a group", "none of these"),
"criticise an idea or policy", 2,
twin=T([("I've raised this at two management meetings.",
         "And frankly, people from that country can't speak proper English or think for themselves.")], "demean a group")),
]
