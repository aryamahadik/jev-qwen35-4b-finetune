"""families/T40/schema.py: a minimal JSON-schema validator (draft-07 subset), written for T40 (no jsonschema installed).

Supported keywords: type (string, integer, number, boolean, array, object, null; a list of types), enum, const, format
(email, date), pattern (re.fullmatch), minimum, maximum, minLength, maxLength, items, minItems, maxItems, properties,
required, additionalProperties (False). validate(value, schema) returns a list of (path, keyword) errors; an empty
list means valid. Keywords split into two families for the resolver:
  STRUCTURAL  required, additionalProperties      -> the arguments' shape is wrong (BAD_ARGS)
  VALUE       everything else                     -> a value breaks its parameter's type or constraint (TYPE_VIOLATION)
Booleans are never integers or numbers (JSON, unlike Python).
"""
from __future__ import annotations

import datetime as dt
import re

STRUCTURAL = ("required", "additionalProperties")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def type_ok(v, t: str) -> bool:
    if t == "string":
        return isinstance(v, str)
    if t == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    if t == "boolean":
        return isinstance(v, bool)
    if t == "array":
        return isinstance(v, list)
    if t == "object":
        return isinstance(v, dict)
    if t == "null":
        return v is None
    raise ValueError(f"unknown type {t!r}")


def format_ok(v: str, fmt: str) -> bool:
    if fmt == "email":
        return EMAIL_RE.fullmatch(v) is not None
    if fmt == "date":
        if not DATE_RE.fullmatch(v):
            return False
        try:
            dt.date.fromisoformat(v)
        except ValueError:
            return False
        return True
    raise ValueError(f"unknown format {fmt!r}")


def validate(value, schema: dict, path: str = "$") -> list:
    errs: list = []
    t = schema.get("type")
    if t is not None:
        ts = t if isinstance(t, list) else [t]
        if not any(type_ok(value, x) for x in ts):
            return [(path, "type")]
    if "const" in schema and value != schema["const"]:
        errs.append((path, "const"))
    if "enum" in schema and value not in schema["enum"]:
        errs.append((path, "enum"))
    if isinstance(value, str):
        if "format" in schema and not format_ok(value, schema["format"]):
            errs.append((path, "format"))
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errs.append((path, "pattern"))
        if "minLength" in schema and len(value) < schema["minLength"]:
            errs.append((path, "minLength"))
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errs.append((path, "maxLength"))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errs.append((path, "minimum"))
        if "maximum" in schema and value > schema["maximum"]:
            errs.append((path, "maximum"))
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errs.append((path, "minItems"))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errs.append((path, "maxItems"))
        if "items" in schema:
            for i, x in enumerate(value):
                errs += validate(x, schema["items"], f"{path}[{i}]")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errs.append((f"{path}.{name}", "required"))
        if schema.get("additionalProperties") is False:
            for name in value:
                if name not in props:
                    errs.append((f"{path}.{name}", "additionalProperties"))
        for name, sub in props.items():
            if name in value:
                errs += validate(value[name], sub, f"{path}.{name}")
    return errs


def keywords(errs: list) -> set:
    return {k for _, k in errs}


def structural(errs: list) -> bool:
    return any(k in STRUCTURAL for _, k in errs)


def type_string(schema: dict) -> str:
    """The printed type of a parameter schema (the registry notation of the T40 card)."""
    if "enum" in schema:
        return "enum(" + "|".join(schema["enum"]) + ")"
    if schema.get("format") in ("email", "date"):
        return schema["format"]
    if "pattern" in schema:
        m = re.fullmatch(r"\^?([A-Za-z]+_)\[0-9\]\+\$?", schema["pattern"])
        if not m:
            raise ValueError(f"pattern {schema['pattern']!r} has no printed form")
        return f"id({m.group(1)})"
    t = schema["type"]
    if t in ("integer", "number") and "minimum" in schema and "maximum" in schema:
        return f"{t} {schema['minimum']}..{schema['maximum']}"
    return t
