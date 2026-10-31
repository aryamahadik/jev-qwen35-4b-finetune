# T31 authoring task T31-author_wording-a7e52c11-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_wording-a7e52c11-000.json

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
  "qid": "q4e75987758",
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
  "qid": "q715466d394",
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
  "qid": "q0e3f198983",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q06dce8c1a2",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qb11a2820c9",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: direct and plain.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q880686a401",
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
  "qid": "qe8f678a2a2",
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
  "qid": "q67019b3692",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q8fef6fddbb",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: precise and slightly technical.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q5bf2574372",
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
  "qid": "qb26cf65b59",
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
  "qid": "qc40242781b",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qc0a61ac353",
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
  "qid": "qc78cd81fc0",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qc8ebd042ea",
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
  "qid": "q12f5c86a61",
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
  "qid": "q32f163e9f5",
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
  "qid": "qa4efe46bb6",
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
  "qid": "qb7a5815e9a",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: passive voice where natural.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q74f3369a24",
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
  "qid": "q7b7874acca",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: short (under 14 words).",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q4f71cb7dda",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: passive voice where natural.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q7f5edde3bc",
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
  "qid": "q3bb7ae4cf9",
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
  "qid": "q3b1ec76bda",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: short (under 14 words).",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q5e1a8e970a",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: puts the time phrase first.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qc0ecb83943",
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
  "qid": "qd0c3e59a42",
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
  "qid": "qb13b1176a8",
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
  "qid": "qc0b9224ebb",
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
  "qid": "q3379230261",
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
  "qid": "q856e2f21c5",
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
  "qid": "qcdae137d6e",
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
  "qid": "q4861413beb",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: precise and slightly technical.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q89f79fc7ac",
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
  "qid": "q0dab5e3739",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q8f3a0fdaf9",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q24ba026348",
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
  "qid": "q0f70c388bb",
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
  "qid": "qa724564447",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: direct and plain.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q655a421cd1",
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
  "qid": "q4eac5628db",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q37649deeff",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: puts the time phrase first.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q42c81f815a",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q37a85be180",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_ID": "leave it out"
  },
  "rules": [
   "no negation at all"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_wording-a7e52c11-000.json and nothing else.
