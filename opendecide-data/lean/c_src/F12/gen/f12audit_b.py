"""Solver B for audit rows (G0 section 5 "Compiled forms" + "Error tables"; section 3 step 9).

Works on the PARSED structure only. Compiles the named tool to JSON Schema (Draft 2020-12) with the cross-param rules
as allOf members (ONLY_IF -> dependentRequired; UNLESS -> if/then/else after the default fill; EXACTLY_ONE -> oneOf;
AT_LEAST_ONE -> anyOf; AT_MOST_ONE -> not), runs the audit pre-pass (no unit or enum normalisation; decimals scaled
by 10^places; dates to day ordinals; defaults filled) and maps every jsonschema error to its SEM-45 class with one
fixed table keyed by (validator keyword, schema path, declared type, instance JSON type, pair members present).
"""
from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal

import jsonschema

import f12solve_b as B

LIMIT_KW = {"minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "minLength", "maxLength"}
PAIR = {"ONLY_IF": 8, "UNLESS": 9, "EXACTLY_ONE": 10, "AT_LEAST_ONE": 11, "AT_MOST_ONE": 12}


def _bool_text(v):
    return v == "yes"


def compile_tool(tool):
    s = B.schema_of(tool)
    for p in tool["params"]:
        if p["type"] == "boolean":
            s["properties"][p["name"]] = {"type": "boolean"}
    pm = {p["name"]: p for p in tool["params"]}
    allof = []
    for c in tool.get("cons") or []:
        k, p, q = c["k"], c["p"], c["q"]
        if k == "ONLY_IF":
            allof.append({"dependentRequired": {p: [q]}})
        elif k == "UNLESS":
            v = _bool_text(c["v"]) if pm[q]["type"] == "boolean" else c["v"]
            allof.append({"if": {"required": [q], "properties": {q: {"const": v}}}, "then": {},
                          "else": {"required": [p]}})
        elif k == "EXACTLY_ONE":
            allof.append({"oneOf": [{"required": [p]}, {"required": [q]}]})
        elif k == "AT_LEAST_ONE":
            allof.append({"anyOf": [{"required": [p]}, {"required": [q]}]})
        elif k == "AT_MOST_ONE":
            allof.append({"not": {"required": [p, q]}})
    if allof:
        s["allOf"] = allof
    return s


def prepass_audit(p, v):
    t = p["type"]
    if t in ("integer", "decimal"):
        if isinstance(v, bool) or not isinstance(v, (int, Decimal)):
            return v
        x = Decimal(v)
        if t == "decimal":
            x = x * (Decimal(10) ** p["places"])
        return int(x) if x == x.to_integral_value() else float(x)
    if t == "date" and isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return dt.date.fromisoformat(v).toordinal()
    return v


def validate(tools, call):
    """Sorted (class, params) list; [] = valid."""
    by = {t["name"]: t for t in tools}
    if call["tool"] not in by:
        return [(1, ())]
    T = by[call["tool"]]
    pm = {p["name"]: p for p in T["params"]}
    inst = {}
    for k, v in call["args"]:
        inst[k] = prepass_audit(pm[k], v) if k in pm else v
    for p in T["params"]:
        if p["name"] not in inst and p.get("default") is not None:
            inst[p["name"]] = _bool_text(p["default"]) if p["type"] == "boolean" else p["default"]
    sch = compile_tool(T)
    out = []
    for e in jsonschema.Draft202012Validator(sch).iter_errors(inst):
        path = list(e.schema_path)
        if path and path[0] == "allOf":
            c = T["cons"][path[1]]
            out.append((PAIR[c["k"]], (c["p"], c["q"])))
        elif e.validator == "required":
            m = re.fullmatch(r"'(.+)' is a required property", e.message)
            out.append((3, (m.group(1),)))
        elif e.validator == "additionalProperties":
            out.append((2, tuple(sorted(k for k in inst if k not in sch["properties"]))))
        else:
            prop = e.path[0]
            decl = pm[prop]["type"]
            if e.validator == "type":
                out.append((6 if decl == "decimal" and isinstance(e.instance, float) else 4, (prop,)))
            elif e.validator == "enum":
                out.append((5, (prop,)))
            elif e.validator in LIMIT_KW:
                out.append((6, (prop,)))
            elif e.validator == "pattern":
                out.append((7, (prop,)))
            else:
                raise AssertionError(f"unmapped error {e.validator}")
    return sorted(out)


def typed_text(p, text, now):
    """B's own typed form of a resolved forward value (for SEM-28b comparison)."""
    t = p["type"]
    if t == "integer":
        return Decimal(re.match(r"\d+", text).group(0))
    if t == "decimal":
        return Decimal(re.match(r"\d+(?:\.\d+)?", text).group(0))
    if t == "date":
        return dt.date.fromordinal(B.day_ord(text, now)).isoformat()
    if t == "enum":
        return next(x for x in p["members"] if x.casefold() == text.casefold())
    if t == "boolean":
        return text == "yes"
    return text


def _eq(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, Decimal)) or isinstance(b, (int, Decimal)):
        return isinstance(a, (int, Decimal)) and isinstance(b, (int, Decimal)) and Decimal(a) == Decimal(b)
    return a == b


def correct(P, res, call):
    """Y-CORRECT base truth from solver B's outcome and resolution on the parsed structure."""
    if res["outcome"] != "CALL" or call["tool"] != res["tool"] or validate(P["tools"], call):
        return False
    T = next(t for t in P["tools"] if t["name"] == res["tool"])
    exp = {p["name"]: typed_text(p, res["vals"][p["name"]], P["now"]) for p in T["params"] if p["name"] in res["vals"]}
    args = {k: v for k, v in call["args"]}
    for p in T["params"]:
        n = p["name"]
        d = None if p.get("default") is None else (_bool_text(p["default"]) if p["type"] == "boolean"
                                                    else p["default"])
        if n in args:
            if n in exp:
                if not _eq(args[n], exp[n]):
                    return False
            elif d is None or not _eq(args[n], d):
                return False
        elif n in exp and (d is None or not _eq(exp[n], d)):
            return False
    return True
