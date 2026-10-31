# T31 G-LEX extraction task T31-extract_lex-50d7ba59-000 (r2read0, top-up)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/extract/answers/T31-extract_lex-50d7ba59-000.json

Task kind: extract_lex; items: 36; answers expected: 36 (one per item, answer field "choice").

This task file is the only file you may open. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- One JSON array with exactly 36 objects, one per item; each object has exactly the keys "qid" and "choice".
- "qid": copied character for character from its item (q followed by ten letters or digits).
- "choice": one of the item's listed meanings, copied exactly, or null when none fits exactly.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
- The 36 qids of this task: qc814861db3, qe569a5ad98, q829190cf4f, q8d2ed183cd, q1417123fd8, qab426e9075, q03f9131e71, q6d20821322, q1f35f45329, qc1de0b8d55, qb268d0b2c7, qc1c4196a27, q23f9e0e621, q047bc594d7, qb8e693b5f6, q4406a371c8, qaa1e43cdba, q2a75c8ffed, qbc9999c2a4, q1b4f51dfdf, qaa56ec0afd, qdd517c33c4, q1042826952, qef9d3bbda3, q0a32438f52, q09e7d70626, q951815da17, q02d65ca996, q4fc26f8158, qea915f45c1, q2cb29b40ab, q26043a9e1b, q7cdd42fe46, qebe095a64c, q8aca3db938, qf41e80ef1e

## Instructions

Each item gives one phrase or question and a list of meanings. Pick the ONE meaning in the list that the phrase or question expresses exactly, reading its words. If no meaning in the list fits exactly, answer null. Do not answer the question, and do not judge whether any statement is true.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning copied exactly, or null>"}. Valid JSON only; no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly, or null>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qc814861db3",
  "text": "Which listed scope does the runtime policy let billing-agent invoke at the time of the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qe569a5ad98",
  "text": "Who holds the accountable (A) role for request REQ-1001 when the request was made?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "q829190cf4f",
  "text": "Which listed scope is billing-agent cleared to use at that moment?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "q8d2ed183cd",
  "text": "Does the accountable approver binding on the request map to a person other than Dana Okafor?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 },
 {
  "qid": "q1417123fd8",
  "text": "Based on the rules shown, may billing-agent use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "qab426e9075",
  "text": "At that moment, is it true that Dana Okafor does not hold the accountable approver role?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "q03f9131e71",
  "text": "Was the accountable approver role for the request given to somebody other than Dana Okafor?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q6d20821322",
  "text": "Which of the listed scopes was billing-agent authorized to use when the request was made?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "q1f35f45329",
  "text": "Out of curiosity, may billing-agent use invoices.approve at the time of the request?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qc1de0b8d55",
  "text": "Is it correct, when the request was made, that Dana Okafor does not hold the accountable approver role?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qb268d0b2c7",
  "text": "Which of these scopes may billing-agent use at the time of the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 },
 {
  "qid": "qc1c4196a27",
  "text": "Which of the listed scopes does billing-agent have permission to use at the time of the request?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q23f9e0e621",
  "text": "Does Dana Okafor hold the accountable approver role for request REQ-1001 when that request was made?",
  "choices": [
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q047bc594d7",
  "text": "Is invoices.approve permitted to be used by billing-agent at the time of the request?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qb8e693b5f6",
  "text": "Which of the listed scopes may billing-agent invoke under the runtime policy at the time of the request?",
  "choices": [
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q4406a371c8",
  "text": "Would using invoices.approve at the time of the request go beyond the authority held by billing-agent?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "qaa1e43cdba",
  "text": "Does the accountable approver role for the request sit with somebody other than Dana Okafor?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "q2a75c8ffed",
  "text": "Based on the checklist entries, does a person other than Dana Okafor hold the accountable approver role for the request?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "qbc9999c2a4",
  "text": "Going by these records, does billing-agent lack the right to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "q1b4f51dfdf",
  "text": "Just checking, does billing-agent lack the authority to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qaa56ec0afd",
  "text": "Would billing-agent be permitted to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qdd517c33c4",
  "text": "Within the runtime policy, may billing-agent invoke invoices.approve at the time of the request?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "q1042826952",
  "text": "Per the audit checklist, which of the listed scopes is billing-agent entitled to use at the time of the request?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "qef9d3bbda3",
  "text": "Would the authority of billing-agent be overstepped by using invoices.approve at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q0a32438f52",
  "text": "Does billing-agent have the right to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "q09e7d70626",
  "text": "Per the records, which listed scope may billing-agent use at the time of the request?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')"
  ]
 },
 {
  "qid": "q951815da17",
  "text": "From the records shown, does Dana Okafor hold the accountable approver role when the request was made?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "q02d65ca996",
  "text": "Is it correct that Dana Okafor does not hold the accountable approver role on this audit line?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "q4fc26f8158",
  "text": "When the request was made, was the accountable approver role held by somebody other than Dana Okafor?",
  "choices": [
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qea915f45c1",
  "text": "Which of the listed scopes is sanctioned for use by billing-agent at the time of the request?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "q2cb29b40ab",
  "text": "At that moment, which listed scope may billing-agent use?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "q26043a9e1b",
  "text": "Quick check, which of these scopes is billing-agent allowed to use at the time of the request?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q7cdd42fe46",
  "text": "Which of these scopes is approved for billing-agent to use at the time of the request?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "qebe095a64c",
  "text": "Judging from the records above, which listed scope is billing-agent permitted to use at the time of the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "q8aca3db938",
  "text": "According to the rule card, which of the listed scopes may billing-agent use at the time of the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "qf41e80ef1e",
  "text": "At the time of the request, does somebody other than Dana Okafor hold the accountable approver role?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 }
]
