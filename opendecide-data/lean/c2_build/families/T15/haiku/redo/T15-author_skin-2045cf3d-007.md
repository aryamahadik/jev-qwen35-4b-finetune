# Haiku REDO task T15-author_skin-2045cf3d-007 (family T15, kind author_skin, pool skins (case-note headers)): 6 item(s) to answer again

THIS ONE FILE IS YOUR WHOLE TASK. Read all of it, write the answer file with the Write tool, then stop.
Do not open, search or list any other file or folder. Create no other file. Do not put the answer in chat.

Write your answer to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/haiku/redo/answers/T15-author_skin-2045cf3d-007.json

## Answer contract (exact)

The answer file holds ONE JSON list and nothing else: no text before or after it, no comment, no code fence, no wrapper object.
The list has exactly 6 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys,
"qid" and "text". This is the literal shape of the file:

[
  {"qid": "q37e688b3ec", "text": "<header for this item>"},
  {"qid": "q9d7390e1d0", "text": "<header for this item>"},
  {"qid": "qd0079e2c60", "text": "<header for this item>"},
  {"qid": "qfe17337c5d", "text": "<header for this item>"},
  {"qid": "q7e86ac91a0", "text": "<header for this item>"},
  {"qid": "q5b0e763b79", "text": "<header for this item>"}
]

"qid" is copied character for character from its item. "text" is a non-empty JSON string: write a line break inside it as \n
(never a raw line break) and escape a double quote as \". A JSON-register header contains double quotes: escape each one inside your answer string as \" so that the answer file stays valid JSON.
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
  - json: one JSON object on one line; the placeholders sit bare as values (no quotes around them) or inside a quoted string; every other key and value is lower-case letters and underscores only; choose key names and an order that differ from every taken text of this register.
  - memo: write the sentence in your own words; the word "kept" is rejected, so do not say a file is kept by anyone; say who "has", "handles", "wrote" or "looks after" it.
  - ticket: choose field labels, wording and order that differ from every taken ticket; do not repeat the shape "Ticket / Raised by / About".

## What went wrong with the first answer, by qid

- qfe17337c5d (json): the first answer had the same text as another header (see the TAKEN list); write a clearly different one
- qd0079e2c60 (memo): the first answer used the banned status word "kept"
- q9d7390e1d0 (memo): the first answer used the banned status word "kept"
- q5b0e763b79 (memo): G-SL status: Kept
- q7e86ac91a0 (ticket): the first answer had the same text as another header (see the TAKEN list); write a clearly different one
- q37e688b3ec (ticket): the first answer had the same text as another header (see the TAKEN list); write a clearly different one

## TAKEN texts (already accepted; do not reproduce any of them; one JSON string per line)

