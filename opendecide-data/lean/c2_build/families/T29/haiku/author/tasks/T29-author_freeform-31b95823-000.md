# T29 authoring task T29-author_freeform-31b95823-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_freeform-31b95823-000.json

Task kind: author_freeform; items: 24; outputs expected: 24.

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
  "qid": "q4188463359",
  "brief": "a request with a one-line summary first",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Amara Diallo",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qd03a15161b",
  "brief": "a short reminder-style message",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Grace Achebe",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q1b797b2bdb",
  "brief": "a casual message with a light touch of humour",
  "register": "plan",
  "facts": {
   "REQUESTER": "Nikolai Petrov",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q2a45ea3947",
  "brief": "a terse request from a busy lead",
  "register": "plan",
  "facts": {
   "REQUESTER": "Elias Strand",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q0f495e6541",
  "brief": "a request phrased as one step of a plan",
  "register": "plan",
  "facts": {
   "REQUESTER": "Leo Marchetti",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qe985673d7e",
  "brief": "a request from someone who joined the team recently",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Maya Lindqvist",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc4c7c372be",
  "brief": "a polite, formal request",
  "register": "plan",
  "facts": {
   "REQUESTER": "Omar Haddad",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q8fb30aac51",
  "brief": "a note that thanks the agent",
  "register": "plan",
  "facts": {
   "REQUESTER": "Felix Huber",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qf265c98b32",
  "brief": "a message that opens with a greeting",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Rosa Alvarez",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qce83c59e93",
  "brief": "a message saying the request came out of a meeting",
  "register": "plan",
  "facts": {
   "REQUESTER": "Mateo Ruiz",
   "REASON": "month-end close"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qed9f824dd8",
  "brief": "a friendly message to the agent",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Sofia Lindgren",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qc6142727fd",
  "brief": "a hurried note written between meetings",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Hana Sato",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qb47e122dd0",
  "brief": "a request that gives the context in a few words",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Lucia Romano",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qf5f618c314",
  "brief": "a request that names the work first and the person second",
  "register": "plan",
  "facts": {
   "REQUESTER": "Ade Bankole",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qf24c08441e",
  "brief": "a terse request from a busy lead",
  "register": "plan",
  "facts": {
   "REQUESTER": "Lena Whitcombe",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qbfdeb5583f",
  "brief": "a request relayed from a planning session",
  "register": "plan",
  "facts": {
   "REQUESTER": "Ken Watanabe",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qcaadf36d6a",
  "brief": "a request in a neutral, impersonal tone",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Chiara Benedetti",
   "REASON": "vendor onboarding"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q1b8f09e1b0",
  "brief": "a request from someone who joined the team recently",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Ravi Anand",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "qefe4021bd7",
  "brief": "a polite, formal request",
  "register": "plan",
  "facts": {
   "REQUESTER": "Mira Castell",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q680451a981",
  "brief": "a request filed through an internal form",
  "register": "plan",
  "facts": {
   "REQUESTER": "Theo Grant",
   "REASON": "audit preparation"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q10bad4c51b",
  "brief": "a handoff at the change of shift",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Sara Novak",
   "REASON": "quarterly cleanup"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q643897d828",
  "brief": "a request written for a shared work queue",
  "register": "plan",
  "facts": {
   "REQUESTER": "Bram Visser",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q73418829b1",
  "brief": "a structured note with labelled parts",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Yara Nasser",
   "REASON": "incident follow-up"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 },
 {
  "qid": "q33e1b96489",
  "brief": "a hurried note written between meetings",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Dana Okafor",
   "REASON": "customer migration"
  },
  "rules": [
   "exactly one document",
   "the name and the reason phrase each exactly once, verbatim"
  ]
 }
]
