# Haiku exactness read NEGTW-polarity-8ba298a9-023 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/exact_prog/answers/NEGTW-polarity-8ba298a9-023.json

The answer is one JSON list with exactly 10 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (10; one JSON object per line)

```json
[
{"qid": "q3f2ed7c8be", "question_a": "Can the resident park on this street?", "question_b": "Is it true that the resident cannot park on this street?"},
{"qid": "q3daa4b809c", "question_a": "Can the student submit the form online?", "question_b": "Is it right to say that the student cannot submit the form online?"},
{"qid": "q10851be19a", "question_a": "Does the price include tax?", "question_b": "Is it the case that the price lacks tax?"},
{"qid": "q095e62e296", "question_a": "Does the guide explain how to reset the device?", "question_b": "Is it true that the guide doesn't explain how to reset the device?"},
{"qid": "q34127227e0", "question_a": "Has the road reopened to traffic?", "question_b": "Is it not the case that the road has reopened to traffic?"},
{"qid": "q7f0044580b", "question_a": "Have the files been listed?", "question_b": "Is it true that the files have not been listed?"},
{"qid": "qac20c789a1", "question_a": "Does the plan have a backup route?", "question_b": "Is it true that the plan lacks a backup route?"},
{"qid": "q9287587950", "question_a": "Does the memo ask staff to reply by email?", "question_b": "Is it accurate to say that the memo asks staff to reply by email?"},
{"qid": "q17fccc39da", "question_a": "Is there a contact name in the email?", "question_b": "Is it correct that there is not a contact name in the email?"},
{"qid": "qeafed5a26c", "question_a": "Is the class eligible for the discount?", "question_b": "Is it right to say that the class isn't eligible for the discount?"}
]
```
