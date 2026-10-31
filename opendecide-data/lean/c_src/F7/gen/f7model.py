"""F7 rubric model and solver A (spec 2, 4.1, 3.4).

Card structure (Python dict, never shown to the parser or solver B):
  items: {key: item}; item kinds bool / num / date / ord, each with an up direction `dir` (+1: larger value or presence
         moves the case up the scale; -1: the reverse). Domains are grids (2.2): num multiples of r in [lo, hi]; dates
         day ordinals in [lo, hi]; ord rank indices; bool {False, True}.
  mode: ladder / highest / count / points / cut / grid; crits {k: crit} for k = 1..K-1 (ladder, highest);
        listed / weights / bands (count, points); qty / cuts / side / rising / integer (cut); grid rows.
  overrides: [{"type": "floor"|"cap", "cond": crit, "m": level}], winner ("cap"|"floor") when both.
Criterion trees: {"t": "atom", "a": atom} | and / or (inline, 2 parts) | allof / anyof (list; a nested list only last)
  | unless {"a": crit (atom or inline and of 2 atoms), "b": atom} | onlyif {"main": crit, "c": atom}.
Atoms: {"item", "op", "t", ...}: num/date/ord ops ">=", ">", "<=", "<"; date "within" (D <= v <= D + N); bool
  "present" / "absent". Wording choices (comparator word, negation form) are kept in the atom for the renderer.
Solver A: forward, imperative evaluation with exact arithmetic (Fraction, integer day ordinals).
"""
from __future__ import annotations

import datetime as dt
from fractions import Fraction

EPOCH = dt.date(2000, 1, 1)


def day(d: dt.date) -> int:
    return (d - EPOCH).days


def from_day(n: int) -> dt.date:
    return EPOCH + dt.timedelta(days=int(n))


# ------------------------------------------------------------------------------------------------ atoms and criteria
def eval_atom(a: dict, v: dict, *, flip_incl: str | None = None, within_excl: bool = False,
              rank_swap: bool = False) -> bool:
    """flip_incl: 'incl->excl' (C8 reading) or 'excl->incl' (C9 reading) on num atoms; for dates 'date' swaps
    before/after inclusivity (C10 reading 1); within_excl excludes both ends of 'within' (C10 reading 2);
    rank_swap swaps inclusivity on ordered-category atoms (C25 reading)."""
    x = v[a["item"]]
    op = a["op"]
    if op == "present":
        return bool(x)
    if op == "absent":
        return not bool(x)
    if op == "within":
        D, N = a["t"], a["N"]
        if within_excl:
            return D < x < D + N
        return D <= x <= D + N
    t = a["t"]
    kind = a.get("kind")
    if kind == "num" and flip_incl:
        if flip_incl == "incl->excl" and op in (">=", "<="):
            op = op[0]
        elif flip_incl == "excl->incl" and op in (">", "<"):
            op = op + "="
    if kind == "date" and flip_incl == "date":
        op = {">=": ">", ">": ">=", "<=": "<", "<": "<="}[op]
    if kind == "ord" and rank_swap:
        op = {">=": ">", ">": ">=", "<=": "<", "<": "<="}[op]
    if op == ">=":
        return x >= t
    if op == ">":
        return x > t
    if op == "<=":
        return x <= t
    if op == "<":
        return x < t
    raise ValueError(op)


def atoms_of(c: dict) -> list[dict]:
    t = c["t"]
    if t == "atom":
        return [c["a"]]
    if t in ("and", "or", "allof", "anyof"):
        return [a for p in c["parts"] for a in atoms_of(p)]
    if t == "unless":
        return atoms_of(c["a"]) + [c["b"]]
    if t == "onlyif":
        return atoms_of(c["main"]) + [c["c"]]
    raise ValueError(t)


def eval_crit(c: dict, v: dict, rd: dict | None = None) -> bool:
    rd = rd or {}
    t = c["t"]
    if t == "atom":
        return eval_atom(c["a"], v, flip_incl=rd.get("flip_incl"), within_excl=rd.get("within_excl", False),
                         rank_swap=rd.get("rank_swap", False))
    if t in ("and", "allof"):
        return all(eval_crit(p, v, rd) for p in c["parts"])
    if t in ("or", "anyof"):
        vals = [eval_crit(p, v, rd) for p in c["parts"]]
        if rd.get("or_exclusive"):
            return sum(vals) == 1
        return any(vals)
    if t == "unless":
        a = eval_crit(c["a"], v, rd)
        if rd.get("unless_ignored"):
            return a
        return a and not eval_crit({"t": "atom", "a": c["b"]}, v, rd)
    if t == "onlyif":
        m = eval_crit(c["main"], v, rd)
        cc = eval_crit({"t": "atom", "a": c["c"]}, v, rd)
        if rd.get("onlyif_as_if"):
            return m or cc
        return m and cc
    raise ValueError(t)


def n_ops(c: dict) -> int:
    """Operator count (2.3, R13)."""
    t = c["t"]
    if t == "atom":
        return 0
    if t in ("and", "or"):
        return 1 + sum(n_ops(p) for p in c["parts"])
    if t in ("allof", "anyof"):
        return len(c["parts"]) - 1 + sum(n_ops(p) for p in c["parts"])
    if t == "unless":
        return 1 + n_ops(c["a"])
    if t == "onlyif":
        return 1 + n_ops(c["main"])
    raise ValueError(t)


