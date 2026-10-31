# Haiku REDO task T15-author_skin-2045cf3d-001 (family T15, kind author_skin, pool skins (case-note headers)): 1 item(s) to answer again

THIS ONE FILE IS YOUR WHOLE TASK. Read all of it, write the answer file with the Write tool, then stop.
Do not open, search or list any other file or folder. Create no other file. Do not put the answer in chat.

Write your answer to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/haiku/redo/answers/T15-author_skin-2045cf3d-001.json

## Answer contract (exact)

The answer file holds ONE JSON list and nothing else: no text before or after it, no comment, no code fence, no wrapper object.
The list has exactly 1 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys,
"qid" and "text". This is the literal shape of the file:

[
  {"qid": "q231cf5040f", "text": "<header for this item>"}
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
  - email: greeting line, one sentence, sign-off line holding {WORKER}; the word "kept" is rejected.

## What went wrong with the first answer, by qid

- q231cf5040f (email): the first answer used the banned status word "kept"

## TAKEN texts (already accepted; do not reproduce any of them; one JSON string per line)

### register email (39 taken)
"Dear colleague,\nCase reference {CASE_ID} concerns {SUBJECT}.\nYours faithfully, {WORKER}"
"Dear colleague,\nFor the record, {CASE_ID} concerning {SUBJECT} is held by the desk.\nYours faithfully, {WORKER}"
"Dear colleague,\nPlease see {CASE_ID} about {SUBJECT} on the queue.\nThanks, {WORKER}"
"Dear colleague,\nThe file {CASE_ID} about {SUBJECT} is attached to this mail.\nYours faithfully, {WORKER}"
"Dear colleague,\nThe record {CASE_ID} for {SUBJECT} has been sent to the front counter.\nRegards, {WORKER}"
"Dear colleague,\nThis is a short outreach note on case {CASE_ID} for {SUBJECT}.\nRegards, {WORKER}"
"Dear team,\nPlease see the attached summary on case {CASE_ID} for {SUBJECT}.\nYours sincerely, {WORKER}"
"Dear {SUBJECT},\nCase {CASE_ID} is recorded with the help line team.\nSincerely, {WORKER}"
"Dear {SUBJECT},\nPlease find {CASE_ID} logged with the help line team.\nYours faithfully, {WORKER}"
"Dear {SUBJECT},\nThanks for getting in touch about case {CASE_ID}.\nWarm wishes, {WORKER}"
"Dear {SUBJECT},\nThis concerns case {CASE_ID} with the outreach team.\nYours faithfully, {WORKER}"
"Dear {SUBJECT},\nThis is a standard notice about {CASE_ID} from the district office.\nKind regards, {WORKER}"
"Dear {SUBJECT},\nThis reply concerns case {CASE_ID}.\nYours sincerely, {WORKER}"
"Hello team,\nThank you for reviewing case {CASE_ID} with a warm eye on {SUBJECT}.\nWarm regards, {WORKER}"
"Hello there,\nA short update on file {CASE_ID} for {SUBJECT} follows below.\nBest, {WORKER}"
"Hello there,\nThanks for calling about {SUBJECT}; the reference is {CASE_ID}.\nKind regards, {WORKER}"
"Hello there,\nThis note is about {SUBJECT}, under case reference {CASE_ID}.\nWarm regards, {WORKER}"
"Hello {SUBJECT},\nA routine note about {CASE_ID} comes from the district office.\nBest wishes, {WORKER}"
"Hello {SUBJECT},\nQuick update: the staff support desk has {CASE_ID} in view.\nRegards, {WORKER}"
"Hello {SUBJECT},\nThanks for popping in about case {CASE_ID}.\nWarm regards, {WORKER}"
"Hello,\nHere is the write-up for {CASE_ID} about {SUBJECT}.\nWith thanks, {WORKER}"
"Hello,\nThe casework team holds {CASE_ID} for {SUBJECT}.\nBest, {WORKER}"
"Hello,\nYour details for {SUBJECT} are with the intake desk under {CASE_ID}.\nWarm regards, {WORKER}"
"Hi team,\nA short routine note goes out on case {CASE_ID} about {SUBJECT}.\nThanks, {WORKER}"
"Hi team,\nCase {CASE_ID} for {SUBJECT} has gone to the desk.\nThanks, {WORKER}"
"Hi team,\nThanks for waiting, {CASE_ID} about {SUBJECT} is in good hands.\nWarm wishes, {WORKER}"
"Hi team,\nThis mail concerns file {CASE_ID}, which is about {SUBJECT}.\nRegards, {WORKER}"
"Hi {SUBJECT},\nBrief update on case {CASE_ID} below.\nThanks, {WORKER}"
"Hi {SUBJECT},\nBrisk update from the branch office on {CASE_ID}.\nCheers, {WORKER}"
"Hi {SUBJECT},\nQuick note on case {CASE_ID} follows.\nCheers, {WORKER}"
"Hi {SUBJECT},\nThank you for coming in to the walk-in centre about {CASE_ID}.\nWarm wishes, {WORKER}"
"Hi {SUBJECT},\nThanks for holding on about case {CASE_ID}.\nTake care, {WORKER}"
"Hi {SUBJECT},\nThe town hall office is holding {CASE_ID} for you.\nThanks, {WORKER}"
"Hi {SUBJECT},\nThis is a quick note on case {CASE_ID} from the records office.\nCheers, {WORKER}"
"Hi {SUBJECT},\nThis is a routine update on case {CASE_ID}.\nBest, {WORKER}"
"Hi {SUBJECT},\nYour case {CASE_ID} is being reviewed with care.\nKind thanks, {WORKER}"
"Hi {SUBJECT},\nYour case {CASE_ID} sits with the casework team.\nBest, {WORKER}"
"Hi,\nQuick update: file {CASE_ID} about {SUBJECT} is in my queue.\nThanks, {WORKER}"
"Hi,\nQuick word on {CASE_ID} for {SUBJECT}, as the desk is busy.\nCheers, {WORKER}"

## Items (1; one JSON object per line; these are the exact items of the first task)

```json
[
{"qid": "q231cf5040f", "brief": "Write a short e-mail. Setting: a people services team. Tone: plain and routine.", "register": "email", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A short e-mail of 2-3 lines with no empty line: a greeting line, one sentence, and a sign-off line that holds {WORKER}."]}
]
```
