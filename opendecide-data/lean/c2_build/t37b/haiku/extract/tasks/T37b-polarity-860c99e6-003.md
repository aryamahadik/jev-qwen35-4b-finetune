# Haiku polarity read A T37b-polarity-860c99e6-003 (family T37b, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/haiku/extract/answers/T37b-polarity-860c99e6-003.json

The answer is one JSON list with exactly 50 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}. Words in capital letters inside curly braces, such as {N}, are placeholders: each one stands for the same value in both questions.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (50; one JSON object per line)

```json
[
{"qid": "q4d783cac43", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "Do the listed duties form part of the job of the occupation named above?"},
{"qid": "qca712c5d9d", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the action being judged wrong by common social norms?"},
{"qid": "qa2e6becdef", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the deed being assessed wrong according to common social norms?"},
{"qid": "qef8f33dcfc", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Because it is a different answer, leaves out important information, or adds misleading or superfluous information, is the candidate answer an unacceptable substitute for the reference answer?"},
{"qid": "q94c8c04c3e", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every item of information in the summary sentence backed by the evidence sentences?"},
{"qid": "q89b94d3289", "question_a": "Is this action against the law in most places?", "question_b": "Is this action in breach of the law in most locations?"},
{"qid": "qcf1682878b", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Is there confirmation in the assistant's reply that the booking the customer asked for was actually made?"},
{"qid": "qe7ac35ee1e", "question_a": "Does the evidence support the claim?", "question_b": "Does the evidence lend support to the claim?"},
{"qid": "q3040be903d", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the action being judged wrong under common social norms?"},
{"qid": "q67336dc007", "question_a": "Is this post hateful?", "question_b": "Hateful, is this post?"},
{"qid": "q94eaf176f7", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "According to this vehicle safety complaint, was the vehicle actually involved in a crash?"},
{"qid": "qf3f4f243c1", "question_a": "Does the evidence support the claim?", "question_b": "Is the claim supported by the evidence?"},
{"qid": "q21c53c648e", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's reply confirm the booking the customer asked for was actually made?"},
{"qid": "q318ec7e166", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "According to common social norms, is the action being judged acceptable?"},
{"qid": "q1c97ee5ce2", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "Does this vehicle safety complaint state that the vehicle was actually involved in a collision?"},
{"qid": "qa3f7d601c9", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Does this vehicle safety complaint say the vehicle actually caught fire?"},
{"qid": "q250c95f097", "question_a": "By the end of this conversation, has the customer actually bought movie tickets?", "question_b": "According to this conversation, has the customer actually bought movie tickets by the time it ends?"},
{"qid": "qa33b6b5cd6", "question_a": "Is the statement supported by the table?", "question_b": "Does the table provide support for the statement?"},
{"qid": "q657af00fae", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Does this paragraph come out with the contrarian climate claim that {CLAIM}?"},
{"qid": "q2258b9e5dd", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the action being assessed as wrong according to common social norms?"},
{"qid": "q0bac8a8e50", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "Based on the text, are the listed duties part of the job of the occupation named above?"},
{"qid": "q00ea06f549", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's reply confirm, for the booking the customer asked for, that it was actually made?"},
{"qid": "q7ab2e3b322", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Can the candidate answer stand in for the reference answer on this question, giving at least the same info without leaving out anything important or adding misleading or extra bits?"},
{"qid": "q4d906be47c", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action judged acceptable by common social norms?"},
{"qid": "qdb037b5f46", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Going by this vehicle safety complaint, did the vehicle actually catch fire?"},
{"qid": "q403cf29726", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Made by this paragraph, is the contrarian climate claim that {CLAIM}?"},
{"qid": "qb2e281173b", "question_a": "Does the evidence contradict the claim?", "question_b": "Is the claim contradicted by the evidence?"},
{"qid": "q30c5a39bc9", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "According to the list, are these duties part of the job of the occupation named above?"},
{"qid": "qa418d47634", "question_a": "Is this action against the law in most places?", "question_b": "Is this action prohibited by the law in most places?"},
{"qid": "qdf5d6da7d1", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action being judged permissible under common social norms?"},
{"qid": "qc1527c0f30", "question_a": "Is the statement supported by the table?", "question_b": "Is the statement supported according to the table?"},
{"qid": "q8429a592a6", "question_a": "Is this action against the law in most places?", "question_b": "Does this action break the law in most places?"},
{"qid": "q3f22681b78", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Hey, does this paragraph say the contrarian climate claim that {CLAIM}?"},
{"qid": "q7a3c15758b", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the act under evaluation acceptable according to common social norms?"},
{"qid": "qf6c33d8448", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Looking at the summary sentence, is every piece of information in it supported by the evidence sentences?"},
{"qid": "q5063e8dc1d", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "In this vehicle safety complaint, is it stated that the vehicle actually caught fire?"},
{"qid": "q1fda670098", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Within this paragraph, does it make the contrarian climate claim that {CLAIM}?"},
{"qid": "qd122fee7b9", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Do the evidence sentences support every piece of information in the summary sentence?"},
{"qid": "q5a559f8729", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Is there confirmation that the candidate answer is an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?"},
{"qid": "q400ea7bc7e", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Can the candidate answer replace the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "qee84ab1bbf", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "Are the enumerated duties included in the job of the occupation named above?"},
{"qid": "q7ac326c203", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Is this paragraph making the contrarian climate claim that {CLAIM}?"},
{"qid": "q1937b73068", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Can the proposed answer be used in place of the reference answer, conveying at least the same information for this question, without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "qe0531de44b", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's reply verify that the booking the customer asked for was actually made?"},
{"qid": "qc32181a7e2", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every detail in the summary sentence supported by the evidence sentences?"},
{"qid": "q1a35cc45be", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Going by common social norms, is the action being judged wrong?"},
{"qid": "qda6a8677f5", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's written response confirm that the booking the customer asked for was actually made?"},
{"qid": "q9dbb17452d", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the action being judged, according to common social norms, wrong?"},
{"qid": "qdcea9c9ab9", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Is the candidate answer usable in place of the reference answer without dropping anything important or adding misleading or superfluous information while conveying at least the same information for this question?"},
{"qid": "q98f8951041", "question_a": "Is this post hateful?", "question_b": "Is this post of a hateful nature?"}
]
```
