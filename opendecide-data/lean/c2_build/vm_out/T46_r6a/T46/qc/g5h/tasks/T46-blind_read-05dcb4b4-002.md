# G5-H blind read T46-blind_read-05dcb4b4-002 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r6a/T46/qc/g5h/answers/T46-blind_read-05dcb4b4-002.json

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
  "qid": "q15a31e4b54",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-8164\nvendor=Brightwater Traders\nduplicate_of_paid_invoice=false\namount=1158.87\npayment_requested_during_business_hours=false\npurchase_order_received=false\nvendor_tax_form_missing=false\namount_approval_threshold=10000.00\nvendor_on_sanctions_list=false",
  "question": "Proposed action: 63\nDo the facts here rule out the proposed action?",
  "definitions": "Meanings:\n- 938: shelve the matter until more details come in\n- 8: reject the request in full\n- 63: continue the work as originally asked, there is nothing in the way\n- 2141: get the boss to make the final call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5b776d06e3",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-3570\n- vendor: Silverline Labs\n- awaiting purchase order: no\n- amount: 25000.00\n- vendor on sanctions list: no\n- duplicate of paid invoice: yes\n- payment requested during business hours: yes\n- vendor tax form on file: yes\n- amount approval threshold: 25000.00",
  "question": "Proposed action: put_on_hold\nDoes the evidence in the record rule out the proposed action as a choice?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q965cbf261a",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-1823\nvendor = Fairview Industries\nduplicate_of_paid_invoice = false\nawaiting_purchase_order = false\nvendor_on_sanctions_list = false\npayment_requested_during_business_hours = false\namount_approval_threshold = 1000.00\namount = 338.05\nvendor_tax_form_on_file = false",
  "question": "Proposed action: 69\nIs it not the case that, given the record, the proposed action is not a poor call?",
  "definitions": "Meanings:\n- 932: hand it up to the person who decides\n- 1: run the requested step through\n- 3122: be held back until a check or document arrives\n- 69: end this here and now\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qffb857d878",
  "kind": "yes/no",
  "text": "# request record\ninvoice_id: INV-2549\nvendor: Harbor Foods\namount_approval_threshold: 500.00\npayment_requested_during_business_hours: true\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: false\nawaiting_purchase_order: false\nvendor_tax_form_on_file: true\namount: 499.99",
  "question": "Proposed action: pay\nIs it not so that the proposed action is not at odds with the facts and the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if amount is at least amount_approval_threshold.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_on_sanctions_list is true.\nOtherwise: pay.\nNever counted: awaiting_purchase_order, vendor_tax_form_on_file, payment_requested_during_business_hours.\nMeanings:\n- reject: be halted at once and left unperformed\n- pay: complete the job as it was assigned\n- escalate: forward it to the decision maker\n- hold: be paused until a document has been received\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qae00fa83d8",
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
  "qid": "q1090469747",
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
  "qid": "q63d4adebea",
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
  "qid": "qb20d26ea80",
  "kind": "yes/no",
  "text": "---\n# record\nmeta:\n    invoice_id: \"INV-8817\"\n    vendor: \"Stonebridge Labs\"\nmetrics:\n    amount_approval_threshold: 5000.00\n    amount: 904.23\nsignals:\n    vendor_tax_form_on_file: true\n    payment_requested_during_business_hours: true\n    purchase_order_received: false\n    vendor_free_of_sanctions: true\n    duplicate_of_paid_invoice: true",
  "question": "Proposed action: put on hold\nIs it not the case that the proposed action is not a poor choice for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. turn down if vendor_free_of_sanctions is false.\n3. put on hold if purchase_order_received is false.\nOtherwise: go ahead.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qecc53eb162",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n    invoice_id: INV-4968\n    vendor: Bluepeak Partners\namounts:\n    amount: 1010.58\n    amount_approval_threshold: 5000.00\nchecks:\n    duplicate_of_paid_invoice: false\n    vendor_tax_form_on_file: false\n    purchase_order_received: true\n    payment_requested_during_business_hours: true\n    vendor_on_sanctions_list: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 507 if purchase_order_received is false or vendor_tax_form_on_file is false.\n2. 9 if amount is above amount_approval_threshold.\n3. 56 if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: 1467.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 507: hold up for a sec until more info comes in\n- 9: forward it to the decision maker\n- 56: halt the request at this point\n- 1467: carry on with it now\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "1467",
   "9",
   "507"
  ]
 },
 {
  "qid": "q072c6874ad",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-4531\n- vendor: Ironleaf Industries\n- vendor tax form missing: no\n- vendor on sanctions list: no\n- amount: 276.00\n- awaiting purchase order: no\n- payment requested during business hours: no\n- amount approval threshold: 500.00\n- duplicate of paid invoice: no",
  "question": "Meanings:\n- hold: hold up for a sec until more info comes in\n- escalate: escalate this to someone senior who decides\n- reject: block this from going any further\n- pay: go ahead and the requester will be served\nThe record is complete: nothing else applies.\n\nMind telling me which of the actions below is the best call for this request?",
  "options": [
   "hold",
   "pay",
   "reject"
  ]
 },
 {
  "qid": "q8bbeb7221a",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-2585\", \"vendor\": \"Copperfield Partners\", \"amount\": 10000.01, \"vendor_tax_form_missing\": false, \"vendor_on_sanctions_list\": false, \"duplicate_of_paid_invoice\": false, \"purchase_order_received\": true, \"amount_approval_threshold\": 10000.00, \"payment_requested_during_business_hours\": true}",
  "question": "Meanings:\n- FM: hold off until the check has been completed by the team\n- NJJC: leave the requester without the result they asked for\n- D: escalate the matter to the accountable decision maker\n- SGP: execute the request exactly as written\nThe record is complete: nothing else applies.\n\nHey, which of the actions listed after this question is the right call here?",
  "options": [
   "D",
   "SGP",
   "FM"
  ]
 },
 {
  "qid": "q9308b5ff1e",
  "kind": "yes/no",
  "text": "---\ninvoice_id: \"INV-6967\"\nvendor: \"Summit Foods\"\namount: 442.15\nduplicate_of_paid_invoice: false\nvendor_tax_form_missing: false\namount_approval_threshold: 500.00\nvendor_on_sanctions_list: true\nawaiting_purchase_order: false\npayment_requested_during_business_hours: false",
  "question": "Proposed action: deny\nQuick check: do the facts in the record rule out the proposed action here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if amount is above amount_approval_threshold.\n2. deny if vendor_on_sanctions_list is true.\n3. defer if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4cae7c87eb",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id | INV-9819\nvendor | Riverbend Systems\npayment_requested_during_business_hours | true\npurchase_order_received | true\namount | 561.86\nvendor_free_of_sanctions | true\nvendor_tax_form_missing | false\nduplicate_of_paid_invoice | false\namount_approval_threshold | 500.00",
  "question": "Proposed action: defer\nBe honest, do the facts here rule out the proposed action?",
  "definitions": "Meanings:\n- ask_manager: hand this to the person who decides\n- defer: hold the request so the requester waits for their check\n- deny: halt this item because the rules forbid it\n- approve: carry on with it now\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5bf08b7448",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-3684\n- vendor: Silverline Partners\n- awaiting purchase order: yes\n- amount: 5000.00\n- amount approval threshold: 5000.00\n- vendor on sanctions list: no\n- payment requested during business hours: yes\n- vendor tax form missing: no\n- duplicate of paid invoice: no",
  "question": "Proposed action: defer\nDoes the evidence in the record rule out the proposed action as a choice?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qbfd4b80dd2",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-1845\nvendor=Silverline Labs\namount_approval_threshold=5000.00\namount=4899.72\nvendor_tax_form_missing=false\npayment_requested_during_business_hours=true\nawaiting_purchase_order=false\nduplicate_of_paid_invoice=false\nvendor_free_of_sanctions=false",
  "question": "Proposed action: reject\nDoes what we know about this rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. reject if vendor_free_of_sanctions is false.\n2. escalate if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. hold if amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- escalate: escalate it so the person asking receives a decision\n- pay: continue with the request as nothing obstructs it\n- reject: block it right away\n- hold: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q667a76f372",
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
  "qid": "q7bbb747994",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id                              | INV-3141\nvendor                                  | Harbor Supply\npurchase_order_received                 | true\nvendor_tax_form_missing                 | false\nvendor_free_of_sanctions                | false\nduplicate_of_paid_invoice               | false\namount_approval_threshold               | 10000.00\npayment_requested_during_business_hours | true\namount                                  | 4469.79",
  "question": "Proposed action: cancel_order\nIs it not so that the proposed action is not mistaken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel_order if vendor_free_of_sanctions is false.\n2. hand_to_a_person if purchase_order_received is false or vendor_tax_form_missing is true.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q607b95a370",
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
  "qid": "qda021afe9a",
  "kind": "choice",
  "text": "# request record\ninvoice_id                              | INV-6425\nvendor                                  | Oakmont Works\namount                                  | 4628.90\nvendor_on_sanctions_list                | false\namount_approval_threshold               | 5000.00\npayment_requested_during_business_hours | true\nvendor_tax_form_on_file                 | true\nduplicate_of_paid_invoice               | true\npurchase_order_received                 | true",
  "question": "The record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "deny",
   "ask_manager",
   "approve"
  ]
 },
 {
  "qid": "q4398c3535b",
  "kind": "yes/no",
  "text": "invoice_id: INV-9529\nvendor: Fairview Systems\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: true\namount_approval_threshold: 5000.00\nvendor_on_sanctions_list: true\namount: 4027.05\nawaiting_purchase_order: false\nvendor_tax_form_missing: false",
  "question": "Proposed action: deny\nBased on the record, can it be said the proposed action is not the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q2f38b66178",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-6787\",\n  \"vendor\":\"Harbor Supply\",\n  \"awaiting_purchase_order\":false,\n  \"vendor_tax_form_missing\":false,\n  \"vendor_free_of_sanctions\":true,\n  \"duplicate_of_paid_invoice\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"amount_approval_threshold\":1000.00,\n  \"amount\":289.48\n}",
  "question": "Proposed action: hand_to_a_person\nIs it not correct that the proposed action is not an error given what the record shows?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. cancel_order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. hand_to_a_person if vendor_tax_form_missing is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- cancel_order: bin this idea and keep it out of the flow\n- release: proceed with the task as asked\n- delay: wait for the document to come through\n- hand_to_a_person: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5d5d071082",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-1823\nvendor = Fairview Industries\nduplicate_of_paid_invoice = false\nawaiting_purchase_order = false\nvendor_on_sanctions_list = false\npayment_requested_during_business_hours = false\namount_approval_threshold = 1000.00\namount = 338.05\nvendor_tax_form_on_file = false",
  "question": "Proposed action: 69\nWould the proposed action be not the right choice here?",
  "definitions": "Meanings:\n- 932: hand it up to the person who decides\n- 1: run the requested step through\n- 3122: be held back until a check or document arrives\n- 69: end this here and now\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7fd200304a",
  "kind": "choice",
  "text": "---\n# request record\ninvoice_id: \"INV-7145\"\nvendor: \"Bluepeak Labs\"\nvendor_on_sanctions_list: false\namount: 687.73\namount_approval_threshold: 500.00\nvendor_tax_form_on_file: true\nawaiting_purchase_order: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "reject",
   "escalate",
   "pay"
  ]
 },
 {
  "qid": "q7f12ef677d",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-5596\nvendor=Lakeshore Partners\npurchase_order_received=true\namount_approval_threshold=1000.00\nvendor_on_sanctions_list=true\npayment_requested_during_business_hours=true\nvendor_tax_form_on_file=true\namount=1799.28\nduplicate_of_paid_invoice=false",
  "question": "Proposed action: QDMF\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QDMF if purchase_order_received is false.\n2. PDR if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. DF if vendor_tax_form_on_file is false or amount is above amount_approval_threshold.\nOtherwise: F.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- DF: be handed over to the deciding person\n- F: proceed with the request since the way is clear and nothing blocks it\n- QDMF: stall the request until the check comes back\n- PDR: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q55c46e5c14",
  "kind": "yes/no",
  "text": "invoice_id | INV-5424\nvendor | Bluepeak Systems\namount_approval_threshold | 10000.00\npurchase_order_received | false\nduplicate_of_paid_invoice | false\nvendor_on_sanctions_list | false\namount | 10000.00\npayment_requested_during_business_hours | true\nvendor_tax_form_on_file | true",
  "question": "Proposed action: PD\nDo the record's facts rule out the proposed action entirely?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. PD if purchase_order_received is false or vendor_tax_form_on_file is false.\n2. XWW if amount is above amount_approval_threshold.\n3. FLFH if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\nOtherwise: Q.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- XWW: give it to a person who has the authority to decide\n- PD: hold up for a sec until more info comes in\n- FLFH: be blocked outright so it never gets carried out\n- Q: proceed as requested as nothing impedes this course\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3955403263",
  "kind": "yes/no",
  "text": "---\nmeta:\n  invoice_id: \"INV-7487\"\n  vendor: \"Copperfield Works\"\nmetrics:\n  amount_approval_threshold: 25000.00\n  amount: 12633.16\nsignals:\n  vendor_on_sanctions_list: true\n  vendor_tax_form_on_file: true\n  awaiting_purchase_order: false\n  duplicate_of_paid_invoice: false\n  payment_requested_during_business_hours: true",
  "question": "Proposed action: approve\nDo the details shown in the record rule out the proposed action here?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q75551a9ee6",
  "kind": "choice",
  "text": "# case\ninvoice_id = INV-4531\nvendor = Ironleaf Industries\nduplicate_of_paid_invoice = false\nvendor_on_sanctions_list = false\nawaiting_purchase_order = false\npayment_requested_during_business_hours = false\nvendor_tax_form_missing = false\namount_approval_threshold = 500.00\namount = 276.00",
  "question": "Meanings:\n- hold: hold up for a sec until more info comes in\n- escalate: escalate this to someone senior who decides\n- reject: block this from going any further\n- pay: go ahead and the requester will be served\nThe record is complete: nothing else applies.\n\nMind telling me which of the actions below is the best call for this request?",
  "options": [
   "hold",
   "pay",
   "reject"
  ]
 },
 {
  "qid": "q29ca78406c",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-1823\", \"vendor\": \"Bluepeak Traders\", \"amount_approval_threshold\": 5000.00, \"payment_requested_during_business_hours\": true, \"vendor_tax_form_on_file\": true, \"vendor_free_of_sanctions\": true, \"amount\": 3690.56, \"purchase_order_received\": true, \"duplicate_of_paid_invoice\": false}",
  "question": "Proposed action: put on hold\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q138156c8fb",
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
  "qid": "q56afe2e48f",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-4979\nvendor | Pinecrest Foods\nduplicate_of_paid_invoice | false\npayment_requested_during_business_hours | true\nvendor_on_sanctions_list | false\nawaiting_purchase_order | true\namount_approval_threshold | 25000.00\namount | 5785.90\nvendor_tax_form_missing | false",
  "question": "Proposed action: release\nHonestly, would you say the proposed action is the right move for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q0e4ab86c25",
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
  "qid": "qd1c5e2eeb2",
  "kind": "yes/no",
  "text": "{\n    \"record\":{\n        \"invoice_id\":\"INV-1421\",\n        \"vendor\":\"Riverbend Supply\"\n    },\n    \"numbers\":{\n        \"amount\":2500.00,\n        \"amount_approval_threshold\":2500.00\n    },\n    \"flags\":{\n        \"purchase_order_received\":true,\n        \"vendor_tax_form_on_file\":true,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_free_of_sanctions\":false,\n        \"duplicate_of_paid_invoice\":false\n    }\n}",
  "question": "Proposed action: pay\nIs the proposed action the suitable determination for the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: drop this request from the queue\n- hold: stay put until the check is finished\n- pay: run with it carry on as you were\n- escalate: pass the request to a decider\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7bebfe7817",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-9792\",\"vendor\":\"Brightwater Systems\",\"vendor_on_sanctions_list\":false,\"amount\":11957.09,\"vendor_tax_form_on_file\":false,\"duplicate_of_paid_invoice\":false,\"purchase_order_received\":true,\"amount_approval_threshold\":25000.00,\"payment_requested_during_business_hours\":true}",
  "question": "Meanings:\n- SKCS: withhold action until supporting information is supplied\n- JQ: ditch the whole thing, nobody should act on it\n- JQL: hand this to the person who decides\n- J: press on with the work as originally set\nThe record is complete: nothing else applies.\n\nWhich of these actions should be taken for this request?",
  "options": [
   "SKCS",
   "JQL",
   "JQ"
  ]
 },
 {
  "qid": "q2170dda987",
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
  "qid": "q6f17bd09d4",
  "kind": "choice",
  "text": "---\nmeta:\n  invoice_id: \"INV-7459\"\n  vendor: \"Silverline Logistics\"\nmetrics:\n  amount: 174.53\n  amount_approval_threshold: 500.00\nsignals:\n  awaiting_purchase_order: false\n  duplicate_of_paid_invoice: false\n  payment_requested_during_business_hours: false\n  vendor_on_sanctions_list: true\n  vendor_tax_form_missing: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QDDH if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. SN if vendor_on_sanctions_list is true.\n3. XRF if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: Z.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- Z: go ahead with the requested action\n- QDDH: forward the case to the designated decision maker\n- XRF: hang tight until we get the check back\n- SN: stop the request so the requester gets nothing from it\nThe record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "QDDH",
   "SN",
   "Z"
  ]
 },
 {
  "qid": "qd448358cbd",
  "kind": "choice",
  "text": "{\n  \"invoice_id\": \"INV-7560\",\n  \"vendor\": \"Lakeshore Group\",\n  \"vendor_tax_form_missing\": false,\n  \"payment_requested_during_business_hours\": false,\n  \"purchase_order_received\": true,\n  \"vendor_on_sanctions_list\": false,\n  \"amount\": 5000.01,\n  \"duplicate_of_paid_invoice\": false,\n  \"amount_approval_threshold\": 5000.00\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand to a person if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. cancel order if vendor_on_sanctions_list is true.\n3. delay if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "release",
   "hand to a person",
   "delay"
  ]
 },
 {
  "qid": "q7fc3c1d24a",
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
  "qid": "qf786f429d0",
  "kind": "yes/no",
  "text": "{\n    \"invoice_id\":\"INV-4458\",\n    \"vendor\":\"Riverbend Industries\",\n    \"vendor_tax_form_on_file\":true,\n    \"amount\":807.83,\n    \"amount_approval_threshold\":1000.00,\n    \"vendor_free_of_sanctions\":true,\n    \"duplicate_of_paid_invoice\":true,\n    \"payment_requested_during_business_hours\":true,\n    \"purchase_order_received\":true\n}",
  "question": "Proposed action: hold\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- hold: park the file until the requester sends the document in\n- reject: refuse this request entirely\n- pay: continue so the requester receives the result\n- escalate: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q38f76882ad",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id = INV-7530\nvendor = Bluepeak Systems\nvendor_tax_form_on_file = true\namount_approval_threshold = 25000.00\npurchase_order_received = true\nduplicate_of_paid_invoice = false\namount = 20256.62\npayment_requested_during_business_hours = false\nvendor_free_of_sanctions = true",
  "question": "Proposed action: pay\nWould what the record shows make the proposed action the right call here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. reject if vendor_free_of_sanctions is false.\n3. hold if purchase_order_received is false or vendor_tax_form_on_file is false.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- reject: bin this idea and keep it out of the flow\n- hold: pump the brakes until more details show up\n- escalate: send it up so the requester gets a firm decision\n- pay: go on and finish it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1581954df4",
  "kind": "choice",
  "text": "invoice_id=INV-9327\nvendor=Bluepeak Traders\nvendor_tax_form_missing=false\nduplicate_of_paid_invoice=false\nawaiting_purchase_order=false\nvendor_free_of_sanctions=true\npayment_requested_during_business_hours=false\namount=508.92\namount_approval_threshold=1000.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel order if vendor_free_of_sanctions is false.\n2. hand to a person if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. delay if amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed under the record would the requester see as the right call?",
  "options": [
   "delay",
   "release",
   "cancel order"
  ]
 },
 {
  "qid": "qbd05438c5e",
  "kind": "choice",
  "text": "{\n  \"subject\": {\n    \"invoice_id\": \"INV-6807\",\n    \"vendor\": \"Copperfield Industries\"\n  },\n  \"amounts\": {\n    \"amount\": 2262.07,\n    \"amount_approval_threshold\": 2500.00\n  },\n  \"checks\": {\n    \"purchase_order_received\": true,\n    \"duplicate_of_paid_invoice\": true,\n    \"vendor_tax_form_missing\": false,\n    \"payment_requested_during_business_hours\": false,\n    \"vendor_on_sanctions_list\": true\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. VD if amount is above amount_approval_threshold.\n2. KSWZ if vendor_on_sanctions_list is true.\n3. SBX if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: G.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nMeanings:\n- G: carry out the task as instructed without any obstacle\n- VD: send it up to the person who makes the call\n- KSWZ: drop it right away\n- SBX: hold off until the check clears\nThe record is complete: nothing else applies.\n\nTaking the actions listed into account, what is the right call for the request?",
  "options": [
   "VD",
   "KSWZ",
   "G"
  ]
 },
 {
  "qid": "qfdb42a3dcf",
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
  "qid": "qf5a82645b8",
  "kind": "choice",
  "text": "---\ninvoice_id: \"INV-9018\"\nvendor: \"Cedar Traders\"\nduplicate_of_paid_invoice: false\nvendor_free_of_sanctions: true\namount_approval_threshold: 1000.00\nvendor_tax_form_on_file: true\namount: 1000.01\npayment_requested_during_business_hours: true\nawaiting_purchase_order: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if amount is at least amount_approval_threshold.\n2. delay if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. cancel_order if duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours.\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "cancel_order",
   "release",
   "hand_to_a_person"
  ]
 },
 {
  "qid": "q840cb2486e",
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
  "qid": "q692975e684",
  "kind": "yes/no",
  "text": "{\n  \"case\": {\n    \"invoice_id\": \"INV-8797\",\n    \"vendor\": \"Cedar Logistics\"\n  },\n  \"values\": {\n    \"amount\": 175.57,\n    \"amount_approval_threshold\": 500.00\n  },\n  \"tests\": {\n    \"vendor_on_sanctions_list\": false,\n    \"payment_requested_during_business_hours\": true,\n    \"awaiting_purchase_order\": true,\n    \"duplicate_of_paid_invoice\": false,\n    \"vendor_tax_form_missing\": false\n  }\n}",
  "question": "Proposed action: 3725\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 9 if duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n2. 842 if vendor_on_sanctions_list is true.\n3. 3725 if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: 58.\nNever counted: payment_requested_during_business_hours.\nMeanings:\n- 9: give it to a person who has the authority to decide\n- 3725: shelve the matter until more details come in\n- 842: block it right away\n- 58: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qea86b21677",
  "kind": "choice",
  "text": "invoice_id: INV-2514\nvendor: Ironleaf Labs\namount: 4570.79\npurchase_order_received: true\namount_approval_threshold: 5000.00\npayment_requested_during_business_hours: false\nvendor_tax_form_on_file: true\nduplicate_of_paid_invoice: true\nvendor_free_of_sanctions: true",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed after this is the most suitable for the request?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q3cb06fcfb5",
  "kind": "yes/no",
  "text": "# record\ninvoice_id: INV-5470\nvendor: Cedar Supply\namount: 1452.26\nvendor_on_sanctions_list: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\npurchase_order_received: true\namount_approval_threshold: 1000.00\nvendor_tax_form_on_file: true",
  "question": "Proposed action: defer\nIs it not true that the proposed action is not off target for the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if vendor_on_sanctions_list is true.\n2. ask_manager if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. defer if amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd15a2c2f22",
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
  "qid": "q2abb8b5fda",
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
  "qid": "q2ac446e7bf",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-8850\nvendor = Bluepeak Works\npayment_requested_during_business_hours = true\nduplicate_of_paid_invoice = false\nvendor_tax_form_on_file = true\nvendor_on_sanctions_list = false\namount = 4584.60\nawaiting_purchase_order = false\namount_approval_threshold = 10000.00",
  "question": "Proposed action: pay\nIs the proposed action not really the right move for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if amount is at least amount_approval_threshold.\n2. hold if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. reject if duplicate_of_paid_invoice is true.\nOtherwise: pay.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours.\nMeanings:\n- reject: stop the request so the requester gets nothing from it\n- pay: carry out the request as written\n- escalate: send it onward because someone else must decide\n- hold: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 }
]
