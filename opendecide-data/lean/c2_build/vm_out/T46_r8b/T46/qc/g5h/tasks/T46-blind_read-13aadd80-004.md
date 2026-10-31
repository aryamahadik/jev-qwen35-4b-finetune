# G5-H blind read T46-blind_read-13aadd80-004 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8b/T46/qc/g5h/answers/T46-blind_read-13aadd80-004.json

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
  "qid": "qb82367a430",
  "kind": "choice",
  "text": "{\"ticket_id\":\"TCK-8632\",\"customer\":\"Nadia Tanaka\",\"customer_message_written_in_a_casual_tone\":true,\"proof_of_purchase_missing\":false,\"item_return_not_yet_received\":false,\"harmless_greeting_present_in_the_message\":true,\"claim_free_of_ombudsman_cases\":true,\"legal_complaint_filed\":false,\"claim_form_filled_in_with_the_usual_font\":true,\"free_of_safety_incident_reports\":false,\"item_excluded_by_policy\":false,\"claim_amount\":194.81,\"customer_message_is_short\":true,\"claim_amount_hard_limit\":200.00,\"claim_involves_a_media_inquiry\":false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if item_return_not_yet_received is true or claim_free_of_ombudsman_cases is false.\n2. cancel if item_excluded_by_policy is true or legal_complaint_filed is true or claim_amount is above claim_amount_hard_limit.\n3. ask_a_human if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: proceed.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nTaking the facts of the request into account, which action listed should be picked?",
  "options": [
   "wait",
   "cancel",
   "proceed"
  ]
 },
 {
  "qid": "q4fdfbc8352",
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
  "qid": "q88f794fde0",
  "kind": "yes/no",
  "text": "---\n# record\nrequest_id: \"REQ-2372\"\nrequester: \"ياسمين حاتم الدباغ\"\nnote: \"موافقة المدير المباشر موجودة على طلب الوصول.\"\nrequested_role_permitted_by_policy: true\nethics_office_flagged_the_request: false\naccess_days: 26\naccess_days_approval_threshold: 60\nrequest_grants_admin_rights: false\naccount_suspended: false\nmfa_enrollment_incomplete: false\nbusiness_justification_missing: false\nrequest_text_written_in_capital_letters: false\nlegal_preservation_order_on_the_account: false\nrequester_not_barred_from_this_system: false",
  "question": "Proposed action: proceed\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- wait: hold the request so the requester waits for their check\n- ask a human: route the request to the decision maker\n- cancel: end it so the requester sees their request closed\n- proceed: keep plugging away at it nothing else stands in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd3d6fa1e66",
  "kind": "yes/no",
  "text": "{\"request_id\":\"REQ-8051\",\"requester\":\"Hugo Mensah\",\"legal_preservation_order_on_the_account\":false,\"request_grants_admin_rights\":false,\"access_days_approval_threshold\":60,\"request_text_written_in_capital_letters\":true,\"access_days\":60,\"requester_barred_from_this_system\":false,\"business_justification_missing\":true,\"request_free_of_ethics_office_flags\":true,\"account_suspended\":false,\"requested_role_forbidden_by_policy\":false,\"mfa_enrollment_complete\":true}",
  "question": "Proposed action: 2677\nShould the proposed action be taken for this request?",
  "definitions": "Meanings:\n- 698: keep moving on this one nothing is holding it up\n- 7: reject the petition as the action is unauthorized\n- 18: bring in the owner who can rule on this\n- 2677: hold the request so the requester waits for their check\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qdaa73fd9ea",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n    invoice_id: INV-1641\n    vendor: Silverline Group\namounts:\n    amount_approval_threshold: 10000.00\n    amount: 1145.77\nchecks:\n    approver_declared_a_conflict_of_interest: true\n    duplicate_of_paid_invoice: false\n    vendor_free_of_sanctions: true\n    payment_requested_during_business_hours: true\n    vendor_name_written_in_capital_letters: false\n    purchase_order_received: false\n    invoice_pdf_uses_a_portrait_layout: true\n    vendor_tax_form_missing: false\n    vendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hand_to_a_person if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. cancel_order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. delay if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "delay",
   "hand_to_a_person",
   "release"
  ]
 },
 {
  "qid": "qe4adb71cec",
  "kind": "choice",
  "text": "# extract\nticket_id=TCK-9810\ncustomer=Hugo Novak\nclaim_free_of_ombudsman_cases=true\nlegal_complaint_filed=false\nproof_of_purchase_attached=true\ncustomer_message_is_short=true\nclaim_involves_a_media_inquiry=false\nclaim_amount=536.39\ncustomer_message_written_in_a_casual_tone=true\nharmless_greeting_present_in_the_message=true\nfree_of_safety_incident_reports=true\nclaim_form_filled_in_with_the_usual_font=true\nitem_excluded_by_policy=false\nclaim_amount_hard_limit=1000.00\nitem_return_not_yet_received=false",
  "question": "Meanings:\n- refuse: reject the request in full\n- approve: continue as requested with the path fully open\n- delay: wait for the missing material to come in before deciding anything\n- ask a human: delegate the call to whoever holds authority\nThe record is complete: nothing else applies.\n\nBased on what the record shows, which of the actions listed is the right call?",
  "options": [
   "refuse",
   "approve",
   "delay"
  ]
 },
 {
  "qid": "qa5ccdccc22",
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
  "qid": "qbd50573277",
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
  "qid": "q175db7589f",
  "kind": "yes/no",
  "text": "{\n  \"request_id\":\"REQ-1430\",\n  \"requester\":\"Idris Adeyemi\",\n  \"requested_role_permitted_by_policy\":true,\n  \"business_justification_provided\":true,\n  \"legal_preservation_order_on_the_account\":false,\n  \"request_free_of_ethics_office_flags\":true,\n  \"access_days_approval_threshold\":7,\n  \"request_grants_admin_rights\":false,\n  \"requester_not_barred_from_this_system\":true,\n  \"access_days\":4,\n  \"mfa_enrollment_complete\":true,\n  \"request_text_written_in_capital_letters\":false,\n  \"account_suspended\":false\n}",
  "question": "Proposed action: allow\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_provided is false or requested_role_permitted_by_policy is false.\n2. page oncall if mfa_enrollment_complete is false or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. block access if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: allow.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- block access: shut this down fast\n- allow: proceed with the task as asked\n- quarantine: defer the step until the verification is in\n- page oncall: send it up so the requester gets a firm decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q354bc69e2c",
  "kind": "choice",
  "text": "---\nleave_id: \"LVE-7952\"\nemployee: \"سوسن أمجد الراشد\"\nnote: \"طلب الإجازة مقدم في الموعد المحدد بالسياسة.\"\nrequest_falls_in_blackout_period: false\nlawyer_letter_received_about_this_leave: false\nno_union_grievance_raised_over_this_leave: true\nrequests_team_free_of_harassment_complaints: true\nnotice_period_met: true\nteam_coverage_arranged: true\nleave_days: 2\nleave_days_soft_limit: 10\nleave_request_written_in_a_formal_tone: false\nmedical_certificate_contested: false\nleave_balance_available: true",
  "question": "The record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "postpone",
   "approve_leave",
   "refer_to_hr"
  ]
 },
 {
  "qid": "q42b8abd1f2",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n    run_id: RUN-6764\n    agent: lumen\nvalues:\n    steps_used: 5\n    steps_used_hard_limit: 8\ntests:\n    task_description_incomplete: false\n    last_tool_output_verified: false\n    action_free_of_ethics_concerns: true\n    action_permitted_by_security_policy: true\n    tool_output_shows_tampering: false\n    owner_sign_off_required_for_this_action: false\n    log_lines_written_in_a_compact_style: true",
  "question": "Meanings:\n- 7690: go ahead with the requested action\n- 820: hand this to the person who decides\n- 32: shut this down fast\n- 7: suspend progress until verification is received\nThe record is complete: nothing else applies.\n\nGiven what the requester needs, which of the actions below should be taken?",
  "options": [
   "7",
   "32",
   "7690"
  ]
 },
 {
  "qid": "q60a38e2a5c",
  "kind": "yes/no",
  "text": "{\"leave_id\":\"LVE-4030\",\"employee\":\"ريم سامي الزهراني\",\"note\":\"عدد الأيام المطلوبة للإجازة ما يزال موضع استفسار.\",\"team_coverage_arranged\":true,\"notice_period_met\":true,\"requests_team_free_of_harassment_complaints\":true,\"leave_days\":6,\"no_union_grievance_raised_over_this_leave\":true,\"leave_days_soft_limit\":10,\"leave_balance_available\":true,\"leave_request_written_in_a_formal_tone\":false,\"medical_certificate_contested\":false,\"request_falls_in_blackout_period\":false,\"lawyer_letter_received_about_this_leave\":false}",
  "question": "Proposed action: 31\nReviewing this as an auditor, do the record's facts rule out the proposed action for the request?",
  "definitions": "Meanings:\n- 7819: have the task carried out as it was originally asked\n- 31: pump the brakes until more details show up\n- 434: bring in the authority who can settle it for the requester\n- 4: end it so the requester sees their request closed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qee073d2009",
  "kind": "choice",
  "text": "{\n    \"record\": {\n        \"leave_id\": \"LVE-3904\",\n        \"employee\": \"Aiko Keller\"\n    },\n    \"numbers\": {\n        \"leave_days_soft_limit\": 7,\n        \"leave_days\": 7\n    },\n    \"flags\": {\n        \"leave_request_written_in_a_formal_tone\": false,\n        \"medical_certificate_contested\": false,\n        \"request_falls_in_blackout_period\": false,\n        \"team_coverage_not_arranged\": false,\n        \"leave_balance_available\": true,\n        \"union_grievance_raised_over_this_leave\": false,\n        \"notice_period_met\": true,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"lawyer_letter_received_about_this_leave\": true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. postpone if team_coverage_not_arranged is true or medical_certificate_contested is true or leave_days is above leave_days_soft_limit.\n2. refuse leave if request_falls_in_blackout_period is true or lawyer_letter_received_about_this_leave is true.\n3. refer to hr if union_grievance_raised_over_this_leave is true.\nOtherwise: approve leave.\nNever counted: notice_period_met, leave_balance_available, requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- refuse leave: block this from going any further\n- approve leave: execute the requested action as nothing prevents it\n- postpone: keep it on hold for the missing document\n- refer to hr: route the request to the decision maker\nThe record is complete: nothing else applies.\n\nThe request describes a situation; which of the actions underneath handles it correctly?",
  "options": [
   "postpone",
   "refuse leave",
   "approve leave"
  ]
 },
 {
  "qid": "q996f64ed5c",
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
  "qid": "qe4350ec9b9",
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
  "qid": "qc3bf32bb55",
  "kind": "choice",
  "text": "---\n# request record\nsubject:\n  run_id: \"RUN-5128\"\n  agent: \"indigo\"\namounts:\n  steps_used_hard_limit: 20\n  steps_used: 20\nchecks:\n  last_tool_output_verified: true\n  task_description_complete: true\n  tool_output_shows_tampering: false\n  action_free_of_ethics_concerns: true\n  log_lines_written_in_a_compact_style: true\n  action_forbidden_by_security_policy: false\n  owner_sign_off_required_for_this_action: true",
  "question": "Meanings:\n- stop: refuse to act since the step is prohibited\n- human_review: send it up so the requester gets a firm decision\n- pause: hold off until more information arrives\n- continue: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "continue",
   "pause",
   "human_review"
  ]
 },
 {
  "qid": "q8a40426011",
  "kind": "choice",
  "text": "# request record\ninvoice_id                                   | INV-6070\nvendor                                       | Pinecrest Supply\nduplicate_of_paid_invoice                    | false\nvendor_tax_form_missing                      | true\namount_approval_threshold                    | 5000.00\nvendor_name_written_in_capital_letters       | false\nvendor_on_sanctions_list                     | false\ninvoice_pdf_uses_a_portrait_layout           | false\nawaiting_purchase_order                      | false\nvendor_filed_a_legal_claim_over_this_invoice | false\namount                                       | 9003.16\napprover_declared_a_conflict_of_interest     | false\npayment_requested_during_business_hours      | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 7 if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. 6240 if amount is above amount_approval_threshold.\n3. 608 if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_on_sanctions_list is true or approver_declared_a_conflict_of_interest is true.\nOtherwise: 62.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- 62: keep moving on this one nothing is holding it up\n- 6240: route this to the one who signs off\n- 7: reject this item since it violates the policy\n- 608: park the file until the requester sends the document in\nThe record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "608",
   "6240",
   "62"
  ]
 },
 {
  "qid": "q40690db764",
  "kind": "yes/no",
  "text": "# record\nleave_id: LVE-7932\nemployee: كنان ياسر الوادي\nnote: فترة الإجازة لا تتعارض مع أي مهام مجدولة للقسم.\nleave_balance_available: true\nlawyer_letter_received_about_this_leave: false\nleave_request_written_in_a_formal_tone: false\nteam_coverage_not_arranged: false\nleave_days_soft_limit: 10\nrequests_team_free_of_harassment_complaints: false\nnotice_period_not_met: false\nleave_days: 2\nno_union_grievance_raised_over_this_leave: true\nrequest_falls_in_blackout_period: false\nmedical_certificate_contested: false",
  "question": "Proposed action: send to a person\nAs an auditor, is the proposed action not the right call for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qae52c1849e",
  "kind": "choice",
  "text": "---\n# record\ninvoice_id: INV-9933\nvendor: Northwind Labs\nvendor_filed_a_legal_claim_over_this_invoice: false\npayment_requested_during_business_hours: true\nduplicate_of_paid_invoice: false\ninvoice_pdf_uses_a_portrait_layout: true\namount_approval_threshold: 500.00\nvendor_tax_form_on_file: true\napprover_free_of_conflicts_of_interest: true\nvendor_free_of_sanctions: false\namount: 283.40\nvendor_name_written_in_capital_letters: false\nawaiting_purchase_order: false",
  "question": "Meanings:\n- wait: hold up for a sec until more info comes in\n- proceed: proceed in accordance with the stated request\n- ask a human: direct the request to the responsible decider\n- cancel: block it right away\nThe record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "cancel",
   "wait",
   "proceed"
  ]
 },
 {
  "qid": "qfd786ee08f",
  "kind": "yes/no",
  "text": "# record\nleave_id=LVE-3775\nemployee=Dana Lindqvist\nno_union_grievance_raised_over_this_leave=true\nleave_days=5\nrequests_team_free_of_harassment_complaints=true\nleave_balance_exhausted=true\nnotice_period_not_met=false\nlawyer_letter_received_about_this_leave=false\nrequest_falls_in_blackout_period=false\nmedical_certificate_contested=false\nleave_days_soft_limit=5\nleave_request_written_in_a_formal_tone=false\nteam_coverage_arranged=true",
  "question": "Proposed action: 4\nWould the proposed action not be the appropriate course under the applicable procedure?",
  "definitions": "Meanings:\n- 50: reject this item since it violates the policy\n- 947: hold off until the check clears\n- 4: give it to a person who has the authority to decide\n- 3539: carry it through and the requester is satisfied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7b3e183708",
  "kind": "choice",
  "text": "# extract\nrequest_id | REQ-4995\nrequester | Hugo Imai\naccess_days_approval_threshold | 45\nbusiness_justification_missing | false\nrequester_barred_from_this_system | false\naccess_days | 46\naccount_suspended | false\nmfa_enrollment_incomplete | false\nrequested_role_forbidden_by_policy | false\nrequest_free_of_ethics_office_flags | true\nrequest_text_written_in_capital_letters | true\nrequest_grants_admin_rights | false\nlegal_preservation_order_on_the_account | false",
  "question": "Meanings:\n- cancel: kill this one off, it is off the table for good\n- proceed: keep moving on this one nothing is holding it up\n- ask a human: forward it to the decision maker\n- wait: hold this until a check comes back\nThe record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "proceed",
   "wait",
   "ask a human"
  ]
 },
 {
  "qid": "q7bde7b4cea",
  "kind": "choice",
  "text": "{\n  \"request\":{\n    \"ticket_id\":\"TCK-1668\",\n    \"customer\":\"Jonas Petrov\"\n  },\n  \"figures\":{\n    \"claim_amount_hard_limit\":1000.00,\n    \"claim_amount\":117.93\n  },\n  \"checks\":{\n    \"claim_involves_a_media_inquiry\":false,\n    \"legal_complaint_filed\":false,\n    \"claim_free_of_ombudsman_cases\":true,\n    \"proof_of_purchase_missing\":false,\n    \"customer_message_is_short\":true,\n    \"item_excluded_by_policy\":false,\n    \"customer_message_written_in_a_casual_tone\":false,\n    \"harmless_greeting_present_in_the_message\":true,\n    \"claim_form_filled_in_with_the_usual_font\":true,\n    \"item_return_not_yet_received\":false,\n    \"free_of_safety_incident_reports\":true\n  }\n}",
  "question": "Meanings:\n- 7950: shelve the matter until more details come in\n- 78: shut off this process completely\n- 189: forward the case to the designated decision maker\n- 9: go on and finish it the path is clear\nThe record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "189",
   "7950",
   "9"
  ]
 },
 {
  "qid": "qd6aba2e010",
  "kind": "yes/no",
  "text": "# request record\ninvoice_id = INV-2341\nvendor = Riverbend Supply\ninvoice_pdf_uses_a_portrait_layout = false\namount_approval_threshold = 500.00\nvendor_tax_form_missing = true\nvendor_filed_a_legal_claim_over_this_invoice = false\nduplicate_of_paid_invoice = false\namount = 229.85\napprover_free_of_conflicts_of_interest = true\nvendor_free_of_sanctions = true\nvendor_name_written_in_capital_letters = false\npayment_requested_during_business_hours = true\npurchase_order_received = true",
  "question": "Proposed action: approve\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. ask a human if amount is above amount_approval_threshold.\n3. delay if purchase_order_received is false or vendor_tax_form_missing is true or vendor_free_of_sanctions is false or approver_free_of_conflicts_of_interest is false.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- delay: hold all progress until the requisite documentation arrives\n- ask a human: delegate the call to whoever holds authority\n- refuse: drop this right there, we are not touching it\n- approve: continue as requested with the path fully open\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q963940cecb",
  "kind": "yes/no",
  "text": "invoice_id=INV-3268\nvendor=Bluepeak Supply\nvendor_name_written_in_capital_letters=false\nduplicate_of_paid_invoice=true\nvendor_tax_form_on_file=true\nvendor_filed_a_legal_claim_over_this_invoice=false\nvendor_on_sanctions_list=false\npayment_requested_during_business_hours=true\namount_approval_threshold=10000.00\napprover_declared_a_conflict_of_interest=false\ninvoice_pdf_uses_a_portrait_layout=true\namount=7567.77\npurchase_order_received=true",
  "question": "Proposed action: deny\nIs the proposed action the right call, judging from what the record shows?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qfd93d6a8bc",
  "kind": "yes/no",
  "text": "# record\nleave_id: LVE-3295\nemployee: Ingrid Imai\nrequest_falls_in_blackout_period: true\nleave_days_soft_limit: 10\nrequests_team_free_of_harassment_complaints: true\nmedical_certificate_contested: false\nno_union_grievance_raised_over_this_leave: true\nleave_days: 6\nleave_request_written_in_a_formal_tone: false\nleave_balance_exhausted: true\nlawyer_letter_received_about_this_leave: false\nteam_coverage_arranged: true\nnotice_period_met: true",
  "question": "Proposed action: defer\nIs the proposed action not the best thing to do with this?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_met is false or team_coverage_arranged is false or leave_balance_exhausted is true or lawyer_letter_received_about_this_leave is true or leave_days is above leave_days_soft_limit.\n2. deny if request_falls_in_blackout_period is true.\n3. ask_manager if medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false.\nOtherwise: approve.\nNever counted: no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qda4bb74c00",
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
  "qid": "qa67eb8c1b3",
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
  "qid": "q8e3c307f82",
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
  "qid": "qe8b7da137a",
  "kind": "yes/no",
  "text": "leave_id: LVE-7827\nemployee: Nadia Mensah\nleave_request_written_in_a_formal_tone: false\nleave_days: 13\nrequests_team_free_of_harassment_complaints: true\nrequest_falls_in_blackout_period: false\nmedical_certificate_contested: false\nunion_grievance_raised_over_this_leave: false\nlawyer_letter_received_about_this_leave: false\nnotice_period_not_met: false\nleave_days_soft_limit: 14\nleave_balance_exhausted: true\nteam_coverage_arranged: true",
  "question": "Proposed action: CCV\nWould what the record shows make the proposed action the right call here?",
  "definitions": "Meanings:\n- MM: pause and collect more information first\n- RKDZ: escalate this to someone senior who decides\n- CCV: stop the request so the requester gets nothing from it\n- R: proceed with the request since the way is clear and nothing blocks it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q051bf866e1",
  "kind": "yes/no",
  "text": "---\n# request record\nrequest_id: \"REQ-8744\"\nrequester: \"Nadia Imai\"\nrequester_not_barred_from_this_system: true\nlegal_preservation_order_on_the_account: true\nbusiness_justification_missing: false\nrequest_free_of_ethics_office_flags: true\naccess_days: 12\naccount_suspended: false\nrequest_grants_admin_rights: false\nrequest_text_written_in_capital_letters: true\naccess_days_approval_threshold: 60\nmfa_enrollment_complete: true\nrequested_role_forbidden_by_policy: false",
  "question": "Proposed action: 9605\nShould the proposed action be taken for this request?",
  "definitions": "Meanings:\n- 9605: forward the matter as the call rests with someone higher\n- 3: hold the request until the check is done\n- 645: leave the requester without the result they asked for\n- 11: press on with the work as originally set\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qea288544b5",
  "kind": "yes/no",
  "text": "ticket_id=TCK-7826\ncustomer=Zoe Moreau\nfree_of_legal_complaints=true\nharmless_greeting_present_in_the_message=true\nclaim_form_filled_in_with_the_usual_font=true\nclaim_amount=156.29\ncustomer_message_is_short=true\nproof_of_purchase_attached=true\nfree_of_safety_incident_reports=false\nclaim_free_of_ombudsman_cases=true\nclaim_involves_a_media_inquiry=false\nitem_excluded_by_policy=false\ncustomer_message_written_in_a_formal_tone=false\nitem_return_received=true\nclaim_amount_hard_limit=200.00",
  "question": "Proposed action: cancel\nIs the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. wait if proof_of_purchase_attached is false or claim_involves_a_media_inquiry is true.\n3. ask a human if item_return_received is false or free_of_legal_complaints is false or free_of_safety_incident_reports is false.\nOtherwise: proceed.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q300dd93480",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"leave_id\": \"LVE-8049\",\n        \"employee\": \"Anders Novak\"\n    },\n    \"metrics\": {\n        \"leave_days_soft_limit\": 7,\n        \"leave_days\": 2\n    },\n    \"signals\": {\n        \"union_grievance_raised_over_this_leave\": true,\n        \"team_coverage_arranged\": true,\n        \"leave_balance_available\": true,\n        \"leave_request_written_in_a_formal_tone\": true,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"notice_period_met\": true,\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"request_falls_in_blackout_period\": false\n    }\n}",
  "question": "Proposed action: turn_down\nIs it not correct that the proposed action is not off base, judging by the record on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if notice_period_met is false or team_coverage_arranged is false or leave_balance_available is false or lawyer_letter_received_about_this_leave is true or leave_days is above leave_days_soft_limit.\n2. turn_down if request_falls_in_blackout_period is true.\n3. send_to_a_person if medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false.\nOtherwise: go_ahead.\nNever counted: union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qdcb124201f",
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
  "qid": "q1f2b30dafa",
  "kind": "yes/no",
  "text": "run_id=RUN-6657\nagent=delta\ntool_output_shows_tampering=false\nsteps_used=12\nlog_lines_written_in_a_verbose_style=false\ntask_description_incomplete=false\nsteps_used_hard_limit=12\nowner_sign_off_required_for_this_action=false\naction_permitted_by_security_policy=true\naction_free_of_ethics_concerns=true\nlast_tool_output_verified=true",
  "question": "Proposed action: go ahead\nWould the proposed action not be the appropriate course under the applicable procedure?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put on hold if last_tool_output_verified is false or task_description_incomplete is true.\n3. turn down if action_permitted_by_security_policy is false or owner_sign_off_required_for_this_action is true or steps_used is above steps_used_hard_limit.\nOtherwise: go ahead.\nNever counted: log_lines_written_in_a_verbose_style.\nMeanings:\n- send to a person: send this on to whoever decides\n- go ahead: proceed as asked since everything is cleared\n- turn down: refuse to act since the step is prohibited\n- put on hold: suspend action until the facts are confirmed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q51053b1519",
  "kind": "yes/no",
  "text": "{\n    \"deploy_id\": \"DEP-1900\",\n    \"service\": \"auth_proxy\",\n    \"backout_plan_missing\": false,\n    \"deploy_blocked_by_security_policy\": false,\n    \"service_free_of_major_incidents\": true,\n    \"contract_customer_asked_for_a_say_in_this_rollout\": false,\n    \"files_changed_soft_limit\": 20,\n    \"deploy_title_written_in_normal_case\": true,\n    \"canary_results_complete\": true,\n    \"deploy_prohibited_during_the_audit_window\": false,\n    \"commit_messages_written_in_a_detailed_style\": true,\n    \"deploy_has_a_long_description\": true,\n    \"rollout_approval_revoked\": false,\n    \"commit_messages_written_in_a_casual_tone\": true,\n    \"files_changed\": 5\n}",
  "question": "Proposed action: 5256\nIs it not true that the proposed action is not out of line with the ask?",
  "definitions": "Meanings:\n- 51: hold the request so the requester waits for their check\n- 1: shut this down fast\n- 5256: commence the action as specified without impediment\n- 692: give it to the person in charge of the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4efb128553",
  "kind": "yes/no",
  "text": "---\nticket_id: TCK-3590\ncustomer: دلال ماهر الكيلاني\nnote: لا يوجد أي خلاف في تاريخ الشراء أو المبلغ.\nclaim_form_filled_in_with_the_usual_font: true\nclaim_involves_a_media_inquiry: false\ncustomer_message_written_in_a_formal_tone: false\nitem_excluded_by_policy: false\nclaim_amount_hard_limit: 100.00\ncustomer_message_is_short: false\nclaim_free_of_ombudsman_cases: true\nproof_of_purchase_attached: true\nfree_of_legal_complaints: true\nclaim_amount: 12.15\nharmless_greeting_present_in_the_message: true\nitem_return_received: true\nfree_of_safety_incident_reports: true",
  "question": "Proposed action: 6302\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Meanings:\n- 6302: stall the request until the check comes back\n- 94: forward the matter as the call rests with someone higher\n- 5: be stopped and never carried out\n- 214: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9eb9a9b1bc",
  "kind": "choice",
  "text": "---\n# record\nrecord:\n  run_id: RUN-2030\n  agent: delta\nnumbers:\n  steps_used_hard_limit: 8\n  steps_used: 3\nflags:\n  tool_output_shows_tampering: false\n  task_description_incomplete: false\n  action_free_of_ethics_concerns: true\n  action_forbidden_by_security_policy: false\n  log_lines_written_in_a_verbose_style: false\n  last_tool_output_verified: false\n  owner_sign_off_required_for_this_action: false",
  "question": "Meanings:\n- 32: cease the operation as it is prohibited\n- 2492: run with this one\n- 306: keep waiting for the missing details\n- 6: hand the matter to a decider so the requester gets a verdict\nThe record is complete: nothing else applies.\n\nWhich of the actions below does the record point to as the right call?",
  "options": [
   "2492",
   "6",
   "306"
  ]
 },
 {
  "qid": "q9f2f59b326",
  "kind": "yes/no",
  "text": "request_id=REQ-6525\nrequester=Jonas Hadjiev\nmfa_enrollment_complete=true\naccount_suspended=false\nrequested_role_forbidden_by_policy=false\nrequest_grants_admin_rights=true\nlegal_preservation_order_on_the_account=false\naccess_days=30\nbusiness_justification_provided=true\nrequester_not_barred_from_this_system=true\nrequest_text_written_in_capital_letters=false\naccess_days_approval_threshold=30\nrequest_free_of_ethics_office_flags=true",
  "question": "Proposed action: approve\nIs the proposed action the sensible thing to do for the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if mfa_enrollment_complete is false or requester_not_barred_from_this_system is false or request_free_of_ethics_office_flags is false.\n2. deny if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. ask manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: approve.\nNever counted: business_justification_provided, request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2143c11d71",
  "kind": "choice",
  "text": "ticket_id | TCK-5483\ncustomer | Nadia Haddad\nclaim_amount_hard_limit | 50.00\nclaim_form_filled_in_with_the_usual_font | true\nclaim_amount | 50.00\nitem_excluded_by_policy | true\ncustomer_message_written_in_a_casual_tone | true\ncustomer_message_is_short | true\nlegal_complaint_filed | false\nclaim_involves_a_media_inquiry | false\nitem_return_received | true\nproof_of_purchase_missing | false\nharmless_greeting_present_in_the_message | true\nclaim_free_of_ombudsman_cases | true\nfree_of_safety_incident_reports | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if claim_amount is above claim_amount_hard_limit.\n2. ask a human if item_return_received is false or item_excluded_by_policy is true or legal_complaint_filed is true or free_of_safety_incident_reports is false or claim_involves_a_media_inquiry is true.\n3. delay if proof_of_purchase_missing is true or claim_free_of_ombudsman_cases is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nGiven what the requester needs, which of the actions below should be taken?",
  "options": [
   "refuse",
   "ask a human",
   "delay"
  ]
 },
 {
  "qid": "qcd425705df",
  "kind": "choice",
  "text": "{\n  \"meta\": {\n    \"leave_id\": \"LVE-6398\",\n    \"employee\": \"Felix Calloway\"\n  },\n  \"metrics\": {\n    \"leave_days_soft_limit\": 14,\n    \"leave_days\": 7\n  },\n  \"signals\": {\n    \"leave_balance_exhausted\": false,\n    \"medical_certificate_contested\": false,\n    \"notice_period_not_met\": false,\n    \"request_falls_in_blackout_period\": false,\n    \"team_coverage_not_arranged\": false,\n    \"leave_request_written_in_a_formal_tone\": true,\n    \"union_grievance_raised_over_this_leave\": false,\n    \"requests_team_free_of_harassment_complaints\": true,\n    \"lawyer_letter_received_about_this_leave\": false\n  }\n}",
  "question": "Meanings:\n- XPGF: halt the request at this point\n- HSF: pass the request to a decider\n- QT: finish what was asked as stated, the way ahead is fully free\n- T: suspend progress until verification is received\nThe record is complete: nothing else applies.\n\nChecklist item: which of the actions listed below is the right call for the request?",
  "options": [
   "QT",
   "T",
   "HSF"
  ]
 },
 {
  "qid": "q0a18fb0d64",
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
  "qid": "q63ee12b737",
  "kind": "yes/no",
  "text": "# case\ninvoice_id = INV-5508\nvendor = Northwind Works\nvendor_name_written_in_capital_letters = false\nvendor_on_sanctions_list = false\nvendor_tax_form_missing = true\namount = 1401.16\npayment_requested_during_business_hours = true\namount_approval_threshold = 10000.00\nduplicate_of_paid_invoice = false\nawaiting_purchase_order = false\nvendor_filed_a_legal_claim_over_this_invoice = false\ninvoice_pdf_uses_a_portrait_layout = true\napprover_declared_a_conflict_of_interest = false",
  "question": "Proposed action: BQHL\nIs it not true that the proposed action sits in the record and is not a mismatch?",
  "definitions": "Meanings:\n- RW: shut off this process completely\n- T: proceed and the requester gets what they asked\n- SXN: submit it upward to the approver\n- BQHL: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qacf0e539c5",
  "kind": "yes/no",
  "text": "# case\nleave_id                                    | LVE-8686\nemployee                                    | Jonas Rossi\nno_union_grievance_raised_over_this_leave   | true\nleave_days_soft_limit                       | 21\nrequest_falls_in_blackout_period            | false\nteam_coverage_arranged                      | false\nnotice_period_met                           | true\nrequests_team_free_of_harassment_complaints | true\nleave_request_written_in_a_formal_tone      | false\nlawyer_letter_received_about_this_leave     | false\nmedical_certificate_contested               | true\nleave_balance_exhausted                     | false\nleave_days                                  | 20",
  "question": "Proposed action: go ahead\nHas the audit trail in the record ruled out the proposed action as a sound call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if notice_period_met is false or team_coverage_arranged is false or leave_days is above leave_days_soft_limit.\n2. turn down if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. send to a person if leave_balance_exhausted is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: go ahead.\nNever counted: leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q141c3ef9c7",
  "kind": "yes/no",
  "text": "ticket_id: TCK-5463\ncustomer: Nadia Petrov\nclaim_amount: 361.77\nclaim_amount_hard_limit: 1000.00\nfree_of_safety_incident_reports: true\ncustomer_message_written_in_a_formal_tone: false\nitem_return_not_yet_received: false\nitem_excluded_by_policy: true\nharmless_greeting_present_in_the_message: true\nclaim_free_of_ombudsman_cases: true\nfree_of_legal_complaints: true\nclaim_involves_a_media_inquiry: false\nclaim_form_filled_in_with_the_usual_font: true\ncustomer_message_is_short: true\nproof_of_purchase_attached: true",
  "question": "Proposed action: cancel\nWould the proposed action be the right move for the request in the record?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q0a522d23ec",
  "kind": "yes/no",
  "text": "# extract\ndeploy_id                                         | DEP-6606\nservice                                           | auth_proxy\nbackout_plan_documented                           | true\ndeploy_prohibited_during_the_audit_window         | false\nfiles_changed_soft_limit                          | 20\ndeploy_blocked_by_security_policy                 | false\ncanary_results_incomplete                         | false\nservice_free_of_major_incidents                   | false\ncommit_messages_written_in_a_casual_tone          | true\ndeploy_has_a_long_description                     | false\ndeploy_title_written_in_normal_case               | true\nrollout_approval_revoked                          | false\nfiles_changed                                     | 21\ncontract_customer_asked_for_a_say_in_this_rollout | false\ncommit_messages_written_in_a_detailed_style       | true",
  "question": "Proposed action: turn down\nHas the record ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_documented is false or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- go ahead: keep going exactly as requested because every obstacle has cleared\n- put on hold: hold off until more information arrives\n- send to a person: be passed along to whoever makes the call\n- turn down: stop the request so the requester gets nothing from it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa01e99cd53",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n* leave id: LVE-5561\n* employee: Marta Imai\n* no union grievance raised over this leave: no\n* leave days: 1\n* team coverage not arranged: no\n* requests team free of harassment complaints: yes\n* leave request written in a formal tone: no\n* notice period not met: yes\n* leave balance exhausted: no\n* leave days soft limit: 10\n* lawyer letter received about this leave: no\n* medical certificate contested: no\n* request falls in blackout period: no",
  "question": "Proposed action: 1\nWould the proposed action be considered the correct disposition of the request in the record?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 5654 if notice_period_not_met is true or team_coverage_not_arranged is true or leave_days is above leave_days_soft_limit.\n2. 1 if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. 44 if leave_balance_exhausted is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: 580.\nNever counted: leave_request_written_in_a_formal_tone.\nMeanings:\n- 5654: keep it on hold for the missing document\n- 1: stop this course of action at once\n- 580: have the plan kept moving as it was requested\n- 44: pass this along to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb9af0b2c0d",
  "kind": "yes/no",
  "text": "{\n    \"case\":{\n        \"leave_id\":\"LVE-4570\",\n        \"employee\":\"بلال أسامة القرشي\",\n        \"note\":\"الموظف قدم جميع المستندات المطلوبة وهي صحيحة.\"\n    },\n    \"values\":{\n        \"leave_days_soft_limit\":14,\n        \"leave_days\":9\n    },\n    \"tests\":{\n        \"lawyer_letter_received_about_this_leave\":true,\n        \"requests_team_free_of_harassment_complaints\":true,\n        \"medical_certificate_contested\":false,\n        \"request_falls_in_blackout_period\":true,\n        \"team_coverage_arranged\":true,\n        \"leave_balance_available\":true,\n        \"notice_period_not_met\":true,\n        \"leave_request_written_in_a_formal_tone\":false,\n        \"no_union_grievance_raised_over_this_leave\":true\n    }\n}",
  "question": "Proposed action: 47\nWeighed against the request in the record, does the proposed action look like the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 125 if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. 7126 if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. 47 if leave_balance_available is false.\nOtherwise: 5.\nNever counted: notice_period_not_met, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nMeanings:\n- 7126: chill until the document turns up\n- 5: continue so the requester receives the result\n- 47: be blocked outright so it never gets carried out\n- 125: be routed to whoever holds the decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q603538143e",
  "kind": "yes/no",
  "text": "# record\nleave_id: LVE-6086\nemployee: Leila Tanaka\nrequest_falls_in_blackout_period: true\nleave_days: 2\nno_union_grievance_raised_over_this_leave: true\nrequests_team_free_of_harassment_complaints: true\nlawyer_letter_received_about_this_leave: false\nleave_days_soft_limit: 7\nleave_request_written_in_a_formal_tone: false\nnotice_period_not_met: false\nteam_coverage_arranged: true\nleave_balance_exhausted: true\nmedical_certificate_contested: false",
  "question": "Proposed action: ask a human\nIs the proposed action the right step for the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. delay if notice_period_not_met is true or team_coverage_arranged is false.\n3. refuse if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\nOtherwise: approve.\nNever counted: leave_balance_exhausted, medical_certificate_contested, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2ebade4592",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n* deploy id: DEP-6172\n* service: pricing\n* commit messages written in a casual tone: yes\n* deploy prohibited during the audit window: no\n* deploy blocked by security policy: no\n* canary results incomplete: no\n* commit messages written in a terse style: no\n* files changed: 80\n* files changed soft limit: 80\n* contract customer asked for a say in this rollout: yes\n* deploy has a long description: no\n* backout plan missing: no\n* service free of major incidents: yes\n* deploy title written in normal case: yes\n* rollout approval revoked: no",
  "question": "Proposed action: KBK\nIs the proposed action the suitable determination for the request in the record?",
  "definitions": "Meanings:\n- RR: be turned away and treated as off limits\n- KBK: transfer the case to the responsible decision maker for determination\n- B: wait until a document arrives before you move forward with it\n- TFQL: run the requested step through\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3c62e2a957",
  "kind": "choice",
  "text": "{\n    \"meta\": {\n        \"ticket_id\": \"TCK-6787\",\n        \"customer\": \"Kofi Okonkwo\"\n    },\n    \"metrics\": {\n        \"claim_amount_hard_limit\": 50.00,\n        \"claim_amount\": 30.90\n    },\n    \"signals\": {\n        \"legal_complaint_filed\": false,\n        \"claim_free_of_ombudsman_cases\": true,\n        \"item_excluded_by_policy\": false,\n        \"free_of_safety_incident_reports\": true,\n        \"claim_involves_a_media_inquiry\": false,\n        \"customer_message_written_in_a_casual_tone\": true,\n        \"harmless_greeting_present_in_the_message\": true,\n        \"customer_message_is_short\": true,\n        \"claim_form_filled_in_with_the_usual_font\": true,\n        \"item_return_received\": true,\n        \"proof_of_purchase_attached\": true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if free_of_safety_incident_reports is false or claim_free_of_ombudsman_cases is false.\n2. turn down if proof_of_purchase_attached is false or item_excluded_by_policy is true or claim_involves_a_media_inquiry is true or claim_amount is above claim_amount_hard_limit.\n3. put on hold if item_return_received is false.\nOtherwise: go ahead.\nNever counted: legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nAmong the actions listed after this, which best matches the request?",
  "options": [
   "turn down",
   "send to a person",
   "go ahead"
  ]
 }
]
