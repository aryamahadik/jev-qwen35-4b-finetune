# T29 authoring task T29-author_wording-7ba474e4-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_wording-7ba474e4-000.json

Task kind: author_wording; items: 7; outputs expected: 56.

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
  "qid": "q34c426da10",
  "brief": {
   "meaning": "yes/no: does the policy allow the call {ACTION} on {TARGET} at all, either straight away or once the user confirms it? Use a positive word for allowed (allowed, acceptable under the policy, within the policy); no negation",
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
  "qid": "qcbd7d6b123",
  "brief": {
   "meaning": "yes/no: is the call {ACTION} on {TARGET} NOT barred by the policy (yes when it may run straight away or after the user's confirmation)? Use exactly one 'not' or 'n't', applied to 'barred', 'prohibited' or 'off limits'",
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
  "qid": "q87114f261d",
  "brief": {
   "meaning": "yes/no: does the policy allow the call {ACTION} on {TARGET} at all, either straight away or once the user confirms it? Use a positive word for allowed (allowed, acceptable under the policy, within the policy); no negation",
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
 },
 {
  "qid": "q7df0d63c8d",
  "brief": {
   "meaning": "yes/no: does the agent have to turn the call {ACTION} on {TARGET} down outright, because the policy bars it (so even the user's confirmation would not change that)? No negation",
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
  "qid": "q1d2fa03eea",
  "brief": {
   "meaning": "yes/no: does the agent have to turn the call {ACTION} on {TARGET} down outright, because the policy bars it (so even the user's confirmation would not change that)? No negation",
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
  "qid": "q23d3c09cb5",
  "brief": {
   "meaning": "yes/no: is the call {ACTION} on {TARGET} NOT barred by the policy (yes when it may run straight away or after the user's confirmation)? Use exactly one 'not' or 'n't', applied to 'barred', 'prohibited' or 'off limits'",
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
  "qid": "qf3fbbf2af4",
  "brief": {
   "meaning": "yes/no: does the agent have to turn the call {ACTION} on {TARGET} down outright, because the policy bars it (so even the user's confirmation would not change that)? No negation",
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
 }
]
