# T24 authoring task T24-author_freeform-9b31a329-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_freeform-9b31a329-000.json

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

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "text": "<the document>"}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q7c45a742d0",
  "brief": "a terse note; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Sanjay Iqbal"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q9032881c7b",
  "brief": "a polite first message; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Leon Novak"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q3350bc414b",
  "brief": "a polite first message; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Ines Duarte"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q3e0bf29a50",
  "brief": "a terse note; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Keiko Sato"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q56451dcb5b",
  "brief": "a terse note; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Oscar Byrne"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q08484ba948",
  "brief": "a terse note; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Mira Castell"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q3d30d9a32a",
  "brief": "a polite first message; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Tara Walsh"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q744849cf08",
  "brief": "a terse note; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Victor Osei"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q4bcd54d69a",
  "brief": "a polite first message; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Tomas Ferreira"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qdfc4eb0de8",
  "brief": "a terse note; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Keiko Sato"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qd2f4d5f2d8",
  "brief": "a polite first message; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Tara Walsh"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qe7078d9197",
  "brief": "a terse note; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Victor Osei"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qb98e3c888a",
  "brief": "a polite first message; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Tomas Ferreira"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q210deb5641",
  "brief": "a terse note; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Keiko Sato"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qda35e0795a",
  "brief": "a terse note; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Lena Whitcombe"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q13854df560",
  "brief": "a polite first message; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Rosa Kim"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qedb32f1417",
  "brief": "a polite first message; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Grace Mensah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qfd0d47e034",
  "brief": "a polite first message; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Priya Shah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q964dcd6906",
  "brief": "a polite first message; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Tara Walsh"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q1d744c199a",
  "brief": "a polite first message; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Ravi Anand"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qe2471a6141",
  "brief": "a terse note; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Aiko Brandt"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qbaa66fe996",
  "brief": "a terse note; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Victor Osei"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qe8745528f3",
  "brief": "a terse note; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Omar Haddad"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q62597a1e8f",
  "brief": "a terse note; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Omar Haddad"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q112a5aa723",
  "brief": "a polite first message; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Ines Duarte"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q50602df0ce",
  "brief": "a polite first message; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Grace Mensah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qade37cc0d8",
  "brief": "a terse note; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Aiko Brandt"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q7e79b14db8",
  "brief": "a polite first message; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Tomas Ferreira"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q3ee8811d80",
  "brief": "a polite first message; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Ines Duarte"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q409c1efb73",
  "brief": "a terse note; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Sanjay Iqbal"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q09ad7fa32e",
  "brief": "a terse note; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Oscar Byrne"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q6aa5e090ec",
  "brief": "a polite first message; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Leon Novak"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q2b8af552e0",
  "brief": "a terse note; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Maya Reyes"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q233c406e18",
  "brief": "a polite first message; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Leon Novak"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q66c3728de3",
  "brief": "a terse note; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Maya Reyes"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q84c11a1479",
  "brief": "a terse note; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Hugo Laine"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qac326dc431",
  "brief": "a polite first message; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Dana Okafor"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q5872245037",
  "brief": "a polite first message; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Ravi Anand"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qd506137c82",
  "brief": "a terse note; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Maya Reyes"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q46f6cb77bb",
  "brief": "a terse note; the free-text description of a support ticket, written by a support agent",
  "register": "ticket",
  "facts": {
   "CUSTOMER": "Mira Castell"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q52fc452954",
  "brief": "a terse note; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Aiko Brandt"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q5c42e0ee82",
  "brief": "a terse note; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Lena Whitcombe"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q196fab0be9",
  "brief": "a polite first message; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Dana Okafor"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q6be6e04839",
  "brief": "a polite first message; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Priya Shah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qe3370f3dad",
  "brief": "a polite first message; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Nadia Petrov"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qcc9fd340c6",
  "brief": "a polite first message; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Nadia Petrov"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q24ef2eeb98",
  "brief": "a polite first message; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Priya Shah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q5ac90452bc",
  "brief": "a polite first message; an internal note a support agent writes about the customer's contact",
  "register": "memo",
  "facts": {
   "CUSTOMER": "Rosa Kim"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qdf926065e8",
  "brief": "a terse note; a chat message the customer types to a support agent",
  "register": "chat",
  "facts": {
   "CUSTOMER": "Hugo Laine"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q447a7c9993",
  "brief": "a terse note; a short formal letter from the customer",
  "register": "letter",
  "facts": {
   "CUSTOMER": "Sanjay Iqbal"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 }
]