# ------------------------------------------------------------------------------------------------ level functions
def mode_level(card: dict, v: dict, rd: dict | None = None) -> int:
    rd = rd or {}
    K = card["K"]
    mode = card["mode"]
    if rd.get("mode_swap") and mode in ("ladder", "highest"):
        mode = "highest" if mode == "ladder" else "ladder"
    if mode == "ladder":
        lvl = 0
        for k in range(1, K):
            if eval_crit(card["crits"][k], v, rd):
                lvl = k
            else:
                break
        return lvl
    if mode == "highest":
        lvl = 0
        for k in range(1, K):
            if eval_crit(card["crits"][k], v, rd):
                lvl = k
        return lvl
    if mode in ("count", "points"):
        tot = count_total(card, v, rd)
        for k, (lo, hi) in enumerate(card["bands"]):
            if lo <= tot <= hi:
                return k
        raise ValueError(f"total {tot} in no band")
    if mode == "cut":
        return cut_level(card, v[card["qty"]], side_swap=rd.get("side_swap", False))
    if mode == "grid":
        lvl = 0
        for k in range(1, K):
            if all(eval_atom(a, v) for a in card["grid"][k]):
                lvl = k
        return lvl
    raise ValueError(mode)


def count_total(card: dict, v: dict, rd: dict | None = None) -> int:
    rd = rd or {}
    pts = card.get("weights") if card["mode"] == "points" and not rd.get("points_as_count") else None
    tot = 0
    for f in card["listed"]:
        if v[f]:
            n = rd.get("count_twice", {}).get(f, 1) if rd.get("count_twice") else 1
            tot += (pts[f] if pts else 1) * n
    if rd.get("fillers_count"):
        tot += sum(1 for f in card.get("fillers_on_row", []) if v.get(f))
    return tot


def cut_level(card: dict, x, *, side_swap: bool = False) -> int:
    cuts = card["cuts"]
    K = card["K"]
    if card["integer"]:
        j = sum(1 for c in cuts if x >= c)  # closed integer ranges: a cut is the lowest value of its range
    else:
        side = card["side"]
        if side_swap:
            side = "low" if side == "high" else "high"
        if side == "high":
            j = sum(1 for c in cuts if x >= c)
        else:
            j = sum(1 for c in cuts if x > c)
    return j if card["rising"] else K - 1 - j


def firing(card: dict, v: dict, rd: dict | None = None) -> tuple[bool, bool]:
    f = c = False
    for o in card.get("overrides", []):
        if eval_crit(o["cond"], v, rd):
            if o["type"] == "floor":
                f = True
            else:
                c = True
    return f, c


def final_level(card: dict, v: dict, rd: dict | None = None) -> int:
    rd = rd or {}
    M = mode_level(card, v, rd)
    ovs = card.get("overrides", [])
    if not ovs:
        return M
    fl = next((o for o in ovs if o["type"] == "floor"), None)
    cp = next((o for o in ovs if o["type"] == "cap"), None)
    ff, cf = firing(card, v, rd)
    if rd.get("ignore_floor"):
        ff = False
    if rd.get("ignore_cap"):
        cf = False
    if ff and cf:
        winner = card["winner"]
        if rd.get("prec_swap"):
            winner = "floor" if winner == "cap" else "cap"
        return cp["m"] if winner == "cap" else fl["m"]
    if ff:
        return max(M, fl["m"])
    if cf:
        return min(M, cp["m"])
    return M


def solve_a(card: dict, v: dict) -> int:
    """Solver A: gold level index."""
    return final_level(card, v)


# ------------------------------------------------------------------------------------------------ decisive path
def decisive_criterion(card: dict, v: dict) -> tuple[str, dict | None]:
    """(kind, crit) of the 2.7 decisive criterion D: ('override', cond) when an override is binding, else the mode's."""
    g = final_level(card, v)
    M = mode_level(card, v)
    if card.get("overrides") and g != M:
        ff, cf = firing(card, v)
        if ff and cf:
            w = card["winner"]
            return "override", next(o for o in card["overrides"] if o["type"] == w)["cond"]
        typ = "floor" if ff else "cap"
        return "override", next(o for o in card["overrides"] if o["type"] == typ)["cond"]
    K = card["K"]
    if card["mode"] == "ladder":
        return "level", card["crits"][g + 1] if g < K - 1 else card["crits"][K - 1]
    if card["mode"] == "highest":
        return "level", card["crits"][g] if g >= 1 else card["crits"][1]
    if card["mode"] == "cut":
        return "qty", None
    return "none", None


def decisive_atom(c: dict, v: dict) -> dict:
    t = c["t"]
    if t == "atom":
        return c["a"]
    parts = (c["parts"] if t in ("and", "or", "allof", "anyof") else
             [c["a"], {"t": "atom", "a": c["b"]}] if t == "unless" else [c["main"], {"t": "atom", "a": c["c"]}])
    val = eval_crit(c, v)
    if t in ("and", "allof", "unless", "onlyif") and not val:
        for i, p in enumerate(parts):
            pv = eval_crit(p, v)
            if t == "unless" and i == 1:
                if pv:
                    return decisive_atom(p, v)
            elif not pv:
                return decisive_atom(p, v)
    if t in ("or", "anyof") and val:
        for p in parts:
            if eval_crit(p, v):
                return decisive_atom(p, v)
    return decisive_atom(parts[0], v)
