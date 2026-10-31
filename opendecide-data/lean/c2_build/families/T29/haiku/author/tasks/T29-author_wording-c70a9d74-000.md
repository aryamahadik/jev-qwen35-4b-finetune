# T29 authoring task T29-author_wording-c70a9d74-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_wording-c70a9d74-000.json

Task kind: author_wording; items: 8; outputs expected: 64.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS. A program shows a policy, a proposed tool call {ACTION} on {TARGET} and a data
snapshot, then asks one question in your wording. Each item states exactly what the question must mean; write the
number of different wordings it asks for, all with that same meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question, 8-30 words, ending with "?". Use {ACTION} and {TARGET} each exactly once, spelled exactly so.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it.
3. Use a negation word only where the item asks for one, and then exactly one ("not" or "n't"), placed as the item
   says. Everywhere else: no negation at all (not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out).
4. No digits, number words, dates, clock times, hedges (maybe, probably, seems, think, believe, likely) or time
   words such as now, currently, already, soon, yet, immediately, today (say "straight away", "right away" or "at
   this point" instead). No names; capital letter only on the first word.
5. Never mention rule numbers, thresholds, snapshot fields or an earlier message, and never list answer choices
   unless the item says the question names outcomes.
6. Vary the structure across your wordings: who is the subject (the agent, the call, the policy), modal verbs,
   "Under this policy, ...", "According to the policy, ...", short and long forms.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qa854b611c0",
  "brief": {
   "meaning": "yes/no: may the agent run the call {ACTION} on {TARGET} straight away, with no further step first? (yes only when it can run it right away). No negation",
   "style": "formal and policy-centred",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once"
  ]
 },
 {
  "qid": "q2d1e6ce838",
  "brief": {
   "meaning": "yes/no: may the agent run the call {ACTION} on {TARGET} straight away, with no further step first? (yes only when it can run it right away). No negation",
   "style": "short and direct",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once"
  ]
 },
 {
  "qid": "q558118111e",
  "brief": {
   "meaning": "yes/no: may the agent run the call {ACTION} on {TARGET} straight away, with no further step first? (yes only when it can run it right away). No negation",
   "style": "plain conversational",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once"
  ]
 },
 {
  "qid": "qcd211facc6",
  "brief": {
   "meaning": "yes/no: does the call {ACTION} on {TARGET} end in one of these two named outcomes: the agent holds the call until the user explicitly confirms it, or the agent turns the call down outright? Name both outcomes in the question. No negation",
   "style": "neutral reviewer's tone",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once"
  ]
 },
 {
  "qid": "q7bb7a1d8fd",
  "brief": {
   "meaning": "yes/no: may the agent run the call {ACTION} on {TARGET} straight away, with no further step first? (yes only when it can run it right away). No negation",
   "style": "agent-centred",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once"
  ]
 },
 {
  "qid": "q0f97d06c83",
  "brief": {
   "meaning": "yes/no, the negated form of: 'may the agent run {ACTION} on {TARGET} straight away?'. Put exactly one 'not' or 'n't' on running it straight away, e.g. 'is the agent not clear to ...' (yes when the agent has to hold the call or turn it down)",
   "style": "careful and precise",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once"
  ]
 },
 {
  "qid": "q9f68527d14",
  "brief": {
   "meaning": "yes/no: does the call {ACTION} on {TARGET} end in one of these two named outcomes: the agent holds the call until the user explicitly confirms it, or the agent turns the call down outright? Name both outcomes in the question. No negation",
   "style": "brisk, workplace tone",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once"
  ]
 },
 {
  "qid": "q9102711aa6",
  "brief": {
   "meaning": "yes/no, the negated form of: 'may the agent run {ACTION} on {TARGET} straight away?'. Put exactly one 'not' or 'n't' on running it straight away, e.g. 'is the agent not clear to ...' (yes when the agent has to hold the call or turn it down)",
   "style": "about the call itself as the subject",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once"
  ]
 }
]
