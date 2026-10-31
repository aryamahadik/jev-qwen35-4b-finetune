# G5-H blind read T46-blind_read-05dcb4b4-001 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r6a/T46/qc/g5h/answers/T46-blind_read-05dcb4b4-001.json

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
  "qid": "q50ca7032e0",
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
  "qid": "qe21d1eec62",
  "kind": "choice",
  "text": "{\n    \"record\":{\n        \"invoice_id\":\"INV-1421\",\n        \"vendor\":\"Ironleaf Foods\"\n    },\n    \"numbers\":{\n        \"amount_approval_threshold\":500.00,\n        \"amount\":500.00\n    },\n    \"flags\":{\n        \"vendor_on_sanctions_list\":true,\n        \"duplicate_of_paid_invoice\":false,\n        \"purchase_order_received\":true,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_tax_form_on_file\":true\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "ask manager",
   "deny",
   "approve"
  ]
 },
 {
  "qid": "qb53ccb20b0",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-5624\",\"vendor\":\"Riverbend Logistics\",\"awaiting_purchase_order\":false,\"duplicate_of_paid_invoice\":false,\"vendor_free_of_sanctions\":false,\"payment_requested_during_business_hours\":true,\"amount_approval_threshold\":10000.00,\"vendor_tax_form_missing\":false,\"amount\":3673.63}",
  "question": "Meanings:\n- reject: shut off this process completely\n- hold: hold up for a sec until more info comes in\n- escalate: bring in the authority who can settle it for the requester\n- pay: complete the job as it was assigned\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "pay",
   "reject",
   "hold"
  ]
 },
 {
  "qid": "q2b275a979d",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id | INV-9718\nvendor | Ironleaf Works\namount_approval_threshold | 1000.00\namount | 1000.00\nvendor_on_sanctions_list | false\nawaiting_purchase_order | false\nvendor_tax_form_on_file | true\npayment_requested_during_business_hours | true\nduplicate_of_paid_invoice | false",
  "question": "Proposed action: cancel_order\nIs the proposed action ruled out by what the record says?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n2. hand_to_a_person if amount is above amount_approval_threshold.\n3. cancel_order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qecf359c6b4",
  "kind": "choice",
  "text": "---\ncase:\n    invoice_id: \"INV-6490\"\n    vendor: \"Oakmont Traders\"\nvalues:\n    amount: 182.09\n    amount_approval_threshold: 500.00\ntests:\n    vendor_free_of_sanctions: true\n    payment_requested_during_business_hours: true\n    vendor_tax_form_missing: false\n    purchase_order_received: false\n    duplicate_of_paid_invoice: false",
  "question": "Meanings:\n- reject: drop this request from the queue\n- pay: allow the matter to be taken forward as planned\n- escalate: pass the request to a decider\n- hold: suspend progress until verification is received\nThe record is complete: nothing else applies.\n\nWhich of the actions below does the record point to as the right call?",
  "options": [
   "pay",
   "reject",
   "hold"
  ]
 },
 {
  "qid": "qebc142e14b",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-9761\n- vendor: Fairview Logistics\n- amount: 1296.30\n- amount approval threshold: 2500.00\n- payment requested during business hours: yes\n- duplicate of paid invoice: no\n- awaiting purchase order: yes\n- vendor tax form on file: yes\n- vendor free of sanctions: no",
  "question": "Proposed action: deny\nIs it not so that the proposed action is not mistaken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. deny if vendor_free_of_sanctions is false.\n3. defer if awaiting_purchase_order is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- approve: execute the request exactly as written\n- ask_manager: send it up so the requester gets a firm decision\n- defer: park the file until the requester sends the document in\n- deny: drop it right away\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf4fb338b2e",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-4728\nvendor=Redwood Group\namount_approval_threshold=10000.00\nvendor_tax_form_missing=false\nduplicate_of_paid_invoice=false\npurchase_order_received=true\npayment_requested_during_business_hours=true\namount=5713.69\nvendor_on_sanctions_list=true",
  "question": "Proposed action: 6\nDoes the proposed action fit the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 88 if vendor_tax_form_missing is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. 294 if vendor_on_sanctions_list is true.\n3. 9158 if purchase_order_received is false.\nOtherwise: 6.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 9158: hold off until the check clears\n- 88: route this to the one who signs off\n- 6: finish what was asked as stated, the way ahead is fully free\n- 294: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3f22ae3a78",
  "kind": "yes/no",
  "text": "invoice_id=INV-4463\nvendor=Summit Traders\npurchase_order_received=true\nduplicate_of_paid_invoice=false\namount_approval_threshold=10000.00\nvendor_free_of_sanctions=true\nvendor_tax_form_missing=false\namount=4685.32\npayment_requested_during_business_hours=true",
  "question": "Proposed action: release\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if amount is at least amount_approval_threshold.\n2. delay if purchase_order_received is false or vendor_tax_form_missing is true.\n3. cancel_order if duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb1debce456",
  "kind": "yes/no",
  "text": "{\n  \"record\": {\n    \"invoice_id\": \"INV-1553\",\n    \"vendor\": \"Bluepeak Group\"\n  },\n  \"numbers\": {\n    \"amount_approval_threshold\": 10000.00,\n    \"amount\": 3591.52\n  },\n  \"flags\": {\n    \"payment_requested_during_business_hours\": true,\n    \"vendor_on_sanctions_list\": false,\n    \"duplicate_of_paid_invoice\": false,\n    \"vendor_tax_form_on_file\": false,\n    \"awaiting_purchase_order\": false\n  }\n}",
  "question": "Proposed action: defer\nDoes what the record shows suggest the proposed action is not the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q4c8194730d",
  "kind": "yes/no",
  "text": "invoice_id: INV-5517\nvendor: Pinecrest Foods\nvendor_tax_form_on_file: true\nawaiting_purchase_order: false\namount: 1176.64\namount_approval_threshold: 2500.00\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false",
  "question": "Proposed action: CCV\nWould what the record shows make the proposed action the right call here?",
  "definitions": "Meanings:\n- MM: pause and collect more information first\n- RKDZ: escalate this to someone senior who decides\n- CCV: stop the request so the requester gets nothing from it\n- R: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe9bce91f7f",
  "kind": "yes/no",
  "text": "---\n# record\ninvoice_id: \"INV-4630\"\nvendor: \"Pinecrest Traders\"\namount_approval_threshold: 1000.00\nawaiting_purchase_order: false\nvendor_tax_form_on_file: true\namount: 1844.56\nvendor_free_of_sanctions: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false",
  "question": "Proposed action: hold\nTell me straight, is the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_free_of_sanctions is false.\nOtherwise: pay.\nNever counted: awaiting_purchase_order, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- hold: keep waiting for the missing details\n- reject: ditch the whole thing, nobody should act on it\n- pay: keep going exactly as requested because every obstacle has cleared\n- escalate: kick it up to whoever makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2d0b268e33",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-2597\",\n  \"vendor\":\"Fairview Supply\",\n  \"payment_requested_during_business_hours\":true,\n  \"duplicate_of_paid_invoice\":true,\n  \"vendor_tax_form_on_file\":true,\n  \"vendor_on_sanctions_list\":false,\n  \"amount_approval_threshold\":500.00,\n  \"amount\":479.71,\n  \"purchase_order_received\":true\n}",
  "question": "Proposed action: pay\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- reject: shut this down fast\n- pay: proceed with the task as asked\n- hold: defer the step until the verification is in\n- escalate: send it up so the requester gets a firm decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3a9da10edf",
  "kind": "yes/no",
  "text": "---\n# case\nsubject:\n  invoice_id: \"INV-8608\"\n  vendor: \"Northwind Traders\"\namounts:\n  amount_approval_threshold: 10000.00\n  amount: 10000.00\nchecks:\n  payment_requested_during_business_hours: true\n  vendor_free_of_sanctions: true\n  awaiting_purchase_order: false\n  vendor_tax_form_on_file: true\n  duplicate_of_paid_invoice: false",
  "question": "Proposed action: release\nIs the proposed action not the right call for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q2d4ac65c6c",
  "kind": "yes/no",
  "text": "{\n  \"request\": {\n    \"invoice_id\": \"INV-7310\",\n    \"vendor\": \"Oakmont Supply\"\n  },\n  \"figures\": {\n    \"amount\": 938.33,\n    \"amount_approval_threshold\": 1000.00\n  },\n  \"checks\": {\n    \"vendor_free_of_sanctions\": false,\n    \"awaiting_purchase_order\": false,\n    \"vendor_tax_form_missing\": false,\n    \"payment_requested_during_business_hours\": true,\n    \"duplicate_of_paid_invoice\": false\n  }\n}",
  "question": "Proposed action: 439\nIs the proposed action not really the right move for this request?",
  "definitions": "Meanings:\n- 9: defer the step until the verification is in\n- 5773: let the request be continued as originally asked\n- 439: reject the petition as the action is unauthorized\n- 11: pass the request to a decider\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2e5c2659fd",
  "kind": "yes/no",
  "text": "invoice_id=INV-6875\nvendor=Lakeshore Supply\nawaiting_purchase_order=true\nvendor_free_of_sanctions=true\nvendor_tax_form_missing=false\nduplicate_of_paid_invoice=false\namount=1202.72\npayment_requested_during_business_hours=true\namount_approval_threshold=5000.00",
  "question": "Proposed action: go_ahead\nQuick check: do the facts in the record rule out the proposed action here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn_down if vendor_free_of_sanctions is false.\n3. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qeddd9da3e3",
  "kind": "yes/no",
  "text": "# record\ninvoice_id: INV-4197\nvendor: Northwind Foods\npayment_requested_during_business_hours: false\namount: 2500.01\nvendor_tax_form_on_file: true\namount_approval_threshold: 2500.00\npurchase_order_received: true\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: false",
  "question": "Proposed action: GZP\nWeighed against the request in the record, does the proposed action look like the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. BV if vendor_on_sanctions_list is true.\n2. NGNQ if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. GZP if amount is above amount_approval_threshold.\nOtherwise: L.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- GZP: keep it on hold for the missing document\n- L: go on and finish it\n- NGNQ: bring in the authority who can settle it for the requester\n- BV: veto this move and leave it there\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q86acb0cfda",
  "kind": "choice",
  "text": "---\n# case\ninvoice_id: \"INV-9883\"\nvendor: \"Lakeshore Industries\"\nduplicate_of_paid_invoice: false\nvendor_on_sanctions_list: false\namount_approval_threshold: 500.00\npurchase_order_received: false\namount: 170.61\nvendor_tax_form_on_file: true\npayment_requested_during_business_hours: true",
  "question": "Meanings:\n- 311: hold the request until the check is done\n- 38: end it so the requester sees their request closed\n- 6436: get referred to the person who decides\n- 3: keep going with it\nThe record is complete: nothing else applies.\n\nLooking across the actions listed, what would be the correct response to this request?",
  "options": [
   "3",
   "311",
   "6436"
  ]
 },
 {
  "qid": "qb72a01c326",
  "kind": "choice",
  "text": "{\n    \"record\": {\n        \"invoice_id\": \"INV-5205\",\n        \"vendor\": \"Copperfield Systems\"\n    },\n    \"numbers\": {\n        \"amount\": 10000.00,\n        \"amount_approval_threshold\": 10000.00\n    },\n    \"flags\": {\n        \"duplicate_of_paid_invoice\": false,\n        \"purchase_order_received\": false,\n        \"vendor_free_of_sanctions\": true,\n        \"payment_requested_during_business_hours\": true,\n        \"vendor_tax_form_missing\": false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- reject: block this from going any further\n- pay: execute the requested action as nothing prevents it\n- hold: keep it on hold for the missing document\n- escalate: route the request to the decision maker\nThe record is complete: nothing else applies.\n\nThe request describes a situation; which of the actions underneath handles it correctly?",
  "options": [
   "hold",
   "reject",
   "pay"
  ]
 },
 {
  "qid": "q40c4941ec9",
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
  "qid": "q089f0b092a",
  "kind": "choice",
  "text": "invoice_id: INV-9618\nvendor: Summit Traders\nawaiting_purchase_order: true\npayment_requested_during_business_hours: false\namount: 4748.20\nvendor_free_of_sanctions: true\nvendor_tax_form_on_file: true\namount_approval_threshold: 2500.00\nduplicate_of_paid_invoice: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. PVQQ if awaiting_purchase_order is true.\n2. D if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. HV if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: HTX.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- PVQQ: wait for the document to come through\n- HV: hand this off because a decider has to choose\n- HTX: keep plugging away at it nothing else stands in the way\n- D: stop the request so the requester gets nothing from it\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "PVQQ",
   "D",
   "HTX"
  ]
 },
 {
  "qid": "q0377534254",
  "kind": "choice",
  "text": "---\nrequest:\n    invoice_id: INV-3978\n    vendor: Fairview Labs\nfigures:\n    amount_approval_threshold: 10000.00\n    amount: 15968.37\nchecks:\n    vendor_tax_form_on_file: true\n    payment_requested_during_business_hours: true\n    awaiting_purchase_order: false\n    vendor_free_of_sanctions: true\n    duplicate_of_paid_invoice: false",
  "question": "Meanings:\n- SDG: get referred to the person who decides\n- GD: terminate the process as continuation is prohibited\n- W: keep it on hold for the missing document\n- QMSW: complete the action that was asked for\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "GD",
   "W",
   "SDG"
  ]
 },
 {
  "qid": "q840edc23fc",
  "kind": "yes/no",
  "text": "---\n# record\nmeta:\n    invoice_id: \"INV-2787\"\n    vendor: \"Redwood Works\"\nmetrics:\n    amount: 4058.12\n    amount_approval_threshold: 10000.00\nsignals:\n    awaiting_purchase_order: true\n    vendor_free_of_sanctions: false\n    duplicate_of_paid_invoice: true\n    vendor_tax_form_missing: false\n    payment_requested_during_business_hours: false",
  "question": "Proposed action: 4322\nIs the proposed action not a sound choice for this situation?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 4322 if amount is at least amount_approval_threshold.\n2. 65 if duplicate_of_paid_invoice is true.\n3. 8 if vendor_free_of_sanctions is false.\nOtherwise: 636.\nNever counted: awaiting_purchase_order, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- 65: toss it out, we are never doing this\n- 636: finish it so the requester has their answer\n- 8: be forwarded to the person in charge\n- 4322: stay put until the check is finished\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q71696daf38",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n* invoice id: INV-4156\n* vendor: Cedar Traders\n* awaiting purchase order: no\n* duplicate of paid invoice: no\n* vendor free of sanctions: yes\n* payment requested during business hours: yes\n* amount approval threshold: 5000.00\n* vendor tax form missing: no\n* amount: 5000.01",
  "question": "Proposed action: send_to_a_person\nHave the recorded facts ruled out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn_down if vendor_free_of_sanctions is false.\n3. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- send_to_a_person: submit the question to the authorised decision maker\n- go_ahead: let this be advanced exactly as originally specified\n- put_on_hold: wait for the missing material to come in before deciding anything\n- turn_down: leave the requester without the result they asked for\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qeb2a855334",
  "kind": "choice",
  "text": "# case\ninvoice_id: INV-2832\nvendor: Brightwater Works\npurchase_order_received: true\nvendor_tax_form_on_file: false\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: true\namount_approval_threshold: 1000.00\nduplicate_of_paid_invoice: true\namount: 690.13",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if purchase_order_received is false.\n2. cancel order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nGiven the request and the facts stated, which of the actions listed is the right call?",
  "options": [
   "release",
   "delay",
   "cancel order"
  ]
 },
 {
  "qid": "q2da4324954",
  "kind": "yes/no",
  "text": "---\n# request record\ninvoice_id: \"INV-1226\"\nvendor: \"Redwood Partners\"\nvendor_tax_form_missing: false\nvendor_free_of_sanctions: true\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\nawaiting_purchase_order: false\namount: 25000.01\namount_approval_threshold: 25000.00",
  "question": "Proposed action: go ahead\nIs the proposed action the right move for this request, given the facts involved?",
  "definitions": "Meanings:\n- send to a person: hand this to the person who decides\n- put on hold: stay put until the check is finished\n- go ahead: proceed with the task as asked\n- turn down: withdraw from the step as it is forbidden\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q35e1d1e368",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  invoice_id: INV-2138\n  vendor: Brightwater Industries\nnumbers:\n  amount: 10000.00\n  amount_approval_threshold: 10000.00\nflags:\n  duplicate_of_paid_invoice: false\n  payment_requested_during_business_hours: true\n  vendor_free_of_sanctions: false\n  vendor_tax_form_missing: false\n  awaiting_purchase_order: false",
  "question": "Proposed action: release\nHas the request, read alongside the facts, ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. hand_to_a_person if amount is above amount_approval_threshold.\n3. cancel_order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfac18e20d6",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n* invoice id: INV-9043\n* vendor: Riverbend Industries\n* duplicate of paid invoice: no\n* payment requested during business hours: yes\n* amount: 1984.26\n* amount approval threshold: 2500.00\n* vendor tax form on file: yes\n* vendor on sanctions list: no\n* purchase order received: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if purchase_order_received is false.\n2. reject if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. escalate if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nThe request describes a situation; which of the actions underneath handles it correctly?",
  "options": [
   "reject",
   "hold",
   "pay"
  ]
 },
 {
  "qid": "q7b30004f01",
  "kind": "choice",
  "text": "invoice_id=INV-9498\nvendor=Northwind Works\nduplicate_of_paid_invoice=false\nvendor_tax_form_missing=true\namount_approval_threshold=500.00\nvendor_on_sanctions_list=true\nawaiting_purchase_order=false\npayment_requested_during_business_hours=true\namount=499.99",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if amount is at least amount_approval_threshold.\n2. defer if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. deny if duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours.\nMeanings:\n- deny: reject the petition as the action is unauthorized\n- approve: carry on with it now\n- defer: be left pending until the review has been finished\n- ask manager: route it elsewhere because a decider must weigh in\nThe record is complete: nothing else applies.\n\nTaking the facts of the request into account, which action listed should be picked?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q8adebb3fed",
  "kind": "yes/no",
  "text": "invoice_id: INV-2508\nvendor: Redwood Works\namount_approval_threshold: 500.00\npayment_requested_during_business_hours: true\namount: 149.09\npurchase_order_received: true\nduplicate_of_paid_invoice: false\nvendor_tax_form_missing: false\nvendor_free_of_sanctions: false",
  "question": "Proposed action: hold\nDoes the record itself rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q24ff8c559a",
  "kind": "yes/no",
  "text": "---\ninvoice_id: \"INV-5138\"\nvendor: \"Fairview Industries\"\nvendor_tax_form_on_file: true\namount_approval_threshold: 10000.00\nduplicate_of_paid_invoice: true\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: true\npurchase_order_received: true\namount: 7690.03",
  "question": "Proposed action: defer\nBe honest, do the facts here rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if purchase_order_received is false or vendor_tax_form_on_file is false.\n2. ask_manager if amount is above amount_approval_threshold.\n3. deny if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- defer: be kept on hold until more information is supplied\n- deny: scrap the plan and drop this request\n- approve: let this be advanced exactly as originally specified\n- ask_manager: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5e85490b0e",
  "kind": "yes/no",
  "text": "invoice_id | INV-5424\nvendor | Bluepeak Systems\namount_approval_threshold | 10000.00\npurchase_order_received | false\nduplicate_of_paid_invoice | false\nvendor_on_sanctions_list | false\namount | 10000.00\npayment_requested_during_business_hours | true\nvendor_tax_form_on_file | true",
  "question": "Proposed action: PD\nIs the proposed action the right call for this request, as the record shows it?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. PD if purchase_order_received is false or vendor_tax_form_on_file is false.\n2. XWW if amount is above amount_approval_threshold.\n3. FLFH if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: Q.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- XWW: give it to a person who has the authority to decide\n- PD: hold up for a sec until more info comes in\n- FLFH: be blocked outright so it never gets carried out\n- Q: proceed as requested as nothing impedes this course\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2c54d332f4",
  "kind": "yes/no",
  "text": "invoice_id=INV-1364\nvendor=Riverbend Group\nduplicate_of_paid_invoice=false\npayment_requested_during_business_hours=true\nawaiting_purchase_order=false\nvendor_tax_form_on_file=true\namount_approval_threshold=2500.00\namount=1702.33\nvendor_on_sanctions_list=false",
  "question": "Proposed action: reject\nIs it not the case that the proposed action is not a poor choice for this request?",
  "definitions": "Meanings:\n- escalate: be passed along to whoever makes the call\n- hold: defer further action pending verification of the document\n- reject: block the action because it is off limits to the team\n- pay: run with this one\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfc367e2b1c",
  "kind": "yes/no",
  "text": "# case\ninvoice_id: INV-6637\nvendor: Fairview Partners\nawaiting_purchase_order: false\nvendor_on_sanctions_list: false\nvendor_tax_form_missing: false\namount_approval_threshold: 25000.00\namount: 25000.01\npayment_requested_during_business_hours: false\nduplicate_of_paid_invoice: false",
  "question": "Proposed action: GR\nDo the facts of this request support the proposed action as the correct decision?",
  "definitions": "Meanings:\n- QJSC: bin this idea and keep it out of the flow\n- D: pause the request and gather more information before going on\n- XWT: forward the case to the designated decision maker\n- GR: carry it through and the requester is satisfied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8f0550848e",
  "kind": "yes/no",
  "text": "# request record\ninvoice_id: INV-6962\nvendor: Copperfield Works\nduplicate_of_paid_invoice: false\namount_approval_threshold: 5000.00\nvendor_tax_form_on_file: true\npurchase_order_received: true\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: true\namount: 5000.01",
  "question": "Proposed action: hand_to_a_person\nIs the proposed action not what this request calls for?",
  "definitions": "Meanings:\n- hand_to_a_person: get sent upward to the one who decides\n- delay: be held back until a check or document arrives\n- release: have the item pushed forward as the request stated\n- cancel_order: be turned away and treated as off limits\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q05b2457233",
  "kind": "yes/no",
  "text": "---\ncase:\n    invoice_id: \"INV-8722\"\n    vendor: \"Stonebridge Systems\"\nvalues:\n    amount_approval_threshold: 25000.00\n    amount: 9860.78\ntests:\n    payment_requested_during_business_hours: true\n    purchase_order_received: true\n    vendor_free_of_sanctions: true\n    duplicate_of_paid_invoice: false\n    vendor_tax_form_on_file: false",
  "question": "Proposed action: approve\nDo the facts of this request support the proposed action as the correct decision?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qcc55d39fa1",
  "kind": "choice",
  "text": "# record\ninvoice_id | INV-1016\nvendor | Harbor Logistics\npayment_requested_during_business_hours | true\nvendor_free_of_sanctions | true\nduplicate_of_paid_invoice | false\nawaiting_purchase_order | false\namount | 302.86\namount_approval_threshold | 1000.00\nvendor_tax_form_on_file | true",
  "question": "Meanings:\n- L: decline the request as the action is prohibited\n- LVVP: carry out the task as instructed without any obstacle\n- VMH: refer this item to the person who holds decision authority\n- SP: pause the request and gather more information before going on\nThe record is complete: nothing else applies.\n\nLooking across the actions listed, what would be the correct response to this request?",
  "options": [
   "LVVP",
   "L",
   "SP"
  ]
 },
 {
  "qid": "qc208a8e838",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-1864\", \"vendor\": \"Ironleaf Logistics\", \"vendor_tax_form_missing\": false, \"amount\": 563.70, \"purchase_order_received\": true, \"amount_approval_threshold\": 2500.00, \"payment_requested_during_business_hours\": true, \"duplicate_of_paid_invoice\": true, \"vendor_free_of_sanctions\": true}",
  "question": "Meanings:\n- 2: shelve the matter until more details come in\n- 6404: refer the matter to the decision holder\n- 550: continue so the requester receives the result\n- 71: end this effort right away\nThe record is complete: nothing else applies.\n\nWhich of the listed actions do the facts support as the right call?",
  "options": [
   "71",
   "550",
   "6404"
  ]
 },
 {
  "qid": "q8baff48bcc",
  "kind": "yes/no",
  "text": "# request record\ninvoice_id: INV-7845\nvendor: Brightwater Logistics\nduplicate_of_paid_invoice: true\nvendor_tax_form_missing: false\npurchase_order_received: true\nvendor_free_of_sanctions: true\namount: 23959.71\namount_approval_threshold: 25000.00\npayment_requested_during_business_hours: false",
  "question": "Proposed action: release\nIs the proposed action not a sound choice for this situation?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if amount is at least amount_approval_threshold.\n2. delay if purchase_order_received is false or vendor_tax_form_missing is true.\n3. cancel_order if duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- release: proceed and the requester gets what they asked\n- delay: pause this until the requester supplies the missing document\n- cancel_order: be rejected in full and never acted upon\n- hand_to_a_person: be passed along to whoever makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q77d353dab6",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-9445\n  vendor: Copperfield Supply\nvalues:\n  amount: 773.77\n  amount_approval_threshold: 1000.00\ntests:\n  awaiting_purchase_order: false\n  vendor_tax_form_missing: false\n  payment_requested_during_business_hours: true\n  vendor_free_of_sanctions: false\n  duplicate_of_paid_invoice: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. NVG if amount is at least amount_approval_threshold.\n2. TCKG if duplicate_of_paid_invoice is true.\n3. L if vendor_free_of_sanctions is false.\nOtherwise: XB.\nNever counted: awaiting_purchase_order, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- L: route the request to the decision maker\n- NVG: wait until a document arrives before you move forward with it\n- XB: continue with the request as nothing obstructs it\n- TCKG: drop this right there, we are not touching it\nThe record is complete: nothing else applies.\n\nWhich of the actions listed should the team commit to for this request, as the manager?",
  "options": [
   "NVG",
   "XB",
   "TCKG"
  ]
 },
 {
  "qid": "q92a128765d",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-3137\",\"vendor\":\"Pinecrest Foods\",\"payment_requested_during_business_hours\":true,\"purchase_order_received\":true,\"vendor_tax_form_missing\":true,\"vendor_free_of_sanctions\":true,\"amount\":6917.95,\"amount_approval_threshold\":10000.00,\"duplicate_of_paid_invoice\":false}",
  "question": "Proposed action: ask_manager\nIs the proposed action not really the right move for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. deny if vendor_free_of_sanctions is false.\n3. defer if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- deny: cease the operation as it is prohibited\n- defer: hold off until more information arrives\n- ask_manager: bring in the owner who can rule on this\n- approve: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfd7d7ecfc4",
  "kind": "choice",
  "text": "---\n# record\ninvoice_id: \"INV-2294\"\nvendor: \"Cedar Works\"\namount_approval_threshold: 500.00\nvendor_tax_form_on_file: false\namount: 474.31\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: true\npurchase_order_received: true\nvendor_on_sanctions_list: false",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed under the record would the requester see as the right call?",
  "options": [
   "approve",
   "deny",
   "defer"
  ]
 },
 {
  "qid": "q6466ce0a30",
  "kind": "yes/no",
  "text": "---\nmeta:\n  invoice_id: \"INV-7122\"\n  vendor: \"Lakeshore Labs\"\nmetrics:\n  amount: 25000.01\n  amount_approval_threshold: 25000.00\nsignals:\n  payment_requested_during_business_hours: false\n  duplicate_of_paid_invoice: false\n  vendor_tax_form_on_file: true\n  vendor_free_of_sanctions: true\n  purchase_order_received: true",
  "question": "Proposed action: approve\nIs the proposed action not the best thing to do with this?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if vendor_free_of_sanctions is false.\n2. ask manager if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. defer if amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q73137ec942",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-1353\n- vendor: Summit Systems\n- amount approval threshold: 5000.00\n- purchase order received: yes\n- vendor free of sanctions: yes\n- vendor tax form on file: yes\n- amount: 859.00\n- duplicate of paid invoice: no\n- payment requested during business hours: no",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions below answers the request given the facts you can see?",
  "options": [
   "hand_to_a_person",
   "cancel_order",
   "release"
  ]
 },
 {
  "qid": "qbf974b9434",
  "kind": "yes/no",
  "text": "invoice_id: INV-3173\nvendor: Lakeshore Labs\nvendor_free_of_sanctions: false\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: true\nvendor_tax_form_missing: false\nawaiting_purchase_order: false\namount_approval_threshold: 10000.00\namount: 6636.78",
  "question": "Proposed action: hand to a person\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q1178c28cef",
  "kind": "choice",
  "text": "{\n    \"meta\":{\n        \"invoice_id\":\"INV-5500\",\n        \"vendor\":\"Bluepeak Systems\"\n    },\n    \"metrics\":{\n        \"amount_approval_threshold\":1000.00,\n        \"amount\":481.98\n    },\n    \"signals\":{\n        \"payment_requested_during_business_hours\":true,\n        \"awaiting_purchase_order\":false,\n        \"vendor_tax_form_on_file\":true,\n        \"vendor_on_sanctions_list\":false,\n        \"duplicate_of_paid_invoice\":false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. P if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. CPHQ if vendor_on_sanctions_list is true.\n3. HF if awaiting_purchase_order is true.\nOtherwise: GKG.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- P: route the request to the decision maker\n- HF: defer the step until the verification is in\n- CPHQ: toss it out, we are never doing this\n- GKG: push ahead as planned\nThe record is complete: nothing else applies.\n\nChecklist: which of the actions listed below best answers the request?",
  "options": [
   "P",
   "CPHQ",
   "GKG"
  ]
 },
 {
  "qid": "qe97e286d34",
  "kind": "choice",
  "text": "invoice_id: INV-2504\nvendor: Pinecrest Industries\npurchase_order_received: false\nvendor_on_sanctions_list: true\nvendor_tax_form_missing: false\namount: 2178.57\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\namount_approval_threshold: 2500.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if purchase_order_received is false or vendor_tax_form_missing is true.\n2. send_to_a_person if amount is above amount_approval_threshold.\n3. turn_down if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- send_to_a_person: escalate this to the person who decides\n- go_ahead: keep plugging away at it nothing else stands in the way\n- turn_down: decline the request as the action is prohibited\n- put_on_hold: wait for the missing material to come in before deciding anything\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "turn_down",
   "go_ahead",
   "put_on_hold"
  ]
 },
 {
  "qid": "qc7736b0a4e",
  "kind": "choice",
  "text": "# record\ninvoice_id | INV-5114\nvendor | Copperfield Logistics\namount_approval_threshold | 5000.00\nduplicate_of_paid_invoice | false\nvendor_tax_form_missing | true\namount | 5000.00\npurchase_order_received | true\npayment_requested_during_business_hours | true\nvendor_on_sanctions_list | false",
  "question": "Meanings:\n- XCL: wait so the requester can supply more information first\n- RZBJ: drop it right away\n- Z: let this be advanced exactly as originally specified\n- XQ: submit the question to the authorised decision maker\nThe record is complete: nothing else applies.\n\nLooking at what was asked, which of the actions below best fits the request?",
  "options": [
   "Z",
   "RZBJ",
   "XCL"
  ]
 },
 {
  "qid": "q6b64fa6620",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-6799\nvendor = Riverbend Industries\nvendor_on_sanctions_list = false\nvendor_tax_form_missing = false\namount = 7509.63\npayment_requested_during_business_hours = true\namount_approval_threshold = 10000.00\nduplicate_of_paid_invoice = false\nawaiting_purchase_order = true",
  "question": "Proposed action: BQHL\nIs the proposed action not what this request calls for?",
  "definitions": "Meanings:\n- RW: shut off this process completely\n- T: proceed and the requester gets what they asked\n- SXN: submit it upward to the approver\n- BQHL: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q696b6655c4",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"invoice_id\": \"INV-7266\",\n        \"vendor\": \"Lakeshore Works\"\n    },\n    \"values\": {\n        \"amount_approval_threshold\": 5000.00,\n        \"amount\": 3298.80\n    },\n    \"tests\": {\n        \"vendor_free_of_sanctions\": true,\n        \"vendor_tax_form_on_file\": true,\n        \"awaiting_purchase_order\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"duplicate_of_paid_invoice\": false\n    }\n}",
  "question": "Proposed action: hold\nWould the proposed action be considered the correct disposition of the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: drop this right there, we are not touching it\n- hold: wait so the requester can supply more information first\n- pay: execute the request exactly as written\n- escalate: toss it over to the one who makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q264eafb29d",
  "kind": "yes/no",
  "text": "# case\ninvoice_id                              | INV-1980\nvendor                                  | Summit Works\namount_approval_threshold               | 10000.00\namount                                  | 10000.00\nvendor_tax_form_on_file                 | true\npayment_requested_during_business_hours | true\nduplicate_of_paid_invoice               | false\nvendor_on_sanctions_list                | false\nawaiting_purchase_order                 | false",
  "question": "Proposed action: hold\nHonestly, would you say the proposed action is the right move for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_on_sanctions_list is true.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- escalate: submit it upward to the approver\n- hold: chill until the document turns up\n- reject: reject the petition as the action is unauthorized\n- pay: run the task as it was asked, with nothing standing between it and completion\nThe record is complete: nothing else applies."
 }
]
