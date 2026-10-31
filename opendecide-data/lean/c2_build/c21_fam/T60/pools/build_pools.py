"""T60 reword pools (lane L-K). Program expansion of Claude-written parts; drop-only round trip against the seed template of each form (slot set,
numbers, negation count; GV12 two-way: no alternative adds a decision-bearing word the seed lacks). >= 50 wordings per QUESTION form and per CARD
CLAUSE (K14). No labels, no gold, no benchmark text; names enter only through {slot} placeholders filled from namespace.py.

Run: python3 -I build_pools.py   (writes wording_pool_v1.json and pool_manifest.json next to this file)
"""
import itertools
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
from tool_engine.wording import reword_ok, template_slots  # noqa: E402
import t60_wording as SEEDS  # noqa: E402

PRE = ["", "Rule: ", "Policy: ", "Card rule: ", "Note: ", "In this card: "]
TAIL = ["", " (this is one of the conditions)", " (it is part of the rule)"]


def _qs(openers, cores, tails=("",)):
    return [[openers, cores, list(tails)]]


EXPAND = {
    "q.h1": [[["", "In this case, ", "For this subtask, ", "Given the brief, ", "On these facts, "],
              ["should the agent", "should the assistant"],
              ["hand this subtask to a separate worker", "delegate this subtask to a separate worker", "pass this subtask to a separate worker",
               "send this subtask to a separate worker"],
              [", or"], ["do it itself in this thread", "do it itself in the main thread", "carry it out itself here", "handle it in this thread"],
              ["?"]]],
    "q.h2": _qs(["At the context summary,", "When the context is summarised,", "At summary time,", "As the context is summarised,", "For the summary,",
                 "While summarising the context,"],
                ["should this fact be kept in the summary or dropped?", "is this fact kept in the summary or dropped?",
                 "should this fact go into the summary or be left out?", "should this fact stay in the summary or be dropped?",
                 "is this fact carried into the summary or dropped?"], ["", " Decide for this fact only."]),
    "q.h3": [[["", "For this task, ", "Given the request, ", "At this point, ", "Before starting, "],
              ["should the agent", "does the agent need to"], ["write out a plan before acting", "draw up a plan before acting",
                                                              "put a plan down before acting", "plan the steps before acting"],
              [", or"], ["act now", "go ahead and act now", "just act now", "start acting now"], ["?"]]],
    "clause.d_size": [[PRE, ["Hand a subtask to a separate worker only when ALL four conditions hold.", "Delegate a subtask only when all four conditions hold.",
                             "A subtask goes to a separate worker only when all four conditions hold."],
                       [" First: it has at least {s} steps or reads at least {v} tokens in all.", " First: it has at least {s} steps, or it reads at least {v} tokens.",
                        " First: it has {s} or more steps, or it reads {v} or more tokens."]]],
    "clause.d_brief": [[PRE, ["Second: the worker needs at most {b} facts from the main thread.", "Second: no more than {b} facts from the main thread are needed.",
                              "Second: the worker needs {b} or fewer facts from the main thread.", "Second: at most {b} facts from the main thread are required."],
                        TAIL]],
    "clause.d_bound": [[PRE, ["Third: the worker returns at most {r} tokens.", "Third: its result is at most {r} tokens long.",
                              "Third: the worker returns {r} tokens or fewer.", "Third: the result it hands back is at most {r} tokens."], TAIL]],
    "clause.d_free": [[PRE, ["Fourth: it writes no resource the main thread also uses, and it does not depend on a pending main step. Otherwise do it in this thread.",
                             "Fourth: it shares no written resource with the main thread and needs no pending main step. Otherwise do it here.",
                             "Fourth: it writes nothing the main thread also uses, and it waits for no pending main step. Otherwise do it in this thread.",
                             "Fourth: no resource it writes is also used by the main thread, and no pending main step feeds it. Otherwise do it here."], TAIL]],
    "clause.k_rule": [[PRE, ["Keep a fact in the summary if a step still to run will take it from the conversation context.",
                             "A fact belongs in the summary when a step still waiting to run takes it from the conversation context.",
                             "Put a fact in the summary when some step still to run will take it from the conversation context.",
                             "A fact is kept in the summary if a step still waiting to run takes it from the conversation context."], TAIL]],
    "clause.k_recover_on": [[PRE, ["Steps that only run if something fails (rollback, retry, read-back) count as steps still to run.",
                                   "A step that runs only on failure (rollback, retry, read-back) counts as a step still to run.",
                                   "Rollback, retry and read-back steps that run only on failure count as steps still to run.",
                                   "A step that only runs when something fails (rollback, retry, read-back) counts as still to run."], TAIL]],
    "clause.k_recover_off": [[PRE, ["Steps that only run if something fails (rollback, retry, read-back) do not count as steps still to run.",
                                    "A step that runs only on failure (rollback, retry, read-back) does not count as a step still to run.",
                                    "Rollback, retry and read-back steps that run only on failure do not count as steps still to run.",
                                    "A step that only runs when something fails (rollback, retry, read-back) does not count as still to run."], TAIL]],
    "clause.p_r1": [[PRE, ["Write a plan first only when ALL three conditions hold. First: some step is high stakes, meaning it cannot be undone, reaches "
                           "outside the team, or changes {h} or more {unit_pl}.",
                           "Plan before acting only when all three conditions hold. First: some step is high stakes (it cannot be undone, reaches outside "
                           "the team, or changes {h} or more {unit_pl}).",
                           "A plan comes first only when all three conditions hold. First: some step is high stakes, which means it cannot be undone, "
                           "reaches outside the team, or changes {h} or more {unit_pl}."], TAIL]],
    "clause.p_r2": [[PRE, ["Second: the task has at least {n} steps.", "Second: there are at least {n} steps in the task.",
                           "Second: the task has {n} or more steps.", "Second: the task is made of at least {n} steps."], TAIL]],
    "clause.p_r3": [[PRE, ["Third: the request does not say in what order the steps must run. Otherwise act.",
                           "Third: the order of the steps is not given in the request. Otherwise act.",
                           "Third: the request gives no order for the steps. Otherwise act.",
                           "Third: nothing in the request says in what order the steps run. Otherwise act."], TAIL]],
    "opt.DELEGATE": [[["Hand", "Pass", "Send", "Give"], [" the subtask to a separate worker"], [" with a brief", " along with a brief", " together with a brief",
                                                                                                  ""], [""]]],
}


