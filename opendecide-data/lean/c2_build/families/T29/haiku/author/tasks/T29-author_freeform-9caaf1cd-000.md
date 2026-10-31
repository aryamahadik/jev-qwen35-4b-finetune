# T29 authoring task T29-author_freeform-9caaf1cd-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_freeform-9caaf1cd-000.json

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
  "qid": "q7e48913efc",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q7005389f5e",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Ken Watanabe",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q4ce4993274",
  "brief": "a message that opens with a greeting",
  "register": "email",
  "facts": {
   "REQUESTER": "Dana Okafor",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q10675a91f4",
  "brief": "a friendly message to the agent",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Ines Moreau",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q6b386078fc",
  "brief": "a request that names the work first and the person second",
  "register": "chat",
  "facts": {
   "REQUESTER": "Jonah Pike",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q58336e4177",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Leo Marchetti",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qf6891e1a87",
  "brief": "a request from someone who joined the team recently",
  "register": "chat",
  "facts": {
   "REQUESTER": "Grace Achebe",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q0b19c09852",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Mira Castell",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q9cbc599c17",
  "brief": "a request from someone who joined the team recently",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ravi Anand",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qd533501271",
  "brief": "a message saying the request came out of a meeting",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Ken Watanabe",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc7c3890a01",
  "brief": "a message that opens with a greeting",
  "register": "email",
  "facts": {
   "REQUESTER": "Hana Sato",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q5df5f77bc5",
  "brief": "a structured note with labelled parts",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Lucia Romano",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q75ada704f9",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Lena Whitcombe",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q1c0afeaa09",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Nikolai Petrov",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q79fae55410",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Maya Lindqvist",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qb9d8e6641b",
  "brief": "a request that gives the context in a few words",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Tomas Ferreira",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q9bd31a5c31",
  "brief": "a request in a neutral, impersonal tone",
  "register": "memo",
  "facts": {
   "REQUESTER": "Sara Novak",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qf6290e6261",
  "brief": "a request in a neutral, impersonal tone",
  "register": "memo",
  "facts": {
   "REQUESTER": "Priya Velasco",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q8a352be88b",
  "brief": "a polite, formal request",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Omar Haddad",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qbdfdd33c6f",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Theo Grant",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q83b04641ec",
  "brief": "a request with a one-line summary first",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Sofia Lindgren",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q6308df1e86",
  "brief": "a note that thanks the agent",
  "register": "chat",
  "facts": {
   "REQUESTER": "Felix Huber",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qb13a538833",
  "brief": "a request that gives the context in a few words",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Lucia Romano",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qe46929700e",
  "brief": "a request with a one-line summary first",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Ines Moreau",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q4c4c78c4b0",
  "brief": "a request phrased as one step of a plan",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Omar Haddad",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qdcd2598a7c",
  "brief": "a handoff at the change of shift",
  "register": "memo",
  "facts": {
   "REQUESTER": "Sara Novak",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc95d6bd26e",
  "brief": "a casual message with a light touch of humour",
  "register": "memo",
  "facts": {
   "REQUESTER": "Lena Whitcombe",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q7951365de6",
  "brief": "a request relayed from a planning session",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Mateo Ruiz",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qd6403b70d7",
  "brief": "a request phrased as one step of a plan",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Mira Castell",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q59326b7e74",
  "brief": "a hurried note written between meetings",
  "register": "email",
  "facts": {
   "REQUESTER": "Rosa Alvarez",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q5b349f8dde",
  "brief": "a handoff at the change of shift",
  "register": "memo",
  "facts": {
   "REQUESTER": "Priya Velasco",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q1386d8948c",
  "brief": "a request from someone who joined the team recently",
  "register": "chat",
  "facts": {
   "REQUESTER": "Maya Lindqvist",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q7505486500",
  "brief": "a message saying the request came out of a meeting",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q6588392c66",
  "brief": "a handoff at the change of shift",
  "register": "memo",
  "facts": {
   "REQUESTER": "Chiara Benedetti",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qac473becb4",
  "brief": "a note that thanks the agent",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ade Bankole",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qf288cec01a",
  "brief": "a hurried note written between meetings",
  "register": "email",
  "facts": {
   "REQUESTER": "Hana Sato",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qec68a9b5b2",
  "brief": "a note that thanks the agent",
  "register": "chat",
  "facts": {
   "REQUESTER": "Jonah Pike",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q256ab59732",
  "brief": "a hurried note written between meetings",
  "register": "email",
  "facts": {
   "REQUESTER": "Dana Okafor",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q9113e0a2bd",
  "brief": "a casual message with a light touch of humour",
  "register": "memo",
  "facts": {
   "REQUESTER": "Elias Strand",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qca945e208f",
  "brief": "a structured note with labelled parts",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Tomas Ferreira",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc04b9d7d08",
  "brief": "a request written for a shared work queue",
  "register": "email",
  "facts": {
   "REQUESTER": "Aiko Brandt",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q873e42af84",
  "brief": "a request that gives the context in a few words",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Yara Nasser",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc6bcf062e3",
  "brief": "a request filed through an internal form",
  "register": "email",
  "facts": {
   "REQUESTER": "Bram Visser",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qb0800fc555",
  "brief": "a request filed through an internal form",
  "register": "email",
  "facts": {
   "REQUESTER": "Aiko Brandt",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q0e8dad01cf",
  "brief": "a request that names the work first and the person second",
  "register": "chat",
  "facts": {
   "REQUESTER": "Felix Huber",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q7181818486",
  "brief": "a terse request from a busy lead",
  "register": "memo",
  "facts": {
   "REQUESTER": "Elias Strand",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q16f9bf3b5b",
  "brief": "a request filed through an internal form",
  "register": "email",
  "facts": {
   "REQUESTER": "Theo Grant",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qce6d0b7a87",
  "brief": "a short reminder-style message",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ravi Anand",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q082b0d0a7c",
  "brief": "a friendly message to the agent",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Amara Diallo",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q6f4f08fcbb",
  "brief": "a request with a one-line summary first",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Amara Diallo",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 }
]
