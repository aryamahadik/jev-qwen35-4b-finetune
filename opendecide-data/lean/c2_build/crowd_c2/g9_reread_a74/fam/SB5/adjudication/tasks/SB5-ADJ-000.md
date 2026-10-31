# G9 re-read adjudication (flag only) SB5-ADJ-000 (family SB5)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/crowd_c2/g9_reread_a74/fam/SB5/adjudication/answers/SB5-ADJ-000.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 18. Answers expected: 18 (one per item, each with that item's qid).

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
  "aid": "a0000",
  "kind": "yes/no",
  "text": "يارب كون معاي .وإنو من ترك شيئآ لله عوضه الله خيرآ منها في الدنيا قبل الآخره جربو وحتشوفوا بعينكم إللي حيحصل",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0001",
  "kind": "yes/no",
  "text": "فعلا والله هو القرار والثبات عليه",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0002",
  "kind": "yes/no",
  "text": "شو هالغباء فضحتنا",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0003",
  "kind": "yes/no",
  "text": "حيوان وكلب الله يموتك",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0004",
  "kind": "yes/no",
  "text": "هذا هو الحب الاصيل الوفي بكل معنى الوفاء",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0005",
  "kind": "yes/no",
  "text": "ينور عليك..........ويكثر من امثالك",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0006",
  "kind": "yes/no",
  "text": "شو بالا يا دانيا و المشكلة مش عارفه تكتب هعهعه",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0007",
  "kind": "yes/no",
  "text": "إلى إعتصام مفتوح (ميدان تحرير ) للتخلص من قوى الفساد و الإفساد",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0008",
  "kind": "yes/no",
  "text": "الى من اشكوك !",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0009",
  "kind": "yes/no",
  "text": "استغفر الله مجانين يروحون سوبر ستار",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0010",
  "kind": "yes/no",
  "text": "لا حول ولا قوة ألا بالله أذا أخذ ما أوهب أسقط ما أوجب",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0011",
  "kind": "yes/no",
  "text": "يا ارحم الراحمين يا الله",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0012",
  "kind": "yes/no",
  "text": "الله يلعنو",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0013",
  "kind": "yes/no",
  "text": "سد بوزك",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "no"
 },
 {
  "aid": "a0014",
  "kind": "yes/no",
  "text": "نار جهنم تاخدو",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0015",
  "kind": "yes/no",
  "text": "الله يصبحك برضاه",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0016",
  "kind": "yes/no",
  "text": "وانا من الناس اللي فعلا محتاجين يحاسبوا نفسهم ويصلحو من نفسهم لاننا عارفين انه لا ملجأ لنا الا لله",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 },
 {
  "aid": "a0017",
  "kind": "yes/no",
  "text": "لو حد يا جماعة يعرف طبيب اذن يدلني ولا شكلي هارميهم خلاص باظو",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "program_answer": "yes"
 }
]
