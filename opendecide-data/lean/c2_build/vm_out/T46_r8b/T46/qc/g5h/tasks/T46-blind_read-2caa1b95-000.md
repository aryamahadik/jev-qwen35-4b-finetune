# G5-H blind read T46-blind_read-2caa1b95-000 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8b/T46/qc/g5h/answers/T46-blind_read-2caa1b95-000.json

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
  "qid": "q8fe57de878",
  "kind": "yes/no",
  "text": "ticket_id=TCK-7826\ncustomer=Zoe Moreau\nfree_of_legal_complaints=true\nharmless_greeting_present_in_the_message=true\nclaim_form_filled_in_with_the_usual_font=true\nclaim_amount=156.29\ncustomer_message_is_short=true\nproof_of_purchase_attached=true\nfree_of_safety_incident_reports=false\nclaim_free_of_ombudsman_cases=true\nclaim_involves_a_media_inquiry=false\nitem_excluded_by_policy=false\ncustomer_message_written_in_a_formal_tone=false\nitem_return_received=true\nclaim_amount_hard_limit=200.00",
  "question": "Proposed action: cancel\nIs the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. wait if proof_of_purchase_attached is false or claim_involves_a_media_inquiry is true.\n3. ask a human if item_return_received is false or free_of_legal_complaints is false or free_of_safety_incident_reports is false.\nOtherwise: proceed.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q68cdc67438",
  "kind": "yes/no",
  "text": "# record\nticket_id | TCK-1104\ncustomer | Elena Castell\ncustomer_message_written_in_a_casual_tone | true\nclaim_amount_hard_limit | 2000.00\nfree_of_safety_incident_reports | true\nclaim_form_filled_in_with_the_usual_font | true\nclaim_free_of_ombudsman_cases | true\ncustomer_message_is_short | true\nclaim_amount | 640.15\nclaim_involves_a_media_inquiry | false\nitem_excluded_by_policy | false\nharmless_greeting_present_in_the_message | false\nitem_return_received | true\nproof_of_purchase_missing | false\nlegal_complaint_filed | true",
  "question": "Proposed action: ask a human\nIs the proposed action correct for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if claim_amount is at least claim_amount_hard_limit.\n2. ask a human if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. wait if proof_of_purchase_missing is true or item_excluded_by_policy is true.\nOtherwise: proceed.\nNever counted: item_return_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q38a6b4de74",
  "kind": "yes/no",
  "text": "---\n# request record\nrequest_id: \"REQ-8744\"\nrequester: \"Nadia Imai\"\nrequester_not_barred_from_this_system: true\nlegal_preservation_order_on_the_account: true\nbusiness_justification_missing: false\nrequest_free_of_ethics_office_flags: true\naccess_days: 12\naccount_suspended: false\nrequest_grants_admin_rights: false\nrequest_text_written_in_capital_letters: true\naccess_days_approval_threshold: 60\nmfa_enrollment_complete: true\nrequested_role_forbidden_by_policy: false",
  "question": "Proposed action: 9605\nShould the proposed action be taken for this request?",
  "definitions": "Meanings:\n- 9605: forward the matter as the call rests with someone higher\n- 3: hold the request until the check is done\n- 645: leave the requester without the result they asked for\n- 11: press on with the work as originally set\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q15715c274f",
  "kind": "yes/no",
  "text": "{\"request_id\":\"REQ-8051\",\"requester\":\"Hugo Mensah\",\"legal_preservation_order_on_the_account\":false,\"request_grants_admin_rights\":false,\"access_days_approval_threshold\":60,\"request_text_written_in_capital_letters\":true,\"access_days\":60,\"requester_barred_from_this_system\":false,\"business_justification_missing\":true,\"request_free_of_ethics_office_flags\":true,\"account_suspended\":false,\"requested_role_forbidden_by_policy\":false,\"mfa_enrollment_complete\":true}",
  "question": "Proposed action: 2677\nShould the proposed action be taken for this request?",
  "definitions": "Meanings:\n- 698: keep moving on this one nothing is holding it up\n- 7: reject the petition as the action is unauthorized\n- 18: bring in the owner who can rule on this\n- 2677: hold the request so the requester waits for their check\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q694ad92da5",
  "kind": "choice",
  "text": "deploy_id | DEP-5417\nservice | reports\ndeploy_prohibited_during_the_audit_window | false\nservice_free_of_major_incidents | false\ncanary_results_incomplete | false\nfiles_changed | 20\ndeploy_title_written_in_normal_case | false\ndeploy_blocked_by_security_policy | false\ncontract_customer_asked_for_a_say_in_this_rollout | false\ncommit_messages_written_in_a_casual_tone | true\nrollout_approval_revoked | false\nbackout_plan_documented | true\ndeploy_has_a_long_description | false\nfiles_changed_soft_limit | 20\ncommit_messages_written_in_a_detailed_style | true",
  "question": "Meanings:\n- KRGT: keep moving so the asker gets the outcome\n- GNF: direct the request to the responsible decider\n- CL: be blocked outright so it never gets carried out\n- R: stall the request until the check comes back\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "KRGT",
   "GNF",
   "R"
  ]
 },
 {
  "qid": "qdea4efa45b",
  "kind": "yes/no",
  "text": "{\n  \"request\":{\n    \"request_id\":\"REQ-7782\",\n    \"requester\":\"Paolo Imai\"\n  },\n  \"figures\":{\n    \"access_days\":1,\n    \"access_days_approval_threshold\":60\n  },\n  \"checks\":{\n    \"requester_barred_from_this_system\":true,\n    \"request_grants_admin_rights\":false,\n    \"legal_preservation_order_on_the_account\":false,\n    \"requested_role_forbidden_by_policy\":false,\n    \"account_suspended\":false,\n    \"mfa_enrollment_incomplete\":false,\n    \"request_text_written_in_capital_letters\":false,\n    \"business_justification_missing\":false,\n    \"ethics_office_flagged_the_request\":false\n  }\n}",
  "question": "Proposed action: cancel\nDo the request and its facts together make the proposed action the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q5da7ab4a7d",
  "kind": "choice",
  "text": "{\n    \"request\": {\n        \"invoice_id\": \"INV-3246\",\n        \"vendor\": \"Brightwater Labs\"\n    },\n    \"figures\": {\n        \"amount_approval_threshold\": 25000.00,\n        \"amount\": 21076.25\n    },\n    \"checks\": {\n        \"payment_requested_during_business_hours\": true,\n        \"approver_declared_a_conflict_of_interest\": false,\n        \"duplicate_of_paid_invoice\": false,\n        \"vendor_tax_form_on_file\": true,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": false,\n        \"awaiting_purchase_order\": false,\n        \"invoice_pdf_uses_a_landscape_layout\": false,\n        \"vendor_free_of_sanctions\": false,\n        \"vendor_name_written_in_capital_letters\": false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. NRNK if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. ZXZ if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. LW if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\nOtherwise: P.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- LW: wait for the document before going further\n- ZXZ: decline the request as the action is prohibited\n- NRNK: bring in the authority who can settle it for the requester\n- P: advance the task as stated without any blockers\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "ZXZ",
   "NRNK",
   "LW"
  ]
 },
 {
  "qid": "qcec73aaea6",
  "kind": "choice",
  "text": "---\n# record\nrun_id: \"RUN-9474\"\nagent: \"indigo\"\nowner_sign_off_required_for_this_action: false\nlog_lines_written_in_a_compact_style: true\naction_permitted_by_security_policy: true\naction_free_of_ethics_concerns: true\nsteps_used_hard_limit: 60\ntool_output_shows_tampering: true\nsteps_used: 60\nlast_tool_output_unverified: false\ntask_description_complete: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 6 if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. 740 if task_description_complete is false or steps_used is above steps_used_hard_limit.\n3. 4154 if action_permitted_by_security_policy is false or owner_sign_off_required_for_this_action is true.\nOtherwise: 52.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_compact_style.\nMeanings:\n- 740: hold off until more information arrives\n- 4154: send it onward because someone else must decide\n- 6: withdraw from the step as it is forbidden\n- 52: have the plan kept moving as it was requested\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "740",
   "6",
   "52"
  ]
 },
 {
  "qid": "q7334810c5a",
  "kind": "choice",
  "text": "# request record\nrun_id                                  | RUN-7396\nagent                                   | fjord\nsteps_used                              | 3\ntool_output_shows_tampering             | false\ntask_description_incomplete             | false\nlog_lines_written_in_a_verbose_style    | false\naction_free_of_ethics_concerns          | true\nlast_tool_output_unverified             | false\nowner_sign_off_required_for_this_action | false\naction_permitted_by_security_policy     | true\nsteps_used_hard_limit                   | 60",
  "question": "Meanings:\n- proceed: run the task as it was asked, with nothing standing between it and completion\n- ask_a_human: hand this to the person who decides\n- wait: pause and collect more information first\n- cancel: bin this idea and keep it out of the flow\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the most suitable for the request?",
  "options": [
   "proceed",
   "ask_a_human",
   "wait"
  ]
 },
 {
  "qid": "q4bcd90c33e",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"invoice_id\": \"INV-6116\",\n        \"vendor\": \"Redwood Logistics\"\n    },\n    \"metrics\": {\n        \"amount_approval_threshold\": 2500.00,\n        \"amount\": 1562.42\n    },\n    \"signals\": {\n        \"approver_declared_a_conflict_of_interest\": false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": false,\n        \"awaiting_purchase_order\": true,\n        \"vendor_name_written_in_capital_letters\": true,\n        \"payment_requested_during_business_hours\": true,\n        \"vendor_on_sanctions_list\": true,\n        \"invoice_pdf_uses_a_landscape_layout\": false,\n        \"vendor_tax_form_missing\": false,\n        \"duplicate_of_paid_invoice\": false\n    }\n}",
  "question": "Proposed action: refuse\nWould the proposed action be the right answer to what this request calls for?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if approver_declared_a_conflict_of_interest is true.\n2. refuse if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- delay: defer further action pending verification of the document\n- refuse: kill this one off\n- ask a human: hand it up to the person who decides\n- approve: just crack on with it there is nothing in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe135697dab",
  "kind": "choice",
  "text": "---\n# record\nrecord:\n  run_id: RUN-2030\n  agent: delta\nnumbers:\n  steps_used_hard_limit: 8\n  steps_used: 3\nflags:\n  tool_output_shows_tampering: false\n  task_description_incomplete: false\n  action_free_of_ethics_concerns: true\n  action_forbidden_by_security_policy: false\n  log_lines_written_in_a_verbose_style: false\n  last_tool_output_verified: false\n  owner_sign_off_required_for_this_action: false",
  "question": "Meanings:\n- 32: cease the operation as it is prohibited\n- 2492: run with this one\n- 306: keep waiting for the missing details\n- 6: hand the matter to a decider so the requester gets a verdict\nThe record is complete: nothing else applies.\n\nWhich of the actions below does the record point to as the right call?",
  "options": [
   "2492",
   "6",
   "306"
  ]
 },
 {
  "qid": "q716220e683",
  "kind": "choice",
  "text": "# case\nticket_id: TCK-1823\ncustomer: Samir Adeyemi\ncustomer_message_is_short: true\nharmless_greeting_present_in_the_message: true\nproof_of_purchase_attached: true\nclaim_amount: 500.01\nclaim_form_filled_in_with_the_usual_font: true\nitem_return_received: true\nlegal_complaint_filed: false\nitem_excluded_by_policy: false\nclaim_involves_a_media_inquiry: false\nfree_of_safety_incident_reports: true\nclaim_amount_hard_limit: 500.00\nclaim_free_of_ombudsman_cases: true\ncustomer_message_written_in_a_formal_tone: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "deny",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "qefbbd9f02c",
  "kind": "choice",
  "text": "{\n    \"case\": {\n        \"invoice_id\": \"INV-4118\",\n        \"vendor\": \"Summit Group\"\n    },\n    \"values\": {\n        \"amount_approval_threshold\": 25000.00,\n        \"amount\": 23406.36\n    },\n    \"tests\": {\n        \"approver_declared_a_conflict_of_interest\": false,\n        \"invoice_pdf_uses_a_landscape_layout\": false,\n        \"vendor_tax_form_on_file\": true,\n        \"purchase_order_received\": true,\n        \"duplicate_of_paid_invoice\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"vendor_name_written_in_capital_letters\": true,\n        \"vendor_on_sanctions_list\": false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": false\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "ask_a_human",
   "approve",
   "delay"
  ]
 },
 {
  "qid": "qff72226c2f",
  "kind": "yes/no",
  "text": "# case\nticket_id = TCK-3487\ncustomer = Omar Ferreira\nproof_of_purchase_missing = true\nclaim_amount = 50.00\ncustomer_message_written_in_a_casual_tone = true\nclaim_amount_hard_limit = 50.00\nitem_return_received = true\nlegal_complaint_filed = false\nclaim_form_filled_in_with_the_usual_font = true\ncustomer_message_is_short = true\nfree_of_safety_incident_reports = true\nclaim_free_of_ombudsman_cases = true\nclaim_involves_a_media_inquiry = false\nharmless_greeting_present_in_the_message = true\nitem_excluded_by_policy = false",
  "question": "Proposed action: go ahead\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. put on hold if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\n3. send to a person if item_return_received is false or legal_complaint_filed is true or free_of_safety_incident_reports is false.\nOtherwise: go ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- send to a person: route this matter to the individual empowered to decide\n- go ahead: go ahead and the requester will be served\n- put on hold: defer the step until the verification is in\n- turn down: be stopped and never carried out\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qce74d8531e",
  "kind": "choice",
  "text": "{\"ticket_id\": \"TCK-6371\", \"customer\": \"Dana Mensah\", \"item_excluded_by_policy\": false, \"claim_amount_hard_limit\": 500.00, \"claim_form_filled_in_with_the_usual_font\": true, \"item_return_received\": true, \"free_of_safety_incident_reports\": true, \"harmless_greeting_present_in_the_message\": false, \"customer_message_written_in_a_casual_tone\": false, \"proof_of_purchase_missing\": true, \"claim_involves_a_media_inquiry\": false, \"customer_message_is_short\": true, \"claim_amount\": 80.19, \"claim_free_of_ombudsman_cases\": true, \"free_of_legal_complaints\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 6 if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. 627 if item_excluded_by_policy is true or free_of_legal_complaints is false or claim_amount is above claim_amount_hard_limit.\n3. 66 if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: 7111.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- 7111: complete the job as it was assigned\n- 6: stay put until the check is finished\n- 627: make sure the requester never gets what they wanted\n- 66: get sent upward to the one who decides\nThe record is complete: nothing else applies.\n\nAuditing the request, which of the actions below is the defensible choice?",
  "options": [
   "627",
   "7111",
   "66"
  ]
 },
 {
  "qid": "qedb15ae7c9",
  "kind": "choice",
  "text": "---\ncase:\n    invoice_id: \"INV-4911\"\n    vendor: \"Copperfield Foods\"\nvalues:\n    amount_approval_threshold: 5000.00\n    amount: 1226.92\ntests:\n    payment_requested_during_business_hours: true\n    invoice_pdf_uses_a_landscape_layout: false\n    duplicate_of_paid_invoice: false\n    awaiting_purchase_order: false\n    approver_free_of_conflicts_of_interest: true\n    vendor_tax_form_missing: true\n    vendor_free_of_sanctions: true\n    vendor_name_written_in_capital_letters: false\n    vendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. cancel if vendor_free_of_sanctions is false.\n3. ask_a_human if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: proceed.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_free_of_conflicts_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "ask_a_human",
   "proceed",
   "wait"
  ]
 },
 {
  "qid": "qfa64182be4",
  "kind": "choice",
  "text": "# record\ninvoice_id | INV-3352\nvendor | Silverline Systems\namount_approval_threshold | 5000.00\nvendor_tax_form_on_file | true\nvendor_name_written_in_capital_letters | false\npayment_requested_during_business_hours | true\ninvoice_pdf_uses_a_landscape_layout | false\nduplicate_of_paid_invoice | true\npurchase_order_received | true\nvendor_free_of_sanctions | false\namount | 4755.66\nvendor_filed_a_legal_claim_over_this_invoice | false\napprover_declared_a_conflict_of_interest | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true or amount is at least amount_approval_threshold.\n2. put on hold if purchase_order_received is false or vendor_tax_form_on_file is false.\n3. turn down if duplicate_of_paid_invoice is true.\nOtherwise: go ahead.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- put on hold: pause this until the requester supplies the missing document\n- send to a person: forward the matter as the call rests with someone higher\n- turn down: stop the work since it cannot move forward\n- go ahead: proceed as asked since everything is cleared\nThe record is complete: nothing else applies.\n\nFrom the requester's side, which of the actions listed below is the right call for this request?",
  "options": [
   "go ahead",
   "send to a person",
   "put on hold"
  ]
 },
 {
  "qid": "q3b3752e869",
  "kind": "choice",
  "text": "{\"ticket_id\":\"TCK-8632\",\"customer\":\"Nadia Tanaka\",\"customer_message_written_in_a_casual_tone\":true,\"proof_of_purchase_missing\":false,\"item_return_not_yet_received\":false,\"harmless_greeting_present_in_the_message\":true,\"claim_free_of_ombudsman_cases\":true,\"legal_complaint_filed\":false,\"claim_form_filled_in_with_the_usual_font\":true,\"free_of_safety_incident_reports\":false,\"item_excluded_by_policy\":false,\"claim_amount\":194.81,\"customer_message_is_short\":true,\"claim_amount_hard_limit\":200.00,\"claim_involves_a_media_inquiry\":false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if item_return_not_yet_received is true or claim_free_of_ombudsman_cases is false.\n2. cancel if item_excluded_by_policy is true or legal_complaint_filed is true or claim_amount is above claim_amount_hard_limit.\n3. ask_a_human if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: proceed.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nTaking the facts of the request into account, which action listed should be picked?",
  "options": [
   "wait",
   "cancel",
   "proceed"
  ]
 },
 {
  "qid": "q86b8119cff",
  "kind": "yes/no",
  "text": "invoice_id | INV-7422\nvendor | Riverbend Traders\ninvoice_pdf_uses_a_landscape_layout | false\nawaiting_purchase_order | false\npayment_requested_during_business_hours | true\nduplicate_of_paid_invoice | true\namount | 2138.37\nvendor_tax_form_on_file | true\napprover_declared_a_conflict_of_interest | false\namount_approval_threshold | 5000.00\nvendor_on_sanctions_list | true\nvendor_name_written_in_capital_letters | false\nvendor_filed_a_legal_claim_over_this_invoice | false",
  "question": "Proposed action: cancel\nSet beside the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if vendor_on_sanctions_list is true or approver_declared_a_conflict_of_interest is true.\n2. ask a human if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. wait if awaiting_purchase_order is true or amount is at least amount_approval_threshold.\nOtherwise: proceed.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3d3e7beba6",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n  run_id: RUN-9590\n  agent: atlas\nvalues:\n  steps_used: 7\n  steps_used_hard_limit: 40\ntests:\n  action_forbidden_by_security_policy: false\n  last_tool_output_verified: true\n  log_lines_written_in_a_compact_style: true\n  task_description_complete: true\n  action_free_of_ethics_concerns: true\n  owner_sign_off_required_for_this_action: false\n  tool_output_shows_tampering: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "turn_down"
  ]
 },
 {
  "qid": "q4d3f165344",
  "kind": "choice",
  "text": "---\ninvoice_id: INV-6459\nvendor: Oakmont Labs\npurchase_order_received: true\npayment_requested_during_business_hours: false\namount: 18051.09\nvendor_tax_form_on_file: true\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: false\napprover_declared_a_conflict_of_interest: false\ninvoice_pdf_uses_a_portrait_layout: false\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_name_written_in_capital_letters: false\namount_approval_threshold: 25000.00",
  "question": "The record is complete: nothing else applies.\n\nMind telling me which of the actions below is the best call for this request?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "send_to_a_person"
  ]
 },
 {
  "qid": "q64b8181a3d",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n    run_id: RUN-6764\n    agent: lumen\nvalues:\n    steps_used: 5\n    steps_used_hard_limit: 8\ntests:\n    task_description_incomplete: false\n    last_tool_output_verified: false\n    action_free_of_ethics_concerns: true\n    action_permitted_by_security_policy: true\n    tool_output_shows_tampering: false\n    owner_sign_off_required_for_this_action: false\n    log_lines_written_in_a_compact_style: true",
  "question": "Meanings:\n- 7690: go ahead with the requested action\n- 820: hand this to the person who decides\n- 32: shut this down fast\n- 7: suspend progress until verification is received\nThe record is complete: nothing else applies.\n\nGiven what the requester needs, which of the actions below should be taken?",
  "options": [
   "7",
   "32",
   "7690"
  ]
 },
 {
  "qid": "q869fb64196",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n* leave id: LVE-1396\n* employee: Anders Rossi\n* team coverage not arranged: no\n* union grievance raised over this leave: no\n* leave request written in a formal tone: no\n* notice period not met: no\n* leave balance available: no\n* lawyer letter received about this leave: no\n* leave days soft limit: 3\n* medical certificate contested: no\n* leave days: 1\n* requests team free of harassment complaints: yes\n* request falls in blackout period: no",
  "question": "Meanings:\n- ask a human: refer the matter to the decision holder\n- proceed: proceed as asked since everything is cleared\n- wait: defer further action pending verification of the document\n- cancel: be dropped here and not acted upon at all\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "wait",
   "cancel",
   "proceed"
  ]
 },
 {
  "qid": "qfec27518c9",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- deploy id: DEP-2712\n- service: inventory\n- deploy title written in normal case: yes\n- service free of major incidents: yes\n- commit messages written in a terse style: no\n- deploy has a long description: no\n- deploy blocked by security policy: no\n- files changed soft limit: 10\n- backout plan missing: yes\n- files changed: 1\n- commit messages written in a casual tone: yes\n- canary results incomplete: no\n- rollout approval revoked: no\n- deploy prohibited during the audit window: no\n- contract customer asked for a say in this rollout: yes",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pause if backout_plan_missing is true or files_changed is above files_changed_soft_limit.\n2. stop if deploy_blocked_by_security_policy is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true.\n3. human_review if service_free_of_major_incidents is false or contract_customer_asked_for_a_say_in_this_rollout is true.\nOtherwise: continue.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- pause: be kept on hold until more information is supplied\n- human_review: pass this along to the decision maker\n- continue: continue the work as originally asked, there is nothing in the way\n- stop: halt the request at this point\nThe record is complete: nothing else applies.\n\nWhich action listed below fits this request best?",
  "options": [
   "pause",
   "continue",
   "stop"
  ]
 },
 {
  "qid": "qa1000f79d8",
  "kind": "yes/no",
  "text": "# extract\nticket_id: TCK-1973\ncustomer: Mira Moreau\nclaim_involves_a_media_inquiry: false\nclaim_amount: 258.47\nitem_excluded_by_policy: false\ncustomer_message_written_in_a_casual_tone: true\nproof_of_purchase_missing: false\nclaim_amount_hard_limit: 500.00\nlegal_complaint_filed: false\nclaim_form_filled_in_with_the_usual_font: true\nitem_return_not_yet_received: true\nfree_of_safety_incident_reports: true\ncustomer_message_is_short: true\nharmless_greeting_present_in_the_message: true\nclaim_free_of_ombudsman_cases: true",
  "question": "Proposed action: put on hold\nReviewing this as an auditor, do the record's facts rule out the proposed action for the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if free_of_safety_incident_reports is false.\n2. turn down if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. put on hold if item_return_not_yet_received is true.\nOtherwise: go ahead.\nNever counted: proof_of_purchase_missing, item_excluded_by_policy, legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5a336b7734",
  "kind": "yes/no",
  "text": "# extract\nrun_id = RUN-9663\nagent = delta\nlast_tool_output_verified = false\nsteps_used_hard_limit = 16\nlog_lines_written_in_a_compact_style = true\nsteps_used = 4\naction_forbidden_by_security_policy = false\ntool_output_shows_tampering = false\nowner_sign_off_required_for_this_action = false\naction_free_of_ethics_concerns = true\ntask_description_incomplete = false",
  "question": "Proposed action: wait\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- ask_a_human: route this matter to the individual empowered to decide\n- cancel: withdraw from the step as it is forbidden\n- proceed: execute the requested action as nothing prevents it\n- wait: hold the request until the check is done\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q51546e0b39",
  "kind": "choice",
  "text": "# record\nrequest_id: REQ-6656\nrequester: Marta Mensah\nrequested_role_permitted_by_policy: true\nrequest_grants_admin_rights: false\nmfa_enrollment_incomplete: false\nrequest_free_of_ethics_office_flags: true\nrequest_text_written_in_capital_letters: false\nbusiness_justification_missing: false\naccess_days: 27\naccount_suspended: false\nlegal_preservation_order_on_the_account: false\nrequester_not_barred_from_this_system: false\naccess_days_approval_threshold: 60",
  "question": "The record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "quarantine",
   "allow",
   "block_access"
  ]
 },
 {
  "qid": "q099cb21b1f",
  "kind": "choice",
  "text": "# extract\nrequest_id | REQ-4995\nrequester | Hugo Imai\naccess_days_approval_threshold | 45\nbusiness_justification_missing | false\nrequester_barred_from_this_system | false\naccess_days | 46\naccount_suspended | false\nmfa_enrollment_incomplete | false\nrequested_role_forbidden_by_policy | false\nrequest_free_of_ethics_office_flags | true\nrequest_text_written_in_capital_letters | true\nrequest_grants_admin_rights | false\nlegal_preservation_order_on_the_account | false",
  "question": "Meanings:\n- cancel: kill this one off, it is off the table for good\n- proceed: keep moving on this one nothing is holding it up\n- ask a human: forward it to the decision maker\n- wait: hold this until a check comes back\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "proceed",
   "wait",
   "ask a human"
  ]
 },
 {
  "qid": "q5b7a13b335",
  "kind": "choice",
  "text": "# extract\nrequest_id: REQ-9113\nrequester: Lena Novak\naccess_days: 2\naccess_days_approval_threshold: 60\nrequester_barred_from_this_system: true\nrequest_grants_admin_rights: false\naccount_suspended: false\nrequest_text_written_in_capital_letters: false\nrequest_free_of_ethics_office_flags: true\nmfa_enrollment_incomplete: false\nbusiness_justification_provided: true\nrequested_role_forbidden_by_policy: false\nlegal_preservation_order_on_the_account: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if business_justification_provided is false or requested_role_forbidden_by_policy is true.\n2. ask manager if mfa_enrollment_incomplete is true or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. deny if account_suspended is true or requester_barred_from_this_system is true.\nOtherwise: approve.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nGiven what the requester needs, which of the actions below should be taken?",
  "options": [
   "approve",
   "deny",
   "ask manager"
  ]
 },
 {
  "qid": "qeb37976c5a",
  "kind": "yes/no",
  "text": "# record\nrequest_id=REQ-9634\nrequester=Dana Lindqvist\nbusiness_justification_missing=true\nrequest_free_of_ethics_office_flags=true\nlegal_preservation_order_on_the_account=false\naccount_suspended=false\nmfa_enrollment_incomplete=false\naccess_days_approval_threshold=90\nrequest_grants_admin_rights=false\nrequester_not_barred_from_this_system=true\naccess_days=90\nrequest_text_written_in_capital_letters=true\nrequested_role_permitted_by_policy=true",
  "question": "Proposed action: allow\nIs it not true that the proposed action we are discussing is not mistaken for this request?",
  "definitions": "Meanings:\n- page_oncall: pass this along to the decision maker\n- allow: proceed as asked since everything is cleared\n- block_access: cease the operation as it is prohibited\n- quarantine: keep it on hold for the missing document\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcd9089e3c6",
  "kind": "choice",
  "text": "{\n  \"request\":{\n    \"ticket_id\":\"TCK-1668\",\n    \"customer\":\"Jonas Petrov\"\n  },\n  \"figures\":{\n    \"claim_amount_hard_limit\":1000.00,\n    \"claim_amount\":117.93\n  },\n  \"checks\":{\n    \"claim_involves_a_media_inquiry\":false,\n    \"legal_complaint_filed\":false,\n    \"claim_free_of_ombudsman_cases\":true,\n    \"proof_of_purchase_missing\":false,\n    \"customer_message_is_short\":true,\n    \"item_excluded_by_policy\":false,\n    \"customer_message_written_in_a_casual_tone\":false,\n    \"harmless_greeting_present_in_the_message\":true,\n    \"claim_form_filled_in_with_the_usual_font\":true,\n    \"item_return_not_yet_received\":false,\n    \"free_of_safety_incident_reports\":true\n  }\n}",
  "question": "Meanings:\n- 7950: shelve the matter until more details come in\n- 78: shut off this process completely\n- 189: forward the case to the designated decision maker\n- 9: go on and finish it the path is clear\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "189",
   "7950",
   "9"
  ]
 },
 {
  "qid": "q59a1302f4a",
  "kind": "choice",
  "text": "{\"leave_id\":\"LVE-2584\",\"employee\":\"Zoe Hadjiev\",\"medical_certificate_contested\":false,\"union_grievance_raised_over_this_leave\":false,\"leave_days_soft_limit\":14,\"lawyer_letter_received_about_this_leave\":false,\"team_coverage_not_arranged\":false,\"leave_balance_available\":false,\"requests_team_free_of_harassment_complaints\":true,\"leave_request_written_in_a_formal_tone\":false,\"leave_days\":14,\"notice_period_not_met\":false,\"request_falls_in_blackout_period\":false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if team_coverage_not_arranged is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. wait if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. cancel if leave_balance_available is false.\nOtherwise: proceed.\nNever counted: notice_period_not_met, union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed should the team commit to for this request, as the manager?",
  "options": [
   "ask a human",
   "cancel",
   "proceed"
  ]
 },
 {
  "qid": "q776cf493cf",
  "kind": "choice",
  "text": "# case\nrequest_id = REQ-2624\nrequester = Tomas Brandt\naccess_days_approval_threshold = 60\nrequest_grants_admin_rights = false\nlegal_preservation_order_on_the_account = false\nrequest_text_written_in_capital_letters = false\nrequested_role_permitted_by_policy = true\nethics_office_flagged_the_request = false\naccess_days = 13\naccount_suspended = false\nmfa_enrollment_incomplete = false\nrequester_not_barred_from_this_system = true\nbusiness_justification_missing = false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 55 if mfa_enrollment_incomplete is true or requester_not_barred_from_this_system is false or ethics_office_flagged_the_request is true.\n2. 5455 if account_suspended is true or requested_role_permitted_by_policy is false.\n3. 837 if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: 1.\nNever counted: business_justification_missing, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- 5455: halt the request at this point\n- 55: hold the request so the requester waits for their check\n- 1: commence the action as specified without impediment\n- 837: route it elsewhere because a decider must weigh in\nThe record is complete: nothing else applies.\n\nAs the manager, which of the actions listed is the right call for this request?",
  "options": [
   "55",
   "837",
   "1"
  ]
 },
 {
  "qid": "qe8788dce8d",
  "kind": "choice",
  "text": "leave_id | LVE-5322\nemployee | Nadia Brandt\nleave_days | 13\nleave_balance_exhausted | false\nrequest_falls_in_blackout_period | true\nleave_days_soft_limit | 14\nno_union_grievance_raised_over_this_leave | true\nnotice_period_not_met | false\nteam_coverage_not_arranged | false\nleave_request_written_in_a_formal_tone | false\nrequests_team_free_of_harassment_complaints | true\nlawyer_letter_received_about_this_leave | false\nmedical_certificate_contested | false",
  "question": "The record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "approve_leave",
   "refuse_leave",
   "postpone"
  ]
 },
 {
  "qid": "qd972d585a1",
  "kind": "yes/no",
  "text": "# request record\nrun_id=RUN-1329\nagent=garnet\naction_forbidden_by_security_policy=false\nlast_tool_output_unverified=false\nlog_lines_written_in_a_verbose_style=true\naction_free_of_ethics_concerns=true\ntask_description_complete=true\ntool_output_shows_tampering=false\nsteps_used_hard_limit=30\nsteps_used=15\nowner_sign_off_required_for_this_action=true",
  "question": "Proposed action: pause\nIs the proposed action not consistent with the handling procedure for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. human_review if action_free_of_ethics_concerns is false or steps_used is above steps_used_hard_limit.\n2. pause if owner_sign_off_required_for_this_action is true.\n3. stop if task_description_complete is false or tool_output_shows_tampering is true or action_forbidden_by_security_policy is true.\nOtherwise: continue.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb9ade9ca92",
  "kind": "choice",
  "text": "# record\nticket_id | TCK-7015\ncustomer | Kofi Okonkwo\nclaim_amount | 100.01\nfree_of_legal_complaints | true\nclaim_free_of_ombudsman_cases | true\nfree_of_safety_incident_reports | true\nproof_of_purchase_attached | true\nitem_return_not_yet_received | false\nclaim_form_filled_in_with_the_usual_font | true\nclaim_amount_hard_limit | 100.00\nitem_excluded_by_policy | false\nharmless_greeting_present_in_the_message | true\nclaim_involves_a_media_inquiry | false\ncustomer_message_is_short | true\ncustomer_message_written_in_a_formal_tone | false",
  "question": "Meanings:\n- XCL: wait so the requester can supply more information first\n- RZBJ: drop it right away\n- Z: let this be advanced exactly as originally specified\n- XQ: submit the question to the authorised decision maker\nThe record is complete: nothing else applies.\n\nLooking at what was asked, which of the actions below best fits the request?",
  "options": [
   "Z",
   "RZBJ",
   "XCL"
  ]
 },
 {
  "qid": "qbd697f0052",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-8349\n- vendor: Stonebridge Systems\n- approver free of conflicts of interest: yes\n- amount approval threshold: 2500.00\n- duplicate of paid invoice: no\n- vendor filed a legal claim over this invoice: no\n- vendor tax form missing: no\n- invoice pdf uses a landscape layout: no\n- vendor on sanctions list: no\n- payment requested during business hours: yes\n- vendor name written in capital letters: no\n- amount: 336.01\n- purchase order received: no",
  "question": "Proposed action: delay\nLooking at what the record says, is the proposed action a good fit for the request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q13db48186d",
  "kind": "yes/no",
  "text": "# request record\nticket_id                                 | TCK-8810\ncustomer                                  | Ingrid Anand\nclaim_free_of_ombudsman_cases             | true\nclaim_involves_a_media_inquiry            | false\nitem_return_received                      | true\nclaim_form_filled_in_with_the_usual_font  | true\nfree_of_safety_incident_reports           | true\nclaim_amount                              | 50.00\nitem_excluded_by_policy                   | false\nclaim_amount_hard_limit                   | 50.00\ncustomer_message_written_in_a_formal_tone | false\ncustomer_message_is_short                 | true\nharmless_greeting_present_in_the_message  | true\nfree_of_legal_complaints                  | true\nproof_of_purchase_attached                | true",
  "question": "Proposed action: defer\nIs it not the case that the facts behind this case back the proposed action and that it is not mistaken?",
  "definitions": "Meanings:\n- defer: pause this until the requester supplies the missing document\n- approve: let this be advanced exactly as originally specified\n- deny: be turned away and treated as off limits\n- ask manager: delegate the call to whoever holds authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qef50a0233d",
  "kind": "choice",
  "text": "{\n    \"record\": {\n        \"leave_id\": \"LVE-1310\",\n        \"employee\": \"نضال سمير الخوري\",\n        \"note\": \"الموظف قدم جميع المستندات المطلوبة وهي صحيحة.\"\n    },\n    \"numbers\": {\n        \"leave_days_soft_limit\": 5,\n        \"leave_days\": 4\n    },\n    \"flags\": {\n        \"leave_balance_available\": true,\n        \"request_falls_in_blackout_period\": false,\n        \"medical_certificate_contested\": false,\n        \"notice_period_met\": true,\n        \"no_union_grievance_raised_over_this_leave\": true,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"team_coverage_not_arranged\": false,\n        \"leave_request_written_in_a_formal_tone\": true,\n        \"lawyer_letter_received_about_this_leave\": false\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nGiven the details in the record, which action listed would be the correct decision?",
  "options": [
   "refuse",
   "approve",
   "delay"
  ]
 },
 {
  "qid": "q58c7af15f6",
  "kind": "yes/no",
  "text": "{\"leave_id\": \"LVE-9699\", \"employee\": \"Samir Haddad\", \"notice_period_met\": true, \"requests_team_free_of_harassment_complaints\": true, \"request_falls_in_blackout_period\": true, \"leave_balance_available\": true, \"leave_days_soft_limit\": 21, \"medical_certificate_contested\": false, \"team_coverage_arranged\": true, \"lawyer_letter_received_about_this_leave\": false, \"leave_days\": 14, \"leave_request_written_in_a_formal_tone\": false, \"union_grievance_raised_over_this_leave\": false}",
  "question": "Proposed action: cancel\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q13563f9029",
  "kind": "yes/no",
  "text": "# extract\ndeploy_id                                         | DEP-6606\nservice                                           | auth_proxy\nbackout_plan_documented                           | true\ndeploy_prohibited_during_the_audit_window         | false\nfiles_changed_soft_limit                          | 20\ndeploy_blocked_by_security_policy                 | false\ncanary_results_incomplete                         | false\nservice_free_of_major_incidents                   | false\ncommit_messages_written_in_a_casual_tone          | true\ndeploy_has_a_long_description                     | false\ndeploy_title_written_in_normal_case               | true\nrollout_approval_revoked                          | false\nfiles_changed                                     | 21\ncontract_customer_asked_for_a_say_in_this_rollout | false\ncommit_messages_written_in_a_detailed_style       | true",
  "question": "Proposed action: turn down\nDoes the proposed action make sense for the request shown in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_documented is false or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- go ahead: keep going exactly as requested because every obstacle has cleared\n- put on hold: hold off until more information arrives\n- send to a person: be passed along to whoever makes the call\n- turn down: stop the request so the requester gets nothing from it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7a5b0a6864",
  "kind": "choice",
  "text": "# extract\nrun_id: RUN-9319\nagent: lumen\nsteps_used_hard_limit: 20\nowner_sign_off_required_for_this_action: true\naction_forbidden_by_security_policy: false\ntool_output_shows_tampering: false\naction_free_of_ethics_concerns: false\ntask_description_incomplete: false\nlog_lines_written_in_a_compact_style: true\nlast_tool_output_unverified: true\nsteps_used: 13",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is at least steps_used_hard_limit.\n2. put_on_hold if task_description_incomplete is true or owner_sign_off_required_for_this_action is true.\n3. send_to_a_person if action_free_of_ethics_concerns is false.\nOtherwise: go_ahead.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies.\n\nTaking the actions listed into account, what is the right call for the request?",
  "options": [
   "turn_down",
   "go_ahead",
   "put_on_hold"
  ]
 },
 {
  "qid": "q1ea626b436",
  "kind": "choice",
  "text": "---\nrequest:\n  ticket_id: TCK-3365\n  customer: دينا وائل الأنصاري\n  note: الحالة بسيطة ومكتملة ولا تحتاج إلى تدخل إضافي.\nfigures:\n  claim_amount: 35.26\n  claim_amount_hard_limit: 50.00\nchecks:\n  legal_complaint_filed: true\n  claim_involves_a_media_inquiry: false\n  free_of_safety_incident_reports: false\n  customer_message_is_short: true\n  claim_form_filled_in_with_the_usual_font: true\n  item_return_received: true\n  harmless_greeting_present_in_the_message: true\n  proof_of_purchase_attached: true\n  item_excluded_by_policy: false\n  customer_message_written_in_a_formal_tone: false\n  claim_free_of_ombudsman_cases: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. wait if proof_of_purchase_attached is false or claim_amount is at least claim_amount_hard_limit.\n3. cancel if item_excluded_by_policy is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\nOtherwise: proceed.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "wait",
   "cancel",
   "proceed"
  ]
 },
 {
  "qid": "q6300ed557a",
  "kind": "choice",
  "text": "{\n  \"request\":{\n    \"run_id\":\"RUN-3737\",\n    \"agent\":\"indigo\"\n  },\n  \"figures\":{\n    \"steps_used\":17,\n    \"steps_used_hard_limit\":60\n  },\n  \"checks\":{\n    \"action_free_of_ethics_concerns\":false,\n    \"action_permitted_by_security_policy\":true,\n    \"task_description_complete\":true,\n    \"tool_output_shows_tampering\":false,\n    \"owner_sign_off_required_for_this_action\":false,\n    \"log_lines_written_in_a_compact_style\":true,\n    \"last_tool_output_unverified\":false\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 737 if owner_sign_off_required_for_this_action is true.\n2. 5877 if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is above steps_used_hard_limit.\n3. 1 if last_tool_output_unverified is true.\nOtherwise: 27.\nNever counted: task_description_complete, action_free_of_ethics_concerns, log_lines_written_in_a_compact_style.\nMeanings:\n- 1: be kept on hold until more information is supplied\n- 27: have the plan kept moving as it was requested\n- 5877: shut this down before it spreads into the workflow\n- 737: transfer the case to the responsible decision maker for determination\nThe record is complete: nothing else applies.\n\nAuditing the request, which of the actions below is the defensible choice?",
  "options": [
   "5877",
   "1",
   "27"
  ]
 },
 {
  "qid": "qb28c0571e7",
  "kind": "choice",
  "text": "# case\nleave_id: LVE-6460\nemployee: لمى سهيل الإدريسي\nnote: الموافقة على الإجازة ما زالت ناقصة بسبب بيانات غير مؤكدة.\nleave_days: 2\nleave_request_written_in_a_formal_tone: false\nleave_balance_available: true\nunion_grievance_raised_over_this_leave: false\nteam_coverage_not_arranged: false\nnotice_period_met: true\nrequests_team_free_of_harassment_complaints: true\nmedical_certificate_contested: false\nlawyer_letter_received_about_this_leave: false\nrequest_falls_in_blackout_period: false\nleave_days_soft_limit: 14",
  "question": "Meanings:\n- send_to_a_person: pass this along to the decision maker\n- go_ahead: execute the request exactly as written\n- put_on_hold: wait for the document to come through\n- turn_down: reject this item since it violates the policy\nThe record is complete: nothing else applies.\n\nPicking from the actions listed, what best serves this request?",
  "options": [
   "go_ahead",
   "turn_down",
   "put_on_hold"
  ]
 },
 {
  "qid": "q3b6aa04cdf",
  "kind": "choice",
  "text": "run_id | RUN-9671\nagent | fjord\ntool_output_shows_tampering | true\nlast_tool_output_unverified | true\nsteps_used_hard_limit | 16\nsteps_used | 11\naction_free_of_ethics_concerns | true\nowner_sign_off_required_for_this_action | false\ntask_description_incomplete | false\nlog_lines_written_in_a_verbose_style | true\naction_permitted_by_security_policy | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. stop if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is at least steps_used_hard_limit.\n2. pause if task_description_incomplete is true or owner_sign_off_required_for_this_action is true.\n3. human review if action_free_of_ethics_concerns is false.\nOtherwise: continue.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "continue",
   "human review",
   "stop"
  ]
 },
 {
  "qid": "q9ddc599d7a",
  "kind": "choice",
  "text": "---\nleave_id: \"LVE-7952\"\nemployee: \"سوسن أمجد الراشد\"\nnote: \"طلب الإجازة مقدم في الموعد المحدد بالسياسة.\"\nrequest_falls_in_blackout_period: false\nlawyer_letter_received_about_this_leave: false\nno_union_grievance_raised_over_this_leave: true\nrequests_team_free_of_harassment_complaints: false\nnotice_period_met: true\nteam_coverage_arranged: true\nleave_days: 2\nleave_days_soft_limit: 10\nleave_request_written_in_a_formal_tone: false\nmedical_certificate_contested: false\nleave_balance_available: true",
  "question": "The record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "postpone",
   "approve_leave",
   "refer_to_hr"
  ]
 },
 {
  "qid": "q5846e61d07",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-8824\", \"vendor\": \"Riverbend Foods\", \"vendor_tax_form_missing\": true, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"amount_approval_threshold\": 25000.00, \"approver_free_of_conflicts_of_interest\": true, \"payment_requested_during_business_hours\": true, \"vendor_free_of_sanctions\": true, \"awaiting_purchase_order\": false, \"duplicate_of_paid_invoice\": false, \"vendor_name_written_in_capital_letters\": false, \"invoice_pdf_uses_a_landscape_layout\": false, \"amount\": 23943.73}",
  "question": "Proposed action: defer\nDoes the proposed action not fit what this request needs?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q498bab64d1",
  "kind": "yes/no",
  "text": "{\n    \"deploy_id\": \"DEP-1900\",\n    \"service\": \"auth_proxy\",\n    \"backout_plan_missing\": false,\n    \"deploy_blocked_by_security_policy\": false,\n    \"service_free_of_major_incidents\": true,\n    \"contract_customer_asked_for_a_say_in_this_rollout\": false,\n    \"files_changed_soft_limit\": 20,\n    \"deploy_title_written_in_normal_case\": true,\n    \"canary_results_complete\": true,\n    \"deploy_prohibited_during_the_audit_window\": false,\n    \"commit_messages_written_in_a_detailed_style\": true,\n    \"deploy_has_a_long_description\": true,\n    \"rollout_approval_revoked\": false,\n    \"commit_messages_written_in_a_casual_tone\": true,\n    \"files_changed\": 5\n}",
  "question": "Proposed action: 5256\nIs it not true that the proposed action is not out of line with the ask?",
  "definitions": "Meanings:\n- 51: hold the request so the requester waits for their check\n- 1: shut this down fast\n- 5256: commence the action as specified without impediment\n- 692: give it to the person in charge of the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q63c63c7aa3",
  "kind": "yes/no",
  "text": "ticket_id | TCK-8915\ncustomer | Leila Mensah\nharmless_greeting_present_in_the_message | false\nfree_of_safety_incident_reports | true\nclaim_amount_hard_limit | 100.00\nitem_excluded_by_policy | false\nfree_of_legal_complaints | true\ncustomer_message_is_short | true\nclaim_free_of_ombudsman_cases | true\nclaim_form_filled_in_with_the_usual_font | true\nclaim_involves_a_media_inquiry | false\ncustomer_message_written_in_a_casual_tone | false\nproof_of_purchase_attached | true\nclaim_amount | 89.73\nitem_return_received | true",
  "question": "Proposed action: approve\nDoes the record itself rule out the proposed action?",
  "definitions": "Meanings:\n- delay: hold off until the check has been completed by the team\n- refuse: terminate the process as continuation is prohibited\n- ask a human: send it onward because someone else must decide\n- approve: proceed as asked since everything is cleared\nThe record is complete: nothing else applies."
 }
]