### register json (39 taken)
"{\"about\": {SUBJECT}, \"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"team\": \"help line\"}"
"{\"case\": \"{CASE_ID}\", \"caseworker\": \"{WORKER}\", \"about\": \"{SUBJECT}\", \"desk\": \"call centre\"}"
"{\"case\": {CASE_ID}, \"about\": {SUBJECT}, \"caseworker\": {WORKER}, \"service\": \"regional\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"desk\": \"intake\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"desk\": \"internal\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"desk\": \"services counter\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"hub\": \"support\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"kind\": \"case file\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"line\": \"help\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"team\": \"casework\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"team\": \"outreach\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"tone\": \"warm\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"unit\": \"staff support\"}"
"{\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}}"
"{\"case\": {CASE_ID}, \"handler\": {WORKER}, \"about\": {SUBJECT}, \"team\": \"people_services\"}"
"{\"case\": {CASE_ID}, \"lead\": {WORKER}, \"subject\": {SUBJECT}, \"office\": \"town_hall\"}"
"{\"case\": {CASE_ID}, \"reviewer\": {WORKER}, \"about\": {SUBJECT}, \"desk\": \"review\"}"
"{\"case\": {CASE_ID}, \"worker\": {WORKER}, \"about\": {SUBJECT}, \"office\": \"town hall\"}"
"{\"case_id\": {CASE_ID}, \"worker\": {WORKER}, \"person\": {SUBJECT}}"
"{\"case_ref\": {CASE_ID}, \"handler\": {WORKER}, \"about\": \"{SUBJECT}\", \"type\": \"file\"}"
"{\"case_ref\": {CASE_ID}, \"handler\": {WORKER}, \"subject\": {SUBJECT}}"
"{\"case_ref\": {CASE_ID}, \"owner\": \"{WORKER}\", \"about\": {SUBJECT}}"
"{\"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"case\": {CASE_ID}, \"desk\": \"community\"}"
"{\"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"case\": {CASE_ID}, \"office\": \"branch\"}"
"{\"caseworker\": {WORKER}, \"case\": \"{CASE_ID}\", \"about\": \"{SUBJECT}\", \"hub\": \"support\"}"
"{\"file\": {CASE_ID}, \"worker\": {WORKER}, \"subject\": \"{SUBJECT}\", \"desk\": \"staff support\"}"
"{\"record\": \"case\", \"reference\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}}"
"{\"record\": {CASE_ID}, \"handler\": {WORKER}, \"subject\": {SUBJECT}}"
"{\"record\": {CASE_ID}, \"officer\": {WORKER}, \"concerning\": \"{SUBJECT}\"}"
"{\"ref\": \"{CASE_ID}\", \"caseworker\": {WORKER}, \"about\": {SUBJECT}}"
"{\"ref\": {CASE_ID}, \"caseworker\": \"{WORKER}\", \"about\": {SUBJECT}, \"kind\": \"intake\"}"
"{\"ref\": {CASE_ID}, \"handled_by\": {WORKER}, \"about\": {SUBJECT}, \"setting\": \"walk-in\"}"
"{\"ref\": {CASE_ID}, \"handler\": \"{WORKER}\", \"subject\": \"{SUBJECT}\", \"desk\": \"walk-in\"}"
"{\"ref\": {CASE_ID}, \"handler\": {WORKER}, \"about\": {SUBJECT}}"
"{\"ref\": {CASE_ID}, \"lead\": \"{WORKER}\", \"person\": {SUBJECT}}"
"{\"ref\": {CASE_ID}, \"worker\": {WORKER}, \"about\": {SUBJECT}, \"team\": \"outreach\"}"
"{\"reference\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}, \"office\": \"district\"}"
"{\"reference\": {CASE_ID}, \"held_by\": {WORKER}, \"about\": {SUBJECT}, \"unit\": \"district\"}"
"{\"team\": \"casework\", \"case_ref\": {CASE_ID}, \"worker\": {WORKER}, \"about\": \"{SUBJECT}\"}"

