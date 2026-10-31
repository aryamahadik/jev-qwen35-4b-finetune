# T07 redo2 authoring task T07-author_lexicon-fe87c60e-000 (kind author_lexicon)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo2/answers/T07-author_lexicon-fe87c60e-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 4 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "forms". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits). The qids of this task: q9143f63a0f, q5520d76d47, qdaaa5bb537, q4b9e7913ad.
- "forms": a JSON list of strings, exactly as many as the item asks for. Outputs per item: 6.
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal shape (the qid shown is the first real one): [{"qid": "q9143f63a0f", "forms": ["<sentence 1>", "<sentence 2>", ...]}, ...]

Task kind: author_lexicon; items: 4; outputs expected: 24.

## Instructions

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: write SMALL-PRINT SENTENCES. Each item states one exact meaning, the placeholder {X} and what {X} stands for;
write the number of different sentences it asks for, all with exactly that meaning. Each sentence must work on its own
as one sentence of an advertisement's small print, directly after the symbol *.

Hard rules (a program checks every sentence; a sentence that breaks one is thrown away):
1. Exactly one placeholder {X}, spelled exactly so; no other placeholder and no real value in its place.
2. One sentence: a capital letter (or {X}) first, a full stop at the end, no other full stop, 2-14 words.
3. The meaning must be unmistakable to any careful reader, exactly at the edge case the item names.
4. No digits, number words (billion, dozen, dozens, eight, eighteen, eighth, eighty, eleven, fifteen, fifth, fifty, first, five, forty, four, fourteen, fourth, half, hundred, million, nine, nineteen, ninety, ninth, one, second, seven, seventeen, seventh, seventy, six, sixteen, sixth, sixty, ten, tenth, third, thirteen, thirty, thousand, three, thrice, twelve, twenty, twice, two, zero), names, hedges (allegedly, almost, apparently, approximately, believe, guess, likely, maybe, nearly, perhaps, possibly, presumably, probably, reportedly, roughly, seem, seemed, seemingly, seems, somewhat, supposedly, suspect, think, uncertain, unlikely, unsure).
5. No negation: not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, free of, no longer, fail to, neglect to, omit to, decline to, prevent ... from, rule out. Exclusion verbs (excludes, excluded) and the word "only" are fine.
6. None of these words: beginning, between, billed, billing, but, coupon, coupons, discount, discounts, either, ends, except, excepting, expires, if, otherwise, starting, tax, taxes, through, thru, till, total, unless, until, when, whenever, while, within. The word "or" only directly inside an inclusive comparison
   (or more, or less, or higher, or lower, or above, or below, on or before, on or after); never "or any".
7. Say who or what the line is for only with the frames the item lists (its rules). Use no other verb or adjective
   for who may receive the offer.
8. Talk only about the item's subject: membership sentences use "members", "member", "membership" or "level";
   price-status sentences name the status with the word "status", or with "priced as" or "pricing" (never the word
   "category", never the word "price"); delivery-region sentences say delivery, deliver, delivered, ship or shipped
   (never "shipping"). Words of one subject never appear in a sentence about another subject.
9. Words you must never use (any letter case), because each names a value (a region, product category, price status
   or membership level) or a headline offer. The list also holds ordinary words (colours, rooms, materials, places, goods, ranks and so on) because each is a membership level, a delivery region or a product category in some shop's advertisements; avoid every one of them, also in another form (plural, past tense):
