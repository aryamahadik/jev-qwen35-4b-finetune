# T29 redo2 authoring task T29-author_freeform-d6896288-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/redo2/answers/T29-author_freeform-d6896288-001.json

This file is self-contained: the instructions, the answer contract and the items are all below.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 25 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: q2850ae56b0, q7022b8e0ae, qc0a06accf1, qf7e02ae485, q1f7960509a, q06f9bd0c16, q7668c7133c, qa4a3e1ef84, q70a97b2b46, qac6b13d706, q7be0455ace, q1a5cbfed6f, qf994112b47, q85ff44caed, q05fddcfae3, q3aa2463d99, q4264d44992, q32f08c1005, qa1321f41e9, q03be64ddcb, q1c75ac0998, q4ef6dd91af, qc9cc5a59f1, q679501fbec, q3f3ed1e7af.
- "text": one JSON string (the whole document).
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one; replace the angle brackets with your own text):
[{"qid": "q2850ae56b0", "text": "<the document>"}, ...]

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
  "qid": "q2850ae56b0",
  "brief": "a handoff at the change of shift",
  "register": "memo",
  "facts": {
   "REQUESTER": "Elias Strand",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q7022b8e0ae",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Sofia Lindgren",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qc0a06accf1",
  "brief": "a message that opens with a greeting",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ade Bankole",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qf7e02ae485",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Sara Novak",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q1f7960509a",
  "brief": "a request filed through an internal form",
  "register": "memo",
  "facts": {
   "REQUESTER": "Priya Velasco",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q06f9bd0c16",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Sara Novak",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q7668c7133c",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Sofia Lindgren",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qa4a3e1ef84",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Omar Haddad",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q70a97b2b46",
  "brief": "a structured note with labelled parts",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ravi Anand",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qac6b13d706",
  "brief": "a handoff at the change of shift",
  "register": "memo",
  "facts": {
   "REQUESTER": "Elias Strand",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q7be0455ace",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Sara Novak",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q1a5cbfed6f",
  "brief": "a request filed through an internal form",
  "register": "memo",
  "facts": {
   "REQUESTER": "Priya Velasco",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qf994112b47",
  "brief": "a message saying the request came out of a meeting",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Leo Marchetti",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q85ff44caed",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Yara Nasser",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q05fddcfae3",
  "brief": "a casual message with a light touch of humour",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Ken Watanabe",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q3aa2463d99",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q4264d44992",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Jonah Pike",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q32f08c1005",
  "brief": "a casual message with a light touch of humour",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Ken Watanabe",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qa1321f41e9",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Jonah Pike",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q03be64ddcb",
  "brief": "a casual message with a light touch of humour",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Tomas Ferreira",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q1c75ac0998",
  "brief": "a request in a neutral, impersonal tone",
  "register": "email",
  "facts": {
   "REQUESTER": "Bram Visser",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q4ef6dd91af",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Grace Achebe",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "qc9cc5a59f1",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Yara Nasser",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q679501fbec",
  "brief": "a handoff at the change of shift",
  "register": "memo",
  "facts": {
   "REQUESTER": "Elias Strand",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 },
 {
  "qid": "q3f3ed1e7af",
  "brief": "a note that thanks the agent",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Lucia Romano",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim",
   "request words only from the closed lists"
  ]
 }
]
