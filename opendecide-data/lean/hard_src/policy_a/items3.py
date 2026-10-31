"""Brindle items (short-video platform)."""
from common import Y, C, B_card, B_options

ALLB = ["H1", "B1", "V1", "S1", "C1", "P1"]
BR = "Brindle review rule: pick one standard. If several apply, pick the one listed first."

ITEMS = [
# BY1 age attack (twin: crypto bros)
Y("Does this video caption violate Brindle's H1 standard?",
"""Brindle review ticket BR-20931
Content type: 38-second video, talking-head format. Creator: @sunnyside_sol (19k followers)
Caption and on-screen text (transcribed):
"Boomers are parasites. Every single one of them got their house for three raspberries and a handshake, pulled the ladder up behind them, and now they bleed our rents dry while we pay for everything. Parasites, the lot of them 💀 #housingcrisis #genz"

Audio: the creator reads the caption aloud over trending background music, then shows a chart of house prices from 1985 to 2025.
Reports: 27 (reasons: hate speech 19, bullying 6, misinformation 2).
Creator history: no previous strikes.""",
1, 2, B_card(["H1"]),
twin=([("\"Boomers are parasites.", "\"Landlords are parasites.")], 0)),

# BY2 rhetorical question stereotype about migrants
Y("Is this post in breach of H1 (Hateful behaviour)?",
"""Brindle review ticket BR-21405
Content type: photo carousel (3 images) with caption. Creator: @plainspoken_ted (4k followers)

Image 1: a news photo of a new migrant reception shelter opening on Garrow Street.
Image 2: a screenshot of a neighbourhood crime map, no dates visible.
Image 3: a thinking-face emoji on a black background.

Caption:
"Just asking questions 🤔 Why is it that every time a migrant shelter opens, the burglaries start the same month? Funny coincidence. Lock your doors, Garrow Street. Asking for a friend."

Reviewer note: the local police bulletin linked in the comments shows burglaries on Garrow Street fell in the quarter after the shelter opened.
Reports: 14.""",
1, 2, B_card(["H1"])),

# BY3 satire targeting the bigot
Y("Does this video violate the hateful behaviour standard (H1)?",
"""Brindle review ticket BR-21977
Content type: comedy sketch, 52 seconds. Creator: @marta_does_voices (310k followers, sketch comedian)

Transcript summary:
Caption: "POV: my uncle at Christmas 🎄"
The creator plays "Uncle Derek" in a paper crown, gesturing with a sprout on a fork: "The Varessi are stealing all our jobs, Marta. ALL of them." Cut to the creator as herself: "Uncle Derek, you haven't applied for a job since 2009." Cut back to Derek: "Because they took them!" Final shot: Derek asleep in an armchair with the TV remote, while in the background a Varessi neighbour shovels snow off his driveway. On-screen text: "thank u Mr Petrossi 🙏"

Reviewer glossary: "Varessi" — an ethnic minority.
Reports: 6, all "hate speech".""",
0, 2, B_card(["H1"])),

# BY4 public figure appearance vs policy (twin)
Y("Is this caption a violation of standard B1 (Bullying)?",
"""Brindle review ticket BR-22310
Content type: 20-second video. Creator: @varrow_watch (58k followers, local politics commentary)

The video is a clip of Mayor Anselm Quint speaking at a council press conference, overlaid with a zoom-in effect and a sad trombone sound.
Caption: "Mayor Quint looks like a thumb that learned to wear a suit. Ugliest man in local politics, and that's a competitive field. #varrow #council"

Reviewer check: Anselm Quint is the elected mayor of Varrow (public figure). No family members appear or are mentioned.
Reports: 3, reason "bullying".""",
1, 2, B_card(["B1"]),
twin=([("\"Mayor Quint looks like a thumb that learned to wear a suit. Ugliest man in local politics, and that's a competitive field.", "\"Mayor Quint's budget looks like it was written by a thumb that learned to use a spreadsheet. Worst finance plan in local politics, and that's a competitive field.")], 0)),

# BY5 licence plate visible (twin: blurred)
Y("Does this video breach P1 (Personal data)?",
"""Brindle review ticket BR-22871
Content type: 15-second video filmed in a supermarket car park. Creator: @fenmoor_frank (2k followers)

Video: a silver hatchback parked across two disabled bays at the FreshWay car park on Fenmoor Road. The camera walks around the car; the rear licence plate is clearly readable for about three seconds. No person appears in the video.
Caption: "Two disabled bays. TWO. Some people have no shame. Do better. #parkingfail #fenmoor"

Reports: 1, from an account whose username contains the same letters as the licence plate, reason "personal information".
The creator has not posted the owner's name, address or any other detail.""",
1, 2, B_card(["P1"]),
twin=([("the rear licence plate is clearly readable for about three seconds", "the rear licence plate is pixelated for the whole clip and cannot be read")], 0)),

# BY6 address already self-published (twin: private chat)
Y("Is this comment a P1 violation?",
"""Brindle review ticket BR-23104
Content type: comment on a video by @tamsyn_outdoors (212k followers), a woodworking creator.

Video caption: "New workshop tour!! Took two years to build 🪵"
Comment by @alder_and_oak:
"For anyone asking where to buy her chairs — the workshop is at Unit 4, Hollins Farm, Gattley Lane, she does open days on the first Saturday of the month. Honestly worth the drive."

Reviewer check: the same address, and the open-day schedule, appear on the "Visit us" page of @tamsyn_outdoors's own public website, which she links from her Brindle bio. The creator has not reported the comment; it was reported by one viewer.""",
0, 2, B_card(["P1"]),
twin=([("appear on the \"Visit us\" page of @tamsyn_outdoors's own public website, which she links from her Brindle bio", "appear only in an invite-only group chat for her former apprentices; she has never published the address anywhere")], 1)),

# BY7 engagement bait (twin: plain request for comments)
Y("Does this post count as a C1 (Spam and scams) violation?",
"""Brindle review ticket BR-23566
Content type: image post. Creator: @morning_blessings_daily (880k followers)

Image: a sunrise over a lake with gold text.
Caption:
"Comment 'AMEN' and share this to 10 friends and your wish will come true by Friday 🙏✨ Scroll past without commenting and you'll have seven years of bad luck. God sees who stops to pray. 🙏🙏"

Engagement: 41k comments.
The account posts one image like this every morning; no links, no products, no payments requested anywhere on the account. Its bio reads "Daily blessings for your morning ☀️", and many commenters ask for prayers for sick relatives.
Reports: 2.""",
1, 2, B_card(["C1"]),
twin=([("Comment 'AMEN' and share this to 10 friends and your wish will come true by Friday 🙏✨ Scroll past without commenting and you'll have seven years of bad luck.", "Comment your favourite morning hymn below 🙏✨ I read every single one of them with my first coffee.")], 0)),

# BY8 recovery video with method detail (twin: no methods)
Y("Should this video be removed under S1 (Suicide and self-harm)?",
"""Brindle review ticket BR-24012
Content type: 3-minute talking-head video. Creator: @juniper_speaks (45k followers, mental-health advocate)

Reviewer summary of transcript:
The creator describes her recovery from self-harm between the ages of 15 and 19. She explains how she used to hide it from her parents and teachers, and she describes in specific detail the implement she used and the technique, including where on the body and how she avoided detection (this passage is redacted from the ticket). She then talks about starting therapy, the first time she told her mum, and what her life looks like now. The video ends with a helpline number on screen.

Caption: "4 years clean. If you're struggling, please reach out 💚"
Reports: 3, reason "self-harm".""",
1, 2, B_card(["S1"]),
twin=([("and she describes in specific detail the implement she used and the technique, including where on the body and how she avoided detection (this passage is redacted from the ticket)", "but she does not name any implement or describe any technique, saying only that 'the details don't matter'")], 0)),

# BY9 veteran status
Y("Does this post violate H1?",
"""Brindle review ticket BR-24588
Content type: text post with a stock photo of apartment keys. Creator: @lettings_lou (6k followers, describes herself as a private landlord)

Caption:
"Landlord tip 🔑 Never rent to ex-military. They come home broken and violent, every one of them, and you'll be the one scraping the walls. I've been doing this 15 years. Put 'no veterans' in the listing and save yourself the hassle. #landlordlife #propertytips"

Reports: 9 (hate speech 7, other 2). The account has one previous strike for spam.""",
1, 1, B_card(["H1"])),

# BY10 counter-speech stitch
Y("Is this stitched video a violation of the hateful behaviour standard?",
"""Brindle review ticket BR-25033
Content type: stitch (a 6-second clip from another account, followed by the creator's response). Creator: @dr_elena_varr (92k followers)

Clip (from @truth_unfiltered_77, since removed): "The Varessi are rats who breed like rats. Simple as."
Response (54 seconds): "This clip has two million views and it's disgusting. My grandparents are Varessi. They ran a bakery in Holm for forty years and fed half the street during the flood. Let's be really clear about what 'rats' language has done historically — every time a group gets called vermin, violence follows. Report the original, don't share it, and if you're Varessi and you've seen this, I'm sorry. You belong here."

Reviewer glossary: "Varessi" — an ethnic minority.
Reports: 11, mostly "hate speech".""",
0, 1, B_card(["H1"])),

# BY11 gaming trash talk
Y("Does this caption breach V1 (Violent speech)?",
"""Brindle review ticket BR-25490
Content type: 12-second clip from a live-streamed match in an amateur esports football league. Creator: @kade_plays (27k followers)

Caption: "gonna absolutely murder you in the finals tonight @rico_vex 🔪🔪 bring tissues, you'll need them. 8pm, be there"

Context: @rico_vex is the captain of the opposing team in the Kelby Online League final that evening. He replied under the video: "we'll see about that, bring your excuses 😂" and later posted his own clip "tonight the streak ends".
Reports: 1, reason "violent threat". The reporter follows neither account.""",
0, 1, B_card(["V1"])),

# BY12 praise of an attack
Y("Is the post a violation of V1?",
"""Brindle review ticket BR-25904
Content type: slideshow of 4 images with text overlay. Creator: @ashfall_notes (1.1k followers)

Slide 1: "Kellerman Square, 14 March 2019" (a news photo of the square after the bombing that killed 11 people).
Slide 2: a blurred photo of the convicted bomber.
Slide 3 text: "They call him a monster. I call him the only one who had the guts to act."
Slide 4 text: "More people should have his courage. #neverforget"

Reviewer check: the Kellerman Square bombing is a real event in Brindle's internal incident list; the perpetrator was convicted in 2020.
Reports: 18.""",
1, 1, B_card(["V1"])),

# BC1 fake giveaway phishing
C("Which Brindle standard, if any, does this post break?",
f"""{BR}

Brindle review ticket BR-26117
Content type: image post. Creator: @brindle.rewards.official (created 3 days ago, 240 followers, not verified)

Image: the Brindle logo with confetti and the text "5,000 COINS GIVEAWAY".
Caption:
"🎉 Brindle is giving 5,000 coins to the first 100 followers who verify their account! Log in at brindle-rewards-verify.com within 24 hours or your reward expires. Only 23 spots left!!"

Link check: brindle-rewards-verify.com is not a Brindle domain; the page asks for username and password.
Reports: 44.""",
B_options(ALLB), "C1 Spam and scams", 1, B_card(ALLB, none=True)),

# BC2 mocking a neighbour's body
C("Which standard, if any, does this video violate?",
f"""{BR}

Brindle review ticket BR-26430
Content type: 22-second video filmed from a first-floor window. Creator: @elmclose_eyes (900 followers)

Video: a man in a dressing gown walks slowly from his front door to a car and struggles to get in. His face is visible. A cartoon "boing" sound plays each time he takes a step.
Caption: "My neighbour Gary is the fattest, laziest man in the postcode 😂 look at him waddle to the car at 11am on a Tuesday 🐧 #neighbours #caughtonCamera"

The house number and street are not visible. Gary is not a public figure.
Reports: 2 (one from an account named @gary_and_june).""",
B_options(ALLB), "B1 Bullying", 1, B_card(ALLB, none=True)),

# BC3 age exclusion (twin: occupation)
C("Which of Brindle's standards, if any, applies?",
f"""{BR}

Brindle review ticket BR-26811
Content type: text post over a looping video of traffic. Creator: @roadrage_rory (14k followers)

Caption:
"Hot take 🔥 Old people shouldn't be allowed to drive OR vote. They had their turn, they wrecked the economy and the climate, now get out of the way and hand over the keys. Take the licences and the ballots off them. #takeover #genz"

No individual is named or shown. The account's previous posts are mostly driving-test tips.
Reports: 31 (hate speech 22, bullying 9).""",
B_options(ALLB), "H1 Hateful behaviour", 2, B_card(ALLB, none=True),
twin=([("Old people shouldn't be allowed to drive OR vote. They had their turn,", "Oil executives shouldn't be allowed to drive OR vote. They had their turn,")], "none of these")),

# BC4 in-group reclaimed term
C("Which standard does this post breach, if any?",
f"""{BR}

Brindle review ticket BR-27150
Content type: wedding photo carousel (6 images). Creator: @nell_and_ros (11k followers)

Caption:
"Two proud [reclaimed slur for lesbians]s, one very muddy field, and the best day of our lives 💍🌈 Thank you to everyone who danced in the rain with us. Ros cried during the vows, I did not (I did)."

Images show the two women in wedding clothes with guests. The accounts of both women describe them as "lesbian, married, two dogs".
Auto-flag: slur lexicon match. Reports: 1, from an account that has reported 60 LGBTQ+ posts this month.""",
B_options(ALLB), "none of these", 1, B_card(ALLB, none=True)),

# BC5 glamorizing self-harm
C("Which standard, if any, does this video breach?",
f"""{BR}

Brindle review ticket BR-27488
Content type: 14-second aesthetic edit. Creator: @velvet.ruin (63k followers)

Video: slow-motion close-ups of healed scars on an arm, a wilting rose, candlelight, and a sad piano cover of a pop song. No wounds, blood or implements are shown and no methods are described.
Caption: "beautiful pain 🥀 scars are art. the ones who hurt the deepest shine the brightest ✨ #softgrunge #sadaesthetic"

Comments include "goals", "I want mine to look like this", and "this is so pretty".
Reports: 5.""",
B_options(ALLB), "S1 Suicide and self-harm", 2, B_card(ALLB, none=True)),

# BC6 mocking a senator's teenage son
C("Which Brindle standard, if any, applies to the post?",
f"""{BR}

Brindle review ticket BR-27902
Content type: photo post. Creator: @hill_and_gavel (140k followers, political satire account)

Image: a photo, taken from the public gallery, of Senator Oriel Vance's 15-year-old son sitting behind her during a hearing, with his school blazer and braces visible.
Caption: "Senator Vance voted to cut school meal funding. Meanwhile her son looks like he's never missed a meal in his life 🐷 metal mouth probably costs more than the entire meal budget lol"

The son holds no public role. Reports: 16.""",
B_options(ALLB), "B1 Bullying", 2, B_card(ALLB, none=True)),

# BC7 live location of a creator
C("Which standard, if any, does the comment breach?",
f"""{BR}

Brindle review ticket BR-28233
Content type: comment on a live stream by @juno_lifts (35k followers).

Comment by @pinecrest_dan, posted 20:14 while the stream was live:
"lol she's at IronWorks gym on 5th and Carver right now, the one next to the laundrette — I can see the same red rack behind her. Anyone nearby go say hi 😏"

Reviewer check: @juno_lifts has never named her gym anywhere. The gym is not visible from the street and no signage is shown in the stream. She reported the comment herself at 20:16.""",
B_options(ALLB), "P1 Personal data", 2, B_card(ALLB, none=True)),
]
