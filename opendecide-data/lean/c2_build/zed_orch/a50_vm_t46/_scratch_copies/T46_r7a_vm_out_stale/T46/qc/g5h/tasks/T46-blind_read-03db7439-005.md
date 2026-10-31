# G5-H blind read T46-blind_read-03db7439-005 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r7a/T46/qc/g5h/answers/T46-blind_read-03db7439-005.json

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
  "qid": "qafd09e7416",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n- invoice id: INV-2851\n- vendor: Oakmont Logistics\n- amount approval threshold: 1000.00\n- purchase order received: yes\n- amount: 509.48\n- payment requested during business hours: yes\n- vendor free of sanctions: yes\n- approver free of conflicts of interest: no\n- vendor tax form missing: no\n- invoice pdf uses a landscape layout: yes\n- duplicate of paid invoice: no\n- vendor filed a legal claim over this invoice: no\n- vendor name written in capital letters: yes",
  "question": "The record is complete: nothing else applies.\n\nReview step: which of the actions listed below matches the request as recorded?",
  "options": [
   "turn down",
   "send to a person",
   "put on hold"
  ]
 },
 {
  "qid": "q0efcb55c59",
  "kind": "yes/no",
  "text": "# request record\nticket_id: TCK-6395\ncustomer: Ravi Ferreira\nclaim_involves_a_media_inquiry: false\nclaim_free_of_ombudsman_cases: true\nharmless_greeting_present_in_the_message: true\nitem_excluded_by_policy: false\nitem_return_received: true\nfree_of_legal_complaints: true\nclaim_form_filled_in_with_the_usual_font: true\nclaim_amount: 1000.01\nproof_of_purchase_missing: false\nclaim_amount_hard_limit: 1000.00\nfree_of_safety_incident_reports: true",
  "question": "Proposed action: go_ahead\nIs it not correct that the evidence points toward the proposed action, and it is not a poor choice?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q045e6ef355",
  "kind": "yes/no",
  "text": "# record\nticket_id | TCK-1104\ncustomer | Elena Castell\nclaim_amount_hard_limit | 1000.00\nfree_of_safety_incident_reports | true\nclaim_form_filled_in_with_the_usual_font | true\nclaim_free_of_ombudsman_cases | true\nclaim_amount | 320.07\nclaim_involves_a_media_inquiry | false\nitem_excluded_by_policy | false\nharmless_greeting_present_in_the_message | false\nitem_return_received | true\nproof_of_purchase_missing | false\nlegal_complaint_filed | true",
  "question": "Proposed action: send to a person\nIs the proposed action correct for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if claim_amount is at least claim_amount_hard_limit.\n2. send to a person if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. put on hold if proof_of_purchase_missing is true or item_excluded_by_policy is true.\nOtherwise: go ahead.\nNever counted: item_return_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qfe1fa9d21d",
  "kind": "yes/no",
  "text": "{\n    \"request_id\":\"REQ-8173\",\n    \"requester\":\"كنان ياسر الوادي\",\n    \"note\":\"لا توجد ملاحظات على هوية الموظف مقدم الطلب.\",\n    \"account_suspended\":false,\n    \"requester_not_barred_from_this_system\":true,\n    \"request_grants_admin_rights\":false,\n    \"legal_preservation_order_on_the_account\":false,\n    \"access_days\":1,\n    \"business_justification_missing\":false,\n    \"ethics_office_flagged_the_request\":false,\n    \"request_text_written_in_capital_letters\":true,\n    \"access_days_approval_threshold\":60,\n    \"requested_role_permitted_by_policy\":true,\n    \"mfa_enrollment_incomplete\":false\n}",
  "question": "Proposed action: grant\nIs the proposed action the right move for this request, given the facts involved?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer to owner if request_grants_admin_rights is true or ethics_office_flagged_the_request is true or access_days is at least access_days_approval_threshold.\n2. pend if mfa_enrollment_incomplete is true.\n3. refuse if business_justification_missing is true or account_suspended is true or requested_role_permitted_by_policy is false or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\nOtherwise: grant.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- refer to owner: be handed over to the deciding person\n- grant: let the request be continued as originally asked\n- pend: await further verification before any progression\n- refuse: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qc5ffea1c12",
  "kind": "choice",
  "text": "---\n# request record\nsubject:\n  run_id: \"RUN-8665\"\n  agent: \"kestrel\"\namounts:\n  steps_used_hard_limit: 20\n  steps_used: 20\nchecks:\n  last_tool_output_verified: false\n  task_description_complete: true\n  tool_output_shows_tampering: false\n  action_free_of_ethics_concerns: true\n  log_lines_written_in_a_compact_style: true\n  action_forbidden_by_security_policy: false\n  owner_sign_off_required_for_this_action: false",
  "question": "Meanings:\n- turn_down: refuse to act since the step is prohibited\n- send_to_a_person: send it up so the requester gets a firm decision\n- put_on_hold: hold off until more information arrives\n- go_ahead: carry out the task as instructed without any obstacle\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "send_to_a_person"
  ]
 },
 {
  "qid": "q82533cd532",
  "kind": "choice",
  "text": "# case\nrun_id                                  | RUN-9564\nagent                                   | helix\nlast_tool_output_verified               | true\nlog_lines_written_in_a_compact_style    | true\nsteps_used_hard_limit                   | 30\ntool_output_shows_tampering             | false\nowner_sign_off_required_for_this_action | false\naction_permitted_by_security_policy     | true\naction_free_of_ethics_concerns          | true\nsteps_used                              | 31\ntask_description_incomplete             | false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if action_free_of_ethics_concerns is false or steps_used is above steps_used_hard_limit.\n2. put_on_hold if owner_sign_off_required_for_this_action is true.\n3. turn_down if task_description_incomplete is true or tool_output_shows_tampering is true or action_permitted_by_security_policy is false.\nOtherwise: go_ahead.\nNever counted: last_tool_output_verified, log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies.\n\nFrom an audit standpoint, which of the actions listed is the appropriate call here?",
  "options": [
   "go_ahead",
   "send_to_a_person",
   "put_on_hold"
  ]
 },
 {
  "qid": "q470380dfee",
  "kind": "choice",
  "text": "---\n# request record\ninvoice_id: \"INV-8224\"\nvendor: \"Harbor Traders\"\nvendor_name_written_in_capital_letters: false\ninvoice_pdf_uses_a_portrait_layout: true\nvendor_on_sanctions_list: false\namount: 1869.80\namount_approval_threshold: 5000.00\nvendor_tax_form_on_file: true\nawaiting_purchase_order: false\npayment_requested_during_business_hours: true\nvendor_filed_a_legal_claim_over_this_invoice: false\nduplicate_of_paid_invoice: false\napprover_free_of_conflicts_of_interest: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "reject",
   "escalate",
   "pay"
  ]
 },
 {
  "qid": "q377d508884",
  "kind": "choice",
  "text": "---\n# case\nsubject:\n    request_id: REQ-3142\n    requester: Zoe Sorensen\namounts:\n    access_days: 45\n    access_days_approval_threshold: 45\nchecks:\n    request_text_written_in_capital_letters: true\n    request_grants_admin_rights: false\n    requested_role_permitted_by_policy: true\n    ethics_office_flagged_the_request: false\n    mfa_enrollment_complete: true\n    requester_not_barred_from_this_system: true\n    business_justification_provided: false\n    account_suspended: false\n    legal_preservation_order_on_the_account: false",
  "question": "Meanings:\n- MDZQ: halt the request at this point\n- NHZ: be left pending until the review has been finished\n- Q: forward the matter as the call rests with someone higher\n- NT: proceed and the requester gets what they asked\nThe record is complete: nothing else applies.\n\nWith reference to the record, which of the actions listed below is the appropriate course for the request?",
  "options": [
   "Q",
   "NT",
   "NHZ"
  ]
 },
 {
  "qid": "q1688cd7e2e",
  "kind": "choice",
  "text": "{\"invoice_id\":\"INV-4455\",\"vendor\":\"Brightwater Systems\",\"vendor_name_written_in_capital_letters\":false,\"vendor_free_of_sanctions\":true,\"invoice_pdf_uses_a_portrait_layout\":true,\"purchase_order_received\":true,\"approver_free_of_conflicts_of_interest\":true,\"duplicate_of_paid_invoice\":false,\"amount_approval_threshold\":5000.00,\"vendor_tax_form_missing\":false,\"payment_requested_during_business_hours\":true,\"vendor_filed_a_legal_claim_over_this_invoice\":false,\"amount\":4196.47}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if vendor_filed_a_legal_claim_over_this_invoice is true.\n2. cancel order if duplicate_of_paid_invoice is true.\n3. hand to a person if vendor_free_of_sanctions is false or approver_free_of_conflicts_of_interest is false or amount is at least amount_approval_threshold.\nOtherwise: release.\nNever counted: purchase_order_received, vendor_tax_form_missing, payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nGiven the request and the facts stated, which of the actions listed is the right call?",
  "options": [
   "cancel order",
   "delay",
   "release"
  ]
 },
 {
  "qid": "q54db1abc28",
  "kind": "choice",
  "text": "---\n# request record\ninvoice_id: \"INV-6927\"\nvendor: \"Northwind Works\"\nvendor_filed_a_legal_claim_over_this_invoice: false\npayment_requested_during_business_hours: true\napprover_free_of_conflicts_of_interest: true\namount: 172.58\nvendor_name_written_in_capital_letters: false\nduplicate_of_paid_invoice: false\nvendor_tax_form_on_file: false\nvendor_on_sanctions_list: false\namount_approval_threshold: 1000.00\npurchase_order_received: true\ninvoice_pdf_uses_a_landscape_layout: false",
  "question": "Meanings:\n- SKCS: withhold action until supporting information is supplied\n- JQ: ditch the whole thing, nobody should act on it\n- JQL: hand this to the person who decides\n- J: press on with the work as originally set\nThe record is complete: nothing else applies.\n\nWhich of these actions should be taken for this request?",
  "options": [
   "SKCS",
   "JQL",
   "JQ"
  ]
 },
 {
  "qid": "q223207a1d1",
  "kind": "yes/no",
  "text": "# record\ndeploy_id=DEP-3263\nservice=notifier\ncanary_results_complete=false\nfiles_changed=7\ndeploy_prohibited_during_the_audit_window=false\nrollout_approval_revoked=true\ncommit_messages_written_in_a_terse_style=false\ndeploy_has_a_long_description=false\ncontract_customer_asked_for_a_say_in_this_rollout=true\nservice_free_of_major_incidents=true\nbackout_plan_documented=true\nfiles_changed_soft_limit=80\ndeploy_blocked_by_security_policy=false",
  "question": "Proposed action: HDW\nSo, have the facts in the record ruled out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. HDW if canary_results_complete is false.\n2. LB if rollout_approval_revoked is true.\n3. L if backout_plan_documented is false or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\nOtherwise: XNNS.\nNever counted: deploy_has_a_long_description, deploy_blocked_by_security_policy, service_free_of_major_incidents, contract_customer_asked_for_a_say_in_this_rollout, commit_messages_written_in_a_terse_style.\nMeanings:\n- LB: kill this one off, it is off the table for good\n- XNNS: have the plan kept moving as it was requested\n- HDW: be forwarded to the person in charge\n- L: pause and collect more information first\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb0c1fa4e2b",
  "kind": "choice",
  "text": "# request record\nrun_id=RUN-8556\nagent=ember\nowner_sign_off_required_for_this_action=false\nlast_tool_output_verified=true\ntool_output_shows_tampering=false\naction_free_of_ethics_concerns=false\ntask_description_complete=true\naction_forbidden_by_security_policy=false\nlog_lines_written_in_a_compact_style=true\nsteps_used=59\nsteps_used_hard_limit=60",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if last_tool_output_verified is false or action_free_of_ethics_concerns is false.\n2. turn_down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is at least steps_used_hard_limit.\n3. send_to_a_person if task_description_complete is false or owner_sign_off_required_for_this_action is true.\nOtherwise: go_ahead.\nNever counted: log_lines_written_in_a_compact_style.\nMeanings:\n- turn_down: halt this item because the rules forbid it\n- put_on_hold: wait for the check and the requester will hear back later\n- send_to_a_person: be passed along to whoever makes the call\n- go_ahead: carry out the request as written\nThe record is complete: nothing else applies.\n\nHey, which of the actions listed after this question is the right call here?",
  "options": [
   "put_on_hold",
   "go_ahead",
   "turn_down"
  ]
 },
 {
  "qid": "qf969530045",
  "kind": "choice",
  "text": "{\n    \"subject\": {\n        \"request_id\": \"REQ-3391\",\n        \"requester\": \"Dana Moreau\"\n    },\n    \"amounts\": {\n        \"access_days_approval_threshold\": 45,\n        \"access_days\": 37\n    },\n    \"checks\": {\n        \"requester_barred_from_this_system\": false,\n        \"legal_preservation_order_on_the_account\": false,\n        \"request_text_written_in_capital_letters\": true,\n        \"request_free_of_ethics_office_flags\": true,\n        \"requested_role_forbidden_by_policy\": false,\n        \"request_grants_admin_rights\": false,\n        \"business_justification_missing\": false,\n        \"mfa_enrollment_complete\": true,\n        \"account_suspended\": false\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if business_justification_missing is true or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. ask_manager if mfa_enrollment_complete is false or request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n3. deny if account_suspended is true or requested_role_forbidden_by_policy is true.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "ask_manager",
   "approve",
   "deny"
  ]
 },
 {
  "qid": "q16e04daac6",
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
  "qid": "qd09c0bf448",
  "kind": "choice",
  "text": "{\n  \"record\":{\n    \"ticket_id\":\"TCK-7090\",\n    \"customer\":\"Nadia Sorensen\"\n  },\n  \"numbers\":{\n    \"claim_amount\":1381.04,\n    \"claim_amount_hard_limit\":2000.00\n  },\n  \"flags\":{\n    \"harmless_greeting_present_in_the_message\":true,\n    \"claim_free_of_ombudsman_cases\":true,\n    \"claim_involves_a_media_inquiry\":true,\n    \"legal_complaint_filed\":false,\n    \"proof_of_purchase_attached\":true,\n    \"item_return_not_yet_received\":false,\n    \"claim_form_filled_in_with_the_usual_font\":true,\n    \"free_of_safety_incident_reports\":false,\n    \"item_excluded_by_policy\":false\n  }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. put on hold if proof_of_purchase_attached is false or claim_involves_a_media_inquiry is true.\n3. send to a person if item_return_not_yet_received is true or legal_complaint_filed is true or free_of_safety_incident_reports is false.\nOtherwise: go ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nLooking at what was asked, which of the actions below best fits the request?",
  "options": [
   "put on hold",
   "go ahead",
   "send to a person"
  ]
 },
 {
  "qid": "qb518f2f65b",
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
  "qid": "q95104d0cef",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n  deploy_id: DEP-2352\n  service: ledger\nvalues:\n  files_changed_soft_limit: 80\n  files_changed: 6\ntests:\n  deploy_blocked_by_security_policy: false\n  deploy_has_a_long_description: false\n  canary_results_complete: true\n  backout_plan_missing: false\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  service_free_of_major_incidents: false\n  rollout_approval_revoked: false\n  deploy_prohibited_during_the_audit_window: false\n  commit_messages_written_in_a_terse_style: false",
  "question": "Proposed action: go ahead\nIs the proposed action correct for this request?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q3a9bd3a104",
  "kind": "yes/no",
  "text": "{\"request_id\": \"REQ-5172\", \"requester\": \"Marta Imai\", \"business_justification_provided\": true, \"requested_role_permitted_by_policy\": true, \"mfa_enrollment_complete\": true, \"legal_preservation_order_on_the_account\": false, \"access_days\": 70, \"account_suspended\": false, \"request_free_of_ethics_office_flags\": true, \"request_grants_admin_rights\": false, \"access_days_approval_threshold\": 90, \"request_text_written_in_capital_letters\": false, \"requester_barred_from_this_system\": false}",
  "question": "Proposed action: deny\nIs the proposed action not what should happen with this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if business_justification_provided is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\n2. ask manager if mfa_enrollment_complete is false or request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is above access_days_approval_threshold.\n3. deny if account_suspended is true or requested_role_permitted_by_policy is false.\nOtherwise: approve.\nNever counted: request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qccf5701c92",
  "kind": "choice",
  "text": "# record\nticket_id | TCK-3072\ncustomer | Marta Hadjiev\nclaim_amount | 200.00\nfree_of_legal_complaints | true\nclaim_free_of_ombudsman_cases | true\nfree_of_safety_incident_reports | true\nproof_of_purchase_attached | true\nitem_return_not_yet_received | false\nclaim_form_filled_in_with_the_usual_font | true\nclaim_amount_hard_limit | 200.00\nitem_excluded_by_policy | false\nharmless_greeting_present_in_the_message | true\nclaim_involves_a_media_inquiry | false",
  "question": "Meanings:\n- XCL: wait so the requester can supply more information first\n- RZBJ: drop it right away\n- Z: let this be advanced exactly as originally specified\n- XQ: submit the question to the authorised decision maker\nThe record is complete: nothing else applies.\n\nLooking at what was asked, which of the actions below best fits the request?",
  "options": [
   "Z",
   "RZBJ",
   "XCL"
  ]
 },
 {
  "qid": "q498e24b013",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n    ticket_id: TCK-7570\n    customer: Mira Brandt\nvalues:\n    claim_amount: 45.51\n    claim_amount_hard_limit: 50.00\ntests:\n    claim_involves_a_media_inquiry: false\n    claim_form_filled_in_with_the_usual_font: false\n    item_excluded_by_policy: false\n    harmless_greeting_present_in_the_message: false\n    proof_of_purchase_missing: false\n    free_of_legal_complaints: true\n    item_return_received: true\n    claim_free_of_ombudsman_cases: true\n    free_of_safety_incident_reports: true",
  "question": "Proposed action: go ahead\nHas the request, read alongside the facts, ruled out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qf6143acd9b",
  "kind": "choice",
  "text": "---\n# request record\nsubject:\n  request_id: \"REQ-4089\"\n  requester: \"صالح كمال الهاشمي\"\n  note: \"المستندات المطلوبة للوصول كاملة ومرفقة بالطلب.\"\namounts:\n  access_days_approval_threshold: 60\n  access_days: 36\nchecks:\n  request_free_of_ethics_office_flags: true\n  request_text_written_in_capital_letters: false\n  requester_barred_from_this_system: false\n  business_justification_missing: false\n  account_suspended: false\n  request_grants_admin_rights: false\n  legal_preservation_order_on_the_account: false\n  requested_role_permitted_by_policy: true\n  mfa_enrollment_incomplete: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action below would serve the person who made this request best?",
  "options": [
   "refuse",
   "grant",
   "refer to owner"
  ]
 },
 {
  "qid": "q1164816039",
  "kind": "choice",
  "text": "{\"ticket_id\":\"TCK-3190\",\"customer\":\"Felix Rossi\",\"free_of_safety_incident_reports\":true,\"legal_complaint_filed\":false,\"claim_form_filled_in_with_the_usual_font\":true,\"claim_involves_a_media_inquiry\":false,\"claim_amount\":33.99,\"item_return_not_yet_received\":true,\"harmless_greeting_present_in_the_message\":true,\"item_excluded_by_policy\":false,\"proof_of_purchase_attached\":true,\"claim_free_of_ombudsman_cases\":true,\"claim_amount_hard_limit\":50.00}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if free_of_safety_incident_reports is false.\n2. turn down if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. put on hold if item_return_not_yet_received is true.\nOtherwise: go ahead.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies.\n\nGiven what the requester needs, which of the actions below should be taken?",
  "options": [
   "put on hold",
   "go ahead",
   "turn down"
  ]
 },
 {
  "qid": "q9c3f54f215",
  "kind": "yes/no",
  "text": "deploy_id=DEP-7183\nservice=checkout\ndeploy_blocked_by_security_policy=false\ndeploy_prohibited_during_the_audit_window=false\ndeploy_has_a_long_description=false\nbackout_plan_documented=true\ncontract_customer_asked_for_a_say_in_this_rollout=false\nfiles_changed_soft_limit=10\ncanary_results_incomplete=false\nservice_free_of_major_incidents=true\nrollout_approval_revoked=false\ncommit_messages_written_in_a_detailed_style=true\nfiles_changed=4",
  "question": "Proposed action: turn_down\nIs it not correct that the proposed action is not off base, judging by the record on file?",
  "definitions": "Meanings:\n- send_to_a_person: be passed along to whoever makes the call\n- put_on_hold: defer further action pending verification of the document\n- turn_down: block the action because it is off limits to the team\n- go_ahead: run with this one\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qeb27e3594c",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  invoice_id: INV-4478\n  vendor: Cedar Traders\nnumbers:\n  amount_approval_threshold: 25000.00\n  amount: 22278.00\nflags:\n  payment_requested_during_business_hours: false\n  approver_free_of_conflicts_of_interest: true\n  purchase_order_received: true\n  invoice_pdf_uses_a_landscape_layout: false\n  vendor_name_written_in_capital_letters: false\n  duplicate_of_paid_invoice: false\n  vendor_tax_form_on_file: true\n  vendor_on_sanctions_list: true\n  vendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "Proposed action: escalate\nSo, is the proposed action a good call for what was asked here?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "qa01b2a60a6",
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
  "qid": "q8e78ce8a49",
  "kind": "yes/no",
  "text": "---\n# request record\ninvoice_id: \"INV-7482\"\nvendor: \"Fairview Logistics\"\nvendor_filed_a_legal_claim_over_this_invoice: false\nawaiting_purchase_order: true\namount_approval_threshold: 1000.00\nduplicate_of_paid_invoice: false\namount: 936.89\npayment_requested_during_business_hours: false\nvendor_free_of_sanctions: true\ninvoice_pdf_uses_a_landscape_layout: false\nvendor_name_written_in_capital_letters: false\napprover_declared_a_conflict_of_interest: true\nvendor_tax_form_missing: false",
  "question": "Proposed action: pay\nHey, do the facts in the record rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. hold if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. reject if vendor_free_of_sanctions is false.\n3. escalate if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: pay.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q03ff22ad1f",
  "kind": "yes/no",
  "text": "# extract\nrun_id                                  | RUN-1759\nagent                                   | garnet\naction_permitted_by_security_policy     | true\ntool_output_shows_tampering             | true\nlast_tool_output_verified               | true\ntask_description_incomplete             | false\nsteps_used_hard_limit                   | 30\nowner_sign_off_required_for_this_action | false\naction_free_of_ethics_concerns          | true\nsteps_used                              | 3\nlog_lines_written_in_a_verbose_style    | false",
  "question": "Proposed action: turn_down\nIs it not so that the proposed action we have on the table is not a poor choice for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send_to_a_person if owner_sign_off_required_for_this_action is true.\n2. turn_down if tool_output_shows_tampering is true or action_permitted_by_security_policy is false or steps_used is above steps_used_hard_limit.\n3. put_on_hold if last_tool_output_verified is false.\nOtherwise: go_ahead.\nNever counted: task_description_incomplete, action_free_of_ethics_concerns, log_lines_written_in_a_verbose_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf0194ef0d7",
  "kind": "choice",
  "text": "{\"ticket_id\": \"TCK-2025\", \"customer\": \"Jonas Haddad\", \"item_return_not_yet_received\": false, \"item_excluded_by_policy\": true, \"claim_free_of_ombudsman_cases\": true, \"claim_involves_a_media_inquiry\": false, \"proof_of_purchase_attached\": true, \"claim_amount\": 92.81, \"free_of_safety_incident_reports\": true, \"claim_amount_hard_limit\": 100.00, \"harmless_greeting_present_in_the_message\": true, \"free_of_legal_complaints\": true, \"claim_form_filled_in_with_the_usual_font\": true}",
  "question": "Meanings:\n- 2: shelve the matter until more details come in\n- 6404: refer the matter to the decision holder\n- 550: continue so the requester receives the result\n- 71: end this effort right away\nThe record is complete: nothing else applies.\n\nWhich of the listed actions do the facts support as the right call?",
  "options": [
   "71",
   "550",
   "6404"
  ]
 },
 {
  "qid": "qd367df3c5f",
  "kind": "choice",
  "text": "Ticket extract: the checks below say yes or no\n* request id: REQ-4668\n* requester: سامر لؤي الأيوبي\n* note: طلب الوصول مكتمل ويستوفي جميع الشروط المطلوبة.\n* mfa enrollment incomplete: no\n* requester not barred from this system: yes\n* business justification missing: no\n* requested role forbidden by policy: no\n* request grants admin rights: no\n* access days approval threshold: 7\n* request free of ethics office flags: yes\n* legal preservation order on the account: no\n* account suspended: no\n* access days: 2\n* request text written in capital letters: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. page oncall if request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n2. quarantine if mfa_enrollment_incomplete is true.\n3. block access if business_justification_missing is true or account_suspended is true or requested_role_forbidden_by_policy is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- allow: continue so the requester receives the result\n- quarantine: wait for the document to come through\n- block access: skip this one, it is a hard pass for us\n- page oncall: escalate this to the person who decides\nThe record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "allow",
   "quarantine",
   "page oncall"
  ]
 },
 {
  "qid": "q003e1803bd",
  "kind": "choice",
  "text": "# case\ndeploy_id = DEP-8636\nservice = checkout\nbackout_plan_documented = true\nservice_free_of_major_incidents = true\ndeploy_prohibited_during_the_audit_window = false\ndeploy_has_a_long_description = false\ncontract_customer_asked_for_a_say_in_this_rollout = false\ncommit_messages_written_in_a_terse_style = false\nfiles_changed_soft_limit = 50\nrollout_approval_revoked = false\nfiles_changed = 50\ncanary_results_incomplete = false\ndeploy_blocked_by_security_policy = true",
  "question": "Meanings:\n- put_on_hold: pause and collect more information first\n- send_to_a_person: hand this to the person who decides\n- go_ahead: run the task as it was asked, with nothing standing between it and completion\n- turn_down: drop this right there, we are not touching it\nThe record is complete: nothing else applies.\n\nAs a manager, which of the actions listed would you pick for this request?",
  "options": [
   "send_to_a_person",
   "go_ahead",
   "turn_down"
  ]
 },
 {
  "qid": "q360b6e0d11",
  "kind": "choice",
  "text": "request_id: REQ-9988\nrequester: Ravi Lindqvist\nlegal_preservation_order_on_the_account: true\nmfa_enrollment_complete: true\nrequested_role_permitted_by_policy: true\naccess_days_approval_threshold: 60\nrequest_grants_admin_rights: false\nrequest_free_of_ethics_office_flags: true\nbusiness_justification_provided: true\naccount_suspended: false\nrequest_text_written_in_capital_letters: false\naccess_days: 21\nrequester_barred_from_this_system: false",
  "question": "Meanings:\n- page oncall: pass the request to a decider\n- quarantine: hold off until the check clears\n- block access: decline the request as the action is prohibited\n- allow: continue as requested with the path fully open\nThe record is complete: nothing else applies.\n\nWhich of the actions listed after this is the appropriate call for the request?",
  "options": [
   "page oncall",
   "quarantine",
   "allow"
  ]
 },
 {
  "qid": "qc7354e25c9",
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
  "qid": "q085708d7f3",
  "kind": "yes/no",
  "text": "{\n    \"request\": {\n        \"invoice_id\": \"INV-6548\",\n        \"vendor\": \"Stonebridge Group\"\n    },\n    \"figures\": {\n        \"amount_approval_threshold\": 2500.00,\n        \"amount\": 2238.02\n    },\n    \"checks\": {\n        \"invoice_pdf_uses_a_portrait_layout\": true,\n        \"awaiting_purchase_order\": false,\n        \"vendor_tax_form_on_file\": false,\n        \"payment_requested_during_business_hours\": true,\n        \"duplicate_of_paid_invoice\": false,\n        \"approver_free_of_conflicts_of_interest\": true,\n        \"vendor_on_sanctions_list\": false,\n        \"vendor_filed_a_legal_claim_over_this_invoice\": false,\n        \"vendor_name_written_in_capital_letters\": false\n    }\n}",
  "question": "Proposed action: defer\nWeighed against the request in the record, does the proposed action look like the right call?",
  "definitions": "Meanings:\n- ask_manager: route this matter to the individual empowered to decide\n- approve: keep it moving forward\n- deny: cease the operation as it is prohibited\n- defer: shelve the matter until more details come in\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qa3dc754af1",
  "kind": "yes/no",
  "text": "{\"invoice_id\":\"INV-1633\",\"vendor\":\"Stonebridge Foods\",\"vendor_tax_form_on_file\":true,\"duplicate_of_paid_invoice\":false,\"vendor_name_written_in_capital_letters\":false,\"awaiting_purchase_order\":true,\"amount_approval_threshold\":5000.00,\"vendor_filed_a_legal_claim_over_this_invoice\":false,\"payment_requested_during_business_hours\":false,\"invoice_pdf_uses_a_landscape_layout\":false,\"amount\":2585.37,\"approver_free_of_conflicts_of_interest\":true,\"vendor_on_sanctions_list\":true}",
  "question": "Proposed action: deny\nDo the facts of this request support the proposed action as the correct decision?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if vendor_on_sanctions_list is true or approver_free_of_conflicts_of_interest is false.\n2. ask manager if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. defer if awaiting_purchase_order is true or amount is at least amount_approval_threshold.\nOtherwise: approve.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- deny: stop the work since it cannot move forward\n- approve: just crack on with it there is nothing in the way\n- ask manager: route the case to a decider so the requester knows the outcome\n- defer: wait for the check and the requester will hear back later\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q23fdcf1849",
  "kind": "yes/no",
  "text": "{\n    \"request\": {\n        \"ticket_id\": \"TCK-1817\",\n        \"customer\": \"Anders Sorensen\"\n    },\n    \"figures\": {\n        \"claim_amount\": 81.34,\n        \"claim_amount_hard_limit\": 100.00\n    },\n    \"checks\": {\n        \"claim_involves_a_media_inquiry\": false,\n        \"claim_form_filled_in_with_the_usual_font\": true,\n        \"claim_free_of_ombudsman_cases\": true,\n        \"legal_complaint_filed\": false,\n        \"item_return_not_yet_received\": false,\n        \"proof_of_purchase_attached\": true,\n        \"free_of_safety_incident_reports\": true,\n        \"item_excluded_by_policy\": false,\n        \"harmless_greeting_present_in_the_message\": true\n    }\n}",
  "question": "Proposed action: W\nIs it not true that the proposed action matches both the request and the facts, and is not a poor choice?",
  "definitions": "Meanings:\n- JL: skip this one, it is a hard pass for us\n- W: go on and finish it the path is clear\n- WXLT: defer the step until the verification is in\n- GJF: escalate this to the person who decides\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qee438d12a2",
  "kind": "yes/no",
  "text": "{\n    \"request\": {\n        \"request_id\": \"REQ-4105\",\n        \"requester\": \"Paolo Castell\"\n    },\n    \"figures\": {\n        \"access_days\": 24,\n        \"access_days_approval_threshold\": 90\n    },\n    \"checks\": {\n        \"account_suspended\": false,\n        \"requested_role_permitted_by_policy\": true,\n        \"request_free_of_ethics_office_flags\": true,\n        \"business_justification_provided\": true,\n        \"request_text_written_in_capital_letters\": false,\n        \"legal_preservation_order_on_the_account\": false,\n        \"mfa_enrollment_complete\": false,\n        \"requester_barred_from_this_system\": false,\n        \"request_grants_admin_rights\": false\n    }\n}",
  "question": "Proposed action: pend\nDo the record's facts rule out the proposed action entirely?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refer to owner if request_grants_admin_rights is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n2. pend if mfa_enrollment_complete is false.\n3. refuse if business_justification_provided is false or account_suspended is true or requested_role_permitted_by_policy is false or requester_barred_from_this_system is true or legal_preservation_order_on_the_account is true.\nOtherwise: grant.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- pend: be paused until a document has been received\n- grant: go ahead and the requester will be served\n- refer to owner: pass it on so the asker gets a final answer from the owner\n- refuse: block this from going any further\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qe238144a5b",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  ticket_id: TCK-8824\n  customer: Priya Duarte\nnumbers:\n  claim_amount_hard_limit: 100.00\n  claim_amount: 100.00\nflags:\n  claim_involves_a_media_inquiry: false\n  proof_of_purchase_attached: true\n  free_of_safety_incident_reports: true\n  claim_form_filled_in_with_the_usual_font: true\n  item_return_not_yet_received: false\n  claim_free_of_ombudsman_cases: true\n  item_excluded_by_policy: false\n  legal_complaint_filed: false\n  harmless_greeting_present_in_the_message: true",
  "question": "Proposed action: 20\nTaken with the request, do the facts rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 1065 if free_of_safety_incident_reports is false.\n2. 1 if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. 721 if item_return_not_yet_received is true.\nOtherwise: 20.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, legal_complaint_filed, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- 20: keep moving on this one nothing is holding it up\n- 1: shut this down before it spreads into the workflow\n- 1065: hand this to the person who decides\n- 721: wait for the check and the requester will hear back later\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q240f14cd65",
  "kind": "yes/no",
  "text": "---\n# extract\ninvoice_id: INV-6009\nvendor: Stonebridge Systems\ninvoice_pdf_uses_a_landscape_layout: false\nduplicate_of_paid_invoice: false\namount: 25000.00\nvendor_tax_form_missing: false\nvendor_free_of_sanctions: false\npurchase_order_received: true\npayment_requested_during_business_hours: true\namount_approval_threshold: 25000.00\napprover_declared_a_conflict_of_interest: false\nvendor_name_written_in_capital_letters: false\nvendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "Proposed action: deny\nMeasured against the request and its facts, is the proposed action not the best call to make?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if purchase_order_received is false or vendor_tax_form_missing is true.\n2. deny if vendor_free_of_sanctions is false.\n3. ask manager if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: approve.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_declared_a_conflict_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb625eb607e",
  "kind": "choice",
  "text": "{\n  \"meta\": {\n    \"ticket_id\": \"TCK-6316\",\n    \"customer\": \"Marta Novak\"\n  },\n  \"metrics\": {\n    \"claim_amount_hard_limit\": 100.00,\n    \"claim_amount\": 78.24\n  },\n  \"signals\": {\n    \"proof_of_purchase_missing\": true,\n    \"claim_involves_a_media_inquiry\": false,\n    \"free_of_safety_incident_reports\": true,\n    \"item_excluded_by_policy\": false,\n    \"item_return_received\": true,\n    \"claim_free_of_ombudsman_cases\": true,\n    \"free_of_legal_complaints\": true,\n    \"harmless_greeting_present_in_the_message\": true,\n    \"claim_form_filled_in_with_the_usual_font\": true\n  }\n}",
  "question": "Meanings:\n- defer: hold all progress until the requisite documentation arrives\n- ask_manager: hand the matter to a decider so the requester gets a verdict\n- approve: continue as requested with the path fully open\n- deny: block the action because it is off limits to the team\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "deny",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q3d5f969db4",
  "kind": "choice",
  "text": "{\"deploy_id\": \"DEP-5247\", \"service\": \"catalog\", \"backout_plan_missing\": false, \"service_free_of_major_incidents\": false, \"contract_customer_asked_for_a_say_in_this_rollout\": false, \"deploy_prohibited_during_the_audit_window\": false, \"commit_messages_written_in_a_detailed_style\": true, \"deploy_blocked_by_security_policy\": false, \"deploy_has_a_long_description\": false, \"files_changed\": 10, \"rollout_approval_revoked\": false, \"canary_results_complete\": true, \"files_changed_soft_limit\": 10}",
  "question": "Meanings:\n- FM: hold off until the check has been completed by the team\n- NJJC: leave the requester without the result they asked for\n- D: escalate the matter to the accountable decision maker\n- SGP: execute the request exactly as written\nThe record is complete: nothing else applies.\n\nHey, which of the actions listed after this question is the right call here?",
  "options": [
   "D",
   "SGP",
   "FM"
  ]
 },
 {
  "qid": "qd4be719eb7",
  "kind": "yes/no",
  "text": "{\"request_id\": \"REQ-7564\", \"requester\": \"Jonas Okafor\", \"mfa_enrollment_complete\": true, \"account_suspended\": false, \"legal_preservation_order_on_the_account\": false, \"request_text_written_in_capital_letters\": false, \"access_days_approval_threshold\": 7, \"access_days\": 1, \"requester_barred_from_this_system\": false, \"business_justification_provided\": true, \"ethics_office_flagged_the_request\": false, \"requested_role_permitted_by_policy\": true, \"request_grants_admin_rights\": false}",
  "question": "Proposed action: pend\nDo the facts recorded for this request rule out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q445b15e5cf",
  "kind": "choice",
  "text": "invoice_id | INV-9477\nvendor | Copperfield Supply\namount | 1647.21\nduplicate_of_paid_invoice | false\nvendor_filed_a_legal_claim_over_this_invoice | false\nvendor_on_sanctions_list | false\nvendor_name_written_in_capital_letters | false\namount_approval_threshold | 10000.00\npayment_requested_during_business_hours | true\npurchase_order_received | false\nvendor_tax_form_on_file | true\napprover_free_of_conflicts_of_interest | true\ninvoice_pdf_uses_a_portrait_layout | true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 54 if vendor_on_sanctions_list is true or approver_free_of_conflicts_of_interest is false.\n2. 9 if vendor_tax_form_on_file is false or duplicate_of_paid_invoice is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. 411 if purchase_order_received is false or amount is at least amount_approval_threshold.\nOtherwise: 3855.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- 3855: have the item pushed forward as the request stated\n- 9: bring in the authority who can settle it for the requester\n- 54: drop this request from the queue\n- 411: park the file until the requester sends the document in\nThe record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "3855",
   "411",
   "9"
  ]
 },
 {
  "qid": "q0551b0dbc5",
  "kind": "choice",
  "text": "{\n  \"request\": {\n    \"request_id\": \"REQ-7172\",\n    \"requester\": \"Sana Ferreira\"\n  },\n  \"figures\": {\n    \"access_days_approval_threshold\": 60,\n    \"access_days\": 14\n  },\n  \"checks\": {\n    \"requester_not_barred_from_this_system\": true,\n    \"requested_role_permitted_by_policy\": true,\n    \"legal_preservation_order_on_the_account\": true,\n    \"business_justification_missing\": false,\n    \"mfa_enrollment_incomplete\": false,\n    \"request_text_written_in_capital_letters\": false,\n    \"account_suspended\": false,\n    \"request_free_of_ethics_office_flags\": true,\n    \"request_grants_admin_rights\": false\n  }\n}",
  "question": "Meanings:\n- approve: complete the job as it was assigned\n- deny: cease the operation as it is prohibited\n- defer: wait so the requester can supply more information first\n- ask_manager: get the boss to make the final call\nThe record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "ask_manager",
   "approve",
   "defer"
  ]
 },
 {
  "qid": "q2354e362da",
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
  "qid": "qdfd337f8c1",
  "kind": "yes/no",
  "text": "Ticket extract (checks are answered yes or no)\n* run id: RUN-1777\n* agent: jasper\n* task description complete: yes\n* action free of ethics concerns: no\n* last tool output verified: yes\n* action forbidden by security policy: no\n* owner sign off required for this action: no\n* steps used: 59\n* steps used hard limit: 60\n* tool output shows tampering: no\n* log lines written in a compact style: yes",
  "question": "Proposed action: turn_down\nDoes the evidence in the record rule out the proposed action as a choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if last_tool_output_verified is false or action_free_of_ethics_concerns is false.\n2. turn_down if tool_output_shows_tampering is true or action_forbidden_by_security_policy is true or steps_used is at least steps_used_hard_limit.\n3. send_to_a_person if task_description_complete is false or owner_sign_off_required_for_this_action is true.\nOtherwise: go_ahead.\nNever counted: log_lines_written_in_a_compact_style.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q94174f00d1",
  "kind": "yes/no",
  "text": "ticket_id=TCK-1351\ncustomer=Elena Ferreira\nfree_of_safety_incident_reports=false\nclaim_form_filled_in_with_the_usual_font=true\nclaim_involves_a_media_inquiry=false\nfree_of_legal_complaints=true\nproof_of_purchase_attached=true\nclaim_free_of_ombudsman_cases=true\nitem_excluded_by_policy=false\nclaim_amount_hard_limit=50.00\nclaim_amount=50.00\nitem_return_not_yet_received=false\nharmless_greeting_present_in_the_message=true",
  "question": "Proposed action: approve\nWould the proposed action not be the appropriate course under the applicable procedure?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false or claim_free_of_ombudsman_cases is false.\n2. deny if proof_of_purchase_attached is false or item_excluded_by_policy is true or claim_involves_a_media_inquiry is true or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_not_yet_received is true.\nOtherwise: approve.\nNever counted: free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- ask manager: send this on to whoever decides\n- approve: proceed as asked since everything is cleared\n- deny: refuse to act since the step is prohibited\n- defer: suspend action until the facts are confirmed\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qf3317c4792",
  "kind": "yes/no",
  "text": "# record\nticket_id: TCK-4778\ncustomer: Hugo Mensah\nlegal_complaint_filed: false\nclaim_amount: 348.76\nclaim_free_of_ombudsman_cases: true\nfree_of_safety_incident_reports: true\nclaim_involves_a_media_inquiry: true\nitem_excluded_by_policy: true\nproof_of_purchase_missing: false\nclaim_form_filled_in_with_the_usual_font: true\nclaim_amount_hard_limit: 1000.00\nharmless_greeting_present_in_the_message: true\nitem_return_received: true",
  "question": "Proposed action: defer\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. deny if item_return_received is false or free_of_safety_incident_reports is false.\n2. defer if item_excluded_by_policy is true or claim_amount is above claim_amount_hard_limit.\n3. ask manager if proof_of_purchase_missing is true or legal_complaint_filed is true or claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false.\nOtherwise: approve.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nMeanings:\n- deny: refuse the request because it crosses a clear line\n- defer: withhold action until supporting information is supplied\n- approve: continue with what was requested\n- ask manager: bring in the authority who can settle it for the requester\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qb5ae05fcae",
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
  "qid": "q298b67291d",
  "kind": "choice",
  "text": "invoice_id: INV-9756\nvendor: Fairview Labs\nduplicate_of_paid_invoice: true\nvendor_name_written_in_capital_letters: false\npayment_requested_during_business_hours: true\napprover_free_of_conflicts_of_interest: true\namount_approval_threshold: 25000.00\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_on_sanctions_list: false\nvendor_tax_form_on_file: true\ninvoice_pdf_uses_a_landscape_layout: false\namount: 10547.82\npurchase_order_received: true",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if approver_free_of_conflicts_of_interest is false.\n2. turn down if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true.\n3. put on hold if purchase_order_received is false or vendor_tax_form_on_file is false or vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: go ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- go ahead: run the task as it was asked, with nothing standing between it and completion\n- put on hold: be paused until a document has been received\n- turn down: decline the request as the action is prohibited\n- send to a person: escalate the matter to the accountable decision maker\nThe record is complete: nothing else applies.\n\nWhich action listed below fits this request best?",
  "options": [
   "send to a person",
   "turn down",
   "go ahead"
  ]
 },
 {
  "qid": "qfee9111fd3",
  "kind": "yes/no",
  "text": "ticket_id: TCK-2805\ncustomer: Sana Keller\nfree_of_safety_incident_reports: false\nproof_of_purchase_attached: true\nclaim_amount_hard_limit: 2000.00\nitem_excluded_by_policy: true\nitem_return_received: true\nharmless_greeting_present_in_the_message: true\nclaim_involves_a_media_inquiry: false\nclaim_amount: 1388.92\nfree_of_legal_complaints: true\nclaim_form_filled_in_with_the_usual_font: true\nclaim_free_of_ombudsman_cases: true",
  "question": "Proposed action: approve\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask manager if free_of_safety_incident_reports is false.\n2. deny if claim_involves_a_media_inquiry is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n3. defer if item_return_received is false.\nOtherwise: approve.\nNever counted: proof_of_purchase_attached, item_excluded_by_policy, free_of_legal_complaints, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message.\nThe record is complete: nothing else applies."
 }
]
