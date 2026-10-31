# T07 authoring task T07-author_freeform-21e4f5e9-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_freeform-21e4f5e9-000.json

Task kind: author_freeform; items: 38; outputs expected: 38.

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write one short ADVERTISEMENT TEXT per item, in the item's register, from the facts given. The text has two
parts: a BODY you write, then the SMALL PRINT, which is the FINE_PRINT fact copied character for character.

Hard rules (a text that breaks one is thrown away):
1. The body names the shop exactly once, with the STORE fact written exactly as given (same letters and capitals).
2. End the text with the FINE_PRINT fact, copied exactly (same characters in the same order, starting with its *),
   on its own line after the body. It appears exactly once, and the * appears nowhere else.
3. Body length: 20-70 words (sms: 10-35 words); one block, single line breaks only, never an empty line.
4. The body never repeats, explains or rephrases anything in the FINE_PRINT, and never names or hints at any offer or
   benefit (a program prints the headline offer above your text).
5. In the body: no digits, number words or ordinals, no dates, times, months, weekdays or time words, no currency or
   percent signs, no web or e-mail addresses, no codes.
6. In the body, none of these words (any letter case):
- number: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
- relative time: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
- quantity: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
- quantifier: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
- modal: able, allowed, can, cannot, could, forbidden, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, would
- hedge: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
- status: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
- operator: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
- phrases: have to, has to, had to, got to, sort of, kind of
7. Words you must never use in the body (any letter case), because they would state an offer or a condition, or name what the small print talks about:
above, address, after, amount, amounts, appliance, appliances, applied, applies, apply, area, areas, arvale, assemble, assembled, assembly, asterisk, autumn, basic, bedding, before, below, black, blue, box, brenmoor, bronze, calderon, categories, category, clearance, condition, conditions, coupon, coupons, date, dates, day, days, deadline, deliver, delivered, deliveries, delivers, delivery, detail, details, discount, discounted, discounts, double, dunmere, electronics, elite, ending, ends, eskarth, every, exclude, excluded, excludes, excluding, exclusion, exclusions, exclusive, exclusively, expire, expires, expiry, fall, fallowmere, final, fine, footnote, footnotes, free, freely, furniture, garden, gear, gift, gifts, gold, green, greyhaven, holiday, holidays, hollin, hour, hours, install, installation, installed, kitchenware, level, levels, lifetime, limit, limited, lower, match, matched, matching, maximum, member, members, membership, minimum, minute, minutes, month, months, only, open, over, pet, platinum, plus, point, points, postcode, pre-order, premier, price, priced, prices, pricing, print, qualifying, rank, ranks, refurbished, region, regions, regular, restricted, restriction, restrictions, return, returns, reward, rewards, sale, sales, season, seasonal, seasons, select, selected, ship, shipment, shipments, shipped, shipping, ships, silver, spend, spending, sports, spring, status, subtotal, summer, supplies, term, terms, through, tier, tiers, till, time, tools, total, totals, toys, under, until, valid, validity, warranties, warranty, week, weeks, while, winter, wrap, wrapped, wrapping, year, years, zone, zones
8. No negation in the body: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
9. Capital letters in the body only at the start of a sentence or a line (or a label such as "Subject:"), plus the
   shop's name.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "text": "<the text>"}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qcc1558a0af",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Excludes the toys category. Order by 19 January 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qac86aa01a2",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Items sold as open box are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qeef3eda304",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Excludes final sale items. Minimum order subtotal: $150.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q676e5b589a",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Pebblestone Garden",
   "FINE_PRINT": "*Items sold as pre-order are excluded. Order by 12 March 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qf259feab65",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Valid on orders over $200.00. Valid for orders placed on or before 22 July 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q36f799aaf0",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Excludes delivery to Greyhaven."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q8e67262891",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Covers the kitchenware product category only. Excludes delivery to Brenmoor."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qcf06f8ee57",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Larkspur Playthings",
   "FINE_PRINT": "*Excludes delivery to Brenmoor. The order subtotal must be above $200.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4dbed6b531",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Valid on orders of $75.00 or more. Valid for orders placed on or after 4 September 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q2e34f0e211",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Valid for orders placed from 20 March 2026 onward."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qb8de67ab1c",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Orders delivered to Arvale are excluded. Items sold as clearance are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q401ee70b6c",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Cedarline Living",
   "FINE_PRINT": "*Excludes pre-order items. Orders delivered to Greyhaven are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qb391e9662f",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Pebblestone Garden",
   "FINE_PRINT": "*Excludes final sale items. Excludes the electronics category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qb8f31a5cd0",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Northvale Audio",
   "FINE_PRINT": "*Valid for orders placed from 21 May 2026 onward. Orders delivered to Hollin are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q04d76ee6c8",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Juniper Gadgets",
   "FINE_PRINT": "*Members at the Plus level or lower only. Valid for orders placed on or before 23 May 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qdf79a43a35",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Minimum order subtotal: $100.00. Excludes delivery to Hollin."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qc10def8876",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Cedarline Living",
   "FINE_PRINT": "*The order subtotal must be above $100.00. Valid for orders placed before 17 February 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qe0d4585628",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Oakhurst Interiors",
   "FINE_PRINT": "*Excludes the bedding category. Valid on orders of $50.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q5d8666d054",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Valid on orders of $35.00 or more. Valid for orders placed on or before 18 July 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q8e0787e5e3",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Members at the Premier level or higher only. Valid on orders of $200.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qf9251b0f7e",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Wrenfield Outdoor",
   "FINE_PRINT": "*Excludes the pet supplies category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q7f1c463106",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Valid on orders over $25.00. Valid for orders placed from 14 July 2026 onward."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q0d9bf86a05",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*The order subtotal must be above $100.00. Members at the Blue level or higher only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q38f9f11b0b",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Valid for orders placed before 27 May 2026. Excludes delivery to Dunmere."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qa6889b9ca9",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Harborlight Goods",
   "FINE_PRINT": "*Order by 9 August 2026 at the latest. Excludes delivery to Greyhaven."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q39bcbe72bb",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Excludes final sale items. Valid for orders placed on or after 27 October 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qe54a204810",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Valid on orders of $50.00 or more. Orders must be placed earlier than 14 January 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4b4d85859a",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Harborlight Goods",
   "FINE_PRINT": "*Valid on orders over $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qc3e8dfc6c2",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Excludes delivery to Calderon. Valid for orders placed on or before 26 March 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qcca7df781f",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Wrenfield Outdoor",
   "FINE_PRINT": "*Excludes final sale items. Valid on orders over $35.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q9082fd6d82",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Excludes delivery to Eskarth. Minimum order subtotal: $35.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q1e82c7b51c",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Cedarline Living",
   "FINE_PRINT": "*Valid for orders placed before 13 April 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q756768dc32",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Larkspur Playthings",
   "FINE_PRINT": "*Excludes the pet supplies category. Valid on orders over $25.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q48a8125f3d",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Orders delivered to Fallowmere are excluded. Members at the Blue level or higher only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4e85d3a76a",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Harborlight Goods",
   "FINE_PRINT": "*Order by 24 August 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qb8867d5eb9",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Harborlight Goods",
   "FINE_PRINT": "*Members at the Blue level or lower only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q49585dbbe0",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Members at the Plus level or higher only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qefb3135996",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty)",
  "register": "warranty_card",
  "facts": {
   "STORE": "Fernway Market",
   "FINE_PRINT": "*Valid only for orders delivered to Calderon. Excludes the pet supplies category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 }
]
