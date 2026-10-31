# G5-H blind read T46-blind_read-13aadd80-003 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8b/T46/qc/g5h/answers/T46-blind_read-13aadd80-003.json

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
  "qid": "q998d346429",
  "kind": "yes/no",
  "text": "{\n    \"request\": {\n        \"deploy_id\": \"DEP-5299\",\n        \"service\": \"inventory\"\n    },\n    \"figures\": {\n        \"files_changed\": 75,\n        \"files_changed_soft_limit\": 80\n    },\n    \"checks\": {\n        \"rollout_approval_revoked\": false,\n        \"commit_messages_written_in_a_casual_tone\": true,\n        \"canary_results_incomplete\": false,\n        \"deploy_has_a_long_description\": false,\n        \"deploy_blocked_by_security_policy\": false,\n        \"backout_plan_missing\": false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\": false,\n        \"deploy_prohibited_during_the_audit_window\": false,\n        \"commit_messages_written_in_a_terse_style\": false,\n        \"deploy_title_written_in_normal_case\": true,\n        \"service_free_of_major_incidents\": true\n    }\n}",
  "question": "Proposed action: stop\nShould the proposed action be taken for this request?",
  "definitions": "Meanings:\n- stop: block it right away\n- human_review: hand this off because a decider has to choose\n- pause: hold up for a sec until more info comes in\n- continue: keep it moving forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q84c287fafd",
  "kind": "yes/no",
  "text": "{\n  \"ticket_id\":\"TCK-8352\",\n  \"customer\":\"Nadia Imai\",\n  \"harmless_greeting_present_in_the_message\":true,\n  \"claim_involves_a_media_inquiry\":false,\n  \"claim_amount_hard_limit\":500.00,\n  \"item_excluded_by_policy\":false,\n  \"claim_free_of_ombudsman_cases\":true,\n  \"free_of_safety_incident_reports\":true,\n  \"item_return_not_yet_received\":false,\n  \"proof_of_purchase_missing\":false,\n  \"claim_form_filled_in_with_the_usual_font\":true,\n  \"customer_message_is_short\":true,\n  \"customer_message_written_in_a_casual_tone\":true,\n  \"legal_complaint_filed\":false,\n  \"claim_amount\":378.96\n}",
  "question": "Proposed action: ask_a_human\nIs it not the case that the proposed action is what the request and facts call for, and is not a poor choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if claim_amount is above claim_amount_hard_limit.\n2. ask_a_human if item_return_not_yet_received is true or item_excluded_by_policy is true or legal_complaint_filed is true or free_of_safety_incident_reports is false or claim_involves_a_media_inquiry is true.\n3. delay if proof_of_purchase_missing is true or claim_free_of_ombudsman_cases is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- refuse: bin this idea and keep it out of the flow\n- approve: proceed with the task as asked\n- delay: wait for the document to come through\n- ask_a_human: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q61a28e9931",
  "kind": "yes/no",
  "text": "# extract\nrun_id = RUN-9663\nagent = delta\nlast_tool_output_verified = false\nsteps_used_hard_limit = 16\nlog_lines_written_in_a_compact_style = true\nsteps_used = 4\naction_forbidden_by_security_policy = false\ntool_output_shows_tampering = false\nowner_sign_off_required_for_this_action = false\naction_free_of_ethics_concerns = true\ntask_description_incomplete = false",
  "question": "Proposed action: wait\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- ask_a_human: route this matter to the individual empowered to decide\n- cancel: withdraw from the step as it is forbidden\n- proceed: execute the requested action as nothing prevents it\n- wait: hold the request until the check is done\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q541cec763b",
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
  "qid": "q30d6b047b4",
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
  "qid": "q177da13eca",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"invoice_id\": \"INV-7316\",\n        \"vendor\": \"Summit Logistics\"\n    },\n    \"values\": {\n        \"amount_approval_threshold\": 500.00,\n        \"amount\": 500.00\n    },\n    \"tests\": {\n        \"approver_declared_a_conflict_of_interest\": false,\n        \"duplicate_of_paid_invoice\": false,\n        \"invoice_pdf_uses_a_landscape_layout\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"vendor_name_written_in_capital_letters\": false,\n        \"vendor_tax_form_missing\": false,\n        \"purchase_order_received\": true,\n        \"vendor_free_of_sanctions\": true,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": false\n    }\n}",
  "question": "Proposed action: delay\nDoes the proposed action make sense for the request shown in the record?",
  "definitions": "Meanings:\n- refuse: skip this one, it is a hard pass for us\n- delay: hold all progress until the requisite documentation arrives\n- ask a human: get sent upward to the one who decides\n- approve: run the requested step through\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qdea69c3321",
  "kind": "choice",
  "text": "# record\nticket_id=TCK-4077\ncustomer=Idris Rossi\nclaim_amount_hard_limit=50.00\nfree_of_safety_incident_reports=true\nproof_of_purchase_missing=false\nitem_return_received=true\nclaim_involves_a_media_inquiry=false\nitem_excluded_by_policy=false\ncustomer_message_is_short=true\nharmless_greeting_present_in_the_message=true\nclaim_form_filled_in_with_the_usual_font=true\nfree_of_legal_complaints=true\ncustomer_message_written_in_a_formal_tone=false\nclaim_amount=48.83\nclaim_free_of_ombudsman_cases=true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. GKZR if claim_amount is above claim_amount_hard_limit.\n2. WFM if item_return_received is false or item_excluded_by_policy is true or free_of_legal_complaints is false or free_of_safety_incident_reports is false or claim_involves_a_media_inquiry is true.\n3. TJ if proof_of_purchase_missing is true or claim_free_of_ombudsman_cases is false.\nOtherwise: J.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nMeanings:\n- J: complete the job as it was assigned\n- WFM: forward it to the decision maker\n- TJ: stay put until the check is finished\n- GKZR: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies.\n\nConsidering what was asked and the facts available, which action below should be chosen?",
  "options": [
   "TJ",
   "J",
   "WFM"
  ]
 },
 {
  "qid": "q7994906314",
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
  "qid": "qef628e1849",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-1633\",\"vendor\":\"Stonebridge Foods\",\"vendor_tax_form_on_file\":true,\"duplicate_of_paid_invoice\":false,\"vendor_name_written_in_capital_letters\":false,\"awaiting_purchase_order\":true,\"amount_approval_threshold\":5000.00,\"vendor_filed_a_legal_claim_over_this_invoice\":false,\"payment_requested_during_business_hours\":false,\"invoice_pdf_uses_a_landscape_layout\":false,\"amount\":2585.37,\"approver_free_of_conflicts_of_interest\":true,\"vendor_on_sanctions_list\":true}",
  "question": "Proposed action: turn down\nDo the facts here rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if vendor_on_sanctions_list is true or approver_free_of_conflicts_of_interest is false.\n2. send to a person if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. put on hold if awaiting_purchase_order is true or amount is at least amount_approval_threshold.\nOtherwise: go ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- turn down: stop the work since it cannot move forward\n- go ahead: just crack on with it there is nothing in the way\n- send to a person: route the case to a decider so the requester knows the outcome\n- put on hold: wait for the check and the requester will hear back later\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9f3af2d69b",
  "kind": "yes/no",
  "text": "leave_id | LVE-9441\nemployee | عادل فؤاد النابلسي\nnote | المدير المباشر وافق على الطلب مسبقاً.\nrequests_team_free_of_harassment_complaints | true\nnotice_period_not_met | false\nleave_days | 7\nunion_grievance_raised_over_this_leave | false\nmedical_certificate_contested | false\nleave_request_written_in_a_formal_tone | false\nteam_coverage_arranged | true\nlawyer_letter_received_about_this_leave | false\nleave_days_soft_limit | 7\nrequest_falls_in_blackout_period | false\nleave_balance_available | false",
  "question": "Proposed action: PXS\nLooking at what the record says, is the proposed action a good fit for the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. T if notice_period_not_met is true or team_coverage_arranged is false or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. VSFG if medical_certificate_contested is true.\n3. HM if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: PXS.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- T: hold all progress until the requisite documentation arrives\n- VSFG: reject the request in full\n- PXS: run the requested step through\n- HM: get the boss to make the final call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb67dd2af01",
  "kind": "yes/no",
  "text": "---\n# record\nrun_id: RUN-9481\nagent: fjord\nsteps_used: 5\nsteps_used_hard_limit: 20\nowner_sign_off_required_for_this_action: false\nlog_lines_written_in_a_compact_style: true\nlast_tool_output_verified: true\ntool_output_shows_tampering: false\ntask_description_complete: true\naction_forbidden_by_security_policy: true\naction_free_of_ethics_concerns: true",
  "question": "Proposed action: 7\nReviewing this file as an auditor, is the proposed action not the correct step?",
  "definitions": "Meanings:\n- 7: ditch the whole thing, nobody should act on it\n- 6528: carry out the task as instructed without any obstacle\n- 338: route the case to a decider so the requester knows the outcome\n- 51: hold the request so the requester waits for their check\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q50a7c3b9a4",
  "kind": "yes/no",
  "text": "{\n  \"request_id\":\"REQ-1430\",\n  \"requester\":\"Idris Adeyemi\",\n  \"requested_role_permitted_by_policy\":true,\n  \"business_justification_provided\":true,\n  \"legal_preservation_order_on_the_account\":false,\n  \"request_free_of_ethics_office_flags\":true,\n  \"access_days_approval_threshold\":7,\n  \"request_grants_admin_rights\":false,\n  \"requester_not_barred_from_this_system\":false,\n  \"access_days\":4,\n  \"mfa_enrollment_complete\":true,\n  \"request_text_written_in_capital_letters\":false,\n  \"account_suspended\":false\n}",
  "question": "Proposed action: allow\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_provided is false or requested_role_permitted_by_policy is false.\n2. page oncall if mfa_enrollment_complete is false or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. block access if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: allow.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- block access: shut this down fast\n- allow: proceed with the task as asked\n- quarantine: defer the step until the verification is in\n- page oncall: send it up so the requester gets a firm decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q93fcf38496",
  "kind": "yes/no",
  "text": "# case\ndeploy_id: DEP-7725\nservice: gateway\ndeploy_prohibited_during_the_audit_window: false\ncommit_messages_written_in_a_casual_tone: true\ncanary_results_complete: true\nrollout_approval_revoked: false\ncommit_messages_written_in_a_detailed_style: true\nbackout_plan_documented: true\ndeploy_title_written_in_normal_case: true\nservice_free_of_major_incidents: true\ndeploy_blocked_by_security_policy: false\ncontract_customer_asked_for_a_say_in_this_rollout: false\nfiles_changed: 4\nfiles_changed_soft_limit: 15\ndeploy_has_a_long_description: true",
  "question": "Proposed action: continue\nSeen against the request in the record, would the proposed action be the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pause if backout_plan_documented is false.\n2. stop if rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is at least files_changed_soft_limit.\n3. human review if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\nOtherwise: continue.\nNever counted: canary_results_complete, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc72440b9e6",
  "kind": "yes/no",
  "text": "{\n    \"request\":{\n        \"leave_id\":\"LVE-4253\",\n        \"employee\":\"Omar Lindqvist\"\n    },\n    \"figures\":{\n        \"leave_days\":2,\n        \"leave_days_soft_limit\":5\n    },\n    \"checks\":{\n        \"union_grievance_raised_over_this_leave\":false,\n        \"team_coverage_not_arranged\":false,\n        \"lawyer_letter_received_about_this_leave\":false,\n        \"leave_request_written_in_a_formal_tone\":false,\n        \"requests_team_free_of_harassment_complaints\":true,\n        \"request_falls_in_blackout_period\":false,\n        \"leave_balance_available\":true,\n        \"medical_certificate_contested\":false,\n        \"notice_period_met\":true\n    }\n}",
  "question": "Proposed action: H\nLooking at the facts, does that rule out the proposed action for this request?",
  "definitions": "Meanings:\n- LB: kill this one off, it is off the table for good\n- BZJQ: hold the request so the requester waits for their check\n- H: get referred to the person who decides\n- VNV: execute the request exactly as written\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7bb5b04edf",
  "kind": "yes/no",
  "text": "---\nrequest:\n    request_id: REQ-6320\n    requester: Felix Brandt\nfigures:\n    access_days: 2\n    access_days_approval_threshold: 14\nchecks:\n    account_suspended: false\n    request_text_written_in_capital_letters: false\n    mfa_enrollment_complete: true\n    request_grants_admin_rights: false\n    requester_barred_from_this_system: false\n    requested_role_forbidden_by_policy: true\n    ethics_office_flagged_the_request: true\n    legal_preservation_order_on_the_account: false\n    business_justification_provided: true",
  "question": "Proposed action: refuse\nIs the proposed action the appropriate course of action for the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if business_justification_provided is false or mfa_enrollment_complete is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. refuse if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. refer to owner if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: grant.\nNever counted: ethics_office_flagged_the_request, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qba714b2d1a",
  "kind": "yes/no",
  "text": "---\nleave_id: LVE-9339\nemployee: غسان مروان العلوي\nnote: الموافقة على الإجازة ما زالت ناقصة بسبب بيانات غير مؤكدة.\nnotice_period_not_met: false\nunion_grievance_raised_over_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nleave_request_written_in_a_formal_tone: false\nleave_balance_exhausted: false\nteam_coverage_not_arranged: false\nleave_days: 2\nrequest_falls_in_blackout_period: false\nleave_days_soft_limit: 7\nlawyer_letter_received_about_this_leave: false\nmedical_certificate_contested: false",
  "question": "Proposed action: defer\nIs the proposed action the right call, judging from what the record shows?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q4a29d5d026",
  "kind": "choice",
  "text": "---\n# case\nticket_id: TCK-1668\ncustomer: Jonas Petrov\nclaim_involves_a_media_inquiry: false\ncustomer_message_written_in_a_casual_tone: false\nproof_of_purchase_missing: true\nitem_return_not_yet_received: false\nclaim_form_filled_in_with_the_usual_font: true\nclaim_amount_hard_limit: 1000.00\nitem_excluded_by_policy: false\nharmless_greeting_present_in_the_message: true\ncustomer_message_is_short: true\nclaim_amount: 117.93\nfree_of_safety_incident_reports: true\nlegal_complaint_filed: false\nclaim_free_of_ombudsman_cases: true",
  "question": "Meanings:\n- 7950: shelve the matter until more details come in\n- 78: shut off this process completely\n- 189: forward the case to the designated decision maker\n- 9: go on and finish it the path is clear\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "189",
   "7950",
   "9"
  ]
 },
 {
  "qid": "qa2b2a7cc75",
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
  "qid": "q2de133beed",
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
  "qid": "q67e3bb91a1",
  "kind": "choice",
  "text": "{\n    \"deploy_id\": \"DEP-6932\",\n    \"service\": \"inventory\",\n    \"service_free_of_major_incidents\": true,\n    \"files_changed\": 4,\n    \"deploy_title_written_in_normal_case\": true,\n    \"commit_messages_written_in_a_casual_tone\": true,\n    \"deploy_blocked_by_security_policy\": false,\n    \"files_changed_soft_limit\": 15,\n    \"rollout_approval_revoked\": false,\n    \"deploy_prohibited_during_the_audit_window\": true,\n    \"backout_plan_missing\": false,\n    \"contract_customer_asked_for_a_say_in_this_rollout\": true,\n    \"canary_results_incomplete\": false,\n    \"deploy_has_a_long_description\": false,\n    \"commit_messages_written_in_a_terse_style\": false\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. PLPD if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. QK if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. XWX if backout_plan_missing is true or rollout_approval_revoked is true.\nOtherwise: M.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- XWX: wait so the requester can supply more information first\n- QK: be turned away and treated as off limits\n- M: keep going with it nothing is blocking you\n- PLPD: pass the request to a decider\nThe record is complete: nothing else applies.\n\nPicking from the actions listed, what best serves this request?",
  "options": [
   "PLPD",
   "M",
   "QK"
  ]
 },
 {
  "qid": "q035ab3c27d",
  "kind": "yes/no",
  "text": "# record\nrequest_id | REQ-3758\nrequester | Nadia Imai\nmfa_enrollment_incomplete | false\nrequest_text_written_in_capital_letters | false\nlegal_preservation_order_on_the_account | false\nethics_office_flagged_the_request | false\naccess_days_approval_threshold | 60\naccess_days | 27\nrequest_grants_admin_rights | true\naccount_suspended | false\nrequester_not_barred_from_this_system | true\nbusiness_justification_missing | false\nrequested_role_permitted_by_policy | false",
  "question": "Proposed action: ask_a_human\nWould the proposed action not be the appropriate course under the applicable procedure?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. wait if requested_role_permitted_by_policy is false.\n3. cancel if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: proceed.\nNever counted: business_justification_missing, requester_not_barred_from_this_system, request_text_written_in_capital_letters.\nMeanings:\n- proceed: complete the job as it was assigned\n- ask_a_human: give it to the person in charge of the call\n- cancel: end this here and now\n- wait: wait for that check then we will see\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd8f2bd1b15",
  "kind": "yes/no",
  "text": "{\n    \"request\":{\n        \"deploy_id\":\"DEP-7571\",\n        \"service\":\"notifier\"\n    },\n    \"figures\":{\n        \"files_changed_soft_limit\":10,\n        \"files_changed\":2\n    },\n    \"checks\":{\n        \"deploy_prohibited_during_the_audit_window\":false,\n        \"commit_messages_written_in_a_terse_style\":false,\n        \"deploy_has_a_long_description\":false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\":true,\n        \"canary_results_complete\":true,\n        \"deploy_blocked_by_security_policy\":false,\n        \"commit_messages_written_in_a_casual_tone\":true,\n        \"backout_plan_missing\":false,\n        \"rollout_approval_revoked\":false,\n        \"deploy_title_written_in_normal_case\":true,\n        \"service_free_of_major_incidents\":true\n    }\n}",
  "question": "Proposed action: human_review\nIs the proposed action the right step for the request?",
  "definitions": "Meanings:\n- pause: wait for that check then we will see\n- human_review: give it to a person who has the authority to decide\n- stop: shut this down before it spreads into the workflow\n- continue: keep going exactly as requested because every obstacle has cleared\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q57c5c4caa4",
  "kind": "yes/no",
  "text": "{\n  \"record\": {\n    \"request_id\": \"REQ-6858\",\n    \"requester\": \"Zoe Haddad\"\n  },\n  \"numbers\": {\n    \"access_days\": 60,\n    \"access_days_approval_threshold\": 60\n  },\n  \"flags\": {\n    \"business_justification_provided\": false,\n    \"request_grants_admin_rights\": false,\n    \"request_text_written_in_capital_letters\": true,\n    \"requested_role_forbidden_by_policy\": false,\n    \"requester_not_barred_from_this_system\": true,\n    \"legal_preservation_order_on_the_account\": false,\n    \"ethics_office_flagged_the_request\": false,\n    \"account_suspended\": true,\n    \"mfa_enrollment_incomplete\": false\n  }\n}",
  "question": "Proposed action: approve\nDoes the proposed action fit the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if mfa_enrollment_incomplete is true or requester_not_barred_from_this_system is false or ethics_office_flagged_the_request is true.\n2. refuse if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. ask_a_human if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: approve.\nNever counted: business_justification_provided, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- delay: defer further action pending verification of the document\n- ask_a_human: route this matter to the individual empowered to decide\n- approve: execute the request exactly as written\n- refuse: stop the work since it cannot move forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa09e4bebb7",
  "kind": "choice",
  "text": "{\n  \"case\": {\n    \"request_id\": \"REQ-9596\",\n    \"requester\": \"Tomas Tanaka\"\n  },\n  \"values\": {\n    \"access_days\": 90,\n    \"access_days_approval_threshold\": 90\n  },\n  \"tests\": {\n    \"request_grants_admin_rights\": false,\n    \"business_justification_provided\": true,\n    \"account_suspended\": false,\n    \"legal_preservation_order_on_the_account\": false,\n    \"mfa_enrollment_incomplete\": false,\n    \"request_text_written_in_capital_letters\": false,\n    \"requester_not_barred_from_this_system\": false,\n    \"request_free_of_ethics_office_flags\": true,\n    \"requested_role_permitted_by_policy\": true\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if business_justification_provided is false or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n2. ask manager if mfa_enrollment_incomplete is true or request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n3. deny if account_suspended is true or requested_role_permitted_by_policy is false.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- ask manager: pass the request along since the decision belongs to another person\n- deny: block the action because it is off limits to the team\n- approve: proceed as requested as nothing impedes this course\n- defer: be parked until a verification has been logged\nThe record is complete: nothing else applies.\n\nLooking at this case file, which of the actions listed is the right call?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "qe3ee4690c5",
  "kind": "choice",
  "text": "# extract\nticket_id: TCK-7676\ncustomer: Sana Castell\nharmless_greeting_present_in_the_message: true\nproof_of_purchase_attached: true\nfree_of_safety_incident_reports: true\nclaim_amount: 200.01\nclaim_amount_hard_limit: 200.00\ncustomer_message_written_in_a_formal_tone: false\nfree_of_legal_complaints: true\ncustomer_message_is_short: true\nitem_excluded_by_policy: false\nclaim_free_of_ombudsman_cases: true\nclaim_form_filled_in_with_the_usual_font: false\nitem_return_not_yet_received: false\nclaim_involves_a_media_inquiry: false",
  "question": "Meanings:\n- approve: advance the task as stated without any blockers\n- defer: chill until the document turns up\n- ask manager: send it up to the person who makes the call\n- deny: stop the work since it cannot move forward\nThe record is complete: nothing else applies.\n\nReading the file for this case, which listed action is the best call?",
  "options": [
   "deny",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q395256d4f4",
  "kind": "choice",
  "text": "---\n# request record\nrecord:\n    ticket_id: \"TCK-9150\"\n    customer: \"Tomas Moreau\"\nnumbers:\n    claim_amount: 256.82\n    claim_amount_hard_limit: 2000.00\nflags:\n    harmless_greeting_present_in_the_message: true\n    proof_of_purchase_missing: false\n    claim_form_filled_in_with_the_usual_font: true\n    legal_complaint_filed: true\n    claim_involves_a_media_inquiry: false\n    customer_message_is_short: true\n    customer_message_written_in_a_casual_tone: true\n    free_of_safety_incident_reports: true\n    claim_free_of_ombudsman_cases: true\n    item_return_not_yet_received: false\n    item_excluded_by_policy: false",
  "question": "Meanings:\n- HDSK: pump the brakes until more details show up\n- FZ: continue as requested with the path fully open\n- WLC: end it so the requester sees their request closed\n- T: kick it up to whoever makes the call\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "HDSK",
   "FZ",
   "T"
  ]
 },
 {
  "qid": "qdf5b8d7912",
  "kind": "choice",
  "text": "# record\ndeploy_id | DEP-4154\nservice | reports\nfiles_changed | 13\nfiles_changed_soft_limit | 15\ncanary_results_complete | true\ncommit_messages_written_in_a_casual_tone | true\ndeploy_title_written_in_normal_case | true\ndeploy_prohibited_during_the_audit_window | false\ndeploy_has_a_long_description | false\nservice_free_of_major_incidents | false\nrollout_approval_revoked | true\ncontract_customer_asked_for_a_say_in_this_rollout | false\nbackout_plan_missing | false\ndeploy_blocked_by_security_policy | false\ncommit_messages_written_in_a_detailed_style | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\n2. turn_down if rollout_approval_revoked is true.\n3. put_on_hold if canary_results_complete is false or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\nOtherwise: go_ahead.\nNever counted: backout_plan_missing, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- turn_down: halt this item because the rules forbid it\n- send_to_a_person: be routed to whoever holds the decision\n- put_on_hold: wait for the document before going further\n- go_ahead: just crack on with it there is nothing in the way\nThe record is complete: nothing else applies.\n\nTaking the facts of the request into account, which action listed should be picked?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "turn_down"
  ]
 },
 {
  "qid": "qea0c1a427f",
  "kind": "choice",
  "text": "---\n# request record\nticket_id: \"TCK-7030\"\ncustomer: \"Elena Lindqvist\"\nclaim_amount: 2000.01\nproof_of_purchase_missing: false\ncustomer_message_written_in_a_formal_tone: false\nclaim_amount_hard_limit: 2000.00\nclaim_form_filled_in_with_the_usual_font: true\nfree_of_safety_incident_reports: true\nitem_excluded_by_policy: false\nclaim_involves_a_media_inquiry: false\nitem_return_received: true\ncustomer_message_is_short: true\nharmless_greeting_present_in_the_message: true\nclaim_free_of_ombudsman_cases: true\nlegal_complaint_filed: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if free_of_safety_incident_reports is false.\n2. turn_down if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. put_on_hold if item_return_received is false.\nOtherwise: go_ahead.\nNever counted: proof_of_purchase_missing, item_excluded_by_policy, legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nMeanings:\n- go_ahead: move ahead on the request in the form it arrived since the path is open\n- send_to_a_person: route this to the one who signs off\n- turn_down: send the requester away with the request left unfinished\n- put_on_hold: await further verification before any progression\nThe record is complete: nothing else applies.\n\nOf the actions listed after this, which is the fitting call for the request?",
  "options": [
   "turn_down",
   "put_on_hold",
   "go_ahead"
  ]
 },
 {
  "qid": "q404a81e0d8",
  "kind": "yes/no",
  "text": "leave_id=LVE-5594\nemployee=هيفاء نزار الساعدي\nnote=تواريخ الإجازة لا تتعارض مع جدول العمل.\nteam_coverage_arranged=true\nnotice_period_met=true\nleave_balance_available=false\nlawyer_letter_received_about_this_leave=false\nleave_request_written_in_a_formal_tone=false\nleave_days_soft_limit=21\nleave_days=18\nrequest_falls_in_blackout_period=false\nrequests_team_free_of_harassment_complaints=true\nmedical_certificate_contested=false\nno_union_grievance_raised_over_this_leave=false",
  "question": "Proposed action: W\nShould the proposed action be taken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QRW if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. JF if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. W if leave_balance_available is false.\nOtherwise: HKWC.\nNever counted: notice_period_met, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nMeanings:\n- W: kill this one off, it is off the table for good\n- JF: defer the step until the verification is in\n- QRW: be handed over to the deciding person\n- HKWC: advance the task as stated without any blockers\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1b0fff446f",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n* deploy id: DEP-5133\n* service: inventory\n* contract customer asked for a say in this rollout: no\n* deploy has a long description: no\n* commit messages written in a casual tone: yes\n* deploy blocked by security policy: no\n* deploy prohibited during the audit window: no\n* backout plan missing: no\n* deploy title written in normal case: yes\n* files changed: 7\n* service free of major incidents: yes\n* commit messages written in a detailed style: yes\n* files changed soft limit: 20\n* canary results incomplete: no\n* rollout approval revoked: no",
  "question": "Proposed action: GCT\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. GCT if backout_plan_missing is true or rollout_approval_revoked is true or files_changed is at least files_changed_soft_limit.\n2. CQFW if contract_customer_asked_for_a_say_in_this_rollout is true.\n3. X if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\nOtherwise: DN.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- CQFW: route it elsewhere because a decider must weigh in\n- DN: go ahead with the requested action\n- X: be turned away and treated as off limits\n- GCT: keep it in limbo until the verification has been confirmed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6212146fb9",
  "kind": "choice",
  "text": "# record\nrequest_id | REQ-7120\nrequester | Felix Castell\naccount_suspended | false\naccess_days_approval_threshold | 60\nrequested_role_forbidden_by_policy | false\nrequest_text_written_in_capital_letters | false\nrequest_free_of_ethics_office_flags | true\nmfa_enrollment_complete | true\nrequest_grants_admin_rights | false\nlegal_preservation_order_on_the_account | true\nrequester_barred_from_this_system | false\naccess_days | 1\nbusiness_justification_missing | false",
  "question": "The record is complete: nothing else applies.\n\nWhat do the facts support, and which of the actions listed follows from them?",
  "options": [
   "ask_a_human",
   "delay",
   "approve"
  ]
 },
 {
  "qid": "q2080097b77",
  "kind": "yes/no",
  "text": "# record\nrequest_id | REQ-3758\nrequester | Nadia Imai\nmfa_enrollment_incomplete | false\nrequest_text_written_in_capital_letters | false\nlegal_preservation_order_on_the_account | false\nethics_office_flagged_the_request | false\naccess_days_approval_threshold | 60\naccess_days | 27\nrequest_grants_admin_rights | true\naccount_suspended | false\nrequester_not_barred_from_this_system | true\nbusiness_justification_missing | false\nrequested_role_permitted_by_policy | false",
  "question": "Proposed action: ask_a_human\nIs it not the case that the facts shown here back the proposed action, which is not mistaken?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. wait if requested_role_permitted_by_policy is false.\n3. cancel if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: proceed.\nNever counted: business_justification_missing, requester_not_barred_from_this_system, request_text_written_in_capital_letters.\nMeanings:\n- proceed: complete the job as it was assigned\n- ask_a_human: give it to the person in charge of the call\n- cancel: end this here and now\n- wait: wait for that check then we will see\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q043af4c6ef",
  "kind": "choice",
  "text": "# case\nticket_id: TCK-1823\ncustomer: Samir Adeyemi\ncustomer_message_is_short: true\nharmless_greeting_present_in_the_message: true\nproof_of_purchase_attached: true\nclaim_amount: 265.75\nclaim_form_filled_in_with_the_usual_font: true\nitem_return_received: true\nlegal_complaint_filed: false\nitem_excluded_by_policy: false\nclaim_involves_a_media_inquiry: false\nfree_of_safety_incident_reports: true\nclaim_amount_hard_limit: 500.00\nclaim_free_of_ombudsman_cases: true\ncustomer_message_written_in_a_formal_tone: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "deny",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "q85d82132f2",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  leave_id: LVE-7443\n  employee: Aiko Mensah\nnumbers:\n  leave_days_soft_limit: 21\n  leave_days: 10\nflags:\n  leave_balance_exhausted: false\n  leave_request_written_in_a_formal_tone: true\n  request_falls_in_blackout_period: false\n  medical_certificate_contested: false\n  lawyer_letter_received_about_this_leave: false\n  team_coverage_arranged: true\n  requests_team_free_of_harassment_complaints: false\n  notice_period_met: true\n  union_grievance_raised_over_this_leave: false",
  "question": "Proposed action: proceed\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if notice_period_met is false or team_coverage_arranged is false or leave_balance_exhausted is true or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. cancel if medical_certificate_contested is true.\n3. ask_a_human if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: proceed.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- ask_a_human: route the case to a decider so the requester knows the outcome\n- cancel: be stopped and never carried out\n- proceed: go on and finish it the path is clear\n- wait: be kept on hold until more information is supplied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2adc55d231",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-2055\", \"vendor\": \"Silverline Group\", \"payment_requested_during_business_hours\": false, \"invoice_pdf_uses_a_landscape_layout\": true, \"awaiting_purchase_order\": false, \"vendor_on_sanctions_list\": false, \"amount_approval_threshold\": 10000.00, \"duplicate_of_paid_invoice\": false, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"vendor_name_written_in_capital_letters\": false, \"approver_free_of_conflicts_of_interest\": false, \"amount\": 4792.99, \"vendor_tax_form_on_file\": true}",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "put_on_hold",
   "go_ahead",
   "send_to_a_person"
  ]
 },
 {
  "qid": "q24cdb42da4",
  "kind": "choice",
  "text": "{\n    \"subject\": {\n        \"leave_id\": \"LVE-2290\",\n        \"employee\": \"وفاء محسن الفارس\",\n        \"note\": \"التوقيع المرفق بطلب الإجازة ليس توقيع الموظف المعني.\"\n    },\n    \"amounts\": {\n        \"leave_days\": 1,\n        \"leave_days_soft_limit\": 5\n    },\n    \"checks\": {\n        \"leave_request_written_in_a_formal_tone\": false,\n        \"request_falls_in_blackout_period\": false,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"team_coverage_arranged\": true,\n        \"leave_balance_exhausted\": false,\n        \"notice_period_met\": true,\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"union_grievance_raised_over_this_leave\": false\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "proceed",
   "cancel",
   "ask a human"
  ]
 },
 {
  "qid": "qf5a36d789e",
  "kind": "choice",
  "text": "invoice_id=INV-5383\nvendor=Riverbend Partners\nvendor_tax_form_missing=false\nduplicate_of_paid_invoice=false\napprover_free_of_conflicts_of_interest=true\nvendor_filed_a_legal_claim_over_this_invoice=false\nawaiting_purchase_order=false\ninvoice_pdf_uses_a_landscape_layout=false\nvendor_free_of_sanctions=true\npayment_requested_during_business_hours=false\namount=500.01\nvendor_name_written_in_capital_letters=false\namount_approval_threshold=500.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if approver_free_of_conflicts_of_interest is false.\n2. cancel if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. wait if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: proceed.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed under the record would the requester see as the right call?",
  "options": [
   "wait",
   "proceed",
   "cancel"
  ]
 },
 {
  "qid": "q0f02071ec4",
  "kind": "choice",
  "text": "{\n    \"request\": {\n        \"run_id\": \"RUN-9822\",\n        \"agent\": \"jasper\"\n    },\n    \"figures\": {\n        \"steps_used\": 4,\n        \"steps_used_hard_limit\": 16\n    },\n    \"checks\": {\n        \"action_free_of_ethics_concerns\": true,\n        \"tool_output_shows_tampering\": false,\n        \"log_lines_written_in_a_verbose_style\": false,\n        \"action_permitted_by_security_policy\": false,\n        \"owner_sign_off_required_for_this_action\": false,\n        \"task_description_incomplete\": true,\n        \"last_tool_output_unverified\": false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. human review if action_free_of_ethics_concerns is false or owner_sign_off_required_for_this_action is true.\n2. pause if action_permitted_by_security_policy is false.\n3. stop if tool_output_shows_tampering is true or steps_used is above steps_used_hard_limit.\nOtherwise: continue.\nNever counted: last_tool_output_unverified, task_description_incomplete, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "continue",
   "human review",
   "pause"
  ]
 },
 {
  "qid": "qfd3aad0517",
  "kind": "yes/no",
  "text": "invoice_id | INV-7422\nvendor | Riverbend Traders\ninvoice_pdf_uses_a_landscape_layout | false\nawaiting_purchase_order | false\npayment_requested_during_business_hours | true\nduplicate_of_paid_invoice | true\namount | 2138.37\nvendor_tax_form_on_file | true\napprover_declared_a_conflict_of_interest | false\namount_approval_threshold | 5000.00\nvendor_on_sanctions_list | true\nvendor_name_written_in_capital_letters | false\nvendor_filed_a_legal_claim_over_this_invoice | false",
  "question": "Proposed action: cancel\nSet beside the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if vendor_on_sanctions_list is true or approver_declared_a_conflict_of_interest is true.\n2. ask a human if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. wait if awaiting_purchase_order is true or amount is at least amount_approval_threshold.\nOtherwise: proceed.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd3780f7ecf",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- request id: REQ-7490\n- requester: Nadia Haddad\n- requested role permitted by policy: yes\n- access days: 4\n- mfa enrollment incomplete: no\n- request text written in capital letters: no\n- request grants admin rights: yes\n- request free of ethics office flags: yes\n- account suspended: no\n- business justification missing: no\n- legal preservation order on the account: yes\n- requester not barred from this system: yes\n- access days approval threshold: 7",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if mfa_enrollment_incomplete is true or requester_not_barred_from_this_system is false or request_free_of_ethics_office_flags is false.\n2. deny if account_suspended is true or requested_role_permitted_by_policy is false.\n3. ask_manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: approve.\nNever counted: business_justification_missing, request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "ask_manager",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q8e23a239e7",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  deploy_id: DEP-8639\n  service: inventory\nnumbers:\n  files_changed_soft_limit: 30\n  files_changed: 30\nflags:\n  rollout_approval_revoked: false\n  commit_messages_written_in_a_terse_style: false\n  deploy_prohibited_during_the_audit_window: true\n  deploy_has_a_long_description: false\n  service_free_of_major_incidents: true\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  deploy_blocked_by_security_policy: false\n  deploy_title_written_in_normal_case: true\n  commit_messages_written_in_a_casual_tone: true\n  backout_plan_documented: true\n  canary_results_incomplete: false",
  "question": "Proposed action: go ahead\nSet beside the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. put on hold if canary_results_incomplete is true.\nOtherwise: go ahead.\nNever counted: backout_plan_documented, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q88873296d2",
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
  "qid": "q968249daeb",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"run_id\": \"RUN-7525\",\n        \"agent\": \"beacon\"\n    },\n    \"metrics\": {\n        \"steps_used_hard_limit\": 8,\n        \"steps_used\": 2\n    },\n    \"signals\": {\n        \"owner_sign_off_required_for_this_action\": false,\n        \"task_description_complete\": true,\n        \"last_tool_output_verified\": false,\n        \"tool_output_shows_tampering\": false,\n        \"action_forbidden_by_security_policy\": false,\n        \"log_lines_written_in_a_verbose_style\": true,\n        \"action_free_of_ethics_concerns\": true\n    }\n}",
  "question": "Proposed action: wait\nWould what the record shows make the proposed action the right call here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if owner_sign_off_required_for_this_action is true.\n2. cancel if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is above steps_used_hard_limit.\n3. wait if last_tool_output_verified is false.\nOtherwise: proceed.\nNever counted: task_description_complete, action_free_of_ethics_concerns, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa2d1cae65a",
  "kind": "yes/no",
  "text": "# request record\ndeploy_id=DEP-6882\nservice=notifier\ndeploy_blocked_by_security_policy=false\nfiles_changed=80\ndeploy_has_a_long_description=false\ndeploy_prohibited_during_the_audit_window=false\nservice_free_of_major_incidents=true\ncommit_messages_written_in_a_casual_tone=true\ncontract_customer_asked_for_a_say_in_this_rollout=false\ncommit_messages_written_in_a_terse_style=false\nfiles_changed_soft_limit=80\ncanary_results_incomplete=true\ndeploy_title_written_in_normal_case=true\nrollout_approval_revoked=false\nbackout_plan_documented=true",
  "question": "Proposed action: QJFN\nOverall, would you say the proposed action suits the request in the record?",
  "definitions": "Meanings:\n- JWF: stop this course of action at once\n- BC: forward the case to the designated decision maker\n- QJFN: hold off until the check has been completed by the team\n- S: proceed in accordance with the stated request\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0736952745",
  "kind": "yes/no",
  "text": "{\n  \"request\":{\n    \"request_id\":\"REQ-7782\",\n    \"requester\":\"Paolo Imai\"\n  },\n  \"figures\":{\n    \"access_days\":1,\n    \"access_days_approval_threshold\":60\n  },\n  \"checks\":{\n    \"requester_barred_from_this_system\":true,\n    \"request_grants_admin_rights\":false,\n    \"legal_preservation_order_on_the_account\":false,\n    \"requested_role_forbidden_by_policy\":false,\n    \"account_suspended\":false,\n    \"mfa_enrollment_incomplete\":false,\n    \"request_text_written_in_capital_letters\":false,\n    \"business_justification_missing\":false,\n    \"ethics_office_flagged_the_request\":false\n  }\n}",
  "question": "Proposed action: cancel\nHave the recorded facts ruled out the proposed action for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q318876c046",
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
  "qid": "q66529c6c3d",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-4515\nvendor=Riverbend Works\namount_approval_threshold=25000.00\namount=16489.36\nvendor_tax_form_missing=false\npayment_requested_during_business_hours=true\nawaiting_purchase_order=false\nduplicate_of_paid_invoice=false\nvendor_filed_a_legal_claim_over_this_invoice=false\nvendor_name_written_in_capital_letters=false\nvendor_free_of_sanctions=true\ninvoice_pdf_uses_a_landscape_layout=false\napprover_free_of_conflicts_of_interest=true",
  "question": "Proposed action: reject\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if approver_free_of_conflicts_of_interest is false.\n2. reject if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- escalate: escalate it so the person asking receives a decision\n- pay: continue with the request as nothing obstructs it\n- reject: block it right away\n- hold: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q822f9f87db",
  "kind": "choice",
  "text": "{\n  \"request\":{\n    \"run_id\":\"RUN-3737\",\n    \"agent\":\"indigo\"\n  },\n  \"figures\":{\n    \"steps_used\":61,\n    \"steps_used_hard_limit\":60\n  },\n  \"checks\":{\n    \"action_free_of_ethics_concerns\":false,\n    \"action_permitted_by_security_policy\":true,\n    \"task_description_complete\":true,\n    \"tool_output_shows_tampering\":false,\n    \"owner_sign_off_required_for_this_action\":false,\n    \"log_lines_written_in_a_compact_style\":true,\n    \"last_tool_output_unverified\":false\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 737 if owner_sign_off_required_for_this_action is true.\n2. 5877 if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is above steps_used_hard_limit.\n3. 1 if last_tool_output_unverified is true.\nOtherwise: 27.\nNever counted: task_description_complete, action_free_of_ethics_concerns, log_lines_written_in_a_compact_style.\nMeanings:\n- 1: be kept on hold until more information is supplied\n- 27: have the plan kept moving as it was requested\n- 5877: shut this down before it spreads into the workflow\n- 737: transfer the case to the responsible decision maker for determination\nThe record is complete: nothing else applies.\n\nAuditing the request, which of the actions below is the defensible choice?",
  "options": [
   "5877",
   "1",
   "27"
  ]
 },
 {
  "qid": "qec4eff5031",
  "kind": "yes/no",
  "text": "{\n    \"request_id\":\"REQ-3577\",\n    \"requester\":\"Priya Mensah\",\n    \"request_text_written_in_capital_letters\":true,\n    \"business_justification_provided\":true,\n    \"requested_role_forbidden_by_policy\":false,\n    \"access_days_approval_threshold\":14,\n    \"request_free_of_ethics_office_flags\":true,\n    \"mfa_enrollment_complete\":true,\n    \"access_days\":7,\n    \"requester_barred_from_this_system\":false,\n    \"account_suspended\":false,\n    \"legal_preservation_order_on_the_account\":false,\n    \"request_grants_admin_rights\":false\n}",
  "question": "Proposed action: quarantine\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. block_access if account_suspended is true or requested_role_forbidden_by_policy is true or request_grants_admin_rights is true.\n2. page_oncall if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. quarantine if business_justification_provided is false or mfa_enrollment_complete is false or requester_barred_from_this_system is true or request_free_of_ethics_office_flags is false.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- quarantine: park the file until the requester sends the document in\n- block_access: refuse this request entirely\n- allow: continue so the requester receives the result\n- page_oncall: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q57b3490e42",
  "kind": "choice",
  "text": "---\nrequest:\n    request_id: REQ-6321\n    requester: Sana Calloway\nfigures:\n    access_days_approval_threshold: 60\n    access_days: 60\nchecks:\n    business_justification_missing: false\n    account_suspended: false\n    requester_not_barred_from_this_system: true\n    legal_preservation_order_on_the_account: false\n    requested_role_forbidden_by_policy: true\n    request_grants_admin_rights: false\n    mfa_enrollment_incomplete: false\n    request_text_written_in_capital_letters: false\n    request_free_of_ethics_office_flags: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n2. refuse if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. refer to owner if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: grant.\nNever counted: request_free_of_ethics_office_flags, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nQuick question: which of the actions listed after this is the best call?",
  "options": [
   "refer to owner",
   "refuse",
   "grant"
  ]
 }
]
