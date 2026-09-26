"""affect_c / annotated dialogue corpus (Whitlow Everyday Dialogue Corpus; invented speakers and settings)."""
from _lib import C, Y, T

D = {
    "anger": "Displeasure at a wrong a person has done, directed at that person through blame, accusation or confrontation.",
    "frustration": "Irritation at being blocked from a goal by circumstances or objects, without accusing a person of a wrong.",
    "amusement": "Finding something funny and enjoying it.",
    "joy": "Happiness at a good event, where no more specific label in this list fits.",
    "surprise": "A jolt at something unexpected, before or without a settled positive or negative reaction.",
    "fear": "Alarm at a threat to safety that is present right now.",
    "anxiety": "Worry about a possible bad outcome that has not happened yet.",
    "relief": "The easing of worry because a feared outcome did not happen or is over.",
    "sadness": "Sorrow over a painful situation, where no more specific label in this list fits.",
    "grief": "Sorrow over a death or permanent loss that has already happened.",
    "disappointment": "Unhappiness that an expected or hoped-for outcome did not happen, where no one is blamed.",
    "hope": "Looking forward to a wanted outcome that may still happen.",
    "gratitude": "Warm appreciation directed at someone for help or a benefit they gave.",
    "pride": "Pleasure in an achievement of oneself or of someone the speaker closely identifies with, such as their own child, team or club.",
    "admiration": "Warm approval of the qualities or skill of someone the speaker does not claim as their own.",
    "envy": "Wanting an advantage, possession or success that someone else has.",
    "jealousy": "Fear of losing a valued relationship, or someone's attention, to a rival.",
    "guilt": "A bad feeling about a specific action of one's own that harmed someone else, with an urge to repair it.",
    "embarrassment": "Brief discomfort at a minor social slip or exposure witnessed by others, with no serious harm done.",
    "shame": "A painful sense that one's whole self is flawed or worthless, with an urge to hide.",
    "regret": "Wishing one had chosen differently, with the focus on what the choice cost oneself.",
    "contempt": "Regarding someone as inferior, stupid or beneath respect, shown through disdain or mockery.",
    "schadenfreude": "Pleasure at the misfortune of a rival or someone the speaker dislikes, because it is their misfortune.",
    "sympathy": "Concern and sorrow for someone else's misfortune.",
    "confusion": "Being unable to make sense of unclear or conflicting information and wanting it cleared up.",
    "curiosity": "An interested desire to find something out for its own sake, with no difficulty making sense of what one already has.",
    "excitement": "Eager, energised anticipation of a specific event that is coming.",
    "disgust": "Revulsion at something physically or morally repellent.",
    "boredom": "Weariness and restlessness from having nothing engaging to do.",
    "awe": "Wonder at something vast, powerful or extraordinary that makes the self feel small.",
    "none of these": "The target speaker's primary emotion is not any of the listed emotions.",
}


def o(*names):
    return [(n, D[n]) for n in names]


card = o

