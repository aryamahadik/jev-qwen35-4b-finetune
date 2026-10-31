# Haiku REDO task T15-author_skin-2045cf3d-004 (family T15, kind author_skin, pool skins (case-note headers)): 1 item(s) to answer again

THIS ONE FILE IS YOUR WHOLE TASK. Read all of it, write the answer file with the Write tool, then stop.
Do not open, search or list any other file or folder. Create no other file. Do not put the answer in chat.

Write your answer to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T15/haiku/redo/answers/T15-author_skin-2045cf3d-004.json

## Answer contract (exact)

The answer file holds ONE JSON list and nothing else: no text before or after it, no comment, no code fence, no wrapper object.
The list has exactly 1 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys,
"qid" and "text". This is the literal shape of the file:

[
  {"qid": "qe399c528aa", "text": "<header for this item>"}
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
  - memo: write the sentence in your own words; the word "kept" is rejected, so do not say a file is kept by anyone; say who "has", "handles", "wrote" or "looks after" it.

## What went wrong with the first answer, by qid

- qe399c528aa (memo): the first answer used the banned status word "kept"

## TAKEN texts (already accepted; do not reproduce any of them; one JSON string per line)

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

## Items (1; one JSON object per line; these are the exact items of the first task)

```json
[
{"qid": "qe399c528aa", "brief": "Write an internal case note. Setting: a regional service office. Tone: plain and routine.", "register": "memo", "slots": {"CASE_ID": "case reference", "WORKER": "caseworker name", "SUBJECT": "name of the person the file is about"}, "rules": ["A short internal note of 1-2 sentences; it may open with a label such as 'Case note:'."]}
]
```