acre, adult, alder, aldrusk, alvinmere, ambrewick, ammerlund, animal, animals, antique, appliance, appliances, apprentice, ardenbeck, ardenhaw, area, art, arvale, assemble, assembled, assembly, aubrenne, baby, backpacks, bags, baking, ballet, balloons, balsa, barrel, basic, bats, beacon, beagle, beans, bed, bedding, bellarow, bexterne, bib, bikes, birch, bird, black, blackout, blaze, blinds, blue, board, boards, bobbin, bolt, bonfire, bonsai, books, boots, bottles, boulder, box, boxes, brannoch, brass, brelmont, brenmoor, bricks, bridle, bright, brilliant, brisenhold, brisnell, brocade, brogue, bronze, brushes, bruvellan, building, bulbs, bungalow, bush, caddamore, caddies, caddowen, caddy, cadet, cadvane, cake, calderon, camera, candle, candles, canister, canvas, car, card, cards, carpets, cases, casserole, cat, cauldron, cedar, ceramic, chairs, champion, chef, chest, chrome, circular, clearance, clutch, cob, cobalt, cobble, collections, coltrissa, commodore, compost, cookbooks, cooling, cordless, corrimbe, corrowen, corundum, corvania, cosmetic, cottage, cotton, cottrowe, covers, cressmoor, cricket, crochet, crossinde, cruiser, cumbrel, cup, curtains, cushions, cycling, decks, dendrithe, denim, desk, diamond, dim, dishes, dog, door, doorbells, dosserley, double, dravenmoor, drills, drum, drumavel, dryers, duffel, dunlorn, dunmere, dunsarre, duvet, eddamore, eldrinde, electronics, elite, ellsward, elm, enamel, ensign, eskarra, eskarth, espresso, esterwold, exercise, fabrics, fallowmere, fallowry, fans, fastoway, feed, feeding, feldspar, felgrove, fencing, fenmoral, fenrald, ferrandy, ferrowick, filters, final, fishing, fitted, floor, foam, foreman, fountain, frames, free, fruit, frying, fulcrane, furniture, gallandry, gallon, games, garden, garnet, garrowen, garrowmere, gear, gentrell, gift, gifts, gigabyte, gildenvar, girder, glaspeck, glass, glossopane, goggles, gold, gorrimel, gorrowick, graphics, green, greeting, greyhaven, grove, hair, haldrecourt, hallowmere, halvedon, hamster, hardback, harlovia, harnethy, hartsinde, hatchling, hazel, heads, heat, hebrondell, hedge, heirloom, helmets, hendrimoor, herbal, heslecourt, hesmere, hiking, hobwinter, hollin, holvarden, hooks, horse, houseplants, hunter, ibbsdale, iltorvan, ilverine, imbrook, infant, infusions, install, installation, installed, iron, irrenwood, isarvel, jackets, jacquenay, jerrevine, jerseys, jessmere, jessvelle, jigsaw, journeyman, junior, juvenile, kellandra, kelvarn, kelvarra, kenvaris, kerrawick, kestrand, kilobyte, king, kiravel, kirrensey, kitchenware, kits, knight, knives, lace, lamp, lamps, lantern, lanterne, larch, lead, ledger, lens, lenses, leotards, lifetime, line, linen, linings, liskamber, litter, livestock, loafer, loom, lorvane, lounge, lumbardine, lures, lusterne, lusvale, machines, mandreth, manor, mansion, maple, marlin, marrowen, match, matched, matching, mats, maxi, meadow, megabyte, megalith, memo, memory, mennoway, midi, mini, minnow, mirrors, mirrovane, mirrowen, mixers, model, modules, moissanite, mollinsk, mordane, morrandy, morvane, morvendy, morvenlea, motion, mouldings, mount, murdrowe, nail, needles, net, nethermoor, netherstay, newborn, nickel, oak, olmerow, olvanne, open, ophelmar, organisers, orsovane, osmeldine, osterlin, ostravelle, ostrelle, ostrenn, overlock, oxford, pad, padlocks, pads, paint, paints, pallador, pamphlet, pandrey, pans, paper, paperback, parasol, pascombe, patio, pawn, peak, pebble, pelladine, pelvarin, pencil, pendant, pendrake, pennavey, pennoval, pennyrigge, pens, pentavel, pet, picture, pillowcases, pillows, pinch, pip, plants, plates, platinum, plot, plus, plush, poetry, point, points, polish, pomerant, pony, power, pre-order, premier, pressure, price, puzzles, pyrendal, quamberly, quarrowby, quart, quartz, queen, quendral, quenmere, quillandra, quillmarsh, quilting, rabbit, racer, rackets, radiant, rain, ranch, ranger, ravenelle, ravenholt, redwood, refurbished, regular, rendavy, retro, return, returns, revenhall, reward, rewards, rhomsby, ridge, ripple, road, roasted, roller, rook, rookie, room, roskenwald, rowan, rowanvarre, ruddlemoor, rugs, runner, ruthvane, sablewyn, sachet, saddle, sale, salmon, sample, sandals, sapling, satchel, saucepans, savarno, saws, scout, screws, sculdry, seats, seed, sellinor, senior, sensors, sequoia, seratine, sets, sewing, shades, shag, sheets, shipping, shoes, shorts, shower, shrub, sideboards, siderhald, sidrana, silicone, silver, single, skateboard, skillet, skirts, sleeping, slipper, smart, somberlyn, sorrenvale, sorvell, spark, spatulas, spool, sport, sports, sprig, sprout, spruce, stand, stands, stavanderly, stenvoy, stockpot, strategy, substrates, suitcases, suldane, sulvoy, summit, sundervell, supplies, surf, swell, swim, sylvandre, syndarra, tables, tackle, tamberley, tap, tape, tarvendell, tavistry, tea, teldoray, tembrick, tennis, tents, teranwold, tessimere, tester, tharvoll, thessory, thimble, thread, throw, tibbery, tins, tiransk, tiverlin, toasters, toddler, tools, topaz, toppers, torwick, touring, townhouse, toys, trail, trainers, travel, treats, trees, trenhollow, trevalick, tripod, trousers, trout, trunk, tungsten, tuskerly, tutu, ulvarren, umbrenne, units, vaelbrook, vallowry, vanity, varrowby, vases, velthorn, velunda, velvet, ventrine, veteran, video, villa, vintage, voile, wall, wallpaper, warmblood, warranties, warranty, warrenvale, washers, washi, water, wax, wendlark, wessenmoor, wessinde, wetsuits, wilmarrow, wingback, wipes, wire, wood, woodland, wool, work, worsted, worvinde, wrap, wrapped, wrapping, wrenhaddow, wylbourne, yarn, yarrowdene, yolstrand, ysmarre, zantaru, zelvane
10. All sentences in your answer differ clearly; do not copy the example.
11. Before you write the answer, check every word of every text against the word lists above and replace any word that is listed.

