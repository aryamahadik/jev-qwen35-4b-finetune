"""Canonical problems for the band (S3), date (S4) and statement (S5) engines (3.8 structure hash)."""
from __future__ import annotations

from .canon import frac, _Roles


def _fr(v):
    return None if v is None else frac(v)


def canonize_band(LP):
    R = _Roles()
    P = {"eng": "band", "world": LP["world"], "unit": frac(LP["unit"]), "rate_kind": LP["rate_kind"],
         "count": bool(LP.get("count"))}
    a = LP["amt"]
    if a["kind"] == "stated":
        P["amt"] = {"kind": "stated", "a": R.get(a["a"], "a")}
    else:
        P["amt"] = {"kind": "mul", "q": R.get(a["q"], "q"), "p": R.get(a["p"], "p")}
    P["bands"] = [{"name": f"b{i + 1}", "lo": _fr(b.get("lo")), "hi": _fr(b.get("hi")), "rate": frac(b["rate"])}
                  for i, b in enumerate(LP["bands"])]
    if LP.get("fee"):
        P["fee"] = R.get(LP["fee"], "s")
    P["steps"] = [{"op": s["op"], "id": s["id"], "v": R.get(s["v"], "s"), "scope": s.get("scope")} for s in LP.get("steps", [])]
    if LP.get("x10"):
        P["x10"] = {"f": R.get(LP["x10"]["f"], "f"), "v": LP["x10"]["v"]}
    P["vals"] = {R.m[k]: frac(v) for k, v in LP["vals"].items() if k in R.m}
    P["facts"] = {R.m[k]: v for k, v in LP.get("facts", {}).items() if k in R.m}
    if LP.get("cats"):
        P["cats"] = {R.m[k]: sorted(v) for k, v in LP["cats"].items() if k in R.m}
    sem = dict(LP.get("sem", {}))
    if "R1u" in sem:
        sem["R1u"] = frac(sem["R1u"])
    P["sem"] = {k: sem[k] for k in sorted(sem)}
    q = {k: v for k, v in LP["q"].items() if not k.startswith("_") and k not in ("tf", "frame", "pol")}
    if "T" in q:
        q["T"] = frac(q["T"])
    if q.get("kind") == "cases":
        q["cases"] = [{"vals": {R.m[k]: frac(v) for k, v in c.get("vals", {}).items() if k in R.m},
                       "facts": {R.m[k]: v for k, v in c.get("facts", {}).items() if k in R.m}} for c in q["cases"]]
    P["q"] = q
    if LP.get("printed"):
        P["printed"] = {LP["printed_nodes"][k]: frac(v) for k, v in LP["printed"].items()}
    return P


def canonize(LP):
    e = LP["eng"]
    if e == "band":
        return canonize_band(LP)
    if e == "date":
        from .canon_date import canonize_date
        return canonize_date(LP)
    if e == "stmt":
        from .canon_date import canonize_stmt
        return canonize_stmt(LP)
    raise ValueError(e)
