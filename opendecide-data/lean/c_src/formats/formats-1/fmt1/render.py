"""State renderers: Doc IR -> the `state` text of one row, in one format style's container.

Contract (every container):
  - never invents content: every value, name and sentence comes from the Doc; the renderer adds only the style's chrome
    (titles, headers, bullets, separators, greetings from the register lexicon);
  - never drops content: a Doc part that the style cannot show raises FormatError (pick another style);
  - never writes a missing-value marker by itself: None, bool and "" raise in text containers; "-", "n/a", "N/A",
    "TBD", "?" and dash variants raise everywhere (XF06); a blank cell or field is written only for the explicit BLANK
    sentinel, a left-out key only for OMIT, and JSON/YAML null only with allow_null=True;
  - never reformats numbers (no thousands separators; F10 AR08): int and Decimal print as given;
  - YAML never writes `~` or an empty scalar; yes/no/on/off and other coercible strings are quoted (XF06 rendering).

Doc IR:
  {"title": str | None, "meta": [[label, value], ...], "blocks": [block, ...]}
  block types:
    {"type": "para", "text": str}
    {"type": "items", "items": [str, ...]}                       unordered statements
    {"type": "steps", "items": [str, ...]}                       ordered steps
    {"type": "fields", "label": str | None, "pairs": [[key, value], ...]}     one record
    {"type": "table", "caption": str | None, "columns": [str, ...], "rows": [[value, ...], ...]}
    {"type": "events", "events": [{"ts", "actor"?, "level"?, "text"}, ...]}  ts: str or datetime
    {"type": "messages", "messages": [{"speaker", "to"?, "ts"?, "subject"?, "text"}, ...]}  oldest first
    {"type": "changes", "target": str | None, "entries": [{"key", "value"} | {"key", "old", "new"}, ...]}
    {"type": "section", "heading": str, "blocks": [...]}
  values: str, int, Decimal, float (finite, no exponent), Choice (form check boxes); in JSON/YAML also bool and None
  (None only with allow_null=True); sentinels BLANK, OMIT, ABSENT (diff side absent).
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import re
from decimal import Decimal
from html import escape as _hesc

from . import pool


class FormatError(ValueError):
    """The style cannot render this Doc without inventing, dropping or corrupting content."""


class _Sentinel:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return self.name


BLANK = _Sentinel("BLANK")    # explicit empty cell / field (its meaning must be stated by the card)
OMIT = _Sentinel("OMIT")      # key left out (key-value, JSON, YAML, form, prose fields)
ABSENT = _Sentinel("ABSENT")  # diff: the key does not exist on that side


class Choice:
    """A form field with printed choices; `selected` is the value. Non-checkbox skins print the selected value only."""

    def __init__(self, selected, choices):
        if selected not in choices:
            raise FormatError("Choice: selected value is in no choice")
        self.selected, self.choices = selected, list(choices)


_DASHES = set("-‐‑‒–—―−")
_BANNED_WORDS = {"n/a", "tbd", "?", "??"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def is_banned_marker(s: str) -> bool:
    t = s.strip().lower()
    return t in _BANNED_WORDS or (t != "" and set(t) <= _DASHES)


# ----------------------------------------------------------------------------------------------------------------------
# values

def text_value(v, *, blank_ok: bool = False, single_line: bool = True) -> str:
    if v is BLANK:
        if not blank_ok:
            raise FormatError("BLANK is not allowed in this place")
        return ""
    if v is OMIT or v is ABSENT:
        raise FormatError(f"{v!r} is not allowed in this place")
    if isinstance(v, Choice):
        v = v.selected
    if v is None or isinstance(v, bool):
        raise FormatError("None/bool in a text container: pass the family's explicit word")
    if isinstance(v, int):
        s = str(v)
    elif isinstance(v, Decimal):
        if not v.is_finite():
            raise FormatError("non-finite Decimal")
        s = format(v, "f")
    elif isinstance(v, float):
        s = repr(v)
        if not math.isfinite(v) or "e" in s.lower():
            raise FormatError("float needs exponent; pass a string or Decimal")
    elif isinstance(v, str):
        s = v
    else:
        raise FormatError(f"unsupported value type {type(v).__name__}")
    if s == "":
        raise FormatError("empty string: use BLANK if the card defines a blank")
    if is_banned_marker(s):
        raise FormatError("XF06 banned marker")
    if single_line and ("\n" in s or "\r" in s):
        raise FormatError("newline inside a single-line value")
    return s


def typed_value(v, *, allow_null: bool):
    if v is None:
        if not allow_null:
            raise FormatError("None: pass allow_null=True to write null")
        return None
    if v is BLANK or v is ABSENT:
        raise FormatError(f"{v!r} has no JSON/YAML form")
    if isinstance(v, Choice):
        v = v.selected
    if isinstance(v, bool) or isinstance(v, int):
        return v
    if isinstance(v, Decimal):
        if not v.is_finite():
            raise FormatError("non-finite Decimal")
        if v.as_tuple().exponent >= 0:
            return int(v)
        f = float(v)
        if Decimal(repr(f)) != v:
            raise FormatError("Decimal is not exact as a JSON number; pass a string")
        return f
    if isinstance(v, float):
        if not math.isfinite(v):
            raise FormatError("non-finite float")
        return v
    if isinstance(v, str):
        if v == "":
            raise FormatError("empty string")
        if is_banned_marker(v):
            raise FormatError("XF06 banned marker")
        return v
    raise FormatError(f"unsupported value type {type(v).__name__}")


def fmt_ts(ts, fmt: str) -> str:
    """str timestamps print as given; datetime/date use the skin's format with English month names."""
    if isinstance(ts, str):
        return text_value(ts)
    if isinstance(ts, (dt.datetime, dt.date)):
        if isinstance(ts, dt.datetime):
            if ts.microsecond or (ts.second and "%S" not in fmt):
                raise FormatError("timestamp precision is finer than this format shows; pass a string")
            if ts.tzinfo is not None:
                raise FormatError("time zones are not shown; pass a naive datetime or a string")
        f = fmt.replace("%b", MONTHS[ts.month - 1])
        if not isinstance(ts, dt.datetime):
            f = re.sub(r"[ T]?%H:?%M(:?%S)?", "", f)
        return ts.strftime(f)
    raise FormatError("timestamp must be str, date or datetime")


def keyname(label: str, case: str) -> str:
    if not isinstance(label, str) or not label.strip():
        raise FormatError("empty key")
    if case == "as_given":
        return label
    words = re.findall(r"[A-Za-z0-9]+", label)
    if not words:
        raise FormatError(f"key has no letters or digits: {label!r}")
    if case == "snake":
        return "_".join(w.lower() for w in words)
    if case == "camel":
        return words[0].lower() + "".join(w[:1].upper() + w[1:].lower() for w in words[1:])
    raise FormatError(f"unknown key case {case}")


