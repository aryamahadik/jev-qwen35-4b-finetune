# T41 G-LEX extraction task T41-glex-read1-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/a57_pool_quarantine/T41/glex/answers/T41-glex-read1-000.json

Task kind: extract_lex; items: 50; answers expected: 50 (one per item).

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

Each item gives one line and a list of meanings. Pick the ONE meaning in the list that the line expresses exactly, reading its words. If no meaning in the list fits exactly, answer null. Do not answer the line, and do not judge whether anything is true.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one entry per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning copied exactly, or null>"}. Valid JSON only; no text before or after the array. Run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly, or null>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "qf8d56e7674",
  "text": "Does the agent settle the proposed action alone, either by running it or by refusing it?",
  "choices": [
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q2aecedd951",
  "text": "Must the agent hold the action back, either by refusing it or by asking the user for approval?",
  "choices": [
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?"
  ]
 },
 {
  "qid": "qe50584a7d7",
  "text": "Which outcome does the proposed action get: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q5852df3b54",
  "text": "Is it true that the agent can't run the action on its own?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?"
  ]
 },
 {
  "qid": "q4c6650969c",
  "text": "Is the action blocked because the origin of a value is untrusted and its delegation covers another action?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "qc415375502",
  "text": "Is it true that the action isn't blocked for the origin of a value?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q99c625ff7c",
  "text": "Does the proposed action pause for the user's confirmation to run?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "q5754a0e49f",
  "text": "a production from a production may be used straight away by the agent without asking the user",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "q0607f32da8",
  "text": "Is it true that the action for a value's origin isn't blocked?",
  "choices": [
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)"
  ]
 },
 {
  "qid": "q51407e60b1",
  "text": "Is the action blocked because a value came from an untrusted source and a covering delegation is absent?",
  "choices": [
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "qf5df27a645",
  "text": "Is the action stopped because an untrusted source supplied a value and a covering delegation is absent?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q9f58652135",
  "text": "Is the action blocked because a value came from an untrusted source and its delegation covers another action?",
  "choices": [
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q8162c22869",
  "text": "What decision applies to the proposed action: run, block for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q2df600d451",
  "text": "Does the agent decide the action by itself, either by running it or by refusing it?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "qc184864b80",
  "text": "the agent may use a production that comes from a production directly without asking the user",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "q41e5572c23",
  "text": "Does the agent settle the action alone, either by running it or by refusing it?",
  "choices": [
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?"
  ]
 },
 {
  "qid": "qb6f0f6c584",
  "text": "Does the proposed action end in either running on its own or waiting for the user's confirmation?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?"
  ]
 },
 {
  "qid": "q7441a1714b",
  "text": "Which decision does the proposed action get: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "qf7069f1f10",
  "text": "Does the action wait for the user's confirmation to run?",
  "choices": [
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q67a52728d8",
  "text": "a production drawn from a production may be used by the agent directly with no user question",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "q9d6de79e26",
  "text": "Is the action's end state either an autonomous run or a pause for the user's confirmation?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "q96bd355b1e",
  "text": "Is the agent allowed to run the proposed action by itself, bypassing any refusal and any check with the user?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?"
  ]
 },
 {
  "qid": "qe65824da6f",
  "text": "Which decision does the proposed action get: run, blocked for an untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?"
  ]
 },
 {
  "qid": "q6e9d06c04e",
  "text": "Which of the decisions applies to the proposed action: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q640ae650db",
  "text": "Does the agent have to hold the proposed action back, either by refusing it or by checking with the user?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?"
  ]
 },
 {
  "qid": "qeac1bb661a",
  "text": "Does the proposed action wait for the user's confirmation to run?",
  "choices": [
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)"
  ]
 },
 {
  "qid": "q9dd89094fc",
  "text": "Is it true that the agent is not able to run the action on its own?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)"
  ]
 },
 {
  "qid": "q86ee7d09b3",
  "text": "a production that comes from a production may be used only after explicit user confirmation",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used only after the user confirms it"
  ]
 },
 {
  "qid": "q1e6adf55e7",
  "text": "Is it true that the agent can't carry out the action by itself?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "q2033c5bb44",
  "text": "Does the proposed action need the user's confirmation to run?",
  "choices": [
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?"
  ]
 },
 {
  "qid": "q1882d7fb26",
  "text": "Is it not true that the agent can't run the action on its own?",
  "choices": [
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q4f5bf5dace",
  "text": "Would the agent be permitted to run the proposed action by itself, skipping refusal and the user check?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "q32aac79d97",
  "text": "Is it true that the action is not blocked for the origin of a value?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?"
  ]
 },
 {
  "qid": "q3e6b0e7007",
  "text": "Must the agent hold the action back, either by refusing it or by checking with the user?",
  "choices": [
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "qc1cb99b6c4",
  "text": "Does the agent decide the proposed action by itself, either by running it or by refusing it?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q030a010ce9",
  "text": "Is it not true that the agent cannot run the action on its own?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?"
  ]
 },
 {
  "qid": "qc4ac5870b9",
  "text": "a production coming from a production is usable only when the user confirms it first",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used only after the user confirms it"
  ]
 },
 {
  "qid": "qbc16abcef5",
  "text": "a production that comes from a production may be used directly, with no question put to the user",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "q9cdaa45f3d",
  "text": "Before it runs, must the action await the user's confirmation?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "qbf181851df",
  "text": "Is the agent allowed to run the proposed action on its own, skipping any refusal and any check with the user?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q82e2c4ff5a",
  "text": "Must the agent hold the proposed action back, either by refusing it or by checking with the user?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?"
  ]
 },
 {
  "qid": "q030adbf1ac",
  "text": "Will the action either run on its own or wait for the user's confirmation?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)"
  ]
 },
 {
  "qid": "q509d80f913",
  "text": "Does the action wait for the user's confirmation before it runs?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?"
  ]
 },
 {
  "qid": "qa6d3e5130f",
  "text": "Does a value from an untrusted origin block the action, with its covering delegation absent?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "q721108a1b3",
  "text": "Does the proposed action finish by either running alone or waiting for the user to confirm?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?"
  ]
 },
 {
  "qid": "q1d7c4c9393",
  "text": "a production that comes from a production can be used by the agent directly with no question to the user",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "q42efe00d6a",
  "text": "Does the agent settle the proposed action alone, by either running it or refusing it?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?"
  ]
 },
 {
  "qid": "q49f57a4337",
  "text": "Does the agent settle the action alone, by either running it or refusing it?",
  "choices": [
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "qc3350404e4",
  "text": "Which decision applies to the proposed action: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "q7a4f9cbb1c",
  "text": "Must the agent hold back the action, by refusing it or by checking with the user?",
  "choices": [
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?"
  ]
 }
]
