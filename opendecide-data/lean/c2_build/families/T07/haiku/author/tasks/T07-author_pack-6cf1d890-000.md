# T07 authoring task T07-author_pack-6cf1d890-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_pack-6cf1d890-000.json

Task kind: author_pack; items: 30; outputs expected: 30.

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: invent one STORE PACK per item: the invented values a fictional shop of the item's kind uses in its adverts and
order records. Fit every value to the item's shop kind.

Fields of "pack" (all invented: no real company, brand, product line, person or place):
- "store": the shop's name, two or three capitalised words, letters only (such as "Fernway Market"). It must not
  contain a word that names a product category, a delivery region, a membership level or a price status.
- "ladder": the shop's membership levels, lowest first, exactly as many as the item asks (3 or 4). Each level is one
  capitalised word, letters only, and the order from lowest to highest must be easy to follow (metals, gems, sizes,
  trees by height, stars by brightness ...). Avoid the common ladders Bronze/Silver/Gold/Platinum,
  Basic/Plus/Premier/Elite and Green/Blue/Black.
- "regions": exactly four invented delivery-region names, one capitalised word each, letters only, sounding like
  places but not real ones (such as "Arvale").
- "categories": exactly three product categories the shop sells, lower case, one or two words, plural or mass nouns
  (such as "camp stoves"). Never a price word or a status such as clearance, sale, refurbished or open box.
- "customers": exactly four invented customers' full names (first name and family name, letters only, an optional
  hyphen), varied in cultural origin, no famous people.
No digits anywhere. No value may contain a negation word (such as no, not, never, none, nobody). All values within a
pack differ, and no value repeats a value of another item in this task.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "pack": {"store": "...", "ladder": [...], "regions": [...], "categories": [...], "customers": [...]}}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q5c3cc2466a",
  "brief": {
   "shop_kind": "a skate and surf shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q8d56bbc8ba",
  "brief": {
   "shop_kind": "a workwear outfitter",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qc75a8c9d20",
  "brief": {
   "shop_kind": "a model and hobby shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qe3ea8d0374",
  "brief": {
   "shop_kind": "a mattress store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qd25936a3a6",
  "brief": {
   "shop_kind": "a home appliance retailer",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q56ec75660f",
  "brief": {
   "shop_kind": "a beauty supplies shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q4d97f9017f",
  "brief": {
   "shop_kind": "a ceramics studio shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q79d483ee45",
  "brief": {
   "shop_kind": "a dance wear shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qf3b23cf596",
  "brief": {
   "shop_kind": "a camera repair and accessories shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q97136aa3c4",
  "brief": {
   "shop_kind": "a bathroom fittings showroom",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q614ed3771e",
  "brief": {
   "shop_kind": "a swimming and pool supplies store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qf3599ed0c3",
  "brief": {
   "shop_kind": "a kitchen appliance outlet",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qff5dcbaae0",
  "brief": {
   "shop_kind": "a candle and gift shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qa3b7f30711",
  "brief": {
   "shop_kind": "a picture framing shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qca6763a536",
  "brief": {
   "shop_kind": "a sewing machine dealer",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qca5c6d5843",
  "brief": {
   "shop_kind": "a stargazing and telescope shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qa1d3d9cd48",
  "brief": {
   "shop_kind": "a home brewing supplies shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qe6cfe61dfa",
  "brief": {
   "shop_kind": "a board game store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q72c74115ec",
  "brief": {
   "shop_kind": "a cycling apparel store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qde46d82531",
  "brief": {
   "shop_kind": "a smart home gadget store",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qb747d08d78",
  "brief": {
   "shop_kind": "a rug and carpet store",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q4e1131b4b1",
  "brief": {
   "shop_kind": "a school supplies store",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q2484889c7d",
  "brief": {
   "shop_kind": "a reptile and aquarium store",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qa5ca1d4036",
  "brief": {
   "shop_kind": "a tool hire and sales yard",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q456ae53cb4",
  "brief": {
   "shop_kind": "a garden furniture store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qa5b3f24ca0",
  "brief": {
   "shop_kind": "a window blinds and curtains shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qc4db1c84c6",
  "brief": {
   "shop_kind": "a climbing gear shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qafb68dcb3a",
  "brief": {
   "shop_kind": "a yarn and knitting shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q26b8de266b",
  "brief": {
   "shop_kind": "an equestrian supplies store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qd4283e6e9c",
  "brief": {
   "shop_kind": "a vintage furniture dealer",
   "ladder_levels": 4
  }
 }
]
