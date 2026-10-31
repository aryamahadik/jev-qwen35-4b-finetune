# Haiku G-LEX read NEGTW-polarity-19b9b467-002 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_train_r2/answers/NEGTW-polarity-19b9b467-002.json

The answer is one JSON list with exactly 50 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (50; one JSON object per line)

```json
[
{"qid": "q969fbb0c45", "question_a": "Does the contract ban a merger?", "question_b": "Does the contract permit a merger?"},
{"qid": "q61ca2c53f6", "question_a": "Is the product shown in the photo?", "question_b": "Is it false to say that the product is shown in the photo?"},
{"qid": "qc2b8023507", "question_a": "Does the statement specify the payment date?", "question_b": "Is it wrong to say that the statement specifies the payment date?"},
{"qid": "q93f93202c5", "question_a": "Does the plan have a backup route?", "question_b": "Would it be inaccurate that the plan has a backup route?"},
{"qid": "q43e34a7564", "question_a": "Does the sign allow visitors to park here?", "question_b": "Would it be incorrect that the sign allows visitors to park here?"},
{"qid": "qc4b5898822", "question_a": "Does the form request a phone number?", "question_b": "Would it be incorrect that the form requests a phone number?"},
{"qid": "qaf3dbfab1d", "question_a": "Does the notice omit a fee amount?", "question_b": "Does the notice provide a fee amount?"},
{"qid": "qdad15072c6", "question_a": "Is the summary unsupported by the source?", "question_b": "Is the summary supported by the source?"},
{"qid": "q70dc72c847", "question_a": "Is the rule supported by the study?", "question_b": "Is the rule unsupported by the study?"},
{"qid": "q4e4b164c73", "question_a": "Is the photo allowed in the gallery?", "question_b": "Is the photo disallowed in the gallery?"},
{"qid": "qf45fc9f2a8", "question_a": "Does the bag contain a receipt?", "question_b": "Is it untrue that the bag contains a receipt?"},
{"qid": "q43ab7287da", "question_a": "Is the parking excluded from the rate?", "question_b": "Is the parking included from the rate?"},
{"qid": "qb804565291", "question_a": "Is the budget unlimited in amount?", "question_b": "Is the budget limited in amount?"},
{"qid": "q85b336642c", "question_a": "Does the form omit a date?", "question_b": "Does the form mention a date?"},
{"qid": "q5e2a480481", "question_a": "Does the rule allow the practice?", "question_b": "Does the rule forbid the practice?"},
{"qid": "q0de3540d73", "question_a": "Does the lesson plan involve group work?", "question_b": "Would it be untrue that the lesson plan involves group work?"},
{"qid": "q9fee1fe7c0", "question_a": "Does the menu show the price?", "question_b": "Does the menu omit the price?"},
{"qid": "qabf896f7f6", "question_a": "Does the report include a summary table?", "question_b": "Is it inaccurate to say that the report includes a summary table?"},
{"qid": "q39546e2c91", "question_a": "Does the drawer contain a spare key?", "question_b": "Is it mistaken to say that the drawer contains a spare key?"},
{"qid": "q84d93ff468", "question_a": "Is the check signed by the payee?", "question_b": "Is it true that the check is not unsigned by the payee?"},
{"qid": "q8adb1477f5", "question_a": "Is the parking lot available to visitors?", "question_b": "Is it incorrect to say that the parking lot is available to visitors?"},
{"qid": "qb1868c8d14", "question_a": "Is the badge issued to every volunteer?", "question_b": "Would it be untrue to say that the badge is issued to every volunteer?"},
{"qid": "qd3860677f6", "question_a": "Is the sale permitted in this zone?", "question_b": "Is the sale prohibited in this zone?"},
{"qid": "q31d3293d7f", "question_a": "Does the badge permit entry after six pm?", "question_b": "Does the badge prohibit entry after six pm?"},
{"qid": "q42e4b9faa7", "question_a": "Does the letter confirm the new meeting room?", "question_b": "Would it be mistaken to say that the letter confirms the new meeting room?"},
{"qid": "qedbd6b86e6", "question_a": "Does the ticket include a meal?", "question_b": "Would it be incorrect to say that the ticket includes a meal?"},
{"qid": "q21ecfbdff6", "question_a": "Does the regulation forbid the export?", "question_b": "Does the regulation allow the export?"},
{"qid": "q3075f3f50f", "question_a": "Does the website provide a refund option?", "question_b": "Is it incorrect to say that the website provides a refund option?"},
{"qid": "q11adc768ec", "question_a": "Is the entry prohibited for minors?", "question_b": "Is the entry permitted for minors?"},
{"qid": "qca1d59e817", "question_a": "Does the guide explain how to reset the device?", "question_b": "Is it false to say that the guide explains how to reset the device?"},
{"qid": "qf58168158c", "question_a": "Is the locker locked for staff?", "question_b": "Is the locker unlocked for staff?"},
{"qid": "qadf5bf70e2", "question_a": "Does the course include an exam?", "question_b": "Would it be false that the course includes an exam?"},
{"qid": "q98fdc63712", "question_a": "Does the letter contain an offer?", "question_b": "Would it be false that the letter contains an offer?"},
{"qid": "qe95357af24", "question_a": "Does the letter permit a sublet?", "question_b": "Does the letter ban a sublet?"},
{"qid": "q8cb0e5ca21", "question_a": "Is the study supported by the trials?", "question_b": "Is it true that the study is not unsupported by the trials?"},
{"qid": "q61a4c82634", "question_a": "Is the car unlocked in the lot?", "question_b": "Is the car locked in the lot?"},
{"qid": "q727c5eea05", "question_a": "Is the badge issued to every volunteer?", "question_b": "Is it right that the badge is issued to every volunteer?"},
{"qid": "q067a5599a8", "question_a": "Does the letter include a meeting?", "question_b": "Does the letter exclude a meeting?"},
{"qid": "qf3810d5155", "question_a": "Is the backup file forbidden on the shared drive?", "question_b": "Is the backup file allowed on the shared drive?"},
{"qid": "q00b09c629e", "question_a": "Is the parking lot available to visitors?", "question_b": "Would it be inaccurate that the parking lot is available to visitors?"},
{"qid": "qb18a6e541a", "question_a": "Does the sign allow visitors to park here?", "question_b": "Would it be incorrect to say that the sign allows visitors to park here?"},
{"qid": "qc3151069e3", "question_a": "Does the label omit a warning?", "question_b": "Does the label mention a warning?"},
{"qid": "q804d83ca59", "question_a": "Does the package include a charger?", "question_b": "Is it correct to say that the package includes a charger?"},
{"qid": "q22945ecc23", "question_a": "Is the fee included in the ticket price?", "question_b": "Would it be accurate that the fee is included in the ticket price?"},
{"qid": "qe31dd8afb1", "question_a": "Does the report exclude a fee?", "question_b": "Does the report include a fee?"},
{"qid": "q7bb424dc29", "question_a": "Is the drone prohibited over the site?", "question_b": "Is the drone permitted over the site?"},
{"qid": "qfffc16dcb8", "question_a": "Does the label state the country of origin?", "question_b": "Would it be true that the label states the country of origin?"},
{"qid": "q9a8fe64930", "question_a": "Does the shop have a returns desk?", "question_b": "Is it untrue that the shop has a returns desk?"},
{"qid": "qef1e61e49e", "question_a": "Is the document written in plain language?", "question_b": "Is it inaccurate that the document is written in plain language?"},
{"qid": "q2d903461ae", "question_a": "Is the trail closed in winter?", "question_b": "Is it wrong to say that the trail is closed in winter?"}
]
```
