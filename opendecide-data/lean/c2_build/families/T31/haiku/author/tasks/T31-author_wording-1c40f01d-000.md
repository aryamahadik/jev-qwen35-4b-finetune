# T31 authoring task T31-author_wording-1c40f01d-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_wording-1c40f01d-000.json

Task kind: author_wording; items: 45; answers expected: 45 (one per item, each with its qid).

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
  "qid": "q6df3883c44",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: puts the time phrase first.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q82652b6876",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: formal, as in an audit checklist.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q826c410249",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q40dfff9e7d",
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
  "qid": "qf2aca37f1e",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qef0ceb4d95",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q182777190d",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: conversational, as a colleague would ask.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q7f29ff9886",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: passive voice where natural.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q3d9b7c0d56",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: direct and plain.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "qf891f6a017",
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
  "qid": "q0cff21b785",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: precise and slightly technical.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q26a4750a26",
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
  "qid": "qc6c90017d2",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q6643f434ba",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q46f8e6f7df",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q1b8a102dea",
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
  "qid": "q67f9c34bdf",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: direct and plain.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qd8b01eac5f",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q171becfdc0",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: direct and plain.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q0022472fab",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: formal, as in an audit checklist.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q2bf3e5a49f",
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
  "qid": "q9f0022262e",
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
  "qid": "qbdd1419632",
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
  "qid": "q98fce2be6f",
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
  "qid": "qc649451e1a",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "qab922d25ee",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qa6b77698a8",
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
  "qid": "q94152d551a",
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
  "qid": "q4921055395",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q34e3611181",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: conversational, as a colleague would ask.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "q746330f093",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "q7d76083c05",
  "brief": "Meaning: Ask whether the accountable (A) role for the request belongs to a person other than {CANDIDATE} (yes = someone else holds it). Express 'someone else' with 'other than', 'besides' or 'someone else'; use no other negation (no 'not', no n't). Style: formal, as in an audit checklist.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no 'not' and no n't; the one implicit negation the meaning asks for only"
  ]
 },
 {
  "qid": "qace97a8c6e",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q0359617a84",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qba7a48f03f",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: short (under 14 words).",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qab23f84a59",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q9357438e80",
  "brief": "Meaning: Ask whether it is true that {CANDIDATE} does not hold the accountable (A) role for the request (yes = {CANDIDATE} does not hold it). Use exactly one 'not', inside an embedded statement: 'Is it true / correct / the case that ... not ...?'. Never start with a negative auxiliary (Isn't, Doesn't, Is ... not ...?). Style: puts the time phrase first.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "q5779f4453e",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: short (under 14 words).",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qb9131db82a",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: passive voice where natural.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qddaa487209",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qdd585f3513",
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
  "qid": "qd849a3a50b",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: precise and slightly technical.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q60cdc0e566",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qf083788d57",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: puts the time phrase first.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qe800668cdd",
  "brief": "Meaning: Ask whether {CANDIDATE} holds the accountable (A) role for the request at the time it was made (yes = {CANDIDATE} holds it). Style: passive voice where natural.",
  "slots": {
   "CANDIDATE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_wording-1c40f01d-000.json and nothing else.
