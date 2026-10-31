# T31 authoring task T31-author_skin-fd5950e2-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_skin-fd5950e2-000.json

Task kind: author_skin; items: 25; answers expected: 25 (one per item, each with its qid).

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write NARRATIVE SKINS in the register "memo" (an internal memo: a short heading line (for example 'Internal memo' or 'Memo to the sign-off desk'), then one to three sentences).
A program later puts a block of records and a question after your text; you never see them. Your text only says who
raised which request. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.

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
2. No name or capitalised word except at the start of a line or sentence, a speaker label at the start of a line,
   and the acronyms RACI, UTC, IT, HR, VP, API, A. Write teams in lowercase ("the finance desk").
3. Never mention a record, role, approver, delegation, grant record, scope, permission, deadline, rule, decision,
   outcome or question, and never say or hint whether anything was signed off, cleared, permitted, refused or is
   still waiting. "approval" may only name the request type ("an approval request"); never use "grant" at all.
4. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, fail to, refuse to, decline to, hardly, barely, scarcely, few, except, unless, false, other than, free of, no longer, rule out, prevent ... from.
5. Never use these words (a program checks them): able, accept, accepted, active, additional, afternoon, afterwards, ago, all, allegedly, allow, allowed, almost, already, always, annually, another, any, anybody, anyone, anything, apparently, appear, appeared, appears, approve, approved, approximately, asap, assume, assumed, assumes, believe, billion, block, blocked, both, breached, broken, bulk, bunch, ca, can, cancel, canceled, cancelled, cannot, closed, complete, completed, compliant, confirm, confirmation, confirmed, could, couple, currently, daily, delivered, denial, denied, deny, done, double, dozen, dozens, each, earlier, eight, eighteen, eighth, eighty, either, eleven, eligibility, eligible, entire, entirely, entitled, evening, every, everybody, everyone, everything, except, excluding, expire, expired, extra, fail, failed, failure, fake, few, fewer, fewest, fifteen, fifth, fifty, finished, first, five, forbidden, formerly, forty, four, fourteen, fourth, fraud, fraudulent, genuine, gotta, granted, guess, half, handful, hourly, hundred, if, immediately, inactive, ineligible, instead, invalid, kept, last, late, lately, later, least, legitimate, less, likely, lots, majority, mandatory, many, maximum, may, maybe, midday, midnight, might, million, minimum, minority, monthly, more, morning, most, much, multiple, must, mustn, nearly, need, needed, needs, neither, never, next, night, nine, nineteen, ninety, ninth, no, nobody, noncompliant, none, noon, nothing, now, numerous, often, ok, okay, one, only, open, opened, optional, otherwise, ought, outstanding, overdue, overnight, paid, pair, partial, partially, past, pending, percent, percentage, perhaps, permitted, plenty, possibly, presumably, previously, probably, processed, prohibited, provided, providing, quarter, queued, rarely, recently, refund, refunded, regardless, reject, rejected, reportedly, required, resolved, revoke, revoked, roughly, second, seem, seemed, seemingly, seems, seldom, settled, seven, seventeen, seventh, seventy, several, shall, shortly, should, shouldn, single, six, sixteen, sixth, sixty, some, somebody, someone, something, sometimes, somewhat, soon, succeeded, success, successful, successfully, superseded, supposedly, suspect, ten, tenth, think, third, thirteen, thirty, thousand, three, thrice, today, tomorrow, tonight, total, triple, twelve, twenty, twice, two, unable, uncertain, unless, unlikely, unpaid, unresolved, unsure, unverified, upcoming, usually, valid, various, verified, void, waive, waived, weekend, weekly, whenever, whole, will, wo, would, yearly, yesterday, yet, zero.
6. Length 8-45 words (json and yaml: 3-7 keys).
7. Each item asks for a particular variation; follow it, and make every text in this task clearly different from the
   others (wording, structure, tone, where the placeholders sit).

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
text with its placeholders>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q32495582bb",
  "brief": "Variation: written by a colleague forwarding the request; polite and plain; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "q048b648835",
  "brief": "Variation: written by a front desk; one sentence only; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "qd80e93fc84",
  "brief": "Variation: written by a team lead passing it on; use {poss|REQUESTER}; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "qa0146ecaec",
  "brief": "Variation: written by the requester; put the item before the requester; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "qcc46064f3b",
  "brief": "Variation: written by the requester; terse, almost telegraphic; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "q5d1c456dc2",
  "brief": "Variation: neutral, as a system would write it; put the item before the requester; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "q0ef170f398",
  "brief": "Variation: written by a colleague forwarding the request; start a sentence with {A|ITEM} or {cap|ITEM}; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "q8738f9b9df",
  "brief": "Variation: neutral, as a system would write it; warm and chatty; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "q2057067199",
  "brief": "Variation: written by an assistant logging the request; matter-of-fact; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "qfbbf9afa6c",
  "brief": "Variation: written by an assistant logging the request; put the requester at the very start; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "q1da93539a4",
  "brief": "Variation: written by the requester; polite and plain; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "qb332acdbce",
  "brief": "Variation: neutral, as a system would write it; terse, almost telegraphic; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "q3b638ffc8b",
  "brief": "Variation: written by a front desk; formal and brief; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "q0d8b918b5c",
  "brief": "Variation: written by a team lead passing it on; warm and chatty; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "q1dea8a5d8d",
  "brief": "Variation: written by a team lead passing it on; use {a|ITEM}; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "qd7c9bdf6bd",
  "brief": "Variation: written by a colleague forwarding the request; one sentence only; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "q90100d1ea4",
  "brief": "Variation: written by a front desk; matter-of-fact; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "qc8551515c9",
  "brief": "Variation: written by a front desk; start a sentence with {A|ITEM} or {cap|ITEM}; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "q802606514d",
  "brief": "Variation: written by an assistant logging the request; use {poss|REQUESTER}; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "q5fbe90bfeb",
  "brief": "Variation: neutral, as a system would write it; use {a|ITEM}; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "q5cad06fb00",
  "brief": "Variation: written by an assistant logging the request; formal and brief; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "q19e50af329",
  "brief": "Variation: written by a colleague forwarding the request; two short sentences; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "qa7998917d2",
  "brief": "Variation: written by the requester; use 'the {ITEM}'; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 },
 {
  "qid": "qe940a6dd98",
  "brief": "Variation: written by the requester; two short sentences; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 },
 {
  "qid": "q9d8e8b0b39",
  "brief": "Variation: written by a team lead passing it on; put the requester at the very start; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "required, exactly once"
  },
  "rules": [
   "use {REQ_ID} exactly once"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_skin-fd5950e2-000.json and nothing else.
