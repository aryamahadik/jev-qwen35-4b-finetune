# G5-H blind read T46-blind_read-9ed82ffe-002 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r6a/T46/qc/g5h/answers/T46-blind_read-9ed82ffe-002.json

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
  "qid": "q268a71da20",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-8185\", \"vendor\": \"Ironleaf Industries\", \"amount\": 4031.67, \"vendor_free_of_sanctions\": true, \"duplicate_of_paid_invoice\": false, \"payment_requested_during_business_hours\": true, \"awaiting_purchase_order\": false, \"amount_approval_threshold\": 2500.00, \"vendor_tax_form_on_file\": true}",
  "question": "Proposed action: ask_manager\nDoes the proposed action make sense for the request shown in the record?",
  "definitions": "Meanings:\n- ask_manager: forward the matter as the call rests with someone higher\n- defer: pause this until the requester supplies the missing document\n- deny: be halted at once and left unperformed\n- approve: keep going with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q58f440ed39",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n* invoice id: INV-4156\n* vendor: Cedar Traders\n* awaiting purchase order: no\n* duplicate of paid invoice: no\n* vendor free of sanctions: yes\n* payment requested during business hours: yes\n* amount approval threshold: 5000.00\n* vendor tax form missing: no\n* amount: 5000.01",
  "question": "Proposed action: send_to_a_person\nHave the recorded facts ruled out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn_down if vendor_free_of_sanctions is false.\n3. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- send_to_a_person: submit the question to the authorised decision maker\n- go_ahead: let this be advanced exactly as originally specified\n- put_on_hold: wait for the missing material to come in before deciding anything\n- turn_down: leave the requester without the result they asked for\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6c54e14baa",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-1970\n- vendor: Redwood Group\n- amount approval threshold: 500.00\n- payment requested during business hours: yes\n- duplicate of paid invoice: yes\n- amount: 619.32\n- vendor tax form on file: yes\n- vendor on sanctions list: no\n- awaiting purchase order: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if amount is at least amount_approval_threshold.\n2. cancel order if duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_on_sanctions_list is true.\nOtherwise: release.\nNever counted: awaiting_purchase_order, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- hand to a person: bring in the authority who can settle it for the requester\n- delay: be held back until a check or document arrives\n- cancel order: terminate the process as continuation is prohibited\n- release: go ahead and the requester will be served\nThe record is complete: nothing else applies.\n\nBased on what the record shows, which of the actions listed is the right call?",
  "options": [
   "cancel order",
   "delay",
   "release"
  ]
 },
 {
  "qid": "qa60c19ac94",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-1996\nvendor=Redwood Supply\nduplicate_of_paid_invoice=false\namount_approval_threshold=500.00\nvendor_free_of_sanctions=true\namount=317.99\npurchase_order_received=true\npayment_requested_during_business_hours=true\nvendor_tax_form_missing=false",
  "question": "Proposed action: go_ahead\nFrom an audit standpoint, is the proposed action the right call for this request?",
  "definitions": "Meanings:\n- put_on_hold: hold the request until the check is done\n- go_ahead: go on and finish it the path is clear\n- turn_down: make sure the requester never gets what they wanted\n- send_to_a_person: submit the question to the authorised decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8d49bcec34",
  "kind": "choice",
  "text": "---\n# extract\ninvoice_id: INV-3492\nvendor: Oakmont Supply\nduplicate_of_paid_invoice: false\nawaiting_purchase_order: false\nvendor_tax_form_missing: false\npayment_requested_during_business_hours: true\nvendor_on_sanctions_list: false\namount_approval_threshold: 10000.00\namount: 10000.01",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel_order if vendor_on_sanctions_list is true.\n2. hand_to_a_person if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- delay: hold up for a sec until more info comes in\n- release: execute the request exactly as written\n- hand_to_a_person: hand this over to whoever has the final say\n- cancel_order: refuse the request because it crosses a clear line\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "hand_to_a_person",
   "release",
   "delay"
  ]
 },
 {
  "qid": "q640663b098",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-5038\",\"vendor\":\"Harbor Traders\",\"duplicate_of_paid_invoice\":false,\"purchase_order_received\":true,\"vendor_tax_form_on_file\":true,\"amount_approval_threshold\":10000.00,\"vendor_on_sanctions_list\":true,\"payment_requested_during_business_hours\":true,\"amount\":5076.95}",
  "question": "Proposed action: reject\nReviewing this file as an auditor, is the proposed action not the correct step?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. reject if vendor_on_sanctions_list is true.\n2. escalate if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. hold if amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9810747bc0",
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
  "qid": "q6522c2ce03",
  "kind": "yes/no",
  "text": "invoice_id | INV-4912\nvendor | Bluepeak Group\namount | 5000.00\nawaiting_purchase_order | false\nvendor_tax_form_on_file | true\namount_approval_threshold | 5000.00\nduplicate_of_paid_invoice | false\nvendor_free_of_sanctions | true\npayment_requested_during_business_hours | true",
  "question": "Proposed action: PXS\nLooking at what the record says, is the proposed action a good fit for the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. T if awaiting_purchase_order is true.\n2. VSFG if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. HM if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: PXS.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- T: hold all progress until the requisite documentation arrives\n- VSFG: reject the request in full\n- PXS: run the requested step through\n- HM: get the boss to make the final call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q97621028ef",
  "kind": "yes/no",
  "text": "invoice_id=INV-9309\nvendor=Northwind Partners\nvendor_on_sanctions_list=true\nawaiting_purchase_order=false\namount=10000.00\npayment_requested_during_business_hours=true\nduplicate_of_paid_invoice=false\namount_approval_threshold=10000.00\nvendor_tax_form_on_file=true",
  "question": "Proposed action: V\nDoes the proposed action make sense for the request shown in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. WND if amount is above amount_approval_threshold.\n2. V if vendor_on_sanctions_list is true.\n3. PH if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: MKQD.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- PH: suspend progress until verification is received\n- V: decline the request as the action is prohibited\n- WND: route this to the one who signs off\n- MKQD: carry on with it now\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q92486ac78f",
  "kind": "yes/no",
  "text": "# record\ninvoice_id: INV-6645\nvendor: Cedar Works\namount_approval_threshold: 10000.00\nvendor_free_of_sanctions: true\npayment_requested_during_business_hours: false\nduplicate_of_paid_invoice: true\nvendor_tax_form_missing: false\namount: 17812.07\npurchase_order_received: true",
  "question": "Proposed action: escalate\nHas the record ruled out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is at least amount_approval_threshold.\n2. hold if purchase_order_received is false or vendor_tax_form_missing is true.\n3. reject if duplicate_of_paid_invoice is true.\nOtherwise: pay.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nMeanings:\n- hold: hold this until a check comes back\n- reject: halt this item because the rules forbid it\n- pay: finish what was asked as stated, the way ahead is fully free\n- escalate: delegate the call to whoever holds authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0ca135bf8f",
  "kind": "yes/no",
  "text": "---\n# record\ninvoice_id: \"INV-6573\"\nvendor: \"Oakmont Foods\"\nduplicate_of_paid_invoice: false\npurchase_order_received: true\nvendor_tax_form_on_file: true\namount: 278.57\npayment_requested_during_business_hours: false\nvendor_on_sanctions_list: false\namount_approval_threshold: 500.00",
  "question": "Proposed action: 695\nIs it not correct that the proposed action is not an error given what the record shows?",
  "definitions": "Meanings:\n- 94: hold off until more information arrives\n- 5: escalate this to someone senior who decides\n- 695: push ahead as planned\n- 5136: send the requester away with the request left unfinished\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qed6ecf7725",
  "kind": "choice",
  "text": "{\n  \"record\":{\n    \"invoice_id\":\"INV-8726\",\n    \"vendor\":\"Summit Logistics\"\n  },\n  \"numbers\":{\n    \"amount\":18059.39,\n    \"amount_approval_threshold\":25000.00\n  },\n  \"flags\":{\n    \"duplicate_of_paid_invoice\":true,\n    \"awaiting_purchase_order\":false,\n    \"vendor_on_sanctions_list\":false,\n    \"vendor_tax_form_on_file\":true,\n    \"payment_requested_during_business_hours\":true\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 4 if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n2. 70 if amount is above amount_approval_threshold.\n3. 4032 if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: 922.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 4: wait until a document arrives before you move forward with it\n- 4032: cease the operation as it is prohibited\n- 70: get referred to the person who decides\n- 922: continue with the request as nothing obstructs it\nThe record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "4",
   "4032",
   "922"
  ]
 },
 {
  "qid": "q6b3930286d",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-2880\nvendor=Riverbend Labs\npurchase_order_received=true\namount=412.43\npayment_requested_during_business_hours=false\nvendor_tax_form_on_file=true\nduplicate_of_paid_invoice=true\nvendor_on_sanctions_list=true\namount_approval_threshold=1000.00",
  "question": "Proposed action: HDW\nSo, have the facts in the record ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. HDW if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. LB if vendor_on_sanctions_list is true.\n3. L if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: XNNS.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- LB: kill this one off, it is off the table for good\n- XNNS: have the plan kept moving as it was requested\n- HDW: be forwarded to the person in charge\n- L: pause and collect more information first\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9b15a9734f",
  "kind": "choice",
  "text": "---\n# request record\nsubject:\n  invoice_id: \"INV-7228\"\n  vendor: \"Stonebridge Partners\"\namounts:\n  amount: 2262.99\n  amount_approval_threshold: 2500.00\nchecks:\n  awaiting_purchase_order: false\n  vendor_on_sanctions_list: true\n  duplicate_of_paid_invoice: false\n  payment_requested_during_business_hours: true\n  vendor_tax_form_missing: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action below would serve the person who made this request best?",
  "options": [
   "deny",
   "approve",
   "ask manager"
  ]
 },
 {
  "qid": "q749a9383ec",
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
  "qid": "qd0943d2e78",
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
  "qid": "q8820d4291f",
  "kind": "yes/no",
  "text": "invoice_id | INV-8468\nvendor | Brightwater Logistics\nduplicate_of_paid_invoice | false\nawaiting_purchase_order | true\namount | 1106.70\nvendor_on_sanctions_list | false\npayment_requested_during_business_hours | true\namount_approval_threshold | 5000.00\nvendor_tax_form_on_file | true",
  "question": "Proposed action: delay\nDoes the proposed action make sense for the request shown in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel_order if vendor_on_sanctions_list is true.\n3. delay if awaiting_purchase_order is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- release: have the task carried out as it was originally asked\n- delay: keep it in limbo until the verification has been confirmed\n- cancel_order: block this from going any further\n- hand_to_a_person: refer this item to the person who holds decision authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0d74db372e",
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
  "qid": "q3d0b94df76",
  "kind": "yes/no",
  "text": "# case\ninvoice_id                              | INV-1980\nvendor                                  | Summit Works\namount_approval_threshold               | 10000.00\namount                                  | 10000.00\nvendor_tax_form_on_file                 | true\npayment_requested_during_business_hours | true\nduplicate_of_paid_invoice               | false\nvendor_on_sanctions_list                | false\nawaiting_purchase_order                 | false",
  "question": "Proposed action: hold\nHonestly, would you say the proposed action is the right move for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_on_sanctions_list is true.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- escalate: submit it upward to the approver\n- hold: chill until the document turns up\n- reject: reject the petition as the action is unauthorized\n- pay: run the task as it was asked, with nothing standing between it and completion\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q959bf92228",
  "kind": "choice",
  "text": "# record\ninvoice_id: INV-8393\nvendor: Oakmont Logistics\npayment_requested_during_business_hours: true\nvendor_free_of_sanctions: true\namount: 8102.56\nduplicate_of_paid_invoice: false\namount_approval_threshold: 5000.00\npurchase_order_received: true\nvendor_tax_form_missing: false",
  "question": "Meanings:\n- pay: keep going exactly as requested because every obstacle has cleared\n- escalate: forward it to the decision maker\n- reject: send the requester away with the request left unfinished\n- hold: park the file until the requester sends the document in\nThe record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "escalate",
   "pay",
   "hold"
  ]
 },
 {
  "qid": "qf41056e124",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"invoice_id\": \"INV-7266\",\n        \"vendor\": \"Lakeshore Works\"\n    },\n    \"values\": {\n        \"amount_approval_threshold\": 5000.00,\n        \"amount\": 3298.80\n    },\n    \"tests\": {\n        \"vendor_free_of_sanctions\": true,\n        \"vendor_tax_form_on_file\": true,\n        \"awaiting_purchase_order\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"duplicate_of_paid_invoice\": false\n    }\n}",
  "question": "Proposed action: hold\nWould the proposed action be considered the correct disposition of the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: drop this right there, we are not touching it\n- hold: wait so the requester can supply more information first\n- pay: execute the request exactly as written\n- escalate: toss it over to the one who makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf18c2c7295",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-4349\",\n  \"vendor\":\"Cedar Labs\",\n  \"vendor_on_sanctions_list\":false,\n  \"purchase_order_received\":true,\n  \"duplicate_of_paid_invoice\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"amount_approval_threshold\":1000.00,\n  \"amount\":1696.73,\n  \"vendor_tax_form_missing\":false\n}",
  "question": "Proposed action: pay\nIs the proposed action not suited to this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qa54ab3ed6f",
  "kind": "choice",
  "text": "---\n# record\ninvoice_id: \"INV-3407\"\nvendor: \"Copperfield Foods\"\nduplicate_of_paid_invoice: false\npurchase_order_received: true\npayment_requested_during_business_hours: true\namount: 180.04\nvendor_tax_form_missing: false\nvendor_free_of_sanctions: false\namount_approval_threshold: 500.00",
  "question": "Meanings:\n- 6: continue as requested with the path fully open\n- 25: veto this move and leave it there\n- 970: bring in the owner who can rule on this\n- 3690: suspend progress until verification is received\nThe record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "6",
   "25",
   "3690"
  ]
 },
 {
  "qid": "q19581ace51",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-8456\", \"vendor\": \"Harbor Group\", \"amount\": 1420.61, \"amount_approval_threshold\": 10000.00, \"vendor_on_sanctions_list\": false, \"payment_requested_during_business_hours\": false, \"vendor_tax_form_on_file\": true, \"purchase_order_received\": true, \"duplicate_of_paid_invoice\": true}",
  "question": "Proposed action: VHTT\nIs it not the case that, given the record, the proposed action is not a poor call?",
  "definitions": "Meanings:\n- BV: get referred to the person who decides\n- VHTT: go on and finish it the path is clear\n- G: scrap the plan and drop this request\n- VGT: keep their request on hold until more information arrives from them\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q75ebe04621",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"invoice_id\": \"INV-2334\",\n        \"vendor\": \"Redwood Group\"\n    },\n    \"values\": {\n        \"amount_approval_threshold\": 1000.00,\n        \"amount\": 1000.00\n    },\n    \"tests\": {\n        \"vendor_free_of_sanctions\": true,\n        \"duplicate_of_paid_invoice\": false,\n        \"vendor_tax_form_missing\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"awaiting_purchase_order\": false\n    }\n}",
  "question": "Proposed action: ask_manager\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if amount is above amount_approval_threshold.\n2. deny if vendor_free_of_sanctions is false.\n3. defer if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q488ea95828",
  "kind": "choice",
  "text": "# case\ninvoice_id = INV-3806\nvendor = Silverline Traders\npayment_requested_during_business_hours = false\namount_approval_threshold = 2500.00\namount = 1929.40\nvendor_on_sanctions_list = true\nvendor_tax_form_on_file = true\nduplicate_of_paid_invoice = false\npurchase_order_received = true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand to a person if amount is at least amount_approval_threshold.\n2. delay if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. cancel order if duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nWhich of the actions below does the record point to as the right call?",
  "options": [
   "delay",
   "release",
   "cancel order"
  ]
 },
 {
  "qid": "qb1f504e601",
  "kind": "yes/no",
  "text": "---\ncase:\n    invoice_id: \"INV-8722\"\n    vendor: \"Stonebridge Systems\"\nvalues:\n    amount_approval_threshold: 25000.00\n    amount: 9860.78\ntests:\n    payment_requested_during_business_hours: true\n    purchase_order_received: true\n    vendor_free_of_sanctions: true\n    duplicate_of_paid_invoice: false\n    vendor_tax_form_on_file: false",
  "question": "Proposed action: approve\nDo the facts of this request support the proposed action as the correct decision?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qeb29ac74ce",
  "kind": "choice",
  "text": "# record\ninvoice_id: INV-9041\nvendor: Northwind Logistics\namount_approval_threshold: 10000.00\namount: 10000.00\npayment_requested_during_business_hours: true\npurchase_order_received: true\nduplicate_of_paid_invoice: false\nvendor_on_sanctions_list: false\nvendor_tax_form_on_file: true",
  "question": "Meanings:\n- WN: refuse to act since the step is prohibited\n- XQZ: direct the request to the responsible decider\n- B: suspend action until the facts are confirmed\n- DWPJ: just crack on with it there is nothing in the way\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "B",
   "WN",
   "DWPJ"
  ]
 },
 {
  "qid": "qbac4908eed",
  "kind": "choice",
  "text": "---\n# record\ninvoice_id: INV-2048\nvendor: Silverline Partners\nvendor_tax_form_missing: false\namount_approval_threshold: 1000.00\nduplicate_of_paid_invoice: false\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: false\namount: 1000.01\npurchase_order_received: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if purchase_order_received is false or vendor_tax_form_missing is true.\n2. ask manager if amount is above amount_approval_threshold.\n3. deny if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed does the record best support for this request?",
  "options": [
   "deny",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "q5f2a8ad488",
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
  "qid": "qabd5657841",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-2458\n- vendor: Silverline Logistics\n- amount approval threshold: 2500.00\n- vendor tax form missing: no\n- duplicate of paid invoice: no\n- payment requested during business hours: yes\n- amount: 2500.01\n- awaiting purchase order: no\n- vendor on sanctions list: no",
  "question": "Proposed action: delay\nFitting the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. cancel order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_tax_form_missing is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe40e37ab65",
  "kind": "choice",
  "text": "# request record\ninvoice_id = INV-4761\nvendor = Bluepeak Partners\nvendor_on_sanctions_list = false\namount = 845.15\npurchase_order_received = false\nvendor_tax_form_missing = false\namount_approval_threshold = 500.00\npayment_requested_during_business_hours = true\nduplicate_of_paid_invoice = false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if purchase_order_received is false or vendor_tax_form_missing is true.\n2. ask manager if amount is above amount_approval_threshold.\n3. deny if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- deny: veto this move and leave it there\n- approve: run the requested step through\n- ask manager: route the case to a decider so the requester knows the outcome\n- defer: wait for that check then we will see\nThe record is complete: nothing else applies.\n\nWhich of the actions below answers the request given the facts you can see?",
  "options": [
   "defer",
   "deny",
   "approve"
  ]
 },
 {
  "qid": "q2bd516831a",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-3222\", \"vendor\": \"Copperfield Logistics\", \"vendor_tax_form_on_file\": false, \"amount\": 305.63, \"vendor_on_sanctions_list\": false, \"awaiting_purchase_order\": false, \"duplicate_of_paid_invoice\": false, \"amount_approval_threshold\": 500.00, \"payment_requested_during_business_hours\": true}",
  "question": "Proposed action: cancel_order\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q3a6758c0db",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id = INV-1320\nvendor = Northwind Works\nduplicate_of_paid_invoice = false\nvendor_free_of_sanctions = true\npayment_requested_during_business_hours = false\namount_approval_threshold = 10000.00\nvendor_tax_form_on_file = true\namount = 4217.65\npurchase_order_received = true",
  "question": "Proposed action: send to a person\nReviewing this file as an auditor, is the proposed action not the correct step?",
  "definitions": "Meanings:\n- go ahead: proceed with the request since the way is clear and nothing blocks it\n- send to a person: direct the request to the responsible decider\n- put on hold: hold the request so the requester waits for their check\n- turn down: be turned away and treated as off limits\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc5ccd762ae",
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
  "qid": "qbdfca0c2ae",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-2865\n- vendor: Harbor Supply\n- amount approval threshold: 25000.00\n- purchase order received: yes\n- vendor free of sanctions: no\n- vendor tax form missing: no\n- payment requested during business hours: yes\n- amount: 3659.70\n- duplicate of paid invoice: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if amount is above amount_approval_threshold.\n2. turn down if vendor_free_of_sanctions is false.\n3. put on hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: go ahead.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- send to a person: give it to the person in charge of the call\n- put on hold: hold up for a sec until more info comes in\n- go ahead: complete the job as it was assigned\n- turn down: block the action because it is off limits to the team\nThe record is complete: nothing else applies.\n\nChecklist item: which of the actions listed below is the right call for the request?",
  "options": [
   "turn down",
   "go ahead",
   "put on hold"
  ]
 },
 {
  "qid": "qf33dbc1e8c",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-8775\", \"vendor\": \"Bluepeak Foods\", \"vendor_free_of_sanctions\": true, \"payment_requested_during_business_hours\": false, \"amount\": 5000.00, \"amount_approval_threshold\": 5000.00, \"duplicate_of_paid_invoice\": false, \"purchase_order_received\": true, \"vendor_tax_form_on_file\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 87 if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. 2461 if vendor_free_of_sanctions is false.\n3. 2 if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: 829.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 829: finish what was asked as stated, the way ahead is fully free\n- 2461: halt the request at this point\n- 87: pass the request along since the decision belongs to another person\n- 2: pause and collect more information first\nThe record is complete: nothing else applies.\n\nWhich listed action is the best call for the request?",
  "options": [
   "87",
   "2",
   "829"
  ]
 },
 {
  "qid": "qfb32c7b031",
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
  "qid": "qf1c259f74a",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-5281\nvendor = Cedar Industries\namount_approval_threshold = 25000.00\npayment_requested_during_business_hours = true\nvendor_tax_form_on_file = true\nvendor_on_sanctions_list = false\namount = 25000.00\nawaiting_purchase_order = true\nduplicate_of_paid_invoice = false",
  "question": "Proposed action: approve\nIs the proposed action not the right move, given what the record shows?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n2. ask manager if amount is above amount_approval_threshold.\n3. deny if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- ask manager: route this matter to the individual empowered to decide\n- approve: go ahead and the requester will be served\n- defer: defer the step until the verification is in\n- deny: be stopped and never carried out\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa9340b696e",
  "kind": "yes/no",
  "text": "---\n# extract\ninvoice_id: INV-2187\nvendor: Lakeshore Industries\nvendor_tax_form_on_file: false\nduplicate_of_paid_invoice: false\namount_approval_threshold: 1000.00\npayment_requested_during_business_hours: true\nawaiting_purchase_order: false\nvendor_free_of_sanctions: true\namount: 683.97",
  "question": "Proposed action: cancel order\nLooking at this, is the proposed action not the right thing to do?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qe3b32950f7",
  "kind": "yes/no",
  "text": "---\n# request record\ninvoice_id: \"INV-3909\"\nvendor: \"Lakeshore Foods\"\nvendor_free_of_sanctions: true\namount_approval_threshold: 1000.00\nawaiting_purchase_order: false\npayment_requested_during_business_hours: true\namount: 1000.00\nduplicate_of_paid_invoice: false\nvendor_tax_form_missing: false",
  "question": "Proposed action: go_ahead\nAs a reviewer checking the file, is the proposed action not a sound decision here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. send_to_a_person if amount is above amount_approval_threshold.\n3. turn_down if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0de57edcb2",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  invoice_id: INV-6710\n  vendor: Ironleaf Traders\nnumbers:\n  amount_approval_threshold: 5000.00\n  amount: 4999.99\nflags:\n  vendor_tax_form_missing: false\n  vendor_on_sanctions_list: false\n  payment_requested_during_business_hours: true\n  duplicate_of_paid_invoice: false\n  purchase_order_received: true",
  "question": "Proposed action: 20\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 721 if amount is at least amount_approval_threshold.\n2. 1 if duplicate_of_paid_invoice is true.\n3. 1065 if vendor_on_sanctions_list is true.\nOtherwise: 20.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- 20: keep moving on this one nothing is holding it up\n- 1: shut this down before it spreads into the workflow\n- 1065: hand this to the person who decides\n- 721: wait for the check and the requester will hear back later\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q294f087915",
  "kind": "choice",
  "text": "invoice_id: INV-1377\nvendor: Stonebridge Labs\namount: 500.01\namount_approval_threshold: 500.00\nduplicate_of_paid_invoice: false\npurchase_order_received: true\nvendor_free_of_sanctions: true\npayment_requested_during_business_hours: false\nvendor_tax_form_missing: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if purchase_order_received is false or vendor_tax_form_missing is true.\n2. escalate if amount is above amount_approval_threshold.\n3. reject if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "escalate",
   "reject",
   "hold"
  ]
 },
 {
  "qid": "q6c639b5803",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-2585\", \"vendor\": \"Copperfield Partners\", \"amount\": 10000.00, \"vendor_tax_form_missing\": false, \"vendor_on_sanctions_list\": false, \"duplicate_of_paid_invoice\": false, \"purchase_order_received\": true, \"amount_approval_threshold\": 10000.00, \"payment_requested_during_business_hours\": true}",
  "question": "Meanings:\n- FM: hold off until the check has been completed by the team\n- NJJC: leave the requester without the result they asked for\n- D: escalate the matter to the accountable decision maker\n- SGP: execute the request exactly as written\nThe record is complete: nothing else applies.\n\nHey, which of the actions listed after this question is the right call here?",
  "options": [
   "D",
   "SGP",
   "FM"
  ]
 },
 {
  "qid": "qc44fc38488",
  "kind": "yes/no",
  "text": "# request record\ninvoice_id: INV-2549\nvendor: Harbor Foods\namount_approval_threshold: 500.00\npayment_requested_during_business_hours: true\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: false\nawaiting_purchase_order: false\nvendor_tax_form_on_file: true\namount: 500.01",
  "question": "Proposed action: pay\nWould the proposed action be not the right choice here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: awaiting_purchase_order, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- reject: be halted at once and left unperformed\n- pay: complete the job as it was assigned\n- escalate: forward it to the decision maker\n- hold: be paused until a document has been received\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd77b407fa3",
  "kind": "yes/no",
  "text": "---\nrequest:\n  invoice_id: INV-9994\n  vendor: Riverbend Systems\nfigures:\n  amount: 350.92\n  amount_approval_threshold: 2500.00\nchecks:\n  vendor_tax_form_missing: true\n  duplicate_of_paid_invoice: false\n  awaiting_purchase_order: false\n  vendor_free_of_sanctions: false\n  payment_requested_during_business_hours: true",
  "question": "Proposed action: release\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if amount is at least amount_approval_threshold.\n2. cancel order if duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_free_of_sanctions is false.\nOtherwise: release.\nNever counted: awaiting_purchase_order, vendor_tax_form_missing, payment_requested_during_business_hours.\nMeanings:\n- release: go on and finish it the path is clear\n- hand to a person: escalate the matter to the accountable decision maker\n- cancel order: halt this item because the rules forbid it\n- delay: pump the brakes until more details show up\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5f498c8418",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id: INV-5161\nvendor: Riverbend Works\namount: 346.76\npayment_requested_during_business_hours: true\namount_approval_threshold: 500.00\nduplicate_of_paid_invoice: false\nvendor_on_sanctions_list: true\nvendor_tax_form_missing: false\npurchase_order_received: false",
  "question": "Proposed action: hold\nTell me, has the record ruled out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if vendor_tax_form_missing is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_on_sanctions_list is true.\n3. hold if purchase_order_received is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: drop this request from the queue\n- hold: park the file until the requester sends the document in\n- escalate: transfer it to the person with authority\n- pay: press on with the work as originally set\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe7ca723f14",
  "kind": "yes/no",
  "text": "{\n  \"record\":{\n    \"invoice_id\":\"INV-2836\",\n    \"vendor\":\"Stonebridge Foods\"\n  },\n  \"numbers\":{\n    \"amount_approval_threshold\":2500.00,\n    \"amount\":2500.00\n  },\n  \"flags\":{\n    \"payment_requested_during_business_hours\":true,\n    \"vendor_tax_form_on_file\":true,\n    \"duplicate_of_paid_invoice\":false,\n    \"vendor_on_sanctions_list\":true,\n    \"awaiting_purchase_order\":false\n  }\n}",
  "question": "Proposed action: cancel_order\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel_order if vendor_on_sanctions_list is true.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8f3e1e3522",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-3883\",\"vendor\":\"Harbor Industries\",\"payment_requested_during_business_hours\":true,\"awaiting_purchase_order\":false,\"amount\":14605.88,\"amount_approval_threshold\":25000.00,\"vendor_free_of_sanctions\":false,\"vendor_tax_form_missing\":false,\"duplicate_of_paid_invoice\":false}",
  "question": "Meanings:\n- deny: shut this down right away, we are staying clear of it\n- approve: go ahead with the requested action\n- ask manager: transfer the case to the responsible decision maker for determination\n- defer: hold up for a sec until more info comes in\nThe record is complete: nothing else applies.\n\nIf you were deciding, which of the actions listed after this fits best?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q83c6b92219",
  "kind": "choice",
  "text": "# request record\ninvoice_id | INV-8526\nvendor | Northwind Foods\npurchase_order_received | true\nvendor_tax_form_missing | false\namount | 500.01\nvendor_on_sanctions_list | false\npayment_requested_during_business_hours | true\namount_approval_threshold | 500.00\nduplicate_of_paid_invoice | false",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "cancel order",
   "hand to a person",
   "release"
  ]
 }
]
