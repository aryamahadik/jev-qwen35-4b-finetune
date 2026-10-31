# Haiku G-LEX read NEGTW-polarity-17d0720b-002 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_train_r1/answers/NEGTW-polarity-17d0720b-002.json

The answer is one JSON list with exactly 45 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (45; one JSON object per line)

```json
[
{"qid": "q67aa02ad20", "question_a": "Is the document written in plain language?", "question_b": "Is it inaccurate that the document is written in plain language?"},
{"qid": "qe001c5a915", "question_a": "Does the bag contain a receipt?", "question_b": "Is it untrue that the bag contains a receipt?"},
{"qid": "q9eaa60b74b", "question_a": "Is the photo ID required at check-in?", "question_b": "Is the photo ID optional at check-in?"},
{"qid": "q519bfcbdf7", "question_a": "Does the ticket mention a refund?", "question_b": "Is it true that the ticket does not omit a refund?"},
{"qid": "qd9aac64cb3", "question_a": "Is the form unsigned by the parent?", "question_b": "Is the form signed by the parent?"},
{"qid": "qb639edde24", "question_a": "Does the drawer contain a spare key?", "question_b": "Would it be right that the drawer contains a spare key?"},
{"qid": "qebbe71c8a1", "question_a": "Does the ticket show the seat?", "question_b": "Does the ticket omit the seat?"},
{"qid": "qc904f74fc4", "question_a": "Is the car unlocked in the lot?", "question_b": "Is the car locked in the lot?"},
{"qid": "q4fbb370a97", "question_a": "Is the camping spot allowed near the river?", "question_b": "Is the camping spot forbidden near the river?"},
{"qid": "qabb3f7e98f", "question_a": "Is the phone number required on the form?", "question_b": "Is it true that the phone number is not optional on the form?"},
{"qid": "q0de03b6c60", "question_a": "Is the summary unsupported by the source?", "question_b": "Is the summary supported by the source?"},
{"qid": "q729051664c", "question_a": "Does the index list the older reports?", "question_b": "Does the index omit the older reports?"},
{"qid": "qfe3e311f99", "question_a": "Is the late checkout allowed for guests?", "question_b": "Is it true that the late checkout is not forbidden for guests?"},
{"qid": "q9b1b26ad9c", "question_a": "Does the report contain a fee?", "question_b": "Does the report lack a fee?"},
{"qid": "qdc85130862", "question_a": "Is the room planned for a larger group?", "question_b": "Would it be false that the room is planned for a larger group?"},
{"qid": "q7d362372d3", "question_a": "Is the picnic permitted in the park?", "question_b": "Is it true that the picnic is not prohibited in the park?"},
{"qid": "qc6d35edef1", "question_a": "Is the area restricted after dark?", "question_b": "Is the area unrestricted after dark?"},
{"qid": "qf85359e3a1", "question_a": "Is the forecast confirmed by the data?", "question_b": "Is it true that the forecast is not unconfirmed by the data?"},
{"qid": "q4ba8ac56a2", "question_a": "Does the label contain a warning?", "question_b": "Is it true that the label does not lack a warning?"},
{"qid": "q5eaf6ea09e", "question_a": "Is the pet disallowed on the bus?", "question_b": "Is the pet allowed on the bus?"},
{"qid": "qdf01aaafe0", "question_a": "Does the label omit the dose?", "question_b": "Does the label show the dose?"},
{"qid": "q1e85687aaf", "question_a": "Is the record unsupported by the audit?", "question_b": "Is the record supported by the audit?"},
{"qid": "qad95585535", "question_a": "Does the letter include a meeting?", "question_b": "Does the letter exclude a meeting?"},
{"qid": "qa913f6580b", "question_a": "Does the record name the vendor?", "question_b": "Does the record omit the vendor?"},
{"qid": "q59d9e9bac6", "question_a": "Is the figure confirmed by the audit?", "question_b": "Is the figure unconfirmed by the audit?"},
{"qid": "qa022d10a76", "question_a": "Does the code allow the extension?", "question_b": "Is it true that the code does not forbid the extension?"},
{"qid": "qe81a5dbd0c", "question_a": "Is the record supported by the audit?", "question_b": "Is the record unsupported by the audit?"},
{"qid": "qdd6b456eea", "question_a": "Does the handbook allow the late entry?", "question_b": "Does the handbook forbid the late entry?"},
{"qid": "q413f0c0d06", "question_a": "Is the locker locked for staff?", "question_b": "Is the locker unlocked for staff?"},
{"qid": "qe4a8438b97", "question_a": "Does the report say the test result?", "question_b": "Does the report omit the test result?"},
{"qid": "q9afe592441", "question_a": "Does the record name the buyer?", "question_b": "Does the record omit the buyer?"},
{"qid": "q6a8efdbf9c", "question_a": "Is the plan unlimited in size?", "question_b": "Is the plan limited in size?"},
{"qid": "q9d0323e958", "question_a": "Is the offer valid for new customers?", "question_b": "Would it be mistaken that the offer is valid for new customers?"},
{"qid": "q9a3357f350", "question_a": "Is the car locked in the lot?", "question_b": "Is the car unlocked in the lot?"},
{"qid": "q4b253ff5ff", "question_a": "Is the email address required for sign-up?", "question_b": "Is the email address optional for sign-up?"},
{"qid": "q469a9d4920", "question_a": "Does the notice omit a fee amount?", "question_b": "Does the notice provide a fee amount?"},
{"qid": "q6fd9a32cf1", "question_a": "Does the handbook permit personal calls at work?", "question_b": "Does the handbook prohibit personal calls at work?"},
{"qid": "qaaf0c6055a", "question_a": "Is the rule supported by the study?", "question_b": "Is the rule unsupported by the study?"},
{"qid": "q9e3023888d", "question_a": "Is the photo allowed in the gallery?", "question_b": "Is the photo disallowed in the gallery?"},
{"qid": "q61f3a797e6", "question_a": "Is the photo ID optional at check-in?", "question_b": "Is the photo ID required at check-in?"},
{"qid": "q6f5005c604", "question_a": "Is the rule covered by the audit?", "question_b": "Is the rule uncovered by the audit?"},
{"qid": "q5835f6eee4", "question_a": "Is the drone prohibited over the site?", "question_b": "Is the drone permitted over the site?"},
{"qid": "q0ed6840232", "question_a": "Does the contract ban a merger?", "question_b": "Does the contract permit a merger?"},
{"qid": "qcf1a482145", "question_a": "Does the memo contain a budget?", "question_b": "Does the memo lack a budget?"},
{"qid": "q9ae6290334", "question_a": "Does the brochure list the event dates?", "question_b": "Does the brochure omit the event dates?"}
]
```
