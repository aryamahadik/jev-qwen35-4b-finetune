# Haiku G-LEX read NEGTW-polarity-5f788008-003 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_train_r2/answers/NEGTW-polarity-5f788008-003.json

The answer is one JSON list with exactly 28 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (28; one JSON object per line)

```json
[
{"qid": "qcc78dbc671", "question_a": "Does the bag contain a receipt?", "question_b": "Is it untrue that the bag contains a receipt?"},
{"qid": "q7b77044ea8", "question_a": "Is the report based on a public survey?", "question_b": "Does the notice confirm that the report is based on a public survey?"},
{"qid": "q58af208537", "question_a": "Does the email announce a change of venue?", "question_b": "Would the facts show that the email announces a change of venue?"},
{"qid": "qac6bd1618c", "question_a": "Is the plan unlimited in size?", "question_b": "Is the plan limited in size?"},
{"qid": "q5d9089d2d4", "question_a": "Is the cost included in the fare?", "question_b": "Is the cost excluded in the fare?"},
{"qid": "qe7174f52cf", "question_a": "Does the form say the deadline?", "question_b": "Is it true that the form does not omit the deadline?"},
{"qid": "qc38e2b2ef6", "question_a": "Is the summary unsupported by the source?", "question_b": "Is the summary supported by the source?"},
{"qid": "q21f6c76589", "question_a": "Does the update address the login problem?", "question_b": "Would the facts show that the update addresses the login problem?"},
{"qid": "q805ab0b3a2", "question_a": "Is the parking lot available to visitors?", "question_b": "Would it be inaccurate that the parking lot is available to visitors?"},
{"qid": "q53cbeea753", "question_a": "Does the email announce a change of venue?", "question_b": "Is it wrong that the email announces a change of venue?"},
{"qid": "q6230ef8cf7", "question_a": "Is the parking excluded from the rate?", "question_b": "Is the parking included from the rate?"},
{"qid": "qd679ed2785", "question_a": "Does the plan have a backup route?", "question_b": "Would it be inaccurate that the plan has a backup route?"},
{"qid": "q0dba2e8ff7", "question_a": "Does the brochure list the event dates?", "question_b": "Does the brochure omit the event dates?"},
{"qid": "q524c66c67d", "question_a": "Does the policy include a limit?", "question_b": "Is it true that the policy does not exclude a limit?"},
{"qid": "qd8e6d6360a", "question_a": "Does the notice provide a copy of the order?", "question_b": "Is it true that the notice does not omit a copy of the order?"},
{"qid": "q5beed45c7a", "question_a": "Does the agreement require a written notice?", "question_b": "Would you call it untrue that the agreement requires a written notice?"},
{"qid": "q2678e5bf5b", "question_a": "Is the pet disallowed on the bus?", "question_b": "Is the pet allowed on the bus?"},
{"qid": "q82d3071d12", "question_a": "Is the study supported by the trials?", "question_b": "Is it true that the study is not unsupported by the trials?"},
{"qid": "q549254b347", "question_a": "Is the parking permitted on this street?", "question_b": "Is the parking prohibited on this street?"},
{"qid": "q14bbe621b4", "question_a": "Does the record name the vendor?", "question_b": "Does the record omit the vendor?"},
{"qid": "q6562eeeea4", "question_a": "Does the index list the older reports?", "question_b": "Does the index omit the older reports?"},
{"qid": "qc33e8f2bba", "question_a": "Is the figure confirmed by the audit?", "question_b": "Is the figure unconfirmed by the audit?"},
{"qid": "q3a12ba1678", "question_a": "Is the locker locked for staff?", "question_b": "Is the locker unlocked for staff?"},
{"qid": "qbdcad40531", "question_a": "Does the record name the patient?", "question_b": "Is it true that the record does not omit the patient?"},
{"qid": "q12069fbddc", "question_a": "Does the label omit a warning?", "question_b": "Does the label mention a warning?"},
{"qid": "q9ba921b575", "question_a": "Does the label ban a pet?", "question_b": "Does the label permit a pet?"},
{"qid": "qfe298a9676", "question_a": "Does the shop have a returns desk?", "question_b": "Is it incorrect that the shop has a returns desk?"},
{"qid": "qc40b609e27", "question_a": "Does the plan have a backup route?", "question_b": "Would it be right that the plan has a backup route?"}
]
```
