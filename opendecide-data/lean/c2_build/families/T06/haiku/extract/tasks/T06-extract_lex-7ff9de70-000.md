# T06 extraction task T06-extract_lex-7ff9de70-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/extract/answers/T06-extract_lex-7ff9de70-000.json

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
- the store promises a full refund for faulty items asked for within the stated days of the purchase (order) date
- the store accepts returns within the stated days but does not say what the customer gets back
- the store promises a full refund to a customer who changed their mind, within the stated days of the purchase (order) date
- the store gives store credit or an exchange, not money back, for returns within the stated days
- the store promises a full refund for any reason within the stated days of the delivery date
- the store promises a full refund for any reason within the stated days of the purchase (order) date
- the store promises a full refund within the stated days of the day the customer received or collected the goods

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "q4e2292253e",
  "text": "Should you change your mind, you are owed a full refund within 1 day of the order date."
 },
 {
  "qid": "q7f3f1122fd",
  "text": "A faulty item is refunded in full. The return must be asked for within 1 day of the order date."
 },
 {
  "qid": "qd7d80e3444",
  "text": "If an item is faulty, you are refunded in full when you ask for a return within 1 day of the purchase date."
 },
 {
  "qid": "q124247b12a",
  "text": "Full refund for any item sent back, whatever the reason, within 1 day of delivery."
 },
 {
  "qid": "q122b9e7fd0",
  "text": "Within 1 day from delivery, send back any item for any reason and earn a full refund."
 },
 {
  "qid": "q690684d9d5",
  "text": "Within 1 day of the purchase date, you are refunded in full for changing your mind."
 },
 {
  "qid": "q9a92c4c3b1",
  "text": "Within 1 day of the order date, a faulty item qualifies for a full refund on request."
 },
 {
  "qid": "q6616f15218",
  "text": "Any item may be sent back for any reason. Such returns are refunded in full within 1 day of delivery."
 },
 {
  "qid": "q8ffcbdad8e",
  "text": "Returns for any reason are accepted on any item. A full refund is given within 1 day of delivery."
 },
 {
  "qid": "q75707e38a5",
  "text": "Any item you return for any reason, within 1 day of delivery, earns you a full refund."
 },
 {
  "qid": "q6f6832f978",
  "text": "Expect a full refund on any item, whatever the reason, within 1 day from the day you ordered."
 },
 {
  "qid": "qe82a4bffbe",
  "text": "Within 1 day of purchase, any returned item is refunded in full, whatever the reason."
 },
 {
  "qid": "q58950c17c4",
  "text": "Within 1 day of the order date, a faulty item gets a full refund."
 },
 {
  "qid": "q3a3536c14c",
  "text": "Refunded in full within 1 day of delivery, on any item returned for any reason."
 },
 {
  "qid": "q6312c10f55",
  "text": "We issue a refund in full for any item returned for any reason, within 1 day of delivery."
 },
 {
  "qid": "q3bf6a5d6b3",
  "text": "A full refund applies to every item, whichever the reason it is returned, within 1 day of delivery."
 },
 {
  "qid": "qbe18a253f9",
  "text": "A full refund within 1 day of the purchase date is given for a change of mind."
 },
 {
  "qid": "qe7c8a22ab5",
  "text": "Return any item, for any reason. You will be refunded in full within 1 day of delivery."
 },
 {
  "qid": "qe3fb2cbdd6",
  "text": "Within 1 day of the purchase date, any faulty item is refunded in full."
 },
 {
  "qid": "qca8a2a8039",
  "text": "Faulty item: refund in full within 1 day of purchase."
 },
 {
  "qid": "qc5598c0a42",
  "text": "We refund in full any item, for any reason, when returned within 1 day of purchase."
 },
 {
  "qid": "qe406f0af3f",
  "text": "We give a full refund for faulty items when you ask for a return within 1 day of the purchase date."
 },
 {
  "qid": "q905ff1aab6",
  "text": "A faulty item is covered. A full refund applies when the return is requested within 1 day of your order."
 },
 {
  "qid": "q7878582ab4",
  "text": "We give a full refund on any item returned for any reason, within 1 day of the delivery date."
 },
 {
  "qid": "q3d95a1395f",
  "text": "Faulty items only. A full refund is given when a return is asked for within 1 day of the order date."
 },
 {
  "qid": "q9474c06f5d",
  "text": "Any item returned, whatever the reason, gets a refund in full within 1 day of delivery."
 },
 {
  "qid": "q33f7652873",
  "text": "We give a full refund for faulty items if you ask for a return within 1 day of purchase."
 },
 {
  "qid": "q537c99e9e2",
  "text": "Any item returned for any reason: refunded in full within 1 day of the order date."
 },
 {
  "qid": "q9aa36a99a4",
  "text": "Any item returned for any reason: full refund within 1 day of the purchase date."
 },
 {
  "qid": "qdf5db55ab3",
  "text": "You can ask for a full refund on a faulty item within 1 day of the day you bought it."
 },
 {
  "qid": "q224b516a9f",
  "text": "Any item you return, for any reason, is refunded in full within 1 day of the delivery date."
 },
 {
  "qid": "q75ab2906bd",
  "text": "Within 1 day of delivery, any item sent back for any reason is refunded in full."
 },
 {
  "qid": "qc230b11765",
  "text": "Any item returned for any reason earns you a full refund within 1 day of purchase."
 },
 {
  "qid": "q0a887a17d6",
  "text": "Have you changed your mind? You are refunded in full within 1 day of purchase."
 },
 {
  "qid": "q82ce4983e3",
  "text": "Any item can be returned for any reason. A full refund is yours if you return it within 1 day of the order date."
 },
 {
  "qid": "q257585cc6e",
  "text": "Within 1 day of your purchase, you can return any item for any reason and be refunded in full."
 },
 {
  "qid": "q2e31f557c6",
  "text": "Full refund for any faulty item, if the return is asked for within 1 day of purchase."
 },
 {
  "qid": "qdfd52dd848",
  "text": "Refunded in full: any item returned for any reason, within 1 day of delivery."
 },
 {
  "qid": "qd0a9a65cdc",
  "text": "You can return any item for any reason. It is refunded in full within 1 day of the purchase date."
 },
 {
  "qid": "q18cb7a9eb0",
  "text": "Changing your mind is covered. A full refund is due within 1 day of the day you ordered."
 },
 {
  "qid": "q6a55988f47",
  "text": "Within 1 day of the delivery date, any returned item is refunded in full, whatever the reason."
 },
 {
  "qid": "qb0c28d6727",
  "text": "Refund in full on any returned item, for any reason, within 1 day of purchase."
 },
 {
  "qid": "q8743eb0591",
  "text": "You are owed a full refund on any item returned for any reason within 1 day of purchase."
 },
 {
  "qid": "q02c94ed7ae",
  "text": "Any item, any reason: full refund within 1 day of delivery."
 },
 {
  "qid": "q111f3b4baf",
  "text": "Any item sent back for any reason is covered. A full refund is due within 1 day of the order date."
 },
 {
  "qid": "q9c11832e31",
  "text": "A full refund applies to a faulty item when return is requested within 1 day of purchase."
 },
 {
  "qid": "qa6506eacec",
  "text": "Within 1 day of the order date, an item sent back for any reason is refunded in full."
 },
 {
  "qid": "q0727515ea0",
  "text": "We give a full refund to anyone who changes their mind within 1 day of the purchase date."
 },
 {
  "qid": "q49fd89b55d",
  "text": "A faulty item earns a full refund when a return is requested within 1 day of the purchase date."
 },
 {
  "qid": "qa7f8ab4027",
  "text": "We give a full refund on any product returned for any reason, within 1 day of the purchase date."
 }
]
```
