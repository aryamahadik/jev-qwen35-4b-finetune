# T07 authoring task T07-author_wording-762e590a-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_wording-762e590a-000.json

Task kind: author_wording; items: 7; outputs expected: 42.

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write QUESTION WORDINGS. A program shows a shop's advertisement (headline offers marked with symbols, and small
print), a customer's order record and short reading instructions, then asks one question in your wording. Each item
states exactly what the question must mean; write the number of different wordings it asks for, all with that same
meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question, 6-30 words, ending with "?". Use each placeholder the item lists exactly once, spelled exactly so with
   its curly braces: {CUSTOMER} (the customer's full name), {ORDER_ID} (the order's code) and, where listed, {ASKED}
   (the name of one advertised benefit, such as 'free returns' or 'the price match'). Never put "a", "an" or "the"
   directly before {ASKED}.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it.
3. Negation exactly as the item says and nowhere else. The full list of negation words is: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
4. No digits, number words, dates, names, hedges (maybe, probably, seems, think, believe, likely) or time words (now,
   currently, already, soon, yet, today, next, last). Capital letter only on the first word.
5. Never name a benefit, a region, a product category, a price status, a membership level, an amount or a date
   (the placeholders carry them), and never list answer choices. None of these words (any letter case):
   appliance, appliances, arvale, assemble, assembled, assembly, basic, bedding, black, blue, box, brenmoor, bronze, calderon, clearance, delivery, double, dunmere, electronics, elite, eskarth, fallowmere, final, free, furniture, garden, gear, gift, gifts, gold, green, greyhaven, hollin, install, installation, installed, kitchenware, lifetime, lower, match, matched, matching, open, pet, platinum, plus, point, points, pre-order, premier, price, refurbished, regular, return, returns, reward, rewards, sale, shipping, silver, sports, supplies, tools, toys, warranties, warranty, wrap, wrapped, wrapping.
   A question about which condition is missed also avoids these words: address, amount, amounts, area, areas, autumn, categories, category, clearance, coupon, coupons, date, dates, day, days, deliver, delivered, deliveries, delivers, delivery, discount, discounted, discounts, fall, holiday, holidays, hour, hours, level, levels, minute, minutes, month, months, postcode, price, priced, prices, pricing, rank, ranks, region, regions, sale, sales, season, seasonal, seasons, ship, shipment, shipments, shipped, shipping, ships, spend, spending, spring, status, subtotal, summer, tier, tiers, time, total, totals, week, weeks, winter, year, years, zone, zones.
6. Tie the question to the advertisement as the item's style says, and vary the structure across your wordings
   (who is the subject: the customer, the order, the advertisement; short and long forms).
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qf0903a460a",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the advertised terms? Use a verb with the opposite meaning of 'get' (such as lose out on, go short of, forfeit, be shut out of) and NO negation word at all (not 'without', not 'denied', not 'fail')",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 6
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "6 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q1e59af3d15",
  "brief": {
   "meaning": "which single condition in the small print attached to {ASKED} does order {ORDER_ID} from {CUSTOMER} miss, IF ANY? The reader picks from a list shown after the question that also has a choice for 'every condition is met', so the question must allow that no condition is missed: include 'if any' (or 'if there is one'). Never assume a condition is missed, never name a condition or a kind of condition, no negation word",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 6
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "6 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q93f396e7e1",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} get {ASKED} under the advertisement's terms (its headline together with that headline's small print)? Use a positive verb such as get, receive, earn, come with. No negation word at all",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 6
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "6 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q3e96d4c9cf",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} fail to get {ASKED} under the advertised terms? Use 'fail to' / 'fails to' with a positive verb after it (get, receive, earn, secure); no other negation word, no 'not'",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 6
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "6 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "qa9fd30f281",
  "brief": {
   "meaning": "which of the advertised headline offers does order {ORDER_ID} from {CUSTOMER} actually get, once each offer's own small print is applied? The reader picks from a list shown after the question, so the question names no outcome (never the words both, neither, only, all, none, either, each, every) and has no negation word",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 6
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code"
  },
  "rules": [
   "6 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q8ce57fc8ae",
  "brief": {
   "meaning": "yes/no, a DOUBLE negation with a positive meaning: 'is it not the case that order {ORDER_ID} from {CUSTOMER} does not get {ASKED} under the advertised terms?'. Use exactly two negation words, both 'not' or 'n't' (one on the whole claim, one on getting); no other negation word",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 6
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "6 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "qfa071d1095",
  "brief": {
   "meaning": "yes/no: is it true that order {ORDER_ID} from {CUSTOMER} does NOT get {ASKED} under the advertised terms? Use exactly one 'not' or 'n't', placed on getting the benefit; no other negation word",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 6
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "6 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 }
]
