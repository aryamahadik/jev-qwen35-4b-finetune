# A46 replay label-noise blind read RSBS02-blind_read-5ca3e748-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/sb_blocks/SB5/screen/reads/answers/RSBS02-blind_read-5ca3e748-002.json

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
  "qid": "q178307c31b",
  "kind": "yes/no",
  "text": "وش هالتحف والله مساكين ماكلين مقلب بقوه",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qc8651a7550",
  "kind": "yes/no",
  "text": "اللهم اجعلني دائما مظلوم",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q2bebaf274f",
  "kind": "yes/no",
  "text": "يااااااااااا الله ما احلاه من خبر والله فرحتوني",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4278de7226",
  "kind": "yes/no",
  "text": "ذا مرتك بتعمل هيك يا ادمن لا تفكر كل الرجال مثلك تفي عليك",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q74281e61de",
  "kind": "yes/no",
  "text": "اللهم ما اعنا على التغير",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q0fbaf739ae",
  "kind": "yes/no",
  "text": "حلوه عدوله احس انه يفطر حشيش",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q1224d79dfc",
  "kind": "yes/no",
  "text": "من كانت له عزيمة لن ييأس ، ومن ابتغى الأجر من الله ثابر، حياكم الله اخي مؤمن",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q707df250cd",
  "kind": "yes/no",
  "text": "يارب اعنا علي ترك المعاصي ماحيينا",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qb5623de07a",
  "kind": "yes/no",
  "text": "يعني يجبون كم واحد يعطونهم فلوس ويجون يستهبلوا عندهم عشان يحركون البرنامج",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q0889e13997",
  "kind": "yes/no",
  "text": "اللي صوةتو بشبه ابو وديع ليش بتمسخرو عليه",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q71cdfd4eb1",
  "kind": "yes/no",
  "text": "أكيد جزاك الله خيرا",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qffff3bd4cc",
  "kind": "yes/no",
  "text": "أللهم ارضنا بما قسمته لنا",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qbaa8afa475",
  "kind": "yes/no",
  "text": "الله ايه الجمال ده سبحانك ربي",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4c7bb370ac",
  "kind": "yes/no",
  "text": "#احسنوا الظن",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q6b87b3b1bd",
  "kind": "yes/no",
  "text": "يا هيك الشباب يا بلاش",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q319805bf3e",
  "kind": "yes/no",
  "text": "والله اول واحد سمعته منهم احسب سمااعتي خرباً يابطني من الضحك والله زااااحفين",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q36c74773c3",
  "kind": "yes/no",
  "text": "اللي لازم يصير اضراب جميع موظفي الدوائر الحكوميه و الخاصه لمدة اسبوع و شوف بعدها",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q175a7772b2",
  "kind": "yes/no",
  "text": "هو أحنا خلينآ نخلص أم هالبرجين الللي صرلهم 16 سنة و بعدين بنفكر نعمل نووي \" سلمي \" هههه من الديسي",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q22abe4cb17",
  "kind": "yes/no",
  "text": "الحمد لله الذى لا يُحمد على مكره سواه",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qc0d61ff6c8",
  "kind": "yes/no",
  "text": "بس أنا مش منهم ولا البنات يلي بالجروبات",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qc1940eb48b",
  "kind": "yes/no",
  "text": "من احبه الله حبب به خلقه",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4d2e9b5d23",
  "kind": "yes/no",
  "text": "والله شوي وتجيني جلطه لما ماطلعت الاولى ذيك المره",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q68b2aaa14a",
  "kind": "yes/no",
  "text": "الله يلعن امك وش ها القرف",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q5794e99cc2",
  "kind": "yes/no",
  "text": "ولا جورج في الزمنات بس حرام يفضحوهم",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q1d560869f0",
  "kind": "yes/no",
  "text": "كـلمـة حـبـ عـجـبـتـنـى جـيـتـ آقــؤلهـآ جــرحـتـنـى",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q071c80c52a",
  "kind": "yes/no",
  "text": "والله انت الحبيبة يا طيبة",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q79bce75e7a",
  "kind": "yes/no",
  "text": "يا طيبة بالروح افتدينا",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q8ed2656a9d",
  "kind": "yes/no",
  "text": "مين وله؟",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qab970abd68",
  "kind": "yes/no",
  "text": "اميره ممكن اضافه لو سمحتي",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q7a0611d08b",
  "kind": "yes/no",
  "text": "تقول داخله فيها ترله انحولت مع الاغنيه",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q1200a465e2",
  "kind": "yes/no",
  "text": "صباح الخير و النور و الأنوار",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qa1d412e66e",
  "kind": "yes/no",
  "text": "يلعن شرفك شو واثقة من حالك",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q1d4a63a995",
  "kind": "yes/no",
  "text": "والله ما يحرر عزبت بنقاليه",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q264c7b5166",
  "kind": "yes/no",
  "text": "كنت أخادع الحيـاة لكي أعيش كما أريد .. لكن الحياة خدعتني و عشت كما هي تريد",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q3c250ac4d9",
  "kind": "yes/no",
  "text": "التطبيقات قليله بالمتجر ولازال امام مايكروسوفت عمل طويل للتغلب على هذه المشكله",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qd5758a2d0d",
  "kind": "yes/no",
  "text": "مقال رائع والله يهدي بناتنا ياااارب ويرجعهم للصواب",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q8ccdf594bf",
  "kind": "yes/no",
  "text": "للأسف البعض يعتقد ان المفاعل النووي سيحل مشاكلنا الاقتصادية ولكن الأردن لا يمتلك موارد مالية وهذا يعني الحاجة لشريك أجنبي \"كما اعلنت هيئة الطاقة\" يملك غالبية الأسهم كما في تركيا على سبيل المثال وذلك يعني ان هذا الشريك سيمتلك الجزء الأكبر من المفاعل ولن يكون ملك للأردن وبالتالي ستقوم الحكومة ايضاً بدفع تكاليف الكهرباء للمستثمر وبالتالي المفاعل النووي لن يوفر لك الكهرباء بسعر قليل",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q5d7c17ac68",
  "kind": "yes/no",
  "text": "يع شوهاي الوساخة",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q0e557c6416",
  "kind": "yes/no",
  "text": "ابتسم امام كل الناس لتسرهم و تجبر خواطرهم فتبسمك في وجوههم صدقه",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q88fe03feb1",
  "kind": "yes/no",
  "text": "ربنا المستعان ادعولنا ارجوكم",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qda3faaadb5",
  "kind": "yes/no",
  "text": "نعم فالنجعل حب الله هو الغايه وربنايسامح كل تائب",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q669aa982f2",
  "kind": "yes/no",
  "text": "الحمد لله كلما ارى ناس اسلموا تعم الفرحة في قلبي",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q8ecf323abf",
  "kind": "yes/no",
  "text": "احذفه لاني بجلس احش فيهم لمين اكفر",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "qa73cc6df27",
  "kind": "yes/no",
  "text": "و إلى أسماء الاسد : كـــس أخـــت زوجـــك :)",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q4511914e44",
  "kind": "yes/no",
  "text": "تعليم الاطفال علا الاغاني وعلا الرقص بدلن من تعليم القران الكريم بدلن من تعليم الدين الله لا يوفقكم",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q474226018c",
  "kind": "yes/no",
  "text": "والله كذب من سوبر ستار القذر هذاا",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q451dfd771e",
  "kind": "yes/no",
  "text": "دعاء جميل ماشاء الله",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q390e821403",
  "kind": "yes/no",
  "text": "الحق عالحقير اللي نزل المنشور_بجوز اهله لابسين منه_ولك لاتنزل اشي زي هيك يا؟؟؟!",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q5524e64db0",
  "kind": "yes/no",
  "text": "كلام حلو ومشجع",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling."
 },
 {
  "qid": "q78db2614a1",
  "kind": "yes/no",
  "text": "لازم يحكم عليهم بالسجن",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling."
 }
]
