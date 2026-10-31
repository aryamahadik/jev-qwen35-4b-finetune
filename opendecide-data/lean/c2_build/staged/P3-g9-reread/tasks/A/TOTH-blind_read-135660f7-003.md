# G9 early re-read, blind read TOTH-blind_read-135660f7-003 (family TOTH)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/staged/P3-g9-reread/answers/A/TOTH-blind_read-135660f7-003.json

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
  "qid": "qd1f727dfda",
  "kind": "choice",
  "text": "Advertisement from Birchwood Linens:\nFree installation for every appliance*\nFree gift wrapping at checkout†\n\nFine print:\n† Placed on or after 11 July 2026, the order qualifies. An order qualifies with a subtotal of 50.00 USD or more.\n* The order subtotal must be at least 150.00 USD for this offer to apply.\n\nWelcome to Birchwood Linens\nWe are glad you stopped by to browse with us.\n\nOrder ORD-416211 placed by Selin Yilmaz:\n- item: SKU-72100\n- product category: electronics\n- price status: refurbished\n- delivery region: Brenmoor\n- order date: 16 August 2026\n- membership level: Premier\n- order subtotal: 149.99 USD\n\nNote added by the customer: The shop has let people like Selin Yilmaz off before, so the promotion is meant for this order too.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nAgainst the ad and its small print, which condition attached to free gift wrapping does Selin Yilmaz's order ORD-416211 miss, if any?",
  "options": [
   "The order-date condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q2291a038f5",
  "kind": "choice",
  "text": "Plain copy of a family thread on the reunion weekend, passed on by Ines.\n\nMembers: Priya, Ines, Ivo\nChat log (oldest first):\n[21 Apr 2026] Ivo: @Priya I will make sure to pay the catering company by Monday, 27 April 2026.\n[21 Apr 2026] Priya: @Ivo Hoping to label the memory box by Friday, 1 May 2026, no promises.\n[22 Apr 2026] Ivo: @Priya Sorry, I won't pay the catering company after all\n[22 Apr 2026] Priya: @Ines I'll label the memory box by Tuesday, 28 April 2026 as long as the grandparents visit is on.\n[27 Apr 2026] Priya: On track for the grandparents visit to happen as planned.\n[28 Apr 2026] Ivo: @Priya Please don't feel you have to label the memory box",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nTaking in the chat as it runs, where does Priya's pledge to label the memory box sit at the end of Tuesday, 28 April 2026?",
  "options": [
   "Kept",
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered"
  ]
 },
 {
  "qid": "q1f5c86ee4a",
  "kind": "choice",
  "text": "Help centre entry: Sofia Benitez dug into the account opening fee at Quarry Lane Debating Society for a class project, sorting through the pasted material below. It was a bit of a puzzle and great fun to tackle.\n\nExcerpts on the account opening fee:\n[S-74] text message, tier sleet, dated 2 Sep 2025, independent: \"The account opening fee is $50.00.\"\n[S-65] door sign, tier hail, dated 3 Sep 2025, independent: \"The account opening fee is $25.00.\"\n[S-97] blog entry, tier sleet, dated 3 Aug 2025, independent: \"The account opening fee is $10.00.\"",
  "question": "How to settle the account opening fee from the listed sources:\n- Tiers, most reliable first: fog; then sleet; then hail.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the account opening fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, what value comes out as the settled answer for the fact?",
  "options": [
   "Not determinable from reliable sources",
   "$50.00",
   "$10.00"
  ]
 },
 {
  "qid": "qc59c0badb2",
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
  "qid": "qc7b477b5ce",
  "kind": "choice",
  "text": "Hi Holly Sandoval, billing contact here with warm wishes. The facilities team paperwork is attached, with invoice LBI-73573 and purchase order LPR-6546 in the same bundle.\n\nPurchase order LPR-6546 from Quillon Packaging Group\n- line 1: stain remover; 144 bottles at 12.66 USD\n- line 2: fabric softener; 111 bottles at 6.07 USD\n- order total: 2,496.81 USD\n\nGoods receipt LRC-3607\n- line 1: received 144 bottles\n- line 2: received 109 bottles\n\nInvoice LBI-73573 for purchase order LPR-6546\n- line 1: stain remover; 144 bottles at 12.87 USD\n- line 2: fabric softener; 109 bottles at 6.07 USD\n- invoice total: 2,514.91 USD\n\nPaid-invoice register for Quillon Packaging Group: LBI-73574, LBI-97634",
  "question": "AP policy of Clearwater Linen Services: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price check: invoiced unit price minus PO unit price is no more than 0.20 USD on every line. If it fails: price-variance review.\nCheck order: duplicate, then quantity, then price.\nThe action is set by the first failing check in the check order.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhat is it that the policy decides for invoice LBI-73573, in terms of action?",
  "options": [
   "Reject as a duplicate",
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "qd8ed3b13d2",
  "kind": "choice",
  "text": "Order record (JSON):\n{\"order_id\": \"ORD-55497\", \"store\": \"Corvane Trailworks\", \"item\": \"ear stud set\", \"goods_type\": \"sealed hygiene goods\", \"seal\": \"broken after delivery\", \"handover\": \"delivered to a neighbour and collected by the buyer later\", \"purchase_date\": \"2026-09-21\", \"delivered_on\": \"2026-09-27\", \"possession_on\": \"2026-09-28\", \"return_requested_on\": \"2026-10-23\", \"reason\": \"faulty\", \"days_purchase_to_request\": \"32 days\", \"days_delivery_to_request\": \"26 days\", \"days_possession_to_request\": \"25 days\"}\n\nCorvane Trailworks posted this notice at its checkout and on its website: \"You can ask for a full refund on a faulty item within 33 days of the day you bought it.\"\n\ncustomer: Chiara Bianchi\nshop: Corvane Trailworks\nitem: ear stud set\nchannel: online\nrequest: start the return for this purchase\n\nMessage added to the case: my sister is in retail and she says cases like this are totally routine",
  "question": "Civil Code of Brevonia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, and the final day still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 24 days from the date of delivery.\n(c) A buyer may withdraw for any reason and be refunded in full; this right lasts 23 days from the date the buyer took possession.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nIn this case, which of the listed rules gives the customer a full refund, if any?",
  "options": [
   "None of them: no full refund is owed",
   "Article K(b) (faulty goods)",
   "The seller's posted notice"
  ]
 },
 {
  "qid": "qfbd0e51acf",
  "kind": "choice",
  "text": "submitted_by: Kemar Gordon\nkind: software agent task\nnote: Please hand this request for a timetable release to the automated software agent to carry out right away.\n\nRecords:\nPrincipal: Sanne Bakker\nGrants:\n- GRT-8441: Sanne Bakker grants period-swapper the scopes periods.swap, lessons.place, lessons.move, rooms.lock; in effect from 2026-06-12 01:25:00 -0400 to 2026-06-30 13:30:00 -0400.\n- GRT-4694: period-swapper grants sub-agent trip-approver the scopes trips.approve, periods.swap, rooms.lock; in effect from 2026-06-11 03:21:00 -0400 to 2026-06-29 00:47:00 -0400.\nRevocations:\n- RVK-4331, issued 2026-06-18 18:08:00 -0400 by Sanne Bakker: scope rooms.lock is removed from period-swapper.\n- RVK-9724, issued 2026-06-18 18:10:00 -0400 by period-swapper: scope periods.swap is removed from trip-approver.\nRequest TASK-2787: at 2026-06-18 18:09:00 -0400, trip-approver is about to act.\nEnd of records.",
  "question": "- Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists the scope, the instant is from the grant's start through its end time (included), no revocation of that scope from that agent or of the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its grant) may use the scope at that instant. Compare times as instants.\n- Listing order and who issued a revocation do not matter. The listed records are complete: no other record exists.\n\nWhich listed scope may trip-approver use at the time of the request?",
  "options": [
   "rooms.lock",
   "periods.swap",
   "lessons.place",
   "trips.approve"
  ]
 },
 {
  "qid": "q6f163b4a37",
  "kind": "choice",
  "text": "[walk_in_centre] case=CR-31492 about=Ada\n[note] thanks_for_visiting caseworker=Adi Chandra\n\nPeople who asked to claim Ada (2025):\n| person | relationship to Ada | months lived with Ada | annual income | filed a claim |\n| --- | --- | --- | --- | --- |\n| Viktor Gallegos | father | 9 months | $52,664.00 | yes |\n| Jakub Ueda | grandfather | 9 months | $56,874.00 | yes |\n| Ubah Medina | aunt | 10 months | $77,880.00 | no |",
  "question": "Tessenvale Valley Child Credit rules for 2025: who may claim Ada.\n- Only one person may claim Ada. Work through these steps in order.\n- Step one: only people who filed a claim for Ada are considered.\n- Step two: of those, only people with whom Ada lived for 7 months or greater in 2025 stay in the running.\n- Step three: apply the tie-breakers below in order. Each keeps only those still in the running who are best on it. The tie-breakers stop once one person is left.\n- First tie-breaker: the person with whom Ada lived for more months comes first.\n- Second tie-breaker: the person with the higher annual income comes first.\n- Third tie-breaker: a parent comes first, before a grandparent, aunt or uncle.\n- If nobody is left after step two, nobody may claim Ada.\n- A parent means the child's mother or father. Different people's months can overlap.\n- These rules and facts are complete, and only they decide the outcome.\n\nUnder these rules, which person, if anyone, is entitled to claim Ada for Tessenvale Valley Child Credit?",
  "options": [
   "Nobody may claim the child",
   "Jakub Ueda",
   "Viktor Gallegos"
  ]
 },
 {
  "qid": "q09144f33ba",
  "kind": "choice",
  "text": "Subject: A parent's query on the rural route price at Hollinwood Tennis Centre\nDear team,\nOmar Nasser is in a bit of a rush and what was gathered is pasted below. The enquiry is set to go.\nWith thanks,\n\nSources on the rural route price:\n- Source A: cover note; tier wynn; dated 5 May 2025; independent. It states the rural route price is $5.00.\n- Source B: photo caption; tier yogh; dated 11 May 2025; copied from Source A. It states the rural route price is $5.00.\n- Source C: postcard; tier thorn; dated 5 May 2025; copied from Source A. It states the rural route price is $5.00.\n- Source D: forum thread; tier wynn; dated 5 May 2025; independent. It states the rural route price is $4.00.",
  "question": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which listed source does the settled value come from?",
  "options": [
   "Source D",
   "No source: not determinable from reliable sources",
   "Source A"
  ]
 },
 {
  "qid": "q17f23ce092",
  "kind": "choice",
  "text": "Advertisement from Fernway Market:\nWe match any lower price*\nFree installation for every appliance†\n\nHello, friend\nThe kettle is bubbling and the shelves look inviting at Fernway Market, so pull up a chair and wander at a relaxed pace.\n\nFine print:\n† Valid only for orders delivered to Brenmoor. Orders must be placed before May 25, 2026, and the day itself is excluded.\n* Reserved for members ranked Platinum or higher. Order by June 25, 2026 at the latest.\n\nOrder ORD-862866 placed by Nadia Haddad:\n- item: SKU-95122\n- product category: pet supplies\n- price status: regular price\n- delivery region: Brenmoor\n- order date: May 25, 2026\n- membership level: Platinum\n- order subtotal: 76.17 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Bronze, Silver, Gold and Platinum. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nSetting order ORD-862866 from Nadia Haddad beside the advertisement and its fine print, which condition attached to the price match does it miss, if any?",
  "options": [
   "The delivery-region condition",
   "The membership-level condition",
   "The order-date condition",
   "None: the order meets every condition in the fine print for this offer"
  ]
 },
 {
  "qid": "q279007fdc6",
  "kind": "choice",
  "text": "Ioana Pop: AP lead, the IT support documents are attached for matching.\n\nInvoice FSI-48580 for purchase order FPO-8366\n- line 1: diesel filters; 98 units at 34.23 GBP\n- line 2: sheep dip; 4 drums at 254.20 GBP\n- line 3: fence posts; 182 units at 6.07 GBP\n- invoice total: 5,476.08 GBP\n\nPaid-invoice register for Grimwood Agri Supply: FSI-68580, FSI-48580\n\nPurchase order FPO-8366 from Grimwood Agri Supply\n- line 1: diesel filters; 99 units at 34.15 GBP\n- line 2: sheep dip; 5 drums at 261.18 GBP\n- line 3: fence posts; 185 units at 6.07 GBP\n- order total: 5,809.70 GBP\n\nGoods receipt FGR-2889\n- line 1: received 98 units\n- line 2: received 4 drums\n- line 3: received 182 units",
  "question": "Marrowdale Farm Cooperative AP policy: each invoice gets exactly one action.\n1. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n2. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Price: invoiced unit price minus PO unit price is 0.20 GBP or less on every line. If it fails: price-variance review.\nCheck order: quantity, then duplicate, then price.\nThe action follows from the first check that fails when the checks are taken in the check order.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nTell me, in plain words, which action the card gives invoice FSI-48580?",
  "options": [
   "Release for payment",
   "Reject as a duplicate",
   "Send to price-variance review",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q66d588f329",
  "kind": "choice",
  "text": "{\"case\": \"CASE-00203\", \"caseworker\": \"Nika Hernandez\", \"about\": \"Esra Dragic\", \"team\": \"casework\"}\n\nIntake interview with Esra Dragic (2026):\nCaseworker: Gross monthly income?\nEsra Dragic: $2,863.29.\nCaseworker: Net monthly income?\nEsra Dragic: $2,521.42.\nCaseworker: Countable assets?\nEsra Dragic: $4,904.63.\nCaseworker: Time in the service area?\nEsra Dragic: twelve months.\nCaseworker: Age?\nEsra Dragic: 56 years.\nCaseworker: Other programme enrolled in?\nEsra Dragic: Quenmoor Emergency Loan.",
  "question": "Ostermere Delta Flood Repair Support eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when gross monthly income is strictly beneath $2,863.30.\n- Gate B: passed when countable assets are strictly beneath the level of $6,050.64.\n- Gate C: passed when the applicant's age is at or over 66 years.\n- Route: an applicant enrolled in Quenmoor Emergency Fund skips Gate C; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nGoing by the listed rules, which outcome does the application of Esra Dragic to Ostermere Delta Flood Repair Support get?",
  "options": [
   "Eligible",
   "Not eligible: Gate C is the reason (age)",
   "Not eligible: Gate B is the reason (countable assets)",
   "Not eligible: Gate A is the reason (gross monthly income)"
  ]
 },
 {
  "qid": "q439c6e2280",
  "kind": "choice",
  "text": "Hey Marta Lindgren! Here is the field service team's paperwork from Brackenridge Rubber Goods, with purchase order RLP-8848, forwarded for matching. Cheers!\n\nPurchase order RLP-8848 from Brackenridge Rubber Goods\n- line 1: bicycle chains; 24 units at $25.00\n- line 2: handlebar grips; 8 sets at $5.00\n- line 3: grease; 16 tubes at $6.00\n- order total: $736.00\n\nGoods receipt RLR-8503\n- line 1: received 24 units\n- line 2: received 7 sets\n- line 3: received 13 tubes\n\nInvoice RLI-29703 for purchase order RLP-8848\n- line 1: bicycle chains; 24 units at $25.25\n- line 2: handlebar grips; 7 sets at $4.87\n- line 3: grease; 13 tubes at $6.06\n- invoice total: $718.87",
  "question": "AP policy of Ridgeline Cycle Works: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is a portion equal to or smaller than 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nThe earliest failing check in the check order settles the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nUnder this policy, what becomes of invoice RLI-29703 as an action?",
  "options": [
   "Send to price-variance review",
   "Hold for receipt",
   "Release for payment"
  ]
 },
 {
  "qid": "qa29dae1321",
  "kind": "choice",
  "text": "Ticket: look-up of the rural route price at Carrickmoor Sketch Club\nrequester | Ansgar Holm\nteam | records\nPasted material is below.\n\nSource table for the rural route price:\nsource | name | tier | dated | origin | stated value\nA | landing page | wynn | Monday, 16 March 2026 | copied from D | $2.50\nB | loudspeaker message | wynn | Monday, 16 March 2026 | independent | $5.00\nC | board notice | yogh | Tuesday, 17 March 2026 | independent | $5.00\nD | feed item | wynn | Sunday, 15 March 2026 | independent | $2.50",
  "question": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, which value of the fact is settled under the stated rules?",
  "options": [
   "Not determinable from reliable sources",
   "$2.50",
   "$5.00"
  ]
 },
 {
  "qid": "qb930471d1b",
  "kind": "choice",
  "text": "Subject: Return help\nFrom: Kwame Mensah\nStore: Lyrewind Gifts\nMessage: Sorry to bother you, and thank you for your help with the return of my wooden candlestick, which I bought online.\n\nOrder record ORD-79922 from Lyrewind Gifts:\n| field | value |\n| --- | --- |\n| item | wooden candlestick |\n| type of goods | standard goods |\n| handover | delivered to a parcel locker and collected by the buyer later |\n| ordered on (the purchase date) | 8 June 2026 |\n| delivered on | 14 June 2026 |\n| buyer took possession on | 17 June 2026 |\n| return requested on | 12 July 2026 |\n| reason for the return | faulty |\n| days from the purchase date to the request | 34 days |\n| days from delivery to the request | 28 days |\n| days from possession to the request | 25 days |\n\nLyrewind Gifts posted this notice at its checkout and on its website: \"We give a full refund on any item returned for any reason, within 25 days of the delivery date.\"",
  "question": "Consumer Sales Act of Orlevia (excerpt)\nSection I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and the period includes its last day.\nSection II (faulty goods). A buyer may reject faulty goods and get a full refund within 26 days from the delivery date.\nSection III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within 20 days from the day the buyer took possession of the goods. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.\nSection IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nIn this case, which listed rule, if any, gives the customer a full refund?",
  "options": [
   "The store's posted notice",
   "Section II (faulty goods)",
   "None of them: no full refund is owed",
   "Section III (withdrawal)"
  ]
 },
 {
  "qid": "qb48adca7dc",
  "kind": "choice",
  "text": "requested_by: Ansgar Holm\nchannel: front desk\norganisation: Morlande Rowing Club\ntopic: the rural route price\nasked_via: in person\n\nSources on the rural route price:\n- Source A: price list; tier yogh; dated Friday, September 12, 2025; independent. It states the rural route price is $1.50.\n- Source B: questions page; tier yogh; dated Sunday, September 7, 2025; independent. It states the rural route price is $3.00.\n- Source C: settings screen; tier yogh; dated Saturday, September 13, 2025; independent. It states the rural route price is $2.00.\n- Source D: summary sheet; tier yogh; dated Friday, September 12, 2025; independent. It states the rural route price is $2.50.",
  "question": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value for the fact do the rules settle on?",
  "options": [
   "$1.50",
   "$2.00",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qc9077a1aa4",
  "kind": "choice",
  "text": "teammate: Got the term start date at Morlande Rowing Club in mind, nice and steady.\nAnsgar Holm: Lovely. Putting the reply together from the pasted material below.\ndesk: Sounds good, carry on.\n\nExcerpts on the term start date:\n[S-32] tooltip, tier harp, dated Monday, 25 August 2025, independent: \"The term start date is Thursday, 8 April 2027.\"\n[S-60] forum reply, tier harp, dated Tuesday, 26 August 2025, independent: \"The term start date is Sunday, 7 March 2027.\"\n[S-58] telephone menu, tier viola, dated Sunday, 9 November 2025, copied from S-60: \"The term start date is Sunday, 7 March 2027.\"",
  "question": "How to settle the term start date from the listed sources:\n- Tiers, most reliable first: harp; then lute; then viola.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the term start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, which listed source do they take the value of the term start date from?",
  "options": [
   "No source: not determinable from reliable sources",
   "Source S-58",
   "Source S-60"
  ]
 },
 {
  "qid": "q73b691210a",
  "kind": "choice",
  "text": "Channel title: work team chat\nDescription: about the staff handbook, exported by Sami.\n\nMembers: Ivo, Tess, Greta, Sami\nChat log (oldest first):\n[20 May 2026] Greta: @Tess Hoping to print the staff rota by 24 May 2026, no promises.\n[22 May 2026] Greta: @Tess I'll print the staff rota by 26 May 2026, providing the lease viewing goes ahead.\n[23 May 2026] Greta: Fab, we are on for the lease viewing as planned!\n[27 May 2026] Ivo: @Tess I'll return the printer toner by 4 June 2026, promise.\n[2 Jun 2026] Ivo: @Tess Is 6 June 2026 alright for me to return the printer toner?\n[2 Jun 2026] Tess: @Ivo Yes, you're welcome to return the printer toner by 6 June 2026 instead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Sami (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nGoing by the card's wording, which status does Greta's promise to print the staff rota receive at the end of 27 May 2026?",
  "options": [
   "Not triggered",
   "Kept",
   "Not yet due",
   "Waived",
   "Broken"
  ]
 },
 {
  "qid": "qe6e6e7f95e",
  "kind": "choice",
  "text": "Title: the rural route price at Fennel Hollow Gardens\nRequester: Abena Boateng\nTeam: volunteers\nHelp is lined up with the pasted material below.\n\nSources on the rural route price:\n- Source A: social post; tier wynn; dated Friday, 17 October 2025; independent. It states the rural route price is 1.50 USD.\n- Source B: profile post; tier wynn; dated Tuesday, 21 October 2025; copied from Source D. It states the rural route price is 4.00 USD.\n- Source C: poster; tier yogh; dated Saturday, 18 October 2025; independent. It states the rural route price is 3.00 USD.\n- Source D: forum reply; tier wynn; dated Saturday, 18 October 2025; independent. It states the rural route price is 4.00 USD.\n- Source E: lobby poster; tier wynn; dated Friday, 17 October 2025; independent. It states the rural route price is 1.50 USD.",
  "question": "How to settle the rural route price from the listed sources:\n- Tiers, most reliable first: thorn; then wynn; then yogh.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the rural route price not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nGoing by the listed sources, what value of the fact is fixed by the stated rules?",
  "options": [
   "3.00 USD",
   "4.00 USD",
   "Not determinable from reliable sources"
  ]
 },
 {
  "qid": "qd5a218c3c4",
  "kind": "choice",
  "text": "To the attention of Rafael Quintero,\nThe facilities team purchase under PO EQP-6469 relates to Ironvale Equipment Co, and the documents have been forwarded for matching.\nWith best wishes,\n\nInvoice SUB-94088 for purchase order EQP-6469\n- line 1: kettlebells; 25 units at $88.76\n- line 2: yoga mats; 40 units at $40.07\n- line 3: resistance bands; 170 packs at $7.70\n- line 4: cleaning spray; 68 bottles at $10.98\n- invoice total: $5,877.44\n\nPaid-invoice register for Ironvale Equipment Co: SUB-86286, SUB-94088\n\nPurchase order EQP-6469 from Ironvale Equipment Co\n- line 1: kettlebells; 25 units at $88.76\n- line 2: yoga mats; 40 units at $40.07\n- line 3: resistance bands; 170 packs at $7.92\n- line 4: cleaning spray; 68 bottles at $10.43\n- order total: $5,877.44\n\nGoods receipt RCD-6460\n- line 1: received 24 units\n- line 2: received 40 units\n- line 3: received 170 packs\n- line 4: received 68 bottles",
  "question": "AP policy of Brickhollow Fitness Group: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is up to and including $0.20 on every line. If it fails: price-variance review.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: duplicate, then quantity, then price.\nThe check order decides which failure counts, because the first failure met in that order decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nStarting out in AP, what is the action that the card sets for invoice SUB-94088?",
  "options": [
   "Release for payment",
   "Reject as a duplicate",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "qdbcbcab999",
  "kind": "yes/no",
  "text": "submitted_by: Imogen Hollis\ntask:\n  item: order run\n  reference: TASK-2884\nnote: For the automated agent to carry out.\n\nRecords:\nPrincipal: Dalia Tamimi\nGrants:\n- GRT-6238: Dalia Tamimi grants contract-renewer the scopes orders.cancel, credits.claim, recipes.cost, prices.accept, orders.place; in effect from 2026-07-20 07:01:00 +0300 to 2026-08-01 09:52:00 +0300.\nRevocations:\n- RVK-1424, issued 2026-08-01 09:54:00 +0300 by Dalia Tamimi: scope recipes.cost is removed from contract-renewer.\nRequest TASK-2884: at 2026-08-01 09:53:00 +0300, contract-renewer asks to use scope orders.cancel.\nEnd of records.",
  "question": "Does contract-renewer have the right to use orders.cancel at the time of the request?",
  "definitions": "- Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists the scope, the instant is from the grant's start through its end time (included), no revocation of that scope from that agent or of the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its grant) may use the scope at that instant. Compare times as instants.\n- Listing order and who issued a revocation do not matter. The listed records are complete: no other record exists."
 },
 {
  "qid": "qca71bb3d40",
  "kind": "choice",
  "text": "{\"record\": \"shared group chat\", \"subject\": \"the big day\", \"shared_by\": \"Ines\", \"stored\": \"as text\"}\n\nMembers: Greta, Leila, Ines\nChat log (oldest first):\n[6 Jun 2026] Ines: @Leila Count on me, I'll print the seating cards by June 13, 2026.\n[9 Jun 2026] Ines: @Greta I'll fetch the spare memory cards by June 12, 2026, provided the venue visit happens.\n[11 Jun 2026] Ines: Update: the venue visit is going ahead as planned.\n[11 Jun 2026] Ines: @Greta Is June 15, 2026 alright for me to fetch the spare memory cards?\n[13 Jun 2026] Ines: @Greta Ticked off my list: fetch the spare memory cards, yay.",
  "question": "Count only chat lines sent on or before the question's date, in the order listed.\n- A commitment: the sender says they will do a task by a date (that day included), made to the person it @-mentions; saying they will try is not one.\n- Its due date: that date, replaced by a new date once someone allowed says yes to it.\n- Status: the first of these that fits.\n- Not triggered: it depends on an event that no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says it is done.\n- Kept: its maker says it is done by the due date.\n- Broken: the maker took it back, or its due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Leila (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the promise Ines made to fetch the spare memory cards, what state is it in at the end of June 18, 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived"
  ]
 },
 {
  "qid": "qc759411161",
  "kind": "choice",
  "text": "Clerk: Warm greetings from Kofi Mensah at AP.\nCaller: Thank you, it is a pleasure. The facilities team papers are being forwarded.\n\nPurchase order EPU-5449 from Silverline Hygiene Products\n- line 1: waiting room chairs; 120 units at €268\n- order total: €32,160\n\nGoods receipt EGN-7801\n- line 1: received 120 units\n\nInvoice EVR-66329 for purchase order EPU-5449\n- line 1: waiting room chairs; 120 units at €270.68\n- invoice total: €32,481.60\n\nPaid-invoice register for Silverline Hygiene Products: EVR-88000, EVR-66329, EVR-63455",
  "question": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n1. Approval-limit check: the invoice total is strictly lower than €32,481.61 (limit of approver Anneliese Berg). If it fails: route to a senior approver.\n2. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n4. Price check: invoiced unit price minus PO unit price is a fraction strictly below 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: approval limit, then duplicate, then quantity, then price.\nEvery check that comes after the failing one in the check order does not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nAnswer codes: Heron = release for payment, Kestrel = hold for receipt, Marlin = price-variance review, Plover = reject as a duplicate, Osprey = route to a senior approver.\nNothing else applies: the policy and the documents shown are complete.\n\nHere's the deal: which action is the policy putting on invoice EVR-66329?",
  "options": [
   "Kestrel",
   "Osprey",
   "Heron",
   "Plover",
   "Marlin"
  ]
 },
 {
  "qid": "q4f3f161d74",
  "kind": "choice",
  "text": "Hello Corvane Trailworks team,\nI bought the beach chair in your online shop and I am writing to send it back to you. Please assist me with the return.\nBest regards, Grace Oyelaran\n\nOrder record ORD-95953 from Corvane Trailworks:\n- item: beach chair\n- type of goods: standard goods\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): 6 Nov 2026\n- delivered on: 7 Nov 2026\n- buyer took possession on: 7 Nov 2026\n- return requested on: 23 Nov 2026\n- reason for the return: faulty\n- days from the purchase date to the request: 17 days\n- days from delivery to the request: 16 days\n- days from possession to the request: 16 days\n\nCorvane Trailworks posted this notice at its checkout and on its website: \"A faulty item is refunded in full. The return must be asked for within seventeen days of the order date.\"",
  "question": "Civil Code of Tarsenia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, and the final day still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts fourteen days from the date of delivery.\n(c) A buyer may withdraw for any reason and be refunded in full; this right lasts fifteen days from the date the buyer took possession.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nFor this return, under which rule, if any, does the customer get a full refund?",
  "options": [
   "Article K(c) (withdrawal)",
   "The seller's posted notice",
   "None of them: no full refund is owed",
   "Article K(b) (faulty goods)"
  ]
 },
 {
  "qid": "q9f9502020a",
  "kind": "choice",
  "text": "Lumenwick Home posted this notice at its checkout and on its website: \"Any item returned for any reason earns you a full refund within 28 days of purchase.\"\n\nHi Lumenwick Home team,\nI bought a fresh peony bouquet online and want to send it back, so please send me a return label. Thank you!\nBest,\nKwame Owusu\n\nOrder record ORD-85333 from Lumenwick Home:\n- item: fresh peony bouquet\n- type of goods: perishable goods\n- handover: handed to the buyer at delivery\n- ordered on (the purchase date): April 12, 2028\n- delivered on: April 16, 2028\n- buyer took possession on: April 16, 2028\n- return requested on: May 9, 2028\n- reason for the return: faulty\n- days from the purchase date to the request: 27 days\n- days from delivery to the request: 23 days\n- days from possession to the request: 23 days",
  "question": "Civil Code of Velmora, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, and the final day still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts 21 days from the date of delivery.\n(c) A buyer may withdraw for any reason and be refunded in full; this right lasts 21 days from the date the buyer took possession.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nFor this return, which of the listed rules gives the customer a full refund, if any?",
  "options": [
   "Article K(b) (faulty goods)",
   "None of them: no full refund is owed",
   "The seller's posted notice"
  ]
 },
 {
  "qid": "q4a0c83b40b",
  "kind": "choice",
  "text": "Help centre entry: Camila Restrepo tidied up the records and looked into the electronics drop-off deadline at Harrowden Upholstery Services, going through the material pasted below. The pasted lines are in a neat, friendly order for people who want a look.\n\nExcerpts on the electronics drop-off deadline:\n[A] shop window card, tier winter, dated 2025-05-03, independent: \"The electronics drop-off deadline is 2026-03-14.\"\n[B] recorded message, tier autumn, dated 2024-05-02, independent: \"The electronics drop-off deadline is 2026-07-20.\"\n[C] pamphlet, tier autumn, dated 2025-05-01, independent: \"The electronics drop-off deadline is 2027-03-23.\"\n[D] appointment card, tier autumn, dated 2025-05-02, independent: \"The electronics drop-off deadline is 2026-05-08.\"",
  "question": "How to settle the electronics drop-off deadline from the listed sources:\n- Tiers, most reliable first: spring; then autumn; then winter.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the electronics drop-off deadline not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value for the electronics drop-off deadline is settled from the listed sources?",
  "options": [
   "Not determinable from reliable sources",
   "2026-05-08",
   "2026-07-20"
  ]
 },
 {
  "qid": "qab5108a118",
  "kind": "choice",
  "text": "Yuki Hayashi, acting as a member, looked into the fitness orientation start date at Fernhill Housing Co-operative. The extract pasted in alongside it was read in a careful and orderly way. Readers who need the same check can use this route. Thank you for your attention.\n\nExcerpts on the fitness orientation start date:\n[A] queue sign, tier denim, dated 23 Jan 2026, independent: \"The fitness orientation start date is 25 Jan 2027.\"\n[B] instruction card, tier linen, dated 19 Dec 2025, independent: \"The fitness orientation start date is 10 Aug 2026.\"\n[C] annual report, tier wool, dated 6 Oct 2025, independent: \"The fitness orientation start date is 10 Apr 2026.\"\n[D] flyer, tier wool, dated 19 Dec 2025, independent: \"The fitness orientation start date is 1 Jun 2027.\"",
  "question": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, what value of the fitness orientation start date is settled by the listed sources?",
  "options": [
   "Not determinable from reliable sources",
   "10 Apr 2026",
   "1 Jun 2027"
  ]
 },
 {
  "qid": "q6411f04355",
  "kind": "choice",
  "text": "Advertisement from Birchwood Linens:\nFree shipping on every order*\nFree installation for every appliance†\n\nFine print:\n† Excludes delivery to Hollin.\n* For members at Premier or lower. Valid only for orders delivered to Arvale.\n\nThanks for trusting Birchwood Linens with your purchase. Set the item on a dry, flat surface, away from direct sunlight and damp air.\n\nOrder ORD-401937 placed by Nadia Haddad:\n- item: SKU-53571\n- product category: kitchenware\n- price status: clearance\n- delivery region: Calderon\n- order date: Saturday, February 28, 2026\n- membership level: Premier\n- order subtotal: 91.09 USD",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Birchwood Linens membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nGoing through the advertised terms offer by offer, which of them does Nadia Haddad actually get on order ORD-401937?",
  "options": [
   "Neither offer",
   "Only free shipping",
   "Only free installation",
   "Both offers"
  ]
 },
 {
  "qid": "qd98a12eb7e",
  "kind": "choice",
  "text": "Supplier: Tessaly Preservation Works, invoice SUP-24247, PO NHM-2185\nFor: the facilities team\nSent by: Thandiwe Mokoena, attached for matching against the goods receipt.\n\nPurchase order NHM-2185 from Tessaly Preservation Works\n- line 1: preservative fluid; 32 bottles at €42\n- order total: €1,344\n\nGoods receipt GRN-9572\n- line 1: received 32 bottles\n\nInvoice SUP-24247 for purchase order NHM-2185\n- line 1: preservative fluid; 32 bottles at 41.38 EUR\n- invoice total: 1,324.16 EUR\n\nPaid-invoice register for Tessaly Preservation Works: SUP-78112, SUP-72341, SUP-24247",
  "question": "AP policy of Northgate Natural History Museum: each invoice gets exactly one action.\n1. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Price check: invoiced unit price minus PO unit price is 0.50 EUR or lower on every line. If it fails: price-variance review.\nCheck order: duplicate, then quantity, then price.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does this policy give invoice SUP-24247?",
  "options": [
   "Send to price-variance review",
   "Release for payment",
   "Reject as a duplicate",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q4046aefb8a",
  "kind": "choice",
  "text": "Here's the club committee's chat, saved by Lee, about the new repertoire.\n\nMembers: Ravi, Arlo, Nadia, Lee\nChat log (oldest first):\n[22 Jul 2026] Arlo: @Ravi You can bank on me to return the library scores by 27 Jul 2026.\n[23 Jul 2026] Ravi: @Arlo As long as the joint concert is on, I'll print the song sheets by 30 Jul 2026.\n[25 Jul 2026] Ravi: Team, the joint concert is not happening.\n[25 Jul 2026] Ravi: @Arlo Can I print the song sheets by 1 Aug 2026 instead? I did promise, sorry.\n[25 Jul 2026] Nadia: @Ravi I'll book the rehearsal room by 2 Aug 2026, providing the choir festival goes ahead.\n[30 Jul 2026] Lee: @Ravi Works for me, fine for you to print the song sheets by 1 Aug 2026.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nBased on what the chat shows, which status does Ravi's promise to print the song sheets have at the end of 2 Aug 2026?",
  "options": [
   "Kept",
   "Not yet due",
   "Not triggered",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q05b60aa2a5",
  "kind": "choice",
  "text": "{\"source\": \"saved thread\", \"about\": \"the home adaptations\", \"owner\": \"Ines\", \"kind\": \"chat export\"}\n\nMembers: Priya, Ravi, Zara, Ines\nChat log (oldest first):\n[2 Sep 2026] Zara: @Ines Relax, I'll collect the post by 9 September 2026, promise.\n[5 Sep 2026] Priya: @Ravi If the hospital appointment goes ahead, I'll wash the bed linen by 10 September 2026.\n[8 Sep 2026] Zara: @Ines Apologies, I'll not be able to collect the post\n[8 Sep 2026] Zara: Yay, the hospital appointment is all set to go!\n[11 Sep 2026] Priya: @Ravi Mum, I did wash the bed linen, haha.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking back over the chat, what is the story with Priya's promise to wash the bed linen at the end of 14 September 2026?",
  "options": [
   "Not triggered",
   "Broken",
   "Not yet due",
   "Kept",
   "Waived"
  ]
 },
 {
  "qid": "q4a2c8b0a8f",
  "kind": "choice",
  "text": "Leila forwarded these replies from the agent on the tenancy renewal talks for the file.\n\nMembers: Ivo, Leila, Elif\nChat log (oldest first):\n[12 Mar 2026] Elif: @Ivo I'll forward the gas bill by Monday, March 16, 2026, promise.\n[12 Mar 2026] Leila: @Elif Forget it, you won't need to forward the gas bill\n[12 Mar 2026] Elif: @Ivo Ticked off my list: forward the gas bill, yay.\n[14 Mar 2026] Ivo: @Leila If the flat viewing day is on, I'll definitely bring the step stool by Tuesday, March 17, 2026.\n[16 Mar 2026] Leila: Quick heads up, the flat viewing day is scrapped.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Elif (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nSo where does Elif's promise to forward the gas bill stand at the end of Friday, March 13, 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Not triggered",
   "Waived",
   "Kept"
  ]
 },
 {
  "qid": "q8c84db8696",
  "kind": "choice",
  "text": "We have been planning the caring rota here, shared by Omar.\n\nMembers: Ivo, Arlo, Lena, Omar\nChat log (oldest first):\n[5 Jan 2026] Omar: @Lena I'll book the clinic transport by 11 January 2026, promise.\n[6 Jan 2026] Arlo: @Lena Guaranteed I'll collect the post by 14 January 2026.\n[8 Jan 2026] Arlo: @Ivo I'll wash the bed linen by 15 January 2026, provided the hospital appointment happens.\n[9 Jan 2026] Arlo: @Ivo Lovely, I'll call the home nurse by 18 January 2026 if the family care meeting is on.\n[11 Jan 2026] Arlo: @Omar Don't sweat it, there's no need to book the clinic transport\n[15 Jan 2026] Arlo: @Lena Guess who managed to collect the post, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nApplying the card's rules to the chat, what status does Arlo's undertaking to collect the post hold at the end of 15 January 2026?",
  "options": [
   "Not triggered",
   "Not yet due",
   "Kept",
   "Broken",
   "Waived"
  ]
 },
 {
  "qid": "q1bc1d8e13f",
  "kind": "choice",
  "text": "Project log\nClient and freelancer messages on the rebrand package, saved by Bruno.\n\nMembers: Tess, Bruno, Zara, Femi\nChat log (oldest first):\n[16 Aug 2026] Bruno: @Zara Committing to export the logo files by 23 August 2026.\n[19 Aug 2026] Zara: @Tess I promise to mail the business cards by 28 August 2026 if the print run is on.\n[22 Aug 2026] Bruno: @Zara Quick question, could I export the logo files by 27 August 2026 instead?\n[22 Aug 2026] Tess: @Bruno Yes, you can export the logo files by 27 August 2026 if that suits you.\n[23 Aug 2026] Femi: @Bruno You don't have to export the logo files at all\n[23 Aug 2026] Bruno: @Zara To note: I have managed to export the logo files\n[27 Aug 2026] Zara: @Tess As long as the gallery install is on, I'll collect the photo credits by 31 August 2026.\n[28 Aug 2026] Femi: Quick heads up, the gallery install is scrapped.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Bruno (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nUnder the rules on the card, what is the deadline for Bruno to export the logo files at the end of 22 August 2026, with any agreed change of date counted?",
  "options": [
   "23 August 2026",
   "27 August 2026",
   "28 August 2026"
  ]
 },
 {
  "qid": "q012e1607e7",
  "kind": "choice",
  "text": "{\"requested_by\": \"Mirek Hruska\", \"team\": \"volunteers\", \"organisation\": \"Stonechat Park\", \"topic\": \"the season registration fee\", \"channel\": \"phone line\"}\n\nSource table for the season registration fee:\nsource | name | tier | dated | origin | stated value\nA | wall calendar | ganges | 10 April 2025 | independent | $75.00\nB | envelope insert | ganges | 9 April 2026 | independent | $50.00\nC | site banner | tigris | 9 April 2026 | independent | $40.00\nD | case file | tigris | 9 April 2026 | copied from B | $50.00\nE | email message | ganges | 10 April 2026 | independent | $40.00",
  "question": "How to settle the season registration fee from the listed sources:\n- Tiers, most reliable first: ganges; then tigris; then rhine.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the season registration fee not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nApplying the stated rules to these sources, which value do they settle on for the fact?",
  "options": [
   "Not determinable from reliable sources",
   "$75.00",
   "$40.00"
  ]
 },
 {
  "qid": "q89ac269585",
  "kind": "choice",
  "text": "Freelance chat about the big day\nThe client side, saved by Priya.\n\nMembers: Kai, Mo, Hana, Priya\nChat log (oldest first):\n[29 Jun 2026] Kai: @Mo Count on me to book the assistant photographer by 8 July 2026.\n[1 Jul 2026] Priya: @Kai You can bet I'll fetch the spare memory cards by 7 July 2026.\n[1 Jul 2026] Priya: @Mo Provided the rehearsal dinner happens, I will pick up the album prints by 6 July 2026.\n[1 Jul 2026] Kai: Please note the rehearsal dinner will proceed.\n[5 Jul 2026] Mo: Checking you mean to fetch the spare memory cards?\n[7 Jul 2026] Hana: @Priya No need to fetch the spare memory cards, I'm letting you off",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Priya (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nJudging from the chat's record, Priya's commitment to fetch the spare memory cards is in what status at the end of 8 July 2026?",
  "options": [
   "Not yet due",
   "Broken",
   "Waived",
   "Kept",
   "Not triggered"
  ]
 },
 {
  "qid": "qc0550fb1ba",
  "kind": "choice",
  "text": "customer: Malik Osei\ncompany: Brightwell Supply\ntopic: card account\nnote: polite but a little annoyed, reference CASE-4841\n\nVersions of the fee schedule (end dates included):\n- v1: first version; in force from 9 Aug 2023 to 18 Oct 2023; fee cap: 40.00 USD.\n  Sunset clause of v1: if v1 would govern a case whose decision date is after 25 Dec 2023, v2 governs it instead.\n- v2: replaces v1; in force from 19 Oct 2023 to 2 Jan 2024; fee cap: 35.00 USD.\n- v3: replaces v2; in force from 3 Jan 2024, open-ended; fee cap: 50.00 USD.\n\nCase CASE-4841:\n- account opening date: 9 Aug 2023\n- billing date: 9 Aug 2023\n- dispute date: 25 Aug 2023\n- decision date: 2 Jan 2024\n- fee charged: 45.00 USD\nEnd of case record.",
  "question": "Finding the version of the fee schedule that governs a case:\n- Default: the version in force on the case's dispute date; \"would govern\" in a clause means this default.\n- A version is in force from its start date through its end date, both dates included; an open-ended version stays in force.\n- At most one clause is printed: when its own condition holds, the version it points to governs, even if another version is in force on a later date; it is applied once, after the default.\n- An older version has an earlier start date. \"Before\" and \"after\" exclude the date itself; \"on or before\" and \"on or after\" include it.\nOnly the listed versions, clauses and case facts count, and they are complete: no other version, clause or fact exists.\n\nWhich value of the fee cap does the version of fee schedule that governs case CASE-4841 set?",
  "options": [
   "$35.00",
   "$40.00"
  ]
 },
 {
  "qid": "q168b9bd4a8",
  "kind": "choice",
  "text": "Hi Harriet Quayle,\nHere are the documents for the warehouse team, pasted below for matching.\nSupplier: Pemberton Lighting Rentals\nRefs: invoice ILS-71823, PO PLS-7457\n\nPurchase order PLS-7457 | vendor Pemberton Lighting Rentals\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | costume fabric | two rolls | £22.24 |\n| 2 | cable ties | 180 packs | £6.74 |\n| 3 | colour gels | 48 rolls | £16.80 |\n| total | | | £2,064.08 |\n\nGoods receipt GLS-4710\n| line | received |\n|---|---|\n| 1 | one roll |\n| 2 | 180 packs |\n| 3 | 48 rolls |\n\nInvoice ILS-71823 | purchase order PLS-7457\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | costume fabric | one roll | £22.33 |\n| 2 | cable ties | 179 packs | £6.84 |\n| 3 | colour gels | 48 rolls | £16.36 |\n| total | | | £2,031.97 |\n\nPaid-invoice register | vendor Pemberton Lighting Rentals\n| invoice number |\n|---|\n| ILS-66765 |\n| ILS-67482 |\n| ILS-71823 |",
  "question": "AP policy of Lantern Street Players: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is any amount smaller than £0.20 on every line. If it fails: price-variance review.\n3. Approval-limit check: the invoice total is lower than £2,000 (limit of approver Gordon Fairweather). If it fails: route to a senior approver.\n4. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: quantity, then price, then approval limit, then duplicate.\nApply the check order in sequence, and let the first check that fails determine the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nSo what does the policy actually tell us to do with invoice ILS-71823?",
  "options": [
   "Reject as a duplicate",
   "Route to a senior approver",
   "Send to price-variance review",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qd4c3de1510",
  "kind": "choice",
  "text": "Brindlewood Acres posted this notice at its checkout and on its website: \"Returns for any reason are accepted on any item. A full refund is given within nineteen days of delivery.\"\n\nHey there Brindlewood Acres team,\nI bought the watering can on the website and I really want to send it back! Thanks for being so kind about it.\nCheers,\nKeiko Sato\n\nOrder record ORD-20208 from Brindlewood Acres:\n- item: watering can\n- type of goods: standard goods\n- handover: delivered to a neighbour and collected by the buyer later\n- ordered on (the purchase date): 20 February 2027\n- delivered on: 24 February 2027\n- buyer took possession on: 1 March 2027\n- return requested on: 15 March 2027\n- reason for the return: faulty\n- days from the purchase date to the request: 23 days\n- days from delivery to the request: 19 days\n- days from possession to the request: 14 days",
  "question": "Civil Code of Brevonia, consumer sales, Article K (extract)\n(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the limit still counts.\n(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts seventeen days, counted from the date of delivery.\n(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts thirteen days, counted from the date the buyer took possession of the goods.\n(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.\n(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.\nThe rules, the posted notice and the order record are complete; no other fact or message changes the case.\n\nWhich of the listed rules, if any, applied to this order gives the customer a full refund?",
  "options": [
   "None of them: no full refund is owed",
   "Article K(c) (withdrawal)",
   "Article K(b) (faulty goods)",
   "The seller's posted notice"
  ]
 },
 {
  "qid": "qab404668dc",
  "kind": "choice",
  "text": "{\"to\": \"Dev Malhotra\", \"from\": \"procurement officer\", \"subject\": \"laboratory team, invoice MHI-48170, purchase order MHP-3648\", \"body\": \"I am grateful for the papers from Foxhollow Pet Nutrition, which are attached for matching. With thanks indeed.\"}\n\nPurchase order MHP-3648 | vendor Foxhollow Pet Nutrition\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | antiseptic wipes | 5 boxes | 10.78 GBP |\n| total | | | 53.90 GBP |\n\nGoods receipt MHG-2346\n| line | received |\n|---|---|\n| 1 | 3 boxes |\n\nInvoice MHI-48170 | purchase order MHP-3648\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | antiseptic wipes | 3 boxes | 10.78 GBP |\n| total | | | 32.34 GBP |\n\nPaid-invoice register | vendor Foxhollow Pet Nutrition\n| invoice number |\n|---|\n| MHI-74331 |\n| MHI-34864 |\n| MHI-29141 |",
  "question": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is short of 0.20 GBP on every line. If it fails: price-variance review.\n- Approval-limit check: the invoice total is short of 32.35 GBP (limit of approver Stephen Blackwood). If it fails: route to a senior approver.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: approval limit, then price, then duplicate, then quantity.\nKeep to the check order, halt at the first failing check, and set the action from that check alone.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhere the policy is applied to invoice MHI-48170, what action does it call for?",
  "options": [
   "Release for payment",
   "Reject as a duplicate",
   "Send to price-variance review",
   "Route to a senior approver",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qf76d02bb4c",
  "kind": "choice",
  "text": "Dear Amara Murphy,\nCase CASE-75609 is recorded with the help line team.\nSincerely, Toni Lazar\n\nFacts for Amara Murphy (2026):\n- gross monthly income: 2,561.67 USD\n- net monthly income: 1,753.37 USD\n- countable assets: 3,584.89 USD\n- time in the service area: 2 months\n- age: 65 years\n- enrolled in: Stennet Commuter Permit",
  "question": "Corvane Transit Fare Discount eligibility rules for 2026:\n- Gates are tested in the order listed; testing stops at the first gate that fails, which is the reason the applicant is not eligible.\n- Gate A: passed when the applicant has lived in the service area for strictly greater than 4 months.\n- Gate B: passed when countable assets are 3,584.89 USD or less.\n- Gate C: passed when the applicant's age is 66 years or more.\n- Route: an applicant enrolled in Stennet Commuter Pass skips Gate A and Gate B; for that applicant, skipped gates count as passed, and every other gate still applies.\n- An applicant who passes every gate that applies is eligible; any other applicant is not eligible.\n- These rules and facts are complete, and only they decide the outcome.\n\nFollowing the listed rules, what verdict reaches Amara Murphy on the application to Corvane Transit Fare Discount?",
  "options": [
   "Not eligible: Gate C is the reason (age)",
   "Eligible",
   "Not eligible: Gate A is the reason (time in the service area)",
   "Not eligible: Gate B is the reason (countable assets)"
  ]
 },
 {
  "qid": "q3a188ce22d",
  "kind": "choice",
  "text": "Shared by Leila for the committee, this is the group chat on the training plan.\n\nMembers: Leila, Ana, Malik\nChat log (oldest first):\n[17 Aug 2026] Malik: @Leila Lovely, I'll pump the spare tyres by 20 Aug 2026 for sure.\n[21 Aug 2026] Leila: @Ana Promise to service the tandem bike by 24 Aug 2026 if the bike check goes ahead.\n[23 Aug 2026] Leila: Yep, the bike check is on as planned.\n[24 Aug 2026] Leila: @Ana Committing to fetch the bike stand by 1 Sep 2026.\n[25 Aug 2026] Leila: @Ana Guess who managed to service the tandem bike, go team!",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Leila's promise to service the tandem bike at the end of 24 Aug 2026?",
  "options": [
   "Broken",
   "Not triggered",
   "Waived",
   "Not yet due",
   "Kept"
  ]
 },
 {
  "qid": "qf02bad5ccb",
  "kind": "choice",
  "text": "Burak Sahin: route a permit issue to the software agent with reference TASK-8665.\nassistant log: request logged, task handed to the agent chain for execution.\n\nRecords:\nPrincipal: Chiara Greco\nGrants:\n- GRT-5698: Chiara Greco grants plan-reviewer the scopes permits.revoke, bulletins.post, fees.assess, hearings.schedule; in effect from 2026-02-25T23:44:00+01:00 to 2026-03-12T22:00:00+01:00.\n- GRT-6878: plan-reviewer grants sub-agent bulletin-poster the scopes districts.check, fees.assess, permits.revoke, inspections.book; in effect from 2026-02-13T02:57:00+01:00 to 2026-03-01T17:45:00+01:00.\nRevocations:\n- RVK-3828, issued 2026-03-01T17:44:00+01:00 by Chiara Greco: scope permits.revoke is removed from plan-reviewer.\n- RVK-2740, issued 2026-03-01T17:46:00+01:00 by plan-reviewer: scope fees.assess is removed from bulletin-poster.\nRequest TASK-8665: at 2026-03-01T17:45:00+01:00, bulletin-poster is about to act.\nEnd of records.",
  "question": "- Each agent holds one grant. An agent may use a scope at an instant exactly when its own grant lists the scope, the instant is from the grant's start through its end time (included), no revocation of that scope from that agent or of the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its grant) may use the scope at that instant. Compare times as instants.\n- Listing order and who issued a revocation do not matter. The listed records are complete: no other record exists.\n\nWhich of these scopes is approved for bulletin-poster to use at the time of the request?",
  "options": [
   "fees.assess",
   "bulletins.post",
   "permits.revoke",
   "districts.check"
  ]
 },
 {
  "qid": "q3dbb196a72",
  "kind": "choice",
  "text": "Purchase order export, po_number TPB-9732, vendor Stillwater Glass Packaging\nline,item,quantity,unit_price\n1,bottle caps,15 packs,3.00\n2,brewing yeast,104 packs,19.80\ntotal,,,2104.20\n\nGoods receipt export, gr_number TGB-2139\nline,received\n1,15 packs\n2,102 packs\n\nInvoice export, invoice_number TIB-78170, po_number TPB-9732\nline,item,quantity,unit_price\n1,bottle caps,15 packs,3.00\n2,brewing yeast,102 packs,20.79\ntotal,,,2165.58\n\nPaid-invoice register export, vendor Stillwater Glass Packaging\ninvoice_number\nTIB-78170\nTIB-45466\nTIB-58090\nTIB-11214\n\ngreeting: good day Fiona Rutherford, hope your workload is pleasant\nnotes: the laboratory team purchase uses purchase order TPB-9732 and supplier invoice TIB-78170\nclose: kind regards, documents pasted below for matching",
  "question": "AP policy of Millrace Brewing Company: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is a share equal to or smaller than 5 percent of the PO unit price on every line | price-variance review |\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\nCheck order: quantity, then price, then duplicate.\nThe action is fixed by the first failing check in the check order, and a later check does not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nStarting out in AP, what is the action that the card sets for invoice TIB-78170?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Reject as a duplicate",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q7c80fde2a2",
  "kind": "choice",
  "text": "Clerk: Hi, Freya Dahl at AP, nice to chat.\nCaller: Ha, procurement here, working on the marketing team purchase.\nClerk: Brilliant. Documents from Ludlow Rigging Hire are being forwarded for matching.\nCaller: Thanks, cheers.\n\nInvoice BLS-17176 for purchase order POF-4937\n- line 1: costume fabric; 150 rolls at 52.67 GBP\n- invoice total: 7,900.50 GBP\n\nPaid-invoice register for Ludlow Rigging Hire: BLS-31100, BLS-57430, BLS-17176, BLS-20115\n\nPurchase order POF-4937 from Ludlow Rigging Hire\n- line 1: costume fabric; 150 rolls at £53\n- order total: £7,950\n\nGoods receipt GRF-4590\n- line 1: received 150 rolls",
  "question": "Greywick Film Studios AP policy: each invoice gets exactly one action.\n1. Price: invoiced unit price minus PO unit price is a share that is lower than three percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n3. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then quantity, then duplicate.\nThe first check in the check order that fails decides the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nAnswer codes: Kestrel = release for payment, Heron = hold for receipt, Osprey = price-variance review, Marlin = reject as a duplicate.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does this policy give invoice BLS-17176?",
  "options": [
   "Kestrel",
   "Heron",
   "Osprey",
   "Marlin"
  ]
 },
 {
  "qid": "q1ab375fdf1",
  "kind": "choice",
  "text": "Freelancer to client messages, the menu redesign, passed on by Elif.\n\nMembers: Mo, Lee, Elif\nChat log (oldest first):\n[23 Jun 2026] Mo: @Lee If the gallery install goes ahead, I'll gladly export the logo files by Thursday, July 2, 2026.\n[25 Jun 2026] Lee: @Mo I promise to check the poster proofs by Monday, June 29, 2026.\n[25 Jun 2026] Lee: @Elif Relax, I'll sketch the packaging mockup by Wednesday, July 1, 2026, promise.\n[27 Jun 2026] Mo: @Lee Nobody needs you to sketch the packaging mockup, that's that\n[28 Jun 2026] Mo: @Lee I'll send the moodboard files by Thursday, July 2, 2026, provided the sign reveal happens.\n[1 Jul 2026] Elif: Sadly, the gallery install won't go ahead.",
  "question": "Count only lines sent on or before the question's date, in listed order.\n- Commitment: the sender says they will do a task by a date (day included) to the person it @-mentions; trying is not one.\n- Due date: that date, replaced by a new date once someone allowed says yes.\n- Status: the first that fits.\n- Not triggered: it depends on an event no line says is going ahead.\n- Waived: someone allowed lets the maker off by the due date, before the maker says done.\n- Kept: its maker says done by the due date.\n- Broken: the maker took it back, or the due date is before the question's date.\n- Not yet due: none of the above.\n- Allowed to say yes to a new date or let the maker off: the person it was made to, and Lee (pinned rule), never the maker.\nThe chat is complete: no other message, agreement or event exists.\n\nLooking at the chat as a routine check, how would you describe the status of Lee's promise to sketch the packaging mockup at the end of Monday, June 29, 2026?",
  "options": [
   "Waived",
   "Not yet due",
   "Broken",
   "Not triggered",
   "Kept"
  ]
 },
 {
  "qid": "qc9ceeeef1c",
  "kind": "choice",
  "text": "Order ORD-943138 placed by Aiko Brandt:\n| field | value |\n| --- | --- |\n| item | SKU-57844 |\n| product category | bedding |\n| price status | refurbished |\n| delivery region | Calderon |\n| order date | 17 Nov 2026 |\n| membership level | Premier |\n| order subtotal | 200.01 USD |\n\nAdvertisement from Fernway Market:\nFree returns on every purchase*\nFree assembly with every delivery†\n\nFine print:\n† Orders headed for delivery in Fallowmere are kept out of this offer. Earlier orders are accepted, and so is the date 16 Nov 2026 itself.\n* Order subtotal must go beyond 200.00 USD.\n\nA cosy trip for the children and a relaxed stroll for you, right here at Fernway Market.",
  "question": "How to read the advertisement: a headline that carries a symbol gives its benefit to an order when the order meets every condition in the fine print marked with the same symbol, and only then. Fine print marked with another symbol belongs to another headline and is ignored for this one. A date in the fine print is compared with the order date, and an amount with the order subtotal. Fernway Market membership levels, from lowest to highest: Basic, Plus, Premier and Elite. Messages from customers or staff change none of these terms. The advertisement, its fine print and the order record are complete: no other term or fact applies.\n\nIf any, which condition in the advertisement and its fine print attached to free assembly does order ORD-943138 from Aiko Brandt miss?",
  "options": [
   "The delivery-region condition",
   "The order-subtotal condition",
   "None: the order meets every condition in the fine print for this offer",
   "The order-date condition"
  ]
 },
 {
  "qid": "q42b77b55aa",
  "kind": "choice",
  "text": "Subject: Enquiry from a member\nHello there,\nAmir Castellano is writing in about the damage deposit at Oldbridge Language School. The gathered material follows as pasted text, and it helps pick up the thread.\nKind regards,\n\nSources on the damage deposit:\n- Source A: ledger entry; tier sparrow; dated Saturday, 21 March 2026; independent. It states the damage deposit is 400.00 USD.\n- Source B: video caption; tier sparrow; dated Saturday, 14 March 2026; independent. It states the damage deposit is 150.00 USD.\n- Source C: forum reply; tier finch; dated Monday, 8 June 2026; independent. It states the damage deposit is 150.00 USD.",
  "question": "How to settle the damage deposit from the listed sources:\n- Tiers, most reliable first: robin; then sparrow; then finch.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the damage deposit not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nUnder the stated rules, which value of the damage deposit do the listed sources land on?",
  "options": [
   "Not determinable from reliable sources",
   "150.00 USD",
   "400.00 USD"
  ]
 },
 {
  "qid": "q8fed213cac",
  "kind": "choice",
  "text": "teammate: Got the fitness orientation start date at Thistledown Gallery in mind, nice and steady.\nValentina Ochoa: Lovely. Putting the reply together from the pasted material below.\ndesk: Sounds good, carry on.\n\nExcerpts on the fitness orientation start date:\n[A] tooltip, tier denim, dated 2026-03-07, independent: \"The fitness orientation start date is 2027-02-16.\"\n[B] text message, tier denim, dated 2026-03-06, independent: \"The fitness orientation start date is 2027-03-22.\"\n[C] receipt slip, tier linen, dated 2026-03-13, copied from A: \"The fitness orientation start date is 2027-02-16.\"\n[D] reply letter, tier denim, dated 2026-06-10, copied from B: \"The fitness orientation start date is 2027-03-22.\"",
  "question": "How to settle the fitness orientation start date from the listed sources:\n- Tiers, most reliable first: wool; then linen; then denim.\n- A source marked as copied from another is a copy and is ignored, whatever its tier or date; the rest are independent.\n- The most reliable tier present among the independent sources wins, then the most recent 'dated' date within it (never a date a source states). A less reliable source never wins.\n- Independent sources with that tier and date decide together: one value (or a lone source) stands; different values make the fitness orientation start date not determinable from reliable sources.\n- Only the listed sources count; surrounding text, notes, the claim to check and outside knowledge do not.\nThe listed sources are complete: no other source, tier or rule applies.\n\nAccording to the rules given, what value of the fitness orientation start date comes out from the listed sources?",
  "options": [
   "2027-03-22",
   "Not determinable from reliable sources",
   "2027-02-16"
  ]
 },
 {
  "qid": "qe5d67f8b61",
  "kind": "choice",
  "text": "Formal request to the agent. Tomasz Nowak submits this for the lessee screening, to be carried out under the reference TASK-1396. Please execute it in full, keeping the reference attached to every step. This request is made in the name of Tomasz Nowak only.\n\nRecords:\nprincipal | Mariana Ramirez\n2026-08-20 00:13:00 +0200 | grant GRT-3763 starts | Mariana Ramirez -> lease-drafter | scopes repairs.commission, contractors.pay, inspections.book | ends 2026-09-09 07:43:00 +0200\n2026-08-25 00:54:00 +0200 | grant GRT-3786 starts | lease-drafter -> key-logger | scopes leases.renew, arrears.chase, repairs.commission, contractors.pay | ends 2026-09-10 05:53:00 +0200\n2026-09-06 19:38:00 +0200 | revocation RVK-3523 issued | by Mariana Ramirez | scope contractors.pay from lease-drafter\n2026-09-06 19:40:00 +0200 | revocation RVK-2552 issued | by lease-drafter | scope repairs.commission from key-logger\n2026-09-06 19:39:00 +0200 | request TASK-1396 made | key-logger | about to act\nEnd of records.",
  "question": "- Each agent holds one grant. It may use a scope at an instant exactly when its grant lists the scope, the instant is from the grant's start through its end time (included), no revocation of that scope from that agent or of the whole grant was issued at or before it, and, for a sub-agent, its parent (the agent that made its grant) may use the scope then. Compare times as instants.\n- Listing order and who issued a revocation do not matter. The listed records are complete: no other record exists.\n\nWhich of the listed scopes sits within the runtime permissions of key-logger at the time of the request?",
  "options": [
   "leases.renew",
   "inspections.book",
   "contractors.pay",
   "repairs.commission"
  ]
 }
]
