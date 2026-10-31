"""Section-2 alternatives as error tags (1.3, 1.5). Two kinds:
  - rewrite tags (E1 predicate ignored, E2 boundary flipped, E3 unit_step / rolling_N, E11 filter ignored, E12 count
    vs distinct, E19 neither as not-both): a pure AST transform from (tag, parameters), applied identically before
    either solver evaluates (1.3: "G3 can rebuild every option from tag and parameters");
  - mode tags (E4, E6, E7, E8, E16, E17, E20, E23, E24, E26, E27, E29, E30, E32, E34): each solver switches its own
    evaluation.
applicable(q, card) lists the tags that can apply to a query (for distractors and for meta.edge, 1.5).
"""
from __future__ import annotations

import copy

from f9ast import atoms

REWRITE = {"E1", "E2", "E3", "E11", "E12", "E19"}
FLAG_OF = {"E1": None, "E2": "T10", "E3": "T15", "E11": None, "E12": "T27", "E19": "T13", "E4": "T3",
           "E29": "T5", "E30": "T2", "E7": "T24", "E23": "T22", "E8": "T22", "E24": "T23", "E16": "T7",
           "E17": "T8", "E26": "T30", "E20": "T14", "E6": "T29", "E27": "T32", "E34": "T32", "E32": "T41",
           "E25": "T26", "E13": "T31"}


def _flip(op):
    return {">=": ">", ">": ">=", "<=": "<", "<": "<="}.get(op, op)


def _base(q):
    b = q
    while b["op"] in ("thr", "not"):
        b = b["inner"]
    return b


def _fkey(b):
    for k in ("f", "fe", "fd", "a"):
        if isinstance(b.get(k), dict):
            return k
    return None


def _top_atoms(p):
    """Top-level AND operands (an atom alone is one operand)."""
    if p is None:
        return []
    return list(p["args"]) if p["k"] == "and" else [p]


def rewrite(q, alt):
    """Return a rewritten copy of q for a rewrite tag, or q itself for a mode tag."""
    if not alt or alt[0] not in REWRITE:
        return q
    q2 = copy.deepcopy(q)
    b = _base(q2)
    tag = alt[0]
    if tag == "E11":
        fk = alt[1] if len(alt) > 1 else _fkey(b)
        b[fk] = None
        return q2
    if tag == "E12":
        if b["op"] == "cdist":
            b["op"] = "count"
        elif b["op"] == "count" and len(alt) > 1:
            b["op"] = "cdist"
            b["col"] = alt[1]
        return q2
    if tag == "E1" and len(alt) > 3:  # one part of an S6 line condition dropped (level or component)
        fk, i, part = alt[1], alt[2], alt[3]
        ops = _top_atoms(b[fk])
        a = dict(ops[i])
        if part == "level":
            a.pop("level", None), a.pop("lvl_op", None)
        else:
            a.pop("comp", None)
        ops[i] = a
        b[fk] = ops[0] if len(ops) == 1 else {"k": "and", "args": ops}
        return q2
    if tag == "E1":
        fk, i = alt[1], alt[2]
        ops = _top_atoms(b[fk])
        rest = [x for j, x in enumerate(ops) if j != i]
        b[fk] = None if not rest else (rest[0] if len(rest) == 1 else {"k": "and", "args": rest})
        return q2
    # E2 / E3 / E19 address one atom by (field, index in atoms() order)
    if tag == "E2" and alt[1] in ("thr", "cmp"):
        return q2  # handled as a mode inside the solvers (threshold / group comparator)
    if tag == "E2" and alt[1] == "pcmp":
        b["cmp"] = _flip(b["cmp"])  # S5 column count: the T10 boundary of its own comparator flipped
        return q2
    fk, i = alt[1], (alt[2] if tag != "E19" else None)
    target = atoms(b[fk])[i] if tag != "E19" else None
    if tag == "E2":
        if target["k"] == "cmp":
            target["op"] = _flip(target["op"])
        elif target["k"] == "between":
            target["open"] = not target.get("open", False)
        elif target["k"] == "win":
            side = alt[3]
            if side == "lo":
                target["li"] = not target.get("li", True)
            else:
                target["hi_i"] = not target.get("hi_i", True)
        elif target["k"] == "line":
            target["lvl_op"] = _flip(target.get("lvl_op", "="))
        return q2
    if tag == "E3":
        kind = alt[3]
        if kind == "unit_step":
            side, d = alt[4], alt[5]
            step = target.get("step", 1)
            if side == "lo" and target.get("lo") is not None:
                target["lo"] += d * step
            elif side == "hi" and target.get("hi") is not None:
                target["hi"] += d * step
        elif kind == "rolling_N":
            target["lo"] -= 1
        return q2
    if tag == "E19":
        # 'neither A nor B' read as 'not both': NOT(OR(A, B)) -> NOT(AND(A, B)); in a two-value set the same
        def walk(p):
            if p is None:
                return p
            if p["k"] == "not" and p["arg"]["k"] == "or":
                return {"k": "not", "arg": {"k": "and", "args": p["arg"]["args"]}}
            if p["k"] == "not" and p["arg"]["k"] == "in":
                a = p["arg"]
                return {"k": "not", "arg": {"k": "and", "args": [
                    {"k": "cmp", "col": a["col"], "op": "=", "lit": v} for v in a["vals"]]}}
            if p["k"] in ("and", "or"):
                return {**p, "args": [walk(x) for x in p["args"]]}
            return p
        fk = alt[1]
        b[fk] = walk(b[fk])
        return q2
    return q2


