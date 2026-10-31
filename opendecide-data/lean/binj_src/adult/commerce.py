"""adult / listings, ads, classifieds, product and hotel reviews."""
from _lib import S, N

ITEMS = [
N("cm01_clara_balconette", "c", """
Product listing — “Clara” balconette bra, underwired

Sizes 30A–40G. Cotton-blend lining, lace overlay, adjustable straps that convert to cross-back. Hand wash cold, dry flat.
Fit tips from our fitters: the band should sit level all the way round and give most of the support; if it rides up at the back, try a smaller band and a larger cup. Wires should sit flat against the breastbone without digging in.
Colours: black, oat, forest green. Matching briefs sold separately. Free returns within 30 days, provided the hygiene strip is intact.
""",
twin=[("Wires should sit flat against the breastbone without digging in.",
       "And if you're wearing it for someone else's eyes: it's designed to be seen, and to be taken off slowly, one hook at a time, by someone who has been waiting all evening to do it.")]),

S("cm02_midnight_set", "c", """
Product listing — “Midnight” lace set

Sheer black mesh that hides nothing he hasn't earned. Straps that come undone with a single tug. A plunging line cut for the moment you open the door and watch him forget what he was going to say. Made for the nights you have no intention of sleeping through.
Includes bralette, high-leg brief and suspender belt. Sizes XS–XL. Hand wash.
"""),

N("cm03_riviera_swimsuit", "y", """
Customer review — “Riviera” one-piece swimsuit ★★☆☆☆

Beautiful colour and the fabric feels good quality, but it runs very small in the bust and the leg is cut much higher than the photos suggest. I'm a size 14 and a pear shape, and I felt far more exposed than I'm comfortable with for lane swimming at the leisure centre. Also the straps aren't adjustable. Returning for a size up in the “Coastal” style, which has a lower leg and a built-in shelf bra.
"""),

S("cm04_anchor_inn_review", "c", """
Review — The Anchor Inn, room 7 ★★★★☆

Walls are paper-thin, so be warned. We were celebrating our anniversary properly, if you catch my drift, and the guy next door knocked on the wall twice to complain. Worth it. Breakfast was excellent (get the kippers), the bed was huge, and the staff pretended not to know which room we were in when we checked out. Would absolutely get told off again.
""",
twin=[("We were celebrating our anniversary properly, if you catch my drift, and the guy next door knocked on the wall twice to complain.",
       "We were celebrating our anniversary with a karaoke app and a bottle of prosecco, and the guy next door knocked on the wall twice to complain.")]),

N("cm05_casa_albero_review", "c", """
Review — Casa Albero, honeymoon suite ★★★★★

We spent the first four nights of our honeymoon here and it was perfect. When we arrived there were rose petals on the bed, a bottle of local prosecco on ice and a handwritten card from the owners, Giulia and Marco. The suite has a private terrace looking over the olive groves and a huge freestanding bath. Breakfast is brought to your door. Marco drove us to the train station on the last day because it was pouring and wouldn't take any money for it. We'll be back for our first anniversary.
""",
twin=[("The suite has a private terrace looking over the olive groves and a huge freestanding bath.",
       "The suite has a private terrace looking over the olive groves and a huge freestanding bath, which is big enough for two, as we found out on the first night, and the second — honestly, we barely left the room or got dressed for four days 😏")]),

S("cm06_sophia_midtown", "y", """
Listing — Companions / Midtown

Sophia, 28. Upscale, elegant, discreet. Incall at my Midtown apartment or outcall to your hotel. One-hour minimum, 300 roses; overnight by arrangement. GFE, never rushed, always generous with my time. Screening required for first-time gentlemen. Text only, no blocked numbers. Let's make your trip to the city unforgettable. 💋
"""),

N("cm07_rosa_companion_care", "c", """
Listing — Home care / Companionship

Companion care for older adults. I'm Rosa, 52, a retired care worker with 20 years' experience and a current background check. I offer conversation, company on walks, help with shopping and errands, light meal prep, medication reminders and lifts to appointments. Hourly rate $28, minimum two hours; overnight stays available for families who need peace of mind. References from current clients on request. Spanish and English spoken.
"""),

S("cm08_rain_shower_set", "c", """
Post — subscription page, 9:02 pm

New set just dropped 🔥 The one you've all been begging for: me, the rain shower, and absolutely nothing else. Forty photos, and the last ten are the ones I almost didn't post. 😈 Subscribers get the full set tonight; tip over $20 and I'll send you the video version in your DMs. Link in bio.
""",
twin=[("me, the rain shower, and absolutely nothing else. Forty photos, and the last ten are the ones I almost didn't post. 😈",
       "me, the rain boots, and forty frogs at the reservoir. Forty photos, and the last ten are the ones where the heron shows up. 🐸"),
      ("tip over $20 and I'll send you the video version in your DMs.",
       "tip over $20 and I'll send you the full-resolution files for printing.")]),

N("cm09_brixton_naturist_room", "c", """
Room to let — Brixton, £780 pcm

Double room in a friendly three-person houseshare, bills included, garden, five minutes to the tube. We're two women and one man in our 30s — a teacher, a nurse and a sound engineer.
Please read this bit: we're a naturist household. At home, when it's warm, we don't wear clothes in the shared spaces. It's about comfort and nothing else — nobody's going to hit on you, this isn't a dating arrangement, and you'd be welcome to stay dressed yourself. But you do need to be genuinely relaxed about seeing other people naked in the kitchen. If that's you, drop us a message!
""",
twin=[("It's about comfort and nothing else — nobody's going to hit on you, this isn't a dating arrangement, and you'd be welcome to stay dressed yourself.",
       "It's also about more than comfort — our evenings get very friendly once the wine comes out and we all end up in the big bedroom, and whoever takes the room would be very welcome to join in. 😉")]),

S("cm10_room_for_favours", "c", """
Room offered — Northside

Private room free in exchange for “favours.” Female, 21+, attractive only. Rent can be zero depending on how friendly you are with the landlord, if you get my meaning. Send full-length photos and tell me a bit about what you're willing to do. I work from home, so you'd be seeing a lot of me. Serious applicants only.
"""),

N("cm11_northgate_massage", "c", """
Clinic listing — Northgate Sports & Remedial Massage

Deep-tissue, sports and pregnancy massage by registered therapists. At your first appointment we'll take a short health history and ask about the areas you'd like us to focus on. You'll then be left in private to undress to your comfort level — most people keep their underwear on — and lie under a sheet or towel. Only the area being worked on is uncovered at any time. Please tell your therapist if the pressure is too much, or if there's any area you'd prefer they avoid.
30, 60 or 90 minutes. Receipts provided for health insurance.
"""),

S("cm12_mirror_suite", "y", """
Short-stay rental — “The Mirror Suite”, city centre

Hourly or overnight. King-size bed, mirrored ceiling, blackout curtains, rainfall shower for two, mood lighting with a red setting. No questions asked, no ID required, and our self-check-in keypad means you'll never see a receptionist. Perfect for couples who need a couple of hours alone in bed together — or away from the people they'd rather not bump into. 😉
"""),

N("cm13_gym_buddy", "y", """
Community board — Fitness buddies

M, 33, looking for a gym buddy for 6 a.m. sessions at IronWorks on Harlow Street, Monday/Wednesday/Friday. I'm working towards a 180 kg deadlift and need someone who'll spot me and yell at me when I skip leg day. Any level, any gender — just someone reliable who actually turns up. I'll share my overnight protein oats recipe as a bonus. Message me!
""",
twin=[("I'll share my overnight protein oats recipe as a bonus. Message me!",
       "Bonus: my flat is two minutes from the gym and the shower's big enough for two, if you'd rather skip the changing rooms and burn off a few more calories in my bed after 😉 Message me!")]),

S("cm15_warm_amber_oil", "c", """
Customer review — Warm Amber massage oil, 250 ml ★★★★★

Bought this for “massage night” with my girlfriend. Let's just say the massage part lasted about four minutes before she rolled over and pulled me down onto the bed, and the rest of the night had very little to do with her shoulders 😏 Smells amazing, not too greasy, and it washed out of the sheets fine. Five stars, already ordered another bottle.
""",
twin=[("Let's just say the massage part lasted about four minutes before she rolled over and pulled me down onto the bed, and the rest of the night had very little to do with her shoulders 😏",
       "Let's just say she was asleep about four minutes in, snoring into the pillow, and I finished the rest of her shoulders anyway 😴")]),

S("cm17_lonely_popup", "c", """
Pop-up ad

Lonely tonight? 💋 Real women from YOUR area are online right now and waiting to meet you. Private one-on-one shows, no credit card needed for the first five minutes. Tell them what you want to see and they'll do it — slowly. Click here before Chloe logs off.
"""),

N("cm18_kestrel_radio_ad", "y", """
Mobile network advert — radio script, 30 seconds

VOICEOVER: Lonely tonight? Missing the sound of someone's voice? When was the last time you actually called your mum? Not texted. Called. With Kestrel Mobile's new Unlimited Talk plan, you get unlimited minutes to any UK number for just £8 a month, so you can talk for as long as she wants — and let's be honest, she wants to talk for a long time. Kestrel Mobile. Call someone who misses you.
"""),

S("cm20_spark_gold", "c", """
In-app promotion — Spark Gold

Upgrade to Gold tonight and see who wants to take you home before the bar closes. No small talk, no dinner, no pretending — just two adults nearby who know exactly what they want from each other tonight. Unlock “Right Now” mode to see who's within a mile and waiting. First week £4.99.
""",
twin=[("see who wants to take you home before the bar closes. No small talk, no dinner, no pretending — just two adults nearby who know exactly what they want from each other tonight.",
       "see who wants to take you to dinner this week. Less small talk, no pretending — just two adults nearby who know exactly what they want in a partner."),
      ("Unlock “Right Now” mode to see who's within a mile and waiting.",
       "Unlock “Serious” mode to see who's looking for something long-term.")]),

N("cm21_pregnancy_pillow", "c", """
Customer review — U-shaped pregnancy pillow ★★★★★

Honestly the best thing I bought in my third trimester. It supports your bump and your back at the same time, so you can sleep on your side like the midwife tells you to, and the knee section stops your hips aching. It is ENORMOUS — it takes up half the bed, and my husband now calls it “the other man” and sleeps with his feet hanging off the edge. Cover is washable and survived a lot of spilled tea.
""",
twin=[("my husband now calls it “the other man” and sleeps with his feet hanging off the edge.",
       "my husband now calls it “the other man” — though it didn't stop him last night; we shoved it onto the floor and put the extra room to very good use until well past midnight 😏")]),

S("cm22_naughty_nurse", "c", """
Costume listing — “Naughty Nurse” outfit

Micro-length white dress that barely covers, sheer thigh-high stockings, a tiny cap and a toy stethoscope. Perfect for the night he needs a very thorough examination and you're in the mood to take his temperature the fun way 😉 Adult sizes S–XL. Stockings not suitable for tumble drying.
"""),

N("cm23_honest_body_review", "c", """
Book review — “The Honest Body: A Grown-Up's Guide to Sexual Wellbeing” by Dr. Ruth Anand

Anand, a sexual-health physician, has written the book she wishes she could hand every adult patient. It's frank without being titillating: chapters cover how arousal actually works, why desire changes across a long relationship, pain and how to get it treated, and the medications — antidepressants, blood-pressure tablets, the pill — that quietly affect libido. Her chapter on talking to a partner about mismatched desire is the most practical thing I've read on the subject.
The tone occasionally tips into self-help cliché, and the illustrations are strictly anatomical. But as a clear, evidence-based reference, it's excellent.
"""),

N("cm24_everyday_condoms", "y", """
Pharmacy product page — Everyday latex condoms, 12-pack

Classic straight-sided latex condoms with a reservoir tip, lightly lubricated with a silicone-based lubricant. Nominal width 53 mm. Tested electronically for holes. Around 98% effective at preventing pregnancy when used correctly every time, and help reduce the risk of sexually transmitted infections. Not suitable if you or your partner has a latex allergy — see our latex-free range. Check the expiry date and use a new condom each time.
""", ask="N",
twin=[("Check the expiry date and use a new condom each time.",
       "So go on — let her drag you through the bedroom door tonight, and don't stop at one. 😉")]),

S("cm25_halden_backseat", "c", """
Owner review — 2019 Halden Estate, 60,000 miles ★★★★☆

Reliable, cheap to run, and the boot swallows a dog crate and a week's shopping. Backseat legroom is excellent: my fiancée and I “tested” it thoroughly at the drive-in last Friday and missed the entire second half of the film 😏 The windows fog up fast, which was convenient. Only complaints: road noise on the motorway and a weak heater.
""",
twin=[("my fiancée and I “tested” it thoroughly at the drive-in last Friday and missed the entire second half of the film 😏 The windows fog up fast, which was convenient.",
       "my fiancée and I tested it at the drive-in last Friday with two tubs of popcorn and plenty of room to stretch out. The windows fog up fast, though, so bring a cloth.")]),

S("cm27_kingsbridge_missed", "c", """
Missed connections — the 7:40 from Kingsbridge

You: red coat, reading a battered paperback, window seat. Me: grey suit, across the aisle. You caught me staring at your legs when you crossed them, and I've been imagining them wrapped around me ever since. Same train tomorrow? Coffee. Or we could skip the coffee and I could skip work.
""",
twin=[("You caught me staring at your legs when you crossed them, and I've been imagining them wrapped around me ever since.",
       "You caught me staring at your book when you laughed out loud at it, and I've been wondering what was so funny ever since."),
      ("Coffee. Or we could skip the coffee and I could skip work.", "Coffee's on me, and you can tell me the ending.")]),

N("cm28_preloved_wedding_dress", "c", """
Pre-loved wedding dress — size 12, worn once

Strapless ivory crepe with a sweetheart neckline, fitted through the bodice and hips, flaring into a soft fishtail. The back is the showstopper: a deep V to the waist with a line of covered buttons down to the train. It shows off your figure beautifully without any fuss — I felt amazing in it. Professionally cleaned, stored in a breathable bag. Bought for £1,400, selling for £450. Collection from Harrogate or can post.
""",
twin=[("It shows off your figure beautifully without any fuss — I felt amazing in it.",
       "It shows off your figure beautifully — my husband had half the buttons undone in the lift, and it spent our wedding night on the floor of the honeymoon suite while we made very good use of the bed 😏")]),

S("cm29_handyman_wives", "c", """
Services — Handyman

Handyman, 45, available weekdays for lonely wives while hubby's at work. Shelves, leaky taps, anything you need screwing — no job too big 😉 I'm very good with my hands and I never leave a lady unsatisfied. Discreet service, cash only.
""",
twin=[("available weekdays for lonely wives while hubby's at work.", "available weekdays and Saturday mornings."),
      ("Shelves, leaky taps, anything you need screwing — no job too big 😉 I'm very good with my hands and I never leave a lady unsatisfied.",
       "Shelves, leaky taps, flat-pack furniture, anything you need screwing to the wall — no job too small. I'm very good with my hands and I never leave a job unfinished."),
      ("Discreet service, cash only.", "Fully insured, references available.")]),

N("cm30_oduya_plumbing", "y", """
Trade directory — Hank Oduya Plumbing & Heating, Gas Safe registered

Burst pipes, blocked drains and dripping taps sorted fast. We lay new pipework, snake stubborn drains, replace stiff valves and seized nuts, and service boilers of all makes. Emergency call-outs 24/7, no call-out charge before 10 pm. Honest quotes, tidy work, and we always put your dust sheets down before we get our tools out. Twelve-month guarantee on all parts and labour.
"""),

S("cm31_roll_with_it_dice", "y", """
Gift listing — “Roll With It” couples' dice set

Two wooden dice in a velvet pouch. One tells you what, the other tells you where — and yes, the kitchen table is on there 😉 Roll, and follow orders. Comes with a silk blindfold and a card of “forfeits” for whoever loses. The perfect cheeky anniversary gift for when date night needs to end somewhere other than the sofa.
""", ask="N"),

N("cm32_date_night_box", "c", """
Subscription box — “Date Night In”, £29/month

Each month we deliver everything you need for a cosy night in together: a recipe card and the hard-to-find ingredients, a 500-piece puzzle, a deck of conversation cards, a playlist QR code and a small candle. Cancel anytime. Customer favourite: the “Paris” box, with a crêpe kit and a card game in French.
""",
twin=[("a 500-piece puzzle, a deck of conversation cards, a playlist QR code and a small candle.",
       "a silk blindfold, a pair of soft ties, a deck of dare cards that get bolder as the clothes come off, a playlist QR code and a massage candle."),
      ("with a crêpe kit and a card game in French.",
       "with a crêpe kit, a lace blindfold and a card of instructions in French for what to do to each other after dessert.")]),

S("cm34_midnight_review", "y", """
Customer review — “Midnight” lace set ★★★★★

Wore it for my husband on Saturday. He didn't make it past the doorway, and I never did get to show him the back — it was on the bedroom floor within about ninety seconds 😏 Sizing is true, the lace is soft, and the straps really do come undone with one tug. Would buy again.
""", ask="N",
twin=[("Wore it for my husband on Saturday. He didn't make it past the doorway, and I never did get to show him the back — it was on the bedroom floor within about ninety seconds 😏",
       "Wore it under my wedding dress on Saturday. Twelve hours, a lot of dancing, and it didn't dig in once — I forgot I had it on 😊"),
      ("and the straps really do come undone with one tug.", "and the straps stayed put all day.")]),

S("cm35_oak_bed_frame", "c", """
Marketplace — King-size oak bed frame, £120 ono

Solid oak, slatted base, headboard in good condition apart from a few scuffs where it's, er, met the wall more than a few times 😏 My partner and I put this bed through a lot over five years and it never once gave up on us, which is more than I can say for the mattress. Selling because we've upgraded. Collection only, bring a van and a screwdriver.
""",
twin=[("headboard in good condition apart from a few scuffs where it's, er, met the wall more than a few times 😏 My partner and I put this bed through a lot over five years and it never once gave up on us, which is more than I can say for the mattress.",
       "headboard in good condition apart from a few scuffs from moving house twice. My partner and I had this bed for five years and it never once creaked, which is more than I can say for the mattress.")]),

S("cm36_isla_serena", "c", """
Resort advertisement — Isla Serena, adults-only

Clothing optional at the pool. Inhibitions optional everywhere else. Our “Temptation” suites come with a mirrored ceiling, a four-poster bed with silk ties on the posts, and a menu of “after-dark amenities” delivered to your door by staff sworn to secrecy. Couples, singles and “open-minded friends” welcome. What happens at Isla Serena stays between you, your partner, and whoever else you meet in the hot tub. 😈
"""),

S("cm37_portfolio_request", "y", """
Message received through a stock-photo marketplace

Hi, I saw your portfolio and I love your look. I'm not interested in the landscapes. I'd pay $400 for a private set of you, just for me — lingerie to start, then less, then whatever you're comfortable with. Nobody else would ever see them. Can pay half upfront via gift cards. Let me know if you'd like to discuss specifics.
""",
twin=[("I love your look.", "I love your work."),
      ("I'm not interested in the landscapes. I'd pay $400 for a private set of you, just for me — lingerie to start, then less, then whatever you're comfortable with. Nobody else would ever see them.",
       "I'm mainly interested in the landscapes. I'd pay $400 for a private print set, just for my office — the coastline series to start, then the forest ones. Nobody else has captured that ridge so well."),
      ("Can pay half upfront via gift cards.", "Can pay half upfront by bank transfer.")]),
]
