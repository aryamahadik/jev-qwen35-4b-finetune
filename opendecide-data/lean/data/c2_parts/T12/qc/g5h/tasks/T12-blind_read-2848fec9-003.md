# G5-H blind read T12-blind_read-2848fec9-003 (family T12)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T12/qc/g5h/answers/T12-blind_read-2848fec9-003.json

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
  "qid": "q642cf66318",
  "kind": "choice",
  "text": "Memo: marketing team invoice BCV-61446. Forwarded to Shauna Rennie.\n\nPurchase order BCP-4574 from Wexcombe Janitorial Supply\n- line 1: microfibre cloths; 117 packs at £8.06\n- line 2: bin liners; six rolls at £5.73\n- order total: £977.40\n\nGoods receipt BCR-2573\n- line 1: received 114 packs\n- line 2: received four rolls\n\nInvoice BCV-61446 for purchase order BCP-4574\n- line 1: microfibre cloths; 115 packs at £8.10\n- line 2: bin liners; three rolls at £5.59\n- invoice total: £948.27",
  "question": "AP policy of Brightstone Office Care: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is lower than £0.05 on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nThe action stands once it is set, because checks that come later in the check order do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nAs a new clerk on the AP team, which action does the policy give invoice BCV-61446?",
  "options": [
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "qcd9d94d233",
  "kind": "choice",
  "text": "Raised by: Rosie Fenwick\nTeam: laboratory\nSubject: supplier invoice, PO and goods receipt attached\n\nPurchase order MHP-1190 | vendor Crestline Surgical Instruments\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | cat litter | 25 bags | 11.18 GBP |\n| 2 | sutures | 100 packs | 9.39 GBP |\n| 3 | antiseptic wipes | 144 boxes | 11.52 GBP |\n| 4 | exam gloves | 2 boxes | 11.35 GBP |\n| total | | | 2,900.08 GBP |\n\nGoods receipt MHG-4687\n| line | received |\n|---|---|\n| 1 | 25 bags |\n| 2 | 100 packs |\n| 3 | 144 boxes |\n| 4 | 2 boxes |\n\nInvoice MHI-80517 | purchase order MHP-1190\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | cat litter | 25 bags | 11.18 GBP |\n| 2 | sutures | 100 packs | 9.39 GBP |\n| 3 | antiseptic wipes | 144 boxes | 11.52 GBP |\n| 4 | exam gloves | 2 boxes | 11.35 GBP |\n| total | | | 2,900.08 GBP |",
  "question": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is less than 0.25 GBP on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nIs the action for invoice MHI-80517 set out in the policy, and what is it?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "qe75e569d4b",
  "kind": "yes/no",
  "text": "Sophie Bramble: Hi facilities team, the documents for your purchase are pasted below for matching.\n\nInvoice SPV-95759 for purchase order PRQ-3972\n- line 1: fining agent; 4 packs at $14.29\n- invoice total: $57.16\n\nPaid-invoice register for Marrow Cork Supply: SPV-95759, SPV-75759\n\nPurchase order PRQ-3972 from Marrow Cork Supply\n- line 1: fining agent; 5 packs at $13.79\n- order total: $68.95\n\nGoods receipt GRZ-9702\n- line 1: received 4 packs",
  "question": "As a new clerk in AP, is invoice SPV-95759 allowed through to payment under the policy?",
  "definitions": "AP policy of Ambersett Wine Cellars: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is equal to or less than $0.50 on every line. If it fails: price-variance review.\n2. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then duplicate, then quantity.\nEvery check that comes after the failing one in the check order does not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qf3d3060cc5",
  "kind": "choice",
  "text": "Hello Dimitri Sorokin, wishing you a pleasant working session. The purchase order PQS-7035 for the facilities team is pasted below for matching, with gratitude.\n\nPurchase order PQS-7035 | vendor Lumenbridge Hardware Resellers\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | battery packs | fifteen packs | $23.58 |\n| total | | | $353.70 |\n\nGoods receipt RQS-3111\n| line | received |\n|---|---|\n| 1 | twelve packs |\n\nInvoice IQS-71578 | purchase order PQS-7035\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | battery packs | twelve packs | $23.58 |\n| total | | | $282.96 |\n\nPaid-invoice register | vendor Lumenbridge Hardware Resellers\n| invoice number |\n|---|\n| IQS-56160 |\n| IQS-39403 |\n| IQS-28364 |\n| IQS-64729 |",
  "question": "Quorin Digital Services AP policy: each invoice gets exactly one action.\n- Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Price: invoiced unit price minus PO unit price is $0.75 or lower on every line. If it fails: price-variance review.\nCheck order: quantity, then price, then duplicate.\nKeep to the check order, halt at the first failing check, and set the action from that check alone.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nIn the policy's eyes, which action does invoice IQS-71578 land on?",
  "options": [
   "Release for payment",
   "Send to price-variance review",
   "Hold for receipt",
   "Reject as a duplicate"
  ]
 },
 {
  "qid": "q0b684f8a3c",
  "kind": "choice",
  "text": "Hello Sunniva Haugland,\nIt is lovely to be in touch.\nOur billing desk is sending supplier invoice EVR-62034 for the warehouse team, pasted below for matching.\nKind regards,\n\nPurchase order EPU-7774 from Silverline Hygiene Products\n- line 1: surgical gloves; 2 boxes at €28.00\n- order total: €56.00\n\nGoods receipt EGN-7638\n- line 1: received 2 boxes\n\nInvoice EVR-62034 for purchase order EPU-7774\n- line 1: surgical gloves; 2 boxes at €28.57\n- invoice total: €57.14",
  "question": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a fraction smaller than or matching 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nOnce a check fails in the check order, later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nPlease verify the policy's reading of invoice EVR-62034: which action does it apply?",
  "options": [
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q9ad752d579",
  "kind": "yes/no",
  "text": "Clerk: Hello, this is Noa Friedman from the marketing side.\nCaller: Hello Noa Friedman, thank you for the call.\nClerk: The documents for the marketing team are being sent over.\n\nInvoice RXB-47506 for purchase order RXO-2061\n- line 1: pill counters; 5 units at 215.47 EUR\n- line 2: printer ribbons; 18 rolls at 47.25 EUR\n- invoice total: 1,927.85 EUR\n\nPurchase order RXO-2061 from Vellmar Dispensing Co\n- line 1: pill counters; 8 units at 206.20 EUR\n- line 2: printer ribbons; 19 rolls at 45.00 EUR\n- order total: 2,504.60 EUR\n\nGoods receipt RXR-5128\n- line 1: received 5 units\n- line 2: received 18 rolls",
  "question": "Just the price check here, by itself: does invoice RXB-47506 pass?",
  "definitions": "AP policy of Medgrove Pharmacy Group: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a fraction smaller than or equal to 5 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nOnce the first failing check in the check order has set the action, later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q6a9ae334c8",
  "kind": "choice",
  "text": "Clerk: Bruno Ferreira here, reaching out for the facilities purchase.\nCaller: Thank you kindly. The paperwork is pasted below for matching.\n\nInvoice RXB-67986 for purchase order RXO-8345\n- line 1: syringes; 10 boxes at €19\n- invoice total: €190\n\nPurchase order RXO-8345 from Asterholm Generics\n- line 1: syringes; 10 boxes at €19\n- order total: €190\n\nGoods receipt RXR-1250\n- line 1: received 9 boxes",
  "question": "AP policy of Medgrove Pharmacy Group: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is a fraction that is smaller than 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nHere's the deal: which action is the policy putting on invoice RXB-67986?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q465de896d4",
  "kind": "yes/no",
  "text": "Raised by: office manager\nTeam: warehouse\nSubject: PO attached\nTo: Yara Benitez\n\nPurchase order RLP-9271 from Velloway Gear Systems\n- line 1: brake cables; 8 packs at $9\n- line 2: inner tubes; 25 units at $5\n- line 3: grease; 150 tubes at $8\n- line 4: bicycle chains; 16 units at $15\n- order total: $1,637\n\nGoods receipt RLR-3268\n- line 1: received 7 packs\n- line 2: received 25 units\n- line 3: received 149 tubes\n- line 4: received 16 units\n\nInvoice RLI-66123 for purchase order RLP-9271\n- line 1: brake cables; 8 packs at $9\n- line 2: inner tubes; 25 units at $5\n- line 3: grease; 150 tubes at $8\n- line 4: bicycle chains; 16 units at $15\n- invoice total: $1,637\n\nBilling notice: continued service for Velloway Gear Systems depends on payment, so please pay as soon as possible.",
  "question": "Does the policy's handling of invoice RLI-66123 come down to price-variance review as the sole action?",
  "definitions": "AP policy of Ridgeline Cycle Works: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a proportion that is less than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q6ffa40ded6",
  "kind": "yes/no",
  "text": "Raised by: receiving dock worker\nTeam: the field service team\nSupplier: Solstice Dental Supply, papers attached\nTo: Ilona Fischer\n\nPurchase order GDP-8922 from Solstice Dental Supply\n- line 1: impression trays; 179 units at €15\n- order total: €2,685\n\nGoods receipt GDR-5671\n- line 1: received 179 units\n\nInvoice GDV-61254 for purchase order GDP-8922\n- line 1: impression trays; 179 units at €15.76\n- invoice total: €2,821.04\n\nPaid-invoice register for Solstice Dental Supply: GDV-89270, GDV-20906",
  "question": "Is it right that the policy releases invoice GDV-61254 for payment?",
  "definitions": "Greenhollow Dental Practice AP policy: each invoice gets exactly one action.\n1. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n2. Approval limit: invoice total is strictly beneath €3,147.39 (limit of approver Jurgen Holtz). If it fails: route to a senior approver.\n3. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n4. Price: invoiced unit price minus PO unit price is a proportion equal to or lower than 5 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then approval limit, then duplicate, then price.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q9e16ddb399",
  "kind": "yes/no",
  "text": "Dear Lucy Okereke, the team assistant for the facilities team writes to forward the Pendlebury Animal Pharma documents, attached for matching. Thank you.\n\nPurchase order MHP-9533 | vendor Pendlebury Animal Pharma\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | antiseptic wipes | 120 boxes | £12.35 |\n| 2 | vaccine vials | 72 boxes | £49.11 |\n| total | | | £5,017.92 |\n\nGoods receipt MHG-3463\n| line | received |\n|---|---|\n| 1 | 120 boxes |\n| 2 | 72 boxes |\n\nInvoice MHI-40522 | purchase order MHP-9533\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | antiseptic wipes | 120 boxes | £12.35 |\n| 2 | vaccine vials | 72 boxes | £49.22 |\n| total | | | £5,025.84 |",
  "question": "Would price-variance review be the only step the card takes on invoice MHI-40522?",
  "definitions": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is not more than £0.10 on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nKeep to the check order, halt at the first failing check, and set the action from that check alone.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qf024d6f555",
  "kind": "yes/no",
  "text": "Sabine Hartwig, warehouse team. Pasted below: invoice TIN-24019. For matching.\n\nPurchase order TPO-5849 | vendor Lindenhof Fresh Produce\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | disposable gloves | 100 boxes | €13.00 |\n| 2 | fresh herbs | 94 bags | €4.00 |\n| 3 | table linen | 102 sets | €15.00 |\n| total | | | €3,206.00 |\n\nGoods receipt TGR-4830\n| line | received |\n|---|---|\n| 1 | 100 boxes |\n| 2 | 92 bags |\n| 3 | 102 sets |\n\nInvoice TIN-24019 | purchase order TPO-5849\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | disposable gloves | 100 boxes | €13.01 |\n| 2 | fresh herbs | 94 bags | €4.00 |\n| 3 | table linen | 99 sets | €15.45 |\n| total | | | €3,206.55 |\n\nPaid-invoice register | vendor Lindenhof Fresh Produce\n| invoice number |\n|---|\n| TIN-41439 |\n| TIN-61551 |\n| TIN-24059 |",
  "question": "Taking only the price check on its own, does this policy have invoice TIN-24019 fail that check?",
  "definitions": "AP policy of Saffron Table Catering: each invoice gets exactly one action.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price check: invoiced unit price minus PO unit price is a share strictly less than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n- Approval-limit check: the invoice total is at most €2,500.00 (limit of approver Ayesha Rahman). If it fails: route to a senior approver.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then approval limit, then duplicate, then price.\nOnce the first failing check in the check order has set the action, later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q933302717f",
  "kind": "choice",
  "text": "Raised by: team lead\nTeam: the facilities team\nSubject: thanks a lot, Marta Lindgren\nDetails: Velloway Gear Systems, PO RLP-7783, papers attached for matching against the purchase order and goods receipt.\n\nPurchase order RLP-7783 from Velloway Gear Systems\n- line 1: grease; fifteen tubes at $5\n- line 2: bicycle chains; ten units at $32\n- order total: $395\n\nGoods receipt RLR-4610\n- line 1: received fifteen tubes\n- line 2: received ten units\n\nInvoice RLI-40581 for purchase order RLP-7783\n- line 1: grease; fifteen tubes at 4.88 USD\n- line 2: bicycle chains; ten units at 32.18 USD\n- invoice total: $395",
  "question": "Ridgeline Cycle Works AP policy: each invoice gets exactly one action.\n- Price: invoiced unit price minus PO unit price is a share that is less than one percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhat is the action this policy gives invoice RLI-40581?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "q52e4bcbe5e",
  "kind": "yes/no",
  "text": "Dear Tendai Moyo,\nThank you for your kind attention. The papers for the laboratory team, supplied by Redmere Protein Supply, are being sent along and attached for matching.\nWith sincere gratitude,\n\nInvoice SUB-57633 for purchase order EQP-7303\n- line 1: whey powder; 36 bags at $152.82\n- line 2: hand towels; 80 packs at $10.68\n- line 3: resistance bands; 34 packs at $10.06\n- line 4: cleaning spray; 75 bottles at $12.62\n- invoice total: $7,644.46\n\nPurchase order EQP-7303 from Redmere Protein Supply\n- line 1: whey powder; 36 bags at $152.82\n- line 2: hand towels; 80 packs at $10.85\n- line 3: resistance bands; 34 packs at $9.91\n- line 4: cleaning spray; 75 bottles at $12.62\n- order total: $7,652.96\n\nGoods receipt RCD-9408\n- line 1: received 36 bags\n- line 2: received 80 packs\n- line 3: received 34 packs\n- line 4: received 74 bottles",
  "question": "Just the price check here, by itself: does invoice SUB-57633 pass?",
  "definitions": "AP policy of Brickhollow Fitness Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is not more than $0.15 on every line. If it fails: price-variance review.\n2. Approval-limit check: the invoice total is $6,270.19 or less (limit of approver Ravi Thakur). If it fails: route to a senior approver.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then approval limit, then quantity.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q41d0b9bb7a",
  "kind": "choice",
  "text": "Purchase order export, po_number DPO-2752, vendor Corbeil Educational Supply\nline,item,quantity,unit_price\n1,science kits,5 kits,67.14\ntotal,,,335.70\n\nGoods receipt export, gr_number DGR-6932\nline,received\n1,4 kits\n\nInvoice export, invoice_number DIV-70944, po_number DPO-2752\nline,item,quantity,unit_price\n1,science kits,5 kits,67.89\ntotal,,,339.45\n\n{\"to\": \"Rhea Delacroix\", \"from\": \"office manager\", \"team\": \"IT support\", \"docs\": \"Pasted below are the papers from Corbeil Educational Supply and the purchase order DPO-2752. Thank you.\"}",
  "question": "AP policy of Maple Ridge School District: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is lower than $0.75 on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: price, then quantity.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhat treatment does the AP policy give invoice DIV-70944, expressed as an action?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q1524ca430b",
  "kind": "choice",
  "text": "Purchase order (JSON):\n{\"po_number\":\"KPO-8789\",\"vendor\":\"Brassfield Plate Works\",\"lines\":[{\"line\":1,\"item\":\"printing plates\",\"quantity\":\"96 units\",\"unit_price_cents\":1918},{\"line\":2,\"item\":\"binding glue\",\"quantity\":\"8 bottles\",\"unit_price_cents\":1395}],\"total_cents\":195288}\n\nGoods receipt (JSON):\n{\"gr_number\":\"KGR-5533\",\"lines\":[{\"line\":1,\"received\":\"95 units\"},{\"line\":2,\"received\":\"8 bottles\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"KVI-10485\",\"po_number\":\"KPO-8789\",\"lines\":[{\"line\":1,\"item\":\"printing plates\",\"quantity\":\"96 units\",\"unit_price_cents\":1918},{\"line\":2,\"item\":\"binding glue\",\"quantity\":\"8 bottles\",\"unit_price_cents\":1395}],\"total_cents\":195288}\n\n[billing] from=billing contact to=Keiko Nomura team=marketing invoice=KVI-10485 po=KPO-8789 attached for matching",
  "question": "AP policy of Ashgrove Printing House: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is below $0.20 on every line | price-variance review |\nCheck order: price, then quantity.\nWalk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nSo what does the policy actually tell us to do with invoice KVI-10485?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q921ff28795",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"PBK-8715\",\"vendor\":\"Ashcombe Bakery Supply\",\"lines\":[{\"line\":1,\"item\":\"baking trays\",\"quantity\":\"120 units\",\"unit_price_cents\":603},{\"line\":2,\"item\":\"butter\",\"quantity\":\"141 cases\",\"unit_price_cents\":9003}],\"total_cents\":1341783}\n\nGoods receipt (JSON):\n{\"gr_number\":\"RBK-1343\",\"lines\":[{\"line\":1,\"received\":\"120 units\"},{\"line\":2,\"received\":\"141 cases\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"IBK-53973\",\"po_number\":\"PBK-8715\",\"lines\":[{\"line\":1,\"item\":\"baking trays\",\"quantity\":\"120 units\",\"unit_price_cents\":603},{\"line\":2,\"item\":\"butter\",\"quantity\":\"141 cases\",\"unit_price_cents\":9003}],\"total_cents\":1341783}\n\n[team-lead] from=team lead to=Viktor Hadler regarding the IT support team\nsupplier Ashcombe Bakery Supply, invoice IBK-53973 pasted below, lovely working with you",
  "question": "Forget everything else for a moment: does invoice IBK-53973 pass the price check on its own?",
  "definitions": "AP policy of Golden Crumb Bakeries: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is less than or equal to 0.10 USD on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: quantity, then price.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q9e6cf4017e",
  "kind": "yes/no",
  "text": "To: Ines Carvalho\nFrom: procurement officer\nRe: Tamworth Roofing Supply for the IT support team\nDocuments attached for matching.\n\nPurchase order KBP-7231 | vendor Tamworth Roofing Supply\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | plasterboard | 57 units | 31.00 EUR |\n| 2 | cement | 142 bags | 16.00 EUR |\n| 3 | silicone sealant | 6 tubes | 2.00 EUR |\n| total | | | 4,051.00 EUR |\n\nGoods receipt KBG-8978\n| line | received |\n|---|---|\n| 1 | 54 units |\n| 2 | 139 bags |\n| 3 | 4 tubes |\n\nInvoice KBI-25376 | purchase order KBP-7231\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | plasterboard | 54 units | 31.11 EUR |\n| 2 | cement | 139 bags | 15.54 EUR |\n| 3 | silicone sealant | 4 tubes | 2.01 EUR |\n| total | | | 3,848.04 EUR |",
  "question": "Just starting out in AP, would invoice KBI-25376 fail the price check when that check is judged on its own?",
  "definitions": "AP policy of Hartwell Build Group: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a portion that sits below 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nWalk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q93fb99cb9b",
  "kind": "choice",
  "text": "Purchase order (JSON):\n{\"po_number\":\"PBK-2770\",\"vendor\":\"Sunridge Flour Mills\",\"lines\":[{\"line\":1,\"item\":\"cake boxes\",\"quantity\":\"2 packs\",\"unit_price_cents\":349},{\"line\":2,\"item\":\"butter\",\"quantity\":\"181 cases\",\"unit_price_cents\":6057},{\"line\":3,\"item\":\"baking trays\",\"quantity\":\"10 units\",\"unit_price_cents\":1568},{\"line\":4,\"item\":\"bread flour\",\"quantity\":\"20 bags\",\"unit_price_cents\":1175}],\"total_cents\":1136195}\n\nGoods receipt (JSON):\n{\"gr_number\":\"RBK-4117\",\"lines\":[{\"line\":1,\"received\":\"1 pack\"},{\"line\":2,\"received\":\"181 cases\"},{\"line\":3,\"received\":\"10 units\"},{\"line\":4,\"received\":\"20 bags\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"IBK-12616\",\"po_number\":\"PBK-2770\",\"lines\":[{\"line\":1,\"item\":\"cake boxes\",\"quantity\":\"2 packs\",\"unit_price_cents\":349},{\"line\":2,\"item\":\"butter\",\"quantity\":\"181 cases\",\"unit_price_cents\":6057},{\"line\":3,\"item\":\"baking trays\",\"quantity\":\"10 units\",\"unit_price_cents\":1580},{\"line\":4,\"item\":\"bread flour\",\"quantity\":\"20 bags\",\"unit_price_cents\":1169}],\"total_cents\":1136195}\n\n[team-assistant] writing to Rosalind Fenner about the laboratory team, Sunridge Flour Mills documents attached",
  "question": "AP policy of Golden Crumb Bakeries: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is equal to or less than 0.10 USD on every line | price-variance review |\nCheck order: quantity, then price.\nThe earliest failing check in the check order settles the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nAs a new clerk on the AP team, which action does the policy give invoice IBK-12616?",
  "options": [
   "Release for payment",
   "Send to price-variance review",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q1635c2b846",
  "kind": "yes/no",
  "text": "Hey there,\nJust a little note for the file about the marketing team purchase under PO RXO-3634, which is pasted below for matching.\nCheers,\nNoa Friedman\n\nInvoice RXB-50746 for purchase order RXO-3634\n- line 1: blister packs; 97 packs at €11.33\n- line 2: gauze pads; 45 packs at €8.00\n- line 3: amber vials; 24 packs at €19.55\n- invoice total: €1,928.21\n\nPurchase order RXO-3634 from Vellmar Dispensing Co\n- line 1: blister packs; 100 packs at €11.00\n- line 2: gauze pads; 48 packs at €8.00\n- line 3: amber vials; 24 packs at €19.00\n- order total: €1,940.00\n\nGoods receipt RXR-7427\n- line 1: received 100 packs\n- line 2: received 45 packs\n- line 3: received 23 packs",
  "question": "Under the AP policy, does invoice RXB-50746 pass the price check taken on its own?",
  "definitions": "AP policy of Medgrove Pharmacy Group: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is a proportion lower than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n3. Approval-limit check: the invoice total is not more than €1,363.25 (limit of approver Gideon Mwangi). If it fails: route to a senior approver.\nCheck order: quantity, then price, then approval limit.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q730bd07232",
  "kind": "choice",
  "text": "dear: AP lead, warm wishes from Declan Murphy\nteam: the facilities team\nvendor: supplier Ardenvale Timber Merchants, invoice WSI-31057\npapers: purchase order WPO-2512, attached for matching\n\nPurchase order WPO-2512 | vendor Ardenvale Timber Merchants\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | oak planks | 116 units | €73.60 |\n| 2 | upholstery foam | 75 rolls | €50.00 |\n| total | | | €12,287.60 |\n\nGoods receipt WGR-3161\n| line | received |\n|---|---|\n| 1 | 113 units |\n| 2 | 75 rolls |\n\nInvoice WSI-31057 | purchase order WPO-2512\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | oak planks | 113 units | €75.34 |\n| 2 | upholstery foam | 75 rolls | €51.79 |\n| total | | | €12,397.67 |\n\nHello from your account manager, and we value this working relationship, so please prioritise payment.",
  "question": "AP policy of Oakhaven Joinery Workshop: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is a share strictly less than 5 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nAnswer codes: Osprey = release for payment, Marlin = hold for receipt, Plover = price-variance review.\nNothing else applies: the policy and the documents shown are complete.\n\nWhat does the policy say to do with invoice WSI-31057?",
  "options": [
   "Plover",
   "Osprey",
   "Marlin"
  ]
 },
 {
  "qid": "q2a341b3279",
  "kind": "yes/no",
  "text": "Caller: Hello, this is the supplier's billing contact.\nClerk: Hello, this is Lenka Svoboda.\nCaller: Thank you, the documents for the laboratory team are being sent over.\n\nInvoice BIN-39975 for purchase order ARQ-6385\n- line 1: oak planks; 4 units at €92.92\n- line 2: scale models; 32 kits at €116.24\n- invoice total: €4,091.36\n\nPaid-invoice register for Brackenmoor Glazing: BIN-82904, BIN-27458, BIN-88820, BIN-52116\n\nPurchase order ARQ-6385 from Brackenmoor Glazing\n- line 1: oak planks; 5 units at €90.93\n- line 2: scale models; 36 kits at €114.24\n- order total: €4,567.29\n\nGoods receipt RCP-5097\n- line 1: received 4 units\n- line 2: received 33 kits",
  "question": "As a new clerk on the AP team, does invoice BIN-39975 fail the price check taken on its own?",
  "definitions": "Quellon Architects AP policy: each invoice gets exactly one action.\n1. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n2. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Price: invoiced unit price minus PO unit price is smaller than €2.00 on every line. If it fails: price-variance review.\nCheck order: quantity, then duplicate, then price.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q6a093bb1eb",
  "kind": "yes/no",
  "text": "Subject: Silverline Hygiene Products papers for matching\nTo: Teresa Llorente\nTeam: the warehouse team\nNote: hope you are doing well, PO EPU-1320 and the invoice pasted below.\n\nPurchase order EPU-1320 from Silverline Hygiene Products\n- line 1: waiting room chairs; 15 units at €184.00\n- line 2: paper gowns; 82 packs at €6.00\n- order total: €3,252.00\n\nGoods receipt EGN-4265\n- line 1: received 15 units\n- line 2: received 82 packs\n\nInvoice EVR-98657 for purchase order EPU-1320\n- line 1: waiting room chairs; 15 units at €184.00\n- line 2: paper gowns; 82 packs at €6.19\n- invoice total: €3,267.58",
  "question": "Does the policy decide that invoice EVR-98657 is released for payment?",
  "definitions": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a fraction that is at most 3 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nTake the checks in the check order and let the first one that fails set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q84fe623937",
  "kind": "choice",
  "text": "Purchase order export, po_number TPB-8593, vendor Corvane Hop Growers\nline,item,quantity,unit_price\n1,bottle caps,85 packs,3.60\n2,hop pellets,22 bags,66.20\ntotal,,,1762.40\n\nGoods receipt export, gr_number TGB-5517\nline,received\n1,85 packs\n2,22 bags\n\nInvoice export, invoice_number TIB-95757, po_number TPB-8593\nline,item,quantity,unit_price\n1,bottle caps,85 packs,3.55\n2,hop pellets,22 bags,63.44\ntotal,,,1697.43\n\n{\"from\": \"Tariq Syed\", \"file\": \"marketing team, purchase order TPB-8593\", \"note\": \"Thank you for your attention. Documents are attached for matching.\"}",
  "question": "AP policy of Millrace Brewing Company: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Approval-limit check | the invoice total is £2,179.05 or lower (limit of approver Jacqueline Ncube) | route to a senior approver |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is a fraction smaller than or matching five percent of the PO unit price on every line | price-variance review |\nCheck order: approval limit, then quantity, then price.\nWalk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nAnswer codes: Osprey = release for payment, Kestrel = hold for receipt, Plover = price-variance review, Marlin = route to a senior approver.\nNothing else applies: the policy and the documents shown are complete.\n\nHere's the deal: which action is the policy putting on invoice TIB-95757?",
  "options": [
   "Kestrel",
   "Marlin",
   "Plover",
   "Osprey"
  ]
 },
 {
  "qid": "qa9eaad6145",
  "kind": "yes/no",
  "text": "Purchase order export, po_number PFM-1072, vendor Ravenscourt Fixtures Supply\nline,item,quantity,unit_price\n1,door closers,40 units,86.00\n2,filter panels,25 boxes,26.00\ntotal,,,4090.00\n\nGoods receipt export, gr_number RFM-9164\nline,received\n1,37 units\n2,25 boxes\n\nInvoice export, invoice_number IFM-80889, po_number PFM-1072\nline,item,quantity,unit_price\n1,door closers,37 units,87.64\n2,filter panels,25 boxes,25.79\ntotal,,,3887.43\n\n{\"from\": \"Mirela Popescu\", \"to\": \"AP lead\",\n\"note\": \"PO PFM-1072 papers for facilities team, with invoice IFM-80889 pasted below.\"}",
  "question": "Under the policy, is invoice IFM-80889 blocked from payment?",
  "definitions": "AP policy of Brenton Estate Services: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is a portion equal to or smaller than 3 percent of the PO unit price on every line | price-variance review |\nCheck order: quantity, then price.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q6de008141f",
  "kind": "yes/no",
  "text": "Raised by: receiving dock worker\nTeam: the field service team\nSupplier: Solstice Dental Supply, papers attached\nTo: Ilona Fischer\n\nPurchase order GDP-8922 from Solstice Dental Supply\n- line 1: impression trays; 179 units at €15\n- order total: €2,685\n\nGoods receipt GDR-5671\n- line 1: received 179 units\n\nInvoice GDV-61254 for purchase order GDP-8922\n- line 1: impression trays; 179 units at €15.76\n- invoice total: €2,821.04\n\nPaid-invoice register for Solstice Dental Supply: GDV-89270, GDV-20906",
  "question": "Does the policy decide that invoice GDV-61254 ends in a hold, a review, a rejection, or a routing to a senior approver?",
  "definitions": "Greenhollow Dental Practice AP policy: each invoice gets exactly one action.\n1. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n2. Approval limit: invoice total is strictly beneath €3,147.39 (limit of approver Jurgen Holtz). If it fails: route to a senior approver.\n3. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n4. Price: invoiced unit price minus PO unit price is a proportion equal to or lower than 5 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then approval limit, then duplicate, then price.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q698490d3ad",
  "kind": "yes/no",
  "text": "Office note for Ines Carvalho. Here is the facilities team set, with the purchase order POF-8001 pasted below.\n\nInvoice BLS-35262 for purchase order POF-8001\n- line 1: lighting gels; 25 packs at £13.43\n- line 2: camera batteries; 2 packs at £64.88\n- invoice total: £465.51\n\nPaid-invoice register for Penrose Lighting Rental: BLS-67905, BLS-35262, BLS-75262\n\nPurchase order POF-8001 from Penrose Lighting Rental\n- line 1: lighting gels; 24 packs at £14.00\n- line 2: camera batteries; 2 packs at £63.00\n- order total: £462.00\n\nGoods receipt GRF-1660\n- line 1: received 24 packs\n- line 2: received 2 packs",
  "question": "Is it true, as a new clerk, that invoice BLS-35262 fails the price check taken by itself?",
  "definitions": "AP policy of Greywick Film Studios: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a proportion strictly smaller than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Approval-limit check: the invoice total is strictly beneath £465.51 (limit of approver Tomoko Ueda). If it fails: route to a senior approver.\n4. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then quantity, then approval limit, then duplicate.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q4b560083f9",
  "kind": "yes/no",
  "text": "Raised by: Pilar Navarro\nTeam: the warehouse team\nSupplier: Feldmark Upholstery Textiles\nReferences: invoice WSI-39989, PO WPO-6454, forwarded for matching.\n\nPurchase order WPO-6454 | vendor Feldmark Upholstery Textiles\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | oak planks | 10 units | 60.00 EUR |\n| total | | | 600.00 EUR |\n\nGoods receipt WGR-4088\n| line | received |\n|---|---|\n| 1 | 8 units |\n\nInvoice WSI-39989 | purchase order WPO-6454\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | oak planks | 8 units | 60.60 EUR |\n| total | | | 484.80 EUR |\n\nPaid-invoice register | vendor Feldmark Upholstery Textiles\n| invoice number |\n|---|\n| WSI-68117 |\n| WSI-39899 |\n| WSI-61958 |",
  "question": "Under the policy, does the treatment of invoice WSI-39989 leave it not released for payment?",
  "definitions": "AP policy of Oakhaven Joinery Workshop: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a proportion that equals or is lower than 1 percent of the PO unit price on every line. If it fails: price-variance review.\n2. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then duplicate, then quantity.\nEach check runs in the check order, and the first one that fails sets the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q2a44fc21e2",
  "kind": "yes/no",
  "text": "Purchase order export, po_number FPO-2646, vendor Saltmarsh Packaging Group\nline,item,quantity,unit_price\n1,paper cartons,25 cartons,3.00\ntotal,,,75.00\n\nGoods receipt export, gr_number FGR-3753\nline,received\n1,22 cartons\n\nInvoice export, invoice_number FIN-20151, po_number FPO-2646\nline,item,quantity,unit_price\n1,paper cartons,22 cartons,3.09\ntotal,,,67.98\n\nPaid-invoice register export, vendor Saltmarsh Packaging Group\ninvoice_number\nFIN-52738\nFIN-14526\nFIN-28061\n\n{\"to\": \"Kwame Asamoah\", \"from\": \"office manager\", \"note\": \"The purchase order FPO-2646 from Saltmarsh Packaging Group is attached. It is for the facilities team.\"}",
  "question": "Does the card clear invoice FIN-20151 for payment?",
  "definitions": "AP policy of Oakridge Food Producers: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Approval-limit check | the invoice total is 67.98 GBP or less (limit of approver Hugo Lambert) | route to a senior approver |\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is a proportion equal to or lower than 3 percent of the PO unit price on every line | price-variance review |\nCheck order: approval limit, then duplicate, then quantity, then price.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q37e65f8c18",
  "kind": "yes/no",
  "text": "Subject: Silverline Hygiene Products papers for matching\nTo: Teresa Llorente\nTeam: the warehouse team\nNote: hope you are doing well, PO EPU-1320 and the invoice pasted below.\n\nPurchase order EPU-1320 from Silverline Hygiene Products\n- line 1: waiting room chairs; 15 units at €184.00\n- line 2: paper gowns; 82 packs at €6.00\n- order total: €3,252.00\n\nGoods receipt EGN-4265\n- line 1: received 15 units\n- line 2: received 82 packs\n\nInvoice EVR-98657 for purchase order EPU-1320\n- line 1: waiting room chairs; 15 units at €184.00\n- line 2: paper gowns; 82 packs at €6.00\n- invoice total: €3,252.00",
  "question": "Does the policy decide that invoice EVR-98657 is released for payment?",
  "definitions": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a fraction that is at most 3 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nTake the checks in the check order and let the first one that fails set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qb18d0fcd87",
  "kind": "choice",
  "text": "Message for AP lead from Paolo Greco: field service purchase, papers pasted below for matching.\n\nPurchase order GDP-4279 from Quarrington Sterilisation Products\n- line 1: composite resin; 8 tubes at €18\n- order total: €144\n\nGoods receipt GDR-4167\n- line 1: received 6 tubes\n\nInvoice GDV-78318 for purchase order GDP-4279\n- line 1: composite resin; 4 tubes at 18.09 EUR\n- invoice total: 72.36 EUR",
  "question": "AP policy of Greenhollow Dental Practice: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is any share smaller than 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nWhatever the later checks in the check order show, they do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nToward what action does the AP policy lead invoice GDV-78318?",
  "options": [
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q06a84dec2b",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"PBK-5495\",\"vendor\":\"Copperleaf Dairy Cooperative\",\"lines\":[{\"line\":1,\"item\":\"vanilla extract\",\"quantity\":\"36 bottles\",\"unit_price_cents\":975}],\"total_cents\":35100}\n\nGoods receipt (JSON):\n{\"gr_number\":\"RBK-8586\",\"lines\":[{\"line\":1,\"received\":\"33 bottles\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"IBK-12676\",\"po_number\":\"PBK-5495\",\"lines\":[{\"line\":1,\"item\":\"vanilla extract\",\"quantity\":\"33 bottles\",\"unit_price_cents\":995}],\"total_cents\":32835}\n\nfrom: procurement officer, catching up\nto: Rosalind Fenner\nteam: the laboratory team purchase we mentioned before\ndocs: pasted below, ready for matching",
  "question": "Sorry to ask as a new starter, but when the price check is looked at on its own, does invoice IBK-12676 fail it?",
  "definitions": "AP policy of Golden Crumb Bakeries: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is beneath 0.20 USD on every line | price-variance review |\nCheck order: price, then quantity.\nThe action is set by the first failing check in the check order.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q5c4fabe4e7",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"VHP-3694\",\"vendor\":\"Ardelle Amenities Company\",\"lines\":[{\"line\":1,\"item\":\"pillows\",\"quantity\":\"3 units\",\"unit_price_cents\":4200}],\"total_cents\":12600}\n\nGoods receipt (JSON):\n{\"gr_number\":\"VHG-7287\",\"lines\":[{\"line\":1,\"received\":\"2 units\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"VHI-58379\",\"po_number\":\"VHP-3694\",\"lines\":[{\"line\":1,\"item\":\"pillows\",\"quantity\":\"3 units\",\"unit_price_cents\":4242}],\"total_cents\":12726}\n\nfrom: procurement officer, same as usual\nto: Anselm Richter\nteam: the field service team\nbits: pasted below for matching",
  "question": "Judged by the price check on its own, would invoice VHI-58379 pass that check?",
  "definitions": "AP policy of Velmora Boutique Hotel: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is a proportion that equals or is lower than 1 percent of the PO unit price on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: price, then quantity.\nThe action stands once it is set, because checks that come later in the check order do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qe1899b70ce",
  "kind": "yes/no",
  "text": "[handoff] from=procurement officer to=Marta Lindgren for the facilities team, po=RLP-9409 pasted below for matching, with appreciation\n\nPurchase order RLP-9409 from Tarn Frame Forge\n- line 1: bicycle chains; 25 units at $35.00\n- line 2: brake cables; 75 packs at $10.00\n- order total: $1,625.00\n\nGoods receipt RLR-6802\n- line 1: received 25 units\n- line 2: received 75 packs\n\nInvoice RLI-40073 for purchase order RLP-9409\n- line 1: bicycle chains; 25 units at $36.04\n- line 2: brake cables; 75 packs at $9.65\n- invoice total: $1,624.75",
  "question": "Under the policy, does invoice RLI-40073 go to price-variance review as its only action?",
  "definitions": "AP policy of Ridgeline Cycle Works: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a share that is less than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nWhichever failing check comes first in the check order decides the action, and later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q85705b2ca2",
  "kind": "choice",
  "text": "Purchase order (JSON):\n{\"po_number\":\"PBK-8615\",\"vendor\":\"Ashcombe Bakery Supply\",\"lines\":[{\"line\":1,\"item\":\"baking trays\",\"quantity\":\"180 units\",\"unit_price_cents\":797},{\"line\":2,\"item\":\"bread flour\",\"quantity\":\"20 bags\",\"unit_price_cents\":2642},{\"line\":3,\"item\":\"butter\",\"quantity\":\"120 cases\",\"unit_price_cents\":5886}],\"total_cents\":902620}\n\nGoods receipt (JSON):\n{\"gr_number\":\"RBK-3342\",\"lines\":[{\"line\":1,\"received\":\"178 units\"},{\"line\":2,\"received\":\"18 bags\"},{\"line\":3,\"received\":\"120 cases\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"IBK-47674\",\"po_number\":\"PBK-8615\",\"lines\":[{\"line\":1,\"item\":\"baking trays\",\"quantity\":\"178 units\",\"unit_price_cents\":797},{\"line\":2,\"item\":\"bread flour\",\"quantity\":\"18 bags\",\"unit_price_cents\":2522},{\"line\":3,\"item\":\"butter\",\"quantity\":\"120 cases\",\"unit_price_cents\":5901}],\"total_cents\":895382}\n\nnote: for Rosalind Fenner, the marketing team\nsupplier: Ashcombe Bakery Supply\npo: PBK-8615\npasted: below",
  "question": "AP policy of Golden Crumb Bakeries: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is equal to or less than 0.15 USD on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: price, then quantity.\nRun the checks in the check order, and once one fails, let that result decide the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nFrom the card, what action must invoice IBK-47674 get?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q8d17c444d3",
  "kind": "yes/no",
  "text": "From: Felix Brunner\nTo: AP lead\nTeam: laboratory team\nPO NHM-9716, docs attached.\n\nPurchase order NHM-9716 from Tessaly Preservation Works\n- line 1: museum tissue; three reams at 6.61 EUR\n- line 2: glass vials; 150 boxes at 13.69 EUR\n- order total: 2,073.33 EUR\n\nGoods receipt GRN-1852\n- line 1: received one ream\n- line 2: received 149 boxes\n\nInvoice SUP-84568 for purchase order NHM-9716\n- line 1: museum tissue; one ream at 6.61 EUR\n- line 2: glass vials; 149 boxes at 13.89 EUR\n- invoice total: 2,076.22 EUR",
  "question": "Would the AP policy simply send invoice SUP-84568 to price-variance review and leave it there?",
  "definitions": "AP policy of Northgate Natural History Museum: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is falling short of 0.20 EUR on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nWork through the check order, and when you find the first failing check, use it to set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q0052b41511",
  "kind": "yes/no",
  "text": "Kwabena Oppong, the field service team bundle is with me at the dock. Supplier invoice SPV-61906 sits in it, forwarded for matching.\n\nInvoice SPV-61906 for purchase order PRQ-2496\n- line 1: wine bottles; 96 cases at 71.25 USD\n- line 2: corks; 48 boxes at 12.37 USD\n- line 3: fining agent; 19 packs at 25.36 USD\n- line 4: barrel hoops; 70 sets at 39.57 USD\n- invoice total: 10,685.50 USD\n\nPaid-invoice register for Dornhaus Cooperage: SPV-54888, SPV-82764, SPV-44339, SPV-11169\n\nPurchase order PRQ-2496 from Dornhaus Cooperage\n- line 1: wine bottles; 96 cases at 71.25 USD\n- line 2: corks; 48 boxes at 12.37 USD\n- line 3: fining agent; 20 packs at 25.22 USD\n- line 4: barrel hoops; 73 sets at 39.43 USD\n- order total: 10,816.55 USD\n\nGoods receipt GRZ-3284\n- line 1: received 96 cases\n- line 2: received 48 boxes\n- line 3: received 19 packs\n- line 4: received 70 sets",
  "question": "Would you say invoice SPV-61906 fails the price check, looking only at that check?",
  "definitions": "AP policy of Ambersett Wine Cellars: each invoice gets exactly one action.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price check: invoiced unit price minus PO unit price is smaller than 0.15 USD on every line. If it fails: price-variance review.\n- Approval-limit check: the invoice total is falling short of 10,685.50 USD (limit of approver Anaya Iyer). If it fails: route to a senior approver.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then approval limit, then duplicate, then price.\nEach check runs in the check order, and the first one that fails sets the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q97fbf9636c",
  "kind": "choice",
  "text": "Dear laboratory team,\nFrom Bruno Ferreira, here is supplier invoice RXB-71859 from Quilltrade Medical Supply, pasted below for matching.\nKind regards,\n\nInvoice RXB-71859 for purchase order RXO-2668\n- line 1: blister packs; 60 packs at 13.64 EUR\n- line 2: printer ribbons; 22 rolls at 31.78 EUR\n- invoice total: 1,517.56 EUR\n\nPaid-invoice register for Quilltrade Medical Supply: RXB-49630, RXB-36812, RXB-39509, RXB-42363\n\nPurchase order RXO-2668 from Quilltrade Medical Supply\n- line 1: blister packs; 60 packs at 13.20 EUR\n- line 2: printer ribbons; 25 rolls at 32.00 EUR\n- order total: 1,592.00 EUR\n\nGoods receipt RXR-4459\n- line 1: received 59 packs\n- line 2: received 24 rolls",
  "question": "AP policy of Medgrove Pharmacy Group: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a portion that stays below five percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then duplicate, then quantity.\nWhatever the later checks in the check order show, they do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nAnswer codes: Osprey = release for payment, Marlin = hold for receipt, Kestrel = price-variance review, Plover = reject as a duplicate.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does the policy tell us to take for invoice RXB-71859?",
  "options": [
   "Osprey",
   "Marlin",
   "Plover",
   "Kestrel"
  ]
 },
 {
  "qid": "qe6b728e285",
  "kind": "yes/no",
  "text": "To: Declan Murphy\nFrom: procurement office\nRe: laboratory purchase, documents forwarded for matching\n\nPurchase order WPO-7864 | vendor Caldwell Hardware Trade\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | wall fixings | 110 boxes | 5.00 EUR |\n| 2 | oak planks | 75 units | 28.00 EUR |\n| total | | | 2,650.00 EUR |\n\nGoods receipt WGR-5737\n| line | received |\n|---|---|\n| 1 | 110 boxes |\n| 2 | 74 units |\n\nInvoice WSI-71273 | purchase order WPO-7864\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | wall fixings | 110 boxes | 5.00 EUR |\n| 2 | oak planks | 75 units | 28.00 EUR |\n| total | | | 2,650.00 EUR |",
  "question": "Would this policy let invoice WSI-71273 be paid?",
  "definitions": "AP policy of Oakhaven Joinery Workshop: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is a portion smaller than or the same as 1 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qd2a633e0f1",
  "kind": "choice",
  "text": "To: Ilse Brandt\nFrom: office manager\nRe: supplier invoice LSI-44706 from Meadowbrook Stem Supply for the laboratory team\nThe purchase order LPO-1856 and the goods receipt are attached for matching.\n\nPurchase order LPO-1856 | vendor Meadowbrook Stem Supply\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | potting soil | 4 bags | 7.00 USD |\n| total | | | 28.00 USD |\n\nGoods receipt LGR-9408\n| line | received |\n|---|---|\n| 1 | 4 bags |\n\nInvoice LSI-44706 | purchase order LPO-1856\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | potting soil | 4 bags | 7.32 USD |\n| total | | | 29.28 USD |\n\nPaid-invoice register | vendor Meadowbrook Stem Supply\n| invoice number |\n|---|\n| LSI-55809 |\n| LSI-81336 |\n| LSI-44708 |\n| LSI-31746 |",
  "question": "AP policy of Larkspur Flower Group: each invoice gets exactly one action.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price check: invoiced unit price minus PO unit price is a proportion equal to or lower than 1 percent of the PO unit price on every line. If it fails: price-variance review.\n- Approval-limit check: the invoice total is falling short of 250.00 USD (limit of approver Dana Lindqvist). If it fails: route to a senior approver.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then duplicate, then approval limit, then price.\nRun the checks in the check order, and once one fails, let that result decide the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nQuick question: what action does the card give invoice LSI-44706?",
  "options": [
   "Reject as a duplicate",
   "Hold for receipt",
   "Send to price-variance review",
   "Route to a senior approver",
   "Release for payment"
  ]
 },
 {
  "qid": "qca1d2f0f04",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"PBK-1177\",\"vendor\":\"Sunridge Flour Mills\",\"lines\":[{\"line\":1,\"item\":\"sesame seeds\",\"quantity\":\"13 bags\",\"unit_price_cents\":1882}],\"total_cents\":24466}\n\nGoods receipt (JSON):\n{\"gr_number\":\"RBK-5396\",\"lines\":[{\"line\":1,\"received\":\"10 bags\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"IBK-61385\",\"po_number\":\"PBK-1177\",\"lines\":[{\"line\":1,\"item\":\"sesame seeds\",\"quantity\":\"10 bags\",\"unit_price_cents\":1907}],\"total_cents\":19070}\n\nPaid-invoice register (JSON):\n{\"vendor\":\"Sunridge Flour Mills\",\"paid_invoice_numbers\":[\"IBK-61985\",\"IBK-61385\"]}\n\n[log-entry] originator=AP clerk Viktor Hadler\nteam=facilities, supplier=Sunridge Flour Mills, invoice=IBK-61385, po=PBK-1177 attached for matching",
  "question": "Would the policy's treatment of invoice IBK-61385 amount to price-variance review as its only action?",
  "definitions": "AP policy of Golden Crumb Bakeries: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Price check | invoiced unit price minus PO unit price is at or below $0.25 on every line | price-variance review |\nCheck order: quantity, then duplicate, then price.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qa13b57992d",
  "kind": "choice",
  "text": "Nkechi Eze: AP lead, the warehouse documents are attached for matching.\n\nPurchase order GDP-4581 from Quarrington Sterilisation Products\n- line 1: impression trays; 96 units at 12.60 EUR\n- order total: 1,209.60 EUR\n\nGoods receipt GDR-8154\n- line 1: received 96 units\n\nInvoice GDV-95426 for purchase order GDP-4581\n- line 1: impression trays; 96 units at 13.21 EUR\n- invoice total: 1,268.16 EUR",
  "question": "AP policy of Greenhollow Dental Practice: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a share that equals or is smaller than 5 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Approval-limit check: the invoice total is equal to or below €250 (limit of approver Celeste Moreau). If it fails: route to a senior approver.\nCheck order: approval limit, then quantity, then price.\nThe earliest failing check in the check order settles the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does the policy tell us to take for invoice GDV-95426?",
  "options": [
   "Route to a senior approver",
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "qc4df34f303",
  "kind": "choice",
  "text": "Subject: documents forwarded for matching\nFor: Priya Raman\nFrom: procurement officer\nTeam: IT support\n\nPurchase order BMR-8501 from Holcombe Tyre Supply\n- line 1: cleaning rags; 96 bags at £7.72\n- line 2: brake pads; twenty sets at £27.08\n- order total: £1,282.72\n\nGoods receipt BGN-7189\n- line 1: received 95 bags\n- line 2: received twenty sets\n\nInvoice BVI-22943 for purchase order BMR-8501\n- line 1: cleaning rags; 96 bags at £7.72\n- line 2: brake pads; twenty sets at £27.08\n- invoice total: £1,282.72",
  "question": "AP policy of Brackley Motor Repairs: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is up to and including £0.10 on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nWork through the check order, and when you find the first failing check, use it to set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nPursuant to the AP policy, which action is prescribed for invoice BVI-22943?",
  "options": [
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q1f9a250d5b",
  "kind": "yes/no",
  "text": "Here are the field service team documents from Lucy Okereke, sent to the AP lead for matching.\n\nPurchase order MHP-1428 | vendor Crestline Surgical Instruments\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | dog food | 180 bags | £21.62 |\n| 2 | antiseptic wipes | 86 boxes | £8.41 |\n| 3 | sutures | 200 packs | £15.60 |\n| 4 | vaccine vials | 80 boxes | £49.77 |\n| total | | | £11,716.46 |\n\nGoods receipt MHG-6314\n| line | received |\n|---|---|\n| 1 | 178 bags |\n| 2 | 83 boxes |\n| 3 | 200 packs |\n| 4 | 78 boxes |\n\nInvoice MHI-44574 | purchase order MHP-1428\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | dog food | 176 bags | £21.62 |\n| 2 | antiseptic wipes | 83 boxes | £8.61 |\n| 3 | sutures | 200 packs | £15.68 |\n| 4 | vaccine vials | 78 boxes | £49.88 |\n| total | | | £11,546.39 |",
  "question": "Forget the other checks for a sec: would invoice MHI-44574 fail the price check by itself?",
  "definitions": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n1. Approval-limit check: the invoice total is any amount smaller than £25,000.00 (limit of approver Stephen Blackwood). If it fails: route to a senior approver.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Price check: invoiced unit price minus PO unit price is £0.25 or less on every line. If it fails: price-variance review.\nCheck order: approval limit, then quantity, then price.\nOnce the checks are taken in the check order, the first one that fails settles the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q580c0b96e0",
  "kind": "yes/no",
  "text": "Purchase order export, po_number PFM-2128, vendor Hollowell Electrical Trading\nline,item,quantity,unit_price\n1,sealant tubes,154 tubes,8.00\ntotal,,,1232.00\n\nGoods receipt export, gr_number RFM-8976\nline,received\n1,151 tubes\n\nInvoice export, invoice_number IFM-83852, po_number PFM-2128\nline,item,quantity,unit_price\n1,sealant tubes,151 tubes,8.08\ntotal,,,1220.08\n\n[clerk-note] team=marketing\nsent from=Mirela Popescu with purchase documents forwarded for matching",
  "question": "Is invoice IFM-83852 released to be paid under the card?",
  "definitions": "AP policy of Brenton Estate Services: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is a share that is less than 1 percent of the PO unit price on every line | price-variance review |\nCheck order: price, then quantity.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q31b0a1f263",
  "kind": "yes/no",
  "text": "Respected Freya Dahl,\nIt is my pleasure to share the documents for the marketing team, concerning Ludlow Rigging Hire under PO POF-6568, pasted below for matching.\nRespectfully,\n\nInvoice BLS-47397 for purchase order POF-6568\n- line 1: gaffer tape; 69 rolls at £9.40\n- invoice total: £648.60\n\nPaid-invoice register for Ludlow Rigging Hire: BLS-56702, BLS-29672, BLS-34052, BLS-62572\n\nPurchase order POF-6568 from Ludlow Rigging Hire\n- line 1: gaffer tape; 70 rolls at £9.40\n- order total: £658\n\nGoods receipt GRF-5422\n- line 1: received 69 rolls",
  "question": "Under the AP policy, is payment of invoice BLS-47397 blocked?",
  "definitions": "AP policy of Greywick Film Studios: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Price check: invoiced unit price minus PO unit price is a fraction smaller than or matching 5 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then duplicate, then price.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q1fd3784ff0",
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
  "qid": "q4f93bf2063",
  "kind": "yes/no",
  "text": "Hiya,\nThis note sits in the file: documents for the IT support team, PO MHP-6328, are pasted below for matching.\nThanks,\nRosie Fenwick\n\nPurchase order MHP-6328 | vendor Crestline Surgical Instruments\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | exam gloves | 96 boxes | £14.81 |\n| 2 | dog food | 121 bags | £39.20 |\n| total | | | £6,164.96 |\n\nGoods receipt MHG-8864\n| line | received |\n|---|---|\n| 1 | 96 boxes |\n| 2 | 121 bags |\n\nInvoice MHI-47924 | purchase order MHP-6328\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | exam gloves | 96 boxes | £14.81 |\n| 2 | dog food | 121 bags | £39.20 |\n| total | | | £6,164.96 |",
  "question": "Does this policy's outcome for invoice MHI-47924 amount to it being not released for payment?",
  "definitions": "AP policy of Meadowsend Animal Hospital: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is equal to or below £0.25 on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nOnce a check fails in the check order, later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q71cae1e144",
  "kind": "choice",
  "text": "Hi colleagues,\nSupplier invoice TIN-70181 from Lindenhof Fresh Produce is forwarded for matching. It is for the field service team.\nBest,\nJonas Ekstrom\n\nPurchase order TPO-9708 | vendor Lindenhof Fresh Produce\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | table linen | 3 sets | 40.20 EUR |\n| 2 | chicken breasts | 30 cases | 172.60 EUR |\n| total | | | 5,298.60 EUR |\n\nGoods receipt TGR-5631\n| line | received |\n|---|---|\n| 1 | 1 set |\n| 2 | 28 cases |\n\nInvoice TIN-70181 | purchase order TPO-9708\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | table linen | 1 set | 41.66 EUR |\n| 2 | chicken breasts | 26 cases | 172.60 EUR |\n| total | | | 4,529.26 EUR |\n\nPaid-invoice register | vendor Lindenhof Fresh Produce\n| invoice number |\n|---|\n| TIN-61379 |\n| TIN-34446 |\n| TIN-74143 |",
  "question": "AP policy of Saffron Table Catering: each invoice gets exactly one action.\n1. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n2. Approval-limit check: the invoice total is at most 4,609.64 EUR (limit of approver Ruben Calderon). If it fails: route to a senior approver.\n3. Price check: invoiced unit price minus PO unit price is a share strictly less than 5 percent of the PO unit price on every line. If it fails: price-variance review.\n4. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: duplicate, then approval limit, then price, then quantity.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does the policy reach for invoice TIN-70181?",
  "options": [
   "Release for payment",
   "Route to a senior approver",
   "Hold for receipt",
   "Reject as a duplicate",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "qa028fdc2d0",
  "kind": "yes/no",
  "text": "Dear IT support team, please find the purchase documents attached for matching.\nYours faithfully,\nDeclan Murphy\n\nPurchase order WPO-7174 | vendor Caldwell Hardware Trade\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | sanding discs | 200 packs | 18.00 EUR |\n| total | | | 3,600.00 EUR |\n\nGoods receipt WGR-4109\n| line | received |\n|---|---|\n| 1 | 197 packs |\n\nInvoice WSI-97291 | purchase order WPO-7174\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | sanding discs | 198 packs | 18.90 EUR |\n| total | | | 3,742.20 EUR |",
  "question": "Just starting out in AP, would invoice WSI-97291 fail the price check when that check is judged on its own?",
  "definitions": "AP policy of Oakhaven Joinery Workshop: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a proportion strictly smaller than five percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nWhichever failing check comes first in the check order decides the action, and later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q8be3b1846e",
  "kind": "choice",
  "text": "Dear Yara Benitez,\nThank you for taking this on. The marketing documents are attached below for matching.\nKind regards,\nOffice manager\n\nPurchase order RLP-9448 from Velloway Gear Systems\n- line 1: handlebar grips; 72 sets at $12.00\n- line 2: grease; 84 tubes at $5.00\n- line 3: spoke nipples; 8 packs at $6.00\n- order total: $1,332.00\n\nGoods receipt RLR-6095\n- line 1: received 71 sets\n- line 2: received 84 tubes\n- line 3: received 5 packs\n\nInvoice RLI-67903 for purchase order RLP-9448\n- line 1: handlebar grips; 72 sets at $12.42\n- line 2: grease; 84 tubes at $4.64\n- line 3: spoke nipples; 8 packs at $6.00\n- invoice total: $1,332.00",
  "question": "Ridgeline Cycle Works AP policy: each invoice gets exactly one action.\n- Price: invoiced unit price minus PO unit price is a proportion that is less than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nLooking at the unit prices on invoice RLI-67903, which line, if any, fails the price check?",
  "options": [
   "grease",
   "spoke nipples",
   "None of the lines",
   "handlebar grips"
  ]
 }
]
