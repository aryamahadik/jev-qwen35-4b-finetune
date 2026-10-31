"""families/T46/tables.py: the T46 DISPOSITION-GATE program tables (solver-A side; G0_SPEC.md sections 2-3 state them).

Imports nothing (data only). The tables are the program-asserted T46 lexicon of A59 (c): every surface label, every
state flag value and every Haiku gloss maps to exactly ONE semantic class across the whole family.

  classes   P permit (carry on as asked) | H hold (wait: a check, a document or more information is needed)
            D deny (refuse or stop: it must not be done) | E human (a person must decide)
  flags     a state flag is a field whose value is true / false. Each flag has two phrasings: A (the problem is `true`)
            and B (the problem is `false`); the row draws the phrasing from its key. Class H / D / E flags are
            problems of that class; class A ("oddity") flags report a harmless oddity (outside business hours, capital
            letters ...): BOTH their values mean P. An active oddity or a problem flag the card does not count is an
            "alarming but permitted" cue.
  numeric   one (value, limit) pair per workflow; the limit field's suffix names the consequence of going above it:
            _approval_threshold -> E, _hard_limit -> D, _soft_limit -> H.
"""
from __future__ import annotations

FAMILY = "T46"
CLASSES = ("P", "H", "D", "E")
SEM_OF = {"P": "disp.permit", "H": "disp.hold", "D": "disp.deny", "E": "disp.human"}
CLASS_OF_SEM = {v: k for k, v in SEM_OF.items()}
MEANING = {
    "P": "carry on as asked: nothing stands in the way",
    "H": "do not go ahead yet: wait for a check, a document or more information",
    "D": "refuse or stop it: it must not be done",
    "E": "pass it to a person who decides",
}
MEANING_TO_CLASS = {v: k for k, v in MEANING.items()}
SUFFIX_CLASS = {"_approval_threshold": "E", "_hard_limit": "D", "_soft_limit": "H"}
CLOSED_WORLD = "The record is complete: nothing else applies."

# ------------------------------------------------------------------------------------------------ vocabularies
# id -> labels {class: snake form}; the spelled-out form replaces "_" by " ". Lengths within a vocabulary are distinct
# (kit plan_report: the gold's length rank is uniform when the shown labels have distinct lengths).
VOCABS = {
    "V1": {"P": "pay", "H": "hold", "D": "reject", "E": "escalate"},
    "V2": {"P": "continue", "H": "observe", "D": "stop", "E": "human_review"},
    "V3": {"P": "refund", "H": "replace", "D": "decline_claim", "E": "human_agent"},
    "V4": {"P": "approve", "H": "defer", "D": "deny", "E": "ask_manager"},
    "V5": {"P": "allow", "H": "quarantine", "D": "block_access", "E": "page_oncall"},
    "V6": {"P": "grant", "H": "pend", "D": "refuse", "E": "refer_to_owner"},
    "V7": {"P": "approve_leave", "H": "postpone", "D": "refuse_leave", "E": "refer_to_hr"},
    "V8": {"P": "promote", "H": "pause", "D": "rollback", "E": "page_owner"},
    "V9": {"P": "proceed", "H": "wait", "D": "cancel", "E": "notify_lead"},
    "V10": {"P": "go_ahead", "H": "put_on_hold", "D": "turn_down", "E": "send_to_a_person"},
    "V11": {"P": "release", "H": "delay", "D": "cancel_order", "E": "hand_to_a_person"},
    # Round 7 (G0 amendment): V2, V3, V8 and V9 each have a label the blind reads rejected ("observe", "refund", "replace",
    # "promote", "rollback", "page_owner", "notify_lead"), so only 7 of 11 sets were usable (target >= 8) and agent / deploy had
    # one. V12-V14 reuse label words already in the family (one meaning per word) in new combinations; they are read blind too.
    "V12": {"P": "proceed", "H": "wait", "D": "cancel", "E": "ask_a_human"},
    "V13": {"P": "continue", "H": "pause", "D": "stop", "E": "human_review"},
    "V14": {"P": "approve", "H": "delay", "D": "refuse", "E": "ask_a_human"},
}
DOMAINS = {
    "invoice": ("V1", "V4", "V9", "V10", "V11", "V12", "V14"),
    "support": ("V3", "V4", "V9", "V10", "V12", "V14"),
    "agent": ("V2", "V9", "V10", "V8", "V12", "V13"),
    "access": ("V5", "V6", "V4", "V9", "V12", "V14"),
    "hr": ("V7", "V4", "V9", "V10", "V12", "V14"),
    "deploy": ("V8", "V2", "V9", "V10", "V12", "V13"),
    "purchase": ("V4", "V1", "V11", "V7", "V14"),
}


