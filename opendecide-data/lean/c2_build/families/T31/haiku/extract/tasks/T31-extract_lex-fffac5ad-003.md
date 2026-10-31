# T31 G-LEX extraction task T31-extract_lex-fffac5ad-003 (read0)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/extract/answers/T31-extract_lex-fffac5ad-003.json

Task kind: extract_lex; items: 37; answers expected: 37 (one per item, answer field "choice").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

Each item gives one phrase or question and a list of meanings. Pick the ONE meaning in the list that the phrase or question expresses exactly, reading its words. If no meaning in the list fits exactly, answer null. Do not answer the question, and do not judge whether any statement is true.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning copied exactly, or null>"}. Valid JSON only; no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly, or null>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q0d5eb3ebf4",
  "text": "Was billing-agent permitted to use invoices.approve when the request was made?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q0b22487fa5",
  "text": "Under the audit procedure, which person was recorded as the accountable approver when the request was made?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "q179ccdf7d7",
  "text": "When the request was made, who is the accountable approver?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "q290cdd5a33",
  "text": "Is invocation of invoices.approve by billing-agent permitted at the time of the request?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q8bc63ffd1f",
  "text": "Following the audit procedure, who was the accountable approver at the time of the request?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "q32b29081fd",
  "text": "Would using invoices.approve at the time of the request exceed the authority of billing-agent?",
  "choices": [
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q33882258cb",
  "text": "Which person is the value of the accountable approver field for the request at that moment?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "q2b52cf6176",
  "text": "Would billing-agent exceed its authority with invoices.approve at the time of the request?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "qccb7eec155",
  "text": "Is it true that Dana Okafor does not hold the accountable approver role for request REQ-1001?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q2de2ff51bb",
  "text": "up to and including $1,200.00",
  "choices": [
   "strictly less than the bound",
   "less than or equal to the bound",
   "strictly greater than the bound",
   "greater than or equal to the bound"
  ]
 },
 {
  "qid": "qa185b991f2",
  "text": "strictly greater than the stated threshold $1,200.00",
  "choices": [
   "strictly less than the bound",
   "greater than or equal to the bound",
   "less than or equal to the bound",
   "strictly greater than the bound"
  ]
 },
 {
  "qid": "qdc25d0cc06",
  "text": "Did Dana Okafor hold the accountable approver role at the time of the request?",
  "choices": [
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "q047f4d7ad3",
  "text": "Is it true that the accountable approver role for request REQ-1001 is not held by Dana Okafor when the request was made?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q9b7ec8db53",
  "text": "min $1,200.00, inclusive",
  "choices": [
   "strictly greater than the bound",
   "greater than or equal to the bound",
   "less than or equal to the bound",
   "strictly less than the bound"
  ]
 },
 {
  "qid": "qf401538527",
  "text": "Is it the case that billing-agent is not allowed to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q6e8ff12370",
  "text": "less than or equal to $1,200.00, inclusive",
  "choices": [
   "greater than or equal to the bound",
   "strictly greater than the bound",
   "strictly less than the bound",
   "less than or equal to the bound"
  ]
 },
 {
  "qid": "qb4f6d23f74",
  "text": "strictly greater than the level of $1,200.00",
  "choices": [
   "greater than or equal to the bound",
   "less than or equal to the bound",
   "strictly greater than the bound",
   "strictly less than the bound"
  ]
 },
 {
  "qid": "q344e5eda68",
  "text": "Was Dana Okafor the accountable approver on request REQ-1001 when the request was made?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "q52f80a67d5",
  "text": "At that moment, going by these records, did Dana Okafor hold the accountable approver role?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "qe52028fd4f",
  "text": "When the request was made, did Dana Okafor hold the accountable approver role?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "q1c4bdcc0b3",
  "text": "When the request was made, which person held the accountable approver role for REQ-1001?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q92a44691ec",
  "text": "lower than or equal to $1,200.00",
  "choices": [
   "less than or equal to the bound",
   "greater than or equal to the bound",
   "strictly greater than the bound",
   "strictly less than the bound"
  ]
 },
 {
  "qid": "q5abb2131f4",
  "text": "Going by these records, would using invoices.approve at the time of the request exceed the authority of billing-agent?",
  "choices": [
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q9b96f8eaca",
  "text": "At that moment, does the accountable approver field point to anybody other than Dana Okafor?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "q9ab1a2e53f",
  "text": "Which of the listed scopes was billing-agent permitted to use when the request was made?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "qd12ab16b45",
  "text": "Just to confirm, is it true that billing-agent is not permitted to use invoices.approve at the time of the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qc8897d92cd",
  "text": "Would it be somebody other than Dana Okafor who had the accountable approver role when the request was made?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "q4fdb107f27",
  "text": "Is billing-agent entitled to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 },
 {
  "qid": "q9ae0c4c9ee",
  "text": "$1,200.00 excluded, anything lower",
  "choices": [
   "greater than or equal to the bound",
   "less than or equal to the bound",
   "strictly less than the bound",
   "strictly greater than the bound"
  ]
 },
 {
  "qid": "qfcb7822fc4",
  "text": "Who had the accountable approver role when the request was made?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q0832de57a0",
  "text": "At the time of the request, does billing-agent lack the authority needed to use invoices.approve?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "qfe1bbf22be",
  "text": "Tell me, is billing-agent allowed to use invoices.approve when the request was made?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "qe76fc5f007",
  "text": "Based on the records above, is it true that billing-agent is not allowed to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q5ff4eca392",
  "text": "Did Dana Okafor hold the accountable approver role for request REQ-1001 when the request was made?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qe55cf7f0c7",
  "text": "less than $1,200.00, the threshold excluded",
  "choices": [
   "greater than or equal to the bound",
   "strictly greater than the bound",
   "strictly less than the bound",
   "less than or equal to the bound"
  ]
 },
 {
  "qid": "qcd67cef0c2",
  "text": "For the audit file, which of the listed scopes may billing-agent use at the time of the request?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "qcdb88eba5a",
  "text": "at most $1,200.00, and that counts",
  "choices": [
   "strictly greater than the bound",
   "strictly less than the bound",
   "greater than or equal to the bound",
   "less than or equal to the bound"
  ]
 }
]
