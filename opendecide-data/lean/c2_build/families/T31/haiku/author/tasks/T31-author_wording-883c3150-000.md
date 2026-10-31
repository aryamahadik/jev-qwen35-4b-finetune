# T31 authoring task T31-author_wording-883c3150-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_wording-883c3150-000.json

Task kind: author_wording; items: 42; answers expected: 42 (one per item, each with its qid).

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

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
question>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qb8f0635b21",
  "brief": "Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT} (yes = it would). Use no negation words. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q794340ae89",
  "brief": "Meaning: Ask whether {REQ_AGENT} lacks the authority (or permission, or right) to use {REQ_SCOPE} at the time of the request (yes = it lacks it). Use a form of 'lack' and name the authority, permission or right to use; never ask whether its grant lists the scope; no other negation. Style: short (under 14 words).",
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
  "qid": "q37d001ac2b",
  "brief": "Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT} (yes = it would). Use no negation words. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qd04bb2e6c9",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q73fcf4a797",
  "brief": "Meaning: Ask whether {REQ_AGENT} lacks the authority (or permission, or right) to use {REQ_SCOPE} at the time of the request (yes = it lacks it). Use a form of 'lack' and name the authority, permission or right to use; never ask whether its grant lists the scope; no other negation. Style: puts the time phrase first.",
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
  "qid": "q5c465b8c3b",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q40db12407a",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: puts the time phrase first.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q559589e9c3",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q49af9f7b89",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q0a103960fa",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qde31a61aec",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q637047e024",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q47a0268d8c",
  "brief": "Meaning: Ask whether it is true that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request (yes = it is not permitted). Use exactly one 'not', inside 'Is it true / the case that ... is not permitted / not allowed / not entitled to use ...?'. Never start with a negative auxiliary. Style: puts the time phrase first.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "qfc10be5ce6",
  "brief": "Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT} (yes = it would). Use no negation words. Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q8f824fad3b",
  "brief": "Meaning: Ask whether it is true that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request (yes = it is not permitted). Use exactly one 'not', inside 'Is it true / the case that ... is not permitted / not allowed / not entitled to use ...?'. Never start with a negative auxiliary. Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "qa71c792c59",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qb1ba577269",
  "brief": "Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT} (yes = it would). Use no negation words. Style: short (under 14 words).",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qde06fff421",
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
  "qid": "q6fb1641aee",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: short (under 14 words).",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qe45c109f84",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q2c18dda450",
  "brief": "Meaning: Ask whether it is true that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request (yes = it is not permitted). Use exactly one 'not', inside 'Is it true / the case that ... is not permitted / not allowed / not entitled to use ...?'. Never start with a negative auxiliary. Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "q7aa74dc44f",
  "brief": "Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT} (yes = it would). Use no negation words. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q8e623f29ae",
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
  "qid": "q17e7639362",
  "brief": "Meaning: Ask whether using {REQ_SCOPE} at the time of the request would exceed, go beyond or fall outside the authority of {REQ_AGENT} (yes = it would). Use no negation words. Style: precise and slightly technical.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qb7f1d7ee06",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q34739f2671",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q844d8ddea4",
  "brief": "Meaning: Ask whether it is true that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request (yes = it is not permitted). Use exactly one 'not', inside 'Is it true / the case that ... is not permitted / not allowed / not entitled to use ...?'. Never start with a negative auxiliary. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "q73787d3505",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: short (under 14 words).",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qf2e770f2e9",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q3a70711201",
  "brief": "Meaning: Ask whether {REQ_AGENT} lacks the authority (or permission, or right) to use {REQ_SCOPE} at the time of the request (yes = it lacks it). Use a form of 'lack' and name the authority, permission or right to use; never ask whether its grant lists the scope; no other negation. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
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
  "qid": "q06ef05f265",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q41fe5a1463",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: formal, as in an audit checklist.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q9678c4e872",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q3193b02f02",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: puts the time phrase first.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qa77051c79d",
  "brief": "Meaning: Ask whether {REQ_AGENT} lacks the authority (or permission, or right) to use {REQ_SCOPE} at the time of the request (yes = it lacks it). Use a form of 'lack' and name the authority, permission or right to use; never ask whether its grant lists the scope; no other negation. Style: formal, as in an audit checklist.",
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
  "qid": "q88921b0742",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q352455ad5d",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: uses 'per the records' or 'going by these records'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q5e27563a85",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: puts the time phrase first.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "qc8df30a2e0",
  "brief": "Meaning: Ask whether it is true that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request (yes = it is not permitted). Use exactly one 'not', inside 'Is it true / the case that ... is not permitted / not allowed / not entitled to use ...?'. Never start with a negative auxiliary. Style: direct and plain.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "exactly one 'not', inside an embedded statement"
  ]
 },
 {
  "qid": "qd73466a9c6",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: starts with a lead-in such as 'According to the records,' or 'Based on the records above,'.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q5f58b34725",
  "brief": "Meaning: Ask which one of the listed scopes {REQ_AGENT} may use at the time of the request. The program shows the scopes as answer options; do not list them. Style: names the time explicitly ('at the time of the request' or 'when the request was made').",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 },
 {
  "qid": "q98807c84eb",
  "brief": "Meaning: Ask whether {REQ_AGENT} may use {REQ_SCOPE} at the time of the request, in the sense of permission then (yes = it may). Style: passive voice where natural.",
  "slots": {
   "REQ_AGENT": "required, exactly once",
   "REQ_SCOPE": "required, exactly once",
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_wording-883c3150-000.json and nothing else.
