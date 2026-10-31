# Haiku polarity read B T37b-polarity-a5e5abd8-002 (family T37b, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/haiku/extract/answers/T37b-polarity-a5e5abd8-002.json

The answer is one JSON list with exactly 50 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}. Words in capital letters inside curly braces, such as {N}, are placeholders: each one stands for the same value in both questions.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (50; one JSON object per line)

```json
[
{"qid": "q90fd48bea1", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every piece of information in the summary sentence backed up by the evidence sentences?"},
{"qid": "q2ce2f30192", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Going by common social norms, is the action being judged wrong?"},
{"qid": "q0e60331d40", "question_a": "Does the evidence support the claim?", "question_b": "Is there support from the evidence for the claim?"},
{"qid": "q361c721aba", "question_a": "Does the evidence contradict the claim?", "question_b": "Looking at the evidence, does it contradict the claim?"},
{"qid": "qbb762b861c", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Is there confirmation in the assistant's reply that the booking the customer asked for was actually made?"},
{"qid": "q1cf4d98016", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is the action being assessed as wrong according to common social norms?"},
{"qid": "qb3f2e5d8b1", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "According to common social norms, is the action being judged wrong?"},
{"qid": "qe709d5bc56", "question_a": "By the end of this conversation, has the customer actually bought movie tickets?", "question_b": "By the conclusion of this conversation, has the customer actually purchased movie tickets?"},
{"qid": "qd567fcd970", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Does the assistant's reply confirm, for the booking the customer asked for, that it was actually made?"},
{"qid": "qd4b022696f", "question_a": "Does the evidence contradict the claim?", "question_b": "Does the evidence conflict with what the claim says?"},
{"qid": "q6d5492a665", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Looking at the summary sentence, is every piece of information in it supported by the evidence sentences?"},
{"qid": "q87bf3edbad", "question_a": "Is this post hateful?", "question_b": "Is this post full of hatred?"},
{"qid": "q6c19847d80", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Within this paragraph, does it make the contrarian climate claim that {CLAIM}?"},
{"qid": "qa9b6daa17e", "question_a": "Is the statement supported by the table?", "question_b": "Is the statement backed up by the table?"},
{"qid": "q27607c768d", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "The action being judged, is it wrong according to common social norms?"},
{"qid": "q83c28363d9", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "Does this vehicle safety complaint state that the vehicle was actually involved in a crash?"},
{"qid": "q636e85064d", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "Does this paragraph put forward the contrarian climate claim that {CLAIM}?"},
{"qid": "q6909c0cbc6", "question_a": "Does the evidence support the claim?", "question_b": "Does the evidence back up the claim?"},
{"qid": "qaf1b63ba6f", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Does the candidate answer count as an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?"},
{"qid": "q4bf09e81b2", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every piece of information in the sentence that gives the summary supported by the evidence sentences?"},
{"qid": "q33f8d70416", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Is the proposed answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?"},
{"qid": "qc75275603d", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Can the candidate answer replace the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "q90329deebb", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "Is the action being judged acceptable as per common social norms?"},
{"qid": "q5298b50e50", "question_a": "Is this action against the law in most places?", "question_b": "Based on the text, is this action against the law in most places?"},
{"qid": "qc86656a68e", "question_a": "Is the statement supported by the table?", "question_b": "Does the table provide support for the statement?"},
{"qid": "qd49785bdbd", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "Is the candidate answer usable in place of the reference answer without dropping anything important or adding misleading or superfluous information while conveying at least the same information for this question?"},
{"qid": "q6f8b8d379c", "question_a": "Is this post hateful?", "question_b": "Is there a hateful quality to this post?"},
{"qid": "q1bfa97817e", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Is every piece of the summary sentence's information supported by the evidence sentences?"},
{"qid": "q88da04bd02", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "In light of the reference answer, is the candidate answer an unacceptable substitute, because it is a different answer, leaves out important information, or adds misleading or superfluous information?"},
{"qid": "q44a4b4f41f", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Is the booking the customer asked for confirmed as actually made in the assistant's reply?"},
{"qid": "q4680bac0ba", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Is there a judgment that the action is wrong according to common social norms?"},
{"qid": "q41852c8120", "question_a": "Is the action being judged acceptable according to common social norms?", "question_b": "According to common social norms, is the action being judged acceptable?"},
{"qid": "qd2e4b318df", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "Going by this vehicle safety complaint, did the vehicle actually catch fire?"},
{"qid": "qffbd186782", "question_a": "Is every piece of information in the summary sentence supported by the evidence sentences?", "question_b": "Do the evidence sentences support every piece of information in the summary sentence?"},
{"qid": "q64966d34ac", "question_a": "Is the candidate answer an unacceptable substitute for the reference answer, because it is a different answer, leaves out important information, or adds misleading or superfluous information?", "question_b": "Is the candidate answer an unacceptable swap for the reference answer, since it's a different answer, leaves out important information, or adds misleading or extra information?"},
{"qid": "qb5cb074685", "question_a": "Does this vehicle safety complaint report that the vehicle actually caught fire?", "question_b": "According to this vehicle safety complaint, did the vehicle actually catch fire?"},
{"qid": "qa176fc4231", "question_a": "Is this post hateful?", "question_b": "In this post, is there hatred?"},
{"qid": "qee47f029d5", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "Was the vehicle actually involved in a crash, according to this vehicle safety complaint?"},
{"qid": "qd108698592", "question_a": "Is the statement supported by the table?", "question_b": "According to the table, is the statement supported?"},
{"qid": "q4f0703369b", "question_a": "Is this action against the law in most places?", "question_b": "Is this act against the law in most places?"},
{"qid": "qd59ce99458", "question_a": "Is this action against the law in most places?", "question_b": "Is this action illegal in most places?"},
{"qid": "q320a4e2ff3", "question_a": "Is this post hateful?", "question_b": "Is this post regarded as hateful?"},
{"qid": "q5738987e90", "question_a": "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", "question_b": "Does this complaint on vehicle safety say the vehicle was actually involved in a crash?"},
{"qid": "q9329f95fd1", "question_a": "Can the candidate answer be used in place of the reference answer, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?", "question_b": "In place of the reference answer, can the candidate answer be used, conveying at least the same information for this question without leaving out anything important or adding misleading or superfluous information?"},
{"qid": "qb461bea8d4", "question_a": "Does this paragraph make the contrarian climate claim that {CLAIM}?", "question_b": "According to this paragraph, does it make the contrarian climate claim that {CLAIM}?"},
{"qid": "qc58445f4a3", "question_a": "Does the evidence contradict the claim?", "question_b": "Is the evidence in contradiction with the claim?"},
{"qid": "q9b3aa9c9e4", "question_a": "Does the evidence contradict the claim?", "question_b": "Is the claim contradicted by the evidence?"},
{"qid": "q2a4f8eac80", "question_a": "Is the action being judged wrong according to common social norms?", "question_b": "Under common social norms, is the action being judged wrong?"},
{"qid": "qc939386fbb", "question_a": "Does the evidence support the claim?", "question_b": "Does the evidence bolster the assertion?"},
{"qid": "qf9e08960e8", "question_a": "Does the assistant's reply confirm that the booking the customer asked for was actually made?", "question_b": "Based on the text, does the assistant's reply confirm that the booking the customer asked for was actually made?"}
]
```
