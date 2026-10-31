# T12 authoring task T12-author_freeform-620403bd-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/author/answers/T12-author_freeform-620403bd-000.json

Task kind: author_freeform; items: 12; outputs expected: 24 (2 per item, answer field "texts").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You write short cover notes for a synthetic training dataset. Setting: in an accounts-payable (AP) team, a clerk matches a supplier's invoice against the purchase order (PO) and the goods receipt under a written company policy. A program builds every example: it prints the documents, the policy and the question, and it fills every value. Everything you write must be invented: never copy text from real companies, products, people, laws, websites or published datasets. In every example a note introduces three documents about one purchase: a purchase order, a goods receipt and a supplier invoice. The program prints the documents and the policy after your note. Each item gives two facts: CLERK (the full name of the AP clerk who writes or receives the note) and DEPT (the team the purchase is for). Write natural free text that uses both facts word for word and adds no fact of its own. Each item asks for 2 different notes in the answer field "texts"; a program checks every note and drops any that breaks a rule.

RULES (every item):
R1. Write the CLERK value exactly as given (full name, same spelling and capitals) and the DEPT value exactly as given, each once or twice. Never write a part of the name alone (no first name or family name by itself), and no other name of a person, team, company, product or place.
R2. One block of text: no empty line, no leading or trailing spaces; 1-4 sentences or lines, at most 60 words.
R3. Say only who the note is from or to, which team the purchase is for, and that the documents are attached, pasted below or forwarded for matching. Never say or hint whether anything is correct, matches, differs, is late, short, extra, cheap or expensive. Never ask anyone to do anything with the invoice or the payment (no paying, stopping, looking it over, checking, refusing, passing it up or signing it off), and no urgency.
R4. Outside the placeholders: no digits, no number words or ordinals, no dates, times, months or weekdays, no money or percent signs, no prices, amounts, quantities, totals, ids, e-mail or web addresses.
R5. Outside the placeholders, none of these words (any letter case):
   - number: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
   - relative_time: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
   - quantity: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
   - quantifier: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
   - modal: able, allowed, can, cannot, could, forbidden, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, would
   - hedge: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
   - status: accept, accepted, active, allow, allowed, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, eligible, entitled, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, ineligible, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
   - operator: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
   - also: amount, amounts, budget, cents, cheap, correct, cost, costs, critical, decline, declined, discrepancies, discrepancy, dollars, early, emergency, error, errors, euros, examine, expensive, fine, hurry, incorrect, inspect, issue, issues, late, mismatch, mismatched, missing, mistake, money, overcharged, pay, paying, payment, payments, pays, pounds, price, prices, priority, problem, problems, quantities, quantity, quickly, refuse, refused, right, rush, shortage, shortfall, sign, signed, stop, stopped, stops, suspicious, urgent, urgently, verify, wrong