def label_forms(vocab: str, cls: str) -> tuple:
    """(snake, spelled) surface forms of one label (equal when the label is one word)."""
    s = VOCABS[vocab][cls]
    return s, s.replace("_", " ")


def all_label_texts() -> dict:
    """{surface text: class} over every vocabulary; raises if a text names two classes (one meaning per word)."""
    out = {}
    for v, labs in VOCABS.items():
        for c, snake in labs.items():
            for t in {snake, snake.replace("_", " ")}:
                if out.get(t, c) != c:
                    raise ValueError(f"label text {t!r} names two classes")
                out[t] = c
    return out


# ------------------------------------------------------------------------------------------------ workflows
# flag = (fid, class, nameA, nameB): nameA's problem value is true, nameB's problem value is false. Class "A" = alarm.
FLAGS = {
    "invoice": [
        ("po", "H", "awaiting_purchase_order", "purchase_order_received"),
        ("tax", "H", "vendor_tax_form_missing", "vendor_tax_form_on_file"),
        ("sanc", "D", "vendor_on_sanctions_list", "vendor_free_of_sanctions"),
        ("dup", "D", "duplicate_of_paid_invoice", "invoice_is_unique"),
        ("bank", "E", "bank_details_changed_recently", "bank_details_unchanged_since_last_payment"),
        ("disp", "E", "vendor_disputes_the_amount", "vendor_accepts_the_amount"),
        ("odd", "A", "payment_requested_outside_business_hours", "payment_requested_during_business_hours"),
        ("contact", "A", "vendor_changed_its_billing_contact", "vendor_kept_its_billing_contact"),
    ],
    "support": [
        ("proof", "H", "proof_of_purchase_missing", "proof_of_purchase_attached"),
        ("ret", "H", "item_return_not_yet_received", "item_return_received"),
        ("fraud", "D", "customer_flagged_for_claim_fraud", "customer_clear_of_fraud_flags"),
        ("excl", "D", "item_excluded_by_policy", "item_covered_by_policy"),
        ("legal", "E", "legal_complaint_filed", "free_of_legal_complaints"),
        ("safe", "E", "safety_incident_reported", "free_of_safety_incident_reports"),
        ("caps", "A", "customer_wrote_in_capital_letters", "customer_wrote_in_normal_case"),
        ("repeat", "A", "customer_contacted_support_before", "customer_contacts_support_for_the_first_time"),
    ],
    "agent": [
        ("tool", "H", "last_tool_output_unverified", "last_tool_output_verified"),
        ("task", "H", "task_description_incomplete", "task_description_complete"),
        ("scope", "D", "action_outside_granted_scope", "action_inside_granted_scope"),
        ("tamper", "D", "tool_output_shows_tampering", "tool_output_integrity_intact"),
        ("irrev", "E", "action_irreversible_and_unreviewed", "action_reversible_or_reviewed"),
        ("conf", "E", "agents_report_conflicting_results", "agents_report_matching_results"),
        ("sched", "A", "run_started_outside_the_usual_schedule", "run_started_on_the_usual_schedule"),
        ("calls", "A", "run_used_more_tool_calls_than_average", "run_used_an_average_number_of_tool_calls"),
    ],
    "access": [
        ("just", "H", "business_justification_missing", "business_justification_provided"),
        ("mfa", "H", "mfa_enrollment_incomplete", "mfa_enrollment_complete"),
        ("susp", "D", "account_suspended", "account_active_and_unsuspended"),
        ("role", "D", "requested_role_forbidden_by_policy", "requested_role_permitted_by_policy"),
        ("priv", "E", "request_grants_admin_rights", "request_grants_standard_rights_only"),
        ("inv", "E", "user_under_security_investigation", "user_free_of_security_investigations"),
        ("hours", "A", "request_made_outside_business_hours", "request_made_during_business_hours"),
        ("team", "A", "requester_recently_changed_teams", "requester_stayed_on_the_same_team"),
    ],
    "hr": [
        ("notice", "H", "notice_period_not_met", "notice_period_met"),
        ("cover", "H", "team_coverage_not_arranged", "team_coverage_arranged"),
        ("bal", "D", "leave_balance_exhausted", "leave_balance_available"),
        ("black", "D", "request_falls_in_blackout_period", "request_outside_blackout_period"),
        ("med", "E", "medical_certificate_contested", "medical_certificate_uncontested"),
        ("compl", "E", "complaint_filed_against_requester", "requester_free_of_complaints"),
        ("wkend", "A", "request_filed_on_a_weekend", "request_filed_on_a_weekday"),
        ("prev", "A", "requester_took_leave_last_month", "requester_stayed_at_work_last_month"),
    ],
    "deploy": [
        ("canary", "H", "canary_results_incomplete", "canary_results_complete"),
        ("rb", "H", "backout_plan_missing", "backout_plan_documented"),
        ("tests", "D", "required_tests_failing", "required_tests_passing"),
        ("freeze", "D", "change_freeze_in_effect", "outside_change_freeze"),
        ("dep", "E", "depends_on_unreviewed_external_change", "dependencies_all_reviewed"),
        ("scan", "E", "security_scan_findings_disputed", "security_scan_findings_uncontested"),
        ("hours", "A", "deploy_happens_outside_working_hours", "deploy_happens_in_working_hours"),
        ("desc", "A", "deploy_has_a_long_description", "deploy_has_a_short_description"),
    ],
    "purchase": [        # dev-only workflow skin (A59 (e): own dev, at least 30% of dev)
        ("quote", "H", "competing_quote_missing", "competing_quotes_collected"),
        ("spec", "H", "technical_spec_incomplete", "technical_spec_complete"),
        ("debar", "D", "supplier_debarred", "supplier_eligible_for_awards"),
        ("split", "D", "order_split_to_avoid_limits", "order_placed_whole"),
        ("coi", "E", "buyer_declared_conflict_of_interest", "buyer_free_of_conflicts"),
        ("aud", "E", "open_audit_finding_on_supplier", "supplier_free_of_open_audit_findings"),
        ("qend", "A", "order_placed_at_quarter_end", "order_placed_mid_quarter"),
        ("far", "A", "supplier_is_far_away", "supplier_is_nearby"),
    ],
}
# Round 5 (G0 amendment): the blind G-LEX reads rejected 64 of the 224 flag-value forms (an escalation fact read as "hold", an
# oddity read as "tell someone"), which left only the invoice workflow usable. Extra candidate flags are added with class-evident
# names (escalation facts name a person's ruling, a legal or regulatory matter, a safety or ethics matter; prohibitions name a ban
# or a policy bar; oddities name a routine or format fact). They are read blind like every other form; a flag whose forms are not
# all admitted is never drawn, so the admitted set decides which of these exist.
_EXTRA = {
    "invoice": [
        ("legal", "E", "vendor_filed_a_legal_claim_over_this_invoice", "vendor_free_of_legal_claims_over_this_invoice"),
        ("reg", "E", "regulator_inquiry_open_about_the_vendor", "vendor_free_of_regulator_inquiries"),
        ("coi", "E", "approver_declared_a_conflict_of_interest", "approver_free_of_conflicts_of_interest"),
        ("term", "D", "vendor_contract_terminated", "vendor_contract_in_force"),
        ("fmt", "A", "invoice_pdf_uses_a_landscape_layout", "invoice_pdf_uses_a_portrait_layout"),
        ("caps", "A", "vendor_name_written_in_capital_letters", "vendor_name_written_in_normal_case"),
        ("rout1", "A", "harmless_duplicate_email_copy_received", "harmless_single_email_copy_received"),
        ("rout2", "A", "routine_month_end_invoice_batch", "routine_mid_month_invoice_batch"),
    ],
    "support": [
        ("ban", "D", "customer_banned_from_making_claims", "customer_not_banned_from_making_claims"),
        ("media", "E", "claim_involves_a_media_inquiry", "claim_free_of_media_inquiries"),
        ("ombud", "E", "ombudsman_case_opened_for_the_claim", "claim_free_of_ombudsman_cases"),
        ("fmt", "A", "claim_form_filled_in_with_a_different_font", "claim_form_filled_in_with_the_usual_font"),
        ("lang", "A", "customer_wrote_in_a_second_language", "customer_wrote_in_the_main_language"),
        ("rout1", "A", "harmless_greeting_missing_from_the_message", "harmless_greeting_present_in_the_message"),
        ("rout2", "A", "routine_weekend_support_contact", "routine_weekday_support_contact"),
    ],
    "agent": [
        ("forbid", "D", "action_forbidden_by_security_policy", "action_permitted_by_security_policy"),
        ("legalrev", "E", "legal_review_requested_on_this_action", "action_free_of_legal_review_requests"),
        ("ethic", "E", "action_raises_an_ethics_concern", "action_free_of_ethics_concerns"),
        ("signoff", "E", "owner_sign_off_required_for_this_action", "no_owner_sign_off_required_for_this_action"),
        ("fmt", "A", "log_lines_written_in_a_verbose_style", "log_lines_written_in_a_compact_style"),
        ("name", "A", "agent_renamed_since_its_last_run", "agent_name_unchanged_since_its_last_run"),
        ("rout1", "A", "harmless_retry_of_a_read_only_call", "harmless_no_retry_of_a_read_only_call"),
        ("rout2", "A", "routine_nightly_run", "routine_daytime_run"),
    ],
    "access": [
        ("ban", "D", "requester_barred_from_this_system", "requester_not_barred_from_this_system"),
        ("legal", "E", "legal_preservation_order_on_the_account", "account_free_of_legal_preservation_orders"),
        ("ethic", "E", "ethics_office_flagged_the_request", "request_free_of_ethics_office_flags"),
        ("fmt", "A", "request_text_written_in_capital_letters", "request_text_written_in_normal_case"),
        ("device", "A", "request_sent_from_a_second_device", "request_sent_from_the_usual_device"),
        ("rout1", "A", "harmless_typo_in_the_request_title", "harmless_no_typo_in_the_request_title"),
        ("rout2", "A", "routine_quarterly_access_review", "routine_monthly_access_review"),
    ],
    "hr": [
        ("harass", "E", "harassment_complaint_lodged_about_the_requests_team", "requests_team_free_of_harassment_complaints"),
        ("union", "E", "union_grievance_raised_over_this_leave", "no_union_grievance_raised_over_this_leave"),
        ("legal", "E", "lawyer_letter_received_about_this_leave", "no_lawyer_letter_received_about_this_leave"),
        ("fmt", "A", "form_submitted_as_a_scanned_copy", "form_submitted_as_a_typed_copy"),
        ("manager", "A", "requester_reports_to_a_new_manager", "requester_reports_to_the_same_manager"),
        ("rout1", "A", "harmless_late_night_submission", "harmless_daytime_submission"),
        ("rout2", "A", "routine_summer_holiday_request", "routine_winter_holiday_request"),
    ],
    "deploy": [
        ("sec", "D", "deploy_blocked_by_security_policy", "deploy_permitted_by_security_policy"),
        ("revoked", "D", "rollout_approval_revoked", "rollout_approval_in_place"),
        ("audit", "D", "deploy_prohibited_during_the_audit_window", "deploy_outside_the_audit_window"),
        ("legal", "E", "legal_has_asked_to_review_this_rollout", "rollout_free_of_legal_review_requests"),
        ("incident", "E", "open_major_incident_involves_this_service", "service_free_of_major_incidents"),
        ("custask", "E", "contract_customer_asked_for_a_say_in_this_rollout", "no_customer_asked_for_a_say_in_this_rollout"),
        ("fmt", "A", "commit_messages_written_in_a_terse_style", "commit_messages_written_in_a_detailed_style"),
        ("rout1", "A", "harmless_rename_of_a_comment_only_file", "harmless_no_rename_of_a_comment_only_file"),
        ("rout2", "A", "routine_weekly_rollout_train", "routine_hotfix_rollout"),
    ],
    "purchase": [
        ("fmt", "A", "quote_pdf_uses_a_landscape_layout", "quote_pdf_uses_a_portrait_layout"),
        ("lang", "A", "supplier_wrote_in_a_second_language", "supplier_wrote_in_the_main_language"),
        ("rout1", "A", "harmless_duplicate_email_of_the_quote", "harmless_single_email_of_the_quote"),
        ("rout2", "A", "routine_year_end_order_batch", "routine_mid_year_order_batch"),
        ("embargo", "D", "supplier_country_under_an_embargo", "supplier_country_free_of_embargoes"),
        ("legal", "E", "supplier_sued_the_company_over_a_past_order", "supplier_has_not_sued_the_company_over_a_past_order"),
    ],
}
for _wf, _ex in _EXTRA.items():
    FLAGS[_wf] = FLAGS[_wf] + _ex
