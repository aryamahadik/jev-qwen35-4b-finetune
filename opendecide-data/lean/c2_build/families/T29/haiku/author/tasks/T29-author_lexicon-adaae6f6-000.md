# T29 authoring task T29-author_lexicon-adaae6f6-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_lexicon-adaae6f6-000.json

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
  "qid": "qcd57ca7c95",
  "brief": {
   "how_many": 10,
   "frames": [
    "the undo window is ___ (with {X} = '24 hours')",
    "a person last edited the target record ___ before the request time (with {X} = '60 minutes')"
   ],
   "avoid": "phrases whose edge reading is unclear, such as 'up to', 'within', 'around'"
  },
  "meaning": "strictly less than {X}: a value equal to {X} does NOT meet it",
  "slots": {
   "X": "the bound with its unit (a number of records, hours or minutes, or an amount of money)"
  },
  "rules": [
   "10 forms",
   "{X} exactly once",
   "each form must read naturally in every frame listed"
  ]
 },
 {
  "qid": "qce9812d8ef",
  "brief": {
   "how_many": 10,
   "frames": [
    "the amount paid out is ___ (with {X} = '$5,000.00')"
   ],
   "avoid": "phrases whose edge reading is unclear, such as 'up to', 'within', 'around'"
  },
  "meaning": "the amount {X} or more: an amount equal to {X} DOES meet it",
  "slots": {
   "X": "the bound with its unit (a number of records, hours or minutes, or an amount of money)"
  },
  "rules": [
   "10 forms",
   "{X} exactly once",
   "each form must read naturally in every frame listed"
  ]
 },
 {
  "qid": "q7b6bf77e9c",
  "brief": {
   "how_many": 10,
   "frames": [
    "the amount paid out is ___ (with {X} = '$5,000.00')"
   ],
   "avoid": "phrases whose edge reading is unclear, such as 'up to', 'within', 'around'"
  },
  "meaning": "strictly more than the amount {X}: an amount equal to {X} does NOT meet it",
  "slots": {
   "X": "the bound with its unit (a number of records, hours or minutes, or an amount of money)"
  },
  "rules": [
   "10 forms",
   "{X} exactly once",
   "each form must read naturally in every frame listed"
  ]
 },
 {
  "qid": "qe70f3671c5",
  "brief": {
   "how_many": 10,
   "frames": [
    "the call affects ___ (with {X} = '200 records')"
   ],
   "avoid": "phrases whose edge reading is unclear, such as 'up to', 'within', 'around'"
  },
  "meaning": "strictly more than {X}: a value equal to {X} does NOT meet it",
  "slots": {
   "X": "the bound with its unit (a number of records, hours or minutes, or an amount of money)"
  },
  "rules": [
   "10 forms",
   "{X} exactly once",
   "each form must read naturally in every frame listed"
  ]
 },
 {
  "qid": "q284eb839b4",
  "brief": {
   "how_many": 10,
   "frames": [
    "the call affects ___ (with {X} = '200 records')"
   ],
   "avoid": "phrases whose edge reading is unclear, such as 'up to', 'within', 'around'"
  },
  "meaning": "{X} or more: a value equal to {X} DOES meet it",
  "slots": {
   "X": "the bound with its unit (a number of records, hours or minutes, or an amount of money)"
  },
  "rules": [
   "10 forms",
   "{X} exactly once",
   "each form must read naturally in every frame listed"
  ]
 },
 {
  "qid": "q3f4b71a51c",
  "brief": {
   "how_many": 10,
   "frames": [
    "the undo window is ___ (with {X} = '24 hours')",
    "a person last edited the target record ___ before the request time (with {X} = '60 minutes')"
   ],
   "avoid": "phrases whose edge reading is unclear, such as 'up to', 'within', 'around'"
  },
  "meaning": "{X} or less: a value equal to {X} DOES meet it",
  "slots": {
   "X": "the bound with its unit (a number of records, hours or minutes, or an amount of money)"
  },
  "rules": [
   "10 forms",
   "{X} exactly once",
   "each form must read naturally in every frame listed"
  ]
 }
]
