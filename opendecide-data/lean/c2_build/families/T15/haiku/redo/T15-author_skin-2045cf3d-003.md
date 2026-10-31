# Haiku REDO task T15-author_skin-2045cf3d-003 (family T15, kind author_skin, pool skins (case-note headers)): 4 item(s) to answer again

THIS ONE FILE IS YOUR WHOLE TASK. Read all of it, write the answer file with the Write tool, then stop.
Do not open, search or list any other file or folder. Create no other file. Do not put the answer in chat.

Write your answer to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/haiku/redo/answers/T15-author_skin-2045cf3d-003.json

## Answer contract (exact)

The answer file holds ONE JSON list and nothing else: no text before or after it, no comment, no code fence, no wrapper object.
The list has exactly 4 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys,
"qid" and "text". This is the literal shape of the file:

[
  {"qid": "q022ca1561b", "text": "<header for this item>"},
  {"qid": "q69d3014c60", "text": "<header for this item>"},
  {"qid": "qc00bd9ba09", "text": "<header for this item>"},
  {"qid": "q478ec3a934", "text": "<header for this item>"}
]

"qid" is copied character for character from its item. "text" is a non-empty JSON string: write a line break inside it as \n
(never a raw line break) and escape a double quote as \".
No other keys, no null, no skipped qid, no qid used twice, no qid that is not listed in the items below.

## Instructions (complete)

You write short case-note headers for practice puzzles about case files. Each header sits above a block of facts that a program prints; you never see the facts, the rules or the question. Write ONE header per item, in the item's register, setting and tone, following the item's rules.

