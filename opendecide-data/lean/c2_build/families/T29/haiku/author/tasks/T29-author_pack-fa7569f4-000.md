# T29 authoring task T29-author_pack-fa7569f4-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_pack-fa7569f4-000.json

Task kind: author_pack; items: 40; outputs expected: 40.

You are writing short pieces of text for a synthetic training dataset about software agents that follow
written company policies. Everything you write is either a reusable template (a program later fills each {SLOT}
placeholder with a value) or a list of invented values. Write natural, varied English. Invent everything: never copy
text from real companies, products, people, laws, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: invent one organisation PACK per item. A pack is a small set of invented values for one organisation. Each
item gives a setting (the kind of organisation); fit the values to it.

Fields of "pack" (all invented; no real company, brand, product or person):
- "org_name": the organisation's short invented name, one or two words.
- "org_domain": its domain: lowercase letters (and at most one hyphen) followed by ".example", e.g. "ledgerline.example".
- "lookalike_domains": exactly two domains that look almost like org_domain but are different strings: insert or
  remove one hyphen, double or drop one letter, or switch the ending to ".test". Never identical to org_domain.
- "partner_domains": exactly two domains of other invented organisations this one works with (suppliers, service
  firms), clearly different names, ending in ".example".
- "target_prefix": 2-4 capital letters for the ids of records this organisation keeps (e.g. "INV", "CUS", "TBL").
- "people": exactly four invented full names (first name + family name, letters only), varied in cultural origin,
  no titles, no famous people, no word that is also a negation (such as "Never" or "Nobody").
No digits in any field. All four people, both look-alikes and both partners are distinct within the pack, and no
value repeats one from another item of this task.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "pack": {...the fields listed below...}}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q81ffc2295f",
  "brief": {
   "setting": "a charity fundraising platform"
  }
 },
 {
  "qid": "q70a442bbd9",
  "brief": {
   "setting": "a recruitment agency"
  }
 },
 {
  "qid": "qa6a5cc10e5",
  "brief": {
   "setting": "an orchestra"
  }
 },
 {
  "qid": "q5c69d197da",
  "brief": {
   "setting": "a hardware store chain"
  }
 },
 {
  "qid": "qbd5d4cd29f",
  "brief": {
   "setting": "a sports league office"
  }
 },
 {
  "qid": "qafaa6c5b7c",
  "brief": {
   "setting": "a fitness app maker"
  }
 },
 {
  "qid": "q7a57c5351e",
  "brief": {
   "setting": "a farm equipment dealer"
  }
 },
 {
  "qid": "q7bfeee4e8e",
  "brief": {
   "setting": "a used car marketplace"
  }
 },
 {
  "qid": "q0c07ab1ea7",
  "brief": {
   "setting": "a recycling collector"
  }
 },
 {
  "qid": "q19562f5283",
  "brief": {
   "setting": "a wind farm operator"
  }
 },
 {
  "qid": "q55100799fd",
  "brief": {
   "setting": "a mortgage broker"
  }
 },
 {
  "qid": "q5d4c9de6bf",
  "brief": {
   "setting": "a tea importer"
  }
 },
 {
  "qid": "qc1fa40b100",
  "brief": {
   "setting": "a coffee roaster"
  }
 },
 {
  "qid": "q2ca50de4de",
  "brief": {
   "setting": "a tax preparation firm"
  }
 },
 {
  "qid": "qc5fcd0d039",
  "brief": {
   "setting": "a credit union"
  }
 },
 {
  "qid": "q5e976358b2",
  "brief": {
   "setting": "an event ticketing service"
  }
 },
 {
  "qid": "q4bb517473f",
  "brief": {
   "setting": "a satellite imagery firm"
  }
 },
 {
  "qid": "q66af5365d2",
  "brief": {
   "setting": "a vineyard group"
  }
 },
 {
  "qid": "q8985526805",
  "brief": {
   "setting": "a parking operator"
  }
 },
 {
  "qid": "qa7320383a0",
  "brief": {
   "setting": "a warehouse automation vendor"
  }
 },
 {
  "qid": "q6a435a5530",
  "brief": {
   "setting": "a scientific journal publisher"
  }
 },
 {
  "qid": "q04f0b94f0e",
  "brief": {
   "setting": "a climbing gym chain"
  }
 },
 {
  "qid": "qdf06e7c434",
  "brief": {
   "setting": "a hospital laundry service"
  }
 },
 {
  "qid": "q02e70c81c2",
  "brief": {
   "setting": "a dairy cooperative"
  }
 },
 {
  "qid": "q52c42e5dde",
  "brief": {
   "setting": "a bookkeeping startup"
  }
 },
 {
  "qid": "q4082ab24f8",
  "brief": {
   "setting": "a home insurance broker"
  }
 },
 {
  "qid": "q59d4af867d",
  "brief": {
   "setting": "a translation agency"
  }
 },
 {
  "qid": "qc135d70e75",
  "brief": {
   "setting": "a stock photo agency"
  }
 },
 {
  "qid": "qd2f643e8b9",
  "brief": {
   "setting": "a security training firm"
  }
 },
 {
  "qid": "q6f184c31ea",
  "brief": {
   "setting": "a medical device repair shop"
  }
 },
 {
  "qid": "q91416ad826",
  "brief": {
   "setting": "a boat charter company"
  }
 },
 {
  "qid": "qb208f781bf",
  "brief": {
   "setting": "a podcast network"
  }
 },
 {
  "qid": "q252c809420",
  "brief": {
   "setting": "a children's museum"
  }
 },
 {
  "qid": "qaef1d3a2a4",
  "brief": {
   "setting": "an architecture practice"
  }
 },
 {
  "qid": "q48c2f1b304",
  "brief": {
   "setting": "a film festival office"
  }
 },
 {
  "qid": "q50a3655786",
  "brief": {
   "setting": "a bakery chain"
  }
 },
 {
  "qid": "q91c601dfd4",
  "brief": {
   "setting": "a public archive"
  }
 },
 {
  "qid": "qc8d56c083f",
  "brief": {
   "setting": "a car rental franchise"
  }
 },
 {
  "qid": "q32d9b2baba",
  "brief": {
   "setting": "a school district IT team"
  }
 },
 {
  "qid": "qa253e9013f",
  "brief": {
   "setting": "a moving company"
  }
 }
]
