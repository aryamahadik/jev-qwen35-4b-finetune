# T31 authoring task T31-author_freeform-9a4524ec-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_freeform-9a4524ec-000.json

Task kind: author_freeform; items: 26; answers expected: 26 (one per item, each with its qid).

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
6. 30-90 words, in the item's register, natural and different from the other texts in this task.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "text": "<your
text>"}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q0b410caca7",
  "brief": "Register: ticket. Style: written on a phone, informal. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Lucas Brenner",
   "ITEM": "newsletter send",
   "REQ_ID": "TASK-8394"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q0365c4dffb",
  "brief": "Register: ticket. Style: busy and brisk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Freya Holm",
   "ITEM": "ticket sweep",
   "REQ_ID": "TASK-2386"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q5976c372d4",
  "brief": "Register: memo. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Aaron Pike",
   "ITEM": "meeting booking",
   "REQ_ID": "TASK-3396"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q8b9a74d58e",
  "brief": "Register: memo. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Talia Brook",
   "ITEM": "meeting booking",
   "REQ_ID": "TASK-5558"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qd9959ba26a",
  "brief": "Register: memo. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Caleb Strand",
   "ITEM": "document filing",
   "REQ_ID": "TASK-7375"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q51c697e787",
  "brief": "Register: ticket. Style: formal. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Aaron Pike",
   "ITEM": "calendar cleanup",
   "REQ_ID": "TASK-6946"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qf21b6ee418",
  "brief": "Register: memo. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Caleb Strand",
   "ITEM": "invoice run",
   "REQ_ID": "TASK-4843"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q496da49c3d",
  "brief": "Register: ticket. Style: written on a phone, informal. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Clara Weiss",
   "ITEM": "customer refund",
   "REQ_ID": "TASK-5758"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q4d0f6ef517",
  "brief": "Register: ticket. Style: busy and brisk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Jonas Feld",
   "ITEM": "document filing",
   "REQ_ID": "TASK-8253"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q46a1a09b96",
  "brief": "Register: memo. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Ruth Adeyemi",
   "ITEM": "calendar cleanup",
   "REQ_ID": "TASK-9319"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qa5180f82d8",
  "brief": "Register: memo. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "ITEM": "hotel change",
   "REQ_ID": "TASK-1672"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q9e36339963",
  "brief": "Register: ticket. Style: formal. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Elias Moreau",
   "ITEM": "visa filing",
   "REQ_ID": "TASK-2747"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qb76caf6db8",
  "brief": "Register: ticket. Style: plain and neutral. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "ITEM": "newsletter send",
   "REQ_ID": "TASK-5480"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q4a22b661e8",
  "brief": "Register: ticket. Style: busy and brisk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Clara Weiss",
   "ITEM": "document filing",
   "REQ_ID": "TASK-4625"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q6697c3ffcc",
  "brief": "Register: memo. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Ines Duarte",
   "ITEM": "document filing",
   "REQ_ID": "TASK-6058"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q233b628293",
  "brief": "Register: memo. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Mira Castell",
   "ITEM": "receipt upload",
   "REQ_ID": "TASK-5814"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qbf21b993fb",
  "brief": "Register: memo. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "ITEM": "release build",
   "REQ_ID": "TASK-7420"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q93e38d5ed7",
  "brief": "Register: memo. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Iris Vance",
   "ITEM": "expense report",
   "REQ_ID": "TASK-2617"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q41e03e02ec",
  "brief": "Register: memo. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "ITEM": "expense report",
   "REQ_ID": "TASK-5407"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qaa14353f0c",
  "brief": "Register: ticket. Style: plain and neutral. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Wen Zhao",
   "ITEM": "meeting booking",
   "REQ_ID": "TASK-4510"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qfe502a7c00",
  "brief": "Register: memo. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Malik Osei",
   "ITEM": "ticket sweep",
   "REQ_ID": "TASK-6824"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q67462563a6",
  "brief": "Register: ticket. Style: plain and neutral. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Aiko Brandt",
   "ITEM": "travel booking",
   "REQ_ID": "TASK-6035"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q5e088d59ff",
  "brief": "Register: ticket. Style: written on a phone, informal. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Felix Ortega",
   "ITEM": "customer refund",
   "REQ_ID": "TASK-7390"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qf8e5fed1b1",
  "brief": "Register: memo. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "memo",
  "facts": {
   "REQUESTER": "Aiko Brandt",
   "ITEM": "release build",
   "REQ_ID": "TASK-4683"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qf3a7dddcd3",
  "brief": "Register: ticket. Style: formal. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Freya Holm",
   "ITEM": "visa filing",
   "REQ_ID": "TASK-2261"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q5399408d27",
  "brief": "Register: ticket. Style: written on a phone, informal. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "ticket",
  "facts": {
   "REQUESTER": "Omar Saleh",
   "ITEM": "newsletter send",
   "REQ_ID": "TASK-5541"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_freeform-9a4524ec-000.json and nothing else.
