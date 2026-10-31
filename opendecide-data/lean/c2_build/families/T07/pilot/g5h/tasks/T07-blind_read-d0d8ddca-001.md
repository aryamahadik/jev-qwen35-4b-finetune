# G5-H blind read T07-blind_read-d0d8ddca-001 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/pilot/g5h/answers/T07-blind_read-d0d8ddca-001.json

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
  "qid": "q22440b372a",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nFree shipping on every order*\nFree assembly with every delivery†\n\nThanks for trusting Northvale Audio with your purchase. Set the item on a dry, flat surface, away from direct sunlight and damp air.\n\nOrder ORD-224577 placed by Selin Yilmaz:\n- item: SKU-33058\n- product category: kitchenware\n- price status: clearance\n- delivery region: Fallowmere\n- order date: Tuesday, April 7, 2026\n- membership level: Premier\n- order subtotal: 209.86 USD\n\nFine print from the bottom of the advertisement:\n† Shoppers may place orders on Monday, April 6, 2026 itself and on every day before it. Applies to membership at Premier or lower.\n* For members at Premier or lower.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers that what the advertisement says lists does order ORD-224577 from Selin Yilmaz truly get?",
  "options": [
   "Only free shipping",
   "Both offers",
   "Only free assembly",
   "Neither offer"
  ]
 },
 {
  "qid": "qb732732439",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nFree returns on every purchase*\nFree shipping on every order†\n\nFine print:\n* Applies to orders placed ahead of Monday, 31 August 2026.\n† Order subtotal strictly more than 25.00 USD.\n\nSharp, direct, clear-cut\nNorthvale Audio keeps its shelves clean, its lines crisp and its range easy to follow.\n\nOrder ORD-474001 placed by Aiko Brandt:\n- item: SKU-51137\n- product category: kitchenware\n- price status: regular price\n- delivery region: Eskarth\n- order date: Saturday, 22 August 2026\n- membership level: Elite\n- order subtotal: 25.01 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does customer Aiko Brandt on order ORD-474001 truly receive, given what the advertisement says?",
  "options": [
   "Neither offer",
   "Only free shipping",
   "Both offers",
   "Only free returns"
  ]
 },
 {
  "qid": "q9c97f77c99",
  "kind": "choice",
  "text": "Advertisement from Birchwood Linens:\nWe match any lower price*\nFree shipping on every order†\n\nSubject: Straightforward shopping\nHello, we like plain speaking, so here it is: Birchwood Linens keeps the essentials stocked and easy to find.\n\nFine print:\n† The headline benefit stops short of delivery to Fallowmere. An order qualifies with a subtotal of $150.00 or more.\n* The subtotal of the order needs to be $25.00 or higher. Orders placed by 17 November 2026 are valid, and the stated day is included.\n\nOrder ORD-881859 placed by Ines Duarte:\n- item: SKU-32310\n- product category: pet supplies\n- price status: regular price\n- delivery region: Fallowmere\n- order date: 23 October 2026\n- membership level: Premier\n- order subtotal: $149.99",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Birchwood Linens levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nLooking at Ines Duarte's order ORD-881859 and what the advertisement says, which condition in the small print attached to the price match does it miss, if any?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qb3a43efa59",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nFree assembly with every delivery*\nDouble reward points on every purchase†\n\nFine print:\n† Items whose status is refurbished sit outside this offer.\n* Valid for orders placed from Saturday, February 7, 2026 onward. Items drawn from the furniture category miss the headline benefit.\n\nCheerio from the cheerful crew at Brightwell Home, we have a heap of quirky bits waiting for a giggle.\n\nOrder ORD-204993 placed by Aiko Brandt:\n- item: SKU-79867\n- product category: pet supplies\n- price status: refurbished\n- delivery region: Greyhaven\n- order date: Sunday, March 15, 2026\n- membership level: Plus\n- order subtotal: $142.30",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says alongside the advertised terms, does order ORD-204993 from Aiko Brandt fail to secure free assembly?"
 },
 {
  "qid": "q97ed3c49fe",
  "kind": "yes/no",
  "text": "Advertisement from Cedarline Living:\nFree assembly with every delivery*\n\nHello, neighbours! Cedarline Living is a small shop with a big heart, and we are happy you popped in. Come say hi, browse at your own pace, and tell us what you love.\n*The order subtotal must be above $75.\n\nOrder ORD-735332 placed by Ravi Anand:\n- item: SKU-43305\n- product category: kitchenware\n- price status: refurbished\n- delivery region: Dunmere\n- order date: 9 Jun 2026\n- membership level: Green\n- order subtotal: 75.01 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-735332 from Ravi Anand forfeit free assembly under the advertised terms, as those terms are written?"
 },
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
  "qid": "qa415eac525",
  "kind": "choice",
  "text": "Order ORD-438199 placed by Mira Castell:\n| field | value |\n| --- | --- |\n| item | SKU-55720 |\n| product category | kitchenware |\n| price status | refurbished |\n| delivery region | Brenmoor |\n| order date | 2026-07-04 |\n| membership level | Premier |\n| order subtotal | $170.33 |\n\nAdvertisement from Copperleaf Kitchen:\nA lifetime warranty on everything we sell*\n\n{\"title\": \"Practical shopping from Copperleaf Kitchen\", \"subtitle\": \"Tidy labels and a neat layout help you find things fast\", \"button\": \"See the range\"}\n\nFine print:\n* Reserved for members at Plus or below.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms, which condition attached to the lifetime warranty does order ORD-438199 from Mira Castell miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qbb060c8f40",
  "kind": "choice",
  "text": "Order ORD-452078 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-15559 |\n| product category | pet supplies |\n| price status | clearance |\n| delivery region | Hollin |\n| order date | Thursday, 19 March 2026 |\n| membership level | Green |\n| order subtotal | 55.98 USD |\n\nAdvertisement from Northvale Audio:\nFree assembly with every delivery*\nWe match any lower price†\n\nIt's lovely to have you here. Northvale Audio is delighted to share its range with you.\n\nFine print:\n* Every item priced as open box is excluded from this offer.\n† Minimum order subtotal: 50.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertisement and its fine print offer by offer, which headline offers does Ines Duarte actually get on order ORD-452078?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only free assembly",
   "Only the price match"
  ]
 },
 {
  "qid": "qa3d81e5487",
  "kind": "choice",
  "text": "Advertisement from Kestrel Outfitters:\nWe match any lower price*\nDouble reward points on every purchase†\n\nFine print:\n* Valid on orders of 150.00 USD or more.\n† Minimum order subtotal: 100.00 USD.\n\nQuiet confidence suits a home beautifully. We are proud to share our favourite finds from Kestrel Outfitters.\n\nOrder ORD-955513 placed by Selin Yilmaz:\n- item: SKU-26352\n- product category: garden tools\n- price status: refurbished\n- delivery region: Hollin\n- order date: 24 May 2026\n- membership level: Blue\n- order subtotal: 114.41 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nCould you say which of the advertised terms Selin Yilmaz actually gets on order ORD-955513 while the small print is checked offer by offer?",
  "options": [
   "Both offers",
   "Neither offer",
   "Only the price match",
   "Only double reward points"
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
  "qid": "q3cc3be7400",
  "kind": "choice",
  "text": "Order ORD-303688 placed by Kofi Asante:\n| field | value |\n| --- | --- |\n| item | SKU-92303 |\n| product category | sports gear |\n| price status | open box |\n| delivery region | Greyhaven |\n| order date | 24 February 2026 |\n| membership level | Basic |\n| order subtotal | 129.82 USD |\n\nAdvertisement from Harborlight Goods:\nFree gift wrapping at checkout*\n\nSubject: a warm welcome from our little corner of the world\nHello and welcome,\nHarborlight Goods is delighted to share ideas for calm, cozy living. Our team loves helping you create a welcoming space. Thank you for being here with us.\n*Excludes items with refurbished status. For Basic members and below.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, if any, of the ad and its small print attached to free gift wrapping does order ORD-303688 from Kofi Asante miss?",
  "options": [
   "The price-status condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qb92e707f92",
  "kind": "choice",
  "text": "Support chat about order ORD-252547:\nDana Okafor: Hi, I placed order ORD-252547 on 24 March 2026 for item SKU-12359, and the order subtotal was $55.38.\nAgent: Thanks. The item is in the garden tools product category, its price status is regular price, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Premier.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nA lifetime warranty on everything we sell*\nFree gift wrapping at checkout†\n\nHello there from Pebblestone Garden. Explore the range at speed and spot the pieces that suit you.\n\nFine print:\n† The order subtotal must be above $50.\n* The order subtotal must be strictly greater than $50.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Pebblestone Garden levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers survive the advertisement and its fine print for order ORD-252547 from Dana Okafor, checked offer by offer?",
  "options": [
   "Both offers",
   "Only the lifetime warranty",
   "Only free gift wrapping",
   "Neither offer"
  ]
 },
 {
  "qid": "q9b9c6819a1",
  "kind": "yes/no",
  "text": "Advertisement from Harborlight Goods:\nFree gift wrapping at checkout*\n\n{\"title\": \"Harborlight Goods app\", \"subtitle\": \"Browse the range, build a list, and check out quickly\", \"button\": \"Get started\"}\n\nOrder ORD-436956 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-67060 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Fallowmere |\n| order date | 2026-03-29 |\n| membership level | Platinum |\n| order subtotal | 183.27 USD |\n\nFine print from the bottom of the advertisement:\n* Items under the bedding category are carved out of this offer. The headline benefit is withheld on delivery to Fallowmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the ad and its small print, is it true that order ORD-436956 from Jonah Pryce doesn't get free gift wrapping under the advertised terms?"
 },
 {
  "qid": "qc6371ed8bb",
  "kind": "choice",
  "text": "Support chat about order ORD-629386:\nHugo Lindqvist: Hi, I placed order ORD-629386 on 16 September 2026 for item SKU-56066, and the order subtotal was $118.70.\nAgent: Thanks. The item is in the electronics product category, its price status is regular price, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Plus.\nHugo Lindqvist: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nOur corner shop at Oakhurst Interiors is tucked away, which is part of the charm.\n\nFine print:\n* Orders placed by 1 September 2026 are valid, and the stated day is included.\n† An order placed on or before 12 October 2026 qualifies. The order subtotal must be above $100.00.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does order ORD-629386 from Hugo Lindqvist truly get under the advertisement and its fine print?",
  "options": [
   "Only free shipping",
   "Only free gift wrapping",
   "Neither offer",
   "Both offers"
  ]
 },
 {
  "qid": "qca7f1566a9",
  "kind": "yes/no",
  "text": "Order ORD-541242 placed by Felix Moreau:\n| field | value |\n| --- | --- |\n| item | SKU-56214 |\n| product category | toys |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | June 13, 2026 |\n| membership level | Basic |\n| order subtotal | $204.64 |\n\nAdvertisement from Copperleaf Kitchen:\nFree returns on every purchase*\n\nFine print:\n* Every item in the bedding category falls outside the offer.\n\nSensible picks, down to earth\nStroll the aisles at Copperleaf Kitchen and see how straightforward products slot into ordinary homes.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the ad and its small print together, does order ORD-541242 from Felix Moreau fail to secure free returns under the advertised terms?"
 },
 {
  "qid": "q78c59b70e7",
  "kind": "yes/no",
  "text": "Order ORD-269004 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-90730 |\n| product category | pet supplies |\n| price status | pre-order |\n| delivery region | Calderon |\n| order date | Saturday, 28 March 2026 |\n| membership level | Plus |\n| order subtotal | $50.00 |\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nBrowsing here is easy and the staff are happy to help you find what suits your home. Pop in and see what Copperleaf Kitchen has on the shelves.\n\nFine print:\n* Order subtotal exceeds $50.00. Each order needs delivery to Calderon to earn the benefit. Qualifying orders include the date Saturday, 28 February 2026 and every later day.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-269004 from Ravi Anand get free assembly?"
 },
 {
  "qid": "q1df781bd3a",
  "kind": "yes/no",
  "text": "Advertisement from Northvale Audio:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Items under the bedding category are carved out of this offer.\n† Every delivery bound for Calderon lies outside the headline offer. Valid for orders placed before 2026-08-31.\n\nKnown to the neighbourhood\nFamiliar faces greet you at Northvale Audio, a little place with a big heart for the street.\n\nOrder ORD-235934 placed by Mira Castell:\n- item: SKU-77467\n- product category: bedding\n- price status: clearance\n- delivery region: Calderon\n- order date: 2026-09-19\n- membership level: Basic\n- order subtotal: 109.28 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that the order ORD-235934 placed by Mira Castell does not get free returns under the advertised terms, as what the advertisement says indicates?"
 },
 {
  "qid": "qe50a6aa8e0",
  "kind": "choice",
  "text": "Support chat about order ORD-627133:\nInes Duarte: Hi, I placed order ORD-627133 on September 20, 2026 for item SKU-83706, and the order subtotal was 179.93 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is pre-order, and it ships to the Hollin delivery region.\nAgent: Your membership level is Elite.\nInes Duarte: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nFree assembly with every delivery*\nWe match any lower price†\n\nMake a move\nOur modern shapes and sharp colours are ready for a fresh look at Wrenfield Outdoor.\n\nFine print:\n* Any order placed on October 21, 2026 and beyond is accepted.\n† Items marked with the final sale status fall outside the benefit set out here.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking the small print into account offer by offer, what are the advertised terms that Ines Duarte actually gets on order ORD-627133?",
  "options": [
   "Only the price match",
   "Neither offer",
   "Only free assembly",
   "Both offers"
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
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q852b151c37",
  "kind": "choice",
  "text": "Support chat about order ORD-170280:\nFelix Moreau: Hi, I placed order ORD-170280 on Monday, 15 June 2026 for item SKU-82261, and the order subtotal was 63.20 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is clearance, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Platinum.\nFelix Moreau: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree assembly with every delivery*\n\nOur corner of town is brighter with Cedarline Living in it, so stop in for a warm, personal welcome.\n\nFine print:\n* Reserved for members ranked Platinum or higher. For the offer, the order subtotal must be higher than $75.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe advertisement and its fine print attach conditions to free assembly; which, if any, does order ORD-170280 from Felix Moreau miss?",
  "options": [
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
  "qid": "q6fb6f7e03a",
  "kind": "choice",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nBring the family along\nWrenfield Outdoor is a welcoming place for parents, grandparents and children, with friendly staff ready to help.\n\nFine print:\n† Orders headed for delivery in Brenmoor are kept out of this offer.\n* Applies to orders placed ahead of Monday, July 27, 2026. Valid for orders whose subtotal is $75 or more.\n\nOrder ORD-221730 placed by Owen Mensah:\n- item: SKU-51500\n- product category: furniture\n- price status: regular price\n- delivery region: Brenmoor\n- order date: Sunday, July 26, 2026\n- membership level: Gold\n- order subtotal: $94.20",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, drawn from the ad and its small print attached to free shipping, does order ORD-221730 from Owen Mensah miss, if any?",
  "options": [
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "qafa79ba412",
  "kind": "yes/no",
  "text": "Advertisement from Fernway Market:\nFree returns on every purchase*\nDouble reward points on every purchase†\n\nFine print:\n† Orders placed by 13 June 2026 are valid, and the stated day is included.\n* Excludes the toys category.\n\nWipe it with a damp cloth and let it air-dry. Thanks for buying from Fernway Market.\n\nOrder ORD-394280 placed by Selin Yilmaz:\n- item: SKU-79020\n- product category: toys\n- price status: regular price\n- delivery region: Arvale\n- order date: 24 June 2026\n- membership level: Gold\n- order subtotal: $57.60",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the advertisement with its fine print confirm that order ORD-394280 from Selin Yilmaz comes with free returns?"
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
  "qid": "q642b1ff81c",
  "kind": "yes/no",
  "text": "Advertisement from Oakhurst Interiors:\nA lifetime warranty on everything we sell*\n\nSubject: Quick scroll, sharp picks\nHey, Oakhurst Interiors is moving fast and the lineup is crisp.\n\nFine print:\n* Goods filed under a different category from pet supplies fall outside the benefit. An order whose delivery goes to Hollin falls outside the headline benefit.\n\nOrder ORD-274231 placed by Hugo Lindqvist:\n- item: SKU-81803\n- product category: pet supplies\n- price status: regular price\n- delivery region: Hollin\n- order date: September 17, 2026\n- membership level: Silver\n- order subtotal: $76.96",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not so that Hugo Lindqvist does not get the lifetime warranty on order ORD-274231, per the advertisement and its fine print?"
 },
 {
  "qid": "q812cafb5bd",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree shipping on every order*\n\nHey, Brightwell Home crew! Stop in and find clever doodads that make life brighter.\n*Valid on orders of 100.00 USD or more. Items in the bedding product category are excluded.\n\nOrder ORD-228338 placed by Kofi Asante:\n- item: SKU-11321\n- product category: bedding\n- price status: pre-order\n- delivery region: Dunmere\n- order date: 21 April 2026\n- membership level: Basic\n- order subtotal: 116.26 USD\n\nNote added by the customer: Kofi Asante insists the advert on the website looked far more generous when the order was placed, and that is what the offer should follow.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Brightwell Home levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nLooking at Kofi Asante's order ORD-228338 and what the advertisement says, which condition in the small print attached to free shipping does it miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition",
   "The order-subtotal condition"
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
  "qid": "q5b0dfc678f",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nFree returns on every purchase*\n\nA step ahead\nWalk into Fernway Market and discover a shop that knows its craft and takes real pride in its shelves.\n\nFine print:\n* Every delivery bound for Greyhaven lies outside the headline offer. Valid for orders placed on or after Saturday, 11 July 2026.\n\nOrder ORD-641368 placed by Owen Mensah:\n| field | value |\n| --- | --- |\n| item | SKU-45310 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | Saturday, 8 August 2026 |\n| membership level | Platinum |\n| order subtotal | $96.53 |",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Fernway Market levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich small-print condition in the ad, attached to free returns, does order ORD-641368 from Owen Mensah miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The delivery-region condition"
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
  "qid": "qd037e4c83f",
  "kind": "choice",
  "text": "Order ORD-193939 placed by Mira Castell:\n| field | value |\n| --- | --- |\n| item | SKU-36147 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | Friday, 27 March 2026 |\n| membership level | Premier |\n| order subtotal | 155.99 USD |\n\nAdvertisement from Fernway Market:\nFree assembly with every delivery*\nFree installation for every appliance†\n\nFine print:\n† The order date needs to be on or before Thursday, 26 March 2026.\n* For Plus members and above.\n\nGood coffee, good company and a little bit of fun at Fernway Market. Pop by and see what we have been up to.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIn the ad, which condition attached to free installation does order ORD-193939 from Mira Castell miss, if any?",
  "options": [
   "The order-date condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q168b608902",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nFree installation for every appliance*\nDouble reward points on every purchase†\n\nFine print:\n† Members at the Premier level or higher only. Delivery to Hollin is the sole route to the headline benefit.\n* Only orders placed before November 18, 2026 count toward this offer. Stock with pre-order status is excluded from this benefit.\n\nWe appreciate your custom at Brightwell Home. Look closely at the stitching and tighten loose fixings gently.\n\nOrder ORD-284642 placed by Owen Mensah:\n- item: SKU-40262\n- product category: electronics\n- price status: final sale\n- delivery region: Hollin\n- order date: October 19, 2026\n- membership level: Premier\n- order subtotal: 247.24 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Brightwell Home levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDo the advertised terms, taking in the headline and small print, let Owen Mensah get free installation on order ORD-284642?"
 },
 {
  "qid": "qd226731be8",
  "kind": "choice",
  "text": "Order ORD-312606 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-89776 |\n| product category | electronics |\n| price status | pre-order |\n| delivery region | Eskarth |\n| order date | 6 Oct 2026 |\n| membership level | Premier |\n| order subtotal | 97.42 USD |\n\nAdvertisement from Fernway Market:\nFree assembly with every delivery*\n\nFine print:\n* Items priced as pre-order are excluded.\n\nGrins, colour and cheeky surprises are waiting at Fernway Market, so bring your curiosity.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Fernway Market levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, which condition in the small print attached to free assembly does order ORD-312606 from Selin Yilmaz miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition"
  ]
 },
 {
  "qid": "qc2759dd9e7",
  "kind": "choice",
  "text": "Advertisement from Copperleaf Kitchen:\nWe match any lower price*\nFree returns on every purchase†\n\nFine print:\n† The order subtotal must be at least $75.00 for this offer to apply. The headline benefit stops short of delivery to Eskarth.\n* Products in the kitchenware category are excluded from this offer. The benefit is withheld from anything with clearance pricing.\n\n{\"title\": \"Browse the new range at Copperleaf Kitchen\", \"subtitle\": \"Scroll the favourites and find a piece to love\", \"button\": \"Start looking\"}\n\nOrder ORD-361385 placed by Nadia Haddad:\n- item: SKU-31968\n- product category: kitchenware\n- price status: clearance\n- delivery region: Eskarth\n- order date: 2026-03-13\n- membership level: Bronze\n- order subtotal: $94.05",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich small-print condition in the ad, attached to free returns, does order ORD-361385 from Nadia Haddad miss, if any?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "The price-status condition",
   "The product-category condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q5ad2af5531",
  "kind": "yes/no",
  "text": "Order ORD-269004 placed by Ravi Anand:\n- item: SKU-90730\n- product category: pet supplies\n- price status: pre-order\n- delivery region: Calderon\n- order date: Saturday, 28 March 2026\n- membership level: Plus\n- order subtotal: $50.00\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nCopperleaf Kitchen is a down-to-earth shop with reliable products and helpful staff.\n\nFine print:\n* Order subtotal exceeds $50.00. Each order needs delivery to Calderon to earn the benefit. Qualifying orders include the date Saturday, 28 February 2026 and every later day.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-269004 from Ravi Anand get free assembly?"
 },
 {
  "qid": "q41282b18fb",
  "kind": "yes/no",
  "text": "Support chat about order ORD-736594:\nMira Castell: Hi, I placed order ORD-736594 on 1 May 2026 for item SKU-48333, and the order subtotal was $223.09.\nAgent: Thanks. The item is in the furniture product category, its price status is refurbished, and it ships to the Greyhaven delivery region.\nAgent: Your membership level is Black.\nMira Castell: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\nDouble reward points on every purchase†\n\nA bit of dusting goes a long way. Thanks, and happy handling from Birchwood Linens.\n\nFine print:\n† Only a delivery to Greyhaven qualifies for this offer.\n* Excludes all items with refurbished status. Delivery to Greyhaven only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertised terms, which include the headline and its small print, does Mira Castell come with free shipping on order ORD-736594?"
 },
 {
  "qid": "q3659ef8520",
  "kind": "yes/no",
  "text": "Order ORD-222742 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-53874 |\n| product category | kitchenware |\n| price status | open box |\n| delivery region | Arvale |\n| order date | Sunday, March 8, 2026 |\n| membership level | Green |\n| order subtotal | $144.80 |\n\nAdvertisement from Northvale Audio:\nFree installation for every appliance*\n\nFine print:\n* Valid for orders placed before Sunday, March 1, 2026.\n\nThank you kindly for picking Northvale Audio. Let your new piece rest in a quiet corner away from direct sun and dust it gently with a soft duster.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhen the headline and its small print are read against the advertised terms, does order ORD-222742 from Tomas Ferreira receive free installation?"
 },
 {
  "qid": "qb13d507c54",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nDouble reward points on every purchase*\n\nFine print:\n* Applies to Plus level and higher members. Headline benefit is confined to delivery landing in Greyhaven.\n\nStep into Larkspur Playthings and see why our edit is admired for craftsmanship, clarity and character.\n\nOrder ORD-332984 placed by Jonah Pryce:\n- item: SKU-23660\n- product category: bedding\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: 1 June 2026\n- membership level: Plus\n- order subtotal: $205.51",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad and its small print say that order ORD-332984 from Jonah Pryce gets double reward points?"
 },
 {
  "qid": "qe8c6785426",
  "kind": "yes/no",
  "text": "Support chat about order ORD-160626:\nTomas Ferreira: Hi, I placed order ORD-160626 on 15 Aug 2026 for item SKU-16308, and the order subtotal was 30.60 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Hollin delivery region.\nAgent: Your membership level is Bronze.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree shipping on every order*\n\nStop by Juniper Gadgets for the essentials you use at home.\n\nFine print:\n* For the offer, the order subtotal must be higher than 35.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-160626 placed by Tomas Ferreira lose out on free shipping?"
 }
]
