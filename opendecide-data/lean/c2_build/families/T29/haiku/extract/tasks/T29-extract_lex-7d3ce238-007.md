# T29 extraction task T29-extract_lex-7d3ce238-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/extract/answers/T29-extract_lex-7d3ce238-007.json

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
  "qid": "q56cd7116f4",
  "text": "Is the call call_7f3a on INV-20419 going to finish with the agent running it straight away or turning it down outright?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qdb497ed0fb",
  "text": "call_7f3a on INV-20419, go run it",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "q8d76c73f71",
  "text": "Which of the policy's rules decides the outcome for the call call_7f3a on INV-20419?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q747c68ee1d",
  "text": "Forbidden ranks highest, needs confirmation ranks below it, and the default of running the call straight away when no rule applies ranks lowest.",
  "choices": [
   "forbidden rules beat needs-confirmation rules, which beat the default",
   "the first listed rule that applies decides the outcome",
   "needs-confirmation rules beat forbidden rules, which beat the default"
  ]
 },
 {
  "qid": "qf1f8d1210a",
  "text": "not less than $0.01",
  "choices": [
   "strictly less than the bound: the bound itself does not count",
   "strictly more than the bound: the bound itself does not count",
   "the bound or less: the bound itself counts",
   "the bound or more: the bound itself counts"
  ]
 },
 {
  "qid": "q5751b34690",
  "text": "The forbidden tier is ranked above the needs confirmation tier, which is ranked above the default of running the call straight away when no rule applies.",
  "choices": [
   "forbidden rules beat needs-confirmation rules, which beat the default",
   "the first listed rule that applies decides the outcome",
   "needs-confirmation rules beat forbidden rules, which beat the default"
  ]
 },
 {
  "qid": "q4ddfb735e8",
  "text": "strictly under 7 days",
  "choices": [
   "strictly less than the bound: the bound itself does not count",
   "the bound or more: the bound itself counts",
   "strictly more than the bound: the bound itself does not count",
   "the bound or less: the bound itself counts"
  ]
 },
 {
  "qid": "q92bd67ad10",
  "text": "That is the call_7f3a call that targets INV-20419.",
  "choices": [
   "the user only asks about or refers to the named call and does not agree to it",
   "the user clearly and unconditionally tells the agent to run the named call on the named target"
  ]
 },
 {
  "qid": "qd575be1482",
  "text": "The forbidden tier outweighs the needs confirmation tier, and the needs confirmation tier outweighs the default of running the call straight away when no rule applies.",
  "choices": [
   "needs-confirmation rules beat forbidden rules, which beat the default",
   "forbidden rules beat needs-confirmation rules, which beat the default",
   "the first listed rule that applies decides the outcome"
  ]
 },
 {
  "qid": "q39565b6cdc",
  "text": "Which result does the policy give if someone asks to run call_7f3a on INV-20419?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "qeabed91a0f",
  "text": "yep, run call_7f3a on INV-20419",
  "choices": [
   "the user only asks about or refers to the named call and does not agree to it",
   "the user clearly and unconditionally tells the agent to run the named call on the named target"
  ]
 },
 {
  "qid": "q5f6584b965",
  "text": "Will the agent have to get the user's explicit confirmation as the required step in order to run call_7f3a on INV-20419?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "q707bbb5d6e",
  "text": "strictly less than 7 days",
  "choices": [
   "strictly more than the bound: the bound itself does not count",
   "strictly less than the bound: the bound itself does not count",
   "the bound or less: the bound itself counts",
   "the bound or more: the bound itself counts"
  ]
 },
 {
  "qid": "q83c860b62a",
  "text": "To be precise, what outcome does the written policy assign to call_7f3a on INV-20419?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "qb8b22de7be",
  "text": "Does the agent's standing mean it is not allowed to run the call call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "q4b7a9bb606",
  "text": "Is the call call_7f3a on INV-20419 not barred, meaning it may run straight away or after confirmation?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q8787aa8c16",
  "text": "Which outcome does the policy assign to call_7f3a on INV-20419?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "qf41f83bb00",
  "text": "Is it your job, as the agent, to turn down call_7f3a on INV-20419 outright, since the policy bars it even after confirmation?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q9900d52231",
  "text": "The default of running the call straight away when no rule applies ranks below the needs confirmation tier, and the needs confirmation tier ranks below the forbidden tier.",
  "choices": [
   "needs-confirmation rules beat forbidden rules, which beat the default",
   "the first listed rule that applies decides the outcome",
   "forbidden rules beat needs-confirmation rules, which beat the default"
  ]
 },
 {
  "qid": "qf15049d97b",
  "text": "Would the call call_7f3a on INV-20419 be permitted by the policy at all, straight away or once the user confirms it?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q3ee592463d",
  "text": "Under the policy, does the call call_7f3a on INV-20419 end with the agent holding it until the user explicitly confirms it, or turning it down outright?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "qb94f520ad2",
  "text": "Would call_7f3a on INV-20419 delete the current contents?",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "q34150f496c",
  "text": "According to the policy, may the agent carry out call_7f3a on INV-20419 at all, either straight away or with the user's confirmation?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "q82da5acdfd",
  "text": "Under this policy, must the agent refuse the step call_7f3a on INV-20419 outright, even if the user confirms it?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qd901d6d2d0",
  "text": "What happens to INV-20419 after call_7f3a is called?",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "qb75da97176",
  "text": "Is the step call_7f3a on INV-20419 a case where the agent has to turn it down outright, since the policy bars it even with the user's confirmation?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qfab1baf4c3",
  "text": "What progress has the call_7f3a call on INV-20419 made?",
  "choices": [
   "the user only asks about or refers to the named call and does not agree to it",
   "the user clearly and unconditionally tells the agent to run the named call on the named target"
  ]
 },
 {
  "qid": "q3073121093",
  "text": "Is the agent cleared to run the step call_7f3a on INV-20419 straight away, skipping any step in between?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "qb9168f827e",
  "text": "A rule in the forbidden tier beats a rule in the needs confirmation tier, and a needs confirmation rule beats the default of running the call straight away when no rule applies.",
  "choices": [
   "needs-confirmation rules beat forbidden rules, which beat the default",
   "forbidden rules beat needs-confirmation rules, which beat the default",
   "the first listed rule that applies decides the outcome"
  ]
 },
 {
  "qid": "q5f87475b5a",
  "text": "Forbidden ranks above needs confirmation, which ranks above default (run straight away when no rule applies).",
  "choices": [
   "the first listed rule that applies decides the outcome",
   "needs-confirmation rules beat forbidden rules, which beat the default",
   "forbidden rules beat needs-confirmation rules, which beat the default"
  ]
 },
 {
  "qid": "q1e0153dbb4",
  "text": "Is the result for the call call_7f3a on INV-20419 a hold until the user explicitly confirms it, or an outright turn-down?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q0e5a5794b9",
  "text": "Does the call call_7f3a on INV-20419 come out as the agent running it straight away, or as the agent turning it down outright?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "qe2518848f1",
  "text": "Is the agent allowed to run call_7f3a on INV-20419 straight away, before any further step?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q788394ed01",
  "text": "Must the agent get explicit user confirmation, the required step, before it runs call_7f3a on INV-20419?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "qf1138d3524",
  "text": "Is the call call_7f3a on INV-20419 a request the agent is not allowed to run straight away?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q69f36473e3",
  "text": "Under this policy, which rule ends up deciding the outcome for the call call_7f3a on INV-20419?",
  "choices": [
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q6695f52c3a",
  "text": "Quick check: which policy rule decides the outcome for call_7f3a on INV-20419?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q668650fb46",
  "text": "Does the policy make the user's explicit confirmation the prerequisite step for the agent's run of call_7f3a on INV-20419?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q264456b554",
  "text": "Bottom line, does the call call_7f3a on INV-20419 end up held until the user explicitly confirms it, or turned down outright?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q870baa5ce5",
  "text": "no greater than 7 days",
  "choices": [
   "strictly less than the bound: the bound itself does not count",
   "the bound or more: the bound itself counts",
   "the bound or less: the bound itself counts",
   "strictly more than the bound: the bound itself does not count"
  ]
 },
 {
  "qid": "qc8fc47f168",
  "text": "What outcome should the call call_7f3a on INV-20419 get?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q5148c6c08a",
  "text": "Under this policy, what outcome is stipulated for a call call_7f3a directed at INV-20419?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "qc367d290a5",
  "text": "Has the agent been given the go-ahead to run the call call_7f3a on INV-20419 straight away, before any other step?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q7eb7eeccb3",
  "text": "higher than $0.01",
  "choices": [
   "the bound or more: the bound itself counts",
   "strictly more than the bound: the bound itself does not count",
   "strictly less than the bound: the bound itself does not count",
   "the bound or less: the bound itself counts"
  ]
 },
 {
  "qid": "qf16a0aab18",
  "text": "Under this policy, what outcome applies to the call call_7f3a made against INV-20419?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "qbd30adb672",
  "text": "Under the policy, may the agent proceed with the call call_7f3a on INV-20419 straight away, ahead of every other step?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "qc74f3ad815",
  "text": "Per the governing policy text, what outcome is assigned to the call call_7f3a on INV-20419?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q72adb179c3",
  "text": "Under the policy, is the agent not cleared to run the call call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "qb2b98a3b5e",
  "text": "Would the policy force the agent to turn down the step call_7f3a on INV-20419 outright, even when the user approves it?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "qce6cb8d334",
  "text": "Which fields of INV-20419 would call_7f3a alter?",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 }
]
