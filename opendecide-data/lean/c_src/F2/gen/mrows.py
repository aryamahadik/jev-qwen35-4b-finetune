"""Money rows (S1 forward, S2 target-first): value draws under placement and tag targets, gold, options, tags.

gen_row(card, rng, var, plan) returns a row spec dict (no text yet) or raises Reject. The caller (build.py) renders it.
"""
from __future__ import annotations

import math
from decimal import Decimal

from . import mcard, money, options as O
from .common import D, ONE, ZERO, on_grid, quant
from .money import Reject

MAX_TRIES = 300


def _final(LP, rd=None):
    v, tr = money.evaluate(LP, rd or {})
    return v, tr


def _unit(LP):
    return D(LP["unit"])


def grid_ok(LP, card, shown):
    """R7 on every row (final value on the display grid); when R1 is not shown (not relevant or dropped from a short
    card) every value the rules compute is exact on the grid too (A51, R1-18)."""
    v, tr = _final(LP)
    u = _unit(LP)
    if v < 0 or not on_grid(v, u):
        return False
    if "R1" not in LP["sem"] or "R1" not in shown:
        for nid, x in tr.nodes:
            if not on_grid(x, u):
                return False
    if LP["target"] != "fee" and any(not on_grid(a, u) for a in tr.line_amts) and "R1" not in LP["sem"]:
        return False
    return True


def invariance_ok(LP, card, shown, lab_fn):
    """Joint invariance filter over the omitted relevant dimensions of a short card (2.1): every combination of their
    filter alternatives gives the gold label."""
    om = card.get("omitted", [])
    if not om:
        return True
    sem = LP["sem"]
    alts = []
    for d in om:
        if d == "R1":
            alts.append([{"R1": x} for x in ("half_up", "half_even", "floor", "ceiling")] + [{"R4alt": "display"}])
        elif d == "R5":
            alts.append([{"R5": x} for x in ("ceil", "floor", "exact")])
        elif d == "U3":
            alts.append([{"U3": x} for x in ("pro_rata", "full_k", "blocks")])
        elif d == "X8":
            alts.append([{"X8": "floor"}, {"X8": "none"}])
    gold = lab_fn(LP, {})
    import itertools
    for combo in itertools.product(*alts):
        s = {}
        for c in combo:
            s.update(c)
        try:
            if lab_fn(LP, {"sem": s}) != gold:
                return False
        except (Reject, ArithmeticError, ValueError):
            return False
    return True


def depth_info(LP, printed):
    """(depth, total ops, sel, group) from the canonical operation graph (1.1)."""
    v, tr = _final(LP)
    ops = tr.ops
    st = len([n for n in tr.nodes if n[0] in printed])
    depth = ops - st
    if st and ops - st == 1 and ops >= 3:
        grp = "c"
    elif ops <= 2 and not st:
        grp = "a" if ops == 1 else "b"
    elif not st and ops in (3, 4):
        grp = "d"
    else:
        grp = "x"
    return depth, ops, tr.sel, grp


def adj_tags(LP, label_schema, lab_fn, val_fn):
    """has:/bind:/dec: tags (3.8). bind = the value changes without x; dec = the label changes without x."""
    sem = LP["sem"]
    ops = {s["op"] for s in LP["steps"]}
    tests = []
    if "cap" in ops:
        tests.append(("cap", {"err": "E-cap"}))
    if "min" in ops:
        tests.append(("floor", {"err": "E-floor"}))
    if LP.get("excs"):
        tests.append(("exc", {"excl": {e["no"] for e in LP["excs"]}}))
    if "R1" in sem:
        tests.append(("round", {"norround": True}))
    if "R5" in sem:
        tests.append(("partial", {"sem": {"R5": "exact"}}))
    if "U3" in sem:
        tests.append(("partial", {"sem": {"U3": "pro_rata"}}))
    tags = []
    v0 = val_fn(LP, {})
    l0 = lab_fn(LP, {})
    for x, rd in tests:
        tags.append(f"has:{x}")
        try:
            v1 = val_fn(LP, rd)
            l1 = lab_fn(LP, rd)
        except (Reject, ArithmeticError, ValueError):
            continue
        if v1 != v0:
            tags.append(f"bind:{x}")
        if l1 != l0:
            tags.append(f"dec:{x}")
    return sorted(set(tags))


