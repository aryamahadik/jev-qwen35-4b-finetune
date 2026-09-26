"""affect_c / personal journals, family chats and voicemails (Hearthnote journaling app; invented people)."""
from _lib import C, Y, T

D = {
    "joy": "Intense happiness about a good event that has happened or is happening now.",
    "contentment": "Calm, low-key satisfaction with how things are right now.",
    "excitement": "Eager, energised anticipation of a specific pleasurable event still to come.",
    "hope": "Looking forward to a wanted outcome that may or may not happen.",
    "anxiety": "Worry about a possible bad outcome whose occurrence is uncertain.",
    "dread": "Heavy anticipation of an unpleasant event the writer is sure will happen.",
    "fear": "Alarm at a threat to safety that is present right now.",
    "relief": "The easing of worry because a feared outcome did not happen or is over.",
    "gratitude": "Warm appreciation directed at someone for help or a kindness they gave.",
    "pride": "Pleasure in an achievement credited to oneself or to someone one closely identifies with.",
    "nostalgia": "Warm, wistful affection for a remembered period of the past.",
    "longing": "Yearning for a specific absent person, place or thing to be present.",
    "loneliness": "Distress at lacking companionship or social connection in general.",
    "grief": "Sorrow over the death or permanent loss of someone or something loved.",
    "sadness": "Sorrow over a painful situation that is not better described by a more specific label.",
    "disappointment": "Unhappiness that an expected or hoped-for outcome did not happen.",
    "guilt": "A bad feeling about a specific action of one's own that harmed someone else, with an urge to make amends.",
    "shame": "A painful sense that one's whole self is bad or worthless, with an urge to hide.",
    "embarrassment": "Brief discomfort at a minor social slip or exposure witnessed by others, with no serious harm done.",
    "jealousy": "Fear of losing a valued relationship, or someone's affection or attention, to a rival.",
    "envy": "Wanting an advantage or possession that someone else has.",
    "resentment": "Lingering bitterness about past unfair treatment.",
    "anger": "Displeasure at a wrong someone has just done, blaming or confronting them.",
    "amusement": "Finding something funny and enjoying it.",
    "awe": "Wonder at something vast or overwhelming that makes the self feel small.",
    "boredom": "Weariness and restlessness from a lack of anything engaging to do.",
    "surprise": "A jolt at something unexpected, before or without a settled positive or negative reaction.",
    "admiration": "Warm approval of another person's qualities or skill.",
    "none of these": "The writer's primary emotion is not any of the listed emotions.",
}


def o(*names):
    return [(n, D[n]) for n in names]


card = o

