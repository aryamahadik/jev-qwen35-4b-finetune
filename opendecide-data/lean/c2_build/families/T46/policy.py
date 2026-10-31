"""families/T46/policy.py: the T46 policy cards and the decision engine (solver A: an ordered first-match rule engine).

A row's decision is `decide(card, wf, vals)`:
  active(flag)   a flag is ACTIVE when its printed value equals the problem value of the phrasing the row uses
                 (phrasing 0: problem = true; phrasing 1: problem = false)
  card           {"order": [classes], "lines": {cls: {"flags": [fid], "num": bool}}, "ignore": [fid], "inclusive": bool,
                  "note": bool}; the first class in `order` that has an active line condition decides, else P.
  plain card     the intrinsic table: every class H / D / E flag in its own class, the numeric pair in the class named
                 by its limit field's suffix, strict "above", alarm flags uncovered; order D, E, H (never ties: plain
                 rows have at most one covered active condition).
  stated card    8 variants per workflow: some flags re-mapped to another class, some dropped into the "never counted"
                 list, the numeric re-mapped, "above" or "at or above", and a priority order; every class keeps a line.
"""
from __future__ import annotations

import random

from . import tables as T

PRIORITY_PLAIN = ("D", "E", "H")
N_VARIANTS = 8


def flags_of(wf: str) -> list:
    return T.FLAGS[wf]


def problem_class(wf: str, fid: str) -> str:
    return next(c for f, c, _a, _b in T.FLAGS[wf] if f == fid)


def flag_name(wf: str, fid: str, phr: int) -> str:
    _f, _c, a, b = next(x for x in T.FLAGS[wf] if x[0] == fid)
    return a if phr == 0 else b


def problem_value(phr: int) -> bool:
    return phr == 0


def is_active(phr: int, printed: bool) -> bool:
    return printed == problem_value(phr)


def num_class(wf: str) -> str:
    limit = T.NUMERIC[wf][1]
    return next(c for s, c in T.SUFFIX_CLASS.items() if limit.endswith(s))


def plain_card(wf: str, flags: list | None = None) -> dict:
    flags = flags if flags is not None else T.FLAGS[wf]
    lines = {c: {"flags": [], "num": False} for c in ("H", "D", "E")}
    for fid, c, _a, _b in flags:
        if c in lines:
            lines[c]["flags"].append(fid)
    lines[num_class(wf)]["num"] = True
    ignore = [fid for fid, c, _a, _b in flags if c == "A"]
    return {"order": list(PRIORITY_PLAIN), "lines": lines, "ignore": ignore, "inclusive": False, "note": True,
            "kind": "plain"}


def stated_card(wf: str, variant: int, flags: list | None = None) -> dict:
    """Card variant `variant` of workflow `wf`: deterministic, label-blind, every class H / D / E keeps a condition."""
    flags = flags if flags is not None else T.FLAGS[wf]
    base = plain_card(wf, flags)
    for attempt in range(200):
        rng = random.Random(f"T46card|{wf}|{variant}|{attempt}")
        lines = {c: {"flags": [], "num": False} for c in ("H", "D", "E")}
        ignore = list(base["ignore"])
        for fid, c, _a, _b in flags:
            if c == "A":
                continue
            u = rng.random()
            if u < 0.18:
                ignore.append(fid)                                  # the card does not count this flag
                continue
            cls = c if u < 0.72 else rng.choice([x for x in ("H", "D", "E") if x != c])
            lines[cls]["flags"].append(fid)
        ncls = num_class(wf)
        if rng.random() >= 0.75:
            ncls = rng.choice([x for x in ("H", "D", "E") if x != ncls])
        lines[ncls]["num"] = True
        if all(lines[c]["flags"] or lines[c]["num"] for c in ("H", "D", "E")):
            order = ["H", "D", "E"]
            rng.shuffle(order)
            return {"order": order, "lines": lines, "ignore": sorted(ignore, key=lambda f: _index(flags, f)),
                    "inclusive": rng.random() < 0.30, "note": False, "kind": "stated"}
    raise ValueError(f"no stated card for {wf} variant {variant}")


def _index(flags: list, fid: str) -> int:
    return [f for f, *_ in flags].index(fid)


def card_for(wf: str, arm: str, variant: int, flags: list | None = None) -> dict:
    return plain_card(wf, flags) if arm == "plain" else stated_card(wf, variant, flags)


def over(num: int, lim: int, inclusive: bool) -> bool:
    return num >= lim if inclusive else num > lim


def line_hits(card: dict, cls: str, wf: str, vals: dict) -> list:
    """The conditions of line `cls` that hold: [("flag", fid) | ("num", None) | ("note", None)]."""
    ln = card["lines"].get(cls)
    hits = []
    if ln:
        hits += [("flag", f) for f in ln["flags"] if is_active(vals["phr"][f], vals["flags"][f])]
        if ln["num"] and over(vals["num"], vals["lim"], card["inclusive"]):
            hits.append(("num", None))
    if card.get("note") and vals.get("note_cls") == cls:
        hits.append(("note", None))
    return hits


def decide(card: dict, wf: str, vals: dict) -> str:
    for cls in card["order"]:
        if line_hits(card, cls, wf, vals):
            return cls
    return "P"


def covered_hits(card: dict, wf: str, vals: dict) -> dict:
    """{cls: [conditions that hold]} over the covered lines (the engine's evidence)."""
    return {c: h for c in card["order"] if (h := line_hits(card, c, wf, vals))}


def uncovered_flags(card: dict, flags: list) -> list:
    """Flags no line covers (alarm flags and flags the card does not count)."""
    cov = {f for ln in card["lines"].values() for f in ln["flags"]}
    return [f for f, *_ in flags if f not in cov]
