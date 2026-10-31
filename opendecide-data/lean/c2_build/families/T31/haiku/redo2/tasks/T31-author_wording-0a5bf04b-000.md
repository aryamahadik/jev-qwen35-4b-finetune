# T31 TOP-UP authoring task T31-author_wording-0a5bf04b-000 (kind: author_wording; 24 items)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/answers/T31-author_wording-0a5bf04b-000.json

WHY THIS TASK EXISTS: new items for the T31 pool (ch_scope brief says 'which of the listed scopes' (no number word); wording pool toward about 170). Every item is new; answer all 24.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 24 objects, one per item at the bottom of this file.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character. A qid is the letter q followed by ten letters or digits
  (11 characters in all). Every qid below appears exactly once in your answer; never invent or shorten one.
- "text": your text as one JSON string (a line break inside it as \n, a double quote as \").
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
- The 24 qids of this task: q4dba22d6ed, qd2960a2eeb, q219d560322, q3b8e11ae28, q12a4b94fdf, q6b9868a3b3, q9ea1dfb06f, q9eadf71a92, qae60508abc, q8e6364bfa7, q59eec60ca6, q903543c5bc, q6ce6a8f5d9, q8597150d9a, qe229ed7b68, qaa81c43ef6, q7821b61f8f, q1c202bc666, q44d1db044b, qa8090f7fee, q04ad78abe7, q0ce4e3d0fd, q4002bf0549, q77c9be8656
Literal example of the shape (your own text in "text"):
[{"qid": "q4dba22d6ed", "text": "..."}, ...]

Task kind: author_wording; items: 24; answers expected: 24 (one per item, each with its qid).

FULL INSTRUCTIONS:

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS about whether a software agent may use a permission scope at the time of a request. A program shows a rule card and a block of records, then asks one
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
  Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request.
    - Among the scope identifiers, which may {REQ_AGENT} exercise at the time of the request?
    - At the time of the request, which of the listed scopes may {REQ_AGENT} use?
    - Based on the records above, which of the listed scopes may {REQ_AGENT} use at the time of the request?
    - For the audit file, which of the listed scopes may {REQ_AGENT} use at the time of the request?
    - Hey, which of the listed scopes can {REQ_AGENT} use at the time of the request?
    - Per the records, which of the listed scopes is {REQ_AGENT} allowed to use at the time of the request?
    - When the request was made, which of the listed scopes may {REQ_AGENT} use?
    - Which listed scope may {REQ_AGENT} use at the time of the request?
    - Which of the listed scopes has {REQ_AGENT} been cleared to use at the time of the request?
    - Which of the listed scopes may {REQ_AGENT} use at the time of the request?
    - Which of the listed scopes may {REQ_AGENT} use when the request was made?
    - Which of the listed scopes sits within the runtime permissions of {REQ_AGENT} at the time of the request?
    - Which of the listed scopes was {REQ_AGENT} permitted to use when the request was made?
  Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then.
    - According to the records, is {REQ_AGENT} allowed to use {REQ_SCOPE} at the time of the request?
    - According to the records, is {REQ_AGENT} permitted to use {REQ_SCOPE} at the time of the request?
    - At that moment, is {REQ_AGENT} permitted to use {REQ_SCOPE}?
    - At the time of the request, may {REQ_AGENT} use {REQ_SCOPE}?
    - Based on the records above, is {REQ_AGENT} entitled to use {REQ_SCOPE} at the time of the request?
    - Did {REQ_AGENT} have the right to use {REQ_SCOPE} when the request was made?
    - Does the audit standard allow {REQ_AGENT} to use {REQ_SCOPE} at the time of the request?
    - Does the runtime policy permit {REQ_AGENT} to invoke {REQ_SCOPE} at the time of the request?
    - Does {REQ_AGENT} have permission to use {REQ_SCOPE} at the time of the request?
    - Formally, is {REQ_AGENT} authorized to use {REQ_SCOPE} at the time of the request?
    - Hey, is {REQ_AGENT} allowed to use {REQ_SCOPE} at the time of the request?
    - Is invocation of {REQ_SCOPE} by {REQ_AGENT} permitted at the time of the request?
    - Is the use of {REQ_SCOPE} permitted for {REQ_AGENT} at the time of the request?
    - Is use of {REQ_SCOPE} by {REQ_AGENT} sanctioned at the time of the request?
    - Is {REQ_AGENT} cleared to use {REQ_SCOPE} at the time of the request?
    - Is {REQ_AGENT} entitled to use {REQ_SCOPE} at the time of the request?
    - Is {REQ_AGENT} permitted to use {REQ_SCOPE} at the time of the request?
    - Is {REQ_SCOPE} cleared for use by {REQ_AGENT} at the time of the request?
    - Per the audit checklist, is {REQ_AGENT} permitted to use {REQ_SCOPE} at the time of the request?
    - Per the records, may {REQ_AGENT} use {REQ_SCOPE} at the time of the request?
    - Tell me, is {REQ_AGENT} allowed to use {REQ_SCOPE} when the request was made?
    - Was {REQ_AGENT} permitted to use {REQ_SCOPE} when the request was made?
  Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT}.
    - Based on the records above, would {REQ_AGENT} go beyond its authority by using {REQ_SCOPE} at the time of the request?
    - For audit purposes, does the use of {REQ_SCOPE} at the time of the request go beyond the authority of {REQ_AGENT}?
    - Going by these records, would using {REQ_SCOPE} at the time of the request exceed the authority of {REQ_AGENT}?
    - Going by these records, would using {REQ_SCOPE} at the time of the request fall outside the authority of {REQ_AGENT}?
    - Is the authority of {REQ_AGENT} at the time of the request exceeded by using {REQ_SCOPE}?
    - Quick question: would using {REQ_SCOPE} at the time of the request be too much for {REQ_AGENT}?
    - When the request was made, would using {REQ_SCOPE} go beyond the authority of {REQ_AGENT}?
    - Would invoking {REQ_SCOPE} at the time of the request fall outside the authority bound to {REQ_AGENT}?
    - Would the authority of {REQ_AGENT} be exceeded by using {REQ_SCOPE} at the time of the request?
    - Would using {REQ_SCOPE} at the time of the request exceed the authority of {REQ_AGENT}?
    - Would {REQ_AGENT} exceed its authority with {REQ_SCOPE} at the time of the request?
  Meaning: Ask whether {REQ_AGENT} lacks the authority (or permission, or right) to use {REQ_SCOPE} at the time of the request.
    - At the time of the request, does {REQ_AGENT} lack the authority needed to use {REQ_SCOPE}?
    - At the time of the request, does {REQ_AGENT} lack the right to use {REQ_SCOPE}?
    - Based on the records above, does {REQ_AGENT} lack the right to use {REQ_SCOPE} at that moment?
    - Did {REQ_AGENT} lack the authority to use {REQ_SCOPE} when the request was made?
    - Does {REQ_AGENT} lack permission to use {REQ_SCOPE} at the time of the request?
    - Does {REQ_AGENT} lack the authority to use {REQ_SCOPE} when the request was made?
    - Does {REQ_AGENT} lack the runtime permission that would let it use {REQ_SCOPE} at the time of the request?
    - Hey, so does {REQ_AGENT} lack the authority to use {REQ_SCOPE} at the time of the request?
    - Is {REQ_AGENT} left lacking permission to use {REQ_SCOPE} at the time of the request?
    - Per the records, does {REQ_AGENT} lack the permission needed to use {REQ_SCOPE} at the time of the request?
    - Under the audit checklist, does {REQ_AGENT} lack the authority to use {REQ_SCOPE} at the time of the request?

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
question>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q4dba22d6ed",
  "brief": "Meaning: Ask whether {REQ_AGENT} lacks the authority (or permission, or right) to use {REQ_SCOPE} at the time of the request (yes = it lacks it). Use a form of 'lack' and name the authority, permission or right to use; never ask whether its grant lists the scope; no other negation. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "qd2960a2eeb",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q219d560322",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: puts the time phrase first.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q3b8e11ae28",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Never start the question with the word 'May' (a checking program reads a capitalised May as the month); 'may' later in the question is fine. Style: short (under 14 words).",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "the first word is never 'May'"
  ]
 },
 {
  "qid": "q12a4b94fdf",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q6b9868a3b3",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q9ea1dfb06f",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: short (under 14 words).",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q9eadf71a92",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "qae60508abc",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Never start the question with the word 'May' (a checking program reads a capitalised May as the month); 'may' later in the question is fine. Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "the first word is never 'May'"
  ]
 },
 {
  "qid": "q8e6364bfa7",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q59eec60ca6",
  "brief": "Meaning: Ask whether {REQ_AGENT} lacks the authority (or permission, or right) to use {REQ_SCOPE} at the time of the request (yes = it lacks it). Use a form of 'lack' and name the authority, permission or right to use; never ask whether its grant lists the scope; no other negation. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "q903543c5bc",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q6ce6a8f5d9",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Never start the question with the word 'May' (a checking program reads a capitalised May as the month); 'may' later in the question is fine. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "the first word is never 'May'"
  ]
 },
 {
  "qid": "q8597150d9a",
  "brief": "Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT} (yes = it would). Use no negation words, and never the word 'past' (a checking program reads it as a time word). Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "never the word 'past'"
  ]
 },
 {
  "qid": "qe229ed7b68",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: short (under 14 words).",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "qaa81c43ef6",
  "brief": "Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT} (yes = it would). Use no negation words, and never the word 'past' (a checking program reads it as a time word). Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "never the word 'past'"
  ]
 },
 {
  "qid": "q7821b61f8f",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q1c202bc666",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q44d1db044b",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "qa8090f7fee",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Never start the question with the word 'May' (a checking program reads a capitalised May as the month); 'may' later in the question is fine. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "the first word is never 'May'"
  ]
 },
 {
  "qid": "q04ad78abe7",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q0ce4e3d0fd",
  "brief": "Meaning: Ask which of the listed scopes {REQ_AGENT} may use at the time of the request. Write 'which of the listed scopes', 'which listed scope' or 'which of these scopes'; never 'which one' and no other number word (a checking program rejects them). The program shows the scopes as answer options; do not list them. Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "'which of the listed scopes' or 'which listed scope'; never 'which one'"
  ]
 },
 {
  "qid": "q4002bf0549",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Never start the question with the word 'May' (a checking program reads a capitalised May as the month); 'may' later in the question is fine. Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "the first word is never 'May'"
  ]
 },
 {
  "qid": "q77c9be8656",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Never start the question with the word 'May' (a checking program reads a capitalised May as the month); 'may' later in the question is fine. Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all",
   "the first word is never 'May'"
  ]
 }
]

Reminder: write one JSON array with exactly 24 objects ({"qid": "...", "text": "..."}) to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/answers/T31-author_wording-0a5bf04b-000.json and nothing else.
