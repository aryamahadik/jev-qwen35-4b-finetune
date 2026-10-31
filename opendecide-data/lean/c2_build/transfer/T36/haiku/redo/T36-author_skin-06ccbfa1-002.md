# Haiku REDO task T36-author_skin-06ccbfa1-002 (family T36, kind author_skin): 13 item(s) to answer again

Read this whole file. Do not open, list, search or write any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T36/haiku/redo/answers/T36-author_skin-06ccbfa1-002.json

## Answer contract (exact)

The answer file holds ONE JSON array with exactly 13 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "text" (a string: the text you wrote; write \n for a line break and \" for a double quote in the text).
Valid JSON only: no text before or after the array, no comments, no code fence, no other keys. Every item answered once.

Literal example of the required shape:

[
  {"qid": "q97285fb1bd", "text": "<your new text for this item>"},
  {"qid": "q7507d85e00", "text": "<your new text for this item>"},
  ...
]

## Instructions

You are writing short text pieces for a test set about software projects and the external packages they depend on. Invent everything: never copy text from real projects, packages, companies, people or websites. Write in English. Make every piece clearly different from the others in this file (structure, opening, length, word choice). Each item below has a qid and the details of one piece to write; the answer is one object per item as in the contract above.

TASK: for each item write ONE short narrative text in the item's register (style notes below): a note from or about the maintainer of a software project who is looking at the project's dependency on one package. Right after your text a program prints the package's declared version range, its published versions and a question; your text only sets the scene and adds no fact of its own.
Placeholders: use exactly these three, each EXACTLY ONCE, copied exactly with their braces: {PERSON} (the maintainer's full name, e.g. Dana Okafor), {PROJECT} (the project's name, e.g. Harbor Lantern) and {PKG} (the package's id, e.g. fernhill-cache; use it as a name, as in "the {PKG} package" or "package {PKG}"). Never use another placeholder or curly brace, never write a real value in their place, and never put "a" or "an" directly before a placeholder.
Register styles: dep_pr_review: a review comment on a pull request that touches the project's dependencies: one to three sentences | dev_chat: a team-chat message: one to three short chat lines | maintainer_email: an e-mail: an optional "Subject:" line, a greeting, a short body and a sign-off | issue: an issue-tracker post: a short title line, then a body of one to three sentences | dep_ticket: a ticket written as plain "Field: value" lines (such as Summary, Owner, Component, Notes) | dep_wiki: a short paragraph from the project's internal wiki page about its external packages
Length: 12-60 words (log and ticket lines may be shorter). One block of text: no empty line, no leading or trailing spaces; line breaks only where the register needs them.
Hard rules (a text that breaks one is thrown away):
1. Apart from the placeholders: no digits, no dates, times, months or weekdays, no currency or percent signs, no web or e-mail addresses, no codes or ids.
2. Apart from the placeholders, none of these words (any letter case):
   - number words: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
   - time words: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
   - quantity words: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
   - quantifiers: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
   - modal words: able, can, cannot, could, forbidden, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, would
   - hedges: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
   - status words: accept, accepted, active, allow, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
   - condition words: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
   - phrases: have to, has to, had to, got to, sort of, kind of
3. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, refuse to, prevent ... from, rule out.
4. Capital letters only at the start of a sentence, a line, a list item or a label, and for CI, PR, QA and API; no names of people, companies, products, places or teams (the placeholders carry the only names).
5. Say nothing about versions or version numbers, version ranges, operators or symbols, release stages (test builds, release candidates, nightly builds and the like), whether any version is acceptable, suitable, approved or safe, which version gets picked or used, moving to another version, or how new or old anything is; use no word that ranks versions by age or by order. Never hint at any answer: the text only sets the scene for a look at the project's dependency on the package.
Follow each item's angle for variety. Before writing, check every text: the three placeholders each appear exactly once; no digit; no banned word; no negation.

## Redo note

REDO NOTE (added for this redo; every rule above still holds). An earlier text for each item below was thrown away by the
program's word check. Write a completely NEW text for each item, in the item's register and following the item's angle.
Slips that caused the earlier rejections; avoid all of them:
- The word "third" in any form, above all in "third-party". When you mean packages that come from elsewhere, write
  "external packages" or "imported packages". The check reads every part of a hyphenated word, so "third-party" fails.
- The words "can" and "much", and every other modal or quantity word from the lists above. Re-read your text word by word.
- Words that judge whether something suits, agrees with, corresponds to or is admitted by a requirement, a rule or a limit;
  words that put something on one side or the other of a boundary or limit; words about letting something into, or keeping
  it out of, a group; words about permission or support. They slip into everyday phrases (a phrase about how well something
  "suits" a team habit, about what sits "at the edge" of a group, about what is "let in"). The scene is only who is looking
  at what in the project, and why. Use plain scene-setting words such as "looking at", "reviewing", "checking", "going
  over", "notes on", "handing over", "keeping track of", and plain position words such as "in", "at", "across", "around",
  "behind", "near".
- Any word about setting up, choosing, picking, swapping or supporting software, or about how steady or how new a package
  is.
Keep every text different from every other text in this file (opening, structure, length, word choice). Before you write the
file, read each text once more against the word lists above and against this note.

## Items (13; one JSON object per line)

```json
[
{"qid": "q97285fb1bd", "brief": "Angle: formal and courteous. Write one text.", "register": "maintainer_email", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the maintainer_email register (style notes in the instructions)"]},
{"qid": "q7507d85e00", "brief": "Angle: routine housekeeping. Write one text.", "register": "maintainer_email", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the maintainer_email register (style notes in the instructions)"]},
{"qid": "qbc6288960d", "brief": "Angle: written by a new team member who is still learning the codebase. Write one text.", "register": "issue", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the issue register (style notes in the instructions)"]},
{"qid": "qb5f69a8e80", "brief": "Angle: formal and courteous. Write one text.", "register": "dep_pr_review", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dep_pr_review register (style notes in the instructions)"]},
{"qid": "qa871beabb9", "brief": "Angle: written while preparing a release. Write one text.", "register": "dep_wiki", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dep_wiki register (style notes in the instructions)"]},
{"qid": "qc156a20a77", "brief": "Angle: a hand-over note to a teammate. Write one text.", "register": "dep_wiki", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dep_wiki register (style notes in the instructions)"]},
{"qid": "qdb1272326c", "brief": "Angle: careful and precise. Write one text.", "register": "dev_chat", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dev_chat register (style notes in the instructions)"]},
{"qid": "q9e14310560", "brief": "Angle: part of a weekly dependency review. Write one text.", "register": "dep_wiki", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dep_wiki register (style notes in the instructions)"]},
{"qid": "qf54a50036f", "brief": "Angle: friendly and relaxed. Write one text.", "register": "dep_wiki", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dep_wiki register (style notes in the instructions)"]},
{"qid": "qaee879e2e4", "brief": "Angle: asks a colleague for a second pair of eyes. Write one text.", "register": "dep_wiki", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dep_wiki register (style notes in the instructions)"]},
{"qid": "qb70b43433a", "brief": "Angle: plain and brief. Write one text.", "register": "dep_ticket", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dep_ticket register (style notes in the instructions)"]},
{"qid": "qbdfc799469", "brief": "Angle: plain and brief. Write one text.", "register": "dep_wiki", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the dep_wiki register (style notes in the instructions)"]},
{"qid": "q9e704e80c1", "brief": "Angle: formal and courteous. Write one text.", "register": "issue", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the issue register (style notes in the instructions)"]}
]
```
