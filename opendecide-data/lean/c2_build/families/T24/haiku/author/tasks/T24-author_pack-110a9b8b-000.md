# T24 authoring task T24-author_pack-110a9b8b-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T24/haiku/author/answers/T24-author_pack-110a9b8b-000.json

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
  "qid": "qa16b1de762",
  "brief": {
   "setting": "a flower delivery service"
  }
 },
 {
  "qid": "q9591496bde",
  "brief": {
   "setting": "a pet grooming salon"
  }
 },
 {
  "qid": "q83160e8e75",
  "brief": {
   "setting": "a campsite"
  }
 },
 {
  "qid": "q5f3ce2ea96",
  "brief": {
   "setting": "a computer repair shop"
  }
 },
 {
  "qid": "q95b27a9f92",
  "brief": {
   "setting": "a shoe repair shop"
  }
 },
 {
  "qid": "q83f2214306",
  "brief": {
   "setting": "a cooking class school"
  }
 },
 {
  "qid": "q1c4bceaa10",
  "brief": {
   "setting": "a self-service laundromat"
  }
 },
 {
  "qid": "q7a660b5167",
  "brief": {
   "setting": "a home cleaning service"
  }
 },
 {
  "qid": "q31cb7aaebc",
  "brief": {
   "setting": "a garden centre"
  }
 },
 {
  "qid": "qb1c037e726",
  "brief": {
   "setting": "a tailoring shop"
  }
 },
 {
  "qid": "qed6b488d46",
  "brief": {
   "setting": "a car parts shop"
  }
 },
 {
  "qid": "qf4ebbc4b5c",
  "brief": {
   "setting": "a day spa"
  }
 },
 {
  "qid": "q8e6fa96769",
  "brief": {
   "setting": "a phone repair kiosk"
  }
 },
 {
  "qid": "qda3c11e105",
  "brief": {
   "setting": "a concert hall cloakroom"
  }
 },
 {
  "qid": "qdd258fecda",
  "brief": {
   "setting": "a dog walking service"
  }
 },
 {
  "qid": "qefdb02b764",
  "brief": {
   "setting": "an escape room venue"
  }
 },
 {
  "qid": "q45551d9e03",
  "brief": {
   "setting": "a poster printing shop"
  }
 },
 {
  "qid": "q2d74bf7b73",
  "brief": {
   "setting": "a museum gift shop"
  }
 },
 {
  "qid": "q944fed1b35",
  "brief": {
   "setting": "a dry cleaner"
  }
 },
 {
  "qid": "qc1b64171ed",
  "brief": {
   "setting": "a boat tour operator"
  }
 },
 {
  "qid": "qf7af87d924",
  "brief": {
   "setting": "a bowling alley"
  }
 },
 {
  "qid": "q9d8c5a4582",
  "brief": {
   "setting": "a furniture delivery service"
  }
 },
 {
  "qid": "qe82fe1dc02",
  "brief": {
   "setting": "a language learning app"
  }
 },
 {
  "qid": "qd6b04abd2e",
  "brief": {
   "setting": "a camera rental shop"
  }
 },
 {
  "qid": "qc5e8e1e41a",
  "brief": {
   "setting": "a removals firm"
  }
 },
 {
  "qid": "q059d279a9f",
  "brief": {
   "setting": "a music streaming service"
  }
 },
 {
  "qid": "q62ca2ec293",
  "brief": {
   "setting": "a city bike share scheme"
  }
 },
 {
  "qid": "q6847f3385e",
  "brief": {
   "setting": "a ski equipment rental"
  }
 },
 {
  "qid": "q7dc113a732",
  "brief": {
   "setting": "a bakery taking custom cake orders"
  }
 },
 {
  "qid": "qa8b9ec1045",
  "brief": {
   "setting": "a coworking space"
  }
 },
 {
  "qid": "qa0a9fe1fba",
  "brief": {
   "setting": "an online bookshop"
  }
 },
 {
  "qid": "q47b19dfce0",
  "brief": {
   "setting": "a meal kit delivery service"
  }
 },
 {
  "qid": "qe199b5b77b",
  "brief": {
   "setting": "a mattress store"
  }
 },
 {
  "qid": "q5dede41160",
  "brief": {
   "setting": "a wedding venue"
  }
 },
 {
  "qid": "qa3bd5f306d",
  "brief": {
   "setting": "a toy library"
  }
 },
 {
  "qid": "q3f2236539f",
  "brief": {
   "setting": "a photo printing shop"
  }
 },
 {
  "qid": "qa549f492b3",
  "brief": {
   "setting": "a climbing wall"
  }
 },
 {
  "qid": "q6002e75464",
  "brief": {
   "setting": "a bicycle rental shop"
  }
 },
 {
  "qid": "qe11757dcf8",
  "brief": {
   "setting": "a parking garage"
  }
 },
 {
  "qid": "q839f5e5ce2",
  "brief": {
   "setting": "a car wash chain"
  }
 }
]
