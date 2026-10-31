# T07 redo2 authoring task T07-author_skin-d31228b4-002 (kind author_skin)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/answers/T07-author_skin-d31228b4-002.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 10 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "texts". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits). The qids of this task: qc090b22166, q874a2c8206, q40c9ba42e7, qd84b4276a9, q7640fdfdfc, q599b4d1c13, q58c34a8f68, q54d9c64d96, q76cb3e70f1, qe911ba48c0.
- "texts": a JSON list of strings, exactly as many as the item asks for (each one complete text). Outputs per item: 4.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal shape (the qid shown is the first real one): [{"qid": "qc090b22166", "texts": ["<text 1>", "<text 2>", ...]}, ...]

Task kind: author_skin; items: 10; outputs expected: 40.

## Instructions

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write AD COPY TEMPLATES. Each item names a register (the kind of text), its format, a tone and how many texts to
write. This is the general, friendly part of a shop's advertisement. Elsewhere on the page a program prints the shop's
headline offers, their small print and the customer's order, so your text adds no fact, no offer and no condition of
its own: it welcomes the reader, talks about the shop and its range in general terms, and names the shop once.

Placeholder: use {STORE} (the shop's name) EXACTLY ONCE, spelled exactly so with its curly braces; no other
placeholder, and never a shop name of your own. Never put "a", "an" or "the" directly before {STORE}.

Hard rules (a program checks every text; a text that breaks one is thrown away):
1. One block of text, never an empty line; single line breaks only where the register needs them. Length: 8-60 words
   (shelf_tag: 2-15 words).
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
4. Words you must never use outside the placeholder (any letter case), because they would state an offer or a
   condition, or name what the small print talks about. The list also holds ordinary words (colours, rooms, materials, places, goods, ranks and so on) because each is a membership level, a delivery region or a product category in some shop's advertisements; avoid every one of them, also in another form (plural, past tense):
above, acre, address, adult, after, alder, aldrusk, alvinmere, ambrewick, ammerlund, amount, amounts, animal, animals, antique, appliance, appliances, applied, applies, apply, apprentice, ardenbeck, ardenhaw, area, areas, art, arvale, assemble, assembled, assembly, asterisk, aubrenne, autumn, baby, backpacks, bags, baking, ballet, balloons, balsa, barrel, basic, bats, beacon, beagle, beans, bed, bedding, before, bellarow, below, bexterne, bib, bikes, birch, bird, black, blackout, blaze, blinds, blue, board, boards, bobbin, bolt, bonfire, bonsai, books, boots, bottles, boulder, box, boxes, brannoch, brass, brelmont, brenmoor, bricks, bridle, bright, brilliant, brisenhold, brisnell, brocade, brogue, bronze, brushes, bruvellan, building, bulbs, bungalow, bush, caddamore, caddies, caddowen, caddy, cadet, cadvane, cake, calderon, camera, candle, candles, canister, canvas, car, card, cards, carpets, cases, casserole, cat, categories, category, cauldron, cedar, ceramic, chairs, champion, chef, chest, chrome, circular, clearance, clutch, cob, cobalt, cobble, collections, coltrissa, commodore, compost, condition, conditions, cookbooks, cooling, cordless, corrimbe, corrowen, corundum, corvania, cosmetic, cottage, cotton, cottrowe, coupon, coupons, covers, cressmoor, cricket, crochet, crossinde, cruiser, cumbrel, cup, curtains, cushions, cycling, date, dates, day, days, deadline, decks, deliver, delivered, deliveries, delivers, delivery, dendrithe, denim, desk, detail, details, diamond, dim, discount, discounted, discounts, dishes, dog, door, doorbells, dosserley, double, dravenmoor, drills, drum, drumavel, dryers, duffel, dunlorn, dunmere, dunsarre, duvet, eddamore, eldrinde, electronics, elite, ellsward, elm, enamel, ending, ends, ensign, eskarra, eskarth, espresso, esterwold, every, exclude, excluded, excludes, excluding, exclusion, exclusions, exclusive, exclusively, exercise, expire, expires, expiry, fabrics, fall, fallowmere, fallowry, fans, fastoway, feed, feeding, feldspar, felgrove, fencing, fenmoral, fenrald, ferrandy, ferrowick, filters, final, fine, fishing, fitted, floor, foam, footnote, footnotes, foreman, fountain, frames, free, freely, fruit, frying, fulcrane, furniture, gallandry, gallon, games, garden, garnet, garrowen, garrowmere, gear, gentrell, gift, gifts, gigabyte, gildenvar, girder, glaspeck, glass, glossopane, goggles, gold, gorrimel, gorrowick, graphics, green, greeting, greyhaven, grove, hair, haldrecourt, hallowmere, halvedon, hamster, hardback, harlovia, harnethy, hartsinde, hatchling, hazel, heads, heat, hebrondell, hedge, heirloom, helmets, hendrimoor, herbal, heslecourt, hesmere, hiking, hobwinter, holiday, holidays, hollin, holvarden, hooks, horse, hour, hours, houseplants, hunter, ibbsdale, iltorvan, ilverine, imbrook, infant, infusions, install, installation, installed, iron, irrenwood, isarvel, jackets, jacquenay, jerrevine, jerseys, jessmere, jessvelle, jigsaw, journeyman, junior, juvenile, kellandra, kelvarn, kelvarra, kenvaris, kerrawick, kestrand, kilobyte, king, kiravel, kirrensey, kitchenware, kits, knight, knives, lace, lamp, lamps, lantern, lanterne, larch, lead, ledger, lens, lenses, leotards, level, levels, lifetime, limit, limited, line, linen, linings, liskamber, litter, livestock, loafer, loom, lorvane, lounge, lower, lumbardine, lures, lusterne, lusvale, machines, mandreth, manor, mansion, maple, marlin, marrowen, match, matched, matching, mats, maxi, maximum, meadow, megabyte, megalith, member, members, membership, memo, memory, mennoway, midi, mini, minimum, minnow, minute, minutes, mirrors, mirrovane, mirrowen, mixers, model, modules, moissanite, mollinsk, month, months, mordane, morrandy, morvane, morvendy, morvenlea, motion, mouldings, mount, murdrowe, nail, needles, net, nethermoor, netherstay, newborn, nickel, oak, olmerow, olvanne, only, open, ophelmar, organisers, orsovane, osmeldine, osterlin, ostravelle, ostrelle, ostrenn, over, overlock, oxford, pad, padlocks, pads, paint, paints, pallador, pamphlet, pandrey, pans, paper, paperback, parasol, pascombe, patio, pawn, peak, pebble, pelladine, pelvarin, pencil, pendant, pendrake, pennavey, pennoval, pennyrigge, pens, pentavel, pet, picture, pillowcases, pillows, pinch, pip, plants, plates, platinum, plot, plus, plush, poetry, point, points, polish, pomerant, pony, postcode, power, pre-order, premier, pressure, price, priced, prices, pricing, print, puzzles, pyrendal, qualifying, quamberly, quarrowby, quart, quartz, queen, quendral, quenmere, quillandra, quillmarsh, quilting, rabbit, racer, rackets, radiant, rain, ranch, ranger, rank, ranks, ravenelle, ravenholt, redwood, refurbished, region, regions, regular, rendavy, restricted, restriction, restrictions, retro, return, returns, revenhall, reward, rewards, rhomsby, ridge, ripple, road, roasted, roller, rook, rookie, room, roskenwald, rowan, rowanvarre, ruddlemoor, rugs, runner, ruthvane, sablewyn, sachet, saddle, sale, sales, salmon, sample, sandals, sapling, satchel, saucepans, savarno, saws, scout, screws, sculdry, season, seasonal, seasons, seats, seed, select, selected, sellinor, senior, sensors, sequoia, seratine, sets, sewing, shades, shag, sheets, ship, shipment, shipments, shipped, shipping, ships, shoes, shorts, shower, shrub, sideboards, siderhald, sidrana, silicone, silver, single, skateboard, skillet, skirts, sleeping, slipper, smart, somberlyn, sorrenvale, sorvell, spark, spatulas, spend, spending, spool, sport, sports, sprig, spring, sprout, spruce, stand, stands, status, stavanderly, stenvoy, stockpot, strategy, substrates, subtotal, suitcases, suldane, sulvoy, summer, summit, sundervell, supplies, surf, swell, swim, sylvandre, syndarra, tables, tackle, tamberley, tap, tape, tarvendell, tavistry, tea, teldoray, tembrick, tennis, tents, teranwold, term, terms, tessimere, tester, tharvoll, thessory, thimble, thread, through, throw, tibbery, tier, tiers, till, time, tins, tiransk, tiverlin, toasters, toddler, tools, topaz, toppers, torwick, total, totals, touring, townhouse, toys, trail, trainers, travel, treats, trees, trenhollow, trevalick, tripod, trousers, trout, trunk, tungsten, tuskerly, tutu, ulvarren, umbrenne, under, units, until, vaelbrook, valid, validity, vallowry, vanity, varrowby, vases, velthorn, velunda, velvet, ventrine, veteran, video, villa, vintage, voile, wall, wallpaper, warmblood, warranties, warranty, warrenvale, washers, washi, water, wax, week, weeks, wendlark, wessenmoor, wessinde, wetsuits, while, wilmarrow, wingback, winter, wipes, wire, wood, woodland, wool, work, worsted, worvinde, wrap, wrapped, wrapping, wrenhaddow, wylbourne, yarn, yarrowdene, year, years, yolstrand, ysmarre, zantaru, zelvane, zone, zones
5. No negation at all: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
6. Capital letters only at the start of a sentence, a line or a label such as "Subject:"; no names of people, places,
   brands, products or membership levels.
7. Never say or hint who gets what: no promise of any benefit, nothing about earning, claiming, deserving or keeping
   anything. To thank or welcome the reader, use only plain words such as "thank you", "thanks", "welcome", "we are glad" and "we appreciate".
8. Never use the symbols * or †, and never mention small print, footnotes, terms or conditions.
9. The texts of one item differ clearly in wording and structure, and differ from the register's example. Do not copy
   an example.
10. Before you write the answer, check every word of every text against the word lists above and replace any word that is listed.

Register formats and examples (for format only; JSON strings as you would write them in your answer):
- web_banner: a website banner: one or two short sentences of welcome copy. Example: "Welcome to {STORE}. Browse the range, compare styles side by side and find a favourite for your home."
- app_banner: a mobile app banner: a short title line and a short subtitle line. Example: "Fresh arrivals at {STORE}\nTap to browse the range and save the pieces you like."
- flyer: a printed flyer: a short heading line, then one or two sentences. Example: "Come and see us\nThe team at {STORE} is happy to help you find the right fit for your plans."
- catalogue: the opening blurb of a printed catalogue: a heading line, then one or two sentences. Example: "Inside this catalogue\nOur buyers at {STORE} picked practical designs and honest materials for everyday life."
- checkout_note: a note shown on a checkout page: one or two sentences thanking the shopper or inviting them to review their basket. Example: "Thank you for shopping with {STORE}. Please take a moment to check your basket."
- email_promo: a promotional e-mail: a line starting with 'Subject:', then a greeting and one or two sentences. Example: "Subject: Hello from {STORE}\nHello, our new range has arrived. Browse it online and treat yourself to a piece you love."
- sms: a promotional text message: one or two short sentences. Example: "{STORE}: new arrivals are in. Tap the link in your account to browse."
- social_post: a social media post: one to three short sentences, no hashtags, no emoji. Example: "Our shelves are stocked and our team loves good design. Come and say hello at {STORE}!"
- warranty_card: a product-care card that comes in the box with a purchase: one to three sentences about caring for the product and thanking the customer (never use the word warranty). Example: "Thank you for choosing {STORE}. Keep this card with your receipt and wipe the surface with a soft dry cloth."
- loyalty_newsletter: the opening of a customer newsletter: a heading line, then one or two sentences. Example: "News from {STORE}\nThis issue looks at the people behind our favourite products."
- shelf_tag: a shelf tag next to a product: a very short line (two to fifteen words). Example: "A shopper favourite at {STORE}"
- app_banner, JSON form (where the item says so): a mobile app banner written as a JSON object with exactly the keys "title", "subtitle" and "button" (three short strings); {STORE} sits inside one of the strings. Example: "{\"title\": \"Fresh arrivals at {STORE}\", \"subtitle\": \"Tap to browse the range\", \"button\": \"Take a look\"}"

## Items (10; answer every item, keyed by its qid)

```json
[
 {
  "qid": "qc090b22166",
  "brief": "register: shelf_tag; format: a shelf tag next to a product: a very short line (two to fifteen words); tone: warm and welcoming; write 4 different texts",
  "register": "shelf_tag",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "q874a2c8206",
  "brief": "register: social_post; format: a social media post: one to three short sentences, no hashtags, no emoji; tone: playful and light; write 4 different texts",
  "register": "social_post",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "q40c9ba42e7",
  "brief": "register: social_post; format: a social media post: one to three short sentences, no hashtags, no emoji; tone: polished and confident; write 4 different texts",
  "register": "social_post",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "qd84b4276a9",
  "brief": "register: flyer; format: a printed flyer: a short heading line, then one or two sentences; tone: polished and confident; write 4 different texts",
  "register": "flyer",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "q7640fdfdfc",
  "brief": "register: email_promo; format: a promotional e-mail: a line starting with 'Subject:', then a greeting and one or two sentences; tone: practical and down to earth; write 4 different texts",
  "register": "email_promo",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "q599b4d1c13",
  "brief": "register: sms; format: a promotional text message: one or two short sentences; tone: neighbourly, small-shop feel; write 4 different texts",
  "register": "sms",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "q58c34a8f68",
  "brief": "register: app_banner; format: a mobile app banner written as a JSON object with exactly the keys \"title\", \"subtitle\" and \"button\" (three short strings); {STORE} sits inside one of the strings; tone: practical and down to earth; write 4 different texts",
  "register": "app_banner",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "q54d9c64d96",
  "brief": "register: warranty_card; format: a product-care card that comes in the box with a purchase: one to three sentences about caring for the product and thanking the customer (never use the word warranty); tone: brisk and modern; write 4 different texts",
  "register": "warranty_card",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "q76cb3e70f1",
  "brief": "register: sms; format: a promotional text message: one or two short sentences; tone: family-friendly; write 4 different texts",
  "register": "sms",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 },
 {
  "qid": "qe911ba48c0",
  "brief": "register: warranty_card; format: a product-care card that comes in the box with a purchase: one to three sentences about caring for the product and thanking the customer (never use the word warranty); tone: warm and welcoming; write 4 different texts",
  "register": "warranty_card",
  "slots": {
   "STORE": "the shop's name"
  },
  "rules": [
   "use {STORE} exactly once",
   "4 texts, each clearly different from the others",
   "check every word against the word lists before answering"
  ]
 }
]
```
