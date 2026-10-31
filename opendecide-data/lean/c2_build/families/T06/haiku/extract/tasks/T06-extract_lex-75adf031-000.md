# T06 extraction task T06-extract_lex-75adf031-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/extract/answers/T06-extract_lex-75adf031-000.json

Task: extract_lex; glex-r3; items: 50; outputs expected: 50.

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
- the store accepts returns within the stated days but does not say what the customer gets back
- the store promises a full refund to a customer who changed their mind, within the stated days of the purchase (order) date
- the store promises a full refund for faulty items asked for within the stated days of the purchase (order) date
- the store promises a full refund for any reason within the stated days of the purchase (order) date
- the store gives store credit or an exchange, not money back, for returns within the stated days
- the store promises a full refund for any reason within the stated days of the delivery date

ITEMS (JSON; answer every item, keyed by its qid):
```json
[
 {
  "qid": "q40f7ec2d42",
  "text": "You are owed a full refund on any item returned for any reason within 30 days of purchase."
 },
 {
  "qid": "q54fcd8ebf0",
  "text": "A faulty item earns a full refund when a return is requested within 30 days of the purchase date."
 },
 {
  "qid": "qd65803f77a",
  "text": "A faulty item is refunded in full. The return must be asked for within 30 days of the order date."
 },
 {
  "qid": "qbdbd12bb83",
  "text": "Changing your mind is covered. A full refund is due within 30 days of the day you ordered."
 },
 {
  "qid": "q04c3c44f6e",
  "text": "Should you change your mind, you are owed a full refund within 30 days of the order date."
 },
 {
  "qid": "qb574092bfa",
  "text": "We issue a refund in full for any item returned for any reason, within 30 days of delivery."
 },
 {
  "qid": "q21f0759436",
  "text": "We give a full refund on any product returned for any reason, within 30 days of the purchase date."
 },
 {
  "qid": "qa2a976cfe5",
  "text": "Within 30 days of the purchase date, any faulty item is refunded in full."
 },
 {
  "qid": "qb8ff071430",
  "text": "If an item is faulty, you are refunded in full when you ask for a return within 30 days of the purchase date."
 },
 {
  "qid": "q27bd05c93d",
  "text": "Any item returned for any reason earns you a full refund within 30 days of purchase."
 },
 {
  "qid": "qcadfb90c9c",
  "text": "A faulty item is covered. A full refund applies when the return is requested within 30 days of your order."
 },
 {
  "qid": "q589e2e3979",
  "text": "We refund in full any item, for any reason, when returned within 30 days of purchase."
 },
 {
  "qid": "q30ba68e574",
  "text": "Refunded in full: any item returned for any reason, within 30 days of delivery."
 },
 {
  "qid": "q3127178696",
  "text": "We give a full refund to anyone who changes their mind within 30 days of the purchase date."
 },
 {
  "qid": "q6bede915f1",
  "text": "Within 30 days of the order date, an item sent back for any reason is refunded in full."
 },
 {
  "qid": "q594b74e195",
  "text": "Full refund for any faulty item, if the return is asked for within 30 days of purchase."
 },
 {
  "qid": "q5fb9b09f1e",
  "text": "Any item you return, for any reason, is refunded in full within 30 days of the delivery date."
 },
 {
  "qid": "q6b9cd56583",
  "text": "Any item you return for any reason, within 30 days of delivery, earns you a full refund."
 },
 {
  "qid": "qc1cd0ebf99",
  "text": "Any item can be returned for any reason. A full refund is yours if you return it within 30 days of the order date."
 },
 {
  "qid": "qaaf370eea5",
  "text": "Any item, any reason: full refund within 30 days of delivery."
 },
 {
  "qid": "qac0b5a5437",
  "text": "Expect a full refund on any item, whatever the reason, within 30 days from the day you ordered."
 },
 {
  "qid": "q011ab5065a",
  "text": "Full refund for any item sent back, whatever the reason, within 30 days of delivery."
 },
 {
  "qid": "q7b11722ab2",
  "text": "Within 30 days of your purchase, you can return any item for any reason and be refunded in full."
 },
 {
  "qid": "q7780a8fe74",
  "text": "Any item may be sent back for any reason. Such returns are refunded in full within 30 days of delivery."
 },
 {
  "qid": "q98ae376755",
  "text": "Any item returned for any reason: refunded in full within 30 days of the order date."
 },
 {
  "qid": "q1e9180f648",
  "text": "Refund in full on any returned item, for any reason, within 30 days of purchase."
 },
 {
  "qid": "q10b901775e",
  "text": "Faulty items only. A full refund is given when a return is asked for within 30 days of the order date."
 },
 {
  "qid": "q9287d31b22",
  "text": "A full refund within 30 days of the purchase date is given for a change of mind."
 },
 {
  "qid": "q3eb295fb08",
  "text": "Refunded in full within 30 days of delivery, on any item returned for any reason."
 },
 {
  "qid": "q56dc5fc089",
  "text": "Any item sent back for any reason is covered. A full refund is due within 30 days of the order date."
 },
 {
  "qid": "q602b025a3b",
  "text": "Within 30 days of the order date, a faulty item qualifies for a full refund on request."
 },
 {
  "qid": "qf505d821ea",
  "text": "Within 30 days of the order date, a faulty item gets a full refund."
 },
 {
  "qid": "qd66589fc38",
  "text": "Any item returned, whatever the reason, gets a refund in full within 30 days of delivery."
 },
 {
  "qid": "qda79aa4fb7",
  "text": "We give a full refund on any item returned for any reason, within 30 days of the delivery date."
 },
 {
  "qid": "q8ab748ecb1",
  "text": "Return any item, for any reason. You will be refunded in full within 30 days of delivery."
 },
 {
  "qid": "q9e11449a07",
  "text": "Within 30 days of delivery, any item sent back for any reason is refunded in full."
 },
 {
  "qid": "qd5fadaa65e",
  "text": "Within 30 days of the delivery date, any returned item is refunded in full, whatever the reason."
 },
 {
  "qid": "qf5fe142e90",
  "text": "You can return any item for any reason. It is refunded in full within 30 days of the purchase date."
 },
 {
  "qid": "qd4a0bd451a",
  "text": "A full refund applies to every item, whichever the reason it is returned, within 30 days of delivery."
 },
 {
  "qid": "q1d31560444",
  "text": "Faulty item: refund in full within 30 days of purchase."
 },
 {
  "qid": "qe1fcbeb29b",
  "text": "Have you changed your mind? You are refunded in full within 30 days of purchase."
 },
 {
  "qid": "qd814b991b4",
  "text": "We give a full refund for faulty items when you ask for a return within 30 days of the purchase date."
 },
 {
  "qid": "q3141a47de5",
  "text": "Returns for any reason are accepted on any item. A full refund is given within 30 days of delivery."
 },
 {
  "qid": "q09a77207c1",
  "text": "Within 30 days from delivery, send back any item for any reason and earn a full refund."
 },
 {
  "qid": "qbd6694c6d5",
  "text": "Within 30 days of the purchase date, you are refunded in full for changing your mind."
 },
 {
  "qid": "q388c5f323f",
  "text": "A full refund applies to a faulty item when return is requested within 30 days of purchase."
 },
 {
  "qid": "qeccb14c276",
  "text": "Any item returned for any reason: full refund within 30 days of the purchase date."
 },
 {
  "qid": "q1639a6e6bd",
  "text": "We give a full refund for faulty items if you ask for a return within 30 days of purchase."
 },
 {
  "qid": "qa5330e77fa",
  "text": "Within 30 days of purchase, any returned item is refunded in full, whatever the reason."
 },
 {
  "qid": "q4c0cdf0f5f",
  "text": "You can ask for a full refund on a faulty item within 30 days of the day you bought it."
 }
]
```
