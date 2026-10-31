# T29 authoring task T29-author_wording-5bb519ab-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/dneg_i2/answers/T29-author_wording-5bb519ab-000.json

Task kind: author_wording; items: 6; outputs expected: 48.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS WITH TWO NEGATIONS. A program shows a policy, a proposed tool call {ACTION} on {TARGET} and
a data snapshot, then asks one question in your wording. Each item states the meaning; write the number of different
wordings it asks for, all with that same meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question, 10-30 words, ending with "?". Use {ACTION} and {TARGET} each exactly once, spelled exactly so.
2. Exactly two negations, and both are the word "not" (never n't, never no, never, none, nor, neither, without, lack,
   deny, unless, except, fail to, rule out, or any other negation cue).
3. Open with the explicit outer frame "Is it not the case that", "Is it not true that" or "Is it not so that" (capital
   on the first word only), optionally after "Under this policy," or "According to the policy,". Inside the frame the
   second "not" goes on a word of capability or clearance: "may not run", "is not cleared to run", "is not free to run",
   "is not able to run".
4. The clause inside the frame says the agent can NOT run the call right away, and the frame turns that round, so the
   whole question means: yes only when the agent can run the call right away. Never let the clause say anything else.
5. No word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere, and
   never a contracted frame (Isn't, Aren't, Doesn't, Don't ...).
6. No digits, number words, dates, clock times, hedges (maybe, probably, seems, think, believe, likely) or time words
   such as now, currently, already, soon, yet, immediately, today (say "straight away", "right away" or "at this point"
   instead). No names; capital letter only on the first word, and never the word "May" with a capital letter.
7. Never mention rule numbers, thresholds, snapshot fields or an earlier message, and never list answer choices.
8. Vary the structure across your wordings: who is the subject (the agent, the call, the policy), short and long forms,
   and which of the four capability phrases carries the second "not".
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q3f9d737a18",
  "brief": {
   "meaning": "yes/no with the same meaning as the plain question 'may the agent run the call {ACTION} on {TARGET} straight away, with no further step first?' (yes only when it can run it right away), written with exactly two negations, each the word 'not': an explicit outer frame 'is it not the case that' (or 'is it not true that', 'is it not so that') around a clause that puts 'not' on a word of capability or clearance, built on 'the agent may not run ...', 'the agent is not cleared to run ...', 'the agent is not free to run ...' or 'the agent is not able to run ...'. Put no word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere in the question, and never open with a contracted frame (isn't, aren't, doesn't, don't); no negation other than those two 'not's",
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
  "qid": "qc70bac8229",
  "brief": {
   "meaning": "yes/no with the same meaning as the plain question 'may the agent run the call {ACTION} on {TARGET} straight away, with no further step first?' (yes only when it can run it right away), written with exactly two negations, each the word 'not': an explicit outer frame 'is it not the case that' (or 'is it not true that', 'is it not so that') around a clause that puts 'not' on a word of capability or clearance, built on 'the agent may not run ...', 'the agent is not cleared to run ...', 'the agent is not free to run ...' or 'the agent is not able to run ...'. Put no word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere in the question, and never open with a contracted frame (isn't, aren't, doesn't, don't); no negation other than those two 'not's",
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
  "qid": "q37a29f2c4f",
  "brief": {
   "meaning": "yes/no with the same meaning as the plain question 'may the agent run the call {ACTION} on {TARGET} straight away, with no further step first?' (yes only when it can run it right away), written with exactly two negations, each the word 'not': an explicit outer frame 'is it not the case that' (or 'is it not true that', 'is it not so that') around a clause that puts 'not' on a word of capability or clearance, built on 'the agent may not run ...', 'the agent is not cleared to run ...', 'the agent is not free to run ...' or 'the agent is not able to run ...'. Put no word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere in the question, and never open with a contracted frame (isn't, aren't, doesn't, don't); no negation other than those two 'not's",
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
  "qid": "q441de496f1",
  "brief": {
   "meaning": "yes/no with the same meaning as the plain question 'may the agent run the call {ACTION} on {TARGET} straight away, with no further step first?' (yes only when it can run it right away), written with exactly two negations, each the word 'not': an explicit outer frame 'is it not the case that' (or 'is it not true that', 'is it not so that') around a clause that puts 'not' on a word of capability or clearance, built on 'the agent may not run ...', 'the agent is not cleared to run ...', 'the agent is not free to run ...' or 'the agent is not able to run ...'. Put no word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere in the question, and never open with a contracted frame (isn't, aren't, doesn't, don't); no negation other than those two 'not's",
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
  "qid": "q06cd594966",
  "brief": {
   "meaning": "yes/no with the same meaning as the plain question 'may the agent run the call {ACTION} on {TARGET} straight away, with no further step first?' (yes only when it can run it right away), written with exactly two negations, each the word 'not': an explicit outer frame 'is it not the case that' (or 'is it not true that', 'is it not so that') around a clause that puts 'not' on a word of capability or clearance, built on 'the agent may not run ...', 'the agent is not cleared to run ...', 'the agent is not free to run ...' or 'the agent is not able to run ...'. Put no word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere in the question, and never open with a contracted frame (isn't, aren't, doesn't, don't); no negation other than those two 'not's",
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
  "qid": "qd1522aa41c",
  "brief": {
   "meaning": "yes/no with the same meaning as the plain question 'may the agent run the call {ACTION} on {TARGET} straight away, with no further step first?' (yes only when it can run it right away), written with exactly two negations, each the word 'not': an explicit outer frame 'is it not the case that' (or 'is it not true that', 'is it not so that') around a clause that puts 'not' on a word of capability or clearance, built on 'the agent may not run ...', 'the agent is not cleared to run ...', 'the agent is not free to run ...' or 'the agent is not able to run ...'. Put no word of blocking, barring, stopping, holding back, turning down, rejecting, denying or withholding anywhere in the question, and never open with a contracted frame (isn't, aren't, doesn't, don't); no negation other than those two 'not's",
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
