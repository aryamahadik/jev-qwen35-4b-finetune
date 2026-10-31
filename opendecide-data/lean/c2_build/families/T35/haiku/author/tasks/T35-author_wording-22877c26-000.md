# T35 authoring task T35-author_wording-22877c26-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/author/answers/T35-author_wording-22877c26-000.json

Task kind: author_wording; items: 5; outputs expected: 40.

You are writing short pieces of text for a synthetic training dataset about web crawlers and the websites
they visit. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a
value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real
companies, crawlers, products, people, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS. A program shows a website's robots.txt file, a crawler's fetch request (the crawler's
product token, a URL and the path to check) and a card of rules, then asks one question in your wording. Each item
states exactly what the question must mean and how many different wordings to write, all with that meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question of 6-24 words, ending with "?", on one line.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it.
3. Tie the question to the rules shown, with a phrase such as "under these rules", "according to these rules",
   "by these rules", "going by the rules" or "do these rules ..." (a question about a line may say "of the
   robots.txt" instead).
4. The question is about what the rules decide, never about ability, advice, safety, manners, ethics or law: never
   use can, could, able, okay, OK, should, ought, would, safe, polite, fair, ethical, wise, legal, legally or
   technically.
5. Never start with the word "May" (write "Under these rules, may ..." instead), and never write "May" with a capital
   anywhere else.
6. Negation: exactly as the item says. When the item asks for none, use none of these: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, refuse to, decline to, prevent ... from, rule out.
7. No digits, number words or ordinals, dates, time words (now, currently, yet, already, soon, today, still) or hedges
   (maybe, probably, likely, seem, think, believe). No names: a capital letter only on the first word (and in "URL").
8. Call the crawler "the crawler" or "this crawler", or use {UA} exactly once where the item says so; call the URL
   "this URL", "the requested URL" or "the URL". Never quote a path, pattern, line, status, website or organisation.
9. Vary the structure across your wordings (who is the subject: the crawler, the URL, the rules; short and long forms).
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q74d9f0d04e",
  "brief": {
   "meaning": "yes/no: under the rules shown, may the crawler fetch the requested URL? (yes = the rules let the crawler fetch it). No negation of any kind",
   "style": "formal and rule-centred",
   "how_many": 8
  },
  "slots": {
   "UA": "the crawler's product token, a single CamelCase word such as 'MaplewickBot'"
  },
  "rules": [
   "use {UA} exactly once",
   "8 different wordings"
  ]
 },
 {
  "qid": "q12544e7172",
  "brief": {
   "meaning": "yes/no: under the rules shown, may the crawler fetch the requested URL? (yes = the rules let the crawler fetch it). No negation of any kind",
   "style": "crawler-centred",
   "how_many": 8
  },
  "slots": {},
  "rules": [
   "no placeholder: say 'the crawler'",
   "8 different wordings"
  ]
 },
 {
  "qid": "q2f51a3684d",
  "brief": {
   "meaning": "yes/no: under the rules shown, may the crawler fetch the requested URL? (yes = the rules let the crawler fetch it). No negation of any kind",
   "style": "plain conversational",
   "how_many": 8
  },
  "slots": {},
  "rules": [
   "no placeholder: say 'the crawler'",
   "8 different wordings"
  ]
 },
 {
  "qid": "qf0e0361520",
  "brief": {
   "meaning": "yes/no: under the rules shown, may the crawler fetch the requested URL? (yes = the rules let the crawler fetch it). No negation of any kind",
   "style": "short and direct",
   "how_many": 8
  },
  "slots": {},
  "rules": [
   "no placeholder: say 'the crawler'",
   "8 different wordings"
  ]
 },
 {
  "qid": "q31ed0a99cf",
  "brief": {
   "meaning": "yes/no: under the rules shown, may the crawler fetch the requested URL? (yes = the rules let the crawler fetch it). No negation of any kind",
   "style": "URL-centred",
   "how_many": 8
  },
  "slots": {
   "UA": "the crawler's product token, a single CamelCase word such as 'MaplewickBot'"
  },
  "rules": [
   "use {UA} exactly once",
   "8 different wordings"
  ]
 }
]