### register memo (36 taken)
"A quick note for the district team: {WORKER} is taking care of {CASE_ID} for {SUBJECT}."
"Back office note: {WORKER} is moving case {CASE_ID} for {SUBJECT}."
"Case note from the support hub: {WORKER} is handling case {CASE_ID} for {SUBJECT}."
"Case note: a warm hello from the services counter. {WORKER} has {CASE_ID} for {SUBJECT}."
"Case note: routine check on {CASE_ID}, held by {WORKER} for {SUBJECT}."
"Case note: thanks for your patience. {WORKER} has {CASE_ID} in hand for {SUBJECT}."
"Case note: the help desk has {WORKER} on file {CASE_ID} for {SUBJECT}."
"Case note: the intake desk has {SUBJECT} on case {CASE_ID}, with {WORKER} in charge."
"Case note: the record for {SUBJECT} sits under {CASE_ID}, and {WORKER} is the caseworker on it."
"Case note: the staff support desk holds the record for {SUBJECT}. Case {CASE_ID}, handled by {WORKER}."
"Case note: {CASE_ID} for {SUBJECT}. Handled by {WORKER}."
"Case note: {CASE_ID} is in good hands with {WORKER}, who looks after the matter for {SUBJECT}."
"Case note: {CASE_ID} is with {WORKER}. Quick update on {SUBJECT} from the outreach team."
"Case note: {CASE_ID} sits with {WORKER} and concerns {SUBJECT}."
"Case note: {WORKER} covers case {CASE_ID} for {SUBJECT}, with thanks."
"Case note: {WORKER} holds case file {CASE_ID} about {SUBJECT}. The record sits at the town hall desk."
"Case note: {WORKER} holds case {CASE_ID} for {SUBJECT}."
"Case note: {WORKER} holds the matter of {SUBJECT} under reference {CASE_ID}."
"Case note: {WORKER} is glad to hold case {CASE_ID} for {SUBJECT}."
"Case note: {WORKER} is glad to take on the matter of {SUBJECT}, reference {CASE_ID}."
"Case note: {WORKER} is handling {SUBJECT} on case {CASE_ID}. Thanks for the help."
"Case note: {WORKER} logged file {CASE_ID} for {SUBJECT} at the walk-in desk."
"Case note: {WORKER} picks up file {CASE_ID}, about {SUBJECT}, at the counter."
"Desk note: {CASE_ID}\nQuick note by {WORKER} at the community help desk, about {SUBJECT}."
"Front counter note: {WORKER} logged case {CASE_ID} for {SUBJECT} in a hurry."
"Internal case note for {CASE_ID}.\nSet down by {WORKER} at the town hall office, for {SUBJECT}."
"Internal note for the branch desk. {CASE_ID} rests with {WORKER} and concerns {SUBJECT}."
"Internal note: {CASE_ID} is held by {WORKER}. Regarding {SUBJECT}, please refer to the desk log."
"Internal note: {WORKER} handles case {CASE_ID} about {SUBJECT}."
"Note for the intake desk: {SUBJECT} is named on case {CASE_ID}, which {WORKER} keeps."
"Note for {CASE_ID}, with thanks.\n{WORKER} is looking after {SUBJECT} at the district office."
"Quick note from the help line: {WORKER} is on {CASE_ID} for {SUBJECT}."
"Quick note: {WORKER} is running {CASE_ID} for {SUBJECT}. Outreach is moving fast."
"Records desk note. {WORKER} keeps {CASE_ID}, which concerns {SUBJECT}."
"Routine case note: {CASE_ID} sits with {WORKER} about {SUBJECT}. Standard entry for the call centre."
"Routine note: {CASE_ID}\nFrom {WORKER} for the call centre, about {SUBJECT}."

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

## Items (6; one JSON object per line; these are the exact items of the first task)

```json
[
{"qid": "q37e688b3ec", "brief": "Write a work ticket. Setting: a town hall office. Tone: plain and routine.", "register": "ticket", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A work ticket of 2-3 short 'field: value' lines (for example a ticket line, a 'raised by' line and an 'about' line)."]},
{"qid": "q9d7390e1d0", "brief": "Write an internal case note. Setting: a help line team. Tone: brisk and busy.", "register": "memo", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A short internal note of 1-2 sentences; it may open with a label such as 'Case note:'."]},
{"qid": "qd0079e2c60", "brief": "Write an internal case note. Setting: a records office. Tone: formal and dry.", "register": "memo", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A short internal note of 1-2 sentences; it may open with a label such as 'Case note:'."]},
{"qid": "qfe17337c5d", "brief": "Write a JSON case record. Setting: a review desk. Tone: plain and routine.", "register": "json", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["One JSON object on one line with 3-4 lower-case keys, for example {\"case\": {CASE_ID}, \"caseworker\": {WORKER}, \"about\": {SUBJECT}}. Write each placeholder bare as a value (no quotes around it) or inside a quoted string; any other value is a short quoted lower-case string."]},
{"qid": "q7e86ac91a0", "brief": "Write a work ticket. Setting: a front counter. Tone: warm and friendly.", "register": "ticket", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A work ticket of 2-3 short 'field: value' lines (for example a ticket line, a 'raised by' line and an 'about' line)."]},
{"qid": "q5b0e763b79", "brief": "Write an internal case note. Setting: a review desk. Tone: plain and routine.", "register": "memo", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A short internal note of 1-2 sentences; it may open with a label such as 'Case note:'."]}
]
```
