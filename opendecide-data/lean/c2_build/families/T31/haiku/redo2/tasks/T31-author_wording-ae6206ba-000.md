# T31 TOP-UP authoring task T31-author_wording-ae6206ba-000 (kind: author_wording; 11 items)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/answers/T31-author_wording-ae6206ba-000.json

WHY THIS TASK EXISTS: new items for the T31 pool (yn_holder_other brief names 'other than' only (NEG_COUNTS (0, 1)); wording pool toward about 170). Every item is new; answer all 11.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 11 objects, one per item at the bottom of this file.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character. A qid is the letter q followed by ten letters or digits
  (11 characters in all). Every qid below appears exactly once in your answer; never invent or shorten one.
- "text": your text as one JSON string (a line break inside it as \n, a double quote as \").
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
- The 11 qids of this task: qdf05183856, q79acfaeff2, q4f37c0c301, qe0f30348cd, q75dc77e9a1, q2e2c768f40, q0b41601d5a, q4efd872bd5, q21b2c20eb9, qc8c50af66b, qf46a4cde9e
Literal example of the shape (your own text in "text"):
[{"qid": "qdf05183856", "text": "..."}, ...]

Task kind: author_wording; items: 11; answers expected: 11 (one per item, each with its qid).

FULL INSTRUCTIONS:

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS about the accountable (A) role for a sign-off request (who is the approver). A program shows a rule card and a block of records, then asks one
question in your wording. Each item states exactly what the question must mean; write one wording per item, and make
the wordings in this task clearly different from each other.

Placeholders (plain, exactly as written; no grammar helpers inside questions):
  {CANDIDATE}  a person's full name        {REQ_AGENT}  an agent id such as ledger-bot
  {REQ_SCOPE}  a scope id such as invoices.send   {REQ_ID}  the request's reference code
Use each placeholder the item requires exactly once; use {REQ_ID} only where the item allows it (at most once);
use no other placeholder.

Hard rules (a wording that breaks one is thrown away):
1. One question, 6-30 words, ending with "?".
2. Keep the meaning exactly as the item states it: same person, agent or scope, the time of the request, no
   widening, narrowing or softening.
3. Sign-off questions call the role "the accountable (A) role", "the A role" or "the accountable approver"; never
   "responsible", "owner", "manager" or "in charge" (those name other things).
4. Agent questions are about permission at the time of the request (whether the agent may use the scope then),
   never about whether the agent's grant lists the scope.
5. Time: "at the time of the request", "when the request was made", "at that moment", or no time phrase. Never now,
   currently, today, still, already, yet, at present.
6. Negation only where the item asks for it, and then exactly as the item says. Everywhere else none of: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, fail to, refuse to, decline to, hardly, barely, scarcely, few, except, unless, false, other than, free of, no longer, rule out, prevent ... from.
7. No digits, number words, dates, names or capital letters (except the first word and the placeholders); no hedges
   (maybe, probably, seems, likely). Never list answer choices; never mention any other person, agent or scope.
8. A checking program also rejects these words in a question: afternoon, afterwards, ago, allegedly, almost, already, annually, apparently, appear, appeared, appears, approximately, asap, assume, assumed, assumes, believe, billion, currently, daily, dozen, dozens, earlier, eight, eighteen, eighth, eighty, eleven, evening, fifteen, fifth, fifty, first, five, formerly, forty, four, fourteen, fourth, guess, half, hourly, hundred, immediately, last, lately, later, likely, maybe, midday, midnight, million, monthly, morning, nearly, next, night, nine, nineteen, ninety, ninth, noon, now, one, overdue, overnight, past, perhaps, possibly, presumably, previously, probably, recently, reportedly, roughly, second, seem, seemed, seemingly, seems, seven, seventeen, seventh, seventy, shortly, six, sixteen, sixth, sixty, somewhat, soon, supposedly, suspect, ten, tenth, think, third, thirteen, thirty, thousand, three, thrice, today, tomorrow, tonight, twelve, twenty, twice, two, uncertain, unlikely, unsure, upcoming, weekend, weekly, yearly, yesterday, yet, zero; any month or weekday name (so never start with 'May'); 'kind of' and 'sort of'.
9. Wordings that already exist are listed below. Never repeat one of them word for word; write wordings that differ from them in structure and word choice, with the same meaning.
EXISTING WORDINGS (do not repeat):
  Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made.
    - According to the records, was {CANDIDATE} in the accountable approver post at the time of the request?
    - At that moment, going by these records, did {CANDIDATE} hold the accountable approver role?
    - At that moment, is {CANDIDATE} the accountable approver for the request?
    - Audit item: when the request was made, did {CANDIDATE} hold the accountable approver role?
    - Based on the records above, was {CANDIDATE} the accountable approver when the request was made?
    - Checking the audit checklist, does {CANDIDATE} hold the accountable approver role at the time of the request?
    - Did {CANDIDATE} hold the accountable approver role at the time of the request?
    - Did {CANDIDATE} hold the accountable approver role for request {REQ_ID} when the request was made?
    - Does the accountable approver field for the request resolve to {CANDIDATE} at that moment?
    - Does {CANDIDATE} occupy the accountable approver slot for request {REQ_ID} at the time of the request?
    - For the audit file, is it confirmed that {CANDIDATE} was the accountable approver at the time of the request?
    - Is {CANDIDATE} the accountable approver at the time of the request?
    - Just checking, did {CANDIDATE} have the accountable approver role at that moment?
    - Just checking, was {CANDIDATE} the accountable approver when the request was made?
    - On request {REQ_ID}, does the accountable approver assignment name {CANDIDATE} at the time of the request?
    - Per the records, was {CANDIDATE} holding the accountable approver role at the time of the request?
    - Per the records, was {CANDIDATE} sitting in the accountable approver seat for request {REQ_ID} when the request was made?
    - Was the accountable approver role for request {REQ_ID} held by {CANDIDATE} when the request was made?
    - Was the accountable approver role, at the time of the request, held by {CANDIDATE}?
    - Was {CANDIDATE} the accountable approver for this request at that moment?
    - Was {CANDIDATE} the accountable approver on request {REQ_ID} when the request was made?
    - Was {CANDIDATE} the holder of the accountable approver role at the time of the request?
    - When the request was made, did {CANDIDATE} hold the accountable approver role?
    - When the request was made, was {CANDIDATE} the accountable approver for {REQ_ID}?
    - Would you say {CANDIDATE} was serving as the accountable approver when the request was made?
  Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE}.
    - At that moment, does the accountable approver field point to anybody other than {CANDIDATE}?
    - Going by these records, is the accountable approver role held by anyone other than {CANDIDATE} when the request was made?
    - Is the accountable approver role for the request held by a person other than {CANDIDATE}?
    - Just wondering, is the accountable approver for the request a person other than {CANDIDATE}?
    - Per the audit checklist, was the accountable approver role for request {REQ_ID} assigned to someone other than {CANDIDATE} when the request was made?
    - Per the records, does the accountable approver role for the request belong to a person other than {CANDIDATE}?
    - Under the audit checklist, is the accountable approver role for the request assigned to a person other than {CANDIDATE}?
    - When the request was made, did a person other than {CANDIDATE} hold the accountable approver role?
    - When the request was made, did the accountable approver role belong to a person other than {CANDIDATE}?
    - Would it be somebody other than {CANDIDATE} who had the accountable approver role when the request was made?
  Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request.
    - At the time of the request, is it true that {CANDIDATE} does not hold the accountable approver role?
    - Based on the records above, is it true that {CANDIDATE} does not hold the accountable approver role when the request was made?
    - For the audit file, is it correct that {CANDIDATE} does not hold the accountable approver role for the request?
    - Going by these records, is it correct that {CANDIDATE} does not hold the accountable approver role for request {REQ_ID}?
    - Is it correct that {CANDIDATE} does not hold the accountable approver designation on request {REQ_ID} at the time of the request?
    - Is it the case that {CANDIDATE} does not hold the accountable approver role when the request was made?
    - Is it true that the accountable approver role for request {REQ_ID} is not held by {CANDIDATE} when the request was made?
    - Is it true that {CANDIDATE} does not hold the accountable approver role for request {REQ_ID}?
    - Is it true that {CANDIDATE} was not the accountable approver at that moment?
    - Would you say it is the case that {CANDIDATE} does not hold the accountable approver role at the time of the request?

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
question>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qdf05183856",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: direct and plain.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q79acfaeff2",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = a person other than {CANDIDATE} holds it). Write the exact words 'other than' followed by {CANDIDATE} (for example 'a person other than {CANDIDATE}' or 'anyone other than {CANDIDATE}'). Never 'besides', 'apart from', 'except', 'else', 'not' or n't: a checking program accepts only 'other than'. Style: direct and plain.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'other than', followed by {CANDIDATE}",
   "no 'besides', no 'else', no 'not', no n't"
  ]
 },
 {
  "qid": "q4f37c0c301",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = a person other than {CANDIDATE} holds it). Write the exact words 'other than' followed by {CANDIDATE} (for example 'a person other than {CANDIDATE}' or 'anyone other than {CANDIDATE}'). Never 'besides', 'apart from', 'except', 'else', 'not' or n't: a checking program accepts only 'other than'. Style: puts the time phrase first.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'other than', followed by {CANDIDATE}",
   "no 'besides', no 'else', no 'not', no n't"
  ]
 },
 {
  "qid": "qe0f30348cd",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "q75dc77e9a1",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = a person other than {CANDIDATE} holds it). Write the exact words 'other than' followed by {CANDIDATE} (for example 'a person other than {CANDIDATE}' or 'anyone other than {CANDIDATE}'). Never 'besides', 'apart from', 'except', 'else', 'not' or n't: a checking program accepts only 'other than'. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'other than', followed by {CANDIDATE}",
   "no 'besides', no 'else', no 'not', no n't"
  ]
 },
 {
  "qid": "q2e2c768f40",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q0b41601d5a",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = a person other than {CANDIDATE} holds it). Write the exact words 'other than' followed by {CANDIDATE} (for example 'a person other than {CANDIDATE}' or 'anyone other than {CANDIDATE}'). Never 'besides', 'apart from', 'except', 'else', 'not' or n't: a checking program accepts only 'other than'. Style: passive voice where natural.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'other than', followed by {CANDIDATE}",
   "no 'besides', no 'else', no 'not', no n't"
  ]
 },
 {
  "qid": "q4efd872bd5",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: formal, as in an audit checklist.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "q21b2c20eb9",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = a person other than {CANDIDATE} holds it). Write the exact words 'other than' followed by {CANDIDATE} (for example 'a person other than {CANDIDATE}' or 'anyone other than {CANDIDATE}'). Never 'besides', 'apart from', 'except', 'else', 'not' or n't: a checking program accepts only 'other than'. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'other than', followed by {CANDIDATE}",
   "no 'besides', no 'else', no 'not', no n't"
  ]
 },
 {
  "qid": "qc8c50af66b",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = a person other than {CANDIDATE} holds it). Write the exact words 'other than' followed by {CANDIDATE} (for example 'a person other than {CANDIDATE}' or 'anyone other than {CANDIDATE}'). Never 'besides', 'apart from', 'except', 'else', 'not' or n't: a checking program accepts only 'other than'. Style: precise and slightly technical.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'other than', followed by {CANDIDATE}",
   "no 'besides', no 'else', no 'not', no n't"
  ]
 },
 {
  "qid": "qf46a4cde9e",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: puts the time phrase first.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 }
]

Reminder: write one JSON array with exactly 11 objects ({"qid": "...", "text": "..."}) to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/answers/T31-author_wording-ae6206ba-000.json and nothing else.
