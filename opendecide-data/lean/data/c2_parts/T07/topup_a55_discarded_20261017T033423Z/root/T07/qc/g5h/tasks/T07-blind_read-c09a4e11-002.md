# G5-H blind read T07-blind_read-c09a4e11-002 (family T07)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T07/topup_a55/root/T07/qc/g5h/answers/T07-blind_read-c09a4e11-002.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 5. Answers expected: 5 (one per item, each with that item's qid).

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
  "qid": "q301675ec7a",
  "kind": "yes/no",
  "text": "Order ORD-280151 placed by Hugo Lindqvist:\n| field | value |\n| --- | --- |\n| item | SKU-92420 |\n| product category | furniture |\n| price status | regular price |\n| delivery region | Brenmoor |\n| order date | 10 March 2026 |\n| membership level | Green |\n| order subtotal | $167.18 |\n\nAdvertisement from Tidewell Supply:\nA lifetime warranty on everything we sell*\nFree shipping on every order†\n\nSubject: Elevated living, simply expressed\nDear friend, Tidewell Supply brings sophisticated taste to the home, with pieces that hold their own.\n\nFine print:\n* Delivery to Brenmoor sits outside the headline benefit. Valid for orders placed before 22 February 2026.\n† Only the furniture category earns the headline benefit. Orders headed for delivery in Eskarth are kept out of this offer.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Tidewell Supply membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nUnder the advertised terms, does the order ORD-280151 placed by Hugo Lindqvist forfeit free shipping, as what the advertisement says indicates?"
 },
 {
  "qid": "qb69ef05ba1",
  "kind": "yes/no",
  "text": "Support chat about order ORD-394873:\nHugo Lindqvist: Hi, I placed order ORD-394873 on 2026-03-02 for item SKU-92943, and the order subtotal was 231.21 USD.\nAgent: Thanks. The item is in the garden tools product category, its price status is clearance, and it ships to the Eskarth delivery region.\nAgent: Your membership level is Blue.\nHugo Lindqvist: I am asking about the advertisement below.\n\nAdvertisement from Birchwood Linens:\nFree shipping on every order*\n\nOur doors are wide and our kettle is warm at Birchwood Linens, so please come and sit down for a bit.\n\nFine print:\n* Customers must spend at least $200 on the order subtotal. Valid for orders placed from 2026-03-02 onward.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Green, Blue and Black. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-394873 from Hugo Lindqvist fail to receive free shipping under the advertised terms?"
 },
 {
  "qid": "q594c69e753",
  "kind": "choice",
  "text": "Advertisement from Brightwell Home:\nFree returns on every purchase*\nWe match any lower price†\n\nFine print:\n† An order placed on or before 11 June 2026 qualifies. For members at Plus or lower.\n* Placed before 8 June 2026 counts; that very day is excluded.\n\nGood coffee, good company and a little bit of fun at Brightwell Home. Pop by and see what we have been up to.\n\nOrder ORD-895256 placed by Felix Moreau:\n- item: SKU-18703\n- product category: toys\n- price status: regular price\n- delivery region: Dunmere\n- order date: 7 June 2026\n- membership level: Premier\n- order subtotal: $74.85\n\nNote added by the customer: Felix Moreau feels a small wobble in the arrival should not spoil the promotion, since the order landed almost exactly as expected.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Brightwell Home membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing by the advertisement and its fine print, which condition attached to the price match does order ORD-895256 from Felix Moreau miss, if any?",
  "options": [
   "The order-date condition",
   "The membership-level condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "qffcc773b4f",
  "kind": "choice",
  "text": "Order ORD-232564 placed by Hugo Lindqvist:\n| field | value |\n| --- | --- |\n| item | SKU-54549 |\n| product category | garden tools |\n| price status | refurbished |\n| delivery region | Calderon |\n| order date | Friday, July 3, 2026 |\n| membership level | Plus |\n| order subtotal | $171.49 |\n\nAdvertisement from Copperleaf Kitchen:\nDouble reward points on every purchase*\nFree shipping on every order†\n\nFine print:\n† Items at open box pricing are withheld from this benefit.\n* Headline benefit is limited to delivery in Calderon.\n\nSubject: A warm hello from our team\nDear friend, we love sharing our newest pieces with you at Copperleaf Kitchen.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Copperleaf Kitchen membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nOf the conditions in the small print attached to free shipping, which, if any, does order ORD-232564 from Hugo Lindqvist miss, according to what the advertisement says?",
  "options": [
   "None: the order meets every condition in the fine print for this offer",
   "The price-status condition",
   "The delivery-region condition"
  ]
 },
 {
  "qid": "q41f9b46a08",
  "kind": "yes/no",
  "text": "Advertisement from Wrenfield Outdoor:\nFree shipping on every order*\nWe match any lower price†\n\nQuick look, clear choice\nStep up to Wrenfield Outdoor and scan a sharp, edited range built to make choosing simple.\n\nFine print:\n† Shoppers get the headline benefit solely for delivery in Arvale. Minimum order subtotal: 35.00 USD.\n* For members at Bronze or lower. Orders headed for delivery in Dunmere are kept out of this offer.\n\nOrder ORD-541695 placed by Lena Whitcombe:\n| field | value |\n| --- | --- |\n| item | SKU-59315 |\n| product category | pet supplies |\n| price status | refurbished |\n| delivery region | Arvale |\n| order date | 2026-06-23 |\n| membership level | Platinum |\n| order subtotal | 35.00 USD |",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Wrenfield Outdoor membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nDoes order ORD-541695 from Lena Whitcombe forfeit the price match under the advertised terms, as those terms are written?"
 }
]
