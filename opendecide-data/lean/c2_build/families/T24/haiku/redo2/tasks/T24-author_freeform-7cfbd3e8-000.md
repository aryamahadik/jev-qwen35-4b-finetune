# T24 redo2 authoring task T24-author_freeform-7cfbd3e8-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/redo2/answers/T24-author_freeform-7cfbd3e8-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. It is the only file you may open.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 50 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: q3014d97ca0, qc73691b5c8, q85c8733197, q6b8a517d2f, qbb8b4adcee, qadc35443e7, q8185e2d072, q45239bed8f, qf9b68f007b, q46564bb48f, q5ef099bc52, q9aecbf2347, q017830f0f6, q8a8f2b236b, qe3d7250077, qc8379a047e, q3b16322c1e, q80292316db, q5dd279557e, q9d70268a42, qf1e2ec3208, q8dee542269, qbed7c6932c, q2d9e810a81, q64fa033c39, qd9576de7ff, q4685afa413, q22d6eb3d59, q85dabaf5f7, q6593bc8650, qbcd98a6ba8, q99828e4964, q2f1ab9c833, q0837dc62aa, qcb508035d6, q473d103521, q132be2c792, qd3ba4f3425, q7db4b7cc04, q5e3bb99206, q301cabc4a3, q3036aaaa0c, q2cfb143b7e, qb5e0d8c3f4, qc206a9a745, q91dd835cc6, q0ab1bc72e2, q5b2fe3cd17, qce9000cef7, qa32145ff68.
- "text": one JSON string (the whole e-mail, its line breaks written as \n).
- Valid JSON only: no object around the array, no text before or after it, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one; replace the angle brackets with your own text):
[{"qid": "q3014d97ca0", "text": "<the e-mail>"}, ...]

Task kind: author_freeform; items: 50; outputs expected: 50.

You are writing short pieces of text for a synthetic training dataset about everyday customer-service
policies (returns, repairs, bookings, deposits, fees and the like). Everything you write is either a reusable template
(a program later fills each {SLOT} placeholder with a value) or a set of invented values. Write natural, varied
English. Invent everything: never copy text from real companies, products, people, laws, websites or published
datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write one short FREE-FORM DOCUMENT per item, in the item's register, from the facts given. The document is the
narrative part of a page: a message or note from or about the customer who raised a case under an invented
customer-service policy. A program prints the policy and the case record elsewhere, so the document adds no fact of
its own and never hints at how the case will be decided.

Hard rules (a document that breaks one is thrown away):
1. Two to four sentences, 25-80 words, one block of text (single line breaks allowed, never an empty line).
2. Write the CUSTOMER's full name exactly as given, letter for letter with its capitals, exactly once, and no other
   personal names, initials or nicknames. No gendered pronouns (he, she, his, her): after the name, use "they" or no
   pronoun.
3. No digits, number words or ordinals; no dates, times, months or weekdays; no words such as today, tomorrow, now,
   soon, later, earlier, yesterday, recently; no codes, case numbers or ids; no web or e-mail addresses; no currency
   or percent signs.
4. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, refuse to, prevent ... from, rule out.
5. Refer to the subject only as the case, the request, my case or my request. Say nothing about what was bought, used,
   booked or damaged; about dates, deadlines, amounts, categories or conditions; about the policy's rules or versions
   (never new, old, revised or updated rules); or about any result, any money paid back or what the customer hopes to
   get (asking to have the case looked at is fine).
6. Capital letters only at the start of a sentence or a line, plus the customer's name.

E-mail rules (every item of this task is an e-mail written BY the customer; an e-mail that breaks one is thrown away):
7. The CUSTOMER is the person who raised the case and the WRITER of the e-mail. The e-mail goes from the customer to
   the support team: never write it to the customer, and never greet the customer.
8. Three parts on separate lines (single line breaks, never an empty line): a greeting line, the message (two or three
   sentences), and the sign-off.
9. The greeting line names nobody: it greets the support team, as in "Hello,", "Hi there,", "Good day," or "Dear
   support team,". The customer's name never appears in the greeting line.
