# T24 authoring task T24-author_skin-90de9359-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_skin-90de9359-000.json

Task kind: author_skin; items: 8; outputs expected: 40.

You are writing short pieces of text for a synthetic training dataset about everyday customer-service
policies (returns, repairs, bookings, deposits, fees and the like). Everything you write is either a reusable template
(a program later fills each {SLOT} placeholder with a value) or a set of invented values. Write natural, varied
English. Invent everything: never copy text from real companies, products, people, laws, websites or published
datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write NARRATIVE TEMPLATES in the register "json": a JSON object (one or several lines) with three to five snake_case keys; each placeholder is a bare JSON value with no quotes around it, e.g. "customer": {CUSTOMER}; at most one extra key whose value is a plain neutral word or short phrase in quotes (such as "topic": "request").
A narrative is a short message or note from or about the customer who raised a case under an invented
customer-service policy. Elsewhere on the page a program prints the policy and the case record; your text adds no
fact of its own and never hints at how the case will be decided.

Placeholders: each item lists the placeholders ("slots") to use and what the program puts in them. Use every listed
placeholder EXACTLY ONCE, spelled exactly as given with its curly braces (e.g. {CUSTOMER}); never use any other
placeholder and never write a real value in its place.

Hard rules (a text that breaks one is thrown away):
1. One block of text: no empty line, no leading or trailing spaces; line breaks only where the register needs them.
2. Never put "a" or "an" directly before a placeholder.
3. Outside the placeholders: no digits, number words or ordinals; no dates, times, months or weekdays; no currency
   or percent signs; no web or e-mail addresses; no codes or ids.
4. Outside the placeholders, none of these words (any letter case):
   - number: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
   - relative time: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
   - quantity: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
   - quantifier: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
   - modal: able, allowed, can, cannot, could, forbidden, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, would
   - hedge: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
   - status: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
   - operator: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
   - phrases: have to, has to, had to, got to, sort of, kind of
5. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, refuse to, prevent ... from, rule out.
6. Capital letters only at the start of a sentence, a line, a list item or a label; no names of people, companies,
   products, places or teams (the only name is the {CUSTOMER} placeholder).
7. Refer to the subject only as the case, the request, my case or my request. Say nothing about what was bought,
   used, booked or damaged; about dates, deadlines, amounts, categories or conditions (except through the
   placeholders); about the policy's rules or versions (never new, old, revised or updated rules); or about any
   result, any money paid back or what the customer hopes to get (asking to have the case looked at is fine).
8. Use each placeholder only in the role its description gives.
9. The texts of one item vary clearly in wording and structure (not one word swapped), and none copies the example.

Example of the register (for format only):
  "{\"case\": {CASE_ID}, \"customer\": {CUSTOMER}, \"topic\": \"request under the policy\"}"

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qdaefe1e053",
  "brief": "a terse note; write 5 texts",
  "register": "json",
  "slots": {
   "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
   "CASE_ID": "the case number, e.g. 'LUG-48213'",
   "COND": "the condition noted on the case, a short lower-case label, e.g. 'receipt kept'; use it only as a labelled value, as in 'condition: {COND}'"
  },
  "rules": [
   "use each of {CUSTOMER}, {CASE_ID}, {COND} exactly once",
   "5 texts, each clearly distinct from the others"
  ]
 },
 {
  "qid": "q9c396f6660",
  "brief": "a note written by a support agent after a call; write 5 texts",
  "register": "json",
  "slots": {
   "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
   "CASE_ID": "the case number, e.g. 'LUG-48213'",
   "CAT": "the category of the case, a short lower-case label, e.g. 'suitcases'; use it as a label, as in 'category: {CAT}' or 'the {CAT} category'"
  },
  "rules": [
   "use each of {CUSTOMER}, {CASE_ID}, {CAT} exactly once",
   "5 texts, each clearly distinct from the others"
  ]
 },
 {
  "qid": "q07e5c966ae",
  "brief": "a short, plain note; write 5 texts",
  "register": "json",
  "slots": {
   "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
   "CASE_ID": "the case number, e.g. 'LUG-48213'",
   "COND": "the condition noted on the case, a short lower-case label, e.g. 'receipt kept'; use it only as a labelled value, as in 'condition: {COND}'"
  },
  "rules": [
   "use each of {CUSTOMER}, {CASE_ID}, {COND} exactly once",
   "5 texts, each clearly distinct from the others"
  ]
 },
 {
  "qid": "qe645954570",
  "brief": "a friendly note with a thank-you; write 5 texts",
  "register": "json",
  "slots": {
   "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
   "CASE_ID": "the case number, e.g. 'LUG-48213'"
  },
  "rules": [
   "use each of {CUSTOMER}, {CASE_ID} exactly once",
   "5 texts, each clearly distinct from the others"
  ]
 },
 {
  "qid": "q894fa4fb80",
  "brief": "a message written in a hurry; write 5 texts",
  "register": "json",
  "slots": {
   "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
   "CASE_ID": "the case number, e.g. 'LUG-48213'",
   "AMOUNT": "the money amount of the case, e.g. '$1,250.00'; use it only as a labelled value, as in 'amount: {AMOUNT}'"
  },
  "rules": [
   "use each of {CUSTOMER}, {CASE_ID}, {AMOUNT} exactly once",
   "5 texts, each clearly distinct from the others"
  ]
 },
 {
  "qid": "q75ef06607a",
  "brief": "a formal request to have the case looked at; write 5 texts",
  "register": "json",
  "slots": {
   "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
   "CASE_ID": "the case number, e.g. 'LUG-48213'",
   "REQ": "the date the request was sent, e.g. '5 March 2026'; use it only as that date, as in 'sent on {REQ}' or 'request date: {REQ}'"
  },
  "rules": [
   "use each of {CUSTOMER}, {CASE_ID}, {REQ} exactly once",
   "5 texts, each clearly distinct from the others"
  ]
 },
 {
  "qid": "q2a3f7a7eef",
  "brief": "a message with a short greeting; write 5 texts",
  "register": "json",
  "slots": {
   "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
   "CASE_ID": "the case number, e.g. 'LUG-48213'",
   "AMOUNT": "the money amount of the case, e.g. '$1,250.00'; use it only as a labelled value, as in 'amount: {AMOUNT}'"
  },
  "rules": [
   "use each of {CUSTOMER}, {CASE_ID}, {AMOUNT} exactly once",
   "5 texts, each clearly distinct from the others"
  ]
 },
 {
  "qid": "q76a4365228",
  "brief": "a polite first message; write 5 texts",
  "register": "json",
  "slots": {
   "CUSTOMER": "the customer's full name, e.g. 'Jordan Vale'",
   "CASE_ID": "the case number, e.g. 'LUG-48213'",
   "CAT": "the category of the case, a short lower-case label, e.g. 'suitcases'; use it as a label, as in 'category: {CAT}' or 'the {CAT} category'"
  },
  "rules": [
   "use each of {CUSTOMER}, {CASE_ID}, {CAT} exactly once",
   "5 texts, each clearly distinct from the others"
  ]
 }
]
