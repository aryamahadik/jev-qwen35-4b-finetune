# T12 authoring task T12-author_wording-7811a383-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/author/answers/T12-author_wording-7811a383-000.json

Task kind: author_wording; items: 6; outputs expected: 30 (5 per item, answer field "texts").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

You write question lines for a synthetic training dataset. Setting: in an accounts-payable (AP) team, a clerk matches a supplier's invoice against the purchase order (PO) and the goods receipt under a written company policy. A program builds every example: it prints the documents, the policy and the question, and it fills every value. Everything you write must be invented: never copy text from real companies, products, people, laws, websites or published datasets. The policy card lists two to four checks for the invoice: always a quantity check (invoiced against received quantities) and a price check (invoiced against PO unit prices); sometimes a check against a register of invoices already paid, and a check of the invoice total against an approver's limit. The checks run in a stated check order, and the first check that fails sets the one action the invoice gets: it is released for payment only when every check passes; otherwise it is held for receipt, sent to price-variance review, rejected as a duplicate, or routed to a senior approver. Your question is shown after the card and the documents; the placeholder {INVOICE_ID} stands for the invoice number. You never see the card, the documents or the answer, and you never answer the question. In this task you may use the action and check words an item asks for. Each item says exactly what its questions must ask; two independent readers must recover that meaning and a program counts negation words, so write precise, unambiguous questions. Each item asks for 5 questions in the answer field "texts".

RULES (every item):
R1. Each question is one sentence on one line, ends with a question mark and has at most 30 words.
R2. Use {INVOICE_ID} exactly once, spelled exactly like that, right after the word for the invoice ("invoice {INVOICE_ID}", or "bill {INVOICE_ID}" where the item says so); no other placeholder or curly brace.
R3. Refer to the policy as "the policy", "this policy", "the AP policy" or "the card".
R4. No digit or number word (one, two, first, second, half), no date or time word (now, today, next, last, already, yet, later, soon), no hedge (maybe, probably, likely, seem, appear, think), no name, and no capitalised word except the first word and AP or PO.
R5. Never hint at the answer, and never mention answer options, letters, codes or a list to choose from.
R6. The 5 questions of an item differ in structure and wording, not only in one or two words.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item, in item order: {"qid": "<the item's qid>", "<answer field>": ...}. Copy each qid exactly; give exactly the number of outputs each item asks for. Valid JSON only (escape an inner double quote as \" and a line break inside a text as \n); no comments, no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "texts": [...]}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qf3c60ec542",
  "brief": "Write 5 questions. Each question must ask which line of invoice {INVOICE_ID}, if any, fails the price check (the reader picks a line, or none, from options shown separately). Keep the words 'price check' and say 'if any' or 'if there is one'. Never mention quantities, totals or the other checks. Style for this item: conversational but exact. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "q2122a71ff3",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether the policy sends invoice {INVOICE_ID} to price-variance review, that is, whether price-variance review is the one action the invoice gets. Keep the words 'price-variance review'. Never say 'on its own', 'alone' or 'price check', and never name another action (held, rejected, routed, escalated). Style for this item: formal wording that refers to the policy. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "qf884264db7",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether the policy sends invoice {INVOICE_ID} to price-variance review, that is, whether price-variance review is the one action the invoice gets. Keep the words 'price-variance review'. Never say 'on its own', 'alone' or 'price check', and never name another action (held, rejected, routed, escalated). Style for this item: framed as a check of how the policy treats this invoice. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "q219855b370",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether the policy sends invoice {INVOICE_ID} to price-variance review, that is, whether price-variance review is the one action the invoice gets. Keep the words 'price-variance review'. Never say 'on its own', 'alone' or 'price check', and never name another action (held, rejected, routed, escalated). Style for this item: plain everyday wording. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "q2dd09c7534",
  "brief": "Write 5 questions. Each question must ask which line of invoice {INVOICE_ID}, if any, fails the price check (the reader picks a line, or none, from options shown separately). Keep the words 'price check' and say 'if any' or 'if there is one'. Never mention quantities, totals or the other checks. Style for this item: framed as a check of how the policy treats this invoice. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "q8983636cfb",
  "brief": "Write 5 questions. Each question must ask which line of invoice {INVOICE_ID}, if any, fails the price check (the reader picks a line, or none, from options shown separately). Keep the words 'price check' and say 'if any' or 'if there is one'. Never mention quantities, totals or the other checks. Style for this item: framed around the outcome under this policy. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 }
]
