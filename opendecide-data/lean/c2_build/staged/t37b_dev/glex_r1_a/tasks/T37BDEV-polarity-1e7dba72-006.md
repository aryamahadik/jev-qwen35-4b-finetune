# T37b-dev G-LEX read T37BDEV-polarity-1e7dba72-006 (family T37BDEV, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/staged/t37b_dev/glex_r1_a/answers/T37BDEV-polarity-1e7dba72-006.json

The answer is one JSON list with exactly 18 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (18; one JSON object per line)

```json
[
{"qid": "q6a284f9720", "question_a": "Does the email announce a change of venue?", "question_b": "Would it be the way that the email does not announce a change of venue?"},
{"qid": "q39c4d2d0e7", "question_a": "Does the form request a phone number?", "question_b": "Would it add up that the form requests a phone number?"},
{"qid": "qd8681c0bf7", "question_a": "Does the bus have a ramp for wheelchairs?", "question_b": "Would it be the situation that the bus does not have a ramp for wheelchairs?"},
{"qid": "qdccf292519", "question_a": "Is the meeting scheduled for the morning?", "question_b": "Would it come to pass that the meeting is scheduled for the morning?"},
{"qid": "q48adc942d6", "question_a": "Does the lecture have a recorded version?", "question_b": "Would it eventuate that the lecture does not have a recorded version?"},
{"qid": "q51a02e9c9e", "question_a": "Does the policy cover damage caused by floods?", "question_b": "Is it the point that the policy does not cover damage caused by floods?"},
{"qid": "q61c786ea7a", "question_a": "Does the bag contain a receipt?", "question_b": "Would it pan out that the bag contains a receipt?"},
{"qid": "q4aa8e037c8", "question_a": "Is the fee included in the ticket price?", "question_b": "Is it prescribed that the fee is included in the ticket price?"},
{"qid": "q8346500009", "question_a": "Does the kit contain spare batteries?", "question_b": "Does it work out that the kit does not contain spare batteries?"},
{"qid": "qe3aa576585", "question_a": "Does the menu contain a vegetarian dish?", "question_b": "Is it down to the fact that the menu does not contain a vegetarian dish?"},
{"qid": "qaf5afaca43", "question_a": "Is the course limited to adults?", "question_b": "Would it pan out that the course is limited to adults?"},
{"qid": "q1207d55b28", "question_a": "Does the shop have a returns desk?", "question_b": "Would it come about that the shop has a returns desk?"},
{"qid": "q612eeb269b", "question_a": "Does the card support contactless payment?", "question_b": "Does it hold generally that the card supports contactless payment?"},
{"qid": "q620a778d38", "question_a": "Does the course include an exam?", "question_b": "Is it decided that the course includes an exam?"},
{"qid": "q7f149b6235", "question_a": "Does the sign allow visitors to park here?", "question_b": "Is it just that the sign allows visitors to park here?"},
{"qid": "q832c9b3c5d", "question_a": "Does the bus have a ramp for wheelchairs?", "question_b": "Would it be the outcome that the bus does not have a ramp for wheelchairs?"},
{"qid": "q734d5aad55", "question_a": "Does the tour include a guide?", "question_b": "Would it be the circumstance that the tour does not include a guide?"},
{"qid": "qfb69913513", "question_a": "Does the lesson plan involve group work?", "question_b": "Is it settled that the lesson plan involves group work?"}
]
```
