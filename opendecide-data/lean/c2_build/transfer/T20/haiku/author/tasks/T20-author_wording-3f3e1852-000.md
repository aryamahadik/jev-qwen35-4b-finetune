# T20 authoring task T20-author_wording-3f3e1852-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/transfer/T20/haiku/author/answers/T20-author_wording-3f3e1852-000.json

Task kind: author_wording; items: 10; outputs expected: 60 (6 per item, answer field "texts").

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
  "qid": "qccfd3bb080",
  "brief": "Write 6 questions. Each question must ask which level incident {INC_ID} is at, at the check time, under the card's rules (the reader picks one of the four levels from options shown separately). Use the word level or severity; never use the verb reach; never ask for a starting or base level. Style for this item: formal wording that refers to the card's rules. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID} exactly once each"
  ]
 },
 {
  "qid": "qd6b80ed085",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} reaches {LEVEL} at the check time. Either use the verb reach (reach or reaches) directly followed by {LEVEL}, or write \"{LEVEL} or more severe\". Never ask whether it is at {LEVEL} alone. Style for this item: framed around what the rules give for this incident. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 },
 {
  "qid": "qe5a1aaf6e1",
  "brief": "Write 6 questions. Each question must ask which level incident {INC_ID} is at, at the check time, under the card's rules (the reader picks one of the four levels from options shown separately). Use the word level or severity; never use the verb reach; never ask for a starting or base level. Style for this item: framed as a question from a new on-call engineer. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID} exactly once each"
  ]
 },
 {
  "qid": "q655b5ee8b0",
  "brief": "Write 6 questions. Each question must ask which level incident {INC_ID} is at, at the check time, under the card's rules (the reader picks one of the four levels from options shown separately). Use the word level or severity; never use the verb reach; never ask for a starting or base level. Style for this item: plain everyday wording. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID} exactly once each"
  ]
 },
 {
  "qid": "qb7d149b898",
  "brief": "Write 6 questions. Each question must ask which level incident {INC_ID} is at, at the check time, under the card's rules (the reader picks one of the four levels from options shown separately). Use the word level or severity; never use the verb reach; never ask for a starting or base level. Style for this item: short and direct. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID} exactly once each"
  ]
 },
 {
  "qid": "qb2a6509f82",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} reaches {LEVEL} at the check time. Either use the verb reach (reach or reaches) directly followed by {LEVEL}, or write \"{LEVEL} or more severe\". Never ask whether it is at {LEVEL} alone. Style for this item: short and direct. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 },
 {
  "qid": "q7875ee0ea4",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} reaches {LEVEL} at the check time. Either use the verb reach (reach or reaches) directly followed by {LEVEL}, or write \"{LEVEL} or more severe\". Never ask whether it is at {LEVEL} alone. Style for this item: formal wording that refers to the card's rules. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 },
 {
  "qid": "q5733ff01fe",
  "brief": "Write 6 questions. Each question must ask which level incident {INC_ID} is at, at the check time, under the card's rules (the reader picks one of the four levels from options shown separately). Use the word level or severity; never use the verb reach; never ask for a starting or base level. Style for this item: conversational but exact. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID} exactly once each"
  ]
 },
 {
  "qid": "qfb67d37a56",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} reaches {LEVEL} at the check time. Either use the verb reach (reach or reaches) directly followed by {LEVEL}, or write \"{LEVEL} or more severe\". Never ask whether it is at {LEVEL} alone. Style for this item: conversational but exact. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 },
 {
  "qid": "q0be31d6f0b",
  "brief": "Write 6 questions. Each question must ask, as a yes/no question, whether incident {INC_ID} reaches {LEVEL} at the check time. Either use the verb reach (reach or reaches) directly followed by {LEVEL}, or write \"{LEVEL} or more severe\". Never ask whether it is at {LEVEL} alone. Style for this item: plain everyday wording. Answer field: \"texts\".",
  "slots": {
   "INC_ID": "the incident's id",
   "LEVEL": "the name of one level"
  },
  "rules": [
   "Rules R1-R7 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail, refuse, deny.",
   "use {INC_ID}, {LEVEL} exactly once each"
  ]
 }
]
