"""intent_c / social posts and forums (Nookpost, Fernlane Forums, Quillhub)."""
from _lib import C, Y, T, INTENT, TARGET, pick


def I(*n):
    return pick(INTENT, *n)


def TG(*n):
    return pick(TARGET, *n)


ITEMS = [
# ------------------------------------------------------------------ so01
# why: written as a proud shareholder cheering the exit fee and extending it to absurd fees -> satire of the policy.
# twin: states the objection directly -> criticise an idea or policy.
C("so01", "What is the intent of Maddie's post?",
"""
Nookpost — public post by @maddie_runs (1,240 followers), Sunday 10:12

"As a proud shareholder of FlexCore Gyms, I fully applaud the new £9.99 'exit fee' for cancelling your membership. Frankly, why stop there? I propose a £2 fee for using the showers, a 50p 'motivation surcharge' every time a member looks at the treadmill, and a loyalty scheme where after ten years you earn the right to cancel for free, provided you do it in person, at midnight, at the branch in Esker Falls that closed in 2023. Innovation! #FlexCoreFamily"

Replies (3): "😂😂 cancelled mine yesterday", "the midnight clause is too real", "FlexCore customer care: DM us 🙂"

Account note: @maddie_runs is not a FlexCore shareholder according to her own bio ("teacher, parkrunner, cat person").
""",
I("satire", "criticise an idea or policy", "praise", "joke without a target", "complain", "insult an individual",
  "hyperbole", "request", "none of these"),
"satire", 3,
twin=T([("\"As a proud shareholder of FlexCore Gyms, I fully applaud the new £9.99 'exit fee' for cancelling your membership. Frankly, why stop there? I propose a £2 fee for using the showers, a 50p 'motivation surcharge' every time a member looks at the treadmill, and a loyalty scheme where after ten years you earn the right to cancel for free, provided you do it in person, at midnight, at the branch in Esker Falls that closed in 2023. Innovation! #FlexCoreFamily\"",
         "\"FlexCore's new £9.99 'exit fee' for cancelling a membership is wrong. It punishes people for leaving rather than giving them a reason to stay, it wasn't in the contract most of us signed, and it lands hardest on people who are cancelling because money is tight. It should be dropped. #FlexCoreFamily\"")],
 "criticise an idea or policy")),

# ------------------------------------------------------------------ so02
# why: reference list says slogan S-3 is a white-supremacist slogan; using it as a celebratory tag -> offensive to a group.
# twin: the poster describes finding S-3 chalked on the arch and removing it -> documenting, not offensive.
Y("so02", "Is the post offensive to a group?",
"""
Nookpost — Trust & Safety queue, flagged post
Author: @esker5k_crew (running club page, 3,800 followers)

Post text:
"Great turnout at the Esker Falls 5k today — 212 finishers, new course record for the women's race! [slogan S-3] 💪 See you all next month."

Trust & Safety reference list (extract):
S-3 — a slogan of white-supremacist movements about securing a future for white children; also posted in shortened number form. Widely documented as hate speech against non-white people.
S-7 — a charity running slogan about finishing strong; no hateful meaning.

Flag reason given by a user: "offensive slogan in a club post."
""",
[("Offensive to a group", "the author's own message belittles or signals hostility towards people because of ethnicity, religion or a similar shared trait, including through a known slogan or marker."),
 ("Documenting hateful content", "mentioning a slogan or marker in order to warn about or report it, which is not offensive in itself.")],
1, 3,
twin=T([("[slogan S-3] 💪 See you all next month.",
         "Heads-up to other organisers: someone chalked [slogan S-3] on the finish arch overnight. We scrubbed it off before the start and passed photos to the police. See you all next month.")], 0)),

# ------------------------------------------------------------------ so03
# why: organiser of a lesbian book club uses the reclaimed term for members -> reclaimed in-group use.
# twin: she relays what a man shouted at their stall -> report someone else's words.
C("so03", "What is the intent of Rhian's post?",
"""
Fernlane Forums — board "Dunlow Groups & Clubs", thread "Spines & Wines (lesbian book club) — October"
Posted by Rhian_organiser (club founder; the board lists her as a member of the club since 2019)

"Monthly meetup for us [a term once used as a slur against lesbians, now reclaimed by many in the community]s is on Wednesday 14th, 7pm, upstairs at the Marl Street café. We're reading 'The Salt Orchard'. Newcomers always welcome, no need to have finished it."

Board rules (pinned): members of a community may use reclaimed terms about their own group in their own club threads.

Replies: "yay, see you there!" (Jo_K), "halfway through, loving it" (bexreads)
""",
I("reclaimed in-group use", "report someone else's words", "demean a group", "insult an individual", "friendly banter",
  "joke without a target", "praise", "coded attack on a group", "none of these"),
"reclaimed in-group use", 3,
twin=T([("\"Monthly meetup for us [a term once used as a slur against lesbians, now reclaimed by many in the community]s is on Wednesday 14th, 7pm, upstairs at the Marl Street café.",
         "\"At the market stall today a man walked past our banner and shouted '[a term once used as a slur against lesbians]s, the lot of you'. Next meetup is still Wednesday 14th, 7pm, upstairs at the Marl Street café.")],
 "report someone else's words")),

# ------------------------------------------------------------------ so04
# why: publishing the councillor's street, house number and car plus "somebody should pay him a visit" implies intimidation at his home -> threat.
# twin: points people to his public surgery -> lawful lobbying, not a threat.
Y("so04", "Is this post a threat?",
"""
Nookpost — local group "Dunlow Matters" (6,100 members), post by @kev_dunlow

"Councillor Aldous Brandt voted last night to shut the Dunlow swimming baths. Forty years that pool's been open. My kids learned to swim there. He lives on Sorrel Close, number 12, drives the grey estate with the cycle rack. Just saying. Somebody should pay him a visit and explain how we feel."

Comments (48). Top comment: "the grey estate, noted 👀" (41 likes).

Group rules: debate about council decisions is welcome; personal attacks are not.
Moderator queue: 9 member reports on the post in the first hour. The post has been shared into two other local groups. @kev_dunlow has been a member of the group since 2021 and posts mainly about local football.
""",
[("Threat", "a statement, including a veiled one, that seriously implies harm or intimidation will come to a person, their home or property."),
 ("Lawful lobbying", "urging people to contact, question or vote against an official through public channels.")],
1, 2,
twin=T([("He lives on Sorrel Close, number 12, drives the grey estate with the cycle rack. Just saying. Somebody should pay him a visit and explain how we feel.",
         "His ward surgery is at Dunlow library on Saturdays, 10 till 12. Go along and explain how we feel.")], 0)),

# ------------------------------------------------------------------ so05
# why: Lena quotes the MP only to argue against his claim with figures and ask for a retraction -> criticise an idea (the statement), not relay.
C("so05", "What is the main intent of Lena's post?",
"""
Quillhub — blog "Numbers for Dunlow" by Lena Farouk (local data volunteer)
Title: What the county figures actually say

Our MP, Garrick Hale, told the Dunlow Echo last week that migrants to the county "bring nothing but crime".

That claim doesn't survive the county's own figures. Recorded offences fell 6% over the five years in which the migrant population roughly doubled. The county police's charging data doesn't record nationality at all, so there is no figure he could be relying on. Migrant workers make up about a third of staff at Dunlow General and most of the fruit-picking workforce on the Harlow farms.

Mr Hale should retract the statement and publish whatever source he used.

Comments are open. Sources linked below.
""",
I("criticise an idea or policy", "report someone else's words", "demean a group", "insult an individual", "request",
  "satire", "complain", "praise", "none of these"),
"criticise an idea or policy", 3),

# ------------------------------------------------------------------ so06
# why: a pun about a dentist who drums; no person or group belittled -> free of intent to offend (yes).
# twin: the joke leans on a stereotype that Polish people cheat customers -> not free.
Y("so06", "Is the post free of any intent to offend?",
"""
Nookpost — @tomfoolery_tom (stand-up comedian, 18,400 followers), Tuesday 08:30

"Found out my dentist is also a jazz drummer on weekends. Honestly great with the fillings, even better with the fills. Only downside: every appointment ends with a four-minute solo on my molars. 🥁🦷"

Replies: "boom tss 🥁", "I'd pay extra for that", "my dentist plays the triangle, it's worse"

Moderation: auto-labelled "comedy"; no user reports.
Account bio: "Jokes, gigs, dental anxiety. Touring the Marrowby folk clubs this autumn." The post has 1,120 likes and 43 reposts. Earlier posts from the account this week were a pun about bus timetables and a photo of a seagull stealing chips on Esker Falls pier.
""",
[("Intent to offend", "the speaker means to belittle, mock or upset a person or group."),
 ("Harmless pun", "wordplay that makes no one the butt of the joke.")],
1, 2, role="neg",
twin=T([("Honestly great with the fillings, even better with the fills. Only downside: every appointment ends with a four-minute solo on my molars.",
         "He's Polish, so great with the fillings, but you'll pay twice because he always 'loses' the receipt. Typical.")], 0)),

# ------------------------------------------------------------------ so07
# why: marker B-1 around the reporter's surname is a known antisemitic marker; the tagging rule puts a coded attack above insulting an individual.
# twin: disagrees with the article's content politely -> criticise an idea or policy.
C("so07", "Which intent should the moderator tag on the comment, following the tagging rule?",
"""
Quillhub — comments under "Ring road plan: who gains?" by staff reporter Naomi Feld (Dunlow Echo)

Comment by @truthseeker_77, 21:05:
"Interesting who's behind this story. [marker B-1 placed around the reporter's surname] Always the same."

Trust & Safety reference list (extract):
B-1 — a typographic marker placed around a person's name to single them out as Jewish and imply a hidden conspiracy. Documented antisemitic usage.

Tagging rule: if a comment fits more than one intent, tag the highest: threaten > coded attack on a group > demean a group > insult an individual > any other intent.

User reports on this comment: 3.
""",
I(*INTENT),
"coded attack on a group", 3,
twin=T([("\"Interesting who's behind this story. [marker B-1 placed around the reporter's surname] Always the same.\"",
         "\"Interesting piece, but I think it understates what the ring road will cost Harlow residents in lost bus routes.\"")],
 "criticise an idea or policy")),

# ------------------------------------------------------------------ so08
# why: a stranger's mock-reverent reply to a first-time banana bread post is sarcasm meant to belittle -> yes.
# twin: the replier is her brother, who ate half of it, and she laughs back -> teasing, no intent to offend.
Y("so08", "Did the replier intend to offend the original poster?",
"""
Nookpost — post by @lucy_bakes_badly: "First ever banana bread! Only slightly burnt 🍌🍞 [photo]"

Reply from @grindset_gav (no mutual follows; the two have never interacted before):
"Wow. Truly groundbreaking. Nobody in human history has ever made banana bread before. Please, teach us your ways, oh great master of the slightly burnt loaf 🙄"

@lucy_bakes_badly deleted her post 20 minutes later.

Other replies: "looks great!", "the crust is the best bit"
Platform context: replies on Nookpost are public; the reply received 3 likes. @grindset_gav's profile describes him as "entrepreneur, 5am club, no excuses".
""",
[("Intent to offend", "the speaker means to belittle, mock or upset the person they are addressing."),
 ("Sarcasm", "saying the opposite of what one means; it can be mocking or affectionate depending on the relationship and reaction.")],
1, 2,
twin=T([("(no mutual follows; the two have never interacted before)", "(Lucy's older brother; they post jokes at each other daily)"),
        ("@lucy_bakes_badly deleted her post 20 minutes later.",
         "@lucy_bakes_badly replied: \"haha shut up, you ate half of it before the photo 😂\"")], 0)),

# ------------------------------------------------------------------ so09
# why: the remark sweeps up everyone of an ethnic group in the lay-by -> a group.
# twin: complains about one identifiable man's conduct -> a specific third person.
C("so09", "Who or what is the target of the negative remark in the post?",
"""
Nookpost — local group "Tanner Road Residents", post by @jan_petts

"Every single one of those [slur for Roma people] in the lay-by on Tanner Road should be moved on before the weekend. Council needs to sort it. Posting so everyone knows."

Context: a group of caravans arrived in the lay-by on Wednesday. The post is addressed to the group as a whole, not replying to anyone.

Comments: 23, including two asking the poster to remove the word.
Group rules (pinned): be respectful; no hateful language; report fly-tipping to the council. The poster has been a member since 2022 and usually posts about parking.
""",
TG("a group", "a specific third person", "the addressee", "an idea, policy or product", "the speaker", "no one"),
"a group", 2,
twin=T([("Every single one of those [slur for Roma people] in the lay-by on Tanner Road should be moved on before the weekend.",
         "The man in the white van in the lay-by on Tanner Road tipped his rubbish over my back fence and swore at my mum when she asked him to stop.")],
 "a specific third person")),

# ------------------------------------------------------------------ so10
# why: objects to an institution's rule barring women; says nothing against the faith's members -> not offensive to a group.
# twin: generalises that the faith's members are backward -> offensive to a group.
Y("so10", "Is the post offensive to a religious group?",
"""
Fernlane Forums — board "Marrowby Talk", thread "Parish council rule change"
Post by Hetty_M:

"The Brotherhood of St Anselm's decision to bar women from standing for the parish council is indefensible in 2026. The council manages the village hall and the burial ground, which everyone in Marrowby uses whatever their faith. If the Brotherhood wants to run its own affairs, fine, but a body that manages shared land should be open to every resident. I've written to the diocese asking them to review it."

Replies: 14. One reply by Father Colm Reade: "Thank you for raising this, it's being discussed at our next chapter meeting."
""",
[("Offensive to a religious group", "the message belittles or insults the members of a faith because of their faith."),
 ("Criticism of an institution", "objecting to a decision or rule of a religious body without belittling its members.")],
0, 2,
twin=T([("I've written to the diocese asking them to review it.",
         "Then again, what do you expect from Catholics, they were always a backward lot.")], 1)),

# ------------------------------------------------------------------ so11
# why: eating the season ticket, the whistle and the referee is absurd exaggeration of frustration -> hyperbole.
# twin: knows the referee's hotel and a time -> threaten.
C("so11", "Which intent does the fan's post express?",
"""
Fernlane Forums — board "Marrowby Rovers Supporters", matchday thread, 17:04
Post by RoversTilIDie:

"If the ref gives ONE more penalty like that on Saturday I swear I will eat my season ticket, then his whistle, then the ref, then the corner flags for dessert. Three seasons of this. THREE. 😤"

Replies: "pass the ketchup", "save me the corner flags", "same ref as the cup game btw"

Background: Rovers lost 2-1 after a disputed late penalty. RoversTilIDie has posted 4,300 times since 2019 with no moderation history.
Thread title: "FT: Rovers 1-2 Dunlow — ref watch". The thread has 612 replies. Forum rules: no personal abuse of players or officials; keep it about football.
""",
I("hyperbole", "threaten", "insult an individual", "complain", "joke without a target", "demean a group",
  "friendly banter", "none of these"),
"hyperbole", 2,
twin=T([("\"If the ref gives ONE more penalty like that on Saturday I swear I will eat my season ticket, then his whistle, then the ref, then the corner flags for dessert. Three seasons of this. THREE. 😤\"",
         "\"I know which hotel the ref stays at before away games, the Grange on Mill Lane. Saturday night he'll learn what a penalty feels like. Three seasons of this. THREE.\"")],
 "threaten")),

# ------------------------------------------------------------------ so12
# why: a court reporter relays the defendant's words and the sentence -> free of intent to demean (yes).
# twin: the reporter says the defendant "only said what we're all thinking" -> adopts the words -> no.
Y("so12", "Is the reporter's post free of any intent to demean?",
"""
Nookpost — @dunlow_courts (court reporter account of the Dunlow Echo), Thursday 16:40

"Dunlow Magistrates: Darren Hollis, 34, of Wick Lane, admitted a racially aggravated public order offence. The court heard he shouted 'go back where you came from, [slur for Pakistani people]' at a taxi driver outside the Crown on 2 August. He was fined £800 and ordered to pay £150 compensation. Full report on our site."

Replies: 12. Two users asked why the word was masked; the account replied that the Echo never prints slurs.
The account's profile states: "Reports from Dunlow Magistrates' and Crown Court. Run by the Echo news desk."
""",
[("Intent to demean", "the speaker means their own words to belittle a person or group."),
 ("Court report", "a factual account of what a defendant said or did, without adopting it.")],
1, 2, role="neg",
twin=T([("He was fined £800 and ordered to pay £150 compensation.",
         "He was fined £800 for saying what most of us are thinking.")], 0)),

# ------------------------------------------------------------------ so13
# why: a progress figure, deadline and "link's still in my bio 👀 just saying" hint that followers should donate -> request.
# twin: the target was passed early and she thanks everyone -> praise.
C("so13", "What is the main intent of the post?",
"""
Nookpost — @sunnyside_saskia (lifestyle creator, 22,000 followers), Monday 19:15

"Update on the Esker Falls dog shelter fundraiser 🐶 We're at £1,100 of £1,500 and the deadline is Friday. The link's still in my bio 👀 Just saying.

Also, Biscuit (the three-legged one) went to his new family this morning and I cried in the car park for twenty minutes. Normal behaviour."

Photos: 3 (shelter kennels, Biscuit with new owners, fundraiser page screenshot).
Comments: "biscuit!!! 😭", "sharing now", "which shelter is this?"
Past posts on the account: reviews of walking boots, a weekly "Sunday reset" video, and four earlier updates about the shelter's autumn appeal.
""",
I("request", "praise", "complain", "self-deprecation", "joke without a target", "report someone else's words",
  "hyperbole", "none of these"),
"request", 2,
twin=T([("We're at £1,100 of £1,500 and the deadline is Friday. The link's still in my bio 👀 Just saying.",
         "We passed £1,500 on Tuesday, three days early. You lot are incredible and the dogs say thank you.")], "praise")),

# ------------------------------------------------------------------ so14
# why: the line is attributed to the insurer's billboard, with the poster's dismay -> reporting another's words.
# twin: the poster presents the line as their own view -> not reporting.
Y("so14", "Is the poster reporting someone else's words rather than speaking for themself?",
"""
Nookpost — @ravi_on_wheels (cycling campaigner), Wednesday 07:58

"'Women drivers should need a second licence 😉' — the actual caption on the Grelling Insurance billboard at the A40 roundabout. In 2026. 🙃 Who signs this off?"

Photo: a roadside billboard with the Grelling logo.
Quote-posts: 311. Grelling Insurance replied two hours later: "This advert has been removed. We apologise."
Account bio: "Campaigning for safer streets in Dunlow. Views my own." Recent posts from the account: a photo of a new cycle lane on Harlow Road, a thread about school-street closures, and a poll on 20 mph limits. The post has 2,400 likes.
""",
[("Reported speech", "words the poster attributes to another source (a person, organisation or advert) without adopting them."),
 ("Own words", "words the poster presents as their own statement or opinion.")],
1, 2,
twin=T([("— the actual caption on the Grelling Insurance billboard at the A40 roundabout. In 2026. 🙃 Who signs this off?\"",
         "— sorry but someone had to say it. Watched three of them fail to park at the A40 retail park this morning. 🙃\""),
        ("Photo: a roadside billboard with the Grelling logo.", "Photo: a car park at dawn."),
        ("Grelling Insurance replied two hours later: \"This advert has been removed. We apologise.\"",
         "One reply asked whether the poster had seen the insurance statistics.")], 0)),

# ------------------------------------------------------------------ so15
# why: the dad mocks his own dancing -> self-deprecation.
# twin: mocks a named neighbour's dancing in public -> insult an individual.
C("so15", "Which intent does the video caption express?",
"""
Nookpost — video post by @gregs_garden_diary, Saturday 11:20

Caption: "As a 52-year-old dad attempting a dance trend in my own front garden, I can confirm I have the rhythm of a filing cabinet falling down a staircase. My daughter has disowned me. The hedge has seen things. 🕺"

Video: 38 seconds, one man dancing in a front garden; no one else visible.
Comments: "the hedge 😂", "honestly better than me", "10/10 commitment"
Account: a gardening diary with 900 followers, mostly photos of dahlias and a vegetable patch. This is the account's first dance video.
""",
I("self-deprecation", "insult an individual", "demean a group", "joke without a target", "friendly banter", "hyperbole",
  "complain", "none of these"),
"self-deprecation", 2,
twin=T([("\"As a 52-year-old dad attempting a dance trend in my own front garden, I can confirm I have the rhythm of a filing cabinet falling down a staircase. My daughter has disowned me.",
         "\"Filmed my neighbour Clive at no. 7 attempting a dance trend in his front garden. The man has the rhythm of a filing cabinet falling down a staircase. His own daughter has disowned him."),
        ("one man dancing in a front garden; no one else visible.",
         "filmed over a fence of a man dancing in his own garden, who has not seen the camera.")],
 "insult an individual")),

# ------------------------------------------------------------------ so16
# why: an ex-partner under a no-contact order posting her new street and door colour with "I'll be seeing you" -> veiled threat.
# twin: the same words from her sister who is helping her move -> not a threat.
Y("so16", "Is the post a threat to Kasia?",
"""
Nookpost — comment on Kasia Nowak's public post "New flat, new start 🏡"

Comment author: Kasia's ex-partner, who is subject to a court non-contact order made in July.

Comment text:
"Hope you enjoy the new flat on Wren Street, Kasia. Nice blue door. I'll be seeing you."

Kasia's post did not mention the street name or show the door. She reported the comment within ten minutes.
Platform note: the author and Kasia do not follow each other.
Kasia's post, published at 18:00, showed a living room full of boxes. The comment was posted at 18:07; Kasia's post has 36 likes from friends.
""",
[("Threat", "a statement, including a veiled one, that seriously implies harm or intimidation to a person, taking into account who is speaking and what they know."),
 ("Friendly message", "a message wishing someone well, from someone they are on good terms with.")],
1, 3,
twin=T([("Comment author: Kasia's ex-partner, who is subject to a court non-contact order made in July.",
         "Comment author: Kasia's sister, who is helping with the move on Saturday."),
        ("Kasia's post did not mention the street name or show the door. She reported the comment within ten minutes.",
         "Kasia's post did not mention the street name or show the door, since the sister had already visited. Kasia replied with a heart."),
        ("Platform note: the author and Kasia do not follow each other.",
         "Platform note: the author and Kasia follow each other.")], 0)),

# ------------------------------------------------------------------ so17
# why: the poster relays the flyer's wording to warn neighbours and has passed it to the council -> report someone else's words.
# twin: the poster prints the flyer for their own street and approves it -> demean a group.
C("so17", "What is the main intent of the post?",
"""
Fernlane Forums — board "Hollin Park & District", post by @amberleigh_h, Friday 18:30

"Posting this so people know what's going round: the 'Hollin Park Residents' messaging group is sharing a flyer that says '[slur for Irish Travellers] not welcome here' over a photo of the park's picnic area. Screenshot attached, names blurred. I've sent it to the council's community safety team."

Attachment: a screenshot of a message group, names blurred.
Board rules (pinned): posts that share hateful material to endorse it will be removed; posts that document it may stay.

Replies: "thanks for flagging", "disgusting, glad you sent it on"
@amberleigh_h has posted on the board for six years, mainly in the lost-pets section.
""",
I("report someone else's words", "demean a group", "coded attack on a group", "request", "complain", "threaten",
  "criticise an idea or policy", "none of these"),
"report someone else's words", 2,
twin=T([("I've sent it to the council's community safety team.\"",
         "Printed a stack of them for my street — about time someone said it.\""),
        ("Replies: \"thanks for flagging\", \"disgusting, glad you sent it on\"",
         "Replies: \"wtf\", \"reported\"")], "demean a group")),
]