def _unique(keys: list[str]) -> None:
    if len(keys) != len(set(keys)):
        raise FormatError("two keys render to the same key")


# ----------------------------------------------------------------------------------------------------------------------
# validation

_BLOCK_KEYS = {
    "para": {"text"}, "items": {"items"}, "steps": {"items"}, "fields": {"pairs", "label"},
    "table": {"columns", "rows", "caption"}, "events": {"events"}, "messages": {"messages"},
    "changes": {"entries", "target"}, "section": {"heading", "blocks"},
}


def _walk_types(blocks, depth=0):
    for b in blocks:
        t = b.get("type")
        if t not in _BLOCK_KEYS:
            raise FormatError(f"unknown block type {t!r}")
        extra = set(b) - _BLOCK_KEYS[t] - {"type"}
        if extra:
            raise FormatError(f"unknown keys {sorted(extra)} in {t} block")
        yield t
        if t == "section":
            if depth >= 2:
                raise FormatError("sections nest at most 2 deep")
            yield from _walk_types(b["blocks"], depth + 1)
        if t == "table":
            n = len(b["columns"])
            if n == 0 or any(len(r) != n for r in b["rows"]):
                raise FormatError("ragged table")
            if not b["rows"]:
                raise FormatError("table with no rows")
        if t in ("items", "steps") and not b["items"]:
            raise FormatError("empty list")


def validate(doc: dict, accepts: list[str]) -> None:
    extra = set(doc) - {"title", "meta", "blocks"}
    if extra:
        raise FormatError(f"unknown doc keys {sorted(extra)}")
    types = set(_walk_types(doc.get("blocks", [])))
    if doc.get("meta"):
        types.add("meta")
    bad = types - set(accepts)
    if bad:
        raise FormatError(f"container cannot show {sorted(bad)}")


# ----------------------------------------------------------------------------------------------------------------------
# shared text tables

def _cells(row, blank_ok):
    return [text_value(c, blank_ok=blank_ok) for c in row]


def _is_num(s: str) -> bool:
    return bool(re.fullmatch(r"[+-]?\d+(\.\d+)?", s))


def text_table(columns: list[str], rows: list[list], form: str, *, align: bool = False) -> str:
    head = [text_value(c) for c in columns]
    blank_ok = form in ("md", "pipe")
    body = [_cells(r, blank_ok) for r in rows]
    for cell in head + [c for r in body for c in r]:
        if form in ("md", "pipe", "grid") and "|" in cell:
            raise FormatError("'|' inside a cell")
        if form == "aligned" and ("  " in cell or cell == ""):
            raise FormatError("aligned table cell with double space or blank")
    allr = [head] + body
    w = [max(len(r[i]) for r in allr) for i in range(len(head))]
    if form == "md":
        num = [all(_is_num(r[i]) for r in body) for i in range(len(head))]
        if align:
            def line(r):
                return "| " + " | ".join(c.rjust(w[i]) if num[i] else c.ljust(w[i]) for i, c in enumerate(r)) + " |"
            sep = "| " + " | ".join(("-" * max(3, w[i] - 1) + ":") if num[i] else "-" * max(3, w[i])
                                    for i in range(len(head))) + " |"
        else:
            def line(r):
                return "| " + " | ".join(r) + " |"
            sep = "| " + " | ".join("---" for _ in head) + " |"
        return "\n".join([line(head), sep] + [line(r) for r in body]).replace("|  |", "| |")
    if form == "pipe":
        return "\n".join(" | ".join(r) for r in allr)
    if form == "aligned":
        rule = "  ".join("=" * w[i] for i in range(len(head)))
        rows_t = ["  ".join(c.ljust(w[i]) for i, c in enumerate(r)).rstrip() for r in allr]
        return "\n".join([rows_t[0], rule] + rows_t[1:])
    if form == "grid":
        border = "+" + "+".join("-" * (w[i] + 2) for i in range(len(head))) + "+"
        hsep = "+" + "+".join("=" * (w[i] + 2) for i in range(len(head))) + "+"

        def gl(r):
            return "| " + " | ".join(c.ljust(w[i]) for i, c in enumerate(r)) + " |"
        out = [border, gl(head), hsep]
        for r in body:
            out += [gl(r), border]
        return "\n".join(out)
    raise FormatError(f"unknown table form {form}")


def fixed_width(columns: list[str], rows: list[list]) -> str:
    """Header row then rows; columns padded and separated by at least 2 spaces; no blank cells."""
    allr = [[text_value(c) for c in columns]] + [_cells(r, False) for r in rows]
    for c in (x for r in allr for x in r):
        if "  " in c:
            raise FormatError("fixed-width cell with a double space")
    w = [max(len(r[i]) for r in allr) for i in range(len(columns))]
    return "\n".join("  ".join(c.ljust(w[i]) for i, c in enumerate(r)).rstrip() for r in allr)


def _fields_rows(pairs, *, omit_ok=True):
    rows = []
    for k, v in pairs:
        if v is OMIT:
            if not omit_ok:
                raise FormatError("OMIT is not allowed here")
            continue
        rows.append([k, v])
    return rows


def _event_columns(events, voc):
    has_actor = [("actor" in e and e["actor"] is not None) for e in events]
    has_level = [("level" in e and e["level"] is not None) for e in events]
    if len(set(has_actor)) > 1 or len(set(has_level)) > 1:
        raise FormatError("events: actor/level must be present on all events or on none")
    cols = [voc["time"]] + ([voc["actor"]] if has_actor[0] else []) + ([voc["level"]] if has_level[0] else []) \
        + [voc["text"]]
    return cols, has_actor[0], has_level[0]


def _event_rows(events, ts_fmt, has_actor, has_level):
    rows = []
    for e in events:
        r = [fmt_ts(e["ts"], ts_fmt)]
        if has_actor:
            r.append(e["actor"])
        if has_level:
            r.append(e["level"])
        r.append(e["text"])
        rows.append(r)
    return rows


DEFAULT_TS = "%Y-%m-%d %H:%M"


# ----------------------------------------------------------------------------------------------------------------------
# prose

def _key_l(key: str) -> str:
    first = key.split(" ")[0]
    if len(first) >= 2 and first.isupper():
        return key
    return key[:1].lower() + key[1:]


def _sentence(fmt: str, key: str, value: str) -> str:
    s = fmt.format(key=key, key_l=_key_l(key), value=value)
    return s[:-1] if s.endswith("..") else s


