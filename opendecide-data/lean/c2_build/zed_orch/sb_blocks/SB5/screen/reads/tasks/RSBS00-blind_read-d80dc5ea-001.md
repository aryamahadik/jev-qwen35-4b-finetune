# A46 replay label-noise blind read RSBS00-blind_read-d80dc5ea-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/sb_blocks/SB5/screen/reads/answers/RSBS00-blind_read-d80dc5ea-001.json

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
  "qid": "q9cdb4f41c0",
  "kind": "yes/no",
  "text": "مش عارف كيف الناس بتحبك يا زلمة؟",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qd92e4ab456",
  "kind": "yes/no",
  "text": "نعم الصديق الوفى",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q53adf29677",
  "kind": "yes/no",
  "text": "والله ظلموه لجنة الطراطير",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q2bdb141955",
  "kind": "yes/no",
  "text": "مش طبيعي سماكة الدم شو ها عدولة خرب المفطع لشو المبالغة والاوفر يعني",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q530fba2ffb",
  "kind": "yes/no",
  "text": "تفائلوا بالخير تجدوه",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qfa802124f9",
  "kind": "yes/no",
  "text": "أسأل الله أن يرزقني من يدعو لي في ظهر الغيب",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q76087ec5d8",
  "kind": "yes/no",
  "text": "والشكرلله والفضل لله على هذه النعمه التي انعم الله علينا بها وجعلنا من الماء كل شي حي",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q77d2086a44",
  "kind": "yes/no",
  "text": "الارواح جنود مجنده من تعارف منها أأتلف ومن تنافر منها اختلف",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q3ddb77c3fc",
  "kind": "yes/no",
  "text": "ينور عليك..........ويكثر من امثالك",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q6c30079c3e",
  "kind": "yes/no",
  "text": "اول واحد ذكرنى بصاحب اسمه قردة",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q9335178b75",
  "kind": "yes/no",
  "text": "عنجد هذا الانسان تافه وحقير",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qc04e838664",
  "kind": "yes/no",
  "text": "يعني بكل وضوح بدكوا تذلوا الشعب الأردني و تخلوه كل 4 شهور يصف طابور عشان يوخدلوا اكمن ليرة",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qa79f45177c",
  "kind": "yes/no",
  "text": "شو الاشي الي بيضحك (ما ازنخك)",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q0af4c3afb4",
  "kind": "yes/no",
  "text": "مش حلو",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q5b684f2899",
  "kind": "yes/no",
  "text": "من رافق وافق",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qcd9663fb18",
  "kind": "yes/no",
  "text": "ازا كان حالك احسن من حالو دوس لايك وقول سبحان الله",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q0cdc6e199d",
  "kind": "yes/no",
  "text": "والله انا خايف انو طخوا بعد هاي الصورة",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q35af2b1d98",
  "kind": "yes/no",
  "text": "يارب دعوناك فستجب لنا وحقق لنا ماهو اصلح وافضل لنا",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qe2c066e832",
  "kind": "yes/no",
  "text": "يلعن اخت اليهود اذا بدهم يرجعو شبر من فلسطين ل هاالمنا",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q052cf942ec",
  "kind": "yes/no",
  "text": "و الله مش عارفة شو بدنا نسوي نشحد مثلا",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qa642cf8499",
  "kind": "yes/no",
  "text": "أنوا ا ا ا ا ا ا اع الشماته هالكلبا",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qfeebb3648f",
  "kind": "yes/no",
  "text": "اللهم قوِّ إيماننا لنكون أصحاب عزيمة و قرار",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qb0032d5b26",
  "kind": "yes/no",
  "text": "يا الله عالمواساه يرحم ايام زمان",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q1e857c0ca1",
  "kind": "yes/no",
  "text": "اخذت القرار لكن برجع تانى وخايفه اموت وانا بغضب ربنا سبحانه وتعالى مع انى انا حسه انى قلبى مليان وعامر بنور الله اعمل ايه اجوك انصحنى",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q7b0ef3d8fd",
  "kind": "yes/no",
  "text": "صباح الورد والفل",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qcba8ff0b0f",
  "kind": "yes/no",
  "text": "اللهم اكفني بحلالك عن حرامك واغنني بفضلك عمن سواك يا رب",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q94ba88d726",
  "kind": "yes/no",
  "text": "انا اشوفه انه عادي ولا فيه اي معنى وايش مليوني مشاهد والله انه ما يستحق الى هذا الحد من المشاهده وبعدين هاض شي مقزز",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q09db859ed4",
  "kind": "yes/no",
  "text": "تفائلوا بالخير تجدوه و اعملوا الصالحات",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qefedfaed97",
  "kind": "yes/no",
  "text": "الله ينتقم منهم اجمعين اللي في بالي",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qa5c890e2cd",
  "kind": "yes/no",
  "text": "الله لا يخلف عليهم و لا يكثر خيرهم فعلن شعب مسكين و عبد الله النسور بطل رفع الاسعار",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q796d76b729",
  "kind": "yes/no",
  "text": "واثق من نفسه الحبيب",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qd88a8f8205",
  "kind": "yes/no",
  "text": "وهذه من اكبر المشاكل التي تؤرق الشباب في هذه الايام",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qef2def84f1",
  "kind": "yes/no",
  "text": "كلام صحيح من شان هيك الدول اللي ما فيها بطالة والمجتمعات المفتوحة بتقل فيها المشاكل النفسية",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qf522e7528d",
  "kind": "yes/no",
  "text": "انا دايما فرحان و مش سائل بالدنيا و الحمد لله",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q9e9c878c84",
  "kind": "yes/no",
  "text": "كلام ذهب",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qbee1e3dee2",
  "kind": "yes/no",
  "text": "اطمئن يا قلبى فرزقى لا ياخذة غيرى",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q823522b473",
  "kind": "yes/no",
  "text": "واي ناس فاظيين صج عاااهاات!!",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qcf3e76bd5f",
  "kind": "yes/no",
  "text": "اللهم إنى أقسمت عليك بك أن تهدى شباب المسلمين وتنور قلوبهم كما أنعمت على طارق بنعمة اﻹسﻻم",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q55fdbeb7ce",
  "kind": "yes/no",
  "text": "اتحزن : فإن الله يدافع عنك ، والملائكة تستغفر لك ، و المؤمنون يشركونك في دعائهم كل صلاة ،و النبي صلى الله عليه و سلم يشفع ، و القرآن يعدك وعدا حسنا ،و فوق هذا رحمة أرحم الراحمين",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q66747114c7",
  "kind": "yes/no",
  "text": "هاض بعرفو بس مقرف",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q5f53cacdc6",
  "kind": "yes/no",
  "text": "اللهم اهدنا الى صراطتك المستقيم",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q1e8222e19a",
  "kind": "yes/no",
  "text": "اللهم انزع من قلوبنا مالا يرضيك",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4971c744ac",
  "kind": "yes/no",
  "text": "جزاك الله خيرا",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q776f57240c",
  "kind": "yes/no",
  "text": "والله عاهات",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q60d0c94717",
  "kind": "yes/no",
  "text": "اجل اسقاط حكومة طروانة",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q00021c23bf",
  "kind": "yes/no",
  "text": "المواساة والمحبة بكل الامور رمز الاخوة",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4343e437e4",
  "kind": "yes/no",
  "text": "انسان غريب",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q0949d3e017",
  "kind": "yes/no",
  "text": "والله صحيح",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q7e9f623a04",
  "kind": "yes/no",
  "text": "صح جدا",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4d3edaf3b5",
  "kind": "yes/no",
  "text": "\"ما بدي غير 10 يعملو لايك للبيج",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 }
]
