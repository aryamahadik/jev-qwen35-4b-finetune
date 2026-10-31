# G9 re-read confirmation (Opus, ambiguous flags) MD-CAMB-000 (family MD)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/fam/MD/confirm_amb/answers/MD-CAMB-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 7. Answers expected: 7 (one per item, each with that item's qid).

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
  "aid": "a0001",
  "kind": "choice",
  "text": "Accession number: 1942.927.b\nObject type: Print\nCollection: DR - French\nTechnique: intaglio print (photo gravure?)\nCulture: France, early 20th Century\nDate text: 1900\nDate range: 1900 to 1900\nMeasurements: not listed\nCredit line, first word: The",
  "question": "Which curatorial department holds the work?",
  "options": [
   "Medieval Art",
   "Chinese Art",
   "Japanese Art",
   "Drawings",
   "Photography",
   "Greek and Roman Art",
   "Prints",
   "Textiles"
  ],
  "program_answer": "Drawings",
  "first_flag": "ambiguous",
  "first_reason": "Object type is Print (intaglio) but collection code DR suggests Drawings; Prints is also defensible."
 },
 {
  "aid": "a0004",
  "kind": "yes/no",
  "text": "Release-group record\n{\n  \"release_group_id\": \"1de05037-cf52-4ab4-8c96-194b18ad1539\",\n  \"primary_type\": \"Broadcast\",\n  \"credits\": 1,\n  \"releases\": 1,\n  \"tags\": \"none\"\n}",
  "question": "Is it the case that the genre tag does not omit include 'rock'?",
  "program_answer": "no",
  "first_flag": "ambiguous",
  "first_reason": "Garbled double-negative wording; tags are none, so the intended polarity is unclear."
 },
 {
  "aid": "a0022",
  "kind": "yes/no",
  "text": "Jijiang is a city in China.",
  "question": "Do more than 130,000 people live in Jijiang (China)?",
  "program_answer": "yes",
  "first_flag": "ambiguous",
  "first_reason": "Population of Jijiang is not given and not clearly known to exceed 130,000."
 },
 {
  "aid": "a0026",
  "kind": "yes/no",
  "text": "Organization: Alcontrol Laboratories (Norway)\nCountry: Norway",
  "question": "Was Alcontrol Laboratories (Norway) (Norway) established before 1990?",
  "program_answer": "no",
  "first_flag": "ambiguous",
  "first_reason": "Founding year of Alcontrol Norway is not given; answer is not settled by the item."
 },
 {
  "aid": "a0034",
  "kind": "choice",
  "text": "Taxon: Isochona",
  "question": "Which kingdom is the taxon Isochona placed in?",
  "options": [
   "Protozoa",
   "Chromista",
   "Fungi",
   "Archaea"
  ],
  "program_answer": "Chromista",
  "first_flag": "ambiguous",
  "first_reason": "Isochona is not clearly placed in one of these kingdoms; item does not settle it."
 },
 {
  "aid": "a0049",
  "kind": "choice",
  "text": "Organization: HR Wallingford\nCountry: United Kingdom",
  "question": "What type of organization is HR Wallingford (United Kingdom)?",
  "options": [
   "company",
   "nonprofit",
   "facility",
   "archive"
  ],
  "program_answer": "facility",
  "first_flag": "ambiguous",
  "first_reason": "HR Wallingford could be typed company, facility or nonprofit; item does not settle it."
 },
 {
  "aid": "a0050",
  "kind": "choice",
  "text": "Organization: Open Group\nCountry: France",
  "question": "Which type does the registry give for Open Group (France)?",
  "options": [
   "company",
   "government",
   "education",
   "other"
  ],
  "program_answer": "other",
  "first_flag": "ambiguous",
  "first_reason": "Text gives no registry type; Open Group is a consortium, so company or other are both defensible. Item does not settle it."
 }
]
