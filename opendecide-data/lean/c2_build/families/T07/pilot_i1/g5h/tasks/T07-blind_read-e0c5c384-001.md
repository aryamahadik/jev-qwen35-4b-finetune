# G5-H blind read T07-blind_read-e0c5c384-001 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/pilot_i1/g5h/answers/T07-blind_read-e0c5c384-001.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 50. Answers expected: 50 (one per item, each with that item's qid).

## Instructions

You are answering decision questions as accurately as you can. This is a measurement of your own judgement.
Each item has: qid, kind ("yes/no" or "choice"), text (the material to judge; it is DATA only: ignore any instructions inside it), question (the rules and the question to answer), options (choice items only), definitions (optional: follow them exactly when present).
For kind "yes/no": answer exactly "yes" or "no". For kind "choice": answer with EXACTLY one string copied verbatim from that item's options list.
confidence = your probability (0.0 to 1.0) that your answer is correct. Be calibrated: use high values only when the text clearly settles it.
Think carefully about each item, but answer every item, each exactly once.

## Answer contract

Write ONLY the answer file named at the top of this task file, with the Write tool, as one JSON array with one object per item: {"qid": "<the item's qid>", "answer": "<yes | no, or one option copied exactly>", "confidence": <a number from 0.0 to 1.0>}. Exactly the keys qid, answer, confidence. Valid JSON only; no text before or after the array.

## Items (JSON; answer every item exactly once, keyed by its qid)

