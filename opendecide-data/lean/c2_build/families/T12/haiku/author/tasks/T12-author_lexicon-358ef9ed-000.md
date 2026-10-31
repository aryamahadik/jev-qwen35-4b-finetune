# T12 authoring task T12-author_lexicon-358ef9ed-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/author/answers/T12-author_lexicon-358ef9ed-000.json

Task kind: author_lexicon; items: 4; outputs expected: 40 (10 per item, answer field "texts").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You write short operator phrases for a synthetic training dataset. Setting: in an accounts-payable (AP) team, a clerk matches a supplier's invoice against the purchase order (PO) and the goods receipt under a written company policy. A program builds every example: it prints the documents, the policy and the question, and it fills every value. Everything you write must be invented: never copy text from real companies, products, people, laws, websites or published datasets. A program inserts each phrase into fixed sentences of the policy card. Two or three independent readers will later be asked what each phrase means, and a phrase is kept only if every reader picks the meaning you were given, so every phrase must have exactly one clear reading. Each item asks for 10 different phrases in the answer field "texts".

RULES (every item):
R1. Each phrase is one line with no line break, in lower case except where a sentence must start with a capital.
R2. The 10 phrases of an item differ from each other (not only in letter case or punctuation).
R3. Write only what the item asks; add no example values, no names and no digits.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", "<answer field>": ...}. Copy each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner double quote as \" and a line break inside a text as \n); no comments, no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "texts": [...]}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q8b49a0e436",
  "brief": "Write 10 different phrases that each mean: less than or equal to the bound {X}, where {X} is an amount of money, filled like '$0.50' or '0.50 USD'. A phrase replaces ___ in 'invoiced unit price minus PO unit price is ___ on every line' / 'the invoice total is ___ (limit of approver Dana Whitlock)' and must read naturally there. Answer field: \"texts\" (a list of 10 phrases, each containing {X} exactly once).",
  "meaning": "less than or equal to the bound",
  "slots": {
   "X": "an amount of money, filled like '$0.50' or '0.50 USD'"
  },
  "rules": [
   "Use {X} exactly once, spelled exactly like that; no other placeholder or curly brace.",
   "2-8 words; lower case; no digits; no punctuation except a hyphen.",
   "State the endpoint plainly: a value exactly equal to {X} must clearly count as meeting the condition (styles such as 'at most {X}', '{X} or less'). Do not reuse these style examples word for word in more than two of your phrases.",
   "Never use the words within, under, over, beyond, exceed, exceeding, limit, cap, maximum, minimum, ceiling, allowed, permitted or range, and never 'up to' unless it is followed by 'and including'.",
   "No negation word, except the comparator phrases 'no more than' and 'not more than'.",
   "Never start the phrase with 'is'; the sentence already holds it."
  ]
 },
 {
  "qid": "q33dfb824c6",
  "brief": "Write 10 different phrases that each mean: strictly less than the bound {X}, where {X} is an amount of money, filled like '$0.50' or '0.50 USD'. A phrase replaces ___ in 'invoiced unit price minus PO unit price is ___ on every line' / 'the invoice total is ___ (limit of approver Dana Whitlock)' and must read naturally there. Answer field: \"texts\" (a list of 10 phrases, each containing {X} exactly once).",
  "meaning": "strictly less than the bound",
  "slots": {
   "X": "an amount of money, filled like '$0.50' or '0.50 USD'"
  },
  "rules": [
   "Use {X} exactly once, spelled exactly like that; no other placeholder or curly brace.",
   "2-8 words; lower case; no digits; no punctuation except a hyphen.",
   "State the endpoint plainly: a value exactly equal to {X} must clearly NOT meet the condition (styles such as 'less than {X}', 'below {X}'). Do not reuse these style examples word for word in more than two of your phrases.",
   "Never use the words within, under, over, beyond, exceed, exceeding, limit, cap, maximum, minimum, ceiling, allowed, permitted or range, and never 'up to' unless it is followed by 'and including'.",
   "No negation word, except the comparator phrases 'no more than' and 'not more than'.",
   "Never start the phrase with 'is'; the sentence already holds it."
  ]
 },
 {
  "qid": "q3c7cdd21be",
  "brief": "Write 10 different phrases that each mean: less than or equal to the bound {X}, where {X} is a percentage, filled like '3 percent'. A phrase replaces ___ in 'invoiced unit price minus PO unit price is ___ of the PO unit price on every line' and must read naturally there. Answer field: \"texts\" (a list of 10 phrases, each containing {X} exactly once).",
  "meaning": "less than or equal to the bound",
  "slots": {
   "X": "a percentage, filled like '3 percent'"
  },
  "rules": [
   "Use {X} exactly once, spelled exactly like that; no other placeholder or curly brace.",
   "2-8 words; lower case; no digits; no punctuation except a hyphen.",
   "State the endpoint plainly: a value exactly equal to {X} must clearly count as meeting the condition (styles such as 'at most {X}', '{X} or less'). Do not reuse these style examples word for word in more than two of your phrases.",
   "Never use the words within, under, over, beyond, exceed, exceeding, limit, cap, maximum, minimum, ceiling, allowed, permitted or range, and never 'up to' unless it is followed by 'and including'.",
   "No negation word, except the comparator phrases 'no more than' and 'not more than'.",
   "Never start the phrase with 'is'; the sentence already holds it."
  ]
 },
 {
  "qid": "q6491d1dc19",
  "brief": "Write 10 different phrases that each mean: strictly less than the bound {X}, where {X} is a percentage, filled like '3 percent'. A phrase replaces ___ in 'invoiced unit price minus PO unit price is ___ of the PO unit price on every line' and must read naturally there. Answer field: \"texts\" (a list of 10 phrases, each containing {X} exactly once).",
  "meaning": "strictly less than the bound",
  "slots": {
   "X": "a percentage, filled like '3 percent'"
  },
  "rules": [
   "Use {X} exactly once, spelled exactly like that; no other placeholder or curly brace.",
   "2-8 words; lower case; no digits; no punctuation except a hyphen.",
   "State the endpoint plainly: a value exactly equal to {X} must clearly NOT meet the condition (styles such as 'less than {X}', 'below {X}'). Do not reuse these style examples word for word in more than two of your phrases.",
   "Never use the words within, under, over, beyond, exceed, exceeding, limit, cap, maximum, minimum, ceiling, allowed, permitted or range, and never 'up to' unless it is followed by 'and including'.",
   "No negation word, except the comparator phrases 'no more than' and 'not more than'.",
   "Never start the phrase with 'is'; the sentence already holds it."
  ]
 }
]
