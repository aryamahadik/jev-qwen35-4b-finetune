# G5-H blind read T46-blind_read-2caa1b95-004 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8b/T46/qc/g5h/answers/T46-blind_read-2caa1b95-004.json

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
  "qid": "q2fb6a5722f",
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
  "qid": "q184ddcc688",
  "kind": "yes/no",
  "text": "{\n  \"ticket_id\":\"TCK-8352\",\n  \"customer\":\"Nadia Imai\",\n  \"harmless_greeting_present_in_the_message\":true,\n  \"claim_involves_a_media_inquiry\":false,\n  \"claim_amount_hard_limit\":500.00,\n  \"item_excluded_by_policy\":false,\n  \"claim_free_of_ombudsman_cases\":true,\n  \"free_of_safety_incident_reports\":true,\n  \"item_return_not_yet_received\":false,\n  \"proof_of_purchase_missing\":false,\n  \"claim_form_filled_in_with_the_usual_font\":true,\n  \"customer_message_is_short\":true,\n  \"customer_message_written_in_a_casual_tone\":true,\n  \"legal_complaint_filed\":false,\n  \"claim_amount\":378.96\n}",
  "question": "Proposed action: ask_a_human\nIs it not the case that the proposed action is what the request and facts call for, and is not a poor choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if claim_amount is above claim_amount_hard_limit.\n2. ask_a_human if item_return_not_yet_received is true or item_excluded_by_policy is true or legal_complaint_filed is true or free_of_safety_incident_reports is false or claim_involves_a_media_inquiry is true.\n3. delay if proof_of_purchase_missing is true or claim_free_of_ombudsman_cases is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- refuse: bin this idea and keep it out of the flow\n- approve: proceed with the task as asked\n- delay: wait for the document to come through\n- ask_a_human: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc8b595a294",
  "kind": "yes/no",
  "text": "---\n# record\nrun_id: RUN-5515\nagent: ember\ntask_description_complete: true\ntool_output_shows_tampering: false\nsteps_used: 11\nsteps_used_hard_limit: 30\nlast_tool_output_unverified: false\naction_free_of_ethics_concerns: true\nowner_sign_off_required_for_this_action: false\naction_permitted_by_security_policy: false\nlog_lines_written_in_a_verbose_style: false",
  "question": "Proposed action: human review\nDoes the record's evidence rule out the proposed action as the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. human review if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. pause if last_tool_output_unverified is true or task_description_complete is false.\n3. stop if action_permitted_by_security_policy is false or owner_sign_off_required_for_this_action is true or steps_used is above steps_used_hard_limit.\nOtherwise: continue.\nNever counted: log_lines_written_in_a_verbose_style.\nMeanings:\n- continue: carry on with it now\n- stop: stop the work since it cannot move forward\n- pause: keep it in limbo until the verification has been confirmed\n- human review: transfer it to the person with authority\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3b3536bef1",
  "kind": "choice",
  "text": "---\nrequest:\n  run_id: RUN-4463\n  agent: jasper\nfigures:\n  steps_used: 15\n  steps_used_hard_limit: 20\nchecks:\n  task_description_incomplete: false\n  action_permitted_by_security_policy: true\n  action_free_of_ethics_concerns: true\n  owner_sign_off_required_for_this_action: false\n  last_tool_output_verified: true\n  log_lines_written_in_a_verbose_style: true\n  tool_output_shows_tampering: false",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions listed fits the case described in this file best?",
  "options": [
   "continue",
   "human review",
   "stop"
  ]
 },
 {
  "qid": "q0f25bfdfc5",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"leave_id\": \"LVE-8049\",\n        \"employee\": \"Anders Novak\"\n    },\n    \"metrics\": {\n        \"leave_days_soft_limit\": 7,\n        \"leave_days\": 2\n    },\n    \"signals\": {\n        \"union_grievance_raised_over_this_leave\": true,\n        \"team_coverage_arranged\": true,\n        \"leave_balance_available\": true,\n        \"leave_request_written_in_a_formal_tone\": true,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"notice_period_met\": true,\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"request_falls_in_blackout_period\": false\n    }\n}",
  "question": "Proposed action: turn_down\nIs it not correct that the proposed action is not off base, judging by the record on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if notice_period_met is false or team_coverage_arranged is false or leave_balance_available is false or lawyer_letter_received_about_this_leave is true or leave_days is above leave_days_soft_limit.\n2. turn_down if request_falls_in_blackout_period is true.\n3. send_to_a_person if medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false.\nOtherwise: go_ahead.\nNever counted: union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4e4862a49a",
  "kind": "yes/no",
  "text": "{\n    \"record\":{\n        \"deploy_id\":\"DEP-7513\",\n        \"service\":\"auth_proxy\"\n    },\n    \"numbers\":{\n        \"files_changed\":39,\n        \"files_changed_soft_limit\":80\n    },\n    \"flags\":{\n        \"deploy_prohibited_during_the_audit_window\":true,\n        \"deploy_blocked_by_security_policy\":false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\":false,\n        \"canary_results_complete\":true,\n        \"service_free_of_major_incidents\":true,\n        \"rollout_approval_revoked\":true,\n        \"deploy_has_a_long_description\":false,\n        \"deploy_title_written_in_normal_case\":true,\n        \"commit_messages_written_in_a_detailed_style\":true,\n        \"commit_messages_written_in_a_casual_tone\":true,\n        \"backout_plan_documented\":true\n    }\n}",
  "question": "Proposed action: turn down\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if canary_results_complete is false.\n2. turn down if rollout_approval_revoked is true.\n3. put on hold if backout_plan_documented is false or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\nOtherwise: go ahead.\nNever counted: deploy_has_a_long_description, deploy_blocked_by_security_policy, service_free_of_major_incidents, contract_customer_asked_for_a_say_in_this_rollout, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- turn down: shut this down right away, we are staying clear of it\n- send to a person: hand this over to whoever has the final say\n- put on hold: chill until the document turns up\n- go ahead: proceed and the requester gets what they asked\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0566aa3bb3",
  "kind": "choice",
  "text": "{\n  \"case\":{\n    \"ticket_id\":\"TCK-8919\",\n    \"customer\":\"Ingrid Imai\"\n  },\n  \"values\":{\n    \"claim_amount_hard_limit\":1000.00,\n    \"claim_amount\":999.99\n  },\n  \"tests\":{\n    \"customer_message_written_in_a_casual_tone\":true,\n    \"item_return_not_yet_received\":false,\n    \"harmless_greeting_present_in_the_message\":true,\n    \"claim_free_of_ombudsman_cases\":true,\n    \"customer_message_is_short\":true,\n    \"claim_form_filled_in_with_the_usual_font\":true,\n    \"legal_complaint_filed\":true,\n    \"item_excluded_by_policy\":false,\n    \"claim_involves_a_media_inquiry\":false,\n    \"proof_of_purchase_attached\":true,\n    \"free_of_safety_incident_reports\":false\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. cancel if claim_amount is at least claim_amount_hard_limit.\n2. ask a human if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. wait if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: proceed.\nNever counted: item_return_not_yet_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- wait: pause this until the requester supplies the missing document\n- cancel: stop this course of action at once\n- proceed: continue as requested with the path fully open\n- ask a human: send it onward because someone else must decide\nThe record is complete: nothing else applies.\n\nGiven the details in the record, which action listed would be the correct decision?",
  "options": [
   "proceed",
   "cancel",
   "ask a human"
  ]
 },
 {
  "qid": "q8e0939d2d8",
  "kind": "choice",
  "text": "---\n# case\ninvoice_id: INV-2869\nvendor: Brightwater Partners\nvendor_free_of_sanctions: true\nduplicate_of_paid_invoice: true\npayment_requested_during_business_hours: true\napprover_declared_a_conflict_of_interest: false\namount: 947.27\nvendor_tax_form_missing: false\nvendor_name_written_in_capital_letters: false\nvendor_filed_a_legal_claim_over_this_invoice: false\nawaiting_purchase_order: false\ninvoice_pdf_uses_a_portrait_layout: true\namount_approval_threshold: 1000.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if approver_declared_a_conflict_of_interest is true.\n2. turn_down if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: go_ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- put_on_hold: pause the request and gather more information before going on\n- go_ahead: continue so the requester receives the result\n- turn_down: withdraw from the step as it is forbidden\n- send_to_a_person: refer the matter to the decision holder\nThe record is complete: nothing else applies.\n\nGiven the request and the facts stated, which of the actions listed is the right call?",
  "options": [
   "send_to_a_person",
   "go_ahead",
   "turn_down"
  ]
 },
 {
  "qid": "qfff94d2340",
  "kind": "yes/no",
  "text": "---\n# record\nticket_id: \"TCK-9835\"\ncustomer: \"Ingrid Novak\"\nitem_return_received: true\nclaim_form_filled_in_with_the_usual_font: true\nharmless_greeting_present_in_the_message: true\nclaim_involves_a_media_inquiry: false\nitem_excluded_by_policy: false\nproof_of_purchase_missing: true\ncustomer_message_written_in_a_formal_tone: false\nfree_of_safety_incident_reports: true\nclaim_amount_hard_limit: 200.00\nlegal_complaint_filed: true\ncustomer_message_is_short: true\nclaim_amount: 126.47\nclaim_free_of_ombudsman_cases: true",
  "question": "Proposed action: wait\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. wait if proof_of_purchase_missing is true or claim_amount is at least claim_amount_hard_limit.\n3. cancel if item_excluded_by_policy is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\nOtherwise: proceed.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_formal_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe2d3e95229",
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
  "qid": "qe39e233389",
  "kind": "yes/no",
  "text": "leave_id | LVE-9441\nemployee | عادل فؤاد النابلسي\nnote | المدير المباشر وافق على الطلب مسبقاً.\nrequests_team_free_of_harassment_complaints | true\nnotice_period_not_met | false\nleave_days | 7\nunion_grievance_raised_over_this_leave | false\nmedical_certificate_contested | false\nleave_request_written_in_a_formal_tone | false\nteam_coverage_arranged | true\nlawyer_letter_received_about_this_leave | false\nleave_days_soft_limit | 7\nrequest_falls_in_blackout_period | false\nleave_balance_available | false",
  "question": "Proposed action: PXS\nLooking at what the record says, is the proposed action a good fit for the request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. T if notice_period_not_met is true or team_coverage_arranged is false or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. VSFG if medical_certificate_contested is true.\n3. HM if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: PXS.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- T: hold all progress until the requisite documentation arrives\n- VSFG: reject the request in full\n- PXS: run the requested step through\n- HM: get the boss to make the final call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa09275bfd4",
  "kind": "yes/no",
  "text": "---\n# request record\nsubject:\n  deploy_id: \"DEP-1264\"\n  service: \"auth_proxy\"\namounts:\n  files_changed: 10\n  files_changed_soft_limit: 15\nchecks:\n  commit_messages_written_in_a_detailed_style: false\n  deploy_title_written_in_normal_case: true\n  deploy_prohibited_during_the_audit_window: false\n  backout_plan_documented: true\n  deploy_blocked_by_security_policy: true\n  rollout_approval_revoked: true\n  deploy_has_a_long_description: false\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  commit_messages_written_in_a_casual_tone: true\n  canary_results_complete: false\n  service_free_of_major_incidents: true",
  "question": "Proposed action: wait\nBe honest, do the facts here rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. cancel if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. wait if canary_results_complete is false.\nOtherwise: proceed.\nNever counted: backout_plan_documented, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- wait: be kept on hold until more information is supplied\n- cancel: scrap the plan and drop this request\n- proceed: let this be advanced exactly as originally specified\n- ask_a_human: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q7630eb912c",
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
  "qid": "qc29d370f20",
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
  "qid": "qcb4eaa9691",
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
  "qid": "q62a90c85ba",
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
  "qid": "q460b4e5756",
  "kind": "choice",
  "text": "# record\nrequest_id: REQ-3636\nrequester: Omar Calloway\naccount_suspended: false\nbusiness_justification_missing: false\nmfa_enrollment_incomplete: false\nlegal_preservation_order_on_the_account: true\nrequester_not_barred_from_this_system: true\naccess_days: 1\nrequest_free_of_ethics_office_flags: true\naccess_days_approval_threshold: 14\nrequest_grants_admin_rights: false\nrequested_role_forbidden_by_policy: false\nrequest_text_written_in_capital_letters: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. HD if request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n2. W if mfa_enrollment_incomplete is true.\n3. RJGT if business_justification_missing is true or account_suspended is true or requested_role_forbidden_by_policy is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\nOtherwise: HSZ.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- HD: get referred to the person who decides\n- W: keep it on hold for the missing document\n- RJGT: decline the request as the action is prohibited\n- HSZ: continue the work as originally asked, there is nothing in the way\nThe record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "HD",
   "RJGT",
   "HSZ"
  ]
 },
 {
  "qid": "qb3f81a8656",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-5682\n- requester: Mira Vasquez\n- requested role forbidden by policy: no\n- requester barred from this system: no\n- account suspended: no\n- request grants admin rights: no\n- mfa enrollment incomplete: yes\n- ethics office flagged the request: no\n- business justification missing: no\n- legal preservation order on the account: no\n- access days: 7\n- request text written in capital letters: no\n- access days approval threshold: 14",
  "question": "Proposed action: approve\nAs an auditor, do the facts in the record rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. delay if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_missing, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf44ac99529",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-8460\nvendor | Copperfield Systems\nduplicate_of_paid_invoice | false\nvendor_name_written_in_capital_letters | false\napprover_declared_a_conflict_of_interest | false\npurchase_order_received | true\namount | 1963.33\ninvoice_pdf_uses_a_landscape_layout | false\nvendor_tax_form_missing | false\npayment_requested_during_business_hours | true\nvendor_filed_a_legal_claim_over_this_invoice | true\nvendor_free_of_sanctions | true\namount_approval_threshold | 2500.00",
  "question": "Proposed action: 199\nQuick check: do the facts in the record rule out the proposed action here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 43 if purchase_order_received is false or vendor_tax_form_missing is true.\n2. 1799 if vendor_free_of_sanctions is false.\n3. 199 if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: 5.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- 1799: make sure the requester never gets what they wanted\n- 199: send this on to whoever decides\n- 43: hold all progress until the requisite documentation arrives\n- 5: execute the request exactly as written\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q220638c373",
  "kind": "choice",
  "text": "---\n# record\nrequest:\n    deploy_id: DEP-1964\n    service: reports\nfigures:\n    files_changed: 22\n    files_changed_soft_limit: 50\nchecks:\n    deploy_blocked_by_security_policy: true\n    commit_messages_written_in_a_detailed_style: true\n    backout_plan_documented: true\n    commit_messages_written_in_a_casual_tone: true\n    deploy_has_a_long_description: false\n    canary_results_incomplete: false\n    rollout_approval_revoked: false\n    deploy_title_written_in_normal_case: false\n    deploy_prohibited_during_the_audit_window: false\n    contract_customer_asked_for_a_say_in_this_rollout: true\n    service_free_of_major_incidents: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if backout_plan_documented is false.\n2. cancel if rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true or contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is at least files_changed_soft_limit.\n3. ask a human if deploy_blocked_by_security_policy is true or service_free_of_major_incidents is false.\nOtherwise: proceed.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- proceed: keep plugging away at it nothing else stands in the way\n- wait: hold this until a check comes back\n- cancel: kill this one off, it is off the table for good\n- ask a human: submit the question to the authorised decision maker\nThe record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "wait",
   "proceed",
   "cancel"
  ]
 },
 {
  "qid": "q8010128fed",
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
  "qid": "qad8078e98a",
  "kind": "choice",
  "text": "leave_id: LVE-5502\nemployee: Nadia Duarte\nmedical_certificate_contested: true\nleave_days_soft_limit: 21\nleave_days: 2\nno_union_grievance_raised_over_this_leave: false\nnotice_period_not_met: false\nteam_coverage_arranged: true\nleave_balance_available: true\nlawyer_letter_received_about_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nrequest_falls_in_blackout_period: false\nleave_request_written_in_a_formal_tone: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_not_met is true or team_coverage_arranged is false or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. deny if medical_certificate_contested is true.\n3. ask manager if no_union_grievance_raised_over_this_leave is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- deny: be rejected in full and never acted upon\n- ask manager: route it elsewhere because a decider must weigh in\n- approve: go ahead and the requester will be served\n- defer: freeze progress until the paperwork arrives\nThe record is complete: nothing else applies.\n\nWhich of the actions listed fits the case described in this file best?",
  "options": [
   "deny",
   "ask manager",
   "defer"
  ]
 },
 {
  "qid": "q651d2ca781",
  "kind": "choice",
  "text": "deploy_id: DEP-3043\nservice: reports\nbackout_plan_missing: false\ncommit_messages_written_in_a_casual_tone: true\ndeploy_has_a_long_description: false\ncommit_messages_written_in_a_terse_style: false\nfiles_changed: 8\nrollout_approval_revoked: false\ncanary_results_complete: true\ndeploy_blocked_by_security_policy: true\ndeploy_prohibited_during_the_audit_window: false\nfiles_changed_soft_limit: 30\ndeploy_title_written_in_normal_case: true\ncontract_customer_asked_for_a_say_in_this_rollout: true\nservice_free_of_major_incidents: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. QRH if backout_plan_missing is true or files_changed is above files_changed_soft_limit.\n2. PW if deploy_blocked_by_security_policy is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true.\n3. SMJT if service_free_of_major_incidents is false or contract_customer_asked_for_a_say_in_this_rollout is true.\nOtherwise: G.\nNever counted: canary_results_complete, deploy_has_a_long_description, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- QRH: be left pending until the review has been finished\n- G: go on and finish it\n- PW: drop it right away\n- SMJT: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies.\n\nWhich of the actions listed under the record would the requester see as the right call?",
  "options": [
   "G",
   "PW",
   "SMJT"
  ]
 },
 {
  "qid": "q6851a35180",
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
  "qid": "q5d44e0f601",
  "kind": "yes/no",
  "text": "---\n# case\nsubject:\n    leave_id: LVE-3068\n    employee: Mira Okafor\namounts:\n    leave_days_soft_limit: 7\n    leave_days: 3\nchecks:\n    team_coverage_not_arranged: false\n    union_grievance_raised_over_this_leave: false\n    leave_request_written_in_a_formal_tone: true\n    request_falls_in_blackout_period: false\n    leave_balance_available: true\n    medical_certificate_contested: false\n    requests_team_free_of_harassment_complaints: false\n    notice_period_met: true\n    lawyer_letter_received_about_this_leave: false",
  "question": "Proposed action: approve\nOn review of the record, is the proposed action the appropriate decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if notice_period_met is false or request_falls_in_blackout_period is true.\n2. delay if team_coverage_not_arranged is true or leave_balance_available is false or leave_days is above leave_days_soft_limit.\n3. ask a human if medical_certificate_contested is true or union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q354f4ea472",
  "kind": "yes/no",
  "text": "{\"leave_id\": \"LVE-6939\", \"employee\": \"Paolo Anand\", \"leave_days\": 1, \"leave_days_soft_limit\": 3, \"request_falls_in_blackout_period\": false, \"notice_period_met\": true, \"team_coverage_arranged\": true, \"leave_balance_available\": true, \"requests_team_free_of_harassment_complaints\": true, \"lawyer_letter_received_about_this_leave\": false, \"leave_request_written_in_a_formal_tone\": false, \"union_grievance_raised_over_this_leave\": false, \"medical_certificate_contested\": false}",
  "question": "Proposed action: wait\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q378cb57a08",
  "kind": "choice",
  "text": "# record\ndeploy_id | DEP-8517\nservice | uploads\ndeploy_prohibited_during_the_audit_window | true\ncanary_results_incomplete | false\ndeploy_has_a_long_description | false\ndeploy_blocked_by_security_policy | false\ncommit_messages_written_in_a_detailed_style | true\nbackout_plan_missing | false\nrollout_approval_revoked | false\nfiles_changed | 6\nservice_free_of_major_incidents | true\ncontract_customer_asked_for_a_say_in_this_rollout | false\ncommit_messages_written_in_a_casual_tone | true\nfiles_changed_soft_limit | 15\ndeploy_title_written_in_normal_case | false",
  "question": "Meanings:\n- stop: leave the requester without the result they asked for\n- pause: park this until a record turns up\n- human review: pass this along to the decision maker\n- continue: proceed as requested as nothing impedes this course\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "stop",
   "pause",
   "continue"
  ]
 },
 {
  "qid": "qb8536f7289",
  "kind": "yes/no",
  "text": "# case\nleave_id                                    | LVE-8686\nemployee                                    | Jonas Rossi\nno_union_grievance_raised_over_this_leave   | true\nleave_days_soft_limit                       | 21\nrequest_falls_in_blackout_period            | false\nteam_coverage_arranged                      | false\nnotice_period_met                           | true\nrequests_team_free_of_harassment_complaints | true\nleave_request_written_in_a_formal_tone      | false\nlawyer_letter_received_about_this_leave     | false\nmedical_certificate_contested               | true\nleave_balance_exhausted                     | false\nleave_days                                  | 20",
  "question": "Proposed action: go ahead\nHas the audit trail in the record ruled out the proposed action as a sound call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if notice_period_met is false or team_coverage_arranged is false or leave_days is above leave_days_soft_limit.\n2. turn down if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. send to a person if leave_balance_exhausted is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: go ahead.\nNever counted: leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9fbf91a751",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-5682\n- requester: Mira Vasquez\n- requested role forbidden by policy: no\n- requester barred from this system: no\n- account suspended: no\n- request grants admin rights: no\n- mfa enrollment incomplete: no\n- ethics office flagged the request: no\n- business justification missing: no\n- legal preservation order on the account: no\n- access days: 7\n- request text written in capital letters: no\n- access days approval threshold: 14",
  "question": "Proposed action: approve\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. delay if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_missing, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4f1c4851b6",
  "kind": "yes/no",
  "text": "---\n# record\ndeploy_id: \"DEP-4792\"\nservice: \"profile\"\ndeploy_prohibited_during_the_audit_window: false\nbackout_plan_documented: true\ndeploy_blocked_by_security_policy: false\nservice_free_of_major_incidents: true\ndeploy_has_a_long_description: false\ncommit_messages_written_in_a_detailed_style: true\ncommit_messages_written_in_a_casual_tone: true\ncanary_results_incomplete: true\nrollout_approval_revoked: false\nfiles_changed_soft_limit: 50\ncontract_customer_asked_for_a_say_in_this_rollout: false\nfiles_changed: 24\ndeploy_title_written_in_normal_case: true",
  "question": "Proposed action: RFCB\nIs the proposed action ruled out by what the record says?",
  "definitions": "Meanings:\n- D: finish what was asked as stated, the way ahead is fully free\n- RFCB: keep waiting for the missing details\n- FXG: drop it right away\n- PK: send it up to the person who makes the call\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q48f484b61e",
  "kind": "yes/no",
  "text": "# extract\ndeploy_id                                         | DEP-6606\nservice                                           | auth_proxy\nbackout_plan_documented                           | true\ndeploy_prohibited_during_the_audit_window         | false\nfiles_changed_soft_limit                          | 20\ndeploy_blocked_by_security_policy                 | false\ncanary_results_incomplete                         | false\nservice_free_of_major_incidents                   | false\ncommit_messages_written_in_a_casual_tone          | true\ndeploy_has_a_long_description                     | false\ndeploy_title_written_in_normal_case               | true\nrollout_approval_revoked                          | false\nfiles_changed                                     | 21\ncontract_customer_asked_for_a_say_in_this_rollout | false\ncommit_messages_written_in_a_detailed_style       | true",
  "question": "Proposed action: turn down\nHas the record ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_documented is false or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- go ahead: keep going exactly as requested because every obstacle has cleared\n- put on hold: hold off until more information arrives\n- send to a person: be passed along to whoever makes the call\n- turn down: stop the request so the requester gets nothing from it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q23d0c7ca01",
  "kind": "yes/no",
  "text": "---\n# record\nrequest_id: \"REQ-2372\"\nrequester: \"ياسمين حاتم الدباغ\"\nnote: \"موافقة المدير المباشر موجودة على طلب الوصول.\"\nrequested_role_permitted_by_policy: true\nethics_office_flagged_the_request: false\naccess_days: 26\naccess_days_approval_threshold: 60\nrequest_grants_admin_rights: false\naccount_suspended: false\nmfa_enrollment_incomplete: false\nbusiness_justification_missing: false\nrequest_text_written_in_capital_letters: false\nlegal_preservation_order_on_the_account: false\nrequester_not_barred_from_this_system: true",
  "question": "Proposed action: proceed\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- wait: hold the request so the requester waits for their check\n- ask a human: route the request to the decision maker\n- cancel: end it so the requester sees their request closed\n- proceed: keep plugging away at it nothing else stands in the way\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5f27cf8ea0",
  "kind": "yes/no",
  "text": "leave_id: LVE-3042\nemployee: ريما فايز الزبيدي\nnote: طلب الإجازة مقدم في الموعد المحدد بالسياسة.\nleave_days_soft_limit: 10\nleave_request_written_in_a_formal_tone: false\nleave_balance_available: false\nmedical_certificate_contested: false\nno_union_grievance_raised_over_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nleave_days: 4\nteam_coverage_arranged: true\nrequest_falls_in_blackout_period: true\nnotice_period_met: false\nlawyer_letter_received_about_this_leave: false",
  "question": "Proposed action: delay\nDoes what we know about this rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. delay if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. refuse if leave_balance_available is false.\nOtherwise: approve.\nNever counted: notice_period_met, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc9a9d29c4f",
  "kind": "yes/no",
  "text": "{\n    \"leave_id\":\"LVE-8173\",\n    \"employee\":\"كنان ياسر الوادي\",\n    \"note\":\"طلب الإجازة مقدم في الموعد المحدد بالسياسة.\",\n    \"team_coverage_not_arranged\":false,\n    \"leave_balance_available\":true,\n    \"medical_certificate_contested\":false,\n    \"lawyer_letter_received_about_this_leave\":false,\n    \"leave_days\":1,\n    \"no_union_grievance_raised_over_this_leave\":true,\n    \"requests_team_free_of_harassment_complaints\":true,\n    \"notice_period_not_met\":false,\n    \"request_falls_in_blackout_period\":true,\n    \"leave_days_soft_limit\":14,\n    \"leave_request_written_in_a_formal_tone\":true\n}",
  "question": "Proposed action: approve\nDo the documented facts rule out the proposed action under this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_not_met is true or team_coverage_not_arranged is true or leave_days is above leave_days_soft_limit.\n2. deny if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. ask manager if leave_balance_available is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: leave_request_written_in_a_formal_tone.\nMeanings:\n- ask manager: be handed over to the deciding person\n- approve: let the request be continued as originally asked\n- defer: await further verification before any progression\n- deny: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfa0c5e9302",
  "kind": "choice",
  "text": "---\n# record\nrequest_id: \"REQ-1062\"\nrequester: \"Mira Imai\"\nlegal_preservation_order_on_the_account: false\naccess_days_approval_threshold: 30\naccess_days: 6\naccount_suspended: false\nethics_office_flagged_the_request: true\nrequested_role_forbidden_by_policy: true\nrequest_text_written_in_capital_letters: false\nrequester_not_barred_from_this_system: true\nrequest_grants_admin_rights: false\nmfa_enrollment_complete: true\nbusiness_justification_provided: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. wait if business_justification_provided is false or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n2. ask_a_human if mfa_enrollment_complete is false or request_grants_admin_rights is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n3. cancel if account_suspended is true or requested_role_forbidden_by_policy is true.\nOtherwise: proceed.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "ask_a_human",
   "proceed",
   "wait"
  ]
 },
 {
  "qid": "q30e787ccd4",
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
  "qid": "q76c4bb4da1",
  "kind": "choice",
  "text": "{\n    \"meta\":{\n        \"deploy_id\":\"DEP-1137\",\n        \"service\":\"auth_proxy\"\n    },\n    \"metrics\":{\n        \"files_changed\":30,\n        \"files_changed_soft_limit\":30\n    },\n    \"signals\":{\n        \"deploy_blocked_by_security_policy\":false,\n        \"deploy_title_written_in_normal_case\":true,\n        \"rollout_approval_revoked\":false,\n        \"deploy_has_a_long_description\":false,\n        \"commit_messages_written_in_a_casual_tone\":true,\n        \"commit_messages_written_in_a_detailed_style\":true,\n        \"backout_plan_missing\":false,\n        \"deploy_prohibited_during_the_audit_window\":false,\n        \"contract_customer_asked_for_a_say_in_this_rollout\":false,\n        \"service_free_of_major_incidents\":true,\n        \"canary_results_incomplete\":false\n    }\n}",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "wait",
   "proceed",
   "cancel"
  ]
 },
 {
  "qid": "qf38e26476a",
  "kind": "choice",
  "text": "invoice_id: INV-9368\nvendor: Silverline Group\nvendor_filed_a_legal_claim_over_this_invoice: false\nawaiting_purchase_order: false\npayment_requested_during_business_hours: true\namount: 789.49\napprover_declared_a_conflict_of_interest: false\ninvoice_pdf_uses_a_landscape_layout: false\nvendor_name_written_in_capital_letters: false\nvendor_free_of_sanctions: true\nvendor_tax_form_on_file: true\namount_approval_threshold: 1000.00\nduplicate_of_paid_invoice: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. PVQQ if awaiting_purchase_order is true.\n2. HV if vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. D if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or approver_declared_a_conflict_of_interest is true or amount is above amount_approval_threshold.\nOtherwise: HTX.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- PVQQ: wait for the document to come through\n- HV: hand this off because a decider has to choose\n- HTX: keep plugging away at it nothing else stands in the way\n- D: stop the request so the requester gets nothing from it\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "PVQQ",
   "D",
   "HTX"
  ]
 },
 {
  "qid": "q36c62c68b2",
  "kind": "yes/no",
  "text": "{\n    \"request\":{\n        \"leave_id\":\"LVE-4253\",\n        \"employee\":\"Omar Lindqvist\"\n    },\n    \"figures\":{\n        \"leave_days\":2,\n        \"leave_days_soft_limit\":5\n    },\n    \"checks\":{\n        \"union_grievance_raised_over_this_leave\":false,\n        \"team_coverage_not_arranged\":false,\n        \"lawyer_letter_received_about_this_leave\":false,\n        \"leave_request_written_in_a_formal_tone\":false,\n        \"requests_team_free_of_harassment_complaints\":true,\n        \"request_falls_in_blackout_period\":false,\n        \"leave_balance_available\":true,\n        \"medical_certificate_contested\":false,\n        \"notice_period_met\":true\n    }\n}",
  "question": "Proposed action: H\nLooking at the facts, does that rule out the proposed action for this request?",
  "definitions": "Meanings:\n- LB: kill this one off, it is off the table for good\n- BZJQ: hold the request so the requester waits for their check\n- H: get referred to the person who decides\n- VNV: execute the request exactly as written\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q35bfbd7479",
  "kind": "yes/no",
  "text": "# record\ninvoice_id=INV-4515\nvendor=Riverbend Works\namount_approval_threshold=25000.00\namount=16489.36\nvendor_tax_form_missing=false\npayment_requested_during_business_hours=true\nawaiting_purchase_order=false\nduplicate_of_paid_invoice=false\nvendor_filed_a_legal_claim_over_this_invoice=false\nvendor_name_written_in_capital_letters=false\nvendor_free_of_sanctions=true\ninvoice_pdf_uses_a_landscape_layout=false\napprover_free_of_conflicts_of_interest=true",
  "question": "Proposed action: reject\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if approver_free_of_conflicts_of_interest is false.\n2. reject if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- escalate: escalate it so the person asking receives a decision\n- pay: continue with the request as nothing obstructs it\n- reject: block it right away\n- hold: wait until a document arrives before you move forward with it\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q079ca99c9d",
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
  "qid": "q20f17cb461",
  "kind": "yes/no",
  "text": "{\n    \"meta\": {\n        \"leave_id\": \"LVE-8049\",\n        \"employee\": \"Anders Novak\"\n    },\n    \"metrics\": {\n        \"leave_days_soft_limit\": 7,\n        \"leave_days\": 2\n    },\n    \"signals\": {\n        \"union_grievance_raised_over_this_leave\": true,\n        \"team_coverage_arranged\": true,\n        \"leave_balance_available\": true,\n        \"leave_request_written_in_a_formal_tone\": true,\n        \"requests_team_free_of_harassment_complaints\": true,\n        \"notice_period_met\": true,\n        \"medical_certificate_contested\": false,\n        \"lawyer_letter_received_about_this_leave\": false,\n        \"request_falls_in_blackout_period\": false\n    }\n}",
  "question": "Proposed action: turn_down\nConsidering what was asked and the facts involved, is the proposed action not the correct decision?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if notice_period_met is false or team_coverage_arranged is false or leave_balance_available is false or lawyer_letter_received_about_this_leave is true or leave_days is above leave_days_soft_limit.\n2. turn_down if request_falls_in_blackout_period is true.\n3. send_to_a_person if medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false.\nOtherwise: go_ahead.\nNever counted: union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa2bc92f79a",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-9970\n- vendor: Oakmont Foods\n- vendor filed a legal claim over this invoice: no\n- invoice pdf uses a landscape layout: no\n- approver free of conflicts of interest: yes\n- payment requested during business hours: no\n- vendor name written in capital letters: no\n- duplicate of paid invoice: yes\n- amount approval threshold: 5000.00\n- purchase order received: no\n- amount: 5000.00\n- vendor free of sanctions: yes\n- vendor tax form missing: no",
  "question": "Proposed action: delay\nBased on the request itself and the facts around it, is the proposed action not the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if purchase_order_received is false or vendor_tax_form_missing is true.\n2. refuse if vendor_free_of_sanctions is false.\n3. ask_a_human if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_free_of_conflicts_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- approve: finish it so the requester has their answer\n- ask_a_human: hand this to the person who decides\n- refuse: decline the request as the action is prohibited\n- delay: wait so the requester can supply more information first\nThe record is complete: nothing else applies."
 },
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
  "qid": "qc8cf7635c0",
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
  "qid": "q19c9b29a8f",
  "kind": "yes/no",
  "text": "---\n# record\ndeploy_id: \"DEP-8080\"\nservice: \"billing\"\ncontract_customer_asked_for_a_say_in_this_rollout: false\nbackout_plan_documented: true\ndeploy_title_written_in_normal_case: true\ncommit_messages_written_in_a_terse_style: false\ncanary_results_incomplete: false\ncommit_messages_written_in_a_casual_tone: true\ndeploy_blocked_by_security_policy: false\nrollout_approval_revoked: false\nfiles_changed: 1\ndeploy_has_a_long_description: false\ndeploy_prohibited_during_the_audit_window: false\nservice_free_of_major_incidents: true\nfiles_changed_soft_limit: 15",
  "question": "Proposed action: put on hold\nTell me straight, is the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_documented is false or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- put on hold: keep waiting for the missing details\n- turn down: ditch the whole thing, nobody should act on it\n- go ahead: keep going exactly as requested because every obstacle has cleared\n- send to a person: kick it up to whoever makes the call\nThe record is complete: nothing else applies."
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
 }
]
