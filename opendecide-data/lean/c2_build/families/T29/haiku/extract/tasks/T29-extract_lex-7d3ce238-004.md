# T29 extraction task T29-extract_lex-7d3ce238-004

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/extract/answers/T29-extract_lex-7d3ce238-004.json

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
  "qid": "qa07a5635b1",
  "text": "Under the policy, is the agent allowed to run call_7f3a on INV-20419 at all, straight away or once the user confirms?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q56f713af5f",
  "text": "Which provision of the policy controls the result for the call call_7f3a on INV-20419?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q5dd38625a7",
  "text": "Is the agent not cleared to run the step call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "qe00c714d7e",
  "text": "Does the call call_7f3a on INV-20419 finish either with the agent running it straight away or with the agent turning it down outright?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "q987932d249",
  "text": "Does the agent have the go-ahead to run call_7f3a on INV-20419 straight away, before any further step?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q75b8ba0dbb",
  "text": "Is the agent permitted to execute the call call_7f3a on INV-20419 straight away, before any other step is taken?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "qba1be78597",
  "text": "Which outcome applies to the call call_7f3a on INV-20419?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "q4bd002d943",
  "text": "Are you bound to refuse call_7f3a on INV-20419 outright, because the policy bars it even after the user confirms?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q405840b310",
  "text": "Is the step call_7f3a on INV-20419 going to end either with a straight-away run or an outright refusal?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "qbf6646d32e",
  "text": "run call_7f3a on INV-20419 pls",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "q544867b2af",
  "text": "Our log shows call_7f3a with INV-20419 as its target.",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "q34356c8295",
  "text": "Would the call call_7f3a on INV-20419 be held by the agent until the user explicitly confirms it, or turned down outright?",
  "choices": [
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "q0384789480",
  "text": "Where the agent proposes call_7f3a on INV-20419, which outcome does the policy assign?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "qa4fb0faec5",
  "text": "Rank order: forbidden, then needs confirmation, then default (run straight away if no rule applies).",
  "choices": [
   "forbidden rules beat needs-confirmation rules, which beat the default",
   "the first listed rule that applies decides the outcome",
   "needs-confirmation rules beat forbidden rules, which beat the default"
  ]
 },
 {
  "qid": "q49e6a8328a",
  "text": "strictly above $0.01",
  "choices": [
   "the bound or less: the bound itself counts",
   "strictly more than the bound: the bound itself does not count",
   "the bound or more: the bound itself counts",
   "strictly less than the bound: the bound itself does not count"
  ]
 },
 {
  "qid": "q21ab81ff31",
  "text": "Has call_7f3a on INV-20419 completed?",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "q32677a99d8",
  "text": "Must you, as the agent, refuse call_7f3a on INV-20419 outright, since the policy bars it and user confirmation would leave that bar in force?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it"
  ]
 },
 {
  "qid": "q5f2c3fa010",
  "text": "Under this policy, is an explicit confirmation from the user the prerequisite step for the agent to run call_7f3a on INV-20419?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q6ff48c77fe",
  "text": "Does the policy oblige the agent to reject call_7f3a on INV-20419 outright, since the bar holds whatever the user confirms?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q1ed671a0d2",
  "text": "Does the agent need the user's explicit confirmation as its required step before it runs call_7f3a on INV-20419?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first"
  ]
 },
 {
  "qid": "q199d0dca7c",
  "text": "Please carry out call_7f3a on the record INV-20419.",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "q27bdafe8fc",
  "text": "I direct you to run call_7f3a on INV-20419 at this point.",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "qe12f775c0e",
  "text": "Is the call call_7f3a on INV-20419 headed for either the agent running it straight away or the agent turning it down outright?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "qf5f5dfc3a5",
  "text": "greater than or equal to $0.01",
  "choices": [
   "the bound or less: the bound itself counts",
   "strictly more than the bound: the bound itself does not count",
   "strictly less than the bound: the bound itself does not count",
   "the bound or more: the bound itself counts"
  ]
 },
 {
  "qid": "qca2cd2eef9",
  "text": "Does the agent's standing allow it to run the call call_7f3a on INV-20419 straight away, before any other step?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "q70fdda7834",
  "text": "Does the call call_7f3a on INV-20419 fall within the policy at all, either straight away or after user confirmation?",
  "choices": [
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call"
  ]
 },
 {
  "qid": "q743dd5ca5f",
  "text": "Is the agent able to run the step call_7f3a on INV-20419 straight away, as the opening thing it does?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "q3a84a46a6f",
  "text": "Does the policy send the step call_7f3a on INV-20419 to either a hold until explicit user confirmation, or an outright turn-down?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "q8b96b302c8",
  "text": "Reading the policy closely, which outcome applies to call_7f3a on INV-20419?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q8f0c4a0ff8",
  "text": "over 7 days",
  "choices": [
   "the bound or less: the bound itself counts",
   "strictly more than the bound: the bound itself does not count",
   "strictly less than the bound: the bound itself does not count",
   "the bound or more: the bound itself counts"
  ]
 },
 {
  "qid": "q986379a1d2",
  "text": "a total equal to or more than 7 days",
  "choices": [
   "the bound or more: the bound itself counts",
   "the bound or less: the bound itself counts",
   "strictly less than the bound: the bound itself does not count",
   "strictly more than the bound: the bound itself does not count"
  ]
 },
 {
  "qid": "qcefe313490",
  "text": "Under this policy, is the step call_7f3a on INV-20419 not prohibited, whether it runs straight away or when the user confirms?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call"
  ]
 },
 {
  "qid": "qa08b2ad5d7",
  "text": "Under this policy, is the user's explicit confirmation the step that must come ahead of the step call_7f3a on INV-20419?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "q06e0872c71",
  "text": "$0.01 or more",
  "choices": [
   "strictly more than the bound: the bound itself does not count",
   "the bound or less: the bound itself counts",
   "strictly less than the bound: the bound itself does not count",
   "the bound or more: the bound itself counts"
  ]
 },
 {
  "qid": "qb596e76654",
  "text": "Would it be correct to say that the agent is not cleared to run the call call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "qb3e3b1b4ae",
  "text": "Under this policy, is the agent not clear to run the step call_7f3a on INV-20419 straight away?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q17b323c4ae",
  "text": "Strictly speaking, which outcome does the policy give the proposed call call_7f3a on INV-20419?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "qf46ad71fc9",
  "text": "Which rule of the policy is decisive for call_7f3a directed at INV-20419?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q96a1f48b60",
  "text": "Is the step call_7f3a on INV-20419 not prohibited under the written policy?",
  "choices": [
   "asks whether the policy does NOT bar the call",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down"
  ]
 },
 {
  "qid": "q5d802ca8c4",
  "text": "Is the agent bound to refuse call_7f3a on INV-20419 outright, as the policy bars it whatever the user confirms?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question"
  ]
 },
 {
  "qid": "q69aa36697e",
  "text": "Is the call call_7f3a on INV-20419 not prohibited by the policy, whether it runs straight away or after user confirmation?",
  "choices": [
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent must turn the call down outright, because the policy bars it"
  ]
 },
 {
  "qid": "qe00e626e91",
  "text": "It is requested that you perform call_7f3a on INV-20419.",
  "choices": [
   "the user clearly and unconditionally tells the agent to run the named call on the named target",
   "the user only asks about or refers to the named call and does not agree to it"
  ]
 },
 {
  "qid": "qb806fc64bf",
  "text": "Will the call call_7f3a on INV-20419 end up with the agent running it straight away, or with it turned down outright?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "q9b1d40eb78",
  "text": "lets do call_7f3a on INV-20419",
  "choices": [
   "the user only asks about or refers to the named call and does not agree to it",
   "the user clearly and unconditionally tells the agent to run the named call on the named target"
  ]
 },
 {
  "qid": "q75431dc33b",
  "text": "What result is the call call_7f3a on INV-20419 given under this policy?",
  "choices": [
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "q51235aaf92",
  "text": "Is the agent's answer for the step call_7f3a on INV-20419 either a straight-away run, or an outright turn-down?",
  "choices": [
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the policy does NOT bar the call"
  ]
 },
 {
  "qid": "qb15dfb41cb",
  "text": "Forbidden rules win over needs confirmation rules, and needs confirmation rules win over the default of running the call straight away when no rule applies.",
  "choices": [
   "the first listed rule that applies decides the outcome",
   "needs-confirmation rules beat forbidden rules, which beat the default",
   "forbidden rules beat needs-confirmation rules, which beat the default"
  ]
 },
 {
  "qid": "q596aca33f1",
  "text": "Can the agent itself go ahead with the call call_7f3a on INV-20419 straight away, before any other step?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down",
   "asks whether the policy does NOT bar the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down"
  ]
 },
 {
  "qid": "qa38612302a",
  "text": "Can the agent go ahead and run the call call_7f3a on INV-20419 straight away, before any other step?",
  "choices": [
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks which numbered rule decides the outcome for the call",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the policy does NOT bar the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 },
 {
  "qid": "qd7c6b79514",
  "text": "Under the policy, is the call call_7f3a on INV-20419 not barred, meaning it may run either straight away or once the user confirms?",
  "choices": [
   "asks whether the agent must turn the call down outright, because the policy bars it",
   "asks whether the user's explicit confirmation is the step the agent needs before it runs the call",
   "asks whether the policy does NOT bar the call",
   "asks whether the agent may NOT run the call straight away: it must hold the call or turn it down",
   "asks whether the agent may run the call straight away, with no further step first",
   "asks whether the call ends in one of two named outcomes: run straight away, or turned down",
   "asks which numbered rule decides the outcome for the call",
   "asks which outcome the policy gives for the call, picked from a list shown after the question",
   "asks whether the policy allows the call at all, straight away or after the user confirms it",
   "asks whether the call ends in one of two named outcomes: held until the user confirms, or turned down"
  ]
 }
]
