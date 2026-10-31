# Haiku G-LEX read NEGTW-polarity-5f788008-002 (family NEGTW, kind polarity)

Read this whole file. Do not open any other file. When you are done, write your answer with the Write tool to exactly this path (nothing else, no other file):

    /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/negtwins/haiku/glex_train_r2/answers/NEGTW-polarity-5f788008-002.json

The answer is one JSON list with exactly 50 objects, one per item below, each carrying that item's qid.

## Instructions

Each item holds two yes/no questions, question_a and question_b, that will be asked about the same text with the same definitions. Reply 'same' if a correct yes to question_a always goes with a correct yes to question_b and a correct no with a correct no; 'opposite' if a correct yes to one always goes with a correct no to the other; 'unclear' if neither holds for certain or a question is ungrammatical. Reply with JSON: a list of objects {"qid": <qid>, "relation": "same" | "opposite" | "unclear"}.

## Answer format

[{"qid": "q...", "relation": "same" | "opposite" | "unclear"}, ...]

## Items (50; one JSON object per line)

```json
[
{"qid": "q19b6ac3e70", "question_a": "Does the poster invite visitors to the open day?", "question_b": "Is the reading accurate that the poster invites visitors to the open day?"},
{"qid": "q419994d253", "question_a": "Is the letter unsigned by the chief?", "question_b": "Is the letter signed by the chief?"},
{"qid": "qe27d1ef565", "question_a": "Does the bag contain a receipt?", "question_b": "Does the report establish that the bag contains a receipt?"},
{"qid": "qe6294b8353", "question_a": "Is the sample provided at no cost?", "question_b": "Would the record confirm that the sample is provided at no cost?"},
{"qid": "q15d576132e", "question_a": "Is the pool available after six?", "question_b": "Is it mistaken that the pool is available after six?"},
{"qid": "q2c505e1f7a", "question_a": "Is the waiver signed before the trip?", "question_b": "Is the waiver unsigned before the trip?"},
{"qid": "q8a22c2ef82", "question_a": "Is the rule supported by the study?", "question_b": "Is the rule unsupported by the study?"},
{"qid": "q972783ae74", "question_a": "Does the shop have a returns desk?", "question_b": "Is it untrue that the shop has a returns desk?"},
{"qid": "qff0218fd8b", "question_a": "Is the photo ID optional at check-in?", "question_b": "Is the photo ID required at check-in?"},
{"qid": "q3229761b69", "question_a": "Does the rule permit pets in the building?", "question_b": "Would the facts show that the rule permits pets in the building?"},
{"qid": "q45042c14ce", "question_a": "Is the entry prohibited for minors?", "question_b": "Is the entry permitted for minors?"},
{"qid": "q5deb26986a", "question_a": "Does the label contain a warning?", "question_b": "Is it true that the label does not lack a warning?"},
{"qid": "qb074dc7346", "question_a": "Does the menu contain a vegetarian dish?", "question_b": "Would the record show that the menu contains a vegetarian dish?"},
{"qid": "q5a0e7e3b5c", "question_a": "Does the folder contain the signed forms?", "question_b": "Would it be mistaken that the folder contains the signed forms?"},
{"qid": "q530bc11dcb", "question_a": "Does the form request a phone number?", "question_b": "Would the record show that the form requests a phone number?"},
{"qid": "q6e3444734b", "question_a": "Does the email announce a change of venue?", "question_b": "Does the record show something untrue that the email announces a change of venue?"},
{"qid": "q33b10a6b41", "question_a": "Is the breakfast excluded from the stay?", "question_b": "Is the breakfast included from the stay?"},
{"qid": "q1250b1b926", "question_a": "Does the letter contain an offer?", "question_b": "Would it be false that the letter contains an offer?"},
{"qid": "q4c2515ed45", "question_a": "Is the rule covered by the audit?", "question_b": "Is the rule uncovered by the audit?"},
{"qid": "q0d6aa19a5f", "question_a": "Does the badge prohibit entry after six pm?", "question_b": "Does the badge permit entry after six pm?"},
{"qid": "qdc4b9079d1", "question_a": "Is the parking permit forbidden on this street?", "question_b": "Is the parking permit allowed on this street?"},
{"qid": "q9a9fd48fac", "question_a": "Is the class eligible for the discount?", "question_b": "Does the notice confirm that the class is eligible for the discount?"},
{"qid": "q03a7452ff5", "question_a": "Is the budget unlimited in amount?", "question_b": "Is the budget limited in amount?"},
{"qid": "q486682d5d2", "question_a": "Does the directory omit the new clinic?", "question_b": "Does the directory list the new clinic?"},
{"qid": "q6ffa0fb913", "question_a": "Is the picnic permitted in the park?", "question_b": "Is it true that the picnic is not prohibited in the park?"},
{"qid": "q18281409c2", "question_a": "Is the form unsigned by the parent?", "question_b": "Is the form signed by the parent?"},
{"qid": "q883b7d1768", "question_a": "Is the locker unlocked for staff?", "question_b": "Is it true that the locker is not locked for staff?"},
{"qid": "q0d1c1fe0fe", "question_a": "Is the sale permitted in this zone?", "question_b": "Is the sale prohibited in this zone?"},
{"qid": "q4dccb1826d", "question_a": "Is the entrance located on the east side?", "question_b": "Would you call it untrue that the entrance is located on the east side?"},
{"qid": "q10bf889852", "question_a": "Is the library restricted to members?", "question_b": "Is the library unrestricted to members?"},
{"qid": "q9abe8a7ebc", "question_a": "Does the regulation forbid the export?", "question_b": "Does the regulation allow the export?"},
{"qid": "q3d6ba0917e", "question_a": "Is the camping spot allowed near the river?", "question_b": "Is the camping spot forbidden near the river?"},
{"qid": "q194e169ba4", "question_a": "Does the course include an exam?", "question_b": "Would it be false that the course includes an exam?"},
{"qid": "q356646fd88", "question_a": "Does the ticket mention a refund?", "question_b": "Is it true that the ticket does not omit a refund?"},
{"qid": "qcb3a48d048", "question_a": "Does the license prohibit resale of the software?", "question_b": "Does the license permit resale of the software?"},
{"qid": "q95518c0864", "question_a": "Is the clause uncovered by the warranty?", "question_b": "Is the clause covered by the warranty?"},
{"qid": "qf0c0deed9e", "question_a": "Is the backup file forbidden on the shared drive?", "question_b": "Is the backup file allowed on the shared drive?"},
{"qid": "q362058fa91", "question_a": "Is the claim confirmed by the source?", "question_b": "Is the claim unconfirmed by the source?"},
{"qid": "q01756358db", "question_a": "Does the badge permit entry after six pm?", "question_b": "Does the badge prohibit entry after six pm?"},
{"qid": "qe32b71d4fe", "question_a": "Does the report say the test result?", "question_b": "Does the report omit the test result?"},
{"qid": "q98d0504d24", "question_a": "Does the form omit a date?", "question_b": "Does the form mention a date?"},
{"qid": "q0f1db0ba97", "question_a": "Is the entry unrestricted for adults?", "question_b": "Is the entry restricted for adults?"},
{"qid": "q11f3355ed1", "question_a": "Is the quota limited in scope?", "question_b": "Is the quota unlimited in scope?"},
{"qid": "q5f6231b491", "question_a": "Does the menu contain a vegetarian dish?", "question_b": "Does the record show something untrue that the menu contains a vegetarian dish?"},
{"qid": "q5947e244e5", "question_a": "Is the clause listed in the appendix?", "question_b": "Is the clause unlisted in the appendix?"},
{"qid": "q80d9db96a7", "question_a": "Does the notice provide a date of issue?", "question_b": "Does the notice omit a date of issue?"},
{"qid": "q72a47d6721", "question_a": "Does the review recommend the product to families?", "question_b": "Is it untrue that the review recommends the product to families?"},
{"qid": "qbddb7795c9", "question_a": "Does the lesson plan involve group work?", "question_b": "Does the record show something untrue that the lesson plan involves group work?"},
{"qid": "q4942bf5d3a", "question_a": "Does the code allow the extension?", "question_b": "Is it true that the code does not forbid the extension?"},
{"qid": "q5726f99055", "question_a": "Is the number unconfirmed by the ledger?", "question_b": "Is the number confirmed by the ledger?"}
]
```
