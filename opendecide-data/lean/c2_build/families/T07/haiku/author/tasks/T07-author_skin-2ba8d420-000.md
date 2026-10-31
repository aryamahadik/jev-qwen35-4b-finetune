# T07 authoring task T07-author_skin-2ba8d420-000

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/author/answers/T07-author_skin-2ba8d420-000.json

Task kind: author_skin; items: 8; outputs expected: 40.

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write AD COPY TEMPLATES in the register "catalogue": the opening blurb of a printed catalogue: a heading line, then one or two sentences.
This is the general, friendly part of a shop's advertisement. Elsewhere on the page a program prints the shop's
headline offers, their small print and the customer's order, so your text adds no fact, no offer and no condition of
its own: it welcomes the reader, talks about the shop and its range in general terms, and names the shop once.

Placeholder: use {STORE} (the shop's name) EXACTLY ONCE, spelled exactly so with its curly braces; no other
placeholder, and never a shop name of your own. Never put "a", "an" or "the" directly before {STORE}.

Hard rules (a text that breaks one is thrown away):
1. One block of text, never an empty line; single line breaks only where the register needs them. Length: 8-60 words
   (shelf tags: 2-15 words).
2. Outside the placeholder: no digits, number words or ordinals, no dates, times, months, weekdays or time words, no
   currency or percent signs, no web or e-mail addresses.
3. Outside the placeholder, none of these words (any letter case):
- number: billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero
- relative time: afternoon, afterwards, ago, already, annually, asap, currently, daily, earlier, evening, formerly, hourly, immediately, last, lately, later, midday, midnight, monthly, morning, next, night, noon, now, overdue, overnight, past, previously, recently, shortly, soon, today, tomorrow, tonight, upcoming, weekend, weekly, yearly, yesterday, yet
- quantity: additional, another, bulk, bunch, couple, double, entire, entirely, extra, few, fewer, fewest, handful, least, less, lots, majority, many, maximum, minimum, minority, more, most, much, multiple, numerous, pair, partial, partially, percent, percentage, plenty, quarter, several, single, total, triple, various, whole
- quantifier: all, always, any, anybody, anyone, anything, both, each, either, every, everybody, everyone, everything, neither, never, no, nobody, none, nothing, often, only, rarely, seldom, some, somebody, someone, something, sometimes, usually, whenever
- modal: able, allowed, can, cannot, could, forbidden, gotta, mandatory, may, might, must, mustn, need, needed, needs, optional, ought, permitted, prohibited, required, shall, should, shouldn, unable, will, would
- hedge: allegedly, almost, apparently, appear, appeared, appears, approximately, assume, assumed, assumes, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure
- status: accept, accepted, active, allow, allowed, approval, approve, approved, authorised, authorized, block, blocked, breached, broken, cancel, canceled, cancelled, closed, complete, completed, compliant, confirm, confirmation, confirmed, delivered, denial, denied, deny, done, eligibility, expire, expired, fail, failed, failure, fake, finished, fraud, fraudulent, genuine, grant, granted, inactive, invalid, kept, late, legitimate, noncompliant, ok, okay, open, opened, outstanding, paid, pending, processed, queued, refund, refunded, reject, rejected, resolved, revoke, revoked, settled, succeeded, success, successful, successfully, superseded, unauthorised, unauthorized, unpaid, unresolved, unverified, valid, verified, void, waive, waived
- operator: except, excluding, if, instead, otherwise, provided, providing, regardless, unless
- phrases: have to, has to, had to, got to, sort of, kind of
4. Words you must never use outside the placeholder (any letter case), because they would state an offer or a condition, or name what the small print talks about:
above, address, after, amount, amounts, appliance, appliances, applied, applies, apply, area, areas, arvale, assemble, assembled, assembly, asterisk, autumn, basic, bedding, before, below, black, blue, box, brenmoor, bronze, calderon, categories, category, clearance, condition, conditions, coupon, coupons, date, dates, day, days, deadline, deliver, delivered, deliveries, delivers, delivery, detail, details, discount, discounted, discounts, double, dunmere, electronics, elite, ending, ends, eskarth, every, exclude, excluded, excludes, excluding, exclusion, exclusions, exclusive, exclusively, expire, expires, expiry, fall, fallowmere, final, fine, footnote, footnotes, free, freely, furniture, garden, gear, gift, gifts, gold, green, greyhaven, holiday, holidays, hollin, hour, hours, install, installation, installed, kitchenware, level, levels, lifetime, limit, limited, lower, match, matched, matching, maximum, member, members, membership, minimum, minute, minutes, month, months, only, open, over, pet, platinum, plus, point, points, postcode, pre-order, premier, price, priced, prices, pricing, print, qualifying, rank, ranks, refurbished, region, regions, regular, restricted, restriction, restrictions, return, returns, reward, rewards, sale, sales, season, seasonal, seasons, select, selected, ship, shipment, shipments, shipped, shipping, ships, silver, spend, spending, sports, spring, status, subtotal, summer, supplies, term, terms, through, tier, tiers, till, time, tools, total, totals, toys, under, until, valid, validity, warranties, warranty, week, weeks, while, winter, wrap, wrapped, wrapping, year, years, zone, zones
5. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
6. Capital letters only at the start of a sentence, a line or a label such as "Subject:"; no names of people, places,
   brands, products or membership levels.
7. Never say or hint who gets what: no promise of any benefit, nothing about earning, claiming or deserving anything.
8. Never use the symbols * or †, and never mention small print, footnotes, terms or conditions.
9. The texts of one item differ clearly in wording and structure, and differ from the example. Do not copy the example.

Example(s) of the register (for format only; JSON strings as you would write them in your answer):
  "Inside this catalogue\nOur buyers at {STORE} picked practical designs and honest materials for everyday life."
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]
Copy each qid exactly. Give exactly the number of outputs each item asks for.

ITEMS (JSON; answer every item, keyed by its qid):
[
 {
  "qid": "qe6f005a639",
  "brief": "tone: polished and confident; format: the opening blurb of a printed catalogue: a heading line, then one or two sentences; write 5 different texts",
  "register": "catalogue",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "5 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q904c6c6e68",
  "brief": "tone: practical and down to earth; format: the opening blurb of a printed catalogue: a heading line, then one or two sentences; write 5 different texts",
  "register": "catalogue",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "5 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q6fac44c876",
  "brief": "tone: family-friendly; format: the opening blurb of a printed catalogue: a heading line, then one or two sentences; write 5 different texts",
  "register": "catalogue",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "5 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q37b092a05f",
  "brief": "tone: playful and light; format: the opening blurb of a printed catalogue: a heading line, then one or two sentences; write 5 different texts",
  "register": "catalogue",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "5 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q725f646de4",
  "brief": "tone: neighbourly, small-shop feel; format: the opening blurb of a printed catalogue: a heading line, then one or two sentences; write 5 different texts",
  "register": "catalogue",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "5 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q5c40d0d2c7",
  "brief": "tone: brisk and modern; format: the opening blurb of a printed catalogue: a heading line, then one or two sentences; write 5 different texts",
  "register": "catalogue",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "5 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "qff12532da8",
  "brief": "tone: warm and welcoming; format: the opening blurb of a printed catalogue: a heading line, then one or two sentences; write 5 different texts",
  "register": "catalogue",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "5 texts, each clearly different from the others"
  ]
 },
 {
  "qid": "q52bc55054c",
  "brief": "tone: calm and premium; format: the opening blurb of a printed catalogue: a heading line, then one or two sentences; write 5 different texts",
  "register": "catalogue",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "5 texts, each clearly different from the others"
  ]
 }
]
