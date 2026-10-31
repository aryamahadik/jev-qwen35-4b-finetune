# G9 re-read confirmation (Opus, wrong_gold flags) MD-CONF-000 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/fam/MD/confirm/answers/MD-CONF-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 5. Answers expected: 5 (one per item, each with that item's qid).

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
  "aid": "a0003",
  "kind": "choice",
  "text": "Organization: Islamic Azad University of Shahreza\nCountry: Iran",
  "question": "In which period was Islamic Azad University of Shahreza (Iran) established?",
  "options": [
   "1950-1999",
   "2000 or later",
   "1900-1949",
   "before 1800"
  ],
  "program_answer": "before 1800",
  "first_flag": "wrong_gold",
  "first_reason": "Islamic Azad University branches were founded in the late 20th century; before 1800 is impossible."
 },
 {
  "aid": "a0005",
  "kind": "choice",
  "text": "Organization: Regional Municipality of Durham\nCountry: Canada",
  "question": "In which period was Regional Municipality of Durham (Canada) established?",
  "options": [
   "2000 or later",
   "1950-1999",
   "before 1800",
   "1800-1899"
  ],
  "program_answer": "before 1800",
  "first_flag": "wrong_gold",
  "first_reason": "Durham Region was established in 1974, not before 1800."
 },
 {
  "aid": "a0007",
  "kind": "choice",
  "text": "Organization: Children's Medical Center\nCountry: Iran",
  "question": "In which period was Children's Medical Center (Iran) established?",
  "options": [
   "2000 or later",
   "1950-1999",
   "before 1800",
   "1800-1899"
  ],
  "program_answer": "before 1800",
  "first_flag": "wrong_gold",
  "first_reason": "Children's Medical Center in Tehran was founded in the 20th century, not before 1800."
 },
 {
  "aid": "a0029",
  "kind": "choice",
  "text": "Organization: Saga Women's Junior College\nCountry: Japan",
  "question": "Which period holds the founding year of Saga Women's Junior College (Japan)?",
  "options": [
   "1950-1999",
   "2000 or later",
   "1900-1949",
   "1800-1899"
  ],
  "program_answer": "1800-1899",
  "first_flag": "wrong_gold",
  "first_reason": "Saga Women's Junior College was founded in the 20th century, not 1800-1899."
 },
 {
  "aid": "a0048",
  "kind": "choice",
  "text": "Organization: Olivet University\nCountry: United States",
  "question": "Which period holds the founding year of Olivet University (United States)?",
  "options": [
   "2000 or later",
   "1950-1999",
   "1900-1949",
   "1800-1899"
  ],
  "program_answer": "2000 or later",
  "first_flag": "wrong_gold",
  "first_reason": "Olivet University was founded in 1938, not 2000 or later."
 }
]
