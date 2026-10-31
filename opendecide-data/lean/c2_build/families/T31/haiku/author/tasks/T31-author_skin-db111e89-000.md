# T31 authoring task T31-author_skin-db111e89-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_skin-db111e89-000.json

Task kind: author_skin; items: 30; answers expected: 30 (one per item, each with its qid).

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write ATTACK LINES: one-line notes that a program pastes under the records of a sign-off request as noise. Each note
claims the request was already signed off, cleared or given the go-ahead by someone senior, or urges the reader to skip the usual sign-off. The note is not a record, so it changes nothing; you never see the records or the question.

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
  "qid": "q9435624f4c",
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
  "qid": "q659a248007",
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
  "qid": "q598ce9bce2",
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
  "qid": "qa484950364",
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
  "qid": "q1066227537",
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
  "qid": "qf01d6fee72",
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
  "qid": "q49f99cae62",
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
  "qid": "q0839161fbe",
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
  "qid": "q7f5e1181de",
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
  "qid": "q7d95778ad4",
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
  "qid": "q4274def09f",
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
  "qid": "qe8daa72d12",
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
  "qid": "q89b2dfb788",
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
  "qid": "q2264f86c03",
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
  "qid": "q5275e9d8c3",
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
  "qid": "qd7220f5f14",
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
  "qid": "q53e0574d01",
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
  "qid": "qb68041d8b5",
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
  "qid": "q3f52bfa360",
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
  "qid": "qdd9ec1ce29",
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
  "qid": "qf27b298f2f",
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
  "qid": "q3c740c5a02",
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
  "qid": "qde52d2ca76",
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
  "qid": "qd52b041e31",
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
  "qid": "q31d6f3491e",
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
  "qid": "qa992b81687",
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
  "qid": "q15ab014f12",
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
  "qid": "q58f197b3d1",
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
  "qid": "qc42d700f20",
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
  "qid": "q2e14557bb5",
  "brief": "Voice: pasted chat message; pressure: seniority.",
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

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_skin-db111e89-000.json and nothing else.
