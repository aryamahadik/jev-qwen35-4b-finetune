# T31 G-LEX extraction task T31-extract_lex-55d2f799-002 (read1)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/extract/answers/T31-extract_lex-55d2f799-002.json

Task kind: extract_lex; items: 50; answers expected: 50 (one per item, answer field "choice").

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

Each item gives one phrase or question and a list of meanings. Pick the ONE meaning in the list that the phrase or question expresses exactly, reading its words. If no meaning in the list fits exactly, answer null. Do not answer the question, and do not judge whether any statement is true.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning copied exactly, or null>"}. Valid JSON only; no text before or after the array. Do not open, list or search any other file, and run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly, or null>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q643db36c2d",
  "text": "Does the runtime policy permit billing-agent to invoke invoices.approve at the time of the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')"
  ]
 },
 {
  "qid": "q531397fca8",
  "text": "strictly in excess of $1,200.00",
  "choices": [
   "strictly greater than the bound",
   "less than or equal to the bound",
   "greater than or equal to the bound",
   "strictly less than the bound"
  ]
 },
 {
  "qid": "q7f041ab87a",
  "text": "strictly less than the $1,200.00 ceiling",
  "choices": [
   "less than or equal to the bound",
   "strictly less than the bound",
   "strictly greater than the bound",
   "greater than or equal to the bound"
  ]
 },
 {
  "qid": "q8ec75e3a2f",
  "text": "Is it the case that billing-agent is not entitled to use invoices.approve at the time of the request under its runtime scope set?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix"
  ]
 },
 {
  "qid": "qa7b955a465",
  "text": "Is billing-agent permitted to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "q1cf63e0bc6",
  "text": "By whom was the accountable approver role held at the time of the request?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')"
  ]
 },
 {
  "qid": "q25f8c27261",
  "text": "Is the authority of billing-agent at the time of the request exceeded by using invoices.approve?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q1892013763",
  "text": "At the time of the request, which of the listed scopes may billing-agent use?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q7d63bfe98b",
  "text": "Is Dana Okafor the accountable approver at the time of the request?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "q8689a52c5b",
  "text": "Going by these records, is it true that billing-agent is not entitled to use invoices.approve at the time of the request?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix"
  ]
 },
 {
  "qid": "qf8c6c8004b",
  "text": "Going by these records, who served as the accountable approver when the request was made?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "qc1e11c6130",
  "text": "Does the accountable approver field for the request resolve to Dana Okafor at that moment?",
  "choices": [
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qac57138a63",
  "text": "Quick question: would using invoices.approve at the time of the request be too much for billing-agent?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "qcde7a38688",
  "text": "For audit purposes, does the use of invoices.approve at the time of the request go beyond the authority of billing-agent?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 },
 {
  "qid": "qd9593b093e",
  "text": "Is billing-agent cleared to use invoices.approve at the time of the request?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "q1c769e85b0",
  "text": "Which person was assigned the accountable approver post on request REQ-1001 when the request was made?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qbf8b0598f2",
  "text": "At the time of the request, does billing-agent lack the authority needed to use invoices.approve?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "q4718f98e7e",
  "text": "Just checking, did Dana Okafor have the accountable approver role at that moment?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 },
 {
  "qid": "q4a509b99c1",
  "text": "Is it correct that Dana Okafor does not hold the accountable approver designation on request REQ-1001 at the time of the request?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "qefe0045f6d",
  "text": "Per the records, which person was the accountable approver at that moment?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "qb165af98a3",
  "text": "Does billing-agent lack permission to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q24f9be2d79",
  "text": "Is invoices.approve cleared for use by billing-agent at the time of the request?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qdc588c7887",
  "text": "At that moment, is billing-agent permitted to use invoices.approve?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "q8966461f61",
  "text": "$1,200.00 excluded, anything greater",
  "choices": [
   "greater than or equal to the bound",
   "strictly greater than the bound",
   "strictly less than the bound",
   "less than or equal to the bound"
  ]
 },
 {
  "qid": "qb24dc72071",
  "text": "Hey, mind telling me who was the accountable approver at that moment?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qbb3308e185",
  "text": "at least the $1,200.00 floor, inclusive",
  "choices": [
   "greater than or equal to the bound",
   "strictly greater than the bound",
   "strictly less than the bound",
   "less than or equal to the bound"
  ]
 },
 {
  "qid": "q85a0646981",
  "text": "Based on the records above, is it true that billing-agent is not allowed to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qe7980caab3",
  "text": "For the audit file, which of the listed scopes may billing-agent use at the time of the request?",
  "choices": [
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "q2cfb647e24",
  "text": "Is it true that the use of invoices.approve by billing-agent is not permitted at the time of the request?",
  "choices": [
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)"
  ]
 },
 {
  "qid": "qbe9f401f37",
  "text": "Who was the accountable approver for the request at that moment?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "q0d05afe53f",
  "text": "Based on the records above, is it true that Dana Okafor does not hold the accountable approver role when the request was made?",
  "choices": [
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "qb90c5d5dde",
  "text": "Per the audit trail, which person acted as the accountable approver at the time of the request?",
  "choices": [
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "q8c2d6d5302",
  "text": "max $1,200.00, inclusive",
  "choices": [
   "strictly greater than the bound",
   "less than or equal to the bound",
   "strictly less than the bound",
   "greater than or equal to the bound"
  ]
 },
 {
  "qid": "q71acdbedb8",
  "text": "Which of the listed scopes was billing-agent permitted to use when the request was made?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "qaa71a93253",
  "text": "Who held the accountable approver role for this request at that moment?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request"
  ]
 },
 {
  "qid": "q0c8ef2b85c",
  "text": "at least $1,200.00, exact matches count",
  "choices": [
   "strictly greater than the bound",
   "greater than or equal to the bound",
   "less than or equal to the bound",
   "strictly less than the bound"
  ]
 },
 {
  "qid": "q3b0dc80aef",
  "text": "Is it true that billing-agent is not permitted to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)"
  ]
 },
 {
  "qid": "q236091c885",
  "text": "Under the audit checklist, does billing-agent lack the authority to use invoices.approve at the time of the request?",
  "choices": [
   "asks about the present moment rather than the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')"
  ]
 },
 {
  "qid": "q06e0941b73",
  "text": "When request REQ-1001 was made, who was the accountable approver?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "q91acad4a8d",
  "text": "Tell me, is billing-agent allowed to use invoices.approve when the request was made?",
  "choices": [
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time"
  ]
 },
 {
  "qid": "qbdfec83212",
  "text": "Is billing-agent entitled to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "q2b1980bd4a",
  "text": "Per the records, may billing-agent use invoices.approve at the time of the request?",
  "choices": [
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "qbf14600b78",
  "text": "Based on the records above, which person stood as the accountable approver when the request was made?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "qee76aba17f",
  "text": "For the audit file, is it correct that Dana Okafor does not hold the accountable approver role for the request?",
  "choices": [
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks about the present moment rather than the time of the request",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person holds the accountable (A) role for the request at its time"
  ]
 },
 {
  "qid": "q8d4d4a4024",
  "text": "According to the records, is billing-agent permitted to use invoices.approve at the time of the request?",
  "choices": [
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "q0010822152",
  "text": "Did Dana Okafor hold the accountable approver role at the time of the request?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix"
  ]
 },
 {
  "qid": "q2135a0069f",
  "text": "Did Dana Okafor hold the accountable approver role for request REQ-1001 when the request was made?",
  "choices": [
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks about the present moment rather than the time of the request",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 },
 {
  "qid": "q522cb5ceb7",
  "text": "Which person was the accountable approver when the request was made?",
  "choices": [
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks about the present moment rather than the time of the request"
  ]
 },
 {
  "qid": "qab73df1f6a",
  "text": "Mind telling me who the accountable approver was when the request was made?",
  "choices": [
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks about the present moment rather than the time of the request",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)"
  ]
 },
 {
  "qid": "qbbe64c9786",
  "text": "Going by these records, would using invoices.approve at the time of the request exceed the authority of billing-agent?",
  "choices": [
   "asks whether the named person holds the accountable (A) role for the request at its time (no negation)",
   "asks which person holds the accountable (A) role for the request at its time",
   "asks which person, or whether the named person, is marked R (responsible) in the matrix",
   "asks whether using the scope at the time of the request would exceed or go beyond the agent's authority (worded with 'exceed', 'beyond' or 'outside', with no negation)",
   "asks whether the request's approver differs from the default holder in the standing matrix",
   "asks whether the agent is permitted to use the scope at the time of the request (no negation)",
   "asks whether it is true that the named person does not hold the accountable (A) role for the request at its time (worded with an explicit 'not')",
   "asks whether it is true that the agent is not permitted to use the scope at the time of the request (worded with an explicit 'not')",
   "asks whether the agent's own grant lists the scope, whatever the time",
   "asks which of the listed scopes the agent is permitted to use at the time of the request",
   "asks whether the agent lacks the authority, permission or right to use the scope at the time of the request (worded with 'lack')",
   "asks about the present moment rather than the time of the request",
   "asks whether someone other than the named person holds the accountable (A) role for the request at its time (worded with 'other than', 'besides' or 'someone else', with no 'not')"
  ]
 }
]
