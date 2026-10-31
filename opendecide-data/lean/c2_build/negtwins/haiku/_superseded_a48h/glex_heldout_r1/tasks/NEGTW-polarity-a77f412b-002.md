# Haiku G-LEX read NEGTW-polarity-a77f412b-002 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_heldout_r1/answers/NEGTW-polarity-a77f412b-002.json

The answer is one JSON list with exactly 4 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (4; one JSON object per line)

```json
[
{"qid": "q0ad15924ff", "question_a": "Is the land right vested in the tribe?", "question_b": "Is the land right unvested in the tribe?"},
{"qid": "qa4851a8c7e", "question_a": "Is the plate unaffixed to the frame?", "question_b": "Is the plate affixed to the frame?"},
{"qid": "qb30ee29fce", "question_a": "Does the shop have a returns desk?", "question_b": "Is it attested that the shop has a returns desk?"},
{"qid": "qf8988c7050", "question_a": "Is the clinic accredited by the ministry?", "question_b": "Is the clinic unaccredited by the ministry?"}
]
```