def _r_prose(doc, sk, st, reg, allow_null):
    p = sk["params"]
    if doc.get("meta"):
        raise FormatError("prose has no header")
    paras: list[str] = []
    counter = {"para": 0, "sec": 0}
    fmt = p["field_fmt"]

    def numbered(t):
        if p["list_mode"] == "numbered_paras":
            counter["para"] += 1
            return p["para_num"].format(i=counter["para"]) + t
        return t

    def blocks(bl, out):
        for b in bl:
            t = b["type"]
            if t == "para":
                out.append(numbered(text_value(b["text"])))
            elif t in ("items", "steps", "fields"):
                if t == "fields":
                    if b.get("label"):
                        out.append(text_value(b["label"]))
                    parts = [_sentence(fmt, text_value(k), text_value(v)) for k, v in _fields_rows(b["pairs"])]
                else:
                    parts = [text_value(i) for i in b["items"]]
                if p["list_mode"] == "inline":
                    out.append(" ".join(parts))
                elif p["list_mode"] == "lines":
                    out.append("\n".join(parts))
                else:
                    out.extend(numbered(x) for x in parts)
            elif t == "section":
                h = text_value(b["heading"])
                counter["sec"] += 1
                if p["heading"] == "colon":
                    h = h + ":"
                elif p["heading"] == "section_sign":
                    h = f"§ {counter['sec']} {h}"
                sub: list[str] = []
                blocks(b["blocks"], sub)
                out.append(h + "\n" + "\n\n".join(sub) if sub else h)
    if doc.get("title"):
        t = text_value(doc["title"])
        paras.append({"plain": t, "caps": t.upper(), "underline": t + "\n" + "=" * len(t)}[p["title"]])
    blocks(doc.get("blocks", []), paras)
    return None, "\n\n".join(paras)


# ----------------------------------------------------------------------------------------------------------------------
# memo-like bodies (memo, email single, sop share the list forms)

def _heading(h: str, form: str, n: int) -> str:
    return {"caps": h.upper(), "colon": h + ":", "plain": h, "numbered": f"{n}. {h}", "equals": f"== {h} ==",
            "bracket": f"[{h}]", "underline": h + "\n" + "=" * len(h)}[form]


def _body(bl, *, bullet, step, heading_form, table_form, field_fmt="{key}: {value}", blank_ok=False, sec=None):
    sec = sec if sec is not None else [0]
    out = []
    for b in bl:
        t = b["type"]
        if t == "para":
            out.append(text_value(b["text"]))
        elif t == "items":
            out.append("\n".join(bullet + text_value(i) for i in b["items"]))
        elif t == "steps":
            out.append("\n".join(step.format(i=k + 1) + text_value(i) for k, i in enumerate(b["items"])))
        elif t == "fields":
            lines = [text_value(b["label"])] if b.get("label") else []
            for k, v in _fields_rows(b["pairs"]):
                val = text_value(v, blank_ok=blank_ok)
                lines.append(field_fmt.format(key=text_value(k), value=val).rstrip())
            out.append("\n".join(lines))
        elif t == "table":
            cap = [text_value(b["caption"])] if b.get("caption") else []
            out.append("\n".join(cap + [text_table(b["columns"], b["rows"], table_form)]))
        elif t == "section":
            sec[0] += 1
            h = _heading(text_value(b["heading"]), heading_form, sec[0])
            inner = _body(b["blocks"], bullet=bullet, step=step, heading_form=heading_form, table_form=table_form,
                          field_fmt=field_fmt, blank_ok=blank_ok, sec=[0])
            out.append(h + ("\n" + inner if inner else ""))
        else:
            raise FormatError(f"{t} is not shown in this container")
    return "\n\n".join(out)


def _header_line(fmt, label, value, width):
    lab = text_value(label)
    val = text_value(value)
    dots = "." * max(3, width - len(lab) + 3)
    return fmt.format(label=lab, LABEL=lab.upper(), value=val, dots=dots)


def _r_memo(doc, sk, st, reg, allow_null):
    p = sk["params"]
    lines = []
    title_word = reg["memo_title"]
    if p["title_slot"] == "inline" and doc.get("title"):
        lines.append(f"{title_word} | {text_value(doc['title'])}")
    else:
        lines.append(title_word)
        if doc.get("title"):
            lines.append(text_value(doc["title"]))
    meta = doc.get("meta") or []
    width = max([len(text_value(k)) for k, _ in meta] or [0])
    head = [_header_line(p["header_fmt"], k, v, width) for k, v in meta]
    out = "\n".join(lines)
    if head:
        out += "\n" + "\n".join(head)
    if p["rule"]:
        out += "\n" + p["rule"]
    body = _body(doc.get("blocks", []), bullet=p["bullet"], step=p["step"], heading_form=p["heading"],
                 table_form=p["table"])
    return None, out + ("\n\n" + body if body else "")


# ----------------------------------------------------------------------------------------------------------------------
# email

def _greet(reg, to):
    if not reg["email_greeting"]:
        return None
    if to:
        return reg["email_greeting"].format(to=text_value(to))
    return reg["email_greeting_generic"]


def _close(reg, speaker):
    if not reg["email_closing"]:
        return None
    if reg["closing_with_name"] and speaker:
        return reg["email_closing"] + "\n" + text_value(speaker)
    return reg["email_closing"]


def _msg_body(reg, m):
    text = text_value(m["text"], single_line=False)
    parts = [x for x in (_greet(reg, m.get("to")), text, _close(reg, m.get("speaker"))) if x]
    return "\n\n".join(parts)


def _msg_headers(names, m, subject_prefix=""):
    vals = [m.get("speaker"), m.get("to"), m.get("ts"), m.get("subject")]
    out = []
    for n, v in zip(names, vals):
        if v is None:
            continue
        if n in ("Date", "Sent", "Posted"):
            v = fmt_ts(v, "%d %b %Y %H:%M")
        elif n == "Subject":
            v = subject_prefix + text_value(v)
        out.append(f"{n}: {text_value(v)}")
    return out


