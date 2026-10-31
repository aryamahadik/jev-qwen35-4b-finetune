# G5-H blind read T12-blind_read-0d6842c6-005 (family T12)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T12/qc/g5h/answers/T12-blind_read-0d6842c6-005.json

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
  "qid": "q5b32be555f",
  "kind": "yes/no",
  "text": "{\"to\": \"Sunniva Haugland\", \"from\": \"billing contact\", \"subject\": \"field service team, invoice EVR-77452\", \"body\": \"Attached for matching.\"}\n\nPurchase order EPU-5901 from Silverline Hygiene Products\n- line 1: surgical gloves; 120 boxes at 17.00 EUR\n- line 2: hand sanitiser; 166 bottles at 10.00 EUR\n- line 3: syringes; 200 boxes at 13.00 EUR\n- order total: 6,300.00 EUR\n\nGoods receipt EGN-8328\n- line 1: received 120 boxes\n- line 2: received 166 bottles\n- line 3: received 198 boxes\n\nInvoice EVR-77452 for purchase order EPU-5901\n- line 1: surgical gloves; 120 boxes at 17.01 EUR\n- line 2: hand sanitiser; 165 bottles at 10.30 EUR\n- line 3: syringes; 198 boxes at 12.43 EUR\n- invoice total: 6,201.84 EUR\n\nPaid-invoice register for Silverline Hygiene Products: EVR-27452, EVR-39196",
  "question": "For invoice EVR-77452, when only the price check is judged on its own, does the invoice fail that check under the card?",
  "definitions": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Price check: invoiced unit price minus PO unit price is a share that is less than 3 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then duplicate, then price.\nThe action is set by the first failing check in the check order.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q400322d32a",
  "kind": "yes/no",
  "text": "Subject: paperwork from Ostrander Chemical Supply for the field service team\nFrom: receiving dock\nDetails: papers attached, forwarded to Malik Osei for matching.\n\nPurchase order LPR-3446 from Ostrander Chemical Supply\n- line 1: laundry detergent; 24 drums at 40.21 USD\n- line 2: garment bags; four rolls at 22.32 USD\n- order total: 1,054.32 USD\n\nGoods receipt LRC-2668\n- line 1: received 24 drums\n- line 2: received four rolls\n\nInvoice LBI-55095 for purchase order LPR-3446\n- line 1: laundry detergent; 24 drums at 40.18 USD\n- line 2: garment bags; four rolls at 22.50 USD\n- invoice total: 1,054.32 USD",
  "question": "Is it true that invoice LBI-55095 gets sent to price-variance review, and that is all?",
  "definitions": "AP policy of Clearwater Linen Services: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is 0.25 USD or lower on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qdcde928551",
  "kind": "yes/no",
  "text": "Hi,\nSupplier invoice SUB-71870 is pasted below for matching, and it belongs to PO EQP-6440 for the laboratory team.\nThanks,\nRafael Quintero\n\nInvoice SUB-71870 for purchase order EQP-6440\n- line 1: yoga mats; 200 units at 44.76 USD\n- line 2: whey powder; 40 bags at 64.85 USD\n- invoice total: $11,546\n\nPaid-invoice register for Redmere Protein Supply: SUB-37141, SUB-33570, SUB-12208, SUB-71800\n\nPurchase order EQP-6440 from Redmere Protein Supply\n- line 1: yoga mats; 200 units at 44.81 USD\n- line 2: whey powder; 40 bags at 64.60 USD\n- order total: $11,546\n\nGoods receipt RCD-3254\n- line 1: received 200 units\n- line 2: received 40 bags",
  "question": "Is invoice SUB-71870 released for payment?",
  "definitions": "Brickhollow Fitness Group AP policy: each invoice gets exactly one action.\n1. Price: invoiced unit price minus PO unit price is less than or equal to $1 on every line. If it fails: price-variance review.\n2. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n3. Approval limit: invoice total is at most 12,054.18 USD (limit of approver Ravi Thakur). If it fails: route to a senior approver.\n4. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then quantity, then approval limit, then duplicate.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qc554453a42",
  "kind": "yes/no",
  "text": "Hi Aoife Brennan! Here is purchase order PQS-6297 for the facilities team, forwarded for matching. Thanks a lot!\n\nPurchase order PQS-6297 | vendor Veldman Cable Works\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | battery packs | 30 packs | $21.30 |\n| 2 | printer toner | 54 cartons | $32.11 |\n| 3 | server racks | 48 units | $457.53 |\n| total | | | $24,334.38 |\n\nGoods receipt RQS-3403\n| line | received |\n|---|---|\n| 1 | 30 packs |\n| 2 | 53 cartons |\n| 3 | 48 units |\n\nInvoice IQS-91861 | purchase order PQS-6297\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | battery packs | 30 packs | $20.98 |\n| 2 | printer toner | 54 cartons | $32.11 |\n| 3 | server racks | 48 units | $457.73 |\n| total | | | $24,334.38 |",
  "question": "Under the policy, does invoice IQS-91861 go to price-variance review as its only action?",
  "definitions": "AP policy of Quorin Digital Services: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is lower than $0.20 on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nThe action is fixed by the first failing check in the check order, and a later check does not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qfba770cd5a",
  "kind": "choice",
  "text": "Purchase order export, po_number FPO-7978, vendor Redcliffe Spice Merchants\nline,item,quantity,unit_price\n1,paper cartons,15 cartons,3.20\ntotal,,,48.00\n\nGoods receipt export, gr_number FGR-2984\nline,received\n1,13 cartons\n\nInvoice export, invoice_number FIN-40956, po_number FPO-7978\nline,item,quantity,unit_price\n1,paper cartons,15 cartons,3.37\ntotal,,,50.55\n\nfrom: procurement officer, same as usual\nto: Ingrid Solberg\nteam: the facilities team\nbits: pasted below for matching",
  "question": "Oakridge Food Producers AP policy: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Approval limit | invoice total is lower than £500 (limit of approver Farida Qureshi) | route to a senior approver |\n| Price | invoiced unit price minus PO unit price is a proportion that equals or is lower than 5 percent of the PO unit price on every line | price-variance review |\n| Quantity | invoiced quantity at most received quantity on every line | hold for receipt |\nCheck order: approval limit, then price, then quantity.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nGoing by the way the AP policy treats invoice FIN-40956, what line, if any, fails the price check?",
  "options": [
   "None of the lines",
   "paper cartons"
  ]
 },
 {
  "qid": "q5343872ac3",
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
  "qid": "q28f195b52d",
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
  "qid": "qb90fafc6f4",
  "kind": "choice",
  "text": "Hi Rafael Quintero. Sending the IT support team papers. PO EQP-8811 is in the pack, attached.\n\nInvoice SUB-95921 for purchase order EQP-8811\n- line 1: whey powder; 98 bags at $144.68\n- line 2: cleaning spray; 50 bottles at $13.01\n- line 3: resistance bands; 70 packs at $14.46\n- invoice total: $15,841.34\n\nPurchase order EQP-8811 from Redmere Protein Supply\n- line 1: whey powder; 96 bags at $144.58\n- line 2: cleaning spray; 48 bottles at $13.09\n- line 3: resistance bands; 72 packs at $14.35\n- order total: $15,541.20\n\nGoods receipt RCD-4213\n- line 1: received 96 bags\n- line 2: received 48 bottles\n- line 3: received 70 packs",
  "question": "AP policy of Brickhollow Fitness Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is at or below $0.25 on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nA later check in the check order does not change an action that is already decided.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nUnder this policy, what becomes of invoice SUB-95921 as an action?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "q4658adddf1",
  "kind": "choice",
  "text": "Purchase order export, po_number DPO-4861, vendor Tallgrass Furniture Outfitters\nline,item,quantity,unit_price\n1,cleaning wipes,12 boxes,6.91\ntotal,,,82.92\n\nGoods receipt export, gr_number DGR-8682\nline,received\n1,10 boxes\n\nInvoice export, invoice_number DIV-87460, po_number DPO-4861\nline,item,quantity,unit_price\n1,cleaning wipes,11 boxes,7.12\ntotal,,,78.32\n\nPaid-invoice register export, vendor Tallgrass Furniture Outfitters\ninvoice_number\nDIV-11366\nDIV-87460\nDIV-38492\nDIV-20739\n\n[log-entry] originator=AP clerk Rhea Delacroix\nteam=facilities, supplier=Tallgrass Furniture Outfitters, invoice=DIV-87460, po=DPO-4861 attached for matching",
  "question": "Maple Ridge School District AP policy: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Approval limit | invoice total is any amount smaller than $78.33 (limit of approver Winston Hobbs) | route to a senior approver |\n| Quantity | invoiced quantity at most received quantity on every line | hold for receipt |\n| Duplicate | invoice number not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Price | invoiced unit price minus PO unit price is equal to or below $0.20 on every line | price-variance review |\nCheck order: approval limit, then quantity, then duplicate, then price.\nThe action follows from the first check that fails when the checks are taken in the check order.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nPlease verify the policy's reading of invoice DIV-87460: which action does it apply?",
  "options": [
   "Release for payment",
   "Reject as a duplicate",
   "Route to a senior approver",
   "Send to price-variance review",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qb9c8edb314",
  "kind": "choice",
  "text": "[ap-note] from AP clerk Aoife Brennan\nto team=facilities, documents pasted below\n\nPurchase order PQS-2854 | vendor Veldman Cable Works\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | laptop docks | 80 units | 152.67 USD |\n| 2 | ethernet cables | 178 spools | 61.28 USD |\n| 3 | battery packs | 48 packs | 17.78 USD |\n| total | | | 23,974.88 USD |\n\nGoods receipt RQS-3161\n| line | received |\n|---|---|\n| 1 | 79 units |\n| 2 | 176 spools |\n| 3 | 47 packs |\n\nInvoice IQS-63268 | purchase order PQS-2854\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | laptop docks | 79 units | 152.67 USD |\n| 2 | ethernet cables | 176 spools | 61.28 USD |\n| 3 | battery packs | 48 packs | 17.97 USD |\n| total | | | 23,708.77 USD |",
  "question": "Quorin Digital Services AP policy: each invoice gets exactly one action.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Approval limit: invoice total is strictly lower than 23,708.78 USD (limit of approver Rajesh Iyer). If it fails: route to a senior approver.\n- Price: invoiced unit price minus PO unit price is lower than 0.20 USD on every line. If it fails: price-variance review.\nCheck order: price, then quantity, then approval limit.\nWalk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nHaving weighed invoice IQS-63268 under the policy, which action has it decided on?",
  "options": [
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review",
   "Route to a senior approver"
  ]
 },
 {
  "qid": "q9b64988173",
  "kind": "yes/no",
  "text": "Purchase order export, po_number FPO-2646, vendor Saltmarsh Packaging Group\nline,item,quantity,unit_price\n1,paper cartons,25 cartons,3.00\ntotal,,,75.00\n\nGoods receipt export, gr_number FGR-3753\nline,received\n1,22 cartons\n\nInvoice export, invoice_number FIN-20151, po_number FPO-2646\nline,item,quantity,unit_price\n1,paper cartons,22 cartons,3.09\ntotal,,,67.98\n\nPaid-invoice register export, vendor Saltmarsh Packaging Group\ninvoice_number\nFIN-52738\nFIN-14526\nFIN-28061\n\n{\"to\": \"Kwame Asamoah\", \"from\": \"office manager\", \"note\": \"The purchase order FPO-2646 from Saltmarsh Packaging Group is attached. It is for the facilities team.\"}",
  "question": "Does the card clear invoice FIN-20151 for payment?",
  "definitions": "AP policy of Oakridge Food Producers: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Approval-limit check | the invoice total is 67.98 GBP or less (limit of approver Hugo Lambert) | route to a senior approver |\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Price check | invoiced unit price minus PO unit price is a proportion equal to or lower than 3 percent of the PO unit price on every line | price-variance review |\nCheck order: approval limit, then duplicate, then quantity, then price.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qc411c1efcb",
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
  "qid": "q5bcecd5a8e",
  "kind": "choice",
  "text": "Clerk: This is Hakan Yilmaz.\nClerk: Writing to the marketing team about the paperwork.\nCaller: Supplier invoice KBI-70864, supplied by Stonebridge Aggregates, is on the way.\n\nPurchase order KBP-5628 | vendor Stonebridge Aggregates\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | plasterboard | 36 units | 22.00 EUR |\n| total | | | 792.00 EUR |\n\nGoods receipt KBG-9886\n| line | received |\n|---|---|\n| 1 | 36 units |\n\nInvoice KBI-70864 | purchase order KBP-5628\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | plasterboard | 36 units | 22.07 EUR |\n| total | | | 794.52 EUR |",
  "question": "Hartwell Build Group AP policy: each invoice gets exactly one action.\n1. Price: invoiced unit price minus PO unit price is a share equal to 3 percent or smaller of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nA later check in the check order does not change an action that is already decided.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nHaving weighed invoice KBI-70864 under the policy, which action has it decided on?",
  "options": [
   "Send to price-variance review",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qb950ef0207",
  "kind": "choice",
  "text": "Hi Rafael Quintero. Sending the field service team papers. PO EQP-8217 is in the pack, attached.\n\nInvoice SUB-31970 for purchase order EQP-8217\n- line 1: resistance bands; 8 packs at 11.61 USD\n- line 2: cleaning spray; 2 bottles at 3.90 USD\n- invoice total: 100.68 USD\n\nPurchase order EQP-8217 from Redmere Protein Supply\n- line 1: resistance bands; 8 packs at 11.61 USD\n- line 2: cleaning spray; 2 bottles at 3.75 USD\n- order total: 100.38 USD\n\nGoods receipt RCD-6903\n- line 1: received 8 packs\n- line 2: received 2 bottles",
  "question": "AP policy of Brickhollow Fitness Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is short of 0.15 USD on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Approval-limit check: the invoice total is short of 100.38 USD (limit of approver Ravi Thakur). If it fails: route to a senior approver.\nCheck order: price, then quantity, then approval limit.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nCan you check how the policy treats invoice SUB-31970 and say which action it gets?",
  "options": [
   "Send to price-variance review",
   "Release for payment",
   "Route to a senior approver",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q18e1840175",
  "kind": "yes/no",
  "text": "Lead note. Sophie Bramble, marketing side. Supplier invoice SPV-59440 from Velden Glass Co, forwarded for matching.\n\nInvoice SPV-59440 for purchase order PRQ-1533\n- line 1: bottling labels; 161 rolls at 14.15 USD\n- line 2: barrel hoops; 92 sets at 23.07 USD\n- invoice total: 4,400.59 USD\n\nPaid-invoice register for Velden Glass Co: SPV-42853, SPV-60728\n\nPurchase order PRQ-1533 from Velden Glass Co\n- line 1: bottling labels; 163 rolls at 13.96 USD\n- line 2: barrel hoops; 94 sets at 23.07 USD\n- order total: 4,444.06 USD\n\nGoods receipt GRZ-2696\n- line 1: received 161 rolls\n- line 2: received 93 sets",
  "question": "Is it right to say that, under this policy, invoice SPV-59440 passes the price check taken on its own?",
  "definitions": "AP policy of Ambersett Wine Cellars: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is beneath 0.20 USD on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Approval-limit check: the invoice total is at or below 25,000.00 USD (limit of approver Anaya Iyer). If it fails: route to a senior approver.\n4. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then quantity, then approval limit, then duplicate.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q12233267a7",
  "kind": "yes/no",
  "text": "Hello,\nThe facilities team purchase is under PO FPO-8903. Supplier invoice FSI-52718 is attached for matching.\nRegards,\nHaruka Sakai\n\nInvoice FSI-52718 for purchase order FPO-8903\n- line 1: mineral blocks; 1 pallet at £92.62\n- line 2: seed potatoes; 2 bags at £38.48\n- invoice total: £169.58\n\nPaid-invoice register for Havenbrook Tractor Parts: FSI-20823, FSI-80869\n\nPurchase order FPO-8903 from Havenbrook Tractor Parts\n- line 1: mineral blocks; 2 pallets at £92.55\n- line 2: seed potatoes; 5 bags at £37.99\n- order total: £375.05\n\nGoods receipt FGR-5735\n- line 1: received 2 pallets\n- line 2: received 5 bags",
  "question": "Is it right that the policy stops or blocks payment of invoice FSI-52718?",
  "definitions": "AP policy of Marrowdale Farm Cooperative: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is smaller than £0.50 on every line. If it fails: price-variance review.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: quantity, then price, then duplicate.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q9775289745",
  "kind": "yes/no",
  "text": "Hey there,\nJust a little note for the file about the marketing team purchase under PO RXO-3634, which is pasted below for matching.\nCheers,\nNoa Friedman\n\nInvoice RXB-50746 for purchase order RXO-3634\n- line 1: blister packs; 97 packs at €11.33\n- line 2: gauze pads; 45 packs at €8.00\n- line 3: amber vials; 24 packs at €19.55\n- invoice total: €1,928.21\n\nPurchase order RXO-3634 from Vellmar Dispensing Co\n- line 1: blister packs; 100 packs at €11.00\n- line 2: gauze pads; 48 packs at €8.00\n- line 3: amber vials; 24 packs at €19.00\n- order total: €1,940.00\n\nGoods receipt RXR-7427\n- line 1: received 100 packs\n- line 2: received 45 packs\n- line 3: received 23 packs",
  "question": "Under the AP policy, does invoice RXB-50746 pass the price check taken on its own?",
  "definitions": "AP policy of Medgrove Pharmacy Group: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is a proportion lower than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n3. Approval-limit check: the invoice total is not more than €1,363.25 (limit of approver Gideon Mwangi). If it fails: route to a senior approver.\nCheck order: quantity, then price, then approval limit.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q49a266a25f",
  "kind": "choice",
  "text": "Purchase order export, po_number PFM-8083, vendor Ravenscourt Fixtures Supply\nline,item,quantity,unit_price\n1,filter panels,24 boxes,62.00\n2,sealant tubes,132 tubes,5.00\n3,light bulbs,16 boxes,40.00\ntotal,,,2788.00\n\nGoods receipt export, gr_number RFM-4954\nline,received\n1,24 boxes\n2,132 tubes\n3,16 boxes\n\nInvoice export, invoice_number IFM-83987, po_number PFM-8083\nline,item,quantity,unit_price\n1,filter panels,24 boxes,62.00\n2,sealant tubes,132 tubes,5.00\n3,light bulbs,16 boxes,40.00\ntotal,,,2788.00\n\nPaid-invoice register export, vendor Ravenscourt Fixtures Supply\ninvoice_number\nIFM-83987\nIFM-83977\nIFM-77514\nIFM-22839\n\n{\"from\": \"Mirela Popescu\", \"to\": \"file\", \"team\": \"facilities\", \"details\": \"Copies attached for matching, under purchase order PFM-8083.\"}",
  "question": "AP policy of Brenton Estate Services: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Price check | invoiced unit price minus PO unit price is a portion lower than one percent of the PO unit price on every line | price-variance review |\nCheck order: quantity, then duplicate, then price.\nOnce the first failing check in the check order has set the action, later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWith reference to the card, what action is set out for invoice IFM-83987?",
  "options": [
   "Reject as a duplicate",
   "Send to price-variance review",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q157c37e32f",
  "kind": "choice",
  "text": "Hello file, sending the laboratory paperwork, pasted below for matching, from Oluwaseun Adeyemi. Best wishes, AP clerk\n\nInvoice BIN-45995 for purchase order ARQ-7442\n- line 1: drafting film; 30 rolls at €45.33\n- line 2: plotter ink; 120 bottles at €37.96\n- line 3: concrete mix; 187 bags at €7.66\n- invoice total: €7,347.52\n\nPaid-invoice register for Stonecradle Quarries: BIN-45995, BIN-45991\n\nPurchase order ARQ-7442 from Stonecradle Quarries\n- line 1: drafting film; 30 rolls at €45.33\n- line 2: plotter ink; 120 bottles at €37.96\n- line 3: concrete mix; 187 bags at €7.66\n- order total: €7,347.52\n\nGoods receipt RCP-4705\n- line 1: received 30 rolls\n- line 2: received 120 bottles\n- line 3: received 187 bags",
  "question": "AP policy of Quellon Architects: each invoice gets exactly one action.\n- Approval-limit check: the invoice total is less than €7,347.52 (limit of approver Sami Laurila). If it fails: route to a senior approver.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is strictly beneath €0.15 on every line. If it fails: price-variance review.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: price, then approval limit, then quantity, then duplicate.\nThe earliest failing check in the check order settles the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does this policy give invoice BIN-45995?",
  "options": [
   "Release for payment",
   "Reject as a duplicate",
   "Route to a senior approver",
   "Send to price-variance review",
   "Hold for receipt"
  ]
 },
 {
  "qid": "q5844c959ad",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"VHP-3694\",\"vendor\":\"Ardelle Amenities Company\",\"lines\":[{\"line\":1,\"item\":\"pillows\",\"quantity\":\"3 units\",\"unit_price_cents\":4200}],\"total_cents\":12600}\n\nGoods receipt (JSON):\n{\"gr_number\":\"VHG-7287\",\"lines\":[{\"line\":1,\"received\":\"2 units\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"VHI-58379\",\"po_number\":\"VHP-3694\",\"lines\":[{\"line\":1,\"item\":\"pillows\",\"quantity\":\"3 units\",\"unit_price_cents\":4337}],\"total_cents\":13011}\n\nfrom: procurement officer, same as usual\nto: Anselm Richter\nteam: the field service team\nbits: pasted below for matching",
  "question": "So does invoice VHI-58379 fail the price check when you look at that check on its own?",
  "definitions": "AP policy of Velmora Boutique Hotel: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Price check | invoiced unit price minus PO unit price is a proportion that equals or is lower than 1 percent of the PO unit price on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: price, then quantity.\nThe action stands once it is set, because checks that come later in the check order do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qa642c9a925",
  "kind": "choice",
  "text": "Caller: Hello, we are the field service team.\nClerk: Hello, Dimitri Sorokin from AP here. Supplier invoice IQS-81833 from Stratocore Networking is being sent over.\n\nPurchase order PQS-7469 | vendor Stratocore Networking\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | printer toner | 2 cartons | 70.86 USD |\n| 2 | ethernet cables | 98 spools | 72.56 USD |\n| 3 | battery packs | 200 packs | 14.29 USD |\n| 4 | laptop docks | 30 units | 114.61 USD |\n| total | | | 13,548.90 USD |\n\nGoods receipt RQS-9709\n| line | received |\n|---|---|\n| 1 | 2 cartons |\n| 2 | 98 spools |\n| 3 | 200 packs |\n| 4 | 30 units |\n\nInvoice IQS-81833 | purchase order PQS-7469\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | printer toner | 2 cartons | 70.86 USD |\n| 2 | ethernet cables | 98 spools | 72.56 USD |\n| 3 | battery packs | 200 packs | 14.29 USD |\n| 4 | laptop docks | 30 units | 114.61 USD |\n| total | | | 13,548.90 USD |",
  "question": "AP policy of Quorin Digital Services: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is at most 0.15 USD on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Approval-limit check: the invoice total is strictly beneath 5,000.00 USD (limit of approver Hannah Lindau). If it fails: route to a senior approver.\nCheck order: quantity, then price, then approval limit.\nTake the checks in the check order and let the first one that fails set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nDouble-checking the card, which action does it assign to invoice IQS-81833?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Route to a senior approver",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q9935f8984f",
  "kind": "choice",
  "text": "Cheers, Declan Quigley, from billing. The marketing team papers, covering invoice FSI-15573 and purchase order FPO-6665, are attached below. Warmly yours!\n\nInvoice FSI-15573 for purchase order FPO-6665\n- line 1: diesel filters; 35 units at 30.38 GBP\n- line 2: baling twine; twenty rolls at 16.88 GBP\n- line 3: mineral blocks; 75 pallets at 172.10 GBP\n- invoice total: 14,308.40 GBP\n\nPurchase order FPO-6665 from Brackley Seed Merchants\n- line 1: diesel filters; 36 units at 30.28 GBP\n- line 2: baling twine; twenty rolls at 16.59 GBP\n- line 3: mineral blocks; 75 pallets at 177.66 GBP\n- order total: 14,746.38 GBP\n\nGoods receipt FGR-4326\n- line 1: received 35 units\n- line 2: received nineteen rolls\n- line 3: received 75 pallets",
  "question": "AP policy of Marrowdale Farm Cooperative: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is 0.25 GBP or less on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nOnce a check fails in the check order, later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nHere's the deal: which action is the policy putting on invoice FSI-15573?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "q69535cf9ab",
  "kind": "choice",
  "text": "{\"to\": \"Dimitri Sorokin\",\n\"from\": \"AP intern\",\n\"note\": \"So, Stratocore Networking papers for the marketing team are pasted below. Enjoy the rest of your sunshine!\"}\n\nPurchase order PQS-1019 | vendor Stratocore Networking\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | laptop docks | 130 units | 135.36 USD |\n| 2 | server racks | 96 units | 933.30 USD |\n| total | | | 107,193.60 USD |\n\nGoods receipt RQS-3014\n| line | received |\n|---|---|\n| 1 | 130 units |\n| 2 | 94 units |\n\nInvoice IQS-25824 | purchase order PQS-1019\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | laptop docks | 128 units | 136.66 USD |\n| 2 | server racks | 96 units | 933.63 USD |\n| total | | | 107,120.96 USD |",
  "question": "AP policy of Quorin Digital Services: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is lower than 1.50 USD on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nA later check in the check order does not change an action that is already decided.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nUnder the terms of this policy, which action applies to invoice IQS-25824?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Release for payment"
  ]
 },
 {
  "qid": "qaa7e070ba6",
  "kind": "yes/no",
  "text": "Note for the file from Ilse Brandt.\nThis is for the laboratory team: PO LPO-3496, supplier invoice LSI-48200, papers attached for matching, happy to keep it on record.\n\nPurchase order LPO-3496 | vendor Corvin Ribbon Works\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | roses | 66 boxes | $26.00 |\n| 2 | floral foam | 144 packs | $7.00 |\n| 3 | ceramic vases | 177 units | $17.00 |\n| 4 | wire stems | 75 rolls | $10.00 |\n| total | | | $6,483.00 |\n\nGoods receipt LGR-5071\n| line | received |\n|---|---|\n| 1 | 66 boxes |\n| 2 | 144 packs |\n| 3 | 177 units |\n| 4 | 75 rolls |\n\nInvoice LSI-48200 | purchase order LPO-3496\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | roses | 66 boxes | $26.00 |\n| 2 | floral foam | 144 packs | $7.00 |\n| 3 | ceramic vases | 177 units | $17.00 |\n| 4 | wire stems | 75 rolls | $10.00 |\n| total | | | $6,483.00 |\n\nPaid-invoice register | vendor Corvin Ribbon Works\n| invoice number |\n|---|\n| LSI-72524 |\n| LSI-60303 |\n| LSI-61590 |",
  "question": "Does the policy decide that invoice LSI-48200 is released for payment?",
  "definitions": "AP policy of Larkspur Flower Group: each invoice gets exactly one action.\n1. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n2. Price check: invoiced unit price minus PO unit price is a proportion that equals or is lower than three percent of the PO unit price on every line. If it fails: price-variance review.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: duplicate, then price, then quantity.\nThe action stands once it is set, because checks that come later in the check order do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q011c8a50eb",
  "kind": "yes/no",
  "text": "Caller: Team assistant here, for the IT support team.\nClerk: Dev Malhotra, AP. Documents from Pendlebury Animal Pharma are being sent over, with purchase order MHP-1161.\n\nPurchase order MHP-1161 | vendor Pendlebury Animal Pharma\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | sutures | 5 packs | £9.99 |\n| 2 | antiseptic wipes | 20 boxes | £8.91 |\n| total | | | £228.15 |\n\nGoods receipt MHG-3040\n| line | received |\n|---|---|\n| 1 | 5 packs |\n| 2 | 17 boxes |\n\nInvoice MHI-15295 | purchase order MHP-1161\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | sutures | 5 packs | £10.19 |\n| 2 | antiseptic wipes | 17 boxes | £9.09 |\n| total | | | £205.48 |",
  "question": "Would you say it is not true that invoice MHI-15295 is not released for payment under the policy?",
  "definitions": "Meadowsend Animal Hospital AP policy: each invoice gets exactly one action.\n1. Price: invoiced unit price minus PO unit price is short of £0.20 on every line. If it fails: price-variance review.\n2. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n3. Approval limit: invoice total is at or below £146.76 (limit of approver Nomvula Dube). If it fails: route to a senior approver.\nCheck order: price, then quantity, then approval limit.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q8cf4089ee1",
  "kind": "choice",
  "text": "Hello,\nFor the marketing purchase, the papers are pasted below for matching.\nRegards,\nBruno Ferreira\n\nInvoice RXB-42918 for purchase order RXO-4074\n- line 1: blister packs; 50 packs at 10.28 EUR\n- line 2: amber vials; 56 packs at 10.75 EUR\n- invoice total: 1,116.00 EUR\n\nPaid-invoice register for Asterholm Generics: RXB-99786, RXB-88780\n\nPurchase order RXO-4074 from Asterholm Generics\n- line 1: blister packs; 50 packs at 10.00 EUR\n- line 2: amber vials; 56 packs at 11.00 EUR\n- order total: 1,116.00 EUR\n\nGoods receipt RXR-2932\n- line 1: received 50 packs\n- line 2: received 56 packs",
  "question": "AP policy of Medgrove Pharmacy Group: each invoice gets exactly one action.\n1. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Price check: invoiced unit price minus PO unit price is a portion that is 1 percent or below of the PO unit price on every line. If it fails: price-variance review.\nCheck order: duplicate, then quantity, then price.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does the AP policy assign to invoice RXB-42918 under its stated sequence of steps?",
  "options": [
   "Send to price-variance review",
   "Release for payment",
   "Reject as a duplicate",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qf0715410ce",
  "kind": "choice",
  "text": "Clerk: Greetings, this is the accounts payable clerk.\nCaller: Greetings. We are the laboratory team.\nClerk: Thank you. My name is Kiyoshi Mori.\nCaller: Copies tied to purchase order OPO-8138 are on their way.\n\nInvoice OIN-93826 for purchase order OPO-8138\n- line 1: cleaning cloths; 50 packs at 6.05 GBP\n- invoice total: 302.50 GBP\n\nPurchase order OPO-8138 from Corrin Frame Works\n- line 1: cleaning cloths; 50 packs at £6\n- order total: £300\n\nGoods receipt OGR-8932\n- line 1: received 50 packs",
  "question": "AP policy of Lumenvale Eyecare Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a share strictly less than one percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nWalk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nAnswer codes: Heron = release for payment, Kestrel = hold for receipt, Plover = price-variance review.\nNothing else applies: the policy and the documents shown are complete.\n\nHaving weighed invoice OIN-93826 under the policy, which action has it decided on?",
  "options": [
   "Heron",
   "Plover",
   "Kestrel"
  ]
 },
 {
  "qid": "q087520e409",
  "kind": "choice",
  "text": "Clerk: Thandiwe Mokoena here, go ahead.\nCaller: Thank you kindly. The warehouse purchase documents are pasted below for matching.\n\nPurchase order NHM-3960 from Tessaly Preservation Works\n- line 1: storage drawers; 25 units at 59.95 EUR\n- order total: 1,498.75 EUR\n\nGoods receipt GRN-5929\n- line 1: received 22 units\n\nInvoice SUP-11937 for purchase order NHM-3960\n- line 1: storage drawers; 25 units at 60.45 EUR\n- invoice total: 1,511.25 EUR",
  "question": "AP policy of Northgate Natural History Museum: each invoice gets exactly one action.\n1. Approval-limit check: the invoice total is lower than 1,511.25 EUR (limit of approver Emil Strand). If it fails: route to a senior approver.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Price check: invoiced unit price minus PO unit price is any amount smaller than 0.50 EUR on every line. If it fails: price-variance review.\nCheck order: approval limit, then quantity, then price.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nGoing by the way the AP policy treats invoice SUP-11937, what line, if any, fails the price check?",
  "options": [
   "storage drawers",
   "None of the lines"
  ]
 },
 {
  "qid": "q39d93062fe",
  "kind": "yes/no",
  "text": "From: Felix Brunner\nTo: AP lead\nTeam: laboratory team\nPO NHM-9716, docs attached.\n\nPurchase order NHM-9716 from Tessaly Preservation Works\n- line 1: museum tissue; three reams at 6.61 EUR\n- line 2: glass vials; 150 boxes at 13.69 EUR\n- order total: 2,073.33 EUR\n\nGoods receipt GRN-1852\n- line 1: received one ream\n- line 2: received 149 boxes\n\nInvoice SUP-84568 for purchase order NHM-9716\n- line 1: museum tissue; one ream at 6.61 EUR\n- line 2: glass vials; 149 boxes at 13.89 EUR\n- invoice total: 2,076.22 EUR",
  "question": "Would the AP policy simply send invoice SUP-84568 to price-variance review and leave it there?",
  "definitions": "AP policy of Northgate Natural History Museum: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is falling short of 0.20 EUR on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nWork through the check order, and when you find the first failing check, use it to set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q750a718a37",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"KPO-2207\",\"vendor\":\"Brassfield Plate Works\",\"lines\":[{\"line\":1,\"item\":\"binding glue\",\"quantity\":\"50 bottles\",\"unit_price_cents\":1660},{\"line\":2,\"item\":\"printing plates\",\"quantity\":\"6 units\",\"unit_price_cents\":5597}],\"total_cents\":116582}\n\nGoods receipt (JSON):\n{\"gr_number\":\"KGR-6255\",\"lines\":[{\"line\":1,\"received\":\"49 bottles\"},{\"line\":2,\"received\":\"4 units\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"KVI-77743\",\"po_number\":\"KPO-2207\",\"lines\":[{\"line\":1,\"item\":\"binding glue\",\"quantity\":\"50 bottles\",\"unit_price_cents\":1617},{\"line\":2,\"item\":\"printing plates\",\"quantity\":\"4 units\",\"unit_price_cents\":5601}],\"total_cents\":103254}\n\n[dock] from=receiving dock to=Ruth Ambrose team=IT support invoice=KVI-77743 attached",
  "question": "Under the AP policy, is payment of invoice KVI-77743 blocked?",
  "definitions": "Ashgrove Printing House AP policy: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Quantity | invoiced quantity at most received quantity on every line | hold for receipt |\n| Price | invoiced unit price minus PO unit price is beneath $0.15 on every line | price-variance review |\nCheck order: quantity, then price.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q2d428e2827",
  "kind": "yes/no",
  "text": "Caller: Hello there, we are the laboratory team, and we are grateful for the help.\nClerk: How lovely to hear from you, Harriet Quayle here, and the papers are being sent across for matching: supplier invoice ILS-65505 from Pemberton Lighting Rentals and purchase order PLS-6577.\n\nPurchase order PLS-6577 | vendor Pemberton Lighting Rentals\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | timber battens | ten units | 3.72 GBP |\n| total | | | 37.20 GBP |\n\nGoods receipt GLS-7249\n| line | received |\n|---|---|\n| 1 | ten units |\n\nInvoice ILS-65505 | purchase order PLS-6577\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | timber battens | ten units | 3.82 GBP |\n| total | | | 38.20 GBP |\n\nPaid-invoice register | vendor Pemberton Lighting Rentals\n| invoice number |\n|---|\n| ILS-34643 |\n| ILS-24934 |",
  "question": "Is the verdict for invoice ILS-65505, as this policy sets it, that it is released for payment?",
  "definitions": "AP policy of Lantern Street Players: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is lower than 0.10 GBP on every line. If it fails: price-variance review.\n2. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then duplicate, then quantity.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qf22bfa7e08",
  "kind": "choice",
  "text": "Felix Brunner: For the facilities team, the supplier invoice SUP-78046 from Halvard Specimen Supply is attached.\nCaller: Thanks, we have it.\n\nPurchase order NHM-6661 from Halvard Specimen Supply\n- line 1: glass vials; three boxes at 11.18 EUR\n- line 2: cotton gloves; 60 packs at 11.56 EUR\n- line 3: preservative fluid; 96 bottles at 14.86 EUR\n- line 4: storage drawers; eleven units at 149.08 EUR\n- order total: 3,793.58 EUR\n\nGoods receipt GRN-1527\n- line 1: received two boxes\n- line 2: received 60 packs\n- line 3: received 96 bottles\n- line 4: received eight units\n\nInvoice SUP-78046 for purchase order NHM-6661\n- line 1: glass vials; three boxes at 11.18 EUR\n- line 2: cotton gloves; 60 packs at 11.45 EUR\n- line 3: preservative fluid; 96 bottles at 14.86 EUR\n- line 4: storage drawers; eleven units at 149.68 EUR\n- invoice total: 3,793.58 EUR\n\nPaid-invoice register for Halvard Specimen Supply: SUP-70652, SUP-57844",
  "question": "Northgate Natural History Museum AP policy: each invoice gets exactly one action.\n- Price: invoiced unit price minus PO unit price is 0.10 EUR or less on every line. If it fails: price-variance review.\n- Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then duplicate, then price.\nEvery check that comes after the failing one in the check order does not change the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nLooking at all of it, what should we do with invoice SUP-78046?",
  "options": [
   "Reject as a duplicate",
   "Send to price-variance review",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qbc2029bd05",
  "kind": "yes/no",
  "text": "Caller: Hello, this is the supplier's billing contact.\nClerk: Hello, this is Lenka Svoboda.\nCaller: Thank you, the documents for the laboratory team are being sent over.\n\nInvoice BIN-39975 for purchase order ARQ-6385\n- line 1: oak planks; 4 units at €92.92\n- line 2: scale models; 32 kits at €116.24\n- invoice total: €4,091.36\n\nPaid-invoice register for Brackenmoor Glazing: BIN-82904, BIN-27458, BIN-88820, BIN-52116\n\nPurchase order ARQ-6385 from Brackenmoor Glazing\n- line 1: oak planks; 5 units at €90.93\n- line 2: scale models; 36 kits at €114.24\n- order total: €4,567.29\n\nGoods receipt RCP-5097\n- line 1: received 4 units\n- line 2: received 33 kits",
  "question": "As a new clerk on the AP team, does invoice BIN-39975 fail the price check taken on its own?",
  "definitions": "Quellon Architects AP policy: each invoice gets exactly one action.\n1. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n2. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Price: invoiced unit price minus PO unit price is smaller than €2.00 on every line. If it fails: price-variance review.\nCheck order: quantity, then duplicate, then price.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q99b2189ea5",
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
  "qid": "q99ea1ef1b8",
  "kind": "yes/no",
  "text": "[warm-note] hello Lauren Mistry, the field service team lead here, invoice ILS-32017 from Halden Costume House is attached for matching, big thanks\n\nPurchase order PLS-5735 | vendor Halden Costume House\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | timber battens | 133 units | 4.18 GBP |\n| 2 | colour gels | 12 rolls | 7.21 GBP |\n| total | | | 642.46 GBP |\n\nGoods receipt GLS-2119\n| line | received |\n|---|---|\n| 1 | 133 units |\n| 2 | 10 rolls |\n\nInvoice ILS-32017 | purchase order PLS-5735\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | timber battens | 133 units | 4.23 GBP |\n| 2 | colour gels | 10 rolls | 6.86 GBP |\n| total | | | 631.19 GBP |",
  "question": "Is the verdict for invoice ILS-32017, as this policy sets it, that it is released for payment?",
  "definitions": "AP policy of Lantern Street Players: each invoice gets exactly one action.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Price check: invoiced unit price minus PO unit price is falling short of 0.10 GBP on every line. If it fails: price-variance review.\n- Approval-limit check: the invoice total is below 2,000.00 GBP (limit of approver Gordon Fairweather). If it fails: route to a senior approver.\nCheck order: approval limit, then price, then quantity.\nTake the checks in the check order and let the first one that fails set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qa6da7a55cb",
  "kind": "yes/no",
  "text": "[team-lead] from=team lead to=Idris Bello regarding the warehouse team\nsupplier Brightwell Scenic Supply, invoice ILS-70878 pasted below, lovely working with you\n\nPurchase order PLS-2209 | vendor Brightwell Scenic Supply\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | gaffer tape | 12 rolls | 16.98 GBP |\n| total | | | 203.76 GBP |\n\nGoods receipt GLS-5123\n| line | received |\n|---|---|\n| 1 | 12 rolls |\n\nInvoice ILS-70878 | purchase order PLS-2209\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | gaffer tape | 12 rolls | 17.19 GBP |\n| total | | | 206.28 GBP |\n\nPaid-invoice register | vendor Brightwell Scenic Supply\n| invoice number |\n|---|\n| ILS-31015 |\n| ILS-10502 |\n| ILS-63916 |",
  "question": "Does invoice ILS-70878 get stuck as not released for payment under the policy?",
  "definitions": "AP policy of Lantern Street Players: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is any amount smaller than 0.50 GBP on every line. If it fails: price-variance review.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity, then duplicate.\nApply the check order in sequence, and let the first check that fails determine the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q5ad1df7f3c",
  "kind": "yes/no",
  "text": "Dear Tendai Moyo,\nThank you for your kind attention. The papers for the laboratory team, supplied by Redmere Protein Supply, are being sent along and attached for matching.\nWith sincere gratitude,\n\nInvoice SUB-57633 for purchase order EQP-7303\n- line 1: whey powder; 36 bags at $152.82\n- line 2: hand towels; 80 packs at $10.68\n- line 3: resistance bands; 34 packs at $10.31\n- line 4: cleaning spray; 75 bottles at $12.62\n- invoice total: $7,652.96\n\nPurchase order EQP-7303 from Redmere Protein Supply\n- line 1: whey powder; 36 bags at $152.82\n- line 2: hand towels; 80 packs at $10.85\n- line 3: resistance bands; 34 packs at $9.91\n- line 4: cleaning spray; 75 bottles at $12.62\n- order total: $7,652.96\n\nGoods receipt RCD-9408\n- line 1: received 36 bags\n- line 2: received 80 packs\n- line 3: received 34 packs\n- line 4: received 74 bottles",
  "question": "Is it true, as a new clerk, that invoice SUB-57633 fails the price check taken by itself?",
  "definitions": "AP policy of Brickhollow Fitness Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is not more than $0.15 on every line. If it fails: price-variance review.\n2. Approval-limit check: the invoice total is $6,270.19 or less (limit of approver Ravi Thakur). If it fails: route to a senior approver.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then approval limit, then quantity.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q647c03a6a5",
  "kind": "yes/no",
  "text": "Raised by: office manager\nTeam: warehouse\nSubject: PO attached\nTo: Yara Benitez\n\nPurchase order RLP-9271 from Velloway Gear Systems\n- line 1: brake cables; 8 packs at $9\n- line 2: inner tubes; 25 units at $5\n- line 3: grease; 150 tubes at $8\n- line 4: bicycle chains; 16 units at $15\n- order total: $1,637\n\nGoods receipt RLR-3268\n- line 1: received 7 packs\n- line 2: received 25 units\n- line 3: received 149 tubes\n- line 4: received 16 units\n\nInvoice RLI-66123 for purchase order RLP-9271\n- line 1: brake cables; 8 packs at $9\n- line 2: inner tubes; 25 units at $5\n- line 3: grease; 150 tubes at $8\n- line 4: bicycle chains; 16 units at $15\n- invoice total: $1,637\n\nBilling notice: continued service for Velloway Gear Systems depends on payment, so please pay as soon as possible.",
  "question": "Does the policy's handling of invoice RLI-66123 come down to price-variance review as the sole action?",
  "definitions": "AP policy of Ridgeline Cycle Works: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a proportion that is less than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q34361dc02b",
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
  "qid": "qe8a08abb58",
  "kind": "yes/no",
  "text": "Greetings,\nHere are the warehouse team pieces: PO EQP-8336 and supplier invoice SUB-27972, forwarded for matching.\nKind regards,\nTendai Moyo\n\nInvoice SUB-27972 for purchase order EQP-8336\n- line 1: whey powder; 50 bags at $68.14\n- line 2: yoga mats; 8 units at $37.11\n- invoice total: $3,703.88\n\nPurchase order EQP-8336 from Cobalt Rubber Mats\n- line 1: whey powder; 50 bags at $68.22\n- line 2: yoga mats; 8 units at $36.61\n- order total: $3,703.88\n\nGoods receipt RCD-2222\n- line 1: received 50 bags\n- line 2: received 8 units",
  "question": "Under the policy, does the treatment of invoice SUB-27972 leave it not released for payment?",
  "definitions": "AP policy of Brickhollow Fitness Group: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is lower than $0.75 on every line. If it fails: price-variance review.\n3. Approval-limit check: the invoice total is no more than $3,703.88 (limit of approver Ravi Thakur). If it fails: route to a senior approver.\nCheck order: quantity, then price, then approval limit.\nTake the checks in the check order and let the first one that fails set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qe2270b2472",
  "kind": "choice",
  "text": "Caller: Hello, this is the team lead from the purchase side, writing to Paolo Greco.\nClerk: Hello, Paolo Greco speaking.\nCaller: Thank you kindly for the call, the laboratory documents are being forwarded for matching.\n\nPurchase order GDP-7054 from Solstice Dental Supply\n- line 1: suction tips; 24 packs at 7.40 EUR\n- order total: 177.60 EUR\n\nGoods receipt GDR-6824\n- line 1: received 24 packs\n\nInvoice GDV-13708 for purchase order GDP-7054\n- line 1: suction tips; 25 packs at 7.77 EUR\n- invoice total: 194.25 EUR",
  "question": "AP policy of Greenhollow Dental Practice: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is any share smaller than 5 percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nA later check in the check order does not change an action that is already decided.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does the policy tell us to take for invoice GDV-13708?",
  "options": [
   "Release for payment",
   "Hold for receipt",
   "Send to price-variance review"
  ]
 },
 {
  "qid": "q6da2b2d654",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"FSP-5629\",\"vendor\":\"Ironside Hose Company\",\"lines\":[{\"line\":1,\"item\":\"cable glands\",\"quantity\":\"100 packs\",\"unit_price_cents\":614}],\"total_cents\":61400}\n\nGoods receipt (JSON):\n{\"gr_number\":\"FSG-9081\",\"lines\":[{\"line\":1,\"received\":\"98 packs\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"FSV-97228\",\"po_number\":\"FSP-5629\",\"lines\":[{\"line\":1,\"item\":\"cable glands\",\"quantity\":\"98 packs\",\"unit_price_cents\":618}],\"total_cents\":60564}\n\nPaid-invoice register (JSON):\n{\"vendor\":\"Ironside Hose Company\",\"paid_invoice_numbers\":[\"FSV-97228\",\"FSV-97528\",\"FSV-64945\"]}\n\nfrom: Shabnam Rezaei\nto: AP lead, thank you kindly for your help\nteam: the field service team\ndocs: purchase order FSP-5629, supplier invoice FSV-97228 from Ironside Hose Company, pasted below for matching",
  "question": "Is invoice FSV-97228 not released for payment once the AP policy has been applied to it?",
  "definitions": "AP policy of Tidewater Field Services: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Price check | invoiced unit price minus PO unit price is not more than £0.05 on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: duplicate, then price, then quantity.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q84414549fe",
  "kind": "choice",
  "text": "Ngozi Eze, the IT support team sent its purchase documents over, and they are attached for matching.\n\nInvoice OIN-34943 for purchase order OPO-6870\n- line 1: frame cases; 135 units at 9.27 GBP\n- invoice total: 1,251.45 GBP\n\nPaid-invoice register for Halbrook Lens Labs: OIN-24247, OIN-68878, OIN-15620, OIN-33591\n\nPurchase order OPO-6870 from Halbrook Lens Labs\n- line 1: frame cases; 135 units at £9\n- order total: £1,215\n\nGoods receipt OGR-5864\n- line 1: received 134 units",
  "question": "AP policy of Lumenvale Eyecare Group: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Price check: invoiced unit price minus PO unit price is a fraction that remains smaller than 3 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then duplicate, then price.\nWhen a check fails in the check order, the first such failure decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nAs a new clerk on the AP team, which action does the policy give invoice OIN-34943?",
  "options": [
   "Hold for receipt",
   "Send to price-variance review",
   "Reject as a duplicate",
   "Release for payment"
  ]
 },
 {
  "qid": "q340d86550a",
  "kind": "choice",
  "text": "Clerk: This is Ngozi Eze at AP.\nCaller: Got it. The warehouse team purchase is under purchase order OPO-3934.\nClerk: Papers from Corrin Frame Works are coming.\n\nInvoice OIN-56638 for purchase order OPO-3934\n- line 1: repair kits; 20 kits at 7.04 GBP\n- invoice total: 140.80 GBP\n\nPaid-invoice register for Corrin Frame Works: OIN-56637, OIN-71713, OIN-56638, OIN-13277\n\nPurchase order OPO-3934 from Corrin Frame Works\n- line 1: repair kits; 20 kits at 7.00 GBP\n- order total: 140.00 GBP\n\nGoods receipt OGR-5730\n- line 1: received 20 kits",
  "question": "AP policy of Lumenvale Eyecare Group: each invoice gets exactly one action.\n- Approval-limit check: the invoice total is any amount smaller than 1,000.00 GBP (limit of approver Gareth Dunbar). If it fails: route to a senior approver.\n- Price check: invoiced unit price minus PO unit price is a proportion strictly smaller than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price, then approval limit, then duplicate.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nUnder the AP policy, which action fits invoice OIN-56638?",
  "options": [
   "Reject as a duplicate",
   "Release for payment",
   "Send to price-variance review",
   "Hold for receipt",
   "Route to a senior approver"
  ]
 },
 {
  "qid": "q885f804fbe",
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
  "qid": "qdcc3f6832b",
  "kind": "yes/no",
  "text": "Hello,\nThe facilities team purchase is under PO FPO-8903. Supplier invoice FSI-52718 is attached for matching.\nRegards,\nHaruka Sakai\n\nInvoice FSI-52718 for purchase order FPO-8903\n- line 1: mineral blocks; 1 pallet at £92.62\n- line 2: seed potatoes; 2 bags at £38.48\n- invoice total: £169.58\n\nPaid-invoice register for Havenbrook Tractor Parts: FSI-20823, FSI-80869\n\nPurchase order FPO-8903 from Havenbrook Tractor Parts\n- line 1: mineral blocks; 2 pallets at £92.55\n- line 2: seed potatoes; 5 bags at £37.99\n- order total: £375.05\n\nGoods receipt FGR-5735\n- line 1: received 2 pallets\n- line 2: received 5 bags",
  "question": "Does the card clear invoice FSI-52718 for payment?",
  "definitions": "AP policy of Marrowdale Farm Cooperative: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is smaller than £0.50 on every line. If it fails: price-variance review.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: quantity, then price, then duplicate.\nLater checks in the check order do not change the action that the first failing check set.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q7d932deca4",
  "kind": "yes/no",
  "text": "Brief: Tanya Obi, laboratory team, Wexcombe Janitorial Supply, invoice BCV-82664. Attached for matching.\n\nPurchase order BCP-9731 from Wexcombe Janitorial Supply\n- line 1: hand soap; 4 bottles at 5.42 GBP\n- line 2: glass cleaner; 80 bottles at 4.95 GBP\n- order total: 417.68 GBP\n\nGoods receipt BCR-1797\n- line 1: received 3 bottles\n- line 2: received 78 bottles\n\nInvoice BCV-82664 for purchase order BCP-9731\n- line 1: hand soap; 3 bottles at 5.16 GBP\n- line 2: glass cleaner; 78 bottles at 4.78 GBP\n- invoice total: 388.32 GBP\n\nPaid-invoice register for Wexcombe Janitorial Supply: BCV-82464, BCV-36469, BCV-73435, BCV-89304",
  "question": "Under the policy, is invoice BCV-82664 blocked from payment?",
  "definitions": "AP policy of Brightstone Office Care: each invoice gets exactly one action.\n- Approval-limit check: the invoice total is below 388.32 GBP (limit of approver Eleanor Hughes). If it fails: route to a senior approver.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price check: invoiced unit price minus PO unit price is at most 0.10 GBP on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: approval limit, then quantity, then price, then duplicate.\nWork through the check order, and when you find the first failing check, use it to set the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qb64f222b1c",
  "kind": "yes/no",
  "text": "Purchase order (JSON):\n{\"po_number\":\"FSP-5629\",\"vendor\":\"Ironside Hose Company\",\"lines\":[{\"line\":1,\"item\":\"cable glands\",\"quantity\":\"100 packs\",\"unit_price_cents\":614}],\"total_cents\":61400}\n\nGoods receipt (JSON):\n{\"gr_number\":\"FSG-9081\",\"lines\":[{\"line\":1,\"received\":\"98 packs\"}]}\n\nInvoice (JSON):\n{\"invoice_number\":\"FSV-97228\",\"po_number\":\"FSP-5629\",\"lines\":[{\"line\":1,\"item\":\"cable glands\",\"quantity\":\"98 packs\",\"unit_price_cents\":618}],\"total_cents\":60564}\n\nPaid-invoice register (JSON):\n{\"vendor\":\"Ironside Hose Company\",\"paid_invoice_numbers\":[\"FSV-34864\",\"FSV-97528\",\"FSV-64945\"]}\n\nfrom: Shabnam Rezaei\nto: AP lead, thank you kindly for your help\nteam: the field service team\ndocs: purchase order FSP-5629, supplier invoice FSV-97228 from Ironside Hose Company, pasted below for matching",
  "question": "Under the AP policy, does invoice FSV-97228 end up released for payment?",
  "definitions": "AP policy of Tidewater Field Services: each invoice gets exactly one action.\n| check | passes when | if it fails |\n|---|---|---|\n| Duplicate check | the invoice number is not in the paid-invoice register (exact match only) | reject as a duplicate |\n| Price check | invoiced unit price minus PO unit price is not more than £0.05 on every line | price-variance review |\n| Quantity check | invoiced quantity is at most received quantity on every line | hold for receipt |\nCheck order: duplicate, then price, then quantity.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qc90436c580",
  "kind": "yes/no",
  "text": "Hey Connor Mbeki, heads up: the IT support purchase papers are pasted below for matching. Thanks!\n\nPurchase order BMR-2289 from Holcombe Tyre Supply\n- line 1: cleaning rags; 144 bags at 9.96 GBP\n- line 2: spark plugs; 25 boxes at 17.71 GBP\n- order total: 1,876.99 GBP\n\nGoods receipt BGN-4202\n- line 1: received 143 bags\n- line 2: received 25 boxes\n\nInvoice BVI-86837 for purchase order BMR-2289\n- line 1: cleaning rags; 143 bags at 9.96 GBP\n- line 2: spark plugs; 25 boxes at 17.04 GBP\n- invoice total: 1,850.28 GBP\n\nPaid-invoice register for Holcombe Tyre Supply: BVI-35247, BVI-16395, BVI-69899, BVI-29260",
  "question": "Does this policy's outcome for invoice BVI-86837 amount to it being not released for payment?",
  "definitions": "AP policy of Brackley Motor Repairs: each invoice gets exactly one action.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price check: invoiced unit price minus PO unit price is at most 0.25 GBP on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: duplicate, then quantity, then price.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qf77bab0ceb",
  "kind": "yes/no",
  "text": "Clerk: Regarding the warehouse team, this is Kwabena Oppong at AP.\nCaller: Acknowledged.\nClerk: Paperwork from Dornhaus Cooperage is being forwarded.\nCaller: Thanks. Supplier invoice SPV-95827 is the document for matching.\n\nInvoice SPV-95827 for purchase order PRQ-5160\n- line 1: barrel hoops; 60 sets at $30.57\n- invoice total: $1,834.20\n\nPaid-invoice register for Dornhaus Cooperage: SPV-93187, SPV-36552\n\nPurchase order PRQ-5160 from Dornhaus Cooperage\n- line 1: barrel hoops; 60 sets at $31.00\n- order total: $1,860.00\n\nGoods receipt GRZ-2479\n- line 1: received 60 sets",
  "question": "Is the claim that invoice SPV-95827 is not released for payment, under the AP policy, not true?",
  "definitions": "Ambersett Wine Cellars AP policy: each invoice gets exactly one action.\n- Approval limit: invoice total is at or below $1,834.20 (limit of approver Anaya Iyer). If it fails: route to a senior approver.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price: invoiced unit price minus PO unit price is $1.00 or less on every line. If it fails: price-variance review.\nCheck order: price, then approval limit, then duplicate, then quantity.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 }
]