def val_fn(LP, rd):
    v, _ = money.evaluate(LP, rd)
    return v


def yn_lab(LP, rd):
    return money.yn_label(LP, rd)[0]     # affirmative truth (labels follow by neg parity)


def thr_place_far(rng, R, unit, aff):
    """S1 far placement: abs(R - T) log-uniform in [2 units, 0.5 R] on the side the label needs (A43)."""
    if R < 8 * unit:
        raise Reject("R < 8 units")
    up = rng.random() < 0.5
    hi = max(R / 2, 2 * unit)
    d = D(str(math.exp(rng.uniform(math.log(float(2 * unit)), math.log(float(hi))))))
    d = quant(d, unit, "half_up")
    if d < 2 * unit:
        d = 2 * unit
    fam = rng.choice(["incl", "excl"])
    # up comparators are true when T < R
    if up:
        op = "ge" if fam == "incl" else "gt"
        T = R - d if aff else R + d
    else:
        op = "le" if fam == "incl" else "lt"
        T = R + d if aff else R - d
    if T <= 0:
        raise Reject("T <= 0")
    return op, T


def near_family(rng, delta, aff):
    """S2 step 3: the comparator family given delta and the affirmative truth value (derived so that P(yes|incl) =
    P(yes|excl) = 50% and the inclusive share is 50% overall and at delta 0; A41)."""
    if delta == 0:
        return "incl" if aff else "excl"
    p_incl = 2 / 7 if aff else 5 / 7
    return "incl" if rng.random() < p_incl else "excl"


def near_op(rng, delta, aff, fam, prefer_dir=None):
    """The comparator for R = T + delta x unit with affirmative truth aff and family fam."""
    cands = []
    for op in (("ge", "le") if fam == "incl" else ("gt", "lt")):
        if delta > 0:
            t = op in ("ge", "gt")
        elif delta < 0:
            t = op in ("le", "lt")
        else:
            t = op in ("ge", "le")
        if t == aff:
            cands.append(op)
    if prefer_dir and len(cands) > 1:
        c2 = [o for o in cands if (o in ("ge", "gt")) == (prefer_dir == "up")]
        if c2:
            return c2[0]
    return rng.choice(cands)


# ----------------------------------------------------------------------------------------------------------------- rows

def node_names(card, LP):
    """Printable node id -> card name (only nodes the card names can be printed intermediates)."""
    m = card["m"]
    out = {}
    for i, ln in enumerate(m["lines"]):
        if ln["p"] in ("mul", "perk"):
            out[f"line{i}"] = ln["lc"]
    if m.get("sub"):
        out["sum"] = m["sub"]
    for st in m["steps"]:
        if st["op"] == "fee" and m["target"] != "fee":
            out["fee"] = st["fee"]
    return out


def choose_printing(card, LP, rng, want_c):
    """Row group (1.1): returns (printed node ids, group). Raises Reject when the row fits no group."""
    v, tr = _final(LP)
    ops = tr.ops
    if ops <= 2:
        return set(), ("a" if ops == 1 else "b")
    names = node_names(card, LP)
    inter = [n for n, _ in tr.nodes[:-1]]
    can_c = (all(n in names for n in inter) and ops <= 5 and "R5" not in LP["sem"] and "U3" not in LP["sem"]
             and all(on_grid(x, _unit(LP)) for n, x in tr.nodes[:-1]))
    if can_c and (want_c or ops > 4):
        return set(inter), "c"
    if ops <= 4:
        return set(), "d"
    raise Reject("no row group")


def apply_printed(LP, tr_nodes, printed, names):
    LP["printed"] = {names[n]: x for n, x in tr_nodes if n in printed}
    LP["printed_nodes"] = {names[n]: n for n, x in tr_nodes if n in printed}


def gen_entity_id(card, rng, used):
    w = card["idw"]
    while True:
        x = f"{card['prefix']}-{rng.randint(10 ** (w - 1), 10 ** w - 1)}"
        if x not in used:
            used.add(x)
            return x
