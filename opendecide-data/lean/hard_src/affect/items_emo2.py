"""Affect hard items, batch emo2: single-label emotion with close pairs and annotation rules (items 21-40)."""
from common import E, T

ITEMS = [
# 21 anger via sarcasm ("Congratulations"), traps: disgust, admiration, joy
E("emo_mould_paintover",
"""From: Leah Mbeki
To: Harwick Lettings - Property Management
Cc: Wendlebury Council Environmental Health
Subject: Flat 4, 18 Ostler Row - black mould (reported 12 May)

Congratulations. Four months after I first reported black mould spreading across the bedroom ceiling, after two "inspections" by people who never went into the bedroom, your contractor came this morning and painted over it. Painted. Over it. It will be back through the paint within a fortnight and you know that as well as I do.

My daughter has had a chest infection since July. Her doctor has put in writing that damp is a likely factor. You have had that letter since 3 August.

I expect a written reply from you personally, not from the enquiries inbox, by Friday, setting out when the leak behind the ceiling will be fixed. If I don't get one, environmental health will be getting the photos, the doctor's letter and every email in this chain, and I will be naming your company in every tenant forum and review site I can find.

Leah Mbeki""",
"anger", 1, near=["disgust", "annoyance", "disapproval", "admiration"], t="Leah's email"),

# 22 fear (present danger, no fear words), traps: caring, nervousness
E("emo_intruder_texts",
"""Annotation guideline (excerpt): Label the single emotion the author most directly expresses. If none of the listed emotions is expressed, use neutral.

Text messages, 02:14-02:19, from Yasmin (number 12) to Gil (number 14)

02:14 Gil are you awake
02:14 someone is in our back garden with a torch. they just tried the kitchen door handle
02:15 i'm upstairs with the kids in the bathroom, lights off. Karim is away until thursday
02:15 rang the police, they said ten minutes
02:16 they're trying the side window now. i can hear it rattling
02:17 please DON'T come over on your own. just keep your outside light on and your phone near you
02:19 torch is gone from the garden but i can't tell if they're still at the side""",
"fear", 1, near=["nervousness", "caring", "anger", "surprise"], t="Yasmin's texts"),

# 23 gratitude, traps: relief, caring, love
E("emo_neighbour_thanks",
"""Card left in the letterbox of 7 Juniper Close, Tuesday

Dear Rhona and Paul,

We got back at last on Sunday night, two days late, after the airline cancelled our connection and we ended up sleeping on a bench in Terminal 2. The first thing we saw when we opened the door was Pepper, fed, brushed, and asleep on the radiator, the parcel from my mother on the hall table, and the bins back in from the kerb.

You didn't have to do any of that. You'd only agreed to water the tomatoes. Thank you, truly, both of you, for going so far beyond what we asked. Pepper clearly thinks she has moved house.

There's a bottle of the Sicilian red you liked on your doorstep, and we'd love to have you both round for dinner once we've unpacked.

With thanks,
Imogen and Dara""",
"gratitude", 1, near=["relief", "caring", "love", "joy"], t="the card"),

# 24 sadness (explicitly not death, not unmet expectation), traps: grief, disappointment
E("emo_ward_evening",
"""Private journal kept by a ward nurse (shared anonymously on a staff wellbeing site with the author's permission)

Thursday.

Some shifts just sit on you. Nothing dramatic happened today. Nobody died on the ward, nobody shouted at me, the handover was on time for once. Mrs K asked me three times this afternoon when her son was coming, and each time I told her gently that he'd phoned to say it would be the weekend. She said "oh, that's nice" every time, as if it were news.

I drove home the long way, past the reservoir, and sat in the car outside the flat for twenty minutes with the engine off. I didn't cry exactly. I just felt heavy, like someone had turned the colour down on everything. I made toast and didn't eat it.

I'm on again at 7. It'll probably be fine.""",
"sadness", 2, near=["grief", "disappointment", "caring", "nervousness"], t="the journal entry"),

# 25 remorse, traps: embarrassment, sadness
E("emo_merged_branch",
"""Direct message, Monday 08:05

From: Tobias Lindgren
To: Mei-Ling Cho

Mei-Ling, I owe you a proper apology, not just the one-line one I sent on Friday night.

I merged the refactor branch without reading the migration warning, and it wiped the annotation table. That was two weeks of your labelling work, and you spent your weekend redoing the first batch because of my carelessness. You had plans with your family on Saturday and you cancelled them. That's on me and nobody else.

I've done three things since: restored what I could from Thursday's snapshot (about 60% of your labels, list attached), set up nightly backups of that table, and changed the merge settings so a destructive migration needs a second reviewer. None of that gives you your weekend back. I'm really sorry.

If you want to take Friday off in lieu, I've already cleared it with Sunita.""",
"remorse", 1, near=["embarrassment", "sadness", "caring", "gratitude"], t="Tobias's message"),

# 26 desire, traps: love, optimism, admiration
E("emo_teak_desk",
"""Voice note transcribed by a notes app, Saturday 16:40 (Anneke, talking to herself while walking home)

"Note to self. The teak writing desk in the window of Holloway & Daughters on Harbour Street, the one with the brass-edged drawers and the little green leather inset. That's the fourth time this week I've crossed the road to look at it. I want it so badly it's ridiculous. I keep imagining it under the bay window with the lamp on it. It's 640 and I've got about 410 in the house fund that isn't earmarked. Ask if they'd hold it for a deposit. Ask if they do instalments. Check whether it'll actually fit up the stairs, measure the turn on the landing. Also, buy milk.\"""",
"desire", 1, near=["love", "optimism", "admiration", "excitement"], t="Anneke's voice note"),

# 27 joy (not pride, not relief), traps: pride, love, gratitude
E("emo_tomatoes",
"""Garden diary, allotment plot 17, Sunday 3 August

Warm, still, 24 C by four o'clock.

First proper tomatoes of the year, a whole bowl of the little yellow ones from the plants Joan next door passed over the fence in May. I sat on the upturned crate by the shed with the bowl on my knee, eating them one after another while they were still warm from the sun. The sparrows were bickering in the hedge and someone three plots down was playing old dance-band music on a radio. I don't think I've been this happy on an ordinary Sunday in years.

Jobs for next week: tie in the cordons again, the tallest have bent; net the brassicas before the pigeons find them; ask Joan whether she wants any of the courgettes, because there are far too many.""",
"joy", 1, near=["pride", "gratitude", "love", "relief"], t="the diary entry"),

# 28 annoyance via sarcasm, traps: joy/amusement keywords
E("emo_printer_floor3",
"""#floor-3-general (Slack), Friday 10:17

Maren Holt: Oh, wonderful. The printer by the kitchen has once again decided that A4 is more of a suggestion than a paper size. Fourth jam this morning, and it's always halfway through a 40-page contract. I'll be over here feeding it one sheet at a time like a baby bird if anyone needs me. Has anyone actually reported it, or are we all just silently suffering?

Colin Mistry: I reported it on Tuesday, ticket IT-8841. They said a replacement drum was on order.

Maren Holt: Of course it is.

Colin Mistry: The one on floor 4 by the lifts works if you're desperate.""",
"annoyance", 2, near=["joy", "amusement", "anger", "disappointment"], t="Maren's first message"),

# 29 confusion, traps: nervousness, annoyance, anger
E("emo_two_letters",
"""Annotation guideline (excerpt): Label the single emotion the author most directly expresses. If none of the listed emotions is expressed, use neutral.

Letter received by Lumen Grid Energy customer correspondence team, handwritten, scanned 11 September

Dear Sir or Madam,

Account 4401-778-2

On Saturday I received two letters from you in the same post. The first one, dated 2 September, says my account is in credit by £41.20 and that I owe nothing. The second one, dated 3 September, says that because my account is in arrears my monthly payment will go up from £64 to £96 from October.

I have read them both several times at the kitchen table and I can't make them agree. Am I in credit or am I behind? If I am in credit, why is the payment going up? If I am behind, what is the £41.20? I have not changed anything and I have paid every month by direct debit since 2011.

Please could someone explain in plain words which letter is the right one.

Yours faithfully,
Edith Carrow (Mrs)""",
"confusion", 1, near=["nervousness", "annoyance", "anger", "curiosity"], t="Mrs Carrow's letter"),

# 30 topic rule: disappointment about the topic, gratitude elsewhere; twin changes topic -> gratitude
E("emo_topic_headphones",
"""Annotation guideline (excerpt): Each review carries a Topic field. Label the emotion the reviewer expresses about the Topic only; ignore emotions about any other part of the purchase.

Review ID: KR-55120
Topic: the headphones
Product: Kestrel Pro ANC over-ear headphones (order shipped via Parcelwise)

"Two parts to this. First, the delivery: the Parcelwise driver carried all four of my boxes up three flights because the lift was out, and waited while I found my glasses to sign. Huge thanks to him, genuinely, he saved my back.

Second, the headphones. Every review I'd read said the noise cancelling on these was the best in its price range, and that's why I paid the extra £60 over the model I was going to buy. On the bus it's barely noticeable; I can still hear every conversation behind me. Battery and comfort are fine. I'd pictured blissful silence on my commute and I've got slightly muffled chatter.\"""",
"disappointment", 3, near=["gratitude", "annoyance", "admiration", "sadness"], t="the reviewer",
twin=T([("Topic: the headphones", "Topic: the delivery")], "gratitude")),

# 31 embarrassment (harmless), traps: amusement, remorse
E("emo_glass_door",
"""Direct message, first week at a new job

From: Sofia Andrade
To: her friend Lucie (who works elsewhere)

ok I need to tell someone. new office has these enormous glass doors into the atrium and they are SPOTLESS. I was walking out of the induction talking to the head of department, feeling very professional, and walked straight into the closed one. Full forehead. Loud. Everyone in the atrium turned round. I'm fine, not even a bump, and the door is fine. But the head of department had to ask if I was OK, and I said "yes, sorry, I was just testing it", which made it worse.

I've been sitting at my desk for an hour with my face burning, pretending to read the IT policy. I'm going to have to walk past that door every single day until I retire.""",
"embarrassment", 1, near=["amusement", "remorse", "fear", "sadness"], t="Sofia's message"),

# 32 pride (own achievement), traps: relief, joy, gratitude
E("emo_quilt_finish",
"""Thornbury Quilters' Guild - show-and-tell thread
Post by Ruth Adeyinka

Finished! Photo attached. The double-wedding-ring quilt I started in January 2023: 2,016 hand-pieced arcs, every one of them cut and stitched by me, and hand-quilted on the frame in the back bedroom. I unpicked the whole third row twice because the curves wouldn't sit flat, and I refused to let the machine do the quilting even when my wrists were begging me to.

It's hanging over the banister now and every time I walk past it I stop and look at it. I made that. Two and a half years of evenings, and it is the best thing I have ever made with my hands.

It's going to the county show in October. The pattern notes and my templates are in the guild library for anyone brave enough.""",
"pride", 1, near=["joy", "relief", "admiration", "love"], t="Ruth's post"),

# 33 approval vs disapproval (others are angry); twin -> disapproval
E("emo_parking_permit",
"""Comments section, Fenwick Gazette online: "Council brings in resident permits for Albion Street"

Comment by d_whitlow:
Lots of anger in these comments, so here's a calmer take. I live on Albion Street and I've read the consultation report. Commuters parking for the station were filling the street by 7 AM and the carers who visit number 22 had nowhere to stop, so I think permits are the right approach for our road, and £40 a year is a reasonable price for that.

Some of you are furious about the visitor-pass limit. The report says it will be reviewed after six months.

For anyone asking, applications open on the council website on 1 October and you need a utility bill in your name.""",
"approval", 2, near=["disapproval", "anger", "admiration", "optimism"], t="d_whitlow's comment",
twin=T([("Commuters parking for the station were filling the street by 7 AM and the carers who visit number 22 had nowhere to stop, so I think permits are the right approach for our road, and £40 a year is a reasonable price for that.",
         "The report's own survey found the street is never more than two-thirds full, even at 7 AM, so I think permits are the wrong approach for our road, and £40 a year to fix a problem we don't have is poor value.")],
       "disapproval")),

# 34 neutral: author forwards someone else's anger
E("emo_forwarded_complaint",
"""Annotation guideline (excerpt): Label the emotion expressed by the person who wrote the message. Text they quote or forward from someone else is not their expression. If they express no listed emotion themselves, use neutral.

From: Farida Nasser (Customer Operations)
To: Platform on-call
Subject: FW: Checkout failures - Brenwick Outfitters

Forwarding the below from Brenwick's ops director, received 15:02:

> "This is completely unacceptable. We lost three hours of Saturday checkout during our biggest sale of the year. I am furious and I want a named person to call me today."

Can someone on-call pull the gateway logs for 12:00-15:00 and check whether the failures line up with the certificate rotation? Account manager is Ben Ochieng, cc'd. I've told Brenwick we'll call by 17:00 with a status update. Incident ref INC-4471.

Farida""",
"neutral", 2, near=["anger", "nervousness", "annoyance", "disapproval"], t="Farida's message"),

# 35 realization, traps: surprise, amusement, disgust
E("emo_cat_tuesdays",
"""Annotation guideline (excerpt): Label the single emotion the author most directly expresses. If none of the listed emotions is expressed, use neutral.

Ask the Vet Nurse (reader forum) - thread "Cat only vomits on Tuesdays??"

Original post (Monday): For about two months our cat Pickle has been sick on the hall floor almost every Tuesday afternoon and not on other days. Same food all week. Vet found nothing. Any ideas?

Follow-up post by the same reader (Wednesday):
Thank you for all the suggestions. I was typing out a reply listing everything that happens on Tuesdays, and halfway through the list I stopped. Tuesday is the day our cleaner comes, and she mops the hall with that lemon floor cleaner, and Pickle lies on the hall tiles every afternoon because they're cool. She's been licking it off her paws. It's been in front of me the whole time. I've asked the cleaner to switch to plain water in the hall and I'll report back in a fortnight.""",
"realization", 2, near=["surprise", "amusement", "disgust", "gratitude"], t="the follow-up post"),

# 36 curiosity vs neutral request; twin -> neutral
E("emo_museum_query",
"""Enquiry form - Holt Valley Industrial Museum
Submitted by: Declan Farrow
Topic: Collections

"Hello. On Saturday I visited the textile gallery and the label next to the 1890s jacquard loom mentions that the punched cards were later reused by the mill as ledger dividers. I'd love to know more about that. Were the reused cards still readable as patterns, and has anyone ever tried to reconstruct the designs from them? I'm also wondering whether the museum's archive has any of the ledgers with the cards still inside.

If it's easier to answer in person, I'm happy to come in on one of the archive open days. My email is on the form.\"""",
"curiosity", 2, near=["confusion", "admiration", "desire", "neutral"], t="Declan's enquiry",
twin=T([("I'd love to know more about that. Were the reused cards still readable as patterns, and has anyone ever tried to reconstruct the designs from them? I'm also wondering whether the museum's archive has any of the ledgers with the cards still inside.",
         "For a citation in my thesis I need the accession number of that loom and the name of the collection it belongs to. Please also confirm the label text is quoted correctly: \"punched cards later reused as ledger dividers, c. 1905\".")],
       "neutral")),

# 37 grief vs sadness; twin -> sadness
E("emo_grey_week",
"""Post in the "Getting Through It" peer-support group, Friday night

I don't really have a question, I just wanted to write it somewhere.

It's been eleven days since we buried my brother. I keep picking up my phone to send him the stupid photos I always sent him, the dog in a hat, a sign with a spelling mistake, and then I remember and put it back down. Everything feels grey. I haven't seen anyone except the postman since Tuesday. I went to the supermarket and stood in front of the cereal for ten minutes and came home with nothing.

People at work have been kind. I know it's supposed to get easier. Tonight it doesn't feel like it will.

Thanks for reading, if anyone does.""",
"grief", 2, near=["sadness", "love", "disappointment", "gratitude"], t="the post",
twin=T([("It's been eleven days since we buried my brother. I keep picking up my phone to send him the stupid photos I always sent him, the dog in a hat, a sign with a spelling mistake, and then I remember and put it back down.",
         "It's been eleven days of rain and I've been working from home the whole time. Nothing's wrong exactly; my brother is fine, everyone's fine, I just feel flat.")],
       "sadness")),

# 38 amusement vs annoyance (teacher and a hamster excuse); twin -> annoyance
E("emo_hamster_excuse",
"""Staffroom message board, Harrowgate Middle School - note from Mr Iqbal (Year 7 English)

Homework log, 7C, Monday:

Theo's explanation for the missing essay, reproduced exactly: "It was eaten by the class hamster. The one we don't have yet but will get if we are good." I laughed out loud at my desk, and I'm still smiling about it now. Genuinely one of the best I've had in twelve years of teaching.

He's been told the essay is due Thursday instead, and I've suggested he put that talent into the creative-writing competition, deadline 30 October.

Other missing work for 7C: Amara and Jonah (both absent Friday, extension agreed). Reminder to all Year 7 staff that reports are due to heads of year by the 15th.""",
"amusement", 2, near=["annoyance", "joy", "admiration", "disapproval"], t="Mr Iqbal's note",
twin=T([("I laughed out loud at my desk, and I'm still smiling about it now. Genuinely one of the best I've had in twelve years of teaching.",
         "That is the third invented excuse from Theo this half-term and I'm running out of patience with them. Honestly, it's wearing.")],
       "annoyance")),

# 39 love (for a person), traps: gratitude, caring, joy
E("emo_anniversary_letter",
"""Letter tucked into a fortieth-anniversary card, read aloud at the party by the couple's granddaughter (with permission)

Bernard,

Forty years ago you turned up at my parents' house in a borrowed suit that was far too long in the arms, and you asked my father if you could take me to the pictures. You were so nervous you called him "Your Honour".

I've loved you every day since, even the days you reversed the caravan into the gatepost and the winter you decided to learn the bagpipes. You're the first person I want to tell everything to, and still the last voice I want to hear before I sleep. There is nobody on this earth I would rather grow old and cranky beside.

Happy anniversary, my darling.

Always,
Margot""",
"love", 1, near=["gratitude", "joy", "amusement", "caring"], t="Margot's letter"),

# 40 optimism (about someone else's recovery), traps: caring, nervousness, sadness
E("emo_rehab_update",
"""Family update email, sent to the "Friends of Nell" list by her husband, Aurelio

Hi all,

Week three at the rehabilitation unit. Nell's physio had her standing between the parallel bars for ninety seconds on Monday and nearly three minutes today. She still tires quickly and the left hand isn't doing much yet. The consultant was careful to say that nobody can promise anything with this kind of stroke.

But I watched her today and I believe she will walk out of that unit on her own two feet by spring. Everything is moving in the right direction, a little more each week, and she is more determined than anyone I've ever met. We're going to get there.

Visiting is 2-4 and 6-8. She'd love postcards more than flowers (the ward won't take flowers). The address is on the attached sheet.

Aurelio""",
"optimism", 2, near=["caring", "nervousness", "admiration", "sadness"], t="Aurelio's email"),
]
