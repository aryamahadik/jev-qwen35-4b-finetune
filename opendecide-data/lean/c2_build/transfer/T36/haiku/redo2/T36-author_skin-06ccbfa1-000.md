# Haiku REDO-2 task T36-author_skin-06ccbfa1-000 (family T36, kind author_skin): 1 item(s), 3 candidate texts each

Read this whole file. Do not open, list, search or write any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T36/haiku/redo2/answers/T36-author_skin-06ccbfa1-000.json

## Answer contract (exact)

The answer file holds ONE JSON array with exactly 1 object(s), one per item below, every qid exactly once (any order). Each object has exactly two keys: "qid" (the item's qid, copied exactly) and "texts" (a list of exactly 3 different strings: 3 alternative texts for that item, each complete on its own and each following every rule below; write \n for a line break and \" for a double quote in a string).
Valid JSON only: no text before or after the array, no comments, no code fence, no other keys. Every item answered once.

Literal example of the required shape:

[
  {"qid": "qa2b46e4961", "texts": ["<text A>", "<text B>", "<text C>"]},
  ...
]

How the texts are used: a program checks each text against the rules below in the order you wrote them and keeps the first text that passes every check; the others are thrown away. So every text must follow every rule, and the texts of one item must be clearly different from each other.

## Instructions

You are writing short text pieces for a test set about software projects and the external packages they depend on. Invent everything: never copy text from real projects, packages, companies, people or websites. Write in English. Make every text clearly different from every other text in this file (structure, opening, length, word choice). Each item below has a qid and the details of what to write; the answer is one object per item as in the contract above.

TASK: for each item write 3 alternative short narrative texts in the item's register (style notes below): a note from or about the maintainer of a software project who is looking at the project's dependency on one package. Right after your text a program prints the package's declared version range, its published versions and a question; your text only sets the scene and adds no fact of its own.
Placeholders: use exactly these three, each EXACTLY ONCE, copied exactly with their braces: {PERSON} (the maintainer's full name, e.g. Dana Okafor), {PROJECT} (the project's name, e.g. Harbor Lantern) and {PKG} (the package's id, e.g. fernhill-cache; use it as a name, as in "the {PKG} package" or "package {PKG}"). Never use another placeholder or curly brace, never write a real value in their place, and never put "a" or "an" directly before a placeholder.
Register styles: maintainer_email: an e-mail: an optional "Subject:" line, a greeting, a short body and a sign-off
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
   - status words: accept, accepted, active, allow, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
   - condition words: except, if, instead, otherwise, provided, providing, regardless, unless
   - phrases: have to, has to, had to, got to, sort of, kind of
3. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, refuse to, prevent ... from, rule out.
4. Capital letters only at the start of a sentence, a line, a list item or a label, and for CI, PR, QA and API; no names of people, companies, products, places or teams (the placeholders carry the only names).
5. Say nothing about versions or version numbers, version ranges, operators or symbols, release stages (test builds, release candidates, nightly builds and the like), whether any version is acceptable, suitable, approved or safe, which version gets picked or used, moving to another version, or how new or old anything is; use no word that ranks versions by age or by order. Never hint at any answer: the text only sets the scene for a look at the project's dependency on the package.
Follow each item's angle for variety. Before writing, check every text: the three placeholders each appear exactly once; no digit; no banned word; no negation.

## Redo note

REDO NOTE (added for this second redo; every rule above still holds). Earlier texts for each item below were thrown away by the program's word check. Write completely new texts. Causes to avoid:
- A missing placeholder: a text that said "the package" and left out {PKG}. Each text holds {PERSON}, {PROJECT} and {PKG}, each exactly once, copied with braces; count them in every text before you write the file.
- Reserved words. The check throws away a text that uses any of these kinds of words, in any form (with -s, -ed, -ing and the like):
  - words that judge whether something agrees with, suits, corresponds to or is admitted by a requirement, a rule or a limit, and words for being able to work together with something or for backing it;
  - the everyday verb and noun for getting together with people (a get-together of the team): they are spelled like a reserved word, so write "sync", "call", "catch-up", "planning session" or "review session";
  - place words for being in the interior of something, in a region bounded by a limit, or beyond its edge: write plain position words such as "in", "at", "for", "across", "around", "near";
  - words about letting something into a group or keeping it out of one;
  - words about putting software onto a machine, and words for settling a question (write "look into", "work through", "go over");
  - comparison words for height, rank or age: the -er and -est forms of high, low, new and old, and the -est form of late;
  - words about how steady software is, about changes that harm its users, about moving software to a different level, and the names of early test stages of software.
- The word "third" in any form, also as part of "third-party" (write "external package" or "imported package"; the check reads every part of a hyphenated word), and every other word in the lists of hard rule 2; "can" and "much" slipped in earlier. Re-read every text word by word against those lists.
- Any word about setting up, choosing, picking or swapping software, or about how new a package is.
The scene is only who is looking at what in the project, and why: plain words such as "looking at", "reviewing", "checking", "going over", "notes on", "handing over", "keeping track of".
Before you write the file, check each text: {PERSON}, {PROJECT} and {PKG} each exactly once; no "a" or "an" right before a placeholder; no digit; no word from the lists; no negation; no reserved word.

## Items (1; one JSON object per line)

```json
[
{"qid": "qa2b46e4961", "brief": "Angle: plain and brief. Write 3 alternative texts.", "register": "maintainer_email", "slots": ["{PERSON}", "{PROJECT}", "{PKG}"], "rules": ["use each of {PERSON}, {PROJECT}, {PKG} exactly once", "write in the maintainer_email register (style notes in the instructions)"]}
]
```