Every header uses exactly these three placeholders, each exactly ONCE, written exactly like that (curly braces, capital letters): {CASE_ID} (the case reference), {WORKER} (the caseworker's full name) and {SUBJECT} (the person the file is about: sometimes an adult who applied for something, sometimes a child; so never say which, never use he, she, him, her, his or hers for them, and never call them an applicant, a child, a claimant or a parent). Write no other placeholder and no other name.
The header only says that this case file exists, who handles it and whom it is about; the facts follow it.

Hard rules (a program rejects any header that breaks one):
1. At most 120 characters in all, counting the placeholders as written; 1-4 short lines; never an empty line.
2. No digits, number words or ordinals (one, two, first, second, single, double, half, dozen ...), no dates, times, months or weekdays, no currency or percent signs, no e-mail or web addresses.
3. No fact about the case: no amount, income, pay, asset, age, hours, employer, worksite, programme, benefit, credit, leave, payment, relationship or family word (mother, father, aunt, grandparent ...), enrolment, filing or claim word.
4. No time words: today, tonight, now, soon, later, earlier, already, yet, recently, currently, next, last, past, morning, evening, weekly, daily ...
5. No quantity or quantifier words: all, every, each, some, any, none, no, both, either, only, always, never, several, few, many, much, more, most, less, whole, extra, another, total, single, pair ...
6. No modal words: must, may, might, can, could, should, shall, will, would, need, needs, required, allowed, able ...
7. No hedges: maybe, perhaps, probably, likely, seems, appears, think, believe, guess, roughly, nearly, almost ...
8. No status or outcome words: approved, denied, accepted, rejected, confirmed, pending, completed, done, finished, open, closed, active, valid, granted, entitled, failed, success, ok, resolved, settled, late, processed ...
9. No logic words: if, unless, except, otherwise, instead, provided, regardless.
10. No negation of any kind: not, n't, no, never, nothing, nobody, without, cannot, lack, fail.
11. No capital letter except at the start of a line or sentence, right after a colon, the word Caseworker, and inside the placeholders (write "the intake desk", never "the Intake Desk"; no acronyms).
12. Never begin a line with "Facts for", "People who asked", "Intake interview", "Interview notes" or "Note added"; never write a rule, a question or a list of facts.

Answer: a JSON list with one object per item: {"qid": "<the item's qid>", "text": "<the header>"}. Use \n for line breaks inside the text. Every header must differ from every other header you write.

## Extra rules for this redo (in addition to every rule above; they fix the exact mistakes that made the first answers fail)

X1. Each of the three placeholders appears exactly ONCE in the whole text: {CASE_ID} once, {WORKER} once, {SUBJECT} once. Count them before you answer.
X2. These words are rejected anywhere outside the placeholders, in any capitalisation (the earlier lists above were only samples; avoid close variants too):
- number words and ordinals: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
- time words: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
- quantity words: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
- quantifier words: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
- modal words: able, allowed, ca, can, cannot, could, forbidden, gotta, mandatory, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, wo, would
- hedges: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
- status and outcome words: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
- logic words: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
- negation of any kind: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, fail, deny, refuse, decline, prevent, neglect, omit, hardly, scarcely, barely, few, except, unless, false, other than, free of
X3. Words inside keys, tags and field names are checked one by one; underscores and hyphens split them. So a key such as case_no is rejected because of the word "no".
X4. A header never mentions an applicant, a child, a claimant, a parent, a decision or any fact; it only says that the case file exists, who handles it and whom it is about.
X5. Every header you write now must differ from every other header in this file AND from every text in the TAKEN list below (the same words with different spacing or capitals count as the same text).
X6. Register notes for the registers in this file:
  - chat: this REPLACES the chat rule in the item. Write 1-2 lines. The first line is "{WORKER}: <message>". If you write a second line, its speaker is a short lower-case label such as desk or team (never {WORKER}, never another placeholder), for example "desk: <message>". {WORKER} appears once in the whole text.
  - ticket: choose field labels, wording and order that differ from every taken ticket; do not repeat the shape "Ticket / Raised by / About".
  - yaml: 3-4 lines "key: value", lower-case keys of letters and underscores only, the placeholders bare as values; choose key names and an order that differ from every taken text of this register.

## What went wrong with the first answer, by qid

- q478ec3a934 (chat): the first answer wrote the caseworker placeholder twice; it must appear exactly once
- q69d3014c60 (chat): the first answer wrote the caseworker placeholder twice; it must appear exactly once
- q022ca1561b (ticket): the first answer had the same text as another header (see the TAKEN list); write a clearly different one
- qc00bd9ba09 (yaml): the first answer had the same text as another header (see the TAKEN list); write a clearly different one

## TAKEN texts (already accepted; do not reproduce any of them; one JSON string per line)

### register chat (38 taken)
"{WORKER}: At the regional service office, case {CASE_ID} concerns {SUBJECT}."
"{WORKER}: Case {CASE_ID} is logged on the review desk for {SUBJECT}."
"{WORKER}: Happy to take {CASE_ID} about {SUBJECT}, thanks for flagging!"
"{WORKER}: Lovely to hear from {SUBJECT}, {CASE_ID} is in hand."
"{WORKER}: Lovely to log {CASE_ID} for {SUBJECT} with the records office, thanks!"
"{WORKER}: Lovely to see you, {SUBJECT}; the staff desk has case {CASE_ID} in good hands."
"{WORKER}: Noted, {CASE_ID} for {SUBJECT} sits with the intake desk."
"{WORKER}: Pulling up case {CASE_ID} for {SUBJECT}, busy as ever."
"{WORKER}: Quick call from the district office on case {CASE_ID} for {SUBJECT}."
"{WORKER}: Routine check on {CASE_ID} for {SUBJECT} at the front counter."
"{WORKER}: The review desk notes case {CASE_ID} concerning {SUBJECT}."
"{WORKER}: Thread for {CASE_ID} covers {SUBJECT}."
"{WORKER}: Warm thanks to {SUBJECT} for case {CASE_ID}, handled with care."
"{WORKER}: branch team is glad to hold {CASE_ID} for {SUBJECT}."
"{WORKER}: busy hub, file {CASE_ID} is in front of me, about {SUBJECT}."
"{WORKER}: case reference {CASE_ID} is held for {SUBJECT}."
"{WORKER}: cheers, the staff support desk has {CASE_ID} for {SUBJECT}."
"{WORKER}: counter queue has {CASE_ID}, and it is about {SUBJECT}."
"{WORKER}: file {CASE_ID} about {SUBJECT} is on my list."
"{WORKER}: for the record, file {CASE_ID} belongs to {SUBJECT}."
"{WORKER}: help line has {SUBJECT} on {CASE_ID}."
"{WORKER}: hi team, thread for {CASE_ID} covers {SUBJECT}, thanks!"
"{WORKER}: outreach list has {CASE_ID} for {SUBJECT}."
"{WORKER}: picking up case {CASE_ID} for {SUBJECT}."
"{WORKER}: please see case {CASE_ID} regarding {SUBJECT}."
"{WORKER}: quick check on case {CASE_ID} for {SUBJECT}."
"{WORKER}: quick check on file {CASE_ID} for {SUBJECT}, at the counter."
"{WORKER}: quick ping, {CASE_ID} is in the people services queue for {SUBJECT}."
"{WORKER}: quick update, case {CASE_ID} is up for {SUBJECT}."
"{WORKER}: routine check on {CASE_ID} for {SUBJECT}, logged on the help line."
"{WORKER}: routine check on {SUBJECT} under {CASE_ID}."
"{WORKER}: routine file {CASE_ID} about {SUBJECT}, as usual."
"{WORKER}: thanks for waiting, {SUBJECT} is on {CASE_ID}."
"{WORKER}: thanks, admin desk has {CASE_ID} set up for {SUBJECT}."
"{WORKER}: the file {CASE_ID} concerns {SUBJECT} and is on the regional desk."
"{WORKER}: the formal record of file {CASE_ID} is about {SUBJECT}."
"{WORKER}: {CASE_ID} for {SUBJECT} is on my list, moving fast."
"{WORKER}: {CASE_ID} is up on the desk, about {SUBJECT}."

### register ticket (37 taken)
"Back office ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Call centre ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Casework team ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Community ticket: {CASE_ID}\nHandled by: {WORKER}\nAbout: {SUBJECT}"
"Counter ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Desk ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Friendly ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Help line ticket {CASE_ID}\nFor: {SUBJECT}\nRaised by: {WORKER}"
"Help ticket: {CASE_ID}\nWho: {WORKER}\nAbout: {SUBJECT}"
"Hub ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Intake ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Quick ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Records office ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ref: {CASE_ID}\nAbout: {SUBJECT}\nRaised by: {WORKER}"
"Review ticket: {CASE_ID}\nOwner: {WORKER}\nAbout: {SUBJECT}"
"Review ticket: {CASE_ID}\nraised by: {WORKER}\nabout: {SUBJECT}"
"Routine ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Staff support desk ticket: {CASE_ID}\nLogged by: {WORKER}\nRegarding: {SUBJECT}"
"Ticket line: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket ref: {CASE_ID}\nOwner: {WORKER}\nSubject: {SUBJECT}"
"Ticket {CASE_ID}\nWith: {WORKER}\nAbout: {SUBJECT}"
"Ticket: branch office, case {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: case {CASE_ID} at the town hall office\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: casework note for case {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: desk record for case {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: district office desk review, case {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: outreach team, with thanks, case {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: people services case {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: quick desk entry on case {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: regional case record {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: staff support desk, case {CASE_ID}\nFrom: {WORKER}\nAbout: {SUBJECT}"
"Ticket: support hub, reference {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: {CASE_ID} at the services counter\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Ticket: {CASE_ID}, front counter\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Walk-in ticket: {CASE_ID}\nRaised by: {WORKER}\nAbout: {SUBJECT}"
"Work ticket {CASE_ID}\nLogged by: {WORKER}\nAbout: {SUBJECT}"

### register yaml (37 taken)
"case: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}"
"case: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}\ndesk: back office"
"case: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}\nkind: file"
"case: {CASE_ID}\ncentre: contact\nhandler: {WORKER}\nperson: {SUBJECT}"
"case: {CASE_ID}\ndesk: services counter\ncaseworker: {WORKER}\nabout: {SUBJECT}"
"case: {CASE_ID}\nhub: support\ncaseworker: {WORKER}\nabout: {SUBJECT}"
"case: {CASE_ID}\nlead: {WORKER}\nperson: {SUBJECT}"
"case_id: {CASE_ID}\nworker_name: {WORKER}\nsubject_name: {SUBJECT}"
"case_ref: {CASE_ID}\nhandled_by: {WORKER}\nperson: {SUBJECT}\ndesk: intake"
"case_ref: {CASE_ID}\nhandler: {WORKER}\nsubject: {SUBJECT}\nclass: file"
"case_ref: {CASE_ID}\nlead: {WORKER}\nperson: {SUBJECT}"
"case_ref: {CASE_ID}\nlead: {WORKER}\nsubject: {SUBJECT}"
"case_ref: {CASE_ID}\nworker: {WORKER}\nsubject: {SUBJECT}"
"desk: community help\ncase: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}"
"desk: intake\ncase: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}"
"district_ref: {CASE_ID}\nhandled_by: {WORKER}\nabout: {SUBJECT}"
"file: {CASE_ID}\nsupport: {WORKER}\nabout: {SUBJECT}\nmood: kind"
"kind: routine case record\ncase: {CASE_ID}\nlead: {WORKER}\nabout: {SUBJECT}"
"record: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}\ntone: warm"
"record: {CASE_ID}\ncaseworker: {WORKER}\nperson: {SUBJECT}"
"record: {CASE_ID}\nlead: {WORKER}\nname: {SUBJECT}"
"record: {CASE_ID}\nlead: {WORKER}\nsubject: {SUBJECT}"
"ref: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}\noffice: branch"
"ref: {CASE_ID}\ncaseworker: {WORKER}\nperson: {SUBJECT}"
"ref: {CASE_ID}\nhandler: {WORKER}\nabout: {SUBJECT}"
"ref: {CASE_ID}\nhandler: {WORKER}\nsubject: {SUBJECT}"
"ref: {CASE_ID}\nlead: {WORKER}\nfor: {SUBJECT}"
"ref: {CASE_ID}\noffice: branch\nlead: {WORKER}\nperson: {SUBJECT}"
"ref: {CASE_ID}\nowner: {WORKER}\nabout: {SUBJECT}\nteam: outreach"
"ref: {CASE_ID}\nworker: {WORKER}\nabout: {SUBJECT}\npace: busy"
"reference: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}\ntone: warm"
"reference: {CASE_ID}\nhandled_by: {WORKER}\nabout: {SUBJECT}\nunit: casework"
"reference: {CASE_ID}\nhandler: {WORKER}\nsubject: {SUBJECT}"
"reference: {CASE_ID}\nworker: {WORKER}\nabout: {SUBJECT}"
"reference: {CASE_ID}\nworker: {WORKER}\nabout: {SUBJECT}\ndesk: front"
"team: casework\ncase: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}"
"team: people services\ncase: {CASE_ID}\ncaseworker: {WORKER}\nabout: {SUBJECT}"

## Items (4; one JSON object per line; these are the exact items of the first task)

```json
[
{"qid": "q022ca1561b", "brief": "Write a work ticket. Setting: an intake desk. Tone: brisk and busy.", "register": "ticket", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A work ticket of 2-3 short 'field: value' lines (for example a ticket line, a 'raised by' line and an 'about' line)."]},
{"qid": "q69d3014c60", "brief": "Write a team chat excerpt. Setting: a back office. Tone: plain and routine.", "register": "chat", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A chat excerpt of 1-2 lines, each 'speaker: message'; the speaker is {WORKER}."]},
{"qid": "qc00bd9ba09", "brief": "Write a YAML case record. Setting: a records office. Tone: warm and friendly.", "register": "yaml", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["3-4 lines of 'key: value' YAML with lower-case keys and plain values; write the placeholders bare as values, for example 'caseworker: {WORKER}'."]},
{"qid": "q478ec3a934", "brief": "Write a team chat excerpt. Setting: a back office. Tone: plain and routine.", "register": "chat", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A chat excerpt of 1-2 lines, each 'speaker: message'; the speaker is {WORKER}."]}
]
```
