# T24 authoring task T24-author_lexicon-8b6a4b49-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_lexicon-8b6a4b49-000.json

Task kind: author_lexicon; items: 7; outputs expected: 56.

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
  "qid": "qc7d0fee4a2",
  "brief": {
   "how_many": 8,
   "style": "phrased around the cases ('Cases whose {A} ...')",
   "edge_case": "a case whose {A} is exactly {S} or exactly {E} is inside the window",
   "avoid": "state the inclusivity inside the form ('both dates included', 'inclusive', 'from {S} through {E}', 'on or after {S} and on or before {E}'); never a bare 'from {S} to {E}', 'between {S} and {E}' or 'until {E}'; make clear that {N} replaces the usual time limit"
  },
  "meaning": "a special time limit by date window: cases whose {A} falls inside the window from {S} to {E}, with BOTH end dates included, have the time limit {N}, which replaces the usual time limit for them",
  "slots": {
   "A": "the name of one date of the case, e.g. 'delivery date'",
   "S": "the first date of the window, e.g. '5 March 2026'",
   "E": "the last date of the window, e.g. '19 March 2026'",
   "N": "the time limit: a number of days with its unit, e.g. '14 days'"
  },
  "rules": [
   "8 forms",
   "{A}, {S}, {E}, {N}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q4e79d75be3",
  "brief": {
   "how_many": 8,
   "style": "phrased around the time limit ('The time limit is {N} instead for ...')",
   "edge_case": "a case whose {A} is exactly {S} or exactly {E} is inside the window",
   "avoid": "state the inclusivity inside the form ('both dates included', 'inclusive', 'from {S} through {E}', 'on or after {S} and on or before {E}'); never a bare 'from {S} to {E}', 'between {S} and {E}' or 'until {E}'; make clear that {N} replaces the usual time limit"
  },
  "meaning": "a special time limit by date window: cases whose {A} falls inside the window from {S} to {E}, with BOTH end dates included, have the time limit {N}, which replaces the usual time limit for them",
  "slots": {
   "A": "the name of one date of the case, e.g. 'delivery date'",
   "S": "the first date of the window, e.g. '5 March 2026'",
   "E": "the last date of the window, e.g. '19 March 2026'",
   "N": "the time limit: a number of days with its unit, e.g. '14 days'"
  },
  "rules": [
   "8 forms",
   "{A}, {S}, {E}, {N}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q96c00c6ff8",
  "brief": {
   "how_many": 8,
   "style": "a short policy line",
   "edge_case": "the form makes clear that {N} replaces the usual time limit for the {C} category (e.g. with 'instead' or 'in place of the usual time limit')",
   "avoid": "never name a date and never say what the days are counted from"
  },
  "meaning": "a special time limit for one category: cases in the category {C} have the time limit {N}, which replaces the usual time limit for them (the days are still counted from the date the usual time limit names)",
  "slots": {
   "C": "a category name, e.g. 'suitcases'",
   "N": "the time limit: a number of days with its unit, e.g. '14 days'"
  },
  "rules": [
   "8 forms",
   "{C}, {N}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "qde08086fcc",
  "brief": {
   "how_many": 8,
   "style": "phrased around the category ('For the {C} category, ...')",
   "edge_case": "the form makes clear that {N} replaces the usual time limit for the {C} category (e.g. with 'instead' or 'in place of the usual time limit')",
   "avoid": "never name a date and never say what the days are counted from"
  },
  "meaning": "a special time limit for one category: cases in the category {C} have the time limit {N}, which replaces the usual time limit for them (the days are still counted from the date the usual time limit names)",
  "slots": {
   "C": "a category name, e.g. 'suitcases'",
   "N": "the time limit: a number of days with its unit, e.g. '14 days'"
  },
  "rules": [
   "8 forms",
   "{C}, {N}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q2f3d3d2aea",
  "brief": {
   "how_many": 8,
   "style": "phrased around the time limit ('The time limit for ...')",
   "edge_case": "the form makes clear that {N} replaces the usual time limit for the {C} category (e.g. with 'instead' or 'in place of the usual time limit')",
   "avoid": "never name a date and never say what the days are counted from"
  },
  "meaning": "a special time limit for one category: cases in the category {C} have the time limit {N}, which replaces the usual time limit for them (the days are still counted from the date the usual time limit names)",
  "slots": {
   "C": "a category name, e.g. 'suitcases'",
   "N": "the time limit: a number of days with its unit, e.g. '14 days'"
  },
  "rules": [
   "8 forms",
   "{C}, {N}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "q47932f09d2",
  "brief": {
   "how_many": 8,
   "style": "a short policy line",
   "edge_case": "a case whose {A} is exactly {S} or exactly {E} is inside the window",
   "avoid": "state the inclusivity inside the form ('both dates included', 'inclusive', 'from {S} through {E}', 'on or after {S} and on or before {E}'); never a bare 'from {S} to {E}', 'between {S} and {E}' or 'until {E}'; make clear that {N} replaces the usual time limit"
  },
  "meaning": "a special time limit by date window: cases whose {A} falls inside the window from {S} to {E}, with BOTH end dates included, have the time limit {N}, which replaces the usual time limit for them",
  "slots": {
   "A": "the name of one date of the case, e.g. 'delivery date'",
   "S": "the first date of the window, e.g. '5 March 2026'",
   "E": "the last date of the window, e.g. '19 March 2026'",
   "N": "the time limit: a number of days with its unit, e.g. '14 days'"
  },
  "rules": [
   "8 forms",
   "{A}, {S}, {E}, {N}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 },
 {
  "qid": "qa3c683e71a",
  "brief": {
   "how_many": 8,
   "style": "starting with 'For' or 'When'",
   "edge_case": "a case whose {A} is exactly {S} or exactly {E} is inside the window",
   "avoid": "state the inclusivity inside the form ('both dates included', 'inclusive', 'from {S} through {E}', 'on or after {S} and on or before {E}'); never a bare 'from {S} to {E}', 'between {S} and {E}' or 'until {E}'; make clear that {N} replaces the usual time limit"
  },
  "meaning": "a special time limit by date window: cases whose {A} falls inside the window from {S} to {E}, with BOTH end dates included, have the time limit {N}, which replaces the usual time limit for them",
  "slots": {
   "A": "the name of one date of the case, e.g. 'delivery date'",
   "S": "the first date of the window, e.g. '5 March 2026'",
   "E": "the last date of the window, e.g. '19 March 2026'",
   "N": "the time limit: a number of days with its unit, e.g. '14 days'"
  },
  "rules": [
   "8 forms",
   "{A}, {S}, {E}, {N}: each exactly once",
   "one line, capital first letter, no period at the end"
  ]
 }
]