def _r_email(doc, sk, st, reg, allow_null):
    p = sk["params"]
    bl = doc.get("blocks", [])
    if p["order"] == "single":
        if any(b["type"] == "messages" for b in bl):
            raise FormatError("email.single wraps a body; use a thread skin for messages")
        meta = doc.get("meta") or []
        head = [f"{text_value(k)}: {text_value(v)}" for k, v in meta]
        to = next((v for k, v in meta if str(k).strip().lower() == "to"), None)
        frm = next((v for k, v in meta if str(k).strip().lower() == "from"), None)
        body = _body(bl, bullet=p["bullet"], step=p["step"], heading_form="colon", table_form="aligned")
        parts = [x for x in (_greet(reg, to), body, _close(reg, frm)) if x]
        top = ([text_value(doc["title"])] if doc.get("title") else []) + head
        return None, ("\n".join(top) + "\n\n" if top else "") + "\n\n".join(parts)
    if doc.get("meta"):
        raise FormatError("thread skins take headers from the messages, not doc meta")
    if len(bl) != 1 or bl[0]["type"] != "messages":
        raise FormatError("thread skins need exactly one messages block")
    msgs = bl[0]["messages"]
    if not msgs:
        raise FormatError("empty thread")
    title = doc.get("title")
    prefix = ""
    lines_top = []
    if title:
        if p.get("subject_prefix"):
            prefix = p["subject_prefix"].format(title=text_value(title))
            if not any(m.get("subject") for m in msgs):
                raise FormatError("list_archive prints the title inside Subject headers; give subjects")
        else:
            lines_top.append(text_value(title))
    if p["order"] == "newest_first":
        newest = msgs[-1]
        out = _msg_headers(p["headers"], newest) + ["", _msg_body(reg, newest)]
        for depth, m in enumerate(reversed(msgs[:-1]), start=1):
            q = p["quote"] * depth
            att = (p["attribution"].format(ts=fmt_ts(m["ts"], "%d %b %Y %H:%M"), speaker=text_value(m["speaker"]))
                   if m.get("ts") is not None else f"{text_value(m['speaker'])} wrote:")
            if m.get("subject") is not None or m.get("to") is not None:
                raise FormatError("quoted messages show only speaker and time")
            out += ["", p["quote"] * (depth - 1) + att]
            out += [(q + ln) if ln else q.rstrip() for ln in _msg_body(reg, m).split("\n")]
        return None, "\n\n".join(lines_top + ["\n".join(out)])
    blocks = []
    n = len(msgs)
    for i, m in enumerate(msgs, start=1):
        b = []
        if p.get("counter"):
            b.append(p["counter"].format(i=i, n=n))
        b += _msg_headers(p["headers"], m, prefix)
        b += ["", _msg_body(reg, m)]
        blocks.append("\n".join(b))
    sep = "\n\n" + p["separator"] + "\n\n" if p.get("separator") else "\n\n"
    return None, "\n\n".join(lines_top + [sep.join(blocks)])


# ----------------------------------------------------------------------------------------------------------------------
# chat

_SPEAKER_BAD = re.compile(r"[:<>|\[\]()\t]")


def _r_chat(doc, sk, st, reg, allow_null):
    p = sk["params"]
    if doc.get("title") or doc.get("meta"):
        raise FormatError("chat logs carry no title or header")
    bl = doc.get("blocks", [])
    if len(bl) != 1 or bl[0]["type"] != "messages":
        raise FormatError("chat needs exactly one messages block")
    out = []
    for m in bl[0]["messages"]:
        if m.get("to") is not None or m.get("subject") is not None:
            raise FormatError("chat lines show speaker, time and text only")
        sp = text_value(m["speaker"])
        if _SPEAKER_BAD.search(sp) or "  " in sp:
            raise FormatError("speaker name has a separator character")
        has_ts = m.get("ts") is not None
        if p["needs_ts"] != has_ts:
            raise FormatError("this chat skin needs times on every message" if p["needs_ts"]
                              else "this chat skin shows no times; the doc has times")
        ts = fmt_ts(m["ts"], p["ts_fmt"]) if has_ts else ""
        out.append(p["line"].format(ts=ts, speaker=sp, text=text_value(m["text"])))
    return None, ("\n\n" if p["block"] else "\n").join(out)


# ----------------------------------------------------------------------------------------------------------------------
# JSON / YAML object model

def _vocab(sk):
    v = sk.get("vocab")
    if not v:
        raise FormatError("skin has no vocabulary")
    return v


def _obj(doc, sk, allow_null):
    p = sk["params"]
    kc = p["key_case"]
    voc = _vocab(sk)

    def K(x):
        return keyname(x, kc)

    def tv(x):
        return typed_value(x, allow_null=allow_null)

    def blocks(bl):
        out = {}
        for b in bl:
            t = b["type"]
            if t == "para":
                k, v = K(voc["notes"]), text_value(b["text"])
            elif t in ("items", "steps"):
                k, v = K(voc[t]), [text_value(i) for i in b["items"]]
            elif t == "fields":
                k = K(b["label"]) if b.get("label") else K(voc["details"])
                v = {K(text_value(a)): tv(c) for a, c in b["pairs"] if c is not OMIT}
                _unique([K(text_value(a)) for a, c in b["pairs"] if c is not OMIT])
            elif t == "table":
                k = K(b["caption"]) if b.get("caption") else K(voc["rows"])
                cols = [K(text_value(c)) for c in b["columns"]]
                _unique(cols)
                v = [{c: tv(x) for c, x in zip(cols, r) if x is not OMIT} for r in b["rows"]]
            elif t == "events":
                k = K(voc["events"])
                v = []
                for e in b["events"]:
                    o = {K(voc["time"]): fmt_ts(e["ts"], "%Y-%m-%dT%H:%M:%S")}
                    if e.get("actor") is not None:
                        o[K(voc["actor"])] = text_value(e["actor"])
                    if e.get("level") is not None:
                        o[K(voc["level"])] = text_value(e["level"])
                    o[K(voc["text"])] = text_value(e["text"], single_line=False)
                    v.append(o)
            elif t == "messages":
                k = K(voc["messages"])
                v = []
                for m in b["messages"]:
                    o = {K(voc["from"]): text_value(m["speaker"])}
                    if m.get("to") is not None:
                        o[K(voc["to"])] = text_value(m["to"])
                    if m.get("ts") is not None:
                        o[K(voc["time"])] = fmt_ts(m["ts"], "%Y-%m-%dT%H:%M:%S")
                    if m.get("subject") is not None:
                        o[K(voc["subject"])] = text_value(m["subject"])
                    o[K(voc["text"])] = text_value(m["text"], single_line=False)
                    v.append(o)
            elif t == "section":
                k = K(text_value(b["heading"]))
                inner = b["blocks"]
                if len(inner) == 1 and inner[0]["type"] in ("table", "items", "steps", "events", "messages") \
                        and not inner[0].get("caption"):
                    v = list(blocks(inner).values())[0]
                elif len(inner) == 1 and inner[0]["type"] == "fields" and not inner[0].get("label"):
                    v = list(blocks(inner).values())[0]
                else:
                    v = blocks(inner)
            else:
                raise FormatError(f"{t} has no JSON/YAML form")
            if k in out:
                raise FormatError(f"duplicate key {k!r} (give captions or labels)")
            if v in ({}, []):
                raise FormatError("empty object or list")
            out[k] = v
        return out

    top = {}
    if doc.get("title") and p.get("title", "key") == "key":
        top[K(voc["title"])] = text_value(doc["title"])
    for a, c in doc.get("meta") or []:
        if c is OMIT:
            continue
        ka = K(text_value(a))
        if ka in top:
            raise FormatError("duplicate meta key")
        top[ka] = tv(c)
    bl = doc.get("blocks", [])
    if not top and len(bl) == 1 and bl[0]["type"] == "fields" and not bl[0].get("label"):
        return list(blocks(bl).values())[0]
    body = blocks(bl)
    dup = set(top) & set(body)
    if dup:
        raise FormatError(f"duplicate key {sorted(dup)}")
    top.update(body)
    return top


