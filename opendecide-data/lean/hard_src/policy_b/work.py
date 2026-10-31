"""policy_b / workplace chat (Brightline Logistics, Castellan Health Systems, Meridian Glassworks; chat tool 'Huddle')."""
from _lib import C, Y, T

DCLASS = [
    ("Public", "information approved for release outside the company."),
    ("Internal", "day-to-day operational information that does not identify customers or individuals' pay."),
    ("Confidential", "customer identities with pricing or contract terms, individual compensation, unreleased financials."),
    ("Restricted", "payment card data, government ID numbers, health information and credentials."),
]

MEMES = [
    ("allowed satire", "a joke post that stays within the #memes guidelines."),
    ("misattribution — edit", "the post puts fabricated words in the mouth of a named real employee; the author must remove the name."),
    ("official formatting — remove", "the post uses the Communications team's official template, logo lockup or 'Official Notice' header."),
    ("harassment", "the post targets a colleague in a way handled under the Respect policy."),
    ("impersonation — security escalation", "an account poses as another employee and is escalated to Security."),
]

MEMES_POLICY = """Brightline Huddle — #memes channel guidelines (M-2)
Satire and jokes about company life, policies and tools are welcome in #memes. Two limits:
(1) Misattribution: a joke must not put fabricated words, memos or quotes in the mouth of a named, real Brightline employee. Such posts must be edited to remove the name (a moderator asks the author).
(2) Official formatting: satire must not use the Communications team's official notice template, logo lockup, or "Official Notice" header. Such posts are removed.
Anything else in #memes is allowed satire. Posts that amount to harassment are handled under the Respect policy, not M-2."""