# Round 7 (G0 amendment): after the round-5 reads hr kept no oddity flag (so it was unusable) and agent, access and purchase kept one.
# Cosmetic oddities (tone, length, ink, capital letters) were the ones the readers admitted; each is read blind like every form.
_EXTRA7 = {
    "hr": [
        ("ink", "A", "leave_form_signed_in_blue_ink", "leave_form_signed_in_black_ink"),
        ("title", "A", "leave_request_title_written_in_capital_letters", "leave_request_title_written_in_normal_case"),
        ("tone", "A", "leave_request_written_in_a_formal_tone", "leave_request_written_in_a_casual_tone"),
        ("msglen", "A", "leave_request_message_is_long", "leave_request_message_is_short"),
        ("device", "A", "leave_request_sent_from_a_second_device", "leave_request_sent_from_the_usual_device"),
    ],
    "agent": [
        ("outlen", "A", "agent_output_is_long", "agent_output_is_short"),
        ("tone", "A", "agent_reply_written_in_a_formal_tone", "agent_reply_written_in_a_casual_tone"),
        ("title", "A", "task_title_written_in_capital_letters", "task_title_written_in_normal_case"),
        ("tz", "A", "run_timestamps_written_in_utc", "run_timestamps_written_in_local_time"),
    ],
    "access": [
        ("title", "A", "request_title_is_long", "request_title_is_short"),
        ("tone", "A", "access_request_written_in_a_formal_tone", "access_request_written_in_a_casual_tone"),
        ("ink", "A", "access_form_signed_in_blue_ink", "access_form_signed_in_black_ink"),
    ],
    "support": [
        ("tone", "A", "customer_message_written_in_a_formal_tone", "customer_message_written_in_a_casual_tone"),
        ("msglen", "A", "customer_message_is_long", "customer_message_is_short"),
        ("title", "A", "message_title_written_in_capital_letters", "message_title_written_in_normal_case"),
    ],
    "deploy": [
        ("tone", "A", "commit_messages_written_in_a_formal_tone", "commit_messages_written_in_a_casual_tone"),
        ("branch", "A", "deploy_from_a_branch_with_a_long_name", "deploy_from_a_branch_with_a_short_name"),
        ("title", "A", "deploy_title_written_in_capital_letters", "deploy_title_written_in_normal_case"),
    ],
    "purchase": [
        ("tone", "A", "supplier_message_written_in_a_formal_tone", "supplier_message_written_in_a_casual_tone"),
        ("msglen", "A", "supplier_message_is_long", "supplier_message_is_short"),
    ],
}
for _wf, _ex in _EXTRA7.items():
    FLAGS[_wf] = FLAGS[_wf] + _ex
