# T31 authoring task T31-author_pack-ee4efc84-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_pack-ee4efc84-000.json

Task kind: author_pack; items: 8; answers expected: 8 (one per item, each with its qid).

You are writing short pieces of text for a synthetic training dataset about who may decide or act at a given moment: sign-off requests in companies, and software agents (AI assistants working through chains of sub-agents) that carry out tasks. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder. Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file, with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write NAME LISTS: invented full names for people in invented organisations. Each item names a mix of origins.

Hard rules: exactly the number of names the item asks for; each name is a given name plus a family name (two or three
words), letters, spaces and hyphens only; all names distinct; no famous or real public figures; no given name that is
also an everyday English word (Will, May, Grant, Hope, Faith, Joy, Bill, Rich, Summer, Mark ...); no name containing
not, no, none, never or nor as a word.

ANSWER FORMAT: one JSON array with one object per item, in any order: {"qid": "<the item's qid>", "names": ["<name>",
...]}. Nothing else in the file.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qe3dc16c356",
  "brief": "Write 40 names; mix: South Asian and Southern European."
 },
 {
  "qid": "qb0bfe89e11",
  "brief": "Write 40 names; mix: Eastern European and Middle Eastern."
 },
 {
  "qid": "q07a67f8614",
  "brief": "Write 40 names; mix: Southeast Asian and Central European."
 },
 {
  "qid": "q5cf794b75a",
  "brief": "Write 40 names; mix: East African and Iberian."
 },
 {
  "qid": "q7b7bce169b",
  "brief": "Write 40 names; mix: West African and Scandinavian."
 },
 {
  "qid": "q09fcb907cd",
  "brief": "Write 40 names; mix: British, Irish and Caribbean."
 },
 {
  "qid": "q6b943a7328",
  "brief": "Write 40 names; mix: East Asian and Latin American."
 },
 {
  "qid": "qeddf156a02",
  "brief": "Write 40 names; mix: Pacific Islander, Turkish and Dutch."
 }
]

Reminder: write one JSON array to /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T31/haiku/author/answers/T31-author_pack-ee4efc84-000.json and nothing else.
