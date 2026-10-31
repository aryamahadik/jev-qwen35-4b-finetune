# G5-H blind read T46-blind_read-03db7439-002 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r7a/T46/qc/g5h/answers/T46-blind_read-03db7439-002.json

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
  "qid": "q1e269a035c",
  "kind": "choice",
  "text": "{\n  \"record\":{\n    \"invoice_id\":\"INV-6425\",\n    \"vendor\":\"Riverbend Works\"\n  },\n  \"numbers\":{\n    \"amount\":357.35,\n    \"amount_approval_threshold\":500.00\n  },\n  \"flags\":{\n    \"duplicate_of_paid_invoice\":false,\n    \"invoice_pdf_uses_a_portrait_layout\":true,\n    \"vendor_name_written_in_capital_letters\":false,\n    \"payment_requested_during_business_hours\":false,\n    \"vendor_on_sanctions_list\":false,\n    \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n    \"vendor_tax_form_on_file\":true,\n    \"purchase_order_received\":true,\n    \"approver_free_of_conflicts_of_interest\":true\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if purchase_order_received is false.\n2. hand_to_a_person if vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. cancel_order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or approver_free_of_conflicts_of_interest is false or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- hand_to_a_person: transfer the case to the responsible decision maker for determination\n- release: run with this one\n- cancel_order: refuse this request entirely\n- delay: suspend progress until verification is received\nThe record is complete: nothing else applies.\n\nWhat would the requester most want done from the actions listed below?",
  "options": [
   "release",
   "delay",
   "cancel_order"
  ]
 },
 {
  "qid": "qbd348e8d9d",
  "kind": "choice",
  "text": "# case\nrequest_id: REQ-6460\nrequester: لمى سهيل الإدريسي\nnote: موافقة المدير المباشر موجودة على طلب الوصول.\nrequest_text_written_in_capital_letters: false\nrequest_grants_admin_rights: false\nlegal_preservation_order_on_the_account: false\naccess_days_approval_threshold: 60\nrequested_role_permitted_by_policy: true\nethics_office_flagged_the_request: false\nbusiness_justification_provided: true\naccount_suspended: false\naccess_days: 60\nmfa_enrollment_incomplete: false\nrequester_not_barred_from_this_system: true",
  "question": "Meanings:\n- refer_to_owner: pass this along to the decision maker\n- grant: execute the request exactly as written\n- pend: wait for the document to come through\n- refuse: reject this item since it violates the policy\nThe record is complete: nothing else applies.\n\nPicking from the actions listed, what best serves this request?",
  "options": [
   "grant",
   "refuse",
   "pend"
  ]
 },
 {
  "qid": "q0fe27baa48",
  "kind": "yes/no",
  "text": "# request record\ndeploy_id=DEP-4474\nservice=exporter\ndeploy_blocked_by_security_policy=false\nfiles_changed=50\ndeploy_has_a_long_description=false\ndeploy_prohibited_during_the_audit_window=false\nservice_free_of_major_incidents=true\ncontract_customer_asked_for_a_say_in_this_rollout=false\ncommit_messages_written_in_a_terse_style=false\nfiles_changed_soft_limit=50\ncanary_results_incomplete=false\nrollout_approval_revoked=false\nbackout_plan_documented=true",
  "question": "Proposed action: QJFN\nOverall, would you say the proposed action suits the request in the record?",
  "definitions": "Meanings:\n- JWF: stop this course of action at once\n- BC: forward the case to the designated decision maker\n- QJFN: hold off until the check has been completed by the team\n- S: proceed in accordance with the stated request\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4ca13e97f9",
  "kind": "yes/no",
  "text": "{\"deploy_id\":\"DEP-8699\",\"service\":\"profile\",\"files_changed\":15,\"rollout_approval_revoked\":false,\"deploy_has_a_long_description\":false,\"deploy_prohibited_during_the_audit_window\":false,\"backout_plan_missing\":false,\"canary_results_incomplete\":false,\"commit_messages_written_in_a_detailed_style\":true,\"service_free_of_major_incidents\":true,\"files_changed_soft_limit\":80,\"contract_customer_asked_for_a_say_in_this_rollout\":false,\"deploy_blocked_by_security_policy\":false}",
  "question": "Proposed action: go ahead\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_missing is true or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style.\nMeanings:\n- send to a person: hand this to the person who decides\n- turn down: leave the requester without the result they asked for\n- put on hold: park this until a record turns up\n- go ahead: keep it moving forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcdd39a58b3",
  "kind": "choice",
  "text": "ticket_id=TCK-1118\ncustomer=Marta Novak\nclaim_free_of_ombudsman_cases=true\nfree_of_legal_complaints=true\nclaim_form_filled_in_with_the_usual_font=true\nfree_of_safety_incident_reports=true\nproof_of_purchase_attached=true\nclaim_amount=100.00\nharmless_greeting_present_in_the_message=true\nclaim_amount_hard_limit=100.00\nclaim_involves_a_media_inquiry=false\nitem_return_received=true\nitem_excluded_by_policy=false",
  "question": "The record is complete: nothing else applies.\n\nThe facts point somewhere; which of the actions shown is supported by them?",
  "options": [
   "approve",
   "deny",
   "ask_manager"
  ]
 },
 {
  "qid": "q0a6e26cc38",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"invoice_id\": \"INV-6116\",\n        \"vendor\": \"Redwood Logistics\"\n    },\n    \"metrics\": {\n        \"amount_approval_threshold\": 2500.00,\n        \"amount\": 1562.42\n    },\n    \"signals\": {\n        \"approver_declared_a_conflict_of_interest\": false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": false,\n        \"awaiting_purchase_order\": true,\n        \"vendor_name_written_in_capital_letters\": true,\n        \"payment_requested_during_business_hours\": true,\n        \"vendor_on_sanctions_list\": true,\n        \"invoice_pdf_uses_a_landscape_layout\": false,\n        \"vendor_tax_form_missing\": false,\n        \"duplicate_of_paid_invoice\": false\n    }\n}",
  "question": "Proposed action: cancel order\nWould the proposed action be the right answer to what this request calls for?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand to a person if approver_declared_a_conflict_of_interest is true.\n2. cancel order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- delay: defer further action pending verification of the document\n- cancel order: kill this one off\n- hand to a person: hand it up to the person who decides\n- release: just crack on with it there is nothing in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q77629acfb8",
  "kind": "choice",
  "text": "{\n    \"subject\": {\n        \"invoice_id\": \"INV-9815\",\n        \"vendor\": \"Lakeshore Labs\"\n    },\n    \"amounts\": {\n        \"amount_approval_threshold\": 500.00,\n        \"amount\": 746.46\n    },\n    \"checks\": {\n        \"purchase_order_received\": true,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": false,\n        \"invoice_pdf_uses_a_portrait_layout\": true,\n        \"duplicate_of_paid_invoice\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"vendor_name_written_in_capital_letters\": false,\n        \"vendor_tax_form_missing\": false,\n        \"approver_free_of_conflicts_of_interest\": true,\n        \"vendor_on_sanctions_list\": false\n    }\n}",
  "question": "Meanings:\n- 7: refer the matter to the decision holder\n- 4434: end it so the requester sees their request closed\n- 96: keep it on hold for the missing document\n- 193: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "193",
   "7",
   "96"
  ]
 },
 {
  "qid": "qb2c1c7e879",
  "kind": "yes/no",
  "text": "---\n# extract\nrequest_id: REQ-8418\nrequester: فارس مهند الجبوري\nnote: صلاحية الوصول المطلوبة تتوافق مع دور الموظف الوظيفي.\naccess_days: 2\nrequester_barred_from_this_system: false\nrequest_grants_admin_rights: false\nlegal_preservation_order_on_the_account: false\nethics_office_flagged_the_request: false\nrequest_text_written_in_capital_letters: false\nbusiness_justification_missing: true\naccess_days_approval_threshold: 30\nmfa_enrollment_incomplete: false\nrequested_role_permitted_by_policy: true\naccount_suspended: false",
  "question": "Proposed action: defer\nUpon audit, is the proposed action the correct determination given the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if account_suspended is true or requested_role_permitted_by_policy is false or request_grants_admin_rights is true.\n2. ask manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. defer if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4558aac6d2",
  "kind": "yes/no",
  "text": "---\n# extract\ndeploy_id: DEP-2750\nservice: inventory\ncanary_results_complete: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\nfiles_changed_soft_limit: 50\ndeploy_blocked_by_security_policy: false\nfiles_changed: 51\ncommit_messages_written_in_a_terse_style: true\ndeploy_prohibited_during_the_audit_window: false\ndeploy_has_a_long_description: false\nbackout_plan_documented: true\nservice_free_of_major_incidents: true\nrollout_approval_revoked: false",
  "question": "Proposed action: put on hold\nIs it not true that the proposed action, as the file shows, is not a poor choice?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q4c483254fe",
  "kind": "choice",
  "text": "# record\nrequest_id | REQ-8950\nrequester | Mira Petrov\nlegal_preservation_order_on_the_account | false\nrequest_grants_admin_rights | true\naccess_days_approval_threshold | 45\nethics_office_flagged_the_request | false\nrequester_barred_from_this_system | false\nrequest_text_written_in_capital_letters | true\nmfa_enrollment_incomplete | false\naccess_days | 24\nrequested_role_forbidden_by_policy | false\naccount_suspended | true\nbusiness_justification_missing | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. block_access if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. page_oncall if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: allow.\nNever counted: ethics_office_flagged_the_request, request_text_written_in_capital_letters.\nMeanings:\n- page_oncall: transfer the case to the responsible decision maker for determination\n- block_access: reject the petition as the action is unauthorized\n- quarantine: be left pending until the review has been finished\n- allow: let this be advanced exactly as originally specified\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "allow",
   "block_access",
   "quarantine"
  ]
 },
 {
  "qid": "qeec85867bd",
  "kind": "yes/no",
  "text": "{\"run_id\": \"RUN-7030\", \"agent\": \"fjord\", \"log_lines_written_in_a_compact_style\": true, \"action_permitted_by_security_policy\": true, \"steps_used\": 12, \"last_tool_output_unverified\": false, \"tool_output_shows_tampering\": false, \"action_free_of_ethics_concerns\": true, \"task_description_incomplete\": false, \"owner_sign_off_required_for_this_action\": false, \"steps_used_hard_limit\": 16}",
  "question": "Proposed action: go_ahead\nIs it not correct that the proposed action is not mistaken on the items of the review sheet?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if action_free_of_ethics_concerns is false or owner_sign_off_required_for_this_action is true.\n2. put_on_hold if action_permitted_by_security_policy is false.\n3. turn_down if tool_output_shows_tampering is true or steps_used is above steps_used_hard_limit.\nOtherwise: go_ahead.\nNever counted: last_tool_output_unverified, task_description_incomplete, log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5e7edd04d9",
  "kind": "choice",
  "text": "{\n    \"deploy_id\":\"DEP-1106\",\n    \"service\":\"exporter\",\n    \"canary_results_incomplete\":true,\n    \"deploy_prohibited_during_the_audit_window\":false,\n    \"deploy_blocked_by_security_policy\":true,\n    \"files_changed_soft_limit\":50,\n    \"deploy_has_a_long_description\":false,\n    \"files_changed\":48,\n    \"service_free_of_major_incidents\":true,\n    \"contract_customer_asked_for_a_say_in_this_rollout\":false,\n    \"commit_messages_written_in_a_terse_style\":false,\n    \"backout_plan_missing\":false,\n    \"rollout_approval_revoked\":false\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. put on hold if canary_results_incomplete is true.\nOtherwise: go ahead.\nNever counted: backout_plan_missing, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_terse_style.\nThe record is complete: nothing else applies.\n\nWhich of these actions should be taken for this request?",
  "options": [
   "go ahead",
   "put on hold",
   "turn down"
  ]
 },
 {
  "qid": "qa1c4517a6f",
  "kind": "choice",
  "text": "---\n# case\ninvoice_id: INV-1993\nvendor: Cedar Group\napprover_declared_a_conflict_of_interest: false\nduplicate_of_paid_invoice: false\namount: 13419.03\nvendor_free_of_sanctions: true\nawaiting_purchase_order: false\namount_approval_threshold: 25000.00\nvendor_name_written_in_capital_letters: false\ninvoice_pdf_uses_a_landscape_layout: false\npayment_requested_during_business_hours: true\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_tax_form_missing: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if approver_declared_a_conflict_of_interest is true.\n2. turn_down if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "send_to_a_person"
  ]
 },
 {
  "qid": "q3a4039fcd4",
  "kind": "choice",
  "text": "---\n# record\nmeta:\n    deploy_id: \"DEP-9187\"\n    service: \"notifier\"\nmetrics:\n    files_changed: 3\n    files_changed_soft_limit: 30\nsignals:\n    backout_plan_missing: false\n    deploy_prohibited_during_the_audit_window: false\n    canary_results_complete: true\n    contract_customer_asked_for_a_say_in_this_rollout: false\n    rollout_approval_revoked: false\n    deploy_has_a_long_description: false\n    commit_messages_written_in_a_terse_style: true\n    deploy_blocked_by_security_policy: false\n    service_free_of_major_incidents: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. NMN if backout_plan_missing is true or files_changed is above files_changed_soft_limit.\n2. M if deploy_blocked_by_security_policy is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true.\n3. RJVH if service_free_of_major_incidents is false or contract_customer_asked_for_a_say_in_this_rollout is true.\nOtherwise: JC.\nNever counted: canary_results_complete, deploy_has_a_long_description, commit_messages_written_in_a_terse_style.\nMeanings:\n- NMN: be held back until a check or document arrives\n- M: stop the work since it cannot move forward\n- JC: have the task carried out as it was originally asked\n- RJVH: send it to whoever has the final say\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "NMN",
   "RJVH",
   "JC"
  ]
 },
 {
  "qid": "q96bed2066d",
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
  "qid": "qf3ea485596",
  "kind": "yes/no",
  "text": "---\nrequest_id: REQ-9339\nrequester: غسان مروان العلوي\nnote: قائمة الأنظمة المطلوب الوصول إليها لم تحدد بوضوح.\nrequester_not_barred_from_this_system: true\nbusiness_justification_missing: false\nlegal_preservation_order_on_the_account: false\naccess_days_approval_threshold: 30\nethics_office_flagged_the_request: false\nmfa_enrollment_incomplete: false\nrequest_text_written_in_capital_letters: false\naccess_days: 8\nrequest_grants_admin_rights: false\naccount_suspended: false\nrequested_role_forbidden_by_policy: false",
  "question": "Proposed action: pend\nIs the proposed action the right call, judging from what the record shows?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q3e82e16c37",
  "kind": "yes/no",
  "text": "{\"run_id\": \"RUN-8560\", \"agent\": \"garnet\", \"log_lines_written_in_a_verbose_style\": false, \"action_free_of_ethics_concerns\": true, \"action_forbidden_by_security_policy\": false, \"steps_used_hard_limit\": 40, \"last_tool_output_verified\": false, \"tool_output_shows_tampering\": false, \"task_description_complete\": true, \"steps_used\": 14, \"owner_sign_off_required_for_this_action\": false}",
  "question": "Proposed action: turn_down\nFrom an audit standpoint, have the facts in the record ruled out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q6f7af97a2a",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-1395\",\n  \"vendor\":\"Fairview Group\",\n  \"awaiting_purchase_order\":false,\n  \"vendor_tax_form_missing\":false,\n  \"vendor_free_of_sanctions\":true,\n  \"invoice_pdf_uses_a_landscape_layout\":false,\n  \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n  \"duplicate_of_paid_invoice\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"vendor_name_written_in_capital_letters\":false,\n  \"amount_approval_threshold\":1000.00,\n  \"approver_free_of_conflicts_of_interest\":true,\n  \"amount\":725.81\n}",
  "question": "Proposed action: hand_to_a_person\nIs it not the case that the proposed action is what the request and facts call for, and is not a poor choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. hand_to_a_person if vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. cancel_order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or approver_free_of_conflicts_of_interest is false or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- cancel_order: bin this idea and keep it out of the flow\n- release: proceed with the task as asked\n- delay: wait for the document to come through\n- hand_to_a_person: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8308583e81",
  "kind": "choice",
  "text": "---\n# request record\nrecord:\n    request_id: \"REQ-7856\"\n    requester: \"Lena Rossi\"\nnumbers:\n    access_days_approval_threshold: 30\n    access_days: 16\nflags:\n    ethics_office_flagged_the_request: false\n    mfa_enrollment_incomplete: false\n    account_suspended: false\n    request_grants_admin_rights: false\n    business_justification_provided: false\n    requester_not_barred_from_this_system: true\n    legal_preservation_order_on_the_account: false\n    request_text_written_in_capital_letters: false\n    requested_role_forbidden_by_policy: false",
  "question": "Meanings:\n- deny: be stopped and never carried out\n- ask_manager: route it elsewhere because a decider must weigh in\n- approve: continue so the requester receives the result\n- defer: stay put until the check is finished\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "defer",
   "deny",
   "approve"
  ]
 },
 {
  "qid": "q971767a4ce",
  "kind": "yes/no",
  "text": "run_id | RUN-4148\nagent | kestrel\ntool_output_shows_tampering | false\nsteps_used | 28\nlast_tool_output_unverified | true\naction_free_of_ethics_concerns | true\nsteps_used_hard_limit | 60\naction_permitted_by_security_policy | false\nlog_lines_written_in_a_compact_style | true\ntask_description_incomplete | false\nowner_sign_off_required_for_this_action | false",
  "question": "Proposed action: put on hold\nUpon audit, is the proposed action the correct determination given the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put on hold if last_tool_output_unverified is true or task_description_incomplete is true.\n3. turn down if action_permitted_by_security_policy is false or owner_sign_off_required_for_this_action is true or steps_used is above steps_used_hard_limit.\nOtherwise: go ahead.\nNever counted: log_lines_written_in_a_compact_style.\nMeanings:\n- send to a person: route this to the one who signs off\n- turn down: halt this item because the rules forbid it\n- put on hold: stay put until the check is finished\n- go ahead: carry out the request as written\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd4de39f3f5",
  "kind": "choice",
  "text": "ticket_id: TCK-1489\ncustomer: Leila Quispe\nitem_excluded_by_policy: false\nclaim_free_of_ombudsman_cases: true\nitem_return_received: true\nclaim_amount: 1421.92\nclaim_involves_a_media_inquiry: false\nharmless_greeting_present_in_the_message: true\nlegal_complaint_filed: false\nclaim_form_filled_in_with_the_usual_font: true\nclaim_amount_hard_limit: 2000.00\nproof_of_purchase_attached: true\nfree_of_safety_incident_reports: true",
  "question": "Meanings:\n- deny: reject this item since it violates the policy\n- approve: carry out the request as written\n- defer: pause here and wait for the check\n- ask_manager: route this to the one who signs off\nThe record is complete: nothing else applies.\n\nWhat is the best action to pick from the list for this request?",
  "options": [
   "ask_manager",
   "deny",
   "approve"
  ]
 },
 {
  "qid": "q0405caaa63",
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
  "qid": "q1ed2d6f124",
  "kind": "yes/no",
  "text": "# extract\nticket_id=TCK-2153\ncustomer=زياد نبيل الدوسري\nnote=الحالة بسيطة ومكتملة ولا تحتاج إلى تدخل إضافي.\nclaim_form_filled_in_with_the_usual_font=true\nclaim_involves_a_media_inquiry=false\nclaim_free_of_ombudsman_cases=true\nfree_of_safety_incident_reports=true\nitem_excluded_by_policy=false\nharmless_greeting_present_in_the_message=false\nlegal_complaint_filed=false\nclaim_amount_hard_limit=200.00\nclaim_amount=153.76\nproof_of_purchase_missing=false\nitem_return_received=true",
  "question": "Proposed action: send_to_a_person\nBe honest, is the proposed action the right call for what came in?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if item_return_received is false or free_of_safety_incident_reports is false.\n2. put_on_hold if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. send_to_a_person if proof_of_purchase_missing is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: go_ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3e10198a7b",
  "kind": "choice",
  "text": "# record\nticket_id | TCK-7633\ncustomer | طارق ناصر الجزائري\nnote | فاتورة الشراء مرفقة وتطابق ما ورد في الطلب.\nfree_of_safety_incident_reports | true\nitem_excluded_by_policy | true\nlegal_complaint_filed | false\nclaim_free_of_ombudsman_cases | true\nclaim_amount | 358.76\nclaim_form_filled_in_with_the_usual_font | true\nclaim_involves_a_media_inquiry | false\nclaim_amount_hard_limit | 500.00\nproof_of_purchase_attached | false\nharmless_greeting_present_in_the_message | true\nitem_return_not_yet_received | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if item_return_not_yet_received is true or free_of_safety_incident_reports is false.\n2. put_on_hold if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. send_to_a_person if proof_of_purchase_attached is false or legal_complaint_filed is true or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: go_ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- go_ahead: have the item pushed forward as the request stated\n- send_to_a_person: escalate this to the person who decides\n- put_on_hold: hold off until the check has been completed by the team\n- turn_down: reject the request in full\nThe record is complete: nothing else applies.\n\nWhat would the requester most want done from the actions listed below?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "put_on_hold"
  ]
 },
 {
  "qid": "q1abb974e0f",
  "kind": "yes/no",
  "text": "# extract\nrun_id=RUN-5763\nagent=ember\nsteps_used_hard_limit=16\nlast_tool_output_unverified=true\naction_forbidden_by_security_policy=false\ntask_description_complete=true\nowner_sign_off_required_for_this_action=false\naction_free_of_ethics_concerns=true\nsteps_used=12\nlog_lines_written_in_a_compact_style=true\ntool_output_shows_tampering=true",
  "question": "Proposed action: turn_down\nDo the request and the facts together rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if last_tool_output_unverified is true or action_free_of_ethics_concerns is false.\n2. turn_down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is at least steps_used_hard_limit.\n3. send_to_a_person if task_description_complete is false or owner_sign_off_required_for_this_action is true.\nOtherwise: go_ahead.\nNever counted: log_lines_written_in_a_compact_style.\nMeanings:\n- send_to_a_person: give it to the person in charge of the call\n- turn_down: skip this one, it is a hard pass for us\n- go_ahead: run the task as it was asked, with nothing standing between it and completion\n- put_on_hold: shelve the matter until more details come in\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe2bab7da42",
  "kind": "choice",
  "text": "# request record\nrequest_id: REQ-9087\nrequester: Yara Tanaka\nlegal_preservation_order_on_the_account: false\nrequested_role_permitted_by_policy: true\nrequest_text_written_in_capital_letters: false\nbusiness_justification_missing: true\naccount_suspended: false\nethics_office_flagged_the_request: false\nrequester_barred_from_this_system: false\nmfa_enrollment_complete: true\nrequest_grants_admin_rights: true\naccess_days: 46\naccess_days_approval_threshold: 45",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 83 if mfa_enrollment_complete is false or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\n2. 5 if account_suspended is true or requested_role_permitted_by_policy is false.\n3. 4742 if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: 726.\nNever counted: business_justification_missing, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- 5: reject the request in full\n- 83: hold off until the check clears\n- 726: continue as requested with the path fully open\n- 4742: pass this along to the decision maker\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "726",
   "4742",
   "83"
  ]
 },
 {
  "qid": "qf4d218c0e3",
  "kind": "choice",
  "text": "{\n    \"meta\": {\n        \"request_id\": \"REQ-2549\",\n        \"requester\": \"Yara Imai\"\n    },\n    \"metrics\": {\n        \"access_days_approval_threshold\": 30,\n        \"access_days\": 3\n    },\n    \"signals\": {\n        \"request_free_of_ethics_office_flags\": true,\n        \"account_suspended\": false,\n        \"legal_preservation_order_on_the_account\": true,\n        \"requester_not_barred_from_this_system\": true,\n        \"business_justification_missing\": false,\n        \"request_text_written_in_capital_letters\": false,\n        \"request_grants_admin_rights\": false,\n        \"mfa_enrollment_complete\": true,\n        \"requested_role_forbidden_by_policy\": false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if business_justification_missing is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n2. refer to owner if mfa_enrollment_complete is false or request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n3. refuse if account_suspended is true or requested_role_forbidden_by_policy is true.\nOtherwise: grant.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- refer to owner: give it to a person who has the authority to decide\n- grant: proceed in accordance with the stated request\n- pend: keep it on hold for the missing document\n- refuse: veto this move and leave it there\nThe record is complete: nothing else applies.\n\nLooking across the actions listed, what would be the correct response to this request?",
  "options": [
   "refuse",
   "grant",
   "pend"
  ]
 },
 {
  "qid": "qa0559d4761",
  "kind": "yes/no",
  "text": "# record\nrequest_id: REQ-8606\nrequester: Leila Vasquez\nrequester_barred_from_this_system: false\nrequested_role_permitted_by_policy: true\nlegal_preservation_order_on_the_account: false\nmfa_enrollment_complete: true\nrequest_free_of_ethics_office_flags: true\nrequest_text_written_in_capital_letters: true\naccount_suspended: true\nrequest_grants_admin_rights: false\naccess_days: 16\naccess_days_approval_threshold: 30\nbusiness_justification_missing: false",
  "question": "Proposed action: ask manager\nIs the proposed action the right step for the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if business_justification_missing is true or requested_role_permitted_by_policy is false.\n2. ask manager if mfa_enrollment_complete is false or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. deny if account_suspended is true or requester_barred_from_this_system is true.\nOtherwise: approve.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8aa1d9f7e1",
  "kind": "choice",
  "text": "# record\nrequest_id | REQ-9428\nrequester | Dana Anand\naccount_suspended | false\naccess_days_approval_threshold | 60\nrequested_role_forbidden_by_policy | false\nrequest_text_written_in_capital_letters | true\nrequest_free_of_ethics_office_flags | true\nmfa_enrollment_complete | true\nrequest_grants_admin_rights | false\nlegal_preservation_order_on_the_account | false\nrequester_barred_from_this_system | false\naccess_days | 55\nbusiness_justification_missing | true",
  "question": "The record is complete: nothing else applies.\n\nWhat do the facts support, and which of the actions listed follows from them?",
  "options": [
   "ask_manager",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q16e31983fb",
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
  "qid": "q63f734084d",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id = INV-7112\nvendor = Copperfield Industries\nvendor_tax_form_missing = false\namount_approval_threshold = 2500.00\npayment_requested_during_business_hours = true\namount = 2171.77\npurchase_order_received = true\ninvoice_pdf_uses_a_portrait_layout = true\nvendor_on_sanctions_list = false\napprover_declared_a_conflict_of_interest = false\nvendor_name_written_in_capital_letters = true\nduplicate_of_paid_invoice = false\nvendor_filed_a_legal_claim_over_this_invoice = false",
  "question": "Proposed action: go_ahead\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "Meanings:\n- send_to_a_person: hand this over to whoever has the final say\n- turn_down: halt the request at this point\n- put_on_hold: withhold action until supporting information is supplied\n- go_ahead: proceed in accordance with the stated request\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcc0ff0ab37",
  "kind": "yes/no",
  "text": "{\"request_id\": \"REQ-5140\", \"requester\": \"Yara Imai\", \"legal_preservation_order_on_the_account\": false, \"mfa_enrollment_incomplete\": false, \"requested_role_permitted_by_policy\": true, \"business_justification_missing\": false, \"access_days\": 47, \"access_days_approval_threshold\": 90, \"request_grants_admin_rights\": false, \"ethics_office_flagged_the_request\": false, \"request_text_written_in_capital_letters\": false, \"account_suspended\": false, \"requester_barred_from_this_system\": false}",
  "question": "Proposed action: refer to owner\nIs the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\n2. refuse if account_suspended is true or requested_role_permitted_by_policy is false.\n3. refer to owner if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: grant.\nNever counted: business_justification_missing, request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qac984c425c",
  "kind": "choice",
  "text": "# request record\nticket_id: TCK-4914\ncustomer: سامر لؤي الأيوبي\nnote: تم التحقق من الهوية وكل ما يتعلق بالطلب سليم.\nfree_of_safety_incident_reports: true\nclaim_form_filled_in_with_the_usual_font: true\nproof_of_purchase_attached: true\nlegal_complaint_filed: false\nclaim_amount: 119.40\nclaim_amount_hard_limit: 500.00\nitem_return_not_yet_received: true\nharmless_greeting_present_in_the_message: true\nclaim_involves_a_media_inquiry: false\nitem_excluded_by_policy: false\nclaim_free_of_ombudsman_cases: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false.\n2. deny if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_not_yet_received is true.\nOtherwise: approve.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nWhich of the listed actions is the right call for this request?",
  "options": [
   "deny",
   "approve",
   "ask manager"
  ]
 },
 {
  "qid": "qd7fde9fb46",
  "kind": "choice",
  "text": "---\n# request record\nsubject:\n  run_id: \"RUN-6915\"\n  agent: \"helix\"\namounts:\n  steps_used: 11\n  steps_used_hard_limit: 16\nchecks:\n  log_lines_written_in_a_verbose_style: false\n  action_free_of_ethics_concerns: true\n  action_forbidden_by_security_policy: true\n  tool_output_shows_tampering: false\n  last_tool_output_unverified: false\n  task_description_incomplete: false\n  owner_sign_off_required_for_this_action: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if owner_sign_off_required_for_this_action is true.\n2. turn_down if action_forbidden_by_security_policy is true.\n3. put_on_hold if last_tool_output_unverified is true or task_description_incomplete is true or action_free_of_ethics_concerns is false or steps_used is above steps_used_hard_limit.\nOtherwise: go_ahead.\nNever counted: tool_output_shows_tampering, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nWhich action listed below fits this request best?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "turn_down"
  ]
 },
 {
  "qid": "qe64b7ec331",
  "kind": "choice",
  "text": "# record\nrequest_id | REQ-6552\nrequester | نضال سمير الخوري\nnote | طلب الوصول قدمه الموظف بالطريقة الرسمية المعتمدة.\naccess_days_approval_threshold | 45\naccount_suspended | false\nrequest_text_written_in_capital_letters | true\nrequested_role_forbidden_by_policy | false\nrequest_grants_admin_rights | false\nrequest_free_of_ethics_office_flags | true\nlegal_preservation_order_on_the_account | true\naccess_days | 32\nbusiness_justification_missing | false\nrequester_not_barred_from_this_system | true\nmfa_enrollment_complete | true",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed should the team commit to for this request, as the manager?",
  "options": [
   "grant",
   "refer to owner",
   "refuse"
  ]
 },
 {
  "qid": "q2af26d3cf8",
  "kind": "choice",
  "text": "---\ncase:\n    deploy_id: \"DEP-6759\"\n    service: \"search\"\nvalues:\n    files_changed_soft_limit: 20\n    files_changed: 2\ntests:\n    deploy_has_a_long_description: false\n    rollout_approval_revoked: false\n    service_free_of_major_incidents: false\n    commit_messages_written_in_a_terse_style: true\n    backout_plan_documented: false\n    deploy_prohibited_during_the_audit_window: false\n    contract_customer_asked_for_a_say_in_this_rollout: false\n    canary_results_incomplete: false\n    deploy_blocked_by_security_policy: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\n2. turn down if rollout_approval_revoked is true.\n3. put on hold if canary_results_incomplete is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\nOtherwise: go ahead.\nNever counted: backout_plan_documented, deploy_has_a_long_description, commit_messages_written_in_a_terse_style.\nThe record is complete: nothing else applies.\n\nWhat would the requester most want done from the actions listed below?",
  "options": [
   "turn down",
   "send to a person",
   "go ahead"
  ]
 },
 {
  "qid": "qe01d51d0a1",
  "kind": "choice",
  "text": "# record\ninvoice_id: INV-1640\nvendor: Stonebridge Traders\nvendor_on_sanctions_list: false\ninvoice_pdf_uses_a_landscape_layout: false\nvendor_name_written_in_capital_letters: true\napprover_free_of_conflicts_of_interest: true\namount: 500.01\npurchase_order_received: true\nvendor_tax_form_on_file: true\nvendor_filed_a_legal_claim_over_this_invoice: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\namount_approval_threshold: 500.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. reject if vendor_on_sanctions_list is true or approver_free_of_conflicts_of_interest is false.\n2. escalate if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. hold if purchase_order_received is false or amount is at least amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the listed actions do the facts support as the right call?",
  "options": [
   "hold",
   "pay",
   "reject"
  ]
 },
 {
  "qid": "qf0d0dd623d",
  "kind": "yes/no",
  "text": "# extract\nticket_id = TCK-9058\ncustomer = Leila Okafor\nitem_excluded_by_policy = false\nitem_return_received = false\nclaim_amount_hard_limit = 2000.00\nclaim_free_of_ombudsman_cases = true\nlegal_complaint_filed = false\nproof_of_purchase_attached = false\nharmless_greeting_present_in_the_message = true\nclaim_involves_a_media_inquiry = false\nfree_of_safety_incident_reports = true\nclaim_amount = 542.52\nclaim_form_filled_in_with_the_usual_font = true",
  "question": "Proposed action: go ahead\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if claim_amount is at least claim_amount_hard_limit.\n2. send to a person if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. put on hold if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: go ahead.\nNever counted: item_return_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- send to a person: kick it up to whoever makes the call\n- turn down: refuse to act since the step is prohibited\n- put on hold: withhold action until supporting information is supplied\n- go ahead: proceed with the task as asked\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6bcd58e15c",
  "kind": "yes/no",
  "text": "{\n    \"meta\":{\n        \"invoice_id\":\"INV-7085\",\n        \"vendor\":\"Harbor Works\"\n    },\n    \"metrics\":{\n        \"amount\":10335.11,\n        \"amount_approval_threshold\":25000.00\n    },\n    \"signals\":{\n        \"approver_declared_a_conflict_of_interest\":false,\n        \"vendor_free_of_sanctions\":false,\n        \"invoice_pdf_uses_a_portrait_layout\":true,\n        \"vendor_tax_form_missing\":false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n        \"purchase_order_received\":true,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_name_written_in_capital_letters\":true,\n        \"duplicate_of_paid_invoice\":false\n    }\n}",
  "question": "Proposed action: hold\nIs the proposed action not a sound choice for this situation?",
  "definitions": "Meanings:\n- reject: end this effort right away\n- escalate: get sent upward to the one who decides\n- pay: keep going with it nothing is blocking you\n- hold: withhold action until supporting information is supplied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe9cbaa09f6",
  "kind": "choice",
  "text": "# record\ndeploy_id: DEP-5587\nservice: inventory\nfiles_changed: 20\nrollout_approval_revoked: false\ndeploy_blocked_by_security_policy: false\ncontract_customer_asked_for_a_say_in_this_rollout: false\nfiles_changed_soft_limit: 20\nbackout_plan_missing: false\ndeploy_prohibited_during_the_audit_window: false\ndeploy_has_a_long_description: false\ncanary_results_complete: true\nservice_free_of_major_incidents: true\ncommit_messages_written_in_a_terse_style: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 51 if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. 1 if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. 353 if canary_results_complete is false.\nOtherwise: 8222.\nNever counted: backout_plan_missing, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_terse_style.\nMeanings:\n- 1: block it right away\n- 51: route the request to the decision maker\n- 353: chill until the document turns up\n- 8222: continue as requested with the path fully open\nThe record is complete: nothing else applies.\n\nWhich of these actions should we take for this request?",
  "options": [
   "353",
   "8222",
   "51"
  ]
 },
 {
  "qid": "qc7e5d28100",
  "kind": "yes/no",
  "text": "{\n  \"subject\": {\n    \"ticket_id\": \"TCK-1104\",\n    \"customer\": \"Nadia Okonkwo\"\n  },\n  \"amounts\": {\n    \"claim_amount\": 464.29,\n    \"claim_amount_hard_limit\": 1000.00\n  },\n  \"checks\": {\n    \"claim_involves_a_media_inquiry\": false,\n    \"item_return_received\": true,\n    \"claim_form_filled_in_with_the_usual_font\": true,\n    \"item_excluded_by_policy\": false,\n    \"free_of_safety_incident_reports\": false,\n    \"free_of_legal_complaints\": true,\n    \"harmless_greeting_present_in_the_message\": true,\n    \"claim_free_of_ombudsman_cases\": true,\n    \"proof_of_purchase_attached\": true\n  }\n}",
  "question": "Proposed action: QRLB\nDoes the record itself rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QRLB if free_of_safety_incident_reports is false.\n2. XWZ if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. XX if item_return_received is false.\nOtherwise: P.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- XWZ: reject this item since it violates the policy\n- XX: postpone proceeding until the check is completed\n- P: just crack on with it there is nothing in the way\n- QRLB: hand it up to the person who decides\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4f261b0c05",
  "kind": "yes/no",
  "text": "---\ndeploy_id: \"DEP-4882\"\nservice: \"ledger\"\ndeploy_has_a_long_description: false\nfiles_changed: 18\ncontract_customer_asked_for_a_say_in_this_rollout: false\nservice_free_of_major_incidents: true\nrollout_approval_revoked: false\ncommit_messages_written_in_a_detailed_style: false\ndeploy_blocked_by_security_policy: false\ndeploy_prohibited_during_the_audit_window: true\nfiles_changed_soft_limit: 30\nbackout_plan_documented: true\ncanary_results_complete: false",
  "question": "Proposed action: put_on_hold\nBe honest, do the facts here rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. turn_down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. put_on_hold if canary_results_complete is false.\nOtherwise: go_ahead.\nNever counted: backout_plan_documented, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style.\nMeanings:\n- put_on_hold: be kept on hold until more information is supplied\n- turn_down: scrap the plan and drop this request\n- go_ahead: let this be advanced exactly as originally specified\n- send_to_a_person: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4a4db7b74c",
  "kind": "choice",
  "text": "# request record\nrun_id                                  | RUN-6693\nagent                                   | atlas\nsteps_used                              | 27\ntool_output_shows_tampering             | false\ntask_description_incomplete             | false\nlog_lines_written_in_a_verbose_style    | true\naction_free_of_ethics_concerns          | true\nlast_tool_output_unverified             | false\nowner_sign_off_required_for_this_action | true\naction_permitted_by_security_policy     | true\nsteps_used_hard_limit                   | 60",
  "question": "Meanings:\n- go_ahead: run the task as it was asked, with nothing standing between it and completion\n- send_to_a_person: hand this to the person who decides\n- put_on_hold: pause and collect more information first\n- turn_down: bin this idea and keep it out of the flow\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the most suitable for the request?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "put_on_hold"
  ]
 },
 {
  "qid": "q8a8b419b49",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-2783\", \"vendor\": \"Fairview Supply\", \"duplicate_of_paid_invoice\": false, \"vendor_on_sanctions_list\": false, \"payment_requested_during_business_hours\": true, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"approver_declared_a_conflict_of_interest\": false, \"awaiting_purchase_order\": false, \"vendor_tax_form_on_file\": true, \"amount_approval_threshold\": 500.00, \"vendor_name_written_in_capital_letters\": false, \"amount\": 537.03, \"invoice_pdf_uses_a_landscape_layout\": false}",
  "question": "Meanings:\n- DRC: be blocked outright so it never gets carried out\n- W: go on and finish it the path is clear\n- GW: sit on it till the doc shows up\n- BBCR: route it elsewhere because a decider must weigh in\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "BBCR",
   "DRC",
   "GW"
  ]
 },
 {
  "qid": "qa1fd8f5cf7",
  "kind": "choice",
  "text": "---\nticket_id: \"TCK-6909\"\ncustomer: \"Ravi Duarte\"\nharmless_greeting_present_in_the_message: true\nclaim_involves_a_media_inquiry: false\nclaim_amount: 1999.99\nfree_of_safety_incident_reports: true\nproof_of_purchase_attached: true\nitem_excluded_by_policy: false\nitem_return_not_yet_received: false\nclaim_amount_hard_limit: 2000.00\nlegal_complaint_filed: false\nclaim_form_filled_in_with_the_usual_font: true\nclaim_free_of_ombudsman_cases: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if claim_amount is at least claim_amount_hard_limit.\n2. send to a person if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. put on hold if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: go ahead.\nNever counted: item_return_not_yet_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- put on hold: pause this until the requester supplies the missing document\n- turn down: stop this course of action at once\n- go ahead: continue as requested with the path fully open\n- send to a person: send it onward because someone else must decide\nThe record is complete: nothing else applies.\n\nGiven the details in the record, which action listed would be the correct decision?",
  "options": [
   "go ahead",
   "turn down",
   "send to a person"
  ]
 },
 {
  "qid": "q4a9a2bc7d2",
  "kind": "yes/no",
  "text": "---\n# record\nticket_id: TCK-9742\ncustomer: Mira Mensah\nfree_of_safety_incident_reports: false\nitem_excluded_by_policy: false\nitem_return_received: true\nclaim_form_filled_in_with_the_usual_font: true\nclaim_free_of_ombudsman_cases: true\nclaim_amount: 1166.55\nclaim_involves_a_media_inquiry: false\nproof_of_purchase_attached: true\nfree_of_legal_complaints: true\nclaim_amount_hard_limit: 2000.00\nharmless_greeting_present_in_the_message: true",
  "question": "Proposed action: put_on_hold\nIs it not correct that the evidence points toward the proposed action, and it is not a poor choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. put_on_hold if proof_of_purchase_attached is false or claim_involves_a_media_inquiry is true.\n3. send_to_a_person if item_return_received is false or free_of_legal_complaints is false or free_of_safety_incident_reports is false.\nOtherwise: go_ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd4a5fb33a8",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-2488\",\"vendor\":\"Ironleaf Logistics\",\"duplicate_of_paid_invoice\":false,\"invoice_pdf_uses_a_landscape_layout\":false,\"awaiting_purchase_order\":false,\"amount_approval_threshold\":1000.00,\"vendor_filed_a_legal_claim_over_this_invoice\":false,\"amount\":688.31,\"vendor_tax_form_missing\":false,\"approver_declared_a_conflict_of_interest\":false,\"payment_requested_during_business_hours\":false,\"vendor_name_written_in_capital_letters\":false,\"vendor_on_sanctions_list\":false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. cancel order if vendor_on_sanctions_list is true.\n3. hand to a person if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "cancel order",
   "release",
   "hand to a person"
  ]
 },
 {
  "qid": "qa19349cd7f",
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
  "qid": "qb167b307b5",
  "kind": "yes/no",
  "text": "ticket_id | TCK-6993\ncustomer | Felix Brandt\nitem_excluded_by_policy | false\nclaim_involves_a_media_inquiry | false\nclaim_free_of_ombudsman_cases | true\nfree_of_safety_incident_reports | true\nclaim_form_filled_in_with_the_usual_font | true\nclaim_amount | 799.30\nitem_return_not_yet_received | false\nclaim_amount_hard_limit | 2000.00\nproof_of_purchase_attached | true\nharmless_greeting_present_in_the_message | true\nfree_of_legal_complaints | true",
  "question": "Proposed action: go ahead\nDoes the record back up the proposed action as the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if item_return_not_yet_received is true or free_of_safety_incident_reports is false.\n2. put on hold if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. send to a person if proof_of_purchase_attached is false or free_of_legal_complaints is false or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: go ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- go ahead: press on with the work as originally set\n- put on hold: defer the step until the verification is in\n- turn down: toss it out, we are never doing this\n- send to a person: be handed over to the deciding person\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q85e82c9d2e",
  "kind": "yes/no",
  "text": "{\n    \"request_id\":\"REQ-2273\",\n    \"requester\":\"وفاء محسن الفارس\",\n    \"note\":\"موافقة المدير المباشر موجودة على طلب الوصول.\",\n    \"request_text_written_in_capital_letters\":false,\n    \"request_free_of_ethics_office_flags\":true,\n    \"business_justification_provided\":true,\n    \"request_grants_admin_rights\":false,\n    \"account_suspended\":false,\n    \"mfa_enrollment_incomplete\":false,\n    \"access_days_approval_threshold\":30,\n    \"requester_barred_from_this_system\":false,\n    \"legal_preservation_order_on_the_account\":false,\n    \"access_days\":4,\n    \"requested_role_forbidden_by_policy\":false\n}",
  "question": "Proposed action: JCM\nAs a reviewer checking the file, is the proposed action not a sound decision here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. JCM if mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or request_free_of_ethics_office_flags is false.\n2. J if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. DVNF if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: WK.\nNever counted: business_justification_provided, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- WK: proceed with the task as asked\n- DVNF: direct the request to the responsible decider\n- JCM: stay on hold until the paperwork arrives\n- J: halt the request at this point\nThe record is complete: nothing else applies."
 }
]