def _collection(doc, sk, allow_null):
    """json.lines / json.array: exactly one table, events or messages block, nothing else."""
    if doc.get("title") or doc.get("meta"):
        raise FormatError("a single-collection skin has no title or header")
    bl = doc.get("blocks", [])
    if len(bl) != 1 or bl[0]["type"] not in ("table", "events", "messages") or bl[0].get("caption"):
        raise FormatError("a single-collection skin needs one uncaptioned table, events or messages block")
    return list(_obj({"blocks": bl}, sk, allow_null).values())[0]


def _json_default(o):
    raise FormatError(f"unserialisable {type(o).__name__}")


def _r_json(doc, sk, st, reg, allow_null):
    p = sk["params"]
    if p["layout"] == "lines":
        rows = _collection(doc, sk, allow_null)
        return None, "\n".join(json.dumps(r, ensure_ascii=False, default=_json_default) for r in rows)
    if p["layout"] == "array":
        obj = _collection(doc, sk, allow_null)
    else:
        obj = _obj(doc, sk, allow_null)
    if p["indent"] is None:
        return None, json.dumps(obj, ensure_ascii=False, default=_json_default)
    return None, json.dumps(obj, ensure_ascii=False, indent=p["indent"], default=_json_default)


_YAML_SPECIAL_START = set("-?:,[]{}#&*!|>'\"%@`")


def _yaml_needs_quote(s: str, flow: bool) -> bool:
    if s == "" or s != s.strip() or "\n" in s or "\t" in s:
        return True
    if s[0] in _YAML_SPECIAL_START or ": " in s or " #" in s or s.endswith(":"):
        return True
    if flow and any(c in s for c in ",[]{}"):
        return True
    import yaml  # PyYAML (MIT); used only to test that a plain scalar reads back as the same string
    try:
        back = yaml.safe_load(s)
    except Exception:
        return True
    return back != s or not isinstance(back, str)


def _yaml_scalar(v, flow=False) -> str:
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False) if _yaml_needs_quote(v, flow) else v
    raise FormatError(f"unsupported YAML value {type(v).__name__}")


def _yaml_lines(obj, indent: int, seq_indent: bool, flow_rows: bool, pad: str = "") -> list[str]:
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = _yaml_scalar(k)
            if isinstance(v, dict):
                out.append(f"{pad}{ks}:")
                out += _yaml_lines(v, indent, seq_indent, flow_rows, pad + " " * indent)
            elif isinstance(v, list):
                out.append(f"{pad}{ks}:")
                out += _yaml_lines(v, indent, seq_indent, flow_rows, pad + (" " * indent if seq_indent else ""))
            else:
                out.append(f"{pad}{ks}: {_yaml_scalar(v)}")
        return out
    if isinstance(obj, list):
        for it in obj:
            if isinstance(it, dict):
                if flow_rows and all(not isinstance(x, (dict, list)) for x in it.values()):
                    inner = ", ".join(f"{_yaml_scalar(k, True)}: {_yaml_scalar(x, True)}" for k, x in it.items())
                    out.append(f"{pad}- {{{inner}}}")
                else:
                    sub = _yaml_lines(it, indent, seq_indent, flow_rows, pad + "  ")
                    out.append(f"{pad}- {sub[0][len(pad) + 2:]}")
                    out += sub[1:]
            elif isinstance(it, list):
                raise FormatError("nested lists are not used")
            else:
                out.append(f"{pad}- {_yaml_scalar(it)}")
        return out
    return [pad + _yaml_scalar(obj)]


def _r_yaml(doc, sk, st, reg, allow_null):
    p = sk["params"]
    obj = _obj(doc, sk, allow_null)
    lines = []
    if doc.get("title") and p["title"] == "comment":
        lines.append("# " + text_value(doc["title"]))
    if not isinstance(obj, dict):
        raise FormatError("YAML top level is a mapping")
    lines += _yaml_lines(obj, p["indent"], p["seq_indent"], p["rows"] == "flow")
    return None, "\n".join(lines)


# ----------------------------------------------------------------------------------------------------------------------
# CSV and aligned text tables

def _one_tabular(doc, voc):
    bl = doc.get("blocks", [])
    if doc.get("meta"):
        raise FormatError("delimited tables carry no header pairs")
    if len(bl) != 1:
        raise FormatError("delimited-table skins show exactly one table")
    b = bl[0]
    if b["type"] == "table":
        if b.get("caption"):
            raise FormatError("captions are not shown; use the doc title")
        return b["columns"], b["rows"]
    if b["type"] == "fields":
        if b.get("label"):
            raise FormatError("labels are not shown; use the doc title")
        return [voc["field"], voc["value"]], _fields_rows(b["pairs"])
    if b["type"] == "events":
        cols, ha, hl = _event_columns(b["events"], voc)
        return cols, _event_rows(b["events"], DEFAULT_TS, ha, hl)
    raise FormatError(f"{b['type']} is not tabular")


def _r_csv(doc, sk, st, reg, allow_null):
    p = sk["params"]
    voc = _vocab(sk)
    cols, rows = _one_tabular(doc, voc)
    title = text_value(doc["title"]) if doc.get("title") else None
    if p["fixed"]:
        return title, fixed_width(cols, rows)
    head = [text_value(c) for c in cols]
    body = [[text_value(c, blank_ok=True) for c in r] for r in rows]
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=p["delim"], lineterminator="\n",
                   quoting=csv.QUOTE_ALL if p["quote_all"] else csv.QUOTE_MINIMAL)
    w.writerow(head)
    w.writerows(body)
    return title, buf.getvalue().rstrip("\n")


# ----------------------------------------------------------------------------------------------------------------------
# markdown

def _md_title(t, form):
    return {"hash1": "# " + t, "hash2": "## " + t, "hash3": "### " + t, "hash4": "#### " + t, "bold": "**" + t + "**",
            "plain": t}[form]


