"""affect_c / customer-contact QA emotion tagging (Harrowgate Contact Centre and its invented clients)."""
from _lib import C, Y, T

D = {
    "anger": "The customer holds a specific person or organisation responsible for a wrong done to them and blames, accuses or demands redress from them.",
    "frustration": "The customer is irritated at being blocked, stalled or sent round in circles while trying to reach a goal, without accusing anyone of a wrong.",
    "impatience": "The customer is restless about a wait that is still going on, with the focus on how long it is taking right now.",
    "disappointment": "The customer is unhappy that an outcome they expected or hoped for did not happen; the focus is the gap between expectation and result, and no one is blamed.",
    "sadness": "Sorrow about a painful situation or loss that is not better described by a more specific label in this list.",
    "grief": "Sorrow over the death or permanent loss of a person or animal the customer loved.",
    "anxiety": "Worry about a possible bad outcome that has not happened yet.",
    "fear": "Alarm at a threat to safety that is present right now.",
    "relief": "The easing of worry or distress because a feared outcome did not happen or has ended.",
    "hope": "Looking forward to a wanted outcome that may still happen, with attention on the chance that it will.",
    "gratitude": "Warm appreciation directed at another party for help or a benefit that party gave.",
    "satisfaction": "Contentment that a product or service has met the customer's needs, without thanks directed at anyone in particular.",
    "pride": "Pleasure in an achievement the customer credits to themself.",
    "amusement": "Finding something genuinely funny and enjoying it.",
    "confusion": "Not understanding what is happening or what something means, without a stronger negative feeling dominating.",
    "contempt": "Regarding a party as incompetent, inferior or beneath respect, shown through disdain or mockery rather than an accusation of a specific wrong.",
    "embarrassment": "Discomfort at one's own social slip or awkward exposure in front of others, where no one has been seriously harmed.",
    "guilt": "A bad feeling about a specific action of one's own that harmed someone else, with an urge to apologise or make amends.",
    "shame": "A painful sense that one's whole self is flawed or worthless, with an urge to hide.",
    "regret": "Wishing one had chosen differently, with the focus on what the choice cost oneself.",
    "none of these": "The customer's primary emotion is not any of the emotions listed.",
}


def o(*names):
    return [(n, D[n]) for n in names]


def card(*names):
    return [(n, D[n]) for n in names]


