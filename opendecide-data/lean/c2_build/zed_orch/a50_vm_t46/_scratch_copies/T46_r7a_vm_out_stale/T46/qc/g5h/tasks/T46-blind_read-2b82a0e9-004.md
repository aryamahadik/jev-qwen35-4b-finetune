# G5-H blind read T46-blind_read-2b82a0e9-004 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r7a/T46/qc/g5h/answers/T46-blind_read-2b82a0e9-004.json

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
  "qid": "q9f55b1eae0",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-4455\",\"vendor\":\"Brightwater Systems\",\"vendor_name_written_in_capital_letters\":false,\"vendor_free_of_sanctions\":true,\"invoice_pdf_uses_a_portrait_layout\":true,\"purchase_order_received\":true,\"approver_free_of_conflicts_of_interest\":true,\"duplicate_of_paid_invoice\":false,\"amount_approval_threshold\":5000.00,\"vendor_tax_form_missing\":false,\"payment_requested_during_business_hours\":true,\"vendor_filed_a_legal_claim_over_this_invoice\":false,\"amount\":4196.47}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. cancel order if duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_free_of_sanctions is false or approver_free_of_conflicts_of_interest is false or amount is at least amount_approval_threshold.\nOtherwise: release.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nGiven the request and the facts stated, which of the actions listed is the right call?",
  "options": [
   "cancel order",
   "delay",
   "release"
  ]
 },
 {
  "qid": "q567a325268",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n* invoice id: INV-8384\n* vendor: Bluepeak Group\n* duplicate of paid invoice: no\n* payment requested during business hours: yes\n* amount: 7718.66\n* amount approval threshold: 25000.00\n* vendor tax form on file: yes\n* vendor filed a legal claim over this invoice: no\n* approver free of conflicts of interest: yes\n* vendor name written in capital letters: no\n* vendor on sanctions list: no\n* invoice pdf uses a portrait layout: yes\n* purchase order received: yes",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if purchase_order_received is false.\n2. escalate if vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. reject if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or approver_free_of_conflicts_of_interest is false or amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nThe request describes a situation; which of the actions underneath handles it correctly?",
  "options": [
   "reject",
   "hold",
   "pay"
  ]
 },
 {
  "qid": "qe5d535b599",
  "kind": "yes/no",
  "text": "{\n  \"run_id\": \"RUN-6185\",\n  \"agent\": \"jasper\",\n  \"action_permitted_by_security_policy\": true,\n  \"owner_sign_off_required_for_this_action\": true,\n  \"steps_used_hard_limit\": 40,\n  \"task_description_complete\": true,\n  \"steps_used\": 33,\n  \"last_tool_output_verified\": true,\n  \"log_lines_written_in_a_compact_style\": true,\n  \"tool_output_shows_tampering\": false,\n  \"action_free_of_ethics_concerns\": true\n}",
  "question": "Proposed action: go_ahead\nDo the record facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if last_tool_output_verified is false or action_free_of_ethics_concerns is false.\n2. turn_down if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is at least steps_used_hard_limit.\n3. send_to_a_person if task_description_complete is false or owner_sign_off_required_for_this_action is true.\nOtherwise: go_ahead.\nNever counted: log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfa8628b39f",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n    ticket_id: TCK-7570\n    customer: Mira Brandt\nvalues:\n    claim_amount: 45.51\n    claim_amount_hard_limit: 50.00\ntests:\n    claim_involves_a_media_inquiry: false\n    claim_form_filled_in_with_the_usual_font: false\n    item_excluded_by_policy: false\n    harmless_greeting_present_in_the_message: false\n    proof_of_purchase_missing: false\n    free_of_legal_complaints: true\n    item_return_received: true\n    claim_free_of_ombudsman_cases: true\n    free_of_safety_incident_reports: true",
  "question": "Proposed action: go ahead\nHas the request, read alongside the facts, ruled out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qac45ecf994",
  "kind": "yes/no",
  "text": "# record\nticket_id=TCK-4514\ncustomer=Nadia Haddad\nfree_of_safety_incident_reports=true\nitem_return_not_yet_received=false\nclaim_amount=425.61\nitem_excluded_by_policy=false\nclaim_involves_a_media_inquiry=false\nproof_of_purchase_attached=true\nclaim_amount_hard_limit=2000.00\nharmless_greeting_present_in_the_message=true\nfree_of_legal_complaints=true\nclaim_form_filled_in_with_the_usual_font=true\nclaim_free_of_ombudsman_cases=true",
  "question": "Proposed action: go_ahead\nFrom an audit standpoint, is the proposed action the right call for this request?",
  "definitions": "Meanings:\n- put_on_hold: hold the request until the check is done\n- go_ahead: go on and finish it the path is clear\n- turn_down: make sure the requester never gets what they wanted\n- send_to_a_person: submit the question to the authorised decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd43c7df400",
  "kind": "yes/no",
  "text": "---\n# extract\nrequest_id: REQ-8418\nrequester: فارس مهند الجبوري\nnote: صلاحية الوصول المطلوبة تتوافق مع دور الموظف الوظيفي.\naccess_days: 2\nrequester_barred_from_this_system: false\nrequest_grants_admin_rights: false\nlegal_preservation_order_on_the_account: false\nethics_office_flagged_the_request: false\nrequest_text_written_in_capital_letters: false\nbusiness_justification_missing: true\naccess_days_approval_threshold: 30\nmfa_enrollment_incomplete: false\nrequested_role_permitted_by_policy: true\naccount_suspended: false",
  "question": "Proposed action: defer\nUpon audit, is the proposed action the correct determination given the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if account_suspended is true or requested_role_permitted_by_policy is false or request_grants_admin_rights is true.\n2. ask manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. defer if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7c1e3b2ed3",
  "kind": "choice",
  "text": "---\n# record\nmeta:\n    ticket_id: \"TCK-9749\"\n    customer: \"Sana Petrov\"\nmetrics:\n    claim_amount_hard_limit: 1000.00\n    claim_amount: 1000.01\nsignals:\n    legal_complaint_filed: false\n    claim_involves_a_media_inquiry: false\n    claim_free_of_ombudsman_cases: true\n    harmless_greeting_present_in_the_message: true\n    proof_of_purchase_missing: false\n    free_of_safety_incident_reports: true\n    item_excluded_by_policy: false\n    item_return_received: true\n    claim_form_filled_in_with_the_usual_font: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. turn down if item_excluded_by_policy is true or legal_complaint_filed is true or claim_amount is above claim_amount_hard_limit.\n3. send to a person if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: go ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "turn down",
   "go ahead",
   "put on hold"
  ]
 },
 {
  "qid": "qdfa29c9830",
  "kind": "yes/no",
  "text": "# request record\nticket_id                                | TCK-6842\ncustomer                                 | Sana Ferreira\nclaim_free_of_ombudsman_cases            | true\nclaim_involves_a_media_inquiry           | false\nitem_return_received                     | false\nclaim_form_filled_in_with_the_usual_font | false\nfree_of_safety_incident_reports          | true\nclaim_amount                             | 100.00\nitem_excluded_by_policy                  | false\nclaim_amount_hard_limit                  | 100.00\nharmless_greeting_present_in_the_message | true\nfree_of_legal_complaints                 | true\nproof_of_purchase_attached               | true",
  "question": "Proposed action: defer\nIs it not the case that the facts behind this case back the proposed action and that it is not mistaken?",
  "definitions": "Meanings:\n- defer: pause this until the requester supplies the missing document\n- approve: let this be advanced exactly as originally specified\n- deny: be turned away and treated as off limits\n- ask manager: delegate the call to whoever holds authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5d9156ef3c",
  "kind": "yes/no",
  "text": "{\"run_id\": \"RUN-8560\", \"agent\": \"garnet\", \"log_lines_written_in_a_verbose_style\": false, \"action_free_of_ethics_concerns\": true, \"action_forbidden_by_security_policy\": false, \"steps_used_hard_limit\": 40, \"last_tool_output_verified\": false, \"tool_output_shows_tampering\": false, \"task_description_complete\": true, \"steps_used\": 14, \"owner_sign_off_required_for_this_action\": false}",
  "question": "Proposed action: turn_down\nFrom an audit standpoint, have the facts in the record ruled out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q2def4841f1",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-3152\nvendor | Brightwater Foods\nvendor_filed_a_legal_claim_over_this_invoice | false\npurchase_order_received | true\npayment_requested_during_business_hours | true\nvendor_tax_form_missing | true\ninvoice_pdf_uses_a_landscape_layout | false\nvendor_name_written_in_capital_letters | false\namount | 3466.21\napprover_declared_a_conflict_of_interest | false\nvendor_on_sanctions_list | false\namount_approval_threshold | 25000.00\nduplicate_of_paid_invoice | false",
  "question": "Proposed action: go_ahead\nAuditing this request closely, is the proposed action not a defensible choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. turn_down if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. put_on_hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- go_ahead: keep moving on this one nothing is holding it up\n- send_to_a_person: hand the matter to a decider so the requester gets a verdict\n- put_on_hold: be parked until a verification has been logged\n- turn_down: withdraw from the step as it is forbidden\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q85d4306b01",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n* run id: RUN-7792\n* agent: jasper\n* steps used hard limit: 30\n* last tool output verified: yes\n* log lines written in a compact style: yes\n* task description incomplete: no\n* tool output shows tampering: no\n* action permitted by security policy: yes\n* action free of ethics concerns: no\n* steps used: 29\n* owner sign off required for this action: no",
  "question": "Proposed action: 9680\nIs the proposed action the right call for this request, as the record shows it?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 96 if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is at least steps_used_hard_limit.\n2. 9 if task_description_incomplete is true or owner_sign_off_required_for_this_action is true.\n3. 9680 if action_free_of_ethics_concerns is false.\nOtherwise: 834.\nNever counted: last_tool_output_verified, log_lines_written_in_a_compact_style.\nMeanings:\n- 96: block it right away\n- 9680: hand the matter to a decider so the requester gets a verdict\n- 9: stall the request until the check comes back\n- 834: allow the matter to be taken forward as planned\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qbf37056e4a",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-9410\n- vendor: Redwood Works\n- awaiting purchase order: no\n- vendor filed a legal claim over this invoice: no\n- invoice pdf uses a portrait layout: yes\n- amount: 2450.72\n- amount approval threshold: 2500.00\n- payment requested during business hours: yes\n- vendor name written in capital letters: no\n- vendor tax form on file: yes\n- approver free of conflicts of interest: yes\n- vendor free of sanctions: yes\n- duplicate of paid invoice: no",
  "question": "Proposed action: escalate\nIs the proposed action the appropriate procedure for the request set out in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if approver_free_of_conflicts_of_interest is false.\n2. reject if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qab90e6939a",
  "kind": "choice",
  "text": "{\n    \"request\":{\n        \"ticket_id\":\"TCK-2708\",\n        \"customer\":\"Jonas Castell\"\n    },\n    \"figures\":{\n        \"claim_amount_hard_limit\":500.00,\n        \"claim_amount\":353.35\n    },\n    \"checks\":{\n        \"item_return_received\":true,\n        \"item_excluded_by_policy\":false,\n        \"claim_free_of_ombudsman_cases\":true,\n        \"claim_form_filled_in_with_the_usual_font\":true,\n        \"proof_of_purchase_missing\":true,\n        \"free_of_safety_incident_reports\":true,\n        \"harmless_greeting_present_in_the_message\":true,\n        \"free_of_legal_complaints\":true,\n        \"claim_involves_a_media_inquiry\":false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. put on hold if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\n3. send to a person if item_return_received is false or free_of_legal_complaints is false or free_of_safety_incident_reports is false.\nOtherwise: go ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed would be the right call for the matter in this file?",
  "options": [
   "put on hold",
   "send to a person",
   "go ahead"
  ]
 },
 {
  "qid": "q74288e3454",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-6162\n  vendor: Oakmont Systems\nvalues:\n  amount: 66.96\n  amount_approval_threshold: 500.00\ntests:\n  invoice_pdf_uses_a_landscape_layout: false\n  vendor_filed_a_legal_claim_over_this_invoice: false\n  vendor_free_of_sanctions: false\n  payment_requested_during_business_hours: true\n  vendor_name_written_in_capital_letters: false\n  duplicate_of_paid_invoice: false\n  purchase_order_received: true\n  approver_free_of_conflicts_of_interest: true\n  vendor_tax_form_on_file: true",
  "question": "Proposed action: cancel_order\nIs it not so that the proposed action we have on the table is not a poor choice for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q012082a630",
  "kind": "choice",
  "text": "---\nrequest:\n    request_id: REQ-6321\n    requester: Sana Calloway\nfigures:\n    access_days_approval_threshold: 60\n    access_days: 60\nchecks:\n    business_justification_missing: false\n    account_suspended: false\n    requester_not_barred_from_this_system: true\n    legal_preservation_order_on_the_account: false\n    requested_role_forbidden_by_policy: true\n    request_grants_admin_rights: false\n    mfa_enrollment_incomplete: false\n    request_text_written_in_capital_letters: false\n    request_free_of_ethics_office_flags: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n2. refuse if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. refer to owner if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: grant.\nNever counted: request_free_of_ethics_office_flags, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nQuick question: which of the actions listed after this is the best call?",
  "options": [
   "refer to owner",
   "refuse",
   "grant"
  ]
 },
 {
  "qid": "q0267d7ed27",
  "kind": "yes/no",
  "text": "ticket_id=TCK-2805\ncustomer=Sana Keller\nclaim_form_filled_in_with_the_usual_font=true\nharmless_greeting_present_in_the_message=true\nclaim_free_of_ombudsman_cases=true\nclaim_amount=1388.92\nitem_return_received=true\nclaim_involves_a_media_inquiry=false\nitem_excluded_by_policy=true\nfree_of_safety_incident_reports=false\nfree_of_legal_complaints=true\nproof_of_purchase_attached=true\nclaim_amount_hard_limit=2000.00",
  "question": "Proposed action: approve\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false.\n2. deny if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_received is false.\nOtherwise: approve.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qca8fc2aaea",
  "kind": "yes/no",
  "text": "ticket_id | TCK-3788\ncustomer | Felix Duarte\nitem_excluded_by_policy | false\nlegal_complaint_filed | false\nclaim_involves_a_media_inquiry | false\nclaim_free_of_ombudsman_cases | true\nitem_return_not_yet_received | true\nclaim_amount | 43.16\nharmless_greeting_present_in_the_message | false\nproof_of_purchase_missing | false\nclaim_form_filled_in_with_the_usual_font | true\nfree_of_safety_incident_reports | true\nclaim_amount_hard_limit | 200.00",
  "question": "Proposed action: defer\nIs the proposed action not suited to this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false.\n2. deny if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_not_yet_received is true.\nOtherwise: approve.\nNever counted: proof_of_purchase_missing, item_excluded_by_policy, legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- approve: continue the work as originally asked, there is nothing in the way\n- ask manager: be passed along to whoever makes the call\n- defer: wait so the requester can supply more information first\n- deny: be blocked outright so it never gets carried out\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7dc2c45ac1",
  "kind": "choice",
  "text": "---\ndeploy_id: DEP-5267\nservice: checkout\ncommit_messages_written_in_a_detailed_style: true\ndeploy_has_a_long_description: false\nbackout_plan_documented: false\nfiles_changed_soft_limit: 30\ndeploy_prohibited_during_the_audit_window: false\ndeploy_blocked_by_security_policy: false\nrollout_approval_revoked: false\nfiles_changed: 29\nservice_free_of_major_incidents: true\ncanary_results_incomplete: false\ncontract_customer_asked_for_a_say_in_this_rollout: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if backout_plan_documented is false.\n2. turn down if rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is at least files_changed_soft_limit.\n3. send to a person if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style.\nMeanings:\n- put on hold: stay put until the check is finished\n- go ahead: execute the requested action as nothing prevents it\n- send to a person: be routed to whoever holds the decision\n- turn down: scrap the plan and drop this request\nThe record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "put on hold",
   "go ahead",
   "send to a person"
  ]
 },
 {
  "qid": "qf3b0dda226",
  "kind": "yes/no",
  "text": "{\n  \"record\": {\n    \"ticket_id\": \"TCK-6456\",\n    \"customer\": \"Omar Castell\"\n  },\n  \"numbers\": {\n    \"claim_amount\": 1405.63,\n    \"claim_amount_hard_limit\": 2000.00\n  },\n  \"flags\": {\n    \"item_return_received\": true,\n    \"claim_free_of_ombudsman_cases\": true,\n    \"proof_of_purchase_missing\": false,\n    \"item_excluded_by_policy\": false,\n    \"claim_involves_a_media_inquiry\": false,\n    \"harmless_greeting_present_in_the_message\": true,\n    \"legal_complaint_filed\": false,\n    \"claim_form_filled_in_with_the_usual_font\": true,\n    \"free_of_safety_incident_reports\": true\n  }\n}",
  "question": "Proposed action: defer\nDoes what the record shows suggest the proposed action is not the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q29847834d6",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-6806\nvendor = Cedar Supply\nawaiting_purchase_order = false\nvendor_on_sanctions_list = true\nvendor_filed_a_legal_claim_over_this_invoice = false\nduplicate_of_paid_invoice = false\ninvoice_pdf_uses_a_portrait_layout = true\nvendor_tax_form_on_file = true\npayment_requested_during_business_hours = false\nvendor_name_written_in_capital_letters = false\napprover_declared_a_conflict_of_interest = false\namount_approval_threshold = 500.00\namount = 121.80",
  "question": "Proposed action: cancel_order\nWould the proposed action be the right answer to what this request calls for?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true or amount is at least amount_approval_threshold.\n2. delay if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. cancel_order if duplicate_of_paid_invoice is true.\nOtherwise: release.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q79d41e1001",
  "kind": "choice",
  "text": "---\ncase:\n    invoice_id: \"INV-2180\"\n    vendor: \"Northwind Industries\"\nvalues:\n    amount_approval_threshold: 1000.00\n    amount: 782.99\ntests:\n    vendor_tax_form_on_file: true\n    vendor_filed_a_legal_claim_over_this_invoice: false\n    payment_requested_during_business_hours: true\n    duplicate_of_paid_invoice: false\n    vendor_on_sanctions_list: true\n    awaiting_purchase_order: false\n    invoice_pdf_uses_a_landscape_layout: false\n    vendor_name_written_in_capital_letters: false\n    approver_declared_a_conflict_of_interest: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. deny if duplicate_of_paid_invoice is true.\n3. ask_manager if vendor_on_sanctions_list is true or approver_declared_a_conflict_of_interest is true or amount is at least amount_approval_threshold.\nOtherwise: approve.\nNever counted: awaiting_purchase_order, vendor_tax_form_on_file, payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nConsidering what was asked and the facts available, which action below should be chosen?",
  "options": [
   "approve",
   "defer",
   "ask_manager"
  ]
 },
 {
  "qid": "q4104628ae0",
  "kind": "yes/no",
  "text": "---\n# record\nrun_id: \"RUN-1245\"\nagent: \"garnet\"\nlog_lines_written_in_a_compact_style: false\nlast_tool_output_verified: true\naction_forbidden_by_security_policy: false\ntask_description_complete: true\nsteps_used_hard_limit: 16\nsteps_used: 15\ntool_output_shows_tampering: false\naction_free_of_ethics_concerns: true\nowner_sign_off_required_for_this_action: false",
  "question": "Proposed action: 695\nIs it not correct that the proposed action is not off base, judging by the record on file?",
  "definitions": "Meanings:\n- 94: hold off until more information arrives\n- 5: escalate this to someone senior who decides\n- 695: push ahead as planned\n- 5136: send the requester away with the request left unfinished\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9a60f58630",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-8566\", \"vendor\": \"Cedar Labs\", \"invoice_pdf_uses_a_landscape_layout\": false, \"payment_requested_during_business_hours\": true, \"duplicate_of_paid_invoice\": false, \"vendor_name_written_in_capital_letters\": false, \"amount\": 614.01, \"approver_declared_a_conflict_of_interest\": false, \"amount_approval_threshold\": 1000.00, \"purchase_order_received\": true, \"vendor_free_of_sanctions\": true, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"vendor_tax_form_on_file\": true}",
  "question": "Proposed action: deny\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. deny if duplicate_of_paid_invoice is true.\n3. ask manager if vendor_free_of_sanctions is false or approver_declared_a_conflict_of_interest is true or amount is at least amount_approval_threshold.\nOtherwise: approve.\nNever counted: purchase_order_received, vendor_tax_form_on_file, payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q60260e6ab7",
  "kind": "yes/no",
  "text": "ticket_id=TCK-1351\ncustomer=Elena Ferreira\nfree_of_safety_incident_reports=true\nclaim_form_filled_in_with_the_usual_font=true\nclaim_involves_a_media_inquiry=false\nfree_of_legal_complaints=true\nproof_of_purchase_attached=true\nclaim_free_of_ombudsman_cases=true\nitem_excluded_by_policy=false\nclaim_amount_hard_limit=50.00\nclaim_amount=50.00\nitem_return_not_yet_received=false\nharmless_greeting_present_in_the_message=true",
  "question": "Proposed action: approve\nWould the proposed action not be the appropriate course under the applicable procedure?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false or claim_free_of_ombudsman_cases is false.\n2. deny if proof_of_purchase_attached is false or item_excluded_by_policy is true or claim_involves_a_media_inquiry is true or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_not_yet_received is true.\nOtherwise: approve.\nNever counted: free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- ask manager: send this on to whoever decides\n- approve: proceed as asked since everything is cleared\n- deny: refuse to act since the step is prohibited\n- defer: suspend action until the facts are confirmed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfc0232b141",
  "kind": "choice",
  "text": "# case\nrequest_id: REQ-8172\nrequester: Priya Tanaka\nbusiness_justification_provided: false\nethics_office_flagged_the_request: false\naccess_days: 45\nrequester_not_barred_from_this_system: true\naccess_days_approval_threshold: 45\nmfa_enrollment_incomplete: false\naccount_suspended: false\nrequested_role_forbidden_by_policy: false\nlegal_preservation_order_on_the_account: false\nrequest_text_written_in_capital_letters: false\nrequest_grants_admin_rights: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. block access if account_suspended is true or requested_role_forbidden_by_policy is true or request_grants_admin_rights is true.\n2. page oncall if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. quarantine if business_justification_provided is false or mfa_enrollment_incomplete is true or requester_not_barred_from_this_system is false or ethics_office_flagged_the_request is true.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- quarantine: freeze progress until the paperwork arrives\n- page oncall: hand it up to the person who decides\n- allow: run with it carry on as you were\n- block access: bin this idea and keep it out of the flow\nThe record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "quarantine",
   "page oncall",
   "allow"
  ]
 },
 {
  "qid": "q9b6fde34f8",
  "kind": "yes/no",
  "text": "# request record\nticket_id                                | TCK-2892\ncustomer                                 | Ravi Keller\nitem_return_not_yet_received             | false\nharmless_greeting_present_in_the_message | true\nclaim_free_of_ombudsman_cases            | true\nlegal_complaint_filed                    | false\nitem_excluded_by_policy                  | false\nclaim_amount                             | 414.11\nclaim_form_filled_in_with_the_usual_font | true\nclaim_amount_hard_limit                  | 2000.00\nfree_of_safety_incident_reports          | true\nproof_of_purchase_missing                | false\nclaim_involves_a_media_inquiry           | true",
  "question": "Proposed action: turn down\nDo the facts we have help rule out the proposed action here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if item_return_not_yet_received is true or claim_free_of_ombudsman_cases is false.\n2. turn down if item_excluded_by_policy is true or legal_complaint_filed is true or claim_amount is above claim_amount_hard_limit.\n3. send to a person if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: go ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- turn down: block this from going any further\n- put on hold: wait for that check then we will see\n- go ahead: just crack on with it there is nothing in the way\n- send to a person: give it to a person who has the authority to decide\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qba98f43d8e",
  "kind": "choice",
  "text": "# case\ndeploy_id: DEP-7748\nservice: uploads\nservice_free_of_major_incidents: true\nrollout_approval_revoked: true\ncanary_results_incomplete: false\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_prohibited_during_the_audit_window: false\ncommit_messages_written_in_a_detailed_style: false\ndeploy_blocked_by_security_policy: false\nfiles_changed_soft_limit: 10\nbackout_plan_documented: true\nfiles_changed: 10\ndeploy_has_a_long_description: false",
  "question": "The record is complete: nothing else applies.\n\nReading the file for this case, which listed action is the best call?",
  "options": [
   "put on hold",
   "go ahead",
   "turn down"
  ]
 },
 {
  "qid": "qe2d3e95229",
  "kind": "choice",
  "text": "---\nrequest:\n    run_id: RUN-2928\n    agent: indigo\nfigures:\n    steps_used: 15\n    steps_used_hard_limit: 16\nchecks:\n    tool_output_shows_tampering: false\n    last_tool_output_unverified: false\n    owner_sign_off_required_for_this_action: false\n    log_lines_written_in_a_verbose_style: false\n    task_description_incomplete: false\n    action_forbidden_by_security_policy: false\n    action_free_of_ethics_concerns: true",
  "question": "The record is complete: nothing else applies.\n\nLooking across the actions listed, what would be the correct response to this request?",
  "options": [
   "put on hold",
   "send to a person",
   "go ahead"
  ]
 },
 {
  "qid": "q50492fd276",
  "kind": "choice",
  "text": "{\"request_id\": \"REQ-4275\", \"requester\": \"Nadia Vasquez\", \"access_days\": 71, \"request_grants_admin_rights\": false, \"legal_preservation_order_on_the_account\": false, \"requester_not_barred_from_this_system\": true, \"account_suspended\": false, \"mfa_enrollment_incomplete\": false, \"requested_role_permitted_by_policy\": true, \"business_justification_missing\": false, \"request_text_written_in_capital_letters\": false, \"access_days_approval_threshold\": 60, \"ethics_office_flagged_the_request\": false}",
  "question": "Meanings:\n- pend: keep waiting for the missing details\n- refuse: refuse this request entirely\n- refer_to_owner: escalate this to someone senior who decides\n- grant: advance the task as stated without any blockers\nThe record is complete: nothing else applies.\n\nFrom the requester's side, which of the actions listed below is the right call for this request?",
  "options": [
   "refer_to_owner",
   "grant",
   "refuse"
  ]
 },
 {
  "qid": "q843c1e707a",
  "kind": "yes/no",
  "text": "ticket_id=TCK-9266\ncustomer=Idris Keller\nitem_return_not_yet_received=false\nclaim_form_filled_in_with_the_usual_font=true\nclaim_involves_a_media_inquiry=false\nharmless_greeting_present_in_the_message=true\nclaim_free_of_ombudsman_cases=true\nfree_of_safety_incident_reports=true\nfree_of_legal_complaints=true\nclaim_amount_hard_limit=100.00\nitem_excluded_by_policy=false\nclaim_amount=99.99\nproof_of_purchase_attached=true",
  "question": "Proposed action: go_ahead\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if item_return_not_yet_received is true or claim_free_of_ombudsman_cases is false.\n2. put_on_hold if proof_of_purchase_attached is false or claim_amount is at least claim_amount_hard_limit.\n3. turn_down if item_excluded_by_policy is true or free_of_legal_complaints is false or claim_involves_a_media_inquiry is true.\nOtherwise: go_ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9f4acd3850",
  "kind": "yes/no",
  "text": "{\"request_id\":\"REQ-4030\",\"requester\":\"ريم سامي الزهراني\",\"note\":\"ينتظر الطلب رد القسم المختص بشأن الصلاحية المطلوبة.\",\"requester_not_barred_from_this_system\":true,\"legal_preservation_order_on_the_account\":false,\"request_grants_admin_rights\":false,\"request_text_written_in_capital_letters\":false,\"request_free_of_ethics_office_flags\":true,\"account_suspended\":false,\"requested_role_permitted_by_policy\":true,\"business_justification_provided\":true,\"access_days_approval_threshold\":45,\"mfa_enrollment_complete\":true,\"access_days\":23}",
  "question": "Proposed action: 31\nQuick question: is the proposed action the right thing to do with this request?",
  "definitions": "Meanings:\n- 7819: have the task carried out as it was originally asked\n- 31: pump the brakes until more details show up\n- 434: bring in the authority who can settle it for the requester\n- 4: end it so the requester sees their request closed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qaa507754e0",
  "kind": "choice",
  "text": "{\"deploy_id\": \"DEP-5126\", \"service\": \"scheduler\", \"deploy_has_a_long_description\": false, \"files_changed_soft_limit\": 10, \"contract_customer_asked_for_a_say_in_this_rollout\": false, \"deploy_prohibited_during_the_audit_window\": false, \"rollout_approval_revoked\": false, \"commit_messages_written_in_a_detailed_style\": false, \"backout_plan_missing\": false, \"service_free_of_major_incidents\": true, \"deploy_blocked_by_security_policy\": false, \"canary_results_complete\": false, \"files_changed\": 7}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if backout_plan_missing is true.\n2. turn_down if rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is at least files_changed_soft_limit.\n3. send_to_a_person if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\nOtherwise: go_ahead.\nNever counted: canary_results_complete, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style.\nThe record is complete: nothing else applies.\n\nIf you were deciding, which of the actions listed after this fits best?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "turn_down"
  ]
 },
 {
  "qid": "q35c6ef41fa",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n- ticket id: TCK-3692\n- customer: Priya Imai\n- item return not yet received: yes\n- claim free of ombudsman cases: yes\n- item excluded by policy: no\n- claim involves a media inquiry: yes\n- claim amount hard limit: 100.00\n- claim amount: 77.71\n- proof of purchase missing: no\n- legal complaint filed: yes\n- claim form filled in with the usual font: yes\n- harmless greeting present in the message: no\n- free of safety incident reports: yes",
  "question": "Proposed action: MCN\nIs the proposed action the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. W if free_of_safety_incident_reports is false or claim_free_of_ombudsman_cases is false.\n2. SQ if proof_of_purchase_missing is true or item_excluded_by_policy is true or claim_involves_a_media_inquiry is true or claim_amount is above claim_amount_hard_limit.\n3. WBXG if item_return_not_yet_received is true.\nOtherwise: MCN.\nNever counted: legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- SQ: skip this one, it is a hard pass for us\n- WBXG: pump the brakes until more details show up\n- W: pass this along to the decision maker\n- MCN: proceed as asked since everything is cleared\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7700bf429a",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n    invoice_id: INV-9900\n    vendor: Stonebridge Traders\namounts:\n    amount_approval_threshold: 10000.00\n    amount: 1771.14\nchecks:\n    approver_declared_a_conflict_of_interest: false\n    duplicate_of_paid_invoice: false\n    vendor_free_of_sanctions: true\n    payment_requested_during_business_hours: true\n    vendor_name_written_in_capital_letters: false\n    purchase_order_received: true\n    invoice_pdf_uses_a_portrait_layout: false\n    vendor_tax_form_missing: false\n    vendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. turn_down if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. put_on_hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "put_on_hold",
   "send_to_a_person",
   "go_ahead"
  ]
 },
 {
  "qid": "q62a90c85ba",
  "kind": "choice",
  "text": "{\n    \"subject\":{\n        \"run_id\":\"RUN-3685\",\n        \"agent\":\"jasper\"\n    },\n    \"amounts\":{\n        \"steps_used_hard_limit\":30,\n        \"steps_used\":31\n    },\n    \"checks\":{\n        \"action_forbidden_by_security_policy\":false,\n        \"owner_sign_off_required_for_this_action\":false,\n        \"log_lines_written_in_a_verbose_style\":false,\n        \"action_free_of_ethics_concerns\":true,\n        \"tool_output_shows_tampering\":false,\n        \"task_description_incomplete\":false,\n        \"last_tool_output_unverified\":false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put on hold if task_description_incomplete is true or steps_used is above steps_used_hard_limit.\n3. send to a person if action_forbidden_by_security_policy is true or owner_sign_off_required_for_this_action is true.\nOtherwise: go ahead.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nFrom the requester's side, which of the actions listed below is the right call for this request?",
  "options": [
   "go ahead",
   "put on hold",
   "send to a person"
  ]
 },
 {
  "qid": "q00f3ef9ef2",
  "kind": "yes/no",
  "text": "# request record\nticket_id: TCK-6395\ncustomer: Ravi Ferreira\nclaim_involves_a_media_inquiry: false\nclaim_free_of_ombudsman_cases: true\nharmless_greeting_present_in_the_message: true\nitem_excluded_by_policy: false\nitem_return_received: true\nfree_of_legal_complaints: true\nclaim_form_filled_in_with_the_usual_font: true\nclaim_amount: 1000.01\nproof_of_purchase_missing: false\nclaim_amount_hard_limit: 1000.00\nfree_of_safety_incident_reports: true",
  "question": "Proposed action: go_ahead\nIs it not correct that the evidence points toward the proposed action, and it is not a poor choice?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q9d785ccf1f",
  "kind": "yes/no",
  "text": "---\n# extract\nrequest_id: REQ-8418\nrequester: فارس مهند الجبوري\nnote: صلاحية الوصول المطلوبة تتوافق مع دور الموظف الوظيفي.\naccess_days: 2\nrequester_barred_from_this_system: false\nrequest_grants_admin_rights: false\nlegal_preservation_order_on_the_account: false\nethics_office_flagged_the_request: false\nrequest_text_written_in_capital_letters: false\nbusiness_justification_missing: false\naccess_days_approval_threshold: 30\nmfa_enrollment_incomplete: false\nrequested_role_permitted_by_policy: true\naccount_suspended: false",
  "question": "Proposed action: defer\nUpon audit, is the proposed action the correct determination given the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if account_suspended is true or requested_role_permitted_by_policy is false or request_grants_admin_rights is true.\n2. ask manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. defer if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc8c96ec168",
  "kind": "choice",
  "text": "{\n    \"record\": {\n        \"request_id\": \"REQ-7123\",\n        \"requester\": \"Marta Sorensen\"\n    },\n    \"numbers\": {\n        \"access_days_approval_threshold\": 90,\n        \"access_days\": 91\n    },\n    \"flags\": {\n        \"request_text_written_in_capital_letters\": true,\n        \"mfa_enrollment_complete\": true,\n        \"request_grants_admin_rights\": false,\n        \"legal_preservation_order_on_the_account\": false,\n        \"requester_barred_from_this_system\": false,\n        \"request_free_of_ethics_office_flags\": true,\n        \"account_suspended\": false,\n        \"requested_role_forbidden_by_policy\": false,\n        \"business_justification_missing\": false\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nWhich of these actions should we take for this request?",
  "options": [
   "defer",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "qb30499c1c5",
  "kind": "choice",
  "text": "{\"deploy_id\": \"DEP-1470\", \"service\": \"catalog\", \"rollout_approval_revoked\": false, \"backout_plan_documented\": true, \"files_changed_soft_limit\": 15, \"deploy_has_a_long_description\": false, \"canary_results_incomplete\": true, \"contract_customer_asked_for_a_say_in_this_rollout\": true, \"service_free_of_major_incidents\": true, \"files_changed\": 12, \"commit_messages_written_in_a_detailed_style\": true, \"deploy_blocked_by_security_policy\": false, \"deploy_prohibited_during_the_audit_window\": false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if backout_plan_documented is false or files_changed is above files_changed_soft_limit.\n2. turn down if deploy_blocked_by_security_policy is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true.\n3. send to a person if service_free_of_major_incidents is false or contract_customer_asked_for_a_say_in_this_rollout is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style.\nThe record is complete: nothing else applies.\n\nChecklist: which of the actions listed below best answers the request?",
  "options": [
   "send to a person",
   "put on hold",
   "go ahead"
  ]
 },
 {
  "qid": "q1cb2345d3e",
  "kind": "choice",
  "text": "request_id=REQ-4319\nrequester=Felix Brandt\naccess_days_approval_threshold=60\naccount_suspended=false\nlegal_preservation_order_on_the_account=false\nrequest_grants_admin_rights=false\nmfa_enrollment_complete=true\nrequested_role_forbidden_by_policy=true\nrequester_barred_from_this_system=false\nbusiness_justification_provided=true\nrequest_text_written_in_capital_letters=false\nrequest_free_of_ethics_office_flags=true\naccess_days=24",
  "question": "The record is complete: nothing else applies.\n\nWhich of the listed actions do the facts support as the right call?",
  "options": [
   "block_access",
   "allow",
   "quarantine"
  ]
 },
 {
  "qid": "q38f6ada4e4",
  "kind": "choice",
  "text": "# record\nrun_id: RUN-3394\nagent: fjord\naction_free_of_ethics_concerns: true\ntool_output_shows_tampering: false\nlog_lines_written_in_a_compact_style: true\nsteps_used_hard_limit: 12\nsteps_used: 2\ntask_description_complete: true\nlast_tool_output_verified: true\nowner_sign_off_required_for_this_action: true\naction_permitted_by_security_policy: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if owner_sign_off_required_for_this_action is true.\n2. turn down if action_permitted_by_security_policy is false.\n3. put on hold if last_tool_output_verified is false or task_description_complete is false or action_free_of_ethics_concerns is false or steps_used is above steps_used_hard_limit.\nOtherwise: go ahead.\nNever counted: tool_output_shows_tampering, log_lines_written_in_a_compact_style.\nMeanings:\n- put on hold: stay on hold until the paperwork arrives\n- turn down: kill this one off\n- send to a person: escalate this to someone senior who decides\n- go ahead: have the item pushed forward as the request stated\nThe record is complete: nothing else applies.\n\nReading the file for this case, which listed action is the best call?",
  "options": [
   "go ahead",
   "send to a person",
   "turn down"
  ]
 },
 {
  "qid": "q21e76346d0",
  "kind": "choice",
  "text": "---\n# record\nrecord:\n  invoice_id: \"INV-9422\"\n  vendor: \"Pinecrest Industries\"\nnumbers:\n  amount_approval_threshold: 2500.00\n  amount: 1571.40\nflags:\n  approver_free_of_conflicts_of_interest: true\n  awaiting_purchase_order: false\n  payment_requested_during_business_hours: true\n  vendor_filed_a_legal_claim_over_this_invoice: false\n  vendor_tax_form_on_file: true\n  duplicate_of_paid_invoice: true\n  vendor_name_written_in_capital_letters: false\n  invoice_pdf_uses_a_landscape_layout: false\n  vendor_on_sanctions_list: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if vendor_filed_a_legal_claim_over_this_invoice is true or approver_free_of_conflicts_of_interest is false or amount is at least amount_approval_threshold.\n2. hold if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n3. reject if duplicate_of_paid_invoice is true.\nOtherwise: pay.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "pay",
   "reject",
   "escalate"
  ]
 },
 {
  "qid": "q9f6e6ffdff",
  "kind": "choice",
  "text": "---\nrequest:\n  ticket_id: TCK-5505\n  customer: وفاء محسن الفارس\n  note: تم التحقق من الهوية وكل ما يتعلق بالطلب سليم.\nfigures:\n  claim_amount: 185.03\n  claim_amount_hard_limit: 200.00\nchecks:\n  legal_complaint_filed: false\n  claim_involves_a_media_inquiry: false\n  free_of_safety_incident_reports: false\n  claim_form_filled_in_with_the_usual_font: true\n  item_return_received: true\n  harmless_greeting_present_in_the_message: false\n  proof_of_purchase_attached: true\n  item_excluded_by_policy: false\n  claim_free_of_ombudsman_cases: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. put_on_hold if proof_of_purchase_attached is false or claim_amount is at least claim_amount_hard_limit.\n3. turn_down if item_excluded_by_policy is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\nOtherwise: go_ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "put_on_hold",
   "turn_down",
   "go_ahead"
  ]
 },
 {
  "qid": "q83d211f2fc",
  "kind": "choice",
  "text": "{\n    \"request\": {\n        \"ticket_id\": \"TCK-8849\",\n        \"customer\": \"Yara Rossi\"\n    },\n    \"figures\": {\n        \"claim_amount\": 14.58,\n        \"claim_amount_hard_limit\": 100.00\n    },\n    \"checks\": {\n        \"claim_form_filled_in_with_the_usual_font\": true,\n        \"claim_free_of_ombudsman_cases\": true,\n        \"claim_involves_a_media_inquiry\": false,\n        \"item_return_not_yet_received\": false,\n        \"proof_of_purchase_missing\": true,\n        \"item_excluded_by_policy\": true,\n        \"harmless_greeting_present_in_the_message\": true,\n        \"free_of_legal_complaints\": true,\n        \"free_of_safety_incident_reports\": true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if item_return_not_yet_received is true or free_of_safety_incident_reports is false.\n2. put on hold if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. send to a person if proof_of_purchase_missing is true or free_of_legal_complaints is false or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: go ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "go ahead",
   "send to a person",
   "put on hold"
  ]
 },
 {
  "qid": "q7dfd6c064c",
  "kind": "choice",
  "text": "---\n# request record\nsubject:\n  request_id: \"REQ-4089\"\n  requester: \"صالح كمال الهاشمي\"\n  note: \"المستندات المطلوبة للوصول كاملة ومرفقة بالطلب.\"\namounts:\n  access_days_approval_threshold: 60\n  access_days: 36\nchecks:\n  request_free_of_ethics_office_flags: true\n  request_text_written_in_capital_letters: false\n  requester_barred_from_this_system: false\n  business_justification_missing: false\n  account_suspended: false\n  request_grants_admin_rights: false\n  legal_preservation_order_on_the_account: false\n  requested_role_permitted_by_policy: true\n  mfa_enrollment_incomplete: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action below would serve the person who made this request best?",
  "options": [
   "refuse",
   "grant",
   "refer to owner"
  ]
 },
 {
  "qid": "q2e3d651ff1",
  "kind": "choice",
  "text": "# request record\ninvoice_id: INV-2776\nvendor: Harbor Labs\nvendor_on_sanctions_list: false\nvendor_filed_a_legal_claim_over_this_invoice: false\namount: 189.66\ninvoice_pdf_uses_a_landscape_layout: false\napprover_free_of_conflicts_of_interest: true\nawaiting_purchase_order: false\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: true\nvendor_name_written_in_capital_letters: false\namount_approval_threshold: 500.00\nvendor_tax_form_missing: false",
  "question": "Meanings:\n- hand_to_a_person: delegate the call to whoever holds authority\n- cancel_order: toss it out, we are never doing this\n- release: execute the requested action as nothing prevents it\n- delay: be parked until a verification has been logged\nThe record is complete: nothing else applies.\n\nThe record shows the situation; which of the actions listed is the right call?",
  "options": [
   "cancel_order",
   "delay",
   "release"
  ]
 },
 {
  "qid": "q2f85645c2b",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-1633\",\"vendor\":\"Stonebridge Foods\",\"vendor_tax_form_on_file\":true,\"duplicate_of_paid_invoice\":false,\"vendor_name_written_in_capital_letters\":false,\"awaiting_purchase_order\":true,\"amount_approval_threshold\":5000.00,\"vendor_filed_a_legal_claim_over_this_invoice\":false,\"payment_requested_during_business_hours\":false,\"invoice_pdf_uses_a_landscape_layout\":false,\"amount\":2585.37,\"approver_free_of_conflicts_of_interest\":true,\"vendor_on_sanctions_list\":true}",
  "question": "Proposed action: deny\nDo the facts of this request support the proposed action as the correct decision?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if vendor_on_sanctions_list is true or approver_free_of_conflicts_of_interest is false.\n2. ask manager if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. defer if awaiting_purchase_order is true or amount is at least amount_approval_threshold.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- deny: stop the work since it cannot move forward\n- approve: just crack on with it there is nothing in the way\n- ask manager: route the case to a decider so the requester knows the outcome\n- defer: wait for the check and the requester will hear back later\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2d23ed920d",
  "kind": "choice",
  "text": "---\n# request record\ninvoice_id: \"INV-5072\"\nvendor: \"Stonebridge Foods\"\ninvoice_pdf_uses_a_portrait_layout: true\nvendor_tax_form_on_file: true\nvendor_on_sanctions_list: false\namount_approval_threshold: 10000.00\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_name_written_in_capital_letters: false\namount: 10000.00\napprover_declared_a_conflict_of_interest: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\npurchase_order_received: true",
  "question": "Meanings:\n- reject: be rejected in full and never acted upon\n- pay: run the task as it was asked, with nothing standing between it and completion\n- hold: defer further action pending verification of the document\n- escalate: hand this off because a decider has to choose\nThe record is complete: nothing else applies.\n\nWhat is the best action to pick from the list for this request?",
  "options": [
   "hold",
   "pay",
   "escalate"
  ]
 },
 {
  "qid": "q10b4c1c039",
  "kind": "yes/no",
  "text": "# case\nrun_id = RUN-5806\nagent = atlas\nsteps_used_hard_limit = 8\nlog_lines_written_in_a_verbose_style = false\nowner_sign_off_required_for_this_action = false\ntask_description_complete = true\ntool_output_shows_tampering = false\naction_free_of_ethics_concerns = true\naction_forbidden_by_security_policy = false\nlast_tool_output_unverified = false\nsteps_used = 4",
  "question": "Proposed action: go ahead\nIs the proposed action not really the right move for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is at least steps_used_hard_limit.\n2. put on hold if task_description_complete is false or owner_sign_off_required_for_this_action is true.\n3. send to a person if action_free_of_ethics_concerns is false.\nOtherwise: go ahead.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_verbose_style.\nMeanings:\n- turn down: stop the request so the requester gets nothing from it\n- go ahead: carry out the request as written\n- send to a person: send it onward because someone else must decide\n- put on hold: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe9df801141",
  "kind": "choice",
  "text": "---\nrequest:\n  invoice_id: INV-5734\n  vendor: Pinecrest Logistics\nfigures:\n  amount_approval_threshold: 10000.00\n  amount: 1808.28\nchecks:\n  purchase_order_received: true\n  vendor_tax_form_on_file: true\n  approver_free_of_conflicts_of_interest: true\n  invoice_pdf_uses_a_landscape_layout: false\n  duplicate_of_paid_invoice: false\n  vendor_name_written_in_capital_letters: false\n  vendor_filed_a_legal_claim_over_this_invoice: false\n  payment_requested_during_business_hours: true\n  vendor_on_sanctions_list: true",
  "question": "The record is complete: nothing else applies.\n\nAs a manager, which of the actions listed would you pick for this request?",
  "options": [
   "reject",
   "pay",
   "escalate"
  ]
 }
]
