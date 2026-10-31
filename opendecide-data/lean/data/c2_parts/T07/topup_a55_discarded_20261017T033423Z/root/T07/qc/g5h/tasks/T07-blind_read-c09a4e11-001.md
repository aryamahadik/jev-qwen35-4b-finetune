# G5-H blind read T07-blind_read-c09a4e11-001 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T07/topup_a55/root/T07/qc/g5h/answers/T07-blind_read-c09a4e11-001.json

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
  "qid": "q42d2bf05ae",
  "kind": "choice",
  "text": "Advertisement from Northvale Audio:\nFree gift wrapping at checkout*\nA lifetime warranty on everything we sell†\n\n{\"title\": \"Northvale Audio app\", \"subtitle\": \"Browse the range, build a list, and check out quickly\", \"button\": \"Get started\"}\n\nFine print:\n* The benefit is withheld from anything with final sale pricing.\n† The benefit is reserved for delivery bound for Calderon.\n\nOrder ORD-714089 placed by Hugo Lindqvist:\n- item: SKU-84541\n- product category: furniture\n- price status: final sale\n- delivery region: Arvale\n- order date: 17 July 2026\n- membership level: Premier\n- order subtotal: 159.98 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Northvale Audio membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking Hugo Lindqvist's order ORD-714089 against the ad and its small print, which condition attached to the lifetime warranty does it miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qfb734e1178",
  "kind": "choice",
  "text": "Order ORD-952893 placed by Ravi Anand:\n| field | value |\n| --- | --- |\n| item | SKU-47546 |\n| product category | garden tools |\n| price status | open box |\n| delivery region | Dunmere |\n| order date | 16 Apr 2026 |\n| membership level | Plus |\n| order subtotal | 47.10 USD |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nFine print:\n† Items at open box pricing are withheld from this benefit.\n* Headline benefit is limited to delivery in Hollin.\n\nSubject: A warm hello from our team\nDear friend, we love sharing our newest pieces with you at Copperleaf Kitchen.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOf the conditions in the small print attached to free shipping, which, if any, does order ORD-952893 from Ravi Anand miss, according to what the advertisement says?",
  "options": [
   "The price-status condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q6711fec87b",
  "kind": "yes/no",
  "text": "Support chat about order ORD-640330:\nNadia Haddad: Hi, I placed order ORD-640330 on Thursday, 24 September 2026 for item SKU-86417, and the order subtotal was $125.05.\nAgent: Thanks. The item is in the garden tools product category, its price status is regular price, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Green.\nNadia Haddad: I am asking about the advertisement below.\n\nAdvertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree gift wrapping at checkout†\n\nWipe it with a damp cloth and let it air-dry. Thanks for buying from Larkspur Playthings.\n\nFine print:\n† Valid for orders whose subtotal is $25.00 or more.\n* Order by Tuesday, 25 August 2026 at the latest. An order qualifies with a subtotal of $100.00 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that Nadia Haddad's order ORD-640330 does not get double reward points under the advertised terms?"
 },
 {
  "qid": "qf603c40b82",
  "kind": "choice",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\n\nThank you for shopping with Wrenfield Outdoor. Take a cheerful peek at your basket and check out.\n\nFine print:\n* Shoppers may place orders on Sunday, June 7, 2026 itself and on every day before it. Delivery to Fallowmere sits outside the headline benefit.\n\nOrder ORD-634375 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-28799 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Dunmere |\n| order date | Monday, June 8, 2026 |\n| membership level | Platinum |\n| order subtotal | $118.97 |",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Wrenfield Outdoor levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to free shipping does order ORD-634375 from Ines Duarte miss, if any?",
  "options": [
   "The delivery-region condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q49b3c5b018",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree shipping on every order†\n\nSubject: Straightforward shopping\nHello, we like plain speaking, so here it is: Larkspur Playthings keeps the essentials stocked and easy to find.\n\nOrder ORD-396338 placed by Mira Castell:\n- item: SKU-22062\n- product category: toys\n- price status: clearance\n- delivery region: Calderon\n- order date: August 24, 2026\n- membership level: Elite\n- order subtotal: $190.46\n\nFine print from the bottom of the advertisement:\n† Any delivery to Greyhaven is excluded from this offer. Orders dated on or before August 24, 2026 count.\n* Anything with delivery in Calderon is excluded from the headline benefit.\n\nNote added by the customer: Mira Castell hopes the matter can be sorted out kindly, since the offer was clearly what drew this purchase in the beginning.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says, with its headline and small print together, does order ORD-396338 from Mira Castell receive free shipping?"
 },
 {
  "qid": "q49c8679bf4",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\nWe match any lower price†\n\nGet cozy at Wrenfield Outdoor, the friendliest corner of the internet.\n\nFine print:\n† Shoppers get the headline benefit solely for delivery in Greyhaven. Minimum order subtotal: $50.\n* For members at Silver or lower. Orders headed for delivery in Greyhaven are kept out of this offer.\n\nOrder ORD-884374 placed by Owen Mensah:\n- item: SKU-79560\n- product category: kitchenware\n- price status: regular price\n- delivery region: Greyhaven\n- order date: 11 Aug 2026\n- membership level: Silver\n- order subtotal: $35.16",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-884374 from Owen Mensah forfeit the price match under the advertised terms, as those terms are written?"
 },
 {
  "qid": "q2eeb6bd888",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nWe match any lower price*\nFree returns on every purchase†\n\nFine print:\n† Items marked with the pre-order status fall outside the benefit set out here.\n* Products assigned to the sports gear category are excluded.\n\nHappy shopping, families! Brightwell Home hopes your basket brings smiles to the house.\n\nOrder ORD-731651 placed by Tomas Ferreira:\n- item: SKU-83517\n- product category: sports gear\n- price status: pre-order\n- delivery region: Dunmere\n- order date: Sunday, August 16, 2026\n- membership level: Plus\n- order subtotal: $153.22",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does Tomas Ferreira actually get on order ORD-731651 when the ad and its small print have been applied offer by offer?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the price match",
   "Only free returns"
  ]
 },
 {
  "qid": "q7b241abe27",
  "kind": "choice",
  "text": "Support chat about order ORD-649753:\nFelix Moreau: Hi, I placed order ORD-649753 on June 12, 2026 for item SKU-11189, and the order subtotal was $71.75.\nAgent: Thanks. The item is in the electronics product category, its price status is clearance, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Plus.\nFelix Moreau: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\nSubject: Little hands, big smiles\nHello, here at Oakhurst Interiors we love seeing tiny hands explore and big smiles spread across faces.\n\nFine print:\n† Orders must be placed before July 15, 2026, and the day itself is excluded. Requires membership at Elite or higher.\n* Members at the Plus level or higher only. Valid for orders whose subtotal is $75 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, if any, of the ad and its small print attached to free gift wrapping does order ORD-649753 from Felix Moreau miss?",
  "options": [
   "The order-subtotal condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition"
  ]
 },
 {
  "qid": "qb380d6188c",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nSubject: simple ways to enjoy better sound\nHello there,\nKestrel Outfitters helps your everyday listening sound clearer. Our speakers, headphones and cables are chosen for dependable performance. Setup is straightforward, so start enjoying the music.\nTake care,\n*Valid for orders placed on or before 25 April 2026. Members at the Black level or higher only.\n\nOrder ORD-123036 placed by Felix Moreau:\n- item: SKU-15618\n- product category: electronics\n- price status: regular price\n- delivery region: Fallowmere\n- order date: 25 March 2026\n- membership level: Black\n- order subtotal: $238.11",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-123036 from Felix Moreau come with the lifetime warranty under what the advertisement says, headline and small print included?"
 },
 {
  "qid": "qc0b62839f7",
  "kind": "choice",
  "text": "Order ORD-989604 placed by Priya Raman:\n| field | value |\n| --- | --- |\n| item | SKU-63727 |\n| product category | toys |\n| price status | clearance |\n| delivery region | Greyhaven |\n| order date | March 20, 2026 |\n| membership level | Green |\n| order subtotal | $97.04 |\n\nAdvertisement from Brightwell Home:\nFree assembly with every delivery*\nA lifetime warranty on everything we sell†\n\nWelcome to our pages\nThe people at Brightwell Home have gathered thoughtful pieces that feel right at home.\n\nFine print:\n* Excludes the sports gear category. Any item whose status is clearance falls outside this offer.\n† Shoppers get the headline benefit solely for delivery in Greyhaven.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does customer Priya Raman on order ORD-989604 truly receive, given what the advertisement says?",
  "options": [
   "Both offers",
   "Only free assembly",
   "Only the lifetime warranty",
   "Neither offer"
  ]
 },
 {
  "qid": "qceac441980",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree returns on every purchase*\nWe match any lower price†\n\nFine print:\n† An order placed on or before 12 July 2026 qualifies. For members at Plus or lower.\n* Placed before 6 June 2026 counts; that very day is excluded.\n\nGood coffee, good company and a little bit of fun at Brightwell Home. Pop by and see what we have been up to.\n\nOrder ORD-749086 placed by Lena Whitcombe:\n- item: SKU-10235\n- product category: toys\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 12 July 2026\n- membership level: Premier\n- order subtotal: 47.27 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, which condition attached to the price match does order ORD-749086 from Lena Whitcombe miss, if any?",
  "options": [
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition"
  ]
 },
 {
  "qid": "q4317caf507",
  "kind": "yes/no",
  "text": "Advertisement from Bluecrest Sports:\nDouble reward points on every purchase*\nFree returns on every purchase†\n\nFine print:\n* Any order placed on September 2, 2026 and beyond is accepted. Items at the final sale pricing status sit outside this promotion.\n† Each item bearing the pre-order status is withheld from the main benefit.\n\nSubject: Tidy layout, simple search\nHello, the crisp design of Bluecrest Sports keeps the range in clear view and within easy grasp.\n\nOrder ORD-165332 placed by Lena Whitcombe:\n- item: SKU-70010\n- product category: bedding\n- price status: pre-order\n- delivery region: Greyhaven\n- order date: September 2, 2026\n- membership level: Black\n- order subtotal: $178.72",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Bluecrest Sports levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad and its small print say that order ORD-165332 from Lena Whitcombe gets double reward points?"
 },
 {
  "qid": "q79cee2841b",
  "kind": "choice",
  "text": "Support chat about order ORD-247693:\nDana Okafor: Hi, I placed order ORD-247693 on 31 March 2026 for item SKU-61547, and the order subtotal was $100.00.\nAgent: Thanks. The item is in the sports gear product category, its price status is open box, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Premier.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\nSubject: Little hands, big smiles\nHello, here at Oakhurst Interiors we love seeing tiny hands explore and big smiles spread across faces.\n\nFine print:\n† Orders must be placed before 16 April 2026, and the day itself is excluded. Requires membership at Premier or higher.\n* Members at the Premier level or higher only. Valid for orders whose subtotal is $100.00 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, if any, of the ad and its small print attached to free gift wrapping does order ORD-247693 from Dana Okafor miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The membership-level condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q133edae572",
  "kind": "yes/no",
  "text": "Advertisement from Kestrel Outfitters:\nA lifetime warranty on everything we sell*\n\nSubject: simple ways to enjoy better sound\nHello there,\nKestrel Outfitters helps your everyday listening sound clearer. Our speakers, headphones and cables are chosen for dependable performance. Setup is straightforward, so start enjoying the music.\nTake care,\n*Valid for orders placed on or before 26 Aug 2026. Members at the Blue level or higher only.\n\nOrder ORD-942232 placed by Clara Voss:\n- item: SKU-14508\n- product category: sports gear\n- price status: open box\n- delivery region: Fallowmere\n- order date: 11 Sep 2026\n- membership level: Blue\n- order subtotal: 244.44 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Kestrel Outfitters membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-942232 from Clara Voss come with the lifetime warranty under what the advertisement says, headline and small print included?"
 },
 {
  "qid": "qb626dad7ea",
  "kind": "yes/no",
  "text": "Order ORD-458829 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-76429 |\n| product category | furniture |\n| price status | final sale |\n| delivery region | Arvale |\n| order date | 12 July 2026 |\n| membership level | Black |\n| order subtotal | $207.01 |\n\nAdvertisement from Tidewell Supply:\nA lifetime warranty on everything we sell*\nFree shipping on every order†\n\nSubject: Elevated living, simply expressed\nDear friend, Tidewell Supply brings sophisticated taste to the home, with pieces that hold their own.\n\nFine print:\n* Delivery to Arvale sits outside the headline benefit. Valid for orders placed before 7 July 2026.\n† Only the kitchenware category earns the headline benefit. Orders headed for delivery in Dunmere are kept out of this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does the order ORD-458829 placed by Aiko Brandt forfeit free shipping, as what the advertisement says indicates?"
 },
 {
  "qid": "qab01c77b85",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree returns on every purchase*\nWe match any lower price†\n\nFine print:\n† An order placed on or before 12 July 2026 qualifies. For members at Plus or lower.\n* Placed before 6 June 2026 counts; that very day is excluded.\n\nGood coffee, good company and a little bit of fun at Brightwell Home. Pop by and see what we have been up to.\n\nOrder ORD-749086 placed by Lena Whitcombe:\n- item: SKU-10235\n- product category: toys\n- price status: regular price\n- delivery region: Brenmoor\n- order date: 12 July 2026\n- membership level: Plus\n- order subtotal: 47.27 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, which condition attached to the price match does order ORD-749086 from Lena Whitcombe miss, if any?",
  "options": [
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer",
   "The membership-level condition"
  ]
 },
 {
  "qid": "q48acb7c820",
  "kind": "choice",
  "text": "Order ORD-117429 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-40679 |\n| product category | furniture |\n| price status | final sale |\n| delivery region | Eskarth |\n| order date | 4 March 2026 |\n| membership level | Blue |\n| order subtotal | 115.08 USD |\n\nAdvertisement from Northvale Audio:\nWe match any lower price*\nFree gift wrapping at checkout†\n\nCome for a chat, stay for the cosy corners, and leave with a little treasure from Northvale Audio.\n\nFine print:\n* The benefit is reserved for delivery bound for Fallowmere.\n† Anything filed under the furniture category sits outside this offer.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Northvale Audio levels, lowest to highest: Green, Blue and Black. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nFor order ORD-117429 placed by Aiko Brandt, which headline offers does the advertisement and its fine print actually allow, offer by offer?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the price match",
   "Only free gift wrapping"
  ]
 },
 {
  "qid": "qbd9660e149",
  "kind": "choice",
  "text": "Advertisement from Pebblestone Garden:\nFree assembly with every delivery*\n\nFine print:\n* An order placed on or before 5 Oct 2026 qualifies. Members at Platinum and above only.\n\nA quiet welcome awaits at Pebblestone Garden, where considered pieces are arranged with care.\n\nOrder ORD-574557 placed by Ines Duarte:\n- item: SKU-95545\n- product category: sports gear\n- price status: open box\n- delivery region: Greyhaven\n- order date: 5 Oct 2026\n- membership level: Gold\n- order subtotal: 39.49 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Pebblestone Garden membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, which condition in the small print attached to free assembly does order ORD-574557 from Ines Duarte miss, if any?",
  "options": [
   "The order-date condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qa045dbaaf0",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree shipping on every order†\n\nSubject: Straightforward shopping\nHello, we like plain speaking, so here it is: Larkspur Playthings keeps the essentials stocked and easy to find.\n\nOrder ORD-224962 placed by Dana Okafor:\n- item: SKU-33122\n- product category: garden tools\n- price status: regular price\n- delivery region: Dunmere\n- order date: Monday, 27 April 2026\n- membership level: Premier\n- order subtotal: $201.32\n\nFine print from the bottom of the advertisement:\n† Any delivery to Calderon is excluded from this offer. Orders dated on or before Saturday, 11 April 2026 count.\n* Anything with delivery in Calderon is excluded from the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says, with its headline and small print together, does order ORD-224962 from Dana Okafor receive free shipping?"
 },
 {
  "qid": "q8b290a0645",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\nWe match any lower price†\n\nGet cozy at Wrenfield Outdoor, the friendliest corner of the internet.\n\nFine print:\n† Shoppers get the headline benefit solely for delivery in Arvale. Minimum order subtotal: 35.00 USD.\n* For members at Bronze or lower. Orders headed for delivery in Dunmere are kept out of this offer.\n\nOrder ORD-541695 placed by Lena Whitcombe:\n- item: SKU-59315\n- product category: pet supplies\n- price status: refurbished\n- delivery region: Arvale\n- order date: 2026-06-23\n- membership level: Platinum\n- order subtotal: 34.99 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-541695 from Lena Whitcombe forfeit the price match under the advertised terms, as those terms are written?"
 },
 {
  "qid": "q9332237ccd",
  "kind": "choice",
  "text": "Order ORD-111241 placed by Lena Whitcombe:\n| field | value |\n| --- | --- |\n| item | SKU-80947 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Brenmoor |\n| order date | 2026-10-19 |\n| membership level | Blue |\n| order subtotal | $27.82 |\n\nAdvertisement from Brightwell Home:\nFree assembly with every delivery*\n\nFine print:\n* Order subtotal must go beyond $35. Headline benefit is limited to delivery in Brenmoor.\n\nThank you for bringing this lovely item into your family at Brightwell Home. Please read the care tips and place this note with the product.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, which condition attached to free assembly does order ORD-111241 from Lena Whitcombe miss, if any?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q2807731273",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\nWe match any lower price†\n\nGet cozy at Wrenfield Outdoor, the friendliest corner of the internet.\n\nFine print:\n† Shoppers get the headline benefit solely for delivery in Arvale. Minimum order subtotal: 35.00 USD.\n* For members at Bronze or lower. Orders headed for delivery in Dunmere are kept out of this offer.\n\nOrder ORD-541695 placed by Lena Whitcombe:\n- item: SKU-59315\n- product category: pet supplies\n- price status: refurbished\n- delivery region: Arvale\n- order date: 2026-06-23\n- membership level: Platinum\n- order subtotal: 35.00 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-541695 from Lena Whitcombe forfeit the price match under the advertised terms, as those terms are written?"
 },
 {
  "qid": "qc5c65a3f1a",
  "kind": "choice",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\n\nWrenfield Outdoor, measured and poised\nA gracious setting to linger and admire the craftsmanship.\n\nFine print:\n* Shoppers may place orders on August 4, 2026 itself and on every day before it. Delivery to Hollin sits outside the headline benefit.\n\nOrder ORD-841351 placed by Kofi Asante:\n- item: SKU-35026\n- product category: toys\n- price status: pre-order\n- delivery region: Arvale\n- order date: July 5, 2026\n- membership level: Platinum\n- order subtotal: 231.18 USD",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Wrenfield Outdoor levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to free shipping does order ORD-841351 from Kofi Asante miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q2d86090e9f",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\n\nSubject: A standard built to endure\nHello, the cut and finish on show at Juniper Gadgets is confident and clean.\n\nFine print:\n* Only the garden tools category earns the headline benefit. Stock with final sale status is excluded from this benefit.\n\nOrder ORD-933578 placed by Jonah Pryce:\n- item: SKU-79572\n- product category: garden tools\n- price status: final sale\n- delivery region: Brenmoor\n- order date: 29 May 2026\n- membership level: Green\n- order subtotal: 17.10 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, does order ORD-933578 from Jonah Pryce fail to get free gift wrapping under the advertised terms?"
 },
 {
  "qid": "q57630bd0e3",
  "kind": "choice",
  "text": "Support chat about order ORD-247693:\nDana Okafor: Hi, I placed order ORD-247693 on 16 April 2026 for item SKU-61547, and the order subtotal was $100.00.\nAgent: Thanks. The item is in the sports gear product category, its price status is open box, and it ships to the Dunmere delivery region.\nAgent: Your membership level is Premier.\nDana Okafor: I am asking about the advertisement below.\n\nAdvertisement from Oakhurst Interiors:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\nSubject: Little hands, big smiles\nHello, here at Oakhurst Interiors we love seeing tiny hands explore and big smiles spread across faces.\n\nFine print:\n† Orders must be placed before 16 April 2026, and the day itself is excluded. Requires membership at Premier or higher.\n* Members at the Premier level or higher only. Valid for orders whose subtotal is $100.00 or more.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Oakhurst Interiors membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich condition, if any, of the ad and its small print attached to free gift wrapping does order ORD-247693 from Dana Okafor miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition",
   "The membership-level condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "qcb91b34af1",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nWander around Tidewell Supply at your own pace and see what makes us giggle.\n\nOrder ORD-804134 placed by Tomas Ferreira:\n- item: SKU-93863\n- product category: furniture\n- price status: refurbished\n- delivery region: Fallowmere\n- order date: August 24, 2026\n- membership level: Premier\n- order subtotal: $232.34\n\nFine print from the bottom of the advertisement:\n* Items in the furniture product category are excluded. For members at Premier or lower.\n† Items under the kitchenware category are carved out of this offer. Any item whose status is clearance falls outside this offer.\n\nNote added by the customer: Tomas Ferreira argues that a parcel arriving only a little later than the promised window is close enough, so the deal still holds.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-804134 placed by Tomas Ferreira lose out on the price match?"
 },
 {
  "qid": "q0aed493b40",
  "kind": "yes/no",
  "text": "Advertisement from Juniper Gadgets:\nFree gift wrapping at checkout*\n\nSubject: A standard built to endure\nHello, the cut and finish on show at Juniper Gadgets is confident and clean.\n\nFine print:\n* Only the kitchenware category earns the headline benefit. Stock with clearance status is excluded from this benefit.\n\nOrder ORD-900022 placed by Tomas Ferreira:\n- item: SKU-17252\n- product category: toys\n- price status: refurbished\n- delivery region: Greyhaven\n- order date: 26 August 2026\n- membership level: Black\n- order subtotal: 208.91 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Juniper Gadgets membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nBased on what the advertisement says, does order ORD-900022 from Tomas Ferreira fail to get free gift wrapping under the advertised terms?"
 },
 {
  "qid": "qbb3c7ac43e",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree installation for every appliance†\n\nWelcome back to Larkspur Playthings. Your basket is ready and waiting for a closer glance.\n\nFine print:\n† Membership level Plus or lower required. Anything with delivery in Hollin is excluded from the headline benefit.\n* Only members at the Premier level or higher may take part. Only a delivery to Calderon qualifies for this offer.\n\nOrder ORD-946397 placed by Felix Moreau:\n- item: SKU-73502\n- product category: kitchenware\n- price status: regular price\n- delivery region: Hollin\n- order date: Monday, August 31, 2026\n- membership level: Premier\n- order subtotal: 128.40 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking the advertisement and its fine print into account, has order ORD-946397 from Felix Moreau lost out on double reward points?"
 },
 {
  "qid": "q4063f31c77",
  "kind": "yes/no",
  "text": "Support chat about order ORD-855361:\nSelin Yilmaz: Hi, I placed order ORD-855361 on Saturday, 5 September 2026 for item SKU-43067, and the order subtotal was 188.71 USD.\nAgent: Thanks. The item is in the kitchenware product category, its price status is refurbished, and it ships to the Calderon delivery region.\nAgent: Your membership level is Silver.\nSelin Yilmaz: I am asking about the advertisement below.\n\nAdvertisement from Juniper Gadgets:\nFree installation for every appliance*\n\nHello neighbour, pop by Juniper Gadgets for a chat and a look around.\n\nFine print:\n* Valid: any order taken on or before Thursday, 3 September 2026.",
  "question": "A headline holds for an order exactly when the order meets all the fine print under its symbol; other fine print is ignored. Dates mean order dates and amounts mean order subtotals. Juniper Gadgets levels, lowest to highest: Bronze, Silver, Gold and Platinum. Notes from customers or staff change no terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-855361 placed by Selin Yilmaz doesn't get free installation under the advertised terms, based on the advertisement and its fine print?"
 },
 {
  "qid": "qc936990c8a",
  "kind": "yes/no",
  "text": "Order ORD-428038 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-11164 |\n| product category | kitchenware |\n| price status | refurbished |\n| delivery region | Hollin |\n| order date | 28 October 2026 |\n| membership level | Bronze |\n| order subtotal | 79.87 USD |\n\nAdvertisement from Bluecrest Sports:\nDouble reward points on every purchase*\n\nStylish, streamlined and straight ahead, that is the vibe at Bluecrest Sports. Walk in and feel it.\n\nFine print:\n* Every order placed on or after 2 October 2026 is covered by the offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading the advertisement and its fine print, does order ORD-428038 from Clara Voss lose out on double reward points?"
 },
 {
  "qid": "q014c878eef",
  "kind": "choice",
  "text": "Order ORD-232564 placed by Hugo Lindqvist:\n| field | value |\n| --- | --- |\n| item | SKU-54549 |\n| product category | garden tools |\n| price status | open box |\n| delivery region | Calderon |\n| order date | Friday, July 3, 2026 |\n| membership level | Plus |\n| order subtotal | $171.49 |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nFine print:\n† Items at open box pricing are withheld from this benefit.\n* Headline benefit is limited to delivery in Calderon.\n\nSubject: A warm hello from our team\nDear friend, we love sharing our newest pieces with you at Copperleaf Kitchen.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOf the conditions in the small print attached to free shipping, which, if any, does order ORD-232564 from Hugo Lindqvist miss, according to what the advertisement says?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q9396315ffe",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree shipping on every order*\n\nFine print:\n* The order subtotal must be above $75.00. Delivery to Hollin sits outside the headline benefit.\n\nStep right in\nBrisk service, modern style and a lively edge make Brightwell Home worth a visit.\n\nOrder ORD-510270 placed by Aiko Brandt:\n- item: SKU-41250\n- product category: bedding\n- price status: final sale\n- delivery region: Brenmoor\n- order date: Thursday, 16 July 2026\n- membership level: Basic\n- order subtotal: $69.64",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nTaking order ORD-510270 from Aiko Brandt against the advertised terms, which condition in the small print attached to free shipping does it miss, if any?",
  "options": [
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "qbce19acb85",
  "kind": "choice",
  "text": "Advertisement from Wrenfield Outdoor:\nFree installation for every appliance*\n\nSubject: Hello from your local shop\nHi there,\nWrenfield Outdoor is your small neighbourhood shop, and we love helping furry friends feel at home. Drop by for a chat and a friendly face. We are so glad you are part of our little community.\n*The order subtotal must be above 200.00 USD. Excludes items with refurbished status.\n\nOrder ORD-608272 placed by Ravi Anand:\n- item: SKU-93161\n- product category: electronics\n- price status: open box\n- delivery region: Fallowmere\n- order date: 23 March 2026\n- membership level: Silver\n- order subtotal: 207.64 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIf any, which condition in the advertisement and its fine print attached to free installation does order ORD-608272 from Ravi Anand miss?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The order-subtotal condition",
   "The price-status condition"
  ]
 },
 {
  "qid": "qe4a7df6dfd",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree shipping on every order†\n\nSubject: Straightforward shopping\nHello, we like plain speaking, so here it is: Larkspur Playthings keeps the essentials stocked and easy to find.\n\nOrder ORD-224962 placed by Dana Okafor:\n- item: SKU-33122\n- product category: garden tools\n- price status: regular price\n- delivery region: Dunmere\n- order date: Monday, 27 April 2026\n- membership level: Premier\n- order subtotal: $201.32\n\nFine print from the bottom of the advertisement:\n† Any delivery to Calderon is excluded from this offer. Orders dated on or before Saturday, 11 April 2026 count.\n* Anything with delivery in Calderon is excluded from the headline benefit.\n\nNote added by the customer: The shop always makes exceptions for people who come back again and again, so Dana Okafor argues the offer is meant for orders such as this.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nReading what the advertisement says, with its headline and small print together, does order ORD-224962 from Dana Okafor receive free shipping?"
 },
 {
  "qid": "q9588aa1cee",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nWe match any lower price*\nFree returns on every purchase†\n\nFine print:\n† Items marked with the refurbished status fall outside the benefit set out here.\n* Products assigned to the furniture category are excluded.\n\nHappy shopping, families! Brightwell Home hopes your basket brings smiles to the house.\n\nOrder ORD-837293 placed by Jonah Pryce:\n- item: SKU-79411\n- product category: garden tools\n- price status: final sale\n- delivery region: Brenmoor\n- order date: Friday, 9 October 2026\n- membership level: Plus\n- order subtotal: 207.16 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does Jonah Pryce actually get on order ORD-837293 when the ad and its small print have been applied offer by offer?",
  "options": [
   "Neither offer",
   "Only free returns",
   "Both offers",
   "Only the price match"
  ]
 },
 {
  "qid": "q8b5ca02b5b",
  "kind": "yes/no",
  "text": "Order ORD-799464 placed by Selin Yilmaz:\n| field | value |\n| --- | --- |\n| item | SKU-86015 |\n| product category | kitchenware |\n| price status | clearance |\n| delivery region | Fallowmere |\n| order date | Friday, 10 April 2026 |\n| membership level | Bronze |\n| order subtotal | 131.99 USD |\n\nAdvertisement from Bluecrest Sports:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nFine print:\n* Valid: any order taken on or before Sunday, 26 April 2026.\n† Valid for orders placed from Monday, 30 March 2026 onward. Reserved for members at Bronze or below.\n\nCrafted to endure\nWe are proud to present Bluecrest Sports, a house of considered design and enduring materials.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does order ORD-799464 from Selin Yilmaz lose out on free gift wrapping?"
 },
 {
  "qid": "qce65bf91d2",
  "kind": "choice",
  "text": "Order ORD-559076 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-37604 |\n| product category | garden tools |\n| price status | clearance |\n| delivery region | Fallowmere |\n| order date | 14 Oct 2026 |\n| membership level | Black |\n| order subtotal | 28.77 USD |\n\nAdvertisement from Brightwell Home:\nFree assembly with every delivery*\n\nFine print:\n* Order subtotal must go beyond 25.00 USD. Headline benefit is limited to delivery in Dunmere.\n\nThank you for bringing this lovely item into your family at Brightwell Home. Please read the care tips and place this note with the product.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, which condition attached to free assembly does order ORD-559076 from Tomas Ferreira miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q17d8d3822b",
  "kind": "yes/no",
  "text": "Advertisement from Tidewell Supply:\nFree gift wrapping at checkout*\nWe match any lower price†\n\nWander around Tidewell Supply at your own pace and see what makes us giggle.\n\nOrder ORD-354384 placed by Ines Duarte:\n- item: SKU-89814\n- product category: bedding\n- price status: pre-order\n- delivery region: Calderon\n- order date: July 9, 2026\n- membership level: Premier\n- order subtotal: $184.68\n\nFine print from the bottom of the advertisement:\n* Items in the bedding product category are excluded. For members at Premier or lower.\n† Items under the sports gear category are carved out of this offer. Any item whose status is final sale falls outside this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement's conditions in general, does order ORD-354384 placed by Ines Duarte lose out on the price match?"
 },
 {
  "qid": "qf65c21d743",
  "kind": "choice",
  "text": "Order ORD-519659 placed by Nadia Haddad:\n| field | value |\n| --- | --- |\n| item | SKU-49561 |\n| product category | toys |\n| price status | pre-order |\n| delivery region | Dunmere |\n| order date | April 9, 2026 |\n| membership level | Blue |\n| order subtotal | $73.12 |\n\nAdvertisement from Brightwell Home:\nFree assembly with every delivery*\nA lifetime warranty on everything we sell†\n\nWelcome to our pages\nThe people at Brightwell Home have gathered thoughtful pieces that feel right at home.\n\nFine print:\n* Excludes the garden tools category. Any item whose status is pre-order falls outside this offer.\n† Shoppers get the headline benefit solely for delivery in Dunmere.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich headline offers does customer Nadia Haddad on order ORD-519659 truly receive, given what the advertisement says?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the lifetime warranty",
   "Only free assembly"
  ]
 },
 {
  "qid": "q76892ccd0e",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nFree installation for every appliance*\nFree shipping on every order†\n\nSubject: Straightforward shopping\nHello, we like plain speaking, so here it is: Larkspur Playthings keeps the essentials stocked and easy to find.\n\nOrder ORD-396338 placed by Mira Castell:\n- item: SKU-22062\n- product category: toys\n- price status: clearance\n- delivery region: Calderon\n- order date: August 24, 2026\n- membership level: Elite\n- order subtotal: $190.46\n\nFine print from the bottom of the advertisement:\n† Any delivery to Greyhaven is excluded from this offer. Orders dated on or before August 24, 2026 count.\n* Anything with delivery in Calderon is excluded from the headline benefit.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIs it true that order ORD-396338 placed by Mira Castell doesn't get free shipping under the advertised terms, based on the ad and its small print?"
 },
 {
  "qid": "qe48f9963e6",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nWe match any lower price*\nFree returns on every purchase†\n\nFine print:\n† Items marked with the refurbished status fall outside the benefit set out here.\n* Products assigned to the furniture category are excluded.\n\nHappy shopping, families! Brightwell Home hopes your basket brings smiles to the house.\n\nOrder ORD-837293 placed by Jonah Pryce:\n- item: SKU-79411\n- product category: furniture\n- price status: final sale\n- delivery region: Brenmoor\n- order date: Friday, 9 October 2026\n- membership level: Plus\n- order subtotal: 207.16 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does Jonah Pryce actually get on order ORD-837293 when the ad and its small print have been applied offer by offer?",
  "options": [
   "Neither offer",
   "Only free returns",
   "Both offers",
   "Only the price match"
  ]
 },
 {
  "qid": "q89e2f20d83",
  "kind": "yes/no",
  "text": "Order ORD-370943 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-22347 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | September 17, 2026 |\n| membership level | Gold |\n| order subtotal | $182.55 |\n\nAdvertisement from Bluecrest Sports:\nDouble reward points on every purchase*\n\nStylish, streamlined and straight ahead, that is the vibe at Bluecrest Sports. Walk in and feel it.\n\nFine print:\n* Every order placed on or after September 17, 2026 is covered by the offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad, with its small print taken into account, mean that Ines Duarte earns double reward points on order ORD-370943?"
 },
 {
  "qid": "qad097c02bc",
  "kind": "yes/no",
  "text": "Advertisement from Larkspur Playthings:\nDouble reward points on every purchase*\nFree installation for every appliance†\n\nWelcome back to Larkspur Playthings. Your basket is ready and waiting for a closer glance.\n\nFine print:\n† Membership level Plus or lower required. Anything with delivery in Hollin is excluded from the headline benefit.\n* Only members at the Premier level or higher may take part. Only a delivery to Calderon qualifies for this offer.\n\nOrder ORD-946397 placed by Felix Moreau:\n- item: SKU-73502\n- product category: kitchenware\n- price status: regular price\n- delivery region: Hollin\n- order date: Monday, August 31, 2026\n- membership level: Premier\n- order subtotal: 128.40 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Larkspur Playthings membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes Felix Moreau get double reward points on order ORD-946397 when the advertised terms, with the headline and its small print, are applied?"
 },
 {
  "qid": "q967dbc9fe0",
  "kind": "yes/no",
  "text": "Order ORD-428038 placed by Clara Voss:\n| field | value |\n| --- | --- |\n| item | SKU-11164 |\n| product category | kitchenware |\n| price status | refurbished |\n| delivery region | Hollin |\n| order date | 28 October 2026 |\n| membership level | Bronze |\n| order subtotal | 79.87 USD |\n\nAdvertisement from Bluecrest Sports:\nDouble reward points on every purchase*\n\nStylish, streamlined and straight ahead, that is the vibe at Bluecrest Sports. Walk in and feel it.\n\nFine print:\n* Every order placed on or after 2 October 2026 is covered by the offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad, with its small print taken into account, mean that Clara Voss earns double reward points on order ORD-428038?"
 },
 {
  "qid": "qd179a814fb",
  "kind": "choice",
  "text": "Order ORD-559076 placed by Tomas Ferreira:\n| field | value |\n| --- | --- |\n| item | SKU-37604 |\n| product category | garden tools |\n| price status | clearance |\n| delivery region | Dunmere |\n| order date | 14 Oct 2026 |\n| membership level | Black |\n| order subtotal | 28.77 USD |\n\nAdvertisement from Brightwell Home:\nFree assembly with every delivery*\n\nFine print:\n* Order subtotal must go beyond 25.00 USD. Headline benefit is limited to delivery in Dunmere.\n\nThank you for bringing this lovely item into your family at Brightwell Home. Please read the care tips and place this note with the product.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, which condition attached to free assembly does order ORD-559076 from Tomas Ferreira miss, if any?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The delivery-region condition",
   "The order-subtotal condition"
  ]
 },
 {
  "qid": "q60e40b369a",
  "kind": "yes/no",
  "text": "Order ORD-370943 placed by Ines Duarte:\n| field | value |\n| --- | --- |\n| item | SKU-22347 |\n| product category | kitchenware |\n| price status | regular price |\n| delivery region | Eskarth |\n| order date | September 17, 2026 |\n| membership level | Gold |\n| order subtotal | $182.55 |\n\nAdvertisement from Bluecrest Sports:\nDouble reward points on every purchase*\n\nStylish, streamlined and straight ahead, that is the vibe at Bluecrest Sports. Walk in and feel it.\n\nFine print:\n* Every order placed on or after October 10, 2026 is covered by the offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes the ad, with its small print taken into account, mean that Ines Duarte earns double reward points on order ORD-370943?"
 },
 {
  "qid": "q31750e58e8",
  "kind": "choice",
  "text": "Support chat about order ORD-799145:\nInes Duarte: Hi, I placed order ORD-799145 on September 14, 2026 for item SKU-60688, and the order subtotal was $244.31.\nAgent: Thanks. The item is in the pet supplies product category, its price status is clearance, and it ships to the Fallowmere delivery region.\nAgent: Your membership level is Elite.\nInes Duarte: I am asking about the advertisement below.\n\nAdvertisement from Wrenfield Outdoor:\nFree shipping on every order*\nFree returns on every purchase†\n\nPopping by from the corner, Wrenfield Outdoor says hi\nYour neighbourhood favourite, stocked with care.\n\nFine print:\n† Any order placed on September 8, 2026 and beyond is accepted. The headline benefit is set aside for anything in the pet supplies category.\n* Any order placed on September 15, 2026 and beyond is accepted. Limited to members at the Premier level or lower.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nChecking the ad, which small-print condition attached to free returns does order ORD-799145 from Ines Duarte miss, if any?",
  "options": [
   "The product-category condition",
   "The membership-level condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qb12c499d50",
  "kind": "yes/no",
  "text": "Support chat about order ORD-826536:\nHugo Lindqvist: Hi, I placed order ORD-826536 on 2026-07-08 for item SKU-29761, and the order subtotal was $29.76.\nAgent: Thanks. The item is in the sports gear product category, its price status is clearance, and it ships to the Brenmoor delivery region.\nAgent: Your membership level is Green.\nHugo Lindqvist: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\n\nOur doors are wide and our kettle is warm at Birchwood Linens, so please come and sit down for a bit.\n\nFine print:\n* Customers must spend at least $35.00 on the order subtotal. Valid for orders placed from 2026-07-08 onward.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-826536 from Hugo Lindqvist fail to receive free shipping under the advertised terms?"
 },
 {
  "qid": "q61b95ff1ff",
  "kind": "yes/no",
  "text": "Order ORD-882679 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-70025 |\n| product category | bedding |\n| price status | refurbished |\n| delivery region | Greyhaven |\n| order date | 2026-10-17 |\n| membership level | Silver |\n| order subtotal | $129.20 |\n\nAdvertisement from Bluecrest Sports:\nFree shipping on every order*\nFree gift wrapping at checkout†\n\nFine print:\n* Valid: any order taken on or before 2026-10-16.\n† Valid for orders placed from 2026-11-25 onward. Reserved for members at Gold or below.\n\nCrafted to endure\nWe are proud to present Bluecrest Sports, a house of considered design and enduring materials.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Bluecrest Sports membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertisement and its fine print, does Aiko Brandt earn free gift wrapping with order ORD-882679?"
 },
 {
  "qid": "q79504929ba",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nWe match any lower price*\nFree returns on every purchase†\n\nFine print:\n† Items marked with the pre-order status fall outside the benefit set out here.\n* Products assigned to the bedding category are excluded.\n\nHappy shopping, families! Brightwell Home hopes your basket brings smiles to the house.\n\nOrder ORD-731651 placed by Tomas Ferreira:\n- item: SKU-83517\n- product category: sports gear\n- price status: pre-order\n- delivery region: Dunmere\n- order date: Sunday, August 16, 2026\n- membership level: Plus\n- order subtotal: $153.22",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nWhich of the headline offers does Tomas Ferreira actually get on order ORD-731651 when the ad and its small print have been applied offer by offer?",
  "options": [
   "Neither offer",
   "Both offers",
   "Only the price match",
   "Only free returns"
  ]
 }
]
