# T12 REDO-2 authoring task T12-author_lexicon-deaaa5ce-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/redo2/author/answers/T12-author_lexicon-deaaa5ce-000.json

Task kind: author_lexicon; items: 2; outputs expected: 24 (12 per item, answer field "texts").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You write short operator phrases for a synthetic training dataset. Setting: in an accounts-payable (AP) team, a clerk matches a supplier's invoice against the purchase order (PO) and the goods receipt under a written company policy. A program builds every example: it prints the documents, the policy and the question, and it fills every value. Everything you write must be invented: never copy text from real companies, products, people, laws, websites or published datasets. A program inserts each phrase into one fixed sentence of the policy card: the price condition of a card whose bound is a percentage of the PO unit price, 'invoiced unit price minus PO unit price is ___ of the PO unit price on every line'. The {X} in your phrase is filled with that percentage, like '3 percent'. Two independent readers will later be asked what each phrase means, and a phrase is kept only if both readers pick the meaning you were given, so every phrase must have exactly one clear reading. The program already uses the phrases listed under EXISTING PHRASES (most of them for amounts of money); yours must be new phrases made for a percentage: each one names the part of the PO unit price with one of the nouns share, fraction, portion or proportion. Each item asks for 12 different phrases in the answer field "texts".

RULES (every item):
R1. Each phrase is one line with no line break, in lower case.
R2. The 12 phrases of an item differ from each other, and not only in letter case, punctuation, an article (a, an, the) or the word 'any'.
R3. Write only what the item asks; add no example values, no names and no digits.
R4. Each phrase contains exactly one of the nouns share, fraction, portion or proportion (singular), naming the part of the PO unit price that the difference is; across the 12 phrases of an item use at least three of these four nouns.
R5. Never write the words percent, percentage or per cent, and no percent sign: the value filled into {X} already ends with the word percent.
R6. Never end a phrase with 'of', and never write the words PO, price, unit, line or every: the sentence goes on with 'of the PO unit price on every line'.

EXISTING PHRASES (never write one of these, and never one of these with only an article (a, an, the) or the word 'any' added or taken away):
- at or below {X}
- equal to or below {X}
- equal to or less than {X}
- less than or equal to {X}
- no more than {X}
- not more than {X}
- up to and including {X}
- at most {X}
- {X} or less
- {X} or lower
- less than {X}
- below {X}
- lower than {X}
- smaller than {X}
- falling short of {X}
- beneath {X}
- short of {X}
- any amount smaller than {X}
- strictly lower than {X}
- strictly beneath {X}
- any share smaller than {X}

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", "<answer field>": ...}. Copy each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner double quote as \" and a line break inside a text as \n); no comments, no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "texts": [...]}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q279e622ab6",
  "brief": "Write 12 different phrases that each mean: less than or equal to the bound {X}, where {X} is a percentage, filled like '3 percent'. A phrase replaces ___ in 'invoiced unit price minus PO unit price is ___ of the PO unit price on every line' and must read naturally there; it names the part of the PO unit price with one of the nouns share, fraction, portion or proportion. Answer field: \"texts\" (a list of 12 phrases, each containing {X} exactly once).",
  "meaning": "less than or equal to the bound",
  "slots": {
   "X": "a percentage, filled like '3 percent'"
  },
  "rules": [
   "Use {X} exactly once, spelled exactly like that; no other placeholder or curly brace.",
   "2-8 words besides {X}; lower case; no digits; no punctuation except a hyphen.",
   "State the endpoint plainly: a share exactly equal to {X} must clearly count as meeting the condition (comparison styles such as 'at most', 'or less', 'or smaller', 'no more than', 'equal to or less than', always joined to the noun).",
   "A noun next to {X} with no comparison word (styles like 'a share of {X}' or 'a fraction of {X}') states no endpoint and is not allowed: every phrase holds one comparison word or phrase.",
   "Vary the comparison words as well as the noun: no comparison wording (such as 'at most' or 'or less') in more than three of your 12 phrases.",
   "Never use the words within, under, over, beyond, exceed, exceeds, exceeding, limit, cap, capped, maximum, minimum, max, min, ceiling, allowed, permitted or range, and never 'up to' unless it is followed by 'and including'.",
   "No negation word (no, not, none, never, nothing, without), except inside the comparator phrases 'no more than' and 'not more than'; so never 'no larger', 'no greater', 'no bigger' or 'not above'.",
   "Never start the phrase with 'is'; the sentence already holds it."
  ]
 },
 {
  "qid": "qf8377cdc5b",
  "brief": "Write 12 different phrases that each mean: strictly less than the bound {X}, where {X} is a percentage, filled like '3 percent'. A phrase replaces ___ in 'invoiced unit price minus PO unit price is ___ of the PO unit price on every line' and must read naturally there; it names the part of the PO unit price with one of the nouns share, fraction, portion or proportion. Answer field: \"texts\" (a list of 12 phrases, each containing {X} exactly once).",
  "meaning": "strictly less than the bound",
  "slots": {
   "X": "a percentage, filled like '3 percent'"
  },
  "rules": [
   "Use {X} exactly once, spelled exactly like that; no other placeholder or curly brace.",
   "2-8 words besides {X}; lower case; no digits; no punctuation except a hyphen.",
   "State the endpoint plainly: a share exactly equal to {X} must clearly NOT meet the condition (comparison styles such as 'less than', 'smaller than', 'below', 'lower than', 'strictly less than', always joined to the noun).",
   "A noun next to {X} with no comparison word (styles like 'a share of {X}' or 'a fraction of {X}') states no endpoint and is not allowed: every phrase holds one comparison word or phrase.",
   "Vary the comparison words as well as the noun: no comparison wording (such as 'less than' or 'below') in more than three of your 12 phrases.",
   "Never use the words within, under, over, beyond, exceed, exceeds, exceeding, limit, cap, capped, maximum, minimum, max, min, ceiling, allowed, permitted or range, and never 'up to' unless it is followed by 'and including'.",
   "No negation word at all (no, not, none, never, nothing, without); so never 'not as large as', 'no larger' or 'not reaching'.",
   "Never start the phrase with 'is'; the sentence already holds it."
  ]
 }
]
