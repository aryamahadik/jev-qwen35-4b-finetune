# G5-H blind read T07-blind_read-77c62d0b-000 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/pilot/g5h/answers/T07-blind_read-77c62d0b-000.json

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
  "qid": "qab9066a78b",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nWe match any lower price*\n\nFine print:\n* Any item priced as clearance sits outside the headline benefit. Orders taken on February 9, 2026 and any day later count.\n\nWith thanks from the team at Northvale Audio, we hope you enjoy your new item. Clean it gently with a soft dry cloth so it stays looking lovely.\n\nOrder ORD-769243 placed by Kofi Asante:\n- item: SKU-19340\n- product category: kitchenware\n- price status: clearance\n- delivery region: Calderon\n- order date: March 5, 2026\n- membership level: Plus\n- order subtotal: $71.98",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to the price match does order ORD-769243 from Kofi Asante miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The order-date condition"
  ]
 },
 {
  "qid": "qb6224ca60f",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree installation for every appliance*\n\nFine print:\n* Only a delivery to Dunmere qualifies for this offer. The order subtotal must be strictly greater than 35.00 USD.\n\nGrab the kids and take a happy look at what you picked from Tidewell Supply.\n\nOrder ORD-209627 placed by Nadia Haddad:\n- item: SKU-14848\n- product category: toys\n- price status: final sale\n- delivery region: Dunmere\n- order date: Tuesday, June 9, 2026\n- membership level: Basic\n- order subtotal: 37.27 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDo the advertised terms, taking in the headline and small print, let Nadia Haddad get free installation on order ORD-209627?"
 },
 {
  "qid": "qa35f65af8d",
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
  "qid": "q1a8aaebd31",
  "kind": "yes/no",
  "text": "Advertisement from Pebblestone Garden:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nHi from Pebblestone Garden, your local shop is buzzing and the kettle is on.\n\nOrder ORD-341548 placed by Mira Castell:\n- item: SKU-78509\n- product category: furniture\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 2026-03-13\n- membership level: Silver\n- order subtotal: $91.93\n\nFine print from the bottom of the advertisement:\n† The benefit is reserved for delivery bound for Brenmoor. Products in the electronics category are excluded from this offer.\n* Delivery to Brenmoor is the sole route to the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-341548 from Mira Castell forfeit free shipping under the advertised terms, as set out by the advertisement and its fine print?"
 },
 {
  "qid": "q02a4d3c664",
  "kind": "yes/no",
  "text": "Support chat about order ORD-736594:\nMira Castell: Hi, I placed order ORD-736594 on 1 May 2026 for item SKU-48333, and the order subtotal was $223.09.\nAgent: Thanks. The item is in the furniture product category, its price status is refurbished, and it ships to the Greyhaven delivery region.\nAgent: Your membership level is Black.\nMira Castell: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\nDouble reward points on every purchase†\n\nA bit of dusting goes a long way. Thanks, and happy handling from Birchwood Linens.\n\nFine print:\n† Only a delivery to Greyhaven qualifies for this offer.\n* Excludes all items with refurbished status. Delivery to Greyhaven only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertised terms, which include the headline and its small print, does Mira Castell come with free shipping on order ORD-736594?"
 },
 {
  "qid": "qd65fafa074",
  "kind": "yes/no",
  "text": "Order ORD-562064 placed by Priya Raman:\n| field | value |\n| --- | --- |\n| item | SKU-17978 |\n| product category | kitchenware |\n| price status | open box |\n| delivery region | Arvale |\n| order date | 11 Aug 2026 |\n| membership level | Blue |\n| order subtotal | 243.91 USD |\n\nAdvertisement from Tidewell Supply:\nDouble reward points on every purchase*\n\nFine print:\n* Items at clearance pricing are withheld from this benefit. Goods in the kitchenware category fall outside the headline benefit.\n\nFresh finds and a brisk checkout await, so thanks for choosing Tidewell Supply for your order.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, does order ORD-562064 from Priya Raman get double reward points under its headline and that headline's small print?"
 },
 {
  "qid": "qa165f85abf",
  "kind": "choice",
  "text": "Order ORD-438199 placed by Mira Castell:\n| field | value |\n| --- | --- |\n| item | SKU-55720 |\n| product category | kitchenware |\n| price status | refurbished |\n| delivery region | Brenmoor |\n| order date | 2026-07-04 |\n| membership level | Premier |\n| order subtotal | $170.33 |\n\nAdvertisement from Copperleaf Kitchen:\nA lifetime warranty on everything we sell*\n\n{\"title\": \"Practical shopping from Copperleaf Kitchen\", \"subtitle\": \"Tidy labels and a neat layout help you find things fast\", \"button\": \"See the range\"}\n\nFine print:\n* Reserved for members at Plus or below.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms, which condition attached to the lifetime warranty does order ORD-438199 from Mira Castell miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q7fa7332042",
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
  "qid": "qf5bb67e473",
  "kind": "yes/no",
  "text": "Order ORD-347603 placed by Priya Raman:\n| field | value |\n| --- | --- |\n| item | SKU-49118 |\n| product category | bedding |\n| price status | clearance |\n| delivery region | Calderon |\n| order date | 2026-06-24 |\n| membership level | Black |\n| order subtotal | $25 |\n\nAdvertisement from Northvale Audio:\nFree assembly with every delivery*\n\nTake a breath at Northvale Audio\nA calm, uncluttered space to browse beautiful things.\n\nFine print:\n* Valid for orders placed on or before 2026-07-26. Subtotal of $25 or more required. The benefit is reserved for delivery bound for Calderon.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that, under the advertised terms, Priya Raman's order ORD-347603 does not get free assembly, according to what the advertisement says?"
 },
 {
  "qid": "q6d31770bc2",
  "kind": "yes/no",
  "text": "Order ORD-269004 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-90730 |\n| product category | pet supplies |\n| price status | pre-order |\n| delivery region | Calderon |\n| order date | Saturday, 28 March 2026 |\n| membership level | Plus |\n| order subtotal | $50.00 |\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nBrowsing here is easy and the staff are happy to help you find what suits your home. Pop in and see what Copperleaf Kitchen has on the shelves.\n\nFine print:\n* Order subtotal exceeds $50.00. Each order needs delivery to Calderon to earn the benefit. Qualifying orders include the date Saturday, 28 February 2026 and every later day.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-269004 from Ravi Anand get free assembly?"
 },
 {
  "qid": "q8507f954cc",
  "kind": "yes/no",
  "text": "Support chat about order ORD-160626:\nTomas Ferreira: Hi, I placed order ORD-160626 on 15 Aug 2026 for item SKU-16308, and the order subtotal was 30.60 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Hollin delivery region.\nAgent: Your membership level is Bronze.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree shipping on every order*\n\nStop by Juniper Gadgets for the essentials you use at home.\n\nFine print:\n* For the offer, the order subtotal must be higher than 35.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-160626 placed by Tomas Ferreira lose out on free shipping?"
 },
 {
  "qid": "q7c01bf469c",
  "kind": "choice",
  "text": "Order ORD-292996 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-93640 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Greyhaven |\n| order date | 2026-01-25 |\n| membership level | Plus |\n| order subtotal | 95.91 USD |\n\nAdvertisement from Harborlight Goods:\nFree assembly with every delivery*\nA lifetime warranty on everything we sell†\n\nFine print:\n* Qualifying orders are placed before 2026-01-26, excluding that date. For the offer, the order subtotal must be higher than 75.00 USD.\n† Orders headed for delivery in Dunmere are kept out of this offer.\n\n{\"title\": \"Harborlight Goods app\", \"subtitle\": \"Browse the range, build a list, and check out quickly\", \"button\": \"Get started\"}",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe advertised terms attach conditions to free assembly; which, if any, does order ORD-292996 from Jonah Pryce miss?",
  "options": [
   "The order-subtotal condition",
   "The order-date condition",
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q6750bc9e8d",
  "kind": "yes/no",
  "text": "Order ORD-515339 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-90936 |\n| product category | bedding |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | May 3, 2026 |\n| membership level | Basic |\n| order subtotal | $75 |\n\nAdvertisement from Harborlight Goods:\nDouble reward points on every purchase*\n\nFine print:\n* Order subtotal must go beyond $75. Only members at the Elite level or higher may take part.\n\nIt is lovely to have you at Harborlight Goods. Take a relaxed moment looking at your basket.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, does order ORD-515339 from Jonah Pryce get double reward points under its headline and that headline's small print?"
 },
 {
  "qid": "q854cfed399",
  "kind": "yes/no",
  "text": "Advertisement from Northvale Audio:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Items under the bedding category are carved out of this offer.\n† Every delivery bound for Calderon lies outside the headline offer. Valid for orders placed before 2026-08-31.\n\nKnown to the neighbourhood\nFamiliar faces greet you at Northvale Audio, a little place with a big heart for the street.\n\nOrder ORD-235934 placed by Mira Castell:\n- item: SKU-77467\n- product category: bedding\n- price status: clearance\n- delivery region: Calderon\n- order date: 2026-09-19\n- membership level: Basic\n- order subtotal: 109.28 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that the order ORD-235934 placed by Mira Castell does not get free returns under the advertised terms, as what the advertisement says indicates?"
 },
 {
  "qid": "q85d2cc9f12",
  "kind": "yes/no",
  "text": "Support chat about order ORD-300420:\nSelin Yilmaz: Hi, I placed order ORD-300420 on Sunday, 13 September 2026 for item SKU-32482, and the order subtotal was 119.41 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Calderon delivery region.\nAgent: Your membership level is Premier.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree gift wrapping at checkout*\nFree shipping on every order†\n\nGood stock, well arranged\nWalk around Oakhurst Interiors and see how neatly things are laid out, with clear signs and helpful shelves.\n\nFine print:\n† Valid for orders placed before Saturday, 22 August 2026.\n* The subtotal of the order needs to be 100.00 USD or higher.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the ad and its small print, does order ORD-300420 from Selin Yilmaz lose out on free shipping under the advertised terms?"
 },
 {
  "qid": "q2ed2340e9b",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree assembly with every delivery*\n\nSerene surroundings and timeless craft at Tidewell Supply\nPure lines, gentle light and a graceful selection.\n\nFine print:\n* Goods filed under a different category from pet supplies fall outside the benefit. Order subtotal strictly more than $200.\n\nOrder ORD-317422 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-22972 |\n| product category | sports gear |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | Friday, 15 May 2026 |\n| membership level | Premier |\n| order subtotal | 227.50 USD |",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nHas Ines Duarte lost out on free assembly with order ORD-317422, judging by the advertisement and its fine print?"
 },
 {
  "qid": "q9d3651cca5",
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
  "qid": "qec1679525a",
  "kind": "yes/no",
  "text": "Order ORD-832634 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-71380 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Hollin |\n| order date | 11 May 2026 |\n| membership level | Black |\n| order subtotal | $200.00 |\n\nAdvertisement from Northvale Audio:\nFree assembly with every delivery*\n\nTake a breath at Northvale Audio\nA calm, uncluttered space to browse beautiful things.\n\nFine print:\n* Valid for orders placed on or before 19 June 2026. Subtotal of $200.00 or more required. The benefit is reserved for delivery bound for Hollin.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that, under the advertised terms, Clara Voss's order ORD-832634 does not get free assembly, according to what the advertisement says?"
 },
 {
  "qid": "q76c0d06054",
  "kind": "yes/no",
  "text": "Support chat about order ORD-682914:\nFelix Moreau: Hi, I placed order ORD-682914 on 2026-07-23 for item SKU-66324, and the order subtotal was $75.00.\nAgent: Thanks. The item is in the kitchenware product category, its price status is regular price, and it ships to the Arvale delivery region.\nAgent: Your membership level is Green.\nFelix Moreau: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nFree installation for every appliance*\n\nWelcome to our catalogue\nFamily favourites, practical picks and friendly ideas for busy households, gathered together by the team at Larkspur Playthings.\n\nFine print:\n* Valid only for items in the furniture category. Applies to order subtotals of $75.00 or more.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Larkspur Playthings levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, does order ORD-682914 from Felix Moreau fail to receive free installation under the advertised terms?"
 },
 {
  "qid": "qc73eaa573d",
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
  "qid": "qfb508c2f69",
  "kind": "choice",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nBring the family along\nWrenfield Outdoor is a welcoming place for parents, grandparents and children, with friendly staff ready to help.\n\nFine print:\n† Orders headed for delivery in Brenmoor are kept out of this offer.\n* Applies to orders placed ahead of Monday, July 27, 2026. Valid for orders whose subtotal is $75 or more.\n\nOrder ORD-221730 placed by Owen Mensah:\n- item: SKU-51500\n- product category: furniture\n- price status: regular price\n- delivery region: Brenmoor\n- order date: Sunday, July 26, 2026\n- membership level: Gold\n- order subtotal: $74.99",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, drawn from the ad and its small print attached to free shipping, does order ORD-221730 from Owen Mensah miss, if any?",
  "options": [
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q7ee8659a4a",
  "kind": "yes/no",
  "text": "Advertisement from Northvale Audio:\nDouble reward points on every purchase*\n\nTidy it up with a soft cloth once the fun has ended, and store it somewhere cool. We hope Northvale Audio brings smiles to your household.\n\nFine print:\n* Orders dated on or before Saturday, September 5, 2026 count. Items with pre-order status fall outside this benefit.\n\nOrder ORD-803663 placed by Dana Okafor:\n- item: SKU-22273\n- product category: pet supplies\n- price status: refurbished\n- delivery region: Arvale\n- order date: Thursday, August 20, 2026\n- membership level: Plus\n- order subtotal: $151.29",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nHaving read the ad's headline and the small print that goes with it, does order ORD-803663 from Dana Okafor receive double reward points?"
 },
 {
  "qid": "q3c8a13ecd0",
  "kind": "yes/no",
  "text": "Advertisement from Pebblestone Garden:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nHi from Pebblestone Garden, your local shop is buzzing and the kettle is on.\n\nOrder ORD-767061 placed by Owen Mensah:\n- item: SKU-89544\n- product category: bedding\n- price status: regular price\n- delivery region: Calderon\n- order date: Friday, July 31, 2026\n- membership level: Bronze\n- order subtotal: 62.72 USD\n\nFine print from the bottom of the advertisement:\n† The benefit is reserved for delivery bound for Calderon. Products in the toys category are excluded from this offer.\n* Delivery to Fallowmere is the sole route to the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-767061 from Owen Mensah forfeit free shipping under the advertised terms, as set out by the advertisement and its fine print?"
 },
 {
  "qid": "q555a332e78",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree installation for every appliance*\n\nFine print:\n* Only a delivery to Dunmere qualifies for this offer. The order subtotal must be strictly greater than 35.00 USD.\n\nGrab the kids and take a happy look at what you picked from Tidewell Supply.\n\nOrder ORD-209627 placed by Nadia Haddad:\n- item: SKU-14848\n- product category: toys\n- price status: final sale\n- delivery region: Dunmere\n- order date: Tuesday, June 9, 2026\n- membership level: Basic\n- order subtotal: 37.27 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nMeasured against the advertisement and its fine print, does order ORD-209627 from Nadia Haddad lose out on free installation?"
 },
 {
  "qid": "q5ea90aea8a",
  "kind": "choice",
  "text": "Support chat about order ORD-774024:\nClara Voss: Hi, I placed order ORD-774024 on 7 March 2026 for item SKU-51788, and the order subtotal was $141.73.\nAgent: Thanks. The item is in the pet supplies product category, its price status is pre-order, and it ships to the Hollin delivery region.\nAgent: Your membership level is Platinum.\nClara Voss: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree shipping on every order*\nDouble reward points on every purchase†\n\nPop in and say hello\nOur friendly folks at Juniper Gadgets are keen to meet you and guide you to a piece you adore.\n\nFine print:\n* Orders placed on the date 20 February 2026 count, and so do all later orders.\n† Items in the pet supplies product category are excluded.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOn order ORD-774024, which headline offers does Clara Voss actually receive, going offer by offer through what the advertisement says?",
  "options": [
   "Neither offer",
   "Only double reward points",
   "Only free shipping",
   "Both offers"
  ]
 },
 {
  "qid": "q0fbfada348",
  "kind": "yes/no",
  "text": "Order ORD-222742 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-53874 |\n| product category | kitchenware |\n| price status | open box |\n| delivery region | Arvale |\n| order date | Sunday, March 8, 2026 |\n| membership level | Green |\n| order subtotal | $144.80 |\n\nAdvertisement from Northvale Audio:\nFree installation for every appliance*\n\nFine print:\n* Valid for orders placed before Sunday, March 1, 2026.\n\nThank you kindly for picking Northvale Audio. Let your new piece rest in a quiet corner away from direct sun and dust it gently with a soft duster.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhen the headline and its small print are read against the advertised terms, does order ORD-222742 from Tomas Ferreira receive free installation?"
 },
 {
  "qid": "q39efec099c",
  "kind": "choice",
  "text": "Advertisement from Cedarline Living:\nDouble reward points on every purchase*\nFree installation for every appliance†\n\nFine print:\n* Orders taken on Monday, 28 September 2026 and any day later count.\n† Valid: any order taken on or before Sunday, 27 September 2026.\n\nWelcome to the family at Cedarline Living. A quick buff with a soft cloth leaves it looking sharp.\n\nOrder ORD-676707 placed by Kofi Asante:\n- item: SKU-98263\n- product category: electronics\n- price status: clearance\n- delivery region: Calderon\n- order date: Sunday, 27 September 2026\n- membership level: Blue\n- order subtotal: 42.16 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOn order ORD-676707, which headline offers does Kofi Asante actually receive, going offer by offer through what the advertisement says?",
  "options": [
   "Only double reward points",
   "Both offers",
   "Neither offer",
   "Only free installation"
  ]
 },
 {
  "qid": "qcfb19474ca",
  "kind": "yes/no",
  "text": "Support chat about order ORD-245098:\nOwen Mensah: Hi, I placed order ORD-245098 on Friday, October 16, 2026 for item SKU-46491, and the order subtotal was $118.62.\nAgent: Thanks. The item is in the kitchenware product category, its price status is regular price, and it ships to the Arvale delivery region.\nAgent: Your membership level is Bronze.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree shipping on every order*\n\nStop by Juniper Gadgets for the essentials you use at home.\n\nFine print:\n* For the offer, the order subtotal must be higher than $100.00.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-245098 placed by Owen Mensah lose out on free shipping?"
 },
 {
  "qid": "q3494bf172a",
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
  "qid": "q253545a606",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree assembly with every delivery*\n\nFresh arrivals, clean lines and quick browsing. Welcome to Bluecrest Sports.\n\nOrder ORD-931168 placed by Hugo Lindqvist:\n- item: SKU-81161\n- product category: garden tools\n- price status: regular price\n- delivery region: Calderon\n- order date: 2026-04-08\n- membership level: Black\n- order subtotal: $83.47\n\nFine print from the bottom of the advertisement:\n* Eligibility for the benefit is restricted to the pet supplies product category. Reserved for members ranked Black or higher.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich small-print condition in the ad, attached to free assembly, does order ORD-931168 from Hugo Lindqvist miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition",
   "The membership-level condition"
  ]
 },
 {
  "qid": "qe66b46c2ee",
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
  "qid": "q292f3241db",
  "kind": "yes/no",
  "text": "Advertisement from Oakhurst Interiors:\nA lifetime warranty on everything we sell*\n\nFine print:\n* Orders must be placed before 2026-10-04, and the day itself is excluded. Anything with delivery in Eskarth is excluded from the headline benefit.\n\nSensible choices and straight-talking service help shape Oakhurst Interiors for busy shoppers.\n\nOrder ORD-866597 placed by Ines Duarte:\n- item: SKU-26250\n- product category: furniture\n- price status: regular price\n- delivery region: Greyhaven\n- order date: 2026-10-02\n- membership level: Bronze\n- order subtotal: $190.04",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says, with its headline and small print together, does order ORD-866597 from Ines Duarte receive the lifetime warranty?"
 },
 {
  "qid": "q4b2bfa54ec",
  "kind": "choice",
  "text": "Advertisement from Copperleaf Kitchen:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\nOur corner of town is brighter with Copperleaf Kitchen in it, so stop in for a warm, personal welcome.\n\nOrder ORD-773861 placed by Aiko Brandt:\n- item: SKU-26604\n- product category: furniture\n- price status: clearance\n- delivery region: Greyhaven\n- order date: 22 Sep 2026\n- membership level: Gold\n- order subtotal: $154.74\n\nFine print from the bottom of the advertisement:\n* Items whose status is clearance are excluded.\n† Orders must be placed before 23 Sep 2026, and the day itself is excluded.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Copperleaf Kitchen levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-773861 from Aiko Brandt, which headline offers hold up under the ad and its small print, offer by offer?",
  "options": [
   "Only free gift wrapping",
   "Only free installation",
   "Neither offer",
   "Both offers"
  ]
 },
 {
  "qid": "q7099267fd4",
  "kind": "yes/no",
  "text": "Order ORD-399120 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-65079 |\n| product category | garden tools |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | Thursday, July 9, 2026 |\n| membership level | Basic |\n| order subtotal | 73.44 USD |\n\nAdvertisement from Harborlight Goods:\nFree returns on every purchase*\n\nQuick tip: wipe it down with a microfibre cloth and keep the surface clean. Thanks for picking Harborlight Goods.\n\nFine print:\n* Valid for orders placed before Thursday, August 6, 2026. Members at the Plus level or higher only.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nPer the advertisement and its fine print, is it true that order ORD-399120 from Nadia Haddad does not get free returns under the advertised terms?"
 },
 {
  "qid": "q607be8ac10",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nDouble reward points on every purchase*\n\nFine print:\n* Applies to Plus level and higher members. Headline benefit is confined to delivery landing in Greyhaven.\n\nStep into Larkspur Playthings and see why our edit is admired for craftsmanship, clarity and character.\n\nOrder ORD-332984 placed by Jonah Pryce:\n- item: SKU-23660\n- product category: bedding\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: 1 June 2026\n- membership level: Plus\n- order subtotal: $205.51",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad and its small print say that order ORD-332984 from Jonah Pryce gets double reward points?"
 },
 {
  "qid": "q8bcd9b7b4a",
  "kind": "choice",
  "text": "Advertisement from Birchwood Linens:\nFree assembly with every delivery*\nWe match any lower price†\n\nFine print:\n* Valid: any order taken on or before July 6, 2026. Every item in the bedding category falls outside the offer.\n† Valid: any order taken on or before July 5, 2026.\n\nSubject: Cosy, gentle and kid-friendly\nHello there, families, and welcome. Birchwood Linens is a happy place for little ones and grown-ups alike.\n\nOrder ORD-464452 placed by Priya Raman:\n- item: SKU-85949\n- product category: furniture\n- price status: regular price\n- delivery region: Brenmoor\n- order date: July 6, 2026\n- membership level: Plus\n- order subtotal: $78.27",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIf any, which condition in the advertisement and its fine print attached to the price match does order ORD-464452 from Priya Raman miss?",
  "options": [
   "The product-category condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q4d388581e3",
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
  "qid": "qdb7be10035",
  "kind": "choice",
  "text": "Advertisement from Marigold Pets:\nDouble reward points on every purchase*\nFree assembly with every delivery†\n\nA gentle welcome awaits at Marigold Pets, where handsome goods are arranged with care.\n\nFine print:\n† Applies to orders placed ahead of 18 June 2026.\n* Orders placed by 17 June 2026 are valid, and the stated day is included.\n\nOrder ORD-180306 placed by Mira Castell:\n- item: SKU-28197\n- product category: bedding\n- price status: open box\n- delivery region: Brenmoor\n- order date: 18 June 2026\n- membership level: Green\n- order subtotal: 61.80 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecked offer by offer against the ad and its small print, which headline offers does Mira Castell actually get with order ORD-180306?",
  "options": [
   "Only free assembly",
   "Neither offer",
   "Only double reward points",
   "Both offers"
  ]
 },
 {
  "qid": "q529cecc413",
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
  "qid": "q91fd8cc6c1",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree gift wrapping at checkout*\nDouble reward points on every purchase†\n\nFine print:\n* Anything with delivery in Fallowmere is excluded from the headline benefit. Valid: any order taken on or before Monday, March 2, 2026.\n† Valid on orders over $150.\n\nGood coffee, good company and a little bit of fun at Marigold Pets. Pop by and see what we have been up to.\n\nOrder ORD-955847 placed by Selin Yilmaz:\n- item: SKU-30632\n- product category: pet supplies\n- price status: regular price\n- delivery region: Eskarth\n- order date: Tuesday, March 3, 2026\n- membership level: Blue\n- order subtotal: $150.01",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Marigold Pets levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print together, does order ORD-955847 from Selin Yilmaz lose out on free gift wrapping under the advertised terms?"
 },
 {
  "qid": "qcaaf345e1c",
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
  "qid": "qf6054a4d7d",
  "kind": "yes/no",
  "text": "Advertisement from Northvale Audio:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Items under the toys category are carved out of this offer.\n† Every delivery bound for Greyhaven lies outside the headline offer. Valid for orders placed before 2026-05-29.\n\nKnown to the neighbourhood\nFamiliar faces greet you at Northvale Audio, a little place with a big heart for the street.\n\nOrder ORD-606502 placed by Jonah Pryce:\n- item: SKU-22064\n- product category: sports gear\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 2026-05-06\n- membership level: Premier\n- order subtotal: 92.88 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that the order ORD-606502 placed by Jonah Pryce does not get free returns under the advertised terms, as what the advertisement says indicates?"
 },
 {
  "qid": "q97ee61c385",
  "kind": "yes/no",
  "text": "Support chat about order ORD-899052:\nTomas Ferreira: Hi, I placed order ORD-899052 on 21 February 2026 for item SKU-91003, and the order subtotal was $86.93.\nAgent: Thanks. The item is in the kitchenware product category, its price status is final sale, and it ships to the Calderon delivery region.\nAgent: Your membership level is Platinum.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree assembly with every delivery*\n\nLittle ones and grown ups, come along to Cedarline Living.\nImaginative play is a joyful way to learn and laugh together.\nOur cozy corners are ready for busy hands and curious minds.\n*Order by 4 March 2026 at the latest. Excludes delivery to Brenmoor.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, is it true that order ORD-899052 from Tomas Ferreira does not get free assembly under the advertised terms?"
 },
 {
  "qid": "q4dbc46a375",
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
  "qid": "q8e554ab977",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nFree installation for every appliance*\nDouble reward points on every purchase†\n\nFine print:\n† Members at the Premier level or higher only. Delivery to Hollin is the sole route to the headline benefit.\n* Only orders placed before November 18, 2026 count toward this offer. Stock with pre-order status is excluded from this benefit.\n\nWe appreciate your custom at Brightwell Home. Look closely at the stitching and tighten loose fixings gently.\n\nOrder ORD-284642 placed by Owen Mensah:\n- item: SKU-40262\n- product category: electronics\n- price status: final sale\n- delivery region: Hollin\n- order date: October 19, 2026\n- membership level: Premier\n- order subtotal: 247.24 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Brightwell Home levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDo the advertised terms, taking in the headline and small print, let Owen Mensah get free installation on order ORD-284642?"
 },
 {
  "qid": "q6770e32d6b",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\nFree assembly with every delivery†\n\nWith thanks from the team at Juniper Gadgets, we hope you enjoy your new item. Clean it gently with a soft dry cloth so it stays looking lovely.\n\nFine print:\n* Placed on or after Wednesday, August 26, 2026, the order qualifies. An order qualifies with a subtotal of $200 or more.\n† Shoppers get the headline benefit solely for delivery in Hollin. Order subtotal strictly more than $150.\n\nOrder ORD-285520 placed by Tomas Ferreira:\n- item: SKU-10182\n- product category: toys\n- price status: pre-order\n- delivery region: Hollin\n- order date: Wednesday, August 26, 2026\n- membership level: Black\n- order subtotal: $150.01",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does order ORD-285520 from Tomas Ferreira fail to get free gift wrapping?"
 },
 {
  "qid": "q61e87292b1",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nDouble reward points on every purchase*\n\nFine print:\n* The order subtotal must be at least $200 for this offer to apply. Valid for orders placed before May 19, 2026.\n\nThanks kindly from the folks at Bluecrest Sports. Enjoy a cuppa and a gentle glance at your basket.\n\nOrder ORD-660104 placed by Nadia Haddad:\n- item: SKU-41440\n- product category: electronics\n- price status: regular price\n- delivery region: Greyhaven\n- order date: May 19, 2026\n- membership level: Black\n- order subtotal: $200",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nAgainst the advertisement and its fine print, which condition attached to double reward points does Nadia Haddad's order ORD-660104 miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q324ebb270c",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree installation for every appliance*\nA lifetime warranty on everything we sell†\n\nFine print:\n* Items marked with the refurbished status fall outside the benefit set out here. Headline benefit is confined to delivery landing in Greyhaven.\n† Shoppers get the headline benefit solely for delivery in Arvale. Items marked with the refurbished status fall outside the benefit set out here.\n\nA cosy trip for the children and a relaxed stroll for you, right here at Marigold Pets.\n\nOrder ORD-758313 placed by Ines Duarte:\n- item: SKU-52856\n- product category: sports gear\n- price status: open box\n- delivery region: Arvale\n- order date: Saturday, 28 February 2026\n- membership level: Green\n- order subtotal: $160.42",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, does order ORD-758313 from Ines Duarte fail to get the lifetime warranty under the advertised terms?"
 },
 {
  "qid": "q9342ef43d4",
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
  "qid": "qa4fd3d8f68",
  "kind": "yes/no",
  "text": "Order ORD-195773 placed by Kofi Asante:\n| field | value |\n| --- | --- |\n| item | SKU-60774 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Hollin |\n| order date | October 23, 2026 |\n| membership level | Basic |\n| order subtotal | 30.43 USD |\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nBrowsing here is easy and the staff are happy to help you find what suits your home. Pop in and see what Copperleaf Kitchen has on the shelves.\n\nFine print:\n* Order subtotal exceeds 25.00 USD. Each order needs delivery to Hollin to earn the benefit. Qualifying orders include the date October 5, 2026 and every later day.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-195773 from Kofi Asante get free assembly?"
 }
]
