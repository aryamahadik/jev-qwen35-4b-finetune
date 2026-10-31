# Haiku polarity read B T37b-polarity-a5e5abd8-003 (family T37b, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/haiku/extract/answers/T37b-polarity-a5e5abd8-003.json

The answer is one JSON list with exactly 50 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}. Words in capital letters inside curly braces, such as {N}, are placeholders: each one stands for the same value in both questions.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (50; one JSON object per line)

```json
[
{"qid": "q55df928649", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the act under evaluation acceptable according to common social norms?"},
{"qid": "qae5436f7b8", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Does this vehicle safety complaint say that the vehicle actually caught fire?"},
{"qid": "qa4aa089b48", "question_a": "By the end of this conversation, has the customer actually bought movie tickets?", "question_b": "Has the customer actually bought movie tickets by the time this conversation finishes?"},
{"qid": "q34d83f1132", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Is the candidate answer an unacceptable stand-in for the reference answer, because it is a different answer, drops important information, or adds misleading or superfluous information?"},
{"qid": "qff45981d09", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Hey, does this paragraph say the contrarian climate claim that {CLAIM}?"},
{"qid": "q3055da7112", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action being judged permissible under common social norms?"},
{"qid": "q07c1233132", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "For the occupation named above, are the listed duties part of its job?"},
{"qid": "qa841545c8f", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "Is there a report in this vehicle safety complaint that the vehicle was actually involved in a crash?"},
{"qid": "qd4335cb50c", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Is there an assertion in this paragraph of the contrarian climate claim that {CLAIM}?"},
{"qid": "q7b03031f72", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "So, are the duties on the list part of the job of the occupation named above?"},
{"qid": "q187e778d31", "question_a": "Does the evidence contradict the claim?", "question_b": "According to the text, does the evidence contradict the claim?"},
{"qid": "q5d4b651210", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is there acceptability for the action being judged according to common social norms?"},
{"qid": "qee6dca0bfc", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action being judged okay according to common social norms?"},
{"qid": "q4f8f8b192e", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's reply confirm that it was actually made, the booking the customer asked for?"},
{"qid": "qefc9de07f1", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Because it is a different answer, leaves out important information, or adds misleading or superfluous information, is the candidate answer an unacceptable substitute for the reference answer?"},
{"qid": "q3e94a2e71c", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Going by common social norms, is this action judged wrong?"},
{"qid": "qb99e83b8c6", "question_a": "Is the statement supported by the table?", "question_b": "Is the statement supported according to the table?"},
{"qid": "q2af2afee45", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's reply verify that the booking the customer asked for was actually made?"},
{"qid": "q43f00c52e2", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Is there confirmation that this paragraph makes the contrarian climate claim that {CLAIM}?"},
{"qid": "qa99123ff80", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every piece of information in the summary sentence given support by the evidence sentences?"},
{"qid": "qe684c90f3c", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every detail in the summary sentence supported by the evidence sentences?"},
{"qid": "q5994ae72e9", "question_a": "Is this action against the law in most places?", "question_b": "Does this action violate the law in most places?"},
{"qid": "qb3820530a5", "question_a": "By the end of this conversation, has the customer actually bought movie tickets?", "question_b": "By the end of this conversation, is there actually a purchase of movie tickets by the customer?"},
{"qid": "q436b5394f5", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Does this vehicle safety complaint state that the vehicle actually began to burn?"},
{"qid": "qf1a520bbaf", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Does this passage advance the contrarian climate claim that {CLAIM}?"},
{"qid": "qb5ed3e508e", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "According to the list, are these duties part of the job of the occupation named above?"},
{"qid": "q56f5d50815", "question_a": "According to the assistant's last message, is {SPAN} confirmed for {ORDER}?", "question_b": "Per the assistant's latest message, is {SPAN} confirmed for {ORDER}?"},
{"qid": "qae03966543", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's response confirm that the booking requested by the customer was actually made?"},
{"qid": "qb227788210", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the action being judged wrong under common social norms?"},
{"qid": "qd60fc3c558", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "Do the listed duties form part of the job of the occupation named above?"},
{"qid": "q1fb439323a", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action, as judged by common social norms, acceptable?"},
{"qid": "qa8cc231c59", "question_a": "Is this post hateful?", "question_b": "Is this post of a hateful nature?"},
{"qid": "qad1a126cac", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's written response confirm that the booking the customer asked for was actually made?"},
{"qid": "q2ce6aec3ad", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Does this vehicle safety complaint say the vehicle actually caught fire?"},
{"qid": "qa199ea1264", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Is it appropriate to use the candidate answer in place of the reference answer for this question, conveying at least the same information without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "qcfc8741eb1", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "Has this vehicle safety complaint reported that the vehicle was actually involved in a crash?"},
{"qid": "q8c668f518b", "question_a": "Is the statement supported by the table?", "question_b": "Is the statement substantiated by the table?"},
{"qid": "q768f668830", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's reply confirm the booking the customer asked for was actually made?"},
{"qid": "q27a4b9c68f", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "Are the listed duties part of the above-named occupation's job?"},
{"qid": "q8e268ad610", "question_a": "Does the evidence support the claim?", "question_b": "According to the evidence, does it support the claim?"},
{"qid": "q696e864d8c", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is the summary sentence's information, every piece of it, supported by the evidence sentences?"},
{"qid": "q66a42c4248", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Does the candidate answer work in place of the reference answer for this question, conveying at least the same information without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "qea3c0fb1e6", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the action being judged wrong, based on common social norms?"},
{"qid": "qac23e81930", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the action being judged wrong in accordance with common social norms?"},
{"qid": "q121f09ed4d", "question_a": "Are the listed duties part of the job of the occupation named above?", "question_b": "Are the listed duties part of the job for the occupation named above?"},
{"qid": "q36274746cc", "question_a": "By the end of this conversation, has the customer actually bought movie tickets?", "question_b": "By this conversation's end, has the customer actually bought movie tickets?"},
{"qid": "q51c555065c", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Is it the assistant's reply that confirms the booking the customer asked for was actually made?"},
{"qid": "qddeffb81f9", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Can the candidate answer be used as a substitute for the reference answer, providing at least the same information for this question, without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "q1b2556536e", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "In the summary sentence, is every piece of information supported by the evidence sentences?"},
{"qid": "q91c101d435", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Does this vehicle safety complaint state that the vehicle actually caught fire?"}
]
```
