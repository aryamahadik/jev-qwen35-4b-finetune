# G5-H blind read T46-blind_read-bc9e16d1-003 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8a/T46/qc/g5h/answers/T46-blind_read-bc9e16d1-003.json

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
  "qid": "q2d3f05c49f",
  "kind": "choice",
  "text": "# record\nrequest_id | REQ-7165\nrequester | Ravi Mensah\nrequester_not_barred_from_this_system | true\naccess_days_approval_threshold | 30\nbusiness_justification_missing | false\nrequested_role_forbidden_by_policy | false\nrequest_grants_admin_rights | true\naccess_days | 30\nlegal_preservation_order_on_the_account | false\nmfa_enrollment_complete | true\nrequest_free_of_ethics_office_flags | true\naccount_suspended | false\nrequest_text_written_in_capital_letters | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 1664 if mfa_enrollment_complete is false or requester_not_barred_from_this_system is false or request_free_of_ethics_office_flags is false.\n2. 53 if account_suspended is true or requested_role_forbidden_by_policy is true.\n3. 8 if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: 445.\nNever counted: business_justification_missing, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- 53: make sure the requester never gets what they wanted\n- 445: complete the job as it was assigned\n- 8: give it to a person who has the authority to decide\n- 1664: hold the request until a check is completed\nThe record is complete: nothing else applies.\n\nConsidering what was asked and the facts available, which action below should be chosen?",
  "options": [
   "1664",
   "53",
   "445"
  ]
 },
 {
  "qid": "q74344d86b4",
  "kind": "choice",
  "text": "{\n    \"record\":{\n        \"ticket_id\":\"TCK-8691\",\n        \"customer\":\"Priya Adeyemi\"\n    },\n    \"numbers\":{\n        \"claim_amount_hard_limit\":100.00,\n        \"claim_amount\":68.67\n    },\n    \"flags\":{\n        \"free_of_safety_incident_reports\":true,\n        \"harmless_greeting_present_in_the_message\":true,\n        \"item_return_not_yet_received\":false,\n        \"claim_free_of_ombudsman_cases\":true,\n        \"claim_form_filled_in_with_the_usual_font\":true,\n        \"customer_message_is_short\":false,\n        \"proof_of_purchase_missing\":false,\n        \"free_of_legal_complaints\":true,\n        \"claim_involves_a_media_inquiry\":false,\n        \"customer_message_written_in_a_casual_tone\":true,\n        \"item_excluded_by_policy\":false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if claim_amount is above claim_amount_hard_limit.\n2. ask_a_human if item_return_not_yet_received is true or item_excluded_by_policy is true or free_of_legal_complaints is false or free_of_safety_incident_reports is false or claim_involves_a_media_inquiry is true.\n3. wait if proof_of_purchase_missing is true or claim_free_of_ombudsman_cases is false.\nOtherwise: proceed.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed fits the case described in this file best?",
  "options": [
   "proceed",
   "cancel",
   "wait"
  ]
 },
 {
  "qid": "q377cd738c8",
  "kind": "yes/no",
  "text": "{\n  \"ticket_id\":\"TCK-8857\",\n  \"customer\":\"Anders Haddad\",\n  \"legal_complaint_filed\":true,\n  \"item_excluded_by_policy\":false,\n  \"customer_message_written_in_a_casual_tone\":true,\n  \"item_return_received\":true,\n  \"claim_involves_a_media_inquiry\":false,\n  \"harmless_greeting_present_in_the_message\":true,\n  \"free_of_safety_incident_reports\":true,\n  \"claim_form_filled_in_with_the_usual_font\":true,\n  \"customer_message_is_short\":false,\n  \"claim_amount\":27.17,\n  \"claim_amount_hard_limit\":100.00,\n  \"proof_of_purchase_missing\":true,\n  \"claim_free_of_ombudsman_cases\":true\n}",
  "question": "Proposed action: turn down\nMeasured against the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. turn down if item_excluded_by_policy is true or legal_complaint_filed is true or claim_amount is above claim_amount_hard_limit.\n3. send to a person if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: go ahead.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q05e4a075a2",
  "kind": "yes/no",
  "text": "---\n# record\nmeta:\n    invoice_id: \"INV-2735\"\n    vendor: \"Riverbend Works\"\nmetrics:\n    amount_approval_threshold: 5000.00\n    amount: 1450.97\nsignals:\n    vendor_filed_a_legal_claim_over_this_invoice: false\n    vendor_on_sanctions_list: false\n    purchase_order_received: true\n    invoice_pdf_uses_a_portrait_layout: true\n    duplicate_of_paid_invoice: true\n    vendor_tax_form_missing: false\n    payment_requested_during_business_hours: true\n    approver_declared_a_conflict_of_interest: false\n    vendor_name_written_in_capital_letters: false",
  "question": "Proposed action: turn_down\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Meanings:\n- go_ahead: keep going with it\n- turn_down: shut this down right away, we are staying clear of it\n- put_on_hold: hold this until a check comes back\n- send_to_a_person: transfer it to the person with authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qae42d4bf92",
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
  "qid": "qae58fe7eac",
  "kind": "choice",
  "text": "{\n    \"record\": {\n        \"request_id\": \"REQ-7123\",\n        \"requester\": \"Marta Sorensen\"\n    },\n    \"numbers\": {\n        \"access_days_approval_threshold\": 90,\n        \"access_days\": 36\n    },\n    \"flags\": {\n        \"request_text_written_in_capital_letters\": true,\n        \"mfa_enrollment_complete\": true,\n        \"request_grants_admin_rights\": false,\n        \"legal_preservation_order_on_the_account\": false,\n        \"requester_barred_from_this_system\": false,\n        \"request_free_of_ethics_office_flags\": true,\n        \"account_suspended\": false,\n        \"requested_role_forbidden_by_policy\": false,\n        \"business_justification_missing\": false\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nWhich of these actions should we take for this request?",
  "options": [
   "delay",
   "ask a human",
   "approve"
  ]
 },
 {
  "qid": "q415f4d88cf",
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
  "qid": "q1989888f00",
  "kind": "choice",
  "text": "ticket_id=TCK-8737\ncustomer=Jonas Rossi\nharmless_greeting_present_in_the_message=true\nclaim_amount=100.00\nclaim_free_of_ombudsman_cases=true\nfree_of_safety_incident_reports=true\nclaim_form_filled_in_with_the_usual_font=true\nfree_of_legal_complaints=true\nitem_return_not_yet_received=false\ncustomer_message_written_in_a_casual_tone=false\nproof_of_purchase_missing=true\nclaim_amount_hard_limit=100.00\ncustomer_message_is_short=true\nitem_excluded_by_policy=false\nclaim_involves_a_media_inquiry=false",
  "question": "Meanings:\n- 4652: forward the matter as the call rests with someone higher\n- 4: hold the request until the check is done\n- 73: keep going with it nothing is blocking you\n- 147: shut this down right away, we are staying clear of it\nThe record is complete: nothing else applies.\n\nFrom the requester's side, which of the actions listed below is the right call for this request?",
  "options": [
   "4",
   "147",
   "73"
  ]
 },
 {
  "qid": "q8be5962a4b",
  "kind": "choice",
  "text": "# case\ndeploy_id: DEP-9297\nservice: gateway\nservice_free_of_major_incidents: true\ndeploy_title_written_in_normal_case: true\nrollout_approval_revoked: false\ncanary_results_incomplete: false\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_prohibited_during_the_audit_window: false\ncommit_messages_written_in_a_detailed_style: true\ndeploy_blocked_by_security_policy: true\nfiles_changed_soft_limit: 15\nbackout_plan_documented: true\nfiles_changed: 15\ndeploy_has_a_long_description: false\ncommit_messages_written_in_a_casual_tone: true",
  "question": "The record is complete: nothing else applies.\n\nReading the file for this case, which listed action is the best call?",
  "options": [
   "put on hold",
   "go ahead",
   "turn down"
  ]
 },
 {
  "qid": "qc33cc336ad",
  "kind": "yes/no",
  "text": "leave_id: LVE-3042\nemployee: ريما فايز الزبيدي\nnote: طلب الإجازة مقدم في الموعد المحدد بالسياسة.\nleave_days_soft_limit: 10\nleave_request_written_in_a_formal_tone: false\nleave_balance_available: false\nmedical_certificate_contested: false\nno_union_grievance_raised_over_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nleave_days: 4\nteam_coverage_arranged: true\nrequest_falls_in_blackout_period: true\nnotice_period_met: false\nlawyer_letter_received_about_this_leave: false",
  "question": "Proposed action: delay\nDo the request and its facts together make the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. delay if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. refuse if leave_balance_available is false.\nOtherwise: approve.\nNever counted: notice_period_met, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcfa0183396",
  "kind": "yes/no",
  "text": "{\"leave_id\": \"LVE-6939\", \"employee\": \"Paolo Anand\", \"leave_days\": 1, \"leave_days_soft_limit\": 3, \"request_falls_in_blackout_period\": false, \"notice_period_met\": true, \"team_coverage_arranged\": true, \"leave_balance_available\": true, \"requests_team_free_of_harassment_complaints\": true, \"lawyer_letter_received_about_this_leave\": false, \"leave_request_written_in_a_formal_tone\": false, \"union_grievance_raised_over_this_leave\": false, \"medical_certificate_contested\": false}",
  "question": "Proposed action: wait\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qeb5a70342e",
  "kind": "choice",
  "text": "---\nrequest:\n  ticket_id: TCK-3365\n  customer: دينا وائل الأنصاري\n  note: الحالة بسيطة ومكتملة ولا تحتاج إلى تدخل إضافي.\nfigures:\n  claim_amount: 35.26\n  claim_amount_hard_limit: 50.00\nchecks:\n  legal_complaint_filed: true\n  claim_involves_a_media_inquiry: false\n  free_of_safety_incident_reports: false\n  customer_message_is_short: true\n  claim_form_filled_in_with_the_usual_font: true\n  item_return_received: true\n  harmless_greeting_present_in_the_message: true\n  proof_of_purchase_attached: true\n  item_excluded_by_policy: false\n  customer_message_written_in_a_formal_tone: false\n  claim_free_of_ombudsman_cases: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. wait if proof_of_purchase_attached is false or claim_amount is at least claim_amount_hard_limit.\n3. cancel if item_excluded_by_policy is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\nOtherwise: proceed.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "wait",
   "cancel",
   "proceed"
  ]
 },
 {
  "qid": "q6f021880ef",
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
  "qid": "q459f24f81e",
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
  "qid": "qbb169c4f47",
  "kind": "yes/no",
  "text": "{\"request_id\":\"REQ-4861\",\"requester\":\"Anders Okafor\",\"requested_role_forbidden_by_policy\":true,\"access_days\":30,\"ethics_office_flagged_the_request\":false,\"legal_preservation_order_on_the_account\":false,\"request_text_written_in_capital_letters\":false,\"request_grants_admin_rights\":false,\"business_justification_provided\":true,\"requester_barred_from_this_system\":false,\"access_days_approval_threshold\":30,\"mfa_enrollment_complete\":true,\"account_suspended\":false}",
  "question": "Proposed action: refer_to_owner\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer_to_owner if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. pend if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_complete is false or account_suspended is true.\nOtherwise: grant.\nNever counted: business_justification_provided, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qca4407cff4",
  "kind": "yes/no",
  "text": "# case\nticket_id: TCK-6213\ncustomer: Anders Lindqvist\nclaim_form_filled_in_with_the_usual_font: true\nitem_excluded_by_policy: false\nclaim_amount: 1000.00\nfree_of_safety_incident_reports: true\ncustomer_message_is_short: true\nfree_of_legal_complaints: true\nitem_return_not_yet_received: false\nclaim_involves_a_media_inquiry: false\nclaim_amount_hard_limit: 1000.00\nharmless_greeting_present_in_the_message: false\nproof_of_purchase_missing: true\nclaim_free_of_ombudsman_cases: true\ncustomer_message_written_in_a_casual_tone: true",
  "question": "Proposed action: ask manager\nIs it not correct that the evidence points toward the proposed action, and it is not a poor choice?",
  "definitions": "Meanings:\n- deny: end this here and now\n- approve: keep going exactly as requested because every obstacle has cleared\n- defer: hold up for a sec until more info comes in\n- ask manager: route this matter to the individual empowered to decide\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf8745cd233",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- run id: RUN-3866\n- agent: helix\n- steps used hard limit: 60\n- owner sign off required for this action: no\n- log lines written in a compact style: yes\n- action free of ethics concerns: yes\n- task description complete: no\n- action forbidden by security policy: no\n- last tool output verified: no\n- tool output shows tampering: no\n- steps used: 36",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put_on_hold if task_description_complete is false or steps_used is above steps_used_hard_limit.\n3. send_to_a_person if action_forbidden_by_security_policy is true or owner_sign_off_required_for_this_action is true.\nOtherwise: go_ahead.\nNever counted: last_tool_output_verified, log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies.\n\nWhich of the actions below is the right decision for this request?",
  "options": [
   "turn_down",
   "put_on_hold",
   "go_ahead"
  ]
 },
 {
  "qid": "q6f63f6856b",
  "kind": "choice",
  "text": "{\n  \"leave_id\": \"LVE-5160\",\n  \"employee\": \"Ravi Imai\",\n  \"leave_balance_exhausted\": false,\n  \"team_coverage_not_arranged\": false,\n  \"leave_days_soft_limit\": 7,\n  \"notice_period_met\": true,\n  \"request_falls_in_blackout_period\": false,\n  \"lawyer_letter_received_about_this_leave\": false,\n  \"requests_team_free_of_harassment_complaints\": true,\n  \"leave_days\": 7,\n  \"medical_certificate_contested\": false,\n  \"leave_request_written_in_a_formal_tone\": false,\n  \"no_union_grievance_raised_over_this_leave\": false\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if notice_period_met is false or request_falls_in_blackout_period is true.\n2. delay if team_coverage_not_arranged is true or leave_balance_exhausted is true or leave_days is above leave_days_soft_limit.\n3. ask a human if medical_certificate_contested is true or no_union_grievance_raised_over_this_leave is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nFrom the choices below, which action makes the most sense here?",
  "options": [
   "approve",
   "ask a human",
   "delay"
  ]
 },
 {
  "qid": "qf9b9d84b5f",
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
  "qid": "qd6fbb0d292",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- leave id: LVE-1863\n- employee: Jonas Imai\n- lawyer letter received about this leave: no\n- leave days: 21\n- notice period met: yes\n- requests team free of harassment complaints: yes\n- team coverage not arranged: no\n- leave request written in a formal tone: no\n- leave days soft limit: 21\n- medical certificate contested: no\n- leave balance available: yes\n- request falls in blackout period: no\n- union grievance raised over this leave: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 4181 if notice_period_met is false or team_coverage_not_arranged is true or leave_days is above leave_days_soft_limit.\n2. 5 if request_falls_in_blackout_period is true.\n3. 85 if leave_balance_available is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or union_grievance_raised_over_this_leave is true.\nOtherwise: 853.\nNever counted: lawyer_letter_received_about_this_leave, leave_request_written_in_a_formal_tone.\nMeanings:\n- 85: delegate the call to whoever holds authority\n- 4181: suspend action until the facts are confirmed\n- 5: shut off this process completely\n- 853: advance the task as stated without any blockers\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "853",
   "4181",
   "85"
  ]
 },
 {
  "qid": "q532e4a8bfd",
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
  "qid": "q3d3ecf8ecb",
  "kind": "choice",
  "text": "---\n# request record\nrequest_id: \"REQ-9316\"\nrequester: \"Lena Haddad\"\nrequest_grants_admin_rights: false\nbusiness_justification_provided: true\nmfa_enrollment_complete: true\naccess_days_approval_threshold: 30\nethics_office_flagged_the_request: false\nlegal_preservation_order_on_the_account: false\naccount_suspended: false\naccess_days: 40\nrequester_not_barred_from_this_system: true\nrequest_text_written_in_capital_letters: false\nrequested_role_forbidden_by_policy: false",
  "question": "Meanings:\n- refuse: shut off this process completely\n- pend: hold all progress until the requisite documentation arrives\n- refer to owner: delegate the call to whoever holds authority\n- grant: carry on with it now\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "grant",
   "refuse",
   "refer to owner"
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
  "qid": "q07897c2ed2",
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
  "qid": "qf51ee59333",
  "kind": "choice",
  "text": "{\n  \"record\":{\n    \"ticket_id\":\"TCK-8298\",\n    \"customer\":\"Jonas Castell\"\n  },\n  \"numbers\":{\n    \"claim_amount\":753.59,\n    \"claim_amount_hard_limit\":1000.00\n  },\n  \"flags\":{\n    \"customer_message_is_short\":true,\n    \"harmless_greeting_present_in_the_message\":true,\n    \"claim_free_of_ombudsman_cases\":true,\n    \"claim_involves_a_media_inquiry\":true,\n    \"legal_complaint_filed\":false,\n    \"proof_of_purchase_attached\":true,\n    \"customer_message_written_in_a_casual_tone\":true,\n    \"item_return_not_yet_received\":false,\n    \"claim_form_filled_in_with_the_usual_font\":true,\n    \"free_of_safety_incident_reports\":false,\n    \"item_excluded_by_policy\":false\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. delay if proof_of_purchase_attached is false or claim_involves_a_media_inquiry is true.\n3. ask a human if item_return_not_yet_received is true or legal_complaint_filed is true or free_of_safety_incident_reports is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nLooking at what was asked, which of the actions below best fits the request?",
  "options": [
   "delay",
   "approve",
   "ask a human"
  ]
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
  "qid": "q2fa23c8eaa",
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
  "qid": "q3fd5962437",
  "kind": "choice",
  "text": "# request record\nleave_id | LVE-3290\nemployee | Samir Calloway\nteam_coverage_not_arranged | false\nlawyer_letter_received_about_this_leave | false\nleave_request_written_in_a_formal_tone | false\nnotice_period_met | true\nunion_grievance_raised_over_this_leave | true\nleave_days_soft_limit | 21\nleave_days | 3\nleave_balance_exhausted | false\nmedical_certificate_contested | false\nrequest_falls_in_blackout_period | false\nrequests_team_free_of_harassment_complaints | true",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, what is the right call for this request?",
  "options": [
   "refuse",
   "ask a human",
   "approve"
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
  "qid": "qa6e3d3ffdc",
  "kind": "choice",
  "text": "# extract\ninvoice_id: INV-5393\nvendor: Northwind Labs\nawaiting_purchase_order: false\namount: 493.80\nduplicate_of_paid_invoice: true\ninvoice_pdf_uses_a_portrait_layout: false\namount_approval_threshold: 500.00\npayment_requested_during_business_hours: true\nvendor_tax_form_on_file: true\napprover_declared_a_conflict_of_interest: false\nvendor_on_sanctions_list: false\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_name_written_in_capital_letters: true",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed fits the case described in this file best?",
  "options": [
   "pay",
   "hold",
   "reject"
  ]
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
  "qid": "qc10777df0d",
  "kind": "choice",
  "text": "{\"run_id\": \"RUN-5054\", \"agent\": \"helix\", \"owner_sign_off_required_for_this_action\": false, \"action_forbidden_by_security_policy\": false, \"action_free_of_ethics_concerns\": true, \"steps_used_hard_limit\": 60, \"task_description_incomplete\": false, \"tool_output_shows_tampering\": false, \"last_tool_output_unverified\": false, \"steps_used\": 18, \"log_lines_written_in_a_compact_style\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. wait if task_description_incomplete is true or steps_used is above steps_used_hard_limit.\n3. ask_a_human if action_forbidden_by_security_policy is true or owner_sign_off_required_for_this_action is true.\nOtherwise: proceed.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_compact_style.\nMeanings:\n- ask_a_human: direct the request to the responsible decider\n- proceed: keep it moving forward\n- wait: hold the request so the requester waits for their check\n- cancel: make sure the requester never gets what they wanted\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "wait",
   "ask_a_human",
   "proceed"
  ]
 },
 {
  "qid": "qd465453a5d",
  "kind": "choice",
  "text": "# record\nrequest_id: REQ-4268\nrequester: Samir Okonkwo\naccess_days: 60\nbusiness_justification_provided: true\nrequest_grants_admin_rights: false\nlegal_preservation_order_on_the_account: false\nrequest_text_written_in_capital_letters: false\nmfa_enrollment_complete: true\nrequest_free_of_ethics_office_flags: true\nrequester_barred_from_this_system: true\naccount_suspended: false\nrequested_role_permitted_by_policy: true\naccess_days_approval_threshold: 60",
  "question": "Meanings:\n- wait: withhold action until supporting information is supplied\n- ask a human: delegate the call to whoever holds authority\n- cancel: halt this item because the rules forbid it\n- proceed: complete the action that was asked for\nThe record is complete: nothing else applies.\n\nIn this case file, which of the listed actions is the correct decision?",
  "options": [
   "cancel",
   "wait",
   "proceed"
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
  "qid": "qd241ab5a28",
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
 }
]
