# T31 authoring task T31-author_lexicon-a2f0cd0c-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_lexicon-a2f0cd0c-000.json

Task kind: author_lexicon; items: 36; answers expected: 36 (one per item, each with its qid).

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write AMOUNT-BAND PHRASES. In a record line a program writes the word "amounts" followed by your phrase and a
full stop ("amounts ___."), where {X} is a money amount it fills in (for example $5,000.00). Each item states the
exact meaning; write one phrase with that meaning, different from the other phrases in this task.

Hard rules (a phrase that breaks one is thrown away):
1. Use {X} exactly once, plain; 2-8 words; lowercase; it must read naturally right after the word "amounts".
2. The words must make plain whether an amount exactly equal to {X} is included or excluded.
3. Never use the bare words under, over, below, above, beyond, within, exceeding, or "up to" without "and
   including" ("strictly below" and "strictly above" are fine).
4. No negation, no digits, no number words, no currency words of your own.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
phrase>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q8198929f09",
  "brief": "Style: conversational.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qc9dfa6c00e",
  "brief": "Style: with {X} at the start.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q82d8c5cf3c",
  "brief": "Style: plain.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qc2da46e309",
  "brief": "Style: terse.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q0b8336c413",
  "brief": "Style: with {X} at the end.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q734967697c",
  "brief": "Style: conversational.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qfea0b4b001",
  "brief": "Style: formal, as in a policy register.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q11e4370eee",
  "brief": "Style: plain.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q5034745aaf",
  "brief": "Style: plain.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q6b646a8418",
  "brief": "Style: uses 'strictly' or 'inclusive' / 'included'.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q8c41e0fd2a",
  "brief": "Style: with 'of' before {X}.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qe7f815ee7e",
  "brief": "Style: financial wording.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q26e7e5f464",
  "brief": "Style: plain.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qcc07c69b13",
  "brief": "Style: financial wording.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qb1c7e058d2",
  "brief": "Style: uses 'strictly' or 'inclusive' / 'included'.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qd7903bcd33",
  "brief": "Style: conversational.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q6ea1551e57",
  "brief": "Style: terse.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qdd56590b47",
  "brief": "Style: with {X} at the end.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q542cea9dc3",
  "brief": "Style: with 'of' before {X}.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qa02ef0639e",
  "brief": "Style: terse.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q02b51d41b4",
  "brief": "Style: formal, as in a policy register.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q288c0f95e9",
  "brief": "Style: uses 'strictly' or 'inclusive' / 'included'.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q4ac185d8bf",
  "brief": "Style: financial wording.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q2aa7a4bef4",
  "brief": "Style: financial wording.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qb1537c4b96",
  "brief": "Style: with {X} at the start.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q00e9a957c2",
  "brief": "Style: conversational.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qebe49c4ee2",
  "brief": "Style: with {X} at the start.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q3dbb83f945",
  "brief": "Style: with {X} at the end.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q597eadf664",
  "brief": "Style: with 'of' before {X}.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q12ef82dac8",
  "brief": "Style: formal, as in a policy register.",
  "meaning": "amounts strictly greater than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qef8490f58d",
  "brief": "Style: formal, as in a policy register.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "qebd15600c5",
  "brief": "Style: with {X} at the end.",
  "meaning": "amounts greater than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q51f8be9c14",
  "brief": "Style: uses 'strictly' or 'inclusive' / 'included'.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q429031aa86",
  "brief": "Style: terse.",
  "meaning": "amounts less than or equal to {X}: an amount exactly equal to {X} IS included",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q4f1a7a69d4",
  "brief": "Style: with 'of' before {X}.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 },
 {
  "qid": "q48ecef710f",
  "brief": "Style: with {X} at the start.",
  "meaning": "amounts strictly less than {X}: an amount exactly equal to {X} is EXCLUDED",
  "slots": {
   "X": "the money amount, exactly once"
  },
  "rules": [
   "2-8 words",
   "inclusion or exclusion of {X} itself must be plain"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_lexicon-a2f0cd0c-000.json and nothing else.
