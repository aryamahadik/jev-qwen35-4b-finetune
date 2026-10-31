# T35 authoring task T35-author_pack-24b34ec9-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/author/answers/T35-author_pack-24b34ec9-000.json

Task kind: author_pack; items: 12; outputs expected: 48.

You are writing short pieces of text for a synthetic training dataset about web crawlers and the websites
they visit. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a
value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real
companies, crawlers, products, people, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: invent CRAWLER OPERATORS. Each item gives a kind of organisation that runs a web crawler; invent four
different operators of that kind. Each operator has two fields:
- "operator": the organisation's invented name, 2-3 words, every word starting with a capital letter, letters only
  (for example "Fernhill Labs").
- "token": the product token of its crawler: one word in CamelCase, letters only, 6-16 letters, usually ending in
  Bot, Crawler, Spider, Fetcher, Archiver, Scout or Reader (for example "FernhillBot"). It may echo the operator's
  name.
Rules: no real crawler, search engine, company or product name (nothing like the crawlers of real search engines,
AI companies, social networks or SEO tools); no digits, hyphens or spaces in a token; no negation word in any name;
no token starts with the same five letters as another token in your whole answer; every name and token is distinct.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "operators": [{"operator": "<name>", "token": "<token>"}, ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q344567305e",
  "brief": {
   "organisation_kind": "a small search engine company",
   "how_many": 4
  }
 },
 {
  "qid": "q750f1dee02",
  "brief": {
   "organisation_kind": "a news aggregator",
   "how_many": 4
  }
 },
 {
  "qid": "q8a84eab961",
  "brief": {
   "organisation_kind": "an accessibility auditing firm",
   "how_many": 4
  }
 },
 {
  "qid": "q84fc96d9f6",
  "brief": {
   "organisation_kind": "a service that builds link preview cards for chat apps",
   "how_many": 4
  }
 },
 {
  "qid": "q7e9444069e",
  "brief": {
   "organisation_kind": "a library consortium",
   "how_many": 4
  }
 },
 {
  "qid": "q674c743ae5",
  "brief": {
   "organisation_kind": "a market research agency",
   "how_many": 4
  }
 },
 {
  "qid": "q04c4afa11d",
  "brief": {
   "organisation_kind": "a link checking service",
   "how_many": 4
  }
 },
 {
  "qid": "q9f1d98ec90",
  "brief": {
   "organisation_kind": "a small university research lab",
   "how_many": 4
  }
 },
 {
  "qid": "q3fca23cfbf",
  "brief": {
   "organisation_kind": "a nonprofit web archive",
   "how_many": 4
  }
 },
 {
  "qid": "q877fa26c01",
  "brief": {
   "organisation_kind": "a website quality monitoring service",
   "how_many": 4
  }
 },
 {
  "qid": "qd0aa36d7fb",
  "brief": {
   "organisation_kind": "a price comparison start-up",
   "how_many": 4
  }
 },
 {
  "qid": "q6c646a549e",
  "brief": {
   "organisation_kind": "a digital humanities project",
   "how_many": 4
  }
 }
]
