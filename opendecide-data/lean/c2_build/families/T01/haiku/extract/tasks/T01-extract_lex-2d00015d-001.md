# T01 extraction task T01-extract_lex-2d00015d-001

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T01/haiku/extract/answers/T01-extract_lex-2d00015d-001.json

Task kind: extract_lex; read: glex-r3; items: 10; outputs expected: 10.

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
  "qid": "q04269fdb24",
  "text": "within 30 days running from the later of the dates below",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the later of two dates",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q87bacaddf8",
  "text": "a waiting period of 30 days that begins on the day after its start date",
  "choices": [
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is the day after its start date",
   "a period counted from the later of two dates",
   "a waiting period whose first day is its start date"
  ]
 },
 {
  "qid": "q06bec6c76c",
  "text": "within 30 days counted forward from the later among these dates",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a period counted from the later of two dates",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is its start date",
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length"
  ]
 },
 {
  "qid": "q1a95b1684c",
  "text": "a waiting period of 30 days whose earliest counted day is the day after its start date",
  "choices": [
   "a cap on the days present in each calendar year",
   "a period counted from the later of two dates",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date"
  ]
 },
 {
  "qid": "qb7d7eeea0c",
  "text": "a waiting period of 30 days counted from the day after its start date",
  "choices": [
   "a cap on the days present in every rolling period of the stated length",
   "a cap on the days present in each calendar year",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date"
  ]
 },
 {
  "qid": "q6bc9a6df83",
  "text": "inside 30 days counted from the later of these dates",
  "choices": [
   "a period counted from the earlier of two dates",
   "a cap on the days present in each calendar year",
   "a period counted from the later of two dates",
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length"
  ]
 },
 {
  "qid": "qa5f3632b92",
  "text": "a maximum of 1 day in each 7-day window that rolls forward",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a period counted from the later of two dates",
   "a period counted from the earlier of two dates",
   "a cap on the days present in each calendar year"
  ]
 },
 {
  "qid": "q07777e1cf0",
  "text": "at most 1 day in each 7-day window that moves forward",
  "choices": [
   "a waiting period whose first day is the day after its start date",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a cap on the days present in each calendar year",
   "a period counted from the earlier of two dates",
   "a period counted from the later of two dates"
  ]
 },
 {
  "qid": "q964fb98665",
  "text": "a maximum of 1 day within every moving 7-day stretch",
  "choices": [
   "a cap on the days present in each calendar year",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is its start date",
   "a cap on the days present in every rolling period of the stated length",
   "a waiting period whose first day is the day after its start date",
   "a period counted from the later of two dates"
  ]
 },
 {
  "qid": "q484a9600bc",
  "text": "a maximum of 1 day within any 7-day window that keeps moving",
  "choices": [
   "a period counted from the later of two dates",
   "a cap on the days present in each calendar year",
   "a cap on the days present in every rolling period of the stated length",
   "a waiting period whose first day is the day after its start date",
   "a period counted from the earlier of two dates",
   "a waiting period whose first day is its start date"
  ]
 }
]
