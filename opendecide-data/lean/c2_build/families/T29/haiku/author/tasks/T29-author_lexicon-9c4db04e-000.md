# T29 authoring task T29-author_lexicon-9c4db04e-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_lexicon-9c4db04e-000.json

Task kind: author_lexicon; items: 2; outputs expected: 24.

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
  "qid": "q3d15ba0edb",
  "brief": {
   "how_many": 12,
   "style": "full sentence, plain English",
   "frame": "Precedence: ___"
  },
  "meaning": "one sentence that ranks the policy's rule tiers: a rule of the 'forbidden' tier beats a rule of the 'needs confirmation' tier, which beats the default (running the call straight away when no rule applies). Name both tiers with exactly these words, 'forbidden' and 'needs confirmation', and mention the default. Say nothing about the user's confirmation and add no other rule",
  "slots": {},
  "rules": [
   "12 forms",
   "one sentence each",
   "no placeholders"
  ]
 },
 {
  "qid": "qc1d2b3d4a5",
  "brief": {
   "how_many": 12,
   "style": "compact, like a policy line",
   "frame": "Precedence: ___"
  },
  "meaning": "one sentence that ranks the policy's rule tiers: a rule of the 'forbidden' tier beats a rule of the 'needs confirmation' tier, which beats the default (running the call straight away when no rule applies). Name both tiers with exactly these words, 'forbidden' and 'needs confirmation', and mention the default. Say nothing about the user's confirmation and add no other rule",
  "slots": {},
  "rules": [
   "12 forms",
   "one sentence each",
   "no placeholders"
  ]
 }
]
