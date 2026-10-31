# T20 authoring task T20-author_freeform-c32d065e-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/haiku/author/answers/T20-author_freeform-c32d065e-000.json

Task kind: author_freeform; items: 8; outputs expected: 16 (2 per item, answer field "texts").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You write short narrative notes for a synthetic dataset. Setting: an operations group runs online services and logs every incident. For each incident a program prints a short note from the person who reports it, then the incident record and a card of rules, then a question. The program fills every value. Everything you write must be invented: never copy text from real companies, products, people, websites or published datasets. Your note only says who reports the incident or writes the note, which on-call team gets it, and that the incident record follows. Each item gives two facts: REPORTER (a person's full name) and TEAM (the name of an on-call team). Write natural free text that uses both facts word for word and adds no fact of its own. Each item asks for 2 different notes in the answer field "texts"; a program checks every note and drops any that breaks a rule.

RULES (every item):
R1. Write the REPORTER value exactly as given (full name, same spelling and capitals) and the TEAM value exactly as given, each exactly once. Never write a part of a name alone (no first name or last name by itself), and no other name of a person, team, company, product or place. No curly braces.
R2. One block of text: no empty line, no leading or trailing spaces; 1-3 sentences or lines, at most 50 words.
R3. Say only who reports or writes, which team gets it, and that the incident record or details follow (below, attached, pasted, see the record). Add no fact of your own.
R4. No time at all: no digits, number words or ordinals, no clock times, dates, weekdays or months, and no time words (now, today, tonight, ago, soon, earlier, later, already, yet, still, recently, minutes, hours, this morning, overnight, before, after, until, since, when, while ...).
R5. Never mention what is affected or how badly (outage, slowness, broken, impact, users, data, exposure), any service or system name, and never these words, which name services in the record: payments, login, search, checkout, reports, email, storage, chat (say message, note or channel instead). Never mention an acknowledgement, a check, a maintenance window, a state (open, closed, resolved, fixed, ongoing ...), a level, rank or priority (high, low, top, worst ...), any word that judges how serious, pressing or important the incident is, passing it up to someone higher, or summoning someone by pager (write alert or notify instead).
R6. Outside the placeholders, none of these words (any letter case):
   - number: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
   - relative_time: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
   - quantity: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
   - quantifier: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
   - modal: able, allowed, can, cannot, could, forbidden, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, would
   - hedge: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
   - status: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
   - operator: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
   - also: ack, acked, acknowledge, acknowledged, acknowledgement, acknowledgment, affected, affecting, after, afternoon, again, already, am, asap, bad, before, big, breach, broken, chat, chats, check, checked, checking, checkout, checkouts, closed, cosmetic, daily, data, day, days, degradation, degraded, down, downtime, during, early, email, emails, emergency, escalation, escalations, evening, exposed, exposure, fast, fine, fixed, high, higher, highest, hour, hours, huge, immediately, impact, impacted, impacting, importance, important, investigating, just, late, leak, leaked, level, levels, login, logins, low, lower, lowest, maintenance, massive, midnight, minute, minutes, mitigated, monitoring, morning, night, noon, ok, okay, ongoing, open, opened, outage, outages, overnight, payment, payments, pm, priorities, priority, quick, quickly, rank, ranking, reopened, reports, resolved, restored, search, searches, serious, seriously, since, slow, slowness, small, still, storage, then, tier, timely, tiny, top, trivial, until, user, users, week, weekend, weekly, when, while, window, worse, worst, yet
R7. No negation at all: not, n't (don't, isn't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, fail, refuse, deny, unless, except.
R8. Capital letters only at the start of a sentence or a line, and in the REPORTER and TEAM values as given.
R9. Never start the note, or any line of it, with the word Incident.
R10. The 2 notes of an item differ clearly in wording and structure.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", "<answer field>": ...}. Copy each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner double quote as \" and a line break inside a text as \n); no comments, no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "texts": [...]}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q135725187a",
  "brief": "Write 2 different notes in the register 'customer_report'. Writer: the incident coordinator, routing the record; tone: plain and direct. Answer field: \"texts\" (a list of 2 strings).",
  "register": "customer_report",
  "facts": {
   "REPORTER": "Cormac Doyle",
   "TEAM": "Beacon rota"
  },
  "rules": [
   "Format: a support agent's note passing on a customer's report to a team (the customer is never named; never the word reports)",
   "Rules R1-R10 of the instructions apply."
  ]
 },
 {
  "qid": "q3662422576",
  "brief": "Write 2 different notes in the register 'exec_summary'. Writer: a colleague from a neighbouring team; tone: formal and polite. Answer field: \"texts\" (a list of 2 strings).",
  "register": "exec_summary",
  "facts": {
   "REPORTER": "Dalia Mansour",
   "TEAM": "Northwind guild"
  },
  "rules": [
   "Format: a short note for company leadership, written by one person on behalf of a team",
   "Rules R1-R10 of the instructions apply."
  ]
 },
 {
  "qid": "qdbc53337e7",
  "brief": "Write 2 different notes in the register 'exec_summary'. Writer: a support agent, forwarding the incident to the on-call team; tone: calm and neutral. Answer field: \"texts\" (a list of 2 strings).",
  "register": "exec_summary",
  "facts": {
   "REPORTER": "Hana Novak",
   "TEAM": "Riverbend crew"
  },
  "rules": [
   "Format: a short note for company leadership, written by one person on behalf of a team",
   "Rules R1-R10 of the instructions apply."
  ]
 },
 {
  "qid": "qbe72a06de4",
  "brief": "Write 2 different notes in the register 'customer_report'. Writer: an engineer handing the incident over to another team; tone: matter-of-fact. Answer field: \"texts\" (a list of 2 strings).",
  "register": "customer_report",
  "facts": {
   "REPORTER": "Gabriel Fontaine",
   "TEAM": "Meridian crew"
  },
  "rules": [
   "Format: a support agent's note passing on a customer's report to a team (the customer is never named; never the word reports)",
   "Rules R1-R10 of the instructions apply."
  ]
 },
 {
  "qid": "q7080c4161f",
  "brief": "Write 2 different notes in the register 'exec_summary'. Writer: a reliability engineer, filing the record for a team; tone: brisk and businesslike. Answer field: \"texts\" (a list of 2 strings).",
  "register": "exec_summary",
  "facts": {
   "REPORTER": "Beatriz Lima",
   "TEAM": "Tidewater guild"
  },
  "rules": [
   "Format: a short note for company leadership, written by one person on behalf of a team",
   "Rules R1-R10 of the instructions apply."
  ]
 },
 {
  "qid": "q95f1ce63e4",
  "brief": "Write 2 different notes in the register 'exec_summary'. Writer: a team lead, assigning the incident to a team; tone: terse, almost telegraphic. Answer field: \"texts\" (a list of 2 strings).",
  "register": "exec_summary",
  "facts": {
   "REPORTER": "Freya Holm",
   "TEAM": "Harbor squad"
  },
  "rules": [
   "Format: a short note for company leadership, written by one person on behalf of a team",
   "Rules R1-R10 of the instructions apply."
  ]
 },
 {
  "qid": "qf9a939b9ad",
  "brief": "Write 2 different notes in the register 'customer_report'. Writer: the person who noticed the incident, writing to the on-call team; tone: warm and friendly. Answer field: \"texts\" (a list of 2 strings).",
  "register": "customer_report",
  "facts": {
   "REPORTER": "Adebayo Ogun",
   "TEAM": "Orchard squad"
  },
  "rules": [
   "Format: a support agent's note passing on a customer's report to a team (the customer is never named; never the word reports)",
   "Rules R1-R10 of the instructions apply."
  ]
 },
 {
  "qid": "q5307ceaf73",
  "brief": "Write 2 different notes in the register 'customer_report'. Writer: a relay bot, passing on a person's report; tone: courteous and a little wordy. Answer field: \"texts\" (a list of 2 strings).",
  "register": "customer_report",
  "facts": {
   "REPORTER": "Emeka Nwosu",
   "TEAM": "Saffron unit"
  },
  "rules": [
   "Format: a support agent's note passing on a customer's report to a team (the customer is never named; never the word reports)",
   "Rules R1-R10 of the instructions apply."
  ]
 }
]
