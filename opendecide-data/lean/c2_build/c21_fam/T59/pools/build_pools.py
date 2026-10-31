"""T59 reword pools (lane L-K). Program expansion of Claude-written parts; drop-only round trip against the seed template of each form (slot
set, numbers, negation count, GV12 two-way: no alternative adds a decision-bearing word the seed does not have). No labels, no gold, no
benchmark text; entity / field / value names enter only through {slot} placeholders filled from namespace.py.
The >= 50 wordings per QUESTION form (K15) are met here; the Haiku reword pass may add more (two-way slot round trip, GV12).

Run: python3 -I build_pools.py   (writes wording_pool_v1.json and pool_manifest.json next to this file)
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
from tool_engine.wording import reword_ok, template_slots  # noqa: E402
import t59_wording as SEEDS  # noqa: E402

A_ASK = ["stop and ask the user", "ask the user first", "pause and ask the user", "check with the user first"]
B_GO = ["carry on without asking", "go ahead without asking", "continue without asking", "proceed without asking"]
Q_MID = [
    [["Partway through the task,", "At this point in the run,", "In the middle of the run,", "Midway through the work,", "So far into the task,"],
     ["should the agent"], A_ASK, [", or"], B_GO, ["?"]],
    [["Should the agent"], A_ASK, [", or"], B_GO, ["at this point in the run?", "partway through the task?", "in the middle of the run?"]],
]
Q_EARLY = [
    [["Before its first change,", "Before it changes anything,", "Ahead of the first change,", "At the very start of the work,"],
     ["should the agent"], A_ASK, [", or"], B_GO, ["?"]],
    [["The agent is about to make its first change. Should it", "The agent has not changed anything yet. Should it"], A_ASK, [", or"], B_GO, ["?"]],
]
O_ASK = [[["Stop and ask", "Pause and ask", "Halt and ask", "Stop here and ask"], ["the user", "the person", "the requester"],
          ["before going on", "before the next step", "before doing anything else", "before acting", "first"]]]
O_GO = [[["Carry on", "Go ahead", "Continue", "Proceed"], ["with the next step", "with the plan", "on its own", ""],
         ["without asking the user", "without asking", "without checking with the user", "without pausing to ask"]]]
EXPAND = {"q.mid": Q_MID, "q.early": Q_EARLY, "opt.ASK": O_ASK, "opt.PROCEED": O_GO}


def build(min_per_form=50):
    seeds = SEEDS.seed_pool().pools
    pools = {k: list(v) for k, v in seeds.items()}
    per = {}
    for form, specs in EXPAND.items():
        seed0 = seeds[form][0]
        seen, kept, rt, dup = set(), [], 0, 0
        for s in (x.replace(" ?", "?") for x in X.expand_parts(specs)):
            if s in seen:
                dup += 1
                continue
            if not reword_ok(seed0, s):
                rt += 1
                continue
            seen.add(s)
            kept.append(s)
        if len(kept) < min_per_form:
            raise ValueError("form %s has %d wordings (need %d)" % (form, len(kept), min_per_form))
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
    man = dict(family="T59", forms=len(pools), min_per_form=50, per_form=per, pool_sha256=X.pool_sha(pools),
               note="forms marked seed_only keep their Claude-written seeds until the Haiku reword pass")
    with open(os.path.join(HERE, "pool_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, indent=1, sort_keys=True)
        f.write("\n")
    print("forms", len(pools), "sha", man["pool_sha256"])


if __name__ == "__main__":
    main()
