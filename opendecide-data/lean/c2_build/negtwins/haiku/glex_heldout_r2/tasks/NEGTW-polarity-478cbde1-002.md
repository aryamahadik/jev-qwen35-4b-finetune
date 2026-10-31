# Haiku G-LEX read NEGTW-polarity-478cbde1-002 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_heldout_r2/answers/NEGTW-polarity-478cbde1-002.json

The answer is one JSON list with exactly 16 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (16; one JSON object per line)

```json
[
{"qid": "qa5143df713", "question_a": "Is the loan approved by the committee?", "question_b": "Would it be wrong to say that the loan is approved by the committee?"},
{"qid": "q2c9da6e545", "question_a": "Is the land right vested in the tribe?", "question_b": "Is the land right unvested in the tribe?"},
{"qid": "q2f3e21d4bf", "question_a": "Is the boiler certified after inspection?", "question_b": "Is it true that the boiler is not uncertified after inspection?"},
{"qid": "q14f5fab9f7", "question_a": "Does the bundle include a manual?", "question_b": "Is it inaccurate that the bundle includes a manual?"},
{"qid": "q53f5f0211f", "question_a": "Does the drawer contain a spare key?", "question_b": "Is it untrue to say that the drawer contains a spare key?"},
{"qid": "qf34df718b4", "question_a": "Is the tender unsealed in a box?", "question_b": "Is the tender sealed in a box?"},
{"qid": "q3bdfc57503", "question_a": "Does the statement specify the payment date?", "question_b": "Is it wrong to say that the statement specifies the payment date?"},
{"qid": "qdadd5ee92a", "question_a": "Is the institute unaccredited by the council?", "question_b": "Is the institute accredited by the council?"},
{"qid": "q30de271aab", "question_a": "Is the badge issued to every volunteer?", "question_b": "Would it be untrue to say that the badge is issued to every volunteer?"},
{"qid": "q4b432daa06", "question_a": "Is the offer valid for new customers?", "question_b": "Is it untrue to say that the offer is valid for new customers?"},
{"qid": "qdf04303460", "question_a": "Does the trail have a marked entrance?", "question_b": "Would it be untrue to say that the trail has a marked entrance?"},
{"qid": "q848757f3a0", "question_a": "Is the poem unascribed to the monk?", "question_b": "Is the poem ascribed to the monk?"},
{"qid": "qe51c93f2f2", "question_a": "Does the schedule contain a tariff?", "question_b": "Is it true that the schedule does not exclude a tariff?"},
{"qid": "q1c99ee15ef", "question_a": "Does the letter contain an offer?", "question_b": "Would it be wrong that the letter contains an offer?"},
{"qid": "qea7c08a6fd", "question_a": "Is the tablet ascribed to the priest?", "question_b": "Is it true that the tablet is not unascribed to the priest?"},
{"qid": "q3518df1a56", "question_a": "Is the programme unaccredited in the state?", "question_b": "Is the programme accredited in the state?"}
]
```
