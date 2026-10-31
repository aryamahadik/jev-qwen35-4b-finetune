# T24 authoring task T24-author_pack-f6e3d247-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_pack-f6e3d247-000.json

Task kind: author_pack; items: 40; outputs expected: 40.

You are writing short pieces of text for a synthetic training dataset about everyday customer-service
policies (returns, repairs, bookings, deposits, fees and the like). Everything you write is either a reusable template
(a program later fills each {SLOT} placeholder with a value) or a set of invented values. Write natural, varied
English. Invent everything: never copy text from real companies, products, people, laws, websites or published
datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: invent one policy PACK per item: the vocabulary of one invented everyday customer-service policy. Each item
gives a setting (the kind of business or service); fit every value to it.

Fields of "pack" (all invented; no real company, brand, product, place or person):
- "title": the policy's name: two to four lower-case words ending with the word "policy" (e.g. "lost luggage policy").
- "prefix": exactly three capital letters that start the case numbers (e.g. "LUG").
- "date_fields": exactly two names of dates that every case of this policy has, each two or three lower-case words
  ending with the word "date" (e.g. ["flight date", "report date"]). In a normal case the first date is never later
  than the second. Neither may be "request date".
- "money_field": the name of the money amount of a case, one to three lower-case words (e.g. "claimed value").
- "categories": four or five kinds of items, services or plans the policy covers, lower case, one to three words each
  (e.g. ["suitcases", "backpacks", "sports gear", "instruments"]).
- "conditions": exactly three short states a case can be in, lower case, one to three words each, that read
  naturally after "the condition is" (e.g. ["tagged", "receipt kept", "photo only"]).
- "outcomes": exactly three outcome names, lower case, two or three words each, in this order: the full result the
  customer asks for, a partial or alternative result, and the request turned down (e.g. ["full settlement",
  "partial settlement", "claim declined"]). Each reads naturally after "the outcome is".

Rules for every value (a pack that breaks one is thrown away):
1. Only lower-case letters, spaces, hyphens and apostrophes (the prefix: three capital letters); no digits, commas,
   pipes or braces; never the word "and".
2. No negation word or cue anywhere: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, refuse to, prevent ... from, rule out.
3. All values within a pack are distinct, and no word of the three outcome names appears in the categories,
   conditions, date fields or money field. Categories, conditions, date fields and the money field never use the
   words refund, credit, compensation, voucher, reimbursement, payout or rebate.
4. No word about comparing or revising anywhere (such as alter, revise, update, version, identical, compare).
5. Everyday consumer settings only: nothing medical, legal, about children or about personal safety; plain words.
6. Every pack in your answer has its own title, prefix and categories (no repeats across items).

Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "pack": {...the fields listed above...}}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qbb50e2442d",
  "brief": {
   "setting": "a wine club"
  }
 },
 {
  "qid": "q36b0042fca",
  "brief": {
   "setting": "a sports kit shop"
  }
 },
 {
  "qid": "q34aef28cd6",
  "brief": {
   "setting": "a dance studio"
  }
 },
 {
  "qid": "q0ab214b265",
  "brief": {
   "setting": "a public swimming pool"
  }
 },
 {
  "qid": "qfbdec55c87",
  "brief": {
   "setting": "a language exam centre"
  }
 },
 {
  "qid": "q844b2c48c2",
  "brief": {
   "setting": "a stationery shop"
  }
 },
 {
  "qid": "q30fba721ba",
  "brief": {
   "setting": "a theme park"
  }
 },
 {
  "qid": "qef0b7b39e7",
  "brief": {
   "setting": "a golf course"
  }
 },
 {
  "qid": "q28f92fd533",
  "brief": {
   "setting": "a self-storage facility"
  }
 },
 {
  "qid": "q017b739a65",
  "brief": {
   "setting": "a kayak hire base"
  }
 },
 {
  "qid": "qe88a35df3d",
  "brief": {
   "setting": "a jewellery repair shop"
  }
 },
 {
  "qid": "q72bb5502be",
  "brief": {
   "setting": "a magazine publisher"
  }
 },
 {
  "qid": "q880df3cb1a",
  "brief": {
   "setting": "a recording studio"
  }
 },
 {
  "qid": "qcc99ae0799",
  "brief": {
   "setting": "a tutoring centre"
  }
 },
 {
  "qid": "qad6cc47e87",
  "brief": {
   "setting": "a board game cafe"
  }
 },
 {
  "qid": "qbdbd7a5d15",
  "brief": {
   "setting": "a cat boarding cattery"
  }
 },
 {
  "qid": "q1714eee875",
  "brief": {
   "setting": "a scuba diving school"
  }
 },
 {
  "qid": "q095e2c7579",
  "brief": {
   "setting": "a party equipment hire"
  }
 },
 {
  "qid": "q5398b82b06",
  "brief": {
   "setting": "a window cleaning service"
  }
 },
 {
  "qid": "q9cc908f8e7",
  "brief": {
   "setting": "a chess club"
  }
 },
 {
  "qid": "q0e6b1514dd",
  "brief": {
   "setting": "a cinema"
  }
 },
 {
  "qid": "q55b88d220c",
  "brief": {
   "setting": "an online plant nursery"
  }
 },
 {
  "qid": "q89309cbba1",
  "brief": {
   "setting": "a craft supply store"
  }
 },
 {
  "qid": "q6607e9e698",
  "brief": {
   "setting": "a portrait photography studio"
  }
 },
 {
  "qid": "q96486bfab9",
  "brief": {
   "setting": "a hair salon"
  }
 },
 {
  "qid": "q38b5c201a2",
  "brief": {
   "setting": "a key cutting kiosk"
  }
 },
 {
  "qid": "qd4ac2b54ca",
  "brief": {
   "setting": "a tool hire shop"
  }
 },
 {
  "qid": "qc476c43fb9",
  "brief": {
   "setting": "a picture framing shop"
  }
 },
 {
  "qid": "q483064e452",
  "brief": {
   "setting": "a farm produce box delivery"
  }
 },
 {
  "qid": "qc5393e9ba2",
  "brief": {
   "setting": "a car ferry booking desk"
  }
 },
 {
  "qid": "q78e940328b",
  "brief": {
   "setting": "a holiday cottage agency"
  }
 },
 {
  "qid": "q965ad45e4f",
  "brief": {
   "setting": "a vintage clothing shop"
  }
 },
 {
  "qid": "q654944eed4",
  "brief": {
   "setting": "a carpet cleaning service"
  }
 },
 {
  "qid": "q2b1e2912c7",
  "brief": {
   "setting": "a printer ink shop"
  }
 },
 {
  "qid": "q617bb3b2d0",
  "brief": {
   "setting": "a pottery studio"
  }
 },
 {
  "qid": "q6ac058a0b7",
  "brief": {
   "setting": "a costume rental shop"
  }
 },
 {
  "qid": "q5d00f3b6ae",
  "brief": {
   "setting": "a coffee machine supplier"
  }
 },
 {
  "qid": "q0fdeb94a15",
  "brief": {
   "setting": "a driving school"
  }
 },
 {
  "qid": "qcc73ecb021",
  "brief": {
   "setting": "an electric bike shop"
  }
 },
 {
  "qid": "q19067a687d",
  "brief": {
   "setting": "a piano tuning service"
  }
 }
]
