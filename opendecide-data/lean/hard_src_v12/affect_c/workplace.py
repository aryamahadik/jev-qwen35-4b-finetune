"""affect_c / workplace comment coding (surveys, Slack, check-ins, exit interviews; invented employers)."""
from _lib import C, Y, T

D = {
    "pride": "Pleasure in an achievement the speaker credits to themself or to a group they belong to.",
    "gratitude": "Warm appreciation directed at another person or group for help or a benefit they gave.",
    "admiration": "Warm approval of another person's skill or qualities, without wanting what they have.",
    "envy": "Wanting an advantage, possession or success that someone else has, with discomfort at lacking it.",
    "jealousy": "Fear of losing a valued relationship, or someone's attention or regard, to a rival.",
    "resentment": "Lingering bitterness over unfair treatment in the past that has not been put right.",
    "anger": "Immediate displeasure at a wrong that has just happened, or is happening, to the speaker, blaming whoever is responsible.",
    "indignation": "Anger at an unfairness done to other people or to a principle, where the speaker is not the one harmed.",
    "frustration": "Irritation at being blocked or stalled in reaching a goal, without blaming anyone for a wrong.",
    "disappointment": "Unhappiness that an expected or hoped-for outcome did not happen, where no one is blamed.",
    "sadness": "Sorrow over a loss or painful situation that is not better described by a more specific label.",
    "guilt": "A bad feeling about a specific action of one's own that harmed someone else, with an urge to apologise or make amends.",
    "shame": "A painful sense that one's whole self is flawed or inadequate, with an urge to hide or withdraw.",
    "embarrassment": "Brief discomfort at a minor social slip witnessed by others, where no one is seriously harmed.",
    "regret": "Wishing one had chosen differently, with the focus on what the choice cost oneself.",
    "anxiety": "Worry about a possible bad outcome that has not happened yet.",
    "fear": "Alarm at a threat to safety that is present right now.",
    "relief": "The easing of worry because a feared outcome did not happen or is over.",
    "hope": "Looking forward to a wanted outcome that may still happen.",
    "excitement": "Eager, energised anticipation of a specific event the speaker is looking forward to.",
    "boredom": "Weariness and restlessness from work that is dull, repetitive or unstimulating.",
    "loneliness": "Distress at lacking social connection or companionship.",
    "schadenfreude": "Pleasure at someone else's misfortune.",
    "sympathy": "Concern and sorrow for someone else's misfortune.",
    "contempt": "Regarding someone as inferior or beneath respect.",
    "amusement": "Finding something funny and enjoying it.",
    "none of these": "The primary emotion is not any of the listed emotions.",
}


def o(*names):
    return [(n, D[n]) for n in names]


card = o

