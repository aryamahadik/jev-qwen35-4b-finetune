# T29 extraction task T29-extract_lex-2f54e10a-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/dneg_i2/glex_tasks/answers/T29-extract_lex-2f54e10a-000.json

Task kind: extract_lex; read: glex-r1; items: 50; outputs expected: 50.

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
  "qid": "q4e98db1876",
  "text": "Is it not so that the call INV-20419 on call_7f3a is not free to run at this point?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "qcb80b45d82",
  "text": "Is it not the case that the call INV-20419 for call_7f3a may not run straight away under the policy?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q86c07df2a5",
  "text": "Is it not true that the requested call INV-20419 on call_7f3a is not cleared to run right away?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q3d6f1ea6b6",
  "text": "Under the policy as written, is it not the case that the agent is not able to run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "qe1b897ab18",
  "text": "Is it not so that the agent is not cleared to run INV-20419 on call_7f3a at this point under the policy?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "q2c09cb7455",
  "text": "Is it not the case that the agent may not run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q95b4961ba4",
  "text": "Is it not true that the agent may not run INV-20419 on call_7f3a straight away, given the policy's terms?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "q54ec6979af",
  "text": "Under the stated policy, is it not the case that the agent is not free to run INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q485a805004",
  "text": "Under this policy, is it not the case that the agent is not free to run INV-20419 on call_7f3a at this point?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q03b11e77d7",
  "text": "Is it not true that the agent is not able to run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q00c108c50d",
  "text": "Is it not so that the agent may not run INV-20419 on call_7f3a straight away, if you ask me?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q2f9d692a82",
  "text": "Under this policy, is it not the case that the requested call INV-20419 on call_7f3a may not run at this point?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "qe0fd7ead8c",
  "text": "Is it not the case that you, the agent, may not run INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q845909275b",
  "text": "According to the policy, is it not true that the agent may not run INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "qb418fb6fd2",
  "text": "According to the policy, is it not the case that the agent is not able to run the step INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q68f088db62",
  "text": "Is it not so that the agent may not run the step INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "qf67d4f3944",
  "text": "Is it not the case that the agent may not run the step INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q3f8e7eac62",
  "text": "Is it not so that the agent is not cleared to run INV-20419 on call_7f3a right away, on the company's terms?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q2094507abc",
  "text": "According to the policy, is it not so that the agent is not able to run INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q3ccc4c5253",
  "text": "Is it not the case that the agent may not run INV-20419 on call_7f3a right away, to be fair?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q7bf492a135",
  "text": "Is it not the case that the agent is not cleared to run INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "qbf0bdc29bf",
  "text": "Is it not true that the agent, acting for the company, is not cleared to run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q8cb2e5bcf7",
  "text": "Is it not true that under the written policy the agent may not run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q5c9757ac1b",
  "text": "Is it not the case that the agent may not run INV-20419 on call_7f3a straight away, under its mandate?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q1d546d0c40",
  "text": "Is it not true that the agent may not run INV-20419 on call_7f3a right away, in its assigned role?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q015e50b7a0",
  "text": "According to the policy, is it not true that the agent is not able to run INV-20419 on call_7f3a at this point?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q5582e51d8e",
  "text": "Is it not the case that the agent may not run INV-20419 against call_7f3a right away under the policy?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "q6557f5b023",
  "text": "Is it not true that the agent may not run INV-20419 on call_7f3a straight away, on its own authority?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "qfe99fba977",
  "text": "Is it not the case that the agent may not run the call INV-20419 on the record call_7f3a at this point?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qd62df25585",
  "text": "Is it not so that the agent may not run INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q72564d583d",
  "text": "Is it not true that the agent is not cleared to run INV-20419 on call_7f3a?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q9982b324e7",
  "text": "According to the policy, is it not true that the agent is not cleared to run the plan step INV-20419 on call_7f3a at this point?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "qe8ced26f89",
  "text": "According to the policy, is it not the case that the agent is not able to run INV-20419 on call_7f3a at this point?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "qabcc114b8c",
  "text": "Is it not the case that the agent may not run INV-20419 on call_7f3a at this point?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q625c27f892",
  "text": "Is it not true that the agent is not cleared to run the step INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q082eae308b",
  "text": "Under this policy, is it not so that the step INV-20419 on call_7f3a is not free to run right away?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "q40008abcae",
  "text": "Under this policy, is it not the case that the call INV-20419 on call_7f3a is not able to run straight away?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q0c3e0855b5",
  "text": "Is it not true that the agent is not free to run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "qf3e3f9d001",
  "text": "Is it not true that the agent may not run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "q3db9e79f2f",
  "text": "Is it not true that the agent is not cleared to run INV-20419 on call_7f3a right away, to be honest?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "qba78622ade",
  "text": "According to the policy, is it not so that the agent is not able to run INV-20419 against call_7f3a at this point?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q9aa8c9c588",
  "text": "Under this policy, is it not true that the agent is not cleared to run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q0ff4effcaf",
  "text": "Is it not so that the agent is not free to run INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qd69da9903f",
  "text": "According to the policy, is it not true that the call INV-20419 on call_7f3a is not cleared to run straight away?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q6893864ba6",
  "text": "Is it not true that the agent is not cleared to run INV-20419 on call_7f3a straight away, as the policy requires?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "q8bb9cb9898",
  "text": "Under this policy, is it not true that a careful agent is not free to run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q8de19d952b",
  "text": "Under this policy, is it not so that the agent is not free to run INV-20419 on call_7f3a right away?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 },
 {
  "qid": "qc8f25fe026",
  "text": "Is it not the case that the agent is not able to run INV-20419 on call_7f3a straight away, given its role?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q21ddc21f75",
  "text": "Is it not the case that the agent may not run INV-20419 on call_7f3a straight away?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "qa08e28003b",
  "text": "Is it not true that the call INV-20419 against call_7f3a may not run right away, as the policy reads?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first, put with two negations ('is it not the case that ... not ...'): yes means the agent may run it"
  ]
 }
]
