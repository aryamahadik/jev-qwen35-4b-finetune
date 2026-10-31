# T29 redo2 authoring task T29-author_wording-fa215601-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/redo2/answers/T29-author_wording-fa215601-000.json

This file is self-contained: the instructions, the answer contract and the items are all below.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 3 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "wordings". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: q278f254c63, q8a48b9181e, qe76720b144.
- "wordings": a JSON array of exactly 8 strings, all different.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one; replace the angle brackets with your own text):
[{"qid": "q278f254c63", "wordings": ["<first>", "<second>", ...]}, ...]

Task kind: author_wording; items: 3; outputs expected: 24.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS. A program shows a policy, a proposed tool call {ACTION} on {TARGET} and a data
snapshot, then asks one yes/no question in your wording. Every item of this task has the same meaning (stated in the
item): the question asks only whether the policy bars the call, with one "not". Write the number of different
wordings each item asks for.

Hard rules (a wording that breaks one is thrown away):
1. One question, 8-30 words, ending with "?". Use {ACTION} and {TARGET} each exactly once, spelled exactly so; no
   other placeholder.
2. Exactly one negation: the word "not", written out (never "n't"), placed after the subject and directly before the
   bar word, as in "is ... not barred", "is ... not prohibited", "is ... not off limits", "is it true that the policy
   does not bar ...". Never open the question with a negative ("Isn't ...",
   "Doesn't ...", "Is it not ...", "Does the policy not ...", "Has the policy not ..."): such questions invite the opposite answer. No other
   negation anywhere: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
3. The question is only about whether the policy bars the call: add nothing about what follows from the answer. Never mention
   running or making the call straight away, right away, at once or later; the user, a confirmation, an approval or
   a sign-off; holding, pausing or waiting; turning the call down or declining it; "at all"; "either ... or";
   "whether ... or". Never use a positive permission word (allowed, acceptable, within the policy, clear to, fine,
   okay): the question is the bar word with its one "not".
4. None of these number words: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero. No digits, dates, month names or clock times. None of these
   time words: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet. Do not use the word "may" anywhere (a program reads "May" as a month). No hedges
   (allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure). No names; a capital letter only on the first word.
5. Never mention rule numbers, thresholds, snapshot fields, an earlier message or answer choices.
6. Vary the structure: the subject can be the call, the agent ("is the agent not barred from running ...") or the
   policy ("is it true that the policy does not bar ..."); openings such as "Under this policy, ...", "According to
   the policy, ...", "Under the written policy, ..."; short and long forms. All wordings in your answer differ clearly
   (not one word swapped).
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q278f254c63",
  "brief": {
   "meaning": "yes/no: is the call {ACTION} on {TARGET} not barred by the policy? A reader answers yes when the policy does not bar the call and no when the policy bars it. Exactly one 'not', written out, directly before the bar word (barred, prohibited or off limits); nothing else about what follows from the answer",
   "style": "formal and policy-centred",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once",
   "exactly one 'not', written out, directly before the bar word",
   "no mention of running straight away, of the user or of a confirmation"
  ]
 },
 {
  "qid": "q8a48b9181e",
  "brief": {
   "meaning": "yes/no: is the call {ACTION} on {TARGET} not barred by the policy? A reader answers yes when the policy does not bar the call and no when the policy bars it. Exactly one 'not', written out, directly before the bar word (barred, prohibited or off limits); nothing else about what follows from the answer",
   "style": "with the agent as the subject",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once",
   "exactly one 'not', written out, directly before the bar word",
   "no mention of running straight away, of the user or of a confirmation"
  ]
 },
 {
  "qid": "qe76720b144",
  "brief": {
   "meaning": "yes/no: is the call {ACTION} on {TARGET} not barred by the policy? A reader answers yes when the policy does not bar the call and no when the policy bars it. Exactly one 'not', written out, directly before the bar word (barred, prohibited or off limits); nothing else about what follows from the answer",
   "style": "short and direct",
   "how_many": 8
  },
  "slots": {
   "ACTION": "the id of the requested tool call, a snake_case name such as 'rename_project_folders'",
   "TARGET": "the id of the record the call acts on, such as 'DOC-48213'"
  },
  "rules": [
   "8 wordings with exactly this meaning",
   "{ACTION} and {TARGET} each exactly once",
   "exactly one 'not', written out, directly before the bar word",
   "no mention of running straight away, of the user or of a confirmation"
  ]
 }
]
