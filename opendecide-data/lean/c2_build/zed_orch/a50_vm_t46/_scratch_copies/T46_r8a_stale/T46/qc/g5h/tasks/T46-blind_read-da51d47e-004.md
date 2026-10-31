# G5-H blind read T46-blind_read-da51d47e-004 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8a/T46/qc/g5h/answers/T46-blind_read-da51d47e-004.json

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
  "qid": "qa46bef625c",
  "kind": "yes/no",
  "text": "{\n  \"ticket_id\":\"TCK-8857\",\n  \"customer\":\"Anders Haddad\",\n  \"legal_complaint_filed\":true,\n  \"item_excluded_by_policy\":false,\n  \"customer_message_written_in_a_casual_tone\":true,\n  \"item_return_received\":true,\n  \"claim_involves_a_media_inquiry\":false,\n  \"harmless_greeting_present_in_the_message\":true,\n  \"free_of_safety_incident_reports\":true,\n  \"claim_form_filled_in_with_the_usual_font\":true,\n  \"customer_message_is_short\":false,\n  \"claim_amount\":27.17,\n  \"claim_amount_hard_limit\":100.00,\n  \"proof_of_purchase_missing\":true,\n  \"claim_free_of_ombudsman_cases\":true\n}",
  "question": "Proposed action: turn down\nFrom an audit standpoint, have the facts in the record ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. turn down if item_excluded_by_policy is true or legal_complaint_filed is true or claim_amount is above claim_amount_hard_limit.\n3. send to a person if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: go ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
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
  "qid": "q715ad2d49e",
  "kind": "choice",
  "text": "# request record\nrun_id: RUN-4930\nagent: fjord\nsteps_used_hard_limit: 8\ntool_output_shows_tampering: false\nlast_tool_output_verified: false\naction_free_of_ethics_concerns: true\nowner_sign_off_required_for_this_action: false\ntask_description_complete: false\naction_forbidden_by_security_policy: false\nsteps_used: 3\nlog_lines_written_in_a_verbose_style: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if owner_sign_off_required_for_this_action is true.\n2. cancel if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is above steps_used_hard_limit.\n3. wait if last_tool_output_verified is false.\nOtherwise: proceed.\nNever counted: task_description_complete, action_free_of_ethics_concerns, log_lines_written_in_a_verbose_style.\nMeanings:\n- cancel: shut this down fast\n- wait: sit on it till the doc shows up\n- proceed: carry out the request as written\n- ask_a_human: route it elsewhere because a decider must weigh in\nThe record is complete: nothing else applies.\n\nThe request describes a situation; which of the actions underneath handles it correctly?",
  "options": [
   "ask_a_human",
   "cancel",
   "wait"
  ]
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
  "qid": "q2fb6a5722f",
  "kind": "choice",
  "text": "ticket_id: TCK-5437\ncustomer: Ingrid Lindqvist\nproof_of_purchase_missing: true\nfree_of_legal_complaints: true\nitem_return_received: true\nharmless_greeting_present_in_the_message: true\nclaim_form_filled_in_with_the_usual_font: true\nitem_excluded_by_policy: false\nclaim_amount_hard_limit: 1000.00\nclaim_involves_a_media_inquiry: false\nclaim_free_of_ombudsman_cases: true\ncustomer_message_written_in_a_casual_tone: false\ncustomer_message_is_short: true\nfree_of_safety_incident_reports: true\nclaim_amount: 968.76",
  "question": "The record is complete: nothing else applies.\n\nAs the manager, which of the actions listed is the right call for this request?",
  "options": [
   "cancel",
   "proceed",
   "wait"
  ]
 },
 {
  "qid": "q184ddcc688",
  "kind": "yes/no",
  "text": "{\n  \"ticket_id\":\"TCK-8352\",\n  \"customer\":\"Nadia Imai\",\n  \"harmless_greeting_present_in_the_message\":true,\n  \"claim_involves_a_media_inquiry\":false,\n  \"claim_amount_hard_limit\":500.00,\n  \"item_excluded_by_policy\":false,\n  \"claim_free_of_ombudsman_cases\":true,\n  \"free_of_safety_incident_reports\":true,\n  \"item_return_not_yet_received\":false,\n  \"proof_of_purchase_missing\":false,\n  \"claim_form_filled_in_with_the_usual_font\":true,\n  \"customer_message_is_short\":true,\n  \"customer_message_written_in_a_casual_tone\":true,\n  \"legal_complaint_filed\":false,\n  \"claim_amount\":378.96\n}",
  "question": "Proposed action: ask_a_human\nIs it not the case that the proposed action is what the request and facts call for, and is not a poor choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if claim_amount is above claim_amount_hard_limit.\n2. ask_a_human if item_return_not_yet_received is true or item_excluded_by_policy is true or legal_complaint_filed is true or free_of_safety_incident_reports is false or claim_involves_a_media_inquiry is true.\n3. delay if proof_of_purchase_missing is true or claim_free_of_ombudsman_cases is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- refuse: bin this idea and keep it out of the flow\n- approve: proceed with the task as asked\n- delay: wait for the document to come through\n- ask_a_human: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc8b595a294",
  "kind": "yes/no",
  "text": "---\n# record\nrun_id: RUN-5515\nagent: ember\ntask_description_complete: true\ntool_output_shows_tampering: false\nsteps_used: 11\nsteps_used_hard_limit: 30\nlast_tool_output_unverified: false\naction_free_of_ethics_concerns: true\nowner_sign_off_required_for_this_action: false\naction_permitted_by_security_policy: false\nlog_lines_written_in_a_verbose_style: false",
  "question": "Proposed action: human review\nDoes the record's evidence rule out the proposed action as the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. human review if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. pause if last_tool_output_unverified is true or task_description_complete is false.\n3. stop if action_permitted_by_security_policy is false or owner_sign_off_required_for_this_action is true or steps_used is above steps_used_hard_limit.\nOtherwise: continue.\nNever counted: log_lines_written_in_a_verbose_style.\nMeanings:\n- continue: carry on with it now\n- stop: stop the work since it cannot move forward\n- pause: keep it in limbo until the verification has been confirmed\n- human review: transfer it to the person with authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q66b0ec4b7a",
  "kind": "choice",
  "text": "{\n    \"record\": {\n        \"request_id\": \"REQ-8373\",\n        \"requester\": \"Zoe Okafor\"\n    },\n    \"numbers\": {\n        \"access_days\": 61,\n        \"access_days_approval_threshold\": 45\n    },\n    \"flags\": {\n        \"account_suspended\": false,\n        \"request_text_written_in_capital_letters\": false,\n        \"legal_preservation_order_on_the_account\": false,\n        \"requested_role_forbidden_by_policy\": false,\n        \"mfa_enrollment_complete\": true,\n        \"request_grants_admin_rights\": false,\n        \"requester_barred_from_this_system\": false,\n        \"request_free_of_ethics_office_flags\": true,\n        \"business_justification_missing\": false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. FNJ if account_suspended is true or requested_role_forbidden_by_policy is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n2. ZG if request_grants_admin_rights is true or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n3. KDLN if business_justification_missing is true or mfa_enrollment_complete is false.\nOtherwise: R.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- ZG: send the requester away with the request left unfinished\n- FNJ: transfer the case to the responsible decision maker for determination\n- KDLN: park the file until the requester sends the document in\n- R: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies.\n\nTaking the facts of the request into account, which action listed should be picked?",
  "options": [
   "ZG",
   "FNJ",
   "R"
  ]
 },
 {
  "qid": "q3fd1631dd5",
  "kind": "choice",
  "text": "---\n# request record\nrecord:\n    invoice_id: \"INV-4359\"\n    vendor: \"Harbor Logistics\"\nnumbers:\n    amount: 500.00\n    amount_approval_threshold: 500.00\nflags:\n    awaiting_purchase_order: false\n    invoice_pdf_uses_a_portrait_layout: true\n    vendor_tax_form_missing: false\n    approver_declared_a_conflict_of_interest: false\n    vendor_on_sanctions_list: true\n    vendor_filed_a_legal_claim_over_this_invoice: false\n    payment_requested_during_business_hours: true\n    duplicate_of_paid_invoice: false\n    vendor_name_written_in_capital_letters: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 1735 if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. 8 if vendor_on_sanctions_list is true.\n3. 79 if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: 626.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- 8: end it so the requester sees their request closed\n- 79: bring in the owner who can rule on this\n- 1735: hold all progress until the requisite documentation arrives\n- 626: allow the matter to be taken forward as planned\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "79",
   "8",
   "626"
  ]
 },
 {
  "qid": "q0f25bfdfc5",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"leave_id\": \"LVE-8049\",\n        \"employee\": \"Anders Novak\"\n    },\n    \"metrics\": {\n        \"leave_days_soft_limit\": 7,\n        \"leave_days\": 2\n    },\n    \"signals\": {\n        \"union_grievance_raised_over_this_leave\": true,\n        \"team_coverage_arranged\": true,\n        \"leave_balance_available\": true,\n        \"leave_request_written_in_a_formal_tone\": true,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"notice_period_met\": true,\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"request_falls_in_blackout_period\": false\n    }\n}",
  "question": "Proposed action: turn_down\nIs it not correct that the proposed action is not off base, judging by the record on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if notice_period_met is false or team_coverage_arranged is false or leave_balance_available is false or lawyer_letter_received_about_this_leave is true or leave_days is above leave_days_soft_limit.\n2. turn_down if request_falls_in_blackout_period is true.\n3. send_to_a_person if medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false.\nOtherwise: go_ahead.\nNever counted: union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9d26cbac89",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- request id: REQ-7080\n- requester: Elena Quispe\n- mfa enrollment complete: no\n- requested role forbidden by policy: no\n- access days: 19\n- request grants admin rights: no\n- legal preservation order on the account: no\n- business justification provided: yes\n- request text written in capital letters: no\n- access days approval threshold: 60\n- account suspended: no\n- ethics office flagged the request: yes\n- requester barred from this system: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer to owner if request_grants_admin_rights is true or ethics_office_flagged_the_request is true or access_days is at least access_days_approval_threshold.\n2. pend if mfa_enrollment_complete is false.\n3. refuse if business_justification_provided is false or account_suspended is true or requested_role_forbidden_by_policy is true or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\nOtherwise: grant.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- grant: proceed with the request since the way is clear and nothing blocks it\n- pend: hold the request until a check is completed\n- refer to owner: be forwarded to the person in charge\n- refuse: refuse this request entirely\nThe record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "refer to owner",
   "grant",
   "pend"
  ]
 },
 {
  "qid": "q4e4862a49a",
  "kind": "yes/no",
  "text": "{\n    \"record\":{\n        \"deploy_id\":\"DEP-7513\",\n        \"service\":\"auth_proxy\"\n    },\n    \"numbers\":{\n        \"files_changed\":39,\n        \"files_changed_soft_limit\":80\n    },\n    \"flags\":{\n        \"deploy_prohibited_during_the_audit_window\":true,\n        \"deploy_blocked_by_security_policy\":false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\":false,\n        \"canary_results_complete\":true,\n        \"service_free_of_major_incidents\":true,\n        \"rollout_approval_revoked\":true,\n        \"deploy_has_a_long_description\":false,\n        \"deploy_title_written_in_normal_case\":true,\n        \"commit_messages_written_in_a_detailed_style\":true,\n        \"commit_messages_written_in_a_casual_tone\":true,\n        \"backout_plan_documented\":true\n    }\n}",
  "question": "Proposed action: turn down\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if canary_results_complete is false.\n2. turn down if rollout_approval_revoked is true.\n3. put on hold if backout_plan_documented is false or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\nOtherwise: go ahead.\nNever counted: deploy_has_a_long_description, deploy_blocked_by_security_policy, service_free_of_major_incidents, contract_customer_asked_for_a_say_in_this_rollout, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- turn down: shut this down right away, we are staying clear of it\n- send to a person: hand this over to whoever has the final say\n- put on hold: chill until the document turns up\n- go ahead: proceed and the requester gets what they asked\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc9f6c86640",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n    request_id: REQ-4731\n    requester: Hugo Tanaka\namounts:\n    access_days_approval_threshold: 14\n    access_days: 14\nchecks:\n    legal_preservation_order_on_the_account: false\n    account_suspended: true\n    requested_role_permitted_by_policy: true\n    request_grants_admin_rights: false\n    business_justification_provided: true\n    mfa_enrollment_incomplete: false\n    request_free_of_ethics_office_flags: true\n    requester_barred_from_this_system: false\n    request_text_written_in_capital_letters: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n2. delay if requested_role_permitted_by_policy is false.\n3. refuse if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_provided, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions below does the record point to as the right call?",
  "options": [
   "approve",
   "ask_a_human",
   "refuse"
  ]
 },
 {
  "qid": "qfff94d2340",
  "kind": "yes/no",
  "text": "---\n# record\nticket_id: \"TCK-9835\"\ncustomer: \"Ingrid Novak\"\nitem_return_received: true\nclaim_form_filled_in_with_the_usual_font: true\nharmless_greeting_present_in_the_message: true\nclaim_involves_a_media_inquiry: false\nitem_excluded_by_policy: false\nproof_of_purchase_missing: true\ncustomer_message_written_in_a_formal_tone: false\nfree_of_safety_incident_reports: true\nclaim_amount_hard_limit: 200.00\nlegal_complaint_filed: true\ncustomer_message_is_short: true\nclaim_amount: 126.47\nclaim_free_of_ombudsman_cases: true",
  "question": "Proposed action: wait\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. wait if proof_of_purchase_missing is true or claim_amount is at least claim_amount_hard_limit.\n3. cancel if item_excluded_by_policy is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\nOtherwise: proceed.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q64f825deff",
  "kind": "choice",
  "text": "{\n  \"ticket_id\": \"TCK-6179\",\n  \"customer\": \"Sana Mensah\",\n  \"harmless_greeting_present_in_the_message\": false,\n  \"item_excluded_by_policy\": false,\n  \"proof_of_purchase_attached\": false,\n  \"customer_message_is_short\": true,\n  \"claim_amount\": 200.00,\n  \"claim_amount_hard_limit\": 200.00,\n  \"customer_message_written_in_a_casual_tone\": true,\n  \"item_return_received\": true,\n  \"legal_complaint_filed\": false,\n  \"claim_involves_a_media_inquiry\": false,\n  \"free_of_safety_incident_reports\": true,\n  \"claim_free_of_ombudsman_cases\": true,\n  \"claim_form_filled_in_with_the_usual_font\": true\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. delay if proof_of_purchase_attached is false or claim_involves_a_media_inquiry is true.\n3. ask a human if item_return_received is false or legal_complaint_filed is true or free_of_safety_incident_reports is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- ask a human: hand this off because a decider has to choose\n- delay: hold the request so the requester waits for their check\n- approve: let this be advanced exactly as originally specified\n- refuse: toss it out, we are never doing this\nThe record is complete: nothing else applies.\n\nFrom the actions listed, what should be done with this request?",
  "options": [
   "approve",
   "delay",
   "ask a human"
  ]
 },
 {
  "qid": "qe39e233389",
  "kind": "yes/no",
  "text": "leave_id | LVE-9441\nemployee | عادل فؤاد النابلسي\nnote | المدير المباشر وافق على الطلب مسبقاً.\nrequests_team_free_of_harassment_complaints | true\nnotice_period_not_met | false\nleave_days | 7\nunion_grievance_raised_over_this_leave | false\nmedical_certificate_contested | false\nleave_request_written_in_a_formal_tone | false\nteam_coverage_arranged | true\nlawyer_letter_received_about_this_leave | false\nleave_days_soft_limit | 7\nrequest_falls_in_blackout_period | false\nleave_balance_available | false",
  "question": "Proposed action: PXS\nLooking at what the record says, is the proposed action a good fit for the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. T if notice_period_not_met is true or team_coverage_arranged is false or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. VSFG if medical_certificate_contested is true.\n3. HM if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: PXS.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- T: hold all progress until the requisite documentation arrives\n- VSFG: reject the request in full\n- PXS: run the requested step through\n- HM: get the boss to make the final call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa09275bfd4",
  "kind": "yes/no",
  "text": "---\n# request record\nsubject:\n  deploy_id: \"DEP-1264\"\n  service: \"auth_proxy\"\namounts:\n  files_changed: 10\n  files_changed_soft_limit: 15\nchecks:\n  commit_messages_written_in_a_detailed_style: false\n  deploy_title_written_in_normal_case: true\n  deploy_prohibited_during_the_audit_window: false\n  backout_plan_documented: true\n  deploy_blocked_by_security_policy: true\n  rollout_approval_revoked: true\n  deploy_has_a_long_description: false\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  commit_messages_written_in_a_casual_tone: true\n  canary_results_complete: false\n  service_free_of_major_incidents: true",
  "question": "Proposed action: wait\nBe honest, do the facts here rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. cancel if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. wait if canary_results_complete is false.\nOtherwise: proceed.\nNever counted: backout_plan_documented, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- wait: be kept on hold until more information is supplied\n- cancel: scrap the plan and drop this request\n- proceed: let this be advanced exactly as originally specified\n- ask_a_human: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7acdf57d21",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- request id: REQ-5354\n- requester: Mira Ferreira\n- mfa enrollment complete: yes\n- request grants admin rights: no\n- access days approval threshold: 7\n- legal preservation order on the account: no\n- account suspended: no\n- ethics office flagged the request: no\n- business justification provided: yes\n- access days: 1\n- requested role forbidden by policy: no\n- requester barred from this system: yes\n- request text written in capital letters: no",
  "question": "Meanings:\n- 6: keep going with it\n- 184: route the case to a decider so the requester knows the outcome\n- 3083: be parked until a verification has been logged\n- 51: halt the request at this point\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "3083",
   "6",
   "51"
  ]
 },
 {
  "qid": "q12290a0a31",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n  request_id: REQ-9651\n  requester: Leila Ferreira\nvalues:\n  access_days: 42\n  access_days_approval_threshold: 45\ntests:\n  business_justification_missing: false\n  requested_role_permitted_by_policy: true\n  requester_barred_from_this_system: false\n  legal_preservation_order_on_the_account: false\n  mfa_enrollment_incomplete: false\n  request_free_of_ethics_office_flags: true\n  request_text_written_in_capital_letters: false\n  account_suspended: false\n  request_grants_admin_rights: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 8 if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. 4997 if account_suspended is true or requested_role_permitted_by_policy is false.\n3. 872 if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: 31.\nNever counted: request_free_of_ethics_office_flags, request_text_written_in_capital_letters.\nMeanings:\n- 4997: send the requester away with the request left unfinished\n- 31: just crack on with it there is nothing in the way\n- 872: refer this item to the person who holds decision authority\n- 8: hold off until the check clears\nThe record is complete: nothing else applies.\n\nAs an auditor, which of the listed actions is the correct call for this request?",
  "options": [
   "31",
   "872",
   "8"
  ]
 },
 {
  "qid": "qc29d370f20",
  "kind": "choice",
  "text": "# record\ninvoice_id=INV-9078\nvendor=Ironleaf Logistics\nawaiting_purchase_order=false\namount=18301.22\ninvoice_pdf_uses_a_landscape_layout=false\nduplicate_of_paid_invoice=true\namount_approval_threshold=25000.00\napprover_free_of_conflicts_of_interest=true\nvendor_tax_form_missing=false\nvendor_on_sanctions_list=true\nvendor_filed_a_legal_claim_over_this_invoice=false\npayment_requested_during_business_hours=false\nvendor_name_written_in_capital_letters=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. VZFM if vendor_filed_a_legal_claim_over_this_invoice is true or approver_free_of_conflicts_of_interest is false or amount is at least amount_approval_threshold.\n2. PF if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n3. K if duplicate_of_paid_invoice is true.\nOtherwise: XVL.\nNever counted: vendor_on_sanctions_list, payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- PF: suspend action until the facts are confirmed\n- K: make sure the requester never gets what they wanted\n- XVL: complete the job as it was assigned\n- VZFM: send it up to the person who makes the call\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "XVL",
   "PF",
   "K"
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
  "qid": "qb3f81a8656",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-5682\n- requester: Mira Vasquez\n- requested role forbidden by policy: no\n- requester barred from this system: no\n- account suspended: no\n- request grants admin rights: no\n- mfa enrollment incomplete: yes\n- ethics office flagged the request: no\n- business justification missing: no\n- legal preservation order on the account: no\n- access days: 7\n- request text written in capital letters: no\n- access days approval threshold: 14",
  "question": "Proposed action: approve\nAs an auditor, do the facts in the record rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. delay if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_missing, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf44ac99529",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-8460\nvendor | Copperfield Systems\nduplicate_of_paid_invoice | false\nvendor_name_written_in_capital_letters | false\napprover_declared_a_conflict_of_interest | false\npurchase_order_received | true\namount | 1963.33\ninvoice_pdf_uses_a_landscape_layout | false\nvendor_tax_form_missing | false\npayment_requested_during_business_hours | true\nvendor_filed_a_legal_claim_over_this_invoice | true\nvendor_free_of_sanctions | true\namount_approval_threshold | 2500.00",
  "question": "Proposed action: 199\nQuick check: do the facts in the record rule out the proposed action here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 43 if purchase_order_received is false or vendor_tax_form_missing is true.\n2. 1799 if vendor_free_of_sanctions is false.\n3. 199 if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: 5.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- 1799: make sure the requester never gets what they wanted\n- 199: send this on to whoever decides\n- 43: hold all progress until the requisite documentation arrives\n- 5: execute the request exactly as written\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5a453f6d9f",
  "kind": "choice",
  "text": "run_id: RUN-6037\nagent: jasper\nlog_lines_written_in_a_verbose_style: false\nlast_tool_output_verified: true\naction_free_of_ethics_concerns: true\naction_forbidden_by_security_policy: true\nowner_sign_off_required_for_this_action: false\ntool_output_shows_tampering: false\nsteps_used: 3\nsteps_used_hard_limit: 16\ntask_description_complete: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if owner_sign_off_required_for_this_action is true.\n2. cancel if action_forbidden_by_security_policy is true.\n3. wait if last_tool_output_verified is false or task_description_complete is false or action_free_of_ethics_concerns is false or steps_used is above steps_used_hard_limit.\nOtherwise: proceed.\nNever counted: tool_output_shows_tampering, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "wait",
   "proceed",
   "cancel"
  ]
 },
 {
  "qid": "q8a8984e0e1",
  "kind": "choice",
  "text": "---\n# record\nleave_id: \"LVE-4935\"\nemployee: \"Yara Lindqvist\"\nnotice_period_met: true\nleave_balance_available: true\nteam_coverage_arranged: true\nrequests_team_free_of_harassment_complaints: true\nunion_grievance_raised_over_this_leave: false\nlawyer_letter_received_about_this_leave: false\nleave_days_soft_limit: 7\nrequest_falls_in_blackout_period: false\nleave_request_written_in_a_formal_tone: false\nleave_days: 3\nmedical_certificate_contested: true",
  "question": "Meanings:\n- delay: withhold action until supporting information is supplied\n- approve: keep going exactly as requested because every obstacle has cleared\n- ask_a_human: be passed along to whoever makes the call\n- refuse: block it right away\nThe record is complete: nothing else applies.\n\nChecklist item: which of the actions listed below is the right call for the request?",
  "options": [
   "ask_a_human",
   "delay",
   "approve"
  ]
 },
 {
  "qid": "q8010128fed",
  "kind": "choice",
  "text": "# record\nleave_id | LVE-9814\nemployee | Priya Okonkwo\nrequests_team_free_of_harassment_complaints | true\nleave_days_soft_limit | 5\nleave_days | 3\nteam_coverage_not_arranged | false\nlawyer_letter_received_about_this_leave | false\nrequest_falls_in_blackout_period | false\nleave_balance_available | true\nunion_grievance_raised_over_this_leave | false\nmedical_certificate_contested | false\nnotice_period_met | true\nleave_request_written_in_a_formal_tone | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if team_coverage_not_arranged is true or medical_certificate_contested is true or leave_days is above leave_days_soft_limit.\n2. deny if request_falls_in_blackout_period is true or lawyer_letter_received_about_this_leave is true.\n3. ask_manager if union_grievance_raised_over_this_leave is true.\nOtherwise: approve.\nNever counted: notice_period_met, leave_balance_available, requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nThe record shows the situation; which of the actions listed is the right call?",
  "options": [
   "defer",
   "approve",
   "deny"
  ]
 },
 {
  "qid": "q651d2ca781",
  "kind": "choice",
  "text": "deploy_id: DEP-3043\nservice: reports\nbackout_plan_missing: false\ncommit_messages_written_in_a_casual_tone: true\ndeploy_has_a_long_description: false\ncommit_messages_written_in_a_terse_style: false\nfiles_changed: 8\nrollout_approval_revoked: false\ncanary_results_complete: true\ndeploy_blocked_by_security_policy: true\ndeploy_prohibited_during_the_audit_window: false\nfiles_changed_soft_limit: 30\ndeploy_title_written_in_normal_case: true\ncontract_customer_asked_for_a_say_in_this_rollout: true\nservice_free_of_major_incidents: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QRH if backout_plan_missing is true or files_changed is above files_changed_soft_limit.\n2. PW if deploy_blocked_by_security_policy is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true.\n3. SMJT if service_free_of_major_incidents is false or contract_customer_asked_for_a_say_in_this_rollout is true.\nOtherwise: G.\nNever counted: canary_results_complete, deploy_has_a_long_description, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- QRH: be left pending until the review has been finished\n- G: go on and finish it\n- PW: drop it right away\n- SMJT: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies.\n\nWhich of the actions listed under the record would the requester see as the right call?",
  "options": [
   "G",
   "PW",
   "SMJT"
  ]
 },
 {
  "qid": "q6851a35180",
  "kind": "choice",
  "text": "{\n    \"subject\":{\n        \"ticket_id\":\"TCK-1254\",\n        \"customer\":\"Samir Petrov\"\n    },\n    \"amounts\":{\n        \"claim_amount_hard_limit\":200.00,\n        \"claim_amount\":158.82\n    },\n    \"checks\":{\n        \"free_of_legal_complaints\":true,\n        \"customer_message_is_short\":true,\n        \"customer_message_written_in_a_formal_tone\":false,\n        \"claim_involves_a_media_inquiry\":false,\n        \"free_of_safety_incident_reports\":true,\n        \"proof_of_purchase_attached\":true,\n        \"item_return_not_yet_received\":false,\n        \"item_excluded_by_policy\":false,\n        \"claim_form_filled_in_with_the_usual_font\":true,\n        \"claim_free_of_ombudsman_cases\":false,\n        \"harmless_greeting_present_in_the_message\":true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if free_of_safety_incident_reports is false.\n2. deny if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_not_yet_received is true.\nOtherwise: approve.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nMeanings:\n- ask_manager: route the case to a decider so the requester knows the outcome\n- approve: allow the matter to be taken forward as planned\n- defer: pause this until the requester supplies the missing document\n- deny: skip this one, it is a hard pass for us\nThe record is complete: nothing else applies.\n\nMind telling me which of the actions below is the best call for this request?",
  "options": [
   "defer",
   "approve",
   "deny"
  ]
 },
 {
  "qid": "q2233b4c522",
  "kind": "choice",
  "text": "---\n# record\ninvoice_id: INV-6317\nvendor: Oakmont Traders\ninvoice_pdf_uses_a_portrait_layout: true\napprover_free_of_conflicts_of_interest: true\nvendor_free_of_sanctions: true\nvendor_filed_a_legal_claim_over_this_invoice: false\namount: 123.30\npurchase_order_received: true\npayment_requested_during_business_hours: true\nvendor_name_written_in_capital_letters: false\nduplicate_of_paid_invoice: false\nvendor_tax_form_on_file: true\namount_approval_threshold: 1000.00",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "hand_to_a_person",
   "cancel_order",
   "release"
  ]
 },
 {
  "qid": "q354f4ea472",
  "kind": "yes/no",
  "text": "{\"leave_id\": \"LVE-6939\", \"employee\": \"Paolo Anand\", \"leave_days\": 1, \"leave_days_soft_limit\": 3, \"request_falls_in_blackout_period\": false, \"notice_period_met\": true, \"team_coverage_arranged\": true, \"leave_balance_available\": true, \"requests_team_free_of_harassment_complaints\": true, \"lawyer_letter_received_about_this_leave\": false, \"leave_request_written_in_a_formal_tone\": false, \"union_grievance_raised_over_this_leave\": false, \"medical_certificate_contested\": false}",
  "question": "Proposed action: wait\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q378cb57a08",
  "kind": "choice",
  "text": "# record\ndeploy_id | DEP-8517\nservice | uploads\ndeploy_prohibited_during_the_audit_window | true\ncanary_results_incomplete | false\ndeploy_has_a_long_description | false\ndeploy_blocked_by_security_policy | false\ncommit_messages_written_in_a_detailed_style | true\nbackout_plan_missing | false\nrollout_approval_revoked | false\nfiles_changed | 6\nservice_free_of_major_incidents | true\ncontract_customer_asked_for_a_say_in_this_rollout | false\ncommit_messages_written_in_a_casual_tone | true\nfiles_changed_soft_limit | 15\ndeploy_title_written_in_normal_case | false",
  "question": "Meanings:\n- stop: leave the requester without the result they asked for\n- pause: park this until a record turns up\n- human review: pass this along to the decision maker\n- continue: proceed as requested as nothing impedes this course\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "stop",
   "pause",
   "continue"
  ]
 },
 {
  "qid": "qb8536f7289",
  "kind": "yes/no",
  "text": "# case\nleave_id                                    | LVE-8686\nemployee                                    | Jonas Rossi\nno_union_grievance_raised_over_this_leave   | true\nleave_days_soft_limit                       | 21\nrequest_falls_in_blackout_period            | false\nteam_coverage_arranged                      | false\nnotice_period_met                           | true\nrequests_team_free_of_harassment_complaints | true\nleave_request_written_in_a_formal_tone      | false\nlawyer_letter_received_about_this_leave     | false\nmedical_certificate_contested               | true\nleave_balance_exhausted                     | false\nleave_days                                  | 20",
  "question": "Proposed action: go ahead\nHas the audit trail in the record ruled out the proposed action as a sound call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if notice_period_met is false or team_coverage_arranged is false or leave_days is above leave_days_soft_limit.\n2. turn down if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. send to a person if leave_balance_exhausted is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: go ahead.\nNever counted: leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
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
  "qid": "q9fbf91a751",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-5682\n- requester: Mira Vasquez\n- requested role forbidden by policy: no\n- requester barred from this system: no\n- account suspended: no\n- request grants admin rights: no\n- mfa enrollment incomplete: no\n- ethics office flagged the request: no\n- business justification missing: no\n- legal preservation order on the account: no\n- access days: 7\n- request text written in capital letters: no\n- access days approval threshold: 14",
  "question": "Proposed action: approve\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. delay if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_missing, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4f1c4851b6",
  "kind": "yes/no",
  "text": "---\n# record\ndeploy_id: \"DEP-4792\"\nservice: \"profile\"\ndeploy_prohibited_during_the_audit_window: false\nbackout_plan_documented: true\ndeploy_blocked_by_security_policy: false\nservice_free_of_major_incidents: true\ndeploy_has_a_long_description: false\ncommit_messages_written_in_a_detailed_style: true\ncommit_messages_written_in_a_casual_tone: true\ncanary_results_incomplete: true\nrollout_approval_revoked: false\nfiles_changed_soft_limit: 50\ncontract_customer_asked_for_a_say_in_this_rollout: false\nfiles_changed: 24\ndeploy_title_written_in_normal_case: true",
  "question": "Proposed action: RFCB\nIs the proposed action ruled out by what the record says?",
  "definitions": "Meanings:\n- D: finish what was asked as stated, the way ahead is fully free\n- RFCB: keep waiting for the missing details\n- FXG: drop it right away\n- PK: send it up to the person who makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe489863fe5",
  "kind": "choice",
  "text": "# request record\nticket_id                                 | TCK-5730\ncustomer                                  | Kofi Ferreira\nclaim_involves_a_media_inquiry            | false\nproof_of_purchase_attached                | false\nitem_return_not_yet_received              | false\nclaim_form_filled_in_with_the_usual_font  | true\nclaim_free_of_ombudsman_cases             | true\nitem_excluded_by_policy                   | false\nharmless_greeting_present_in_the_message  | true\nclaim_amount                              | 61.35\nfree_of_legal_complaints                  | true\nfree_of_safety_incident_reports           | false\nclaim_amount_hard_limit                   | 50.00\ncustomer_message_is_short                 | false\ncustomer_message_written_in_a_formal_tone | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ZJD if free_of_safety_incident_reports is false.\n2. TTKH if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. VB if item_return_not_yet_received is true.\nOtherwise: X.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nMeanings:\n- X: complete the action that was asked for\n- TTKH: block the action because it is off limits to the team\n- ZJD: hand this over to whoever has the final say\n- VB: hold all progress until the requisite documentation arrives\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "TTKH",
   "ZJD",
   "X"
  ]
 },
 {
  "qid": "q230e9aa257",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n* request id: REQ-3306\n* requester: Idris Calloway\n* mfa enrollment complete: yes\n* business justification provided: yes\n* requested role permitted by policy: yes\n* requester not barred from this system: yes\n* access days approval threshold: 90\n* access days: 35\n* legal preservation order on the account: no\n* request text written in capital letters: no\n* request grants admin rights: no\n* ethics office flagged the request: no\n* account suspended: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if business_justification_provided is false or mfa_enrollment_complete is false or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n2. refuse if account_suspended is true or requested_role_permitted_by_policy is false.\n3. refer to owner if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: grant.\nNever counted: ethics_office_flagged_the_request, request_text_written_in_capital_letters.\nMeanings:\n- refuse: shut this down before it spreads into the workflow\n- pend: pause the request and gather more information before going on\n- grant: complete the action that was asked for\n- refer to owner: pass the request to a decider\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "grant",
   "refuse",
   "pend"
  ]
 },
 {
  "qid": "q5de1cf23f9",
  "kind": "choice",
  "text": "---\n# record\nrecord:\n  request_id: REQ-8127\n  requester: Leila Haddad\nnumbers:\n  access_days_approval_threshold: 90\n  access_days: 4\nflags:\n  legal_preservation_order_on_the_account: false\n  business_justification_provided: true\n  request_grants_admin_rights: false\n  requested_role_permitted_by_policy: true\n  mfa_enrollment_complete: true\n  account_suspended: false\n  request_text_written_in_capital_letters: true\n  ethics_office_flagged_the_request: false\n  requester_barred_from_this_system: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. delay if requested_role_permitted_by_policy is false.\n3. refuse if mfa_enrollment_complete is false or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_provided, requester_barred_from_this_system, request_text_written_in_capital_letters.\nMeanings:\n- approve: continue with what was requested\n- refuse: kill this one off, it is off the table for good\n- delay: chill until the document turns up\n- ask_a_human: give it to a person who has the authority to decide\nThe record is complete: nothing else applies.\n\nChecklist: which of the actions listed below best answers the request?",
  "options": [
   "refuse",
   "delay",
   "approve"
  ]
 },
 {
  "qid": "qae7820e508",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n* run id: RUN-9770\n* agent: atlas\n* action permitted by security policy: yes\n* last tool output unverified: yes\n* owner sign off required for this action: no\n* action free of ethics concerns: yes\n* steps used hard limit: 40\n* steps used: 14\n* log lines written in a verbose style: no\n* tool output shows tampering: no\n* task description complete: yes",
  "question": "Meanings:\n- ask a human: hand it up to the person who decides\n- cancel: end this here and now\n- proceed: press on with the work as originally set\n- wait: keep waiting for the missing details\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "proceed",
   "ask a human",
   "wait"
  ]
 },
 {
  "qid": "q23d0c7ca01",
  "kind": "yes/no",
  "text": "---\n# record\nrequest_id: \"REQ-2372\"\nrequester: \"ياسمين حاتم الدباغ\"\nnote: \"موافقة المدير المباشر موجودة على طلب الوصول.\"\nrequested_role_permitted_by_policy: true\nethics_office_flagged_the_request: false\naccess_days: 26\naccess_days_approval_threshold: 60\nrequest_grants_admin_rights: false\naccount_suspended: false\nmfa_enrollment_incomplete: false\nbusiness_justification_missing: false\nrequest_text_written_in_capital_letters: false\nlegal_preservation_order_on_the_account: false\nrequester_not_barred_from_this_system: true",
  "question": "Proposed action: proceed\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- wait: hold the request so the requester waits for their check\n- ask a human: route the request to the decision maker\n- cancel: end it so the requester sees their request closed\n- proceed: keep plugging away at it nothing else stands in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5f27cf8ea0",
  "kind": "yes/no",
  "text": "leave_id: LVE-3042\nemployee: ريما فايز الزبيدي\nnote: طلب الإجازة مقدم في الموعد المحدد بالسياسة.\nleave_days_soft_limit: 10\nleave_request_written_in_a_formal_tone: false\nleave_balance_available: false\nmedical_certificate_contested: false\nno_union_grievance_raised_over_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nleave_days: 4\nteam_coverage_arranged: true\nrequest_falls_in_blackout_period: true\nnotice_period_met: false\nlawyer_letter_received_about_this_leave: false",
  "question": "Proposed action: delay\nDoes what we know about this rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. delay if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. refuse if leave_balance_available is false.\nOtherwise: approve.\nNever counted: notice_period_met, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc9a9d29c4f",
  "kind": "yes/no",
  "text": "{\n    \"leave_id\":\"LVE-8173\",\n    \"employee\":\"كنان ياسر الوادي\",\n    \"note\":\"طلب الإجازة مقدم في الموعد المحدد بالسياسة.\",\n    \"team_coverage_not_arranged\":false,\n    \"leave_balance_available\":true,\n    \"medical_certificate_contested\":false,\n    \"lawyer_letter_received_about_this_leave\":false,\n    \"leave_days\":1,\n    \"no_union_grievance_raised_over_this_leave\":true,\n    \"requests_team_free_of_harassment_complaints\":true,\n    \"notice_period_not_met\":false,\n    \"request_falls_in_blackout_period\":true,\n    \"leave_days_soft_limit\":14,\n    \"leave_request_written_in_a_formal_tone\":true\n}",
  "question": "Proposed action: approve\nDo the documented facts rule out the proposed action under this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_not_met is true or team_coverage_not_arranged is true or leave_days is above leave_days_soft_limit.\n2. deny if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. ask manager if leave_balance_available is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: leave_request_written_in_a_formal_tone.\nMeanings:\n- ask manager: be handed over to the deciding person\n- approve: let the request be continued as originally asked\n- defer: await further verification before any progression\n- deny: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q30e787ccd4",
  "kind": "choice",
  "text": "ticket_id | TCK-3428\ncustomer | Felix Okonkwo\nclaim_amount | 846.57\ncustomer_message_is_short | true\nclaim_form_filled_in_with_the_usual_font | true\nharmless_greeting_present_in_the_message | false\nitem_return_received | false\nclaim_amount_hard_limit | 1000.00\nfree_of_safety_incident_reports | true\ncustomer_message_written_in_a_casual_tone | true\nlegal_complaint_filed | false\nitem_excluded_by_policy | false\nclaim_involves_a_media_inquiry | false\nclaim_free_of_ombudsman_cases | true\nproof_of_purchase_attached | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 9 if free_of_safety_incident_reports is false or claim_free_of_ombudsman_cases is false.\n2. 54 if proof_of_purchase_attached is false or item_excluded_by_policy is true or claim_involves_a_media_inquiry is true or claim_amount is above claim_amount_hard_limit.\n3. 411 if item_return_received is false.\nOtherwise: 3855.\nNever counted: legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- 3855: have the item pushed forward as the request stated\n- 9: bring in the authority who can settle it for the requester\n- 54: drop this request from the queue\n- 411: park the file until the requester sends the document in\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "3855",
   "411",
   "9"
  ]
 },
 {
  "qid": "q76c4bb4da1",
  "kind": "choice",
  "text": "{\n    \"meta\":{\n        \"deploy_id\":\"DEP-1137\",\n        \"service\":\"auth_proxy\"\n    },\n    \"metrics\":{\n        \"files_changed\":30,\n        \"files_changed_soft_limit\":30\n    },\n    \"signals\":{\n        \"deploy_blocked_by_security_policy\":false,\n        \"deploy_title_written_in_normal_case\":true,\n        \"rollout_approval_revoked\":false,\n        \"deploy_has_a_long_description\":false,\n        \"commit_messages_written_in_a_casual_tone\":true,\n        \"commit_messages_written_in_a_detailed_style\":true,\n        \"backout_plan_missing\":false,\n        \"deploy_prohibited_during_the_audit_window\":false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\":false,\n        \"service_free_of_major_incidents\":true,\n        \"canary_results_incomplete\":false\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "wait",
   "proceed",
   "cancel"
  ]
 },
 {
  "qid": "q36c62c68b2",
  "kind": "yes/no",
  "text": "{\n    \"request\":{\n        \"leave_id\":\"LVE-4253\",\n        \"employee\":\"Omar Lindqvist\"\n    },\n    \"figures\":{\n        \"leave_days\":2,\n        \"leave_days_soft_limit\":5\n    },\n    \"checks\":{\n        \"union_grievance_raised_over_this_leave\":false,\n        \"team_coverage_not_arranged\":false,\n        \"lawyer_letter_received_about_this_leave\":false,\n        \"leave_request_written_in_a_formal_tone\":false,\n        \"requests_team_free_of_harassment_complaints\":true,\n        \"request_falls_in_blackout_period\":false,\n        \"leave_balance_available\":true,\n        \"medical_certificate_contested\":false,\n        \"notice_period_met\":true\n    }\n}",
  "question": "Proposed action: H\nLooking at the facts, does that rule out the proposed action for this request?",
  "definitions": "Meanings:\n- LB: kill this one off, it is off the table for good\n- BZJQ: hold the request so the requester waits for their check\n- H: get referred to the person who decides\n- VNV: execute the request exactly as written\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q35bfbd7479",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-4515\nvendor=Riverbend Works\namount_approval_threshold=25000.00\namount=16489.36\nvendor_tax_form_missing=false\npayment_requested_during_business_hours=true\nawaiting_purchase_order=false\nduplicate_of_paid_invoice=false\nvendor_filed_a_legal_claim_over_this_invoice=false\nvendor_name_written_in_capital_letters=false\nvendor_free_of_sanctions=true\ninvoice_pdf_uses_a_landscape_layout=false\napprover_free_of_conflicts_of_interest=true",
  "question": "Proposed action: reject\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if approver_free_of_conflicts_of_interest is false.\n2. reject if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- escalate: escalate it so the person asking receives a decision\n- pay: continue with the request as nothing obstructs it\n- reject: block it right away\n- hold: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qafbee6c775",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-9256\",\"vendor\":\"Oakmont Supply\",\"approver_declared_a_conflict_of_interest\":false,\"invoice_pdf_uses_a_portrait_layout\":true,\"vendor_name_written_in_capital_letters\":false,\"payment_requested_during_business_hours\":true,\"vendor_tax_form_missing\":false,\"amount_approval_threshold\":5000.00,\"duplicate_of_paid_invoice\":false,\"amount\":4456.65,\"vendor_filed_a_legal_claim_over_this_invoice\":true,\"vendor_free_of_sanctions\":true,\"purchase_order_received\":true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. ask_a_human if amount is above amount_approval_threshold.\n3. delay if purchase_order_received is false or vendor_tax_form_missing is true or vendor_free_of_sanctions is false or approver_declared_a_conflict_of_interest is true.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- delay: wait for that check then we will see\n- ask_a_human: forward the case to the designated decision maker\n- refuse: stop the request so the requester gets nothing from it\n- approve: have the plan kept moving as it was requested\nThe record is complete: nothing else applies.\n\nTaking the actions listed into account, what is the right call for the request?",
  "options": [
   "approve",
   "ask_a_human",
   "refuse"
  ]
 },
 {
  "qid": "q20f17cb461",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"leave_id\": \"LVE-8049\",\n        \"employee\": \"Anders Novak\"\n    },\n    \"metrics\": {\n        \"leave_days_soft_limit\": 7,\n        \"leave_days\": 2\n    },\n    \"signals\": {\n        \"union_grievance_raised_over_this_leave\": true,\n        \"team_coverage_arranged\": true,\n        \"leave_balance_available\": true,\n        \"leave_request_written_in_a_formal_tone\": true,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"notice_period_met\": true,\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"request_falls_in_blackout_period\": false\n    }\n}",
  "question": "Proposed action: turn_down\nConsidering what was asked and the facts involved, is the proposed action not the correct decision?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if notice_period_met is false or team_coverage_arranged is false or leave_balance_available is false or lawyer_letter_received_about_this_leave is true or leave_days is above leave_days_soft_limit.\n2. turn_down if request_falls_in_blackout_period is true.\n3. send_to_a_person if medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false.\nOtherwise: go_ahead.\nNever counted: union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa2bc92f79a",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-9970\n- vendor: Oakmont Foods\n- vendor filed a legal claim over this invoice: no\n- invoice pdf uses a landscape layout: no\n- approver free of conflicts of interest: yes\n- payment requested during business hours: no\n- vendor name written in capital letters: no\n- duplicate of paid invoice: yes\n- amount approval threshold: 5000.00\n- purchase order received: no\n- amount: 5000.00\n- vendor free of sanctions: yes\n- vendor tax form missing: no",
  "question": "Proposed action: delay\nBased on the request itself and the facts around it, is the proposed action not the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if purchase_order_received is false or vendor_tax_form_missing is true.\n2. refuse if vendor_free_of_sanctions is false.\n3. ask_a_human if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_free_of_conflicts_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- approve: finish it so the requester has their answer\n- ask_a_human: hand this to the person who decides\n- refuse: decline the request as the action is prohibited\n- delay: wait so the requester can supply more information first\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb533b6bc0b",
  "kind": "choice",
  "text": "# extract\nrun_id: RUN-5717\nagent: jasper\nsteps_used_hard_limit: 8\naction_free_of_ethics_concerns: true\nlog_lines_written_in_a_compact_style: true\nsteps_used: 2\nlast_tool_output_verified: true\nowner_sign_off_required_for_this_action: true\ntask_description_incomplete: false\ntool_output_shows_tampering: false\naction_forbidden_by_security_policy: false",
  "question": "Meanings:\n- pause: hang tight until we get the check back\n- stop: stop this course of action at once\n- human review: hand this over to whoever has the final say\n- continue: keep moving so the asker gets the outcome\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "pause",
   "human review",
   "continue"
  ]
 }
]
