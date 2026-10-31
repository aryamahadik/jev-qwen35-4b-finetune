# G5-H blind read T07-blind_read-77c62d0b-001 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T07/pilot/g5h/answers/T07-blind_read-77c62d0b-001.json

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
  "qid": "q9240cd5204",
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
  "qid": "qb7366acb78",
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
  "qid": "q84357e0cd0",
  "kind": "yes/no",
  "text": "Advertisement from Harborlight Goods:\nFree gift wrapping at checkout*\n\n{\"title\": \"Harborlight Goods app\", \"subtitle\": \"Browse the range, build a list, and check out quickly\", \"button\": \"Get started\"}\n\nOrder ORD-436956 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-67060 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Fallowmere |\n| order date | 2026-03-29 |\n| membership level | Platinum |\n| order subtotal | 183.27 USD |\n\nFine print from the bottom of the advertisement:\n* Items under the bedding category are carved out of this offer. The headline benefit is withheld on delivery to Fallowmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the ad and its small print, is it true that order ORD-436956 from Jonah Pryce doesn't get free gift wrapping under the advertised terms?"
 },
 {
  "qid": "q9c086a02a4",
  "kind": "choice",
  "text": "Advertisement from Juniper Gadgets:\nFree installation for every appliance*\nFree assembly with every delivery†\n\nFine print:\n* Order by Monday, July 13, 2026 at the latest. Members ranked Black and above are the only ones covered.\n† Qualifying subtotal: strictly above $50. For Green members and below.\n\nA bit of dusting goes a long way. Thanks, and happy handling from Juniper Gadgets.\n\nOrder ORD-474453 placed by Dana Okafor:\n- item: SKU-55236\n- product category: garden tools\n- price status: clearance\n- delivery region: Fallowmere\n- order date: Monday, July 13, 2026\n- membership level: Blue\n- order subtotal: $64.46",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Juniper Gadgets levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOf the conditions in the small print attached to free assembly, which, if any, does order ORD-474453 from Dana Okafor miss, according to what the advertisement says?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The membership-level condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q4d2b395285",
  "kind": "yes/no",
  "text": "Order ORD-594605 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-32167 |\n| product category | electronics |\n| price status | refurbished |\n| delivery region | Eskarth |\n| order date | 2026-04-18 |\n| membership level | Plus |\n| order subtotal | $157.05 |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\n\nFind the polished range at Copperleaf Kitchen, where considered design meets dependable quality.\n\nFine print:\n* The order subtotal must be strictly greater than $150. Valid: any order taken on or before 2026-04-17.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes Selin Yilmaz get double reward points on order ORD-594605 when the advertised terms, with the headline and its small print, are applied?"
 },
 {
  "qid": "q195e8a5aac",
  "kind": "yes/no",
  "text": "Support chat about order ORD-815992:\nOwen Mensah: Hi, I placed order ORD-815992 on 28 October 2026 for item SKU-65776, and the order subtotal was 89.75 USD.\nAgent: Thanks. The item is in the bedding product category, its price status is open box, and it ships to the Hollin delivery region.\nAgent: Your membership level is Silver.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nA lifetime warranty on everything we sell*\n\nSubject: Plans worth making together\nHello there,\nCedarline Living invites your family to enjoy fresh air and easygoing fun. We are happy to help you plan a family outing. Thank you for being part of our community, and we look forward to welcoming you.\n*Valid on orders of 75.00 USD or more.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Cedarline Living levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement alongside its fine print, does Owen Mensah receive the lifetime warranty on order ORD-815992?"
 },
 {
  "qid": "qacaa7e016d",
  "kind": "yes/no",
  "text": "Order ORD-515339 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-90936 |\n| product category | bedding |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | May 3, 2026 |\n| membership level | Basic |\n| order subtotal | $75 |\n\nAdvertisement from Harborlight Goods:\nDouble reward points on every purchase*\n\nFine print:\n* Order subtotal must go beyond $75. Only members at the Elite level or higher may take part.\n\nIt is lovely to have you at Harborlight Goods. Take a relaxed moment looking at your basket.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does the order ORD-515339 placed by Jonah Pryce fail to earn double reward points, according to the advertisement and its fine print?"
 },
 {
  "qid": "qd71683510b",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree gift wrapping at checkout*\nDouble reward points on every purchase†\n\nFine print:\n* Anything with delivery in Brenmoor is excluded from the headline benefit. Valid: any order taken on or before 4 Sep 2026.\n† Valid on orders over $200.00.\n\nGood coffee, good company and a little bit of fun at Marigold Pets. Pop by and see what we have been up to.\n\nOrder ORD-402763 placed by Dana Okafor:\n- item: SKU-29364\n- product category: garden tools\n- price status: final sale\n- delivery region: Calderon\n- order date: 23 Sep 2026\n- membership level: Green\n- order subtotal: $200.01",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Marigold Pets levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBetween the advertisement and its fine print, does order ORD-402763 from Dana Okafor get free gift wrapping?"
 },
 {
  "qid": "q5bc7480b0f",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree assembly with every delivery*\n\nFine print:\n* Every item in the electronics category falls outside the offer. Headline benefit is confined to delivery landing in Calderon.\n\nQuality that speaks for itself and service that feels personal. Welcome to Bluecrest Sports.\n\nOrder ORD-279070 placed by Aiko Brandt:\n- item: SKU-97827\n- product category: electronics\n- price status: regular price\n- delivery region: Calderon\n- order date: 20 July 2026\n- membership level: Black\n- order subtotal: 45.67 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe advertisement and its fine print attach conditions to free assembly; which, if any, does order ORD-279070 from Aiko Brandt miss?",
  "options": [
   "The delivery-region condition",
   "The product-category condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q8a41327fb4",
  "kind": "choice",
  "text": "Support chat about order ORD-184657:\nNadia Haddad: Hi, I placed order ORD-184657 on 26 March 2026 for item SKU-70854, and the order subtotal was $184.14.\nAgent: Thanks. The item is in the garden tools product category, its price status is pre-order, and it ships to the Hollin delivery region.\nAgent: Your membership level is Plus.\nNadia Haddad: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nA lifetime warranty on everything we sell*\nFree gift wrapping at checkout†\n\nHello there from Pebblestone Garden. Explore the range at speed and spot the pieces that suit you.\n\nFine print:\n† The order subtotal must be above $200.00.\n* The order subtotal must be strictly greater than $200.00.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Pebblestone Garden levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers survive the advertisement and its fine print for order ORD-184657 from Nadia Haddad, checked offer by offer?",
  "options": [
   "Only the lifetime warranty",
   "Both offers",
   "Neither offer",
   "Only free gift wrapping"
  ]
 },
 {
  "qid": "qe6537db41b",
  "kind": "yes/no",
  "text": "Advertisement from Fernway Market:\nFree returns on every purchase*\nDouble reward points on every purchase†\n\nFine print:\n† Orders placed by 13 June 2026 are valid, and the stated day is included.\n* Excludes the toys category.\n\nWipe it with a damp cloth and let it air-dry. Thanks for buying from Fernway Market.\n\nOrder ORD-394280 placed by Selin Yilmaz:\n- item: SKU-79020\n- product category: toys\n- price status: regular price\n- delivery region: Arvale\n- order date: 24 June 2026\n- membership level: Gold\n- order subtotal: $57.60",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the advertisement with its fine print confirm that order ORD-394280 from Selin Yilmaz comes with free returns?"
 },
 {
  "qid": "q3540ad1a40",
  "kind": "choice",
  "text": "Advertisement from Harborlight Goods:\nWe match any lower price*\nFree assembly with every delivery†\n\nOur range is carefully chosen and our service is quietly exceptional at Harborlight Goods.\n\nFine print:\n† Membership tier Silver or lower applies.\n* Valid only for items in the electronics category.\n\nOrder ORD-289393 placed by Felix Moreau:\n- item: SKU-86295\n- product category: electronics\n- price status: pre-order\n- delivery region: Greyhaven\n- order date: June 7, 2026\n- membership level: Silver\n- order subtotal: $56.63",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the advertised terms does order ORD-289393 from Felix Moreau actually get with the small print applied offer by offer?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the price match",
   "Only free assembly"
  ]
 },
 {
  "qid": "q3b8bc1513f",
  "kind": "choice",
  "text": "Support chat about order ORD-854147:\nOwen Mensah: Hi, I placed order ORD-854147 on Tuesday, July 28, 2026 for item SKU-84641, and the order subtotal was 67.10 USD.\nAgent: Thanks. The item is in the toys product category, its price status is regular price, and it ships to the Greyhaven delivery region.\nAgent: Your membership level is Plus.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nFree installation for every appliance*\nDouble reward points on every purchase†\n\nSubject: Welcome to Pebblestone Garden\nDear friend,\nWe are delighted to share our refined home pieces, chosen with a quiet eye for craft.\n\nFine print:\n† Only the toys category earns the headline benefit.\n* For Premier members and above.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does order ORD-854147 from Owen Mensah truly get, by the terms set out in what the advertisement says?",
  "options": [
   "Only free installation",
   "Neither offer",
   "Only double reward points",
   "Both offers"
  ]
 },
 {
  "qid": "qe2fe4a9564",
  "kind": "yes/no",
  "text": "Order ORD-184362 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-99345 |\n| product category | kitchenware |\n| price status | pre-order |\n| delivery region | Greyhaven |\n| order date | June 3, 2026 |\n| membership level | Platinum |\n| order subtotal | $69.49 |\n\nAdvertisement from Bluecrest Sports:\nFree shipping on every order*\n\nStep in, look around, and see what Bluecrest Sports has built for modern living.\n\nFine print:\n* Members ranked Platinum and above are the only ones covered. Applies to orders placed on or after June 3, 2026.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms and what the advertisement says, does order ORD-184362 from Clara Voss lose out on free shipping?"
 },
 {
  "qid": "q7454b475b7",
  "kind": "choice",
  "text": "Support chat about order ORD-385758:\nMira Castell: Hi, I placed order ORD-385758 on March 3, 2026 for item SKU-84278, and the order subtotal was $35.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Gold.\nMira Castell: I am asking about the advertisement below.\n\nAdvertisement from Marigold Pets:\nFree installation for every appliance*\n\nThanks for choosing Marigold Pets, and a warm welcome from our small team to yours. Clean it with a soft cloth, let it air out, and find it a cosy spot at home.\n*Excludes delivery to Brenmoor. Minimum order subtotal: $35.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-385758 from Mira Castell, which condition in the small print attached to free installation does it miss, if any, as the advertisement says?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q8658638722",
  "kind": "yes/no",
  "text": "Order ORD-594605 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-32167 |\n| product category | electronics |\n| price status | refurbished |\n| delivery region | Eskarth |\n| order date | 2026-04-18 |\n| membership level | Plus |\n| order subtotal | $157.05 |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\n\nFind the polished range at Copperleaf Kitchen, where considered design meets dependable quality.\n\nFine print:\n* The order subtotal must be strictly greater than $150. Valid: any order taken on or before 2026-04-17.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking the advertisement and its fine print into account, has order ORD-594605 from Selin Yilmaz lost out on double reward points?"
 },
 {
  "qid": "qca19fae60d",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nFree returns on every purchase*\nA lifetime warranty on everything we sell†\n\nFine print:\n* Products assigned to the bedding category are excluded.\n† Products sitting in any category besides sports gear fall outside this offer.\n\nPractical shopping, close to home\nWorkmanlike stock and well-made wares fill the rows at Northvale Audio for small projects and big plans.\n\nOrder ORD-209897 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-44227 |\n| product category | electronics |\n| price status | final sale |\n| delivery region | Brenmoor |\n| order date | 2026-10-16 |\n| membership level | Premier |\n| order subtotal | $83.76 |",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOffer by offer, which headline offers from the advertisement and its fine print does Tomas Ferreira actually get on order ORD-209897?",
  "options": [
   "Only the lifetime warranty",
   "Neither offer",
   "Both offers",
   "Only free returns"
  ]
 },
 {
  "qid": "qe1c16393e8",
  "kind": "choice",
  "text": "Support chat about order ORD-936040:\nKofi Asante: Hi, I placed order ORD-936040 on 2026-06-20 for item SKU-67120, and the order subtotal was 50.01 USD.\nAgent: Thanks. The item is in the electronics product category, its price status is pre-order, and it ships to the Hollin delivery region.\nAgent: Your membership level is Bronze.\nKofi Asante: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\n{\"title\": \"Browse the new range at Cedarline Living\", \"subtitle\": \"Scroll the favourites and find a piece to love\", \"button\": \"Start looking\"}\n\nFine print:\n† Only members at the Silver level or higher may take part.\n* Order subtotal exceeds 50.00 USD. An order whose delivery goes to Hollin falls outside the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the ad and its small print attached to free gift wrapping does order ORD-936040 from Kofi Asante miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition",
   "The order-subtotal condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q18ce7c0790",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree assembly with every delivery*\n\nSubject: a note from our calm corner\nDear friend,\nBluecrest Sports selects its pieces with thoughtful care and a refined eye.\nOur shelves are arranged in a calm, elegant way.\nWe hope you enjoy a relaxed visit and a warm welcome, with our best wishes.\n*Valid only for orders delivered to Fallowmere. Excludes items with final sale status.\n\nOrder ORD-607429 placed by Jonah Pryce:\n- item: SKU-68567\n- product category: bedding\n- price status: pre-order\n- delivery region: Fallowmere\n- order date: June 19, 2026\n- membership level: Blue\n- order subtotal: 165.54 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhere the advertisement attaches small print to free assembly, which condition, if any, does order ORD-607429 from Jonah Pryce miss?",
  "options": [
   "The delivery-region condition",
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q8f56682301",
  "kind": "choice",
  "text": "Order ORD-765498 placed by Kofi Asante:\n| field | value |\n| --- | --- |\n| item | SKU-56044 |\n| product category | furniture |\n| price status | refurbished |\n| delivery region | Fallowmere |\n| order date | March 28, 2026 |\n| membership level | Elite |\n| order subtotal | 142.65 USD |\n\nAdvertisement from Fernway Market:\nFree assembly with every delivery*\n\nSubject: Quietly elegant style from Fernway Market\nHello there,\nOur newest pieces have a graceful feel and a modern look.\n\nFine print:\n* Orders dated on or before April 23, 2026 count. Stock flagged as refurbished sits outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-765498 from Kofi Asante and reading the ad and its small print, which condition attached to free assembly does it miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The price-status condition"
  ]
 },
 {
  "qid": "qf79132bdcc",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree assembly with every delivery*\nFree installation for every appliance†\n\nYour cosy corner awaits\nStep inside Wrenfield Outdoor and feel right at home.\n\nFine print:\n† Items listed at pre-order pricing are excluded from the benefit.\n* Items that hold the clearance status are excluded from the main benefit.\n\nOrder ORD-343181 placed by Ravi Anand:\n- item: SKU-98042\n- product category: bedding\n- price status: open box\n- delivery region: Greyhaven\n- order date: 26 May 2026\n- membership level: Platinum\n- order subtotal: $86.80",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nMeasured against the advertisement and its fine print, does order ORD-343181 from Ravi Anand lose out on free installation?"
 },
 {
  "qid": "q0a6f060b80",
  "kind": "choice",
  "text": "Order ORD-312606 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-89776 |\n| product category | electronics |\n| price status | pre-order |\n| delivery region | Eskarth |\n| order date | 6 Oct 2026 |\n| membership level | Premier |\n| order subtotal | 97.42 USD |\n\nAdvertisement from Fernway Market:\nFree assembly with every delivery*\n\nFine print:\n* Items priced as pre-order are excluded.\n\nGrins, colour and cheeky surprises are waiting at Fernway Market, so bring your curiosity.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Fernway Market levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, which condition in the small print attached to free assembly does order ORD-312606 from Selin Yilmaz miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition"
  ]
 },
 {
  "qid": "q805c6e6b19",
  "kind": "yes/no",
  "text": "Advertisement from Oakhurst Interiors:\nA lifetime warranty on everything we sell*\n\nSubject: Quick scroll, sharp picks\nHey, Oakhurst Interiors is moving fast and the lineup is crisp.\n\nFine print:\n* Goods filed under a different category from pet supplies fall outside the benefit. An order whose delivery goes to Hollin falls outside the headline benefit.\n\nOrder ORD-274231 placed by Hugo Lindqvist:\n- item: SKU-81803\n- product category: pet supplies\n- price status: regular price\n- delivery region: Hollin\n- order date: September 17, 2026\n- membership level: Silver\n- order subtotal: $76.96",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not so that Hugo Lindqvist does not get the lifetime warranty on order ORD-274231, per the advertisement and its fine print?"
 },
 {
  "qid": "q675a8dc062",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nHello there\nWe are glad you stopped by. Marigold Pets is here to make your visit feel warm and easy.\n\nOrder ORD-839855 placed by Clara Voss:\n- item: SKU-15677\n- product category: garden tools\n- price status: open box\n- delivery region: Dunmere\n- order date: March 23, 2026\n- membership level: Black\n- order subtotal: 70.81 USD\n\nFine print from the bottom of the advertisement:\n* Orders must be placed before March 24, 2026, and the day itself is excluded. Any delivery to Arvale is excluded from this offer.\n† The headline benefit is withheld on delivery to Dunmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not accurate to say that Clara Voss does not get free shipping with order ORD-839855 under the advertised terms?"
 },
 {
  "qid": "qcd9c4765a6",
  "kind": "yes/no",
  "text": "Order ORD-269004 placed by Ravi Anand:\n- item: SKU-90730\n- product category: pet supplies\n- price status: pre-order\n- delivery region: Calderon\n- order date: Saturday, 28 March 2026\n- membership level: Plus\n- order subtotal: $50.00\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nCopperleaf Kitchen is a down-to-earth shop with reliable products and helpful staff.\n\nFine print:\n* Order subtotal exceeds $50.00. Each order needs delivery to Calderon to earn the benefit. Qualifying orders include the date Saturday, 28 February 2026 and every later day.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-269004 from Ravi Anand get free assembly?"
 },
 {
  "qid": "q9db847fa9d",
  "kind": "yes/no",
  "text": "Support chat about order ORD-743714:\nOwen Mensah: Hi, I placed order ORD-743714 on August 22, 2026 for item SKU-70899, and the order subtotal was 71.79 USD.\nAgent: Thanks. The item is in the bedding product category, its price status is pre-order, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Silver.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nA lifetime warranty on everything we sell*\n\nSubject: Plans worth making together\nHello there,\nCedarline Living invites your family to enjoy fresh air and easygoing fun. We are happy to help you plan a family outing. Thank you for being part of our community, and we look forward to welcoming you.\n*Valid on orders of 100.00 USD or more.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Cedarline Living levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement alongside its fine print, does Owen Mensah receive the lifetime warranty on order ORD-743714?"
 },
 {
  "qid": "q4bb6c632a1",
  "kind": "yes/no",
  "text": "Order ORD-964081 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-81061 |\n| product category | kitchenware |\n| price status | open box |\n| delivery region | Eskarth |\n| order date | Wednesday, September 16, 2026 |\n| membership level | Plus |\n| order subtotal | $98.60 |\n\nAdvertisement from Fernway Market:\nFree returns on every purchase*\n\nFine print:\n* Excludes the pet supplies category. Orders placed by Friday, September 18, 2026 are valid, and the stated day is included.\n\nThank you for placing your order with Fernway Market. Take a considered look at your basket and continue with confidence.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad, with its small print taken into account, mean that Ravi Anand earns free returns on order ORD-964081?"
 },
 {
  "qid": "qc63244444e",
  "kind": "yes/no",
  "text": "Support chat about order ORD-464687:\nInes Duarte: Hi, I placed order ORD-464687 on 26 February 2026 for item SKU-19134, and the order subtotal was 35.01 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is clearance, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Green.\nInes Duarte: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nWe match any lower price*\nFree returns on every purchase†\n\nThoughtfully sourced living\nExplore the range at Larkspur Playthings, where careful craft meets the tastes of contemporary homes.\n\nFine print:\n* Orders count only with a subtotal beyond $35.\n† An order placed on or before 22 March 2026 qualifies. Customers at the Green tier or lower can use this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, does Ines Duarte earn free returns with order ORD-464687?"
 },
 {
  "qid": "q436fef8a0b",
  "kind": "yes/no",
  "text": "Order ORD-399120 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-65079 |\n| product category | garden tools |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | Thursday, July 9, 2026 |\n| membership level | Plus |\n| order subtotal | 73.44 USD |\n\nAdvertisement from Harborlight Goods:\nFree returns on every purchase*\n\nQuick tip: wipe it down with a microfibre cloth and keep the surface clean. Thanks for picking Harborlight Goods.\n\nFine print:\n* Valid for orders placed before Thursday, August 6, 2026. Members at the Plus level or higher only.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nPer the advertisement and its fine print, is it true that order ORD-399120 from Nadia Haddad does not get free returns under the advertised terms?"
 },
 {
  "qid": "q219976f819",
  "kind": "yes/no",
  "text": "Advertisement from Cedarline Living:\nFree assembly with every delivery*\n\nHello, neighbours! Cedarline Living is a small shop with a big heart, and we are happy you popped in. Come say hi, browse at your own pace, and tell us what you love.\n*The order subtotal must be above $75.\n\nOrder ORD-735332 placed by Ravi Anand:\n- item: SKU-43305\n- product category: kitchenware\n- price status: refurbished\n- delivery region: Dunmere\n- order date: 9 Jun 2026\n- membership level: Green\n- order subtotal: 75.01 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-735332 from Ravi Anand forfeit free assembly under the advertised terms, as those terms are written?"
 },
 {
  "qid": "q40d7b651bf",
  "kind": "yes/no",
  "text": "Order ORD-541242 placed by Felix Moreau:\n| field | value |\n| --- | --- |\n| item | SKU-56214 |\n| product category | toys |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | June 13, 2026 |\n| membership level | Basic |\n| order subtotal | $204.64 |\n\nAdvertisement from Copperleaf Kitchen:\nFree returns on every purchase*\n\nFine print:\n* Every item in the bedding category falls outside the offer.\n\nSensible picks, down to earth\nStroll the aisles at Copperleaf Kitchen and see how straightforward products slot into ordinary homes.\n\nNote added by the customer: Felix Moreau says the reviews will be full of this, loudly and at length, unless the offer is honored.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the ad and its small print together, does order ORD-541242 from Felix Moreau fail to secure free returns under the advertised terms?"
 },
 {
  "qid": "q73e8de78be",
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
  "qid": "qfea4ae8f4f",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nFree assembly with every delivery*\nFree returns on every purchase†\n\nSubject: So glad you dropped in\nDear visitor, Brightwell Home is delighted to welcome you with a warm smile.\n\nFine print:\n* The headline benefit is withheld on delivery to Dunmere.\n† Reserved for members ranked Plus or higher. Products sitting in any category besides garden tools fall outside this offer.\n\nOrder ORD-326323 placed by Kofi Asante:\n- item: SKU-91409\n- product category: garden tools\n- price status: open box\n- delivery region: Dunmere\n- order date: 2 March 2026\n- membership level: Plus\n- order subtotal: $39.26",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not the case that order ORD-326323 from Kofi Asante does not get free returns under the advertised terms?"
 },
 {
  "qid": "q5d25da2767",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree assembly with every delivery†\n\nFine print:\n† Delivery to Dunmere only. Items whose status is open box are excluded.\n* Applies to orders placed on or after 2026-09-15. Any item whose status is clearance falls outside this offer.\n\nWe are so happy you have joined the family at Larkspur Playthings. A quick dust and a soft touch keep it lovely for ages.\n\nOrder ORD-233009 placed by Aiko Brandt:\n- item: SKU-44090\n- product category: garden tools\n- price status: clearance\n- delivery region: Arvale\n- order date: 2026-09-29\n- membership level: Basic\n- order subtotal: $40.68",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not the case that order ORD-233009 from Aiko Brandt does not get free assembly under the advertisement and its fine print?"
 },
 {
  "qid": "q6ffdfdafdb",
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
  "qid": "qc61d3f4adb",
  "kind": "yes/no",
  "text": "Advertisement from Fernway Market:\nFree installation for every appliance*\n\nFine print:\n* Orders count only with a subtotal beyond $150.00. Members at Silver and above only.\n\nWelcome back to Fernway Market. Your basket is ready and waiting for a closer glance.\n\nOrder ORD-381656 placed by Nadia Haddad:\n- item: SKU-12563\n- product category: pet supplies\n- price status: regular price\n- delivery region: Hollin\n- order date: 3 September 2026\n- membership level: Gold\n- order subtotal: $150.01",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nJudged by the advertised terms, does the order ORD-381656 placed by Nadia Haddad fail to earn free installation?"
 },
 {
  "qid": "q9fff59c3c6",
  "kind": "yes/no",
  "text": "Order ORD-541242 placed by Felix Moreau:\n| field | value |\n| --- | --- |\n| item | SKU-56214 |\n| product category | toys |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | June 13, 2026 |\n| membership level | Basic |\n| order subtotal | $204.64 |\n\nAdvertisement from Copperleaf Kitchen:\nFree returns on every purchase*\n\nFine print:\n* Every item in the bedding category falls outside the offer.\n\nSensible picks, down to earth\nStroll the aisles at Copperleaf Kitchen and see how straightforward products slot into ordinary homes.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the ad and its small print together, does order ORD-541242 from Felix Moreau fail to secure free returns under the advertised terms?"
 },
 {
  "qid": "qb44c749e2d",
  "kind": "yes/no",
  "text": "Support chat about order ORD-464687:\nInes Duarte: Hi, I placed order ORD-464687 on 26 February 2026 for item SKU-19134, and the order subtotal was 35.01 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is clearance, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Green.\nInes Duarte: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nWe match any lower price*\nFree returns on every purchase†\n\nThoughtfully sourced living\nExplore the range at Larkspur Playthings, where careful craft meets the tastes of contemporary homes.\n\nFine print:\n* Orders count only with a subtotal beyond $35.\n† An order placed on or before 22 March 2026 qualifies. Customers at the Green tier or lower can use this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print together, does order ORD-464687 from Ines Duarte lose out on free returns under the advertised terms?"
 },
 {
  "qid": "q97a45fd333",
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
  "qid": "q3f0a0d56d9",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree installation for every appliance*\n\nFine print:\n* Items in the furniture product category are excluded.\n\nSerene spaces\nStep into the calm of Wrenfield Outdoor, where soft light drifts across tactile textures and unhurried displays.\n\nOrder ORD-163913 placed by Ravi Anand:\n- item: SKU-38491\n- product category: garden tools\n- price status: regular price\n- delivery region: Fallowmere\n- order date: Monday, 29 June 2026\n- membership level: Platinum\n- order subtotal: 114.93 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nMeasured against the advertised terms in full, does order ORD-163913 from Ravi Anand lose out on free installation?"
 },
 {
  "qid": "q6ce08f1e1e",
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
  "qid": "qab7e59c6a3",
  "kind": "yes/no",
  "text": "Support chat about order ORD-840242:\nDana Okafor: Hi, I placed order ORD-840242 on 16 June 2026 for item SKU-85413, and the order subtotal was 248.19 USD.\nAgent: Thanks. The item is in the pet supplies product category, its price status is final sale, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Green.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\nDouble reward points on every purchase†\n\nA bit of dusting goes a long way. Thanks, and happy handling from Birchwood Linens.\n\nFine print:\n† Only a delivery to Fallowmere qualifies for this offer.\n* Excludes all items with clearance status. Delivery to Brenmoor only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertised terms, which include the headline and its small print, does Dana Okafor come with free shipping on order ORD-840242?"
 },
 {
  "qid": "q21d995f8b5",
  "kind": "yes/no",
  "text": "Support chat about order ORD-442090:\nAiko Brandt: Hi, I placed order ORD-442090 on Friday, 1 May 2026 for item SKU-88872, and the order subtotal was 50.01 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is regular price, and it ships to the Arvale delivery region.\nAgent: Your membership level is Premier.\nAiko Brandt: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nReady for a little wander along the cheerful aisles? Wrenfield Outdoor has a twinkle on the shelves.\n\nFine print:\n† Valid for orders placed on or before Thursday, 30 April 2026. The subtotal on the order has to be more than 50.00 USD to count.\n* Anything with delivery in Eskarth is excluded from the headline benefit. Qualifying subtotal: strictly above 25.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-442090 placed by Aiko Brandt doesn't get double reward points under the advertised terms, based on the advertisement and its fine print?"
 },
 {
  "qid": "qb4d33d31ad",
  "kind": "choice",
  "text": "Advertisement from Larkspur Playthings:\nA lifetime warranty on everything we sell*\nFree assembly with every delivery†\n\nWe hope the things you picked at Larkspur Playthings suit your plans. Take a look at your basket, then check out when you are set.\n\nFine print:\n† Valid on orders of $25 or more. Headline benefit is limited to delivery in Arvale.\n* Orders must reach $200 or more in subtotal. An order whose delivery goes to Eskarth falls outside the headline benefit.\n\nOrder ORD-332010 placed by Lena Whitcombe:\n- item: SKU-80420\n- product category: toys\n- price status: final sale\n- delivery region: Arvale\n- order date: April 23, 2026\n- membership level: Elite\n- order subtotal: $25",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nPer what the advertisement says, which condition in the small print attached to free assembly does Lena Whitcombe's order ORD-332010 miss, if any?",
  "options": [
   "The order-subtotal condition",
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q49086683ec",
  "kind": "choice",
  "text": "Support chat about order ORD-127066:\nAiko Brandt: Hi, I placed order ORD-127066 on 9 Aug 2026 for item SKU-11820, and the order subtotal was $160.52.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Arvale delivery region.\nAgent: Your membership level is Black.\nAiko Brandt: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nA lifetime warranty on everything we sell*\n\nBring the family along\nLarkspur Playthings is a welcoming place for parents, grandparents and children, with friendly staff ready to help.\n\nFine print:\n* Valid for orders placed before 2 Sep 2026. Valid only for orders delivered to Eskarth.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Larkspur Playthings levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, which condition attached to the lifetime warranty does order ORD-127066 from Aiko Brandt miss, if any?",
  "options": [
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qc857024a7c",
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
  "qid": "q1e7f9b6382",
  "kind": "yes/no",
  "text": "Support chat about order ORD-625106:\nFelix Moreau: Hi, I placed order ORD-625106 on 2026-07-06 for item SKU-36193, and the order subtotal was 245.63 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is open box, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Blue.\nFelix Moreau: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nFree installation for every appliance*\n\nSay hi to the crew at Larkspur Playthings! We love helping you plan your getaway with trusted picks and friendly advice.\n*Delivery to Eskarth only. Order by 2026-07-18 at the latest.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-625106 from Felix Moreau get free installation?"
 },
 {
  "qid": "qcd24a3c6c4",
  "kind": "yes/no",
  "text": "Order ORD-694766 placed by Dana Okafor:\n| field | value |\n| --- | --- |\n| item | SKU-52637 |\n| product category | kitchenware |\n| price status | final sale |\n| delivery region | Dunmere |\n| order date | 2026-04-23 |\n| membership level | Blue |\n| order subtotal | 56.76 USD |\n\nAdvertisement from Tidewell Supply:\nWe match any lower price*\n\nSharp lines look best with a soft touch, so brush away dust and wipe it dry. Thanks for stopping by Tidewell Supply.\n\nFine print:\n* Order by 2026-05-27 at the latest. The subtotal of the order needs to be 75.00 USD or higher.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Tidewell Supply levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it not true that, under the advertised terms, order ORD-694766 from Dana Okafor does not get the price match?"
 },
 {
  "qid": "q7614522a60",
  "kind": "yes/no",
  "text": "Order ORD-357606 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-92739 |\n| product category | kitchenware |\n| price status | final sale |\n| delivery region | Hollin |\n| order date | 14 May 2026 |\n| membership level | Green |\n| order subtotal | $61.07 |\n\nAdvertisement from Northvale Audio:\nDouble reward points on every purchase*\nFree assembly with every delivery†\n\nWe hope your visit to Northvale Audio leaves you smiling and feeling welcome.\n\nFine print:\n* Reserved for members ranked Blue or higher. The order subtotal must be at least $50 for this offer to apply.\n† Placed before 15 May 2026 counts; that very day is excluded.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says alongside the advertised terms, does order ORD-357606 from Ravi Anand fail to secure double reward points?"
 },
 {
  "qid": "qcb9d45a6c9",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nFree assembly with every delivery*\nDouble reward points on every purchase†\n\nFine print:\n† Items whose status is refurbished sit outside this offer.\n* Valid for orders placed from Saturday, February 7, 2026 onward. Items drawn from the furniture category miss the headline benefit.\n\nCheerio from the cheerful crew at Brightwell Home, we have a heap of quirky bits waiting for a giggle.\n\nOrder ORD-204993 placed by Aiko Brandt:\n- item: SKU-79867\n- product category: pet supplies\n- price status: refurbished\n- delivery region: Greyhaven\n- order date: Sunday, March 15, 2026\n- membership level: Plus\n- order subtotal: $142.30",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says alongside the advertised terms, does order ORD-204993 from Aiko Brandt fail to secure free assembly?"
 }
]