def applicable(q, card, form):
    """Candidate alternatives for this query (each a tuple). form: yn | value | record | set | cpick."""
    out = []
    b = _base(q)
    sem = card["sem"]
    fk = _fkey(b)
    if fk:
        tops = _top_atoms(b[fk])
        if len(tops) >= 2:
            for i in range(len(tops)):
                out.append(("E1", fk, i))
        for i, a in enumerate(tops):
            # an S6 line condition with a level and a component is two conditions on one line: E1 drops one of them
            if a["k"] == "line" and "level" in a and "comp" in a:
                out += [("E1", fk, i, "level"), ("E1", fk, i, "comp")]
        if b["op"] not in ("lookup_p", "quant_lookup", "ent_any", "req_any", "forall", "compare"):
            out.append(("E11", fk))
        for i, a in enumerate(atoms(b[fk])):
            if a["k"] in ("cmp", "between") and a.get("op", "x") not in ("=", "!="):
                out.append(("E2", fk, i))
            elif a["k"] == "win":
                if a.get("lo") is not None:
                    out.append(("E2", fk, i, "lo"))
                    out.append(("E3", fk, i, "unit_step", "lo", -1))
                    out.append(("E3", fk, i, "unit_step", "lo", 1))
                if a.get("hi") is not None:
                    out.append(("E2", fk, i, "hi"))
                    out.append(("E3", fk, i, "unit_step", "hi", 1))
                    out.append(("E3", fk, i, "unit_step", "hi", -1))
                if a.get("_form") == "rolling":
                    out.append(("E3", fk, i, "rolling_N"))
            elif a["k"] == "line" and a.get("lvl_op") in (">=", ">", "<=", "<"):
                out.append(("E2", fk, i))
        if any(p["k"] == "not" and p["arg"]["k"] in ("or", "in") for p in _nots(b[fk])):
            out.append(("E19", fk))
    if q["op"] == "thr" and q.get("cmp") in (">=", ">", "<=", "<"):
        out.append(("E2", "thr"))
    if b["op"] == "compare" and b.get("cmp") in (">", ">=", "<", "<="):
        out.append(("E2", "cmp"))
    if b["op"] in ("row_total", "row_top", "col_count"):  # S5 pivot (F9-R5-05): T31 / T30 readings
        out += [("E13", "with_marked"), ("E26", "footnote_row")]
        if b["op"] == "col_count" and b.get("cmp") in (">", ">=", "<", "<="):
            out.append(("E2", "pcmp"))
    if b["op"] == "cdist":
        out.append(("E12",))
    if sem.get("missing") == "T5":
        out.append(("E29",))
        out.append(("E4", "meet"))
    if sem.get("missing") == "T4":
        out.append(("E4", "meet"))
    if sem.get("world") == "T2" and b["op"] == "lookup":
        out.append(("E30",))
    if b["op"] in ("argmax", "argmin", "g_argmax", "comp_argmax", "row_top"):
        out += [("E7", "dir"), ("E7", "first"), ("E7", "last")]
    if b["op"] == "mean" and form == "value":
        out.append(("E23",))
    if b["op"] in ("mean", "min", "max") and form == "value":
        out.append(("E24",))
    if b["op"] == "mean" and q["op"] == "thr":
        out.append(("E8",))
    if b["op"] == "compare" and b.get("agg") == "mean":
        out.append(("E8",))
    terms = card.get("terms") or {}
    used = [a["name"] for a in atoms(b.get(fk) if fk else None) if a["k"] == "term"]
    if b["op"] == "lookup_p":
        used += [a["name"] for a in atoms(b["p"]) if a["k"] == "term"]
    for tn in dict.fromkeys(used):
        t = terms[tn]
        if t["kind"] == "T7":
            out.append(("E16",))
        if t["kind"] == "T8":
            out.append(("E17",))
        if t.get("overrides"):
            out.append(("E26", "general_over_specific"))
            if t["kind"] == "T7":
                out.append(("E26", "unless_kept"))
            out.append(("E26", "closure_kept"))
        if t.get("usual"):
            out.append(("E26", "usual_meaning"))
    if b["op"] == "quant_lookup" or any(a["k"] == "quant" for a in atoms(b.get(fk) if fk else None)):
        out.append(("E20",))
    if card["sampler"] == "S3" and b["op"] in ("g_count", "g_argmax"):
        out += [("E6", "orphans"), ("E6", "zero_drop")] if b["op"] == "g_argmax" else [("E6", "orphans")]
    if card["sampler"] == "S6":
        if b["op"] in ("first", "last"):
            out.append(("E27",))
        if b["op"] in ("count_lines", "exists_lines", "comp_argmax", "first", "last"):
            out.append(("E34",))
        if b["op"] in ("cpick", "select", "req_any"):
            out += [("E32", "last_line"), ("E32", "first_line")]
            if b["op"] != "req_any":
                out.append(("E32", "same_line"))
    if b["op"] == "lookup" and form == "value":
        pass  # E0 handled by the row builder (other ids)
    return out


def _nots(p):
    if p is None:
        return []
    if p["k"] == "not":
        return [p] + _nots(p["arg"])
    if p["k"] in ("and", "or"):
        return [x for a in p["args"] for x in _nots(a)]
    return []


def flag_of(alt):
    if alt[0] in ("E2", "E3"):
        return "T10"
    return FLAG_OF.get(alt[0])