def build(min_per_form=50):
    seeds = SEEDS.seed_pool().pools
    pools = {k: list(v) for k, v in seeds.items()}
    per = {}
    for form, specs in EXPAND.items():
        seed0 = seeds[form][0]
        seen, kept, rt, dup = set(), [], 0, 0
        for s in (x.replace(" ?", "?").replace("  ", " ").strip() for x in X.expand_parts(specs)):
            if s in seen:
                dup += 1
                continue
            if not reword_ok(seed0, s):
                rt += 1
                continue
            seen.add(s)
            kept.append(s)
        need = 12 if form.startswith("opt.") else min_per_form
        if len(kept) < need:
            raise ValueError("form %s has %d wordings (need %d)" % (form, len(kept), need))
        for t in seeds[form]:
            if t not in kept:
                kept.append(t)
        pools[form] = kept
        per[form] = dict(candidates=len(kept) + rt + dup, count=len(kept), dropped_roundtrip=rt, dropped_duplicate=dup, slots=sorted(template_slots(seed0)))
    for form, ws in pools.items():
        per.setdefault(form, dict(count=len(ws), seed_only=True))
    return pools, per


def main():
    pools, per = build()
    with open(os.path.join(HERE, "wording_pool_v1.json"), "w", encoding="utf-8") as f:
        json.dump(pools, f, indent=1, sort_keys=True)
        f.write("\n")
    man = dict(family="T60", forms=len(pools), min_per_form=50, per_form=per, pool_sha256=X.pool_sha(pools),
               note="forms marked seed_only keep their Claude-written seeds until the Haiku reword pass")
    with open(os.path.join(HERE, "pool_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1, sort_keys=True)
        f.write("\n")
    print("forms", len(pools), "sha", man["pool_sha256"])


if __name__ == "__main__":
    main()
