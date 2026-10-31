"""adult / social media, chats, forums, jokes, double meanings."""
from _lib import S, N

ITEMS = [
N("sc01_reservoir_birding", "c", """
Birding log — Hollow Lane reservoir, Sunday 7 am

Cold and still, good light. At the feeders by the hide: six blue tits, two great tits, a coal tit and a pair of long-tailed tits working through the fat balls. Great spotted woodpecker drumming in the alders. On the water, a pair of goldeneye, fourteen tufted duck and a single female smew — first of the winter. Two woodcock flushed from the path on the way back. Still no sign of the bittern everyone's been talking about.
""",
twin=[("Still no sign of the bittern everyone's been talking about.",
       "Still no sign of the bittern, but the woman in the next hide more than made up for it — we shared a flask, then a sleeping bag in the back of her van, and neither of us saw another bird all morning 😏")]),

N("sc02_harlow_match_report", "c", """
Club newsletter — Harlow RFC 24–17 Westbridge

Harlow's pack was dominant from the first scrum. Hooker Danny Reyes found his jumpers at every lineout, and the tighthead had his opposite number on the back foot all afternoon. The pivotal moment came on 62 minutes: Westbridge's fly-half was sin-binned for a high tackle, and from the resulting penalty Harlow kicked to the corner, mauled over and scored through Reyes at the back of the drive. Man of the match: Reyes, who also tackled everything in sight.
"""),

N("sc03_brahma_rooster", "y", """
Livestock for sale — Upper Dale, collection only

Big cock for sale. Two-year-old Light Brahma rooster, feathered feet, very handsome and very loud — crows from 4:30 a.m., which is why my neighbours have asked me to rehome him. Gentle with people, good with his hens, protective without being aggressive. Vaccinated. £25 or swap for point-of-lay pullets. Can deliver locally for fuel money.
"""),

N("sc04_stripped_screw_holes", "c", """
Woodworking forum — “Stripped screw holes in oak — help?”

I'm assembling a bed frame from rough-sawn oak, and three of the screw holes on the side rails have stripped, so the screws just spin. The shaft of the screw is fine but the thread won't bite. Do I glue in a hardwood dowel and re-drill, or go up a size? Also — pilot hole or no pilot hole for 5 mm screws in oak? I nailed the slats in by hand and now I'm worried the whole thing will be stiff and squeaky. Photos attached.
""",
twin=[("I nailed the slats in by hand and now I'm worried the whole thing will be stiff and squeaky.",
       "I need it done by Friday, because my girlfriend is moving in and she's made it very clear that the first thing we're doing in this bed is not sleeping. I'd rather it didn't collapse halfway through 😏")]),

S("sc05_carpenter_brunch", "c", """
Group chat — “Brunch Club 🥂”

Tasha: SO?? how was the date with the carpenter
Lou: let's just say he's very good with wood
Lou: and with his hands generally
Lou: I can't feel my legs and I'm going to be late to brunch 😂
Mira: LOUISE 😂😂
""",
twin=[("let's just say he's very good with wood", "let's just say he built me a bookshelf on the second date"),
      ("and with his hands generally", "and he fixed my wobbly table while I made tea"),
      ("I can't feel my legs and I'm going to be late to brunch 😂", "I can't stop smiling and I'm going to be late to brunch 😂")]),

N("sc06_mae_stomach", "c", """
Instagram caption — @mae.moves

Hi, this is my stomach. It has stretch marks from two pregnancies, a C-section scar, and a soft little pouch that no amount of crunches is going to shift. For years I wore a swimsuit with a skirt and stood behind people in photos. This summer I wore a bikini on the beach in Tenby and nobody cared, least of all me. My body has carried two pregnancies and carries me up Pen y Fan. It's allowed to look like it's lived.
#bodypositivity #postpartumbody #normalizenormalbodies
"""),

S("sc07_wetsuit_replies", "c", """
Replies to a beach photo posted by @jo.surfs

@jo.surfs: first surf of the season 🌊 water was 12 degrees, send help
@bigmike_77: your thighs in that wetsuit 🥵 I'd let you crush me any day
@bigmike_77: post more from the back, I'll be putting this one to good use tonight 😏
@jo.surfs: blocked
"""),

N("sc08_glute_progress", "c", """
Reddit — r/fitness progress post

F/31/5'6" — 16 weeks of glute-focused training. Starting hip thrust: 60 kg for 8. Today: 140 kg for 8. Hip measurement went from 98 cm to 104 cm while my waist stayed the same, so it's muscle, not just food (though there was also a lot of food).
Routine: hip thrusts and RDLs twice a week, Bulgarian split squats, cable kickbacks, lots of walking. 130 g protein a day. The biggest change isn't the photos, honestly — it's that my lower back pain from sitting at a desk is gone.
"""),

S("sc09_discord_voice", "c", """
Discord DM — 1:07 am

kai: gg, you carried that last round
rhea: lol you were fine
kai: ngl your voice on comms has been doing things to me all night
kai: hop off the game and call me from bed? I want to hear what else that voice can do 😏
rhea: ...give me five minutes
""",
twin=[("ngl your voice on comms has been doing things to me all night", "ngl your callouts on comms have been carrying us all night"),
      ("hop off the game and call me from bed? I want to hear what else that voice can do 😏",
       "hop in voice tomorrow for the raid? I want to see what else that sniper build can do 🎯"),
      ("...give me five minutes", "...ok, 8 pm?")]),

N("sc11_sandbar_notice", "y", """
Beach notice — Sandbar Bay, naturist section

The area between the two blue posts is designated for naturist use from May to September. Visitors outside this area should remain clothed.
Please respect other beach users: photography of other people is prohibited, and any lewd behaviour or harassment will be reported to the rangers. Keep a respectful distance from other bathers. Use sunscreen generously — people burn in places they don't expect. The dunes are a protected habitat; please stay on marked paths.
Lifeguard cover 10 am–6 pm. Toilets and showers at the north car park.
"""),

S("sc12_dunes_meetup", "c", """
Forum — Naturist meetups / South Coast

Anyone heading to the naturist end at Sandbar Bay on Saturday? A few of us are planning to “meet up” in the dunes once the lifeguards knock off and the beach empties out 😉 Couples and single ladies especially welcome. Bring a blanket and an open mind — what happens behind the dunes stays behind the dunes. DM for the exact spot, discretion assured.
""",
twin=[("A few of us are planning to “meet up” in the dunes once the lifeguards knock off and the beach empties out 😉 Couples and single ladies especially welcome. Bring a blanket and an open mind — what happens behind the dunes stays behind the dunes. DM for the exact spot, discretion assured.",
       "A few of us are planning a litter pick along the dunes once the lifeguards knock off and the beach empties out. Everyone welcome, clothed or not. Bring gloves and a bin bag — the storm left the tideline in a state. DM for the meeting point.")]),

N("sc13_number14_chat", "c", """
Flat group chat — “Number 14 🏠”

Priya: whoever was up at 2 am last night, what WAS that noise
Josh: sorry that was me, I was assembling the new wardrobe
Josh: the instructions were in Swedish and I lost a fight with a hinge
Priya: at 2 am??
Josh: couldn't sleep. it's done now at least. I'll buy earplugs for everyone
""",
twin=[("sorry that was me, I was assembling the new wardrobe", "sorry that was me, Dan came back with me after the pub"),
      ("the instructions were in Swedish and I lost a fight with a hinge",
       "and we, uh, didn't do much sleeping 😳 the headboard lost a fight with the wall"),
      ("couldn't sleep. it's done now at least. I'll buy earplugs for everyone",
       "he's staying over again tonight. I'll buy earplugs for everyone")]),

S("sc14_northern_line_blouse", "c", """
Post by @anon_commuter

Just saw the most beautiful woman on the Northern line. Silk blouse clinging in all the right places, top button undone, and every time the train lurched she had to grab the pole right next to me. I missed my stop on purpose. I've been picturing that blouse on my bedroom floor all afternoon. If you were in carriage 3 at 8:15, find me. 😏
"""),

N("sc15_neruda_commuter", "c", """
Post by @bookish_bea

The cutest man on the 8:15 was reading Neruda with a pencil behind his ear, underlining things and mouthing the words. I missed my stop pretending to read over his shoulder. He caught me and just tilted the book so I could see better. We didn't say a word. I'm going to be on the 8:15 every day until I die.
""",
twin=[("We didn't say a word. I'm going to be on the 8:15 every day until I die.",
       "We didn't say a word. He got off at my stop, I took him home, and neither of us made it to work — the Neruda ended up somewhere under my bed. 😏")]),

N("sc16_coming_out_bi", "y", """
Facebook post

I've written and deleted this a dozen times, so here goes. I'm bi. I've known for a long time, and I've been out to close friends for a couple of years, but I'm tired of editing myself around everyone else. Yes, I'm still with Callum; no, nothing's changed between us; he's known since our second date and he's the one who told me to stop hiding. If you have questions, ask me kindly. If you have opinions, keep them. Love you all. 🏳️‍🌈
""", ask="N"),

S("sc17_room_402", "y", """
Messages — Friday 10:51 pm

Marcus: Hotel Aster, room 402. Door's on the latch.
Marcus: Lights are off. Don't say anything when you come in.
Marcus: Just find me in the dark and take your time. I've been thinking about you all week.
Leo: Parking now.
""",
twin=[("Lights are off. Don't say anything when you come in.",
       "Lights are off. Don't say anything when you come in — Dev's flight lands at eleven and we're all hiding behind the curtains."),
      ("Just find me in the dark and take your time. I've been thinking about you all week.",
       "Just find us in the dark and grab a party popper. I've been planning this surprise all week.")]),

N("sc19_maid_of_honour_confession", "y", """
Anonymous confession — r/TrueOffMyChest

I slept with my best friend's ex last year, about two months after they broke up. It happened once, we both regretted it, and we agreed never to tell her. Now she's getting married and she's asked me to be her maid of honour, and every time she hugs me I feel sick. I don't know if telling her would be honest or just selfish — making myself feel better by wrecking her happiness. What would you want, if you were her?
""",
twin=[("It happened once, we both regretted it, and we agreed never to tell her.",
       "I still think about that night — his hands in my hair, the way he pinned me against his kitchen counter before we'd even said hello, the whole slow, breathless night that followed. We agreed never to tell her.")]),

S("sc20_scorpio_venus", "y", """
Weekly horoscope — Scorpio (Oct 23 – Nov 21)

With Venus parked in your eighth house, the bedroom is your playground this week. Someone who's been watching you across a crowded room wants to find out if your reputation is deserved — and you should let them. Thursday night is especially charged: lock the door, turn your phone off, and don't plan on getting much sleep. Lucky colour: red lace.
"""),

N("sc21_minister_resigns", "y", """
News — Deputy minister resigns over affair with aide

Deputy Transport Minister Graham Holt resigned on Tuesday after a newspaper reported that he had had an affair with a member of his parliamentary staff while overseeing a contract she had lobbied on. Holt, who is married, said in a statement that he had “fallen short of the standards expected” and apologised to his family. The ethics commissioner has opened an inquiry into whether the relationship should have been declared. Opposition MPs called for the contract to be paused pending the investigation.
"""),

S("sc22_paprika_joke", "c", """
Post by @dadjokesdaily

My wife said she wanted to “spice things up in the bedroom,” so I brought the paprika. She was not amused. Eventually she explained what she meant, and let's just say I'm a fast learner — we didn't come out until Sunday lunchtime and the neighbours have stopped making eye contact. 😏
""",
twin=[("Eventually she explained what she meant, and let's just say I'm a fast learner — we didn't come out until Sunday lunchtime and the neighbours have stopped making eye contact. 😏",
       "Eventually she explained she meant repainting it. We did it in terracotta. The neighbours helped pick the colour and now want theirs done too. 🎨")]),

N("sc23_scorpio_mars", "c", """
Weekly horoscope — Scorpio (Oct 23 – Nov 21)

With Mars charging through your tenth house, passion is running high this week — channel it into the project you've been circling for months. Someone senior has been watching your work more closely than you realise. Thursday is ideal for a bold pitch; Saturday, for switching your phone off and letting someone cook for you. Lucky colour: deep red.
""",
twin=[("Saturday, for switching your phone off and letting someone cook for you.",
       "Saturday, for switching your phone off, locking the bedroom door and letting someone keep you up all night — and not with conversation.")]),

S("sc24_hotel_bar_roleplay", "y", """
Reddit — r/confessions

My husband and I tried role-play for the first time on our anniversary. He sat at the hotel bar pretending to be a stranger, bought me a drink and “picked me up.” I have never felt so nervous and so ridiculous. We got a room upstairs, and let's just say he wasn't a stranger for very long 😉 We've been married eleven years and it felt like the first night all over again.
""", ask="N"),

S("sc26_mulholland_text", "c", """
Text from an unknown number, Tuesday 9:14 pm

It's Nico. I know it's been a while. I still think about that night in your car up on Mulholland — you know which one, the windows all steamed up and your seat reclined as far as it would go. I'm in LA on Friday. I'd like a repeat. Same spot, same car if you've still got it.
""",
twin=[("that night in your car up on Mulholland — you know which one, the windows all steamed up and your seat reclined as far as it would go.",
       "that night your car broke down up on Mulholland — you know which one, the radiator steaming and the two of us pushing it half a mile in the dark."),
      ("I'd like a repeat. Same spot, same car if you've still got it.",
       "I'd like to finally return your jumper cables. Same spot? Kidding. Coffee?")]),

S("sc27_team_lead_dm", "c", """
Slack DM — from your team lead, 5:48 pm

Great job on the client call today. That dress on camera though… 😍 You should definitely wear it to the offsite next week. I'd pay good money for a private presentation in my hotel room afterwards, just you, me and the minibar 😉 Let me know.
""",
twin=[("That dress on camera though… 😍 You should definitely wear it to the offsite next week. I'd pay good money for a private presentation in my hotel room afterwards, just you, me and the minibar 😉 Let me know.",
       "The client asked for the deck you shared, so please send it over. You should definitely present it again at the offsite next week — I'll book the big room. Let me know.")]),

N("sc28_council_chat", "c", """
Group chat — “The Council 👑”

Amara: he texted “had fun last night” and nothing else. what do I say
Jules: say “me too!” and nothing else
Priy: no, ask him to the thing on Saturday, be bold
Jules: she JUST saw him
Amara: we only kissed goodbye, I don't want to seem intense
Priy: we are grown women, just ask him
Amara: fine. sending “me too! are you around this weekend?”
Jules: perfect. now put the phone down
""",
twin=[("we only kissed goodbye, I don't want to seem intense",
       "we didn't exactly get round to kissing goodbye, we got round to his bedroom and I left at 6 am 😳 I don't want to seem intense")]),

S("sc29_two_truths_reply", "c", """
Reply on a dating-app prompt — “Two truths and a lie”

Prompt (Carys, 30): I've been to Iceland; I can juggle; I've never been kissed on a first date.
Reply from Dom (32): The third one's the lie, and I'd love to make it a lie again. Actually, forget the first date — tell me when your flatmate's out and I'll come over and keep you up until sunrise, and we won't be juggling 😏
"""),

S("sc30_crete_notes", "c", """
Personal blog — “Notes from Crete, day 4”

I wasn't planning to write about him, but here we are. Every morning at ten the man from the next villa walks down to the water, and every morning I happen to be on my balcony with my coffee. Oil gleaming across his shoulders, wet trunks clinging to everything, water running down the curve of his back as he walks out of the surf in what I swear is slow motion. I've started imagining exactly how he'd look sprawled across my sheets instead. My husband thinks I've taken up birdwatching.
"""),

S("sc31_pasta_comments", "y", """
Comments on a pasta-making video

@chef.marco.cucina: Today: fresh pappardelle, rolled by hand 🍝
@hungry_hank: watching those forearms knead the dough for ten minutes straight did things to me I can't explain
@hungry_hank: come knead me instead, I'll make it worth your while 😏 bring the flour, we won't be needing aprons, or anything else
"""),

S("sc32_dog_at_sisters", "c", """
Text messages — Wednesday 3:30 pm

Ruth: my sister's got the dog till Sunday
Ruth: the house is ours. all of it
Ruth: I'm thinking the sofa, then the shower, then maybe we'll make it to the bed eventually
Ruth: don't eat a big lunch 😘
Dan: leaving work early. like, now
"""),

S("sc33_rent_help_dm", "c", """
Instagram message request

Hey beautiful. Saw your post about the rent going up 😔 I'm a generous man and I like to help. $1,500 a month, and all I'd ask is two evenings a week at my apartment, you in something nice for me, and no questions about where the evening goes from there 😉 Think about it.
"""),

S("sc34_copy_room", "y", """
Short story — “The Christmas Party”, excerpt

By eleven the office party had thinned to a few stragglers singing in the kitchen. Hannah found him in the dark copy room, tie loose, pretending to look for his coat. She shut the door behind her with her heel. “Your coat isn't in here,” she said. “I know,” he said. The photocopier's standby light blinked green, and then neither of them was paying any attention to it, or to the singing, or to the buttons of his shirt, or to the fact that anyone might need the copy room at all.
""", ask="N"),

S("sc35_leeds_visit", "c", """
Forum — Men for men / Leeds

Visiting for work, staying near the station till Thursday. 41, fit, bearded, discreet. Looking to meet a guy tonight or tomorrow for something physical, no strings — hotel room's all ours, door will be unlocked, and I'll have the lights low. Tell me what you're into and send a face pic.
"""),

S("sc36_festival_tent", "y", """
Post by @outdoorsy_olivia

PSA: if you're going to share a two-person tent with your boyfriend at a festival, maybe don't pitch it three feet from his parents' camper van. We tried to be very quiet. We were not quiet enough. His mum made pointed comments about “the wind” at breakfast, and his dad hasn't looked me in the eye since Saturday. 🏕️😳
""", ask="N"),

S("sc37_private_story", "c", """
Snapchat story text — from @velvetvee

Adding people to my private story tonight 🔥 It's where I post what I can't post here — the mirror selfies after I get out of the bath, the angles Instagram would ban me for. $15 gets you added for a month. Reply “IN” and I'll send the payment link. 😘
"""),

S("sc38_reunion_dare", "c", """
Group chat — “Ten-year reunion weekend 🍷”

Zara: ok truth or dare, Ollie, you're up
Ollie: dare obviously
Zara: go knock on Freya's cabin door, and don't come back till morning 😏
Ollie: say less
Freya: door's already unlocked and I'm already in bed 😇
Kit: I'm moving to the other cabin
"""),

S("sc39_roleplay_prompt", "c", """
Message to a roleplay chatbot

Let's do a scenario. You're my new neighbour, you've locked yourself out wearing just a towel, and you knock on my door asking to wait inside until the locksmith comes. Describe how you slowly make it obvious that you don't actually want the locksmith to come. Keep it flirty, let the towel slip, and build up to us ending up in my bedroom.
"""),

S("sc40_solaris_hot_tub", "c", """
Travel forum — “Anyone else been to Club Solaris in Ayia Napa?”

Went last week with the lads. Food was average, pool was great, but the real reason to go is the hot tub after midnight. Second night, two women from Manchester on a hen do joined us, the bikinis came off within about twenty minutes, and I'll leave the rest to your imagination except to say none of us got much sleep and security had to ask us to “keep it down” twice. 10/10 would go back.
"""),

S("sc41_grey_dress_email", "c", """
Email — subject: “Thursday”

I can't concentrate. I keep thinking about the way you looked in that grey dress at the conference dinner, and how long it took me to get you out of it afterwards. I've booked the same room for Thursday. Tell him you're working late. Wear the grey dress again — I'd like to take my time with the zip this time.
"""),

S("sc42_language_exchange", "c", """
Language exchange app — chat

Matteo: your English is already perfect, you don't need me 😄
Camille: haha thank you, your French too
Matteo: I think we should practise in person. my apartment, Friday, a bottle of wine
Matteo: we can skip the grammar and go straight to the body language 😏 I'll teach you some words they don't put in textbooks, whispered, in bed
"""),

S("sc43_gilded_cage_review", "c", """
Review — The Gilded Cage, Las Vegas ★★★★☆

Came here for my brother's bachelor party. Drinks overpriced, bouncers friendly. The main stage show is the reason to go: Scarlett's routine on the pole had the whole room silent, and by the end of her last song there wasn't much left of her costume except the heels. The private dances in the back rooms are worth every dollar, if you know what I mean. Dress code enforced, no sneakers.
"""),
]
