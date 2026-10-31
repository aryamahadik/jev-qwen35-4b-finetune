# G5-H blind read T07-blind_read-408cf0a5-001 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T07/qc/g5h/answers/T07-blind_read-408cf0a5-001.json

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
  "qid": "q12c4b55d6f",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree returns on every purchase*\nFree gift wrapping at checkout†\n\nWe appreciate your custom at Larkspur Playthings. Look closely at the stitching and tighten loose fixings gently.\n\nFine print:\n* Orders must be placed on or after 8 August 2026. The order subtotal must be strictly greater than 200.00 USD.\n† Eligibility is limited to the kitchenware category. Valid: any order taken on or before 1 August 2026.\n\nOrder ORD-241677 placed by Aiko Brandt:\n- item: SKU-25686\n- product category: sports gear\n- price status: clearance\n- delivery region: Calderon\n- order date: 1 August 2026\n- membership level: Elite\n- order subtotal: 200.01 USD\n\nNote added by the customer: Aiko Brandt argues the fine print is practically unreadable, and a headline should not be wiped out by lettering nobody can see.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-241677 from Aiko Brandt fail to get free returns under the advertised terms, as the advertisement and its fine print spell out?"
 },
 {
  "qid": "qde0cc3ec30",
  "kind": "choice",
  "text": "Advertisement from Pebblestone Garden:\nFree returns on every purchase*\n\nFine print:\n* Restricted to members at the Bronze level and lower.\n\nOur corner shop at Pebblestone Garden is tucked away, which is part of the charm.\n\nOrder ORD-730559 placed by Ines Duarte:\n- item: SKU-97725\n- product category: bedding\n- price status: open box\n- delivery region: Calderon\n- order date: Wednesday, 16 September 2026\n- membership level: Silver\n- order subtotal: 110.55 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to free returns does order ORD-730559 from Ines Duarte miss, if any?",
  "options": [
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qd662819fad",
  "kind": "choice",
  "text": "Order ORD-843534 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-39898 |\n| product category | garden tools |\n| price status | refurbished |\n| delivery region | Arvale |\n| order date | 28 May 2026 |\n| membership level | Green |\n| order subtotal | 100.06 USD |\n\nAdvertisement from Brightwell Home:\nA lifetime warranty on everything we sell*\nDouble reward points on every purchase†\n\nFine print:\n† Qualifying orders: subtotal 100.00 USD or more.\n* Each order needs delivery to Arvale to earn the benefit. Stock flagged as refurbished sits outside this offer.\n\nSoft light, measured choices and a feeling of unhurried grace greet you at Brightwell Home.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhere the advertisement attaches small print to the lifetime warranty, which condition, if any, does order ORD-843534 from Ines Duarte miss?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition"
  ]
 },
 {
  "qid": "qadba6c606c",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nA lifetime warranty on everything we sell*\nFree gift wrapping at checkout†\n\nFine print:\n* Limited to members at the Premier level or lower.\n† Items at the open box pricing status sit outside this promotion.\n\nStop by Brightwell Home for the essentials you use at home.\n\nOrder ORD-164875 placed by Tomas Ferreira:\n- item: SKU-50460\n- product category: bedding\n- price status: pre-order\n- delivery region: Eskarth\n- order date: 27 August 2026\n- membership level: Premier\n- order subtotal: $82.07\n\nNote added by the customer: Tomas Ferreira has given this store loyalty for a good while, so surely the promotion can stretch a little.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers from the ad and its small print does order ORD-164875 placed by Tomas Ferreira actually get, offer by offer?",
  "options": [
   "Only the lifetime warranty",
   "Both offers",
   "Only free gift wrapping",
   "Neither offer"
  ]
 },
 {
  "qid": "q9acf53676e",
  "kind": "yes/no",
  "text": "Support chat about order ORD-929336:\nLena Whitcombe: Hi, I placed order ORD-929336 on 2026-05-04 for item SKU-76259, and the order subtotal was $91.16.\nAgent: Thanks. The item is in the electronics product category, its price status is regular price, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Elite.\nLena Whitcombe: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nFree gift wrapping at checkout*\n\nWelcome back to Pebblestone Garden. Your basket is ready and waiting for a closer glance.\n\nFine print:\n* Valid on orders of $75.00 or more. Applies to orders placed on or after 2026-05-04.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhen the headline and its small print are read against the advertised terms, does order ORD-929336 from Lena Whitcombe receive free gift wrapping?"
 },
 {
  "qid": "q12a3528f83",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree shipping on every order*\n\nJuniper Gadgets is a friendly corner of the high street, full of local makers and warm hellos. Come say hello and have a browse. We love having you here.\n*Excludes items with refurbished status. Covers the sports gear product category only.\n\nOrder ORD-662214 placed by Ravi Anand:\n- item: SKU-16238\n- product category: kitchenware\n- price status: pre-order\n- delivery region: Calderon\n- order date: July 9, 2026\n- membership level: Black\n- order subtotal: 57.78 USD\n\nNote added by the customer: Ravi Anand feels a small wobble in the arrival should not spoil the promotion, since the order landed almost exactly as expected.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad and its small print say that order ORD-662214 from Ravi Anand gets free shipping?"
 },
 {
  "qid": "q0823955bc2",
  "kind": "choice",
  "text": "Order ORD-898133 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-15890 |\n| product category | bedding |\n| price status | final sale |\n| delivery region | Brenmoor |\n| order date | 14 August 2026 |\n| membership level | Premier |\n| order subtotal | 49.99 USD |\n\nAdvertisement from Fernway Market:\nWe match any lower price*\nFree assembly with every delivery†\n\nFine print:\n* Qualifying orders are placed before 14 August 2026, excluding that date. Shoppers get the headline benefit solely for delivery in Brenmoor.\n† Valid for orders whose subtotal is $50 or more.\n\nCome on in, Fernway Market has a warm corner for you\nSettle back and enjoy the easy pace of browsing.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nLooking at the ad and its small print, which condition attached to the price match does order ORD-898133 from Selin Yilmaz miss, if any?",
  "options": [
   "The order-subtotal condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qac0812b009",
  "kind": "yes/no",
  "text": "Advertisement from Bluecrest Sports:\nWe match any lower price*\n\nBring the crew along to Bluecrest Sports for a relaxed look around. Little ones and older friends alike find a favourite here.\n\nFine print:\n* Items marked with the pre-order status fall outside the benefit set out here. An order whose delivery goes to Hollin falls outside the headline benefit.\n\nOrder ORD-441490 placed by Felix Moreau:\n- item: SKU-35332\n- product category: toys\n- price status: pre-order\n- delivery region: Hollin\n- order date: Tuesday, 6 October 2026\n- membership level: Black\n- order subtotal: 170.54 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Bluecrest Sports levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the advertisement with its fine print confirm that order ORD-441490 from Felix Moreau comes with the price match?"
 },
 {
  "qid": "q751b0ffc30",
  "kind": "yes/no",
  "text": "Support chat about order ORD-612835:\nTomas Ferreira: Hi, I placed order ORD-612835 on Wednesday, October 14, 2026 for item SKU-59299, and the order subtotal was 39.25 USD.\nAgent: Thanks. The item is in the electronics product category, its price status is regular price, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Plus.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Pebblestone Garden:\nFree shipping on every order*\n\nWarm wishes from the team at Pebblestone Garden, and thank you for coming along.\n\nFine print:\n* Restricted to members at the Plus level and lower. Valid on orders of 50.00 USD or more.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Pebblestone Garden levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-612835 from Tomas Ferreira get free shipping?"
 },
 {
  "qid": "q5788fc0755",
  "kind": "choice",
  "text": "Support chat about order ORD-946816:\nDana Okafor: Hi, I placed order ORD-946816 on Tuesday, 14 July 2026 for item SKU-46080, and the order subtotal was 220.72 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is refurbished, and it ships to the Calderon delivery region.\nAgent: Your membership level is Plus.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nA lifetime warranty on everything we sell*\nFree shipping on every order†\n\nAn elegant pause at Oakhurst Interiors\nThoughtfully edited displays, unhurried and softly lit.\n\nFine print:\n* Items at the refurbished pricing status sit outside this promotion.\n† Stock flagged as open box sits outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nThe ad and its small print tie conditions to free shipping; which, if any, does order ORD-946816 from Dana Okafor miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition"
  ]
 },
 {
  "qid": "qe8b9273c48",
  "kind": "choice",
  "text": "Order ORD-385723 placed by Jonah Pryce:\n| field | value |\n| --- | --- |\n| item | SKU-49961 |\n| product category | toys |\n| price status | clearance |\n| delivery region | Arvale |\n| order date | 2026-09-07 |\n| membership level | Basic |\n| order subtotal | 88.75 USD |\n\nAdvertisement from Harborlight Goods:\nFree assembly with every delivery*\nFree returns on every purchase†\n\nA little shop with a big heart\nAt Harborlight Goods we enjoy meeting our customers and sharing what we discover along the way.\n\nFine print:\n† Items at final sale pricing are withheld from this benefit. Valid on orders over 100.00 USD.\n* Anything with delivery in Fallowmere is excluded from the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nPer what the advertisement says, which condition in the small print attached to free returns does Jonah Pryce's order ORD-385723 miss, if any?",
  "options": [
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q7b46fda48e",
  "kind": "choice",
  "text": "Support chat about order ORD-376966:\nJonah Pryce: Hi, I placed order ORD-376966 on 3 June 2026 for item SKU-68358, and the order subtotal was 48.93 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is pre-order, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Black.\nJonah Pryce: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\nWe match any lower price†\n\n{\"title\": \"A sharper way to shop at Birchwood Linens\", \"subtitle\": \"Precise search, clear ranges, dependable results\", \"button\": \"Begin here\"}\n\nFine print:\n* Items whose status is final sale sit outside this offer. Items under the sports gear category are carved out of this offer.\n† Minimum order subtotal: 50.00 USD.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-376966 from Jonah Pryce, which condition in the small print attached to free shipping does it miss, if any, as the advertisement says?",
  "options": [
   "The order-subtotal condition",
   "The price-status condition",
   "The product-category condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q436bc12cfb",
  "kind": "choice",
  "text": "Advertisement from Marigold Pets:\nFree installation for every appliance*\nFree assembly with every delivery†\n\nFine print:\n† Subtotal must be strictly above 200.00 USD.\n* Subtotal of 75.00 USD or more required.\n\nSubject: Notes from the counter\nHello there, our staff at Marigold Pets have been busy, and we hope you enjoy a little peek inside.\n\nOrder ORD-679433 placed by Mira Castell:\n- item: SKU-35850\n- product category: garden tools\n- price status: clearance\n- delivery region: Fallowmere\n- order date: 2026-06-15\n- membership level: Black\n- order subtotal: 122.10 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGiven the advertisement and its fine print, which of its headline offers does order ORD-679433, placed by Mira Castell, really get?",
  "options": [
   "Both offers",
   "Neither offer",
   "Only free assembly",
   "Only free installation"
  ]
 },
 {
  "qid": "qee45819068",
  "kind": "yes/no",
  "text": "Order ORD-661048 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-47347 |\n| product category | pet supplies |\n| price status | final sale |\n| delivery region | Fallowmere |\n| order date | 12 Sep 2026 |\n| membership level | Plus |\n| order subtotal | 91.48 USD |\n\nAdvertisement from Copperleaf Kitchen:\nFree gift wrapping at checkout*\nFree shipping on every order†\n\nFine print:\n* Orders placed by 6 Oct 2026 are valid, and the stated day is included. Applies to members of the Plus level or lower.\n† Excludes all items with final sale status. An order placed on or before 12 Sep 2026 qualifies.\n\nSubject: A little note from Copperleaf Kitchen\nHi friend, it is lovely to see you here and we wanted to send our warmest wishes.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the advertisement with its fine print confirm that order ORD-661048 from Tomas Ferreira comes with free gift wrapping?"
 },
 {
  "qid": "q3e418aaabf",
  "kind": "choice",
  "text": "Advertisement from Bluecrest Sports:\nFree gift wrapping at checkout*\nFree installation for every appliance†\n\nKeep it simple at Bluecrest Sports, with useful kit and practical help close at hand.\n\nFine print:\n† Products whose category is pet supplies sit outside the headline benefit.\n* Minimum order subtotal: $50.00.\n\nOrder ORD-886531 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-76364 |\n| product category | toys |\n| price status | refurbished |\n| delivery region | Eskarth |\n| order date | 24 February 2026 |\n| membership level | Green |\n| order subtotal | $50.00 |",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOffer by offer, which headline offers does what the advertisement says, small print included, actually give Tomas Ferreira on order ORD-886531?",
  "options": [
   "Neither offer",
   "Only free gift wrapping",
   "Only free installation",
   "Both offers"
  ]
 },
 {
  "qid": "q2345d72862",
  "kind": "yes/no",
  "text": "Advertisement from Fernway Market:\nFree installation for every appliance*\n\nFine print:\n* Anything with delivery in Eskarth is excluded from the headline benefit. Applies to order subtotals of $75 or more.\n\nWelcome to our catalogue\nFamily favourites, practical picks and friendly ideas for busy households, gathered together by the team at Fernway Market.\n\nOrder ORD-539634 placed by Kofi Asante:\n- item: SKU-92433\n- product category: furniture\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: 3 October 2026\n- membership level: Silver\n- order subtotal: $74.99",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the ad and its small print, does order ORD-539634 from Kofi Asante lose out on free installation under the advertised terms?"
 },
 {
  "qid": "q6cef840688",
  "kind": "choice",
  "text": "Support chat about order ORD-838642:\nOwen Mensah: Hi, I placed order ORD-838642 on Tuesday, 4 August 2026 for item SKU-14628, and the order subtotal was $165.05.\nAgent: Thanks. The item is in the toys product category, its price status is final sale, and it ships to the Hollin delivery region.\nAgent: Your membership level is Blue.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nWe match any lower price*\nFree shipping on every order†\n\nHop in, Birchwood Linens is feeling playful\nTry a treat from our giggle-worthy shelves.\n\nFine print:\n† Excludes delivery to Calderon. Valid only for items in the toys category.\n* Excludes delivery to Calderon. For Black members and above.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing through the ad, which small-print condition attached to the price match does order ORD-838642 from Owen Mensah miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition",
   "The delivery-region condition",
   "The product-category condition"
  ]
 },
 {
  "qid": "q0d869394d6",
  "kind": "yes/no",
  "text": "Advertisement from Birchwood Linens:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\nFast forward\nOur team at Birchwood Linens has sharpened the edit with sleek, refined pieces.\n\nFine print:\n† Order subtotal exceeds $150. Headline benefit applies to orders with delivery in Dunmere only.\n* Anything with delivery in Fallowmere is excluded from the headline benefit.\n\nOrder ORD-782502 placed by Jonah Pryce:\n- item: SKU-72153\n- product category: electronics\n- price status: pre-order\n- delivery region: Arvale\n- order date: Monday, July 20, 2026\n- membership level: Elite\n- order subtotal: 150.01 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking the advertisement and its fine print into account, has order ORD-782502 from Jonah Pryce lost out on free gift wrapping?"
 },
 {
  "qid": "q2b4eddb502",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nWe match any lower price*\n\nFine print:\n* Orders must be placed before Friday, July 31, 2026, and the day itself is excluded.\n\n{\"title\": \"Sleek picks from Larkspur Playthings\", \"subtitle\": \"Built for speed, styled for you\", \"button\": \"Shop the lineup\"}\n\nOrder ORD-959089 placed by Kofi Asante:\n- item: SKU-85456\n- product category: furniture\n- price status: pre-order\n- delivery region: Arvale\n- order date: Friday, July 31, 2026\n- membership level: Elite\n- order subtotal: 38.65 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder what the advertisement says, headline and small print included, does Kofi Asante get the price match on order ORD-959089?"
 },
 {
  "qid": "qe1f18884ad",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree returns on every purchase*\nFree installation for every appliance†\n\nFine print:\n* Subtotal must be strictly above 25.00 USD.\n† Excludes the electronics category. Orders must be placed on or after Wednesday, March 4, 2026.\n\nWelcome back to Juniper Gadgets. Your basket is ready and waiting for a closer glance.\n\nOrder ORD-367426 placed by Lena Whitcombe:\n- item: SKU-83284\n- product category: electronics\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: Wednesday, March 18, 2026\n- membership level: Blue\n- order subtotal: 31.94 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Juniper Gadgets levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad, with its small print taken into account, mean that Lena Whitcombe earns free installation on order ORD-367426?"
 },
 {
  "qid": "q800346368b",
  "kind": "choice",
  "text": "Support chat about order ORD-536743:\nLena Whitcombe: Hi, I placed order ORD-536743 on Monday, 2 March 2026 for item SKU-36979, and the order subtotal was $58.68.\nAgent: Thanks. The item is in the pet supplies product category, its price status is final sale, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Black.\nLena Whitcombe: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\nDouble reward points on every purchase†\n\nGlad you dropped in at Birchwood Linens. Take a swift glance at your basket and head to checkout.\n\nFine print:\n† The order date needs to be on or before Monday, 2 March 2026.\n* The order subtotal must be strictly greater than $75.00.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecked offer by offer against the ad and its small print, which headline offers does Lena Whitcombe actually get with order ORD-536743?",
  "options": [
   "Only double reward points",
   "Both offers",
   "Neither offer",
   "Only free shipping"
  ]
 },
 {
  "qid": "q8811ef9af6",
  "kind": "yes/no",
  "text": "Order ORD-992891 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-37935 |\n| product category | kitchenware |\n| price status | pre-order |\n| delivery region | Greyhaven |\n| order date | October 24, 2026 |\n| membership level | Plus |\n| order subtotal | $39.22 |\n\nAdvertisement from Fernway Market:\nDouble reward points on every purchase*\n\nSubject: a calm note about everyday comforts\nHello there,\nFernway Market has thoughtfully chosen everyday essentials for the friends who share your home. Our picks feel soft, sturdy and easy to care for.\nWarm wishes,\n*The order subtotal must be above $50. Delivery to Greyhaven only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDo the advertisement and its fine print together let order ORD-992891 from Nadia Haddad get double reward points?"
 },
 {
  "qid": "qd9debd6415",
  "kind": "yes/no",
  "text": "Advertisement from Pebblestone Garden:\nFree gift wrapping at checkout*\nFree shipping on every order†\n\nFine print:\n† Each item bearing the refurbished status is withheld from the main benefit.\n* Only items with open box status are excluded from the main benefit.\n\nSubject: A warm hello from our team\nDear friend, we love sharing our newest pieces with you at Pebblestone Garden.\n\nOrder ORD-116506 placed by Nadia Haddad:\n- item: SKU-45762\n- product category: toys\n- price status: refurbished\n- delivery region: Calderon\n- order date: 25 May 2026\n- membership level: Bronze\n- order subtotal: $176.94",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Pebblestone Garden levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWould you say it is not the case that Nadia Haddad does not get free shipping on order ORD-116506 when the advertisement and its fine print are read?"
 },
 {
  "qid": "q73f0691a4a",
  "kind": "yes/no",
  "text": "Advertisement from Harborlight Goods:\nFree installation for every appliance*\n\nReady when you are\nHarborlight Goods stocks the practical bits for home projects, mending and tidy-up jobs.\n\nFine print:\n* The subtotal on the order has to be more than $25.00 to count. Orders delivered to Eskarth are excluded.\n\nOrder ORD-743603 placed by Tomas Ferreira:\n- item: SKU-46291\n- product category: electronics\n- price status: regular price\n- delivery region: Fallowmere\n- order date: 4 Jul 2026\n- membership level: Platinum\n- order subtotal: $25.01",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-743603 from Tomas Ferreira forfeit free installation under the advertised terms, as set out by the advertisement and its fine print?"
 },
 {
  "qid": "qbb322bab1b",
  "kind": "yes/no",
  "text": "Support chat about order ORD-977268:\nPriya Raman: Hi, I placed order ORD-977268 on 18 Sep 2026 for item SKU-91917, and the order subtotal was $78.52.\nAgent: Thanks. The item is in the bedding product category, its price status is open box, and it ships to the Arvale delivery region.\nAgent: Your membership level is Platinum.\nPriya Raman: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree returns on every purchase*\nFree installation for every appliance†\n\nSimple, sensible, reliable\nOur approach at Juniper Gadgets is plain and steady: good products, clear information and a friendly welcome.\n\nFine print:\n† Stock with pre-order status is excluded from this benefit. The order subtotal must be strictly greater than $100.00.\n* Products whose category is bedding sit outside the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWould you say it is not the case that Priya Raman does not get free returns on order ORD-977268 when the advertisement and its fine print are read?"
 },
 {
  "qid": "q4327eb1ddc",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nFree returns on every purchase*\nFree shipping on every order†\n\nFine print:\n† Items priced as pre-order are excluded. Excludes the bedding category.\n* Items priced as clearance are excluded. Eligibility for the benefit is restricted to the toys product category.\n\nLittle ones and grown-ups alike are welcome at Marigold Pets, so bring the crew along.\n\nOrder ORD-506670 placed by Tomas Ferreira:\n- item: SKU-27526\n- product category: pet supplies\n- price status: open box\n- delivery region: Calderon\n- order date: 6 Oct 2026\n- membership level: Green\n- order subtotal: 119.92 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertised terms, which include the headline and its small print, does Tomas Ferreira come with free returns on order ORD-506670?"
 },
 {
  "qid": "q4bac2c4764",
  "kind": "yes/no",
  "text": "Advertisement from Cedarline Living:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nFine print:\n* Customers at the Green tier or lower can use this offer. Subtotal must be strictly above $100.00.\n† Only members at the Blue level or higher may take part.\n\nA step ahead\nWalk into Cedarline Living and discover a shop that knows its craft and takes real pride in its shelves.\n\nOrder ORD-263492 placed by Lena Whitcombe:\n- item: SKU-25508\n- product category: furniture\n- price status: regular price\n- delivery region: Hollin\n- order date: 2026-07-23\n- membership level: Green\n- order subtotal: $114.99",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes Lena Whitcombe get free gift wrapping on order ORD-263492 when the advertised terms, with the headline and its small print, are applied?"
 },
 {
  "qid": "qe73ad0ff7b",
  "kind": "yes/no",
  "text": "Support chat about order ORD-844941:\nLena Whitcombe: Hi, I placed order ORD-844941 on May 30, 2026 for item SKU-72935, and the order subtotal was $91.98.\nAgent: Thanks. The item is in the pet supplies product category, its price status is pre-order, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Platinum.\nLena Whitcombe: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree returns on every purchase*\nFree installation for every appliance†\n\nSimple, sensible, reliable\nOur approach at Juniper Gadgets is plain and steady: good products, clear information and a friendly welcome.\n\nFine print:\n† Stock with final sale status is excluded from this benefit. The order subtotal must be strictly greater than $75.00.\n* Products whose category is sports gear sit outside the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWould you say it is not the case that Lena Whitcombe does not get free returns on order ORD-844941 when the advertisement and its fine print are read?"
 },
 {
  "qid": "q90b81d7255",
  "kind": "choice",
  "text": "Support chat about order ORD-317413:\nInes Duarte: Hi, I placed order ORD-317413 on 25 March 2026 for item SKU-14370, and the order subtotal was $89.55.\nAgent: Thanks. The item is in the pet supplies product category, its price status is open box, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Bronze.\nInes Duarte: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nWe match any lower price*\nFree installation for every appliance†\n\nSubject: A quiet welcome, and a soft hello\nHello, we are glad you stopped by. At Juniper Gadgets we keep the collection calm, carefully chosen and easy to browse at your own pace.\n\nFine print:\n* Products whose category is pet supplies sit outside the headline benefit. Limited to membership at the Silver level or below.\n† Orders submitted on or before 25 March 2026 are accepted. Stock flagged as open box sits outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, if any, of the ad and its small print attached to free installation does order ORD-317413 from Ines Duarte miss?",
  "options": [
   "The product-category condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition",
   "The price-status condition"
  ]
 },
 {
  "qid": "q3e07b0a0a5",
  "kind": "choice",
  "text": "Advertisement from Harborlight Goods:\nDouble reward points on every purchase*\n\nSubject: a calm note about everyday comforts\nHello there,\nHarborlight Goods has thoughtfully chosen everyday essentials for the friends who share your home. Our picks feel soft, sturdy and easy to care for.\nWarm wishes,\n*The order subtotal must be above $50.00. Delivery to Calderon only.\n\nOrder ORD-458905 placed by Jonah Pryce:\n- item: SKU-19953\n- product category: toys\n- price status: pre-order\n- delivery region: Calderon\n- order date: Tuesday, September 15, 2026\n- membership level: Silver\n- order subtotal: $38.26",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Harborlight Goods membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOf the conditions in the small print attached to double reward points, which, if any, does order ORD-458905 from Jonah Pryce miss, according to what the advertisement says?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q64e1ac3311",
  "kind": "choice",
  "text": "Order ORD-489590 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-13931 |\n| product category | kitchenware |\n| price status | pre-order |\n| delivery region | Eskarth |\n| order date | 2026-07-26 |\n| membership level | Premier |\n| order subtotal | 80.73 USD |\n\nAdvertisement from Fernway Market:\nFree assembly with every delivery*\n\nThanks for making Fernway Market part of your routine. Give it a quick shine with a clean cloth, skip harsh cleaners, and enjoy it looking sharp for longer. Thank you for choosing us, and we are glad you are here.\n*Valid for orders placed before 2026-07-26.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the ad's small print attached to free assembly does Ravi Anand's order ORD-489590 miss, if any?",
  "options": [
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q442c7bbf3d",
  "kind": "yes/no",
  "text": "Advertisement from Marigold Pets:\nWe match any lower price*\nDouble reward points on every purchase†\n\nFine print:\n* Items at the open box pricing status sit outside this promotion.\n† Items whose status is refurbished are excluded. The headline benefit stops short of delivery to Dunmere.\n\nStylish, streamlined and straight ahead, that is the vibe at Marigold Pets. Walk in and feel it.\n\nOrder ORD-170823 placed by Felix Moreau:\n- item: SKU-60511\n- product category: furniture\n- price status: pre-order\n- delivery region: Eskarth\n- order date: Thursday, May 28, 2026\n- membership level: Blue\n- order subtotal: 40.55 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, is it true that order ORD-170823 from Felix Moreau does not get double reward points under the advertised terms?"
 },
 {
  "qid": "q59010fc8f9",
  "kind": "choice",
  "text": "Advertisement from Pebblestone Garden:\nA lifetime warranty on everything we sell*\nFree installation for every appliance†\n\nStraight talk and sensible choices define Pebblestone Garden, so come see what we stock.\n\nFine print:\n† The headline benefit stops short of delivery to Greyhaven. Valid for orders placed before February 26, 2026.\n* Covers the toys product category only. Requires membership at Gold or higher.\n\nOrder ORD-778705 placed by Dana Okafor:\n- item: SKU-75700\n- product category: kitchenware\n- price status: pre-order\n- delivery region: Brenmoor\n- order date: April 7, 2026\n- membership level: Silver\n- order subtotal: $210.83",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition in the small print attached to free installation does order ORD-778705 from Dana Okafor miss, if any, given the advertisement and its fine print?",
  "options": [
   "The order-date condition",
   "The membership-level condition",
   "The product-category condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q6c85fb669b",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nKeep it simple at Wrenfield Outdoor, with useful kit and practical help close at hand.\n\nOrder ORD-840091 placed by Felix Moreau:\n- item: SKU-71420\n- product category: garden tools\n- price status: pre-order\n- delivery region: Dunmere\n- order date: 2026-08-22\n- membership level: Platinum\n- order subtotal: 34.99 USD\n\nFine print from the bottom of the advertisement:\n* Delivery to Dunmere only. The subtotal of the order needs to be 35.00 USD or higher.\n† The benefit is reserved for delivery bound for Dunmere. Orders must reach 35.00 USD or more in subtotal.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, is it true that order ORD-840091 from Felix Moreau does not get free shipping?"
 },
 {
  "qid": "qb2a4a85a62",
  "kind": "choice",
  "text": "Advertisement from Marigold Pets:\nFree gift wrapping at checkout*\n\nFine print:\n* Qualifying orders: subtotal $25.00 or more.\n\nHi there, and welcome to the playground at Marigold Pets.\n\nOrder ORD-663633 placed by Felix Moreau:\n- item: SKU-22035\n- product category: garden tools\n- price status: regular price\n- delivery region: Arvale\n- order date: Monday, 9 March 2026\n- membership level: Blue\n- order subtotal: $25.00",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Marigold Pets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nLooking at the advertisement and its fine print, which condition attached to free gift wrapping does customer Felix Moreau, on order ORD-663633, miss, if any?",
  "options": [
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qee6ea84a49",
  "kind": "yes/no",
  "text": "Support chat about order ORD-344699:\nNadia Haddad: Hi, I placed order ORD-344699 on 2026-10-21 for item SKU-42982, and the order subtotal was $169.19.\nAgent: Thanks. The item is in the furniture product category, its price status is regular price, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Black.\nNadia Haddad: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nSurprise yourself\nA small detour to Larkspur Playthings leads to giggles, goofy moments and a grin that sneaks up on you.\n\nFine print:\n* Qualifying orders include the date 2026-10-21 and every later day. Each order needs delivery to Eskarth to earn the benefit.\n† Headline benefit is limited to delivery in Greyhaven.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, and going by what the advertisement says, is it true that order ORD-344699 from Nadia Haddad doesn't get double reward points?"
 },
 {
  "qid": "qa58e59db54",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree returns on every purchase*\nFree gift wrapping at checkout†\n\nWe appreciate your custom at Larkspur Playthings. Look closely at the stitching and tighten loose fixings gently.\n\nFine print:\n* Orders must be placed on or after 8 August 2026. The order subtotal must be strictly greater than 200.00 USD.\n† Eligibility is limited to the kitchenware category. Valid: any order taken on or before 1 August 2026.\n\nOrder ORD-241677 placed by Aiko Brandt:\n- item: SKU-25686\n- product category: sports gear\n- price status: clearance\n- delivery region: Calderon\n- order date: 1 August 2026\n- membership level: Elite\n- order subtotal: 200.01 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the advertised terms, which include the headline and its small print, does Aiko Brandt come with free returns on order ORD-241677?"
 },
 {
  "qid": "qa10a2cf1bc",
  "kind": "choice",
  "text": "Order ORD-515661 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-34204 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | 22 Mar 2026 |\n| membership level | Black |\n| order subtotal | 147.12 USD |\n\nAdvertisement from Brightwell Home:\nFree assembly with every delivery*\nFree returns on every purchase†\n\nFine print:\n* Orders must be placed earlier than 20 Apr 2026.\n† Order by 5 Mar 2026 at the latest.\n\nPsst, your basket is ready to party! Give it a wink and head to the checkout at Brightwell Home.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does order ORD-515661 from Selin Yilmaz truly get, by the terms set out in what the advertisement says?",
  "options": [
   "Both offers",
   "Only free returns",
   "Only free assembly",
   "Neither offer"
  ]
 },
 {
  "qid": "qfc94acc281",
  "kind": "yes/no",
  "text": "Order ORD-366908 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-73414 |\n| product category | bedding |\n| price status | regular price |\n| delivery region | Fallowmere |\n| order date | Sunday, September 6, 2026 |\n| membership level | Plus |\n| order subtotal | 162.85 USD |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\nFree gift wrapping at checkout†\n\nWe are delighted that you chose Copperleaf Kitchen. Please review your basket as you proceed.\n\nFine print:\n* For Plus members and above. The order subtotal must be strictly greater than 150.00 USD.\n† The order date needs to be on or before Monday, August 24, 2026.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-366908 from Selin Yilmaz come with double reward points under what the advertisement says, headline and small print included?"
 },
 {
  "qid": "qa4333c9ce0",
  "kind": "choice",
  "text": "Advertisement from Oakhurst Interiors:\nFree returns on every purchase*\n\nThoughtful, refined and quietly elegant: Oakhurst Interiors is a place for slow, deliberate choices.\n\nFine print:\n* Qualifying orders include the date Wednesday, 17 June 2026 and every later day.\n\nOrder ORD-430391 placed by Priya Raman:\n- item: SKU-80466\n- product category: garden tools\n- price status: regular price\n- delivery region: Brenmoor\n- order date: Tuesday, 16 June 2026\n- membership level: Platinum\n- order subtotal: $227.58",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to free returns does order ORD-430391 from Priya Raman miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition"
  ]
 },
 {
  "qid": "qa6414716ab",
  "kind": "yes/no",
  "text": "Advertisement from Copperleaf Kitchen:\nFree installation for every appliance*\nDouble reward points on every purchase†\n\nFine print:\n† Items with refurbished status fall outside this benefit.\n* The subtotal on the order has to be more than 100.00 USD to count. Delivery to Hollin is the sole route to the headline benefit.\n\nReady to go? Give your cart a glance and enjoy the rest of your visit to Copperleaf Kitchen.\n\nOrder ORD-769078 placed by Aiko Brandt:\n- item: SKU-35081\n- product category: furniture\n- price status: final sale\n- delivery region: Hollin\n- order date: March 13, 2026\n- membership level: Silver\n- order subtotal: 106.03 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the order ORD-769078 from Aiko Brandt against the advertised terms, is it true that it doesn't get free installation?"
 },
 {
  "qid": "q7d429c8b51",
  "kind": "yes/no",
  "text": "Advertisement from Oakhurst Interiors:\nWe match any lower price*\nDouble reward points on every purchase†\n\nLittle hands and big smiles are welcome at Oakhurst Interiors. Head out together and enjoy a pleasant stroll among the displays.\n\nFine print:\n† Valid for orders whose subtotal is $35.00 or more. Orders dated on or before 8 June 2026 count.\n* Every order placed on or after 13 May 2026 is covered by the offer.\n\nOrder ORD-740156 placed by Ravi Anand:\n- item: SKU-25445\n- product category: bedding\n- price status: regular price\n- delivery region: Dunmere\n- order date: 13 May 2026\n- membership level: Bronze\n- order subtotal: $35.00",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-740156 from Ravi Anand get double reward points?"
 },
 {
  "qid": "qbec0b17863",
  "kind": "yes/no",
  "text": "Advertisement from Birchwood Linens:\nFree shipping on every order*\nWe match any lower price†\n\nWelcome to our pages\nThe people at Birchwood Linens have gathered thoughtful pieces that feel right at home.\n\nFine print:\n* An order placed on or before 7 August 2026 qualifies.\n† Applies to orders placed on or after 6 August 2026. The headline benefit is set aside for anything in the bedding category.\n\nOrder ORD-949387 placed by Nadia Haddad:\n- item: SKU-81310\n- product category: sports gear\n- price status: final sale\n- delivery region: Eskarth\n- order date: 17 August 2026\n- membership level: Plus\n- order subtotal: $126.16",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Birchwood Linens levels, lowest to highest: Basic, Plus, Premier and Elite. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, with headline and small print read together, does order ORD-949387 from Nadia Haddad get the price match?"
 },
 {
  "qid": "qa42dff91fc",
  "kind": "choice",
  "text": "Support chat about order ORD-685015:\nOwen Mensah: Hi, I placed order ORD-685015 on March 19, 2026 for item SKU-78662, and the order subtotal was $42.61.\nAgent: Thanks. The item is in the kitchenware product category, its price status is regular price, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Bronze.\nOwen Mensah: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nA lifetime warranty on everything we sell*\nFree gift wrapping at checkout†\n\nPieces that feel right, chosen with care and a steady hand. Explore what is new at Juniper Gadgets.\n\nFine print:\n† Valid on orders of $35.00 or more.\n* An order whose delivery goes to Eskarth falls outside the headline benefit. Applies to members up to Gold or lower.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor the order ORD-685015 placed by Owen Mensah, which of the advertised terms does it actually get when the small print is checked offer by offer?",
  "options": [
   "Both offers",
   "Only the lifetime warranty",
   "Only free gift wrapping",
   "Neither offer"
  ]
 },
 {
  "qid": "q07d38337dc",
  "kind": "yes/no",
  "text": "Support chat about order ORD-858275:\nNadia Haddad: Hi, I placed order ORD-858275 on March 21, 2026 for item SKU-86824, and the order subtotal was 96.24 USD.\nAgent: Thanks. The item is in the pet supplies product category, its price status is regular price, and it ships to the Hollin delivery region.\nAgent: Your membership level is Bronze.\nNadia Haddad: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree assembly with every delivery*\nWe match any lower price†\n\nSubject: So glad you dropped in\nDear visitor, Cedarline Living is delighted to welcome you with a warm smile.\n\nFine print:\n* Placed before April 8, 2026 counts; that very day is excluded. Order subtotal must go beyond $100.\n† Goods in the garden tools category fall outside the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhen the headline and its small print are read against the advertised terms, does order ORD-858275 from Nadia Haddad receive free assembly?"
 },
 {
  "qid": "qf2ba2d32e0",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nWe match any lower price*\nFree assembly with every delivery†\n\nFine print:\n† Applies to orders placed ahead of Friday, February 13, 2026.\n* Valid only for orders delivered to Calderon.\n\nA calm, careful approach suits this piece beautifully. We hope its quiet elegance accompanies you, and thank you for choosing Northvale Audio.\n\nOrder ORD-525733 placed by Jonah Pryce:\n- item: SKU-12794\n- product category: bedding\n- price status: clearance\n- delivery region: Greyhaven\n- order date: Sunday, February 22, 2026\n- membership level: Elite\n- order subtotal: $228.93",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers from the advertisement and its fine print actually reach customer Jonah Pryce on order ORD-525733?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the price match",
   "Only free assembly"
  ]
 },
 {
  "qid": "q4debd365fe",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nFree gift wrapping at checkout*\n\nWe appreciate your visit to Fernway Market. Please glance at the items in your basket and carry on at your own pace.\n\nFine print:\n* Valid only for orders delivered to Brenmoor.\n\nOrder ORD-737408 placed by Selin Yilmaz:\n- item: SKU-56493\n- product category: furniture\n- price status: regular price\n- delivery region: Hollin\n- order date: 2026-04-11\n- membership level: Bronze\n- order subtotal: 99.35 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-737408 from Selin Yilmaz against the advertised terms, which condition in the small print attached to free gift wrapping does it miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q94459c912e",
  "kind": "yes/no",
  "text": "Support chat about order ORD-453516:\nTomas Ferreira: Hi, I placed order ORD-453516 on Sunday, April 12, 2026 for item SKU-74908, and the order subtotal was $204.02.\nAgent: Thanks. The item is in the pet supplies product category, its price status is regular price, and it ships to the Calderon delivery region.\nAgent: Your membership level is Platinum.\nTomas Ferreira: I am asking about the advertisement below.\n\nAdvertisement from Cedarline Living:\nFree assembly with every delivery*\n\nWhatever brings you here, Cedarline Living is glad to have you. Settle in and make yourself at home.\n\nFine print:\n* Headline benefit applies to orders with delivery in Calderon only.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Cedarline Living membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does order ORD-453516 from Tomas Ferreira lose out on free assembly?"
 },
 {
  "qid": "q3bcf817bba",
  "kind": "yes/no",
  "text": "Order ORD-737428 placed by Mira Castell:\n| field | value |\n| --- | --- |\n| item | SKU-38249 |\n| product category | kitchenware |\n| price status | clearance |\n| delivery region | Fallowmere |\n| order date | Friday, 17 July 2026 |\n| membership level | Basic |\n| order subtotal | 234.39 USD |\n\nAdvertisement from Fernway Market:\nFree assembly with every delivery*\nWe match any lower price†\n\nFine print:\n† Orders dated on or before Friday, 17 July 2026 count.\n* Items whose status is clearance are excluded.\n\nMade for living\nBrowse the displays at Fernway Market and pick out pieces that suit the way you live.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement alongside its fine print, does Mira Castell receive free assembly on order ORD-737428?"
 },
 {
  "qid": "qed41f4153c",
  "kind": "yes/no",
  "text": "Order ORD-727061 placed by Hugo Lindqvist:\n| field | value |\n| --- | --- |\n| item | SKU-45309 |\n| product category | pet supplies |\n| price status | open box |\n| delivery region | Hollin |\n| order date | Saturday, 18 July 2026 |\n| membership level | Green |\n| order subtotal | $20.61 |\n\nAdvertisement from Northvale Audio:\nDouble reward points on every purchase*\nWe match any lower price†\n\nTidy it up with a soft cloth once the fun has ended, and store it somewhere cool. We hope Northvale Audio brings smiles to your household.\n\nFine print:\n* Each item bearing the open box status is withheld from the main benefit.\n† Placed before Sunday, 19 July 2026 counts; that very day is excluded. Qualifying orders: subtotal $25 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, and going by what the advertisement says, is it true that order ORD-727061 from Hugo Lindqvist doesn't get double reward points?"
 }
]