ITEMS = [
# ------------------------------------------------------------------ a01
# why: same words "I can't believe you did that." Stage directions (snorting, grinning, keeps it on
# the door) -> amusement. Twin: A forwarded B's resignation draft; B cold, "You had no right" ->
# confronts A for a wrong -> anger.
C("a01", "Which emotion does speaker B express in turn 2? Stage directions override the literal words.",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-0412 · open-plan office, two colleagues of six years
Corpus note: clips are transcribed from consented recordings; each clip is double-annotated, and disagreements are resolved by a third annotator using the definitions sheet only.
Annotation target: speaker B, turn 2. Stage directions in [brackets] describe tone and body language and override the literal words. Label with the corpus definitions only.

A: I swapped the nameplate on your desk for one that says "The Duchess" while you were at lunch. Facilities made it for me.
B: [snorting, picks it up and props it at an angle, grinning] I can't believe you did that.
A: You're keeping it?
B: [still laughing] It's going on my door.
""",
o("amusement", "anger", "surprise", "joy", "gratitude", "embarrassment", "contempt", "frustration", "pride", "none of these"),
"amusement", 2,
twin=T([("I swapped the nameplate on your desk for one that says \"The Duchess\" while you were at lunch. Facilities made it for me.",
         "I forwarded your draft resignation letter to the whole team while you were at lunch. I thought it would be funny."),
        ("[snorting, picks it up and props it at an angle, grinning]", "[flat, cold voice, standing up]"),
        ("A: You're keeping it?\nB: [still laughing] It's going on my door.", "A: It was a joke!\nB: [walking out] You had no right. None.")],
       "anger")),

# ------------------------------------------------------------------ a02
# why: whose emotion. A has auditioned three times and would give an arm for the place the brother
# got -> envy. Twin asks about B, who is beaming about her little brother -> pride, not envy.
Y("a02", "Is speaker A primarily expressing envy?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-0877 · two friends at a bus stop
Annotation target: the speaker named in the question. Stage directions in [brackets] override literal words.

A: Your brother got into Carrick Conservatory? The actual Carrick?
B: [beaming] Full scholarship. He found out this morning.
A: [quietly, looking at the timetable] I've auditioned there three times. Three. I'd give my left arm for that place. I'm not saying he doesn't deserve it.
B: He practised six hours a day for two years. I sat through every single scale.
A: [forced smile] Yeah. Tell him congrats from me.
B: [grinning] He'll be unbearable at Christmas and I don't care. That's my little brother.
""",
card("envy", "jealousy", "pride", "admiration"),
1, 2,
twin=T([], 0, instructions="Is speaker B primarily expressing envy?")),

# ------------------------------------------------------------------ a03
# why: sarcastic "Best day ever"/"soulmate" with slammed tray, tight jaw; blocked by a machine, no
# person accused -> frustration. Twin: giggling, holding the page like a trophy, framing it -> amusement.
C("a03", "What is speaker B's primary emotion across her turns?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-1093 · university library, flatmates
Corpus note: clips are transcribed from consented recordings; each clip is double-annotated, and disagreements are resolved by a third annotator using the definitions sheet only.
Annotation target: speaker B, all turns. Stage directions in [brackets] describe tone and override the literal words.

A: Did the printer eat your thesis chapter again?
B: [slams the paper tray shut, jaw tight, jabbing the reset button] Yep. Best day ever. Truly, this machine is my soulmate. Third time this week.
A: Want me to try the one on floor two?
B: [exhaling hard through her nose] It's also broken. They're all broken. I just need ONE page to come out.
""",
o("frustration", "anger", "amusement", "joy", "sadness", "disappointment", "anxiety", "contempt", "surprise", "none of these"),
"frustration", 2,
twin=T([("[slams the paper tray shut, jaw tight, jabbing the reset button]", "[holding up the shredded, concertinaed page like a trophy, giggling]"),
        ("[exhaling hard through her nose] It's also broken. They're all broken. I just need ONE page to come out.",
         "[wiping her eyes, still laughing] No, look — it's folded my title page into a perfect fan. I'm framing this.")],
       "amusement")),

# ------------------------------------------------------------------ a04
# why: B's own remark hurt Nadia's view of A (she blanked A); B owns it and will repair -> guilt.
# Twin: no harm (Nadia laughed, asked for tips) but everyone heard and B went red -> embarrassment.
C("a04", "Label speaker B's primary emotion in turn 2.",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-1450 · shared kitchen, housemates
Annotation target: speaker B, turn 2. Stage directions in [brackets] describe tone and body language.

A: Did you tell Nadia I said her jollof was bland?
B: [long pause, not meeting A's eyes] ...I did. It slipped out at the barbecue when she asked what you thought, and she's been cool with you ever since — I saw her blank you at the gate this morning. That's my fault, not yours. I'm going to ring her tonight, tell her I got it wrong, and sort it.
A: You don't have to—
B: I do.
""",
o("guilt", "embarrassment", "shame", "regret", "sadness", "anxiety", "sympathy", "anger", "none of these"),
"guilt", 3,
twin=T([("and she's been cool with you ever since — I saw her blank you at the gate this morning. That's my fault, not yours. I'm going to ring her tonight, tell her I got it wrong, and sort it.",
         "and she just laughed, said she knows it needs more pepper, and asked you for tips — no harm done at all. But the whole garden heard me say it and I went red to my ears."),
        ("A: You don't have to—\nB: I do.", "A: She texted me asking for my recipe.\nB: [covering face] Don't.")],
       "embarrassment")),

# ------------------------------------------------------------------ a05
# why: B hasn't opened the result; worried about failing and losing the place -> anxiety, not
# relief (no). Twin: B passed, place confirmed, can finally sleep -> relief (yes).
Y("a05", "In B's final turn, is B primarily expressing relief?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-1788 · phone call, siblings
Corpus note: clips are transcribed from consented recordings; each clip is double-annotated, and disagreements are resolved by a third annotator using the definitions sheet only.
Annotation target: speaker B, final turn. Note whether the event B reacts to is still ahead or already over.

A: Results are up on the portal. Have you looked?
B: [voice tight] Don't. I'm not opening it until Mum's home. If I've failed chemistry again I lose the Leeds place, and I can't do another year of resits.
A: You studied loads.
B: [fast, breathless] I studied loads last time. Just — talk about something else until six, okay? I keep refreshing the page and closing it.
""",
card("relief", "anxiety", "hope"),
0, 2,
twin=T([("[voice tight] Don't. I'm not opening it until Mum's home. If I've failed chemistry again I lose the Leeds place, and I can't do another year of resits.",
         "[breathing out slowly] I looked. I passed chemistry. The Leeds place is confirmed — no more resits, ever."),
        ("[fast, breathless] I studied loads last time. Just — talk about something else until six, okay? I keep refreshing the page and closing it.",
         "[laughing weakly] I've been holding my breath since August. I think I can finally sleep tonight.")],
       1)),

# ------------------------------------------------------------------ a06
# why: mother's daughter's achievement, "she built that. That's my girl", framing the medal ->
# pride (achievement of someone she closely identifies with); admiration is for people not one's own.
C("a06", "Which corpus label fits speaker A in turn 3? When two definitions fit, use the more specific one.",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-2031 · marathon finish line, a mother (A) and her friend (B)
Annotation target: speaker A, turn 3. Stage directions in [brackets] describe tone and body language.

B: Is that her? In the orange?
A: That's her. Mile 26. [clutching B's arm]
A: [voice cracking, filming on her phone] Eight months ago she couldn't run to the end of our road. She trained every morning before school, in the dark, on her own — she built that. That's my girl. Look at her form, B, look at it!
B: She's flying.
A: I'm going to have that medal framed for the hallway.
""",
o("pride", "admiration", "joy", "excitement", "surprise", "relief", "gratitude", "awe", "amusement", "hope",
  "anxiety", "fear", "sadness", "grief", "envy", "jealousy", "guilt", "embarrassment", "shame", "contempt",
  "schadenfreude", "sympathy", "confusion", "curiosity", "boredom", "none of these"),
"pride", 2),

# ------------------------------------------------------------------ a07
# why: calls B a mug, "can't fix that level of thick", "I'd need crayons", slow head shake,
# mocking aside to the barman -> contempt.
Y("a07", "Is speaker A primarily expressing contempt in turn 3?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-2205 · pub, two acquaintances
Annotation target: speaker A, turn 3. Stage directions in [brackets] override literal words.

A: You bought bottled water? For the house?
B: Twelve-pack. The tap tastes funny.
A: [slow head shake, half-smile, not looking at B] Anyone who pays for bottled water when the tap's free is a mug. Honestly, you can't fix that level of thick. I'd explain how a water main works, but I'd need crayons.
B: Right. Okay.
A: [to the barman] Another one, and a glass of tap for my friend here, since it's apparently exotic.
""",
card("contempt", "anger", "amusement"),
1, 2),

# ------------------------------------------------------------------ a08
# why: rule = only the final turn. B's final turn: Gran said she'd probably not see her again,
# "I keep hearing it" -> sadness (no death has happened, so not grief). Twin: final turn has Gran
# coming for Christmas and B can't wait -> excitement.
C("a08", "Per the corpus guideline for mixed turns, what emotion should be labelled for speaker B?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-2390 · living room, B is emigrating
Annotation target: speaker B. Guideline: when a speaker shows different emotions across turns, label the emotion of that speaker's final turn only.

A: So it's really happening. Six weeks.
B: [bouncing on the sofa] Six weeks! A flat two streets from the beach in Perth, a job at the marine lab, sunshine in February — I've wanted this since I was fourteen. I've already bought snorkels.
A: And Gran?
B: [quiet, turning the ring on her finger] She held my hand for ages on Sunday and said she'd probably not see me again. She's ninety-three. I keep hearing it.
""",
o("sadness", "excitement", "joy", "guilt", "anxiety", "grief", "disappointment", "hope", "fear", "none of these"),
"sadness", 3,
twin=T([("[quiet, turning the ring on her finger] She held my hand for ages on Sunday and said she'd probably not see me again. She's ninety-three. I keep hearing it.",
         "[bouncing again] She's flying out for Christmas — she's already bought a sunhat. I've planned the whole week, the reef, the lot. I can't wait to show her.")],
       "excitement")),

# ------------------------------------------------------------------ a09
# why: Priti fears being swapped out for Hollis in Jas's friendship -> jealousy. Twin: wants the
# Paris trip Hollis won, "just want what she's got" -> envy -> no.
Y("a09", "Is Priti primarily expressing jealousy?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-2577 · school corridor, two 15-year-olds
Corpus note: clips are transcribed from consented recordings; each clip is double-annotated, and disagreements are resolved by a third annotator using the definitions sheet only.
Annotation target: Priti, all turns. Stage directions in [brackets] describe tone and body language.

Priti: You and Hollis have your own jokes now. I said "the pigeon" at lunch and you both lost it and I didn't know why.
Jas: It's just a thing from art club.
Priti: [arms folded] You used to save me the aisle seat on the bus. Today you saved it for her. It's like I'm being swapped out and nobody's told me.
Jas: That's not—
Priti: [turning away] Whatever. Sit with her then.
""",
card("jealousy", "envy", "anger"),
1, 2,
twin=T([("Priti: You and Hollis have your own jokes now. I said \"the pigeon\" at lunch and you both lost it and I didn't know why.\nJas: It's just a thing from art club.\nPriti: [arms folded] You used to save me the aisle seat on the bus. Today you saved it for her. It's like I'm being swapped out and nobody's told me.",
         "Priti: Hollis got picked for the Paris art trip. Front row at the gallery, the whole thing.\nJas: She entered the portrait competition and won.\nPriti: [arms folded] I entered too. I'd give anything to go — I've wanted to see those paintings since Year 7. It's not about her. I just want what she's got."),
        ("Whatever. Sit with her then.", "Whatever. Good for her.")],
       0)),

# ------------------------------------------------------------------ a10
# why: expected progress (sister jumped two bands, teacher said a month) didn't come; "nobody's
# fault" -> disappointment. Twin: tutor says he's on the edge, "this could be the month" -> hope.
C("a10", "Which label fits the parent (speaker B) in turn 2?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-2701 · parents' evening, teacher (A) and parent (B)
Annotation target: speaker B, turn 2. Stage directions in [brackets] describe tone and body language.

A: So Reuben has been on the reading-recovery plan for six weeks now, and he's still on the orange band.
B: [sighing, shoulders dropping] Six weeks and not a single level. We really thought it would have clicked by now — his sister jumped two bands on the same plan, and you'd said at the start most children move within a month. We've done the twenty minutes every night. It's nobody's fault, he's trying. It's just not where we'd pictured him by half-term.
A: Some children take longer.
""",
o("disappointment", "sadness", "frustration", "anger", "anxiety", "hope", "guilt", "shame", "none of these"),
"disappointment", 2,
twin=T([("[sighing, shoulders dropping] Six weeks and not a single level. We really thought it would have clicked by now — his sister jumped two bands on the same plan, and you'd said at the start most children move within a month. We've done the twenty minutes every night. It's nobody's fault, he's trying. It's just not where we'd pictured him by half-term.",
         "[leaning forward] But his tutor says he's right on the edge of green — he read a whole page to her on Friday without stopping. We've done the twenty minutes every night. If this is the month it clicks, it could change everything for him.")],
       "hope")),

# ------------------------------------------------------------------ a11
# why: whose emotion. B is wheezing with laughter at the spin -> amusement. Twin asks about A:
# hands over face, cheeks scarlet, nobody hurt, wants to hide in the cupboard -> embarrassment.
C("a11", "What emotion is speaker B primarily expressing?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-2855 · staff room after a school assembly, two teachers
Annotation target: the speaker named in the question. Stage directions in [brackets] describe tone and body language.

A: [hands over face] I tripped on the microphone cable in front of four hundred children. Four hundred. I went down like a tree and my notes went everywhere.
B: [shoulders shaking] You did a little spin first.
A: [peeking through fingers, cheeks scarlet] Nobody was hurt, the kids clapped, I know it's nothing. I just want to crawl into the stock cupboard until June.
B: [wheezing, wiping eyes] The spin, though. The spin was art. I'm going to be laughing about this at my retirement do.
""",
o("amusement", "embarrassment", "shame", "joy", "sympathy", "contempt", "surprise", "guilt", "none of these"),
"amusement", 2,
twin=T([], "embarrassment", instructions="What emotion is speaker A primarily expressing?")),

# ------------------------------------------------------------------ a12
# why: B is moved and "owes" A for a three-hour drive -> gratitude, so "other than" = no. Twin: B
# hisses, had a spare, humiliated in front of new team -> not gratitude -> yes.
Y("a12", "Is speaker B's primary emotion in turn 2 something other than gratitude?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-3016 · car park outside an office, old friends
Annotation target: speaker B, turn 2. Stage directions in [brackets] describe tone and body language.

A: [out of breath, holding up a blue inhaler] You left this on the hall table. I saw it when I got home.
B: [hand on chest] You drove three hours to bring me my inhaler? After a night shift? I don't — I don't know what to say. I'd have been in trouble on the hill walk this afternoon. I owe you, properly. Dinner, every weekend, for a month.
A: Just don't forget it again.
""",
card("gratitude", "embarrassment", "anger"),
0, 2, role="neg",
twin=T([("[hand on chest] You drove three hours to bring me my inhaler? After a night shift? I don't — I don't know what to say. I'd have been in trouble on the hill walk this afternoon. I owe you, properly. Dinner, every weekend, for a month.",
         "[glancing back at the office windows, hissing] You drove three hours to bring me my inhaler? I told you I had a spare in my bag. My whole new team just watched you wave it across the car park like I'm six. Put it away.")],
       1)),

# ------------------------------------------------------------------ a13
# why: rival club relegated, watched nine times, "sweetest night", cackling -> pleasure at a
# rival's misfortune -> schadenfreude (more specific than joy/amusement). Twin: keeper in tears,
# "I couldn't enjoy it", felt for them -> sympathy.
C("a13", "Which label fits the host (speaker A) in turn 1? Use the more specific definition when two fit.",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-3170 · supporters' podcast, recorded
Annotation target: speaker A (host), turn 1, with turn 3 as context. Stage directions in [brackets] describe tone.

A: Forty years. Forty years of them lording it over us — the chants, the banners, that open-top bus they did when we went down in '09. And last night they get relegated on the final day, by an own goal, in the ninety-fourth minute. [cackling] I've watched it nine times. Nine! Sweetest night of my life, and it wasn't even our match.
B: You're a terrible person.
A: I'm a happy terrible person.
""",
o("schadenfreude", "joy", "amusement", "contempt", "pride", "sympathy", "relief", "surprise", "none of these"),
"schadenfreude", 2,
twin=T([("[cackling] I've watched it nine times. Nine! Sweetest night of my life, and it wasn't even our match.",
         "[pause] And then I saw their keeper on his knees, in tears, and their academy kids crying in the stand. I couldn't enjoy it. Nobody deserves to go down like that."),
        ("B: You're a terrible person.\nA: I'm a happy terrible person.", "B: You've gone soft.\nA: Maybe. I just felt for them.")],
       "sympathy")),

# ------------------------------------------------------------------ a14
# why: someone is trying the door right now, caller hiding -> present threat -> fear. Twin: ex
# released, might find her one day, "nothing's happened yet" -> anxiety -> no.
Y("a14", "Is the caller primarily expressing fear?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-3302 · non-emergency police line, anonymised
Corpus note: clips are transcribed from consented recordings; each clip is double-annotated, and disagreements are resolved by a third annotator using the definitions sheet only.
Annotation target: caller (C), turns 1 and 2 together. Stage directions in [brackets] describe tone.

Operator: Police non-emergency line, how can I help?
C: [whispering, fast] There's someone trying the back door handle right now. I can hear it rattling. I'm in the bathroom with the light off and the door locked. My phone's on 8 percent.
Operator: I'm transferring you to 999 now. Stay on the line and stay where you are.
C: [breath catching] It's stopped. No — it's going again.
""",
card("fear", "anxiety"),
1, 2,
twin=T([("[whispering, fast] There's someone trying the back door handle right now. I can hear it rattling. I'm in the bathroom with the light off and the door locked. My phone's on 8 percent.",
         "[slowly] My ex-partner was released from prison last Tuesday. I moved after the trial, but I keep thinking he might find my new address one day. I've started checking the locks every night before bed."),
        ("I'm transferring you to 999 now. Stay on the line and stay where you are.",
         "I understand. I can put you in touch with a safety adviser and log your address for extra patrols."),
        ("[breath catching] It's stopped. No — it's going again.", "[quietly] Nothing's happened yet. I just can't shake it.")],
       0)),

# ------------------------------------------------------------------ a15
# why: "We did this ourselves ... we did that" about his own club -> pride. Twin: credits the
# supporters' trust who paid for the physio, "I owe every one of those people" -> gratitude.
C("a15", "What is the coach's primary emotion in turn 2?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-3488 · post-match interview, amateur rugby
Corpus note: clips are transcribed from consented recordings; each clip is double-annotated, and disagreements are resolved by a third annotator using the definitions sheet only.
Annotation target: the coach (B), turn 2. Stage directions in [brackets] describe tone and body language.

A (reporter): Bottom of the table in January, promoted today. How does that feel?
B: [chest out, grinning, gesturing at the players behind him] We did this ourselves. We rebuilt the whole defence on the training pitch — eighteen sessions in the rain, no budget, no new signings, just us. People wrote us off in January. Look at the table now. This group, this club, we did that.
A: What's next?
B: A very long night.
""",
o("pride", "gratitude", "joy", "admiration", "relief", "excitement", "amusement", "contempt", "none of these"),
"pride", 2,
twin=T([("[chest out, grinning, gesturing at the players behind him] We did this ourselves. We rebuilt the whole defence on the training pitch — eighteen sessions in the rain, no budget, no new signings, just us. People wrote us off in January. Look at the table now. This group, this club, we did that.",
         "[turning to the stand, hand raised] That's down to the supporters' trust. When the club couldn't pay for a physio in January, they raised the money themselves in a fortnight. Every win since came from that. I owe every one of those people this afternoon.")],
       "gratitude")),

# ------------------------------------------------------------------ a16
# why: conflicting documents, "can't tell which wins", explicitly not stressed with weeks to go ->
# confusion (not curiosity: she has trouble making sense of it). Twin: due at nine tomorrow, could
# lose grade and scholarship, awake since four, hands trembling -> anxiety.
C("a16", "Label the student's primary emotion in turn 1.",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-3640 · student and tutor, office hours
Annotation target: student (S), turn 1. Stage directions in [brackets] describe tone and body language.

S: [frowning, flipping between two printouts] Sorry — quick one. The assignment brief says 2,000 words "excluding appendices", but the marking rubric says "the word count includes all submitted material". Which one do we follow? I'm not stressed about it, honestly; it's not due for three weeks and I'm nearly done. I just genuinely can't tell which document wins.
T: Good catch. I'll check with the module lead and email the class.
""",
o("confusion", "anxiety", "frustration", "curiosity", "surprise", "anger", "fear", "boredom", "none of these"),
"confusion", 3,
twin=T([("[frowning, flipping between two printouts]", "[hands trembling, flipping between two printouts]"),
        ("I'm not stressed about it, honestly; it's not due for three weeks and I'm nearly done. I just genuinely can't tell which document wins.",
         "It's due at nine tomorrow, and if I pick wrong I could lose the whole grade and my scholarship with it. I've been awake since four counting and recounting.")],
       "anxiety")),

# ------------------------------------------------------------------ a17
# why: "in awe" is used ironically about a broken patch; lost saves, reinstalling, slapping desk ->
# frustration, not awe (no wonder at something vast).
Y("a17", "Is speaker A primarily expressing awe in turn 1?",
"""
Whitlow Everyday Dialogue Corpus · clip EDC-3811 · gaming voice chat, two players
Corpus note: clips are transcribed from consented recordings; each clip is double-annotated, and disagreements are resolved by a third annotator using the definitions sheet only.
Annotation target: speaker A, turn 1. Everyday words do not decide the label; the definitions and stage directions do.

A: [flat, slapping the desk] Honestly in awe of how bad this patch is. Two years of saves — gone. My 140-hour farm, gone. The launcher says "syncing" and then just closes. I've reinstalled three times tonight and I still can't get past the title screen.
B: Did you try the cloud backup?
A: [sighing] That's what it's syncing FROM. The backup is empty too.
""",
card("awe", "frustration"),
0, 2),
]
