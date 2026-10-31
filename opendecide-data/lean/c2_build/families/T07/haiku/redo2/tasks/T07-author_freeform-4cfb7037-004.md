# T07 redo2 authoring task T07-author_freeform-4cfb7037-004 (kind author_freeform)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/answers/T07-author_freeform-4cfb7037-004.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 38 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "text". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits). The qids of this task: q94a3d7ed29, q1ba8ea6f79, qb0cb4fa857, q155f9c4b82, q5a212a02e7, q596ec5af6a, qf9e72e705c, q51baeb8ab5, qc0c626fe60, qbff679cdd8, qd423a7869e, qeb40e6af86, qf9d9e2ea38, q054d96a3d5, q2941d4b623, q8a72715407, qceced448ea, qecc431fc3b, qd130579bff, q2c40b3d9a6, qd794f3539e, qc972e8ba80, qb51d1a491e, q695ad0b43e, q45f039d922, q8c5028e717, qc6b0c0a31b, q6d3f596d02, qe1a36cb881, qc76e98b5f0, q8f36b05467, q101ee0228f, qb87fe641ff, qaab1727253, qd587b3e2c5, q456e9aadb2, q86560c55be, q36d331c04d.
- "text": one JSON string (the whole text; write a line break as \n).
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal shape (the qid shown is the first real one): [{"qid": "q94a3d7ed29", "text": "<the text>"}, ...]

Task kind: author_freeform; items: 38; outputs expected: 38.

## Instructions

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write one short ADVERTISEMENT TEXT per item, in the item's register and tone, from the facts given. The text has
two parts: a BODY you write, then the SMALL PRINT, which is the FINE_PRINT fact copied character for character.

Hard rules (a program checks every text; a text that breaks one is thrown away):
1. The body names the shop exactly once, with the STORE fact written exactly as given (same letters and capitals).
2. End the text with the FINE_PRINT fact, copied exactly (same characters in the same order, starting with its *), on
   its own line after the body. It appears exactly once, and the * appears nowhere else.
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
7. Words you must never use in the body (any letter case), because they would state an offer or a condition, or name
   what the small print talks about. The list also holds ordinary words (colours, rooms, materials, places, goods, ranks and so on) because each is a membership level, a delivery region or a product category in some shop's advertisements; avoid every one of them, also in another form (plural, past tense). The FINE_PRINT may hold such words: the lists apply to the body only:
