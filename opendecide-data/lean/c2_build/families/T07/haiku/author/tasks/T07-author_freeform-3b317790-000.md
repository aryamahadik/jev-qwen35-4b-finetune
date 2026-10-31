# T07 authoring task T07-author_freeform-3b317790-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_freeform-3b317790-000.json

Task kind: author_freeform; items: 30; outputs expected: 30.

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
  "qid": "q0c926eecb4",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*Items sold as open box are excluded. The order subtotal must be above $75.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q5f3aab08d7",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Quaymoor Traders",
   "FINE_PRINT": "*Excludes delivery to Greyhaven."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4d16a68f1b",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Valid on orders of $50.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q6929cc6d61",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Thistledown Supply",
   "FINE_PRINT": "*Delivery to Hollin only. Valid on orders of $75.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q1b9b9d71d8",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Quaymoor Traders",
   "FINE_PRINT": "*Excludes refurbished items. Minimum order subtotal: $35.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q2f8f325055",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Thistledown Supply",
   "FINE_PRINT": "*Order by 31 July 2026 at the latest. Valid on orders of $200.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4851361057",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*Orders must be placed earlier than 28 April 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qe3f4e8eb81",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*Valid on orders over $25.00. Excludes open box items."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4bcd49255e",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Quaymoor Traders",
   "FINE_PRINT": "*Valid on orders of $25.00 or more. Order by 14 May 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qedd7334f89",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*The order subtotal must be above $35.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qc411c6d3bd",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Minimum order subtotal: $50.00. Items sold as pre-order are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qe6f97cf382",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*Valid on orders of $35.00 or more. Excludes delivery to Fallowmere."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q33de384259",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*Excludes final sale items. Orders delivered to Arvale are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q1b80d22d98",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*Items sold as pre-order are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q2b6084bb62",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Excludes delivery to Greyhaven. Valid on orders of $200.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qb66d74e860",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Quaymoor Traders",
   "FINE_PRINT": "*Orders delivered to Calderon are excluded. Items sold as final sale are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q6416dd0b00",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Excludes open box items. Valid only for orders delivered to Arvale."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q1218175d6e",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Thistledown Supply",
   "FINE_PRINT": "*For Premier members and below."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q154ba1496e",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Thistledown Supply",
   "FINE_PRINT": "*Excludes pre-order items. Valid for orders placed on or before 7 July 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q94f9571772",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Items in the bedding product category are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q8f5beeddc2",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Thistledown Supply",
   "FINE_PRINT": "*Valid only for orders delivered to Calderon."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q3c82edd241",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Thistledown Supply",
   "FINE_PRINT": "*Valid on orders of $75.00 or more. For Plus members and above."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q50dfd8eda3",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Quaymoor Traders",
   "FINE_PRINT": "*Covers the electronics product category only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4daebd0869",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Order by 1 June 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q40f062b6cb",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Members at the Platinum level or higher only. Minimum order subtotal: $150.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q6fe5242d0f",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*Valid on orders of $150.00 or more. Delivery to Dunmere only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q3e55a5de25",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*Delivery to Fallowmere only. Excludes refurbished items."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q89ecffa814",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Valid for orders placed on or after 4 June 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q9337151515",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Elmstead Emporium",
   "FINE_PRINT": "*For Platinum members and above."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q2af2bb58d0",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences",
  "register": "voice_promo",
  "facts": {
   "STORE": "Thistledown Supply",
   "FINE_PRINT": "*Order by 18 May 2026 at the latest. Items sold as pre-order are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 }
]
