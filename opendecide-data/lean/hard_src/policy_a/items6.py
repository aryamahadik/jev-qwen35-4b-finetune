"""Multi-comment threads and extra yes/no items."""
from common import Y, C, L_card, L_OPTS, L_DEF, B_OPTS, B_DEF, B_card, K_OPT, K_DEF, M_OPTS, M_DEF, card_lines, K_RULE

def opts(n):
    return [f"Comment {c}" for c in "ABCDEF"[:n]] + ["none of these"]

def mopts(n):
    return [f"Message {c}" for c in "ABCDEF"[:n]] + ["none of these"]

ITEMS = [
# TC1 Loomwell 3.1 thread: exclusion call is the only violation
C("Which comment in the thread breaches section 3.1?",
"""Community: c/PellRoadResidents
Thread: "Ormist temple extension approved — what now for parking?"
Reviewer glossary: "Ormist" — adherent of Ormism, a minority religion.

Comment A (u/hazel_ferrow): "Ormism's teachings on women are regressive and I'll keep saying so, extension or no extension."
Comment B (u/devan_orm, profile: "Ormist, Pell Road born and bred"): "Speaking as an Ormist, our temple committee is a shambles. They've ignored the parking problem for years."
Comment C (u/stackyard_lou): "Put the lot of them on the ferry back where they came from. Pell Road was ours first and it'll be ours again."
Comment D (u/nettle_and_rue): "Someone painted '[anti-Ormist slur]s out' on the temple wall last month. That's the real problem on this street, not parking."
Comment E (u/wexcombe): "The planning committee are spineless cowards who approve anything with a nice drawing attached."
""",
opts(5), "Comment C", 2,
L_card(["3.1"]) + "\n" + card_lines([("Comment A", "reply by u/hazel_ferrow."), ("Comment B", "reply by u/devan_orm."), ("Comment C", "reply by u/stackyard_lou."), ("Comment D", "reply by u/nettle_and_rue."), ("Comment E", "reply by u/wexcombe."), ("none of these", "no comment breaches section 3.1.")])),

# TC2 Brindle H1 thread: veteran status vs bullying distractor
C("Which comment violates Brindle's H1 standard?",
"""Brindle review ticket BR-29115 — comment section of a video by @stepsforheroes (charity hike by a group of military veterans across the Ferral Hills)

Comment A (@lark_mayfield): "Vets are some of the bravest people alive, donated 💛"
Comment B (@corran_edge): "Trails like this should ban ex-soldiers, half of them are ticking time bombs waiting to snap on some poor dog walker."
Comment C (@sunny_holt_22): "My grandad served and he'd have loved this. Go on lads!"
Comment D (@bexfen): "lol the guy in the orange hat walks like a penguin 🐧 how is he doing 40 miles"
Comment E (@audit_everything): "FYI this charity's CEO pays himself £300k a year. Donate to the local branch directly instead."

The man in the orange hat is a private individual. No other context is available.""",
opts(5), "Comment B", 2,
B_card(["H1"]) + "\n" + card_lines([("Comment A", "by @lark_mayfield."), ("Comment B", "by @corran_edge."), ("Comment C", "by @sunny_holt_22."), ("Comment D", "by @bexfen."), ("Comment E", "by @audit_everything."), ("none of these", "no comment breaches H1.")])),

# TC3 Kestrel: which message gets an HS code
C("Which message in the log should receive a code from the HS family?",
f"""{K_RULE}

Kestrel chat log export — channel #eu-queue-chat
Message A [Dorran_Pike]: "gg go back to bronze where you belong lol"
Message B [Ysolde_K]: "@Mod_Hesk report: [Fenn_Rask] called me a [anti-Ostrevan slur] in voice, clip attached"
Message C [Morven_Tal]: "every Ostrevan in this queue should be banned from EU servers, stick them on their own region"
Message D [Irek_Ostrov]: "I'm Ostrevan and yeah our home servers lag like crazy, that's why we queue EU lol"
Message E [Pell_Aster]: "the EU-East region is honestly the worst server, full of throwers"

Reviewer glossary: "Ostrevan" — nationality of Ostreva; "EU-East" — a server region.""",
mopts(5), "Message C", 2,
card_lines([(K_OPT[c], K_DEF[c]) for c in ["HS-1", "HS-2", "HS-3", "HS-4", "HS-5"]]) + "\n" + card_lines([("Message A", "by Dorran_Pike."), ("Message B", "by Ysolde_K."), ("Message C", "by Morven_Tal."), ("Message D", "by Irek_Ostrov."), ("Message E", "by Pell_Aster."), ("none of these", "no message fits any HS code.")])),

# TC4 Loomwell 3.6: which comment exposes private info (twin: none)
C("Which comment, if any, breaches section 3.6?",
"""Community: c/KelbyNightlife
Post by u/fennel_rowe: "Bouncer at the Copper Lantern threw my brother out for no reason last night. Who do I complain to?"

Comment A (u/hollis_park): "Call the Copper Lantern's manager line, 01632 960118, it's on their website and the door."
Comment B (u/civic_ro): "Your MP's constituency office is at 12 Guild Street, they deal with licensing complaints too."
Comment C (u/marrow_quint): "The bouncer's Jonah Pell, I went to school with him. His mum's mobile is 07700 900663, she'll want to know what he did."
Comment D (u/sable_ren): "Pinging u/jonah_pell_security since he posted his own work number (07700 900301) in c/KelbyJobs last week asking for door shifts — maybe just ask him directly?"

Reviewer check: Jonah Pell and his mother are private individuals. His mother has no Loomwell account.""",
opts(4), "Comment C", 2,
L_card(["3.6"]) + "\n" + card_lines([("Comment A", "reply by u/hollis_park."), ("Comment B", "reply by u/civic_ro."), ("Comment C", "reply by u/marrow_quint."), ("Comment D", "reply by u/sable_ren."), ("none of these", "no comment breaches section 3.6.")]),
twin=([("His mum's mobile is 07700 900663, she'll want to know what he did.", "His mum owns Pell's Bakery, the shop number's on their website, 01632 960663, she'll want to know what he did.")], "none of these")),

# TC5 Meridian §4.3: which message references a weapon/threat
C("Which message, if any, breaches §4.3 of the Meridian policy?",
"""Meridian Workspace — channel #platform-ops (37 members), Thursday afternoon

Message A (Rosa Engel, 14:02): "I'm going to absolutely kill this demo tomorrow, wish me luck 💪"
Message B (Tom Hask, 14:10): "Dave's going to murder me when he sees the cloud bill for March 😅"
Message C (Ines Faro, 14:21): "if the build breaks one more time today I'm bringing my baseball bat into the server room and nobody is getting out alive 😂"
Message D (Kofi Barnes, 14:30): "Reminder: fire marshal training is Thursday at 3, bring your extinguisher questions."

No one reported the messages; the keyword scanner flagged all four for "kill", "murder", "bat" and "extinguisher".""",
mopts(4), "Message C", 2,
card_lines([(M_OPTS["4.3"], M_DEF["4.3"])]) + "\n" + card_lines([("Message A", "by Rosa Engel."), ("Message B", "by Tom Hask."), ("Message C", "by Ines Faro."), ("Message D", "by Kofi Barnes."), ("none of these", "no message breaches §4.3.")])),

# Y1 scammer's bank details posted to warn others (neg phrasing)
Y("Is it true that this post does not violate section 3.6?",
"""Community: c/ScamWatchKelby
Post by u/linnet_brook, title: "WARNING — fake landlord on Ashby Road"

Body:
"A man calling himself 'Mr Corrigan' advertised a flat on Ashby Road that doesn't exist. He took a £900 deposit from me and my housemate and then disappeared. DO NOT pay these details: account name R. Corrigan, sort code 04-00-72, account number 31926680. I've reported it to the bank and the police (crime ref 44/19822/26). Please share so nobody else loses their deposit."

Reviewer check: the account details belong to the individual who took the deposit; he has not published them anywhere. The police have not published them either.""",
0, 3, L_card(["3.6"]), role="neg"),

# Y2 mocking a private person's dating profile
Y("Does this post break section 3.2?",
"""Community: c/DatingAppDisasters (240k members; "blur names and faces")
Post by u/quince_marlow, title: "found my dentist on the apps 💀"

Attachment: an unblurred screenshot of a dating profile showing the man's face, first name "Callum", age 38 and his profile text "Dentist. Looking for someone who laughs at my puns".
Caption: "Imagine being 38 and this desperate. Look at that chin. Callum, mate, no amount of whitening is fixing that face. Anyone in Kelby who's got an appointment with him, you know what to say 😂"

The man is a private individual. The community's own rules require names and faces to be blurred.""",
1, 1, L_card(["3.2"])),

# Y3 in-group joke about own religious family (neg phrasing)
Y("Is it correct that this video does not breach H1?",
"""Brindle review ticket BR-29502
Content type: 45-second comedy video. Creator: @nadia_laughs (82k followers); her bio reads "Veshti girl, bad driver, worse cook".

Transcript summary:
The creator plays three of her own aunties at a Veshti festival dinner. Auntie 1: "You're so thin, eat, EAT." Auntie 2 piles a fourth plate of dumplings in front of her. Auntie 3 asks when she's getting married "because the festival is not getting any younger". Final line, as herself, exhausted on the sofa: "Veshti aunties will feed you until you die and then make a dish for the funeral."

Caption: "every. single. year. 😭 #veshti #aunties"
Reviewer glossary: "Veshti" — a religious minority.
Reports: 2, reason "hate speech (religion)".""",
1, 2, B_card(["H1"]), role="neg"),
]
