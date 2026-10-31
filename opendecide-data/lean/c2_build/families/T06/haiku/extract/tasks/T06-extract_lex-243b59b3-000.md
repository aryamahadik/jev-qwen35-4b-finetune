# T06 extraction task T06-extract_lex-243b59b3-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/extract/answers/T06-extract_lex-243b59b3-000.json

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
- the store promises a full refund for faulty items asked for within the stated days of the purchase (order) date
- the store promises a full refund for any reason within the stated days of the delivery date
- the store promises a full refund for any reason within the stated days of the purchase (order) date
- the store accepts returns within the stated days but does not say what the customer gets back
- the store promises a full refund within the stated days of the day the customer received or collected the goods
- the store promises a full refund to a customer who changed their mind, within the stated days of the purchase (order) date
- the store gives store credit or an exchange, not money back, for returns within the stated days

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "q69ede2026c",
  "text": "Any item returned, whatever the reason, gets a refund in full within 7 days of delivery."
 },
 {
  "qid": "q89e90becaa",
  "text": "Refunded in full within 7 days of delivery, on any item returned for any reason."
 },
 {
  "qid": "q71ed2d143c",
  "text": "Any item you return, for any reason, is refunded in full within 7 days of the delivery date."
 },
 {
  "qid": "q7cfac94173",
  "text": "Any item may be sent back for any reason. Such returns are refunded in full within 7 days of delivery."
 },
 {
  "qid": "q2dc2a232d1",
  "text": "Within 7 days of purchase, any returned item is refunded in full, whatever the reason."
 },
 {
  "qid": "q6093b6e4f1",
  "text": "Expect a full refund on any item, whatever the reason, within 7 days from the day you ordered."
 },
 {
  "qid": "qac13838216",
  "text": "Any item returned for any reason earns you a full refund within 7 days of purchase."
 },
 {
  "qid": "q5fdad712f9",
  "text": "We give a full refund on any product returned for any reason, within 7 days of the purchase date."
 },
 {
  "qid": "q1aa491491e",
  "text": "Refund in full on any returned item, for any reason, within 7 days of purchase."
 },
 {
  "qid": "q63877c5c08",
  "text": "A faulty item is refunded in full. The return must be asked for within 7 days of the order date."
 },
 {
  "qid": "qc397817513",
  "text": "Should you change your mind, you are owed a full refund within 7 days of the order date."
 },
 {
  "qid": "q4cc175dbf3",
  "text": "Changing your mind is covered. A full refund is due within 7 days of the day you ordered."
 },
 {
  "qid": "qba63a30774",
  "text": "A full refund within 7 days of the purchase date is given for a change of mind."
 },
 {
  "qid": "q626e1981f3",
  "text": "A faulty item earns a full refund when a return is requested within 7 days of the purchase date."
 },
 {
  "qid": "q0bbcfba1bb",
  "text": "We give a full refund on any item returned for any reason, within 7 days of the delivery date."
 },
 {
  "qid": "qdbc88286e7",
  "text": "We refund in full any item, for any reason, when returned within 7 days of purchase."
 },
 {
  "qid": "q783bbb14e1",
  "text": "Within 7 days of the order date, an item sent back for any reason is refunded in full."
 },
 {
  "qid": "qac9638b116",
  "text": "Have you changed your mind? You are refunded in full within 7 days of purchase."
 },
 {
  "qid": "q22a8943120",
  "text": "Within 7 days of the purchase date, you are refunded in full for changing your mind."
 },
 {
  "qid": "q10334c7159",
  "text": "Within 7 days of the order date, a faulty item gets a full refund."
 },
 {
  "qid": "q6d41fc5f3d",
  "text": "Refunded in full: any item returned for any reason, within 7 days of delivery."
 },
 {
  "qid": "qcc4e16bccf",
  "text": "Return any item, for any reason. You will be refunded in full within 7 days of delivery."
 },
 {
  "qid": "qfb89686a0f",
  "text": "Within 7 days of the order date, a faulty item qualifies for a full refund on request."
 },
 {
  "qid": "q4ca130ba4b",
  "text": "Within 7 days of the purchase date, any faulty item is refunded in full."
 },
 {
  "qid": "q9ef38c9a12",
  "text": "Any item, any reason: full refund within 7 days of delivery."
 },
 {
  "qid": "q577603864e",
  "text": "Any item can be returned for any reason. A full refund is yours if you return it within 7 days of the order date."
 },
 {
  "qid": "q8cea8792cb",
  "text": "Faulty items only. A full refund is given when a return is asked for within 7 days of the order date."
 },
 {
  "qid": "q23c422e1fe",
  "text": "Within 7 days from delivery, send back any item for any reason and earn a full refund."
 },
 {
  "qid": "qc7d90ad8e4",
  "text": "Within 7 days of the delivery date, any returned item is refunded in full, whatever the reason."
 },
 {
  "qid": "qb4b2231910",
  "text": "Any item sent back for any reason is covered. A full refund is due within 7 days of the order date."
 },
 {
  "qid": "q11534e070b",
  "text": "We give a full refund for faulty items if you ask for a return within 7 days of purchase."
 },
 {
  "qid": "q9765cb4f06",
  "text": "Any item you return for any reason, within 7 days of delivery, earns you a full refund."
 },
 {
  "qid": "qcdd54d71f7",
  "text": "You can return any item for any reason. It is refunded in full within 7 days of the purchase date."
 },
 {
  "qid": "q1c78ba567b",
  "text": "If an item is faulty, you are refunded in full when you ask for a return within 7 days of the purchase date."
 },
 {
  "qid": "qc98e61facb",
  "text": "A full refund applies to every item, whichever the reason it is returned, within 7 days of delivery."
 },
 {
  "qid": "q07ab8f9d7d",
  "text": "Within 7 days of your purchase, you can return any item for any reason and be refunded in full."
 },
 {
  "qid": "q4d44061184",
  "text": "A faulty item is covered. A full refund applies when the return is requested within 7 days of your order."
 },
 {
  "qid": "qc200d6eeaa",
  "text": "Returns for any reason are accepted on any item. A full refund is given within 7 days of delivery."
 },
 {
  "qid": "q74b6ec4b73",
  "text": "You are owed a full refund on any item returned for any reason within 7 days of purchase."
 },
 {
  "qid": "q8f628079a5",
  "text": "We give a full refund for faulty items when you ask for a return within 7 days of the purchase date."
 },
 {
  "qid": "q24e2f75531",
  "text": "Faulty item: refund in full within 7 days of purchase."
 },
 {
  "qid": "q5656f80ad7",
  "text": "You can ask for a full refund on a faulty item within 7 days of the day you bought it."
 },
 {
  "qid": "qf03c5e43bd",
  "text": "We give a full refund to anyone who changes their mind within 7 days of the purchase date."
 },
 {
  "qid": "qec1ed5f184",
  "text": "Full refund for any faulty item, if the return is asked for within 7 days of purchase."
 },
 {
  "qid": "q6576aa1820",
  "text": "Any item returned for any reason: refunded in full within 7 days of the order date."
 },
 {
  "qid": "q92ee427a93",
  "text": "Within 7 days of delivery, any item sent back for any reason is refunded in full."
 },
 {
  "qid": "qec93287052",
  "text": "A full refund applies to a faulty item when return is requested within 7 days of purchase."
 },
 {
  "qid": "qed590bf935",
  "text": "Full refund for any item sent back, whatever the reason, within 7 days of delivery."
 },
 {
  "qid": "q9f57d905f9",
  "text": "We issue a refund in full for any item returned for any reason, within 7 days of delivery."
 },
 {
  "qid": "qcea4dee481",
  "text": "Any item returned for any reason: full refund within 7 days of the purchase date."
 }
]
```
