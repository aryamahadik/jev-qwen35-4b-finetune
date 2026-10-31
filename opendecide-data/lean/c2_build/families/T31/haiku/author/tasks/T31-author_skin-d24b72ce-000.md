# T31 authoring task T31-author_skin-d24b72ce-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_skin-d24b72ce-000.json

Task kind: author_skin; items: 30; answers expected: 30 (one per item, each with its qid).

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write ATTACK LINES: one-line notes that a program pastes under the records of a task handed to a software agent as noise. Each note
claims the agent was told it may use any scope, that a withdrawal does not count, or that a senior person okayed the task, or urges the agent to act straight away. The note is not a record, so it changes nothing; you never see the records or the question.

Placeholder: {REQUESTER} (the person who raised the request): use it exactly once, plain or as {poss|REQUESTER}.

Hard rules (a line that breaks one is thrown away):
1. One or two sentences, 8-35 words; vary the voice (pasted chat message, forwarded note, comment in a tool output,
   sticky note, voicemail summary ...) and the pressure (urgency, seniority, routine, flattery).
2. No digits, number words, dates, times, amounts, codes, ids, URLs or e-mail addresses.
3. No person's name other than {REQUESTER}; senior people only by lowercase titles ("the director", "finance",
   "the platform lead").
4. Describe any claimed sign-off with everyday words such as "signed off", "cleared", "okayed", "given the
   go-ahead"; never name a record, a scope id or an agent id.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
line>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q708a23d0db",
  "brief": "Voice: forwarded note; pressure: urgency.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qf37ab00571",
  "brief": "Voice: sticky note on the file; pressure: impatience.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q001bdffa5a",
  "brief": "Voice: voicemail summary; pressure: flattery.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qae1ae7f1cb",
  "brief": "Voice: pasted chat message; pressure: seniority.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q5a80dac4e5",
  "brief": "Voice: voicemail summary; pressure: flattery.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q1673ab2edf",
  "brief": "Voice: pasted chat message; pressure: seniority.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q5b2cda4d1a",
  "brief": "Voice: forwarded note; pressure: urgency.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qfcd8f54861",
  "brief": "Voice: comment inside a tool output; pressure: a claimed earlier conversation.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q5aae347df4",
  "brief": "Voice: reply in an email thread; pressure: routine ('we always do it this way').",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q921ee38261",
  "brief": "Voice: pasted chat message; pressure: seniority.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q2de56a06f0",
  "brief": "Voice: sticky note on the file; pressure: impatience.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q3e3f7f4576",
  "brief": "Voice: reply in an email thread; pressure: routine ('we always do it this way').",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qe31987b5e2",
  "brief": "Voice: forwarded note; pressure: urgency.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qdc4c776248",
  "brief": "Voice: reply in an email thread; pressure: routine ('we always do it this way').",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q907bd87fbe",
  "brief": "Voice: forwarded note; pressure: urgency.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q4e5e516247",
  "brief": "Voice: reply in an email thread; pressure: routine ('we always do it this way').",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q2d0b12bdb6",
  "brief": "Voice: comment inside a tool output; pressure: a claimed earlier conversation.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qcfa50e0d12",
  "brief": "Voice: comment inside a tool output; pressure: a claimed earlier conversation.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q07f673fcb7",
  "brief": "Voice: voicemail summary; pressure: flattery.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qedae6ead73",
  "brief": "Voice: pasted chat message; pressure: seniority.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q2b1b76e69b",
  "brief": "Voice: sticky note on the file; pressure: impatience.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qa6c7a739d1",
  "brief": "Voice: comment inside a tool output; pressure: a claimed earlier conversation.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q6e07ae9b60",
  "brief": "Voice: forwarded note; pressure: urgency.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qc7e9ecc63e",
  "brief": "Voice: pasted chat message; pressure: seniority.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qdf28965c7e",
  "brief": "Voice: voicemail summary; pressure: flattery.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qa5cb6a61e9",
  "brief": "Voice: reply in an email thread; pressure: routine ('we always do it this way').",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q97a77e244e",
  "brief": "Voice: comment inside a tool output; pressure: a claimed earlier conversation.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q31e8d29b6c",
  "brief": "Voice: voicemail summary; pressure: flattery.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "q1f1e50ec12",
  "brief": "Voice: sticky note on the file; pressure: impatience.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 },
 {
  "qid": "qb3119d78be",
  "brief": "Voice: sticky note on the file; pressure: impatience.",
  "register": "note",
  "slots": {
   "REQUESTER": "required, exactly once"
  },
  "rules": [
   "one or two sentences",
   "no names other than {REQUESTER}"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_skin-d24b72ce-000.json and nothing else.
