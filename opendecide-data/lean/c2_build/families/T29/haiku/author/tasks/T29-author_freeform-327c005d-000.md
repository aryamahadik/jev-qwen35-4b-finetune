# T29 authoring task T29-author_freeform-327c005d-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_freeform-327c005d-000.json

Task kind: author_freeform; items: 50; outputs expected: 50.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write one short FREE-FORM DOCUMENT per item, in the item's register, from the facts given. The document is the
narrative part of a page: it says who wants the agent to make a tool call and for which piece of work. A program
prints the call, a data snapshot and a policy elsewhere, so the document adds no fact of its own.

Hard rules (a document that breaks one is thrown away):
1. Two to four sentences, 30-90 words, one block of text (single line breaks allowed, never an empty line).
2. Write the REQUESTER's full name exactly as given (same letters and capitals), exactly once, and no other personal
   names, initials, nicknames or shortened forms. Use no gendered pronouns (he, she, his, her); use the name once and
   "they" or no pronoun after that.
3. Write the REASON phrase exactly as given (same letters, lowercase), exactly once. Treat it as the label of a piece
   of work and describe it no further, so the text would still read well if another work label (such as
   'vendor onboarding' or 'audit preparation') replaced it.
4. No digits, number words or ordinals; no dates, times, months, weekdays or words like today, tomorrow, now, soon,
   later, earlier; no codes or ids; no web or e-mail addresses or domains; no currency or percent signs.
5. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
6. Never approve, sign off, agree to, judge or rank the call; never mention a policy, a rule, a check or consent; say
   nothing about records, amounts, destinations, teams, environments, kinds of data, timing or risk.
7. Capital letters only at the start of a sentence or line, plus the requester's name and the words Agent and User.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "text": "<the document>"}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qa13ee40cbc",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Theo Grant",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q8f3908e5e5",
  "brief": "a request in a neutral, impersonal tone",
  "register": "memo",
  "facts": {
   "REQUESTER": "Priya Velasco",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qf7e1173fc2",
  "brief": "a message saying the request came out of a meeting",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Mateo Ruiz",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc27989c500",
  "brief": "a request that gives the context in a few words",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Tomas Ferreira",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc7e1b0ebe1",
  "brief": "a casual message with a light touch of humour",
  "register": "memo",
  "facts": {
   "REQUESTER": "Nikolai Petrov",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q8e03dc3f90",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Maya Lindqvist",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qbb32f91ceb",
  "brief": "a friendly message to the agent",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Ines Moreau",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q11b140e483",
  "brief": "a friendly message to the agent",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Amara Diallo",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q429aa4a533",
  "brief": "a request with a one-line summary first",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Ines Moreau",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q45dc304bf0",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Nikolai Petrov",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qb9a6634d8f",
  "brief": "a handoff at the change of shift",
  "register": "memo",
  "facts": {
   "REQUESTER": "Priya Velasco",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q9fdaaa7b7b",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Mateo Ruiz",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc1f032980a",
  "brief": "a note that thanks the agent",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ade Bankole",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q6cde40ae04",
  "brief": "a request from someone who joined the team recently",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ravi Anand",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q49e3777306",
  "brief": "a request that names the work first and the person second",
  "register": "chat",
  "facts": {
   "REQUESTER": "Jonah Pike",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q24dd3cf256",
  "brief": "a hurried note written between meetings",
  "register": "email",
  "facts": {
   "REQUESTER": "Dana Okafor",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc1fd825e36",
  "brief": "a casual message with a light touch of humour",
  "register": "memo",
  "facts": {
   "REQUESTER": "Lena Whitcombe",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qccd6822653",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qfd772b5052",
  "brief": "a request phrased as one step of a plan",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Mira Castell",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q843f5de5e9",
  "brief": "a structured note with labelled parts",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Lucia Romano",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q2c4607da40",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Lena Whitcombe",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q39ed0f5798",
  "brief": "a request that names the work first and the person second",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ade Bankole",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q9f2f15aec9",
  "brief": "a structured note with labelled parts",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Yara Nasser",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qfa8eabafca",
  "brief": "a request that names the work first and the person second",
  "register": "chat",
  "facts": {
   "REQUESTER": "Felix Huber",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q11ab16b823",
  "brief": "a hurried note written between meetings",
  "register": "email",
  "facts": {
   "REQUESTER": "Rosa Alvarez",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q445917d8ee",
  "brief": "a message saying the request came out of a meeting",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Ken Watanabe",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q24a3374e06",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Grace Achebe",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q922eaf97d6",
  "brief": "a handoff at the change of shift",
  "register": "memo",
  "facts": {
   "REQUESTER": "Chiara Benedetti",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q9add61c633",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Bram Visser",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qf8338ab444",
  "brief": "a note that thanks the agent",
  "register": "chat",
  "facts": {
   "REQUESTER": "Jonah Pike",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q85f53f6f7e",
  "brief": "a message that opens with a greeting",
  "register": "email",
  "facts": {
   "REQUESTER": "Dana Okafor",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q96e0e02e35",
  "brief": "a request with a one-line summary first",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Sofia Lindgren",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q210e565316",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ravi Anand",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qe9d9fb119f",
  "brief": "a message that opens with a greeting",
  "register": "email",
  "facts": {
   "REQUESTER": "Rosa Alvarez",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q15ce5d9f84",
  "brief": "a request phrased as one step of a plan",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Leo Marchetti",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qfb93dc9025",
  "brief": "a casual message with a light touch of humour",
  "register": "memo",
  "facts": {
   "REQUESTER": "Elias Strand",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qb263b977bd",
  "brief": "a request in a neutral, impersonal tone",
  "register": "memo",
  "facts": {
   "REQUESTER": "Sara Novak",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q01383ab1ef",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Leo Marchetti",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q0178324472",
  "brief": "a message saying the request came out of a meeting",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q9847155127",
  "brief": "a message that opens with a greeting",
  "register": "email",
  "facts": {
   "REQUESTER": "Hana Sato",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q120848c4b8",
  "brief": "a request from someone who joined the team recently",
  "register": "chat",
  "facts": {
   "REQUESTER": "Grace Achebe",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q2926d2efab",
  "brief": "a structured note with labelled parts",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Tomas Ferreira",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qb2e57b86bd",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Aiko Brandt",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q80b5e7f38e",
  "brief": "a friendly message to the agent",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Sofia Lindgren",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q02f60ac23a",
  "brief": "a request that gives the context in a few words",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Yara Nasser",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qdfb8285487",
  "brief": "a request filed through an internal form",
  "register": "email",
  "facts": {
   "REQUESTER": "Aiko Brandt",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qbd8380ca87",
  "brief": "a request filed through an internal form",
  "register": "email",
  "facts": {
   "REQUESTER": "Bram Visser",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qac278ce73d",
  "brief": "a request in a neutral, impersonal tone",
  "register": "memo",
  "facts": {
   "REQUESTER": "Chiara Benedetti",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q160ffda684",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Mira Castell",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qd61fcffc44",
  "brief": "a request phrased as one step of a plan",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Omar Haddad",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 }
]
