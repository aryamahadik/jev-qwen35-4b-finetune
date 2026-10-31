"""adult / dating, relationships, romance, propositions."""
from _lib import S, N

ITEMS = [
N("dt01_theo_profile", "c", """
Profile — Theo, 36, Leeds

About me: Recovering lawyer, current sourdough obsessive. I will ask about your dog before I ask your name. Sunday mornings are for the market on Kirkgate and an embarrassing amount of coffee, and I'm trying to learn the cello, badly, much to my neighbours' despair.
Looking for: Someone who laughs at their own jokes and will split a dessert with me.
Deal-breakers: Rudeness to waiters. Pineapple on pizza is negotiable.
Prompt — “My ideal first date”: A walk along the canal, then chips, then an argument about which Bond film is best.
""",
twin=[("Looking for: Someone who laughs at their own jokes and will split a dessert with me.",
       "Looking for: Someone who'd rather skip dessert and come straight back to my bed. No strings, no breakfast, and I'll call you a cab at dawn.")]),

S("dt02_rae_flatmate", "c", """
Match chat — Rae (34) → you

Rae: Hey you. Loved the photo from the lake, by the way — very outdoorsy of you.
Rae: So. My flatmate's away at her sister's until Sunday, which means the flat is very quiet and very empty.
Rae: Come round Friday after nine. Don't bother bringing wine, and don't plan on getting much sleep. 😏
Rae: Door code is 4471. I'll leave the hall light on.
""",
twin=[("which means the flat is very quiet and very empty", "which means I finally have the living room and the good speakers to myself"),
      ("Don't bother bringing wine, and don't plan on getting much sleep. 😏", "Bring wine and your worst board game, and prepare to lose. 😄")]),

N("dt03_slow_lane_column", "c", """
Ask Marguerite

Dear Marguerite,
I'm 41, divorced for three years, and back on the dating apps after a long break. I met a man — I'll call him R. — and we've been on four dates. He's kind, funny, and he kissed me goodnight after the second date, which was lovely. But on our last date he mentioned that he'd like to take things further physically soon, and I froze. I like him. I'm just not ready, and I don't know if I'll be ready in a month or in six. I'm worried that if I say that, he'll lose interest, and I'm also worried that I'm “too old” to be this nervous. How do I tell him without making it a whole thing?
— Slow Lane in Sheffield

Dear Slow Lane,
First: there is no age at which nerves expire. Second: the pace at which you become intimate with someone is a decision two people make together, and “not yet” is a complete sentence. You don't owe him a date on the calendar.
Say it plainly and warmly, preferably not over text: “I really like spending time with you, and I want to keep seeing you. I'm not ready to take things further physically yet, and I'd rather go slowly.” Then watch what he does with that information. A man worth your Friday nights will say something like “Thanks for telling me” and ask where you'd like to go next week. A man who sulks, bargains or disappears has told you something useful, and quickly.
You might also ask yourself what “ready” would feel like. Sometimes it's about trust; sometimes it's about the divorce and the version of you who was married. A few sessions with a counsellor can help untangle that — not because anything is wrong with you, but because three years is not very long.
— M.
"""),

S("dt04_rain_key", "y", """
Excerpt — chapter eleven of an unpublished novel

The rain hadn't let up by the time they reached her building. Lena fumbled the key twice, laughing at herself, and Marcus finally took it out of her hand and opened the door. Inside, neither of them reached for the light switch.
His jacket hit the floor first. Her dress followed somewhere between the hallway and the bedroom, and she stopped caring where. He said her name once, low, like a question, and she answered by pulling him down with her.
By the time the storm finally broke, a little after three, they had long since stopped keeping track of whose shirt was whose, and the only sound in the flat was the two of them catching their breath.
"""),

N("dt05_ferry_pier", "y", """
Excerpt — from a short story in a regional literary magazine

The ferry was forty minutes late, and by the time it came in, the café on the pier had stopped pretending to be open. Hana sat on the sea wall with her coat pulled around her knees. Tomas sat down next to her, not quite touching, and offered her half of the pastry he had been saving for the crossing.
They talked about her father's shop, which she was going to have to sell, and about the brother he hadn't spoken to in four years. When the lights of the ferry finally appeared out on the grey water, he took her hand and held it the way you hold something you have been told is fragile.
On the ramp, before they went their separate ways to the upper and lower decks, he kissed her once, carefully, as if asking a question. She answered by kissing him back, and then she laughed, and went up the stairs without looking round.
""",
twin=[("On the ramp, before they went their separate ways to the upper and lower decks, he kissed her once, carefully, as if asking a question. She answered by kissing him back, and then she laughed, and went up the stairs without looking round.",
       "They didn't take separate decks. He had a cabin booked, and when the door shut behind them she was already tugging his coat off his shoulders; neither of them came up for air, or for the view, until the ferry bumped the far harbour at dawn.")]),

S("dt06_ribbons_text", "c", """
Text messages, Thursday 4:52 pm

Jordan: meeting finally over. how's your day
Sam: long. but better now
Jordan: wear the thing I bought you tonight. the black one with the ribbons at the back
Jordan: I'll be home at seven and I'm not hungry for dinner
Sam: I'll leave the bedroom door open then 😇
"""),

N("dt07_maid_of_honour", "c", """
Maid of honour speech, draft 3

For those who don't know me, I'm Anika, Priya's sister, and I have known the bride for thirty-one years, which means I have a lot of material and a strict instruction from our mother to use none of it.
When Priya first brought Jonah home, Dad sat him down on the sofa and made him listen to four hours of cricket stories. He didn't leave. He asked for more. That's when I knew.
Since then they've been inseparable. They hold hands in the supermarket. They share one plate of chips and fight over the last one. They have a joint spreadsheet for their houseplants. Jonah learned to make Dad's dal from a voice note, and Priya learned the offside rule, which is the greatest act of love I have ever witnessed.
Tomorrow they fly to Lisbon for the honeymoon, so please, raise your glasses — to Priya and Jonah, and to many more years of arguing about chips.
""",
twin=[("They hold hands in the supermarket.",
       "They hold hands in the supermarket, and judging by the noise complaints from their old landlord, they do a lot more than hold hands at home — I'm told the headboard left a dent in the wall.")]),

S("dt08_lunch_breaks", "c", """
Personals — Men seeking women

M, 40s, professional, married but it's complicated. Seeking a discreet lady for weekday lunch breaks — there's a hotel five minutes from the business park and I'll take care of the room. Chemistry first, no strings, no sleepovers, no texting after six. I'm fit, clean, and very good at making an hour feel like an afternoon. Tell me what you'd want to do with that hour and I'll tell you if I can keep up.
"""),

N("dt10_duvet_caption", "c", """
Instagram caption — posted by @marisolandjune

Five years ago today I married the woman who steals the duvet, sings Fleetwood Mac badly in the shower and still leaves notes in my lunchbox. We celebrated at the same cheap Thai place we went to on our first date, and the owner remembered us. 🥹 Five years of you, and I'd choose every single day again. Happy anniversary, June. ❤️
#fiveyears #wifey #loveislove
""",
twin=[("and I'd choose every single day again.",
       "and five years of the best nights of my life under that stolen duvet, if you know what I mean 😏 Tonight we're not leaving the bedroom.")]),

S("dt11_pic_request", "y", """
Match chat — Dev (31) and Sam (29)

Dev: you looked really good tonight btw
Sam: haha thanks, you cleaned up ok yourself
Dev: send me a pic of what you're wearing under that dress. or what you're not wearing 😈
Sam: lol slow down
Dev: come on, just one. I'll send one back, you know you want to see it
""", ask="N",
twin=[("send me a pic of what you're wearing under that dress. or what you're not wearing 😈",
       "send me a pic of that dessert you ordered. I need to know if it's worth going back for 🍰"),
      ("come on, just one. I'll send one back, you know you want to see it",
       "come on, just one. I'll send you my sad microwave pasta in return")]),

N("dt12_first_date_habits", "c", """
Meeting someone from an app? Ten habits that keep first dates safe

1. Video-call before you meet. Two minutes is enough to confirm the person matches their photos.
2. Meet somewhere public and busy, and get there under your own steam.
3. Tell a friend where you'll be and when you expect to be home. Share your location if you're comfortable.
4. Keep an eye on your drink; if you leave the table, order a new one.
5. Don't feel you owe anyone a second venue, a lift home, or an invitation in.
6. If you do decide to go home with someone, talk about consent and protection before things get physical, while you're both clear-headed.
7. Keep your home address to yourself until you know them better.
8. Trust the small uneasy feeling. You can leave mid-drink; “I'm heading off, take care” is enough.
9. Report profiles that pressure you for money, images or personal details.
10. Agree a code word with a friend that means “call me with an emergency.”
"""),

S("dt13_club_velour", "c", """
Event listing — Saturday 14 June, Club Velour, Canal Street

Couples' Night returns! First drink on the house for every pair through the door before 10 pm. DJ Oriel on the decks from nine.
Dress code: lingerie or less. No jeans, no trainers.
The private rooms upstairs open at midnight for couples who want to swap more than phone numbers. Keys from the bar, no questions asked, and nobody leaves with the partner they came in with unless they want to.
Singles admitted by invitation only. Strictly over-21s; ID checked at the door.
"""),

N("dt14_palais_oral_history", "y", """
Transcribed from a family oral-history recording, 2019

Your grandmother always said she knew on the third dance. I say it was the second, but she was the one keeping count. It was the Palais in Hammersmith, 1958, and I'd borrowed my brother's jacket, which was too big in the shoulders. She told me I looked like a wardrobe. I asked her to dance again anyway.
We courted for two years. Every Sunday I took the bus to her mother's for tea and sat on a sofa with a plastic cover while her mother asked me about my prospects. I didn't have any prospects. I had a bicycle. Your grandmother used to walk me back to the stop and we'd hold hands under her umbrella, and that was the whole of it, and it was enough.
We married in the spring of 1960. Sixty-one years. She still laughed at the wardrobe joke the week before she died.
"""),

S("dt15_nocturne_poem", "c", """
“Nocturne” — posted to a poetry forum, weekly prompt: after midnight

Unbutton the evening, one button at a time;
let the lamp keep what it sees.
Your mouth, a map I've learned by heart,
goes travelling the long country of my skin —
we will not need the blanket,
we will not need to sleep,
until the birds begin,
and when they do, we'll make them wait.
"""),

N("dt16_tuesday_poem", "y", """
“Tuesday” — from a small-press poetry pamphlet

You fold the towels the way my mother did,
in thirds, then thirds again,
and I have never told you
that it undoes me every time.
You hum when you are reading.
You leave the last square of chocolate
on my side of the table
and pretend you forgot.
Thirty years. I would marry you again
in the rain, in the same bad suit,
at the same registry office
with the broken clock.
"""),

S("dt17_conference_room", "c", """
Slack DM, 6:14 pm

Jess: that presentation ran SO long 😩
Omar: I can think of better ways to spend an hour in that conference room
Jess: oh yeah?
Omar: lock the door and I'll show you. nobody checks the third floor after six, and I've been thinking about that skirt all afternoon 😏
Jess: omar!! 😳 give me ten minutes
""",
twin=[("lock the door and I'll show you. nobody checks the third floor after six, and I've been thinking about that skirt all afternoon 😏",
       "a nap, for one. or finishing the Q3 deck so we don't have to redo it tomorrow. I've been dreading those charts all afternoon 😩"),
      ("omar!! 😳 give me ten minutes", "omar!! 😂 fine, give me ten minutes and I'll grab the laptop")]),

N("dt18_whitby_breakup", "c", """
Text message, Sunday 11:03 pm

I've been trying to write this for a week so I'm just going to send it. I don't think we should keep seeing each other. It isn't anything you did. You've been kind to me the whole time, I loved meeting your sister, and that weekend in Whitby was one of the best I've had in years. But I keep waiting to feel more than I do, and it isn't fair to you for me to keep waiting. I'd like to still be friends one day, if you want that, but I understand if you need space. I'm sorry. I'll drop your jumper round on Tuesday.
""",
twin=[("and that weekend in Whitby was one of the best I've had in years.",
       "and that weekend in Whitby, when we didn't leave the hotel bed until checkout and not because we were tired, was one of the best I've had in years.")]),

S("dt19_gentleman_traveller", "c", """
Profile — “Gentleman Traveller”, 52

Busy executive, widowed, based in Zurich and London. I travel constantly and I'm tired of dining alone. Seeking an attractive, polished companion, 25+, for weekend trips, gallery openings and private time at the hotel afterwards.
Monthly allowance for the right arrangement. Intimacy expected; chemistry required. Discretion is everything — I don't do social media and neither should you.
Serious enquiries only. Please include recent full-length photos.
""",
twin=[("gallery openings and private time at the hotel afterwards.", "gallery openings and long dinners."),
      ("Intimacy expected; chemistry required.", "Strictly platonic; good conversation required."),
      ("Please include recent full-length photos.", "Please include a note on what you're reading.")]),

N("dt20_kofi_profile", "c", """
Profile — Kofi, 38

6'2", dad bod in progress, tattoos on both forearms (yes, one is a spelling mistake, ask me about it). Gym three mornings a week, mainly so I can keep eating my aunt's jollof without guilt.
I'm a paramedic, so my hours are chaos and my stories are unrepeatable at dinner. I like long walks that end at a pub, crosswords, and people who say what they mean.
Looking for someone who wants a real relationship, likes dogs, and doesn't mind that I fall asleep during every film.
""",
twin=[("Looking for someone who wants a real relationship, likes dogs, and doesn't mind that I fall asleep during every film.",
       "Looking for someone who wants to come back to mine after the first drink and find out exactly what a paramedic can do with his hands. I promise you won't be falling asleep 😏")]),

N("dt21_after_baby_column", "y", """
Column — “Us, After Baby”, by a licensed couples therapist

One of the most common things new parents tell me, usually in a low voice as if confessing a crime, is that they haven't had sex since the birth and they're worried about what that means. Here's what I tell them: for most couples, desire drops sharply in the first year. Sleep deprivation, hormonal shifts during breastfeeding and recovery from delivery all play a part. It is normal, and it is usually temporary.
What helps is not scheduling sex like a dental appointment, but protecting small moments of connection: ten minutes on the sofa at the end of the day, a hand on the shoulder in passing, actually asking “how are you?” and waiting for the answer. Talk about it openly and without blame. If one of you is experiencing pain, or low mood that lasts more than a couple of weeks, see a GP — both are common and treatable.
""", ask="N"),

S("dt22_corkscrew", "c", """
Anonymous confessions board — post #4482

I've had a thing for my neighbour across the landing for months. Last night around eleven she knocked to borrow a corkscrew. She never made it back to her own flat. The corkscrew is still on my counter, and so is her bra, and I can still smell her perfume on my pillow. I have no idea what happens when we pass each other on the stairs tomorrow, and honestly I don't care. Best Tuesday of my life.
""",
twin=[("She never made it back to her own flat.", "She stayed for one glass and we talked until one."),
      ("and so is her bra, and I can still smell her perfume on my pillow",
       "and so is her phone number, written on the back of a takeaway menu")]),

N("dt23_mercer_street_blurb", "c", """
Back-cover copy — “The Last Loaf on Mercer Street”

When disgraced pastry chef Delphine Aubert inherits her great-aunt's failing bakery in a Vermont town she has never heard of, she plans to sell it by Christmas. Then she meets Callum Reyes, the grumpy carpenter who has been fixing the bakery's ovens for free for three years and has opinions about her croissants.
Sparks fly. Flour flies further. And as the town's winter festival approaches, Delphine has to decide whether she's running from her past or finally baking her way toward a future.
A cosy, slow-burn romance about second chances, small-town secrets and the perfect sourdough starter.
""",
twin=[("Sparks fly. Flour flies further.",
       "Sparks fly — and so do their clothes, all over the flour-dusted counter one night after closing, and then again in the storeroom, and again upstairs.")]),

S("dt24_room_twelve_blurb", "y", """
Back-cover copy — “Room Twelve”

Every Thursday at nine, Nathaniel Crane unlocks the door of Room Twelve at the Harbour Hotel, and Iris is already waiting for him — in nothing but his shirt, with the curtains drawn and the do-not-disturb sign on the handle. No names. No feelings. No daylight.
It's the perfect arrangement, until the night she discovers who he really is, and realises she can't give up Thursdays any more than she can give up breathing.
"""),

N("dt25_osteria_reservation", "c", """
Online reservation — Osteria Lume, Saturday 8 pm, table for two

Special requests: It's our 20th wedding anniversary! My husband doesn't know I booked the place where he proposed (table by the window, if it's still there). Could you put a single rose on the table and maybe bring the tiramisu with a candle at the end? He'll pretend to be embarrassed but he'll love it. Also, he's allergic to shellfish. Thank you so much!
""",
twin=[("He'll pretend to be embarrassed but he'll love it.",
       "He'll pretend to be embarrassed but he'll love it. I've also booked the room upstairs, so please don't let dessert drag — I'm planning to have him out of that suit well before midnight 😉")]),

S("dt26_voicemail_landed", "y", """
Voicemail transcript, Wednesday 7:18 am

“Hi, it's me. Just landed. Sorry, I know it's early. I'm still thinking about Saturday — the way you pulled me back under the covers every time I tried to get up for my flight. I nearly missed it, you know. Anyway. Clear your Friday night, and your Saturday morning, because I'm not planning on letting you get dressed until Sunday. Okay. Bye. Call me.”
"""),

N("dt27_denver_tour_guide", "y", """
Forum — Travel buddies / Denver

Visiting Denver for a conference next week (F, 38). Free after 8 pm most nights and I don't know a soul in the city. Looking for someone who knows the brewery scene and wouldn't mind playing tour guide for an evening — happy to buy the first round and the tacos. Bonus points if you know where to see live bluegrass on a Tuesday. Send me your top three spots and a bit about yourself!
""",
twin=[("Looking for someone who knows the brewery scene and wouldn't mind playing tour guide for an evening — happy to buy the first round and the tacos.",
       "Looking for someone who'd rather skip the brewery and come straight up to my hotel room — do-not-disturb sign on, no names needed, gone by breakfast.")]),

N("dt28_ace_marriage", "c", """
r/asexuality — “How my allo partner and I make it work (long, sorry)”

I'm ace and my husband isn't. We've been married six years, and for the first two I felt like I was constantly failing a test I didn't understand. We ended up seeing a counsellor who actually knew what asexuality was, which helped more than anything.
What works for us: we talked, very plainly, about what sex means to each of us. For him it's mostly about feeling wanted and close. For me closeness comes from other things. So we built a lot of it — long baths together, cuddling every night, holding hands on the sofa, a standing Sunday walk where we talk about anything. We agreed on what we're each comfortable with, and we check in every few months because feelings change.
I'm not posting this as a template. Every couple is different. But if you're ace and scared that it means you can't have a loving marriage, you can. It just takes more talking than people expect.
"""),

S("dt29_hen_suite", "c", """
Group chat — “Mel's Last Fling 💍”

Okay ladies, final plan for Saturday!! 7 pm cocktails at the hotel bar, 8:30 dinner, then everyone up to the suite. And yes — Marco from “Firefighters After Dark” is booked for a private show at ten 🔥 He'll be losing the uniform piece by piece and Mel is getting a front-row chair, so bring plenty of singles. What happens in the suite stays in the suite 😘
""",
twin=[("Marco from “Firefighters After Dark” is booked for a private show at ten 🔥 He'll be losing the uniform piece by piece and Mel is getting a front-row chair, so bring plenty of singles.",
       "a cocktail instructor is booked for a private class at ten 🍸 He'll be teaching us three drinks and Mel is getting the first shaker, so bring an appetite.")]),

N("dt30_red_dress", "c", """
Text thread, Friday 5:40 pm

Leah: reservation's at 8, I'll pick you up at half 7
Chris: what should I wear? is it fancy
Leah: a bit! wear the red dress, you look amazing in it
Chris: the one from Ana's wedding?
Leah: that's the one. and bring a jacket, it's on the roof terrace
""",
twin=[("wear the red dress, you look amazing in it",
       "wear the red dress, and nothing underneath it. I'll be thinking about peeling it off you all through dinner")]),

S("dt31_squeaky_bed", "c", """
Post by @dana_does_diy

My husband announced on Saturday morning that this was finally the weekend he'd “fix the squeaky bed.” Reader, it is Sunday night, the bed is squeakier than ever, and neither of us has left the bedroom since noon except to answer the door for a pizza. The neighbours have started knocking on the wall. Best DIY weekend of our marriage. 😇
""",
twin=[("and neither of us has left the bedroom since noon except to answer the door for a pizza. The neighbours have started knocking on the wall.",
       "and he has now watched eleven YouTube tutorials, bought three kinds of washer and taken the whole frame apart on the landing. The neighbours have started offering advice over the fence."),
      ("Best DIY weekend of our marriage. 😇", "Worst DIY weekend of our marriage. 🙃")]),

N("dt32_consent_workshop", "c", """
Workshop handout — “Talking About Consent: A Guide for Adult Couples” (community health centre, Tuesday evenings)

Consent isn't a one-time signature. It's an ongoing conversation that applies to long-term partners as much as to new ones. In this session we'll practise:
• Asking clearly and accepting the answer, including “not tonight” and “I'm not sure.”
• Noticing non-verbal signals and checking in when they change.
• Understanding why alcohol and pressure undermine consent.
• Talking about boundaries, contraception and sexual health outside the bedroom, when both people are relaxed.
• What to do if a partner has crossed a line, and where to get support.
The session is discussion-based, confidential and open to adults of any orientation. Couples and individuals both welcome. Tea and biscuits provided.
"""),

S("dt33_profile_pic_dm", "y", """
DMs — Instagram

Ty: new profile pic is 🔥
Ines: haha thank you, my sister took it at the lake
Ty: the angle is doing a LOT for you. that top especially. I've been staring at it for ten minutes and thinking about what I'd do to you if I'd been there instead of her
Ty: send me the ones she didn't post 😏
""", ask="N"),

N("dt34_unsent_note", "c", """
Draft saved in Notes, not sent

I can't stop thinking about you and it's getting embarrassing. Your laugh, which is too loud for libraries. The way you hum when you cook and pretend you're not humming. How you remembered my mum's surgery date and texted me that morning. I keep rehearsing how to say this out loud, and every version sounds like a greeting card. So here's the plain one: I like you, a lot, and I'd like to take you to dinner, properly, as a date. If that's not what you want, I'll still be your friend and I'll still steal your chips.
""",
twin=[("I'd like to take you to dinner, properly, as a date.",
       "I'd like to take you home, properly, and not let you out of my bed until morning.")]),
]
