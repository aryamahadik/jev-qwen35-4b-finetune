# T31 authoring task T31-author_freeform-f7d87e0e-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_freeform-f7d87e0e-000.json

Task kind: author_freeform; items: 28; answers expected: 28 (one per item, each with its qid).

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
  "qid": "qa3f307976f",
  "brief": "Register: export. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "export",
  "facts": {
   "REQUESTER": "Sara Ilves",
   "ITEM": "hotel change",
   "REQ_ID": "TASK-7391"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qfe3964142a",
  "brief": "Register: transcript. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Yara Haddad",
   "ITEM": "release build",
   "REQ_ID": "TASK-6738"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q9f89d3930a",
  "brief": "Register: email. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Iris Vance",
   "ITEM": "document filing",
   "REQ_ID": "TASK-2751"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q6febc32dea",
  "brief": "Register: export. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "export",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "ITEM": "staging deploy",
   "REQ_ID": "TASK-8063"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q81be69d051",
  "brief": "Register: transcript. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Dina Farouk",
   "ITEM": "meeting booking",
   "REQ_ID": "TASK-2559"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q7d0fc3cd8b",
  "brief": "Register: chat. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Zoe Carrick",
   "ITEM": "travel booking",
   "REQ_ID": "TASK-1701"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qa5c429ecdb",
  "brief": "Register: chat. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Omar Saleh",
   "ITEM": "invoice run",
   "REQ_ID": "TASK-7860"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qa8d0689de9",
  "brief": "Register: email. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Kofi Mensah",
   "ITEM": "customer refund",
   "REQ_ID": "TASK-8736"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q654e7ab846",
  "brief": "Register: transcript. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Ruth Adeyemi",
   "ITEM": "visa filing",
   "REQ_ID": "TASK-2703"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qe967ad76e2",
  "brief": "Register: email. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Iris Vance",
   "ITEM": "ticket sweep",
   "REQ_ID": "TASK-7822"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qb6fe7ef10b",
  "brief": "Register: chat. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Paolo Greco",
   "ITEM": "newsletter send",
   "REQ_ID": "TASK-3844"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qaa0bdf87b9",
  "brief": "Register: email. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Vikram Desai",
   "ITEM": "vendor payout",
   "REQ_ID": "TASK-8267"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q23ef313524",
  "brief": "Register: email. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Gita Rao",
   "ITEM": "invoice run",
   "REQ_ID": "TASK-9188"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qcf1aaab38e",
  "brief": "Register: transcript. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Lena Whitcombe",
   "ITEM": "newsletter send",
   "REQ_ID": "TASK-9679"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q977032e45e",
  "brief": "Register: chat. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Sara Ilves",
   "ITEM": "visa filing",
   "REQ_ID": "TASK-2421"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qd643c95d12",
  "brief": "Register: transcript. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Felix Ortega",
   "ITEM": "meeting booking",
   "REQ_ID": "TASK-6586"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q2fc9aab6f0",
  "brief": "Register: chat. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Ines Duarte",
   "ITEM": "hotel change",
   "REQ_ID": "TASK-4535"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q23a5fd7978",
  "brief": "Register: transcript. Style: careful and detailed about who is asking. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Mira Castell",
   "ITEM": "ticket sweep",
   "REQ_ID": "TASK-6029"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q7ff57a25ab",
  "brief": "Register: email. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Mira Castell",
   "ITEM": "meeting booking",
   "REQ_ID": "TASK-6339"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q92c5a523c8",
  "brief": "Register: runbook. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Maya Lindgren",
   "ITEM": "newsletter send",
   "REQ_ID": "TASK-4425"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q0c067fe4e2",
  "brief": "Register: transcript. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Nadia Kowal",
   "ITEM": "customer refund",
   "REQ_ID": "TASK-9784"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q02bdc78a78",
  "brief": "Register: runbook. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "runbook",
  "facts": {
   "REQUESTER": "Yara Haddad",
   "ITEM": "hotel change",
   "REQ_ID": "TASK-4206"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qc86949f157",
  "brief": "Register: chat. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Bruno Lacerda",
   "ITEM": "expense report",
   "REQ_ID": "TASK-5335"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q68b0a73d35",
  "brief": "Register: email. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Bea Novak",
   "ITEM": "expense report",
   "REQ_ID": "TASK-5885"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "qad54f497e2",
  "brief": "Register: transcript. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "transcript",
  "facts": {
   "REQUESTER": "Paolo Greco",
   "ITEM": "invoice run",
   "REQ_ID": "TASK-4371"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q4cb353636f",
  "brief": "Register: chat. Style: a forwarded note with a one-line intro. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Freya Holm",
   "ITEM": "staging deploy",
   "REQ_ID": "TASK-8554"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q804c81b2eb",
  "brief": "Register: email. Style: polite and short. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "email",
  "facts": {
   "REQUESTER": "Priya Raman",
   "ITEM": "calendar cleanup",
   "REQ_ID": "TASK-3174"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 },
 {
  "qid": "q38b7205b40",
  "brief": "Register: chat. Style: friendly with a little small talk. The request asks an automated software agent to carry out a task, for example an invoice run, a calendar cleanup or a release build; a person hands the task over and gives its reference code.",
  "register": "chat",
  "facts": {
   "REQUESTER": "Lucas Brenner",
   "ITEM": "receipt upload",
   "REQ_ID": "TASK-5081"
  },
  "rules": [
   "each fact exactly as given",
   "no 'a' or 'an' right before the item"
  ]
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_freeform-f7d87e0e-000.json and nothing else.
