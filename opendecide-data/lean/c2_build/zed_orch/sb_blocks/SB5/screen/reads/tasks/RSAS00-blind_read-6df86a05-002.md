# A46 replay label-noise blind read RSAS00-blind_read-6df86a05-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/sb_blocks/SB5/screen/reads/answers/RSAS00-blind_read-6df86a05-002.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
If an item truly cannot be settled from its text and definitions (the needed information is missing, or the question has no single defensible answer), answer exactly "abstain" instead. Use it rarely; a hard item that you can still reason out is not a reason to abstain.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no | abstain, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "qe40f0a9725",
  "kind": "yes/no",
  "text": "شو هالغباء فضحتنا",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4309e2a369",
  "kind": "yes/no",
  "text": "اقترح تحويلهم الى طبيب نفسي و ليس الى القضاء",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qefd5dc6743",
  "kind": "yes/no",
  "text": "يا الله ارحم عبدك الفقير المسكين وجميع المسلمين والمسلمات",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qc02508d7d1",
  "kind": "yes/no",
  "text": "الله اكبر على كل ظالم",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4adec73688",
  "kind": "yes/no",
  "text": "اللهم اعنا على فعل الخيرات",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q98e3059369",
  "kind": "yes/no",
  "text": "اللهم اكرمنا برضاك",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qcde598a1b1",
  "kind": "yes/no",
  "text": "ربنا يعنا علي كل شيء",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qb83c20a2b8",
  "kind": "yes/no",
  "text": "كلمات حلو",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q6675fd7564",
  "kind": "yes/no",
  "text": "وماذا عن التفاؤل في يوم ربيعي جميل نحقق به الامال الطوال",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qf617880aef",
  "kind": "yes/no",
  "text": "انا مع الاخ محمد سلامة بهالموضوع",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q9cb3e3ca5a",
  "kind": "yes/no",
  "text": "ثقيلين دم كثير",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qfa82f405f6",
  "kind": "yes/no",
  "text": "اللهم اكفني بحلالك عن حرامك واغنني بفضلك عمن سواك يا رب",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q809bc39687",
  "kind": "yes/no",
  "text": "بصمات راقية لأديب الدعوة محمد الغزالي",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qa14452a0f0",
  "kind": "yes/no",
  "text": "الى يقارن بينه وبين مرسى يبقى متخلف",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qfc518cf164",
  "kind": "yes/no",
  "text": "شو هيدا دلع اخر زمن",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q14d36ac1ed",
  "kind": "yes/no",
  "text": "حلوه عدوله احس انه يفطر حشيش",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qfc8fdbe542",
  "kind": "yes/no",
  "text": "تكالبت عليه الكلاب ولم تسمح له بالبروز بعد البرنامج",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q73e59535eb",
  "kind": "yes/no",
  "text": "فدمك عود مع عنبر",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qb26cfedfdf",
  "kind": "yes/no",
  "text": "ما ارحمك يا ربى بخلقك سبحانك يا حبيبى يا الله",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qfbcf8767dd",
  "kind": "yes/no",
  "text": "اشهد الله اني احبك فى الله و ادعوا ان نحشر مع حبيبنا و امامنا محمد صلى الله عليه و سلم فى الجنة امين",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q377b0b29f6",
  "kind": "yes/no",
  "text": "شو بدو بهالسّحنه",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qa540ca5623",
  "kind": "yes/no",
  "text": "اظن انهم حبو وانجرحوا وضاعت عقولهم وما دخل قلوبهم الا اغاني الجروح عشان كذا حافظينها وجايين يقولونها .. اللهم لاشماته",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q2ed3abd293",
  "kind": "yes/no",
  "text": "حسبنا الله و نعم الوكيل فيكوا",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qedeac123f0",
  "kind": "yes/no",
  "text": "يا مقلب القلوب ثبت قلوبنا على الاسلام",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qcf3a5560f1",
  "kind": "yes/no",
  "text": "لجنة فاشله تتمسخر على المتقدمين",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q9626f16aba",
  "kind": "yes/no",
  "text": "بتقول كلام دي الفل",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q6f72429d2f",
  "kind": "yes/no",
  "text": "ومن احسن قولاممن دعاالي وعمل صالحاووقال انني من المسلمين،",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q37d98c7fa8",
  "kind": "yes/no",
  "text": "جد اشي بخزي!!",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q97585ff1eb",
  "kind": "yes/no",
  "text": "طبعا واقع",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q8d2fbd780d",
  "kind": "yes/no",
  "text": "كلامك يشعرني بالتفاؤل ... و يمدني بالقوة و الاستمرار",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qda0f6dd849",
  "kind": "yes/no",
  "text": "والله نفسى بس الواحد بيجى علية فترات ينسى يعمل اية بجد",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q9f6fd6551c",
  "kind": "yes/no",
  "text": "والله صحيح",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q9055ce0fa6",
  "kind": "yes/no",
  "text": "هذا هو الدين",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q5c22fcfff0",
  "kind": "yes/no",
  "text": "حسبنا الله و نعم الوكيل في اناس همهم تجويع الشعب",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q35e318d26c",
  "kind": "yes/no",
  "text": "كتكوت ضعيف الجناح و الدنيا غدرت هااا",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q93470151fe",
  "kind": "yes/no",
  "text": "التشائم يقتل الحياة",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qb2fafe76e1",
  "kind": "yes/no",
  "text": "قلولهم هذا سوبر ستار مش مسابقة لبياع الخضار",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qdaf6954961",
  "kind": "yes/no",
  "text": "وانا مع انو الطاقة الشمسية هي البديل!",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qc2a6ba4094",
  "kind": "yes/no",
  "text": "لا وحده مع القران هو انيسي ام الغرام فلا احتاجه مطلقا",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q785cc0e243",
  "kind": "yes/no",
  "text": "يااااااااااا الله ما احلاه من خبر والله فرحتوني",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qb767c647b4",
  "kind": "yes/no",
  "text": "مش طبيعي",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q8cdfb4895f",
  "kind": "yes/no",
  "text": "و هكذا جنت على نفسها براقش",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qe0d322a853",
  "kind": "yes/no",
  "text": "ربنايحفظك ياشيخ",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4cc4f8e853",
  "kind": "yes/no",
  "text": "وعلي الله قصد السبيل",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qb2daef9505",
  "kind": "yes/no",
  "text": "اللهم انصر الإسلام وأعز المسلمين",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q70967dd315",
  "kind": "yes/no",
  "text": "ما اروع برنامج الطريق الى الله",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q35ecfa6385",
  "kind": "yes/no",
  "text": "اللهم ارزقنا الصدق و الاخلاص",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qb5d49c97dc",
  "kind": "yes/no",
  "text": "يا طيب صباحك كل خيرات",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q143ecae461",
  "kind": "yes/no",
  "text": "يارب يقدرنا على ادخال المياه النظيفة لكل بيت محتاجة المياه",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q3bb1cbbdcf",
  "kind": "yes/no",
  "text": "بدي اروح عمرة الله ييسر",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 }
]