# numeric pair per workflow: value field, limit field, kind, unit words, limit range (cents or counts)
NUMERIC = {
    "invoice": ("amount", "amount_approval_threshold", "money", (50000, 100000, 250000, 500000, 1000000, 2500000)),
    "support": ("claim_amount", "claim_amount_hard_limit", "money", (5000, 10000, 20000, 50000, 100000, 200000)),
    "agent": ("steps_used", "steps_used_hard_limit", "count", (8, 12, 16, 20, 30, 40, 60)),
    "access": ("access_days", "access_days_approval_threshold", "count", (7, 14, 30, 45, 60, 90)),
    "hr": ("leave_days", "leave_days_soft_limit", "count", (3, 5, 7, 10, 14, 21)),
    "deploy": ("files_changed", "files_changed_soft_limit", "count", (10, 15, 20, 30, 50, 80)),
    "purchase": ("order_value", "order_value_approval_threshold", "money", (200000, 500000, 1000000, 2500000)),
}
ID_KEY = {"invoice": ("invoice_id", "INV"), "support": ("ticket_id", "TCK"), "agent": ("run_id", "RUN"),
          "access": ("request_id", "REQ"), "hr": ("leave_id", "LVE"), "deploy": ("deploy_id", "DEP"),
          "purchase": ("po_id", "PO")}
