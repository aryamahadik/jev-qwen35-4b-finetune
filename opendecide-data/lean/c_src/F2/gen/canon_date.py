"""Canonical problems for S4 date rows and S5 statements (3.8): dates as ISO, numbers as reduced fractions, names as
role ids."""
from __future__ import annotations

from .canon import frac, _Roles


def _iso(d):
    return d.isoformat() if hasattr(d, "isoformat") else str(d)


def canonize_date(LP):
    R = _Roles()
    ev = R.get(LP["evt"], "d")
    ac = R.get(LP["act"], "d")
    r = LP["rule"]
    rule = {"kind": r["kind"]}
    if r["kind"] in ("cal", "bday"):
        rule["N"] = r["N"]
    if r["kind"] == "month":
        rule["M"] = r["M"]
    if r.get("ext"):
        e = r["ext"]
        rule["ext"] = {"K": e["K"], "unit": e["unit"], "conn": e["conn"], "join": e["join"],
                       "conds": [{"f": R.get(c["f"], "f"), "op": c["op"], "v": c["v"]} for c in e["conds"]]}
    P = {"eng": "date", "world": LP["world"], "rule": rule, "evt": ev, "act": ac, "d6a": bool(LP.get("d6a")),
         "holidays": sorted(_iso(h) for h in LP.get("holidays", []))}
    P["dates"] = {R.m[k]: _iso(v) for k, v in LP.get("dates", {}).items() if k in R.m}
    P["facts"] = {R.m[k]: v for k, v in LP.get("facts", {}).items() if k in R.m}
    if LP.get("cats"):
        P["cats"] = {R.m[k]: sorted(v) for k, v in LP["cats"].items() if k in R.m}
    if LP.get("count"):
        c = LP["count"]
        P["count"] = {"kind": c["kind"], "d1": R.get(c["d1"], "d"), "d2": R.get(c["d2"], "d")}
    if LP.get("windows"):
        P["windows"] = [{"name": f"w{i + 1}", "lo": w.get("lo"), "hi": w.get("hi")} for i, w in enumerate(LP["windows"])]
    P["sem"] = {k: LP["sem"][k] for k in sorted(LP.get("sem", {}))}
    q = {k: v for k, v in LP["q"].items() if not k.startswith("_") and k not in ("tf", "frame", "pol")}
    if q.get("kind") == "cases":
        q["cases"] = [{"dates": {R.m[k]: _iso(v) for k, v in c["dates"].items() if k in R.m},
                       "facts": {R.m[k]: v for k, v in c["facts"].items() if k in R.m}} for c in q["cases"]]
    P["q"] = q
    return P


def canonize_stmt(LP):
    from .canon import canonize_money
    P = canonize_money({**LP, "eng": "money"})
    P["eng"] = "stmt"
    if LP.get("settle"):
        s = LP["settle"]
        P["settle"] = {"N": s["N"], "D7": s["D7"], "per": s["per_date"].isoformat(),
                       "holidays": sorted(h.isoformat() for h in s["holidays"])}
    if LP.get("marks"):
        P["marks"] = list(LP["marks"])
    return P
