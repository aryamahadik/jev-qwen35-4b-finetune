# T29 authoring task T29-author_skin-f4385b7d-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_skin-f4385b7d-000.json

Task kind: author_skin; items: 8; outputs expected: 48.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write NARRATIVE TEMPLATES in the register "runbook": an excerpt of a runbook page: a page or step heading line and one or two lines describing the step the agent performs and who maintains the page.
A narrative only says who wants the agent to make a tool call and for what piece of work. Elsewhere on the page a
program prints the call, a data snapshot and a policy; your text must add no fact of its own.

Placeholders: each item lists the placeholders ("slots") to use. Use every listed placeholder EXACTLY ONCE, spelled
exactly as given with its curly braces (e.g. {REQUESTER}), never inside quotes unless the register shows it, and
never use any other placeholder or write a real value in its place.

Hard rules (a text that breaks one is thrown away):
1. One block of text: no empty line, no leading or trailing spaces; line breaks only where the register needs them.
2. Never put "a" or "an" directly before a placeholder.
3. Outside the placeholders: no digits, no number words or ordinals, no dates, times, months or weekdays, no
   currency or percent signs, no web addresses, e-mail addresses or domains, no codes that mix letters and digits.
4. Outside the placeholders, none of these words (any letter case):
- number: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
- relative time: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
- quantity: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
- quantifier: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
- modal: able, allowed, can, cannot, could, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, prohibited, required, shall, should, shouldn, unable, will, would
- hedge: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
- status: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
- operator: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
- phrases: have to, has to, had to, got to, sort of, kind of
5. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
6. Capital letters only at the start of a sentence, a line, a list item or a label; the only other capitalised words
   allowed are Agent and User. No names of people, teams, companies, products, places or departments.
7. Say nothing about records, amounts of money, destinations, teams, environments, kinds of data, timing, risk,
   reversibility or what the call will change. Never approve, sign off, agree to, judge or rank the call, and never
   mention a policy, a rule, a check or the user's consent.
8. To describe the request, use verbs such as: requested, wants, lined up, put in, filed, raised, sent over, handed
   over, passed along, is after.
9. The texts of one item must differ clearly in wording and structure (not one word swapped), and differ from the
   example. Do not copy the example.

Example of the register (for format only):
  "Runbook page maintained by {REQUESTER}. Step for {REASON}: the agent runs {ACTION} on {TARGET}."
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q347de32db1",
  "brief": "a handoff at the change of shift; write 6 different texts",
  "register": "runbook",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
   "REASON": "the piece of work the request belongs to, a short noun phrase such as 'audit preparation', 'quarterly cleanup', 'month-end close', 'incident follow-up'",
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "use each of {REQUESTER}, {REASON}, {ACTION}, {TARGET} exactly once",
   "6 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q774423f945",
  "brief": "a terse request from a busy lead; write 6 different texts",
  "register": "runbook",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
   "REASON": "the piece of work the request belongs to, a short noun phrase such as 'audit preparation', 'quarterly cleanup', 'month-end close', 'incident follow-up'",
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "use each of {REQUESTER}, {REASON}, {ACTION}, {TARGET} exactly once",
   "6 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q328ea872ae",
  "brief": "a short reminder-style message; write 6 different texts",
  "register": "runbook",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
   "REASON": "the piece of work the request belongs to, a short noun phrase such as 'audit preparation', 'quarterly cleanup', 'month-end close', 'incident follow-up'"
  },
  "rules": [
   "use each of {REQUESTER}, {REASON} exactly once",
   "6 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "qf8c268b36c",
  "brief": "a friendly message to the agent; write 6 different texts",
  "register": "runbook",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
   "REASON": "the piece of work the request belongs to, a short noun phrase such as 'audit preparation', 'quarterly cleanup', 'month-end close', 'incident follow-up'",
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'"
  },
  "rules": [
   "use each of {REQUESTER}, {REASON}, {ACTION} exactly once",
   "6 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "qe0c6e310b1",
  "brief": "a request relayed from a planning session; write 6 different texts",
  "register": "runbook",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
   "REASON": "the piece of work the request belongs to, a short noun phrase such as 'audit preparation', 'quarterly cleanup', 'month-end close', 'incident follow-up'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "use each of {REQUESTER}, {REASON}, {TARGET} exactly once",
   "6 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q7fbb197165",
  "brief": "a request written for a shared work queue; write 6 different texts",
  "register": "runbook",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
   "REASON": "the piece of work the request belongs to, a short noun phrase such as 'audit preparation', 'quarterly cleanup', 'month-end close', 'incident follow-up'",
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "use each of {REQUESTER}, {REASON}, {ACTION}, {TARGET} exactly once",
   "6 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q3e176c39ff",
  "brief": "a polite, formal request; write 6 different texts",
  "register": "runbook",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
   "REASON": "the piece of work the request belongs to, a short noun phrase such as 'audit preparation', 'quarterly cleanup', 'month-end close', 'incident follow-up'",
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'"
  },
  "rules": [
   "use each of {REQUESTER}, {REASON}, {ACTION} exactly once",
   "6 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q2f51735b98",
  "brief": "a hurried note written between meetings; write 6 different texts",
  "register": "runbook",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)",
   "REASON": "the piece of work the request belongs to, a short noun phrase such as 'audit preparation', 'quarterly cleanup', 'month-end close', 'incident follow-up'",
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "use each of {REQUESTER}, {REASON}, {ACTION}, {TARGET} exactly once",
   "6 texts, each clearly different from the others"
  ]
 }
]
