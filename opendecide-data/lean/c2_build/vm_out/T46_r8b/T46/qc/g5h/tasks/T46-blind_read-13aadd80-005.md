# G5-H blind read T46-blind_read-13aadd80-005 (family T46)

ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):
/home/aryamahadik/repo/opendecide-data/lean/c2_build/vm_out/T46_r8b/T46/qc/g5h/answers/T46-blind_read-13aadd80-005.json

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
  "qid": "qfdfe70616f",
  "kind": "choice",
  "text": "leave_id | LVE-5322\nemployee | Nadia Brandt\nleave_days | 13\nleave_balance_exhausted | false\nrequest_falls_in_blackout_period | true\nleave_days_soft_limit | 14\nno_union_grievance_raised_over_this_leave | true\nnotice_period_not_met | false\nteam_coverage_not_arranged | false\nleave_request_written_in_a_formal_tone | false\nrequests_team_free_of_harassment_complaints | true\nlawyer_letter_received_about_this_leave | false\nmedical_certificate_contested | false",
  "question": "The record is complete: nothing else applies.\n\nChoosing from the actions listed, what is the right call for this request?",
  "options": [
   "approve_leave",
   "refuse_leave",
   "postpone"
  ]
 },
 {
  "qid": "q6304939fc3",
  "kind": "choice",
  "text": "# case\nticket_id: TCK-1823\ncustomer: Samir Adeyemi\ncustomer_message_is_short: true\nharmless_greeting_present_in_the_message: true\nproof_of_purchase_attached: true\nclaim_amount: 500.01\nclaim_form_filled_in_with_the_usual_font: true\nitem_return_received: true\nlegal_complaint_filed: false\nitem_excluded_by_policy: false\nclaim_involves_a_media_inquiry: false\nfree_of_safety_incident_reports: true\nclaim_amount_hard_limit: 500.00\nclaim_free_of_ombudsman_cases: true\ncustomer_message_written_in_a_formal_tone: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action below fits what this person is asking for?",
  "options": [
   "deny",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "q9509440e34",
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
  "qid": "qda86c36ce2",
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
  "qid": "q8c675df369",
  "kind": "yes/no",
  "text": "# extract\nleave_id: LVE-4615\nemployee: Omar Imai\nrequest_falls_in_blackout_period: false\nteam_coverage_not_arranged: false\nmedical_certificate_contested: false\nlawyer_letter_received_about_this_leave: false\nleave_days: 5\nrequests_team_free_of_harassment_complaints: true\nnotice_period_not_met: false\nleave_balance_exhausted: true\nno_union_grievance_raised_over_this_leave: true\nleave_request_written_in_a_formal_tone: false\nleave_days_soft_limit: 5",
  "question": "Proposed action: cancel\nIs it not true that the proposed action passes audit and is not a mismatch for the facts?",
  "definitions": "Meanings:\n- proceed: have the item pushed forward as the request stated\n- cancel: be stopped and never carried out\n- wait: defer further action pending verification of the document\n- ask_a_human: escalate it so the person asking receives a decision\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q282c84cdb3",
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
  "qid": "q118946a737",
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
  "qid": "q4bf3fff343",
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
  "qid": "qd3a408161d",
  "kind": "choice",
  "text": "{\"request_id\":\"REQ-6759\",\"requester\":\"Marta Petrov\",\"request_text_written_in_capital_letters\":false,\"requested_role_forbidden_by_policy\":false,\"mfa_enrollment_complete\":true,\"business_justification_missing\":true,\"requester_not_barred_from_this_system\":true,\"request_free_of_ethics_office_flags\":true,\"access_days_approval_threshold\":7,\"access_days\":10,\"legal_preservation_order_on_the_account\":false,\"request_grants_admin_rights\":false,\"account_suspended\":false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if business_justification_missing is true or requested_role_forbidden_by_policy is true.\n2. ask manager if mfa_enrollment_complete is false or legal_preservation_order_on_the_account is true or request_free_of_ethics_office_flags is false or access_days is at least access_days_approval_threshold.\n3. deny if account_suspended is true or requester_not_barred_from_this_system is false.\nOtherwise: approve.\nNever counted: request_grants_admin_rights, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies.\n\nThe request describes a situation; which of the actions underneath handles it correctly?",
  "options": [
   "defer",
   "ask manager",
   "approve"
  ]
 },
 {
  "qid": "q351b62d1ce",
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
  "qid": "qabe8f99f9b",
  "kind": "choice",
  "text": "{\"ticket_id\": \"TCK-7048\", \"customer\": \"Nadia Calloway\", \"harmless_greeting_present_in_the_message\": true, \"claim_involves_a_media_inquiry\": false, \"claim_form_filled_in_with_the_usual_font\": true, \"free_of_legal_complaints\": true, \"claim_free_of_ombudsman_cases\": false, \"customer_message_is_short\": true, \"claim_amount_hard_limit\": 100.00, \"customer_message_written_in_a_casual_tone\": true, \"claim_amount\": 91.14, \"item_return_not_yet_received\": false, \"free_of_safety_incident_reports\": false, \"proof_of_purchase_missing\": true, \"item_excluded_by_policy\": false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 40 if item_return_not_yet_received is true or claim_free_of_ombudsman_cases is false.\n2. 6168 if item_excluded_by_policy is true or free_of_legal_complaints is false or claim_amount is above claim_amount_hard_limit.\n3. 1 if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: 396.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- 1: forward the case to the approver with authority\n- 396: complete the action that was asked for\n- 40: withhold action until supporting information is supplied\n- 6168: be halted at once and left unperformed\nThe record is complete: nothing else applies.\n\nTaking the actions listed into account, what is the right call for the request?",
  "options": [
   "6168",
   "396",
   "40"
  ]
 },
 {
  "qid": "q28b0b10d73",
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
  "qid": "q262098fcd3",
  "kind": "choice",
  "text": "Ticket extract (checks are answered yes or no)\n- invoice id: INV-8007\n- vendor: Pinecrest Labs\n- duplicate of paid invoice: no\n- invoice pdf uses a portrait layout: no\n- amount: 433.95\n- amount approval threshold: 1000.00\n- vendor tax form missing: no\n- vendor filed a legal claim over this invoice: no\n- payment requested during business hours: yes\n- vendor free of sanctions: yes\n- approver declared a conflict of interest: no\n- awaiting purchase order: no\n- vendor name written in capital letters: no",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if awaiting_purchase_order is true.\n2. send to a person if vendor_tax_form_missing is true or vendor_filed_a_legal_claim_over_this_invoice is true.\n3. turn down if vendor_free_of_sanctions is false or duplicate_of_paid_invoice is true or approver_declared_a_conflict_of_interest is true or amount is above amount_approval_threshold.\nOtherwise: go ahead.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_portrait_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- put on hold: hold off until the check clears\n- go ahead: carry on with it now\n- turn down: leave the requester without the result they asked for\n- send to a person: transfer the case to the responsible decision maker for determination\nThe record is complete: nothing else applies.\n\nIf you were auditing this file, which of the listed actions would be the correct response?",
  "options": [
   "go ahead",
   "turn down",
   "put on hold"
  ]
 },
 {
  "qid": "q8f7082c7d2",
  "kind": "yes/no",
  "text": "Ticket extract: the checks below say yes or no\n- leave id: LVE-9635\n- employee: Nadia Moreau\n- leave balance available: yes\n- lawyer letter received about this leave: yes\n- requests team free of harassment complaints: yes\n- leave days: 5\n- leave request written in a formal tone: yes\n- union grievance raised over this leave: no\n- request falls in blackout period: no\n- notice period not met: no\n- leave days soft limit: 7\n- team coverage not arranged: no\n- medical certificate contested: yes",
  "question": "Proposed action: deny\nGiven the request and the facts, is the proposed action not the right call?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_not_met is true or team_coverage_not_arranged is true or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. deny if medical_certificate_contested is true.\n3. ask manager if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nMeanings:\n- defer: be held back until a check or document arrives\n- approve: complete the action that was asked for\n- deny: veto this move and leave it there\n- ask manager: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qbe344857de",
  "kind": "yes/no",
  "text": "---\n# extract\ncase:\n  invoice_id: INV-4615\n  vendor: Stonebridge Works\nvalues:\n  amount_approval_threshold: 10000.00\n  amount: 6017.96\ntests:\n  payment_requested_during_business_hours: false\n  awaiting_purchase_order: false\n  vendor_free_of_sanctions: true\n  vendor_name_written_in_capital_letters: true\n  vendor_tax_form_missing: true\n  invoice_pdf_uses_a_landscape_layout: true\n  duplicate_of_paid_invoice: false\n  approver_free_of_conflicts_of_interest: true\n  vendor_filed_a_legal_claim_over_this_invoice: true",
  "question": "Proposed action: delay\nIs it not the case that the facts available line up with the proposed action and it is not out of step?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if awaiting_purchase_order is true or vendor_tax_form_missing is true.\n2. cancel order if vendor_free_of_sanctions is false.\n3. hand to a person if vendor_filed_a_legal_claim_over_this_invoice is true or amount is above amount_approval_threshold.\nOtherwise: release.\nNever counted: duplicate_of_paid_invoice, payment_requested_during_business_hours, approver_free_of_conflicts_of_interest, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- cancel order: decline the request as the action is prohibited\n- delay: wait for the document to come through\n- hand to a person: be routed to whoever holds the decision\n- release: advance the task as stated without any blockers\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q77b7a7b0b9",
  "kind": "yes/no",
  "text": "---\nticket_id: TCK-5863\ncustomer: Idris Anand\nclaim_amount_hard_limit: 2000.00\nclaim_amount: 2000.01\ncustomer_message_is_short: true\nclaim_involves_a_media_inquiry: false\ncustomer_message_written_in_a_casual_tone: true\nfree_of_safety_incident_reports: true\nclaim_free_of_ombudsman_cases: true\nclaim_form_filled_in_with_the_usual_font: true\nharmless_greeting_present_in_the_message: true\nitem_return_received: true\nitem_excluded_by_policy: false\nlegal_complaint_filed: false\nproof_of_purchase_attached: true",
  "question": "Proposed action: approve\nIs the proposed action not the right call for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. refuse if claim_amount is at least claim_amount_hard_limit.\n2. ask a human if legal_complaint_filed is true or claim_involves_a_media_inquiry is true.\n3. delay if proof_of_purchase_attached is false or item_excluded_by_policy is true.\nOtherwise: approve.\nNever counted: item_return_received, free_of_safety_incident_reports, claim_free_of_ombudsman_cases, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q5f48373bec",
  "kind": "choice",
  "text": "# record\nleave_id: LVE-4170\nemployee: Yara Okonkwo\nmedical_certificate_contested: false\nleave_balance_available: true\nteam_coverage_arranged: true\nno_union_grievance_raised_over_this_leave: true\nleave_days_soft_limit: 7\nleave_request_written_in_a_formal_tone: false\nrequest_falls_in_blackout_period: false\nrequests_team_free_of_harassment_complaints: true\nlawyer_letter_received_about_this_leave: false\nleave_days: 7\nnotice_period_met: true",
  "question": "Meanings:\n- 78: refuse to act since the step is prohibited\n- 2: keep moving on this one nothing is holding it up\n- 6446: keep it in limbo until the verification has been confirmed\n- 631: hand this over to whoever has the final say\nThe record is complete: nothing else applies.\n\nWhich of the actions set out below is recommended for the request in the record?",
  "options": [
   "631",
   "78",
   "2"
  ]
 },
 {
  "qid": "qadb75a7faa",
  "kind": "yes/no",
  "text": "---\nmeta:\n  leave_id: \"LVE-5961\"\n  employee: \"Omar Moreau\"\nmetrics:\n  leave_days_soft_limit: 21\n  leave_days: 1\nsignals:\n  lawyer_letter_received_about_this_leave: false\n  requests_team_free_of_harassment_complaints: false\n  medical_certificate_contested: false\n  notice_period_not_met: false\n  team_coverage_not_arranged: false\n  leave_balance_available: true\n  union_grievance_raised_over_this_leave: false\n  request_falls_in_blackout_period: false\n  leave_request_written_in_a_formal_tone: false",
  "question": "Proposed action: approve\nWould the proposed action be the right answer to what this request calls for?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. delay if notice_period_not_met is true or team_coverage_not_arranged is true or leave_balance_available is false or request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n2. refuse if medical_certificate_contested is true.\n3. ask_a_human if union_grievance_raised_over_this_leave is true or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q600df55cc6",
  "kind": "yes/no",
  "text": "{\"invoice_id\": \"INV-5873\", \"vendor\": \"Ironleaf Traders\", \"approver_free_of_conflicts_of_interest\": true, \"vendor_tax_form_on_file\": true, \"amount\": 3309.32, \"vendor_on_sanctions_list\": false, \"awaiting_purchase_order\": true, \"vendor_name_written_in_capital_letters\": false, \"duplicate_of_paid_invoice\": false, \"vendor_filed_a_legal_claim_over_this_invoice\": false, \"invoice_pdf_uses_a_portrait_layout\": true, \"amount_approval_threshold\": 5000.00, \"payment_requested_during_business_hours\": true}",
  "question": "Proposed action: refuse\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q0336a72018",
  "kind": "choice",
  "text": "---\ndeploy_id: \"DEP-7444\"\nservice: \"inventory\"\nfiles_changed_soft_limit: 20\ncontract_customer_asked_for_a_say_in_this_rollout: false\ncanary_results_complete: true\ncommit_messages_written_in_a_casual_tone: false\ncommit_messages_written_in_a_detailed_style: true\ndeploy_has_a_long_description: false\nservice_free_of_major_incidents: true\ndeploy_prohibited_during_the_audit_window: false\nrollout_approval_revoked: false\ndeploy_title_written_in_normal_case: true\nbackout_plan_documented: true\ndeploy_blocked_by_security_policy: false\nfiles_changed: 4",
  "question": "The record is complete: nothing else applies.\n\nOf the actions listed, which is the correct call for this request?",
  "options": [
   "turn_down",
   "put_on_hold",
   "go_ahead"
  ]
 },
 {
  "qid": "qeb27e3594c",
  "kind": "yes/no",
  "text": "---\n# record\nrecord:\n  invoice_id: INV-4478\n  vendor: Cedar Traders\nnumbers:\n  amount_approval_threshold: 25000.00\n  amount: 22278.00\nflags:\n  payment_requested_during_business_hours: false\n  approver_free_of_conflicts_of_interest: true\n  purchase_order_received: true\n  invoice_pdf_uses_a_landscape_layout: false\n  vendor_name_written_in_capital_letters: false\n  duplicate_of_paid_invoice: false\n  vendor_tax_form_on_file: true\n  vendor_on_sanctions_list: true\n  vendor_filed_a_legal_claim_over_this_invoice: false",
  "question": "Proposed action: escalate\nSo, is the proposed action a good call for what was asked here?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q9120ca4702",
  "kind": "yes/no",
  "text": "leave_id: LVE-3042\nemployee: ريما فايز الزبيدي\nnote: طلب الإجازة مقدم في الموعد المحدد بالسياسة.\nleave_days_soft_limit: 10\nleave_request_written_in_a_formal_tone: false\nleave_balance_available: false\nmedical_certificate_contested: false\nno_union_grievance_raised_over_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nleave_days: 4\nteam_coverage_arranged: true\nrequest_falls_in_blackout_period: true\nnotice_period_met: false\nlawyer_letter_received_about_this_leave: false",
  "question": "Proposed action: delay\nDoes what we know about this rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. delay if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. refuse if leave_balance_available is false.\nOtherwise: approve.\nNever counted: notice_period_met, no_union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qcc787566de",
  "kind": "yes/no",
  "text": "{\"deploy_id\":\"DEP-2388\",\"service\":\"mailer\",\"files_changed\":41,\"rollout_approval_revoked\":false,\"deploy_has_a_long_description\":false,\"deploy_prohibited_during_the_audit_window\":false,\"backout_plan_missing\":false,\"canary_results_incomplete\":false,\"deploy_title_written_in_normal_case\":true,\"commit_messages_written_in_a_detailed_style\":true,\"service_free_of_major_incidents\":true,\"files_changed_soft_limit\":50,\"commit_messages_written_in_a_casual_tone\":true,\"contract_customer_asked_for_a_say_in_this_rollout\":false,\"deploy_blocked_by_security_policy\":false}",
  "question": "Proposed action: go ahead\nBe honest, is the proposed action not a good fit for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. send to a person if contract_customer_asked_for_a_say_in_this_rollout is true.\n2. turn down if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true or files_changed is above files_changed_soft_limit.\n3. put on hold if backout_plan_missing is true or rollout_approval_revoked is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- send to a person: hand this to the person who decides\n- turn down: leave the requester without the result they asked for\n- put on hold: park this until a record turns up\n- go ahead: keep it moving forward\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q72dfa2be46",
  "kind": "yes/no",
  "text": "---\n# case\nsubject:\n    deploy_id: DEP-4450\n    service: checkout\namounts:\n    files_changed: 15\n    files_changed_soft_limit: 15\nchecks:\n    commit_messages_written_in_a_terse_style: false\n    contract_customer_asked_for_a_say_in_this_rollout: false\n    backout_plan_missing: false\n    canary_results_incomplete: false\n    rollout_approval_revoked: false\n    deploy_has_a_long_description: false\n    deploy_blocked_by_security_policy: false\n    deploy_title_written_in_normal_case: false\n    service_free_of_major_incidents: true\n    commit_messages_written_in_a_casual_tone: true\n    deploy_prohibited_during_the_audit_window: false",
  "question": "Proposed action: turn down\nDo the record's facts rule out the proposed action entirely?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put on hold if backout_plan_missing is true or files_changed is above files_changed_soft_limit.\n2. turn down if deploy_blocked_by_security_policy is true or rollout_approval_revoked is true or deploy_prohibited_during_the_audit_window is true.\n3. send to a person if service_free_of_major_incidents is false or contract_customer_asked_for_a_say_in_this_rollout is true.\nOtherwise: go ahead.\nNever counted: canary_results_incomplete, deploy_has_a_long_description, commit_messages_written_in_a_terse_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- turn down: kill this one off\n- go ahead: keep moving on this one nothing is holding it up\n- put on hold: suspend progress until verification is received\n- send to a person: pass it on so the asker gets a final answer from the owner\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q03bdd8c9cd",
  "kind": "choice",
  "text": "---\ninvoice_id: INV-6459\nvendor: Oakmont Labs\npurchase_order_received: true\npayment_requested_during_business_hours: false\namount: 18051.09\nvendor_tax_form_on_file: true\nvendor_on_sanctions_list: false\nduplicate_of_paid_invoice: false\napprover_declared_a_conflict_of_interest: false\ninvoice_pdf_uses_a_portrait_layout: false\nvendor_filed_a_legal_claim_over_this_invoice: false\nvendor_name_written_in_capital_letters: false\namount_approval_threshold: 25000.00",
  "question": "The record is complete: nothing else applies.\n\nMind telling me which of the actions below is the best call for this request?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "send_to_a_person"
  ]
 },
 {
  "qid": "q4a5246d669",
  "kind": "choice",
  "text": "# record\nrequest_id: REQ-6656\nrequester: Marta Mensah\nrequested_role_permitted_by_policy: true\nrequest_grants_admin_rights: false\nmfa_enrollment_incomplete: false\nrequest_free_of_ethics_office_flags: true\nrequest_text_written_in_capital_letters: false\nbusiness_justification_missing: false\naccess_days: 27\naccount_suspended: false\nlegal_preservation_order_on_the_account: false\nrequester_not_barred_from_this_system: false\naccess_days_approval_threshold: 60",
  "question": "The record is complete: nothing else applies.\n\nFor the purposes of this file, which of the actions below is the proper disposition?",
  "options": [
   "quarantine",
   "allow",
   "block_access"
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
  "qid": "qc574d4f610",
  "kind": "choice",
  "text": "{\"leave_id\":\"LVE-2584\",\"employee\":\"Zoe Hadjiev\",\"medical_certificate_contested\":false,\"union_grievance_raised_over_this_leave\":false,\"leave_days_soft_limit\":14,\"lawyer_letter_received_about_this_leave\":false,\"team_coverage_not_arranged\":false,\"leave_balance_available\":false,\"requests_team_free_of_harassment_complaints\":true,\"leave_request_written_in_a_formal_tone\":false,\"leave_days\":14,\"notice_period_not_met\":false,\"request_falls_in_blackout_period\":false}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if team_coverage_not_arranged is true or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. wait if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. cancel if leave_balance_available is false.\nOtherwise: proceed.\nNever counted: notice_period_not_met, union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nWhich of the actions listed should the team commit to for this request, as the manager?",
  "options": [
   "ask a human",
   "cancel",
   "proceed"
  ]
 },
 {
  "qid": "qb9d0a0d66c",
  "kind": "yes/no",
  "text": "---\nleave_id: LVE-9339\nemployee: غسان مروان العلوي\nnote: الموافقة على الإجازة ما زالت ناقصة بسبب بيانات غير مؤكدة.\nnotice_period_not_met: false\nunion_grievance_raised_over_this_leave: false\nrequests_team_free_of_harassment_complaints: true\nleave_request_written_in_a_formal_tone: false\nleave_balance_exhausted: false\nteam_coverage_not_arranged: false\nleave_days: 2\nrequest_falls_in_blackout_period: false\nleave_days_soft_limit: 7\nlawyer_letter_received_about_this_leave: false\nmedical_certificate_contested: false",
  "question": "Proposed action: defer\nHas the record ruled out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q7b8feb2e7a",
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
  "qid": "q966488194f",
  "kind": "yes/no",
  "text": "# record\ninvoice_id | INV-3152\nvendor | Brightwater Foods\nvendor_filed_a_legal_claim_over_this_invoice | false\npurchase_order_received | true\npayment_requested_during_business_hours | true\nvendor_tax_form_missing | true\ninvoice_pdf_uses_a_landscape_layout | false\nvendor_name_written_in_capital_letters | false\namount | 3466.21\napprover_declared_a_conflict_of_interest | false\nvendor_on_sanctions_list | false\namount_approval_threshold | 25000.00\nduplicate_of_paid_invoice | false",
  "question": "Proposed action: proceed\nAuditing this request closely, is the proposed action not a defensible choice?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if vendor_filed_a_legal_claim_over_this_invoice is true or approver_declared_a_conflict_of_interest is true.\n2. cancel if vendor_on_sanctions_list is true or duplicate_of_paid_invoice is true or amount is above amount_approval_threshold.\n3. wait if purchase_order_received is false or vendor_tax_form_missing is true.\nOtherwise: proceed.\nNever counted: payment_requested_during_business_hours, invoice_pdf_uses_a_landscape_layout, vendor_name_written_in_capital_letters.\nMeanings:\n- proceed: keep moving on this one nothing is holding it up\n- ask_a_human: hand the matter to a decider so the requester gets a verdict\n- wait: be parked until a verification has been logged\n- cancel: withdraw from the step as it is forbidden\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q1e5df8cd1b",
  "kind": "choice",
  "text": "---\n# extract\ncase:\n  run_id: RUN-9590\n  agent: atlas\nvalues:\n  steps_used: 7\n  steps_used_hard_limit: 40\ntests:\n  action_forbidden_by_security_policy: false\n  last_tool_output_verified: true\n  log_lines_written_in_a_compact_style: true\n  task_description_complete: true\n  action_free_of_ethics_concerns: true\n  owner_sign_off_required_for_this_action: false\n  tool_output_shows_tampering: false",
  "question": "The record is complete: nothing else applies.\n\nWhich action listed matches what the record shows as the right response to this request?",
  "options": [
   "go_ahead",
   "put_on_hold",
   "turn_down"
  ]
 },
 {
  "qid": "q551fd177f3",
  "kind": "yes/no",
  "text": "leave_id: LVE-3935\nemployee: Anders Whitcombe\nteam_coverage_arranged: true\nleave_request_written_in_a_formal_tone: false\nleave_days_soft_limit: 3\nrequests_team_free_of_harassment_complaints: true\nunion_grievance_raised_over_this_leave: false\nnotice_period_met: true\nmedical_certificate_contested: false\nleave_balance_exhausted: true\nleave_days: 3\nlawyer_letter_received_about_this_leave: false\nrequest_falls_in_blackout_period: false",
  "question": "Proposed action: deny\nAs a reviewer checking the file, is the proposed action not a sound decision here?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_manager if team_coverage_arranged is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\n2. defer if request_falls_in_blackout_period is true or leave_days is above leave_days_soft_limit.\n3. deny if leave_balance_exhausted is true.\nOtherwise: approve.\nNever counted: notice_period_met, union_grievance_raised_over_this_leave, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qefe8d32a06",
  "kind": "yes/no",
  "text": "{\"ticket_id\": \"TCK-1279\", \"customer\": \"Priya Rossi\", \"claim_amount\": 815.15, \"item_excluded_by_policy\": false, \"free_of_safety_incident_reports\": true, \"proof_of_purchase_missing\": true, \"item_return_received\": true, \"claim_form_filled_in_with_the_usual_font\": true, \"harmless_greeting_present_in_the_message\": true, \"customer_message_written_in_a_formal_tone\": false, \"legal_complaint_filed\": false, \"claim_amount_hard_limit\": 1000.00, \"claim_free_of_ombudsman_cases\": true, \"claim_involves_a_media_inquiry\": false, \"customer_message_is_short\": true}",
  "question": "Proposed action: put_on_hold\nDoes the proposed action constitute the appropriate response to the request on file?",
  "definitions": "Meanings:\n- put_on_hold: sit on it till the doc shows up\n- send_to_a_person: send it up to the person who makes the call\n- go_ahead: carry out the request as written\n- turn_down: be stopped and never carried out\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qd87f5a69bc",
  "kind": "choice",
  "text": "# case\ndeploy_id: DEP-6834\nservice: mailer\nservice_free_of_major_incidents: true\ndeploy_title_written_in_normal_case: true\nrollout_approval_revoked: false\ncanary_results_incomplete: false\ncontract_customer_asked_for_a_say_in_this_rollout: false\ndeploy_prohibited_during_the_audit_window: false\ncommit_messages_written_in_a_detailed_style: true\ndeploy_blocked_by_security_policy: false\nfiles_changed_soft_limit: 15\nbackout_plan_documented: true\nfiles_changed: 15\ndeploy_has_a_long_description: false\ncommit_messages_written_in_a_casual_tone: true",
  "question": "The record is complete: nothing else applies.\n\nReading the file for this case, which listed action is the best call?",
  "options": [
   "put on hold",
   "go ahead",
   "turn down"
  ]
 },
 {
  "qid": "qf60af7cfd6",
  "kind": "yes/no",
  "text": "invoice_id=INV-3268\nvendor=Bluepeak Supply\nvendor_name_written_in_capital_letters=false\nduplicate_of_paid_invoice=false\nvendor_tax_form_on_file=true\nvendor_filed_a_legal_claim_over_this_invoice=false\nvendor_on_sanctions_list=false\npayment_requested_during_business_hours=true\namount_approval_threshold=10000.00\napprover_declared_a_conflict_of_interest=false\ninvoice_pdf_uses_a_portrait_layout=true\namount=7567.77\npurchase_order_received=true",
  "question": "Proposed action: deny\nHas the record ruled out the proposed action?",
  "definitions": "The record is complete: nothing else applies."
 },
 {
  "qid": "q6444cde2fa",
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
  "qid": "q3ce8def0ca",
  "kind": "choice",
  "text": "{\"ticket_id\": \"TCK-6371\", \"customer\": \"Dana Mensah\", \"item_excluded_by_policy\": false, \"claim_amount_hard_limit\": 500.00, \"claim_form_filled_in_with_the_usual_font\": true, \"item_return_received\": true, \"free_of_safety_incident_reports\": true, \"harmless_greeting_present_in_the_message\": false, \"customer_message_written_in_a_casual_tone\": false, \"proof_of_purchase_missing\": true, \"claim_involves_a_media_inquiry\": false, \"customer_message_is_short\": true, \"claim_amount\": 80.19, \"claim_free_of_ombudsman_cases\": true, \"free_of_legal_complaints\": true}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 6 if item_return_received is false or claim_free_of_ombudsman_cases is false.\n2. 627 if item_excluded_by_policy is true or free_of_legal_complaints is false or claim_amount is above claim_amount_hard_limit.\n3. 66 if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\nOtherwise: 7111.\nNever counted: free_of_safety_incident_reports, claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- 7111: complete the job as it was assigned\n- 6: stay put until the check is finished\n- 627: make sure the requester never gets what they wanted\n- 66: get sent upward to the one who decides\nThe record is complete: nothing else applies.\n\nAuditing the request, which of the actions below is the defensible choice?",
  "options": [
   "627",
   "7111",
   "66"
  ]
 },
 {
  "qid": "q4a5bf38316",
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
  "qid": "q733d91d760",
  "kind": "choice",
  "text": "# case\nrequest_id = REQ-2624\nrequester = Tomas Brandt\naccess_days_approval_threshold = 60\nrequest_grants_admin_rights = false\nlegal_preservation_order_on_the_account = false\nrequest_text_written_in_capital_letters = false\nrequested_role_permitted_by_policy = true\nethics_office_flagged_the_request = false\naccess_days = 13\naccount_suspended = false\nmfa_enrollment_incomplete = false\nrequester_not_barred_from_this_system = true\nbusiness_justification_missing = false",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. 55 if mfa_enrollment_incomplete is true or requester_not_barred_from_this_system is false or ethics_office_flagged_the_request is true.\n2. 5455 if account_suspended is true or requested_role_permitted_by_policy is false.\n3. 837 if legal_preservation_order_on_the_account is true or access_days is above access_days_approval_threshold.\nOtherwise: 1.\nNever counted: business_justification_missing, request_grants_admin_rights, request_text_written_in_capital_letters.\nMeanings:\n- 5455: halt the request at this point\n- 55: hold the request so the requester waits for their check\n- 1: commence the action as specified without impediment\n- 837: route it elsewhere because a decider must weigh in\nThe record is complete: nothing else applies.\n\nAs the manager, which of the actions listed is the right call for this request?",
  "options": [
   "55",
   "837",
   "1"
  ]
 },
 {
  "qid": "qef23766c84",
  "kind": "choice",
  "text": "{\n    \"request_id\": \"REQ-2115\",\n    \"requester\": \"Anders Mensah\",\n    \"request_text_written_in_capital_letters\": false,\n    \"requested_role_forbidden_by_policy\": false,\n    \"access_days\": 30,\n    \"access_days_approval_threshold\": 30,\n    \"legal_preservation_order_on_the_account\": true,\n    \"mfa_enrollment_incomplete\": false,\n    \"ethics_office_flagged_the_request\": false,\n    \"business_justification_missing\": false,\n    \"request_grants_admin_rights\": false,\n    \"account_suspended\": false,\n    \"requester_not_barred_from_this_system\": true\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. quarantine if business_justification_missing is true or requester_not_barred_from_this_system is false or legal_preservation_order_on_the_account is true.\n2. page oncall if mfa_enrollment_incomplete is true or request_grants_admin_rights is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n3. block access if account_suspended is true or requested_role_forbidden_by_policy is true.\nOtherwise: allow.\nNever counted: request_text_written_in_capital_letters.\nMeanings:\n- quarantine: keep it in limbo until the verification has been confirmed\n- block access: shut off this process completely\n- allow: run the requested step through\n- page oncall: pass the request along since the decision belongs to another person\nThe record is complete: nothing else applies.\n\nWhat would the requester most want done from the actions listed below?",
  "options": [
   "quarantine",
   "allow",
   "block access"
  ]
 },
 {
  "qid": "qb1625900fe",
  "kind": "yes/no",
  "text": "# record\ndeploy_id: DEP-7188\nservice: gateway\ndeploy_has_a_long_description: false\nservice_free_of_major_incidents: true\nrollout_approval_revoked: true\ndeploy_blocked_by_security_policy: false\nbackout_plan_missing: false\nfiles_changed_soft_limit: 15\ncontract_customer_asked_for_a_say_in_this_rollout: false\nfiles_changed: 6\ncanary_results_incomplete: false\ncommit_messages_written_in_a_casual_tone: true\ndeploy_prohibited_during_the_audit_window: false\ncommit_messages_written_in_a_detailed_style: true\ndeploy_title_written_in_normal_case: true",
  "question": "Proposed action: turn_down\nGiven the request and the facts, is the proposed action the right call?",
  "definitions": "Meanings:\n- turn_down: stop this course of action at once\n- go_ahead: keep moving on this one nothing is holding it up\n- send_to_a_person: pass this along to the decision maker\n- put_on_hold: keep waiting for the missing details\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q825b6aa1e2",
  "kind": "yes/no",
  "text": "---\n# request record\nsubject:\n  deploy_id: \"DEP-1264\"\n  service: \"auth_proxy\"\namounts:\n  files_changed: 10\n  files_changed_soft_limit: 15\nchecks:\n  commit_messages_written_in_a_detailed_style: false\n  deploy_title_written_in_normal_case: true\n  deploy_prohibited_during_the_audit_window: false\n  backout_plan_documented: true\n  deploy_blocked_by_security_policy: true\n  rollout_approval_revoked: true\n  deploy_has_a_long_description: false\n  contract_customer_asked_for_a_say_in_this_rollout: false\n  commit_messages_written_in_a_casual_tone: true\n  canary_results_complete: false\n  service_free_of_major_incidents: true",
  "question": "Proposed action: wait\nBe honest, do the facts here rule out the proposed action?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask_a_human if contract_customer_asked_for_a_say_in_this_rollout is true or files_changed is above files_changed_soft_limit.\n2. cancel if deploy_blocked_by_security_policy is true or deploy_prohibited_during_the_audit_window is true.\n3. wait if canary_results_complete is false.\nOtherwise: proceed.\nNever counted: backout_plan_documented, deploy_has_a_long_description, rollout_approval_revoked, service_free_of_major_incidents, commit_messages_written_in_a_detailed_style, commit_messages_written_in_a_casual_tone, deploy_title_written_in_normal_case.\nMeanings:\n- wait: be kept on hold until more information is supplied\n- cancel: scrap the plan and drop this request\n- proceed: let this be advanced exactly as originally specified\n- ask_a_human: hand this off because a decider has to choose\nThe record is complete: nothing else applies."
 },
 {
  "qid": "qdf52059d18",
  "kind": "yes/no",
  "text": "{\n    \"leave_id\":\"LVE-8173\",\n    \"employee\":\"كنان ياسر الوادي\",\n    \"note\":\"طلب الإجازة مقدم في الموعد المحدد بالسياسة.\",\n    \"team_coverage_not_arranged\":false,\n    \"leave_balance_available\":true,\n    \"medical_certificate_contested\":false,\n    \"lawyer_letter_received_about_this_leave\":false,\n    \"leave_days\":1,\n    \"no_union_grievance_raised_over_this_leave\":true,\n    \"requests_team_free_of_harassment_complaints\":true,\n    \"notice_period_not_met\":false,\n    \"request_falls_in_blackout_period\":true,\n    \"leave_days_soft_limit\":14,\n    \"leave_request_written_in_a_formal_tone\":true\n}",
  "question": "Proposed action: approve\nDo the documented facts rule out the proposed action under this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. defer if notice_period_not_met is true or team_coverage_not_arranged is true or leave_days is above leave_days_soft_limit.\n2. deny if request_falls_in_blackout_period is true or no_union_grievance_raised_over_this_leave is false.\n3. ask manager if leave_balance_available is false or medical_certificate_contested is true or requests_team_free_of_harassment_complaints is false or lawyer_letter_received_about_this_leave is true.\nOtherwise: approve.\nNever counted: leave_request_written_in_a_formal_tone.\nMeanings:\n- ask manager: be handed over to the deciding person\n- approve: let the request be continued as originally asked\n- defer: await further verification before any progression\n- deny: reject the petition as the action is unauthorized\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q4a2fa0b1c1",
  "kind": "yes/no",
  "text": "# case\nticket_id = TCK-3487\ncustomer = Omar Ferreira\nproof_of_purchase_missing = true\nclaim_amount = 50.00\ncustomer_message_written_in_a_casual_tone = true\nclaim_amount_hard_limit = 50.00\nitem_return_received = true\nlegal_complaint_filed = false\nclaim_form_filled_in_with_the_usual_font = true\ncustomer_message_is_short = true\nfree_of_safety_incident_reports = true\nclaim_free_of_ombudsman_cases = true\nclaim_involves_a_media_inquiry = false\nharmless_greeting_present_in_the_message = true\nitem_excluded_by_policy = false",
  "question": "Proposed action: go ahead\nDoes the proposed action match what the record supports for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. turn down if item_excluded_by_policy is true or claim_free_of_ombudsman_cases is false or claim_amount is above claim_amount_hard_limit.\n2. put on hold if proof_of_purchase_missing is true or claim_involves_a_media_inquiry is true.\n3. send to a person if item_return_received is false or legal_complaint_filed is true or free_of_safety_incident_reports is false.\nOtherwise: go ahead.\nNever counted: claim_form_filled_in_with_the_usual_font, harmless_greeting_present_in_the_message, customer_message_written_in_a_casual_tone, customer_message_is_short.\nMeanings:\n- send to a person: route this matter to the individual empowered to decide\n- go ahead: go ahead and the requester will be served\n- put on hold: defer the step until the verification is in\n- turn down: be stopped and never carried out\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q57c5121e37",
  "kind": "choice",
  "text": "{\n    \"case\":{\n        \"leave_id\":\"LVE-8442\",\n        \"employee\":\"Marta Sorensen\"\n    },\n    \"values\":{\n        \"leave_days\":2,\n        \"leave_days_soft_limit\":7\n    },\n    \"tests\":{\n        \"leave_request_written_in_a_formal_tone\":false,\n        \"team_coverage_arranged\":true,\n        \"no_union_grievance_raised_over_this_leave\":false,\n        \"leave_balance_available\":true,\n        \"requests_team_free_of_harassment_complaints\":true,\n        \"request_falls_in_blackout_period\":false,\n        \"medical_certificate_contested\":false,\n        \"lawyer_letter_received_about_this_leave\":false,\n        \"notice_period_met\":true\n    }\n}",
  "question": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. put_on_hold if team_coverage_arranged is false or medical_certificate_contested is true or leave_days is above leave_days_soft_limit.\n2. turn_down if request_falls_in_blackout_period is true or lawyer_letter_received_about_this_leave is true.\n3. send_to_a_person if no_union_grievance_raised_over_this_leave is false.\nOtherwise: go_ahead.\nNever counted: notice_period_met, leave_balance_available, requests_team_free_of_harassment_complaints, leave_request_written_in_a_formal_tone.\nThe record is complete: nothing else applies.\n\nWhat would the requester most want done from the actions listed below?",
  "options": [
   "put_on_hold",
   "go_ahead",
   "send_to_a_person"
  ]
 },
 {
  "qid": "qa37cb2186e",
  "kind": "yes/no",
  "text": "request_id | REQ-6572\nrequester | Idris Lindqvist\nmfa_enrollment_incomplete | false\nrequest_text_written_in_capital_letters | true\nrequest_grants_admin_rights | false\naccess_days_approval_threshold | 7\nbusiness_justification_provided | true\nrequested_role_forbidden_by_policy | false\naccount_suspended | false\nlegal_preservation_order_on_the_account | false\naccess_days | 6\nrequester_barred_from_this_system | false\nethics_office_flagged_the_request | false",
  "question": "Proposed action: proceed\nIs it not true that the proposed action is not mistaken, given what the record shows?",
  "definitions": "Meanings:\n- wait: hold the request so the requester waits for their check\n- proceed: keep it moving forward\n- cancel: block the action because it is off limits to the team\n- ask a human: route the request to the decision maker\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q6949e11322",
  "kind": "choice",
  "text": "deploy_id | DEP-5417\nservice | reports\ndeploy_prohibited_during_the_audit_window | false\nservice_free_of_major_incidents | false\ncanary_results_incomplete | false\nfiles_changed | 20\ndeploy_title_written_in_normal_case | false\ndeploy_blocked_by_security_policy | false\ncontract_customer_asked_for_a_say_in_this_rollout | false\ncommit_messages_written_in_a_casual_tone | true\nrollout_approval_revoked | false\nbackout_plan_documented | true\ndeploy_has_a_long_description | false\nfiles_changed_soft_limit | 20\ncommit_messages_written_in_a_detailed_style | true",
  "question": "Meanings:\n- KRGT: keep moving so the asker gets the outcome\n- GNF: direct the request to the responsible decider\n- CL: be blocked outright so it never gets carried out\n- R: stall the request until the check comes back\nThe record is complete: nothing else applies.\n\nWhich of the actions listed below is the right call for this request?",
  "options": [
   "KRGT",
   "GNF",
   "R"
  ]
 },
 {
  "qid": "q04eea90e4d",
  "kind": "yes/no",
  "text": "Ticket extract, checks answered with yes or no\n- request id: REQ-5682\n- requester: Mira Vasquez\n- requested role forbidden by policy: no\n- requester barred from this system: no\n- account suspended: no\n- request grants admin rights: no\n- mfa enrollment incomplete: no\n- ethics office flagged the request: no\n- business justification missing: no\n- legal preservation order on the account: no\n- access days: 7\n- request text written in capital letters: no\n- access days approval threshold: 14",
  "question": "Proposed action: approve\nDoes the record point to the proposed action as the right decision for this request?",
  "definitions": "Policy: apply the numbered lines in order; the first line that applies decides.\n1. ask a human if request_grants_admin_rights is true or legal_preservation_order_on_the_account is true or ethics_office_flagged_the_request is true or access_days is above access_days_approval_threshold.\n2. delay if requested_role_forbidden_by_policy is true.\n3. refuse if mfa_enrollment_incomplete is true or account_suspended is true.\nOtherwise: approve.\nNever counted: business_justification_missing, requester_barred_from_this_system, request_text_written_in_capital_letters.\nThe record is complete: nothing else applies."
 },
 {
  "qid": "q24d2dce339",
  "kind": "choice",
  "text": "{\n  \"request\": {\n    \"request_id\": \"REQ-8931\",\n    \"requester\": \"رنا جمال التونسي\",\n    \"note\": \"حالة الوصول إلى النظام استثنائية وتقع خارج نطاق صلاحية الكاتب.\"\n  },\n  \"figures\": {\n    \"access_days\": 9,\n    \"access_days_approval_threshold\": 14\n  },\n  \"checks\": {\n    \"request_grants_admin_rights\": false,\n    \"requested_role_forbidden_by_policy\": false,\n    \"account_suspended\": false,\n    \"requester_not_barred_from_this_system\": true,\n    \"business_justification_missing\": false,\n    \"legal_preservation_order_on_the_account\": false,\n    \"mfa_enrollment_incomplete\": false,\n    \"request_free_of_ethics_office_flags\": true,\n    \"request_text_written_in_capital_letters\": false\n  }\n}",
  "question": "Meanings:\n- QQT: allow the matter to be taken forward as planned\n- PCRB: route this matter to the individual empowered to decide\n- X: pump the brakes until more details show up\n- BJ: stop the work since it cannot move forward\nThe record is complete: nothing else applies.\n\nHey, which of the actions listed after this question is the right call here?",
  "options": [
   "PCRB",
   "QQT",
   "BJ"
  ]
 }
]