## Items (4; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q9143f63a0f",
  "brief": {
   "how_many": 6,
   "style": "terse small-print style, like a printed footnote",
   "x_stands_for": "the price status of the item (a status such as 'clearance', 'final sale' or 'open box')",
   "example": "Excludes stock with {X} status."
  },
  "meaning": "items with the named price status are excluded from the headline benefit; edge case: an item with the {X} status is outside; items with any other status are inside",
  "slots": {
   "X": "the price status of the item (a status such as 'clearance', 'final sale' or 'open box')"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop",
   "Name the status with the word 'status', or with 'priced as' or 'pricing'",
   "Say the items are out only with one of: 'excludes', 'is excluded', 'are excluded', 'falls outside', 'fall outside', 'sits outside', 'sit outside', 'is withheld from', 'are withheld from'",
   "Never the word 'category' and never the word 'price'"
  ]
 },
 {
  "qid": "q5520d76d47",
  "brief": {
   "how_many": 6,
   "style": "a fuller plain-English sentence",
   "x_stands_for": "the price status of the item (a status such as 'clearance', 'final sale' or 'open box')",
   "example": "Any item with {X} status falls outside this offer."
  },
  "meaning": "items with the named price status are excluded from the headline benefit; edge case: an item with the {X} status is outside; items with any other status are inside",
  "slots": {
   "X": "the price status of the item (a status such as 'clearance', 'final sale' or 'open box')"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop",
   "Name the status with the word 'status', or with 'priced as' or 'pricing'",
   "Say the items are out only with one of: 'excludes', 'is excluded', 'are excluded', 'falls outside', 'fall outside', 'sits outside', 'sit outside', 'is withheld from', 'are withheld from'",
   "Never the word 'category' and never the word 'price'"
  ]
 },
 {
  "qid": "qdaaa5bb537",
  "brief": {
   "how_many": 6,
   "style": "terse small-print style, like a printed footnote",
   "x_stands_for": "a membership level name (such as 'Gold'); levels are ranked lowest to highest",
   "example": "Reserved for {X} members and below."
  },
  "meaning": "the customer's membership level must be the named level or a lower one; edge case: a member AT level {X} is INSIDE; lower levels are inside; higher levels are outside",
  "slots": {
   "X": "a membership level name (such as 'Gold'); levels are ranked lowest to highest"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop",
   "Say who the line is for only with one of these frames: 'For ...', 'Applies to ...', 'Reserved for ...', 'Limited to ...', 'Restricted to ...'",
   "Name the members with 'members', 'member', 'membership' or 'level', and give the edge with 'or lower', 'or below', 'and below' or 'and lower' right after the level",
   "No other verb or adjective for who may receive the offer"
  ]
 },
 {
  "qid": "q4b9e7913ad",
  "brief": {
   "how_many": 6,
   "style": "a fuller plain-English sentence",
   "x_stands_for": "a membership level name (such as 'Gold'); levels are ranked lowest to highest",
   "example": "This offer applies to members at the {X} level or lower."
  },
  "meaning": "the customer's membership level must be the named level or a lower one; edge case: a member AT level {X} is INSIDE; lower levels are inside; higher levels are outside",
  "slots": {
   "X": "a membership level name (such as 'Gold'); levels are ranked lowest to highest"
  },
  "rules": [
   "6 sentences",
   "{X} exactly once",
   "one sentence each, ending with a full stop",
   "Say who the line is for only with one of these frames: 'For ...', 'Applies to ...', 'Reserved for ...', 'Limited to ...', 'Restricted to ...'",
   "Name the members with 'members', 'member', 'membership' or 'level', and give the edge with 'or lower', 'or below', 'and below' or 'and lower' right after the level",
   "No other verb or adjective for who may receive the offer"
  ]
 }
]
```
