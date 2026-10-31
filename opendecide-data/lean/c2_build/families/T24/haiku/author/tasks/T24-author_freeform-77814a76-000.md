# T24 authoring task T24-author_freeform-77814a76-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_freeform-77814a76-000.json

Task kind: author_freeform; items: 24; outputs expected: 24.

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
  "qid": "qb0e32770dd",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Lena Whitcombe"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q8227852340",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Dana Okafor"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q699cb1bf93",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Sanjay Iqbal"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qeb40fb78f8",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Omar Haddad"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q86602b5eb1",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Lena Whitcombe"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q04bf6fa413",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Tara Walsh"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qad25e34bb9",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Aiko Brandt"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q81f327a1b1",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Nadia Petrov"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q69079ebc41",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Tomas Ferreira"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q72a36b64ef",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Priya Shah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q937708da41",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Keiko Sato"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q46e66ece75",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Mira Castell"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qa598ae8d27",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Victor Osei"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q2fbdc12d04",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Rosa Kim"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q909e0a481f",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Ines Duarte"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qfb3f697660",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Dana Okafor"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qc7cc95be89",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Oscar Byrne"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q89f9edd70c",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Leon Novak"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q4337de147a",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Nadia Petrov"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q9956685c2f",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Grace Mensah"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qb3a1abe770",
  "brief": "a polite first message; a short transcript of a phone call, with lines starting 'Agent:' and 'Caller:'",
  "register": "transcript",
  "facts": {
   "CUSTOMER": "Ravi Anand"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qd6ed6e1dd0",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Hugo Laine"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "qe6570487ee",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Maya Reyes"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 },
 {
  "qid": "q2e9ca73acf",
  "brief": "a terse note; a voicemail the customer leaves, as spoken",
  "register": "voicemail",
  "facts": {
   "CUSTOMER": "Omar Haddad"
  },
  "rules": [
   "exactly one document",
   "the name exactly once, verbatim"
  ]
 }
]
