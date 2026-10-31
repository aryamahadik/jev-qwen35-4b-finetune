# Haiku G-LEX read NEGTW-polarity-270ef05d-003 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_train_r1/answers/NEGTW-polarity-270ef05d-003.json

The answer is one JSON list with exactly 28 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (28; one JSON object per line)

```json
[
{"qid": "qb9c44c52f3", "question_a": "Does the notice provide a copy of the order?", "question_b": "Is it true that the notice does not omit a copy of the order?"},
{"qid": "q4463020576", "question_a": "Does the pamphlet have a section on safety?", "question_b": "Does it hold that the pamphlet has a section on safety?"},
{"qid": "qebbc635815", "question_a": "Is the feed unrestricted for friends?", "question_b": "Is the feed restricted for friends?"},
{"qid": "qb1f55a3c61", "question_a": "Does the label omit a warning?", "question_b": "Does the label mention a warning?"},
{"qid": "q0538cb90ba", "question_a": "Is the parking lot available to visitors?", "question_b": "Would it be inaccurate that the parking lot is available to visitors?"},
{"qid": "q2846bbe618", "question_a": "Does the bag contain a receipt?", "question_b": "Is it untrue that the bag contains a receipt?"},
{"qid": "qc7a3e632df", "question_a": "Is the sample provided at no cost?", "question_b": "Would the record confirm that the sample is provided at no cost?"},
{"qid": "q71405da249", "question_a": "Is the car allowed in the lot?", "question_b": "Is the car disallowed in the lot?"},
{"qid": "q24e5fd0905", "question_a": "Does the offer include free delivery?", "question_b": "Is it inaccurate that the offer includes free delivery?"},
{"qid": "qfc8c6092cd", "question_a": "Does the menu contain a vegetarian dish?", "question_b": "Does the record show something untrue that the menu contains a vegetarian dish?"},
{"qid": "qf6e74a8f24", "question_a": "Is the letter unsigned by the chief?", "question_b": "Is the letter signed by the chief?"},
{"qid": "q95c70bccba", "question_a": "Is the email address required for sign-up?", "question_b": "Is the email address optional for sign-up?"},
{"qid": "qb54bd721bd", "question_a": "Is the quota limited in scope?", "question_b": "Is the quota unlimited in scope?"},
{"qid": "q53241f4bba", "question_a": "Are the students allowed to leave early?", "question_b": "Is it true that the students are not disallowed to leave early?"},
{"qid": "qdae4240a5f", "question_a": "Does the kit contain spare batteries?", "question_b": "Would the record show that the kit contains spare batteries?"},
{"qid": "q52f750e87d", "question_a": "Is the car unlocked in the lot?", "question_b": "Is the car locked in the lot?"},
{"qid": "qef5f6cf7ba", "question_a": "Does the handbook allow the late entry?", "question_b": "Does the handbook forbid the late entry?"},
{"qid": "q597e6c7fe1", "question_a": "Does the label omit the dose?", "question_b": "Does the label show the dose?"},
{"qid": "qdfc8749795", "question_a": "Is the museum free for children?", "question_b": "Is it mistaken that the museum is free for children?"},
{"qid": "qcefd9435e9", "question_a": "Does the form say the deadline?", "question_b": "Is it true that the form does not omit the deadline?"},
{"qid": "qb8934eaab8", "question_a": "Does the file contain a password?", "question_b": "Is it incorrect that the file contains a password?"},
{"qid": "q875bb76cf0", "question_a": "Is the quota limited in scope?", "question_b": "Is it true that the quota is not unlimited in scope?"},
{"qid": "q9183654907", "question_a": "Is the sale permitted in this zone?", "question_b": "Is the sale prohibited in this zone?"},
{"qid": "qcde3c2c0fc", "question_a": "Does the ticket omit the seat?", "question_b": "Does the ticket show the seat?"},
{"qid": "qf3fe2a7bda", "question_a": "Is the room planned for a larger group?", "question_b": "Would it be false that the room is planned for a larger group?"},
{"qid": "q1dcd471b0d", "question_a": "Does the rule permit pets in the building?", "question_b": "Would the facts show that the rule permits pets in the building?"},
{"qid": "qb26a26e86a", "question_a": "Is the breakfast excluded from the stay?", "question_b": "Is the breakfast included from the stay?"},
{"qid": "q8b59cfcea6", "question_a": "Does the folder contain the signed forms?", "question_b": "Would it be mistaken that the folder contains the signed forms?"}
]
```
