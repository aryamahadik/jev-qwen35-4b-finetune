# T29 authoring task T29-author_pack-c161f8fd-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T29/haiku/author/answers/T29-author_pack-c161f8fd-000.json

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
  "qid": "qe1ad62145e",
  "brief": {
   "setting": "a wholesale florist"
  }
 },
 {
  "qid": "q95d4b734d2",
  "brief": {
   "setting": "a regional water utility"
  }
 },
 {
  "qid": "q9e95daf1d6",
  "brief": {
   "setting": "a regional freight brokerage"
  }
 },
 {
  "qid": "qbde19afa8f",
  "brief": {
   "setting": "a game studio"
  }
 },
 {
  "qid": "q0bce678711",
  "brief": {
   "setting": "a municipal library network"
  }
 },
 {
  "qid": "q67df0bf350",
  "brief": {
   "setting": "a dental practice group"
  }
 },
 {
  "qid": "q03993f4f59",
  "brief": {
   "setting": "a food delivery cooperative"
  }
 },
 {
  "qid": "q23a040cf9c",
  "brief": {
   "setting": "a mid-size online bookshop"
  }
 },
 {
  "qid": "q74da9356c7",
  "brief": {
   "setting": "a veterinary pharmacy"
  }
 },
 {
  "qid": "qc4de5eadb3",
  "brief": {
   "setting": "a solar panel installer"
  }
 },
 {
  "qid": "qd6457fea24",
  "brief": {
   "setting": "a coworking space operator"
  }
 },
 {
  "qid": "q140402b42a",
  "brief": {
   "setting": "a ski resort"
  }
 },
 {
  "qid": "qc529e5903f",
  "brief": {
   "setting": "a home care agency"
  }
 },
 {
  "qid": "qda63e07a1b",
  "brief": {
   "setting": "a hotel group"
  }
 },
 {
  "qid": "q5bc6e3d9c4",
  "brief": {
   "setting": "a robotics startup"
  }
 },
 {
  "qid": "qd4d7c740b2",
  "brief": {
   "setting": "a crop research station"
  }
 },
 {
  "qid": "qbc8ce9bb10",
  "brief": {
   "setting": "a payroll services bureau"
  }
 },
 {
  "qid": "q4b6c34e8a4",
  "brief": {
   "setting": "a chain of veterinary clinics"
  }
 },
 {
  "qid": "q0ef99e0a76",
  "brief": {
   "setting": "a cloud backup provider"
  }
 },
 {
  "qid": "q1952e1fc17",
  "brief": {
   "setting": "a marine survey company"
  }
 },
 {
  "qid": "q5b3a07349e",
  "brief": {
   "setting": "a community health clinic network"
  }
 },
 {
  "qid": "q225c94f49d",
  "brief": {
   "setting": "a craft brewery group"
  }
 },
 {
  "qid": "qaa97044426",
  "brief": {
   "setting": "a fashion resale marketplace"
  }
 },
 {
  "qid": "q42c6c0bbc9",
  "brief": {
   "setting": "a food bank network"
  }
 },
 {
  "qid": "q071646af00",
  "brief": {
   "setting": "a language school group"
  }
 },
 {
  "qid": "qce55b6b7f2",
  "brief": {
   "setting": "a print shop chain"
  }
 },
 {
  "qid": "q8cbad66f71",
  "brief": {
   "setting": "a city transit IT desk"
  }
 },
 {
  "qid": "qf625d962e1",
  "brief": {
   "setting": "a regional news site"
  }
 },
 {
  "qid": "q53c298c619",
  "brief": {
   "setting": "a university research office"
  }
 },
 {
  "qid": "q108e56e608",
  "brief": {
   "setting": "an insurance claims office"
  }
 },
 {
  "qid": "qb7e513a511",
  "brief": {
   "setting": "a property management firm"
  }
 },
 {
  "qid": "qedfccf11c8",
  "brief": {
   "setting": "a legal aid clinic"
  }
 },
 {
  "qid": "q9a8d7ee653",
  "brief": {
   "setting": "a regional airline's ground operations team"
  }
 },
 {
  "qid": "q738f0b594c",
  "brief": {
   "setting": "a seed bank"
  }
 },
 {
  "qid": "qb235b7c201",
  "brief": {
   "setting": "a toy manufacturer"
  }
 },
 {
  "qid": "q7cf3f7d9f2",
  "brief": {
   "setting": "a museum consortium"
  }
 },
 {
  "qid": "q2fcd244f8b",
  "brief": {
   "setting": "a bicycle sharing scheme"
  }
 },
 {
  "qid": "q5e3b01a7d5",
  "brief": {
   "setting": "a pet insurance startup"
  }
 },
 {
  "qid": "q13a1b0f25a",
  "brief": {
   "setting": "a parcel locker network"
  }
 },
 {
  "qid": "qdb69b3c561",
  "brief": {
   "setting": "a public radio station"
  }
 }
]
