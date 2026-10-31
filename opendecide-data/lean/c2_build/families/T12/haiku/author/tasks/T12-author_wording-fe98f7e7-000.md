# T12 authoring task T12-author_wording-fe98f7e7-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/haiku/author/answers/T12-author_wording-fe98f7e7-000.json

Task kind: author_wording; items: 11; outputs expected: 55 (5 per item, answer field "texts").

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
  "qid": "qb25a84f4f4",
  "brief": "Write 5 questions. Each question must ask which line of bill {INVOICE_ID}, if any, fails the price check (the reader picks a line, or none, from options shown separately). Keep the words 'price check' and say 'if any' or 'if there is one'. Never mention quantities, totals or the other checks. Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "q3a8645881c",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether the policy stops or blocks payment of bill {INVOICE_ID} (yes: the invoice is kept from being paid now, whatever the reason). Build it on the idea of payment being stopped or blocked; never use the words released, held, review, rejected or routed. Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "q94ffc1a81d",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether it is NOT true that bill {INVOICE_ID} is NOT released for payment under the policy (so yes means it IS released). The question holds EXACTLY TWO negation words, each 'not' or \"n't\": one in the frame ('Is it not true that ...', \"Isn't it the case that ...\") and one negating released ('... is not released for payment'); never name another action (held, review, rejected, routed, escalated). Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Exactly two negation words as described; never 'no', 'never', 'neither', 'nor', 'without', 'fail' or 'unless'."
  ]
 },
 {
  "qid": "q8049b030e4",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether bill {INVOICE_ID} is NOT released for payment under the policy (yes: it gets some other action). The question holds EXACTLY ONE negation word, 'not' or \"n't\", and it negates released (built on '... is not released for payment' or '... isn't released for payment'); never name another action (held, review, rejected, routed, escalated). Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Exactly one negation word as described; no other negation word anywhere."
  ]
 },
 {
  "qid": "qd96214e4f8",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether the policy sends bill {INVOICE_ID} to price-variance review, that is, whether price-variance review is the one action the invoice gets. Keep the words 'price-variance review'. Never say 'on its own', 'alone' or 'price check', and never name another action (held, rejected, routed, escalated). Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "qc7cf67f6f4",
  "brief": "Write 5 questions. Each question must ask which action the policy gives bill {INVOICE_ID} (the reader picks the action from options shown separately). Never name or describe any action or outcome, and never use the words released, held, review, rejected, routed, pay or payment. Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "qf5a50e9a61",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether bill {INVOICE_ID} is released for payment under the policy. Yes must mean released for payment; no must mean any other action; never name another action (held, review, rejected, routed, escalated). Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "qf9bd06d587",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether it is NOT true that bill {INVOICE_ID} is NOT released for payment under the policy (so yes means it IS released). The question holds EXACTLY TWO negation words, each 'not' or \"n't\": one in the frame ('Is it not true that ...', \"Isn't it the case that ...\") and one negating released ('... is not released for payment'); never name another action (held, review, rejected, routed, escalated). Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Exactly two negation words as described; never 'no', 'never', 'neither', 'nor', 'without', 'fail' or 'unless'."
  ]
 },
 {
  "qid": "q0a7a4f0542",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether bill {INVOICE_ID} fails the price check taken on its own (judged by the price check alone, whatever the other checks or the check order decide). Use the words 'price check' and fail / fails, and a phrase such as 'taken on its own', 'on its own', 'by itself', 'alone' or 'looking only at'. Never use within, inside, tolerance, variance, limit, allowed or any action word. Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "q5d3e724881",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether bill {INVOICE_ID} ends in one of the four exception outcomes, naming all four joined by 'or' in any order: a hold, a review, a rejection, or a routing to a senior approver. Yes means one of them; no means released for payment. Do not mention release or payment. Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 },
 {
  "qid": "q302c8c00d9",
  "brief": "Write 5 questions. Each question must ask, as a yes/no question, whether bill {INVOICE_ID} passes the price check taken on its own (judged by the price check alone, whatever the other checks or the check order decide). Use the words 'price check' and pass / passes, and a phrase such as 'taken on its own', 'on its own', 'by itself', 'alone' or 'looking only at'. Never use within, inside, tolerance, variance, limit, allowed or any action word. Held-out style for this item: call the invoice 'bill {INVOICE_ID}' (never 'invoice') and phrase the question as an auditor quizzing a trainee. Answer field: \"texts\" (a list of 5 strings).",
  "slots": {
   "INVOICE_ID": "the invoice number"
  },
  "rules": [
   "Rules R1-R6 of the instructions apply.",
   "Use no negation word at all: not, n't, no, none, nothing, nobody, never, neither, nor, without, unless, except, lack, fail to, refuse, deny."
  ]
 }
]
