"""Canonical surface form for the G3 comparison: the generated structure (ids -> the row's surface names) and the
parsed structure map to the same canonical JSON when the round trip is exact."""
from __future__ import annotations

import json
import re


def _atom(at, nm):
    t = at["t"]
    if t == "num":
        return ["num", nm["attr"](at["a"]), at["op"], at["n"]]
    if t == "cat":
        return ["cat", nm["attr"](at["a"]), at["v"]]
    if t == "ev":
        return ["ev", nm["ev"](at["e"]), bool(at.get("neg"))]
    return ["cls", nm["cls"](at["c"])]


def _rule_key(r, nm, by_rid):
    conds = sorted(json.dumps(_atom(a, nm)) for a in r["conds"])
    u = json.dumps(_atom(r["unless"], nm)) if r.get("unless") else None
    exc = None
    if r.get("exc"):
        e = r["exc"]
        if e.startswith("T:") or e.startswith("T|") or (e.startswith("T") and ":" in e):
            exc = "TABLE:" + e.split(":", 1)[1]
        else:
            exc = _rule_key(by_rid[e], nm, by_rid)
    return json.dumps([nm["notice"](r["notice"]), nm["out"](r["out"]), conds, u, exc])


def canon(S: dict, case: str, named: bool) -> str:
    """S: a generator R (named=False: ids + name maps in S['_nm']) or a parsed structure (named=True)."""
    if named:
        ident = lambda x: x  # noqa: E731
        nm = {"attr": ident, "ev": ident, "cls": ident, "notice": ident, "out": ident}
    else:
        nm = S["_nm"]
    by_rid = {r["rid"]: r for r in S["rules"]}
    rules = sorted(_rule_key(r, nm, by_rid) for r in S["rules"])
    T = S.get("table")
    tab = None
    if T:
        tab = [nm["notice"](T["notice"]), nm["attr"](T["A"]), nm["attr"](T["B"]),
               sorted((k, nm["out"](v)) for k, v in T["cells"].items())]
    oi = sorted(json.dumps([nm["out"](o["out"]), _atom(o["cond"], nm)]) for o in S.get("onlyif", []))
    F = S["facts"][case]

    def _clean(v):
        return {k: x for k, x in v.items() if k != "mtext"}
    F = {k: ({a: _clean(b) for a, b in v.items()} if isinstance(v, dict) else v) for k, v in F.items()}
    facts = {
        "num": sorted((nm["attr"](k), json.dumps(v, sort_keys=True)) for k, v in F["num"].items()),
        "cat": sorted((nm["attr"](k), json.dumps(v, sort_keys=True)) for k, v in F["cat"].items()),
        "ev": sorted((nm["ev"](k), json.dumps(v, sort_keys=True)) for k, v in F["ev"].items()),
        "cls": sorted((nm["cls"](k), json.dumps(v, sort_keys=True)) for k, v in F["cls"].items()),
        "inert": sorted(json.dumps(x) for x in F.get("inert", [])),
    }
    lists = sorted((nm["cls"](k), sorted(json.dumps(list(e)) for e in v)) for k, v in S["lists"].items())
    attrs = sorted(json.dumps([nm["attr"](k), v["kind"], v.get("unit"), v.get("lo"), v.get("hi"),
                               v.get("vals")]) for k, v in S["attrs"].items())
    notices = sorted((nm["notice"](k), json.dumps(v["date"], sort_keys=True)) for k, v in S["notices"].items())
    sub = sorted([nm["cls"](b), nm["cls"](a)] for b, a in S.get("subclass", []))
    local = nm["cls"](S["local"]) if S.get("local") else None
    out = {"world": S["world"], "local": local, "D": S["D"], "marker": S["marker"], "tag": S.get("ev_tag"),
           "attrs": attrs, "notices": notices, "rules": rules, "table": tab, "onlyif": oi,
           "default": nm["out"](S["default"]), "sub": sub, "facts": facts, "lists": lists}
    return json.dumps(out, sort_keys=True)


def gen_named_view(R: dict, case: str, outmap: dict) -> dict:
    """Restrict a generated R to what the row shows and attach the id -> surface-name maps."""
    from .rules_gen import ref_vars
    roles = ref_vars(R)
    ref_ev = {k[1] for k in roles if k[0] == "ev"}
    ref_cls = {k[1] for k in roles if k[0] == "cls"}
    for b, a in R.get("subclass", []):
        ref_cls |= {b, a}
    if R.get("local"):
        ref_cls.add(R["local"])
    attrs = R["attrs"]
    nm = {"attr": lambda a: attrs[a]["name"], "ev": lambda e: R["events"][e]["name"],
          "cls": lambda c: R["classes"][c]["name"], "notice": lambda n: R["notices"][n]["name"],
          "out": lambda o: outmap[o]}
    F = R["facts"][case]
    F2 = {"num": dict(F["num"]), "cat": dict(F["cat"]), "inert": list(F.get("inert", [])),
          "ev": {k: v for k, v in F["ev"].items() if k in ref_ev},
          "cls": {k: v for k, v in F["cls"].items() if k in ref_cls}}
    for k, v in F["ev"].items():
        if k not in ref_ev:
            raise ValueError("unreferenced event line rendered")
    lists = {k: v for k, v in R["lists"].items() if k in ref_cls}
    S = dict(R)
    S["facts"] = {case: F2}
    S["lists"] = lists
    S["_nm"] = nm
    S["notices"] = {k: v for k, v in R["notices"].items()}
    return S
