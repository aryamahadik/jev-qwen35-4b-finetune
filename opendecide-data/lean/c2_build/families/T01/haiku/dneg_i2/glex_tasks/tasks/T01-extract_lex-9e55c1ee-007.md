# T01 extraction task T01-extract_lex-9e55c1ee-007

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/haiku/dneg_i2/glex_tasks/answers/T01-extract_lex-9e55c1ee-007.json

Task kind: extract_lex; read: glex-i2-r2; items: 2; outputs expected: 2.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a double quote as \" and a line break as \n.

TASK: READ EACH TEXT ALONE and pick the ONE CHOICE whose meaning the text expresses. Each item gives a TEXT (a short
question, a rule clause or a comparison phrase, with its values already filled in) and CHOICES (a list of meanings).

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
  "qid": "qe49ec8da1b",
  "text": "Going by the record, is it not true that the purchase request made by Brightwell Supply does not require written quotes?",
  "choices": [
   "asks for the due date of the response under the response rule",
   "asks for the last date on which the filing is still in time",
   "asks whether no cash report is required for the day",
   "asks whether the response counts as received on time, put as a double negation",
   "asks for the first date on which a loss would be covered",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether a cash report is required for the day, put as a double negation",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks whether the loss is covered",
   "asks whether the loss happened during the waiting period",
   "asks whether the response counts as received on time",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the purchase request needs written quotes",
   "asks whether the filing was not made in time",
   "asks whether the purchase request does not need written quotes",
   "asks whether the loss is covered, put as a double negation (not not covered)",
   "asks how many days present fall inside the checked period",
   "asks whether the response counts as received late, after the due date",
   "asks whether the response was not on time",
   "asks which of the day's totals call for a cash report",
   "asks on which date the office counts the response as received",
   "asks whether the person is over the stay limit, put as a double negation (not not over)",
   "asks whether the filing was made late, after the final day",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the loss is not covered",
   "asks whether the filing was made in time, put as a double negation (not not in time)",
   "asks whether the filing was made in time",
   "asks whether the purchase request needs written quotes, put as a double negation",
   "asks whether a cash report is required for the day"
  ]
 },
 {
  "qid": "q93995ac29c",
  "text": "According to the rule card, is it not true that purchase request call_7f3a from Dana Okafor does not call for written quotes?",
  "choices": [
   "asks for the first date on which a loss would be covered",
   "asks whether a cash report is required for the day, put as a double negation",
   "asks whether the person is over the stay limit, put as a double negation (not not over)",
   "asks which of the day's totals call for a cash report",
   "asks whether the person is not over the stay limit in the checked period",
   "asks whether no cash report is required for the day",
   "asks whether the loss is covered",
   "asks whether the purchase request does not need written quotes",
   "asks for the due date of the response under the response rule",
   "asks on which date the office counts the response as received",
   "asks whether the loss happened during the waiting period",
   "asks whether the person failed to file in time, that is, filed after the final day",
   "asks whether the purchase request needs written quotes",
   "asks for the last date on which the filing is still in time",
   "asks whether a cash report is required for the day",
   "asks whether the filing was made in time",
   "asks whether the response counts as received late, after the due date",
   "asks whether the response was not on time",
   "asks whether the person is over the stay limit in the checked period",
   "asks whether the filing was made in time, put as a double negation (not not in time)",
   "asks whether the person is within the stay limit (at most the limit) in the checked period",
   "asks for the total the purchase rule compares with its threshold, new request included",
   "asks whether the purchase request needs written quotes, put as a double negation",
   "asks whether the loss is not covered",
   "asks how many days present fall inside the checked period",
   "asks whether the filing was not made in time",
   "asks whether the rule lets the purchase request go ahead without written quotes",
   "asks whether the rule lets the day close without a cash report",
   "asks whether the response counts as received on time",
   "asks whether the filing was made late, after the final day",
   "asks whether the response counts as received on time, put as a double negation",
   "asks whether the loss is covered, put as a double negation (not not covered)"
  ]
 }
]
