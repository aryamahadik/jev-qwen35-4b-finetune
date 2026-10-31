# G5-H blind read T46-blind_read-03db7439-000 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r7a/T46/qc/g5h/answers/T46-blind_read-03db7439-000.json

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
  "qid": "q467c538c44",
  "kind": "yes/no",
  "text": "{\"run_id\": \"RUN-8548\", \"agent\": \"kestrel\", \"tool_output_shows_tampering\": false, \"owner_sign_off_required_for_this_action\": false, \"action_permitted_by_security_policy\": true, \"last_tool_output_verified\": true, \"task_description_complete\": true, \"action_free_of_ethics_concerns\": true, \"steps_used_hard_limit\": 8, \"log_lines_written_in_a_verbose_style\": true, \"steps_used\": 4}",
  "question": "Proposed action: VHTT\nIs it not so that the proposed action, per what is logged, is not a bad fit?",
  "definitions": "Meanings:\n- BV: get referred to the person who decides\n- VHTT: go on and finish it the path is clear\n- G: scrap the plan and drop this request\n- VGT: keep their request on hold until more information arrives from them\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q59b8bb361a",
  "kind": "yes/no",
  "text": "---\nrequest_id: REQ-9339\nrequester: غسان مروان العلوي\nnote: قائمة الأنظمة المطلوب الوصول إليها لم تحدد بوضوح.\nrequester_not_barred_from_this_system: true\nbusiness_justification_missing: false\nlegal_preservation_order_on_the_account: false\naccess_days_approval_threshold: 30\nethics_office_flagged_the_request: false\nmfa_enrollment_incomplete: false\nrequest_text_written_in_capital_letters: false\naccess_days: 8\nrequest_grants_admin_rights: false\naccount_suspended: false\nrequested_role_forbidden_by_policy: false",
  "question": "Proposed action: pend\nHas the record ruled out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q6f55590325",
  "kind": "choice",
  "text": "{\n  \"record\":{\n    \"invoice_id\":\"INV-4779\",\n    \"vendor\":\"Harbor Traders\"\n  },\n  \"numbers\":{\n    \"amount\":164.11,\n    \"amount_approval_threshold\":500.00\n  },\n  \"flags\":{\n    \"vendor_on_sanctions_list\":false,\n    \"invoice_pdf_uses_a_landscape_layout\":false,\n    \"payment_requested_during_business_hours\":true,\n    \"vendor_tax_form_missing\":false,\n    \"purchase_order_received\":true,\n    \"duplicate_of_paid_invoice\":false,\n    \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n    \"approver_free_of_conflicts_of_interest\":false,\n    \"vendor_name_written_in_capital_letters\":false\n  }\n}",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed after this, which is the fitting call for the request?",
  "options": [
   "pay",
   "escalate",
   "reject"
  ]
 },
 {
  "qid": "q71df0aefa4",
  "kind": "choice",
  "text": "---\n# record\nrecord:\n  run_id: RUN-7650\n  agent: atlas\nnumbers:\n  steps_used: 2\n  steps_used_hard_limit: 12\nflags:\n  action_free_of_ethics_concerns: false\n  tool_output_shows_tampering: true\n  log_lines_written_in_a_verbose_style: false\n  action_permitted_by_security_policy: true\n  task_description_complete: true\n  owner_sign_off_required_for_this_action: false\n  last_tool_output_verified: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if owner_sign_off_required_for_this_action is true.\n2. turn_down if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is above steps_used_hard_limit.\n3. put_on_hold if last_tool_output_verified is false.\nOtherwise: go_ahead.\nNever counted: task_description_complete, action_free_of_ethics_concerns, log_lines_written_in_a_verbose_style.\nMeanings:\n- go_ahead: continue with what was requested\n- turn_down: kill this one off, it is off the table for good\n- put_on_hold: chill until the document turns up\n- send_to_a_person: give it to a person who has the authority to decide\nThe record is complete: nothing else applies.\n\nChecklist: which of the actions listed below best answers the request?",
  "options": [
   "turn_down",
   "put_on_hold",
   "go_ahead"
  ]
 },
 {
  "qid": "qc19e299077",
  "kind": "choice",
  "text": "# record\ndeploy_id | DEP-4061\nservice | catalog\nservice_free_of_major_incidents | true\ncommit_messages_written_in_a_detailed_style | false\nbackout_plan_missing | true\ncontract_customer_asked_for_a_say_in_this_rollout | false\ncanary_results_complete | true\ndeploy_blocked_by_security_policy | false\ndeploy_prohibited_during_the_audit_window | false\nfiles_changed | 6\nrollout_approval_revoked | false\nfiles_changed_soft_limit | 15\ndeploy_has_a_long_description | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if backout_plan_missing is true or rollout_approval_revoked is true or files_changed is at least files_changed_soft_limit.\n2. send_to_a_person if contract_customer_asked_for_a_say_in_this_rollout is true.\n3. turn_down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\nOtherwise: go_ahead.\nNever counted: canary_results_complete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style.\nThe record is complete: nothing else applies.\n\nThe record shows the situation; which of the actions listed is the right call?",
  "options": [
   "put_on_hold",
   "go_ahead",
   "turn_down"
  ]
 },
 {
  "qid": "qa345e1a02f",
  "kind": "choice",
  "text": "---\nticket_id: TCK-8201\ncustomer: Mira Mensah\nitem_excluded_by_policy: false\nclaim_amount: 467.33\nharmless_greeting_present_in_the_message: true\nclaim_amount_hard_limit: 1000.00\nclaim_free_of_ombudsman_cases: true\nproof_of_purchase_missing: false\nfree_of_legal_complaints: true\nclaim_involves_a_media_inquiry: false\nitem_return_received: true\nclaim_form_filled_in_with_the_usual_font: true\nfree_of_safety_incident_reports: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. turn_down if item_excluded_by_policy is true or free_of_legal_complaints is false or claim_amount is above claim_amount_hard_limit.\n3. send_to_a_person if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: go_ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed would you sign off on for this request, as the manager?",
  "options": [
   "turn_down",
   "put_on_hold",
   "go_ahead"
  ]
 },
 {
  "qid": "q0e4a8dec07",
  "kind": "yes/no",
  "text": "request_id: REQ-5114\nrequester: صالح كمال الهاشمي\nnote: الموظف مسجل في النظام وطلبه لا يحتاج إلى مراجعة إضافية.\naccount_suspended: false\naccess_days: 55\nbusiness_justification_missing: false\naccess_days_approval_threshold: 60\nethics_office_flagged_the_request: false\nrequest_text_written_in_capital_letters: false\nrequested_role_forbidden_by_policy: false\nlegal_preservation_order_on_the_account: false\nmfa_enrollment_incomplete: false\nrequest_grants_admin_rights: false\nrequester_not_barred_from_this_system: false",
  "question": "Proposed action: block_access\nReviewing this as an auditor, do the record's facts rule out the proposed action for the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_missing is true or requested_role_forbidden_by_policy is true.\n2. page_oncall if mfa_enrollment_incomplete is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is at least access_days_approval_threshold.\n3. block_access if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: allow.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- allow: let the request be continued as originally asked\n- quarantine: suspend progress until verification is received\n- block_access: drop this request from the queue\n- page_oncall: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q197f9880ae",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- deploy id: DEP-1936\n- service: billing\n- contract customer asked for a say in this rollout: no\n- commit messages written in a detailed style: yes\n- files changed: 65\n- canary results complete: yes\n- deploy blocked by security policy: no\n- rollout approval revoked: no\n- files changed soft limit: 80\n- backout plan documented: yes\n- deploy prohibited during the audit window: yes\n- service free of major incidents: yes\n- deploy has a long description: yes",
  "question": "Meanings:\n- put_on_hold: hold off until the check has been completed by the team\n- send_to_a_person: delegate the call to whoever holds authority\n- turn_down: send the requester away with the request left unfinished\n- go_ahead: continue the work as originally asked, there is nothing in the way\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "send_to_a_person",
   "turn_down",
   "go_ahead"
  ]
 },
 {
  "qid": "qce81721ff4",
  "kind": "choice",
  "text": "{\n  \"invoice_id\": \"INV-8709\",\n  \"vendor\": \"Stonebridge Partners\",\n  \"awaiting_purchase_order\": false,\n  \"vendor_name_written_in_capital_letters\": true,\n  \"invoice_pdf_uses_a_landscape_layout\": false,\n  \"approver_free_of_conflicts_of_interest\": true,\n  \"duplicate_of_paid_invoice\": false,\n  \"vendor_filed_a_legal_claim_over_this_invoice\": false,\n  \"amount_approval_threshold\": 500.00,\n  \"amount\": 311.43,\n  \"vendor_on_sanctions_list\": false,\n  \"payment_requested_during_business_hours\": true,\n  \"vendor_tax_form_on_file\": true\n}",
  "question": "Meanings:\n- cancel_order: terminate the process as continuation is prohibited\n- delay: hold the request until the check is done\n- release: continue so the requester receives the result\n- hand_to_a_person: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "delay",
   "cancel_order",
   "release"
  ]
 },
 {
  "qid": "qcf3931bcc7",
  "kind": "yes/no",
  "text": "---\n# record\ndeploy_id: \"DEP-3742\"\nservice: \"mailer\"\nservice_free_of_major_incidents: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_prohibited_during_the_audit_window: false\ncanary_results_incomplete: false\nfiles_changed_soft_limit: 30\nbackout_plan_missing: false\nrollout_approval_revoked: false\nfiles_changed: 13\ndeploy_blocked_by_security_policy: false\ncommit_messages_written_in_a_terse_style: false\ndeploy_has_a_long_description: false",
  "question": "Proposed action: put_on_hold\nSeen against the request in the record, would the proposed action be the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q7b3647fcd9",
  "kind": "yes/no",
  "text": "{\n    \"subject\":{\n        \"invoice_id\":\"INV-9551\",\n        \"vendor\":\"Riverbend Systems\"\n    },\n    \"amounts\":{\n        \"amount\":591.08,\n        \"amount_approval_threshold\":1000.00\n    },\n    \"checks\":{\n        \"vendor_name_written_in_capital_letters\":false,\n        \"invoice_pdf_uses_a_landscape_layout\":true,\n        \"purchase_order_received\":true,\n        \"approver_free_of_conflicts_of_interest\":true,\n        \"vendor_free_of_sanctions\":true,\n        \"duplicate_of_paid_invoice\":false,\n        \"vendor_tax_form_missing\":false,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_filed_a_legal_claim_over_this_invoice\":false\n    }\n}",
  "question": "Proposed action: approve\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if vendor_filed_a_legal_claim_over_this_invoice is true or approver_free_of_conflicts_of_interest is false or amount is at least amount_approval_threshold.\n2. defer if purchase_order_received is false or vendor_tax_form_missing is true.\n3. deny if duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- deny: block it right away\n- ask_manager: escalate this to the person who decides\n- approve: continue with the request as nothing obstructs it\n- defer: sit on it till the doc shows up\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q08ce44017f",
  "kind": "choice",
  "text": "# case\nticket_id: TCK-3405\ncustomer: Yara Novak\nproof_of_purchase_missing: true\nfree_of_legal_complaints: true\nitem_excluded_by_policy: false\nitem_return_received: true\nclaim_amount_hard_limit: 100.00\nharmless_greeting_present_in_the_message: true\nclaim_free_of_ombudsman_cases: false\nfree_of_safety_incident_reports: false\nclaim_involves_a_media_inquiry: false\nclaim_amount: 83.11\nclaim_form_filled_in_with_the_usual_font: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if free_of_safety_incident_reports is false.\n2. turn down if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. put on hold if item_return_received is false.\nOtherwise: go ahead.\nNever counted: proof_of_purchase_missing, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- put on hold: stall the request until the check comes back\n- send to a person: refer this item to the person who holds decision authority\n- turn down: ditch the whole thing, nobody should act on it\n- go ahead: finish it so the requester has their answer\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "go ahead",
   "put on hold",
   "send to a person"
  ]
 },
 {
  "qid": "q0546b4b58c",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- run id: RUN-8325\n- agent: helix\n- owner sign off required for this action: no\n- action free of ethics concerns: yes\n- tool output shows tampering: no\n- log lines written in a compact style: no\n- action permitted by security policy: yes\n- last tool output verified: yes\n- steps used: 18\n- task description incomplete: no\n- steps used hard limit: 30",
  "question": "Proposed action: 7\nIs it not true that the proposed action is not out of line with the ask?",
  "definitions": "Meanings:\n- 154: run with it carry on as you were\n- 10: ditch the whole thing, nobody should act on it\n- 7: withhold action until supporting information is supplied\n- 7834: escalate the matter to the accountable decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0f7f0c2889",
  "kind": "yes/no",
  "text": "---\nrequest:\n    run_id: RUN-8387\n    agent: delta\nfigures:\n    steps_used: 6\n    steps_used_hard_limit: 8\nchecks:\n    last_tool_output_verified: true\n    task_description_complete: true\n    owner_sign_off_required_for_this_action: false\n    log_lines_written_in_a_verbose_style: false\n    tool_output_shows_tampering: false\n    action_free_of_ethics_concerns: false\n    action_forbidden_by_security_policy: false",
  "question": "Proposed action: turn down\nAuditing this request closely, is the proposed action not a defensible choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put on hold if task_description_complete is false or steps_used is above steps_used_hard_limit.\n3. send to a person if action_forbidden_by_security_policy is true or owner_sign_off_required_for_this_action is true.\nOtherwise: go ahead.\nNever counted: last_tool_output_verified, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q86e4ee520e",
  "kind": "choice",
  "text": "# record\nrequest_id | REQ-3300\nrequester | Omar Castell\nrequest_text_written_in_capital_letters | false\nrequest_grants_admin_rights | false\nrequest_free_of_ethics_office_flags | true\nrequester_not_barred_from_this_system | true\naccess_days_approval_threshold | 7\nbusiness_justification_provided | true\naccount_suspended | false\nrequested_role_permitted_by_policy | true\nmfa_enrollment_complete | true\nlegal_preservation_order_on_the_account | false\naccess_days | 10",
  "question": "Meanings:\n- page oncall: transfer the case to the responsible decision maker for determination\n- block access: skip this one, it is a hard pass for us\n- quarantine: park the file until the requester sends the document in\n- allow: carry out the request as written\nThe record is complete: nothing else applies.\n\nWhich of the actions below does the record point to as the right call?",
  "options": [
   "allow",
   "page oncall",
   "quarantine"
  ]
 },
 {
  "qid": "qcee94f4e14",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-8824\", \"vendor\": \"Riverbend Foods\", \"vendor_tax_form_missing\": true, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"amount_approval_threshold\": 25000.00, \"approver_free_of_conflicts_of_interest\": true, \"payment_requested_during_business_hours\": true, \"vendor_free_of_sanctions\": true, \"awaiting_purchase_order\": false, \"duplicate_of_paid_invoice\": false, \"vendor_name_written_in_capital_letters\": false, \"invoice_pdf_uses_a_landscape_layout\": false, \"amount\": 23943.73}",
  "question": "Proposed action: defer\nDoes the proposed action not fit what this request needs?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qada5d8ad90",
  "kind": "choice",
  "text": "---\n# record\ninvoice_id: \"INV-6901\"\nvendor: \"Ironleaf Logistics\"\nduplicate_of_paid_invoice: false\napprover_free_of_conflicts_of_interest: true\nawaiting_purchase_order: false\nvendor_filed_a_legal_claim_over_this_invoice: false\namount_approval_threshold: 25000.00\nvendor_name_written_in_capital_letters: false\nvendor_on_sanctions_list: false\namount: 13281.25\npayment_requested_during_business_hours: true\ninvoice_pdf_uses_a_landscape_layout: false\nvendor_tax_form_missing: false",
  "question": "Meanings:\n- deny: kill this one off, it is off the table for good\n- approve: proceed as asked since everything is cleared\n- defer: wait for the document to come through\n- ask manager: route it elsewhere because a decider must weigh in\nThe record is complete: nothing else applies.\n\nConsidering what was asked and the facts available, which action below should be chosen?",
  "options": [
   "approve",
   "ask manager",
   "defer"
  ]
 },
 {
  "qid": "q93270b3b9d",
  "kind": "yes/no",
  "text": "# extract\nrun_id = RUN-9663\nagent = delta\nlast_tool_output_verified = false\nsteps_used_hard_limit = 16\nlog_lines_written_in_a_compact_style = true\nsteps_used = 4\naction_forbidden_by_security_policy = false\ntool_output_shows_tampering = false\nowner_sign_off_required_for_this_action = false\naction_free_of_ethics_concerns = true\ntask_description_incomplete = false",
  "question": "Proposed action: put_on_hold\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- send_to_a_person: route this matter to the individual empowered to decide\n- turn_down: withdraw from the step as it is forbidden\n- go_ahead: execute the requested action as nothing prevents it\n- put_on_hold: hold the request until the check is done\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6b2e9e4ffb",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-7020\n- vendor: Riverbend Partners\n- duplicate of paid invoice: yes\n- awaiting purchase order: no\n- vendor tax form missing: no\n- vendor filed a legal claim over this invoice: no\n- payment requested during business hours: yes\n- approver free of conflicts of interest: yes\n- vendor name written in capital letters: no\n- invoice pdf uses a landscape layout: no\n- amount approval threshold: 500.00\n- vendor on sanctions list: no\n- amount: 462.53",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions below answers the request given the facts you can see?",
  "options": [
   "reject",
   "escalate",
   "pay"
  ]
 },
 {
  "qid": "qa35701207a",
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
  "qid": "q0abec323d1",
  "kind": "choice",
  "text": "request_id=REQ-2166\nrequester=Lena Petrov\naccount_suspended=false\nmfa_enrollment_complete=true\nrequester_not_barred_from_this_system=true\naccess_days=38\nrequested_role_permitted_by_policy=true\naccess_days_approval_threshold=60\nbusiness_justification_provided=true\nrequest_free_of_ethics_office_flags=true\nlegal_preservation_order_on_the_account=false\nrequest_grants_admin_rights=false\nrequest_text_written_in_capital_letters=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if account_suspended is true or requested_role_permitted_by_policy is false or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n2. deny if request_grants_admin_rights is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n3. defer if business_justification_provided is false or mfa_enrollment_complete is false.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nAmong the actions listed after this, which best matches the request?",
  "options": [
   "defer",
   "approve",
   "deny"
  ]
 },
 {
  "qid": "q8122d874c7",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n  deploy_id: DEP-5638\n  service: catalog\nvalues:\n  files_changed_soft_limit: 15\n  files_changed: 2\ntests:\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  commit_messages_written_in_a_detailed_style: true\n  deploy_has_a_long_description: false\n  rollout_approval_revoked: false\n  service_free_of_major_incidents: true\n  canary_results_complete: true\n  deploy_prohibited_during_the_audit_window: false\n  deploy_blocked_by_security_policy: false\n  backout_plan_missing: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if canary_results_complete is false.\n2. turn down if rollout_approval_revoked is true.\n3. put on hold if backout_plan_missing is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\nOtherwise: go ahead.\nNever counted: deploy_has_a_long_description, deploy_blocked_by_security_policy, service_free_of_major_incidents, contract_customer_asked_for_a_say_in_this_rollout, commit_messages_written_in_a_detailed_style.\nMeanings:\n- turn down: shut this down before it spreads into the workflow\n- go ahead: move ahead on the request in the form it arrived since the path is open\n- send to a person: hand this over to whoever has the final say\n- put on hold: hold up for a sec until more info comes in\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below would be the appropriate determination for the request in question?",
  "options": [
   "go ahead",
   "put on hold",
   "turn down"
  ]
 },
 {
  "qid": "qd6cf174534",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n    deploy_id: DEP-1936\n    service: billing\namounts:\n    files_changed: 65\n    files_changed_soft_limit: 80\nchecks:\n    canary_results_complete: true\n    commit_messages_written_in_a_detailed_style: true\n    deploy_prohibited_during_the_audit_window: true\n    deploy_has_a_long_description: true\n    backout_plan_documented: true\n    rollout_approval_revoked: false\n    service_free_of_major_incidents: true\n    deploy_blocked_by_security_policy: false\n    contract_customer_asked_for_a_say_in_this_rollout: false",
  "question": "Meanings:\n- put_on_hold: hold off until the check has been completed by the team\n- send_to_a_person: delegate the call to whoever holds authority\n- turn_down: send the requester away with the request left unfinished\n- go_ahead: continue the work as originally asked, there is nothing in the way\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "send_to_a_person",
   "turn_down",
   "go_ahead"
  ]
 },
 {
  "qid": "q06c362394b",
  "kind": "choice",
  "text": "invoice_id: INV-6355\nvendor: Cedar Systems\ninvoice_pdf_uses_a_portrait_layout: true\nduplicate_of_paid_invoice: false\npurchase_order_received: true\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_free_of_sanctions: true\nvendor_tax_form_missing: false\npayment_requested_during_business_hours: true\namount_approval_threshold: 10000.00\nvendor_name_written_in_capital_letters: false\napprover_declared_a_conflict_of_interest: false\namount: 9711.04",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if purchase_order_received is false or vendor_tax_form_missing is true.\n2. deny if vendor_free_of_sanctions is false.\n3. ask manager if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nAs the team lead, which of the actions listed should we go with for this request?",
  "options": [
   "approve",
   "defer",
   "deny"
  ]
 },
 {
  "qid": "q4fd14499d2",
  "kind": "choice",
  "text": "ticket_id | TCK-9721\ncustomer | Yara Novak\nfree_of_safety_incident_reports | true\nclaim_amount_hard_limit | 50.00\nclaim_form_filled_in_with_the_usual_font | true\nclaim_amount | 32.40\nproof_of_purchase_attached | true\nlegal_complaint_filed | false\nitem_excluded_by_policy | true\nclaim_involves_a_media_inquiry | false\nclaim_free_of_ombudsman_cases | true\nitem_return_not_yet_received | false\nharmless_greeting_present_in_the_message | true",
  "question": "Meanings:\n- PHZ: be handed over to the deciding person\n- WXKB: complete the job as it was assigned\n- NZ: shut this down before it spreads into the workflow\n- G: stall the request until the check comes back\nThe record is complete: nothing else applies.\n\nLooking at what was asked, which of the actions below best fits the request?",
  "options": [
   "G",
   "NZ",
   "WXKB"
  ]
 },
 {
  "qid": "q6efb13ab66",
  "kind": "choice",
  "text": "---\n# request record\nticket_id: \"TCK-9822\"\ncustomer: \"Dana Duarte\"\nclaim_amount: 50.00\nproof_of_purchase_missing: true\nclaim_amount_hard_limit: 50.00\nclaim_form_filled_in_with_the_usual_font: false\nfree_of_safety_incident_reports: true\nitem_excluded_by_policy: true\nclaim_involves_a_media_inquiry: false\nitem_return_received: false\nharmless_greeting_present_in_the_message: true\nclaim_free_of_ombudsman_cases: true\nlegal_complaint_filed: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if free_of_safety_incident_reports is false.\n2. deny if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_received is false.\nOtherwise: approve.\nNever counted: proof_of_purchase_missing, item_excluded_by_policy, legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- approve: move ahead on the request in the form it arrived since the path is open\n- ask_manager: route this to the one who signs off\n- deny: send the requester away with the request left unfinished\n- defer: await further verification before any progression\nThe record is complete: nothing else applies.\n\nOf the actions listed after this, which is the fitting call for the request?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "qd981325de1",
  "kind": "choice",
  "text": "{\n    \"record\": {\n        \"ticket_id\": \"TCK-5592\",\n        \"customer\": \"Dana Duarte\"\n    },\n    \"numbers\": {\n        \"claim_amount\": 999.99,\n        \"claim_amount_hard_limit\": 1000.00\n    },\n    \"flags\": {\n        \"proof_of_purchase_attached\": true,\n        \"claim_form_filled_in_with_the_usual_font\": true,\n        \"item_excluded_by_policy\": false,\n        \"harmless_greeting_present_in_the_message\": true,\n        \"claim_involves_a_media_inquiry\": true,\n        \"free_of_legal_complaints\": true,\n        \"item_return_not_yet_received\": false,\n        \"free_of_safety_incident_reports\": true,\n        \"claim_free_of_ombudsman_cases\": true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. J if claim_amount is at least claim_amount_hard_limit.\n2. HXLB if free_of_legal_complaints is false or claim_involves_a_media_inquiry is true.\n3. HD if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: LZG.\nNever counted: item_return_not_yet_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- HD: wait for that check then we will see\n- LZG: carry on with it now\n- J: kill this one off, it is off the table for good\n- HXLB: pass the request to a decider\nThe record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "J",
   "LZG",
   "HXLB"
  ]
 },
 {
  "qid": "qaa5d3b4ee0",
  "kind": "yes/no",
  "text": "{\n    \"case\":{\n        \"request_id\":\"REQ-4570\",\n        \"requester\":\"ريم سامي الزهراني\",\n        \"note\":\"موافقة المدير المباشر موجودة على طلب الوصول.\"\n    },\n    \"values\":{\n        \"access_days_approval_threshold\":60,\n        \"access_days\":11\n    },\n    \"tests\":{\n        \"request_text_written_in_capital_letters\":false,\n        \"account_suspended\":false,\n        \"requested_role_permitted_by_policy\":true,\n        \"mfa_enrollment_complete\":true,\n        \"business_justification_missing\":false,\n        \"legal_preservation_order_on_the_account\":true,\n        \"ethics_office_flagged_the_request\":false,\n        \"request_grants_admin_rights\":true,\n        \"requester_barred_from_this_system\":false\n    }\n}",
  "question": "Proposed action: 47\nIs the proposed action not the best thing to do with this?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 7126 if mfa_enrollment_complete is false or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\n2. 47 if account_suspended is true or requested_role_permitted_by_policy is false.\n3. 125 if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: 5.\nNever counted: business_justification_missing, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- 7126: chill until the document turns up\n- 5: continue so the requester receives the result\n- 47: be blocked outright so it never gets carried out\n- 125: be routed to whoever holds the decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5c447d2707",
  "kind": "choice",
  "text": "---\ndeploy_id: DEP-5267\nservice: checkout\ncommit_messages_written_in_a_detailed_style: true\ndeploy_has_a_long_description: false\nbackout_plan_documented: true\nfiles_changed_soft_limit: 30\ndeploy_prohibited_during_the_audit_window: false\ndeploy_blocked_by_security_policy: false\nrollout_approval_revoked: false\nfiles_changed: 29\nservice_free_of_major_incidents: true\ncanary_results_incomplete: false\ncontract_customer_asked_for_a_say_in_this_rollout: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if backout_plan_documented is false.\n2. turn down if rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is at least files_changed_soft_limit.\n3. send to a person if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style.\nMeanings:\n- put on hold: stay put until the check is finished\n- go ahead: execute the requested action as nothing prevents it\n- send to a person: be routed to whoever holds the decision\n- turn down: scrap the plan and drop this request\nThe record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "put on hold",
   "go ahead",
   "send to a person"
  ]
 },
 {
  "qid": "q49c0072c9f",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n* deploy id: DEP-3600\n* service: notifier\n* contract customer asked for a say in this rollout: no\n* deploy has a long description: no\n* deploy blocked by security policy: no\n* deploy prohibited during the audit window: no\n* backout plan missing: no\n* files changed: 11\n* service free of major incidents: yes\n* commit messages written in a detailed style: yes\n* files changed soft limit: 10\n* canary results incomplete: no\n* rollout approval revoked: no",
  "question": "Proposed action: GCT\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. GCT if backout_plan_missing is true or rollout_approval_revoked is true or files_changed is at least files_changed_soft_limit.\n2. CQFW if contract_customer_asked_for_a_say_in_this_rollout is true.\n3. X if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\nOtherwise: DN.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style.\nMeanings:\n- CQFW: route it elsewhere because a decider must weigh in\n- DN: go ahead with the requested action\n- X: be turned away and treated as off limits\n- GCT: keep it in limbo until the verification has been confirmed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qca4d4cc8ff",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-3152\nvendor | Brightwater Foods\nvendor_filed_a_legal_claim_over_this_invoice | false\npurchase_order_received | true\npayment_requested_during_business_hours | true\nvendor_tax_form_missing | true\ninvoice_pdf_uses_a_landscape_layout | false\nvendor_name_written_in_capital_letters | false\namount | 3466.21\napprover_declared_a_conflict_of_interest | false\nvendor_on_sanctions_list | false\namount_approval_threshold | 25000.00\nduplicate_of_paid_invoice | false",
  "question": "Proposed action: go_ahead\nAuditing this request closely, is the proposed action not a defensible choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. turn_down if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. put_on_hold if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- go_ahead: keep moving on this one nothing is holding it up\n- send_to_a_person: hand the matter to a decider so the requester gets a verdict\n- put_on_hold: be parked until a verification has been logged\n- turn_down: withdraw from the step as it is forbidden\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb7b0fc4310",
  "kind": "yes/no",
  "text": "{\n    \"case\":{\n        \"deploy_id\":\"DEP-7007\",\n        \"service\":\"gateway\"\n    },\n    \"values\":{\n        \"files_changed\":13,\n        \"files_changed_soft_limit\":30\n    },\n    \"tests\":{\n        \"service_free_of_major_incidents\":true,\n        \"commit_messages_written_in_a_detailed_style\":true,\n        \"backout_plan_documented\":true,\n        \"canary_results_incomplete\":false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\":true,\n        \"deploy_prohibited_during_the_audit_window\":false,\n        \"deploy_blocked_by_security_policy\":false,\n        \"deploy_has_a_long_description\":false,\n        \"rollout_approval_revoked\":false\n    }\n}",
  "question": "Proposed action: put on hold\nWould the proposed action be the right move for the request in the record?",
  "definitions": "Meanings:\n- put on hold: sit on it till the doc shows up\n- go ahead: keep moving so the asker gets the outcome\n- turn down: be halted at once and left unperformed\n- send to a person: send this on to whoever decides\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7b26174465",
  "kind": "yes/no",
  "text": "---\n# extract\nrequest_id: REQ-8418\nrequester: فارس مهند الجبوري\nnote: صلاحية الوصول المطلوبة تتوافق مع دور الموظف الوظيفي.\naccess_days: 2\nrequester_barred_from_this_system: false\nrequest_grants_admin_rights: false\nlegal_preservation_order_on_the_account: false\nethics_office_flagged_the_request: false\nrequest_text_written_in_capital_letters: false\nbusiness_justification_missing: false\naccess_days_approval_threshold: 30\nmfa_enrollment_incomplete: false\nrequested_role_permitted_by_policy: true\naccount_suspended: false",
  "question": "Proposed action: defer\nUpon audit, is the proposed action the correct determination given the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if account_suspended is true or requested_role_permitted_by_policy is false or request_grants_admin_rights is true.\n2. ask manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. defer if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q577bc6bfd7",
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
  "qid": "q46d11cf6f6",
  "kind": "choice",
  "text": "---\nrequest_id: \"REQ-4940\"\nrequester: \"Tomas Petrov\"\nrequester_barred_from_this_system: false\naccess_days: 91\naccess_days_approval_threshold: 90\nrequested_role_permitted_by_policy: true\naccount_suspended: false\nrequest_text_written_in_capital_letters: false\nbusiness_justification_missing: false\nlegal_preservation_order_on_the_account: false\nethics_office_flagged_the_request: false\nmfa_enrollment_complete: true\nrequest_grants_admin_rights: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if request_grants_admin_rights is true or ethics_office_flagged_the_request is true or access_days is at least access_days_approval_threshold.\n2. defer if mfa_enrollment_complete is false.\n3. deny if business_justification_missing is true or account_suspended is true or requested_role_permitted_by_policy is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "deny",
   "approve",
   "ask_manager"
  ]
 },
 {
  "qid": "q2340a40b2f",
  "kind": "choice",
  "text": "request_id=REQ-9434\nrequester=Samir Mensah\nrequested_role_permitted_by_policy=true\naccess_days=5\nlegal_preservation_order_on_the_account=false\naccess_days_approval_threshold=14\nrequest_text_written_in_capital_letters=false\naccount_suspended=false\nbusiness_justification_missing=false\nrequester_barred_from_this_system=false\nrequest_grants_admin_rights=false\nethics_office_flagged_the_request=false\nmfa_enrollment_complete=false",
  "question": "Meanings:\n- 9226: hand the matter to a decider so the requester gets a verdict\n- 20: terminate the process as continuation is prohibited\n- 925: proceed with the task as asked\n- 2: pause here and wait for the check\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "925",
   "2",
   "20"
  ]
 },
 {
  "qid": "q33cf180115",
  "kind": "choice",
  "text": "# extract\nrun_id: RUN-8395\nagent: ember\nlast_tool_output_unverified: false\naction_permitted_by_security_policy: true\nsteps_used_hard_limit: 30\ntask_description_incomplete: false\nlog_lines_written_in_a_verbose_style: false\naction_free_of_ethics_concerns: false\ntool_output_shows_tampering: false\nsteps_used: 31\nowner_sign_off_required_for_this_action: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is at least steps_used_hard_limit.\n2. put on hold if task_description_incomplete is true or owner_sign_off_required_for_this_action is true.\n3. send to a person if action_free_of_ethics_concerns is false.\nOtherwise: go ahead.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed does the record best support for this request?",
  "options": [
   "send to a person",
   "put on hold",
   "turn down"
  ]
 },
 {
  "qid": "q498ba0966b",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- run id: RUN-2164\n- agent: kestrel\n- last tool output verified: yes\n- action forbidden by security policy: no\n- task description complete: yes\n- log lines written in a compact style: yes\n- tool output shows tampering: no\n- steps used hard limit: 8\n- steps used: 7\n- owner sign off required for this action: no\n- action free of ethics concerns: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is at least steps_used_hard_limit.\n2. put on hold if task_description_complete is false or owner_sign_off_required_for_this_action is true.\n3. send to a person if action_free_of_ethics_concerns is false.\nOtherwise: go ahead.\nNever counted: last_tool_output_verified, log_lines_written_in_a_compact_style.\nMeanings:\n- go ahead: proceed with the request since the way is clear and nothing blocks it\n- put on hold: hold the request until a check is completed\n- send to a person: be forwarded to the person in charge\n- turn down: refuse this request entirely\nThe record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "send to a person",
   "go ahead",
   "put on hold"
  ]
 },
 {
  "qid": "qcce99308b3",
  "kind": "yes/no",
  "text": "{\n  \"meta\":{\n    \"run_id\":\"RUN-6741\",\n    \"agent\":\"indigo\"\n  },\n  \"metrics\":{\n    \"steps_used_hard_limit\":30,\n    \"steps_used\":9\n  },\n  \"signals\":{\n    \"task_description_incomplete\":false,\n    \"action_free_of_ethics_concerns\":true,\n    \"last_tool_output_verified\":true,\n    \"owner_sign_off_required_for_this_action\":true,\n    \"log_lines_written_in_a_compact_style\":true,\n    \"action_permitted_by_security_policy\":true,\n    \"tool_output_shows_tampering\":false\n  }\n}",
  "question": "Proposed action: turn_down\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put_on_hold if last_tool_output_verified is false or task_description_incomplete is true.\n3. turn_down if action_permitted_by_security_policy is false or owner_sign_off_required_for_this_action is true or steps_used is above steps_used_hard_limit.\nOtherwise: go_ahead.\nNever counted: log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7ef1085c33",
  "kind": "yes/no",
  "text": "request_id=REQ-1599\nrequester=Zoe Vasquez\naccess_days=45\nmfa_enrollment_incomplete=false\nlegal_preservation_order_on_the_account=false\nrequested_role_permitted_by_policy=true\nethics_office_flagged_the_request=false\nrequest_grants_admin_rights=false\nrequester_not_barred_from_this_system=true\naccess_days_approval_threshold=45\nrequest_text_written_in_capital_letters=false\nbusiness_justification_provided=true\naccount_suspended=false",
  "question": "Proposed action: grant\nIs the proposed action the appropriate course of action for the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer to owner if account_suspended is true or requested_role_permitted_by_policy is false or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. refuse if request_grants_admin_rights is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n3. pend if business_justification_provided is false or mfa_enrollment_incomplete is true.\nOtherwise: grant.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- pend: keep it in limbo until the verification has been confirmed\n- grant: keep it moving forward\n- refuse: shut this down right away, we are staying clear of it\n- refer to owner: escalate the matter to the accountable decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf4c0a53048",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-6429\", \"vendor\": \"Pinecrest Works\", \"vendor_name_written_in_capital_letters\": false, \"amount\": 5000.01, \"payment_requested_during_business_hours\": true, \"approver_free_of_conflicts_of_interest\": true, \"vendor_on_sanctions_list\": false, \"purchase_order_received\": true, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"invoice_pdf_uses_a_portrait_layout\": true, \"amount_approval_threshold\": 5000.00, \"vendor_tax_form_on_file\": true, \"duplicate_of_paid_invoice\": false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if purchase_order_received is false.\n2. send to a person if vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. turn down if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or approver_free_of_conflicts_of_interest is false or amount is above amount_approval_threshold.\nOtherwise: go ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- put on hold: stay put until the check is finished\n- go ahead: push ahead as planned\n- send to a person: delegate the call to whoever holds authority\n- turn down: reject the request in full\nThe record is complete: nothing else applies.\n\nWhich of the listed actions is the right call for this request?",
  "options": [
   "turn down",
   "go ahead",
   "put on hold"
  ]
 },
 {
  "qid": "q9f14d596ee",
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
  "qid": "qb3c30abe47",
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
  "qid": "qef87d726ec",
  "kind": "choice",
  "text": "---\nmeta:\n  request_id: \"REQ-2898\"\n  requester: \"Priya Adeyemi\"\nmetrics:\n  access_days: 3\n  access_days_approval_threshold: 30\nsignals:\n  ethics_office_flagged_the_request: true\n  legal_preservation_order_on_the_account: false\n  request_text_written_in_capital_letters: false\n  request_grants_admin_rights: false\n  requester_not_barred_from_this_system: true\n  mfa_enrollment_complete: true\n  account_suspended: false\n  business_justification_missing: true\n  requested_role_forbidden_by_policy: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if business_justification_missing is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n2. refer_to_owner if mfa_enrollment_complete is false or request_grants_admin_rights is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n3. refuse if account_suspended is true or requested_role_forbidden_by_policy is true.\nOtherwise: grant.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- refuse: end this here and now\n- pend: hold all progress until the requisite documentation arrives\n- grant: run the task as it was asked, with nothing standing between it and completion\n- refer_to_owner: route this to the one who signs off\nThe record is complete: nothing else applies.\n\nPicking from the actions listed, what best serves this request?",
  "options": [
   "refer_to_owner",
   "pend",
   "refuse"
  ]
 },
 {
  "qid": "qbb60c0ced9",
  "kind": "choice",
  "text": "{\n    \"record\":{\n        \"ticket_id\":\"TCK-3256\",\n        \"customer\":\"Hugo Okafor\"\n    },\n    \"numbers\":{\n        \"claim_amount\":52.28,\n        \"claim_amount_hard_limit\":100.00\n    },\n    \"flags\":{\n        \"claim_form_filled_in_with_the_usual_font\":true,\n        \"proof_of_purchase_attached\":true,\n        \"item_return_not_yet_received\":false,\n        \"legal_complaint_filed\":false,\n        \"item_excluded_by_policy\":false,\n        \"claim_free_of_ombudsman_cases\":true,\n        \"harmless_greeting_present_in_the_message\":true,\n        \"claim_involves_a_media_inquiry\":true,\n        \"free_of_safety_incident_reports\":true\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nWhich of the listed actions is the right call for this request?",
  "options": [
   "ask manager",
   "deny",
   "approve"
  ]
 },
 {
  "qid": "qbb24929e50",
  "kind": "choice",
  "text": "# extract\nrequest_id | REQ-4995\nrequester | Hugo Imai\naccess_days_approval_threshold | 45\nbusiness_justification_missing | false\nrequester_barred_from_this_system | false\naccess_days | 7\naccount_suspended | false\nmfa_enrollment_incomplete | false\nrequested_role_forbidden_by_policy | false\nrequest_free_of_ethics_office_flags | true\nrequest_text_written_in_capital_letters | false\nrequest_grants_admin_rights | false\nlegal_preservation_order_on_the_account | false",
  "question": "Meanings:\n- refuse: kill this one off, it is off the table for good\n- grant: keep moving on this one nothing is holding it up\n- refer to owner: forward it to the decision maker\n- pend: hold this until a check comes back\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "grant",
   "pend",
   "refer to owner"
  ]
 },
 {
  "qid": "q33aacbde5f",
  "kind": "yes/no",
  "text": "{\"run_id\": \"RUN-8548\", \"agent\": \"kestrel\", \"tool_output_shows_tampering\": false, \"owner_sign_off_required_for_this_action\": false, \"action_permitted_by_security_policy\": true, \"last_tool_output_verified\": true, \"task_description_complete\": true, \"action_free_of_ethics_concerns\": true, \"steps_used_hard_limit\": 8, \"log_lines_written_in_a_verbose_style\": true, \"steps_used\": 4}",
  "question": "Proposed action: VHTT\nConsidering what was asked and the facts involved, is the proposed action not the correct decision?",
  "definitions": "Meanings:\n- BV: get referred to the person who decides\n- VHTT: go on and finish it the path is clear\n- G: scrap the plan and drop this request\n- VGT: keep their request on hold until more information arrives from them\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd619d76cc7",
  "kind": "yes/no",
  "text": "{\"deploy_id\": \"DEP-3893\", \"service\": \"catalog\", \"rollout_approval_revoked\": false, \"deploy_blocked_by_security_policy\": true, \"canary_results_incomplete\": false, \"deploy_prohibited_during_the_audit_window\": false, \"files_changed\": 10, \"deploy_has_a_long_description\": false, \"contract_customer_asked_for_a_say_in_this_rollout\": false, \"files_changed_soft_limit\": 10, \"commit_messages_written_in_a_terse_style\": false, \"service_free_of_major_incidents\": true, \"backout_plan_documented\": true}",
  "question": "Proposed action: go_ahead\nDoes the record's evidence rule out the proposed action as the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn_down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put_on_hold if backout_plan_documented is false or rollout_approval_revoked is true.\nOtherwise: go_ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_terse_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf83d1fc87a",
  "kind": "choice",
  "text": "# record\nticket_id | TCK-3187\ncustomer | Omar Moreau\nproof_of_purchase_missing | false\nclaim_free_of_ombudsman_cases | true\nlegal_complaint_filed | false\nclaim_amount | 200.00\nclaim_amount_hard_limit | 200.00\nharmless_greeting_present_in_the_message | true\nitem_return_not_yet_received | true\nclaim_involves_a_media_inquiry | false\nclaim_form_filled_in_with_the_usual_font | true\nitem_excluded_by_policy | false\nfree_of_safety_incident_reports | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false or claim_free_of_ombudsman_cases is false.\n2. deny if proof_of_purchase_missing is true or item_excluded_by_policy is true or claim_involves_a_media_inquiry is true or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_not_yet_received is true.\nOtherwise: approve.\nNever counted: legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "approve",
   "defer",
   "deny"
  ]
 },
 {
  "qid": "qbecff22207",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-5006\nvendor=Pinecrest Logistics\nduplicate_of_paid_invoice=false\nvendor_filed_a_legal_claim_over_this_invoice=false\napprover_declared_a_conflict_of_interest=false\namount=4403.30\npayment_requested_during_business_hours=true\npurchase_order_received=true\ninvoice_pdf_uses_a_landscape_layout=false\nvendor_name_written_in_capital_letters=true\nvendor_tax_form_missing=false\namount_approval_threshold=5000.00\nvendor_on_sanctions_list=false",
  "question": "Proposed action: 63\nIs the proposed action the right move for this request, given the facts involved?",
  "definitions": "Meanings:\n- 938: shelve the matter until more details come in\n- 8: reject the request in full\n- 63: continue the work as originally asked, there is nothing in the way\n- 2141: get the boss to make the final call\nThe record is complete: nothing else applies."
 }
]
