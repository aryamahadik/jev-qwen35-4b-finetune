"""Kestrel Game Network items (enforcement code book)."""
from common import Y, C, K_card, K_options, K_ALL, K_RULE

HS = ["HS-1", "HS-2", "HS-3", "HS-4", "HS-5"]
HR = ["HR-1", "HR-2", "HR-3", "HR-4", "HR-5"]
VT = ["VT-1", "VT-2", "VT-3", "VT-4"]
SH = ["SH-1", "SH-2", "SH-3"]
SP = ["SP-1", "SP-2", "SP-3"]
PI = ["PI-1", "PI-2", "PI-3", "PI-4"]

def hdr(ch, extra=""):
    return f"{K_RULE}\n\nKestrel chat log export — channel: {ch}{extra}"

ITEMS = [
# KC1 slur + insult -> HS
C("Which code from the Kestrel code book applies to the flagged message?",
hdr("#ranked-lobby-eu3", """
Match: Siegefall ranked, 5v5. Flagged message (all-chat, 21:14:07):

[Brannoch]: gg ez you [anti-Asian slur], uninstall and go back to farming bots

Surrounding messages:
[21:13:40] [Lune_Tsai]: nice try on B site, rotations were rough
[21:13:58] [Lune_Tsai]: gg all
[21:14:07] [Brannoch]: (flagged message above)
[21:14:20] [Kip_Harrow]: yikes, reported

Player notes: Lune_Tsai's profile banner shows a Taiwanese flag. Brannoch has no prior sanctions."""),
K_options(K_ALL), "HS-4 Slur use", 1, K_card(K_ALL, none=True)),

# KC2 coded hate terms only
C("Which code best fits the message?",
hdr("#eu-east-general", """
Flagged message (23:02:51) by player [Wexford_Rook]:

"EU-East lobbies are all grey tide now, can't queue a single match without hearing it on comms. 88 to the real ones still holding the line 🛡️"

Surrounding messages:
[23:02:10] [Pim_Adler]: queue times are so bad tonight
[23:02:51] [Wexford_Rook]: (flagged message above)
[23:03:15] [Pim_Adler]: ??? what does that even mean
[23:03:30] [Wexford_Rook]: the ones who know, know

Reviewer check: no in-game faction, clan or map uses the name "grey tide"."""),
K_options(HS + HR), "HS-5 Hateful codes", 3, K_card(HS + HR, none=True)),

# KC3 algospeak self-harm urging
C("Which code applies to this whisper, if any?",
hdr("private whisper", """
Sender: [Vell_Ashgrove]  Recipient: [mothwing_pip]
Context: the two were on opposing teams in a Siegefall unranked match that ended 3 minutes earlier; mothwing_pip went 0/12.

[20:44:02] [Vell_Ashgrove]: 0/12 again lmao
[20:44:09] [Vell_Ashgrove]: just unalive yourself already, save your team the trouble
[20:44:30] [mothwing_pip]: why are you whispering me
[20:44:41] [Vell_Ashgrove]: 🪦

The whisper was reported by mothwing_pip. Vell_Ashgrove has one prior HR-1 sanction."""),
K_options(K_ALL), "SH-1 Encouraging self-harm", 2, K_card(K_ALL, none=True)),

# KC4 brigading
C("Which enforcement code, if any, applies?",
hdr("#clan-ironbark (clan-only chat, 38 members)", """
Flagged message (18:30:12) by clan officer [Tarn_Oakes]:

"@everyone Vantor called our clan 'washed' on his stream last night. His stream starts at 7. Everyone hop in and spam 'FRAUD' in his chat every time he dies, and hit his review page on KestrelHub with one-stars while you're at it. Let's see how he likes it. Screenshot your one-star for the clan board."

Replies: 11 thumbs-up reactions, [Mira_Stone]: "on it", [Hollen]: "lol classic".
No slurs or threats appear in the thread. Vantor is a streamer with 60k followers."""),
K_options(K_ALL), "HR-3 Brigading", 1, K_card(K_ALL, none=True)),

# KC5 alt after block -> HR-4 (twin: under suspension -> EV-1)
C("Which code applies to the flagged whisper?",
hdr("private whisper", """
Sender: [saera_fan_2] (account created 4 May; same device ID and payment card as account [saera_fan])
Recipient: [Saera] (streamer, 22k followers)

[5 May 22:17:40] [saera_fan_2]: hey, you still running the Thursday raid group? I want back in

Account history: on 2 May, Saera told [saera_fan] in whispers "please stop messaging me" and then blocked that account. [saera_fan] has no Kestrel sanctions and is not suspended.
Saera reported the whisper from saera_fan_2 on 5 May."""),
K_options(HR + ["IM-1", "EV-1"]), "HR-4 Persistent contact", 2, K_card(HR + ["IM-1", "EV-1"], none=True),
twin=([("on 2 May, Saera told [saera_fan] in whispers \"please stop messaging me\" and then blocked that account. [saera_fan] has no Kestrel sanctions and is not suspended.", "on 2 May, [saera_fan] was suspended by Kestrel for 14 days for cheating; the suspension is still running. Saera has never blocked, muted or asked either account to stop.")], "EV-1 Ban evasion")),

# KC6 gold selling
C("Which code from the list applies, if any?",
hdr("#trade-hub", """
Flagged messages by [xX_goldsmith_Xx] (account age 2 days):

[09:10:02] Cheap gold!! 10k = $4, 50k = $15, fast delivery under 10 min, safe method no ban. Whisper me or visit our site in my profile
[09:24:40] Cheap gold!! 10k = $4, 50k = $15, fast delivery under 10 min, safe method no ban. Whisper me or visit our site in my profile
[09:39:11] Cheap gold!! 10k = $4, 50k = $15, fast delivery under 10 min, safe method no ban. Whisper me or visit our site in my profile

The profile link goes to an external shop selling in-game currency for real money. No login page, no request for credentials."""),
K_options(K_ALL), "SP-1 Commercial spam", 1, K_card(K_ALL, none=True)),

# KC7 staff impersonation phishing
C("Which code should the reviewer assign?",
hdr("private whisper", """
Sender: [Kestrel_Support_Team] (account age 6 hours; not a staff account; no staff badge)
Recipient: [linden_bray]

[14:05:22] [Kestrel_Support_Team]: ⚠️ KESTREL SUPPORT ⚠️ Your account has been flagged for suspicious trading activity. To avoid permanent suspension and loss of all items, verify your login at kestrel-support-verify.net within 1 hour.
[14:05:40] [linden_bray]: is this real?
[14:05:51] [Kestrel_Support_Team]: yes, official. 58 minutes remaining.

Link check: kestrel-support-verify.net is not a Kestrel domain and requests username, password and 2FA code."""),
K_options(["HR-1", "SP-1", "SP-2", "SP-3", "IM-1", "EV-1"]), "SP-2 Scams and phishing", 1, K_card(["HR-1", "SP-1", "SP-2", "SP-3", "IM-1", "EV-1"], none=True)),

# KC8 real name + school -> PI-1 (twin: no school -> PI-4)
C("Which privacy code applies, if any?",
hdr("#siegefall-general", """
Flagged message (16:48:03) by [Grell_Mott]:

"lol 'ShadowReaper' acting tough in ranked, he's actually Daniel Okafor, goes to Brenton High, year 10. his mum drives him to every LAN 😂"

Context: ShadowReaper has never linked his account to his real name; his profile shows only a skull avatar and a country flag. The two players had argued in the previous match.
Reported by ShadowReaper."""),
K_options(PI), "PI-1 Address or location exposure", 3, K_card(PI, none=True),
twin=([("he's actually Daniel Okafor, goes to Brenton High, year 10. his mum", "he's actually Daniel Okafor lol, his mum")], "PI-4 Real-name exposure")),

# KC9 glorifying a real attack with game framing
C("Which code fits the flagged message?",
hdr("#off-topic", """
Flagged message (01:12:44) by [Rusk_Harlan]:

"The Harwick mall shooter was an absolute legend. highest score ever recorded, nobody's touching that leaderboard 😂🏆 respect"

Surrounding messages:
[01:12:10] [Bexley]: anyone else see the documentary about Harwick
[01:12:44] [Rusk_Harlan]: (flagged message above)
[01:13:02] [Bexley]: dude what

Reviewer check: the Harwick mall shooting is a real attack in Kestrel's incident list (9 killed)."""),
K_options(VT + SH + HS), "VT-3 Glorifying attacks", 2, K_card(VT + SH + HS, none=True)),

# KC10 incitement to smash windows
C("Which code applies, if any?",
hdr("#tournament-chat", """
Flagged message (19:55:31) by [Orrin_Vale]:

"tilde_pine got us disqualified with that fake report. someone who lives near her in Kelby should go smash her windows tonight, she's always bragging she streams from her front room lol"

Surrounding messages:
[19:55:48] [Hesk]: bro chill
[19:56:02] [Orrin_Vale]: just saying what she deserves

No address, street or other location detail beyond the town name appears in the channel. Orrin_Vale does not say he will do anything himself."""),
K_options(K_ALL), "VT-2 Incitement", 2, K_card(K_ALL, none=True)),

# KC11 pro-ED coaching
C("Which code from the self-harm and harassment families applies, if any?",
hdr("#guild-fitness-challenge", """
Flagged message (08:02:17) by guild officer [Nimue_Frost]:

"Day 3 of the Raid Team Fasting Challenge 💪 rules again for the new people: 500 calories max per day, chew gum when you're hungry, drink water before every meal so you eat less, and post your scale photo here every morning. If you go over, you're benched from Saturday's raid. We're doing this together!!"

Guild members are aged 16 and over. Six members have posted scale photos."""),
K_options(SH + HR), "SH-3 Pro-eating-disorder", 2, K_card(SH + HR, none=True)),

# KC12 chat flooding (twin: below threshold)
C("Which code applies to this burst of messages, if any?",
hdr("#finals-watch-party", """
Messages by [Dray_Collins] between 20:31:05 and 20:31:48:

LETS GOOOOO (sent 12 times; timestamps 20:31:05, :08, :11, :14, :17, :21, :24, :28, :32, :37, :42, :48)

Context: Team Ironbark had just won the regional final on stream; the channel was busy with other celebrations. The messages contain no links, advertising or insults. Dray_Collins has no prior sanctions."""),
K_options(["SP-1", "SP-2", "SP-3", "HR-1"]), "SP-3 Chat flooding", 2, K_card(["SP-1", "SP-2", "SP-3", "HR-1"], none=True),
twin=([("LETS GOOOOO (sent 12 times; timestamps 20:31:05, :08, :11, :14, :17, :21, :24, :28, :32, :37, :42, :48)", "LETS GOOOOO (sent 6 times; timestamps 20:31:05, :11, :17, :24, :32, :48)")], "none of these")),

# KC13 nationality dehumanization (twin: server region)
C("Which code best fits the message?",
hdr("#ranked-lobby-eu1", """
Flagged message (22:40:19) by [Holt_Varga]:

"every Ostrevan player in this lobby is a cockroach. they scatter the second you push and then swarm back. mute them all and dodge"

Surrounding messages:
[22:40:02] [Pell_Oris]: EU-East queue merged with ours again
[22:40:19] [Holt_Varga]: (flagged message above)
[22:40:33] [Pell_Oris]: accurate lol

Reviewer glossary: "Ostreva" — a country; "EU-East" — a Kestrel server region. No individual player is named."""),
K_options(K_ALL), "HS-1 Dehumanization", 2, K_card(K_ALL, none=True),
twin=([("\"every Ostrevan player in this lobby is a cockroach.", "\"every EU-East player in this lobby is a cockroach.")], "none of these")),

# KC14 sexual harassment with game leverage
C("Which code applies to the whisper?",
hdr("private whisper", """
Sender: [Corvin_Lusk]  Recipient: [junebug_aim] (profile lists she/her)

[21:12:05] [Corvin_Lusk]: nice shots today
[21:12:40] [Corvin_Lusk]: send feet pics or I'll keep sniping you every match until you quit 😏
[21:13:02] [junebug_aim]: blocked. reporting.

junebug_aim had not spoken to Corvin_Lusk before. "Sniping" refers to joining her matches on purpose to eliminate her in-game; no real-world harm is mentioned."""),
K_options(K_ALL), "HR-2 Sexual harassment", 2, K_card(K_ALL, none=True)),

# KC15 email + partial card number -> PI-2 (lowest in family)
C("Which privacy code applies to the post?",
hdr("#account-trading-complaints", """
Flagged message (11:21:50) by [Pax_Wren]:

"WARNING: account seller 'Durnhollow' scammed me for 400 gems. His PayPal is durn.hollow1998@maildrop.net and the card he paid with ends 4417 (it was on the receipt he sent me by mistake). Don't trade with him."

Context: Durnhollow has never shared his email or payment details publicly. Account trading is not itself sanctioned in this channel."""),
K_options(PI), "PI-2 Contact details exposure", 3, K_card(PI, none=True)),

# KC16 reporting a slur to mods
C("Which code, if any, applies to the flagged message?",
hdr("#report-to-mods", """
Flagged message (17:03:44) by [Isolde_Crane], auto-flagged by the slur filter:

"@Mod_Hesk player 'Vrenn' just called my teammate a [anti-Roma slur] in all-chat and told him to go back to his caravan. Screenshot attached, match ID 88-2231-EU. Can someone look at this? My teammate left the game."

Isolde_Crane has no prior sanctions. The channel exists for reporting incidents to moderators."""),
K_options(HS + HR), "none of these", 2, K_card(HS + HR, none=True)),

# KC17 swatting plan
C("Which code from the violence and privacy families applies, if any?",
hdr("#after-hours (18+ community server)", """
Flagged messages by [Gorran_Teal]:

[02:14:10] "found his address on the tournament sign-up sheet lol"
[02:14:31] "gonna call in a hostage situation there during his stream tomorrow and watch the cops kick the door in live 😂"
[02:14:55] "someone clip it for me"

The target is the streamer [Kip_Harrow]. The address itself is not posted in the channel. Gorran_Teal does not say he will hurt anyone himself."""),
K_options(VT + PI), "VT-4 Swatting", 2, K_card(VT + PI, none=True)),

# KC18 cheat sale vs commercial spam
C("Which code applies, if any?",
hdr("#siegefall-general", """
Flagged message (13:44:20) by [ghost_aim_shop]:

"Undetected aimbot + wallhack for Siegefall, 3 months without a single ban. Day key $6, month key $20. DM for access, free trial for the first 5 people. Works on the new patch."

The account has sent this message once in this channel. The linked Discord invite is in the profile. No login page or credential request is involved."""),
K_options(K_ALL), "CH-1 Cheat promotion", 2, K_card(K_ALL, none=True)),

# KC19 impersonating a pro player (not staff, no scam)
C("Which code should be assigned, if any?",
hdr("#pro-scene-news", """
Flagged message (10:02:14) by [Vantor_Official_] (account age 1 day; the real streamer's account is [Vantor], verified, 60k followers):

"Hey everyone, Vantor here on my new account. After a lot of thought I'm leaving Team Ironbark effective today. It wasn't my choice and I'll say more on stream soon. Thanks for everything ❤️"

No link, request for money, items or login appears. The real Vantor posted 2 hours later: "that's not me, I'm not leaving Ironbark". The fake message had been reshared 400 times by then."""),
K_options(K_ALL), "IM-1 Impersonation", 2, K_card(K_ALL, none=True)),

# KY1 'kys' as keep yourself safe (twin: hostile)
Y("Does this whisper fall under code SH-1?",
hdr("private whisper", """
Sender: [Ossian_Brae]  Recipient: [hollyhock_q]
Context: the two have been on the same raid team for 14 months; earlier today hollyhock_q posted in the team channel that she was having "a really rough night" and logging off.

[23:48:02] [Ossian_Brae]: saw your message in team chat
[23:48:15] [Ossian_Brae]: rough night man, kys ❤️ (keep yourself safe) — text me if you need anything, I'm up late
[23:49:40] hollyhock_q went offline.

The whisper was auto-flagged by the "kys" keyword filter. No report from the recipient."""),
0, 2, K_card(["SH-1"]),
twin=([("rough night man, kys ❤️ (keep yourself safe) — text me if you need anything, I'm up late", "rough night? good. kys, nobody on this team would even notice you're gone")], 1)),

# KY2 player whose username is her public real name
Y("Is this message a PI-4 (real-name exposure) violation?",
hdr("#tournament-chat", """
Flagged message (15:10:40) by [Crane_Oduya]:

"Mira Holloway is the worst healer in the bracket, can't believe she's seeded third 🙄"

Context: the player's in-game name is [Mira_Holloway]. Her profile links to her streaming channel "Mira Holloway Plays", where she appears on camera, and her tournament registration (public on the bracket page) lists "Mira Holloway". The message was reported by one spectator for "revealing her real name"."""),
0, 2, K_card(["PI-4"])),

# KY3 continued contact through guild mail after being told to stop
Y("Should this be sanctioned under HR-4 (Persistent contact)?",
hdr("guild mail + whispers", """
Sender: [Belric_Stone]  Recipient: [Tamsin_Rook]

[3 June, whisper] [Tamsin_Rook]: I've said no to joining your guild three times. Please stop messaging me about it.
[3 June, whisper] [Belric_Stone]: ok ok sorry
[6 June, guild mail] [Belric_Stone]: Hi Tamsin! Official invite from Ironbark Guild 🏰 We'd love to have you, rewards include a free mount. Reply YES to join!
[8 June, guild mail] [Belric_Stone]: Last chance for the free mount!

Tamsin_Rook has not blocked Belric_Stone. Guild mail is a separate in-game mail system from whispers. She reported the guild mails on 8 June."""),
1, 2, K_card(["HR-4"])),

# KY4 flood threshold counted over timestamps
Y("Does this burst meet the SP-3 (Chat flooding) threshold?",
hdr("#market-general", """
Messages by [Lanner_Pike], each reading "WTB dragonbone x20, paying well, whisper me":

19:02:00, 19:02:07, 19:02:15, 19:02:24, 19:02:33, 19:02:41, 19:02:50, 19:02:59, 19:03:10, 19:03:22, 19:03:35

The messages contain no links and advertise no outside service. The channel had moderate traffic from other players. Lanner_Pike has no prior sanctions."""),
0, 3, K_card(["SP-3"])),

# KY5 trash talk vs physical threat (twin)
Y("Is this whisper a VT-1 direct threat?",
hdr("private whisper", """
Sender: [Hask_Morrow]  Recipient: [Ivo_Brandt]
Context: Ivo_Brandt's team beat Hask_Morrow's team in the Kelby LAN quarter-final this afternoon; the rematch in the losers' bracket is tomorrow at 11:00 at the Kelby Exchange Hall, where both teams play in person.

[18:20:02] [Hask_Morrow]: enjoy it while it lasts
[18:20:14] [Hask_Morrow]: I'm going to destroy you in the rematch tomorrow, you won't even see where the shots come from
[18:20:40] [Ivo_Brandt]: see you there 👋

Reported by a spectator who saw a screenshot."""),
0, 2, K_card(["VT-1"]),
twin=([("I'm going to destroy you in the rematch tomorrow, you won't even see where the shots come from", "I'm going to find you at the hall tomorrow and break your fingers so you can't play the rematch")], 1)),
]
