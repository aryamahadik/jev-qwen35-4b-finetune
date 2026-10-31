# G5-H blind read T46-blind_read-05dcb4b4-003 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r6a/T46/qc/g5h/answers/T46-blind_read-05dcb4b4-003.json

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
  "qid": "q421419be5d",
  "kind": "yes/no",
  "text": "{\n  \"meta\":{\n    \"invoice_id\":\"INV-9197\",\n    \"vendor\":\"Copperfield Logistics\"\n  },\n  \"metrics\":{\n    \"amount_approval_threshold\":2500.00,\n    \"amount\":4049.50\n  },\n  \"signals\":{\n    \"vendor_on_sanctions_list\":false,\n    \"duplicate_of_paid_invoice\":true,\n    \"vendor_tax_form_missing\":false,\n    \"purchase_order_received\":true,\n    \"payment_requested_during_business_hours\":true\n  }\n}",
  "question": "Proposed action: cancel_order\nBased on the record, can it be said the proposed action is not the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel_order if vendor_on_sanctions_list is true.\n2. hand_to_a_person if purchase_order_received is false or vendor_tax_form_missing is true.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qed560d12d1",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-8190\n- vendor: Summit Group\n- awaiting purchase order: no\n- vendor on sanctions list: yes\n- amount: 274.11\n- payment requested during business hours: yes\n- vendor tax form on file: yes\n- duplicate of paid invoice: no\n- amount approval threshold: 500.00",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed after this is the most suitable for the request?",
  "options": [
   "put on hold",
   "go ahead",
   "turn down"
  ]
 },
 {
  "qid": "qf7899ea792",
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
  "qid": "qc689b214e5",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-5054\", \"vendor\": \"Stonebridge Group\", \"payment_requested_during_business_hours\": true, \"amount\": 10000.01, \"vendor_free_of_sanctions\": true, \"awaiting_purchase_order\": false, \"duplicate_of_paid_invoice\": false, \"amount_approval_threshold\": 10000.00, \"vendor_tax_form_missing\": false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if awaiting_purchase_order is true.\n2. turn_down if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. send_to_a_person if vendor_tax_form_missing is true or amount is above amount_approval_threshold.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- send_to_a_person: direct the request to the responsible decider\n- go_ahead: keep it moving forward\n- put_on_hold: hold the request so the requester waits for their check\n- turn_down: make sure the requester never gets what they wanted\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "put_on_hold",
   "send_to_a_person",
   "go_ahead"
  ]
 },
 {
  "qid": "q31680cca91",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-2121\", \"vendor\": \"Silverline Partners\", \"duplicate_of_paid_invoice\": false, \"amount_approval_threshold\": 2500.00, \"vendor_tax_form_missing\": false, \"payment_requested_during_business_hours\": true, \"amount\": 567.36, \"awaiting_purchase_order\": false, \"vendor_free_of_sanctions\": false}",
  "question": "Proposed action: release\nIs it not so that the proposed action is not off base for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if amount is above amount_approval_threshold.\n2. cancel_order if vendor_free_of_sanctions is false.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa59c1cca11",
  "kind": "yes/no",
  "text": "---\n# record\ninvoice_id: \"INV-8807\"\nvendor: \"Riverbend Foods\"\nawaiting_purchase_order: false\nvendor_on_sanctions_list: true\namount: 5714.95\nduplicate_of_paid_invoice: false\nvendor_tax_form_missing: false\namount_approval_threshold: 10000.00\npayment_requested_during_business_hours: true",
  "question": "Proposed action: go ahead\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- put on hold: hold the request so the requester waits for their check\n- send to a person: route the request to the decision maker\n- turn down: end it so the requester sees their request closed\n- go ahead: keep plugging away at it nothing else stands in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5c8bc2ac48",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\": \"INV-1173\",\n  \"vendor\": \"Redwood Group\",\n  \"duplicate_of_paid_invoice\": false,\n  \"amount_approval_threshold\": 25000.00,\n  \"vendor_free_of_sanctions\": true,\n  \"amount\": 18563.42,\n  \"awaiting_purchase_order\": false,\n  \"vendor_tax_form_missing\": false,\n  \"payment_requested_during_business_hours\": true\n}",
  "question": "Proposed action: approve\nIs the proposed action the right move for this request, given the facts involved?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if amount is above amount_approval_threshold.\n2. deny if vendor_free_of_sanctions is false.\n3. defer if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9621320a09",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n  invoice_id: \"INV-8212\"\n  vendor: \"Ironleaf Group\"\namounts:\n  amount_approval_threshold: 5000.00\n  amount: 4520.76\nchecks:\n  purchase_order_received: true\n  vendor_on_sanctions_list: false\n  duplicate_of_paid_invoice: true\n  vendor_tax_form_missing: false\n  payment_requested_during_business_hours: true",
  "question": "The record is complete: nothing else applies.\n\nAs the team lead, which of the actions listed should we go with for this request?",
  "options": [
   "pay",
   "escalate",
   "reject"
  ]
 },
 {
  "qid": "q68a0158c4c",
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
  "qid": "q124ce292ad",
  "kind": "yes/no",
  "text": "---\n# case\nsubject:\n  invoice_id: \"INV-3180\"\n  vendor: \"Harbor Labs\"\namounts:\n  amount_approval_threshold: 1000.00\n  amount: 993.93\nchecks:\n  purchase_order_received: true\n  payment_requested_during_business_hours: true\n  vendor_tax_form_missing: false\n  vendor_on_sanctions_list: false\n  duplicate_of_paid_invoice: false",
  "question": "Proposed action: delay\nIs it not the case that the proposed action is not a poor choice for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel_order if vendor_on_sanctions_list is true.\n3. delay if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- hand_to_a_person: bring in the owner who can rule on this\n- release: push ahead as planned\n- delay: shelve the matter until more details come in\n- cancel_order: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q075284c3f1",
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
  "qid": "qd8c67e7cc7",
  "kind": "choice",
  "text": "{\n    \"record\":{\n        \"invoice_id\":\"INV-8031\",\n        \"vendor\":\"Cedar Logistics\"\n    },\n    \"numbers\":{\n        \"amount\":768.76,\n        \"amount_approval_threshold\":2500.00\n    },\n    \"flags\":{\n        \"vendor_tax_form_on_file\":true,\n        \"duplicate_of_paid_invoice\":false,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_free_of_sanctions\":false,\n        \"awaiting_purchase_order\":false\n    }\n}",
  "question": "Meanings:\n- 591: execute the request exactly as written\n- 1186: be forwarded to the person in charge\n- 64: stop this course of action at once\n- 5: pause the request and gather more information before going on\nThe record is complete: nothing else applies.\n\nReviewing this file as an auditor, which action below would you say is correct?",
  "options": [
   "1186",
   "64",
   "591"
  ]
 },
 {
  "qid": "q79e0cd1b44",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-5281\nvendor = Cedar Industries\namount_approval_threshold = 25000.00\npayment_requested_during_business_hours = true\nvendor_tax_form_on_file = true\nvendor_on_sanctions_list = false\namount = 25000.00\nawaiting_purchase_order = true\nduplicate_of_paid_invoice = false",
  "question": "Proposed action: approve\nIs the proposed action not the right move, given what the record shows?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n2. ask manager if amount is above amount_approval_threshold.\n3. deny if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- ask manager: route this matter to the individual empowered to decide\n- approve: go ahead and the requester will be served\n- defer: defer the step until the verification is in\n- deny: be stopped and never carried out\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfbc91db3fd",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-9237\n- vendor: Lakeshore Logistics\n- vendor tax form on file: yes\n- payment requested during business hours: yes\n- amount: 801.06\n- vendor free of sanctions: yes\n- purchase order received: yes\n- duplicate of paid invoice: yes\n- amount approval threshold: 500.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if amount is at least amount_approval_threshold.\n2. defer if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. deny if duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- approve: proceed with the request since the way is clear and nothing blocks it\n- defer: hold the request until a check is completed\n- ask manager: be forwarded to the person in charge\n- deny: refuse this request entirely\nThe record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "ask manager",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q4d9c91a8ac",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-3110\n- vendor: Summit Labs\n- duplicate of paid invoice: yes\n- amount: 6275.76\n- vendor tax form on file: no\n- payment requested during business hours: yes\n- vendor on sanctions list: no\n- purchase order received: yes\n- amount approval threshold: 10000.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 9696 if purchase_order_received is false.\n2. 495 if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. 91 if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: 1.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 1: advance the task as stated without any blockers\n- 91: forward the matter as the call rests with someone higher\n- 9696: hold the request until a check is completed\n- 495: be rejected in full and never acted upon\nThe record is complete: nothing else applies.\n\nHey, which of the actions listed after this question is the right call here?",
  "options": [
   "495",
   "1",
   "91"
  ]
 },
 {
  "qid": "q7f9379b531",
  "kind": "choice",
  "text": "{\n  \"meta\":{\n    \"invoice_id\":\"INV-6445\",\n    \"vendor\":\"Summit Logistics\"\n  },\n  \"metrics\":{\n    \"amount\":314.90,\n    \"amount_approval_threshold\":1000.00\n  },\n  \"signals\":{\n    \"vendor_on_sanctions_list\":false,\n    \"awaiting_purchase_order\":false,\n    \"duplicate_of_paid_invoice\":true,\n    \"payment_requested_during_business_hours\":true,\n    \"vendor_tax_form_on_file\":true\n  }\n}",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "deny",
   "ask_manager",
   "approve"
  ]
 },
 {
  "qid": "q912adf2556",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-2880\nvendor=Riverbend Labs\npurchase_order_received=true\namount=412.43\npayment_requested_during_business_hours=false\nvendor_tax_form_on_file=true\nduplicate_of_paid_invoice=true\nvendor_on_sanctions_list=true\namount_approval_threshold=1000.00",
  "question": "Proposed action: HDW\nSo, have the facts in the record ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. HDW if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. LB if vendor_on_sanctions_list is true.\n3. L if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: XNNS.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- LB: kill this one off, it is off the table for good\n- XNNS: have the plan kept moving as it was requested\n- HDW: be forwarded to the person in charge\n- L: pause and collect more information first\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q30187857a6",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n* invoice id: INV-4763\n* vendor: Ironleaf Logistics\n* vendor tax form on file: yes\n* amount approval threshold: 25000.00\n* payment requested during business hours: yes\n* purchase order received: yes\n* vendor on sanctions list: no\n* amount: 23131.63\n* duplicate of paid invoice: yes",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if purchase_order_received is false.\n2. reject if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. escalate if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: shut this down before it spreads into the workflow\n- hold: pause the request and gather more information before going on\n- pay: complete the action that was asked for\n- escalate: pass the request to a decider\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "pay",
   "reject",
   "hold"
  ]
 },
 {
  "qid": "qcde4641e8d",
  "kind": "choice",
  "text": "---\nrequest:\n    invoice_id: INV-4200\n    vendor: Redwood Group\nfigures:\n    amount: 2500.00\n    amount_approval_threshold: 2500.00\nchecks:\n    awaiting_purchase_order: false\n    payment_requested_during_business_hours: true\n    duplicate_of_paid_invoice: false\n    vendor_free_of_sanctions: false\n    vendor_tax_form_missing: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if awaiting_purchase_order is true.\n2. deny if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. ask manager if vendor_tax_form_missing is true or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nQuick question: which of the actions listed after this is the best call?",
  "options": [
   "ask manager",
   "deny",
   "approve"
  ]
 },
 {
  "qid": "q920aa43624",
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
  "qid": "qd25ee3bce6",
  "kind": "choice",
  "text": "{\n    \"invoice_id\": \"INV-8163\",\n    \"vendor\": \"Redwood Group\",\n    \"payment_requested_during_business_hours\": false,\n    \"vendor_free_of_sanctions\": true,\n    \"amount_approval_threshold\": 25000.00,\n    \"amount\": 18723.52,\n    \"vendor_tax_form_on_file\": true,\n    \"duplicate_of_paid_invoice\": false,\n    \"awaiting_purchase_order\": true\n}",
  "question": "Meanings:\n- hand_to_a_person: route it elsewhere because a decider must weigh in\n- cancel_order: shut this down right away, we are staying clear of it\n- release: have the plan kept moving as it was requested\n- delay: freeze progress until the paperwork arrives\nThe record is complete: nothing else applies.\n\nThe facts point somewhere; which of the actions shown is supported by them?",
  "options": [
   "cancel_order",
   "release",
   "delay"
  ]
 },
 {
  "qid": "q9afc4710ef",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-5648\n- vendor: Summit Labs\n- vendor on sanctions list: no\n- amount approval threshold: 10000.00\n- vendor tax form on file: yes\n- amount: 4361.67\n- awaiting purchase order: no\n- duplicate of paid invoice: no\n- payment requested during business hours: no",
  "question": "Proposed action: hand to a person\nIs it not so that the proposed action is not mistaken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand to a person if amount is above amount_approval_threshold.\n2. cancel order if vendor_on_sanctions_list is true.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfe783e8add",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-8934\",\"vendor\":\"Stonebridge Foods\",\"amount\":768.25,\"purchase_order_received\":true,\"vendor_free_of_sanctions\":true,\"vendor_tax_form_missing\":false,\"duplicate_of_paid_invoice\":false,\"payment_requested_during_business_hours\":true,\"amount_approval_threshold\":1000.00}",
  "question": "Proposed action: deny\nLooking at this, is the proposed action not the right thing to do?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qa2d002257a",
  "kind": "yes/no",
  "text": "invoice_id: INV-9529\nvendor: Fairview Systems\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: true\namount_approval_threshold: 5000.00\nvendor_on_sanctions_list: true\namount: 4027.05\nawaiting_purchase_order: false\nvendor_tax_form_missing: false",
  "question": "Proposed action: deny\nWeighed against the request in the record, does the proposed action look like the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qa3013593bd",
  "kind": "yes/no",
  "text": "{\n    \"record\":{\n        \"invoice_id\":\"INV-6648\",\n        \"vendor\":\"Redwood Group\"\n    },\n    \"numbers\":{\n        \"amount_approval_threshold\":500.00,\n        \"amount\":231.55\n    },\n    \"flags\":{\n        \"duplicate_of_paid_invoice\":false,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_free_of_sanctions\":false,\n        \"purchase_order_received\":true,\n        \"vendor_tax_form_on_file\":false\n    }\n}",
  "question": "Proposed action: reject\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: shut this down right away, we are staying clear of it\n- escalate: hand this over to whoever has the final say\n- hold: chill until the document turns up\n- pay: proceed and the requester gets what they asked\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4381422995",
  "kind": "yes/no",
  "text": "---\n# extract\ninvoice_id: INV-5313\nvendor: Lakeshore Works\nduplicate_of_paid_invoice: false\namount: 254.93\namount_approval_threshold: 500.00\nawaiting_purchase_order: false\npayment_requested_during_business_hours: true\nvendor_free_of_sanctions: true\nvendor_tax_form_missing: false",
  "question": "Proposed action: put on hold\nIs the proposed action ruled out by the facts set out in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if amount is above amount_approval_threshold.\n2. turn down if vendor_free_of_sanctions is false.\n3. put on hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: go ahead.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3e6708fd7a",
  "kind": "choice",
  "text": "{\n  \"subject\":{\n    \"invoice_id\":\"INV-4993\",\n    \"vendor\":\"Northwind Systems\"\n  },\n  \"amounts\":{\n    \"amount\":1081.66,\n    \"amount_approval_threshold\":1000.00\n  },\n  \"checks\":{\n    \"vendor_tax_form_missing\":false,\n    \"duplicate_of_paid_invoice\":false,\n    \"awaiting_purchase_order\":false,\n    \"vendor_free_of_sanctions\":true,\n    \"payment_requested_during_business_hours\":false\n  }\n}",
  "question": "The record is complete: nothing else applies.\n\nGiven the request and the facts stated, which of the actions listed is the right call?",
  "options": [
   "put_on_hold",
   "send_to_a_person",
   "go_ahead"
  ]
 },
 {
  "qid": "q14f16f64f0",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-8608\n- vendor: Northwind Traders\n- vendor free of sanctions: yes\n- payment requested during business hours: yes\n- awaiting purchase order: no\n- duplicate of paid invoice: no\n- vendor tax form on file: yes\n- amount approval threshold: 10000.00\n- amount: 10000.00",
  "question": "Proposed action: release\nIs the proposed action not the right call for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q3c22923692",
  "kind": "choice",
  "text": "# extract\ninvoice_id | INV-8928\nvendor | Redwood Group\namount_approval_threshold | 5000.00\nduplicate_of_paid_invoice | false\npayment_requested_during_business_hours | true\nawaiting_purchase_order | false\nvendor_free_of_sanctions | true\nvendor_tax_form_missing | false\namount | 3383.39",
  "question": "Meanings:\n- turn down: kill this one off, it is off the table for good\n- go ahead: keep moving on this one nothing is holding it up\n- send to a person: forward it to the decision maker\n- put on hold: hold this until a check comes back\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "go ahead",
   "put on hold",
   "send to a person"
  ]
 },
 {
  "qid": "qe8edf7c033",
  "kind": "choice",
  "text": "# record\ninvoice_id=INV-6550\nvendor=Summit Industries\namount=1133.80\nvendor_tax_form_missing=true\namount_approval_threshold=5000.00\npayment_requested_during_business_hours=true\nvendor_on_sanctions_list=true\nduplicate_of_paid_invoice=false\npurchase_order_received=true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. deny if vendor_on_sanctions_list is true.\n3. defer if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- ask manager: send it onward because someone else must decide\n- approve: commence the action as specified without impediment\n- defer: freeze progress until the paperwork arrives\n- deny: stop the request so the requester gets nothing from it\nThe record is complete: nothing else applies.\n\nChecklist item: which of the actions listed below is the right call for the request?",
  "options": [
   "deny",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "q98e47edc5d",
  "kind": "yes/no",
  "text": "invoice_id | INV-2627\nvendor | Stonebridge Logistics\npayment_requested_during_business_hours | true\namount | 45826.81\nvendor_on_sanctions_list | true\nvendor_tax_form_missing | false\nduplicate_of_paid_invoice | false\nawaiting_purchase_order | false\namount_approval_threshold | 25000.00",
  "question": "Proposed action: hold\nIs the proposed action not suited to this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: awaiting_purchase_order, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- pay: continue the work as originally asked, there is nothing in the way\n- escalate: be passed along to whoever makes the call\n- hold: wait so the requester can supply more information first\n- reject: be blocked outright so it never gets carried out\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe89c6d890c",
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
  "qid": "q74ea71795d",
  "kind": "yes/no",
  "text": "{\n  \"record\":{\n    \"invoice_id\":\"INV-2836\",\n    \"vendor\":\"Stonebridge Foods\"\n  },\n  \"numbers\":{\n    \"amount_approval_threshold\":2500.00,\n    \"amount\":2500.00\n  },\n  \"flags\":{\n    \"payment_requested_during_business_hours\":true,\n    \"vendor_tax_form_on_file\":true,\n    \"duplicate_of_paid_invoice\":false,\n    \"vendor_on_sanctions_list\":true,\n    \"awaiting_purchase_order\":false\n  }\n}",
  "question": "Proposed action: cancel_order\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel_order if vendor_on_sanctions_list is true.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q499b67debb",
  "kind": "choice",
  "text": "# record\ninvoice_id=INV-1170\nvendor=Riverbend Works\nvendor_free_of_sanctions=true\namount_approval_threshold=2500.00\namount=435.46\nawaiting_purchase_order=false\npayment_requested_during_business_hours=true\nvendor_tax_form_on_file=false\nduplicate_of_paid_invoice=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. TJ if awaiting_purchase_order is true.\n2. GKZR if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. WFM if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: J.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- J: complete the job as it was assigned\n- WFM: forward it to the decision maker\n- TJ: stay put until the check is finished\n- GKZR: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies.\n\nConsidering what was asked and the facts available, which action below should be chosen?",
  "options": [
   "TJ",
   "J",
   "WFM"
  ]
 },
 {
  "qid": "qf07a666533",
  "kind": "yes/no",
  "text": "invoice_id=INV-5258\nvendor=Riverbend Labs\namount_approval_threshold=25000.00\nawaiting_purchase_order=false\nduplicate_of_paid_invoice=false\namount=5930.35\nvendor_tax_form_on_file=true\npayment_requested_during_business_hours=false\nvendor_on_sanctions_list=false",
  "question": "Proposed action: pay\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qe1789fa91f",
  "kind": "yes/no",
  "text": "{\n    \"subject\":{\n        \"invoice_id\":\"INV-6473\",\n        \"vendor\":\"Summit Logistics\"\n    },\n    \"amounts\":{\n        \"amount\":2341.70,\n        \"amount_approval_threshold\":10000.00\n    },\n    \"checks\":{\n        \"purchase_order_received\":true,\n        \"vendor_free_of_sanctions\":true,\n        \"duplicate_of_paid_invoice\":false,\n        \"vendor_tax_form_missing\":false,\n        \"payment_requested_during_business_hours\":false\n    }\n}",
  "question": "Proposed action: approve\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if amount is at least amount_approval_threshold.\n2. defer if purchase_order_received is false or vendor_tax_form_missing is true.\n3. deny if duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- deny: block it right away\n- ask_manager: escalate this to the person who decides\n- approve: continue with the request as nothing obstructs it\n- defer: sit on it till the doc shows up\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qeaaa15a4d6",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-8359\",\n  \"vendor\":\"Stonebridge Supply\",\n  \"amount\":422.27,\n  \"amount_approval_threshold\":1000.00,\n  \"duplicate_of_paid_invoice\":true,\n  \"payment_requested_during_business_hours\":false,\n  \"vendor_tax_form_missing\":false,\n  \"purchase_order_received\":true,\n  \"vendor_free_of_sanctions\":true\n}",
  "question": "Proposed action: send_to_a_person\nIs it not so that the proposed action is not mistaken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn_down if vendor_free_of_sanctions is false.\n3. put_on_hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcfdf9b8e69",
  "kind": "yes/no",
  "text": "{\n    \"record\":{\n        \"invoice_id\":\"INV-6648\",\n        \"vendor\":\"Redwood Group\"\n    },\n    \"numbers\":{\n        \"amount_approval_threshold\":500.00,\n        \"amount\":231.55\n    },\n    \"flags\":{\n        \"duplicate_of_paid_invoice\":false,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_free_of_sanctions\":false,\n        \"purchase_order_received\":true,\n        \"vendor_tax_form_on_file\":false\n    }\n}",
  "question": "Proposed action: reject\nGiven the request and the facts, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: shut this down right away, we are staying clear of it\n- escalate: hand this over to whoever has the final say\n- hold: chill until the document turns up\n- pay: proceed and the requester gets what they asked\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q36ff76e98c",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-7803\n- vendor: Ironleaf Traders\n- amount approval threshold: 2500.00\n- amount: 3490.23\n- vendor free of sanctions: yes\n- vendor tax form on file: yes\n- payment requested during business hours: yes\n- duplicate of paid invoice: no\n- awaiting purchase order: yes",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. D if amount is at least amount_approval_threshold.\n2. KPM if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. DDSK if duplicate_of_paid_invoice is true.\nOtherwise: FK.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- DDSK: halt this item because the rules forbid it\n- D: be passed along to whoever makes the call\n- FK: continue so the requester receives the result\n- KPM: hold the request until the check is done\nThe record is complete: nothing else applies.\n\nAs an auditor, which of the listed actions is the correct call for this request?",
  "options": [
   "DDSK",
   "D",
   "FK"
  ]
 },
 {
  "qid": "q8286c46d8b",
  "kind": "yes/no",
  "text": "invoice_id | INV-8468\nvendor | Brightwater Logistics\nduplicate_of_paid_invoice | false\nawaiting_purchase_order | true\namount | 1106.70\nvendor_on_sanctions_list | false\npayment_requested_during_business_hours | true\namount_approval_threshold | 5000.00\nvendor_tax_form_on_file | true",
  "question": "Proposed action: delay\nDoes the proposed action make sense for the request shown in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel_order if vendor_on_sanctions_list is true.\n3. delay if awaiting_purchase_order is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- release: have the task carried out as it was originally asked\n- delay: keep it in limbo until the verification has been confirmed\n- cancel_order: block this from going any further\n- hand_to_a_person: refer this item to the person who holds decision authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2c3170fc95",
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
  "qid": "q226d642950",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-3388\",\"vendor\":\"Northwind Foods\",\"payment_requested_during_business_hours\":true,\"amount\":20793.88,\"duplicate_of_paid_invoice\":true,\"amount_approval_threshold\":25000.00,\"vendor_on_sanctions_list\":true,\"vendor_tax_form_missing\":true,\"purchase_order_received\":true}",
  "question": "Proposed action: put on hold\nHas the request, read alongside the facts, ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if amount is at least amount_approval_threshold.\n2. put on hold if purchase_order_received is false or vendor_tax_form_missing is true.\n3. turn down if duplicate_of_paid_invoice is true.\nOtherwise: go ahead.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours.\nMeanings:\n- send to a person: transfer it to the person with authority\n- turn down: shut this down before it spreads into the workflow\n- go ahead: have the plan kept moving as it was requested\n- put on hold: suspend action until the facts are confirmed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd4d70d7eb3",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-2299\n- vendor: Cedar Works\n- purchase order received: yes\n- payment requested during business hours: yes\n- vendor tax form missing: no\n- amount: 512.37\n- duplicate of paid invoice: yes\n- vendor free of sanctions: yes\n- amount approval threshold: 1000.00",
  "question": "Meanings:\n- deny: reject the request in full\n- defer: hold off until the check clears\n- ask manager: bring in the authority who can settle it for the requester\n- approve: proceed as asked since everything is cleared\nThe record is complete: nothing else applies.\n\nWhich of the actions listed under the record would the requester see as the right call?",
  "options": [
   "deny",
   "ask manager",
   "defer"
  ]
 },
 {
  "qid": "q0e8b69ccd4",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-1597\nvendor | Summit Systems\nvendor_free_of_sanctions | false\namount_approval_threshold | 2500.00\nawaiting_purchase_order | false\nvendor_tax_form_missing | false\npayment_requested_during_business_hours | true\namount | 2475.83\nduplicate_of_paid_invoice | false",
  "question": "Proposed action: delay\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if amount is at least amount_approval_threshold.\n2. cancel order if duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_free_of_sanctions is false.\nOtherwise: release.\nNever counted: awaiting_purchase_order, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- release: finish what was asked as stated, the way ahead is fully free\n- delay: wait for the document to come through\n- hand to a person: forward it to the decision maker\n- cancel order: refuse the request because it crosses a clear line\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1a011301be",
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
  "qid": "q183286d907",
  "kind": "choice",
  "text": "# extract\ninvoice_id=INV-8653\nvendor=Ironleaf Foods\nvendor_tax_form_missing=false\namount_approval_threshold=5000.00\npurchase_order_received=true\namount=592.69\nvendor_on_sanctions_list=false\nduplicate_of_paid_invoice=false\npayment_requested_during_business_hours=true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- hold: wait so the requester can supply more information first\n- reject: drop this right there, we are not touching it\n- pay: proceed in accordance with the stated request\n- escalate: get sent upward to the one who decides\nThe record is complete: nothing else applies.\n\nGiven the request and the facts stated, which of the actions listed is the right call?",
  "options": [
   "hold",
   "escalate",
   "pay"
  ]
 },
 {
  "qid": "qb732b1db97",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\": \"INV-9272\",\n  \"vendor\": \"Oakmont Traders\",\n  \"payment_requested_during_business_hours\": false,\n  \"amount_approval_threshold\": 2500.00,\n  \"amount\": 1830.08,\n  \"duplicate_of_paid_invoice\": false,\n  \"purchase_order_received\": true,\n  \"vendor_free_of_sanctions\": false,\n  \"vendor_tax_form_on_file\": true\n}",
  "question": "Proposed action: pay\nDo the record facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_free_of_sanctions is false.\nOtherwise: pay.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc771a2abfd",
  "kind": "yes/no",
  "text": "# record\ninvoice_id: INV-6645\nvendor: Cedar Works\namount_approval_threshold: 10000.00\nvendor_free_of_sanctions: true\npayment_requested_during_business_hours: false\nduplicate_of_paid_invoice: true\nvendor_tax_form_missing: false\namount: 17812.07\npurchase_order_received: true",
  "question": "Proposed action: escalate\nHas the record ruled out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is at least amount_approval_threshold.\n2. hold if purchase_order_received is false or vendor_tax_form_missing is true.\n3. reject if duplicate_of_paid_invoice is true.\nOtherwise: pay.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- hold: hold this until a check comes back\n- reject: halt this item because the rules forbid it\n- pay: finish what was asked as stated, the way ahead is fully free\n- escalate: delegate the call to whoever holds authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q82ee2aa418",
  "kind": "choice",
  "text": "{\n  \"meta\":{\n    \"invoice_id\":\"INV-6445\",\n    \"vendor\":\"Summit Logistics\"\n  },\n  \"metrics\":{\n    \"amount\":314.90,\n    \"amount_approval_threshold\":1000.00\n  },\n  \"signals\":{\n    \"vendor_on_sanctions_list\":false,\n    \"awaiting_purchase_order\":false,\n    \"duplicate_of_paid_invoice\":false,\n    \"payment_requested_during_business_hours\":true,\n    \"vendor_tax_form_on_file\":true\n  }\n}",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "deny",
   "ask_manager",
   "approve"
  ]
 },
 {
  "qid": "q1e62f4ecd5",
  "kind": "choice",
  "text": "# record\ninvoice_id=INV-7365\nvendor=Ironleaf Logistics\nduplicate_of_paid_invoice=false\namount_approval_threshold=5000.00\nvendor_free_of_sanctions=true\nawaiting_purchase_order=false\namount=2353.59\nvendor_tax_form_missing=true\npayment_requested_during_business_hours=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. F if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. WG if vendor_free_of_sanctions is false.\n3. JLC if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: HWDZ.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- F: submit it upward to the approver\n- JLC: hold all progress until the requisite documentation arrives\n- HWDZ: continue with the request as nothing obstructs it\n- WG: toss it out, we are never doing this\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "HWDZ",
   "JLC",
   "WG"
  ]
 }
]
