# Haiku G-LEX read NEGTW-polarity-270ef05d-002 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_train_r1/answers/NEGTW-polarity-270ef05d-002.json

The answer is one JSON list with exactly 50 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (50; one JSON object per line)

```json
[
{"qid": "qe4a22f5a9e", "question_a": "Is the summary unsupported by the source?", "question_b": "Is the summary supported by the source?"},
{"qid": "q544610bd22", "question_a": "Does the notice provide a date of issue?", "question_b": "Does the notice omit a date of issue?"},
{"qid": "q97481e777e", "question_a": "Is the backup file allowed on the shared drive?", "question_b": "Is the backup file forbidden on the shared drive?"},
{"qid": "q0b7de0702d", "question_a": "Does the report name the person who signed it?", "question_b": "Is the reading accurate that the report names the person who signed it?"},
{"qid": "qdf208e47de", "question_a": "Does the trail have a marked entrance?", "question_b": "Would a reviewer agree that the trail has a marked entrance?"},
{"qid": "q8f77eb26c8", "question_a": "Does the file contain a password?", "question_b": "Would the record confirm that the file contains a password?"},
{"qid": "q6d0eec98e2", "question_a": "Does the ticket show the seat?", "question_b": "Does the ticket omit the seat?"},
{"qid": "q2ae95f631d", "question_a": "Does the statement specify the payment date?", "question_b": "Does it hold that the statement specifies the payment date?"},
{"qid": "qb4aa9a1e55", "question_a": "Is the photo ID required at check-in?", "question_b": "Is the photo ID optional at check-in?"},
{"qid": "q1054c6061f", "question_a": "Is the parking permit forbidden on this street?", "question_b": "Is the parking permit allowed on this street?"},
{"qid": "qd9f917e3ec", "question_a": "Is the document written in plain language?", "question_b": "Is it inaccurate that the document is written in plain language?"},
{"qid": "q76f9a0d4e7", "question_a": "Is the record supported by the audit?", "question_b": "Is the record unsupported by the audit?"},
{"qid": "q16e1979cd9", "question_a": "Does the review recommend the product to families?", "question_b": "Is it untrue that the review recommends the product to families?"},
{"qid": "q16653666a8", "question_a": "Is the parking excluded from the rate?", "question_b": "Is the parking included from the rate?"},
{"qid": "q574b1df00f", "question_a": "Is the waiver signed before the trip?", "question_b": "Is the waiver unsigned before the trip?"},
{"qid": "q8b4be3484c", "question_a": "Is the pet disallowed on the bus?", "question_b": "Is the pet allowed on the bus?"},
{"qid": "qb8431561ef", "question_a": "Is the locker locked for staff?", "question_b": "Is the locker unlocked for staff?"},
{"qid": "qc05166989b", "question_a": "Does the shop have a returns desk?", "question_b": "Would you call it untrue that the shop has a returns desk?"},
{"qid": "q2b390717ed", "question_a": "Does the price include tax?", "question_b": "Is it wrong that the price includes tax?"},
{"qid": "q8783d92307", "question_a": "Is the budget unlimited in amount?", "question_b": "Is the budget limited in amount?"},
{"qid": "q89157ed27f", "question_a": "Is the record unsupported by the audit?", "question_b": "Is the record supported by the audit?"},
{"qid": "q5ae649f743", "question_a": "Does the brochure omit the event dates?", "question_b": "Does the brochure list the event dates?"},
{"qid": "qd765646e66", "question_a": "Is the form signed by the parent?", "question_b": "Is the form unsigned by the parent?"},
{"qid": "q3de968cbad", "question_a": "Does the letter mention a meeting?", "question_b": "Does the letter omit a meeting?"},
{"qid": "qc92771e574", "question_a": "Does the file contain a password?", "question_b": "Would a reviewer agree that the file contains a password?"},
{"qid": "qc5c51dfa6d", "question_a": "Does the letter contain an offer?", "question_b": "Would it be false that the letter contains an offer?"},
{"qid": "q3d4828d6f4", "question_a": "Does the index list the older reports?", "question_b": "Does the index omit the older reports?"},
{"qid": "qddd3b7f4e6", "question_a": "Is the class eligible for the discount?", "question_b": "Does the notice confirm that the class is eligible for the discount?"},
{"qid": "q0547ddc7af", "question_a": "Is the course limited to adults?", "question_b": "Is it incorrect that the course is limited to adults?"},
{"qid": "qa75d926794", "question_a": "Is the entrance located on the east side?", "question_b": "Would it be inaccurate that the entrance is located on the east side?"},
{"qid": "q561bda9924", "question_a": "Is the rule covered by the audit?", "question_b": "Is the rule uncovered by the audit?"},
{"qid": "q5b080dfd7d", "question_a": "Does the email announce a change of venue?", "question_b": "Does the record show something untrue that the email announces a change of venue?"},
{"qid": "qfc990054b1", "question_a": "Does the menu omit the spice level?", "question_b": "Does the menu say the spice level?"},
{"qid": "qc6935a8039", "question_a": "Does the notice provide a copy of the order?", "question_b": "Does the notice omit a copy of the order?"},
{"qid": "q7a65977001", "question_a": "Does the report include a summary table?", "question_b": "Does the report establish that the report includes a summary table?"},
{"qid": "q079498adf0", "question_a": "Does the jar contain any nuts?", "question_b": "Would a reviewer agree that the jar contains any nuts?"},
{"qid": "qd77f4cf3f9", "question_a": "Does the label contain a warning?", "question_b": "Is it true that the label does not lack a warning?"},
{"qid": "qd754b0351e", "question_a": "Does the notice omit an address for replies?", "question_b": "Does the notice provide an address for replies?"},
{"qid": "q0254439a0d", "question_a": "Does the plan have a backup route?", "question_b": "Would it be inaccurate that the plan has a backup route?"},
{"qid": "q72bf0e4caa", "question_a": "Does the menu show the price?", "question_b": "Does the menu omit the price?"},
{"qid": "q0dac2dbc4e", "question_a": "Is the late checkout allowed for guests?", "question_b": "Is it true that the late checkout is not forbidden for guests?"},
{"qid": "q59143e2ade", "question_a": "Does the record omit the clerk?", "question_b": "Does the record name the clerk?"},
{"qid": "qb067ecabf6", "question_a": "Is the room planned for a larger group?", "question_b": "Does this claim hold that the room is planned for a larger group?"},
{"qid": "qd1bba393a9", "question_a": "Is the entry unrestricted for adults?", "question_b": "Is the entry restricted for adults?"},
{"qid": "q13f6042c8a", "question_a": "Is the record unlisted in the ledger?", "question_b": "Is the record listed in the ledger?"},
{"qid": "q896e70ff99", "question_a": "Is the form unsigned by the parent?", "question_b": "Is the form signed by the parent?"},
{"qid": "q45c64b795c", "question_a": "Is the check signed by the payee?", "question_b": "Is it true that the check is not unsigned by the payee?"},
{"qid": "qcaecd23828", "question_a": "Does the guide explain how to reset the device?", "question_b": "Would the record confirm that the guide explains how to reset the device?"},
{"qid": "q312bd459f6", "question_a": "Is the quote unconfirmed by the transcript?", "question_b": "Is the quote confirmed by the transcript?"},
{"qid": "q8eeb89da93", "question_a": "Does the memo contain a budget?", "question_b": "Does the memo lack a budget?"}
]
```