PERSON_KEY = {"invoice": ("vendor", "company"), "support": ("customer", "person"), "agent": ("agent", "agent"),
              "access": ("requester", "person"), "hr": ("employee", "person"), "deploy": ("service", "service"),
              "purchase": ("buyer", "person")}
TRAIN_WORKFLOWS = ("invoice", "support", "agent", "access", "hr", "deploy")
DEV_WORKFLOWS = ("purchase",)
NOTE_KEY = "note"

# ------------------------------------------------------------------------------------------------ name pools
FIRST = ("Dana", "Lena", "Ravi", "Mira", "Tomas", "Aiko", "Jonas", "Priya", "Marta", "Omar", "Elena", "Kofi", "Nadia",
         "Samir", "Ingrid", "Hugo", "Leila", "Paolo", "Yara", "Felix", "Sana", "Anders", "Zoe", "Idris")
LAST = ("Okafor", "Whitcombe", "Anand", "Castell", "Ferreira", "Brandt", "Lindqvist", "Hadjiev", "Moreau", "Tanaka",
        "Quispe", "Vasquez", "Novak", "Haddad", "Keller", "Adeyemi", "Rossi", "Sorensen", "Petrov", "Mensah",
        "Calloway", "Imai", "Duarte", "Okonkwo")
FIRST_DEV = ("Bruno", "Talia", "Edmund", "Farah", "Gideon", "Hana", "Ivor", "Junko")
LAST_DEV = ("Aldridge", "Bellamy", "Cardoso", "Dlamini", "Eriksen", "Fontaine", "Grigoryan", "Holloway")
CO_A = ("Northwind", "Bluepeak", "Harbor", "Cedar", "Ironleaf", "Summit", "Copperfield", "Lakeshore", "Redwood",
        "Silverline", "Brightwater", "Stonebridge", "Fairview", "Oakmont", "Pinecrest", "Riverbend")
