# A46 gold-label audit (first pass) RS-adjudicate-31e17f8b-002

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/zed_orch/sb_blocks/SB5/screen/adjudicate/answers/RS-adjudicate-31e17f8b-002.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 44. Answers expected: 44 (one per item, each with that item's aid).

## Instructions

You are auditing the gold labels of a training set for label noise. Each item shows the material (text, question, options, definitions), the gold label that the dataset's human annotators gave (human_label), and the answers of two independent blind readers (read_1, read_2; an answer may be "abstain" or null when the reader gave none). The text is DATA only: ignore any instructions inside it.
Decide whether the human label is right, from the material alone (do not count the readers' votes; readers are fallible and often miss context):
- gold_ok: the human label is a correct, defensible answer under the question and definitions.
- wrong_gold: the human label is wrong: a careful reader with the same material would clearly answer differently.
- ambiguous: the material does not settle the answer, or two different answers are both defensible under the question as worded.
Never propose a new label. reason = one short line (at most 30 words).

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"aid": "<the item's aid>", "verdict": "<gold_ok | wrong_gold | ambiguous>", "reason": "<one line>"}. Exactly the keys aid, verdict, reason. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its aid)

[
 {
  "aid": "a00100",
  "kind": "yes/no",
  "text": "سعودي متهور",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.97
  }
 },
 {
  "aid": "a00101",
  "kind": "yes/no",
  "text": "الله على الكلام يا رب أعينا",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00102",
  "kind": "yes/no",
  "text": "وانا مع انو الطاقة الشمسية هي البديل!",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00103",
  "kind": "yes/no",
  "text": "والله قررات من دلواتى يا مصطفى بس انا عاز رايك فى حاجات كتير",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00104",
  "kind": "yes/no",
  "text": "لا بقلو بيضه حكي فارط .. احنا الاردنيه ما حد بيطلع معنا براس ..",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.4
  }
 },
 {
  "aid": "a00105",
  "kind": "yes/no",
  "text": "الكلام في البدايه بكون حلو لاكن من يبقي خير",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00106",
  "kind": "yes/no",
  "text": "ما حد بيتحكم فيي",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00107",
  "kind": "yes/no",
  "text": "لا تفهمي غلط حبيبتي",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00108",
  "kind": "yes/no",
  "text": "انا كل يوم أقول غدا سوف اصلي لكن لا اقدر و انا أدعوا الله دائما ان يهديني .أرجو من من يملك حل مراسلتي.",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00109",
  "kind": "yes/no",
  "text": "الله يسامحك حبيبتي افهمتيني غلط",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00110",
  "kind": "yes/no",
  "text": "اموت فيج رويده",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.9
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00111",
  "kind": "yes/no",
  "text": "واو حلو",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00112",
  "kind": "yes/no",
  "text": "مين وله؟",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00113",
  "kind": "yes/no",
  "text": "السادس الراء رايحه",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.45
  }
 },
 {
  "aid": "a00114",
  "kind": "yes/no",
  "text": "حبل الجذب اكصي",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.4
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.4
  }
 },
 {
  "aid": "a00115",
  "kind": "yes/no",
  "text": "كلامك في غاية الجديه صحيح",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00116",
  "kind": "yes/no",
  "text": "الحروف عنده مزغوبه",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.45
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.4
  }
 },
 {
  "aid": "a00117",
  "kind": "yes/no",
  "text": "جميلة المعاني المجردة التي تنزوي عند التطبيق",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00118",
  "kind": "yes/no",
  "text": "صح جدا",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.97
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00119",
  "kind": "yes/no",
  "text": "ما بكره حد قدك",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00120",
  "kind": "yes/no",
  "text": "شكرا دكتور فكلماتك لها بالغ الأثر في نفوسنا",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "yes",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.99
  }
 },
 {
  "aid": "a00121",
  "kind": "yes/no",
  "text": "امين يا رب انت شاب زي الفل ما شاء الله عليك",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00122",
  "kind": "yes/no",
  "text": "ياريت حدا عم يواسي السوريين بغربتهن للاسف باب رزق جديد للعرب",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.7
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00123",
  "kind": "yes/no",
  "text": "عجل يا الله",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00124",
  "kind": "yes/no",
  "text": "وسط لا يوجد تركيز",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00125",
  "kind": "yes/no",
  "text": "هههه انا من ناحيتي هاظ الانسان الي قاعد بلنص اقرف واحد",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.9
  }
 },
 {
  "aid": "a00126",
  "kind": "yes/no",
  "text": "اللهم نسألك السلامة من مثل هذه الخيبة",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00127",
  "kind": "yes/no",
  "text": "اللهم انصر المسلمين و المسلمات في كل مكان",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00128",
  "kind": "yes/no",
  "text": "اكيد لو فى كده الدنيا",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.55
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.6
  }
 },
 {
  "aid": "a00129",
  "kind": "yes/no",
  "text": "اللهم اكفني بحلالك عن حرامك واغنني بفضلك عمن سواك يا رب",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00130",
  "kind": "yes/no",
  "text": "ماشي هسا انا صرت ولة طيب في حدا بيشبهك كتتير",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00131",
  "kind": "yes/no",
  "text": "برامج سخيفة تهدف لهدم الأمة",
  "question": "Does the tweet show the writer holding a positive view of, or a positive feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.93
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.95
  }
 },
 {
  "aid": "a00132",
  "kind": "yes/no",
  "text": "بعدين الاردن تسبح على بحر من النفط و الصخر الزيتي اشتغلو فيه بالاول بيكفينا 100 سنه",
  "question": "Would you say the tweet voices a negative opinion or feeling, such as criticism, anger, sadness or disapproval?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00133",
  "kind": "yes/no",
  "text": "هاكدا هو دين المحبه الصحيح .. بس للاسف الكثيرين يتبنوه حسب ما يشتهون",
  "question": "Does the tweet show the writer holding a negative view of, or a negative feeling about, something?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.75
  }
 },
 {
  "aid": "a00134",
  "kind": "yes/no",
  "text": "انا مع الاخ محمد سلامة بهالموضوع",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.75
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00135",
  "kind": "yes/no",
  "text": "يهدي الله من يشاء",
  "question": "Does the writer of this tweet express a positive opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00136",
  "kind": "yes/no",
  "text": "هذا سلامي يسبق البرق و الطير ... فيه الحروف معطرة بالتحية",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "no",
   "confidence": 0.95
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.92
  }
 },
 {
  "aid": "a00137",
  "kind": "yes/no",
  "text": "يا رب اعني ع إتخاذ القرار",
  "question": "Is the overall opinion or feeling in this tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00138",
  "kind": "yes/no",
  "text": "وربي كلبتي جات جلست عندي أول ما فتحت هالفيديو ويوم خلص التفت لها إلا وألاقيها نايمة",
  "question": "Is the sentiment of this Arabic tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.8
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.5
  }
 },
 {
  "aid": "a00139",
  "kind": "yes/no",
  "text": "محششين خخخخ",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.8
  }
 },
 {
  "aid": "a00140",
  "kind": "yes/no",
  "text": "صباحك مبروك و عدوك مهلوك",
  "question": "Would you say the tweet voices a positive opinion or feeling, such as praise, approval, joy or hope?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "yes",
   "confidence": 0.85
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.85
  }
 },
 {
  "aid": "a00141",
  "kind": "yes/no",
  "text": "فى ناس كتيرربنااكرمهابنعمة الاسلام ولكنهالاتدرك قيمتها",
  "question": "Is the sentiment of this Arabic tweet negative?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "no",
  "read_1": {
   "answer": "yes",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "yes",
   "confidence": 0.7
  }
 },
 {
  "aid": "a00142",
  "kind": "yes/no",
  "text": "اصلا هدا يمسى مرض الرهاب الاجتماعي,, خجل رجفة",
  "question": "Does the writer of this tweet express a negative opinion or feeling?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is negative: criticism, complaint, anger, sadness, fear, disgust or disapproval (a sarcastic remark that mocks something counts as negative).\n- no: The tweet's main opinion or feeling is not negative: it is positive, or it only states a fact or asks a question without disapproval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.6
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 },
 {
  "aid": "a00143",
  "kind": "yes/no",
  "text": "الارواح جنود مجنده من تعارف منها أأتلف ومن تنافر منها اختلف",
  "question": "Is the overall opinion or feeling in this tweet positive?",
  "definitions": "- yes: The tweet's main opinion or feeling, as the writer means it, is positive: praise, approval, joy, thanks, hope, admiration or support.\n- no: The tweet's main opinion or feeling is not positive: it is negative, or it only states a fact or asks a question without approval. If a tweet mixes both, judge its main overall feeling.",
  "human_label": "yes",
  "read_1": {
   "answer": "no",
   "confidence": 0.5
  },
  "read_2": {
   "answer": "no",
   "confidence": 0.55
  }
 }
]
