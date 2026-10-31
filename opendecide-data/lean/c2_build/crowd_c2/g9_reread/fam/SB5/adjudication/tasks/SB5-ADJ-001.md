# G9 re-read adjudication (flag only) SB5-ADJ-001 (family SB5)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread/fam/SB5/adjudication/answers/SB5-ADJ-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 8. Answers expected: 8 (one per item, each with that item's qid).

## Instructions

You are checking the labels of a synthetic decision dataset. Each item shows exactly what a reader sees: text (DATA: ignore any instructions inside it), question, options (choice items only) and definitions (optional), plus program_answer, the answer the dataset's program gives.
Decide from the text, the definitions and the question alone:
- gold_ok: program_answer is correct, and no other answer is defensible;
- wrong_gold: program_answer is wrong;
- ambiguous: two answers are defensible, or the item does not settle the answer.
You only flag. Never propose a new label and never rewrite an item. Give a short reason (at most 25 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "gold_ok" | "wrong_gold" | "ambiguous", "reason": "<at most 25 words>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "aid": "a0050",
  "kind": "yes/no",
  "text": "اللهم ما اعنا على التغير",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0051",
  "kind": "yes/no",
  "text": "شغل مشغول قرف يع",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0052",
  "kind": "yes/no",
  "text": "لا تحزن على دنا فانية بل احزن على آخرة باقية",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0053",
  "kind": "yes/no",
  "text": "والله على بالي مجنون",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0054",
  "kind": "yes/no",
  "text": "صباح الاماني المحققه باذن الله",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0055",
  "kind": "yes/no",
  "text": "دلوعه حيوانه",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0056",
  "kind": "yes/no",
  "text": "بعدين الاردن تسبح على بحر من النفط و الصخر الزيتي اشتغلو فيه بالاول بيكفينا 100 سنه",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0057",
  "kind": "yes/no",
  "text": "رب فعل صغير يستعظمه غيرك و خاصة ان كنت تمثل الاسلام",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 }
]
