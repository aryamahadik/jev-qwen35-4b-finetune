# G5-H blind read T46-blind_read-05dcb4b4-004 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r6a/T46/qc/g5h/answers/T46-blind_read-05dcb4b4-004.json

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
  "qid": "q5a6496a22d",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-6664\", \"vendor\": \"Bluepeak Partners\", \"vendor_tax_form_on_file\": true, \"amount_approval_threshold\": 5000.00, \"amount\": 5000.00, \"duplicate_of_paid_invoice\": false, \"vendor_free_of_sanctions\": true, \"awaiting_purchase_order\": false, \"payment_requested_during_business_hours\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel_order if vendor_free_of_sanctions is false.\n2. hand_to_a_person if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "cancel_order",
   "hand_to_a_person",
   "release"
  ]
 },
 {
  "qid": "qbe3c868575",
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
  "qid": "q204a569b3e",
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
  "qid": "qdc3afc6ba2",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id                              | INV-3141\nvendor                                  | Harbor Supply\npurchase_order_received                 | true\nvendor_tax_form_missing                 | false\nvendor_free_of_sanctions                | true\nduplicate_of_paid_invoice               | false\namount_approval_threshold               | 10000.00\npayment_requested_during_business_hours | true\namount                                  | 4469.79",
  "question": "Proposed action: cancel_order\nDoes the record show that the proposed action is not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel_order if vendor_free_of_sanctions is false.\n2. hand_to_a_person if purchase_order_received is false or vendor_tax_form_missing is true.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qbfa300cda3",
  "kind": "choice",
  "text": "# record\ninvoice_id: INV-8393\nvendor: Oakmont Logistics\npayment_requested_during_business_hours: true\nvendor_free_of_sanctions: true\namount: 5000.00\nduplicate_of_paid_invoice: false\namount_approval_threshold: 5000.00\npurchase_order_received: true\nvendor_tax_form_missing: false",
  "question": "Meanings:\n- pay: keep going exactly as requested because every obstacle has cleared\n- escalate: forward it to the decision maker\n- reject: send the requester away with the request left unfinished\n- hold: park the file until the requester sends the document in\nThe record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "escalate",
   "pay",
   "hold"
  ]
 },
 {
  "qid": "q56ce6f22f3",
  "kind": "choice",
  "text": "# request record\ninvoice_id                              | INV-7887\nvendor                                  | Bluepeak Labs\namount                                  | 10000.01\nvendor_tax_form_missing                 | false\nvendor_on_sanctions_list                | false\namount_approval_threshold               | 10000.00\nduplicate_of_paid_invoice               | false\npayment_requested_during_business_hours | false\nawaiting_purchase_order                 | false",
  "question": "Meanings:\n- go_ahead: run the task as it was asked, with nothing standing between it and completion\n- send_to_a_person: hand this to the person who decides\n- put_on_hold: pause and collect more information first\n- turn_down: bin this idea and keep it out of the flow\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the most suitable for the request?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "put_on_hold"
  ]
 },
 {
  "qid": "q33467b0a40",
  "kind": "choice",
  "text": "# extract\ninvoice_id = INV-8694\nvendor = Ironleaf Partners\namount_approval_threshold = 2500.00\namount = 1373.42\nduplicate_of_paid_invoice = true\nvendor_on_sanctions_list = false\npayment_requested_during_business_hours = false\nawaiting_purchase_order = false\nvendor_tax_form_missing = false",
  "question": "Meanings:\n- 37: be handed over to the deciding person\n- 877: shut this down before it spreads into the workflow\n- 5: pause and collect more information first\n- 8810: go ahead and the requester will be served\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "37",
   "8810",
   "877"
  ]
 },
 {
  "qid": "qf9e84d7920",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-3222\", \"vendor\": \"Copperfield Logistics\", \"vendor_tax_form_on_file\": false, \"amount\": 305.63, \"vendor_on_sanctions_list\": false, \"awaiting_purchase_order\": false, \"duplicate_of_paid_invoice\": false, \"amount_approval_threshold\": 500.00, \"payment_requested_during_business_hours\": true}",
  "question": "Proposed action: cancel_order\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qdf848b4176",
  "kind": "yes/no",
  "text": "---\n# record\ninvoice_id: \"INV-7182\"\nvendor: \"Brightwater Foods\"\namount_approval_threshold: 5000.00\nvendor_tax_form_missing: false\npayment_requested_during_business_hours: true\namount: 8404.14\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: false\npurchase_order_received: true",
  "question": "Proposed action: send to a person\nDoes the record's evidence rule out the proposed action as the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if amount is above amount_approval_threshold.\n2. turn down if vendor_on_sanctions_list is true.\n3. put on hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: go ahead.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- go ahead: carry out the request as written\n- turn down: halt the request at this point\n- send to a person: route the request to the decision maker\n- put on hold: hold up for a sec until more info comes in\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qbafbd22f21",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n  invoice_id: \"INV-4956\"\n  vendor: \"Ironleaf Logistics\"\namounts:\n  amount: 386.54\n  amount_approval_threshold: 1000.00\nchecks:\n  vendor_on_sanctions_list: false\n  purchase_order_received: true\n  payment_requested_during_business_hours: true\n  duplicate_of_paid_invoice: false\n  vendor_tax_form_missing: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. deny if vendor_on_sanctions_list is true.\n3. defer if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- deny: bin this idea and keep it out of the flow\n- approve: proceed with the task as asked\n- ask manager: hand the matter to a decider so the requester gets a verdict\n- defer: wait for the document to come through\nThe record is complete: nothing else applies.\n\nChecklist item: which of the actions listed below is the right call for the request?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q98d3cb3c2c",
  "kind": "yes/no",
  "text": "---\n# extract\ninvoice_id: INV-2126\nvendor: Stonebridge Group\npurchase_order_received: true\nvendor_on_sanctions_list: true\namount: 2011.35\npayment_requested_during_business_hours: true\nvendor_tax_form_missing: false\namount_approval_threshold: 2500.00\nduplicate_of_paid_invoice: false",
  "question": "Proposed action: put_on_hold\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if amount is at least amount_approval_threshold.\n2. turn_down if duplicate_of_paid_invoice is true.\n3. send_to_a_person if vendor_on_sanctions_list is true.\nOtherwise: go_ahead.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qff49184144",
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
  "qid": "qb542011db7",
  "kind": "yes/no",
  "text": "{\n  \"subject\": {\n    \"invoice_id\": \"INV-5784\",\n    \"vendor\": \"Fairview Partners\"\n  },\n  \"amounts\": {\n    \"amount_approval_threshold\": 2500.00,\n    \"amount\": 1996.93\n  },\n  \"checks\": {\n    \"vendor_on_sanctions_list\": false,\n    \"payment_requested_during_business_hours\": false,\n    \"vendor_tax_form_on_file\": true,\n    \"purchase_order_received\": true,\n    \"duplicate_of_paid_invoice\": false\n  }\n}",
  "question": "Proposed action: delay\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel_order if vendor_on_sanctions_list is true.\n3. delay if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- hand_to_a_person: toss it over to the one who makes the call\n- release: continue with what was requested\n- delay: hang tight until we get the check back\n- cancel_order: refuse this request entirely\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4cd8248a3b",
  "kind": "yes/no",
  "text": "---\ninvoice_id: INV-5064\nvendor: Harbor Group\nvendor_free_of_sanctions: true\namount_approval_threshold: 1000.00\npayment_requested_during_business_hours: true\nvendor_tax_form_missing: false\nduplicate_of_paid_invoice: false\npurchase_order_received: true\namount: 1000.01",
  "question": "Proposed action: approve\nIs it not the case that, given the record, the proposed action is not a poor call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q081e8eeaf8",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-8542\",\"vendor\":\"Silverline Traders\",\"amount_approval_threshold\":5000.00,\"duplicate_of_paid_invoice\":false,\"payment_requested_during_business_hours\":true,\"vendor_tax_form_on_file\":true,\"vendor_free_of_sanctions\":true,\"purchase_order_received\":false,\"amount\":4722.05}",
  "question": "Proposed action: 31\nQuick question: is the proposed action the right thing to do with this request?",
  "definitions": "Meanings:\n- 7819: have the task carried out as it was originally asked\n- 31: pump the brakes until more details show up\n- 434: bring in the authority who can settle it for the requester\n- 4: end it so the requester sees their request closed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7b5b8fd069",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-9730\",\"vendor\":\"Riverbend Logistics\",\"amount_approval_threshold\":1000.00,\"awaiting_purchase_order\":false,\"payment_requested_during_business_hours\":true,\"vendor_tax_form_on_file\":false,\"vendor_on_sanctions_list\":false,\"duplicate_of_paid_invoice\":false,\"amount\":1148.48}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 2828 if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n2. 254 if amount is above amount_approval_threshold.\n3. 31 if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: 9.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 9: push ahead as planned\n- 2828: keep their request on hold until more information arrives from them\n- 254: get referred to the person who decides\n- 31: shut off this process completely\nThe record is complete: nothing else applies.\n\nWhich of the actions listed does the record best support for this request?",
  "options": [
   "9",
   "31",
   "2828"
  ]
 },
 {
  "qid": "q16746373fe",
  "kind": "choice",
  "text": "{\n  \"subject\": {\n    \"invoice_id\": \"INV-6442\",\n    \"vendor\": \"Riverbend Traders\"\n  },\n  \"amounts\": {\n    \"amount_approval_threshold\": 5000.00,\n    \"amount\": 6465.60\n  },\n  \"checks\": {\n    \"purchase_order_received\": false,\n    \"vendor_tax_form_missing\": false,\n    \"vendor_free_of_sanctions\": false,\n    \"payment_requested_during_business_hours\": true,\n    \"duplicate_of_paid_invoice\": false\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 329 if amount is at least amount_approval_threshold.\n2. 8027 if duplicate_of_paid_invoice is true.\n3. 3 if vendor_free_of_sanctions is false.\nOtherwise: 18.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- 8027: end this here and now\n- 18: keep going with it\n- 329: keep it on hold for the missing document\n- 3: toss it over to the one who makes the call\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "8027",
   "18",
   "329"
  ]
 },
 {
  "qid": "q2c446777a4",
  "kind": "choice",
  "text": "{\n  \"record\":{\n    \"invoice_id\":\"INV-8683\",\n    \"vendor\":\"Cedar Partners\"\n  },\n  \"numbers\":{\n    \"amount\":6908.59,\n    \"amount_approval_threshold\":25000.00\n  },\n  \"flags\":{\n    \"duplicate_of_paid_invoice\":false,\n    \"payment_requested_during_business_hours\":false,\n    \"vendor_on_sanctions_list\":true,\n    \"vendor_tax_form_on_file\":true,\n    \"purchase_order_received\":true\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if purchase_order_received is false.\n2. cancel_order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. hand_to_a_person if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- hand_to_a_person: transfer the case to the responsible decision maker for determination\n- release: run with this one\n- cancel_order: refuse this request entirely\n- delay: suspend progress until verification is received\nThe record is complete: nothing else applies.\n\nWhat would the requester most want done from the actions listed below?",
  "options": [
   "release",
   "delay",
   "cancel_order"
  ]
 },
 {
  "qid": "q0439bf049b",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-1495\", \"vendor\": \"Brightwater Systems\", \"awaiting_purchase_order\": false, \"duplicate_of_paid_invoice\": false, \"payment_requested_during_business_hours\": true, \"vendor_free_of_sanctions\": false, \"amount\": 517.03, \"amount_approval_threshold\": 2500.00, \"vendor_tax_form_on_file\": true}",
  "question": "Proposed action: deny\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if amount is at least amount_approval_threshold.\n2. deny if duplicate_of_paid_invoice is true.\n3. ask_manager if vendor_free_of_sanctions is false.\nOtherwise: approve.\nNever counted: awaiting_purchase_order, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- approve: have the task carried out as it was originally asked\n- defer: wait for that check then we will see\n- ask_manager: route it elsewhere because a decider must weigh in\n- deny: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5eba0a37a4",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id=INV-6392\nvendor=Pinecrest Labs\npurchase_order_received=false\nvendor_tax_form_on_file=true\nduplicate_of_paid_invoice=false\nvendor_free_of_sanctions=true\npayment_requested_during_business_hours=true\namount_approval_threshold=500.00\namount=223.70",
  "question": "Proposed action: GX\nGiven the request and its facts, has the proposed action been ruled out?",
  "definitions": "Meanings:\n- F: hold off until the check has been completed by the team\n- VBM: cease the operation as it is prohibited\n- FNZR: complete the action that was asked for\n- GX: pass this along to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1458b9366d",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-4349\",\n  \"vendor\":\"Cedar Labs\",\n  \"vendor_on_sanctions_list\":false,\n  \"purchase_order_received\":true,\n  \"duplicate_of_paid_invoice\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"amount_approval_threshold\":1000.00,\n  \"amount\":1696.73,\n  \"vendor_tax_form_missing\":false\n}",
  "question": "Proposed action: pay\nIs it not the case that the proposed action is not a poor choice for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qc8d8a01d4a",
  "kind": "yes/no",
  "text": "# record\ninvoice_id: INV-8076\nvendor: Fairview Works\namount: 1000.00\npurchase_order_received: true\npayment_requested_during_business_hours: true\nvendor_tax_form_on_file: true\nduplicate_of_paid_invoice: false\namount_approval_threshold: 1000.00\nvendor_free_of_sanctions: false",
  "question": "Proposed action: reject\nHas anything in the record ruled out the proposed action for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q0d1f881442",
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
  "qid": "qd088afc2a1",
  "kind": "yes/no",
  "text": "---\n# record\ninvoice_id: \"INV-6573\"\nvendor: \"Oakmont Foods\"\nduplicate_of_paid_invoice: false\npurchase_order_received: true\nvendor_tax_form_on_file: true\namount: 278.57\npayment_requested_during_business_hours: false\nvendor_on_sanctions_list: false\namount_approval_threshold: 500.00",
  "question": "Proposed action: 695\nIs it not correct that the proposed action is not an error given what the record shows?",
  "definitions": "Meanings:\n- 94: hold off until more information arrives\n- 5: escalate this to someone senior who decides\n- 695: push ahead as planned\n- 5136: send the requester away with the request left unfinished\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qed2352bbc0",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id: INV-5161\nvendor: Riverbend Works\namount: 346.76\npayment_requested_during_business_hours: true\namount_approval_threshold: 500.00\nduplicate_of_paid_invoice: false\nvendor_on_sanctions_list: true\nvendor_tax_form_missing: false\npurchase_order_received: false",
  "question": "Proposed action: hold\nTell me, has the record ruled out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if vendor_tax_form_missing is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_on_sanctions_list is true.\n3. hold if purchase_order_received is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: drop this request from the queue\n- hold: park the file until the requester sends the document in\n- escalate: transfer it to the person with authority\n- pay: press on with the work as originally set\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7d018ef370",
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
  "qid": "q7d41cc3c13",
  "kind": "yes/no",
  "text": "---\n# record\nmeta:\n    invoice_id: \"INV-2787\"\n    vendor: \"Redwood Works\"\nmetrics:\n    amount: 4058.12\n    amount_approval_threshold: 10000.00\nsignals:\n    awaiting_purchase_order: true\n    vendor_free_of_sanctions: false\n    duplicate_of_paid_invoice: true\n    vendor_tax_form_missing: false\n    payment_requested_during_business_hours: false",
  "question": "Proposed action: 4322\nIs it not true that the proposed action is not out of step with what the request asks for?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 4322 if amount is at least amount_approval_threshold.\n2. 65 if duplicate_of_paid_invoice is true.\n3. 8 if vendor_free_of_sanctions is false.\nOtherwise: 636.\nNever counted: awaiting_purchase_order, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- 65: toss it out, we are never doing this\n- 636: finish it so the requester has their answer\n- 8: be forwarded to the person in charge\n- 4322: stay put until the check is finished\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q89c4daa2f7",
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
  "qid": "q93805f5d5c",
  "kind": "choice",
  "text": "invoice_id=INV-3515\nvendor=Fairview Supply\npayment_requested_during_business_hours=true\namount=318.94\nduplicate_of_paid_invoice=false\nawaiting_purchase_order=true\nvendor_free_of_sanctions=true\nvendor_tax_form_on_file=true\namount_approval_threshold=500.00",
  "question": "Meanings:\n- 9226: hand the matter to a decider so the requester gets a verdict\n- 20: terminate the process as continuation is prohibited\n- 925: proceed with the task as asked\n- 2: pause here and wait for the check\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "925",
   "2",
   "20"
  ]
 },
 {
  "qid": "q539a8cd994",
  "kind": "choice",
  "text": "# record\ninvoice_id | INV-8310\nvendor | Harbor Logistics\namount | 7360.23\namount_approval_threshold | 10000.00\nvendor_on_sanctions_list | false\nduplicate_of_paid_invoice | false\npayment_requested_during_business_hours | true\nvendor_tax_form_on_file | true\npurchase_order_received | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if purchase_order_received is false or vendor_tax_form_on_file is false.\n2. hand to a person if amount is above amount_approval_threshold.\n3. cancel order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nAmong the actions listed after this, which best matches the request?",
  "options": [
   "release",
   "cancel order",
   "delay"
  ]
 },
 {
  "qid": "q19ab73da23",
  "kind": "yes/no",
  "text": "# request record\ninvoice_id: INV-2549\nvendor: Harbor Foods\namount_approval_threshold: 500.00\npayment_requested_during_business_hours: true\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: false\nawaiting_purchase_order: false\nvendor_tax_form_on_file: true\namount: 500.01",
  "question": "Proposed action: pay\nWould the proposed action be not the right choice here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: awaiting_purchase_order, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- reject: be halted at once and left unperformed\n- pay: complete the job as it was assigned\n- escalate: forward it to the decision maker\n- hold: be paused until a document has been received\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2a21f07f17",
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
  "qid": "q01b1c29d72",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-3894\n- vendor: Pinecrest Systems\n- amount: 9999.99\n- payment requested during business hours: yes\n- vendor tax form missing: no\n- amount approval threshold: 10000.00\n- purchase order received: no\n- vendor free of sanctions: yes\n- duplicate of paid invoice: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if amount is at least amount_approval_threshold.\n2. put on hold if purchase_order_received is false or vendor_tax_form_missing is true.\n3. turn down if duplicate_of_paid_invoice is true.\nOtherwise: go ahead.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "go ahead",
   "put on hold",
   "turn down"
  ]
 },
 {
  "qid": "q0c9ffdbd91",
  "kind": "yes/no",
  "text": "invoice_id | INV-7956\nvendor | Lakeshore Works\nvendor_on_sanctions_list | false\namount | 445.66\npayment_requested_during_business_hours | true\nduplicate_of_paid_invoice | false\nvendor_tax_form_on_file | true\nawaiting_purchase_order | true\namount_approval_threshold | 500.00",
  "question": "Proposed action: reject\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qcc17b3cf5f",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-2778\",\"vendor\":\"Copperfield Systems\",\"amount_approval_threshold\":500.00,\"vendor_tax_form_on_file\":true,\"amount\":500.01,\"purchase_order_received\":true,\"vendor_free_of_sanctions\":true,\"payment_requested_during_business_hours\":true,\"duplicate_of_paid_invoice\":false}",
  "question": "Proposed action: escalate\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. reject if vendor_free_of_sanctions is false.\n2. escalate if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. hold if amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q60a6a04e42",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-8185\", \"vendor\": \"Ironleaf Industries\", \"amount\": 4031.67, \"vendor_free_of_sanctions\": true, \"duplicate_of_paid_invoice\": false, \"payment_requested_during_business_hours\": true, \"awaiting_purchase_order\": false, \"amount_approval_threshold\": 2500.00, \"vendor_tax_form_on_file\": true}",
  "question": "Proposed action: ask_manager\nDoes the proposed action make sense for the request shown in the record?",
  "definitions": "Meanings:\n- ask_manager: forward the matter as the call rests with someone higher\n- defer: pause this until the requester supplies the missing document\n- deny: be halted at once and left unperformed\n- approve: keep going with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q92ed5f0fa0",
  "kind": "choice",
  "text": "# case\ninvoice_id                              | INV-4234\nvendor                                  | Riverbend Group\nvendor_tax_form_on_file                 | true\namount                                  | 2522.67\npayment_requested_during_business_hours | true\npurchase_order_received                 | true\nvendor_on_sanctions_list                | false\nduplicate_of_paid_invoice               | false\namount_approval_threshold               | 10000.00",
  "question": "Meanings:\n- delay: be parked until a verification has been logged\n- release: run the task as it was asked, with nothing standing between it and completion\n- hand_to_a_person: give it to a person who has the authority to decide\n- cancel_order: halt the request at this point\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "release",
   "hand_to_a_person",
   "delay"
  ]
 },
 {
  "qid": "q94dcd77ea5",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"invoice_id\": \"INV-2334\",\n        \"vendor\": \"Redwood Group\"\n    },\n    \"values\": {\n        \"amount_approval_threshold\": 1000.00,\n        \"amount\": 1000.00\n    },\n    \"tests\": {\n        \"vendor_free_of_sanctions\": true,\n        \"duplicate_of_paid_invoice\": false,\n        \"vendor_tax_form_missing\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"awaiting_purchase_order\": false\n    }\n}",
  "question": "Proposed action: ask_manager\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if amount is above amount_approval_threshold.\n2. deny if vendor_free_of_sanctions is false.\n3. defer if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2e8887b2b5",
  "kind": "yes/no",
  "text": "---\n# request record\ninvoice_id: \"INV-3909\"\nvendor: \"Lakeshore Foods\"\nvendor_free_of_sanctions: true\namount_approval_threshold: 1000.00\nawaiting_purchase_order: false\npayment_requested_during_business_hours: true\namount: 1000.00\nduplicate_of_paid_invoice: false\nvendor_tax_form_missing: false",
  "question": "Proposed action: go_ahead\nAs a reviewer checking the file, is the proposed action not a sound decision here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. send_to_a_person if amount is above amount_approval_threshold.\n3. turn_down if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qde30a73407",
  "kind": "choice",
  "text": "---\n# case\ninvoice_id: INV-6139\nvendor: Silverline Group\nduplicate_of_paid_invoice: false\nawaiting_purchase_order: true\nvendor_free_of_sanctions: true\namount_approval_threshold: 5000.00\npayment_requested_during_business_hours: true\nvendor_tax_form_missing: false\namount: 4883.39",
  "question": "Meanings:\n- turn_down: kill this one off, it is off the table for good\n- put_on_hold: pump the brakes until more details show up\n- go_ahead: run with it carry on as you were\n- send_to_a_person: route the case to a decider so the requester knows the outcome\nThe record is complete: nothing else applies.\n\nFrom the requester's side, which of the actions listed below is the right call for this request?",
  "options": [
   "put_on_hold",
   "go_ahead",
   "turn_down"
  ]
 },
 {
  "qid": "q873964d96e",
  "kind": "yes/no",
  "text": "invoice_id | INV-4324\nvendor | Lakeshore Industries\nvendor_tax_form_on_file | true\npayment_requested_during_business_hours | false\nduplicate_of_paid_invoice | false\npurchase_order_received | true\nvendor_free_of_sanctions | true\namount_approval_threshold | 10000.00\namount | 7893.09",
  "question": "Proposed action: R\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. FC if amount is at least amount_approval_threshold.\n2. CXS if duplicate_of_paid_invoice is true.\n3. HVQL if vendor_free_of_sanctions is false.\nOtherwise: R.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- FC: keep waiting for the missing details\n- R: commence the action as specified without impediment\n- CXS: skip this one, it is a hard pass for us\n- HVQL: send it to whoever has the final say\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9ad9a7059a",
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
  "qid": "q1f2b06928c",
  "kind": "choice",
  "text": "---\ncase:\n    invoice_id: \"INV-1983\"\n    vendor: \"Lakeshore Partners\"\nvalues:\n    amount: 1141.60\n    amount_approval_threshold: 2500.00\ntests:\n    vendor_on_sanctions_list: false\n    awaiting_purchase_order: false\n    vendor_tax_form_on_file: true\n    payment_requested_during_business_hours: false\n    duplicate_of_paid_invoice: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. cancel order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nWhat would the requester most want done from the actions listed below?",
  "options": [
   "cancel order",
   "hand to a person",
   "release"
  ]
 },
 {
  "qid": "q4d5f5a73d2",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id = INV-1320\nvendor = Northwind Works\nduplicate_of_paid_invoice = false\nvendor_free_of_sanctions = true\npayment_requested_during_business_hours = false\namount_approval_threshold = 10000.00\nvendor_tax_form_on_file = true\namount = 4217.65\npurchase_order_received = true",
  "question": "Proposed action: send to a person\nReviewing this file as an auditor, is the proposed action not the correct step?",
  "definitions": "Meanings:\n- go ahead: proceed with the request since the way is clear and nothing blocks it\n- send to a person: direct the request to the responsible decider\n- put on hold: hold the request so the requester waits for their check\n- turn down: be turned away and treated as off limits\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1fce04c2a7",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-5949\n- vendor: Copperfield Supply\n- duplicate of paid invoice: yes\n- awaiting purchase order: no\n- vendor tax form missing: no\n- payment requested during business hours: yes\n- amount approval threshold: 10000.00\n- vendor on sanctions list: no\n- amount: 1686.15",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions below answers the request given the facts you can see?",
  "options": [
   "reject",
   "escalate",
   "pay"
  ]
 },
 {
  "qid": "qb24f57d99b",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id | INV-5861\nvendor | Fairview Group\namount_approval_threshold | 25000.00\namount | 24999.99\nduplicate_of_paid_invoice | true\npayment_requested_during_business_hours | false\nvendor_on_sanctions_list | false\nvendor_tax_form_on_file | true\npurchase_order_received | true",
  "question": "Proposed action: escalate\nAs a reviewer checking the file, is the proposed action not a sound decision here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- pay: continue as requested with the path fully open\n- reject: be halted at once and left unperformed\n- escalate: be handed over to the deciding person\n- hold: pause this until the requester supplies the missing document\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q52815dfa00",
  "kind": "yes/no",
  "text": "---\nrequest:\n  invoice_id: INV-7531\n  vendor: Oakmont Systems\nfigures:\n  amount_approval_threshold: 5000.00\n  amount: 621.40\nchecks:\n  awaiting_purchase_order: true\n  vendor_free_of_sanctions: true\n  vendor_tax_form_on_file: true\n  payment_requested_during_business_hours: false\n  duplicate_of_paid_invoice: false",
  "question": "Proposed action: go_ahead\nDo the facts here rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qb6bda2bfe6",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-4349\",\n  \"vendor\":\"Cedar Labs\",\n  \"vendor_on_sanctions_list\":false,\n  \"purchase_order_received\":true,\n  \"duplicate_of_paid_invoice\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"amount_approval_threshold\":1000.00,\n  \"amount\":1696.73,\n  \"vendor_tax_form_missing\":false\n}",
  "question": "Proposed action: pay\nIs the proposed action not suited to this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qd03819e416",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id = INV-6613\nvendor = Oakmont Industries\nvendor_on_sanctions_list = false\nvendor_tax_form_on_file = false\nawaiting_purchase_order = false\namount = 5000.00\npayment_requested_during_business_hours = false\namount_approval_threshold = 5000.00\nduplicate_of_paid_invoice = false",
  "question": "Proposed action: go_ahead\nOverall, would you say the proposed action suits the request in the record?",
  "definitions": "Meanings:\n- go_ahead: allow the matter to be taken forward as planned\n- turn_down: end this here and now\n- send_to_a_person: escalate this to someone senior who decides\n- put_on_hold: hold the request so the requester waits for their check\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q530b7c8fbf",
  "kind": "choice",
  "text": "invoice_id: INV-7655\nvendor: Oakmont Partners\nvendor_tax_form_missing: true\nduplicate_of_paid_invoice: false\nvendor_free_of_sanctions: true\namount: 564.45\namount_approval_threshold: 2500.00\npayment_requested_during_business_hours: true\nawaiting_purchase_order: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if amount is at least amount_approval_threshold.\n2. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. turn_down if duplicate_of_paid_invoice is true.\nOtherwise: go_ahead.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nWhat is the best action to pick from the list for this request?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "send_to_a_person"
  ]
 }
]
