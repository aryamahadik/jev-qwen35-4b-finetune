"""Affect hard items, batch yn: yes/no questions for emotion presence, stance labels and intent routing."""
from common import YE, YS, YI, T

RULE = ("Annotation rule: a message can carry more than one emotion. Answer yes if the named emotion is expressed "
        "anywhere in the message by the person asked about, as defined; emotions that are only imagined, predicted, "
        "or attributed to other people do not count.")
VET = ("Brightpaw Veterinary - routing policy: route each message to the one intent that matches what the client "
       "needs from the clinic now. Anything that needs a vet today goes to urgent care.")
POLICY = ("Routing policy: assign the one intent that matches what the customer is asking us to do in this message. "
          "Background details and features merely mentioned do not decide the intent.")

ITEMS = [
# YE1 "terrified" about an interview -> not fear (no danger) -> 0
YE("yn_interview_terrified",
RULE + """

Message in a careers forum, posted by jonah_b, Sunday 23:10

Final-round interview at Harlow & Pike tomorrow at 9. Panel of four, including the managing partner, and a 20-minute presentation on a case they only sent me this afternoon. I am absolutely terrified. I've rehearsed the presentation six times and I still lose my thread on slide 4 every single time. I keep imagining freezing in front of them and just standing there in silence. I know I should sleep but I'm lying here running the opening lines over and over. Any last-minute tips for keeping it together on the day?""",
"fear", 0, 2, extra=["nervousness"]),

# YE2 sarcastic thanks -> not gratitude -> 0
YE("yn_sarcastic_thanks",
RULE + """

Review left on the Parcelwise app, 1 star, by user m_okafor

Thanks SO much, Parcelwise, for leaving my new laptop on the front step in the pouring rain, in a cardboard box, with the "safe place" photo helpfully showing the puddle it was sitting in. Really appreciate the thought. The safe place on my account is the locked porch, which you'd know if you'd read the delivery notes. The box was soaked through when I got home at six. Luckily the laptop was in a plastic sleeve, no thanks to you. Great service as always.""",
"gratitude", 0, 1, extra=["annoyance", "anger"]),

# YE3 condolence "sorry" -> not remorse -> 0; twin adds own failing -> 1
YE("yn_condolence_sorry",
RULE + """

Card sent to Ruth Adeyemi by her former colleague Martin Hale

Dear Ruth,

I was so sorry to hear about your father. I only met him the once, at your fortieth, but I remember him telling me the whole history of the canal lock by the pub, and how proud he was of you and the boys.

I hope the funeral on Friday goes as well as these things can. If there's anything at all I can do in the next few weeks, walking Bramble, bringing round a meal, anything, please just ask.

Thinking of you all,
Martin""",
"remorse", 0, 2, extra=["sadness", "caring"],
twin=T([("I hope the funeral on Friday goes as well as these things can.",
         "I'm so ashamed that I missed the funeral on Friday after promising you I'd be there; I let you down when you needed people, and I'm truly sorry.")],
       1)),

# YE4 parent about child's achievement -> pride -> 1; twin neighbour's child -> 0
YE("yn_son_apprenticeship",
RULE + """

Post in the Millbrook Parents group by Colm Fitzgerald

Can I have a little moment here. Our son Daniel got the letter today: he's been accepted onto the Harland Aerospace engineering apprenticeship, one of twelve places out of over nine hundred applicants. Two years ago he was nearly excluded and could barely be persuaded to get out of bed. He turned it round himself, re-sat his maths at the college in the evenings and built the drone for his portfolio in the shed.

I'm not usually one for posting this kind of thing, but I've read that letter about fifteen times tonight.""",
"pride", 1, 2, extra=["admiration", "joy"],
twin=T([("Our son Daniel got the letter today:", "Our neighbours' son Daniel, whom I only know to say hello to, got the letter today:"),
        ("I've read that letter about fifteen times tonight.", "His mum showed me the letter over the fence this evening.")], 0)),

# YE5 hypothetical relief -> 0
YE("yn_hypothetical_relief",
RULE + """

Text from Grace to her brother Luka, Wednesday 16:02

Scan's done. They said the results go to my consultant and he'll phone by Monday, which means a whole weekend of waiting. If it comes back clear I'll be so relieved I'll probably cry in the car park. If it doesn't, well, we'll deal with it. Can you still do Saturday lunch? I'd rather be out of the house than sitting by the phone. Mum doesn't know I had it today, so please don't mention it on the call tonight.""",
"relief", 0, 2, extra=["nervousness", "optimism"]),

# YE6 disappointment without the word -> 1
YE("yn_bonus_half",
RULE + """

Direct message from Wren to her friend Ilse, Thursday 18:45

Bonus letters came out today. Mine is £2,100. In March my manager sat me down after the Castleford launch and told me to expect "at least double last year", which would have been about £4,500, and I'd been counting on that for the deposit on the flat on Rowan Street. I'd even measured the windows for curtains. So that's the flat gone, at least for this year. I'm not angry with anyone, it's a bad year for the company and I know that. I'd just let myself plan around it.""",
"disappointment", 1, 2, extra=["sadness", "anger"]),

# YE7 mocking "lol" -> not amusement; asked in negated form -> gold 1
YE("yn_mocking_lol",
RULE + """

Reply on the Tallow app's public feedback board, by user k_dimitrov

lol ok so the "fixed" version from last night now crashes the moment it opens. not even a login screen, just straight back to the home screen. amazing work guys lol. this is the third "critical fix" this month and every one has broken something the last one fixed. I've got a shift rota in there that I need for tomorrow morning. can someone tell me how to roll back to 4.2, or do I have to wait for you to break it in a new and exciting way""",
"amusement", 0, 2, extra=["annoyance", "disapproval"], neg=True),

# YE8 explicit calm before a test -> 0; twin shaking -> 1
YE("yn_driving_test",
RULE + """

Message from Tobi to his driving instructor, Rhiannon, Monday 21:30

Hi Rhiannon, just confirming I'll be at the test centre at 8:40 tomorrow for the 9:07 test, and I'll bring the provisional licence and the theory certificate. I've done everything I can: we've driven the whole route twice and I finally have the parallel parking sorted. Honestly I feel calm about it. Whatever happens, happens. Thanks for all the lessons, whatever the result.

Tobi""",
"nervousness", 0, 2, t="Tobi", extra=["fear", "optimism"],
twin=T([("Honestly I feel calm about it. Whatever happens, happens.",
         "Honestly my hands are shaking just typing this, and I keep picturing stalling at the first junction.")],
       1)),

# YS1 criticises dog owners, praises the park -> "against" is wrong -> 0
YS("yn_dog_park",
"""Brennan Falls Community Board - post by Delphine Achterberg

To the small number of dog owners who seem to think the poo bags at the gate are decorative: please, I beg you. I spent twenty minutes on Saturday cleaning my daughter's trainers after she ran across the grass by the benches. There's a bin at each corner of the park. It isn't hard.

That said, the park itself is the best thing the council has done in this neighbourhood for years. The double gates, the separate area for small dogs, the water fountain at dog height. We use it every day and I'd hate to see it closed because of a few people.

The friends' group meets on the first Monday of the month if you want to help.""",
"the Brennan Falls dog park", "against", 0, 2),

# YS2 favor the incinerator; asked in negated form -> gold 0
YS("yn_incinerator",
"""Letters page, Westfield Advertiser

Say what you like about the smell from the Westfield incinerator on a hot day, and I have said plenty of it over the garden fence, it has cut the landfill lorries on Stanmore Road from forty a day to six. My grandchildren can cross the road to the park again. The monitoring results published by the council every quarter have been within limits for three years running.

If the council's review ends up putting the incinerator's future to a vote, mine goes to keeping it, smell and all.

Edna Pole, Stanmore Road""",
"the Westfield incinerator", "favor", 1, 2, neg=True),

# YS3 backs the rival in a two-candidate race -> "neither" is wrong -> 0
YS("yn_ward_rival",
"""Comment under the Hollins Echo article "Ward 7: Gareth Olumide and Councillor Priya Nandakumar go head to head for one seat"

Comment by Tariq Jamal:

I've read both candidates' leaflets and been to both hustings. I'm voting for Gareth Olumide. He answered every question at the St Luke's hustings without notes and he's the only one who has actually run a budget, having chaired the food bank for six years.

I've got nothing personal against anyone. It's just that on Thursday I'll be putting my cross next to Gareth's name, and I'd encourage anyone still making up their mind to watch the hustings recording on the Echo's website.""",
"Councillor Priya Nandakumar", "neither", 0, 3),

# YS4 sarcasm -> against -> 1
YS("yn_marina_sarcasm",
"""Old Quay Residents' Association - comments on the consultation

Comment by Winifred Asante:

Wonderful news that the Old Quay marina development will bring "vibrant waterside living" to our neighbourhood. Nothing says vibrant like 240 luxury flats with a gated berth each, a car park where the fishermen's huts used to be, and a public footpath that closes at dusk "for residents' security". I'm sure the three fishing families who've been told to find somewhere else to land their catch will find it very vibrant indeed.

Consultation responses close on 30 November. Paper forms are at the library.""",
"the Old Quay marina development", "against", 1, 1),

# YS5 reports others, asks a question -> neither -> 1; twin endorses -> 0
YS("yn_self_checkout",
"""Hollins Lane Library Users (group page) - post by Bernard Asomugha

Has anyone else been in since the new self-checkout machines went in? Several of the older members at Tuesday's knitting circle were grumbling that they can't read the screens and miss chatting to the staff at the desk. My neighbour says the queues are shorter now.

I haven't used them yet myself; I've been away. Does anyone know if the staffed desk is still open on Saturday mornings, or is it machines only? I need to pick up an inter-library loan and I'm not sure if the machines can do those.""",
"the library's new self-checkout machines", "neither", 1, 2,
twin=T([("Several of the older members at Tuesday's knitting circle were grumbling that they can't read the screens and miss chatting to the staff at the desk.",
         "Several of the older members at Tuesday's knitting circle were grumbling that they can't read the screens and miss chatting to the staff at the desk, and frankly I think they're right: the machines were a mistake.")],
       0)),

# YS6 reluctant but supports -> favor -> 1
YS("yn_congestion_charge",
"""Letter to the editor, Castleford Evening News

I don't love the idea of paying £8 every time I drive into town. I'm a self-employed plumber and my van is my office, so I know exactly what that will cost me over a year.

But I've also stood on Castle Street at five o'clock with the queue backed up to the bridge and the air so thick you can taste it, and my apprentice has asthma. The proposed congestion charge is the only plan anyone has put on the table that would actually change that, and the money is ring-fenced for buses. Put it in.

Rhys Evans, Castleford""",
"the proposed congestion charge", "favor", 1, 2),

# YI1 dog ate dark chocolate just now -> urgent care -> 1; twin: tiny amount days ago -> 0
YI("yn_vet_chocolate",
VET + """

Brightpaw Veterinary - web chat (client side)
Client: Petra Lindahl | Patient: Otis, 8 kg terrier cross | Saturday 15:20

Hi, Otis has just eaten about half a 100 g bar of 70% dark chocolate that my son left on the sofa. It happened maybe twenty minutes ago. He seems completely normal at the moment, wagging and begging for more. I've read online that chocolate is bad for dogs but I don't know if that amount matters for his size. Do I need to bring him in?""",
"Brightpaw Veterinary", "urgent care", 1, 1, extra=["book appointment"],
twin=T([("Otis has just eaten about half a 100 g bar of 70% dark chocolate that my son left on the sofa. It happened maybe twenty minutes ago. He seems completely normal at the moment, wagging and begging for more. I've read online that chocolate is bad for dogs but I don't know if that amount matters for his size. Do I need to bring him in?",
         "on Wednesday Otis ate a single milk-chocolate button that my son dropped. He's been completely normal in the three days since, eating, walking, all fine. I'm not worried about him now; I'd just like to book a general check-up for him sometime next month, as he's due one anyway.")],
       0)),

# YI2 refill request -> prescription refill -> 1
YI("yn_vet_thyroid",
VET + """

Brightpaw Veterinary - email
From: Harold Birtwistle | Patient: Luna, 14-year-old domestic shorthair | Sent: Tuesday 09:02

Good morning. Luna's thyroid tablets (the 2.5 mg ones Dr Osei prescribed in June) will run out on Friday. She is doing well on them: eating, putting on weight, and back to sleeping on the radiator. Could you please send the next month's supply to the Brightpaw pharmacy counter for me to collect on Thursday afternoon? I'm also happy to pay over the phone if that's easier. Her next blood test is booked for November as planned.""",
"Brightpaw Veterinary", "prescription refill", 1, 1, extra=["lab results", "book appointment"]),

# YI3 asks for vaccination history, "results" word -> lab results is wrong -> 0
YI("yn_vet_vax_records",
VET + """

Brightpaw Veterinary - voicemail transcript, Wednesday 17:48
Caller: Samira Haddad | Patient: Pepper, spaniel

"Hi, it's Samira Haddad, Pepper's owner. Pepper's going into Oakfield Kennels for a week from the 20th, and they need proof that her vaccinations are up to date, including kennel cough. Could someone email me her full vaccination history? I know you did her blood test results last month as well, but they don't need those, just the jabs. My email's on her file. Thanks very much.\"""",
"Brightpaw Veterinary", "lab results", 0, 2, extra=["vaccination records", "boarding booking"]),

# YI4 move existing appointment -> book appointment is wrong -> 0
YI("yn_vet_move_booster",
VET + """

Brightpaw Veterinary - web form "Appointments"
Client: Declan O'Rourke | Patient: Milo, 2-year-old Labrador | Submitted: Sunday 20:15

We have an appointment on Tuesday at 3 PM for Milo's annual booster with Dr Kaur. My shift has been changed and I can't get there on Tuesday. Could we move it to Thursday, any time after 2 PM? If Thursday is full, Friday morning would also work. Milo is well; there's nothing urgent, it's just the booster.""",
"Brightpaw Veterinary", "book appointment", 0, 2, extra=["reschedule or cancel appointment"]),

# YI5 502 errors -> site down -> 1
YI("yn_sc_502",
POLICY + """

Stackhouse Cloud - support ticket
Customer: Merrow & Finch Tailoring (plan: Business) | Submitted by: Anika Rao | 10:31, Wednesday

Since 10:14 every page on merrowfinch.example returns "502 Bad Gateway", including the home page and the checkout. The admin panel won't load either. We haven't deployed anything since Monday, and the DNS and SSL settings haven't been touched; the certificate is valid until March. Our autumn collection email goes out to 18,000 subscribers at noon, so we need the site back up before then.""",
"Stackhouse Cloud", "site down", 1, 1, extra=["SSL certificate problem", "DNS or domain setup"]),

# YI6 cancelled subscription charged again -> dispute a charge -> 1
YI("yn_qcu_streamnest",
POLICY + """

Quillfeather Credit Union - secure message
Member: Ophelia Grant | Received: Monday 12:12

Hello. I cancelled my StreamNest subscription in May, and I have the cancellation confirmation email from them dated 14 May. But on 3 September they charged my Quillfeather debit card $12.99 again, and it has gone through as a completed transaction. StreamNest's support hasn't answered in two weeks. I don't need a new card and I don't want to freeze this one, I use it every day. I just want the $12.99 back.""",
"Quillfeather Credit Union", "dispute a charge", 1, 2, extra=["pending charge query", "freeze card"]),
]
