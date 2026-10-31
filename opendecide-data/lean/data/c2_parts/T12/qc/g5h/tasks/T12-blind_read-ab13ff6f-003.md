# G5-H blind read (all free-form rows) T12-blind_read-ab13ff6f-003 (family T12)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/Users/aryamahadik/Documents/jev/opendecide-data/lean/data/c2_parts/T12/qc/g5h/answers/T12-blind_read-ab13ff6f-003.json

This task file is the only file you may open. Do not open, list or search any other file or folder, do not run shell commands and do not use the web.

Items: 34. Answers expected: 34 (one per item, each with that item's qid).

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
  "qid": "q729e36a004",
  "kind": "choice",
  "text": "Raised by: AP intern to Felix Oyelaran\nTeam: facilities\nSubject: PO and goods receipt attached for matching\n\nPurchase order RLP-7230 from Brackenridge Rubber Goods\n- line 1: bicycle chains; 6 units at 33.80 USD\n- line 2: inner tubes; 114 units at 3.00 USD\n- order total: 544.80 USD\n\nGoods receipt RLR-7120\n- line 1: received 4 units\n- line 2: received 111 units\n\nInvoice RLI-10828 for purchase order RLP-7230\n- line 1: bicycle chains; 4 units at 33.80 USD\n- line 2: inner tubes; 112 units at 3.00 USD\n- invoice total: 471.20 USD",
  "question": "AP policy of Ridgeline Cycle Works: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Approval-limit check: the invoice total is less than 483.74 USD (limit of approver Tobias Reinholt). If it fails: route to a senior approver.\n3. Price check: invoiced unit price minus PO unit price is a proportion that equals or is lower than 5 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then approval limit, then price.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhich action does the policy tell us to take for invoice RLI-10828?",
  "options": [
   "Hold for receipt",
   "Release for payment",
   "Send to price-variance review",
   "Route to a senior approver"
  ]
 },
 {
  "qid": "qd644d755af",
  "kind": "yes/no",
  "text": "Clerk: Kwabena Oppong speaking.\nCaller: Thank you kindly for the call. This is for the IT support team, and the paperwork is pasted below for matching.\n\nInvoice SPV-66901 for purchase order PRQ-1979\n- line 1: wine bottles; sixteen cases at 43.11 USD\n- line 2: oak barrels; 159 units at 782.48 USD\n- invoice total: 125,104.08 USD\n\nPurchase order PRQ-1979 from Marrow Cork Supply\n- line 1: wine bottles; sixteen cases at 43.11 USD\n- line 2: oak barrels; 159 units at 782.48 USD\n- order total: 125,104.08 USD\n\nGoods receipt GRZ-3169\n- line 1: received sixteen cases\n- line 2: received 158 units",
  "question": "So does invoice SPV-66901 fail the price check when you look at that check on its own?",
  "definitions": "AP policy of Ambersett Wine Cellars: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is at most 0.50 USD on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Approval-limit check: the invoice total is beneath 127,788.46 USD (limit of approver Dmitri Volkov). If it fails: route to a senior approver.\nCheck order: quantity, then approval limit, then price.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qb42e4bc14c",
  "kind": "yes/no",
  "text": "To: Priyanka Desai\nFrom: procurement office\nRe: IT support purchase, documents forwarded for matching\n\nPurchase order PCL-7966 from Ferrante Reagent Company\n- line 1: sample tubes; 93 tubes at 5.00 USD\n- order total: 465.00 USD\n\nGoods receipt RCL-2676\n- line 1: received 91 tubes\n\nInvoice ICL-98341 for purchase order PCL-7966\n- line 1: sample tubes; 91 tubes at 5.24 USD\n- invoice total: 476.84 USD",
  "question": "Would you say invoice ICL-98341 fails the price check, looking only at that check?",
  "definitions": "AP policy of Calloway Research Laboratory: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is a share that is less than 3 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then price.\nWhichever failing check comes first in the check order decides the action, and later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q2081549fe3",
  "kind": "yes/no",
  "text": "Caller: Hello, this is the supplier's billing contact.\nClerk: Hello, this is Lenka Svoboda.\nCaller: Thank you, the documents for the laboratory team are being sent over.\n\nInvoice BIN-39975 for purchase order ARQ-6385\n- line 1: oak planks; 4 units at €92.92\n- line 2: scale models; 32 kits at €116.24\n- invoice total: €4,091.36\n\nPaid-invoice register for Brackenmoor Glazing: BIN-82904, BIN-27458, BIN-88820, BIN-52116\n\nPurchase order ARQ-6385 from Brackenmoor Glazing\n- line 1: oak planks; 5 units at €90.93\n- line 2: scale models; 36 kits at €114.24\n- order total: €4,567.29\n\nGoods receipt RCP-5097\n- line 1: received 4 units\n- line 2: received 33 kits",
  "question": "Would you say invoice BIN-39975 passes the price check when that check is looked at on its own?",
  "definitions": "Quellon Architects AP policy: each invoice gets exactly one action.\n1. Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n2. Duplicate: invoice number not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Price: invoiced unit price minus PO unit price is smaller than €2.00 on every line. If it fails: price-variance review.\nCheck order: quantity, then duplicate, then price.\nFollow the check order and halt at the first check that fails, because later checks do not change the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q748da17ef6",
  "kind": "choice",
  "text": "Clerk: Thandiwe Mokoena here, go ahead.\nCaller: Thank you kindly. The warehouse purchase documents are pasted below for matching.\n\nPurchase order NHM-3960 from Tessaly Preservation Works\n- line 1: storage drawers; 25 units at 59.95 EUR\n- order total: 1,498.75 EUR\n\nGoods receipt GRN-5929\n- line 1: received 22 units\n\nInvoice SUP-11937 for purchase order NHM-3960\n- line 1: storage drawers; 25 units at 60.45 EUR\n- invoice total: 1,511.25 EUR",
  "question": "AP policy of Northgate Natural History Museum: each invoice gets exactly one action.\n1. Approval-limit check: the invoice total is lower than 1,511.25 EUR (limit of approver Emil Strand). If it fails: route to a senior approver.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n3. Price check: invoiced unit price minus PO unit price is any amount smaller than 0.50 EUR on every line. If it fails: price-variance review.\nCheck order: approval limit, then quantity, then price.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nGoing by the way the AP policy treats invoice SUP-11937, what line, if any, fails the price check?",
  "options": [
   "storage drawers",
   "None of the lines"
  ]
 },
 {
  "qid": "qa8d23913de",
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
  "qid": "q462b0ea6fe",
  "kind": "yes/no",
  "text": "Message to Priya Raman from team lead: the marketing set is pasted below for matching.\n\nPurchase order BMR-6493 from Carrow Lubricant Group\n- line 1: cleaning rags; 12 bags at £10.82\n- order total: £129.84\n\nGoods receipt BGN-1816\n- line 1: received 12 bags\n\nInvoice BVI-40351 for purchase order BMR-6493\n- line 1: cleaning rags; 15 bags at £10.96\n- invoice total: £164.40",
  "question": "Put plainly, will invoice BVI-40351 end up not released for payment?",
  "definitions": "AP policy of Brackley Motor Repairs: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is lower than £0.25 on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe earliest failing check in the check order settles the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q5021a86285",
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
  "qid": "q0f816a4e4e",
  "kind": "yes/no",
  "text": "Raised by: procurement officer\nTo: Yusuf Demir\nTeam: field service\nSubject: purchase order, goods receipt and supplier invoice attached\n\nPurchase order GCP-9163 | vendor Fernbank Growers Union\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | bagged compost | five bags | £6.03 |\n| 2 | garden twine | fifteen rolls | £4.91 |\n| 3 | potting mix | 183 bags | £3.15 |\n| 4 | seed packets | two packs | £3.68 |\n| total | | | £687.61 |\n\nGoods receipt GCR-4536\n| line | received |\n|---|---|\n| 1 | five bags |\n| 2 | fifteen rolls |\n| 3 | 183 bags |\n| 4 | two packs |\n\nInvoice GCS-85340 | purchase order GCP-9163\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | bagged compost | five bags | £6.03 |\n| 2 | garden twine | fifteen rolls | £4.91 |\n| 3 | potting mix | 183 bags | £3.15 |\n| 4 | seed packets | two packs | £3.68 |\n| total | | | £687.61 |",
  "question": "Seen by a new clerk, does the AP policy block payment of invoice GCS-85340?",
  "definitions": "Hawthorn Yard Garden Centre AP policy: each invoice gets exactly one action.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Price: invoiced unit price minus PO unit price is less than £0.05 on every line. If it fails: price-variance review.\nCheck order: price, then quantity.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q319bfd4d0c",
  "kind": "choice",
  "text": "To: Hamish Crawford\nFrom: office manager\nRe: IT support purchase, documents attached\n\nPurchase order GCP-8758 | vendor Fernbank Growers Union\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | potting mix | 4 bags | £5.41 |\n| 2 | terracotta pots | 12 units | £7.23 |\n| total | | | £108.40 |\n\nGoods receipt GCR-6339\n| line | received |\n|---|---|\n| 1 | 2 bags |\n| 2 | 11 units |\n\nInvoice GCS-84189 | purchase order GCP-8758\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | potting mix | 2 bags | £5.56 |\n| 2 | terracotta pots | 11 units | £7.37 |\n| total | | | £92.19 |\n\nPaid-invoice register | vendor Fernbank Growers Union\n| invoice number |\n|---|\n| GCS-18518 |\n| GCS-66615 |\n| GCS-84129 |\n| GCS-12812 |",
  "question": "AP policy of Hawthorn Yard Garden Centre: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is lower than £0.15 on every line. If it fails: price-variance review.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: quantity, then price, then duplicate.\nApply the check order in sequence, and let the first check that fails determine the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nWhat does the policy say to do with invoice GCS-84189?",
  "options": [
   "Reject as a duplicate",
   "Send to price-variance review",
   "Hold for receipt",
   "Release for payment"
  ]
 },
 {
  "qid": "q577cb70cea",
  "kind": "yes/no",
  "text": "For file, from Oskar Lindahl: the warehouse purchase documents are attached below for matching.\n\nPurchase order PCL-1301 from Ferrante Reagent Company\n- line 1: reagent kits; 100 kits at $149.00\n- line 2: sample tubes; 81 tubes at $8.00\n- order total: $15,548.00\n\nGoods receipt RCL-1534\n- line 1: received 98 kits\n- line 2: received 81 tubes\n\nInvoice ICL-59016 for purchase order PCL-1301\n- line 1: reagent kits; 98 kits at $152.43\n- line 2: sample tubes; 81 tubes at $8.37\n- invoice total: $15,616.11",
  "question": "Does invoice ICL-59016 end in a hold, a review, a rejection, or a routing to a senior approver?",
  "definitions": "AP policy of Calloway Research Laboratory: each invoice gets exactly one action.\n1. Approval-limit check: the invoice total is beneath $5,000.00 (limit of approver Ebru Kaya). If it fails: route to a senior approver.\n2. Price check: invoiced unit price minus PO unit price is a share equal to or smaller than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: approval limit, then price, then quantity.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q15647719b2",
  "kind": "yes/no",
  "text": "Message to Wen Zhao from team lead: the field service set is pasted below for matching.\n\nInvoice BIN-53308 for purchase order ARQ-4924\n- line 1: concrete mix; 200 bags at €10.89\n- line 2: plotter ink; 180 bottles at €30\n- invoice total: €7,578\n\nPaid-invoice register for Stonecradle Quarries: BIN-49945, BIN-89404, BIN-72054\n\nPurchase order ARQ-4924 from Stonecradle Quarries\n- line 1: concrete mix; 200 bags at €10.71\n- line 2: plotter ink; 180 bottles at €30.20\n- order total: €7,578\n\nGoods receipt RCP-7740\n- line 1: received 199 bags\n- line 2: received 179 bottles",
  "question": "Is it true, as a new clerk, that invoice BIN-53308 fails the price check taken by itself?",
  "definitions": "AP policy of Quellon Architects: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is lower than €0.15 on every line. If it fails: price-variance review.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n4. Approval-limit check: the invoice total is strictly lower than €2,000 (limit of approver Yannick Girard). If it fails: route to a senior approver.\nCheck order: quantity, then price, then duplicate, then approval limit.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q2babaee381",
  "kind": "yes/no",
  "text": "Dear Shauna Rennie, kindly note that the laboratory purchase papers are pasted below for matching, and we are grateful for your time and attention.\n\nPurchase order BCP-6794 from Gilmour Mop Company\n- line 1: bin liners; 36 rolls at £9.69\n- line 2: glass cleaner; 34 bottles at £7.07\n- order total: £589.22\n\nGoods receipt BCR-6928\n- line 1: received 36 rolls\n- line 2: received 34 bottles\n\nInvoice BCV-18435 for purchase order BCP-6794\n- line 1: bin liners; 36 rolls at £9.93\n- line 2: glass cleaner; 34 bottles at £6.53\n- invoice total: £579.50",
  "question": "Under the AP policy, is payment of invoice BCV-18435 blocked?",
  "definitions": "AP policy of Brightstone Office Care: each invoice gets exactly one action.\n- Approval-limit check: the invoice total is below £1,000.00 (limit of approver Eleanor Hughes). If it fails: route to a senior approver.\n- Price check: invoiced unit price minus PO unit price is strictly beneath £0.25 on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: approval limit, then quantity, then price.\nOnce a check fails in the check order, later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qdfa4d91265",
  "kind": "yes/no",
  "text": "Sophie Bramble: Hi facilities team, the documents for your purchase are pasted below for matching.\n\nInvoice SPV-95759 for purchase order PRQ-3972\n- line 1: fining agent; 4 packs at $14.29\n- invoice total: $57.16\n\nPaid-invoice register for Marrow Cork Supply: SPV-95759, SPV-75759\n\nPurchase order PRQ-3972 from Marrow Cork Supply\n- line 1: fining agent; 5 packs at $13.79\n- order total: $68.95\n\nGoods receipt GRZ-9702\n- line 1: received 4 packs",
  "question": "As a new clerk in AP, is invoice SPV-95759 allowed through to payment under the policy?",
  "definitions": "AP policy of Ambersett Wine Cellars: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is equal to or less than $0.50 on every line. If it fails: price-variance review.\n2. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then duplicate, then quantity.\nEvery check that comes after the failing one in the check order does not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qad8e4c5596",
  "kind": "yes/no",
  "text": "Hello Kiyoshi Mori,\nBelow this line are the laboratory papers, ready for matching.\nCheers,\nAP intern\n\nInvoice OIN-58997 for purchase order OPO-3396\n- line 1: lens blanks; 180 boxes at 58.06 GBP\n- line 2: display stands; 30 units at 30.64 GBP\n- line 3: saline; 15 bottles at £2\n- invoice total: £11,400\n\nPurchase order OPO-3396 from Halbrook Lens Labs\n- line 1: lens blanks; 180 boxes at £58\n- line 2: display stands; 30 units at £31\n- line 3: saline; 15 bottles at £2\n- order total: £11,400\n\nGoods receipt OGR-3690\n- line 1: received 180 boxes\n- line 2: received 30 units\n- line 3: received 15 bottles",
  "question": "Would you say invoice OIN-58997 fails the price check, looking only at that check?",
  "definitions": "AP policy of Lumenvale Eyecare Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a fraction that is smaller than 1 percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nWhen a check fails in the check order, the first such failure decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q3b0a82e083",
  "kind": "choice",
  "text": "To file,\nThe marketing documents are attached for matching.\nRhys Pritchard\n\nInvoice OIN-72703 for purchase order OPO-7211\n- line 1: cleaning cloths; two packs at £4.96\n- line 2: saline; 80 bottles at £2.75\n- invoice total: £229.92\n\nPurchase order OPO-7211 from Corrin Frame Works\n- line 1: cleaning cloths; two packs at £5.00\n- line 2: saline; 80 bottles at £2.80\n- order total: £234.00\n\nGoods receipt OGR-7594\n- line 1: received two packs\n- line 2: received 80 bottles",
  "question": "AP policy of Lumenvale Eyecare Group: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a proportion that is less than five percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nWhichever failing check comes first in the check order decides the action, and later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nGiven the outcome this policy gives invoice OIN-72703, which line, if any, fails the price check?",
  "options": [
   "None of the lines",
   "saline",
   "cleaning cloths"
  ]
 },
 {
  "qid": "q24ecd40a1c",
  "kind": "yes/no",
  "text": "Dear IT support team, please find the purchase documents attached for matching.\nYours faithfully,\nDeclan Murphy\n\nPurchase order WPO-7174 | vendor Caldwell Hardware Trade\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | sanding discs | 200 packs | 18.00 EUR |\n| total | | | 3,600.00 EUR |\n\nGoods receipt WGR-4109\n| line | received |\n|---|---|\n| 1 | 197 packs |\n\nInvoice WSI-97291 | purchase order WPO-7174\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | sanding discs | 198 packs | 18.90 EUR |\n| total | | | 3,742.20 EUR |",
  "question": "Just starting out in AP, would invoice WSI-97291 fail the price check when that check is judged on its own?",
  "definitions": "AP policy of Oakhaven Joinery Workshop: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a proportion strictly smaller than five percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nWhichever failing check comes first in the check order decides the action, and later checks do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q7fa5333a13",
  "kind": "yes/no",
  "text": "For Pilar Navarro, from the office: the field service purchase documents are forwarded for matching.\n\nPurchase order WPO-6179 | vendor Feldmark Upholstery Textiles\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | oak planks | twenty units | €47.00 |\n| total | | | €940.00 |\n\nGoods receipt WGR-5961\n| line | received |\n|---|---|\n| 1 | twenty units |\n\nInvoice WSI-31037 | purchase order WPO-6179\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | oak planks | twenty units | €47.46 |\n| total | | | €949.20 |",
  "question": "Is it right to say that, under this policy, invoice WSI-31037 passes the price check taken on its own?",
  "definitions": "AP policy of Oakhaven Joinery Workshop: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a portion lower than one percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qfdb2ba5e62",
  "kind": "yes/no",
  "text": "Yara Nassar: marketing papers forwarded below, lined up for matching. Enjoy the rest of your work!\n\nInvoice SUB-29026 for purchase order EQP-2379\n- line 1: yoga mats; 78 units at $40.78\n- line 2: cleaning spray; 92 bottles at $4.42\n- line 3: whey powder; 59 bags at $136.69\n- invoice total: $11,652.19\n\nPaid-invoice register for Redmere Protein Supply: SUB-59269, SUB-79385, SUB-46893\n\nPurchase order EQP-2379 from Redmere Protein Supply\n- line 1: yoga mats; 80 units at $41.86\n- line 2: cleaning spray; 93 bottles at $4.21\n- line 3: whey powder; 59 bags at $136.65\n- order total: $11,802.68\n\nGoods receipt RCD-9159\n- line 1: received 78 units\n- line 2: received 92 bottles\n- line 3: received 59 bags",
  "question": "Sorry to ask as a new starter, but when the price check is looked at on its own, does invoice SUB-29026 fail it?",
  "definitions": "AP policy of Brickhollow Fitness Group: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is equal to or below $0.05 on every line. If it fails: price-variance review.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n4. Approval-limit check: the invoice total is beneath $9,925.39 (limit of approver Esme Walsh). If it fails: route to a senior approver.\nCheck order: quantity, then price, then duplicate, then approval limit.\nThe check order decides which failure counts, because the first failure met in that order decides the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q6bee464601",
  "kind": "yes/no",
  "text": "For file, from Oskar Lindahl: the warehouse purchase documents are attached below for matching.\n\nPurchase order PCL-1301 from Ferrante Reagent Company\n- line 1: reagent kits; 100 kits at $149.00\n- line 2: sample tubes; 81 tubes at $8.00\n- order total: $15,548.00\n\nGoods receipt RCL-1534\n- line 1: received 98 kits\n- line 2: received 81 tubes\n\nInvoice ICL-59016 for purchase order PCL-1301\n- line 1: reagent kits; 98 kits at $152.43\n- line 2: sample tubes; 81 tubes at $8.37\n- invoice total: $15,616.11",
  "question": "Under the AP policy, does invoice ICL-59016 end up released for payment?",
  "definitions": "AP policy of Calloway Research Laboratory: each invoice gets exactly one action.\n1. Approval-limit check: the invoice total is beneath $5,000.00 (limit of approver Ebru Kaya). If it fails: route to a senior approver.\n2. Price check: invoiced unit price minus PO unit price is a share equal to or smaller than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n3. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: approval limit, then price, then quantity.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q6df4de70ed",
  "kind": "yes/no",
  "text": "Dear Sunniva Haugland, it is my pleasure to forward the laboratory documents for matching.\nYours sincerely,\nTeam lead\n\nPurchase order EPU-3911 from Ordenbrook Medical Supplies\n- line 1: surgical gloves; 12 boxes at 15.00 EUR\n- line 2: bandage rolls; 24 rolls at 7.00 EUR\n- order total: 348.00 EUR\n\nGoods receipt EGN-3464\n- line 1: received 12 boxes\n- line 2: received 24 rolls\n\nInvoice EVR-91520 for purchase order EPU-3911\n- line 1: surgical gloves; 12 boxes at 15.35 EUR\n- line 2: bandage rolls; 24 rolls at 7.29 EUR\n- invoice total: 359.16 EUR",
  "question": "Does the AP policy send invoice EVR-91520 to price-variance review, with that being the sole action the invoice gets?",
  "definitions": "Eastbridge Community Clinic AP policy: each invoice gets exactly one action.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Approval limit: invoice total is not more than 500.00 EUR (limit of approver Matteo Serrano). If it fails: route to a senior approver.\n- Price: invoiced unit price minus PO unit price is a proportion that equals or is lower than 3 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: quantity, then approval limit, then price.\nWalk through the check order in turn, and let the first failure you meet set the action; later checks do not change it.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qdcb6ed4c6a",
  "kind": "yes/no",
  "text": "From: Mateo Giordano\nRe: IT support purchase, documents forwarded for matching\n\nPurchase order TPO-8289 | vendor Morrow Kitchen Equipment\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | fresh herbs | 60 bags | 5.40 EUR |\n| total | | | 324.00 EUR |\n\nGoods receipt TGR-6134\n| line | received |\n|---|---|\n| 1 | 60 bags |\n\nInvoice TIN-10569 | purchase order TPO-8289\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | fresh herbs | 62 bags | 5.67 EUR |\n| total | | | 351.54 EUR |",
  "question": "Being new to AP, does the card say payment of invoice TIN-10569 is stopped?",
  "definitions": "AP policy of Saffron Table Catering: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a portion smaller than or the same as 5 percent of the PO unit price on every line. If it fails: price-variance review.\n- Approval-limit check: the invoice total is less than 250.00 EUR (limit of approver Ruben Calderon). If it fails: route to a senior approver.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price, then approval limit.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q3eaf0bb5d8",
  "kind": "yes/no",
  "text": "To: Teresa Llorente\nFrom: receiving-dock worker\nRe: marketing purchase, documents attached for matching\n\nPurchase order EPU-4000 from Ordenbrook Medical Supplies\n- line 1: hand sanitiser; 75 bottles at 9.00 EUR\n- line 2: bandage rolls; six rolls at 6.00 EUR\n- order total: 711.00 EUR\n\nGoods receipt EGN-8992\n- line 1: received 72 bottles\n- line 2: received six rolls\n\nInvoice EVR-51841 for purchase order EPU-4000\n- line 1: hand sanitiser; 75 bottles at 9.26 EUR\n- line 2: bandage rolls; six rolls at 6.17 EUR\n- invoice total: 731.52 EUR",
  "question": "Just the price check on its own, then: does invoice EVR-51841 fail it?",
  "definitions": "AP policy of Eastbridge Community Clinic: each invoice gets exactly one action.\n- Approval-limit check: the invoice total is no more than 731.52 EUR (limit of approver Matteo Serrano). If it fails: route to a senior approver.\n- Price check: invoiced unit price minus PO unit price is a portion that stays below three percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: approval limit, then quantity, then price.\nThe action is fixed by the first failing check in the check order, and a later check does not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q2b758bed95",
  "kind": "yes/no",
  "text": "Hello,\nFor the field service purchase, the papers are pasted below for matching.\nRegards,\nTanya Obi\n\nPurchase order BCP-8784 from Wexcombe Janitorial Supply\n- line 1: hand soap; five bottles at 2.86 GBP\n- line 2: glass cleaner; ten bottles at 8.11 GBP\n- order total: 95.40 GBP\n\nGoods receipt BCR-4678\n- line 1: received three bottles\n- line 2: received eight bottles\n\nInvoice BCV-39043 for purchase order BCP-8784\n- line 1: hand soap; five bottles at 2.86 GBP\n- line 2: glass cleaner; eight bottles at 8.15 GBP\n- invoice total: 79.50 GBP",
  "question": "Does the policy decide that invoice BCV-39043 is released for payment?",
  "definitions": "AP policy of Brightstone Office Care: each invoice gets exactly one action.\n- Approval-limit check: the invoice total is falling short of 1,000.00 GBP (limit of approver Eleanor Hughes). If it fails: route to a senior approver.\n- Price check: invoiced unit price minus PO unit price is lower than 0.10 GBP on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: approval limit, then quantity, then price.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qdcc2038225",
  "kind": "yes/no",
  "text": "Tanya Obi, the warehouse documents are pasted below for matching, with thanks. Kind regards from the receiving-dock worker.\n\nPurchase order BCP-5981 from Harrowdene Chemicals\n- line 1: mop heads; 130 units at £8.75\n- order total: £1,137.50\n\nGoods receipt BCR-3057\n- line 1: received 129 units\n\nInvoice BCV-57546 for purchase order BCP-5981\n- line 1: mop heads; 127 units at £8.75\n- invoice total: £1,111.25",
  "question": "As a new clerk in AP, is invoice BCV-57546 allowed through to payment under the policy?",
  "definitions": "AP policy of Brightstone Office Care: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is at or below £0.20 on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe outcome stays where the first failure put it, because later checks in the check order do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: GBP, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q8497e380e0",
  "kind": "yes/no",
  "text": "For Pilar Navarro, from the office: the field service purchase documents are forwarded for matching.\n\nPurchase order WPO-6179 | vendor Feldmark Upholstery Textiles\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | oak planks | twenty units | €47.00 |\n| total | | | €940.00 |\n\nGoods receipt WGR-5961\n| line | received |\n|---|---|\n| 1 | twenty units |\n\nInvoice WSI-31037 | purchase order WPO-6179\n| line | item | quantity | unit price |\n|---|---|---|---|\n| 1 | oak planks | twenty units | €47.47 |\n| total | | | €949.40 |",
  "question": "Just starting out in AP, would invoice WSI-31037 fail the price check when that check is judged on its own?",
  "definitions": "AP policy of Oakhaven Joinery Workshop: each invoice gets exactly one action.\n1. Price check: invoiced unit price minus PO unit price is a portion lower than one percent of the PO unit price on every line. If it fails: price-variance review.\n2. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q211bbbff06",
  "kind": "choice",
  "text": "To: Priyanka Desai\nFrom: supplier billing contact\nRe: warehouse purchase, documents pasted below for matching\n\nPurchase order PCL-7238 from Obsidian Lab Instruments\n- line 1: petri dishes; 15 packs at $13\n- line 2: glass slides; 50 boxes at $12\n- line 3: reagent kits; 135 kits at $109\n- order total: $15,510\n\nGoods receipt RCL-4583\n- line 1: received 14 packs\n- line 2: received 50 boxes\n- line 3: received 135 kits\n\nInvoice ICL-54699 for purchase order PCL-7238\n- line 1: petri dishes; 15 packs at $13\n- line 2: glass slides; 50 boxes at $12\n- line 3: reagent kits; 135 kits at $109\n- invoice total: $15,510",
  "question": "Calloway Research Laboratory AP policy: each invoice gets exactly one action.\n- Approval limit: invoice total is falling short of $50,000 (limit of approver Marcus Whitfield). If it fails: route to a senior approver.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\n- Price: invoiced unit price minus PO unit price is a proportion strictly smaller than 3 percent of the PO unit price on every line. If it fails: price-variance review.\nCheck order: approval limit, then quantity, then price.\nGo through the check order one check at a time, and let the first failing check set the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nIs the action for invoice ICL-54699 set out in the policy, and what is it?",
  "options": [
   "Send to price-variance review",
   "Route to a senior approver",
   "Release for payment",
   "Hold for receipt"
  ]
 },
 {
  "qid": "qfb7cc23eab",
  "kind": "yes/no",
  "text": "Kwabena Oppong: marketing papers attached for matching. From team lead.\n\nInvoice SPV-16349 for purchase order PRQ-7867\n- line 1: barrel hoops; four sets at $17.28\n- invoice total: $69.12\n\nPurchase order PRQ-7867 from Velden Glass Co\n- line 1: barrel hoops; five sets at $16.77\n- order total: $83.85\n\nGoods receipt GRZ-4176\n- line 1: received four sets",
  "question": "Being new to AP, does the card say payment of invoice SPV-16349 is stopped?",
  "definitions": "AP policy of Ambersett Wine Cellars: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is equal to or less than $0.50 on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price.\nThe action is fixed by the first failing check in the check order, and a later check does not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qc7770b06f2",
  "kind": "yes/no",
  "text": "Message to Wen Zhao from team lead: the field service set is pasted below for matching.\n\nInvoice BIN-53308 for purchase order ARQ-4924\n- line 1: concrete mix; 200 bags at €10.85\n- line 2: plotter ink; 180 bottles at €30\n- invoice total: €7,570\n\nPaid-invoice register for Stonecradle Quarries: BIN-49945, BIN-89404, BIN-72054\n\nPurchase order ARQ-4924 from Stonecradle Quarries\n- line 1: concrete mix; 200 bags at €10.71\n- line 2: plotter ink; 180 bottles at €30.20\n- order total: €7,578\n\nGoods receipt RCP-7740\n- line 1: received 199 bags\n- line 2: received 179 bottles",
  "question": "Is it true, as a new clerk, that invoice BIN-53308 fails the price check taken by itself?",
  "definitions": "AP policy of Quellon Architects: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is lower than €0.15 on every line. If it fails: price-variance review.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n4. Approval-limit check: the invoice total is strictly lower than €2,000 (limit of approver Yannick Girard). If it fails: route to a senior approver.\nCheck order: quantity, then price, then duplicate, then approval limit.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "q1de837244c",
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
  "qid": "q872c65c073",
  "kind": "yes/no",
  "text": "Dear Yvette Dubois,\nThe field service purchase documents are attached for matching.\nThanks,\nOffice manager\n\nInvoice SIG-23516 for purchase order ORQ-7095\n- line 1: fader caps; 121 packs at 5.00 USD\n- line 2: audio valves; 10 units at 139.00 USD\n- line 3: broadcast tape; 96 rolls at 9.00 USD\n- invoice total: 2,859.00 USD\n\nPaid-invoice register for Merrin Studio Acoustics: SIG-28516, SIG-25534\n\nPurchase order ORQ-7095 from Merrin Studio Acoustics\n- line 1: fader caps; 121 packs at 5.00 USD\n- line 2: audio valves; 10 units at 139.00 USD\n- line 3: broadcast tape; 96 rolls at 9.00 USD\n- order total: 2,859.00 USD\n\nGoods receipt GRT-2796\n- line 1: received 121 packs\n- line 2: received 10 units\n- line 3: received 96 rolls",
  "question": "Would price-variance review be the only step the card takes on invoice SIG-23516?",
  "definitions": "AP policy of Wrenfield Community Radio: each invoice gets exactly one action.\n- Price check: invoiced unit price minus PO unit price is a fraction strictly below 1 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\nCheck order: quantity, then price, then duplicate.\nThe action stands once it is set, because checks that come later in the check order do not change it.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qb9e934711a",
  "kind": "choice",
  "text": "Dear Yara Benitez,\nThank you for taking this on. The marketing documents are attached below for matching.\nKind regards,\nOffice manager\n\nPurchase order RLP-9448 from Velloway Gear Systems\n- line 1: handlebar grips; 72 sets at $12.00\n- line 2: grease; 84 tubes at $5.00\n- line 3: spoke nipples; 8 packs at $6.00\n- order total: $1,332.00\n\nGoods receipt RLR-6095\n- line 1: received 71 sets\n- line 2: received 84 tubes\n- line 3: received 5 packs\n\nInvoice RLI-67903 for purchase order RLP-9448\n- line 1: handlebar grips; 72 sets at $12.42\n- line 2: grease; 84 tubes at $4.64\n- line 3: spoke nipples; 8 packs at $6.00\n- invoice total: $1,332.00",
  "question": "Ridgeline Cycle Works AP policy: each invoice gets exactly one action.\n- Price: invoiced unit price minus PO unit price is a proportion that is less than 3 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity: invoiced quantity at most received quantity on every line. If it fails: hold for receipt.\nCheck order: price, then quantity.\nThe check order sets the sequence, and the first failing check in that sequence determines the action.\nIf every check passes: release for payment, the only paying action. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete.\n\nLooking at the unit prices on invoice RLI-67903, which line, if any, fails the price check?",
  "options": [
   "grease",
   "spoke nipples",
   "None of the lines",
   "handlebar grips"
  ]
 },
 {
  "qid": "qa51a0c4091",
  "kind": "yes/no",
  "text": "Message to Wen Zhao from team lead: the field service set is pasted below for matching.\n\nInvoice BIN-53308 for purchase order ARQ-4924\n- line 1: concrete mix; 200 bags at €10.89\n- line 2: plotter ink; 180 bottles at €30\n- invoice total: €7,578\n\nPaid-invoice register for Stonecradle Quarries: BIN-49945, BIN-89404, BIN-72054\n\nPurchase order ARQ-4924 from Stonecradle Quarries\n- line 1: concrete mix; 200 bags at €10.71\n- line 2: plotter ink; 180 bottles at €30.20\n- order total: €7,578\n\nGoods receipt RCP-7740\n- line 1: received 199 bags\n- line 2: received 179 bottles",
  "question": "Would this policy count invoice BIN-53308 as a pass on the price check looked at by itself?",
  "definitions": "AP policy of Quellon Architects: each invoice gets exactly one action.\n1. Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\n2. Price check: invoiced unit price minus PO unit price is lower than €0.15 on every line. If it fails: price-variance review.\n3. Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n4. Approval-limit check: the invoice total is strictly lower than €2,000 (limit of approver Yannick Girard). If it fails: route to a senior approver.\nCheck order: quantity, then price, then duplicate, then approval limit.\nReading the check order ends at the first failure, so later checks do not change the action.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: EUR, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 },
 {
  "qid": "qb46e232ec1",
  "kind": "yes/no",
  "text": "Raised by: procurement officer\nTo: Priyanka Desai\nTeam: warehouse\nSubject: purchase order, goods receipt and supplier invoice attached\n\nPurchase order PCL-3017 from Ferrante Reagent Company\n- line 1: pipette tips; 4 boxes at $22.40\n- line 2: lab coats; 73 units at $66.80\n- order total: $4,966\n\nGoods receipt RCL-6070\n- line 1: received 3 boxes\n- line 2: received 73 units\n\nInvoice ICL-97972 for purchase order PCL-3017\n- line 1: pipette tips; 3 boxes at $22.93\n- line 2: lab coats; 73 units at $69.49\n- invoice total: $5,141.56\n\nPaid-invoice register for Ferrante Reagent Company: ICL-97972, ICL-29781, ICL-97952",
  "question": "Would this policy let invoice ICL-97972 be paid?",
  "definitions": "AP policy of Calloway Research Laboratory: each invoice gets exactly one action.\n- Duplicate check: the invoice number is not in the paid-invoice register (exact match only). If it fails: reject as a duplicate.\n- Price check: invoiced unit price minus PO unit price is a share that is less than 5 percent of the PO unit price on every line. If it fails: price-variance review.\n- Quantity check: invoiced quantity is at most received quantity on every line. If it fails: hold for receipt.\nCheck order: quantity, then price, then duplicate.\nFind the first failing check in the check order and let it set the action for the whole card.\nIf every check passes: release for payment, the only action that pays. Lower invoiced prices always pass.\nAmounts: USD, whole cents.\nNothing else applies: the policy and the documents shown are complete."
 }
]
