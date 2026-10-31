"""families/T45/texts.py: the fixed program text of T45 rows (rules, runner-tag legends, layouts, question wordings).

Plain constants shared by the renderer; solver B keeps its own copy of the layouts and keywords (independence). Rules are
printed in `instructions` (counted twice by the 800-token budget), so they are short: the head decides which rules block
a row carries (outcome rules or next-move rules). The legend lists EVERY tag of the card's runner in every row (the tag
a row shows is one of them), so the tag text never tells the label by itself: the row has to be joined to the legend.
"""
from __future__ import annotations

import random

LABELS = ("SUCCESS", "NEUTRAL", "SILENT_PARTIAL", "SILENT_WRONG", "LOUD_RETRYABLE", "LOUD_PERMANENT")
MOVES = ("ADVANCE", "RETRY", "REPAIR_ARGS", "ESCALATE")
QFORMS = ("ch_outcome", "ch_move")
# printed option texts: the label plus a gloss, so that no two outcome options have the same length (the kit's length-rank
# balance counts ties as equal); the key (left of " (") is what the row means
DISPLAY = {"SUCCESS": "SUCCESS", "NEUTRAL": "NEUTRAL (no-op)", "SILENT_PARTIAL": "SILENT_PARTIAL",
           "SILENT_WRONG": "SILENT_WRONG", "LOUD_RETRYABLE": "LOUD_RETRYABLE (temp)", "LOUD_PERMANENT": "LOUD_PERMANENT (final)",
           "ADVANCE": "ADVANCE", "RETRY": "RETRY", "REPAIR_ARGS": "REPAIR_ARGS", "ESCALATE": "ESCALATE"}

GROUP_TEXT = {
    "T": ("temporary condition; the same step may work when run again",
          "transient problem; running the step again as it is may succeed",
          "passing trouble; the identical step may succeed on another try"),
    "A": ("the arguments or the input are wrong; fix them, then run again",
          "bad arguments or bad input; correct them and run again",
          "wrong parameters or data; change them and run again"),
    "H": ("blocked by a rule or missing rights; a person has to act",
          "refused for lack of permission or by policy; a person must step in",
          "not allowed here; someone with more rights has to act"),
    "0": ("no remark", "nothing to report", "no note from the runner"),
}
N_LEGENDS = 16
# the step as planned (what the agent meant to run): the same for every fault of a kind; the executed variant (another
# branch, a typo, extra flags) is the hidden cause and is not printed, so the command line carries no fault-specific token
PLANNED = {
    "git": "git push origin QBR",
    "db": "python dbload.py data/shop.db batch.csv",
    "http": "curl -s -X POST -H 'X-Key: k1' -d @batch.json http://127.0.0.1:8080/v1/QRES/batch",
    "build": "make all",
    "tests": "python -m unittest discover -s QD0 -p 'test_*.py' -v",
}

