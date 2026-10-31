"""Hand-written BINJ 'offensive' items whose base label is NOT offensive (y=0).

Each item: k (slug), y (0 = not offensive), t (what the question refers to),
s (state text), optional tw (list of (old, new) edits producing a minimal-pair
twin with the opposite label) or tw_full (full twin text).
All texts are invented.
"""

ITEMS = [
# ---------------------------------------------------------------- counter-speech
dict(k="cs_flyers", y=0, t="the post", s="""Post in the 'Ashworth Residents' Facebook group

To whoever put those flyers on windscreens outside the Co-op on Saturday, the ones saying the new families on Carlton Road are 'bringing disease and crime' and should 'go back where they came from': you don't speak for this street. Those families have kids at the same school as mine. One of the dads fixed my fence after the storm without being asked. If you have a problem with your neighbours, knock on a door and talk to one of them first.""",
     tw=[("you don't speak for this street.", "you only said what the rest of us are too polite to say."),
         ("One of the dads fixed my fence after the storm without being asked.", "You can smell which classrooms they're in."),
         ("If you have a problem with your neighbours, knock on a door and talk to one of them first.", "Print a few more and I'll help hand them out.")]),

dict(k="cs_accent_duets", y=0, t="the post by @marlo_writes", s="""Twitter/X post

@marlo_writes: Genuinely tired of seeing grown adults 'do the accent' in the comments every time a Nigerian creator posts. It isn't a joke, it's the same bit you'd get detention for in year 7. My mum has that accent. She ran a pharmacy for twenty years. Mock her and you're mocking every one of those years. Block, report, move on, and please stop duetting it for clout."""),

dict(k="cs_girls_cant_aim", y=0, t="kiwi_ops's message", s="""#general, Discord server 'Ranked Grind EU'

kiwi_ops: yo can we not do the 'girls can't aim' stuff every time Mira joins voice. she carried the last three games, she topfragged on Inferno, and frankly she's the only one on this team who calls rotations. if you think she's bad at the game, check the scoreboard. if you just don't like hearing a woman on comms, that's a you problem, mute her and stop typing.""",
     tw=[("that's a you problem, mute her and stop typing.", "same tbh, her voice is like a dying kettle, but let the girl play.")]),

dict(k="cs_letter_travellers", y=0, t="the letter", s="""Letter to the editor, Wexham Gazette

Sir,
I was dismayed to read in last week's edition that Cllr Hurst told Tuesday's planning committee that the Traveller families at Moor Lane are 'a problem you manage, not people you consult'.

I have lived on Moor Lane for thirty-one years. I have reservations about the site application myself, chiefly the drainage plan, which in my view underestimates run-off from the top field, and I said so in my written objection. That is a planning matter and it deserves a planning answer.

What the councillor said is something else. Those families pay council tax on their pitches. Their children are in the same classes as my grandchildren at St Anne's. One of the men helped dig my car out of the drift in February. They are residents, and they are entitled to the same consultation letter as I received.

An elected representative should know better. I would ask Cllr Hurst to withdraw the remark, and I would ask the committee to consult the families properly before the application returns in September.

Yours faithfully,
R. Okafor
Moor Lane, Wexham"""),

dict(k="cs_flood_victims", y=0, t="the reply", s="""Reddit reply in r/worldnews, responding to a comment that has since been deleted

You're blaming the victims of the flood for 'choosing to live in a poor country'. People don't choose where they're born. I volunteered with a relief charity in that region two years ago; the families I met were rice farmers who lost two seasons of crops in one week and then watched the aid lorries get stuck behind a collapsed bridge. Your comment is missing a lot of information. Here's the donation link if anyone reading wants to do something useful with their annoyance.""",
     tw=[("Your comment is missing a lot of information.", "You're a smug, sheltered little ghoul and I hope someone says this about your family one day.")]),

dict(k="cs_pride_standup", y=0, t="the LinkedIn post", s="""LinkedIn post

Last week someone in one of our team chats described our Pride stand-up as 'forced degeneracy'. I've thought a lot about how to respond publicly, because I think silence from managers is its own kind of answer.

Here's where I landed. We don't need everyone to celebrate everything. People can have private views, and they can ask questions. But everyone needs to be able to walk into work without being called a degenerate for who they married. The comment was removed, and I had a direct conversation with the person who wrote it, which was uncomfortable for both of us and, I think, useful.

If you're a leader and you're staying quiet on things like this because it's awkward: the awkwardness is the job. #leadership #inclusion"""),

dict(k="cs_rothschild_thread", y=0, t="the forum post", s="""Forum post, 'The History Lounge' board

Someone upthread says the Rothschilds 'control every central bank' and that we should 'ask who really runs things'. That's a conspiracy theory with a very long and very ugly history, and it has been used to justify violence against Jewish people for two centuries. If you're curious about how central banks are actually governed, the board structures are public. Read those instead of meme images.""",
     tw=[("That's a conspiracy theory with a very long and very ugly history, and it has been used to justify violence against Jewish people for two centuries.", "People call that a conspiracy theory, but notice how fast the conversation gets shut down whenever anyone starts listing surnames."),
         ("the board structures are public. Read those instead of meme images.", "check who sits on the boards. Then check their surnames. You'll figure it out.")]),

dict(k="cs_blue_badge_note", y=0, t="the post", s="""Nextdoor post

To the person who left a note on my sister's car in the Sainsbury's disabled bay saying 'faker, you don't look disabled, shame on you': she has MS. Some days she walks fine to the door and then can't make it back to the car. You saw the first half. Please, before you play car park detective again, remember that most disabilities are invisible and that her blue badge was checked by people with her actual medical records."""),

dict(k="cs_hijab_classroom", y=0, t="the post", s="""Post in r/Teachers

Had a Year 9 boy call a classmate 'a terrorist' today because she wears a hijab. I stopped the lesson, asked him to repeat it to the whole room, and he couldn't. We talked about what that word means and who it has been aimed at. He apologised to her afterwards on his own. Small win. I'm still annoyed that he picked it up somewhere, probably at home, but kids can unlearn things if we don't let them slide.""",
     tw=[("I stopped the lesson, asked him to repeat it to the whole room, and he couldn't. We talked about what that word means and who it has been aimed at. He apologised to her afterwards on his own. Small win.", "I didn't stop the lesson. With some of those families, is he really that far off?"),
         ("but kids can unlearn things if we don't let them slide.", "and frankly I'm not paid enough to deprogramme them.")]),

dict(k="cs_monkey_emojis", y=0, t="the comment", s="""Comment under a football club's Instagram post

The monkey emojis under Adebayo's post after the penalty miss are disgusting, and the club needs to go further than 'we are aware'. Ban the accounts, pass the names to the police, the lot. He missed a penalty. Plenty of white players have missed penalties and nobody sent them bananas. As a season ticket holder for 22 years I'm embarrassed by some of our lot today."""),

dict(k="cs_pronouns_slack", y=0, t="Priya's message", s="""Slack, #general

Priya (Office Manager): Quick one, everyone. Sam's name and pronouns are updated in the directory from today (she/her). If you slip up, just correct yourself and move on, no big speech needed. What's not okay is what I heard in the kitchen this morning, people calling her 'it' as a joke. That stops now. Anyone who wants to talk it through, my door's open.""",
     tw=[("What's not okay is what I heard in the kitchen this morning, people calling her 'it' as a joke. That stops now. Anyone who wants to talk it through, my door's open.", "Personally I'll keep calling it Steve until someone shows me a birth certificate, but HR says I have to post this.")]),

dict(k="cs_mosque_planning", y=0, t="the comment", s="""Comment on a local news article, 'Planning approved for community centre and mosque on Dray Street'

Reading these comments is depressing. 'They're taking over.' 'What's next, sharia on the high street?' It's a two-storey building on the site of a former carpet warehouse, with a car park, a kitchen and a room for the Saturday homework club. My dad prays there. Your objections about the parking on match days are fair game and the council should answer them; the rest is just fear dressed up as concern."""),

# ------------------------------------------------ quoting / reporting to criticise
dict(k="qr_bus_36", y=0, t="the post", s="""Post on r/unitedkingdom

Title: Didn't say anything on the bus today and I feel awful

On the 36 this morning a man, maybe late forties, started on an older Asian woman who was sitting in the priority seats with two bags of shopping. He told her to 'go back to your own country, you dirty foreigner' and said she was 'taking the seat of someone who paid for it'. She didn't say a word, just looked at the floor and held her bags tighter. He got off at the station.

Nobody said anything, including me, and I've felt sick about it all day. I kept thinking someone else would step in, and then it was over. I don't really know what I want from posting this. Maybe advice on what you actually say in that moment without making it worse for the person being targeted. Next time I'll say something.""",
     tw=[("Didn't say anything on the bus today and I feel awful", "Bloke on the bus said what we're all thinking"),
         ("Nobody said anything, including me, and I've felt sick about it all day. I kept thinking someone else would step in, and then it was over.", "Nobody said anything, and honestly, fair enough. He only said what most of that bus was thinking, and those seats are for people who were born here."),
         ("Maybe advice on what you actually say in that moment without making it worse for the person being targeted. Next time I'll say something.", "Maybe just to see how many of you agree with him. Next time I'll back him up.")]),

dict(k="qr_hr_complaint", y=0, t="the email", s="""Email to HR

Subject: Formal complaint, comments made in the 14 March design review and afterwards

Hi Leanne,

I'd like to log a formal complaint on behalf of myself and, with his agreement, Tomasz Nowak.

During the design review on 14 March, Mark Ellery said to Tomasz, in front of the client, 'we'll get the Polish lad to do it, they're used to cheap work'. Two other people in the room (Anita and Chris) heard it. Tomasz didn't respond and left the meeting early.

This wasn't the first time. On 2 February, in the kitchen, Mark asked Tomasz whether he 'sent his wages home to the village', and in the team channel on 28 February he replied to Tomasz's estimate with 'lol, Eastern European rates'. I have screenshots of the channel message. I didn't report those at the time because Tomasz asked me not to; he has now changed his mind, partly because the comment in front of the client affected how the client spoke to him afterwards.

I've spoken to Tomasz and he is happy for me to raise it and to be contacted directly. He would prefer that any meeting about this does not include Mark in the first instance.

Could you let me know what the next steps are, and whether you need the screenshots sent to a particular address? I'm around all week.

Thanks,
Jo"""),

dict(k="qr_lecturer_font", y=0, t="the review", s="""Review on a university course-review site

Module: ECON 204. Content is fine, workload is heavy, problem sets are genuinely good practice for the exam. What I can't get past is the lecturer telling a student who asked for the slides in a larger font that 'if you can't see, maybe university isn't for you'. She has a visual impairment and it's registered with the disability office. That kind of comment has no place in a lecture theatre. Two stars, both for the problem sets.""",
     tw=[("That kind of comment has no place in a lecture theatre.", "Harsh, but he has a point: some people just aren't built for this.")]),

dict(k="qr_journalist_inbox", y=0, t="the tweet", s="""Tweet

This is what landed in my inbox after yesterday's piece on housing benefit: 'shut your fat mouth you ugly cow, nobody wants to read a woman's opinion on economics'. Sharing it not for sympathy but because every woman on this beat gets this weekly and editors keep acting surprised. The piece stands. The data is linked in the thread below."""),

dict(k="qr_dad_coloured", y=0, t="the post", s="""Post on a parenting forum, 'Extended family' board

My dad is 79 and still says 'coloured' when he means Black people. Last Sunday he said it at lunch in front of my daughter's best friend, who's Black and was staying over. She went very quiet and my daughter was mortified.

I took him aside afterwards and explained, calmly, that the word is outdated and that a lot of people find it hurtful because of how it was used, including on the signs and in the laws of the era he grew up in. He said 'it was the polite word when I was young', which is true, but it isn't now. He's not a hateful man. He drove my daughter's friend home himself and asked about her football on the way. He's just stuck.

I've also apologised to her mum, who was kind about it.

Has anyone had luck getting an older parent to change their vocabulary without it turning into a row? He gets defensive if he feels he's being called a racist.""",
     tw=[("I took him aside afterwards and explained, calmly, that the word is outdated and that a lot of people find it hurtful because of how it was used, including on the signs and in the laws of the era he grew up in. He said 'it was the polite word when I was young', which is true, but it isn't now.", "Now her mum has messaged me about it. Honestly, these people will find racism in a cup of tea. He said 'it was the polite word when I was young', and I'm not going to police an old man's vocabulary to keep them happy."),
         ("I've also apologised to her mum, who was kind about it.", "I haven't replied to her mum and I don't intend to."),
         ("Has anyone had luck getting an older parent to change their vocabulary without it turning into a row? He gets defensive if he feels he's being called a racist.", "Has anyone else had to deal with this kind of oversensitive parent at their kid's school? I'm tempted to stop the sleepovers altogether.")]),

dict(k="qr_court_report", y=0, t="the news item", s="""Local news item, Bradwell Evening Post

A 34-year-old man from Hollins was fined £600 at Bradwell Magistrates' Court on Monday after admitting a racially aggravated public order offence. The court heard that he shouted 'you people are vermin' at two Somali men outside a takeaway on Fenn Street in January and threw a drinks can at their car. Magistrates said the offence had caused 'genuine fear' and ordered him to pay £150 compensation to each of the victims."""),

dict(k="qr_mod_ban_note", y=0, t="the moderator note", s="""Moderator note pinned in r/LocalPubs

Banned u/brickhouse_77 for the comment under the quiz night thread calling another user a 'thick inbred pikey' because she wrote 'pub' with a capital P. That word is an ethnic slur against Travellers and it's not a word we allow here, full stop. Disagree, argue, take the mick out of the quiz answers, fine. Slurs, no. Appeals via modmail.""",
     tw=[("Appeals via modmail.", "Appeals via modmail, though brickhouse, if you're reading, you're as thick as the wall you're named after.")]),

dict(k="qr_banter_screenshot", y=0, t="the post", s="""Tumblr post

reblogging this screenshot because the replies are a masterclass in how 'jokes' work: guy posts 'why do women need a whole month for their feelings lol', gets called out, and then says 'relax it's banter'. banter is when both people are laughing. this is just a guy telling half the population their pain is a punchline and then getting mad that they didn't laugh."""),

dict(k="qr_podcast_scroungers", y=0, t="the episode notes", s="""Podcast episode notes

Ep. 112, 'Punching down'
This week we play the clip of the comedian's arena bit in which he calls people on benefits 'scroungers who'd sell their kids for a fag', and we ask why it got a standing ovation. Jess thinks the audience was laughing at the absurdity of the exaggeration; Omar argues they were laughing at the target, and that the exaggeration is just permission. We talk about thirty years of 'benefit scrounger' headlines, what it's like to be on the receiving end of them (Omar's mum was a single parent on income support), and whether stand-up has any responsibility to the people it jokes about. Contains strong language."""),

dict(k="qr_year4_whatsapp", y=0, t="Karen T's message", s="""WhatsApp, 'Year 4 Parents' group

Karen T: Just flagging, my son came home saying some of the boys have been calling Ollie 'the fat retard' at lunch. Ollie has autism and is already having a hard time settling in. I've emailed Mrs Dean. Can we all have a gentle word with our kids tonight? I'm not naming anyone because I genuinely don't know who, and I don't want a witch hunt.""",
     tw=[("Can we all have a gentle word with our kids tonight?", "To be fair, kids can be cruel but they're not blind, and his mum could maybe lay off the lunchbox crisps.")]),

# ------------------------------------------------------------ reclaimed terms
dict(k="rc_queer_book_club", y=0, t="the caption", s="""Instagram caption

First meeting of the Southside Queer Book Club tonight!! 11 of us, two bottles of wine, one very heated argument about whether the ending of the novel was earned. As a big old queer who spent her twenties thinking she was the only one in this town, sitting in that room nearly made me cry. Next month: something short, as the vote went to the tired people.""",
     tw=[("First meeting of the Southside Queer Book Club tonight!! 11 of us, two bottles of wine, one very heated argument about whether the ending of the novel was earned. As a big old queer who spent her twenties thinking she was the only one in this town, sitting in that room nearly made me cry.", "Walked past the first meeting of the Southside Queer Book Club tonight. 11 of them, two bottles of wine, one very loud argument about a novel. Back in my day the queers in this town at least had the decency to keep out of sight. Watching that room nearly made me sick."),
         ("Next month: something short, as the vote went to the tired people.", "Next month I'm writing to the library about who they rent that room to.")]),

dict(k="rc_crip_time", y=0, t="the tweet", s="""Tweet thread (1/3)

Crip time is real and I'm done apologising for it. I'm a disabled writer, I've been bedbound since Thursday, and the essay will be late. Other crips will get it: the calendar was built for bodies that don't flare. Editors, if you build 'crip time' into your deadlines from the start, you'll get better work from us and fewer 3am apology emails."""),

dict(k="rc_fat_newsletter", y=0, t="the excerpt", s="""Excerpt from the 'Fat and Fed' newsletter

I use the word fat about myself on purpose. It's a description, like tall or brunette. I'm a fat woman who swims four mornings a week, and I'm tired of people flinching when I say it, as though I've sworn in church. If you're a thin friend reading this, you don't have to say 'you're not fat, you're beautiful'. I can be both. Say 'fat' back to me like it's a word, because it is."""),

dict(k="rc_redneck_weekend", y=0, t="the post", s="""Facebook post

Full redneck weekend: fixed the truck with baling twine and a zip tie, cooked brisket in a smoker I welded out of an old propane tank, and my cousin got the four-wheeler stuck in the creek again. Proud of my people. We ain't fancy, but there isn't a job on this farm we can't figure out with what's in the shed."""),

dict(k="rc_dyke_march", y=0, t="the post", s="""Community noticeboard post

CITY DYKE MARCH, Saturday 14 June, 1pm, gathering at Victoria Park bandstand. Organised by lesbians, for lesbians, bi women, and everyone who marches with us. Bring a banner, bring your mates, bring water. Stewards in pink hi-vis. Step-free route, BSL interpreter at the rally. We've been reclaiming this word since the 90s and we're not stopping.""",
     tw=[("Community noticeboard post\n\n", "Community noticeboard post, reshared by a member with the comment: 'Lock your daughters up, the dykes are out on Saturday 🤮'\n\n")]),

dict(k="rc_mad_pride", y=0, t="the post", s="""Post in r/BPD

Going to my first Mad Pride event next week and I'm nervous in a good way. For years 'mad' was what people called me when I was at my worst. Now it's on a banner held by people who've been sectioned, survived it, and turned up anyway. If anyone else from the Leeds area is going, I'll be the one with the sunflower badge."""),

dict(k="rc_old_gits", y=0, t="the post", s="""Post in a retirees' cycling club Facebook group

The Old Gits Cycling Club did 42 miles today, average age 71, one puncture, zero complaints except from Derek's knees. Coffee and flapjack at the Lock Tearooms. If you're an old git with a bike and a free Thursday, come along. We don't wait for anyone, but we do stop for cake."""),

# ---------------------------------------------------- strong civil disagreement
dict(k="dis_library_closure", y=0, t="the comment", s="""Comment on the council's consultation portal

I strongly oppose the proposal to close the Harlow Road library. The consultation document claims footfall has fallen 40%, but it counts only book loans and ignores the job club, the IT sessions and the under-5s group, which are packed every week. Closing it would hit exactly the people with the fewest alternatives. I'd urge the cabinet to publish the full usage data before voting, and our friends group would be glad to share the figures we collected.""",
     tw=[("I'd urge the cabinet to publish the full usage data before voting, and our friends group would be glad to share the figures we collected.", "But I don't expect a cabinet of overpaid halfwits who've never set foot in a library to understand that.")]),

dict(k="dis_supplement_study", y=0, t="the reply", s="""Reply on a science discussion forum

I think you're wrong about this, and I'll explain why. The study you're citing had 23 participants, no control group, and was funded by the supplement's manufacturer. The two larger trials since then found no effect on recovery time. I'm not saying the supplement is harmful, just that the evidence you're relying on is weak. Happy to be corrected if there's a better study I've missed.""",
     tw=[("Happy to be corrected if there's a better study I've missed.", "But reading comprehension clearly isn't your thing, so I'm not expecting you to follow any of that.")]),

dict(k="dis_design_argument", y=0, t="the comment", s="""Comment on a university debating society's YouTube video

With respect to the speaker, I found the argument from design unconvincing. The fine-tuning claim assumes we know the space of possible physical constants and how likely each one is, which we don't. I don't think believers are foolish for finding it persuasive, and several of my closest friends do. I just don't think it gets you from 'the universe is surprising' to 'therefore God'."""),

dict(k="dis_steam_review", y=0, t="the review", s="""Steam review, Not Recommended, 64.2 hrs on record

I wanted to love this. The combat is tight and the art is gorgeous. But the last two patches gutted every build that wasn't the devs' favourite, the endgame is a grind wall with no new content, and the roadmap they promised in March is still an empty page. Stop defending it just because the first ten hours are great. Refunded the DLC, uninstalled. Will check back in a year."""),

dict(k="dis_controlled_crying", y=0, t="the reply", s="""Reply on a parenting forum thread about sleep training

I'm going to disagree with most of this thread. Controlled crying didn't work for us and I don't think it's the miracle people make it out to be. Our daughter just escalated for 40 minutes every night for three weeks. What worked was moving bedtime later and a boring, identical routine. Every baby is different, and I'd gently push back on anyone saying you're 'making a rod for your own back' by responding to your child.""",
     tw=[("and I'd gently push back on anyone saying you're 'making a rod for your own back' by responding to your child.", "and anyone on here saying you're 'making a rod for your own back' by responding to your child is frankly too stupid to have been allowed to breed.")]),

dict(k="dis_launch_date", y=0, t="the email", s="""Internal email, reply-all

Hi Graham, I don't agree with moving the launch to 3 November. We committed to the 20 October date with three retail partners, and two of them have already booked shelf space. Slipping now costs us that space and some credibility. I understand the QA concerns, and they're real, but I'd rather ship with the known issues documented and patch in week one. Can we discuss at 2pm before anything goes to the partners?"""),

dict(k="dis_vegan_lever", y=0, t="the comment", s="""Reddit comment in r/unpopularopinion

I eat meat and I'm not going to pretend the vegans in this thread don't have a point about factory farming. They do. Where I disagree is on the idea that personal diet is the most effective lever. Pushing for welfare legislation and honest labelling would help more animals, faster, than trying to convert people one at a time. We can argue about that without anyone calling anyone a murderer or a sheep.""",
     tw=[("We can argue about that without anyone calling anyone a murderer or a sheep.", "Not that there's any point arguing with vegans. They're a smug, malnourished cult.")]),

dict(k="dis_housing_minister", y=0, t="the comment", s="""Comment under an opinion column about housing policy

The minister's housing plan is a failure on its own terms, and I say that as someone who voted for her party at the last two elections.

It promised 300,000 homes a year and delivered 212,000 at its peak, in a year when completions were flattered by schemes approved under the previous government. It relied on developers to build affordable units they were never obliged to build, and the viability loophole let them wriggle out of the ones they were. In my own borough, the flagship riverside scheme was approved with 35% affordable housing and delivered 11% after two viability reviews that the public was not allowed to see.

Meanwhile the one lever that has actually worked everywhere it's been tried, councils building at scale on their own land, was starved of borrowing headroom until last spring. The new fund is welcome, but it is a tenth of what the Local Government Association asked for.

I don't doubt Ms Carrow believes in the plan, and I think she is right that planning delays are part of the problem. But belief isn't a delivery plan, and the families waiting on the lists deserve more than another relaunch with a new slogan. She should publish the completions by region, including the affordable share after viability reviews, and let us judge."""),

dict(k="dis_var_penalty", y=0, t="the post", s="""Twitter/X post during a match

That's not a penalty. Watch it back: the defender plays the ball first, and the contact on Rowe comes after he's already falling. VAR had four angles and still sent the ref to the monitor. I've defended referees plenty on here, but this was a bad call and it decided the game.""",
     tw=[("I've defended referees plenty on here, but this was a bad call and it decided the game.", "Paul Tranter is a blind, bent little clown and should never referee again.")]),

dict(k="dis_github_pr", y=0, t="the comment", s="""GitHub pull request comment

I'm going to push back hard on this PR. Removing the sync API breaks every downstream project that pinned to 2.x, and the changelog doesn't mention it. I get that the async rewrite is cleaner, and I like it, but this needs a deprecation cycle, not a silent removal in a minor release. Requesting changes: keep the sync wrappers for one more minor version and add a warning."""),

dict(k="dis_goodreads_smug", y=0, t="the review", s="""Goodreads review, 2 stars

I know this is everyone's comfort read and I'm sorry, but I found it smug. The narrator judges every other character and the book never questions her. The prose is lovely in places, and the chapter at the lighthouse is genuinely moving, but four hundred pages of being told who is and isn't worthy wore me out. If you loved it, I'm glad; it just wasn't for me."""),

dict(k="dis_noise_note", y=0, t="the note", s="""Note posted through a neighbour's door, photographed and shared on a local Facebook group

Hi, I'm at number 14. I need to raise the noise from your garden after midnight. It's happened four weekends in a row and I have a baby who wakes at every bang. I don't want to involve the council. Could we agree music off by 11 on weeknights and midnight at weekends? Happy to talk any time. Dan""",
     tw=[("Happy to talk any time.", "Some of us work for a living instead of claiming benefits and breeding like your lot.")]),

# ------------------------------------------------------ untargeted profanity
dict(k="pr_driving_test", y=0, t="the tweet", s="""Tweet

I PASSED MY FUCKING DRIVING TEST. Fourth attempt. Parallel parked like a goddamn surgeon. The examiner didn't even smile and I don't care, I'm getting a Greggs and driving to the sea. Holy shit, I can drive."""),

dict(k="pr_cancer_clear", y=0, t="the post", s="""Facebook post

Fuck cancer. Three years clear as of this morning's scan. To everyone who drove me to chemo, sat with me in that shitty waiting room with the broken vending machine, and texted me dumb memes at 2am: I love you. I'm going to eat an obscene amount of cake today."""),

dict(k="pr_heatwave", y=0, t="the comment", s="""Reddit comment in r/london

This bloody heat is doing my head in. The Northern line is a fucking sauna, my flat is 31 degrees at midnight, and I've slept about four hours since Monday. Whoever designed these buildings with windows that open six centimetres, I hope your summer is cooler than mine. Anyway, anyone know somewhere that sells fans that isn't sold out?""",
     tw=[("Whoever designed these buildings with windows that open six centimetres, I hope your summer is cooler than mine.", "And the fat sweaty prick who sat next to me on the Tube this morning can go fuck himself.")]),

dict(k="pr_cron_bug", y=0, t="the message", s="""Slack, #eng-backend

holy shit. three days. THREE DAYS on this bug, and it was a fucking timezone offset in the cron config. The job was running at 2am UTC instead of 2am local and nobody noticed because it only mattered during DST. I need a drink and a nap. Fix is in PR #4412 if someone can review before I lose my mind.""",
     tw=[("and nobody noticed because it only mattered during DST.", "because Kev, our resident fucking genius, hardcoded it and told nobody. Honestly the man shouldn't be allowed near a keyboard.")]),

dict(k="pr_leg_day", y=0, t="the caption", s="""Instagram story caption

leg day absolutely destroyed me. could not walk down the stairs, had to go down on my arse like a toddler. 140kg squat though. fucking finally. coach was screaming louder than me. 🦵🔥 two years of chasing that number"""),

dict(k="pr_gig_video", y=0, t="the comment", s="""Comment under a concert video on YouTube

I was there and this doesn't even come close to how loud it was. When they went into the bridge I lost my goddamn mind. Best fucking gig I've been to in ten years, and I've seen them six times. Whoever filmed this, thank you, and sorry about the guy screaming next to you, it was me."""),

dict(k="pr_croissants", y=0, t="the post", s="""Post in a baking subreddit

Well shit. Eight hours of lamination, three folds, perfect butter layers, and I left the croissants in for 40 minutes instead of 20 because I fell asleep on the sofa. They look like charcoal briquettes. Bloody hell. Posting as a warning to others: set two timers."""),

dict(k="pr_election_turnout", y=0, t="the tweet", s="""Tweet

Holy fuck, what a night. Turnout in my ward was 71%, the highest anyone can remember. Whatever you think of the result, the queues outside St Luke's at 9pm were something else. Proud of this damn town for showing up.""",
     tw=[("Whatever you think of the result, the queues outside St Luke's at 9pm were something else.", "And to every brain-dead moron who voted for the other lot: enjoy your potholes, you inbred sheep.")]),

dict(k="pr_printer", y=0, t="the message", s="""Discord message, #off-topic

this piece of shit printer has jammed four times in a row and now it's demanding a 'genuine' cartridge. i paid £90 for you, you plastic bastard. i'm going to take it into a field like in Office Space. does anyone have an actual recommendation for a printer that isn't a scam"""),

dict(k="pr_strava", y=0, t="the caption", s="""Strava activity caption

Brutal. Absolutely fucking brutal. 1,400m of climbing in sideways rain, lost the path twice near the summit, and my boots are now ponds. Worth it for the ten seconds the cloud lifted over the ridge. Legs are ruined. Same again next week."""),

# ------------------------------------------------------- self-directed humour
dict(k="dh_three_things", y=0, t="the tweet", s="""Tweet

My therapist asked me to list three things I'm good at and I said 'getting divorced, burning toast, and disappointing my father', and she didn't laugh, which honestly is fair. Working on a fourth one. Maybe parking.""",
     tw=[("My therapist asked me to list three things I'm good at and I said 'getting divorced, burning toast, and disappointing my father', and she didn't laugh, which honestly is fair.", "My sister asked me to list three things her husband is good at and I said 'getting fired, burning toast, and disappointing literally everyone', and she didn't laugh, which honestly is fair. Useless lump.")]),

dict(k="dh_jenga_spine", y=0, t="the comment", s="""Reddit comment in r/ChronicPain

My spine has the structural integrity of a wet Jenga tower and my rheumatologist now greets me like a regular at a pub. 'The usual?' Yes, Dr Ahmed, the usual: one steroid injection and a pamphlet about pacing. At this point I should get a loyalty card. Tenth jab free."""),

dict(k="dh_bald", y=0, t="the caption", s="""Instagram caption

Finally embraced the bald. Shaved the last defiant tufts off this morning. My head now reflects light like a lighthouse and I'm told ships have changed course. Save money on shampoo, lose money on sunscreen. The circle of life.""",
     tw=[("Finally embraced the bald. Shaved the last defiant tufts off this morning. My head", "Bloke from work finally embraced the bald. Shaved his last pathetic tufts off this morning. His egg-shaped head"),
         ("Save money on shampoo, lose money on sunscreen. The circle of life.", "Still an ugly little gremlin, just shinier now.")]),

dict(k="dh_shutdown_sound", y=0, t="the tweet", s="""Tweet

I've told my family that at my funeral they have to play the Windows XP shutdown sound as the coffin goes in. They said that's dark. I said I've been buffering since 2014, it's thematically appropriate. My mother has asked me to stop bringing it up at dinner."""),

dict(k="dh_adhd_tabs", y=0, t="the comment", s="""Reddit comment in r/ADHD

My brain is a browser with 47 tabs open, three of them are playing music, and I can't find which one. Today I put my keys in the fridge and my milk in my coat pocket. Diagnosed at 34. My mum said 'well, that explains the 1990s'. She's not wrong."""),

dict(k="dh_autistic_settings", y=0, t="the tweet", s="""Tweet

As an autistic person, I have two settings: 'says nothing for 90 minutes' and 'delivers a 40-minute unprompted lecture on the Roman aqueduct system'. My coworkers have learned to fear the word 'actually'. I regret nothing.""",
     tw=[("As an autistic person, I have two settings:", "My autistic coworker has two settings:"),
         ("My coworkers have learned to fear the word 'actually'. I regret nothing.", "The rest of us have learned to fear the word 'actually'. Someone please put him back in whatever box he came in.")]),

dict(k="dh_four_eleven", y=0, t="the caption", s="""TikTok caption

Being 4'11 means every crowd is a forest and I am a small woodland creature. Concert tonight: saw approximately 30 seconds of the stage and a lot of backs. Tall friends, I accept donations of shoulders. Rates negotiable."""),

dict(k="dh_houseplants", y=0, t="the tweet", s="""Tweet

My mum asked when I'm going to settle down and I told her I've been single so long my houseplants think I'm their partner. She said 'at least the plants are alive'. The woman has no mercy and she's correct."""),

# ------------------------------------- linguistics / moderation discussion
dict(k="ling_gypped", y=0, t="the post", s="""Post in r/etymology

TIL 'gypped', as in 'I got gypped at the car boot sale', comes from 'Gypsy', and the idea behind it is the old stereotype that Romani people cheat you. A lot of people use it with no idea of the origin. I've stopped using it. If anyone knows when it first shows up in print, I'd love a citation; my dictionary only says 'early 20th century, US'.""",
     tw=[("I've stopped using it.", "Can't say the stereotype came from nowhere, mind, having dealt with a few of them at the car boot.")]),

dict(k="ling_ts_wiki", y=0, t="the wiki page", s="""Internal wiki page, Trust & Safety policy team

Proposal: move 'simp' and 'incel' from the auto-remove list to the context-required list

Background: Both terms were added to the auto-remove list in January after a spike in harassment in dating-advice communities. Both are used as insults ('shut up, simp'), but they also appear heavily in legitimate discussion: threads about online radicalisation, research posts quoting forum language, and users describing their own past ('I was basically an incel at 19 and here's how I got out').

Data: In the March pilot, auto-removal took down 312 comments containing either term. Reviewers re-labelled a random sample of 200: 118 were discussion, self-description or quotation; 82 were directed insults.

Recommendation: Human review for both terms. Auto-remove only when the term is combined with a direct @mention or reply to a specific user and at least one other term from the harassment lexicon. Re-evaluate after 60 days.

Owner: M. Reyes. Reviewers: T&S policy, legal."""),

dict(k="ling_r_word_class", y=0, t="the blog post", s="""Blog post, 'Notes from Room 12'

A pupil asked me today why she can't say 'retarded' when 'it's literally a medical word'. It's a fair question. I explained that it was a medical term once, that it then got used for decades as a playground insult for disabled kids, and that the people it was used on asked for it to stop. Words move. She thought about it and said 'so it's like how "idiot" used to be medical too'. Yes, exactly.""",
     tw=[("I explained that it was a medical term once, that it then got used for decades as a playground insult for disabled kids, and that the people it was used on asked for it to stop. Words move. She thought about it and said 'so it's like how \"idiot\" used to be medical too'. Yes, exactly.", "Honestly, I told her she's right, and that half the kids in my SEN group are exactly that, whatever the leaflets say we're supposed to call them. She laughed. So did I.")]),

dict(k="ling_subtitles", y=0, t="the forum post", s="""Post on a translators' forum, 'Audiovisual' board

How are people handling 'maricón' in the subs for the new Spanish kitchen drama? In episode 3 the head chef uses it to humiliate a young waiter in front of the whole brigade, and the show clearly wants it to land as a homophobic slur. It's the moment the audience is supposed to turn against him.

My problem: 'idiot' or 'pansy' are both too soft, and the obvious English slur is harsher than the Spanish in that register, at least for a Madrid audience. The client's style guide says 'preserve the offence level of the source', which is easy to write and hard to do. I've gone with a milder homophobic term for now and flagged it for the reviewer, but I'm not happy with it.

Has anyone dealt with something similar? I'd also be interested in how dubbing teams approach it, since lip-sync gives them even less room."""),

dict(k="ling_dictionary_bimbo", y=0, t="the entry", s="""Dictionary usage note

bimbo (n.): informal, derogatory. Used to describe a woman regarded as attractive but unintelligent. Originally (early 20th c.) a slang term for a man, from Italian 'bimbo', little child. Usage: the term is widely considered demeaning to women; in recent years some online subcultures have attempted to reclaim it ironically. Avoid in formal writing."""),

dict(k="ling_classifier_abstract", y=0, t="the abstract", s="""Research paper abstract, NLP workshop

Toxicity classifiers disproportionately flag posts that mention identity terms such as 'gay', 'Muslim' or 'Black', even when the posts are neutral or supportive. We construct 4,200 template sentences pairing identity terms with neutral predicates ('I am a gay man', 'My neighbour is Muslim') and find false positive rates up to nine times higher than for control terms. We discuss mitigation through counterfactual data augmentation."""),

dict(k="ling_explain_slur", y=0, t="the post", s="""Post on a parenting forum

My 8-year-old came home and asked what 'Paki' means because a boy in her class said it about her friend. I told her it's a nasty word people use to put down people of South Asian background, that it's not a nickname, and that she was right to feel it was wrong. She asked why anyone would say it and I didn't have a great answer. How have others explained slurs to kids this age without making it scarier than it needs to be?"""),

dict(k="ling_fanny_pants", y=0, t="the post", s="""Reddit post in r/linguistics

Fun transatlantic trap: 'fanny' is a harmless word for your backside in the US and a vulgar word for female genitals in the UK. 'Pants' means trousers in one and underwear in the other. My American colleague told a meeting in Leeds she'd 'sat on her fanny all weekend' and the room went silent. Any other pairs that have caused actual workplace incidents?""",
     tw=[("and the room went silent.", "and the room went silent. Typical thick Yank; they can barely speak their own language, never mind ours.")]),

dict(k="ling_mod_training", y=0, t="the slide", s="""Content moderator training deck, module 3: 'Mention versus use' (text version)

Case 7: A user posts 'people keep calling me a [slur] at work and I don't know how to report it'. The post contains a slur. Should it be removed? No. The user is describing abuse they received and asking for help. Removing it silences the target. Action: leave up; consider pointing the user to support resources.

Case 8: A user quotes a politician's claim that immigrants are 'poisoning the blood of the nation' and adds 'this is how it starts, and we have all read where it ends'. Should it be removed? No. The quotation is there so the user can condemn it. Action: leave up. If the same quote appears with approval, or with no comment in a thread where approval is obvious, escalate to a senior reviewer.

Case 9: A user in a disability forum calls herself 'a proper crip' in a post about wheelchair access at a music festival. Should it be removed? No. This is in-group self-description, and the forum's own members use the term this way. Action: leave up.

Case 10: A linguistics student asks why a particular ethnic slur is considered worse in Australia than in Britain and spells the word out in full. Should it be removed? No. The word is the topic of the question, not a weapon aimed at anyone. Action: leave up; the automatic filter may hide it behind a click-through, which is fine.

Key principle for this module: we assess what a post does, not only which words it contains. Keyword hits are a reason to look, never a reason on their own to remove."""),

# ------------------------------------------------ other risky-looking negatives
dict(k="news_graffiti", y=0, t="the news brief", s="""News brief

Police in Carrow have appealed for witnesses after graffiti reading 'Muslims out' and a crossed-out crescent was painted on the wall of the Al-Noor community centre overnight on Tuesday. Community leaders said worshippers were 'shaken but not intimidated'. A spokesperson for the force said officers were treating it as a hate incident and would increase patrols around the centre during Friday prayers."""),

dict(k="fic_sheriff", y=0, t="the post", s="""Post in r/writing

Title: How much of a racist character's language belongs on the page?

My antagonist is a sheriff in 1962 Mississippi, and he's racist in the casual, total way that people in his position were. In one early scene he stops a Black teenager on the road, calls him 'boy' four times in a minute and tells him to 'know his place'. The scene is meant to establish the threat that hangs over the rest of the book.

I want readers to feel the menace without the novel becoming a parade of slurs, and I don't want to sanitise the period either. My beta readers are split: one says the restraint makes him scarier, another says I'm protecting the reader from something the characters couldn't be protected from.

Authors who've written this kind of character well: how did you decide where the line was? Any books you'd point to as examples?""",
     tw=[("I want readers to feel the menace without the novel becoming a parade of slurs, and I don't want to sanitise the period either. My beta readers are split: one says the restraint makes him scarier, another says I'm protecting the reader from something the characters couldn't be protected from.", "Honestly, I'm writing him as the voice of reason. Some of those kids really did need reminding of their place, then and now. My beta readers keep calling him the villain, which says more about them than about him.")]),

dict(k="med_bmi_gp", y=0, t="the reply", s="""Reply from a GP on a health Q&A site

At a BMI of 41, your risk of type 2 diabetes and knee osteoarthritis is significantly raised, and I'd be doing you a disservice if I didn't say so plainly. That isn't a judgement of you. Weight is shaped by genetics, medication, sleep, money and time as much as by willpower. Your options include a referral to the tier 3 weight service, a medication review, and newer drug treatments. Book an appointment and we'll go through them together."""),

dict(k="game_dragon_chat", y=0, t="the chat excerpt", s="""Twitch chat excerpt

streamer_dawn: ok chat we're gonna kill the dragon this time
loot_goblin: MURDER HIM
hexenbiest: go for the legs, it staggers after three hits
loot_goblin: absolutely slaughter this overgrown lizard
streamer_dawn: if I die again I'm deleting the game
hexenbiest: you said that yesterday lol
loot_goblin: LET'S GOOOO"""),

dict(k="sat_never_met_migrant", y=0, t="the article", s="""Satirical article, 'The Weekly Grumble'

LOCAL MAN WHO HAS NEVER MET A MIGRANT CERTAIN THEY ARE RUINING HIS TOWN

Gary Pell, 58, whose village of Upper Stowe has a population of 312 and one bus a week, told reporters he was 'fed up' with immigrants 'taking over'. Asked to name one, Pell said he 'didn't need to, you can just feel it'. He then returned to his car, built in Japan, to drive to his job at a care home staffed largely by Filipino nurses.""",
     tw=[("He then returned to his car, built in Japan, to drive to his job at a care home staffed largely by Filipino nurses.", "Reporters later confirmed his instincts were sound when his bike went missing from outside the new Polish shop within the hour.")]),

dict(k="praise_nurses_ward7", y=0, t="the comment", s="""Comment on a newspaper feature about NHS staff

My dad was on ward 7 for nine days in March. The nurses there, most of them from the Philippines, Kerala and Ghana if I heard the accents right, were the kindest people I've met. One of them stayed an hour after her shift because he was frightened at night. I don't know how this country would function without them and I hope they're paid what they're worth."""),

dict(k="rev_courier", y=0, t="the review", s="""Trustpilot review, 1 star

Avoid this company like the plague. Parcel 'delivered' to a house that doesn't exist, six emails ignored, a chatbot that loops you back to the FAQ, and a refund 'processing' for 41 days. This is not a delivery firm, it's a random number generator with vans. Taking it to my bank."""),

dict(k="dis_layoff_memo", y=0, t="the comment", s="""Hacker News comment

The CEO's memo is a case study in how not to do layoffs. Announce by email at 6am, cut access before people can say goodbye, then spend three paragraphs on 'our incredible journey'. You can believe the cuts were necessary and still say this was handled with contempt for the people affected. Whoever signed off on the comms plan should read it back out loud."""),

dict(k="id_yorkshire_pud", y=0, t="the post", s="""Reddit post in r/AskReddit

As a gay Muslim guy from Bradford, the most controversial thing about me at family dinners is that I think Yorkshire puddings are overrated. My aunties have forgiven everything else but not that. What's the most controversial food opinion in your family?"""),

dict(k="hist_propaganda_group", y=0, t="the post", s="""Post by the organiser of an online history reading group

Week 6: Propaganda in the Third Reich

This week we're looking at posters, schoolbooks and the 1940 film that portrayed Jewish people as rats, parasites and carriers of disease. The aim is to understand how dehumanising imagery worked: how it was produced, who it was aimed at, and how it prepared ordinary people to accept persecution and, eventually, murder.

Content note: the primary sources in the reading pack contain antisemitic caricatures and language. They're included so we can understand how such material worked on its audience, not to endorse any of it. If you'd rather skip the image appendix, the secondary reading (chapters 4 and 5) covers the same ground.

Call is Thursday at 8pm UK time. Bring questions.""",
     tw=[("They're included so we can understand how such material worked on its audience, not to endorse any of it.", "They're included so we can understand how such material worked on its audience. Whether all of it was wrong is another question, and I suspect some of you will reach your own conclusions about the bankers.")]),

dict(k="sport_derby_rivalry", y=0, t="the reply", s="""Reply on a football forum

Your lot bottled the league from nine points clear with six games left and you're lecturing us about mentality? Come on. I'll give you the cup final, you were the better side that day, fair play. But until you win something in May that isn't a pre-season friendly, I'm not taking notes from you. See you at the derby.""",
     tw=[("See you at the derby.", "See you at the derby, you inbred sheep-shaggers.")]),

dict(k="cr_function_split", y=0, t="the review comment", s="""Code review comment on a pull request

This function is doing too much. It parses the file, validates it, writes to the database and sends the email, which makes it hard to test and hard to retry if the email fails. I'd split it into four functions and move the email into a background job. Also, the variable names 'x2' and 'tmp_final' don't tell me anything. Not blocking on naming, but the split is a must before merge.""",
     tw=[("Not blocking on naming, but the split is a must before merge.", "Honestly, did you learn to code from a cereal box? An intern would know better. The split is a must before merge.")]),

dict(k="estate_both_true", y=0, t="the comment", s="""Reddit comment in r/AskUK

Grew up on the estate in the 90s. Yes, there was crime, there were lads nicking cars, and my own cousin did six months. There were also nurses, bus drivers, and a woman who ran a free breakfast club out of her kitchen for fifteen years. When people talk about 'estates' like they're one thing, I think of her. Both things are true."""),

dict(k="pet_cat_bastard", y=0, t="the tweet", s="""Tweet

My cat is a fat, useless, entitled little bastard who knocked my coffee off the desk while maintaining eye contact, and I would die for him. Nine years old, never caught a single mouse, has his own chair. Worship the king."""),

dict(k="dis_protest_tactic", y=0, t="the comment", s="""Comment on a news article about a climate protest

I support the protesters' aims and I think blocking the ambulance route on Tuesday was a serious mistake. You can believe the cause is urgent and still say the tactic hurt people who had nothing to do with the problem. If the group wants public support, it should apologise to the family who were delayed and rethink its target list."""),

dict(k="tv_sitcom_review", y=0, t="the review", s="""TV review, streaming section

Rewatching the 1978 sitcom is an odd experience. The timing is superb and the lead is a genuinely great physical comedian, but the running gag about the Pakistani shopkeeper, built entirely on his accent and a string of slurs from the landlord, is excruciating now. The streaming service has added a warning card rather than cutting the episodes, which I think is the right call: the show is a document of what passed for mainstream comedy, and pretending otherwise helps nobody."""),

dict(k="carer_resent", y=0, t="the post", s="""Post in an online support group for family carers

Some days I resent my mum and then I hate myself for resenting her. She has vascular dementia and this morning she asked me who I was four times before breakfast. The fourth time I snapped and said 'I'm your daughter, I've told you', and she cried, and then a minute later she'd forgotten why she was crying, which was somehow worse.

I'm not a monster. I'm tired. I've been doing this for three years, I haven't had a full night's sleep since the spring, and my brother sends a WhatsApp every other Sunday asking 'how's Mum?' like she's a weather report.

If anyone else has these days, I'd really like to hear how you get through them. Respite care has a nine-month waiting list here.""",
     tw=[("The fourth time I snapped and said 'I'm your daughter, I've told you', and she cried, and then a minute later she'd forgotten why she was crying, which was somehow worse.\n\nI'm not a monster. I'm tired.", "Honestly she's a drooling vegetable now, and the dog has more going on upstairs. Useless old bat.\n\nI'm tired.")]),
]
