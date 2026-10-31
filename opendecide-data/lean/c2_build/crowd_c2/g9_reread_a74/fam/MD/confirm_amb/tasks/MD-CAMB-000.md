# G9 re-read confirmation (Opus, ambiguous flags) MD-CAMB-000 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread_a74/fam/MD/confirm_amb/answers/MD-CAMB-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 1. Answers expected: 1 (one per item, each with that item's qid).

## Instructions

A first reader flagged each item below as wrong_gold or ambiguous (their flag and reason are shown as first_flag / first_reason). Re-judge each item yourself from the text, definitions and question alone, without deferring to the first reader. program_answer is the dataset program's answer.
- gold_ok: program_answer is correct and no other answer is defensible;
- wrong_gold: program_answer is wrong;
- ambiguous: two answers are defensible, or the item does not settle the answer.
You only flag. Never propose a new label. Give a short reason (at most 25 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "gold_ok" | "wrong_gold" | "ambiguous", "reason": "<at most 25 words>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "aid": "a0026",
  "kind": "yes/no",
  "text": "Wellington is a city in New Zealand.",
  "question": "Does Wellington (New Zealand) have more than 300,000 inhabitants?",
  "program_answer": "yes",
  "first_flag": "ambiguous",
  "first_reason": "Wellington city has about 210k; urban or regional figures exceed 300k. Depends on definition."
 }
]
