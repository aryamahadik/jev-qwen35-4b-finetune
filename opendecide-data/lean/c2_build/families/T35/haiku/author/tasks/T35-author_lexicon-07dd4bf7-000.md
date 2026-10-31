# T35 authoring task T35-author_lexicon-07dd4bf7-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/author/answers/T35-author_lexicon-07dd4bf7-000.json

Task kind: author_lexicon; items: 6; outputs expected: 36.

You are writing short pieces of text for a synthetic training dataset about web crawlers and the websites
they visit. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a
value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real
companies, crawlers, products, people, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write RULE SENTENCES. A card of rules for reading a robots.txt file has two numbered lines that a program fills
with one of your sentences. Each item states exactly what the sentence must mean and how many different sentences to
write, all with that meaning.

Hard rules (a sentence that breaks one is thrown away):
1. One sentence of 6-26 words, starting with a capital letter and ending with a full stop; no placeholder, no curly
   braces, no digits, no line break.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it.
3. Never use the words first, last, order, listed, earliest, priority, specific, literal, always or any number word
   other than "one".
4. Vary the structure across your sentences.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "forms": ["<sentence 1>", "<sentence 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qe490cfa5bc",
  "brief": {
   "style": "compact",
   "how_many": 6,
   "frame": "a numbered line of the card: '4. ___'"
  },
  "meaning": "among the matching lines (the lines of the applying groups whose pattern matches the path), the line whose pattern is longest decides the request; length is the number of characters in the pattern exactly as written, and each \"*\" and each \"$\" counts as one character. The sentence must name this measure: use the word 'character' or 'characters' and write both \"*\" and \"$\" with their double quotes",
  "slots": {},
  "rules": [
   "6 different sentences",
   "one sentence each"
  ]
 },
 {
  "qid": "qc609132e58",
  "brief": {
   "style": "plain and complete",
   "how_many": 6,
   "frame": "a numbered line of the card: '4. ___'"
  },
  "meaning": "among the matching lines (the lines of the applying groups whose pattern matches the path), the line whose pattern is longest decides the request; length is the number of characters in the pattern exactly as written, and each \"*\" and each \"$\" counts as one character. The sentence must name this measure: use the word 'character' or 'characters' and write both \"*\" and \"$\" with their double quotes",
  "slots": {},
  "rules": [
   "6 different sentences",
   "one sentence each"
  ]
 },
 {
  "qid": "q7edb3411ea",
  "brief": {
   "style": "plain and complete",
   "how_many": 6,
   "frame": "a numbered line of the card: '5. ___'"
  },
  "meaning": "when the longest matching lines are an Allow line and a Disallow line of equal length, the Allow line wins. The sentence must keep the equal-length condition (say 'equal', 'same length', 'equally long' or 'tie') and name both line types exactly as 'Allow' and 'Disallow', with capitals",
  "slots": {},
  "rules": [
   "6 different sentences",
   "one sentence each"
  ]
 },
 {
  "qid": "q95d3bfe343",
  "brief": {
   "style": "in the voice of a rulebook",
   "how_many": 6,
   "frame": "a numbered line of the card: '4. ___'"
  },
  "meaning": "among the matching lines (the lines of the applying groups whose pattern matches the path), the line whose pattern is longest decides the request; length is the number of characters in the pattern exactly as written, and each \"*\" and each \"$\" counts as one character. The sentence must name this measure: use the word 'character' or 'characters' and write both \"*\" and \"$\" with their double quotes",
  "slots": {},
  "rules": [
   "6 different sentences",
   "one sentence each"
  ]
 },
 {
  "qid": "q255d7d38e2",
  "brief": {
   "style": "compact",
   "how_many": 6,
   "frame": "a numbered line of the card: '5. ___'"
  },
  "meaning": "when the longest matching lines are an Allow line and a Disallow line of equal length, the Allow line wins. The sentence must keep the equal-length condition (say 'equal', 'same length', 'equally long' or 'tie') and name both line types exactly as 'Allow' and 'Disallow', with capitals",
  "slots": {},
  "rules": [
   "6 different sentences",
   "one sentence each"
  ]
 },
 {
  "qid": "q7d3f3771c2",
  "brief": {
   "style": "in the voice of a rulebook",
   "how_many": 6,
   "frame": "a numbered line of the card: '5. ___'"
  },
  "meaning": "when the longest matching lines are an Allow line and a Disallow line of equal length, the Allow line wins. The sentence must keep the equal-length condition (say 'equal', 'same length', 'equally long' or 'tie') and name both line types exactly as 'Allow' and 'Disallow', with capitals",
  "slots": {},
  "rules": [
   "6 different sentences",
   "one sentence each"
  ]
 }
]
