# Haiku G-LEX read NEGTW-polarity-270ef05d-000 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_train_r1/answers/NEGTW-polarity-270ef05d-000.json

The answer is one JSON list with exactly 50 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (50; one JSON object per line)

```json
[
{"qid": "q4b3d695925", "question_a": "Does the handbook permit personal calls at work?", "question_b": "Does the handbook prohibit personal calls at work?"},
{"qid": "qa453d009d0", "question_a": "Does the course include an exam?", "question_b": "Would it be false that the course includes an exam?"},
{"qid": "q381d580e4f", "question_a": "Is the guide intended for beginners?", "question_b": "Is the reading accurate that the guide is intended for beginners?"},
{"qid": "q5bcc996ae5", "question_a": "Does the shop have a returns desk?", "question_b": "Is it incorrect that the shop has a returns desk?"},
{"qid": "q610bc09bc8", "question_a": "Is the pool available after six?", "question_b": "Is it mistaken that the pool is available after six?"},
{"qid": "q2669eac595", "question_a": "Is the library restricted to members?", "question_b": "Is the library unrestricted to members?"},
{"qid": "qd416d9e6f3", "question_a": "Does the ticket permit an exemption?", "question_b": "Is it true that the ticket does not ban an exemption?"},
{"qid": "qc9b4109f76", "question_a": "Does the bag contain a receipt?", "question_b": "Does the report establish that the bag contains a receipt?"},
{"qid": "qb6c6cf9d9e", "question_a": "Are the tickets restricted to residents?", "question_b": "Is it true that the tickets are not unrestricted to residents?"},
{"qid": "q31cd81898c", "question_a": "Does the badge permit entry after six pm?", "question_b": "Does the badge prohibit entry after six pm?"},
{"qid": "qe2982e64d1", "question_a": "Does the lesson plan involve group work?", "question_b": "Does the record show something untrue that the lesson plan involves group work?"},
{"qid": "q943fb214c8", "question_a": "Is the offer valid for new customers?", "question_b": "Would it be mistaken that the offer is valid for new customers?"},
{"qid": "q8a7c6ae574", "question_a": "Does the code allow the extension?", "question_b": "Is it true that the code does not forbid the extension?"},
{"qid": "q2bed8e4847", "question_a": "Is the cost included in the fare?", "question_b": "Is the cost excluded in the fare?"},
{"qid": "q3228075feb", "question_a": "Does the cake contain eggs?", "question_b": "Does the notice confirm that the cake contains eggs?"},
{"qid": "qfc2dc92eaa", "question_a": "Is the camping spot allowed near the river?", "question_b": "Is the camping spot forbidden near the river?"},
{"qid": "qa66c695bf3", "question_a": "Does the shop have a returns desk?", "question_b": "Is it untrue that the shop has a returns desk?"},
{"qid": "q206a7e84a7", "question_a": "Is the answer given in the first paragraph?", "question_b": "Does this claim hold that the answer is given in the first paragraph?"},
{"qid": "q18c4e64e4d", "question_a": "Does the policy say the refund period?", "question_b": "Does the policy omit the refund period?"},
{"qid": "q2c23b4281e", "question_a": "Does the label ban a pet?", "question_b": "Does the label permit a pet?"},
{"qid": "q016496af72", "question_a": "Does the report show the total?", "question_b": "Is it true that the report does not omit the total?"},
{"qid": "qd28f21fa8a", "question_a": "Does the directory omit the new clinic?", "question_b": "Does the directory list the new clinic?"},
{"qid": "q1e8ef8d03c", "question_a": "Does the rule allow the practice?", "question_b": "Does the rule forbid the practice?"},
{"qid": "qd5c14b83d0", "question_a": "Is the number unconfirmed by the ledger?", "question_b": "Is the number confirmed by the ledger?"},
{"qid": "q1e83656d80", "question_a": "Is the locker unlocked for staff?", "question_b": "Is it true that the locker is not locked for staff?"},
{"qid": "q686bfebe3a", "question_a": "Does the sign permit cycling on the path?", "question_b": "Is it true that the sign does not prohibit cycling on the path?"},
{"qid": "q685c8df2fd", "question_a": "Is the plan unlimited in size?", "question_b": "Is the plan limited in size?"},
{"qid": "q9607e76583", "question_a": "Does the bundle include a manual?", "question_b": "Is it inaccurate that the bundle includes a manual?"},
{"qid": "q406074e92c", "question_a": "Does the lesson plan involve group work?", "question_b": "Does this claim hold that the lesson plan involves group work?"},
{"qid": "q3a4e6611eb", "question_a": "Is the report based on a public survey?", "question_b": "Does the notice confirm that the report is based on a public survey?"},
{"qid": "qbac60bfcf5", "question_a": "Does the form omit a date?", "question_b": "Does the form mention a date?"},
{"qid": "q9425a06dd4", "question_a": "Is the picnic permitted in the park?", "question_b": "Is it true that the picnic is not prohibited in the park?"},
{"qid": "qdebc7e2b1d", "question_a": "Is the supply limited in volume?", "question_b": "Is the supply unlimited in volume?"},
{"qid": "qff26d174db", "question_a": "Does the poster invite visitors to the open day?", "question_b": "Is the reading accurate that the poster invites visitors to the open day?"},
{"qid": "qd8bbb5adb5", "question_a": "Does the contract ban a merger?", "question_b": "Does the contract permit a merger?"},
{"qid": "q2523ee895b", "question_a": "Is the phone number optional on the form?", "question_b": "Is the phone number required on the form?"},
{"qid": "q3e86dcf788", "question_a": "Does the email announce a change of venue?", "question_b": "Would the facts show that the email announces a change of venue?"},
{"qid": "q17b8cea6ca", "question_a": "Is the drone prohibited over the site?", "question_b": "Is the drone permitted over the site?"},
{"qid": "qae9d1224ef", "question_a": "Is the label listed in the table?", "question_b": "Is it true that the label is not unlisted in the table?"},
{"qid": "qe115aad472", "question_a": "Is the drink included in the ticket?", "question_b": "Is it true that the drink is not excluded in the ticket?"},
{"qid": "q2e5c39b16d", "question_a": "Does the record name the patient?", "question_b": "Is it true that the record does not omit the patient?"},
{"qid": "q11939d706d", "question_a": "Is the study supported by the trials?", "question_b": "Is it true that the study is not unsupported by the trials?"},
{"qid": "q42217e6d29", "question_a": "Does the menu contain a vegetarian dish?", "question_b": "Would the record show that the menu contains a vegetarian dish?"},
{"qid": "qe3a3902b3f", "question_a": "Does the review recommend the product to families?", "question_b": "Does the report establish that the review recommends the product to families?"},
{"qid": "q43fcc98587", "question_a": "Is the entrance located on the east side?", "question_b": "Would you call it untrue that the entrance is located on the east side?"},
{"qid": "qf592a79bfd", "question_a": "Is the device disallowed on the network?", "question_b": "Is the device allowed on the network?"},
{"qid": "q730f12efe8", "question_a": "Does the form request a phone number?", "question_b": "Would the record show that the form requests a phone number?"},
{"qid": "q8905f3f1ca", "question_a": "Is the cabinet unlocked in the lab?", "question_b": "Is the cabinet locked in the lab?"},
{"qid": "qae6f878a74", "question_a": "Does the policy include a limit?", "question_b": "Is it true that the policy does not exclude a limit?"},
{"qid": "qd883cfb9c9", "question_a": "Does the bag contain a receipt?", "question_b": "Is it mistaken that the bag contains a receipt?"}
]
```