def _r_md(doc, sk, st, reg, allow_null):
    p = sk["params"]
    voc = _vocab(sk)
    out = []
    if doc.get("title"):
        out.append(_md_title(text_value(doc["title"]), p["title"]))
    if doc.get("meta"):
        out.append("\n".join(f"{p['bullet']}{text_value(k)}: {text_value(v)}" for k, v in doc["meta"]))
    cap = {"plain": "plain", "hash3": "hash3", "bold": "bold"}[p["caption"]]

    def tbl(cols, rows):
        if p["table"] == "grid":
            return text_table(cols, rows, "grid")
        return text_table(cols, rows, "md", align=p["align"])

    def blocks(bl, level_form):
        res = []
        for b in bl:
            t = b["type"]
            if t == "para":
                res.append(text_value(b["text"]))
            elif t == "items":
                res.append("\n".join(p["bullet"] + text_value(i) for i in b["items"]))
            elif t == "steps":
                res.append("\n".join(p["step"].format(i=k + 1) + text_value(i) for k, i in enumerate(b["items"])))
            elif t == "fields":
                pre = [_md_title(text_value(b["label"]), cap)] if b.get("label") else []
                cols = [voc["field"].capitalize(), voc["value"].capitalize()]
                res.append("\n".join(pre + [tbl(cols, _fields_rows(b["pairs"]))]))
            elif t == "table":
                pre = [_md_title(text_value(b["caption"]), cap)] if b.get("caption") else []
                res.append("\n".join(pre + [tbl(b["columns"], b["rows"])]))
            elif t == "events":
                cols, ha, hl = _event_columns(b["events"], voc)
                res.append(tbl([c.capitalize() for c in cols], _event_rows(b["events"], DEFAULT_TS, ha, hl)))
            elif t == "section":
                res.append(_md_title(text_value(b["heading"]), level_form))
                res += blocks(b["blocks"], {"hash1": "hash2", "hash2": "hash3", "hash3": "hash4"}.get(level_form, level_form))
        return res
    out += blocks(doc.get("blocks", []), p["heading"])
    return None, "\n\n".join(out)


# ----------------------------------------------------------------------------------------------------------------------
# HTML

def _h(s) -> str:
    return _hesc(text_value(s), quote=False)


def _hcell(s) -> str:
    return _hesc(text_value(s, blank_ok=True), quote=False)


def _r_html(doc, sk, st, reg, allow_null):
    p = sk["params"]
    voc = _vocab(sk)
    el: list = []  # nested list of (tag-open, children, tag-close) rendered below

    def table(cols, rows, caption=None):
        kids = []
        if caption is not None and p.get("caption_tag"):
            kids.append(f"<caption>{_h(caption)}</caption>")
        head = "<tr>" + "".join(f"<th>{_h(c)}</th>" for c in cols) + "</tr>"
        body = ["<tr>" + "".join(f"<td>{_hcell(c)}</td>" for c in r) + "</tr>" for r in rows]
        if p["thead"]:
            kids += [("<thead>", [head], "</thead>"), ("<tbody>", body, "</tbody>")]
        else:
            kids += [head] + body
        node = ("<table>", kids, "</table>")
        if caption is not None and not p.get("caption_tag"):
            return [f"<{p['heading_tag']}>{_h(caption)}</{p['heading_tag']}>", node]
        return [node]

    def fields(b):
        rows = _fields_rows(b["pairs"])
        pre = [f"<{p['heading_tag']}>{_h(b['label'])}</{p['heading_tag']}>"] if b.get("label") else []
        if p["fields"] == "dl":
            kids = []
            for k, v in rows:
                kids += [f"<dt>{_h(k)}</dt>", f"<dd>{_hcell(v)}</dd>"]
            return pre + [("<dl>", kids, "</dl>")]
        if p["fields"] == "row_th":
            kids = [f"<tr><th scope=\"row\">{_h(k)}</th><td>{_hcell(v)}</td></tr>" for k, v in rows]
            return pre + [("<table>", [("<tbody>", kids, "</tbody>")], "</table>")]
        kids = [f"<tr><th>{_h(k)}</th><td>{_hcell(v)}</td></tr>" for k, v in rows]
        return pre + [("<table>", kids, "</table>")]

    def blocks(bl, htag):
        res = []
        for b in bl:
            t = b["type"]
            if t == "para":
                res.append(f"<p>{_h(b['text'])}</p>")
            elif t in ("items", "steps"):
                tag = "ul" if t == "items" else "ol"
                res.append((f"<{tag}>", [f"<li>{_h(i)}</li>" for i in b["items"]], f"</{tag}>"))
            elif t == "fields":
                res += fields(b)
            elif t == "table":
                res += table(b["columns"], b["rows"], b.get("caption"))
            elif t == "events":
                cols, ha, hl = _event_columns(b["events"], voc)
                res += table([c.capitalize() for c in cols], _event_rows(b["events"], DEFAULT_TS, ha, hl))
            elif t == "section":
                res.append(("<section>", [f"<{htag}>{_h(b['heading'])}</{htag}>"] + blocks(b["blocks"], htag),
                            "</section>"))
        return res

    if doc.get("title"):
        tt = f"<{p['title_tag']}>{_h(doc['title'])}</{p['title_tag']}>"
        el.append(("<header>", [tt], "</header>") if p["wrapper"] == "article" else tt)
    if doc.get("meta"):
        kids = []
        for k, v in doc["meta"]:
            kids += [f"<dt>{_h(k)}</dt>", f"<dd>{_h(v)}</dd>"]
        el.append(("<dl>", kids, "</dl>"))
    el += blocks(doc.get("blocks", []), p["heading_tag"])
    if p["wrapper"] == "div":
        el = [("<div class=\"doc\">", el, "</div>")]
    elif p["wrapper"] == "article":
        el = [("<article>", el, "</article>")]

    def emit(nodes, depth):
        out = []
        for n in nodes:
            if isinstance(n, str):
                out.append(("  " * depth if p["pretty"] else "") + n)
            else:
                o, kids, c = n
                if p["pretty"]:
                    out.append("  " * depth + o)
                    out += emit(kids, depth + 1)
                    out.append("  " * depth + c)
                else:
                    out.append(o + "".join(emit(kids, 0)) + c)
        return out
    lines = emit(el, 0)
    return None, "\n".join(lines) if p["pretty"] else "".join(lines)


# ----------------------------------------------------------------------------------------------------------------------
# key-value

