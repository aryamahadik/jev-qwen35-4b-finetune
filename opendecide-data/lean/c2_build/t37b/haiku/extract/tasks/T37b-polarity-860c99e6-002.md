# Haiku polarity read A T37b-polarity-860c99e6-002 (family T37b, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/haiku/extract/answers/T37b-polarity-860c99e6-002.json

The answer is one JSON list with exactly 50 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}. Words in capital letters inside curly braces, such as {N}, are placeholders: each one stands for the same value in both questions.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (50; one JSON object per line)

```json
[
{"qid": "q95f68486e1", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every bit of info in the summary sentence backed up by the evidence sentences?"},
{"qid": "qff39da2410", "question_a": "Does the evidence support the claim?", "question_b": "Does the evidence back up the claim?"},
{"qid": "qb041dc29af", "question_a": "Is the statement supported by the table?", "question_b": "Supported by the table, is the statement?"},
{"qid": "qd75884aa29", "question_a": "Is this action against the law in most places?", "question_b": "Does this action violate the law in most places?"},
{"qid": "q29c53c28bd", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Is it this paragraph that makes the contrarian climate claim that {CLAIM}?"},
{"qid": "q15d4d4b34e", "question_a": "Is the statement supported by the table?", "question_b": "Is there support for the statement in the table?"},
{"qid": "q46d8fbcc49", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Is the candidate answer an unacceptable substitute for the reference answer, because it gives another answer, skips important information, or adds information that misleads or is superfluous?"},
{"qid": "q2d76e28afb", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action being judged okay according to common social norms?"},
{"qid": "qd4d413814f", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is there a judgment that the action is wrong according to common social norms?"},
{"qid": "qfc63083a9b", "question_a": "Does the evidence support the claim?", "question_b": "Does that evidence support that claim?"},
{"qid": "q988a53b562", "question_a": "By the end of this conversation, has the customer actually bought movie tickets?", "question_b": "Has the customer actually bought movie tickets by the time this conversation finishes?"},
{"qid": "q02260de927", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Under common social norms, is the action being judged wrong?"},
{"qid": "qd2e4b66c72", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "In place of the reference answer, can the candidate answer be used, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "q9f1241411f", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Based on the text, can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "qdfc48d8b56", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "For the occupation named above, are the listed duties part of its job?"},
{"qid": "qb1fb0ae933", "question_a": "Does the evidence contradict the claim?", "question_b": "Going by the text, does the evidence contradict the claim?"},
{"qid": "qdb61e8d98b", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Can the reference answer be replaced by the candidate answer, with the candidate conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "q5961a21b87", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Does the paragraph make the contrarian climate claim that {CLAIM}?"},
{"qid": "q16775c641d", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Can the candidate answer be used in place of the reference answer, conveying at least the same information without leaving out anything important or adding misleading or superfluous information, for this question?"},
{"qid": "qdd18935a1f", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Did the vehicle actually catch fire, according to this vehicle safety complaint?"},
{"qid": "qeaae3a3131", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "So, are the duties on the list part of the job of the occupation named above?"},
{"qid": "q1c5035d9e0", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Going by the text, is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?"},
{"qid": "qf5c4be2760", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Is the candidate answer a usable replacement for the reference answer on this question, conveying at least the same information without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "qf03284c0c6", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "Does this vehicle safety complaint state that the vehicle was actually involved in a crash?"},
{"qid": "q2d51ff5c8b", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's response confirm that the booking requested by the customer was actually made?"},
{"qid": "qc1f96cb013", "question_a": "Is this action against the law in most places?", "question_b": "Is this action forbidden by law in most places?"},
{"qid": "q248fe8c951", "question_a": "Is this post hateful?", "question_b": "Is there a hateful quality to this post?"},
{"qid": "q4d5187f878", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Is the booking the customer asked for confirmed as actually made in the assistant's reply?"},
{"qid": "q9ea72fbd18", "question_a": "Is this post hateful?", "question_b": "In this post, is there hatred?"},
{"qid": "q33702141ff", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "Does this vehicle safety complaint say the vehicle was actually involved in a crash?"},
{"qid": "q892950252c", "question_a": "Does the evidence contradict the claim?", "question_b": "Does the evidence contradict it?"},
{"qid": "q4f74453e65", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Is the candidate answer an unacceptable swap for the reference answer, since it's a different answer, leaves out important information, or adds misleading or extra information?"},
{"qid": "q6dd5250462", "question_a": "Is this action against the law in most places?", "question_b": "Is it against the law in most places?"},
{"qid": "q1f2df2cfd9", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Is the candidate answer judged to be an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?"},
{"qid": "qe8caeb08c5", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Does this paragraph put forward the contrarian climate claim that {CLAIM}?"},
{"qid": "q403bdcff25", "question_a": "Is the statement supported by the table?", "question_b": "Based on the table, is the statement supported?"},
{"qid": "q7367c91d1d", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "Are the listed duties part of the job, for the occupation named above?"},
{"qid": "q6c660878cc", "question_a": "Does the evidence support the claim?", "question_b": "According to the evidence, does it support the claim?"},
{"qid": "qffa1c7d795", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Does this vehicle safety complaint state that the vehicle actually began to burn?"},
{"qid": "qa718c0d3be", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Based on the text, does this paragraph make the contrarian climate claim that {CLAIM}?"},
{"qid": "qabaf6ccbd9", "question_a": "Is the statement supported by the table?", "question_b": "Does the data table back up the statement?"},
{"qid": "qaa2e4d19a6", "question_a": "Is the statement supported by the table?", "question_b": "Does the table back up the statement?"},
{"qid": "q5501c0c48c", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action under assessment deemed acceptable according to common social norms?"},
{"qid": "q6475dff083", "question_a": "Is this action against the law in most places?", "question_b": "Based on the text, is this action against the law in most places?"},
{"qid": "q968798eb47", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Does the paragraph here make the contrarian climate claim that {CLAIM}?"},
{"qid": "q70c32339be", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "In the assistant's reply, is it confirmed that the booking the customer asked for was actually made?"},
{"qid": "qbfbfa6732b", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every piece of information in the summary sentence backed up by the evidence sentences?"},
{"qid": "q14e29f8f4f", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action under judgment acceptable according to common social norms?"},
{"qid": "q2c5afa435b", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "Is the inclusion of the listed duties in the job of the occupation named above true?"},
{"qid": "q24cfa5f444", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every piece of the summary sentence's information supported by the evidence sentences?"}
]
```
