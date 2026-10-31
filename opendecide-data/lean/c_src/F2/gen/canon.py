"""Canonical problem and structure hash (3.8, SC4c): labels -> role ids, numbers -> exact reduced fractions, dates ISO.

Both the generator (from its labeled problem LP) and the parser (from the rendered text) call canonize(LP); G3 (a)
compares the two hashes. canonize() is the self-contained definition the orchestrator can apply to sealed part P.
Roles are assigned by first reference in the card's rule order, so they never depend on names, packs or units.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from decimal import Decimal
from fractions import Fraction


def frac(v) -> str:
    """Exact reduced fraction of a decimal literal (string, int or Decimal)."""
    f = Fraction(Decimal(str(v)))
    return f"{f.numerator}/{f.denominator}"


class _Roles:
    def __init__(self):
        self.m = {}
        self.n = {}

    def get(self, label, kind):
        if label is None:
            return None
        key = (kind, label)
        if label in self.m:
            return self.m[label]
        self.n[kind] = self.n.get(kind, 0) + 1
        r = f"{kind}{self.n[kind]}"
        self.m[label] = r
        return r


def _num(v):
    if isinstance(v, (int, Decimal)) or (isinstance(v, str) and v.replace(".", "", 1).isdigit()):
        return frac(v)
    return v


def canonize_money(LP: dict) -> dict:
    R = _Roles()
    vals, facts = LP.get("vals", {}), LP.get("facts", {})
    P = {"eng": "money", "world": LP["world"], "unit": frac(LP["unit"]), "target": LP.get("target", "final")}
    lines = []
    for ln in LP["lines"]:
        d = {"p": ln["p"]}
        for k in ("q", "r", "a", "b4x", "b4m"):
            if ln.get(k) is not None:
                d[k] = R.get(ln[k], {"q": "q", "r": "r", "a": "a", "b4x": "x", "b4m": "m"}[k])
        if ln.get("k") is not None:
            d["k"] = frac(ln["k"])
        if ln.get("mark"):
            d["mark"] = ln["mark"]
        lines.append(d)
    P["lines"] = lines
    steps = []
    for st in LP["steps"]:
        d = {"op": st["op"], "id": st.get("id", st["op"])}
        v = st.get("v")
        if isinstance(v, list):
            d["v"] = [R.get(x, "s") for x in v]
        elif v is not None:
            d["v"] = R.get(v, "s")
        for k in ("scope", "lim"):
            if st.get(k) is not None:
                d[k] = st[k]
        steps.append(d)
    P["steps"] = steps
    excs = []
    for e in LP.get("excs", []):
        d = {"no": e["no"], "conn": e["conn"], "join": e["join"], "kind": e["kind"],
             "v": R.get(e["v"], "x"), "on": R.get(e["on"], "s")}
        d["conds"] = [{"f": R.get(c["f"], "f"), "op": c["op"], "v": _num(c["v"]) if c["op"] != "is" else c["v"]}
                      for c in e["conds"]]
        excs.append(d)
    P["excs"] = excs
    # values and facts by role (only the referenced ones: an unreferenced document value is inert)
    P["vals"] = {R.m[k]: frac(v) for k, v in vals.items() if k in R.m}
    P["facts"] = {R.m[k]: (v if not str(v).lstrip("-").isdigit() else frac(v)) for k, v in facts.items() if k in R.m}
    if LP.get("cats"):
        P["cats"] = {R.m[k]: sorted(v) for k, v in LP["cats"].items() if k in R.m}
    sem = dict(LP.get("sem", {}))
    if "R1u" in sem:
        sem["R1u"] = frac(sem["R1u"])
    P["sem"] = {k: sem[k] for k in sorted(sem)}
    q = dict(LP["q"])
    if "T" in q:
        q["T"] = frac(q["T"])
    if q.get("kind") == "outcome":
        q["outs"] = [{"name": f"o{i + 1}", "lo": None if o.get("lo") is None else frac(o["lo"]),
                      "hi": None if o.get("hi") is None else frac(o["hi"])} for i, o in enumerate(q["outs"])]
    if q.get("kind") == "cases":
        cs = []
        for c in q["cases"]:
            cv = {R.m[k]: frac(v) for k, v in c.get("vals", {}).items() if k in R.m}
            cf = {R.m[k]: v for k, v in c.get("facts", {}).items() if k in R.m}
            cs.append({"vals": cv, "facts": cf})
        q["cases"] = cs
    for k in list(q):
        if k in ("tf", "frame", "wording", "pol") or k.startswith("_"):
            q.pop(k, None)
    P["q"] = q
    if LP.get("printed"):
        pn = LP["printed_nodes"]
        P["printed"] = {pn[k]: frac(v) for k, v in LP["printed"].items()}
    return P


def structure_hash(P: dict) -> str:
    return hashlib.sha256(json.dumps(P, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def canonize(LP: dict) -> dict:
    eng = LP["eng"]
    if eng == "money":
        return canonize_money(LP)
    from . import canon_more
    return canon_more.canonize(LP)


def _strip_private(LP):
    return {k: v for k, v in LP.items() if not k.startswith("_")}
