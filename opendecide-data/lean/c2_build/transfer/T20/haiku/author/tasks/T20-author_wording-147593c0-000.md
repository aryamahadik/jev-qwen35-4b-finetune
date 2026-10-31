# T20 authoring task T20-author_wording-147593c0-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/haiku/author/answers/T20-author_wording-147593c0-000.json

Task kind: author_wording; items: 6; outputs expected: 36 (6 per item, answer field "texts").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You write question lines for a synthetic dataset. Setting: an operations group logs incidents. A reader sees an incident record (it has an opening time, maybe an acknowledgement time, and a check time) and a card of rules that sets the incident's level on a scale of four named levels, from the most severe to the least severe; the card says that an incident reaches a level when it is at that level or a more severe one. Your question is shown after the card. The placeholder {INC_ID} stands for the incident's id; {LEVEL} and {LEVEL_NEXT} each stand for the name of one level. You never see the card, the record or the answer, and you never answer the question. Each item says exactly what its questions must ask; two independent readers must recover that meaning and a program counts negation words, so write precise, unambiguous questions. Each item asks for 6 questions in the answer field "texts".

RULES (every item):
R1. Each question is one sentence on one line, ends with a question mark and has at most 30 words.
R2. Use each placeholder the item lists exactly once, spelled exactly with its curly braces, and no other placeholder or curly brace; write {INC_ID} right after the word incident ("incident {INC_ID}").
R3. Name the time with exactly "at the check time" or "as of the check time" (never "by the check time").
R4. No digit or number word (one, two, first, second, four ...), no hedge (maybe, probably, likely, seem, think), no name, and no capitalised word except the first word. Never write a level name yourself: levels appear only through the placeholders.
R5. Never use these words: exactly, only, just, precisely, ever, eventually, final, finally, still, yet, already, now, currently, expected, target, goal, supposed, should.
R6. Never hint at the answer, and never mention answer options, letters or a list to choose from.
R7. The 6 questions of an item differ in structure and wording, not only in one or two words.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", "<answer field>": ...}. Copy each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner double quote as \" and a line break inside a text as \n); no comments, no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "texts": [...]}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q5fb6b75352",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} is at {LEVEL_NEXT} or less severe at the check time. Keep the exact words \"{LEVEL_NEXT} or less severe\". Never use the verb reach. Style for this item: framed as a question from a new on-call engineer. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL_NEXT": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID}, {LEVEL_NEXT} exactly once each"
  ]
 },
 {
  "qid": "q70919a4d79",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} does not reach {LEVEL} at the check time (yes means it stays less severe than {LEVEL}). Use the verb reach with {LEVEL} as its object. Style for this item: framed as a question from a new on-call engineer. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Exactly one negation word, not or n't, and it negates reach (\"does not reach\", \"doesn't reach\"); no other negation word, and never the word fail.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 },
 {
  "qid": "q27b1a9a40a",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} does not reach {LEVEL} at the check time (yes means it stays less severe than {LEVEL}). Use the verb reach with {LEVEL} as its object. Style for this item: short and direct. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Exactly one negation word, not or n't, and it negates reach (\"does not reach\", \"doesn't reach\"); no other negation word, and never the word fail.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 },
 {
  "qid": "q1b2cd376f0",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} is at {LEVEL_NEXT} or less severe at the check time. Keep the exact words \"{LEVEL_NEXT} or less severe\". Never use the verb reach. Style for this item: short and direct. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL_NEXT": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID}, {LEVEL_NEXT} exactly once each"
  ]
 },
 {
  "qid": "q2fe203a7f3",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} fails to reach {LEVEL} at the check time (yes means it stays less severe than {LEVEL}). Write \"fail to reach {LEVEL}\" or \"fails to reach {LEVEL}\" exactly once. Never mention an expected, intended, planned or required level. Style for this item: short and direct. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "No other negation word: no not, n't, no, never, none, without.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 },
 {
  "qid": "qd605eb946c",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} fails to reach {LEVEL} at the check time (yes means it stays less severe than {LEVEL}). Write \"fail to reach {LEVEL}\" or \"fails to reach {LEVEL}\" exactly once. Never mention an expected, intended, planned or required level. Style for this item: framed as a question from a new on-call engineer. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "No other negation word: no not, n't, no, never, none, without.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 }
]
