# T07 authoring task T07-author_freeform-da6c721b-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_freeform-da6c721b-000.json

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
  "qid": "qdf1926d0a6",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Minimum order subtotal: $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q339c653cc4",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Oakhurst Interiors",
   "FINE_PRINT": "*Valid only for orders delivered to Greyhaven. Excludes refurbished items."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q9e38221c26",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Valid on orders of $25.00 or more. Members at the Plus level or higher only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q6d45d17847",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*For Premier members and above. Valid for orders placed on or before 29 September 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q6acd87c9fc",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Wrenfield Outdoor",
   "FINE_PRINT": "*For Premier members and below."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qd53de5987e",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Items in the furniture product category are excluded. Items sold as open box are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qce61920b2c",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*The order subtotal must be above $35.00. Excludes refurbished items."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qfa7dbab97a",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Fernway Market",
   "FINE_PRINT": "*Excludes clearance items. Valid for orders placed before 10 November 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q0008a1e65d",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Fernway Market",
   "FINE_PRINT": "*Valid for orders placed on or before 13 November 2026. Excludes the pet supplies category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q3da23c77bc",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Excludes delivery to Calderon. Items in the garden tools product category are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q952d925619",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Wrenfield Outdoor",
   "FINE_PRINT": "*Delivery to Brenmoor only. Order by 19 October 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qf69114f0e3",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Juniper Gadgets",
   "FINE_PRINT": "*Order by 23 March 2026 at the latest. Items sold as final sale are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qfb47d8935d",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Juniper Gadgets",
   "FINE_PRINT": "*Members at the Elite level or higher only. Items sold as open box are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q0f105443e7",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Valid for orders placed on or before 9 November 2026. Minimum order subtotal: $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qe6b3b7aa8b",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Fernway Market",
   "FINE_PRINT": "*Minimum order subtotal: $150.00. Valid only for orders delivered to Arvale."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q10113c36f3",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Delivery to Calderon only. Valid on orders over $50.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q09983c15f7",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Valid for orders placed on or after 28 November 2026. Minimum order subtotal: $35.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qa4e6f40f2c",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Valid on orders over $35.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qa44743aaf4",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Items in the toys product category are excluded. Orders delivered to Fallowmere are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qfef043733c",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Northvale Audio",
   "FINE_PRINT": "*Members at the Elite level or higher only. Valid on orders over $150.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q755b42353a",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Delivery to Dunmere only. Valid on orders of $200.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qda459fd912",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Juniper Gadgets",
   "FINE_PRINT": "*Valid on orders of $75.00 or more. Items in the sports gear product category are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q2e1bf6c54c",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Pebblestone Garden",
   "FINE_PRINT": "*Excludes open box items."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q5afb3f72ec",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Order by 3 August 2026 at the latest. The order subtotal must be above $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q539d63a053",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*The order subtotal must be above $200.00. Orders delivered to Arvale are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q044b77e3a0",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Excludes delivery to Arvale. Orders must be placed earlier than 12 February 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q64ed397038",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Oakhurst Interiors",
   "FINE_PRINT": "*Valid for orders placed on or after 28 February 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qe8e6598e34",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Excludes delivery to Dunmere. Valid for orders placed on or after 1 November 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q9d14aa99e2",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Harborlight Goods",
   "FINE_PRINT": "*Items in the kitchenware product category are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q7f4bce06c7",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Fernway Market",
   "FINE_PRINT": "*Valid only for orders delivered to Arvale."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q410739c128",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Members at the Basic level or lower only. Items sold as pre-order are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q62ae5d73a0",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Minimum order subtotal: $150.00. Excludes pre-order items."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4d41e12675",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Juniper Gadgets",
   "FINE_PRINT": "*Items sold as open box are excluded. Delivery to Fallowmere only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qd247178279",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Excludes delivery to Hollin."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q8fe20575b5",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Wrenfield Outdoor",
   "FINE_PRINT": "*For Plus members and above. Excludes delivery to Dunmere."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q5c37c02fca",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Valid only for items in the bedding category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q427ed86ee6",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*The order subtotal must be above $200.00. Excludes the bedding category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qf3a6722a2b",
  "brief": "write one text; register format: a promotional text message: one or two short sentences",
  "register": "sms",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Order by 31 March 2026 at the latest. Delivery to Calderon only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 }
]