ITEMS = [
# ------------------------------------------------------------------ s01
# why: sarcasm ("wonderful", "myth") coded by meaning; customer explicitly blames no one and
# just wants to reach the parcel -> frustration. Twin adds an accusation of the driver lying
# plus a demand for redress -> anger.
C("s01", "Which emotion label from the Customer Emotion Guide should QA assign to the customer in this chat?",
"""
Harrowgate Contact Centre — QA emotion tagging, client: Parcelwise
Ticket PW-558120 · channel: web chat · 14:52

Guide reminders for this client: tag the customer's primary emotion. Sarcasm and irony are tagged by their intended meaning, never by the literal words.

Agent (Bex): Hi, thanks for waiting. I can see parcel PW-558120 is showing "out for delivery".
Customer (Gareth Linwood): Oh wonderful. That's the fourth "out for delivery" this week, and still nothing on the doormat. I'm starting to think the van is a myth, like the Loch Ness monster but with a tracking number.
Agent: I'm sorry about that. The system shows it is on vehicle 12 today.
Customer: It showed that on Monday. And on Wednesday. Look, nobody needs to be sacked over it, I just need the thing. Can someone tell me which depot has it so I can drive over and pick it up myself?

Customer rating left at end of chat: 2/5.
""",
o("anger", "frustration", "disappointment", "amusement", "confusion", "anxiety", "gratitude", "sadness", "satisfaction", "none of these"),
"frustration", 2,
twin=T([("Look, nobody needs to be sacked over it, I just need the thing. Can someone tell me which depot has it so I can drive over and pick it up myself?",
         "And today your driver marked it 'customer not in' while I sat by the door all afternoon. He lied on the record, and I want him reported and my delivery fee refunded.")],
       "anger")),

# ------------------------------------------------------------------ s02
# why: final turn = the hold was released, nothing taken, "heart can slow down" -> relief.
# Twin: hold still under review for 48h, final turn is worry about what may happen -> anxiety, so not relief.
Y("s02", "Under this queue's tagging rule, is the customer primarily expressing relief?",
"""
Orrin Mobile — Fraud & Disputes line · call transcript excerpt · QA sample 7/40
Tagging rule for this queue: when a customer shows more than one emotion, tag the emotion in the customer's final turn.

Customer (Ms Adaeze Obi): There's a £640 payment to something called "VNTR*GLOBAL" on my account and I didn't make it. I've been pacing the kitchen since six this morning. That's my rent.
Agent (Callum): Let me look... Right. That isn't a payment. It's a pre-authorisation hold from the car-hire firm you booked last week. It was released at 11:02 this morning, and the full £640 is back in your available balance. Nothing has left your account.
Customer: So it's gone? Nothing was taken? ...Okay. Okay. My heart can slow down now. Sorry for shouting earlier, I thought someone had got into everything.

Call length 6m 12s. Outcome code: see case notes.
""",
card("relief", "anxiety", "gratitude"),
1, 2,
twin=T([("It was released at 11:02 this morning, and the full £640 is back in your available balance. Nothing has left your account.",
         "It hasn't been released yet; our fraud team will know within 48 hours whether it is genuine, and until then the £640 stays unavailable."),
        ("So it's gone? Nothing was taken? ...Okay. Okay. My heart can slow down now. Sorry for shouting earlier, I thought someone had got into everything.",
         "Forty-eight hours? So I just wait two days not knowing whether my rent is still there? I won't sleep until someone rings me back.")],
       0)),

# ------------------------------------------------------------------ s03
# why: expected deluxe edition did not come; customer explicitly says nobody is at fault -> disappointment.
# Twin: shop knew the run was short and kept taking deluxe money; customer holds them responsible
# and demands redress -> anger.
C("s03", "Using the guide's definitions, what is the customer's primary emotion in this email?",
"""
Harrowgate QA — client: Gildwick Games (online shop) · email ticket GG-20417

From: Rowan Pell
Subject: Order 88-1045 — deluxe edition

Hi,
My order for Lanterns of Ossory arrived this morning — the standard edition, not the deluxe I pre-ordered in March. I've read the email you sent round last month explaining that the deluxe print run came up short and that some pre-orders would be switched with a partial refund. It's not anyone's fault the print run fell short; these things happen with small publishers. It's just that I'd been counting down to the metal coins and the cloth map for five months, and now they're not coming. Please go ahead and refund the difference to my card.
Thanks,
Rowan

Tagging rule: tag the customer's primary emotion as expressed in the message.
""",
o("disappointment", "sadness", "anger", "frustration", "regret", "anxiety", "gratitude", "satisfaction", "confusion", "none of these"),
"disappointment", 2,
twin=T([("I've read the email you sent round last month explaining that the deluxe print run came up short and that some pre-orders would be switched with a partial refund. It's not anyone's fault the print run fell short; these things happen with small publishers.",
         "Your own forum post shows you knew in February that the deluxe run was short, yet you went on taking full deluxe payments, mine included, in March. That is taking money for something you knew you couldn't send, and I hold you responsible."),
        ("It's just that I'd been counting down to the metal coins and the cloth map for five months, and now they're not coming. Please go ahead and refund the difference to my card.",
         "I want a full refund today and a written explanation from your managing director.")],
       "anger")),

# ------------------------------------------------------------------ s04
# why: "Thanks SO much" is sarcastic (40 min hold, transfer loop, scores 1/1/0); intended emotion
# is not gratitude -> yes to the negative question. Twin: sincere thanks to a named agent -> gratitude -> no.
Y("s04", "Is the customer's intended primary emotion in this survey answer something other than gratitude?",
"""
Harrowgate QA — client: Brightfold Bank · post-call survey free-text · ref BF-S-33190

Q: "Anything else you'd like to tell us about today's call?"
Customer answer (verbatim): "Thanks SO much for the forty minutes of hold music. The same eight bars of pan pipes, over and over, really made my morning. And the part where I was transferred to the department that transferred me back to the first department? Chef's kiss. I only rang to change my address. I'll be doing it in the branch."

Survey scores given: agent helpfulness 1/5, ease 1/5, likelihood to recommend 0/10.

Coding notes for analysts: tag the emotion the customer intends to convey; irony and sarcasm are coded by their intended meaning.
""",
card("gratitude", "frustration"),
1, 2, role="neg",
twin=T([("Thanks SO much for the forty minutes of hold music. The same eight bars of pan pipes, over and over, really made my morning. And the part where I was transferred to the department that transferred me back to the first department? Chef's kiss. I only rang to change my address. I'll be doing it in the branch.",
         "Thank you so much to Priyanka, who stayed on the line past the end of her shift and never once rushed me. I only rang to change my address, and she spotted that my pension was still being paid into my old account and moved it for me. I'll be writing to her manager."),
        ("agent helpfulness 1/5, ease 1/5, likelihood to recommend 0/10", "agent helpfulness 5/5, ease 4/5, likelihood to recommend 10/10")],
       0)),

# ------------------------------------------------------------------ s05
# why: whose emotion. The mother keeps asking whether men will come to take her furniture or
# house = worry about a possible future harm -> anxiety (not fear: no present threat).
# Twin asks for the caller's own emotion: he blames the company for broken promises and demands
# redress -> anger.
C("s05", "According to the caller, what is his mother's primary emotion?",
"""
Harrowgate QA — client: Tallis Energy · complaint call · CASE TE-90022

Caller (Mr Hamid Serrano, calling on behalf of his mother, account holder Mrs Lucia Serrano, 81):
"I'll tell you exactly why I'm calling. My mother was billed £1,900 for a meter reading your own engineer admitted was wrong, in writing, in June. You promised a corrected bill within fourteen days. That was eleven weeks ago. Since then your system has sent her three red 'final demand' letters. Every time the post comes she asks me whether men are going to come and take her furniture, whether she'll lose the house. She isn't sleeping. I want the demands withdrawn today, and I want a named person responsible for this case, because your company has broken its own promise three times."

Agent summary: caller raised his voice twice; demanded escalation; complaint logged at stage 2.
""",
o("anger", "anxiety", "fear", "frustration", "sadness", "confusion", "contempt", "disappointment", "guilt", "shame", "none of these"),
"anxiety", 3,
twin=T([], "anger", instructions="What is the caller's own primary emotion in this call?")),

# ------------------------------------------------------------------ s06
# why: stated rule = tag the emotion the customer names as strongest; she names (3), not
# understanding the meter -> confusion. Twin names (1), appreciation of the engineer -> gratitude.
C("s06", "Applying the client's tagging rule, which emotion should be tagged for this customer?",
"""
Harrowgate QA — client: Tallis Energy · email ticket TE-91873

From: Wendy Achterberg
Subject: Smart meter visit — three things

Hello,
Three things after yesterday's visit.
(1) The engineer, Devan, was lovely. He fixed the fault in twenty minutes, explained what he was doing and even moved the bike so he could get at the cupboard. Please pass on how much I appreciate him.
(2) I'm still irritated that it took two missed appointment slots to get him here.
(3) I don't understand the new meter. The display shows two readings, the app shows a third, and nobody has told me which one I'll be billed on.
If you asked me which of these is the strongest for me right now, it's number 3.
Regards,
Wendy

Tagging rule: when a message expresses several emotions, tag the one the customer names as strongest; if none is named, tag the one in the last sentence.
""",
o("confusion", "gratitude", "frustration", "anger", "satisfaction", "anxiety", "impatience", "disappointment", "none of these"),
"confusion", 2,
twin=T([("it's number 3.", "it's number 1.")], "gratitude")),

# ------------------------------------------------------------------ s07
# why: minor social slip (silly voice note heard by triage staff), she says nobody is hurt,
# wants to crawl under the desk, face on fire -> embarrassment, not shame (no whole-self
# judgement) or guilt (no harm to anyone).
Y("s07", "Is the customer primarily expressing embarrassment in this chat?",
"""
Harrowgate QA — client: Orrin Mobile · web chat · ref OM-C-77310

Customer (Tamsin Heald): Hi. This is a weird one. About ten minutes ago I meant to send a voice note to my sister and it went to your WhatsApp support number instead. It's me singing happy birthday to her very badly and then doing a dog impression. Can it be deleted before anyone listens to it?
Agent (Joel): Hi Tamsin! It's already been played by our triage team, I'm afraid, but I've deleted it now and it won't be kept on file.
Customer: Oh no. Oh no no no. My face is on fire. It's not a big deal, I know, nobody's hurt, nothing bad happened. I just want to crawl under the desk. Please tell the team to forget the dog bit.
Agent: Consider it forgotten. For what it's worth, the dog was very convincing.
Customer: Stop 🙈

Guide note: tag the customer's primary emotion across the chat.
""",
card("embarrassment", "shame", "guilt", "amusement"),
1, 2),

# ------------------------------------------------------------------ s08
# why: connection is tomorrow and may be cancelled; customer is worried about a possible bad
# outcome -> anxiety (not fear: no present threat). Twin: the flight already happened, he made
# it, "can finally breathe", shoulders dropped -> relief.
C("s08", "What is the customer's primary emotion in their final message, per the client's tagging rule?",
"""
Harrowgate QA — client: Skylark Regional Airways · messaging channel · ref SK-40218

Customer (Mr Ellis Ngata): Hi, booking ref QX7L2P. I'm flying Tarrow to Vell tomorrow at 07:10 and connecting to Port Addie at 10:35. The forecast says the storm reaches Vell overnight. What happens if the Vell connection is cancelled? My daughter's wedding is on Saturday morning and I'm giving the speech. I've checked the app eleven times tonight.
Agent (Sunniva): I understand. If the connection is cancelled we will rebook you on the next available service or offer a refund.
Customer: The next available service could be Sunday. Please, is there anything you can do now, before it happens?

Tagging rule for this client: tag the customer's primary emotion in their final message; attend to whether the event they react to is still ahead of them or already over.
""",
o("anxiety", "relief", "fear", "hope", "impatience", "frustration", "sadness", "gratitude", "anger", "none of these"),
"anxiety", 2,
twin=T([("I'm flying Tarrow to Vell tomorrow at 07:10 and connecting to Port Addie at 10:35. The forecast says the storm reaches Vell overnight. What happens if the Vell connection is cancelled?",
         "I flew Tarrow to Vell this morning and made the 10:35 connection to Port Addie with four minutes to spare, running the length of the terminal while the storm closed Vell behind us. Every flight after ours was cancelled."),
        ("I've checked the app eleven times tonight.", "I'm in Port Addie now."),
        ("I understand. If the connection is cancelled we will rebook you on the next available service or offer a refund.",
         "I can see you were on the last departure out of Vell today."),
        ("The next available service could be Sunday. Please, is there anything you can do now, before it happens?",
         "For two days I was sure I'd miss her walking down the aisle. My shoulders have finally come down. I just need to know where my suitcase went.")],
       "relief")),

# ------------------------------------------------------------------ s09
# why: one-star sarcastic review ("10/10", "Fantastic", "Truly the future") about a kettle that
# keeps failing; intended meaning is irritation at being blocked, not amusement -> no.
Y("s09", "Is the reviewer primarily expressing amusement?",
"""
Harrowgate QA — client: Kelderhome smart appliances · app-store review routed to support · ref KH-R-1204

Rating: ★☆☆☆☆
Title: Truly the future
"10/10 would recommend if you enjoy boiling water with your phone. Every morning the kettle 'forgets' my Wi-Fi, so I stand in the kitchen at 6:40, barefoot, re-pairing a kettle, while the kids ask why there's no tea. Yesterday the app pushed a firmware update mid-boil and the kettle just... stopped. Half-warm water. Fantastic. Can't wait to see what it forgets tomorrow. Before anyone asks: yes, I have reset it. Four times. Following your own 12-step guide."

Coding note: sarcasm and irony are coded by intended meaning. Emoji and star ratings count as context.
""",
card("amusement", "frustration"),
0, 2),

# ------------------------------------------------------------------ s10
# why: her own act (sending untracked to save £1) harmed her customer, who missed the ceremony;
# she wants to apologise and make amends -> guilt. Twin: the cost falls on herself (lost sale,
# paid twice) and she wishes she had chosen differently -> regret.
C("s10", "Which label from the guide fits the writer's primary emotion?",
"""
Harrowgate QA — client: Parcelwise Business · email · ref PWB-6621

From: Esi Mensah, owner, Fernbrook Candles
Subject: Parcel for Mrs Dorsey — my mistake

Hi team,
I'm writing about parcel PWB-6621-A. My customer, Mrs Dorsey, ordered a set of candles for her daughter's naming ceremony on Saturday. To save a pound I sent it untracked economy instead of the next-day service she paid for at checkout, and now it hasn't arrived and she's had to go without them for the ceremony. That's on me, not on your drivers.
Could you please arrange an express resend of a replacement set today? I'll pay whatever it costs. I'd also like to include a handwritten note apologising to her properly — can the driver hand it over with the box?
Thanks,
Esi
""",
o("guilt", "shame", "regret", "embarrassment", "anger", "disappointment", "sadness", "anxiety", "frustration", "none of these"),
"guilt", 3,
twin=T([("and now it hasn't arrived and she's had to go without them for the ceremony.",
         "and now she has cancelled, claimed her money back through her card company, and I've paid for the candles and the postage with nothing to show for it."),
        ("Could you please arrange an express resend of a replacement set today? I'll pay whatever it costs.",
         "Could you please return the original parcel to me when it turns up?"),
        ("I'd also like to include a handwritten note apologising to her properly — can the driver hand it over with the box?",
         "I should have spent the extra pound. Choosing economy has cost me the whole sale, and I keep wishing I'd ticked the other box.")],
       "regret")),

# ------------------------------------------------------------------ s11
# why: customer rules out being annoyed; mocks staff competence ("couldn't organise a queue",
# "speak slowly", "which way up") without accusing them of a specific wrong -> contempt.
C("s11", "Under the guide, what is the customer's primary emotion across this chat?",
"""
Harrowgate QA — client: Orrin Broadband · live chat · ref OB-C-50917

Customer (user "d.varga"): I'm not even annoyed any more, I've gone past that. Your lot couldn't organise a queue in a bakery. Three engineers, three different "diagnoses", and one of them tried to fix a fibre fault by turning the router upside down. Put me through to someone who knows what a router is, if the building contains one. I'll speak slowly for them.
Agent (Hollie): I'm sorry to hear about your experience. I can book a senior technician for Thursday.
Customer: A "senior" one. Does he know which way up it goes? Fine. Thursday.

Coding note: tag the customer's primary emotion; do not tag a feeling the customer explicitly says they no longer have.
""",
o("contempt", "anger", "frustration", "amusement", "disappointment", "impatience", "confusion", "sadness", "none of these"),
"contempt", 3),

# ------------------------------------------------------------------ s12
# why: rule = final sentence; final sentence is keeping the phone by her and asking to be rung
# the minute it's found -> hope. Twin: final sentence pictures the ring going down a drain,
# hands shaking -> anxiety, so not hope.
Y("s12", "Under the client's tagging rule, is the guest primarily expressing hope?",
"""
Harrowgate QA — client: Marrowby Hotels · phone · ref MH-LF-3380 (lost property)

Guest (Mrs Ilse Fairweather) — transcript extract:
"I stayed in room 214 from the 3rd to the 5th. I think my ring came off with the bath towel on the last morning — a thin gold band with a small garnet. It was my grandmother's; it's the only thing of hers I have. Reception told me housekeeping would search the laundry cage tonight before the linen van collects at six. I know it's a small thing and the odds aren't great. But they said a ring turned up in a pillowcase last month, so it does happen. If there's even a chance, I'll keep my phone next to me all evening — please ring me the minute they find anything."

Tagging rule for this client: when more than one emotion is present, tag the one in the guest's final sentence.
""",
card("hope", "anxiety"),
1, 2,
twin=T([("If there's even a chance, I'll keep my phone next to me all evening — please ring me the minute they find anything.",
         "I keep picturing it going through the industrial washer and down a drain before anyone looks, and my hands won't stop shaking.")],
       0)),

# ------------------------------------------------------------------ s13
# why: customer rules out upset and hurry; says it is "mind-numbingly dull" = boredom, which is
# not in the list -> none of these. Twin: has to leave in eleven minutes, pleads for pickup in the
# next ten, focus on how long the ongoing wait is taking -> impatience.
C("s13", "Which label should QA record for the customer's primary emotion?",
"""
Harrowgate QA — client: Brightfold Bank · callback notes + customer message · ref BF-Q-2291
Queue context: mortgage servicing line, Tuesday afternoon; average wait that day 38 minutes. The QA reviewer reads the customer's own words and the agent's note together.

Customer message left in the queue app while on hold (minute 34):
"Still here. I've now counted every tile on the kitchen ceiling. Twice. There are 48, one is cracked. Not upset, not in any hurry — I've taken the whole day off to sort the mortgage paperwork and there's nothing else on. It's just mind-numbingly dull listening to the same flute loop. If someone picks up at any point today, that's fine."

Agent note on callback (minute 41): customer calm; completed the mortgage address change without issue.
""",
o("impatience", "frustration", "anger", "amusement", "sadness", "confusion", "anxiety", "contempt", "satisfaction", "none of these"),
"none of these", 3,
twin=T([("Not upset, not in any hurry — I've taken the whole day off to sort the mortgage paperwork and there's nothing else on.",
         "I have to leave for the school pickup in eleven minutes and every minute of this is eating into that."),
        ("It's just mind-numbingly dull listening to the same flute loop.", "Same flute loop. Again."),
        ("If someone picks up at any point today, that's fine.", "Can someone PLEASE pick up in the next ten minutes?"),
        ("customer calm;", "customer in a hurry;")],
       "impatience")),

# ------------------------------------------------------------------ s14
# why: whose emotion. The caller says she has done her crying and is practical; it is her son who
# cannot open post or face the house -> caller herself: no. Twin asks about the son -> grief: yes.
Y("s14", "Is the caller herself primarily expressing grief in this call?",
"""
Harrowgate QA — client: Tallis Energy · bereavement line · ref TE-B-1182

Caller (Mrs Petra Laine):
"Hello, yes. My husband Aurelio died on the 2nd of this month and the account is in his name. I need it moved to mine and a final bill for his part. I should say — I'm fine, honestly. He was ill for a long time, we had time to prepare, and I've done my crying. It's my son, Mateo, who's taking it hard. He can't open any post with his dad's name on it, he just leaves it on the stairs, and yesterday he sat in the car outside for an hour because he couldn't face the house. So if you could address everything to me, not 'the family', that would help him. Right — the account number is 4471-209."

Agent note: caller composed and practical throughout; account transferred; bereavement flag set.
""",
card("grief", "sadness"),
0, 3,
twin=T([], 1, instructions="According to the caller, is her son Mateo primarily experiencing grief?")),

# ------------------------------------------------------------------ s15
# why: he built the cabin himself, first build, neighbours ask who he hired ("Nobody!") ->
# pleasure in own achievement -> pride. Twin: the store's fitter stayed unpaid to finish it,
# "because of him", "make sure he hears this" -> gratitude.
C("s15", "Following the tagging rule, which emotion best describes this writer?",
"""
Harrowgate QA — client: Cobbett & Lane DIY · email (feedback inbox) · ref CL-F-7810

From: Nnamdi Oyelaran
Subject: The Alder garden cabin!!

Hi Cobbett & Lane,
Just had to write. I built the whole Alder 3x4 garden cabin myself from your kit over four weekends — the first thing I've ever built bigger than a bookshelf. Base, frame, roof felt, the lot, and it's level to the millimetre. My neighbours keep coming round to look and asking who I hired. Nobody! Photos attached: the frame going up, the finished roof, and me with a mug of tea in the doorway. Might do a shed next.
All the best,
Nnamdi

Tagging rule: tag the writer's primary emotion; where praise is involved, ask whose achievement or help the writer is focused on.
""",
o("pride", "gratitude", "satisfaction", "amusement", "relief", "hope", "confusion", "none of these"),
"pride", 2,
twin=T([("I built the whole Alder 3x4 garden cabin myself from your kit over four weekends — the first thing I've ever built bigger than a bookshelf. Base, frame, roof felt, the lot, and it's level to the millimetre. My neighbours keep coming round to look and asking who I hired. Nobody!",
         "Your fitter, Marek, stayed three hours past the end of his shift on Saturday to finish our Alder 3x4 garden cabin before the rain came, and wouldn't take a penny extra. My mum can use it as her painting room from tomorrow because of him."),
        ("Might do a shed next.", "Please make sure he hears this.")],
       "gratitude")),

# ------------------------------------------------------------------ s16
# why: her dog died; lead by the door, quiet house, "no one left to insure" -> grief. The thanks
# for the claim is a side remark; sadness is less specific than grief here.
C("s16", "Which emotion does the guide assign to this customer's message?",
"""
Harrowgate QA — client: Pawsure Pet Insurance · claim email · ref PS-C-44102

From: Oona Barraclough
Subject: Claim 44102 — Biscuit

Hello,
I've received the settlement for Biscuit's last vet bill, thank you. You've all been kind and quick and I have no complaints about the claim at all.
Biscuit was put to sleep on Tuesday. She was fourteen, and she'd slept on the end of my bed every night since she was a puppy. I keep seeing her lead on the hook by the door and I can't bring myself to take it down. The house is so quiet. I'm writing mainly to cancel the policy — there's no one left to insure.
Oona
""",
o("grief", "sadness", "gratitude", "satisfaction", "guilt", "disappointment", "anger", "anxiety", "regret", "none of these"),
"grief", 2),

# ------------------------------------------------------------------ s17
# why: same words "Brilliant. Just brilliant." After a full fix and credit applied, customer says
# everything she needed is done, no thanks to anyone -> satisfaction. Twin: repair slot moved
# again to 14 days out -> blocked goal, no accusation -> frustration.
C("s17", "What is the customer's primary emotion, reading her words in context?",
"""
Harrowgate QA — client: Orrin Broadband · live chat · ref OB-C-51450

Agent (Faisal): Thanks for waiting, Ms Kowalczyk. I've checked the line: the fault was at the street cabinet, not your house. The repair crew finished there twenty minutes ago, your speed test now shows 150 Mbps, and I've applied the service credit for the outage days to your next bill automatically.
Customer (Ms Irena Kowalczyk): Brilliant. Just brilliant.
Customer: That's everything I needed — it's working in every room and the credit is right. I'll close the chat now.
Agent: Glad to hear it. Anything else?
Customer: No, all sorted.

Coding note: identical words can carry different emotions; tag by what the customer means in context.
""",
o("satisfaction", "frustration", "gratitude", "anger", "amusement", "contempt", "disappointment", "confusion", "none of these"),
"satisfaction", 2,
twin=T([("the fault was at the street cabinet, not your house. The repair crew finished there twenty minutes ago, your speed test now shows 150 Mbps, and I've applied the service credit for the outage days to your next bill automatically.",
         "the fault is at the street cabinet. The repair slot has been moved again — the earliest crew is now fourteen days out, and the credit can't be applied until the fault is fixed."),
        ("That's everything I needed — it's working in every room and the credit is right. I'll close the chat now.",
         "Fourteen more days of working off my phone's hotspot. That's the third time the slot has moved. I'll close the chat now."),
        ("Glad to hear it. Anything else?", "I'm sorry. Anything else?"),
        ("No, all sorted.", "No. There's nothing else you can do, clearly.")],
       "frustration")),
]
