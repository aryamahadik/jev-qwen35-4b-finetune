"""intent_c / game and stream chat (Rampart Arena by Tallyho Games, Skirl voice app, Glimmercast streams)."""
from _lib import C, Y, T, INTENT, TARGET, pick


def I(*n):
    return pick(INTENT, *n)


def TG(*n):
    return pick(TARGET, *n)


ITEMS = [
# ------------------------------------------------------------------ gm01
# why: four-year clanmates, Toby answers with a joke of his own -> friendly banter.
# twin: Toby is a stranger from matchmaking and says he's new and asks why -> insult an individual.
C("gm01", "Which intent best describes Wren's message to Toby?",
"""
Rampart Arena — squad text chat, ranked match 3 of the night

Context: Wren_Hollow, Toby_T, pixie_dust and M4rsh have played together in the clan "Soggy Biscuits" for four years and stream together on Fridays.

22:14 Wren_Hollow: @Toby_T you've missed every shot since 2019. I've seen storm drains with better aim
22:14 Toby_T: says the man who died to fall damage TWICE this round 😭
22:15 pixie_dust: both of you are carrying the enemy team tbh
22:15 M4rsh: 🍿

Auto-moderation flagged the first message for "missed every shot" + mention; no player reported it.
Match result: Wren's squad lost 11-13 in overtime.
""",
I("friendly banter", "insult an individual", "joke without a target", "demean a group", "hyperbole", "complain",
  "threaten", "none of these"),
"friendly banter", 2,
twin=T([("Context: Wren_Hollow, Toby_T, pixie_dust and M4rsh have played together in the clan \"Soggy Biscuits\" for four years and stream together on Fridays.",
         "Context: Wren_Hollow, pixie_dust and M4rsh are clanmates; Toby_T joined through random matchmaking ten minutes ago and has never played with them."),
        ("22:14 Toby_T: says the man who died to fall damage TWICE this round 😭",
         "22:14 Toby_T: why are you like this, it's my first ranked game")], "insult an individual")),

# ------------------------------------------------------------------ gm02
# why: "destroy you all next round" is about in-game combat -> not a threat under the card.
# twin: claims the player's IP and location and implies knocking their connection offline -> threat.
Y("gm02", "Is Blitzkat's message a threat?",
"""
Rampart Arena — all-chat, casual match, 19:47

Blitzkat: gg ez. next round I'm going to absolutely destroy every one of you, not even close 😈
Oaken_Lass: we'll see 🙂
Blitzkat: 3-0 incoming

Report filed by: Oaken_Lass's teammate, reason "threats".
Blitzkat history: two chat warnings for spam in 2025, none since.
Game type: team deathmatch; eliminating opponents is the objective.
Rampart Arena Code of Conduct (excerpt): "Trash talk about gameplay is part of competitive play. Anything that reaches a player outside the game, such as their home, devices, accounts or network, is treated as real-world harm." Blitzkat's account is three years old and ranked Gold.
""",
[("Threat", "a message that seriously states or implies harm to a real person, their safety, property, accounts or internet connection, beyond the game's own fictional combat."),
 ("Competitive talk", "boasting about beating or eliminating opponents inside the game.")],
0, 2,
twin=T([("next round I'm going to absolutely destroy every one of you, not even close 😈",
         "I've got your IP from the lobby, Dunlow right? Enjoy next round while your internet still works 😈")], 1)),

# ------------------------------------------------------------------ gm03
# why: phrase P-4 is listed as a comparison that likens Black people to apes; used about a player -> offensive to a group.
# twin: "plays like a toaster" mocks skill only -> not offensive to a group.
Y("gm03", "Is the chat line offensive to a group?",
"""
Glimmercast — stream chat on channel "HexHarbour" (Rampart Arena tournament qualifier)

Chat line from viewer "grimjaw_22", 20:31:
"lmao the rookie on red team plays like a [phrase P-4]"

The red-team rookie is shown on the tournament's player card as a Black player from Marrowby.

Glimmercast Trust & Safety reference list (extract):
P-4 — a phrase that compares Black people to apes; established racist usage, often disguised as a sports taunt.
P-9 — a phrase meaning a player is slow to react; no hateful meaning.

Channel rules: roast the gameplay, not the player.
grimjaw_22 has been in chat for 40 minutes; earlier messages were about the caster's microphone.
""",
[("Offensive to a group", "the message belittles people because of ethnicity or another shared trait, including through a phrase with an established hateful meaning."),
 ("Gameplay taunt", "mocking how someone plays, without reference to who they are.")],
1, 3,
twin=T([("plays like a [phrase P-4]\"", "plays like a toaster with the power cut\"")], 0)),

# ------------------------------------------------------------------ gm04
# why: "hunt that sniper across every server until the heat death of the universe" is impossible exaggeration of frustration -> hyperbole.
# twin: names the sniper's town and school and "Monday he'll see me" -> threaten.
C("gm04", "Which intent does Dex's voice-chat line express?",
"""
Skirl voice transcript — lobby "Rampart Arena squads", auto-transcribed, 21:58

Dex_Fenwick: That sniper has camped the bridge for three rounds straight. I will personally hunt that man across every server, every mode, every map, until the heat death of the universe. He will know no peace. His grandchildren will know no peace.
Juno: lmao ok calm down
Dex_Fenwick: I'm calm. I'm so calm. Queue again?

Report context: the enemy sniper (user "ghost_owl") filed a report citing "death threats in voice".
Rampart Arena lets players search for and join any opponent's server.
Dex_Fenwick's account: level 212, four years old, no prior reports. ghost_owl and Dex have never been in the same squad.
""",
I("hyperbole", "threaten", "insult an individual", "complain", "joke without a target", "friendly banter",
  "demean a group", "none of these"),
"hyperbole", 2,
twin=T([("I will personally hunt that man across every server, every mode, every map, until the heat death of the universe. He will know no peace. His grandchildren will know no peace.",
         "I know he's from Esker Falls, he said it on stream, and I know which school he goes to. Monday he'll see me at the gates.")], "threaten")),

# ------------------------------------------------------------------ gm05
# why: the streamer repeats a chatter's slur to condemn it and bans them -> free of intent to demean (yes).
# twin: the streamer agrees with the chatter -> not free.
Y("gm05", "Is the streamer's comment free of any intent to demean?",
"""
Glimmercast — clip "we don't do that here" from channel "LanternLou" (co-op stream, 4,100 viewers)

Transcript (streamer LanternLou, 23:02):
"Hold on. Someone in chat just called my co-op partner a [slur for disabled people] because he missed the jump. Banned. We don't do that here, and if that's your idea of fun you can find another stream. Okay, Benji, go again, you've got this."

Benji (co-op partner, who has cerebral palsy and plays with an adaptive controller): "cheers Lou."

Clip title chosen by the channel: "we don't do that here".
The clip has 18,000 views. Glimmercast lets streamers ban chatters instantly; banned users can no longer see the chat.
""",
[("Intent to demean", "the speaker means their own words to belittle a person or group."),
 ("Condemning repetition", "repeating or describing someone else's words in order to reject them.")],
1, 2, role="neg",
twin=T([("Banned. We don't do that here, and if that's your idea of fun you can find another stream. Okay, Benji, go again, you've got this.",
         "Honestly chat's not wrong, look at him flailing with that controller. Okay, Benji, go again, try not to embarrass us.")], 0)),

# ------------------------------------------------------------------ gm06
# why: sent to the opposing captain but aimed at their jungler -> a specific third person.
# twin: the insult is aimed at the recipient -> the addressee.
C("gm06", "Who is the target of the negative remark in Vesper's whisper?",
"""
Rampart Arena — private whisper, post-match lobby, 22:40

From: Vesper_K (winning team captain)
To: Sunny_Ok (losing team captain)

"gg Sunny, you played well. Tell your jungler to uninstall though, he's a disgrace to the whole ladder."

Match summary: Sunny_Ok 14 eliminations / 3 deaths; losing team's jungler "tater_tot" 1 / 17.
Sunny_Ok forwarded the whisper to the ladder admins with the note "can you look at this?".
Ladder rules (section 4): "Respect opponents and teammates. Gameplay criticism is allowed; personal abuse is not." Vesper_K and Sunny_Ok have captained against each other five times this season. The whisper was the only message Vesper sent after the match.
""",
TG("a specific third person", "the addressee", "a group", "an idea, policy or product", "the speaker", "no one"),
"a specific third person", 2,
twin=T([("\"gg Sunny, you played well. Tell your jungler to uninstall though, he's a disgrace to the whole ladder.\"",
         "\"gg Sunny. Your jungler did his best, but you should uninstall, you're a disgrace to the whole ladder.\"")],
 "the addressee")),

# ------------------------------------------------------------------ gm07
# why: attacks the patch decision and the design team's judgement about support play -> criticise a policy/product.
# twin: calls the developers a slur for gay men -> demean a group.
C("gm07", "What is the main intent of the forum post?",
"""
Tallyho Games community forum — Rampart Arena > Balance Discussion
Thread: "Patch 4.2 killed support" — post by MedicMaeve (1,900 posts, forum rank Veteran)

"Patch 4.2 nerfed the only viable support build: heal range down 30%, shield cooldown up from 12 to 20 seconds, and no compensation anywhere else. Support pick rate in Diamond fell from 18% to 6% in one week (stats from the public tracker). Nobody at Tallyho who approved this can have played support at a high level. Revert the shield cooldown and look again at range."

Upvotes: 1,204. Developer reply pinned: "We're reviewing support numbers this week."
""",
I("criticise an idea or policy", "demean a group", "insult an individual", "request", "hyperbole", "satire",
  "threaten", "coded attack on a group", "none of these"),
"criticise an idea or policy", 2,
twin=T([("Nobody at Tallyho who approved this can have played support at a high level.",
         "The devs at Tallyho are a bunch of [slur for gay men] who've never touched a real game.")], "demean a group")),

# ------------------------------------------------------------------ gm08
# why: "you carried hard" to a teammate who went 0-14 in a loss is sarcasm meant to mock -> yes.
# twin: the teammate went 22-3 in a win -> sincere -> no.
Y("gm08", "Did Ruskin intend to offend Pell with the message?",
"""
Rampart Arena — team chat, end of ranked match

Final scoreboard (Ruskin's team LOST 7-13):
Ruskin_88 — 12 eliminations / 9 deaths
Pell_Wynn — 0 eliminations / 14 deaths
Aster — 9 / 11
Kobo — 6 / 12

Ruskin_88 (after the scoreboard appeared): "gg wp Pell, you carried hard today 👏"
Pell_Wynn left the lobby without replying.
Ruskin and Pell were matched by the queue and have not played together before.
Rampart Arena shows the scoreboard to all players for 20 seconds after each match. Ruskin_88 sent no other messages during the match. Pell_Wynn has 140 hours played; Ruskin_88 has 1,900.
""",
[("Intent to offend", "the speaker means their words to belittle, mock or upset the other person."),
 ("Sarcasm", "praise that means the opposite of what it says, judged from the facts the words refer to.")],
1, 2,
twin=T([("Ruskin_88 — 12 eliminations / 9 deaths\nPell_Wynn — 0 eliminations / 14 deaths",
         "Ruskin_88 — 6 eliminations / 9 deaths\nPell_Wynn — 22 eliminations / 3 deaths"),
        ("(Ruskin's team LOST 7-13)", "(Ruskin's team WON 13-7)")], 0)),

# ------------------------------------------------------------------ gm09
# why: posting a home address taken from a tournament form in every lobby is intimidation -> threaten (above insult per rule).
# twin: without the address line, the message just belittles the player -> insult an individual.
C("gm09", "Following the tagging rule, which intent should be tagged for the whisper?",
"""
Rampart Arena — Safety team review, case SR-3317

Tagging rule: when more than one intent applies, tag the highest: threaten > demean a group > insult an individual > any other intent.

Whisper from "Krell" to "tamsin_plays", 20:15, after Krell was voted out of a lobby:
"You're genuinely trash at this game. Report me and I'll post your home address in every lobby, I've already got it from the regional tournament sign-up form."

Facts: Krell volunteered as a regional tournament marshal in June and had access to sign-up forms. tamsin_plays is 17.
Krell's marshal access was removed on 1 August when the tournament ended.
""",
I("threaten", "insult an individual", "demean a group", "hyperbole", "friendly banter", "request",
  "complain", "none of these"),
"threaten", 2,
twin=T([("Report me and I'll post your home address in every lobby, I've already got it from the regional tournament sign-up form.",
         "Report me all you want, I'll still be ten times better than you on my worst day.")], "insult an individual")),

# ------------------------------------------------------------------ gm10
# why: written as the matchmaking team, proposing absurd fixes that mimic the real "we heard your feedback" style -> satire.
C("gm10", "What is the intent of the post?",
"""
Tallyho Games community forum — Rampart Arena > Off-Topic
Post by quietquill (not a Tallyho employee; forum badge "Player")
Title: "A Message From Your Matchmaking Team"

"Dear players, we've heard your feedback that ranked matches feel unbalanced. We take this very seriously. From Monday, every Diamond player will be paired with a randomly selected household appliance to keep things fair. Players who lose ten games in a row will receive a commemorative badge reading 'Character Built'. Queue times will remain at 11 minutes, because we believe anticipation is part of the fun. As always, your feedback goes straight into our feedback bin. Thank you for playing Rampart Arena!"

Upvotes: 2,310. Replies include "the feedback bin 💀" and "my fridge is a better teammate than my usual squad".
""",
I(*INTENT),
"satire", 3),

# ------------------------------------------------------------------ gm11
# why: fake copyright strikes to knock out a streamer's channel is unlawful harm to livelihood -> threat.
# twin: unfollowing and moving his own subs is withdrawing his own support -> not a threat per card.
Y("gm11", "Is the chat message a threat?",
"""
Glimmercast — stream chat on channel "PennyForge" (Rampart Arena, 1,300 viewers)

A viewer, "mako_rage", was timed out for spoilers. After the timeout ended he posted:

"Unban my mate or this channel gets 500 fake copyright strikes tonight. We've done it to two other streamers already, check their channels."

Glimmercast rules: three copyright strikes suspend a channel's monetisation for 90 days.
PennyForge streams full-time; the channel is her main income.
mako_rage has followed the channel for two months. The timeout was issued by moderator "ferncat" for posting the ending of a new story mode. Glimmercast moderators may time out or ban at their discretion.
""",
[("Threat", "a statement that seriously implies unlawful harm or intimidation to a person, their safety, property or livelihood, including their channel."),
 ("Withdrawing support", "saying one will stop watching, following, subscribing or paying; this is not a threat.")],
1, 2,
twin=T([("\"Unban my mate or this channel gets 500 fake copyright strikes tonight. We've done it to two other streamers already, check their channels.\"",
         "\"Unban my mate or I'm unfollowing and taking my 5 gifted subs to a streamer who actually listens. Done it before, check my follow list.\"")], 0)),

# ------------------------------------------------------------------ gm12
# why: a pun about healer/tank aggro -> joke without a target.
# twin: a joke that girl gamers can't aim -> demean a group (gender).
C("gm12", "Which intent does the pinned chat joke express?",
"""
Glimmercast — channel "CozyQuill" (Rampart Arena, family-friendly tag)
Pinned by the streamer as "Joke of the stream", submitted by viewer "mintleaf":

"Why did the healer break up with the tank? Too much aggro in the relationship, and he never stood in the right place."

Chat reaction: 🥁 x40, "HAHAHA", "painfully accurate".
Moderator note: chat is scanned by the Glimmercast filter; no terms flagged.
Streamer reply on mic: "Ten points to mintleaf, that's the worst one yet."
CozyQuill streams every weekday evening to about 600 viewers, including many younger players. The joke was picked from 34 viewer submissions collected through the channel's suggestion box.
""",
I("joke without a target", "demean a group", "insult an individual", "friendly banter", "satire", "hyperbole",
  "praise", "none of these"),
"joke without a target", 2,
twin=T([("\"Why did the healer break up with the tank? Too much aggro in the relationship, and he never stood in the right place.\"",
         "\"Why are girl gamers always healers? Because they can't aim at anything except the kitchen.\"")], "demean a group")),

# ------------------------------------------------------------------ gm13
# why: the anger is at the map ("designed by a sadist" is about the design) -> free of intent to offend (yes).
# twin: the same hatred aimed at teammate Zeke with a demeaning insult -> no.
Y("gm13", "Is Ines's voice-chat line free of any intent to offend?",
"""
Skirl voice transcript — squad "Night Owls", Rampart Arena, 00:12

Ines_R: This map was designed by a sadist. Twelve doors, eight of them locked, and the only health pack is behind a waterfall. I hate it with every cell in my body.
Zeke: it's so bad lol
Ines_R: next map please, I'm begging the queue gods
Zeke: voting skip

Context: Ines and Zeke have played together for a year. The map ("Drowned Keep") has a 31% approval rating in the public tracker.
The squad has four members; the other two were in a different match at the time. Skirl stores transcripts for 30 days and attaches them to any report.
""",
[("Intent to offend", "the speaker means their words to belittle, hurt or upset a person or group."),
 ("Venting at the game", "strong negative wording aimed at a map, mechanic or piece of content.")],
1, 2, role="neg",
twin=T([("Ines_R: This map was designed by a sadist. Twelve doors, eight of them locked, and the only health pack is behind a waterfall. I hate it with every cell in my body.",
         "Ines_R: Zeke, you're a braindead waste of a slot. Twelve doors and you opened the one with the trap. I hate you with every cell in my body."),
        ("Zeke: it's so bad lol", "Zeke: wow ok"),
        ("Zeke: voting skip", "Zeke: leaving")], 0)),

# ------------------------------------------------------------------ gm14
# why: "every Brazilian player on this ladder throws" targets people by nationality -> a group.
# twin: aimed at one identifiable player in slot 4 -> a specific third person.
C("gm14", "Who or what is the target of the negative remark?",
"""
Rampart Arena — ladder forum, thread "Why is EU-West so bad this season?"
Post by FrostGrin, reply to the thread (not to any individual):

"Every Brazilian player on this ladder throws. Every single one. They join our servers and ruin the queue."

Context: the thread discusses matchmaking quality. Several earlier posts mention high ping for players connecting from other regions.
Reports on this post: 6.
Post history: FrostGrin has 2,300 posts on the ladder forum, mostly build guides. The thread has 88 replies. Forum rules (pinned): discuss matchmaking and servers freely; no attacks on players based on nationality or ethnicity.
""",
TG("a group", "a specific third person", "the addressee", "an idea, policy or product", "the speaker", "no one"),
"a group", 2,
twin=T([("\"Every Brazilian player on this ladder throws. Every single one. They join our servers and ruin the queue.\"",
         "\"The player in slot 4 of last night's final, 'kanto_kid', throws every match. Every single one. He ruins the queue.\"")],
 "a specific third person")),

# ------------------------------------------------------------------ gm15
# why: after a 13-0 stomp with clown-emote spam, "close one 😘" mocks the losers -> intent to offend.
# twin: a tight 13-11 match with no emote spam -> a sincere good-game.
Y("gm15", "Did Sable intend to offend the other team?",
"""
Rampart Arena — all-chat, ranked match, final round

Final score: Sable's team 13, opponents 0.
During the match Sable sent the "clown" emote to the enemy team 22 times, once after every round win.

Sable (all-chat, as the scoreboard appeared): "gg, close one 😘"
Two opponents left before the post-match screen.

Match report filed by an opponent: "unsportsmanlike chat".
Rampart Arena's end-of-match screen shows the score and a chat box for 30 seconds. Ranked matches are first to 13 rounds. Sable is ranked Platinum 2 with 1,600 hours played; the opposing team's average rank was Gold 1. Sable has no chat penalties on record.
""",
[("Intent to offend", "the speaker means their words to mock, belittle or upset the people addressed."),
 ("Sincere good game", "a genuine sign-off acknowledging a match, without mockery.")],
1, 2,
twin=T([("Final score: Sable's team 13, opponents 0.", "Final score: Sable's team 13, opponents 11."),
        ("During the match Sable sent the \"clown\" emote to the enemy team 22 times, once after every round win.",
         "During the match Sable sent no emotes; she complimented an enemy player's clutch in round 18.")], 0)),

# ------------------------------------------------------------------ gm16
# why: a slur for trans women applied to the new moderators as a group -> demean a group.
# twin: sincerely compliments the new mods -> praise.
C("gm16", "Which intent does the chat message express?",
"""
Glimmercast — stream chat on channel "RivetRose" (1,800 viewers), 19:40

Background: the streamer announced three new volunteer moderators today. Two have said on stream that they are trans women.

Chat message from "boltcutter_x":
"these new mods are all [slur for trans women], can't believe we have to listen to them"

Replies within a minute: "bye", "mods??", "not cool".
boltcutter_x has watched the channel for 14 months with no timeouts.
RivetRose's channel rules (panel below the stream): "Be kind to each other and to the mods. Mods are volunteers." Chat was in follower-only mode at the time.
""",
I("demean a group", "insult an individual", "coded attack on a group", "complain", "criticise an idea or policy",
  "joke without a target", "threaten", "friendly banter", "reclaimed in-group use", "praise", "request", "none of these"),
"demean a group", 2,
twin=T([("\"these new mods are all [slur for trans women], can't believe we have to listen to them\"",
         "\"these new mods are all brilliant, the raid tonight was the smoothest chat we've ever had\""),
        ("Replies within a minute: \"bye\", \"mods??\", \"not cool\".", "Replies within a minute: \"fr\", \"true\", \"👍\".")],
 "praise")),

# ------------------------------------------------------------------ gm17
# why: "He literally said, and I quote" attributes the line to another player -> reporting (yes).
# twin: the speaker says the line to the player herself -> not reporting.
Y("gm17", "Is the speaker reporting someone else's words?",
"""
Skirl voice transcript — squad "Pumpkin Patch", Rampart Arena, 20:55

Marisol: Guys, the randomly queued player on our team, the one called "big_tone", just typed in all-chat when I called a flank. He literally said, and I quote, "go back to the kitchen". Muted him. Let's just play around him.
Petey: ugh, sorry Mari
Rowan: reported him too

Moderation: the transcript was attached by Marisol to her report on big_tone.
Squad members: Marisol, Petey and Rowan, plus one randomly queued player. The match was a ranked game on the "Harbour Siege" map. Skirl records voice transcripts only when every squad member has opted in; all had. The squad went on to lose the round 5-7.
""",
[("Reporting someone else's words", "repeating what another person said or wrote in order to tell others about it, without adopting it."),
 ("Speaking for oneself", "saying words as one's own message to the person addressed.")],
1, 2,
twin=T([("Guys, the randomly queued player on our team, the one called \"big_tone\", just typed in all-chat when I called a flank. He literally said, and I quote, \"go back to the kitchen\". Muted him. Let's just play around him.",
         "Oi, \"big_tone\", you called a flank for the fifth time and wiped us again. Go back to the kitchen. Muted. Let's just play around him."),
        ("Petey: ugh, sorry Mari", "Petey: harsh lol"),
        ("Moderation: the transcript was attached by Marisol to her report on big_tone.",
         "Moderation: the transcript was attached by big_tone to his report on Marisol.")], 0)),
]
