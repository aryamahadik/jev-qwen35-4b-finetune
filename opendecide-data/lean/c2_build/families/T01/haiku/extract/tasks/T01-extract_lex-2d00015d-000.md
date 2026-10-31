# T01 extraction task T01-extract_lex-2d00015d-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/haiku/extract/answers/T01-extract_lex-2d00015d-000.json

Task kind: extract_lex; read: glex-r3; items: 25; outputs expected: 25.

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
  "qid": "q5c380ebd17",
  "text": "a waiting period of 30 days in which counting begins the day after its start date",
  "choices": [
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is the day after its start date",
   "a period counted from the later of two dates",
   "a waiting period whose first day is its start date",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q6d9191fd0b",
  "text": "a waiting period of 30 days that begins on the next day after its start date",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a period counted from the earlier of two dates",
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the later of two dates",
   "a waiting period whose first day is its start date"
  ]
 },
 {
  "qid": "qe9993d2e62",
  "text": "at most 1 day across any 7-day window that slides ahead day by day",
  "choices": [
   "a waiting period whose first day is its start date",
   "a period counted from the earlier of two dates",
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date"
  ]
 },
 {
  "qid": "qa6835a65ec",
  "text": "within 30 days after the later date out of these dates",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q5409210944",
  "text": "up to 1 day in every 7-day run that moves forward through time",
  "choices": [
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a period counted from the earlier of two dates",
   "a cap on the days present in every rolling period of the stated length",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q366c1823fa",
  "text": "a waiting period of 30 days whose opening day is the day after its start date",
  "choices": [
   "a waiting period whose first day is its start date",
   "a period counted from the later of two dates",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a cap on the days present in each calendar year",
   "a waiting period whose first day is the day after its start date"
  ]
 },
 {
  "qid": "q2f83a76349",
  "text": "at most 1 day inside every moving 7-day period",
  "choices": [
   "a waiting period whose first day is its start date",
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date"
  ]
 },
 {
  "qid": "qd873b7d86c",
  "text": "a waiting period of 30 days with the start date itself left out, beginning the day after its start date",
  "choices": [
   "a waiting period whose first day is its start date",
   "a period counted from the later of two dates",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length"
  ]
 },
 {
  "qid": "qa04185ce83",
  "text": "up to 1 day inside any moving 7-day stretch",
  "choices": [
   "a period counted from the later of two dates",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a waiting period whose first day is the day after its start date",
   "a period counted from the earlier of two dates",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q74077cff53",
  "text": "within 30 days starting from the later of the dates listed below",
  "choices": [
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a waiting period whose first day is its start date",
   "a period counted from the later of two dates",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q2291cf9d83",
  "text": "up to 1 day in any 7-day period that rolls forward day by day",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the later of two dates",
   "a waiting period whose first day is its start date",
   "a cap on the days present in each calendar year",
   "a period counted from the earlier of two dates"
  ]
 },
 {
  "qid": "q58f88a1732",
  "text": "within 30 days following the later of these dates",
  "choices": [
   "a cap on the days present in each calendar year",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the later of two dates"
  ]
 },
 {
  "qid": "q092b17710b",
  "text": "a maximum of 1 day during any 7-day window that moves ahead",
  "choices": [
   "a waiting period whose first day is its start date",
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date"
  ]
 },
 {
  "qid": "q15e448c3c5",
  "text": "a waiting period of 30 days that opens on the day after its start date",
  "choices": [
   "a waiting period whose first day is its start date",
   "a period counted from the earlier of two dates",
   "a cap on the days present in every rolling period of the stated length",
   "a cap on the days present in each calendar year",
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date"
  ]
 },
 {
  "qid": "q9167451d05",
  "text": "a waiting period of 30 days starting with the day after its start date",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a period counted from the later of two dates",
   "a cap on the days present in each calendar year",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates"
  ]
 },
 {
  "qid": "qd4385030e4",
  "text": "within 30 days from whichever is later of these dates",
  "choices": [
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a period counted from the later of two dates",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q0e8c26dafc",
  "text": "inside 30 days beginning at the later of these dates",
  "choices": [
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in each calendar year",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length"
  ]
 },
 {
  "qid": "qcaadc7b79e",
  "text": "a waiting period of 30 days that runs from the day after its start date",
  "choices": [
   "a cap on the days present in each calendar year",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date"
  ]
 },
 {
  "qid": "q830d5895ca",
  "text": "at most 1 day in any rolling 7-day window",
  "choices": [
   "a cap on the days present in each calendar year",
   "a period counted from the later of two dates",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is its start date",
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in every rolling period of the stated length"
  ]
 },
 {
  "qid": "qb5453e79af",
  "text": "up to 1 day in any 7-day window that keeps sliding forward",
  "choices": [
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is its start date"
  ]
 },
 {
  "qid": "q78a8179991",
  "text": "a waiting period of 30 days that picks up on the day after its start date",
  "choices": [
   "a cap on the days present in every rolling period of the stated length",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a cap on the days present in each calendar year",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates"
  ]
 },
 {
  "qid": "q895015406c",
  "text": "within 30 days reckoned after the later of these dates",
  "choices": [
   "a cap on the days present in every rolling period of the stated length",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q64a48f908a",
  "text": "at most 1 day inside every 7-day stretch that moves along",
  "choices": [
   "a cap on the days present in each calendar year",
   "a period counted from the later of two dates",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is its start date",
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in every rolling period of the stated length"
  ]
 },
 {
  "qid": "q49075e9667",
  "text": "within 30 days measured from the later of the dates below",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a cap on the days present in each calendar year",
   "a waiting period whose first day is its start date",
   "a period counted from the later of two dates"
  ]
 },
 {
  "qid": "q81b1894944",
  "text": "a maximum of 1 day in any 7-day span that moves ahead with each new day",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a period counted from the earlier of two dates",
   "a cap on the days present in every rolling period of the stated length",
   "a waiting period whose first day is its start date",
   "a period counted from the later of two dates",
   "a cap on the days present in each calendar year"
  ]
 }
]
