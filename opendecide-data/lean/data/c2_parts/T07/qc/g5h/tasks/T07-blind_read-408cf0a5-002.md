# G5-H blind read T07-blind_read-408cf0a5-002 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T07/qc/g5h/answers/T07-blind_read-408cf0a5-002.json

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
  "qid": "qe457a99e31",
  "kind": "yes/no",
  "text": "Order ORD-464634 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-83782 |\n| product category | sports gear |\n| price status | refurbished |\n| delivery region | Brenmoor |\n| order date | May 12, 2026 |\n| membership level | Platinum |\n| order subtotal | 108.58 USD |\n\nAdvertisement from Kestrel Outfitters:\nWe match any lower price*\n\nSubject: Cosy, gentle and kid-friendly\nHello there, families, and welcome. Kestrel Outfitters is a happy place for little ones and grown-ups alike.\n\nFine print:\n* Placed before May 7, 2026 counts; that very day is excluded.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it the case that order ORD-464634 from Ines Duarte earns the price match under the advertised terms, headline and small print included?"
 },
 {
  "qid": "q66c275356c",
  "kind": "choice",
  "text": "Advertisement from Marigold Pets:\nFree installation for every appliance*\nA lifetime warranty on everything we sell†\n\nFine print:\n* Delivery that reaches Fallowmere puts the order outside the benefit. Products in the pet supplies category are excluded from this offer.\n† The headline benefit is set aside for anything in the toys category. Earlier orders are accepted, and so is the date May 14, 2026 itself.\n\nReady for a little wander along the cheerful aisles? Marigold Pets has a twinkle on the shelves.\n\nOrder ORD-543785 placed by Owen Mensah:\n- item: SKU-96477\n- product category: pet supplies\n- price status: pre-order\n- delivery region: Dunmere\n- order date: May 14, 2026\n- membership level: Black\n- order subtotal: $233.60",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to the lifetime warranty does order ORD-543785 from Owen Mensah miss, if any?",
  "options": [
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q05238f0295",
  "kind": "choice",
  "text": "Advertisement from Marigold Pets:\nWe match any lower price*\nFree gift wrapping at checkout†\n\nWelcome to Marigold Pets, a quiet space curated with patience and a love of rich, honest materials.\n\nFine print:\n† Items under the electronics category are carved out of this offer.\n* Products sitting in any category besides kitchenware fall outside this offer. For the offer, the order subtotal must be higher than 50.00 USD.\n\nOrder ORD-115805 placed by Hugo Lindqvist:\n- item: SKU-16373\n- product category: garden tools\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 25 February 2026\n- membership level: Green\n- order subtotal: 49.61 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nLooking at the ad, which condition attached to free gift wrapping does order ORD-115805 from Hugo Lindqvist miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The product-category condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q33f6012225",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nFine print:\n* Placed before 26 Apr 2026 counts; that very day is excluded. For membership levels up to Green and below.\n\n{\"title\": \"Welcome home to Kestrel Outfitters\", \"subtitle\": \"Cheerful pieces that suit young and old alike\", \"button\": \"Look around\"}\n\nOrder ORD-638728 placed by Felix Moreau:\n- item: SKU-20257\n- product category: toys\n- price status: open box\n- delivery region: Hollin\n- order date: 26 Apr 2026\n- membership level: Green\n- order subtotal: 104.01 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Kestrel Outfitters levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the order ORD-638728 from Felix Moreau against the advertised terms, is it true that it doesn't get the lifetime warranty?"
 },
 {
  "qid": "q9e9ce10832",
  "kind": "choice",
  "text": "Order ORD-257032 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-39568 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Brenmoor |\n| order date | 2026-03-16 |\n| membership level | Basic |\n| order subtotal | 25.00 USD |\n\nAdvertisement from Copperleaf Kitchen:\nWe match any lower price*\nFree installation for every appliance†\n\nFine print:\n* Orders delivered to Calderon are excluded.\n† Valid on orders of 25.00 USD or more.\n\nBrisk care is easy: a soft cloth, a dry spot, and a quick wipe. Cheers from Copperleaf Kitchen!",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-257032 placed by Ines Duarte, which headline offers does the advertisement and its fine print actually allow, offer by offer?",
  "options": [
   "Only free installation",
   "Only the price match",
   "Neither offer",
   "Both offers"
  ]
 },
 {
  "qid": "q1e30a99ec1",
  "kind": "choice",
  "text": "Advertisement from Cedarline Living:\nFree gift wrapping at checkout*\nFree assembly with every delivery†\n\nSubject: Tidy layout, simple search\nHello, the crisp design of Cedarline Living keeps the range in clear view and within easy grasp.\n\nOrder ORD-742589 placed by Jonah Pryce:\n- item: SKU-46951\n- product category: electronics\n- price status: regular price\n- delivery region: Greyhaven\n- order date: 4 Jul 2026\n- membership level: Blue\n- order subtotal: $199.65\n\nFine print from the bottom of the advertisement:\n* For Blue members and below.\n† Applies to Black level and higher members.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does Jonah Pryce actually get on order ORD-742589 when the ad and its small print have been applied offer by offer?",
  "options": [
   "Only free assembly",
   "Both offers",
   "Only free gift wrapping",
   "Neither offer"
  ]
 },
 {
  "qid": "qa0e443ad6f",
  "kind": "choice",
  "text": "Support chat about order ORD-784281:\nSelin Yilmaz: Hi, I placed order ORD-784281 on 3 October 2026 for item SKU-26299, and the order subtotal was $74.99.\nAgent: Thanks. The item is in the toys product category, its price status is open box, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Basic.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nFree returns on every purchase*\nWe match any lower price†\n\nWe are happy you chose Pebblestone Garden. Take a look at your basket, then head to payment.\n\nFine print:\n* Orders taken on 1 September 2026 and any day later count. Valid for orders whose subtotal is $25 or more.\n† Minimum order subtotal: $75.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the ad's small print attached to the price match does Selin Yilmaz's order ORD-784281 miss, if any?",
  "options": [
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "qccdafc7edf",
  "kind": "choice",
  "text": "Order ORD-235646 placed by Kofi Asante:\n| field | value |\n| --- | --- |\n| item | SKU-35468 |\n| product category | kitchenware |\n| price status | final sale |\n| delivery region | Calderon |\n| order date | Wednesday, February 25, 2026 |\n| membership level | Plus |\n| order subtotal | $86.72 |\n\nAdvertisement from Harborlight Goods:\nA lifetime warranty on everything we sell*\nFree assembly with every delivery†\n\nFine print:\n† Any delivery to Fallowmere is excluded from this offer. The order subtotal must be above $75.00.\n* Delivery that reaches Dunmere puts the order outside the benefit. Applies to members of the Basic level or lower.\n\nSerene surroundings and timeless craft at Harborlight Goods\nPure lines, gentle light and a graceful selection.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the small print attached to free assembly does order ORD-235646 from Kofi Asante miss, if any, given the advertisement and its fine print?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition",
   "The order-subtotal condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q5effb4acca",
  "kind": "choice",
  "text": "Support chat about order ORD-359618:\nAiko Brandt: Hi, I placed order ORD-359618 on Monday, March 9, 2026 for item SKU-75395, and the order subtotal was 111.87 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is regular price, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Plus.\nAiko Brandt: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree installation for every appliance*\nDouble reward points on every purchase†\n\nOakhurst Interiors is a little shop with a big heart, run by folks who love talking about what they sell.\n\nFine print:\n† Orders must reach 150.00 USD or more in subtotal.\n* For Plus members and above.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the small print offer by offer, which of the advertised terms does Aiko Brandt actually get on order ORD-359618?",
  "options": [
   "Both offers",
   "Only double reward points",
   "Only free installation",
   "Neither offer"
  ]
 },
 {
  "qid": "q2b9ede42cb",
  "kind": "choice",
  "text": "Advertisement from Tidewell Supply:\nWe match any lower price*\n\nSubject: a warm welcome to fresh air\nDear friend,\nWelcome to Tidewell Supply, where we love helping people step outside with confidence.\nOur team is glad to share sturdy essentials for your adventures ahead.\nWe appreciate you stopping by, and we hope your path feels bold and easy.\nWarm regards,\nThe friendly crew\n*Valid for orders placed from 25 March 2026 onward. Minimum order subtotal: $35.00.\n\nOrder ORD-532428 placed by Jonah Pryce:\n- item: SKU-71504\n- product category: toys\n- price status: regular price\n- delivery region: Hollin\n- order date: 22 April 2026\n- membership level: Premier\n- order subtotal: $34.99",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Tidewell Supply levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nAccording to what the advertisement says, which condition attached to the price match does order ORD-532428 from Jonah Pryce miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "qb3d32b1fe9",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nA lifetime warranty on everything we sell*\nFree gift wrapping at checkout†\n\nFine print:\n* Limited to members at the Premier level or lower.\n† Items at the open box pricing status sit outside this promotion.\n\nStop by Brightwell Home for the essentials you use at home.\n\nOrder ORD-164875 placed by Tomas Ferreira:\n- item: SKU-50460\n- product category: bedding\n- price status: pre-order\n- delivery region: Eskarth\n- order date: 27 August 2026\n- membership level: Premier\n- order subtotal: $82.07",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers from the ad and its small print does order ORD-164875 placed by Tomas Ferreira actually get, offer by offer?",
  "options": [
   "Only the lifetime warranty",
   "Both offers",
   "Only free gift wrapping",
   "Neither offer"
  ]
 },
 {
  "qid": "q7e3b6fc959",
  "kind": "yes/no",
  "text": "Advertisement from Brightwell Home:\nDouble reward points on every purchase*\nFree assembly with every delivery†\n\nFun ideas and cheerful colour burst from the displays at Brightwell Home, so bounce on in.\n\nFine print:\n* For Plus members and above. Stock with pre-order status is excluded from this benefit.\n† An order qualifies with a subtotal of $200.00 or more. Placed before 11 July 2026 counts; that very day is excluded.\n\nOrder ORD-660385 placed by Clara Voss:\n- item: SKU-91950\n- product category: pet supplies\n- price status: pre-order\n- delivery region: Greyhaven\n- order date: 10 July 2026\n- membership level: Premier\n- order subtotal: $220.43",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-660385 from Clara Voss, does it fail to receive double reward points under the advertised terms, as the ad and its small print describe?"
 },
 {
  "qid": "q155e825234",
  "kind": "yes/no",
  "text": "Order ORD-278605 placed by Kofi Asante:\n| field | value |\n| --- | --- |\n| item | SKU-51207 |\n| product category | sports gear |\n| price status | regular price |\n| delivery region | Arvale |\n| order date | 7 September 2026 |\n| membership level | Silver |\n| order subtotal | $77.15 |\n\nAdvertisement from Bluecrest Sports:\nDouble reward points on every purchase*\n\nBluecrest Sports focuses on practical comfort for busy homes. Browse our range, read the descriptions, and pick what fits your routine. We are happy to answer your questions.\n*Valid for orders placed on or after 17 August 2026. Delivery to Arvale only.\n\nNote added by the customer: Kofi Asante recalls a worker on the helpline clearly saying the deal would cover this order, and that is what counts.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-278605 from Kofi Asante fail to receive double reward points under the advertised terms, judging by what the advertisement says?"
 },
 {
  "qid": "qfb845afcd9",
  "kind": "yes/no",
  "text": "Advertisement from Cedarline Living:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nFine print:\n* Customers at the Blue tier or lower can use this offer. Subtotal must be strictly above 35.00 USD.\n† Only members at the Blue level or higher may take part.\n\nCome on in, have a look around and meet the people behind the counter at Cedarline Living.\n\nOrder ORD-459766 placed by Hugo Lindqvist:\n| field | value |\n| --- | --- |\n| item | SKU-95262 |\n| product category | bedding |\n| price status | pre-order |\n| delivery region | Eskarth |\n| order date | 14 Jul 2026 |\n| membership level | Blue |\n| order subtotal | 35.00 USD |",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes Hugo Lindqvist get free gift wrapping on order ORD-459766 when the advertised terms, with the headline and its small print, are applied?"
 },
 {
  "qid": "qdaf8cd21ca",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nFine print:\n* Placed before 26 Apr 2026 counts; that very day is excluded. For membership levels up to Green and below.\n\n{\"title\": \"Welcome home to Kestrel Outfitters\", \"subtitle\": \"Cheerful pieces that suit young and old alike\", \"button\": \"Look around\"}\n\nOrder ORD-638728 placed by Felix Moreau:\n- item: SKU-20257\n- product category: toys\n- price status: open box\n- delivery region: Hollin\n- order date: 22 Mar 2026\n- membership level: Green\n- order subtotal: 104.01 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Kestrel Outfitters levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the order ORD-638728 from Felix Moreau against the advertised terms, is it true that it doesn't get the lifetime warranty?"
 },
 {
  "qid": "q23b8262ca7",
  "kind": "choice",
  "text": "Support chat about order ORD-967569:\nDana Okafor: Hi, I placed order ORD-967569 on May 23, 2026 for item SKU-82565, and the order subtotal was 174.72 USD.\nAgent: Thanks. The item is in the electronics product category, its price status is refurbished, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Bronze.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree returns on every purchase*\n\nSubject: a little hello from your local play corner\nHello neighbour,\nCedarline Living is happy to see familiar faces at the counter. We love swapping play ideas and chatting about what kids are curious about. Pop in and say hi. We are delighted to meet you.\n*Items whose status is refurbished are excluded.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, which condition attached to free returns does order ORD-967569 from Dana Okafor miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition"
  ]
 },
 {
  "qid": "qea9e804ed7",
  "kind": "yes/no",
  "text": "Order ORD-541443 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-11529 |\n| product category | electronics |\n| price status | regular price |\n| delivery region | Brenmoor |\n| order date | August 28, 2026 |\n| membership level | Platinum |\n| order subtotal | 221.44 USD |\n\nAdvertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\n\n{\"title\": \"Your shopping, made simple at Juniper Gadgets\", \"subtitle\": \"Sort by aisle, keep a favourites list, and pay with ease\", \"button\": \"Let's get going\"}\n\nFine print:\n* Only members at the Gold level or higher may take part. Any product that belongs to the sports gear category is excluded from the offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-541443 placed by Jonah Pryce doesn't get free gift wrapping under the advertised terms, based on the advertisement and its fine print?"
 },
 {
  "qid": "qfc957eaedd",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree returns on every purchase*\nFree installation for every appliance†\n\nFine print:\n* Excludes delivery to Arvale.\n† Items marked with the refurbished status fall outside the benefit set out here. Any order placed on Friday, 21 August 2026 and beyond is accepted.\n\nOur shelves are bursting with ideas, and the team at Bluecrest Sports is grinning ear to ear.\n\nOrder ORD-306988 placed by Nadia Haddad:\n- item: SKU-90534\n- product category: electronics\n- price status: final sale\n- delivery region: Arvale\n- order date: Thursday, 20 August 2026\n- membership level: Blue\n- order subtotal: 38.56 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-306988 from Nadia Haddad, which headline offers hold up under the ad and its small print, offer by offer?",
  "options": [
   "Both offers",
   "Only free returns",
   "Only free installation",
   "Neither offer"
  ]
 },
 {
  "qid": "q45c2d4c319",
  "kind": "choice",
  "text": "Order ORD-673595 placed by Lena Whitcombe:\n| field | value |\n| --- | --- |\n| item | SKU-37954 |\n| product category | pet supplies |\n| price status | open box |\n| delivery region | Eskarth |\n| order date | 2026-04-10 |\n| membership level | Elite |\n| order subtotal | $150.01 |\n\nAdvertisement from Fernway Market:\nFree returns on every purchase*\nFree assembly with every delivery†\n\nFine print:\n† Orders headed for delivery in Eskarth are kept out of this offer. Earlier orders are accepted, and so is the date 2026-04-23 itself.\n* Order subtotal must go beyond $150.00.\n\nA cosy trip for the children and a relaxed stroll for you, right here at Fernway Market.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIf any, which condition in the advertisement and its fine print attached to free assembly does order ORD-673595 from Lena Whitcombe miss?",
  "options": [
   "The order-date condition",
   "The order-subtotal condition",
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q26e63da73b",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree assembly with every delivery*\n\nSubject: Hello, friend\nDear friend, we are truly glad you came by, and Wrenfield Outdoor is eager to make you feel at home.\n\nFine print:\n* Minimum order subtotal: $50. Any item whose status is pre-order falls outside this offer.\n\nOrder ORD-299762 placed by Felix Moreau:\n- item: SKU-19530\n- product category: bedding\n- price status: refurbished\n- delivery region: Calderon\n- order date: Thursday, May 7, 2026\n- membership level: Platinum\n- order subtotal: 53.21 USD\n\nNote added by the customer: Felix Moreau says a headline that large was clearly designed to cover all sorts of orders, and this order is simply part of that.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms and what the advertisement says, does order ORD-299762 from Felix Moreau lose out on free assembly?"
 },
 {
  "qid": "q7dd61eb761",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\nFree returns on every purchase†\n\nFine print:\n† Minimum order subtotal: $150.\n* Eligibility is limited to the sports gear category. Valid for orders placed on or before 26 Jun 2026.\n\nWe are so glad you came into Juniper Gadgets. Please take a warm look at your basket and keep going.\n\nOrder ORD-778011 placed by Mira Castell:\n| field | value |\n| --- | --- |\n| item | SKU-80028 |\n| product category | sports gear |\n| price status | regular price |\n| delivery region | Brenmoor |\n| order date | 22 May 2026 |\n| membership level | Black |\n| order subtotal | 113.44 USD |",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGiven the advertisement and its fine print, will order ORD-778011 from Mira Castell lose out on free gift wrapping?"
 },
 {
  "qid": "q8622ff8559",
  "kind": "yes/no",
  "text": "Advertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\n\nSubject: practical ideas that make sense\nDear friend,\nThanks for reading. Copperleaf Kitchen focuses on useful things that are easy to use. Take a look at our sensible ideas for your home and your routine. We are happy to help.\nSincerely, the team\n*Delivery to Hollin only.\n\nOrder ORD-842591 placed by Felix Moreau:\n- item: SKU-88152\n- product category: kitchenware\n- price status: regular price\n- delivery region: Hollin\n- order date: Tuesday, September 22, 2026\n- membership level: Gold\n- order subtotal: $137.93",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it the case that order ORD-842591 from Felix Moreau earns double reward points under the advertised terms, headline and small print included?"
 },
 {
  "qid": "qfe2c1a9c38",
  "kind": "yes/no",
  "text": "Support chat about order ORD-102174:\nHugo Lindqvist: Hi, I placed order ORD-102174 on Saturday, 1 August 2026 for item SKU-60994, and the order subtotal was $34.99.\nAgent: Thanks. The item is in the bedding product category, its price status is open box, and it ships to the Arvale delivery region.\nAgent: Your membership level is Premier.\nHugo Lindqvist: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nA lifetime warranty on everything we sell*\nDouble reward points on every purchase†\n\nA calm glance at your basket keeps things simple, so carry on at Oakhurst Interiors.\n\nFine print:\n† The subtotal of the order needs to be $35 or higher. Only the bedding category earns the headline benefit.\n* Order subtotal exceeds $25.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Oakhurst Interiors levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nHas Hugo Lindqvist lost out on the lifetime warranty with order ORD-102174, judging by the advertisement and its fine print?"
 },
 {
  "qid": "qf0839b49ae",
  "kind": "choice",
  "text": "Support chat about order ORD-816501:\nPriya Raman: Hi, I placed order ORD-816501 on 2026-04-16 for item SKU-64186, and the order subtotal was 133.77 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is clearance, and it ships to the Arvale delivery region.\nAgent: Your membership level is Silver.\nPriya Raman: I am asking about the advertisement below.\n\nAdvertisement from Marigold Pets:\nWe match any lower price*\nDouble reward points on every purchase†\n\nYour basket is ready for a speedy finish at Marigold Pets. Take a moment to scan your items.\n\nFine print:\n* Order by 2026-05-07 at the latest.\n† Membership tier Bronze or lower applies.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the ad and its small print offer by offer, which headline offers does order ORD-816501 from Priya Raman actually get?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only double reward points",
   "Only the price match"
  ]
 },
 {
  "qid": "q31770ef8a6",
  "kind": "yes/no",
  "text": "Support chat about order ORD-545947:\nClara Voss: Hi, I placed order ORD-545947 on 10 Jul 2026 for item SKU-75314, and the order subtotal was 35.00 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is pre-order, and it ships to the Hollin delivery region.\nAgent: Your membership level is Premier.\nClara Voss: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nWe match any lower price*\n\nHello from Oakhurst Interiors! Come explore our new arrivals and find your favorite pick.\n*Minimum order subtotal: 35.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad, with its small print taken into account, mean that Clara Voss earns the price match on order ORD-545947?"
 },
 {
  "qid": "q55262b5457",
  "kind": "choice",
  "text": "Order ORD-875414 placed by Owen Mensah:\n| field | value |\n| --- | --- |\n| item | SKU-29704 |\n| product category | toys |\n| price status | regular price |\n| delivery region | Fallowmere |\n| order date | 9 Apr 2026 |\n| membership level | Black |\n| order subtotal | $210.56 |\n\nAdvertisement from Tidewell Supply:\nFree gift wrapping at checkout*\n\nA calm, careful approach suits this piece beautifully. We hope its quiet elegance accompanies you, and thank you for choosing Tidewell Supply.\n\nFine print:\n* Members whose level is at least Black can redeem it. Placed before 24 Apr 2026 counts; that very day is excluded.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Tidewell Supply levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich ad condition attached to free gift wrapping does order ORD-875414 from Owen Mensah miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition",
   "The order-date condition"
  ]
 },
 {
  "qid": "qa6cb87c604",
  "kind": "choice",
  "text": "Order ORD-925478 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-30297 |\n| product category | garden tools |\n| price status | refurbished |\n| delivery region | Fallowmere |\n| order date | Saturday, June 6, 2026 |\n| membership level | Elite |\n| order subtotal | $168.84 |\n\nAdvertisement from Harborlight Goods:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nSubject: Fast, fresh, and built for the modern pace\nHi, Harborlight Goods is a sleek hub for quick decisions and clean lines.\n\nFine print:\n* Shoppers may place orders on Tuesday, May 5, 2026 itself and on every day before it.\n† Items priced as final sale are excluded. For the offer, the order subtotal must be higher than $150.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Harborlight Goods levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe advertisement and its fine print attach conditions to the price match; which, if any, does order ORD-925478 from Ines Duarte miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition",
   "The price-status condition",
   "The order-date condition"
  ]
 },
 {
  "qid": "qbd84c51ea5",
  "kind": "yes/no",
  "text": "Advertisement from Northvale Audio:\nFree shipping on every order*\n\nThank you for bringing this lovely item into your family at Northvale Audio. Please read the care tips and place this note with the product.\n\nFine print:\n* Minimum order subtotal: $150. Eligibility is limited to members at Plus level or lower.\n\nOrder ORD-702676 placed by Ravi Anand:\n- item: SKU-31251\n- product category: garden tools\n- price status: regular price\n- delivery region: Fallowmere\n- order date: 2 October 2026\n- membership level: Premier\n- order subtotal: $168.49",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, is it true that the order ORD-702676 from Ravi Anand doesn't get free shipping under the advertised terms?"
 },
 {
  "qid": "q1383e6b355",
  "kind": "yes/no",
  "text": "Support chat about order ORD-435043:\nRavi Anand: Hi, I placed order ORD-435043 on 21 September 2026 for item SKU-45651, and the order subtotal was 27.37 USD.\nAgent: Thanks. The item is in the kitchenware product category, its price status is final sale, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Black.\nRavi Anand: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nScroll, compare and pick out a design you adore at Birchwood Linens.\n\nFine print:\n† Items that hold the final sale status are excluded from the main benefit. Orders submitted on or before 21 September 2026 are accepted.\n* Qualifying orders include the date 23 October 2026 and every later day. Qualifying orders: subtotal $35 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it the case that order ORD-435043 from Ravi Anand earns free gift wrapping under the advertised terms, headline and small print included?"
 },
 {
  "qid": "q95ce25752a",
  "kind": "choice",
  "text": "Advertisement from Larkspur Playthings:\nWe match any lower price*\nFree returns on every purchase†\n\nLittle hands and big smiles are welcome at Larkspur Playthings. Head out together and enjoy a pleasant stroll among the displays.\n\nFine print:\n* Minimum order subtotal: $35.00. Goods filed under a different category from bedding fall outside the benefit.\n† The subtotal on the order has to be more than $100.00 to count. Items whose status is clearance sit outside this offer.\n\nOrder ORD-245672 placed by Hugo Lindqvist:\n- item: SKU-84607\n- product category: bedding\n- price status: final sale\n- delivery region: Greyhaven\n- order date: May 16, 2026\n- membership level: Basic\n- order subtotal: $27.63",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, drawn from the ad and its small print attached to the price match, does order ORD-245672 from Hugo Lindqvist miss, if any?",
  "options": [
   "The product-category condition",
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q47b1579d4b",
  "kind": "yes/no",
  "text": "Advertisement from Harborlight Goods:\nA lifetime warranty on everything we sell*\n\nSubject: Quietly elegant style from Harborlight Goods\nHello there,\nOur newest pieces have a graceful feel and a modern look.\n\nFine print:\n* The order date needs to be on or before 2026-11-25.\n\nOrder ORD-301509 placed by Felix Moreau:\n- item: SKU-28882\n- product category: furniture\n- price status: regular price\n- delivery region: Dunmere\n- order date: 2026-10-28\n- membership level: Silver\n- order subtotal: $208.77",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, does order ORD-301509 from Felix Moreau get the lifetime warranty under its headline and that headline's small print?"
 },
 {
  "qid": "qfbd35eddc1",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree assembly with every delivery*\n\nGather your crew, because Marigold Pets is set for a wild and wonderful stretch of trails.\n*For Blue members and above. Excludes delivery to Fallowmere.\n\nOrder ORD-495834 placed by Clara Voss:\n- item: SKU-87494\n- product category: pet supplies\n- price status: final sale\n- delivery region: Eskarth\n- order date: July 22, 2026\n- membership level: Black\n- order subtotal: $35.76",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Marigold Pets levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder what the advertisement says, headline and small print included, does Clara Voss get free assembly on order ORD-495834?"
 },
 {
  "qid": "qf885d21b46",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nFree installation for every appliance*\n\nFine print:\n* Orders must be placed on or after Friday, March 6, 2026. Delivery that reaches Calderon puts the order outside the benefit.\n\nHop along to Kestrel Outfitters and see what's bouncing around the shelves!\n\nOrder ORD-783504 placed by Tomas Ferreira:\n- item: SKU-12908\n- product category: pet supplies\n- price status: regular price\n- delivery region: Hollin\n- order date: Thursday, March 26, 2026\n- membership level: Blue\n- order subtotal: $121.26",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nHaving read the ad's headline and the small print that goes with it, does order ORD-783504 from Tomas Ferreira receive free installation?"
 },
 {
  "qid": "q1482fb0795",
  "kind": "yes/no",
  "text": "Support chat about order ORD-595591:\nTomas Ferreira: Hi, I placed order ORD-595591 on Friday, 24 April 2026 for item SKU-66898, and the order subtotal was $51.80.\nAgent: Thanks. The item is in the kitchenware product category, its price status is pre-order, and it ships to the Arvale delivery region.\nAgent: Your membership level is Premier.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nFree installation for every appliance*\n\nCrafted to endure\nWe are proud to present Pebblestone Garden, a house of considered design and enduring materials.\n\nFine print:\n* Customers must spend at least $50 on the order subtotal. Orders dated on or before Wednesday, 27 May 2026 count.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes what the advertisement says, with that headline's small print counted, mean that order ORD-595591 from Tomas Ferreira earns free installation?"
 },
 {
  "qid": "q792ac67e3b",
  "kind": "choice",
  "text": "Support chat about order ORD-219460:\nJonah Pryce: Hi, I placed order ORD-219460 on 26 October 2026 for item SKU-89695, and the order subtotal was $175.34.\nAgent: Thanks. The item is in the sports gear product category, its price status is pre-order, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Elite.\nJonah Pryce: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nDouble reward points on every purchase*\n\nSubject: a little hello from your local play corner\nHello neighbour,\nOakhurst Interiors is happy to see familiar faces at the counter. We love swapping play ideas and chatting about what kids are curious about. Pop in and say hi. We are delighted to meet you.\n*Items whose status is final sale are excluded.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Oakhurst Interiors levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-219460 from Jonah Pryce against the advertised terms, which condition in the small print attached to double reward points does it miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition"
  ]
 },
 {
  "qid": "q5669d3c90f",
  "kind": "choice",
  "text": "Support chat about order ORD-682893:\nMira Castell: Hi, I placed order ORD-682893 on 7 Jun 2026 for item SKU-11993, and the order subtotal was $132.98.\nAgent: Thanks. The item is in the furniture product category, its price status is regular price, and it ships to the Hollin delivery region.\nAgent: Your membership level is Silver.\nMira Castell: I am asking about the advertisement below.\n\nAdvertisement from Marigold Pets:\nDouble reward points on every purchase*\nA lifetime warranty on everything we sell†\n\nVisit Marigold Pets and discover pieces built with care, backed by a team that loves to help.\n\nFine print:\n* Membership tier Silver or lower applies.\n† Orders placed by 14 Jun 2026 are valid, and the stated day is included.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich ad condition attached to double reward points does order ORD-682893 from Mira Castell miss, if any?",
  "options": [
   "The membership-level condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qf03c3e36bc",
  "kind": "yes/no",
  "text": "Support chat about order ORD-291213:\nLena Whitcombe: Hi, I placed order ORD-291213 on 8 Apr 2026 for item SKU-54138, and the order subtotal was 68.57 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Silver.\nLena Whitcombe: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\n\nRefined essentials\nJuniper Gadgets brings calm, well-made pieces right to your screen.\n\nFine print:\n* Only members at the Gold level or higher may take part. Any product that belongs to the sports gear category is excluded from the offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-291213 placed by Lena Whitcombe doesn't get free gift wrapping under the advertised terms, based on the advertisement and its fine print?"
 },
 {
  "qid": "qeffcc709e1",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree returns on every purchase*\nFree installation for every appliance†\n\nFine print:\n* Excludes delivery to Eskarth.\n† Items marked with the final sale status fall outside the benefit set out here. Any order placed on 2026-06-21 and beyond is accepted.\n\nOur shelves are bursting with ideas, and the team at Bluecrest Sports is grinning ear to ear.\n\nOrder ORD-474047 placed by Jonah Pryce:\n- item: SKU-23883\n- product category: bedding\n- price status: refurbished\n- delivery region: Eskarth\n- order date: 2026-06-21\n- membership level: Blue\n- order subtotal: 208.94 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-474047 from Jonah Pryce, which headline offers hold up under the ad and its small print, offer by offer?",
  "options": [
   "Only free installation",
   "Both offers",
   "Only free returns",
   "Neither offer"
  ]
 },
 {
  "qid": "q8b082fe2e4",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree returns on every purchase*\n\nFine print:\n* Every delivery bound for Calderon lies outside the headline offer.\n\nHello from the team at Bluecrest Sports! Pop it on a shelf where it gets to enjoy the view and a little sunshine.\n\nOrder ORD-612882 placed by Lena Whitcombe:\n- item: SKU-30954\n- product category: electronics\n- price status: regular price\n- delivery region: Eskarth\n- order date: 9 Jul 2026\n- membership level: Green\n- order subtotal: $134.20",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking into account what the advertisement says, which condition attached to free returns does customer Lena Whitcombe on order ORD-612882 miss, if any?",
  "options": [
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q82fa22cf3c",
  "kind": "yes/no",
  "text": "Support chat about order ORD-645088:\nSelin Yilmaz: Hi, I placed order ORD-645088 on 2026-08-03 for item SKU-59011, and the order subtotal was $64.46.\nAgent: Thanks. The item is in the electronics product category, its price status is regular price, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Plus.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nFree returns on every purchase*\n\nSubject: A gentle welcome to you\nHello,\nWrenfield Outdoor is delighted to share a warm welcome with you. We hope your home feels cozy and calm. Thanks for being part of our community, and we are glad you stopped by.\n*Excludes delivery to Dunmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking the advertisement and its fine print into account, has order ORD-645088 from Selin Yilmaz lost out on free returns?"
 },
 {
  "qid": "q53f6858cf7",
  "kind": "choice",
  "text": "Order ORD-320348 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-15650 |\n| product category | bedding |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | May 19, 2026 |\n| membership level | Gold |\n| order subtotal | 22.52 USD |\n\nAdvertisement from Kestrel Outfitters:\nFree installation for every appliance*\nFree shipping on every order†\n\nFine print:\n* Every delivery bound for Hollin lies outside the headline offer. Valid on orders of $25 or more.\n† Delivery to Brenmoor only.\n\nStep right in\nBrisk service, modern style and a lively edge make Kestrel Outfitters worth a visit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does order ORD-320348 from Tomas Ferreira actually get when the advertisement and its fine print are applied offer by offer?",
  "options": [
   "Neither offer",
   "Only free installation",
   "Both offers",
   "Only free shipping"
  ]
 },
 {
  "qid": "q2bfe69ccbb",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree returns on every purchase*\nFree shipping on every order†\n\nFine print:\n† Items priced as pre-order are excluded. Excludes the bedding category.\n* Items priced as clearance are excluded. Eligibility for the benefit is restricted to the pet supplies product category.\n\nLittle ones and grown-ups alike are welcome at Marigold Pets, so bring the crew along.\n\nOrder ORD-506670 placed by Tomas Ferreira:\n- item: SKU-27526\n- product category: pet supplies\n- price status: open box\n- delivery region: Calderon\n- order date: 6 Oct 2026\n- membership level: Green\n- order subtotal: 119.92 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertised terms, which include the headline and its small print, does Tomas Ferreira come with free returns on order ORD-506670?"
 },
 {
  "qid": "qb4192842b2",
  "kind": "choice",
  "text": "Order ORD-272630 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-29172 |\n| product category | furniture |\n| price status | final sale |\n| delivery region | Calderon |\n| order date | 4 April 2026 |\n| membership level | Black |\n| order subtotal | $35 |\n\nAdvertisement from Larkspur Playthings:\nWe match any lower price*\nDouble reward points on every purchase†\n\nWelcome to our pages\nThe people at Larkspur Playthings have gathered thoughtful pieces that feel right at home.\n\nFine print:\n† Members ranked Black and above are the only ones covered.\n* Headline benefit is confined to delivery landing in Arvale. Customers must spend at least $35 on the order subtotal.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nLooking at the ad, which condition attached to the price match does order ORD-272630 from Ravi Anand miss, if any?",
  "options": [
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q05596d4dfd",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nFree gift wrapping at checkout*\n\nWe appreciate your visit to Fernway Market. Please glance at the items in your basket and carry on at your own pace.\n\nFine print:\n* Valid only for orders delivered to Brenmoor.\n\nOrder ORD-737408 placed by Selin Yilmaz:\n- item: SKU-56493\n- product category: furniture\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 2026-04-11\n- membership level: Bronze\n- order subtotal: 99.35 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-737408 from Selin Yilmaz against the advertised terms, which condition in the small print attached to free gift wrapping does it miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qb79b664c51",
  "kind": "choice",
  "text": "Advertisement from Larkspur Playthings:\nFree assembly with every delivery*\nFree gift wrapping at checkout†\n\nThank you for placing your order with Larkspur Playthings. Take a considered look at your basket and continue with confidence.\n\nFine print:\n† Shoppers get the headline benefit solely for delivery in Arvale.\n* Products assigned to the garden tools category are excluded.\n\nOrder ORD-253371 placed by Jonah Pryce:\n- item: SKU-84628\n- product category: kitchenware\n- price status: open box\n- delivery region: Arvale\n- order date: 2026-04-16\n- membership level: Premier\n- order subtotal: $159.97",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Larkspur Playthings levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecked offer by offer against the ad and its small print, which headline offers does Jonah Pryce actually get with order ORD-253371?",
  "options": [
   "Only free assembly",
   "Only free gift wrapping",
   "Both offers",
   "Neither offer"
  ]
 },
 {
  "qid": "q2aabfbeaa1",
  "kind": "choice",
  "text": "Order ORD-261166 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-42525 |\n| product category | sports gear |\n| price status | clearance |\n| delivery region | Calderon |\n| order date | Thursday, 28 May 2026 |\n| membership level | Gold |\n| order subtotal | $51.29 |\n\nAdvertisement from Bluecrest Sports:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nFine print:\n† Applies to orders placed ahead of Friday, 29 May 2026.\n* Goods in the sports gear category fall outside the headline benefit. Valid only for orders delivered to Calderon.\n\nWelcome home! Give it a gentle wipe with a soft cloth, and thank you for trusting Bluecrest Sports with your choice.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-261166 from Clara Voss and reading what the advertisement says, which condition in the small print attached to free shipping does it miss, if any?",
  "options": [
   "The product-category condition",
   "The order-date condition",
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q63dced218a",
  "kind": "choice",
  "text": "Advertisement from Copperleaf Kitchen:\nFree assembly with every delivery*\n\nFine print:\n* Members ranked Platinum and above are the only ones covered. Orders headed for delivery in Brenmoor are kept out of this offer.\n\nSubject: Quiet confidence\nHi, simple beauty and thoughtful craft are what shape Copperleaf Kitchen, from the front window to the far end.\n\nOrder ORD-212661 placed by Aiko Brandt:\n- item: SKU-34915\n- product category: sports gear\n- price status: pre-order\n- delivery region: Brenmoor\n- order date: Monday, 13 April 2026\n- membership level: Platinum\n- order subtotal: 20.39 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, which condition attached to free assembly does order ORD-212661 from Aiko Brandt miss, if any?",
  "options": [
   "The delivery-region condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qbe3a86f6d3",
  "kind": "choice",
  "text": "Order ORD-379757 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-82175 |\n| product category | furniture |\n| price status | open box |\n| delivery region | Arvale |\n| order date | July 23, 2026 |\n| membership level | Plus |\n| order subtotal | 145.35 USD |\n\nAdvertisement from Copperleaf Kitchen:\nFree installation for every appliance*\nFree assembly with every delivery†\n\nMake a move\nOur modern shapes and sharp colours are ready for a fresh look at Copperleaf Kitchen.\n\nFine print:\n* Every item in the furniture category falls outside the offer.\n† Qualifying orders: subtotal 200.00 USD or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIf any, which condition in the advertisement and its fine print attached to free installation does order ORD-379757 from Tomas Ferreira miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition",
   "The product-category condition"
  ]
 },
 {
  "qid": "q7f492476bf",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree returns on every purchase*\n\nFine print:\n* Items in the kitchenware product category are excluded.\n\nStep in, look around, and see what Juniper Gadgets has built for modern living.\n\nOrder ORD-541118 placed by Nadia Haddad:\n- item: SKU-34813\n- product category: electronics\n- price status: regular price\n- delivery region: Arvale\n- order date: Wednesday, 21 October 2026\n- membership level: Blue\n- order subtotal: 40.38 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, does Nadia Haddad earn free returns with order ORD-541118?"
 },
 {
  "qid": "q8ffc36fa66",
  "kind": "yes/no",
  "text": "Advertisement from Cedarline Living:\nA lifetime warranty on everything we sell*\n\nFine print:\n* Subtotal of $100.00 or more required.\n\nQuick look, clear choice\nStep up to Cedarline Living and scan a sharp, edited range built to make choosing simple.\n\nOrder ORD-892184 placed by Priya Raman:\n- item: SKU-77589\n- product category: pet supplies\n- price status: regular price\n- delivery region: Fallowmere\n- order date: 2026-08-08\n- membership level: Blue\n- order subtotal: $78.77",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nRead with its small print, does the ad show that order ORD-892184 from Priya Raman earns the lifetime warranty?"
 }
]
