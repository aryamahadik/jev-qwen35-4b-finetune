# T06 extraction task T06-extract_lex-e6c2fa0c-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/extract/answers/T06-extract_lex-e6c2fa0c-000.json

Task: extract_lex; glex-r2; items: 50; outputs expected: 50.

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
- asks whether the customer gets any money back, store credit or an exchange
- asks, with the store as the subject and no negation, whether the store has to give the customer a full refund (yes = a full refund is due)
- asks, with 'no' in front of a noun, whether the customer has no right to a full refund or no full refund is due (yes = no full refund is due)
- asks, with 'not' or n't on the verb, whether the customer is not entitled to a full refund (yes = no full refund is due)
- asks on which date the period of the customer's legal right to withdraw from or cancel the purchase ends
- asks on which date the period of the customer's legal right to reject faulty goods ends
- asks, using two negations, whether it is false that the customer has no right to a full refund (yes = a full refund is due)
- asks on which date the period of the store's own notice or promise ends
- asks, with the customer as the subject and no negation, whether the customer has a right to a full refund (yes = a full refund is due)
- asks which listed rule, if any, gives the customer a full refund
- asks, with no negation word, whether the store may refuse or turn down a full refund (yes = no full refund is due)

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "qe2ddb94ae3",
  "text": "Is it not the case that the customer, for this order, has no right to a full refund?"
 },
 {
  "qid": "qaf60a37143",
  "text": "Looking at this order, which date is the final day of the period of the customer's legal right to reject faulty goods?"
 },
 {
  "qid": "qa5d91da417",
  "text": "Which date, for this order, marks the end of the period of the customer's legal right to reject faulty goods?"
 },
 {
  "qid": "q7710618ee6",
  "text": "For this return, which listed rule, if any, gives the customer a full refund?"
 },
 {
  "qid": "q7743047682",
  "text": "Which of the listed rules, if any, secures a full refund for the customer?"
 },
 {
  "qid": "q915921760c",
  "text": "Which of the listed rules, if any, applied to this order gives the customer a full refund?"
 },
 {
  "qid": "qb04a0b28ce",
  "text": "On these facts, which listed rule, if any, entitles the customer to a full refund?"
 },
 {
  "qid": "q28f9c57797",
  "text": "Which of the listed rules, if any, gives the customer for this order a full refund?"
 },
 {
  "qid": "qbdd567e0d4",
  "text": "For this return, on what final day does the period of the customer's legal right to cancel for any reason end?"
 },
 {
  "qid": "q09f5b11002",
  "text": "Taking the facts as given, on which date does the period of the customer's legal right to reject faulty goods end?"
 },
 {
  "qid": "qddd1985fc6",
  "text": "Which rule from the list, if any, gives the customer a full refund for this order?"
 },
 {
  "qid": "qdc793159a1",
  "text": "Which date is the final day of the period of the customer's legal right to reject faulty goods?"
 },
 {
  "qid": "qe5e5649d61",
  "text": "On these facts, which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "qa6dafa362d",
  "text": "Looking at this order, is it not the case that the customer has no right to any full refund?"
 },
 {
  "qid": "q5666fc6fd9",
  "text": "Is it not the case that the customer has no right to a full refund here?"
 },
 {
  "qid": "qd2c6250926",
  "text": "Which listed rule, if any, gives the customer on this order a full refund?"
 },
 {
  "qid": "q72c077ca63",
  "text": "On these facts, is it not the case that the customer has no right to a full refund?"
 },
 {
  "qid": "qfcf691625d",
  "text": "What is the final day of the customer's legal right to reject faulty goods here?"
 },
 {
  "qid": "qf1e3b735c6",
  "text": "Which of the listed rules, if any, gives the customer a full refund here?"
 },
 {
  "qid": "q6da40222f9",
  "text": "On which date does the period of the customer's legal right to reject faulty goods end for this order?"
 },
 {
  "qid": "qa3aaf9a828",
  "text": "Among the listed rules, which, if any, gives the customer a full refund?"
 },
 {
  "qid": "q2d784b8797",
  "text": "On which date does the period of the customer's legal right to reject faulty goods end?"
 },
 {
  "qid": "q5e7dda7c5b",
  "text": "On the case as written, which of the listed rules gives the customer a full refund, if any?"
 },
 {
  "qid": "q89458f93b9",
  "text": "For this return, which of the listed rules gives the customer a full refund, if any?"
 },
 {
  "qid": "q805a16e19e",
  "text": "Taking the facts as given, which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "q382e7a9459",
  "text": "Which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "qb0b0014b3a",
  "text": "Looking at this order, which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "q6294fb3402",
  "text": "Which of the listed rules, if any, gives the customer a full refund in this case?"
 },
 {
  "qid": "qcf79809568",
  "text": "Which of the listed rules, if any, gives the customer a full refund for this order?"
 },
 {
  "qid": "qace8b8472b",
  "text": "In this case, which listed rule, if any, gives the customer a full refund?"
 },
 {
  "qid": "q8ef50db4df",
  "text": "Is it not the case that the customer has no right to receive a full refund in this case?"
 },
 {
  "qid": "q0104d13c08",
  "text": "Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason?"
 },
 {
  "qid": "qca77cc8454",
  "text": "On these facts, on which date does the period of the customer's legal right to reject faulty goods run out?"
 },
 {
  "qid": "qf0d4647d8d",
  "text": "Taking the facts as given, is it not the case that the customer has no right to a full refund?"
 },
 {
  "qid": "q630b06d73b",
  "text": "On which date does the period of the customer's legal right to reject faulty goods end in this case?"
 },
 {
  "qid": "qbbb5da08cb",
  "text": "In this case, which of the listed rules, if any, gives the customer a full refund?"
 },
 {
  "qid": "qfa57a29f05",
  "text": "Which of the listed rules, if any, entitles the customer to a full refund in this case?"
 },
 {
  "qid": "qeddd1eb97b",
  "text": "For this return, on which date does the period of the customer's legal right to reject faulty goods end?"
 },
 {
  "qid": "qd42619cf8d",
  "text": "Which listed rule, if any, gives the customer a full refund?"
 },
 {
  "qid": "q46b8851a69",
  "text": "In this case, which of the listed rules gives the customer a full refund, if any?"
 },
 {
  "qid": "qb3f04dca37",
  "text": "In this case, by which date does the period of the customer's legal right to reject faulty goods end?"
 },
 {
  "qid": "q79e9df31b6",
  "text": "In this case, from the listed rules, which, if any, gives the customer a full refund?"
 },
 {
  "qid": "q06df360655",
  "text": "In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end?"
 },
 {
  "qid": "qbacddf2081",
  "text": "For this return, which of the listed rules, if any, grants the customer a full refund?"
 },
 {
  "qid": "q333c70492c",
  "text": "Which of the listed rules, if any, grants a full refund to the customer here?"
 },
 {
  "qid": "qb7f0838a5c",
  "text": "Among the listed rules, which, if any, gives the customer a full refund here?"
 },
 {
  "qid": "qe511c14457",
  "text": "Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
 },
 {
  "qid": "q19379aa314",
  "text": "Among the listed rules, which, if any, gives the customer a full refund in this case?"
 },
 {
  "qid": "q5461ccfc5b",
  "text": "Which of the listed rules gives the customer a full refund on this order, if any?"
 },
 {
  "qid": "q7e4eb59479",
  "text": "For this return, which of the listed rules, if any, gives the customer a full refund?"
 }
]
```
