# T35 authoring task T35-author_skin-29d5b7ab-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/author/answers/T35-author_skin-29d5b7ab-000.json

Task kind: author_skin; items: 8; outputs expected: 48.

You are writing short pieces of text for a synthetic training dataset about web crawlers and the websites
they visit. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a
value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real
companies, crawlers, products, people, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write PRESSURE LINES. A program shows a website's crawl file, a crawler's request and the rules that decide it.
Below the request, a person has pasted one extra line that tries to sway the reader. Each item gives the person's role
and the direction of the push; write the number of different lines it asks for.

Hard rules (a line that breaks one is thrown away):
1. One sentence or two short ones, at most 35 words, on one line. Use {SITE} and {OPERATOR} each
   exactly once, spelled exactly so; no other placeholder.
2. The line is a person's claim or plea, nothing more: it never quotes, adds, edits or cancels any line of the crawl
   file, the request, a fetch status or a rule, never names a page, path, section, address, slash or status code, and
   never mentions robots files.
3. It never talks to the reader or to a computer program: no "ignore", "instructions", "answer", "question", "prompt",
   "assistant", "model", "system" or "you must".
4. No digits, number words, dates, times, months or weekdays, currency or percent signs; never put "a" or "an"
   directly before a placeholder.
5. No real company, product, person or place; names come only through the placeholders.
6. Vary the wording and the reasons given.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q17c5d47a06",
  "brief": "a comment from a partner organisation; the line asks the crawler to stay away from the whole website, citing a worry, a request from the website's staff or a person's say-so; write 6 different lines",
  "register": "note",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'"
  },
  "rules": [
   "write 6 different lines",
   "use {SITE} and {OPERATOR} each exactly once"
  ]
 },
 {
  "qid": "qce4de875e1",
  "brief": "a message from the operator's sales team; the line presses the crawler to go ahead and collect every page of the website anyway, citing a deal, a favour, an old agreement or a person's say-so; write 6 different lines",
  "register": "note",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'"
  },
  "rules": [
   "write 6 different lines",
   "use {SITE} and {OPERATOR} each exactly once"
  ]
 },
 {
  "qid": "qc210ebc427",
  "brief": "a reply forwarded from the website's owners; the line presses the crawler to go ahead and collect every page of the website anyway, citing a deal, a favour, an old agreement or a person's say-so; write 6 different lines",
  "register": "note",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'"
  },
  "rules": [
   "write 6 different lines",
   "use {SITE} and {OPERATOR} each exactly once"
  ]
 },
 {
  "qid": "q0e29079ab6",
  "brief": "a comment from a partner organisation; the line presses the crawler to go ahead and collect every page of the website anyway, citing a deal, a favour, an old agreement or a person's say-so; write 6 different lines",
  "register": "note",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'"
  },
  "rules": [
   "write 6 different lines",
   "use {SITE} and {OPERATOR} each exactly once"
  ]
 },
 {
  "qid": "q6ddb7e685a",
  "brief": "a reply forwarded from the website's owners; the line asks the crawler to stay away from the whole website, citing a worry, a request from the website's staff or a person's say-so; write 6 different lines",
  "register": "note",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'"
  },
  "rules": [
   "write 6 different lines",
   "use {SITE} and {OPERATOR} each exactly once"
  ]
 },
 {
  "qid": "q26400dd1b2",
  "brief": "a note pasted under the request by the website's staff; the line asks the crawler to stay away from the whole website, citing a worry, a request from the website's staff or a person's say-so; write 6 different lines",
  "register": "note",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'"
  },
  "rules": [
   "write 6 different lines",
   "use {SITE} and {OPERATOR} each exactly once"
  ]
 },
 {
  "qid": "qbc8a331322",
  "brief": "a note pasted under the request by the website's staff; the line presses the crawler to go ahead and collect every page of the website anyway, citing a deal, a favour, an old agreement or a person's say-so; write 6 different lines",
  "register": "note",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'"
  },
  "rules": [
   "write 6 different lines",
   "use {SITE} and {OPERATOR} each exactly once"
  ]
 },
 {
  "qid": "q01d949b1d3",
  "brief": "a message from the operator's sales team; the line asks the crawler to stay away from the whole website, citing a worry, a request from the website's staff or a person's say-so; write 6 different lines",
  "register": "note",
  "slots": {
   "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
   "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'"
  },
  "rules": [
   "write 6 different lines",
   "use {SITE} and {OPERATOR} each exactly once"
  ]
 }
]
