# G5-H blind read T46-blind_read-9ed82ffe-005 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r6a/T46/qc/g5h/answers/T46-blind_read-9ed82ffe-005.json

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
  "qid": "q255e577131",
  "kind": "yes/no",
  "text": "---\n# request record\nrecord:\n    invoice_id: \"INV-7597\"\n    vendor: \"Harbor Labs\"\nnumbers:\n    amount: 6165.30\n    amount_approval_threshold: 5000.00\nflags:\n    duplicate_of_paid_invoice: false\n    payment_requested_during_business_hours: false\n    vendor_tax_form_missing: false\n    awaiting_purchase_order: false\n    vendor_free_of_sanctions: true",
  "question": "Proposed action: escalate\nLooking at what the record says, is the proposed action a good fit for the request?",
  "definitions": "Meanings:\n- reject: halt this item because the rules forbid it\n- escalate: forward the case to the designated decision maker\n- pay: run the requested step through\n- hold: be held back until a check or document arrives\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q85cb375825",
  "kind": "yes/no",
  "text": "invoice_id: INV-5517\nvendor: Pinecrest Foods\nvendor_tax_form_on_file: true\nawaiting_purchase_order: false\namount: 1176.64\namount_approval_threshold: 2500.00\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false",
  "question": "Proposed action: CCV\nWould what the record shows make the proposed action the right call here?",
  "definitions": "Meanings:\n- MM: pause and collect more information first\n- RKDZ: escalate this to someone senior who decides\n- CCV: stop the request so the requester gets nothing from it\n- R: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfb0d657479",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-1823\", \"vendor\": \"Bluepeak Traders\", \"amount_approval_threshold\": 5000.00, \"payment_requested_during_business_hours\": true, \"vendor_tax_form_on_file\": true, \"vendor_free_of_sanctions\": true, \"amount\": 3690.56, \"purchase_order_received\": true, \"duplicate_of_paid_invoice\": false}",
  "question": "Proposed action: put on hold\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qd9f3c3e4ad",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-6264\", \"vendor\": \"Lakeshore Traders\", \"amount\": 2331.78, \"vendor_tax_form_on_file\": true, \"awaiting_purchase_order\": false, \"payment_requested_during_business_hours\": true, \"vendor_free_of_sanctions\": true, \"duplicate_of_paid_invoice\": false, \"amount_approval_threshold\": 5000.00}",
  "question": "Proposed action: approve\nDoes the evidence in the record rule out the proposed action as a choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n2. ask_manager if amount is above amount_approval_threshold.\n3. deny if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qeb1b69fd28",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n* invoice id: INV-1531\n* vendor: Stonebridge Foods\n* vendor tax form on file: yes\n* duplicate of paid invoice: no\n* payment requested during business hours: no\n* amount approval threshold: 25000.00\n* amount: 25000.00\n* purchase order received: no\n* vendor free of sanctions: yes",
  "question": "Meanings:\n- MDZQ: halt the request at this point\n- NHZ: be left pending until the review has been finished\n- Q: forward the matter as the call rests with someone higher\n- NT: proceed and the requester gets what they asked\nThe record is complete: nothing else applies.\n\nWith reference to the record, which of the actions listed below is the appropriate course for the request?",
  "options": [
   "Q",
   "NT",
   "NHZ"
  ]
 },
 {
  "qid": "q8f66244415",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n* invoice id: INV-8754\n* vendor: Copperfield Works\n* duplicate of paid invoice: no\n* vendor free of sanctions: no\n* payment requested during business hours: yes\n* amount approval threshold: 2500.00\n* amount: 2112.24\n* purchase order received: yes\n* vendor tax form on file: yes",
  "question": "The record is complete: nothing else applies.\n\nFor the case in this file, which of the actions listed should be taken?",
  "options": [
   "pay",
   "escalate",
   "reject"
  ]
 },
 {
  "qid": "q76610d7f1c",
  "kind": "choice",
  "text": "# request record\ninvoice_id: INV-5166\nvendor: Pinecrest Foods\nvendor_tax_form_missing: false\namount_approval_threshold: 5000.00\npayment_requested_during_business_hours: true\npurchase_order_received: true\nduplicate_of_paid_invoice: true\nvendor_on_sanctions_list: true\namount: 1558.86",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if amount is at least amount_approval_threshold.\n2. deny if duplicate_of_paid_invoice is true.\n3. ask manager if vendor_on_sanctions_list is true.\nOtherwise: approve.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nWhich of the listed actions is the right call for this request?",
  "options": [
   "deny",
   "approve",
   "ask manager"
  ]
 },
 {
  "qid": "q24236482f0",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-8542\",\"vendor\":\"Silverline Traders\",\"amount_approval_threshold\":5000.00,\"duplicate_of_paid_invoice\":false,\"payment_requested_during_business_hours\":true,\"vendor_tax_form_on_file\":true,\"vendor_free_of_sanctions\":true,\"purchase_order_received\":false,\"amount\":4722.05}",
  "question": "Proposed action: 31\nQuick question: is the proposed action the right thing to do with this request?",
  "definitions": "Meanings:\n- 7819: have the task carried out as it was originally asked\n- 31: pump the brakes until more details show up\n- 434: bring in the authority who can settle it for the requester\n- 4: end it so the requester sees their request closed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0b955fa73b",
  "kind": "yes/no",
  "text": "# request record\ninvoice_id: INV-7845\nvendor: Brightwater Logistics\nduplicate_of_paid_invoice: true\nvendor_tax_form_missing: false\npurchase_order_received: true\nvendor_free_of_sanctions: true\namount: 23959.71\namount_approval_threshold: 25000.00\npayment_requested_during_business_hours: false",
  "question": "Proposed action: release\nIs the proposed action not a sound choice for this situation?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if amount is at least amount_approval_threshold.\n2. delay if purchase_order_received is false or vendor_tax_form_missing is true.\n3. cancel_order if duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- release: proceed and the requester gets what they asked\n- delay: pause this until the requester supplies the missing document\n- cancel_order: be rejected in full and never acted upon\n- hand_to_a_person: be passed along to whoever makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc9280fdb38",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-6787\",\n  \"vendor\":\"Harbor Supply\",\n  \"awaiting_purchase_order\":false,\n  \"vendor_tax_form_missing\":false,\n  \"vendor_free_of_sanctions\":true,\n  \"duplicate_of_paid_invoice\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"amount_approval_threshold\":1000.00,\n  \"amount\":289.48\n}",
  "question": "Proposed action: hand_to_a_person\nIs it not correct that the proposed action is not an error given what the record shows?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. cancel_order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. hand_to_a_person if vendor_tax_form_missing is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- cancel_order: bin this idea and keep it out of the flow\n- release: proceed with the task as asked\n- delay: wait for the document to come through\n- hand_to_a_person: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8f218c4773",
  "kind": "choice",
  "text": "{\n  \"subject\": {\n    \"invoice_id\": \"INV-1726\",\n    \"vendor\": \"Silverline Partners\"\n  },\n  \"amounts\": {\n    \"amount\": 1163.46,\n    \"amount_approval_threshold\": 5000.00\n  },\n  \"checks\": {\n    \"duplicate_of_paid_invoice\": true,\n    \"awaiting_purchase_order\": false,\n    \"vendor_tax_form_missing\": false,\n    \"vendor_free_of_sanctions\": true,\n    \"payment_requested_during_business_hours\": false\n  }\n}",
  "question": "Meanings:\n- ask manager: submit the question to the authorised decision maker\n- defer: stay on hold until the paperwork arrives\n- deny: end this here and now\n- approve: keep moving so the asker gets the outcome\nThe record is complete: nothing else applies.\n\nMind telling me which of the actions below is the best call for this request?",
  "options": [
   "ask manager",
   "deny",
   "defer"
  ]
 },
 {
  "qid": "q2d0e7a24f8",
  "kind": "choice",
  "text": "invoice_id=INV-2856\nvendor=Pinecrest Foods\nawaiting_purchase_order=false\nduplicate_of_paid_invoice=true\npayment_requested_during_business_hours=true\nvendor_tax_form_missing=false\namount=1000.01\namount_approval_threshold=1000.00\nvendor_on_sanctions_list=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if vendor_on_sanctions_list is true.\n2. send_to_a_person if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. put_on_hold if amount is above amount_approval_threshold.\nOtherwise: go_ahead.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nGiven the request and the facts stated, which of the actions listed is the right call?",
  "options": [
   "put_on_hold",
   "go_ahead",
   "turn_down"
  ]
 },
 {
  "qid": "qe3416ef62f",
  "kind": "choice",
  "text": "# record\ninvoice_id: INV-4848\nvendor: Redwood Works\nawaiting_purchase_order: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\namount: 372.29\nvendor_tax_form_missing: false\nvendor_on_sanctions_list: false\namount_approval_threshold: 500.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. HD if amount is at least amount_approval_threshold.\n2. W if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. RJGT if duplicate_of_paid_invoice is true.\nOtherwise: HSZ.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours.\nMeanings:\n- HD: get referred to the person who decides\n- W: keep it on hold for the missing document\n- RJGT: decline the request as the action is prohibited\n- HSZ: continue the work as originally asked, there is nothing in the way\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "HD",
   "RJGT",
   "HSZ"
  ]
 },
 {
  "qid": "q8d59f747dd",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-9508\",\"vendor\":\"Oakmont Supply\",\"awaiting_purchase_order\":true,\"payment_requested_during_business_hours\":true,\"duplicate_of_paid_invoice\":true,\"amount\":22218.56,\"vendor_tax_form_missing\":false,\"vendor_free_of_sanctions\":true,\"amount_approval_threshold\":25000.00}",
  "question": "Proposed action: PD\nLooking at the facts, does that rule out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. KXM if amount is at least amount_approval_threshold.\n2. L if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. PD if duplicate_of_paid_invoice is true.\nOtherwise: CFSM.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- KXM: route this matter to the individual empowered to decide\n- L: hold up for a sec until more info comes in\n- PD: reject this item since it violates the policy\n- CFSM: proceed as requested as nothing impedes this course\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q56b814a2c1",
  "kind": "yes/no",
  "text": "---\ninvoice_id: INV-2433\nvendor: Riverbend Systems\nduplicate_of_paid_invoice: false\nvendor_free_of_sanctions: true\namount_approval_threshold: 25000.00\nvendor_tax_form_on_file: true\npayment_requested_during_business_hours: true\npurchase_order_received: false\namount: 2895.01",
  "question": "Proposed action: B\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Meanings:\n- JN: forward the case to the approver with authority\n- WSTX: run with it carry on as you were\n- B: hold up for a sec until more info comes in\n- VZV: refuse this request entirely\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q94cf622e93",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-4728\nvendor=Redwood Group\namount_approval_threshold=10000.00\nvendor_tax_form_missing=false\nduplicate_of_paid_invoice=false\npurchase_order_received=true\npayment_requested_during_business_hours=true\namount=5713.69\nvendor_on_sanctions_list=true",
  "question": "Proposed action: 6\nDoes the proposed action fit the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 88 if vendor_tax_form_missing is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. 294 if vendor_on_sanctions_list is true.\n3. 9158 if purchase_order_received is false.\nOtherwise: 6.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 9158: hold off until the check clears\n- 88: route this to the one who signs off\n- 6: finish what was asked as stated, the way ahead is fully free\n- 294: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9ccf6f941e",
  "kind": "yes/no",
  "text": "{\n    \"subject\": {\n        \"invoice_id\": \"INV-6974\",\n        \"vendor\": \"Northwind Supply\"\n    },\n    \"amounts\": {\n        \"amount_approval_threshold\": 5000.00,\n        \"amount\": 2434.64\n    },\n    \"checks\": {\n        \"payment_requested_during_business_hours\": true,\n        \"vendor_tax_form_missing\": false,\n        \"duplicate_of_paid_invoice\": false,\n        \"awaiting_purchase_order\": false,\n        \"vendor_free_of_sanctions\": false\n    }\n}",
  "question": "Proposed action: cancel order\nLooking at the facts, does that rule out the proposed action for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qc51aac2b2b",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-5624\",\"vendor\":\"Riverbend Logistics\",\"awaiting_purchase_order\":false,\"duplicate_of_paid_invoice\":false,\"vendor_free_of_sanctions\":true,\"payment_requested_during_business_hours\":true,\"amount_approval_threshold\":10000.00,\"vendor_tax_form_missing\":false,\"amount\":3673.63}",
  "question": "Meanings:\n- reject: shut off this process completely\n- hold: hold up for a sec until more info comes in\n- escalate: bring in the authority who can settle it for the requester\n- pay: complete the job as it was assigned\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "pay",
   "reject",
   "hold"
  ]
 },
 {
  "qid": "q0a14efe209",
  "kind": "yes/no",
  "text": "{\n  \"request\": {\n    \"invoice_id\": \"INV-7310\",\n    \"vendor\": \"Oakmont Supply\"\n  },\n  \"figures\": {\n    \"amount\": 938.33,\n    \"amount_approval_threshold\": 1000.00\n  },\n  \"checks\": {\n    \"vendor_free_of_sanctions\": false,\n    \"awaiting_purchase_order\": false,\n    \"vendor_tax_form_missing\": false,\n    \"payment_requested_during_business_hours\": true,\n    \"duplicate_of_paid_invoice\": false\n  }\n}",
  "question": "Proposed action: 439\nIs the proposed action not really the right move for this request?",
  "definitions": "Meanings:\n- 9: defer the step until the verification is in\n- 5773: let the request be continued as originally asked\n- 439: reject the petition as the action is unauthorized\n- 11: pass the request to a decider\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5bfdf81241",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-2597\",\n  \"vendor\":\"Fairview Supply\",\n  \"payment_requested_during_business_hours\":true,\n  \"duplicate_of_paid_invoice\":true,\n  \"vendor_tax_form_on_file\":true,\n  \"vendor_on_sanctions_list\":false,\n  \"amount_approval_threshold\":500.00,\n  \"amount\":479.71,\n  \"purchase_order_received\":true\n}",
  "question": "Proposed action: pay\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- reject: shut this down fast\n- pay: proceed with the task as asked\n- hold: defer the step until the verification is in\n- escalate: send it up so the requester gets a firm decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7336200feb",
  "kind": "choice",
  "text": "invoice_id: INV-1927\nvendor: Stonebridge Partners\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\nvendor_tax_form_on_file: true\namount: 10000.01\nvendor_on_sanctions_list: false\npurchase_order_received: true\namount_approval_threshold: 10000.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "escalate",
   "pay",
   "hold"
  ]
 },
 {
  "qid": "q37700158d7",
  "kind": "yes/no",
  "text": "---\ninvoice_id: \"INV-5138\"\nvendor: \"Fairview Industries\"\nvendor_tax_form_on_file: true\namount_approval_threshold: 10000.00\nduplicate_of_paid_invoice: true\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: true\npurchase_order_received: true\namount: 7690.03",
  "question": "Proposed action: defer\nBe honest, do the facts here rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if purchase_order_received is false or vendor_tax_form_on_file is false.\n2. ask_manager if amount is above amount_approval_threshold.\n3. deny if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- defer: be kept on hold until more information is supplied\n- deny: scrap the plan and drop this request\n- approve: let this be advanced exactly as originally specified\n- ask_manager: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb494220779",
  "kind": "choice",
  "text": "---\n# request record\nrecord:\n    invoice_id: \"INV-9585\"\n    vendor: \"Harbor Logistics\"\nnumbers:\n    amount: 369.70\n    amount_approval_threshold: 1000.00\nflags:\n    duplicate_of_paid_invoice: false\n    vendor_free_of_sanctions: true\n    vendor_tax_form_missing: false\n    awaiting_purchase_order: false\n    payment_requested_during_business_hours: true",
  "question": "The record is complete: nothing else applies.\n\nSign-off check: which of the actions listed below is the correct call for the request?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "turn_down"
  ]
 },
 {
  "qid": "qaa114c192f",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-8359\",\n  \"vendor\":\"Stonebridge Supply\",\n  \"amount\":422.27,\n  \"amount_approval_threshold\":1000.00,\n  \"duplicate_of_paid_invoice\":false,\n  \"payment_requested_during_business_hours\":false,\n  \"vendor_tax_form_missing\":false,\n  \"purchase_order_received\":true,\n  \"vendor_free_of_sanctions\":true\n}",
  "question": "Proposed action: send_to_a_person\nIs it not so that the proposed action is not mistaken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn_down if vendor_free_of_sanctions is false.\n3. put_on_hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q57294a5464",
  "kind": "yes/no",
  "text": "invoice_id | INV-4324\nvendor | Lakeshore Industries\nvendor_tax_form_on_file | true\npayment_requested_during_business_hours | false\nduplicate_of_paid_invoice | true\npurchase_order_received | true\nvendor_free_of_sanctions | true\namount_approval_threshold | 10000.00\namount | 7893.09",
  "question": "Proposed action: R\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. FC if amount is at least amount_approval_threshold.\n2. CXS if duplicate_of_paid_invoice is true.\n3. HVQL if vendor_free_of_sanctions is false.\nOtherwise: R.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- FC: keep waiting for the missing details\n- R: commence the action as specified without impediment\n- CXS: skip this one, it is a hard pass for us\n- HVQL: send it to whoever has the final say\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qae3270a9b6",
  "kind": "yes/no",
  "text": "---\n# record\ninvoice_id: \"INV-8807\"\nvendor: \"Riverbend Foods\"\nawaiting_purchase_order: false\nvendor_on_sanctions_list: true\namount: 5714.95\nduplicate_of_paid_invoice: false\nvendor_tax_form_missing: false\namount_approval_threshold: 10000.00\npayment_requested_during_business_hours: true",
  "question": "Proposed action: go ahead\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- put on hold: hold the request so the requester waits for their check\n- send to a person: route the request to the decision maker\n- turn down: end it so the requester sees their request closed\n- go ahead: keep plugging away at it nothing else stands in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9dd6544dcc",
  "kind": "choice",
  "text": "---\n# record\ninvoice_id: \"INV-9474\"\nvendor: \"Northwind Group\"\nvendor_on_sanctions_list: true\npayment_requested_during_business_hours: true\namount: 2500.00\nduplicate_of_paid_invoice: false\nawaiting_purchase_order: false\nvendor_tax_form_on_file: true\namount_approval_threshold: 2500.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 740 if awaiting_purchase_order is true.\n2. 6 if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. 4154 if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: 52.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 740: hold off until more information arrives\n- 4154: send it onward because someone else must decide\n- 6: withdraw from the step as it is forbidden\n- 52: have the plan kept moving as it was requested\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "740",
   "6",
   "52"
  ]
 },
 {
  "qid": "q5018220068",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-1823\nvendor = Fairview Industries\nduplicate_of_paid_invoice = false\nawaiting_purchase_order = false\nvendor_on_sanctions_list = false\npayment_requested_during_business_hours = false\namount_approval_threshold = 1000.00\namount = 338.05\nvendor_tax_form_on_file = false",
  "question": "Proposed action: 69\nIs it not the case that, given the record, the proposed action is not a poor call?",
  "definitions": "Meanings:\n- 932: hand it up to the person who decides\n- 1: run the requested step through\n- 3122: be held back until a check or document arrives\n- 69: end this here and now\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcd2b624494",
  "kind": "yes/no",
  "text": "{\n  \"subject\": {\n    \"invoice_id\": \"INV-5784\",\n    \"vendor\": \"Fairview Partners\"\n  },\n  \"amounts\": {\n    \"amount_approval_threshold\": 2500.00,\n    \"amount\": 1996.93\n  },\n  \"checks\": {\n    \"vendor_on_sanctions_list\": false,\n    \"payment_requested_during_business_hours\": false,\n    \"vendor_tax_form_on_file\": true,\n    \"purchase_order_received\": true,\n    \"duplicate_of_paid_invoice\": false\n  }\n}",
  "question": "Proposed action: delay\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel_order if vendor_on_sanctions_list is true.\n3. delay if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- hand_to_a_person: toss it over to the one who makes the call\n- release: continue with what was requested\n- delay: hang tight until we get the check back\n- cancel_order: refuse this request entirely\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q320b605702",
  "kind": "yes/no",
  "text": "invoice_id | INV-7919\nvendor | Oakmont Logistics\namount_approval_threshold | 500.00\namount | 279.19\nvendor_tax_form_missing | false\nawaiting_purchase_order | false\nduplicate_of_paid_invoice | true\nvendor_on_sanctions_list | false\npayment_requested_during_business_hours | false",
  "question": "Proposed action: deny\nReviewing this as an auditor, do the record's facts rule out the proposed action for the request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qbc3a8bb7f0",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-7375\n  vendor: Northwind Systems\nvalues:\n  amount: 10000.01\n  amount_approval_threshold: 10000.00\ntests:\n  vendor_on_sanctions_list: false\n  purchase_order_received: true\n  duplicate_of_paid_invoice: false\n  payment_requested_during_business_hours: true\n  vendor_tax_form_on_file: true",
  "question": "Proposed action: pay\nBased on the record, is the proposed action the correct call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is above amount_approval_threshold.\n2. reject if vendor_on_sanctions_list is true.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- pay: keep going with it nothing is blocking you\n- reject: kill this one off\n- escalate: send it up so the requester gets a firm decision\n- hold: postpone proceeding until the check is completed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfc93e03ef3",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-3136\", \"vendor\": \"Redwood Industries\", \"vendor_on_sanctions_list\": false, \"amount\": 659.46, \"amount_approval_threshold\": 500.00, \"vendor_tax_form_missing\": true, \"payment_requested_during_business_hours\": true, \"awaiting_purchase_order\": false, \"duplicate_of_paid_invoice\": false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. reject if vendor_on_sanctions_list is true.\n2. escalate if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. hold if amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nBased on what the record shows, which of the actions listed is the right call?",
  "options": [
   "reject",
   "pay",
   "escalate"
  ]
 },
 {
  "qid": "q9e87a7192f",
  "kind": "yes/no",
  "text": "{\n  \"record\": {\n    \"invoice_id\": \"INV-1553\",\n    \"vendor\": \"Bluepeak Group\"\n  },\n  \"numbers\": {\n    \"amount_approval_threshold\": 10000.00,\n    \"amount\": 3591.52\n  },\n  \"flags\": {\n    \"payment_requested_during_business_hours\": true,\n    \"vendor_on_sanctions_list\": false,\n    \"duplicate_of_paid_invoice\": false,\n    \"vendor_tax_form_on_file\": false,\n    \"awaiting_purchase_order\": false\n  }\n}",
  "question": "Proposed action: defer\nDoes what the record shows suggest the proposed action is not the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qa2b622f792",
  "kind": "yes/no",
  "text": "---\n# case\nsubject:\n  invoice_id: \"INV-3180\"\n  vendor: \"Harbor Labs\"\namounts:\n  amount_approval_threshold: 1000.00\n  amount: 993.93\nchecks:\n  purchase_order_received: true\n  payment_requested_during_business_hours: true\n  vendor_tax_form_missing: false\n  vendor_on_sanctions_list: false\n  duplicate_of_paid_invoice: false",
  "question": "Proposed action: delay\nIs it not the case that the proposed action is not a poor choice for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel_order if vendor_on_sanctions_list is true.\n3. delay if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- hand_to_a_person: bring in the owner who can rule on this\n- release: push ahead as planned\n- delay: shelve the matter until more details come in\n- cancel_order: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2afcbaa8c9",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-8608\n- vendor: Northwind Traders\n- vendor free of sanctions: yes\n- payment requested during business hours: yes\n- awaiting purchase order: no\n- duplicate of paid invoice: no\n- vendor tax form on file: yes\n- amount approval threshold: 10000.00\n- amount: 10000.00",
  "question": "Proposed action: release\nIs the proposed action not the right call for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q545356a8cb",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-2608\n- vendor: Oakmont Traders\n- amount approval threshold: 500.00\n- vendor tax form on file: yes\n- purchase order received: yes\n- payment requested during business hours: yes\n- vendor free of sanctions: yes\n- amount: 122.65\n- duplicate of paid invoice: yes",
  "question": "Meanings:\n- 6: keep going with it\n- 184: route the case to a decider so the requester knows the outcome\n- 3083: be parked until a verification has been logged\n- 51: halt the request at this point\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "3083",
   "6",
   "51"
  ]
 },
 {
  "qid": "q55d231058a",
  "kind": "choice",
  "text": "invoice_id: INV-7655\nvendor: Oakmont Partners\nvendor_tax_form_missing: true\nduplicate_of_paid_invoice: false\nvendor_free_of_sanctions: true\namount: 564.45\namount_approval_threshold: 2500.00\npayment_requested_during_business_hours: true\nawaiting_purchase_order: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if amount is at least amount_approval_threshold.\n2. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. turn_down if duplicate_of_paid_invoice is true.\nOtherwise: go_ahead.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nWhat is the best action to pick from the list for this request?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "send_to_a_person"
  ]
 },
 {
  "qid": "q8e75bd4620",
  "kind": "yes/no",
  "text": "---\n# case\nsubject:\n  invoice_id: \"INV-8608\"\n  vendor: \"Northwind Traders\"\namounts:\n  amount_approval_threshold: 10000.00\n  amount: 10000.00\nchecks:\n  payment_requested_during_business_hours: true\n  vendor_free_of_sanctions: true\n  awaiting_purchase_order: false\n  vendor_tax_form_on_file: true\n  duplicate_of_paid_invoice: false",
  "question": "Proposed action: release\nIs the proposed action not the right call for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qf8cb0e694e",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-3244\n- vendor: Northwind Systems\n- payment requested during business hours: yes\n- purchase order received: yes\n- amount approval threshold: 5000.00\n- vendor tax form on file: yes\n- vendor on sanctions list: yes\n- duplicate of paid invoice: no\n- amount: 860.59",
  "question": "Meanings:\n- hold: hold off until the check has been completed by the team\n- escalate: delegate the call to whoever holds authority\n- reject: send the requester away with the request left unfinished\n- pay: continue the work as originally asked, there is nothing in the way\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "escalate",
   "reject",
   "pay"
  ]
 },
 {
  "qid": "q073540822b",
  "kind": "choice",
  "text": "# record\ninvoice_id: INV-5550\nvendor: Copperfield Traders\npurchase_order_received: true\namount: 500.01\nvendor_free_of_sanctions: true\npayment_requested_during_business_hours: true\namount_approval_threshold: 500.00\nvendor_tax_form_on_file: true\nduplicate_of_paid_invoice: false",
  "question": "Meanings:\n- 78: refuse to act since the step is prohibited\n- 2: keep moving on this one nothing is holding it up\n- 6446: keep it in limbo until the verification has been confirmed\n- 631: hand this over to whoever has the final say\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "631",
   "78",
   "2"
  ]
 },
 {
  "qid": "q1de5979a02",
  "kind": "yes/no",
  "text": "# case\ninvoice_id: INV-3482\nvendor: Riverbend Foods\nawaiting_purchase_order: false\nduplicate_of_paid_invoice: false\namount_approval_threshold: 25000.00\nvendor_tax_form_on_file: true\nvendor_free_of_sanctions: true\npayment_requested_during_business_hours: true\namount: 7475.87",
  "question": "Proposed action: deny\nIs the proposed action ruled out by what the record says?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if amount is at least amount_approval_threshold.\n2. defer if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. deny if duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- approve: advance the task as stated without any blockers\n- defer: wait for the document to come through\n- ask manager: route this matter to the individual empowered to decide\n- deny: refuse the request because it crosses a clear line\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd9ac0bdc7b",
  "kind": "choice",
  "text": "invoice_id | INV-8359\nvendor | Harbor Supply\nawaiting_purchase_order | false\nvendor_tax_form_on_file | false\namount | 10000.00\npayment_requested_during_business_hours | true\namount_approval_threshold | 10000.00\nduplicate_of_paid_invoice | false\nvendor_on_sanctions_list | false",
  "question": "Meanings:\n- KRGT: keep moving so the asker gets the outcome\n- GNF: direct the request to the responsible decider\n- CL: be blocked outright so it never gets carried out\n- R: stall the request until the check comes back\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "KRGT",
   "GNF",
   "R"
  ]
 },
 {
  "qid": "q4f3eeebe98",
  "kind": "yes/no",
  "text": "invoice_id | INV-4324\nvendor | Lakeshore Industries\nvendor_tax_form_on_file | true\npayment_requested_during_business_hours | false\nduplicate_of_paid_invoice | false\npurchase_order_received | true\nvendor_free_of_sanctions | true\namount_approval_threshold | 10000.00\namount | 7893.09",
  "question": "Proposed action: R\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. FC if amount is at least amount_approval_threshold.\n2. CXS if duplicate_of_paid_invoice is true.\n3. HVQL if vendor_free_of_sanctions is false.\nOtherwise: R.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- FC: keep waiting for the missing details\n- R: commence the action as specified without impediment\n- CXS: skip this one, it is a hard pass for us\n- HVQL: send it to whoever has the final say\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qbfe10033eb",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-2942\n- vendor: Copperfield Labs\n- amount: 4035.41\n- amount approval threshold: 5000.00\n- vendor free of sanctions: yes\n- payment requested during business hours: yes\n- vendor tax form on file: no\n- purchase order received: yes\n- duplicate of paid invoice: no",
  "question": "Proposed action: escalate\nIs the proposed action not what should happen with this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1dfd83b5e9",
  "kind": "choice",
  "text": "---\n# request record\nrecord:\n    invoice_id: \"INV-5710\"\n    vendor: \"Lakeshore Partners\"\nnumbers:\n    amount: 500.01\n    amount_approval_threshold: 500.00\nflags:\n    vendor_tax_form_on_file: true\n    vendor_free_of_sanctions: true\n    awaiting_purchase_order: false\n    duplicate_of_paid_invoice: false\n    payment_requested_during_business_hours: true",
  "question": "Meanings:\n- deny: toss it out, we are never doing this\n- ask manager: send it onward because someone else must decide\n- defer: defer further action pending verification of the document\n- approve: complete the action that was asked for\nThe record is complete: nothing else applies.\n\nJudging by the facts in the record, which listed action is the right call?",
  "options": [
   "deny",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "q6ce3c6a336",
  "kind": "choice",
  "text": "{\n    \"subject\":{\n        \"invoice_id\":\"INV-7288\",\n        \"vendor\":\"Stonebridge Industries\"\n    },\n    \"amounts\":{\n        \"amount_approval_threshold\":5000.00,\n        \"amount\":5646.82\n    },\n    \"checks\":{\n        \"vendor_on_sanctions_list\":false,\n        \"payment_requested_during_business_hours\":true,\n        \"duplicate_of_paid_invoice\":false,\n        \"purchase_order_received\":true,\n        \"vendor_tax_form_on_file\":true\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "pay",
   "escalate",
   "reject"
  ]
 },
 {
  "qid": "q80f94de235",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-1845\nvendor=Silverline Labs\namount_approval_threshold=5000.00\namount=4899.72\nvendor_tax_form_missing=false\npayment_requested_during_business_hours=true\nawaiting_purchase_order=false\nduplicate_of_paid_invoice=false\nvendor_free_of_sanctions=false",
  "question": "Proposed action: reject\nDoes what we know about this rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. reject if vendor_free_of_sanctions is false.\n2. escalate if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. hold if amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- escalate: escalate it so the person asking receives a decision\n- pay: continue with the request as nothing obstructs it\n- reject: block it right away\n- hold: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc058dbbd54",
  "kind": "yes/no",
  "text": "---\nrequest:\n  invoice_id: INV-7531\n  vendor: Oakmont Systems\nfigures:\n  amount_approval_threshold: 5000.00\n  amount: 621.40\nchecks:\n  awaiting_purchase_order: true\n  vendor_free_of_sanctions: true\n  vendor_tax_form_on_file: true\n  payment_requested_during_business_hours: false\n  duplicate_of_paid_invoice: false",
  "question": "Proposed action: go_ahead\nDo the facts here rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qa2bc205c32",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"invoice_id\": \"INV-4297\",\n        \"vendor\": \"Copperfield Supply\"\n    },\n    \"metrics\": {\n        \"amount_approval_threshold\": 25000.00,\n        \"amount\": 24381.77\n    },\n    \"signals\": {\n        \"vendor_tax_form_on_file\": true,\n        \"vendor_on_sanctions_list\": false,\n        \"duplicate_of_paid_invoice\": true,\n        \"payment_requested_during_business_hours\": true,\n        \"purchase_order_received\": true\n    }\n}",
  "question": "Proposed action: defer\nWould what the record shows make the proposed action the right call here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if vendor_on_sanctions_list is true.\n2. ask manager if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. defer if amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5286751a5d",
  "kind": "yes/no",
  "text": "---\ninvoice_id: \"INV-5594\"\nvendor: \"Redwood Labs\"\nvendor_free_of_sanctions: false\npayment_requested_during_business_hours: true\namount_approval_threshold: 5000.00\namount: 9349.71\nvendor_tax_form_on_file: true\nduplicate_of_paid_invoice: false\nawaiting_purchase_order: true",
  "question": "Proposed action: 28\nIs it not so that the proposed action is not at odds with the facts and the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 9 if amount is at least amount_approval_threshold.\n2. 28 if duplicate_of_paid_invoice is true.\n3. 7957 if vendor_free_of_sanctions is false.\nOtherwise: 758.\nNever counted: awaiting_purchase_order, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- 758: just crack on with it there is nothing in the way\n- 28: refuse to act since the step is prohibited\n- 7957: route the case to a decider so the requester knows the outcome\n- 9: wait for the missing material to come in before deciding anything\nThe record is complete: nothing else applies."
 }
]
