# T06 extraction task T06-extract_lex-170ed4db-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/extract/answers/T06-extract_lex-170ed4db-000.json

Task: extract_lex; glex-r3; items: 6; outputs expected: 6.

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
- the store promises a full refund within the stated days of the day the customer received or collected the goods
- the store promises a full refund for faulty items asked for within the stated days of the purchase (order) date
- the store promises a full refund to a customer who changed their mind, within the stated days of the purchase (order) date
- the store promises a full refund for any reason within the stated days of the purchase (order) date
- the store gives store credit or an exchange, not money back, for returns within the stated days
- the store promises a full refund for any reason within the stated days of the delivery date
- the store accepts returns within the stated days but does not say what the customer gets back

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "q02ece9f627",
  "text": "Within 30 days of purchase, changing your mind earns you a full refund."
 },
 {
  "qid": "q27538a82a2",
  "text": "Full refund for a change of mind, within 30 days of the purchase date."
 },
 {
  "qid": "q946042dcb6",
  "text": "Change of mind: full refund within 30 days of purchase."
 },
 {
  "qid": "q7a5f79f529",
  "text": "Within 30 days of the order date, a change of mind earns a full refund."
 },
 {
  "qid": "q864b0d195a",
  "text": "Changed your mind on an order? A full refund is paid within 30 days of order."
 },
 {
  "qid": "qcf6aac3236",
  "text": "If you have changed your mind, you can have a full refund within 30 days from the day you bought it."
 }
]
```
