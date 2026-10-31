# T29 redo2 authoring task T29-author_freeform-d6896288-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/redo2/answers/T29-author_freeform-d6896288-000.json

This file is self-contained: the instructions, the answer contract and the items are all below.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 25 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: q8446d07060, q5e41776620, q223d5a6d2e, qa4063bbcb0, q354e58df42, qc9c1630bc4, qac047e002e, qdba29a534d, q9555663a9d, q71e0d40b91, q7caec19822, qce0da5bd03, qf32ae6beea, q6c64b91e6e, q1362ff521b, q2cf1c80e4c, q1b8dfa669a, qecc7fa8b4a, q00f4feca35, q25f802ff9c, qd6eab526fe, qbb2c9e8c2f, qef19b7b2fb, q40b40a41f8, q27f090d289.
- "text": one JSON string (the whole document).
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one; replace the angle brackets with your own text):
[{"qid": "q8446d07060", "text": "<the document>"}, ...]

Task kind: author_freeform; items: 25; outputs expected: 25.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write one short FREE-FORM DOCUMENT per item, in the item's register, from the facts given. The document is the
narrative part of a page: it says who wants the agent to make a tool call and for which piece of work. A program
prints the call, a data snapshot and a policy elsewhere, so the document adds no fact of its own.

Request words (closed lists; a program checks every word, and a document that uses another word for these is thrown
away):
- Say what the person wants ONLY with these words: wants, requested, requests, is requesting, has requested, put in a request, filed a request, raised a request, sent over a request, passed along a request, handed over a request, lined up, is after.
- Name what the agent does ONLY as: make the call, run the call, carry out the call, handle the call, take care of the call (you may say "the tool call" or "the requested call" instead of "the call").
- Use no other verb for making a request, for putting a question, or for moving forward with the call. Never tell
  the agent to act ("just run it", "please make the call"): the document only reports what the person wants.

Hard rules (a document that breaks one is thrown away):
1. Two to four sentences, 30-90 words, one block of text (single line breaks allowed, never an empty line).
2. Write the REQUESTER's full name exactly as given (same letters and capitals), exactly once, and no other personal
   names, initials, nicknames or shortened forms. Use no gendered pronouns (he, she, his, her, him); use the name once
   and "they" or no pronoun after that.
3. Write the REASON phrase exactly as given (same letters, lowercase), exactly once. Treat it as the label of a piece
   of work and describe it no further, so the text would still read well if another work label replaced it.
4. No digits, number words or ordinals; no dates, times, months or weekdays; no codes or ids; no web or e-mail
   addresses or domains; no currency or percent signs.
5. Outside the name and the reason phrase, none of these words (any letter case):
- number: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
- relative time: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
- quantity: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
- quantifier: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
- modal: able, allowed, can, cannot, could, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, prohibited, required, shall, should, shouldn, unable, will, would
- hedge: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
- status: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
- operator: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
- phrases: have to, has to, had to, got to, sort of, kind of
6. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
7. Never approve, sign off, agree to, judge or rank the call; never mention a policy, a rule, a check or consent; say
   nothing about records, amounts, destinations, teams, environments, kinds of data, timing or risk.
8. Capital letters only at the start of a sentence or line, plus the requester's name and the words Agent and User.
9. The documents of your answer differ clearly from each other in wording and structure.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "text": "<the document>"}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q8446d07060",
  "brief": "a request in a neutral, impersonal tone",
  "register": "email",
  "facts": {
   "REQUESTER": "Hana Sato",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q5e41776620",
  "brief": "a structured note with labelled parts",
  "register": "chat",
  "facts": {
   "REQUESTER": "Felix Huber",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q223d5a6d2e",
  "brief": "a structured note with labelled parts",
  "register": "chat",
  "facts": {
   "REQUESTER": "Felix Huber",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qa4063bbcb0",
  "brief": "a message that opens with a greeting",
  "register": "chat",
  "facts": {
   "REQUESTER": "Maya Lindqvist",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q354e58df42",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Grace Achebe",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qc9c1630bc4",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Rosa Alvarez",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qac047e002e",
  "brief": "a hurried note written between meetings",
  "register": "email",
  "facts": {
   "REQUESTER": "Dana Okafor",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qdba29a534d",
  "brief": "a hurried note written between meetings",
  "register": "email",
  "facts": {
   "REQUESTER": "Theo Grant",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q9555663a9d",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q71e0d40b91",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Lena Whitcombe",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q7caec19822",
  "brief": "a request filed through an internal form",
  "register": "memo",
  "facts": {
   "REQUESTER": "Nikolai Petrov",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qce0da5bd03",
  "brief": "a structured note with labelled parts",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ravi Anand",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qf32ae6beea",
  "brief": "a note that thanks the agent",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Lucia Romano",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q6c64b91e6e",
  "brief": "a hurried note written between meetings",
  "register": "email",
  "facts": {
   "REQUESTER": "Theo Grant",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q1362ff521b",
  "brief": "a note that thanks the agent",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Mateo Ruiz",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q2cf1c80e4c",
  "brief": "a request in a neutral, impersonal tone",
  "register": "email",
  "facts": {
   "REQUESTER": "Hana Sato",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q1b8dfa669a",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Rosa Alvarez",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qecc7fa8b4a",
  "brief": "a message that opens with a greeting",
  "register": "chat",
  "facts": {
   "REQUESTER": "Maya Lindqvist",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q00f4feca35",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Omar Haddad",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q25f802ff9c",
  "brief": "a friendly message to the agent",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Amara Diallo",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qd6eab526fe",
  "brief": "a friendly message to the agent",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Mira Castell",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qbb2c9e8c2f",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Aiko Brandt",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qef19b7b2fb",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Aiko Brandt",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q40b40a41f8",
  "brief": "a note that thanks the agent",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Lucia Romano",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q27f090d289",
  "brief": "a friendly message to the agent",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Amara Diallo",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 }
]
