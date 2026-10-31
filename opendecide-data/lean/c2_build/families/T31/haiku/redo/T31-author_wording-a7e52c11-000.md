# T31 REDO authoring task T31-author_wording-a7e52c11-000 (kind: author_wording; 1 item)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo/answers/T31-author_wording-a7e52c11-000.json

WHY THIS FILE EXISTS: this task was given once before. All of its items were answered except one, whose answer came
back under a mistyped id (a character was missing) and so could not be matched to its item. This file asks for that
one item again. Answer ONLY the 1 item listed at the bottom of this file.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 1 object.
- The object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character, from the item at the bottom of this file. A qid is the
  letter q followed by ten letters or digits (11 characters in all). The qid of the item to answer is: qc40242781b
- "text": your question wording as one JSON string, with its placeholders written as described in the instructions.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.

Literal example of the required shape (put your own wording in "text"; the qid shown is the real one):
[{"qid": "qc40242781b", "text": "<your question wording goes here, ending with a question mark>"}]

Task kind: author_wording; items: 1; answers expected: 1 (one per item, with its qid).

FULL INSTRUCTIONS (the same instructions every other item of this task was written under):

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS about the accountable (A) role for a sign-off request (who is the approver). A program shows a rule card and a block of records, then asks one
question in your wording. Each item states exactly what the question must mean; write one wording per item, and make
the wordings in this task clearly different from each other.

Placeholders (plain, exactly as written; no grammar helpers inside questions):
  {CANDIDATE}  a person's full name        {REQ_AGENT}  an agent id such as ledger-bot
  {REQ_SCOPE}  a scope id such as invoices.send   {REQ_ID}  the request's reference code
Use each placeholder the item requires exactly once; use {REQ_ID} only where the item allows it (at most once);
use no other placeholder.

Hard rules (a wording that breaks one is thrown away):
1. One question, 6-30 words, ending with "?".
2. Keep the meaning exactly as the item states it: same person, agent or scope, the time of the request, no
   widening, narrowing or softening.
3. Sign-off questions call the role "the accountable (A) role", "the A role" or "the accountable approver"; never
   "responsible", "owner", "manager" or "in charge" (those name other things).
4. Agent questions are about permission at the time of the request (whether the agent may use the scope then),
   never about whether the agent's grant lists the scope.
5. Time: "at the time of the request", "when the request was made", "at that moment", or no time phrase. Never now,
   currently, today, still, already, yet, at present.
6. Negation only where the item asks for it, and then exactly as the item says. Everywhere else none of: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, fail to, refuse to, decline to, hardly, barely, scarcely, few, except, unless, false, other than, free of, no longer, rule out, prevent ... from.
7. No digits, number words, dates, names or capital letters (except the first word and the placeholders); no hedges
   (maybe, probably, seems, likely). Never list answer choices; never mention any other person, agent or scope.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
question>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qc40242781b",
  "brief": "Meaning: Ask which person holds the accountable (A) role, that is who the approver is, for the request at the time it was made. The program shows the people as answer options; do not list them. Style: conversational, as a colleague would ask.",
  "slots": {
   "REQ_ID": "optional, at most once"
  },
  "rules": [
   "no negation at all"
  ]
 }
]

Reminder: write one JSON array with exactly 1 object ({"qid": "...", "text": "..."}) to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo/answers/T31-author_wording-a7e52c11-000.json and nothing else.
