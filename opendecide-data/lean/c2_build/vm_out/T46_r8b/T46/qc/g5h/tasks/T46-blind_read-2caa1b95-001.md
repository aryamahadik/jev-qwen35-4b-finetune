# G5-H blind read T46-blind_read-2caa1b95-001 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8b/T46/qc/g5h/answers/T46-blind_read-2caa1b95-001.json

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
  "qid": "q0b6f48851e",
  "kind": "yes/no",
  "text": "---\nmeta:\n  leave_id: \"LVE-5961\"\n  employee: \"Omar Moreau\"\nmetrics:\n  leave_days_soft_limit: 21\n  leave_days: 1\nsignals:\n  lawyer_letter_received_about_this_leave: false\n  requests_team_free_of_harassment_complaints: false\n  medical_certificate_contested: false\n  notice_period_not_met: false\n  team_coverage_not_arranged: false\n  leave_balance_available: true\n  union_grievance_raised_over_this_leave: false\n  request_falls_in_blackout_period: false\n  leave_request_written_in_a_formal_tone: false",
  "question": "Proposed action: approve\nWould the proposed action be the right answer to what this request calls for?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if notice_period_not_met is true or team_coverage_not_arranged is true or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. refuse if medical_certificate_contested is true.\n3. ask_a_human if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q163226454b",
  "kind": "yes/no",
  "text": "request_id | REQ-6572\nrequester | Idris Lindqvist\nmfa_enrollment_incomplete | false\nrequest_text_written_in_capital_letters | true\nrequest_grants_admin_rights | false\naccess_days_approval_threshold | 7\nbusiness_justification_provided | true\nrequested_role_forbidden_by_policy | false\naccount_suspended | false\nlegal_preservation_order_on_the_account | false\naccess_days | 6\nrequester_barred_from_this_system | false\nethics_office_flagged_the_request | false",
  "question": "Proposed action: proceed\nIs it not true that the proposed action is not mistaken, given what the record shows?",
  "definitions": "Meanings:\n- wait: hold the request so the requester waits for their check\n- proceed: keep it moving forward\n- cancel: block the action because it is off limits to the team\n- ask a human: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc0e3c89922",
  "kind": "choice",
  "text": "# record\nleave_id | LVE-2692\nemployee | Paolo Petrov\nrequest_falls_in_blackout_period | false\nleave_days | 7\nrequests_team_free_of_harassment_complaints | true\nteam_coverage_not_arranged | false\nnotice_period_not_met | false\nleave_days_soft_limit | 14\nleave_request_written_in_a_formal_tone | false\nunion_grievance_raised_over_this_leave | true\nmedical_certificate_contested | true\nleave_balance_exhausted | false\nlawyer_letter_received_about_this_leave | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. MS if notice_period_not_met is true or team_coverage_not_arranged is true or leave_balance_exhausted is true or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. K if medical_certificate_contested is true.\n3. RZX if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: ZFJR.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- ZFJR: just crack on with it there is nothing in the way\n- RZX: give it to the person in charge of the call\n- K: drop it right away\n- MS: shelve the matter until more details come in\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "ZFJR",
   "K",
   "RZX"
  ]
 },
 {
  "qid": "q2c80af92b6",
  "kind": "yes/no",
  "text": "# record\ndeploy_id: DEP-7188\nservice: gateway\ndeploy_has_a_long_description: false\nservice_free_of_major_incidents: true\nrollout_approval_revoked: true\ndeploy_blocked_by_security_policy: false\nbackout_plan_missing: false\nfiles_changed_soft_limit: 15\ncontract_customer_asked_for_a_say_in_this_rollout: false\nfiles_changed: 6\ncanary_results_incomplete: false\ncommit_messages_written_in_a_casual_tone: true\ndeploy_prohibited_during_the_audit_window: false\ncommit_messages_written_in_a_detailed_style: true\ndeploy_title_written_in_normal_case: true",
  "question": "Proposed action: turn_down\nGiven the request and the facts, is the proposed action the right call?",
  "definitions": "Meanings:\n- turn_down: stop this course of action at once\n- go_ahead: keep moving on this one nothing is holding it up\n- send_to_a_person: pass this along to the decision maker\n- put_on_hold: keep waiting for the missing details\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8328c2af43",
  "kind": "choice",
  "text": "# record\ninvoice_id=INV-8685\nvendor=Riverbend Works\nawaiting_purchase_order=false\ninvoice_pdf_uses_a_landscape_layout=false\nvendor_tax_form_on_file=true\nvendor_on_sanctions_list=false\namount_approval_threshold=10000.00\npayment_requested_during_business_hours=true\nvendor_name_written_in_capital_letters=false\nduplicate_of_paid_invoice=false\nvendor_filed_a_legal_claim_over_this_invoice=false\namount=10000.01\napprover_declared_a_conflict_of_interest=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. hand to a person if vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. cancel order if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or approver_declared_a_conflict_of_interest is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below would be the appropriate determination for the request in question?",
  "options": [
   "hand to a person",
   "release",
   "cancel order"
  ]
 },
 {
  "qid": "qf65f8a289a",
  "kind": "choice",
  "text": "{\n    \"meta\": {\n        \"request_id\": \"REQ-6715\",\n        \"requester\": \"Felix Ferreira\"\n    },\n    \"metrics\": {\n        \"access_days\": 5,\n        \"access_days_approval_threshold\": 45\n    },\n    \"signals\": {\n        \"account_suspended\": true,\n        \"mfa_enrollment_incomplete\": false,\n        \"request_free_of_ethics_office_flags\": true,\n        \"legal_preservation_order_on_the_account\": false,\n        \"business_justification_missing\": false,\n        \"requested_role_permitted_by_policy\": true,\n        \"request_grants_admin_rights\": false,\n        \"requester_not_barred_from_this_system\": true,\n        \"request_text_written_in_capital_letters\": false\n    }\n}",
  "question": "Meanings:\n- pend: be held back until a check or document arrives\n- refer to owner: route this matter to the individual empowered to decide\n- grant: proceed and the requester gets what they asked\n- refuse: be turned away and treated as off limits\nThe record is complete: nothing else applies.\n\nWhich action listed below fits this request best?",
  "options": [
   "refuse",
   "grant",
   "refer to owner"
  ]
 },
 {
  "qid": "qd6a1026c19",
  "kind": "choice",
  "text": "request_id=REQ-9651\nrequester=Leila Ferreira\naccess_days_approval_threshold=45\nrequester_barred_from_this_system=false\nrequest_grants_admin_rights=true\nrequest_text_written_in_capital_letters=false\nbusiness_justification_missing=false\nlegal_preservation_order_on_the_account=true\nmfa_enrollment_incomplete=false\nrequest_free_of_ethics_office_flags=true\naccess_days=42\nrequested_role_permitted_by_policy=true\naccount_suspended=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 8 if business_justification_missing is true or mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. 4997 if account_suspended is true or requested_role_permitted_by_policy is false.\n3. 872 if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: 31.\nNever counted: request_free_of_ethics_office_flags, request_text_written_in_capital_letters.\nMeanings:\n- 4997: send the requester away with the request left unfinished\n- 31: just crack on with it there is nothing in the way\n- 872: refer this item to the person who holds decision authority\n- 8: hold off until the check clears\nThe record is complete: nothing else applies.\n\nAs an auditor, which of the listed actions is the correct call for this request?",
  "options": [
   "31",
   "872",
   "8"
  ]
 },
 {
  "qid": "q545d184087",
  "kind": "choice",
  "text": "{\n    \"deploy_id\": \"DEP-2716\",\n    \"service\": \"mailer\",\n    \"commit_messages_written_in_a_terse_style\": false,\n    \"deploy_prohibited_during_the_audit_window\": false,\n    \"service_free_of_major_incidents\": true,\n    \"deploy_blocked_by_security_policy\": false,\n    \"contract_customer_asked_for_a_say_in_this_rollout\": true,\n    \"canary_results_complete\": true,\n    \"deploy_has_a_long_description\": true,\n    \"files_changed_soft_limit\": 80,\n    \"commit_messages_written_in_a_casual_tone\": true,\n    \"files_changed\": 12,\n    \"backout_plan_missing\": false,\n    \"deploy_title_written_in_normal_case\": true,\n    \"rollout_approval_revoked\": false\n}",
  "question": "Meanings:\n- 11: allow the matter to be taken forward as planned\n- 5336: be paused until a document has been received\n- 464: escalate this to the person who decides\n- 3: terminate the process as continuation is prohibited\nThe record is complete: nothing else applies.\n\nWhich of the actions listed would be the right call for the matter in this file?",
  "options": [
   "464",
   "3",
   "11"
  ]
 },
 {
  "qid": "q3536e0fa43",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"leave_id\": \"LVE-4716\",\n        \"employee\": \"Tomas Moreau\"\n    },\n    \"values\": {\n        \"leave_days_soft_limit\": 7,\n        \"leave_days\": 8\n    },\n    \"tests\": {\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"leave_balance_available\": true,\n        \"notice_period_not_met\": false,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"request_falls_in_blackout_period\": false,\n        \"leave_request_written_in_a_formal_tone\": false,\n        \"team_coverage_not_arranged\": false,\n        \"union_grievance_raised_over_this_leave\": false\n    }\n}",
  "question": "Proposed action: DRV\nDo the facts we have help rule out the proposed action here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. DRV if notice_period_not_met is true or team_coverage_not_arranged is true or leave_days is above leave_days_soft_limit.\n2. DT if request_falls_in_blackout_period is true.\n3. DBDV if leave_balance_available is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or union_grievance_raised_over_this_leave is true.\nOtherwise: D.\nNever counted: lawyer_letter_received_about_this_leave, leave_request_written_in_a_formal_tone.\nMeanings:\n- DRV: hang tight until we get the check back\n- DBDV: give it to the person in charge of the call\n- DT: end it so the requester sees their request closed\n- D: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3c265a37aa",
  "kind": "choice",
  "text": "{\"deploy_id\":\"DEP-6644\",\"service\":\"gateway\",\"contract_customer_asked_for_a_say_in_this_rollout\":false,\"canary_results_incomplete\":true,\"deploy_has_a_long_description\":false,\"files_changed_soft_limit\":80,\"backout_plan_missing\":false,\"commit_messages_written_in_a_casual_tone\":true,\"service_free_of_major_incidents\":true,\"deploy_title_written_in_normal_case\":true,\"commit_messages_written_in_a_detailed_style\":true,\"deploy_prohibited_during_the_audit_window\":false,\"files_changed\":42,\"deploy_blocked_by_security_policy\":false,\"rollout_approval_revoked\":false}",
  "question": "Meanings:\n- turn down: shut off this process completely\n- put on hold: hold up for a sec until more info comes in\n- send to a person: bring in the authority who can settle it for the requester\n- go ahead: complete the job as it was assigned\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "go ahead",
   "turn down",
   "put on hold"
  ]
 },
 {
  "qid": "q9af63ab744",
  "kind": "yes/no",
  "text": "invoice_id: INV-3507\nvendor: Stonebridge Works\nvendor_free_of_sanctions: false\nduplicate_of_paid_invoice: false\napprover_declared_a_conflict_of_interest: false\npayment_requested_during_business_hours: true\nvendor_tax_form_missing: false\nawaiting_purchase_order: false\namount_approval_threshold: 2500.00\ninvoice_pdf_uses_a_portrait_layout: true\namount: 253.25\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_name_written_in_capital_letters: false",
  "question": "Proposed action: ask a human\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q977eded8d3",
  "kind": "yes/no",
  "text": "leave_id: LVE-7827\nemployee: Nadia Mensah\nleave_request_written_in_a_formal_tone: false\nleave_days: 13\nrequests_team_free_of_harassment_complaints: true\nrequest_falls_in_blackout_period: false\nmedical_certificate_contested: false\nunion_grievance_raised_over_this_leave: false\nlawyer_letter_received_about_this_leave: false\nnotice_period_not_met: false\nleave_days_soft_limit: 14\nleave_balance_exhausted: false\nteam_coverage_arranged: true",
  "question": "Proposed action: CCV\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Meanings:\n- MM: pause and collect more information first\n- RKDZ: escalate this to someone senior who decides\n- CCV: stop the request so the requester gets nothing from it\n- R: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6517d0a212",
  "kind": "choice",
  "text": "# case\ndeploy_id: DEP-6834\nservice: mailer\nservice_free_of_major_incidents: true\ndeploy_title_written_in_normal_case: true\nrollout_approval_revoked: false\ncanary_results_incomplete: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_prohibited_during_the_audit_window: false\ncommit_messages_written_in_a_detailed_style: true\ndeploy_blocked_by_security_policy: false\nfiles_changed_soft_limit: 15\nbackout_plan_documented: true\nfiles_changed: 15\ndeploy_has_a_long_description: false\ncommit_messages_written_in_a_casual_tone: true",
  "question": "The record is complete: nothing else applies.\n\nReading the file for this case, which listed action is the best call?",
  "options": [
   "put on hold",
   "go ahead",
   "turn down"
  ]
 },
 {
  "qid": "q7174b31c82",
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
  "qid": "q095f930614",
  "kind": "choice",
  "text": "# extract\nticket_id | TCK-1079\ncustomer | Elena Sorensen\nlegal_complaint_filed | false\nclaim_involves_a_media_inquiry | false\nharmless_greeting_present_in_the_message | true\ncustomer_message_written_in_a_formal_tone | false\nitem_excluded_by_policy | false\nclaim_form_filled_in_with_the_usual_font | true\nitem_return_not_yet_received | false\nclaim_free_of_ombudsman_cases | true\nfree_of_safety_incident_reports | true\nproof_of_purchase_missing | false\nclaim_amount_hard_limit | 50.00\ncustomer_message_is_short | true\nclaim_amount | 20.74",
  "question": "Meanings:\n- turn_down: be dropped here and not acted upon at all\n- send_to_a_person: refer the matter to the decision holder\n- go_ahead: continue with what was requested\n- put_on_hold: stay put until the check is finished\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "go_ahead",
   "turn_down",
   "send_to_a_person"
  ]
 },
 {
  "qid": "qb6bb39cc81",
  "kind": "yes/no",
  "text": "{\n  \"record\": {\n    \"request_id\": \"REQ-6858\",\n    \"requester\": \"Zoe Haddad\"\n  },\n  \"numbers\": {\n    \"access_days\": 60,\n    \"access_days_approval_threshold\": 60\n  },\n  \"flags\": {\n    \"business_justification_provided\": false,\n    \"request_grants_admin_rights\": false,\n    \"request_text_written_in_capital_letters\": true,\n    \"requested_role_forbidden_by_policy\": false,\n    \"requester_not_barred_from_this_system\": true,\n    \"legal_preservation_order_on_the_account\": false,\n    \"ethics_office_flagged_the_request\": false,\n    \"account_suspended\": true,\n    \"mfa_enrollment_incomplete\": false\n  }\n}",
  "question": "Proposed action: approve\nDoes the proposed action fit the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if mfa_enrollment_incomplete is true or requester_not_barred_from_this_system is false or ethics_office_flagged_the_request is true.\n2. refuse if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. ask_a_human if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: approve.\nNever counted: business_justification_provided, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- delay: defer further action pending verification of the document\n- ask_a_human: route this matter to the individual empowered to decide\n- approve: execute the request exactly as written\n- refuse: stop the work since it cannot move forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa6fd139e1b",
  "kind": "choice",
  "text": "leave_id: LVE-5160\nemployee: Ravi Imai\nleave_days: 7\nleave_days_soft_limit: 7\nmedical_certificate_contested: false\nno_union_grievance_raised_over_this_leave: true\nleave_balance_exhausted: false\nteam_coverage_not_arranged: false\nleave_request_written_in_a_formal_tone: false\nrequest_falls_in_blackout_period: false\nnotice_period_met: true\nlawyer_letter_received_about_this_leave: false\nrequests_team_free_of_harassment_complaints: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if notice_period_met is false or request_falls_in_blackout_period is true.\n2. delay if team_coverage_not_arranged is true or leave_balance_exhausted is true or leave_days is above leave_days_soft_limit.\n3. ask a human if medical_certificate_contested is true or no_union_grievance_raised_over_this_leave is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "approve",
   "ask a human",
   "delay"
  ]
 },
 {
  "qid": "q5a0c1684c4",
  "kind": "choice",
  "text": "---\n# request record\nsubject:\n  invoice_id: \"INV-5657\"\n  vendor: \"Brightwater Partners\"\namounts:\n  amount: 315.65\n  amount_approval_threshold: 500.00\nchecks:\n  vendor_on_sanctions_list: false\n  approver_declared_a_conflict_of_interest: false\n  vendor_name_written_in_capital_letters: false\n  payment_requested_during_business_hours: true\n  invoice_pdf_uses_a_landscape_layout: false\n  awaiting_purchase_order: false\n  vendor_tax_form_missing: false\n  duplicate_of_paid_invoice: false\n  vendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "The record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "turn_down",
   "put_on_hold",
   "go_ahead"
  ]
 },
 {
  "qid": "q0dfce0aae0",
  "kind": "choice",
  "text": "{\"deploy_id\": \"DEP-6799\", \"service\": \"notifier\", \"files_changed_soft_limit\": 30, \"contract_customer_asked_for_a_say_in_this_rollout\": true, \"commit_messages_written_in_a_detailed_style\": true, \"files_changed\": 17, \"rollout_approval_revoked\": false, \"commit_messages_written_in_a_casual_tone\": false, \"backout_plan_documented\": true, \"deploy_blocked_by_security_policy\": false, \"service_free_of_major_incidents\": true, \"deploy_title_written_in_normal_case\": true, \"canary_results_complete\": true, \"deploy_has_a_long_description\": true, \"deploy_prohibited_during_the_audit_window\": false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\n2. turn down if rollout_approval_revoked is true.\n3. put on hold if canary_results_complete is false or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\nOtherwise: go ahead.\nNever counted: backout_plan_documented, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nThe record is complete: nothing else applies.\n\nWhich action listed below fits this request best?",
  "options": [
   "send to a person",
   "go ahead",
   "put on hold"
  ]
 },
 {
  "qid": "qf5b3f03abf",
  "kind": "choice",
  "text": "# request record\nrequest_id = REQ-4760\nrequester = دلال ماهر الكيلاني\nnote = جميع البيانات المرفقة بطلب الوصول مطابقة للسجل.\naccess_days_approval_threshold = 30\nrequest_grants_admin_rights = false\nmfa_enrollment_complete = true\naccess_days = 12\naccount_suspended = false\nrequest_text_written_in_capital_letters = true\nrequester_not_barred_from_this_system = true\nrequested_role_permitted_by_policy = true\nlegal_preservation_order_on_the_account = false\nbusiness_justification_missing = false\nrequest_free_of_ethics_office_flags = true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if account_suspended is true or requested_role_permitted_by_policy is false or request_grants_admin_rights is true.\n2. ask_manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. defer if business_justification_missing is true or mfa_enrollment_complete is false or requester_not_barred_from_this_system is false or request_free_of_ethics_office_flags is false.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- approve: complete the action that was asked for\n- deny: kill this one off, it is off the table for good\n- defer: wait for that check then we will see\n- ask_manager: route the case to a decider so the requester knows the outcome\nThe record is complete: nothing else applies.\n\nIf you were deciding, which of the actions listed after this fits best?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q97c0340c3c",
  "kind": "choice",
  "text": "# record\ndeploy_id=DEP-2685\nservice=uploads\nservice_free_of_major_incidents=true\ndeploy_blocked_by_security_policy=false\ndeploy_title_written_in_normal_case=true\ndeploy_prohibited_during_the_audit_window=true\nrollout_approval_revoked=false\ndeploy_has_a_long_description=false\nfiles_changed_soft_limit=10\ncanary_results_complete=true\ncommit_messages_written_in_a_casual_tone=true\ncommit_messages_written_in_a_detailed_style=true\nfiles_changed=9\nbackout_plan_documented=true\ncontract_customer_asked_for_a_say_in_this_rollout=false",
  "question": "The record is complete: nothing else applies.\n\nAmong the actions listed after this, which best matches the request?",
  "options": [
   "pause",
   "stop",
   "continue"
  ]
 },
 {
  "qid": "qe5ea71ae18",
  "kind": "yes/no",
  "text": "{\n  \"ticket_id\":\"TCK-8857\",\n  \"customer\":\"Anders Haddad\",\n  \"legal_complaint_filed\":true,\n  \"item_excluded_by_policy\":false,\n  \"customer_message_written_in_a_casual_tone\":true,\n  \"item_return_received\":true,\n  \"claim_involves_a_media_inquiry\":false,\n  \"harmless_greeting_present_in_the_message\":true,\n  \"free_of_safety_incident_reports\":true,\n  \"claim_form_filled_in_with_the_usual_font\":true,\n  \"customer_message_is_short\":false,\n  \"claim_amount\":27.17,\n  \"claim_amount_hard_limit\":100.00,\n  \"proof_of_purchase_missing\":true,\n  \"claim_free_of_ombudsman_cases\":true\n}",
  "question": "Proposed action: turn down\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. turn down if item_excluded_by_policy is true or legal_complaint_filed is true or claim_amount is above claim_amount_hard_limit.\n3. send to a person if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: go ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa70481620d",
  "kind": "yes/no",
  "text": "ticket_id: TCK-5463\ncustomer: Nadia Petrov\nclaim_amount: 361.77\nclaim_amount_hard_limit: 1000.00\nfree_of_safety_incident_reports: true\ncustomer_message_written_in_a_formal_tone: false\nitem_return_not_yet_received: false\nitem_excluded_by_policy: true\nharmless_greeting_present_in_the_message: true\nclaim_free_of_ombudsman_cases: true\nfree_of_legal_complaints: true\nclaim_involves_a_media_inquiry: false\nclaim_form_filled_in_with_the_usual_font: true\ncustomer_message_is_short: true\nproof_of_purchase_attached: true",
  "question": "Proposed action: cancel\nWould the proposed action be the right move for the request in the record?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q2f1e76be56",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n* ticket id: TCK-5406\n* customer: Lena Lindqvist\n* customer message is short: yes\n* proof of purchase missing: no\n* item excluded by policy: no\n* claim amount: 500.01\n* free of safety incident reports: yes\n* item return not yet received: no\n* harmless greeting present in the message: yes\n* claim amount hard limit: 500.00\n* legal complaint filed: no\n* claim form filled in with the usual font: no\n* customer message written in a formal tone: no\n* claim free of ombudsman cases: yes\n* claim involves a media inquiry: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if claim_amount is above claim_amount_hard_limit.\n2. send_to_a_person if item_return_not_yet_received is true or item_excluded_by_policy is true or legal_complaint_filed is true or free_of_safety_incident_reports is false or claim_involves_a_media_inquiry is true.\n3. put_on_hold if proof_of_purchase_missing is true or claim_free_of_ombudsman_cases is false.\nOtherwise: go_ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "turn_down",
   "go_ahead",
   "send_to_a_person"
  ]
 },
 {
  "qid": "qf588f57e37",
  "kind": "choice",
  "text": "{\n    \"meta\": {\n        \"ticket_id\": \"TCK-6787\",\n        \"customer\": \"Kofi Okonkwo\"\n    },\n    \"metrics\": {\n        \"claim_amount_hard_limit\": 50.00,\n        \"claim_amount\": 30.90\n    },\n    \"signals\": {\n        \"legal_complaint_filed\": false,\n        \"claim_free_of_ombudsman_cases\": true,\n        \"item_excluded_by_policy\": false,\n        \"free_of_safety_incident_reports\": true,\n        \"claim_involves_a_media_inquiry\": true,\n        \"customer_message_written_in_a_casual_tone\": true,\n        \"harmless_greeting_present_in_the_message\": true,\n        \"customer_message_is_short\": true,\n        \"claim_form_filled_in_with_the_usual_font\": true,\n        \"item_return_received\": true,\n        \"proof_of_purchase_attached\": true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if free_of_safety_incident_reports is false or claim_free_of_ombudsman_cases is false.\n2. turn down if proof_of_purchase_attached is false or item_excluded_by_policy is true or claim_involves_a_media_inquiry is true or claim_amount is above claim_amount_hard_limit.\n3. put on hold if item_return_received is false.\nOtherwise: go ahead.\nNever counted: legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nAmong the actions listed after this, which best matches the request?",
  "options": [
   "turn down",
   "send to a person",
   "go ahead"
  ]
 },
 {
  "qid": "q84ed42df20",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- ticket id: TCK-6230\n- customer: Jonas Duarte\n- harmless greeting present in the message: yes\n- item return not yet received: no\n- customer message is short: yes\n- free of legal complaints: yes\n- claim free of ombudsman cases: yes\n- claim amount hard limit: 100.00\n- claim amount: 61.88\n- free of safety incident reports: yes\n- claim involves a media inquiry: no\n- proof of purchase missing: yes\n- item excluded by policy: no\n- customer message written in a casual tone: yes\n- claim form filled in with the usual font: yes",
  "question": "The record is complete: nothing else applies.\n\nAs the manager, which of the actions listed is the right call for this request?",
  "options": [
   "ask a human",
   "wait",
   "proceed"
  ]
 },
 {
  "qid": "q00e9ca2e00",
  "kind": "choice",
  "text": "{\n  \"request\": {\n    \"request_id\": \"REQ-8931\",\n    \"requester\": \"رنا جمال التونسي\",\n    \"note\": \"حالة الوصول إلى النظام استثنائية وتقع خارج نطاق صلاحية الكاتب.\"\n  },\n  \"figures\": {\n    \"access_days\": 9,\n    \"access_days_approval_threshold\": 14\n  },\n  \"checks\": {\n    \"request_grants_admin_rights\": false,\n    \"requested_role_forbidden_by_policy\": false,\n    \"account_suspended\": false,\n    \"requester_not_barred_from_this_system\": true,\n    \"business_justification_missing\": false,\n    \"legal_preservation_order_on_the_account\": false,\n    \"mfa_enrollment_incomplete\": false,\n    \"request_free_of_ethics_office_flags\": true,\n    \"request_text_written_in_capital_letters\": false\n  }\n}",
  "question": "Meanings:\n- QQT: allow the matter to be taken forward as planned\n- PCRB: route this matter to the individual empowered to decide\n- X: pump the brakes until more details show up\n- BJ: stop the work since it cannot move forward\nThe record is complete: nothing else applies.\n\nHey, which of the actions listed after this question is the right call here?",
  "options": [
   "PCRB",
   "QQT",
   "BJ"
  ]
 },
 {
  "qid": "q2ce80c7721",
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
  "qid": "q9b6931ad43",
  "kind": "yes/no",
  "text": "---\n# record\ndeploy_id: \"DEP-4792\"\nservice: \"profile\"\ndeploy_prohibited_during_the_audit_window: false\nbackout_plan_documented: true\ndeploy_blocked_by_security_policy: false\nservice_free_of_major_incidents: true\ndeploy_has_a_long_description: false\ncommit_messages_written_in_a_detailed_style: true\ncommit_messages_written_in_a_casual_tone: true\ncanary_results_incomplete: false\nrollout_approval_revoked: false\nfiles_changed_soft_limit: 50\ncontract_customer_asked_for_a_say_in_this_rollout: false\nfiles_changed: 24\ndeploy_title_written_in_normal_case: true",
  "question": "Proposed action: RFCB\nIs the proposed action ruled out by what the record says?",
  "definitions": "Meanings:\n- D: finish what was asked as stated, the way ahead is fully free\n- RFCB: keep waiting for the missing details\n- FXG: drop it right away\n- PK: send it up to the person who makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcf39bad1c3",
  "kind": "choice",
  "text": "# case\ndeploy_id                                         | DEP-3043\nservice                                           | reports\ndeploy_blocked_by_security_policy                 | true\nservice_free_of_major_incidents                   | true\ncommit_messages_written_in_a_terse_style          | false\nfiles_changed_soft_limit                          | 30\ncontract_customer_asked_for_a_say_in_this_rollout | true\ndeploy_has_a_long_description                     | false\ndeploy_title_written_in_normal_case               | true\ncanary_results_complete                           | true\nrollout_approval_revoked                          | false\nbackout_plan_missing                              | false\ncommit_messages_written_in_a_casual_tone          | true\ndeploy_prohibited_during_the_audit_window         | false\nfiles_changed                                     | 8",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QRH if backout_plan_missing is true or files_changed is above files_changed_soft_limit.\n2. PW if deploy_blocked_by_security_policy is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true.\n3. SMJT if service_free_of_major_incidents is false or contract_customer_asked_for_a_say_in_this_rollout is true.\nOtherwise: G.\nNever counted: canary_results_complete, deploy_has_a_long_description, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- QRH: be left pending until the review has been finished\n- G: go on and finish it\n- PW: drop it right away\n- SMJT: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies.\n\nWhich of the actions listed under the record would the requester see as the right call?",
  "options": [
   "G",
   "PW",
   "SMJT"
  ]
 },
 {
  "qid": "qf433bebeb1",
  "kind": "yes/no",
  "text": "# request record\nleave_id                                    | LVE-7329\nemployee                                    | رائد وليد الشهري\nnote                                        | المدير المباشر وافق على الطلب مسبقاً.\nrequest_falls_in_blackout_period            | true\nleave_request_written_in_a_formal_tone      | true\nleave_days                                  | 3\nrequests_team_free_of_harassment_complaints | true\nteam_coverage_arranged                      | true\nnotice_period_not_met                       | false\nleave_balance_available                     | true\nmedical_certificate_contested               | false\nno_union_grievance_raised_over_this_leave   | true\nlawyer_letter_received_about_this_leave     | false\nleave_days_soft_limit                       | 5",
  "question": "Proposed action: proceed\nDo the record's facts rule out the proposed action entirely?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qf54e4a548e",
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
  "qid": "q0c80fcbaba",
  "kind": "choice",
  "text": "---\n# request record\nrecord:\n    invoice_id: \"INV-7430\"\n    vendor: \"Stonebridge Foods\"\nnumbers:\n    amount_approval_threshold: 10000.00\n    amount: 1879.81\nflags:\n    invoice_pdf_uses_a_landscape_layout: false\n    vendor_tax_form_missing: false\n    duplicate_of_paid_invoice: false\n    vendor_name_written_in_capital_letters: false\n    purchase_order_received: true\n    vendor_filed_a_legal_claim_over_this_invoice: false\n    vendor_free_of_sanctions: true\n    payment_requested_during_business_hours: true\n    approver_free_of_conflicts_of_interest: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if vendor_filed_a_legal_claim_over_this_invoice is true or approver_free_of_conflicts_of_interest is false.\n2. cancel_order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. delay if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- delay: wait until a document arrives before you move forward with it\n- release: go ahead with the requested action\n- hand_to_a_person: hand it up to the person who decides\n- cancel_order: be halted at once and left unperformed\nThe record is complete: nothing else applies.\n\nConsidering what was asked and the facts available, which action below should be chosen?",
  "options": [
   "hand_to_a_person",
   "release",
   "delay"
  ]
 },
 {
  "qid": "q0a93e9ada6",
  "kind": "choice",
  "text": "# record\nrequest_id | REQ-2881\nrequester | Hugo Okonkwo\nlegal_preservation_order_on_the_account | false\nrequested_role_permitted_by_policy | true\naccess_days_approval_threshold | 7\nethics_office_flagged_the_request | false\nrequest_grants_admin_rights | false\nrequester_not_barred_from_this_system | true\nrequest_text_written_in_capital_letters | false\naccess_days | 6\nmfa_enrollment_complete | true\nbusiness_justification_provided | true\naccount_suspended | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if mfa_enrollment_complete is false or requester_not_barred_from_this_system is false or ethics_office_flagged_the_request is true.\n2. refuse if account_suspended is true or requested_role_permitted_by_policy is false.\n3. ask a human if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: approve.\nNever counted: business_justification_provided, request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nAmong the actions listed after this, which best matches the request?",
  "options": [
   "approve",
   "refuse",
   "delay"
  ]
 },
 {
  "qid": "qfcd21a3994",
  "kind": "yes/no",
  "text": "run_id=RUN-6657\nagent=delta\ntool_output_shows_tampering=false\nsteps_used=12\nlog_lines_written_in_a_verbose_style=false\ntask_description_incomplete=false\nsteps_used_hard_limit=12\nowner_sign_off_required_for_this_action=false\naction_permitted_by_security_policy=true\naction_free_of_ethics_concerns=true\nlast_tool_output_verified=true",
  "question": "Proposed action: go ahead\nWould the proposed action not be the appropriate course under the applicable procedure?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put on hold if last_tool_output_verified is false or task_description_incomplete is true.\n3. turn down if action_permitted_by_security_policy is false or owner_sign_off_required_for_this_action is true or steps_used is above steps_used_hard_limit.\nOtherwise: go ahead.\nNever counted: log_lines_written_in_a_verbose_style.\nMeanings:\n- send to a person: send this on to whoever decides\n- go ahead: proceed as asked since everything is cleared\n- turn down: refuse to act since the step is prohibited\n- put on hold: suspend action until the facts are confirmed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q17af2e6ecd",
  "kind": "yes/no",
  "text": "request_id=REQ-6525\nrequester=Jonas Hadjiev\nmfa_enrollment_complete=true\naccount_suspended=false\nrequested_role_forbidden_by_policy=false\nrequest_grants_admin_rights=true\nlegal_preservation_order_on_the_account=false\naccess_days=30\nbusiness_justification_provided=true\nrequester_not_barred_from_this_system=true\nrequest_text_written_in_capital_letters=false\naccess_days_approval_threshold=30\nrequest_free_of_ethics_office_flags=true",
  "question": "Proposed action: approve\nIs the proposed action the sensible thing to do for the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if mfa_enrollment_complete is false or requester_not_barred_from_this_system is false or request_free_of_ethics_office_flags is false.\n2. deny if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. ask manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: approve.\nNever counted: business_justification_provided, request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa5ce5c7cc2",
  "kind": "choice",
  "text": "run_id=RUN-7429\nagent=garnet\nowner_sign_off_required_for_this_action=false\nlog_lines_written_in_a_compact_style=true\nsteps_used_hard_limit=20\naction_permitted_by_security_policy=true\naction_free_of_ethics_concerns=true\ntool_output_shows_tampering=false\nlast_tool_output_verified=true\nsteps_used=11\ntask_description_incomplete=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. W if owner_sign_off_required_for_this_action is true.\n2. GJ if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is above steps_used_hard_limit.\n3. SDS if last_tool_output_verified is false.\nOtherwise: PNNB.\nNever counted: task_description_incomplete, action_free_of_ethics_concerns, log_lines_written_in_a_compact_style.\nMeanings:\n- W: hand the matter to a decider so the requester gets a verdict\n- GJ: toss it out, we are never doing this\n- PNNB: continue as requested with the path fully open\n- SDS: await further verification before any progression\nThe record is complete: nothing else applies.\n\nWhich action below would serve the person who made this request best?",
  "options": [
   "PNNB",
   "GJ",
   "SDS"
  ]
 },
 {
  "qid": "q6aad9fc011",
  "kind": "yes/no",
  "text": "---\n# extract\nleave_id: LVE-8876\nemployee: إياد بشار الحوراني\nnote: فترة الإجازة لا تتعارض مع أي مهام مجدولة للقسم.\nleave_request_written_in_a_formal_tone: false\nmedical_certificate_contested: false\nlawyer_letter_received_about_this_leave: false\nnotice_period_not_met: false\nleave_days: 1\nrequest_falls_in_blackout_period: false\nteam_coverage_not_arranged: false\nleave_balance_available: true\nrequests_team_free_of_harassment_complaints: true\nleave_days_soft_limit: 7\nunion_grievance_raised_over_this_leave: false",
  "question": "Proposed action: wait\nUpon audit, is the proposed action the correct determination given the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if team_coverage_not_arranged is true or medical_certificate_contested is true or leave_days is above leave_days_soft_limit.\n2. cancel if request_falls_in_blackout_period is true or lawyer_letter_received_about_this_leave is true.\n3. ask a human if union_grievance_raised_over_this_leave is true.\nOtherwise: proceed.\nNever counted: notice_period_not_met, leave_balance_available, requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q92c58e0d18",
  "kind": "choice",
  "text": "leave_id: LVE-9401\nemployee: Ingrid Castell\nrequests_team_free_of_harassment_complaints: true\nteam_coverage_arranged: true\nleave_days_soft_limit: 14\nno_union_grievance_raised_over_this_leave: true\nnotice_period_not_met: true\nlawyer_letter_received_about_this_leave: false\nleave_request_written_in_a_formal_tone: false\nleave_balance_available: true\nrequest_falls_in_blackout_period: true\nmedical_certificate_contested: false\nleave_days: 1",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if notice_period_not_met is true or team_coverage_arranged is false or leave_days is above leave_days_soft_limit.\n2. refuse if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. ask a human if leave_balance_available is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: leave_request_written_in_a_formal_tone.\nMeanings:\n- ask a human: pass the request to a decider\n- refuse: decline the request as the action is prohibited\n- approve: go on and finish it\n- delay: keep it in limbo until the verification has been confirmed\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "refuse",
   "approve",
   "delay"
  ]
 },
 {
  "qid": "qeaf6348be8",
  "kind": "choice",
  "text": "# extract\nrun_id: RUN-6489\nagent: atlas\nlast_tool_output_unverified: false\ntask_description_incomplete: false\nlog_lines_written_in_a_compact_style: false\naction_free_of_ethics_concerns: true\nsteps_used_hard_limit: 60\nowner_sign_off_required_for_this_action: false\nsteps_used: 4\ntool_output_shows_tampering: false\naction_forbidden_by_security_policy: false",
  "question": "Meanings:\n- pause: pause the request and gather more information before going on\n- continue: have the item pushed forward as the request stated\n- human review: toss it over to the one who makes the call\n- stop: stop this course of action at once\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "stop",
   "continue",
   "human review"
  ]
 },
 {
  "qid": "q93d5a9dfe0",
  "kind": "choice",
  "text": "# record\nrun_id | RUN-3936\nagent | cobalt\naction_free_of_ethics_concerns | true\nowner_sign_off_required_for_this_action | true\nlast_tool_output_unverified | false\ntool_output_shows_tampering | false\nsteps_used_hard_limit | 20\nlog_lines_written_in_a_compact_style | true\naction_forbidden_by_security_policy | false\ntask_description_complete | true\nsteps_used | 5",
  "question": "The record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "cancel",
   "ask_a_human",
   "proceed"
  ]
 },
 {
  "qid": "q954718960c",
  "kind": "yes/no",
  "text": "{\n  \"request\":{\n    \"request_id\":\"REQ-7782\",\n    \"requester\":\"Paolo Imai\"\n  },\n  \"figures\":{\n    \"access_days\":1,\n    \"access_days_approval_threshold\":60\n  },\n  \"checks\":{\n    \"requester_barred_from_this_system\":true,\n    \"request_grants_admin_rights\":false,\n    \"legal_preservation_order_on_the_account\":false,\n    \"requested_role_forbidden_by_policy\":false,\n    \"account_suspended\":false,\n    \"mfa_enrollment_incomplete\":false,\n    \"request_text_written_in_capital_letters\":false,\n    \"business_justification_missing\":false,\n    \"ethics_office_flagged_the_request\":false\n  }\n}",
  "question": "Proposed action: cancel\nHave the recorded facts ruled out the proposed action for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qd39c7cded6",
  "kind": "yes/no",
  "text": "leave_id: LVE-6998\nemployee: Paolo Ferreira\nlawyer_letter_received_about_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nunion_grievance_raised_over_this_leave: false\nnotice_period_met: true\nleave_balance_exhausted: false\nleave_days_soft_limit: 21\nrequest_falls_in_blackout_period: false\nteam_coverage_not_arranged: false\nleave_request_written_in_a_formal_tone: false\nmedical_certificate_contested: false\nleave_days: 2",
  "question": "Proposed action: refuse leave\nDo the facts here rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q98f1362692",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  deploy_id: DEP-8639\n  service: inventory\nnumbers:\n  files_changed_soft_limit: 30\n  files_changed: 30\nflags:\n  rollout_approval_revoked: false\n  commit_messages_written_in_a_terse_style: false\n  deploy_prohibited_during_the_audit_window: true\n  deploy_has_a_long_description: false\n  service_free_of_major_incidents: true\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  deploy_blocked_by_security_policy: false\n  deploy_title_written_in_normal_case: true\n  commit_messages_written_in_a_casual_tone: true\n  backout_plan_documented: true\n  canary_results_incomplete: false",
  "question": "Proposed action: go ahead\nSet beside the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. put on hold if canary_results_incomplete is true.\nOtherwise: go ahead.\nNever counted: backout_plan_documented, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfa9d67782c",
  "kind": "choice",
  "text": "{\n    \"request_id\": \"REQ-4568\",\n    \"requester\": \"Kofi Calloway\",\n    \"mfa_enrollment_complete\": true,\n    \"request_free_of_ethics_office_flags\": true,\n    \"business_justification_provided\": true,\n    \"legal_preservation_order_on_the_account\": true,\n    \"request_grants_admin_rights\": false,\n    \"access_days_approval_threshold\": 14,\n    \"access_days\": 7,\n    \"requester_not_barred_from_this_system\": true,\n    \"account_suspended\": false,\n    \"request_text_written_in_capital_letters\": false,\n    \"requested_role_forbidden_by_policy\": false\n}",
  "question": "Meanings:\n- delay: be parked until a verification has been logged\n- approve: run the task as it was asked, with nothing standing between it and completion\n- ask_a_human: give it to a person who has the authority to decide\n- refuse: halt the request at this point\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "approve",
   "ask_a_human",
   "delay"
  ]
 },
 {
  "qid": "qfe45ccd945",
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
  "qid": "q98f5ad2d2f",
  "kind": "yes/no",
  "text": "---\nmeta:\n  request_id: \"REQ-5278\"\n  requester: \"Marta Rossi\"\nmetrics:\n  access_days: 28\n  access_days_approval_threshold: 30\nsignals:\n  legal_preservation_order_on_the_account: false\n  requester_not_barred_from_this_system: true\n  requested_role_permitted_by_policy: false\n  account_suspended: false\n  request_grants_admin_rights: false\n  business_justification_missing: false\n  request_text_written_in_capital_letters: false\n  mfa_enrollment_complete: true\n  ethics_office_flagged_the_request: false",
  "question": "Proposed action: grant\nDo the details shown in the record rule out the proposed action here?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qab6af85db2",
  "kind": "yes/no",
  "text": "# case\nticket_id: TCK-6213\ncustomer: Anders Lindqvist\nclaim_form_filled_in_with_the_usual_font: true\nitem_excluded_by_policy: false\nclaim_amount: 1000.00\nfree_of_safety_incident_reports: true\ncustomer_message_is_short: true\nfree_of_legal_complaints: true\nitem_return_not_yet_received: false\nclaim_involves_a_media_inquiry: false\nclaim_amount_hard_limit: 1000.00\nharmless_greeting_present_in_the_message: false\nproof_of_purchase_missing: true\nclaim_free_of_ombudsman_cases: true\ncustomer_message_written_in_a_casual_tone: true",
  "question": "Proposed action: ask manager\nIs it not correct that the evidence points toward the proposed action, and it is not a poor choice?",
  "definitions": "Meanings:\n- deny: end this here and now\n- approve: keep going exactly as requested because every obstacle has cleared\n- defer: hold up for a sec until more info comes in\n- ask manager: route this matter to the individual empowered to decide\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q07342789c1",
  "kind": "yes/no",
  "text": "{\"deploy_id\":\"DEP-2388\",\"service\":\"mailer\",\"files_changed\":41,\"rollout_approval_revoked\":false,\"deploy_has_a_long_description\":false,\"deploy_prohibited_during_the_audit_window\":false,\"backout_plan_missing\":false,\"canary_results_incomplete\":false,\"deploy_title_written_in_normal_case\":true,\"commit_messages_written_in_a_detailed_style\":true,\"service_free_of_major_incidents\":true,\"files_changed_soft_limit\":50,\"commit_messages_written_in_a_casual_tone\":true,\"contract_customer_asked_for_a_say_in_this_rollout\":false,\"deploy_blocked_by_security_policy\":false}",
  "question": "Proposed action: go ahead\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_missing is true or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- send to a person: hand this to the person who decides\n- turn down: leave the requester without the result they asked for\n- put on hold: park this until a record turns up\n- go ahead: keep it moving forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcadc2c5cb4",
  "kind": "yes/no",
  "text": "{\n    \"run_id\": \"RUN-6263\",\n    \"agent\": \"fjord\",\n    \"tool_output_shows_tampering\": false,\n    \"task_description_incomplete\": false,\n    \"log_lines_written_in_a_compact_style\": true,\n    \"last_tool_output_unverified\": false,\n    \"action_free_of_ethics_concerns\": true,\n    \"steps_used_hard_limit\": 8,\n    \"steps_used\": 1,\n    \"owner_sign_off_required_for_this_action\": true,\n    \"action_permitted_by_security_policy\": true\n}",
  "question": "Proposed action: send to a person\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Meanings:\n- put on hold: keep waiting for the missing details\n- go ahead: complete the job as it was assigned\n- send to a person: be passed along to whoever makes the call\n- turn down: end this here and now\nThe record is complete: nothing else applies."
 }
]
