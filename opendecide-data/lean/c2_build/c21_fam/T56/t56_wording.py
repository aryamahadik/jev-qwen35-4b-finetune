"""T56 SEED wordings (Claude-authored; a handful per form). >= 50 claim wordings and >= 50 per question form come from the
Haiku reword pass (reword-only, slot round trip, drop-only). The closing-claim pool is used with BOTH labels."""
from tool_engine.wording import WordingPool

CLAIMS = {  # ONE shared pool for every sub-block: the closing claim must not reveal which fault family a row belongs to
    "all": ["Done: the {entity} work is complete and verified.", "Everything is finished and ready to be committed.",
            "The {entity} task is complete; all the criteria are met.", "I have finished the {entity} work and checked it.",
            "All done. The {entity} change is ready.", "Finished: every requirement is in place.",
            "The {entity} work is complete and confirmed.", "That is everything: the {entity} change is finished."],
}
CRITERIA = {
    "status_is": ["{item} has status {value}", "the status of {item} is {value}"],
    "equals": ["the {field} of {item} equals {value}", "{item} carries {field} {value}"],
    "exists": ["{item} exists", "{item} is present"],
    "absent": ["{item} no longer exists", "{item} is gone"],
    "count_eq": ["the {entity} list holds exactly {value} entries", "there are exactly {value} {entity} entries"],
    "unchanged": ["{item} is left untouched", "{item} stays as it was"],
    "exactly_once": ["{item} receives the notice exactly once", "{item} gets exactly one notice"],
    "reachable": ["{value} runs when {item} is run", "{value} is used by the {item} entrypoint"],
}
TASK = {  # ONE shared template pool for every sub-block (P-7: the task text must not reveal the fault family)
    "all": ["Task: finish the {entity} work. Acceptance criteria: {criteria}. Only files under {scope} may change.",
            "Task: complete the {entity} change. It is done when: {criteria}. Changes are allowed only under {scope}."],
}
QUESTION = {
    "done": ["Is the task done?", "Should the agent's claim of completion be accepted?"],
    "ready": ["Is the work ready to commit?", "Is this ready for a commit or pull request?"],
}
OPTIONS = {
    "DONE": ["Yes, the task is done", "Accept the claim: it is done"],
    "CONTINUE": ["No, the agent should continue", "Do not accept the claim: more work is needed"],
    "READY": ["Yes, ready to commit", "It can be committed"],
    "NOT_READY": ["No, not ready to commit", "It must not be committed yet"],
}
REASON_TEXT = {
    "unmet_criterion": "A criterion is visibly unmet", "short_coverage": "The check covered fewer items than required",
    "stale_evidence": "The passing check is older than the last change", "wrong_target": "The check ran against a different target",
    "ledger_mismatch": "An effect is duplicated or missing in the ledger", "dead_or_demo_only": "The behaviour is not reachable from the entrypoint",
    "unverified": "No check was run", "stray_change": "Files outside the declared scope changed", "none": "Nothing is wrong",
}
CARDS = {
    "card.t56.evidence_required": "Policy: accept a done claim only if checks on the deliverable show every criterion met, cover every listed item, "
                                   "and come after the last change. A claim alone is not evidence.",
    "card.t56.fresh_run_required": "Policy: accept a done claim only if a check on the deliverable covering every listed item, run after the last "
                                    "change (revision stamps show order), shows every criterion met. Optional items may be skipped.",
    "card.t56.scope_declared": "Policy: ready only if fresh, complete checks on the deliverable show every criterion met, the last full check "
                               "follows the last edit, and no path outside the declared scope changed.",
    "card.t56.entrypoint_reach": "Policy: accept a done claim only if fresh, complete checks show every criterion met and the tested behaviour is "
                                  "reachable from the entrypoint (imports wired, guards on, calls present).",
}
WARNINGS = ["deprecated option used", "slow response", "cache was cold", "budget unchanged", "minor clock drift"]
LANG = {"python": dict(ext=".py", imp="import", runner="runner.pytest"), "javascript": dict(ext=".js", imp="import", runner="runner.node_test"),
        "go": dict(ext=".go", imp="import", runner="runner.go_test"), "bash": dict(ext=".sh", imp="source", runner="runner.plain_script_exit_status")}


def seed_pool():
    p = WordingPool()
    for k, ts in CLAIMS.items():
        p.add("claim.%s" % k, ts)
    for k, ts in CRITERIA.items():
        p.add("crit.%s" % k, ts)
    for k, ts in TASK.items():
        p.add("task.%s" % k, ts)
    for k, ts in QUESTION.items():
        p.add("q.%s" % k, ts)
    for k, ts in OPTIONS.items():
        p.add("opt.%s" % k, ts)
    return p
