# T31 authoring task T31-author_wording-3cb3169d-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/heldout/answers/T31-author_wording-3cb3169d-000.json

Task kind: author_wording; items: 24; answers expected: 24 (one per item, each with its qid).

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

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
question>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qf0301b1540",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qf7c8f87ec9",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "q9f9332a373",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: puts the time phrase first.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qd9dce36c17",
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
  "qid": "qb379452a0a",
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
  "qid": "q7db74bd326",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: puts the time phrase first.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "q8125ecfd18",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: short (under 14 words).",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "q08116e52f5",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qff3f22a301",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: passive voice where natural.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "qec9f110113",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: passive voice where natural.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q4cf491b642",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: precise and slightly technical.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "q6f7c646986",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: puts the time phrase first.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qe1935e58e3",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: direct and plain.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q18a03a5056",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: short (under 14 words).",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "qe4ee18f009",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: passive voice where natural.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "q4f08ead283",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: direct and plain.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "q591ad986ac",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: precise and slightly technical.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q9ef80b2b6a",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: short (under 14 words).",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q1cedc72d86",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: precise and slightly technical.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "qfe38c4022c",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "q7557edb61e",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: conversational, as a colleague would ask.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "q6d54365ebd",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "qa861aff9dd",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: passive voice where natural.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q80e7e0a8fa",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/heldout/answers/T31-author_wording-3cb3169d-000.json and nothing else.
