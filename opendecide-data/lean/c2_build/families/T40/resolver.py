"""families/T40/resolver.py: solver A of T40 (gold). Closed-world resolver over the registry + JSON-schema validation
(schema.py) + the slot ledger for grounding (head A); the intent / provider / required-value resolver (head B); the real
str_replace run plus ast.parse (edit.py, head C). Pure functions of (structure, env), env = {slot name: token text}.

Head A, first rule that fits (card order):
  NONEXISTENT_TOOL   the callee (bare name or provider::name) is listed by no tool
  AMBIGUOUS_PROVIDER a bare name is listed by two providers
  OFF_MENU           the tool is listed but not on the menu
  BORROWED_SIGNATURE at least one argument, none belongs to the tool, and every argument name belongs to ONE other tool
  BAD_ARGS           a required argument is missing, or an argument name is not a parameter of the tool
  TYPE_VIOLATION     a value breaks its parameter's JSON-schema type, range, enum, format or pattern
  UNGROUNDED_VALUE   an argument value is in neither the request clauses (nor the provider clause) nor an earlier result
  VALID              none of the above
Head B: CANNOT_ANSWER / ASK_FOLLOWUP / CALL (see action()). Head C: edit.apply_edit.
"""
from __future__ import annotations

import re

from . import edit as E
from .schema import structural, validate

_INT = re.compile(r"-?\d+")
_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def tool_schema(t: dict) -> dict:
    return {"type": "object", "properties": {p["name"]: p["schema"] for p in t["params"]},
            "required": [p["name"] for p in t["params"] if p["req"]], "additionalProperties": False}


def arg_value(tok: str, bare: bool):
    """The JSON value a printed argument stands for: a quoted string, or a bare number."""
    if not bare:
        return tok
    if _INT.fullmatch(tok):
        return int(tok)
    if _NUM.fullmatch(tok):
        return float(tok)
    raise ValueError(f"bare token {tok!r} is not a JSON number")


def ledger(st: dict, env: dict) -> set:
    """The slot ledger: every value the user request or an earlier tool result states."""
    vals = {env[c["slot"]] for c in st["request"]["clauses"]}
    if st["request"]["provider"]:
        vals.add(env[st["request"]["provider"]])
    for r in st["results"]:
        vals |= {env[f["val"]] for f in r["fields"]}
    return vals


def resolve_call(st: dict, env: dict, skip: frozenset = frozenset()) -> str:
    tools, call = st["tools"], st["call"]
    callee = env[call["callee"]]
    if "::" in callee:
        hits = [t for t in tools if f"{t['provider']}::{t['name']}" == callee]
    else:
        hits = [t for t in tools if t["name"] == callee]
    if not hits:
        return "NONEXISTENT_TOOL"
    if len(hits) > 1:
        return "AMBIGUOUS_PROVIDER"
    T = hits[0]
    if "menu" not in skip and env[T["mslot"]] != "yes":
        return "OFF_MENU"
    names = [env[a["nslot"]] for a in call["args"]]
    mine = {p["name"] for p in T["params"]}
    if "borrowed" not in skip and names and not (set(names) & mine) and any(
            y is not T and set(names) <= {p["name"] for p in y["params"]} for y in tools):
        return "BORROWED_SIGNATURE"
    obj = {}
    for a in call["args"]:
        nm = env[a["nslot"]]
        if nm in obj:
            return "BAD_ARGS"
        obj[nm] = arg_value(env[a["slot"]], a["bare"])
    errs = validate(obj, tool_schema(T))
    if errs:
        if structural(errs):
            return "BAD_ARGS"
        if "types" not in skip:
            return "TYPE_VIOLATION"
    known = ledger(st, env)
    if "grounding" not in skip and any(env[a["slot"]] not in known for a in call["args"]):
        return "UNGROUNDED_VALUE"
    return "VALID"


def action(st: dict, env: dict, skip: frozenset = frozenset()) -> str:
    tools, req = st["tools"], st["request"]
    cands = [t for t in tools if t["purpose"] == req["purpose"] and ("menu" in skip or env[t["mslot"]] == "yes")]
    if req["provider"]:
        cands = [t for t in cands if t["provider"] == env[req["provider"]]]
    if not cands:
        return "CANNOT_ANSWER"
    if "provider" not in skip and len({t["provider"] for t in cands}) > 1:
        return "ASK_FOLLOWUP"
    T = cands[0]
    stated = {c["label"].lower() for c in req["clauses"]}
    keys = {env[f["key"]] for r in st["results"] for f in r["fields"]} if "results" not in skip else set()
    for p in T["params"]:
        if p["req"] and p["label"].lower() not in stated and p["name"] not in keys:
            return "ASK_FOLLOWUP"
    return "CALL"


def edit_label(st: dict, env: dict) -> str:
    return E.label_of(st["code"], st["old"], st["new"], env)["label"]


def label(st: dict, env: dict) -> str:
    return {"A": resolve_call, "B": action, "C": edit_label}[st["head"]](st, env)
