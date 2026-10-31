# G5-H blind read T46-blind_read-bc9e16d1-002 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8a/T46/qc/g5h/answers/T46-blind_read-bc9e16d1-002.json

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
  "qid": "q0fb11670b5",
  "kind": "choice",
  "text": "request_id: REQ-3589\nrequester: Paolo Imai\nrequested_role_permitted_by_policy: true\nrequest_text_written_in_capital_letters: false\nmfa_enrollment_complete: true\nlegal_preservation_order_on_the_account: false\nrequester_barred_from_this_system: false\naccess_days: 19\nbusiness_justification_provided: true\naccount_suspended: true\naccess_days_approval_threshold: 45\nrequest_grants_admin_rights: false\nrequest_free_of_ethics_office_flags: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. KWJ if business_justification_provided is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. NSMJ if mfa_enrollment_complete is false or request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n3. S if account_suspended is true or requested_role_permitted_by_policy is false.\nOtherwise: ZB.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- ZB: execute the requested action as nothing prevents it\n- NSMJ: transfer the case to the responsible decision maker for determination\n- S: terminate the process as continuation is prohibited\n- KWJ: park this until a record turns up\nThe record is complete: nothing else applies.\n\nWith reference to the record, which of the actions listed below is the appropriate course for the request?",
  "options": [
   "ZB",
   "NSMJ",
   "S"
  ]
 },
 {
  "qid": "qe5cb4496b4",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-5682\n- requester: Mira Vasquez\n- requested role forbidden by policy: no\n- requester barred from this system: no\n- account suspended: no\n- request grants admin rights: no\n- mfa enrollment incomplete: yes\n- ethics office flagged the request: no\n- business justification missing: no\n- legal preservation order on the account: no\n- access days: 7\n- request text written in capital letters: no\n- access days approval threshold: 14",
  "question": "Proposed action: approve\nAs an auditor, do the facts in the record rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. delay if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_missing, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q10d6fc96f0",
  "kind": "yes/no",
  "text": "---\nmeta:\n  leave_id: \"LVE-4267\"\n  employee: \"Yara Imai\"\nmetrics:\n  leave_days: 3\n  leave_days_soft_limit: 10\nsignals:\n  leave_request_written_in_a_formal_tone: true\n  lawyer_letter_received_about_this_leave: false\n  requests_team_free_of_harassment_complaints: true\n  team_coverage_arranged: false\n  notice_period_met: true\n  leave_balance_available: true\n  union_grievance_raised_over_this_leave: true\n  request_falls_in_blackout_period: false\n  medical_certificate_contested: false",
  "question": "Proposed action: approve\nIs the proposed action not the best thing to do with this?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_met is false or team_coverage_arranged is false or leave_balance_available is false or lawyer_letter_received_about_this_leave is true or leave_days is above leave_days_soft_limit.\n2. deny if request_falls_in_blackout_period is true.\n3. ask manager if medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false.\nOtherwise: approve.\nNever counted: union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1789b9bcd3",
  "kind": "choice",
  "text": "request_id | REQ-4301\nrequester | Aiko Vasquez\nbusiness_justification_provided | true\nlegal_preservation_order_on_the_account | false\naccount_suspended | false\nrequest_grants_admin_rights | false\nrequest_text_written_in_capital_letters | false\nrequest_free_of_ethics_office_flags | true\nrequested_role_forbidden_by_policy | false\nmfa_enrollment_complete | false\nrequester_barred_from_this_system | false\naccess_days_approval_threshold | 14\naccess_days | 7",
  "question": "Meanings:\n- ask a human: transfer it to the person with authority\n- proceed: have the item pushed forward as the request stated\n- cancel: be stopped and never carried out\n- wait: suspend progress until verification is received\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "ask a human",
   "cancel",
   "wait"
  ]
 },
 {
  "qid": "qaa25273fa4",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-2512\n- requester: رنا جمال التونسي\n- note: طلب الوصول يخالف القاعدة الثابتة، ولا يمكن تنفيذه.\n- access days approval threshold: 30\n- mfa enrollment complete: yes\n- request grants admin rights: no\n- request free of ethics office flags: yes\n- legal preservation order on the account: no\n- account suspended: no\n- business justification missing: no\n- request text written in capital letters: no\n- requested role permitted by policy: yes\n- requester not barred from this system: yes\n- access days: 17",
  "question": "Meanings:\n- ask_manager: route it elsewhere because a decider must weigh in\n- approve: have the plan kept moving as it was requested\n- deny: shut this down before it spreads into the workflow\n- defer: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies.\n\nConsidering what was asked and the facts available, which action below should be chosen?",
  "options": [
   "defer",
   "approve",
   "deny"
  ]
 },
 {
  "qid": "qf92ff6d4a9",
  "kind": "choice",
  "text": "{\"deploy_id\": \"DEP-6799\", \"service\": \"notifier\", \"files_changed_soft_limit\": 30, \"contract_customer_asked_for_a_say_in_this_rollout\": false, \"commit_messages_written_in_a_detailed_style\": true, \"files_changed\": 27, \"rollout_approval_revoked\": true, \"commit_messages_written_in_a_casual_tone\": true, \"backout_plan_documented\": true, \"deploy_blocked_by_security_policy\": false, \"service_free_of_major_incidents\": false, \"deploy_title_written_in_normal_case\": true, \"canary_results_complete\": true, \"deploy_has_a_long_description\": false, \"deploy_prohibited_during_the_audit_window\": false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\n2. turn down if rollout_approval_revoked is true.\n3. put on hold if canary_results_complete is false or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\nOtherwise: go ahead.\nNever counted: backout_plan_documented, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nThe record is complete: nothing else applies.\n\nWhich action listed below fits this request best?",
  "options": [
   "send to a person",
   "go ahead",
   "put on hold"
  ]
 },
 {
  "qid": "qf494ec02a9",
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
  "qid": "qdab1fc0b64",
  "kind": "choice",
  "text": "# record\nleave_id | LVE-6552\nemployee | نضال سمير الخوري\nnote | رصيد الإجازات الخاص بالموظف كافٍ لهذه المدة.\nleave_balance_exhausted | false\nrequests_team_free_of_harassment_complaints | true\nleave_request_written_in_a_formal_tone | true\nunion_grievance_raised_over_this_leave | false\nmedical_certificate_contested | false\nrequest_falls_in_blackout_period | false\nteam_coverage_arranged | true\nleave_days_soft_limit | 10\nleave_days | 8\nlawyer_letter_received_about_this_leave | false\nnotice_period_not_met | false",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed should the team commit to for this request, as the manager?",
  "options": [
   "go ahead",
   "send to a person",
   "turn down"
  ]
 },
 {
  "qid": "qb10b6cc52b",
  "kind": "choice",
  "text": "# case\ndeploy_id: DEP-3214\nservice: inventory\ncanary_results_incomplete: true\nfiles_changed_soft_limit: 50\nrollout_approval_revoked: false\ndeploy_prohibited_during_the_audit_window: false\nfiles_changed: 47\ndeploy_has_a_long_description: false\ndeploy_blocked_by_security_policy: false\ncommit_messages_written_in_a_casual_tone: true\nbackout_plan_missing: false\ncommit_messages_written_in_a_detailed_style: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_title_written_in_normal_case: true\nservice_free_of_major_incidents: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. human_review if canary_results_incomplete is true.\n2. stop if rollout_approval_revoked is true.\n3. pause if backout_plan_missing is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\nOtherwise: continue.\nNever counted: deploy_has_a_long_description, deploy_blocked_by_security_policy, service_free_of_major_incidents, contract_customer_asked_for_a_say_in_this_rollout, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- human_review: hand this over to whoever has the final say\n- pause: wait for the check and the requester will hear back later\n- stop: drop this right there, we are not touching it\n- continue: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies.\n\nAs the team lead, which of the actions listed should we go with for this request?",
  "options": [
   "human_review",
   "stop",
   "continue"
  ]
 },
 {
  "qid": "q9b2783034f",
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
  "qid": "q109161f8be",
  "kind": "choice",
  "text": "{\"leave_id\":\"LVE-2504\",\"employee\":\"مريم سعيد الكردي\",\"note\":\"طلب الإجازة مقدم في الموعد المحدد بالسياسة.\",\"union_grievance_raised_over_this_leave\":false,\"requests_team_free_of_harassment_complaints\":true,\"leave_days\":21,\"notice_period_met\":true,\"leave_request_written_in_a_formal_tone\":false,\"leave_balance_exhausted\":false,\"team_coverage_arranged\":true,\"leave_days_soft_limit\":21,\"request_falls_in_blackout_period\":false,\"medical_certificate_contested\":false,\"lawyer_letter_received_about_this_leave\":false}",
  "question": "Meanings:\n- 311: hold the request until the check is done\n- 38: end it so the requester sees their request closed\n- 6436: get referred to the person who decides\n- 3: keep going with it\nThe record is complete: nothing else applies.\n\nLooking across the actions listed, what would be the correct response to this request?",
  "options": [
   "3",
   "311",
   "6436"
  ]
 },
 {
  "qid": "q0bdea09aa8",
  "kind": "choice",
  "text": "# request record\ninvoice_id                                   | INV-2556\nvendor                                       | Cedar Foods\nduplicate_of_paid_invoice                    | false\nvendor_tax_form_missing                      | false\namount_approval_threshold                    | 5000.00\nvendor_name_written_in_capital_letters       | false\nvendor_on_sanctions_list                     | false\ninvoice_pdf_uses_a_portrait_layout           | true\nawaiting_purchase_order                      | false\nvendor_filed_a_legal_claim_over_this_invoice | false\namount                                       | 3036.37\napprover_declared_a_conflict_of_interest     | false\npayment_requested_during_business_hours      | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 7 if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. 6240 if amount is above amount_approval_threshold.\n3. 608 if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_on_sanctions_list is true or approver_declared_a_conflict_of_interest is true.\nOtherwise: 62.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- 62: keep moving on this one nothing is holding it up\n- 6240: route this to the one who signs off\n- 7: reject this item since it violates the policy\n- 608: park the file until the requester sends the document in\nThe record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "608",
   "6240",
   "62"
  ]
 },
 {
  "qid": "q9478c7f128",
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
  "qid": "qce76848230",
  "kind": "yes/no",
  "text": "invoice_id: INV-6949\nvendor: Fairview Labs\nduplicate_of_paid_invoice: true\npayment_requested_during_business_hours: true\namount_approval_threshold: 5000.00\nvendor_name_written_in_capital_letters: false\nvendor_on_sanctions_list: false\ninvoice_pdf_uses_a_portrait_layout: true\namount: 4458.79\nawaiting_purchase_order: false\nvendor_filed_a_legal_claim_over_this_invoice: false\napprover_declared_a_conflict_of_interest: false\nvendor_tax_form_missing: false",
  "question": "Proposed action: turn down\nBased on the record, can it be said the proposed action is not the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qca8d9f4f9e",
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
  "qid": "q58ab385e9e",
  "kind": "choice",
  "text": "{\n    \"record\":{\n        \"run_id\":\"RUN-2756\",\n        \"agent\":\"jasper\"\n    },\n    \"numbers\":{\n        \"steps_used\":4,\n        \"steps_used_hard_limit\":30\n    },\n    \"flags\":{\n        \"tool_output_shows_tampering\":false,\n        \"action_free_of_ethics_concerns\":true,\n        \"task_description_incomplete\":false,\n        \"action_forbidden_by_security_policy\":false,\n        \"log_lines_written_in_a_verbose_style\":false,\n        \"owner_sign_off_required_for_this_action\":false,\n        \"last_tool_output_unverified\":true\n    }\n}",
  "question": "Meanings:\n- 981: freeze progress until the paperwork arrives\n- 9542: proceed as requested as nothing impedes this course\n- 41: drop this right there, we are not touching it\n- 5: forward it to the decision maker\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "5",
   "9542",
   "981"
  ]
 },
 {
  "qid": "qc61fbee8c3",
  "kind": "choice",
  "text": "---\n# record\nrequest:\n    deploy_id: DEP-1964\n    service: reports\nfigures:\n    files_changed: 75\n    files_changed_soft_limit: 50\nchecks:\n    deploy_blocked_by_security_policy: false\n    commit_messages_written_in_a_detailed_style: true\n    backout_plan_documented: false\n    commit_messages_written_in_a_casual_tone: false\n    deploy_has_a_long_description: false\n    canary_results_incomplete: false\n    rollout_approval_revoked: false\n    deploy_title_written_in_normal_case: true\n    deploy_prohibited_during_the_audit_window: false\n    contract_customer_asked_for_a_say_in_this_rollout: false\n    service_free_of_major_incidents: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if backout_plan_documented is false.\n2. cancel if rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is at least files_changed_soft_limit.\n3. ask a human if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\nOtherwise: proceed.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- proceed: keep plugging away at it nothing else stands in the way\n- wait: hold this until a check comes back\n- cancel: kill this one off, it is off the table for good\n- ask a human: submit the question to the authorised decision maker\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "wait",
   "proceed",
   "cancel"
  ]
 },
 {
  "qid": "q86dde392c4",
  "kind": "yes/no",
  "text": "---\nmeta:\n  request_id: \"REQ-5278\"\n  requester: \"Marta Rossi\"\nmetrics:\n  access_days: 28\n  access_days_approval_threshold: 30\nsignals:\n  legal_preservation_order_on_the_account: false\n  requester_not_barred_from_this_system: true\n  requested_role_permitted_by_policy: false\n  account_suspended: false\n  request_grants_admin_rights: false\n  business_justification_missing: false\n  request_text_written_in_capital_letters: false\n  mfa_enrollment_complete: true\n  ethics_office_flagged_the_request: false",
  "question": "Proposed action: grant\nDo the details shown in the record rule out the proposed action here?",
  "definitions": "The record is complete: nothing else applies."
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
  "qid": "q19cb52ebca",
  "kind": "choice",
  "text": "request_id | REQ-6126\nrequester | Hugo Haddad\nrequest_free_of_ethics_office_flags | true\nbusiness_justification_missing | false\nrequester_barred_from_this_system | false\naccount_suspended | false\naccess_days_approval_threshold | 7\nrequest_text_written_in_capital_letters | false\nrequest_grants_admin_rights | false\naccess_days | 3\nrequested_role_permitted_by_policy | true\nlegal_preservation_order_on_the_account | false\nmfa_enrollment_incomplete | false",
  "question": "Meanings:\n- 7: pump the brakes until more details show up\n- 685: get referred to the person who decides\n- 1162: run the task as it was asked, with nothing standing between it and completion\n- 23: be halted at once and left unperformed\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "7",
   "685",
   "1162"
  ]
 },
 {
  "qid": "qf36569f6bb",
  "kind": "choice",
  "text": "---\n# case\nticket_id: TCK-2399\ncustomer: Ravi Vasquez\nclaim_involves_a_media_inquiry: false\ncustomer_message_written_in_a_casual_tone: true\nproof_of_purchase_missing: false\nitem_return_not_yet_received: false\nclaim_form_filled_in_with_the_usual_font: true\nclaim_amount_hard_limit: 1000.00\nitem_excluded_by_policy: false\nharmless_greeting_present_in_the_message: true\ncustomer_message_is_short: true\nclaim_amount: 290.43\nfree_of_safety_incident_reports: true\nlegal_complaint_filed: false\nclaim_free_of_ombudsman_cases: true",
  "question": "Meanings:\n- 7950: shelve the matter until more details come in\n- 78: shut off this process completely\n- 189: forward the case to the designated decision maker\n- 9: go on and finish it the path is clear\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "189",
   "7950",
   "9"
  ]
 },
 {
  "qid": "q65fd62d840",
  "kind": "yes/no",
  "text": "---\nrequest:\n  ticket_id: TCK-2093\n  customer: Sana Hadjiev\nfigures:\n  claim_amount_hard_limit: 50.00\n  claim_amount: 50.00\nchecks:\n  free_of_legal_complaints: true\n  claim_free_of_ombudsman_cases: true\n  customer_message_is_short: true\n  claim_involves_a_media_inquiry: false\n  harmless_greeting_present_in_the_message: true\n  claim_form_filled_in_with_the_usual_font: true\n  item_return_not_yet_received: false\n  item_excluded_by_policy: false\n  proof_of_purchase_attached: true\n  customer_message_written_in_a_formal_tone: true\n  free_of_safety_incident_reports: true",
  "question": "Proposed action: 7159\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Meanings:\n- 32: pause the request and gather more information before going on\n- 7159: proceed in accordance with the stated request\n- 210: route this matter to the individual empowered to decide\n- 9: bin this idea and keep it out of the flow\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q500f718b1d",
  "kind": "yes/no",
  "text": "leave_id: LVE-7827\nemployee: Nadia Mensah\nleave_request_written_in_a_formal_tone: false\nleave_days: 13\nrequests_team_free_of_harassment_complaints: true\nrequest_falls_in_blackout_period: false\nmedical_certificate_contested: false\nunion_grievance_raised_over_this_leave: false\nlawyer_letter_received_about_this_leave: false\nnotice_period_not_met: false\nleave_days_soft_limit: 14\nleave_balance_exhausted: false\nteam_coverage_arranged: true",
  "question": "Proposed action: CCV\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Meanings:\n- MM: pause and collect more information first\n- RKDZ: escalate this to someone senior who decides\n- CCV: stop the request so the requester gets nothing from it\n- R: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1919c8dbd4",
  "kind": "choice",
  "text": "---\n# record\nrecord:\n  request_id: REQ-8127\n  requester: Leila Haddad\nnumbers:\n  access_days_approval_threshold: 90\n  access_days: 4\nflags:\n  legal_preservation_order_on_the_account: false\n  business_justification_provided: true\n  request_grants_admin_rights: false\n  requested_role_permitted_by_policy: true\n  mfa_enrollment_complete: false\n  account_suspended: false\n  request_text_written_in_capital_letters: true\n  ethics_office_flagged_the_request: false\n  requester_barred_from_this_system: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. delay if requested_role_permitted_by_policy is false.\n3. refuse if mfa_enrollment_complete is false or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_provided, requester_barred_from_this_system, request_text_written_in_capital_letters.\nMeanings:\n- approve: continue with what was requested\n- refuse: kill this one off, it is off the table for good\n- delay: chill until the document turns up\n- ask_a_human: give it to a person who has the authority to decide\nThe record is complete: nothing else applies.\n\nChecklist: which of the actions listed below best answers the request?",
  "options": [
   "refuse",
   "delay",
   "approve"
  ]
 },
 {
  "qid": "q8df66a5b3b",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-6162\n  vendor: Oakmont Systems\nvalues:\n  amount: 66.96\n  amount_approval_threshold: 500.00\ntests:\n  invoice_pdf_uses_a_landscape_layout: false\n  vendor_filed_a_legal_claim_over_this_invoice: false\n  vendor_free_of_sanctions: false\n  payment_requested_during_business_hours: true\n  vendor_name_written_in_capital_letters: false\n  duplicate_of_paid_invoice: false\n  purchase_order_received: true\n  approver_free_of_conflicts_of_interest: true\n  vendor_tax_form_on_file: true",
  "question": "Proposed action: cancel\nIs it not so that the proposed action we have on the table is not a poor choice for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q7298ac91f7",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"leave_id\": \"LVE-4716\",\n        \"employee\": \"Tomas Moreau\"\n    },\n    \"values\": {\n        \"leave_days_soft_limit\": 7,\n        \"leave_days\": 8\n    },\n    \"tests\": {\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"leave_balance_available\": true,\n        \"notice_period_not_met\": false,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"request_falls_in_blackout_period\": false,\n        \"leave_request_written_in_a_formal_tone\": false,\n        \"team_coverage_not_arranged\": false,\n        \"union_grievance_raised_over_this_leave\": false\n    }\n}",
  "question": "Proposed action: DRV\nDo the facts we have help rule out the proposed action here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. DRV if notice_period_not_met is true or team_coverage_not_arranged is true or leave_days is above leave_days_soft_limit.\n2. DT if request_falls_in_blackout_period is true.\n3. DBDV if leave_balance_available is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or union_grievance_raised_over_this_leave is true.\nOtherwise: D.\nNever counted: lawyer_letter_received_about_this_leave, leave_request_written_in_a_formal_tone.\nMeanings:\n- DRV: hang tight until we get the check back\n- DBDV: give it to the person in charge of the call\n- DT: end it so the requester sees their request closed\n- D: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd5e7a81e87",
  "kind": "yes/no",
  "text": "# request record\ndeploy_id=DEP-6882\nservice=notifier\ndeploy_blocked_by_security_policy=false\nfiles_changed=80\ndeploy_has_a_long_description=false\ndeploy_prohibited_during_the_audit_window=false\nservice_free_of_major_incidents=true\ncommit_messages_written_in_a_casual_tone=true\ncontract_customer_asked_for_a_say_in_this_rollout=false\ncommit_messages_written_in_a_terse_style=false\nfiles_changed_soft_limit=80\ncanary_results_incomplete=false\ndeploy_title_written_in_normal_case=true\nrollout_approval_revoked=false\nbackout_plan_documented=true",
  "question": "Proposed action: QJFN\nOverall, would you say the proposed action suits the request in the record?",
  "definitions": "Meanings:\n- JWF: stop this course of action at once\n- BC: forward the case to the designated decision maker\n- QJFN: hold off until the check has been completed by the team\n- S: proceed in accordance with the stated request\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q87f735979d",
  "kind": "yes/no",
  "text": "---\n# case\ndeploy_id: \"DEP-3754\"\nservice: \"inventory\"\ndeploy_prohibited_during_the_audit_window: false\nbackout_plan_missing: false\nrollout_approval_revoked: false\ndeploy_title_written_in_normal_case: true\nfiles_changed_soft_limit: 80\nfiles_changed: 9\nservice_free_of_major_incidents: false\ncommit_messages_written_in_a_casual_tone: true\ncanary_results_complete: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_blocked_by_security_policy: false\ncommit_messages_written_in_a_detailed_style: true\ndeploy_has_a_long_description: false",
  "question": "Proposed action: proceed\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Meanings:\n- wait: stay put until the check is finished\n- proceed: continue with the request as nothing obstructs it\n- cancel: reject the petition as the action is unauthorized\n- ask_a_human: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies."
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
  "qid": "q9956f49356",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"invoice_id\": \"INV-6116\",\n        \"vendor\": \"Redwood Logistics\"\n    },\n    \"metrics\": {\n        \"amount_approval_threshold\": 2500.00,\n        \"amount\": 1562.42\n    },\n    \"signals\": {\n        \"approver_declared_a_conflict_of_interest\": false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": false,\n        \"awaiting_purchase_order\": true,\n        \"vendor_name_written_in_capital_letters\": true,\n        \"payment_requested_during_business_hours\": true,\n        \"vendor_on_sanctions_list\": true,\n        \"invoice_pdf_uses_a_landscape_layout\": false,\n        \"vendor_tax_form_missing\": false,\n        \"duplicate_of_paid_invoice\": false\n    }\n}",
  "question": "Proposed action: refuse\nWould the proposed action be the right answer to what this request calls for?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if approver_declared_a_conflict_of_interest is true.\n2. refuse if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- delay: defer further action pending verification of the document\n- refuse: kill this one off\n- ask a human: hand it up to the person who decides\n- approve: just crack on with it there is nothing in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb8557bec5b",
  "kind": "choice",
  "text": "{\n  \"leave_id\": \"LVE-2090\",\n  \"employee\": \"أروى حكيم المالكي\",\n  \"note\": \"المستندات المطلوبة كلها مرفقة بالطلب.\",\n  \"requests_team_free_of_harassment_complaints\": true,\n  \"no_union_grievance_raised_over_this_leave\": true,\n  \"leave_balance_available\": false,\n  \"request_falls_in_blackout_period\": false,\n  \"leave_days\": 5,\n  \"notice_period_met\": false,\n  \"medical_certificate_contested\": false,\n  \"leave_days_soft_limit\": 10,\n  \"team_coverage_not_arranged\": false,\n  \"lawyer_letter_received_about_this_leave\": true,\n  \"leave_request_written_in_a_formal_tone\": false\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. defer if notice_period_met is false or team_coverage_not_arranged is true.\n3. deny if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\nOtherwise: approve.\nNever counted: leave_balance_available, medical_certificate_contested, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this would you pick for this request?",
  "options": [
   "deny",
   "ask_manager",
   "approve"
  ]
 },
 {
  "qid": "q00ef532f61",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n  deploy_id: DEP-9075\n  service: checkout\nvalues:\n  files_changed_soft_limit: 10\n  files_changed: 9\ntests:\n  deploy_blocked_by_security_policy: false\n  deploy_has_a_long_description: true\n  commit_messages_written_in_a_casual_tone: false\n  canary_results_complete: true\n  backout_plan_missing: false\n  deploy_title_written_in_normal_case: true\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  service_free_of_major_incidents: false\n  rollout_approval_revoked: false\n  deploy_prohibited_during_the_audit_window: false\n  commit_messages_written_in_a_terse_style: true",
  "question": "Proposed action: proceed\nIs the proposed action correct for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qd149b0d775",
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
  "qid": "q89e0618813",
  "kind": "yes/no",
  "text": "{\n    \"record\":{\n        \"deploy_id\":\"DEP-7513\",\n        \"service\":\"auth_proxy\"\n    },\n    \"numbers\":{\n        \"files_changed\":39,\n        \"files_changed_soft_limit\":80\n    },\n    \"flags\":{\n        \"deploy_prohibited_during_the_audit_window\":true,\n        \"deploy_blocked_by_security_policy\":false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\":false,\n        \"canary_results_complete\":true,\n        \"service_free_of_major_incidents\":true,\n        \"rollout_approval_revoked\":true,\n        \"deploy_has_a_long_description\":false,\n        \"deploy_title_written_in_normal_case\":true,\n        \"commit_messages_written_in_a_detailed_style\":true,\n        \"commit_messages_written_in_a_casual_tone\":true,\n        \"backout_plan_documented\":true\n    }\n}",
  "question": "Proposed action: turn down\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if canary_results_complete is false.\n2. turn down if rollout_approval_revoked is true.\n3. put on hold if backout_plan_documented is false or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\nOtherwise: go ahead.\nNever counted: deploy_has_a_long_description, deploy_blocked_by_security_policy, service_free_of_major_incidents, contract_customer_asked_for_a_say_in_this_rollout, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- turn down: shut this down right away, we are staying clear of it\n- send to a person: hand this over to whoever has the final say\n- put on hold: chill until the document turns up\n- go ahead: proceed and the requester gets what they asked\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfc3f4c122b",
  "kind": "yes/no",
  "text": "# record\nleave_id: LVE-4344\nemployee: Yara Whitcombe\nleave_balance_exhausted: false\nunion_grievance_raised_over_this_leave: false\nmedical_certificate_contested: false\nleave_request_written_in_a_formal_tone: false\nleave_days_soft_limit: 21\nteam_coverage_arranged: true\nrequest_falls_in_blackout_period: false\nnotice_period_met: true\nrequests_team_free_of_harassment_complaints: true\nleave_days: 12\nlawyer_letter_received_about_this_leave: true",
  "question": "Proposed action: ask manager\nIs the proposed action the right move for this request, given the facts involved?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if notice_period_met is false or request_falls_in_blackout_period is true.\n2. defer if team_coverage_arranged is false or leave_balance_exhausted is true or leave_days is above leave_days_soft_limit.\n3. ask manager if medical_certificate_contested is true or union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- ask manager: transfer it to the person with authority\n- defer: keep waiting for the missing details\n- approve: carry out the task as instructed without any obstacle\n- deny: withdraw from the step as it is forbidden\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6bcd58e15c",
  "kind": "yes/no",
  "text": "{\n    \"meta\":{\n        \"invoice_id\":\"INV-7085\",\n        \"vendor\":\"Harbor Works\"\n    },\n    \"metrics\":{\n        \"amount\":10335.11,\n        \"amount_approval_threshold\":25000.00\n    },\n    \"signals\":{\n        \"approver_declared_a_conflict_of_interest\":false,\n        \"vendor_free_of_sanctions\":false,\n        \"invoice_pdf_uses_a_portrait_layout\":true,\n        \"vendor_tax_form_missing\":false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n        \"purchase_order_received\":true,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_name_written_in_capital_letters\":true,\n        \"duplicate_of_paid_invoice\":false\n    }\n}",
  "question": "Proposed action: hold\nIs the proposed action not a sound choice for this situation?",
  "definitions": "Meanings:\n- reject: end this effort right away\n- escalate: get sent upward to the one who decides\n- pay: keep going with it nothing is blocking you\n- hold: withhold action until supporting information is supplied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q81ec9340f9",
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
  "qid": "q6353740e06",
  "kind": "choice",
  "text": "request_id: REQ-2560\nrequester: Hugo Okafor\nrequest_free_of_ethics_office_flags: true\naccess_days: 54\nrequester_not_barred_from_this_system: true\naccess_days_approval_threshold: 90\nrequested_role_forbidden_by_policy: true\nlegal_preservation_order_on_the_account: false\nrequest_grants_admin_rights: false\nbusiness_justification_provided: true\nmfa_enrollment_complete: true\nrequest_text_written_in_capital_letters: false\naccount_suspended: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_provided is false or requested_role_forbidden_by_policy is true.\n2. page oncall if mfa_enrollment_complete is false or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. block access if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: allow.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "page oncall",
   "allow",
   "quarantine"
  ]
 },
 {
  "qid": "qed9fc90ffa",
  "kind": "yes/no",
  "text": "{\"deploy_id\": \"DEP-9349\", \"service\": \"inventory\", \"canary_results_incomplete\": false, \"service_free_of_major_incidents\": true, \"deploy_prohibited_during_the_audit_window\": false, \"deploy_title_written_in_normal_case\": true, \"files_changed\": 10, \"deploy_has_a_long_description\": false, \"deploy_blocked_by_security_policy\": false, \"commit_messages_written_in_a_terse_style\": false, \"rollout_approval_revoked\": true, \"contract_customer_asked_for_a_say_in_this_rollout\": false, \"commit_messages_written_in_a_casual_tone\": true, \"backout_plan_documented\": true, \"files_changed_soft_limit\": 10}",
  "question": "Proposed action: DXZP\nDo the record's facts rule out the proposed action entirely?",
  "definitions": "Meanings:\n- PM: hand the matter to a decider so the requester gets a verdict\n- KXS: keep it moving forward\n- R: stay put until the check is finished\n- DXZP: be rejected in full and never acted upon\nThe record is complete: nothing else applies."
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
  "qid": "q069bea823f",
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
  "qid": "q84e5edceec",
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
  "qid": "q1e3a75fc4d",
  "kind": "yes/no",
  "text": "{\n  \"ticket_id\":\"TCK-8857\",\n  \"customer\":\"Anders Haddad\",\n  \"legal_complaint_filed\":true,\n  \"item_excluded_by_policy\":false,\n  \"customer_message_written_in_a_casual_tone\":true,\n  \"item_return_received\":true,\n  \"claim_involves_a_media_inquiry\":false,\n  \"harmless_greeting_present_in_the_message\":true,\n  \"free_of_safety_incident_reports\":true,\n  \"claim_form_filled_in_with_the_usual_font\":true,\n  \"customer_message_is_short\":false,\n  \"claim_amount\":27.17,\n  \"claim_amount_hard_limit\":100.00,\n  \"proof_of_purchase_missing\":true,\n  \"claim_free_of_ombudsman_cases\":true\n}",
  "question": "Proposed action: turn down\nFrom an audit standpoint, have the facts in the record ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. turn down if item_excluded_by_policy is true or legal_complaint_filed is true or claim_amount is above claim_amount_hard_limit.\n3. send to a person if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: go ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe83a0035ba",
  "kind": "yes/no",
  "text": "ticket_id | TCK-8915\ncustomer | Leila Mensah\nharmless_greeting_present_in_the_message | false\nfree_of_safety_incident_reports | true\nclaim_amount_hard_limit | 100.00\nitem_excluded_by_policy | false\nfree_of_legal_complaints | true\ncustomer_message_is_short | true\nclaim_free_of_ombudsman_cases | true\nclaim_form_filled_in_with_the_usual_font | true\nclaim_involves_a_media_inquiry | false\ncustomer_message_written_in_a_casual_tone | false\nproof_of_purchase_attached | true\nclaim_amount | 89.73\nitem_return_received | true",
  "question": "Proposed action: approve\nDoes the record itself rule out the proposed action?",
  "definitions": "Meanings:\n- delay: hold off until the check has been completed by the team\n- refuse: terminate the process as continuation is prohibited\n- ask a human: send it onward because someone else must decide\n- approve: proceed as asked since everything is cleared\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3229d3d396",
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
  "qid": "q20fd06f26a",
  "kind": "yes/no",
  "text": "deploy_id: DEP-3754\nservice: inventory\nfiles_changed: 9\ndeploy_title_written_in_normal_case: true\nfiles_changed_soft_limit: 80\ndeploy_prohibited_during_the_audit_window: false\nservice_free_of_major_incidents: false\ncommit_messages_written_in_a_casual_tone: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\nbackout_plan_missing: false\nrollout_approval_revoked: false\ndeploy_has_a_long_description: false\ndeploy_blocked_by_security_policy: false\ncanary_results_complete: true\ncommit_messages_written_in_a_detailed_style: true",
  "question": "Proposed action: proceed\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Meanings:\n- wait: stay put until the check is finished\n- proceed: continue with the request as nothing obstructs it\n- cancel: reject the petition as the action is unauthorized\n- ask_a_human: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd0baafc98f",
  "kind": "choice",
  "text": "# record\nleave_id | LVE-9120\nemployee | Ravi Okonkwo\nunion_grievance_raised_over_this_leave | false\nleave_days_soft_limit | 3\nlawyer_letter_received_about_this_leave | false\nrequest_falls_in_blackout_period | false\nleave_days | 1\nteam_coverage_arranged | true\nrequests_team_free_of_harassment_complaints | true\nleave_balance_available | false\nmedical_certificate_contested | false\nnotice_period_not_met | false\nleave_request_written_in_a_formal_tone | false",
  "question": "Meanings:\n- L: decline the request as the action is prohibited\n- LVVP: carry out the task as instructed without any obstacle\n- VMH: refer this item to the person who holds decision authority\n- SP: pause the request and gather more information before going on\nThe record is complete: nothing else applies.\n\nLooking across the actions listed, what would be the correct response to this request?",
  "options": [
   "LVVP",
   "L",
   "SP"
  ]
 },
 {
  "qid": "qb7f9476b5f",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-4248\",\n  \"vendor\":\"Oakmont Partners\",\n  \"awaiting_purchase_order\":false,\n  \"invoice_pdf_uses_a_portrait_layout\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"approver_free_of_conflicts_of_interest\":true,\n  \"vendor_name_written_in_capital_letters\":false,\n  \"vendor_tax_form_missing\":false,\n  \"amount\":142.15,\n  \"vendor_free_of_sanctions\":true,\n  \"vendor_filed_a_legal_claim_over_this_invoice\":true,\n  \"amount_approval_threshold\":500.00,\n  \"duplicate_of_paid_invoice\":false\n}",
  "question": "Proposed action: ask_manager\nJudging from what the record shows, is the proposed action not the correct decision?",
  "definitions": "Meanings:\n- ask_manager: escalate the matter to the accountable decision maker\n- deny: refuse the request because it crosses a clear line\n- approve: keep going exactly as requested because every obstacle has cleared\n- defer: hold off until the check has been completed by the team\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3fad07d6e3",
  "kind": "choice",
  "text": "---\nrequest:\n  invoice_id: INV-2135\n  vendor: Ironleaf Partners\nfigures:\n  amount: 3075.56\n  amount_approval_threshold: 5000.00\nchecks:\n  vendor_filed_a_legal_claim_over_this_invoice: false\n  payment_requested_during_business_hours: true\n  duplicate_of_paid_invoice: false\n  invoice_pdf_uses_a_portrait_layout: false\n  vendor_on_sanctions_list: false\n  vendor_tax_form_missing: false\n  vendor_name_written_in_capital_letters: false\n  awaiting_purchase_order: false\n  approver_free_of_conflicts_of_interest: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. ask a human if vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. refuse if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or approver_free_of_conflicts_of_interest is false or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- ask a human: hand this to the person who decides\n- delay: hold the request so the requester waits for their check\n- approve: run with it carry on as you were\n- refuse: decline the request as the action is prohibited\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "ask a human",
   "approve",
   "refuse"
  ]
 }
]
