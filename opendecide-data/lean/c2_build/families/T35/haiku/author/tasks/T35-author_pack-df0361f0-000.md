# T35 authoring task T35-author_pack-df0361f0-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T35/haiku/author/answers/T35-author_pack-df0361f0-000.json

Task kind: author_pack; items: 40; outputs expected: 40.

You are writing short pieces of text for a synthetic training dataset about web crawlers and the websites
they visit. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a
value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real
companies, crawlers, products, people, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: invent one SITE PACK per item. A site pack is a small set of invented values for one kind of website. Each
item gives the kind of website; fit every value to it.

Fields of "pack" (all invented; no real brand, company, product, person or place):
- "site_kind": the item's kind of website, copied.
- "site_names": exactly three different invented names for such a website, each 2-4 words, every word starting with a
  capital letter and made of letters only (no digits, no hyphens, no apostrophes, no "and" or "&"), for example
  "Copperbeech Growers". No word that is a negation (such as "Never", "Nobody", "Nothing").
- "sections": exactly eight different names of sections such a website has, each one or two lowercase English
  words made of letters only (for example "opening times" or "members"). Include a mix: public parts (such as a
  catalogue, news or events) and parts meant for staff, members or customers (such as an account, drafts or admin).
- "pages": exactly four different names of single pages or files such a website has, each one or two lowercase
  English words, letters only (for example "price list" or "photo"). No file endings: a program adds them.
No value repeats one from another item of this task. A program turns the sections and pages into web addresses;
you never write an address, a slash or a file ending.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "pack": {...the fields listed below...}}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q975d963af8",
  "brief": {
   "site_kind": "a farmers' market"
  }
 },
 {
  "qid": "q9647dc0e52",
  "brief": {
   "site_kind": "a city zoo"
  }
 },
 {
  "qid": "q6d85155e0d",
  "brief": {
   "site_kind": "a tea shop"
  }
 },
 {
  "qid": "q3a31e383fe",
  "brief": {
   "site_kind": "an aquarium store"
  }
 },
 {
  "qid": "qa0cbc4b592",
  "brief": {
   "site_kind": "a hiking club"
  }
 },
 {
  "qid": "qc657764faa",
  "brief": {
   "site_kind": "a community choir"
  }
 },
 {
  "qid": "q6ffed1ab4d",
  "brief": {
   "site_kind": "a gardening forum"
  }
 },
 {
  "qid": "q53684e74fe",
  "brief": {
   "site_kind": "a neighbourhood bakery"
  }
 },
 {
  "qid": "q261dabeda1",
  "brief": {
   "site_kind": "a botanical garden"
  }
 },
 {
  "qid": "q11d9b57af0",
  "brief": {
   "site_kind": "a local history society"
  }
 },
 {
  "qid": "q5e9cbede83",
  "brief": {
   "site_kind": "a recipe sharing community"
  }
 },
 {
  "qid": "qdf2c80e053",
  "brief": {
   "site_kind": "a model railway club"
  }
 },
 {
  "qid": "q00416e9bc8",
  "brief": {
   "site_kind": "a poster print shop"
  }
 },
 {
  "qid": "q09f22455f0",
  "brief": {
   "site_kind": "a wildlife rescue centre"
  }
 },
 {
  "qid": "qce5ef0917f",
  "brief": {
   "site_kind": "a tutoring service"
  }
 },
 {
  "qid": "q6b1a818da8",
  "brief": {
   "site_kind": "a board game cafe"
  }
 },
 {
  "qid": "q31fa55466b",
  "brief": {
   "site_kind": "a pottery supply store"
  }
 },
 {
  "qid": "qc4e1d48c2c",
  "brief": {
   "site_kind": "a used musical instrument shop"
  }
 },
 {
  "qid": "qc3ac9e70b1",
  "brief": {
   "site_kind": "a weather hobbyist blog"
  }
 },
 {
  "qid": "q27466ee36a",
  "brief": {
   "site_kind": "a regional theatre"
  }
 },
 {
  "qid": "qe3e85dc10c",
  "brief": {
   "site_kind": "a small seaside hotel"
  }
 },
 {
  "qid": "qc0deb8a9cf",
  "brief": {
   "site_kind": "a quilting guild"
  }
 },
 {
  "qid": "qbd302e0eb2",
  "brief": {
   "site_kind": "a vintage map dealer"
  }
 },
 {
  "qid": "qb9c44a1420",
  "brief": {
   "site_kind": "a public swimming pool"
  }
 },
 {
  "qid": "q1a291839c4",
  "brief": {
   "site_kind": "a chess club"
  }
 },
 {
  "qid": "q562111185a",
  "brief": {
   "site_kind": "a language exchange forum"
  }
 },
 {
  "qid": "q1655b4a3af",
  "brief": {
   "site_kind": "a ceramics studio"
  }
 },
 {
  "qid": "qa1d958f8ce",
  "brief": {
   "site_kind": "a craft cider bar"
  }
 },
 {
  "qid": "q85bd389d6d",
  "brief": {
   "site_kind": "a dance school"
  }
 },
 {
  "qid": "q302bb45889",
  "brief": {
   "site_kind": "a camping gear rental"
  }
 },
 {
  "qid": "qebc3602671",
  "brief": {
   "site_kind": "a science podcast"
  }
 },
 {
  "qid": "qd094e737b1",
  "brief": {
   "site_kind": "a bicycle repair cooperative"
  }
 },
 {
  "qid": "q1e1aa4feb7",
  "brief": {
   "site_kind": "a student newspaper"
  }
 },
 {
  "qid": "q472f2d0cf9",
  "brief": {
   "site_kind": "a community radio station"
  }
 },
 {
  "qid": "q58fc08f71a",
  "brief": {
   "site_kind": "a ski club"
  }
 },
 {
  "qid": "q9692d4dae6",
  "brief": {
   "site_kind": "a sailing school"
  }
 },
 {
  "qid": "q55c1fee10e",
  "brief": {
   "site_kind": "a photography club"
  }
 },
 {
  "qid": "qb513bfa5b3",
  "brief": {
   "site_kind": "a regional ferry operator"
  }
 },
 {
  "qid": "q5ade828f21",
  "brief": {
   "site_kind": "a bookbinding studio"
  }
 },
 {
  "qid": "q51c4d4749c",
  "brief": {
   "site_kind": "a dog grooming salon"
  }
 }
]
