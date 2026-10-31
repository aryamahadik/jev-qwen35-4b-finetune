# T06 redo2 authoring task T06-author_wording-ee2771cd-000 (kind author_wording)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T06/haiku/redo2/answers/T06-author_wording-ee2771cd-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 16 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: q9d281000bf, q75e6bfec3e, q3b1a92a248, q737eff5aaa, q230f17482d, q1e29f99cac, q17fae6d672, q2d27375142, q090597c2c7, qb0e98ac209, q9907e5567e, qbfcbfdba40, q974f05a29f, q52cc259ec2, q4f0de8677a, q343b8d00d3.
- "text": one JSON string: the question (one sentence ending with ?).
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one): [{"qid": "q9d281000bf", "text": "<the question>"}, ...]

Task kind: author_wording; items: 16; outputs expected: 16.

## Instructions

You write questions for a reading test about online shopping. Every test item shows one returns case: a consumer law's rules for returns, the store's posted returns notice, an order record and a customer message. The reader answers a question about the case. You see none of the test items. Every item below asks for ONE question with the meaning given in the item: on which date the period of the customer's legal right to cancel the purchase for any reason ends (the final day of that period). The options, shown separately, are dates. The same law gives a second right, about faulty goods; that is a different question and is never named here.

Hard rules (a program throws away any question that breaks one):
1. One sentence ending with "?", 8-30 words, plain English. Refer to "the customer"; no names. A capital letter only on the first word.
2. Name the right with the verb "cancel" or "withdraw" together with the words "for any reason", and say "legal", "law" or "statutory". Ways to name it: "the customer's legal right to cancel the purchase for any reason", "the right the law gives the customer to withdraw for any reason", "the customer's statutory right to cancel for any reason".
3. Never write the word "from" anywhere in the question. So never "withdraw from the purchase", "counted from" or "runs from": with "withdraw", write "withdraw for any reason"; with "cancel", write "cancel the purchase" or "cancel this order".
4. Never say when the period starts or what it is counted by: none of the words delivery, delivered, possession, received, collected, ordered, "order date", "purchase date", "date of purchase", counted, counting, start, starts, begins.
5. Never mention the store's notice, sign, policy or promise, and never write "store's". Never mention faulty goods or rejecting.
6. Ask for the date or day the period ends: use the word "date" or "day", and "end", "run out" or "final day". Never write last, next, now, today, still, yet, already, soon or later.
7. No negation of any kind: not, n't, no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, except, unless, "other than", lack, fail.
8. No digits, number words or ordinals, no dates or month names, no hedges (maybe, perhaps, probably, likely). Never start the question with "May".
9. Ask about the case; never ask whether some answer is correct, and never mention options by letter.
10. Follow the item's style hint for the opening. Never repeat a question that the item lists as already taken, and make every question you write differ from every other one.

## Items (16; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q9d281000bf",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: a plain question that ends with 'in this case?'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q75e6bfec3e",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: a plain question that ends with 'in this case?'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q3b1a92a248",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: a plain question with no opening phrase.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q737eff5aaa",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: open with 'In this case,'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q230f17482d",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: open with 'On the case as written,'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q1e29f99cac",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: a plain question that ends with 'here?'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q17fae6d672",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: a plain question with no opening phrase.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q2d27375142",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: open with 'On these facts,'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q090597c2c7",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: open with 'In this case,'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "qb0e98ac209",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: a plain question that names 'this order' in the middle.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q9907e5567e",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: open with 'On these facts,'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "qbfcbfdba40",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: open with 'Looking at this order,'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q974f05a29f",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: open with 'For this return,'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q52cc259ec2",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: a plain question that ends with 'for this order?'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q4f0de8677a",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: open with 'Taking the facts as given,'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 },
 {
  "qid": "q343b8d00d3",
  "brief": "A multiple-choice question whose options are dates: on which date does the period of the customer's legal right to cancel the purchase for any reason end (its final day)? The law also calls this the right to withdraw for any reason.",
  "slots": [],
  "rules": [
   "Name that legal right with cancel or withdraw plus 'for any reason', and say 'legal', 'law' or 'statutory'. Never write the word 'from'. Never mention the store's notice or promise, faulty goods, or the day the period is counted by. Say 'end', 'run out' or 'final day', never 'last'. No negation.",
   "Style hint: a plain question that ends with 'here?'.",
   "Already taken (never repeat these): For this return, on what final day does the period of the customer's legal right to cancel for any reason end? | In this case, on which date does the period of the customer's legal right to cancel the purchase for any reason end? | Looking at this order, which date ends the period of the customer's legal right to cancel the purchase for any reason? | Taking the facts as given, on which day does the customer's legal right to cancel the purchase for any reason run out?"
  ]
 }
]
```
