# G5-H blind read T46-blind_read-da51d47e-005 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8a/T46/qc/g5h/answers/T46-blind_read-da51d47e-005.json

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
  "qid": "qe39ac0f97f",
  "kind": "yes/no",
  "text": "---\n# case\ndeploy_id: \"DEP-3754\"\nservice: \"inventory\"\ndeploy_prohibited_during_the_audit_window: false\nbackout_plan_missing: false\nrollout_approval_revoked: false\ndeploy_title_written_in_normal_case: true\nfiles_changed_soft_limit: 80\nfiles_changed: 9\nservice_free_of_major_incidents: false\ncommit_messages_written_in_a_casual_tone: true\ncanary_results_complete: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_blocked_by_security_policy: false\ncommit_messages_written_in_a_detailed_style: true\ndeploy_has_a_long_description: false",
  "question": "Proposed action: proceed\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Meanings:\n- wait: stay put until the check is finished\n- proceed: continue with the request as nothing obstructs it\n- cancel: reject the petition as the action is unauthorized\n- ask_a_human: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3da45cbcb3",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n* invoice id: INV-7215\n* vendor: Summit Logistics\n* vendor filed a legal claim over this invoice: no\n* awaiting purchase order: yes\n* payment requested during business hours: yes\n* duplicate of paid invoice: no\n* vendor tax form missing: no\n* invoice pdf uses a portrait layout: yes\n* vendor name written in capital letters: no\n* vendor free of sanctions: yes\n* approver declared a conflict of interest: no\n* amount approval threshold: 25000.00\n* amount: 3343.87",
  "question": "Proposed action: wait\nDoes the proposed action match what the record supports for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qe44d56b514",
  "kind": "yes/no",
  "text": "{\"request_id\":\"REQ-4861\",\"requester\":\"Anders Okafor\",\"requested_role_forbidden_by_policy\":true,\"access_days\":30,\"ethics_office_flagged_the_request\":false,\"legal_preservation_order_on_the_account\":false,\"request_text_written_in_capital_letters\":false,\"request_grants_admin_rights\":false,\"business_justification_provided\":true,\"requester_barred_from_this_system\":false,\"access_days_approval_threshold\":30,\"mfa_enrollment_complete\":true,\"account_suspended\":false}",
  "question": "Proposed action: refer_to_owner\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer_to_owner if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. pend if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_complete is false or account_suspended is true.\nOtherwise: grant.\nNever counted: business_justification_provided, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf2cd3babaa",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-8940\n- requester: Omar Moreau\n- requester barred from this system: no\n- mfa enrollment incomplete: yes\n- requested role forbidden by policy: no\n- access days: 36\n- request grants admin rights: no\n- request text written in capital letters: no\n- legal preservation order on the account: no\n- account suspended: no\n- business justification missing: no\n- access days approval threshold: 45\n- ethics office flagged the request: no",
  "question": "Meanings:\n- grant: allow the matter to be taken forward as planned\n- pend: wait until a document arrives before you move forward with it\n- refer to owner: hand the matter to a decider so the requester gets a verdict\n- refuse: shut off this process completely\nThe record is complete: nothing else applies.\n\nLooking at this case file, which of the actions listed is the right call?",
  "options": [
   "pend",
   "refuse",
   "grant"
  ]
 },
 {
  "qid": "q567663daac",
  "kind": "yes/no",
  "text": "# case\nrun_id: RUN-3482\nagent: jasper\naction_free_of_ethics_concerns: true\nowner_sign_off_required_for_this_action: false\naction_forbidden_by_security_policy: false\nsteps_used_hard_limit: 8\nlast_tool_output_unverified: false\nlog_lines_written_in_a_compact_style: true\ntool_output_shows_tampering: false\nsteps_used: 5\ntask_description_complete: true",
  "question": "Proposed action: cancel\nQuick question: is the proposed action the right thing to do with this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is at least steps_used_hard_limit.\n2. wait if task_description_complete is false or owner_sign_off_required_for_this_action is true.\n3. ask a human if action_free_of_ethics_concerns is false.\nOtherwise: proceed.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_compact_style.\nMeanings:\n- proceed: advance the task as stated without any blockers\n- wait: wait for the document to come through\n- ask a human: route this matter to the individual empowered to decide\n- cancel: refuse the request because it crosses a clear line\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qebea395435",
  "kind": "choice",
  "text": "{\"invoice_id\": \"INV-2944\", \"vendor\": \"Riverbend Partners\", \"amount\": 1293.08, \"duplicate_of_paid_invoice\": false, \"amount_approval_threshold\": 5000.00, \"vendor_name_written_in_capital_letters\": false, \"awaiting_purchase_order\": true, \"approver_declared_a_conflict_of_interest\": false, \"payment_requested_during_business_hours\": false, \"vendor_tax_form_on_file\": true, \"invoice_pdf_uses_a_portrait_layout\": true, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"vendor_free_of_sanctions\": true}",
  "question": "Meanings:\n- 151: skip this one, it is a hard pass for us\n- 99: bring in the owner who can rule on this\n- 1596: have the task carried out as it was originally asked\n- 6: wait for the document before going further\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "151",
   "1596",
   "6"
  ]
 },
 {
  "qid": "q9d4e370497",
  "kind": "yes/no",
  "text": "leave_id=LVE-5594\nemployee=هيفاء نزار الساعدي\nnote=تواريخ الإجازة لا تتعارض مع جدول العمل.\nteam_coverage_arranged=true\nnotice_period_met=true\nleave_balance_available=false\nlawyer_letter_received_about_this_leave=false\nleave_request_written_in_a_formal_tone=false\nleave_days_soft_limit=21\nleave_days=18\nrequest_falls_in_blackout_period=false\nrequests_team_free_of_harassment_complaints=true\nmedical_certificate_contested=false\nno_union_grievance_raised_over_this_leave=false",
  "question": "Proposed action: W\nShould the proposed action be taken for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QRW if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. JF if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. W if leave_balance_available is false.\nOtherwise: HKWC.\nNever counted: notice_period_met, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nMeanings:\n- W: kill this one off, it is off the table for good\n- JF: defer the step until the verification is in\n- QRW: be handed over to the deciding person\n- HKWC: advance the task as stated without any blockers\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9368635583",
  "kind": "choice",
  "text": "---\n# record\nrequest_id: \"REQ-7091\"\nrequester: \"Tomas Hadjiev\"\nethics_office_flagged_the_request: false\nrequested_role_permitted_by_policy: true\naccess_days: 5\nmfa_enrollment_complete: true\naccount_suspended: false\nrequest_text_written_in_capital_letters: true\nrequest_grants_admin_rights: false\naccess_days_approval_threshold: 90\nlegal_preservation_order_on_the_account: false\nbusiness_justification_missing: false\nrequester_barred_from_this_system: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. page oncall if request_grants_admin_rights is true or ethics_office_flagged_the_request is true or access_days is at least access_days_approval_threshold.\n2. quarantine if mfa_enrollment_complete is false.\n3. block access if business_justification_missing is true or account_suspended is true or requested_role_permitted_by_policy is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed would you sign off on for this request, as the manager?",
  "options": [
   "block access",
   "quarantine",
   "allow"
  ]
 },
 {
  "qid": "qae5a54cd1e",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-7700\n- requester: Kofi Lindqvist\n- requester barred from this system: yes\n- legal preservation order on the account: no\n- access days approval threshold: 14\n- account suspended: no\n- mfa enrollment complete: yes\n- request grants admin rights: no\n- access days: 8\n- request text written in capital letters: yes\n- request free of ethics office flags: yes\n- business justification provided: yes\n- requested role forbidden by policy: no",
  "question": "Proposed action: page oncall\nIs the proposed action not what should happen with this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. block access if account_suspended is true or requested_role_forbidden_by_policy is true or request_grants_admin_rights is true.\n2. page oncall if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. quarantine if business_justification_provided is false or mfa_enrollment_complete is false or requester_barred_from_this_system is true or request_free_of_ethics_office_flags is false.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q208dc840eb",
  "kind": "yes/no",
  "text": "leave_id=LVE-1599\nemployee=Zoe Vasquez\nleave_balance_exhausted=false\nrequest_falls_in_blackout_period=false\nleave_days_soft_limit=10\nnotice_period_met=true\nleave_days=10\nteam_coverage_not_arranged=false\nrequests_team_free_of_harassment_complaints=true\nlawyer_letter_received_about_this_leave=false\nleave_request_written_in_a_formal_tone=false\nmedical_certificate_contested=false\nunion_grievance_raised_over_this_leave=false",
  "question": "Proposed action: go ahead\nDo the record facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if notice_period_met is false or request_falls_in_blackout_period is true.\n2. put on hold if team_coverage_not_arranged is true or leave_balance_exhausted is true or leave_days is above leave_days_soft_limit.\n3. send to a person if medical_certificate_contested is true or union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: go ahead.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- put on hold: keep it in limbo until the verification has been confirmed\n- go ahead: keep it moving forward\n- turn down: shut this down right away, we are staying clear of it\n- send to a person: escalate the matter to the accountable decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe27bdea78f",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  leave_id: LVE-7443\n  employee: Aiko Mensah\nnumbers:\n  leave_days_soft_limit: 21\n  leave_days: 10\nflags:\n  leave_balance_exhausted: false\n  leave_request_written_in_a_formal_tone: true\n  request_falls_in_blackout_period: false\n  medical_certificate_contested: false\n  lawyer_letter_received_about_this_leave: false\n  team_coverage_arranged: true\n  requests_team_free_of_harassment_complaints: false\n  notice_period_met: true\n  union_grievance_raised_over_this_leave: false",
  "question": "Proposed action: proceed\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if notice_period_met is false or team_coverage_arranged is false or leave_balance_exhausted is true or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. cancel if medical_certificate_contested is true.\n3. ask_a_human if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: proceed.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- ask_a_human: route the case to a decider so the requester knows the outcome\n- cancel: be stopped and never carried out\n- proceed: go on and finish it the path is clear\n- wait: be kept on hold until more information is supplied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7a6a33d222",
  "kind": "choice",
  "text": "# record\nleave_id=LVE-4637\nemployee=Tomas Lindqvist\nleave_request_written_in_a_formal_tone=false\nmedical_certificate_contested=false\nunion_grievance_raised_over_this_leave=false\nrequest_falls_in_blackout_period=false\nleave_balance_available=true\nteam_coverage_not_arranged=false\nrequests_team_free_of_harassment_complaints=true\nlawyer_letter_received_about_this_leave=false\nleave_days=10\nnotice_period_not_met=false\nleave_days_soft_limit=10",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. wait if notice_period_not_met is true or team_coverage_not_arranged is true.\n3. cancel if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\nOtherwise: proceed.\nNever counted: leave_balance_available, medical_certificate_contested, union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nMeanings:\n- proceed: execute the request exactly as written\n- cancel: refuse the request because it crosses a clear line\n- wait: park this until a record turns up\n- ask_a_human: route it elsewhere because a decider must weigh in\nThe record is complete: nothing else applies.\n\nWhich listed action is the best call for the request?",
  "options": [
   "cancel",
   "ask_a_human",
   "proceed"
  ]
 },
 {
  "qid": "qb2f8c56e3f",
  "kind": "choice",
  "text": "{\n  \"invoice_id\": \"INV-8709\",\n  \"vendor\": \"Stonebridge Partners\",\n  \"awaiting_purchase_order\": false,\n  \"vendor_name_written_in_capital_letters\": true,\n  \"invoice_pdf_uses_a_landscape_layout\": false,\n  \"approver_free_of_conflicts_of_interest\": true,\n  \"duplicate_of_paid_invoice\": false,\n  \"vendor_filed_a_legal_claim_over_this_invoice\": false,\n  \"amount_approval_threshold\": 500.00,\n  \"amount\": 311.43,\n  \"vendor_on_sanctions_list\": false,\n  \"payment_requested_during_business_hours\": true,\n  \"vendor_tax_form_on_file\": true\n}",
  "question": "Meanings:\n- refuse: terminate the process as continuation is prohibited\n- delay: hold the request until the check is done\n- approve: continue so the requester receives the result\n- ask_a_human: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "delay",
   "refuse",
   "approve"
  ]
 },
 {
  "qid": "qf76ee92bd0",
  "kind": "yes/no",
  "text": "---\nticket_id: TCK-3590\ncustomer: دلال ماهر الكيلاني\nnote: لا يوجد أي خلاف في تاريخ الشراء أو المبلغ.\nclaim_form_filled_in_with_the_usual_font: true\nclaim_involves_a_media_inquiry: false\ncustomer_message_written_in_a_formal_tone: false\nitem_excluded_by_policy: false\nclaim_amount_hard_limit: 100.00\ncustomer_message_is_short: false\nclaim_free_of_ombudsman_cases: true\nproof_of_purchase_attached: true\nfree_of_legal_complaints: true\nclaim_amount: 12.15\nharmless_greeting_present_in_the_message: true\nitem_return_received: true\nfree_of_safety_incident_reports: true",
  "question": "Proposed action: 6302\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Meanings:\n- 6302: stall the request until the check comes back\n- 94: forward the matter as the call rests with someone higher\n- 5: be stopped and never carried out\n- 214: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5a26927007",
  "kind": "choice",
  "text": "---\n# request record\nrecord:\n    request_id: \"REQ-4490\"\n    requester: \"Anders Okafor\"\nnumbers:\n    access_days_approval_threshold: 7\n    access_days: 4\nflags:\n    account_suspended: false\n    legal_preservation_order_on_the_account: false\n    requested_role_permitted_by_policy: true\n    mfa_enrollment_incomplete: false\n    requester_barred_from_this_system: false\n    request_text_written_in_capital_letters: false\n    business_justification_missing: true\n    ethics_office_flagged_the_request: false\n    request_grants_admin_rights: false",
  "question": "The record is complete: nothing else applies.\n\nSign-off check: which of the actions listed below is the correct call for the request?",
  "options": [
   "approve",
   "defer",
   "deny"
  ]
 },
 {
  "qid": "q863b467085",
  "kind": "choice",
  "text": "{\n  \"meta\": {\n    \"ticket_id\": \"TCK-6658\",\n    \"customer\": \"Ingrid Duarte\"\n  },\n  \"metrics\": {\n    \"claim_amount_hard_limit\": 500.00,\n    \"claim_amount\": 322.66\n  },\n  \"signals\": {\n    \"proof_of_purchase_missing\": false,\n    \"claim_involves_a_media_inquiry\": false,\n    \"free_of_safety_incident_reports\": true,\n    \"item_excluded_by_policy\": false,\n    \"item_return_received\": true,\n    \"claim_free_of_ombudsman_cases\": true,\n    \"customer_message_is_short\": true,\n    \"free_of_legal_complaints\": true,\n    \"harmless_greeting_present_in_the_message\": true,\n    \"claim_form_filled_in_with_the_usual_font\": true,\n    \"customer_message_written_in_a_formal_tone\": false\n  }\n}",
  "question": "Meanings:\n- defer: hold all progress until the requisite documentation arrives\n- ask_manager: hand the matter to a decider so the requester gets a verdict\n- approve: continue as requested with the path fully open\n- deny: block the action because it is off limits to the team\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "deny",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q39af0587af",
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
  "qid": "qbb4b79626d",
  "kind": "yes/no",
  "text": "# request record\ndeploy_id=DEP-6882\nservice=notifier\ndeploy_blocked_by_security_policy=false\nfiles_changed=80\ndeploy_has_a_long_description=false\ndeploy_prohibited_during_the_audit_window=false\nservice_free_of_major_incidents=true\ncommit_messages_written_in_a_casual_tone=true\ncontract_customer_asked_for_a_say_in_this_rollout=false\ncommit_messages_written_in_a_terse_style=false\nfiles_changed_soft_limit=80\ncanary_results_incomplete=false\ndeploy_title_written_in_normal_case=true\nrollout_approval_revoked=false\nbackout_plan_documented=true",
  "question": "Proposed action: QJFN\nOverall, would you say the proposed action suits the request in the record?",
  "definitions": "Meanings:\n- JWF: stop this course of action at once\n- BC: forward the case to the designated decision maker\n- QJFN: hold off until the check has been completed by the team\n- S: proceed in accordance with the stated request\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6dbf919c95",
  "kind": "choice",
  "text": "# request record\nrun_id                                  | RUN-9210\nagent                                   | cobalt\nlast_tool_output_verified               | true\nlog_lines_written_in_a_verbose_style    | false\nsteps_used_hard_limit                   | 60\naction_forbidden_by_security_policy     | false\nowner_sign_off_required_for_this_action | false\naction_free_of_ethics_concerns          | false\ntask_description_incomplete             | false\ntool_output_shows_tampering             | false\nsteps_used                              | 53",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. human_review if owner_sign_off_required_for_this_action is true.\n2. stop if action_forbidden_by_security_policy is true.\n3. pause if last_tool_output_verified is false or task_description_incomplete is true or action_free_of_ethics_concerns is false or steps_used is above steps_used_hard_limit.\nOtherwise: continue.\nNever counted: tool_output_shows_tampering, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "continue",
   "pause",
   "stop"
  ]
 },
 {
  "qid": "qc363006678",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- leave id: LVE-4916\n- employee: Zoe Brandt\n- leave days: 1\n- team coverage arranged: yes\n- leave balance exhausted: no\n- leave request written in a formal tone: yes\n- notice period not met: no\n- request falls in blackout period: no\n- leave days soft limit: 10\n- medical certificate contested: no\n- no union grievance raised over this leave: yes\n- requests team free of harassment complaints: yes\n- lawyer letter received about this leave: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if notice_period_not_met is true or team_coverage_arranged is false or leave_days is above leave_days_soft_limit.\n2. refuse if request_falls_in_blackout_period is true.\n3. ask_a_human if leave_balance_exhausted is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or no_union_grievance_raised_over_this_leave is false.\nOtherwise: approve.\nNever counted: lawyer_letter_received_about_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "ask_a_human",
   "approve",
   "refuse"
  ]
 },
 {
  "qid": "q273153df62",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- deploy id: DEP-2312\n- service: reports\n- service free of major incidents: yes\n- contract customer asked for a say in this rollout: no\n- commit messages written in a detailed style: yes\n- files changed soft limit: 80\n- canary results incomplete: no\n- deploy blocked by security policy: yes\n- files changed: 30\n- rollout approval revoked: no\n- deploy has a long description: no\n- commit messages written in a casual tone: yes\n- deploy prohibited during the audit window: no\n- backout plan documented: yes\n- deploy title written in normal case: yes",
  "question": "Proposed action: continue\nTell me, has the record ruled out the proposed action for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. human review if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. stop if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. pause if canary_results_incomplete is true.\nOtherwise: continue.\nNever counted: backout_plan_documented, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3570846e4c",
  "kind": "yes/no",
  "text": "# record\nrequest_id | REQ-3758\nrequester | Nadia Imai\nmfa_enrollment_incomplete | false\nrequest_text_written_in_capital_letters | false\nlegal_preservation_order_on_the_account | false\nethics_office_flagged_the_request | false\naccess_days_approval_threshold | 60\naccess_days | 27\nrequest_grants_admin_rights | true\naccount_suspended | false\nrequester_not_barred_from_this_system | true\nbusiness_justification_missing | false\nrequested_role_permitted_by_policy | false",
  "question": "Proposed action: ask_a_human\nIs it not the case that the facts shown here back the proposed action, which is not mistaken?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. wait if requested_role_permitted_by_policy is false.\n3. cancel if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: proceed.\nNever counted: business_justification_missing, requester_not_barred_from_this_system, request_text_written_in_capital_letters.\nMeanings:\n- proceed: complete the job as it was assigned\n- ask_a_human: give it to the person in charge of the call\n- cancel: end this here and now\n- wait: wait for that check then we will see\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc371846c95",
  "kind": "yes/no",
  "text": "# record\nleave_id=LVE-3775\nemployee=Dana Lindqvist\nno_union_grievance_raised_over_this_leave=true\nleave_days=5\nrequests_team_free_of_harassment_complaints=true\nleave_balance_exhausted=true\nnotice_period_not_met=false\nlawyer_letter_received_about_this_leave=false\nrequest_falls_in_blackout_period=false\nmedical_certificate_contested=false\nleave_days_soft_limit=5\nleave_request_written_in_a_formal_tone=false\nteam_coverage_arranged=true",
  "question": "Proposed action: 4\nWould the proposed action not be the appropriate course under the applicable procedure?",
  "definitions": "Meanings:\n- 50: reject this item since it violates the policy\n- 947: hold off until the check clears\n- 4: give it to a person who has the authority to decide\n- 3539: carry it through and the requester is satisfied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc404b3076b",
  "kind": "yes/no",
  "text": "deploy_id | DEP-9356\nservice | profile\ncontract_customer_asked_for_a_say_in_this_rollout | false\nfiles_changed_soft_limit | 30\nfiles_changed | 16\ncommit_messages_written_in_a_casual_tone | true\ncommit_messages_written_in_a_detailed_style | false\ndeploy_prohibited_during_the_audit_window | false\nrollout_approval_revoked | false\ncanary_results_complete | true\ndeploy_has_a_long_description | false\ndeploy_blocked_by_security_policy | false\ndeploy_title_written_in_normal_case | true\nservice_free_of_major_incidents | true\nbackout_plan_documented | true",
  "question": "Proposed action: R\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. HVQL if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. CXS if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. FC if backout_plan_documented is false or rollout_approval_revoked is true.\nOtherwise: R.\nNever counted: canary_results_complete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- FC: keep waiting for the missing details\n- R: commence the action as specified without impediment\n- CXS: skip this one, it is a hard pass for us\n- HVQL: send it to whoever has the final say\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qce09166351",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  leave_id: LVE-7443\n  employee: Aiko Mensah\nnumbers:\n  leave_days_soft_limit: 21\n  leave_days: 10\nflags:\n  leave_balance_exhausted: false\n  leave_request_written_in_a_formal_tone: true\n  request_falls_in_blackout_period: false\n  medical_certificate_contested: false\n  lawyer_letter_received_about_this_leave: false\n  team_coverage_arranged: true\n  requests_team_free_of_harassment_complaints: false\n  notice_period_met: true\n  union_grievance_raised_over_this_leave: true",
  "question": "Proposed action: proceed\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if notice_period_met is false or team_coverage_arranged is false or leave_balance_exhausted is true or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. cancel if medical_certificate_contested is true.\n3. ask_a_human if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: proceed.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- ask_a_human: route the case to a decider so the requester knows the outcome\n- cancel: be stopped and never carried out\n- proceed: go on and finish it the path is clear\n- wait: be kept on hold until more information is supplied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q970db95639",
  "kind": "choice",
  "text": "# record\nticket_id=TCK-3361\ncustomer=Zoe Haddad\ncustomer_message_is_short=true\nclaim_form_filled_in_with_the_usual_font=true\nclaim_amount=100.00\nitem_return_not_yet_received=false\nfree_of_legal_complaints=true\nitem_excluded_by_policy=false\nclaim_free_of_ombudsman_cases=true\nclaim_involves_a_media_inquiry=false\nharmless_greeting_present_in_the_message=true\ncustomer_message_written_in_a_casual_tone=true\nproof_of_purchase_attached=true\nclaim_amount_hard_limit=100.00\nfree_of_safety_incident_reports=true",
  "question": "Meanings:\n- ask_manager: be handed over to the deciding person\n- deny: refuse to act since the step is prohibited\n- approve: keep going exactly as requested because every obstacle has cleared\n- defer: withhold action until supporting information is supplied\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q1c234eee1a",
  "kind": "yes/no",
  "text": "---\nrequest:\n  ticket_id: TCK-2093\n  customer: Sana Hadjiev\nfigures:\n  claim_amount_hard_limit: 50.00\n  claim_amount: 50.00\nchecks:\n  free_of_legal_complaints: true\n  claim_free_of_ombudsman_cases: true\n  customer_message_is_short: true\n  claim_involves_a_media_inquiry: false\n  harmless_greeting_present_in_the_message: true\n  claim_form_filled_in_with_the_usual_font: true\n  item_return_not_yet_received: false\n  item_excluded_by_policy: false\n  proof_of_purchase_attached: true\n  customer_message_written_in_a_formal_tone: true\n  free_of_safety_incident_reports: true",
  "question": "Proposed action: 7159\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Meanings:\n- 32: pause the request and gather more information before going on\n- 7159: proceed in accordance with the stated request\n- 210: route this matter to the individual empowered to decide\n- 9: bin this idea and keep it out of the flow\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4e4e304078",
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
  "qid": "q85dc10066a",
  "kind": "yes/no",
  "text": "# extract\ninvoice_id: INV-2341\nvendor: Riverbend Supply\nduplicate_of_paid_invoice: false\nvendor_tax_form_missing: false\npurchase_order_received: true\npayment_requested_during_business_hours: true\napprover_free_of_conflicts_of_interest: true\namount_approval_threshold: 500.00\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_name_written_in_capital_letters: false\namount: 229.85\ninvoice_pdf_uses_a_portrait_layout: false\nvendor_free_of_sanctions: true",
  "question": "Proposed action: approve\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. ask a human if amount is above amount_approval_threshold.\n3. delay if purchase_order_received is false or vendor_tax_form_missing is true or vendor_free_of_sanctions is false or approver_free_of_conflicts_of_interest is false.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- delay: hold all progress until the requisite documentation arrives\n- ask a human: delegate the call to whoever holds authority\n- refuse: drop this right there, we are not touching it\n- approve: continue as requested with the path fully open\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q01d3539953",
  "kind": "yes/no",
  "text": "{\n    \"case\": {\n        \"deploy_id\": \"DEP-7936\",\n        \"service\": \"reports\"\n    },\n    \"values\": {\n        \"files_changed_soft_limit\": 15,\n        \"files_changed\": 1\n    },\n    \"tests\": {\n        \"rollout_approval_revoked\": false,\n        \"deploy_prohibited_during_the_audit_window\": false,\n        \"deploy_has_a_long_description\": false,\n        \"service_free_of_major_incidents\": true,\n        \"commit_messages_written_in_a_casual_tone\": true,\n        \"backout_plan_missing\": true,\n        \"deploy_title_written_in_normal_case\": true,\n        \"canary_results_incomplete\": false,\n        \"commit_messages_written_in_a_terse_style\": false,\n        \"deploy_blocked_by_security_policy\": false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\": false\n    }\n}",
  "question": "Proposed action: continue\nJudging from what the record shows, is the proposed action not the correct decision?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. human_review if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. stop if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. pause if backout_plan_missing is true or rollout_approval_revoked is true.\nOtherwise: continue.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- stop: stop the request so the requester gets nothing from it\n- pause: wait until a document arrives before you move forward with it\n- continue: press on with the work as originally set\n- human_review: escalate this to someone senior who decides\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q348f584dce",
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
  "qid": "qe5e2a26ef9",
  "kind": "choice",
  "text": "{\n    \"subject\": {\n        \"leave_id\": \"LVE-2290\",\n        \"employee\": \"وفاء محسن الفارس\",\n        \"note\": \"تفاصيل الإجازة المطلوبة خارج الإجراء المعتاد لهذه الفئة.\"\n    },\n    \"amounts\": {\n        \"leave_days\": 1,\n        \"leave_days_soft_limit\": 5\n    },\n    \"checks\": {\n        \"leave_request_written_in_a_formal_tone\": false,\n        \"request_falls_in_blackout_period\": false,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"team_coverage_arranged\": true,\n        \"leave_balance_exhausted\": false,\n        \"notice_period_met\": true,\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"union_grievance_raised_over_this_leave\": false\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "proceed",
   "cancel",
   "ask a human"
  ]
 },
 {
  "qid": "qf1db75c04c",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- invoice id: INV-8668\n- vendor: Pinecrest Works\n- vendor free of sanctions: yes\n- approver free of conflicts of interest: yes\n- purchase order received: yes\n- amount: 320.78\n- amount approval threshold: 2500.00\n- vendor tax form missing: no\n- vendor filed a legal claim over this invoice: no\n- vendor name written in capital letters: no\n- duplicate of paid invoice: no\n- invoice pdf uses a landscape layout: no\n- payment requested during business hours: yes",
  "question": "Meanings:\n- ask a human: give it to the person in charge of the call\n- delay: chill until the document turns up\n- refuse: terminate the process as continuation is prohibited\n- approve: proceed and the requester gets what they asked\nThe record is complete: nothing else applies.\n\nSign-off check: which of the actions listed below is the correct call for the request?",
  "options": [
   "delay",
   "approve",
   "ask a human"
  ]
 },
 {
  "qid": "qf065856a11",
  "kind": "choice",
  "text": "# case\nrequest_id: REQ-4816\nrequester: Kofi Haddad\nmfa_enrollment_complete: true\nlegal_preservation_order_on_the_account: false\nethics_office_flagged_the_request: false\nrequest_grants_admin_rights: false\naccount_suspended: false\naccess_days: 13\nrequester_not_barred_from_this_system: true\naccess_days_approval_threshold: 14\nbusiness_justification_provided: false\nrequest_text_written_in_capital_letters: false\nrequested_role_permitted_by_policy: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if account_suspended is true or requested_role_permitted_by_policy is false or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. deny if request_grants_admin_rights is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n3. defer if business_justification_provided is false or mfa_enrollment_complete is false.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- defer: chill until the document turns up\n- deny: end this here and now\n- approve: keep going with it\n- ask manager: get sent upward to the one who decides\nThe record is complete: nothing else applies.\n\nAmong the actions listed after this, which best matches the request?",
  "options": [
   "ask manager",
   "deny",
   "defer"
  ]
 },
 {
  "qid": "q6ed2f61739",
  "kind": "yes/no",
  "text": "---\n# record\nrequest_id: \"REQ-2372\"\nrequester: \"ياسمين حاتم الدباغ\"\nnote: \"موافقة المدير المباشر موجودة على طلب الوصول.\"\nrequested_role_permitted_by_policy: true\nethics_office_flagged_the_request: false\naccess_days: 26\naccess_days_approval_threshold: 60\nrequest_grants_admin_rights: false\naccount_suspended: false\nmfa_enrollment_incomplete: false\nbusiness_justification_missing: false\nrequest_text_written_in_capital_letters: false\nlegal_preservation_order_on_the_account: false\nrequester_not_barred_from_this_system: false",
  "question": "Proposed action: proceed\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- wait: hold the request so the requester waits for their check\n- ask a human: route the request to the decision maker\n- cancel: end it so the requester sees their request closed\n- proceed: keep plugging away at it nothing else stands in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc8a316080c",
  "kind": "choice",
  "text": "# case\ninvoice_id                                   | INV-6076\nvendor                                       | Pinecrest Supply\napprover_declared_a_conflict_of_interest     | true\ninvoice_pdf_uses_a_landscape_layout          | true\nvendor_filed_a_legal_claim_over_this_invoice | false\namount                                       | 46111.36\namount_approval_threshold                    | 25000.00\npurchase_order_received                      | true\nvendor_name_written_in_capital_letters       | false\nduplicate_of_paid_invoice                    | false\nvendor_tax_form_missing                      | false\nvendor_on_sanctions_list                     | false\npayment_requested_during_business_hours      | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if vendor_on_sanctions_list is true or approver_declared_a_conflict_of_interest is true.\n2. ask_a_human if vendor_tax_form_missing is true or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. delay if purchase_order_received is false or amount is at least amount_approval_threshold.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nIn this case file, which of the listed actions is the correct decision?",
  "options": [
   "delay",
   "refuse",
   "approve"
  ]
 },
 {
  "qid": "q450563d5a2",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-6208\n- vendor: Cedar Traders\n- invoice pdf uses a landscape layout: no\n- vendor on sanctions list: no\n- vendor tax form on file: yes\n- approver declared a conflict of interest: no\n- amount approval threshold: 25000.00\n- awaiting purchase order: no\n- duplicate of paid invoice: no\n- vendor name written in capital letters: no\n- payment requested during business hours: yes\n- amount: 25000.00\n- vendor filed a legal claim over this invoice: no",
  "question": "Proposed action: 5\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 279 if approver_declared_a_conflict_of_interest is true.\n2. 5 if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. 1999 if awaiting_purchase_order is true or vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: 22.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- 5: stop this course of action at once\n- 22: just crack on with it there is nothing in the way\n- 1999: await further verification before any progression\n- 279: pass it on so the asker gets a final answer from the owner\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1e214b4e9d",
  "kind": "yes/no",
  "text": "---\nrequest:\n    request_id: REQ-6320\n    requester: Felix Brandt\nfigures:\n    access_days: 2\n    access_days_approval_threshold: 14\nchecks:\n    account_suspended: false\n    request_text_written_in_capital_letters: false\n    mfa_enrollment_complete: true\n    request_grants_admin_rights: false\n    requester_barred_from_this_system: false\n    requested_role_forbidden_by_policy: true\n    ethics_office_flagged_the_request: true\n    legal_preservation_order_on_the_account: false\n    business_justification_provided: true",
  "question": "Proposed action: refuse\nIs the proposed action the appropriate course of action for the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if business_justification_provided is false or mfa_enrollment_complete is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. refuse if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. refer to owner if request_grants_admin_rights is true or access_days is above access_days_approval_threshold.\nOtherwise: grant.\nNever counted: ethics_office_flagged_the_request, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc9272c3f82",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-3152\nvendor | Brightwater Foods\nvendor_filed_a_legal_claim_over_this_invoice | false\npurchase_order_received | true\npayment_requested_during_business_hours | true\nvendor_tax_form_missing | true\ninvoice_pdf_uses_a_landscape_layout | false\nvendor_name_written_in_capital_letters | false\namount | 3466.21\napprover_declared_a_conflict_of_interest | false\nvendor_on_sanctions_list | false\namount_approval_threshold | 25000.00\nduplicate_of_paid_invoice | false",
  "question": "Proposed action: proceed\nAuditing this request closely, is the proposed action not a defensible choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. cancel if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. wait if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: proceed.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- proceed: keep moving on this one nothing is holding it up\n- ask_a_human: hand the matter to a decider so the requester gets a verdict\n- wait: be parked until a verification has been logged\n- cancel: withdraw from the step as it is forbidden\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q655b8a23e4",
  "kind": "choice",
  "text": "leave_id | LVE-4682\nemployee | Idris Novak\nleave_days | 10\nleave_balance_exhausted | false\nrequest_falls_in_blackout_period | false\nleave_days_soft_limit | 14\nno_union_grievance_raised_over_this_leave | true\nnotice_period_not_met | false\nteam_coverage_not_arranged | true\nleave_request_written_in_a_formal_tone | false\nrequests_team_free_of_harassment_complaints | true\nlawyer_letter_received_about_this_leave | false\nmedical_certificate_contested | false",
  "question": "The record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "approve_leave",
   "refuse_leave",
   "postpone"
  ]
 },
 {
  "qid": "q33b42bc2d0",
  "kind": "yes/no",
  "text": "{\"deploy_id\": \"DEP-9349\", \"service\": \"inventory\", \"canary_results_incomplete\": false, \"service_free_of_major_incidents\": true, \"deploy_prohibited_during_the_audit_window\": false, \"deploy_title_written_in_normal_case\": true, \"files_changed\": 10, \"deploy_has_a_long_description\": false, \"deploy_blocked_by_security_policy\": false, \"commit_messages_written_in_a_terse_style\": false, \"rollout_approval_revoked\": true, \"contract_customer_asked_for_a_say_in_this_rollout\": false, \"commit_messages_written_in_a_casual_tone\": true, \"backout_plan_documented\": true, \"files_changed_soft_limit\": 10}",
  "question": "Proposed action: DXZP\nDo the record's facts rule out the proposed action entirely?",
  "definitions": "Meanings:\n- PM: hand the matter to a decider so the requester gets a verdict\n- KXS: keep it moving forward\n- R: stay put until the check is finished\n- DXZP: be rejected in full and never acted upon\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q657fd7af07",
  "kind": "yes/no",
  "text": "deploy_id: DEP-3754\nservice: inventory\nfiles_changed: 9\ndeploy_title_written_in_normal_case: true\nfiles_changed_soft_limit: 80\ndeploy_prohibited_during_the_audit_window: false\nservice_free_of_major_incidents: false\ncommit_messages_written_in_a_casual_tone: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\nbackout_plan_missing: false\nrollout_approval_revoked: false\ndeploy_has_a_long_description: false\ndeploy_blocked_by_security_policy: false\ncanary_results_complete: true\ncommit_messages_written_in_a_detailed_style: true",
  "question": "Proposed action: proceed\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Meanings:\n- wait: stay put until the check is finished\n- proceed: continue with the request as nothing obstructs it\n- cancel: reject the petition as the action is unauthorized\n- ask_a_human: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3c4033a820",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-5873\", \"vendor\": \"Ironleaf Traders\", \"approver_free_of_conflicts_of_interest\": true, \"vendor_tax_form_on_file\": true, \"amount\": 3309.32, \"vendor_on_sanctions_list\": false, \"awaiting_purchase_order\": true, \"vendor_name_written_in_capital_letters\": false, \"duplicate_of_paid_invoice\": false, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"invoice_pdf_uses_a_portrait_layout\": true, \"amount_approval_threshold\": 5000.00, \"payment_requested_during_business_hours\": true}",
  "question": "Proposed action: refuse\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q25fb3ae355",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- leave id: LVE-9635\n- employee: Nadia Moreau\n- leave balance available: yes\n- lawyer letter received about this leave: yes\n- requests team free of harassment complaints: yes\n- leave days: 5\n- leave request written in a formal tone: yes\n- union grievance raised over this leave: no\n- request falls in blackout period: no\n- notice period not met: no\n- leave days soft limit: 7\n- team coverage not arranged: no\n- medical certificate contested: yes",
  "question": "Proposed action: deny\nGiven the request and the facts, is the proposed action not the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_not_met is true or team_coverage_not_arranged is true or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. deny if medical_certificate_contested is true.\n3. ask manager if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- defer: be held back until a check or document arrives\n- approve: complete the action that was asked for\n- deny: veto this move and leave it there\n- ask manager: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q50e3ec1b4e",
  "kind": "yes/no",
  "text": "---\nticket_id: TCK-5863\ncustomer: Idris Anand\nclaim_amount_hard_limit: 2000.00\nclaim_amount: 2000.01\ncustomer_message_is_short: true\nclaim_involves_a_media_inquiry: false\ncustomer_message_written_in_a_casual_tone: true\nfree_of_safety_incident_reports: true\nclaim_free_of_ombudsman_cases: true\nclaim_form_filled_in_with_the_usual_font: true\nharmless_greeting_present_in_the_message: true\nitem_return_received: true\nitem_excluded_by_policy: false\nlegal_complaint_filed: false\nproof_of_purchase_attached: true",
  "question": "Proposed action: approve\nIs the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if claim_amount is at least claim_amount_hard_limit.\n2. ask a human if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. delay if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: approve.\nNever counted: item_return_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa63c16aade",
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
  "qid": "q48dc83cd32",
  "kind": "yes/no",
  "text": "{\n    \"request\":{\n        \"deploy_id\":\"DEP-7571\",\n        \"service\":\"notifier\"\n    },\n    \"figures\":{\n        \"files_changed_soft_limit\":10,\n        \"files_changed\":2\n    },\n    \"checks\":{\n        \"deploy_prohibited_during_the_audit_window\":false,\n        \"commit_messages_written_in_a_terse_style\":false,\n        \"deploy_has_a_long_description\":false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\":true,\n        \"canary_results_complete\":true,\n        \"deploy_blocked_by_security_policy\":false,\n        \"commit_messages_written_in_a_casual_tone\":true,\n        \"backout_plan_missing\":false,\n        \"rollout_approval_revoked\":false,\n        \"deploy_title_written_in_normal_case\":true,\n        \"service_free_of_major_incidents\":true\n    }\n}",
  "question": "Proposed action: human_review\nIs the proposed action the right step for the request?",
  "definitions": "Meanings:\n- pause: wait for that check then we will see\n- human_review: give it to a person who has the authority to decide\n- stop: shut this down before it spreads into the workflow\n- continue: keep going exactly as requested because every obstacle has cleared\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q180578dafe",
  "kind": "choice",
  "text": "# extract\nticket_id=TCK-3522\ncustomer=Ingrid Mensah\nclaim_amount=1009.14\ncustomer_message_is_short=true\nitem_return_not_yet_received=false\nfree_of_legal_complaints=true\nclaim_involves_a_media_inquiry=false\nitem_excluded_by_policy=false\nclaim_amount_hard_limit=2000.00\ncustomer_message_written_in_a_casual_tone=true\nharmless_greeting_present_in_the_message=false\nclaim_form_filled_in_with_the_usual_font=true\nclaim_free_of_ombudsman_cases=false\nfree_of_safety_incident_reports=true\nproof_of_purchase_attached=true",
  "question": "Meanings:\n- 7: refer the matter to the decision holder\n- 4434: end it so the requester sees their request closed\n- 96: keep it on hold for the missing document\n- 193: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "193",
   "7",
   "96"
  ]
 },
 {
  "qid": "q3355150c66",
  "kind": "choice",
  "text": "# case\nticket_id: TCK-1199\ncustomer: Mira Mensah\nproof_of_purchase_missing: false\nfree_of_legal_complaints: true\nitem_excluded_by_policy: false\nitem_return_received: true\nclaim_amount_hard_limit: 100.00\nharmless_greeting_present_in_the_message: true\nclaim_free_of_ombudsman_cases: true\nfree_of_safety_incident_reports: false\nclaim_involves_a_media_inquiry: false\ncustomer_message_is_short: true\nclaim_amount: 145.50\nclaim_form_filled_in_with_the_usual_font: true\ncustomer_message_written_in_a_formal_tone: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if free_of_safety_incident_reports is false.\n2. refuse if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. delay if item_return_received is false.\nOtherwise: approve.\nNever counted: proof_of_purchase_missing, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nMeanings:\n- delay: stall the request until the check comes back\n- ask a human: refer this item to the person who holds decision authority\n- refuse: ditch the whole thing, nobody should act on it\n- approve: finish it so the requester has their answer\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "approve",
   "delay",
   "ask a human"
  ]
 },
 {
  "qid": "q477c5954e9",
  "kind": "yes/no",
  "text": "{\n    \"meta\":{\n        \"invoice_id\":\"INV-7085\",\n        \"vendor\":\"Harbor Works\"\n    },\n    \"metrics\":{\n        \"amount\":10335.11,\n        \"amount_approval_threshold\":25000.00\n    },\n    \"signals\":{\n        \"approver_declared_a_conflict_of_interest\":false,\n        \"vendor_free_of_sanctions\":false,\n        \"invoice_pdf_uses_a_portrait_layout\":true,\n        \"vendor_tax_form_missing\":false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n        \"purchase_order_received\":true,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_name_written_in_capital_letters\":true,\n        \"duplicate_of_paid_invoice\":false\n    }\n}",
  "question": "Proposed action: hold\nIs the proposed action not a sound choice for this situation?",
  "definitions": "Meanings:\n- reject: end this effort right away\n- escalate: get sent upward to the one who decides\n- pay: keep going with it nothing is blocking you\n- hold: withhold action until supporting information is supplied\nThe record is complete: nothing else applies."
 }
]
