# G5-H blind read T46-blind_read-2b82a0e9-001 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r7a/T46/qc/g5h/answers/T46-blind_read-2b82a0e9-001.json

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
  "qid": "q1c4c177384",
  "kind": "yes/no",
  "text": "{\n    \"request\": {\n        \"request_id\": \"REQ-4105\",\n        \"requester\": \"Paolo Castell\"\n    },\n    \"figures\": {\n        \"access_days\": 24,\n        \"access_days_approval_threshold\": 90\n    },\n    \"checks\": {\n        \"account_suspended\": false,\n        \"requested_role_permitted_by_policy\": true,\n        \"request_free_of_ethics_office_flags\": true,\n        \"business_justification_provided\": true,\n        \"request_text_written_in_capital_letters\": false,\n        \"legal_preservation_order_on_the_account\": false,\n        \"mfa_enrollment_complete\": false,\n        \"requester_barred_from_this_system\": false,\n        \"request_grants_admin_rights\": false\n    }\n}",
  "question": "Proposed action: pend\nDo the record's facts rule out the proposed action entirely?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer to owner if request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n2. pend if mfa_enrollment_complete is false.\n3. refuse if business_justification_provided is false or account_suspended is true or requested_role_permitted_by_policy is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\nOtherwise: grant.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- pend: be paused until a document has been received\n- grant: go ahead and the requester will be served\n- refer to owner: pass it on so the asker gets a final answer from the owner\n- refuse: block this from going any further\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q638f6de41c",
  "kind": "yes/no",
  "text": "ticket_id: TCK-2805\ncustomer: Sana Keller\nfree_of_safety_incident_reports: false\nproof_of_purchase_attached: true\nclaim_amount_hard_limit: 2000.00\nitem_excluded_by_policy: true\nitem_return_received: true\nharmless_greeting_present_in_the_message: true\nclaim_involves_a_media_inquiry: false\nclaim_amount: 1388.92\nfree_of_legal_complaints: true\nclaim_form_filled_in_with_the_usual_font: true\nclaim_free_of_ombudsman_cases: true",
  "question": "Proposed action: approve\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false.\n2. deny if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_received is false.\nOtherwise: approve.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5846e61d07",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-8824\", \"vendor\": \"Riverbend Foods\", \"vendor_tax_form_missing\": true, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"amount_approval_threshold\": 25000.00, \"approver_free_of_conflicts_of_interest\": true, \"payment_requested_during_business_hours\": true, \"vendor_free_of_sanctions\": true, \"awaiting_purchase_order\": false, \"duplicate_of_paid_invoice\": false, \"vendor_name_written_in_capital_letters\": false, \"invoice_pdf_uses_a_landscape_layout\": false, \"amount\": 23943.73}",
  "question": "Proposed action: defer\nDoes the proposed action not fit what this request needs?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qf73a626e74",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n    request_id: REQ-9871\n    requester: Ravi Adeyemi\namounts:\n    access_days_approval_threshold: 7\n    access_days: 1\nchecks:\n    legal_preservation_order_on_the_account: false\n    requester_not_barred_from_this_system: true\n    account_suspended: false\n    request_text_written_in_capital_letters: false\n    business_justification_provided: false\n    request_grants_admin_rights: false\n    mfa_enrollment_incomplete: false\n    requested_role_forbidden_by_policy: false\n    request_free_of_ethics_office_flags: true",
  "question": "The record is complete: nothing else applies.\n\nWhat would a careful auditor select from the actions listed for this request?",
  "options": [
   "refer_to_owner",
   "pend",
   "grant"
  ]
 },
 {
  "qid": "q6c0a2598dd",
  "kind": "choice",
  "text": "invoice_id: INV-9827\nvendor: Lakeshore Group\namount: 437.54\namount_approval_threshold: 1000.00\npurchase_order_received: true\ninvoice_pdf_uses_a_landscape_layout: false\nvendor_name_written_in_capital_letters: false\nvendor_tax_form_missing: true\napprover_free_of_conflicts_of_interest: true\nvendor_filed_a_legal_claim_over_this_invoice: false\nduplicate_of_paid_invoice: false\npayment_requested_during_business_hours: false\nvendor_on_sanctions_list: false",
  "question": "Meanings:\n- deny: end it so the requester sees their request closed\n- ask manager: bring in the owner who can rule on this\n- defer: wait so the requester can supply more information first\n- approve: run the requested step through\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "defer",
   "deny",
   "approve"
  ]
 },
 {
  "qid": "q0edab13457",
  "kind": "choice",
  "text": "---\ncase:\n    invoice_id: \"INV-1368\"\n    vendor: \"Summit Industries\"\nvalues:\n    amount_approval_threshold: 5000.00\n    amount: 2053.84\ntests:\n    payment_requested_during_business_hours: true\n    invoice_pdf_uses_a_landscape_layout: false\n    duplicate_of_paid_invoice: false\n    awaiting_purchase_order: true\n    approver_free_of_conflicts_of_interest: true\n    vendor_tax_form_missing: false\n    vendor_free_of_sanctions: false\n    vendor_name_written_in_capital_letters: false\n    vendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. turn_down if vendor_free_of_sanctions is false.\n3. send_to_a_person if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: go_ahead.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_free_of_conflicts_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "send_to_a_person",
   "go_ahead",
   "put_on_hold"
  ]
 },
 {
  "qid": "q631fa904f2",
  "kind": "choice",
  "text": "{\n  \"subject\":{\n    \"deploy_id\":\"DEP-3320\",\n    \"service\":\"exporter\"\n  },\n  \"amounts\":{\n    \"files_changed\":21,\n    \"files_changed_soft_limit\":20\n  },\n  \"checks\":{\n    \"deploy_blocked_by_security_policy\":false,\n    \"service_free_of_major_incidents\":true,\n    \"commit_messages_written_in_a_detailed_style\":true,\n    \"contract_customer_asked_for_a_say_in_this_rollout\":false,\n    \"deploy_has_a_long_description\":false,\n    \"deploy_prohibited_during_the_audit_window\":false,\n    \"canary_results_incomplete\":false,\n    \"rollout_approval_revoked\":false,\n    \"backout_plan_missing\":false\n  }\n}",
  "question": "Meanings:\n- LPN: move ahead on the request in the form it arrived since the path is open\n- GP: send it up to the person who makes the call\n- F: be blocked outright so it never gets carried out\n- JPXP: wait for that check then we will see\nThe record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "F",
   "LPN",
   "JPXP"
  ]
 },
 {
  "qid": "qc8c2392db0",
  "kind": "yes/no",
  "text": "{\"request_id\": \"REQ-7564\", \"requester\": \"Jonas Okafor\", \"mfa_enrollment_complete\": true, \"account_suspended\": false, \"legal_preservation_order_on_the_account\": false, \"request_text_written_in_capital_letters\": false, \"access_days_approval_threshold\": 7, \"access_days\": 1, \"requester_barred_from_this_system\": false, \"business_justification_provided\": true, \"ethics_office_flagged_the_request\": false, \"requested_role_permitted_by_policy\": true, \"request_grants_admin_rights\": false}",
  "question": "Proposed action: pend\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qc8efbccb1e",
  "kind": "choice",
  "text": "# record\nticket_id=TCK-8124\ncustomer=Nadia Adeyemi\nclaim_form_filled_in_with_the_usual_font=true\nclaim_amount=1000.00\nitem_return_not_yet_received=true\nfree_of_legal_complaints=true\nitem_excluded_by_policy=false\nclaim_free_of_ombudsman_cases=true\nclaim_involves_a_media_inquiry=false\nharmless_greeting_present_in_the_message=true\nproof_of_purchase_attached=true\nclaim_amount_hard_limit=1000.00\nfree_of_safety_incident_reports=true",
  "question": "Meanings:\n- ask_manager: be handed over to the deciding person\n- deny: refuse to act since the step is prohibited\n- approve: keep going exactly as requested because every obstacle has cleared\n- defer: withhold action until supporting information is supplied\nThe record is complete: nothing else applies.\n\nFrom the actions listed after this, which is the correct call for the request?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "qb6076a0e4b",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n* run id: RUN-1777\n* agent: jasper\n* task description complete: yes\n* action free of ethics concerns: no\n* last tool output verified: yes\n* action forbidden by security policy: no\n* owner sign off required for this action: no\n* steps used: 59\n* steps used hard limit: 60\n* tool output shows tampering: no\n* log lines written in a compact style: yes",
  "question": "Proposed action: turn_down\nDoes the evidence in the record rule out the proposed action as a choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if last_tool_output_verified is false or action_free_of_ethics_concerns is false.\n2. turn_down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is at least steps_used_hard_limit.\n3. send_to_a_person if task_description_complete is false or owner_sign_off_required_for_this_action is true.\nOtherwise: go_ahead.\nNever counted: log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6e3b2d9e16",
  "kind": "yes/no",
  "text": "---\nrequest:\n  deploy_id: DEP-5255\n  service: checkout\nfigures:\n  files_changed_soft_limit: 50\n  files_changed: 20\nchecks:\n  commit_messages_written_in_a_detailed_style: true\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  rollout_approval_revoked: false\n  deploy_has_a_long_description: true\n  deploy_prohibited_during_the_audit_window: false\n  deploy_blocked_by_security_policy: false\n  service_free_of_major_incidents: true\n  canary_results_incomplete: true\n  backout_plan_missing: false",
  "question": "Proposed action: go ahead\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_missing is true or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style.\nMeanings:\n- go ahead: go on and finish it the path is clear\n- send to a person: escalate the matter to the accountable decision maker\n- turn down: halt this item because the rules forbid it\n- put on hold: pump the brakes until more details show up\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3228a3ba87",
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
  "qid": "q021d6d8cbd",
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
  "qid": "qbf8848fe76",
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
  "qid": "q30047468c4",
  "kind": "yes/no",
  "text": "{\n    \"subject\":{\n        \"invoice_id\":\"INV-9551\",\n        \"vendor\":\"Riverbend Systems\"\n    },\n    \"amounts\":{\n        \"amount\":591.08,\n        \"amount_approval_threshold\":1000.00\n    },\n    \"checks\":{\n        \"vendor_name_written_in_capital_letters\":false,\n        \"invoice_pdf_uses_a_landscape_layout\":true,\n        \"purchase_order_received\":true,\n        \"approver_free_of_conflicts_of_interest\":true,\n        \"vendor_free_of_sanctions\":true,\n        \"duplicate_of_paid_invoice\":false,\n        \"vendor_tax_form_missing\":false,\n        \"payment_requested_during_business_hours\":true,\n        \"vendor_filed_a_legal_claim_over_this_invoice\":false\n    }\n}",
  "question": "Proposed action: approve\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if vendor_filed_a_legal_claim_over_this_invoice is true or approver_free_of_conflicts_of_interest is false or amount is at least amount_approval_threshold.\n2. defer if purchase_order_received is false or vendor_tax_form_missing is true.\n3. deny if duplicate_of_paid_invoice is true.\nOtherwise: approve.\nNever counted: vendor_free_of_sanctions, payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- deny: block it right away\n- ask_manager: escalate this to the person who decides\n- approve: continue with the request as nothing obstructs it\n- defer: sit on it till the doc shows up\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q11fcd214c3",
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
  "qid": "q75dbedf478",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-8349\n- vendor: Stonebridge Systems\n- approver free of conflicts of interest: yes\n- amount approval threshold: 2500.00\n- duplicate of paid invoice: no\n- vendor filed a legal claim over this invoice: no\n- vendor tax form missing: no\n- invoice pdf uses a landscape layout: no\n- vendor on sanctions list: no\n- payment requested during business hours: yes\n- vendor name written in capital letters: no\n- amount: 336.01\n- purchase order received: no",
  "question": "Proposed action: put on hold\nLooking at what the record says, is the proposed action a good fit for the request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qfa2906af64",
  "kind": "yes/no",
  "text": "# request record\nrequest_id = REQ-7564\nrequester = Jonas Okafor\nrequested_role_permitted_by_policy = true\nrequest_text_written_in_capital_letters = false\nbusiness_justification_provided = true\nrequest_grants_admin_rights = false\naccess_days = 1\nlegal_preservation_order_on_the_account = false\naccount_suspended = false\nethics_office_flagged_the_request = false\nmfa_enrollment_complete = true\naccess_days_approval_threshold = 7\nrequester_barred_from_this_system = false",
  "question": "Proposed action: pend\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q01f9a4698c",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-9431\n- vendor: Oakmont Partners\n- duplicate of paid invoice: no\n- approver declared a conflict of interest: yes\n- amount: 1345.40\n- vendor free of sanctions: yes\n- vendor name written in capital letters: no\n- payment requested during business hours: yes\n- invoice pdf uses a portrait layout: yes\n- amount approval threshold: 2500.00\n- awaiting purchase order: no\n- vendor filed a legal claim over this invoice: no\n- vendor tax form missing: yes",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. escalate if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. reject if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\nOtherwise: pay.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nLooking at this case file, which of the actions listed is the right call?",
  "options": [
   "escalate",
   "pay",
   "reject"
  ]
 },
 {
  "qid": "q2390045f4c",
  "kind": "choice",
  "text": "# case\ndeploy_id: DEP-4631\nservice: pricing\nfiles_changed: 3\nfiles_changed_soft_limit: 10\nbackout_plan_documented: true\ncommit_messages_written_in_a_detailed_style: true\nservice_free_of_major_incidents: true\ndeploy_prohibited_during_the_audit_window: false\nrollout_approval_revoked: false\ncanary_results_complete: true\ndeploy_blocked_by_security_policy: false\ncontract_customer_asked_for_a_say_in_this_rollout: true\ndeploy_has_a_long_description: false",
  "question": "Meanings:\n- 597: shut off this process completely\n- 15: keep going with it nothing is blocking you\n- 8: send it to whoever has the final say\n- 4090: sit on it till the doc shows up\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the most suitable for the request?",
  "options": [
   "4090",
   "8",
   "15"
  ]
 },
 {
  "qid": "q207d4f60fb",
  "kind": "yes/no",
  "text": "{\n  \"run_id\":\"RUN-2726\",\n  \"agent\":\"kestrel\",\n  \"steps_used_hard_limit\":20,\n  \"last_tool_output_verified\":true,\n  \"owner_sign_off_required_for_this_action\":false,\n  \"action_free_of_ethics_concerns\":true,\n  \"task_description_incomplete\":false,\n  \"action_forbidden_by_security_policy\":false,\n  \"log_lines_written_in_a_compact_style\":false,\n  \"steps_used\":15,\n  \"tool_output_shows_tampering\":true\n}",
  "question": "Proposed action: send_to_a_person\nIs it not so that the proposed action, per what is logged, is not a bad fit?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if owner_sign_off_required_for_this_action is true.\n2. turn_down if action_forbidden_by_security_policy is true.\n3. put_on_hold if last_tool_output_verified is false or task_description_incomplete is true or action_free_of_ethics_concerns is false or steps_used is above steps_used_hard_limit.\nOtherwise: go_ahead.\nNever counted: tool_output_shows_tampering, log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1320cd6a77",
  "kind": "yes/no",
  "text": "# extract\nrun_id                                  | RUN-1759\nagent                                   | garnet\naction_permitted_by_security_policy     | true\ntool_output_shows_tampering             | false\nlast_tool_output_verified               | true\ntask_description_incomplete             | false\nsteps_used_hard_limit                   | 30\nowner_sign_off_required_for_this_action | false\naction_free_of_ethics_concerns          | true\nsteps_used                              | 3\nlog_lines_written_in_a_verbose_style    | false",
  "question": "Proposed action: turn_down\nIs it not so that the proposed action we have on the table is not a poor choice for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if owner_sign_off_required_for_this_action is true.\n2. turn_down if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is above steps_used_hard_limit.\n3. put_on_hold if last_tool_output_verified is false.\nOtherwise: go_ahead.\nNever counted: task_description_incomplete, action_free_of_ethics_concerns, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q12290097cc",
  "kind": "choice",
  "text": "# record\nrequest_id: REQ-4268\nrequester: Samir Okonkwo\naccess_days: 60\nbusiness_justification_provided: true\nrequest_grants_admin_rights: false\nlegal_preservation_order_on_the_account: false\nrequest_text_written_in_capital_letters: false\nmfa_enrollment_complete: true\nrequest_free_of_ethics_office_flags: true\nrequester_barred_from_this_system: true\naccount_suspended: false\nrequested_role_permitted_by_policy: true\naccess_days_approval_threshold: 60",
  "question": "Meanings:\n- defer: withhold action until supporting information is supplied\n- ask manager: delegate the call to whoever holds authority\n- deny: halt this item because the rules forbid it\n- approve: complete the action that was asked for\nThe record is complete: nothing else applies.\n\nIn this case file, which of the listed actions is the correct decision?",
  "options": [
   "deny",
   "defer",
   "approve"
  ]
 },
 {
  "qid": "q06d45dbfcd",
  "kind": "yes/no",
  "text": "{\n    \"ticket_id\": \"TCK-2252\",\n    \"customer\": \"Sana Mensah\",\n    \"item_excluded_by_policy\": false,\n    \"claim_involves_a_media_inquiry\": false,\n    \"claim_amount\": 34.30,\n    \"item_return_not_yet_received\": false,\n    \"harmless_greeting_present_in_the_message\": true,\n    \"free_of_legal_complaints\": true,\n    \"claim_amount_hard_limit\": 50.00,\n    \"proof_of_purchase_missing\": false,\n    \"free_of_safety_incident_reports\": true,\n    \"claim_free_of_ombudsman_cases\": true,\n    \"claim_form_filled_in_with_the_usual_font\": true\n}",
  "question": "Proposed action: ask manager\nWould the facts and the request as written rule out the proposed action?",
  "definitions": "Meanings:\n- defer: keep waiting for the missing details\n- approve: complete the job as it was assigned\n- ask manager: be passed along to whoever makes the call\n- deny: end this here and now\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1961bf89b7",
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
  "qid": "q47677fed22",
  "kind": "choice",
  "text": "Ticket extract, checks answered with yes or no\n- run id: RUN-9115\n- agent: indigo\n- log lines written in a compact style: yes\n- action free of ethics concerns: yes\n- last tool output unverified: no\n- task description incomplete: yes\n- tool output shows tampering: no\n- owner sign off required for this action: no\n- steps used: 4\n- action forbidden by security policy: no\n- steps used hard limit: 8",
  "question": "Meanings:\n- go ahead: allow the matter to be taken forward as planned\n- put on hold: wait until a document arrives before you move forward with it\n- send to a person: hand the matter to a decider so the requester gets a verdict\n- turn down: shut off this process completely\nThe record is complete: nothing else applies.\n\nLooking at this case file, which of the actions listed is the right call?",
  "options": [
   "put on hold",
   "turn down",
   "go ahead"
  ]
 },
 {
  "qid": "q7a8fe673fc",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- ticket id: TCK-8545\n- customer: لمى سهيل الإدريسي\n- note: جميع البيانات المقدمة من العميل واضحة وصحيحة.\n- claim amount hard limit: 100.00\n- item excluded by policy: no\n- item return not yet received: no\n- claim involves a media inquiry: no\n- claim form filled in with the usual font: yes\n- proof of purchase missing: no\n- free of safety incident reports: yes\n- claim free of ombudsman cases: yes\n- harmless greeting present in the message: no\n- free of legal complaints: yes\n- claim amount: 100.01",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. put_on_hold if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\n3. send_to_a_person if item_return_not_yet_received is true or free_of_legal_complaints is false or free_of_safety_incident_reports is false.\nOtherwise: go_ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nReading the file for this case, which listed action is the best call?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "turn_down"
  ]
 },
 {
  "qid": "qbdfb887c5c",
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
  "qid": "qbbd014f9a2",
  "kind": "choice",
  "text": "---\n# record\nrun_id: \"RUN-5197\"\nagent: \"indigo\"\nlast_tool_output_verified: true\naction_forbidden_by_security_policy: false\ntask_description_complete: true\nowner_sign_off_required_for_this_action: false\nsteps_used: 6\nlog_lines_written_in_a_verbose_style: true\ntool_output_shows_tampering: false\naction_free_of_ethics_concerns: false\nsteps_used_hard_limit: 16",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put_on_hold if last_tool_output_verified is false or task_description_complete is false.\n3. turn_down if action_forbidden_by_security_policy is true or owner_sign_off_required_for_this_action is true or steps_used is above steps_used_hard_limit.\nOtherwise: go_ahead.\nNever counted: log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies.\n\nLooking at the request, which action from the list should be taken?",
  "options": [
   "send_to_a_person",
   "go_ahead",
   "put_on_hold"
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
  "qid": "qa8d4e7521b",
  "kind": "yes/no",
  "text": "{\"request_id\": \"REQ-5172\", \"requester\": \"Marta Imai\", \"business_justification_provided\": true, \"requested_role_permitted_by_policy\": true, \"mfa_enrollment_complete\": true, \"legal_preservation_order_on_the_account\": false, \"access_days\": 70, \"account_suspended\": false, \"request_free_of_ethics_office_flags\": true, \"request_grants_admin_rights\": false, \"access_days_approval_threshold\": 90, \"request_text_written_in_capital_letters\": false, \"requester_barred_from_this_system\": false}",
  "question": "Proposed action: deny\nIs the proposed action not what should happen with this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if business_justification_provided is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. ask manager if mfa_enrollment_complete is false or request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n3. deny if account_suspended is true or requested_role_permitted_by_policy is false.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q9a783815a5",
  "kind": "yes/no",
  "text": "# extract\nticket_id=TCK-2153\ncustomer=زياد نبيل الدوسري\nnote=الحالة بسيطة ومكتملة ولا تحتاج إلى تدخل إضافي.\nclaim_form_filled_in_with_the_usual_font=true\nclaim_involves_a_media_inquiry=false\nclaim_free_of_ombudsman_cases=true\nfree_of_safety_incident_reports=true\nitem_excluded_by_policy=false\nharmless_greeting_present_in_the_message=false\nlegal_complaint_filed=false\nclaim_amount_hard_limit=200.00\nclaim_amount=153.76\nproof_of_purchase_missing=false\nitem_return_received=true",
  "question": "Proposed action: send_to_a_person\nBe honest, is the proposed action the right call for what came in?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if item_return_received is false or free_of_safety_incident_reports is false.\n2. put_on_hold if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. send_to_a_person if proof_of_purchase_missing is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: go_ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd62a6fad29",
  "kind": "yes/no",
  "text": "{\n  \"record\":{\n    \"request_id\":\"REQ-4526\",\n    \"requester\":\"دينا وائل الأنصاري\",\n    \"note\":\"الوصول المطلوب يتعارض مع فصل المهام المعتمد في المؤسسة.\"\n  },\n  \"numbers\":{\n    \"access_days_approval_threshold\":45,\n    \"access_days\":15\n  },\n  \"flags\":{\n    \"legal_preservation_order_on_the_account\":false,\n    \"mfa_enrollment_complete\":true,\n    \"requested_role_forbidden_by_policy\":false,\n    \"account_suspended\":false,\n    \"request_grants_admin_rights\":false,\n    \"business_justification_provided\":true,\n    \"request_free_of_ethics_office_flags\":true,\n    \"requester_barred_from_this_system\":false,\n    \"request_text_written_in_capital_letters\":false\n  }\n}",
  "question": "Proposed action: block_access\nDoes what we know about this rule out the proposed action?",
  "definitions": "Meanings:\n- quarantine: suspend progress until verification is received\n- allow: proceed with the task as asked\n- page_oncall: bring in the authority who can settle it for the requester\n- block_access: stop the work since it cannot move forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q36736dc5d0",
  "kind": "yes/no",
  "text": "{\n    \"record\":{\n        \"request_id\":\"REQ-1158\",\n        \"requester\":\"Paolo Brandt\"\n    },\n    \"numbers\":{\n        \"access_days_approval_threshold\":90,\n        \"access_days\":5\n    },\n    \"flags\":{\n        \"legal_preservation_order_on_the_account\":false,\n        \"requested_role_permitted_by_policy\":true,\n        \"requester_barred_from_this_system\":false,\n        \"business_justification_missing\":false,\n        \"request_grants_admin_rights\":false,\n        \"request_free_of_ethics_office_flags\":true,\n        \"request_text_written_in_capital_letters\":false,\n        \"mfa_enrollment_complete\":true,\n        \"account_suspended\":false\n    }\n}",
  "question": "Proposed action: 3035\nIs it not the case that the proposed action for this file is not a mistaken move?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 653 if business_justification_missing is true or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. 5 if mfa_enrollment_complete is false or request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n3. 3035 if account_suspended is true or requested_role_permitted_by_policy is false.\nOtherwise: 42.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- 3035: be rejected in full and never acted upon\n- 42: keep going with it nothing is blocking you\n- 5: pass the request to a decider\n- 653: pause and collect more information first\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q895893e6d7",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- ticket id: TCK-7217\n- customer: Anders Imai\n- harmless greeting present in the message: yes\n- claim involves a media inquiry: no\n- item excluded by policy: no\n- claim free of ombudsman cases: yes\n- legal complaint filed: no\n- item return not yet received: yes\n- claim form filled in with the usual font: yes\n- free of safety incident reports: yes\n- claim amount hard limit: 50.00\n- claim amount: 18.33\n- proof of purchase missing: no",
  "question": "Proposed action: put_on_hold\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q22f356af8f",
  "kind": "choice",
  "text": "request_id: REQ-2446\nrequester: Yara Moreau\naccess_days_approval_threshold: 60\nrequest_free_of_ethics_office_flags: true\nmfa_enrollment_incomplete: true\nrequested_role_permitted_by_policy: true\nlegal_preservation_order_on_the_account: false\nrequester_barred_from_this_system: false\naccount_suspended: false\nrequest_text_written_in_capital_letters: true\naccess_days: 69\nbusiness_justification_provided: true\nrequest_grants_admin_rights: false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or request_free_of_ethics_office_flags is false.\n2. deny if account_suspended is true or requested_role_permitted_by_policy is false.\n3. ask_manager if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: approve.\nNever counted: business_justification_provided, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- ask_manager: escalate this to the person who decides\n- approve: keep plugging away at it nothing else stands in the way\n- deny: decline the request as the action is prohibited\n- defer: wait for the missing material to come in before deciding anything\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "deny",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q49d3994338",
  "kind": "yes/no",
  "text": "{\n  \"invoice_id\":\"INV-1395\",\n  \"vendor\":\"Fairview Group\",\n  \"awaiting_purchase_order\":false,\n  \"vendor_tax_form_missing\":false,\n  \"vendor_free_of_sanctions\":true,\n  \"invoice_pdf_uses_a_landscape_layout\":false,\n  \"vendor_filed_a_legal_claim_over_this_invoice\":false,\n  \"duplicate_of_paid_invoice\":false,\n  \"payment_requested_during_business_hours\":true,\n  \"vendor_name_written_in_capital_letters\":false,\n  \"amount_approval_threshold\":1000.00,\n  \"approver_free_of_conflicts_of_interest\":true,\n  \"amount\":725.81\n}",
  "question": "Proposed action: hand_to_a_person\nIs it not the case that the proposed action is what the request and facts call for, and is not a poor choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true.\n2. hand_to_a_person if vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. cancel_order if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or approver_free_of_conflicts_of_interest is false or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- cancel_order: bin this idea and keep it out of the flow\n- release: proceed with the task as asked\n- delay: wait for the document to come through\n- hand_to_a_person: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q3a00247bcc",
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
  "qid": "q23f14e17bb",
  "kind": "yes/no",
  "text": "{\n  \"request\":{\n    \"run_id\":\"RUN-5723\",\n    \"agent\":\"beacon\"\n  },\n  \"figures\":{\n    \"steps_used_hard_limit\":30,\n    \"steps_used\":31\n  },\n  \"checks\":{\n    \"last_tool_output_verified\":true,\n    \"tool_output_shows_tampering\":false,\n    \"owner_sign_off_required_for_this_action\":false,\n    \"task_description_complete\":true,\n    \"action_free_of_ethics_concerns\":true,\n    \"log_lines_written_in_a_compact_style\":false,\n    \"action_forbidden_by_security_policy\":false\n  }\n}",
  "question": "Proposed action: go_ahead\nDoes the record itself rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if owner_sign_off_required_for_this_action is true.\n2. turn_down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is above steps_used_hard_limit.\n3. put_on_hold if last_tool_output_verified is false.\nOtherwise: go_ahead.\nNever counted: task_description_complete, action_free_of_ethics_concerns, log_lines_written_in_a_compact_style.\nMeanings:\n- put_on_hold: park the file until the requester sends the document in\n- send_to_a_person: send it up so the requester gets a firm decision\n- go_ahead: carry on with it now\n- turn_down: refuse to act since the step is prohibited\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q0b990e88f8",
  "kind": "yes/no",
  "text": "{\n    \"request_id\":\"REQ-8173\",\n    \"requester\":\"كنان ياسر الوادي\",\n    \"note\":\"لا توجد ملاحظات على هوية الموظف مقدم الطلب.\",\n    \"account_suspended\":false,\n    \"requester_not_barred_from_this_system\":true,\n    \"request_grants_admin_rights\":false,\n    \"legal_preservation_order_on_the_account\":false,\n    \"access_days\":1,\n    \"business_justification_missing\":false,\n    \"ethics_office_flagged_the_request\":false,\n    \"request_text_written_in_capital_letters\":true,\n    \"access_days_approval_threshold\":60,\n    \"requested_role_permitted_by_policy\":true,\n    \"mfa_enrollment_incomplete\":false\n}",
  "question": "Proposed action: grant\nIs the proposed action the right move for this request, given the facts involved?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer to owner if request_grants_admin_rights is true or ethics_office_flagged_the_request is true or access_days is at least access_days_approval_threshold.\n2. pend if mfa_enrollment_incomplete is true.\n3. refuse if business_justification_missing is true or account_suspended is true or requested_role_permitted_by_policy is false or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\nOtherwise: grant.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- refer to owner: be handed over to the deciding person\n- grant: let the request be continued as originally asked\n- pend: await further verification before any progression\n- refuse: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2f814a0b3d",
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
  "qid": "q61a1d47d36",
  "kind": "yes/no",
  "text": "{\"request_id\": \"REQ-5140\", \"requester\": \"Yara Imai\", \"legal_preservation_order_on_the_account\": false, \"mfa_enrollment_incomplete\": false, \"requested_role_permitted_by_policy\": true, \"business_justification_missing\": false, \"access_days\": 47, \"access_days_approval_threshold\": 90, \"request_grants_admin_rights\": false, \"ethics_office_flagged_the_request\": false, \"request_text_written_in_capital_letters\": false, \"account_suspended\": false, \"requester_barred_from_this_system\": false}",
  "question": "Proposed action: refer to owner\nIs the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. pend if mfa_enrollment_incomplete is true or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\n2. refuse if account_suspended is true or requested_role_permitted_by_policy is false.\n3. refer to owner if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: grant.\nNever counted: business_justification_missing, request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q2a5f0a1cb5",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n* request id: REQ-8068\n* requester: Idris Whitcombe\n* requester barred from this system: no\n* legal preservation order on the account: no\n* business justification missing: no\n* account suspended: no\n* access days: 1\n* mfa enrollment incomplete: no\n* request text written in capital letters: no\n* request grants admin rights: no\n* requested role permitted by policy: yes\n* access days approval threshold: 7\n* request free of ethics office flags: yes",
  "question": "Meanings:\n- refer to owner: refer the matter to the decision holder\n- grant: proceed as asked since everything is cleared\n- pend: defer further action pending verification of the document\n- refuse: be dropped here and not acted upon at all\nThe record is complete: nothing else applies.\n\nReviewing the record, which of the actions below is the right call?",
  "options": [
   "pend",
   "refuse",
   "grant"
  ]
 },
 {
  "qid": "q3015c5aba4",
  "kind": "choice",
  "text": "# request record\nrequest_id                              | REQ-9566\nrequester                               | Ingrid Moreau\nrequest_free_of_ethics_office_flags     | true\nrequest_grants_admin_rights             | false\nlegal_preservation_order_on_the_account | false\nrequester_not_barred_from_this_system   | true\naccess_days_approval_threshold          | 7\nrequested_role_forbidden_by_policy      | false\naccount_suspended                       | true\nmfa_enrollment_incomplete               | false\nbusiness_justification_provided         | true\naccess_days                             | 4\nrequest_text_written_in_capital_letters | false",
  "question": "The record is complete: nothing else applies.\n\nSo which of the actions listed after this question makes sense for the request?",
  "options": [
   "pend",
   "grant",
   "refuse"
  ]
 },
 {
  "qid": "qd8b4f66b1e",
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
  "qid": "qdb860b5b54",
  "kind": "choice",
  "text": "---\nrequest_id: REQ-9731\nrequester: Kofi Adeyemi\nethics_office_flagged_the_request: false\nbusiness_justification_provided: true\naccess_days: 36\nrequest_grants_admin_rights: false\naccess_days_approval_threshold: 30\naccount_suspended: true\nmfa_enrollment_complete: true\nlegal_preservation_order_on_the_account: false\nrequester_barred_from_this_system: false\nrequest_text_written_in_capital_letters: false\nrequested_role_permitted_by_policy: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. block_access if account_suspended is true or requested_role_permitted_by_policy is false or request_grants_admin_rights is true.\n2. page_oncall if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\n3. quarantine if business_justification_provided is false or mfa_enrollment_complete is false or requester_barred_from_this_system is true or ethics_office_flagged_the_request is true.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- quarantine: be kept on hold until more information is supplied\n- allow: complete the job as it was assigned\n- block_access: veto this move and leave it there\n- page_oncall: transfer the case to the responsible decision maker for determination\nThe record is complete: nothing else applies.\n\nBased on what the record shows, which of the actions listed is the right call?",
  "options": [
   "quarantine",
   "page_oncall",
   "block_access"
  ]
 },
 {
  "qid": "qc56125dd65",
  "kind": "choice",
  "text": "# request record\nticket_id: TCK-8344\ncustomer: Dana Sorensen\nclaim_free_of_ombudsman_cases: true\nproof_of_purchase_attached: true\nharmless_greeting_present_in_the_message: true\nclaim_amount: 721.30\nitem_excluded_by_policy: true\nlegal_complaint_filed: false\nitem_return_received: true\nfree_of_safety_incident_reports: true\nclaim_involves_a_media_inquiry: false\nclaim_form_filled_in_with_the_usual_font: true\nclaim_amount_hard_limit: 1000.00",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if claim_amount is at least claim_amount_hard_limit.\n2. send_to_a_person if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. put_on_hold if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: go_ahead.\nNever counted: item_return_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- turn_down: shut this down fast\n- put_on_hold: sit on it till the doc shows up\n- go_ahead: carry out the request as written\n- send_to_a_person: route it elsewhere because a decider must weigh in\nThe record is complete: nothing else applies.\n\nThe request describes a situation; which of the actions underneath handles it correctly?",
  "options": [
   "send_to_a_person",
   "turn_down",
   "put_on_hold"
  ]
 },
 {
  "qid": "q31faf59e9f",
  "kind": "choice",
  "text": "{\"run_id\": \"RUN-5054\", \"agent\": \"helix\", \"owner_sign_off_required_for_this_action\": false, \"action_forbidden_by_security_policy\": false, \"action_free_of_ethics_concerns\": true, \"steps_used_hard_limit\": 60, \"task_description_incomplete\": false, \"tool_output_shows_tampering\": false, \"last_tool_output_unverified\": false, \"steps_used\": 18, \"log_lines_written_in_a_compact_style\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn_down if tool_output_shows_tampering is true or action_free_of_ethics_concerns is false.\n2. put_on_hold if task_description_incomplete is true or steps_used is above steps_used_hard_limit.\n3. send_to_a_person if action_forbidden_by_security_policy is true or owner_sign_off_required_for_this_action is true.\nOtherwise: go_ahead.\nNever counted: last_tool_output_unverified, log_lines_written_in_a_compact_style.\nMeanings:\n- send_to_a_person: direct the request to the responsible decider\n- go_ahead: keep it moving forward\n- put_on_hold: hold the request so the requester waits for their check\n- turn_down: make sure the requester never gets what they wanted\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "put_on_hold",
   "send_to_a_person",
   "go_ahead"
  ]
 },
 {
  "qid": "qb57743c407",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-7020\n- vendor: Riverbend Partners\n- duplicate of paid invoice: no\n- awaiting purchase order: no\n- vendor tax form missing: no\n- vendor filed a legal claim over this invoice: no\n- payment requested during business hours: yes\n- approver free of conflicts of interest: yes\n- vendor name written in capital letters: no\n- invoice pdf uses a landscape layout: no\n- amount approval threshold: 500.00\n- vendor on sanctions list: no\n- amount: 462.53",
  "question": "The record is complete: nothing else applies.\n\nWhich of the actions below answers the request given the facts you can see?",
  "options": [
   "reject",
   "escalate",
   "pay"
  ]
 },
 {
  "qid": "qe56404f23b",
  "kind": "choice",
  "text": "{\"ticket_id\": \"TCK-2025\", \"customer\": \"Jonas Haddad\", \"item_return_not_yet_received\": false, \"item_excluded_by_policy\": true, \"claim_free_of_ombudsman_cases\": true, \"claim_involves_a_media_inquiry\": false, \"proof_of_purchase_attached\": true, \"claim_amount\": 92.81, \"free_of_safety_incident_reports\": true, \"claim_amount_hard_limit\": 100.00, \"harmless_greeting_present_in_the_message\": true, \"free_of_legal_complaints\": true, \"claim_form_filled_in_with_the_usual_font\": true}",
  "question": "Meanings:\n- 2: shelve the matter until more details come in\n- 6404: refer the matter to the decision holder\n- 550: continue so the requester receives the result\n- 71: end this effort right away\nThe record is complete: nothing else applies.\n\nWhich of the listed actions do the facts support as the right call?",
  "options": [
   "71",
   "550",
   "6404"
  ]
 }
]
