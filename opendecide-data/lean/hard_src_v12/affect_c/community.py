"""affect_c / community, school and club settings (Ashby Community Wellbeing Network coding sheet; invented people and places)."""
from _lib import C, Y, T

D = {
    "anger": "Displeasure at a wrong someone has done, holding them responsible and confronting or accusing them.",
    "frustration": "Irritation at being repeatedly blocked or let down by a process or situation, without accusing anyone of a wrong.",
    "disappointment": "Unhappiness that an expected or hoped-for outcome did not happen.",
    "sadness": "Sorrow over a painful situation, where no more specific label here fits.",
    "anxiety": "Worry about a possible bad outcome that has not happened yet.",
    "fear": "Alarm at a threat to safety that is present right now.",
    "relief": "The easing of worry because a feared outcome did not happen or is over.",
    "hope": "Looking forward to a wanted outcome that is uncertain, with attention on the chance that it will happen.",
    "excitement": "Eager, energised anticipation of a pleasurable event that is going to happen.",
    "joy": "Intense happiness about a good event that has happened.",
    "gratitude": "Warm appreciation directed at someone for help or a kindness they gave.",
    "pride": "Pleasure in an achievement credited to oneself or to a group one belongs to.",
    "admiration": "Warm approval of another person's qualities or skill.",
    "envy": "Wanting an advantage or possession that someone else has.",
    "resentment": "Lingering bitterness over past unfair treatment that the speaker has not let go of.",
    "guilt": "A bad feeling about a specific action of one's own that harmed someone else, with an urge to make amends.",
    "shame": "A painful sense that one's whole self is inadequate or worthless, with an urge to hide or withdraw.",
    "embarrassment": "Brief discomfort at a minor social slip witnessed by others, with no serious harm done.",
    "amusement": "Finding something funny and enjoying it.",
    "surprise": "A jolt at something unexpected, before or without a settled positive or negative reaction.",
    "confusion": "Being unable to tell what something means or which of two accounts is right, and wanting it cleared up.",
    "curiosity": "An interested desire to find something out for its own sake.",
    "disgust": "Revulsion at something physically or morally repellent.",
    "contempt": "Regarding someone as inferior or beneath respect.",
    "loneliness": "Distress at lacking companionship or social connection.",
    "boredom": "Weariness and restlessness from having nothing engaging to do.",
    "sympathy": "Concern and sorrow for someone else's misfortune.",
    "none of these": "The primary emotion is not any of the listed emotions.",
}


def o(*names):
    return [(n, D[n]) for n in names]


card = o

ALL27 = [k for k in D if k != "none of these"]

