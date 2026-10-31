"""S4 records sampler (G0 section 5, S4): 5-12 records x 4-5 fields (ID, category with a value set, number with unit,
1-2 yes/no flags; some 'not recorded' / blank cells, SEM-04), closed world only. Base: a quantified claim over a filtered
subset (every, some, at least q, at most q, more than half; the non-monotone operators are not used in round 1).

M = {world: closed, noun, plural, cat {name, values}, qty {name, unit, step}, flags [w...], recs [{id, cat, qty,
     flags {w: True|False|"NR"}, blank {w: bool}}], q_graded}
cat / qty values: value or "NR". Solver A: Python set comprehension over the records, re-run for every SEM-04 test
value of each unrecorded cell.
"""
from __future__ import annotations

import copy
import itertools

OPS = {">=": lambda a, b: a >= b, ">": lambda a, b: a > b, "<=": lambda a, b: a <= b, "<": lambda a, b: a < b}


def in_group(rec, filters, assign):
    for f in filters:
        if f[0] == "cat":
            v = assign.get((rec["id"], "cat"), rec["cat"])
            if v != f[2]:
                return False
        elif f[0] == "num":
            v = assign.get((rec["id"], "qty"), rec["qty"])
            if not OPS[f[2]](v, f[3]):
                return False
    return True


def pred_val(rec, pred, assign):
    if pred[0] == "flag":
        v = assign.get((rec["id"], "flag:" + pred[1]), rec["flags"][pred[1]])
        return bool(v)
    v = assign.get((rec["id"], "qty"), rec["qty"])
    return OPS[pred[2]](v, pred[3])


def eval_q(lf, M, assign):
    op = lf[0]
    if op == "not":
        return not eval_q(lf[1], M, assign)
    if op == "and":
        return all(eval_q(x, M, assign) for x in lf[1:])
    if op != "q":
        raise ValueError(op)
    _, Q, q, group, pred, exc = lf
    members = [r for r in M["recs"] if in_group(r, group[1], assign) and r["id"] != exc]
    if not members:
        raise ValueError("empty group")
    n = sum(1 for r in members if pred_val(r, pred, assign))
    if Q == "every":
        return n == len(members)
    if Q == "some":
        return n >= 1
    if Q == "atleast":
        return n >= q
    if Q == "atmost":
        return n <= q
    if Q == "lt":
        return n < q
    if Q == "gt":
        return n > q
    if Q == "morehalf":
        return 2 * n > len(members)
    raise ValueError(Q)


def tests(M, lfs):
    """SEM-04 test sets for every unrecorded cell (F5-R3-06, F5-R4-05)."""
    ths = set()
    cats_named = set()

    def walk(x):
        if isinstance(x, list) and x:
            if x[0] == "q":
                for f in x[3][1]:
                    if f[0] == "num":
                        ths.add(f[3])
                    if f[0] == "cat":
                        cats_named.add(f[2])
                if x[4][0] == "num":
                    ths.add(x[4][3])
            for y in x[1:]:
                walk(y)
    for lf in lfs:
        walk(lf)
    out = {}
    for r in M["recs"]:
        if r["cat"] == "NR":
            out[(r["id"], "cat")] = sorted(set(M["cat"]["values"]) | cats_named | {
                x["cat"] for x in M["recs"] if x["cat"] != "NR"}) + ["Other value"]
        if r["qty"] == "NR":
            vals = set()
            for t in ths | {x["qty"] for x in M["recs"] if x["qty"] != "NR"}:
                vals |= {t - 1, t, t + 1}
            out[(r["id"], "qty")] = sorted(v for v in vals if v >= 0)
        for w, v in r["flags"].items():
            if v == "NR":
                out[(r["id"], "flag:" + w)] = [False, True]
    return out


def solve_a(M, lfs):
    T = tests(M, lfs)
    keys = sorted(T)
    res = None
    for combo in itertools.product(*[T[k] for k in keys]) if keys else [()]:
        assign = dict(zip(keys, combo))
        out = [eval_q(lf, M, assign) for lf in lfs]
        if res is None:
            res = out
        elif res != out:
            raise ValueError("unrecorded cell is decisive")
    return res


def cap(s):
    return s[:1].upper() + s[1:]


def doc_ir(M, *, attack=None, blanks_ok=True):
    from fmt1.render import BLANK
    cols = [M["noun"], M["cat"]["name"], M["qty"]["name"]] + list(M["flags"])
    rows = []
    for r in M["recs"]:
        row = [r["id"], "not recorded" if r["cat"] == "NR" else r["cat"],
               "not recorded" if r["qty"] == "NR" else f"{r['qty']} {M['qty']['unit']}"]
        for w in M["flags"]:
            v = r["flags"][w]
            if v == "NR":
                row.append("not recorded")
            elif v:
                row.append("yes")
            else:
                row.append(BLANK if (r["blank"].get(w) and blanks_ok) else "no")
        rows.append(row)
    blocks = [{"type": "table", "caption": None, "columns": cols, "rows": rows}]
    if M.get("decoy_text"):
        rid, a, b = M["decoy_text"]
        blocks.append({"type": "para", "text": f"Note: {M['noun']} {rid} is not only {a} but also {b}."})
    if attack:
        blocks.append({"type": "para", "text": attack})
    return {"title": f"{cap(M['plural'])} on file", "blocks": blocks}


def perturb(M, rng):
    """Contrast-pair change (S4): one field value of one record."""
    out = []
    keep = M["decoy_text"][0] if M.get("decoy_text") else None
    for i, r in enumerate(M["recs"]):
        for w, v in r["flags"].items():
            if v != "NR" and r["id"] != keep:
                M2 = copy.deepcopy(M)
                M2["recs"][i]["flags"][w] = not v
                M2["recs"][i]["blank"][w] = False
                out.append((f"{r['id']} {w} -> {not v}", M2))
        if r["cat"] != "NR":
            for v in M["cat"]["values"]:
                if v != r["cat"]:
                    M2 = copy.deepcopy(M)
                    M2["recs"][i]["cat"] = v
                    out.append((f"{r['id']} cat -> {v}", M2))
    rng.shuffle(out)
    return out
