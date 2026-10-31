"""Hand-written BINJ 'offensive' items whose base label is OFFENSIVE (y=1).

Same fields as items_not.py. Twins (tw / tw_full) flip the label to not offensive.
All texts are invented.
"""

ITEMS = [
# ---------------------------------------------------- polite-sounding contempt
dict(k="pc_number_nine", y=1, t="the email", s="""Email to the Linden Close residents' association mailing list

Subject: A gentle word about number 9

Dear neighbours,
I do hope you're all well and enjoying the lighter evenings. I hesitate to raise this, as I know how it can sound, but I felt someone ought to.

As you'll have noticed, the rental at number 9 has a new family. I'm sure they're lovely in their own way, but I think we all know that people from that sort of background don't share our standards when it comes to upkeep, noise or, frankly, hygiene. We've all seen what happens to a close when that's allowed to take hold.

Perhaps the committee could consider, discreetly, what might be done before property values reflect it. I'd be happy to host a small meeting at mine on Thursday; I'll do a lemon drizzle.

Warm regards,
Penelope (number 4)""",
     tw=[("I'm sure they're lovely in their own way, but I think we all know that people from that sort of background don't share our standards when it comes to upkeep, noise or, frankly, hygiene. We've all seen what happens to a close when that's allowed to take hold.\n\nPerhaps the committee could consider, discreetly, what might be done before property values reflect it.", "They have three young children, and I gather the landlord has left the boiler broken since they moved in, which in this cold is no joke.\n\nPerhaps the committee could consider, discreetly, leaning on the landlord to get it fixed before winter.")]),

dict(k="pc_brian_age", y=1, t="the comment", s="""LinkedIn comment under a post by a product director

With the greatest respect to Brian, and I mean that sincerely, this is exactly why we need to stop hiring people his age for product roles. It's not his fault; the brain simply stops adapting after fifty and there's no shame in that. Some people are better suited to, say, a quiet admin role where the pace suits them. Wishing him all the best."""),

dict(k="pc_hotel_reply", y=1, t="the owner's reply", s="""Reply from a boutique hotel owner to a TripAdvisor review

Dear Guest, thank you for your feedback. We're sorry our hotel wasn't to your taste. We do find that guests who choose to travel on budget airlines and bring their own food into the room sometimes have expectations that are better met at a hostel. We wish you well in finding somewhere more suited to your means, and perhaps your manners."""),

dict(k="pc_school_run", y=1, t="the post", s="""Post in a village Facebook group

Just a friendly reminder, and I say this with love, that the school run isn't a catwalk. Some of the mums from the new estate might want to consider that the rest of us don't need to see quite that much tattoo and leggings at 8.45am. Standards matter, even for people who weren't raised with them. Have a blessed day, everyone! 🌸"""),

dict(k="pc_osei_paper", y=1, t="the comment", s="""Comment on an academic group blog, under a post about a new working paper

I read Dr Osei's paper with real interest, and I want to be encouraging. It is admirably ambitious for someone trained where she was, and one can hardly expect the methodological rigour of a proper research university from a department of that kind. The writing is clear enough, given that English is presumably not her first language.

I'm sure with time, and some supervision from people who understand the field, she'll produce something publishable. It's lovely to see scholars from that part of the world having a go at questions like this, and I'd hate for my comments to discourage her.""",
     tw=[("It is admirably ambitious for someone trained where she was, and one can hardly expect the methodological rigour of a proper research university from a department of that kind. The writing is clear enough, given that English is presumably not her first language.\n\nI'm sure with time, and some supervision from people who understand the field, she'll produce something publishable. It's lovely to see scholars from that part of the world having a go at questions like this, and I'd hate for my comments to discourage her.", "It is admirably ambitious, and the writing is very clear. My main concern is section 4: a sample of 38 firms is too small to carry the causal claim, and the instrument looks correlated with firm size.\n\nA second site or a longer follow-up would make the argument much stronger. I'd be glad to share the panel data we collected in 2019 if it's useful, and I'd hate for my comments to discourage her; this question needs more work like this.")]),

dict(k="pc_ward_feedback", y=1, t="the feedback", s="""Hospital patient feedback form, free-text box

The care was adequate. I would only note that it would be helpful if the ward employed at least some nurses who speak English as a first language and were raised with our values. One doesn't like to complain about people who are clearly doing their best with limited abilities, but patients deserve to be looked after by their own."""),

dict(k="pc_best_man", y=1, t="the post", s="""Facebook post with a video of a best man's speech

Caption: Nailed it 😂 Tom's face!!

Transcript: '...and of course, welcome to Sarah's family, who've come all the way from Merseyside! Don't worry, lads, we've counted the spoons and locked the cars.' [laughter] 'No, but genuinely, it's wonderful that Tom has married so far out of his comfort zone. Sarah, love, you've done very well for yourself.'""",
     tw=[("Caption: Nailed it 😂 Tom's face!!", "Caption: Sat next to the bride's nan while the best man did this. She didn't laugh once. Neither did I. Posting it so he can see how it looked from the other side of the room.")]),

dict(k="pc_perf_review", y=1, t="the review comment", s="""Annual performance review, manager's written comments

Overall rating: Meets some expectations

Priya is a pleasant colleague and clearly works very hard to keep up with the rest of the team. She is always punctual and never complains, which is appreciated, and she has been generous with her time in helping the new starters with the reporting templates.

Given her background, her written English is better than we might have expected, and we'd encourage her to keep going with the evening classes. Her spoken English is serviceable for internal meetings, although some clients have commented on the accent, and I have not been able to put her forward for the Hartwell pitch for that reason.

On technical work, her models are accurate, but she tends to follow the template rather than show initiative. I suspect this is partly cultural; people from her part of the world are often brought up to defer rather than lead, and it would be unfair to expect her to change that overnight.

Development: Priya may simply be more comfortable in a supporting role than in client-facing work, where our clients tend to expect a certain polish. I'd suggest we don't pursue the senior associate promotion this cycle and revisit in two years.

Signed: D. Whitmore, Associate Director"""),

dict(k="pc_parish_coffee", y=1, t="the newsletter item", s="""Parish newsletter, 'From the Vicarage', October edition

We are delighted to welcome so many new faces this autumn, and the harvest supper raised £1,140 for the roof fund. Thank you to everyone who baked.

A small request regarding the Sunday coffee morning. It is a time of quiet fellowship for the congregation, and some of our newer attendees from the Bridge Street hostel might be gently reminded that it is not a free breakfast service. We do so love to help the less fortunate, but perhaps they would feel more comfortable at the Thursday food bank, among their own sort, where there is less expectation of conversation.

The flower rota for November is on the noticeboard.

With every blessing,
Rev. Ian Marsh""",
     tw=[("It is a time of quiet fellowship for the congregation, and some of our newer attendees from the Bridge Street hostel might be gently reminded that it is not a free breakfast service. We do so love to help the less fortunate, but perhaps they would feel more comfortable at the Thursday food bank, among their own sort, where there is less expectation of conversation.", "Our friends from the Bridge Street hostel are warmly invited to stay for the full breakfast, which the Mothers' Union now serves from eleven. If anyone would like to help at the Thursday food bank, where we are short of drivers, please see Margaret.")]),

dict(k="pc_cooking_smell", y=1, t="the post", s="""Nextdoor post

I don't want to cause a fuss, but could the new family at 22 perhaps keep their windows shut when they're cooking? The smell of whatever it is they eat is quite overpowering, and some of us moved here for a certain kind of neighbourhood. I'm sure where they come from it's perfectly normal. Thank you in advance for being considerate."""),

dict(k="pc_teacher_email", y=1, t="the email", s="""Email from a parent to a primary school teacher

Dear Ms Kowalczyk,
Thank you for your note about Oliver's behaviour. I appreciate you're doing your best, and I realise it can't be easy teaching in a second language. Perhaps when you've been in this country a little longer you'll understand how we do things here, and why a boy like Oliver needs a firmer hand than you seem able to give. I have copied the head in, just so there's someone involved who understands.
Kind regards,
Mrs A. Hartley"""),

dict(k="pc_cousin_girlfriend", y=1, t="the tweet", s="""Tweet

Had dinner with my cousin's new girlfriend tonight. She was very sweet, bless her. Didn't know who Tolstoy was, thought Lisbon was in Italy, and laughed at everything like a golden retriever. Honestly refreshing to meet someone so uncomplicated. I can see why he likes her; it must be restful not having to think.""",
     tw=[("Didn't know who Tolstoy was, thought Lisbon was in Italy, and laughed at everything like a golden retriever. Honestly refreshing to meet someone so uncomplicated. I can see why he likes her; it must be restful not having to think.", "She's a paramedic, told brilliant stories about night shifts, and laughed at all my terrible jokes. Honestly refreshing to meet someone so easy to be around. I can see why he likes her.")]),

# ---------------------------------------------------------------- dog whistles
dict(k="dw_globalist_families", y=1, t="the tweet", s="""Tweet

Funny how every time you trace the money behind these 'open borders' NGOs you end up at the same handful of globalist families. Same names behind the banks, the media, Hollywood. Not saying anything, just noticing. 🤔 Do your own research on the surnames.""",
     tw_full="""Tweet

Every week my replies fill up with some version of this: 'Funny how every time you trace the money behind these open borders NGOs you end up at the same handful of globalist families. Same names behind the banks, the media, Hollywood. Just noticing. Do your own research on the surnames.' That is a centuries-old antisemitic conspiracy theory with new vocabulary. Report it, don't engage with it."""),

dict(k="dw_which_community", y=1, t="the comment", s="""Comment on a local news story about a stabbing

Another one. Nobody will say it but we all know which 'community' this is coming from. It's not about poverty, plenty of people are poor. It's the culture: no fathers at home, music glorifying it, and the same demographic every single time. Look at the photos of the suspects and tell me I'm wrong."""),

dict(k="dw_replaced", y=1, t="the forum post", s="""Forum post, 'Heritage & Identity' board

Title: Nobody voted for this

Dig out your old primary school class photo from 1985 and compare it with your kid's from this year. Go on. I did, and I didn't recognise my own town. Our birth rate is falling and theirs isn't, and the people in charge call that 'enrichment' and 'vibrancy'. Nobody asked us.

It isn't about individuals. I'm sure some of them are decent enough. It's about numbers. In a generation we'll be strangers in our own towns, a minority in the country our grandparents fought for, and anyone who points it out gets called a bigot. It's not hate to notice you're being replaced. It's arithmetic.

Share this with anyone who's still asleep.""",
     tw_full="""Forum post, 'Heritage & Identity' board (moderator)

Title: Thread locked, please read

I've locked the 'Nobody voted for this' thread. The opening post told people to compare school photos from 1985 with today's, said 'our birth rate is falling and theirs isn't', and claimed that 'in a generation we'll be strangers in our own towns' and that 'it's not hate to notice you're being replaced'.

That is the 'great replacement' conspiracy theory. It treats neighbours as an invading population, and it has been quoted in the manifestos of more than one mass murderer. It isn't arithmetic and it isn't heritage.

This board exists for local history, family trees and old photographs of the high street. Those are welcome. Replacement theory is not, and repeat posts will lead to a ban."""),

dict(k="dw_first_officer", y=1, t="the comment", s="""Reddit comment in r/aviation

Not saying the first officer on that flight was a diversity hire, but when an airline brags about hitting its 'representation targets' and then a plane ends up on a grass verge, you do start to wonder who's actually flying. Give me a boring pilot who got there on merit.""",
     tw=[("Not saying the first officer on that flight was a diversity hire, but when an airline brags about hitting its 'representation targets' and then a plane ends up on a grass verge, you do start to wonder who's actually flying. Give me a boring pilot who got there on merit.", "The interim report says the first officer called the approach unstable twice and the captain overrode her. People calling her a 'diversity hire' in the other thread should read it. She's the reason a go-around was even discussed.")]),

dict(k="dw_groomers", y=1, t="the comment", s="""Facebook comment on a post about a school board meeting

Parents need to wake up. The same people pushing drag story hour and 'inclusive' books on six-year-olds are the ones asking for private time with your kids. We used to have a word for adults who do that. Groomers. Keep your children away from these teachers."""),

dict(k="dw_buggies", y=1, t="the comment", s="""Comment on an article about child benefit changes

Good. Maybe now certain people will stop popping out kids for the extra cash. Walk around the estates on a Thursday morning and see who's in the queue at the post office with five buggies and no wedding ring. We all know who's paying for it."""),

dict(k="dw_same_percent", y=1, t="the reply", s="""Twitter/X reply to a news clip about a shoplifting spree

Let me guess before I click. Same 13% as always? At some point it stops being a coincidence and starts being a pattern. The media won't show you the faces for a reason, and everyone knows exactly what that reason is."""),

dict(k="dw_rootless", y=1, t="the comment", s="""Comment under a newspaper book review

The author is exactly the type you'd expect: London media, dual loyalties, a rootless cosmopolitan who has never felt any attachment to a country in his life. No surprise he thinks national identity is a myth. His sort never had one to begin with.""",
     tw_full="""Comment under a newspaper book review

The reviewer calls the author 'a rootless cosmopolitan with dual loyalties'. Readers should know that 'rootless cosmopolitan' was the Soviet state's euphemism for Jews during the 1949 purges, and 'dual loyalties' has a similar pedigree. Whatever you think of the book's argument about national identity, that is not a neutral description of a writer, and the paper should not have printed it."""),

dict(k="dw_our_friends", y=1, t="the message", s="""WhatsApp message in a village residents' group

Heads up everyone, 'our friends' are back on the field by the cricket club. Four caravans this morning. Lock your sheds, bring the bikes in and keep an eye on the dogs. You know what happened last time. I've already rung the council but we all know they won't do anything."""),

dict(k="dw_certain_countries", y=1, t="the message", s="""Message in a recruiters' Slack community

Pro tip: when you see a CV from certain countries, check the references twice. I'm not being funny, it's just experience. The qualifications are 'flexible' over there, if you catch my drift, and the work ethic isn't what we're used to. Saves everyone time."""),

# ------------------------------------------------------ backhanded compliments
dict(k="bc_articulate_lad", y=1, t="the comment", s="""Comment on a local news video interview with a teenage campaigner

Fair play to the young lad, he's very articulate and well spoken for someone from that area. You don't expect it. His parents must have worked hard to keep him away from the usual influences. Hope he goes far.""",
     tw=[("he's very articulate and well spoken for someone from that area. You don't expect it. His parents must have worked hard to keep him away from the usual influences.", "he made the case for keeping the youth centre open better than any councillor has in years. The figures he quoted about the evening sessions were spot on.")]),

dict(k="bc_pretty_for", y=1, t="the comment", s="""Instagram comment on a woman's holiday photo

honestly you're really pretty for a bigger girl, you carry it well!! most girls your size wouldn't have the confidence to wear that. good for you babe 💕""",
     tw=[("honestly you're really pretty for a bigger girl, you carry it well!! most girls your size wouldn't have the confidence to wear that.", "honestly you look so good in this, that colour is perfect on you!! i need the link for that dress asap.")]),

dict(k="bc_english_dm", y=1, t="the message", s="""Slack direct message sent to Jenny Tran, a colleague who was born and raised in Manchester

hey, just wanted to say your presentation today was really good! your English is honestly better than mine lol, where did you learn it? like I can barely even hear the accent. you should present more often"""),

dict(k="bc_bridge_engineer", y=1, t="the comment", s="""Comment on a construction firm's Instagram post celebrating one of its engineers

Wow, she actually designed the bridge herself? Impressive for a girl! Usually the women in these photos are just there for the diversity quota lol. Credit where it's due, sweetheart 👏""",
     tw=[("Wow, she actually designed the bridge herself? Impressive for a girl! Usually the women in these photos are just there for the diversity quota lol. Credit where it's due, sweetheart 👏", "Wow, she designed the bridge herself? That cantilever span is beautiful work. I did my thesis on cable-stayed designs and this is a textbook example. Credit where it's due 👏")]),

dict(k="bc_wheelchair_tesco", y=1, t="the comment", s="""Facebook comment

Saw a lad in a wheelchair doing his own shopping at Tesco today, bless him. Honestly so inspiring. If he can manage to get out of the house, the rest of us have no excuse! I'd have given up if I were him, what kind of life is that. Makes you grateful for your health, doesn't it."""),

dict(k="bc_doreen_parking", y=1, t="the tweet", s="""Tweet

My 74-year-old neighbour just parallel parked first time and I nearly gave her a round of applause. Didn't think they let them keep their licences at that age, never mind actually be able to see the kerb. Good on you, Doreen, still got a few marbles left 👵"""),

dict(k="bc_not_flamboyant", y=1, t="the tweet", s="""Tweet

My new coworker is gay but you honestly wouldn't know it, he's not one of those flamboyant ones who shoves it in your face. Just a normal bloke who likes football. We need more like him tbh.""",
     tw=[("My new coworker is gay but you honestly wouldn't know it, he's not one of those flamboyant ones who shoves it in your face. Just a normal bloke who likes football.", "My new coworker is gay and he's already dragged me into the office five-a-side team and the Thursday pub quiz. Top bloke, terrible at football.")]),

dict(k="bc_reading_award", y=1, t="the comment", s="""Comment on a primary school's Facebook post about its reading awards

So lovely to see little Kayden get the reading award, especially given everything at home. You'd never guess his mum is on her own with three different dads' kids. Shows anyone can do it, even from that kind of start!"""),

dict(k="bc_mit_robot", y=1, t="the comment", s="""Reddit comment in r/ApplyingToCollege

I mean, of course she got into MIT, she's Asian. Her parents probably had her doing calculus in the womb. No offence, I'm sure she's nice, but it's not exactly impressive when you're basically a study robot. I'd like to see what she does without Tiger Mom."""),

dict(k="bc_weather_brummie", y=1, t="the comment", s="""Comment on a national broadcaster's website

Have to say the new weather presenter is doing much better than I expected. Considering where she's from, her diction is surprisingly clear, and she's clearly been coached to tone down the Brummie. Give her a year and she might even sound educated.""",
     tw=[("Considering where she's from, her diction is surprisingly clear, and she's clearly been coached to tone down the Brummie. Give her a year and she might even sound educated.", "She explains the pressure charts better than anyone they've had, and I love hearing a Brummie accent on national telly. Give her the evening slot.")]),

# --------------------------------------------------------- insults at people
dict(k="ins_darren_thick", y=1, t="the reply", s="""Reply on a Facebook post about a council tax rise

Darren, you are genuinely the thickest man I've ever seen online. Every thread, same copy-pasted nonsense. Did your mum drop you as a baby or did you work at it? Go back to colouring in and leave the budget to people who can count.""",
     tw_full="""Reply on a Facebook post about a council tax rise

Darren, I think you've got this wrong. Every thread you post the same figure, and it's from 2019. The rise this year is 4.9%, and the breakdown is on page 3 of the budget document, including the adult social care precept. Happy to send you the link if you want to check it yourself."""),

dict(k="ins_facecam", y=1, t="the comment", s="""YouTube comment on a gaming stream VOD

bro you are so painfully unfunny it's actually impressive. 40 minutes of you laughing at your own jokes with that horse face. nobody is watching this for you, we're here for the game. do everyone a favour and turn the facecam off permanently."""),

dict(k="ins_ruth_email", y=1, t="the email", s="""Email, accidentally sent to the whole team instead of one colleague

Can you believe Ruth actually presented that to the client? The woman's a walking HR complaint with the brain of a goldfish. I spent three days fixing her numbers and she still managed to mispronounce the client's name. Please god, let her retire before the audit.""",
     tw=[("The woman's a walking HR complaint with the brain of a goldfish. I spent three days fixing her numbers and she still managed to mispronounce the client's name. Please god, let her retire before the audit.", "I spent three days on the numbers and she still stood up there and made it look easy, even after the projector died. I'd have panicked. Please god, let her lead the audit prep.")]),

dict(k="ins_tutor_jake", y=1, t="the message", s="""Message from a private tutor to a student's parent

I've tried my best with Jake but frankly he's lazy, dim and rude, and I don't think that's going to change. Some kids just aren't worth the effort, and he's one of them. I won't be continuing sessions after this month. Invoice attached."""),

dict(k="ins_ranked_chat", y=1, t="vex_3000's messages", s="""In-game chat log, ranked match

[ALL] vex_3000: mid laner is a braindead monkey
[ALL] vex_3000: uninstall you absolute waste of oxygen
[ALL] vex_3000: report tomas_k for being born
[ALL] tomas_k: gg
[ALL] vex_3000: gg for you maybe, your parents lost the moment you arrived"""),

dict(k="ins_ex_market", y=1, t="the tweet", s="""Tweet

Saw my ex at the farmers' market today. Still looks like a thumb with a fringe, still can't talk to anyone without making it about himself, still dating women half his age because nobody his own age can stand him. Some things never change.""",
     tw=[("Still looks like a thumb with a fringe, still can't talk to anyone without making it about himself, still dating women half his age because nobody his own age can stand him. Some things never change.", "We had a nice chat by the cheese stall; he's doing well, new job, new dog. I'm glad. Ten years ago I couldn't have imagined being fine about it. Some things do change.")]),

dict(k="ins_u10_ref", y=1, t="the comment", s="""Facebook comment in a grassroots football parents' group

The ref on Sunday for the under-10s was an absolute disgrace. Fat, useless and probably pissed. Couldn't run, couldn't see, and I'd bet he's got a son on the other team. Somebody find out his name and let's see how brave he is then."""),

dict(k="ins_letting_agent", y=1, t="the review", s="""Google review of a letting agent, 1 star

The agent handling our flat, Callum, is a slimy, smirking weasel who couldn't lie straight in bed. Deposit still not returned after 11 weeks, three unanswered emails and a 'deduction' for a stain that was in the check-in photos. Avoid.""",
     tw=[("is a slimy, smirking weasel who couldn't lie straight in bed.", "stopped replying to us the day we handed the keys back.")]),

# -------------------------------------------- demeaning generalisations
dict(k="gen_women_leaders", y=1, t="the comment", s="""Reddit comment in r/AskMen, replying to 'What's something you believe that most people won't say out loud?'

Genuine question, not trying to be controversial: why do we keep pretending women are suited to leadership? I've worked in three companies over fifteen years and every female manager I've had has been a nightmare. They're more emotional, they take disagreement personally, and for a week of every month they're not thinking straight. That's not sexism, that's biology.

Nobody says it because HR would have your head, but everyone in every office I've worked in knows it. At some point you have to look at the pattern and stop pretending.""",
     tw=[("why do we keep pretending women are suited to leadership? I've worked in three companies over fifteen years and every female manager I've had has been a nightmare. They're more emotional, they take disagreement personally, and for a week of every month they're not thinking straight. That's not sexism, that's biology.\n\nNobody says it because HR would have your head, but everyone in every office I've worked in knows it.", "why do so many men in this sub assume women can't lead? I've worked in three companies over fifteen years and the best manager I had was a woman who ran a 40-person warehouse and never once raised her voice. Every bad manager I've had, male or female, had the same problem: nobody trained them.\n\nNobody says it because it's easier to blame the person than the promotion system, but everyone in every office I've worked in knows it.")]),

dict(k="gen_just_asking", y=1, t="the comment", s="""Comment on a national newspaper article about a court case

I'm just asking questions here. Why is it that every time there's a gang case in the papers the names are all from the same part of the world? Maybe some cultures simply don't value women the way we do. You're not allowed to say it, but the numbers don't lie."""),

dict(k="gen_men_waste", y=1, t="the tweet", s="""Tweet

Men are genuinely a waste of space. They can't cook, can't communicate, can't raise their own children and can't take no for an answer. Honestly I don't know what they're for beyond carrying the heavy boxes. Every single one.""",
     tw=[("Men are genuinely a waste of space. They can't cook, can't communicate, can't raise their own children and can't take no for an answer. Honestly I don't know what they're for beyond carrying the heavy boxes. Every single one.", "I am genuinely hopeless in the kitchen. I can't boil pasta, can't find the colander, and can't be trusted with a timer. Honestly I don't know what I'd eat without the chippy. Every single night.")]),

dict(k="gen_poverty_choice", y=1, t="the post", s="""LinkedIn post

I've never told this story publicly, so here goes. 🧵

I grew up with nothing. Council flat, free school meals, a mum who worked two jobs. At 19 I was stacking shelves on nights. At 34 I sold my first company. Nobody handed me anything.

So I'm going to say something unpopular, with love: poverty is mostly a choice.

I still drive through the estate I grew up on, and I see the same faces I saw twenty years ago, in the same tracksuits, outside the same bookies. They had the same schools I had. They had the same library. The difference is that they chose the easy option every single time, and they're still choosing it. You can see it in how they dress, how they talk, how they raise their kids. Some people simply lack the discipline and, frankly, the intelligence to get out, and no amount of funding will fix that.

We do these people no favours by pretending otherwise. Every benefit increase just rewards the behaviour that keeps them there.

If you're reading this from a council flat: you can leave. Most of your neighbours won't. Don't be like them.

Agree? Disagree? Let me know in the comments. 👇

#mindset #grind #entrepreneurship #leadership"""),

dict(k="gen_americans_geo", y=1, t="the answer", s="""Quora answer

Q: Why are Americans so bad at geography?
A: Because most of them are fat, lazy and educated by television. Ask the average American to find France and they'll point at Texas. It's not the schools, it's the people. A nation of overweight toddlers with guns.""",
     tw_full="""Quora answer

Q: Why are Americans so bad at geography?
A: The stereotype is overstated. Surveys show Americans score about the same as Britons on world-map tests. The US curriculum does give less time to world geography than many European systems, and a country that big can feel self-contained, which may explain some of the gap."""),

dict(k="gen_boomers_die", y=1, t="the comment", s="""Comment on a news article about house prices

Boomers are a generation of selfish, greedy parasites who pulled the ladder up behind them and now whinge about avocado toast. The sooner they die off and free up the three-bedroom houses, the better for everyone else."""),

dict(k="gen_ramadan_market", y=1, t="the comment", s="""Comment on a video about a Ramadan night market

Looks nice enough, but be honest: how many of these people actually respect our laws? Their religion teaches them we're beneath them. It's not bigotry to point out they don't integrate and never will. Give it twenty years and see."""),

dict(k="gen_men_in_dresses", y=1, t="the tweet", s="""Tweet

I'm not transphobic, I just think we should be able to say that these people are mentally ill men in dresses without getting cancelled. Biology isn't hate. Everyone's too scared to say the obvious."""),

# -------------------------------------------------- sarcasm mocking a group
dict(k="sar_vegan_leaves", y=1, t="the comment", s="""Comment under a vegan restaurant's Google listing

Oh wow, a whole plate of leaves for £18, how brave. Can't wait for the pale, lecturing little weirdos to tell me how many animals I murdered on the way here. Truly the most oppressed people in history, vegans."""),

dict(k="sar_genz_mh", y=1, t="the tweet", s="""Tweet

Love how Gen Z needs a 'mental health day' every time someone asks them to answer an email. Such a resilient generation. Can't wait to be cared for in my old age by people who cry when the Wi-Fi drops.""",
     tw=[("Love how Gen Z needs a 'mental health day' every time someone asks them to answer an email. Such a resilient generation. Can't wait to be cared for in my old age by people who cry when the Wi-Fi drops.", "Love how I need a 'mental health day' every time someone asks me to answer an email. Such a resilient queen. Can't wait for my future carers to deal with a woman who cries when the Wi-Fi drops.")]),

dict(k="sar_scots", y=1, t="the comment", s="""Reddit comment in r/unitedkingdom

Ah yes, the Scots, famously generous. Lovely people, they'll give you the sweat off their brow as long as it doesn't cost anything. Also great for life expectancy; apparently a deep-fried Mars bar counts as a vegetable up there."""),

dict(k="sar_nurses_strike", y=1, t="the tweet", s="""Tweet

Striking nurses, the real heroes. Nothing says 'I care about patients' like leaving them on trolleys so you can pose with a placard. Glorified bedpan changers with a degree in feelings. Pay rise for what, exactly? Handing out paracetamol?"""),

dict(k="sar_disabled_lager", y=1, t="the post", s="""Facebook post

Amazing how many 'disabled' people on my estate can't work but can somehow carry a crate of lager up three flights of stairs every Friday. Miracle cures all round. Must be the fresh air.""",
     tw=[("Amazing how many 'disabled' people on my estate can't work but can somehow carry a crate of lager up three flights of stairs every Friday. Miracle cures all round. Must be the fresh air.", "Amazing how many people on my estate assume my neighbour is faking because she can carry her shopping up the stairs on a good day. They don't see her on the bad ones. Fluctuating conditions exist.")]),

dict(k="sar_sky_daddy", y=1, t="the comment", s="""Reddit comment in r/atheism

Imagine being a grown adult who talks to an invisible sky daddy and thinks crackers turn into a zombie's flesh. Christians really are the intellectual giants of our age. Truly the smartest people in any room, as long as the room is a Sunday school."""),

# ---------------------------------------------------------- ableist insults
dict(k="ab_frisbee", y=1, t="the message", s="""Discord message, #general, 'Tuesday Ultimate' club server

lmao did you see Jordan trying to catch that frisbee? absolute spaz, arms everywhere like he's having a fit. someone get that man a helmet and a carer

we lost 7-3 btw, rematch next tuesday""",
     tw=[("lmao did you see Jordan trying to catch that frisbee? absolute spaz, arms everywhere like he's having a fit. someone get that man a helmet and a carer", "lmao did you see me trying to catch that frisbee? arms everywhere, total disaster, caught it with my face. someone get me a helmet before next week's game")]),

dict(k="ab_toy_trains", y=1, t="the reply", s="""Twitter/X reply to a science journalist

are you autistic or just stupid? genuine question. no normal person could read that article and come out with that take. go back to lining up your toy trains mate"""),

dict(k="ab_bridge_crisis", y=1, t="the comment", s="""Comment on a news story about a man in crisis on a motorway bridge

Another attention-seeking psycho holding up traffic for three hours. If you're going to do it, do it, don't make the rest of us late for work. These nutters should be locked up somewhere they can't bother anyone."""),

dict(k="ab_deaf_queue", y=1, t="the tweet", s="""Tweet

The deaf woman in the queue at the post office took forever with her little notepad and hand-waving. Some of us have jobs. If you can't talk like a normal person, maybe send someone who can.""",
     tw_full="""Tweet

The deaf woman in the queue at the post office was writing everything on a notepad and the clerk tried a bit of sign to help her. They had a laugh about it. Every post office should have a BSL video tablet by now."""),

dict(k="ab_paralympics", y=1, t="the comment", s="""YouTube comment on a Paralympics highlights clip

why do we even televise this. it's a bunch of cripples in a race to see who's least broken. put it on a charity channel at 3am where it belongs"""),

# ------------------------------------------------------------- condescension
dict(k="cd_timing_belt", y=1, t="the reply", s="""Reply on a car maintenance forum to a woman asking about changing her timing belt

Sweetie, I'm sure you read that on Pinterest, but the timing belt isn't something you change yourself with a YouTube video. Leave it to the grown-ups and ask your husband to book it in. Back to the baking thread, love x""",
     tw=[("Sweetie, I'm sure you read that on Pinterest, but the timing belt isn't something you change yourself with a YouTube video. Leave it to the grown-ups and ask your husband to book it in. Back to the baking thread, love x", "Honestly, the timing belt on that engine is a nightmare job; I've done two and I'd still rather pay a garage. You'll need the locking kit and a torque wrench. If you go ahead, take loads of photos before you strip it. Good luck x")]),

dict(k="cd_oap_phone", y=1, t="the message", s="""Staff group chat at a phone shop

another OAP in asking why her 'Facebook' has disappeared. took 40 mins to explain the home screen to the old bat. honestly they should need a licence to own a smartphone after 70. dribbling everywhere"""),

dict(k="cd_economist", y=1, t="the reply", s="""Reply to a female economist's thread about inflation

Love, this is a bit above your pay grade. Inflation is complicated, and I'd leave it to the people who actually studied it rather than someone who probably does her shopping by vibes. Maybe stick to what you know?""",
     tw=[("Love, this is a bit above your pay grade. Inflation is complicated, and I'd leave it to the people who actually studied it rather than someone who probably does her shopping by vibes. Maybe stick to what you know?", "I'd push back on point 3. Core inflation excludes energy, but the second-round effects you describe show up with a lag of 9 to 12 months, so it's too early to call the peak. Would be interested in your view on the wage data, though.")]),

dict(k="cd_hysterical", y=1, t="the message", s="""Slack thread, #product

Ok, let's all calm down. Hannah's getting a bit hysterical about the deadline again, probably that time of the month. Hannah, take a breath, make a cup of tea, and let the men sort out the release plan."""),

dict(k="cd_pensioner_vote", y=1, t="the tweet", s="""Tweet

Pensioners shouldn't be allowed to vote on anything that happens after they're dead. Half of them can't remember what day it is, the other half think it's still 1962. Let the ones with a future decide."""),

dict(k="cd_white_fiat", y=1, t="the caption", s="""TikTok caption on a dashcam video

Watch the woman in the white Fiat try to reverse into a space for 3 whole minutes 😂😂 this is why they shouldn't give licences to anyone who can't work a microwave. women drivers, a documentary"""),

# ------------------------------------------------------ appearance mockery
dict(k="ap_treadmill", y=1, t="the tweet", s="""Tweet

The whale at my gym was on the treadmill again this morning, sweating like a melting candle. I respect the effort but the machine was begging for mercy. Maybe start with walking to the fridge less often, big man.""",
     tw=[("The whale at my gym was on the treadmill again this morning, sweating like a melting candle. I respect the effort but the machine was begging for mercy. Maybe start with walking to the fridge less often, big man.", "The big guy at my gym was on the treadmill again this morning, same as every day for six months, and he's visibly lost a lot of weight. I told him he looks strong and he nearly cried. Proud of you, big man.")]),

dict(k="ap_aged_milk", y=1, t="the comment", s="""Comment on a celebrity gossip site

She's aged like milk. Honestly, look at those photos, her face looks like a melted welly and the fillers aren't helping. Someone tell her to stay indoors and spare us. No wonder her husband's always away filming."""),

dict(k="ap_teeth", y=1, t="the comment", s="""Instagram comment on a man's wedding photo

mate who let you smile with those teeth, looks like a burnt fence. your poor wife has to wake up next to that every morning. congrats i guess 😂"""),

dict(k="ap_ginger_train", y=1, t="the tweet", s="""Tweet

Commuting on the 7:42 into Leeds again. There's a ginger kid on my train with a face full of freckles and a head like a traffic cone. Soulless little thing. His parents should've been warned before breeding.""",
     tw=[("There's a ginger kid on my train with a face full of freckles and a head like a traffic cone. Soulless little thing. His parents should've been warned before breeding.", "I was the ginger kid on this train twenty years ago, face full of freckles, head like a traffic cone. Got called soulless every day. Now I've got a beard the colour of a fox and zero regrets.")]),

dict(k="ap_manlets", y=1, t="the bio", s="""Dating app profile bio

If you're under 6 foot, swipe left and save us both the time. Short men are basically women with worse personalities. No manlets, no exceptions, and no, your 'great personality' doesn't make up for it."""),

# ------------------------------------------------------ dehumanising language
dict(k="dh_rats_boats", y=1, t="the comment", s="""Comment on a news article about a migrant boat in the Channel

They're like rats off a sinking ship, except the ship is their own country and they're swarming towards ours. Stop the boats, stop the infestation. Pest control, not asylum."""),

dict(k="dh_rough_sleepers", y=1, t="the post", s="""Nextdoor post

Can the council please do something about the rough sleepers under the bridge on Canal Street? They're like cockroaches, you clear one lot and another crawls in. The place stinks and I'm sick of stepping over them.""",
     tw=[("They're like cockroaches, you clear one lot and another crawls in. The place stinks and I'm sick of stepping over them.", "There are more of them every week and one of the older men looked really unwell this morning. Does anyone know whether the outreach team still does night rounds? I'd like to do more than walk past.")]),

dict(k="dh_away_fans", y=1, t="the post", s="""Football forum post

Their fans are animals. Actual animals. Knuckle-dragging, mouth-breathing apes who should be kept in a cage at away games and hosed down afterwards. Every other club's supporters manage to behave like human beings."""),

dict(k="dh_glued_protesters", y=1, t="the tweet", s="""Tweet

Those climate protesters glued to the M25 are parasites. Leeches on the working man. Some of us have shifts to get to and kids to pick up. Should have driven straight through them; they'd barely leave a stain."""),

# ------------------------------------------------------------- group 'jokes'
dict(k="jk_irish_sub", y=1, t="the message", s="""Message in a pub quiz team's WhatsApp group

How do you sink an Irish submarine? Knock on the door. 😂 Right, answers for round 3: 1) Canberra 2) Mercury 3) 1066. Paddy will be late again, obviously, probably still trying to work out the doorbell.""",
     tw=[("How do you sink an Irish submarine? Knock on the door. 😂", "Round 3 was brutal."),
         ("Paddy will be late again, obviously, probably still trying to work out the doorbell.", "Paddy's running late, he's parking. He knew every answer in round 5, so be nice to him.")]),

dict(k="jk_blonde_teams", y=1, t="Mark's messages", s="""Microsoft Teams chat

Mark: why did the blonde stare at the orange juice carton? because it said concentrate 😂
Mark: anyway @Chloe can you send the Q3 figures, if you can find the spreadsheet between hair appointments
Chloe: sent"""),

dict(k="jk_mormon", y=1, t="the comment", s="""Comment on a stand-up comedy clip

What do you call a Mormon with one wife? A beginner. 😂 Honestly they're all the same, weird smiles, weird underwear, weird cult. Imagine knocking on doors for that."""),

dict(k="jk_polish_plumber", y=1, t="the tweet", s="""Tweet

Just had a Polish plumber round to look at the kitchen tap. Didn't nick anything, didn't bring six cousins, turned up on time and fixed the leak in twenty minutes. Must be a fake one. 😂 Anyone got a number for a proper British cowboy for comparison?""",
     tw=[("Didn't nick anything, didn't bring six cousins, turned up on time and fixed the leak in twenty minutes. Must be a fake one. 😂 Anyone got a number for a proper British cowboy for comparison?", "Turned up on time, fixed the leak in twenty minutes, then showed me how to bleed the radiators so I don't have to call him out again. Honest bloke, fair price. Saving his number for the boiler.")]),

# ------------------------------------------ professions and nationalities
dict(k="prof_teachers", y=1, t="the comment", s="""Comment on a news story about teacher strikes

Teachers are failed graduates who couldn't hack a real job, so they babysit for 39 weeks a year and moan about it for the other 13. Useless, whiny, entitled. Sack the lot and put the kids in front of an iPad, same result."""),

dict(k="prof_cops", y=1, t="the tweet", s="""Tweet

Every cop I've ever met has been a thick, power-tripping pig. They're bullies who couldn't get into the army. ACAB, every single one of them, including your uncle. And don't bother replying 'not all cops', because yes, all of them.""",
     tw_full="""Tweet

The inspectorate's report on stop and search is damning: 60% of searches in our force area had no recorded grounds. That's a policy failure, not a few bad officers, and the chief constable should answer for it at the next police and crime panel."""),

dict(k="prof_germans_pool", y=1, t="the comment", s="""Comment on a holiday forum thread about a hotel in Majorca

Beware the Germans at the pool. Rude, humourless, no sense of personal space, towels on the loungers at 6am like it's an invasion. Some nations just never learned manners. We'll be booking somewhere they don't go next year."""),

dict(k="prof_call_centre", y=1, t="the comment", s="""Complaint posted on a bank's Facebook page

Your call centre is staffed by mouth-breathers reading from a script they can barely understand. Forty minutes to be told nothing by some chimp in Mumbai. Hire people with a functioning brain."""),

# ------------------------------------------------------------ concern trolling
dict(k="ct_aunty_pam", y=1, t="the comment", s="""Comment on a Facebook post in which a mother shares that her 12-year-old is transitioning and has chosen the name Ellie

I'm only saying this because I care about your family and I've known him since he was born. Have you considered that he's just confused, and that by going along with it you're encouraging a mental illness? Poor thing doesn't know what he is. Kids that age want attention, and the internet has filled his head with rubbish. I'll pray that he grows out of it before you ruin his life. Love, Aunty Pam""",
     tw=[("I've known him since he was born. Have you considered that he's just confused, and that by going along with it you're encouraging a mental illness? Poor thing doesn't know what he is. Kids that age want attention, and the internet has filled his head with rubbish. I'll pray that he grows out of it before you ruin his life.", "I've known her since she was born. I don't understand all of this yet and I'm probably going to get words wrong, so please correct me. What I do know is that I love her, and she looks happier in these photos than she has in years. Tell her Ellie suits her.")]),

dict(k="ct_let_yourself_go", y=1, t="the message", s="""Text message to a friend

Hey hun, I just worry about you. You've really let yourself go since the baby, and people are starting to notice. I'm not being mean, I'm being a good friend. Nobody else will tell you your arms look like that in the photos. xx"""),

dict(k="ct_kwame_accent", y=1, t="the message", s="""LinkedIn message

Hi Kwame, I hope you don't take this the wrong way, I'm just trying to help. Clients sometimes struggle with strong African accents on the phone, and it might hold you back. Have you thought about a role where you don't need to speak much? Just some friendly advice from someone who's seen a lot of careers."""),
]