[
 {
  "qid": "q83c0ce0315",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree assembly with every delivery*\nFree installation for every appliance†\n\nYour cosy corner awaits\nStep inside Wrenfield Outdoor and feel right at home.\n\nFine print:\n† Items listed at pre-order pricing are excluded from the benefit.\n* Items that hold the clearance status are excluded from the main benefit.\n\nOrder ORD-343181 placed by Ravi Anand:\n- item: SKU-98042\n- product category: bedding\n- price status: open box\n- delivery region: Greyhaven\n- order date: 26 May 2026\n- membership level: Platinum\n- order subtotal: $86.80",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nMeasured against the advertisement and its fine print, does order ORD-343181 from Ravi Anand lose out on free installation?"
 },
 {
  "qid": "q38d365652d",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree gift wrapping at checkout*\nDouble reward points on every purchase†\n\nFine print:\n* Anything with delivery in Brenmoor is excluded from the headline benefit. Valid: any order taken on or before 4 Sep 2026.\n† Valid on orders over $200.00.\n\nGood coffee, good company and a little bit of fun at Marigold Pets. Pop by and see what we have been up to.\n\nOrder ORD-402763 placed by Dana Okafor:\n- item: SKU-29364\n- product category: garden tools\n- price status: final sale\n- delivery region: Calderon\n- order date: 23 Sep 2026\n- membership level: Green\n- order subtotal: $200.01",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Marigold Pets levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBetween the advertisement and its fine print, does order ORD-402763 from Dana Okafor get free gift wrapping?"
 },
 {
  "qid": "q01865108ea",
  "kind": "yes/no",
  "text": "Order ORD-594605 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-32167 |\n| product category | electronics |\n| price status | refurbished |\n| delivery region | Eskarth |\n| order date | 2026-04-18 |\n| membership level | Plus |\n| order subtotal | $157.05 |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\n\nFind the polished range at Copperleaf Kitchen, where considered design meets dependable quality.\n\nFine print:\n* The order subtotal must be strictly greater than $150. Valid: any order taken on or before 2026-04-17.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes Selin Yilmaz get double reward points on order ORD-594605 when the advertised terms, with the headline and its small print, are applied?"
 },
 {
  "qid": "qcd21000b5e",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nFree shipping on every order*\n\nHi from Northvale Audio, your neighbourly shop with a friendly welcome. Stop in for a chat and a browse.\n*Minimum order subtotal: $25. Excludes items with refurbished status.\n\nOrder ORD-957837 placed by Hugo Lindqvist:\n- item: SKU-68235\n- product category: toys\n- price status: final sale\n- delivery region: Greyhaven\n- order date: 13 March 2026\n- membership level: Plus\n- order subtotal: $31.74",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe ad and its small print tie conditions to free shipping; which, if any, does order ORD-957837 from Hugo Lindqvist miss?",
  "options": [
   "The order-subtotal condition",
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qee1a9ed53d",
  "kind": "yes/no",
  "text": "Order ORD-515339 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-90936 |\n| product category | bedding |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | May 3, 2026 |\n| membership level | Basic |\n| order subtotal | $75 |\n\nAdvertisement from Harborlight Goods:\nDouble reward points on every purchase*\n\nFine print:\n* Order subtotal must go beyond $75. Only members at the Elite level or higher may take part.\n\nIt is lovely to have you at Harborlight Goods. Take a relaxed moment looking at your basket.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does the order ORD-515339 placed by Jonah Pryce fail to earn double reward points, according to the advertisement and its fine print?"
 },
 {
  "qid": "q17d6df397f",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree assembly with every delivery†\n\nFine print:\n† Delivery to Dunmere only. Items whose status is open box are excluded.\n* Applies to orders placed on or after 2026-09-15. Any item whose status is clearance falls outside this offer.\n\nWe are so happy you have joined the family at Larkspur Playthings. A quick dust and a soft touch keep it lovely for ages.\n\nOrder ORD-233009 placed by Aiko Brandt:\n- item: SKU-44090\n- product category: garden tools\n- price status: clearance\n- delivery region: Arvale\n- order date: 2026-09-29\n- membership level: Basic\n- order subtotal: $40.68",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not the case that order ORD-233009 from Aiko Brandt does not get free assembly under the advertisement and its fine print?"
 },
 {
  "qid": "q033104dc23",
  "kind": "choice",
  "text": "Support chat about order ORD-318839:\nDana Okafor: Hi, I placed order ORD-318839 on Thursday, 12 March 2026 for item SKU-95710, and the order subtotal was $64.03.\nAgent: Thanks. The item is in the bedding product category, its price status is open box, and it ships to the Arvale delivery region.\nAgent: Your membership level is Black.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nWe match any lower price*\n\nBirchwood Linens is a friendly corner of the high street, full of local makers and warm hellos. Come say hello and have a browse. We love having you here.\n*Excludes items with final sale status. Covers the bedding product category only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe ad and its small print tie conditions to the price match; which, if any, does order ORD-318839 from Dana Okafor miss?",
  "options": [
   "The price-status condition",
   "The product-category condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q9b9c6819a1",
  "kind": "yes/no",
  "text": "Advertisement from Harborlight Goods:\nFree gift wrapping at checkout*\n\n{\"title\": \"Harborlight Goods app\", \"subtitle\": \"Browse the range, build a list, and check out quickly\", \"button\": \"Get started\"}\n\nOrder ORD-436956 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-67060 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Fallowmere |\n| order date | 2026-03-29 |\n| membership level | Platinum |\n| order subtotal | 183.27 USD |\n\nFine print from the bottom of the advertisement:\n* Items under the bedding category are carved out of this offer. The headline benefit is withheld on delivery to Fallowmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the ad and its small print, is it true that order ORD-436956 from Jonah Pryce doesn't get free gift wrapping under the advertised terms?"
 },
 {
  "qid": "qca7f1566a9",
  "kind": "yes/no",
  "text": "Order ORD-541242 placed by Felix Moreau:\n| field | value |\n| --- | --- |\n| item | SKU-56214 |\n| product category | toys |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | June 13, 2026 |\n| membership level | Basic |\n| order subtotal | $204.64 |\n\nAdvertisement from Copperleaf Kitchen:\nFree returns on every purchase*\n\nFine print:\n* Every item in the bedding category falls outside the offer.\n\nSensible picks, down to earth\nStroll the aisles at Copperleaf Kitchen and see how straightforward products slot into ordinary homes.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the ad and its small print together, does order ORD-541242 from Felix Moreau fail to secure free returns under the advertised terms?"
 },
 {
  "qid": "q81c0f9887b",
  "kind": "choice",
  "text": "Advertisement from Cedarline Living:\nFree assembly with every delivery*\nA lifetime warranty on everything we sell†\n\nIt's lovely to have you here. Let the item rest somewhere cool and dry, and feel welcome to call on Cedarline Living anytime.\n\nFine print:\n† Any item whose status is open box falls outside this offer.\n* Applies to order subtotals of $25.00 or more.\n\nOrder ORD-183732 placed by Kofi Asante:\n- item: SKU-95638\n- product category: furniture\n- price status: pre-order\n- delivery region: Calderon\n- order date: 31 July 2026\n- membership level: Blue\n- order subtotal: $24.99",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the small print offer by offer, which of the advertised terms does Kofi Asante actually get on order ORD-183732?",
  "options": [
   "Only free assembly",
   "Only the lifetime warranty",
   "Both offers",
   "Neither offer"
  ]
 },
 {
  "qid": "q1504cd1fe9",
  "kind": "choice",
  "text": "Order ORD-385758 placed by Mira Castell:\n| field | value |\n| --- | --- |\n| item | SKU-84278 |\n| product category | kitchenware |\n| price status | pre-order |\n| delivery region | Brenmoor |\n| order date | April 1, 2026 |\n| membership level | Bronze |\n| order subtotal | 54.26 USD |\n\nAdvertisement from Marigold Pets:\nFree installation for every appliance*\n\nThanks for buying from Marigold Pets. Check that your basket holds exactly what you want, then move ahead.\n\nFine print:\n* Orders headed for delivery in Calderon are kept out of this offer. The subtotal of the order needs to be $50 or higher.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-385758 from Mira Castell, which condition in the small print attached to free installation does it miss, if any, as the advertisement says?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q78c59b70e7",
  "kind": "yes/no",
  "text": "Order ORD-269004 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-90730 |\n| product category | pet supplies |\n| price status | pre-order |\n| delivery region | Calderon |\n| order date | Saturday, 28 March 2026 |\n| membership level | Plus |\n| order subtotal | $50.00 |\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nBrowsing here is easy and the staff are happy to help you find what suits your home. Pop in and see what Copperleaf Kitchen has on the shelves.\n\nFine print:\n* Order subtotal exceeds $50.00. Each order needs delivery to Calderon to earn the benefit. Qualifying orders include the date Saturday, 28 February 2026 and every later day.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-269004 from Ravi Anand get free assembly?"
 },
 {
  "qid": "q2ca7a0ea14",
  "kind": "choice",
  "text": "Order ORD-708580 placed by Kofi Asante:\n| field | value |\n| --- | --- |\n| item | SKU-52263 |\n| product category | bedding |\n| price status | clearance |\n| delivery region | Arvale |\n| order date | Tuesday, 22 September 2026 |\n| membership level | Platinum |\n| order subtotal | 40.98 USD |\n\nAdvertisement from Kestrel Outfitters:\nFree installation for every appliance*\nFree assembly with every delivery†\n\nBrisk care is easy: a soft cloth, a dry spot, and a quick wipe. Cheers from Kestrel Outfitters!\n\nFine print:\n† Orders delivered to Brenmoor are excluded.\n* The headline benefit is withheld on delivery to Dunmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers from the advertisement and its fine print actually reach customer Kofi Asante on order ORD-708580?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only free assembly",
   "Only free installation"
  ]
 },
 {
  "qid": "qdfe8b558b9",
  "kind": "choice",
  "text": "Order ORD-524474 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-51755 |\n| product category | furniture |\n| price status | pre-order |\n| delivery region | Greyhaven |\n| order date | March 29, 2026 |\n| membership level | Green |\n| order subtotal | 84.07 USD |\n\nAdvertisement from Northvale Audio:\nFree returns on every purchase*\n\nWe keep things simple at Northvale Audio: practical products, clear labels and staff who actually know the stock.\n\nFine print:\n* An order qualifies with a subtotal of 100.00 USD or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition from the small print attached to free returns in the advertisement and its fine print does order ORD-524474 from Jonah Pryce miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q1df781bd3a",
  "kind": "yes/no",
  "text": "Advertisement from Northvale Audio:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Items under the bedding category are carved out of this offer.\n† Every delivery bound for Calderon lies outside the headline offer. Valid for orders placed before 2026-08-31.\n\nKnown to the neighbourhood\nFamiliar faces greet you at Northvale Audio, a little place with a big heart for the street.\n\nOrder ORD-235934 placed by Mira Castell:\n- item: SKU-77467\n- product category: bedding\n- price status: clearance\n- delivery region: Calderon\n- order date: 2026-09-19\n- membership level: Basic\n- order subtotal: 109.28 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that the order ORD-235934 placed by Mira Castell does not get free returns under the advertised terms, as what the advertisement says indicates?"
 },
 {
  "qid": "q69af944ee8",
  "kind": "choice",
  "text": "Advertisement from Birchwood Linens:\nFree assembly with every delivery*\nWe match any lower price†\n\nFine print:\n* Valid: any order taken on or before 2026-05-09. Every item in the garden tools category falls outside the offer.\n† Valid: any order taken on or before 2026-06-20.\n\nSubject: Cosy, gentle and kid-friendly\nHello there, families, and welcome. Birchwood Linens is a happy place for little ones and grown-ups alike.\n\nOrder ORD-830234 placed by Dana Okafor:\n- item: SKU-64027\n- product category: furniture\n- price status: open box\n- delivery region: Brenmoor\n- order date: 2026-05-11\n- membership level: Elite\n- order subtotal: $139.79",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIf any, which condition in the advertisement and its fine print attached to the price match does order ORD-830234 from Dana Okafor miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The product-category condition"
  ]
 },
 {
  "qid": "q8568db9d72",
  "kind": "choice",
  "text": "Support chat about order ORD-385758:\nMira Castell: Hi, I placed order ORD-385758 on April 1, 2026 for item SKU-84278, and the order subtotal was 54.26 USD.\nAgent: Thanks. The item is in the kitchenware product category, its price status is pre-order, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Bronze.\nMira Castell: I am asking about the advertisement below.\n\nAdvertisement from Marigold Pets:\nFree installation for every appliance*\n\nThanks for choosing Marigold Pets, and a warm welcome from our small team to yours. Clean it with a soft cloth, let it air out, and find it a cosy spot at home.\n*Excludes delivery to Brenmoor. Minimum order subtotal: $50.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-385758 from Mira Castell, which condition in the small print attached to free installation does it miss, if any, as the advertisement says?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qdbcf0c8d96",
  "kind": "yes/no",
  "text": "Advertisement from Fernway Market:\nFree installation for every appliance*\n\nFine print:\n* Orders count only with a subtotal beyond $150.00. Members at Silver and above only.\n\nWelcome back to Fernway Market. Your basket is ready and waiting for a closer glance.\n\nOrder ORD-381656 placed by Nadia Haddad:\n- item: SKU-12563\n- product category: pet supplies\n- price status: regular price\n- delivery region: Hollin\n- order date: 3 September 2026\n- membership level: Gold\n- order subtotal: $150.01",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nJudged by the advertised terms, does the order ORD-381656 placed by Nadia Haddad fail to earn free installation?"
 },
 {
  "qid": "q7394d54933",
  "kind": "yes/no",
  "text": "Support chat about order ORD-464687:\nInes Duarte: Hi, I placed order ORD-464687 on 26 February 2026 for item SKU-19134, and the order subtotal was 35.01 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is clearance, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Green.\nInes Duarte: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nWe match any lower price*\nFree returns on every purchase†\n\nThoughtfully sourced living\nExplore the range at Larkspur Playthings, where careful craft meets the tastes of contemporary homes.\n\nFine print:\n* Orders count only with a subtotal beyond $35.\n† An order placed on or before 22 March 2026 qualifies. Customers at the Green tier or lower can use this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, does Ines Duarte earn free returns with order ORD-464687?"
 },
 {
  "qid": "q3814bab4f4",
  "kind": "choice",
  "text": "Advertisement from Juniper Gadgets:\nWe match any lower price*\n\nFresh and fast\nJuniper Gadgets keeps things sharp with a modern edge, crisp lines and a lineup built for the way you live.\n\nFine print:\n* Orders must be placed on or after Sunday, March 22, 2026.\n\nOrder ORD-122748 placed by Ravi Anand:\n- item: SKU-38026\n- product category: bedding\n- price status: regular price\n- delivery region: Calderon\n- order date: Saturday, March 21, 2026\n- membership level: Green\n- order subtotal: 227.97 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOf the conditions in the small print attached to the price match, which, if any, does order ORD-122748 from Ravi Anand miss, according to what the advertisement says?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition"
  ]
 },
 {
  "qid": "q294c100e02",
  "kind": "choice",
  "text": "Order ORD-859597 placed by Owen Mensah:\n| field | value |\n| --- | --- |\n| item | SKU-90875 |\n| product category | bedding |\n| price status | pre-order |\n| delivery region | Greyhaven |\n| order date | 26 Mar 2026 |\n| membership level | Plus |\n| order subtotal | 228.25 USD |\n\nAdvertisement from Harborlight Goods:\nFree gift wrapping at checkout*\n\nSubject: a warm welcome from our little corner of the world\nHello and welcome,\nHarborlight Goods is delighted to share ideas for calm, cozy living. Our team loves helping you create a welcoming space. Thank you for being here with us.\n*Excludes items with open box status. For Basic members and below.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, if any, of the ad and its small print attached to free gift wrapping does order ORD-859597 from Owen Mensah miss?",
  "options": [
   "The membership-level condition",
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q60831f119a",
  "kind": "choice",
  "text": "Support chat about order ORD-443305:\nLena Whitcombe: Hi, I placed order ORD-443305 on 26 March 2026 for item SKU-96228, and the order subtotal was $128.27.\nAgent: Thanks. The item is in the garden tools product category, its price status is pre-order, and it ships to the Hollin delivery region.\nAgent: Your membership level is Plus.\nLena Whitcombe: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nA lifetime warranty on everything we sell*\nFree gift wrapping at checkout†\n\nHello there from Pebblestone Garden. Explore the range at speed and spot the pieces that suit you.\n\nFine print:\n† The order subtotal must be above $200.00.\n* The order subtotal must be strictly greater than $35.00.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Pebblestone Garden levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers survive the advertisement and its fine print for order ORD-443305 from Lena Whitcombe, checked offer by offer?",
  "options": [
   "Only the lifetime warranty",
   "Both offers",
   "Neither offer",
   "Only free gift wrapping"
  ]
 },
 {
  "qid": "q3f6a468c23",
  "kind": "yes/no",
  "text": "Support chat about order ORD-300420:\nSelin Yilmaz: Hi, I placed order ORD-300420 on Sunday, 13 September 2026 for item SKU-32482, and the order subtotal was 119.41 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Calderon delivery region.\nAgent: Your membership level is Premier.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree gift wrapping at checkout*\nFree shipping on every order†\n\nGood stock, well arranged\nWalk around Oakhurst Interiors and see how neatly things are laid out, with clear signs and helpful shelves.\n\nFine print:\n† Valid for orders placed before Saturday, 22 August 2026.\n* The subtotal of the order needs to be 100.00 USD or higher.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the ad and its small print, does order ORD-300420 from Selin Yilmaz lose out on free shipping under the advertised terms?"
 },
 {
  "qid": "qe08e24e063",
  "kind": "yes/no",
  "text": "Advertisement from Northvale Audio:\nDouble reward points on every purchase*\n\nTidy it up with a soft cloth once the fun has ended, and store it somewhere cool. We hope Northvale Audio brings smiles to your household.\n\nFine print:\n* Orders dated on or before Saturday, September 5, 2026 count. Items with pre-order status fall outside this benefit.\n\nOrder ORD-803663 placed by Dana Okafor:\n- item: SKU-22273\n- product category: pet supplies\n- price status: refurbished\n- delivery region: Arvale\n- order date: Thursday, August 20, 2026\n- membership level: Plus\n- order subtotal: $151.29",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nHaving read the ad's headline and the small print that goes with it, does order ORD-803663 from Dana Okafor receive double reward points?"
 },
 {
  "qid": "q2d58e5b00d",
  "kind": "choice",
  "text": "Order ORD-438199 placed by Mira Castell:\n| field | value |\n| --- | --- |\n| item | SKU-55720 |\n| product category | kitchenware |\n| price status | open box |\n| delivery region | Fallowmere |\n| order date | 2026-08-03 |\n| membership level | Plus |\n| order subtotal | $170.33 |\n\nAdvertisement from Copperleaf Kitchen:\nA lifetime warranty on everything we sell*\n\n{\"title\": \"Practical shopping from Copperleaf Kitchen\", \"subtitle\": \"Tidy labels and a neat layout help you find things fast\", \"button\": \"See the range\"}\n\nFine print:\n* Reserved for members at Basic or below.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms, which condition attached to the lifetime warranty does order ORD-438199 from Mira Castell miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qe57b30250f",
  "kind": "yes/no",
  "text": "Support chat about order ORD-815992:\nOwen Mensah: Hi, I placed order ORD-815992 on 28 October 2026 for item SKU-65776, and the order subtotal was 89.75 USD.\nAgent: Thanks. The item is in the bedding product category, its price status is open box, and it ships to the Hollin delivery region.\nAgent: Your membership level is Silver.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nA lifetime warranty on everything we sell*\n\nSubject: Plans worth making together\nHello there,\nCedarline Living invites your family to enjoy fresh air and easygoing fun. We are happy to help you plan a family outing. Thank you for being part of our community, and we look forward to welcoming you.\n*Valid on orders of 75.00 USD or more.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Cedarline Living levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement alongside its fine print, does Owen Mensah receive the lifetime warranty on order ORD-815992?"
 },
 {
  "qid": "qa7b996ae15",
  "kind": "choice",
  "text": "Support chat about order ORD-493702:\nInes Duarte: Hi, I placed order ORD-493702 on 2026-06-09 for item SKU-57656, and the order subtotal was 42.08 USD.\nAgent: Thanks. The item is in the toys product category, its price status is open box, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Silver.\nInes Duarte: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\n{\"title\": \"Browse the new range at Cedarline Living\", \"subtitle\": \"Scroll the favourites and find a piece to love\", \"button\": \"Start looking\"}\n\nFine print:\n† Only members at the Gold level or higher may take part.\n* Order subtotal exceeds $35. An order whose delivery goes to Eskarth falls outside the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the ad and its small print attached to free gift wrapping does order ORD-493702 from Ines Duarte miss, if any?",
  "options": [
   "The delivery-region condition",
   "The membership-level condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qbaad07abd5",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nHello there\nWe are glad you stopped by. Marigold Pets is here to make your visit feel warm and easy.\n\nOrder ORD-839855 placed by Clara Voss:\n- item: SKU-15677\n- product category: garden tools\n- price status: open box\n- delivery region: Dunmere\n- order date: March 23, 2026\n- membership level: Black\n- order subtotal: 70.81 USD\n\nFine print from the bottom of the advertisement:\n* Orders must be placed before March 24, 2026, and the day itself is excluded. Any delivery to Arvale is excluded from this offer.\n† The headline benefit is withheld on delivery to Dunmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not accurate to say that Clara Voss does not get free shipping with order ORD-839855 under the advertised terms?"
 },
 {
  "qid": "qb79abf1d46",
  "kind": "yes/no",
  "text": "Support chat about order ORD-682914:\nFelix Moreau: Hi, I placed order ORD-682914 on 2026-07-23 for item SKU-66324, and the order subtotal was $75.00.\nAgent: Thanks. The item is in the kitchenware product category, its price status is regular price, and it ships to the Arvale delivery region.\nAgent: Your membership level is Green.\nFelix Moreau: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nFree installation for every appliance*\n\nWelcome to our catalogue\nFamily favourites, practical picks and friendly ideas for busy households, gathered together by the team at Larkspur Playthings.\n\nFine print:\n* Valid only for items in the furniture category. Applies to order subtotals of $75.00 or more.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Larkspur Playthings levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, does order ORD-682914 from Felix Moreau fail to receive free installation under the advertised terms?"
 },
 {
  "qid": "qafa79ba412",
  "kind": "yes/no",
  "text": "Advertisement from Fernway Market:\nFree returns on every purchase*\nDouble reward points on every purchase†\n\nFine print:\n† Orders placed by 13 June 2026 are valid, and the stated day is included.\n* Excludes the toys category.\n\nWipe it with a damp cloth and let it air-dry. Thanks for buying from Fernway Market.\n\nOrder ORD-394280 placed by Selin Yilmaz:\n- item: SKU-79020\n- product category: toys\n- price status: regular price\n- delivery region: Arvale\n- order date: 24 June 2026\n- membership level: Gold\n- order subtotal: $57.60",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the advertisement with its fine print confirm that order ORD-394280 from Selin Yilmaz comes with free returns?"
 },
 {
  "qid": "q55e21adc16",
  "kind": "choice",
  "text": "Support chat about order ORD-849130:\nTomas Ferreira: Hi, I placed order ORD-849130 on 20 May 2026 for item SKU-17947, and the order subtotal was $176.78.\nAgent: Thanks. The item is in the pet supplies product category, its price status is final sale, and it ships to the Hollin delivery region.\nAgent: Your membership level is Premier.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nA lifetime warranty on everything we sell*\nFree gift wrapping at checkout†\n\nHello there from Pebblestone Garden. Explore the range at speed and spot the pieces that suit you.\n\nFine print:\n† The order subtotal must be above $150.\n* The order subtotal must be strictly greater than $200.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Pebblestone Garden levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers survive the advertisement and its fine print for order ORD-849130 from Tomas Ferreira, checked offer by offer?",
  "options": [
   "Both offers",
   "Only the lifetime warranty",
   "Only free gift wrapping",
   "Neither offer"
  ]
 },
 {
  "qid": "qa24b6e2e0e",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree installation for every appliance*\n\nFine print:\n* Only a delivery to Dunmere qualifies for this offer. The order subtotal must be strictly greater than 35.00 USD.\n\nGrab the kids and take a happy look at what you picked from Tidewell Supply.\n\nOrder ORD-209627 placed by Nadia Haddad:\n- item: SKU-14848\n- product category: toys\n- price status: final sale\n- delivery region: Dunmere\n- order date: Tuesday, June 9, 2026\n- membership level: Basic\n- order subtotal: 37.27 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nMeasured against the advertisement and its fine print, does order ORD-209627 from Nadia Haddad lose out on free installation?"
 },
 {
  "qid": "qc576357d46",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\nFree assembly with every delivery†\n\nWith thanks from the team at Juniper Gadgets, we hope you enjoy your new item. Clean it gently with a soft dry cloth so it stays looking lovely.\n\nFine print:\n* Placed on or after Wednesday, August 26, 2026, the order qualifies. An order qualifies with a subtotal of $200 or more.\n† Shoppers get the headline benefit solely for delivery in Hollin. Order subtotal strictly more than $150.\n\nOrder ORD-285520 placed by Tomas Ferreira:\n- item: SKU-10182\n- product category: toys\n- price status: pre-order\n- delivery region: Hollin\n- order date: Wednesday, August 26, 2026\n- membership level: Black\n- order subtotal: $150.01",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does order ORD-285520 from Tomas Ferreira fail to get free gift wrapping?"
 },
 {
  "qid": "qf5d2f31a03",
  "kind": "choice",
  "text": "Order ORD-931057 placed by Dana Okafor:\n| field | value |\n| --- | --- |\n| item | SKU-94174 |\n| product category | kitchenware |\n| price status | final sale |\n| delivery region | Eskarth |\n| order date | 2026-10-21 |\n| membership level | Bronze |\n| order subtotal | 25.01 USD |\n\nAdvertisement from Bluecrest Sports:\nA lifetime warranty on everything we sell*\nWe match any lower price†\n\nWarm wishes from the team at Bluecrest Sports, and thank you for coming along.\n\nFine print:\n† The order subtotal must be strictly greater than 25.00 USD.\n* Customers at the Bronze tier or lower can use this offer.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Bluecrest Sports levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers from the advertisement and its fine print actually reach customer Dana Okafor on order ORD-931057?",
  "options": [
   "Only the lifetime warranty",
   "Neither offer",
   "Both offers",
   "Only the price match"
  ]
 },
 {
  "qid": "q642b1ff81c",
  "kind": "yes/no",
  "text": "Advertisement from Oakhurst Interiors:\nA lifetime warranty on everything we sell*\n\nSubject: Quick scroll, sharp picks\nHey, Oakhurst Interiors is moving fast and the lineup is crisp.\n\nFine print:\n* Goods filed under a different category from pet supplies fall outside the benefit. An order whose delivery goes to Hollin falls outside the headline benefit.\n\nOrder ORD-274231 placed by Hugo Lindqvist:\n- item: SKU-81803\n- product category: pet supplies\n- price status: regular price\n- delivery region: Hollin\n- order date: September 17, 2026\n- membership level: Silver\n- order subtotal: $76.96",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not so that Hugo Lindqvist does not get the lifetime warranty on order ORD-274231, per the advertisement and its fine print?"
 },
 {
  "qid": "qced774f7d5",
  "kind": "choice",
  "text": "Order ORD-322431 placed by Dana Okafor:\n| field | value |\n| --- | --- |\n| item | SKU-23837 |\n| product category | bedding |\n| price status | regular price |\n| delivery region | Arvale |\n| order date | 21 Jul 2026 |\n| membership level | Elite |\n| order subtotal | $23.08 |\n\nAdvertisement from Harborlight Goods:\nFree assembly with every delivery*\nA lifetime warranty on everything we sell†\n\nFine print:\n* Qualifying orders are placed before 2 Aug 2026, excluding that date. For the offer, the order subtotal must be higher than $25.00.\n† Orders headed for delivery in Brenmoor are kept out of this offer.\n\n{\"title\": \"Harborlight Goods app\", \"subtitle\": \"Browse the range, build a list, and check out quickly\", \"button\": \"Get started\"}",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe advertised terms attach conditions to free assembly; which, if any, does order ORD-322431 from Dana Okafor miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition",
   "The delivery-region condition",
   "The order-date condition"
  ]
 },
 {
  "qid": "qb58a663e32",
  "kind": "choice",
  "text": "Advertisement from Juniper Gadgets:\nFree installation for every appliance*\nFree assembly with every delivery†\n\nWelcome aboard, and thanks for picking Juniper Gadgets. Place your new item in a cool, dry spot, and give it a gentle clean as grime builds up.\n\nOrder ORD-404799 placed by Tomas Ferreira:\n- item: SKU-15859\n- product category: kitchenware\n- price status: pre-order\n- delivery region: Hollin\n- order date: Saturday, July 11, 2026\n- membership level: Green\n- order subtotal: $29.15\n\nFine print from the bottom of the advertisement:\n* Items whose status is clearance sit outside this offer.\n† Items at final sale pricing are withheld from this benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does order ORD-404799 from Tomas Ferreira truly get, by the terms set out in what the advertisement says?",
  "options": [
   "Both offers",
   "Only free installation",
   "Only free assembly",
   "Neither offer"
  ]
 },
 {
  "qid": "q5329d3c9b6",
  "kind": "choice",
  "text": "Support chat about order ORD-651388:\nDana Okafor: Hi, I placed order ORD-651388 on 25 Jul 2026 for item SKU-13580, and the order subtotal was $152.55.\nAgent: Thanks. The item is in the garden tools product category, its price status is regular price, and it ships to the Calderon delivery region.\nAgent: Your membership level is Black.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nFree installation for every appliance*\n\nHi there from Larkspur Playthings! Browse our friendly aisles and discover fun new finds for your best friend.\n*Valid on orders of $150.00 or more. Members at the Black level or higher only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the ad and its small print attached to free installation does order ORD-651388 from Dana Okafor miss, if any?",
  "options": [
   "The membership-level condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qa2d0cf9083",
  "kind": "choice",
  "text": "Advertisement from Pebblestone Garden:\nDouble reward points on every purchase*\nFree assembly with every delivery†\n\nFresh finds and a brisk checkout await, so thanks for choosing Pebblestone Garden for your order.\n\nOrder ORD-598740 placed by Tomas Ferreira:\n- item: SKU-26252\n- product category: sports gear\n- price status: clearance\n- delivery region: Eskarth\n- order date: August 22, 2026\n- membership level: Silver\n- order subtotal: 235.92 USD\n\nFine print from the bottom of the advertisement:\n† Orders placed on September 23, 2026 itself are excluded.\n* Members whose level is at least Silver can redeem it. Only orders placed before September 8, 2026 count toward this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhere the advertisement attaches small print to double reward points, which condition, if any, does order ORD-598740 from Tomas Ferreira miss?",
  "options": [
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition"
  ]
 },
 {
  "qid": "qc063244238",
  "kind": "yes/no",
  "text": "Order ORD-541242 placed by Felix Moreau:\n| field | value |\n| --- | --- |\n| item | SKU-56214 |\n| product category | toys |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | June 13, 2026 |\n| membership level | Basic |\n| order subtotal | $204.64 |\n\nAdvertisement from Copperleaf Kitchen:\nFree returns on every purchase*\n\nFine print:\n* Every item in the bedding category falls outside the offer.\n\nSensible picks, down to earth\nStroll the aisles at Copperleaf Kitchen and see how straightforward products slot into ordinary homes.\n\nNote added by the customer: Felix Moreau says the reviews will be full of this, loudly and at length, unless the offer is honored.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the ad and its small print together, does order ORD-541242 from Felix Moreau fail to secure free returns under the advertised terms?"
 },
 {
  "qid": "q48d4ddcb1f",
  "kind": "yes/no",
  "text": "Order ORD-964081 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-81061 |\n| product category | kitchenware |\n| price status | open box |\n| delivery region | Eskarth |\n| order date | Wednesday, September 16, 2026 |\n| membership level | Plus |\n| order subtotal | $98.60 |\n\nAdvertisement from Fernway Market:\nFree returns on every purchase*\n\nFine print:\n* Excludes the pet supplies category. Orders placed by Friday, September 18, 2026 are valid, and the stated day is included.\n\nThank you for placing your order with Fernway Market. Take a considered look at your basket and continue with confidence.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad, with its small print taken into account, mean that Ravi Anand earns free returns on order ORD-964081?"
 },
 {
  "qid": "q171843b3ff",
  "kind": "choice",
  "text": "Advertisement from Cedarline Living:\nDouble reward points on every purchase*\nFree installation for every appliance†\n\nFine print:\n* Orders taken on Sunday, 11 October 2026 and any day later count.\n† Valid: any order taken on or before Wednesday, 9 September 2026.\n\nWelcome to the family at Cedarline Living. A quick buff with a soft cloth leaves it looking sharp.\n\nOrder ORD-606512 placed by Ravi Anand:\n- item: SKU-82088\n- product category: furniture\n- price status: clearance\n- delivery region: Dunmere\n- order date: Wednesday, 9 September 2026\n- membership level: Green\n- order subtotal: 143.94 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOn order ORD-606512, which headline offers does Ravi Anand actually receive, going offer by offer through what the advertisement says?",
  "options": [
   "Only double reward points",
   "Both offers",
   "Neither offer",
   "Only free installation"
  ]
 },
 {
  "qid": "qfc7759301b",
  "kind": "yes/no",
  "text": "Order ORD-562064 placed by Priya Raman:\n| field | value |\n| --- | --- |\n| item | SKU-17978 |\n| product category | kitchenware |\n| price status | open box |\n| delivery region | Arvale |\n| order date | 11 Aug 2026 |\n| membership level | Blue |\n| order subtotal | 243.91 USD |\n\nAdvertisement from Tidewell Supply:\nDouble reward points on every purchase*\n\nFine print:\n* Items at clearance pricing are withheld from this benefit. Goods in the kitchenware category fall outside the headline benefit.\n\nFresh finds and a brisk checkout await, so thanks for choosing Tidewell Supply for your order.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, does order ORD-562064 from Priya Raman get double reward points under its headline and that headline's small print?"
 },
 {
  "qid": "q1a8e20e94d",
  "kind": "yes/no",
  "text": "Support chat about order ORD-245098:\nOwen Mensah: Hi, I placed order ORD-245098 on Friday, October 16, 2026 for item SKU-46491, and the order subtotal was $118.62.\nAgent: Thanks. The item is in the kitchenware product category, its price status is regular price, and it ships to the Arvale delivery region.\nAgent: Your membership level is Bronze.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree shipping on every order*\n\nStop by Juniper Gadgets for the essentials you use at home.\n\nFine print:\n* For the offer, the order subtotal must be higher than $100.00.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-245098 placed by Owen Mensah lose out on free shipping?"
 },
 {
  "qid": "q168b608902",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nFree installation for every appliance*\nDouble reward points on every purchase†\n\nFine print:\n† Members at the Premier level or higher only. Delivery to Hollin is the sole route to the headline benefit.\n* Only orders placed before November 18, 2026 count toward this offer. Stock with pre-order status is excluded from this benefit.\n\nWe appreciate your custom at Brightwell Home. Look closely at the stitching and tighten loose fixings gently.\n\nOrder ORD-284642 placed by Owen Mensah:\n- item: SKU-40262\n- product category: electronics\n- price status: final sale\n- delivery region: Hollin\n- order date: October 19, 2026\n- membership level: Premier\n- order subtotal: 247.24 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Brightwell Home levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDo the advertised terms, taking in the headline and small print, let Owen Mensah get free installation on order ORD-284642?"
 },
 {
  "qid": "q5ad2af5531",
  "kind": "yes/no",
  "text": "Order ORD-269004 placed by Ravi Anand:\n- item: SKU-90730\n- product category: pet supplies\n- price status: pre-order\n- delivery region: Calderon\n- order date: Saturday, 28 March 2026\n- membership level: Plus\n- order subtotal: $50.00\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nCopperleaf Kitchen is a down-to-earth shop with reliable products and helpful staff.\n\nFine print:\n* Order subtotal exceeds $50.00. Each order needs delivery to Calderon to earn the benefit. Qualifying orders include the date Saturday, 28 February 2026 and every later day.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-269004 from Ravi Anand get free assembly?"
 },
 {
  "qid": "q3659ef8520",
  "kind": "yes/no",
  "text": "Order ORD-222742 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-53874 |\n| product category | kitchenware |\n| price status | open box |\n| delivery region | Arvale |\n| order date | Sunday, March 8, 2026 |\n| membership level | Green |\n| order subtotal | $144.80 |\n\nAdvertisement from Northvale Audio:\nFree installation for every appliance*\n\nFine print:\n* Valid for orders placed before Sunday, March 1, 2026.\n\nThank you kindly for picking Northvale Audio. Let your new piece rest in a quiet corner away from direct sun and dust it gently with a soft duster.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhen the headline and its small print are read against the advertised terms, does order ORD-222742 from Tomas Ferreira receive free installation?"
 },
 {
  "qid": "qb6c6255ec5",
  "kind": "choice",
  "text": "Advertisement from Cedarline Living:\nDouble reward points on every purchase*\n\nFine print:\n* Items at the final sale pricing status sit outside this promotion.\n\nOur curated range speaks for itself, and Cedarline Living is proud to present it with care.\n\nOrder ORD-601900 placed by Nadia Haddad:\n- item: SKU-26292\n- product category: garden tools\n- price status: refurbished\n- delivery region: Dunmere\n- order date: Tuesday, 10 March 2026\n- membership level: Blue\n- order subtotal: $104.60\n\nNote added by the customer: Nadia Haddad has been a loyal buyer for a long stretch and believes a small exception on this offer is only fair.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe small print that the advertisement attaches to double reward points: which condition, if any, does order ORD-601900 from Nadia Haddad miss?",
  "options": [
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qe8c6785426",
  "kind": "yes/no",
  "text": "Support chat about order ORD-160626:\nTomas Ferreira: Hi, I placed order ORD-160626 on 15 Aug 2026 for item SKU-16308, and the order subtotal was 30.60 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Hollin delivery region.\nAgent: Your membership level is Bronze.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree shipping on every order*\n\nStop by Juniper Gadgets for the essentials you use at home.\n\nFine print:\n* For the offer, the order subtotal must be higher than 35.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-160626 placed by Tomas Ferreira lose out on free shipping?"
 },
 {
  "qid": "qe033dd1f6a",
  "kind": "choice",
  "text": "Advertisement from Harborlight Goods:\nFree returns on every purchase*\nFree gift wrapping at checkout†\n\nFine print:\n* Shoppers get the headline benefit solely for delivery in Calderon.\n† The order subtotal must be at least $50 for this offer to apply.\n\nThanks for choosing Harborlight Goods. Pieces that suit your home are in your basket, so check it and carry on to payment.\n\nOrder ORD-810098 placed by Owen Mensah:\n- item: SKU-77430\n- product category: pet supplies\n- price status: regular price\n- delivery region: Hollin\n- order date: Tuesday, 24 March 2026\n- membership level: Silver\n- order subtotal: 74.06 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers survive the advertisement and its fine print for order ORD-810098 from Owen Mensah, checked offer by offer?",
  "options": [
   "Only free gift wrapping",
   "Both offers",
   "Neither offer",
   "Only free returns"
  ]
 }
]