CO_B = ("Traders", "Supply", "Logistics", "Foods", "Systems", "Partners", "Industries", "Works", "Group", "Labs")
CO_A_DEV = ("Alderwick", "Brightmoor", "Crestfall", "Dunmore")
CO_B_DEV = ("Freight", "Components", "Textiles", "Analytics")
SERVICES = ("checkout", "search", "billing", "ledger", "gateway", "inventory", "notifier", "profile", "catalog",
            "reports", "scheduler", "uploads", "auth_proxy", "pricing", "exporter", "mailer")
SERVICES_DEV = ("fulfilment", "ratings", "geocoder", "archiver")
AGENTS = ("atlas", "beacon", "cobalt", "delta", "ember", "fjord", "garnet", "helix", "indigo", "jasper", "kestrel",
          "lumen")
AGENTS_DEV = ("meridian", "nimbus", "onyx", "prism")


def names_for(kind: str, dev: bool) -> list:
    if kind == "person":
        return [f"{a} {b}" for a in (FIRST_DEV if dev else FIRST) for b in (LAST_DEV if dev else LAST)]
    if kind == "company":
        return [f"{a} {b}" for a in (CO_A_DEV if dev else CO_A) for b in (CO_B_DEV if dev else CO_B)]
    if kind == "service":
        return list(SERVICES_DEV if dev else SERVICES)
    if kind == "agent":
        return list(AGENTS_DEV if dev else AGENTS)
    raise KeyError(kind)


# ------------------------------------------------------------------------------------------------ layouts
LAYOUTS_TRAIN = ("json", "json_nested", "yaml", "yaml_nested", "kv_colon", "kv_equals", "kv_pipe", "ticket")
LAYOUTS_DEV = ("toml", "xml")
FREEFORM_LAYOUTS = ("ticket",)     # ticket-form states count as free-form for the 25% cap (A59 (c))

# ------------------------------------------------------------------------------------------------ question forms
QFORMS_YN = ("yn_is", "yn_not", "yn_ruledout", "yn_dneg")
QFORM_CH = "ch_disp"
PREDICATE = "proposed_is_right_call"
# complement pairs the relation proposals may use: (base form, partner form)
COMPLEMENT_PAIRS = {"yn_is": ("yn_not", "yn_ruledout"), "yn_not": ("yn_is", "yn_dneg"), "yn_ruledout": ("yn_is",),
                    "yn_dneg": ("yn_not",)}
QFORM_MEANING = {
    "yn_is": "asks whether the proposed action is the right call here (yes means it is the right call)",
    "yn_not": "asks whether the proposed action is NOT the right call here (yes means it is not the right call)",
    "yn_ruledout": "asks whether the facts rule the proposed action out (yes means it is the wrong call)",
    "yn_dneg": "asks with two negations whether the proposed action is the right call (yes means it is the right call)",
    "ch_disp": "asks which of the listed actions is the right call here",
}
