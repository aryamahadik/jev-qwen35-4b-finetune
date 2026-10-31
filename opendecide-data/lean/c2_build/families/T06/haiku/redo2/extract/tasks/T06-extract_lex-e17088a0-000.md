# T06 extraction task T06-extract_lex-e17088a0-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/redo2/extract/answers/T06-extract_lex-e17088a0-000.json

Task: extract_lex; glex-r1; items: 16; outputs expected: 16.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a double quote as \" and a line break as \n.

TASK: READ EACH TEXT ALONE and pick the ONE MEANING from the CLOSED LIST that the text expresses. Each item gives a TEXT:
one short store notice or one question about a returns case, with its values already filled in.

Rules:
1. Use only the TEXT and the CLOSED LIST. Do not guess beyond the words, and do not add a condition, a default or any
   fact from outside the text.
2. Copy the chosen meaning exactly, character for character, from the CLOSED LIST. Never write a new meaning.
3. Judge each text on its own words, not on the other items or on the order of the list.
4. Answer every item exactly once.

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen meaning, copied exactly>"}, ...]
Copy each qid exactly.

CLOSED LIST (one meaning per line; copy one of these exactly):
- asks, with 'no' in front of a noun, whether the customer has no right to a full refund or no full refund is due (yes = no full refund is due)
- asks, with the customer as the subject and no negation, whether the customer has a right to a full refund (yes = a full refund is due)
- asks on which date the period of the customer's legal right to reject faulty goods ends
- asks, with 'not' or n't on the verb, whether the customer is not entitled to a full refund (yes = no full refund is due)
- asks whether the customer gets any money back, store credit or an exchange
- asks, with no negation word, whether the store may refuse or turn down a full refund (yes = no full refund is due)
- asks on which date the period of the customer's legal right to withdraw from or cancel the purchase ends
- asks, using two negations, whether it is false that the customer has no right to a full refund (yes = a full refund is due)
- asks on which date the period of the store's own notice or promise ends
- asks which listed rule, if any, gives the customer a full refund
- asks, with the store as the subject and no negation, whether the store has to give the customer a full refund (yes = a full refund is due)

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "q91e99390c2",
  "text": "Which date does the customer's statutory period to cancel for any reason run out?"
 },
 {
  "qid": "qa121edc840",
  "text": "On these facts, by what final day does the statutory time limit to withdraw for any reason run out?"
 },
 {
  "qid": "q6b059927c5",
  "text": "For this return, by which day will the legal window to cancel the purchase for any reason come to an end?"
 },
 {
  "qid": "q3c0bf66bc5",
  "text": "Which date does the period of the statutory right to cancel for any reason end in this case?"
 },
 {
  "qid": "q5f7a9e77cc",
  "text": "Which final day ends the period of the customer's statutory right to withdraw for any reason in this case?"
 },
 {
  "qid": "q37f116389f",
  "text": "Which date marks the end of the legal period for the customer's right to cancel for any reason here?"
 },
 {
  "qid": "q93271610d1",
  "text": "On these facts, on which date does the customer's statutory period to withdraw for any reason end?"
 },
 {
  "qid": "qaa4ef44152",
  "text": "Taking the facts as given, on which final day will the customer's statutory window to withdraw for any reason end?"
 },
 {
  "qid": "q8798043d2a",
  "text": "In this case, what is the final day of the legal window to cancel for any reason?"
 },
 {
  "qid": "qfc90a7253d",
  "text": "On the case as written, by which date does the statutory period for the customer to cancel for any reason end?"
 },
 {
  "qid": "q1c4dc8f03e",
  "text": "In this case, on which day does the period of the right the law gives the customer to withdraw for any reason end?"
 },
 {
  "qid": "q1a8d3186e6",
  "text": "Looking at this order, on which day does the statutory time limit to cancel the purchase for any reason end?"
 },
 {
  "qid": "qdcbc3cdfd7",
  "text": "Which date is the final day of the period of the statutory right to withdraw for any reason here?"
 },
 {
  "qid": "qc83c6398b1",
  "text": "On which date does the customer's legal right to withdraw for any reason end for this order?"
 },
 {
  "qid": "qba0b147967",
  "text": "Which day will bring the statutory period for the customer to cancel the purchase for any reason to an end?"
 },
 {
  "qid": "q449b7df11e",
  "text": "Which date, for this order, will the legal window to withdraw for any reason run out?"
 }
]
```
