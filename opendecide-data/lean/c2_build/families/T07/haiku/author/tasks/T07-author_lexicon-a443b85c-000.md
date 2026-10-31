# T07 authoring task T07-author_lexicon-a443b85c-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_lexicon-a443b85c-000.json

Task kind: author_lexicon; items: 8; outputs expected: 48.

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write SMALL-PRINT SENTENCES. Each item states one exact meaning, the placeholder {X} and what {X} stands for;
write the number of different sentences it asks for, all with exactly that meaning. Each sentence must work on its own
as one sentence of an advertisement's small print, directly after the symbol *.

Hard rules (a sentence that breaks one is thrown away):
1. Exactly one placeholder {X}, spelled exactly so; no other placeholder and no real value in its place.
2. One sentence: a capital letter (or {X}) first, a full stop at the end, no other full stop, 2-14 words.
3. The meaning must be unmistakable to any careful reader, exactly at the edge case the item names.
4. No digits, number words, names, hedges (about, around, roughly, nearly, almost, approximately, maybe).
5. No negation: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out. Exclusion verbs (excludes, excluded) and the word "only" are fine.
6. No word that adds, joins or flips a condition: unless, except, either, otherwise, but, if, when, whenever, while.
   The word "or" only inside an inclusive comparison (or more, or higher, or lower, on or before, on or after).
7. Talk only about the item's subject: delivery-region sentences mention delivery or shipping (where the order is
   delivered, never a billing address); product-category sentences use the word "category"; price-status sentences
   describe items by their status (never the word "category"); date sentences say when the order is placed (never a
   delivery date); amount sentences talk about the order subtotal or the order amount (never a total, a discount, a
   coupon, tax or a shipping cost); membership sentences talk about members or the membership level.
8. Date sentences never use: until, till, through, after (except "on or after"), from (except "from {X} onward"),
   starting, beginning, ends, expires, within, between, up to.
9. All sentences in your answer differ clearly; do not copy the example.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "forms": ["<sentence 1>", "<sentence 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qfe03caec89",
  "brief": {
   "how_many": 6,
   "style": "terse small-print style, like a printed footnote",
   "x_stands_for": "an amount of money (such as '$50.00')",
   "example": "Valid on orders over {X}."
  },
  "meaning": "the order subtotal must be strictly greater than the named amount; edge case: a subtotal EQUAL to {X} is OUTSIDE (it must be strictly more)",
  "slots": {
   "X": "an amount of money (such as '$50.00')"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop"
  ]
 },
 {
  "qid": "qf28777d7b3",
  "brief": {
   "how_many": 6,
   "style": "a fuller plain-English sentence",
   "x_stands_for": "an amount of money (such as '$50.00')",
   "example": "Minimum order subtotal: {X}."
  },
  "meaning": "the order subtotal must be at least the named amount; edge case: a subtotal EQUAL to {X} is INSIDE (it counts)",
  "slots": {
   "X": "an amount of money (such as '$50.00')"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop"
  ]
 },
 {
  "qid": "q959979e589",
  "brief": {
   "how_many": 6,
   "style": "terse small-print style, like a printed footnote",
   "x_stands_for": "an amount of money (such as '$50.00')",
   "example": "Valid on orders of {X} or more."
  },
  "meaning": "the order subtotal must be at least the named amount; edge case: a subtotal EQUAL to {X} is INSIDE (it counts)",
  "slots": {
   "X": "an amount of money (such as '$50.00')"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop"
  ]
 },
 {
  "qid": "q9d8d8782b3",
  "brief": {
   "how_many": 6,
   "style": "a fuller plain-English sentence",
   "x_stands_for": "an amount of money (such as '$50.00')",
   "example": "The order subtotal must be above {X}."
  },
  "meaning": "the order subtotal must be strictly greater than the named amount; edge case: a subtotal EQUAL to {X} is OUTSIDE (it must be strictly more)",
  "slots": {
   "X": "an amount of money (such as '$50.00')"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop"
  ]
 },
 {
  "qid": "qea3b71b7e7",
  "brief": {
   "how_many": 6,
   "style": "terse small-print style, like a printed footnote",
   "x_stands_for": "a membership level name (such as 'Gold'); levels are ranked lowest to highest",
   "example": "For {X} members and below."
  },
  "meaning": "the customer's membership level must be the named level or a lower one; edge case: a member AT level {X} is INSIDE; lower levels are inside; higher levels are outside",
  "slots": {
   "X": "a membership level name (such as 'Gold'); levels are ranked lowest to highest"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop"
  ]
 },
 {
  "qid": "q61d89ae8b5",
  "brief": {
   "how_many": 6,
   "style": "a fuller plain-English sentence",
   "x_stands_for": "a membership level name (such as 'Gold'); levels are ranked lowest to highest",
   "example": "Members at the {X} level or lower only."
  },
  "meaning": "the customer's membership level must be the named level or a lower one; edge case: a member AT level {X} is INSIDE; lower levels are inside; higher levels are outside",
  "slots": {
   "X": "a membership level name (such as 'Gold'); levels are ranked lowest to highest"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop"
  ]
 },
 {
  "qid": "q1e7801101e",
  "brief": {
   "how_many": 6,
   "style": "a fuller plain-English sentence",
   "x_stands_for": "a membership level name (such as 'Gold'); levels are ranked lowest to highest",
   "example": "Members at the {X} level or higher only."
  },
  "meaning": "the customer's membership level must be the named level or a higher one; edge case: a member AT level {X} is INSIDE; higher levels are inside; lower levels are outside",
  "slots": {
   "X": "a membership level name (such as 'Gold'); levels are ranked lowest to highest"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop"
  ]
 },
 {
  "qid": "q1067b68ab9",
  "brief": {
   "how_many": 6,
   "style": "terse small-print style, like a printed footnote",
   "x_stands_for": "a membership level name (such as 'Gold'); levels are ranked lowest to highest",
   "example": "For {X} members and above."
  },
  "meaning": "the customer's membership level must be the named level or a higher one; edge case: a member AT level {X} is INSIDE; higher levels are inside; lower levels are outside",
  "slots": {
   "X": "a membership level name (such as 'Gold'); levels are ranked lowest to highest"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop"
  ]
 }
]