R6. No negation at all: not, n't (don't, isn't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, fail, refuse, deny, unless, except.
R7. Capital letters only at the start of a sentence or a line, in the CLERK name, in the DEPT value as given, and in AP, ERP and PO.
R8. Never start the note, or any line of it, with the words Invoice, Purchase order, Goods receipt or Paid-invoice (those words start the program's document blocks); inside a sentence they are fine.
R9. The 2 notes of an item differ clearly in wording and structure.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", "<answer field>": ...}. Copy each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner double quote as \" and a line break inside a text as \n); no comments, no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "texts": [...]}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qe056350be7",
  "brief": "Write 2 different notes in the register 'voicemail'. Writer: an AP intern, writing to the AP clerk; tone: matter-of-fact. Answer field: \"texts\" (a list of 2 strings).",
  "register": "voicemail",
  "facts": {
   "CLERK": "Bastian Kruger",
   "DEPT": "IT support"
  },
  "rules": [
   "Format: a transcribed voicemail in spoken style: the caller says who they are and that the documents are on their way, with the small fillers of speech (hi, um, thanks), in one to three lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "qc3f5c8b476",
  "brief": "Write 2 different notes in the register 'portal'. Writer: a team lead, writing to the AP clerk; tone: formal and polite. Answer field: \"texts\" (a list of 2 strings).",
  "register": "portal",
  "facts": {
   "CLERK": "Ines Carvalho",
   "DEPT": "field service"
  },
  "rules": [
   "Format: a message posted in a supplier or procurement web portal: a short title line, then one or two sentences or 'Field: value' lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "q56092b507b",
  "brief": "Write 2 different notes in the register 'voicemail'. Writer: an office manager, writing to the AP clerk; tone: matter-of-fact. Answer field: \"texts\" (a list of 2 strings).",
  "register": "voicemail",
  "facts": {
   "CLERK": "Jonas Lindqvist",
   "DEPT": "facilities"
  },
  "rules": [
   "Format: a transcribed voicemail in spoken style: the caller says who they are and that the documents are on their way, with the small fillers of speech (hi, um, thanks), in one to three lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "q7ee9e9b52b",
  "brief": "Write 2 different notes in the register 'portal'. Writer: the AP clerk, writing to the AP lead; tone: plain and direct. Answer field: \"texts\" (a list of 2 strings).",
  "register": "portal",
  "facts": {
   "CLERK": "Chiara Benedetti",
   "DEPT": "field service"
  },
  "rules": [
   "Format: a message posted in a supplier or procurement web portal: a short title line, then one or two sentences or 'Field: value' lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "q4ef8dd78c2",
  "brief": "Write 2 different notes in the register 'voicemail'. Writer: a team assistant, writing to the AP clerk; tone: brief, almost telegraphic. Answer field: \"texts\" (a list of 2 strings).",
  "register": "voicemail",
  "facts": {
   "CLERK": "Dmitri Volkov",
   "DEPT": "facilities"
  },
  "rules": [
   "Format: a transcribed voicemail in spoken style: the caller says who they are and that the documents are on their way, with the small fillers of speech (hi, um, thanks), in one to three lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "q7c48eaecd9",
  "brief": "Write 2 different notes in the register 'portal'. Writer: the AP clerk, writing to the team that made the purchase; tone: plain and direct. Answer field: \"texts\" (a list of 2 strings).",
  "register": "portal",
  "facts": {
   "CLERK": "Kavya Reddy",
   "DEPT": "warehouse"
  },
  "rules": [
   "Format: a message posted in a supplier or procurement web portal: a short title line, then one or two sentences or 'Field: value' lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "q43e7dd911f",
  "brief": "Write 2 different notes in the register 'portal'. Writer: the AP clerk, writing to the team that made the purchase; tone: formal and polite. Answer field: \"texts\" (a list of 2 strings).",
  "register": "portal",
  "facts": {
   "CLERK": "Amara Okonkwo",
   "DEPT": "laboratory"
  },
  "rules": [
   "Format: a message posted in a supplier or procurement web portal: a short title line, then one or two sentences or 'Field: value' lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "q35e8a4e285",
  "brief": "Write 2 different notes in the register 'portal'. Writer: a receiving-dock worker, writing to the AP clerk; tone: chatty but on topic. Answer field: \"texts\" (a list of 2 strings).",
  "register": "portal",
  "facts": {
   "CLERK": "Goran Petrovic",
   "DEPT": "laboratory"
  },
  "rules": [
   "Format: a message posted in a supplier or procurement web portal: a short title line, then one or two sentences or 'Field: value' lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "qc20817defe",
  "brief": "Write 2 different notes in the register 'portal'. Writer: a supplier's billing contact, writing to the AP clerk; tone: courteous and a little wordy. Answer field: \"texts\" (a list of 2 strings).",
  "register": "portal",
  "facts": {
   "CLERK": "Elif Yilmaz",
   "DEPT": "warehouse"
  },
  "rules": [
   "Format: a message posted in a supplier or procurement web portal: a short title line, then one or two sentences or 'Field: value' lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "q290153b5e7",
  "brief": "Write 2 different notes in the register 'voicemail'. Writer: the AP clerk, writing a note to file; tone: crisp and businesslike. Answer field: \"texts\" (a list of 2 strings).",
  "register": "voicemail",
  "facts": {
   "CLERK": "Hiroshi Tanaka",
   "DEPT": "IT support"
  },
  "rules": [
   "Format: a transcribed voicemail in spoken style: the caller says who they are and that the documents are on their way, with the small fillers of speech (hi, um, thanks), in one to three lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "qda5e6bf386",
  "brief": "Write 2 different notes in the register 'voicemail'. Writer: a procurement officer, writing to the AP clerk; tone: warm and friendly. Answer field: \"texts\" (a list of 2 strings).",
  "register": "voicemail",
  "facts": {
   "CLERK": "Farah Haddad",
   "DEPT": "marketing"
  },
  "rules": [
   "Format: a transcribed voicemail in spoken style: the caller says who they are and that the documents are on their way, with the small fillers of speech (hi, um, thanks), in one to three lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 },
 {
  "qid": "q75a6cad265",
  "brief": "Write 2 different notes in the register 'voicemail'. Writer: an AP intern, writing to the AP clerk; tone: brief, almost telegraphic. Answer field: \"texts\" (a list of 2 strings).",
  "register": "voicemail",
  "facts": {
   "CLERK": "Luca Moretti",
   "DEPT": "marketing"
  },
  "rules": [
   "Format: a transcribed voicemail in spoken style: the caller says who they are and that the documents are on their way, with the small fillers of speech (hi, um, thanks), in one to three lines.",
   "Rules R1-R9 of the instructions apply."
  ]
 }
]
