# G5-H blind read T46-blind_read-bc9e16d1-004 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8a/T46/qc/g5h/answers/T46-blind_read-bc9e16d1-004.json

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
  "qid": "q40e29ef778",
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
  "qid": "q2080097b77",
  "kind": "yes/no",
  "text": "# record\nrequest_id | REQ-3758\nrequester | Nadia Imai\nmfa_enrollment_incomplete | false\nrequest_text_written_in_capital_letters | false\nlegal_preservation_order_on_the_account | false\nethics_office_flagged_the_request | false\naccess_days_approval_threshold | 60\naccess_days | 27\nrequest_grants_admin_rights | true\naccount_suspended | false\nrequester_not_barred_from_this_system | true\nbusiness_justification_missing | false\nrequested_role_permitted_by_policy | false",
  "question": "Proposed action: ask_a_human\nIs it not the case that the facts shown here back the proposed action, which is not mistaken?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. wait if requested_role_permitted_by_policy is false.\n3. cancel if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: proceed.\nNever counted: business_justification_missing, requester_not_barred_from_this_system, request_text_written_in_capital_letters.\nMeanings:\n- proceed: complete the job as it was assigned\n- ask_a_human: give it to the person in charge of the call\n- cancel: end this here and now\n- wait: wait for that check then we will see\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q85d82132f2",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  leave_id: LVE-7443\n  employee: Aiko Mensah\nnumbers:\n  leave_days_soft_limit: 21\n  leave_days: 10\nflags:\n  leave_balance_exhausted: false\n  leave_request_written_in_a_formal_tone: true\n  request_falls_in_blackout_period: false\n  medical_certificate_contested: false\n  lawyer_letter_received_about_this_leave: false\n  team_coverage_arranged: true\n  requests_team_free_of_harassment_complaints: false\n  notice_period_met: true\n  union_grievance_raised_over_this_leave: false",
  "question": "Proposed action: proceed\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if notice_period_met is false or team_coverage_arranged is false or leave_balance_exhausted is true or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. cancel if medical_certificate_contested is true.\n3. ask_a_human if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: proceed.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- ask_a_human: route the case to a decider so the requester knows the outcome\n- cancel: be stopped and never carried out\n- proceed: go on and finish it the path is clear\n- wait: be kept on hold until more information is supplied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe6b28de4ac",
  "kind": "choice",
  "text": "---\n# request record\nrecord:\n    ticket_id: \"TCK-7524\"\n    customer: \"Marta Anand\"\nnumbers:\n    claim_amount_hard_limit: 100.00\n    claim_amount: 99.99\nflags:\n    item_return_received: true\n    claim_form_filled_in_with_the_usual_font: true\n    item_excluded_by_policy: false\n    free_of_legal_complaints: true\n    customer_message_is_short: true\n    claim_free_of_ombudsman_cases: false\n    proof_of_purchase_attached: true\n    free_of_safety_incident_reports: true\n    claim_involves_a_media_inquiry: false\n    customer_message_written_in_a_formal_tone: false\n    harmless_greeting_present_in_the_message: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. defer if proof_of_purchase_attached is false or claim_amount is at least claim_amount_hard_limit.\n3. deny if item_excluded_by_policy is true or free_of_legal_complaints is false or claim_involves_a_media_inquiry is true.\nOtherwise: approve.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nThe request describes a situation; which of the actions underneath handles it correctly?",
  "options": [
   "ask_manager",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q89665415f0",
  "kind": "choice",
  "text": "# extract\nrun_id: RUN-5717\nagent: jasper\nsteps_used_hard_limit: 8\naction_free_of_ethics_concerns: true\nlog_lines_written_in_a_compact_style: true\nsteps_used: 2\nlast_tool_output_verified: true\nowner_sign_off_required_for_this_action: true\ntask_description_incomplete: false\ntool_output_shows_tampering: false\naction_forbidden_by_security_policy: false",
  "question": "Meanings:\n- pause: hang tight until we get the check back\n- stop: stop this course of action at once\n- human review: hand this over to whoever has the final say\n- continue: keep moving so the asker gets the outcome\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "pause",
   "human review",
   "continue"
  ]
 },
 {
  "qid": "q8d56f0ab06",
  "kind": "choice",
  "text": "request_id | REQ-6126\nrequester | Hugo Haddad\nrequest_free_of_ethics_office_flags | true\nbusiness_justification_missing | false\nrequester_barred_from_this_system | false\naccount_suspended | false\naccess_days_approval_threshold | 7\nrequest_text_written_in_capital_letters | false\nrequest_grants_admin_rights | true\naccess_days | 3\nrequested_role_permitted_by_policy | true\nlegal_preservation_order_on_the_account | false\nmfa_enrollment_incomplete | false",
  "question": "Meanings:\n- 7: pump the brakes until more details show up\n- 685: get referred to the person who decides\n- 1162: run the task as it was asked, with nothing standing between it and completion\n- 23: be halted at once and left unperformed\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this question suits the request best?",
  "options": [
   "7",
   "685",
   "1162"
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
  "qid": "qfd3aad0517",
  "kind": "yes/no",
  "text": "invoice_id | INV-7422\nvendor | Riverbend Traders\ninvoice_pdf_uses_a_landscape_layout | false\nawaiting_purchase_order | false\npayment_requested_during_business_hours | true\nduplicate_of_paid_invoice | true\namount | 2138.37\nvendor_tax_form_on_file | true\napprover_declared_a_conflict_of_interest | false\namount_approval_threshold | 5000.00\nvendor_on_sanctions_list | true\nvendor_name_written_in_capital_letters | false\nvendor_filed_a_legal_claim_over_this_invoice | false",
  "question": "Proposed action: cancel\nSet beside the request in the record, is the proposed action the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if vendor_on_sanctions_list is true or approver_declared_a_conflict_of_interest is true.\n2. ask a human if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. wait if awaiting_purchase_order is true or amount is at least amount_approval_threshold.\nOtherwise: proceed.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies."
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
  "qid": "q381e11fe85",
  "kind": "choice",
  "text": "---\n# case\ndeploy_id: DEP-6900\nservice: auth_proxy\ncommit_messages_written_in_a_casual_tone: true\ndeploy_blocked_by_security_policy: true\nfiles_changed_soft_limit: 20\ndeploy_title_written_in_normal_case: false\nfiles_changed: 20\ndeploy_has_a_long_description: false\nservice_free_of_major_incidents: true\ncommit_messages_written_in_a_detailed_style: true\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_prohibited_during_the_audit_window: false\ncanary_results_incomplete: false\nrollout_approval_revoked: false\nbackout_plan_missing: false",
  "question": "Meanings:\n- human review: route this matter to the individual empowered to decide\n- continue: let this be advanced exactly as originally specified\n- stop: reject the request in full\n- pause: keep waiting for the missing details\nThe record is complete: nothing else applies.\n\nTaking the actions listed into account, what is the right call for the request?",
  "options": [
   "continue",
   "stop",
   "human review"
  ]
 },
 {
  "qid": "qe7bce48179",
  "kind": "choice",
  "text": "{\"ticket_id\":\"TCK-9172\",\"customer\":\"Mira Imai\",\"claim_involves_a_media_inquiry\":false,\"harmless_greeting_present_in_the_message\":true,\"claim_amount\":21.00,\"free_of_safety_incident_reports\":true,\"claim_form_filled_in_with_the_usual_font\":true,\"claim_amount_hard_limit\":100.00,\"free_of_legal_complaints\":true,\"proof_of_purchase_missing\":true,\"item_return_not_yet_received\":false,\"customer_message_is_short\":true,\"customer_message_written_in_a_formal_tone\":false,\"item_excluded_by_policy\":false,\"claim_free_of_ombudsman_cases\":true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if item_return_not_yet_received is true or free_of_safety_incident_reports is false.\n2. delay if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. ask a human if proof_of_purchase_missing is true or free_of_legal_complaints is false or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "refuse",
   "approve",
   "ask a human"
  ]
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
 },
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
  "qid": "qf2633c978a",
  "kind": "choice",
  "text": "{\n    \"leave_id\":\"LVE-3648\",\n    \"employee\":\"Tomas Vasquez\",\n    \"team_coverage_arranged\":false,\n    \"leave_balance_available\":true,\n    \"lawyer_letter_received_about_this_leave\":false,\n    \"notice_period_met\":true,\n    \"requests_team_free_of_harassment_complaints\":true,\n    \"request_falls_in_blackout_period\":false,\n    \"leave_days\":5,\n    \"no_union_grievance_raised_over_this_leave\":true,\n    \"leave_request_written_in_a_formal_tone\":true,\n    \"leave_days_soft_limit\":10,\n    \"medical_certificate_contested\":false\n}",
  "question": "Meanings:\n- 781: hold off until more information arrives\n- 5: run with this one\n- 8940: send it up so the requester gets a firm decision\n- 36: make sure the requester never gets what they wanted\nThe record is complete: nothing else applies.\n\nWhich of the actions listed would be the right call for the matter in this file?",
  "options": [
   "5",
   "36",
   "781"
  ]
 },
 {
  "qid": "qa67d2a6e96",
  "kind": "choice",
  "text": "# extract\nticket_id=TCK-6262\ncustomer=Zoe Anand\nproof_of_purchase_attached=true\ncustomer_message_written_in_a_casual_tone=true\nclaim_involves_a_media_inquiry=false\nclaim_amount=95.38\nclaim_form_filled_in_with_the_usual_font=true\nfree_of_legal_complaints=true\nfree_of_safety_incident_reports=false\nclaim_free_of_ombudsman_cases=true\nclaim_amount_hard_limit=100.00\ncustomer_message_is_short=true\nitem_excluded_by_policy=false\nharmless_greeting_present_in_the_message=true\nitem_return_not_yet_received=false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false.\n2. deny if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_not_yet_received is true.\nOtherwise: approve.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- defer: wait so the requester can supply more information first\n- deny: drop this right there, we are not touching it\n- approve: proceed in accordance with the stated request\n- ask manager: get sent upward to the one who decides\nThe record is complete: nothing else applies.\n\nGiven the request and the facts stated, which of the actions listed is the right call?",
  "options": [
   "defer",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "q71bb63807f",
  "kind": "choice",
  "text": "# request record\ninvoice_id: INV-7052\nvendor: Lakeshore Traders\namount: 2178.97\npayment_requested_during_business_hours: true\nawaiting_purchase_order: false\namount_approval_threshold: 5000.00\napprover_declared_a_conflict_of_interest: false\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_tax_form_missing: false\nduplicate_of_paid_invoice: false\ninvoice_pdf_uses_a_landscape_layout: false\nvendor_free_of_sanctions: true\nvendor_name_written_in_capital_letters: false",
  "question": "Meanings:\n- defer: hold all progress until the requisite documentation arrives\n- deny: shut this down before it spreads into the workflow\n- approve: complete the action that was asked for\n- ask_manager: send it up so the requester gets a firm decision\nThe record is complete: nothing else applies.\n\nWhich of the listed actions is the right call for this request?",
  "options": [
   "defer",
   "ask_manager",
   "approve"
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
  "qid": "q175db7589f",
  "kind": "yes/no",
  "text": "{\n  \"request_id\":\"REQ-1430\",\n  \"requester\":\"Idris Adeyemi\",\n  \"requested_role_permitted_by_policy\":true,\n  \"business_justification_provided\":true,\n  \"legal_preservation_order_on_the_account\":false,\n  \"request_free_of_ethics_office_flags\":true,\n  \"access_days_approval_threshold\":7,\n  \"request_grants_admin_rights\":false,\n  \"requester_not_barred_from_this_system\":true,\n  \"access_days\":4,\n  \"mfa_enrollment_complete\":true,\n  \"request_text_written_in_capital_letters\":false,\n  \"account_suspended\":false\n}",
  "question": "Proposed action: allow\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_provided is false or requested_role_permitted_by_policy is false.\n2. page oncall if mfa_enrollment_complete is false or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. block access if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: allow.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- block access: shut this down fast\n- allow: proceed with the task as asked\n- quarantine: defer the step until the verification is in\n- page oncall: send it up so the requester gets a firm decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q60a38e2a5c",
  "kind": "yes/no",
  "text": "{\"leave_id\":\"LVE-4030\",\"employee\":\"ريم سامي الزهراني\",\"note\":\"عدد الأيام المطلوبة للإجازة ما يزال موضع استفسار.\",\"team_coverage_arranged\":true,\"notice_period_met\":true,\"requests_team_free_of_harassment_complaints\":true,\"leave_days\":6,\"no_union_grievance_raised_over_this_leave\":true,\"leave_days_soft_limit\":10,\"leave_balance_available\":true,\"leave_request_written_in_a_formal_tone\":false,\"medical_certificate_contested\":false,\"request_falls_in_blackout_period\":false,\"lawyer_letter_received_about_this_leave\":false}",
  "question": "Proposed action: 31\nReviewing this as an auditor, do the record's facts rule out the proposed action for the request?",
  "definitions": "Meanings:\n- 7819: have the task carried out as it was originally asked\n- 31: pump the brakes until more details show up\n- 434: bring in the authority who can settle it for the requester\n- 4: end it so the requester sees their request closed\nThe record is complete: nothing else applies."
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
  "qid": "q00dbbe0cdb",
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
  "qid": "q7a68781ada",
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
  "qid": "qa542d77630",
  "kind": "choice",
  "text": "{\n  \"record\":{\n    \"invoice_id\":\"INV-4779\",\n    \"vendor\":\"Harbor Traders\"\n  },\n  \"numbers\":{\n    \"amount\":164.11,\n    \"amount_approval_threshold\":500.00\n  },\n  \"flags\":{\n    \"vendor_on_sanctions_list\":false,\n    \"invoice_pdf_uses_a_landscape_layout\":false,\n    \"payment_requested_during_business_hours\":true,\n    \"vendor_tax_form_missing\":false,\n    \"purchase_order_received\":true,\n    \"duplicate_of_paid_invoice\":false,\n    \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n    \"approver_free_of_conflicts_of_interest\":true,\n    \"vendor_name_written_in_capital_letters\":false\n  }\n}",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed after this, which is the fitting call for the request?",
  "options": [
   "pay",
   "escalate",
   "reject"
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
  "qid": "qfd786ee08f",
  "kind": "yes/no",
  "text": "# record\nleave_id=LVE-3775\nemployee=Dana Lindqvist\nno_union_grievance_raised_over_this_leave=true\nleave_days=5\nrequests_team_free_of_harassment_complaints=true\nleave_balance_exhausted=true\nnotice_period_not_met=false\nlawyer_letter_received_about_this_leave=false\nrequest_falls_in_blackout_period=false\nmedical_certificate_contested=false\nleave_days_soft_limit=5\nleave_request_written_in_a_formal_tone=false\nteam_coverage_arranged=true",
  "question": "Proposed action: 4\nWould the proposed action not be the appropriate course under the applicable procedure?",
  "definitions": "Meanings:\n- 50: reject this item since it violates the policy\n- 947: hold off until the check clears\n- 4: give it to a person who has the authority to decide\n- 3539: carry it through and the requester is satisfied\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4571a0f06b",
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
  "qid": "qf7e4299628",
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
  "qid": "q724eee096d",
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
  "qid": "q0194dd8f95",
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
  "qid": "q69f974ee4d",
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
  "qid": "q051bf866e1",
  "kind": "yes/no",
  "text": "---\n# request record\nrequest_id: \"REQ-8744\"\nrequester: \"Nadia Imai\"\nrequester_not_barred_from_this_system: true\nlegal_preservation_order_on_the_account: true\nbusiness_justification_missing: false\nrequest_free_of_ethics_office_flags: true\naccess_days: 12\naccount_suspended: false\nrequest_grants_admin_rights: false\nrequest_text_written_in_capital_letters: true\naccess_days_approval_threshold: 60\nmfa_enrollment_complete: true\nrequested_role_forbidden_by_policy: false",
  "question": "Proposed action: 9605\nShould the proposed action be taken for this request?",
  "definitions": "Meanings:\n- 9605: forward the matter as the call rests with someone higher\n- 3: hold the request until the check is done\n- 645: leave the requester without the result they asked for\n- 11: press on with the work as originally set\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q47424c24e1",
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
 }
]