above, acre, address, adult, after, alder, aldrusk, alvinmere, ambrewick, ammerlund, amount, amounts, animal, animals, antique, appliance, appliances, applied, applies, apply, apprentice, ardenbeck, ardenhaw, area, areas, art, arvale, assemble, assembled, assembly, asterisk, aubrenne, autumn, baby, backpacks, bags, baking, ballet, balloons, balsa, barrel, basic, bats, beacon, beagle, beans, bed, bedding, before, bellarow, below, bexterne, bib, bikes, birch, bird, black, blackout, blaze, blinds, blue, board, boards, bobbin, bolt, bonfire, bonsai, books, boots, bottles, boulder, box, boxes, brannoch, brass, brelmont, brenmoor, bricks, bridle, bright, brilliant, brisenhold, brisnell, brocade, brogue, bronze, brushes, bruvellan, building, bulbs, bungalow, bush, caddamore, caddies, caddowen, caddy, cadet, cadvane, cake, calderon, camera, candle, candles, canister, canvas, car, card, cards, carpets, cases, casserole, cat, categories, category, cauldron, cedar, ceramic, chairs, champion, chef, chest, chrome, circular, clearance, clutch, cob, cobalt, cobble, collections, coltrissa, commodore, compost, condition, conditions, cookbooks, cooling, cordless, corrimbe, corrowen, corundum, corvania, cosmetic, cottage, cotton, cottrowe, coupon, coupons, covers, cressmoor, cricket, crochet, crossinde, cruiser, cumbrel, cup, curtains, cushions, cycling, date, dates, day, days, deadline, decks, deliver, delivered, deliveries, delivers, delivery, dendrithe, denim, desk, detail, details, diamond, dim, discount, discounted, discounts, dishes, dog, door, doorbells, dosserley, double, dravenmoor, drills, drum, drumavel, dryers, duffel, dunlorn, dunmere, dunsarre, duvet, eddamore, eldrinde, electronics, elite, ellsward, elm, enamel, ending, ends, ensign, eskarra, eskarth, espresso, esterwold, every, exclude, excluded, excludes, excluding, exclusion, exclusions, exclusive, exclusively, exercise, expire, expires, expiry, fabrics, fall, fallowmere, fallowry, fans, fastoway, feed, feeding, feldspar, felgrove, fencing, fenmoral, fenrald, ferrandy, ferrowick, filters, final, fine, fishing, fitted, floor, foam, footnote, footnotes, foreman, fountain, frames, free, freely, fruit, frying, fulcrane, furniture, gallandry, gallon, games, garden, garnet, garrowen, garrowmere, gear, gentrell, gift, gifts, gigabyte, gildenvar, girder, glaspeck, glass, glossopane, goggles, gold, gorrimel, gorrowick, graphics, green, greeting, greyhaven, grove, hair, haldrecourt, hallowmere, halvedon, hamster, hardback, harlovia, harnethy, hartsinde, hatchling, hazel, heads, heat, hebrondell, hedge, heirloom, helmets, hendrimoor, herbal, heslecourt, hesmere, hiking, hobwinter, holiday, holidays, hollin, holvarden, hooks, horse, hour, hours, houseplants, hunter, ibbsdale, iltorvan, ilverine, imbrook, infant, infusions, install, installation, installed, iron, irrenwood, isarvel, jackets, jacquenay, jerrevine, jerseys, jessmere, jessvelle, jigsaw, journeyman, junior, juvenile, kellandra, kelvarn, kelvarra, kenvaris, kerrawick, kestrand, kilobyte, king, kiravel, kirrensey, kitchenware, kits, knight, knives, lace, lamp, lamps, lantern, lanterne, larch, lead, ledger, lens, lenses, leotards, level, levels, lifetime, limit, limited, line, linen, linings, liskamber, litter, livestock, loafer, loom, lorvane, lounge, lower, lumbardine, lures, lusterne, lusvale, machines, mandreth, manor, mansion, maple, marlin, marrowen, match, matched, matching, mats, maxi, maximum, meadow, megabyte, megalith, member, members, membership, memo, memory, mennoway, midi, mini, minimum, minnow, minute, minutes, mirrors, mirrovane, mirrowen, mixers, model, modules, moissanite, mollinsk, month, months, mordane, morrandy, morvane, morvendy, morvenlea, motion, mouldings, mount, murdrowe, nail, needles, net, nethermoor, netherstay, newborn, nickel, oak, olmerow, olvanne, only, open, ophelmar, organisers, orsovane, osmeldine, osterlin, ostravelle, ostrelle, ostrenn, over, overlock, oxford, pad, padlocks, pads, paint, paints, pallador, pamphlet, pandrey, pans, paper, paperback, parasol, pascombe, patio, pawn, peak, pebble, pelladine, pelvarin, pencil, pendant, pendrake, pennavey, pennoval, pennyrigge, pens, pentavel, pet, picture, pillowcases, pillows, pinch, pip, plants, plates, platinum, plot, plus, plush, poetry, point, points, polish, pomerant, pony, postcode, power, pre-order, premier, pressure, price, priced, prices, pricing, print, puzzles, pyrendal, qualifying, quamberly, quarrowby, quart, quartz, queen, quendral, quenmere, quillandra, quillmarsh, quilting, rabbit, racer, rackets, radiant, rain, ranch, ranger, rank, ranks, ravenelle, ravenholt, redwood, refurbished, region, regions, regular, rendavy, restricted, restriction, restrictions, retro, return, returns, revenhall, reward, rewards, rhomsby, ridge, ripple, road, roasted, roller, rook, rookie, room, roskenwald, rowan, rowanvarre, ruddlemoor, rugs, runner, ruthvane, sablewyn, sachet, saddle, sale, sales, salmon, sample, sandals, sapling, satchel, saucepans, savarno, saws, scout, screws, sculdry, season, seasonal, seasons, seats, seed, select, selected, sellinor, senior, sensors, sequoia, seratine, sets, sewing, shades, shag, sheets, ship, shipment, shipments, shipped, shipping, ships, shoes, shorts, shower, shrub, sideboards, siderhald, sidrana, silicone, silver, single, skateboard, skillet, skirts, sleeping, slipper, smart, somberlyn, sorrenvale, sorvell, spark, spatulas, spend, spending, spool, sport, sports, sprig, spring, sprout, spruce, stand, stands, status, stavanderly, stenvoy, stockpot, strategy, substrates, subtotal, suitcases, suldane, sulvoy, summer, summit, sundervell, supplies, surf, swell, swim, sylvandre, syndarra, tables, tackle, tamberley, tap, tape, tarvendell, tavistry, tea, teldoray, tembrick, tennis, tents, teranwold, term, terms, tessimere, tester, tharvoll, thessory, thimble, thread, through, throw, tibbery, tier, tiers, till, time, tins, tiransk, tiverlin, toasters, toddler, tools, topaz, toppers, torwick, total, totals, touring, townhouse, toys, trail, trainers, travel, treats, trees, trenhollow, trevalick, tripod, trousers, trout, trunk, tungsten, tuskerly, tutu, ulvarren, umbrenne, under, units, until, vaelbrook, valid, validity, vallowry, vanity, varrowby, vases, velthorn, velunda, velvet, ventrine, veteran, video, villa, vintage, voile, wall, wallpaper, warmblood, warranties, warranty, warrenvale, washers, washi, water, wax, week, weeks, wendlark, wessenmoor, wessinde, wetsuits, while, wilmarrow, wingback, winter, wipes, wire, wood, woodland, wool, work, worsted, worvinde, wrap, wrapped, wrapping, wrenhaddow, wylbourne, yarn, yarrowdene, year, years, yolstrand, ysmarre, zantaru, zelvane, zone, zones
8. No negation in the body: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
9. Capital letters in the body only at the start of a sentence or a line (or a label such as "Subject:"), plus the
   shop's name.
