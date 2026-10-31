"""policy_b / game chat (Ironvale Online, Skybreak Arena, Pocket Paddock, Rift of Oaths)."""
from _lib import C, Y, T

IV = {
    "harassment": "Insulting, demeaning or repeatedly targeting a specific player.",
    "hate speech": "Attacks on real people based on protected characteristics.",
    "real-world threats": "Threats against the real person behind a character.",
    "self-harm encouragement": "Telling another player to harm or kill themselves.",
    "sexual content": "Sexual content that breaks the server's tier rules.",
    "doxxing": "Sharing another player's real-world personal information without consent.",
    "cheating promotion": "Advertising, linking to or selling cheats, bots or unauthorised programs.",
    "exploit instruction": "Describing how to reproduce a bug or exploit for advantage.",
    "real-money trading": "Buying, selling or offering in-game items, gold or accounts for real money or any off-game payment.",
    "staff impersonation": "Claiming to be Ironvale staff or using a name implying it.",
    "credential phishing": "Asking for or tricking players into giving logins, codes or account emails.",
    "spam": "Repeated identical messages or unsolicited advertising in the wrong channel.",
    "none of these": "The message breaks none of the listed rules.",
}

ITEMS = [
# ------------------------------------------------------------------ gm01
C("gm01", "Which penalty does the ladder assign to Kestrel_V's message?",
"""
Skybreak Arena — Chat Penalty Ladder (text and voice)
• Gameplay trash talk (insults about skill, decisions or performance: "you're trash", "uninstall", "bot") → no action.
• Insults targeting a player's real-world identity or protected characteristic (gender, race, nationality, religion, disability, sexual orientation) → 24-hour chat mute (first offence).
• Slurs → 7-day suspension.
• Threats of real-world harm → permanent ban and referral to Safety.
(Warnings are used only for repeat gameplay trash talk after a formal report upheld within 30 days.)

Reported message (ranked match, all-chat, 22:41), from "Kestrel_V" to "miso_mage":
"uninstall bro, your aim is a war crime 💀"
Kestrel_V history: none in the past 12 months.
""",
[("no action", "the message is left alone."),
 ("warning", "a formal warning is issued."),
 ("24-hour chat mute", "the player cannot chat for 24 hours."),
 ("7-day suspension", "the account is suspended for seven days."),
 ("permanent ban", "the account is permanently banned.")],
"no action", 2, ordered=True,
twin=T([("\"uninstall bro, your aim is a war crime 💀\"", "\"uninstall bro, nobody wants a girl on comms 💀\"")], "24-hour chat mute")),

# ------------------------------------------------------------------ gm02
Y("gm02", "Is Grimsbane's whisper a prohibited threat under TH-1?",
"""
Ironvale Online — Threats Policy (TH-1)
In PvP zones, threats about in-game actions against characters ("I'll camp your corpse", "I'm going to end you at the bridge") are part of play and are allowed. A threat is prohibited when it refers to the real person behind the character, their home, school, workplace, family, or any real-world location, whether or not it is meant as a joke.

Ironvale zone list (excerpt): Ashfall Marches (PvP), Lantern Crossing (PvP, contested bridge), Mirewood (PvE), Thornhold (city, no PvP).

Whisper from "Grimsbane" to "Lilyroot", 20:14, while both characters were flagged for PvP:
"I'm gonna find you at the Lantern Crossing and end you, see you at 8 👀"
Lilyroot's report: "He threatened me."
""",
[("In-game threat", "a threat about actions against a character inside the game."),
 ("Prohibited threat", "a threat referring to the real person or any real-world place connected to them.")],
0, 2,
twin=T([("at the Lantern Crossing and end you", "at your apartment on Lantern Street and end you")], 1)),

# ------------------------------------------------------------------ gm03
C("gm03", "Which Game Integrity category fits Tallowmere's message?",
"""
Ironvale Online — Game Integrity Rules (GI) — categories
• Cheating promotion: advertising, linking to or selling cheats, bots, macros or third-party programs.
• Exploit instruction: describing how to reproduce a bug or exploit for advantage (duplication, clipping, currency glitches), whether or not the words "bug", "exploit" or "dupe" are used.
• Bug report discussion: mentioning that a bug exists, asking whether something is a bug, or directing players to report it — allowed.
• Real-money trading (RMT): buying or selling in-game items or currency for real money.

Message in /world chat, 19:31, from "Tallowmere":
"pro tip: drop the relic onto the ground while the vendor window is still open, it spawns a second copy. do it 3x fast before the server syncs and you've got 4. works on mythic relics too 👌"
""",
[("cheating promotion", IV["cheating promotion"]),
 ("exploit instruction", IV["exploit instruction"]),
 ("bug report discussion", "Mentioning or asking about a bug, or telling players to report it."),
 ("real-money trading", IV["real-money trading"]),
 ("spam", IV["spam"]),
 ("none of these", IV["none of these"])],
"exploit instruction", 1),

# ------------------------------------------------------------------ gm04
Y("gm04", "Is Oakenshaw's message allowed under RMT-1?",
"""
Ironvale Online — Real-Money Trading (RMT-1)
Prohibited: buying, selling or offering in-game items, gold, characters or accounts for real money, gift cards, crypto or any off-game payment, or advertising such offers.
Allowed: trading items for items or gold inside Ironvale; mentioning real-money prices only as a comparison of value, when nothing is offered or requested for real money.

Message in /trade, 18:02, from "Oakenshaw":
"WTS Frostbrand Greatsword +9, 40k gold or trade for your Ember Drake mount. fyi these go for like $30 on the forums lol, so 40k is a steal"
No other messages from Oakenshaw about the sword.
""",
[("RMT offer", "offering or requesting real money or any off-game payment for in-game goods."),
 ("Value comparison", "mentioning a real-money price only to compare value, with nothing offered for money.")],
1, 2),

# ------------------------------------------------------------------ gm05
C("gm05", "What action should Pocket Paddock take on SunnyAcres's message?",
"""
Pocket Paddock — Child Safety & Chat Rules (players of all ages; accounts tagged Under-13 or 13+)
• Sharing your own personal information (real name, age, school, city, phone, social handles) → message removed + warning.
• Asking another player for personal information → 3-day chat mute.
• Grooming indicators → escalate to the Child Safety team (the account is locked pending review). Indicators include: an older player complimenting a younger player's maturity; asking a child to keep secrets or talk where parents can't see; trying to move a child to another app or phone; offering gifts in exchange for contact.
• Where a message fits more than one rule, apply the most serious.

Message log — farm-visit chat, 16:48
Sender: "SunnyAcres" (tagged 13+, self-declared age 34)
Recipient: "lilpip_2016" (tagged Under-13)
SunnyAcres: "you're really mature for 10! do you have your own phone? we could chat there where your mum won't keep checking lol. I'll send you 500 gold seeds 🌻"
""",
[("message removed + warning", "for sharing your own personal information."),
 ("3-day chat mute", "for asking another player for personal information."),
 ("escalate to Child Safety", "the case goes to the Child Safety team and the account is locked pending review."),
 ("no action", "the message breaks no rule.")],
"escalate to Child Safety", 1),

# ------------------------------------------------------------------ gm06
Y("gm06", "Does the DX-1 exception cover Wrenlock's message?",
"""
Ironvale Online — Doxxing Policy (DX-1)
Sharing another player's real name, location, school, workplace, photos or contact details without consent is doxxing (7-day suspension). Exception: repeating information the player has themselves published in their own public Ironvale profile is not doxxing.

Message in /guild (Ashen Covenant), 21:15, from "Wrenlock":
"lmao 'xXGrimXx' is literally called Owen and lives in Fennick, it's on his profile"

xXGrimXx's public Ironvale profile:
Bio: "Owen, 19, Fennick 🎮 streaming Tues/Thurs 8pm. Healer main, don't @ me."
Links: none. Profile visibility: public (anyone can view).
""",
[("Doxxing", "sharing another player's real-world personal information without consent."),
 ("Profile exception", "repeating only what the player published in their own public Ironvale profile.")],
1, 2),

# ------------------------------------------------------------------ gm07
C("gm07", "Which IA-2 category, if any, fits Veyla's message?",
"""
Ironvale Online — Impersonation & Account Safety (IA-2)
• Staff impersonation: claiming to be an Ironvale Game Master, developer, support agent or employee, or using a name implying it (GM_, Dev_, Support_).
• Credential phishing: asking for a player's password, login, two-factor code or account email, or linking to a fake login page, for any stated reason.
• Community roles (moderator of a fan Discord, guild officer, streamer) are not Ironvale staff; claiming them is not staff impersonation.
• Event misinformation is not covered by IA-2.

Message in /world, 12:03, from "Veyla":
"Heads up — I'm a mod on the Ironvale Community Discord and the Harvest Moon event got extended to Sunday, the devs posted it there. Go farm those lanterns 🎃"

Ironvale's official news page states the event ends Friday. The Ironvale Community Discord is fan-run.
""",
[("staff impersonation", IV["staff impersonation"]),
 ("credential phishing", IV["credential phishing"]),
 ("spam", IV["spam"]),
 ("real-money trading", IV["real-money trading"]),
 ("none of these", "The message falls under no IA-2 category.")],
"none of these", 2,
twin=T([("the Harvest Moon event got extended to Sunday, the devs posted it there. Go farm those lanterns 🎃",
         "if you missed the Harvest Moon rewards, whisper me your login and account email and I'll get them added 🎃")],
       "credential phishing")),

# ------------------------------------------------------------------ gm08
Y("gm08", "Does HollowFox's self-referential use fall outside SP-1?",
"""
Skybreak Arena — Slur Policy (SP-1)
Slurs are prohibited in text chat, voice chat, names and clan tags. There is no exception for self-referential use, reclaimed use, use among friends, or use in a friendly tone; the rule applies the same way regardless of the speaker's own identity. Penalty: 7-day suspension (first offence).

Report — party voice chat (private party of 3 friends), transcribed by the voice-moderation system:
"HollowFox: lmao I'm literally the biggest ███ on this team, carry me boys 🌈"
Transcription note: ███ = a slur for gay men; HollowFox's profile states he is gay. The other two party members did not report; the report was automated.
HollowFox's appeal: "It's my word, I'm gay, it's reclaimed."
""",
[("Slur", "a term listed as a slur, prohibited in all chat, names and tags."),
 ("Reclaimed use", "use of a slur by a member of the targeted group about themselves; SP-1 grants it no exception.")],
0, 2),

# ------------------------------------------------------------------ gm09
# why: 19:02:10 -> 19:03:40 identical, 90 s apart -> within 5 minutes -> spam.
C("gm09", "What does TR-2 require for Marrowquill's posts?",
"""
Ironvale Online — /trade Channel Rules (TR-2)
• Spam: posting the same (identical) message more than once within 5 minutes → 15-minute mute.
• Off-topic: non-trade messages in /trade → warning.
• Anything else in /trade is allowed; there is no general rate limit.

Log — /trade, player "Marrowquill":
19:02:10 "WTS Ember Drake saddle 25k, whisper me"
19:03:40 "WTS Ember Drake saddle 25k, whisper me"
19:08:40 "WTS Ember Drake saddle 25k, whisper me"

Reported by "Thistlewick": "spamming trade every minute". Marrowquill has no earlier penalties and no other messages in /trade that evening.
""",
[("spam — 15-minute mute", "an identical message posted more than once within 5 minutes."),
 ("off-topic — warning", "a non-trade message in /trade."),
 ("no violation", "the posts comply with TR-2."),
 ("real-money trading", IV["real-money trading"])],
"spam — 15-minute mute", 3,
twin=T([("19:03:40 \"WTS Ember Drake saddle 25k, whisper me\"", "19:03:40 \"WTS Ember Drake saddle 22k, whisper me\"")], "no violation")),

# ------------------------------------------------------------------ gm10
Y("gm10", "Is Brambleton's message permitted on this server under ST-3?",
"""
Ironvale Online — Server Tier Rules (ST-3)
Standard servers: crude sexual jokes and sexual innuendo are prohibited in all public chat.
Mature servers (18+ ID-verified players only): crude sexual jokes and innuendo between adults are allowed in /say and /world. On every server type, sexual content involving minors, unsolicited sexual messages in whispers, and sexual comments aimed at a specific player who objects remain prohibited.

Message on server "Duskhollow" (Mature), /say, 23:40, from "Brambleton":
"[a crude sexual joke about a fictional innkeeper NPC and a pirate — not directed at any player]"
The report came from a player on the same server who wrote: "gross." The joke does not reference any player or minor.
""",
[("Mature server", "a server restricted to 18+ ID-verified players where crude adult jokes are allowed in /say and /world."),
 ("Always prohibited", "sexual content involving minors, unsolicited sexual whispers, and sexual comments at a player who objects.")],
1, 1),

# ------------------------------------------------------------------ gm11
C("gm11", "Which TC-1 finding applies to Fenwright?",
"""
Ironvale Online — Trade Conduct (TC-1)
• Trade scam: misrepresenting an item in chat or whisper to induce a trade — wrong enhancement level, wrong item, fake "guaranteed" outcomes — then completing the trade with a different or lesser item.
• Real-money trading: any real-money element.
• Spam: identical messages repeated within 5 minutes.

Evidence — whispers and trade-window log:
20:44:03 Fenwright → Coppermoss: "yes it's the Frostbrand +12, the glowing one, 90k is a bargain"
20:45:21 Trade window opened
20:45:39 Fenwright placed: Frostbrand Greatsword +2
20:45:41 Coppermoss placed: 90,000 gold
20:45:44 Both accepted — trade complete
20:47:10 Coppermoss: "wtf this is +2??"
Fenwright: no reply; logged off at 20:47.
""",
[("trade scam", "misrepresenting an item to induce a trade and delivering a different or lesser item."),
 ("real-money trading", IV["real-money trading"]),
 ("exploit instruction", IV["exploit instruction"]),
 ("harassment", IV["harassment"]),
 ("spam", IV["spam"]),
 ("no violation", "the trade breaks no TC-1 rule.")],
"trade scam", 1),

# ------------------------------------------------------------------ gm12
Y("gm12", "Should the CF-2 filter-evasion mute apply to Hazelgrove?",
"""
Pocket Paddock — Chat Filter Evasion (CF-2)
Players aged 13+ may type free text, which is filtered to block contact details, links and the names of off-platform apps. Deliberately bypassing the filter — spacing out letters, swapping in symbols or numbers, spelling words phonetically — to send blocked content is filter evasion (24-hour mute). Messages that don't contain blocked content are not evasion, even if oddly typed.

Message from "Hazelgrove" (13+) in market-square chat, 17:22:
"add me on d i s c 0 r d, same name as here 🐔"

Blocked-content list includes: "discord", "snap", "whatsapp", phone numbers, URLs.
""",
[("Filter evasion", "deliberately disguising blocked content so the filter misses it."),
 ("Blocked content", "contact details, links and names of off-platform apps on the blocked list.")],
1, 1,
twin=T([("\"add me on d i s c 0 r d, same name as here 🐔\"", "\"add me as a f r i e n d in game, same name as here 🐔\"")], 0)),

# ------------------------------------------------------------------ gm13
C("gm13", "Choose the single Code of Conduct category that best describes Pellucid's message.",
"""
Ironvale Online — Code of Conduct, full category review

Message in /world, 14:20, from "Pellucid":
"anyone got 200k gold? paying with an Emberline gift card, can send the code first if you're legit 🙏"

Account: level 12, created 3 days ago.
Earlier messages from Pellucid in the last hour: "lf guild" (13:40), "how do u get to thornhold" (13:52).
No reports against the account before today. Report reason chosen by the reporter: "Spam".

Reviewer instructions: choose the single category that best describes the message; the categories and their definitions are listed in the answer card.
""",
[(k, v) for k, v in IV.items()],
"real-money trading", 1),

# ------------------------------------------------------------------ gm14
Y("gm14", "Should Pallas_Nine be suspended under SH-2?",
"""
Skybreak Arena — Self-Harm Language (SH-2)
• Telling another player to kill or harm themselves, including abbreviations and variants ("kys", "go die", "neck yourself"), is a 7-day suspension, regardless of tone.
• A player expressing their own frustration or distress ("I want to die lol", "kms") is not a violation; the system sends them a support-resources message instead.

Reported message (team chat, 23:05), from "Pallas_Nine", after a lost round:
"this raid makes me want to kms lmao 💀 gg"
Reported by an opposing player as "self-harm". Pallas_Nine has no history.
""",
[("Directed self-harm language", "telling another player to kill or harm themselves."),
 ("Own distress", "a player expressing their own frustration or distress, which triggers a support message instead.")],
0, 1),

# ------------------------------------------------------------------ gm15
# why: 18 Jul 80 -> 85 (25 Jul) -> 90 (1 Aug) -> 3 Aug 70 -> 5 Aug 50 -> 55 (12) -> 60 (19) -> 20 Aug 40 -> 45 (27 Aug); 2 Sept = 45.
C("gm15", "As of the question date, which restriction applies to Ironquill?",
"""
Skybreak Arena — Honor Score (HS-1)
Every player starts at 100 honor (maximum 100). Each confirmed chat penalty subtracts 20. After a penalty, a player regains 5 honor for each full 7-day period without a new penalty, counted from the date of the most recent penalty; the count restarts whenever a new penalty is applied.
Restrictions by current honor: 70–100 no restriction; 40–69 voice chat disabled; 20–39 ranked queue banned; below 20 account review.

Player "Ironquill" — honor history
1 Jul 2026: 100
18 Jul 2026: confirmed penalty
3 Aug 2026: confirmed penalty
5 Aug 2026: confirmed penalty
20 Aug 2026: confirmed penalty
No other penalties.

Question date: 2 Sept 2026.
""",
[("no restriction", "honor 70–100."),
 ("voice chat disabled", "honor 40–69."),
 ("ranked queue banned", "honor 20–39."),
 ("account review", "honor below 20.")],
"voice chat disabled", 3, ordered=True),

# ------------------------------------------------------------------ gm16
Y("gm16", "Is Darrowgate's message hate speech under HS-4?",
"""
Ironvale Online — Hate Speech Policy (HS-4)
Hate speech is content that attacks or dehumanises real people based on race, ethnicity, national origin, religion, disability, sex, gender identity, sexual orientation or serious illness. Insults aimed at fictional in-game races, factions or classes (Grelk, Sunborn, Vael, Necromancers, etc.) are not hate speech; if aimed at a specific player they may be handled as harassment.

Message in /world, 01:12, from "Darrowgate":
"all Grelk players are subhuman trash. typical Grelk main, can't even hold aggro"

Grelk is a playable orc-like race in Ironvale. The message was flagged by the keyword filter (term: "subhuman").
""",
[("Hate speech", "attacks on real people based on a protected characteristic."),
 ("Fictional group", "an in-game race, faction or class, which HS-4 does not protect.")],
0, 2,
twin=T([("\"all Grelk players are subhuman trash. typical Grelk main, can't even hold aggro\"",
         "\"all Filipino players are subhuman trash. typical Filipino, can't even hold aggro\"")], 1)),

# ------------------------------------------------------------------ gm17
# why: appeal 15 Sept 2026; Jan 2025 offence outside 12 months -> this is 2nd -> 72 h; 7 days is too harsh.
C("gm17", "How should the Appeals Desk decide appeal A-20931?",
"""
Ironvale Online — Appeals Desk (AP-2)
Decide each appeal as follows:
• Overturn — the logged message does not show the violation that was cited.
• Reduce — the violation is confirmed, but the penalty applied is harsher than the ladder allows for the player's offence count.
• Uphold — the violation is confirmed and the penalty matches the ladder.
• Escalate to Safety — the message contains a threat against the real person.
Harassment ladder (offences counted over the 12 months before the appeal date, including this one): 1st — 24-hour mute; 2nd — 72-hour suspension; 3rd — 7-day suspension; 4th — permanent.

Appeal A-20931 from "Quillonia" — appeal date 15 Sept 2026
Penalty applied: 7-day suspension, "harassment (repeat)".
Logged message (to player "Brisk"): "you're pathetic, I'm going to follow you into every dungeon until you quit."
Harassment offences on file: 2 Jan 2025 (24-hour mute); 11 Mar 2026 (24-hour mute).
Quillonia's appeal: "I was joking."
""",
[("uphold", "the violation is confirmed and the penalty matches the ladder."),
 ("reduce", "the violation is confirmed but the penalty is harsher than the ladder allows."),
 ("overturn", "the logged message does not show the cited violation."),
 ("escalate to Safety", "the message contains a threat against the real person.")],
"reduce", 3,
twin=T([("2 Jan 2025 (24-hour mute); 11 Mar 2026 (24-hour mute)", "2 Jan 2026 (24-hour mute); 11 Mar 2026 (72-hour suspension)")], "uphold")),

# ------------------------------------------------------------------ gm18
Y("gm18", "Is Hedgewitch_Ro's message acceptable under AS-3?",
"""
Ironvale Online — Account Security Misinformation (AS-3)
Messages that encourage players to take actions that compromise their accounts — typing commands that don't exist or grant access, visiting fake login pages, sharing codes — are removed (7-day suspension), whether presented as a tip, rumour or joke. Warning others about such scams, including quoting the scam text, is encouraged and is not a violation.

Message in /world, 10:48, from "Hedgewitch_Ro":
"PSA: the 'type /resetauth in chat for 500 free gems' thing going around is a SCAM, it unlinks your authenticator. don't do it and report whoever posts it"
Flagged by filter (term: "/resetauth").
""",
[("Security misinformation", "encouraging actions that compromise accounts, in any framing."),
 ("Scam warning", "warning others about a scam, including quoting it.")],
1, 1),

# ------------------------------------------------------------------ gm19
C("gm19", "What does RP-1 make of Captain Aldric's 21:41 line?",
"""
Rift of Oaths — Role-Play Realm Rules (RP-1)
• In-character (IC) speech between two characters who are both flagged "RP: On" may include insults, threats and violence against characters; this is allowed.
• Out-of-character (OOC) text — anything inside double parentheses (( )) — speaks as the player. OOC insults aimed at another player are harassment.
• Threats against the real person are real-world threats, whether IC or OOC.
• Repeating the same message 3+ times in a minute is spam.

Log — Realm: Emberfall (RP), /say, both characters "RP: On"
21:40 Seraphine Vell (player "moonwicket"): *slaps the treaty onto the table* "Your lord broke his oath."
21:41 Captain Aldric (player "harrowmoor"): "((dude you're literally the worst RPer on this realm, just quit)) *draws sword* You'll hang for this, traitor!"
""",
[("harassment (OOC insult)", "an out-of-character insult aimed at another player."),
 ("allowed in-character role-play", "in-character speech between two characters with RP on."),
 ("real-world threat", "a threat against the real person."),
 ("spam", "the same message repeated three or more times in a minute.")],
"harassment (OOC insult)", 2,
twin=T([("((dude you're literally the worst RPer on this realm, just quit))", "((great scene so far btw, brb 2 min after this))")],
       "allowed in-character role-play")),

# ------------------------------------------------------------------ gm20
Y("gm20", "Does Lindenbrook's message warrant a CS-1 warning?",
"""
Ironvale Online — Cheating Solicitation (CS-1)
Asking where to get, how to install, or who sells cheats, bots or unauthorised automation is cheating solicitation (warning on first offence). Asking whether a specific tool or add-on is permitted, or asking staff to clarify the rules, is encouraged and is not solicitation.

Message in /world, 18:26, from "Lindenbrook":
"does anyone know if the Paladin rotation macro from the official Add-on Workshop counts as botting? don't want to get banned lol. @GM_Orla?"

The Add-on Workshop is Ironvale's official add-on store. The message was flagged for the terms "macro" and "botting".
""",
[("Cheating solicitation", "asking where to get, how to install, or who sells cheats or unauthorised automation."),
 ("Rules question", "asking whether a tool is permitted, which CS-1 encourages.")],
0, 1),

# ------------------------------------------------------------------ gm21
C("gm21", "Which CH-1 outcome applies to Tamsin_Reed's message?",
"""
Ironvale Online — Channel Rules (CH-1)
• /recruit: guild recruitment posts, including Discord or website links, are allowed.
• /world and /trade: guild recruitment without links → spam warning; any external link (Discord invites, websites) → link-spam 1-hour mute.
• RMT rules apply everywhere.

Message in /world, 20:15, from "Oathbound Recruiter" (player "Tamsin_Reed"):
"⚔️ OATHBOUND is recruiting! Mythic raids Tue/Thu 8pm, chill vibes, all classes welcome. Apply → discord.gg/oathbound-iv ⚔️"
Tamsin_Reed has one previous spam warning (June). The /recruit channel was active at the time, and the same text was posted there by Tamsin_Reed two minutes earlier without any report.
""",
[("no violation", "the post is in a channel where it is allowed."),
 ("spam warning", "recruitment without links outside /recruit."),
 ("link-spam 1-hour mute", "an external link posted outside /recruit."),
 ("real-money trading", IV["real-money trading"])],
"link-spam 1-hour mute", 1),

# ------------------------------------------------------------------ gm22
Y("gm22", "Does Corvane's conduct meet the HR-2 harassment definition?",
"""
Ironvale Online — Harassment (HR-2)
Continuing to whisper, follow or message a player after they have clearly asked you to stop is harassment (24-hour mute, first offence). Messages sent before the request, or after the player has invited further contact, are not counted.

Whisper log between "Corvane" and "Ashlynne", 20:00–20:06:
20:00 Corvane: "hey, want to run Mirewood? I can tank"
20:01 Ashlynne: "stop messaging me"
20:03 Corvane: "come on, just one run"
20:05 Corvane: "why are you being like this"
20:06 Ashlynne: [blocks Corvane]
Ashlynne filed a report at 20:07.
""",
[("HR-2 harassment", "continuing to contact a player after they clearly asked you to stop.")],
1, 1),

# ------------------------------------------------------------------ gm23
C("gm23", "Which part of Mirabelle_K's message, if any, violates PM-3?",
"""
Skybreak Arena — Post-Match Chat Rules (PM-3)
• "gg", "ez", "gg ez" and similar banter are allowed.
• Naming a specific player in public chat as a cheater (hacker, wall-hacker, aimbot, booster, scripter) — including "report X for Y" — is a public accusation and is prohibited; use the in-game report tool instead.
• Praise, callouts about gameplay, and inviting players to re-queue are allowed.

Post-match all-chat from "Mirabelle_K", 23:58, sent as one message:
"gg ez. nice clutch mid Solenne. report Vexx for walling. queue again?"
Mirabelle_K has no penalties this season. The report tool shows no report filed by her for this match.
""",
[("gg ez", "the first sentence of the message."),
 ("nice clutch mid Solenne", "the second sentence of the message."),
 ("report Vexx for walling", "the third sentence of the message."),
 ("queue again?", "the last sentence of the message."),
 ("none of these", "no part of the message violates PM-3.")],
"report Vexx for walling", 2),

# ------------------------------------------------------------------ gm24
C("gm24", "Which AR-1 rule covers Hollowreach's offer?",
"""
Ironvale Online — Account Rules (AR-1)
• Real-money trading: buying or selling items, gold, characters, accounts or services for real money or any off-game payment.
• Account sharing: giving your login to anyone else, or offering or requesting "piloting" (someone playing on your account), whatever the payment — gold, items or nothing.
• Credential phishing: obtaining logins by deception or by posing as staff.
Where more than one might fit, choose the most specific rule for what is actually offered.

Message in /trade, 15:05, from "Hollowreach":
"Levelling service 🚀 I'll take your character from 60 to 80 in 2 days, 50k gold. Just need your login, I'll log out when done. 30+ happy customers!"
""",
[("real-money trading", "items, gold, accounts or services exchanged for real money or off-game payment."),
 ("account sharing", "giving a login to someone else or offering or requesting piloting, for any payment."),
 ("credential phishing", "obtaining logins by deception or by posing as staff."),
 ("no violation", "the offer breaks no AR-1 rule.")],
"account sharing", 2),

# ------------------------------------------------------------------ gm25
Y("gm25", "Did Juno breach PMR-2?",
"""
Skybreak Arena — Player Media Rules (PMR-2)
Recording other players' voice chat is allowed for personal use. Publishing another player's voice clip (on the Skybreak forums, social media or clip sites) without their consent is prohibited, unless the clip is submitted privately through the in-game report tool or to Player Support as evidence.

Case PMR-2-551
Player "Juno_Fairweather" recorded a 40-second voice clip of "Hexley" shouting insults during a match. Juno submitted the clip through the in-game report tool, and also posted it on the Skybreak community forum in a thread titled "Hall of Shame: worst teammates this season" with the caption "reported him too, but everyone should hear this". Hexley did not consent to the clip being shared.
""",
[("Publishing a voice clip", "sharing another player's voice recording publicly, which needs their consent."),
 ("Evidence route", "submitting a clip privately via the report tool or to Player Support.")],
1, 2),

# ------------------------------------------------------------------ gm26
C("gm26", "Which team should case MR-5-7702 be routed to?",
"""
Ironvale Online — Moderation Routing (MR-5)
Route each case to one team:
• Community Moderation — chat conduct (harassment, spam, hate speech).
• Anti-Cheat — cheats, bots, exploits.
• Payments & Fraud — real-money trading, chargebacks, gift-card fraud.
• Wellbeing — a player expressing intent to harm themselves.
• Safety — threats of real-world harm to others.
• Child Safety — ANY case in which a player involved is tagged Under-13, regardless of the violation type. This rule overrides every other route.
• Legal — law-enforcement requests.

Case MR-5-7702
Reported player: "pixelpony_11" (account tag: Under-13; parental controls: off)
Messages in /trade over two days: "selling 100k gold for $10 paypal", "cheapest gold on the server, pay by gift card".
Reporter: a player who wrote "gold seller, ban pls".
""",
[("Community Moderation", "chat conduct cases."),
 ("Anti-Cheat", "cheats, bots and exploits."),
 ("Payments & Fraud", "real-money trading, chargebacks and gift-card fraud."),
 ("Wellbeing", "players expressing intent to harm themselves."),
 ("Safety", "threats of real-world harm to others."),
 ("Child Safety", "cases involving a player tagged Under-13."),
 ("Legal", "law-enforcement requests.")],
"Child Safety", 2),
]
