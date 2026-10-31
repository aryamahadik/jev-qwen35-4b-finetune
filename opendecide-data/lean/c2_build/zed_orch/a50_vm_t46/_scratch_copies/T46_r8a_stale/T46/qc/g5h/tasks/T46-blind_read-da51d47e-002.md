# G5-H blind read T46-blind_read-da51d47e-002 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8a/T46/qc/g5h/answers/T46-blind_read-da51d47e-002.json

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
  "qid": "q4e8df6f9b4",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-4615\n  vendor: Stonebridge Works\nvalues:\n  amount_approval_threshold: 10000.00\n  amount: 6017.96\ntests:\n  payment_requested_during_business_hours: false\n  awaiting_purchase_order: false\n  vendor_free_of_sanctions: true\n  vendor_name_written_in_capital_letters: true\n  vendor_tax_form_missing: true\n  invoice_pdf_uses_a_landscape_layout: true\n  duplicate_of_paid_invoice: false\n  approver_free_of_conflicts_of_interest: true\n  vendor_filed_a_legal_claim_over_this_invoice: true",
  "question": "Proposed action: delay\nIs it not the case that the facts available line up with the proposed action and it is not out of step?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. cancel order if vendor_free_of_sanctions is false.\n3. hand to a person if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_free_of_conflicts_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- cancel order: decline the request as the action is prohibited\n- delay: wait for the document to come through\n- hand to a person: be routed to whoever holds the decision\n- release: advance the task as stated without any blockers\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2acc919317",
  "kind": "yes/no",
  "text": "---\n# record\nmeta:\n    request_id: \"REQ-8884\"\n    requester: \"Tomas Adeyemi\"\nmetrics:\n    access_days_approval_threshold: 30\n    access_days: 11\nsignals:\n    requested_role_forbidden_by_policy: false\n    legal_preservation_order_on_the_account: false\n    request_text_written_in_capital_letters: false\n    mfa_enrollment_incomplete: false\n    requester_not_barred_from_this_system: true\n    request_grants_admin_rights: false\n    account_suspended: true\n    ethics_office_flagged_the_request: false\n    business_justification_missing: false",
  "question": "Proposed action: 4322\nIs it not so that the proposed action, looked at fresh, is not a bad call for the job?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 4322 if business_justification_missing is true or requested_role_forbidden_by_policy is true.\n2. 8 if mfa_enrollment_incomplete is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is at least access_days_approval_threshold.\n3. 65 if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: 636.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- 65: toss it out, we are never doing this\n- 636: finish it so the requester has their answer\n- 8: be forwarded to the person in charge\n- 4322: stay put until the check is finished\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8649961c36",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n* run id: RUN-5229\n* agent: helix\n* tool output shows tampering: no\n* task description incomplete: no\n* log lines written in a compact style: yes\n* action forbidden by security policy: no\n* owner sign off required for this action: no\n* action free of ethics concerns: yes\n* steps used: 40\n* last tool output verified: no\n* steps used hard limit: 40",
  "question": "Meanings:\n- DFL: hold off until the check clears\n- ZH: have the item pushed forward as the request stated\n- SHSK: drop it right away\n- C: delegate the call to whoever holds authority\nThe record is complete: nothing else applies.\n\nWhich of the actions below is the right decision for this request?",
  "options": [
   "DFL",
   "C",
   "ZH"
  ]
 },
 {
  "qid": "q06b15d3362",
  "kind": "yes/no",
  "text": "---\n# record\nrun_id: RUN-9481\nagent: fjord\nsteps_used: 5\nsteps_used_hard_limit: 20\nowner_sign_off_required_for_this_action: false\nlog_lines_written_in_a_compact_style: true\nlast_tool_output_verified: true\ntool_output_shows_tampering: false\ntask_description_complete: true\naction_forbidden_by_security_policy: true\naction_free_of_ethics_concerns: true",
  "question": "Proposed action: 7\nReviewing this file as an auditor, is the proposed action not the correct step?",
  "definitions": "Meanings:\n- 7: ditch the whole thing, nobody should act on it\n- 6528: carry out the task as instructed without any obstacle\n- 338: route the case to a decider so the requester knows the outcome\n- 51: hold the request so the requester waits for their check\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q58f6c1bbd8",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n* deploy id: DEP-5133\n* service: inventory\n* contract customer asked for a say in this rollout: no\n* deploy has a long description: no\n* commit messages written in a casual tone: yes\n* deploy blocked by security policy: no\n* deploy prohibited during the audit window: no\n* backout plan missing: no\n* deploy title written in normal case: yes\n* files changed: 7\n* service free of major incidents: yes\n* commit messages written in a detailed style: yes\n* files changed soft limit: 20\n* canary results incomplete: no\n* rollout approval revoked: no",
  "question": "Proposed action: GCT\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. GCT if backout_plan_missing is true or rollout_approval_revoked is true or files_changed is at least files_changed_soft_limit.\n2. CQFW if contract_customer_asked_for_a_say_in_this_rollout is true.\n3. X if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\nOtherwise: DN.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- CQFW: route it elsewhere because a decider must weigh in\n- DN: go ahead with the requested action\n- X: be turned away and treated as off limits\n- GCT: keep it in limbo until the verification has been confirmed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd424494bb8",
  "kind": "yes/no",
  "text": "# record\nleave_id: LVE-3295\nemployee: Ingrid Imai\nrequest_falls_in_blackout_period: true\nleave_days_soft_limit: 10\nrequests_team_free_of_harassment_complaints: true\nmedical_certificate_contested: false\nno_union_grievance_raised_over_this_leave: true\nleave_days: 6\nleave_request_written_in_a_formal_tone: false\nleave_balance_exhausted: true\nlawyer_letter_received_about_this_leave: false\nteam_coverage_arranged: true\nnotice_period_met: true",
  "question": "Proposed action: defer\nIs the proposed action not the best thing to do with this?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_met is false or team_coverage_arranged is false or leave_balance_exhausted is true or lawyer_letter_received_about_this_leave is true or leave_days is above leave_days_soft_limit.\n2. deny if request_falls_in_blackout_period is true.\n3. ask_manager if medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false.\nOtherwise: approve.\nNever counted: no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa96374303f",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- leave id: LVE-9635\n- employee: Nadia Moreau\n- leave balance available: yes\n- lawyer letter received about this leave: yes\n- requests team free of harassment complaints: yes\n- leave days: 5\n- leave request written in a formal tone: yes\n- union grievance raised over this leave: no\n- request falls in blackout period: no\n- notice period not met: no\n- leave days soft limit: 7\n- team coverage not arranged: no\n- medical certificate contested: yes",
  "question": "Proposed action: deny\nShould the proposed action be taken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_not_met is true or team_coverage_not_arranged is true or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. deny if medical_certificate_contested is true.\n3. ask manager if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- defer: be held back until a check or document arrives\n- approve: complete the action that was asked for\n- deny: veto this move and leave it there\n- ask manager: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe429f7cd01",
  "kind": "yes/no",
  "text": "{\n    \"request_id\":\"REQ-3577\",\n    \"requester\":\"Priya Mensah\",\n    \"request_text_written_in_capital_letters\":true,\n    \"business_justification_provided\":true,\n    \"requested_role_forbidden_by_policy\":false,\n    \"access_days_approval_threshold\":14,\n    \"request_free_of_ethics_office_flags\":true,\n    \"mfa_enrollment_complete\":true,\n    \"access_days\":7,\n    \"requester_barred_from_this_system\":false,\n    \"account_suspended\":false,\n    \"legal_preservation_order_on_the_account\":false,\n    \"request_grants_admin_rights\":false\n}",
  "question": "Proposed action: quarantine\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. block_access if account_suspended is true or requested_role_forbidden_by_policy is true or request_grants_admin_rights is true.\n2. page_oncall if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. quarantine if business_justification_provided is false or mfa_enrollment_complete is false or requester_barred_from_this_system is true or request_free_of_ethics_office_flags is false.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- quarantine: park the file until the requester sends the document in\n- block_access: refuse this request entirely\n- allow: continue so the requester receives the result\n- page_oncall: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5f126b70fd",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- deploy id: DEP-5059\n- service: auth_proxy\n- service free of major incidents: yes\n- contract customer asked for a say in this rollout: no\n- commit messages written in a detailed style: yes\n- deploy prohibited during the audit window: no\n- files changed soft limit: 15\n- deploy title written in normal case: yes\n- backout plan missing: no\n- canary results complete: no\n- commit messages written in a casual tone: yes\n- rollout approval revoked: no\n- deploy has a long description: no\n- files changed: 14\n- deploy blocked by security policy: no",
  "question": "Proposed action: pause\nIs the proposed action the right move for this request, given the facts involved?",
  "definitions": "Meanings:\n- human_review: escalate the matter to the accountable decision maker\n- stop: toss it out, we are never doing this\n- continue: just crack on with it there is nothing in the way\n- pause: hold the request until a check is completed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2afb36cd02",
  "kind": "yes/no",
  "text": "---\ndeploy_id: DEP-9318\nservice: search\ncommit_messages_written_in_a_casual_tone: true\ndeploy_has_a_long_description: false\ncanary_results_incomplete: false\ndeploy_blocked_by_security_policy: false\ndeploy_title_written_in_normal_case: false\nbackout_plan_missing: false\ncommit_messages_written_in_a_detailed_style: true\nfiles_changed_soft_limit: 10\ncontract_customer_asked_for_a_say_in_this_rollout: false\nservice_free_of_major_incidents: true\nrollout_approval_revoked: false\ndeploy_prohibited_during_the_audit_window: true\nfiles_changed: 7",
  "question": "Proposed action: stop\nAs a reviewer checking the file, is the proposed action not a sound decision here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. stop if canary_results_incomplete is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true.\n2. human review if backout_plan_missing is true or deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\n3. pause if files_changed is above files_changed_soft_limit.\nOtherwise: continue.\nNever counted: deploy_has_a_long_description, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- continue: allow the matter to be taken forward as planned\n- stop: drop this request from the queue\n- human review: hand it up to the person who decides\n- pause: be parked until a verification has been logged\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qefb302ca6c",
  "kind": "yes/no",
  "text": "---\n# case\nsubject:\n    deploy_id: DEP-4450\n    service: checkout\namounts:\n    files_changed: 15\n    files_changed_soft_limit: 15\nchecks:\n    commit_messages_written_in_a_terse_style: false\n    contract_customer_asked_for_a_say_in_this_rollout: false\n    backout_plan_missing: false\n    canary_results_incomplete: false\n    rollout_approval_revoked: false\n    deploy_has_a_long_description: false\n    deploy_blocked_by_security_policy: false\n    deploy_title_written_in_normal_case: false\n    service_free_of_major_incidents: true\n    commit_messages_written_in_a_casual_tone: true\n    deploy_prohibited_during_the_audit_window: false",
  "question": "Proposed action: turn down\nDo the record's facts rule out the proposed action entirely?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if backout_plan_missing is true or files_changed is above files_changed_soft_limit.\n2. turn down if deploy_blocked_by_security_policy is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true.\n3. send to a person if service_free_of_major_incidents is false or contract_customer_asked_for_a_say_in_this_rollout is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- turn down: kill this one off\n- go ahead: keep moving on this one nothing is holding it up\n- put on hold: suspend progress until verification is received\n- send to a person: pass it on so the asker gets a final answer from the owner\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q58fa35a018",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-5508\nvendor = Northwind Works\nvendor_name_written_in_capital_letters = false\nvendor_on_sanctions_list = false\nvendor_tax_form_missing = true\namount = 1401.16\npayment_requested_during_business_hours = true\namount_approval_threshold = 10000.00\nduplicate_of_paid_invoice = false\nawaiting_purchase_order = false\nvendor_filed_a_legal_claim_over_this_invoice = false\ninvoice_pdf_uses_a_portrait_layout = true\napprover_declared_a_conflict_of_interest = false",
  "question": "Proposed action: BQHL\nIs it not true that the proposed action sits in the record and is not a mismatch?",
  "definitions": "Meanings:\n- RW: shut off this process completely\n- T: proceed and the requester gets what they asked\n- SXN: submit it upward to the approver\n- BQHL: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9cfeb3cbfc",
  "kind": "choice",
  "text": "run_id | RUN-4208\nagent | fjord\ntool_output_shows_tampering | false\nlast_tool_output_unverified | false\nsteps_used_hard_limit | 16\nsteps_used | 19\naction_free_of_ethics_concerns | true\nowner_sign_off_required_for_this_action | false\ntask_description_incomplete | true\nlog_lines_written_in_a_verbose_style | false\naction_permitted_by_security_policy | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. stop if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is at least steps_used_hard_limit.\n2. pause if task_description_incomplete is true or owner_sign_off_required_for_this_action is true.\n3. human review if action_free_of_ethics_concerns is false.\nOtherwise: continue.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "continue",
   "human review",
   "stop"
  ]
 },
 {
  "qid": "qdca06afa0c",
  "kind": "choice",
  "text": "invoice_id: INV-6355\nvendor: Cedar Systems\ninvoice_pdf_uses_a_portrait_layout: true\nduplicate_of_paid_invoice: false\npurchase_order_received: true\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_free_of_sanctions: false\nvendor_tax_form_missing: false\npayment_requested_during_business_hours: true\namount_approval_threshold: 10000.00\nvendor_name_written_in_capital_letters: false\napprover_declared_a_conflict_of_interest: false\namount: 9711.04",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if purchase_order_received is false or vendor_tax_form_missing is true.\n2. deny if vendor_free_of_sanctions is false.\n3. ask manager if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nAs the team lead, which of the actions listed should we go with for this request?",
  "options": [
   "approve",
   "defer",
   "deny"
  ]
 },
 {
  "qid": "q92d57f3698",
  "kind": "choice",
  "text": "# request record\nticket_id: TCK-5453\ncustomer: لينا عماد السقا\nnote: جميع بيانات الطلب مكتملة ومطابقة للسجل.\nfree_of_safety_incident_reports: true\nclaim_form_filled_in_with_the_usual_font: true\nproof_of_purchase_attached: true\ncustomer_message_is_short: false\ncustomer_message_written_in_a_casual_tone: true\nlegal_complaint_filed: false\nclaim_amount: 98.29\nclaim_amount_hard_limit: 200.00\nitem_return_not_yet_received: true\nharmless_greeting_present_in_the_message: true\nclaim_involves_a_media_inquiry: true\nitem_excluded_by_policy: false\nclaim_free_of_ombudsman_cases: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if free_of_safety_incident_reports is false.\n2. turn down if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. put on hold if item_return_not_yet_received is true.\nOtherwise: go ahead.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nWhich of the listed actions is the right call for this request?",
  "options": [
   "turn down",
   "go ahead",
   "send to a person"
  ]
 },
 {
  "qid": "qb2aaad5d91",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- ticket id: TCK-9701\n- customer: Marta Keller\n- legal complaint filed: no\n- item return not yet received: yes\n- claim involves a media inquiry: no\n- claim amount hard limit: 50.00\n- claim free of ombudsman cases: yes\n- harmless greeting present in the message: no\n- proof of purchase missing: no\n- item excluded by policy: yes\n- claim form filled in with the usual font: yes\n- customer message is short: yes\n- claim amount: 43.78\n- customer message written in a formal tone: no\n- free of safety incident reports: yes",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 530 if item_return_not_yet_received is true or free_of_safety_incident_reports is false.\n2. 5 if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. 2360 if proof_of_purchase_missing is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: 18.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nMeanings:\n- 530: scrap the plan and drop this request\n- 5: pause this until the requester supplies the missing document\n- 18: continue so the requester receives the result\n- 2360: route this matter to the individual empowered to decide\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "5",
   "18",
   "530"
  ]
 },
 {
  "qid": "q9b81c376ee",
  "kind": "yes/no",
  "text": "# record\nleave_id: LVE-7932\nemployee: كنان ياسر الوادي\nnote: فترة الإجازة لا تتعارض مع أي مهام مجدولة للقسم.\nleave_balance_available: true\nlawyer_letter_received_about_this_leave: false\nleave_request_written_in_a_formal_tone: false\nteam_coverage_not_arranged: false\nleave_days_soft_limit: 10\nrequests_team_free_of_harassment_complaints: false\nnotice_period_not_met: false\nleave_days: 2\nno_union_grievance_raised_over_this_leave: true\nrequest_falls_in_blackout_period: false\nmedical_certificate_contested: false",
  "question": "Proposed action: send to a person\nAs an auditor, is the proposed action not the right call for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qee984c886a",
  "kind": "choice",
  "text": "---\nrequest:\n  invoice_id: INV-2135\n  vendor: Ironleaf Partners\nfigures:\n  amount: 3075.56\n  amount_approval_threshold: 5000.00\nchecks:\n  vendor_filed_a_legal_claim_over_this_invoice: false\n  payment_requested_during_business_hours: true\n  duplicate_of_paid_invoice: true\n  invoice_pdf_uses_a_portrait_layout: false\n  vendor_on_sanctions_list: false\n  vendor_tax_form_missing: false\n  vendor_name_written_in_capital_letters: false\n  awaiting_purchase_order: false\n  approver_free_of_conflicts_of_interest: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. ask a human if vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. refuse if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or approver_free_of_conflicts_of_interest is false or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- ask a human: hand this to the person who decides\n- delay: hold the request so the requester waits for their check\n- approve: run with it carry on as you were\n- refuse: decline the request as the action is prohibited\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "ask a human",
   "approve",
   "refuse"
  ]
 },
 {
  "qid": "qc6070316c7",
  "kind": "choice",
  "text": "---\n# record\nmeta:\n    deploy_id: \"DEP-3345\"\n    service: \"checkout\"\nmetrics:\n    files_changed: 17\n    files_changed_soft_limit: 20\nsignals:\n    service_free_of_major_incidents: true\n    deploy_has_a_long_description: false\n    canary_results_incomplete: false\n    deploy_blocked_by_security_policy: false\n    deploy_prohibited_during_the_audit_window: true\n    deploy_title_written_in_normal_case: true\n    contract_customer_asked_for_a_say_in_this_rollout: false\n    commit_messages_written_in_a_casual_tone: true\n    backout_plan_missing: false\n    rollout_approval_revoked: false\n    commit_messages_written_in_a_detailed_style: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if backout_plan_missing is true or rollout_approval_revoked is true or files_changed is at least files_changed_soft_limit.\n2. ask_a_human if contract_customer_asked_for_a_say_in_this_rollout is true.\n3. cancel if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\nOtherwise: proceed.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed would be the right call for the matter in this file?",
  "options": [
   "proceed",
   "cancel",
   "wait"
  ]
 },
 {
  "qid": "qc0f4f3b5b5",
  "kind": "yes/no",
  "text": "{\n  \"request_id\":\"REQ-1430\",\n  \"requester\":\"Idris Adeyemi\",\n  \"requested_role_permitted_by_policy\":true,\n  \"business_justification_provided\":true,\n  \"legal_preservation_order_on_the_account\":false,\n  \"request_free_of_ethics_office_flags\":true,\n  \"access_days_approval_threshold\":7,\n  \"request_grants_admin_rights\":false,\n  \"requester_not_barred_from_this_system\":true,\n  \"access_days\":4,\n  \"mfa_enrollment_complete\":true,\n  \"request_text_written_in_capital_letters\":false,\n  \"account_suspended\":false\n}",
  "question": "Proposed action: allow\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_provided is false or requested_role_permitted_by_policy is false.\n2. page oncall if mfa_enrollment_complete is false or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. block access if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: allow.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- block access: shut this down fast\n- allow: proceed with the task as asked\n- quarantine: defer the step until the verification is in\n- page oncall: send it up so the requester gets a firm decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q001197c0ee",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n* run id: RUN-5229\n* agent: helix\n* tool output shows tampering: no\n* task description incomplete: no\n* log lines written in a compact style: yes\n* action forbidden by security policy: no\n* owner sign off required for this action: no\n* action free of ethics concerns: yes\n* steps used: 40\n* last tool output verified: yes\n* steps used hard limit: 40",
  "question": "Meanings:\n- DFL: hold off until the check clears\n- ZH: have the item pushed forward as the request stated\n- SHSK: drop it right away\n- C: delegate the call to whoever holds authority\nThe record is complete: nothing else applies.\n\nWhich of the actions below is the right decision for this request?",
  "options": [
   "DFL",
   "C",
   "ZH"
  ]
 },
 {
  "qid": "qa3f45640a2",
  "kind": "choice",
  "text": "{\n    \"subject\": {\n        \"invoice_id\": \"INV-1077\",\n        \"vendor\": \"Summit Group\"\n    },\n    \"amounts\": {\n        \"amount_approval_threshold\": 2500.00,\n        \"amount\": 2003.42\n    },\n    \"checks\": {\n        \"invoice_pdf_uses_a_landscape_layout\": true,\n        \"vendor_free_of_sanctions\": false,\n        \"vendor_tax_form_on_file\": true,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": true,\n        \"duplicate_of_paid_invoice\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"awaiting_purchase_order\": false,\n        \"approver_declared_a_conflict_of_interest\": false,\n        \"vendor_name_written_in_capital_letters\": true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if awaiting_purchase_order is true or vendor_tax_form_on_file is false.\n2. cancel if vendor_free_of_sanctions is false.\n3. ask a human if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: proceed.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nLooking at this case file, which of the actions listed is the right call?",
  "options": [
   "proceed",
   "cancel",
   "ask a human"
  ]
 },
 {
  "qid": "q99837ab954",
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
  "qid": "q055c1cdd4f",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-1633\",\"vendor\":\"Stonebridge Foods\",\"vendor_tax_form_on_file\":true,\"duplicate_of_paid_invoice\":false,\"vendor_name_written_in_capital_letters\":false,\"awaiting_purchase_order\":true,\"amount_approval_threshold\":5000.00,\"vendor_filed_a_legal_claim_over_this_invoice\":false,\"payment_requested_during_business_hours\":false,\"invoice_pdf_uses_a_landscape_layout\":false,\"amount\":2585.37,\"approver_free_of_conflicts_of_interest\":true,\"vendor_on_sanctions_list\":true}",
  "question": "Proposed action: turn down\nDo the facts here rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if vendor_on_sanctions_list is true or approver_free_of_conflicts_of_interest is false.\n2. send to a person if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. put on hold if awaiting_purchase_order is true or amount is at least amount_approval_threshold.\nOtherwise: go ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- turn down: stop the work since it cannot move forward\n- go ahead: just crack on with it there is nothing in the way\n- send to a person: route the case to a decider so the requester knows the outcome\n- put on hold: wait for the check and the requester will hear back later\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9bff56b487",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-6162\n  vendor: Oakmont Systems\nvalues:\n  amount: 66.96\n  amount_approval_threshold: 500.00\ntests:\n  invoice_pdf_uses_a_landscape_layout: false\n  vendor_filed_a_legal_claim_over_this_invoice: false\n  vendor_free_of_sanctions: false\n  payment_requested_during_business_hours: true\n  vendor_name_written_in_capital_letters: false\n  duplicate_of_paid_invoice: false\n  purchase_order_received: true\n  approver_free_of_conflicts_of_interest: true\n  vendor_tax_form_on_file: true",
  "question": "Proposed action: cancel\nIs it not so that the proposed action we have on the table is not a poor choice for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q6cd293dc23",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- leave id: LVE-4220\n- employee: Dana Castell\n- team coverage not arranged: no\n- leave days: 14\n- leave balance available: yes\n- request falls in blackout period: no\n- union grievance raised over this leave: no\n- lawyer letter received about this leave: no\n- leave days soft limit: 14\n- leave request written in a formal tone: no\n- medical certificate contested: no\n- requests team free of harassment complaints: no\n- notice period not met: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if notice_period_not_met is true or team_coverage_not_arranged is true or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. turn_down if medical_certificate_contested is true.\n3. send_to_a_person if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: go_ahead.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nGiven what the requester needs, which of the actions below should be taken?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "turn_down"
  ]
 },
 {
  "qid": "q8ae9f41c5c",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n* leave id: LVE-5561\n* employee: Marta Imai\n* no union grievance raised over this leave: no\n* leave days: 1\n* team coverage not arranged: no\n* requests team free of harassment complaints: yes\n* leave request written in a formal tone: no\n* notice period not met: yes\n* leave balance exhausted: no\n* leave days soft limit: 10\n* lawyer letter received about this leave: no\n* medical certificate contested: no\n* request falls in blackout period: no",
  "question": "Proposed action: 1\nWould the proposed action be considered the correct disposition of the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 5654 if notice_period_not_met is true or team_coverage_not_arranged is true or leave_days is above leave_days_soft_limit.\n2. 1 if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. 44 if leave_balance_exhausted is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: 580.\nNever counted: leave_request_written_in_a_formal_tone.\nMeanings:\n- 5654: keep it on hold for the missing document\n- 1: stop this course of action at once\n- 580: have the plan kept moving as it was requested\n- 44: pass this along to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q41640f8dc7",
  "kind": "yes/no",
  "text": "{\"leave_id\":\"LVE-4030\",\"employee\":\"ريم سامي الزهراني\",\"note\":\"عدد الأيام المطلوبة للإجازة ما يزال موضع استفسار.\",\"team_coverage_arranged\":true,\"notice_period_met\":true,\"requests_team_free_of_harassment_complaints\":true,\"leave_days\":6,\"no_union_grievance_raised_over_this_leave\":true,\"leave_days_soft_limit\":10,\"leave_balance_available\":true,\"leave_request_written_in_a_formal_tone\":false,\"medical_certificate_contested\":false,\"request_falls_in_blackout_period\":false,\"lawyer_letter_received_about_this_leave\":false}",
  "question": "Proposed action: 31\nReviewing this as an auditor, do the record's facts rule out the proposed action for the request?",
  "definitions": "Meanings:\n- 7819: have the task carried out as it was originally asked\n- 31: pump the brakes until more details show up\n- 434: bring in the authority who can settle it for the requester\n- 4: end it so the requester sees their request closed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q032a3c5430",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-4248\",\n  \"vendor\":\"Oakmont Partners\",\n  \"awaiting_purchase_order\":false,\n  \"invoice_pdf_uses_a_portrait_layout\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"approver_free_of_conflicts_of_interest\":true,\n  \"vendor_name_written_in_capital_letters\":false,\n  \"vendor_tax_form_missing\":false,\n  \"amount\":142.15,\n  \"vendor_free_of_sanctions\":true,\n  \"vendor_filed_a_legal_claim_over_this_invoice\":true,\n  \"amount_approval_threshold\":500.00,\n  \"duplicate_of_paid_invoice\":false\n}",
  "question": "Proposed action: ask_manager\nJudging from what the record shows, is the proposed action not the correct decision?",
  "definitions": "Meanings:\n- ask_manager: escalate the matter to the accountable decision maker\n- deny: refuse the request because it crosses a clear line\n- approve: keep going exactly as requested because every obstacle has cleared\n- defer: hold off until the check has been completed by the team\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc58e7a7c82",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- run id: RUN-4290\n- agent: atlas\n- owner sign off required for this action: no\n- action free of ethics concerns: no\n- log lines written in a compact style: no\n- steps used hard limit: 12\n- task description complete: no\n- action forbidden by security policy: yes\n- last tool output verified: no\n- tool output shows tampering: no\n- steps used: 1",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. GV if action_free_of_ethics_concerns is false or owner_sign_off_required_for_this_action is true.\n2. N if action_forbidden_by_security_policy is true.\n3. SBC if tool_output_shows_tampering is true or steps_used is above steps_used_hard_limit.\nOtherwise: PLTL.\nNever counted: last_tool_output_verified, task_description_complete, log_lines_written_in_a_compact_style.\nMeanings:\n- GV: bring in the owner who can rule on this\n- PLTL: proceed in accordance with the stated request\n- SBC: be dropped here and not acted upon at all\n- N: hold this until a check comes back\nThe record is complete: nothing else applies.\n\nWhich of these actions should we take for this request?",
  "options": [
   "GV",
   "SBC",
   "N"
  ]
 },
 {
  "qid": "q1af2743c40",
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
  "qid": "q9b041848cd",
  "kind": "choice",
  "text": "{\n  \"subject\": {\n    \"ticket_id\": \"TCK-1546\",\n    \"customer\": \"Jonas Mensah\"\n  },\n  \"amounts\": {\n    \"claim_amount_hard_limit\": 200.00,\n    \"claim_amount\": 159.10\n  },\n  \"checks\": {\n    \"customer_message_written_in_a_casual_tone\": true,\n    \"item_return_not_yet_received\": false,\n    \"claim_free_of_ombudsman_cases\": true,\n    \"item_excluded_by_policy\": false,\n    \"claim_form_filled_in_with_the_usual_font\": true,\n    \"proof_of_purchase_attached\": true,\n    \"free_of_legal_complaints\": true,\n    \"customer_message_is_short\": false,\n    \"claim_involves_a_media_inquiry\": false,\n    \"harmless_greeting_present_in_the_message\": true,\n    \"free_of_safety_incident_reports\": true\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. KSWZ if item_return_not_yet_received is true or free_of_safety_incident_reports is false.\n2. SBX if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. VD if proof_of_purchase_attached is false or free_of_legal_complaints is false or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: G.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- G: carry out the task as instructed without any obstacle\n- VD: send it up to the person who makes the call\n- KSWZ: drop it right away\n- SBX: hold off until the check clears\nThe record is complete: nothing else applies.\n\nTaking the actions listed into account, what is the right call for the request?",
  "options": [
   "VD",
   "KSWZ",
   "G"
  ]
 },
 {
  "qid": "qf9a1b85350",
  "kind": "choice",
  "text": "{\n  \"subject\":{\n    \"deploy_id\":\"DEP-5350\",\n    \"service\":\"search\"\n  },\n  \"amounts\":{\n    \"files_changed_soft_limit\":15,\n    \"files_changed\":3\n  },\n  \"checks\":{\n    \"service_free_of_major_incidents\":false,\n    \"backout_plan_missing\":false,\n    \"deploy_title_written_in_normal_case\":true,\n    \"commit_messages_written_in_a_casual_tone\":false,\n    \"deploy_blocked_by_security_policy\":false,\n    \"deploy_has_a_long_description\":false,\n    \"rollout_approval_revoked\":false,\n    \"canary_results_complete\":true,\n    \"commit_messages_written_in_a_terse_style\":true,\n    \"deploy_prohibited_during_the_audit_window\":false,\n    \"contract_customer_asked_for_a_say_in_this_rollout\":false\n  }\n}",
  "question": "Meanings:\n- go ahead: push ahead as planned\n- send to a person: refer the matter to the decision holder\n- turn down: send the requester away with the request left unfinished\n- put on hold: keep their request on hold until more information arrives from them\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "go ahead",
   "send to a person",
   "put on hold"
  ]
 },
 {
  "qid": "q4bccdb32a5",
  "kind": "yes/no",
  "text": "leave_id: LVE-3042\nemployee: ريما فايز الزبيدي\nnote: طلب الإجازة مقدم في الموعد المحدد بالسياسة.\nleave_days_soft_limit: 10\nleave_request_written_in_a_formal_tone: false\nleave_balance_available: false\nmedical_certificate_contested: false\nno_union_grievance_raised_over_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nleave_days: 4\nteam_coverage_arranged: true\nrequest_falls_in_blackout_period: true\nnotice_period_met: false\nlawyer_letter_received_about_this_leave: false",
  "question": "Proposed action: delay\nDo the request and its facts together make the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. delay if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. refuse if leave_balance_available is false.\nOtherwise: approve.\nNever counted: notice_period_met, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7822097394",
  "kind": "yes/no",
  "text": "# record\nleave_id: LVE-7932\nemployee: كنان ياسر الوادي\nnote: فترة الإجازة لا تتعارض مع أي مهام مجدولة للقسم.\nleave_balance_available: true\nlawyer_letter_received_about_this_leave: false\nleave_request_written_in_a_formal_tone: false\nteam_coverage_not_arranged: false\nleave_days_soft_limit: 10\nrequests_team_free_of_harassment_complaints: false\nnotice_period_not_met: false\nleave_days: 2\nno_union_grievance_raised_over_this_leave: true\nrequest_falls_in_blackout_period: false\nmedical_certificate_contested: false",
  "question": "Proposed action: send to a person\nIs the proposed action the right call for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q2752e01c2e",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  invoice_id: INV-4478\n  vendor: Cedar Traders\nnumbers:\n  amount_approval_threshold: 25000.00\n  amount: 22278.00\nflags:\n  payment_requested_during_business_hours: false\n  approver_free_of_conflicts_of_interest: true\n  purchase_order_received: true\n  invoice_pdf_uses_a_landscape_layout: false\n  vendor_name_written_in_capital_letters: false\n  duplicate_of_paid_invoice: false\n  vendor_tax_form_on_file: true\n  vendor_on_sanctions_list: true\n  vendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "Proposed action: escalate\nSo, is the proposed action a good call for what was asked here?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q6fd15368d8",
  "kind": "choice",
  "text": "{\n    \"subject\": {\n        \"leave_id\": \"LVE-4916\",\n        \"employee\": \"Zoe Brandt\"\n    },\n    \"amounts\": {\n        \"leave_days_soft_limit\": 10,\n        \"leave_days\": 1\n    },\n    \"checks\": {\n        \"request_falls_in_blackout_period\": true,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"no_union_grievance_raised_over_this_leave\": true,\n        \"team_coverage_arranged\": true,\n        \"medical_certificate_contested\": false,\n        \"leave_request_written_in_a_formal_tone\": true,\n        \"leave_balance_exhausted\": false,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"notice_period_not_met\": false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if notice_period_not_met is true or team_coverage_arranged is false or leave_days is above leave_days_soft_limit.\n2. refuse if request_falls_in_blackout_period is true.\n3. ask_a_human if leave_balance_exhausted is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or no_union_grievance_raised_over_this_leave is false.\nOtherwise: approve.\nNever counted: lawyer_letter_received_about_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "ask_a_human",
   "approve",
   "refuse"
  ]
 },
 {
  "qid": "q1d8f819f39",
  "kind": "yes/no",
  "text": "{\n  \"request_id\":\"REQ-1430\",\n  \"requester\":\"Idris Adeyemi\",\n  \"requested_role_permitted_by_policy\":true,\n  \"business_justification_provided\":true,\n  \"legal_preservation_order_on_the_account\":false,\n  \"request_free_of_ethics_office_flags\":true,\n  \"access_days_approval_threshold\":7,\n  \"request_grants_admin_rights\":false,\n  \"requester_not_barred_from_this_system\":false,\n  \"access_days\":4,\n  \"mfa_enrollment_complete\":true,\n  \"request_text_written_in_capital_letters\":false,\n  \"account_suspended\":false\n}",
  "question": "Proposed action: allow\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_provided is false or requested_role_permitted_by_policy is false.\n2. page oncall if mfa_enrollment_complete is false or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. block access if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: allow.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- block access: shut this down fast\n- allow: proceed with the task as asked\n- quarantine: defer the step until the verification is in\n- page oncall: send it up so the requester gets a firm decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q890f11c4e4",
  "kind": "yes/no",
  "text": "invoice_id: INV-6949\nvendor: Fairview Labs\nduplicate_of_paid_invoice: true\npayment_requested_during_business_hours: true\namount_approval_threshold: 5000.00\nvendor_name_written_in_capital_letters: false\nvendor_on_sanctions_list: false\ninvoice_pdf_uses_a_portrait_layout: true\namount: 4458.79\nawaiting_purchase_order: false\nvendor_filed_a_legal_claim_over_this_invoice: false\napprover_declared_a_conflict_of_interest: false\nvendor_tax_form_missing: false",
  "question": "Proposed action: turn down\nBased on the record, can it be said the proposed action is not the right call?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q422a498f3a",
  "kind": "yes/no",
  "text": "---\n# record\nmeta:\n    invoice_id: \"INV-2735\"\n    vendor: \"Riverbend Works\"\nmetrics:\n    amount_approval_threshold: 5000.00\n    amount: 1450.97\nsignals:\n    vendor_filed_a_legal_claim_over_this_invoice: false\n    vendor_on_sanctions_list: false\n    purchase_order_received: true\n    invoice_pdf_uses_a_portrait_layout: true\n    duplicate_of_paid_invoice: true\n    vendor_tax_form_missing: false\n    payment_requested_during_business_hours: true\n    approver_declared_a_conflict_of_interest: false\n    vendor_name_written_in_capital_letters: false",
  "question": "Proposed action: turn_down\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Meanings:\n- go_ahead: keep going with it\n- turn_down: shut this down right away, we are staying clear of it\n- put_on_hold: hold this until a check comes back\n- send_to_a_person: transfer it to the person with authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q01ea0a8e6c",
  "kind": "yes/no",
  "text": "{\n    \"request\": {\n        \"deploy_id\": \"DEP-5299\",\n        \"service\": \"inventory\"\n    },\n    \"figures\": {\n        \"files_changed\": 75,\n        \"files_changed_soft_limit\": 80\n    },\n    \"checks\": {\n        \"rollout_approval_revoked\": false,\n        \"commit_messages_written_in_a_casual_tone\": true,\n        \"canary_results_incomplete\": false,\n        \"deploy_has_a_long_description\": false,\n        \"deploy_blocked_by_security_policy\": false,\n        \"backout_plan_missing\": false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\": false,\n        \"deploy_prohibited_during_the_audit_window\": false,\n        \"commit_messages_written_in_a_terse_style\": false,\n        \"deploy_title_written_in_normal_case\": true,\n        \"service_free_of_major_incidents\": true\n    }\n}",
  "question": "Proposed action: stop\nShould the proposed action be taken for this request?",
  "definitions": "Meanings:\n- stop: block it right away\n- human_review: hand this off because a decider has to choose\n- pause: hold up for a sec until more info comes in\n- continue: keep it moving forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q8a898c354c",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n* deploy id: DEP-6172\n* service: pricing\n* commit messages written in a casual tone: yes\n* deploy prohibited during the audit window: no\n* deploy blocked by security policy: no\n* canary results incomplete: no\n* commit messages written in a terse style: no\n* files changed: 80\n* files changed soft limit: 80\n* contract customer asked for a say in this rollout: yes\n* deploy has a long description: no\n* backout plan missing: no\n* service free of major incidents: yes\n* deploy title written in normal case: yes\n* rollout approval revoked: no",
  "question": "Proposed action: KBK\nIs the proposed action the suitable determination for the request in the record?",
  "definitions": "Meanings:\n- RR: be turned away and treated as off limits\n- KBK: transfer the case to the responsible decision maker for determination\n- B: wait until a document arrives before you move forward with it\n- TFQL: run the requested step through\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q29af2b99ae",
  "kind": "choice",
  "text": "# case\nticket_id = TCK-5028\ncustomer = Marta Mensah\ncustomer_message_is_short = true\nitem_excluded_by_policy = false\nclaim_amount_hard_limit = 100.00\nfree_of_safety_incident_reports = true\nclaim_involves_a_media_inquiry = false\nharmless_greeting_present_in_the_message = true\nclaim_free_of_ombudsman_cases = true\nclaim_amount = 123.21\nfree_of_legal_complaints = false\nitem_return_not_yet_received = false\nproof_of_purchase_missing = false\ncustomer_message_written_in_a_formal_tone = false\nclaim_form_filled_in_with_the_usual_font = true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if item_return_not_yet_received is true or claim_free_of_ombudsman_cases is false.\n2. defer if proof_of_purchase_missing is true or claim_amount is at least claim_amount_hard_limit.\n3. deny if item_excluded_by_policy is true or free_of_legal_complaints is false or claim_involves_a_media_inquiry is true.\nOtherwise: approve.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "deny",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q88ffe027a6",
  "kind": "choice",
  "text": "{\"request_id\": \"REQ-9979\", \"requester\": \"Idris Moreau\", \"mfa_enrollment_incomplete\": false, \"request_free_of_ethics_office_flags\": true, \"access_days\": 10, \"account_suspended\": false, \"requested_role_forbidden_by_policy\": false, \"business_justification_missing\": true, \"access_days_approval_threshold\": 14, \"requester_barred_from_this_system\": false, \"request_grants_admin_rights\": false, \"legal_preservation_order_on_the_account\": false, \"request_text_written_in_capital_letters\": false}",
  "question": "Meanings:\n- delay: wait until a document arrives before you move forward with it\n- ask a human: get sent upward to the one who decides\n- refuse: reject this item since it violates the policy\n- approve: run the requested step through\nThe record is complete: nothing else applies.\n\nWhich of the actions listed fits the case described in this file best?",
  "options": [
   "ask a human",
   "refuse",
   "delay"
  ]
 },
 {
  "qid": "q82ed544b51",
  "kind": "choice",
  "text": "{\n  \"meta\":{\n    \"run_id\":\"RUN-1222\",\n    \"agent\":\"fjord\"\n  },\n  \"metrics\":{\n    \"steps_used\":4,\n    \"steps_used_hard_limit\":30\n  },\n  \"signals\":{\n    \"action_permitted_by_security_policy\":false,\n    \"task_description_complete\":true,\n    \"owner_sign_off_required_for_this_action\":false,\n    \"tool_output_shows_tampering\":false,\n    \"last_tool_output_unverified\":false,\n    \"log_lines_written_in_a_compact_style\":true,\n    \"action_free_of_ethics_concerns\":true\n  }\n}",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "cancel",
   "ask_a_human",
   "proceed"
  ]
 },
 {
  "qid": "q8e6dc30ed9",
  "kind": "choice",
  "text": "# record\ninvoice_id: INV-1640\nvendor: Stonebridge Traders\nvendor_on_sanctions_list: false\ninvoice_pdf_uses_a_landscape_layout: false\nvendor_name_written_in_capital_letters: true\napprover_free_of_conflicts_of_interest: true\namount: 176.34\npurchase_order_received: true\nvendor_tax_form_on_file: true\nvendor_filed_a_legal_claim_over_this_invoice: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\namount_approval_threshold: 500.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. reject if vendor_on_sanctions_list is true or approver_free_of_conflicts_of_interest is false.\n2. escalate if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. hold if purchase_order_received is false or amount is at least amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the listed actions do the facts support as the right call?",
  "options": [
   "hold",
   "pay",
   "reject"
  ]
 },
 {
  "qid": "q7a715f0ce3",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- leave id: LVE-2257\n- employee: Kofi Moreau\n- requests team free of harassment complaints: yes\n- lawyer letter received about this leave: no\n- union grievance raised over this leave: no\n- leave balance available: yes\n- leave days: 3\n- notice period met: yes\n- request falls in blackout period: no\n- leave request written in a formal tone: yes\n- team coverage not arranged: no\n- medical certificate contested: no\n- leave days soft limit: 5",
  "question": "Proposed action: delay\nAuditing this request closely, is the proposed action not a defensible choice?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q4089456463",
  "kind": "yes/no",
  "text": "ticket_id: TCK-7294\ncustomer: Mira Calloway\ncustomer_message_written_in_a_formal_tone: true\nclaim_free_of_ombudsman_cases: true\nfree_of_safety_incident_reports: true\nclaim_involves_a_media_inquiry: false\nclaim_amount_hard_limit: 50.00\nclaim_form_filled_in_with_the_usual_font: true\nproof_of_purchase_missing: true\nlegal_complaint_filed: false\ncustomer_message_is_short: true\nitem_excluded_by_policy: false\nclaim_amount: 26.50\nharmless_greeting_present_in_the_message: true\nitem_return_not_yet_received: false",
  "question": "Proposed action: wait\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Meanings:\n- ask a human: forward it to the decision maker\n- wait: shelve the matter until more details come in\n- cancel: end this effort right away\n- proceed: keep it moving forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q91a7a43036",
  "kind": "choice",
  "text": "# record\nleave_id | LVE-9120\nemployee | Ravi Okonkwo\nunion_grievance_raised_over_this_leave | false\nleave_days_soft_limit | 3\nlawyer_letter_received_about_this_leave | false\nrequest_falls_in_blackout_period | false\nleave_days | 1\nteam_coverage_arranged | true\nrequests_team_free_of_harassment_complaints | true\nleave_balance_available | true\nmedical_certificate_contested | false\nnotice_period_not_met | false\nleave_request_written_in_a_formal_tone | false",
  "question": "Meanings:\n- L: decline the request as the action is prohibited\n- LVVP: carry out the task as instructed without any obstacle\n- VMH: refer this item to the person who holds decision authority\n- SP: pause the request and gather more information before going on\nThe record is complete: nothing else applies.\n\nLooking across the actions listed, what would be the correct response to this request?",
  "options": [
   "LVVP",
   "L",
   "SP"
  ]
 },
 {
  "qid": "qa14db93a0c",
  "kind": "yes/no",
  "text": "leave_id: LVE-3935\nemployee: Anders Whitcombe\nteam_coverage_arranged: true\nleave_request_written_in_a_formal_tone: false\nleave_days_soft_limit: 3\nrequests_team_free_of_harassment_complaints: true\nunion_grievance_raised_over_this_leave: false\nnotice_period_met: true\nmedical_certificate_contested: false\nleave_balance_exhausted: true\nleave_days: 3\nlawyer_letter_received_about_this_leave: false\nrequest_falls_in_blackout_period: false",
  "question": "Proposed action: deny\nAs a reviewer checking the file, is the proposed action not a sound decision here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. defer if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. deny if leave_balance_exhausted is true.\nOtherwise: approve.\nNever counted: notice_period_met, union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 }
]
