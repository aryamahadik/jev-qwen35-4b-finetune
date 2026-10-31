# G5-H blind read T12-blind_read-2848fec9-005 (family T12)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T12/qc/g5h/answers/T12-blind_read-2848fec9-005.json

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
  "qid": "qbac2edf808",
  "kind": "yes/no",
  "text": "Clerk: Hello, Tendai Moyo from the AP team is the clerk handling this file.\nCaller: Lovely, we are the marketing team, and this is appreciated.\nClerk: Thank you kindly, the documents are being sent along. Supplier invoice SUB-52706 from Cobalt Rubber Mats sits alongside purchase order EQP-6395.\n\nInvoice SUB-52706 for purchase order EQP-6395\n- line 1: whey powder; 72 bags at 154.88 USD\n- line 2: cleaning spray; 24 bottles at 9.27 USD\n- invoice total: 11,373.84 USD\n\nPurchase order EQP-6395 from Cobalt Rubber Mats\n- line 1: whey powder; 72 bags at 154.69 USD\n- line 2: cleaning spray; 24 bottles at 9.84 USD\n- order total: 11,373.84 USD\n\nGoods receipt RCD-8402\n- line 1: received 72 bags\n- line 2: received 24 bottles",
  "question": "Under this policy, does invoice SUB-52706 end at a hold, a review, a rejection, or a routing to a senior approver?",
  "definitions": "Brickhollow Fitness Group AP policy: each invoice gets exactly one action.\n- Price: invoiced unit price minus PO unit price is less than 0.20 USD on every line. If it fails: price-variance review.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Approval limit: invoice total is any amount smaller than 11,373.85 USD (limit of approver Ravi Thakur). If it fails: route to a senior approver.\nCheck order: price, then quantity, then approval limit.\nThe first check in the check order that fails decides the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q40b988493c",
  "kind": "yes/no",
  "text": "Felix Oyelaran typing from the desk: here is the warehouse team bundle, the Brackenridge Rubber Goods invoice RLI-15365 alongside purchase order RLP-9525, pasted below.\n\nPurchase order RLP-9525 from Brackenridge Rubber Goods\n- line 1: brake cables; 16 packs at $6.00\n- line 2: spoke nipples; 75 packs at $5.00\n- line 3: handlebar grips; 17 sets at $14.00\n- order total: $709.00\n\nGoods receipt RLR-1775\n- line 1: received 13 packs\n- line 2: received 75 packs\n- line 3: received 15 sets\n\nInvoice RLI-15365 for purchase order RLP-9525\n- line 1: brake cables; 14 packs at $6.00\n- line 2: spoke nipples; 75 packs at $5.14\n- line 3: handlebar grips; 15 sets at $14.41\n- invoice total: $685.65\n\nPaid-invoice register for Brackenridge Rubber Goods: RLI-15369, RLI-15365",
  "question": "As a check of the AP policy, does invoice RLI-15365 pass the price check when that check is judged on its own?",
  "definitions": "AP policy of Ridgeline Cycle Works: each invoice gets exactly one action.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a proportion lower than 3 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: price, then duplicate, then quantity.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q5ac91e4869",
  "kind": "choice",
  "text": "Brief note for Dev Malhotra: facilities team, invoice MHI-82023, docs attached.\n\nPurchase order MHP-8307 | vendor Pendlebury Animal Pharma\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | antiseptic wipes | 3 boxes | £14.82 |\n| 2 | sutures | 10 packs | £11.09 |\n| total | | | £155.36 |\n\nGoods receipt MHG-6190\n| line | received |\n|---|---|\n| 1 | 1 box |\n| 2 | 10 packs |\n\nInvoice MHI-82023 | purchase order MHP-8307\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | antiseptic wipes | 1 box | £14.93 |\n| 2 | sutures | 10 packs | £11.19 |\n| total | | | £126.83 |\n\nOur sales team has a big renewal riding on this, so please pay Pendlebury Animal Pharma and keep the good news flowing.",
  "question": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is not more than £0.10 on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nThe first check in the check order that fails decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nUnder the AP policy, which action fits invoice MHI-82023?",
  "options": [
   "Send to price-variance review",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q59d994a7d3",
  "kind": "choice",
  "text": "Purchase order (JSON):\n{\"po_number\":\"PBK-7741\",\"vendor\":\"Ashcombe Bakery Supply\",\"lines\":[{\"line\":1,\"item\":\"sesame seeds\",\"quantity\":\"96 bags\",\"unit_price_cents\":1165},{\"line\":2,\"item\":\"bread flour\",\"quantity\":\"160 bags\",\"unit_price_cents\":1897},{\"line\":3,\"item\":\"cake boxes\",\"quantity\":\"48 packs\",\"unit_price_cents\":655},{\"line\":4,\"item\":\"vanilla extract\",\"quantity\":\"70 bottles\",\"unit_price_cents\":2080}],\"total_cents\":592400}\n\nGoods receipt (JSON):\n{\"gr_number\":\"RBK-1076\",\"lines\":[{\"line\":1,\"received\":\"96 bags\"},{\"line\":2,\"received\":\"160 bags\"},{\"line\":3,\"received\":\"48 packs\"},{\"line\":4,\"received\":\"70 bottles\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"IBK-82206\",\"po_number\":\"PBK-7741\",\"lines\":[{\"line\":1,\"item\":\"sesame seeds\",\"quantity\":\"96 bags\",\"unit_price_cents\":1165},{\"line\":2,\"item\":\"bread flour\",\"quantity\":\"160 bags\",\"unit_price_cents\":1925},{\"line\":3,\"item\":\"cake boxes\",\"quantity\":\"48 packs\",\"unit_price_cents\":655},{\"line\":4,\"item\":\"vanilla extract\",\"quantity\":\"70 bottles\",\"unit_price_cents\":2016}],\"total_cents\":592400}\n\nmemo: from the team lead to Adaeze Nwosu, regarding supplier Ashcombe Bakery Supply\nscope: the field service team\ndocs: attached for matching",
  "question": "AP policy of Golden Crumb Bakeries: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is at or below $0.25 on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: price, then quantity.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nCan you tell me which line of invoice IBK-82206, if any, fails the price check?",
  "options": [
   "cake boxes",
   "vanilla extract",
   "bread flour",
   "sesame seeds",
   "None of the lines"
  ]
 },
 {
  "qid": "qf457d16526",
  "kind": "yes/no",
  "text": "From: Priya Raman. To: AP lead.\nSubject: facilities team, PO BMR-4860, papers attached for matching.\n\nPurchase order BMR-4860 from Ashdown Parts Direct\n- line 1: spark plugs; 181 boxes at 10.91 GBP\n- line 2: windscreen wipers; 10 packs at 12.56 GBP\n- order total: 2,100.31 GBP\n\nGoods receipt BGN-6641\n- line 1: received 181 boxes\n- line 2: received 9 packs\n\nInvoice BVI-17274 for purchase order BMR-4860\n- line 1: spark plugs; 181 boxes at 11.11 GBP\n- line 2: windscreen wipers; 8 packs at 12.75 GBP\n- invoice total: 2,112.91 GBP",
  "question": "Would price-variance review be the only step the card takes on invoice BVI-17274?",
  "definitions": "AP policy of Brackley Motor Repairs: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is any amount smaller than 0.20 GBP on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nThe action is fixed by the first failing check in the check order, and a later check does not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q9e1fe3cd49",
  "kind": "yes/no",
  "text": "[warm-note] hello Gregor Mackie, the warehouse team lead here, invoice BCV-80397 from Wexcombe Janitorial Supply is attached for matching, big thanks\n\nPurchase order BCP-6273 from Wexcombe Janitorial Supply\n- line 1: mop heads; 96 units at 5.78 GBP\n- line 2: bin liners; 148 rolls at 6.02 GBP\n- order total: 1,445.84 GBP\n\nGoods receipt BCR-4602\n- line 1: received 95 units\n- line 2: received 145 rolls\n\nInvoice BCV-80397 for purchase order BCP-6273\n- line 1: mop heads; 96 units at 5.92 GBP\n- line 2: bin liners; 145 rolls at 6.02 GBP\n- invoice total: 1,441.22 GBP\n\nPaid-invoice register for Wexcombe Janitorial Supply: BCV-80297, BCV-96998",
  "question": "So is invoice BCV-80397 not released for payment under the policy?",
  "definitions": "AP policy of Brightstone Office Care: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is any amount smaller than 0.15 GBP on every line. If it fails: price-variance review.\n2. Approval-limit check: the invoice total is lower than 1,441.23 GBP (limit of approver Walid Karam). If it fails: route to a senior approver.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n4. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then approval limit, then duplicate, then quantity.\nWalk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q94f09d55f8",
  "kind": "yes/no",
  "text": "Brief: Tanya Obi, laboratory team, Wexcombe Janitorial Supply, invoice BCV-82664. Attached for matching.\n\nPurchase order BCP-9731 from Wexcombe Janitorial Supply\n- line 1: hand soap; 4 bottles at 5.42 GBP\n- line 2: glass cleaner; 80 bottles at 4.95 GBP\n- order total: 417.68 GBP\n\nGoods receipt BCR-1797\n- line 1: received 3 bottles\n- line 2: received 78 bottles\n\nInvoice BCV-82664 for purchase order BCP-9731\n- line 1: hand soap; 3 bottles at 5.16 GBP\n- line 2: glass cleaner; 78 bottles at 4.78 GBP\n- invoice total: 388.32 GBP\n\nPaid-invoice register for Wexcombe Janitorial Supply: BCV-82464, BCV-36469, BCV-73435, BCV-89304",
  "question": "Under the policy, is invoice BCV-82664 blocked from payment?",
  "definitions": "AP policy of Brightstone Office Care: each invoice gets exactly one action.\n- Approval-limit check: the invoice total is below 388.32 GBP (limit of approver Eleanor Hughes). If it fails: route to a senior approver.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price check: invoiced unit price minus PO unit price is at most 0.10 GBP on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: approval limit, then quantity, then price, then duplicate.\nWork through the check order, and when you find the first failing check, use it to set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q29bc86524b",
  "kind": "yes/no",
  "text": "from: Sunniva Haugland\nto: AP lead, you are a joy to work with\ndocs: papers from Cassivelan Diagnostics for the warehouse team\nrefs: purchase order EPU-9318 and supplier invoice EVR-67101, forwarded for matching\n\nPurchase order EPU-9318 from Cassivelan Diagnostics\n- line 1: hand sanitiser; 45 bottles at 3.20 EUR\n- line 2: surgical gloves; 130 boxes at 15.80 EUR\n- order total: 2,198.00 EUR\n\nGoods receipt EGN-2346\n- line 1: received 42 bottles\n- line 2: received 130 boxes\n\nInvoice EVR-67101 for purchase order EPU-9318\n- line 1: hand sanitiser; 42 bottles at 3.35 EUR\n- line 2: surgical gloves; 130 boxes at 16.59 EUR\n- invoice total: 2,297.40 EUR",
  "question": "Checking how the policy treats invoice EVR-67101: does it pass the price check taken on its own?",
  "definitions": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a portion that sits below five percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nRead the check order from its start and apply the first failing check you reach to the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q5997486c09",
  "kind": "choice",
  "text": "Hey, Yara Nassar here for the AP lead, the laboratory purchase documents are attached below for matching.\n\nInvoice SUB-34132 for purchase order EQP-6352\n- line 1: kettlebells; 70 units at $30.34\n- invoice total: $2,123.80\n\nPurchase order EQP-6352 from Cobalt Rubber Mats\n- line 1: kettlebells; 72 units at $28.99\n- order total: $2,087.28\n\nGoods receipt RCD-1199\n- line 1: received 70 units",
  "question": "AP policy of Brickhollow Fitness Group: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Approval-limit check: the invoice total is falling short of $5,000.00 (limit of approver Esme Walsh). If it fails: route to a senior approver.\n3. Price check: invoiced unit price minus PO unit price is $1.00 or less on every line. If it fails: price-variance review.\nCheck order: quantity, then approval limit, then price.\nWhen a check fails in the check order, the first such failure decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nAnswer codes: Kestrel = release for payment, Osprey = hold for receipt, Plover = price-variance review, Heron = route to a senior approver.\nNothing else applies: the policy and the documents shown are complete.\n\nThe card sets an action for invoice SUB-34132, but which?",
  "options": [
   "Osprey",
   "Kestrel",
   "Plover",
   "Heron"
  ]
 },
 {
  "qid": "q89b9b62f40",
  "kind": "yes/no",
  "text": "Purchase order export, po_number DPO-4278, vendor Vanterpool Athletic Goods\nline,item,quantity,unit_price\n1,whiteboard markers,20 packs,6.61\ntotal,,,132.20\n\nGoods receipt export, gr_number DGR-7061\nline,received\n1,20 packs\n\nInvoice export, invoice_number DIV-36820, po_number DPO-4278\nline,item,quantity,unit_price\n1,whiteboard markers,20 packs,6.71\ntotal,,,134.20\n\n{\"to\": \"Rhea Delacroix\", \"from\": \"receiving dock\", \"team\": \"marketing\", \"forwarded\": \"Supplier invoice DIV-36820 from Vanterpool Athletic Goods is forwarded for matching.\"}",
  "question": "Would a new AP clerk find invoice DIV-36820 released for payment by the policy?",
  "definitions": "AP policy of Maple Ridge School District: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is equal to or below $0.10 on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: price, then quantity.\nWalk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q1e61853e4d",
  "kind": "choice",
  "text": "Hi Priya Raman,\nLovely to share the facilities documents, attached for matching.\nWarm wishes,\nTeam assistant\n\nPurchase order BMR-8314 from Ashdown Parts Direct\n- line 1: cleaning rags; 48 bags at £10.78\n- line 2: spark plugs; 180 boxes at £18.55\n- line 3: windscreen wipers; three packs at £13.44\n- order total: £3,896.76\n\nGoods receipt BGN-3503\n- line 1: received 45 bags\n- line 2: received 179 boxes\n- line 3: received two packs\n\nInvoice BVI-52020 for purchase order BMR-8314\n- line 1: cleaning rags; 45 bags at £11.13\n- line 2: spark plugs; 179 boxes at £18.62\n- line 3: windscreen wipers; three packs at £13.69\n- invoice total: £3,874.90",
  "question": "AP policy of Brackley Motor Repairs: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is at most £0.25 on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nCould you tell a new clerk what action the card gives invoice BVI-52020?",
  "options": [
   "Release for payment",
   "Send to price-variance review",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q651f1119d7",
  "kind": "yes/no",
  "text": "Stefan Kowal,\nDocs for the marketing team, pasted below.\nCheers.\n\nInvoice SIG-47566 for purchase order ORQ-7623\n- line 1: foam windscreens; 14 packs at 20.03 USD\n- invoice total: 280.42 USD\n\nPurchase order ORQ-7623 from Merrin Studio Acoustics\n- line 1: foam windscreens; 16 packs at 20.00 USD\n- order total: 320.00 USD\n\nGoods receipt GRT-1062\n- line 1: received 14 packs",
  "question": "Is invoice SIG-47566 released for payment?",
  "definitions": "AP policy of Wrenfield Community Radio: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Approval-limit check: the invoice total is less than 1,000.00 USD (limit of approver Marisol Ortega). If it fails: route to a senior approver.\n3. Price check: invoiced unit price minus PO unit price is a portion smaller than or the same as 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then approval limit, then price.\nA later check in the check order does not change an action that is already decided.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q0a29be0cf7",
  "kind": "yes/no",
  "text": "Yvette Dubois, the laboratory team. Papers pasted below. Merrin Studio Acoustics, invoice SIG-11598.\n\nInvoice SIG-11598 for purchase order ORQ-1922\n- line 1: foam windscreens; 7 packs at $20.20\n- invoice total: $141.40\n\nPaid-invoice register for Merrin Studio Acoustics: SIG-54345, SIG-99227, SIG-20078\n\nPurchase order ORQ-1922 from Merrin Studio Acoustics\n- line 1: foam windscreens; 6 packs at $20.00\n- order total: $120.00\n\nGoods receipt GRT-2863\n- line 1: received 6 packs",
  "question": "Is invoice SIG-11598 released to be paid under the card?",
  "definitions": "AP policy of Wrenfield Community Radio: each invoice gets exactly one action.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a portion equal to or smaller than 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: price, then quantity, then duplicate.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qeec0b45bb8",
  "kind": "choice",
  "text": "Clerk: Good to speak with you, this is Ines Carvalho from the AP team, writing about the marketing team purchase.\nCaller: Thank you kindly for the call. The documents from Ludlow Rigging Hire are being forwarded for matching, namely supplier invoice BLS-40967 and purchase order POF-7344.\n\nInvoice BLS-40967 for purchase order POF-7344\n- line 1: gaffer tape; 22 rolls at £11.18\n- line 2: lighting gels; 73 packs at £8.97\n- line 3: camera batteries; 113 packs at £52.50\n- line 4: stage blood; 103 bottles at £13\n- invoice total: £8,172.27\n\nPurchase order POF-7344 from Ludlow Rigging Hire\n- line 1: gaffer tape; 24 rolls at £11\n- line 2: lighting gels; 75 packs at £9\n- line 3: camera batteries; 113 packs at £55\n- line 4: stage blood; 106 bottles at £13\n- order total: £8,532\n\nGoods receipt GRF-8267\n- line 1: received 22 rolls\n- line 2: received 73 packs\n- line 3: received 113 packs\n- line 4: received 103 bottles",
  "question": "AP policy of Greywick Film Studios: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a portion that sits below three percent of the PO unit price on every line. If it fails: price-variance review.\n- Approval-limit check: the invoice total is £9,100.74 or lower (limit of approver Brynja Sigurdsson). If it fails: route to a senior approver.\nCheck order: price, then approval limit, then quantity.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nCould a colleague trace how the AP policy handles invoice BLS-40967, and which action follows?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment",
   "Route to a senior approver"
  ]
 },
 {
  "qid": "q392a652226",
  "kind": "choice",
  "text": "Hi laboratory team.\nTeresa Llorente here, with the purchase paperwork attached for matching.\n\nPurchase order EPU-2013 from Cassivelan Diagnostics\n- line 1: surgical gloves; 30 boxes at 11.00 EUR\n- line 2: syringes; 150 boxes at 9.00 EUR\n- order total: 1,680.00 EUR\n\nGoods receipt EGN-2936\n- line 1: received 29 boxes\n- line 2: received 148 boxes\n\nInvoice EVR-20994 for purchase order EPU-2013\n- line 1: surgical gloves; 27 boxes at 11.11 EUR\n- line 2: syringes; 148 boxes at 9.08 EUR\n- invoice total: 1,643.81 EUR",
  "question": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a fraction that remains smaller than 1 percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe action follows from the first check that fails when the checks are taken in the check order.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nAnswer codes: Heron = release for payment, Osprey = hold for receipt, Plover = price-variance review.\nNothing else applies: the policy and the documents shown are complete.\n\nFrom the card, what action must invoice EVR-20994 get?",
  "options": [
   "Osprey",
   "Plover",
   "Heron"
  ]
 },
 {
  "qid": "q6aeb6a4ad6",
  "kind": "choice",
  "text": "Purchase order export, po_number TPB-7310, vendor Stillwater Glass Packaging\nline,item,quantity,unit_price\n1,cask cleaner,72 bottles,11.00\n2,bottle caps,80 packs,7.00\n3,hop pellets,195 bags,36.00\ntotal,,,8372.00\n\nGoods receipt export, gr_number TGB-1271\nline,received\n1,72 bottles\n2,80 packs\n3,195 bags\n\nInvoice export, invoice_number TIB-44636, po_number TPB-7310\nline,item,quantity,unit_price\n1,cask cleaner,72 bottles,11.00\n2,bottle caps,80 packs,7.00\n3,hop pellets,195 bags,36.00\ntotal,,,8372.00\n\ntopic: supplier Stillwater Glass Packaging, invoice TIB-44636\nteam: for the IT support team\nto: Imogen Clarke\nfrom: team assistant",
  "question": "AP policy of Millrace Brewing Company: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is a proportion that is less than 3 percent of the PO unit price on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: price, then quantity.\nApply the check order in sequence, and let the first check that fails determine the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhat is the action this policy gives invoice TIB-44636?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q6776d722f5",
  "kind": "choice",
  "text": "Raised by: office manager. For the facilities team.\nSubject: Gregor Mackie, invoice BCV-14188 forwarded for matching.\n\nPurchase order BCP-7131 from Gilmour Mop Company\n- line 1: floor wax; 40 drums at £104.06\n- line 2: bin liners; 77 rolls at £6.35\n- order total: £4,651.35\n\nGoods receipt BCR-1874\n- line 1: received 40 drums\n- line 2: received 75 rolls\n\nInvoice BCV-14188 for purchase order BCP-7131\n- line 1: floor wax; 40 drums at £104.06\n- line 2: bin liners; 75 rolls at £6.35\n- invoice total: £4,638.65",
  "question": "AP policy of Brightstone Office Care: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is beneath £0.20 on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhat's the move for invoice BCV-14188 according to the rules?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q3720106f63",
  "kind": "yes/no",
  "text": "Lead note. Sophie Bramble, marketing side. Supplier invoice SPV-59440 from Velden Glass Co, forwarded for matching.\n\nInvoice SPV-59440 for purchase order PRQ-1533\n- line 1: bottling labels; 161 rolls at 14.65 USD\n- line 2: barrel hoops; 92 sets at 23.07 USD\n- invoice total: 4,481.09 USD\n\nPaid-invoice register for Velden Glass Co: SPV-42853, SPV-60728\n\nPurchase order PRQ-1533 from Velden Glass Co\n- line 1: bottling labels; 163 rolls at 13.96 USD\n- line 2: barrel hoops; 94 sets at 23.07 USD\n- order total: 4,444.06 USD\n\nGoods receipt GRZ-2696\n- line 1: received 161 rolls\n- line 2: received 93 sets",
  "question": "Taking only the price check on its own, does this policy have invoice SPV-59440 fail that check?",
  "definitions": "AP policy of Ambersett Wine Cellars: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is beneath 0.20 USD on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Approval-limit check: the invoice total is at or below 25,000.00 USD (limit of approver Anaya Iyer). If it fails: route to a senior approver.\n4. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then quantity, then approval limit, then duplicate.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q847ad6044d",
  "kind": "choice",
  "text": "Purchase order (JSON):\n{\"po_number\":\"PBK-8574\",\"vendor\":\"Copperleaf Dairy Cooperative\",\"lines\":[{\"line\":1,\"item\":\"sesame seeds\",\"quantity\":\"36 bags\",\"unit_price_cents\":1442},{\"line\":2,\"item\":\"bread flour\",\"quantity\":\"17 bags\",\"unit_price_cents\":1860},{\"line\":3,\"item\":\"butter\",\"quantity\":\"144 cases\",\"unit_price_cents\":12387}],\"total_cents\":1867260}\n\nGoods receipt (JSON):\n{\"gr_number\":\"RBK-2968\",\"lines\":[{\"line\":1,\"received\":\"36 bags\"},{\"line\":2,\"received\":\"17 bags\"},{\"line\":3,\"received\":\"144 cases\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"IBK-85922\",\"po_number\":\"PBK-8574\",\"lines\":[{\"line\":1,\"item\":\"sesame seeds\",\"quantity\":\"36 bags\",\"unit_price_cents\":1442},{\"line\":2,\"item\":\"bread flour\",\"quantity\":\"17 bags\",\"unit_price_cents\":1860},{\"line\":3,\"item\":\"butter\",\"quantity\":\"144 cases\",\"unit_price_cents\":12400}],\"total_cents\":1869132}\n\nPaid-invoice register (JSON):\n{\"vendor\":\"Copperleaf Dairy Cooperative\",\"paid_invoice_numbers\":[\"IBK-25607\",\"IBK-85922\",\"IBK-38667\"]}\n\n{\"to\": \"Rosalind Fenner\",\n\"from\": \"office manager\",\n\"note\": \"Forwarded for matching: purchase order PBK-8574 and the Copperleaf Dairy Cooperative invoice for the laboratory team.\"}",
  "question": "Golden Crumb Bakeries AP policy: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Approval limit | invoice total is 25,000.00 USD or lower (limit of approver Benedikt Roth) | route to a senior approver |\n| Price | invoiced unit price minus PO unit price is beneath 0.15 USD on every line | price-variance review |\n| Quantity | invoiced quantity at most received quantity on every line | hold for receipt |\n| Duplicate | invoice number not in the paid-invoice register (exact match only) | reject as a duplicate |\nCheck order: approval limit, then price, then quantity, then duplicate.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nChecking how this policy treats invoice IBK-85922, which line, if any, fails the price check?",
  "options": [
   "None of the lines",
   "butter",
   "bread flour",
   "sesame seeds"
  ]
 },
 {
  "qid": "q5047ee9921",
  "kind": "yes/no",
  "text": "Caller: Team assistant here, for the IT support team.\nClerk: Dev Malhotra, AP. Documents from Pendlebury Animal Pharma are being sent over, with purchase order MHP-1161.\n\nPurchase order MHP-1161 | vendor Pendlebury Animal Pharma\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | sutures | 5 packs | £9.99 |\n| 2 | antiseptic wipes | 20 boxes | £8.91 |\n| total | | | £228.15 |\n\nGoods receipt MHG-3040\n| line | received |\n|---|---|\n| 1 | 5 packs |\n| 2 | 17 boxes |\n\nInvoice MHI-15295 | purchase order MHP-1161\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | sutures | 5 packs | £10.19 |\n| 2 | antiseptic wipes | 17 boxes | £9.09 |\n| total | | | £205.48 |",
  "question": "Would you say it is not true that invoice MHI-15295 is not released for payment under the policy?",
  "definitions": "Meadowsend Animal Hospital AP policy: each invoice gets exactly one action.\n1. Price: invoiced unit price minus PO unit price is short of £0.20 on every line. If it fails: price-variance review.\n2. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n3. Approval limit: invoice total is at or below £146.76 (limit of approver Nomvula Dube). If it fails: route to a senior approver.\nCheck order: price, then quantity, then approval limit.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q2e827f0a01",
  "kind": "choice",
  "text": "dear: Aoife Brennan\nabout: papers from Stratocore Networking for the laboratory team\nend: forwarded for matching, team lead\n\nPurchase order PQS-3055 | vendor Stratocore Networking\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | keyboards | 180 units | $32.73 |\n| total | | | $5,891.40 |\n\nGoods receipt RQS-1609\n| line | received |\n|---|---|\n| 1 | 180 units |\n\nInvoice IQS-22217 | purchase order PQS-3055\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | keyboards | 180 units | $32.56 |\n| total | | | $5,860.80 |\n\nPaid-invoice register | vendor Stratocore Networking\n| invoice number |\n|---|\n| IQS-22217 |\n| IQS-22214 |",
  "question": "Quorin Digital Services AP policy: each invoice gets exactly one action.\n1. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n2. Approval limit: invoice total is no more than $5,860.80 (limit of approver Hannah Lindau). If it fails: route to a senior approver.\n3. Price: invoiced unit price minus PO unit price is beneath $0.50 on every line. If it fails: price-variance review.\n4. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: quantity, then approval limit, then price, then duplicate.\nThe action is set by the first failing check in the check order.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich line on invoice IQS-22217 fails the price check, if any?",
  "options": [
   "None of the lines",
   "keyboards"
  ]
 },
 {
  "qid": "qcd602e58d4",
  "kind": "choice",
  "text": "Office note for Sunniva Haugland. Here is the IT support team set, with the purchase order EPU-5438 pasted below.\n\nPurchase order EPU-5438 from Cassivelan Diagnostics\n- line 1: bandage rolls; 128 rolls at €3.00\n- line 2: syringes; 96 boxes at €4.00\n- line 3: waiting room chairs; 200 units at €112.00\n- order total: €23,168.00\n\nGoods receipt EGN-8983\n- line 1: received 128 rolls\n- line 2: received 95 boxes\n- line 3: received 200 units\n\nInvoice EVR-53956 for purchase order EPU-5438\n- line 1: bandage rolls; 128 rolls at €2.94\n- line 2: syringes; 96 boxes at €4.08\n- line 3: waiting room chairs; 200 units at €112.00\n- invoice total: €23,168.00",
  "question": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a portion smaller than or the same as 1 percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nKeep to the check order, halt at the first failing check, and set the action from that check alone.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nLooking at all of it, what should we do with invoice EVR-53956?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "qfcfc3c26ac",
  "kind": "yes/no",
  "text": "Clerk: Ines Carvalho here, reaching out for the field service purchase.\nCaller: Thank you kindly. The paperwork is pasted below for matching.\n\nInvoice BLS-74301 for purchase order POF-6595\n- line 1: gaffer tape; 30 rolls at 9.00 GBP\n- line 2: stage blood; 38 bottles at 18.80 GBP\n- line 3: sandbags; 120 units at 8.38 GBP\n- invoice total: 1,990.00 GBP\n\nPurchase order POF-6595 from Sable Costume Works\n- line 1: gaffer tape; 30 rolls at 9.00 GBP\n- line 2: stage blood; 38 bottles at 20.00 GBP\n- line 3: sandbags; 120 units at 8.00 GBP\n- order total: 1,990.00 GBP\n\nGoods receipt GRF-8980\n- line 1: received 30 rolls\n- line 2: received 38 bottles\n- line 3: received 120 units",
  "question": "Does the AP policy send invoice BLS-74301 to price-variance review, with that being the sole action the invoice gets?",
  "definitions": "AP policy of Greywick Film Studios: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is a proportion that equals or is lower than 3 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nKeep to the check order, halt at the first failing check, and set the action from that check alone.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q3580ccf5f5",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"FSP-3212\",\"vendor\":\"Blackmore Meter Supplies\",\"lines\":[{\"line\":1,\"item\":\"diesel\",\"quantity\":\"27 drums\",\"unit_price_cents\":27884},{\"line\":2,\"item\":\"cable glands\",\"quantity\":\"40 packs\",\"unit_price_cents\":576},{\"line\":3,\"item\":\"hose clamps\",\"quantity\":\"10 packs\",\"unit_price_cents\":872}],\"total_cents\":784628}\n\nGoods receipt (JSON):\n{\"gr_number\":\"FSG-4699\",\"lines\":[{\"line\":1,\"received\":\"27 drums\"},{\"line\":2,\"received\":\"37 packs\"},{\"line\":3,\"received\":\"10 packs\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"FSV-95691\",\"po_number\":\"FSP-3212\",\"lines\":[{\"line\":1,\"item\":\"diesel\",\"quantity\":\"28 drums\",\"unit_price_cents\":27888},{\"line\":2,\"item\":\"cable glands\",\"quantity\":\"37 packs\",\"unit_price_cents\":573},{\"line\":3,\"item\":\"hose clamps\",\"quantity\":\"10 packs\",\"unit_price_cents\":877}],\"total_cents\":810835}\n\nPaid-invoice register (JSON):\n{\"vendor\":\"Blackmore Meter Supplies\",\"paid_invoice_numbers\":[\"FSV-15616\",\"FSV-58760\",\"FSV-87559\"]}\n\n[quick-chat] ap intern here, writing to Nicolette Bauer for the facilities team, po FSP-3212 from Blackmore Meter Supplies forwarded for matching, thanks again",
  "question": "So does invoice FSV-95691 fail the price check when you look at that check on its own?",
  "definitions": "AP policy of Tidewater Field Services: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Price check | invoiced unit price minus PO unit price is strictly lower than £0.05 on every line | price-variance review |\nCheck order: duplicate, then price, then quantity.\nWhen a check fails in the check order, the first such failure decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qb5243753cd",
  "kind": "choice",
  "text": "Documents for the marketing team purchase are attached. From Yvette Dubois, AP.\n\nInvoice SIG-89085 for purchase order ORQ-4537\n- line 1: broadcast tape; eight rolls at 4.00 USD\n- line 2: audio valves; 101 units at 113.00 USD\n- invoice total: 11,445.00 USD\n\nPurchase order ORQ-4537 from Merrin Studio Acoustics\n- line 1: broadcast tape; eight rolls at 4.00 USD\n- line 2: audio valves; 101 units at 113.00 USD\n- order total: 11,445.00 USD\n\nGoods receipt GRT-9935\n- line 1: received eight rolls\n- line 2: received 101 units",
  "question": "Wrenfield Community Radio AP policy: each invoice gets exactly one action.\n1. Price: invoiced unit price minus PO unit price is a proportion lower than one percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n3. Approval limit: invoice total is no more than 25,000.00 USD (limit of approver Dagny Solberg). If it fails: route to a senior approver.\nCheck order: price, then quantity, then approval limit.\nThe action stands once it is set, because checks that come later in the check order do not change it.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does the policy tell us to take for invoice SIG-89085?",
  "options": [
   "Route to a senior approver",
   "Send to price-variance review",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qf951882ba6",
  "kind": "yes/no",
  "text": "Hello,\nThe facilities team purchase is under PO FPO-8903. Supplier invoice FSI-52718 is attached for matching.\nRegards,\nHaruka Sakai\n\nInvoice FSI-52718 for purchase order FPO-8903\n- line 1: mineral blocks; 1 pallet at £92.62\n- line 2: seed potatoes; 2 bags at £38.48\n- invoice total: £169.58\n\nPaid-invoice register for Havenbrook Tractor Parts: FSI-20823, FSI-80869\n\nPurchase order FPO-8903 from Havenbrook Tractor Parts\n- line 1: mineral blocks; 2 pallets at £92.55\n- line 2: seed potatoes; 5 bags at £37.99\n- order total: £375.05\n\nGoods receipt FGR-5735\n- line 1: received 2 pallets\n- line 2: received 5 bags",
  "question": "Does the card clear invoice FSI-52718 for payment?",
  "definitions": "AP policy of Marrowdale Farm Cooperative: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is smaller than £0.50 on every line. If it fails: price-variance review.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: quantity, then price, then duplicate.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q3b19a9132d",
  "kind": "choice",
  "text": "Clerk: Hello, Declan Quigley from the AP team is the clerk handling this file.\nCaller: Lovely, we are the warehouse team, and this is appreciated.\nClerk: Thank you kindly, the documents are being sent along. Supplier invoice FSI-71310 from Brackley Seed Merchants sits alongside purchase order FPO-5416.\n\nInvoice FSI-71310 for purchase order FPO-5416\n- line 1: sheep dip; twenty drums at 300.40 GBP\n- invoice total: £6,008\n\nPaid-invoice register for Brackley Seed Merchants: FSI-71310, FSI-75715, FSI-12078\n\nPurchase order FPO-5416 from Brackley Seed Merchants\n- line 1: sheep dip; 24 drums at 295.45 GBP\n- order total: 7,090.80 GBP\n\nGoods receipt FGR-9137\n- line 1: received 21 drums",
  "question": "AP policy of Marrowdale Farm Cooperative: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is £5 or less on every line. If it fails: price-variance review.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity, then duplicate.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhat is the action this policy gives invoice FSI-71310?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Send to price-variance review",
   "Reject as a duplicate"
  ]
 },
 {
  "qid": "q47b9dad257",
  "kind": "yes/no",
  "text": "Hey Yara Benitez, heads up: the IT support purchase papers are pasted below for matching. Thanks!\n\nPurchase order RLP-1036 from Velloway Gear Systems\n- line 1: inner tubes; 114 units at $9\n- line 2: grease; 36 tubes at $4\n- line 3: spoke nipples; 188 packs at $3\n- order total: $1,734\n\nGoods receipt RLR-6773\n- line 1: received 114 units\n- line 2: received 36 tubes\n- line 3: received 188 packs\n\nInvoice RLI-69883 for purchase order RLP-1036\n- line 1: inner tubes; 114 units at $9\n- line 2: grease; 36 tubes at $4\n- line 3: spoke nipples; 188 packs at $3\n- invoice total: $1,734",
  "question": "Being new to AP, does the card say invoice RLI-69883 is released for payment?",
  "definitions": "AP policy of Ridgeline Cycle Works: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a portion lower than 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nWork through the check order, and when you find the first failing check, use it to set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q1f9e9070ed",
  "kind": "choice",
  "text": "Caller: Hello there, the laboratory team says hi!\nClerk: Hi to you too. Dev Malhotra from AP is happy to send the paperwork over.\n\nPurchase order MHP-2306 | vendor Crestline Surgical Instruments\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | dog food | 3 bags | 41.18 GBP |\n| 2 | sutures | 10 packs | 15.37 GBP |\n| total | | | 277.24 GBP |\n\nGoods receipt MHG-8479\n| line | received |\n|---|---|\n| 1 | 3 bags |\n| 2 | 10 packs |\n\nInvoice MHI-46378 | purchase order MHP-2306\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | dog food | 3 bags | 41.37 GBP |\n| 2 | sutures | 10 packs | 15.57 GBP |\n| total | | | 279.81 GBP |",
  "question": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is less than 0.20 GBP on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe first check in the check order that fails decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nDouble-checking the card, which action does it assign to invoice MHI-46378?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "q964a6b1608",
  "kind": "choice",
  "text": "Subject: lovely to be working with you, Connor Mbeki\nTeam: the warehouse team\nSupplier and PO: Carrow Lubricant Group, BMR-4042\nNote: papers are pasted below for matching, cheers.\n\nPurchase order BMR-4042 from Carrow Lubricant Group\n- line 1: coolant; 60 drums at £46.61\n- line 2: engine oil; 179 bottles at £13.67\n- line 3: cleaning rags; 36 bags at £5.87\n- order total: £5,454.85\n\nGoods receipt BGN-9089\n- line 1: received 60 drums\n- line 2: received 179 bottles\n- line 3: received 36 bags\n\nInvoice BVI-25561 for purchase order BMR-4042\n- line 1: coolant; 60 drums at £46.61\n- line 2: engine oil; 179 bottles at £13.67\n- line 3: cleaning rags; 36 bags at £5.87\n- invoice total: £5,454.85",
  "question": "AP policy of Brackley Motor Repairs: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is smaller than £0.10 on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nWhen a check fails in the check order, the first such failure decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nTell me, in plain words, which action the card gives invoice BVI-25561?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "q0b21787406",
  "kind": "choice",
  "text": "Purchase order export, po_number TPB-1122, vendor Corvane Hop Growers\nline,item,quantity,unit_price\n1,hop pellets,15 bags,26.00\n2,brewing yeast,36 packs,19.00\n3,pale malt,40 bags,34.00\ntotal,,,2434.00\n\nGoods receipt export, gr_number TGB-6874\nline,received\n1,15 bags\n2,35 packs\n3,38 bags\n\nInvoice export, invoice_number TIB-74551, po_number TPB-1122\nline,item,quantity,unit_price\n1,hop pellets,18 bags,26.22\n2,brewing yeast,33 packs,19.00\n3,pale malt,38 bags,34.00\ntotal,,,2390.96\n\n{\"to\": \"Tariq Syed\",\n\"from\": \"receiving dock\",\n\"note\": \"Papers for the marketing team came in with the Corvane Hop Growers shipment and the invoice TIB-74551. Pasted below.\"}",
  "question": "AP policy of Millrace Brewing Company: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is a proportion lower than 1 percent of the PO unit price on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: price, then quantity.\nA later check in the check order does not change an action that is already decided.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nCould a colleague trace how the AP policy handles invoice TIB-74551, and which action follows?",
  "options": [
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q638b06ce7d",
  "kind": "choice",
  "text": "{\"to\": \"Malik Osei\", \"from\": \"office manager\", \"note\": \"Documents for the laboratory team are attached for matching. The purchase order LPR-9696 from Quillon Packaging Group is in the set.\"}\n\nPurchase order LPR-9696 from Quillon Packaging Group\n- line 1: fabric softener; 113 bottles at 8.54 USD\n- line 2: laundry detergent; 72 drums at 68.25 USD\n- line 3: dryer sheets; 180 boxes at $7\n- order total: 7,139.02 USD\n\nGoods receipt LRC-2353\n- line 1: received 113 bottles\n- line 2: received 72 drums\n- line 3: received 180 boxes\n\nInvoice LBI-48934 for purchase order LPR-9696\n- line 1: fabric softener; 113 bottles at 8.54 USD\n- line 2: laundry detergent; 72 drums at 67.75 USD\n- line 3: dryer sheets; 180 boxes at 7.20 USD\n- invoice total: 7,139.02 USD\n\nPaid-invoice register for Quillon Packaging Group: LBI-48934, LBI-90813, LBI-27804",
  "question": "AP policy of Clearwater Linen Services: each invoice gets exactly one action.\n1. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n2. Price check: invoiced unit price minus PO unit price is 0.20 USD or less on every line. If it fails: price-variance review.\n3. Approval-limit check: the invoice total is smaller than $10,000 (limit of approver Elena Vasquez). If it fails: route to a senior approver.\n4. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: duplicate, then price, then approval limit, then quantity.\nTake the checks in the check order and let the first one that fails set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nCould you tell a new clerk what action the card gives invoice LBI-48934?",
  "options": [
   "Release for payment",
   "Route to a senior approver",
   "Send to price-variance review",
   "Reject as a duplicate",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q919adbc91b",
  "kind": "yes/no",
  "text": "Raised by: Dragana Petrovic\nTeam: the marketing team\nSupplier: Tamworth Roofing Supply\nReferences: invoice KBI-98321, PO KBP-4735, forwarded for matching.\n\nPurchase order KBP-4735 | vendor Tamworth Roofing Supply\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | plasterboard | 3 units | €15 |\n| 2 | silicone sealant | 60 tubes | €7 |\n| 3 | roof tiles | 45 pallets | €765 |\n| total | | | €34,890 |\n\nGoods receipt KBG-7493\n| line | received |\n|---|---|\n| 1 | 1 unit |\n| 2 | 59 tubes |\n| 3 | 42 pallets |\n\nInvoice KBI-98321 | purchase order KBP-4735\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | plasterboard | 1 unit | €14.66 |\n| 2 | silicone sealant | 60 tubes | €7 |\n| 3 | roof tiles | 41 pallets | €787.94 |\n| total | | | €32,740.20 |",
  "question": "Taking only the price check on its own, does this policy have invoice KBI-98321 fail that check?",
  "definitions": "AP policy of Hartwell Build Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a share that is lower than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe earliest failing check in the check order settles the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q09d5a5edf4",
  "kind": "choice",
  "text": "{\"to\": \"Grete Lund\", \"from\": \"team lead\", \"note\": \"So glad you are on this, truly. Warm wishes to you, and the marketing team papers go along for matching.\"}\n\nPurchase order LPR-5255 | vendor Bellmere Detergent Works\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | stain remover | 187 bottles | 11.52 USD |\n| total | | | 2,154.24 USD |\n\nGoods receipt LRC-8264\n| line | received |\n|---|---|\n| 1 | 187 bottles |\n\nInvoice LBI-28707 | purchase order LPR-5255\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | stain remover | 190 bottles | 11.53 USD |\n| total | | | 2,190.70 USD |",
  "question": "AP policy of Clearwater Linen Services: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is at or below 0.10 USD on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nOnce a check fails in the check order, later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nUnder this policy, what becomes of invoice LBI-28707 as an action?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "q706146dded",
  "kind": "yes/no",
  "text": "Note for the file from Ilse Brandt.\nThis is for the laboratory team: PO LPO-3496, supplier invoice LSI-48200, papers attached for matching, happy to keep it on record.\n\nPurchase order LPO-3496 | vendor Corvin Ribbon Works\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | roses | 66 boxes | $26.00 |\n| 2 | floral foam | 144 packs | $7.00 |\n| 3 | ceramic vases | 177 units | $17.00 |\n| 4 | wire stems | 75 rolls | $10.00 |\n| total | | | $6,483.00 |\n\nGoods receipt LGR-5071\n| line | received |\n|---|---|\n| 1 | 66 boxes |\n| 2 | 144 packs |\n| 3 | 177 units |\n| 4 | 75 rolls |\n\nInvoice LSI-48200 | purchase order LPO-3496\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | roses | 66 boxes | $26.00 |\n| 2 | floral foam | 144 packs | $7.00 |\n| 3 | ceramic vases | 177 units | $17.00 |\n| 4 | wire stems | 75 rolls | $10.00 |\n| total | | | $6,483.00 |\n\nPaid-invoice register | vendor Corvin Ribbon Works\n| invoice number |\n|---|\n| LSI-72524 |\n| LSI-60303 |\n| LSI-61590 |",
  "question": "Does the policy decide that invoice LSI-48200 is released for payment?",
  "definitions": "AP policy of Larkspur Flower Group: each invoice gets exactly one action.\n1. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n2. Price check: invoiced unit price minus PO unit price is a proportion that equals or is lower than three percent of the PO unit price on every line. If it fails: price-variance review.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: duplicate, then price, then quantity.\nThe action stands once it is set, because checks that come later in the check order do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q22286f1ba3",
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
  "qid": "q94374a9515",
  "kind": "yes/no",
  "text": "Holcombe Tyre Supply sent a little package for the IT support team, Priya Raman: purchase order BMR-8481 is tucked in for matching.\n\nPurchase order BMR-8481 from Holcombe Tyre Supply\n- line 1: brake pads; 100 sets at 33.70 GBP\n- line 2: spark plugs; 50 boxes at 13.27 GBP\n- order total: 4,033.50 GBP\n\nGoods receipt BGN-2341\n- line 1: received 100 sets\n- line 2: received 50 boxes\n\nInvoice BVI-53353 for purchase order BMR-8481\n- line 1: brake pads; 100 sets at 33.70 GBP\n- line 2: spark plugs; 50 boxes at 13.27 GBP\n- invoice total: 4,033.50 GBP",
  "question": "Is it right that the policy releases invoice BVI-53353 for payment?",
  "definitions": "Brackley Motor Repairs AP policy: each invoice gets exactly one action.\n- Approval limit: invoice total is less than or equal to 10,000.00 GBP (limit of approver Sven Holm). If it fails: route to a senior approver.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Price: invoiced unit price minus PO unit price is less than 0.25 GBP on every line. If it fails: price-variance review.\nCheck order: price, then quantity, then approval limit.\nThe action is fixed by the first failing check in the check order, and a later check does not change it.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q571948bf19",
  "kind": "yes/no",
  "text": "Hey Nadia Haddad.\nPurchase for the laboratory team. Documents forwarded for matching.\nTa.\n\nPurchase order BMR-1144 from Carrow Lubricant Group\n- line 1: brake pads; 75 sets at 47.78 GBP\n- order total: 3,583.50 GBP\n\nGoods receipt BGN-7831\n- line 1: received 75 sets\n\nInvoice BVI-94201 for purchase order BMR-1144\n- line 1: brake pads; 75 sets at 46.94 GBP\n- invoice total: 3,520.50 GBP\n\nPaid-invoice register for Carrow Lubricant Group: BVI-36754, BVI-18136, BVI-94281",
  "question": "Is invoice BVI-94201 released for payment?",
  "definitions": "AP policy of Brackley Motor Repairs: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is any amount smaller than 0.75 GBP on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then quantity, then duplicate.\nWhen a check fails in the check order, the first such failure decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q34baec7be7",
  "kind": "choice",
  "text": "Purchase order export, po_number FSP-3449, vendor Ludgrove Safety Equipment\nline,item,quantity,unit_price\n1,pressure gauges,4 units,47.05\ntotal,,,188.20\n\nGoods receipt export, gr_number FSG-3919\nline,received\n1,4 units\n\nInvoice export, invoice_number FSV-15565, po_number FSP-3449\nline,item,quantity,unit_price\n1,pressure gauges,6 units,48.85\ntotal,,,293.10\n\nsubject: purchase order FSP-3449, the field service team\nfrom: billing contact\nto: Owen Pritchard\nfiles: attached, forwarded for matching",
  "question": "Tidewater Field Services AP policy: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity | invoiced quantity at most received quantity on every line | hold for receipt |\n| Price | invoiced unit price minus PO unit price is beneath 1.50 GBP on every line | price-variance review |\nCheck order: quantity, then price.\nA later check in the check order does not change an action that is already decided.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nPlease verify the policy's reading of invoice FSV-15565: which action does it apply?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "q41071a80f1",
  "kind": "choice",
  "text": "Purchase order export, po_number PFM-2374, vendor Peverell Cleaning Chemicals\nline,item,quantity,unit_price\n1,light bulbs,40 boxes,42.60\n2,sealant tubes,15 tubes,5.60\ntotal,,,1788.00\n\nGoods receipt export, gr_number RFM-6277\nline,received\n1,37 boxes\n2,14 tubes\n\nInvoice export, invoice_number IFM-74120, po_number PFM-2374\nline,item,quantity,unit_price\n1,light bulbs,37 boxes,42.52\n2,sealant tubes,14 tubes,5.60\ntotal,,,1651.64\n\n{\"to\": \"Adwoa Boateng\", \"from\": \"office manager\", \"team\": \"marketing\", \"docs\": \"Pasted below are the papers from Peverell Cleaning Chemicals and the purchase order PFM-2374. Thank you.\"}",
  "question": "AP policy of Brenton Estate Services: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Approval-limit check | the invoice total is strictly lower than 2,500.00 EUR (limit of approver Stefan Lorentz) | route to a senior approver |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is a fraction that is smaller than five percent of the PO unit price on every line | price-variance review |\nCheck order: approval limit, then quantity, then price.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nOkay, with the card in hand, what's the action for invoice IFM-74120?",
  "options": [
   "Send to price-variance review",
   "Release for payment",
   "Hold for receipt",
   "Route to a senior approver"
  ]
 },
 {
  "qid": "qfdb9b40a06",
  "kind": "choice",
  "text": "It is a pleasure to share the documents for the field service team with you, Ilse Brandt, namely the purchase order LPO-5601 and the goods receipt, pasted below for matching.\n\nPurchase order LPO-5601 | vendor Harlow Floral Wholesale\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | wire stems | six rolls | $7.20 |\n| 2 | roses | 100 boxes | $29.40 |\n| total | | | $2,983.20 |\n\nGoods receipt LGR-1870\n| line | received |\n|---|---|\n| 1 | three rolls |\n| 2 | 100 boxes |\n\nInvoice LSI-70527 | purchase order LPO-5601\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | wire stems | six rolls | $7.20 |\n| 2 | roses | 100 boxes | $29.40 |\n| total | | | $2,983.20 |\n\nPaid-invoice register | vendor Harlow Floral Wholesale\n| invoice number |\n|---|\n| LSI-80400 |\n| LSI-70527 |",
  "question": "AP policy of Larkspur Flower Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a proportion lower than five percent of the PO unit price on every line. If it fails: price-variance review.\n2. Approval-limit check: the invoice total is beneath $2,983.21 (limit of approver Dana Lindqvist). If it fails: route to a senior approver.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n4. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then approval limit, then duplicate, then quantity.\nOnce the first failing check in the check order has set the action, later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nIs the action for invoice LSI-70527 set out in the policy, and what is it?",
  "options": [
   "Reject as a duplicate",
   "Send to price-variance review",
   "Route to a senior approver",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qcfc554cd4d",
  "kind": "yes/no",
  "text": "Filed by: Lucy Okereke, for the IT support team.\nBits in here: PO MHP-5581 and supplier invoice MHI-59846, attached for matching, so it sits together.\n\nPurchase order MHP-5581 from Pendlebury Animal Pharma\n- line 1: cat litter; 30 bags at 7.94 GBP\n- line 2: exam gloves; 5 boxes at 5.63 GBP\n- order total: 266.35 GBP\n\nGoods receipt MHG-1641\n- line 1: received 30 bags\n- line 2: received 5 boxes\n\nInvoice MHI-59846 for purchase order MHP-5581\n- line 1: cat litter; 31 bags at 8.14 GBP\n- line 2: exam gloves; 5 boxes at 5.83 GBP\n- invoice total: 281.49 GBP",
  "question": "Would this policy count invoice MHI-59846 as a pass on the price check looked at by itself?",
  "definitions": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is not more than 0.20 GBP on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q9fdf669842",
  "kind": "yes/no",
  "text": "Purchase order export, po_number FSP-5629, vendor Ironside Hose Company\nline,item,quantity,unit_price\n1,cable glands,100 packs,6.14\ntotal,,,614.00\n\nGoods receipt export, gr_number FSG-9081\nline,received\n1,98 packs\n\nInvoice export, invoice_number FSV-97228, po_number FSP-5629\nline,item,quantity,unit_price\n1,cable glands,98 packs,6.18\ntotal,,,605.64\n\nPaid-invoice register export, vendor Ironside Hose Company\ninvoice_number\nFSV-34864\nFSV-97528\nFSV-64945\n\nHey Shabnam Rezaei, the field service papers came over from my end, lined up for matching. Busy day here, huh?",
  "question": "Is invoice FSV-97228 not released for payment once the AP policy has been applied to it?",
  "definitions": "AP policy of Tidewater Field Services: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Price check | invoiced unit price minus PO unit price is not more than £0.05 on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: duplicate, then price, then quantity.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qdff9f3d648",
  "kind": "choice",
  "text": "To: Ilse Brandt\nFrom: team assistant\nRe: Harlow Floral Wholesale paperwork for the field service team\nThe purchase order LPO-4601 is pasted below for matching.\n\nPurchase order LPO-4601 | vendor Harlow Floral Wholesale\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | ceramic vases | 200 units | $11 |\n| total | | | $2,200 |\n\nGoods receipt LGR-2049\n| line | received |\n|---|---|\n| 1 | 200 units |\n\nInvoice LSI-87236 | purchase order LPO-4601\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | ceramic vases | 200 units | 11.11 USD |\n| total | | | $2,222 |",
  "question": "AP policy of Larkspur Flower Group: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a proportion equal to or lower than 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does the AP policy assign to invoice LSI-87236 under its stated sequence of steps?",
  "options": [
   "Send to price-variance review",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q1a8715d4f4",
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
  "qid": "qd145555c49",
  "kind": "yes/no",
  "text": "Dev Malhotra - facilities team - invoice MHI-40984 forwarded.\n\nPurchase order MHP-7123 | vendor Crestline Surgical Instruments\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | vaccine vials | 192 boxes | 15.71 GBP |\n| total | | | 3,016.32 GBP |\n\nGoods receipt MHG-5745\n| line | received |\n|---|---|\n| 1 | 189 boxes |\n\nInvoice MHI-40984 | purchase order MHP-7123\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | vaccine vials | 189 boxes | 16.22 GBP |\n| total | | | 3,065.58 GBP |",
  "question": "Does the card send invoice MHI-40984 to price-variance review as its only step?",
  "definitions": "Meadowsend Animal Hospital AP policy: each invoice gets exactly one action.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Approval limit: invoice total is short of 5,000.00 GBP (limit of approver Stephen Blackwood). If it fails: route to a senior approver.\n- Price: invoiced unit price minus PO unit price is equal to or below 0.50 GBP on every line. If it fails: price-variance review.\nCheck order: price, then approval limit, then quantity.\nRead the check order from its start and apply the first failing check you reach to the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qdac3badbbf",
  "kind": "yes/no",
  "text": "{\"to\": \"Yara Benitez\",\n\"from\": \"team lead\",\n\"note\": \"Great to be working with you on this. The IT support team paperwork is pasted below for matching.\"}\n\nPurchase order RLP-1036 from Velloway Gear Systems\n- line 1: inner tubes; 114 units at $9\n- line 2: grease; 36 tubes at $4\n- line 3: spoke nipples; 188 packs at $3\n- order total: $1,734\n\nGoods receipt RLR-6773\n- line 1: received 114 units\n- line 2: received 35 tubes\n- line 3: received 188 packs\n\nInvoice RLI-69883 for purchase order RLP-1036\n- line 1: inner tubes; 114 units at $9\n- line 2: grease; 36 tubes at $4\n- line 3: spoke nipples; 188 packs at $3\n- invoice total: $1,734",
  "question": "Being new to AP, does the card say invoice RLI-69883 is released for payment?",
  "definitions": "AP policy of Ridgeline Cycle Works: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a portion lower than 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nWork through the check order, and when you find the first failing check, use it to set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q5f8f781efb",
  "kind": "yes/no",
  "text": "[assistant] from=team assistant to=Lucy Okereke team=IT support supplier=Foxhollow Pet Nutrition docs pasted below\n\nPurchase order MHP-8671 | vendor Foxhollow Pet Nutrition\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | dog food | 20 bags | 28.84 GBP |\n| total | | | 576.80 GBP |\n\nGoods receipt MHG-3982\n| line | received |\n|---|---|\n| 1 | 20 bags |\n\nInvoice MHI-48507 | purchase order MHP-8671\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | dog food | 20 bags | 30.22 GBP |\n| total | | | 604.40 GBP |",
  "question": "Does a check of how this policy treats invoice MHI-48507 end with price-variance review as the only action?",
  "definitions": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is less than 0.50 GBP on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nThe check order decides which failure counts, because the first failure met in that order decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q4b1e127ea6",
  "kind": "choice",
  "text": "Caller: So, procurement side, with the field service team buy in view.\nClerk: Love that. Malik Hussain here, AP, and the paperwork from Sable Costume Works is coming through.\n\nInvoice BLS-48677 for purchase order POF-9332\n- line 1: gaffer tape; 50 rolls at 6.19 GBP\n- invoice total: 309.50 GBP\n\nPaid-invoice register for Sable Costume Works: BLS-40547, BLS-21084, BLS-76382\n\nPurchase order POF-9332 from Sable Costume Works\n- line 1: gaffer tape; 50 rolls at 6.00 GBP\n- order total: 300.00 GBP\n\nGoods receipt GRF-1001\n- line 1: received 48 rolls",
  "question": "AP policy of Greywick Film Studios: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a portion that is 3 percent or below of the PO unit price on every line. If it fails: price-variance review.\n2. Approval-limit check: the invoice total is less than 322.86 GBP (limit of approver Tomoko Ueda). If it fails: route to a senior approver.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n4. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then approval limit, then quantity, then duplicate.\nOnce the checks are taken in the check order, the first one that fails settles the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhere the policy is applied to invoice BLS-48677, what action does it call for?",
  "options": [
   "Route to a senior approver",
   "Release for payment",
   "Send to price-variance review",
   "Hold for receipt",
   "Reject as a duplicate"
  ]
 },
 {
  "qid": "qf3d02df88e",
  "kind": "yes/no",
  "text": "Hiya,\nThis note sits in the file: documents for the field service team, PO WPO-9591, are pasted below for matching.\nThanks,\nSigrid Engstrom\n\nPurchase order WPO-9591 | vendor Feldmark Upholstery Textiles\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | cabinet hinges | six sets | €22 |\n| total | | | €132 |\n\nGoods receipt WGR-4089\n| line | received |\n|---|---|\n| 1 | three sets |\n\nInvoice WSI-89135 | purchase order WPO-9591\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | cabinet hinges | three sets | 22.67 EUR |\n| total | | | 68.01 EUR |",
  "question": "Does the policy stop or block payment of invoice WSI-89135 for any reason?",
  "definitions": "AP policy of Oakhaven Joinery Workshop: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a proportion equal to or lower than three percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nApply the check order in sequence, and let the first check that fails determine the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 }
]
