# T41 G-LEX extraction task T41-glex-read2-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/a57_pool_quarantine/T41/glex/answers/T41-glex-read2-000.json

Task kind: extract_lex; items: 50; answers expected: 50 (one per item).

This task file is the only file you may open. Do not open, list or search any other file or folder.

## Instructions

Each item gives one line and a list of meanings. Pick the ONE meaning in the list that the line expresses exactly, reading its words. If no meaning in the list fits exactly, answer null. Do not answer the line, and do not judge whether anything is true.

OUTPUT. Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one entry per item: {"qid": "<the item's qid>", "choice": "<the chosen meaning copied exactly, or null>"}. Valid JSON only; no text before or after the array. Run no other tool.

Answer format: [{"qid": "<qid>", "choice": "<one meaning, copied exactly, or null>"}, ...]

## Items (JSON; answer every item once, keyed by its qid)

[
 {
  "qid": "q2b3d911aec",
  "text": "Is the action blocked because a value came from an untrusted source and a covering delegation is absent?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "q976b312249",
  "text": "Which decision is given to the proposed action: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?"
  ]
 },
 {
  "qid": "qb9ce6d7cc6",
  "text": "What decision applies to the proposed action: run, block for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "q51902594f9",
  "text": "Is it not true that the agent can't run the action on its own?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?"
  ]
 },
 {
  "qid": "q44183665d7",
  "text": "a production from a production may be used straight away by the agent without asking the user",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "qe2a9c1241f",
  "text": "Is it true that the action isn't blocked for the origin of a value?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?"
  ]
 },
 {
  "qid": "q6196e2ec15",
  "text": "Is it true that the agent can't carry out the action by itself?",
  "choices": [
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "q27990066da",
  "text": "Is the action's end state either an autonomous run or a pause for the user's confirmation?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q0a0896f2ad",
  "text": "Which decision applies to the proposed action: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "qe6cf6b58a1",
  "text": "Does the agent have clearance to run the proposed action by itself, skipping refusal and the user check?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?"
  ]
 },
 {
  "qid": "q2a4dc8b5fb",
  "text": "Would the agent be permitted to run the proposed action by itself, skipping refusal and the user check?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?"
  ]
 },
 {
  "qid": "qc1c670303f",
  "text": "Does the agent decide the proposed action by itself, either by running it or by refusing it?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?"
  ]
 },
 {
  "qid": "qbf6386525f",
  "text": "Does a value from an untrusted origin block the action, with its covering delegation absent?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)"
  ]
 },
 {
  "qid": "q382278778a",
  "text": "Is it true that the origin of a value does not block the action?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?"
  ]
 },
 {
  "qid": "qe03614f44c",
  "text": "Must the agent hold the proposed action back, either by refusing it or by checking with the user?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?"
  ]
 },
 {
  "qid": "q98d8d24920",
  "text": "the agent may use a production that comes from a production directly without asking the user",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "qae82097cc8",
  "text": "Is it not true that the agent cannot run the action by itself?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "qc9b7a54e70",
  "text": "Does the proposed action wait for the user's confirmation to run?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q68a6dced85",
  "text": "a production that comes from a production may be used only after the user confirms it",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used only after the user confirms it"
  ]
 },
 {
  "qid": "q81595cb6b4",
  "text": "Does the proposed action need the user's confirmation to run?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?"
  ]
 },
 {
  "qid": "q166929871c",
  "text": "Does an untrusted source for a value block the action, with a covering delegation absent?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "qb97fbf662c",
  "text": "Which decision does the proposed action get: run, blocked for an untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?"
  ]
 },
 {
  "qid": "qf70863f9d9",
  "text": "Which of the decisions applies to the proposed action: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q00593e1406",
  "text": "Is the action blocked because a value came from an untrusted source and its delegation covers another action?",
  "choices": [
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?"
  ]
 },
 {
  "qid": "q67ccc5e8fb",
  "text": "Does the action end either by running on its own or by waiting for the user's confirmation?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "qee2895f997",
  "text": "Does the agent settle the action alone, by either running it or refusing it?",
  "choices": [
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?"
  ]
 },
 {
  "qid": "qe3017f8066",
  "text": "Does the proposed action pause for the user's confirmation to run?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)"
  ]
 },
 {
  "qid": "q5a6e01e440",
  "text": "Is the agent allowed to run the proposed action on its own, skipping any refusal and any check with the user?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?"
  ]
 },
 {
  "qid": "q6411bfba6a",
  "text": "a production taken from a production may be used directly with no question to the user",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "qe370099981",
  "text": "Does the agent settle the proposed action alone, by either running it or refusing it?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q14fd9832d1",
  "text": "Is the agent allowed to run the proposed action by itself, bypassing any refusal and any check with the user?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)"
  ]
 },
 {
  "qid": "q4bd1b67e01",
  "text": "Does the action end in running on its own, or in waiting for the user's confirmation?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "q75b29017a6",
  "text": "Does the action wait for the user's confirmation to run?",
  "choices": [
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "qf35a8f73e5",
  "text": "Must the agent hold the action back, either by refusing it or by asking the user for approval?",
  "choices": [
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?"
  ]
 },
 {
  "qid": "q0b1619edc3",
  "text": "Which outcome does the proposed action get: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "qe0941425fd",
  "text": "Is it true that the agent can't run the action on its own?",
  "choices": [
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q8a91e89f5a",
  "text": "Is it true that the action is not blocked for the origin of a value?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?"
  ]
 },
 {
  "qid": "q484012022d",
  "text": "Is it true that the agent is not able to run the action on its own?",
  "choices": [
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "qa30df0ff5d",
  "text": "Is it not true that the agent cannot run the action on its own?",
  "choices": [
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?"
  ]
 },
 {
  "qid": "q155053fd19",
  "text": "a production that comes from a production may be used directly, with no question put to the user",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used by the agent directly, with no question to the user"
  ]
 },
 {
  "qid": "q9d82617815",
  "text": "Is the outcome either a run on its own or a wait for the user's confirmation?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?"
  ]
 },
 {
  "qid": "qbb73679e25",
  "text": "Before it runs, must the action await the user's confirmation?",
  "choices": [
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?"
  ]
 },
 {
  "qid": "qd7e5b791b2",
  "text": "Does the action's outcome lie in either running on its own or waiting for the user's confirmation?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q1574175f61",
  "text": "a production coming from a production is usable only when the user confirms it first",
  "choices": [
   "a value of the named kind that comes from the named kind of tool result may be used only after the user confirms it"
  ]
 },
 {
  "qid": "qae5800beb4",
  "text": "Does the action pause for the user's confirmation to run?",
  "choices": [
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?"
  ]
 },
 {
  "qid": "q9acf5ec923",
  "text": "Is the action blocked because the origin of a value is untrusted and its delegation covers another action?",
  "choices": [
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?"
  ]
 },
 {
  "qid": "q2c2d905eb8",
  "text": "Before it runs, does the action wait for the user's confirmation?",
  "choices": [
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?"
  ]
 },
 {
  "qid": "q8c9b0f3a01",
  "text": "Which decision does the proposed action get: run, blocked for untrusted origin, ask the user, or run despite harmless trigger words?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)"
  ]
 },
 {
  "qid": "q151061432b",
  "text": "Does the agent decide the action by itself, either by running it or by refusing it?",
  "choices": [
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?"
  ]
 },
 {
  "qid": "qb81c160e61",
  "text": "Must the agent hold the action back, either by refusing it or by checking with the user?",
  "choices": [
   "yes/no, negated: is it true that the agent can NOT run the action on its own?",
   "asks which of the four decisions the proposed action gets (run, blocked for untrusted origin, ask the user, run despite harmless trigger words)",
   "yes/no: does the action end in one of the two other outcomes, running on its own or waiting for the user's confirmation (both named)?",
   "yes/no: must the agent hold the action back, either refusing it or checking with the user (a positive word)?",
   "yes/no, no negation: does the action wait for the user's confirmation before it runs?",
   "yes/no, negated: is it true that the action is NOT one that waits for the user's confirmation?",
   "yes/no: does the agent settle the action alone, either running it or refusing it (both named)?",
   "yes/no, negated: is it true that the action is NOT blocked for the origin of a value?",
   "yes/no, no negation: may the agent run the proposed action on its own, with no refusal and no check with the user?",
   "yes/no, double negation: is it NOT true that the agent can NOT run the action on its own?",
   "yes/no, no negation: is the action blocked because a value came from an untrusted source with no covering delegation?"
  ]
 }
]