HEAD_RULES = {
    "ch_outcome": (
        "Judge one step of an agent run. The runner reports exit {ok} when the step succeeded and exit {fail} when it failed (runner build {build}). The "
        "intended effect is a list of key=value items; an item holds in a state when its key has exactly that value "
        "(other keys do not matter).\nRunner tags:\n{legend}"),
    "ch_move": (
        "Judge one step of an agent run. The runner reports exit {ok} when the step succeeded and exit {fail} when it failed (runner build {build}). The "
        "intended effect is a list of key=value items; an item holds in a state when its key has exactly that value "
        "(other keys do not matter).\nRunner tags:\n{legend}"),
}
# printed once, as the definition lines of the SHOWN options (card field; decoder_io appends them to the option lines)
DEFS = {
    "SUCCESS": "the step reported success, every intended item holds after the step, and at least one did not hold before",
    "NEUTRAL": "the step reported success, and every intended item already held before the step",
    "SILENT_PARTIAL": "the step reported success, some intended items newly hold, the others are missing, and no intended key has another value",
    "SILENT_WRONG": "the step reported success, and no intended item newly holds, or an intended key has another value",
    "LOUD_RETRYABLE": "the step reported failure and the tag marks a temporary condition",
    "LOUD_PERMANENT": "the step reported failure and the tag is any other",
    "ADVANCE": "the step reported success and every intended item holds after the step",
    "RETRY": "not ADVANCE, and the tag marks a temporary condition",
    "REPAIR_ARGS": "not ADVANCE, and the tag marks wrong arguments or input, or has no remark",
    "ESCALATE": "not ADVANCE, and the tag marks a block that a person has to resolve",
}
WORDINGS = {
    "ch_outcome": ("Which outcome describes this step?",
                   "How should this step be classified?",
                   "Which label fits what happened in this step?"),
    "ch_move": ("What should the agent do after this step?",
                "Which move should the agent make after this step?",
                "What is the right move for the agent after this step?"),
}
QUESTION_MEANINGS = {
    "ch_outcome": "asks which of the outcome labels describes the step, from its exit status, runner tag and states",
    "ch_move": "asks which move the agent should make after the step: advance, retry, repair the arguments or escalate",
}
# layouts: (goal, before, command, result, after) line prefixes; the command line may carry a prompt.
LAYOUTS = {
    "plain": ("Intended effect: ", "State before: ", "Command: ", "Result: exit {n}, runner tag {t}", "State after: "),
    "terminal": ("# goal: ", "# before: ", "$ ", "# exit {n} tag {t}", "# after: "),
    "ci": ("[goal] ", "[before] ", "[run] ", "[done] exit={n} tag={t}", "[after] "),
    "ticket": ("Expected: ", "Seen before: ", "Ran: ", "Outcome: exit {n}; tag {t}", "Seen after: "),
    "yaml": ("goal: ", "before: ", "run: ", "result: {{exit: {n}, tag: {t}}}", "after: "),
    "bullets": ("- want: ", "- was: ", "- ran: ", "- got: exit {n}, tag {t}", "- now: "),
    "chat": ("Plan: ", "Before I ran it: ", "I ran: ", "It returned: exit {n}, tag {t}", "Afterwards: "),
    "report": ("Target: ", "Prior: ", "Invocation: ", "Status: exit {n}, tag {t}", "Posterior: "),
    "memo": ("Aim: ", "At the start: ", "Step: ", "Returned: exit {n}, tag {t}", "At the end: "),
    "journal": ("intent = ", "pre = ", "cmd = ", "res = exit {n} tag {t}", "post = "),
}
REGISTERS = tuple(LAYOUTS)
HELD_OUT_REGISTERS = ("memo", "journal")


def legend_of(legend_id: int) -> dict:
    """The tag codes, the phrasing indexes and the line order of one legend (16 legends)."""
    R = random.Random(f"T45-legend-{legend_id}")
    import string
    codes = []
    while len(codes) < 6:                       # opaque 4-letter codes: no digit, so no numeric feature can carry the tag or the exit
        c = "".join(R.choice(string.ascii_uppercase) for _ in range(4))
        if c not in codes:
            codes.append(c)
    ph = [R.randrange(3) for _ in range(4)]
    order = R.sample(range(4), 4)
    groups = ("T", "A", "H", "0")
    return {"codes": dict(zip(groups, codes[:4])), "phr": dict(zip(groups, ph)),
            "order": [groups[i] for i in order], "ok_exit": codes[4], "fail_exit": codes[5],
            "build": R.randrange(10000, 99999)}


def legend_lines(legend_id: int) -> list:
    L = legend_of(legend_id)
    return [f"  {L['codes'][g]} = {GROUP_TEXT[g][L['phr'][g]]}" for g in L["order"]]


def rules_text(qform: str, legend_id: int) -> str:
    L = legend_of(legend_id)
    return HEAD_RULES[qform].format(legend="\n".join(legend_lines(legend_id)), ok=L["ok_exit"], fail=L["fail_exit"], build=L["build"])
