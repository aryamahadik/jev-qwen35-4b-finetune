# T06 extraction task T06-extract_lex-edbc2f7c-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/extract/answers/T06-extract_lex-edbc2f7c-000.json

Task: extract_lex; glex-r2; items: 18; outputs expected: 18.

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
- asks which listed rule, if any, gives the customer a full refund
- asks, with the customer as the subject and no negation, whether the customer has a right to a full refund (yes = a full refund is due)
- asks on which date the period of the customer's legal right to withdraw from or cancel the purchase ends
- asks on which date the period of the store's own notice or promise ends
- asks, with 'not' or n't on the verb, whether the customer is not entitled to a full refund (yes = no full refund is due)
- asks on which date the period of the customer's legal right to reject faulty goods ends
- asks, with 'no' in front of a noun, whether the customer has no right to a full refund or no full refund is due (yes = no full refund is due)
- asks, using two negations, whether it is false that the customer has no right to a full refund (yes = a full refund is due)
- asks, with no negation word, whether the store may refuse or turn down a full refund (yes = no full refund is due)
- asks, with the store as the subject and no negation, whether the store has to give the customer a full refund (yes = a full refund is due)

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "q12927dd8b7",
  "text": "Does the store owe the customer a full refund here?"
 },
 {
  "qid": "q172ad5d4e9",
  "text": "Looking at this order, can the customer get a full refund?"
 },
 {
  "qid": "q194903a84b",
  "text": "On the case as written, does the store owe the customer a full refund?"
 },
 {
  "qid": "qdf915ca443",
  "text": "Does the customer qualify for a full refund on these facts?"
 },
 {
  "qid": "qaa4bb4e218",
  "text": "In this case, does the customer qualify for a full refund?"
 },
 {
  "qid": "qfe56087c97",
  "text": "Does the store owe the customer a full refund in this case?"
 },
 {
  "qid": "q31611a860d",
  "text": "On these facts, does the store owe the customer a full refund?"
 },
 {
  "qid": "q2798b6697e",
  "text": "Is the customer entitled to a full refund for this order?"
 },
 {
  "qid": "qa883efe5a0",
  "text": "On these facts, is the customer entitled to a full refund?"
 },
 {
  "qid": "q52e9361574",
  "text": "Does the customer qualify for a full refund in this case?"
 },
 {
  "qid": "q6d80719448",
  "text": "Is the customer entitled to a full refund in this case?"
 },
 {
  "qid": "qa685253b71",
  "text": "Taking the facts as given, is the customer entitled to a full refund?"
 },
 {
  "qid": "qfc4f3dcc1a",
  "text": "In this case, is the customer entitled to a full refund?"
 },
 {
  "qid": "qf6adf6b230",
  "text": "For this return, does the customer have a right to a full refund?"
 },
 {
  "qid": "qf12d40423f",
  "text": "Does the customer, on this order, have a right to a full refund?"
 },
 {
  "qid": "q216efeed9d",
  "text": "On these facts, can the customer get a full refund?"
 },
 {
  "qid": "q123367cdd2",
  "text": "Is the store obliged to give the customer a full refund in this case?"
 },
 {
  "qid": "q49a19483ed",
  "text": "Can the customer get a full refund for this return here?"
 }
]
```
