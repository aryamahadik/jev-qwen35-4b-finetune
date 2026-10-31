"""families/T45/solver_b.py: solver B of T45 (paradigm set_algebra), written from G0_SPEC.md.

It imports nothing from the plugin, the executor or the texts module. parse() reads the RENDERED row: the layout is found
by its five line prefixes (B's own table), the intended effect and the two states become sets of (key, value) pairs, the
runner legend becomes {tag code: group} by keywords, and the options are read back to their label keys. solve_b() answers
by set algebra over those pairs and the legend's group: no execution, no tool model.
"""
from __future__ import annotations

import re

OUTCOMES = ("SUCCESS", "NEUTRAL", "SILENT_PARTIAL", "SILENT_WRONG", "LOUD_RETRYABLE", "LOUD_PERMANENT")
NEXT_MOVES = ("ADVANCE", "RETRY", "REPAIR_ARGS", "ESCALATE")
# (goal, before, command, result, after) line prefixes of every layout
PREFIXES = (
    ("Intended effect: ", "State before: ", "Command: ", "Result: ", "State after: "),
    ("# goal: ", "# before: ", "$ ", "# ", "# after: "),
    ("[goal] ", "[before] ", "[run] ", "[done] ", "[after] "),
    ("Expected: ", "Seen before: ", "Ran: ", "Outcome: ", "Seen after: "),
    ("goal: ", "before: ", "run: ", "result: ", "after: "),
    ("- want: ", "- was: ", "- ran: ", "- got: ", "- now: "),
    ("Plan: ", "Before I ran it: ", "I ran: ", "It returned: ", "Afterwards: "),
    ("Target: ", "Prior: ", "Invocation: ", "Status: ", "Posterior: "),
    ("Aim: ", "At the start: ", "Step: ", "Returned: ", "At the end: "),
    ("intent = ", "pre = ", "cmd = ", "res = ", "post = "),
)
GROUP_WORDS = (("0", r"no remark|nothing to report|no note"), ("H", r"person|someone"), ("A", r"argument|parameter"),
               ("T", r"temporary|transient|passing trouble"))
EXIT_RULE = re.compile(r"exit ([A-Z]{4}) when the step succeeded and exit ([A-Z]{4}) when it failed")
LEGEND_LINE = re.compile(r"^  ([A-Z]{4}) = (.+)$", re.M)
RESULT = re.compile(r"exit\W*([A-Z]{4})\W+(?:runner\W+)?tag\W*([A-Z]{4})")


def pairs_of(text: str) -> dict:
    out = {}
    if not text.strip():
        return out
    for part in text.split(", "):
        k, _, v = part.partition("=")
        out[k] = v
    return out


def parse(row: dict, ctx=None) -> dict:
    lines = row["state"].split("\n")
    if len(lines) != 5:
        raise ValueError("state is not five lines")
    pre = next((p for p in PREFIXES if all(l.startswith(x) for l, x in zip(lines, p))), None)
    if pre is None:
        raise ValueError("no layout matches")
    body = [l[len(x):] for l, x in zip(lines, pre)]
    m = RESULT.search(body[3])
    if not m:
        raise ValueError("result line")
    legend = {}
    for code, text in LEGEND_LINE.findall(row["instructions"]):
        grp = next((g for g, rx in GROUP_WORDS if re.search(rx, text)), None)
        if grp is None:
            raise ValueError(f"legend line {code}")
        legend[code] = grp
    em = EXIT_RULE.search(row["instructions"])
    if not em:
        raise ValueError("exit rule")
    opts = [o.split(" (")[0] for o in row["options"]]
    if all(o in OUTCOMES for o in opts):
        qform = "ch_outcome"
    elif all(o in NEXT_MOVES for o in opts):
        qform = "ch_move"
    else:
        raise ValueError("options are neither outcomes nor moves")
    return {"qform": qform, "legend": legend, "intent": pairs_of(body[0]), "before": pairs_of(body[1]),
            "after": pairs_of(body[4]), "command": body[2], "exit": m.group(1), "ok_exit": em.group(1), "tag": m.group(2),
            "options": opts}


def solve_b(view: dict):
    want = set(view["intent"].items())
    was = set(view["before"].items())
    now = set(view["after"].items())
    group = view["legend"][view["tag"]]
    reported_ok = view["exit"] == view["ok_exit"]
    complete = want <= now
    if view["qform"] == "ch_move":
        if reported_ok and complete:
            return "ADVANCE"
        return {"T": "RETRY", "A": "REPAIR_ARGS", "H": "ESCALATE", "0": "REPAIR_ARGS"}[group]
    if not reported_ok:
        return "LOUD_RETRYABLE" if group == "T" else "LOUD_PERMANENT"
    newly = (want & now) - was
    now_by_key = dict(now)
    other_value = [k for k, v in want if k in now_by_key and now_by_key[k] != v]
    if complete:
        return "SUCCESS" if newly else "NEUTRAL"
    if newly and not other_value:
        return "SILENT_PARTIAL"
    return "SILENT_WRONG"