ITEMS = [
# ------------------------------------------------------------------ c01
# why: rule = highest rating; "looking forward" 4 and "worried" 4 tie; the note is about the
# coast trip ("can't wait", packed) -> excitement. Twin: looking forward 3, worried alone at 4 -> anxiety.
C("c01", "Applying the pastoral coding rule, what is the pupil's primary emotion?",
"""
Ashby Academy · pupil wellbeing check-in form · Year 9 · Mon 08:40 · pupil ref 9K-117

Section A — "How strongly do you feel each of these today?" (1 = not at all, 5 = very strongly)
looking forward 4 · worried 4 · tired 2 · cross 1 · left out 1

Section B — "Anything you want your tutor to know?"
"Can't wait for the coast trip on Friday!! I've already packed my bag and my wetsuit."

Pastoral coding rule: the pupil's primary emotion is the one rated highest in Section A. If two or more are tied for highest, use the Section B note to decide between the tied ones. Section A maps as: looking forward = excitement, worried = anxiety, tired = none of these, cross = anger, left out = loneliness.
""",
o("excitement", "anxiety", "anger", "loneliness", "joy", "hope", "boredom", "sadness", "none of these"),
"excitement", 3,
twin=T([("looking forward 4", "looking forward 3")], "anxiety")),

# ------------------------------------------------------------------ c02
# why: sarcastic "shoutout"/"really appreciate"/"thank you" to someone blocking the driveway weekly,
# tagging the van firm -> intended emotion is anger, not gratitude (no). Twin: neighbour left
# lemons and honey after an operation -> sincere gratitude (yes).
Y("c02", "Is the poster primarily expressing gratitude?",
"""
Hollins Green neighbourhood group (online) · post by Margot Esterhazy · Tue 07:52
(Group of about 1,900 local residents; posts are sampled each month for the Ashby Community Wellbeing Network's mood report, which codes one primary emotion per post.)

"Shoutout to whoever parks their white van across my driveway every Tuesday morning. Really appreciate the free weekly lesson in patience — nothing says 'good neighbour' like me being late for the school run again. Truly, thank you. 🙏 I'll be leaving a note with the same energy."

14 comments · 3 of them tagging "@RoyVansHire"

Moderator coding for the monthly mood report: code the poster's intended primary emotion; irony is coded by its intended meaning.
""",
card("gratitude", "anger"),
0, 2,
twin=T([("parks their white van across my driveway every Tuesday morning. Really appreciate the free weekly lesson in patience — nothing says 'good neighbour' like me being late for the school run again.",
         "left a bag of lemons and a jar of honey on my doorstep on Tuesday morning, the day after my operation. Really appreciate it — I've made three jars of curd and felt looked after all week."),
        ("3 of them tagging \"@RoyVansHire\"", "3 of them guessing it was Mrs Kaur at number 9")],
       1)),

# ------------------------------------------------------------------ c03
# why: grant decision uncertain, strong signals, fingers crossed, sketching beds -> hope (not
# excitement: the event is not certain). Twin: warned half the bids will be cut, awake at 2am
# rechecking figures -> anxiety.
C("c03", "Which label from the coding sheet fits the chair's primary emotion?",
"""
Ashby Estate Growers · committee email · from: chair, Delphine Mortimer · Subject: grant decision on the 14th

Hi all,
Quick update. The council's community fund panel decides on our £8,000 garden grant on the 14th. If it comes through, the estate kids get raised beds, a shed and a water butt by spring — a real place to grow things instead of the car park. The grants officer rang yesterday and said ours was one of the strongest bids she'd read this year, and that the panel "tends to like projects with kids in them". Fingers crossed, everyone. I've already sketched where the beds would go.
Delphine

Coding (network mood report): code the writer's primary emotion.
""",
o("hope", "anxiety", "excitement", "joy", "pride", "gratitude", "relief", "confusion", "none of these"),
"hope", 3,
twin=T([("The grants officer rang yesterday and said ours was one of the strongest bids she'd read this year, and that the panel \"tends to like projects with kids in them\". Fingers crossed, everyone. I've already sketched where the beds would go.",
         "The grants officer rang yesterday to warn that half the bids will be cut this year and that ours has a budget line she's \"not sure about\". I've been up at 2am twice this week re-reading our figures for mistakes, and I keep picturing telling the kids it's off.")],
       "anxiety")),

# ------------------------------------------------------------------ c04
# why: eleven years of past mistreatment, "haven't forgotten", won't be polite, agents "should hear
# it" -> lingering bitterness -> resentment. Twin: "I've let the old years go", glad for dry rooms -> no.
Y("c04", "Is the writer primarily expressing resentment?",
"""
Letter to the editor · Wexham Park Tenants' Association newsletter · from: flat 7C

For eleven years the old landlord ignored our damp complaints — forty-one letters from this block alone — while putting the rent up every April without fail. My daughter spent three winters with a chest infection. Now Harbinger Homes have bought the building and the new owners are finally fixing the walls, which is good, and I'll say so. But I haven't forgotten a single one of those winters, and I don't intend to be polite about it at the handover meeting on the 3rd. Some of the old managing agents are staying on. They should hear it.

Coding: code the writer's primary emotion.
""",
card("resentment", "anger", "relief"),
1, 3,
twin=T([("But I haven't forgotten a single one of those winters, and I don't intend to be polite about it at the handover meeting on the 3rd. Some of the old managing agents are staying on. They should hear it.",
         "And honestly, I've let the old years go. Nothing will give those winters back, and I'm done carrying them. I'm just glad my daughter will sleep in a dry room this Christmas.")],
       0)),

# ------------------------------------------------------------------ c05
# why: minor slip (early entry), laughed at interval, nobody cross, ears burning -> embarrassment.
# Twin: "not a real musician", avoiding the choir, wants to be taken off the list -> shame.
C("c05", "What is the caller's primary emotion under the coding sheet?",
"""
Voicemail to choir director, transcribed by the Ravensworth Singers' welfare officer with permission · from: Clem (alto)

"Hi Gideon, it's Clem. About Saturday — I came in a full bar early in the Fauré solo. Everyone in the church heard it; there was that awful half-second where the organ and I disagreed. I laughed about it at the interval, and you winked at me from the podium, which helped. It's fine, honestly, nobody's cross and the second half went well. My ears were just burning for about an hour afterwards. Anyway, see you Thursday — I'll count very carefully."

Coding: code the caller's primary emotion.
""",
o("embarrassment", "shame", "guilt", "amusement", "anxiety", "sadness", "disappointment", "gratitude", "none of these"),
"embarrassment", 2,
twin=T([("I laughed about it at the interval, and you winked at me from the podium, which helped. It's fine, honestly, nobody's cross and the second half went well. My ears were just burning for about an hour afterwards. Anyway, see you Thursday — I'll count very carefully.",
         "It just proved what I've always known — I'm not a real musician, I'm someone pretending, and now everyone has seen it. I've been avoiding the choir group chat since. Please take me off the Thursday list; I don't want anyone looking at me.")],
       "shame")),

# ------------------------------------------------------------------ c06
# why: wants to work out who wrote the letter for its own sake; rules out worry and looking
# forward to an event; not troubled by unclear information needing a decision -> curiosity.
C("c06", "Code the poster's primary emotion using the full coding sheet.",
"""
Harrow Lane Library book club · online forum · thread: "The Keeper's Letter — ch. 1–12 (spoilers!)"

Post by user "bramblebee":
"Chapter 12 ends with the lighthouse keeper's letter still unopened in the tin, and I have spent all of Sunday turning it over. Who wrote it? I've got three theories: (1) the drowned brother isn't drowned, (2) the harbourmaster's wife, because of the handwriting clue in chapter 4, (3) Nell wrote it to herself, which would explain the dates. I'm not worried about it, and it's not that I'm looking forward to anything in particular — I just badly want to work out what's going on. Anyone else re-read chapter 4?"
""",
o(*ALL27, "none of these"),
"curiosity", 2),

# ------------------------------------------------------------------ c07
# why: whose emotion. Coach: best football of the season, no complaints -> not disappointment -> the
# negative statement is true (yes). Twin asks about Meg, who expected to win ("we were supposed to
# win") -> disappointment -> the negative statement is false (no).
Y("c07", "Is it true that the coach is NOT primarily expressing disappointment?",
"""
Ashby Juniors FC · post-match message to the parents' WhatsApp · from: coach, Lorna Haig · U12 girls

"Evening all. We lost 3–1 to Brookside, but I'll be honest: that's the best forty minutes of football we've played all season. They pressed exactly as we'd practised, kept their shape, and scored a proper team goal. I've no complaints at all — they did everything I asked, and the result was down to Brookside's keeper having the game of her life. Meg (captain) took it hardest in the changing room: she'd told everyone we'd win this one, she was sure of it, and she kept saying 'we were supposed to win' into her towel. Training Tuesday as normal. 🙌"
""",
card("disappointment", "pride"),
1, 3, role="neg",
twin=T([], 0, instructions="Is it true that Meg, as the coach describes her, is NOT primarily experiencing disappointment?")),

# ------------------------------------------------------------------ c08
# why: same words "What a surprise." Sarcastic about a third missed collection, repeated calls with
# no change, no one accused -> frustration. Twin: bins collected a day early for the first time in
# twelve years -> genuine surprise.
C("c08", "What is the poster's intended primary emotion? Irony is coded by its intended meaning.",
"""
Ellerby Road residents' noticeboard (app) · post by Hamish Tallow · Mon 18:10
(The Ellerby Road app covers 240 households; the network's monthly mood report codes one primary emotion per post from the coding sheet and does not contact posters.)

"Bins missed again. Third Monday running. What a surprise. The black bags are now stacked up by the gate, the foxes found them at 2am, and I've spent my evening picking chicken bones off the pavement. I've rung the collection line twice, been told 'it's logged' twice, and nothing changes. Anyone else on the even side get missed?"

Coding: code the poster's primary emotion from the coding sheet.
""",
o("frustration", "surprise", "anger", "amusement", "disappointment", "confusion", "disgust", "sadness", "none of these"),
"frustration", 2,
twin=T([("Bins missed again. Third Monday running. What a surprise. The black bags are now stacked up by the gate, the foxes found them at 2am, and I've spent my evening picking chicken bones off the pavement. I've rung the collection line twice, been told 'it's logged' twice, and nothing changes. Anyone else on the even side get missed?",
         "Bins collected at 5:50 this morning — a day early, on a bank holiday Monday. What a surprise. Twelve years on this road and I've never known them early once. I only heard the lorry because I was up with the baby. Anyone else on the even side get done?")],
       "surprise")),

# ------------------------------------------------------------------ c09
# why: designed and built the arm himself, hand up for the judges, scoresheet above the desk ->
# pride. Twin: team finished his arm while he was ill and kept his name on -> gratitude -> no.
Y("c09", "Is Yusuf primarily expressing pride?",
"""
Carrow University Robotics Society · members' newsletter · "Member spotlight" submission · from: Yusuf Demir (2nd year)
(Spotlight pieces are written by members about their own term; the society's welfare officer codes each one for the network's student mood survey.)

"We placed second at the National Student Robotics Challenge in Leicester! Out of forty-two teams. I designed and built the gripper arm myself — three prototypes, a burnt-out servo, and a lot of 3am hot glue — and it picked up every single object in the final round, including the egg. When the judges asked who built the arm, I got to put my hand up. I've printed the scoresheet and stuck it above my desk."

Coding: code the writer's primary emotion.
""",
card("pride", "gratitude"),
1, 2,
twin=T([("I designed and built the gripper arm myself — three prototypes, a burnt-out servo, and a lot of 3am hot glue — and it picked up every single object in the final round, including the egg. When the judges asked who built the arm, I got to put my hand up. I've printed the scoresheet and stuck it above my desk.",
         "I was off the whole term with glandular fever and didn't make a single build session. The team finished my gripper arm without me, kept my name on the entry, and video-called me from the arena so I could watch the final. I don't know how to thank them enough for that.")],
       0)),

# ------------------------------------------------------------------ c10
# why: rule = closing sentence; closing sentence is about still seeing the plaster -> revulsion ->
# disgust. Twin: closing sentence holds the manager responsible for lying and overcharging -> anger.
C("c10", "Applying the rule for review snippets, which emotion should be coded?",
"""
Review · Plate & Pewter (café, Ashby high street) · ★☆☆☆☆ · by "Juno K."

"Ordered the leek and potato soup. Three spoonfuls in, I lifted out a used sticking plaster — pink, soggy, clearly from someone's finger. I pushed the bowl as far across the table as I could reach and couldn't look at it for the rest of the visit; my stomach turned just thinking about what else was in the pot. My friend stopped eating her sandwich too. I can still see it when I close my eyes."

Coding rule for review snippets: code the emotion of the review's closing sentence.
""",
o("disgust", "anger", "contempt", "disappointment", "surprise", "fear", "amusement", "sadness", "none of these"),
"disgust", 2,
twin=T([("I can still see it when I close my eyes.",
         "The manager then told us it \"must have come in with you\", charged us full price anyway, and I hold him responsible for lying to our faces.")],
       "anger")),

# ------------------------------------------------------------------ c11
# why: parent's own error made the child miss the test; takes the blame, arranges a resit, has
# apologised -> guilt (yes). Twin: the school's texts were wrong; demands correction -> anger (no).
Y("c11", "Is the parent primarily expressing guilt?",
"""
Email · to: attendance@ashbyacademy.example · from: Rahul Iyer · Subject: Aarav Iyer 8M — missed maths test
(Forwarded by the attendance office to the pastoral team, who code the tone of parent emails for the network's family-contact report: one primary emotion per email.)

Dear Attendance Team,
Aarav missed Thursday's maths assessment because I put the wrong date on our kitchen calendar and kept him at his grandmother's for an extra day. Please don't let this count against him — it was entirely my mistake, not his. He'd revised all week and was upset when he found out. I'll bring him in early any morning next week so he can sit it, and I've apologised to him properly.
Kind regards,
Rahul Iyer
""",
card("guilt", "anger", "embarrassment"),
1, 2,
twin=T([("because I put the wrong date on our kitchen calendar and kept him at his grandmother's for an extra day. Please don't let this count against him — it was entirely my mistake, not his.",
         "because your office texted us the wrong date — twice — and he stayed at his grandmother's for an extra day on the strength of it. Please don't let this count against him — it was the school's mistake, not his."),
        ("I'll bring him in early any morning next week so he can sit it, and I've apologised to him properly.",
         "I expect a correction, and an explanation from whoever sends these texts, by Monday.")],
       0)),

# ------------------------------------------------------------------ c12
# why: rule = code the emotion directed at the addressee (the rescue team): thanks, can never
# repay, will fundraise -> gratitude, even though relief is also present.
C("c12", "Under the letter-coding rule, which emotion is coded for this letter?",
"""
Letter · to: Glenharrow Mountain Rescue Team · published (with permission) in their winter newsletter

To all of you,
My son Callum is home, asleep upstairs, because four of you went up Beinn Rua in the dark and the sleet on Saturday night after his ankle broke on the scree. You carried him down for five hours. One of you — I think Ailsa — sat with him under the survival bag and talked to him about football so he wouldn't panic. I will never be able to repay that. Whatever you need — radios, fuel money, a new stretcher — tell me, and I'll run the sponsored walk myself.
With my whole heart,
Moira Blackwood

Coding rule: when a letter mixes emotions, code the one directed at the addressee.
""",
o("gratitude", "relief", "joy", "admiration", "pride", "sympathy", "fear", "anxiety", "none of these"),
"gratitude", 2),

# ------------------------------------------------------------------ c13
# why: the river already crested below the step and the warning is lifted -> relief, not anxiety
# (no). Twin: crest forecast for noon, could go either way, can't settle -> anxiety (yes).
Y("c13", "Is the poster primarily expressing anxiety? Note whether the danger is still ahead or over.",
"""
Kellow Bridge community flood group (messaging) · post by Rhiannon Pryce · Sat 09:30
(The group has 380 households along the river; the network's post-flood report codes one primary emotion per post from the first 48 hours.)

"Update from the bottom of Mill Lane: the siren went at 3am and we moved the car up the hill and the dog and photo albums upstairs. The river crested at about 5:40 — two inches below our front step — and it's been dropping ever since. The River Authority lifted the warning at 8. I've just sat on the stairs with a coffee and cried a bit, but the good kind. Thank you all for the texts."

Coding: code the poster's primary emotion.
""",
card("anxiety", "relief", "fear"),
0, 2,
twin=T([("The river crested at about 5:40 — two inches below our front step — and it's been dropping ever since. The River Authority lifted the warning at 8. I've just sat on the stairs with a coffee and cried a bit, but the good kind.",
         "The river is forecast to crest at about noon, somewhere near our front step — maybe two inches below it, maybe not. The River Authority says it could go either way. I've been sitting on the stairs with a coffee watching the gauge app, unable to settle.")],
       1)),

# ------------------------------------------------------------------ c14
# why: unexpected first place, read it three times, "don't know how I feel yet, mostly stunned" ->
# surprise (no settled reaction yet, so not joy/pride). Twin: results list her as both first and
# withdrawn; asks which is right -> confusion.
C("c14", "What is the writer's primary emotion? When two definitions fit, code the more specific one.",
"""
Ashby & District Chess League · email from a junior member to the club secretary · from: Eliza Brandt (11)
(Forwarded with the family's permission to the league's junior welfare lead, who codes junior members' messages for the network's youth mood report.)

"Hi Mr Okoro! The results email just came and it says I came FIRST in the under-12 section at the regional rapidplay. First!! I only entered for practice — I thought I'd be happy to win two games. I had to read it three times and then show my dad. I didn't see that coming at all. I don't even know how I feel about it yet, mostly I'm just stunned. See you at club night.
Eliza"
""",
o("surprise", "joy", "pride", "confusion", "excitement", "amusement", "gratitude", "relief", "none of these"),
"surprise", 3,
twin=T([("it says I came FIRST in the under-12 section at the regional rapidplay. First!! I only entered for practice — I thought I'd be happy to win two games. I had to read it three times and then show my dad. I didn't see that coming at all. I don't even know how I feel about it yet, mostly I'm just stunned.",
         "it lists me as first in the under-12 section AND as 'withdrawn after round 3' in the same table. I played all five rounds — I have the scoresheets. Did I win or did I withdraw? I've read it three times and my dad can't work it out either. Which one is right?")],
       "confusion")),

# ------------------------------------------------------------------ c15
# why: barely knows the family, keeps thinking of the child, wonders how they're coping, donates
# and offers help -> concern for others' misfortune -> sympathy (more specific than sadness).
C("c15", "Code the poster's primary emotion, using the more specific definition when two fit.",
"""
Hollins Green neighbourhood group · post by Ferdie Ansah · Wed 20:15

"Most of you will have seen the fire engines on Copse Road last night. The Nkemelu family at number 22 got out safely — both kids, the grandmother, even the cat — but the house is gone, and with it everything they owned. I don't know them well; we nod at the bus stop. I keep thinking about the little one standing on the pavement in a borrowed coat, and I can't stop wondering how they're coping tonight. I've dropped a bag of clothes at the church hall and I'll do a school run for them if they need it."
""",
o("sympathy", "sadness", "fear", "anxiety", "gratitude", "relief", "disgust", "admiration", "none of these"),
"sympathy", 2),
]
