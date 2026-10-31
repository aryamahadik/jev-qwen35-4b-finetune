# T07 redo2 authoring task T07-author_wording-ba3a46c7-000 (kind author_wording)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/answers/T07-author_wording-ba3a46c7-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 10 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "wordings". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits). The qids of this task: q95f5c194e7, q7ff7f34ff0, q702d053a6f, qf72a61dd9e, q74c6d338d8, qdead9551de, q349bd13564, q60ac7fb4e2, qc951b4db2c, q40c91cca49.
- "wordings": a JSON list of strings, exactly as many as the item asks for. Outputs per item: 4.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal shape (the qid shown is the first real one): [{"qid": "q95f5c194e7", "wordings": ["<question 1>", "<question 2>", ...]}, ...]

Task kind: author_wording; items: 10; outputs expected: 40.

## Instructions

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

Hard rules (a program checks every wording; a wording that breaks one is thrown away):
1. One question, 6-30 words, ending with "?". Use each placeholder the item lists exactly once, spelled exactly so with
   its curly braces: {CUSTOMER} (the customer's full name), {ORDER_ID} (the order's code) and, where listed,
   {ASKED} (the name of one advertised benefit, such as 'free returns' or 'the price match'). Never put "a", "an" or
   "the" directly before {ASKED}.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it. Use only the verbs the item
   allows for the outcome.
3. Negation exactly as the item says and nowhere else. The full list of negation words is: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out.
4. No digits, number words, dates, names, hedges (maybe, probably, seems, think, believe, likely) or time words (now,
   currently, already, soon, yet, today, next, last). Capital letter only on the first word.
