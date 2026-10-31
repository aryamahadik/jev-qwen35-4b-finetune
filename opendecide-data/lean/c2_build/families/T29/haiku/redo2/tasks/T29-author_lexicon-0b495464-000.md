# T29 redo2 authoring task T29-author_lexicon-0b495464-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/redo2/answers/T29-author_lexicon-0b495464-000.json

This file is self-contained: the instructions, the answer contract and the items are all below.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 2 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "forms". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: qb7d1dbae88, qc46e59bb23.
- "forms": a JSON array of exactly 12 strings, all different.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one; replace the angle brackets with your own text):
[{"qid": "qb7d1dbae88", "forms": ["<first>", "<second>", ...]}, ...]

Task kind: author_lexicon; items: 2; outputs expected: 24.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write COMPARATOR FORMS: short phrases that a program inserts into a policy rule, where {X} stands for a bound
with its unit (for example '200 records'). Each item states the exact meaning, the frame the form must fit and the
forms already taken; write the number of NEW forms it asks for, all with exactly that meaning, each reading naturally
in the frame. Write the whole form in lowercase (it sits inside a sentence).

Hard rules (a form that breaks one is thrown away):
1. Keep every placeholder the item lists exactly once, spelled exactly so with its curly braces; add no other
   placeholder; never put "a" or "an" directly before a placeholder.
2. The meaning must be unmistakable to any careful reader, including at the edge case the item names.
3. Never repeat a form from the item's "taken" list (those already exist), not even with other capitals, spacing or
   punctuation. All forms in your answer are distinct.
4. No digits and none of these number words: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero.
5. None of these time words, in any sense: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet.
6. No hedges: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure. No double quote characters.
7. A capital letter only on the first word (and the word I); no names of people, teams, products or places.
8. Follow the item's own "rules" list exactly. No form adds a condition, an exception or a second idea.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "forms": ["<form 1>", "<form 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qb7d1dbae88",
  "brief": {
   "how_many": 12,
   "frames": [
    "the call affects ___ (with {X} = '200 records')"
   ],
   "avoid": "phrases whose edge reading is unclear: up to, within, around, about, upwards of, in the region of, close to",
   "taken": [
    "a count greater than {X}",
    "a count of at least {X}",
    "a number equal to or greater than {X}",
    "a number greater than {X}",
    "a total equal to or more than {X}",
    "a total exceeding {X}",
    "a total greater than {X}",
    "a total of at least {X}",
    "a total of more than {X}",
    "a total of {X} or more",
    "above {X}",
    "at least as large as {X}",
    "at least {X}",
    "equal to or greater than {X}",
    "equal to or more than {X}",
    "exceeding {X}",
    "greater than or equal to {X}",
    "greater than {X}",
    "higher than {X}",
    "in excess of {X}",
    "more than {X}",
    "no fewer than {X}",
    "no less than {X}",
    "not less than {X}",
    "over {X}",
    "strictly above {X}",
    "strictly greater than {X}",
    "strictly more than {X}",
    "strictly over {X}",
    "surpassing {X}",
    "{X} or greater",
    "{X} or higher",
    "{X} or more"
   ]
  },
  "meaning": "{X} or more: a value equal to {X} DOES meet it",
  "slots": {
   "X": "the bound with its unit (a number of records)"
  },
  "rules": [
   "12 new forms",
   "{X} exactly once",
   "each form reads naturally in the frame",
   "none equal to a taken form"
  ]
 },
 {
  "qid": "qc46e59bb23",
  "brief": {
   "how_many": 12,
   "frames": [
    "the call affects ___ (with {X} = '200 records')"
   ],
   "avoid": "phrases whose edge reading is unclear: up to, within, around, about, upwards of, in the region of, close to",
   "taken": [
    "a count greater than {X}",
    "a count of at least {X}",
    "a number equal to or greater than {X}",
    "a number greater than {X}",
    "a total equal to or more than {X}",
    "a total exceeding {X}",
    "a total greater than {X}",
    "a total of at least {X}",
    "a total of more than {X}",
    "a total of {X} or more",
    "above {X}",
    "at least as large as {X}",
    "at least {X}",
    "equal to or greater than {X}",
    "equal to or more than {X}",
    "exceeding {X}",
    "greater than or equal to {X}",
    "greater than {X}",
    "higher than {X}",
    "in excess of {X}",
    "more than {X}",
    "no fewer than {X}",
    "no less than {X}",
    "not less than {X}",
    "over {X}",
    "strictly above {X}",
    "strictly greater than {X}",
    "strictly more than {X}",
    "strictly over {X}",
    "surpassing {X}",
    "{X} or greater",
    "{X} or higher",
    "{X} or more"
   ]
  },
  "meaning": "strictly more than {X}: a value equal to {X} does NOT meet it",
  "slots": {
   "X": "the bound with its unit (a number of records)"
  },
  "rules": [
   "12 new forms",
   "{X} exactly once",
   "each form reads naturally in the frame",
   "none equal to a taken form"
  ]
 }
]
