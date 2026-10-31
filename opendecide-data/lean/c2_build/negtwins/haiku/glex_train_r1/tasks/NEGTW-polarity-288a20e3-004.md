# Haiku G-LEX read NEGTW-polarity-288a20e3-004 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_train_r1/answers/NEGTW-polarity-288a20e3-004.json

The answer is one JSON list with exactly 17 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (17; one JSON object per line)

```json
[
{"qid": "q06c971797e", "question_a": "Is the drone prohibited over the site?", "question_b": "Is the drone permitted over the site?"},
{"qid": "q50d1fabd6c", "question_a": "Does the offer include free delivery?", "question_b": "Is it wrong that the offer includes free delivery?"},
{"qid": "qd259b5595f", "question_a": "Is the drink included in the ticket?", "question_b": "Is it true that the drink is not excluded in the ticket?"},
{"qid": "qd0448228f6", "question_a": "Does the letter mention a meeting?", "question_b": "Does the letter omit a meeting?"},
{"qid": "qa06e98e27c", "question_a": "Does the policy cover damage caused by floods?", "question_b": "Would it be so that the policy covers damage caused by floods?"},
{"qid": "q3dc1311245", "question_a": "Is the rule covered by the audit?", "question_b": "Is the rule uncovered by the audit?"},
{"qid": "q82e5d40e4c", "question_a": "Does the schedule include a lunch break?", "question_b": "Would it be accurate to say that the schedule includes a lunch break?"},
{"qid": "q355086e406", "question_a": "Does the rent include water?", "question_b": "Would it be inaccurate to say that the rent includes water?"},
{"qid": "qc2c6c29756", "question_a": "Does the regulation forbid the export?", "question_b": "Does the regulation allow the export?"},
{"qid": "q41d0fb036a", "question_a": "Is the breakfast excluded from the stay?", "question_b": "Is the breakfast included from the stay?"},
{"qid": "q6e8ab34fd5", "question_a": "Does the report show the total?", "question_b": "Is it true that the report does not omit the total?"},
{"qid": "q12e8b801c6", "question_a": "Is the number unconfirmed by the ledger?", "question_b": "Is the number confirmed by the ledger?"},
{"qid": "qd6b6b45f88", "question_a": "Is the quota limited in scope?", "question_b": "Is the quota unlimited in scope?"},
{"qid": "qbfa0a8a127", "question_a": "Does the notice omit a fee amount?", "question_b": "Does the notice provide a fee amount?"},
{"qid": "qc28a198246", "question_a": "Does the shop have a returns desk?", "question_b": "Is it incorrect that the shop has a returns desk?"},
{"qid": "q51946670bd", "question_a": "Is the badge issued to every volunteer?", "question_b": "Would it be untrue to say that the badge is issued to every volunteer?"},
{"qid": "qa18006bebc", "question_a": "Does the manual describe the safety checks?", "question_b": "Is it wrong to say that the manual describes the safety checks?"}
]
```
