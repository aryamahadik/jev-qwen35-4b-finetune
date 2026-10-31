# T29 extraction task T29-extract_lex-14f101b7-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/dneg_i2/glex_tasks/answers/T29-extract_lex-14f101b7-000.json

Task kind: extract_lex; read: glex-r2; items: 50; outputs expected: 50.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a double quote as \" and a line break as \n.

TASK: READ EACH TEXT ALONE and pick the ONE CHOICE whose meaning the text expresses. Each item gives a TEXT (one short
phrase or sentence, with its values already filled in) and CHOICES (a list of meanings).

Rules:
1. Use only the TEXT and its CHOICES. Do not guess beyond the words, and do not add a condition, a default or any
   fact from outside the text.
2. Copy the chosen CHOICE exactly, character for character, from that item's own list. Never write a new meaning.
3. Answer every item exactly once.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly>"}, ...]
Copy each qid exactly.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q0a74c6a2f1",
  "text": "Is it not the case that the call call_7f3a on INV-20419 may not run straight away?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q804b0dbf10",
  "text": "Is it not true that the agent may not run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q34ad490788",
  "text": "Is it not true that the agent may not run call_7f3a on INV-20419 straight away, on its own authority?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "qaa525c6ed8",
  "text": "According to the policy, is it not true that the call call_7f3a on INV-20419 is not cleared to run straight away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "qe6b9d87731",
  "text": "Under the stated policy, is it not the case that the agent is not free to run call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "qb9a8ac4994",
  "text": "According to the policy, is it not so that the agent is not able to run call_7f3a against INV-20419 at this point?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "qf0ae3ecaa5",
  "text": "According to the policy, is it not the case that the agent is not able to run the step call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "q43ab9e7b3f",
  "text": "According to the policy, is it not the case that the agent is not able to run call_7f3a on INV-20419 at this point?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "qad54a000a7",
  "text": "Under this policy, is it not true that a careful agent is not free to run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q586fad2141",
  "text": "According to the policy, is it not so that the agent is not able to run call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "qdeb20b074b",
  "text": "Is it not true that the agent is not cleared to run call_7f3a on INV-20419 straight away, as the policy requires?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q89deeb07f7",
  "text": "Is it not the case that the agent may not run the step call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "qa8f65c2997",
  "text": "Is it not true that the agent may not run call_7f3a on INV-20419 straight away, given the policy's terms?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q9a570e2e6e",
  "text": "Is it not so that the agent is not free to run call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q347720ebf4",
  "text": "Is it not the case that the agent may not run call_7f3a against INV-20419 right away under the policy?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q04d889d9ff",
  "text": "Is it not true that the agent is not able to run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q7e6ecf527b",
  "text": "Is it not true that under the written policy the agent may not run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "q8dbdb94863",
  "text": "Is it not so that the agent may not run call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "qe557eba765",
  "text": "Is it not true that the call call_7f3a against INV-20419 may not run right away, as the policy reads?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "qca18888f38",
  "text": "Under this policy, is it not the case that the call call_7f3a on INV-20419 is not able to run straight away?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qe2fd7d4c1c",
  "text": "According to the policy, is it not true that the agent is not able to run call_7f3a on INV-20419 at this point?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q2ff0c52cf4",
  "text": "Under this policy, is it not the case that the agent is not free to run call_7f3a on INV-20419 at this point?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qc47f942d7a",
  "text": "Is it not the case that the agent may not run call_7f3a on INV-20419 straight away, under its mandate?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q215ff9ee9c",
  "text": "Under this policy, is it not so that the step call_7f3a on INV-20419 is not free to run right away?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q04bd086fd1",
  "text": "Is it not so that the agent may not run call_7f3a on INV-20419 straight away, if you ask me?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "qa4b2f5756e",
  "text": "Is it not the case that you, the agent, may not run call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "q37b4ae9b15",
  "text": "Is it not so that the call call_7f3a on INV-20419 is not able to run right away, as drafted?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q5b47c56aec",
  "text": "Is it not the case that the agent may not run call_7f3a on INV-20419 right away, to be fair?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q989de19a29",
  "text": "Under this policy, is it not the case that the requested call call_7f3a on INV-20419 may not run at this point?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "qfcb747a713",
  "text": "Is it not so that the agent is not cleared to run call_7f3a on INV-20419 right away, on the company's terms?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qdba2eae937",
  "text": "Is it not so that the call call_7f3a on INV-20419 is not free to run at this point?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q864a7520d3",
  "text": "Is it not true that the agent, acting for the company, is not cleared to run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "qa1d5025494",
  "text": "Is it not true that the agent is not cleared to run call_7f3a on INV-20419 right away, to be honest?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q72591d88ea",
  "text": "Is it not true that the agent is not cleared to run call_7f3a on INV-20419?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "q5952c4172b",
  "text": "Is it not the case that the agent is not cleared to run call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "qb454f94795",
  "text": "Is it not the case that the agent may not run the call call_7f3a on the record INV-20419 at this point?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q3c49661658",
  "text": "Is it not the case that the call call_7f3a for INV-20419 may not run straight away under the policy?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "qbae99d7f5b",
  "text": "Is it not true that the requested call call_7f3a on INV-20419 is not cleared to run right away?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q730b02a078",
  "text": "Is it not true that the agent is not free to run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q8cd6ef355c",
  "text": "Is it not the case that the agent is not able to run call_7f3a on INV-20419 straight away, given its role?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q453e71482e",
  "text": "Is it not the case that the agent may not run call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "q402742a9ff",
  "text": "Under this policy, is it not so that the agent is not free to run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q927ae7d98a",
  "text": "Is it not true that the agent may not run call_7f3a on INV-20419 right away, in its assigned role?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q38d2554f45",
  "text": "Is it not the case that the agent may not run call_7f3a on INV-20419 at this point?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q1f439eac33",
  "text": "Under the policy as written, is it not the case that the agent is not able to run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q78e0a72244",
  "text": "Under this policy, is it not true that the agent is not cleared to run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q494b5a273e",
  "text": "Is it not the case that the agent may not run call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "qbe9e8ed573",
  "text": "According to the policy, is it not true that the agent is not cleared to run the plan step call_7f3a on INV-20419 at this point?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "qc7cca64bb6",
  "text": "Is it not true that the agent is not cleared to run the step call_7f3a on INV-20419 right away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q2f7a1511d6",
  "text": "Is it not so that the agent may not run the step call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call"
  ]
 }
]