def _r_kv(doc, sk, st, reg, allow_null):
    p = sk["params"]
    kc = p["key_case"]
    voc = _vocab(sk)
    sep_chars = {"{key}: {value}": ":", "{key} = {value}": "=", "{key}={value}": "=", "{key} :: {value}": "::",
                 "{key} {dots} {value}": "..", "{key}:{pad} {value}": ":"}[p["line"]]

    def sec_line(h):
        return {"colon": h + ":", "hash": "# " + h, "caps": h.upper(), "ini": "[" + keyname(h, "snake") + "]",
                "bracket": "[" + h + "]"}[p["section"]]

    def kv_lines(pairs):
        rows = []
        for k, v in pairs:
            if v is OMIT:
                continue
            key = keyname(text_value(k), kc)
            if sep_chars in key:
                raise FormatError("key contains the separator")
            rows.append((key, text_value(v, blank_ok=True)))
        _unique([k for k, _ in rows])
        w = max([len(k) for k, _ in rows] or [0])
        out = []
        for k, v in rows:
            line = p["line"].format(key=k, value=v, dots="." * (w - len(k) + 3), pad=" " * (w - len(k)))
            out.append(line.rstrip())
        return out

    def blocks(bl):
        res = []
        for b in bl:
            t = b["type"]
            if t == "fields":
                res.append("\n".join(([sec_line(text_value(b["label"]))] if b.get("label") else [])
                                     + kv_lines(b["pairs"])))
            elif t == "table":
                recs = ["\n".join(kv_lines(list(zip(b["columns"], r)))) for r in b["rows"]]
                if b.get("caption"):
                    recs[0] = sec_line(text_value(b["caption"])) + "\n" + recs[0]
                res += recs
            elif t == "events":
                cols, ha, hl = _event_columns(b["events"], voc)
                for r in _event_rows(b["events"], DEFAULT_TS, ha, hl):
                    res.append("\n".join(kv_lines(list(zip(cols, r)))))
            elif t == "section":
                inner = blocks(b["blocks"])
                res.append(sec_line(text_value(b["heading"])) + ("\n" + "\n\n".join(inner) if inner else ""))
            else:
                raise FormatError(f"{t} is not shown in key-value records")
        return res
    out = []
    if doc.get("meta"):
        out.append("\n".join(kv_lines(doc["meta"])))
    out += blocks(doc.get("blocks", []))
    title = sec_line(text_value(doc["title"])) if doc.get("title") else None
    return title, "\n\n".join(out)


# ----------------------------------------------------------------------------------------------------------------------
# bullet SOP

def _r_sop(doc, sk, st, reg, allow_null):
    p = sk["params"]
    out = []
    if doc.get("title"):
        t = text_value(doc["title"])
        out.append({"plain": t, "caps": t.upper(), "bracket": "[" + t + "]"}[p["title"]])
    if doc.get("meta"):
        out.append("\n".join(f"{p['bullet']}{text_value(k)}: {text_value(v)}" for k, v in doc["meta"]))
    if p["nested"]:
        res = []
        for b in doc.get("blocks", []):
            if b["type"] == "section":
                inner = _body(b["blocks"], bullet=p["bullet"], step=p["step"], heading_form="plain",
                              table_form="aligned", field_fmt=p["bullet"] + "{key}: {value}")
                ind = "\n".join(("  " + ln) if ln else "" for ln in inner.split("\n"))
                res.append(p["bullet"] + text_value(b["heading"]) + ("\n" + ind if inner else ""))
            else:
                res.append(_body([b], bullet=p["bullet"], step=p["step"], heading_form="plain",
                                 table_form="aligned", field_fmt=p["bullet"] + "{key}: {value}"))
        out += res
    else:
        out.append(_body(doc.get("blocks", []), bullet=p["bullet"], step=p["step"], heading_form=p["heading"],
                         table_form="aligned", field_fmt=p["bullet"] + "{key}: {value}"))
    return None, "\n\n".join(x for x in out if x)


# ----------------------------------------------------------------------------------------------------------------------
# log lines

def _logfmt_val(s: str) -> str:
    return json.dumps(s, ensure_ascii=False) if re.search(r"[\s\"=]", s) else s


def _r_log(doc, sk, st, reg, allow_null):
    p = sk["params"]
    if doc.get("meta"):
        raise FormatError("log lines carry no header")
    bl = doc.get("blocks", [])
    if not bl or any(b["type"] != "events" for b in bl):
        raise FormatError("log lines show events blocks only")
    lines = []
    for b in bl:
        _, ha, hl = _event_columns(b["events"], {"time": "t", "actor": "a", "level": "l", "text": "x"})
        for e in b["events"]:
            ts = fmt_ts(e["ts"], p["ts_fmt"])
            lv = text_value(e["level"]) if hl else None
            if lv is not None:
                lv = lv.upper() if p["level_case"] == "upper" else lv.lower()
                if " " in lv:
                    raise FormatError("level must be one word")
            ac = text_value(e["actor"]) if ha else None
            tx = text_value(e["text"])
            if ac is not None and re.search(r"[:<>|\t\[\]()]", ac):
                raise FormatError("actor has a separator character")
            parts = p["parts"]
            if parts == ["logfmt"]:
                s = f"time={ts}" + (f" level={lv}" if lv else "") + (f" actor={_logfmt_val(ac)}" if ac else "") \
                    + f" msg={_logfmt_val(tx)}"
            elif parts == ["pipe"]:
                s = " | ".join([ts] + ([lv] if lv else []) + ([ac] if ac else []) + [tx])
            elif parts == ["tab"]:
                s = "\t".join([ts] + ([ac] if ac else []) + ([lv] if lv else []) + [tx])
            else:
                seg = []
                for part in parts:
                    if part == "ts":
                        seg.append(ts)
                    elif part == "ts_br":
                        seg.append(f"[{ts}]")
                    elif part == "level" and lv:
                        seg.append(lv)
                    elif part == "level_br" and lv:
                        seg.append(f"[{lv}]")
                    elif part == "level_paren" and lv:
                        seg.append(f"({lv})")
                    elif part == "actor_colon" and ac:
                        seg.append(f"{ac}:")
                    elif part == "actor_angle" and ac:
                        seg.append(f"<{ac}>")
                    elif part == "text":
                        seg.append(tx)
                s = " ".join(seg)
            lines.append(s)
    title = text_value(doc["title"]) if doc.get("title") else None
    return title, "\n".join(lines)


# ----------------------------------------------------------------------------------------------------------------------
# diff

