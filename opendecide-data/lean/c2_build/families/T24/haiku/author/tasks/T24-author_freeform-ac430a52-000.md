# T24 authoring task T24-author_freeform-ac430a52-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_freeform-ac430a52-000.json

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
  "qid": "q0880835f2e",
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
  "qid": "q1ef64c1afc",
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
  "qid": "q294efba9d3",
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
  "qid": "q3d9e9585ef",
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
  "qid": "q29cd4be782",
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
  "qid": "q6638a382f3",
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
  "qid": "q37dfa4de29",
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
  "qid": "q5cc8c61c58",
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
  "qid": "q3cf9b8afb9",
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
  "qid": "q517f6fa7dc",
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
  "qid": "q58597252f1",
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
  "qid": "qf5cf6461f4",
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
  "qid": "qa92a178110",
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
  "qid": "q64f8197926",
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
  "qid": "q3fa95fa236",
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
  "qid": "q08c4c8fd7c",
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
  "qid": "q2223715b34",
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
  "qid": "qde121c3c2c",
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
  "qid": "q9cae185b1e",
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
  "qid": "qd6691cef90",
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
  "qid": "q5b62eb7cde",
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
  "qid": "q41801f74ae",
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
  "qid": "q7b7915093d",
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
  "qid": "qdc8b93ccb9",
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
  "qid": "qcf56ad19db",
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
  "qid": "qe03533a625",
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
  "qid": "qd1cfdc7b25",
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
  "qid": "qc4a07630c9",
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
  "qid": "q44c9ed95a5",
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
  "qid": "qafab1d5958",
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
  "qid": "qb83769ac2c",
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
  "qid": "qd314d56eff",
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
  "qid": "q6085d5a724",
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
  "qid": "qe4aec10ff0",
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
  "qid": "q08a7e6331f",
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
  "qid": "qa8993ded82",
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
  "qid": "qaa4631d1a6",
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
  "qid": "qe66c6c16cd",
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
  "qid": "qd32d5804f7",
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
  "qid": "q5f855c1bcd",
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
  "qid": "qed783404ad",
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
  "qid": "q4e10acc86d",
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
  "qid": "q4125f75bf2",
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
  "qid": "qad685a2e5b",
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
  "qid": "q86ac4dd51d",
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
  "qid": "qcc45c71397",
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
  "qid": "q687e20ccf0",
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
  "qid": "qa4137f45fe",
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
  "qid": "q14169ecd3e",
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
  "qid": "q5a9d84a5dd",
  "brief": "a terse note; a short e-mail from the customer (a greeting, the message, a sign-off)",
  "register": "email",
  "facts": {
   "CUSTOMER": "Aiko Brandt"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 }
]
