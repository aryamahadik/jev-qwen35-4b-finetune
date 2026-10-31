# T24 authoring task T24-author_lexicon-2309cd54-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_lexicon-2309cd54-000.json

Task kind: author_lexicon; items: 6; outputs expected: 48.

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
  "qid": "q42a0ddb9cb",
  "brief": {
   "how_many": 8,
   "style": "phrased around the condition ('For cases whose condition is {K}, ...')",
   "edge_case": "{K} is the case's condition and {O} is the outcome it gets",
   "avoid": "never say what happens to cases in other conditions"
  },
  "meaning": "cases whose condition is {K} get the outcome {O}: the clause names the outcome for that condition and adds no other rule",
  "slots": {
   "K": "a condition name, e.g. 'receipt kept'",
   "O": "an outcome name, e.g. 'partial settlement'"
  },
  "rules": [
   "8 forms",
   "{K}, {O}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q79cf193f71",
  "brief": {
   "how_many": 8,
   "style": "a short policy line",
   "edge_case": "{K} is the case's condition and {O} is the outcome it gets",
   "avoid": "never say what happens to cases in other conditions"
  },
  "meaning": "cases whose condition is {K} get the outcome {O}: the clause names the outcome for that condition and adds no other rule",
  "slots": {
   "K": "a condition name, e.g. 'receipt kept'",
   "O": "an outcome name, e.g. 'partial settlement'"
  },
  "rules": [
   "8 forms",
   "{K}, {O}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q521bb21be4",
  "brief": {
   "how_many": 8,
   "style": "a short policy line",
   "edge_case": "every case in the {C} category is excluded",
   "avoid": "never mention any other category"
  },
  "meaning": "cases in the category {C} are excluded from this policy: it gives them nothing at all",
  "slots": {
   "C": "a category name, e.g. 'suitcases'"
  },
  "rules": [
   "8 forms",
   "{C}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q3ed49df673",
  "brief": {
   "how_many": 8,
   "style": "phrased around the policy's cover ('This policy ...')",
   "edge_case": "every case in the {C} category is excluded",
   "avoid": "never mention any other category"
  },
  "meaning": "cases in the category {C} are excluded from this policy: it gives them nothing at all",
  "slots": {
   "C": "a category name, e.g. 'suitcases'"
  },
  "rules": [
   "8 forms",
   "{C}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q2bb397bf81",
  "brief": {
   "how_many": 8,
   "style": "phrased around the outcome ('The outcome is {O} for ...')",
   "edge_case": "{K} is the case's condition and {O} is the outcome it gets",
   "avoid": "never say what happens to cases in other conditions"
  },
  "meaning": "cases whose condition is {K} get the outcome {O}: the clause names the outcome for that condition and adds no other rule",
  "slots": {
   "K": "a condition name, e.g. 'receipt kept'",
   "O": "an outcome name, e.g. 'partial settlement'"
  },
  "rules": [
   "8 forms",
   "{K}, {O}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "qb4f777c378",
  "brief": {
   "how_many": 8,
   "style": "phrased around the category ('The {C} category ...')",
   "edge_case": "every case in the {C} category is excluded",
   "avoid": "never mention any other category"
  },
  "meaning": "cases in the category {C} are excluded from this policy: it gives them nothing at all",
  "slots": {
   "C": "a category name, e.g. 'suitcases'"
  },
  "rules": [
   "8 forms",
   "{C}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 }
]