ITEMS = [
# ------------------------------------------------------------------ p01
# why: fear of losing Dan to his ex (a rival) -> jealousy; anxiety also fits loosely but the
# guideline says tag the more specific definition.
C("p01", "Which emotion should Hearthnote tag for this entry? When two definitions fit, use the more specific one.",
"""
Hearthnote · private journal entry · tagged by writer as "vent"

Dan's been messaging his ex again. "Just as friends," he says, and maybe that's true. But every time his phone lights up on the sofa I watch his face to see if he smiles, and last night he took it into the hall. She knew him for six years before I did; she knows his family, his jokes, the whole history I'm not part of. I keep imagining him realising he'd rather have that back than have me. I'm not going to go through his phone. I'm just scared of being the one who gets swapped out.

Tagging guideline: tag the writer's primary emotion using the app's emotion definitions.
""",
o("jealousy", "envy", "anxiety", "anger", "sadness", "resentment", "fear", "loneliness", "none of these"),
"jealousy", 2),

# ------------------------------------------------------------------ p02
# why: says "jealous" colloquially, but she wants the flat Lena has and explicitly is not upset
# with Lena; no relationship at risk -> envy.
C("p02", "Under the app definitions, what is Rosa's primary emotion?",
"""
WhatsApp · Rosa → Imogen · Sun 21:03

Rosa: have you seen Lena's post
Rosa: the new flat. balcony, river view, a proper kitchen with an island. she's 24!!
Rosa: I'm 31 and I'm in a box room above a vape shop
Rosa: honestly I'm so jealous I could scream. not of HER, she's lovely, I'm genuinely happy she's happy. I'd just give anything for a place like that. I've been saving for five years and I'm nowhere near
Imogen: it'll happen for you x
Rosa: I know. it's just hard seeing it on a Sunday night

Guideline: tag Rosa's primary emotion by the app definitions; everyday words ("jealous", "gutted", "dying") do not decide the tag.
""",
o("envy", "jealousy", "admiration", "resentment", "sadness", "disappointment", "shame", "anger", "joy", "none of these"),
"envy", 3),

# ------------------------------------------------------------------ p03
# why: withdrawal is done, the conversation will happen and she knows it will go badly -> dread.
# Twin: the panel outcome is uncertain ("could go either way") -> anxiety, not dread.
Y("p03", "Is Mira primarily expressing dread?",
"""
Hearthnote · journal · Mira Solberg · 23:48
(Hearthnote suggests one mood tag per entry so the writer can see patterns across the month; the writer has left this entry untagged, so the tag is chosen from the app definitions.)

Tomorrow at lunch I have to tell Mum I'm leaving medicine. I've already withdrawn — the letter from the faculty came on Friday, it's done. There's no version of tomorrow where she takes it well. She'll go quiet first, then she'll bring up Uncle Tor's clinic and everything they've paid, then she'll cry. I know the whole script. I've been moving my food round the plate all evening. I just want it to be Wednesday.

Tagging guideline: tag the writer's primary emotion; check whether the writer treats the coming event as certain or as uncertain.
""",
card("dread", "anxiety"),
1, 3,
twin=T([("Tomorrow at lunch I have to tell Mum I'm leaving medicine. I've already withdrawn — the letter from the faculty came on Friday, it's done. There's no version of tomorrow where she takes it well. She'll go quiet first, then she'll bring up Uncle Tor's clinic and everything they've paid, then she'll cry. I know the whole script.",
         "Tomorrow at lunch the progression panel decides whether I can stay in medicine after failing the anatomy resit. My tutor says it could go either way; some students get a second resit, some don't. I have no idea which I'll be.")],
       0)),

# ------------------------------------------------------------------ p04
# why: whose emotion. Nan: counting down the days, bed made, biscuits bought -> eager
# anticipation of the visit -> excitement. Twin asks about Grandad himself: boiler fixed, it's
# "off my mind" after lying awake since October -> relief.
C("p04", "What emotion does Grandad describe in Nan?",
"""
Voicemail transcript (saved to Hearthnote by the recipient) · from: Grandad · Sat 10:17

"Hello love, it's Grandad. Just ringing to say your letter came. Your nan's been walking round the garden humming since breakfast. She's already made up your old bed, bought the fancy biscuits, and she's crossing off the days on the calendar by the fridge — nineteen to go till you're home for Christmas, she tells me every morning. Me? I'm just glad the boiler's finally fixed. I'd been lying awake since October picturing you arriving to a freezing house with that cough of yours. The engineer came Thursday, it's roaring away now, so that's off my mind. Right, ring us back. Bye, love."
""",
o("excitement", "relief", "anxiety", "hope", "gratitude", "nostalgia", "dread", "surprise", "none of these"),
"excitement", 2,
twin=T([], "relief", instructions="What is Grandad's own primary emotion in the voicemail?")),

# ------------------------------------------------------------------ p05
# why: "not the lie" but "the kind of person" she is, "rotten through", hiding from mirror and
# family -> shame. Twin: focus on the hurt to Ros and making amends -> guilt, not shame.
Y("p05", "Is the writer primarily expressing shame?",
"""
Hearthnote · journal · private · 01:12
(Hearthnote suggests one mood tag per entry so the writer can see patterns across the month; the writer has left this entry untagged, so the tag is chosen from the app definitions.)

I lied to Ros about why I missed her recital. Told her the train was cancelled; really I just didn't feel like going and stayed in watching rubbish. She'd practised the Brahms for four months.
It's not even the lie that's getting to me. It's that I'm apparently the kind of person who does that — who lets people down and then covers it up without blinking. Rotten through. I've turned the bathroom mirror light off because I can't look at myself, and I've muted the family chat so nobody can reach me.

Tagging guideline: tag the writer's primary emotion by the app definitions.
""",
card("shame", "guilt", "embarrassment"),
1, 3,
twin=T([("It's not even the lie that's getting to me. It's that I'm apparently the kind of person who does that — who lets people down and then covers it up without blinking. Rotten through. I've turned the bathroom mirror light off because I can't look at myself, and I've muted the family chat so nobody can reach me.",
         "She was hurt, and I did that. Tomorrow I'm going to ring her, tell her the truth about the train, and ask if I can take her to dinner and hear the Brahms properly. I owe her that much.")],
       0)),

# ------------------------------------------------------------------ p06
# why: warm wistful affection for 1998 summers, grinning -> nostalgia (more specific than joy).
# Twin: Dad died in March, first time hearing his voice, had to stop the tape -> grief.
C("p06", "Which emotion best fits this entry? When two definitions fit, tag the more specific one.",
"""
Hearthnote · journal · Sunday
(Hearthnote suggests one mood tag per entry so the writer can see patterns across the month; the writer has left this entry untagged, so the tag is chosen from the app definitions.)

Clearing the loft, I found the cassette labelled "PENMORROW 98" in Dad's handwriting. It's him singing along to the car radio on the way to the caravan, completely off-key, and me and Jess shrieking in the back. I dug out the old Walkman and listened to it three times on the loft ladder, grinning like I was nine. Those summers — sand in the sandwiches, the fizzy-cola ferry, Dad burning the sausages every single night — were the best of my life. I've put the tape in the kitchen drawer so I can hear it again.
""",
o("nostalgia", "grief", "sadness", "joy", "longing", "gratitude", "amusement", "contentment", "surprise", "none of these"),
"nostalgia", 2,
twin=T([("I dug out the old Walkman and listened to it three times on the loft ladder, grinning like I was nine. Those summers — sand in the sandwiches, the fizzy-cola ferry, Dad burning the sausages every single night — were the best of my life. I've put the tape in the kitchen drawer so I can hear it again.",
         "Dad died in March. It's the first time I've heard his voice since the funeral, and I had to stop the tape halfway and sit on the loft floor for a long time. I've put it in the kitchen drawer; I can't play it again yet.")],
       "grief")),

# ------------------------------------------------------------------ p07
# why: had tickets since February, learned the album, "really thought tonight was the night",
# nobody's fault -> disappointment. Twin: only came as a favour, doesn't know the songs, quiet
# night suits them -> not disappointment.
Y("p07", "Is Kit primarily expressing disappointment?",
"""
WhatsApp · Kit → Sam · Sat 18:40
(Chat saved to Hearthnote by Kit, who asked the app afterwards to tag the mood of the conversation; only Kit's messages are tagged.)

Kit: they've cancelled it. the Harbourside gig. sign on the door, "artist unwell", refunds in 5-7 days
Kit: we drove four hours for this. I've had the tickets on the fridge since February, I learned the whole new album, I'd planned the setlist in my head
Kit: nobody's fault, obviously, she's ill, I hope she's ok
Kit: just, I really thought tonight was finally the night I'd see her live
Kit: eating chips in the car park now

Tagging guideline: tag Kit's primary emotion by the app definitions.
""",
card("disappointment", "sadness", "anger"),
1, 2,
twin=T([("we drove four hours for this. I've had the tickets on the fridge since February, I learned the whole new album, I'd planned the setlist in my head",
         "we drove four hours for this, though honestly I only came because you had a spare ticket and I don't know any of her songs"),
        ("just, I really thought tonight was finally the night I'd see her live",
         "just, a quiet night with nothing planned suits me fine, the sea's lovely from here")],
       0)),

# ------------------------------------------------------------------ p08
# why: sarcasm ("Love that", "Really lovely", "10/10 privacy"): Mum broke an explicit request and
# Dad found out from the group -> blames/confronts Mum -> anger. Twin: she asked Mum to announce,
# Dad already knew, hearts pouring in -> joy.
C("p08", "What is Chioma's primary emotion? Sarcasm is tagged by its intended meaning.",
"""
Family group chat "Okafor-Hale Clan 🏡" · Tue 19:32
(Screenshot saved to Hearthnote by Chioma the same evening, with a request to tag her own mood in the exchange. The family group has 23 members.)

Mum: 🎉🎉 CONGRATULATIONS to our Chioma and Dev — baby due in May!! 🍼
Chioma: Wow. Love that Mum announced my pregnancy in the family group before I'd even told Dad. Really lovely way for him to find out, from a baby-bottle emoji between Auntie's prayer chains. 10/10 privacy. I asked you ONE thing on Sunday: let me tell him myself.
Dad: Chioma? Is this true?
Chioma: Ring you in five, Dad.
""",
o("anger", "amusement", "joy", "embarrassment", "disappointment", "excitement", "surprise", "resentment", "gratitude", "none of these"),
"anger", 2,
twin=T([("Wow. Love that Mum announced my pregnancy in the family group before I'd even told Dad. Really lovely way for him to find out, from a baby-bottle emoji between Auntie's prayer chains. 10/10 privacy. I asked you ONE thing on Sunday: let me tell him myself.",
         "Wow. Love that Mum announced it — I asked her to on Sunday because I was too nervous to type it myself. Dad already knew, we told him at lunch. Honestly the best moment of my week, look at all these hearts coming in 😭❤️"),
        ("Dad: Chioma? Is this true?", "Dad: My girl!!! ❤️❤️")],
       "joy")),

# ------------------------------------------------------------------ p09
# why: guideline: tag the emotion directed at another person if most of the entry is about that
# person. Almost the whole entry is about Mr Adebayo's kindness and repaying him -> gratitude.
Y("p09", "Under the tagging guideline, is the writer primarily expressing gratitude?",
"""
Hearthnote · journal · 00:40

Pip is home. Eleven days missing, and tonight Mr Adebayo from number 14 found him shut in his shed, thin and furious, and walked him all the way round to our door at midnight in his dressing gown and slippers, holding him like a baby. He wouldn't come in; he said he'd been checking the shed every night since he saw our poster, "just in case". I'm baking him a lemon cake first thing tomorrow and the kids are making him a card. I don't know how to repay someone for that.

Tagging guideline: when an entry mixes emotions, tag the one directed at another person if the writer spends most of the entry on that person.
""",
card("gratitude", "relief", "joy"),
1, 2),

# ------------------------------------------------------------------ p10
# why: vast waterfall, felt tiny "in the best way", problems shrank -> awe. Twin: ledge crumbles,
# clinging to a root waiting for the ranger -> present threat -> fear.
C("p10", "Tag the writer's primary emotion; when two definitions fit, use the more specific one.",
"""
Hearthnote · journal · hiking trip, day 3
(Hearthnote suggests one mood tag per entry so the writer can see patterns across the month; the writer has left this entry untagged, so the tag is chosen from the app definitions.)

Up at 4:30 to reach the Carrow Falls before the day-walkers. Stood on the flat rock under the main drop as the sun came over the ridge — the whole valley roaring, spray lit gold, the water falling three hundred feet like it had been doing it for ten thousand years and would do it for ten thousand more. I felt tiny, in the best way; my problems shrank to the size of pebbles. Didn't take a single photo. It didn't seem right to.
""",
o("awe", "joy", "fear", "contentment", "surprise", "gratitude", "nostalgia", "excitement", "admiration", "none of these"),
"awe", 2,
twin=T([("I felt tiny, in the best way; my problems shrank to the size of pebbles. Didn't take a single photo. It didn't seem right to.",
         "Then the ledge crumbled under my left boot. I'm dictating this crouched against the rock face, one hand round a root, heart hammering, not daring to move until the ranger reaches me.")],
       "fear")),

# ------------------------------------------------------------------ p11
# why: not short of company; it's Idris specifically she wants -> longing. Twin: no one in
# particular missed, just no one at all -> loneliness.
C("p11", "Which app emotion best describes this entry? Prefer the more specific definition when two fit.",
"""
Hearthnote · journal · Thursday
(Hearthnote suggests one mood tag per entry so the writer can see patterns across the month; the writer has left this entry untagged, so the tag is chosen from the app definitions.)
Tagging guideline: tag the writer's primary emotion using the app definitions; when two definitions fit, tag the more specific one.

Seven weeks until Idris flies back from the rig. I sleep on his side of the bed now because the pillow still smells of him a bit. I've got friends round most weekends and my sister rang twice today, so it's not company I'm short of. It's him — his terrible whistling, his cold feet, the way he narrates the football. I've started a paper chain on the fridge, one link per day. I just want him here.
""",
o("longing", "loneliness", "sadness", "anxiety", "nostalgia", "grief", "excitement", "hope", "none of these"),
"longing", 2,
twin=T([("Seven weeks until Idris flies back from the rig. I sleep on his side of the bed now because the pillow still smells of him a bit. I've got friends round most weekends and my sister rang twice today, so it's not company I'm short of. It's him — his terrible whistling, his cold feet, the way he narrates the football. I've started a paper chain on the fridge, one link per day. I just want him here.",
         "Four months since I moved to Harlow for the job. Nobody here knows my name. Weekends go by without a single conversation; I chat to the cashier at the corner shop just to hear a voice. There's no one in particular I'm missing — I just don't have anyone. I've started leaving the radio on so the flat sounds less empty.")],
       "loneliness")),

# ------------------------------------------------------------------ p12
# why: eager countdown, list of ramen shops, can't sit still -> excitement, so "other than" = no.
# Twin: never flown alone, checking passport forty times, stomach in knots -> anxiety -> yes.
Y("p12", "Is the writer's primary emotion something other than excitement?",
"""
Hearthnote · journal · Wed 22:15
(Hearthnote suggests one mood tag per entry so the writer can see patterns across the month; the writer has left this entry untagged, so the tag is chosen from the app definitions.)

TWO SLEEPS UNTIL TOKYO!!! Bag packed since Sunday, passport in the front pocket, yen in an envelope. I've made a list of 23 ramen shops and I intend to visit at least nine. I keep opening the flight app just to look at the words "Departs 11:40". Told everyone at work I'll be unreachable. I can't sit still. Mum says I'm like a kid before Christmas and she's not wrong.

Tagging guideline: tag the writer's primary emotion by the app definitions.
""",
card("excitement", "anxiety"),
0, 2, role="neg",
twin=T([("TWO SLEEPS UNTIL TOKYO!!! Bag packed since Sunday, passport in the front pocket, yen in an envelope. I've made a list of 23 ramen shops and I intend to visit at least nine. I keep opening the flight app just to look at the words \"Departs 11:40\".",
         "Two sleeps until Tokyo. I've never flown alone and I've never been further than Calais. Bag packed since Sunday; I've checked the passport is in the front pocket about forty times. I keep opening the flight app in case the connection time has shrunk and I'll miss it."),
        ("I can't sit still. Mum says I'm like a kid before Christmas and she's not wrong.",
         "I can't sit still, and my stomach's been in knots since Monday.")],
       1)),

# ------------------------------------------------------------------ p13
# why: guideline = tag the feeling the writer names as strongest; she names "the dancing and the
# day itself" -> joy. Twin names "missing Mum" (Mum's empty chair = Mum has died) -> grief.
C("p13", "Following the guideline, which feeling should be tagged for this letter?",
"""
Letter (typed into Hearthnote to keep) · to: Aunt Beryl · after the wedding

Dear Beryl,
It was such a day. The rain held off, Femi cried through the vows, and your trifle was demolished by four o'clock. I danced with every single cousin.
I kept looking at Mum's empty chair at the top table. We'd left her photo on it with the lavender. She'd have hated the DJ and loved everything else.
I'm exhausted, too — three hours' sleep and my feet are in pieces.
If you asked me which feeling is biggest today, it's the dancing and the day itself.
All my love,
Ngozi

Tagging guideline: when a writer names which feeling is strongest, tag that feeling.
""",
o("joy", "grief", "gratitude", "sadness", "contentment", "nostalgia", "excitement", "relief", "longing", "none of these"),
"joy", 2,
twin=T([("it's the dancing and the day itself.", "it's missing Mum.")], "grief")),

# ------------------------------------------------------------------ p14
# why: whose emotion. Tom went beetroot, wanted the ground to swallow him, nobody minded ->
# embarrassment (yes). Twin asks about the writer, who laughed until she had to leave -> amusement (no).
Y("p14", "Is the writer's brother Tom, as described, primarily feeling embarrassment?",
"""
Hearthnote · journal · after Cara's wedding

Tom's best-man speech. Halfway through, a gust took his note cards off the lectern and straight into the ornamental pond. He stood there for a second, went beetroot from collar to hairline, stammered "I, er, had a joke about the pond", then waded in up to his shins to fish them out while ninety guests watched. He told me afterwards he wanted the ground to swallow him. Nobody minded; Cara loved it.
As for me — I laughed so hard I had to leave the marquee and sit on a hay bale. I'm still grinning now, typing this.

Tagging guideline: the question names whose emotion to tag.
""",
card("embarrassment", "shame", "amusement"),
1, 2,
twin=T([], 0, instructions="Is the writer herself primarily feeling embarrassment?")),

# ------------------------------------------------------------------ p15
# why: calm, low-key, "nothing I'd change" -> contentment (not joy: low intensity). Twin: nothing to
# do, clock stuck, reorganised spice rack twice -> boredom.
C("p15", "What is the writer's primary emotion? Note the intensity of what is described.",
"""
Hearthnote · journal · Sunday, 4pm
(Hearthnote suggests one mood tag per entry so the writer can see patterns across the month; the writer has left this entry untagged, so the tag is chosen from the app definitions.)
Tagging guideline: tag the writer's primary emotion using the app definitions; when two definitions fit, tag the more specific one.

Soup on the hob, rain on the kitchen window, both kids on the sofa under one blanket reading their library books. The dog's snoring by the radiator. I've got a cup of tea going cold beside me and I don't mind. Nothing to fix, nowhere to be, nothing I'd change. This is the kind of Sunday I used to wish for when the twins were babies.
""",
o("contentment", "joy", "excitement", "relief", "gratitude", "boredom", "nostalgia", "sadness", "loneliness", "none of these"),
"contentment", 2,
twin=T([("I've got a cup of tea going cold beside me and I don't mind.", "I've got a cup of tea going cold beside me."),
        ("Nothing to fix, nowhere to be, nothing I'd change. This is the kind of Sunday I used to wish for when the twins were babies.",
         "Nothing to do, nothing on, and the clock seems stuck at four. I've reorganised the spice rack twice and scrolled to the end of the internet. The rain has cancelled everything.")],
       "boredom")),

# ------------------------------------------------------------------ p16
# why: result is in and benign; hands stopped shaking, "just breathing" -> relief. Twin: results
# not back for six more days, going through worst cases -> anxiety -> no.
Y("p16", "Is Lotte primarily expressing relief?",
"""
Hearthnote · text log (saved) · Lotte → her sister · Thu 12:04
(Lotte saved this exchange to Hearthnote and asked the app to tag her mood in it; the sister's replies are context only.)

Lotte: results came back. benign. BENIGN
Lotte: six days of waiting for a lump to be nothing and it's nothing
Lotte: I'm sitting in the hospital car park just breathing. my hands have stopped shaking for the first time since last Friday
Lotte: going to go and buy the biggest sandwich in the shop
Sister: 😭❤️ ring me when you're driving

Tagging guideline: tag Lotte's primary emotion; check whether the feared event is still ahead or already over.
""",
card("relief", "anxiety", "joy"),
1, 2,
twin=T([("results came back. benign. BENIGN", "results won't be back till next Friday. another six days"),
        ("six days of waiting for a lump to be nothing and it's nothing", "six more days of not knowing whether it's nothing or not"),
        ("I'm sitting in the hospital car park just breathing. my hands have stopped shaking for the first time since last Friday",
         "I'm sitting in the hospital car park going through every worst case. my hands haven't stopped shaking since last Friday"),
        ("going to go and buy the biggest sandwich in the shop", "can't face food")],
       0)),

# ------------------------------------------------------------------ p17
# why: Ada guards her mother's attention against the new baby ("loves Leo more now"), doesn't want
# his things -> jealousy (fear of losing affection to a rival), not envy.
C("p17", "Based on the parent's note, what emotion is Ada showing? Use the most specific definition that fits.",
"""
Note from parent to Year 1 teacher (copied into the family's Hearthnote) · Mon

Dear Ms Fairlie,
Just a heads-up about Ada at home. Since her baby brother Leo arrived six weeks ago, she climbs into my lap every time I sit down to feed him and tries to push his bottle away. She's started asking for her own bottle again, and on Friday she told her grandad, "Mummy loves Leo more now, she doesn't have time for me." She's fine about his toys and she doesn't want his things — it's me she's guarding. If she's clingy at drop-off, that's why. We're doing special "Ada time" every evening.
Many thanks,
Hanna Lindqvist
""",
o("jealousy", "envy", "anxiety", "sadness", "anger", "resentment", "loneliness", "fear", "longing", "disappointment",
  "shame", "guilt", "embarrassment", "grief", "boredom", "surprise", "dread", "hope", "contentment", "none of these"),
"jealousy", 2),
]