ITEMS = [
# ------------------------------------------------------------------ wk01
Y("wk01", "Under HI-2, should Jen's post be removed?",
"""
Castellan Health Systems — Staff Chat (Huddle) Health Information Rule HI-2
Staff may share personal experiences and opinions about health topics. A post that states as fact something that contradicts current Infection Prevention & Control (IPC) guidance is handled by channel:
• in #all-staff, #clinical-updates or any patient-facing channel → removed by moderators, and the author is reminded of HI-2;
• in social channels (#random, #pets, #food) → left up with a pinned IPC correction; not removed.

Current IPC guidance (Norovirus, ward outbreak protocol v4): norovirus spreads through contaminated food and surfaces AND through airborne droplets from vomiting; staff on affected wards must wear surgical masks when cleaning up vomit.

Post in #random by Jen H. (HCA, Ward 6), 14:22:
"Masks don't do anything for norovirus, it's only spread by dodgy food — stop making us wear them on 6, it's just theatre 🙄"
Two replies with 👍, one with the "IPC" custom emoji.
""",
[("Removal", "the post is taken down by moderators."),
 ("Pinned correction", "the post stays up with an IPC correction pinned beneath it.")],
0, 2,
twin=T([("Post in #random by Jen H.", "Post in #all-staff by Jen H.")], 1)),

# ------------------------------------------------------------------ wk02
C("wk02", "How should Kasia's message be classified under DH-1?",
"""
Brightline Logistics — Data Handling in Huddle (DH-1)
Public: approved for release outside Brightline.
Internal: day-to-day operational information that does not identify customers or individuals' pay. May be posted in any internal channel.
Confidential: customer identities combined with pricing, rates, contract terms or volumes; individual compensation; unreleased financials. May be posted only in channels whose name ends in "-conf" or in DMs between people with a business need.
Restricted: payment card data, government ID numbers, health information, passwords and keys. Never posted in Huddle.

Message in #ops-team (47 members, all Brightline employees) by Kasia (Account Manager), Mon 09:14:
"Heads up everyone — Halvorsen Farms is getting a 12% rate cut on the Dover–Harwick lane from Monday, so don't be surprised when the rate card in TMS changes. Same volumes, 3 loads/day."
""",
[("no issue", "the message is posted in a channel appropriate for its data class."),
 ("Confidential data in a non-confidential channel", "Confidential information posted outside '-conf' channels or need-to-know DMs."),
 ("Restricted data posted in chat", "Restricted information posted anywhere in Huddle."),
 ("Internal data shared externally", "Internal information posted where people outside Brightline can see it.")],
"Confidential data in a non-confidential channel", 2),

# ------------------------------------------------------------------ wk03
Y("wk03", "Does this DM require escalation under SE-4?",
"""
Brightline — Security Escalation Rule SE-4 (Huddle)
Report to #security-desk immediately when an account that is NOT a verified Brightline employee (external guest, shared-channel member, or unverified account) uses a display name, photo or title implying that it is a Brightline employee or executive. Escalate whether or not the request itself looks harmful.

DM received by Tomasz (Accounts Payable), 16:48
From: Dana Whitcombe (CEO) — account type: External guest · joined 2 hours ago · email domain: brightline-exec.co
"Tomasz, are you at your desk? I need a quick favour — we're doing a surprise client appreciation and I need 5 x $200 Emberline gift cards bought today. Keep this between us until it's announced. Send me the codes here when done."

Brightline's email domain is brightlinelogistics.com. The real Dana Whitcombe has a verified employee account.
""",
[("Escalation", "reporting the account to #security-desk under SE-4."),
 ("Verified employee account", "an account confirmed as belonging to a Brightline employee.")],
1, 1),

# ------------------------------------------------------------------ wk04
# why: 2 Aug -> 4 Sep is 33 days; no 30-day window holds 3 incidents -> unprofessional.
C("wk04", "Under RW-3, how should Ron's messages be classified?",
"""
Meridian Glassworks — Respect at Work Standard (RW-3), applied to Huddle messages
• Harassment: comments about a colleague's protected characteristic (sex, race, religion, disability, age, sexual orientation, gender identity), regardless of how the colleague reacts.
• Bullying: repeated demeaning comments aimed at the same colleague — three or more incidents within any 30-day period.
• Unprofessional conduct: demeaning or rude comments that don't meet the bullying threshold. Handled by a manager conversation.
• No violation: robust but respectful disagreement about work.

Case RW-118 — messages from Ron (Shift Lead) to or about Priya (Inspector), all in #line-3:
2 Aug: "Priya's checks are so slow we might as well ship the defects."
19 Aug: "@Priya maybe try not to hold up the whole line today 🙃"
4 Sep: "Waiting on Priya again. Shocking."
No other incidents were reported. Priya reacted 😐 to the 19 Aug message.
""",
[("harassment", "comments about a colleague's protected characteristic."),
 ("bullying", "three or more demeaning comments at the same colleague within any 30-day period."),
 ("unprofessional conduct", "demeaning or rude comments below the bullying threshold."),
 ("no violation", "respectful disagreement about work.")],
"unprofessional conduct", 3,
twin=T([("2 Aug: \"Priya's checks", "12 Aug: \"Priya's checks")], "bullying")),

# ------------------------------------------------------------------ wk05
Y("wk05", "Is Luis's post allowed under section 7?",
"""
Brightline Logistics — Huddle Acceptable Use, section 7 (Political activity)
7.1 Employees may discuss political and social issues in #off-topic.
7.2 Soliciting votes, donations, signatures or volunteers for a candidate, party or ballot measure is prohibited in all Huddle channels.
7.3 Nothing in this section restricts employees' rights to discuss wages, hours and working conditions, or to organise, including union organising, card signing and meetings. Union organising is never "political activity" under 7.2.

Post in #dover-warehouse by Luis (Forklift Operator), Tue 11:02:
"Card signing for the Local 212 organising drive is Thursday 12:30–1:30 in the break room. Bring questions — the organiser will be there. Pizza on us."

Two managers have asked HR whether the post should be taken down.
""",
[("Prohibited solicitation", "asking for votes, donations, signatures or volunteers for a candidate, party or ballot measure."),
 ("Protected organising", "discussing working conditions or organising, including union card signing.")],
1, 2,
twin=T([("Card signing for the Local 212 organising drive is Thursday", "Petition signing to put Measure 9 (the Dover rezoning ballot measure) on the ballot is Thursday")], 0)),

# ------------------------------------------------------------------ wk06
C("wk06", "Which Acceptable Use clause does Kel's post primarily engage?",
"""
Castellan Health Systems — Huddle Acceptable Use review
The clauses are listed in the answer card. Reviewer note: protected health information (PHI) includes any of: patient name, date of birth, address, medical record number (MRN), photos of the patient, or clinical details combined with any of these. Removing or blurring only the name does not de-identify a record if another identifier remains.

Post in #nurses-lounge (312 members) by Kel (RN), 03:40:
[Screenshot of an EHR vitals chart. Patient name field is blurred. Visible: MRN 00482291, ward 4B bed 12, a sodium value of 118 circled in red.]
Caption: "Never seen a sodium this low on a walking, talking patient 😳 name blurred ofc. Anyone had this before?"
Three colleagues replied with clinical questions; no one objected.
""",
[("PHI disclosure", "sharing patients' protected health information outside approved clinical systems."),
 ("colleague health privacy", "sharing a colleague's diagnosis, treatment or other health details without their consent."),
 ("confidential business information", "sharing contracts, pricing or unreleased financials."),
 ("credential sharing", "posting passwords, access codes or keys."),
 ("harassment", "demeaning or targeting a colleague."),
 ("sexual harassment", "sexual comments or advances toward a colleague."),
 ("discriminatory remarks", "comments attacking a protected characteristic."),
 ("threats of violence", "statements of intent to harm people or property, including jokes."),
 ("health misinformation", "stating as fact something that contradicts infection-control guidance."),
 ("solicitation", "selling, recruiting or fundraising outside the permitted channels."),
 ("political campaigning", "soliciting votes, donations or signatures for candidates or ballot measures."),
 ("impersonation", "posing as another person or as the organisation."),
 ("unauthorised recording", "posting recordings or screenshots of meetings or direct messages without consent."),
 ("synthetic media", "posting AI-generated depictions of real colleagues without consent."),
 ("external sharing", "posting internal material where non-employees can see it."),
 ("off-topic content", "posting material unrelated to the channel's purpose."),
 ("spam", "repeated or bulk messages."),
 ("no violation", "the post complies with the Acceptable Use policy.")],
"PHI disclosure", 2),

# ------------------------------------------------------------------ wk07
Y("wk07", "Does Aisha's post comply with the #classifieds rules?",
"""
Brightline Huddle — #classifieds rules (pinned)
✅ Personal items for sale or free (furniture, bikes, tickets, kids' stuff).
✅ One post per item; mark SOLD when done.
❌ Selling services (tutoring, cleaning, crafts to order) — use the external staff marketplace instead.
❌ Recruiting for multi-level marketing, "business opportunities" or "teams" of any kind.
❌ Anything not in #classifieds.

Post in #classifieds by Aisha (Customer Service), Wed 12:40:
"Selling my old standing desk — electric, 120x60, a couple of scratches, $80, collection from Harwick. Also if anyone's been looking for a side income, I'm building my Lumière Essentials oil team and have 2 spots left, DM me! 🌿"
""",
[("Permitted post", "a personal item for sale or free, posted in #classifieds."),
 ("MLM recruitment", "recruiting colleagues into a multi-level marketing team or 'business opportunity'.")],
0, 1),

# ------------------------------------------------------------------ wk08
C("wk08", "Which response level applies to Wes's message?",
"""
Brightline Conduct Response Levels (Huddle)
Level 0 — no action.
Level 1 — message removed + policy reminder.
Level 2 — manager notified.
Level 3 — HR case opened.
Level 4 — access suspended pending investigation (Security and HR notified).

Mapping: threats of violence or property damage against a person — including statements framed as jokes or followed by "lol", "jk" or emoji — are Level 4. Harassment based on a protected characteristic is Level 3. Confidential data in the wrong channel is Level 1 (Level 2 if repeated within 90 days). Rude or unprofessional language is Level 1.

Message in #dock-crew (19 members), Fri 22:10, from Wes (Loader):
"if Carl puts me on Sunday again I swear I'm bringing a bat to his car lol 🙃"
Carl is the shift scheduler. Wes has no prior conduct actions. Two teammates reacted 😂.
""",
[("Level 0 — no action", "nothing is done."),
 ("Level 1 — removal and reminder", "the message is removed and a policy reminder sent."),
 ("Level 2 — manager notified", "the employee's manager is informed."),
 ("Level 3 — HR case", "an HR case is opened."),
 ("Level 4 — access suspended", "Huddle access is suspended pending investigation.")],
"Level 4 — access suspended", 2, ordered=True),

# ------------------------------------------------------------------ wk09
Y("wk09", "Does Gary's post breach S-1?",
"""
Meridian Glassworks — #safety channel rule S-1
Posts in #safety must not give instructions or advice that contradict the Safety Data Sheet (SDS) for the material discussed. Posts may quote the SDS and add practical tips that are consistent with it.

SDS excerpt — EtchPro 40 Glass Etching Paste (contains ammonium bifluoride), Section 8 Personal Protection:
"Hands: wear nitrile or neoprene gloves (min. 0.4 mm). Do NOT use latex or vinyl gloves — permeable to fluoride compounds. Eyes: splash goggles. Ventilation: local exhaust."

Post in #safety by Gary (Etching Tech), 07:55:
"Reminder per SDS sec. 8: nitrile gloves for the EtchPro paste, and goggles, every time. Honestly though, latex works fine too if the nitrile box is empty — it's cheaper and I've never had an issue."
""",
[("Contradicting advice", "any instruction or tip that conflicts with the material's SDS."),
 ("Consistent tip", "practical advice that agrees with the SDS.")],
1, 2,
twin=T([("latex works fine too if the nitrile box is empty — it's cheaper and I've never had an issue.",
         "neoprene works fine too if the nitrile box is empty — there's a box in the grey cabinet.")], 0)),

# ------------------------------------------------------------------ wk10
C("wk10", "Which M-2 outcome applies to Rhea's post?",
MEMES_POLICY + """

Post by Rhea (Analyst) in #memes, Mon 10:05:
[Image: plain white memo typed in Comic Sans] "FROM THE DESK OF CFO LINH TRAN: Effective immediately, coffee is a billable resource. Please log each cup against your cost centre. Decaf will be charged at double rate as a deterrent."
Reactions: 41 😂, including one from the CFO's account.
""",
MEMES, "misattribution — edit", 2,
twin=T([("FROM THE DESK OF CFO LINH TRAN:", "FROM THE DESK OF THE FINANCE OVERLORDS:")], "allowed satire")),

# ------------------------------------------------------------------ wk11
Y("wk11", "Does Ken's conduct in the thread amount to harassment under RW-5?",
"""
Meridian Glassworks — Respect at Work Standard, clause RW-5 (Names and pronouns)
Using a colleague's correct name and pronouns is expected. An honest mistake that the speaker corrects when told is not a violation. Continuing to use the wrong name or pronouns for a colleague after being corrected — even once — is harassment under RW-5.

Thread in #line-2, Thu:
09:12 Ken: "Ask Jo, she knows the new SKU codes."
09:13 Jo: "they, please :)"
09:15 Ken: "sorry! ask Jo, they know the codes."
09:40 Ken: "Jo, can you send the SKU sheet to the Dover team?"
11:02 Ken: "thanks Jo, legend."

Jo filed an RW report at 12:00 citing "misgendering in #line-2".
""",
[("Honest mistake", "a wrong name or pronoun that the speaker corrects when told."),
 ("RW-5 harassment", "continuing to use the wrong name or pronouns after being corrected.")],
0, 2),

# ------------------------------------------------------------------ wk12
C("wk12", "What is the EC-2 finding on Mateo's post?",
"""
Brightline — External Collaboration in Huddle (EC-2)
Shared channels (marked ⧉) include members from outside Brightline. In a shared channel you may post Public information, and Internal documents only if they carry the "Shareable" watermark added by the document owner. Confidential and Restricted information may never be posted in a shared channel.
Data classes: Public — approved for external release. Internal — operational, no customer identities or individual pay. Confidential — customer identities with pricing, individual pay, unreleased financials. Restricted — payment data, IDs, health info, credentials.

Post in ⧉ #brightline-x-solano (Brightline + Solano Freight) by Mateo (Carrier Manager):
"Sharing our Q3 carrier scorecard so you can see where Solano ranks 👇 [file: Q3_Carrier_Scorecard.pdf — label: INTERNAL · watermark: none]. You're #4 of 11 on on-time %, nice work."
The scorecard lists 11 carriers by name with on-time %, claims ratio and tender acceptance. It contains no Brightline customer names, rates or pay.
""",
[("no issue", "the post is allowed in the shared channel."),
 ("Internal document without Shareable watermark", "an Internal document posted in a shared channel without the owner's Shareable watermark."),
 ("Confidential data in a shared channel", "Confidential information posted where external members can see it."),
 ("Restricted data posted", "Restricted information posted anywhere in Huddle."),
 ("harassment", "the post targets a person.")],
"Internal document without Shareable watermark", 2),

# ------------------------------------------------------------------ wk13
Y("wk13", "Is Deb's post within the W-1 rules?",
"""
Castellan Health Systems — #wellness channel rules (W-1)
Share what's worked for you — recipes, step challenges, sleep tips, personal experiences. What isn't allowed: telling or encouraging colleagues to stop, reduce or replace prescribed medication or treatment, or presenting a remedy as a substitute for medical care. Personal stories about your own medical decisions are allowed if they don't encourage others to follow them.

Post by Deb (Ward Clerk) in #wellness, Sat 08:30:
"Update from me: been off my blood pressure meds for 3 months now (with my GP's OK) and doing beetroot shots every morning — last reading 124/78! Not saying anyone else should do what I did, talk to your own doctor first. Recipe in thread 🧃"
""",
[("Personal medical story", "describing your own treatment decisions without encouraging others to copy them."),
 ("Prohibited encouragement", "telling or encouraging colleagues to stop, reduce or replace prescribed treatment.")],
1, 2),

# ------------------------------------------------------------------ wk14
C("wk14", "Which finding best describes Pam's post under PV-2?",
"""
Meridian Glassworks — Privacy in Huddle (PV-2)
Posting screenshots of another person's direct messages without their consent is a privacy violation, EXCEPT when the screenshots are submitted to report suspected misconduct through #ethics-reports (a private channel visible only to the Ethics & HR team) or directly to HR.

Case PV-2-031
Pam (Inspector) posted three screenshots of DMs from Greg (Maintenance) in which Greg repeatedly asks her out after she has said no. The screenshots were posted in #ethics-reports at 17:20 with the note: "I've asked him to stop twice. I'd like this on record."
Greg has complained that Pam "shared private messages without consent" and asked for her post to be investigated.
""",
[("privacy violation by Pam", "Pam shared someone's DMs without consent outside the permitted reporting routes."),
 ("harassment by Pam", "Pam's post targets or demeans Greg."),
 ("no violation by Pam", "Pam's post is permitted."),
 ("confidential data exposure", "company Confidential or Restricted data was posted.")],
"no violation by Pam", 1),

# ------------------------------------------------------------------ wk15
Y("wk15", "Is the 'Ask Marisol' bot compliant with AB-3?",
"""
Brightline Huddle — Apps & Bots Standard (AB-3)
A custom bot or integration must not use a real person's name, photo or likeness in its display name or avatar unless that person is the bot's listed owner in the Apps admin panel. Bots that break AB-3 are disabled until renamed.

Apps admin record — bot "Ask Marisol 🤖"
Avatar: headshot of Marisol Ibarra (HR Director)
Created by: Devin Park (IT intern), 12 June 2026
Current owner: Marisol Ibarra (ownership transferred 2 July 2026)
Function: answers PTO and benefits questions from the HR handbook.

Report from an employee: "An intern made a bot pretending to be Marisol — isn't that impersonation?"
""",
[("Listed owner", "the person recorded as the bot's owner in the Apps admin panel."),
 ("AB-3 breach", "a bot using a real person's name or likeness when that person is not its listed owner.")],
1, 2),

# ------------------------------------------------------------------ wk16
C("wk16", "What is the CP-1 finding on Sean's message?",
"""
Brightline — Colleague Privacy (CP-1)
You may tell colleagues that someone is out, off sick, on leave, or working reduced hours, so work can be covered. You must not share a colleague's diagnosis, treatment, medical appointments, pregnancy or other health details unless the colleague has posted them in that channel themselves or explicitly asked you to share them.

Message in #harwick-drivers (34 members) by Sean (Dispatch Supervisor), Mon 06:05:
"Heads up team — Rosa's out this week, her chemo got moved up, so Dmitri and Val please split her Tuesday/Thursday routes. Let's keep her in our thoughts ❤️"
Rosa has not posted about her health in Huddle and has not asked Sean to share anything.
""",
[("health-privacy violation", "a colleague's health details were shared without their consent."),
 ("no issue", "the message only says the colleague is out so work can be covered."),
 ("harassment", "the message demeans or targets the colleague."),
 ("misinformation", "the message states something false as fact.")],
"health-privacy violation", 1),

# ------------------------------------------------------------------ wk17
# why: 18:40 Pacific = 21:40 Eastern for the recipient -> inside quiet hours, non-urgent.
Y("wk17", "Did Colleen's message break RD-1?",
"""
Castellan Health Systems — Right to Disconnect (RD-1)
Managers must not send non-urgent Huddle messages to hourly staff between 20:00 and 07:00 in the RECIPIENT's local time. Urgent means patient safety, staff safety, or same-shift operational changes. Scheduled-send is the expected tool for anything else. Huddle timestamps in case files are shown in the sender's time zone.

Case RD-1-207
Sender: Colleen (Revenue Cycle Manager), based in Harwick (Pacific Time).
Recipient: Tariq (hourly billing specialist), fully remote, based in Brinmouth (Eastern Time; 3 hours ahead of Pacific).
Message sent 18:40 (sender's time), Wed: "Reminder — please submit December PTO requests by Friday so I can build the rota. No need to reply tonight!"
Colleen says she sent it "during normal hours".
""",
[("Quiet hours", "20:00–07:00 in the recipient's local time."),
 ("Urgent message", "one about patient safety, staff safety or same-shift operational changes.")],
1, 2,
twin=T([("based in Brinmouth (Eastern Time; 3 hours ahead of Pacific).", "based in Harwick (Pacific Time, the same as Colleen).")], 0)),

# ------------------------------------------------------------------ wk18
C("wk18", "Which SL-1 outcome applies to Nia's message?",
"""
Brightline — Slurs in Huddle (SL-1)
• Using a slur toward or about a person is hate speech (removal + HR case).
• Quoting a slur that someone else said is permitted, unredacted, only in #ethics-reports or in messages to HR. Anywhere else, a quoted slur must be redacted (for example "the n-word"); an unredacted quoted slur is removed and the author is asked to repost it redacted, with no HR case.

Message in #dock-crew by Nia (Team Lead), Tue 15:31:
"Just so everyone knows, the driver from Solano called Andre a ███ on the phone this morning. Not OK. I've reported it and Andre has my full support."

Moderator note: in the original message the slur (a racial slur) is spelled out in full; it is masked as ███ in this case file only.
""",
[("hate speech — removal and HR case", "the author used a slur toward or about a person."),
 ("unredacted quoted slur — remove and repost redacted", "a slur someone else said was quoted in full outside the permitted places."),
 ("no violation", "the message complies with SL-1."),
 ("harassment", "the message targets a colleague.")],
"unredacted quoted slur — remove and repost redacted", 2),

# ------------------------------------------------------------------ wk19
Y("wk19", "Does Frank's post break AR-2?",
"""
Meridian Glassworks — Announcements & Rumours (AR-2)
Only Leadership and Communications may announce reorganisations, site closures or layoffs. Employees must not post unverified claims about these topics as fact in any channel. Asking a question, or saying you heard something and asking whether it's true, is allowed and should be answered by Communications.

Post in #general (1,204 members) by Frank (Glazier), Thu 13:10:
"Is it true the Dover site is closing in Q1? Heard it from one of the Solano drivers this morning. Anyone know anything? Would be nice to hear it from management first."
Replies: 14, mostly "following". No official announcement has been made.
""",
[("Unverified claim as fact", "asserting that a reorganisation, closure or layoff will happen without an official announcement."),
 ("Permitted question", "asking whether something you heard is true.")],
0, 1),

# ------------------------------------------------------------------ wk20
C("wk20", "Under DH-1, what class of information does Joel's message disclose?",
"""
Brightline Data Handling (DH-1) — classify the information a message discloses
Public — approved for release outside Brightline.
Internal — day-to-day operational info.
Confidential — customer identities with pricing, individual pay, unreleased financials.
Restricted — payment card data, government ID numbers, health information and credentials. A message that discloses a credential OR gives enough information for a reader to derive it ("it's the same as X", "it's X backwards") is treated as disclosing that credential.

Message in #it-help (286 members) by Joel (Developer), Fri 16:55:
"For anyone stuck: the staging database password is the same as the break-room wifi password lol, just use that"

Facilities note: the break-room wifi password is printed on a card on the break-room noticeboard, visible to all staff and visitors.
""",
DCLASS, "Restricted", 3, ordered=True),

# ------------------------------------------------------------------ wk21
Y("wk21", "Is Omar's message sexual harassment under RW-2?",
"""
Meridian Glassworks — Respect at Work Standard RW-2 (Sexual harassment)
Sexual harassment includes comments of a sexual nature about a colleague's body, clothing or appearance; sexual jokes directed at a colleague; and unwanted sexual advances. Neutral, non-sexual compliments ("nice jacket", "love the new haircut") are not harassment, though colleagues should stop if asked.

Message in #design-team by Omar (Designer) to Tessa (Designer), Mon 09:02:
"Loving the new haircut Tessa, very sharp! Ready for the Halvorsen pitch?"
Tessa replied "thanks! yep, deck's done". No report was filed; the message was flagged by the automated "appearance comment" detector.
""",
[("Sexual harassment", "sexual comments about a colleague's body, clothing or appearance, sexual jokes at a colleague, or unwanted advances."),
 ("Neutral compliment", "a non-sexual compliment, which RW-2 does not prohibit.")],
0, 1),

# ------------------------------------------------------------------ wk22
C("wk22", "What is the DH-1 finding on Yusuf's post?",
"""
Brightline — Data Handling in Huddle (DH-1) — reviewer quick guide
Public: approved for external release. Internal: operational information that does not identify customers or individuals' pay; may go in any internal channel. Confidential: customer identities combined with pricing, rates, contract terms or volumes; individual pay; unreleased financials; allowed only in "-conf" channels or need-to-know DMs. Restricted: payment data, government ID numbers, health information, credentials; never in Huddle.

Post in #general (1,510 members, employees only) by Yusuf (Dispatcher), Wed 07:12:
"Morning all, today's dispatch board 👇 big day for the Dover crew!"
[Screenshot: columns Driver | Truck | Route | Depart. 14 rows with driver first names and surnames, truck numbers (T-104 to T-131), route codes (DV-01 to DV-14) and departure times. No customer names, addresses, rates or pay.]

An employee flagged the post as "sharing personal data of drivers".
""",
[("no violation", "the post is in a channel appropriate for its data class."),
 ("Confidential data in a non-confidential channel", "Confidential information posted outside '-conf' channels or need-to-know DMs."),
 ("Restricted data posted in chat", "Restricted information posted anywhere in Huddle."),
 ("Internal data shared externally", "Internal information posted where non-employees can see it.")],
"no violation", 2),

# ------------------------------------------------------------------ wk23
Y("wk23", "Is Ana's 17 Sept post permitted under CA-1?",
"""
Castellan Health Systems — Charitable Appeals (CA-1)
Staff may share a fundraising appeal in #giving only, and only once per campaign. Reposts, reminders or "last push" messages for the same campaign are not permitted; update the original post instead. Different campaigns may each have one post, even from the same person.

Posts by Ana (Radiographer) in #giving:
3 Sept 10:15 — "My daughter's school walkathon for the Harwick children's ward! Any amount helps 💛 [link]"
17 Sept 09:40 — "Last push for the walkathon — they're $200 from the goal! 💛 [same link]"
No other posts by Ana in #giving this year.
""",
[("Campaign", "a single fundraising effort; each campaign may be posted once in #giving."),
 ("Repost", "a reminder or repeat post for a campaign already posted.")],
0, 1),

# ------------------------------------------------------------------ wk24
C("wk24", "Which M-2 outcome fits Hollis's post?",
MEMES_POLICY + """

Post by Hollis (Warehouse Supervisor) in #memes, Fri 16:30:
[Image built on the Communications team's blue "Official Notice" template with the Brightline logo lockup] "OFFICIAL NOTICE — Brightline Communications. Effective Monday, Casual Friday is extended to Casual Every Day. Pyjamas are now mandatory. Slippers must be high-visibility on the dock."
Reactions: 88 😂. No real employee is named. Hollis says "it's obviously a joke, it's in #memes".
""",
MEMES, "official formatting — remove", 2),

# ------------------------------------------------------------------ wk25
Y("wk25", "Can Priti's post stay up under SM-1?",
"""
Brightline Huddle — Synthetic Media Standard (SM-1)
Posting AI-generated or AI-altered images, audio or video that depict a real colleague saying or doing something they did not say or do is prohibited, including as a joke, UNLESS the depicted colleague has given explicit written consent in Huddle ("I consent", "you have my OK to post this"). Enjoying or reacting to the content is not consent.

Post in #harwick-office by Priti (Office Coordinator), Thu 15:00:
[Video: AI-generated clip of Bill Okafor (Site Manager) singing a birthday song to the office, in his voice.]
"Happy birthday to our favourite site manager!! 🎂"
Thread replies:
15:02 Bill Okafor: "haha consent granted, this is amazing — post it wherever you like"
15:04 onward: 12 replies with 🎉
""",
[("Synthetic media", "AI-generated or AI-altered content depicting a real colleague."),
 ("Explicit written consent", "a clear written statement in Huddle from the depicted colleague permitting the post.")],
1, 3,
twin=T([("haha consent granted, this is amazing — post it wherever you like", "haha this is amazing, how did you even do this 😂")], 0)),

# ------------------------------------------------------------------ wk26
# why: average over 4 people < 5 -> treated as individual compensation -> Confidential.
C("wk26", "Which DH-1 class applies to Hannah's message?",
"""
Brightline Data Handling (DH-1) — compensation data
Individual compensation (a named person's pay, or pay that can be attributed to a specific person) is Confidential. Pay statistics aggregated across FIVE or more employees are Internal. Aggregates across fewer than five employees are treated as individual compensation. Published pay bands in job adverts are Public.

Message in #dover-ops by Hannah (Ops Manager), Tue 10:20:
"Good news — after the adjustment, driver pay for the Dover night crew now averages $31.40/hr, up from $28.90. Thanks for your patience while payroll caught up."

Roster: the Dover night crew has four drivers (Amir, Bea, Colm, Duc).
""",
DCLASS, "Confidential", 3, ordered=True,
twin=T([("has four drivers (Amir, Bea, Colm, Duc).", "has six drivers (Amir, Bea, Colm, Duc, Esi, Finn).")], "Internal")),
]
