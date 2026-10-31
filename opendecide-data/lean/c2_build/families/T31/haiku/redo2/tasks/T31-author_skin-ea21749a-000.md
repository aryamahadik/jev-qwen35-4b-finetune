# T31 TOP-UP authoring task T31-author_skin-ea21749a-000 (kind: author_skin; 28 items)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/answers/T31-author_skin-ea21749a-000.json

WHY THIS TASK EXISTS: new items for the T31 pool (log|appr: 28 of 36 v1 skins failed the G-SL name lint (capital after the tag); lowercase brief). Every item is new; answer all 28.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 28 objects, one per item at the bottom of this file.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character. A qid is the letter q followed by ten letters or digits
  (11 characters in all). Every qid below appears exactly once in your answer; never invent or shorten one.
- "text": your text as one JSON string (a line break inside it as \n, a double quote as \").
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
- The 28 qids of this task: q3c3089b6af, q17238657d8, q749911b0ed, q9059eaebe4, q4ebd8199fe, q55b2842e2d, qc70ae2c1bd, q7c682c83e3, qbdff004e84, qc9a9cf622e, qd19e70b239, q3971eb3304, qebbab0b818, q4893674328, q9ba2b4cbe2, qa198f939e8, q1a64661907, q579f6cc825, qe5f0d40c66, qa69f6cf818, q28dbf1027a, q38c0d697b3, qb486d782ab, q8eefb0132a, q708bdc4384, qa506a50f3d, qa07a5e5a21, q780494a7c8
Literal example of the shape (your own text in "text"):
[{"qid": "q3c3089b6af", "text": "..."}, ...]

Task kind: author_skin; items: 28; answers expected: 28 (one per item, each with its qid).

FULL INSTRUCTIONS:

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write NARRATIVE SKINS in the register "log" (one to three log lines, each starting with a lowercase tag in square brackets such as [intake] or [desk], then one space and text written ENTIRELY in lowercase; no timestamps, no level words, no line numbers).
A program later puts a block of records and a question after your text; you never see them. Your text only says who
raised which request. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.

Placeholders (keep each exactly as written, braces and capitals included):
  {REQUESTER}  the full name of the person who raised the request. Use it exactly once.
  {ITEM}       a short lowercase noun phrase naming what the request is about. Use it exactly once (a grammar
               helper below counts as the use).
  {REQ_ID}     the request's reference code. Use it exactly once where the item says so; otherwise leave it out.
Grammar helpers, used instead of writing the article or the capital yourself: {a|ITEM} gives "a" or "an" plus the
item; {A|ITEM} the same at the start of a sentence; {cap|ITEM} the item with a capital first letter (sentence
start); {poss|REQUESTER} gives the name plus "'s". Never write "a {ITEM}" or "an {ITEM}": write {a|ITEM} or
"the {ITEM}". Write the text so it still reads naturally whatever item or name the program puts in (say nothing
else about the item, the person, the company or its industry).

Hard rules (a text that breaks one is thrown away by a checking program):
1. No digit, number word (one, first, second, half ...), date, clock time, timestamp, weekday, month, money amount,
   currency or percent sign, URL, e-mail address, or code of your own (letters mixed with digits).
2. Write every word in lowercase, including the first word right after the tag and the first word after a full stop:
   '[desk] hi, {REQUESTER} here ...', never '[desk] Hi, {REQUESTER} here ...'. A checking program reads a
   capitalised word after the tag as a person's name and throws the text away. The only capitals allowed are
   inside the placeholders and the acronyms RACI, UTC, IT, HR, VP, API, A. After a tag write {a|ITEM} or 'the {ITEM}', never
   {A|ITEM} or {cap|ITEM}. Avoid the pronoun I (write as a desk or in the third person). Write teams in lowercase
   ("the finance desk").
3. Never mention a record, role, approver, delegation, grant record, scope, permission, deadline, rule, decision,
   outcome or question, and never say or hint whether anything was signed off, cleared, permitted, refused or is
   still waiting. "approval" may only name the request type ("an approval request"); never use "grant" at all.
4. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, fail to, refuse to, decline to, hardly, barely, scarcely, few, except, unless, false, other than, free of, no longer, rule out, prevent ... from.
5. Never use these words (a program checks them): able, accept, accepted, active, additional, afternoon, afterwards, ago, all, allegedly, allow, allowed, almost, already, always, annually, another, any, anybody, anyone, anything, apparently, appear, appeared, appears, approve, approved, approximately, asap, assume, assumed, assumes, believe, billion, block, blocked, both, breached, broken, bulk, bunch, ca, can, cancel, canceled, cancelled, cannot, closed, complete, completed, compliant, confirm, confirmation, confirmed, could, couple, currently, daily, delivered, denial, denied, deny, done, double, dozen, dozens, each, earlier, eight, eighteen, eighth, eighty, either, eleven, eligibility, eligible, entire, entirely, entitled, evening, every, everybody, everyone, everything, except, excluding, expire, expired, extra, fail, failed, failure, fake, few, fewer, fewest, fifteen, fifth, fifty, finished, first, five, forbidden, formerly, forty, four, fourteen, fourth, fraud, fraudulent, genuine, gotta, granted, guess, half, handful, hourly, hundred, if, immediately, inactive, ineligible, instead, invalid, kept, last, late, lately, later, least, legitimate, less, likely, lots, majority, mandatory, many, maximum, may, maybe, midday, midnight, might, million, minimum, minority, monthly, more, morning, most, much, multiple, must, mustn, nearly, need, needed, needs, neither, never, next, night, nine, nineteen, ninety, ninth, no, nobody, noncompliant, none, noon, nothing, now, numerous, often, ok, okay, one, only, open, opened, optional, otherwise, ought, outstanding, overdue, overnight, paid, pair, partial, partially, past, pending, percent, percentage, perhaps, permitted, plenty, possibly, presumably, previously, probably, processed, prohibited, provided, providing, quarter, queued, rarely, recently, refund, refunded, regardless, reject, rejected, reportedly, required, resolved, revoke, revoked, roughly, second, seem, seemed, seemingly, seems, seldom, settled, seven, seventeen, seventh, seventy, several, shall, shortly, should, shouldn, single, six, sixteen, sixth, sixty, some, somebody, someone, something, sometimes, somewhat, soon, succeeded, success, successful, successfully, superseded, supposedly, suspect, ten, tenth, think, third, thirteen, thirty, thousand, three, thrice, today, tomorrow, tonight, total, triple, twelve, twenty, twice, two, unable, uncertain, unless, unlikely, unpaid, unresolved, unsure, unverified, upcoming, usually, valid, various, verified, void, waive, waived, weekend, weekly, whenever, whole, will, wo, would, yearly, yesterday, yet, zero.
6. Length 8-45 words (json and yaml: 3-7 keys).
7. Never write 'kind of' or 'sort of' (a checking program reads them as hedges).
8. Each item asks for a particular variation; follow it, and make every text in this task clearly different from the
   others (wording, structure, tone, where the placeholders sit).

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
text with its placeholders>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q3c3089b6af",
  "brief": "Variation: written by an assistant logging the request; put the item before the requester; very short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q17238657d8",
  "brief": "Variation: written by a front desk; two short sentences; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q749911b0ed",
  "brief": "Variation: written by a team lead passing it on; use 'the {ITEM}'; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q9059eaebe4",
  "brief": "Variation: written by a front desk; warm and chatty; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q4ebd8199fe",
  "brief": "Variation: written by the requester; polite and plain; short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q55b2842e2d",
  "brief": "Variation: written by the requester; polite and plain; on the longer side. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qc70ae2c1bd",
  "brief": "Variation: written by a front desk; two short sentences; very short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q7c682c83e3",
  "brief": "Variation: neutral, as a system would write it; use {a|ITEM}; very short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qbdff004e84",
  "brief": "Variation: neutral, as a system would write it; matter-of-fact; short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qc9a9cf622e",
  "brief": "Variation: written by an assistant logging the request; formal and brief; short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qd19e70b239",
  "brief": "Variation: written by a team lead passing it on; use 'the {ITEM}'; short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q3971eb3304",
  "brief": "Variation: written by the requester; use {poss|REQUESTER}; very short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qebbab0b818",
  "brief": "Variation: written by the requester; use {poss|REQUESTER}; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q4893674328",
  "brief": "Variation: written by a colleague forwarding the request; terse, almost telegraphic; short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q9ba2b4cbe2",
  "brief": "Variation: written by an assistant logging the request; formal and brief; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qa198f939e8",
  "brief": "Variation: written by a team lead passing it on; put the requester at the very start; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q1a64661907",
  "brief": "Variation: written by a colleague forwarding the request; terse, almost telegraphic; on the longer side. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q579f6cc825",
  "brief": "Variation: written by the requester; use {poss|REQUESTER}; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qe5f0d40c66",
  "brief": "Variation: written by a colleague forwarding the request; one sentence only; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qa69f6cf818",
  "brief": "Variation: written by a colleague forwarding the request; one sentence only; very short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q28dbf1027a",
  "brief": "Variation: neutral, as a system would write it; use {a|ITEM}; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q38c0d697b3",
  "brief": "Variation: neutral, as a system would write it; matter-of-fact; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qb486d782ab",
  "brief": "Variation: neutral, as a system would write it; matter-of-fact; on the longer side. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q8eefb0132a",
  "brief": "Variation: written by an assistant logging the request; put the item before the requester; medium length. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q708bdc4384",
  "brief": "Variation: written by a team lead passing it on; use 'the {ITEM}'; very short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qa506a50f3d",
  "brief": "Variation: written by a team lead passing it on; put the requester at the very start; on the longer side. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "qa07a5e5a21",
  "brief": "Variation: written by an assistant logging the request; put the item before the requester; on the longer side. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 },
 {
  "qid": "q780494a7c8",
  "brief": "Variation: written by a front desk; warm and chatty; short. The request asks for sign-off (an approval request) on something a company would spend money on or commit to, for example a supplier renewal, a server rack order or a conference trip.",
  "register": "log",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}",
   "every word after the tag in lowercase (capitals only inside placeholders)"
  ]
 }
]

Reminder: write one JSON array with exactly 28 objects ({"qid": "...", "text": "..."}) to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/answers/T31-author_skin-ea21749a-000.json and nothing else.
