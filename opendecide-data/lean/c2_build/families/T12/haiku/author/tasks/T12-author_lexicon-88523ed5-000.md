# T12 authoring task T12-author_lexicon-88523ed5-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/author/answers/T12-author_lexicon-88523ed5-000.json

Task kind: author_lexicon; items: 3; outputs expected: 30 (10 per item, answer field "texts").

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
  "qid": "q02b840ee28",
  "brief": "Write 10 different one-line sentences for the policy card. On the card the sentence comes right after the line 'Check order: price, then quantity.' (that line names the checks in the order they are run) and it states the precedence rule: the checks are taken in the check order, and the first one that fails decides the action; later checks do not change it. Angle for this item: a statement about which check decides the action. Answer field: \"texts\" (a list of 10 sentences).",
  "meaning": "the first check in the stated check order that fails decides the action",
  "slots": {},
  "rules": [
   "Every sentence contains the exact words 'check order' and ends with a full stop.",
   "8-30 words, one line; no placeholder or curly brace; at most one semicolon.",
   "Never name a particular check or action, and never use the words listed, list, above, below, top, bottom, highest, lowest, printed, numbered, severe, serious, important, priority or worst: the order that counts is the check order line, never the position of a check on the card or how serious it is.",
   "The only negation allowed is 'do not' or 'does not' in a clause about later checks ('later checks do not change it').",
   "Never start a sentence with 'Check order' or 'If every check'."
  ]
 },
 {
  "qid": "qab81a588c5",
  "brief": "Write 10 different one-line sentences for the policy card. On the card the sentence comes right after the line 'Check order: price, then quantity.' (that line names the checks in the order they are run) and it states the precedence rule: the checks are taken in the check order, and the first one that fails decides the action; later checks do not change it. Angle for this item: a statement that stresses that later checks do not change the action. Answer field: \"texts\" (a list of 10 sentences).",
  "meaning": "the first check in the stated check order that fails decides the action",
  "slots": {},
  "rules": [
   "Every sentence contains the exact words 'check order' and ends with a full stop.",
   "8-30 words, one line; no placeholder or curly brace; at most one semicolon.",
   "Never name a particular check or action, and never use the words listed, list, above, below, top, bottom, highest, lowest, printed, numbered, severe, serious, important, priority or worst: the order that counts is the check order line, never the position of a check on the card or how serious it is.",
   "The only negation allowed is 'do not' or 'does not' in a clause about later checks ('later checks do not change it').",
   "Never start a sentence with 'Check order' or 'If every check'."
  ]
 },
 {
  "qid": "qdb326d9093",
  "brief": "Write 10 different one-line sentences for the policy card. On the card the sentence comes right after the line 'Check order: price, then quantity.' (that line names the checks in the order they are run) and it states the precedence rule: the checks are taken in the check order, and the first one that fails decides the action; later checks do not change it. Angle for this item: an instruction to the reader (imperative). Answer field: \"texts\" (a list of 10 sentences).",
  "meaning": "the first check in the stated check order that fails decides the action",
  "slots": {},
  "rules": [
   "Every sentence contains the exact words 'check order' and ends with a full stop.",
   "8-30 words, one line; no placeholder or curly brace; at most one semicolon.",
   "Never name a particular check or action, and never use the words listed, list, above, below, top, bottom, highest, lowest, printed, numbered, severe, serious, important, priority or worst: the order that counts is the check order line, never the position of a check on the card or how serious it is.",
   "The only negation allowed is 'do not' or 'does not' in a clause about later checks ('later checks do not change it').",
   "Never start a sentence with 'Check order' or 'If every check'."
  ]
 }
]
