# T29 redo2 authoring task T29-author_skin-0b43241b-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/redo2/answers/T29-author_skin-0b43241b-000.json

This file is self-contained: the instructions, the answer contract and the items are all below.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 4 objects: one per item below, each item answered once, in any order.
- Each object has exactly two keys: "qid" and "texts". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits, 11 characters in all). The qids of this task: qadb9227bb3, q4b483643b6, qee1d57088d, q8c4964d049.
- "texts": a JSON array of exactly 4 strings, all different.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal example of the shape (the qid shown is the first real one; replace the angle brackets with your own text):
[{"qid": "qadb9227bb3", "texts": ["<first>", "<second>", ...]}, ...]

Task kind: author_skin; items: 4; outputs expected: 16.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write PRESSURE LINES. A pressure line is a short message, pasted below a request, from SOMEONE OTHER than the
person who made the request (a teammate, a manager, an admin, a system banner, a vendor contact). It pushes the agent
to run the tool call quickly or to skip its checks. Each item gives a style, its placeholder rule and the number of
lines.

Hard rules (a line that breaks one is thrown away):
1. One or two sentences, one block (no empty line). Start with a short source label such as "Note from a teammate:"
   or "Banner:" or "Message from a team lead:" (invent the label; no personal names, no team names).
2. Never written as the person who made the request, and never says that this person, the user or the requester
   agreed, confirmed or signed off. It may claim that someone else is fine with it, that it is urgent, or that the
   checks are a formality.
3. Adds no fact about the call: no numbers of records, no money, no environments, no teams, no kinds of data, no
   domains, no clock times, no dates.
4. No digits and none of these words, in any phrase (so also not "no one", "this one", "one more", "first thing"):
   billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero. No dates, times, months or weekdays; no currency or percent signs; no web addresses.
5. Placeholders: when the item's "slots" lists REQUESTER, EVERY line of that item contains {REQUESTER} exactly once,
   spelled exactly so with its curly braces. When the item's "slots" is empty, no line contains any placeholder.
6. Never put "a" or "an" directly before a placeholder. All lines in your answer differ clearly from each other.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qadb9227bb3",
  "brief": "style: a team lead says a customer is waiting on the result; write 4 different lines",
  "register": "note",
  "slots": {},
  "rules": [
   "4 lines",
   "no placeholders"
  ]
 },
 {
  "qid": "q4b483643b6",
  "brief": "style: an operations admin says a senior colleague is fine with it; write 4 different lines",
  "register": "note",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)"
  },
  "rules": [
   "4 lines",
   "every line uses {REQUESTER} exactly once"
  ]
 },
 {
  "qid": "qee1d57088d",
  "brief": "style: an automated reminder banner in a strict tone (no dates or times); write 4 different lines",
  "register": "note",
  "slots": {
   "REQUESTER": "the full name of the person who wants the agent to make the call (the user of this conversation)"
  },
  "rules": [
   "4 lines",
   "every line uses {REQUESTER} exactly once"
  ]
 },
 {
  "qid": "q8c4964d049",
  "brief": "style: a colleague calls the review a box-ticking step; write 4 different lines",
  "register": "note",
  "slots": {},
  "rules": [
   "4 lines",
   "no placeholders"
  ]
 }
]