10. To thank or welcome the reader, use only plain words such as "thank you", "thanks", "welcome", "we are glad" and "we appreciate". Never write that anyone or anything is respected, kept or valued.
11. Before you write the answer, check every word of every text against the word lists above and replace any word that is listed.

## Items (38; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q94a3d7ed29",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: neighbourly, small-shop feel",
  "register": "social_post",
  "facts": {
   "STORE": "Larkspur Playthings",
   "FINE_PRINT": "*Valid for orders placed on or after 9 May 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q1ba8ea6f79",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: brisk and modern",
  "register": "warranty_card",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Minimum order subtotal: $100.00. Excludes delivery to Hollin."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qb0cb4fa857",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: family-friendly",
  "register": "social_post",
  "facts": {
   "STORE": "Oakhurst Interiors",
   "FINE_PRINT": "*For Gold members and above. Valid on orders of $25.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q155f9c4b82",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences; tone: brisk and modern",
  "register": "voice_promo",
  "facts": {
   "STORE": "Quaymoor Traders",
   "FINE_PRINT": "*Covers the electronics product category only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q5a212a02e7",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: practical and down to earth",
  "register": "warranty_card",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Excludes items with open box status."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q596ec5af6a",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: warm and welcoming",
  "register": "warranty_card",
  "facts": {
   "STORE": "Pebblestone Garden",
   "FINE_PRINT": "*Items whose status is pre-order are excluded. Order by 12 March 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qf9e72e705c",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: polished and confident",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Valid on orders of $200.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q51baeb8ab5",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: polished and confident",
  "register": "warranty_card",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Excludes delivery to Greyhaven."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qc0c626fe60",
  "brief": "write one text; register format: a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences; tone: calm and premium",
  "register": "email_promo",
  "facts": {
   "STORE": "Wrenfield Outdoor",
   "FINE_PRINT": "*Valid for orders placed on or before 17 February 2026. Valid only for items in the garden tools category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qbff679cdd8",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: polished and confident",
  "register": "warranty_card",
  "facts": {
   "STORE": "Harborlight Goods",
   "FINE_PRINT": "*Valid on orders over $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qd423a7869e",
  "brief": "write one text; register format: a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences; tone: practical and down to earth",
  "register": "email_promo",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Order by 21 April 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qeb40e6af86",
  "brief": "write one text; register format: a promotional text message: one or two short sentences; tone: playful and light",
  "register": "sms",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Members at the Basic level or lower only. Excludes items with pre-order status."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qf9d9e2ea38",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: warm and welcoming",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Covers the pet supplies product category only. Valid for orders placed on or before 18 March 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q054d96a3d5",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: family-friendly",
  "register": "social_post",
  "facts": {
   "STORE": "Pebblestone Garden",
   "FINE_PRINT": "*Valid on orders of $150.00 or more. Orders delivered to Brenmoor are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q2941d4b623",
  "brief": "write one text; register format: a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences; tone: family-friendly",
  "register": "email_promo",
  "facts": {
   "STORE": "Pebblestone Garden",
   "FINE_PRINT": "*Excludes items with final sale status. For Green members and below."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q8a72715407",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: playful and light",
  "register": "warranty_card",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Minimum order subtotal: $100.00. Excludes delivery to Hollin."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qceced448ea",
  "brief": "write one text; register format: a promotional text message: one or two short sentences; tone: neighbourly, small-shop feel",
  "register": "sms",
  "facts": {
   "STORE": "Oakhurst Interiors",
   "FINE_PRINT": "*Valid only for orders delivered to Greyhaven. Items whose status is refurbished are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qecc431fc3b",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: warm and welcoming",
  "register": "warranty_card",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Valid on orders of $50.00 or more. Orders must be placed earlier than 14 January 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qd130579bff",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences; tone: calm and premium",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Order by 1 June 2026 at the latest."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q2c40b3d9a6",
  "brief": "write one text; register format: a promotional text message: one or two short sentences; tone: polished and confident",
  "register": "sms",
  "facts": {
   "STORE": "Juniper Gadgets",
   "FINE_PRINT": "*Items whose status is open box are excluded. Delivery to Fallowmere only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qd794f3539e",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: family-friendly",
  "register": "social_post",
  "facts": {
   "STORE": "Larkspur Playthings",
   "FINE_PRINT": "*Order by 9 April 2026 at the latest. Excludes delivery to Brenmoor."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qc972e8ba80",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: family-friendly",
  "register": "social_post",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Items whose status is refurbished are excluded. The order subtotal must be above $100.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qb51d1a491e",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: warm and welcoming",
  "register": "social_post",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Order by 18 May 2026 at the latest. For Green members and below."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q695ad0b43e",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: playful and light",
  "register": "social_post",
  "facts": {
   "STORE": "Bluecrest Sports",
   "FINE_PRINT": "*Valid only for items in the bedding category. Valid on orders of $100.00 or more."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q45f039d922",
  "brief": "write one text; register format: a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences; tone: practical and down to earth",
  "register": "email_promo",
  "facts": {
   "STORE": "Fernway Market",
   "FINE_PRINT": "*Valid only for orders delivered to Hollin. Excludes items with final sale status."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q8c5028e717",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences; tone: brisk and modern",
  "register": "voice_promo",
  "facts": {
   "STORE": "Quaymoor Traders",
   "FINE_PRINT": "*Orders delivered to Calderon are excluded. Excludes items with final sale status."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qc6b0c0a31b",
  "brief": "write one text; register format: a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences; tone: calm and premium",
  "register": "email_promo",
  "facts": {
   "STORE": "Fernway Market",
   "FINE_PRINT": "*Valid only for orders delivered to Hollin. Excludes items with final sale status."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q6d3f596d02",
  "brief": "write one text; register format: a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences; tone: neighbourly, small-shop feel",
  "register": "email_promo",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Valid only for orders delivered to Fallowmere. Minimum order subtotal: $50.00."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qe1a36cb881",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences; tone: calm and premium",
  "register": "voice_promo",
  "facts": {
   "STORE": "Rowanbrook Store",
   "FINE_PRINT": "*Minimum order subtotal: $50.00. Excludes items with pre-order status."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qc76e98b5f0",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: calm and premium",
  "register": "warranty_card",
  "facts": {
   "STORE": "Marigold Pets",
   "FINE_PRINT": "*Excludes delivery to Calderon. Valid for orders placed on or before 26 March 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q8f36b05467",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: family-friendly",
  "register": "warranty_card",
  "facts": {
   "STORE": "Kestrel Outfitters",
   "FINE_PRINT": "*Valid on orders of $50.00 or more. Orders must be placed earlier than 14 January 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q101ee0228f",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: brisk and modern",
  "register": "warranty_card",
  "facts": {
   "STORE": "Northvale Audio",
   "FINE_PRINT": "*Valid for orders placed from 21 May 2026 onward. Orders delivered to Hollin are excluded."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qb87fe641ff",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: calm and premium",
  "register": "social_post",
  "facts": {
   "STORE": "Brightwell Home",
   "FINE_PRINT": "*Valid for orders placed before 4 September 2026. Delivery to Fallowmere only."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qaab1727253",
  "brief": "write one text; register format: the script of a short spoken audio advert played in the shop or on local radio: two to four spoken sentences; tone: playful and light",
  "register": "voice_promo",
  "facts": {
   "STORE": "Thistledown Supply",
   "FINE_PRINT": "*Valid on orders of $75.00 or more. For Plus members and above."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "qd587b3e2c5",
  "brief": "write one text; register format: a product-care card that comes in the box: a few sentences about caring for the product and thanking the customer (never use the word warranty); tone: playful and light",
  "register": "warranty_card",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Excludes items with final sale status. Valid for orders placed on or after 27 October 2026."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q456e9aadb2",
  "brief": "write one text; register format: a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences; tone: calm and premium",
  "register": "email_promo",
  "facts": {
   "STORE": "Copperleaf Kitchen",
   "FINE_PRINT": "*Valid only for orders delivered to Fallowmere. Valid for orders placed from 2 May 2026 onward."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q86560c55be",
  "brief": "write one text; register format: a promotional e-mail: a line starting with 'Subject:', a greeting and a few sentences; tone: practical and down to earth",
  "register": "email_promo",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Valid on orders over $50.00. Valid only for items in the pet supplies category."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 },
 {
  "qid": "q36d331c04d",
  "brief": "write one text; register format: a social media post: two to four short sentences, no hashtags, no emoji; tone: practical and down to earth",
  "register": "social_post",
  "facts": {
   "STORE": "Birchwood Linens",
   "FINE_PRINT": "*Order by 18 May 2026 at the latest. For Green members and below."
  },
  "rules": [
   "the STORE fact exactly once, in the body",
   "the FINE_PRINT fact copied exactly, once, at the very end, on its own line",
   "check every word of the body against the word lists before answering"
  ]
 }
]
```
