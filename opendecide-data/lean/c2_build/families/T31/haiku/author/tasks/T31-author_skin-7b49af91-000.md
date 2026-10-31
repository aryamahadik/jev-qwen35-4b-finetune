# T31 authoring task T31-author_skin-7b49af91-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_skin-7b49af91-000.json

Task kind: author_skin; items: 36; answers expected: 36 (one per item, each with its qid).

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write NARRATIVE SKINS in the register "yaml" (a YAML block in block style only (never {...} flow style): lowercase keys; every placeholder is a whole value (requester: {REQUESTER}) or sits inside a sentence value; 3-7 keys, nesting allowed; no lists of numbers and no yes / no / true / false values).
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
  "qid": "q88fa9fa4cd",
  "brief": "Variation: written by a team lead passing it on; a note value written as a sentence; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q0d2dd10ac5",
  "brief": "Variation: written by the requester; keys named like a form (submitted_by, subject, reference); on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q0a1f897d96",
  "brief": "Variation: written by a front desk; a note value written as a sentence; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q767a7cce70",
  "brief": "Variation: written by a colleague forwarding the request; plain field names; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qc7abc105d7",
  "brief": "Variation: written by an assistant logging the request; a short summary sentence as one value; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q19125744b2",
  "brief": "Variation: written by an assistant logging the request; keys named after the case (case, raised_by, about); medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q072a0d680a",
  "brief": "Variation: written by a colleague forwarding the request; keys named after the case (case, raised_by, about); on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qfbb48f60f9",
  "brief": "Variation: neutral, as a system would write it; plain field names; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q7570f927e1",
  "brief": "Variation: written by a front desk; intake-style field names; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qa15f5c1119",
  "brief": "Variation: neutral, as a system would write it; flat, three or four keys; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q245b4b0b74",
  "brief": "Variation: written by a colleague forwarding the request; a short summary sentence as one value; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q9420b8ccc7",
  "brief": "Variation: written by a colleague forwarding the request; flat, three or four keys; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q170763caa6",
  "brief": "Variation: neutral, as a system would write it; a short summary sentence as one value; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qa7385397e3",
  "brief": "Variation: written by the requester; keys named like a form (submitted_by, subject, reference); very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qa347499ff6",
  "brief": "Variation: written by a team lead passing it on; a note value written as a sentence; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qc4647152cd",
  "brief": "Variation: written by a front desk; one nested object; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q6a808b38b1",
  "brief": "Variation: written by a colleague forwarding the request; plain field names; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qfceb140d81",
  "brief": "Variation: written by an assistant logging the request; plain field names; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q328fee3d64",
  "brief": "Variation: written by an assistant logging the request; flat, three or four keys; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qd16948df79",
  "brief": "Variation: written by an assistant logging the request; keys named after the case (case, raised_by, about); medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qd34a574f8d",
  "brief": "Variation: written by a front desk; keys named like a form (submitted_by, subject, reference); medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qcb1bd360e5",
  "brief": "Variation: written by a colleague forwarding the request; flat, three or four keys; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qf6d512f6d6",
  "brief": "Variation: written by a team lead passing it on; one nested object; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qa921e6422f",
  "brief": "Variation: neutral, as a system would write it; keys named after the case (case, raised_by, about); short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q6da22b5ed9",
  "brief": "Variation: written by a team lead passing it on; keys named like a form (submitted_by, subject, reference); short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qc4a6097537",
  "brief": "Variation: written by an assistant logging the request; flat, three or four keys; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qcf2ffa16c1",
  "brief": "Variation: written by the requester; one nested object; very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q4428fa76e5",
  "brief": "Variation: neutral, as a system would write it; keys named after the case (case, raised_by, about); very short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qadc5581521",
  "brief": "Variation: written by the requester; one nested object; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q835d894280",
  "brief": "Variation: written by a front desk; a note value written as a sentence; short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qa6681e138b",
  "brief": "Variation: written by the requester; intake-style field names; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q21b96424df",
  "brief": "Variation: neutral, as a system would write it; a short summary sentence as one value; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q1d520e7e6d",
  "brief": "Variation: written by the requester; a note value written as a sentence; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "qbbe0a7274f",
  "brief": "Variation: written by a team lead passing it on; intake-style field names; medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q8b5dbfe57f",
  "brief": "Variation: written by a team lead passing it on; intake-style field names; on the longer side. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
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
  "qid": "q47d051f5c8",
  "brief": "Variation: written by a front desk; keys named like a form (submitted_by, subject, reference); medium length. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "yaml",
  "slots": {
   "REQUESTER": "required, exactly once",
   "ITEM": "required, exactly once",
   "REQ_ID": "leave it out"
  },
  "rules": [
   "do not use {REQ_ID}"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_skin-7b49af91-000.json and nothing else.