5. Never name a benefit, a region, a product category, a price status, a membership level, an amount or a date (the
   placeholders carry them), and never list answer choices. None of these words (any letter case). The list also holds ordinary words (colours, rooms, materials, places, goods, ranks and so on) because each is a membership level, a delivery region or a product category in some shop's advertisements; avoid every one of them, also in another form (plural, past tense):
   acre, adult, alder, aldrusk, alvinmere, ambrewick, ammerlund, animal, animals, antique, appliance, appliances, apprentice, ardenbeck, ardenhaw, area, art, arvale, assemble, assembled, assembly, aubrenne, baby, backpacks, bags, baking, ballet, balloons, balsa, barrel, basic, bats, beacon, beagle, beans, bed, bedding, bellarow, bexterne, bib, bikes, birch, bird, black, blackout, blaze, blinds, blue, board, boards, bobbin, bolt, bonfire, bonsai, books, boots, bottles, boulder, box, boxes, brannoch, brass, brelmont, brenmoor, bricks, bridle, bright, brilliant, brisenhold, brisnell, brocade, brogue, bronze, brushes, bruvellan, building, bulbs, bungalow, bush, caddamore, caddies, caddowen, caddy, cadet, cadvane, cake, calderon, camera, candle, candles, canister, canvas, car, card, cards, carpets, cases, casserole, cat, cauldron, cedar, ceramic, chairs, champion, chef, chest, chrome, circular, clearance, clutch, cob, cobalt, cobble, collections, coltrissa, commodore, compost, cookbooks, cooling, cordless, corrimbe, corrowen, corundum, corvania, cosmetic, cottage, cotton, cottrowe, covers, cressmoor, cricket, crochet, crossinde, cruiser, cumbrel, cup, curtains, cushions, cycling, decks, delivery, dendrithe, denim, desk, diamond, dim, dishes, dog, door, doorbells, dosserley, double, dravenmoor, drills, drum, drumavel, dryers, duffel, dunlorn, dunmere, dunsarre, duvet, eddamore, eldrinde, electronics, elite, ellsward, elm, enamel, ensign, eskarra, eskarth, espresso, esterwold, exercise, fabrics, fallowmere, fallowry, fans, fastoway, feed, feeding, feldspar, felgrove, fencing, fenmoral, fenrald, ferrandy, ferrowick, filters, final, fishing, fitted, floor, foam, foreman, fountain, frames, free, fruit, frying, fulcrane, furniture, gallandry, gallon, games, garden, garnet, garrowen, garrowmere, gear, gentrell, gift, gifts, gigabyte, gildenvar, girder, glaspeck, glass, glossopane, goggles, gold, gorrimel, gorrowick, graphics, green, greeting, greyhaven, grove, hair, haldrecourt, hallowmere, halvedon, hamster, hardback, harlovia, harnethy, hartsinde, hatchling, hazel, heads, heat, hebrondell, hedge, heirloom, helmets, hendrimoor, herbal, heslecourt, hesmere, hiking, hobwinter, hollin, holvarden, hooks, horse, houseplants, hunter, ibbsdale, iltorvan, ilverine, imbrook, infant, infusions, install, installation, installed, iron, irrenwood, isarvel, jackets, jacquenay, jerrevine, jerseys, jessmere, jessvelle, jigsaw, journeyman, junior, juvenile, kellandra, kelvarn, kelvarra, kenvaris, kerrawick, kestrand, kilobyte, king, kiravel, kirrensey, kitchenware, kits, knight, knives, lace, lamp, lamps, lantern, lanterne, larch, lead, ledger, lens, lenses, leotards, lifetime, line, linen, linings, liskamber, litter, livestock, loafer, loom, lorvane, lounge, lower, lumbardine, lures, lusterne, lusvale, machines, mandreth, manor, mansion, maple, marlin, marrowen, match, matched, matching, mats, maxi, meadow, megabyte, megalith, memo, memory, mennoway, midi, mini, minnow, mirrors, mirrovane, mirrowen, mixers, model, modules, moissanite, mollinsk, mordane, morrandy, morvane, morvendy, morvenlea, motion, mouldings, mount, murdrowe, nail, needles, net, nethermoor, netherstay, newborn, nickel, oak, olmerow, olvanne, open, ophelmar, organisers, orsovane, osmeldine, osterlin, ostravelle, ostrelle, ostrenn, overlock, oxford, pad, padlocks, pads, paint, paints, pallador, pamphlet, pandrey, pans, paper, paperback, parasol, pascombe, patio, pawn, peak, pebble, pelladine, pelvarin, pencil, pendant, pendrake, pennavey, pennoval, pennyrigge, pens, pentavel, pet, picture, pillowcases, pillows, pinch, pip, plants, plates, platinum, plot, plus, plush, poetry, point, points, polish, pomerant, pony, power, pre-order, premier, pressure, price, puzzles, pyrendal, quamberly, quarrowby, quart, quartz, queen, quendral, quenmere, quillandra, quillmarsh, quilting, rabbit, racer, rackets, radiant, rain, ranch, ranger, ravenelle, ravenholt, redwood, refurbished, regular, rendavy, retro, return, returns, revenhall, reward, rewards, rhomsby, ridge, ripple, road, roasted, roller, rook, rookie, room, roskenwald, rowan, rowanvarre, ruddlemoor, rugs, runner, ruthvane, sablewyn, sachet, saddle, sale, salmon, sample, sandals, sapling, satchel, saucepans, savarno, saws, scout, screws, sculdry, seats, seed, sellinor, senior, sensors, sequoia, seratine, sets, sewing, shades, shag, sheets, shipping, shoes, shorts, shower, shrub, sideboards, siderhald, sidrana, silicone, silver, single, skateboard, skillet, skirts, sleeping, slipper, smart, somberlyn, sorrenvale, sorvell, spark, spatulas, spool, sport, sports, sprig, sprout, spruce, stand, stands, stavanderly, stenvoy, stockpot, strategy, substrates, suitcases, suldane, sulvoy, summit, sundervell, supplies, surf, swell, swim, sylvandre, syndarra, tables, tackle, tamberley, tap, tape, tarvendell, tavistry, tea, teldoray, tembrick, tennis, tents, teranwold, tessimere, tester, tharvoll, thessory, thimble, thread, throw, tibbery, tins, tiransk, tiverlin, toasters, toddler, tools, topaz, toppers, torwick, touring, townhouse, toys, trail, trainers, travel, treats, trees, trenhollow, trevalick, tripod, trousers, trout, trunk, tungsten, tuskerly, tutu, ulvarren, umbrenne, units, vaelbrook, vallowry, vanity, varrowby, vases, velthorn, velunda, velvet, ventrine, veteran, video, villa, vintage, voile, wall, wallpaper, warmblood, warranties, warranty, warrenvale, washers, washi, water, wax, wendlark, wessenmoor, wessinde, wetsuits, wilmarrow, wingback, wipes, wire, wood, woodland, wool, work, worsted, worvinde, wrap, wrapped, wrapping, wrenhaddow, wylbourne, yarn, yarrowdene, yolstrand, ysmarre, zantaru, zelvane.
   A question about which condition is missed also avoids these words: address, amount, amounts, area, areas, autumn, categories, category, clearance, coupon, coupons, date, dates, day, days, deliver, delivered, deliveries, delivers, delivery, discount, discounted, discounts, fall, holiday, holidays, hour, hours, level, levels, minute, minutes, month, months, postcode, price, priced, prices, pricing, rank, ranks, region, regions, sale, sales, season, seasonal, seasons, ship, shipment, shipments, shipped, shipping, ships, spend, spending, spring, status, subtotal, summer, tier, tiers, time, total, totals, week, weeks, winter, year, years, zone, zones.
