# T24 authoring task T24-author_lexicon-4eff09fb-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_lexicon-4eff09fb-000.json

Task kind: author_lexicon; items: 4; outputs expected: 32.

You are writing short pieces of text for a synthetic training dataset about everyday customer-service
policies (returns, repairs, bookings, deposits, fees and the like). Everything you write is either a reusable template
(a program later fills each {SLOT} placeholder with a value) or a set of invented values. Write natural, varied
English. Invent everything: never copy text from real companies, products, people, laws, websites or published
datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write CLAUSE FORMS: one-line clauses that a program inserts into the versions of an invented customer-service
policy, both as bullet lines ("- <clause>.") and as cells of a table. Each item states the exact meaning, the
placeholders to keep and the edge case that must stay clear; write the number of distinct forms it asks for, all
with exactly that meaning.

How the program fills the placeholders: {N} becomes a number of days with its unit (e.g. "14 days" or "fourteen
days"); {A} the name of one date of the case (e.g. "delivery date"); {M} the name of the money amount (e.g. "price");
{X} an amount of money (e.g. "$1,250.00", "1,250.00 USD" or "$1,250"); {C} a category name (e.g. "suitcases");
{K} a condition name (e.g. "receipt kept"); {O} an outcome name (e.g. "partial settlement"); {S} and {E} dates
(e.g. "5 March 2026").

Hard rules (a form that breaks one is thrown away):
1. One line that starts with a capital letter, never with a placeholder; no period or other punctuation at the end.
2. Keep every listed placeholder exactly once, spelled exactly so with its curly braces; add no other placeholder.
   Two placeholders never touch (always at least one word between them). Never write "a" or "an" right before a
   placeholder, and never add the word "days" after {N} (it already holds the unit).
3. No digits, number words, dates, months, amounts or other values: the program supplies every value.
4. No hedges (about, around, roughly, nearly, almost, approximately, usually) and no double quote characters.
5. The meaning must be unmistakable to any careful reader, including at the edge case the item names. A form adds
   no condition, no exception and no second idea, and never mentions any other clause.
6. All forms in your answer are distinct.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "forms": ["<form 1>", "<form 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qc6edf08c07",
  "brief": {
   "how_many": 8,
   "style": "a rule about when a request has to be made",
   "edge_case": "a request made exactly {N} after the {A} is on time",
   "avoid": "never use wordings whose edge reading is unclear, such as 'before {N} have passed', 'less than {N}', 'under {N}' or 'by the end of'"
  },
  "meaning": "the base time limit: a request is on time when it is made at most {N} after the {A}. The {A} itself is day zero, so a request made exactly {N} after the {A} is still on time, and one day later is late",
  "slots": {
   "N": "the time limit: a number of days with its unit, e.g. '14 days'",
   "A": "the name of one date of the case, e.g. 'delivery date'"
  },
  "rules": [
   "8 forms",
   "{N}, {A}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q56057a0533",
  "brief": {
   "how_many": 8,
   "style": "a statement of the time limit itself, naming the date it is counted from",
   "edge_case": "a request made exactly {N} after the {A} is on time",
   "avoid": "never use wordings whose edge reading is unclear, such as 'before {N} have passed', 'less than {N}', 'under {N}' or 'by the end of'"
  },
  "meaning": "the base time limit: a request is on time when it is made at most {N} after the {A}. The {A} itself is day zero, so a request made exactly {N} after the {A} is still on time, and one day later is late",
  "slots": {
   "N": "the time limit: a number of days with its unit, e.g. '14 days'",
   "A": "the name of one date of the case, e.g. 'delivery date'"
  },
  "rules": [
   "8 forms",
   "{N}, {A}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "qe621602976",
  "brief": {
   "how_many": 8,
   "style": "phrased around the customer (e.g. 'Customers have ...')",
   "edge_case": "a request made exactly {N} after the {A} is on time",
   "avoid": "never use wordings whose edge reading is unclear, such as 'before {N} have passed', 'less than {N}', 'under {N}' or 'by the end of'"
  },
  "meaning": "the base time limit: a request is on time when it is made at most {N} after the {A}. The {A} itself is day zero, so a request made exactly {N} after the {A} is still on time, and one day later is late",
  "slots": {
   "N": "the time limit: a number of days with its unit, e.g. '14 days'",
   "A": "the name of one date of the case, e.g. 'delivery date'"
  },
  "rules": [
   "8 forms",
   "{N}, {A}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "qfb9f8a8e24",
  "brief": {
   "how_many": 8,
   "style": "a short policy line",
   "edge_case": "a request made exactly {N} after the {A} is on time",
   "avoid": "never use wordings whose edge reading is unclear, such as 'before {N} have passed', 'less than {N}', 'under {N}' or 'by the end of'"
  },
  "meaning": "the base time limit: a request is on time when it is made at most {N} after the {A}. The {A} itself is day zero, so a request made exactly {N} after the {A} is still on time, and one day later is late",
  "slots": {
   "N": "the time limit: a number of days with its unit, e.g. '14 days'",
   "A": "the name of one date of the case, e.g. 'delivery date'"
  },
  "rules": [
   "8 forms",
   "{N}, {A}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 }
]
