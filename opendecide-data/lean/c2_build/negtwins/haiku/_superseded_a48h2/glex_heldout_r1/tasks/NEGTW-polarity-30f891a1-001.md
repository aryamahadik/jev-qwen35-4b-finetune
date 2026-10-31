# Haiku G-LEX read NEGTW-polarity-30f891a1-001 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_heldout_r1/answers/NEGTW-polarity-30f891a1-001.json

The answer is one JSON list with exactly 12 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (12; one JSON object per line)

```json
[
{"qid": "q5a5ac6b21b", "question_a": "Is the bid lodged on time?", "question_b": "Is the bid unlodged on time?"},
{"qid": "q66fe08f8e3", "question_a": "Is the ticket unredeemed at the gate?", "question_b": "Is the ticket redeemed at the gate?"},
{"qid": "qf2847ea8f4", "question_a": "Is the contract ratified by the union?", "question_b": "Is the contract unratified by the union?"},
{"qid": "q4e79a6cdbd", "question_a": "Does the folder contain the signed forms?", "question_b": "Would it be mistaken that the folder contains the signed forms?"},
{"qid": "q880859455f", "question_a": "Is the poem unascribed to the monk?", "question_b": "Is the poem ascribed to the monk?"},
{"qid": "q7a5d562c5f", "question_a": "Is the deposit unlodged with the court?", "question_b": "Is the deposit lodged with the court?"},
{"qid": "q97afc4339f", "question_a": "Is the document written in plain language?", "question_b": "Is it inaccurate that the document is written in plain language?"},
{"qid": "q9298e9160e", "question_a": "Is the institute unaccredited by the council?", "question_b": "Is the institute accredited by the council?"},
{"qid": "q3005263d33", "question_a": "Is the accord ratified by parliament?", "question_b": "Is it true that the accord is not unratified by parliament?"},
{"qid": "q13f8a1baa7", "question_a": "Is the stock option unvested for the new hire?", "question_b": "Is the stock option vested for the new hire?"},
{"qid": "qd2f427fbe0", "question_a": "Is the laboratory accredited for testing?", "question_b": "Is the laboratory unaccredited for testing?"},
{"qid": "qea06752521", "question_a": "Is the translator uncertified by the court?", "question_b": "Is the translator certified by the court?"}
]
```
