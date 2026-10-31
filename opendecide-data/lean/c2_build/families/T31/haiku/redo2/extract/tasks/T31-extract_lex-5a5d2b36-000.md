# T31 G-LEX extraction task T31-extract_lex-5a5d2b36-000 (r2read1, top-up)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/redo2/extract/answers/T31-extract_lex-5a5d2b36-000.json

Task kind: extract_lex; items: 36; answers expected: 36 (one per item, answer field "choice").

This task file is the only file you may open. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- One JSON array with exactly 36 objects, one per item; each object has exactly the keys "qid" and "choice".
- "qid": copied character for character from its item (q followed by ten letters or digits).
- "choice": one of the item's listed meanings, copied exactly, or null when none fits exactly.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments.
- The 36 qids of this task: q40a37dda2c, qd8d7d79e4c, q6b5fbd9bdf, qe89c644a46, q8248a2013e, qb41451b7db, qd290b903e2, q58eb9e8c99, qdb397e0883, qed2a0dc6fd, qa4e41c766b, qffc8d11f63, q1f52e0e179, qfa278d1a78, qf21c2b604c, qfeaddce632, q85960d6b06, qceff121f0c, qbdf800c7b0, qe5a5d1c375, qb2c19ed85d, qe438e5e05d, qdca80504b5, q48af7c343e, q3e151e12b3, q0b0899cbe7, q8e52b5f6a2, q147b9b8b8c, qddca3b966c, q727858e390, q6a7a92af82, qf5dfe6e729, q486f3342e8, q39b4f962ae, q9db98b9b1e, q274a0644c9

## Instructions

Each item gives one phrase or question and a list of meanings. Pick the ONE meaning in the list that the phrase or question expresses exactly, reading its words. If no meaning in the list fits exactly, answer null. Do not answer the question, and do not judge whether any statement is true.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning copied exactly, or null>"}. Valid JSON only; no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly, or null>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q40a37dda2c",
  "text": "Would billing-agent be permitted to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "qd8d7d79e4c",
  "text": "Per the audit checklist, which of the listed scopes is billing-agent entitled to use at the time of the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "q6b5fbd9bdf",
  "text": "Would using invoices.approve at the time of the request go beyond the authority held by billing-agent?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')"
  ]
 },
 {
  "qid": "qe89c644a46",
  "text": "When the request was made, was the accountable approver role held by somebody other than Dana Okafor?",
  "choices": [
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "q8248a2013e",
  "text": "Would the authority of billing-agent be overstepped by using invoices.approve at the time of the request?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "qb41451b7db",
  "text": "Was the accountable approver role for the request given to somebody other than Dana Okafor?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix"
  ]
 },
 {
  "qid": "qd290b903e2",
  "text": "Who holds the accountable (A) role for request REQ-1001 when the request was made?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "q58eb9e8c99",
  "text": "According to the rule card, which of the listed scopes may billing-agent use at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')"
  ]
 },
 {
  "qid": "qdb397e0883",
  "text": "Which of the listed scopes was billing-agent authorized to use when the request was made?",
  "choices": [
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "qed2a0dc6fd",
  "text": "Does the accountable approver binding on the request map to a person other than Dana Okafor?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix"
  ]
 },
 {
  "qid": "qa4e41c766b",
  "text": "Is it correct that Dana Okafor does not hold the accountable approver role on this audit line?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "qffc8d11f63",
  "text": "Which listed scope is billing-agent cleared to use at that moment?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q1f52e0e179",
  "text": "Does Dana Okafor hold the accountable approver role for request REQ-1001 when that request was made?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qfa278d1a78",
  "text": "Within the runtime policy, may billing-agent invoke invoices.approve at the time of the request?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "qf21c2b604c",
  "text": "Judging from the records above, which listed scope is billing-agent permitted to use at the time of the request?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qfeaddce632",
  "text": "Just checking, does billing-agent lack the authority to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 },
 {
  "qid": "q85960d6b06",
  "text": "From the records shown, does Dana Okafor hold the accountable approver role when the request was made?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "qceff121f0c",
  "text": "Which of these scopes is approved for billing-agent to use at the time of the request?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "qbdf800c7b0",
  "text": "Going by these records, does billing-agent lack the right to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "qe5a5d1c375",
  "text": "At the time of the request, does somebody other than Dana Okafor hold the accountable approver role?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qb2c19ed85d",
  "text": "Which of the listed scopes is sanctioned for use by billing-agent at the time of the request?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "qe438e5e05d",
  "text": "Out of curiosity, may billing-agent use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qdca80504b5",
  "text": "Quick check, which of these scopes is billing-agent allowed to use at the time of the request?",
  "choices": [
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "q48af7c343e",
  "text": "Which of the listed scopes may billing-agent invoke under the runtime policy at the time of the request?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "q3e151e12b3",
  "text": "At that moment, which listed scope may billing-agent use?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix"
  ]
 },
 {
  "qid": "q0b0899cbe7",
  "text": "Which of the listed scopes does billing-agent have permission to use at the time of the request?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q8e52b5f6a2",
  "text": "Per the records, which listed scope may billing-agent use at the time of the request?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q147b9b8b8c",
  "text": "Based on the checklist entries, does a person other than Dana Okafor hold the accountable approver role for the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "qddca3b966c",
  "text": "Which of these scopes may billing-agent use at the time of the request?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q727858e390",
  "text": "Is it correct, when the request was made, that Dana Okafor does not hold the accountable approver role?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "q6a7a92af82",
  "text": "Which listed scope does the runtime policy let billing-agent invoke at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qf5dfe6e729",
  "text": "Does the accountable approver role for the request sit with somebody other than Dana Okafor?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 },
 {
  "qid": "q486f3342e8",
  "text": "Based on the rules shown, may billing-agent use invoices.approve at the time of the request?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix"
  ]
 },
 {
  "qid": "q39b4f962ae",
  "text": "Does billing-agent have the right to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix"
  ]
 },
 {
  "qid": "q9db98b9b1e",
  "text": "Is invoices.approve permitted to be used by billing-agent at the time of the request?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')"
  ]
 },
 {
  "qid": "q274a0644c9",
  "text": "At that moment, is it true that Dana Okafor does not hold the accountable approver role?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 }
]
