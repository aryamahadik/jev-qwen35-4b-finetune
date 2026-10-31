# T29 authoring task T29-author_lexicon-0da8edd1-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_lexicon-0da8edd1-000.json

Task kind: author_lexicon; items: 6; outputs expected: 60.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write LEXICON FORMS: short phrases or sentences that a program inserts into a policy text or into a quoted
user message. Each item states the
exact meaning, the placeholders to keep and the frames the form must fit; write the number of distinct forms it
asks for, all with exactly that meaning.

Hard rules (a form that breaks one is thrown away):
1. Keep every listed placeholder exactly once, spelled exactly so with its curly braces; add no other placeholder.
2. The meaning must be unmistakable to any careful reader, including at the edge case the item names.
3. No digits or number words (the program supplies every value), no hedges (about, around, roughly, nearly,
   almost, approximately, maybe), no double quote characters.
4. All forms in your answer are distinct and none adds a condition, an exception or a second idea.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "forms": ["<form 1>", "<form 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qe0fc727519",
  "brief": {
   "how_many": 10,
   "style": "short, casual",
   "frame": "Earlier in this conversation the user wrote: «___»"
  },
  "meaning": "the user clearly and unconditionally tells the agent to run {ACT} on {TGT}: an affirmative instruction for exactly that call, with no question, no condition (if, unless, once, when, as long as), no negation and no hedge",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 forms",
   "{ACT} and {TGT} each exactly once",
   "no double quote characters"
  ]
 },
 {
  "qid": "qb6992c48cc",
  "brief": {
   "how_many": 10,
   "style": "a question about what the call would change",
   "frame": "Earlier in this conversation the user wrote: «___»"
  },
  "meaning": "the user only asks about, or refers to, {ACT} on {TGT} without agreeing to it and without telling the agent to run it: no word of agreement or instruction (yes, sure, okay, fine, do it, run it, confirmed, agreed, please continue)",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 forms",
   "{ACT} and {TGT} each exactly once",
   "no double quote characters"
  ]
 },
 {
  "qid": "qaa5fc63528",
  "brief": {
   "how_many": 10,
   "style": "formal and complete",
   "frame": "Earlier in this conversation the user wrote: «___»"
  },
  "meaning": "the user clearly and unconditionally tells the agent to run {ACT} on {TGT}: an affirmative instruction for exactly that call, with no question, no condition (if, unless, once, when, as long as), no negation and no hedge",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 forms",
   "{ACT} and {TGT} each exactly once",
   "no double quote characters"
  ]
 },
 {
  "qid": "q7f33c8f0de",
  "brief": {
   "how_many": 10,
   "style": "a question about timing or progress of the call, with no time words or numbers",
   "frame": "Earlier in this conversation the user wrote: «___»"
  },
  "meaning": "the user only asks about, or refers to, {ACT} on {TGT} without agreeing to it and without telling the agent to run it: no word of agreement or instruction (yes, sure, okay, fine, do it, run it, confirmed, agreed, please continue)",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 forms",
   "{ACT} and {TGT} each exactly once",
   "no double quote characters"
  ]
 },
 {
  "qid": "q14bd8eec91",
  "brief": {
   "how_many": 10,
   "style": "a neutral remark that refers to the call without agreeing to it",
   "frame": "Earlier in this conversation the user wrote: «___»"
  },
  "meaning": "the user only asks about, or refers to, {ACT} on {TGT} without agreeing to it and without telling the agent to run it: no word of agreement or instruction (yes, sure, okay, fine, do it, run it, confirmed, agreed, please continue)",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 forms",
   "{ACT} and {TGT} each exactly once",
   "no double quote characters"
  ]
 },
 {
  "qid": "q2ad9eba2c3",
  "brief": {
   "how_many": 10,
   "style": "chat style, as typed quickly",
   "frame": "Earlier in this conversation the user wrote: «___»"
  },
  "meaning": "the user clearly and unconditionally tells the agent to run {ACT} on {TGT}: an affirmative instruction for exactly that call, with no question, no condition (if, unless, once, when, as long as), no negation and no hedge",
  "slots": {
   "ACT": "the id of the tool call, a snake_case action name",
   "TGT": "the id of the record"
  },
  "rules": [
   "10 forms",
   "{ACT} and {TGT} each exactly once",
   "no double quote characters"
  ]
 }
]
