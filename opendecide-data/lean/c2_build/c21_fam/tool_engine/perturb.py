"""Perturbation manifest: closed ids for T54 deletions, the T55 2x2 (explicit/implicit x transient/permanent) plus
the ambiguous-write class, and the T56 fault registry (fault -> reason class, hard/easy bin, precedence)."""
import hashlib

# ---- T54 ---------------------------------------------------------------------------------------------------
T54_PERTURB = ("perturb.none", "perturb.del_tool", "perturb.del_param", "perturb.del_result", "perturb.null_del")

# ---- T55 ---------------------------------------------------------------------------------------------------
T55_CELLS = ("explicit_transient", "explicit_permanent", "implicit_first", "implicit_recurrence", "ambiguous")
TRANSIENT_CLASSES = ("transient_unavailable", "rate_limited")
ERROR_CLASSES = ("transient_unavailable", "rate_limited", "auth_denied", "invalid_named_arg", "invalid_unnamed",
                 "unsupported_op", "quota_exhausted", "irrecoverable")
VIOLATION_TYPES = ("empty_when_count_stated", "negative_value", "id_not_in_prior_list", "parts_total_mismatch",
                   "duplicate_in_unique_list", "order_violation", "scale_mismatch", "stale_echo")
HELDOUT_SEED = "t55-heldout-violation-types-v1"       # fixed before any pilot; the draw below is reproducible


def draw_heldout_types(seed=HELDOUT_SEED):
    """Seeded draw of the 2 violation types held out of training (dev-only rows, outside the 3,000)."""
    ranked = sorted(VIOLATION_TYPES, key=lambda t: hashlib.sha256(("%s|%s" % (seed, t)).encode()).hexdigest())
    return tuple(sorted(ranked[:2]))


HELDOUT_TYPES = draw_heldout_types()
TRAIN_TYPES = tuple(t for t in VIOLATION_TYPES if t not in HELDOUT_TYPES)


def t55_cell(rec):
    """2x2 cell of a T55 record, from VISIBLE facts only:
       B1 (and B4 pairs, B5): explicit; transient iff the error class is transient/rate-limited, else permanent.
       B6 (polling) is explicit x transient. B2 is the ambiguous class.
       B3 (implicit): 'transient' = first occurrence, 'permanent' = recurrence (attempt index >= 2).
    NOTE (spec arithmetic): the G0-lite maps implicit x transient to 'B3 RETRY', which is only ~2.7% of the family and
    cannot meet the >= 8% cell bar of P-3. The persistence reading above (first occurrence vs recurrence, both visible
    in the attempt history) is used instead; the orchestrator/Opus must acknowledge this reading."""
    sb = rec["sub_block"]
    if sb == "b2_ambig_write":
        return "ambiguous"
    if sb == "b3_implicit":
        return "implicit_first" if rec["attempt"] == 1 else "implicit_recurrence"
    if sb == "b6_loop_poll":
        return "explicit_transient"
    if sb == "b5_deny_escalate":
        return "explicit_permanent"
    return "explicit_transient" if rec["error"]["class"] in TRANSIENT_CLASSES else "explicit_permanent"


# ---- T56 ---------------------------------------------------------------------------------------------------
REASONS = ("unmet_criterion", "short_coverage", "stale_evidence", "wrong_target", "ledger_mismatch",
           "dead_or_demo_only", "unverified", "stray_change")
FAULT_REASON = {
    "f_unmet": "unmet_criterion", "f_count_short": "short_coverage", "f_skipped": "short_coverage",
    "f_stale_run": "stale_evidence", "f_wrong_target": "wrong_target", "f_ledger_dup": "ledger_mismatch",
    "f_ledger_missing": "ledger_mismatch", "f_demo_only": "dead_or_demo_only", "f_no_check": "unverified",
    "f_stray": "stray_change", "f_stale_final": "stale_evidence", "f_failing_prior": "unmet_criterion",
    "f_none": "none",
}
# precedence: the first failing condition wins (single-fault rows make this matter only for validation)
PRECEDENCE_D1 = ("unverified", "unmet_criterion", "wrong_target", "stale_evidence", "short_coverage",
                 "ledger_mismatch", "dead_or_demo_only")
PRECEDENCE_D4 = ("unverified", "unmet_criterion", "wrong_target", "stale_evidence", "stray_change",
                 "short_coverage", "ledger_mismatch", "dead_or_demo_only")
# HARD BIN: the signal is a RELATION (count vs listed items, rev order, target vs deliverable, ledger count vs claim,
# graph reachability) rather than a literal failing word.
HARD_FAULTS = ("f_count_short", "f_stale_run", "f_wrong_target", "f_ledger_dup", "f_ledger_missing", "f_demo_only",
               "f_stale_final")
EASY_FAULTS = ("f_unmet", "f_skipped", "f_no_check", "f_stray", "f_failing_prior")
DEMO_VARIANTS = ("import_not_wired", "flag_default_off", "unreachable_branch", "helper_never_called")
