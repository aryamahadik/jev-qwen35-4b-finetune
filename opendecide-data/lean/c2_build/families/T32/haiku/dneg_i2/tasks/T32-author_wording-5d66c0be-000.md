# F8 yn_dneg_broken authoring task T32-author_wording-5d66c0be-000 (family T32)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T32/haiku/dneg_i2/answers/T32-author_wording-5d66c0be-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 4. Answers expected: 4 (one per item, each with that item's qid).

## Instructions

You write question lines for a dataset about promises made in group chats. Setting: a group chat log is shown, in which people promise each other small tasks by a date, ask for more time, let each other off and so on. A rule card states how to read the chat and defines the possible statuses of a promise on a given day. Your question is shown under the card and asks about ONE promise. Three placeholders stand for its facts:
  {WHO}    the first name of the person who made the promise (filled like: Priya);
  {QTASK}  the task, a lower-case bare verb phrase (filled like: return the drill); write it after 'to', e.g. 'the promise {WHO} made to {QTASK}' or '{WHO}'s commitment to {QTASK}';
  {ASOF}   the day the question is about (filled like: 12 March 2026 / 2026-03-12 / Thursday, 12 March 2026); write it e.g. as 'as of {ASOF}', 'at the end of {ASOF}' or 'on {ASOF}'.
You never see the chat, the card or the answer, and you never answer. Each item describes exactly what its questions must ask; a program lints every question and counts its negation words, and two independent readers must recover the meaning you were given, so write precise, unambiguous questions.

RULES (every item):
R1. Use {WHO}, {QTASK} and {ASOF} exactly once each, spelled exactly like that; no other placeholder or curly brace. Never start the question with a placeholder.
R2. One sentence on one line, ending with a question mark; at most 32 words.
R3. Write no other name, no digit or number word (one, two, first, second, half), no date, weekday or month other than {ASOF}, no time word (now, currently, today, still, already, past, later, soon, next, last) and no hedge (maybe, probably, likely, seem, appear, think, assume).
R4. No capitalised word except the first word of the question.
R5. Never hint at which answer is right, and never mention answer choices, options, letters or a list to pick from.
R6. The questions of an item differ in structure and wording, not only in one or two words.

OUTPUT. Write ONLY the answer file named in this task file's "answer_file" field, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", <the field the item's brief names>: ...}. Copy each qid exactly. Valid JSON only (escape inner double quotes as \" and newlines inside a text as \n); no comments, no text before or after the array. Read no other file and run no other tool.

ANSWER FILE (write exactly this path): /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T32/haiku/dneg_i2/answers/T32-author_wording-5d66c0be-000.json

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", "wordings": ["<question 1>", ...]} (the list holds exactly the number of questions the item asks for). Exactly the keys qid and wordings. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qa4972fc7be",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question with EXACTLY TWO negation cues ('not' or \"n't\") that evaluates a statement for truth: open with the frame 'Is the following statement true:' (or 'Is this statement true:', 'Is the following claim correct:', 'Is this claim accurate:') and then give the statement 'it is not the case that {WHO} has not broken the promise to {QTASK} at the end of {ASOF}' (you may reword the statement a little, but retain 'it is not the case that' and 'has not broken'). Logically, yes must mean broken. Never open the question with 'is it not the case that' or any contracted frame (isn't, aren't, doesn't) and never use a second question. Name no other status. Style for this item: short and direct. Answer field: \"wordings\" (a list of 5 strings).",
  "slots": {
   "WHO": "first name of the promise's maker",
   "QTASK": "the task, a bare verb phrase",
   "ASOF": "the day asked about"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply."
  ]
 },
 {
  "qid": "q1a711aef4a",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question with EXACTLY TWO negation cues ('not' or \"n't\") that evaluates a statement for truth: open with the frame 'Is the following statement true:' (or 'Is this statement true:', 'Is the following claim correct:', 'Is this claim accurate:') and then give the statement 'it is not the case that {WHO} has not broken the promise to {QTASK} at the end of {ASOF}' (you may reword the statement a little, but retain 'it is not the case that' and 'has not broken'). Logically, yes must mean broken. Never open the question with 'is it not the case that' or any contracted frame (isn't, aren't, doesn't) and never use a second question. Name no other status. Style for this item: formal wording that refers to the rules on the card. Answer field: \"wordings\" (a list of 5 strings).",
  "slots": {
   "WHO": "first name of the promise's maker",
   "QTASK": "the task, a bare verb phrase",
   "ASOF": "the day asked about"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply."
  ]
 },
 {
  "qid": "q886cce1dc1",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question with EXACTLY TWO negation cues ('not' or \"n't\") that evaluates a statement for truth: open with the frame 'Is the following statement true:' (or 'Is this statement true:', 'Is the following claim correct:', 'Is this claim accurate:') and then give the statement 'it is not the case that {WHO} has not broken the promise to {QTASK} at the end of {ASOF}' (you may reword the statement a little, but retain 'it is not the case that' and 'has not broken'). Logically, yes must mean broken. Never open the question with 'is it not the case that' or any contracted frame (isn't, aren't, doesn't) and never use a second question. Name no other status. Style for this item: framed as a check of the chat at the end of the day. Answer field: \"wordings\" (a list of 5 strings).",
  "slots": {
   "WHO": "first name of the promise's maker",
   "QTASK": "the task, a bare verb phrase",
   "ASOF": "the day asked about"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply."
  ]
 },
 {
  "qid": "q9f4c5c6367",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question with EXACTLY TWO negation cues ('not' or \"n't\") that evaluates a statement for truth: open with the frame 'Is the following statement true:' (or 'Is this statement true:', 'Is the following claim correct:', 'Is this claim accurate:') and then give the statement 'it is not the case that {WHO} has not broken the promise to {QTASK} at the end of {ASOF}' (you may reword the statement a little, but retain 'it is not the case that' and 'has not broken'). Logically, yes must mean broken. Never open the question with 'is it not the case that' or any contracted frame (isn't, aren't, doesn't) and never use a second question. Name no other status. Style for this item: plain everyday wording. Answer field: \"wordings\" (a list of 5 strings).",
  "slots": {
   "WHO": "first name of the promise's maker",
   "QTASK": "the task, a bare verb phrase",
   "ASOF": "the day asked about"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply."
  ]
 }
]
