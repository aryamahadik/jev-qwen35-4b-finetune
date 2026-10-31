# T06 extraction task T06-extract_lex-9a5c657f-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/extract/answers/T06-extract_lex-9a5c657f-000.json

Task: extract_lex; glex-r1; items: 50; outputs expected: 50.

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
- asks on which date the period of the store's own notice or promise ends
- asks, with the store as the subject and no negation, whether the store has to give the customer a full refund (yes = a full refund is due)
- asks, with no negation word, whether the store may refuse or turn down a full refund (yes = no full refund is due)
- asks, with 'no' in front of a noun, whether the customer has no right to a full refund or no full refund is due (yes = no full refund is due)
- asks, with the customer as the subject and no negation, whether the customer has a right to a full refund (yes = a full refund is due)
- asks which listed rule, if any, gives the customer a full refund
- asks, using two negations, whether it is false that the customer has no right to a full refund (yes = a full refund is due)
- asks on which date the period of the customer's legal right to reject faulty goods ends
- asks whether the customer gets any money back, store credit or an exchange
- asks, with 'not' or n't on the verb, whether the customer is not entitled to a full refund (yes = no full refund is due)
- asks on which date the period of the customer's legal right to withdraw from or cancel the purchase ends

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "q1272df5bc7",
  "text": "Is it not the case that the customer has no right to receive a full refund in this case?"
 },
 {
  "qid": "q34e2c37420",
  "text": "On the case as written, which of the listed rules gives the customer a full refund, if any?"
 },
 {
  "qid": "qb8f7d0651d",
  "text": "Which of the listed rules, if any, gives the customer for this order a full refund?"
 },
 {
  "qid": "q2ca016caa6",
  "text": "Which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "q0471cf2914",
  "text": "For this return, which of the listed rules gives the customer a full refund, if any?"
 },
 {
  "qid": "q4e44b78449",
  "text": "On these facts, which listed rule, if any, entitles the customer to a full refund?"
 },
 {
  "qid": "q3ebb1ad79c",
  "text": "In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end?"
 },
 {
  "qid": "qb95c2f0727",
  "text": "Which of the listed rules, if any, gives the customer a full refund in this case?"
 },
 {
  "qid": "q3d8efb9703",
  "text": "Looking at this order, which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "qaf4707588f",
  "text": "Which of the listed rules, if any, secures a full refund for the customer?"
 },
 {
  "qid": "q4d83a5e870",
  "text": "Which of the listed rules, if any, grants a full refund to the customer here?"
 },
 {
  "qid": "qb3ef5aa7bb",
  "text": "Among the listed rules, which, if any, gives the customer a full refund?"
 },
 {
  "qid": "qef73945af3",
  "text": "On which date does the period of the customer's legal right to reject faulty goods end for this order?"
 },
 {
  "qid": "q1df17006d0",
  "text": "Among the listed rules, which, if any, gives the customer a full refund here?"
 },
 {
  "qid": "q02a881ed79",
  "text": "For this return, on what final day does the period of the customer's legal right to cancel for any reason end?"
 },
 {
  "qid": "qc76436ee67",
  "text": "On which date does the period of the customer's legal right to reject faulty goods end in this case?"
 },
 {
  "qid": "q5c58958be7",
  "text": "For this return, which of the listed rules, if any, grants the customer a full refund?"
 },
 {
  "qid": "qafa272170f",
  "text": "In this case, from the listed rules, which, if any, gives the customer a full refund?"
 },
 {
  "qid": "qd200cb7360",
  "text": "Which date, for this order, marks the end of the period of the customer's legal right to reject faulty goods?"
 },
 {
  "qid": "qfa4c8217da",
  "text": "Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason?"
 },
 {
  "qid": "q56251d4247",
  "text": "Taking the facts as given, is it not the case that the customer has no right to a full refund?"
 },
 {
  "qid": "q6b43bb1c7b",
  "text": "Which listed rule, if any, gives the customer on this order a full refund?"
 },
 {
  "qid": "q4ec531f4bf",
  "text": "What is the final day of the customer's legal right to reject faulty goods here?"
 },
 {
  "qid": "q7280de48b8",
  "text": "In this case, which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "q61e64ba746",
  "text": "Looking at this order, is it not the case that the customer has no right to any full refund?"
 },
 {
  "qid": "q93ba259bf1",
  "text": "In this case, by which date does the period of the customer's legal right to reject faulty goods end?"
 },
 {
  "qid": "q02b38b485b",
  "text": "In this case, which of the listed rules gives the customer a full refund, if any?"
 },
 {
  "qid": "qa94463b93f",
  "text": "In this case, which listed rule, if any, gives the customer a full refund?"
 },
 {
  "qid": "qb5d710d9eb",
  "text": "Which of the listed rules, if any, applied to this order gives the customer a full refund?"
 },
 {
  "qid": "q42bb7f8dd0",
  "text": "Looking at this order, which date is the final day of the period of the customer's legal right to reject faulty goods?"
 },
 {
  "qid": "q537b3ec3d2",
  "text": "Taking the facts as given, which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "qef46f60405",
  "text": "Which of the listed rules, if any, gives the customer a full refund here?"
 },
 {
  "qid": "q5c752417e6",
  "text": "Which of the listed rules, if any, gives the customer a full refund for this order?"
 },
 {
  "qid": "qdbf89d67f9",
  "text": "Is it not the case that the customer has no right to a full refund here?"
 },
 {
  "qid": "q565e9d15ab",
  "text": "Is it not the case that the customer, for this order, has no right to a full refund?"
 },
 {
  "qid": "q2876f36487",
  "text": "Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
 },
 {
  "qid": "q6cba600795",
  "text": "Among the listed rules, which, if any, gives the customer a full refund in this case?"
 },
 {
  "qid": "qdde5e79c42",
  "text": "On these facts, which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "qb9ef4cf63a",
  "text": "On which date does the period of the customer's legal right to reject faulty goods end?"
 },
 {
  "qid": "qb506b7ecd0",
  "text": "On these facts, is it not the case that the customer has no right to a full refund?"
 },
 {
  "qid": "q05636bd510",
  "text": "Which listed rule, if any, gives the customer a full refund?"
 },
 {
  "qid": "qd1878746d8",
  "text": "For this return, which listed rule, if any, gives the customer a full refund?"
 },
 {
  "qid": "qfc7ad20e98",
  "text": "Which of the listed rules, if any, entitles the customer to a full refund in this case?"
 },
 {
  "qid": "qe8e32bdce5",
  "text": "On these facts, on which date does the period of the customer's legal right to reject faulty goods run out?"
 },
 {
  "qid": "qf5db0080cf",
  "text": "Which of the listed rules gives the customer a full refund on this order, if any?"
 },
 {
  "qid": "q835d5f9b6a",
  "text": "Which date is the final day of the period of the customer's legal right to reject faulty goods?"
 },
 {
  "qid": "q087d31668b",
  "text": "Taking the facts as given, on which date does the period of the customer's legal right to reject faulty goods end?"
 },
 {
  "qid": "q5f1bd05b06",
  "text": "Which rule from the list, if any, gives the customer a full refund for this order?"
 },
 {
  "qid": "qb57b1a80b0",
  "text": "For this return, on which date does the period of the customer's legal right to reject faulty goods end?"
 },
 {
  "qid": "q9406a519b4",
  "text": "For this return, which of the listed rules, if any, gives the customer a full refund?"
 }
]
```