6. Tie the question to the advertisement as the item's style says, and vary the structure across your wordings (who
   is the subject: the customer, the order, the advertisement; short and long forms).
7. Before you write the answer, check every word of every text against the word lists above and replace any word that is listed.

## Items (10; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q95f5c194e7",
  "brief": {
   "meaning": "which of the advertised headline offers does order {ORDER_ID} from {CUSTOMER} actually get, once each offer's own small print is applied? The reader picks from a list shown after the question, so the question names no outcome (never the words both, neither, only, all, none, either, each, every) and has no negation word",
   "style": "refer to 'the advertisement and its fine print'",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q7ff7f34ff0",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the advertised terms? For the outcome use exactly one of these two verbs, in any tense: 'lose out on' (loses out on, lost out on) or 'forfeit' (forfeits, forfeited). No other verb for the outcome, and NO negation word at all (not 'without', not 'denied', not 'fail')",
   "style": "formal, mentioning the advertisement's conditions in general",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q702d053a6f",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the promotion's terms? For the outcome use exactly one of these two verbs, in any tense: 'lose out on' (loses out on, lost out on) or 'forfeit' (forfeits, forfeited). No other verb for the outcome, and NO negation word at all (not 'without', not 'denied', not 'fail')",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "qf72a61dd9e",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the advertised terms? For the outcome use exactly one of these two verbs, in any tense: 'lose out on' (loses out on, lost out on) or 'forfeit' (forfeits, forfeited). No other verb for the outcome, and NO negation word at all (not 'without', not 'denied', not 'fail')",
   "style": "refer to 'the advertisement and its fine print'",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q74c6d338d8",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the advertised terms? For the outcome use exactly one of these two verbs, in any tense: 'lose out on' (loses out on, lost out on) or 'forfeit' (forfeits, forfeited). No other verb for the outcome, and NO negation word at all (not 'without', not 'denied', not 'fail')",
   "style": "refer to 'what the advertisement says'",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "qdead9551de",
  "brief": {
   "meaning": "which single condition in the small print attached to {ASKED} does order {ORDER_ID} from {CUSTOMER} miss, IF ANY? The reader picks from a list shown after the question that also has a choice for 'every condition is met', so the question must allow that no condition is missed: include 'if any' (or 'if there is one'). Never assume a condition is missed, never name a condition or a kind of condition, no negation word",
   "style": "refer to 'the advertisement and its fine print'",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q349bd13564",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the advertised terms? For the outcome use exactly one of these two verbs, in any tense: 'lose out on' (loses out on, lost out on) or 'forfeit' (forfeits, forfeited). No other verb for the outcome, and NO negation word at all (not 'without', not 'denied', not 'fail')",
   "style": "refer to 'the advertisement and its fine print'",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q60ac7fb4e2",
  "brief": {
   "meaning": "yes/no: does order {ORDER_ID} from {CUSTOMER} lose out on {ASKED} under the promotion's terms? For the outcome use exactly one of these two verbs, in any tense: 'lose out on' (loses out on, lost out on) or 'forfeit' (forfeits, forfeited). No other verb for the outcome, and NO negation word at all (not 'without', not 'denied', not 'fail')",
   "style": "call the advertisement 'the promotion' (or 'the promo') and its small print 'the footnotes'; never use the words advertisement, advertised, ad, fine print or small print",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "qc951b4db2c",
  "brief": {
   "meaning": "which single condition in the small print attached to {ASKED} does order {ORDER_ID} from {CUSTOMER} miss, IF ANY? The reader picks from a list shown after the question that also has a choice for 'every condition is met', so the question must allow that no condition is missed: include 'if any' (or 'if there is one'). Never assume a condition is missed, never name a condition or a kind of condition, no negation word",
   "style": "refer to 'what the advertisement says'",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code",
   "ASKED": "the name of one advertised benefit"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 },
 {
  "qid": "q40c91cca49",
  "brief": {
   "meaning": "which of the advertised headline offers does order {ORDER_ID} from {CUSTOMER} actually get, once each offer's own small print is applied? The reader picks from a list shown after the question, so the question names no outcome (never the words both, neither, only, all, none, either, each, every) and has no negation word",
   "style": "refer to 'what the advertisement says'",
   "how_many": 4
  },
  "slots": {
   "CUSTOMER": "the customer's full name",
   "ORDER_ID": "the order's code"
  },
  "rules": [
   "4 wordings with exactly this meaning",
   "each listed placeholder exactly once"
  ]
 }
]
```
