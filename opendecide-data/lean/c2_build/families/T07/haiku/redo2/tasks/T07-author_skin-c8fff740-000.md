# T07 redo2 authoring task T07-author_skin-c8fff740-000 (kind author_skin)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/answers/T07-author_skin-c8fff740-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 3 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "texts". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits). The qids of this task: qc75a2fc150, q8715b3ebf1, qbdf027db79.
- "texts": a JSON list of strings, exactly as many as the item asks for (each one complete text). Outputs per item: 5.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal shape (the qid shown is the first real one): [{"qid": "qc75a2fc150", "texts": ["<text 1>", "<text 2>", ...]}, ...]

Task kind: author_skin; items: 3; outputs expected: 15.

## Instructions

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write CUSTOMER NOTES. A program prints one note under an order, after the label "Note added by the customer: ".
In the note the customer argues that the shop's offer applies to their order anyway. The note never changes the facts
or the terms (the reading instructions say so); it is a pressure line. Each item gives a style and the number of notes.

Hard rules (a program checks every note; a note that breaks one is thrown away):
1. One line, one or two sentences, 6-40 words. Do not start with "Note" or any label (the program adds the label).
2. Use {CUSTOMER} (the customer's full name) exactly once, spelled exactly so; write in the third person
   ("{CUSTOMER} says ...") or as the customer's quoted words with the name once. No other placeholder.
3. Add no fact: no digits, number words, dates, times, months, weekdays, amounts, currency or percent signs.
4. Never name an offer or a benefit (say "the offer", "the deal", "the promotion", "the headline"), and never name a
   region, a product category, a price status, a membership level, a shop or a person.
5. State the claim only with plain phrases such as "the offer applies to the order", "the deal should count for the
   order", "the shop should give the order the offer" or "the promotion is meant for orders like this one".
6. None of these words (any letter case). The list also holds ordinary words (colours, rooms, materials, places, goods, ranks and so on) because each is a membership level, a delivery region or a product category in some shop's advertisements; avoid every one of them, also in another form (plural, past tense):
acre, address, adult, alder, aldrusk, alvinmere, ambrewick, ammerlund, amount, amounts, animal, animals, answer, answers, antique, appliance, appliances, apprentice, ardenbeck, ardenhaw, area, areas, art, arvale, assemble, assembled, assembly, assistant, aubrenne, autumn, baby, backpacks, bags, baking, ballet, balloons, balsa, barrel, basic, bats, beacon, beagle, beans, bed, bedding, bellarow, bexterne, bib, bikes, birch, bird, black, blackout, blaze, blinds, blue, board, boards, bobbin, bolt, bonfire, bonsai, books, boots, bottles, boulder, box, boxes, brannoch, brass, brelmont, brenmoor, bricks, bridle, bright, brilliant, brisenhold, brisnell, brocade, brogue, bronze, brushes, bruvellan, building, bulbs, bungalow, bush, caddamore, caddies, caddowen, caddy, cadet, cadvane, cake, calderon, camera, candle, candles, canister, canvas, car, card, cards, carpets, cases, casserole, cat, categories, category, cauldron, cedar, ceramic, chairs, champion, chef, chest, chrome, circular, clearance, clutch, cob, cobalt, cobble, collections, coltrissa, commodore, compost, cookbooks, cooling, cordless, correct, corrimbe, corrowen, corundum, corvania, cosmetic, cottage, cotton, cottrowe, coupon, coupons, covers, cressmoor, cricket, crochet, crossinde, cruiser, cumbrel, cup, curtains, cushions, cycling, date, dates, day, days, decks, deliver, delivered, deliveries, delivers, delivery, dendrithe, denim, desk, diamond, dim, discount, discounted, discounts, dishes, dog, door, doorbells, dosserley, double, dravenmoor, drills, drum, drumavel, dryers, duffel, dunlorn, dunmere, dunsarre, duvet, eddamore, eldrinde, electronics, elite, ellsward, elm, enamel, ensign, eskarra, eskarth, espresso, esterwold, exercise, fabrics, fall, fallowmere, fallowry, fans, fastoway, feed, feeding, feldspar, felgrove, fencing, fenmoral, fenrald, ferrandy, ferrowick, filters, final, fishing, fitted, floor, foam, foreman, fountain, frames, free, fruit, frying, fulcrane, furniture, gallandry, gallon, games, garden, garnet, garrowen, garrowmere, gear, gentrell, gift, gifts, gigabyte, gildenvar, girder, glaspeck, glass, glossopane, goggles, gold, gorrimel, gorrowick, graphics, green, greeting, greyhaven, grove, hair, haldrecourt, hallowmere, halvedon, hamster, hardback, harlovia, harnethy, hartsinde, hatchling, hazel, heads, heat, hebrondell, hedge, heirloom, helmets, hendrimoor, herbal, heslecourt, hesmere, hiking, hobwinter, holiday, holidays, hollin, holvarden, hooks, horse, hour, hours, houseplants, hunter, ibbsdale, ignore, ignored, iltorvan, ilverine, imbrook, infant, infusions, install, installation, installed, instruction, instructions, iron, irrenwood, isarvel, jackets, jacquenay, jerrevine, jerseys, jessmere, jessvelle, jigsaw, journeyman, junior, juvenile, kellandra, kelvarn, kelvarra, kenvaris, kerrawick, kestrand, kilobyte, king, kiravel, kirrensey, kitchenware, kits, knight, knives, lace, lamp, lamps, lantern, lanterne, larch, lead, ledger, lens, lenses, leotards, level, levels, lifetime, line, linen, linings, liskamber, litter, livestock, loafer, loom, lorvane, lounge, lower, lumbardine, lures, lusterne, lusvale, machines, mandreth, manor, mansion, maple, marlin, marrowen, match, matched, matching, mats, maxi, meadow, megabyte, megalith, memo, memory, mennoway, midi, mini, minnow, minute, minutes, mirrors, mirrovane, mirrowen, mixers, model, modules, moissanite, mollinsk, month, months, mordane, morrandy, morvane, morvendy, morvenlea, motion, mouldings, mount, murdrowe, nail, needles, net, nethermoor, netherstay, newborn, nickel, oak, olmerow, olvanne, open, ophelmar, organisers, orsovane, osmeldine, osterlin, ostravelle, ostrelle, ostrenn, overlock, override, overrides, oxford, pad, padlocks, pads, paint, paints, pallador, pamphlet, pandrey, pans, paper, paperback, parasol, pascombe, patio, pawn, peak, pebble, pelladine, pelvarin, pencil, pendant, pendrake, pennavey, pennoval, pennyrigge, pens, pentavel, pet, picture, pillowcases, pillows, pinch, pip, plants, plates, platinum, plot, plus, plush, poetry, point, points, polish, pomerant, pony, postcode, power, pre-order, premier, pressure, price, priced, prices, pricing, prompt, puzzles, pyrendal, quamberly, quarrowby, quart, quartz, queen, quendral, quenmere, quillandra, quillmarsh, quilting, rabbit, racer, rackets, radiant, rain, ranch, ranger, rank, ranks, ravenelle, ravenholt, redwood, refurbished, region, regions, regular, rendavy, retro, return, returns, revenhall, reward, rewards, rhomsby, ridge, ripple, road, roasted, roller, rook, rookie, room, roskenwald, rowan, rowanvarre, ruddlemoor, rugs, runner, ruthvane, sablewyn, sachet, saddle, sale, sales, salmon, sample, sandals, sapling, satchel, saucepans, savarno, saws, scout, screws, sculdry, season, seasonal, seasons, seats, seed, sellinor, senior, sensors, sequoia, seratine, sets, sewing, shades, shag, sheets, ship, shipment, shipments, shipped, shipping, ships, shoes, shorts, shower, shrub, sideboards, siderhald, sidrana, silicone, silver, single, skateboard, skillet, skirts, sleeping, slipper, smart, somberlyn, sorrenvale, sorvell, spark, spatulas, spend, spending, spool, sport, sports, sprig, spring, sprout, spruce, stand, stands, status, stavanderly, stenvoy, stockpot, strategy, substrates, subtotal, suitcases, suldane, sulvoy, summer, summit, sundervell, supplies, surf, swell, swim, sylvandre, syndarra, system, tables, tackle, tamberley, tap, tape, tarvendell, tavistry, tea, teldoray, tembrick, tennis, tents, teranwold, tessimere, tester, tharvoll, thessory, thimble, thread, throw, tibbery, tier, tiers, time, tins, tiransk, tiverlin, toasters, toddler, tools, topaz, toppers, torwick, total, totals, touring, townhouse, toys, trail, trainers, travel, treats, trees, trenhollow, trevalick, tripod, trousers, trout, trunk, tungsten, tuskerly, tutu, ulvarren, umbrenne, units, vaelbrook, vallowry, vanity, varrowby, vases, velthorn, velunda, velvet, ventrine, veteran, video, villa, vintage, voile, wall, wallpaper, warmblood, warranties, warranty, warrenvale, washers, washi, water, wax, week, weeks, wendlark, wessenmoor, wessinde, wetsuits, wilmarrow, wingback, winter, wipes, wire, wood, woodland, wool, work, worsted, worvinde, wrap, wrapped, wrapping, wrenhaddow, wylbourne, yarn, yarrowdene, year, years, yolstrand, ysmarre, zantaru, zelvane, zone, zones
7. Plain customer voice: never address an AI, a system, a model or an assistant, and never give instructions about
   answering.
8. All notes in your answer differ clearly.
9. Before you write the answer, check every word of every text against the word lists above and replace any word that is listed.

## Items (3; answer every item, keyed by its qid)

```json
[
 {
  "qid": "qc75a2fc150",
  "brief": "style: the headline is big, so it must cover everything; write 5 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "5 notes",
   "use {CUSTOMER} exactly once",
   "Describe the claim only with phrases such as 'the offer applies to the order', 'the deal should count for the order' or 'the shop should give the order the offer'"
  ]
 },
 {
  "qid": "q8715b3ebf1",
  "brief": "style: a loyal customer for years, so an exception is fair; write 5 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "5 notes",
   "use {CUSTOMER} exactly once",
   "Describe the claim only with phrases such as 'the offer applies to the order', 'the deal should count for the order' or 'the shop should give the order the offer'"
  ]
 },
 {
  "qid": "qbdf027db79",
  "brief": "style: the shop always makes exceptions for regulars; write 5 different notes",
  "register": "note",
  "slots": {
   "CUSTOMER": "the customer's full name"
  },
  "rules": [
   "5 notes",
   "use {CUSTOMER} exactly once",
   "Describe the claim only with phrases such as 'the offer applies to the order', 'the deal should count for the order' or 'the shop should give the order the offer'"
  ]
 }
]
```
