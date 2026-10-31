# G5-H blind read T07-blind_read-408cf0a5-004 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T07/qc/g5h/answers/T07-blind_read-408cf0a5-004.json

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
  "qid": "q08b76e0c95",
  "kind": "yes/no",
  "text": "Advertisement from Oakhurst Interiors:\nFree gift wrapping at checkout*\n\nOakhurst Interiors is live with new picks, so jump in and see what is trending.\n\nFine print:\n* Excludes all items with refurbished status. Every order placed on or after 22 February 2026 is covered by the offer.\n\nOrder ORD-993946 placed by Hugo Lindqvist:\n- item: SKU-84669\n- product category: garden tools\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: 31 March 2026\n- membership level: Gold\n- order subtotal: 174.67 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nRead with its small print, does the ad show that order ORD-993946 from Hugo Lindqvist earns free gift wrapping?"
 },
 {
  "qid": "q220bd68122",
  "kind": "yes/no",
  "text": "Advertisement from Pebblestone Garden:\nFree gift wrapping at checkout*\nFree shipping on every order†\n\nFine print:\n† Each item bearing the pre-order status is withheld from the main benefit.\n* Only items with refurbished status are excluded from the main benefit.\n\nSubject: A warm hello from our team\nDear friend, we love sharing our newest pieces with you at Pebblestone Garden.\n\nOrder ORD-551637 placed by Nadia Haddad:\n- item: SKU-34017\n- product category: furniture\n- price status: clearance\n- delivery region: Hollin\n- order date: Friday, 17 April 2026\n- membership level: Bronze\n- order subtotal: 97.38 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Pebblestone Garden levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWould you say it is not the case that Nadia Haddad does not get free shipping on order ORD-551637 when the advertisement and its fine print are read?"
 },
 {
  "qid": "qc92fcf9484",
  "kind": "yes/no",
  "text": "Advertisement from Birchwood Linens:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\nFast forward\nOur team at Birchwood Linens has sharpened the edit with sleek, refined pieces.\n\nFine print:\n† Order subtotal exceeds $150. Headline benefit applies to orders with delivery in Arvale only.\n* Anything with delivery in Fallowmere is excluded from the headline benefit.\n\nOrder ORD-782502 placed by Jonah Pryce:\n- item: SKU-72153\n- product category: electronics\n- price status: pre-order\n- delivery region: Arvale\n- order date: Monday, July 20, 2026\n- membership level: Elite\n- order subtotal: 150.01 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking the advertisement and its fine print into account, has order ORD-782502 from Jonah Pryce lost out on free gift wrapping?"
 },
 {
  "qid": "q970e591a40",
  "kind": "choice",
  "text": "Order ORD-679171 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-96486 |\n| product category | kitchenware |\n| price status | pre-order |\n| delivery region | Brenmoor |\n| order date | 2026-05-27 |\n| membership level | Gold |\n| order subtotal | 112.28 USD |\n\nAdvertisement from Kestrel Outfitters:\nDouble reward points on every purchase*\nFree gift wrapping at checkout†\n\nFine print:\n† An order whose delivery goes to Brenmoor falls outside the headline benefit. Items must belong to the kitchenware product category to earn the benefit.\n* The order date needs to be on or before 2026-05-26.\n\nA bit of dusting goes a long way. Thanks, and happy handling from Kestrel Outfitters.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, which condition in the small print attached to double reward points does order ORD-679171 from Clara Voss miss, if any?",
  "options": [
   "The order-date condition",
   "The product-category condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qad7711d0f7",
  "kind": "yes/no",
  "text": "Advertisement from Birchwood Linens:\nFree shipping on every order*\nWe match any lower price†\n\nWelcome to our pages\nThe people at Birchwood Linens have gathered thoughtful pieces that feel right at home.\n\nFine print:\n* An order placed on or before 7 August 2026 qualifies.\n† Applies to orders placed on or after 6 August 2026. The headline benefit is set aside for anything in the bedding category.\n\nOrder ORD-949387 placed by Nadia Haddad:\n- item: SKU-81310\n- product category: sports gear\n- price status: final sale\n- delivery region: Eskarth\n- order date: 17 August 2026\n- membership level: Plus\n- order subtotal: $126.16",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Birchwood Linens levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-949387 placed by Nadia Haddad doesn't get the price match under the advertised terms, based on the ad and its small print?"
 },
 {
  "qid": "qdc5d6682ee",
  "kind": "choice",
  "text": "Advertisement from Marigold Pets:\nA lifetime warranty on everything we sell*\n\nFine print:\n* Every item in the garden tools category falls outside the offer. The headline benefit stops short of delivery to Dunmere.\n\nCrafted for quiet pleasure\nThis guide introduces refined pieces, careful craftsmanship and gentle colours from Marigold Pets.\n\nOrder ORD-296426 placed by Clara Voss:\n- item: SKU-12161\n- product category: bedding\n- price status: regular price\n- delivery region: Dunmere\n- order date: Tuesday, 26 May 2026\n- membership level: Green\n- order subtotal: $50.89",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe ad and its small print tie conditions to the lifetime warranty; which, if any, does order ORD-296426 from Clara Voss miss?",
  "options": [
   "The product-category condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q23c7e93ff4",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nFree assembly with every delivery*\nFree shipping on every order†\n\nFine print:\n* Orders must reach $50.00 or more in subtotal.\n† Qualifying orders include the date 20 June 2026 and every later day.\n\nNeighbours, come and say hello\nPop round to Fernway Market for a warm chat and a relaxed browse.\n\nOrder ORD-837297 placed by Jonah Pryce:\n- item: SKU-18083\n- product category: electronics\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 16 June 2026\n- membership level: Silver\n- order subtotal: $48.23",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does order ORD-837297 from Jonah Pryce truly get under the advertisement and its fine print?",
  "options": [
   "Neither offer",
   "Only free assembly",
   "Only free shipping",
   "Both offers"
  ]
 },
 {
  "qid": "q0d6e52dc38",
  "kind": "yes/no",
  "text": "Support chat about order ORD-422652:\nClara Voss: Hi, I placed order ORD-422652 on Sunday, August 23, 2026 for item SKU-27767, and the order subtotal was $200.01.\nAgent: Thanks. The item is in the toys product category, its price status is refurbished, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Gold.\nClara Voss: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree shipping on every order*\nDouble reward points on every purchase†\n\nSoft light, gentle music and a calm atmosphere: that is Juniper Gadgets at its finest.\n\nFine print:\n* Valid on orders over $75.00. Every item priced as open box is excluded from this offer.\n† Any delivery to Dunmere is excluded from this offer. Order subtotal must go beyond $200.00. Members whose level is at least Gold can redeem it.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad and its small print say that order ORD-422652 from Clara Voss gets double reward points?"
 },
 {
  "qid": "q23bbe6c017",
  "kind": "choice",
  "text": "Advertisement from Harborlight Goods:\nDouble reward points on every purchase*\nFree installation for every appliance†\n\nGrown-ups and children alike enjoy this, so rinse it gently and dry it well. Thanks from the crew at Harborlight Goods.\n\nFine print:\n† Delivery to Eskarth sits outside the headline benefit. Any product that belongs to the electronics category is excluded from the offer.\n* Items marked with the open box status fall outside the benefit set out here. Any delivery to Brenmoor is excluded from this offer.\n\nOrder ORD-978893 placed by Kofi Asante:\n- item: SKU-75110\n- product category: bedding\n- price status: refurbished\n- delivery region: Brenmoor\n- order date: 28 May 2026\n- membership level: Silver\n- order subtotal: $26.50",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking Kofi Asante's order ORD-978893 against the ad and its small print, which condition attached to double reward points does it miss, if any?",
  "options": [
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition",
   "The price-status condition"
  ]
 },
 {
  "qid": "qa4d9fd22cb",
  "kind": "choice",
  "text": "Advertisement from Marigold Pets:\nA lifetime warranty on everything we sell*\n\nFine print:\n* Every item in the bedding category falls outside the offer. The headline benefit stops short of delivery to Dunmere.\n\nCrafted for quiet pleasure\nThis guide introduces refined pieces, careful craftsmanship and gentle colours from Marigold Pets.\n\nOrder ORD-382384 placed by Selin Yilmaz:\n- item: SKU-89291\n- product category: electronics\n- price status: final sale\n- delivery region: Dunmere\n- order date: Wednesday, September 23, 2026\n- membership level: Blue\n- order subtotal: $193.08",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe ad and its small print tie conditions to the lifetime warranty; which, if any, does order ORD-382384 from Selin Yilmaz miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qf32731adb8",
  "kind": "choice",
  "text": "Support chat about order ORD-259333:\nHugo Lindqvist: Hi, I placed order ORD-259333 on 9 August 2026 for item SKU-42029, and the order subtotal was 113.29 USD.\nAgent: Thanks. The item is in the toys product category, its price status is refurbished, and it ships to the Greyhaven delivery region.\nAgent: Your membership level is Premier.\nHugo Lindqvist: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nFree gift wrapping at checkout*\nDouble reward points on every purchase†\n\nCheers for popping round to Wrenfield Outdoor, your local corner shop.\n\nFine print:\n† The headline benefit stops short of delivery to Greyhaven.\n* Eligibility is limited to the electronics category. Stock with refurbished status is excluded from this benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, drawn from the ad and its small print attached to double reward points, does order ORD-259333 from Hugo Lindqvist miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition",
   "The price-status condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q6354ae1265",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nFree assembly with every delivery*\nFree installation for every appliance†\n\nThanks for dropping by, neighbour! Store it in a cool corner, give it a gentle brush here and there, and tell your friends about Kestrel Outfitters.\n\nFine print:\n* Anything filed under the electronics category sits outside this offer. Any item priced as clearance sits outside the headline benefit.\n† Eligibility for the benefit is restricted to the sports gear product category.\n\nOrder ORD-770652 placed by Owen Mensah:\n- item: SKU-67438\n- product category: electronics\n- price status: final sale\n- delivery region: Hollin\n- order date: Thursday, August 6, 2026\n- membership level: Black\n- order subtotal: 34.14 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDo the advertisement and its fine print together let order ORD-770652 from Owen Mensah get free assembly?"
 },
 {
  "qid": "qc5ecc38fca",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree returns on every purchase*\nFree shipping on every order†\n\nFine print:\n* Orders headed for delivery in Dunmere are kept out of this offer.\n† Reserved for the Premier level and lower.\n\nGrab the kids and pop by Brightwell Home, where there is a lot to look at.\n\nOrder ORD-639095 placed by Owen Mensah:\n- item: SKU-56567\n- product category: furniture\n- price status: clearance\n- delivery region: Hollin\n- order date: 18 Sep 2026\n- membership level: Premier\n- order subtotal: 82.38 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor the order ORD-639095 placed by Owen Mensah, which of the advertised terms does it actually get when the small print is checked offer by offer?",
  "options": [
   "Only free shipping",
   "Only free returns",
   "Neither offer",
   "Both offers"
  ]
 },
 {
  "qid": "qa00be56f30",
  "kind": "yes/no",
  "text": "Order ORD-319360 placed by Hugo Lindqvist:\n| field | value |\n| --- | --- |\n| item | SKU-12651 |\n| product category | kitchenware |\n| price status | clearance |\n| delivery region | Hollin |\n| order date | Monday, August 10, 2026 |\n| membership level | Gold |\n| order subtotal | $200.13 |\n\nAdvertisement from Kestrel Outfitters:\nFree gift wrapping at checkout*\nWe match any lower price†\n\n{\"title\": \"The finest lineup at Kestrel Outfitters\", \"subtitle\": \"Curated lines, presented with clarity and poise\", \"button\": \"Start exploring\"}\n\nFine print:\n† Orders must reach $200.00 or more in subtotal.\n* Valid for orders placed on or before Friday, August 14, 2026.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-319360 from Hugo Lindqvist forfeit free gift wrapping under the advertised terms, as set out by the advertisement and its fine print?"
 },
 {
  "qid": "q924ec0d3d7",
  "kind": "yes/no",
  "text": "Support chat about order ORD-466191:\nPriya Raman: Hi, I placed order ORD-466191 on 2026-08-11 for item SKU-92516, and the order subtotal was $200.00.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Hollin delivery region.\nAgent: Your membership level is Silver.\nPriya Raman: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree assembly with every delivery*\nWe match any lower price†\n\nSubject: So glad you dropped in\nDear visitor, Cedarline Living is delighted to welcome you with a warm smile.\n\nFine print:\n* Placed before 2026-08-11 counts; that very day is excluded. Order subtotal must go beyond $200.00.\n† Goods in the sports gear category fall outside the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhen the headline and its small print are read against the advertised terms, does order ORD-466191 from Priya Raman receive free assembly?"
 },
 {
  "qid": "qfcb4eb568f",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nFine print:\n* Any item priced as pre-order sits outside the headline benefit. Applies to orders placed on or after Monday, September 14, 2026.\n† Items at clearance pricing are withheld from this benefit.\n\nFresh looks, quick decisions\nSharp design, bold colour and easy choices are waiting for you at Northvale Audio.\n\nOrder ORD-757989 placed by Felix Moreau:\n- item: SKU-36670\n- product category: bedding\n- price status: pre-order\n- delivery region: Brenmoor\n- order date: Tuesday, October 20, 2026\n- membership level: Plus\n- order subtotal: $126.71",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGiven the advertisement and its fine print, which of its headline offers does order ORD-757989, placed by Felix Moreau, really get?",
  "options": [
   "Neither offer",
   "Only free shipping",
   "Only free gift wrapping",
   "Both offers"
  ]
 },
 {
  "qid": "q1ea0e7fb47",
  "kind": "yes/no",
  "text": "Support chat about order ORD-539235:\nClara Voss: Hi, I placed order ORD-539235 on Sunday, 3 May 2026 for item SKU-61778, and the order subtotal was $80.16.\nAgent: Thanks. The item is in the kitchenware product category, its price status is final sale, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Platinum.\nClara Voss: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree installation for every appliance*\nDouble reward points on every purchase†\n\nGot a list? Cedarline Living has the basics on the shelves.\n\nFine print:\n* Every order placed on or after Wednesday, 8 April 2026 is covered by the offer.\n† Shoppers get the headline benefit solely for delivery in Eskarth. For Gold members and below.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-539235 from Clara Voss come with free installation under what the advertisement says, headline and small print included?"
 },
 {
  "qid": "qb1f1328d83",
  "kind": "yes/no",
  "text": "Order ORD-568551 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-77972 |\n| product category | kitchenware |\n| price status | clearance |\n| delivery region | Greyhaven |\n| order date | Thursday, 16 July 2026 |\n| membership level | Gold |\n| order subtotal | 100.00 USD |\n\nAdvertisement from Marigold Pets:\nFree shipping on every order*\n\nSophisticated and calm\nAt Marigold Pets, modest pieces rest in soft light, chosen for their composure and subtle finish.\n\nFine print:\n* Minimum order subtotal: 100.00 USD. Orders submitted on or before Wednesday, 15 July 2026 are accepted.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-568551 from Ravi Anand does not get free shipping under the advertised terms, per the ad and its small print?"
 },
 {
  "qid": "q337c9a0b99",
  "kind": "choice",
  "text": "Advertisement from Copperleaf Kitchen:\nFree returns on every purchase*\nFree installation for every appliance†\n\nGive the surface a wipe and check the joints for loose bits. Thanks from the crew at Copperleaf Kitchen.\n\nOrder ORD-955055 placed by Tomas Ferreira:\n- item: SKU-38190\n- product category: toys\n- price status: pre-order\n- delivery region: Hollin\n- order date: June 18, 2026\n- membership level: Silver\n- order subtotal: 95.65 USD\n\nFine print from the bottom of the advertisement:\n* Placed on or after June 18, 2026, the order qualifies. Minimum order subtotal: 75.00 USD. Items at pre-order pricing are withheld from this benefit.\n† Only orders placed before July 25, 2026 count toward this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, which condition attached to free returns does order ORD-955055 from Tomas Ferreira miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The price-status condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "qad6fe62559",
  "kind": "yes/no",
  "text": "Order ORD-407905 placed by Mira Castell:\n| field | value |\n| --- | --- |\n| item | SKU-72809 |\n| product category | sports gear |\n| price status | pre-order |\n| delivery region | Calderon |\n| order date | 28 Feb 2026 |\n| membership level | Green |\n| order subtotal | $173.48 |\n\nAdvertisement from Brightwell Home:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nCheers for popping round to Brightwell Home, your local corner shop.\n\nFine print:\n* Anything with delivery in Greyhaven is excluded from the headline benefit.\n† Applies to members up to Green or lower.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does the order ORD-407905 placed by Mira Castell fail to earn the price match, based on the ad and its small print?"
 },
 {
  "qid": "q13a3ccca10",
  "kind": "choice",
  "text": "Advertisement from Pebblestone Garden:\nFree gift wrapping at checkout*\nFree shipping on every order†\n\nPebblestone Garden is where considered style meets true craft, and it shows in the displays.\n\nFine print:\n* Order by Saturday, 13 June 2026 at the latest. Products in the toys category are excluded from this offer.\n† Orders submitted on or before Saturday, 18 July 2026 are accepted.\n\nOrder ORD-913781 placed by Priya Raman:\n- item: SKU-29757\n- product category: bedding\n- price status: pre-order\n- delivery region: Dunmere\n- order date: Saturday, 13 June 2026\n- membership level: Platinum\n- order subtotal: $27.12",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-913781 from Priya Raman, which headline offers does what the advertisement says actually grant, checked offer by offer against small print?",
  "options": [
   "Only free shipping",
   "Both offers",
   "Neither offer",
   "Only free gift wrapping"
  ]
 },
 {
  "qid": "q5b8fbada28",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree returns on every purchase*\nFree gift wrapping at checkout†\n\nWe appreciate your custom at Larkspur Playthings. Look closely at the stitching and tighten loose fixings gently.\n\nFine print:\n* Orders must be placed on or after 1 August 2026. The order subtotal must be strictly greater than 200.00 USD.\n† Eligibility is limited to the kitchenware category. Valid: any order taken on or before 1 August 2026.\n\nOrder ORD-241677 placed by Aiko Brandt:\n- item: SKU-25686\n- product category: sports gear\n- price status: clearance\n- delivery region: Calderon\n- order date: 1 August 2026\n- membership level: Elite\n- order subtotal: 200.01 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-241677 from Aiko Brandt fail to get free returns under the advertised terms, as the advertisement and its fine print spell out?"
 },
 {
  "qid": "q91f8338240",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nFree shipping on every order*\nA lifetime warranty on everything we sell†\n\nSubject: Shopping trips made gentle\nHello, Kestrel Outfitters is set up for busy households, with calm aisles and friendly help close by.\n\nOrder ORD-416332 placed by Felix Moreau:\n- item: SKU-73551\n- product category: furniture\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: Tuesday, July 28, 2026\n- membership level: Blue\n- order subtotal: 109.82 USD\n\nFine print from the bottom of the advertisement:\n* Any item priced as refurbished sits outside the headline benefit.\n† Minimum order subtotal: $150. Excludes items with refurbished status.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Kestrel Outfitters levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking the advertisement and its fine print into account, has order ORD-416332 from Felix Moreau lost out on free shipping?"
 },
 {
  "qid": "q7626280d1c",
  "kind": "yes/no",
  "text": "Order ORD-699689 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-27116 |\n| product category | kitchenware |\n| price status | pre-order |\n| delivery region | Greyhaven |\n| order date | Monday, 15 June 2026 |\n| membership level | Plus |\n| order subtotal | $180.40 |\n\nAdvertisement from Fernway Market:\nDouble reward points on every purchase*\n\nHello from Fernway Market, your friendly local spot! Fresh bread and crisp apples are waiting, so pop by and say hello.\n*Valid only for orders delivered to Arvale.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWould it be fair to say it is not the case that Nadia Haddad does not get double reward points on order ORD-699689 under the advertised terms?"
 },
 {
  "qid": "q312715dc97",
  "kind": "choice",
  "text": "Support chat about order ORD-320810:\nMira Castell: Hi, I placed order ORD-320810 on 22 Aug 2026 for item SKU-64080, and the order subtotal was 32.89 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is open box, and it ships to the Greyhaven delivery region.\nAgent: Your membership level is Plus.\nMira Castell: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nDouble reward points on every purchase*\n\nWelcome to Pebblestone Garden, a place where parents and children wander the aisles together.\n\nFine print:\n* Orders placed on 23 Aug 2026 itself are excluded. Members ranked Premier and above are the only ones covered.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Pebblestone Garden levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nMeasured against the advertised terms, which condition in the small print attached to double reward points does Mira Castell's order ORD-320810 miss, if any?",
  "options": [
   "The membership-level condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q72cdc2a2ec",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree returns on every purchase*\n\nFine print:\n* Products assigned to the garden tools category are excluded.\n\nFamily-friendly, warm and relaxed, we hope Wrenfield Outdoor becomes a go-to stop for you and yours.\n\nOrder ORD-500164 placed by Nadia Haddad:\n- item: SKU-74169\n- product category: bedding\n- price status: regular price\n- delivery region: Fallowmere\n- order date: 12 September 2026\n- membership level: Bronze\n- order subtotal: $158",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad, with its small print taken into account, mean that Nadia Haddad earns free returns on order ORD-500164?"
 },
 {
  "qid": "q27707e7c97",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree assembly with every delivery*\n\nGather your crew, because Marigold Pets is set for a wild and wonderful stretch of trails.\n*For Black members and above. Excludes delivery to Brenmoor.\n\nOrder ORD-838704 placed by Lena Whitcombe:\n- item: SKU-95173\n- product category: sports gear\n- price status: regular price\n- delivery region: Eskarth\n- order date: October 10, 2026\n- membership level: Black\n- order subtotal: 163.55 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Marigold Pets levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder what the advertisement says, headline and small print included, does Lena Whitcombe get free assembly on order ORD-838704?"
 },
 {
  "qid": "qe4cbb876c7",
  "kind": "choice",
  "text": "Advertisement from Kestrel Outfitters:\nFree gift wrapping at checkout*\n\nUseful things for the home\nOur staff at Kestrel Outfitters gathered handy items that do the job and feel good in your hands.\n\nFine print:\n* Earlier orders are accepted, and so is the date 25 May 2026 itself. Orders headed for delivery in Dunmere are kept out of this offer. Items whose status is refurbished are excluded.\n\nOrder ORD-505993 placed by Clara Voss:\n- item: SKU-93879\n- product category: pet supplies\n- price status: open box\n- delivery region: Hollin\n- order date: 25 May 2026\n- membership level: Black\n- order subtotal: 236.58 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nAccording to what the advertisement says, which condition attached to free gift wrapping does order ORD-505993 from Clara Voss miss, if any?",
  "options": [
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The order-date condition"
  ]
 },
 {
  "qid": "q5acb5a617e",
  "kind": "choice",
  "text": "Order ORD-245727 placed by Kofi Asante:\n| field | value |\n| --- | --- |\n| item | SKU-92311 |\n| product category | toys |\n| price status | pre-order |\n| delivery region | Greyhaven |\n| order date | 19 October 2026 |\n| membership level | Plus |\n| order subtotal | $74.99 |\n\nAdvertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\nFree returns on every purchase†\n\nHello, sunshine\nDrop by Copperleaf Kitchen for a stroll along lively shelves and cheerful ideas.\n\nFine print:\n* An order placed on or before 4 October 2026 qualifies.\n† Customers must spend at least $75 on the order subtotal.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says, small print included, offer by offer, which headline offers does order ORD-245727 from Kofi Asante actually get?",
  "options": [
   "Both offers",
   "Only free returns",
   "Only free assembly",
   "Neither offer"
  ]
 },
 {
  "qid": "qf998ea97f0",
  "kind": "yes/no",
  "text": "Order ORD-738989 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-40399 |\n| product category | pet supplies |\n| price status | pre-order |\n| delivery region | Dunmere |\n| order date | 16 April 2026 |\n| membership level | Green |\n| order subtotal | $58.59 |\n\nAdvertisement from Brightwell Home:\nDouble reward points on every purchase*\n\nFine print:\n* Goods filed under a different category from pet supplies fall outside the benefit. Items priced as refurbished are excluded.\n\nYou are very welcome at Brightwell Home. Our refined range brings clarity and character to the corners of your home.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, does order ORD-738989 from Clara Voss fail to receive double reward points under the advertised terms?"
 },
 {
  "qid": "q9c390b7f6d",
  "kind": "yes/no",
  "text": "Order ORD-552991 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-81813 |\n| product category | sports gear |\n| price status | regular price |\n| delivery region | Arvale |\n| order date | 28 Jul 2026 |\n| membership level | Blue |\n| order subtotal | $249.12 |\n\nAdvertisement from Northvale Audio:\nDouble reward points on every purchase*\n\nNorthvale Audio has sharp new picks for you. Stop by and see what is fresh.\n*Valid for orders placed on or after 1 Aug 2026. Minimum order subtotal: $200.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-552991 from Ines Duarte come with double reward points under the ad and its small print?"
 },
 {
  "qid": "qf12bf309e8",
  "kind": "choice",
  "text": "Advertisement from Oakhurst Interiors:\nDouble reward points on every purchase*\nFree installation for every appliance†\n\n{\"title\": \"Oakhurst Interiors app\", \"subtitle\": \"Browse the range, build a list, and check out quickly\", \"button\": \"Get started\"}\n\nFine print:\n† For Silver members and below. Delivery to Eskarth is the sole route to the headline benefit.\n* Restricted to members at the Bronze level and lower.\n\nOrder ORD-181556 placed by Ravi Anand:\n- item: SKU-43593\n- product category: electronics\n- price status: regular price\n- delivery region: Eskarth\n- order date: Sunday, May 3, 2026\n- membership level: Silver\n- order subtotal: 138.56 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nLooking at the advertisement and its fine print, which condition attached to free installation does customer Ravi Anand, on order ORD-181556, miss, if any?",
  "options": [
   "The membership-level condition",
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q149c5e51d0",
  "kind": "yes/no",
  "text": "Support chat about order ORD-377642:\nRavi Anand: Hi, I placed order ORD-377642 on Friday, October 9, 2026 for item SKU-89720, and the order subtotal was $94.78.\nAgent: Thanks. The item is in the garden tools product category, its price status is refurbished, and it ships to the Greyhaven delivery region.\nAgent: Your membership level is Green.\nRavi Anand: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\nWe are glad you picked Birchwood Linens for your home. Clean it gently, let it air dry, and put it back in its place.\n\nFine print:\n† Membership tier Blue or lower applies. An order placed on or before Thursday, October 8, 2026 qualifies.\n* Items whose status is refurbished are excluded.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-377642 from Ravi Anand come with free gift wrapping under the ad and its small print?"
 },
 {
  "qid": "q3f8a8b0267",
  "kind": "yes/no",
  "text": "Advertisement from Birchwood Linens:\nFree shipping on every order*\n\nFine print:\n* Items whose status is open box are excluded. Customers must spend at least $200 on the order subtotal.\n\nUnderstated materials, soft tones and a serene layout suit the discerning eye at Birchwood Linens.\n\nOrder ORD-941863 placed by Lena Whitcombe:\n- item: SKU-26583\n- product category: kitchenware\n- price status: pre-order\n- delivery region: Brenmoor\n- order date: Thursday, April 23, 2026\n- membership level: Elite\n- order subtotal: $200",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-941863 from Lena Whitcombe forfeit free shipping under the advertised terms, as those terms are written?"
 },
 {
  "qid": "q36dc5871a6",
  "kind": "yes/no",
  "text": "Support chat about order ORD-123124:\nLena Whitcombe: Hi, I placed order ORD-123124 on Wednesday, June 24, 2026 for item SKU-39760, and the order subtotal was 21.26 USD.\nAgent: Thanks. The item is in the bedding product category, its price status is pre-order, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Silver.\nLena Whitcombe: I am asking about the advertisement below.\n\nAdvertisement from Marigold Pets:\nFree returns on every purchase*\nFree installation for every appliance†\n\nRefined essentials\nMarigold Pets brings calm, well-made pieces right to your screen.\n\nFine print:\n* Applies to orders placed on or after Monday, May 25, 2026. Items at the clearance pricing status sit outside this promotion.\n† Anything with delivery in Calderon is excluded from the headline benefit. Eligibility for the benefit is restricted to the bedding product category.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Marigold Pets levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nMeasured against the advertised terms in full, does order ORD-123124 from Lena Whitcombe fail to secure free returns?"
 },
 {
  "qid": "q9f77f761bf",
  "kind": "yes/no",
  "text": "Order ORD-791001 placed by Dana Okafor:\n| field | value |\n| --- | --- |\n| item | SKU-75623 |\n| product category | garden tools |\n| price status | regular price |\n| delivery region | Calderon |\n| order date | 11 Aug 2026 |\n| membership level | Platinum |\n| order subtotal | $50.01 |\n\nAdvertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\nFree assembly with every delivery†\n\nBring the kids along to Kestrel Outfitters for a fun look around the shop.\n\nFine print:\n† Order subtotal strictly more than $50.00.\n* Applies to Platinum level and higher members.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-791001 from Dana Okafor come with the lifetime warranty under the ad and its small print?"
 },
 {
  "qid": "qfab50e4bbd",
  "kind": "choice",
  "text": "Order ORD-898133 placed by Selin Yilmaz:\n- item: SKU-15890\n- product category: bedding\n- price status: final sale\n- delivery region: Brenmoor\n- order date: 14 August 2026\n- membership level: Premier\n- order subtotal: 49.99 USD\n\nAdvertisement from Fernway Market:\nWe match any lower price*\nFree assembly with every delivery†\n\nFine print:\n* Qualifying orders are placed before 15 August 2026, excluding that date. Shoppers get the headline benefit solely for delivery in Brenmoor.\n† Valid for orders whose subtotal is $50 or more.\n\nHooray for shoppers like you! Thanks for roaming the aisles of Fernway Market.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nLooking at the ad and its small print, which condition attached to the price match does order ORD-898133 from Selin Yilmaz miss, if any?",
  "options": [
   "The order-subtotal condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qb59428640a",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nThanks for dropping by, neighbour! Store it in a cool corner, give it a gentle brush here and there, and tell your friends about Kestrel Outfitters.\n\nFine print:\n* Items listed at final sale pricing are excluded from the benefit.\n\nOrder ORD-250564 placed by Hugo Lindqvist:\n- item: SKU-36580\n- product category: kitchenware\n- price status: final sale\n- delivery region: Hollin\n- order date: 23 Mar 2026\n- membership level: Blue\n- order subtotal: 31.95 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-250564 from Hugo Lindqvist lose out on the lifetime warranty according to the advertisement and its fine print?"
 },
 {
  "qid": "q983e2694a4",
  "kind": "choice",
  "text": "Support chat about order ORD-357178:\nNadia Haddad: Hi, I placed order ORD-357178 on 2026-08-21 for item SKU-95450, and the order subtotal was $50.95.\nAgent: Thanks. The item is in the sports gear product category, its price status is clearance, and it ships to the Calderon delivery region.\nAgent: Your membership level is Silver.\nNadia Haddad: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree installation for every appliance*\nFree returns on every purchase†\n\nThoughtfully sourced living\nExplore the range at Cedarline Living, where careful craft meets the tastes of contemporary homes.\n\nFine print:\n† The order subtotal must be above $50.00. Products sitting in any category besides sports gear fall outside this offer.\n* Items whose status is refurbished sit outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, if any, tied to free returns in what the advertisement says does order ORD-357178 from Nadia Haddad miss?",
  "options": [
   "The product-category condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition"
  ]
 },
 {
  "qid": "q65f7518b54",
  "kind": "yes/no",
  "text": "Support chat about order ORD-541443:\nJonah Pryce: Hi, I placed order ORD-541443 on August 28, 2026 for item SKU-11529, and the order subtotal was 221.44 USD.\nAgent: Thanks. The item is in the electronics product category, its price status is regular price, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Platinum.\nJonah Pryce: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\n\nRefined essentials\nJuniper Gadgets brings calm, well-made pieces right to your screen.\n\nFine print:\n* Only members at the Gold level or higher may take part. Any product that belongs to the sports gear category is excluded from the offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-541443 placed by Jonah Pryce doesn't get free gift wrapping under the advertised terms, based on the advertisement and its fine print?"
 },
 {
  "qid": "q85f1603b23",
  "kind": "choice",
  "text": "Advertisement from Tidewell Supply:\nWe match any lower price*\nDouble reward points on every purchase†\n\nSkip the clutter. Tidewell Supply keeps things sleek, simple and easy to navigate.\n\nOrder ORD-926300 placed by Priya Raman:\n- item: SKU-25491\n- product category: garden tools\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 2 September 2026\n- membership level: Premier\n- order subtotal: $154.95\n\nFine print from the bottom of the advertisement:\n† Only members at the Premier level or higher may take part. Excludes the garden tools category.\n* Any order placed on 2 September 2026 and beyond is accepted.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the small print attached to double reward points among the advertised terms does order ORD-926300 from Priya Raman miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition",
   "The order-date condition",
   "The product-category condition"
  ]
 },
 {
  "qid": "qb3af1f992c",
  "kind": "choice",
  "text": "Support chat about order ORD-134908:\nJonah Pryce: Hi, I placed order ORD-134908 on 14 March 2026 for item SKU-84697, and the order subtotal was 67.29 USD.\nAgent: Thanks. The item is in the bedding product category, its price status is clearance, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Basic.\nJonah Pryce: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree returns on every purchase*\nDouble reward points on every purchase†\n\nTinkering, tinkling and tidy little treasures: that is Oakhurst Interiors in a nutshell.\n\nFine print:\n† Applies to Plus level and higher members.\n* Items must belong to the bedding product category to earn the benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does customer Jonah Pryce on order ORD-134908 truly receive, given what the advertisement says?",
  "options": [
   "Only double reward points",
   "Only free returns",
   "Both offers",
   "Neither offer"
  ]
 },
 {
  "qid": "q0184289588",
  "kind": "choice",
  "text": "Advertisement from Larkspur Playthings:\nFree assembly with every delivery*\nFree installation for every appliance†\n\nCalm design, honest craft and a thoughtful eye for quality. Visit Larkspur Playthings and see the range for yourself.\n\nFine print:\n† Headline benefit applies to orders with delivery in Dunmere only.\n* Orders headed for delivery in Brenmoor are kept out of this offer.\n\nOrder ORD-615186 placed by Kofi Asante:\n- item: SKU-94303\n- product category: pet supplies\n- price status: final sale\n- delivery region: Dunmere\n- order date: 25 October 2026\n- membership level: Elite\n- order subtotal: 91.61 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertisement and its fine print, which of its headline offers does customer Kofi Asante truly receive on order ORD-615186?",
  "options": [
   "Neither offer",
   "Only free installation",
   "Only free assembly",
   "Both offers"
  ]
 },
 {
  "qid": "q127eb9dd9d",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nDouble reward points on every purchase*\n\nHooray, you have found Brightwell Home! Make yourself at ease and let the fun begin.\n\nFine print:\n* Order subtotal strictly more than 35.00 USD.\n\nOrder ORD-176663 placed by Felix Moreau:\n| field | value |\n| --- | --- |\n| item | SKU-74456 |\n| product category | bedding |\n| price status | pre-order |\n| delivery region | Greyhaven |\n| order date | 26 May 2026 |\n| membership level | Basic |\n| order subtotal | 44.95 USD |",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertised terms, which include the headline and its small print, does Felix Moreau come with double reward points on order ORD-176663?"
 },
 {
  "qid": "q02e43e9e23",
  "kind": "yes/no",
  "text": "Advertisement from Bluecrest Sports:\nFree shipping on every order*\n\nFine print:\n* Orders dated on or before 9 June 2026 count.\n\nGive the surface a wipe and check the joints for loose bits. Thanks from the crew at Bluecrest Sports.\n\nOrder ORD-626063 placed by Ravi Anand:\n- item: SKU-74750\n- product category: bedding\n- price status: final sale\n- delivery region: Dunmere\n- order date: 23 May 2026\n- membership level: Green\n- order subtotal: 195.92 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print together, does order ORD-626063 from Ravi Anand fail to secure free shipping under the advertised terms?"
 },
 {
  "qid": "qc370c8792a",
  "kind": "choice",
  "text": "Order ORD-723916 placed by Hugo Lindqvist:\n| field | value |\n| --- | --- |\n| item | SKU-74138 |\n| product category | pet supplies |\n| price status | open box |\n| delivery region | Dunmere |\n| order date | Wednesday, February 25, 2026 |\n| membership level | Blue |\n| order subtotal | $25 |\n\nAdvertisement from Tidewell Supply:\nWe match any lower price*\nFree assembly with every delivery†\n\nFine print:\n† Covers the pet supplies product category only. Items at the open box pricing status sit outside this promotion.\n* Subtotal of $25 or more required. Applies to members of the Blue level or lower.\n\nCaring for this piece is straightforward. Use a soft brush for dust, and let the finish breathe between uses. It was a pleasure to serve you at Tidewell Supply.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-723916 from Hugo Lindqvist and reading the ad and its small print, which condition attached to the price match does it miss, if any?",
  "options": [
   "The product-category condition",
   "The order-subtotal condition",
   "The membership-level condition",
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qe8d3e0d3b7",
  "kind": "choice",
  "text": "Order ORD-538898 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-42354 |\n| product category | electronics |\n| price status | regular price |\n| delivery region | Arvale |\n| order date | Friday, May 22, 2026 |\n| membership level | Basic |\n| order subtotal | 212.73 USD |\n\nAdvertisement from Harborlight Goods:\nFree shipping on every order*\n\nIt's lovely to have you here. Let the item rest somewhere cool and dry, and feel welcome to call on Harborlight Goods anytime.\n\nFine print:\n* The headline benefit stops short of delivery to Fallowmere. Placed before Wednesday, May 6, 2026 counts; that very day is excluded.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, if any, tied to free shipping in what the advertisement says does order ORD-538898 from Aiko Brandt miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition",
   "The order-date condition"
  ]
 },
 {
  "qid": "q6a0a53cf7b",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nWe match any lower price*\nFree installation for every appliance†\n\nHello, friend\nThe kettle is bubbling and the shelves look inviting at Fernway Market, so pull up a chair and wander at a relaxed pace.\n\nFine print:\n† Valid only for orders delivered to Brenmoor. Orders must be placed before May 25, 2026, and the day itself is excluded.\n* Reserved for members ranked Platinum or higher. Order by May 24, 2026 at the latest.\n\nOrder ORD-862866 placed by Nadia Haddad:\n- item: SKU-95122\n- product category: pet supplies\n- price status: regular price\n- delivery region: Brenmoor\n- order date: May 25, 2026\n- membership level: Platinum\n- order subtotal: 76.17 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nSetting order ORD-862866 from Nadia Haddad beside the advertisement and its fine print, which condition attached to the price match does it miss, if any?",
  "options": [
   "The delivery-region condition",
   "The membership-level condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q34785cd14a",
  "kind": "choice",
  "text": "Advertisement from Cedarline Living:\nFree gift wrapping at checkout*\nFree assembly with every delivery†\n\nSubject: Tidy layout, simple search\nHello, the crisp design of Cedarline Living keeps the range in clear view and within easy grasp.\n\nOrder ORD-641488 placed by Owen Mensah:\n- item: SKU-15962\n- product category: bedding\n- price status: regular price\n- delivery region: Greyhaven\n- order date: Monday, 20 July 2026\n- membership level: Blue\n- order subtotal: 233.81 USD\n\nFine print from the bottom of the advertisement:\n* For Blue members and below.\n† Applies to Black level and higher members.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does Owen Mensah actually get on order ORD-641488 when the ad and its small print have been applied offer by offer?",
  "options": [
   "Both offers",
   "Only free gift wrapping",
   "Only free assembly",
   "Neither offer"
  ]
 },
 {
  "qid": "qfa2094e472",
  "kind": "yes/no",
  "text": "Support chat about order ORD-396158:\nAiko Brandt: Hi, I placed order ORD-396158 on May 16, 2026 for item SKU-47263, and the order subtotal was 193.47 USD.\nAgent: Thanks. The item is in the bedding product category, its price status is regular price, and it ships to the Calderon delivery region.\nAgent: Your membership level is Black.\nAiko Brandt: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\n\nCozy comfort begins with gentle warmth and a soft, calm feeling. Birchwood Linens helps your family rest easy and share happy smiles.\n*Covers the bedding product category only. The order subtotal must be above 200.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the ad and its small print, does Aiko Brandt get free shipping on order ORD-396158?"
 }
]
