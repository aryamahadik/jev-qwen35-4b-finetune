# T07 redo3 authoring task T07-author_pack-56620cf3-000 (kind author_pack)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/haiku/redo3/answers/T07-author_pack-56620cf3-000.json

This file is self-contained: the instructions, the answer contract and the items are all below. Read this whole file. Do not open, list or search any other file or folder.

ANSWER CONTRACT (exact; a program checks it):
- The answer file holds one JSON array with exactly 17 objects: one per item below, each item answered once.
- Each object has exactly two keys: "qid" and "pack". No other keys.
- "qid": copy the item's qid exactly, character for character (the letter q followed by ten letters or digits). The qids of this task: q77749ea2ca, q21a4354b41, q93210e65d6, qcc2ad5c5f8, qf329089aee, q7075764fed, q7fcdb23724, q3b77503b97, q5d48010c3a, q609204a03b, q0faa119172, qd627c2f0ee, q76424e22ec, q144e6093b8, q7fe74fd9b5, qefa100fd4c, q4f23a7a4f5.
- "pack": one JSON object with exactly these five keys: "store" (a string), "ladder" (a list of strings, as many as the item's ladder_levels), "regions" (a list of exactly 4 strings), "categories" (a list of exactly 3 strings) and "customers" (a list of exactly 4 strings).
- Valid JSON only: no text before or after the array, no markdown code fences, no comments. Inside JSON strings write a line break as \n and a double quote as \".
Literal JSON example (valid JSON; the qid is the first real one of this task; it shows the first item only, your file holds 17 such objects, one per item): [{"qid": "q77749ea2ca", "pack": {"store": "Wrenfield Emporium", "ladder": ["Cog", "Crown", "Pendulum"], "regions": ["Tolverra", "Mistlecombe", "Harrowdene", "Pellimar"], "categories": ["pocket watches", "watch straps", "clock movements"], "customers": ["Imogen Fairweather", "Kwame Boateng", "Anika Rao", "Tomas Lindqvist"]}}]
The example values are for the format only (its ladder has 3 levels; yours has the item's ladder_levels): invent your own values and never copy the example's.

Task kind: author_pack; items: 17; outputs expected: 17.

## Instructions

You are writing short pieces of text for a synthetic training dataset about shop advertisements: a store
advertises headline offers, small print narrows them, and a customer's order is checked against them. Everything you
write is either a reusable template (a program later fills each {SLOT} placeholder with a value), a list of invented
values, or a short text built around facts we give you. Write natural, varied English. Invent everything: never copy
text from real companies, brands, products, people, places, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \n and a double quote as \".

TASK: invent one STORE PACK per item: the invented values a fictional shop of the item's kind uses in its adverts and
order records. Fit every value to the item's shop kind.

A program checks the spelling of every value, and a pack that breaks one rule is thrown away whole. Write plain
English letters only (a-z and A-Z): no accents, hyphens, apostrophes, ampersands, digits or other marks anywhere.

Fields of "pack" (all invented: no real company, brand, product line, person or place):
- "store": the shop's name, two or three words (such as "Wrenfield Emporium"). Each word is one capital letter
  followed by lowercase letters only. It must not contain a word that names a product category, a delivery region, a
  membership level or a price status, and it must not contain a taken word (list below).
- "ladder": the shop's membership levels, lowest first, exactly as many as the item asks (3 or 4). Each level is ONE
  word: one capital letter followed by lowercase letters only. The order from lowest to highest must be easy to follow
  (metals, gems, sizes, trees by height, stars by brightness ...). Avoid the common ladders Bronze/Silver/Gold/Platinum,
  Basic/Plus/Premier/Elite and Green/Blue/Black.
- "regions": exactly four invented delivery-region names, ONE word each (one capital letter followed by lowercase
  letters only), sounding like places but not real ones (such as "Tolverra").
- "categories": exactly three product categories the shop sells: lowercase letters only, one or two words separated by
  one space (never a hyphen), plural or mass nouns (such as "pocket watches"). Never a price word or a status such as
  clearance, sale, refurbished or open box.
- "customers": exactly four invented customers' full names. Each name is exactly two words, a given name and a family
  name, and each word is one capital letter followed by lowercase letters only. No hyphen, no apostrophe, no accent, no
  capital letter inside a word, no initial and no third word. Right: "Marisol Vega", "Oluwaseun Adeyemi". Wrong:
  "Sung-min Park", "Catriona MacLeod", "Zoe O'Neil", "Maria de la Cruz". Vary the cultural origin; no famous people.
No digits anywhere. No value may contain a negation word (such as no, not, never, none, nobody). All values within a
pack differ, and no value repeats a value of another item in this task or of the example.

Taken words. Each word below is already a region, a membership level or a product category word in other shops' packs
or in the seed lists. None of them may appear anywhere in your packs: not as a level, a region or a category word, and
not inside a store name or a customer's name (a pack holding one is thrown away):
acre, adult, alder, aldrusk, alvinmere, ambrewick, ammerlund, animal, animals, antique, apprentice, ardenbeck, ardenhaw, area, art, arvale, aubrenne, baby, backpacks, bags, baking, ballet, balloons, balsa, barrel, basic, bats, beacon, beagle, beans, bed, bedding, bellarow, bexterne, bib, bikes, birch, bird, black, blackout, blaze, blinds, blue, board, boards, bobbin, bolt, bonfire, bonsai, books, boots, bottles, boulder, box, boxes, brannoch, brass, brelmont, brenmoor, bricks, bridle, bright, brilliant, brisenhold, brisnell, brocade, brogue, bronze, brushes, bruvellan, building, bulbs, bungalow, bush, caddamore, caddies, caddowen, caddy, cadet, cadvane, cake, calderon, camera, candle, candles, canister, canvas, car, card, cards, carpets, cases, casserole, cat, cauldron, cedar, ceramic, chairs, champion, chef, chest, chrome, circular, clearance, clutch, cob, cobalt, cobble, collections, coltrissa, commodore, compost, cookbooks, cooling, cordless, corrimbe, corrowen, corundum, corvania, cosmetic, cottage, cotton, cottrowe, covers, cressmoor, cricket, crochet, crossinde, cruiser, cumbrel, cup, curtains, cushions, cycling, decks, dendrithe, denim, desk, diamond, dim, dishes, dog, door, doorbells, dosserley, double, dravenmoor, drills, drum, drumavel, dryers, duffel, dunlorn, dunmere, dunsarre, duvet, eddamore, eldrinde, electronics, elite, ellsward, elm, enamel, ensign, eskarra, eskarth, espresso, esterwold, exercise, fabrics, fallowmere, fallowry, fans, fastoway, feed, feeding, feldspar, felgrove, fencing, fenmoral, fenrald, ferrandy, ferrowick, filters, final, fishing, fitted, floor, foam, foreman, fountain, frames, fruit, frying, fulcrane, furniture, gallandry, gallon, games, garden, garnet, garrowen, garrowmere, gear, gentrell, gigabyte, gildenvar, girder, glaspeck, glass, glossopane, goggles, gold, gorrimel, gorrowick, graphics, green, greeting, greyhaven, grove, hair, haldrecourt, hallowmere, halvedon, hamster, hardback, harlovia, harnethy, hartsinde, hatchling, hazel, heads, heat, hebrondell, hedge, heirloom, helmets, hendrimoor, herbal, heslecourt, hesmere, hiking, hobwinter, hollin, holvarden, hooks, horse, houseplants, hunter, ibbsdale, iltorvan, ilverine, imbrook, infant, infusions, iron, irrenwood, isarvel, jackets, jacquenay, jerrevine, jerseys, jessmere, jessvelle, jigsaw, journeyman, junior, juvenile, kellandra, kelvarn, kelvarra, kenvaris, kerrawick, kestrand, kilobyte, king, kiravel, kirrensey, kitchenware, kits, knight, knives, lace, lamp, lamps, lantern, lanterne, larch, lead, ledger, lens, lenses, leotards, line, linen, linings, liskamber, litter, livestock, loafer, loom, lorvane, lounge, lumbardine, lures, lusterne, lusvale, machines, mandreth, manor, mansion, maple, marlin, marrowen, mats, maxi, meadow, megabyte, megalith, memo, memory, mennoway, midi, mini, minnow, mirrors, mirrovane, mirrowen, mixers, model, modules, moissanite, mollinsk, mordane, morrandy, morvane, morvendy, morvenlea, motion, mouldings, mount, murdrowe, nail, needles, net, nethermoor, netherstay, newborn, nickel, oak, olmerow, olvanne, open, ophelmar, organisers, orsovane, osmeldine, osterlin, ostravelle, ostrelle, ostrenn, overlock, oxford, pad, padlocks, pads, paint, paints, pallador, pamphlet, pandrey, pans, paper, paperback, parasol, pascombe, patio, pawn, peak, pebble, pelladine, pelvarin, pencil, pendant, pendrake, pennavey, pennoval, pennyrigge, pens, pentavel, pet, picture, pillowcases, pillows, pinch, pip, plants, plates, platinum, plot, plus, plush, poetry, polish, pomerant, pony, power, pre-order, premier, pressure, price, puzzles, pyrendal, quamberly, quarrowby, quart, quartz, queen, quendral, quenmere, quillandra, quillmarsh, quilting, rabbit, racer, rackets, radiant, rain, ranch, ranger, ravenelle, ravenholt, redwood, refurbished, regular, rendavy, retro, revenhall, rhomsby, ridge, ripple, road, roasted, roller, rook, rookie, room, roskenwald, rowan, rowanvarre, ruddlemoor, rugs, runner, ruthvane, sablewyn, sachet, saddle, sale, salmon, sample, sandals, sapling, satchel, saucepans, savarno, saws, scout, screws, sculdry, seats, seed, sellinor, senior, sensors, sequoia, seratine, sets, sewing, shades, shag, sheets, shoes, shorts, shower, shrub, sideboards, siderhald, sidrana, silicone, silver, single, skateboard, skillet, skirts, sleeping, slipper, smart, somberlyn, sorrenvale, sorvell, spark, spatulas, spool, sport, sports, sprig, sprout, spruce, stand, stands, stavanderly, stenvoy, stockpot, strategy, substrates, suitcases, suldane, sulvoy, summit, sundervell, supplies, surf, swell, swim, sylvandre, syndarra, tables, tackle, tamberley, tap, tape, tarvendell, tavistry, tea, teldoray, tembrick, tennis, tents, teranwold, tessimere, tester, tharvoll, thessory, thimble, thread, throw, tibbery, tins, tiransk, tiverlin, toasters, toddler, tools, topaz, toppers, torwick, touring, townhouse, toys, trail, trainers, travel, treats, trees, trenhollow, trevalick, tripod, trousers, trout, trunk, tungsten, tuskerly, tutu, ulvarren, umbrenne, units, vaelbrook, vallowry, vanity, varrowby, vases, velthorn, velunda, velvet, ventrine, veteran, video, villa, vintage, voile, wall, wallpaper, warmblood, warrenvale, washers, washi, water, wax, wendlark, wessenmoor, wessinde, wetsuits, wilmarrow, wingback, wipes, wire, wood, woodland, wool, work, worsted, worvinde, wrenhaddow, wylbourne, yarn, yarrowdene, yolstrand, ysmarre, zantaru, zelvane

Words in use. Each word below already appears in the dataset's advertisement copy, notes, questions or small-print
sentences. No level, no region name and no category word may be one of them (a pack holding one is thrown away); store
names and customers' names may use them:
aboard, about, above, accents, accepted, accompanies, according, account, accurate, across, action, activities, actually, ad, add, adds, admire, admired, adore, adults, advance, adventure, adventurer, adventures, advert, advertised, advertisement, advice, after, again, against, ages, agreed, ahead, ahoy, air, air-dry, airy, aisle, aisles, alike, all, allow, almost, alone, along, alongside, already, always, among, angles, answer, answers, any, anyone, anything, anytime, app, appeared, apples, applied, applies, apply, appreciate, appreciates, approach, argues, aromas, around, arranged, arranges, arranging, arrival, arrivals, arrived, arriving, aside, ask, asked, asks, assigned, assortment, assurance, assured, athletes, atmosphere, attach, attached, attaches, attention, attentive, authority, available, avoid, await, awaits, away, back, backdrop, backed, bad, baffled, bakery, balcony, barks, based, basics, basket, bass, bearing, beautiful, beautifully, beauty, because, becomes, beds, been, before, begin, beginning, begins, behind, being, believes, belong, belongs, below, bend, bending, bends, benefit, beside, besides, best, better, between, beyond, big, bike, birdsong, bit, bite, bits, blankets, blocks, blooming, blooms, blossoms, bobs, bold, boldly, booklet, bought, bounce, bouncing, bouncy, bound, bread, breath, breathe, breeze, brewing, brief, brighten, brightens, brighter, bring, bringing, brings, brisk, brought, browse, browsing, brush, bubbling, buddy, buff, buggy, build, builders, builds, built, bunting, burst, bursting, bus, business, bustling, busy, button, buyer, buyers, buying, buzzing, cables, call, calling, calls, calm, came, can, cannot, care, careful, carefully, caring, carried, carry, cart, carved, case, catalogue, catch, catches, category, caused, certain, chain, chair, changes, chapter, character, charm, charming, chat, chatter, chatting, check, checked, checking, checkout, cheeky, cheer, cheerful, cheering, cheerio, cheers, chefs, children, choice, choices, choose, choosing, chose, chosen, chuffed, circle, claims, clarity, classic, classics, clean, cleaners, clear, clear-cut, clearer, clearly, clever, close, close-knit, closely, closer, cloth, cloths, clutter, coastal, coat, coffee, cold, colleague, collection, color, colour, colourful, colours, combine, come, comes, comfort, comfortable, comforts, comfy, coming, community, companion, companions, company, compare, complaint, composed, composure, condition, conditions, confidence, confident, confidently, confined, confirm, confirming, considered, contemporary, continue, continued, controls, conversation, cooking, cool, corner, corners, cosy, could, count, counted, counter, counts, cover, covered, cozy, craft, crafted, craftsmanship, create, creating, creativity, crew, crisp, crumbs, crunchy, cuppa, curated, curates, curios, curiosity, curious, custom, customer, customers, cut, cycle, dab, dads, damp, dance, dart, date, dated, day, deal, dear, decide, decision, decisions, decor, deeper, define, deliberate, delight, delighted, delightful, delights, delivered, delivery, depend, dependable, describe, descriptions, deserve, deserves, design, designed, designer, designers, designs, details, detour, difference, different, dinner, direct, direction, discerning, discover, discoveries, displays, dive, do, does, doesn, doing, done, doodads, doodles, doors, down, down-to-earth, drawn, dreamers, dreaming, drew, drifts, drill, drop, dropped, dropping, drops, dry, dull, dust, duster, dusting, each, eager, ear, earlier, earn, earns, ears, earth, ease, easier, easily, easy, easy-to-clean, easygoing, edge, edit, edited, edition, effectively, effort, effortless, elegance, elegant, elevated, eligibility, else, employee, end, ended, endure, enduring, energetic, energy, enjoy, enjoying, enjoys, enough, essentials, even, every, everyday, everyone, everything, exact, exactly, exceeds, exception, exceptional, exceptions, excited, excluded, excludes, excluding, expected, expects, experience, expert, experts, explain, explore, explorers, exploring, expressed, eye, face, faces, fail, fails, faint, fair, faithful, fall, falls, familiar, families, family, family-friendly, far, fast, fastenings, favorite, favorites, favour, favourite, favourites, features, feedback, feel, feeling, feels, filed, fill, filled, find, finding, finds, fine, finest, finish, finishing, firm, fit, fits, fixings, fixture, flagged, flat, flavors, fluffy, focus, focuses, folks, follow, follows, food, footnote, footnotes, forfeit, forfeiting, form, forms, forward, found, fragrant, fresh, friend, friendliest, friendly, friends, front, fuel, full, fully, fun, furry, fuss, gadgets, gang, gaps, gather, gathered, gatherings, gathers, general, generous, gentle, gently, genuine, gestures, get, getaway, gets, giant, giggle, giggle-worthy, giggles, giggling, give, given, gives, gizmos, glad, glance, glances, glow, glowing, go, go-to, goes, going, good, goodies, goods, goofy, got, grab, grace, graceful, gracious, grandparents, grant, grasp, grateful, gratitude, great, greater, greet, greeted, greetings, grime, grin, grinning, grins, grip, grit, ground, growing, grown, grown-up, grown-ups, grows, guests, guide, guiding, habits, hallway, hand, handle, handling, hands, hands-on, handsome, handy, happily, happy, hard, hardwearing, harsh, haste, having, head, headed, heading, headline, headphones, heap, hear, hearing, hears, heart, hearts, held, hello, hellos, helmet, help, helpers, helpful, helping, helpline, helps, here, hey, hi, hidden, hide, high, higher, hiya, hold, holds, home, homes, honest, honestly, honored, honoured, hooray, hop, hope, hopes, hoping, hosting, hosts, house, household, households, how, hub, huge, hugs, hum, humidity, hungry, hushed, ideas, identical, imaginations, imaginative, impossible, include, included, including, indicates, information, inside, insists, inspiration, inspire, intention, interest, internet, into, introduces, introducing, introduction, invitation, invite, invited, invites, inviting, isn, issue, item, items, itself, jams, jiffy, job, jobs, join, joined, joining, joints, jokes, journey, journeys, joy, joyful, joys, judged, judging, jump, just, keen, keep, keeping, keeps, kept, kettle, kid-friendly, kids, kind, kindly, kit, kitchen, know, known, knows, labels, laid, landed, landing, lands, lanterns, large, lasting, later, latest, laugh, lay, layer, layers, layout, layouts, leads, learn, leashes, least, leave, leaves, leeway, left, leisure, leisurely, length, let, lets, letter, lettering, letters, letting, level, levels, lies, life, lift, light, lightly, like, limited, lined, linen-soft, lines, lineup, linger, list, listed, listening, lists, lit, little, live, lively, living, load, local, local-feeling, locals, long, long-lasting, longer, look, looked, looking, looks, loose, lose, lost, lot, loud, loudly, love, lovely, lovers, loves, lovingly, lower, loyal, loyalty, luck, luminous, luxury, made, magic, main, make, makers, makes, making, manner, mark, marked, mat, material, materials, matter, may, meals, mean, means, meant, measured, meet, meeting, meets, members, membership, memories, mending, mentions, microfibre, mild, mind, minds, minimal, minimum, mischief, miss, mix, modern, modest, moment, moments, momentum, mood, moods, more, move, moves, moving, mums, music, must, name, natter, natural, navigate, navigation, near, nearby, nearly, neat, neater, neatly, needs, neighbors, neighbour, neighbourhood, neighbourly, neighbours, nest, never, new, newest, news, nice, nobody, noise, nooks, note, notes, notice, nutshell, objects, obtain, odd, oddities, off, offer, offers, office, oil, old, older, once, ones, online, only, onward, ooh, options, order, orders, ordinary, organizers, ought, ourselves, out, outing, outings, outside, over, own, pace, pack, packed, page, pages, pal, palettes, pals, parcel, parents, part, party, pass, passed, past, path, patience, patient, patron, patterns, pause, pay, payment, pays, peace, pedaling, peek, people, per, perfect, perform, performance, personal, philosophy, phone, pick, picked, picking, picks, piece, pieces, place, placed, placing, plain, plain-speaking, plan, planning, plans, play, playful, playground, playlist, pleasant, please, pleased, pleasure, plug, poise, poised, polished, politely, pop, popped, popping, porch, pots, practical, practically, precise, premium, prep, prepare, prepared, present, presentation, presented, presents, preserves, press, priced, pricing, pride, print, printed, privilege, problem, proceed, product, products, project, projects, promise, promised, promises, promising, promo, promotion, promptly, proper, properly, proud, provide, psst, public, pull, purchase, purchases, pure, purpose, put, puts, qualifies, qualifying, quality, question, questioned, questions, quick, quickly, quiet, quieter, quietly, quirky, racks, range, ranges, ranked, rapid, rather, reach, reaches, reaching, read, reader, reading, ready, real, really, reasonable, reasons, recalls, receipt, receive, received, receives, recently, recheck, recipe, recognised, recommendation, recommendations, reconsideration, redeem, redeemed, refilled, refined, refining, reflect, reflects, refresh, regards, reimagined, relax, relaxed, reliable, rely, relying, remembers, repay, repeat, repeats, required, requires, reserved, respected, responds, rest, restful, restraint, restricted, restriction, results, review, reviews, rhythm, rich, richer, ride, right, rinse, roaming, rooftops, rooms, roomy, round, route, routine, routines, rows, rules, rummage, run, s, said, same, savour, saw, sawdust-scented, say, saying, says, scan, scene, screen, scroll, seams, search, searching, seat, secure, see, seeing, seek, seekers, seems, seen, selection, selections, selects, sell, sells, send, sends, sense, senses, sensible, serene, serve, serves, service, serving, sessions, set, setting, settings, settle, setup, shady, shake, shape, shaped, shapes, shaping, share, sharing, sharp, sharpened, sharper, shelf, sheltered, shelves, shine, shiny, shop, shopped, shopper, shoppers, shopping, shops, short, should, shouted, show, showing, shown, shows, side, sight, signs, silly, simple, simpler, simply, since, sincerely, sing, sit, sits, sitting, skilled, skip, skipping, sleek, slick, slot, slow, slower, slowly, small, small-print, small-shop, smile, smiles, smiling, smooth, smoothly, snacks, sneaks, snug, soap, soaps, soft, soft-spoken, soften, softly, sole, solely, solidly, something, somewhere, sophisticated, sort, sorted, sorts, sound, sourced, space, spaces, sparkle, sparkles, speak, speakers, speaking, speaks, special, speed, speedy, spell, spells, spend, spills, splash, spoil, sponge, spot, spots, spotted, spread, sprinkle, squint, stack, staff, standard, standards, standing, standout, staples, start, started, starts, state, stated, states, status, stay, stays, steady, step, steps, still, stillness, stitching, stock, stocked, stocking, stocks, stool, stop, stopped, stopping, stops, storage, store, stories, storing, story, straight, straight-talking, straightforward, streamlined, street, stretch, strict, strictly, stroll, strong, studio, stuff, sturdy, style, styled, styles, stylish, subject, submitted, subtitle, subtle, subtler, subtly, subtotal, subtotals, such, suit, suits, sun, sunlight, sunny, sunshine, suppers, supple, support, supporting, sure, surely, surface, surprise, surprises, surrounded, surroundings, survive, swap, swapping, sweet, swift, swing, swipe, t, table, tactile, tail, tailoring, take, taken, takes, taking, talk, talking, taste, tasteful, tastes, tasty, team, tell, tend, tended, terms, textures, thank, thankful, thanks, thin, thing, things, thinking, thinks, those, though, thought, thoughtful, thoughtfully, thrilled, through, tickle, tidied, tidy, tidy-up, tidy-ups, tie, tied, tier, tight, tighten, timeless, tinkering, tinkling, tiny, tip, tips, tiptoe, title, toddlers, together, tone, tones, too, took, top, touch, touches, tough, toward, towards, town, trails, treasure, treasures, treat, treated, treble, trend, trending, trinkets, trip, trips, trolley, trouble, trowels, true, truly, trust, trusted, trusting, trusts, try, tuck, tucked, tune, tunes, turn, turned, turning, turns, twinkle, uncluttered, under, understand, understands, understated, unhurried, unless, unreadable, update, upkeep, ups, use, used, useful, uses, valid, value, version, very, vibe, view, vision, visit, visiting, visitor, visitors, visits, vocals, volume, wags, wait, waiting, waits, waive, walk, walked, wander, wandering, want, wanted, wants, wardrobe, wares, warm, warmest, warmly, warmth, warns, watched, wave, waving, way, ways, wearing, weaves, website, welcome, welcomed, welcomes, welcoming, well, well-made, well-ordered, well-run, went, whatever, where, while, whimsy, whistle, whole, whose, why, wide, wiggle, wild, window, wink, wins, wipe, wiped, wiping, wish, wishes, withheld, within, without, wobble, wonderful, wonders, word, wording, words, workaday, workbench, worker, workmanlike, workouts, works, workshop, workshop-style, world, worth, would, wrench, writes, written, yard, young, youngest, youngsters, yours, yourself

Taken store names (never reuse or imitate one): Ambrey Hollow, Birchwood Linens, Bluecrest Sports, Brackwell Works, Bramblewick Depot, Brastow Mill, Brigend Trading, Brightwell Home, Brindle Folio, Cedarline Living, Cinderly Hearth, Copperleaf Kitchen, Corvane Gallery, Cragmoor Trailhouse, Cressendale Parlour, Driftmoor Lane, Dunmarrow Yard, Ellory Crossing, Elmstead Emporium, Fernway Market, Furrowdale Mill, Gallant Wayfare, Halvet Field, Halvorne Terrace, Harborlight Goods, Hazelcombe Studio, Hensley Academy, Hollinger Pantry, Hollyfern Makers, Jubilee Corner, Juniper Gadgets, Juniper Lane, Kestrel Outfitters, Larkspur Playthings, Lodestar Anglers, Lorrain Vivarium, Mallory Gate, Marbleton Lane, Marigold Pets, Merrowby Annex, Nestwell House, Northvale Audio, Oakhurst Interiors, Oriel House, Ostrander Common, Pawsley Lane, Pebblestone Garden, Pellidor House, Quaymoor Traders, Quenby Attic, Quillfern Point, Rookery Wheelhouse, Rowanbrook Store, Sablecrest Exchange, Sarnet Court, Selvane Grange, Soleward Crossing, Starling Glow, Strenham Stables, Thistledown Row, Thistledown Supply, Thornlea Estate, Tidewell Supply, Tillery Yard, Tollgate Works, Vellmock Bay, Venmoor Road, Wrenfield Mercantile, Wrenfield Outdoor.

Before you write the answer, check every word of every value against the word lists above and replace any word that is listed.

## Items (17; answer every item, keyed by its qid)

```json
[
 {
  "qid": "q77749ea2ca",
  "brief": {
   "shop_kind": "a fishing tackle shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q21a4354b41",
  "brief": {
   "shop_kind": "a workwear outfitter",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q93210e65d6",
  "brief": {
   "shop_kind": "a consumer electronics retailer",
   "ladder_levels": 4
  }
 },
 {
  "qid": "qcc2ad5c5f8",
  "brief": {
   "shop_kind": "a kitchen appliance outlet",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qf329089aee",
  "brief": {
   "shop_kind": "a home brewing supplies shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q7075764fed",
  "brief": {
   "shop_kind": "a swimming and pool supplies store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q7fcdb23724",
  "brief": {
   "shop_kind": "a candle and gift shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q3b77503b97",
  "brief": {
   "shop_kind": "a hardware store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q5d48010c3a",
  "brief": {
   "shop_kind": "a climbing gear shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q609204a03b",
  "brief": {
   "shop_kind": "a tool hire and sales yard",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q0faa119172",
  "brief": {
   "shop_kind": "a mattress store",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qd627c2f0ee",
  "brief": {
   "shop_kind": "a photography store",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q76424e22ec",
  "brief": {
   "shop_kind": "a stargazing and telescope shop",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q144e6093b8",
  "brief": {
   "shop_kind": "a home appliance retailer",
   "ladder_levels": 3
  }
 },
 {
  "qid": "q7fe74fd9b5",
  "brief": {
   "shop_kind": "a ceramics studio shop",
   "ladder_levels": 3
  }
 },
 {
  "qid": "qefa100fd4c",
  "brief": {
   "shop_kind": "an office furniture dealer",
   "ladder_levels": 4
  }
 },
 {
  "qid": "q4f23a7a4f5",
  "brief": {
   "shop_kind": "a music instrument shop",
   "ladder_levels": 4
  }
 }
]
```
