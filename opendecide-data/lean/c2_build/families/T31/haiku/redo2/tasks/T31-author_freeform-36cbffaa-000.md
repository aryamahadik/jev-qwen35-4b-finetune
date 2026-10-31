# T31 TOP-UP authoring task T31-author_freeform-36cbffaa-000 (kind: author_freeform; 6 items)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/answers/T31-author_freeform-36cbffaa-000.json

WHY THIS TASK EXISTS: new items for the T31 pool (Mode F share of the chat / email / transcript top-up (about 20% of the pool, G0 7)). Every item is new; answer all 6.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 6 objects, one per item at the bottom of this file.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character. A qid is the letter q followed by ten letters or digits
  (11 characters in all). Every qid below appears exactly once in your answer; never invent or shorten one.
- "text": your text as one JSON string (a line break inside it as \n, a double quote as \").
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
- The 6 qids of this task: q7d1e3e3516, q94b3dc00fd, q531b711ff8, q6c703eaf7a, q998d5f3d83, q251af08a46
Literal example of the shape (your own text in "text"):
[{"qid": "q7d1e3e3516", "text": "..."}, ...]

Task kind: author_freeform; items: 6; answers expected: 6 (one per item, each with its qid).

FULL INSTRUCTIONS:

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write FREE-FORM OPENINGS: short natural texts in the register each item names (a memo, an email, a chat
message, a ticket description, a call transcript, a runbook step or an export note) in which a person raises a
request. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code. A program later puts a block of records and a question after your text; you never see
them. Each item gives three facts (a person, an item, a reference code). Your text must contain each fact EXACTLY as
given (same spelling and capitals), as plain words (no braces).

Hard rules (a text that breaks one is thrown away by a checking program):
1. The person's full name once or twice; the item text exactly once; the reference code exactly once.
2. Never put "a" or "an" directly before the item, and never start a sentence with the item: write "the <item>",
   "our <item>", "this <item>" or "<person>'s <item>". Write the text so it still reads naturally if another item,
   name or code of the same kind were put in their place (say nothing else about the item itself).
3. Add no other person, team name, company, number, date, time, amount, code, website or e-mail address; no digits
   and no number words (one, first, second, half ...).
4. Never mention records, roles, approvers, delegations, scopes, permissions, rules, deadlines, decisions or
   outcomes, and never say or hint whether anything was signed off, cleared, permitted, refused or is still waiting.
5. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, fail to, refuse to, decline to, hardly, barely, scarcely, few, except, unless, false, other than, free of, no longer, rule out, prevent ... from.
6. No number word at all, not even 'one' (never 'one more thing', 'this one' or 'one quick note'); never 'kind of'
   or 'sort of'.
7. 30-90 words, in the item's register, natural and different from the other texts in this task.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
text>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q7d1e3e3516",
  "brief": "Register: chat. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Maya Lindgren",
   "ITEM": "document filing",
   "REQ_ID": "TASK-4748"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item",
   "no number word, not even 'one'"
  ]
 },
 {
  "qid": "q94b3dc00fd",
  "brief": "Register: email. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Eva Marsh",
   "ITEM": "invoice run",
   "REQ_ID": "TASK-9627"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item",
   "no number word, not even 'one'"
  ]
 },
 {
  "qid": "q531b711ff8",
  "brief": "Register: email. Style: plain and neutral. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Bea Novak",
   "ITEM": "log review",
   "REQ_ID": "TASK-8317"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item",
   "no number word, not even 'one'"
  ]
 },
 {
  "qid": "q6c703eaf7a",
  "brief": "Register: transcript. Style: written on a phone, informal. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Caleb Strand",
   "ITEM": "hotel change",
   "REQ_ID": "TASK-1788"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item",
   "no number word, not even 'one'"
  ]
 },
 {
  "qid": "q998d5f3d83",
  "brief": "Register: chat. Style: busy and brisk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Sara Ilves",
   "ITEM": "document filing",
   "REQ_ID": "TASK-4305"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item",
   "no number word, not even 'one'"
  ]
 },
 {
  "qid": "q251af08a46",
  "brief": "Register: transcript. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Yara Haddad",
   "ITEM": "ticket sweep",
   "REQ_ID": "TASK-8335"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item",
   "no number word, not even 'one'"
  ]
 }
]

Reminder: write one JSON array with exactly 6 objects ({"qid": "...", "text": "..."}) to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/answers/T31-author_freeform-36cbffaa-000.json and nothing else.