def _r_diff(doc, sk, st, reg, allow_null):
    p = sk["params"]
    if doc.get("meta"):
        raise FormatError("diffs carry no header pairs")
    bl = doc.get("blocks", [])
    if not bl or any(b["type"] != "changes" for b in bl):
        raise FormatError("diff shows changes blocks only")
    out = []
    for b in bl:
        tgt = b.get("target")
        if p.get("header") == "path":
            if not tgt:
                raise FormatError("diff.unified_path needs a target path")
        elif tgt:
            raise FormatError("this diff skin shows no path; drop the target or use diff.unified_path")
        ents = b["entries"]
        if not ents:
            raise FormatError("empty change set")
        kinds = []
        for e in ents:
            k = text_value(e["key"])
            if "value" in e:
                kinds.append(("same", k, text_value(e["value"]), None))
            else:
                old, new = e.get("old", ABSENT), e.get("new", ABSENT)
                if old is ABSENT and new is ABSENT:
                    raise FormatError("change with both sides absent")
                o = None if old is ABSENT else text_value(old)
                n = None if new is ABSENT else text_value(new)
                if o is not None and n is not None and o == n:
                    raise FormatError("a change must change the value")
                kinds.append(("chg", k, o, n))
        if not any(x[0] == "chg" for x in kinds):
            raise FormatError("a diff needs at least one change")
        form = p["form"]
        lines = []
        if form == "unified":
            if p["header"] == "path":
                t = text_value(tgt)
                lines += [f"--- a/{t}", f"+++ b/{t}"]
            else:
                lines += [f"--- {p['labels'][0]}", f"+++ {p['labels'][1]}"]
            body = []
            n_old = n_new = 0
            for kd, k, a, c in kinds:
                if kd == "same":
                    body.append(f" {k}: {a}")
                    n_old += 1
                    n_new += 1
                else:
                    if a is not None:
                        body.append(f"-{k}: {a}")
                        n_old += 1
                    if c is not None:
                        body.append(f"+{k}: {c}")
                        n_new += 1
            if p.get("hunk"):
                lines.append(f"@@ -1,{n_old} +1,{n_new} @@")
            lines += body
        elif form == "word":
            for kd, k, a, c in kinds:
                if kd == "same":
                    lines.append(f"{k}: {a}")
                elif a is None:
                    lines.append(f"{{+{k}: {c}+}}")
                elif c is None:
                    lines.append(f"[-{k}: {a}-]")
                else:
                    lines.append(f"{k}: [-{a}-]{{+{c}+}}")
        elif form == "table":
            rows = []
            for kd, k, a, c in kinds:
                if kd == "same":
                    rows.append([k, a, a])
                elif a is None or c is None:
                    raise FormatError("diff.table shows only changed or kept keys (no added or removed keys)")
                else:
                    rows.append([k, a, c])
            lines.append(text_table(p["columns"], rows, "aligned"))
        elif form == "changelog":
            for kd, k, a, c in kinds:
                if kd == "same":
                    lines.append(p["same"].format(key=k, value=a))
                elif a is None:
                    lines.append(p["added"].format(key=k, new=c))
                elif c is None:
                    lines.append(p["removed"].format(key=k, old=a))
                else:
                    lines.append(p["changed"].format(key=k, old=a, new=c))
            lines = [ln[:-1] if ln.endswith("..") else ln for ln in lines]
        elif form == "normal":
            for kd, k, a, c in kinds:
                if kd == "same":
                    lines.append(f"  {k}: {a}")
                else:
                    if a is not None:
                        lines.append(f"< {k}: {a}")
                    if c is not None:
                        lines.append(f"> {k}: {c}")
        out.append("\n".join(lines))
    title = text_value(doc["title"]) if doc.get("title") else None
    return title, "\n\n".join(out)


# ----------------------------------------------------------------------------------------------------------------------
# form

def _r_form(doc, sk, st, reg, allow_null):
    p = sk["params"]
    out = []
    if doc.get("title"):
        out.append(reg["form_title_fmt"].format(title=text_value(doc["title"])))

    def field_lines(pairs):
        rows = [(k, v) for k, v in pairs if v is not OMIT]
        labs = [text_value(k) for k, _ in rows]
        if p["caps_labels"]:
            labs = [x.upper() for x in labs]
        w = max([len(x) for x in labs] or [0])
        lines = []
        for n, (lab, (_, v)) in enumerate(zip(labs, rows), start=1):
            if isinstance(v, Choice) and p["checkbox"]:
                boxes = "  ".join(("[x] " if c == v.selected else "[ ] ") + text_value(c) for c in v.choices)
                val = boxes
            else:
                val = text_value(v, blank_ok=True)
            line = p["field"].format(label=lab, LABEL=lab, value=val, n=n, dots="." * (w - len(lab) + 3))
            lines.append(line.replace("[  ]", "[ ]").rstrip())
        return lines

    def blocks(bl):
        res = []
        for b in bl:
            t = b["type"]
            if t == "fields":
                res.append("\n".join(([text_value(b["label"])] if b.get("label") else [])
                                     + field_lines(b["pairs"])))
            elif t == "para":
                res.append(text_value(b["text"]))
            elif t == "table":
                cap = [text_value(b["caption"])] if b.get("caption") else []
                res.append("\n".join(cap + [text_table(b["columns"], b["rows"], "aligned")]))
            elif t == "section":
                h = _heading(text_value(b["heading"]), p["heading"], 0)
                inner = blocks(b["blocks"])
                res.append(h + ("\n" + "\n\n".join(inner) if inner else ""))
            else:
                raise FormatError(f"{t} is not shown in forms")
        return res
    if doc.get("meta"):
        out.append("\n".join(field_lines(doc["meta"])))
    out += blocks(doc.get("blocks", []))
    return None, "\n\n".join(out)


RENDERERS = {
    "prose": _r_prose, "memo": _r_memo, "email_thread": _r_email, "chat_log": _r_chat, "json": _r_json,
    "yaml": _r_yaml, "csv": _r_csv, "markdown_table": _r_md, "html_snippet": _r_html, "key_value": _r_kv,
    "bullet_sop": _r_sop, "log_lines": _r_log, "diff": _r_diff, "form": _r_form,
}


def _fence(title, body, st):
    f = pool.fence(st["fence"])
    lang = pool.container(st["container"])["lang"]
    if f["name"] == "none":
        block = body
    elif f["name"] == "indent4":
        block = "\n".join(("    " + ln) if ln else "" for ln in body.split("\n"))
    else:
        block = f["open"].format(lang=lang) + "\n" + body + "\n" + f["close"]
    return (title + "\n\n" + block) if title else block


def render_state(doc: dict, style, *, allow_null: bool = False) -> str:
    """Render a Doc in a style (style id or style dict). Raises FormatError if the style cannot show the Doc."""
    st = pool.style(style) if isinstance(style, str) else style
    sk = pool.skin(st["skin"])
    validate(doc, pool.container(st["container"])["accepts"])
    reg = pool.register(st["register"])
    title, body = RENDERERS[st["container"]](doc, sk, st, reg, allow_null)
    if not body:
        raise FormatError("nothing to render")
    return _fence(title, body, st)


def can_render(doc: dict, style, **kw) -> bool:
    try:
        render_state(doc, style, **kw)
        return True
    except FormatError:
        return False
