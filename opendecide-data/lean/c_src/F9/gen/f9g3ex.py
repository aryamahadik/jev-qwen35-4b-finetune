"""G3 card-example check (1.6 'Every example in the card is re-solved by solver B under the card's SEM'; section 5).
Written from the example grammar in f9examples' docstring, not from its renderer: every definition example and every
few-shot case found in the card text is parsed (column, value, atom or term) and re-solved by solver B on a one-record
table; the stated outcome (meets / counts / Yes) must equal solver B's answer. The number found must equal the number
the card holds (side file)."""
from __future__ import annotations

import re

from f9fmt import parse_date
from f9parse import QP, fail
from f9solve_b import SolverB

REC = r"([a-z][a-z ]*?)"
COL = r"([a-z][a-z_.]*[a-z])"
EX_MEET = re.compile(rf"A {REC} with {COL} ([^']+?) (meets|does not meet) '([^']+)'\.")
EX_TERM = re.compile(rf"A {REC} with \(([^()]+)\) (counts|does not count) as ([a-z][a-z ]*?)\.")
FS_MEET = re.compile(rf"A {REC} with {COL} ([^']+?): does it meet '([^']+)'\?")
FS_TERM = re.compile(rf"A {REC} with \(([^()]+)\): does it count as ([a-z][a-z ]*?)\?")
AFTER = re.compile(r'^"?\s*(?:gives|Answer:|Correct choice:|A:|Output:|=>|Outcome:|Answer key:|Its answer:|<answer>)'
                   r"\s*(Yes|No)\b")
BEFORE = re.compile(r"(?:\(|the answer is |^|\s)(Yes|No)\)?\.?\s*$")


def _value(qp, cols, fm, col, s):
    c = cols.get(col) or fail(f"example column {col}")
    if c["type"] == "num":
        v, u = qp.amount(s, col)
        if u != (c.get("unit") or (getattr(fm, "units", None) or {}).get(col)):  # header unit, else the card's T28
            fail("example unit")
        return v
    if c["type"] == "date":
        return parse_date(s, fm.df)
    if c["type"] == "bool":
        toks = {"true": True, "false": False} if fm.bool == "tf" else {"1": True, "0": False}
        return toks.get(s) if s in toks else fail("example boolean")
    if fm.legend and fm.legend["col"] == col:
        return fm.legend["codes"].get(s) or fail("example code")
    return s


def _pairs(cols, s):
    out = []
    for part in s.split("; "):
        hit = [n for n in cols if part.startswith(n + " ")]
        if not hit:
            fail("example pair")
        n = max(hit, key=len)
        out.append((n, part[len(n) + 1:]))
    return out


def _solve(P, cols, vals, p):
    idn = P["ctx"].get("idcol") or "_exid"
    tcols = [{"name": idn, "type": "id"}] + [{"name": n, **{k: v for k, v in cols[n].items() if k != "role"}}
                                             for n, _ in vals]
    ctx = dict(P["ctx"], world="T1", missing=None, t5={}, sampler="S1")
    mini = {"sampler": "S1", "btables": [{"role": "main", "cols": tcols,
                                                  "rows": [["EX-0001"] + [v for _, v in vals]]}], "ctx": ctx}
    a = SolverB(mini).answer({"op": "lookup_p", "id": "EX-0001", "p": p})
    if not isinstance(a, bool):
        fail("example undetermined")
    return a


def _answer(flat, m):
    a = AFTER.match(flat[m.end():].lstrip())
    if a:
        return a.group(1) == "Yes"
    b = BEFORE.search(flat[:m.start()])
    if b:
        return b.group(1) == "Yes"
    fail("few-shot answer")


def check_examples(P, expect_n):
    c = P["card"]
    flat = c.get("flat") or ""
    fm = P["fm"]
    cols = dict(P["cols"])
    for n, u in fm.units.items():
        cols.setdefault(n, {"type": "num", "unit": u, "role": "main", "dp": 0})
    qp = QP(cols, fm, {"conv": c.get("conv", {}), "t10": c.get("t10"), "check_t10": True})
    n = 0
    for m in list(EX_MEET.finditer(flat)) + list(FS_MEET.finditer(flat)):
        col, vs, atom = m.group(2), m.group(3), m.group(5) if m.re is EX_MEET else m.group(4)
        want = (m.group(4) == "meets") if m.re is EX_MEET else _answer(flat, m)
        p = qp.atom(atom)
        if p.get("col") != col:
            fail("example atom column")
        if _solve(P, cols, [(col, _value(qp, cols, fm, col, vs))], p) != want:
            fail("example outcome differs from solver B")
        n += 1
    for m in list(EX_TERM.finditer(flat)) + list(FS_TERM.finditer(flat)):
        pairs = _pairs(cols, m.group(2))
        tn = m.group(4) if m.re is EX_TERM else m.group(3)
        want = (m.group(3) == "counts") if m.re is EX_TERM else _answer(flat, m)
        if tn not in P["ctx"]["terms"]:
            fail("example term")
        vals = [(k, _value(qp, cols, fm, k, s)) for k, s in pairs]
        if _solve(P, cols, vals, {"k": "term", "name": tn}) != want:
            fail("term example outcome differs from solver B")
        n += 1
    if n != expect_n:
        fail(f"examples found {n} != {expect_n}")
    return n
