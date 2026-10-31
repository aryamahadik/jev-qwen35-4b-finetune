# G5-H blind read T07-blind_read-c09a4e11-000 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T07/topup_a55/root/T07/qc/g5h/answers/T07-blind_read-c09a4e11-000.json

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
  "qid": "q7cfdbd394f",
  "kind": "yes/no",
  "text": "Support chat about order ORD-640330:\nNadia Haddad: Hi, I placed order ORD-640330 on Thursday, 24 September 2026 for item SKU-86417, and the order subtotal was $125.05.\nAgent: Thanks. The item is in the garden tools product category, its price status is regular price, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Green.\nNadia Haddad: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree gift wrapping at checkout†\n\nWipe it with a damp cloth and let it air-dry. Thanks for buying from Larkspur Playthings.\n\nFine print:\n† Valid for orders whose subtotal is $25.00 or more.\n* Order by Thursday, 24 September 2026 at the latest. An order qualifies with a subtotal of $100.00 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-640330 from Nadia Haddad get double reward points?"
 },
 {
  "qid": "q517f85012f",
  "kind": "choice",
  "text": "Support chat about order ORD-305472:\nSelin Yilmaz: Hi, I placed order ORD-305472 on Sunday, 10 May 2026 for item SKU-25674, and the order subtotal was $145.14.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Premier.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nWe match any lower price*\nA lifetime warranty on everything we sell†\n\nSubject: A hop, skip and a browse\nHello hello, Oakhurst Interiors is skipping around the shelves with cheerful little curios.\n\nFine print:\n* Members ranked Elite and above are the only ones covered. Order by Wednesday, 3 June 2026 at the latest.\n† Headline benefit applies to orders with delivery in Dunmere only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms, which condition attached to the price match does order ORD-305472 from Selin Yilmaz miss, if any?",
  "options": [
   "The membership-level condition",
   "The order-date condition",
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q4a4dbe2952",
  "kind": "yes/no",
  "text": "Advertisement from Bluecrest Sports:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Any order placed on February 12, 2026 and beyond is accepted. Items at the refurbished pricing status sit outside this promotion.\n† Each item bearing the refurbished status is withheld from the main benefit.\n\nTalk to people who care\nStop by Bluecrest Sports for a warm word and a bit of helpful advice from a close-knit team that is happy to help.\n\nOrder ORD-392107 placed by Priya Raman:\n| field | value |\n| --- | --- |\n| item | SKU-91271 |\n| product category | garden tools |\n| price status | refurbished |\n| delivery region | Fallowmere |\n| order date | March 17, 2026 |\n| membership level | Green |\n| order subtotal | $18.40 |",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Bluecrest Sports levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad and its small print say that order ORD-392107 from Priya Raman gets double reward points?"
 },
 {
  "qid": "qc5cf6b9fc6",
  "kind": "yes/no",
  "text": "Order ORD-458829 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-76429 |\n| product category | furniture |\n| price status | final sale |\n| delivery region | Arvale |\n| order date | 12 July 2026 |\n| membership level | Black |\n| order subtotal | $207.01 |\n\nAdvertisement from Tidewell Supply:\nA lifetime warranty on everything we sell*\nFree shipping on every order†\n\nSubject: Elevated living, simply expressed\nDear friend, Tidewell Supply brings sophisticated taste to the home, with pieces that hold their own.\n\nFine print:\n* Delivery to Arvale sits outside the headline benefit. Valid for orders placed before 7 July 2026.\n† Only the kitchenware category earns the headline benefit. Orders headed for delivery in Dunmere are kept out of this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhen the headline and its small print are read against the advertised terms, does order ORD-458829 from Aiko Brandt receive free shipping?"
 },
 {
  "qid": "q9f29db483c",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nWander around Tidewell Supply at your own pace and see what makes us giggle.\n\nOrder ORD-354384 placed by Ines Duarte:\n- item: SKU-89814\n- product category: bedding\n- price status: pre-order\n- delivery region: Calderon\n- order date: July 9, 2026\n- membership level: Premier\n- order subtotal: $184.68\n\nFine print from the bottom of the advertisement:\n* Items in the bedding product category are excluded. For members at Premier or lower.\n† Items under the sports gear category are carved out of this offer. Any item whose status is pre-order falls outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-354384 placed by Ines Duarte lose out on the price match?"
 },
 {
  "qid": "q87cb66ee83",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nWander around Tidewell Supply at your own pace and see what makes us giggle.\n\nOrder ORD-354384 placed by Ines Duarte:\n- item: SKU-89814\n- product category: bedding\n- price status: pre-order\n- delivery region: Calderon\n- order date: July 9, 2026\n- membership level: Premier\n- order subtotal: $184.68\n\nFine print from the bottom of the advertisement:\n* Items in the bedding product category are excluded. For members at Premier or lower.\n† Items under the sports gear category are carved out of this offer. Any item whose status is pre-order falls outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDo the advertised terms, taking in the headline and small print, let Ines Duarte get the price match on order ORD-354384?"
 },
 {
  "qid": "q1a36a63e4b",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nFree gift wrapping at checkout*\nA lifetime warranty on everything we sell†\n\n{\"title\": \"Northvale Audio app\", \"subtitle\": \"Browse the range, build a list, and check out quickly\", \"button\": \"Get started\"}\n\nFine print:\n* The benefit is withheld from anything with final sale pricing.\n† The benefit is reserved for delivery bound for Calderon.\n\nOrder ORD-477604 placed by Aiko Brandt:\n- item: SKU-88925\n- product category: kitchenware\n- price status: open box\n- delivery region: Hollin\n- order date: 2026-09-17\n- membership level: Premier\n- order subtotal: 225.37 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking Aiko Brandt's order ORD-477604 against the ad and its small print, which condition attached to the lifetime warranty does it miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q5f8b1f6aa8",
  "kind": "yes/no",
  "text": "Order ORD-882679 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-70025 |\n| product category | bedding |\n| price status | refurbished |\n| delivery region | Greyhaven |\n| order date | 2026-10-17 |\n| membership level | Silver |\n| order subtotal | $129.20 |\n\nAdvertisement from Bluecrest Sports:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nFine print:\n* Valid: any order taken on or before 2026-10-16.\n† Valid for orders placed from 2026-10-17 onward. Reserved for members at Gold or below.\n\nCrafted to endure\nWe are proud to present Bluecrest Sports, a house of considered design and enduring materials.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does order ORD-882679 from Aiko Brandt lose out on free gift wrapping?"
 },
 {
  "qid": "q10c66ce8ed",
  "kind": "choice",
  "text": "Advertisement from Pebblestone Garden:\nFree assembly with every delivery*\n\nFine print:\n* An order placed on or before 11 September 2026 qualifies. Members at Gold and above only.\n\nA quiet welcome awaits at Pebblestone Garden, where considered pieces are arranged with care.\n\nOrder ORD-566412 placed by Priya Raman:\n- item: SKU-26896\n- product category: bedding\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 18 September 2026\n- membership level: Platinum\n- order subtotal: $79.14",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, which condition in the small print attached to free assembly does order ORD-566412 from Priya Raman miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition"
  ]
 },
 {
  "qid": "q0805684d1b",
  "kind": "yes/no",
  "text": "Support chat about order ORD-640330:\nNadia Haddad: Hi, I placed order ORD-640330 on Thursday, 24 September 2026 for item SKU-86417, and the order subtotal was $125.05.\nAgent: Thanks. The item is in the garden tools product category, its price status is regular price, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Green.\nNadia Haddad: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree gift wrapping at checkout†\n\nWipe it with a damp cloth and let it air-dry. Thanks for buying from Larkspur Playthings.\n\nFine print:\n† Valid for orders whose subtotal is $25.00 or more.\n* Order by Tuesday, 25 August 2026 at the latest. An order qualifies with a subtotal of $100.00 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-640330 from Nadia Haddad get double reward points?"
 },
 {
  "qid": "qe54b0c3956",
  "kind": "choice",
  "text": "Order ORD-989604 placed by Priya Raman:\n| field | value |\n| --- | --- |\n| item | SKU-63727 |\n| product category | toys |\n| price status | refurbished |\n| delivery region | Greyhaven |\n| order date | March 20, 2026 |\n| membership level | Green |\n| order subtotal | $97.04 |\n\nAdvertisement from Brightwell Home:\nFree assembly with every delivery*\nA lifetime warranty on everything we sell†\n\nWelcome to our pages\nThe people at Brightwell Home have gathered thoughtful pieces that feel right at home.\n\nFine print:\n* Excludes the sports gear category. Any item whose status is clearance falls outside this offer.\n† Shoppers get the headline benefit solely for delivery in Greyhaven.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does customer Priya Raman on order ORD-989604 truly receive, given what the advertisement says?",
  "options": [
   "Both offers",
   "Only free assembly",
   "Only the lifetime warranty",
   "Neither offer"
  ]
 },
 {
  "qid": "qe1beffee0f",
  "kind": "yes/no",
  "text": "Support chat about order ORD-855361:\nSelin Yilmaz: Hi, I placed order ORD-855361 on Saturday, 5 September 2026 for item SKU-43067, and the order subtotal was 188.71 USD.\nAgent: Thanks. The item is in the kitchenware product category, its price status is refurbished, and it ships to the Calderon delivery region.\nAgent: Your membership level is Silver.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree installation for every appliance*\n\nHello neighbour, pop by Juniper Gadgets for a chat and a look around.\n\nFine print:\n* Valid: any order taken on or before Thursday, 3 September 2026.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Juniper Gadgets levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWould it be fair to say it is not the case that Selin Yilmaz does not get free installation on order ORD-855361 under the advertised terms?"
 },
 {
  "qid": "q5c461fa3e8",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree shipping on every order†\n\nSubject: Straightforward shopping\nHello, we like plain speaking, so here it is: Larkspur Playthings keeps the essentials stocked and easy to find.\n\nOrder ORD-396338 placed by Mira Castell:\n- item: SKU-22062\n- product category: toys\n- price status: clearance\n- delivery region: Calderon\n- order date: August 24, 2026\n- membership level: Elite\n- order subtotal: $190.46\n\nFine print from the bottom of the advertisement:\n† Any delivery to Calderon is excluded from this offer. Orders dated on or before August 24, 2026 count.\n* Anything with delivery in Calderon is excluded from the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says, with its headline and small print together, does order ORD-396338 from Mira Castell receive free shipping?"
 },
 {
  "qid": "qda4943c927",
  "kind": "yes/no",
  "text": "Order ORD-882679 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-70025 |\n| product category | bedding |\n| price status | refurbished |\n| delivery region | Greyhaven |\n| order date | 2026-10-17 |\n| membership level | Silver |\n| order subtotal | $129.20 |\n\nAdvertisement from Bluecrest Sports:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nFine print:\n* Valid: any order taken on or before 2026-10-16.\n† Valid for orders placed from 2026-11-25 onward. Reserved for members at Gold or below.\n\nCrafted to endure\nWe are proud to present Bluecrest Sports, a house of considered design and enduring materials.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does order ORD-882679 from Aiko Brandt lose out on free gift wrapping?"
 },
 {
  "qid": "q8c26e6b52f",
  "kind": "choice",
  "text": "Support chat about order ORD-305472:\nSelin Yilmaz: Hi, I placed order ORD-305472 on Sunday, 10 May 2026 for item SKU-25674, and the order subtotal was $145.14.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Elite.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nWe match any lower price*\nA lifetime warranty on everything we sell†\n\nSubject: A hop, skip and a browse\nHello hello, Oakhurst Interiors is skipping around the shelves with cheerful little curios.\n\nFine print:\n* Members ranked Elite and above are the only ones covered. Order by Wednesday, 3 June 2026 at the latest.\n† Headline benefit applies to orders with delivery in Dunmere only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms, which condition attached to the price match does order ORD-305472 from Selin Yilmaz miss, if any?",
  "options": [
   "The membership-level condition",
   "The order-date condition",
   "The delivery-region condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qf8b46d8d30",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree installation for every appliance†\n\nWelcome back to Larkspur Playthings. Your basket is ready and waiting for a closer glance.\n\nFine print:\n† Membership level Basic or lower required. Anything with delivery in Greyhaven is excluded from the headline benefit.\n* Only members at the Premier level or higher may take part. Only a delivery to Arvale qualifies for this offer.\n\nOrder ORD-730925 placed by Mira Castell:\n- item: SKU-39242\n- product category: electronics\n- price status: final sale\n- delivery region: Arvale\n- order date: 24 October 2026\n- membership level: Plus\n- order subtotal: $128.11",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes Mira Castell get double reward points on order ORD-730925 when the advertised terms, with the headline and its small print, are applied?"
 },
 {
  "qid": "qfbe9c0bdb7",
  "kind": "choice",
  "text": "Support chat about order ORD-108464:\nTomas Ferreira: Hi, I placed order ORD-108464 on October 9, 2026 for item SKU-87370, and the order subtotal was 105.28 USD.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Greyhaven delivery region.\nAgent: Your membership level is Plus.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nFree shipping on every order*\nFree returns on every purchase†\n\nPopping by from the corner, Wrenfield Outdoor says hi\nYour neighbourhood favourite, stocked with care.\n\nFine print:\n† Any order placed on November 16, 2026 and beyond is accepted. The headline benefit is set aside for anything in the electronics category.\n* Any order placed on September 26, 2026 and beyond is accepted. Limited to members at the Basic level or lower.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to free returns does order ORD-108464 from Tomas Ferreira miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The product-category condition"
  ]
 },
 {
  "qid": "q91ed219ed4",
  "kind": "yes/no",
  "text": "Support chat about order ORD-394873:\nHugo Lindqvist: Hi, I placed order ORD-394873 on 2026-03-02 for item SKU-92943, and the order subtotal was 231.21 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is clearance, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Blue.\nHugo Lindqvist: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\n\nOur doors are wide and our kettle is warm at Birchwood Linens, so please come and sit down for a bit.\n\nFine print:\n* Customers must spend at least $200 on the order subtotal. Valid for orders placed from 2026-03-02 onward.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes Hugo Lindqvist get free shipping on order ORD-394873 when the advertised terms, with the headline and its small print, are applied?"
 },
 {
  "qid": "q0f08582932",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\nWe match any lower price†\n\nGet cozy at Wrenfield Outdoor, the friendliest corner of the internet.\n\nFine print:\n† Shoppers get the headline benefit solely for delivery in Greyhaven. Minimum order subtotal: $50.\n* For members at Silver or lower. Orders headed for delivery in Greyhaven are kept out of this offer.\n\nOrder ORD-884374 placed by Owen Mensah:\n- item: SKU-79560\n- product category: kitchenware\n- price status: regular price\n- delivery region: Greyhaven\n- order date: 11 Aug 2026\n- membership level: Silver\n- order subtotal: $50.00",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-884374 from Owen Mensah forfeit the price match under the advertised terms, as those terms are written?"
 },
 {
  "qid": "q047558938d",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree returns on every purchase*\nWe match any lower price†\n\nFine print:\n† An order placed on or before 11 June 2026 qualifies. For members at Plus or lower.\n* Placed before 8 June 2026 counts; that very day is excluded.\n\nGood coffee, good company and a little bit of fun at Brightwell Home. Pop by and see what we have been up to.\n\nOrder ORD-895256 placed by Felix Moreau:\n- item: SKU-18703\n- product category: toys\n- price status: regular price\n- delivery region: Dunmere\n- order date: 7 June 2026\n- membership level: Premier\n- order subtotal: $74.85",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, which condition attached to the price match does order ORD-895256 from Felix Moreau miss, if any?",
  "options": [
   "The order-date condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qf456bfc020",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree shipping on every order†\n\nSubject: Straightforward shopping\nHello, we like plain speaking, so here it is: Larkspur Playthings keeps the essentials stocked and easy to find.\n\nOrder ORD-224962 placed by Dana Okafor:\n- item: SKU-33122\n- product category: garden tools\n- price status: regular price\n- delivery region: Dunmere\n- order date: Monday, 27 April 2026\n- membership level: Premier\n- order subtotal: $201.32\n\nFine print from the bottom of the advertisement:\n† Any delivery to Calderon is excluded from this offer. Orders dated on or before Saturday, 11 April 2026 count.\n* Anything with delivery in Calderon is excluded from the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that, under the advertised terms, the order ORD-224962 from Dana Okafor doesn't get free shipping?"
 },
 {
  "qid": "q38c922a7af",
  "kind": "choice",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\n\nWrenfield Outdoor, measured and poised\nA gracious setting to linger and admire the craftsmanship.\n\nFine print:\n* Shoppers may place orders on Sunday, June 7, 2026 itself and on every day before it. Delivery to Fallowmere sits outside the headline benefit.\n\nOrder ORD-634375 placed by Ines Duarte:\n- item: SKU-28799\n- product category: kitchenware\n- price status: regular price\n- delivery region: Dunmere\n- order date: Monday, June 8, 2026\n- membership level: Platinum\n- order subtotal: $118.97",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Wrenfield Outdoor levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to free shipping does order ORD-634375 from Ines Duarte miss, if any?",
  "options": [
   "The delivery-region condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q62e83178b4",
  "kind": "choice",
  "text": "Order ORD-952893 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-47546 |\n| product category | garden tools |\n| price status | open box |\n| delivery region | Dunmere |\n| order date | 16 Apr 2026 |\n| membership level | Plus |\n| order subtotal | 47.10 USD |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nFine print:\n† Items at pre-order pricing are withheld from this benefit.\n* Headline benefit is limited to delivery in Hollin.\n\nSubject: A warm hello from our team\nDear friend, we love sharing our newest pieces with you at Copperleaf Kitchen.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOf the conditions in the small print attached to free shipping, which, if any, does order ORD-952893 from Ravi Anand miss, according to what the advertisement says?",
  "options": [
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qd4e61a9e2d",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree installation for every appliance†\n\nWelcome back to Larkspur Playthings. Your basket is ready and waiting for a closer glance.\n\nFine print:\n† Membership level Basic or lower required. Anything with delivery in Greyhaven is excluded from the headline benefit.\n* Only members at the Plus level or higher may take part. Only a delivery to Arvale qualifies for this offer.\n\nOrder ORD-730925 placed by Mira Castell:\n- item: SKU-39242\n- product category: electronics\n- price status: final sale\n- delivery region: Arvale\n- order date: 24 October 2026\n- membership level: Plus\n- order subtotal: $128.11",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes Mira Castell get double reward points on order ORD-730925 when the advertised terms, with the headline and its small print, are applied?"
 },
 {
  "qid": "qb88e110cf2",
  "kind": "yes/no",
  "text": "Support chat about order ORD-451477:\nRavi Anand: Hi, I placed order ORD-451477 on 8 Aug 2026 for item SKU-27809, and the order subtotal was $249.84.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Calderon delivery region.\nAgent: Your membership level is Green.\nRavi Anand: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree gift wrapping at checkout†\n\nWipe it with a damp cloth and let it air-dry. Thanks for buying from Larkspur Playthings.\n\nFine print:\n† Valid for orders whose subtotal is $50.00 or more.\n* Order by 4 Sep 2026 at the latest. An order qualifies with a subtotal of $200.00 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-451477 from Ravi Anand get double reward points?"
 },
 {
  "qid": "qdd9a9fd8d5",
  "kind": "yes/no",
  "text": "Support chat about order ORD-820169:\nLena Whitcombe: Hi, I placed order ORD-820169 on 2026-03-31 for item SKU-22448, and the order subtotal was 95.49 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is pre-order, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Silver.\nLena Whitcombe: I am asking about the advertisement below.\n\nAdvertisement from Marigold Pets:\nFree installation for every appliance*\n\nHi neighbours, it is Marigold Pets here with fresh ideas for your cooking. Pop by and say hello, we love to see friendly faces.\n*Order by 2026-03-30 at the latest. The order subtotal must be above 100.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-820169 from Lena Whitcombe lose out on free installation under the advertised terms, as the advertisement and its fine print describe?"
 },
 {
  "qid": "q52437c4d4c",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nSubject: simple ways to enjoy better sound\nHello there,\nKestrel Outfitters helps your everyday listening sound clearer. Our speakers, headphones and cables are chosen for dependable performance. Setup is straightforward, so start enjoying the music.\nTake care,\n*Valid for orders placed on or before 26 Aug 2026. Members at the Blue level or higher only.\n\nOrder ORD-942232 placed by Clara Voss:\n- item: SKU-14508\n- product category: sports gear\n- price status: open box\n- delivery region: Fallowmere\n- order date: 11 Sep 2026\n- membership level: Blue\n- order subtotal: 244.44 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print together, does order ORD-942232 from Clara Voss fail to secure the lifetime warranty under the advertised terms?"
 },
 {
  "qid": "q772e945cfa",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\n\nSubject: A standard built to endure\nHello, the cut and finish on show at Juniper Gadgets is confident and clean.\n\nFine print:\n* Only the garden tools category earns the headline benefit. Stock with final sale status is excluded from this benefit.\n\nOrder ORD-933578 placed by Jonah Pryce:\n- item: SKU-79572\n- product category: garden tools\n- price status: final sale\n- delivery region: Brenmoor\n- order date: 29 May 2026\n- membership level: Green\n- order subtotal: 17.10 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, does Jonah Pryce earn free gift wrapping with order ORD-933578?"
 },
 {
  "qid": "q315c530b56",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\n\nSubject: A standard built to endure\nHello, the cut and finish on show at Juniper Gadgets is confident and clean.\n\nFine print:\n* Only the kitchenware category earns the headline benefit. Stock with clearance status is excluded from this benefit.\n\nOrder ORD-900022 placed by Tomas Ferreira:\n- item: SKU-17252\n- product category: kitchenware\n- price status: refurbished\n- delivery region: Greyhaven\n- order date: 26 August 2026\n- membership level: Black\n- order subtotal: 208.91 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, does order ORD-900022 from Tomas Ferreira fail to get free gift wrapping under the advertised terms?"
 },
 {
  "qid": "qe04b0a023e",
  "kind": "yes/no",
  "text": "Advertisement from Bluecrest Sports:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Any order placed on February 12, 2026 and beyond is accepted. Items at the refurbished pricing status sit outside this promotion.\n† Each item bearing the refurbished status is withheld from the main benefit.\n\nSubject: Tidy layout, simple search\nHello, the crisp design of Bluecrest Sports keeps the range in clear view and within easy grasp.\n\nOrder ORD-392107 placed by Priya Raman:\n- item: SKU-91271\n- product category: garden tools\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: March 17, 2026\n- membership level: Green\n- order subtotal: $18.40",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Bluecrest Sports levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-392107 from Priya Raman fail to receive double reward points under the advertised terms, judging by what the advertisement says?"
 },
 {
  "qid": "q2e63f26bf5",
  "kind": "yes/no",
  "text": "Support chat about order ORD-668719:\nSelin Yilmaz: Hi, I placed order ORD-668719 on Thursday, April 16, 2026 for item SKU-98943, and the order subtotal was 224.17 USD.\nAgent: Thanks. The item is in the kitchenware product category, its price status is refurbished, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Platinum.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree installation for every appliance*\n\nHello neighbour, pop by Juniper Gadgets for a chat and a look around.\n\nFine print:\n* Valid: any order taken on or before Saturday, May 23, 2026.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Juniper Gadgets levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWould it be fair to say it is not the case that Selin Yilmaz does not get free installation on order ORD-668719 under the advertised terms?"
 },
 {
  "qid": "q79d5e792aa",
  "kind": "choice",
  "text": "Order ORD-519659 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-49561 |\n| product category | toys |\n| price status | open box |\n| delivery region | Dunmere |\n| order date | April 9, 2026 |\n| membership level | Blue |\n| order subtotal | $73.12 |\n\nAdvertisement from Brightwell Home:\nFree assembly with every delivery*\nA lifetime warranty on everything we sell†\n\nWelcome to our pages\nThe people at Brightwell Home have gathered thoughtful pieces that feel right at home.\n\nFine print:\n* Excludes the garden tools category. Any item whose status is pre-order falls outside this offer.\n† Shoppers get the headline benefit solely for delivery in Dunmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does customer Nadia Haddad on order ORD-519659 truly receive, given what the advertisement says?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the lifetime warranty",
   "Only free assembly"
  ]
 },
 {
  "qid": "q1a50d71aa6",
  "kind": "choice",
  "text": "Advertisement from Wrenfield Outdoor:\nFree installation for every appliance*\n\nSubject: Hello from your local shop\nHi there,\nWrenfield Outdoor is your small neighbourhood shop, and we love helping furry friends feel at home. Drop by for a chat and a friendly face. We are so glad you are part of our little community.\n*The order subtotal must be above 150.00 USD. Excludes items with open box status.\n\nOrder ORD-142242 placed by Clara Voss:\n- item: SKU-36251\n- product category: pet supplies\n- price status: pre-order\n- delivery region: Dunmere\n- order date: 4 March 2026\n- membership level: Gold\n- order subtotal: 123.55 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIf any, which condition in the advertisement and its fine print attached to free installation does order ORD-142242 from Clara Voss miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "qc201adab59",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nSubject: simple ways to enjoy better sound\nHello there,\nKestrel Outfitters helps your everyday listening sound clearer. Our speakers, headphones and cables are chosen for dependable performance. Setup is straightforward, so start enjoying the music.\nTake care,\n*Valid for orders placed on or before 25 April 2026. Members at the Black level or higher only.\n\nOrder ORD-123036 placed by Felix Moreau:\n- item: SKU-15618\n- product category: electronics\n- price status: regular price\n- delivery region: Fallowmere\n- order date: 25 March 2026\n- membership level: Black\n- order subtotal: $238.11",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, and going by what the advertisement says, is it true that order ORD-123036 from Felix Moreau doesn't get the lifetime warranty?"
 },
 {
  "qid": "qd53032d103",
  "kind": "yes/no",
  "text": "Advertisement from Bluecrest Sports:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Any order placed on February 12, 2026 and beyond is accepted. Items at the refurbished pricing status sit outside this promotion.\n† Each item bearing the refurbished status is withheld from the main benefit.\n\nSubject: Tidy layout, simple search\nHello, the crisp design of Bluecrest Sports keeps the range in clear view and within easy grasp.\n\nOrder ORD-392107 placed by Priya Raman:\n- item: SKU-91271\n- product category: garden tools\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: March 17, 2026\n- membership level: Green\n- order subtotal: $18.40",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Bluecrest Sports levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad and its small print say that order ORD-392107 from Priya Raman gets double reward points?"
 },
 {
  "qid": "q1af642196c",
  "kind": "choice",
  "text": "Order ORD-117429 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-40679 |\n| product category | furniture |\n| price status | final sale |\n| delivery region | Fallowmere |\n| order date | 4 March 2026 |\n| membership level | Blue |\n| order subtotal | 115.08 USD |\n\nAdvertisement from Northvale Audio:\nWe match any lower price*\nFree gift wrapping at checkout†\n\nCome for a chat, stay for the cosy corners, and leave with a little treasure from Northvale Audio.\n\nFine print:\n* The benefit is reserved for delivery bound for Fallowmere.\n† Anything filed under the furniture category sits outside this offer.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Northvale Audio levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-117429 placed by Aiko Brandt, which headline offers does the advertisement and its fine print actually allow, offer by offer?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the price match",
   "Only free gift wrapping"
  ]
 },
 {
  "qid": "qcd8bb2d4c5",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nSubject: simple ways to enjoy better sound\nHello there,\nKestrel Outfitters helps your everyday listening sound clearer. Our speakers, headphones and cables are chosen for dependable performance. Setup is straightforward, so start enjoying the music.\nTake care,\n*Valid for orders placed on or before 25 April 2026. Members at the Black level or higher only.\n\nOrder ORD-123036 placed by Felix Moreau:\n- item: SKU-15618\n- product category: electronics\n- price status: regular price\n- delivery region: Fallowmere\n- order date: 25 March 2026\n- membership level: Blue\n- order subtotal: $238.11",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-123036 from Felix Moreau come with the lifetime warranty under what the advertisement says, headline and small print included?"
 },
 {
  "qid": "q5dd0c6d32c",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree shipping on every order†\n\nSubject: Straightforward shopping\nHello, we like plain speaking, so here it is: Larkspur Playthings keeps the essentials stocked and easy to find.\n\nOrder ORD-396338 placed by Mira Castell:\n- item: SKU-22062\n- product category: toys\n- price status: clearance\n- delivery region: Calderon\n- order date: August 24, 2026\n- membership level: Elite\n- order subtotal: $190.46\n\nFine print from the bottom of the advertisement:\n† Any delivery to Greyhaven is excluded from this offer. Orders dated on or before August 24, 2026 count.\n* Anything with delivery in Calderon is excluded from the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says, with its headline and small print together, does order ORD-396338 from Mira Castell receive free shipping?"
 },
 {
  "qid": "q7d44aad031",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree shipping on every order*\n\nFine print:\n* The order subtotal must be above 35.00 USD. Delivery to Arvale sits outside the headline benefit.\n\nStep right in\nBrisk service, modern style and a lively edge make Brightwell Home worth a visit.\n\nOrder ORD-423455 placed by Jonah Pryce:\n- item: SKU-56573\n- product category: garden tools\n- price status: open box\n- delivery region: Eskarth\n- order date: 22 July 2026\n- membership level: Premier\n- order subtotal: 35.00 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-423455 from Jonah Pryce against the advertised terms, which condition in the small print attached to free shipping does it miss, if any?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qe7c94b403e",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nWander around Tidewell Supply at your own pace and see what makes us giggle.\n\nOrder ORD-804134 placed by Tomas Ferreira:\n- item: SKU-93863\n- product category: furniture\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: August 24, 2026\n- membership level: Premier\n- order subtotal: $232.34\n\nFine print from the bottom of the advertisement:\n* Items in the furniture product category are excluded. For members at Premier or lower.\n† Items under the kitchenware category are carved out of this offer. Any item whose status is clearance falls outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement alongside its fine print, does Tomas Ferreira receive the price match on order ORD-804134?"
 },
 {
  "qid": "qc045c864c4",
  "kind": "choice",
  "text": "Advertisement from Pebblestone Garden:\nFree assembly with every delivery*\n\nFine print:\n* An order placed on or before 5 Oct 2026 qualifies. Members at Platinum and above only.\n\nA quiet welcome awaits at Pebblestone Garden, where considered pieces are arranged with care.\n\nOrder ORD-574557 placed by Ines Duarte:\n- item: SKU-95545\n- product category: sports gear\n- price status: open box\n- delivery region: Greyhaven\n- order date: 5 Oct 2026\n- membership level: Platinum\n- order subtotal: 39.49 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, which condition in the small print attached to free assembly does order ORD-574557 from Ines Duarte miss, if any?",
  "options": [
   "The order-date condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qf3fe6c92c7",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nSubject: simple ways to enjoy better sound\nHello there,\nKestrel Outfitters helps your everyday listening sound clearer. Our speakers, headphones and cables are chosen for dependable performance. Setup is straightforward, so start enjoying the music.\nTake care,\n*Valid for orders placed on or before 26 Aug 2026. Members at the Blue level or higher only.\n\nOrder ORD-942232 placed by Clara Voss:\n- item: SKU-14508\n- product category: sports gear\n- price status: open box\n- delivery region: Fallowmere\n- order date: 26 Aug 2026\n- membership level: Blue\n- order subtotal: 244.44 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-942232 from Clara Voss come with the lifetime warranty under what the advertisement says, headline and small print included?"
 },
 {
  "qid": "q54786ce095",
  "kind": "yes/no",
  "text": "Advertisement from Bluecrest Sports:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Any order placed on September 3, 2026 and beyond is accepted. Items at the final sale pricing status sit outside this promotion.\n† Each item bearing the pre-order status is withheld from the main benefit.\n\nSubject: Tidy layout, simple search\nHello, the crisp design of Bluecrest Sports keeps the range in clear view and within easy grasp.\n\nOrder ORD-165332 placed by Lena Whitcombe:\n- item: SKU-70010\n- product category: bedding\n- price status: pre-order\n- delivery region: Greyhaven\n- order date: September 2, 2026\n- membership level: Black\n- order subtotal: $178.72",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Bluecrest Sports levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad and its small print say that order ORD-165332 from Lena Whitcombe gets double reward points?"
 },
 {
  "qid": "q38c6ffe2c9",
  "kind": "choice",
  "text": "Support chat about order ORD-508758:\nFelix Moreau: Hi, I placed order ORD-508758 on Thursday, February 26, 2026 for item SKU-67230, and the order subtotal was $78.78.\nAgent: Thanks. The item is in the toys product category, its price status is regular price, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Basic.\nFelix Moreau: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nWe match any lower price*\nA lifetime warranty on everything we sell†\n\nSubject: A hop, skip and a browse\nHello hello, Oakhurst Interiors is skipping around the shelves with cheerful little curios.\n\nFine print:\n* Members ranked Plus and above are the only ones covered. Order by Monday, March 16, 2026 at the latest.\n† Headline benefit applies to orders with delivery in Fallowmere only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertised terms, which condition attached to the price match does order ORD-508758 from Felix Moreau miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition",
   "The order-date condition"
  ]
 },
 {
  "qid": "q5c0bf072d8",
  "kind": "yes/no",
  "text": "Support chat about order ORD-855361:\nSelin Yilmaz: Hi, I placed order ORD-855361 on Thursday, 3 September 2026 for item SKU-43067, and the order subtotal was 188.71 USD.\nAgent: Thanks. The item is in the kitchenware product category, its price status is refurbished, and it ships to the Calderon delivery region.\nAgent: Your membership level is Silver.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree installation for every appliance*\n\nHello neighbour, pop by Juniper Gadgets for a chat and a look around.\n\nFine print:\n* Valid: any order taken on or before Thursday, 3 September 2026.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Juniper Gadgets levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWould it be fair to say it is not the case that Selin Yilmaz does not get free installation on order ORD-855361 under the advertised terms?"
 },
 {
  "qid": "q90a0bacc48",
  "kind": "yes/no",
  "text": "Support chat about order ORD-820169:\nLena Whitcombe: Hi, I placed order ORD-820169 on 2026-03-31 for item SKU-22448, and the order subtotal was 95.49 USD.\nAgent: Thanks. The item is in the furniture product category, its price status is pre-order, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Silver.\nLena Whitcombe: I am asking about the advertisement below.\n\nAdvertisement from Marigold Pets:\nFree installation for every appliance*\n\nHi neighbours, it is Marigold Pets here with fresh ideas for your cooking. Pop by and say hello, we love to see friendly faces.\n*Order by 2026-03-30 at the latest. The order subtotal must be above 100.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by what the advertisement says, does order ORD-820169 from Lena Whitcombe get free installation under its headline and that headline's small print?"
 },
 {
  "qid": "q420567d143",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree shipping on every order*\n\nFine print:\n* The order subtotal must be above 35.00 USD. Delivery to Arvale sits outside the headline benefit.\n\nStep right in\nBrisk service, modern style and a lively edge make Brightwell Home worth a visit.\n\nOrder ORD-423455 placed by Jonah Pryce:\n- item: SKU-56573\n- product category: garden tools\n- price status: open box\n- delivery region: Eskarth\n- order date: 22 July 2026\n- membership level: Premier\n- order subtotal: 37.13 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-423455 from Jonah Pryce against the advertised terms, which condition in the small print attached to free shipping does it miss, if any?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q08e6ce987c",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nWander around Tidewell Supply at your own pace and see what makes us giggle.\n\nOrder ORD-804134 placed by Tomas Ferreira:\n- item: SKU-93863\n- product category: furniture\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: August 24, 2026\n- membership level: Premier\n- order subtotal: $232.34\n\nFine print from the bottom of the advertisement:\n* Items in the furniture product category are excluded. For members at Premier or lower.\n† Items under the kitchenware category are carved out of this offer. Any item whose status is clearance falls outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-804134 placed by Tomas Ferreira lose out on the price match?"
 },
 {
  "qid": "q6ed4f306ee",
  "kind": "choice",
  "text": "Advertisement from Pebblestone Garden:\nFree assembly with every delivery*\n\nFine print:\n* An order placed on or before 11 September 2026 qualifies. Members at Gold and above only.\n\nA quiet welcome awaits at Pebblestone Garden, where considered pieces are arranged with care.\n\nOrder ORD-566412 placed by Priya Raman:\n- item: SKU-26896\n- product category: bedding\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 11 September 2026\n- membership level: Platinum\n- order subtotal: $79.14",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, which condition in the small print attached to free assembly does order ORD-566412 from Priya Raman miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition"
  ]
 },
 {
  "qid": "q6f41232715",
  "kind": "yes/no",
  "text": "Support chat about order ORD-451477:\nRavi Anand: Hi, I placed order ORD-451477 on 8 Aug 2026 for item SKU-27809, and the order subtotal was $249.84.\nAgent: Thanks. The item is in the sports gear product category, its price status is regular price, and it ships to the Calderon delivery region.\nAgent: Your membership level is Green.\nRavi Anand: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree gift wrapping at checkout†\n\nWipe it with a damp cloth and let it air-dry. Thanks for buying from Larkspur Playthings.\n\nFine print:\n† Valid for orders whose subtotal is $50.00 or more.\n* Order by 4 Sep 2026 at the latest. An order qualifies with a subtotal of $200.00 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, is it true that order ORD-451477 from Ravi Anand does not get double reward points under the advertised terms?"
 }
]
