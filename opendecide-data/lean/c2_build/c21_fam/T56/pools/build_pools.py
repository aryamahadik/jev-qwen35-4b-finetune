"""T56 DONE-CLAIM (done-claim half) reword pools (lane L-T). Program expansion of Claude-written parts; drop-only round
trip against the seed template of each form (slot set, numbers, negation count). No labels, no gold, no benchmark text.
The closing-claim pool is ONE shared pool for every sub-block (the claim must not reveal the fault family), used with
both labels. Test-gaming wording (T56g) is lane L-C and is not in this file.

Run: python3 build_pools.py   (writes wording_pool_v1.json and pool_manifest.json next to this file)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
ROOT = os.path.dirname(FAM)
for p in (ROOT, FAM):
    if p not in sys.path:
        sys.path.insert(0, p)

from tool_engine import wording_expand as X  # noqa: E402
import t56_wording as SEEDS  # noqa: E402

Q_PREFIX = ["", "Given this turn, ", "In this turn, ", "Looking at the context, ", "Based on the turn so far, ",
            "At this point, ", "Considering the conversation, "]
CRIT_PREFIX = ["", "Check: ", "Criterion: ", "Requirement: ", "Condition: ", "Acceptance: ", "Rule: "]

# ---- closing claims: every claim carries {entity} (seed0 slot set) and no negation (seed0 has none) ----
CLAIM = [
    [["Done:", "Finished:", "Complete:", "Wrapped up:"], ["the {entity} work", "the {entity} change", "the {entity} task"],
     [" is complete and verified.", " is complete and confirmed.", " is finished and checked."]],
    [["All done.", "That is everything.", "I am finished."], ["The {entity} change", "The {entity} task", "The {entity} work"],
     [" is ready.", " is finished.", " is complete."]],
]

CRIT = {
    "status_is": ["{item} has status {value}", "{item} is in status {value}", "{item} shows the status {value}",
                  "{item} reads status {value}", "{item} is marked with status {value}", "{item} is set to status {value}",
                  "{item} stands at status {value}", "{item} carries status {value}", "{item} has the status {value}",
                  "{item} is at status {value}"],
    "equals": ["the {field} of {item} equals {value}", "{item} carries {field} {value}", "{item} has {field} equal to {value}",
               "the {field} recorded for {item} equals {value}", "{item} shows {field} {value}", "the {field} of {item} is {value}",
               "{item} holds {field} {value}", "the value of {field} for {item} equals {value}", "{field} on {item} equals {value}",
               "{item} is recorded with {field} {value}"],
    "exists": ["{item} exists", "{item} is present", "{item} is there", "{item} is in place", "{item} is available",
               "{item} can be found", "{item} is on record", "{item} is in the store"],
    "absent": ["{item} no longer exists", "{item} is no longer present", "{item} is no longer there", "{item} is no longer on record",
               "{item} is no longer in the store", "{item} no longer appears", "{item} is no longer available",
               "{item} has been removed and no longer exists", "{item} has been removed; it no longer exists"],
    "count_eq": ["the {entity} list holds exactly {value} entries", "there are exactly {value} {entity} entries",
                 "the {entity} list has exactly {value} entries", "exactly {value} {entity} entries are held",
                 "the {entity} list contains exactly {value} entries", "the number of {entity} entries is exactly {value}",
                 "the {entity} list is exactly {value} entries long", "the {entity} list counts exactly {value} entries"],
    "unchanged": ["{item} is left untouched", "{item} stays as it was", "{item} keeps its earlier state", "{item} is unchanged",
                  "{item} remains as before", "{item} is left as it was", "{item} stays exactly as it was", "{item} is kept as it was"],
    "exactly_once": ["{item} receives the notice exactly once", "{item} gets exactly one notice", "{item} is sent the notice a single time",
                     "{item} receives one notice and only one", "the notice reaches {item} exactly once", "{item} is notified exactly once",
                     "exactly one notice is delivered to {item}", "{item} gets the notice one time only"],
    "reachable": ["{value} runs when {item} is run", "{value} is used by the {item} entrypoint", "{value} is reached from the {item} entrypoint",
                  "running {item} calls {value}", "the {item} entrypoint reaches {value}", "{value} is wired in and runs under {item}",
                  "{item} leads to {value} when it is run", "{value} is on the path from the {item} entrypoint"],
}

TASK = [
    [["Task:", "Job:", "Assignment:", "Work item:"],
     ["finish the {entity} work.", "complete the {entity} change.", "finish the {entity} task."],
     ["Acceptance criteria: {criteria}.", "It is done when: {criteria}.", "The criteria are: {criteria}."],
     ["Only files under {scope} may change.", "Changes are allowed only under {scope}.", "Only paths under {scope} may change."]],
]

QCORE = {
    "done": ["Is the task done?", "Should the agent's claim of completion be accepted?", "Is the job complete?", "Is the work finished?",
             "Has the task been completed?", "Is the assignment done?", "Does the task count as complete?",
             "Should the completion claim stand?", "Is the claim of completion good enough to accept?"],
    "ready": ["Is the work ready to commit?", "Is this ready for a commit or pull request?", "Is the change ready to commit?",
              "Can this be committed now?", "Is the work ready for a commit?", "Is this ready to go into a pull request?",
              "Is the change in a state to commit?", "Is the work fit to commit?", "Can this go into a pull request as it stands?"],
}

OPT = {
    "DONE": [
        [["Yes, the task is done", "Yes, the work is done", "Yes, the task is complete", "Yes, the work is complete",
          "Yes, the job is finished", "Yes, the assignment is done"]],
        [["Yes", "Correct", "Agreed"], [", the task is done", ", the task is complete", ", the work is finished", ", the job is done",
                                       ", the claim holds"]],
        [["Accept the claim: it is done", "Accept the claim, the task is done", "Accept it: the task is done",
          "Accept that the work is complete", "Accept the claim, since the work is complete"]],
        [["Yes", "Agreed"], [", the task is finished", ", the work is complete"], [", accept the claim", ", and close it out",
                                                                              ", so the claim is accepted"]],
        [["Yes, the task is done and the claim stands", "Yes, the work is complete and the claim stands",
          "Yes, the task is finished and the claim is accepted", "Yes, the claim is accepted: the work is done"]],
        [["Yes", "Correct"], [", the work is done, so the claim is accepted", ", the task is done, so the claim is accepted",
                             ", the job is finished, so the claim is accepted"]],
        [["Yes, the task is done", "Yes, the work is complete"], [" and the claim is accepted", " and the completion claim holds"]],
    ],
    "CONTINUE": [
        [["No"], [", the agent should continue", ", the agent should keep working", ", the agent must continue", ", the agent should go on"]],
        [["No"], [", more work is needed", ", more work is still needed", ", the claim is premature", ", the work is still in progress"],
         [" and the agent should continue", " so the agent should keep going"]],
        [["Do not accept the claim", "Do not accept the completion claim"], [": more work is needed", ": the agent should continue",
                                                                        ": keep working"]],
        [["No, send the agent back", "No, return the work to the agent", "No, send it back to the agent"],
         [" to continue", " to keep working", " to finish the work"]],
        [["No", "No, the claim is premature", "No, the completion claim is premature"],
         [" and more work is needed", ", so more work is needed", ", with more work to do"]],
        [["No", "No, the work is unfinished", "No, the job is unfinished"],
         [", the agent should continue", ", the agent must keep working", ", the agent must go on"]],
        [["No, continue", "No, keep working"], [": the work is unfinished", ": the task is still open"]],
        [["No, the agent should continue"], [" because the work is unfinished"]],
        [["No, the agent should continue because more work is needed"]],
    ],
    "READY": [
        [["Yes, ready to commit", "Yes, the work is ready to commit", "Yes, this is ready to commit", "Yes, it is ready for a commit",
          "Yes, ready for a commit", "Yes, ready for a pull request", "Yes, the change is ready to commit",
          "Yes, ready to go into a pull request"]],
        [["Yes", "Correct"], [", it can be committed", ", it can go into a commit", ", it can go into a pull request", ", it is ready to commit"]],
        [["It can be committed", "It is ready to commit", "It can go into a commit", "The work can be committed now"]],
        [["Yes", "Agreed"], [", the change is ready", ", the work is ready"], [" to commit", " for a commit", " for a pull request"]],
        [["Commit it: ready", "Ready to commit: yes", "Ready: yes, commit it", "Go ahead and commit it"]],
        [["Yes, accept it for a commit", "Yes, accept the change for a commit", "Yes, approve the change for a pull request"]],
        [["Yes, ready to commit and open a pull request", "Yes, ready to commit and merge",
          "Yes, the work is ready to commit and open as a pull request"]],
        [["Yes", "Correct"], [", ready to commit now", ", ready for a commit now", ", ready to open a pull request"]],
        [["Yes, the change may be committed", "Yes, it may be committed", "Yes, the work may be committed"]],
        [["Yes, it can be committed now", "Yes, the change can be committed now"]],
    ],
    "NOT_READY": [
        [["No, not ready to commit", "No, not ready for a commit", "No, not ready for a pull request", "No, not ready to commit yet",
          "No, not ready to be committed", "No, not ready to open a pull request"]],
        [["No"], [", it must not be committed yet", ", it must not be committed", ", the change must not go into a commit",
                  ", the work must not be committed yet"]],
        [["No, it is not ready", "No, the work is not ready", "No, this change is not ready"],
         [" to commit", " for a commit", " to go into a pull request", " to be committed yet"]],
        [["Do not commit it", "Do not commit the change", "Do not commit the work"], [", not ready yet"]],
        [["No"], [", not ready: the change is still open", ", not ready: the work is still in progress", ", not ready: the claim is unverified"]],
        [["No, not ready to commit", "No, not ready for a pull request"], [" yet", " at this point", " until it is verified"]],
        [["No"], [", the change must not be committed yet", ", the work must not be committed at this point",
                  ", it must not go into a commit until verified"]],
        [["No, it is not ready", "No, this is not ready", "No, that is not ready"], [" to be committed", " for commit", " for the commit"]],
        [["No, it is still not ready", "No, that is still not ready", "No, this is still not ready"], [" to commit", " to be committed", " for a commit"]],
    ],
}


def candidates_for(form):
    if form == "claim.all":
        return list(X.expand_parts(CLAIM))
    if form.startswith("crit."):
        return list(X.expand_prefix_core(CRIT_PREFIX, CRIT[form[5:]]))
    if form == "task.all":
        return list(X.expand_parts(TASK))
    if form.startswith("q."):
        return list(X.expand_prefix_core(Q_PREFIX, QCORE[form[2:]]))
    if form.startswith("opt."):
        return list(X.expand_parts(OPT[form[4:]]))
    raise KeyError(form)


def main():
    seed_pools = SEEDS.seed_pool().pools
    out, stats, short = {}, {}, []
    for form in sorted(seed_pools):
        seed0 = seed_pools[form][0]
        try:
            kept, st = X.build_form(seed0, candidates_for(form), form)
        except ValueError as e:
            short.append(str(e))
            continue
        out[form] = kept
        stats[form] = st
    if short:
        raise SystemExit("SHORT FORMS:\n  " + "\n  ".join(short))
    with open(os.path.join(HERE, "wording_pool_v1.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    manifest = {
        "family": "T56", "pool": "wording_pool_v1", "forms": len(out),
        "min_per_form": min(len(v) for v in out.values()), "total_wordings": sum(len(v) for v in out.values()),
        "pool_sha256": X.pool_sha(out), "seed_module": "T56/t56_wording.py",
        "round_trip": "tool_engine.wording.reword_ok against the seed0 of each form; drop-only",
        "scope_note": "T56g (test-gaming half) is lane L-C; CARDS, REASON_TEXT and WARNINGS are not pooled here",
        "per_form": {k: {"count": len(out[k]), **stats[k]} for k in sorted(out)},
    }
    with open(os.path.join(HERE, "pool_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("forms", len(out), "min", manifest["min_per_form"], "total", manifest["total_wordings"], "sha", manifest["pool_sha256"][:16])


if __name__ == "__main__":
    main()
