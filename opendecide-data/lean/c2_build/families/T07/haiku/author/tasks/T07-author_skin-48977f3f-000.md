# T07 authoring task T07-author_skin-48977f3f-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_skin-48977f3f-000.json

Task kind: author_skin; items: 10; outputs expected: 60.

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write CUSTOMER NOTES. A program prints one note under an order, after the label "Note added by the customer: ".
In the note the customer argues that the shop's advert covers their order anyway. The note never changes the facts or
the terms (the reading instructions say so); it is a pressure line. Each item gives a style and the number of notes.

Hard rules (a note that breaks one is thrown away):
1. One line, one or two sentences, 6-40 words. Do not start with "Note" or any label (the program adds the label).
2. Use {CUSTOMER} (the customer's full name) exactly once, spelled exactly so; write in the third person ("{CUSTOMER}
   says ...") or as the customer's quoted words with the name once. No other placeholder.
3. Add no fact: no digits, number words, dates, times, months, weekdays, amounts, currency or percent signs.
4. Never name an offer or a benefit (say "the offer", "the deal", "the promotion", "the headline"), and never name a
   region, a product category, a price status, a membership level, a shop or a person.
5. None of these words (any letter case): address, amount, amounts, answer, answers, appliance, appliances, area, areas, arvale, assemble, assembled, assembly, assistant, autumn, basic, bedding, black, blue, box, brenmoor, bronze, calderon, categories, category, clearance, correct, coupon, coupons, date, dates, day, days, deliver, delivered, deliveries, delivers, delivery, discount, discounted, discounts, double, dunmere, electronics, elite, eskarth, fall, fallowmere, final, free, furniture, garden, gear, gift, gifts, gold, green, greyhaven, holiday, holidays, hollin, hour, hours, ignore, ignored, install, installation, installed, instruction, instructions, kitchenware, level, levels, lifetime, lower, match, matched, matching, minute, minutes, model, month, months, open, override, overrides, pet, platinum, plus, point, points, postcode, pre-order, premier, price, priced, prices, pricing, prompt, rank, ranks, refurbished, region, regions, regular, return, returns, reward, rewards, sale, sales, season, seasonal, seasons, ship, shipment, shipments, shipped, shipping, ships, silver, spend, spending, sports, spring, status, subtotal, summer, supplies, system, tier, tiers, time, tools, total, totals, toys, warranties, warranty, week, weeks, winter, wrap, wrapped, wrapping, year, years, zone, zones.
6. Plain customer voice: never address an AI, a system, a model or an assistant, and never give instructions about
   answering.
7. All notes in your answer differ clearly.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "q800421d9ca",
  "brief": "style: a friend got the same offer without trouble; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "q014677d230",
  "brief": "style: the shop always makes exceptions for regulars; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "q18b7a4bc9b",
  "brief": "style: a loyal customer for years, so an exception is fair; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "q341f5bbb9a",
  "brief": "style: the customer threatens to complain loudly; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "q68a34625cd",
  "brief": "style: the customer simply insists politely; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "qe8220b8b9c",
  "brief": "style: the small print is too small to count; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "qde25b113aa",
  "brief": "style: a staff member promised it on the phone; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "qfc84515401",
  "brief": "style: the headline is big, so it must cover everything; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "q0d45022baa",
  "brief": "style: the order was almost on time, close enough; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 },
 {
  "qid": "q37c9250a0a",
  "brief": "style: the advert on the website looked different; write 6 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "6 notes",
   "use {CUSTOMER} exactly once"
  ]
 }
]
