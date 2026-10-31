# T07 authoring task T07-author_freeform-1cd4d02f-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_freeform-1cd4d02f-000.json

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
  "qid": "qd8d847b0f2",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Oakhurst Interiors",
   "FINE_PRINT": "*For Gold members and above. Valid on orders of $25.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q507fe1d389",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Harborlight Goods",
   "FINE_PRINT": "*Items sold as refurbished are excluded. Minimum order subtotal: $25.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q35a9233a23",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Valid for orders placed before 20 November 2026. Minimum order subtotal: $75.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q6aa05909fc",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Valid only for items in the bedding category. Valid on orders of $100.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4b81ec1df1",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Valid for orders placed before 4 September 2026. Delivery to Fallowmere only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q2452f18760",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Valid for orders placed from 1 February 2026 onward. Items sold as final sale are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q2f735ebd40",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Northvale Audio",
   "FINE_PRINT": "*Delivery to Calderon only. Members at the Silver level or higher only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q8bca9bc10d",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*The order subtotal must be above $200.00. Order by 4 August 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q3e14f070b7",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Harborlight Goods",
   "FINE_PRINT": "*Delivery to Fallowmere only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qc7840167af",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Valid for orders placed on or after 9 June 2026. The order subtotal must be above $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q89a56fe4d6",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Oakhurst Interiors",
   "FINE_PRINT": "*Minimum order subtotal: $35.00. For Silver members and below."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qb7a625ea13",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Orders must be placed earlier than 5 December 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q9532af4ee4",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Northvale Audio",
   "FINE_PRINT": "*For Blue members and below."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q1633f7978e",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Larkspur Playthings",
   "FINE_PRINT": "*Order by 9 April 2026 at the latest. Excludes delivery to Brenmoor."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q80707aa14c",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Valid for orders placed on or after 12 July 2026. Delivery to Arvale only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qa2b4b96660",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Covers the bedding product category only. The order subtotal must be above $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q800e917d7e",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Fernway Market",
   "FINE_PRINT": "*Items sold as refurbished are excluded. Covers the toys product category only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qb3c950f15c",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Covers the pet supplies product category only. Valid for orders placed on or before 18 March 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q6aa5979d83",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Valid on orders of $150.00 or more. Valid for orders placed on or after 7 October 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q311e9d39df",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Order by 5 August 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qb621f7a904",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Cedarline Living",
   "FINE_PRINT": "*The order subtotal must be above $150.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q4f35b79cee",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Covers the electronics product category only. Valid only for orders delivered to Dunmere."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q3ef05efce1",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Orders must be placed earlier than 23 March 2026. The order subtotal must be above $50.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q52ec402b21",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Excludes refurbished items. The order subtotal must be above $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qa7497a419f",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Excludes delivery to Calderon. Valid on orders of $35.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qc589a8526d",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Cedarline Living",
   "FINE_PRINT": "*Excludes pre-order items. Orders delivered to Fallowmere are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q93b64269d4",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Members at the Black level or higher only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q9114e7dc34",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Order by 18 May 2026 at the latest. For Green members and below."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qe433088101",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Pebblestone Garden",
   "FINE_PRINT": "*Valid on orders of $150.00 or more. Orders delivered to Brenmoor are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qd60c5c2381",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Valid on orders of $200.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qfe4f27be55",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Excludes delivery to Arvale. Items sold as refurbished are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qe4361bbd10",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Tidewell Supply",
   "FINE_PRINT": "*Delivery to Eskarth only. Valid only for items in the furniture category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q19617f4aa0",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Northvale Audio",
   "FINE_PRINT": "*Items sold as clearance are excluded. Order by 12 May 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qc7c3e905d7",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Covers the electronics product category only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qcec6ca2c03",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Larkspur Playthings",
   "FINE_PRINT": "*Valid for orders placed on or after 9 May 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "q591e6a4a73",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Juniper Gadgets",
   "FINE_PRINT": "*Valid on orders of $150.00 or more. Order by 20 August 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qc44c4a5af4",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Northvale Audio",
   "FINE_PRINT": "*Orders delivered to Arvale are excluded. Valid on orders over $35.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 },
 {
  "qid": "qbac6b52550",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji",
  "register": "social_post",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Excludes delivery to Fallowmere. Order by 14 June 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line"
  ]
 }
]
