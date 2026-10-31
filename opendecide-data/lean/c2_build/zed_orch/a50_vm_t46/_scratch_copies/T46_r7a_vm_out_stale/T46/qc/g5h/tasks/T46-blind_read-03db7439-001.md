# G5-H blind read T46-blind_read-03db7439-001 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r7a/T46/qc/g5h/answers/T46-blind_read-03db7439-001.json

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
  "qid": "qed88141502",
  "kind": "yes/no",
  "text": "{\n  \"record\": {\n    \"ticket_id\": \"TCK-6456\",\n    \"customer\": \"Omar Castell\"\n  },\n  \"numbers\": {\n    \"claim_amount\": 1405.63,\n    \"claim_amount_hard_limit\": 2000.00\n  },\n  \"flags\": {\n    \"item_return_received\": true,\n    \"claim_free_of_ombudsman_cases\": true,\n    \"proof_of_purchase_missing\": false,\n    \"item_excluded_by_policy\": false,\n    \"claim_involves_a_media_inquiry\": false,\n    \"harmless_greeting_present_in_the_message\": true,\n    \"legal_complaint_filed\": false,\n    \"claim_form_filled_in_with_the_usual_font\": true,\n    \"free_of_safety_incident_reports\": true\n  }\n}",
  "question": "Proposed action: defer\nDoes what the record shows suggest the proposed action is not the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q11087bd119",
  "kind": "choice",
  "text": "---\n# record\ninvoice_id: INV-3674\nvendor: Summit Partners\nvendor_on_sanctions_list: false\namount: 602.11\nvendor_tax_form_missing: false\nvendor_filed_a_legal_claim_over_this_invoice: false\nawaiting_purchase_order: false\napprover_free_of_conflicts_of_interest: false\nduplicate_of_paid_invoice: false\namount_approval_threshold: 1000.00\npayment_requested_during_business_hours: true\nvendor_name_written_in_capital_letters: false\ninvoice_pdf_uses_a_portrait_layout: true",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions below answers the request given the facts you can see?",
  "options": [
   "ask manager",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q9dc9201ee4",
  "kind": "yes/no",
  "text": "run_id | RUN-8561\nagent | kestrel\ntool_output_shows_tampering | false\naction_forbidden_by_security_policy | false\nlast_tool_output_verified | true\naction_free_of_ethics_concerns | true\nsteps_used | 17\nlog_lines_written_in_a_verbose_style | true\nsteps_used_hard_limit | 20\ntask_description_incomplete | false\nowner_sign_off_required_for_this_action | false",
  "question": "Proposed action: go ahead\nIs it not true that the proposed action is not mistaken, given what the record shows?",
  "definitions": "Meanings:\n- put on hold: hold the request so the requester waits for their check\n- go ahead: keep it moving forward\n- turn down: block the action because it is off limits to the team\n- send to a person: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q35eda0c5e6",
  "kind": "yes/no",
  "text": "{\n  \"request\":{\n    \"run_id\":\"RUN-5723\",\n    \"agent\":\"beacon\"\n  },\n  \"figures\":{\n    \"steps_used_hard_limit\":30,\n    \"steps_used\":31\n  },\n  \"checks\":{\n    \"last_tool_output_verified\":true,\n    \"tool_output_shows_tampering\":false,\n    \"owner_sign_off_required_for_this_action\":false,\n    \"task_description_complete\":true,\n    \"action_free_of_ethics_concerns\":true,\n    \"log_lines_written_in_a_compact_style\":false,\n    \"action_forbidden_by_security_policy\":false\n  }\n}",
  "question": "Proposed action: go_ahead\nDoes the record itself rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if owner_sign_off_required_for_this_action is true.\n2. turn_down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is above steps_used_hard_limit.\n3. put_on_hold if last_tool_output_verified is false.\nOtherwise: go_ahead.\nNever counted: task_description_complete, action_free_of_ethics_concerns, log_lines_written_in_a_compact_style.\nMeanings:\n- put_on_hold: park the file until the requester sends the document in\n- send_to_a_person: send it up so the requester gets a firm decision\n- go_ahead: carry on with it now\n- turn_down: refuse to act since the step is prohibited\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q928281d98f",
  "kind": "yes/no",
  "text": "{\n  \"run_id\":\"RUN-2726\",\n  \"agent\":\"kestrel\",\n  \"steps_used_hard_limit\":20,\n  \"last_tool_output_verified\":true,\n  \"owner_sign_off_required_for_this_action\":false,\n  \"action_free_of_ethics_concerns\":true,\n  \"task_description_incomplete\":false,\n  \"action_forbidden_by_security_policy\":false,\n  \"log_lines_written_in_a_compact_style\":false,\n  \"steps_used\":15,\n  \"tool_output_shows_tampering\":true\n}",
  "question": "Proposed action: send_to_a_person\nIs it not so that the proposed action, per what is logged, is not a bad fit?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if owner_sign_off_required_for_this_action is true.\n2. turn_down if action_forbidden_by_security_policy is true.\n3. put_on_hold if last_tool_output_verified is false or task_description_incomplete is true or action_free_of_ethics_concerns is false or steps_used is above steps_used_hard_limit.\nOtherwise: go_ahead.\nNever counted: tool_output_shows_tampering, log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc5c0a30f71",
  "kind": "yes/no",
  "text": "# extract\nticket_id = TCK-9058\ncustomer = Leila Okafor\nitem_excluded_by_policy = false\nitem_return_received = false\nclaim_amount_hard_limit = 2000.00\nclaim_free_of_ombudsman_cases = true\nlegal_complaint_filed = false\nproof_of_purchase_attached = true\nharmless_greeting_present_in_the_message = true\nclaim_involves_a_media_inquiry = false\nfree_of_safety_incident_reports = true\nclaim_amount = 542.52\nclaim_form_filled_in_with_the_usual_font = true",
  "question": "Proposed action: go ahead\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if claim_amount is at least claim_amount_hard_limit.\n2. send to a person if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. put on hold if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: go ahead.\nNever counted: item_return_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- send to a person: kick it up to whoever makes the call\n- turn down: refuse to act since the step is prohibited\n- put on hold: withhold action until supporting information is supplied\n- go ahead: proceed with the task as asked\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q59bfec1bc9",
  "kind": "choice",
  "text": "{\"request_id\":\"REQ-9351\",\"requester\":\"Yara Anand\",\"access_days_approval_threshold\":7,\"requested_role_forbidden_by_policy\":false,\"request_grants_admin_rights\":false,\"account_suspended\":false,\"access_days\":6,\"requester_not_barred_from_this_system\":true,\"request_text_written_in_capital_letters\":true,\"mfa_enrollment_complete\":true,\"legal_preservation_order_on_the_account\":false,\"request_free_of_ethics_office_flags\":true,\"business_justification_missing\":false}",
  "question": "The record is complete: nothing else applies.\n\nGiven what the requester needs, which of the actions below should be taken?",
  "options": [
   "allow",
   "quarantine",
   "page_oncall"
  ]
 },
 {
  "qid": "qdea9097c23",
  "kind": "yes/no",
  "text": "{\n  \"meta\": {\n    \"request_id\": \"REQ-9047\",\n    \"requester\": \"Tomas Imai\"\n  },\n  \"metrics\": {\n    \"access_days\": 4,\n    \"access_days_approval_threshold\": 7\n  },\n  \"signals\": {\n    \"requested_role_permitted_by_policy\": true,\n    \"business_justification_provided\": true,\n    \"mfa_enrollment_incomplete\": true,\n    \"legal_preservation_order_on_the_account\": false,\n    \"ethics_office_flagged_the_request\": false,\n    \"account_suspended\": false,\n    \"requester_not_barred_from_this_system\": true,\n    \"request_text_written_in_capital_letters\": true,\n    \"request_grants_admin_rights\": false\n  }\n}",
  "question": "Proposed action: 289\nIs the proposed action not suited to this request?",
  "definitions": "Meanings:\n- 1: finish it so the requester has their answer\n- 37: route this matter to the individual empowered to decide\n- 289: be parked until a verification has been logged\n- 4347: terminate the process as continuation is prohibited\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q11874ffded",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- ticket id: TCK-5718\n- customer: Jonas Brandt\n- free of safety incident reports: yes\n- claim amount hard limit: 1000.00\n- claim free of ombudsman cases: yes\n- item excluded by policy: no\n- claim involves a media inquiry: no\n- legal complaint filed: no\n- claim form filled in with the usual font: no\n- claim amount: 551.83\n- harmless greeting present in the message: yes\n- proof of purchase attached: no\n- item return received: yes",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if claim_amount is above claim_amount_hard_limit.\n2. ask_manager if item_return_received is false or item_excluded_by_policy is true or legal_complaint_filed is true or free_of_safety_incident_reports is false or claim_involves_a_media_inquiry is true.\n3. defer if proof_of_purchase_attached is false or claim_free_of_ombudsman_cases is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nWhich of the actions below is the right decision for this request?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "qdbfe3f161c",
  "kind": "yes/no",
  "text": "# request record\nticket_id                                | TCK-6842\ncustomer                                 | Sana Ferreira\nclaim_free_of_ombudsman_cases            | true\nclaim_involves_a_media_inquiry           | false\nitem_return_received                     | false\nclaim_form_filled_in_with_the_usual_font | false\nfree_of_safety_incident_reports          | true\nclaim_amount                             | 100.00\nitem_excluded_by_policy                  | false\nclaim_amount_hard_limit                  | 100.00\nharmless_greeting_present_in_the_message | true\nfree_of_legal_complaints                 | true\nproof_of_purchase_attached               | true",
  "question": "Proposed action: defer\nIs it not the case that the facts behind this case back the proposed action and that it is not mistaken?",
  "definitions": "Meanings:\n- defer: pause this until the requester supplies the missing document\n- approve: let this be advanced exactly as originally specified\n- deny: be turned away and treated as off limits\n- ask manager: delegate the call to whoever holds authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q495b5446fe",
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
  "qid": "q76a32bb7ad",
  "kind": "yes/no",
  "text": "{\"request_id\": \"REQ-2898\", \"requester\": \"Ingrid Moreau\", \"legal_preservation_order_on_the_account\": false, \"request_grants_admin_rights\": true, \"access_days_approval_threshold\": 30, \"business_justification_provided\": true, \"account_suspended\": false, \"request_text_written_in_capital_letters\": false, \"requester_not_barred_from_this_system\": true, \"access_days\": 24, \"mfa_enrollment_complete\": true, \"requested_role_permitted_by_policy\": true, \"ethics_office_flagged_the_request\": false}",
  "question": "Proposed action: page oncall\nIs the proposed action the suitable determination for the request in the record?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qf34ddc7325",
  "kind": "choice",
  "text": "# request record\nrequest_id | REQ-3290\nrequester | Samir Calloway\nrequest_grants_admin_rights | false\naccess_days_approval_threshold | 90\nlegal_preservation_order_on_the_account | false\nmfa_enrollment_incomplete | false\naccount_suspended | false\nrequester_barred_from_this_system | false\nethics_office_flagged_the_request | true\naccess_days | 9\nbusiness_justification_provided | true\nrequested_role_forbidden_by_policy | false\nrequest_text_written_in_capital_letters | false",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "deny",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "q42872af066",
  "kind": "choice",
  "text": "{\n  \"case\":{\n    \"invoice_id\":\"INV-4435\",\n    \"vendor\":\"Stonebridge Works\"\n  },\n  \"values\":{\n    \"amount_approval_threshold\":25000.00,\n    \"amount\":25000.00\n  },\n  \"tests\":{\n    \"payment_requested_during_business_hours\":true,\n    \"approver_declared_a_conflict_of_interest\":false,\n    \"vendor_tax_form_on_file\":true,\n    \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n    \"vendor_name_written_in_capital_letters\":true,\n    \"vendor_on_sanctions_list\":false,\n    \"invoice_pdf_uses_a_landscape_layout\":false,\n    \"purchase_order_received\":true,\n    \"duplicate_of_paid_invoice\":false\n  }\n}",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "release",
   "cancel_order",
   "delay"
  ]
 },
 {
  "qid": "q2b930d0961",
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
  "qid": "qdfaea4ef83",
  "kind": "yes/no",
  "text": "{\n    \"request\": {\n        \"deploy_id\": \"DEP-6234\",\n        \"service\": \"mailer\"\n    },\n    \"figures\": {\n        \"files_changed\": 30,\n        \"files_changed_soft_limit\": 50\n    },\n    \"checks\": {\n        \"backout_plan_missing\": true,\n        \"service_free_of_major_incidents\": true,\n        \"deploy_has_a_long_description\": false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\": false,\n        \"canary_results_incomplete\": false,\n        \"rollout_approval_revoked\": true,\n        \"deploy_prohibited_during_the_audit_window\": false,\n        \"commit_messages_written_in_a_terse_style\": false,\n        \"deploy_blocked_by_security_policy\": false\n    }\n}",
  "question": "Proposed action: put on hold\nWould the proposed action be the appropriate response to the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if backout_plan_missing is true.\n2. turn down if rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is at least files_changed_soft_limit.\n3. send to a person if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_terse_style.\nMeanings:\n- put on hold: wait for the missing material to come in before deciding anything\n- turn down: veto this move and leave it there\n- go ahead: complete the action that was asked for\n- send to a person: transfer the case to the responsible decision maker for determination\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q217800fa6b",
  "kind": "yes/no",
  "text": "{\n  \"record\":{\n    \"request_id\":\"REQ-4526\",\n    \"requester\":\"دينا وائل الأنصاري\",\n    \"note\":\"الوصول المطلوب يتعارض مع فصل المهام المعتمد في المؤسسة.\"\n  },\n  \"numbers\":{\n    \"access_days_approval_threshold\":45,\n    \"access_days\":15\n  },\n  \"flags\":{\n    \"legal_preservation_order_on_the_account\":false,\n    \"mfa_enrollment_complete\":true,\n    \"requested_role_forbidden_by_policy\":false,\n    \"account_suspended\":false,\n    \"request_grants_admin_rights\":false,\n    \"business_justification_provided\":true,\n    \"request_free_of_ethics_office_flags\":true,\n    \"requester_barred_from_this_system\":false,\n    \"request_text_written_in_capital_letters\":false\n  }\n}",
  "question": "Proposed action: block_access\nDoes what we know about this rule out the proposed action?",
  "definitions": "Meanings:\n- quarantine: suspend progress until verification is received\n- allow: proceed with the task as asked\n- page_oncall: bring in the authority who can settle it for the requester\n- block_access: stop the work since it cannot move forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7f3ccff174",
  "kind": "choice",
  "text": "{\"deploy_id\":\"DEP-4602\",\"service\":\"mailer\",\"service_free_of_major_incidents\":true,\"contract_customer_asked_for_a_say_in_this_rollout\":false,\"commit_messages_written_in_a_terse_style\":false,\"deploy_blocked_by_security_policy\":false,\"files_changed_soft_limit\":15,\"deploy_prohibited_during_the_audit_window\":false,\"deploy_has_a_long_description\":true,\"backout_plan_missing\":false,\"files_changed\":1,\"rollout_approval_revoked\":false,\"canary_results_complete\":true}",
  "question": "The record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "turn down",
   "send to a person",
   "go ahead"
  ]
 },
 {
  "qid": "q28fda7883c",
  "kind": "yes/no",
  "text": "# case\nticket_id: TCK-6071\ncustomer: Leila Anand\nitem_excluded_by_policy: false\nclaim_free_of_ombudsman_cases: true\nfree_of_safety_incident_reports: true\nclaim_amount: 44.99\nclaim_involves_a_media_inquiry: false\nproof_of_purchase_missing: false\nharmless_greeting_present_in_the_message: true\nitem_return_received: true\nclaim_amount_hard_limit: 100.00\nlegal_complaint_filed: false\nclaim_form_filled_in_with_the_usual_font: true",
  "question": "Proposed action: deny\nQuick question: is the proposed action the right thing to do with this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. defer if proof_of_purchase_missing is true or claim_amount is at least claim_amount_hard_limit.\n3. deny if item_excluded_by_policy is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\nOtherwise: approve.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- approve: advance the task as stated without any blockers\n- defer: wait for the document to come through\n- ask manager: route this matter to the individual empowered to decide\n- deny: refuse the request because it crosses a clear line\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q13dd64cab5",
  "kind": "choice",
  "text": "{\"run_id\": \"RUN-5054\", \"agent\": \"helix\", \"owner_sign_off_required_for_this_action\": false, \"action_forbidden_by_security_policy\": false, \"action_free_of_ethics_concerns\": true, \"steps_used_hard_limit\": 60, \"task_description_incomplete\": false, \"tool_output_shows_tampering\": false, \"last_tool_output_unverified\": false, \"steps_used\": 18, \"log_lines_written_in_a_compact_style\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put_on_hold if task_description_incomplete is true or steps_used is above steps_used_hard_limit.\n3. send_to_a_person if action_forbidden_by_security_policy is true or owner_sign_off_required_for_this_action is true.\nOtherwise: go_ahead.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_compact_style.\nMeanings:\n- send_to_a_person: direct the request to the responsible decider\n- go_ahead: keep it moving forward\n- put_on_hold: hold the request so the requester waits for their check\n- turn_down: make sure the requester never gets what they wanted\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "put_on_hold",
   "send_to_a_person",
   "go_ahead"
  ]
 },
 {
  "qid": "qd89bb502ee",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-5682\n- requester: Mira Vasquez\n- requested role forbidden by policy: no\n- requester barred from this system: no\n- account suspended: no\n- request grants admin rights: no\n- mfa enrollment incomplete: no\n- ethics office flagged the request: no\n- business justification missing: no\n- legal preservation order on the account: no\n- access days: 7\n- request text written in capital letters: no\n- access days approval threshold: 14",
  "question": "Proposed action: approve\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. defer if requested_role_forbidden_by_policy is true.\n3. deny if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_missing, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8d5e4856bb",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"deploy_id\": \"DEP-3322\",\n        \"service\": \"ledger\"\n    },\n    \"values\": {\n        \"files_changed\": 2,\n        \"files_changed_soft_limit\": 10\n    },\n    \"tests\": {\n        \"contract_customer_asked_for_a_say_in_this_rollout\": true,\n        \"commit_messages_written_in_a_terse_style\": false,\n        \"deploy_has_a_long_description\": false,\n        \"service_free_of_major_incidents\": true,\n        \"canary_results_incomplete\": false,\n        \"deploy_prohibited_during_the_audit_window\": false,\n        \"backout_plan_documented\": true,\n        \"deploy_blocked_by_security_policy\": true,\n        \"rollout_approval_revoked\": false\n    }\n}",
  "question": "Proposed action: put_on_hold\nWould the proposed action be considered the correct disposition of the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if canary_results_incomplete is true.\n2. turn_down if rollout_approval_revoked is true.\n3. put_on_hold if backout_plan_documented is false or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\nOtherwise: go_ahead.\nNever counted: deploy_has_a_long_description, deploy_blocked_by_security_policy, service_free_of_major_incidents, contract_customer_asked_for_a_say_in_this_rollout, commit_messages_written_in_a_terse_style.\nMeanings:\n- turn_down: drop this right there, we are not touching it\n- put_on_hold: wait so the requester can supply more information first\n- go_ahead: execute the request exactly as written\n- send_to_a_person: toss it over to the one who makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q02d435c3ee",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-9431\n- vendor: Oakmont Partners\n- duplicate of paid invoice: no\n- approver declared a conflict of interest: yes\n- amount: 1345.40\n- vendor free of sanctions: yes\n- vendor name written in capital letters: no\n- payment requested during business hours: yes\n- invoice pdf uses a portrait layout: yes\n- amount approval threshold: 2500.00\n- awaiting purchase order: no\n- vendor filed a legal claim over this invoice: no\n- vendor tax form missing: yes",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. reject if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nLooking at this case file, which of the actions listed is the right call?",
  "options": [
   "escalate",
   "pay",
   "reject"
  ]
 },
 {
  "qid": "q7a3dbe2f23",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-8127\", \"vendor\": \"Riverbend Partners\", \"vendor_tax_form_on_file\": true, \"amount_approval_threshold\": 5000.00, \"amount\": 5000.00, \"invoice_pdf_uses_a_landscape_layout\": false, \"vendor_name_written_in_capital_letters\": false, \"approver_free_of_conflicts_of_interest\": true, \"duplicate_of_paid_invoice\": false, \"vendor_free_of_sanctions\": false, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"awaiting_purchase_order\": false, \"payment_requested_during_business_hours\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if approver_free_of_conflicts_of_interest is false.\n2. cancel_order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "cancel_order",
   "hand_to_a_person",
   "release"
  ]
 },
 {
  "qid": "q6a80ec872a",
  "kind": "choice",
  "text": "{\n    \"subject\":{\n        \"invoice_id\":\"INV-7941\",\n        \"vendor\":\"Lakeshore Supply\"\n    },\n    \"amounts\":{\n        \"amount\":2074.32,\n        \"amount_approval_threshold\":2500.00\n    },\n    \"checks\":{\n        \"vendor_name_written_in_capital_letters\":false,\n        \"approver_free_of_conflicts_of_interest\":true,\n        \"duplicate_of_paid_invoice\":true,\n        \"payment_requested_during_business_hours\":true,\n        \"purchase_order_received\":true,\n        \"invoice_pdf_uses_a_landscape_layout\":false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n        \"vendor_free_of_sanctions\":true,\n        \"vendor_tax_form_missing\":false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. reject if duplicate_of_paid_invoice is true.\n3. escalate if vendor_free_of_sanctions is false or approver_free_of_conflicts_of_interest is false or amount is at least amount_approval_threshold.\nOtherwise: pay.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- escalate: route the case to a decider so the requester knows the outcome\n- pay: allow the matter to be taken forward as planned\n- hold: pause this until the requester supplies the missing document\n- reject: skip this one, it is a hard pass for us\nThe record is complete: nothing else applies.\n\nMind telling me which of the actions below is the best call for this request?",
  "options": [
   "hold",
   "pay",
   "reject"
  ]
 },
 {
  "qid": "q204177ba00",
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
  "qid": "q56b8c303e6",
  "kind": "yes/no",
  "text": "# request record\nrequest_id = REQ-7564\nrequester = Jonas Okafor\nrequested_role_permitted_by_policy = true\nrequest_text_written_in_capital_letters = false\nbusiness_justification_provided = true\nrequest_grants_admin_rights = false\naccess_days = 1\nlegal_preservation_order_on_the_account = false\naccount_suspended = false\nethics_office_flagged_the_request = false\nmfa_enrollment_complete = true\naccess_days_approval_threshold = 7\nrequester_barred_from_this_system = false",
  "question": "Proposed action: pend\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q4157d31274",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n* deploy id: DEP-3535\n* service: pricing\n* commit messages written in a detailed style: yes\n* rollout approval revoked: no\n* files changed soft limit: 50\n* canary results incomplete: no\n* deploy prohibited during the audit window: no\n* files changed: 1\n* deploy has a long description: no\n* deploy blocked by security policy: no\n* backout plan missing: yes\n* service free of major incidents: yes\n* contract customer asked for a say in this rollout: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_missing is true or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed does the record best support for this request?",
  "options": [
   "go ahead",
   "turn down",
   "put on hold"
  ]
 },
 {
  "qid": "q68be77fe72",
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
  "qid": "q052df94a2b",
  "kind": "choice",
  "text": "# request record\ndeploy_id                                         | DEP-2693\nservice                                           | billing\ndeploy_prohibited_during_the_audit_window         | true\ncontract_customer_asked_for_a_say_in_this_rollout | false\nservice_free_of_major_incidents                   | true\nfiles_changed                                     | 13\nrollout_approval_revoked                          | false\ncanary_results_complete                           | true\nfiles_changed_soft_limit                          | 15\ndeploy_blocked_by_security_policy                 | false\ncommit_messages_written_in_a_terse_style          | false\ndeploy_has_a_long_description                     | false\nbackout_plan_documented                           | true",
  "question": "The record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "turn_down",
   "send_to_a_person",
   "go_ahead"
  ]
 },
 {
  "qid": "q01342d0db1",
  "kind": "choice",
  "text": "# extract\ninvoice_id | INV-5383\nvendor | Riverbend Partners\namount_approval_threshold | 500.00\nduplicate_of_paid_invoice | false\namount | 453.35\ninvoice_pdf_uses_a_landscape_layout | false\nvendor_name_written_in_capital_letters | false\nvendor_free_of_sanctions | true\nawaiting_purchase_order | false\nvendor_tax_form_missing | false\nvendor_filed_a_legal_claim_over_this_invoice | false\napprover_free_of_conflicts_of_interest | true\npayment_requested_during_business_hours | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand to a person if approver_free_of_conflicts_of_interest is false.\n2. cancel order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed under the record would the requester see as the right call?",
  "options": [
   "delay",
   "release",
   "cancel order"
  ]
 },
 {
  "qid": "q7999c34dc2",
  "kind": "yes/no",
  "text": "# extract\nticket_id=TCK-2153\ncustomer=زياد نبيل الدوسري\nnote=الحالة بسيطة ومكتملة ولا تحتاج إلى تدخل إضافي.\nclaim_form_filled_in_with_the_usual_font=true\nclaim_involves_a_media_inquiry=true\nclaim_free_of_ombudsman_cases=true\nfree_of_safety_incident_reports=true\nitem_excluded_by_policy=false\nharmless_greeting_present_in_the_message=false\nlegal_complaint_filed=false\nclaim_amount_hard_limit=200.00\nclaim_amount=153.76\nproof_of_purchase_missing=false\nitem_return_received=true",
  "question": "Proposed action: send_to_a_person\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if item_return_received is false or free_of_safety_incident_reports is false.\n2. put_on_hold if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. send_to_a_person if proof_of_purchase_missing is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: go_ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe658514a3a",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"run_id\": \"RUN-7525\",\n        \"agent\": \"beacon\"\n    },\n    \"metrics\": {\n        \"steps_used_hard_limit\": 8,\n        \"steps_used\": 2\n    },\n    \"signals\": {\n        \"owner_sign_off_required_for_this_action\": false,\n        \"task_description_complete\": true,\n        \"last_tool_output_verified\": true,\n        \"tool_output_shows_tampering\": false,\n        \"action_forbidden_by_security_policy\": false,\n        \"log_lines_written_in_a_verbose_style\": true,\n        \"action_free_of_ethics_concerns\": true\n    }\n}",
  "question": "Proposed action: put on hold\nWould what the record shows make the proposed action the right call here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if owner_sign_off_required_for_this_action is true.\n2. turn down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is above steps_used_hard_limit.\n3. put on hold if last_tool_output_verified is false.\nOtherwise: go ahead.\nNever counted: task_description_complete, action_free_of_ethics_concerns, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7eeb88beae",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  run_id: RUN-1750\n  agent: jasper\nnumbers:\n  steps_used_hard_limit: 40\n  steps_used: 40\nflags:\n  last_tool_output_verified: true\n  tool_output_shows_tampering: false\n  action_free_of_ethics_concerns: true\n  task_description_incomplete: false\n  action_forbidden_by_security_policy: false\n  log_lines_written_in_a_compact_style: true\n  owner_sign_off_required_for_this_action: false",
  "question": "Proposed action: go_ahead\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if action_free_of_ethics_concerns is false or owner_sign_off_required_for_this_action is true.\n2. put_on_hold if action_forbidden_by_security_policy is true.\n3. turn_down if tool_output_shows_tampering is true or steps_used is above steps_used_hard_limit.\nOtherwise: go_ahead.\nNever counted: last_tool_output_verified, task_description_incomplete, log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q79c893bb5d",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- ticket id: TCK-6941\n- customer: Elena Duarte\n- proof of purchase attached: yes\n- item excluded by policy: yes\n- free of legal complaints: yes\n- free of safety incident reports: yes\n- claim free of ombudsman cases: yes\n- claim involves a media inquiry: yes\n- harmless greeting present in the message: yes\n- claim amount hard limit: 50.00\n- item return not yet received: yes\n- claim form filled in with the usual font: yes\n- claim amount: 35.34",
  "question": "Proposed action: go_ahead\nIs the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if free_of_safety_incident_reports is false.\n2. turn_down if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. put_on_hold if item_return_not_yet_received is true.\nOtherwise: go_ahead.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4be14d3b1b",
  "kind": "yes/no",
  "text": "# record\nrequest_id=REQ-5355\nrequester=Anders Keller\nethics_office_flagged_the_request=false\nlegal_preservation_order_on_the_account=false\nmfa_enrollment_complete=true\nbusiness_justification_provided=true\nrequester_barred_from_this_system=false\naccount_suspended=true\nrequest_grants_admin_rights=false\nrequested_role_forbidden_by_policy=false\naccess_days_approval_threshold=14\naccess_days=19\nrequest_text_written_in_capital_letters=false",
  "question": "Proposed action: QDMF\nHas anything in the record ruled out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QDMF if business_justification_provided is false or mfa_enrollment_complete is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. PDR if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. DF if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: F.\nNever counted: ethics_office_flagged_the_request, request_text_written_in_capital_letters.\nMeanings:\n- DF: be handed over to the deciding person\n- F: proceed with the request since the way is clear and nothing blocks it\n- QDMF: stall the request until the check comes back\n- PDR: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3eed9c3687",
  "kind": "choice",
  "text": "# record\ninvoice_id=INV-8685\nvendor=Riverbend Works\nawaiting_purchase_order=false\ninvoice_pdf_uses_a_landscape_layout=false\nvendor_tax_form_on_file=true\nvendor_on_sanctions_list=false\namount_approval_threshold=10000.00\npayment_requested_during_business_hours=true\nvendor_name_written_in_capital_letters=false\nduplicate_of_paid_invoice=false\nvendor_filed_a_legal_claim_over_this_invoice=false\namount=10000.01\napprover_declared_a_conflict_of_interest=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if awaiting_purchase_order is true.\n2. send to a person if vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. turn down if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or approver_declared_a_conflict_of_interest is true or amount is above amount_approval_threshold.\nOtherwise: go ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below would be the appropriate determination for the request in question?",
  "options": [
   "send to a person",
   "go ahead",
   "turn down"
  ]
 },
 {
  "qid": "q61caca6e6b",
  "kind": "yes/no",
  "text": "deploy_id | DEP-8240\nservice | checkout\ndeploy_blocked_by_security_policy | false\ndeploy_has_a_long_description | false\ncanary_results_complete | true\nrollout_approval_revoked | false\ncommit_messages_written_in_a_detailed_style | true\ncontract_customer_asked_for_a_say_in_this_rollout | false\nbackout_plan_missing | false\nfiles_changed_soft_limit | 20\ndeploy_prohibited_during_the_audit_window | false\nservice_free_of_major_incidents | true\nfiles_changed | 20",
  "question": "Proposed action: go ahead\nOverall, would you say the proposed action suits the request in the record?",
  "definitions": "Meanings:\n- turn down: kill this one off\n- send to a person: get referred to the person who decides\n- put on hold: stall the request until the check comes back\n- go ahead: continue with what was requested\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3c4780a05b",
  "kind": "choice",
  "text": "# extract\nrun_id: RUN-8170\nagent: delta\naction_free_of_ethics_concerns: true\nsteps_used: 12\ntask_description_complete: true\naction_forbidden_by_security_policy: false\ntool_output_shows_tampering: false\nowner_sign_off_required_for_this_action: false\nlog_lines_written_in_a_compact_style: true\nsteps_used_hard_limit: 12\nlast_tool_output_verified: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put on hold if last_tool_output_verified is false or task_description_complete is false.\n3. turn down if action_forbidden_by_security_policy is true or owner_sign_off_required_for_this_action is true or steps_used is above steps_used_hard_limit.\nOtherwise: go ahead.\nNever counted: log_lines_written_in_a_compact_style.\nMeanings:\n- put on hold: keep it in limbo until the verification has been confirmed\n- send to a person: forward it to the decision maker\n- go ahead: go ahead and the requester will be served\n- turn down: be turned away and treated as off limits\nThe record is complete: nothing else applies.\n\nLooking at this case file, which of the actions listed is the right call?",
  "options": [
   "put on hold",
   "send to a person",
   "go ahead"
  ]
 },
 {
  "qid": "qb88260b28d",
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
  "qid": "qc0423c4daf",
  "kind": "choice",
  "text": "# record\nticket_id=TCK-8124\ncustomer=Nadia Adeyemi\nclaim_form_filled_in_with_the_usual_font=true\nclaim_amount=1000.00\nitem_return_not_yet_received=true\nfree_of_legal_complaints=true\nitem_excluded_by_policy=false\nclaim_free_of_ombudsman_cases=true\nclaim_involves_a_media_inquiry=false\nharmless_greeting_present_in_the_message=true\nproof_of_purchase_attached=true\nclaim_amount_hard_limit=1000.00\nfree_of_safety_incident_reports=true",
  "question": "Meanings:\n- ask_manager: be handed over to the deciding person\n- deny: refuse to act since the step is prohibited\n- approve: keep going exactly as requested because every obstacle has cleared\n- defer: withhold action until supporting information is supplied\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q1785554eb4",
  "kind": "choice",
  "text": "---\nrequest_id: REQ-9731\nrequester: Kofi Adeyemi\nethics_office_flagged_the_request: false\nbusiness_justification_provided: true\naccess_days: 36\nrequest_grants_admin_rights: false\naccess_days_approval_threshold: 30\naccount_suspended: true\nmfa_enrollment_complete: true\nlegal_preservation_order_on_the_account: false\nrequester_barred_from_this_system: false\nrequest_text_written_in_capital_letters: false\nrequested_role_permitted_by_policy: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. block_access if account_suspended is true or requested_role_permitted_by_policy is false or request_grants_admin_rights is true.\n2. page_oncall if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. quarantine if business_justification_provided is false or mfa_enrollment_complete is false or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- quarantine: be kept on hold until more information is supplied\n- allow: complete the job as it was assigned\n- block_access: veto this move and leave it there\n- page_oncall: transfer the case to the responsible decision maker for determination\nThe record is complete: nothing else applies.\n\nBased on what the record shows, which of the actions listed is the right call?",
  "options": [
   "quarantine",
   "page_oncall",
   "block_access"
  ]
 },
 {
  "qid": "q74d14ccdb1",
  "kind": "choice",
  "text": "---\nmeta:\n  ticket_id: \"TCK-9071\"\n  customer: \"تغريد صبحي المهيري\"\n  note: \"المستندات المرفقة صحيحة ولا تحتاج إلى مراجعة إضافية.\"\nmetrics:\n  claim_amount: 94.57\n  claim_amount_hard_limit: 100.00\nsignals:\n  claim_free_of_ombudsman_cases: true\n  legal_complaint_filed: false\n  claim_form_filled_in_with_the_usual_font: true\n  free_of_safety_incident_reports: true\n  claim_involves_a_media_inquiry: false\n  item_excluded_by_policy: true\n  harmless_greeting_present_in_the_message: true\n  proof_of_purchase_attached: true\n  item_return_not_yet_received: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if claim_amount is at least claim_amount_hard_limit.\n2. ask_manager if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. defer if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: approve.\nNever counted: item_return_not_yet_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nWhich of the actions below answers the request given the facts you can see?",
  "options": [
   "approve",
   "ask_manager",
   "defer"
  ]
 },
 {
  "qid": "q3b0f7e5c3b",
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
  "qid": "q2cb873ac2f",
  "kind": "yes/no",
  "text": "---\n# record\nrun_id: \"RUN-1245\"\nagent: \"garnet\"\nlog_lines_written_in_a_compact_style: false\nlast_tool_output_verified: true\naction_forbidden_by_security_policy: false\ntask_description_complete: true\nsteps_used_hard_limit: 16\nsteps_used: 15\ntool_output_shows_tampering: false\naction_free_of_ethics_concerns: true\nowner_sign_off_required_for_this_action: false",
  "question": "Proposed action: 695\nIs it not correct that the proposed action is not off base, judging by the record on file?",
  "definitions": "Meanings:\n- 94: hold off until more information arrives\n- 5: escalate this to someone senior who decides\n- 695: push ahead as planned\n- 5136: send the requester away with the request left unfinished\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q228715d8e9",
  "kind": "choice",
  "text": "---\nrequest:\n  ticket_id: TCK-5505\n  customer: وفاء محسن الفارس\n  note: تم التحقق من الهوية وكل ما يتعلق بالطلب سليم.\nfigures:\n  claim_amount: 185.03\n  claim_amount_hard_limit: 200.00\nchecks:\n  legal_complaint_filed: true\n  claim_involves_a_media_inquiry: false\n  free_of_safety_incident_reports: false\n  claim_form_filled_in_with_the_usual_font: true\n  item_return_received: true\n  harmless_greeting_present_in_the_message: false\n  proof_of_purchase_attached: true\n  item_excluded_by_policy: false\n  claim_free_of_ombudsman_cases: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. put_on_hold if proof_of_purchase_attached is false or claim_amount is at least claim_amount_hard_limit.\n3. turn_down if item_excluded_by_policy is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\nOtherwise: go_ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "put_on_hold",
   "turn_down",
   "go_ahead"
  ]
 },
 {
  "qid": "qe54b7c2789",
  "kind": "yes/no",
  "text": "{\"request_id\": \"REQ-7454\", \"requester\": \"Idris Calloway\", \"access_days_approval_threshold\": 90, \"request_free_of_ethics_office_flags\": true, \"access_days\": 45, \"mfa_enrollment_complete\": false, \"requested_role_forbidden_by_policy\": false, \"requester_barred_from_this_system\": false, \"request_text_written_in_capital_letters\": false, \"account_suspended\": false, \"request_grants_admin_rights\": false, \"business_justification_missing\": false, \"legal_preservation_order_on_the_account\": false}",
  "question": "Proposed action: refer_to_owner\nWould the proposed action be the right move for the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer_to_owner if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n2. pend if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_complete is false or account_suspended is true.\nOtherwise: grant.\nNever counted: business_justification_missing, requester_barred_from_this_system, request_text_written_in_capital_letters.\nMeanings:\n- refer_to_owner: direct the request to the responsible decider\n- pend: keep their request on hold until more information arrives from them\n- grant: carry it through and the requester is satisfied\n- refuse: halt the request at this point\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0a457259d0",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- deploy id: DEP-3929\n- service: billing\n- backout plan documented: yes\n- files changed soft limit: 20\n- deploy blocked by security policy: no\n- commit messages written in a terse style: no\n- files changed: 2\n- deploy has a long description: no\n- rollout approval revoked: no\n- deploy prohibited during the audit window: yes\n- service free of major incidents: yes\n- canary results incomplete: no\n- contract customer asked for a say in this rollout: no",
  "question": "The record is complete: nothing else applies.\n\nWhich listed action is the best call for the request?",
  "options": [
   "put_on_hold",
   "send_to_a_person",
   "turn_down"
  ]
 },
 {
  "qid": "q68b1b25cf2",
  "kind": "yes/no",
  "text": "# record\nrun_id | RUN-7915\nagent | atlas\naction_permitted_by_security_policy | true\nowner_sign_off_required_for_this_action | false\nlast_tool_output_verified | true\nsteps_used | 12\nsteps_used_hard_limit | 12\naction_free_of_ethics_concerns | true\ntask_description_complete | false\nlog_lines_written_in_a_verbose_style | false\ntool_output_shows_tampering | false",
  "question": "Proposed action: 9\nIs it not true that the proposed action is not out of step with what is needed?",
  "definitions": "Meanings:\n- 76: hand this off because a decider has to choose\n- 198: finish it so the requester has their answer\n- 9: decline the request as the action is prohibited\n- 1083: hold this until a check comes back\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q19621e4b6d",
  "kind": "yes/no",
  "text": "{\n  \"run_id\":\"RUN-8041\",\n  \"agent\":\"atlas\",\n  \"action_permitted_by_security_policy\":true,\n  \"owner_sign_off_required_for_this_action\":false,\n  \"tool_output_shows_tampering\":false,\n  \"action_free_of_ethics_concerns\":true,\n  \"steps_used_hard_limit\":40,\n  \"last_tool_output_unverified\":false,\n  \"steps_used\":24,\n  \"log_lines_written_in_a_verbose_style\":false,\n  \"task_description_incomplete\":true\n}",
  "question": "Proposed action: RH\nIs it not so that the proposed action, looked at fresh, is not a bad call for the job?",
  "definitions": "Meanings:\n- MVRS: get the boss to make the final call\n- RH: await further verification before any progression\n- M: be stopped and never carried out\n- QKF: go ahead and the requester will be served\nThe record is complete: nothing else applies."
 }
]