ITEMS = [
# ------------------------------------------------------------------ w01
# why: she wants the posting/line on CV that Tomasz has; not afraid of losing a relationship
# (so not jealousy, despite everyday usage); did not apply, so no unmet expectation -> envy.
C("w01", "Using the handbook definitions, which code fits the writer's primary emotion?",
"""
Slack · DM · #people-pulse export (consented sample) · Harlow & Brandt Consulting

Mira Castellanos → Jonah (buddy), Tue 17:48:
"Tomasz got the Lisbon secondment. Announced in all-hands just now. Good for him, genuinely — he's earned it, and I didn't even apply this round because of the house move. But I've wanted an overseas posting since I joined five years ago, and hearing the words 'eighteen months in Lisbon' out loud hit me somewhere in the ribs. I'd give a lot to have that line on my CV and that view out of the window. I'm not going to be weird with him about it. I just needed to say it to someone who won't repeat it."

Coder instruction: code the writer's primary emotion using the handbook labels. Colloquial wording does not decide the code; the definitions do.
""",
o("envy", "jealousy", "admiration", "resentment", "disappointment", "sadness", "anger", "gratitude", "pride", "none of these"),
"envy", 2),

# ------------------------------------------------------------------ w02
# why: fear of being replaced as the manager's go-to person by a rival; explicitly doesn't want
# his role -> jealousy. Twin: wants Callum's project/laptop/desk, relationship with Marta fine -> envy -> no.
Y("w02", "Is Anjali primarily expressing jealousy in this check-in?",
"""
Weekly check-in form · Pellmore Studios · free-text box "How are things with the team?"

Anjali R. (designer, 3 years): "Ever since Callum joined in March, Marta books her one-to-ones with him first and laughs at his stand-up updates. She used to run every new brief past me before anyone else, and now I hear about them second-hand in the channel. I feel like I'm being edged out as the person she turns to, and I hate how much it bothers me. It's not that I want his role or his projects — I like mine. I just miss being her first call. I'm not raising this formally; I wanted it written down somewhere."

Coding rule: code the respondent's primary emotion from the handbook definitions.
""",
card("jealousy", "envy"),
1, 3,
twin=T([("Ever since Callum joined in March, Marta books her one-to-ones with him first and laughs at his stand-up updates. She used to run every new brief past me before anyone else, and now I hear about them second-hand in the channel. I feel like I'm being edged out as the person she turns to, and I hate how much it bothers me. It's not that I want his role or his projects — I like mine. I just miss being her first call.",
         "Callum joined in March and was handed the Varda rebrand, the new studio laptop and the window desk in his first week. I've pitched to lead a rebrand for three years. I'd love to be running something like that, and I hate how much it bothers me. Marta and I get on as well as ever — that's not it. I just want what he's been given.")],
       0)),

# ------------------------------------------------------------------ w03
# why: specific act (snapping at Joy) harmed her; wants to apologise and take work off her -> guilt.
# Twin: turns it into a verdict on his whole self and wants to hide -> shame.
C("w03", "Which handbook code best describes Lior's primary emotion?",
"""
Email · to: Hana Iwu (team lead) · from: Lior Ben-Ami · Subject: Thursday

Hi Hana,
I've been thinking about Thursday's stand-up. When Joy asked whether the release notes would be done by Friday, I snapped at her in front of the whole team — told her to "read the board for once". She didn't deserve that; she'd been covering my tickets all week while I was on the migration. I've seen her go quiet in the channel since.
I'd like to apologise to her properly, face to face, and I'll take the release notes off her plate this sprint so she isn't stuck with my leftovers.
Could we also talk about my workload at our next one-to-one?
Lior

Coding: primary emotion of the writer, using handbook definitions.
""",
o("guilt", "shame", "embarrassment", "regret", "anger", "sadness", "anxiety", "frustration", "sympathy", "none of these"),
"guilt", 3,
twin=T([("I'd like to apologise to her properly, face to face, and I'll take the release notes off her plate this sprint so she isn't stuck with my leftovers.",
         "It just confirms what I've suspected about myself for a while: I'm not a decent person to work with, and everyone can see it. I'd rather work from home for a few weeks so nobody has to look at me.")],
       "shame")),

# ------------------------------------------------------------------ w04
# why: minor slip (calling the CEO "Mum") in front of 200 people, nobody upset, cheeks hot,
# wanted the floor to open -> embarrassment; not shame (no whole-self verdict), not guilt (no harm).
C("w04", "What is Kit's primary emotion according to the handbook?",
"""
Slack · #random-ish (private channel, 4 members) · Ostrava Freight Ltd

Kit: ok so. all-hands, 200 people on the call, CEO asks if anyone has questions about the Q3 numbers
Kit: I unmute and say "yes Mum, what's the margin on the Baltic route"
Kit: MUM. I called Rolf MUM.
Kit: he just said "good question, son" and answered it and everyone moved on, which somehow made it worse
Kit: nobody's upset, it's genuinely fine, Rolf even sent a 👍 afterwards. I just wanted the floor to open up. my cheeks were hot for the whole rest of the call and I kept my camera off
Priya: 😂 legend
Kit: please never speak of this again

Coding note: code Kit's primary emotion. Other people's reactions are context, not Kit's emotion.
""",
o("embarrassment", "shame", "guilt", "amusement", "anxiety", "regret", "fear", "contempt", "none of these"),
"embarrassment", 2),

# ------------------------------------------------------------------ w05
# why: names two people whose help saved the migration; drinks on her -> gratitude. Twin: credits
# the team's own achievement ("we did it") -> pride, so not gratitude.
Y("w05", "Is the writer primarily expressing gratitude?",
"""
Email · to: platform-team@ · from: Dana Whitcombe (engineering manager) · Subject: Halden migration — done
(Sent Sunday 09:12 to the 14-person platform team, copied to the CTO; included in the quarterly comment-coding sample with the sender's consent.)

Team,
The Halden database migration went live at 02:14 on Sunday with zero customer-facing downtime.
I want to name two people. Rukmini rewrote the rollback scripts over two weekends when we found the old ones couldn't handle the partitioned tables. Ossie caught the timezone bug in the replay job at 01:50, twenty minutes before cutover, and stayed on until six to watch it. Without the two of them we'd have been down for hours and I'd be writing a very different email.
Drinks on Thursday are on me.
Dana

Coding: code the writer's primary emotion.
""",
card("gratitude", "pride"),
1, 2,
twin=T([("I want to name two people. Rukmini rewrote the rollback scripts over two weekends when we found the old ones couldn't handle the partitioned tables. Ossie caught the timezone bug in the replay job at 01:50, twenty minutes before cutover, and stayed on until six to watch it. Without the two of them we'd have been down for hours and I'd be writing a very different email.",
         "Look at what this team did. We designed it, tested it and ran it ourselves, with no vendor and no contractors — the first migration in this company's history with no downtime at all. Two years ago the board said we weren't capable of it. We are the team that did it.")],
       0)),

# ------------------------------------------------------------------ w06
# why: grievance two years old, "carried every day since", unresolved -> resentment.
# Twin: happened this morning, found out an hour ago, wants him to answer today -> anger.
C("w06", "Which emotion code fits the leaver's answer? Pay attention to when the grievance happened.",
"""
Exit interview notes · Corby Analytics · interviewer: HR partner S. Adeyemi · leaver: data scientist, 4 yrs

Q: What is the main reason you are leaving?
A (verbatim, agreed with leaver): "Two years ago my then manager presented my demand-forecasting model to the board as his own work. My name wasn't on a single slide. I raised it with HR at the time; it was 'noted' and nothing happened, and he was promoted that spring. I've carried that every day since. Every time his name comes up in a meeting I feel it again. The new job pays about the same. I'm going because I don't want to work somewhere that let that stand."
Q: Anything we could have done?
A: "Fix it when it happened."

Coding: code the leaver's primary emotion using handbook definitions.
""",
o("resentment", "anger", "disappointment", "sadness", "envy", "contempt", "indignation", "regret", "frustration", "none of these"),
"resentment", 3,
twin=T([("Two years ago my then manager presented", "This morning my manager presented"),
        ("I raised it with HR at the time; it was 'noted' and nothing happened, and he was promoted that spring. I've carried that every day since. Every time his name comes up in a meeting I feel it again.",
         "I found out from the board minutes an hour ago. My hands are still shaking and I want him to answer for it today, in front of HR.")],
       "anger")),

# ------------------------------------------------------------------ w07
# why: respondent is not harmed, objects to unfairness done to the night cleaners -> indignation.
# Twin: respondent is one of the cleaners and is harmed -> anger, so not indignation.
Y("w07", "Is the respondent primarily expressing indignation?",
"""
Staff pulse survey · Q7 "Anything else leadership should hear?" · Marlowe Hospital Trust (estates & facilities)
Survey closed 30 September; 412 responses. Comments are anonymised before coding and the coder sees only the text.

Comment #218: "The cleaners on the night shift were told on Friday that their break room is being turned into a storage cupboard for the new scanners, with nowhere offered instead. They eat their dinners in the stairwell now. I don't work nights, I've never used that room and it doesn't touch me at all, but it is plainly unfair to the people who keep this building running, and someone senior should answer for it publicly."

Coding: code the respondent's primary emotion.
""",
card("indignation", "anger"),
1, 3,
twin=T([("that their break room", "that our break room"),
        ("They eat their dinners in the stairwell now.", "We eat our dinners in the stairwell now."),
        ("I don't work nights, I've never used that room and it doesn't touch me at all, but it is plainly unfair to the people who keep this building running",
         "I'm one of those cleaners, that room was the only place I could sit down in a ten-hour shift, and it is plainly unfair to me")],
       0)),

# ------------------------------------------------------------------ w08
# why: calibration is on Monday (ahead), outcome uncertain, rewriting and refreshing -> anxiety.
# Twin: meeting already happened, bonus safe, shoulders down -> relief.
C("w08", "What is Ollie's primary emotion? Note whether the event is still ahead of him or already over.",
"""
Slack · DM · Fenwick Insurance Group
(Message shared by Ollie for the team's wellbeing-coding pilot, with consent. Coders see only the message and its timestamp. Year-end ratings are decided at a calibration meeting of team leads.)
Sat 22:40 · Ollie Brandauer → Teodora (friend, same team)

"Calibration meeting is at 9 on Monday. If my rating drops from 'exceeds' to 'meets', I lose the bonus — and I've already promised Kate that money for the flat deposit. I've rewritten my self-review four times tonight. I keep refreshing the calendar invite as if it'll tell me something. Can you look at my wins section tomorrow and tell me honestly if it's strong enough?"

Coding: code Ollie's primary emotion from the handbook definitions.
""",
o("anxiety", "fear", "hope", "relief", "excitement", "guilt", "frustration", "gratitude", "none of these"),
"anxiety", 2,
twin=T([("Sat 22:40", "Mon 11:05"),
        ("Calibration meeting is at 9 on Monday. If my rating drops from 'exceeds' to 'meets', I lose the bonus — and I've already promised Kate that money for the flat deposit.",
         "Calibration meeting was at 9 this morning. My rating stayed at 'exceeds', so the bonus is safe — the money I'd already promised Kate for the flat deposit."),
        ("I've rewritten my self-review four times tonight. I keep refreshing the calendar invite as if it'll tell me something.",
         "I'd rewritten my self-review four times for nothing. My shoulders have finally come down from round my ears."),
        ("Can you look at my wins section tomorrow and tell me honestly if it's strong enough?", "Lunch later?")],
       "relief")),

# ------------------------------------------------------------------ w09
# why: warm approval of Farida's skill; explicitly doesn't want her job -> admiration.
# Twin: she got the director role, he'd trade places, it stings -> envy.
C("w09", "Which code best fits the reviewer's primary emotion toward the colleague?",
"""
Peer feedback form · Quarterly · Vellacourt Media · reviewer: Bram Hoekstra · about: Farida Nasser

Q: "Describe a moment this quarter when this colleague stood out."
"The investor Q&A on 12 May. Two hostile questions in a row about the layoffs, one of them clearly designed to trip her up, and Farida answered both calmly, with exact figures, never once defensive, and even got a laugh from the room. I've watched the recording twice since. I don't want her job and I'm not after her spotlight — I just think she's exceptional at this and I'd like to learn from how she does it."

Coding: code the reviewer's primary emotion.
""",
o("admiration", "envy", "pride", "gratitude", "jealousy", "amusement", "resentment", "sympathy", "none of these"),
"admiration", 2,
twin=T([("I don't want her job and I'm not after her spotlight — I just think she's exceptional at this and I'd like to learn from how she does it.",
         "She was promoted to director off the back of it a week later. I'd trade places with her in a heartbeat, and it stings every time I see the new title in her signature.")],
       "envy")),

# ------------------------------------------------------------------ w10
# why: she built it alone, framing the certificate -> pride, so "other than pride" = no.
# Twin: award belonged to Hana, asking for it to be reissued and to apologise -> guilt -> yes.
Y("w10", "Is Noor's primary emotion something other than pride?",
"""
Slack · #wins channel · Tallgrass Logistics · Fri 21:12
(#wins is the company-wide channel where staff post good news; posts are sampled monthly for the culture report, which codes one primary emotion per post using the handbook.)

Noor Qureshi: "Won the Innovation Award at tonight's company dinner for the route-scheduling tool! 🏆 And yes — I did build it, alone, over six months of evenings and weekends after my shift, from the first line of code to the driver app. Two years ago I couldn't write a for-loop. Framing the certificate tonight and putting it next to my diploma."
Reactions: 🎉 x34, 👏 x21

Coding: code Noor's primary emotion.
""",
card("pride", "guilt"),
0, 2, role="neg",
twin=T([("And yes — I did build it, alone, over six months of evenings and weekends after my shift, from the first line of code to the driver app. Two years ago I couldn't write a for-loop. Framing the certificate tonight and putting it next to my diploma.",
         "Except Hana wrote the core engine and my name went on the entry form by mistake. She sat two tables away clapping for me. I've already emailed the committee asking for it to be reissued in her name, and I'll say sorry to her properly on Monday.")],
       1)),

# ------------------------------------------------------------------ w11
# why: people are friendly, work is fine; distress is about lacking connection -> loneliness.
# Twin: doesn't mind being alone; problem is the repetitive work -> boredom.
C("w11", "Code the respondent's primary emotion using the handbook labels.",
"""
Remote-work survey · free-text · Quillfeather Software (fully remote engineer, joined 8 months ago)
Q: "Is there anything about working remotely you'd like the People team to know?"

"Everyone else on my squad sits together in the Rotterdam office. I'm on the video calls, but the jokes and the real decisions happen in the kitchen afterwards, and I hear about them on Monday. Nobody's unkind — people are friendly when I message them. I just go whole days without a conversation that isn't about a ticket. Last Friday I realised I hadn't said a word out loud until dinner. The work itself is fine; I like it."

Coding: code the respondent's primary emotion.
""",
o("loneliness", "sadness", "boredom", "jealousy", "envy", "resentment", "anxiety", "frustration", "disappointment", "none of these"),
"loneliness", 2,
twin=T([("I just go whole days without a conversation that isn't about a ticket. Last Friday I realised I hadn't said a word out loud until dinner. The work itself is fine; I like it.",
         "Honestly, I don't mind that — I like the quiet. What gets me is the work: the same twelve ticket types on repeat, day after day, that I can close half asleep. Last Friday I realised I hadn't learned a single new thing in a month.")],
       "boredom")),

# ------------------------------------------------------------------ w12
# why: popcorn, "not going to pretend I'm sorry", "best Thursday" at the rival team's failure ->
# schadenfreude. Twin: feels awful for them, offers help -> sympathy -> no.
Y("w12", "Is Sol primarily expressing schadenfreude?",
"""
Slack · #platform-banter (private) · Rennick Retail Tech
(Export shared with the culture team after a complaint about tone in private channels; coders assign one primary emotion per speaker using the handbook.)

Sol: did you see? Blue team's launch fell over live in front of the whole exec panel. checkout 500s for eleven minutes, CTO watching
Sol: this is the same team that spent a month calling our staged rollout "cowardly" in every retro
Sol: 🍿🍿🍿
Sol: not going to pretend I'm sorry. best Thursday I've had all year, I've watched the incident channel scroll like it's a film
Maya: harsh 😅
Sol: harsh but fair

Coding note: code Sol's primary emotion.
""",
card("schadenfreude", "sympathy"),
1, 2,
twin=T([("Sol: 🍿🍿🍿\nSol: not going to pretend I'm sorry. best Thursday I've had all year, I've watched the incident channel scroll like it's a film",
         "Sol: and still — I feel awful for them. they worked three weekends straight on that. I've offered to lend them Ines for the rollback"),
        ("Maya: harsh 😅", "Maya: that's kind of you"),
        ("Sol: harsh but fair", "Sol: nobody deserves that in front of the execs")],
       0)),

# ------------------------------------------------------------------ w13
# why: promised outcome did not happen, she accepts the freeze and says nobody did wrong ->
# disappointment. Twin: manager lied and promoted his nephew; she demands an explanation today -> anger.
C("w13", "What is the employee's primary emotion, by the handbook?",
"""
One-to-one notes (shared doc) · Brackwater Engineering · employee: Sanne Voorhees · manager: Ade Kolawole

Sanne's section, written before the meeting:
"In March you told me that if I led the Kestrel migration I'd be put forward for senior this cycle. I led it — on time, under budget. The promotion list came out this morning and my name isn't on it. You've explained that the whole senior band was frozen after the budget cut, and I believe you; nobody has been promoted in any team. Nobody did anything wrong, exactly. I'd just spent six months picturing this, and it isn't happening. I'd like to talk about what the next cycle looks like."

Coding: code the employee's primary emotion.
""",
o("disappointment", "anger", "resentment", "sadness", "frustration", "envy", "shame", "anxiety", "indignation", "none of these"),
"disappointment", 2,
twin=T([("You've explained that the whole senior band was frozen after the budget cut, and I believe you; nobody has been promoted in any team. Nobody did anything wrong, exactly. I'd just spent six months picturing this, and it isn't happening. I'd like to talk about what the next cycle looks like.",
         "Your nephew, who joined in June, is on it. On Friday you told me the band was frozen. You lied to my face, and I want an explanation in this meeting, today.")],
       "anger")),

# ------------------------------------------------------------------ w14
# why: Q12 rule = code the emotion attached to the final request; final request is to review the
# rota, attached to "worries me"/"lie awake" -> anxiety. Twin: final request is a thank-you for
# Facilities -> gratitude.
C("w14", "Applying the Q12 coding rule, which emotion should be coded for comment #57?",
"""
Engagement survey · Q12 open comment · Driftwood Games (live-ops team)
Coding rule for Q12: when a comment contains several emotions, code the one attached to the comment's final request.

Comment #57: "Honestly we nailed the outage response last week — detection to fix in 40 minutes, that's us at our best. Big thank-you to Facilities for bringing pizza up at 1am without being asked. But the on-call rota worries me: four people covering nights and weekends until Christmas, and two of them already look grey. I lie awake thinking someone's going to burn out and quit mid-December. Can we please review the rota before November?"
""",
o("anxiety", "pride", "gratitude", "hope", "frustration", "excitement", "relief", "fear", "sympathy", "none of these"),
"anxiety", 3,
twin=T([("Can we please review the rota before November?", "Can we please do a proper thank-you for Facilities before November?")],
       "gratitude")),

# ------------------------------------------------------------------ w15
# why: turned down the role, "I chose wrong", "my step up... I let it pass", blames only himself;
# focus is the cost of his own choice -> regret. Twin: "I chose right", was there for his father -> no.
Y("w15", "Is Petros primarily expressing regret?",
"""
Email · to: former mentor, Dr Ilona Varga · from: Petros Anagnou · Subject: saw the news

Dear Ilona,
I saw the announcement: the Oslo team won the Nordic Infrastructure Prize. Last spring you offered me the team-lead role there and I turned it down to stay close to home. Watching the ceremony stream tonight, seeing Jens in the role I could have had, I keep thinking I chose wrong. It would have been my step up, my name on that prize, and I let it pass. I don't blame anyone but myself for the choice. Please pass my congratulations to the team.
Warmly,
Petros

Coding: code the writer's primary emotion.
""",
card("regret", "envy", "guilt"),
1, 3,
twin=T([("I keep thinking I chose wrong. It would have been my step up, my name on that prize, and I let it pass. I don't blame anyone but myself for the choice.",
         "I know I chose right. That spring was Dad's surgery and recovery, and I was there for every appointment. No prize would have been worth missing that.")],
       0)),

# ------------------------------------------------------------------ w16
# why: same words "Well, that's that then." Project she expected to survive is cancelled; nobody
# played politics -> disappointment. Twin: the feared audit finding closed with no penalty, "It's
# over", going home to sleep -> relief.
C("w16", "Reading the phrase in context, what is Beatriz's primary emotion?",
"""
Slack · #leadership · Oriel Health Software · Wed 16:05
Posted by Beatriz Salgado (Head of Product), one hour after the board vote:

"Board has voted. The Wayfarer project — the one I pitched two years ago and argued for at every quarterly — is cancelled as of today. I genuinely thought it would survive this round; the pilot numbers were good, and the board had told us in June to expect renewal. Nobody played politics, it's just the new budget. Well, that's that then. I'll write up the wind-down plan for Monday."

Coding: identical phrases can carry different emotions; code the speaker's primary emotion from the context.
""",
o("disappointment", "relief", "sadness", "anger", "gratitude", "anxiety", "resentment", "frustration", "hope", "none of these"),
"disappointment", 2,
twin=T([("The Wayfarer project — the one I pitched two years ago and argued for at every quarterly — is cancelled as of today. I genuinely thought it would survive this round; the pilot numbers were good, and the board had told us in June to expect renewal. Nobody played politics, it's just the new budget.",
         "The audit finding against us — the one that could have cost us the hospital contracts and has kept me awake since June — has been closed with no penalty. I genuinely thought we'd lose at least two contracts over it. It's over."),
        ("I'll write up the wind-down plan for Monday.", "I'm going home to sleep properly for the first time in weeks.")],
       "relief")),

# ------------------------------------------------------------------ w17
# why: dull repetitive data entry, timing the kettle, not worried -> boredom, so "other than
# boredom" = no. Twin: one wrong digit could bring a fine, lies awake -> anxiety -> yes.
Y("w17", "Is Jun's primary emotion something other than boredom?",
"""
Check-in form · Ferris & Lowe Accountants · temp staff · week 3

Q: "How are you finding the work?"
A (Jun Park): "Third week of data entry for the Harbrook audit. I type invoice numbers from scanned PDFs into the ledger, eight hours a day. I could do this in my sleep, and some afternoons I nearly do. Yesterday I started timing how long the office kettle takes to boil, just for something to think about (2 min 40). Nobody's unkind, the pay is fine, and I'm not worried about the contract. The hours just stretch."

Coding: code the respondent's primary emotion.
""",
card("boredom", "anxiety"),
0, 2, role="neg",
twin=T([("I could do this in my sleep, and some afternoons I nearly do. Yesterday I started timing how long the office kettle takes to boil, just for something to think about (2 min 40). Nobody's unkind, the pay is fine, and I'm not worried about the contract. The hours just stretch.",
         "One wrong digit and the regulator can fine the client, and my initials are on every batch. I check each row three times and still lie awake going over the columns. Nobody's unkind, the pay is fine. I just keep thinking about the mistake I haven't found yet.")],
       1)),
]
