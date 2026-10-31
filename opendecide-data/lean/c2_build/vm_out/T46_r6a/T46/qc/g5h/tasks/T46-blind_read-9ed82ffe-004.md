# G5-H blind read T46-blind_read-9ed82ffe-004 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r6a/T46/qc/g5h/answers/T46-blind_read-9ed82ffe-004.json

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
  "qid": "q7198185f63",
  "kind": "yes/no",
  "text": "---\ncase:\n    invoice_id: \"INV-8722\"\n    vendor: \"Stonebridge Systems\"\nvalues:\n    amount_approval_threshold: 25000.00\n    amount: 9860.78\ntests:\n    payment_requested_during_business_hours: true\n    purchase_order_received: true\n    vendor_free_of_sanctions: true\n    duplicate_of_paid_invoice: false\n    vendor_tax_form_on_file: true",
  "question": "Proposed action: approve\nSo, have the facts in the record ruled out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qb7e2b43d4c",
  "kind": "yes/no",
  "text": "invoice_id: INV-2508\nvendor: Redwood Works\namount_approval_threshold: 500.00\npayment_requested_during_business_hours: true\namount: 149.09\npurchase_order_received: true\nduplicate_of_paid_invoice: false\nvendor_tax_form_missing: false\nvendor_free_of_sanctions: false",
  "question": "Proposed action: hold\nDoes the record itself rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q233d6b5589",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-8730\n  vendor: Oakmont Systems\nvalues:\n  amount: 8703.88\n  amount_approval_threshold: 10000.00\ntests:\n  purchase_order_received: true\n  payment_requested_during_business_hours: true\n  duplicate_of_paid_invoice: true\n  vendor_free_of_sanctions: true\n  vendor_tax_form_on_file: true",
  "question": "The record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "pay",
   "hold",
   "reject"
  ]
 },
 {
  "qid": "q8eeccda836",
  "kind": "choice",
  "text": "invoice_id: INV-3344\nvendor: Brightwater Group\nawaiting_purchase_order: false\nduplicate_of_paid_invoice: true\namount: 638.33\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: true\namount_approval_threshold: 1000.00\nvendor_tax_form_missing: false",
  "question": "The record is complete: nothing else applies.\n\nWhat is the best action to pick from the list for this request?",
  "options": [
   "delay",
   "cancel order",
   "release"
  ]
 },
 {
  "qid": "q7b3caf6f44",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-3570\n- vendor: Silverline Labs\n- awaiting purchase order: no\n- amount: 25000.00\n- vendor on sanctions list: no\n- duplicate of paid invoice: yes\n- payment requested during business hours: yes\n- vendor tax form on file: yes\n- amount approval threshold: 25000.00",
  "question": "Proposed action: put_on_hold\nDoes the evidence in the record rule out the proposed action as a choice?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q236c3436d5",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id = INV-6613\nvendor = Oakmont Industries\nvendor_on_sanctions_list = false\nvendor_tax_form_on_file = false\nawaiting_purchase_order = false\namount = 5000.00\npayment_requested_during_business_hours = false\namount_approval_threshold = 5000.00\nduplicate_of_paid_invoice = false",
  "question": "Proposed action: go_ahead\nOverall, would you say the proposed action suits the request in the record?",
  "definitions": "Meanings:\n- go_ahead: allow the matter to be taken forward as planned\n- turn_down: end this here and now\n- send_to_a_person: escalate this to someone senior who decides\n- put_on_hold: hold the request so the requester waits for their check\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q13d55f0225",
  "kind": "choice",
  "text": "# record\ninvoice_id=INV-7150\nvendor=Lakeshore Traders\nawaiting_purchase_order=false\namount=2000.87\nduplicate_of_paid_invoice=true\namount_approval_threshold=5000.00\nvendor_tax_form_missing=false\nvendor_on_sanctions_list=true\npayment_requested_during_business_hours=true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. VZFM if amount is at least amount_approval_threshold.\n2. PF if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. K if duplicate_of_paid_invoice is true.\nOtherwise: XVL.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours.\nMeanings:\n- PF: suspend action until the facts are confirmed\n- K: make sure the requester never gets what they wanted\n- XVL: complete the job as it was assigned\n- VZFM: send it up to the person who makes the call\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "XVL",
   "PF",
   "K"
  ]
 },
 {
  "qid": "qbc420f623a",
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
  "qid": "qdce78e1844",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-3016\", \"vendor\": \"Cedar Foods\", \"vendor_on_sanctions_list\": true, \"awaiting_purchase_order\": false, \"amount\": 10000.00, \"payment_requested_during_business_hours\": true, \"duplicate_of_paid_invoice\": false, \"vendor_tax_form_missing\": false, \"amount_approval_threshold\": 10000.00}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. GD if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. NTRK if vendor_on_sanctions_list is true.\n3. P if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: GQP.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- GQP: continue as requested with the path fully open\n- NTRK: decline the request as the action is prohibited\n- P: defer the step until the verification is in\n- GD: send this on to whoever decides\nThe record is complete: nothing else applies.\n\nFrom the actions listed, what should be done with this request?",
  "options": [
   "GD",
   "GQP",
   "NTRK"
  ]
 },
 {
  "qid": "q6cd707bb3e",
  "kind": "choice",
  "text": "# case\ninvoice_id = INV-2254\nvendor = Summit Partners\namount = 500.00\nvendor_tax_form_on_file = true\nduplicate_of_paid_invoice = false\nawaiting_purchase_order = false\nvendor_on_sanctions_list = false\namount_approval_threshold = 500.00\npayment_requested_during_business_hours = true",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "deny",
   "approve",
   "ask_manager"
  ]
 },
 {
  "qid": "q6ab6d35608",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-5605\",\"vendor\":\"Summit Traders\",\"duplicate_of_paid_invoice\":false,\"amount\":794.02,\"vendor_free_of_sanctions\":false,\"vendor_tax_form_missing\":false,\"payment_requested_during_business_hours\":false,\"amount_approval_threshold\":1000.00,\"awaiting_purchase_order\":false}",
  "question": "Proposed action: deny\nIs the proposed action the right move for this request, given the facts involved?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. ask manager if amount is above amount_approval_threshold.\n3. deny if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- deny: shut this down right away, we are staying clear of it\n- ask manager: submit the question to the authorised decision maker\n- approve: have the item pushed forward as the request stated\n- defer: wait for the document to come through\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q426ed968b5",
  "kind": "yes/no",
  "text": "{\n  \"case\": {\n    \"invoice_id\": \"INV-8797\",\n    \"vendor\": \"Cedar Logistics\"\n  },\n  \"values\": {\n    \"amount\": 175.57,\n    \"amount_approval_threshold\": 500.00\n  },\n  \"tests\": {\n    \"vendor_on_sanctions_list\": false,\n    \"payment_requested_during_business_hours\": true,\n    \"awaiting_purchase_order\": true,\n    \"duplicate_of_paid_invoice\": false,\n    \"vendor_tax_form_missing\": false\n  }\n}",
  "question": "Proposed action: 3725\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 9 if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. 842 if vendor_on_sanctions_list is true.\n3. 3725 if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: 58.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 9: give it to a person who has the authority to decide\n- 3725: shelve the matter until more details come in\n- 842: block it right away\n- 58: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q49da1f126d",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-1688\nvendor | Pinecrest Group\nduplicate_of_paid_invoice | false\npurchase_order_received | true\namount | 5817.90\nvendor_tax_form_missing | false\npayment_requested_during_business_hours | true\nvendor_free_of_sanctions | false\namount_approval_threshold | 5000.00",
  "question": "Proposed action: 199\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 199 if amount is above amount_approval_threshold.\n2. 1799 if vendor_free_of_sanctions is false.\n3. 43 if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: 5.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- 1799: make sure the requester never gets what they wanted\n- 199: send this on to whoever decides\n- 43: hold all progress until the requisite documentation arrives\n- 5: execute the request exactly as written\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8fae8e0b49",
  "kind": "yes/no",
  "text": "---\n# record\ninvoice_id: \"INV-7182\"\nvendor: \"Brightwater Foods\"\namount_approval_threshold: 5000.00\nvendor_tax_form_missing: false\npayment_requested_during_business_hours: true\namount: 8404.14\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: false\npurchase_order_received: true",
  "question": "Proposed action: send to a person\nDoes the record's evidence rule out the proposed action as the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if amount is above amount_approval_threshold.\n2. turn down if vendor_on_sanctions_list is true.\n3. put on hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: go ahead.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- go ahead: carry out the request as written\n- turn down: halt the request at this point\n- send to a person: route the request to the decision maker\n- put on hold: hold up for a sec until more info comes in\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcd05099fca",
  "kind": "choice",
  "text": "invoice_id: INV-7333\nvendor: Ironleaf Partners\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: true\namount: 25000.01\nvendor_tax_form_on_file: true\namount_approval_threshold: 25000.00\npurchase_order_received: true\nvendor_free_of_sanctions: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn_down if vendor_free_of_sanctions is false.\n3. put_on_hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- send_to_a_person: hand it up to the person who decides\n- turn_down: shut this down before it spreads into the workflow\n- put_on_hold: withhold action until supporting information is supplied\n- go_ahead: proceed and the requester gets what they asked\nThe record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "send_to_a_person",
   "turn_down",
   "put_on_hold"
  ]
 },
 {
  "qid": "q7b983f8ae8",
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
  "qid": "q26cc86b887",
  "kind": "choice",
  "text": "# record\ninvoice_id | INV-9020\nvendor | Lakeshore Industries\namount_approval_threshold | 500.00\nduplicate_of_paid_invoice | false\npayment_requested_during_business_hours | false\namount | 500.01\nvendor_on_sanctions_list | false\nawaiting_purchase_order | false\nvendor_tax_form_on_file | true",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed should the team commit to for this request, as the manager?",
  "options": [
   "go ahead",
   "send to a person",
   "turn down"
  ]
 },
 {
  "qid": "qc4647f6c19",
  "kind": "choice",
  "text": "# record\ninvoice_id=INV-9632\nvendor=Northwind Systems\npayment_requested_during_business_hours=false\namount=13608.87\nduplicate_of_paid_invoice=false\nawaiting_purchase_order=false\nvendor_tax_form_missing=false\namount_approval_threshold=25000.00\nvendor_on_sanctions_list=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. ask_manager if amount is above amount_approval_threshold.\n3. deny if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "ask_manager",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q039b246905",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-1597\nvendor | Summit Systems\nvendor_free_of_sanctions | false\namount_approval_threshold | 2500.00\nawaiting_purchase_order | false\nvendor_tax_form_missing | false\npayment_requested_during_business_hours | true\namount | 2475.83\nduplicate_of_paid_invoice | false",
  "question": "Proposed action: delay\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if amount is at least amount_approval_threshold.\n2. cancel order if duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_free_of_sanctions is false.\nOtherwise: release.\nNever counted: awaiting_purchase_order, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- release: finish what was asked as stated, the way ahead is fully free\n- delay: wait for the document to come through\n- hand to a person: forward it to the decision maker\n- cancel order: refuse the request because it crosses a clear line\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q21e1ae3a35",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-8225\n- vendor: Riverbend Partners\n- awaiting purchase order: no\n- duplicate of paid invoice: no\n- amount: 25000.00\n- amount approval threshold: 25000.00\n- payment requested during business hours: no\n- vendor free of sanctions: yes\n- vendor tax form missing: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if awaiting_purchase_order is true.\n2. turn_down if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. send_to_a_person if vendor_tax_form_missing is true or amount is above amount_approval_threshold.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nGiven what the requester needs, which of the actions below should be taken?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "turn_down"
  ]
 },
 {
  "qid": "q8c8ea15463",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-3740\", \"vendor\": \"Oakmont Labs\", \"vendor_on_sanctions_list\": false, \"duplicate_of_paid_invoice\": false, \"amount_approval_threshold\": 2500.00, \"amount\": 2063.18, \"purchase_order_received\": true, \"payment_requested_during_business_hours\": true, \"vendor_tax_form_on_file\": true}",
  "question": "Proposed action: cancel order\nIs the proposed action not what should happen with this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand to a person if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel order if vendor_on_sanctions_list is true.\n3. delay if purchase_order_received is false.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe417c45ba4",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id                              | INV-3141\nvendor                                  | Harbor Supply\npurchase_order_received                 | true\nvendor_tax_form_missing                 | false\nvendor_free_of_sanctions                | false\nduplicate_of_paid_invoice               | false\namount_approval_threshold               | 10000.00\npayment_requested_during_business_hours | true\namount                                  | 4469.79",
  "question": "Proposed action: cancel_order\nIs it not so that the proposed action is not mistaken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel_order if vendor_free_of_sanctions is false.\n2. hand_to_a_person if purchase_order_received is false or vendor_tax_form_missing is true.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2162798dd1",
  "kind": "choice",
  "text": "# case\ninvoice_id: INV-9145\nvendor: Ironleaf Systems\nvendor_tax_form_missing: false\namount_approval_threshold: 1000.00\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\namount: 231.45\nvendor_on_sanctions_list: false\nawaiting_purchase_order: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn_down if vendor_on_sanctions_list is true.\n3. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- send_to_a_person: hand this over to whoever has the final say\n- put_on_hold: wait for the check and the requester will hear back later\n- turn_down: drop this right there, we are not touching it\n- go_ahead: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies.\n\nAs the team lead, which of the actions listed should we go with for this request?",
  "options": [
   "send_to_a_person",
   "turn_down",
   "go_ahead"
  ]
 },
 {
  "qid": "q2f0aea480c",
  "kind": "choice",
  "text": "{\n    \"request\":{\n        \"invoice_id\":\"INV-4590\",\n        \"vendor\":\"Silverline Systems\"\n    },\n    \"figures\":{\n        \"amount\":1874.29,\n        \"amount_approval_threshold\":2500.00\n    },\n    \"checks\":{\n        \"vendor_tax_form_on_file\":true,\n        \"duplicate_of_paid_invoice\":false,\n        \"payment_requested_during_business_hours\":true,\n        \"awaiting_purchase_order\":false,\n        \"vendor_free_of_sanctions\":true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n2. hand to a person if amount is above amount_approval_threshold.\n3. cancel order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed would be the right call for the matter in this file?",
  "options": [
   "delay",
   "hand to a person",
   "release"
  ]
 },
 {
  "qid": "q467f747118",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-8936\", \"vendor\": \"Brightwater Traders\", \"vendor_free_of_sanctions\": true, \"duplicate_of_paid_invoice\": true, \"awaiting_purchase_order\": false, \"amount\": 3493.86, \"vendor_tax_form_on_file\": true, \"payment_requested_during_business_hours\": false, \"amount_approval_threshold\": 10000.00}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 66 if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. 627 if vendor_free_of_sanctions is false.\n3. 6 if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: 7111.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 7111: complete the job as it was assigned\n- 6: stay put until the check is finished\n- 627: make sure the requester never gets what they wanted\n- 66: get sent upward to the one who decides\nThe record is complete: nothing else applies.\n\nAuditing the request, which of the actions below is the defensible choice?",
  "options": [
   "627",
   "7111",
   "66"
  ]
 },
 {
  "qid": "q91d514b81f",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-6664\", \"vendor\": \"Bluepeak Partners\", \"vendor_tax_form_on_file\": true, \"amount_approval_threshold\": 5000.00, \"amount\": 5000.00, \"duplicate_of_paid_invoice\": false, \"vendor_free_of_sanctions\": false, \"awaiting_purchase_order\": false, \"payment_requested_during_business_hours\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel_order if vendor_free_of_sanctions is false.\n2. hand_to_a_person if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "cancel_order",
   "hand_to_a_person",
   "release"
  ]
 },
 {
  "qid": "qe6e91bbd42",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-9761\n- vendor: Fairview Logistics\n- amount: 1296.30\n- amount approval threshold: 2500.00\n- payment requested during business hours: yes\n- duplicate of paid invoice: no\n- awaiting purchase order: yes\n- vendor tax form on file: yes\n- vendor free of sanctions: no",
  "question": "Proposed action: deny\nIs it not so that the proposed action is not mistaken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. deny if vendor_free_of_sanctions is false.\n3. defer if awaiting_purchase_order is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- approve: execute the request exactly as written\n- ask_manager: send it up so the requester gets a firm decision\n- defer: park the file until the requester sends the document in\n- deny: drop it right away\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe425d2103a",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id = INV-7530\nvendor = Bluepeak Systems\nvendor_tax_form_on_file = true\namount_approval_threshold = 25000.00\npurchase_order_received = true\nduplicate_of_paid_invoice = false\namount = 20256.62\npayment_requested_during_business_hours = false\nvendor_free_of_sanctions = true",
  "question": "Proposed action: pay\nWould what the record shows make the proposed action the right call here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: bin this idea and keep it out of the flow\n- hold: pump the brakes until more details show up\n- escalate: send it up so the requester gets a firm decision\n- pay: go on and finish it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc54c1b9b01",
  "kind": "choice",
  "text": "{\n  \"subject\":{\n    \"invoice_id\":\"INV-6623\",\n    \"vendor\":\"Ironleaf Industries\"\n  },\n  \"amounts\":{\n    \"amount\":3982.57,\n    \"amount_approval_threshold\":5000.00\n  },\n  \"checks\":{\n    \"vendor_tax_form_missing\":false,\n    \"payment_requested_during_business_hours\":false,\n    \"purchase_order_received\":true,\n    \"duplicate_of_paid_invoice\":false,\n    \"vendor_free_of_sanctions\":true\n  }\n}",
  "question": "Meanings:\n- escalate: hand it up to the person who decides\n- pay: continue so the requester receives the result\n- hold: keep their request on hold until more information arrives from them\n- reject: shut this down right away, we are staying clear of it\nThe record is complete: nothing else applies.\n\nIf you were deciding, which of the actions listed after this fits best?",
  "options": [
   "escalate",
   "reject",
   "pay"
  ]
 },
 {
  "qid": "q30555436ed",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-1502\n  vendor: Cedar Labs\nvalues:\n  amount_approval_threshold: 5000.00\n  amount: 3940.54\ntests:\n  purchase_order_received: true\n  vendor_free_of_sanctions: true\n  payment_requested_during_business_hours: false\n  duplicate_of_paid_invoice: false\n  vendor_tax_form_missing: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is at least amount_approval_threshold.\n2. hold if purchase_order_received is false or vendor_tax_form_missing is true.\n3. reject if duplicate_of_paid_invoice is true.\nOtherwise: pay.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "hold",
   "escalate",
   "pay"
  ]
 },
 {
  "qid": "q257e4dd7d9",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-3137\",\"vendor\":\"Pinecrest Foods\",\"payment_requested_during_business_hours\":true,\"purchase_order_received\":true,\"vendor_tax_form_missing\":true,\"vendor_free_of_sanctions\":true,\"amount\":6917.95,\"amount_approval_threshold\":10000.00,\"duplicate_of_paid_invoice\":false}",
  "question": "Proposed action: ask_manager\nIs the proposed action not really the right move for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. deny if vendor_free_of_sanctions is false.\n3. defer if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- deny: cease the operation as it is prohibited\n- defer: hold off until more information arrives\n- ask_manager: bring in the owner who can rule on this\n- approve: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7738b7e14c",
  "kind": "yes/no",
  "text": "{\n  \"meta\":{\n    \"invoice_id\":\"INV-9197\",\n    \"vendor\":\"Copperfield Logistics\"\n  },\n  \"metrics\":{\n    \"amount_approval_threshold\":2500.00,\n    \"amount\":4049.50\n  },\n  \"signals\":{\n    \"vendor_on_sanctions_list\":false,\n    \"duplicate_of_paid_invoice\":true,\n    \"vendor_tax_form_missing\":false,\n    \"purchase_order_received\":true,\n    \"payment_requested_during_business_hours\":true\n  }\n}",
  "question": "Proposed action: cancel_order\nBased on the record, can it be said the proposed action is not the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel_order if vendor_on_sanctions_list is true.\n2. hand_to_a_person if purchase_order_received is false or vendor_tax_form_missing is true.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7e75153a73",
  "kind": "choice",
  "text": "---\n# record\nmeta:\n    invoice_id: \"INV-5775\"\n    vendor: \"Oakmont Systems\"\nmetrics:\n    amount_approval_threshold: 500.00\n    amount: 606.94\nsignals:\n    vendor_free_of_sanctions: true\n    duplicate_of_paid_invoice: false\n    vendor_tax_form_missing: false\n    payment_requested_during_business_hours: true\n    awaiting_purchase_order: false",
  "question": "Meanings:\n- approve: keep moving on this one nothing is holding it up\n- deny: be rejected in full and never acted upon\n- ask manager: delegate the call to whoever holds authority\n- defer: sit on it till the doc shows up\nThe record is complete: nothing else applies.\n\nMind telling me which of the actions below is the best call for this request?",
  "options": [
   "ask manager",
   "defer",
   "deny"
  ]
 },
 {
  "qid": "q7ebee52446",
  "kind": "yes/no",
  "text": "invoice_id: INV-1393\nvendor: Bluepeak Works\npurchase_order_received: true\namount: 2500.00\nvendor_tax_form_on_file: true\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: false\namount_approval_threshold: 2500.00\nvendor_on_sanctions_list: true",
  "question": "Proposed action: reject\nIs it not so that the proposed action is not mistaken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\n2. escalate if amount is above amount_approval_threshold.\n3. reject if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qeebb290064",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-6445\n- vendor: Summit Logistics\n- payment requested during business hours: yes\n- vendor tax form on file: yes\n- vendor on sanctions list: no\n- duplicate of paid invoice: yes\n- amount approval threshold: 1000.00\n- awaiting purchase order: no\n- amount: 314.90",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "deny",
   "ask_manager",
   "approve"
  ]
 },
 {
  "qid": "qb5bb03b3fb",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-4979\nvendor | Pinecrest Foods\nduplicate_of_paid_invoice | false\npayment_requested_during_business_hours | true\nvendor_on_sanctions_list | false\nawaiting_purchase_order | false\namount_approval_threshold | 25000.00\namount | 5785.90\nvendor_tax_form_missing | false",
  "question": "Proposed action: release\nHonestly, would you say the proposed action is the right move for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q7d56f23505",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-5648\",\"vendor\":\"Harbor Industries\",\"vendor_tax_form_missing\":true,\"vendor_on_sanctions_list\":false,\"awaiting_purchase_order\":false,\"amount\":1717.54,\"payment_requested_during_business_hours\":true,\"duplicate_of_paid_invoice\":false,\"amount_approval_threshold\":2500.00}",
  "question": "Proposed action: hold\nDoes the proposed action not fit what this request needs?",
  "definitions": "Meanings:\n- escalate: route this to the one who signs off\n- hold: wait for the document before going further\n- reject: terminate the process as continuation is prohibited\n- pay: keep moving so the asker gets the outcome\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2d990ff9bc",
  "kind": "choice",
  "text": "invoice_id | INV-4500\nvendor | Harbor Logistics\namount_approval_threshold | 2500.00\nvendor_on_sanctions_list | true\npurchase_order_received | false\npayment_requested_during_business_hours | true\namount | 749.64\nvendor_tax_form_missing | false\nduplicate_of_paid_invoice | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 700 if vendor_tax_form_missing is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. 80 if vendor_on_sanctions_list is true.\n3. 1 if purchase_order_received is false.\nOtherwise: 4196.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 80: reject this item since it violates the policy\n- 1: hold all progress until the requisite documentation arrives\n- 4196: run the requested step through\n- 700: delegate the call to whoever holds authority\nThe record is complete: nothing else applies.\n\nAs the manager, which of the actions listed is the right call for this request?",
  "options": [
   "700",
   "4196",
   "80"
  ]
 },
 {
  "qid": "q1d0c1d0b3b",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-8850\nvendor = Bluepeak Works\npayment_requested_during_business_hours = true\nduplicate_of_paid_invoice = false\nvendor_tax_form_on_file = true\nvendor_on_sanctions_list = false\namount = 4584.60\nawaiting_purchase_order = false\namount_approval_threshold = 10000.00",
  "question": "Proposed action: pay\nIs the proposed action not really the right move for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is at least amount_approval_threshold.\n2. hold if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. reject if duplicate_of_paid_invoice is true.\nOtherwise: pay.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours.\nMeanings:\n- reject: stop the request so the requester gets nothing from it\n- pay: carry out the request as written\n- escalate: send it onward because someone else must decide\n- hold: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe4d7e16e2a",
  "kind": "choice",
  "text": "# request record\ninvoice_id: INV-1485\nvendor: Harbor Supply\nvendor_on_sanctions_list: true\namount: 707.76\nawaiting_purchase_order: false\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: true\namount_approval_threshold: 1000.00\nvendor_tax_form_missing: false",
  "question": "Meanings:\n- hand_to_a_person: delegate the call to whoever holds authority\n- cancel_order: toss it out, we are never doing this\n- release: execute the requested action as nothing prevents it\n- delay: be parked until a verification has been logged\nThe record is complete: nothing else applies.\n\nThe record shows the situation; which of the actions listed is the right call?",
  "options": [
   "cancel_order",
   "delay",
   "release"
  ]
 },
 {
  "qid": "qd8893a59dc",
  "kind": "choice",
  "text": "{\n    \"record\":{\n        \"invoice_id\":\"INV-2865\",\n        \"vendor\":\"Stonebridge Supply\"\n    },\n    \"numbers\":{\n        \"amount\":8945.12,\n        \"amount_approval_threshold\":10000.00\n    },\n    \"flags\":{\n        \"duplicate_of_paid_invoice\":false,\n        \"payment_requested_during_business_hours\":false,\n        \"vendor_tax_form_missing\":false,\n        \"vendor_free_of_sanctions\":true,\n        \"awaiting_purchase_order\":true\n    }\n}",
  "question": "Meanings:\n- 981: freeze progress until the paperwork arrives\n- 9542: proceed as requested as nothing impedes this course\n- 41: drop this right there, we are not touching it\n- 5: forward it to the decision maker\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "5",
   "9542",
   "981"
  ]
 },
 {
  "qid": "q0c7c2bc85b",
  "kind": "yes/no",
  "text": "{\n    \"record\":{\n        \"invoice_id\":\"INV-6648\",\n        \"vendor\":\"Redwood Group\"\n    },\n    \"numbers\":{\n        \"amount_approval_threshold\":500.00,\n        \"amount\":231.55\n    },\n    \"flags\":{\n        \"duplicate_of_paid_invoice\":false,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_free_of_sanctions\":false,\n        \"purchase_order_received\":true,\n        \"vendor_tax_form_on_file\":false\n    }\n}",
  "question": "Proposed action: reject\nGiven the request and the facts, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: shut this down right away, we are staying clear of it\n- escalate: hand this over to whoever has the final say\n- hold: chill until the document turns up\n- pay: proceed and the requester gets what they asked\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe0c4699ced",
  "kind": "choice",
  "text": "# record\ninvoice_id: INV-6807\nvendor: Copperfield Industries\npayment_requested_during_business_hours: false\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: true\namount_approval_threshold: 2500.00\namount: 2262.07\npurchase_order_received: true\nvendor_tax_form_missing: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. VD if amount is above amount_approval_threshold.\n2. KSWZ if vendor_on_sanctions_list is true.\n3. SBX if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: G.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- G: carry out the task as instructed without any obstacle\n- VD: send it up to the person who makes the call\n- KSWZ: drop it right away\n- SBX: hold off until the check clears\nThe record is complete: nothing else applies.\n\nTaking the actions listed into account, what is the right call for the request?",
  "options": [
   "VD",
   "KSWZ",
   "G"
  ]
 },
 {
  "qid": "qea905c18d0",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-8725\", \"vendor\": \"Bluepeak Partners\", \"amount_approval_threshold\": 25000.00, \"duplicate_of_paid_invoice\": false, \"purchase_order_received\": true, \"vendor_on_sanctions_list\": false, \"payment_requested_during_business_hours\": true, \"vendor_tax_form_on_file\": true, \"amount\": 7983.70}",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "reject",
   "hold",
   "pay"
  ]
 },
 {
  "qid": "q87a5e6dc9d",
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
  "qid": "q4706caeb74",
  "kind": "yes/no",
  "text": "invoice_id=INV-6875\nvendor=Lakeshore Supply\nawaiting_purchase_order=true\nvendor_free_of_sanctions=true\nvendor_tax_form_missing=false\nduplicate_of_paid_invoice=false\namount=1202.72\npayment_requested_during_business_hours=true\namount_approval_threshold=5000.00",
  "question": "Proposed action: go_ahead\nQuick check: do the facts in the record rule out the proposed action here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn_down if vendor_free_of_sanctions is false.\n3. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q409b8567aa",
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
  "qid": "q90fc245257",
  "kind": "choice",
  "text": "invoice_id: INV-1927\nvendor: Stonebridge Partners\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\nvendor_tax_form_on_file: true\namount: 4537.96\nvendor_on_sanctions_list: false\npurchase_order_received: true\namount_approval_threshold: 10000.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "escalate",
   "pay",
   "hold"
  ]
 },
 {
  "qid": "q38a57740d2",
  "kind": "choice",
  "text": "{\n  \"request\": {\n    \"invoice_id\": \"INV-3233\",\n    \"vendor\": \"Fairview Logistics\"\n  },\n  \"figures\": {\n    \"amount\": 1460.29,\n    \"amount_approval_threshold\": 10000.00\n  },\n  \"checks\": {\n    \"awaiting_purchase_order\": false,\n    \"vendor_on_sanctions_list\": false,\n    \"payment_requested_during_business_hours\": true,\n    \"duplicate_of_paid_invoice\": false,\n    \"vendor_tax_form_missing\": false\n  }\n}",
  "question": "Meanings:\n- QQT: allow the matter to be taken forward as planned\n- PCRB: route this matter to the individual empowered to decide\n- X: pump the brakes until more details show up\n- BJ: stop the work since it cannot move forward\nThe record is complete: nothing else applies.\n\nHey, which of the actions listed after this question is the right call here?",
  "options": [
   "PCRB",
   "QQT",
   "BJ"
  ]
 },
 {
  "qid": "q2ec6fd8e6d",
  "kind": "choice",
  "text": "{\n  \"subject\": {\n    \"invoice_id\": \"INV-6442\",\n    \"vendor\": \"Riverbend Traders\"\n  },\n  \"amounts\": {\n    \"amount_approval_threshold\": 5000.00,\n    \"amount\": 6465.60\n  },\n  \"checks\": {\n    \"purchase_order_received\": false,\n    \"vendor_tax_form_missing\": false,\n    \"vendor_free_of_sanctions\": false,\n    \"payment_requested_during_business_hours\": true,\n    \"duplicate_of_paid_invoice\": false\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 329 if amount is at least amount_approval_threshold.\n2. 8027 if duplicate_of_paid_invoice is true.\n3. 3 if vendor_free_of_sanctions is false.\nOtherwise: 18.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- 8027: end this here and now\n- 18: keep going with it\n- 329: keep it on hold for the missing document\n- 3: toss it over to the one who makes the call\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "8027",
   "18",
   "329"
  ]
 }
]
