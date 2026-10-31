# G5-H blind read T07-blind_read-e0c5c384-000 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/pilot_i1/g5h/answers/T07-blind_read-e0c5c384-000.json

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
  "qid": "q239d2eb86c",
  "kind": "yes/no",
  "text": "Advertisement from Pebblestone Garden:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nHi from Pebblestone Garden, your local shop is buzzing and the kettle is on.\n\nOrder ORD-341548 placed by Mira Castell:\n- item: SKU-78509\n- product category: furniture\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 2026-03-13\n- membership level: Silver\n- order subtotal: $91.93\n\nFine print from the bottom of the advertisement:\n† The benefit is reserved for delivery bound for Brenmoor. Products in the electronics category are excluded from this offer.\n* Delivery to Brenmoor is the sole route to the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-341548 from Mira Castell forfeit free shipping under the advertised terms, as set out by the advertisement and its fine print?"
 },
 {
  "qid": "qeb5b3421b7",
  "kind": "choice",
  "text": "Advertisement from Larkspur Playthings:\nA lifetime warranty on everything we sell*\nFree assembly with every delivery†\n\nWe hope the things you picked at Larkspur Playthings suit your plans. Take a look at your basket, then check out when you are set.\n\nFine print:\n† Valid on orders of 75.00 USD or more. Headline benefit is limited to delivery in Dunmere.\n* Orders must reach 35.00 USD or more in subtotal. An order whose delivery goes to Arvale falls outside the headline benefit.\n\nOrder ORD-242727 placed by Hugo Lindqvist:\n- item: SKU-62219\n- product category: pet supplies\n- price status: final sale\n- delivery region: Dunmere\n- order date: 4 August 2026\n- membership level: Premier\n- order subtotal: 35.00 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nPer what the advertisement says, which condition in the small print attached to free assembly does Hugo Lindqvist's order ORD-242727 miss, if any?",
  "options": [
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "qf03da520b7",
  "kind": "yes/no",
  "text": "Advertisement from Pebblestone Garden:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nHi from Pebblestone Garden, your local shop is buzzing and the kettle is on.\n\nOrder ORD-767061 placed by Owen Mensah:\n- item: SKU-89544\n- product category: bedding\n- price status: regular price\n- delivery region: Calderon\n- order date: Friday, July 31, 2026\n- membership level: Bronze\n- order subtotal: 62.72 USD\n\nFine print from the bottom of the advertisement:\n† The benefit is reserved for delivery bound for Calderon. Products in the toys category are excluded from this offer.\n* Delivery to Fallowmere is the sole route to the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-767061 from Owen Mensah forfeit free shipping under the advertised terms, as set out by the advertisement and its fine print?"
 },
 {
  "qid": "qcdcd4d9ae1",
  "kind": "yes/no",
  "text": "Support chat about order ORD-743714:\nOwen Mensah: Hi, I placed order ORD-743714 on August 22, 2026 for item SKU-70899, and the order subtotal was 71.79 USD.\nAgent: Thanks. The item is in the bedding product category, its price status is pre-order, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Silver.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nA lifetime warranty on everything we sell*\n\nSubject: Plans worth making together\nHello there,\nCedarline Living invites your family to enjoy fresh air and easygoing fun. We are happy to help you plan a family outing. Thank you for being part of our community, and we look forward to welcoming you.\n*Valid on orders of 100.00 USD or more.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Cedarline Living levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement alongside its fine print, does Owen Mensah receive the lifetime warranty on order ORD-743714?"
 },
 {
  "qid": "q85cf7b6858",
  "kind": "choice",
  "text": "Support chat about order ORD-936040:\nKofi Asante: Hi, I placed order ORD-936040 on 2026-06-20 for item SKU-67120, and the order subtotal was 50.01 USD.\nAgent: Thanks. The item is in the electronics product category, its price status is pre-order, and it ships to the Hollin delivery region.\nAgent: Your membership level is Bronze.\nKofi Asante: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\n{\"title\": \"Browse the new range at Cedarline Living\", \"subtitle\": \"Scroll the favourites and find a piece to love\", \"button\": \"Start looking\"}\n\nFine print:\n† Only members at the Silver level or higher may take part.\n* Order subtotal exceeds 50.00 USD. An order whose delivery goes to Hollin falls outside the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the ad and its small print attached to free gift wrapping does order ORD-936040 from Kofi Asante miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qe5b9125a6e",
  "kind": "choice",
  "text": "Support chat about order ORD-496629:\nDana Okafor: Hi, I placed order ORD-496629 on 30 Apr 2026 for item SKU-69872, and the order subtotal was $67.03.\nAgent: Thanks. The item is in the bedding product category, its price status is open box, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Premier.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nFree returns on every purchase*\nDouble reward points on every purchase†\n\nWe are so glad you came into Wrenfield Outdoor. Please take a warm look at your basket and keep going.\n\nFine print:\n* Excludes the bedding category. Every order placed on or after 26 Apr 2026 is covered by the offer.\n† Excludes all items with open box status. Qualifying orders: subtotal $75 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe small print that the advertisement attaches to free returns: which condition, if any, does order ORD-496629 from Dana Okafor miss?",
  "options": [
   "The order-date condition",
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition",
   "The product-category condition"
  ]
 },
 {
  "qid": "qb2a03bc668",
  "kind": "yes/no",
  "text": "Support chat about order ORD-464687:\nInes Duarte: Hi, I placed order ORD-464687 on 26 February 2026 for item SKU-19134, and the order subtotal was 35.01 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is clearance, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Green.\nInes Duarte: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nWe match any lower price*\nFree returns on every purchase†\n\nThoughtfully sourced living\nExplore the range at Larkspur Playthings, where careful craft meets the tastes of contemporary homes.\n\nFine print:\n* Orders count only with a subtotal beyond $35.\n† An order placed on or before 22 March 2026 qualifies. Customers at the Green tier or lower can use this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print together, does order ORD-464687 from Ines Duarte lose out on free returns under the advertised terms?"
 },
 {
  "qid": "qf5be0686bd",
  "kind": "yes/no",
  "text": "Order ORD-399120 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-65079 |\n| product category | garden tools |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | Thursday, July 9, 2026 |\n| membership level | Basic |\n| order subtotal | 73.44 USD |\n\nAdvertisement from Harborlight Goods:\nFree returns on every purchase*\n\nQuick tip: wipe it down with a microfibre cloth and keep the surface clean. Thanks for picking Harborlight Goods.\n\nFine print:\n* Valid for orders placed before Thursday, August 6, 2026. Members at the Plus level or higher only.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nPer the advertisement and its fine print, is it true that order ORD-399120 from Nadia Haddad does not get free returns under the advertised terms?"
 },
 {
  "qid": "q1d8a964a05",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree gift wrapping at checkout*\nDouble reward points on every purchase†\n\nFine print:\n* Anything with delivery in Fallowmere is excluded from the headline benefit. Valid: any order taken on or before Monday, March 2, 2026.\n† Valid on orders over $150.\n\nGood coffee, good company and a little bit of fun at Marigold Pets. Pop by and see what we have been up to.\n\nOrder ORD-955847 placed by Selin Yilmaz:\n- item: SKU-30632\n- product category: pet supplies\n- price status: regular price\n- delivery region: Eskarth\n- order date: Tuesday, March 3, 2026\n- membership level: Blue\n- order subtotal: $150.01",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Marigold Pets levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print together, does order ORD-955847 from Selin Yilmaz lose out on free gift wrapping under the advertised terms?"
 },
 {
  "qid": "q8aa7eac333",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree installation for every appliance*\nA lifetime warranty on everything we sell†\n\nFine print:\n* Items marked with the refurbished status fall outside the benefit set out here. Headline benefit is confined to delivery landing in Greyhaven.\n† Shoppers get the headline benefit solely for delivery in Arvale. Items marked with the refurbished status fall outside the benefit set out here.\n\nA cosy trip for the children and a relaxed stroll for you, right here at Marigold Pets.\n\nOrder ORD-758313 placed by Ines Duarte:\n- item: SKU-52856\n- product category: sports gear\n- price status: open box\n- delivery region: Arvale\n- order date: Saturday, 28 February 2026\n- membership level: Green\n- order subtotal: $160.42",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, does order ORD-758313 from Ines Duarte fail to get the lifetime warranty under the advertised terms?"
 },
 {
  "qid": "q541e3f7ef9",
  "kind": "yes/no",
  "text": "Support chat about order ORD-899052:\nTomas Ferreira: Hi, I placed order ORD-899052 on 21 February 2026 for item SKU-91003, and the order subtotal was $86.93.\nAgent: Thanks. The item is in the kitchenware product category, its price status is final sale, and it ships to the Calderon delivery region.\nAgent: Your membership level is Platinum.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree assembly with every delivery*\n\nLittle ones and grown ups, come along to Cedarline Living.\nImaginative play is a joyful way to learn and laugh together.\nOur cozy corners are ready for busy hands and curious minds.\n*Order by 4 March 2026 at the latest. Excludes delivery to Brenmoor.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, is it true that order ORD-899052 from Tomas Ferreira does not get free assembly under the advertised terms?"
 },
 {
  "qid": "qf7cdda4612",
  "kind": "choice",
  "text": "Support chat about order ORD-190135:\nPriya Raman: Hi, I placed order ORD-190135 on March 23, 2026 for item SKU-73591, and the order subtotal was 237.38 USD.\nAgent: Thanks. The item is in the electronics product category, its price status is regular price, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Elite.\nPriya Raman: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nFree installation for every appliance*\nDouble reward points on every purchase†\n\nSubject: Welcome to Pebblestone Garden\nDear friend,\nWe are delighted to share our refined home pieces, chosen with a quiet eye for craft.\n\nFine print:\n† Only the garden tools category earns the headline benefit.\n* For Premier members and above.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does order ORD-190135 from Priya Raman truly get, by the terms set out in what the advertisement says?",
  "options": [
   "Only double reward points",
   "Only free installation",
   "Neither offer",
   "Both offers"
  ]
 },
 {
  "qid": "q7a86324efa",
  "kind": "choice",
  "text": "Order ORD-489649 placed by Hugo Lindqvist:\n| field | value |\n| --- | --- |\n| item | SKU-36853 |\n| product category | bedding |\n| price status | pre-order |\n| delivery region | Brenmoor |\n| order date | 23 Oct 2026 |\n| membership level | Black |\n| order subtotal | 74.99 USD |\n\nAdvertisement from Northvale Audio:\nWe match any lower price*\nDouble reward points on every purchase†\n\nFine print:\n† Items marked with the clearance status fall outside the benefit set out here.\n* Earlier orders are accepted, and so is the date 23 Sep 2026 itself. Valid for orders whose subtotal is $75 or more.\n\nHello from the team at Northvale Audio! Pop it on a shelf where it gets to enjoy the view and a little sunshine.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the small print offer by offer, which of the advertised terms does Hugo Lindqvist actually get on order ORD-489649?",
  "options": [
   "Only double reward points",
   "Both offers",
   "Neither offer",
   "Only the price match"
  ]
 },
 {
  "qid": "q5f7f545ab9",
  "kind": "yes/no",
  "text": "Order ORD-357606 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-92739 |\n| product category | kitchenware |\n| price status | final sale |\n| delivery region | Hollin |\n| order date | 14 May 2026 |\n| membership level | Green |\n| order subtotal | $61.07 |\n\nAdvertisement from Northvale Audio:\nDouble reward points on every purchase*\nFree assembly with every delivery†\n\nWe hope your visit to Northvale Audio leaves you smiling and feeling welcome.\n\nFine print:\n* Reserved for members ranked Blue or higher. The order subtotal must be at least $50 for this offer to apply.\n† Placed before 15 May 2026 counts; that very day is excluded.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says alongside the advertised terms, does order ORD-357606 from Ravi Anand fail to secure double reward points?"
 },
 {
  "qid": "q526ac0214d",
  "kind": "yes/no",
  "text": "Order ORD-195773 placed by Kofi Asante:\n| field | value |\n| --- | --- |\n| item | SKU-60774 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Hollin |\n| order date | October 23, 2026 |\n| membership level | Basic |\n| order subtotal | 30.43 USD |\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nBrowsing here is easy and the staff are happy to help you find what suits your home. Pop in and see what Copperleaf Kitchen has on the shelves.\n\nFine print:\n* Order subtotal exceeds 25.00 USD. Each order needs delivery to Hollin to earn the benefit. Qualifying orders include the date October 5, 2026 and every later day.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-195773 from Kofi Asante get free assembly?"
 },
 {
  "qid": "qfd7781a375",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nFree assembly with every delivery*\nFree returns on every purchase†\n\nSubject: So glad you dropped in\nDear visitor, Brightwell Home is delighted to welcome you with a warm smile.\n\nFine print:\n* The headline benefit is withheld on delivery to Dunmere.\n† Reserved for members ranked Plus or higher. Products sitting in any category besides garden tools fall outside this offer.\n\nOrder ORD-326323 placed by Kofi Asante:\n- item: SKU-91409\n- product category: garden tools\n- price status: open box\n- delivery region: Dunmere\n- order date: 2 March 2026\n- membership level: Plus\n- order subtotal: $39.26",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not the case that order ORD-326323 from Kofi Asante does not get free returns under the advertised terms?"
 },
 {
  "qid": "q74affb8d52",
  "kind": "yes/no",
  "text": "Order ORD-694766 placed by Dana Okafor:\n| field | value |\n| --- | --- |\n| item | SKU-52637 |\n| product category | kitchenware |\n| price status | final sale |\n| delivery region | Dunmere |\n| order date | 2026-04-23 |\n| membership level | Blue |\n| order subtotal | 56.76 USD |\n\nAdvertisement from Tidewell Supply:\nWe match any lower price*\n\nSharp lines look best with a soft touch, so brush away dust and wipe it dry. Thanks for stopping by Tidewell Supply.\n\nFine print:\n* Order by 2026-05-27 at the latest. The subtotal of the order needs to be 75.00 USD or higher.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Tidewell Supply levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not true that, under the advertised terms, order ORD-694766 from Dana Okafor does not get the price match?"
 },
 {
  "qid": "qe8f03422c5",
  "kind": "yes/no",
  "text": "Order ORD-515339 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-90936 |\n| product category | bedding |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | May 3, 2026 |\n| membership level | Basic |\n| order subtotal | $75 |\n\nAdvertisement from Harborlight Goods:\nDouble reward points on every purchase*\n\nFine print:\n* Order subtotal must go beyond $75. Only members at the Elite level or higher may take part.\n\nIt is lovely to have you at Harborlight Goods. Take a relaxed moment looking at your basket.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, does order ORD-515339 from Jonah Pryce get double reward points under its headline and that headline's small print?"
 },
 {
  "qid": "qf1d74280a2",
  "kind": "yes/no",
  "text": "Order ORD-594605 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-32167 |\n| product category | electronics |\n| price status | refurbished |\n| delivery region | Eskarth |\n| order date | 2026-04-18 |\n| membership level | Plus |\n| order subtotal | $157.05 |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\n\nFind the polished range at Copperleaf Kitchen, where considered design meets dependable quality.\n\nFine print:\n* The order subtotal must be strictly greater than $150. Valid: any order taken on or before 2026-04-17.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking the advertisement and its fine print into account, has order ORD-594605 from Selin Yilmaz lost out on double reward points?"
 },
 {
  "qid": "q2bebafa808",
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
  "qid": "q03ca0d76f5",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nDouble reward points on every purchase*\n\nSubject: So glad you dropped in\nDear visitor, Northvale Audio is delighted to welcome you with a warm smile.\n\nFine print:\n* Items marked with the open box status fall outside the benefit set out here. Valid: any order taken on or before 13 May 2026. The headline benefit is set aside for anything in the electronics category.\n\nOrder ORD-860470 placed by Nadia Haddad:\n- item: SKU-11903\n- product category: kitchenware\n- price status: open box\n- delivery region: Greyhaven\n- order date: 26 Apr 2026\n- membership level: Premier\n- order subtotal: 154.61 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Northvale Audio levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, which condition attached to double reward points does order ORD-860470 from Nadia Haddad miss, if any?",
  "options": [
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The product-category condition"
  ]
 },
 {
  "qid": "qef9de8309c",
  "kind": "choice",
  "text": "Support chat about order ORD-352217:\nDana Okafor: Hi, I placed order ORD-352217 on 13 Apr 2026 for item SKU-78742, and the order subtotal was $141.04.\nAgent: Thanks. The item is in the pet supplies product category, its price status is regular price, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Elite.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nFree returns on every purchase*\nFree installation for every appliance†\n\nSwipe around the latest drops at Wrenfield Outdoor and find your favourite.\n\nFine print:\n† Orders must be placed earlier than 14 Apr 2026.\n* The order date needs to be on or before 19 Mar 2026.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, which condition in the small print attached to free installation does order ORD-352217 from Dana Okafor miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition"
  ]
 },
 {
  "qid": "qd9f0e173a6",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nFree returns on every purchase*\n\nA step ahead\nWalk into Fernway Market and discover a shop that knows its craft and takes real pride in its shelves.\n\nFine print:\n* Every delivery bound for Eskarth lies outside the headline offer. Valid for orders placed on or after Saturday, 11 July 2026.\n\nOrder ORD-641368 placed by Owen Mensah:\n| field | value |\n| --- | --- |\n| item | SKU-45310 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | Saturday, 8 August 2026 |\n| membership level | Platinum |\n| order subtotal | $96.53 |",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Fernway Market levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich small-print condition in the ad, attached to free returns, does order ORD-641368 from Owen Mensah miss, if any?",
  "options": [
   "The order-date condition",
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q8b8c37ef9a",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree assembly with every delivery*\n\nFine print:\n* Every item in the furniture category falls outside the offer. Headline benefit is confined to delivery landing in Brenmoor.\n\nPop in and say hello\nOur friendly folks at Bluecrest Sports are keen to meet you and guide you to a piece you adore.\n\nOrder ORD-279997 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-32383 |\n| product category | furniture |\n| price status | clearance |\n| delivery region | Brenmoor |\n| order date | 18 March 2026 |\n| membership level | Blue |\n| order subtotal | 206.97 USD |",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe advertisement and its fine print attach conditions to free assembly; which, if any, does order ORD-279997 from Ravi Anand miss?",
  "options": [
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition"
  ]
 },
 {
  "qid": "qa27ba1d389",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree installation for every appliance*\n\nFine print:\n* Only a delivery to Dunmere qualifies for this offer. The order subtotal must be strictly greater than 35.00 USD.\n\nGrab the kids and take a happy look at what you picked from Tidewell Supply.\n\nOrder ORD-209627 placed by Nadia Haddad:\n- item: SKU-14848\n- product category: toys\n- price status: final sale\n- delivery region: Dunmere\n- order date: Tuesday, June 9, 2026\n- membership level: Basic\n- order subtotal: 37.27 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDo the advertised terms, taking in the headline and small print, let Nadia Haddad get free installation on order ORD-209627?"
 },
 {
  "qid": "q55569e3969",
  "kind": "yes/no",
  "text": "Order ORD-184362 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-99345 |\n| product category | kitchenware |\n| price status | pre-order |\n| delivery region | Greyhaven |\n| order date | June 3, 2026 |\n| membership level | Platinum |\n| order subtotal | $69.49 |\n\nAdvertisement from Bluecrest Sports:\nFree shipping on every order*\n\nStep in, look around, and see what Bluecrest Sports has built for modern living.\n\nFine print:\n* Members ranked Platinum and above are the only ones covered. Applies to orders placed on or after June 3, 2026.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms and what the advertisement says, does order ORD-184362 from Clara Voss lose out on free shipping?"
 },
 {
  "qid": "qba6797f3c8",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nFree gift wrapping at checkout*\n\nFine print:\n* Items whose status is final sale sit outside this offer. Valid for orders whose subtotal is $25.00 or more.\n\nPop in for a chat\nDrop by Fernway Market for a natter and a friendly face behind the counter.\n\nOrder ORD-712543 placed by Priya Raman:\n- item: SKU-34224\n- product category: pet supplies\n- price status: final sale\n- delivery region: Fallowmere\n- order date: 2026-06-27\n- membership level: Platinum\n- order subtotal: $31.06",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Fernway Market levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, which condition in the small print attached to free gift wrapping does order ORD-712543 from Priya Raman miss, if any?",
  "options": [
   "The order-subtotal condition",
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q9b616eb2dd",
  "kind": "choice",
  "text": "Order ORD-657906 placed by Lena Whitcombe:\n| field | value |\n| --- | --- |\n| item | SKU-33221 |\n| product category | garden tools |\n| price status | final sale |\n| delivery region | Fallowmere |\n| order date | 2026-04-22 |\n| membership level | Plus |\n| order subtotal | 28.93 USD |\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\nFree installation for every appliance†\n\nFine print:\n* Products whose category is pet supplies sit outside the headline benefit. Items at the final sale pricing status sit outside this promotion.\n† Requires membership at Plus or higher. Subtotal of 25.00 USD or more required.\n\nSubject: Your taste, our standard\nHello, Copperleaf Kitchen is recognised for quality that speaks for itself.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Copperleaf Kitchen levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms, which condition attached to free installation does order ORD-657906 from Lena Whitcombe miss, if any?",
  "options": [
   "The order-subtotal condition",
   "The product-category condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition"
  ]
 },
 {
  "qid": "q528a2a0494",
  "kind": "yes/no",
  "text": "Order ORD-347603 placed by Priya Raman:\n| field | value |\n| --- | --- |\n| item | SKU-49118 |\n| product category | bedding |\n| price status | clearance |\n| delivery region | Calderon |\n| order date | 2026-06-24 |\n| membership level | Black |\n| order subtotal | $25 |\n\nAdvertisement from Northvale Audio:\nFree assembly with every delivery*\n\nTake a breath at Northvale Audio\nA calm, uncluttered space to browse beautiful things.\n\nFine print:\n* Valid for orders placed on or before 2026-07-26. Subtotal of $25 or more required. The benefit is reserved for delivery bound for Calderon.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that, under the advertised terms, Priya Raman's order ORD-347603 does not get free assembly, according to what the advertisement says?"
 },
 {
  "qid": "qfd2ec6ccf2",
  "kind": "yes/no",
  "text": "Order ORD-399120 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-65079 |\n| product category | garden tools |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | Thursday, July 9, 2026 |\n| membership level | Plus |\n| order subtotal | 73.44 USD |\n\nAdvertisement from Harborlight Goods:\nFree returns on every purchase*\n\nQuick tip: wipe it down with a microfibre cloth and keep the surface clean. Thanks for picking Harborlight Goods.\n\nFine print:\n* Valid for orders placed before Thursday, August 6, 2026. Members at the Plus level or higher only.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nPer the advertisement and its fine print, is it true that order ORD-399120 from Nadia Haddad does not get free returns under the advertised terms?"
 },
 {
  "qid": "qbbf7819bd3",
  "kind": "yes/no",
  "text": "Advertisement from Oakhurst Interiors:\nA lifetime warranty on everything we sell*\n\nFine print:\n* Orders must be placed before 2026-10-04, and the day itself is excluded. Anything with delivery in Eskarth is excluded from the headline benefit.\n\nSensible choices and straight-talking service help shape Oakhurst Interiors for busy shoppers.\n\nOrder ORD-866597 placed by Ines Duarte:\n- item: SKU-26250\n- product category: furniture\n- price status: regular price\n- delivery region: Greyhaven\n- order date: 2026-10-02\n- membership level: Bronze\n- order subtotal: $190.04",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says, with its headline and small print together, does order ORD-866597 from Ines Duarte receive the lifetime warranty?"
 },
 {
  "qid": "q1841096848",
  "kind": "choice",
  "text": "Order ORD-940472 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-43476 |\n| product category | toys |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | Sunday, 25 October 2026 |\n| membership level | Silver |\n| order subtotal | $22.48 |\n\nAdvertisement from Kestrel Outfitters:\nFree returns on every purchase*\n\nFine print:\n* Goods filed under a different category from toys fall outside the benefit.\n\nBring the family along\nKestrel Outfitters is a welcoming place for parents, grandparents and children, with friendly staff ready to help.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, which condition in the small print attached to free returns does order ORD-940472 from Jonah Pryce miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition"
  ]
 },
 {
  "qid": "q154c7082c7",
  "kind": "yes/no",
  "text": "Advertisement from Northvale Audio:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Items under the toys category are carved out of this offer.\n† Every delivery bound for Greyhaven lies outside the headline offer. Valid for orders placed before 2026-05-29.\n\nKnown to the neighbourhood\nFamiliar faces greet you at Northvale Audio, a little place with a big heart for the street.\n\nOrder ORD-606502 placed by Jonah Pryce:\n- item: SKU-22064\n- product category: sports gear\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 2026-05-06\n- membership level: Premier\n- order subtotal: 92.88 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that the order ORD-606502 placed by Jonah Pryce does not get free returns under the advertised terms, as what the advertisement says indicates?"
 },
 {
  "qid": "q217ad8185c",
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
  "qid": "qeb0bc1fb13",
  "kind": "yes/no",
  "text": "Support chat about order ORD-442090:\nAiko Brandt: Hi, I placed order ORD-442090 on Friday, 1 May 2026 for item SKU-88872, and the order subtotal was 50.01 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is regular price, and it ships to the Arvale delivery region.\nAgent: Your membership level is Premier.\nAiko Brandt: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nReady for a little wander along the cheerful aisles? Wrenfield Outdoor has a twinkle on the shelves.\n\nFine print:\n† Valid for orders placed on or before Thursday, 30 April 2026. The subtotal on the order has to be more than 50.00 USD to count.\n* Anything with delivery in Eskarth is excluded from the headline benefit. Qualifying subtotal: strictly above 25.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-442090 placed by Aiko Brandt doesn't get double reward points under the advertised terms, based on the advertisement and its fine print?"
 },
 {
  "qid": "qaa361a7a60",
  "kind": "choice",
  "text": "Order ORD-569779 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-54310 |\n| product category | bedding |\n| price status | clearance |\n| delivery region | Hollin |\n| order date | Tuesday, June 2, 2026 |\n| membership level | Blue |\n| order subtotal | $158.46 |\n\nAdvertisement from Northvale Audio:\nFree returns on every purchase*\n\nWe keep things simple at Northvale Audio: practical products, clear labels and staff who actually know the stock.\n\nFine print:\n* An order qualifies with a subtotal of $150 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition from the small print attached to free returns in the advertisement and its fine print does order ORD-569779 from Clara Voss miss, if any?",
  "options": [
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qad469350c1",
  "kind": "yes/no",
  "text": "Order ORD-832634 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-71380 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Hollin |\n| order date | 11 May 2026 |\n| membership level | Black |\n| order subtotal | $200.00 |\n\nAdvertisement from Northvale Audio:\nFree assembly with every delivery*\n\nTake a breath at Northvale Audio\nA calm, uncluttered space to browse beautiful things.\n\nFine print:\n* Valid for orders placed on or before 19 June 2026. Subtotal of $200.00 or more required. The benefit is reserved for delivery bound for Hollin.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that, under the advertised terms, Clara Voss's order ORD-832634 does not get free assembly, according to what the advertisement says?"
 },
 {
  "qid": "qc6a66f4e8c",
  "kind": "choice",
  "text": "Advertisement from Cedarline Living:\nFree assembly with every delivery*\nA lifetime warranty on everything we sell†\n\nIt's lovely to have you here. Let the item rest somewhere cool and dry, and feel welcome to call on Cedarline Living anytime.\n\nFine print:\n† Any item whose status is open box falls outside this offer.\n* Applies to order subtotals of $25.00 or more.\n\nOrder ORD-183732 placed by Kofi Asante:\n- item: SKU-95638\n- product category: furniture\n- price status: pre-order\n- delivery region: Calderon\n- order date: 31 July 2026\n- membership level: Blue\n- order subtotal: $25.00",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the small print offer by offer, which of the advertised terms does Kofi Asante actually get on order ORD-183732?",
  "options": [
   "Only free assembly",
   "Only the lifetime warranty",
   "Both offers",
   "Neither offer"
  ]
 },
 {
  "qid": "qa25093d892",
  "kind": "choice",
  "text": "Advertisement from Wrenfield Outdoor:\nFree gift wrapping at checkout*\nFree shipping on every order†\n\nWrenfield Outdoor, measured and poised\nA gracious setting to linger and admire the craftsmanship.\n\nOrder ORD-327214 placed by Priya Raman:\n- item: SKU-20874\n- product category: garden tools\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: Sunday, 26 July 2026\n- membership level: Silver\n- order subtotal: 79.07 USD\n\nFine print from the bottom of the advertisement:\n* Valid for orders placed on or before Thursday, 27 August 2026.\n† Placed before Saturday, 15 August 2026 counts; that very day is excluded. Order subtotal strictly more than 100.00 USD.\n\nNote added by the customer: Priya Raman notes that a colleague on the call said the headline would apply, so the advert is effectively the store's own promise.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nCould you tell me which headline offers in the ad and its small print order ORD-327214 from Priya Raman actually gets when applied offer by offer?",
  "options": [
   "Only free shipping",
   "Both offers",
   "Only free gift wrapping",
   "Neither offer"
  ]
 },
 {
  "qid": "q66c80188b9",
  "kind": "yes/no",
  "text": "Support chat about order ORD-625106:\nFelix Moreau: Hi, I placed order ORD-625106 on 2026-07-06 for item SKU-36193, and the order subtotal was 245.63 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is open box, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Blue.\nFelix Moreau: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nFree installation for every appliance*\n\nSay hi to the crew at Larkspur Playthings! We love helping you plan your getaway with trusted picks and friendly advice.\n*Delivery to Eskarth only. Order by 2026-07-18 at the latest.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-625106 from Felix Moreau get free installation?"
 },
 {
  "qid": "qb68bb56aa6",
  "kind": "choice",
  "text": "Support chat about order ORD-899921:\nClara Voss: Hi, I placed order ORD-899921 on Thursday, 16 July 2026 for item SKU-77922, and the order subtotal was $204.44.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Plus.\nClara Voss: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nOur corner shop at Oakhurst Interiors is tucked away, which is part of the charm.\n\nFine print:\n* Orders placed by Thursday, 16 July 2026 are valid, and the stated day is included.\n† An order placed on or before Thursday, 20 August 2026 qualifies. The order subtotal must be above $200.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does order ORD-899921 from Clara Voss truly get under the advertisement and its fine print?",
  "options": [
   "Both offers",
   "Neither offer",
   "Only free shipping",
   "Only free gift wrapping"
  ]
 },
 {
  "qid": "q48290797de",
  "kind": "yes/no",
  "text": "Support chat about order ORD-840242:\nDana Okafor: Hi, I placed order ORD-840242 on 16 June 2026 for item SKU-85413, and the order subtotal was 248.19 USD.\nAgent: Thanks. The item is in the pet supplies product category, its price status is final sale, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Green.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\nDouble reward points on every purchase†\n\nA bit of dusting goes a long way. Thanks, and happy handling from Birchwood Linens.\n\nFine print:\n† Only a delivery to Fallowmere qualifies for this offer.\n* Excludes all items with clearance status. Delivery to Brenmoor only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertised terms, which include the headline and its small print, does Dana Okafor come with free shipping on order ORD-840242?"
 },
 {
  "qid": "q6ca85d610f",
  "kind": "choice",
  "text": "Order ORD-440407 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-34802 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Hollin |\n| order date | 26 Aug 2026 |\n| membership level | Silver |\n| order subtotal | $75.00 |\n\nAdvertisement from Kestrel Outfitters:\nFree shipping on every order*\nDouble reward points on every purchase†\n\nSoft light, measured choices and a feeling of unhurried grace greet you at Kestrel Outfitters.\n\nFine print:\n* Minimum order subtotal: $75.00.\n† Goods in the garden tools category fall outside the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nAccording to what the advertisement says, which of its headline offers does order ORD-440407 from Aiko Brandt actually get?",
  "options": [
   "Neither offer",
   "Only free shipping",
   "Only double reward points",
   "Both offers"
  ]
 },
 {
  "qid": "q0d8c2ef6d5",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree assembly with every delivery*\n\nFresh arrivals, clean lines and quick browsing. Welcome to Bluecrest Sports.\n\nOrder ORD-931168 placed by Hugo Lindqvist:\n- item: SKU-81161\n- product category: garden tools\n- price status: regular price\n- delivery region: Calderon\n- order date: 2026-04-08\n- membership level: Black\n- order subtotal: $83.47\n\nFine print from the bottom of the advertisement:\n* Eligibility for the benefit is restricted to the pet supplies product category. Reserved for members ranked Black or higher.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich small-print condition in the ad, attached to free assembly, does order ORD-931168 from Hugo Lindqvist miss, if any?",
  "options": [
   "The product-category condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qf362cf3d2d",
  "kind": "choice",
  "text": "Advertisement from Oakhurst Interiors:\nA lifetime warranty on everything we sell*\nFree assembly with every delivery†\n\nOur range is carefully chosen and our service is quietly exceptional at Oakhurst Interiors.\n\nFine print:\n* Items at the refurbished pricing status sit outside this promotion.\n† Products whose category is bedding sit outside the headline benefit.\n\nOrder ORD-998401 placed by Nadia Haddad:\n- item: SKU-43166\n- product category: bedding\n- price status: refurbished\n- delivery region: Dunmere\n- order date: July 4, 2026\n- membership level: Bronze\n- order subtotal: 234.23 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-998401 from Nadia Haddad, which headline offers does what the advertisement says actually grant, checked offer by offer against small print?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the lifetime warranty",
   "Only free assembly"
  ]
 },
 {
  "qid": "q569656b0be",
  "kind": "choice",
  "text": "Advertisement from Juniper Gadgets:\nFree installation for every appliance*\nFree assembly with every delivery†\n\nWelcome aboard, and thanks for picking Juniper Gadgets. Place your new item in a cool, dry spot, and give it a gentle clean as grime builds up.\n\nOrder ORD-826887 placed by Priya Raman:\n- item: SKU-13507\n- product category: bedding\n- price status: final sale\n- delivery region: Greyhaven\n- order date: 12 September 2026\n- membership level: Green\n- order subtotal: $164.25\n\nFine print from the bottom of the advertisement:\n* Items whose status is clearance sit outside this offer.\n† Items at final sale pricing are withheld from this benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does order ORD-826887 from Priya Raman truly get, by the terms set out in what the advertisement says?",
  "options": [
   "Both offers",
   "Only free assembly",
   "Only free installation",
   "Neither offer"
  ]
 },
 {
  "qid": "q33bba5fbb4",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree installation for every appliance*\n\nFine print:\n* Items in the furniture product category are excluded.\n\nSerene spaces\nStep into the calm of Wrenfield Outdoor, where soft light drifts across tactile textures and unhurried displays.\n\nOrder ORD-163913 placed by Ravi Anand:\n- item: SKU-38491\n- product category: garden tools\n- price status: regular price\n- delivery region: Fallowmere\n- order date: Monday, 29 June 2026\n- membership level: Platinum\n- order subtotal: 114.93 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nMeasured against the advertised terms in full, does order ORD-163913 from Ravi Anand lose out on free installation?"
 },
 {
  "qid": "qdfd20f4c52",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nA lifetime warranty on everything we sell*\nFree returns on every purchase†\n\nFine print:\n† Items at the clearance pricing status sit outside this promotion.\n* Shoppers get the headline benefit solely for delivery in Arvale.\n\nSubject: Quietly elegant style from Fernway Market\nHello there,\nOur newest pieces have a graceful feel and a modern look.\n\nOrder ORD-636039 placed by Lena Whitcombe:\n- item: SKU-59482\n- product category: pet supplies\n- price status: clearance\n- delivery region: Arvale\n- order date: Sunday, October 4, 2026\n- membership level: Silver\n- order subtotal: $219.83",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Fernway Market levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does order ORD-636039 from Lena Whitcombe actually get when the advertisement and its fine print are applied offer by offer?",
  "options": [
   "Only free returns",
   "Neither offer",
   "Only the lifetime warranty",
   "Both offers"
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
 }
]