10. Put the customer's name where the item's rules say, and nowhere else: EITHER alone on the very last line, directly
   below a sign-off line such as "Kind regards," or "Thanks,"; OR in a self-introduction in the first sentence of the
   message, as in "This is ..., writing about my case." or "My name is ... and I am writing about my request." (then
   the sign-off line is the last line and holds no name).

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "text": "<the document>"}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q3014d97ca0",
  "brief": "a message with a short greeting; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Ravi Anand"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qc73691b5c8",
  "brief": "a short, plain note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Ravi Anand"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q85c8733197",
  "brief": "a message with a short greeting; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Grace Mensah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q6b8a517d2f",
  "brief": "a terse note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Tomas Ferreira"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "qbb8b4adcee",
  "brief": "a formal request to have the case looked at; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Dana Okafor"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qadc35443e7",
  "brief": "a terse note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Rosa Kim"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q8185e2d072",
  "brief": "a message from someone who writes in short sentences; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Priya Shah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q45239bed8f",
  "brief": "a friendly note with a thank-you; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Tara Walsh"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "qf9b68f007b",
  "brief": "a terse note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Hugo Laine"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q46564bb48f",
  "brief": "a polite first message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Tara Walsh"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q5ef099bc52",
  "brief": "a calm, neutral message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Omar Haddad"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q9aecbf2347",
  "brief": "a terse note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Ines Duarte"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q017830f0f6",
  "brief": "a calm, neutral message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Maya Reyes"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q8a8f2b236b",
  "brief": "a message from someone who writes in short sentences; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Leon Novak"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qe3d7250077",
  "brief": "a message with a short greeting; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Oscar Byrne"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qc8379a047e",
  "brief": "a short, plain note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Oscar Byrne"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q3b16322c1e",
  "brief": "a polite first message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Tomas Ferreira"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q80292316db",
  "brief": "a message from someone who writes in short sentences; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Tara Walsh"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q5dd279557e",
  "brief": "a formal request to have the case looked at; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Leon Novak"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q9d70268a42",
  "brief": "a calm, neutral message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Priya Shah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qf1e2ec3208",
  "brief": "a message from someone who writes in short sentences; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Victor Osei"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q8dee542269",
  "brief": "a formal request to have the case looked at; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Victor Osei"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "qbed7c6932c",
  "brief": "a friendly note with a thank-you; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Tomas Ferreira"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q2d9e810a81",
  "brief": "a formal request to have the case looked at; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Maya Reyes"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q64fa033c39",
  "brief": "a calm, neutral message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Dana Okafor"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qd9576de7ff",
  "brief": "a friendly note with a thank-you; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Leon Novak"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q4685afa413",
  "brief": "a message written in a hurry; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Dana Okafor"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q22d6eb3d59",
  "brief": "a message written in a hurry; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Oscar Byrne"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q85dabaf5f7",
  "brief": "a friendly note with a thank-you; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Aiko Brandt"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q6593bc8650",
  "brief": "a message written in a hurry; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Grace Mensah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "qbcd98a6ba8",
  "brief": "a formal request to have the case looked at; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Omar Haddad"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q99828e4964",
  "brief": "a formal request to have the case looked at; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Priya Shah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q2f1ab9c833",
  "brief": "a polite first message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Ines Duarte"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q0837dc62aa",
  "brief": "a message written in a hurry; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Nadia Petrov"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "qcb508035d6",
  "brief": "a calm, neutral message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Nadia Petrov"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q473d103521",
  "brief": "a polite first message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Mira Castell"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q132be2c792",
  "brief": "a short, plain note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Rosa Kim"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qd3ba4f3425",
  "brief": "a message with a short greeting; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Hugo Laine"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q7db4b7cc04",
  "brief": "a message written in a hurry; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Lena Whitcombe"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q5e3bb99206",
  "brief": "a terse note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Mira Castell"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q301cabc4a3",
  "brief": "a message written in a hurry; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Omar Haddad"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q3036aaaa0c",
  "brief": "a terse note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Sanjay Iqbal"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q2cfb143b7e",
  "brief": "a short, plain note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Hugo Laine"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "qb5e0d8c3f4",
  "brief": "a calm, neutral message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Lena Whitcombe"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qc206a9a745",
  "brief": "a short, plain note; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Mira Castell"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer introduces themself in the first sentence of the message (such as 'This is ..., writing about my case.' or 'My name is ... and I am writing about my request.'); the sign-off line is the last line and holds no name"
  ]
 },
 {
  "qid": "q91dd835cc6",
  "brief": "a message with a short greeting; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Lena Whitcombe"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q0ab1bc72e2",
  "brief": "a message from someone who writes in short sentences; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Aiko Brandt"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "q5b2fe3cd17",
  "brief": "a polite first message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Keiko Sato"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qce9000cef7",
  "brief": "a friendly note with a thank-you; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Keiko Sato"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 },
 {
  "qid": "qa32145ff68",
  "brief": "a polite first message; a short e-mail that the customer writes to the support team about their own case (a greeting line, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Sanjay Iqbal"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim",
   "the greeting line is written to the support team and names nobody (such as 'Hello,' or 'Dear support team,')",
   "the customer signs the e-mail: a sign-off line (such as 'Kind regards,') and then the customer's name alone on the last line"
  ]
 }
]
